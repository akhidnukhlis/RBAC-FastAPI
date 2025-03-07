# FastAPI Project

## Struktur Directory
```
seaside-sentinel/
│-- app/        
│   │-- core/
│   │   │-- __init__.py
│   │   │-- database.py     
│   │   │-- config.py
│   │-- middleware/
│   │   │-- __init__.py
│   │   │-- auth_middleware.py     
│   │   │-- permission_middleware.py
│   │-- models/             
│   │   │-- __init__.py
│   │   │-- user.py         
│   │   │-- role.py         
│   │-- repositories/       
│   │   │-- __init__.py
│   │   │-- user.py         
│   │   │-- role.py         
│   │-- routers/            
│   │   │-- __init__.py
│   │   │-- user.py         
│   │   │-- auth.py         
│   │-- schemas/            
│   │   │-- __init__.py
│   │   │-- user.py         
│   │   │-- role.py         
│   │-- services/           
│   │   │-- __init__.py
│   │   │-- user.py         
│   │   │-- role.py         
│   │-- utilities/          
│   │   │-- __init__.py
│   │   │-- utils.py     
│   │-- main.py             # Entry point FastAPI
│-- migrations/             # Folder migrasi Alembic
│-- env/                    # Virtual Environment
│-- .env                    # File konfigurasi environment
│-- requirements.txt        # Dependency project
│-- alembic.ini             # Konfigurasi Alembic
│-- README.md               # Dokumentasi proyek
```

---

## **1. Instalasi & Setup Virtual Environment**
Jalankan perintah berikut untuk menginstal dependensi yang diperlukan:
```sh
# Buat virtual environment
python -m venv env

# Aktifkan virtual environment
# Windows
env\Scripts\activate
# Mac/Linux
source env/bin/activate

# Instal dependensi
pip install -r requirements.txt
```

---

## **2. Konfigurasi Database**
Buat file `.env` di root proyek dan tambahkan konfigurasi database PostgreSQL:
```ini
DATABASE_URL=postgresql://username:password@localhost:5432/nama_database
```
Sesuaikan `username`, `password`, dan `nama_database` sesuai dengan setup PostgreSQL-mu.

Pastikan file `app/core/database.py` memiliki koneksi ke database:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

---

## **3. Inisialisasi & Migrasi Database dengan Alembic**

### **3.1 Inisialisasi Alembic**
Jalankan perintah berikut untuk menginisialisasi Alembic (jika belum ada folder `migrations/`):
```sh
alembic init migrations
```

### **3.2 Konfigurasi Alembic (`migrations/env.py`)**
Edit `migrations/env.py` dan tambahkan:
```python
from app.core.database import Base

target_metadata = Base.metadata
```

### **3.3 Buat Migration Baru**
Jalankan perintah berikut untuk mendeteksi perubahan pada model database:
```sh
alembic revision --autogenerate -m "Initial migration"
```
Jika berhasil, Alembic akan membuat file di dalam folder `migrations/versions/`.

### **3.4 Terapkan Migrasi ke Database**
Jalankan perintah berikut untuk menerapkan perubahan ke database:
```sh
alembic upgrade head
```

---

## **4. Menjalankan Aplikasi**
Jalankan FastAPI dengan perintah berikut:
```sh
uvicorn app.main:app --reload
```
atau menggunakan custom port:
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```
Akses API melalui `http://127.0.0.1:8000/docs` untuk melihat dokumentasi Swagger.

---

## **5. Endpoint Utama**
Berikut adalah beberapa endpoint yang tersedia:
- **`POST /auth/register`** → Registrasi user
- **`POST /auth/login`** → Login user
- **`GET /users/`** → List user
- **`POST /users/`** → Tambah user baru
- **`PUT /users/{id}`** → Update user
- **`DELETE /users/{id}`** → Hapus user
- **`GET /roles/`** → List role
- **`POST /roles/`** → Tambah role baru

---

## **6. Menambahkan Model Baru dan Migrasi Ulang**
Jika ada perubahan pada model database (misalnya menambah kolom baru), jalankan:
```sh
alembic revision --autogenerate -m "Update model"
alembic upgrade head
```

---

## **7. Menjalankan Database Query Secara Manual**
Gunakan perintah berikut untuk membuka sesi interaktif dengan database:
```sh
python
>>> from app.core.database import SessionLocal
>>> db = SessionLocal()
>>> from app.models.user import User
>>> users = db.query(User).all()
>>> print(users)
```

---

## **8. Testing API dengan cURL**
Coba daftar user baru menggunakan cURL:
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/register' \
  -H 'Content-Type: application/json' \
  -d '{"username": "testuser", "password": "password123"}'
```

Jika berhasil, API akan merespons dengan data user yang baru dibuat.

---

## **9. Deployment (Optional)**
Jika ingin deploy ke server, gunakan **Gunicorn**:
```sh
pip install gunicorn
```
Jalankan server menggunakan perintah:
```sh
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

---

## **10. Kesimpulan**
Dokumentasi ini mencakup:
✅ Struktur directory proyek FastAPI 📂  
✅ Instalasi & setup virtual environment 🛠️  
✅ Konfigurasi database PostgreSQL 🗄️  
✅ Migrasi database dengan Alembic 🔄  
✅ Menjalankan API dengan Uvicorn 🚀  
✅ Endpoint utama yang tersedia 📡  
✅ Testing API menggunakan cURL 🧪  

Semoga bermanfaat! 🚀

