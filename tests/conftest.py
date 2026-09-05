import pytest
from fastapi.testclient import TestClient

import app.storage as storage
from app.main import app


@pytest.fixture(autouse=True)
def use_test_database(tmp_path, monkeypatch):
    test_db = tmp_path / "test_automation.db"

    monkeypatch.setattr(storage, "DB_PATH", test_db)

    storage.initialise_database()


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client