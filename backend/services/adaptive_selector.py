from typing import Dict, List, Tuple

# ============================================================
# CONFIGURATION
# ============================================================

WEAK_THRESHOLD = 60        # Below this → weak concept
STRONG_THRESHOLD = 85     # Above this → mastered
MAX_CONCEPTS = 8          # Hard cap for quiz generator


# ============================================================
# CORE ENGINE
# ============================================================

def select_adaptive_concepts(
    concept_analysis: Dict[str, Dict],
    all_concepts: List[str],
    per_quiz: int = MAX_CONCEPTS
) -> Dict:
    """
    Selects concepts for the next quiz adaptively.

    Priority:
    1. Weak concepts
    2. Medium concepts
    3. Strong concepts (least priority)

    Returns:
    - selected_concepts
    - breakdown (weak / medium / strong)
    """

    weak = []
    medium = []
    strong = []

    for concept in all_concepts:
        stats = concept_analysis.get(concept, {})
        accuracy = stats.get("accuracy", 0)

        if accuracy < WEAK_THRESHOLD:
            weak.append(concept)
        elif accuracy < STRONG_THRESHOLD:
            medium.append(concept)
        else:
            strong.append(concept)

    # --------------------------------------------------------
    # Deterministic selection order
    # --------------------------------------------------------
    selected = []

    # 1️⃣ Always prioritize weak concepts
    selected.extend(weak)

    # 2️⃣ Fill with medium concepts
    if len(selected) < per_quiz:
        selected.extend(medium)

    # 3️⃣ Fill remaining with strong concepts
    if len(selected) < per_quiz:
        selected.extend(strong)

    # Cap deterministically
    selected = selected[:per_quiz]

    return {
        "selected_concepts": selected,
        "breakdown": {
            "weak": weak,
            "medium": medium,
            "strong": strong
        }
    }
