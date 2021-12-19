from http import HTTPStatus
from flask import Blueprint, request

from tasks_server.db import get_db

bp = Blueprint("inbox", __name__, url_prefix="/inbox")


@bp.route("/", methods=["GET"])
def list_inbox():
    db = get_db()
    actions = list(map(
        lambda action: {"id": action["id"], "title": action["title"]},
        db.execute("select id, title from task").fetchall()))
    return {
        "items": actions
    }


@bp.route("/", methods=["POST"])
def add_inbox_item():
    data = request.get_json()
    db = get_db()
    db.execute("insert into task (title) values (?)", [data["title"]])
    db.commit()
    return '', HTTPStatus.NO_CONTENT


@bp.route("/<id>", methods=["DELETE"])
def delete_inbox_item(id):
    db = get_db()
    db.execute("delete from task where id = ?", [id])
    db.commit()
    return '', HTTPStatus.NO_CONTENT
