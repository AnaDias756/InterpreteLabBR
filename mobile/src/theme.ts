export const colors = {
  primary: '#b00020',
  primaryDark: '#7f0017',
  bg: '#f2f3f5',
  card: '#ffffff',
  border: '#e1e4e8',
  text: '#1a1a1a',
  textMuted: '#666666',
  alto: '#dc3545',
  baixo: '#007bff',
  normal: '#28a745',
  semRef: '#9e9e9e',
  warningBg: '#fff8e1',
  warningText: '#8a6d00',
  online: '#28a745',
  offline: '#dc3545',
  checking: '#fd7e14',
};

export const classColor = (classificacao: string): string => {
  const c = classificacao.toLowerCase();
  if (c === 'alto') return colors.alto;
  if (c === 'baixo') return colors.baixo;
  if (c === 'normal') return colors.normal;
  return colors.semRef;
};

export const classLabel = (classificacao: string): string => {
  const c = classificacao.toLowerCase();
  if (c === 'alto') return 'Alto';
  if (c === 'baixo') return 'Baixo';
  if (c === 'normal') return 'Normal';
  return '—';
};
