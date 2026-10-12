import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch unified dashboard data:
 * {
 *   timestamp: string,
 *   sensor_data: { soil_moisture, temperature, humidity, light },
 *   prediction: { pump_prediction, irrigation_required, confidence },
 *   system: { status, data_source, model_loaded }
 * }
 */
export const getDashboardSummary = async () => {
  const response = await api.get('/api/dashboard');
  if (response.status !== 200) {
    throw new Error(`Failed to fetch dashboard data: HTTP ${response.status}`);
  }
  return response.data;
};

/**
 * Fetch historical sensor feeds from ThingSpeak.
 * Supports results parameter (1 to 8000, default 100).
 */
export const getTelemetryHistory = async (results = 100) => {
  const response = await api.get('/api/telemetry/history', {
    params: { results }
  });
  if (response.status !== 200) {
    throw new Error(`Failed to fetch telemetry history: HTTP ${response.status}`);
  }
  return response.data;
};

/**
 * Check backend health and model status
 */
export const checkHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

/**
 * Fetch latest telemetry only
 */
export const getLatestTelemetry = async () => {
  const response = await api.get('/api/telemetry/latest');
  return response.data;
};

/**
 * Fetch live prediction directly
 */
export const getLivePrediction = async () => {
  const response = await api.get('/api/predict/live');
  return response.data;
};

export default api;
