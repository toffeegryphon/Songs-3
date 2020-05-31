from fastapi import HTTPException
from fastapi.testclient import TestClient

from typing import List
from unittest.mock import patch, MagicMock

from src.main import app
from src.routers.search import search
from src.pybrainz.models import Artist
from src.pybrainz.query import GetArtistByName, GetRecordingsByArtistId

client = TestClient(app)



class TestSearch:
    mocked_artists: List[Artist] = [
        Artist('uid-0', 'name-0'),
        Artist('uid-1', 'name-1')
    ]

    @patch.object(GetArtistByName, 'get', MagicMock(return_value=mocked_artists))
    def test_search_returns_get(self):
        response = client.get('/search', params={'artist_name': 'test name'})
        assert response.status_code == 200
        assert response.json() == [artist.__dict__ for artist in self.mocked_artists]

    def test_search_blank(self):
        response = client.get('/search')
        assert response.status_code == 422
