from fastapi import APIRouter, HTTPException

from json import loads
from requests import codes

from google.cloud.firestore import DocumentSnapshot

import logging

from src.initialisation import artist_collection
from src.pybrainz.query import GetArtistByName, GetRecordingsByArtistId

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
    request = GetArtistByName(artist_name)
    return request.get()

@router.get('/{artist_id}')
async def read_artist(artist_id: str):
    artist: DocumentSnapshot = artist_collection.document(artist_id).get()
    if not artist.exists:
        request = GetRecordingsByArtistId(artist_id)
        artist = request.get()
    else:
        artist = artist.to_dict()
    return artist