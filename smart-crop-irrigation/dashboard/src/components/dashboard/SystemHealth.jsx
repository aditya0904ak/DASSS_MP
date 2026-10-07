
import React from 'react';

const HealthIndicator = ({ name, isOnline }) => (
  <div className="flex items-center justify-between">
    <span className="text-sm font-medium text-slate-600">{name}</span>
    <div className="flex items-center space-x-2">
      <span className={`h-2 w-2 rounded-full ${isOnline ? 'bg-emerald-500' : 'bg-red-500'}`}></span>
      <span className={`text-xs font-bold ${isOnline ? 'text-emerald-700' : 'text-red-600'}`}>{isOnline ? 'Connected' : 'Offline'}</span>
    </div>
  </div>
);

const SystemHealth = ({ backendStatus, thingspeakStatus }) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest mb-6">System Health</h3>
      <div className="space-y-4">
        <HealthIndicator name="ThingSpeak API" isOnline={thingspeakStatus} />
        <HealthIndicator name="FastAPI Backend" isOnline={backendStatus} />
        <HealthIndicator name="ML Engine" isOnline={backendStatus} />
        <HealthIndicator name="Telemetry Sync" isOnline={thingspeakStatus && backendStatus} />
      </div>
    </div>
  );
};

export default SystemHealth;
