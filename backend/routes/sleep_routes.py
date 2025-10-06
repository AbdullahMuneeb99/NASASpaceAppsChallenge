# backend/routes/sleep_routes.py

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

sleep_bp = Blueprint("sleep", __name__, url_prefix="/sleep")

sleep_data = []


def _mins(t):
    """Convert HH:MM into total minutes since midnight."""
    h, m = map(int, t.split(":"))
    return h * 60 + m


def _dur(bed, wake):
    """Find sleep duration in hours between bed and wake times."""
    try:
        b, w = _mins(bed), _mins(wake)
    except Exception:
        return None
    if w < b:
        w += 24 * 60
    return round((w - b) / 60, 2)


@sleep_bp.route("/add", methods=["POST"])
def add_sleep_log():
    """Add a new sleep record."""
    data = request.get_json()
    bed, wake = data.get("bed"), data.get("wake")
    if not bed or not wake:
        return jsonify({"error": "Missing 'bed' or 'wake' time"}), 400

    duration = _dur(bed, wake)
    if duration is None:
        return jsonify({"error": "Invalid time format (use HH:MM)"}), 400

    record = {"bed": bed, "wake": wake, "hours": duration}
    sleep_data.append(record)
    return jsonify({"ok": True, "hours": duration}), 201


@sleep_bp.route("/recent", methods=["GET"])
def get_recent_logs():
    """Get recent sleep logs."""
    n = int(request.args.get("n", 5))
    return jsonify({"items": sleep_data[-n:][::-1]}), 200


@sleep_bp.route("/average", methods=["GET"])
def get_average_sleep():
    """Get average sleep duration."""
    k = int(request.args.get("k", 7))
    recent = sleep_data[-k:]
    if not recent:
        return jsonify({"average": None}), 200
    avg = round(sum(r["hours"] for r in recent) / len(recent), 2)
    return jsonify({"average": avg}), 200


@sleep_bp.route("/alarm", methods=["POST"])
def plan_alarm():
    """Plan an alarm X minutes from now."""
    data = request.get_json()
    minutes = int(data.get("minutes", 0))
    target_time = datetime.now() + timedelta(minutes=minutes)
    return jsonify({
        "target_hms": target_time.strftime("%H:%M:%S"),
        "target_iso": target_time.isoformat()
    }), 200


'''
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
sleep_data=[]
bp=Blueprint("sleep",__name__)

def _mins(t):
    """Turn HH:MM into total minutes since midnight."""
    h,m=map(int,t.split(":")); return h*60+m
    
def _dur(bed,wake):
    """Hours between bed and wake (wrap past midnight)."""
    try: b,w=_mins(bed),_mins(wake)
    except: return None
    if w<b: w+=24*60
    return round((w-b)/60,2)
    
def add_log(bed,wake):
    """Add a sleep entry and return result dict."""
    d=_dur(bed,wake)
    if d is None: return {"ok":False,"error":"Use HH:MM format"}
    rec={"bed":bed,"wake":wake,"hours":d}; sleep_data.append(rec); return {"ok":True,"hours":d}
    
def get_recent(n=5):
    """Return last n logs, newest first."""
    return sleep_data[-n:][::-1]
    
def get_average(k=7):
    """Average sleep hours for last k logs."""
    rows=sleep_data[-k:]
    return None if not rows else round(sum(r["hours"] for r in rows)/len(rows),2)
    
def plan_alarm(minutes):
    """Alarm time now + X minutes."""
    try: minutes=int(minutes)
    except: minutes=0
    t=datetime.now()+timedelta(minutes=minutes); return {"target_hms":t.strftime("%H:%M:%S"),"target_iso":t.isoformat()}
@bp.post("/sleep/add")

def sleep_add():
    """POST /sleep/add → save sleep record."""
    body=request.get_json(silent=True) or {}; return jsonify(add_log(body.get("bed"),body.get("wake")))
@bp.get("/sleep/recent")

def sleep_recent():
    """GET /sleep/recent?n=5 → recent logs."""
    n=int(request.args.get("n",5)); return jsonify({"items":get_recent(n)})    
@bp.get("/sleep/average")

def sleep_average():
    """GET /sleep/average?k=7 → average hours."""
    k=int(request.args.get("k",7)); return jsonify({"average":get_average(k)})
@bp.post("/alarm/plan")

def alarm_plan():
    """POST /alarm/plan → plan an alarm time."""; body=request.get_json(silent=True) or {}; return jsonify(plan_alarm(body.get("minutes",0)))







'''
