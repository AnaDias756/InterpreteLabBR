import axios from 'axios';
import { InterpretationResponse, PatientData } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
});

export const interpretLab = async (
  file: File,
  patientData: PatientData
): Promise<InterpretationResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('genero', patientData.genero);
  formData.append('idade', patientData.idade.toString());

  const response = await api.post<InterpretationResponse>('/interpret', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const healthCheck = async (): Promise<{ status: string; message: string }> => {
  const response = await api.get('/health');
  return response.data;
};