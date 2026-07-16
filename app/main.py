from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth, tasks, users

# Auto-create tabel di database kalau belum ada (cukup untuk technical test;
# untuk project production sebaiknya pakai Alembic migration).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="API untuk aplikasi Simple Task Management (technical test)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only, batasi origin saat production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Task Management API is running. Buka /docs untuk dokumentasi Swagger."}
