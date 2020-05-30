from fastapi import APIRouter, HTTPException

from json import loads
from requests import codes

import logging

from src.pybrainz.query import Artist, get_artists_by_name

router = APIRouter()

@router.get('/')
async def search(artist_name: str):
    """
    Basic search endpoint

    :param artist_name: name of artist to be searched
    :type artist_name: str
    :return: artist_name
    :rtype: JSON
    """
    artists = get_artists_by_name(artist_name)
    return artists