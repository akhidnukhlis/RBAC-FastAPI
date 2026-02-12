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

Project ini menggunakan **uv** untuk manajemen dependensi yang modern dan sangat cepat.

### 🖥️ Pengguna Windows (WSL)

Untuk pengguna Windows, project ini **sangat disarankan** untuk dijalankan di lingkungan **WSL2 (Windows Subsystem for Linux)**. Hal ini untuk memastikan skrip otomatisasi (seperti `Makefile`) dan toolchain `uv` berjalan dengan optimal selayaknya di sistem Unix/Linux.

1.  **Install WSL**: Buka PowerShell (Admin) dan jalankan `wsl --install`.
2.  **Environment**: Lakukan seluruh proses instalasi di bawah ini di dalam terminal WSL (Ubuntu/Debian).
3.  **Tips:** Gunakan extension **"WSL"** di VS Code untuk membuka folder project ini (`code .`) langsung dari terminal WSL.

---

1.  **Clone Repository:**
    ```bash
    git clone https://github.com/akhidnukhlis/RBAC-FastAPI.git
    cd RBAC-FastAPI
    ```

2.  **Install Dependencies:**
    ```bash
    uv sync
    ```

3.  **Setup Environment:**
    Salin file `.env.example` ke `.env` dan sesuaikan kredensial database Anda.
    ```bash
    cp .env.example .env
    ```

    **Konfigurasi Database (.env):**
    Pastikan Anda mengatur variabel berikut agar aplikasi dapat terhubung ke PostgreSQL:
    
    | Variable | Deskripsi | Contoh |
    | :--- | :--- | :--- |
    | `POSTGRES_HOST` | Host/IP Database | `localhost` |
    | `POSTGRES_USER` | Username Database | `postgres` |
    | `POSTGRES_PASSWORD` | Password Database | `password` |
    | `POSTGRES_DB` | Nama Database | `boilerplate_db` |
    | `POSTGRES_PORT` | Port Database | `5432` |

4.  **Jalankan Database Migration & Seeder:**
    Perintah ini akan membuat semua tabel dan mengisi data awal (Role, Permission, Status, Superadmin).
    ```bash
    uv run alembic upgrade head
    ```

---

## 🏃 Menjalankan Aplikasi

Jalankan server development dengan hot-reload:

```bash
uv run uvicorn app.main:app --reload
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

### Menggunakan Makefile (Shortcut)
Agar lebih efisien, Anda dapat menggunakan perintah berikut alih-alih mengetik panjang di terminal:

| Perintah | Fungsi | Ekuivalen dengan |
| :--- | :--- | :--- |
| `make install` | Install dependencies | `uv sync` |
| `make dev` | Jalankan server (dev) | `uv run uvicorn app.main:app --reload` |
| `make migrate` | Jalankan migrasi DB | `uv run alembic upgrade head` |
| `make migration msg="pesan"` | Buat migrasi baru | `uv run alembic revision ...` |
| `make clean` | Bersihkan cache | `find . -name "__pycache__" ...` |

Contoh penggunaan:
```bash
make dev
make migration msg="tambah tabel produk"
```

### Membuat Tabel/Fitur Baru (Manual):
1.  Buat Model di `app/models/`.
2.  Jangan lupa import model baru di `migrations/env.py`.
3.  Jalankan perintah generate migration:
    ```bash
    uv run alembic revision --autogenerate -m "nama_fitur_baru"
    ```
4.  Apply ke database:
    ```bash
    uv run alembic upgrade head
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
