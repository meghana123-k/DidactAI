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
    payload = request.get_json()

    # -----------------------------
    # 1. Basic validation
    # -----------------------------
    required_fields = [
        "student_id", "topic",
        "assessment_phase", "summary_mode",
        "quiz", "user_answers"
    ]

    for field in required_fields:
        if field not in payload:
            return jsonify({"error": f"Missing field: {field}"}), 400

    student_id = payload["student_id"]
    topic = payload["topic"]
    assessment_phase = payload["assessment_phase"]
    summary_mode = payload["summary_mode"]
    quiz = payload["quiz"]
    user_answers = payload["user_answers"]
    attempt_metadata = payload.get("attempt_metadata", {})

    if assessment_phase not in ("pre", "post"):
        return jsonify({"error": "assessment_phase must be pre or post"}), 400

    # -----------------------------
    # 2. Validate quiz attempt
    # -----------------------------
    attempt_result = validate_quiz_attempt(
        quiz=quiz,
        user_answers=user_answers,
        attempt_metadata=attempt_metadata,
        mode=assessment_phase
    )

    # -----------------------------
    # 3. Persist quiz attempt
    # -----------------------------
    db: Session = get_db_session()

    attempt = QuizAttempt(
        student_id=student_id,
        topic=topic,
        assessment_phase=assessment_phase,
        summary_mode=summary_mode,

        accuracy=attempt_result["summary"]["accuracy"],
        total_score=attempt_result["summary"]["total_score"],
        max_score=attempt_result["summary"]["max_score"],

        difficulty_analysis=attempt_result["difficulty_analysis"],
        concept_analysis=attempt_result["concept_analysis"],

        attempt_metadata=attempt_metadata
    )

    db.add(attempt)
    db.commit()

    # -----------------------------
    # 4. Analytics (only if post)
    # -----------------------------
    analytics = None
    certificate = None

    if assessment_phase == "post":
        # fetch latest pre attempt if exists
        pre_attempt = (
            db.query(QuizAttempt)
            .filter_by(
                student_id=student_id,
                topic=topic,
                assessment_phase="pre"
            )
            .order_by(QuizAttempt.created_at.desc())
            .first()
        )

        analytics = compute_learning_analytics(
            pre_attempt=pre_attempt.__dict__ if pre_attempt else {
                "summary": {"accuracy": 0},
                "concept_analysis": {},
                "difficulty_analysis": {}
            },
            post_attempt=attempt_result
        )

        # -----------------------------
        # 5. Certificate logic
        # -----------------------------
        certificate = create_or_update_certificate(
            db=db,
            student_id=student_id,
            topic=topic,
            accuracy=attempt_result["summary"]["accuracy"],
            analytics=analytics
        )

    # -----------------------------
    # 6. Response
    # -----------------------------
    return jsonify({
        "attempt_result": attempt_result,
        "analytics": analytics,
        "certificate": certificate
    }), 200