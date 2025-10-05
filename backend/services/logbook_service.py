# backend/space_vitals/services/logbook_service.py

from sqlalchemy.orm import Session
from app.models.logbook import LogEntry


def create_log(db: Session, title: str, content: str, author: str) -> LogEntry:
    """
    Create a new log entry and persist it to the database.
    """
    log = LogEntry(title=title, content=content, author=author)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_logs(db: Session, skip: int = 0, limit: int = 50):
    """
    Retrieve a paginated list of logs, newest first.
    """
    return (
        db.query(LogEntry)
        .order_by(LogEntry.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_log(db: Session, log_id: int):
    """
    Retrieve a single log entry by ID.
    """
    return db.query(LogEntry).filter(LogEntry.id == log_id).first()


def update_log(db: Session, log_id: int, **fields):
    """
    Update fields of a log entry if it exists.
    Returns the updated log or None if not found.
    """
    log = get_log(db, log_id)
    if not log:
        return None

    for key, value in fields.items():
        if value is not None and hasattr(log, key):
            setattr(log, key, value)

    db.commit()
    db.refresh(log)
    return log


def delete_log(db: Session, log_id: int) -> bool:
    """
    Delete a log entry by ID.
    Returns True if deleted, False if not found.
    """
    log = get_log(db, log_id)
    if not log:
        return False

    db.delete(log)
    db.commit()
    return True
