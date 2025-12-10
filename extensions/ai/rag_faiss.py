"""
RAG (Retrieval-Augmented Generation) module using FAISS and OpenAI
Keeps index in-memory for development; use pgvector in production
"""
import os
import numpy as np
from flask import current_app

try:
    import faiss
except ImportError:
    faiss = None

try:
    import openai
except ImportError:
    openai = None

EMB_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
EMB_DIM = 1536  # dimension for text-embedding-3-small

# In-memory store (dev-only). In prod use pgvector table.
_index = None
_documents = []  # list of dicts {'id':..., 'text':..., 'meta':...}

def _ensure_index():
    """Initialize FAISS index if not already done."""
    global _index
    if _index is None:
        if faiss is None:
            raise RuntimeError("faiss not installed; install faiss-cpu for local RAG")
        _index = faiss.IndexFlatL2(EMB_DIM)

def embed_text(text: str):
    """Get embedding vector for text using OpenAI."""
    if openai is None:
        raise RuntimeError("openai package not installed")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set")
    
    response = openai.Embedding.create(model=EMB_MODEL, input=text)
    return np.array(response["data"][0]["embedding"], dtype=np.float32)

def add_document(doc_id, text, meta=None):
    """Add a document to in-memory index. Call in admin/import step."""
    try:
        vec = embed_text(text)
        _documents.append({'id': doc_id, 'text': text, 'meta': meta or {}})
        _ensure_index()
        _index.add(np.array([vec]))
        current_app.logger.info(f"Added document {doc_id} to RAG index")
    except Exception as e:
        current_app.logger.error(f"Error adding document {doc_id}: {e}")
        raise

def query_rag(query: str, k: int = 3):
    """
    Query RAG index and generate answer using OpenAI.
    Returns (answer, source_ids) or uses fallback if deps missing.
    """
    # Graceful fallback: if no OpenAI key, use static demo answer
    if not os.getenv("OPENAI_API_KEY"):
        current_app.logger.warning("OPENAI_API_KEY not set; using static fallback answer")
        # Return static helpful response from sample advice
        return (
            "Based on campus resources: Focus on internships and practical projects to build your portfolio. "
            "Learn in-demand skills like Python and SQL. Network with alumni during campus events. "
            "We recommend reaching out to the alumni network directly for personalized advice.",
            []
        )
    if faiss is None and _documents:
        current_app.logger.warning("faiss not available; using simple text search fallback")
    if len(_documents) == 0:
        current_app.logger.warning("RAG index is empty; returning static response")
        return (
            "Our alumni database is being populated. Please check back soon for personalized advice from alumni mentors.",
            []
        )

    try:
        # Try full OpenAI + FAISS flow if available
        if openai is None:
            raise ImportError("OpenAI not installed")
        
        # Get query embedding
        qv = embed_text(query)
        
        # Search FAISS index
        D, I = _index.search(np.array([qv]), k)
        retrieved = []
        for idx in I[0]:
            if 0 <= idx < len(_documents):
                retrieved.append(_documents[idx])
        
        # Build context from retrieved documents
        context = "\n\n---\n\n".join([r['text'] for r in retrieved]) if retrieved else ""
        
        prompt = (
            "You are AskAlum, a campus-specific career mentor assistant for Gradlink. "
            "Use only the following verified alumni advice to answer. "
            "If none is relevant, say you cannot answer and suggest escalating to a mentor.\n\n"
            f"Alumni Advice:\n{context}\n\nStudent Question: {query}\n\nAnswer:"
        )
        
        # Generate answer
        chat_response = openai.ChatCompletion.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful career mentor assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.1
        )
        
        answer = chat_response['choices'][0]['message']['content'].strip()
        source_ids = [r['id'] for r in retrieved]
        
        current_app.logger.info(f"RAG query successful: {len(source_ids)} sources used")
        return answer, source_ids
        
    except (ImportError, AttributeError, KeyError) as e:
        # Fallback: concatenate matching documents without AI
        current_app.logger.warning(f"OpenAI generation failed: {e}; falling back to extractive answer")
        q_lower = query.lower()
        matching = [d for d in _documents if any(word in d['text'].lower() for word in q_lower.split())][:k]
        fallback_answer = " ".join([d['text'] for d in matching]) if matching else "No matching advice found."
        return fallback_answer, [d['id'] for d in matching]
        
    except Exception as e:
        current_app.logger.exception("RAG query failed")
        raise

def clear_index():
    """Clear the in-memory index (for testing)."""
    global _index, _documents
    _index = None
    _documents = []
