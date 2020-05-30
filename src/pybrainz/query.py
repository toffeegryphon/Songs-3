from fastapi import HTTPException

from requests import Response, Session
from typing import List

import logging

from src import HEADERS
from src.pybrainz import ARTIST_URL
from src.pybrainz.models import Artist

# Init MusicBrainz Session
"""
BUG Having this in main will cause circular imports.
Need to think whether to leave this here, or move to __init__
TODO Test
"""
session = Session()
session.headers.update(HEADERS)

def get_artists_by_name(name: str, limit: int = 3, offset: int = 0) -> List[Artist]:
    """
    GETs `limit` number of artists from `offset` based on `name`

    :param name: Name of artist to query
    :type name: str
    :param limit: Number of results to return, defaults to 3
    :type limit: int, optional
    :param offset: Offset from first result, defaults to 0
    :type offset: int, optional
    :return: `limit` number of artists from `offset` based on `name`
    :rtype: list
    :raises HTTPException: if invalid request
    """
    query_params = {
        'query': name,
        'limit': limit,
        'offset': offset
    }
    response = session.get(ARTIST_URL, params=query_params)
    if not response.ok:
        raise HTTPException(response.status_code, response.text)
    artists = []
    for artist in response.json().get('artists', []):
        artists.append(Artist(artist.get('id'), artist.get('name')))
    return artists