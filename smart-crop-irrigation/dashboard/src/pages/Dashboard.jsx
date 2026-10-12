import React, { useState, useEffect, useRef, useCallback } from 'react';
import Sidebar from '../components/layout/Sidebar';
import TopHeader from '../components/layout/TopHeader';
import HeroStatus from '../components/dashboard/HeroStatus';
import KPICards from '../components/dashboard/KPICards';
import MainChart from '../components/dashboard/MainChart';
import IntelligenceCard from '../components/dashboard/IntelligenceCard';
import IrrigationPanel from '../components/dashboard/IrrigationPanel';
import EnvHealthPanel from '../components/dashboard/EnvHealthPanel';
import ActivityLog from '../components/dashboard/ActivityLog';
import SystemHealth from '../components/dashboard/SystemHealth';
import { DashboardSkeleton } from '../components/ui/Skeleton';
import { getDashboardSummary, getTelemetryHistory } from '../services/api';
import { AlertCircle, WifiOff } from 'lucide-react';

const POLL_INTERVAL_MS = 20000; // 20 seconds (matches ThingSpeak rate limit)

const Dashboard = () => {
  const [currentData, setCurrentData] = useState(null);
  const [history, setHistory] = useState([]);
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [lastPolledAt, setLastPolledAt] = useState(null);
  
  const [sysStatus, setSysStatus] = useState({ 
    backend: true, 
    thingspeak: true, 
    modelLoaded: true,
    telemetryFreshness: 'LIVE'
  });
  
  const isMounted = useRef(true);
  const isFetchingRef = useRef(false);

  const addEvent = useCallback((msg, type = 'info') => {
    if (!isMounted.current) return;
    setEvents(prev => [{ time: new Date().toISOString(), message: msg, type }, ...prev].slice(0, 50));
  }, []);

  const fetchHistory = async () => {
    try {
      const histData = await getTelemetryHistory(100);
      if (!isMounted.current) return;
      if (Array.isArray(histData) && histData.length > 0) {
        setHistory(histData);
      }
    } catch (err) {
      console.warn("Failed to fetch historical telemetry:", err);
      addEvent("Historical telemetry fetch degraded", "error");
    }
  };

  const fetchDashboardData = async (isManual = false) => {
    // Prevent overlapping requests
    if (isFetchingRef.current) return;
    isFetchingRef.current = true;

    if (isManual) setIsRefreshing(true);
    
    try {
      const data = await getDashboardSummary();
      if (!isMounted.current) return;
      
      setError(null);
      setLastPolledAt(new Date().toISOString());

      const freshness = data.system?.status || 'STALE';
      const modelLoaded = data.system?.model_loaded !== false;

      setSysStatus({ 
        backend: true, 
        thingspeak: true, 
        modelLoaded,
        telemetryFreshness: freshness 
      });

      // Update current telemetry
      setCurrentData(prev => {
        if (!prev || prev.timestamp !== data.timestamp) {
          addEvent(`Telemetry synchronized (${data.timestamp}) — ${freshness}`);
          return data;
        }
        return {
          ...prev,
          system: data.system // Update system state even if feed is same
        };
      });

      // Synchronize latest reading into history array if not present
      if (data.timestamp && data.sensor_data) {
        setHistory(prev => {
          const exists = prev.some(item => item.timestamp === data.timestamp);
          if (exists) return prev;
          const newEntry = {
            timestamp: data.timestamp,
            ...data.sensor_data
          };
          return [...prev, newEntry];
        });
      }

    } catch (err) {
      if (!isMounted.current) return;
      console.error("Dashboard fetch error:", err);
      
      const status = err.response?.status;
      if (status === 400) {
        const detail = err.response?.data?.detail || "Malformed telemetry from ThingSpeak";
        setError(`ThingSpeak Channel Issue: ${detail}`);
        setSysStatus(prev => ({ ...prev, thingspeak: false, telemetryFreshness: 'STALE' }));
        addEvent(`ThingSpeak feed error: ${detail}`, 'error');
      } else if (status === 502) {
        setError("ThingSpeak Gateway Unreachable. Preserving last recorded telemetry.");
        setSysStatus(prev => ({ ...prev, thingspeak: false, telemetryFreshness: 'STALE' }));
        addEvent('ThingSpeak connection timeout / 502', 'error');
      } else if (status === 503) {
        setError("ML Model Not Available on backend. Run training pipeline first.");
        setSysStatus(prev => ({ ...prev, modelLoaded: false }));
        addEvent('ML model file missing (503)', 'error');
      } else {
        setError("Backend Connection Lost. Attempting reconnection...");
        setSysStatus(prev => ({ ...prev, backend: false, thingspeak: false, telemetryFreshness: 'STALE' }));
        addEvent('FastAPI backend unreachable', 'error');
      }
    } finally {
      isFetchingRef.current = false;
      if (isMounted.current) {
        setIsLoading(false);
        setIsRefreshing(false);
      }
    }
  };

  useEffect(() => {
    isMounted.current = true;
    addEvent('Dashboard initialized — Connecting to FastAPI backend');
    
    const init = async () => {
      await fetchHistory();
      await fetchDashboardData();
    };
    
    init();
    
    const interval = setInterval(() => {
      fetchDashboardData(false);
    }, POLL_INTERVAL_MS);

    return () => {
      isMounted.current = false;
      clearInterval(interval);
    };
  }, [addEvent]);

  if (isLoading) {
    return (
      <div className="flex h-screen bg-slate-50">
        <Sidebar isBackendOnline={false} isThingSpeakOnline={false} />
        <div className="flex-1 flex flex-col md:ml-64">
          <TopHeader isRefreshing={true} />
          <div className="flex-1 overflow-auto">
            <DashboardSkeleton />
          </div>
        </div>
      </div>
    );
  }

  const { sensor_data, prediction, irrigation_decision, timestamp, system } = currentData || {};
  const isStale = (system?.status === 'STALE') || (sysStatus.telemetryFreshness === 'STALE');
  
  const hasMoisture = typeof sensor_data?.soil_moisture === 'number' && Number.isFinite(sensor_data.soil_moisture);
  const moistureVal = hasMoisture ? sensor_data.soil_moisture : null;
  const threshold = irrigation_decision?.threshold ?? prediction?.moisture_threshold ?? 40.0;
  
  // Rule-based decision status & reason
  let decisionStatus = irrigation_decision?.status;
  let decisionReason = irrigation_decision?.reason;

  if (!decisionStatus) {
    if (isStale || !hasMoisture) {
      decisionStatus = 'WAITING FOR VALID SENSOR DATA';
      decisionReason = isStale 
        ? 'Telemetry reading is older than 120s (STALE). Waiting for fresh feed.' 
        : 'Soil moisture reading is missing or invalid.';
    } else if (moistureVal < threshold) {
      decisionStatus = 'IRRIGATION REQUIRED';
      decisionReason = `Soil moisture is ${moistureVal}%, below the ${threshold}% threshold.`;
    } else {
      decisionStatus = 'IRRIGATION NOT REQUIRED';
      decisionReason = `Soil moisture is ${moistureVal}%, meeting the configured ${threshold}% threshold.`;
    }
  }

  const isIrrigationRequired = decisionStatus === 'IRRIGATION REQUIRED';

  return (
    <div className="flex h-screen bg-[#F8FAFC] overflow-hidden">
      <Sidebar 
        isBackendOnline={sysStatus.backend} 
        isThingSpeakOnline={sysStatus.thingspeak}
        isStale={isStale}
      />
      
      <div className="flex-1 flex flex-col md:ml-64 overflow-hidden h-screen">
        <TopHeader 
          lastUpdated={timestamp} 
          backendStatus={system?.status || sysStatus.telemetryFreshness}
          lastPolledAt={lastPolledAt}
          isRefreshing={isRefreshing} 
          onRefresh={() => fetchDashboardData(true)} 
        />
        
        <main className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 pb-20">
          
          {/* Error Banner if any service drops */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-2xl p-4 text-red-800 flex items-start space-x-3 shadow-xs">
              <WifiOff className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-bold">Service Notice: </span>
                <span>{error}</span>
                <p className="text-xs text-red-600 mt-1">
                  Cached telemetry values are retained on screen. Automatic reconnection will retry every 20 seconds.
                </p>
              </div>
            </div>
          )}

          {/* Low Moisture Alert Banner (<40%) */}
          {isIrrigationRequired && (
            <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 text-amber-900 flex items-start justify-between shadow-2xs">
              <div className="flex items-start space-x-3">
                <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-amber-900">
                    IRRIGATION REQUIRED: Soil moisture is {moistureVal}%, below the configured {threshold}% threshold.
                  </h4>
                  <p className="text-xs text-amber-700 mt-1">
                    Agronomic threshold policy triggered. Field watering is required.
                  </p>
                </div>
              </div>
              <span className="text-[10px] font-bold uppercase tracking-wider bg-amber-100 text-amber-800 border border-amber-200 px-2.5 py-1 rounded-md hidden sm:inline flex-shrink-0 ml-4">
                &lt;{threshold}% Rule
              </span>
            </div>
          )}

          {/* Stale Warning Banner if telemetry exceeds 120s */}
          {isStale && !error && (
            <div className="bg-amber-50/90 border border-amber-200 rounded-2xl p-3.5 text-amber-800 flex items-center justify-between text-xs font-medium shadow-2xs">
              <div className="flex items-center space-x-2">
                <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0" />
                <span>
                  Telemetry reading is older than 120s (Status: <strong>STALE</strong>). Waiting for new feed from Wokwi ESP32.
                </span>
              </div>
              <span className="font-mono text-amber-700 hidden sm:inline">CH #3523427</span>
            </div>
          )}

          <HeroStatus 
            decisionStatus={decisionStatus}
            decisionReason={decisionReason}
            irrigationRequired={isIrrigationRequired} 
            telemetryStatus={system?.status || sysStatus.telemetryFreshness}
          />

          <KPICards 
            data={sensor_data} 
            isStale={isStale}
          />

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            <div className="xl:col-span-2">
              <MainChart history={history} />
            </div>
            <div className="xl:col-span-1">
              <IntelligenceCard 
                decision={irrigation_decision}
                prediction={prediction} 
                sensorData={sensor_data} 
                timestamp={timestamp}
                isStale={isStale}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
            <div className="xl:col-span-1">
              <IrrigationPanel 
                decision={irrigation_decision}
                prediction={prediction} 
              />
            </div>
            <div className="xl:col-span-1">
              <EnvHealthPanel data={sensor_data} />
            </div>
            <div className="xl:col-span-1">
              <SystemHealth 
                backendStatus={sysStatus.backend} 
                thingspeakStatus={sysStatus.thingspeak} 
                modelLoaded={sysStatus.modelLoaded}
                telemetryFreshness={system?.status || sysStatus.telemetryFreshness}
              />
            </div>
            <div className="xl:col-span-1">
              <ActivityLog events={events} />
            </div>
          </div>

        </main>
      </div>
    </div>
  );
};

export default Dashboard;
