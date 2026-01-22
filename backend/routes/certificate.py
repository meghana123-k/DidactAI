from flask import Blueprint, request, jsonify
from services.certificate_generator import generate_or_update_certificate

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
        "previous_certificate": {...}      # optional
    }
    """

    data = request.get_json()

    # ----------------------------
    # Basic validation
    # ----------------------------
    student_id = data.get("student_id")
    topic = data.get("topic")
    analytics = data.get("analytics")
    previous_certificate = data.get("previous_certificate")

    if not student_id or not topic or not analytics:
        return jsonify({
            "error": "Missing required fields: student_id, topic, analytics"
        }), 400

    try:
        result = generate_or_update_certificate(
            student_id=student_id,
            topic=topic,
            analytics=analytics,
            previous_certificate=previous_certificate
        )

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:
        # Fail-safe for unexpected issues
        return jsonify({
            "error": "Certificate generation failed",
            "details": str(e)
        }), 500
