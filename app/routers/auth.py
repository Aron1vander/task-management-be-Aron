from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    # Mencari user berdasarkan email yang dikirim dari client.
    user = db.query(models.User).filter(models.User.email == payload.email).first()

    # Validasi password dengan hash yang tersimpan di database.
    if not user or not security.verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau password salah",
        )

    # Jika valid, buat token JWT yang berisi ID user sebagai subject.
    access_token = security.create_access_token(data={"sub": str(user.id_user)})
    return {"access_token": access_token, "token_type": "bearer"}
