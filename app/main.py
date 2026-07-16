from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth, tasks, users

# Membuat tabel-tabel database otomatis saat aplikasi dijalankan.
# Ini cocok untuk keperluan technical test, tetapi untuk production biasanya dipakai migrasi seperti Alembic.
Base.metadata.create_all(bind=engine)

# Membuat instance aplikasi FastAPI sebagai pusat routing dan handler request.
app = FastAPI(
    title="Task Management API",
    description="API untuk aplikasi Simple Task Management (technical test)",
    version="1.0.0",
)

# Mengizinkan cross-origin request dari berbagai frontend selama development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hanya untuk development, sebaiknya dibatasi di production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Menggabungkan router-auth, router-users, dan router-tasks ke aplikasi utama.
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)


# Endpoint sederhana untuk memastikan API berjalan.
@app.get("/", tags=["Root"])
def root():
    return {"message": "Task Management API is running. Buka /docs untuk dokumentasi Swagger."}
