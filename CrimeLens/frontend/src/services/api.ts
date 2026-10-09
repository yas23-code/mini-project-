const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

async function fetchJSON(url: string, options?: RequestInit) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

// Dashboard
export const getDashboardStats = () => fetchJSON(`${API_BASE}/dashboard/stats`);
export const getYearlyTrends = () => fetchJSON(`${API_BASE}/dashboard/trends`);
export const getRegionComparison = () => fetchJSON(`${API_BASE}/dashboard/region-comparison`);
export const getCategoryBreakdown = () => fetchJSON(`${API_BASE}/dashboard/category-breakdown`);

// Crime data
export const getCrimeRecords = (params?: Record<string, string>) => {
  const qs = params ? '?' + new URLSearchParams(params).toString() : '';
  return fetchJSON(`${API_BASE}/crime/records${qs}`);
};
export const getRegions = () => fetchJSON(`${API_BASE}/crime/regions`);
export const getCategories = () => fetchJSON(`${API_BASE}/crime/categories`);
export const getHotspots = () => fetchJSON(`${API_BASE}/crime/hotspots`);

// ML Prediction
export const predictCrime = (data: {
  region: string;
  year: number;
  crime_category: string;
  population_lakhs: number;
}) =>
  fetchJSON(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

export const getModelMetrics = () => fetchJSON(`${API_BASE}/model/metrics`);

// IoT Simulator
export const getSensorReadings = () => fetchJSON(`${API_BASE}/iot/sensors`);
export const updateSensors = (data: {
  pir_motion?: boolean;
  light_intensity?: number;
  sound_level?: number;
  sos_active?: boolean;
}) =>
  fetchJSON(`${API_BASE}/iot/sensors`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

export const getAlerts = (limit = 50) => fetchJSON(`${API_BASE}/iot/alerts?limit=${limit}`);
export const generateRandomEvent = () =>
  fetchJSON(`${API_BASE}/iot/random-event`, { method: 'POST' });

// Health
export const healthCheck = () => fetchJSON(`${API_BASE}/health`);
