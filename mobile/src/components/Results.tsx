import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { InterpretationResponse, RawLabValue } from '../types';
import { colors, classColor, classLabel } from '../theme';
import ReferenceComparisonTable from './ReferenceComparisonTable';

interface Props {
  results: InterpretationResponse;
  onReset: () => void;
}

// Renderiza **negrito** e *itálico* dentro de uma linha de texto
const renderInline = (text: string, baseKey: string): React.ReactNode[] => {
  const nodes: React.ReactNode[] = [];
  const regex = /\*\*([^*]+)\*\*|\*([^*]+)\*/g;
  let lastIndex = 0;
  let key = 0;
  let match: RegExpExecArray | null;
  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) nodes.push(text.slice(lastIndex, match.index));
    if (match[1] !== undefined) {
      nodes.push(<Text key={`${baseKey}-b${key++}`} style={styles.bold}>{match[1]}</Text>);
    } else {
      nodes.push(<Text key={`${baseKey}-i${key++}`} style={styles.italic}>{match[2]}</Text>);
    }
    lastIndex = regex.lastIndex;
  }
  if (lastIndex < text.length) nodes.push(text.slice(lastIndex));
  return nodes;
};

const Briefing: React.FC<{ text: string }> = ({ text }) => {
  const paragrafos = text.split(/\n{2,}/);
  return (
    <View>
      {paragrafos.map((p, i) => (
        <Text key={i} style={styles.briefingParagraph}>
          {renderInline(p.replace(/\n/g, ' '), `p${i}`)}
        </Text>
      ))}
    </View>
  );
};

const Results: React.FC<Props> = ({ results, onReset }) => {
  const abnormalSet = new Set(
    (results.lab_findings || []).map((f) => (f.analito || '').toLowerCase().trim())
  );
  const normalValues: RawLabValue[] = (results.lab_values_raw || []).filter(
    (v) => !abnormalSet.has((v.analito || '').toLowerCase().trim())
  );

  return (
    <View>
      <View style={styles.headerRow}>
        <Text style={styles.headerTitle}>📋 Resultados</Text>
        <TouchableOpacity style={styles.resetBtn} onPress={onReset}>
          <Text style={styles.resetText}>🔄 Nova análise</Text>
        </TouchableOpacity>
      </View>

      {results.lab_findings.length > 0 ? (
        <>
          <Text style={styles.sectionTitle}>🚨 Achados Anormais ({results.lab_findings.length})</Text>
          {results.lab_findings.map((f, i) => (
            <View key={i} style={styles.card}>
              <View style={styles.cardHeader}>
                <Text style={styles.cardTitle}>{f.analito}</Text>
                <View style={[styles.badge, { backgroundColor: classColor(f.resultado) }]}>
                  <Text style={styles.badgeText}>{classLabel(f.resultado)}</Text>
                </View>
              </View>
              <Text style={styles.cardLine}><Text style={styles.bold}>Valor:</Text> {f.valor}</Text>
              <Text style={styles.cardLine}><Text style={styles.bold}>Especialidade:</Text> {f.especialidade}</Text>
            </View>
          ))}

          <Text style={styles.sectionTitle}>👨‍⚕️ Especialidades Recomendadas</Text>
          <View style={styles.chipsRow}>
            {results.recommended_specialties.map((s, i) => (
              <View key={i} style={styles.chip}><Text style={styles.chipText}>{s}</Text></View>
            ))}
          </View>

          <Text style={styles.sectionTitle}>📝 Resumo para o Paciente</Text>
          <View style={styles.briefingBox}>
            <Briefing text={results.patient_briefing} />
          </View>
        </>
      ) : (
        <View style={styles.noFindings}>
          <Text style={styles.noFindingsTitle}>✅ Nenhum Achado Anormal</Text>
          <Text style={styles.cardLine}>Todos os valores analisados estão dentro dos parâmetros (PNS).</Text>
        </View>
      )}

      {normalValues.length > 0 && (
        <>
          <Text style={styles.sectionTitle}>✅ Achados Normais ({normalValues.length})</Text>
          {normalValues.map((item, i) => (
            <View key={`n${i}`} style={styles.card}>
              <View style={styles.cardHeader}>
                <Text style={styles.cardTitle}>{item.analito}</Text>
                <View style={[styles.badge, { backgroundColor: colors.normal }]}>
                  <Text style={styles.badgeText}>Normal</Text>
                </View>
              </View>
              <Text style={styles.cardLine}><Text style={styles.bold}>Valor:</Text> {item.valor}</Text>
            </View>
          ))}
        </>
      )}

      {results.comparacao_referencias && results.comparacao_referencias.length > 0 && (
        <ReferenceComparisonTable itens={results.comparacao_referencias} />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  headerRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  headerTitle: { fontSize: 18, fontWeight: '700', color: colors.text },
  resetBtn: { backgroundColor: colors.normal, paddingHorizontal: 12, paddingVertical: 8, borderRadius: 8 },
  resetText: { color: '#fff', fontWeight: '600', fontSize: 13 },
  sectionTitle: { fontSize: 15, fontWeight: '700', color: colors.text, marginTop: 16, marginBottom: 8 },
  card: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 10,
    padding: 12,
    marginBottom: 8,
  },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 },
  cardTitle: { fontSize: 15, fontWeight: '700', color: colors.text },
  cardLine: { fontSize: 13, color: '#333', marginTop: 2 },
  badge: { paddingHorizontal: 10, paddingVertical: 3, borderRadius: 12 },
  badgeText: { color: '#fff', fontWeight: '700', fontSize: 12 },
  chipsRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  chip: { backgroundColor: colors.primary, paddingHorizontal: 12, paddingVertical: 6, borderRadius: 16 },
  chipText: { color: '#fff', fontWeight: '600', fontSize: 13 },
  briefingBox: {
    backgroundColor: '#eef4ff',
    borderRadius: 10,
    padding: 14,
  },
  briefingParagraph: { fontSize: 14, color: '#333', lineHeight: 21, marginBottom: 10 },
  bold: { fontWeight: '700' },
  italic: { fontStyle: 'italic' },
  noFindings: { backgroundColor: '#e9f7ef', borderRadius: 10, padding: 16, alignItems: 'center' },
  noFindingsTitle: { fontSize: 16, fontWeight: '700', color: colors.normal, marginBottom: 6 },
});

export default Results;
