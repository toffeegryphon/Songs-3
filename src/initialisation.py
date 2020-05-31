from firebase_admin import initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin.firestore import client

from google.cloud.firestore import Client, CollectionReference

from src import FIRESTORE_CERTIFICATE

# Init db
cred = Certificate(FIRESTORE_CERTIFICATE)
initialize_app(cred)
db: Client = client()
artist_collection: CollectionReference = db.collection('artists')