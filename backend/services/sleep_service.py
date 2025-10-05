from datetime import datetime, timedelta
sleep_data = []

def _mins(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m

def _dur(bed, wake):
    try:
        b, w = _mins(bed), _mins(wake)
    except:
        return None
    if w < b:
        w += 24 * 60
    return round((w - b) / 60, 2)

def add_log(bed_hhmm: str, wake_hhmm: str):
    """
    Add a new sleep record to memory.
    Returns: {"ok": True, "hours": float} or {"ok": False, "error": "..."}
    """
    d = _dur(bed_hhmm, wake_hhmm)
    if d is None:
        return {"ok": False, "error": "Use HH:MM (00-23:00-59)"}
    record = {"bed": bed_hhmm, "wake": wake_hhmm, "hours": d}
    sleep_data.append(record)
    return {"ok": True, "hours": d}

def get_recent(n: int = 5):
    """
    Returns the latest n records (newest first).
    """
    return sleep_data[-n:][::-1]

def get_average(k: int = 7):
    """
    Returns average hours of last k records, or None if no data.
    """
    rows = sleep_data[-k:]
    if not rows:
        return None
    hrs = [r["hours"] for r in rows]
    return round(sum(hrs) / len(hrs), 2)

def plan_alarm(minutes_from_now: int):
    """
    Returns target time (no waiting or sound).
    """
    target = datetime.now() + timedelta(minutes=int(minutes_from_now))
    return {
        "target_iso": target.isoformat(),
        "target_hms": target.strftime("%H:%M:%S")
    }
