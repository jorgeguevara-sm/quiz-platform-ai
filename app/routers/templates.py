import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.templates_data.industry_templates import TEMPLATES
from app.routers.tests import get_current_user_from_header, _check_free_plan_limit

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get("/")
def list_templates():
    return [{"key": k, "title": v["title"], "industry": v["industry"]} for k, v in TEMPLATES.items()]


@router.post("/{template_key}/use", response_model=schemas.TestOut)
def use_template(
    template_key: str,
    user: models.User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db),
):
    _check_free_plan_limit(user, db)
    template = TEMPLATES.get(template_key)
    if not template:
        raise HTTPException(status_code=404, detail="Template no encontrado")
    test = models.Test(
        user_id=user.id, title=template["title"], industry=template["industry"],
        language=template["language"], branding={"primary_color": "#2563eb"},
        status="draft", slug=str(uuid.uuid4())[:8],
    )
    db.add(test)
    db.flush()
    for idx, q in enumerate(template["questions"]):
        db.add(models.Question(test_id=test.id, type=q["type"], text=q["text"],
            options=q["options"], order=idx, weight=q["weight"]))
    for r in template["results"]:
        db.add(models.ResultTemplate(test_id=test.id, label=r["label"],
            min_score=r["min_score"], max_score=r["max_score"],
            message=r["message"], cta_text=r.get("cta_text")))
    db.commit()
    db.refresh(test)
    return test
