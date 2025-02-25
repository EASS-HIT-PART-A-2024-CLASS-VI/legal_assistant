# conftest.py
import pytest

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("FALKORDB_PASSWORD", "test_password")
    monkeypatch.setenv("FALKORDB_RAG_URI", "test_uri")
    yield