from flask import Blueprint, request, jsonify
from services.integrity_monitor import IntegrityMonitor, QuestionBehavior
from services.analytics import AnalyticsEngine

analytics_bp = Blueprint("analytics", __name__)

monitor = IntegrityMonitor()
engine = AnalyticsEngine()

@analytics_bp.route("/submit", methods=["POST"])
def submit_quiz():
    data = request.json

    behaviors = [
        QuestionBehavior(**b) for b in data["behaviors"]
    ]

    integrity_result = monitor.compute_integrity_score(behaviors)
    analytics = engine.compute_metrics(
        questions=data["questions"],
        integrity_score=integrity_result["integrity_score"],
        baseline_score=data.get("baseline_score")
    )

    return jsonify({
        "integrity": integrity_result,
        "analytics": analytics
    })
