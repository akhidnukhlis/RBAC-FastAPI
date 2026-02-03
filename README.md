# RBAC - FastAPI

Starter kit API berbasis **FastAPI** dengan arsitektur **Clean Architecture (Repository-Service Pattern)**. Dilengkapi dengan sistem **RBAC (Role-Based Access Control)** yang komprehensif, Authentication (JWT), dan Database yang terkelola via Alembic.

---

## 📂 Struktur Direktori

```text
RBAC-FastAPI/
│
├── app/                        # Main Application Code
│   ├── core/                   # Core Configurations (DB, Security, Args)
│   ├── middleware/             # Middleware (Auth, Permissions)
│   ├── models/                 # SQLAlchemy Models (Database Structure)
│   ├── repositories/           # Data Access Layer (CRUD)
│   ├── routers/                # API Endpoints (Controllers)
│   ├── schemas/                # Pydantic Models (Validation/Serialization)
│   ├── services/               # Business Logic Layer
│   └── main.py                 # App Entry Point & Router Registration
│
├── migrations/                 # Alembic Migrations Directory
│   ├── versions/               # Migration Scripts (Versions)
│   └── env.py                  # Alembic Environment Context
│
├── .env.example                # Template Environment Variables
├── alembic.ini                 # Alembic Configuration
├── pyproject.toml              # Project & Dependency Definitions
└── README.md                   # Documentation
```

---

## 🔥 Fitur Utama

- **Fast & Async**: Dibangun di atas FastAPI + Uvicorn.
- **Architectural Pattern**: Menggunakan Repository -> Service -> Router pattern untuk pemisahan concern yang bersih.
- **Authentication**: JWT-based Auth dengan Hashed Password (Bcrypt).
- **Advanced RBAC**: Role-Based User Management dengan Dynamic Role-Permission assignments.
- **Workflow Approval**: Sistem status user (Pending, Admin Approval, Active, dsb).
- **Database Migrations**: Full database version control dengan Alembic.
- **Initial Seeder**: Dilengkapi seeder otomatis untuk Role, Permission, Status, dan Superadmin.

---

## 🚀 Instalasi & Setup

Project ini menggunakan **Poetry** untuk manajemen dependensi.

1.  **Clone Repository:**
    ```bash
    git clone https://github.com/akhidnukhlis/RBAC-FastAPI.git
    cd RBAC-FastAPI
    ```

2.  **Install Dependencies:**
    ```bash
    poetry install
    ```

3.  **Setup Environment:**
    Salin file `.env.example` ke `.env` dan sesuaikan kredensial database Anda.
    ```bash
    cp .env.example .env
    ```

4.  **Jalankan Database Migration & Seeder:**
    Perintah ini akan membuat semua tabel dan mengisi data awal (Role, Permission, Status, Superadmin).
    ```bash
    poetry run alembic upgrade head
    ```

---

## 🏃 Menjalankan Aplikasi

Jalankan server development dengan hot-reload:

```bash
poetry run uvicorn app.main:app --reload
```

Akses dokumentasi interaktif API (Swagger UI):
👉 **http://localhost:8000/docs**

---

## 🛡️ Default Superadmin Credentials

Setelah menjalankan migration, gunakan akun ini untuk login pertama kali:

- **Email**: `superadmin@rbac.com`
- **Password**: `your-super-password`

*⚠️ **Penting:** Segera ganti password ini setelah login pertama kali di environment produksi.*

---

## 🛠️ Pengembangan (Development Guide)

### Membuat Tabel/Fitur Baru:
1.  Buat Model di `app/models/`.
2.  Jangan lupa import model baru di `migrations/env.py`.
3.  Jalankan perintah generate migration:
    ```bash
    poetry run alembic revision --autogenerate -m "nama_fitur_baru"
    ```
4.  Apply ke database:
    ```bash
    poetry run alembic upgrade head
    ```

### Fitur RBAC (Permission):
Untuk melindungi endpoint API dengan Permission tertentu:

```python
@router.post("/items", dependencies=[Depends(PermissionMiddleware(PERM_ID))])
def create_item():
    pass
```
*Ganti `PERM_ID` dengan ID permission yang sesuai dari tabel `permissions`.*

---
