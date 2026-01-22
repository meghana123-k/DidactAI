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
    Input JSON:
    {
        "quiz_id": "...",
        "user_id": "...",
        "answers": {...},
        "metadata": {...}   # optional timing / behavior
    }
    """

    data = request.get_json(force=True)

    quiz_id = data.get("quiz_id")
    user_id = data.get("user_id")
    user_answers = data.get("answers")
    attempt_metadata = data.get("metadata", {})

    if not quiz_id or not user_id or not user_answers:
        return jsonify({
            "error": "quiz_id, user_id, and answers are required"
        }), 400

    db: Session = SessionLocal()

    try:
        quiz = db.query(Quiz).filter_by(id=quiz_id).first()
        if not quiz:
            return jsonify({"error": "Quiz not found"}), 404

        # Determine attempt number
        attempt_number = (
            db.query(QuizAttempt)
            .filter_by(quiz_id=quiz_id, user_id=user_id)
            .count()
            + 1
        )

        # Validate quiz
        evaluation = validate_quiz_attempt(
            quiz=quiz.quiz_payload,
            user_answers=user_answers,
            attempt_metadata=attempt_metadata,
            mode="post"
        )

        # Persist attempt
        attempt = QuizAttempt(
            quiz_id=quiz.id,
            user_id=user_id,
            attempt_number=attempt_number,
            mode=quiz.mode,
            total_score=evaluation["summary"]["total_score"],
            max_score=evaluation["summary"]["max_score"],
            accuracy=evaluation["summary"]["accuracy"],
            passed=evaluation["summary"]["passed"],
            analytics_snapshot=evaluation,
            difficulty_progress=evaluation.get("difficulty_analysis"),
            concept_progress=evaluation.get("concept_analysis"),
        )

        db.add(attempt)
        db.commit()
        db.refresh(attempt)

        # Persist per-question responses
        for q in evaluation.get("detailed_results", []):
            db.add(QuestionResponse(
                attempt_id=attempt.id,
                question_id=q["question_id"],
                concept=q.get("concept"),
                difficulty=q.get("difficulty"),
                selected_option=q.get("selected"),
                correct_option=q.get("correct_answer"),
                is_correct=q.get("is_correct"),
                time_taken=q.get("time_taken"),
            ))

        db.commit()

        return jsonify({
            "attempt_id": str(attempt.id),
            "evaluation": evaluation
        }), 200

    finally:
        db.close()
