import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Memuat variabel environment dari file .env agar konfigurasi database tidak hardcode.
load_dotenv()

# URL koneksi ke PostgreSQL. Jika tidak ada di environment, gunakan nilai default.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/task_management_db",
)

# Membuat engine SQLAlchemy yang digunakan untuk terhubung ke database.
engine = create_engine(DATABASE_URL)

# Session factory untuk membuat sesi database setiap kali ada request/operasi.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class untuk semua model ORM yang akan dipetakan ke tabel database.
Base = declarative_base()
