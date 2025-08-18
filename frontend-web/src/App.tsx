import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import PatientForm from './components/PatientForm';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import { interpretLab, getApiStatus } from './services/api';
import { InterpretationResponse, PatientData } from './types';
import { 
  initMobileDebugging, 
  MobileDebugger, 
  getDeviceInfo, 
  detectMobileIssues,
  isMobileDevice 
} from './utils/mobileDetection';
import { applyMobileOptimizations } from './utils/mobileOptimizations';
import './App.css';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [patientData, setPatientData] = useState<PatientData>({
    genero: 'feminino',
    idade: 30
  });
  const [results, setResults] = useState<InterpretationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline' | 'slow'>('checking');
  const [apiMessage, setApiMessage] = useState<string>('Verificando conexão...');
  const [connectionAttempts, setConnectionAttempts] = useState(0);
  const [deviceInfo] = useState(() => getDeviceInfo());
  const [mobileIssues] = useState(() => detectMobileIssues());

  useEffect(() => {
    // Inicializa debugging mobile
    initMobileDebugging();
    
    // Aplica otimizações mobile
    if (deviceInfo.isMobile || deviceInfo.isTablet) {
      applyMobileOptimizations();
      MobileDebugger.log('Otimizações mobile aplicadas');
    }
    
    // Log informações do dispositivo
    MobileDebugger.log('App inicializado', {
      deviceInfo,
      mobileIssues,
      url: window.location.href
    });
    
    const checkApi = async () => {
      setApiStatus('checking');
      setApiMessage('Verificando conexão com o servidor...');
      
      MobileDebugger.log('Iniciando verificação de API');
      
      try {
        const status = await getApiStatus();
        setApiStatus(status.status);
        setApiMessage(status.message);
        setConnectionAttempts(0);
        
        MobileDebugger.log('Resposta da API recebida', {
          status: status.status,
          message: status.message,
          isMobile: deviceInfo.isMobile
        });
      } catch (error) {
        setConnectionAttempts(prev => prev + 1);
        setApiStatus('offline');
        setApiMessage(
          connectionAttempts > 2 
            ? 'Servidor pode estar inicializando. Aguarde alguns minutos e tente novamente.'
            : 'Tentando conectar ao servidor...'
        );
        
        MobileDebugger.log('Erro ao verificar API', { 
          error: error instanceof Error ? error.message : 'Erro desconhecido',
          stack: error instanceof Error ? error.stack : undefined,
          attempts: connectionAttempts
        });
        
        // Tentar novamente após um delay se offline
        if (connectionAttempts < 5) {
          setTimeout(checkApi, 5000 + (connectionAttempts * 2000));
        }
      }
    };
    
    checkApi();
    
    // Log específico para dispositivos móveis
    if (deviceInfo.isMobile || deviceInfo.isTablet) {
      MobileDebugger.log('Dispositivo móvel detectado', {
        type: deviceInfo.isMobile ? 'mobile' : 'tablet',
        browser: deviceInfo.browser,
        os: deviceInfo.os,
        screen: `${deviceInfo.screenWidth}x${deviceInfo.screenHeight}`,
        issues: mobileIssues
      });
      
      // Mostra alerta se há problemas críticos
      if (mobileIssues.length > 0) {
        console.warn('Problemas detectados no dispositivo móvel:', mobileIssues);
      }
    }
  }, [connectionAttempts, deviceInfo, mobileIssues]);

  const handleAnalyze = async () => {
    if (!file) {
      setError('Por favor, selecione um arquivo PDF');
      return;
    }

    if (apiStatus === 'offline') {
      setError('Servidor offline. Verifique sua conexão ou aguarde o servidor inicializar.');
      return;
    }

    setLoading(true);
    setError(null);
    
    MobileDebugger.log('Iniciando análise de arquivo', {
      fileName: file.name,
      fileSize: file.size,
      fileType: file.type,
      patientData,
      deviceType: deviceInfo.isMobile ? 'mobile' : deviceInfo.isTablet ? 'tablet' : 'desktop'
    });
    
    try {
      const startTime = Date.now();
      const response = await interpretLab(file, patientData);
      const analysisTime = Date.now() - startTime;
      
      setResults(response);
      
      MobileDebugger.log('Análise concluída com sucesso', {
        analysisTime,
        resultCount: response.lab_findings?.length || 0
      });
    } catch (err: any) {
      let errorMessage = 'Erro ao analisar o laudo';
      
      if (err.message) {
        errorMessage = err.message;
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      }
      
      setError(errorMessage);
      
      MobileDebugger.log('Erro durante análise', {
        error: errorMessage,
        stack: err.stack,
        fileName: file.name,
        fileSize: file.size
      });
      
      // Se erro de conectividade, verificar status da API novamente
      if (err.message?.includes('conectividade') || err.message?.includes('timeout')) {
        setTimeout(async () => {
          try {
            const status = await getApiStatus();
            setApiStatus(status.status);
            setApiMessage(status.message);
          } catch {
            setApiStatus('offline');
            setApiMessage('Servidor offline. Tente novamente em alguns minutos.');
          }
        }, 2000);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setFile(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🧬 Interpretador de Laudos Laboratoriais</h1>
        <div className={`api-status ${apiStatus}`}>
          {apiStatus === 'checking' && '🔄 Verificando conexão...'}
          {apiStatus === 'online' && '🟢 Servidor Online'}
          {apiStatus === 'slow' && '🟡 Servidor Lento'}
          {apiStatus === 'offline' && '🔴 Servidor Offline'}
        </div>
        {apiMessage && (
          <div className="api-message">
            {apiMessage}
          </div>
        )}
      </header>
      
      <main className="App-main">
        {!results ? (
          <div className="upload-section">
            <FileUpload file={file} onFileSelect={setFile} />
            <PatientForm data={patientData} onChange={setPatientData} />
            
            <button 
              onClick={handleAnalyze} 
              disabled={!file || loading || apiStatus === 'offline'}
              className="analyze-button"
            >
              {loading ? '⏳ Processando...' : apiStatus === 'slow' ? '🐌 Analisar (Pode ser lento)' : '🔍 Analisar Laudo'}
            </button>
            
            {apiStatus === 'slow' && (
              <div className="slow-warning">
                ⚠️ Primeira análise pode demorar até 5 minutos (servidor inicializando)
              </div>
            )}
            
            {loading && <LoadingSpinner />}
            {error && (
              <div className="error-message">
                ❌ {error}
              </div>
            )}
          </div>
        ) : (
          <ResultsDisplay results={results} onReset={handleReset} />
        )}
      </main>
    </div>
  );
}

export default App;
