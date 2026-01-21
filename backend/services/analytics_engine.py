from typing import Dict, List
from statistics import mean
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

MASTERY_THRESHOLDS = {
    "strong": 80,     # >= 80%
    "medium": 50,     # 50–79%
    "weak": 0         # < 50%
}

LEARNING_GAIN_THRESHOLDS = {
    "high": 20,       # +20% improvement
    "moderate": 10,   # +10–19%
    "low": 0          # < +10%
}

# ============================================================
# CORE ANALYTICS ENGINE
# ============================================================

def analyze_quiz_performance(
    validation_result: Dict,
    previous_performance: Dict = None
) -> Dict:
    """
    Converts quiz validation output into learning analytics.

    Inputs:
    - validation_result → output from quiz_validator.validate_quiz_attempt
    - previous_performance → optional historical data (same structure)

    Outputs:
    - mastery per concept
    - difficulty readiness
    - learning gain
    - weak concepts for re-quiz
    """

    concept_analysis = validation_result.get("concept_analysis", {})
    difficulty_analysis = validation_result.get("difficulty_analysis", {})
    summary = validation_result.get("summary", {})

    # --------------------------------------------------------
    # CONCEPT MASTERY
    # --------------------------------------------------------
    concept_mastery = {}
    weak_concepts = []

    for concept, stats in concept_analysis.items():
        accuracy = stats.get("accuracy", 0)

        label = _mastery_label(accuracy)

        concept_mastery[concept] = {
            "accuracy": accuracy,
            "level": label
        }

        if label == "weak":
            weak_concepts.append(concept)

    # --------------------------------------------------------
    # DIFFICULTY READINESS
    # --------------------------------------------------------
    difficulty_readiness = {}

    for level, stats in difficulty_analysis.items():
        accuracy = stats.get("accuracy", 0)

        difficulty_readiness[level] = {
            "accuracy": accuracy,
            "ready": accuracy >= 60
        }

    # --------------------------------------------------------
    # LEARNING GAIN (OPTIONAL, IF PREVIOUS DATA EXISTS)
    # --------------------------------------------------------
    learning_gain = None

    if previous_performance:
        prev_accuracy = previous_performance.get("summary", {}).get("accuracy", 0)
        curr_accuracy = summary.get("accuracy", 0)

        delta = round(curr_accuracy - prev_accuracy, 2)

        learning_gain = {
            "previous_accuracy": prev_accuracy,
            "current_accuracy": curr_accuracy,
            "gain": delta,
            "label": _learning_gain_label(delta)
        }

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "overall_accuracy": summary.get("accuracy", 0),
        "passed": summary.get("passed", False),

        "concept_mastery": concept_mastery,
        "weak_concepts": weak_concepts,

        "difficulty_readiness": difficulty_readiness,

        "learning_gain": learning_gain
    }


# ============================================================
# HELPERS
# ============================================================

def _mastery_label(accuracy: float) -> str:
    if accuracy >= MASTERY_THRESHOLDS["strong"]:
        return "strong"
    elif accuracy >= MASTERY_THRESHOLDS["medium"]:
        return "medium"
    return "weak"


def _learning_gain_label(delta: float) -> str:
    if delta >= LEARNING_GAIN_THRESHOLDS["high"]:
        return "high"
    elif delta >= LEARNING_GAIN_THRESHOLDS["moderate"]:
        return "moderate"
    return "low"
