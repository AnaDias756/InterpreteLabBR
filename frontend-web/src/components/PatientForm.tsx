import React from 'react';
import { PatientData } from '../types';

interface PatientFormProps {
  data: PatientData;
  onChange: (data: PatientData) => void;
}

const PatientForm: React.FC<PatientFormProps> = ({ data, onChange }) => {
  return (
    <div className="patient-form">
      <h3>Dados do Paciente</h3>
      
      <div className="form-group">
        <label htmlFor="genero">Sexo Biológico:</label>
        <select
          id="genero"
          value={data.genero}
          onChange={(e) => onChange({ ...data, genero: e.target.value as 'masculino' | 'feminino' })}
        >
          <option value="feminino">Feminino</option>
          <option value="masculino">Masculino</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="idade">Idade:</label>
        <input
          type="number"
          id="idade"
          min="0"
          max="150"
          value={data.idade}
          placeholder="Digite sua idade"
          onChange={(e) => onChange({ ...data, idade: e.target.value === '' ? '' : parseInt(e.target.value) || '' })}
        />
        <span className="unit">anos</span>
      </div>
    </div>
  );
};

export default PatientForm;