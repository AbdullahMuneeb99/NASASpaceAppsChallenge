from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json

sleep_data = []  # stores all sleep entries

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


