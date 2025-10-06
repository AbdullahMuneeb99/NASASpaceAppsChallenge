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







