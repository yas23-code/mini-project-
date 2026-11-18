import { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import {
  Brain,
  AlertTriangle,
  CheckCircle,
  Info,
  Sparkles,
  Sliders,
  Shield,
  Layers,
  ArrowRight,
  TrendingDown,
} from 'lucide-react';
import {
  predictCrime,
  getRegions,
  getCategories,
  getModelMetrics,
  getModelBenchmark,
  simulatePolicy,
} from '../services/api';

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
  const [benchmark, setBenchmark] = useState<any>(null);

  // Form inputs
  const [region, setRegion] = useState('');
  const [year, setYear] = useState(2024);
  const [category, setCategory] = useState('');
  const [population, setPopulation] = useState(200);
  const [selectedModel, setSelectedModel] = useState('random_forest');

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Policy simulator state
  const [lightingPct, setLightingPct] = useState(35);
  const [patrolPct, setPatrolPct] = useState(30);
  const [cctvPct, setCctvPct] = useState(25);
  const [policyResult, setPolicyResult] = useState<any>(null);

  useEffect(() => {
    async function load() {
      try {
        const [rg, cat, met, bench] = await Promise.all([
          getRegions(),
          getCategories(),
          getModelMetrics(),
          getModelBenchmark().catch(() => null),
        ]);
        setRegions(rg.regions);
        setCategories(cat.categories);
        setMetrics(met);
        setBenchmark(bench);
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
    setPolicyResult(null);
    try {
      const res = await predictCrime({
        region,
        year,
        crime_category: category,
        population_lakhs: population,
        model_name: selectedModel,
      });
      setResult(res);

      // Trigger automatic policy baseline simulation
      if (res.estimated_cases) {
        const sim = await simulatePolicy({
          base_cases: res.estimated_cases,
          lighting_improvement_pct: lightingPct,
          patrol_density_increase_pct: patrolPct,
          smart_cctv_coverage_pct: cctvPct,
        });
        setPolicyResult(sim);
      }
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePolicyChange = async (light: number, patrol: number, cctv: number) => {
    setLightingPct(light);
    setPatrolPct(patrol);
    setCctvPct(cctv);
    if (result?.estimated_cases) {
      const sim = await simulatePolicy({
        base_cases: result.estimated_cases,
        lighting_improvement_pct: light,
        patrol_density_increase_pct: patrol,
        smart_cctv_coverage_pct: cctv,
      });
      setPolicyResult(sim);
    }
  };

  // Waterfall Chart Data for Explainable AI (XAI)
  const waterfallData = result?.xai_waterfall
    ? result.xai_waterfall.map((item: any) => ({
        name: item.feature.split(' (')[0],
        fullName: item.feature,
        value: item.contribution,
        direction: item.direction,
      }))
    : [];

  return (
    <div className="page">
      <div className="page__header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          <h1 className="page__title">
            <Brain size={28} style={{ display: 'inline', verticalAlign: 'middle', marginRight: 8 }} />
            AI Crime Prediction &amp; Explainable AI (XAI)
          </h1>
          <span className="badge badge--success" style={{ padding: '6px 14px', fontSize: '0.82rem' }}>
            <Sparkles size={14} style={{ marginRight: 4 }} /> Multi-Model + XAI Suite
          </span>
        </div>
        <p className="page__desc">
          Compare multi-model regression architectures (Random Forest vs Gradient Boosting vs Ridge) and inspect
          local feature attribution explanations and confidence intervals.
        </p>
      </div>

      {/* Model Benchmark Comparison Bar */}
      {benchmark && benchmark.models && (
        <div className="chart-card" style={{ marginBottom: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: 10 }}>
            <h3 className="chart-card__title" style={{ margin: 0, display: 'flex', alignItems: 'center', gap: 8 }}>
              <Layers size={18} color="var(--accent-light)" />
              Multi-Model Architectural Benchmark
            </h3>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Evaluated on identical held-out 20% test partition ({benchmark.sample_count} total records)
            </span>
          </div>

          <div className="benchmark-cards-grid">
            {benchmark.models.map((m: any) => {
              const isSelected = selectedModel === m.name;
              return (
                <div
                  key={m.name}
                  onClick={() => setSelectedModel(m.name)}
                  className={`benchmark-card ${isSelected ? 'benchmark-card--selected' : ''}`}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h4 style={{ margin: 0, fontSize: '0.95rem' }}>{m.display_name}</h4>
                    {m.r2_score >= 0.98 && <span className="badge badge--success">Top R²</span>}
                  </div>
                  <div className="benchmark-metrics-row">
                    <div>
                      <span className="sub-label">R² Score</span>
                      <strong style={{ color: m.r2_score > 0.9 ? '#22c55e' : '#eab308' }}>
                        {(m.r2_score * 100).toFixed(1)}%
                      </strong>
                    </div>
                    <div>
                      <span className="sub-label">MAE</span>
                      <strong>{m.mae.toLocaleString()}</strong>
                    </div>
                    <div>
                      <span className="sub-label">Latency</span>
                      <span style={{ color: 'var(--text-secondary)' }}>{m.inference_latency_ms} ms</span>
                    </div>
                  </div>
                  <div className="card-selector-indicator">
                    {isSelected ? '✓ Active Prediction Model' : 'Click to Select'}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className="predict-layout">
        {/* Input Form */}
        <div className="chart-card predict-form">
          <h3 className="chart-card__title">Prediction Parameters</h3>

          <div className="form-group">
            <label className="form-label">Active ML Model</label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="filter-select form-input"
            >
              <option value="random_forest">Random Forest Regressor (Ensemble Bagging)</option>
              <option value="gradient_boosting">Gradient Boosting Regressor (Sequential Boosting)</option>
              <option value="ridge">Ridge Regression (L2-Regularized Linear)</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Region / Jurisdiction</label>
            <select
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              className="filter-select form-input"
            >
              {regions.map((r) => (
                <option key={r} value={r}>
                  {r}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Target Forecasting Year</label>
            <input
              type="number"
              min={2018}
              max={2030}
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Crime Category</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="filter-select form-input"
            >
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Estimated Population (in Lakhs)</label>
            <input
              type="number"
              min={10}
              max={5000}
              value={population}
              onChange={(e) => setPopulation(Number(e.target.value))}
              className="form-input"
            />
          </div>

          <button
            onClick={handlePredict}
            disabled={loading}
            className="btn btn--primary"
            style={{ width: '100%', marginTop: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}
          >
            {loading ? (
              <>
                <div className="spinner" style={{ width: 16, height: 16 }} />
                Computing Explainable Prediction…
              </>
            ) : (
              <>
                <Brain size={18} /> Run AI Prediction &amp; XAI
              </>
            )}
          </button>

          {error && (
            <div className="alert-card alert-card--warning" style={{ marginTop: '1rem' }}>
              <AlertTriangle size={18} />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Prediction Results & XAI */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {result ? (
            <>
              {/* Primary Estimate Card */}
              <div className="chart-card predict-result-card" style={{ borderLeft: `5px solid ${result.risk_color}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 10 }}>
                  <div>
                    <span className="badge" style={{ background: result.risk_color, color: '#fff', marginBottom: 8 }}>
                      {result.risk_category} Risk Category
                    </span>
                    <h2 style={{ fontSize: '2rem', margin: '4px 0', color: 'var(--text-primary)' }}>
                      {result.estimated_cases.toLocaleString()}{' '}
                      <span style={{ fontSize: '1rem', fontWeight: 400, color: 'var(--text-secondary)' }}>
                        projected cases
                      </span>
                    </h2>
                    <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                      Forecast for {result.region} &bull; {result.crime_category} &bull; Year {result.year}
                    </p>
                  </div>

                  {result.confidence_interval_90 && (
                    <div className="confidence-box">
                      <span className="conf-label">90% Prediction Interval</span>
                      <strong className="conf-range">
                        {result.confidence_interval_90.lower_bound.toLocaleString()} –{' '}
                        {result.confidence_interval_90.upper_bound.toLocaleString()}
                      </strong>
                      <span className="conf-sub">Uncertainty Bounds (Z=1.645)</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Explainable AI (XAI) Waterfall Decomposition */}
              <div className="chart-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                  <h3 className="chart-card__title" style={{ margin: 0, display: 'flex', alignItems: 'center', gap: 8 }}>
                    <Sparkles size={18} color="var(--accent-light)" />
                    Explainable AI (XAI): Feature Attribution Breakdown
                  </h3>
                  <span className="badge badge--info">Local Attribution</span>
                </div>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                  Decomposes the prediction relative to the global historical baseline to explain <em>why</em> the model
                  arrived at this estimated case count.
                </p>

                <div style={{ height: 260, width: '100%' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={waterfallData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis type="number" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                      <YAxis dataKey="name" type="category" stroke="#94a3b8" tick={{ fontSize: 11 }} width={90} />
                      <Tooltip
                        contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                        formatter={(val: any) => [`${Number(val).toLocaleString()} cases`, 'Attribution Force']}
                      />
                      <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                        {waterfallData.map((entry: any, index: number) => (
                          <Cell
                            key={index}
                            fill={
                              entry.direction === 'base'
                                ? '#6366f1'
                                : entry.value >= 0
                                ? '#f97316'
                                : '#22c55e'
                            }
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* "What-If" Policy Intervention Simulator */}
              {policyResult && (
                <div className="chart-card" style={{ border: '1px solid rgba(99, 102, 241, 0.4)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                    <h3 className="chart-card__title" style={{ margin: 0, display: 'flex', alignItems: 'center', gap: 8 }}>
                      <Sliders size={18} color="var(--accent-light)" />
                      "What-If" Policy Intervention Simulator
                    </h3>
                    <span className="badge badge--success">Criminological Elasticity</span>
                  </div>
                  <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                    Simulate how civic and technological interventions could mitigate crime and elevate regional public safety.
                  </p>

                  <div className="policy-sliders-grid" style={{ margin: '1.25rem 0' }}>
                    <div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: 4 }}>
                        <span>Street Illumination Upgrade:</span>
                        <strong style={{ color: '#eab308' }}>+{lightingPct}%</strong>
                      </div>
                      <input
                        type="range"
                        min={0}
                        max={100}
                        value={lightingPct}
                        onChange={(e) => handlePolicyChange(Number(e.target.value), patrolPct, cctvPct)}
                        className="slider"
                        style={{ width: '100%' }}
                      />
                    </div>

                    <div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: 4 }}>
                        <span>Patrol Density Increase:</span>
                        <strong style={{ color: '#38bdf8' }}>+{patrolPct}%</strong>
                      </div>
                      <input
                        type="range"
                        min={0}
                        max={100}
                        value={patrolPct}
                        onChange={(e) => handlePolicyChange(lightingPct, Number(e.target.value), cctvPct)}
                        className="slider"
                        style={{ width: '100%' }}
                      />
                    </div>

                    <div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: 4 }}>
                        <span>Smart CCTV / IoT Coverage:</span>
                        <strong style={{ color: '#a855f7' }}>+{cctvPct}%</strong>
                      </div>
                      <input
                        type="range"
                        min={0}
                        max={100}
                        value={cctvPct}
                        onChange={(e) => handlePolicyChange(lightingPct, patrolPct, Number(e.target.value))}
                        className="slider"
                        style={{ width: '100%' }}
                      />
                    </div>
                  </div>

                  {/* Policy Results Summary Banner */}
                  <div className="policy-results-banner">
                    <div className="policy-stat">
                      <span className="sub">Projected Incident Mitigation</span>
                      <strong style={{ color: '#22c55e', fontSize: '1.4rem' }}>
                        -{policyResult.total_mitigation_pct}%
                      </strong>
                      <span className="desc">~{policyResult.averted_cases.toLocaleString()} cases averted</span>
                    </div>

                    <div className="policy-stat">
                      <span className="sub">Projected Net Cases</span>
                      <strong style={{ color: 'var(--text-primary)', fontSize: '1.4rem' }}>
                        {policyResult.projected_cases.toLocaleString()}
                      </strong>
                      <span className="desc">Reduced from {policyResult.baseline_cases.toLocaleString()}</span>
                    </div>

                    <div className="policy-stat">
                      <span className="sub">Safety Score Impact</span>
                      <strong style={{ color: '#38bdf8', fontSize: '1.4rem' }}>
                        {policyResult.projected_safety_score} / 100
                      </strong>
                      <span className="desc">+{policyResult.safety_gain_points} pts gain</span>
                    </div>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="chart-card empty-state-card" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <Brain size={48} style={{ color: 'var(--accent)', opacity: 0.7, margin: '0 auto 1rem' }} />
              <h3>Awaiting Prediction Parameters</h3>
              <p style={{ color: 'var(--text-secondary)', maxWidth: 420, margin: '0 auto' }}>
                Select a target region, year, crime category, and model architecture, then click{' '}
                <strong>Run AI Prediction</strong> to see estimated cases, Explainable AI (XAI) feature attribution, and What-If policy simulations.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
