from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session

from db.session import SessionLocal
from db.models import Quiz, QuizAttempt, QuestionResponse

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
    - file (optional: pdf / docx / txt)
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
# 2️⃣ SUBMIT QUIZ ATTEMPT (VALIDATE + ANALYTICS + PERSIST)
# ============================================================
@quiz_bp.route("/submit", methods=["POST"])
def submit_quiz():
    """
    Orchestrates quiz submission:
    - validation
    - analytics
    - persistence
    - certificate update
    """

    payload = request.get_json()

    # -------------------------------
    # 1. BASIC VALIDATION
    # -------------------------------
    required_keys = {"user_id", "quiz", "user_answers"}
    if not payload or not required_keys.issubset(payload):
        return jsonify({"error": "Invalid submission payload"}), 400

    user_id = payload["user_id"]
    quiz = payload["quiz"]
    user_answers = payload["user_answers"]
    mode = payload.get("mode", "post")

    # -------------------------------
    # 2. FETCH PREVIOUS ATTEMPT (if any)
    # -------------------------------
    pre_attempt = get_last_attempt(user_id)

    if not pre_attempt:
        # First-time user baseline
        pre_attempt = {
            "summary": {"accuracy": 0},
            "concept_analysis": {},
            "difficulty_analysis": {}
        }

    # -------------------------------
    # 3. VALIDATE QUIZ ATTEMPT
    # -------------------------------
    evaluation = validate_quiz_attempt(
        quiz=quiz,
        user_answers=user_answers,
        mode=mode
    )

    # -------------------------------
    # 4. COMPUTE ANALYTICS
    # -------------------------------
    analytics = compute_learning_analytics(
        pre_attempt=pre_attempt,
        post_attempt=evaluation
    )

    # -------------------------------
    # 5. PERSIST ATTEMPT
    # -------------------------------
    save_quiz_attempt(
        user_id=user_id,
        attempt_payload={
            "evaluation": evaluation,
            "analytics": analytics
        }
    )

    # -------------------------------
    # 6. CERTIFICATE LOGIC (HIGHEST SCORE)
    # -------------------------------
    certificate_status = create_or_update_certificate(
        user_id=user_id,
        accuracy=evaluation["summary"]["accuracy"]
    )

    # -------------------------------
    # 7. RESPONSE
    # -------------------------------
    return jsonify({
        "evaluation": evaluation,
        "analytics": analytics,
        "certificate": certificate_status
    }), 200