import React, { useEffect, useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
  StatusBar,
  Platform,
} from 'react-native';
import { PatientData, ManualLabValues, EMPTY_MANUAL_VALUES, InterpretationResponse } from './src/types';
import { healthCheck, interpretLabManual, interpretLabPdf, PickedPdf } from './src/api';
import { colors } from './src/theme';
import PatientForm from './src/components/PatientForm';
import ManualEntryForm from './src/components/ManualEntryForm';
import PdfUpload from './src/components/PdfUpload';
import Results from './src/components/Results';

type ApiStatus = 'checking' | 'online' | 'offline';
type InputMode = 'manual' | 'pdf';

export default function App() {
  const [inputMode, setInputMode] = useState<InputMode>('pdf');
  const [patientData, setPatientData] = useState<PatientData>({ genero: 'feminino', idade: '' });
  const [manualValues, setManualValues] = useState<ManualLabValues>(EMPTY_MANUAL_VALUES);
  const [pdf, setPdf] = useState<PickedPdf | null>(null);
  const [results, setResults] = useState<InterpretationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [apiStatus, setApiStatus] = useState<ApiStatus>('checking');

  useEffect(() => {
    let ativo = true;
    (async () => {
      try {
        await healthCheck();
        if (ativo) setApiStatus('online');
      } catch {
        if (ativo) setApiStatus('offline');
      }
    })();
    return () => { ativo = false; };
  }, []);

  const hasManualValues = Object.values(manualValues).some((v) => v !== '');

  const handleAnalyze = async () => {
    if (!patientData.idade) {
      setError('Informe a idade do paciente.');
      return;
    }
    if (inputMode === 'manual' && !hasManualValues) {
      setError('Informe ao menos um valor de exame.');
      return;
    }
    if (inputMode === 'pdf' && !pdf) {
      setError('Selecione um arquivo PDF.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const resp = inputMode === 'pdf'
        ? await interpretLabPdf(patientData, pdf as PickedPdf)
        : await interpretLabManual(patientData, manualValues);
      setResults(resp);
    } catch (e: any) {
      const detail = e?.response?.data?.detail;
      setError(detail || e?.message || 'Erro ao analisar. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setManualValues(EMPTY_MANUAL_VALUES);
    setPdf(null);
    setError(null);
  };

  const statusLabel =
    apiStatus === 'checking' ? '🔄 Verificando servidor...'
    : apiStatus === 'online' ? '🟢 Servidor online'
    : '🔴 Servidor offline';

  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar barStyle="dark-content" backgroundColor={colors.card} />
      <View style={styles.header}>
        <Text style={styles.headerTitle}>🩸 Interpretador de Hemograma</Text>
        <Text
          style={[
            styles.status,
            apiStatus === 'online' && { color: colors.online },
            apiStatus === 'offline' && { color: colors.offline },
            apiStatus === 'checking' && { color: colors.checking },
          ]}
        >
          {statusLabel}
        </Text>
      </View>

      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
        {!results ? (
          <>
            <View style={styles.modeRow}>
              {(['pdf', 'manual'] as const).map((m) => (
                <TouchableOpacity
                  key={m}
                  style={[styles.modeBtn, inputMode === m && styles.modeBtnActive]}
                  onPress={() => { setInputMode(m); setError(null); }}
                >
                  <Text style={[styles.modeText, inputMode === m && styles.modeTextActive]}>
                    {m === 'manual' ? '⌨️  Digitar valores' : '📄  Enviar PDF'}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>

            <View style={styles.infoBox}>
              <Text style={styles.infoText}>
                {inputMode === 'manual'
                  ? 'Digite os valores do seu hemograma para uma avaliação baseada na referência da população adulta brasileira (PNS).'
                  : 'Envie o PDF do seu hemograma. O sistema extrai os valores automaticamente e avalia pela referência da população adulta brasileira (PNS).'}
              </Text>
            </View>

            {inputMode === 'manual'
              ? <ManualEntryForm values={manualValues} onChange={setManualValues} />
              : <PdfUpload pdf={pdf} onSelect={setPdf} onError={setError} />}

            <PatientForm data={patientData} onChange={setPatientData} />

            <TouchableOpacity
              style={[styles.analyzeBtn, (loading || apiStatus === 'offline') && styles.analyzeBtnDisabled]}
              onPress={handleAnalyze}
              disabled={loading || apiStatus === 'offline'}
            >
              {loading
                ? <ActivityIndicator color="#fff" />
                : <Text style={styles.analyzeText}>🔍 Analisar</Text>}
            </TouchableOpacity>

            {apiStatus === 'offline' && (
              <Text style={styles.offlineHint}>
                O servidor pode estar inicializando (cold start). Aguarde alguns instantes e reabra o app.
              </Text>
            )}

            {error && <Text style={styles.errorText}>❌ {error}</Text>}
          </>
        ) : (
          <Results results={results} onReset={handleReset} />
        )}

        <Text style={styles.footer}>
          Referência: Rosenfeld et al. (2019) — PNS. Ferramenta de apoio; não substitui avaliação médica.
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.bg, paddingTop: Platform.OS === 'android' ? StatusBar.currentHeight : 0 },
  header: {
    backgroundColor: colors.card,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  headerTitle: { fontSize: 18, fontWeight: '700', color: colors.text },
  status: { fontSize: 12, marginTop: 4, fontWeight: '600' },
  content: { padding: 16, paddingBottom: 40 },
  modeRow: {
    flexDirection: 'row',
    backgroundColor: '#e6eaf0',
    borderRadius: 24,
    padding: 4,
    marginBottom: 16,
  },
  modeBtn: { flex: 1, paddingVertical: 10, borderRadius: 20, alignItems: 'center' },
  modeBtnActive: { backgroundColor: colors.primary },
  modeText: { fontSize: 14, fontWeight: '600', color: colors.textMuted },
  modeTextActive: { color: '#fff' },
  infoBox: {
    backgroundColor: '#eef4ff',
    borderRadius: 10,
    padding: 12,
    marginBottom: 16,
  },
  infoText: { fontSize: 13, color: '#33415a', lineHeight: 19 },
  analyzeBtn: {
    backgroundColor: colors.primary,
    borderRadius: 24,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 4,
  },
  analyzeBtnDisabled: { backgroundColor: '#ccc' },
  analyzeText: { color: '#fff', fontSize: 16, fontWeight: '700' },
  offlineHint: { fontSize: 12, color: colors.textMuted, marginTop: 10, textAlign: 'center' },
  errorText: { color: colors.offline, marginTop: 12, fontSize: 14 },
  footer: { fontSize: 11, color: colors.textMuted, marginTop: 20, textAlign: 'center', lineHeight: 16 },
});
