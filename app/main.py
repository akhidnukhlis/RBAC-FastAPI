from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import middleware CORS
from fastapi_pagination import add_pagination
from app.routers import user_router as users, auth_router, role_router, permission_router, role_permission_router
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.exception_handlers import http_exception_handler, validation_exception_handler, database_exception_handler
from sqlalchemy.exc import OperationalError
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

# --- Global Exception Handlers ---
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(OperationalError, database_exception_handler)

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