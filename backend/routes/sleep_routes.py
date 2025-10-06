from datetime import datetime, timedelta
from flask import Flask, request, jsonify, abort
import json

app = Flask(__name__)

sleep_data = []

def _mins(t):
    """Turn HH:MM into total minutes since midnight."""
    h, m = map(int, t.split(":"))
    return h * 60 + m

def _dur(bed, wake):
    """Find sleep length in hours between bed and wake times."""
    try:
        b, w = _mins(bed), _mins(wake)
    except Exception:
        return None
    if w < b:
        w += 24 * 60
    return round((w - b) / 60, 2)

def add_log(bed, wake):
    """Add a new sleep entry and return the hours slept."""
    d = _dur(bed, wake)
    if d is None:
        return {"ok": False, "error": "Use HH:MM format"}
    rec = {"bed": bed, "wake": wake, "hours": d}
    sleep_data.append(rec)
    return {"ok": True, "hours": d}

def get_recent(n=5):
    """Get the last n sleep logs (most recent first)."""
    return sleep_data[-n:][::-1]

def get_average(k=7):
    """Get average sleep hours for last k logs."""
    rows = sleep_data[-k:]
    if not rows:
        return None
    return round(sum(r["hours"] for r in rows) / len(rows), 2)

def plan_alarm(minutes):
    """Return time info for an alarm after X minutes."""
    try:
        minutes = int(minutes)
    except Exception:
        minutes = 0
    t = datetime.now() + timedelta(minutes=minutes)
    return {"target_hms": t.strftime("%H:%M:%S"), "target_iso": t.isoformat()}

@app.post("/sleep/add")
def sleep_add():
    """POST /sleep/add → save a sleep record."""
    body = request.get_json(silent=True) or {}
    return jsonify(add_log(body.get("bed"), body.get("wake")))

@app.get("/sleep/recent")
def sleep_recent():
    """GET /sleep/recent?n=5 → show recent logs."""
    try:
        n = int(request.args.get("n", 5))
    except Exception:
        n = 5
    return jsonify({"items": get_recent(n)})

@app.get("/sleep/average")
def sleep_average():
    """GET /sleep/average?k=7 → show average sleep hours."""
    try:
        k = int(request.args.get("k", 7))
    except Exception:
        k = 7
    return jsonify({"average": get_average(k)})

@app.post("/alarm/plan")
def alarm_plan():
    """POST /alarm/plan → plan an alarm time."""
    body = request.get_json(silent=True) or {}
    return jsonify(plan_alarm(body.get("minutes", 0)))

if __name__ == "__main__":
    app.run(debug=True)





