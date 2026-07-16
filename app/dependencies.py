from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal
from .security import decode_access_token

# Skema OAuth2 untuk menerima token JWT pada endpoint yang membutuhkan autentikasi.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    # Membuat sesi database baru untuk setiap request dan menutupnya setelah selesai.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    # Jika token tidak valid atau user tidak ditemukan, kembalikan error unauthorized.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id_user == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user
