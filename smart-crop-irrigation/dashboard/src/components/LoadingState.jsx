import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingState = ({ message = "Loading dashboard data..." }) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] w-full">
      <Loader2 className="w-10 h-10 text-green-600 animate-spin mb-4" />
      <p className="text-gray-600 font-medium">{message}</p>
    </div>
  );
};

export default LoadingState;
