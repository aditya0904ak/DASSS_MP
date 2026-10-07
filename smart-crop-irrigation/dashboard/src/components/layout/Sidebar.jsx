
import React from 'react';
import { LayoutDashboard, Radio, Droplets, BrainCircuit, LineChart, Settings, Leaf } from 'lucide-react';

const Sidebar = ({ isBackendOnline, isThingSpeakOnline }) => {
  const navItems = [
    { name: 'Overview', icon: LayoutDashboard, active: true },
    { name: 'Live Monitoring', icon: Radio, active: false },
    { name: 'Irrigation', icon: Droplets, active: false },
    { name: 'Predictions', icon: BrainCircuit, active: false },
    { name: 'Analytics', icon: LineChart, active: false },
    { name: 'System', icon: Settings, active: false },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col h-screen fixed hidden md:flex">
      <div className="p-6 flex items-center space-x-3 text-white">
        <div className="bg-emerald-500/20 p-2 rounded-lg">
          <Leaf className="w-6 h-6 text-emerald-400" />
        </div>
        <div>
          <h1 className="text-xl font-bold tracking-tight">AgriSense</h1>
          <p className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Predictive Intelligence</p>
        </div>
      </div>

      <nav className="flex-1 px-4 py-4 space-y-1">
        {navItems.map((item) => (
          <button
            key={item.name}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
              item.active
                ? 'bg-emerald-500/10 text-emerald-400'
                : 'hover:bg-slate-800 hover:text-white'
            }`}
          >
            <item.icon className={`w-5 h-5 ${item.active ? 'text-emerald-400' : 'text-slate-400'}`} />
            <span>{item.name}</span>
          </button>
        ))}
      </nav>

      <div className="p-4 mx-4 mb-6 rounded-xl bg-slate-800/50 border border-slate-700/50">
        <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">System Status</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-300">ThingSpeak</span>
            <div className="flex items-center space-x-2">
              <span className="relative flex h-2 w-2">
                {isThingSpeakOnline && <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>}
                <span className={`relative inline-flex rounded-full h-2 w-2 ${isThingSpeakOnline ? 'bg-emerald-500' : 'bg-red-500'}`}></span>
              </span>
            </div>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-300">ML Engine</span>
            <div className="flex items-center space-x-2">
              <span className="relative flex h-2 w-2">
                {isBackendOnline && <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>}
                <span className={`relative inline-flex rounded-full h-2 w-2 ${isBackendOnline ? 'bg-emerald-500' : 'bg-red-500'}`}></span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
