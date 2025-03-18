from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlalchemy.orm import Session
from app.core.database import SessionLocal


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant = request.headers.get("X-Tenant")
        db: Session = SessionLocal()

        try:
            if tenant:
                db.execute(f"SET search_path TO {tenant}")
                db.commit()
            request.state.db = db
            response = await call_next(request)
        finally:
            db.close()

        return response