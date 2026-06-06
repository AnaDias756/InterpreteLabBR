# 🩸 InterpreteLabBR — Interpretador de Hemograma

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://reactjs.org)
[![Expo](https://img.shields.io/badge/Expo-SDK%2054-000020.svg)](https://expo.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Sistema de apoio à decisão para **triagem de hemogramas**, fundamentado nos valores
> de referência da **população adulta brasileira (PNS)** e voltado ao formato de laudo
> do **SUS**. Disponível como PWA (web) e aplicativo móvel.

> ⚕️ **Aviso:** ferramenta educativa e de apoio. **Não substitui avaliação médica.**
> Os resultados não constituem diagnóstico.

## 🔗 Acesso em produção

- **PWA (web):** https://interpretlabbr.netlify.app
- **API (backend):** https://interpretador-lab-backend.onrender.com
  ([/health](https://interpretador-lab-backend.onrender.com/health) ·
  [/docs](https://interpretador-lab-backend.onrender.com/docs))

> ℹ️ O backend roda no plano gratuito do Render e "hiberna" após inatividade —
> o primeiro acesso pode levar ~50s (cold start) até "acordar".

## 🎯 Sobre o Projeto

O **InterpreteLabBR** extrai os valores de um hemograma (de um PDF ou digitados
manualmente), classifica cada analito como *normal / alto / baixo* e gera um
briefing educativo ao paciente, sugerindo especialidades médicas quando pertinente.

O diferencial do projeto é a **fundamentação na realidade brasileira**:

- **Valores de referência da PNS** — as faixas de normalidade derivam do estudo de
  Rosenfeld et al. (2019), o único que estabeleceu valores de referência de hemograma
  para adultos brasileiros pelo método paramétrico, com dados da Pesquisa Nacional de
  Saúde. A maioria das ferramentas usa faixas importadas de populações estrangeiras.
- **Foco no laudo do SUS** — o formato de entrada padrão é o do Sistema Único de Saúde,
  escolha deliberada para priorizar a população que mais depende da rede pública e tem
  menor acesso a interpretação especializada (princípios de universalidade e equidade).
- **Comparação de referências** — além de classificar pela PNS, o sistema mostra a
  divergência em relação à referência "clássica/laboratorial" impressa no próprio laudo.

> Este repositório é a base de um **TCC de pós-graduação** que evolui o PWA da graduação
> para um app móvel e adiciona um eixo de validação (extração, classificação e
> usabilidade). Veja [`PROPOSTA_TCC.md`](PROPOSTA_TCC.md).

### ✨ Funcionalidades

- 📄 **Análise por PDF** — upload de laudo; extração automática via parsing de texto
  (e OCR como fallback para imagens)
- ⌨️ **Entrada manual** — digitação dos valores quando não há PDF
- 🇧🇷 **Classificação pela PNS** — normal/alto/baixo estratificado por sexo e idade
- 🔬 **Comparação PNS × referência do laudo** — destaca divergências entre as duas referências
- ⚠️ **Severidade dos achados** (1–5) e 👨‍⚕️ **recomendação de especialidades**
- 📝 **Briefing ao paciente** em linguagem acessível
- 📱 **Multiplataforma** — PWA (React) e app móvel (Expo/React Native)

## 🏗️ Arquitetura

```
┌──────────────────┐     ┌──────────────────┐
│   PWA (React)    │     │  App Móvel       │
│  frontend-web/   │     │  (Expo / RN)     │
└────────┬─────────┘     └────────┬─────────┘
         │        HTTP / JSON      │
         └────────────┬────────────┘
                      ▼
            ┌───────────────────┐
            │   Backend API     │
            │     (FastAPI)     │
            └─────────┬─────────┘
                      ▼
            ┌───────────────────┐
            │ Serviços          │
            │ • pdf_parser      │  extração (texto/OCR + regex)
            │ • rule_engine     │  regras PNS + comparação de refs
            │ • specialty_...   │  seleção de especialidades
            │ • nlg             │  briefing ao paciente
            └─────────┬─────────┘
                      ▼
            ┌───────────────────┐
            │ data/ (CSV)       │
            │ • patterns.csv    │  padrões de extração (laudo SUS)
            │ • lab_reference   │  referência clássica do laudo
            │ • guideline_map   │  regras/diretrizes por analito
            └───────────────────┘
```

## 🚀 Tecnologias

| Camada | Stack |
|---|---|
| **Backend** | FastAPI · Python 3.11 · Pydantic · pdfplumber/PyMuPDF/PyPDF2 · pytesseract + OpenCV (OCR) · pandas/numpy |
| **Frontend Web (PWA)** | React 19 · TypeScript · Axios · React Dropzone |
| **App Móvel** | Expo SDK 54 · React Native 0.81 · expo-document-picker · TypeScript |

## 📁 Estrutura do Projeto

```
InterpreteLabBR/
├── backend/                    # API FastAPI
│   ├── main.py                 # rotas: /health, /interpret, /interpret-manual, /debug
│   └── services/
│       ├── pdf_parser.py       # extração de valores (texto/OCR + regex)
│       ├── rule_engine.py      # classificação PNS + comparação de referências
│       ├── specialty_selector.py
│       └── nlg.py              # geração do briefing ao paciente
├── frontend-web/               # PWA (React + TypeScript) — deploy na Netlify
│   └── src/{components,services,types,utils}/
├── mobile/                     # App móvel (Expo / React Native)
│   └── src/{components,api.ts,config.ts,types.ts,theme.ts}
├── data/                       # Bases de configuração
│   ├── patterns.csv            # padrões de extração (formato do laudo SUS)
│   ├── lab_reference.csv       # referência "clássica" impressa no laudo
│   └── guideline_map.csv       # diretrizes/regras por analito
├── tests/                      # testes do backend
├── requirements-backend.txt    # dependências Python
├── render.yaml                 # configuração de deploy (Render)
├── PROPOSTA_TCC.md             # proposta de TCC (escopo e validação)
├── RENDER_DEPLOY_GUIDE.md      # guia de deploy do backend
└── README.md
```

## ⚡ Instalação e Execução (local)

### Pré-requisitos
- Python 3.11
- Node.js 18+ e npm
- (Opcional) Tesseract OCR — apenas para PDFs que são imagem/escaneados

### 🔧 Backend (FastAPI)

```bash
git clone https://github.com/AnaDias756/InterpreteLabBR.git
cd InterpreteLabBR

pip install -r requirements-backend.txt
cp .env.example .env          # ajuste se necessário

# a partir da raiz do projeto:
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000 · Docs: http://localhost:8000/docs

### 🌐 Frontend Web (PWA)

```bash
cd frontend-web
npm install
npm start                      # http://localhost:3000
```

> Por padrão a API usada é a de produção (definida em `netlify.toml`). Para apontar
> ao backend local, crie `frontend-web/.env` com `REACT_APP_API_URL=http://localhost:8000`.

### 📱 App Móvel (Expo)

```bash
cd mobile
npm install
npx expo install expo-document-picker   # garante a versão compatível com o SDK 54
npx expo start -c                        # abra no Expo Go (Android/iOS)
```

> A URL da API fica em `mobile/src/config.ts`. Por padrão aponta para a produção
> (Render). Para testar contra um backend local, descomente a linha com o IP da sua
> máquina na rede Wi-Fi (`localhost` não funciona a partir do celular).

## 📡 API — Endpoints

### `GET /health`
Status da API.
```json
{
  "status": "healthy",
  "message": "API esta funcionando corretamente",
  "version": "1.0.0",
  "services": { "imports_working": true, "pdf_processing": true }
}
```

### `POST /interpret`  (multipart/form-data)
Analisa um laudo em **PDF**.

| Campo | Tipo | Descrição |
|---|---|---|
| `file` | arquivo | PDF do hemograma |
| `genero` | texto | `"masculino"` ou `"feminino"` |
| `idade` | número | idade em anos |

### `POST /interpret-manual`  (application/json)
Analisa valores **digitados** (sem PDF). Todos os analitos são opcionais — a análise
usa apenas os informados. Série branca e plaquetas em valor **absoluto** (/μL).

```json
{
  "genero": "feminino",
  "idade": 35,
  "hemoglobina": 11.2,
  "hematocrito": 34.0,
  "leucocitos": 6500,
  "plaquetas": 210000
}
```

### Resposta (ambas as rotas)
```json
{
  "lab_findings": [
    {
      "analito": "Hemoglobina", "valor": 11.2, "resultado": "Baixo",
      "severidade": 3, "especialidade": "Hematologia",
      "descricao_achado": "Anemia", "diretriz": "Investigar causa da anemia"
    }
  ],
  "recommended_specialties": ["Hematologia", "Clínica Médica"],
  "patient_briefing": "Resumo educativo dos achados...",
  "lab_values_raw": [{ "analito": "Hemoglobina", "valor": 11.2 }],
  "comparacao_referencias": [
    {
      "analito": "Hemoglobina", "valor": 11.2,
      "classificacao_pns": "Baixo", "classificacao_lab": "Normal",
      "divergente": true
    }
  ]
}
```

> Há ainda `GET /debug` com informações técnicas para troubleshooting.

## ☁️ Deploy

| Componente | Plataforma | Branch | Observações |
|---|---|---|---|
| Backend | **Render** (Free) | `master` | Auto-Deploy; config em `render.yaml`. Veja [`RENDER_DEPLOY_GUIDE.md`](RENDER_DEPLOY_GUIDE.md) |
| PWA | **Netlify** | `master` | Build automático; API definida em `frontend-web/netlify.toml` |
| App móvel | **Expo / EAS Build** | — | `eas build -p android` (ou `--profile preview` para gerar APK de teste) |

Um push para `master` dispara o redeploy automático do backend (Render) e do PWA (Netlify).

## 🔬 Fundamentação científica

> ROSENFELD, Luiz Gastão et al. **Valores de referência para exames laboratoriais de
> hemograma da população adulta brasileira: Pesquisa Nacional de Saúde.** Revista
> Brasileira de Epidemiologia, v. 22, supl. 2, art. e190003, 2019.
> DOI: [10.1590/1980-549720190003.supl.2](https://doi.org/10.1590/1980-549720190003.supl.2).

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/minha-feature`)
3. Commit (`git commit -m 'feat: minha feature'`)
4. Push (`git push origin feature/minha-feature`)
5. Abra um Pull Request

## 📄 Licença

Licenciado sob a Licença MIT — veja [LICENSE](LICENSE).

---

Desenvolvido com ❤️ para ajudar pacientes a entender seus hemogramas — com referência
brasileira (PNS) e foco na população atendida pelo SUS.
