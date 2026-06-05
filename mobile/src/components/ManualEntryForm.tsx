import React from 'react';
import { View, Text, TextInput, StyleSheet } from 'react-native';
import { ManualLabValues } from '../types';
import { colors } from '../theme';

interface Props {
  values: ManualLabValues;
  onChange: (values: ManualLabValues) => void;
}

interface Campo {
  key: keyof ManualLabValues;
  label: string;
  unidade: string;
  exemplo: string;
}

const SERIE_VERMELHA: Campo[] = [
  { key: 'hemacias', label: 'Hemácias', unidade: '10⁶/µL', exemplo: '4,69' },
  { key: 'hemoglobina', label: 'Hemoglobina', unidade: 'g/dL', exemplo: '14,6' },
  { key: 'hematocrito', label: 'Hematócrito', unidade: '%', exemplo: '42,9' },
  { key: 'vcm', label: 'VCM', unidade: 'fL', exemplo: '91,5' },
  { key: 'hcm', label: 'HCM', unidade: 'pg', exemplo: '31,1' },
  { key: 'chcm', label: 'CHCM', unidade: 'g/dL', exemplo: '34,0' },
  { key: 'rdw', label: 'RDW', unidade: '%', exemplo: '11,8' },
];

const SERIE_BRANCA: Campo[] = [
  { key: 'leucocitos', label: 'Leucócitos', unidade: '/µL', exemplo: '3100' },
  { key: 'neutrofilos', label: 'Neutrófilos', unidade: '/µL', exemplo: '1073' },
  { key: 'eosinofilos', label: 'Eosinófilos', unidade: '/µL', exemplo: '22' },
  { key: 'basofilos', label: 'Basófilos', unidade: '/µL', exemplo: '6' },
  { key: 'linfocitos', label: 'Linfócitos', unidade: '/µL', exemplo: '1798' },
  { key: 'monocitos', label: 'Monócitos', unidade: '/µL', exemplo: '202' },
];

const PLAQUETAS: Campo[] = [
  { key: 'plaquetas', label: 'Plaquetas', unidade: '/µL', exemplo: '116000' },
];

const ManualEntryForm: React.FC<Props> = ({ values, onChange }) => {
  const handleField = (key: keyof ManualLabValues, text: string) => {
    onChange({ ...values, [key]: text.replace(/[^0-9.,]/g, '') });
  };

  const renderCampos = (campos: Campo[]) =>
    campos.map((campo) => (
      <View style={styles.fieldRow} key={campo.key}>
        <Text style={styles.fieldLabel}>{campo.label}</Text>
        <TextInput
          style={styles.input}
          keyboardType="decimal-pad"
          value={values[campo.key]}
          placeholder={`ex: ${campo.exemplo}`}
          placeholderTextColor="#999"
          onChangeText={(t) => handleField(campo.key, t)}
        />
        <Text style={styles.unit}>{campo.unidade}</Text>
      </View>
    ));

  return (
    <View style={styles.container}>
      <Text style={styles.intro}>
        Digite apenas os valores que você tem. Campos em branco são ignorados.
      </Text>

      <View style={styles.group}>
        <Text style={styles.legend}>🔴 Série Vermelha (Eritrograma)</Text>
        {renderCampos(SERIE_VERMELHA)}
      </View>

      <View style={styles.group}>
        <Text style={styles.legend}>⚪ Série Branca (Leucograma)</Text>
        <Text style={styles.hint}>⚠️ Informe o valor absoluto (/µL), não a porcentagem.</Text>
        {renderCampos(SERIE_BRANCA)}
      </View>

      <View style={styles.group}>
        <Text style={styles.legend}>🟣 Plaquetas</Text>
        {renderCampos(PLAQUETAS)}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { marginBottom: 16 },
  intro: { fontSize: 13, color: colors.textMuted, marginBottom: 12 },
  group: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 12,
    padding: 14,
    marginBottom: 14,
  },
  legend: { fontSize: 15, fontWeight: '700', color: colors.primary, marginBottom: 10 },
  hint: {
    fontSize: 12,
    color: colors.warningText,
    backgroundColor: colors.warningBg,
    borderRadius: 6,
    paddingHorizontal: 8,
    paddingVertical: 6,
    marginBottom: 10,
  },
  fieldRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 8, gap: 8 },
  fieldLabel: { width: 96, fontSize: 13, fontWeight: '600', color: colors.text },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 6,
    paddingHorizontal: 10,
    paddingVertical: 8,
    fontSize: 15,
    color: colors.text,
  },
  unit: { width: 52, fontSize: 12, color: colors.textMuted },
});

export default ManualEntryForm;
