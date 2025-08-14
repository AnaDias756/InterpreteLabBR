import React from 'react';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Analisando laudo laboratorial...</p>
      <p className="loading-hint">Isso pode levar alguns segundos</p>
    </div>
  );
};

export default LoadingSpinner;