"""
Jalankan sekali untuk mengisi database dengan beberapa user dummy,
supaya endpoint /users dan dropdown assignee di frontend ada datanya.

Cara jalankan:
    python seed.py
"""

from app.database import Base, SessionLocal, engine
from app import models
from app.security import get_password_hash

Base.metadata.create_all(bind=engine)

db = SessionLocal()

dummy_users = [
    {"name": "Aron", "email": "aron@example.com", "password": "password123"},
    {"name": "Budi Santoso", "email": "budi@example.com", "password": "password123"},
    {"name": "Citra Dewi", "email": "citra@example.com", "password": "password123"},
]

for u in dummy_users:
    existing = db.query(models.User).filter(models.User.email == u["email"]).first()
    if not existing:
        user = models.User(
            name=u["name"],
            email=u["email"],
            password=get_password_hash(u["password"]),
        )
        db.add(user)
        print(f"Ditambahkan: {u['email']}")
    else:
        print(f"Sudah ada, dilewati: {u['email']}")

db.commit()
db.close()
print("\nSeed selesai. Kamu bisa login pakai salah satu email di atas dengan password: password123")
