# extensions/ask_alum/views.py
from flask import render_template, request, current_app
from . import ask_bp

# Safe demo set; in production query DB table of verified alumni advice
SAMPLE_ADVICE = [
    {'id':1, 'author':'Alumnus A', 'content':'Focus on internships and practical projects.'},
    {'id':2, 'author':'Alumnus B', 'content':'Learn Python and SQL for data roles.'},
    {'id':3, 'author':'Alumnus C', 'content':'Network with alumni during events.'}
]

@ask_bp.route('/', methods=['GET','POST'])
def ask():
    if not current_app.config['FEATURE_FLAGS'].get('ASK_ALUM', False):
        return "Feature disabled", 404
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('query','').strip()
        if query:
            q = query.lower()
            results = [r for r in SAMPLE_ADVICE if q in r['content'].lower() or q in r['author'].lower()]
    return render_template('ask/form.html', results=results, query=query)
