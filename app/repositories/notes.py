from sqlalchemy.orm import Session
from app.models.multi_tenancy import Note

def create_note(db: Session, note_data):
    db_note = Note(**note_data.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note