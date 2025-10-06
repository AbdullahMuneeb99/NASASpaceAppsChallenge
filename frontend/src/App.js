import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import PowerTab from './components/PowerTab';
import LifeSupportTab from './components/LifeSupportTab';
import MedicalTab from './components/MedicalTab';
import CommunicationsTab from './components/CommunicationsTab';
import SleepTab from './components/SleepTab';
import LogbookTab from './components/LogbookTab';
import './styles/main.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <header className="header">
          <h1 className="app-title">🚀 SpaceVitals Dashboard</h1>
          <nav className="nav-bar">
            <NavLink to="/power" className="nav-link">Power</NavLink>
            <NavLink to="/life-support" className="nav-link">Life Support</NavLink>
            <NavLink to="/medical" className="nav-link">Medical</NavLink>
            <NavLink to="/comms" className="nav-link">Communications</NavLink>
            <NavLink to="/sleep" className="nav-link">Sleep</NavLink>
            <NavLink to="/logbook" className="nav-link">Logbook</NavLink>
          </nav>
        </header>

        <main className="main-content">
          <Routes>
            <Route path="/power" element={<PowerTab />} />
            <Route path="/life-support" element={<LifeSupportTab />} />
            <Route path="/medical" element={<MedicalTab />} />
            <Route path="/comms" element={<CommunicationsTab />} />
            <Route path="/sleep" element={<SleepTab />} />
            <Route path="/logbook" element={<LogbookTab />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
