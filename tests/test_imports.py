def test_ai_modules_importable():
    """Ensure AI modules import without raising exceptions."""
    from extensions.ai import ats as ats_mod
    from extensions.ai import rag_faiss as rag_mod
    from extensions.matching import db_mcs as mcs_mod

    assert hasattr(ats_mod, 'extract_skills_simple')
    assert hasattr(rag_mod, 'clear_index') or hasattr(rag_mod, 'add_document')
    assert hasattr(mcs_mod, 'get_recommendations_for_student')
