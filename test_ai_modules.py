"""Lightweight local smoke tests for AI modules (no external network calls).

This script ensures modules import and their local, offline helpers run.
It avoids calling OpenAI/FAISS network endpoints and prints helpful diagnostics.
"""
import traceback

print('=== AI Modules Smoke Test ===')

# RAG module
try:
    from extensions.ai import rag_faiss as rag
    print('\n[rag_faiss] module imported')
    print('  faiss available:', bool(getattr(rag, 'faiss', None)))
    print('  openai available:', bool(getattr(rag, 'openai', None)))
    # Try safe local operation: clear/inspect index
    if hasattr(rag, 'clear_index'):
        rag.clear_index()
        print('  cleared index (if present)')
    else:
        print('  no clear_index() available')
    # Try calling add_document but catch errors (we expect it to raise if openai missing)
    try:
        rag.add_document('test_doc', 'This is a test doc', {'source': 'smoke_test'})
        print('  add_document succeeded (unexpected without OpenAI)')
    except Exception as e:
        print('  add_document raised (expected if OpenAI missing):', repr(e))

except Exception:
    print('\n[rag_faiss] import failed:')
    traceback.print_exc()

# ATS module (offline checks)
try:
    from extensions.ai import ats
    print('\n[ats] module imported')
    txt = 'Experienced software engineer with Python, SQL, and Docker experience.'
    skills = ats.extract_skills_simple(txt)
    print('  extract_skills_simple ->', skills)
except Exception:
    print('\n[ats] import or run failed:')
    traceback.print_exc()

# DB-backed MCS module (import-only smoke test)
try:
    from extensions.matching import db_mcs
    print('\n[db_mcs] module imported')
except Exception:
    print('\n[db_mcs] import or run failed:')
    traceback.print_exc()

print('\n=== Smoke test complete ===')
