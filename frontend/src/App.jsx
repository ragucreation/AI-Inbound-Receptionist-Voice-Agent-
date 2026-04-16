import React, { useState, useEffect } from 'react'
import './index.css'

function App() {
  const [activeTab, setActiveTab] = useState('logs')
  const [logs, setLogs] = useState([])
  const [leads, setLeads] = useState([])

  // In a real app, these would fetch from the FastAPI backend
  // useEffect(() => {
  //   fetch('/api/logs').then(res => res.json()).then(data => setLogs(data))
  //   fetch('/api/leads').then(res => res.json()).then(data => setLeads(data))
  // }, [])

  // Mock data for initial look
  const mockLogs = [
    { id: 1, caller: '+1 234 567 890', intent: 'Booking', transcript: 'I want to book an appointment tomorrow at 5 PM', time: '2 mins ago' },
    { id: 2, caller: '+1 987 654 321', intent: 'Inquiry', transcript: 'What are your opening hours on Saturday?', time: '10 mins ago' },
    { id: 3, caller: '+1 555 444 333', intent: 'Routing', transcript: 'I need to speak with the billing department', time: '1 hour ago' },
  ]

  const mockLeads = [
    { id: 1, name: 'John Doe', phone: '+1 234 567 890', service: 'Dental Cleaning', status: 'Hot' },
    { id: 2, name: 'Sarah Smith', phone: '+1 987 654 321', service: 'General Checkup', status: 'Normal' },
  ]

  return (
    <div className="dashboard-container">
      <aside className="sidebar glass-card" style={{margin: '1rem', borderRadius: '24px'}}>
        <h2 style={{color: 'var(--primary)', marginBottom: '1rem'}}>AI Reception</h2>
        <nav style={{display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
          <div className={`nav-item ${activeTab === 'logs' ? 'active' : ''}`} onClick={() => setActiveTab('logs')}>
             <span>📞</span> Call Logs
          </div>
          <div className={`nav-item ${activeTab === 'leads' ? 'active' : ''}`} onClick={() => setActiveTab('leads')}>
             <span>🔥</span> Leads
          </div>
          <div className={`nav-item ${activeTab === 'calendar' ? 'active' : ''}`} onClick={() => setActiveTab('calendar')}>
             <span>📅</span> Calendar
          </div>
          <div className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`} onClick={() => setActiveTab('settings')}>
             <span>⚙️</span> Settings
          </div>
        </nav>
      </aside>

      <main className="main-content">
        <header style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem'}}>
          <h1>{activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}</h1>
          <div className="glass-card" style={{padding: '0.5rem 1rem'}}>
            <span style={{color: 'var(--text-muted)'}}>Active: </span>
            <span style={{color: 'var(--success)'}}>● Online</span>
          </div>
        </header>

        <div className="stats-grid">
          <div className="stat-card glass-card">
            <span style={{color: 'var(--text-muted)'}}>Total Calls</span>
            <span className="stat-value">1,284</span>
            <span style={{color: 'var(--success)', fontSize: '0.8rem'}}>+12% from yesterday</span>
          </div>
          <div className="stat-card glass-card">
            <span style={{color: 'var(--text-muted)'}}>New Leads</span>
            <span className="stat-value" style={{color: 'var(--accent)', WebkitTextFillColor: 'unset'}}>48</span>
            <span style={{color: 'var(--success)', fontSize: '0.8rem'}}>+5% this week</span>
          </div>
          <div className="stat-card glass-card">
            <span style={{color: 'var(--text-muted)'}}>Bookings</span>
            <span className="stat-value" style={{color: 'var(--primary)', WebkitTextFillColor: 'unset'}}>156</span>
            <span style={{color: 'var(--text-muted)', fontSize: '0.8rem'}}>Across 4 businesses</span>
          </div>
        </div>

        {activeTab === 'logs' && (
          <div className="glass-card" style={{padding: '1.5rem'}}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Caller</th>
                  <th>Intent</th>
                  <th>Transcript</th>
                  <th>Time</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {mockLogs.map(log => (
                  <tr key={log.id}>
                    <td>{log.caller}</td>
                    <td><span className={`status-badge ${log.intent === 'Booking' ? 'status-hot' : 'status-success'}`}>{log.intent}</span></td>
                    <td style={{fontSize: '0.9rem', color: 'var(--text-muted)'}}>{log.transcript}</td>
                    <td>{log.time}</td>
                    <td><button style={{padding: '0.4rem 0.8rem', fontSize: '0.8rem'}}>View</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'leads' && (
          <div className="glass-card" style={{padding: '1.5rem'}}>
             <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Phone</th>
                  <th>Service</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {mockLeads.map(lead => (
                  <tr key={lead.id}>
                    <td>{lead.name}</td>
                    <td>{lead.phone}</td>
                    <td>{lead.service}</td>
                    <td><span className={`status-badge ${lead.status === 'Hot' ? 'status-hot' : 'status-success'}`}>{lead.status}</span></td>
                    <td><button style={{padding: '0.4rem 0.8rem', fontSize: '0.8rem'}}>Contact</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
