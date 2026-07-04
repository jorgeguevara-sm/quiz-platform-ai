from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services import scoring_service

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/tests/{slug}", response_model=schemas.TestOut)
def get_public_test(slug: str, db: Session = Depends(get_db)):
    test = db.query(models.Test).filter_by(slug=slug, status="published").first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado o no publicado")
    return test


@router.post("/tests/{slug}/responses", response_model=schemas.ResponseOut)
def submit_response(slug: str, payload: schemas.ResponseSubmit, db: Session = Depends(get_db)):
    test = db.query(models.Test).filter_by(slug=slug, status="published").first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado o no publicado")
    score = scoring_service.calculate_score(test.questions, payload.answers)
    result = scoring_service.resolve_result_label(test.results, score)
    response = models.Response(
        test_id=test.id,
        respondent_name=payload.respondent_name,
        respondent_email=payload.respondent_email,
        respondent_phone=payload.respondent_phone,
        answers=payload.answers,
        total_score=score,
        result_label=result.label if result else None,
        completed=True,
    )
    db.add(response)
    db.commit()
    db.refresh(response)
    return response
