import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import PatientForm from './components/PatientForm';
import ManualEntryForm from './components/ManualEntryForm';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorAlert from './components/ErrorAlert';
import { interpretLab, interpretLabManual, getApiStatus } from './services/api';
import { InterpretationResponse, PatientData, ManualLabValues } from './types';
import {
  initMobileDebugging,
  MobileDebugger,
  getDeviceInfo,
  detectMobileIssues
} from './utils/mobileDetection';
import { applyMobileOptimizations } from './utils/mobileOptimizations';
import './App.css';
import References from './components/References';

const EMPTY_MANUAL_VALUES: ManualLabValues = {
  hemacias: '', hemoglobina: '', hematocrito: '', vcm: '', hcm: '', chcm: '', rdw: '',
  leucocitos: '', neutrofilos: '', eosinofilos: '', basofilos: '', linfocitos: '',
  monocitos: '', plaquetas: '',
};

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [inputMode, setInputMode] = useState<'pdf' | 'manual'>('pdf');
  const [manualValues, setManualValues] = useState<ManualLabValues>(EMPTY_MANUAL_VALUES);
  const [patientData, setPatientData] = useState<PatientData>({
    genero: 'feminino',
    idade: ''
  });
  const [results, setResults] = useState<InterpretationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [errorDetail, setErrorDetail] = useState<string | null>(null);
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

  const hasManualValues = Object.values(manualValues).some((v) => v !== '');

  const handleAnalyze = async () => {
    if (inputMode === 'pdf' && !file) {
      setError('Por favor, selecione um arquivo PDF');
      return;
    }

    if (inputMode === 'manual' && !hasManualValues) {
      setError('Por favor, informe ao menos um valor de exame');
      return;
    }

    if (!patientData.idade || patientData.idade === '') {
      setError('Por favor, informe a idade do paciente');
      return;
    }

    if (apiStatus === 'offline') {
      setError('Servidor offline. Verifique sua conexão ou aguarde o servidor inicializar.');
      return;
    }

    setLoading(true);
    setError(null);
    setErrorDetail(null);
    
    MobileDebugger.log('Iniciando análise', {
      inputMode,
      fileName: file?.name,
      fileSize: file?.size,
      fileType: file?.type,
      patientData,
      deviceType: deviceInfo.isMobile ? 'mobile' : deviceInfo.isTablet ? 'tablet' : 'desktop'
    });

    try {
      const startTime = Date.now();
      const response = inputMode === 'manual'
        ? await interpretLabManual(patientData, manualValues)
        : await interpretLab(file as File, patientData);
      const analysisTime = Date.now() - startTime;
      
      setResults(response);
      
      MobileDebugger.log('Análise concluída com sucesso', {
        analysisTime,
        resultCount: response.lab_findings?.length || 0
      });
    } catch (err: any) {
      let errorMessage = 'Erro ao analisar o laudo';
      let errorDetailMsg: string | null = null;

      if (err.response?.status === 422 && err.response?.data?.detail) {
        errorDetailMsg = err.response.data.detail;
        errorMessage = 'Não foi possível interpretar o laudo enviado.';
      } else if (err.message) {
        errorMessage = err.message;
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      }

      setError(errorMessage);
      setErrorDetail(errorDetailMsg);
      
      MobileDebugger.log('Erro durante análise', {
        error: errorMessage,
        stack: err.stack,
        inputMode,
        fileName: file?.name,
        fileSize: file?.size
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
    setManualValues(EMPTY_MANUAL_VALUES);
    setError(null);
    setErrorDetail(null);
  };

  const switchMode = (mode: 'pdf' | 'manual') => {
    setInputMode(mode);
    setError(null);
    setErrorDetail(null);
  };

  const canAnalyze = inputMode === 'pdf' ? !!file : hasManualValues;

  return (
    <div className="App">
      <header className="App-header">
        <h1>🩸 Interpretador de Laudos de Hemograma</h1>
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
            <div className="supported-exams-info">
              <h3>📋 Tipo de Exame Suportado</h3>
              <p>🩸 O sistema aceita apenas laudos de <strong>Hemograma Completo</strong>.</p>
            </div>

            <div className="input-mode-toggle">
              <button
                type="button"
                className={`mode-tab ${inputMode === 'pdf' ? 'active' : ''}`}
                onClick={() => switchMode('pdf')}
              >
                📄 Enviar PDF
              </button>
              <button
                type="button"
                className={`mode-tab ${inputMode === 'manual' ? 'active' : ''}`}
                onClick={() => switchMode('manual')}
              >
                ✍️ Digitar valores
              </button>
            </div>

            {inputMode === 'pdf' ? (
              <FileUpload file={file} onFileSelect={setFile} />
            ) : (
              <ManualEntryForm values={manualValues} onChange={setManualValues} />
            )}
            <PatientForm data={patientData} onChange={setPatientData} />

            <button
              onClick={handleAnalyze}
              disabled={!canAnalyze || !patientData.idade || patientData.idade === '' || loading || apiStatus === 'offline'}
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
                {errorDetail && (
                  <ErrorAlert
                    title="Não foi possível interpretar o laudo"
                    detail={errorDetail}
                    causes={[
                      'O tipo de exame enviado pode não estar entre os suportados atualmente. Apenas são aceitos exames do tipo Hemograma neste sistema.',
                      'PDF corrompido ou com formato/layout não suportado',
                      'Texto do laudo ilegível, muito distorcido ou apenas imagem',
                      'O arquivo não contém resultados de exames laboratoriais'
                    ]}
                    suggestions={[
                      'Verifique se o laudo é de um dos tipos suportados: Hemograma, Coagulograma ou Bioquímica Básica',
                      'Tente enviar outro PDF ou exportar novamente o laudo em melhor qualidade',
                      'Verifique se o PDF possui texto selecionável (não apenas imagens)',
                      'Se o problema persistir, verifique se o laudo segue formatos comuns de laboratórios'
                    ]}
                  />
                )}
              </div>
            )}
          </div>
        ) : (
          <ResultsDisplay results={results} onReset={handleReset} />
        )}
        <References />
      </main>
    </div>
  );
}

export default App;
