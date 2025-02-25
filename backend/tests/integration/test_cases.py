import requests

import io

BASE_URL = "http://localhost:8000"

def test_create_new_case():
    files = [
        ('files', ('test.txt', io.BytesIO(b"test content"), 'text/plain')),
    ]
    response = requests.post(
        f"{BASE_URL}/api/v1/cases/create_new_case",
        files=files,
        data={"case_name": "test_case"}
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Create case successfully"}

def test_create_new_case_invalid_file_type():
    files = [
        ('files', ('test.invalid', io.BytesIO(b"content"), 'invalid/type')),
    ]
    response = requests.post(
        f"{BASE_URL}/api/v1/cases/create_new_case",
        files=files,
        data={"case_name": "test_case"}
    )
    assert response.status_code == 500

def test_delete_case():
    response = requests.delete(f"{BASE_URL}/api/v1/cases/test_case")
    assert response.status_code == 200

def test_search():
    test_data = {
        "question": "tell me about the case",
        "response_mod": "tree_summarize"
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/cases/test_case/search",
        json=test_data
    )
    assert response.status_code == 200
    assert "answer" in response.json()
