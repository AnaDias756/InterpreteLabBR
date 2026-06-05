import React from 'react';
import { ManualLabValues } from '../types';

interface ManualEntryFormProps {
  values: ManualLabValues;
  onChange: (values: ManualLabValues) => void;
}

interface CampoConfig {
  key: keyof ManualLabValues;
  label: string;
  unidade: string;
  exemplo: string;
}

// Agrupamento dos analitos conforme o hemograma
const SERIE_VERMELHA: CampoConfig[] = [
  { key: 'hemacias', label: 'Hemácias', unidade: '10⁶/µL', exemplo: 'ex: 4,69' },
  { key: 'hemoglobina', label: 'Hemoglobina', unidade: 'g/dL', exemplo: 'ex: 14,6' },
  { key: 'hematocrito', label: 'Hematócrito', unidade: '%', exemplo: 'ex: 42,9' },
  { key: 'vcm', label: 'VCM', unidade: 'fL', exemplo: 'ex: 91,5' },
  { key: 'hcm', label: 'HCM', unidade: 'pg', exemplo: 'ex: 31,1' },
  { key: 'chcm', label: 'CHCM', unidade: 'g/dL', exemplo: 'ex: 34,0' },
  { key: 'rdw', label: 'RDW', unidade: '%', exemplo: 'ex: 11,8' },
];

const SERIE_BRANCA: CampoConfig[] = [
  { key: 'leucocitos', label: 'Leucócitos', unidade: '/µL', exemplo: 'ex: 3100' },
  { key: 'neutrofilos', label: 'Neutrófilos', unidade: '/µL', exemplo: 'ex: 1073' },
  { key: 'eosinofilos', label: 'Eosinófilos', unidade: '/µL', exemplo: 'ex: 22' },
  { key: 'basofilos', label: 'Basófilos', unidade: '/µL', exemplo: 'ex: 6' },
  { key: 'linfocitos', label: 'Linfócitos', unidade: '/µL', exemplo: 'ex: 1798' },
  { key: 'monocitos', label: 'Monócitos', unidade: '/µL', exemplo: 'ex: 202' },
];

const PLAQUETAS: CampoConfig[] = [
  { key: 'plaquetas', label: 'Plaquetas', unidade: '/µL', exemplo: 'ex: 116000' },
];

const ManualEntryForm: React.FC<ManualEntryFormProps> = ({ values, onChange }) => {
  const handleField = (key: keyof ManualLabValues, value: string) => {
    onChange({ ...values, [key]: value });
  };

  const renderCampos = (campos: CampoConfig[]) =>
    campos.map((campo) => (
      <div className="manual-field" key={campo.key}>
        <label htmlFor={`manual-${campo.key}`}>{campo.label}</label>
        <div className="manual-input-wrapper">
          <input
            id={`manual-${campo.key}`}
            type="text"
            inputMode="decimal"
            value={values[campo.key]}
            placeholder={campo.exemplo}
            onChange={(e) => handleField(campo.key, e.target.value)}
          />
          <span className="manual-unit">{campo.unidade}</span>
        </div>
      </div>
    ));

  return (
    <div className="manual-entry-form">
      <p className="manual-intro">
        Digite apenas os valores que você tem. Campos em branco são ignorados.
      </p>

      <fieldset className="manual-group">
        <legend>🔴 Série Vermelha (Eritrograma)</legend>
        <div className="manual-grid">{renderCampos(SERIE_VERMELHA)}</div>
      </fieldset>

      <fieldset className="manual-group">
        <legend>⚪ Série Branca (Leucograma)</legend>
        <p className="manual-hint">
          ⚠️ Informe o <strong>valor absoluto</strong> (/µL), não a porcentagem.
        </p>
        <div className="manual-grid">{renderCampos(SERIE_BRANCA)}</div>
      </fieldset>

      <fieldset className="manual-group">
        <legend>🟣 Plaquetas</legend>
        <div className="manual-grid">{renderCampos(PLAQUETAS)}</div>
      </fieldset>
    </div>
  );
};

export default ManualEntryForm;
