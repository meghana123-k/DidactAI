# backend/tests/test_adaptive_selector.py

from services.adaptive_selector import (
    select_adaptive_concepts,
    generate_adaptive_plan,
    MAX_REQUIZ_CONCEPTS
)


def test_selects_only_weak_concepts():
    concept_analysis = {
        "Photosynthesis": {"accuracy": 50},
        "Chlorophyll": {"accuracy": 90},
        "ATP": {"accuracy": 40}
    }

    result = select_adaptive_concepts(concept_analysis)

    assert "Photosynthesis" in result
    assert "ATP" in result
    assert "Chlorophyll" not in result


def test_respects_max_requiz_limit():
    concept_analysis = {
        f"Concept{i}": {"accuracy": 10}
        for i in range(10)
    }

    result = select_adaptive_concepts(concept_analysis)

    assert len(result) == MAX_REQUIZ_CONCEPTS


def test_no_weak_concepts():
    concept_analysis = {
        "OOP": {"accuracy": 90},
        "Inheritance": {"accuracy": 85}
    }

    result = select_adaptive_concepts(concept_analysis)

    assert result == []


def test_generate_plan_mastery():
    analytics = {
        "concept_progress": {
            "OOP": {"post_accuracy": 95}
        }
    }

    plan = generate_adaptive_plan(analytics, "beginner")

    assert plan["status"] == "mastery_achieved"


def test_generate_plan_requiz():
    analytics = {
        "concept_progress": {
            "OOP": {"post_accuracy": 40},
            "Inheritance": {"post_accuracy": 55}
        }
    }

    plan = generate_adaptive_plan(analytics, "beginner")

    assert plan["status"] == "requiz_required"
    assert len(plan["requiz"]) > 0


def test_first_attempt_handling():
    analytics = {}

    plan = generate_adaptive_plan(analytics, "beginner")

    assert plan["status"] == "first_attempt"
