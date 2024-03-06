import sadco.api

from starlette.testclient import TestClient
import pytest


@pytest.fixture
def api():
    api_client = TestClient(app=sadco.api.app)
    api_client.headers = {
        'Accept': 'application/json'
    }
    return api_client
