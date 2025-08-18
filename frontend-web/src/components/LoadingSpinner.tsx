import React, { useState, useEffect } from 'react';

interface LoadingSpinnerProps {
  message?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ message }) => {
  const [dots, setDots] = useState('');
  const [timeElapsed, setTimeElapsed] = useState(0);

  useEffect(() => {
    const dotsInterval = setInterval(() => {
      setDots(prev => prev.length >= 3 ? '' : prev + '.');
    }, 500);

    const timeInterval = setInterval(() => {
      setTimeElapsed(prev => prev + 1);
    }, 1000);

    return () => {
      clearInterval(dotsInterval);
      clearInterval(timeInterval);
    };
  }, []);

  const getTimeMessage = () => {
    if (timeElapsed < 30) {
      return 'Processando arquivo...';
    } else if (timeElapsed < 60) {
      return 'Analisando dados laboratoriais...';
    } else if (timeElapsed < 120) {
      return 'Servidor pode estar inicializando (primeira vez)...';
    } else if (timeElapsed < 180) {
      return 'Aguarde, processamento complexo em andamento...';
    } else {
      return 'Quase pronto, últimos ajustes...';
    }
  };

  const getHintMessage = () => {
    if (timeElapsed < 30) {
      return 'Isso pode levar alguns segundos';
    } else if (timeElapsed < 60) {
      return 'Em dispositivos móveis pode demorar um pouco mais';
    } else if (timeElapsed < 120) {
      return 'Primeira análise pode levar até 5 minutos';
    } else {
      return 'Aguarde, o servidor está processando...';
    }
  };

  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>{message || getTimeMessage()}{dots}</p>
      <p className="loading-hint">{getHintMessage()}</p>
      <div className="loading-progress">
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ 
              width: `${Math.min((timeElapsed / 300) * 100, 100)}%`,
              transition: 'width 1s ease-in-out'
            }}
          ></div>
        </div>
        <p className="time-elapsed">
          {Math.floor(timeElapsed / 60)}:{(timeElapsed % 60).toString().padStart(2, '0')}
        </p>
      </div>
      {timeElapsed > 120 && (
        <div className="patience-message">
          🙏 Obrigado pela paciência! O servidor gratuito pode demorar na primeira vez.
        </div>
      )}
    </div>
  );
};

export default LoadingSpinner;