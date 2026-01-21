from typing import Dict, List, Any
from collections import defaultdict
from datetime import datetime
# ============================================================
# CONFIGURATION
# ============================================================
DIFFICULTY_WEIGHTS = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3
}

PASS_PERCENTAGE = 60  # configurable


# ============================================================
# CORE VALIDATION LOGIC
# ============================================================
def validate_quiz_attempt(
    quiz: Dict,
    user_answers: Dict[str, str],
    attempt_metadata: Dict[str, Dict] = None,
    mode: str = "post"
) -> Dict:
    """
    Validates a full quiz attempt.

    Parameters:
    - quiz: generated quiz object (from quiz_generator)
    - user_answers: {question_id: selected_option}
    - attempt_metadata: optional timing/behavioral data
    - mode: pre / post (for learning gain support)

    Returns:
    - structured evaluation result
    """

    attempt_metadata = attempt_metadata or {}

    total_score = 0
    max_score = 0
    total_questions = 0
    correct_answers = 0

    difficulty_stats = defaultdict(lambda: {"attempted": 0, "correct": 0})
    concept_stats = defaultdict(lambda: {"attempted": 0, "correct": 0})

    detailed_results = []

    for level, questions in quiz["quiz"].items():
        for idx, q in enumerate(questions):
            question_id = f"{level}_{idx}"
            selected = user_answers.get(question_id)
            correct = q["answer"]
            difficulty = q["difficulty"]
            concept = q["answer"]  # atomic normalization

            weight = DIFFICULTY_WEIGHTS.get(difficulty, 1)

            is_correct = selected == correct

            # ---- scoring ----
            max_score += weight
            total_questions += 1
            difficulty_stats[difficulty]["attempted"] += 1
            concept_stats[concept]["attempted"] += 1

            if is_correct:
                total_score += weight
                correct_answers += 1
                difficulty_stats[difficulty]["correct"] += 1
                concept_stats[concept]["correct"] += 1

            detailed_results.append({
                "question_id": question_id,
                "difficulty": difficulty,
                "concept": concept,
                "selected": selected,
                "correct_answer": correct,
                "is_correct": is_correct,
                "weight": weight,
                "time_taken": attempt_metadata.get(question_id, {}).get("time_taken"),
            })

    # ============================================================
    # METRICS
    # ============================================================
    accuracy = round((correct_answers / total_questions) * 100, 2) if total_questions else 0

    difficulty_breakdown = {
        d: {
            "accuracy": round(
                (v["correct"] / v["attempted"]) * 100, 2
            ) if v["attempted"] else 0
        }
        for d, v in difficulty_stats.items()
    }

    concept_breakdown = {
        c: {
            "accuracy": round(
                (v["correct"] / v["attempted"]) * 100, 2
            ) if v["attempted"] else 0
        }
        for c, v in concept_stats.items()
    }

    passed = accuracy >= PASS_PERCENTAGE

    # ============================================================
    # FINAL RESPONSE
    # ============================================================
    return {
        "summary": {
            "mode": mode,
            "total_score": total_score,
            "max_score": max_score,
            "accuracy": accuracy,
            "passed": passed,
            "timestamp": datetime.utcnow().isoformat()
        },
        "difficulty_analysis": difficulty_breakdown,
        "concept_analysis": concept_breakdown,
        "detailed_results": detailed_results
    }

def validate_single_answer(
    correct_answer: str,
    selected_option: str
) -> bool:
    """
    Returns True if the selected option is correct.
    """
    return correct_answer.strip() == selected_option.strip()



def validate_quiz(
    quiz: Dict[str, List[Dict[str, Any]]],
    user_answers: Dict[str, List[int]]
) -> Dict[str, Any]:
    """
    Validates an entire quiz submission.

    Parameters:
    - quiz: generated quiz (grouped by difficulty)
    - user_answers: selected option indices per difficulty

    Returns:
    - detailed evaluation report
    """

    report = {
        "total_questions": 0,
        "total_correct": 0,
        "score_percent": 0.0,
        "by_level": {},
        "by_question": []
    }

    for level, questions in quiz.items():
        level_correct = 0
        level_total = len(questions)

        answers_for_level = user_answers.get(level, [])

        for idx, question in enumerate(questions):
            # Defensive checks
            if idx >= len(answers_for_level):
                selected_index = None
                selected_option = None
                is_correct = False
            else:
                selected_index = answers_for_level[idx]
                options = question["options"]

                if selected_index < 0 or selected_index >= len(options):
                    selected_option = None
                    is_correct = False
                else:
                    selected_option = options[selected_index]
                    is_correct = validate_single_answer(
                        question["answer"],
                        selected_option
                    )

            if is_correct:
                level_correct += 1
                report["total_correct"] += 1

            report["by_question"].append({
                "level": level,
                "question": question["question"],
                "selected_option": selected_option,
                "correct_answer": question["answer"],
                "is_correct": is_correct
            })

        report["by_level"][level] = {
            "correct": level_correct,
            "total": level_total,
            "accuracy": round(
                (level_correct / level_total) * 100, 2
            ) if level_total else 0.0
        }

        report["total_questions"] += level_total

    if report["total_questions"] > 0:
        report["score_percent"] = round(
            (report["total_correct"] / report["total_questions"]) * 100, 2
        )

    return report
