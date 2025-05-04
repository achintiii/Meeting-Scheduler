import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import Report from "./Report";

axios.defaults.baseURL = "http://127.0.0.1:5000";

function MainPage() {
  const [form, setForm] = useState({ title:"", club:"", room:"", start_time:"", end_time:"" });
  const [rows, setRows] = useState([]);
  const [editId, setEditId] = useState(null);

  const change = e => setForm({ ...form, [e.target.name]: e.target.value });

  const save = async e => {
    e.preventDefault();
    const body = { ...form };
    if (editId) await axios.put(`/meetings/${editId}`, body);
    else        await axios.post("/meetings", body);
    setForm({ title:"", club:"", room:"", start_time:"", end_time:"" });
    setEditId(null);
    load();
  };

  const load = async () => {
    const { data } = await axios.get("/meetings");
    const m = data.meetings.map(x=>({
      ...x,
      start_disp: new Date(x.start_time).toLocaleString(),
      end_disp  : new Date(x.end_time).toLocaleString(),
      start_time: x.start_time.slice(0,16),
      end_time  : x.end_time.slice(0,16)
    }));
    setRows(m);
  };

  const del = async id => {
    if (!window.confirm("Delete this meeting?")) return;
    await axios.delete(`/meetings/${id}`);
    load();
  };

  useEffect(()=>{ load(); },[]);

  return (
    <div style={{padding:"2rem"}}>
      <h2>{editId?"Edit Meeting":"Schedule a Meeting"}</h2>
      <form onSubmit={save}>
        <input name="title" placeholder="Title" value={form.title} onChange={change} required/><br/>
        <input name="club"  placeholder="Club"  value={form.club}  onChange={change} required/><br/>
        <input name="room"  placeholder="Room"  value={form.room}  onChange={change} required/><br/>
        <input name="start_time" type="datetime-local" value={form.start_time} onChange={change} required/><br/>
        <input name="end_time"   type="datetime-local" value={form.end_time}   onChange={change} required/><br/>
        <button>{editId?"Update":"Create"} Meeting</button>
      </form>

      <h3 style={{marginTop:"2rem"}}>All Scheduled Meetings</h3>
      <div style={{border:"1px solid gray",padding:"1rem"}}>
        {rows.length===0?
          <p>No meetings scheduled yet.</p>:
          <ul style={{listStyle:"none",padding:0}}>
            {rows.map(r=>(
              <li key={r._id} style={{marginBottom:12,borderBottom:"1px solid #ccc",paddingBottom:6}}>
                <strong>{r.title}</strong> ({r.club})<br/>
                📍 {r.room}<br/>
                🕒 {r.start_disp} → {r.end_disp}<br/>
                <button onClick={()=>{const {_id,start_disp,end_disp,...rest}=r;setForm(rest);setEditId(_id);}}>Edit</button>
                <button style={{marginLeft:8}} onClick={()=>del(r._id)}>Delete</button>
              </li>
            ))}
          </ul>}
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <nav style={{padding:12,background:"#eef0f3",marginBottom:"2rem"}}>
        <NavLink to="/" style={({isActive})=>({marginRight:16,fontWeight:600,color:isActive?"#2563eb":"#333"})}>Manage Meetings</NavLink>
        <NavLink to="/report" style={({isActive})=>({fontWeight:600,color:isActive?"#2563eb":"#333"})}>Reports</NavLink>
      </nav>
      <Routes>
        <Route path="/" element={<MainPage/>}/>
        <Route path="/report" element={<Report/>}/>
      </Routes>
    </Router>
  );
}