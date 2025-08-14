import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import PatientForm from './components/PatientForm';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import { interpretLab, healthCheck } from './services/api';
import { InterpretationResponse, PatientData } from './types';
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
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  useEffect(() => {
    const checkApi = async () => {
      try {
        await healthCheck();
        setApiStatus('online');
      } catch {
        setApiStatus('offline');
      }
    };
    checkApi();
  }, []);

  const handleAnalyze = async () => {
    if (!file) {
      setError('Por favor, selecione um arquivo PDF');
      return;
    }

    if (apiStatus === 'offline') {
      setError('API offline. Verifique se o backend está rodando.');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await interpretLab(file, patientData);
      setResults(response);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Erro ao analisar o laudo';
      setError(errorMessage);
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
          {apiStatus === 'checking' && '🔄 Verificando API...'}
          {apiStatus === 'online' && '🟢 API Online'}
          {apiStatus === 'offline' && '🔴 API Offline'}
        </div>
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
              {loading ? '⏳ Analisando...' : '🔍 Analisar Laudo'}
            </button>
            
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
