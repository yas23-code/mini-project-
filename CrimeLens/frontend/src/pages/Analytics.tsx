import { useEffect, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, Legend, Cell,
} from 'recharts';
import { Filter, AlertTriangle } from 'lucide-react';
import { getCrimeRecords, getRegions, getCategories } from '../services/api';

const COLORS = ['#6366f1', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899', '#f43f5e', '#f97316', '#eab308'];

export default function Analytics() {
  const [records, setRecords] = useState<any[]>([]);
  const [regions, setRegions] = useState<string[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [filterRegion, setFilterRegion] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function load() {
      try {
        const [rg, cat] = await Promise.all([getRegions(), getCategories()]);
        setRegions(rg.regions);
        setCategories(cat.categories);
        const data = await getCrimeRecords({});
        setRecords(data);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const applyFilters = async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (filterRegion) params.region = filterRegion;
      if (filterCategory) params.category = filterCategory;
      params.limit = '500';
      const data = await getCrimeRecords(params);
      setRecords(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  // Aggregate for charts
  const yearWise = records.reduce((acc: Record<number, number>, r) => {
    acc[r.year] = (acc[r.year] || 0) + r.recorded_cases;
    return acc;
  }, {});
  const yearData = Object.entries(yearWise)
    .map(([year, cases]) => ({ year: +year, cases }))
    .sort((a, b) => a.year - b.year);

  const catWise = records.reduce((acc: Record<string, number>, r) => {
    acc[r.crime_category] = (acc[r.crime_category] || 0) + r.recorded_cases;
    return acc;
  }, {});
  const catData = Object.entries(catWise)
    .map(([cat, cases]) => ({ category: cat, cases }))
    .sort((a, b) => (b.cases as number) - (a.cases as number));

  const regionWise = records.reduce((acc: Record<string, number>, r) => {
    acc[r.region] = (acc[r.region] || 0) + r.recorded_cases;
    return acc;
  }, {});
  const regionData = Object.entries(regionWise)
    .map(([region, cases]) => ({ region, cases }))
    .sort((a, b) => (b.cases as number) - (a.cases as number));

  // Year-category breakdown for multi-line chart
  const yearCatMap: Record<number, Record<string, number>> = {};
  records.forEach((r) => {
    if (!yearCatMap[r.year]) yearCatMap[r.year] = {};
    yearCatMap[r.year][r.crime_category] = (yearCatMap[r.year][r.crime_category] || 0) + r.recorded_cases;
  });
  const uniqueCats = [...new Set(records.map((r) => r.crime_category))];
  const yearCatData = Object.entries(yearCatMap)
    .map(([year, cats]) => ({ year: +year, ...cats }))
    .sort((a, b) => a.year - b.year);

  if (error) return (
    <div className="page-error">
      <AlertTriangle size={48} />
      <h2>Error</h2>
      <p>{error}</p>
    </div>
  );

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">Crime Analytics</h1>
        <p className="page__desc">Explore historical crime data from the sample dataset</p>
      </div>

      {/* Filters */}
      <div className="filter-bar">
        <Filter size={18} />
        <select value={filterRegion} onChange={(e) => setFilterRegion(e.target.value)} className="filter-select">
          <option value="">All Regions</option>
          {regions.map((r) => <option key={r} value={r}>{r}</option>)}
        </select>
        <select value={filterCategory} onChange={(e) => setFilterCategory(e.target.value)} className="filter-select">
          <option value="">All Categories</option>
          {categories.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <button onClick={applyFilters} className="btn btn--primary" disabled={loading}>
          {loading ? 'Loading…' : 'Apply Filters'}
        </button>
      </div>

      <p className="text-muted" style={{ marginBottom: '1rem' }}>
        Showing {records.length} records. Dataset: sample/synthetic data for demonstration.
      </p>

      {/* Year trend */}
      <div className="chart-grid">
        <div className="chart-card chart-card--wide">
          <h3 className="chart-card__title">Year-wise Crime Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={yearCatData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="year" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" tickFormatter={(v: number) => `${(v / 1000).toFixed(0)}k`} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                labelStyle={{ color: '#e2e8f0' }}
                formatter={(value: number) => [value?.toLocaleString(), 'Cases']}
              />
              <Legend />
              {uniqueCats.map((cat, i) => (
                <Line key={cat} type="monotone" dataKey={cat} stroke={COLORS[i % COLORS.length]} strokeWidth={2} dot={{ r: 3 }} />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3 className="chart-card__title">Category Comparison</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={catData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="category" stroke="#94a3b8" angle={-20} textAnchor="end" height={60} />
              <YAxis stroke="#94a3b8" tickFormatter={(v: number) => `${(v / 1000).toFixed(0)}k`} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                formatter={(value: number) => [value.toLocaleString(), 'Cases']}
              />
              <Bar dataKey="cases" radius={[6, 6, 0, 0]}>
                {catData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Region bar */}
      <div className="chart-card" style={{ marginTop: '1.5rem' }}>
        <h3 className="chart-card__title">Region-wise Statistics</h3>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={regionData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis type="number" stroke="#94a3b8" tickFormatter={(v: number) => `${(v / 1000).toFixed(0)}k`} />
            <YAxis type="category" dataKey="region" stroke="#94a3b8" width={120} />
            <Tooltip
              contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
              formatter={(value: number) => [value.toLocaleString(), 'Cases']}
            />
            <Bar dataKey="cases" radius={[0, 6, 6, 0]}>
              {regionData.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Data table */}
      <div className="chart-card" style={{ marginTop: '1.5rem' }}>
        <h3 className="chart-card__title">Raw Records (Sample)</h3>
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>Region</th>
                <th>Year</th>
                <th>Category</th>
                <th>Recorded Cases</th>
                <th>Population (Lakhs)</th>
              </tr>
            </thead>
            <tbody>
              {records.slice(0, 30).map((r, i) => (
                <tr key={i}>
                  <td>{r.region}</td>
                  <td>{r.year}</td>
                  <td>{r.crime_category}</td>
                  <td>{r.recorded_cases.toLocaleString()}</td>
                  <td>{r.population_lakhs}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {records.length > 30 && (
            <p className="text-muted" style={{ padding: '0.5rem 1rem' }}>
              Showing first 30 of {records.length} records
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

