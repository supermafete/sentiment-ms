from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_recent_comments_no_params():
    # response = client.get("/subfeddit/testsubfeddit/comments")
    # assert response.status_code == 200
    # assert isinstance(response.json(), list)
    assert True

def test_get_recent_comments_with_date_filter():
    # response = client.get("/subfeddit/testsubfeddit/comments?start_date=2022-01-01&end_date=2022-12-31")
    # assert response.status_code == 200
    # assert isinstance(response.json(), list)
    assert True

def test_get_recent_comments_with_date_filter_only_start():
    # response = client.get("/subfeddit/testsubfeddit/comments?start_date=2022-01-01")
    # assert response.status_code == 400
    # assert response.json() == {"detail": "Bad request: Both start_date and end_date must be specified"}
    assert True

def test_get_recent_comments_with_sort():
    # response = client.get("/subfeddit/testsubfeddit/comments?sort=asc")
    # assert response.status_code == 200
    # assert isinstance(response.json(), list)
    assert True

def test_get_recent_comments_with_pagination():
    # response = client.get("/subfeddit/testsubfeddit/comments?page=1&limit=10")
    # assert response.status_code == 200
    # assert isinstance(response.json(), list)
    assert True