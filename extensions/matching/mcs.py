import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def compute_content_similarity(student_vec, mentor_vec):
    try:
        student_vec = np.array(student_vec, dtype=float)
        mentor_vec = np.array(mentor_vec, dtype=float)
        if np.linalg.norm(student_vec) == 0 or np.linalg.norm(mentor_vec) == 0:
            return 0.0
        return float(cosine_similarity([student_vec], [mentor_vec])[0][0])
    except Exception:
        return 0.0

def compute_logistical_feasibility(student_tz, mentor_tz, student_avail, mentor_avail):
    try:
        tz_score = 1.0 if student_tz == mentor_tz else max(0, 1 - abs(student_tz - mentor_tz) / 24)
        overlap = len(set(student_avail).intersection(set(mentor_avail)))
        total = max(1, len(set(student_avail).union(set(mentor_avail))))
        avail_score = overlap / total
        return 0.6 * tz_score + 0.4 * avail_score
    except Exception:
        return 0.5

def compute_collaborative_filtering(history_scores):
    if not history_scores:
        return 0.5
    return sum(history_scores) / len(history_scores)

def mentor_compatibility_score(student_vec, mentor_vec, student_tz, mentor_tz, student_avail, mentor_avail, cf_history, alpha=0.4, beta=0.4, gamma=0.2):
    cs = compute_content_similarity(student_vec, mentor_vec)
    lf = compute_logistical_feasibility(student_tz, mentor_tz, student_avail, mentor_avail)
    cf = compute_collaborative_filtering(cf_history)
    return round(alpha * cs + beta * lf + gamma * cf, 4)
