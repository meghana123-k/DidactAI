from typing import Dict
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================
MASTERY_THRESHOLD = 80        # % accuracy
WEAK_THRESHOLD = 60           # % accuracy


# ============================================================
# CORE ANALYTICS
# ============================================================
def compute_learning_analytics(
    pre_attempt: Dict,
    post_attempt: Dict
) -> Dict:
    """
    Computes learning gain, concept mastery, and difficulty mastery.

    Input contracts:
    - pre_attempt, post_attempt must come from quiz_validator output
    """

    # -------------------- VALIDATION --------------------
    if not pre_attempt or not post_attempt:
        raise ValueError("Empty attempt data provided")

    for key in ("summary", "concept_analysis", "difficulty_analysis"):
        if key not in pre_attempt or key not in post_attempt:
            raise ValueError(f"Missing '{key}' in attempt data")

    pre_acc = pre_attempt["summary"]["accuracy"]
    post_acc = post_attempt["summary"]["accuracy"]

    if not (0 <= pre_acc <= 100 and 0 <= post_acc <= 100):
        raise ValueError("Accuracy must be between 0 and 100")

    # -------------------- FIRST-TIME USER --------------------
    if pre_attempt["summary"].get("total_questions", 0) == 0:
        return {
            "overall": {
                "pre_accuracy": 0,
                "post_accuracy": post_acc,
                "learning_gain": post_acc,
                "improved": True,
                "first_attempt": True
            },
            "concept_progress": {},
            "difficulty_progress": {},
            "timestamp": datetime.utcnow().isoformat()
        }

    # -------------------- OVERALL --------------------
    learning_gain = round(post_acc - pre_acc, 2)

    # -------------------- CONCEPT PROGRESS --------------------
    concept_progress = {}

    pre_concepts = set(pre_attempt["concept_analysis"].keys())
    post_concepts = set(post_attempt["concept_analysis"].keys())

    for concept, post_stats in post_attempt["concept_analysis"].items():
        post_accuracy = post_stats["accuracy"]
        pre_accuracy = pre_attempt["concept_analysis"].get(
            concept, {"accuracy": 0}
        )["accuracy"]

        delta = round(post_accuracy - pre_accuracy, 2)

        concept_progress[concept] = {
            "pre_accuracy": pre_accuracy,
            "post_accuracy": post_accuracy,
            "gain": delta,
            "status": _concept_status(post_accuracy)
        }

    if pre_concepts != post_concepts:
        concept_progress["_metadata"] = {
            "warning": "Concept mismatch detected",
            "missing_in_post": list(pre_concepts - post_concepts),
            "missing_in_pre": list(post_concepts - pre_concepts)
        }

    # -------------------- DIFFICULTY PROGRESS --------------------
    difficulty_progress = {}

    for level, post_stats in post_attempt["difficulty_analysis"].items():
        post_accuracy = post_stats["accuracy"]
        pre_accuracy = pre_attempt["difficulty_analysis"].get(
            level, {"accuracy": 0}
        )["accuracy"]

        difficulty_progress[level] = {
            "pre_accuracy": pre_accuracy,
            "post_accuracy": post_accuracy,
            "gain": round(post_accuracy - pre_accuracy, 2),
            "mastered": post_accuracy >= MASTERY_THRESHOLD
        }

    return {
        "overall": {
            "pre_accuracy": pre_acc,
            "post_accuracy": post_acc,
            "learning_gain": learning_gain,
            "improved": learning_gain > 0
        },
        "concept_progress": concept_progress,
        "difficulty_progress": difficulty_progress,
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================
# HELPERS
# ============================================================
def _concept_status(accuracy: float) -> str:
    if accuracy >= MASTERY_THRESHOLD:
        return "mastered"
    elif accuracy >= WEAK_THRESHOLD:
        return "improving"
    return "weak"
