import React, { useState, useEffect } from 'react';
import { RefreshCw, Radio } from 'lucide-react';
import { formatDistanceToNow, parseISO } from 'date-fns';

const TopHeader = ({ 
  lastUpdated, 
  backendStatus = 'LIVE', 
  lastPolledAt, 
  isRefreshing, 
  onRefresh 
}) => {
  const [relativeTime, setRelativeTime] = useState('Waiting...');

  // Derive status directly from backend if available, otherwise check age
  const status = backendStatus || 'STALE';

  useEffect(() => {
    if (!lastUpdated) {
      setRelativeTime('No telemetry yet');
      return;
    }

    const updateRelative = () => {
      try {
        const d = parseISO(lastUpdated);
        setRelativeTime(`${formatDistanceToNow(d)} ago`);
      } catch {
        setRelativeTime(lastUpdated);
      }
    };

    updateRelative();
    const interval = setInterval(updateRelative, 5000);
    return () => clearInterval(interval);
  }, [lastUpdated]);

  const getStatusStyles = () => {
    switch (status) {
      case 'LIVE':
        return {
          container: 'bg-emerald-50 border-emerald-200 text-emerald-700',
          dot: 'bg-emerald-500',
          ping: 'bg-emerald-400'
        };
      case 'DELAYED':
        return {
          container: 'bg-amber-50 border-amber-200 text-amber-700',
          dot: 'bg-amber-500',
          ping: 'hidden'
        };
      case 'STALE':
      default:
        return {
          container: 'bg-amber-50 border-amber-300 text-amber-800',
          dot: 'bg-amber-500',
          ping: 'hidden'
        };
    }
  };

  const styles = getStatusStyles();

  return (
    <header className="bg-white border-b border-slate-200 px-6 md:px-8 py-4.5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <div className="flex items-center space-x-2">
          <h2 className="text-xl md:text-2xl font-black text-slate-800 tracking-tight">
            Smart Crop Irrigation Center
          </h2>
          <span className="text-[11px] font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded uppercase tracking-wider">
            IoT Edge
          </span>
        </div>
        <p className="text-xs text-slate-500 mt-0.5">
          Real-time IoT telemetry and predictive machine learning monitoring
        </p>
      </div>
      
      <div className="flex flex-wrap items-center gap-4">
        {/* Telemetry Status Badge */}
        <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-full border text-xs font-bold tracking-wide shadow-xs ${styles.container}`}>
          <span className="relative flex h-2 w-2">
            {status === 'LIVE' && (
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${styles.ping}`}></span>
            )}
            <span className={`relative inline-flex rounded-full h-2 w-2 ${styles.dot}`}></span>
          </span>
          <span>{status === 'LIVE' ? 'LIVE TELEMETRY' : 'STALE TELEMETRY'}</span>
        </div>
        
        {/* Timestamp & Refresh */}
        <div className="flex items-center space-x-3 text-xs text-slate-500">
          <div className="flex flex-col text-right">
            <span className="font-semibold text-slate-700">
              Feed: {relativeTime}
            </span>
            <span className="text-[10px] text-slate-400 font-mono">
              {lastUpdated ? lastUpdated.replace('T', ' ').replace('Z', ' UTC') : '--'}
            </span>
          </div>

          <button 
            onClick={onRefresh}
            className={`p-2 rounded-xl border border-slate-200 hover:bg-slate-50 transition-colors shadow-2xs ${
              isRefreshing ? 'opacity-50 cursor-not-allowed bg-slate-50' : 'bg-white'
            }`}
            title="Poll latest telemetry now"
            disabled={isRefreshing}
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-emerald-600' : 'text-slate-500'}`} />
          </button>
        </div>
      </div>
    </header>
  );
};

export default TopHeader;
