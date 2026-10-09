import { useEffect, useState } from 'react';
import { MapPin, AlertTriangle } from 'lucide-react';
import { getHotspots } from '../services/api';

const RISK_COLORS: Record<string, string> = {
  Low: '#22c55e',
  Moderate: '#eab308',
  High: '#f97316',
  'Very High': '#ef4444',
};

const RISK_BG: Record<string, string> = {
  Low: 'rgba(34,197,94,0.15)',
  Moderate: 'rgba(234,179,8,0.15)',
  High: 'rgba(249,115,22,0.15)',
  'Very High': 'rgba(239,68,68,0.15)',
};

interface HotspotData {
  region: string;
  total_cases: number;
  risk_level: string;
  latitude: number | null;
  longitude: number | null;
  year: number;
}

export default function Hotspots() {
  const [hotspots, setHotspots] = useState<HotspotData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [useMap, setUseMap] = useState(false);
  const [MapComponent, setMapComponent] = useState<any>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await getHotspots();
        setHotspots(data);
        // Try loading Leaflet map
        try {
          const leafletModule = await import('react-leaflet');
          setMapComponent(() => leafletModule);
          setUseMap(true);
        } catch {
          setUseMap(false);
        }
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <div className="page-loading"><div className="spinner" /> Loading hotspot data…</div>;
  if (error) return (
    <div className="page-error">
      <AlertTriangle size={48} />
      <h2>Error</h2>
      <p>{error}</p>
    </div>
  );

  const maxCases = Math.max(...hotspots.map((h) => h.total_cases));

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">
          <MapPin size={28} style={{ display: 'inline', verticalAlign: 'middle', marginRight: 8 }} />
          Crime Hotspot Visualization
        </h1>
        <p className="page__desc">
          Regions ranked by total recorded cases ({hotspots[0]?.year}). Coordinates are approximate state capitals.
        </p>
      </div>

      {/* Leaflet Map */}
      {useMap && MapComponent && (
        <div className="chart-card" style={{ marginBottom: '1.5rem' }}>
          <h3 className="chart-card__title">Geographic View</h3>
          <div style={{ height: 420, borderRadius: 12, overflow: 'hidden' }}>
            <MapComponent.MapContainer
              center={[22.5, 78.9]}
              zoom={5}
              style={{ height: '100%', width: '100%' }}
              scrollWheelZoom={true}
            >
              <MapComponent.TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              {hotspots
                .filter((h) => h.latitude && h.longitude)
                .map((h) => (
                  <MapComponent.CircleMarker
                    key={h.region}
                    center={[h.latitude!, h.longitude!]}
                    radius={Math.max(8, (h.total_cases / maxCases) * 35)}
                    fillColor={RISK_COLORS[h.risk_level] || '#6366f1'}
                    color={RISK_COLORS[h.risk_level] || '#6366f1'}
                    fillOpacity={0.6}
                    weight={2}
                  >
                    <MapComponent.Popup>
                      <div style={{ color: '#1e293b' }}>
                        <strong>{h.region}</strong><br />
                        Cases: {h.total_cases.toLocaleString()}<br />
                        Risk: {h.risk_level}
                      </div>
                    </MapComponent.Popup>
                  </MapComponent.CircleMarker>
                ))}
            </MapComponent.MapContainer>
          </div>
        </div>
      )}

      {/* Ranked regional cards */}
      <div className="chart-card">
        <h3 className="chart-card__title">Regional Risk Ranking</h3>
        <div className="hotspot-grid">
          {hotspots.map((h, i) => (
            <div
              key={h.region}
              className="hotspot-card"
              style={{ borderLeftColor: RISK_COLORS[h.risk_level], background: RISK_BG[h.risk_level] }}
            >
              <div className="hotspot-card__rank">#{i + 1}</div>
              <div className="hotspot-card__info">
                <h4 className="hotspot-card__name">{h.region}</h4>
                <p className="hotspot-card__cases">{h.total_cases.toLocaleString()} cases</p>
                {h.latitude && h.longitude && (
                  <p className="hotspot-card__coords">
                    {h.latitude.toFixed(2)}°N, {h.longitude.toFixed(2)}°E
                  </p>
                )}
              </div>
              <span
                className="risk-badge"
                style={{ background: RISK_COLORS[h.risk_level] }}
              >
                {h.risk_level}
              </span>
              <div className="hotspot-card__bar">
                <div
                  className="hotspot-card__bar-fill"
                  style={{
                    width: `${(h.total_cases / maxCases) * 100}%`,
                    background: RISK_COLORS[h.risk_level],
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
