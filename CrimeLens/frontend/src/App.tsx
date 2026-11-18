import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  BarChart3,
  Brain,
  MapPin,
  Menu,
  X,
  Shield,
  Navigation,
  Car,
} from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import Prediction from './pages/Prediction';
import Hotspots from './pages/Hotspots';
import SafePath from './pages/SafePath';
import PatrolOptimizer from './pages/PatrolOptimizer';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/safepath', label: 'SafePath AI Corridor', icon: Navigation, isNew: true },
  { path: '/patrol-optimizer', label: 'Smart Patrol Hub', icon: Car, isNew: true },
  { path: '/predict', label: 'AI Prediction & XAI', icon: Brain },
  { path: '/hotspots', label: 'Hotspot Map', icon: MapPin },
  { path: '/analytics', label: 'Crime Analytics', icon: BarChart3 },
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
              <p className="sidebar__subtitle">AI Safety &amp; Corridor Suite</p>
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
                <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
                  {item.label}
                  {item.isNew && (
                    <span
                      style={{
                        background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                        color: '#fff',
                        fontSize: '0.65rem',
                        fontWeight: 700,
                        padding: '1px 6px',
                        borderRadius: '4px',
                        letterSpacing: '0.5px',
                        textTransform: 'uppercase',
                      }}
                    >
                      Novel
                    </span>
                  )}
                </span>
              </NavLink>
            ))}
          </nav>

          <div className="sidebar__footer">
            <p>&copy; 2026 CrimeLens Suite</p>
            <p className="sidebar__footer-note">College Mini Project &bull; ABES</p>
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
            <Route path="/safepath" element={<SafePath />} />
            <Route path="/patrol-optimizer" element={<PatrolOptimizer />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/predict" element={<Prediction />} />
            <Route path="/hotspots" element={<Hotspots />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
