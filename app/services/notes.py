from sqlalchemy.orm import Session
from app.repositories.notes import create_note
from app.schemas.notes import NoteCreate

def create_new_note(db: Session, note: NoteCreate, tenant: str):
    db.execute(f"SET search_path TO {tenant}")
    return create_note(db, note)
