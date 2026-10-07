import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

const SensorChart = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 h-80 flex items-center justify-center">
        <span className="text-gray-400">Waiting for data to generate chart...</span>
      </div>
    );
  }

  // Format time for X axis
  const chartData = data.map(item => {
    const date = new Date(item.timestamp);
    return {
      ...item.sensor_data,
      time: `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`
    };
  });

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h3 className="text-gray-900 font-bold text-lg mb-6">Live Sensor History</h3>
      
      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
            <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#9ca3af' }} />
            <YAxis yAxisId="left" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#9ca3af' }} />
            <YAxis yAxisId="right" orientation="right" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#9ca3af' }} />
            <Tooltip 
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            <Legend iconType="circle" />
            
            <Line yAxisId="left" type="monotone" dataKey="soil_moisture" name="Soil Moisture %" stroke="#3b82f6" strokeWidth={2} dot={false} activeDot={{ r: 6 }} />
            <Line yAxisId="left" type="monotone" dataKey="humidity" name="Humidity %" stroke="#10b981" strokeWidth={2} dot={false} activeDot={{ r: 6 }} />
            <Line yAxisId="left" type="monotone" dataKey="temperature" name="Temperature °C" stroke="#f59e0b" strokeWidth={2} dot={false} activeDot={{ r: 6 }} />
            <Line yAxisId="right" type="monotone" dataKey="light" name="Light" stroke="#8b5cf6" strokeWidth={2} dot={false} activeDot={{ r: 6 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default SensorChart;
