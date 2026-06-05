import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { ReferenceComparison } from '../types';
import { colors, classColor, classLabel } from '../theme';

interface Props {
  itens: ReferenceComparison[];
}

const Badge: React.FC<{ classificacao: string }> = ({ classificacao }) => (
  <View style={[styles.badge, { backgroundColor: classColor(classificacao) }]}>
    <Text style={styles.badgeText}>{classLabel(classificacao)}</Text>
  </View>
);

const ReferenceComparisonTable: React.FC<Props> = ({ itens }) => {
  if (!itens || itens.length === 0) return null;
  const divergentes = itens.filter((i) => i.divergente).length;

  return (
    <View style={styles.section}>
      <Text style={styles.title}>🔬 Comparação de Referências</Text>
      <Text style={styles.explain}>
        A classificação usa os valores de referência da população adulta brasileira (PNS).
        Muitos laboratórios usam faixas de livros-texto estrangeiros, que podem divergir —
        especialmente na série branca.
      </Text>

      {divergentes > 0 && (
        <Text style={styles.divergenceNote}>
          ⚠️ {divergentes} {divergentes === 1 ? 'analito diverge' : 'analitos divergem'} entre as duas referências.
        </Text>
      )}

      <View style={styles.headerRow}>
        <Text style={[styles.hCell, styles.colAnalito]}>Analito</Text>
        <Text style={[styles.hCell, styles.colValor]}>Valor</Text>
        <Text style={[styles.hCell, styles.colRef]}>PNS</Text>
        <Text style={[styles.hCell, styles.colRef]}>Lab.</Text>
      </View>

      {itens.map((item, index) => (
        <View key={index} style={[styles.row, item.divergente && styles.rowDivergent]}>
          <Text style={[styles.cell, styles.colAnalito]}>
            {item.analito}{item.divergente ? ' ⚠️' : ''}
          </Text>
          <Text style={[styles.cell, styles.colValor]}>{item.valor}</Text>
          <View style={styles.colRef}><Badge classificacao={item.classificacao_pns} /></View>
          <View style={styles.colRef}><Badge classificacao={item.classificacao_lab} /></View>
        </View>
      ))}

      <Text style={styles.footnote}>
        Referência PNS: Rosenfeld et al. (2019). Referência laboratorial: faixas clássicas
        (Wintrobe; Dacie & Lewis). Esta ferramenta não substitui a avaliação médica.
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  section: {
    backgroundColor: '#fafbfc',
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 12,
    padding: 14,
    marginTop: 16,
  },
  title: { fontSize: 16, fontWeight: '700', color: colors.text, marginBottom: 8 },
  explain: { fontSize: 13, color: '#444', lineHeight: 19, marginBottom: 8 },
  divergenceNote: {
    fontSize: 13,
    color: colors.warningText,
    backgroundColor: colors.warningBg,
    borderRadius: 6,
    paddingHorizontal: 10,
    paddingVertical: 8,
    marginBottom: 10,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0f2f5',
    paddingVertical: 8,
    paddingHorizontal: 6,
    borderTopLeftRadius: 6,
    borderTopRightRadius: 6,
  },
  hCell: { fontSize: 12, fontWeight: '700', color: '#333' },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    paddingHorizontal: 6,
    borderBottomWidth: 1,
    borderBottomColor: '#eaecef',
  },
  rowDivergent: { backgroundColor: colors.warningBg },
  cell: { fontSize: 13, color: colors.text },
  colAnalito: { flex: 2.2 },
  colValor: { flex: 1.4 },
  colRef: { flex: 1.2, alignItems: 'flex-start' },
  badge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10 },
  badgeText: { color: '#fff', fontSize: 11, fontWeight: '700' },
  footnote: { fontSize: 11, color: colors.textMuted, marginTop: 10, lineHeight: 15 },
});

export default ReferenceComparisonTable;
