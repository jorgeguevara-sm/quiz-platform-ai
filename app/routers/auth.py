from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/magic-link")
def request_magic_link(payload: schemas.MagicLinkRequest, db: Session = Depends(get_db)):
    token = auth_service.create_magic_link_token(db, payload.email)
    magic_url = f"/auth/verify?token={token}"
    return {"message": "Magic link generado", "dev_magic_url": magic_url}


@router.post("/verify")
def verify_magic_link(payload: schemas.MagicLinkVerify, db: Session = Depends(get_db)):
    email = auth_service.verify_magic_link_token(db, payload.token)
    if not email:
        raise HTTPException(status_code=400, detail="Token invalido o expirado")

    user = db.query(models.User).filter_by(email=email).first()
    if not user:
        user = models.User(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)

    jwt_token = auth_service.create_jwt_for_user(user.id)
    return {"access_token": jwt_token, "user": schemas.UserOut.model_validate(user)}


def get_current_user(token: str, db: Session = Depends(get_db)) -> models.User:
    user_id = auth_service.decode_jwt(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="No autenticado")
    user = db.query(models.User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user
