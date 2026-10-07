import React from 'react';

const SensorCard = ({ title, value, unit, icon: Icon, colorClass }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex flex-col justify-between hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-gray-500 font-medium text-sm">{title}</h3>
        <div className={`p-2 rounded-lg ${colorClass} bg-opacity-10`}>
          <Icon className={`w-5 h-5 ${colorClass.replace('bg-', 'text-')}`} />
        </div>
      </div>
      <div className="flex items-baseline space-x-1">
        <span className="text-3xl font-bold text-gray-900">{value}</span>
        <span className="text-gray-500 font-medium">{unit}</span>
      </div>
    </div>
  );
};

export default SensorCard;
