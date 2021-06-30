from celery.result import AsyncResult
from flask import current_app, Blueprint, jsonify, request

import app.services as services

bp = Blueprint("all", __name__)

@bp.route("/")
def index():
    return "Hello!"

@bp.before_request
def before_request():
    if request.method=='OPTIONS':
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
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200

@bp.route("/sleep/<int:amount>")
def sleep(amount):
    async_result = services.sleep.delay(amount, "hello, world")
    return jsonify({"msg": "process started", "task_id": async_result.id, "status": 202}), 202
