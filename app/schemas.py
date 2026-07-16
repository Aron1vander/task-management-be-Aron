from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- User ----------
# Schema untuk data user yang diterima atau dikembalikan oleh API.
class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserOut(UserBase):
    id_user: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------- Task ----------
# Schema untuk input dan output task yang dipakai di endpoint task.
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "Todo"
    deadline: Optional[datetime] = None
    assignee_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None
    assignee_id: Optional[int] = None


class TaskOut(TaskBase):
    id_task: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    assignee: Optional[UserOut] = None

    model_config = ConfigDict(from_attributes=True)


# ---------- Auth ----------
# Schema untuk response token saat login berhasil.
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
