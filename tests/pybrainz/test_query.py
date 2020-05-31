from fastapi import HTTPException
from requests import Response
from pytest import raises

from unittest.mock import patch, MagicMock, call

from src.pybrainz import ARTIST_URL, RECORDING_URL
from src.pybrainz.models import Artist, Recording
from src.pybrainz.query import session, Query, Get, GetArtistByName, GetRecordingsByArtistId

# QueryTestCase
class TestQuery:
    def setup_method(self):
        self.test_query = Query()

    def test_query_sets_session_as_default_session(self):
        assert self.test_query.session is session

    def test_query_request_raises_NotImplementedError_if_response_is_none(self):
        with raises(NotImplementedError):
            self.test_query.request()

    def test_query_request_raises_TypeError_if_response_is_invalid_type(self):
        self.test_query.response = 'response'
        with raises(TypeError):
            self.test_query.request()

    def test_query_request_raises_HTTPException_if_response_status_code_is_not_ok(self):
        self.test_query.response = Response()
        self.test_query.response.status_code = 500
        with raises(HTTPException):
            self.test_query.request()

class TestGet:
    def setup_method(self):
        self.test_get = Get()

    @patch.object(Query, '__init__')
    def test_get_init_calls_super(self, mocked_super: MagicMock):
        Get()
        mocked_super.assert_called_once()

    def test_query_params_raises_NotImplementedError(self):
        with raises(NotImplementedError):
            self.test_get.query_params

    @patch('src.pybrainz.query.session')
    @patch.object(Get, 'query_params')
    @patch.object(Query, 'request')
    def test_request_calls_get_with_url_and_query_params_sets_response_and_calls_super(
        self, mocked_super, mocked_params, mocked_session
    ):
        test_response = Response()
        mocked_session.get.return_value = test_response

        test_get = Get()

        test_query_params = {'test': 'params'}
        mocked_params.return_value = test_query_params

        test_url = 'test.url'
        test_get.url = test_url

        test_get.request()
        mocked_session.get.assert_called_once_with(test_url, params=test_get.query_params)
        assert test_get.response == test_response
        mocked_super.assert_called_once()

    def test_clean_raises_SyntaxError_if_response_is_not_generated_yet(self):
        with raises(SyntaxError):
            self.test_get.clean()

    def test_clean_returns_response_json_otherwise(self):
        test_response = MagicMock()
        self.test_get.response = test_response
        self.test_get.clean()
        test_response.json.assert_called_once()
    
    @patch.object(Get, 'request')
    @patch.object(Get, 'clean')
    def test_get_calls_request_then_clean__sets_data_and_returns_cleaned_value(self, mocked_clean, mocked_request):
        mocked_clean.return_value = ['test', 'cleaned']

        manager = MagicMock()
        manager.attach_mock(mocked_request, 'mocked_request')
        manager.attach_mock(mocked_clean, 'mocked_clean')
        
        test_get = Get()
        result = test_get.get()
        expected_calls = [
            call.mocked_request(),
            call.mocked_clean()
        ]
        assert manager.mock_calls == expected_calls
        assert result == mocked_clean.return_value
        assert result == test_get._data

class TestGetArtistByName:
    test_data = {
        'offset': 0,
        'count': 3,
        'artists': [
            {'id': 'id-0', 'name': 'name 0', 'desc': 'desc 0'},
            {'id': 'id-1', 'name': 'name 1', 'desc': 'desc 1'}
        ]
    }

    def setup_method(self):
        self.test_method = GetArtistByName('some name')

    def test_url_is_ARTIST_URL(self):
        assert GetArtistByName.url == ARTIST_URL

    def test_init(self):
        test_name = 'test name'
        test_limit = 5
        test_offset = 2
        test_method = GetArtistByName(test_name, test_limit, test_offset)
        assert test_method.name == test_name
        assert test_method.limit == test_limit
        assert test_method.offset == test_offset
    
    def test_query_params_returns_query_dict(self):
        expected = {
            'query': self.test_method.name,
            'limit': self.test_method.limit,
            'offset': self.test_method.offset
        }
        assert self.test_method.query_params == expected
    
    @patch.object(Get, 'clean', MagicMock(return_value=test_data))
    def test_clean_calls_super_and_returns_list_of_artists(self):
        test_method = GetArtistByName('test name')
        result = test_method.clean()
        expected = [Artist(artist.get('id'), artist.get('name')) for artist in self.test_data.get('artists')]
        assert result == expected

class TestGetRecordingsByArtistId:
    test_count = 10
    test_data = {
        'offset': 0,
        'recording-count': test_count,
        'recordings': [
            {'id': 'id-0', 'title': 'Title 0 (test)', 'desc': 'desc 0'},
            {'id': 'id-1', 'title': 'Title 1 [test]', 'desc': 'desc 1'}
        ]
    }

    def setup_method(self):
        self.test_method = GetRecordingsByArtistId('some-id')

    def test_url_is_RECORDING_URL(self):
        assert GetRecordingsByArtistId.url == RECORDING_URL

    def test_init(self):
        test_id = 'test-id'
        test_limit = 5
        test_offset = 2
        test_method = GetRecordingsByArtistId(test_id, test_limit, test_offset)
        assert test_method.uid == test_id
        assert test_method.limit == test_limit
        assert test_method.offset == test_offset
        assert test_method.count == None
        assert test_method.codes == set()
    
    def test_query_params_returns_query_dict(self):
        expected = {
            'artist': self.test_method.uid,
            'limit': self.test_method.limit,
            'offset': self.test_method.offset
        }
        assert self.test_method.query_params == expected
    
    @patch.object(Get, 'clean', MagicMock(return_value=test_data))
    def test_clean_calls_super_sets_count_and_returns_list_of_recordings(self):
        test_method = GetRecordingsByArtistId('test name')
        result = test_method.clean()
        assert test_method.count == self.test_count
        assert test_method.codes == {'title0', 'title1'}
        expected = [Recording('title0', 'id-0', 'Title 0'), Recording('title1', 'id-1', 'Title 1')]
        assert result == expected
    
    @patch.object(Query, 'request', MagicMock())
    @patch.object(Get, 'clean', MagicMock(return_value=test_data))
    @patch('src.pybrainz.query.session')
    def test_get_requests_and_cleans_until_all_retrieved(self, mocked_session):

        test_limit = 2
        test_method = GetRecordingsByArtistId('test name', test_limit)
        result = test_method.get()
        assert test_method._data == result
        expected = [Recording('title0', 'id-0', 'Title 0'), Recording('title1', 'id-1', 'Title 1')]
        assert result == expected
        assert mocked_session.get.call_count == int((self.test_count + 1) / test_limit)
        assert test_method.offset >= self.test_count
        # TODO Test called in order
