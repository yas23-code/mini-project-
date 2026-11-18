import { useEffect, useState } from 'react';
import {
  Car,
  ShieldAlert,
  Send,
  Zap,
  CheckCircle,
  Clock,
  Radio,
  Sparkles,
  Layers,
  ArrowUpRight,
  TrendingDown,
  Compass,
} from 'lucide-react';
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
import { optimizePatrolFleet, dispatchEmergencyPatrol } from '../services/api';

interface ShiftAllocation {
  morning: number;
  evening: number;
  night: number;
}

interface SectorAllocation {
  sector: string;
  vulnerability: string;
  base_cases: number;
  assigned_units: number;
  coverage_pct: number;
  est_response_time_min: number;
  projected_deterrence_gain_pct: number;
  shifts: ShiftAllocation;
}

interface FleetOptimizationResult {
  total_fleet_size: number;
  allocated_units: number;
  sectors_count: number;
  overall_avg_response_time_min: number;
  overall_deterrence_gain_pct: number;
  allocation_breakdown: SectorAllocation[];
  fleet_readiness: {
    active_patrolling: number;
    airborne_drones: number;
    standby_interceptors: number;
  };
  recent_dispatches: any[];
}

export default function PatrolOptimizer() {
  const [fleetSize, setFleetSize] = useState(30);
  const [result, setResult] = useState<FleetOptimizationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [optimizing, setOptimizing] = useState(false);
  const [dispatching, setDispatching] = useState(false);

  // Dispatch simulation form
  const [targetZone, setTargetZone] = useState('Delhi Central (Commercial / Transit)');
  const [alertType, setAlertType] = useState('citizen_distress_call');
  const [severity, setSeverity] = useState('critical');
  const [latestTicket, setLatestTicket] = useState<any>(null);

  const loadOptimization = async (size: number) => {
    try {
      const data = await optimizePatrolFleet(size);
      setResult(data);
      if (data.allocation_breakdown?.length > 0 && !targetZone) {
        setTargetZone(data.allocation_breakdown[0].sector);
      }
    } catch (err: any) {
      console.error(err);
    } finally {
      setLoading(false);
      setOptimizing(false);
    }
  };

  useEffect(() => {
    loadOptimization(fleetSize);
  }, []);

  const handleReoptimize = () => {
    setOptimizing(true);
    loadOptimization(fleetSize);
  };

  const handleDispatch = async () => {
    setDispatching(true);
    try {
      const ticket = await dispatchEmergencyPatrol({
        alert_type: alertType,
        target_zone: targetZone,
        severity,
      });
      setLatestTicket(ticket);
      // Refresh dispatches list
      loadOptimization(fleetSize);
    } catch (err: any) {
      console.error(err);
    } finally {
      setDispatching(false);
    }
  };

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner" /> Calculating Optimal Patrol Resource Distribution…
      </div>
    );
  }

  const chartData = result?.allocation_breakdown.map((s) => ({
    name: s.sector.split(' ')[0],
    fullName: s.sector,
    units: s.assigned_units,
    deterrence: s.projected_deterrence_gain_pct,
    responseTime: s.est_response_time_min,
  })) || [];

  return (
    <div className="page">
      {/* Header */}
      <div className="page__header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          <h1 className="page__title">
            <Car size={30} style={{ display: 'inline', verticalAlign: 'middle', marginRight: 10, color: 'var(--accent-light)' }} />
            Smart Patrol Resource Allocation Optimizer
          </h1>
          <span className="badge badge--success" style={{ padding: '6px 14px', fontSize: '0.82rem' }}>
            <Sparkles size={14} style={{ marginRight: 4 }} /> AI Dispatch Hub
          </span>
        </div>
        <p className="page__desc">
          Dynamically optimizes patrol fleet deployment across high-vulnerability sectors using predicted crime volume,
          spatial risk density, and non-linear response time minimization curves.
        </p>
      </div>

      {/* Fleet Configuration Bar */}
      <div className="chart-card" style={{ marginBottom: '2rem', border: '1px solid var(--accent-glow)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 16 }}>
          <div style={{ flex: 1, minWidth: 260 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <label className="form-label" style={{ marginBottom: 0 }}>
                Total Available Patrol Fleet Size
              </label>
              <strong style={{ color: 'var(--accent-light)', fontSize: '1.1rem' }}>{fleetSize} Units</strong>
            </div>
            <input
              type="range"
              min={10}
              max={100}
              step={5}
              value={fleetSize}
              onChange={(e) => setFleetSize(Number(e.target.value))}
              className="slider"
              style={{ width: '100%' }}
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 4 }}>
              <span>10 Light Fleet</span>
              <span>50 Standard Fleet</span>
              <span>100 Maximum Surge</span>
            </div>
          </div>

          <button
            onClick={handleReoptimize}
            disabled={optimizing}
            className="btn btn--primary"
            style={{ height: '44px', display: 'flex', alignItems: 'center', gap: 8, padding: '0 24px' }}
          >
            {optimizing ? (
              <>
                <div className="spinner" style={{ width: 16, height: 16 }} />
                Optimizing Matrix…
              </>
            ) : (
              <>
                <Compass size={18} />
                Recompute Optimal Allocation
              </>
            )}
          </button>
        </div>
      </div>

      {result && (
        <>
          {/* Key Metric Cards */}
          <div className="stats-grid" style={{ marginBottom: '2rem' }}>
            <div className="stat-card">
              <span className="stat-card__label">Active Fleet Allocated</span>
              <span className="stat-card__value" style={{ color: 'var(--accent-light)' }}>
                {result.allocated_units} / {result.total_fleet_size}
              </span>
              <span className="stat-card__sub">Across {result.sectors_count} tactical sectors</span>
            </div>

            <div className="stat-card">
              <span className="stat-card__label">Avg. Emergency Response Time</span>
              <span className="stat-card__value" style={{ color: '#22c55e' }}>
                {result.overall_avg_response_time_min} min
              </span>
              <span className="stat-card__sub" style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                <TrendingDown size={14} color="#22c55e" /> Reduced from ~18 min baseline
              </span>
            </div>

            <div className="stat-card">
              <span className="stat-card__label">Crime Deterrence Gain</span>
              <span className="stat-card__value" style={{ color: '#38bdf8' }}>
                +{result.overall_deterrence_gain_pct}%
              </span>
              <span className="stat-card__sub">Non-linear visibility deterrence</span>
            </div>

            <div className="stat-card">
              <span className="stat-card__label">Airborne &amp; Rapid Units</span>
              <span className="stat-card__value" style={{ color: '#eab308' }}>
                {result.fleet_readiness.airborne_drones} Drones &bull; {result.fleet_readiness.standby_interceptors} Standby
              </span>
              <span className="stat-card__sub">Ready for tactical emergency routing</span>
            </div>
          </div>

          {/* Allocation Chart & Rapid Dispatch Grid */}
          <div className="dashboard-grid" style={{ marginBottom: '2rem' }}>
            {/* Chart */}
            <div className="chart-card">
              <h3 className="chart-card__title">Units Allocated per Sector</h3>
              <div style={{ height: 300, width: '100%', marginTop: '1rem' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} margin={{ top: 10, right: 10, left: -15, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="name" stroke="#94a3b8" tick={{ fontSize: 12 }} />
                    <YAxis stroke="#94a3b8" tick={{ fontSize: 12 }} />
                    <Tooltip
                      contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                      formatter={(val: any) => [`${val} Units`, 'Patrol Deployment']}
                    />
                    <Bar dataKey="units" fill="#6366f1" radius={[6, 6, 0, 0]}>
                      {chartData.map((_, idx) => (
                        <Cell key={idx} fill={idx % 2 === 0 ? '#6366f1' : '#818cf8'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Live Tactical Dispatch Panel */}
            <div className="chart-card" style={{ border: '1px solid rgba(239, 68, 68, 0.3)' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <h3 className="chart-card__title" style={{ display: 'flex', alignItems: 'center', gap: 8, margin: 0 }}>
                  <ShieldAlert size={20} color="#ef4444" />
                  Tactical Emergency Dispatch
                </h3>
                <span className="badge badge--danger">Live Action</span>
              </div>

              <div className="form-group" style={{ marginBottom: 12 }}>
                <label className="form-label">Target Incident Sector</label>
                <select
                  value={targetZone}
                  onChange={(e) => setTargetZone(e.target.value)}
                  className="filter-select form-input"
                >
                  {result.allocation_breakdown.map((s) => (
                    <option key={s.sector} value={s.sector}>
                      {s.sector}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group" style={{ marginBottom: 12 }}>
                <label className="form-label">Incident Trigger Type</label>
                <select
                  value={alertType}
                  onChange={(e) => setAlertType(e.target.value)}
                  className="filter-select form-input"
                >
                  <option value="citizen_distress_call">Citizen 112 Emergency Distress Call</option>
                  <option value="cctv_ai_intrusion">Automated CCTV Computer Vision Intrusion</option>
                  <option value="commercial_alarm_webhook">Commercial Security Webhook Alarm</option>
                  <option value="spatial_anomaly_spike">Algorithmic Spatial Crime Surge Spike</option>
                </select>
              </div>

              <button
                onClick={handleDispatch}
                disabled={dispatching}
                className="btn btn--danger"
                style={{ width: '100%', height: '42px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, marginTop: 16 }}
              >
                {dispatching ? (
                  <>
                    <div className="spinner" style={{ width: 16, height: 16 }} /> Dispatching Rapid Unit…
                  </>
                ) : (
                  <>
                    <Send size={16} /> Authorize Immediate Tactical Dispatch
                  </>
                )}
              </button>

              {latestTicket && (
                <div className="dispatch-ticket-card" style={{ marginTop: '1.25rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span className="ticket-badge">{latestTicket.ticket_id}</span>
                    <span className="badge badge--danger" style={{ textTransform: 'uppercase' }}>
                      {latestTicket.status}
                    </span>
                  </div>
                  <h4 style={{ margin: '8px 0 4px', fontSize: '0.95rem' }}>{latestTicket.assigned_unit}</h4>
                  <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    Type: {latestTicket.unit_type} &bull; <strong>ETA: {latestTicket.eta_minutes} min</strong>
                  </p>
                  <p style={{ margin: '6px 0 0', fontSize: '0.78rem', color: '#38bdf8', fontStyle: 'italic' }}>
                    {latestTicket.dispatch_protocol}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Allocation Breakdown Table */}
          <div className="chart-card">
            <h3 className="chart-card__title" style={{ marginBottom: '1.25rem' }}>
              Sector Patrol Resource Distribution Matrix &amp; Shift Breakdown
            </h3>
            <div className="table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Sector / Jurisdiction</th>
                    <th>Vulnerability</th>
                    <th>Base Cases</th>
                    <th>Assigned Units</th>
                    <th>Shift Split (M / E / N)</th>
                    <th>Est. Response</th>
                    <th>Deterrence Gain</th>
                  </tr>
                </thead>
                <tbody>
                  {result.allocation_breakdown.map((s, idx) => (
                    <tr key={idx}>
                      <td style={{ fontWeight: 600 }}>{s.sector}</td>
                      <td>
                        <span
                          className={`badge ${s.vulnerability === 'Very High'
                              ? 'badge--danger'
                              : s.vulnerability === 'High'
                                ? 'badge--warning'
                                : 'badge--info'
                            }`}
                        >
                          {s.vulnerability}
                        </span>
                      </td>
                      <td>{s.base_cases.toLocaleString()}</td>
                      <td>
                        <strong style={{ color: 'var(--accent-light)', fontSize: '1rem' }}>
                          {s.assigned_units} Units
                        </strong>{' '}
                        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                          ({s.coverage_pct}%)
                        </span>
                      </td>
                      <td>
                        <span style={{ color: '#38bdf8' }}>{s.shifts.morning} M</span> &bull;{' '}
                        <span style={{ color: '#eab308' }}>{s.shifts.evening} E</span> &bull;{' '}
                        <span style={{ color: '#f87171', fontWeight: 'bold' }}>{s.shifts.night} Night</span>
                      </td>
                      <td style={{ color: '#22c55e', fontWeight: 600 }}>
                        <Clock size={12} style={{ display: 'inline', marginRight: 4 }} />
                        {s.est_response_time_min} min
                      </td>
                      <td style={{ color: '#38bdf8', fontWeight: 600 }}>
                        +{s.projected_deterrence_gain_pct}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
