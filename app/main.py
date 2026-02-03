from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import middleware CORS
from fastapi_pagination import add_pagination
from app.routers import user_router as users, auth_router, role_router, permission_router, role_permission_router
from app.core.config import settings # Asumsi kamu menyimpan daftar origin di config

app = FastAPI(title="RBAC FastAPI")

# --- Konfigurasi CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register Router ---
app.include_router(users.router)
app.include_router(auth_router.router)
app.include_router(role_router.router)
app.include_router(permission_router.router)
app.include_router(role_permission_router.router)

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Welcome to RBAC FastAPI"}

add_pagination(app)