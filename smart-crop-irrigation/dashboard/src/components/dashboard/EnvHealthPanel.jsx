
import React from 'react';
import { Check, AlertCircle } from 'lucide-react';

const HealthItem = ({ label, status }) => {
  const isOptimal = status === 'Optimal' || status === 'Normal';
  return (
    <div className="flex items-center justify-between p-3 rounded-lg border border-slate-100 bg-slate-50">
      <span className="text-sm font-medium text-slate-600">{label}</span>
      <div className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs font-bold ${isOptimal ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>
        {isOptimal ? <Check className="w-3.5 h-3.5" /> : <AlertCircle className="w-3.5 h-3.5" />}
        <span>{status}</span>
      </div>
    </div>
  );
};

const EnvHealthPanel = ({ data }) => {
  const getSoilStatus = (val) => val < 20 ? 'Attention' : val > 60 ? 'Attention' : 'Optimal';
  const getTempStatus = (val) => val > 35 ? 'Attention' : val < 10 ? 'Attention' : 'Normal';
  const getHumStatus = (val) => val < 30 ? 'Attention' : val > 70 ? 'Attention' : 'Normal';

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest mb-6">Environmental Health</h3>
      <div className="space-y-3">
        <HealthItem label="Soil Condition" status={getSoilStatus(data?.soil_moisture)} />
        <HealthItem label="Temperature" status={getTempStatus(data?.temperature)} />
        <HealthItem label="Humidity" status={getHumStatus(data?.humidity)} />
        <HealthItem label="Light Levels" status="Normal" />
      </div>
    </div>
  );
};

export default EnvHealthPanel;
