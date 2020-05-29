from fastapi import APIRouter, HTTPException

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
    return artist_name