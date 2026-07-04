from app.services import scoring_service
from app import models


class FakeQuestion:
    def __init__(self, id, type, options, weight=1.0, logic_rules=None):
        self.id = id
        self.type = type
        self.options = options
        self.weight = weight
        self.logic_rules = logic_rules or []


class FakeResult:
    def __init__(self, label, min_score, max_score):
        self.label = label
        self.min_score = min_score
        self.max_score = max_score


def test_calculate_score_multiple_choice():
    q = FakeQuestion("q1", "multiple_choice", [{"value": "a", "score": 2}, {"value": "b", "score": 5}])
    score = scoring_service.calculate_score([q], {"q1": "b"})
    assert score == 5.0


def test_calculate_score_scale_applies_weight():
    q = FakeQuestion("q1", "scale", [], weight=2.0)
    score = scoring_service.calculate_score([q], {"q1": 3})
    assert score == 6.0


def test_calculate_score_ignores_missing_answer():
    q = FakeQuestion("q1", "multiple_choice", [{"value": "a", "score": 2}])
    score = scoring_service.calculate_score([q], {})
    assert score == 0.0


def test_resolve_result_label_within_range():
    results = [FakeResult("bajo", 0, 5), FakeResult("alto", 5.01, 10)]
    result = scoring_service.resolve_result_label(results, 7)
    assert result.label == "alto"


def test_resolve_result_label_no_match():
    results = [FakeResult("bajo", 0, 5)]
    result = scoring_service.resolve_result_label(results, 99)
    assert result is None


def test_next_question_id_skip_logic():
    q = FakeQuestion("q1", "yes_no", [], logic_rules=[
        {"if_value": "no", "action": "skip_to", "target_question_id": "q3"}
    ])
    target = scoring_service.next_question_id(q, "no")
    assert target == "q3"
