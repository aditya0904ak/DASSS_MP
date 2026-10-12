import React from 'react';
import { MapPin, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';

const HeroStatus = ({ 
  decisionStatus, 
  decisionReason, 
  irrigationRequired, 
  telemetryStatus = 'LIVE' 
}) => {
  const isStale = telemetryStatus === 'STALE';
  
  // Resolve recommendation status based on rule engine
  let statusText = decisionStatus;
  if (!statusText) {
    if (isStale) {
      statusText = 'WAITING FOR VALID SENSOR DATA';
    } else if (irrigationRequired === true) {
      statusText = 'IRRIGATION REQUIRED';
    } else if (irrigationRequired === false) {
      statusText = 'IRRIGATION NOT REQUIRED';
    } else {
      statusText = 'WAITING FOR VALID SENSOR DATA';
    }
  }

  const isRequired = statusText === 'IRRIGATION REQUIRED';
  const isWaiting = statusText === 'WAITING FOR VALID SENSOR DATA';
  
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center bg-gradient-to-r from-white to-slate-50 gap-4">
      <div>
        <div className="flex items-center space-x-2 text-xs font-bold text-slate-400 uppercase tracking-wider mb-1.5">
          <MapPin className="w-3.5 h-3.5 text-emerald-600" />
          <span>Zone 01 — Smart Precision Irrigation Field</span>
        </div>
        <div className="flex items-center space-x-3">
          <h2 className="text-xl md:text-2xl font-black text-slate-800">
            System Status: <span className={isStale ? "text-amber-600" : "text-emerald-600"}>{isStale ? "Telemetry Stale" : "Active Monitoring"}</span>
          </h2>
          <span className="inline-flex items-center text-xs font-bold px-2.5 py-0.5 rounded-md bg-slate-100 text-slate-600 border border-slate-200">
            <ShieldCheck className="w-3.5 h-3.5 mr-1 text-emerald-600" />
            Agronomic Rule Engine (&lt;40% Threshold)
          </span>
        </div>
      </div>
      
      <div className="flex items-center space-x-4 bg-white px-5 py-3.5 rounded-xl border border-slate-200/80 shadow-xs">
        <div className={`p-2 rounded-full ${
          isWaiting
            ? 'bg-slate-100 text-slate-500'
            : isRequired 
              ? 'bg-amber-100 text-amber-600' 
              : 'bg-emerald-100 text-emerald-600'
        }`}>
          {isWaiting ? (
            <AlertTriangle className="w-5 h-5 text-amber-500" />
          ) : isRequired ? (
            <AlertTriangle className="w-5 h-5 text-amber-600" />
          ) : (
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
          )}
        </div>
        <div>
          <p className="text-[11px] text-slate-400 font-bold uppercase tracking-wider">
            Current Recommendation
          </p>
          <p className={`font-black text-base tracking-tight ${
            isWaiting 
              ? 'text-amber-700' 
              : isRequired 
                ? 'text-amber-700' 
                : 'text-emerald-700'
          }`}>
            {statusText}
          </p>
          {decisionReason && (
            <p className="text-xs text-slate-500 font-medium mt-0.5 max-w-xs">
              {decisionReason}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default HeroStatus;
