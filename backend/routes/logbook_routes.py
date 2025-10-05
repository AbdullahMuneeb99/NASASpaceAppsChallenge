from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.database import get_db
from app.services import logbook_service
router = APIRouter(prefix="/logbook", tags=["Logbook"])
class LogEntryCreate(BaseModel):
    title: str = Field(..., max_length=100); content: str; author: str = Field(..., max_length=50)
class LogEntryUpdate(BaseModel):
    title: str | None = Field(None, max_length=100); content: str | None = None; author: str | None = Field(None, max_length=50)
@router.post("/", status_code=201)
def add_log(entry: LogEntryCreate, db: Session = Depends(get_db)): return logbook_service.create_log(db, entry.title, entry.content, entry.author)
@router.get("/") 
def list_logs(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)): return logbook_service.get_logs(db, skip, limit)
@router.get("/{log_id}")
def get_log(log_id: int, db: Session = Depends(get_db)):
    log = logbook_service.get_log(db, log_id)
    if not log: raise HTTPException(404, "Log not found")
    return log
@router.patch("/{log_id}")
def update_log(log_id: int, payload: LogEntryUpdate, db: Session = Depends(get_db)):
    out = logbook_service.update_log(db, log_id, **payload.model_dump(exclude_unset=True))
    if not out: raise HTTPException(404, "Log not found")
    return out
@router.delete("/{log_id}", status_code=204)
def delete_log(log_id: int, db: Session = Depends(get_db)):
    ok = logbook_service.delete_log(db, log_id)
    if not ok: raise HTTPException(404, "Log not found")
    return None
