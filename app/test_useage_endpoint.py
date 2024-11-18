import pytest
from .main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_get_useage_report():
    response = client.get("/tech-task/usage/")
    assert response.status_code == 200
    assert response.json() == {}