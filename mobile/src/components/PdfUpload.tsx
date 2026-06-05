import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import { colors } from '../theme';
import { PickedPdf } from '../api';

interface Props {
  pdf: PickedPdf | null;
  onSelect: (pdf: PickedPdf | null) => void;
  onError?: (msg: string) => void;
}

const PdfUpload: React.FC<Props> = ({ pdf, onSelect, onError }) => {
  const pick = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'application/pdf',
        copyToCacheDirectory: true,
        multiple: false,
      });
      if (result.canceled) return;
      const asset = result.assets[0];
      if (!asset) return;
      onSelect({ uri: asset.uri, name: asset.name ?? 'laudo.pdf', mimeType: asset.mimeType });
    } catch (e: any) {
      onError?.('Não foi possível abrir o seletor de arquivos.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Laudo em PDF</Text>
      <Text style={styles.hint}>
        Envie o PDF do seu hemograma. Funciona melhor com PDFs que têm texto
        selecionável (não apenas foto/imagem). Apenas Hemograma Completo.
      </Text>

      <TouchableOpacity style={styles.pickBtn} onPress={pick}>
        <Text style={styles.pickText}>{pdf ? '🔄 Trocar arquivo' : '📎 Selecionar PDF'}</Text>
      </TouchableOpacity>

      {pdf && (
        <View style={styles.fileRow}>
          <Text style={styles.fileName} numberOfLines={1}>📄 {pdf.name}</Text>
          <TouchableOpacity onPress={() => onSelect(null)}>
            <Text style={styles.remove}>Remover</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.card,
    borderRadius: 10,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: colors.border,
  },
  title: { fontSize: 16, fontWeight: '700', color: colors.text, marginBottom: 6 },
  hint: { fontSize: 13, color: colors.textMuted, lineHeight: 18, marginBottom: 14 },
  pickBtn: {
    backgroundColor: '#eef4ff',
    borderRadius: 10,
    paddingVertical: 14,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#cfe0ff',
  },
  pickText: { color: '#1f5bd6', fontSize: 15, fontWeight: '700' },
  fileRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginTop: 12,
    backgroundColor: '#f1f8f2',
    borderRadius: 8,
    paddingVertical: 10,
    paddingHorizontal: 12,
  },
  fileName: { flex: 1, marginRight: 10, color: colors.text, fontSize: 13 },
  remove: { color: colors.offline, fontSize: 13, fontWeight: '600' },
});

export default PdfUpload;
