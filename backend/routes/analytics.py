from flask import Blueprint, jsonify

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/", methods=["GET"])
def analytics_health():
    return jsonify({
        "status": "ok",
        "message": "Analytics route placeholder working"
    })
