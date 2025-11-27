def test_rag_imports():
    # ensure rag modules import
    import rag.chunk  # noqa: F401
    import rag.embedding  # noqa: F401
    import rag.retriever  # noqa: F401
    import rag.summarize  # noqa: F401
    assert True
