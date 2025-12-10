# extensions/ask_alum/views.py
from flask import render_template, request, current_app, jsonify
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

@ask_bp.route('/rag', methods=['POST'])
def ask_rag():
    """RAG endpoint: query alumni advice with AI generation."""
    if not current_app.config['FEATURE_FLAGS'].get('ASK_ALUM', False):
        return jsonify({"error": "Feature disabled"}), 404
    
    try:
        data = request.get_json()
        query = (data or {}).get('query', '').strip()
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        # Import here to avoid import errors if faiss/openai not installed
        try:
            from extensions.ai.rag_faiss import query_rag
        except ImportError as e:
            current_app.logger.error(f"RAG module not available: {e}")
            return jsonify({"error": "RAG feature not available"}), 503
        
        # Query RAG
        answer, sources = query_rag(query, k=3)
        
        return jsonify({
            "query": query,
            "answer": answer,
            "sources": sources
        })
    
    except Exception as e:
        current_app.logger.exception("RAG query failed")
        return jsonify({"error": "Internal server error"}), 500
