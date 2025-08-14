# 🩺 Interpretador de Laudos Laboratoriais

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Sistema inteligente para análise e interpretação automatizada de laudos laboratoriais, fornecendo insights médicos e recomendações de especialidades.

## 🎯 Sobre o Projeto

O **Interpretador de Laudos Laboratoriais** é uma aplicação web que utiliza técnicas de OCR, processamento de linguagem natural e regras médicas para analisar resultados de exames laboratoriais em formato PDF. O sistema identifica valores anômalos, classifica a severidade dos achados e sugere especialidades médicas apropriadas.

### ✨ Funcionalidades Principais

- 📄 **Upload e análise de PDFs** de laudos laboratoriais
- 🔍 **Extração automática de valores** usando OCR e regex
- 🧠 **Análise inteligente** com regras médicas especializadas
- ⚠️ **Classificação de severidade** dos achados (1-5)
- 👨‍⚕️ **Recomendação de especialidades** médicas
- 📊 **Interface web moderna** e responsiva
- 🔄 **API RESTful** para integração

## 🏗️ Arquitetura

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐
│                 │ ◄──────────────► │                 │
│  Frontend Web   │                  │  Backend API    │
│  (React + TS)   │                  │   (FastAPI)     │
│                 │                  │                 │
└─────────────────┘                  └─────────────────┘
                                              │
                                              ▼
                                     ┌─────────────────┐
                                     │   Serviços de   │
                                     │   Processamento │
                                     │                 │
                                     │ • PDF Parser    │
                                     │ • Rule Engine   │
                                     │ • NLG System    │
                                     │ • Specialty AI  │
                                     └─────────────────┘
```

## 🚀 Tecnologias

### Backend
- **FastAPI** - Framework web moderno e rápido
- **Python 3.8+** - Linguagem principal
- **OCR** - Extração de texto de PDFs
- **Regex** - Processamento de padrões laboratoriais
- **Pydantic** - Validação de dados

### Frontend
- **React 18** - Biblioteca de interface
- **TypeScript** - Tipagem estática
- **Axios** - Cliente HTTP
- **React Dropzone** - Upload de arquivos
- **CSS3** - Estilização moderna

## 📁 Estrutura do Projeto

```
InterpreteLabBR/
├── 📁 backend/                 # API FastAPI
│   ├── main.py                # Aplicação principal
│   └── services/              # Serviços de processamento
│       ├── pdf_parser.py      # Extração de dados do PDF
│       ├── rule_engine.py     # Motor de regras médicas
│       ├── specialty_selector.py # Seleção de especialidades
│       └── nlg.py            # Geração de linguagem natural
├── 📁 frontend-web/           # Interface React
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── services/         # Serviços de API
│   │   ├── types/           # Tipos TypeScript
│   │   └── App.tsx          # Componente principal
│   └── package.json
├── 📁 data/                   # Dados de configuração
│   ├── patterns.csv          # Padrões de extração
│   └── guideline_map.csv     # Mapeamento de diretrizes
├── requirements-backend.txt   # Dependências Python
├── .env.example              # Variáveis de ambiente
└── README.md                 # Este arquivo
```

## ⚡ Instalação e Execução

### Pré-requisitos
- Python 3.8+
- Node.js 18+
- npm ou yarn

### 🔧 Backend (FastAPI)

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/InterpreteLabBR.git
cd InterpreteLabBR
```

2. **Instale as dependências**
```bash
pip install -r requirements-backend.txt
```

3. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

4. **Execute o servidor**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 🌐 Frontend (React)

1. **Navegue para o diretório frontend**
```bash
cd frontend-web
```

2. **Instale as dependências**
```bash
npm install
```

3. **Execute o servidor de desenvolvimento**
```bash
npm start
```

### 🎉 Acesso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### `GET /health`
Verifica o status da API

**Resposta:**
```json
{
  "status": "healthy",
  "message": "Interpretador de Laudos Laboratoriais está funcionando!"
}
```

### `POST /interpret`
Analisa um laudo laboratorial

**Parâmetros:**
- `file`: Arquivo PDF do laudo (multipart/form-data)
- `genero`: Gênero do paciente ("masculino" ou "feminino")
- `idade`: Idade do paciente (número)

**Resposta:**
```json
{
  "lab_findings": [
    {
      "analito": "Hemoglobina",
      "valor": 10.5,
      "resultado": "Baixo",
      "severidade": 3,
      "especialidade": "Hematologia",
      "descricao_achado": "Anemia moderada",
      "diretriz": "Investigar causa da anemia"
    }
  ],
  "recommended_specialties": ["Hematologia", "Clínica Médica"],
  "patient_briefing": "Resumo dos achados para o paciente..."
}
```

## 🎨 Interface do Usuário

A interface web oferece:

- 📤 **Upload intuitivo** com drag & drop
- 👤 **Formulário de paciente** (gênero e idade)
- ⚡ **Status da API** em tempo real
- 📊 **Visualização de resultados** organizada
- 📱 **Design responsivo** para mobile
- 🎯 **Feedback visual** durante o processamento

## 🧪 Exemplo de Uso

1. Acesse http://localhost:3000
2. Faça upload de um PDF de laudo laboratorial
3. Preencha os dados do paciente (gênero e idade)
4. Clique em "Analisar Laudo"
5. Visualize os resultados organizados por:
   - Achados laboratoriais com severidade
   - Especialidades recomendadas
   - Briefing para o paciente

## 🔬 Processamento de Dados

O sistema processa os laudos através de:

1. **Extração OCR** - Converte PDF em texto
2. **Regex Patterns** - Identifica valores laboratoriais
3. **Rule Engine** - Aplica regras médicas especializadas
4. **Classificação** - Determina severidade (1-5)
5. **NLG** - Gera descrições em linguagem natural
6. **Specialty AI** - Recomenda especialidades médicas

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ para auxiliar pacientes na interpretação de seus laudos laboratoriais.

---

⭐ **Se este projeto foi útil, considere dar uma estrela!**
