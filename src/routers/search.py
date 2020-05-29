from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get('/')
async def search(artist_name: str = ''):
    return artist_name