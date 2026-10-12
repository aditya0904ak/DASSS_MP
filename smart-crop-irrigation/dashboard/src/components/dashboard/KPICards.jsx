import React from 'react';
import { Droplets, Thermometer, Wind, Sun, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';

const getSoilStatus = (val) => {
  if (val == null) return { text: 'Awaiting', color: 'bg-slate-100 text-slate-600' };
  if (val < 40) return { text: 'Low (<40%)', color: 'bg-red-100 text-red-700 border border-red-200' };
  if (val > 60) return { text: 'Saturated', color: 'bg-amber-100 text-amber-700' };
  return { text: 'Optimal', color: 'bg-emerald-100 text-emerald-700' };
};

const getTempStatus = (val) => {
  if (val == null) return { text: 'Awaiting', color: 'bg-slate-100 text-slate-600' };
  if (val > 35) return { text: 'High', color: 'bg-red-100 text-red-700' };
  if (val < 15) return { text: 'Cool', color: 'bg-blue-100 text-blue-700' };
  return { text: 'Optimal', color: 'bg-emerald-100 text-emerald-700' };
};

const getHumStatus = (val) => {
  if (val == null) return { text: 'Awaiting', color: 'bg-slate-100 text-slate-600' };
  if (val < 30) return { text: 'Dry Air', color: 'bg-amber-100 text-amber-700' };
  if (val > 70) return { text: 'Humid', color: 'bg-blue-100 text-blue-700' };
  return { text: 'Optimal', color: 'bg-emerald-100 text-emerald-700' };
};

const getLightStatus = (val) => {
  if (val == null) return { text: 'Awaiting', color: 'bg-slate-100 text-slate-600' };
  if (val < 500) return { text: 'Low ADC', color: 'bg-slate-100 text-slate-700' };
  if (val > 3000) return { text: 'High ADC', color: 'bg-amber-100 text-amber-700' };
  return { text: 'Mid Range', color: 'bg-emerald-100 text-emerald-700' };
};

const KPICard = ({ title, value, unit, icon: Icon, color, statusInfo, delay, isStale, isLowMoisture }) => {
  const colorMap = {
    blue: 'bg-blue-50 text-blue-600 border-blue-100',
    amber: 'bg-amber-50 text-amber-600 border-amber-100',
    emerald: 'bg-emerald-50 text-emerald-600 border-emerald-100',
    purple: 'bg-purple-50 text-purple-600 border-purple-100',
  };

  const displayVal = typeof value === 'number' && Number.isFinite(value) 
    ? (Number.isInteger(value) ? value : value.toFixed(1)) 
    : '--';

  return (
    <motion.div 
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.3 }}
      className={`bg-white rounded-2xl border p-6 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden ${
        isLowMoisture ? 'border-red-300 ring-2 ring-red-100' : 'border-slate-200'
      }`}
    >
      <div className="flex justify-between items-start mb-5">
        <div className={`p-3 rounded-xl border ${colorMap[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
        <div className="flex items-center space-x-1.5">
          {isLowMoisture && (
            <span className="flex items-center text-[10px] font-bold text-red-600 bg-red-50 border border-red-200 px-2 py-0.5 rounded-full mr-1">
              <AlertTriangle className="w-3 h-3 mr-0.5" />
              &lt;40% Threshold
            </span>
          )}
          <span className="relative flex h-2 w-2">
            {!isStale ? (
              <>
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </>
            ) : (
              <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-400"></span>
            )}
          </span>
          <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">
            {isStale ? 'Stale' : 'Live Feed'}
          </span>
        </div>
      </div>
      
      <div>
        <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{title}</h3>
        <div className="mt-1 flex items-baseline space-x-1">
          <span className="text-3xl font-black text-slate-800 tracking-tight">{displayVal}</span>
          <span className="text-sm font-bold text-slate-400">{unit}</span>
        </div>
      </div>
      
      <div className="mt-4 pt-3.5 border-t border-slate-100 flex justify-between items-center text-xs">
        <span className="text-slate-400 font-medium">Condition</span>
        <span className={`font-bold px-2.5 py-0.5 rounded-md ${statusInfo.color}`}>
          {statusInfo.text}
        </span>
      </div>
    </motion.div>
  );
};

const KPICards = ({ data, isStale }) => {
  const isLowMoisture = typeof data?.soil_moisture === 'number' && data.soil_moisture < 40.0;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <KPICard 
        title="Soil Moisture" 
        value={data?.soil_moisture} 
        unit="%" 
        icon={Droplets} 
        color="blue" 
        statusInfo={getSoilStatus(data?.soil_moisture)}
        delay={0.05}
        isStale={isStale}
        isLowMoisture={isLowMoisture}
      />
      <KPICard 
        title="Temperature" 
        value={data?.temperature} 
        unit="°C" 
        icon={Thermometer} 
        color="amber" 
        statusInfo={getTempStatus(data?.temperature)}
        delay={0.1}
        isStale={isStale}
      />
      <KPICard 
        title="Humidity" 
        value={data?.humidity} 
        unit="%" 
        icon={Wind} 
        color="emerald" 
        statusInfo={getHumStatus(data?.humidity)}
        delay={0.15}
        isStale={isStale}
      />
      <KPICard 
        title="LDR Raw Reading (ADC)" 
        value={data?.light} 
        unit="ADC" 
        icon={Sun} 
        color="purple" 
        statusInfo={getLightStatus(data?.light)}
        delay={0.2}
        isStale={isStale}
      />
    </div>
  );
};

export default KPICards;
