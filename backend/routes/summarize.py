from flask import Blueprint, request, jsonify
from services.summarizer.extractive import extractive_summary
from services.summarizer.abstractive import AbstractiveSummarizer
from services.summarizer.conceptual import ConceptualSummarizer

summarize_bp = Blueprint("summarize", __name__)

abstractive = AbstractiveSummarizer()
conceptual = ConceptualSummarizer()

@summarize_bp.route("/", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text")

    extractive = extractive_summary(text)
    abstractive_summary = abstractive.summarize(text)
    conceptual_summary = conceptual.summarize(text)

    return jsonify({
        "extractive": extractive,
        "abstractive": abstractive_summary,
        "conceptual": conceptual_summary
    })
