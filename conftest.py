import pytest
import requests

@pytest.fixture(scope="session")
def api_client():
    return requests.Session()