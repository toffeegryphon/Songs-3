from src.pybrainz.models import Artist

def test_artist_to_dict():
    test_uid = 'some-uid'
    test_name = 'some-name'
    test_artist = Artist(test_uid, test_name)
    assert test_artist.__dict__ == {'uid': test_uid, 'name': test_name}