
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
