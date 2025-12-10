def test_extract_skills_simple():
    from extensions.ai import ats
    txt = 'Skilled in Python, SQL and Docker. Also familiar with machine learning.'
    skills = ats.extract_skills_simple(txt)
    assert 'python' in skills
    assert 'sql' in skills


def test_ats_score_basic():
    from extensions.ai import ats
    resume = 'Experienced engineer with Python and SQL. Education: BSc.'
    job = 'Looking for Python developer with SQL and Docker experience.'
    score, feedback = ats.ats_score(resume, job)
    assert isinstance(score, float)
    assert 'skills_found' in feedback
