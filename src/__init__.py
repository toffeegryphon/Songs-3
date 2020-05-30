APP_NAME = 'SongsBy'
APP_VERSION = '3.0.1'
APP_SOURCE = 'https://github.com/toffeegryphon/Songs-3'

HEADERS = {
    'user-agent': f'{APP_NAME}/{APP_VERSION} ({APP_SOURCE})',
    'accept': 'application/json',
    'content-type': 'application/json; charset=utf-8'
}

FIRESTORE_CERTIFICATE = 'src/songs-522b9-a83d85fea785.json'