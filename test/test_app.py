import pytest
import uuid

from tasks_server import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_runs(client):
    action_title = f"test action {uuid.uuid4()}"
    client.post("/inbox/", json={
        "title": action_title
    })

    inbox = client.get("/inbox/").get_json()
    action = None
    for action in inbox["items"]:
        if action["title"] == action_title:
            break

    assert action is not None

    action_id = action["id"]
    client.delete(f"/inbox/{action_id}")

    inbox = client.get("/inbox/").get_json()
    for action in inbox["items"]:
        assert action["title"] != action_title
