# backend/services/adaptive_selector.py

from typing import Dict, List

WEAK_THRESHOLD = 60
MAX_REQUIZ_CONCEPTS = 5


def select_adaptive_concepts(
    concept_analysis: Dict[str, Dict]
) -> List[str]:
    """
    Selects weak concepts deterministically.
    """

    if not concept_analysis:
        return []

    weak = [
        (concept, stats.get("accuracy", 0))
        for concept, stats in concept_analysis.items()
        if stats.get("accuracy", 0) < WEAK_THRESHOLD
    ]

    # Sort weakest first, deterministic
    weak_sorted = sorted(weak, key=lambda x: x[1])

    return [c for c, _ in weak_sorted[:MAX_REQUIZ_CONCEPTS]]


def generate_adaptive_plan(
    analytics: Dict,
    current_level: str
) -> Dict:
    """
    Generates next learning plan based on analytics output.
    """

    concept_progress = analytics.get("concept_progress", {})

    if not concept_progress:
        return {
            "status": "first_attempt",
            "requiz": [],
            "message": "No prior data available"
        }

    # Normalize for selector
    concept_analysis = {
        concept: {"accuracy": data.get("post_accuracy", 0)}
        for concept, data in concept_progress.items()
    }

    weak_concepts = select_adaptive_concepts(concept_analysis)

    if not weak_concepts:
        return {
            "status": "mastery_achieved",
            "requiz": [],
            "message": "All concepts mastered"
        }

    return {
        "status": "requiz_required",
        "requiz": weak_concepts,
        "next_level": current_level
    }
