import React from 'react';
import { ShieldCheck, Info, Clock, AlertTriangle, CheckCircle2, Droplets } from 'lucide-react';
import { format, parseISO } from 'date-fns';

const IntelligenceCard = ({ decision, prediction, sensorData, timestamp, isStale }) => {
  const threshold = decision?.threshold ?? prediction?.moisture_threshold ?? 40.0;
  const hasMoisture = typeof sensorData?.soil_moisture === 'number' && Number.isFinite(sensorData.soil_moisture);
  const moistureVal = hasMoisture ? sensorData.soil_moisture : null;

  // Derive rule-based decision
  let statusText = decision?.status;
  let reasonText = decision?.reason;

  if (!statusText) {
    if (isStale || !hasMoisture) {
      statusText = 'WAITING FOR VALID SENSOR DATA';
      reasonText = isStale 
        ? 'Telemetry is stale (>120s old). Waiting for fresh sensor feed.' 
        : 'Soil moisture sensor reading is missing or invalid.';
    } else if (moistureVal < threshold) {
      statusText = 'IRRIGATION REQUIRED';
      reasonText = `Soil moisture is ${moistureVal}%, below the ${threshold}% threshold.`;
    } else {
      statusText = 'IRRIGATION NOT REQUIRED';
      reasonText = `Soil moisture is ${moistureVal}%, meeting the configured ${threshold}% threshold.`;
    }
  }

  const isRequired = statusText === 'IRRIGATION REQUIRED';
  const isWaiting = statusText === 'WAITING FOR VALID SENSOR DATA';

  let formattedTime = timestamp || '--';
  try {
    if (timestamp) {
      formattedTime = format(parseISO(timestamp), 'yyyy-MM-dd HH:mm:ss');
    }
  } catch {
    // Keep raw string if parsing fails
  }

  return (
    <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-xl flex flex-col justify-between h-full text-white relative overflow-hidden min-h-[440px]">
      {/* Decorative gradient glow */}
      <div className="absolute -right-10 -top-10 w-44 h-44 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>

      {/* Card Header */}
      <div>
        <div className="flex items-center justify-between mb-3 relative z-10">
          <h3 className="text-base font-bold flex items-center text-slate-200">
            <ShieldCheck className="w-5 h-5 mr-2 text-emerald-400" />
            Decision Engine
          </h3>
          <span className="text-[10px] font-bold uppercase tracking-widest text-emerald-400 bg-emerald-950/60 border border-emerald-800/50 px-2.5 py-1 rounded-md">
            Rule-Based Logic
          </span>
        </div>

        {/* Telemetry Timestamp */}
        <div className="flex items-center text-xs text-slate-400 mb-5 space-x-1.5">
          <Clock className="w-3.5 h-3.5 text-slate-500" />
          <span>Telemetry ref:</span>
          <span className="font-mono text-slate-300">{formattedTime}</span>
        </div>
      </div>

      {/* Primary Recommendation Banner */}
      <div className="relative z-10 my-auto space-y-4">
        <div className={`text-center py-5 px-6 rounded-2xl border transition-all ${
          isWaiting
            ? 'bg-slate-800/60 border-slate-700/80'
            : isRequired 
              ? 'bg-amber-500/10 border-amber-500/30' 
              : 'bg-emerald-500/10 border-emerald-500/30'
        }`}>
          <div className="flex items-center justify-center space-x-2 mb-1.5">
            {isWaiting ? (
              <AlertTriangle className="w-4 h-4 text-amber-400" />
            ) : isRequired ? (
              <Droplets className="w-4 h-4 text-amber-400 animate-pulse" />
            ) : (
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            )}
            <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
              Current Recommendation
            </p>
          </div>
          <h2 className={`text-xl md:text-2xl font-black uppercase tracking-tight ${
            isWaiting
              ? 'text-amber-300'
              : isRequired 
                ? 'text-amber-400' 
                : 'text-emerald-400'
          }`}>
            {statusText}
          </h2>
          <p className="text-xs text-slate-300 mt-2 font-medium max-w-sm mx-auto">
            {reasonText}
          </p>
        </div>

        {/* Deterministic Rule Policy Overview */}
        <div className="p-3.5 rounded-xl bg-slate-800/50 border border-slate-800 text-xs text-slate-300 space-y-2">
          <div className="flex items-center justify-between text-[11px]">
            <span className="font-semibold text-slate-400">Decision Parameter:</span>
            <span className="font-bold text-white">Soil Moisture (&lt;{threshold}% Rule)</span>
          </div>
          <div className="flex items-center justify-between text-[11px]">
            <span className="font-semibold text-slate-400">Current Measured Value:</span>
            <span className={`font-mono font-bold ${hasMoisture && moistureVal < threshold ? 'text-amber-400' : 'text-emerald-400'}`}>
              {hasMoisture ? `${moistureVal}%` : 'Unavailable'}
            </span>
          </div>
          <div className="flex items-center justify-between text-[11px]">
            <span className="font-semibold text-slate-400">Threshold Status:</span>
            <span className="text-slate-300">
              {hasMoisture 
                ? (moistureVal < threshold ? `Below ${threshold}% limit` : `Meets ${threshold}% limit`) 
                : 'Pending sensor stream'}
            </span>
          </div>
        </div>
      </div>

      {/* Sensor Monitoring Parameters & Read-Only Notice */}
      <div className="relative z-10 pt-3 border-t border-slate-800/80 text-xs">
        <div className="flex items-center justify-between text-slate-400 mb-2">
          <span className="font-semibold uppercase tracking-wider text-[10px]">Environmental Monitoring Parameters</span>
          {isStale && <span className="text-[10px] text-amber-400 font-bold">Stale telemetry</span>}
        </div>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="bg-slate-800/60 rounded-lg px-2.5 py-1.5 flex justify-between">
            <span className="text-slate-400">Moisture:</span>
            <span className={`font-bold ${hasMoisture && moistureVal < threshold ? 'text-amber-400' : 'text-white'}`}>
              {hasMoisture ? `${moistureVal}%` : '--'}
            </span>
          </div>
          <div className="bg-slate-800/60 rounded-lg px-2.5 py-1.5 flex justify-between">
            <span className="text-slate-400">Temp:</span>
            <span className="font-bold text-white">{sensorData?.temperature ?? '--'}°C</span>
          </div>
          <div className="bg-slate-800/60 rounded-lg px-2.5 py-1.5 flex justify-between">
            <span className="text-slate-400">Humidity:</span>
            <span className="font-bold text-white">{sensorData?.humidity ?? '--'}%</span>
          </div>
          <div className="bg-slate-800/60 rounded-lg px-2.5 py-1.5 flex justify-between">
            <span className="text-slate-400">LDR (ADC):</span>
            <span className="font-bold text-white">{sensorData?.light ?? '--'}</span>
          </div>
        </div>

        <p className="text-[10px] text-slate-500 mt-2.5 flex items-center">
          <Info className="w-3 h-3 mr-1 flex-shrink-0 text-slate-400" />
          Advisory recommendation only; physical Wokwi pump is read-only.
        </p>
      </div>
    </div>
  );
};

export default IntelligenceCard;
