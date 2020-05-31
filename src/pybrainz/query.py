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
    """
    Base Query object containing MusicBrainz session, None url and basic request checking
    """

    session: Session
    url: str = None
    response: Response = None

    def __init__(self):
        """
        Sets default session
        """
        self.session = session
    
    def request(self):
        """
        Base request. Performs checks.

        :raises NotImplementedError: If response is None. Need to implement child request method and super this.
        :raises TypeError: If response is not a Response.
        :raises HTTPException: If response is not ok.
        """
        if self.response == None: raise NotImplementedError()
        if not isinstance(self.response, Response): raise TypeError()
        if not self.response.ok: raise HTTPException(self.response.status_code, self.response.text)

class Get(Query):
    """
    Base Get Query
    """
    def __init__(self):
        super(Get, self).__init__()

    def get(self):
        """
        Executes request then clean. Sets own _data and returns.

        :return: cleaned response
        :rtype: JSON
        """
        self.request()
        self._data = self.clean()
        return self._data

    def request(self):
        """
        Performs get request using `session`
        """
        self.response = self.session.get(self.url, params=self.query_params)
        super(Get, self).request()
    
    def clean(self) -> dict:
        """
        Performs checks and if pass cleans response to get json.

        :raises SyntaxError: if `response` is None then request has yet to be called.
        :return: json from response
        :rtype: dict
        """
        if not self.response: raise SyntaxError('request must be called first')
        return self.response.json()

    @property
    def query_params(self) -> dict:
        """
        Returns query parameters for get request

        :raises NotImplementedError: child class has yet to implement query_params
        :return: get query parameters
        :rtype: dict
        """
        raise NotImplementedError()

# TODO Refactor rename to plural
class GetArtistByName(Get):
    """
    Generate list of artists searched by name
    """
    url = ARTIST_URL

    def __init__(self, name: str, limit: int = 3, offset: int = 0):
        """
        Initialises query params

        :param name: name to be searched
        :type name: str
        :param limit: number of results to be returned, defaults to 3
        :type limit: int, optional
        :param offset: offset from first result, defaults to 0
        :type offset: int, optional
        """
        super(GetArtistByName, self).__init__()
        self.name = name
        self.limit = limit
        self.offset = offset

    def clean(self) -> List[Artist]:
        """
        cleans response into `list` of `Artists`

        :return: list of artists related to name found
        :rtype: List[Artist]
        """
        result = super(GetArtistByName, self).clean()
        artists = [Artist(artist.get('id'), artist.get('name')) for artist in result.get('artists', [])]
        return artists
    
    @property
    def query_params(self) -> dict:
        """
        parameters to be included in get request

        :return: `query`, `limit`, `offset`
        :rtype: dict
        """
        return {'query': self.name, 'limit': self.limit, 'offset': self.offset}

class GetRecordingsByArtistId(Get):
    """
    Generate list of recordings of artist id
    """
    url = RECORDING_URL

    def __init__(self, id: str, limit: int = 100, offset: int = 0):
        """
        Initialises query params, recordings codes and count.

        :param id: artist id
        :type id: str
        :param limit: number of results to be returned, defaults to 100
        :type limit: int, optional
        :param offset: offset from first result, defaults to 0
        :type offset: int, optional
        """
        super(GetRecordingsByArtistId, self).__init__()
        self.uid = id
        self.limit = limit
        self.offset = offset

        self.codes: Set[str] = set()
        self.count = None
    
    def get(self) -> List[Recording]:
        """
        Retrieves all recordings. Makes request for `limit` number of recordings until all `count` is retrieved.

        :return: list of recordings of artist id
        :rtype: List[Recording]
        """
        # TODO May have to implement timeout/retry strategy
        recordings: List[Recording] = []
        while self.count == None or self.offset < self.count:
            self.request()
            recordings.extend(self.clean())
            self.offset += self.limit
        self._data = recordings
        return self._data
    
    def clean(self) -> List[Recording]:
        """
        Cleans title, generates code, and adds recordings with unique codes to `recordings`

        :return: list of Recordings with unique codes
        :rtype: List[Recording]
        """
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
        """
        Removes anything in any brackets. Assuming no nested brackets

        :param title: original title
        :type title: str
        :return: cleaned title
        :rtype: str
        """
        title = sub(r'\(([^\)]*)\)|\[([^\]]*)\]|\{([^\]]*)\}', '', title)
        return title
    
    def _clean_code(self, code: str) -> str:
        """
        Lowers and removes whitespace

        :param code: original code (currently title)
        :type code: str
        :return: cleaned code
        :rtype: str
        """
        # Lower and remove whitespace
        # TODO Think about -,./
        # TODO Allow unicode
        code = sub(r'[^\w]', '', code.lower())
        return code

    
    @property
    def query_params(self) -> dict:
        """
        parameters to be included in get request

        :return: `artist`, `limit`, `offset`
        :rtype: dict
        """
        return {'artist': self.uid, 'limit': self.limit, 'offset': self.offset}
