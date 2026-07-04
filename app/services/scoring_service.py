"""
Motor de puntuacion y evaluacion de logica condicional.
Reglas de negocio separadas de los routers (arquitectura por capas).
"""
from typing import Dict, Any, List
from app import models


def calculate_score(questions: List[models.Question], answers: Dict[str, Any]) -> float:
    total = 0.0
    for q in questions:
        answer_value = answers.get(q.id)
        if answer_value is None:
            continue
        if q.type in ("multiple_choice", "yes_no"):
            for opt in q.options or []:
                if opt.get("value") == answer_value:
                    total += opt.get("score", 0) * (q.weight or 1.0)
                    break
        elif q.type == "scale":
            try:
                total += float(answer_value) * (q.weight or 1.0)
            except (ValueError, TypeError):
                pass
    return total


def resolve_result_label(results: List[models.ResultTemplate], score: float) -> models.ResultTemplate | None:
    for r in results:
        if r.min_score <= score <= r.max_score:
            return r
    return None


def next_question_id(question: models.Question, answer_value: Any) -> str | None:
    for rule in question.logic_rules or []:
        if str(rule.get("if_value")) == str(answer_value):
            if rule.get("action") == "skip_to":
                return rule.get("target_question_id")
    return None
