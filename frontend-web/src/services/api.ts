import axios, { AxiosError } from 'axios';
import { InterpretationResponse, PatientData } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutos para aguardar cold start do Render
  headers: {
    'Accept': 'application/json',
  },
});

// Verificar conectividade de rede
const isOnline = (): boolean => {
  return navigator.onLine;
};

// Aguardar conectividade se offline
const waitForConnection = async (maxWait: number = 10000): Promise<void> => {
  if (isOnline()) return;
  
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      window.removeEventListener('online', onOnline);
      reject(new Error('Sem conexão com a internet'));
    }, maxWait);
    
    const onOnline = () => {
      clearTimeout(timeout);
      window.removeEventListener('online', onOnline);
      resolve();
    };
    
    window.addEventListener('online', onOnline);
  });
};

// Função para retry com backoff exponencial melhorada
const retryRequest = async <T>(
  requestFn: () => Promise<T>,
  maxRetries: number = 5,
  baseDelay: number = 2000
): Promise<T> => {
  // Verificar conectividade antes de tentar
  await waitForConnection();
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await requestFn();
    } catch (error) {
      const isLastAttempt = attempt === maxRetries;
      const isNetworkError = error instanceof AxiosError && 
        (error.code === 'ECONNABORTED' || 
         error.code === 'NETWORK_ERROR' || 
         error.code === 'ETIMEDOUT' ||
         !error.response ||
         (error.response && error.response.status >= 500));
      
      if (isLastAttempt) {
        // Adicionar contexto ao erro final
        const errorMessage = isNetworkError 
          ? `Erro de conectividade após ${maxRetries + 1} tentativas. Verifique sua conexão e tente novamente.`
          : error instanceof AxiosError && error.response
          ? `Erro do servidor: ${error.response.status} - ${error.response.statusText}`
          : 'Erro desconhecido na comunicação com o servidor';
        throw new Error(errorMessage);
      }
      
      if (!isNetworkError) {
        throw error;
      }
      
      // Aguardar conectividade se perdeu a conexão
      if (!isOnline()) {
        try {
          await waitForConnection(5000);
        } catch {
          // Continue tentando mesmo sem detectar conexão
        }
      }
      
      // Aguardar antes do próximo retry (backoff exponencial)
      const delay = baseDelay * Math.pow(2, attempt);
      console.log(`Tentativa ${attempt + 1}/${maxRetries + 1} falhou. Tentando novamente em ${delay}ms...`);
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
  
  // Converter idade para número, usando 0 como padrão se vazio
  const idade = typeof patientData.idade === 'string' && patientData.idade === '' 
    ? 0 
    : typeof patientData.idade === 'string' 
    ? parseInt(patientData.idade) || 0
    : patientData.idade;
  
  formData.append('idade', idade.toString());

  return retryRequest(async () => {
    const response = await api.post<InterpretationResponse>('/interpret', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 300000, // 5 minutos para upload e processamento
    });
    return response.data;
  }, 3, 3000); // 3 tentativas com delay maior para uploads
};

export const healthCheck = async (): Promise<{ status: string; message: string }> => {
  return retryRequest(async () => {
    const response = await api.get('/health', {
      timeout: 60000, // 1 minuto para health check
    });
    return response.data;
  }, 3, 1000); // 3 tentativas com delay menor para health check
};

// Health check robusto com múltiplas tentativas
export const robustHealthCheck = async (): Promise<{
  isOnline: boolean;
  latency?: number;
  error?: string;
}> => {
  const startTime = Date.now();
  
  try {
    await healthCheck();
    const latency = Date.now() - startTime;
    return { isOnline: true, latency };
  } catch (error) {
    return {
      isOnline: false,
      error: error instanceof Error ? error.message : 'Erro desconhecido'
    };
  }
};

// Verificar status da API com feedback detalhado
export const getApiStatus = async (): Promise<{
  status: 'online' | 'offline' | 'slow';
  message: string;
  latency?: number;
}> => {
  const result = await robustHealthCheck();
  
  if (!result.isOnline) {
    return {
      status: 'offline',
      message: 'API offline. Verifique sua conexão ou aguarde o servidor inicializar.'
    };
  }
  
  if (result.latency && result.latency > 10000) {
    return {
      status: 'slow',
      message: 'API online mas com resposta lenta. Isso é normal no primeiro acesso.',
      latency: result.latency
    };
  }
  
  return {
    status: 'online',
    message: 'API funcionando normalmente',
    latency: result.latency
  };
};