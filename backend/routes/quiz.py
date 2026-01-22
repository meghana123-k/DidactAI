from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session

from db.session import SessionLocal
from db.models import Quiz, QuizAttempt

from services.quiz_generator import generate_quiz_from_summary
from services.quiz_validator import validate_quiz_attempt
from utils.text_preprocessing import extract_text_from_input

quiz_bp = Blueprint("quiz", __name__, url_prefix="/api/quiz")


# ============================================================
# 1️⃣ GENERATE QUIZ (TEXT / FILE → QUIZ + SAVE SNAPSHOT)
# ============================================================
@quiz_bp.route("/", methods=["POST"])
def generate_quiz():
    """
    Accepts:
    - text (optional)
    - file (optional)
    - mode (basic | detailed | conceptual)
    - user_id (required)
    """

    user_id = request.form.get("user_id")
    mode = request.form.get("mode", "conceptual")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    try:
        text = extract_text_from_input(
            text=request.form.get("text"),
            file=request.files.get("file")
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if not text:
        return jsonify({"error": "No input text provided"}), 400

    try:
        quiz_payload = generate_quiz_from_summary(
            summary=text,
            mode=mode
        )
    except Exception as e:
        return jsonify({"error": f"Quiz generation failed: {e}"}), 500

    db: Session = SessionLocal()
    try:
        quiz = Quiz(
            user_id=user_id,
            mode=mode,
            summary_source="input_text",
            quiz_payload=quiz_payload
        )
        db.add(quiz)
        db.commit()
        db.refresh(quiz)

        return jsonify({
            "quiz_id": str(quiz.id),
            "quiz": quiz_payload
        }), 200
    finally:
        db.close()


# ============================================================
# 2️⃣ PURE VALIDATION ENDPOINT (FOR TESTING)
# ============================================================
@quiz_bp.route("/validate", methods=["POST"])
def validate_only():
    """
    PURE validator endpoint.
    No DB. No scoring. Used for your 5 test cases.
    """

    data = request.get_json()

    if "quiz" not in data or "user_answers" not in data:
        return jsonify({"error": "quiz and user_answers are required"}), 400

    result = validate_quiz_attempt(
        quiz=data["quiz"],
        user_answers=data["user_answers"],
        attempt_metadata=data.get("attempt_metadata")
    )

    return jsonify(result), 200


# ============================================================
# 3️⃣ SUBMIT QUIZ ATTEMPT (RAW VALIDATION + PERSIST)
# ============================================================
@quiz_bp.route("/submit", methods=["POST"])
def submit_quiz():
    payload = request.get_json()

    required_fields = [
        "student_id",
        "topic",
        "assessment_phase",
        "summary_mode",
        "quiz",
        "user_answers"
    ]

    for field in required_fields:
        if field not in payload:
            return jsonify({"error": f"Missing field: {field}"}), 400

    if payload["assessment_phase"] not in ("pre", "post"):
        return jsonify({"error": "assessment_phase must be pre or post"}), 400

    attempt_result = validate_quiz_attempt(
        quiz=payload["quiz"],
        user_answers=payload["user_answers"],
        attempt_metadata=payload.get("attempt_metadata")
    )

    db: Session = SessionLocal()
    try:
        attempt = QuizAttempt(
            student_id=payload["student_id"],
            topic=payload["topic"],
            assessment_phase=payload["assessment_phase"],
            summary_mode=payload["summary_mode"],

            raw_results=attempt_result["results"],
            concept_events=attempt_result["concept_events"],

            attempt_metadata=payload.get("attempt_metadata", {})
        )

        db.add(attempt)
        db.commit()

        return jsonify({
            "attempt_result": attempt_result
        }), 200

    finally:
        db.close()
