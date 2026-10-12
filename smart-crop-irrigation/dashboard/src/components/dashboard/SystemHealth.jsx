import React from 'react';

const HealthIndicator = ({ name, isOnline, statusLabel, isStale }) => {
  let dotColor = 'bg-red-500';
  let textColor = 'text-red-700';
  let label = 'Offline';

  if (isOnline) {
    if (isStale) {
      dotColor = 'bg-amber-500';
      textColor = 'text-amber-700';
      label = statusLabel || 'Stale (>120s)';
    } else {
      dotColor = 'bg-emerald-500';
      textColor = 'text-emerald-700';
      label = statusLabel || 'Online (Active)';
    }
  }

  return (
    <div className="flex items-center justify-between text-xs">
      <span className="font-medium text-slate-600">{name}</span>
      <div className="flex items-center space-x-1.5">
        <span className={`h-2 w-2 rounded-full ${dotColor}`}></span>
        <span className={`font-bold ${textColor}`}>{label}</span>
      </div>
    </div>
  );
};

const SystemHealth = ({ 
  backendStatus = true, 
  thingspeakStatus = true, 
  modelLoaded = true,
  telemetryFreshness = 'LIVE' 
}) => {
  const isStale = telemetryFreshness === 'STALE';

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <div className="flex justify-between items-center mb-5">
        <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest">
          System Infrastructure
        </h3>
        <span className="text-[10px] font-mono text-slate-400">CH #3523427</span>
      </div>
      <div className="space-y-3.5">
        <HealthIndicator 
          name="FastAPI Backend" 
          isOnline={backendStatus} 
          statusLabel="Operational" 
        />
        <HealthIndicator 
          name="ML Inference Engine" 
          isOnline={backendStatus && modelLoaded} 
          statusLabel="Decision Tree Ready" 
        />
        <HealthIndicator 
          name="ThingSpeak Channel" 
          isOnline={thingspeakStatus} 
          isStale={isStale}
          statusLabel={isStale ? "Stale (>120s)" : "Receiving Feeds"} 
        />
        <HealthIndicator 
          name="Wokwi ESP32 Uplink" 
          isOnline={thingspeakStatus} 
          isStale={isStale}
          statusLabel={isStale ? "Delayed" : "Synchronized"} 
        />
      </div>
    </div>
  );
};

export default SystemHealth;
