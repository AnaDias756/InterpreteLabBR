# Tarefa 2.1 — Arquitetura de Origem e Mapa de Migração

### InterpreteLabBR: do PWA ao aplicativo móvel (React Native/Expo)

> Documento produzido como parte do OE1 do TCC. Registra a arquitetura do sistema
> antes e após a migração, o inventário de componentes portados ou reaproveitados
> e os ganhos de capacidade nativa obtidos com a transição de paradigma.

---

## 1. Visão Geral da Arquitetura

O InterpreteLabBR adota uma arquitetura **API-first** com separação clara em três camadas:

| Camada | Tecnologia | Responsabilidade |
|---|---|---|
| **Backend** | Python / FastAPI | Toda a lógica clínica: extração OCR, motor de regras PNS, geração de texto (NLG) e seleção de especialidades |
| **Cliente web (PWA)** | React 19 / TypeScript | Interface de apresentação para navegadores; consome a API REST |
| **Cliente móvel (App)** | React Native 0.81 / Expo 54 | Interface de apresentação nativa para Android; consome a mesma API REST |

A principal consequência dessa arquitetura para a migração é que **o backend permaneceu 100% inalterado**: toda a lógica clínica sensível já residia no servidor antes da migração, e nenhuma linha de código Python precisou ser modificada para suportar o novo cliente móvel.

---

## 2. Arquitetura do Backend (compartilhada por PWA e App)

### 2.1 Endpoints REST

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Verificação de disponibilidade do serviço |
| GET | `/debug` | Informações de diagnóstico do ambiente |
| POST | `/interpret` | Recebe laudo em PDF (*multipart/form-data*) + sexo + idade; retorna interpretação completa |
| POST | `/interpret-manual` | Recebe valores digitados manualmente (JSON) + sexo + idade; retorna interpretação completa |

### 2.2 Serviços internos

| Serviço | Arquivo | Função |
|---|---|---|
| **Extração (OCR)** | `backend/services/pdf_parser.py` | Extrai texto do PDF via PyPDF2; usa Tesseract/PyMuPDF como *fallback* de OCR quando o texto não é selecionável |
| **Motor de regras (PNS)** | `backend/services/rule_engine.py` | Carrega `guideline_map.csv` e classifica cada analito como *normal*, *alto* ou *baixo* segundo as faixas da PNS, estratificadas por sexo e faixa etária |
| **NLG** | `backend/services/nlg.py` | Gera *briefing* educativo ao paciente; chama Google Gemini como primeiro recurso e cai em dicionário de explicações determinístico como *fallback* |
| **Seletor de especialidades** | `backend/services/specialty_selector.py` | Pontua especialidades com base na severidade dos achados e retorna as três mais relevantes |

### 2.3 Base de conhecimento (arquivos de dados)

| Arquivo | Conteúdo |
|---|---|
| `data/guideline_map.csv` | Faixas de referência da PNS por analito, sexo e faixa etária — núcleo da classificação clínica |
| `data/patterns.csv` | Expressões regulares para extração dos analitos a partir do texto bruto do laudo SUS |
| `data/lab_reference.csv` | Dados complementares de referência laboratorial |

---

## 3. Arquitetura do PWA (cliente de origem)

### 3.1 Componentes

| Componente | Arquivo | Função |
|---|---|---|
| `App` | `src/App.tsx` | Orquestrador central; gerencia estado global e fluxo de telas |
| `FileUpload` | `src/components/FileUpload.tsx` | Seleção de PDF via *drag-and-drop* (react-dropzone) ou clique |
| `PatientForm` | `src/components/PatientForm.tsx` | Formulário de sexo e idade do paciente |
| `ManualEntryForm` | `src/components/ManualEntryForm.tsx` | Entrada manual dos 14 analitos do hemograma |
| `ResultsDisplay` | `src/components/ResultsDisplay.tsx` | Exibição dos resultados com sinalização semafórica |
| `ReferenceComparison` | `src/components/ReferenceComparison.tsx` | Tabela comparativa de valores com as faixas da PNS |
| `LoadingSpinner` | `src/components/LoadingSpinner.tsx` | Indicador de carregamento animado |
| `ErrorAlert` | `src/components/ErrorAlert.tsx` | Exibição de mensagens de erro |
| `References` | `src/components/References.tsx` | Seção de referências bibliográficas da interface |

### 3.2 Serviços e utilitários do PWA

| Arquivo | Função |
|---|---|
| `src/services/api.ts` | Cliente Axios com *retry* exponencial (até 5 tentativas), *timeout* de 5 min (cold start do Render) e monitoramento de conectividade |
| `src/types/index.ts` | Interfaces TypeScript: `InterpretationResponse`, `PatientData`, `ManualLabValues` |
| `src/utils/mobileDetection.ts` | Detecção de dispositivo móvel e *debugger* de compatibilidade |
| `src/utils/mobileOptimizations.ts` | Aplicação de otimizações CSS para dispositivos móveis via navegador |
| `src/utils/polyfills.ts` | *Polyfills* para compatibilidade cross-browser |

### 3.3 Dependências principais do PWA

| Pacote | Versão | Finalidade |
|---|---|---|
| `react` | ^19.1.1 | Framework de interface |
| `typescript` | ^4.9.5 | Tipagem estática |
| `axios` | ^1.11.0 | Cliente HTTP |
| `react-dropzone` | ^14.3.8 | Seleção de arquivos via drag-and-drop |
| `react-scripts` | 5.0.1 | Toolchain de build (Create React App) |
| `web-vitals` | ^2.1.4 | Métricas de desempenho web |

---

## 4. Arquitetura do Aplicativo Móvel (cliente de destino)

### 4.1 Componentes

| Componente | Arquivo | Função |
|---|---|---|
| `App` | `App.tsx` | Orquestrador central; gerencia estado global e navegação por abas |
| `PdfUpload` | `src/components/PdfUpload.tsx` | Seleção de PDF via *expo-document-picker* (seletor nativo do SO) |
| `PatientForm` | `src/components/PatientForm.tsx` | Formulário de sexo e idade (componentes nativos RN) |
| `ManualEntryForm` | `src/components/ManualEntryForm.tsx` | Entrada manual dos 14 analitos (componentes nativos RN) |
| `Results` | `src/components/Results.tsx` | Exibição dos resultados com sinalização semafórica (ScrollView nativa) |
| `ReferenceComparisonTable` | `src/components/ReferenceComparisonTable.tsx` | Tabela comparativa com faixas da PNS (View/Text nativos) |

### 4.2 Módulos de suporte do App

| Arquivo | Função |
|---|---|
| `src/api.ts` | Cliente Axios adaptado para React Native; sem polyfills de browser |
| `src/types.ts` | Mesmas interfaces TypeScript do PWA (reutilizadas) |
| `src/config.ts` | URL de produção da API (`interpretador-lab-backend.onrender.com`) |
| `src/theme.ts` | Sistema de cores e estilos (substitui CSS) |

### 4.3 Dependências principais do App

| Pacote | Versão | Finalidade |
|---|---|---|
| `react-native` | 0.81.5 | Framework de componentes nativos |
| `expo` | 54.0.35 | Plataforma de build e distribuição (EAS Build → APK) |
| `typescript` | (herdado) | Tipagem estática |
| `axios` | ^1.17.0 | Cliente HTTP |
| `expo-document-picker` | ~14.0.8 | Seletor nativo de arquivos do SO |
| `expo-status-bar` | ~3.0.9 | Controle da barra de status nativa |

---

## 5. Mapa de Migração: PWA → Aplicativo Móvel

### 5.1 Correspondência de componentes

| Componente PWA | Componente App | Status | Observação |
|---|---|---|---|
| `FileUpload.tsx` | `PdfUpload.tsx` | **Reescrito** | `react-dropzone` (web) substituído por `expo-document-picker` (nativo) |
| `PatientForm.tsx` | `PatientForm.tsx` | **Portado** | Mesma lógica; elementos HTML (`<select>`, `<input>`) substituídos por `Picker` e `TextInput` nativos |
| `ManualEntryForm.tsx` | `ManualEntryForm.tsx` | **Portado** | Mesma lógica e campos; `<input type="number">` substituído por `TextInput` com `keyboardType="numeric"` |
| `ResultsDisplay.tsx` | `Results.tsx` | **Portado** | Lógica de sinalização semafórica mantida; `<div>` substituído por `View`/`ScrollView` nativos |
| `ReferenceComparison.tsx` | `ReferenceComparisonTable.tsx` | **Portado** | Estrutura de tabela mantida; HTML table substituído por `View`/`Text` com layout flexbox |
| `LoadingSpinner.tsx` | `ActivityIndicator` (nativo RN) | **Eliminado** | Substituído pelo componente nativo do React Native; sem código customizado necessário |
| `ErrorAlert.tsx` | Inline em `App.tsx` | **Eliminado** | Mensagens de erro incorporadas diretamente no App; sem componente separado |
| `References.tsx` | — | **Não portado** | Seção de referências bibliográficas da interface não incluída na v1 do app |
| `services/api.ts` | `src/api.ts` | **Adaptado** | Lógica de *retry* simplificada; removidos polyfills e utilitários exclusivos de browser |
| `types/index.ts` | `src/types.ts` | **Reutilizado** | Interfaces TypeScript idênticas (`InterpretationResponse`, `PatientData`, `ManualLabValues`) |
| `App.css` / `index.css` | `src/theme.ts` | **Substituído** | CSS substituído por objeto de tema TypeScript com paleta de cores e estilos centralizados |
| `utils/mobileDetection.ts` | — | **Eliminado** | Desnecessário: React Native é sempre móvel por definição |
| `utils/mobileOptimizations.ts` | — | **Eliminado** | Otimizações nativas já são responsabilidade do React Native |
| `utils/polyfills.ts` | — | **Eliminado** | Polyfills de browser não se aplicam ao ambiente React Native |

### 5.2 Correspondência de endpoints (sem alteração)

Ambos os clientes consomem os mesmos endpoints sem modificação no backend:

| Endpoint | PWA | App |
|---|---|---|
| `GET /health` | Sim | Sim |
| `POST /interpret` | Sim | Sim |
| `POST /interpret-manual` | Sim | Sim |

---

## 6. Inventário de Reuso

### 6.1 Resumo quantitativo

| Camada | Situação | Detalhamento |
|---|---|---|
| **Backend completo** | 100% reusado | 4 serviços Python, 3 arquivos de dados, 4 endpoints — nenhuma linha modificada |
| **Interfaces TypeScript** | 100% reusadas | `InterpretationResponse`, `PatientData`, `ManualLabValues`, `EMPTY_MANUAL_VALUES` |
| **Lógica de negócio** | 100% reusada | Reside integralmente no backend; não duplicada em nenhum cliente |
| **Componentes de interface** | ~50% portados | 4 de 9 componentes portados com adaptação; 2 reescritos; 3 eliminados |
| **Camada de API (cliente)** | Adaptado | Estrutura axios mantida; removidos utilitários exclusivos de browser |
| **Estilização** | Substituída | CSS → objeto TypeScript de tema (`theme.ts`) |

### 6.2 Ganhos de capacidade nativa obtidos com a migração

| Capacidade | PWA | App |
|---|---|---|
| **Instalação no dispositivo** | Atalho de navegador (limitado) | APK instalável (ícone nativo na tela inicial) |
| **Seletor de arquivos** | `react-dropzone` (browser) | `expo-document-picker` (seletor nativo do SO) |
| **Componentes visuais** | HTML/CSS renderizado pelo browser | Componentes nativos do Android (melhor desempenho) |
| **Barra de status** | Não controlada | Controlada via `expo-status-bar` |
| **Área segura de tela** | Não garantida | `SafeAreaView` nativo (respeita notch e bordas) |
| **Distribuição** | URL pública (Netlify) | APK distribuível diretamente; preparado para Google Play |
| **Dependência de browser** | Obrigatória | Eliminada |

---

> **Conclusão metodológica.** A arquitetura API-first foi o fator determinante para
> que a migração se concentrasse exclusivamente na camada de apresentação. O reuso
> integral do backend — incluindo o motor de regras da PNS, o pipeline de OCR e a
> camada de NLG — preserva a corretude funcional do sistema e elimina o risco de
> introdução de divergências clínicas durante a transição de paradigma. Esse padrão
> será verificado formalmente na Frente B (regressão funcional), que submeterá as
> mesmas entradas a ambos os clientes e confirmará saídas idênticas da API.
