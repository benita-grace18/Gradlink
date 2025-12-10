# extensions/matching/views.py
from flask import render_template, current_app
from . import mcs_bp
from .mcs import mentor_compatibility_score

@mcs_bp.route('/recommend', methods=['GET'])
def recommend():
    if not current_app.config['FEATURE_FLAGS'].get('MCS_RECOMMENDER', False):
        return "Feature disabled", 404
    # Demo data: replace with DB reads when ready
    student = {
        'id': 1,
        'vec': [0.1, 0.2, 0.3],
        'tz': 5.5,
        'avail': list(range(9, 18))
    }
    mentors = [
        {'id': 11, 'name': 'A. Mentor', 'vec': [0.1,0.19,0.31], 'tz': 5.5, 'avail': list(range(10,17)),'history': [0.8,0.9]},
        {'id': 12, 'name': 'B. Mentor', 'vec': [0.0,0.2,0.4], 'tz': 2.0, 'avail': list(range(20,23)),'history': [0.6,0.7]},
    ]
    recommendations = []
    for m in mentors:
        score = mentor_compatibility_score(student['vec'], m['vec'], student['tz'], m['tz'], student['avail'], m['avail'], m.get('history', []))
        recommendations.append({'mentor': m, 'score': score})
    recommendations = sorted(recommendations, key=lambda r: r['score'], reverse=True)
    return render_template('mcs/recommend.html', recommendations=recommendations)
