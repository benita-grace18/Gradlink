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

def simple_ats_score(text, job_keywords=None):
    if job_keywords is None:
        # sample default keywords tailored to your AIML focus
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
        'found_keywords': found,
        'missing_sections': [s for s in ['Education', 'Experience', 'Skills', 'Projects'] if s.lower() not in txt]
    }
    return ar_score, feedback

# Minimal text extractor stub. Replace with pdfminer / python-docx for production.
def extract_text_from_file(path):
    try:
        ext = path.rsplit('.',1)[1].lower()
        if ext == 'txt':
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        # For unsupported formats in this stub, return empty string
        return ""
    except Exception:
        return ""

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
        text = extract_text_from_file(path)
        score, feedback = simple_ats_score(text)
        # Optionally save minimal metadata to DB later
        return render_template('resume/result.html', score=score, feedback=feedback, filename=filename)
    return render_template('resume/upload.html')
