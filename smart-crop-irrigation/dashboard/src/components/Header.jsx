import React from 'react';
import { Sprout, Wifi, WifiOff } from 'lucide-react';

const Header = ({ isConnected, lastUpdated }) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex flex-col sm:flex-row justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="bg-green-100 p-2 rounded-lg">
              <Sprout className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Smart Crop Irrigation</h1>
              <p className="text-sm text-gray-500">IoT-Based Predictive Water Management System</p>
            </div>
          </div>
          
          <div className="mt-4 sm:mt-0 flex flex-col items-end space-y-1">
            <div className={`flex items-center space-x-2 text-sm font-medium ${isConnected ? 'text-green-600' : 'text-red-500'}`}>
              {isConnected ? <Wifi className="w-4 h-4" /> : <WifiOff className="w-4 h-4" />}
              <span>{isConnected ? 'System Online' : 'System Offline'}</span>
            </div>
            {lastUpdated && (
              <span className="text-xs text-gray-500">
                Last updated: {new Date(lastUpdated).toLocaleTimeString()}
              </span>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
