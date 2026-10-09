import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  BarChart3,
  Brain,
  MapPin,
  Radio,
  Menu,
  X,
  Shield,
} from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import Prediction from './pages/Prediction';
import Hotspots from './pages/Hotspots';
import IoTMonitor from './pages/IoTMonitor';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/analytics', label: 'Crime Analytics', icon: BarChart3 },
  { path: '/predict', label: 'AI Prediction', icon: Brain },
  { path: '/hotspots', label: 'Hotspot Map', icon: MapPin },
  { path: '/iot', label: 'IoT Monitor', icon: Radio },
];

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <Router>
      <div className="app-layout">
        {/* Mobile menu button */}
        <button
          className="mobile-menu-btn"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          aria-label="Toggle menu"
        >
          {sidebarOpen ? <X size={22} /> : <Menu size={22} />}
        </button>

        {/* Sidebar */}
        <aside className={`sidebar ${sidebarOpen ? 'sidebar--open' : ''}`}>
          <div className="sidebar__brand">
            <Shield size={28} className="sidebar__brand-icon" />
            <div>
              <h1 className="sidebar__title">CrimeLens</h1>
              <p className="sidebar__subtitle">AI Safety Monitor</p>
            </div>
          </div>

          <nav className="sidebar__nav">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `sidebar__link ${isActive ? 'sidebar__link--active' : ''}`
                }
                onClick={() => setSidebarOpen(false)}
              >
                <item.icon size={20} />
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>

          <div className="sidebar__footer">
            <p>© 2024 CrimeLens</p>
            <p className="sidebar__footer-note">College Mini Project</p>
          </div>
        </aside>

        {/* Overlay for mobile */}
        {sidebarOpen && (
          <div
            className="sidebar-overlay"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Main content */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/predict" element={<Prediction />} />
            <Route path="/hotspots" element={<Hotspots />} />
            <Route path="/iot" element={<IoTMonitor />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
