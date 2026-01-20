from flask import Blueprint, request, jsonify

from services.summarizer.abstractive import explain
from services.summarizer.extractive import extractive_summary
from services.summarizer.conceptual import get_conceptual_summary
from utils.text_preprocessing import extract_text_from_input

# Blueprint registration
summarize_bp = Blueprint("summarize", __name__)


@summarize_bp.route("/", methods=["POST"])
def summarize():
    """
    Summarization endpoint.

    Accepts:
    - text (optional)
    - file (optional: pdf / doc / docx / txt)
    - mode: basic | detailed | overview

    Behavior:
    - basic    -> LLM only (abstractive)
    - detailed -> extractive -> LLM
    - overview -> conceptual extraction -> LLM

    NOTE:
    - No direct OpenAI / Gemini calls here
    - All LLM usage is routed ONLY through abstractive.py
    """

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

    # ---------------- BASIC ----------------
    if mode == "basic":
        summary = explain(text, mode="basic")

    # --------------- DETAILED --------------
    elif mode == "detailed":
        extracted = extractive_summary(text, ratio=0.35)

        if not extracted:
            return jsonify({"error": "Extractive summarization failed"}), 500

        summary = explain(extracted, mode="detailed")

    # --------------- OVERVIEW --------------
    else:  # overview
        concept_data = get_conceptual_summary(text)
        concepts = concept_data.get("key_concepts", [])

        if not concepts:
            return jsonify({"error": "Concept extraction failed"}), 500

        concept_text = "Key concepts:\n" + "\n".join(f"- {c}" for c in concepts)
        summary = explain(concept_text, mode="overview")

    # ---------------- RESPONSE ----------------
    return jsonify({
        "mode": mode,
        "summary": summary
    })
