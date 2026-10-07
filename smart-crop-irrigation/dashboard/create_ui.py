import os

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# src/components/layout/Sidebar.jsx
write_file('src/components/layout/Sidebar.jsx', """
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
""")

# src/components/layout/TopHeader.jsx
write_file('src/components/layout/TopHeader.jsx', """
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
""")

# src/components/dashboard/HeroStatus.jsx
write_file('src/components/dashboard/HeroStatus.jsx', """
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
""")

# src/components/dashboard/KPICards.jsx
write_file('src/components/dashboard/KPICards.jsx', """
import React from 'react';
import { Droplets, Thermometer, Wind, Sun } from 'lucide-react';
import { motion } from 'framer-motion';

const getSoilStatus = (val) => val < 20 ? 'Dry' : val > 60 ? 'Wet' : 'Optimal';
const getTempStatus = (val) => val > 35 ? 'High' : val < 10 ? 'Low' : 'Normal';
const getHumStatus = (val) => val < 30 ? 'Dry' : val > 70 ? 'Humid' : 'Normal';

const KPICard = ({ title, value, unit, icon: Icon, color, status, delay }) => {
  const colorMap = {
    blue: 'bg-blue-50 text-blue-600 border-blue-100',
    amber: 'bg-amber-50 text-amber-600 border-amber-100',
    emerald: 'bg-emerald-50 text-emerald-600 border-emerald-100',
    purple: 'bg-purple-50 text-purple-600 border-purple-100',
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4 }}
      className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition-shadow"
    >
      <div className="flex justify-between items-start mb-6">
        <div className={`p-3 rounded-xl border ${colorMap[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
        <div className="flex items-center space-x-1">
          <span className="relative flex h-1.5 w-1.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-slate-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-slate-500"></span>
          </span>
          <span className="text-[10px] text-slate-400 font-medium uppercase tracking-wider">Live sensor</span>
        </div>
      </div>
      
      <div>
        <h3 className="text-sm font-semibold text-slate-500">{title}</h3>
        <div className="mt-1 flex items-baseline space-x-1">
          <span className="text-3xl font-bold text-slate-800 tracking-tight">{value ?? '--'}</span>
          <span className="text-sm font-medium text-slate-500">{unit}</span>
        </div>
      </div>
      
      <div className="mt-4 pt-4 border-t border-slate-100 flex justify-between items-center">
        <span className="text-xs font-medium text-slate-500">Status</span>
        <span className="text-xs font-bold text-slate-700 bg-slate-100 px-2 py-1 rounded-md">{status}</span>
      </div>
    </motion.div>
  );
};

const KPICards = ({ data }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <KPICard 
        title="Soil Moisture" 
        value={data?.soil_moisture} 
        unit="%" 
        icon={Droplets} 
        color="blue" 
        status={getSoilStatus(data?.soil_moisture)}
        delay={0.1}
      />
      <KPICard 
        title="Temperature" 
        value={data?.temperature} 
        unit="°C" 
        icon={Thermometer} 
        color="amber" 
        status={getTempStatus(data?.temperature)}
        delay={0.2}
      />
      <KPICard 
        title="Humidity" 
        value={data?.humidity} 
        unit="%" 
        icon={Wind} 
        color="emerald" 
        status={getHumStatus(data?.humidity)}
        delay={0.3}
      />
      <KPICard 
        title="Light Intensity" 
        value={data?.light} 
        unit="lx" 
        icon={Sun} 
        color="purple" 
        status="Current Level"
        delay={0.4}
      />
    </div>
  );
};

export default KPICards;
""")

# src/components/dashboard/MainChart.jsx
write_file('src/components/dashboard/MainChart.jsx', """
import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-900 border border-slate-700 p-3 rounded-lg shadow-xl">
        <p className="text-slate-400 text-xs mb-2">{label}</p>
        <p className="text-white font-bold text-sm">
          {payload[0].name}: {payload[0].value}
        </p>
      </div>
    );
  }
  return null;
};

const MainChart = ({ history }) => {
  const [metric, setMetric] = useState('soil_moisture');
  
  const chartData = history.map(item => {
    const d = new Date(item.timestamp);
    return {
      time: `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`,
      soil_moisture: item.sensor_data.soil_moisture,
      temperature: item.sensor_data.temperature,
      humidity: item.sensor_data.humidity,
      light: item.sensor_data.light,
    };
  });

  const metrics = [
    { id: 'soil_moisture', label: 'Soil Moisture', color: '#3b82f6' },
    { id: 'temperature', label: 'Temperature', color: '#f59e0b' },
    { id: 'humidity', label: 'Humidity', color: '#10b981' },
    { id: 'light', label: 'Light', color: '#8b5cf6' },
  ];

  const activeMetric = metrics.find(m => m.id === metric);

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm h-[400px] flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-bold text-slate-800">Environmental Telemetry</h3>
        <div className="flex space-x-2 bg-slate-50 p-1 rounded-lg border border-slate-200">
          {metrics.map(m => (
            <button
              key={m.id}
              onClick={() => setMetric(m.id)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-colors ${
                metric === m.id ? 'bg-white text-slate-800 shadow-sm border border-slate-200' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              {m.label}
            </button>
          ))}
        </div>
      </div>
      
      <div className="flex-1 w-full min-h-0">
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
              <XAxis 
                dataKey="time" 
                axisLine={false} 
                tickLine={false} 
                tick={{ fill: '#64748b', fontSize: 12 }} 
                dy={10}
              />
              <YAxis 
                axisLine={false} 
                tickLine={false} 
                tick={{ fill: '#64748b', fontSize: 12 }} 
              />
              <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#cbd5e1', strokeWidth: 1, strokeDasharray: '4 4' }} />
              <Line 
                type="monotone" 
                dataKey={metric} 
                name={activeMetric.label}
                stroke={activeMetric.color} 
                strokeWidth={3} 
                dot={{ r: 4, fill: activeMetric.color, strokeWidth: 0 }}
                activeDot={{ r: 6, strokeWidth: 0 }} 
                animationDuration={500}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-full flex items-center justify-center text-slate-400 text-sm">
            Waiting for telemetry data...
          </div>
        )}
      </div>
    </div>
  );
};

export default MainChart;
""")

# src/components/dashboard/IntelligenceCard.jsx
write_file('src/components/dashboard/IntelligenceCard.jsx', """
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
""")

# src/components/dashboard/IrrigationPanel.jsx
write_file('src/components/dashboard/IrrigationPanel.jsx', """
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
""")

# src/components/dashboard/EnvHealthPanel.jsx
write_file('src/components/dashboard/EnvHealthPanel.jsx', """
import React from 'react';
import { Check, AlertCircle } from 'lucide-react';

const HealthItem = ({ label, status }) => {
  const isOptimal = status === 'Optimal' || status === 'Normal';
  return (
    <div className="flex items-center justify-between p-3 rounded-lg border border-slate-100 bg-slate-50">
      <span className="text-sm font-medium text-slate-600">{label}</span>
      <div className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs font-bold ${isOptimal ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>
        {isOptimal ? <Check className="w-3.5 h-3.5" /> : <AlertCircle className="w-3.5 h-3.5" />}
        <span>{status}</span>
      </div>
    </div>
  );
};

const EnvHealthPanel = ({ data }) => {
  const getSoilStatus = (val) => val < 20 ? 'Attention' : val > 60 ? 'Attention' : 'Optimal';
  const getTempStatus = (val) => val > 35 ? 'Attention' : val < 10 ? 'Attention' : 'Normal';
  const getHumStatus = (val) => val < 30 ? 'Attention' : val > 70 ? 'Attention' : 'Normal';

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest mb-6">Environmental Health</h3>
      <div className="space-y-3">
        <HealthItem label="Soil Condition" status={getSoilStatus(data?.soil_moisture)} />
        <HealthItem label="Temperature" status={getTempStatus(data?.temperature)} />
        <HealthItem label="Humidity" status={getHumStatus(data?.humidity)} />
        <HealthItem label="Light Levels" status="Normal" />
      </div>
    </div>
  );
};

export default EnvHealthPanel;
""")

# src/components/dashboard/ActivityLog.jsx
write_file('src/components/dashboard/ActivityLog.jsx', """
import React from 'react';
import { format } from 'date-fns';

const ActivityLog = ({ events }) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm h-full overflow-hidden flex flex-col">
      <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest mb-6">Recent System Activity</h3>
      
      <div className="flex-1 overflow-y-auto pr-2">
        <div className="relative border-l-2 border-slate-100 ml-3 space-y-6 pb-2">
          {events.length === 0 ? (
            <p className="text-xs text-slate-400 pl-4">No recent activity.</p>
          ) : (
            events.map((event, i) => (
              <div key={i} className="relative pl-6">
                <div className={`absolute -left-1.5 top-1.5 w-3 h-3 rounded-full border-2 border-white ${event.type === 'error' ? 'bg-red-500' : 'bg-emerald-500'}`}></div>
                <p className="text-xs font-bold text-slate-400 mb-1">{format(new Date(event.time), 'HH:mm:ss')}</p>
                <p className="text-sm font-medium text-slate-700">{event.message}</p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default ActivityLog;
""")

# src/components/dashboard/SystemHealth.jsx
write_file('src/components/dashboard/SystemHealth.jsx', """
import React from 'react';

const HealthIndicator = ({ name, isOnline }) => (
  <div className="flex items-center justify-between">
    <span className="text-sm font-medium text-slate-600">{name}</span>
    <div className="flex items-center space-x-2">
      <span className={`h-2 w-2 rounded-full ${isOnline ? 'bg-emerald-500' : 'bg-red-500'}`}></span>
      <span className={`text-xs font-bold ${isOnline ? 'text-emerald-700' : 'text-red-600'}`}>{isOnline ? 'Connected' : 'Offline'}</span>
    </div>
  </div>
);

const SystemHealth = ({ backendStatus, thingspeakStatus }) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest mb-6">System Health</h3>
      <div className="space-y-4">
        <HealthIndicator name="ThingSpeak API" isOnline={thingspeakStatus} />
        <HealthIndicator name="FastAPI Backend" isOnline={backendStatus} />
        <HealthIndicator name="ML Engine" isOnline={backendStatus} />
        <HealthIndicator name="Telemetry Sync" isOnline={thingspeakStatus && backendStatus} />
      </div>
    </div>
  );
};

export default SystemHealth;
""")

# src/components/ui/Skeleton.jsx
write_file('src/components/ui/Skeleton.jsx', """
import React from 'react';

export const Skeleton = ({ className }) => {
  return (
    <div className={`animate-pulse bg-slate-200 rounded-md ${className}`}></div>
  );
};

export const DashboardSkeleton = () => (
  <div className="p-6 md:p-8 w-full max-w-7xl mx-auto space-y-8">
    <Skeleton className="h-24 w-full rounded-2xl" />
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {[1, 2, 3, 4].map(i => <Skeleton key={i} className="h-32 rounded-2xl" />)}
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2">
        <Skeleton className="h-[400px] rounded-2xl" />
      </div>
      <Skeleton className="h-[400px] rounded-2xl" />
    </div>
  </div>
);
""")
