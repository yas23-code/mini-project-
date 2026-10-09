import { useEffect, useState, useCallback } from 'react';
import {
  Radio, Eye, Sun, Volume2, AlertOctagon, Zap, AlertTriangle,
  Bell, Activity, RefreshCw
} from 'lucide-react';
import { getSensorReadings, updateSensors, getAlerts, generateRandomEvent } from '../services/api';

const SEVERITY_COLORS: Record<string, string> = {
  critical: '#ef4444',
  warning: '#f97316',
  info: '#3b82f6',
};

export default function IoTMonitor() {
  const [sensors, setSensors] = useState<any>(null);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [updating, setUpdating] = useState(false);

  // Local form state
  const [pirMotion, setPirMotion] = useState(false);
  const [lightIntensity, setLightIntensity] = useState(50);
  const [soundLevel, setSoundLevel] = useState(30);
  const [sosActive, setSosActive] = useState(false);

  const loadData = useCallback(async () => {
    try {
      const [s, a] = await Promise.all([getSensorReadings(), getAlerts(20)]);
      setSensors(s);
      setAlerts(a);
      setPirMotion(s.pir_motion);
      setLightIntensity(s.light_intensity);
      setSoundLevel(s.sound_level);
      setSosActive(s.sos_active);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleUpdate = async () => {
    setUpdating(true);
    try {
      const result = await updateSensors({
        pir_motion: pirMotion,
        light_intensity: lightIntensity,
        sound_level: soundLevel,
        sos_active: sosActive,
      });
      setSensors(result.sensor_state);
      // Refresh alerts
      const a = await getAlerts(20);
      setAlerts(a);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setUpdating(false);
    }
  };

  const handleRandomEvent = async () => {
    setUpdating(true);
    try {
      const result = await generateRandomEvent();
      if (result.sensor_state) {
        setSensors(result.sensor_state);
        setPirMotion(result.sensor_state.pir_motion);
        setLightIntensity(result.sensor_state.light_intensity);
        setSoundLevel(result.sensor_state.sound_level);
      }
      const a = await getAlerts(20);
      setAlerts(a);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setUpdating(false);
    }
  };

  if (loading) return <div className="page-loading"><div className="spinner" /> Loading IoT data…</div>;
  if (error && !sensors) return (
    <div className="page-error">
      <AlertTriangle size={48} />
      <h2>Error</h2>
      <p>{error}</p>
    </div>
  );

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">
          <Radio size={28} style={{ display: 'inline', verticalAlign: 'middle', marginRight: 8 }} />
          IoT Safety Monitor
        </h1>
        <p className="page__desc">
          Software-simulated ESP32 sensors. All values are generated in software — no physical hardware connected.
        </p>
      </div>

      <div className="iot-layout">
        {/* Sensor Controls */}
        <div className="chart-card iot-controls">
          <h3 className="chart-card__title">
            <Activity size={18} /> Sensor Controls (Simulated)
          </h3>

          {/* PIR Motion Toggle */}
          <div className="sensor-control">
            <div className="sensor-control__header">
              <Eye size={18} />
              <span>PIR Motion Detection</span>
            </div>
            <label className="toggle">
              <input
                type="checkbox"
                checked={pirMotion}
                onChange={(e) => setPirMotion(e.target.checked)}
              />
              <span className="toggle__slider" />
            </label>
            <span className={`sensor-status ${pirMotion ? 'sensor-status--on' : ''}`}>
              {pirMotion ? 'Motion Detected' : 'No Motion'}
            </span>
          </div>

          {/* Light Intensity Slider */}
          <div className="sensor-control">
            <div className="sensor-control__header">
              <Sun size={18} />
              <span>Ambient Light Intensity</span>
            </div>
            <input
              type="range"
              min={0}
              max={100}
              value={lightIntensity}
              onChange={(e) => setLightIntensity(+e.target.value)}
              className="sensor-slider"
            />
            <div className="sensor-slider__labels">
              <span>Dark (0)</span>
              <span className="sensor-slider__value">{lightIntensity}%</span>
              <span>Bright (100)</span>
            </div>
            {lightIntensity < 20 && (
              <span className="sensor-warning">⚠ Low light — area may be unsafe</span>
            )}
          </div>

          {/* Sound Level Slider */}
          <div className="sensor-control">
            <div className="sensor-control__header">
              <Volume2 size={18} />
              <span>Sound Level</span>
            </div>
            <input
              type="range"
              min={0}
              max={100}
              value={soundLevel}
              onChange={(e) => setSoundLevel(+e.target.value)}
              className="sensor-slider"
            />
            <div className="sensor-slider__labels">
              <span>Quiet (0)</span>
              <span className="sensor-slider__value">{soundLevel} dB</span>
              <span>Loud (100)</span>
            </div>
            {soundLevel > 75 && (
              <span className="sensor-warning">⚠ High noise level detected</span>
            )}
          </div>

          {/* SOS Button */}
          <div className="sensor-control">
            <div className="sensor-control__header">
              <AlertOctagon size={18} />
              <span>Manual SOS Button</span>
            </div>
            <button
              className={`btn sos-btn ${sosActive ? 'sos-btn--active' : ''}`}
              onClick={() => setSosActive(!sosActive)}
            >
              {sosActive ? '🚨 SOS ACTIVE — Click to Deactivate' : '🆘 Press SOS'}
            </button>
          </div>

          <div className="iot-actions">
            <button onClick={handleUpdate} className="btn btn--primary" disabled={updating}>
              <Zap size={16} /> {updating ? 'Sending…' : 'Send Sensor Data'}
            </button>
            <button onClick={handleRandomEvent} className="btn btn--secondary" disabled={updating}>
              <RefreshCw size={16} /> Generate Random Event
            </button>
          </div>

          {/* Current Readings */}
          {sensors && (
            <div className="sensor-readings">
              <h4>Current Readings</h4>
              <div className="readings-grid">
                <div className="reading">
                  <span className="reading__label">Motion</span>
                  <span className={`reading__value ${sensors.pir_motion ? 'reading__value--alert' : ''}`}>
                    {sensors.pir_motion ? 'Yes' : 'No'}
                  </span>
                </div>
                <div className="reading">
                  <span className="reading__label">Light</span>
                  <span className={`reading__value ${sensors.light_intensity < 20 ? 'reading__value--alert' : ''}`}>
                    {sensors.light_intensity}%
                  </span>
                </div>
                <div className="reading">
                  <span className="reading__label">Sound</span>
                  <span className={`reading__value ${sensors.sound_level > 75 ? 'reading__value--alert' : ''}`}>
                    {sensors.sound_level} dB
                  </span>
                </div>
                <div className="reading">
                  <span className="reading__label">SOS</span>
                  <span className={`reading__value ${sensors.sos_active ? 'reading__value--critical' : ''}`}>
                    {sensors.sos_active ? 'ACTIVE' : 'Inactive'}
                  </span>
                </div>
              </div>
              <p className="text-muted" style={{ fontSize: '0.75rem', marginTop: '0.5rem' }}>
                {sensors.note}
              </p>
            </div>
          )}
        </div>

        {/* Alert History */}
        <div className="chart-card iot-alerts">
          <h3 className="chart-card__title">
            <Bell size={18} /> Alert History
            <span className="alert-count">{alerts.length}</span>
          </h3>
          <div className="alert-timeline">
            {alerts.length === 0 ? (
              <p className="text-muted">No alerts yet. Trigger a sensor event to generate one.</p>
            ) : (
              alerts.map((a) => (
                <div
                  key={a.id}
                  className="alert-timeline__item"
                  style={{ borderLeftColor: SEVERITY_COLORS[a.severity] || '#6366f1' }}
                >
                  <div className="alert-timeline__header">
                    <span
                      className="severity-dot"
                      style={{ background: SEVERITY_COLORS[a.severity] }}
                    />
                    <span className="alert-timeline__type">{a.type.replace(/_/g, ' ')}</span>
                    <span
                      className="alert-timeline__severity"
                      style={{ color: SEVERITY_COLORS[a.severity] }}
                    >
                      {a.severity.toUpperCase()}
                    </span>
                  </div>
                  <p className="alert-timeline__msg">{a.message}</p>
                  <p className="alert-timeline__time">{new Date(a.timestamp).toLocaleString()}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
