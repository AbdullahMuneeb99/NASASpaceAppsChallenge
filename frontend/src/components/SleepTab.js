// sleepTab.js — React tab for Sleep API
import React, { useEffect, useState } from "react";
import { SleepAPI } from "./sleepAPI";

export default function SleepTab() {
  // basic state
  const [bed, setBed] = useState("23:00");          // bedtime HH:MM
  const [wake, setWake] = useState("07:00");        // wake HH:MM
  const [n, setN] = useState(5);                    // recent count
  const [k, setK] = useState(7);                    // avg window
  const [recent, setRecent] = useState([]);         // recent logs
  const [avg, setAvg] = useState(null);             // average hours
  const [msg, setMsg] = useState("");               // status/error
  const [mins, setMins] = useState(10);             // alarm mins
  const [alarm, setAlarm] = useState(null);         // alarm target

  // fetch recent + average
  const refresh = async () => {
    try {
      const [r, a] = await Promise.all([SleepAPI.getRecent(n), SleepAPI.getAverage(k)]);
      setRecent(r.items || []); setAvg(a.average ?? null);
    } catch (e) { setMsg(e.message); }
  };

  // add a sleep log
  const add = async () => {
    setMsg("");
    try {
      const r = await SleepAPI.addLog(bed.trim(), wake.trim());
      setMsg(r.ok ? `Logged ${r.hours} h` : r.error); refresh();
    } catch (e) { setMsg(e.message); }
  };

  // plan an alarm
  const plan = async () => {
    setMsg("");
    try { const r = await SleepAPI.planAlarm(Number(mins||0)); setAlarm(r); setMsg(`Alarm: ${r.target_hms}`); }
    catch (e) { setMsg(e.message); }
  };

  useEffect(() => { refresh(); }, []); // load once

  return (
    <div style={{ maxWidth: 520, padding: 12 }}>
      <h3>Sleep</h3>
      {msg && <div style={{ padding:8,background:"#f6f9ff",border:"1px solid #cfe0ff" }}>{msg}</div>}

      {/* inputs for bed/wake + actions */}
      <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:8 }}>
        <input value={bed}  onChange={e=>setBed(e.target.value)}  placeholder="Bed HH:MM" />
        <input value={wake} onChange={e=>setWake(e.target.value)} placeholder="Wake HH:MM" />
      </div>
      <div style={{ marginTop:8,display:"flex",gap:8 }}>
        <button onClick={add}>Add Log</button><button onClick={refresh}>Refresh</button>
      </div>

      <hr />
      {/* average + recent */}
      <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:8 }}>
        <input value={n} onChange={e=>setN(Number(e.target.value||0))} placeholder="n recent" />
        <input value={k} onChange={e=>setK(Number(e.target.value||0))} placeholder="k avg" />
      </div>
      <div style={{ marginTop:6 }}>Average: <b>{avg==null?"—":`${avg.toFixed(2)} h`}</b></div>
      <ul>{recent.length?recent.map((r,i)=><li key={i}>{r.bed} → {r.wake} | {r.hours} h</li>):<li>None</li>}</ul>

      <hr />
      {/* alarm planner */}
      <div style={{ display:"grid",gridTemplateColumns:"1fr auto",gap:8 }}>
        <input value={mins} onChange={e=>setMins(Number(e.target.value||0))} placeholder="Alarm mins" />
        <button onClick={plan}>Plan Alarm</button>
      </div>
      {alarm && <div style={{ marginTop:6 }}>Target: {alarm.target_hms} <code>{alarm.target_iso}</code></div>}
    </div>
  );

