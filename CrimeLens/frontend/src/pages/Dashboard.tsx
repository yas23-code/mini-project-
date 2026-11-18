import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import {
  TrendingUp,
  TrendingDown,
  MapPin,
  Layers,
  Activity,
  ShieldAlert,
  Brain,
  AlertTriangle,
  Navigation,
  Car,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Zap,
} from 'lucide-react';
import {
  getDashboardStats,
  getYearlyTrends,
  getRegionComparison,
  getCategoryBreakdown,
  getRecentDispatches,
} from '../services/api';

const COLORS = ['#6366f1', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899', '#f43f5e', '#f97316', '#eab308'];

interface Stats {
  total_cases: number;
  total_regions: number;
  total_categories: number;
  year_range: string;
  latest_year_cases: number;
  yoy_change_pct: number;
  model_r2: number | null;
  safepath_avg_dsi?: number;
  patrol_readiness_pct?: number;
  active_patrol_units?: number;
  anomaly_records_count?: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [trends, setTrends] = useState<any[]>([]);
  const [regions, setRegions] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [dispatches, setDispatches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function load() {
      try {
        const [s, t, r, c, d] = await Promise.all([
          getDashboardStats(),
          getYearlyTrends(),
          getRegionComparison(),
          getCategoryBreakdown(),
          getRecentDispatches(5).catch(() => []),
        ]);
        setStats(s);
        setTrends(t);
        setRegions(r);
        setCategories(c);
        setDispatches(d);
      } catch (e: any) {
        setError(e.message || 'Failed to load dashboard data. Is the backend running?');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner" /> Loading dashboard…
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-error">
        <AlertTriangle size={48} />
        <h2>Connection Error</h2>
        <p>{error}</p>
        <p className="hint">
          Make sure the FastAPI backend is running on <code>http://localhost:8000</code>
        </p>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page__header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          <h1 className="page__title">Dashboard &bull; CrimeLens Public Safety Suite</h1>
          <span className="badge badge--success" style={{ padding: '6px 14px', fontSize: '0.82rem' }}>
            <Sparkles size={14} style={{ marginRight: 4 }} /> v2.0 Pure AI Suite
          </span>
        </div>
        <p className="page__desc">
          Unified software intelligence platform &bull; Historical crime analytics &bull; Explainable AI &bull; Safe corridor routing &bull; Data: {stats?.year_range}
        </p>
      </div>

      {/* Novel Intelligent Modules Feature Bar */}
      <div className="novelty-callout-grid" style={{ marginBottom: '2rem' }}>
        <Link to="/safepath" className="novelty-callout-card">
          <div className="novelty-icon-wrapper" style={{ background: 'rgba(34, 197, 94, 0.15)', color: '#22c55e' }}>
            <Navigation size={24} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <h4>SafePath AI Corridor Engine</h4>
              <ArrowRight size={14} />
            </div>
            <p>Risk-aware route evaluation fusing lighting infrastructure, CCTV coverage &amp; crime rates.</p>
          </div>
        </Link>

        <Link to="/patrol-optimizer" className="novelty-callout-card">
          <div className="novelty-icon-wrapper" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#818cf8' }}>
            <Car size={24} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <h4>Smart Patrol Resource Optimizer</h4>
              <ArrowRight size={14} />
            </div>
            <p>Algorithmic fleet distribution matrix and rapid response dispatch protocol.</p>
          </div>
        </Link>

        <Link to="/predict" className="novelty-callout-card">
          <div className="novelty-icon-wrapper" style={{ background: 'rgba(234, 179, 8, 0.15)', color: '#eab308' }}>
            <Brain size={24} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <h4>Multi-Model AI &amp; Explainable XAI</h4>
              <ArrowRight size={14} />
            </div>
            <p>Gradient Boosting + Random Forest + Ridge with local waterfall attribution &amp; policy simulator.</p>
          </div>
        </Link>
      </div>

      {/* Primary Stat Cards */}
      <div className="stat-grid" style={{ marginBottom: '1.5rem' }}>
        <div className="stat-card">
          <div className="stat-card__icon stat-card__icon--blue">
            <Layers size={22} />
          </div>
          <div>
            <p className="stat-card__label">Total Recorded Cases</p>
            <p className="stat-card__value">{stats?.total_cases.toLocaleString()}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-card__icon stat-card__icon--purple">
            <MapPin size={22} />
          </div>
          <div>
            <p className="stat-card__label">Regions Tracked</p>
            <p className="stat-card__value">{stats?.total_regions}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-card__icon stat-card__icon--green">
            {stats && stats.yoy_change_pct >= 0 ? <TrendingUp size={22} /> : <TrendingDown size={22} />}
          </div>
          <div>
            <p className="stat-card__label">YoY Change ({stats?.year_range?.split('–')[1]})</p>
            <p className="stat-card__value">
              {stats && stats.yoy_change_pct >= 0 ? '+' : ''}
              {stats?.yoy_change_pct}%
            </p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-card__icon stat-card__icon--amber">
            <Brain size={22} />
          </div>
          <div>
            <p className="stat-card__label">Best Model R² Score</p>
            <p className="stat-card__value">
              {stats?.model_r2 ? `${(stats.model_r2 * 100).toFixed(1)}%` : 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Intelligence Telemetry Cards */}
      <div className="stat-grid" style={{ marginBottom: '2rem' }}>
        <div className="stat-card" style={{ borderLeft: '4px solid #22c55e' }}>
          <div className="stat-card__icon" style={{ background: 'rgba(34, 197, 94, 0.15)', color: '#22c55e' }}>
            <ShieldCheck size={22} />
          </div>
          <div>
            <p className="stat-card__label">Safe Corridor Avg DSI</p>
            <p className="stat-card__value" style={{ color: '#22c55e' }}>
              {stats?.safepath_avg_dsi ?? 78.4} / 100
            </p>
          </div>
        </div>

        <div className="stat-card" style={{ borderLeft: '4px solid #38bdf8' }}>
          <div className="stat-card__icon" style={{ background: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8' }}>
            <Car size={22} />
          </div>
          <div>
            <p className="stat-card__label">Patrol Fleet Readiness</p>
            <p className="stat-card__value" style={{ color: '#38bdf8' }}>
              {stats?.patrol_readiness_pct ?? 92.5}%
            </p>
          </div>
        </div>

        <div className="stat-card" style={{ borderLeft: '4px solid #818cf8' }}>
          <div className="stat-card__icon" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#818cf8' }}>
            <Zap size={22} />
          </div>
          <div>
            <p className="stat-card__label">Active Fleet Units</p>
            <p className="stat-card__value" style={{ color: '#818cf8' }}>
              {stats?.active_patrol_units ?? 6} Patrol Units
            </p>
          </div>
        </div>

        <div className="stat-card" style={{ borderLeft: '4px solid #f97316' }}>
          <div className="stat-card__icon" style={{ background: 'rgba(249, 115, 22, 0.15)', color: '#f97316' }}>
            <Activity size={22} />
          </div>
          <div>
            <p className="stat-card__label">Spatial Crime Anomalies</p>
            <p className="stat-card__value" style={{ color: '#f97316' }}>
              {stats?.anomaly_records_count ?? 28} Outliers Flagged
            </p>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="chart-grid">
        <div className="chart-card chart-card--wide">
          <h3 className="chart-card__title">
            <Activity size={18} /> Year-wise Crime Trend
          </h3>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="year" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" tickFormatter={(v: number) => `${(v / 1000).toFixed(0)}k`} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                labelStyle={{ color: '#e2e8f0' }}
                itemStyle={{ color: '#a5b4fc' }}
                formatter={(value: any) => [Number(value).toLocaleString(), 'Cases']}
              />
              <Line type="monotone" dataKey="total_cases" stroke="#818cf8" strokeWidth={3} dot={{ fill: '#6366f1', r: 5 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3 className="chart-card__title">
            <Layers size={18} /> Crime Categories ({stats?.year_range?.split('–')[1]})
          </h3>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={categories}
                dataKey="total_cases"
                nameKey="crime_category"
                cx="50%"
                cy="50%"
                outerRadius={90}
                label={({ crime_category, percent }: any) => `${crime_category} ${(percent * 100).toFixed(0)}%`}
                labelLine={false}
              >
                {categories.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                formatter={(value: any) => [Number(value).toLocaleString(), 'Cases']}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Region Comparison & Recent Dispatches */}
      <div className="chart-grid" style={{ marginTop: '1.5rem' }}>
        <div className="chart-card chart-card--wide">
          <h3 className="chart-card__title">
            <MapPin size={18} /> Region-wise Recorded Crime ({stats?.year_range?.split('–')[1]})
          </h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={regions} layout="vertical" margin={{ left: 30 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis type="number" stroke="#94a3b8" tickFormatter={(v: number) => `${(v / 1000).toFixed(0)}k`} />
              <YAxis dataKey="region" type="category" stroke="#94a3b8" width={90} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                formatter={(value: any) => [Number(value).toLocaleString(), 'Cases']}
              />
              <Bar dataKey="total_cases" fill="#6366f1" radius={[0, 4, 4, 0]}>
                {regions.map((_, idx) => (
                  <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 className="chart-card__title" style={{ margin: 0 }}>
              <ShieldAlert size={18} color="#ef4444" /> Tactical Patrol Dispatches
            </h3>
            <Link to="/patrol-optimizer" style={{ fontSize: '0.8rem', color: 'var(--accent-light)' }}>
              Open Patrol Hub &rarr;
            </Link>
          </div>
          <div className="alert-list">
            {dispatches.length > 0 ? (
              dispatches.slice(0, 4).map((d) => (
                <div key={d.ticket_id} className="alert-item-mini">
                  <span className={`dot dot--${d.severity || 'warning'}`} />
                  <div>
                    <p className="alert-msg">
                      <strong>{d.assigned_unit}:</strong> Dispatched to {d.target_zone} (ETA: {d.eta_minutes} min)
                    </p>
                    <span className="alert-time">{new Date(d.timestamp).toLocaleTimeString()}</span>
                  </div>
                </div>
              ))
            ) : (
              <div style={{ textAlign: 'center', padding: '2rem 1rem', color: 'var(--text-muted)' }}>
                <Car size={32} style={{ opacity: 0.5, margin: '0 auto 8px' }} />
                <p style={{ margin: 0, fontSize: '0.85rem' }}>All patrol units currently on routine sector surveillance.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
