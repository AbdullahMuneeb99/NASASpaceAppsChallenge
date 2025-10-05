from sqlalchemy.orm import Session
from app.models.logbook import LogEntry
def create_log(db: Session, title: str, content: str, author: str) -> LogEntry:
    log = LogEntry(title=title, content=content, author=author); db.add(log); db.commit(); db.refresh(log); return log
def get_logs(db: Session, skip: int = 0, limit: int = 50): return db.query(LogEntry).order_by(LogEntry.created_at.desc()).offset(skip).limit(limit).all()
def get_log(db: Session, log_id: int): return db.query(LogEntry).filter(LogEntry.id==log_id).first()
def update_log(db: Session, log_id: int, **fields):
    log = get_log(db, log_id); 
    if not log: return None
    for k,v in fields.items():
        if v is not None and hasattr(log,k): setattr(log,k,v)
    db.commit(); db.refresh(log); return log
def delete_log(db: Session, log_id: int) -> bool:
    log = get_log(db, log_id); 
    if not log: return False
    db.delete(log); db.commit(); return True
