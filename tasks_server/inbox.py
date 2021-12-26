from enum import Enum
from http import HTTPStatus
from flask import Blueprint, request, make_response, url_for

from tasks_server.db import get_db

inbox = Blueprint("inbox", __name__, url_prefix="/inbox")


class TaskStatus(Enum):
    NEW = 0
    DEFERRED = 1
    ACTIONABLE = 2
    COMPLETED = 4
    DROPPED = 4


def web_model_for(item):
    return {
        "title": item["title"],
        "description": item["description"],
        "actions": {
            "complete": url_for("inbox.complete_item", item_id=item["id"], _external=True)
        }
    }


@inbox.route("", methods=["GET"])
def list_inbox():
    db = get_db()
    query_result = \
        db.execute("select id, title, description from task where status = ?",
                   [TaskStatus.NEW.value]).fetchall()
    return {
        "items": list(map(
            lambda item: web_model_for(item),
            query_result
        ))
    }


@inbox.route("", methods=["POST"])
def add_inbox_item():
    data = request.get_json()
    title = data["title"]
    description = ""
    if "description" in data:
        description = data["description"]

    db = get_db()
    query_result = \
        db.execute("insert into task (title, description) values (?, ?) returning id",
                   [title, description]).fetchone()
    db.commit()

    response = make_response()
    response.status_code = HTTPStatus.CREATED
    response.headers["Location"] = \
        url_for("inbox.get_item", item_id=query_result["id"], _external=True)
    return response


@inbox.route("/<item_id>", methods=["GET"])
def get_item(item_id):
    db = get_db()
    query_result = \
        db.execute("select id, title, description from task where id = ?",
                   [item_id]).fetchone()
    return web_model_for(query_result)


@inbox.route("/<item_id>/complete", methods=["POST"])
def complete_item(item_id):
    db = get_db()
    db.execute("update task set status = ? where id = ?",
               [TaskStatus.COMPLETED.value, item_id])
    db.commit()
    return '', HTTPStatus.NO_CONTENT


@inbox.route("/<item_id>", methods=["DELETE"])
def delete_inbox_item(item_id):
    db = get_db()
    db.execute("delete from task where id = ?", [item_id])
    db.commit()
    return '', HTTPStatus.NO_CONTENT
