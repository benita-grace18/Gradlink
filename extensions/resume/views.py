import os
from flask import (
    render_template, request, current_app,
    redirect, flash, url_for
)
from werkzeug.utils import secure_filename
from . import resume_bp

UPLOAD_FOLDER = os.path.join('uploads', 'resumes')
ALLOWED = {'pdf', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

@resume_bp.route('/', methods=['GET', 'POST'])
def upload_resume():
    if not current_app.config['FEATURE_FLAGS'].get('RESUME_UPLOAD', False):
        return "Feature disabled", 404
    
    if request.method == 'POST':
        f = request.files.get('resume')
        if not f or not allowed_file(f.filename):
            flash("Invalid file or missing file.")
            return redirect(request.url)
        
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(f.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(path)
        
        try:
            # Try to use real ATS module
            try:
                from extensions.ai.ats import extract_text_from_file, ats_score
                text = extract_text_from_file(path)
                
                # Get job description from form or use default
                job_desc = request.form.get('job_description', 
                    'Machine learning engineer with Python, SQL, and NLP experience.')
                
                score, feedback = ats_score(text, job_desc)
            except (ImportError, RuntimeError) as e:
                # Fall back to simple scoring if AI module not available
                current_app.logger.warning(f"Real ATS not available, using fallback: {e}")
                text = extract_text_from_file_simple(path)
                score, feedback = simple_ats_score(text)
            
            return render_template('resume/result.html', score=score, feedback=feedback, filename=filename)
        
        except Exception as e:
            current_app.logger.exception("Resume processing failed")
            flash(f"Error processing resume: {str(e)}")
            return redirect(request.url)
    
    return render_template('resume/upload.html')

# Fallback simple scorer and text extractor
def simple_ats_score(text, job_keywords=None):
    if job_keywords is None:
        job_keywords = ['python', 'machine learning', 'nlp', 'data', 'sql']
    txt = (text or "").lower()
    found = [kw for kw in job_keywords if kw.lower() in txt]
    kf = len(found) / len(job_keywords) if job_keywords else 0.0
    fs = 0.0
    for sect in ['education', 'experience', 'skills', 'projects']:
        if sect in txt:
            fs += 0.25
    ar_score = round(100 * (0.6 * kf + 0.4 * fs), 2)
    feedback = {
        'score': ar_score,
        'found_keywords': found,
        'missing_sections': [s for s in ['Education', 'Experience', 'Skills', 'Projects'] if s.lower() not in txt],
        'advice': 'Add more relevant keywords and detail your experiences.'
    }
    return ar_score, feedback

def extract_text_from_file_simple(path):
    try:
        ext = path.rsplit('.',1)[1].lower()
        if ext == 'txt':
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        return ""
    except Exception:
        return ""
