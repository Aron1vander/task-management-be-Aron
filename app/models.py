from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    # Model tabel user yang menyimpan identitas akun pengguna.
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(250), unique=True, nullable=False, index=True)
    password = Column(String(250), nullable=False)  # disimpan dalam bentuk hash, bukan plaintext
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi ke task yang diasigned ke user ini.
    tasks = relationship("Task", back_populates="assignee")


class Task(Base):
    # Model tabel task yang menyimpan data pekerjaan dan tugas.
    __tablename__ = "tasks"

    id_task = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="Todo")  # Todo, In Progress, Done
    deadline = Column(DateTime(timezone=True), nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id_user"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relasi ke user yang menjadi assignee task ini.
    assignee = relationship("User", back_populates="tasks")
