from flask import Blueprint, request, jsonify
from services.quiz_generator import QuizGenerator
from services.quiz_validator import QuizValidator

quiz_bp = Blueprint("quiz", __name__)

generator = QuizGenerator()
validator = QuizValidator()

@quiz_bp.route("/generate", methods=["POST"])
def generate_quiz():
    data = request.json

    quiz = generator.generate_quiz(
        summary=data["summary"],
        concepts=data["concepts"],
        key_terms=data["key_terms"],
        relationships=data["relationships"]
    )

    validated = {}
    for level, questions in quiz.items():
        validated[level.value] = validator.validate_and_score(questions)

    return jsonify(validated)
