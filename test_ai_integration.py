"""Local integration test for AI extensions without running Flask server."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app

print("=" * 60)
print("AI EXTENSIONS INTEGRATION TEST")
print("=" * 60)

with app.app_context():
    # Test 1: Check feature flags are enabled
    print("\n1. Feature Flags Status:")
    flags = app.config['FEATURE_FLAGS']
    for name, enabled in flags.items():
        status = "✓ ENABLED" if enabled else "✗ DISABLED"
        print(f"   {name}: {status}")
    
    # Test 2: Test RAG endpoint logic (without server)
    print("\n2. RAG Module Test:")
    from extensions.ask_alum.views import ask_rag
    from extensions.ai.rag_faiss import query_rag
    try:
        answer, sources = query_rag("How do I prepare for interviews?")
        print(f"   ✓ RAG query successful")
        print(f"     - Answer: {answer[:80]}...")
        print(f"     - Sources: {len(sources)} found")
    except Exception as e:
        print(f"   ✗ RAG error: {e}")
    
    # Test 3: Test ATS module
    print("\n3. ATS Module Test:")
    from extensions.ai.ats import extract_skills_simple, ats_score
    try:
        resume = "Software engineer with Python, SQL, and Docker experience. BSc in Computer Science."
        job = "Looking for Python developer with SQL and Docker skills."
        score, feedback = ats_score(resume, job)
        print(f"   ✓ ATS scoring successful")
        print(f"     - Score: {score}%")
        print(f"     - Skills found: {feedback.get('skills_found', [])}")
    except Exception as e:
        print(f"   ✗ ATS error: {e}")
    
    # Test 4: Test MCS module
    print("\n4. MCS Mentor Matching Test:")
    from extensions.matching.db_mcs import get_recommendations_for_student
    try:
        recs = get_recommendations_for_student(999)
        print(f"   ✓ MCS module loaded")
        print(f"     - Recommendations returned: {len(recs)}")
    except Exception as e:
        print(f"   ✗ MCS error: {e}")
    
    # Test 5: Smoke test endpoints
    print("\n5. Endpoint Routes Test:")
    with app.test_client() as client:
        # ASK_ALUM endpoint
        resp = client.get('/ask/')
        print(f"   GET /ask/ -> {resp.status_code}")
        
        # RESUME endpoint
        resp = client.get('/resume/')
        print(f"   GET /resume/ -> {resp.status_code}")
        
        # MCS endpoint
        resp = client.get('/mcs/recommend')
        print(f"   GET /mcs/recommend -> {resp.status_code}")
        
        # RAG endpoint (POST JSON)
        resp = client.post('/ask/rag', json={"query": "test"})
        print(f"   POST /ask/rag -> {resp.status_code}")
        if resp.status_code == 200:
            data = resp.get_json()
            print(f"     - Response keys: {list(data.keys())}")

print("\n" + "=" * 60)
print("INTEGRATION TEST COMPLETE")
print("=" * 60)
