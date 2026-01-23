from flask import Blueprint, request, jsonify

from services.summarizer.abstractive import explain
from services.summarizer.extractive import extractive_summary
from services.summarizer.conceptual import get_conceptual_summary
from utils.text_preprocessing import extract_text_from_input

summarize_bp = Blueprint("summarize", __name__)


@summarize_bp.route("/", methods=["POST"])
def summarize():
    mode = request.form.get("mode", "").lower()

    try:
        text = extract_text_from_input(
            text=request.form.get("text"),
            file=request.files.get("file")
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if not text or mode not in {"basic", "detailed", "overview"}:
        return jsonify({"error": "Invalid input"}), 400

    response = {"mode": mode}

    # ---------------- BASIC ----------------
    if mode == "basic":
        llm_output = explain(text, mode="basic")
        response.update(llm_output)

    # --------------- DETAILED --------------
    elif mode == "detailed":
        extracted = extractive_summary(text, ratio=0.35)
        if not extracted:
            return jsonify({"error": "Extractive summarization failed"}), 500

        llm_output = explain(extracted, mode="detailed")
        response.update(llm_output)

    # --------------- OVERVIEW --------------
    else:
        concept_data = get_conceptual_summary(text)
        concepts = concept_data.get("key_concepts", [])

        if not concepts:
            return jsonify({"error": "Concept extraction failed"}), 500

        concept_text = "Key concepts:\n" + "\n".join(f"- {c}" for c in concepts)
        llm_output = explain(concept_text, mode="overview")

        response.update(llm_output)
        response["concepts"] = concepts
        response["concept_source"] = concept_data.get("source")
        response["concept_confidence"] = concept_data.get("confidence")

    return jsonify(response)
