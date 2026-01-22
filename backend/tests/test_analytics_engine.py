# backend/tests/test_analytics_engine.py

import pytest
from services.analytics_engine import compute_learning_analytics


# --------------------------------------------------
# FIXTURES
# --------------------------------------------------

@pytest.fixture
def pre_attempt_basic():
    return {
        "summary": {"accuracy": 40},
        "concept_analysis": {
            "Photosynthesis": {"accuracy": 40},
            "Chlorophyll": {"accuracy": 50}
        },
        "difficulty_analysis": {
            "beginner": {"accuracy": 50},
            "intermediate": {"accuracy": 30}
        }
    }


@pytest.fixture
def post_attempt_improved():
    return {
        "summary": {"accuracy": 80},
        "concept_analysis": {
            "Photosynthesis": {"accuracy": 80},
            "Chlorophyll": {"accuracy": 90}
        },
        "difficulty_analysis": {
            "beginner": {"accuracy": 90},
            "intermediate": {"accuracy": 70}
        }
    }


# --------------------------------------------------
# TESTS
# --------------------------------------------------

def test_learning_gain_computation(pre_attempt_basic, post_attempt_improved):
    result = compute_learning_analytics(pre_attempt_basic, post_attempt_improved)

    assert result["overall"]["learning_gain"] == 40
    assert result["overall"]["improved"] is True


def test_concept_mastery_status(pre_attempt_basic, post_attempt_improved):
    result = compute_learning_analytics(pre_attempt_basic, post_attempt_improved)

    concepts = result["concept_progress"]

    assert concepts["Photosynthesis"]["status"] == "mastered"
    assert concepts["Chlorophyll"]["status"] == "mastered"


def test_difficulty_mastery(pre_attempt_basic, post_attempt_improved):
    result = compute_learning_analytics(pre_attempt_basic, post_attempt_improved)

    difficulty = result["difficulty_progress"]

    assert difficulty["beginner"]["mastered"] is True
    assert difficulty["intermediate"]["mastered"] is False


def test_first_time_user_handling():
    pre = {
        "summary": {"accuracy": 0},
        "concept_analysis": {},
        "difficulty_analysis": {}
    }

    post = {
        "summary": {"accuracy": 60},
        "concept_analysis": {
            "OOP": {"accuracy": 60}
        },
        "difficulty_analysis": {
            "beginner": {"accuracy": 60}
        }
    }

    result = compute_learning_analytics(pre, post)

    assert result["overall"]["learning_gain"] == 60
    assert result["overall"]["improved"] is True


def test_perfect_score_no_gain():
    pre = {
        "summary": {"accuracy": 100},
        "concept_analysis": {
            "Encapsulation": {"accuracy": 100}
        },
        "difficulty_analysis": {
            "advanced": {"accuracy": 100}
        }
    }

    post = pre.copy()

    result = compute_learning_analytics(pre, post)

    assert result["overall"]["learning_gain"] == 0
    assert result["overall"]["improved"] is False


def test_invalid_input_raises_error():
    with pytest.raises(ValueError):
        compute_learning_analytics({}, {})
