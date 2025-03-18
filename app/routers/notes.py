from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.notes import NoteCreate, Note
from app.services.notes import create_new_note
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import AuthMiddleware

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(7))], response_model=Note)
def create_note(request: Request, note: NoteCreate, db: Session = Depends(get_db)):
    tenant = request.headers.get("X-Tenant")
    if tenant:
        db.execute(f"SET search_path TO {tenant}")

    return create_new_note(db, note, tenant)
