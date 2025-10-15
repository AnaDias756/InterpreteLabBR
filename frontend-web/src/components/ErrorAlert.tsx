import React from 'react';

interface ErrorAlertProps {
  title?: string;
  causes: string[];
  suggestions: string[];
  detail?: string | null;
}

const ErrorAlert: React.FC<ErrorAlertProps> = ({ title = 'Atenção', causes, suggestions, detail }) => {
  return (
    <div className="error-alert" role="alert" aria-live="assertive">
      <h3 className="error-alert-title">{title}</h3>
      {detail && (
        <p className="error-alert-detail">{detail}</p>
      )}
      <div className="error-alert-section">
        <strong>Possíveis causas:</strong>
        <ul>
          {causes.map((c, idx) => (
            <li key={idx}>{c}</li>
          ))}
        </ul>
      </div>
      <div className="error-alert-section">
        <strong>Sugestões:</strong>
        <ul>
          {suggestions.map((s, idx) => (
            <li key={idx}>{s}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ErrorAlert;
   