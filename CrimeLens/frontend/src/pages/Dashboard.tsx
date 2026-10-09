import { useEffect, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell, Legend,
} from 'recharts';
import {
  TrendingUp, TrendingDown, MapPin, Layers, Activity, ShieldAlert,
  Brain, AlertTriangle,
} from 'lucide-react';
import {
  getDashboardStats, getYearlyTrends, getRegionComparison,
  getCategoryBreakdown, getAlerts,
} from '../services/api';

const COLORS = ['#6366f1', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899', '#f43f5e', '#f97316', '#eab308'];

interface Stats {
  total_cases: number;
  total_regions: number;
  total_categories: number;
  year_range: string;
  latest_year_cases: number;
  yoy_change_pct: number;
  active_alerts: number;
  model_r2: number | null;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [trends, setTrends] = useState<any[]>([]);
  const [regions, setRegions] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function load() {
      try {
        const [s, t, r, c, a] = await Promise.all([
          getDashboardStats(),
          getYearlyTrends(),
          getRegionComparison(),
          getCategoryBreakdown(),
          getAlerts(5),
        ]);
        setStats(s);
        setTrends(t);
        setRegions(r);
        setCategories(c);
        setAlerts(a);
      } catch (e: any) {
        setError(e.message || 'Failed to load dashboard data. Is the backend running?');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <div className="page-loading"><div className="spinner" /> Loading dashboard…</div>;
  if (error) return (
    <div className="page-error">
      <AlertTriangle size={48} />
      <h2>Connection Error</h2>
      <p>{error}</p>
      <p className="hint">Make sure the FastAPI backend is running on <code>http://localhost:8000</code></p>
    </div>
  );

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">Dashboard</h1>
        <p className="page__desc">Crime analytics overview &bull; Data: {stats?.year_range}</p>
      </div>

      {/* Stat cards */}
      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-card__icon stat-card__icon--blue"><Layers size={22} /></div>
          <div>
            <p className="stat-card__label">Total Recorded Cases</p>
            <p className="stat-card__value">{stats?.total_cases.toLocaleString()}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-card__icon stat-card__icon--purple"><MapPin size={22} /></div>
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
          <div className="stat-card__icon stat-card__icon--amber"><Brain size={22} /></div>
          <div>
            <p className="stat-card__label">Model R² Score</p>
            <p className="stat-card__value">{stats?.model_r2 ?? 'N/A'}</p>
          </div>
        </div>
      </div>

      {/* Charts row */}
      <div className="chart-grid">
        <div className="chart-card chart-card--wide">
          <h3 className="chart-card__title">
            <Activity size={18} /> Year-wise Crime Trend
          </h3>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="year" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" tickFormatter={(v: number) => `${(v/1000).toFixed(0)}k`} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                labelStyle={{ color: '#e2e8f0' }}
                itemStyle={{ color: '#a5b4fc' }}
                formatter={(value: number) => [value.toLocaleString(), 'Cases']}
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
              >
                {categories.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                formatter={(value: number) => [value.toLocaleString(), 'Cases']}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Region comparison + alerts */}
      <div className="chart-grid">
        <div className="chart-card chart-card--wide">
          <h3 className="chart-card__title">
            <MapPin size={18} /> Region Comparison ({stats?.year_range?.split('–')[1]})
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={regions} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis type="number" stroke="#94a3b8" tickFormatter={(v: number) => `${(v/1000).toFixed(0)}k`} />
              <YAxis type="category" dataKey="region" stroke="#94a3b8" width={110} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                formatter={(value: number) => [value.toLocaleString(), 'Cases']}
              />
              <Bar dataKey="total_cases" radius={[0, 6, 6, 0]}>
                {regions.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3 className="chart-card__title">
            <ShieldAlert size={18} /> Recent Alerts
          </h3>
          <div className="alert-list">
            {alerts.length === 0 ? (
              <p className="text-muted">No recent alerts</p>
            ) : (
              alerts.map((a: any) => (
                <div key={a.id} className={`alert-item alert-item--${a.severity}`}>
                  <AlertTriangle size={16} />
                  <div>
                    <p className="alert-item__msg">{a.message}</p>
                    <p className="alert-item__time">{new Date(a.timestamp).toLocaleString()}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
