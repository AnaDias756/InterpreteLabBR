import React from 'react';
import ReactDOM from 'react-dom/client';
import './utils/polyfills'; // Carrega polyfills primeiro
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { initPolyfills, checkFeatureSupport } from './utils/polyfills';
import { MobileDebugger } from './utils/mobileDetection';

// Inicializa polyfills
initPolyfills();

// Verifica suporte a funcionalidades
const featureSupport = checkFeatureSupport();
MobileDebugger.log('Verificação de suporte a funcionalidades', featureSupport);

// Verifica se há funcionalidades críticas não suportadas
const criticalFeatures = ['fetch', 'promise', 'addEventListener'];
const missingCriticalFeatures = criticalFeatures.filter(feature => !featureSupport[feature]);

if (missingCriticalFeatures.length > 0) {
  MobileDebugger.log('Funcionalidades críticas não suportadas', { missing: missingCriticalFeatures });
  console.warn('Navegador muito antigo detectado. Algumas funcionalidades podem não funcionar:', missingCriticalFeatures);
}

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

try {
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
  MobileDebugger.log('Aplicação React renderizada com sucesso');
} catch (error) {
  MobileDebugger.log('Erro ao renderizar aplicação React', {
    error: error instanceof Error ? error.message : 'Erro desconhecido',
    stack: error instanceof Error ? error.stack : undefined
  });
  
  // Fallback para navegadores muito antigos
  const rootElement = document.getElementById('root');
  if (rootElement) {
    rootElement.innerHTML = `
      <div style="padding: 20px; text-align: center; font-family: Arial, sans-serif;">
        <h2>Navegador não suportado</h2>
        <p>Seu navegador é muito antigo para executar esta aplicação.</p>
        <p>Por favor, atualize seu navegador ou use um navegador mais moderno.</p>
        <p>Navegadores recomendados:</p>
        <ul style="text-align: left; display: inline-block;">
          <li>Chrome 60+</li>
          <li>Firefox 55+</li>
          <li>Safari 12+</li>
          <li>Edge 79+</li>
        </ul>
      </div>
    `;
  }
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
