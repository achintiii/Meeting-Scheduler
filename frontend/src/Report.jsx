import { useState } from "react";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:5000";

export default function Report() {
  const [f, setF] = useState({ start: "", end: "", club: "", room: "" });
  const [rows, setRows] = useState([]);
  const [stats, setStats] = useState(null);

  async function run() {
    const p = Object.fromEntries(Object.entries(f).filter(([_, v]) => v));
    const res = await axios.get("/meetings/filter", { params: p });
    setRows(res.data.meetings);
    setStats(res.data.stats);
  }

  return (
    <section style={box}>
      <h2>📊 Meeting Reports</h2>
      <div style={{ marginBottom: 16 }}>
        <label>Start <input type="date" value={f.start} onChange={e=>setF({...f,start:e.target.value})}/></label>
        <label style={{marginLeft:12}}>End <input type="date" value={f.end} onChange={e=>setF({...f,end:e.target.value})}/></label>
        <label style={{marginLeft:12}}>Club <input value={f.club} onChange={e=>setF({...f,club:e.target.value})}/></label>
        <label style={{marginLeft:12}}>Room <input value={f.room} onChange={e=>setF({...f,room:e.target.value})}/></label>
        <button onClick={run} style={{marginLeft:12}}>Run</button>
      </div>

      {rows.length===0 ? <p>No matching meetings.</p> :
        <ul style={{listStyle:"none",padding:0}}>
          {rows.map(r=>(
            <li key={r._id} style={{marginBottom:12,borderBottom:"1px solid #ccc",paddingBottom:6}}>
              <strong>{r.title}</strong> ({r.club})<br/>
              📍 {r.room}<br/>
              🕒 {new Date(r.start_time).toLocaleString()} – {new Date(r.end_time).toLocaleString()}
            </li>
          ))}
        </ul>}

      {stats && stats.count>0 &&
        <div style={{marginTop:24}}>
          <h4>Statistics</h4>
          <ul>
            <li>Total meetings: {stats.count}</li>
            <li>Average duration: {stats.avg_duration_min} min</li>
            <li>Shortest duration: {stats.min_duration_min} min</li>
            <li>Longest duration: {stats.max_duration_min} min</li>
            <li>Earliest start: {stats.first_start}</li>
            <li>Latest end: {stats.last_end}</li>
          </ul>
        </div>}
    </section>
  );
}

const box={maxWidth:800,margin:"3rem auto",padding:24,background:"#f9fafb",borderRadius:12,boxShadow:"0 6px 16px rgba(0,0,0,.08)"};