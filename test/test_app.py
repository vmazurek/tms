import pytest
import uuid

from http import HTTPStatus
from tasks_server import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def find_item_by_title(items, title):
    if items is None or len(items) == 0:
        return None
    for item in items:
        if item["title"] == title:
            return item
    return None


def create_inbox_item(client, capture):
    posting = client.post("/inbox", json=capture)
    assert posting.status_code == HTTPStatus.CREATED
    assert posting.headers["Location"] is not None

    getting = client.get(posting.headers["Location"])
    assert getting.status_code == HTTPStatus.OK

    new_item = getting.get_json()
    assert new_item is not None

    return new_item


def test_creates_inbox_items(client):
    capture = {
        "title": f"new inbox item {uuid.uuid4()}",
        "description": "some comment on the item"
    }
    new_item = create_inbox_item(client, capture)
    assert new_item["title"] == capture["title"]
    assert new_item["description"] == capture["description"]


def test_creates_inbox_items_with_title_only(client):
    capture = {
        "title": f"new inbox item {uuid.uuid4()}"
    }
    new_item = create_inbox_item(client, capture)
    assert new_item["title"] == capture["title"]
    assert new_item["description"] == ""


def test_lists_inbox_items(client):
    capture = {
        "title": f"new inbox item {uuid.uuid4()}",
        "description": "some comment on the item"
    }
    create_inbox_item(client, capture)

    inbox = client.get("/inbox")
    assert inbox.status_code == HTTPStatus.OK

    inbox_content = inbox.get_json()
    new_item = find_item_by_title(inbox_content["items"], capture["title"])
    assert new_item is not None
    assert new_item["description"] == capture["description"]


def test_completes_items_from_inbox(client):
    action_title = f"actionable item {uuid.uuid4()}"
    client.post("/inbox", json={"title": action_title})

    inbox = client.get("/inbox")
    assert inbox.status_code == HTTPStatus.OK
    inbox_content = inbox.get_json()
    item = find_item_by_title(inbox_content["items"], action_title)
    assert item is not None

    assert item["actions"]["complete"] is not None
    completion = client.post(item["actions"]["complete"])
    assert completion.status_code == HTTPStatus.NO_CONTENT

    inbox = client.get("/inbox")
    assert inbox.status_code == HTTPStatus.OK
    inbox_content = inbox.get_json()
    item = find_item_by_title(inbox_content["items"], action_title)
    assert item is None
