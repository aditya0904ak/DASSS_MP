import React from 'react';
import { BrainCircuit, Droplets, CheckCircle, XCircle } from 'lucide-react';

const PredictionCard = ({ prediction }) => {
  if (!prediction) return null;

  const { pump_prediction, irrigation_required, confidence } = prediction;
  
  const isRequired = irrigation_required;
  const statusColor = isRequired ? 'text-blue-600' : 'text-gray-500';
  const bgColor = isRequired ? 'bg-blue-50 border-blue-200' : 'bg-gray-50 border-gray-200';

  return (
    <div className={`rounded-xl shadow-sm border p-6 flex flex-col h-full ${bgColor}`}>
      <div className="flex items-center space-x-2 mb-6">
        <BrainCircuit className={`w-6 h-6 ${statusColor}`} />
        <h2 className="text-lg font-bold text-gray-900">Machine Learning Prediction</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 flex-grow">
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100 flex flex-col items-center justify-center text-center">
          <span className="text-sm font-medium text-gray-500 mb-1">Pump Prediction</span>
          <span className={`text-2xl font-bold ${isRequired ? 'text-blue-600' : 'text-gray-700'}`}>
            {pump_prediction === 1 ? 'ON' : 'OFF'}
          </span>
        </div>

        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100 flex flex-col items-center justify-center text-center">
          <span className="text-sm font-medium text-gray-500 mb-2">Irrigation Required</span>
          <div className="flex items-center space-x-1">
            {isRequired ? (
              <>
                <CheckCircle className="w-5 h-5 text-blue-600" />
                <span className="text-xl font-bold text-blue-600">YES</span>
              </>
            ) : (
              <>
                <XCircle className="w-5 h-5 text-gray-400" />
                <span className="text-xl font-bold text-gray-600">NO</span>
              </>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100 flex flex-col items-center justify-center text-center">
          <span className="text-sm font-medium text-gray-500 mb-1">Confidence</span>
          <span className="text-2xl font-bold text-gray-900">
            {(confidence * 100).toFixed(1)}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default PredictionCard;
