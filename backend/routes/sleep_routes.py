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
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json

sleep_data = []

def _mins(t):
    """Turn HH:MM into total minutes since midnight."""
    h, m = map(int, t.split(":")); return h * 60 + m

def _dur(bed, wake):
    """Find sleep length in hours between bed and wake times."""
    try: b, w = _mins(bed), _mins(wake)
    except: return None
    if w < b: w += 24 * 60
    return round((w - b) / 60, 2)

def add_log(bed, wake):
    """Add a new sleep entry and return the hours slept."""
    d = _dur(bed, wake)
    if d is None: return {"ok": False, "error": "Use HH:MM format"}
    rec = {"bed": bed, "wake": wake, "hours": d}
    sleep_data.append(rec)
    return {"ok": True, "hours": d}

def get_recent(n=5):
    """Get the last n sleep logs (most recent first)."""
    return sleep_data[-n:][::-1]

def get_average(k=7):
    """Get average sleep hours for last k logs."""
    rows = sleep_data[-k:]
    if not rows: return None
    return round(sum(r["hours"] for r in rows) / len(rows), 2)

def plan_alarm(minutes):
    """Return time info for an alarm after X minutes."""
    t = datetime.now() + timedelta(minutes=int(minutes))
    return {"target_hms": t.strftime("%H:%M:%S"), "target_iso": t.isoformat()}

@csrf_exempt
def sleep_add(request):
    """POST /sleep/add → save a sleep record."""
    if request.method != "POST": return HttpResponseNotAllowed(["POST"])
    body = json.loads(request.body or b"{}")
    return JsonResponse(add_log(body.get("bed"), body.get("wake")))

def sleep_recent(request):
    """GET /sleep/recent → show recent logs."""
    n = int(request.GET.get("n", 5))
    return JsonResponse({"items": get_recent(n)})

def sleep_average(request):
    """GET /sleep/average → show average sleep hours."""
    k = int(request.GET.get("k", 7))
    return JsonResponse({"average": get_average(k)})

@csrf_exempt
def alarm_plan(request):
    """POST /alarm/plan → plan an alarm time."""
    if request.method != "POST": return HttpResponseNotAllowed(["POST"])
    body = json.loads(request.body or b"{}")
    return JsonResponse(plan_alarm(body.get("minutes", 0)))


'''
