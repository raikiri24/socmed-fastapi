import pytest
from starlette.testclient import TestClient

from main import create_app


@pytest.fixture
def client():
    yield TestClient(create_app())
