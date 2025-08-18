import axios, { AxiosError } from 'axios';
import { InterpretationResponse, PatientData } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutos para aguardar cold start do Render
  headers: {
    'Accept': 'application/json',
  },
});

// Função para retry com backoff exponencial
const retryRequest = async <T>(
  requestFn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> => {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await requestFn();
    } catch (error) {
      const isLastAttempt = attempt === maxRetries;
      const isNetworkError = error instanceof AxiosError && 
        (error.code === 'ECONNABORTED' || error.code === 'NETWORK_ERROR' || !error.response);
      
      if (isLastAttempt || !isNetworkError) {
        throw error;
      }
      
      // Aguardar antes do próximo retry (backoff exponencial)
      const delay = baseDelay * Math.pow(2, attempt);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw new Error('Max retries exceeded');
};

export const interpretLab = async (
  file: File,
  patientData: PatientData
): Promise<InterpretationResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('genero', patientData.genero);
  formData.append('idade', patientData.idade.toString());

  return retryRequest(async () => {
    const response = await api.post<InterpretationResponse>('/interpret', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 180000, // 3 minutos para upload e processamento
    });
    return response.data;
  });
};

export const healthCheck = async (): Promise<{ status: string; message: string }> => {
  return retryRequest(async () => {
    const response = await api.get('/health', {
      timeout: 30000, // 30 segundos para health check
    });
    return response.data;
  });
};