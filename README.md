# 🩺 InterpreteLab BR

**Sistema Inteligente de Interpretação de Laudos Laboratoriais**

Um sistema completo para análise automatizada de exames laboratoriais, oferecendo interpretação inteligente, identificação de achados clínicos e sugestões de especialidades médicas.

## 🚀 Funcionalidades

### Backend (API)
- 📄 **Processamento de PDFs**: Extração inteligente de dados de laudos laboratoriais
- 🧠 **Análise com IA**: Interpretação automatizada usando modelos de linguagem avançados
- 🔍 **Detecção de Achados**: Identificação automática de valores alterados e suas implicações
- 👨‍⚕️ **Sugestão de Especialidades**: Recomendação de especialistas baseada nos achados
- 📊 **Relatórios Estruturados**: Geração de briefings médicos detalhados

### Frontend (Desktop)
- 🖱️ **Interface Intuitiva**: Drag & drop para upload de PDFs
- 👤 **Dados do Paciente**: Entrada de informações como gênero e idade
- ⚡ **Processamento Assíncrono**: Análise em tempo real com barra de progresso
- 🎨 **Visualização Rica**: Cards coloridos para achados, briefing e especialidades

## 🏗️ Arquitetura

```
InterpreteLabBR/
├── backend/           # API FastAPI
│   ├── main.py       # Servidor principal
│   └── services/     # Serviços de processamento
├── frontend/         # Interface desktop PySide6
│   └── main.py      # Aplicação principal
├── data/            # Dados de configuração
└── tests/           # Testes automatizados
```

## 🌐 Deploy

### Backend (Render)
O backend está implantado em: `https://interpretelabbr.onrender.com`

**Endpoints disponíveis:**
- `GET /` - Status da API
- `POST /interpret` - Interpretação de laudos
- `GET /docs` - Documentação Swagger

### Frontend (Desktop)
Distribuição local via executável ou script Python.

## 🛠️ Instalação Local

### Pré-requisitos
- Python 3.8+
- pip

### Backend
```bash
# Instalar dependências
pip install -r requirements-backend.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# Executar servidor
uvicorn backend.main:app --reload
```

### Frontend
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python frontend/main.py
```

### Execução Simplificada
```bash
# Windows - Duplo clique em:
executar.bat
```

## 📋 Uso

1. **Abrir a aplicação** desktop
2. **Arrastar PDF** do laudo para a área designada
3. **Preencher dados** do paciente (gênero, idade)
4. **Clicar em "Analisar"** e aguardar o processamento
5. **Visualizar resultados**:
   - **Achados**: Cards com valores alterados
   - **Briefing**: Interpretação médica detalhada
   - **Especialidades**: Recomendações de especialistas

## 📦 Distribuição

### Opção 1: Script Simples
1. Copiar pasta completa do projeto
2. Executar `executar.bat`

### Opção 2: Executável (PyInstaller)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name InterpretadorLaudos frontend/main.py
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Teste específico
pytest tests/test_pdf_parser.py
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```env
# API Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Optional: External API keys
OPENAI_API_KEY=your_key_here
```

### Dados de Configuração
- `data/patterns.csv`: Padrões de análise laboratorial
- `data/guideline_map.csv`: Mapeamento de diretrizes médicas

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para suporte técnico ou dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação da API em `/docs`

## 🔄 Atualizações

### v1.0.0
- ✅ Sistema completo de interpretação
- ✅ Interface desktop funcional
- ✅ Deploy em produção (Render)
- ✅ Processamento de PDFs
- ✅ Análise com IA
- ✅ Distribuição local

---

**Desenvolvido com ❤️ para a comunidade médica brasileira**