import React from 'react';
import { Check, AlertCircle } from 'lucide-react';

const HealthItem = ({ label, status, isOptimal }) => {
  return (
    <div className="flex items-center justify-between p-3 rounded-lg border border-slate-100 bg-slate-50">
      <span className="text-sm font-medium text-slate-600">{label}</span>
      <div className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs font-bold ${
        isOptimal ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
      }`}>
        {isOptimal ? <Check className="w-3.5 h-3.5" /> : <AlertCircle className="w-3.5 h-3.5" />}
        <span>{status}</span>
      </div>
    </div>
  );
};

const EnvHealthPanel = ({ data }) => {
  const getSoil = (val) => {
    if (val == null) return { status: 'Awaiting', optimal: false };
    if (val < 40) return { status: 'Dry (<40% Threshold)', optimal: false };
    if (val > 60) return { status: 'Over-watered', optimal: false };
    return { status: 'Optimal (40-60%)', optimal: true };
  };

  const getTemp = (val) => {
    if (val == null) return { status: 'Awaiting', optimal: false };
    if (val > 35) return { status: 'Thermal Stress', optimal: false };
    if (val < 15) return { status: 'Cool Ambient', optimal: false };
    return { status: 'Optimal (15-35°C)', optimal: true };
  };

  const getHum = (val) => {
    if (val == null) return { status: 'Awaiting', optimal: false };
    if (val < 30) return { status: 'Dry Air Stress', optimal: false };
    if (val > 70) return { status: 'High Humidity', optimal: false };
    return { status: 'Optimal (30-70%)', optimal: true };
  };

  const getLight = (val) => {
    if (val == null) return { status: 'Awaiting', optimal: false };
    if (val < 500) return { status: 'Low ADC Level', optimal: true };
    if (val > 3000) return { status: 'High ADC Level', optimal: true };
    return { status: 'Moderate ADC Level', optimal: true };
  };

  const soil = getSoil(data?.soil_moisture);
  const temp = getTemp(data?.temperature);
  const hum = getHum(data?.humidity);
  const light = getLight(data?.light);

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest mb-6">Environmental Health</h3>
      <div className="space-y-3">
        <HealthItem label="Soil Moisture" status={soil.status} isOptimal={soil.optimal} />
        <HealthItem label="Temperature" status={temp.status} isOptimal={temp.optimal} />
        <HealthItem label="Humidity" status={hum.status} isOptimal={hum.optimal} />
        <HealthItem label="LDR Sensor (ADC)" status={light.status} isOptimal={light.optimal} />
      </div>
    </div>
  );
};

export default EnvHealthPanel;
