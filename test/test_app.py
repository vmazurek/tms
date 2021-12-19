import pytest

from tasks_server import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_runs(client):
    response = client.get("/").get_json()
    assert response["message"] == "hello!"
