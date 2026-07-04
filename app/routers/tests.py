import uuid
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services import llm_service, auth_service

router = APIRouter(prefix="/tests", tags=["tests"])


def get_current_user_from_header(authorization: str = Header(...), db: Session = Depends(get_db)) -> models.User:
    token = authorization.replace("Bearer ", "")
    user_id = auth_service.decode_jwt(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="No autenticado")
    user = db.query(models.User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


def _check_free_plan_limit(user: models.User, db: Session):
    if user.plan == "free":
        count = db.query(models.Test).filter_by(user_id=user.id).count()
        if count >= 1:
            raise HTTPException(
                status_code=402,
                detail="Plan gratuito limitado a 1 test. Actualiza tu plan para crear mas.",
            )


@router.post("/generate", response_model=schemas.TestOut)
def generate_test(
    payload: schemas.OnboardingInput,
    user: models.User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db),
):
    _check_free_plan_limit(user, db)
    generated = llm_service.generate_test(payload)
    test = models.Test(
        user_id=user.id,
        title=generated.title,
        industry=generated.industry,
        original_prompt=payload.business_description,
        language=generated.language,
        branding={"business_name": payload.professional_name, "primary_color": "#2563eb"},
        status="draft",
        slug=str(uuid.uuid4())[:8],
    )
    db.add(test)
    db.flush()
    for idx, q in enumerate(generated.questions):
        db.add(models.Question(
            test_id=test.id, type=q.type, text=q.text,
            options=[o.model_dump() for o in q.options], order=idx, weight=q.weight,
        ))
    for r in generated.results:
        db.add(models.ResultTemplate(
            test_id=test.id, label=r.label, min_score=r.min_score,
            max_score=r.max_score, message=r.message, cta_text=r.cta_text,
        ))
    db.commit()
    db.refresh(test)
    return test


@router.get("/", response_model=list[schemas.TestOut])
def list_tests(user: models.User = Depends(get_current_user_from_header), db: Session = Depends(get_db)):
    return db.query(models.Test).filter_by(user_id=user.id).order_by(models.Test.created_at.desc()).all()


@router.get("/{test_id}", response_model=schemas.TestOut)
def get_test(test_id: str, user: models.User = Depends(get_current_user_from_header), db: Session = Depends(get_db)):
    test = db.query(models.Test).filter_by(id=test_id, user_id=user.id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    return test


@router.patch("/{test_id}", response_model=schemas.TestOut)
def update_test(
    test_id: str, payload: schemas.TestUpdate,
    user: models.User = Depends(get_current_user_from_header), db: Session = Depends(get_db),
):
    test = db.query(models.Test).filter_by(id=test_id, user_id=user.id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    if payload.title is not None: test.title = payload.title
    if payload.branding is not None: test.branding = payload.branding.model_dump()
    if payload.status is not None: test.status = payload.status
    db.commit()
    db.refresh(test)
    return test


@router.patch("/{test_id}/questions/{question_id}", response_model=schemas.QuestionOut)
def update_question(
    test_id: str, question_id: str, payload: schemas.QuestionUpdate,
    user: models.User = Depends(get_current_user_from_header), db: Session = Depends(get_db),
):
    test = db.query(models.Test).filter_by(id=test_id, user_id=user.id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    question = db.query(models.Question).filter_by(id=question_id, test_id=test_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(question, field, value)
    db.commit()
    db.refresh(question)
    return question


@router.delete("/{test_id}")
def delete_test(test_id: str, user: models.User = Depends(get_current_user_from_header), db: Session = Depends(get_db)):
    test = db.query(models.Test).filter_by(id=test_id, user_id=user.id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    db.delete(test)
    db.commit()
    return {"message": "Test eliminado"}
