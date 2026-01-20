from flask import Blueprint, jsonify

certificate_bp = Blueprint("certificate", __name__)


@certificate_bp.route("/", methods=["GET"])
def certificate_health():
    return jsonify({
        "status": "ok",
        "message": "Certificate route placeholder working"
    })
