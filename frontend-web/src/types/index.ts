export interface LabFinding {
  analito: string;
  valor: number;
  resultado: string;
  severidade: number;
  especialidade: string;
  descricao_achado: string;
  diretriz: string;
}

export interface InterpretationResponse {
  lab_findings: LabFinding[];
  recommended_specialties: string[];
  patient_briefing: string;
}

export interface PatientData {
  genero: 'masculino' | 'feminino';
  idade: number;
}

export interface ApiError {
  detail: string;
}