from fastapi import HTTPException

from re import sub
from requests import Response, Session
from typing import List, Set

import logging

from src import HEADERS
from src.pybrainz import ARTIST_URL, RECORDING_URL
from src.pybrainz.models import Artist, Recording

# Init MusicBrainz Session
"""
BUG Having this in main will cause circular imports.
Need to think whether to leave this here, or move to __init__
TODO Test
"""
session = Session()
session.headers.update(HEADERS)

class Query(object):
    session: Session
    url: str = None
    response: Response = None

    def __init__(self):
        self.session = session
    
    def request(self):
        if self.response == None: raise NotImplementedError()
        if not isinstance(self.response, Response): raise TypeError()
        if not self.response.ok: raise HTTPException(self.response.status_code, self.response.text)

class Get(Query):
    def __init__(self):
        super(Get, self).__init__()

    def get(self):
        self.request()
        self._data = self.clean()
        return self._data

    def request(self):
        self.response = self.session.get(self.url, params=self.query_params)
        super(Get, self).request()
    
    def clean(self) -> dict:
        if not self.response: raise SyntaxError('request must be called first')
        return self.response.json()

    @property
    def query_params(self) -> dict:
        raise NotImplementedError()

class GetArtistByName(Get):
    url = ARTIST_URL

    def __init__(self, name: str, limit: int = 3, offset: int = 0):
        super(GetArtistByName, self).__init__()
        self.name = name
        self.limit = limit
        self.offset = offset

    def clean(self) -> List[Artist]:
        result = super(GetArtistByName, self).clean()
        artists = [Artist(artist.get('id'), artist.get('name')) for artist in result.get('artists', [])]
        return artists
    
    @property
    def query_params(self) -> dict:
        return {'query': self.name, 'limit': self.limit, 'offset': self.offset}

class GetRecordingsByArtistId(Get):
    url = RECORDING_URL

    def __init__(self, id: str, limit: int = 100, offset: int = 0):
        super(GetRecordingsByArtistId, self).__init__()
        self.uid = id
        self.limit = limit
        self.offset = offset

        self.codes: Set[str] = set()
        self.count = None
    
    def get(self) -> List[Recording]:
        recordings: List[Recording] = []
        while self.count == None or self.offset < self.count:
            self.request()
            recordings.extend(self.clean())
            self.offset += self.limit
        self._data = recordings
        return self._data
    
    def clean(self) -> List[Recording]:
        result = super(GetRecordingsByArtistId, self).clean()
        if self.count == None: self.count: int = result.get('recording-count')

        recordings = []
        for recording in result.get('recordings', []):
            # TODO Should error if title is none / not add
            title = self._clean_title(recording.get('title'))
            code = self._clean_code(title.lower())
            if code and code not in self.codes:
                recordings.append(Recording(code, recording.get('id'), title))
                self.codes.add(code)
        return recordings

    def _clean_title(self, title: str) -> str:
        # Remove everything in any brackets
        title = sub(r'\(([^\)]*)\)|\[([^\]]*)\]|\{([^\]]*)\}', '', title)
        return title
    
    def _clean_code(self, code: str) -> str:
        # Lower and remove whitespace
        # TODO Think about -,./
        # TODO Allow unicode
        code = sub(r'[^\w]', '', code.lower())
        return code

    
    @property
    def query_params(self) -> dict:
        return {'artist': self.uid, 'limit': self.limit, 'offset': self.offset}
