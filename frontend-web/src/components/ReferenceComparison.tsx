import React from 'react';
import { ReferenceComparison as ReferenceComparisonItem } from '../types';

interface ReferenceComparisonProps {
  itens: ReferenceComparisonItem[];
}

const badgeColor = (classificacao: string): string => {
  const c = classificacao.toLowerCase();
  if (c === 'alto') return '#dc3545';
  if (c === 'baixo') return '#007bff';
  if (c === 'normal') return '#28a745';
  return '#9e9e9e'; // sem referência
};

const rotulo = (classificacao: string): string => {
  const c = classificacao.toLowerCase();
  if (c === 'alto') return 'Alto';
  if (c === 'baixo') return 'Baixo';
  if (c === 'normal') return 'Normal';
  return '—';
};

const Badge: React.FC<{ classificacao: string }> = ({ classificacao }) => (
  <span className="ref-badge" style={{ backgroundColor: badgeColor(classificacao) }}>
    {rotulo(classificacao)}
  </span>
);

const ReferenceComparison: React.FC<ReferenceComparisonProps> = ({ itens }) => {
  if (!itens || itens.length === 0) return null;

  const divergentes = itens.filter((i) => i.divergente).length;

  return (
    <div className="reference-comparison-section">
      <h3>🔬 Comparação de Referências</h3>
      <p className="ref-explain">
        Este sistema classifica usando os <strong>valores de referência da população
        adulta brasileira (PNS)</strong>. Muitos laboratórios usam faixas de livros-texto
        estrangeiros, que podem divergir — especialmente na série branca. Veja a comparação:
      </p>

      {divergentes > 0 && (
        <p className="ref-divergence-note">
          ⚠️ {divergentes} {divergentes === 1 ? 'analito diverge' : 'analitos divergem'} entre as duas referências.
        </p>
      )}

      <div className="ref-table-wrapper">
        <table className="ref-table">
          <thead>
            <tr>
              <th>Analito</th>
              <th>Valor</th>
              <th>PNS (Brasil)</th>
              <th>Lab. (clássica)</th>
            </tr>
          </thead>
          <tbody>
            {itens.map((item, index) => (
              <tr key={index} className={item.divergente ? 'ref-row-divergent' : ''}>
                <td>{item.analito}{item.divergente && <span className="ref-flag"> ⚠️</span>}</td>
                <td>{item.valor}</td>
                <td><Badge classificacao={item.classificacao_pns} /></td>
                <td><Badge classificacao={item.classificacao_lab} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="ref-footnote">
        Referência PNS: Rosenfeld et al. (2019). Referência laboratorial: faixas clássicas
        (Wintrobe; Dacie &amp; Lewis), como as impressas em laudos do SUS. Esta ferramenta
        não substitui a avaliação médica.
      </p>
    </div>
  );
};

export default ReferenceComparison;
