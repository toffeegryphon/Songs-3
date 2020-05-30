from fastapi import HTTPException
from requests import Response
from pytest import raises

from unittest.mock import patch, MagicMock

from src.pybrainz.models import Artist
from src.pybrainz.query import session, get_artists_by_name

mocked_session = MagicMock()

mocked_get_result = {
    'artists': [
        {'id': 'id-0', 'name': 'name-0', 'description': 'description-0'},
        {'id': 'id-1', 'name': 'name-1', 'description': 'description-1'}
    ]
}

@patch('src.pybrainz.query.session', mocked_session)
def test_get_artists_by_name_raises_HTTPException_if_query_invalid():
    mocked_response = Response()
    mocked_response.status_code = 500
    mocked_session.get.return_value = mocked_response
    with raises(HTTPException):
        get_artists_by_name('some name', 'invalid')

@patch('src.pybrainz.query.session', mocked_session)
def test_get_artists_by_name_returns_artists_list_if_query_valid():
    def mocked_json():
        return mocked_get_result
    mocked_response = Response()
    mocked_response.status_code = 200
    mocked_response.json = mocked_json
    mocked_session.get.return_value = mocked_response
    artists = get_artists_by_name('some name')
    expected = [Artist(artist['id'], artist['name']) for artist in mocked_get_result['artists']]
    assert artists == expected