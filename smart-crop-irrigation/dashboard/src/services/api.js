import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const getLatestTelemetry = async () => {
  const response = await api.get('/api/telemetry/latest');
  return response.data;
};

export const getLivePrediction = async () => {
  const response = await api.get('/api/predict/live');
  return response.data;
};

export const checkHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};
