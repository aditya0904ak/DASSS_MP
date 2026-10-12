import React, { useState, useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { format, parseISO } from 'date-fns';

const CustomTooltip = ({ active, payload, label, unit }) => {
  if (active && payload && payload.length) {
    const dataPoint = payload[0].payload;
    return (
      <div className="bg-slate-900 border border-slate-700 p-3 rounded-xl shadow-2xl text-xs">
        <p className="text-slate-400 font-mono mb-1">{dataPoint.fullTimestamp || label}</p>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: payload[0].color }}></span>
          <span className="text-white font-bold text-sm">
            {payload[0].name}: {payload[0].value} {unit}
          </span>
        </div>
      </div>
    );
  }
  return null;
};

const MainChart = ({ history = [] }) => {
  const [metric, setMetric] = useState('soil_moisture');
  const [rangeLimit, setRangeLimit] = useState(30);

  const metrics = [
    { id: 'soil_moisture', label: 'Soil Moisture', unit: '%', color: '#3b82f6', minDomain: 0, maxDomain: 100 },
    { id: 'temperature', label: 'Temperature', unit: '°C', color: '#f59e0b', minDomain: 0, maxDomain: 50 },
    { id: 'humidity', label: 'Humidity', unit: '%', color: '#10b981', minDomain: 0, maxDomain: 100 },
    { id: 'light', label: 'LDR Raw (ADC)', unit: 'ADC', color: '#8b5cf6', minDomain: 0, maxDomain: 'auto' },
  ];

  const activeMetric = metrics.find(m => m.id === metric) || metrics[0];

  // Process, validate, and normalize history data
  const chartData = useMemo(() => {
    if (!Array.isArray(history) || history.length === 0) return [];

    const mapped = history
      .filter(item => item && item.timestamp)
      .map(item => {
        let timeLabel = item.timestamp;
        let fullTimestamp = item.timestamp;
        try {
          const d = parseISO(item.timestamp);
          timeLabel = format(d, 'HH:mm:ss');
          fullTimestamp = format(d, 'yyyy-MM-dd HH:mm:ss');
        } catch {
          // Fallback if parsing fails
        }

        const soil = item.sensor_data?.soil_moisture ?? item.soil_moisture;
        const temp = item.sensor_data?.temperature ?? item.temperature;
        const hum = item.sensor_data?.humidity ?? item.humidity;
        const lgt = item.sensor_data?.light ?? item.light;

        return {
          time: timeLabel,
          fullTimestamp,
          rawTimestamp: item.timestamp,
          soil_moisture: typeof soil === 'number' && Number.isFinite(soil) ? Math.round(soil * 10) / 10 : null,
          temperature: typeof temp === 'number' && Number.isFinite(temp) ? Math.round(temp * 10) / 10 : null,
          humidity: typeof hum === 'number' && Number.isFinite(hum) ? Math.round(hum * 10) / 10 : null,
          light: typeof lgt === 'number' && Number.isFinite(lgt) ? Math.round(lgt) : null,
        };
      })
      // Ensure strictly ascending chronological order
      .sort((a, b) => new Date(a.rawTimestamp) - new Date(b.rawTimestamp));

    if (rangeLimit === 'all' || mapped.length <= rangeLimit) {
      return mapped;
    }
    return mapped.slice(mapped.length - rangeLimit);
  }, [history, rangeLimit]);

  // Compute live statistics for the selected metric
  const stats = useMemo(() => {
    const validVals = chartData
      .map(d => d[metric])
      .filter(v => v !== null && typeof v === 'number');

    if (validVals.length === 0) return { min: '--', max: '--', latest: '--', count: 0 };

    return {
      min: Math.min(...validVals),
      max: Math.max(...validVals),
      latest: validVals[validVals.length - 1],
      count: validVals.length
    };
  }, [chartData, metric]);

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col h-full min-h-[440px]">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <div>
          <h3 className="text-lg font-bold text-slate-800">Historical Telemetry Stream</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Real ThingSpeak feeds ({stats.count} readings displayed)
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {/* Metric Selector */}
          <div className="flex space-x-1 bg-slate-100 p-1 rounded-xl border border-slate-200/60">
            {metrics.map(m => (
              <button
                key={m.id}
                onClick={() => setMetric(m.id)}
                className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                  metric === m.id
                    ? 'bg-white text-slate-800 shadow-sm border border-slate-200 font-bold'
                    : 'text-slate-500 hover:text-slate-800'
                }`}
              >
                {m.label}
              </button>
            ))}
          </div>

          {/* Range Limit Selector */}
          <div className="flex space-x-1 bg-slate-100 p-1 rounded-xl border border-slate-200/60 text-xs">
            {[10, 30, 100, 'all'].map(opt => (
              <button
                key={opt}
                onClick={() => setRangeLimit(opt)}
                className={`px-2 py-1 rounded-md font-medium transition-colors ${
                  rangeLimit === opt
                    ? 'bg-white text-slate-800 shadow-xs font-bold'
                    : 'text-slate-400 hover:text-slate-600'
                }`}
              >
                {opt === 'all' ? 'All' : `${opt}pts`}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Summary Stats Strip */}
      <div className="grid grid-cols-3 gap-3 mb-4 p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
        <div>
          <span className="text-slate-400 font-medium">Latest:</span>{' '}
          <span className="font-bold text-slate-800">{stats.latest} {activeMetric.unit}</span>
        </div>
        <div>
          <span className="text-slate-400 font-medium">Min:</span>{' '}
          <span className="font-bold text-slate-700">{stats.min} {activeMetric.unit}</span>
        </div>
        <div>
          <span className="text-slate-400 font-medium">Max:</span>{' '}
          <span className="font-bold text-slate-700">{stats.max} {activeMetric.unit}</span>
        </div>
      </div>

      {/* Chart Canvas */}
      <div className="flex-1 w-full min-h-[260px]">
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 10, right: 15, left: -10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
              <XAxis
                dataKey="time"
                axisLine={{ stroke: '#e2e8f0' }}
                tickLine={false}
                tick={{ fill: '#94a3b8', fontSize: 11 }}
                dy={6}
              />
              <YAxis
                axisLine={false}
                tickLine={false}
                tick={{ fill: '#94a3b8', fontSize: 11 }}
                unit={activeMetric.unit}
              />
              <Tooltip
                content={<CustomTooltip unit={activeMetric.unit} />}
                cursor={{ stroke: '#cbd5e1', strokeWidth: 1, strokeDasharray: '4 4' }}
              />
              <Line
                type="monotone"
                dataKey={metric}
                name={activeMetric.label}
                stroke={activeMetric.color}
                strokeWidth={2.5}
                dot={{ r: 3, fill: activeMetric.color, strokeWidth: 0 }}
                activeDot={{ r: 6, strokeWidth: 2, stroke: '#ffffff' }}
                connectNulls
                animationDuration={400}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-slate-400 text-sm py-12">
            <p className="font-medium">No historical telemetry feeds available.</p>
            <p className="text-xs text-slate-400 mt-1">Waiting for initial ThingSpeak feed synchronization...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MainChart;
