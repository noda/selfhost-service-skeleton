from flask import current_app, Blueprint, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from celery import chain

from app import celery
import app.services as services


bp = Blueprint("all", __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    users = current_app.config.get("httpauth")
    if username in users and check_password_hash(users.get(username), password):
        return username


@bp.route("/")
def index():
    return "Hello!"


@bp.before_request
def before_request():
    if request.method == "OPTIONS":
        return jsonify({}), 200


@bp.errorhandler(500)
def internal_error(error):
    return jsonify({"msg": "Internal Server Error", "status": 500}), 500


@bp.errorhandler(400)
def bad_request(error):
    return jsonify({"msg": "Bad Request", "status": 400}), 400


@bp.errorhandler(404)
def not_found(error):
    return jsonify({"msg": "Not Found", "status": 404}), 404


@bp.route("/tasks/<task_id>", methods=["GET"])
@auth.login_required
def get_status(task_id):
    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return jsonify(result), 200


@bp.route("/sleep/<int:amount>")
@auth.login_required
def sleep(amount):
    async_result = services.sleep.delay(amount, "hello, world")
    return (
        jsonify({"msg": "process started", "task_id": async_result.id, "status": 202}),
        202,
    )


@bp.route("/math/<int:a>/<int:b>")
@auth.login_required
def maths(a, b):
    async_result = chain(services.add.s(a, b), services.add.s(100)).delay()
    return (
        jsonify({"msg": "process started", "task_id": async_result.id, "status": 202}),
        202,
    )
