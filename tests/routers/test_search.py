from fastapi.testclient import TestClient

from BE.main import app
from BE.routers.search import search

client = TestClient(app)

def test_search():
    test_query = 'test_name'
    # TODO Create utils
    response = client.get('/search', params={'artist_name': test_query})
    assert response.status_code == 200
    assert response.json() == test_query