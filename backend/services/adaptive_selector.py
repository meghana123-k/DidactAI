from typing import Dict, List, Tuple

# ============================================================
# CONFIG
# ============================================================
WEAK_THRESHOLD = 60
MAX_REQUIZ_CONCEPTS = 5


# ============================================================
# CORE SELECTION
# ============================================================
def select_adaptive_concepts(
    concept_analysis: Dict[str, Dict]
) -> List[str]:
    """
    Selects weak concepts deterministically.
    """

    if not concept_analysis:
        return []

    weak = [
        (concept, stats["accuracy"])
        for concept, stats in concept_analysis.items()
        if "accuracy" in stats and stats["accuracy"] < WEAK_THRESHOLD
    ]

    weak.sort(key=lambda x: x[1])  # weakest first
    return [c for c, _ in weak[:MAX_REQUIZ_CONCEPTS]]


# ============================================================
# PLAN GENERATION
# ============================================================
def generate_adaptive_plan(
    analytics: Dict,
    current_level: str
) -> Dict:
    """
    Generates re-quiz plan based on analytics_engine output.
    """

    concept_progress = analytics.get("concept_progress", {})

    # Convert analytics format → selector format
    concept_analysis = {
        concept: {"accuracy": data["post_accuracy"]}
        for concept, data in concept_progress.items()
        if isinstance(data, dict) and "post_accuracy" in data
    }

    weak_concepts = select_adaptive_concepts(concept_analysis)

    if not weak_concepts:
        return {
            "status": "mastery_achieved",
            "next_level": current_level,
            "requiz": []
        }

    return {
        "status": "requiz_required",
        "current_level": current_level,
        "requiz": weak_concepts
    }
