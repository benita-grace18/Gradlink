"""
ATS (Applicant Tracking System) scoring module
Parses resume files and scores them against job descriptions using TF-IDF
"""
import os
from flask import current_app

try:
    from pdfminer.high_level import extract_text as extract_pdf_text
except ImportError:
    extract_pdf_text = None

try:
    import docx
except ImportError:
    docx = None

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

def extract_text_from_file(file_path):
    """Extract text from PDF, DOCX, or TXT files."""
    try:
        ext = file_path.rsplit('.', 1)[-1].lower()
        
        if ext == 'pdf':
            if extract_pdf_text is None:
                raise RuntimeError("pdfminer.six not installed")
            return extract_pdf_text(file_path)
        
        elif ext in ('docx', 'doc'):
            if docx is None:
                raise RuntimeError("python-docx not installed")
            doc = docx.Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs)
        
        elif ext == 'txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        else:
            raise ValueError(f"Unsupported file format: {ext}")
            
    except Exception as e:
        current_app.logger.error(f"Error extracting text from {file_path}: {e}")
        raise

def extract_skills_simple(text, skill_vocab=None):
    """Extract skills from text using a vocabulary list."""
    text = text.lower()
    if skill_vocab is None:
        skill_vocab = [
            'python', 'javascript', 'sql', 'java', 'c++', 'typescript',
            'machine learning', 'nlp', 'deep learning', 'tensorflow', 'pytorch',
            'react', 'angular', 'vue', 'node.js', 'flask', 'django',
            'docker', 'kubernetes', 'aws', 'gcp', 'azure',
            'git', 'jenkins', 'ci/cd', 'agile', 'scrum',
            'communication', 'leadership', 'problem solving', 'teamwork'
        ]
    found = [s for s in skill_vocab if s in text]
    return list(set(found))  # Remove duplicates

def extract_education(text):
    """Extract education mentions (simplified)."""
    education_keywords = ['bachelor', 'master', 'phd', 'b.s.', 'm.s.', 'b.a.', 'm.a.', 'degree']
    text_lower = text.lower()
    has_education = any(keyword in text_lower for keyword in education_keywords)
    return has_education

def ats_score(resume_text, job_text):
    """
    Score a resume against a job description using TF-IDF similarity.
    Returns (score: float, feedback: dict)
    """
    try:
        # TF-IDF vectorization
        vect = TfidfVectorizer(stop_words='english', max_features=100)
        try:
            mat = vect.fit_transform([resume_text, job_text]).toarray()
        except ValueError:
            # Handle case where corpus is too small
            return 0.0, {"error": "Resume too short to score"}
        
        # Cosine similarity
        sim = float(
            np.dot(mat[0], mat[1]) / 
            ((np.linalg.norm(mat[0]) * np.linalg.norm(mat[1])) + 1e-9)
        )
        
        # Extract features
        skills = extract_skills_simple(resume_text)
        has_education = extract_education(resume_text)
        
        # Calculate score (0-100)
        score = round(100 * sim, 2)
        
        # Generate feedback
        feedback = {
            "score": score,
            "skills_found": skills,
            "has_education": has_education,
            "num_skills": len(skills),
            "advice": (
                "Strengths: " + (f"Found {len(skills)} skills" if skills else "Consider adding more skills") + ". "
                "Improvements: Add more role-specific keywords, quantify achievements, "
                "highlight relevant projects and measurable impact."
            )
        }
        
        current_app.logger.info(f"ATS score calculated: {score}")
        return score, feedback
        
    except Exception as e:
        current_app.logger.exception("ATS scoring failed")
        raise
