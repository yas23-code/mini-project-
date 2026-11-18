const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

async function fetchJSON(url: string, options?: RequestInit) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

// ── Dashboard ────────────────────────────────────────────────
export const getDashboardStats = () => fetchJSON(`${API_BASE}/dashboard/stats`);
export const getYearlyTrends = () => fetchJSON(`${API_BASE}/dashboard/trends`);
export const getRegionComparison = () => fetchJSON(`${API_BASE}/dashboard/region-comparison`);
export const getCategoryBreakdown = () => fetchJSON(`${API_BASE}/dashboard/category-breakdown`);

// ── Crime Data ───────────────────────────────────────────────
export const getCrimeRecords = (params?: Record<string, string>) => {
  const qs = params ? '?' + new URLSearchParams(params).toString() : '';
  return fetchJSON(`${API_BASE}/crime/records${qs}`);
};
export const getRegions = () => fetchJSON(`${API_BASE}/crime/regions`);
export const getCategories = () => fetchJSON(`${API_BASE}/crime/categories`);
export const getHotspots = () => fetchJSON(`${API_BASE}/crime/hotspots`);

// ── ML Prediction & Explainable AI (XAI) ─────────────────────
export const predictCrime = (data: {
  region: string;
  year: number;
  crime_category: string;
  population_lakhs: number;
  model_name?: string;
}) =>
  fetchJSON(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

export const getModelMetrics = () => fetchJSON(`${API_BASE}/model/metrics`);
export const getModelBenchmark = () => fetchJSON(`${API_BASE}/model/benchmark`);

export const simulatePolicy = (data: {
  base_cases: number;
  lighting_improvement_pct?: number;
  patrol_density_increase_pct?: number;
  smart_cctv_coverage_pct?: number;
}) =>
  fetchJSON(`${API_BASE}/policy/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

// ── SafePath AI Corridor Engine ──────────────────────────────
export const getSafePathNodes = () => fetchJSON(`${API_BASE}/safepath/nodes`);

export const evaluateSafePath = (data: {
  origin: string;
  destination: string;
  time_of_day?: string;
}) =>
  fetchJSON(`${API_BASE}/safepath/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

// ── Smart Patrol Resource Optimizer ──────────────────────────
export const optimizePatrolFleet = (fleet_size: number = 30) =>
  fetchJSON(`${API_BASE}/patrol/optimize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fleet_size }),
  });

export const dispatchEmergencyPatrol = (data: {
  alert_type: string;
  target_zone: string;
  severity?: string;
}) =>
  fetchJSON(`${API_BASE}/patrol/dispatch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

export const getRecentDispatches = (limit: number = 10) =>
  fetchJSON(`${API_BASE}/patrol/dispatches?limit=${limit}`);

// ── System Health ────────────────────────────────────────────
export const healthCheck = () => fetchJSON(`${API_BASE}/health`);
