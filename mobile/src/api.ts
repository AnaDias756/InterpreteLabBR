import axios from 'axios';
import { API_BASE_URL } from './config';
import { InterpretationResponse, PatientData, ManualLabValues } from './types';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 min (cold start do Render)
  headers: { Accept: 'application/json' },
});

export async function healthCheck(): Promise<{ status: string; message: string }> {
  const response = await api.get('/health', { timeout: 60000 });
  return response.data;
}

export async function interpretLabManual(
  patientData: PatientData,
  manualValues: ManualLabValues
): Promise<InterpretationResponse> {
  const idade = parseInt(patientData.idade, 10) || 0;

  const payload: Record<string, number | string> = {
    genero: patientData.genero,
    idade,
  };

  (Object.keys(manualValues) as (keyof ManualLabValues)[]).forEach((key) => {
    const raw = manualValues[key];
    if (raw !== '' && raw != null) {
      const valor = parseFloat(String(raw).replace(',', '.'));
      if (!Number.isNaN(valor)) {
        payload[key] = valor;
      }
    }
  });

  const response = await api.post<InterpretationResponse>('/interpret-manual', payload, {
    headers: { 'Content-Type': 'application/json' },
  });
  return response.data;
}

// Representa um PDF escolhido pelo usuário (via expo-document-picker).
export interface PickedPdf {
  uri: string;
  name: string;
  mimeType?: string;
}

export async function interpretLabPdf(
  patientData: PatientData,
  pdf: PickedPdf
): Promise<InterpretationResponse> {
  const idade = parseInt(patientData.idade, 10) || 0;

  // No React Native, arquivos vão no FormData como { uri, name, type }.
  const formData = new FormData();
  formData.append('file', {
    uri: pdf.uri,
    name: pdf.name || 'laudo.pdf',
    type: pdf.mimeType || 'application/pdf',
  } as any);
  formData.append('genero', patientData.genero);
  formData.append('idade', String(idade));

  const response = await api.post<InterpretationResponse>('/interpret', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 300000, // 5 min: upload + extração + OCR podem demorar
  });
  return response.data;
}
