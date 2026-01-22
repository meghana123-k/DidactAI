from flask import Blueprint, request, jsonify
from services.certificate_generator import create_or_update_certificate

certificate_bp = Blueprint("certificate", __name__)


@certificate_bp.route("/certificate", methods=["POST"])
def issue_certificate():
    """
    Issues or updates a certificate based on highest-score policy.

    Expected JSON payload:
    {
        "student_id": "string",
        "topic": "string",
        "analytics": {...},                # output of analytics_engine
        "existing_certificate": {...}      # optional
    }
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid or missing JSON payload"
        }), 400

    # ----------------------------
    # Basic validation
    # ----------------------------
    student_id = data.get("student_id")
    topic = data.get("topic")
    analytics = data.get("analytics")
    existing_certificate = data.get("existing_certificate")

    if not student_id or not topic or not analytics:
        return jsonify({
            "error": "Missing required fields: student_id, topic, analytics"
        }), 400

    try:
        result = create_or_update_certificate(
            student_id=student_id,
            topic=topic,
            analytics=analytics,
            existing_certificate=existing_certificate
        )

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "error": "Certificate generation failed",
            "details": str(e)
        }), 500
