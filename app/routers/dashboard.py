import csv
import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.routers.tests import get_current_user_from_header

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/tests/{test_id}/responses")
def list_responses(test_id: str, user: models.User = Depends(get_current_user_from_header), db: Session = Depends(get_db)):
    test = db.query(models.Test).filter_by(id=test_id, user_id=user.id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    return test.responses


@router.get("/tests/{test_id}/analytics")
def get_analytics(test_id: str, user: models.User = Depends(get_current_user_from_header), db: Session = Depends(get_db)):
    test = db.query(models.Test).filter_by(id=test_id, user_id=user.id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    responses = test.responses
    total = len(responses)
    completed = sum(1 for r in responses if r.completed)
    completion_rate = (completed / total * 100) if total else 0
    result_counts: dict[str, int] = {}
    for r in responses:
        if r.result_label:
            result_counts[r.result_label] = result_counts.get(r.result_label, 0) + 1
    return {
        "total_responses": total,
        "completed_responses": completed,
        "completion_rate": round(completion_rate, 2),
        "result_distribution": result_counts,
    }


@router.get("/tests/{test_id}/export.csv")
def export_csv(test_id: str, user: models.User = Depends(get_current_user_from_header), db: Session = Depends(get_db)):
    test = db.query(models.Test).filter_by(id=test_id, user_id=user.id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["nombre", "email", "telefono", "score", "resultado", "completado", "fecha"])
    for r in test.responses:
        writer.writerow([r.respondent_name, r.respondent_email, r.respondent_phone,
                         r.total_score, r.result_label, r.completed, r.created_at])
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]), media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=responses_{test_id}.csv"},
    )
