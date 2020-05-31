from fastapi import FastAPI

from firebase_admin import initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin.firestore import client

from google.cloud.firestore import Client

import logging

from src.initialisation import db
from src.routers import search

app = FastAPI()

# Set routers
app.include_router(search.router, prefix='/search')