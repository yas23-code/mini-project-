import { useEffect, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  Cell,
} from 'recharts';
import { Brain, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import { predictCrime, getRegions, getCategories, getModelMetrics } from '../services/api';

const RISK_COLORS: Record<string, string> = {
  Low: '#22c55e',
  Moderate: '#eab308',
  High: '#f97316',
  'Very High': '#ef4444',
};

export default function Prediction() {
  const [regions, setRegions] = useState<string[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [metrics, setMetrics] = useState<any>(null);

  const [region, setRegion] = useState('');
  const [year, setYear] = useState(2024);
  const [category, setCategory] = useState('');
  const [population, setPopulation] = useState(200);

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    async function load() {
      try {
        const [rg, cat, met] = await Promise.all([
          getRegions(),
          getCategories(),
          getModelMetrics(),
        ]);
        setRegions(rg.regions);
        setCategories(cat.categories);
        setMetrics(met);
        if (rg.regions.length) setRegion(rg.regions[0]);
        if (cat.categories.length) setCategory(cat.categories[0]);
      } catch (e: any) {
        setError(e.message);
      }
    }
    load();
  }, []);

  const handlePredict = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await predictCrime({
        region,
        year,
        crime_category: category,
        population_lakhs: population,
      });
      setResult(res);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const featureData = metrics?.feature_importance
    ? Object.entries(metrics.feature_importance).map(([name, value]) => ({
        name,
        importance: +(value as number * 100).toFixed(1),
      }))
    : [];

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">
          <Brain size={28} style={{ display: 'inline', verticalAlign: 'middle', marginRight: 8 }} />
          AI Crime Prediction
        </h1>
        <p className="page__desc">
          Random Forest model trained on historical sample data. Estimates are not official forecasts.
        </p>
      </div>

      <div className="predict-layout">
        {/* Input form */}
        <div className="chart-card predict-form">
          <h3 className="chart-card__title">Prediction Parameters</h3>

          <div className="form-group">
            <label className="form-label">Region</label>
            <select value={region} onChange={(e) => setRegion(e.target.value)} className="filter-select form-input">
              {regions.map((r) => <option key={r} value={r}>{r}</option>)}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Year</label>
            <input
              type="number"
              min={2000}
              max={2035}
              value={year}
              onChange={(e) => setYear(+e.target.value)}
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Crime Category</label>
            <select value={category} onChange={(e) => setCategory(e.target.value)} className="filter-select form-input">
              {categories.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Population (Lakhs)</label>
            <input
              type="number"
              min={1}
              max={5000}
              value={population}
              onChange={(e) => setPopulation(+e.target.value)}
              className="form-input"
            />
          </div>

          <button onClick={handlePredict} className="btn btn--primary btn--full" disabled={loading}>
            {loading ? 'Predicting…' : 'Get Prediction'}
          </button>

          {error && (
            <div className="form-error">
              <AlertTriangle size={16} /> {error}
            </div>
          )}
        </div>

        {/* Result */}
        <div className="predict-result-area">
          {result && (
            <div className="chart-card predict-result">
              <h3 className="chart-card__title">
                <CheckCircle size={18} /> Prediction Result
              </h3>
              <div className="result-grid">
                <div className="result-item">
                  <span className="result-label">Region</span>
                  <span className="result-value">{result.region}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">Year</span>
                  <span className="result-value">{result.year}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">Category</span>
                  <span className="result-value">{result.crime_category}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">Population</span>
                  <span className="result-value">{result.population_lakhs} Lakhs</span>
                </div>
                <div className="result-item result-item--highlight">
                  <span className="result-label">Estimated Cases</span>
                  <span className="result-value result-value--big">
                    {result.estimated_cases.toLocaleString()}
                  </span>
                </div>
                <div className="result-item">
                  <span className="result-label">Risk Category</span>
                  <span
                    className="risk-badge"
                    style={{ background: RISK_COLORS[result.risk_category] || '#6366f1' }}
                  >
                    {result.risk_category}
                  </span>
                </div>
              </div>
              <p className="text-muted" style={{ marginTop: '1rem', fontSize: '0.8rem' }}>
                <Info size={14} style={{ display: 'inline', verticalAlign: 'middle' }} />{' '}
                {result.note}
              </p>
            </div>
          )}

          {/* Model metrics */}
          {metrics && (
            <div className="chart-card" style={{ marginTop: '1.5rem' }}>
              <h3 className="chart-card__title">Model Evaluation</h3>
              <div className="result-grid">
                <div className="result-item">
                  <span className="result-label">R² Score</span>
                  <span className="result-value">{metrics.r2_score}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">MAE</span>
                  <span className="result-value">{metrics.mae?.toLocaleString()}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">Train Samples</span>
                  <span className="result-value">{metrics.train_samples}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">Test Samples</span>
                  <span className="result-value">{metrics.test_samples}</span>
                </div>
              </div>
              <p className="text-muted" style={{ margin: '1rem 0 0.5rem' }}>
                {metrics.note}
              </p>

              {featureData.length > 0 && (
                <>
                  <h4 style={{ color: '#e2e8f0', margin: '1rem 0 0.5rem' }}>Feature Importance (%)</h4>
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={featureData} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis type="number" stroke="#94a3b8" domain={[0, 100]} />
                      <YAxis type="category" dataKey="name" stroke="#94a3b8" width={130} />
                      <Tooltip
                        contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                        formatter={(v: number) => [`${v}%`, 'Importance']}
                      />
                      <Bar dataKey="importance" radius={[0, 6, 6, 0]}>
                        {featureData.map((_, i) => (
                          <Cell key={i} fill={['#6366f1', '#8b5cf6', '#a855f7', '#d946ef'][i % 4]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
