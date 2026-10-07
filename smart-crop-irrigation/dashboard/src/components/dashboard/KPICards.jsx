
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
