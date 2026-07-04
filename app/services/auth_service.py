"""
Autenticacion via magic link (sin passwords, sin OAuth social).
"""
import secrets
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
from app import models
from app.config import settings

MAGIC_LINK_EXPIRE_MINUTES = 15
JWT_EXPIRE_HOURS = 24 * 7


def create_magic_link_token(db: Session, email: str) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=MAGIC_LINK_EXPIRE_MINUTES)
    record = models.MagicLinkToken(email=email, token=token, expires_at=expires_at)
    db.add(record)
    db.commit()
    return token


def verify_magic_link_token(db: Session, token: str) -> str | None:
    record = db.query(models.MagicLinkToken).filter_by(token=token, used=False).first()
    if not record or record.expires_at < datetime.utcnow():
        return None
    record.used = True
    db.commit()
    return record.email


def create_jwt_for_user(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_jwt(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return payload.get("sub")
    except Exception:
        return None
