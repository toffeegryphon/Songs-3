from src.pybrainz.models import Artist, Recording

class TestArtist:
    def test_to_dict(self):
        test_uid = 'some-uid'
        test_name = 'some-name'
        test_artist = Artist(test_uid, test_name)
        assert test_artist.__dict__ == {'uid': test_uid, 'name': test_name}

class TestRecording:
    def test_to_dict(self):
        test_code = 'sometitle'
        test_id = 'some-uid'
        test_title = 'Some Title'
        test_recording = Recording(test_code, test_id, test_title)
        assert test_recording.__dict__ == {'code': test_code, 'uid': test_id, 'title': test_title}