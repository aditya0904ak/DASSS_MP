
import React from 'react';
import { MapPin, CheckCircle2, AlertTriangle } from 'lucide-react';

const HeroStatus = ({ irrigationRequired }) => {
  const isRecommended = irrigationRequired === true;
  
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center bg-gradient-to-r from-white to-slate-50">
      <div>
        <div className="flex items-center space-x-2 text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
          <MapPin className="w-3.5 h-3.5" />
          <span>Field 01 — Smart Irrigation Zone</span>
        </div>
        <h2 className="text-xl font-bold text-slate-800">System Status: <span className="text-emerald-600">Optimal</span></h2>
      </div>
      
      <div className="mt-4 md:mt-0 flex items-center space-x-4 bg-white px-5 py-3 rounded-xl border border-slate-100 shadow-sm">
        <div className={`p-2 rounded-full ${isRecommended ? 'bg-amber-100 text-amber-600' : 'bg-emerald-100 text-emerald-600'}`}>
          {isRecommended ? <AlertTriangle className="w-5 h-5" /> : <CheckCircle2 className="w-5 h-5" />}
        </div>
        <div>
          <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">Current Recommendation</p>
          <p className={`font-bold ${isRecommended ? 'text-amber-700' : 'text-emerald-700'}`}>
            {isRecommended ? 'Irrigation Recommended' : 'Irrigation Not Required'}
          </p>
        </div>
      </div>
    </div>
  );
};

export default HeroStatus;
