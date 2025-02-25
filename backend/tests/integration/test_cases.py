import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.utils.db_client import FalkorDBClient
import io

client = TestClient(app)


@pytest.fixture
def mock_db_client(mocker):
    mock_client = mocker.Mock(spec=FalkorDBClient)
    return mock_client


@pytest.fixture
def sample_file():
    return io.BytesIO(b"test content")


def test_create_new_case():
    """Test creating a new case with file upload"""
    files = [
        ('files', ('test.txt', io.BytesIO(b"test content"), 'text/plain')),
    ]
    response = client.post(
        "/api/v1/cases/create_new_case",
        files=files,
        data={"case_name": "test_case"}
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Create case successfully"}

#
# def test_list_cases(mock_db_client):
#     """Test listing all cases"""
#     mock_db_client.client.list_graphs.return_value = ["case1", "case2"]
#
#     response = client.get("/api/v1/cases/list_cases")
#     assert response.status_code == 200
#     assert response.json() == {"cases": ["case1", "case2"]}
#
#
# def test_search():
#     """Test search endpoint"""
#     test_data = {
#         "question": "test question",
#         "response_mod": "SIMPLE"
#     }
#     response = client.post(
#         "/api/v1/cases/test_case/search",
#         json=test_data
#     )
#     assert response.status_code == 200
#     assert "answer" in response.json()
#
#
# def test_delete_case(mock_db_client):
#     """Test deleting a case"""
#     response = client.delete("/api/v1/cases/test_case")
#     assert response.status_code == 200
#
#
# def test_get_case(mock_db_client):
#     """Test getting case graph data"""
#     mock_graph_data = {
#         "relationships": [],
#         "entities": []
#     }
#     mock_db_client.query.return_value = []
#
#     response = client.get("/api/v1/cases/test_case")
#     assert response.status_code == 200
#     assert "relationships" in response.json()
#     assert "entities" in response.json()
#
#
# @pytest.mark.parametrize("file_type,content", [
#     ("application/pdf", b"%PDF-test"),
#     ("text/plain", b"plain text"),
#     ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", b"docx content")
# ])
# def test_create_new_case_different_file_types(file_type, content):
#     """Test creating cases with different file types"""
#     files = [
#         ('files', ('test_file', io.BytesIO(content), file_type)),
#     ]
#     response = client.post(
#         "/api/v1/cases/create_new_case",
#         files=files,
#         data={"case_name": "test_case"}
#     )
#     assert response.status_code == 201
#
#
# def test_create_new_case_invalid_file_type():
#     """Test creating case with invalid file type"""
#     files = [
#         ('files', ('test.invalid', io.BytesIO(b"content"), 'invalid/type')),
#     ]
#     response = client.post(
#         "/api/v1/cases/create_new_case",
#         files=files,
#         data={"case_name": "test_case"}
#     )
#     assert response.status_code == 415
#
#
# def test_search_with_invalid_response_mod():
#     """Test search with invalid response modifier"""
#     test_data = {
#         "question": "test question",
#         "response_mod": "INVALID"
#     }
#     response = client.post(
#         "/api/v1/cases/test_case/search",
#         json=test_data
#     )
#     assert response.status_code == 422