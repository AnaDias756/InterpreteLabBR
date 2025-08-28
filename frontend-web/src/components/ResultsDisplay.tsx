import React from 'react';
import { InterpretationResponse } from '../types';

interface ResultsDisplayProps {
  results: InterpretationResponse;
  onReset: () => void;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results, onReset }) => {
  const getResultColor = (resultado: string) => {
    const resultadoLower = resultado.toLowerCase();
    if (resultadoLower === 'alto') return '#dc3545'; // Vermelho
    if (resultadoLower === 'baixo') return '#007bff'; // Azul
    return '#28a745'; // Verde para Normal
  };

  const getResultText = (resultado: string) => {
    const resultadoLower = resultado.toLowerCase();
    if (resultadoLower === 'alto') return 'Alto';
    if (resultadoLower === 'baixo') return 'Baixo';
    return 'Normal';
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>📋 Resultados da Análise</h2>
        <button onClick={onReset} className="new-analysis-btn">
          🔄 Nova Análise
        </button>
      </div>

      {results.lab_findings.length > 0 ? (
        <>
          <div className="findings-section">
            <h3>🚨 Achados Anormais ({results.lab_findings.length})</h3>
            <div className="findings-grid">
              {results.lab_findings.map((finding, index) => (
                <div key={index} className="finding-card">
                  <div className="finding-header">
                    <h4>{finding.analito}</h4>
                    <span 
                      className="result-badge"
                      style={{ backgroundColor: getResultColor(finding.resultado) }}
                    >
                      {getResultText(finding.resultado)}
                    </span>
                  </div>
                  
                  <div className="finding-details">
                    <p><strong>Valor:</strong> {finding.valor}</p>
                    <p><strong>Resultado:</strong> {finding.resultado}</p>
                    <p><strong>Especialidade:</strong> {finding.especialidade}</p>
                    <p><strong>Descrição:</strong> {finding.descricao_achado}</p>
                    {finding.diretriz && (
                      <p><strong>Diretriz:</strong> {finding.diretriz}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="specialties-section">
            <h3>👨‍⚕️ Especialidades Recomendadas</h3>
            <div className="specialties-list">
              {results.recommended_specialties.map((specialty, index) => (
                <span key={index} className="specialty-tag">
                  {specialty}
                </span>
              ))}
            </div>
          </div>

          <div className="briefing-section">
            <h3>📝 Resumo para o Paciente</h3>
            <div className="briefing-content">
              {results.patient_briefing}
            </div>
          </div>
        </>
      ) : (
        <div className="no-findings">
          <h3>✅ Nenhum Achado Anormal</h3>
          <p>Todos os valores analisados estão dentro dos parâmetros normais.</p>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;