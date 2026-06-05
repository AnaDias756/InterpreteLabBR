import React from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { PatientData } from '../types';
import { colors } from '../theme';

interface Props {
  data: PatientData;
  onChange: (data: PatientData) => void;
}

const PatientForm: React.FC<Props> = ({ data, onChange }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Dados do Paciente</Text>

      <Text style={styles.label}>Sexo biológico</Text>
      <View style={styles.row}>
        {(['feminino', 'masculino'] as const).map((g) => (
          <TouchableOpacity
            key={g}
            style={[styles.genderBtn, data.genero === g && styles.genderBtnActive]}
            onPress={() => onChange({ ...data, genero: g })}
          >
            <Text style={[styles.genderText, data.genero === g && styles.genderTextActive]}>
              {g === 'feminino' ? 'Feminino' : 'Masculino'}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={[styles.label, { marginTop: 14 }]}>Idade</Text>
      <View style={styles.ageRow}>
        <TextInput
          style={styles.ageInput}
          keyboardType="number-pad"
          value={data.idade}
          placeholder="Ex: 35"
          placeholderTextColor="#999"
          onChangeText={(t) => onChange({ ...data, idade: t.replace(/[^0-9]/g, '') })}
          maxLength={3}
        />
        <Text style={styles.unit}>anos</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: colors.border,
  },
  title: { fontSize: 16, fontWeight: '700', color: colors.text, marginBottom: 12 },
  label: { fontSize: 13, fontWeight: '600', color: colors.text, marginBottom: 6 },
  row: { flexDirection: 'row', gap: 8 },
  genderBtn: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: colors.border,
    backgroundColor: '#f6f8fa',
    alignItems: 'center',
  },
  genderBtnActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  genderText: { fontSize: 15, fontWeight: '600', color: '#444' },
  genderTextActive: { color: '#fff' },
  ageRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  ageInput: {
    flex: 1,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    color: colors.text,
  },
  unit: { fontSize: 13, color: colors.textMuted },
});

export default PatientForm;
