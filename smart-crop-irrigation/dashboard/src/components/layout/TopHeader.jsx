
import React from 'react';
import { RefreshCw } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

const TopHeader = ({ lastUpdated, isRefreshing, onRefresh }) => {
  return (
    <header className="bg-white border-b border-slate-200 px-8 py-5 flex flex-col sm:flex-row justify-between items-start sm:items-center">
      <div>
        <h2 className="text-2xl font-bold text-slate-800">Smart Irrigation Control Center</h2>
        <p className="text-sm text-slate-500 mt-1">Real-time crop environment and predictive irrigation monitoring</p>
      </div>
      
      <div className="mt-4 sm:mt-0 flex items-center space-x-6">
        <div className="flex items-center space-x-2 bg-emerald-50 px-3 py-1.5 rounded-full border border-emerald-100">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-xs font-semibold text-emerald-700 tracking-wide">LIVE</span>
        </div>
        
        <div className="flex items-center space-x-3 text-sm text-slate-500">
          <span>
            Last synchronized: {lastUpdated ? `${formatDistanceToNow(new Date(lastUpdated))} ago` : 'Waiting...'}
          </span>
          <button 
            onClick={onRefresh}
            className={`p-1.5 rounded-md hover:bg-slate-100 transition-colors ${isRefreshing ? 'opacity-50 cursor-not-allowed' : ''}`}
            disabled={isRefreshing}
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-emerald-600' : 'text-slate-400'}`} />
          </button>
        </div>
      </div>
    </header>
  );
};

export default TopHeader;
