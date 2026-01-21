from flask import Blueprint, request, jsonify

from services.quiz_generator import generate_quiz_from_summary
from utils.text_preprocessing import extract_text_from_input
from services.quiz_validator import validate_quiz
quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/", methods=["POST"], url_prefix="/api/quiz")
def generate_quiz_route():
    """
    Accepts:
    - text (optional)
    - file (optional: pdf / docx / txt)
    - source (optional): raw | summary
    """

    source = request.form.get("source", "summary")

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
        quiz = generate_quiz_from_summary(text)
    except Exception as e:
         return jsonify({"error": f"Quiz generation failed: {e}"}), 500
    return jsonify({
        "source": source,
        "quiz": quiz
    })
@quiz_bp.route("/generate", methods=["POST"])
def generate_quiz():
    """
    Input:
    {
        "summary": "...",
        "mode": "basic | detailed | conceptual"
    }
    """

    data = request.get_json(force=True)

    summary = data.get("summary", "")
    mode = data.get("mode", "conceptual")

    if not summary or not isinstance(summary, str):
        return jsonify({"error": "Summary text is required"}), 400

    try:
        quiz_payload = generate_quiz_from_summary(
            summary=summary,
            mode=mode
        )
        return jsonify(quiz_payload), 200

    except Exception as e:
        return jsonify({
            "error": "Quiz generation failed",
            "details": str(e)
        }), 500


# ============================================================
# 2️⃣ QUIZ SUBMISSION / VALIDATION
# ============================================================
@quiz_bp.route("/submit", methods=["POST"])
def submit_quiz():
    """
    Input:
    {
        "quiz": {...},               # generated quiz
        "answers": {...},            # user answers
        "metadata": {...},           # optional timing / behavior
        "mode": "pre | post"
    }
    """

    data = request.get_json(force=True)

    quiz = data.get("quiz")
    answers = data.get("answers", {})
    metadata = data.get("metadata", {})
    mode = data.get("mode", "post")

    if not quiz or not answers:
        return jsonify({"error": "Quiz and answers are required"}), 400

    try:
        result = validate_quiz(
            quiz=quiz,
            user_answers=answers,
            attempt_metadata=metadata,
            mode=mode
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "error": "Quiz validation failed",
            "details": str(e)
        }), 500