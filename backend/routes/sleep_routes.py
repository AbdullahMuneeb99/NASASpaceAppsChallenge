from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json

sleep_data = []

def _mins(t):
    h, m = map(int, t.split(":")); return h * 60 + m

def _dur(bed, wake):
    try:
        b, w = _mins(bed), _mins(wake)
    except:
        return None
    if w < b: w += 24 * 60
    return round((w - b) / 60, 2)

def add_log(bed, wake):
    d = _dur(bed, wake)
    if d is None: return {"ok": False, "error": "Use HH:MM (00-23:00-59)"}
    rec = {"bed": bed, "wake": wake, "hours": d}
    sleep_data.append(rec)
    return {"ok": True, "hours": d}

def get_recent(n=5): return sleep_data[-n:][::-1]

def get_average(k=7):
    rows = sleep_data[-k:]
    if not rows: return None
    hrs = [r["hours"] for r in rows]
    return round(sum(hrs) / len(hrs), 2)

def plan_alarm(minutes):
    t = datetime.now() + timedelta(minutes=int(minutes))
    return {"target_hms": t.strftime("%H:%M:%S"), "target_iso": t.isoformat()}

@csrf_exempt
def sleep_add(request):
    if request.method != "POST": return HttpResponseNotAllowed(["POST"])
    body = json.loads(request.body or "{}")
    return JsonResponse(add_log(body.get("bed"), body.get("wake")))

def sleep_recent(request):
    n = int(request.GET.get("n", 5))
    return JsonResponse({"items": get_recent(n)})

def sleep_average(request):
    k = int(request.GET.get("k", 7))
    return JsonResponse({"average": get_average(k)})

@csrf_exempt
def alarm_plan(request):
    if request.method != "POST": return HttpResponseNotAllowed(["POST"])
    body = json.loads(request.body or "{}")
    return JsonResponse(plan_alarm(body.get("minutes", 0)))
