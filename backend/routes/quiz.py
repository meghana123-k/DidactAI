from flask import Blueprint, request, jsonify

from services.quiz_generator import generate_quiz
from utils.text_preprocessing import extract_text_from_input

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/", methods=["POST"])
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
        quiz = generate_quiz(text)
    except Exception as e:
         return jsonify({"error": f"Quiz generation failed: {e}"}), 500
    return jsonify({
        "source": source,
        "quiz": quiz
    })

