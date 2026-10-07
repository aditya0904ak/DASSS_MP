import React, { useState, useEffect, useRef } from 'react';
import Sidebar from '../components/layout/Sidebar';
import TopHeader from '../components/layout/TopHeader';
import HeroStatus from '../components/dashboard/HeroStatus';
import KPICards from '../components/dashboard/KPICards';
import MainChart from '../components/dashboard/MainChart';
import IntelligenceCard from '../components/dashboard/IntelligenceCard';
import IrrigationPanel from '../components/dashboard/IrrigationPanel';
import EnvHealthPanel from '../components/dashboard/EnvHealthPanel';
import ActivityLog from '../components/dashboard/ActivityLog';
import SystemHealth from '../components/dashboard/SystemHealth';
import { DashboardSkeleton } from '../components/ui/Skeleton';
import { getLivePrediction } from '../services/api';

const MAX_HISTORY = 30;

const Dashboard = () => {
  const [currentData, setCurrentData] = useState(null);
  const [history, setHistory] = useState([]);
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState(null);
  
  const [sysStatus, setSysStatus] = useState({ backend: true, thingspeak: true });
  
  const isMounted = useRef(true);

  const addEvent = (msg, type = 'info') => {
    setEvents(prev => [{ time: new Date().toISOString(), message: msg, type }, ...prev].slice(0, 50));
  };

  const fetchLiveData = async (isManual = false) => {
    if (isManual) setIsRefreshing(true);
    
    try {
      const data = await getLivePrediction();
      if (!isMounted.current) return;
      
      setCurrentData(data);
      setError(null);
      setSysStatus({ backend: true, thingspeak: true });
      
      setHistory(prev => {
        const newHistory = [...prev, data];
        return newHistory.length > MAX_HISTORY ? newHistory.slice(newHistory.length - MAX_HISTORY) : newHistory;
      });

      addEvent('Sensor telemetry & prediction updated');
      
    } catch (err) {
      if (!isMounted.current) return;
      console.error(err);
      
      if (err.response?.status === 400) {
        setError("Telemetry temporarily unavailable (ThingSpeak offline)");
        setSysStatus(prev => ({ ...prev, thingspeak: false }));
        addEvent('ThingSpeak connection failed', 'error');
      } else {
        setError("Backend connection lost. Trying to reconnect...");
        setSysStatus({ backend: false, thingspeak: false });
        addEvent('Backend connection lost', 'error');
      }
    } finally {
      if (isMounted.current) {
        setIsLoading(false);
        setIsRefreshing(false);
      }
    }
  };

  useEffect(() => {
    isMounted.current = true;
    addEvent('System initialization started');
    fetchLiveData();
    
    const interval = setInterval(() => fetchLiveData(false), 20000);
    return () => {
      isMounted.current = false;
      clearInterval(interval);
    };
  }, []);

  if (isLoading) {
    return (
      <div className="flex h-screen bg-slate-50">
        <Sidebar isBackendOnline={false} isThingSpeakOnline={false} />
        <div className="flex-1 flex flex-col md:ml-64">
          <TopHeader isRefreshing={true} />
          <div className="flex-1 overflow-auto">
            <DashboardSkeleton />
          </div>
        </div>
      </div>
    );
  }

  const { sensor_data, prediction, timestamp } = currentData || {};

  return (
    <div className="flex h-screen bg-[#F8FAFC] overflow-hidden">
      {/* Sidebar - fixed on desktop */}
      <Sidebar isBackendOnline={sysStatus.backend} isThingSpeakOnline={sysStatus.thingspeak} />
      
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col md:ml-64 overflow-hidden h-screen">
        <TopHeader 
          lastUpdated={timestamp || new Date().toISOString()} 
          isRefreshing={isRefreshing} 
          onRefresh={() => fetchLiveData(true)} 
        />
        
        <main className="flex-1 overflow-y-auto p-4 md:p-8 space-y-8 pb-20">
          
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-red-700 flex items-center shadow-sm">
              <span className="font-bold mr-2">System Error:</span> {error}
            </div>
          )}

          {/* Hero Section */}
          <HeroStatus irrigationRequired={prediction?.irrigation_required} />

          {/* KPI Cards */}
          <KPICards data={sensor_data} />

          {/* Main Intelligence Section */}
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            <div className="xl:col-span-2">
              <MainChart history={history} />
            </div>
            <div className="xl:col-span-1">
              <IntelligenceCard prediction={prediction} sensorData={sensor_data} />
            </div>
          </div>

          {/* Bottom Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
            <div className="xl:col-span-1">
              <IrrigationPanel prediction={prediction} />
            </div>
            <div className="xl:col-span-1">
              <EnvHealthPanel data={sensor_data} />
            </div>
            <div className="xl:col-span-1">
              <SystemHealth backendStatus={sysStatus.backend} thingspeakStatus={sysStatus.thingspeak} />
            </div>
            <div className="xl:col-span-1">
              <ActivityLog events={events} />
            </div>
          </div>

        </main>
      </div>
    </div>
  );
};

export default Dashboard;
