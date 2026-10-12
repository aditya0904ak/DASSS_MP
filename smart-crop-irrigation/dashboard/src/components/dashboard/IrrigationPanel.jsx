import React from 'react';
import { Power, Info, Cpu } from 'lucide-react';

const IrrigationPanel = ({ decision, prediction }) => {
  const isRequired = decision?.irrigation_required === true || (!decision && prediction?.irrigation_required === true);
  const isWaiting = decision?.status === 'WAITING FOR VALID SENSOR DATA';

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm h-full flex flex-col justify-between">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
          Irrigation Actuator Output
        </h3>
        <span className="flex items-center text-[10px] font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
          <Cpu className="w-3 h-3 mr-1 text-slate-500" />
          Rule Policy
        </span>
      </div>

      <div className="flex-1 flex flex-col items-center justify-center my-4">
        <div className={`w-28 h-28 rounded-full flex items-center justify-center border-4 shadow-inner transition-colors duration-500 ${
          isWaiting
            ? 'border-slate-100 bg-slate-50 text-slate-400'
            : isRequired 
              ? 'border-amber-200 bg-amber-50 text-amber-600' 
              : 'border-emerald-100 bg-emerald-50 text-emerald-600'
        }`}>
          <Power className={`w-12 h-12 transition-transform duration-300 ${isRequired ? 'scale-110' : 'scale-95'}`} />
        </div>
        
        <div className="mt-5 flex flex-col items-center text-center">
          <div className="flex items-center space-x-2">
            <span className={`h-2.5 w-2.5 rounded-full ${
              isWaiting 
                ? 'bg-amber-400' 
                : isRequired 
                  ? 'bg-amber-500 animate-pulse' 
                  : 'bg-emerald-500'
            }`}></span>
            <span className="text-xl font-black tracking-tight text-slate-800">
              {isWaiting ? 'WAITING' : isRequired ? 'ACTUATION ADVISORY' : 'STANDBY'}
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1 font-medium">
            {isWaiting 
              ? 'Awaiting fresh sensor stream' 
              : isRequired 
                ? 'Field moisture depleted (<40%)' 
                : 'Moisture level sufficient (>=40%)'}
          </p>
        </div>
      </div>

      <div className="pt-4 border-t border-slate-100 text-center">
        <div className="flex items-center justify-center text-[11px] text-slate-500 font-medium">
          <Info className="w-3.5 h-3.5 mr-1 text-slate-400 flex-shrink-0" />
          <span>Physical relay simulated on Wokwi ESP32 (Read-Only)</span>
        </div>
      </div>
    </div>
  );
};

export default IrrigationPanel;
