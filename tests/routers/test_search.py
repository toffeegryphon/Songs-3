from fastapi import HTTPException
from fastapi.testclient import TestClient

from typing import List
from unittest.mock import patch, MagicMock

from src.main import app
from src.routers.search import search
from src.pybrainz.query import Artist

client = TestClient(app)

mocked_artists: List[Artist] = [
    Artist('uid-0', 'name-0'),
    Artist('uid-1', 'name-1')
]

@patch('src.routers.search.get_artists_by_name')
def test_search_valid(mocked_get: MagicMock):
    mocked_get.return_value = mocked_artists
    response = client.get('/search', params={'artist_name': 'test_name'})
    assert response.status_code == 200
    assert response.json() == [artist.__dict__ for artist in mocked_artists]

@patch('src.routers.search.get_artists_by_name')
def test_search_invalid(mocked_get: MagicMock):
    test_code = 500
    test_message = 'test_error'
    def side_effect(*args, **kwargs):
        raise HTTPException(test_code, test_message)
    mocked_get.side_effect = side_effect
    response = client.get('/search', params={'artist_name': True})
    assert response.status_code == test_code
    assert response.json() == {'detail': test_message}

def test_search_blank():
    response = client.get('/search')
    assert response.status_code == 422