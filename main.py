from fastapi import FastAPI

from firebase_admin import initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin.firestore import client

from google.cloud.firestore import Client

import logging

from BE import FIRESTORE_CERTIFICATE
from BE.routers import search

app = FastAPI()

# Init db
cred = Certificate(FIRESTORE_CERTIFICATE)
initialize_app(cred)
db: Client = client()

# Set routers
app.include_router(search.router, prefix='/search')