import React from 'react';
import { LayoutDashboard, Radio, Droplets, BrainCircuit, LineChart, Settings, Leaf } from 'lucide-react';

const Sidebar = ({ isBackendOnline = true, isThingSpeakOnline = true, isStale = false }) => {
  const navItems = [
    { name: 'Overview', icon: LayoutDashboard, active: true },
    { name: 'Live Telemetry', icon: Radio, active: false },
    { name: 'Irrigation Advisory', icon: Droplets, active: false },
    { name: 'Model Predictions', icon: BrainCircuit, active: false },
    { name: 'Historical Analytics', icon: LineChart, active: false },
    { name: 'System Settings', icon: Settings, active: false },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col h-screen fixed hidden md:flex z-20">
      <div className="p-6 flex items-center space-x-3 text-white">
        <div className="bg-emerald-500/20 p-2.5 rounded-xl border border-emerald-500/30">
          <Leaf className="w-6 h-6 text-emerald-400" />
        </div>
        <div>
          <h1 className="text-xl font-black tracking-tight">AgriSense</h1>
          <p className="text-[10px] text-slate-400 uppercase tracking-widest font-semibold">Precision IoT</p>
        </div>
      </div>

      <nav className="flex-1 px-4 py-4 space-y-1">
        {navItems.map((item) => (
          <button
            key={item.name}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-xs font-bold transition-all ${
              item.active
                ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/20 shadow-xs'
                : 'hover:bg-slate-800 hover:text-white text-slate-400'
            }`}
          >
            <item.icon className={`w-4 h-4 ${item.active ? 'text-emerald-400' : 'text-slate-500'}`} />
            <span>{item.name}</span>
          </button>
        ))}
      </nav>

      <div className="p-4 mx-4 mb-6 rounded-2xl bg-slate-800/60 border border-slate-700/60">
        <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">
          Telemetry Link
        </h3>
        <div className="space-y-2.5">
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-300 font-medium">ThingSpeak</span>
            <div className="flex items-center space-x-1.5">
              <span className={`h-2 w-2 rounded-full ${
                !isThingSpeakOnline 
                  ? 'bg-red-500' 
                  : isStale 
                    ? 'bg-amber-400' 
                    : 'bg-emerald-400'
              }`}></span>
              <span className="text-[10px] font-bold text-slate-400">
                {!isThingSpeakOnline ? 'Offline' : isStale ? 'Stale' : 'Live'}
              </span>
            </div>
          </div>
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-300 font-medium">FastAPI</span>
            <div className="flex items-center space-x-1.5">
              <span className={`h-2 w-2 rounded-full ${isBackendOnline ? 'bg-emerald-400' : 'bg-red-500'}`}></span>
              <span className="text-[10px] font-bold text-slate-400">
                {isBackendOnline ? 'Online' : 'Offline'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
