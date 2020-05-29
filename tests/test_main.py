from fastapi.testclient import TestClient

from BE.main import app

client = TestClient(app)