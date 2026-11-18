import { useEffect, useState } from 'react';
import {
  Navigation,
  ShieldCheck,
  AlertTriangle,
  Clock,
  MapPin,
  Moon,
  Sun,
  Sunrise,
  Radio,
  CheckCircle2,
  Sparkles,
  ArrowRight,
  Shield,
  Layers,
} from 'lucide-react';
import { getSafePathNodes, evaluateSafePath } from '../services/api';

interface Waypoint {
  id: string;
  name: string;
  lat: number;
  lng: number;
  dsi: number;
  lighting_index: number;
  cctv_coverage: number;
  has_police_post: boolean;
  type: string;
}

interface RouteMetrics {
  path: string[];
  waypoints: Waypoint[];
  total_distance_km: number;
  estimated_minutes: number;
  average_dsi: number;
  safety_rating: string;
  status_color: string;
  police_stations_count: number;
  hazards: Array<{ node_id: string; name: string; risk_reason: string; dsi: number }>;
  coordinates: [number, number][];
}

interface SafePathResponse {
  origin: Waypoint;
  destination: Waypoint;
  time_of_day: string;
  comparison: {
    safety_gain_pct: number;
    distance_diff_km: number;
    summary: string;
  };
  direct_route: RouteMetrics;
  safe_corridor: RouteMetrics;
}

export default function SafePath() {
  const [nodes, setNodes] = useState<Waypoint[]>([]);
  const [origin, setOrigin] = useState('CP_CENTRAL');
  const [destination, setDestination] = useState('SAKET_DISTRICT');
  const [timeOfDay, setTimeOfDay] = useState('night');

  const [routeResult, setRouteResult] = useState<SafePathResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [evaluating, setEvaluating] = useState(false);
  const [error, setError] = useState('');

  // Dynamic Leaflet import
  const [useMap, setUseMap] = useState(false);
  const [MapModule, setMapModule] = useState<any>(null);

  useEffect(() => {
    async function init() {
      try {
        const [nodeData, leafletMod] = await Promise.all([
          getSafePathNodes(),
          import('react-leaflet').catch(() => null),
        ]);
        setNodes(nodeData.nodes || []);
        if (leafletMod) {
          setMapModule(() => leafletMod);
          setUseMap(true);
        }

        // Run initial evaluation
        const initialRes = await evaluateSafePath({
          origin: 'CP_CENTRAL',
          destination: 'SAKET_DISTRICT',
          time_of_day: 'night',
        });
        setRouteResult(initialRes);
      } catch (err: any) {
        setError(err.message || 'Failed to initialize SafePath engine');
      } finally {
        setLoading(false);
      }
    }
    init();
  }, []);

  const handleEvaluate = async () => {
    if (origin === destination) {
      setError('Origin and destination cannot be identical.');
      return;
    }
    setError('');
    setEvaluating(true);
    try {
      const res = await evaluateSafePath({
        origin,
        destination,
        time_of_day: timeOfDay,
      });
      setRouteResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to evaluate route');
    } finally {
      setEvaluating(false);
    }
  };

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner" /> Initializing SafePath AI Corridor Engine…
      </div>
    );
  }

  return (
    <div className="page">
      {/* Header */}
      <div className="page__header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          <h1 className="page__title">
            <Navigation
              size={30}
              style={{ display: 'inline', verticalAlign: 'middle', marginRight: 10, color: 'var(--accent-light)' }}
            />
            SafePath AI — Dynamic Route & Corridor Engine
          </h1>
          <span className="badge badge--success" style={{ padding: '6px 14px', fontSize: '0.82rem' }}>
            <Sparkles size={14} style={{ marginRight: 4 }} /> Novel Algorithm
          </span>
        </div>
        <p className="page__desc">
          Evaluates multi-modal urban transit paths by fusing municipal street lighting infrastructure, CCTV coverage,
          historical crime density, and time-of-day vulnerability to find risk-minimized safe corridors.
        </p>
      </div>

      {error && (
        <div className="alert-card alert-card--warning" style={{ marginBottom: '1.5rem' }}>
          <AlertTriangle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Control Form Bar */}
      <div className="chart-card" style={{ marginBottom: '2rem', border: '1px solid var(--accent-glow)' }}>
        <div className="safepath-form-grid">
          <div className="form-group">
            <label className="form-label">
              <MapPin size={16} style={{ color: '#22c55e', verticalAlign: 'middle', marginRight: 6 }} />
              Starting Location (Origin)
            </label>
            <select
              value={origin}
              onChange={(e) => setOrigin(e.target.value)}
              className="filter-select form-input"
            >
              {nodes.map((n) => (
                <option key={n.id} value={n.id}>
                  {n.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">
              <MapPin size={16} style={{ color: '#ef4444', verticalAlign: 'middle', marginRight: 6 }} />
              Destination
            </label>
            <select
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              className="filter-select form-input"
            >
              {nodes.map((n) => (
                <option key={n.id} value={n.id}>
                  {n.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Time of Day (Risk Factor)</label>
            <div style={{ display: 'flex', gap: '6px' }}>
              {[
                { id: 'day', label: 'Day', icon: Sun },
                { id: 'dusk', label: 'Dusk', icon: Sunrise },
                { id: 'night', label: 'Night', icon: Moon },
                { id: 'late_night', label: '2 AM+', icon: Radio },
              ].map((t) => (
                <button
                  key={t.id}
                  type="button"
                  onClick={() => setTimeOfDay(t.id)}
                  className={`btn ${timeOfDay === t.id ? 'btn--primary' : 'btn--outline'}`}
                  style={{ flex: 1, padding: '8px 4px', fontSize: '0.8rem', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 4 }}
                >
                  <t.icon size={14} />
                  {t.label}
                </button>
              ))}
            </div>
          </div>

          <div className="form-group" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'flex-end' }}>
            <button
              onClick={handleEvaluate}
              disabled={evaluating}
              className="btn btn--primary"
              style={{ width: '100%', height: '42px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}
            >
              {evaluating ? (
                <>
                  <div className="spinner" style={{ width: 18, height: 18 }} />
                  Calculating Risk Corridors…
                </>
              ) : (
                <>
                  <ShieldCheck size={18} />
                  Evaluate Safe Corridor
                </>
              )}
            </button>
          </div>
        </div>

        <div style={{ marginTop: '1rem', paddingTop: '0.75rem', borderTop: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 10 }}>
          <span style={{ fontSize: '0.86rem', color: 'var(--text-secondary)' }}>
            <strong>Safety Metrics:</strong> Continuous Arterial Illumination &bull; CCTV Monitored Intersections &bull; Police Outposts
          </span>
          <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            Metropolitan Testbed: Central & South Urban NCR Transit Corridor
          </span>
        </div>
      </div>

      {routeResult && (
        <>
          {/* Executive Comparison Banner */}
          <div className="safepath-comparison-banner" style={{ marginBottom: '2rem' }}>
            <div className="safepath-banner-gain">
              <span className="gain-label">Safety Enhancement</span>
              <span className="gain-value">+{routeResult.comparison.safety_gain_pct}%</span>
              <span className="gain-sub">Dynamic Safety Index Gain</span>
            </div>
            <div className="safepath-banner-text">
              <h3>
                <ShieldCheck size={22} style={{ color: '#22c55e', display: 'inline', verticalAlign: 'middle', marginRight: 8 }} />
                AI Safe Corridor Identified
              </h3>
              <p>{routeResult.comparison.summary}</p>
              <div style={{ display: 'flex', gap: '16px', marginTop: '10px', flexWrap: 'wrap' }}>
                <span className="stat-pill">
                  <Clock size={14} /> +{Math.max(1, routeResult.safe_corridor.estimated_minutes - routeResult.direct_route.estimated_minutes)} min transit time
                </span>
                <span className="stat-pill">
                  <Shield size={14} /> {routeResult.safe_corridor.police_stations_count} Police Kiosks on Safe Path vs {routeResult.direct_route.police_stations_count} Direct
                </span>
                <span className="stat-pill">
                  <Layers size={14} /> {routeResult.safe_corridor.hazards.length} Hazards on Safe Path vs {routeResult.direct_route.hazards.length} Direct
                </span>
              </div>
            </div>
          </div>

          {/* Route Comparison Cards */}
          <div className="safepath-routes-grid" style={{ marginBottom: '2rem' }}>
            {/* Direct Route Card */}
            <div className="chart-card route-card route-card--direct">
              <div className="route-card__header">
                <div>
                  <span className="badge badge--warning">Fastest / Standard Path</span>
                  <h3 style={{ marginTop: 6, fontSize: '1.15rem' }}>Direct Shortest Route</h3>
                </div>
                <div className="dsi-meter dsi-meter--warning">
                  <span className="dsi-meter__val">{routeResult.direct_route.average_dsi}</span>
                  <span className="dsi-meter__label">DSI Score</span>
                </div>
              </div>

              <div className="route-stats-row">
                <div>
                  <span className="stat-label">Total Distance</span>
                  <span className="stat-val">{routeResult.direct_route.total_distance_km} km</span>
                </div>
                <div>
                  <span className="stat-label">Est. Travel Time</span>
                  <span className="stat-val">{routeResult.direct_route.estimated_minutes} min</span>
                </div>
                <div>
                  <span className="stat-label">Security Rating</span>
                  <span className="stat-val" style={{ color: '#f97316' }}>{routeResult.direct_route.safety_rating}</span>
                </div>
              </div>

              <div className="route-hazards-panel">
                <h4>Waypoint Risk Diagnostics:</h4>
                {routeResult.direct_route.hazards.length > 0 ? (
                  routeResult.direct_route.hazards.map((h, i) => (
                    <div key={i} className="hazard-pill">
                      <AlertTriangle size={14} style={{ color: '#ef4444', flexShrink: 0 }} />
                      <span><strong>{h.name}:</strong> {h.risk_reason} (DSI: {h.dsi})</span>
                    </div>
                  ))
                ) : (
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No extreme hazard nodes flagged.</p>
                )}
              </div>
            </div>

            {/* Safe Corridor Card */}
            <div className="chart-card route-card route-card--safe">
              <div className="route-card__header">
                <div>
                  <span className="badge badge--success">AI-Optimized Safe Corridor</span>
                  <h3 style={{ marginTop: 6, fontSize: '1.15rem', color: '#818cf8' }}>High-Illumination Safe Path</h3>
                </div>
                <div className="dsi-meter dsi-meter--success">
                  <span className="dsi-meter__val">{routeResult.safe_corridor.average_dsi}</span>
                  <span className="dsi-meter__label">DSI Score</span>
                </div>
              </div>

              <div className="route-stats-row">
                <div>
                  <span className="stat-label">Total Distance</span>
                  <span className="stat-val">{routeResult.safe_corridor.total_distance_km} km</span>
                </div>
                <div>
                  <span className="stat-label">Est. Travel Time</span>
                  <span className="stat-val">{routeResult.safe_corridor.estimated_minutes} min</span>
                </div>
                <div>
                  <span className="stat-label">Security Rating</span>
                  <span className="stat-val" style={{ color: '#22c55e' }}>{routeResult.safe_corridor.safety_rating}</span>
                </div>
              </div>

              <div className="route-hazards-panel">
                <h4>Corridor Protection Features:</h4>
                <div className="hazard-pill hazard-pill--safe">
                  <CheckCircle2 size={14} style={{ color: '#22c55e', flexShrink: 0 }} />
                  <span>Continuous arterial street lighting coverage (&gt; 85% average)</span>
                </div>
                <div className="hazard-pill hazard-pill--safe">
                  <CheckCircle2 size={14} style={{ color: '#22c55e', flexShrink: 0 }} />
                  <span>Active police post monitoring &amp; emergency CCTV integration</span>
                </div>
              </div>
            </div>
          </div>

          {/* Interactive Map */}
          {useMap && MapModule && (
            <div className="chart-card" style={{ marginBottom: '2rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: 10 }}>
                <h3 className="chart-card__title">
                  <MapPin size={20} style={{ display: 'inline', verticalAlign: 'middle', marginRight: 6 }} />
                  SafePath Geospatial Corridor Map
                </h3>
                <div style={{ display: 'flex', gap: 16, fontSize: '0.85rem' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <span style={{ width: 14, height: 4, background: '#f97316', display: 'inline-block', borderRadius: 2 }} /> Direct Path
                  </span>
                  <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <span style={{ width: 14, height: 4, background: '#22c55e', display: 'inline-block', borderRadius: 2 }} /> AI Safe Corridor
                  </span>
                </div>
              </div>

              <div style={{ height: 460, borderRadius: 12, overflow: 'hidden' }}>
                <MapModule.MapContainer
                  center={[28.60, 77.22]}
                  zoom={12}
                  style={{ height: '100%', width: '100%' }}
                  scrollWheelZoom={true}
                >
                  <MapModule.TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  />

                  {/* Direct Path Polyline */}
                  <MapModule.Polyline
                    positions={routeResult.direct_route.coordinates}
                    pathOptions={{ color: '#f97316', weight: 4, dashArray: '8, 8', opacity: 0.8 }}
                  />

                  {/* Safe Path Polyline */}
                  <MapModule.Polyline
                    positions={routeResult.safe_corridor.coordinates}
                    pathOptions={{ color: '#22c55e', weight: 6, opacity: 0.95 }}
                  />

                  {/* Waypoint Markers */}
                  {routeResult.safe_corridor.waypoints.map((wp) => (
                    <MapModule.CircleMarker
                      key={wp.id}
                      center={[wp.lat, wp.lng]}
                      radius={wp.has_police_post ? 9 : 7}
                      pathOptions={{
                        color: wp.dsi > 70 ? '#22c55e' : '#eab308',
                        fillColor: wp.dsi > 70 ? '#22c55e' : '#eab308',
                        fillOpacity: 0.85,
                        weight: 2,
                      }}
                    >
                      <MapModule.Popup>
                        <div style={{ color: '#1e293b', fontSize: '0.85rem', minWidth: 160 }}>
                          <strong>{wp.name}</strong>
                          <br />
                          <strong>DSI Score:</strong> {wp.dsi} / 100
                          <br />
                          <strong>Lighting:</strong> {wp.lighting_index}%
                          <br />
                          <strong>CCTV:</strong> {wp.cctv_coverage}%
                          <br />
                          {wp.has_police_post && <span style={{ color: '#15803d', fontWeight: 'bold' }}>✓ Police Station On-Site</span>}
                        </div>
                      </MapModule.Popup>
                    </MapModule.CircleMarker>
                  ))}
                </MapModule.MapContainer>
              </div>
            </div>
          )}

          {/* Sequential Corridor Waypoints */}
          <div className="chart-card">
            <h3 className="chart-card__title" style={{ marginBottom: '1.25rem' }}>
              Safe Corridor Transit Sequence &amp; Environmental Factors
            </h3>
            <div className="safepath-timeline">
              {routeResult.safe_corridor.waypoints.map((wp, idx) => (
                <div key={wp.id} className="timeline-node">
                  <div className="timeline-marker">
                    <span className="step-num">{idx + 1}</span>
                  </div>
                  <div className="timeline-content">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 6 }}>
                      <h4 style={{ margin: 0, fontSize: '0.95rem' }}>{wp.name}</h4>
                      <span className="badge badge--success">DSI {wp.dsi}</span>
                    </div>
                    <p style={{ margin: '4px 0 0', fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                      Illumination: <strong>{wp.lighting_index}%</strong> &bull; CCTV Coverage: <strong>{wp.cctv_coverage}%</strong>
                      {wp.has_police_post ? ' &bull; 🛡 Active Police Post' : ''}
                    </p>
                  </div>
                  {idx < routeResult.safe_corridor.waypoints.length - 1 && (
                    <ArrowRight size={18} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
                  )}
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
