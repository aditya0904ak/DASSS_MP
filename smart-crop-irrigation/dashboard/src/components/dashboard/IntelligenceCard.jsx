
import React from 'react';
import { BrainCircuit } from 'lucide-react';

const IntelligenceCard = ({ prediction, sensorData }) => {
  if (!prediction) return null;

  const isReq = prediction.irrigation_required;
  const confidencePct = (prediction.confidence * 100).toFixed(0);
  
  return (
    <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-xl flex flex-col h-full text-white relative overflow-hidden">
      {/* Decorative bg element */}
      <div className="absolute -right-10 -top-10 w-40 h-40 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="flex items-center justify-between mb-8 relative z-10">
        <h3 className="text-lg font-bold flex items-center text-slate-200">
          <BrainCircuit className="w-5 h-5 mr-2 text-emerald-400" />
          AI Irrigation Intelligence
        </h3>
        <span className="text-[10px] font-bold uppercase tracking-widest text-slate-500 bg-slate-800 px-2 py-1 rounded">Decision Engine</span>
      </div>

      <div className="flex-1 flex flex-col items-center justify-center relative z-10 mb-8">
        <div className={`text-center py-6 px-8 rounded-2xl w-full border ${isReq ? 'bg-amber-500/10 border-amber-500/30' : 'bg-emerald-500/10 border-emerald-500/30'}`}>
          <p className="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-2">Recommendation</p>
          <h2 className={`text-2xl md:text-3xl font-black uppercase tracking-tight ${isReq ? 'text-amber-400' : 'text-emerald-400'}`}>
            {isReq ? 'Irrigation Recommended' : 'Irrigation Not Required'}
          </h2>
        </div>
        
        <div className="mt-8 flex items-center justify-center space-x-6 w-full">
          <div className="relative w-20 h-20 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
              <path className="text-slate-800" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" />
              <path className="text-emerald-500 transition-all duration-1000 ease-out" strokeDasharray={`${confidencePct}, 100`} d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" />
            </svg>
            <div className="absolute flex flex-col items-center justify-center">
              <span className="text-lg font-bold">{confidencePct}%</span>
            </div>
          </div>
          <div>
            <p className="text-sm font-bold text-slate-300">Confidence Score</p>
            <p className="text-xs text-slate-500 mt-1">Based on current environmental conditions</p>
          </div>
        </div>
      </div>

      <div className="relative z-10 pt-6 border-t border-slate-800">
        <p className="text-xs text-slate-500 font-medium uppercase tracking-widest mb-4">Model Inputs</p>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-slate-800/50 rounded-lg p-3">
            <p className="text-xs text-slate-400">Soil Moisture</p>
            <p className="text-sm font-bold text-white mt-1">{sensorData?.soil_moisture}%</p>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-3">
            <p className="text-xs text-slate-400">Temperature</p>
            <p className="text-sm font-bold text-white mt-1">{sensorData?.temperature}°C</p>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-3">
            <p className="text-xs text-slate-400">Humidity</p>
            <p className="text-sm font-bold text-white mt-1">{sensorData?.humidity}%</p>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-3">
            <p className="text-xs text-slate-400">Light Intensity</p>
            <p className="text-sm font-bold text-white mt-1">{sensorData?.light} lx</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IntelligenceCard;
