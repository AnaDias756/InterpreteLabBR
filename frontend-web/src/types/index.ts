export interface LabFinding {
  analito: string;
  valor: number;
  resultado: string;
  severidade: number;
  especialidade: string;
  descricao_achado: string;
  diretriz: string;
}

export interface RawLabValue {
  analito: string;
  valor: number;
}

export interface InterpretationResponse {
  lab_findings: LabFinding[];
  recommended_specialties: string[];
  patient_briefing: string;
  lab_values_raw: RawLabValue[];
}

export interface PatientData {
  genero: 'masculino' | 'feminino';
  idade: number | string;
}

// Valores digitados manualmente (strings, pois vêm dos inputs do formulário)
export type ManualLabValues = {
  hemacias: string;
  hemoglobina: string;
  hematocrito: string;
  vcm: string;
  hcm: string;
  chcm: string;
  rdw: string;
  leucocitos: string;
  neutrofilos: string;
  eosinofilos: string;
  basofilos: string;
  linfocitos: string;
  monocitos: string;
  plaquetas: string;
};

export interface ApiError {
  detail: string;
}