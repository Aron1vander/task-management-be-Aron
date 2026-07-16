from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..dependencies import get_current_user, get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[schemas.TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Mengambil seluruh task dari database untuk ditampilkan ke client.
    return db.query(models.Task).all()


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Mencari satu task berdasarkan ID. Jika tidak ada, kirim error 404.
    task = db.query(models.Task).filter(models.Task.id_task == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task tidak ditemukan")
    return task


@router.post("/", response_model=schemas.TaskOut, status_code=201)
def create_task(
    payload: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Membuat object Task dari data input yang diterima dari request.
    task = models.Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    payload: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Mencari task yang ingin diubah, lalu update field yang dikirim client.
    task = db.query(models.Task).filter(models.Task.id_task == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task tidak ditemukan")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Menghapus task dari database jika data ditemukan.
    task = db.query(models.Task).filter(models.Task.id_task == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task tidak ditemukan")

    db.delete(task)
    db.commit()
    return
