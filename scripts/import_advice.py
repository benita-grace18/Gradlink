"""One-time script to import advice into the in-memory RAG index.

This repository uses a single-file `app.py` rather than an application factory.
This script imports the running Flask `app` and, as a fallback, a small
`SAMPLE_ADVICE` set from the AskAlum extension so it can be run without DB
models present. It calls `extensions.ai.rag_faiss.add_document` to seed the
index (development only).

Usage:
    python scripts/import_advice.py
"""
import os
import sys

# Ensure project root is on path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app import app
from extensions.ai.rag_faiss import add_document, _ensure_index

# Try import of a DB-backed Advice model; fall back to sample advice
SAMPLE = None
try:
    # If you have a DB model named Advice, uncomment and adjust the import below
    # from app.models import Advice
    # SAMPLE = [{'id': a.id, 'author': getattr(a, 'author', 'db'), 'content': getattr(a, 'content', str(a))} for a in Advice.query.all()]
    raise ImportError
except Exception:
    try:
        from extensions.ask_alum.views import SAMPLE_ADVICE
        SAMPLE = SAMPLE_ADVICE
    except Exception:
        SAMPLE = [
            {'id': 1, 'author': 'Alumnus A', 'content': 'Focus on internships and practical projects.'},
            {'id': 2, 'author': 'Alumnus B', 'content': 'Learn Python and SQL for data roles.'},
        ]


def import_advice_to_rag():
    with app.app_context():
        _ensure_index()
        count = 0
        for item in SAMPLE:
            doc_id = f"advice_{item.get('id')}"
            text = item.get('content', '')
            meta = {'author': item.get('author')}
            try:
                add_document(doc_id, text, meta)
                print(f"Imported {doc_id}")
                count += 1
            except Exception as e:
                print(f"Failed to import {doc_id}: {e}")

        print(f"\nImported {count} documents into the RAG index (dev only)")


if __name__ == '__main__':
    import_advice_to_rag()
