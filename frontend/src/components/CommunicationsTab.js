// CommunicationsTab.js — React UI for comms
import React, { useEffect, useState } from "react";
import { CommsAPI } from "./communicationsAPI";

export default function CommunicationsTab() {
  // basic form + view state
  const [sender,setSender]=useState("Astronaut A");       // who sends
  const [recipient,setRecipient]=useState("Mission Control"); // who receives
  const [channel,setChannel]=useState("earth");           // crew | earth | station
  const [type,setType]=useState("text");                  // text | voice
  const [content,setContent]=useState("");                // message body
  const [list,setList]=useState([]);                      // message list
  const [latest,setLatest]=useState(null);                // most recent
  const [msg,setMsg]=useState("");                        // status/error

  // load messages for current channel
  const refresh=async()=>{ try{
    const [L,Last]=await Promise.all([CommsAPI.getMessages(channel),CommsAPI.getLatest(channel)]);
    setList(L.items||L||[]); setLatest(Last.item||Last||null);
  }catch(e){ setMsg(e.message);}};

  // send a message
  const send=async()=>{ setMsg("");
    try{ await CommsAPI.sendMessage({sender,recipient,channel,content,type});
      setContent(""); setMsg("Sent"); refresh();
    }catch(e){ setMsg(e.message);}};

  // clear all messages
  const clear=async()=>{ setMsg("");
    try{ await CommsAPI.clear(); setList([]); setLatest(null); setMsg("Cleared"); }
    catch(e){ setMsg(e.message);}};

  useEffect(()=>{ refresh(); },[]);        // first load
  useEffect(()=>{ refresh(); },[channel]); // when channel changes

  return (<div style={{maxWidth:640,padding:12}}>
    <h3>Communications</h3>
    {msg&&<div style={{padding:8,background:"#f6f9ff",border:"1px solid #cfe0ff"}}>{msg}</div>}

    {/* compose row */}
    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr 1fr",gap:6}}>
      <input value={sender} onChange={e=>setSender(e.target.value)} placeholder="Sender"/>
      <input value={recipient} onChange={e=>setRecipient(e.target.value)} placeholder="Recipient"/>
      <select value={channel} onChange={e=>setChannel(e.target.value)}>
        <option value="crew">crew</option><option value="earth">earth</option><option value="station">station</option>
      </select>
      <select value={type} onChange={e=>setType(e.target.value)}>
        <option value="text">text</option><option value="voice">voice</option>
      </select>
    </div>
    <textarea rows={3} style={{width:"100%",marginTop:6,padding:8}} value={content} onChange={e=>setContent(e.target.value)} placeholder="Write message…"/>
    <div style={{marginTop:6,display:"flex",gap:8}}>
      <button onClick={send}>Send</button><button onClick={refresh}>Refresh</button><button onClick={clear}>Clear</button>
    </div>

    {/* latest + list */}
    <hr/><div><b>Latest:</b> {latest?`${latest.sender} → ${latest.recipient} [${latest.channel}/${latest.type}] ${latest.content}`:"—"}</div>
    <ul style={{marginTop:6,paddingLeft:18}}>
      {list.length?list.map((m,i)=><li key={i}>{m.timestamp||""} — <b>{m.sender}</b> → {m.recipient} [{m.channel}/{m.type}]: {m.content}</li>):<li>No messages</li>}
    </ul>
  </div>);
}
