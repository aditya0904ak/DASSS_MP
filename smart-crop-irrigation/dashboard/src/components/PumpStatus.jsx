import React from 'react';
import { Power } from 'lucide-react';

const PumpStatus = ({ prediction }) => {
  if (!prediction) return null;

  const isOn = prediction.pump_prediction === 1;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 h-full flex flex-col items-center justify-center">
      <h3 className="text-gray-500 font-medium text-sm mb-4">Pump Status Monitor</h3>
      
      <div className={`w-24 h-24 rounded-full flex items-center justify-center mb-4 transition-colors ${isOn ? 'bg-blue-100' : 'bg-gray-100'}`}>
        <Power className={`w-12 h-12 ${isOn ? 'text-blue-600' : 'text-gray-400'}`} />
      </div>
      
      <div className="text-center">
        <span className="block text-2xl font-bold text-gray-900 mb-1">
          {isOn ? 'Pump ON' : 'Pump OFF'}
        </span>
        <span className={`text-sm font-medium px-3 py-1 rounded-full ${isOn ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600'}`}>
          {isOn ? 'Active' : 'Standby'}
        </span>
      </div>
      
      <p className="text-xs text-gray-400 mt-6 text-center">
        * Based on current ML prediction. Hardware relay control pending.
      </p>
    </div>
  );
};

export default PumpStatus;
