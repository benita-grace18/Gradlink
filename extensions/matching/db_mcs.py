"""
Database-backed Mentor Compatibility Scoring (MCS)
Matches students to mentors using TF-IDF skill similarity and logistical factors
"""
from flask import current_app
from models import User
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_recommendations_for_student(student_id, num_recommendations=3):
    """
    Get mentor recommendations for a student using database data.
    
    Args:
        student_id: ID of the student
        num_recommendations: How many mentors to return
    
    Returns:
        List of dicts with mentor info and compatibility score
    """
    try:
        # Get student
        student = User.query.get(student_id)
        if not student:
            return []
        
        # Get student's skills (assume stored in a skills field or profile text)
        student_skills = getattr(student, 'skills', '') or student.bio or ''
        if not student_skills:
            return []
        
        # Get all mentors (assuming a role field or mentor flag)
        mentors = User.query.filter(
            (User.id != student_id) &
            (User.role == 'mentor' if hasattr(User, 'role') else True)
        ).limit(20).all()
        
        if not mentors:
            return []
        
        # Extract mentor skills
        mentor_skills = [
            (m.id, getattr(m, 'username', '') or str(m.id), getattr(m, 'skills', '') or getattr(m, 'bio', '') or '')
            for m in mentors
        ]
        
        # TF-IDF matching
        all_texts = [student_skills] + [skills for _, _, skills in mentor_skills]
        try:
            vect = TfidfVectorizer(stop_words='english', max_features=50)
            mat = vect.fit_transform(all_texts).toarray()
        except ValueError:
            # Corpus too small, return empty
            return []
        
        # Calculate cosine similarity
        student_vec = mat[0]
        scores = []
        for i, (mentor_id, mentor_name, _) in enumerate(mentor_skills, 1):
            mentor_vec = mat[i]
            sim = float(
                np.dot(student_vec, mentor_vec) / 
                ((np.linalg.norm(student_vec) * np.linalg.norm(mentor_vec)) + 1e-9)
            )
            
            # Logistical feasibility (simplified: prefer available mentors)
            logistical = 0.5
            
            # Combined score
            combined = 0.7 * sim + 0.3 * logistical
            scores.append((mentor_id, mentor_name, combined, sim))
        
        # Sort by score and return top N
        scores.sort(key=lambda x: x[2], reverse=True)
        recommendations = [
            {
                "mentor_id": m_id,
                "mentor_name": m_name,
                "compatibility_score": round(100 * score, 1),
                "skill_match": round(100 * skill_sim, 1)
            }
            for m_id, m_name, score, skill_sim in scores[:num_recommendations]
        ]
        
        current_app.logger.info(f"Generated {len(recommendations)} recommendations for student {student_id}")
        return recommendations
        
    except Exception as e:
        current_app.logger.exception(f"Error generating mentor recommendations: {e}")
        return []
