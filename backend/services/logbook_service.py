# backend/services/logbook_service.py

from datetime import datetime

class LogEntry:
    _entries = []
    _id_counter = 1

    def __init__(self, author, content):
        self.id = LogEntry._id_counter
        LogEntry._id_counter += 1
        self.author = author
        self.content = content
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "timestamp": self.timestamp
        }

class LogbookService:
    @staticmethod
    def get_logs():
        # Return newest first
        return [entry.to_dict() for entry in reversed(LogEntry._entries)]

    @staticmethod
    def create_log(author, content):
        entry = LogEntry(author, content)
        LogEntry._entries.append(entry)
        return entry.to_dict()

    @staticmethod
    def get_log(log_id):
        for entry in LogEntry._entries:
            if entry.id == log_id:
                return entry.to_dict()
        return None

    @staticmethod
    def update_log(log_id, author=None, content=None):
        for entry in LogEntry._entries:
            if entry.id == log_id:
                if author is not None:
                    entry.author = author
                if content is not None:
                    entry.content = content
                return entry.to_dict()
        return None

    @staticmethod
    def delete_log(log_id):
        for i, entry in enumerate(LogEntry._entries):
            if entry.id == log_id:
                LogEntry._entries.pop(i)
                return True
        return False
