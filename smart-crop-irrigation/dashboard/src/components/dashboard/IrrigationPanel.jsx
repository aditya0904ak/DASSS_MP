
import React from 'react';
import { Power, Settings2 } from 'lucide-react';

const IrrigationPanel = ({ prediction, lastUpdated }) => {
  if (!prediction) return null;
  const isPumpOn = prediction.pump_prediction === 1;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm h-full flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest">Irrigation Status</h3>
        <Settings2 className="w-4 h-4 text-slate-400" />
      </div>

      <div className="flex-1 flex flex-col items-center justify-center">
        <div className={`w-32 h-32 rounded-full flex items-center justify-center border-4 shadow-inner transition-colors duration-500 ${isPumpOn ? 'border-emerald-100 bg-emerald-50' : 'border-slate-100 bg-slate-50'}`}>
          <Power className={`w-12 h-12 ${isPumpOn ? 'text-emerald-500' : 'text-slate-300'}`} />
        </div>
        
        <div className="mt-6 flex flex-col items-center text-center">
          <div className="flex items-center space-x-2">
            <span className={`h-2.5 w-2.5 rounded-full ${isPumpOn ? 'bg-emerald-500' : 'bg-slate-400'}`}></span>
            <span className="text-2xl font-black tracking-tight text-slate-800">
              PUMP {isPumpOn ? 'ON' : 'OFF'}
            </span>
          </div>
          <p className="text-sm text-slate-500 mt-2 font-medium">System mode: Monitoring Only</p>
        </div>
      </div>

      <div className="mt-6 pt-6 border-t border-slate-100 text-center">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide">Automatic actuator control: Not enabled</p>
      </div>
    </div>
  );
};

export default IrrigationPanel;
