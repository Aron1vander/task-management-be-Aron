# Task Management API (Backend)

Backend untuk Simple Task Management App. Dibuat dengan **FastAPI** + **PostgreSQL**, autentikasi **JWT**.

## Struktur Project

```
task-management-backend/
├── app/
│   ├── main.py           # entry point FastAPI
│   ├── database.py       # koneksi PostgreSQL (SQLAlchemy)
│   ├── models.py         # model tabel: User, Task
│   ├── schemas.py        # schema Pydantic (request/response)
│   ├── security.py       # hashing password & JWT
│   ├── dependencies.py   # get_db, get_current_user
│   └── routers/
│       ├── auth.py       # POST /auth/login
│       ├── users.py      # GET /users
│       └── tasks.py      # CRUD /tasks
├── seed.py               # seed dummy user
├── requirements.txt
└── .env.example
```

## 1. Setup

```bash
cd task-management-backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Buat database di pgAdmin

Buka pgAdmin → klik kanan **Databases** → **Create** → **Database** → beri nama `task_management_db`.

## 3. Konfigurasi environment

```bash
cp .env.example .env
```

Edit `.env`, sesuaikan `password_kamu` dengan password PostgreSQL kamu:

```
DATABASE_URL=postgresql://postgres:password_kamu@localhost:5432/task_management_db
SECRET_KEY=isi-dengan-string-acak-panjang
```

## 4. Seed dummy user (untuk login & dropdown assignee)

```bash
python seed.py
```

Ini akan bikin 3 user, semua dengan password `password123`:
- aron@example.com
- budi@example.com
- citra@example.com

## 5. Jalankan server

```bash
uvicorn app.main:app --reload
```

Server jalan di `http://localhost:8000`. Tabel `users` dan `tasks` otomatis dibuat saat pertama kali dijalankan.

## 6. Cek dokumentasi API otomatis

Buka `http://localhost:8000/docs` (Swagger UI) — ini juga bisa dipakai untuk testing manual sebelum bikin Postman collection.

## Endpoint yang tersedia

| Method | Endpoint       | Auth | Keterangan                    |
|--------|----------------|------|--------------------------------|
| POST   | /auth/login    | -    | Login, return JWT token       |
| GET    | /users         | JWT  | Daftar user (untuk assignee)  |
| GET    | /tasks         | JWT  | Daftar semua task             |
| GET    | /tasks/{id}    | JWT  | Detail satu task              |
| POST   | /tasks         | JWT  | Buat task baru                |
| PUT    | /tasks/{id}    | JWT  | Update task                   |
| DELETE | /tasks/{id}    | JWT  | Hapus task                    |

Untuk endpoint yang butuh JWT, kirim header:
```
Authorization: Bearer <access_token>
```
