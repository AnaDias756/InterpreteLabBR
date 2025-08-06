# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-19

### Adicionado
- 🎉 **Lançamento inicial do InterpreteLab BR**
- 📄 **Processamento de PDFs**: Sistema completo de extração de dados de laudos laboratoriais
- 🧠 **Análise com IA**: Interpretação automatizada usando modelos de linguagem (Ollama/OpenAI)
- 🔍 **Detecção de Achados**: Identificação automática de valores alterados com severidade
- 👨‍⚕️ **Sugestão de Especialidades**: Recomendação de especialistas baseada nos achados
- 📊 **Relatórios Estruturados**: Geração de briefings médicos detalhados
- 🖱️ **Interface Desktop**: Aplicação PySide6 com drag & drop para PDFs
- 👤 **Dados do Paciente**: Sistema de entrada para gênero e idade
- ⚡ **Processamento Assíncrono**: Análise em tempo real com barra de progresso
- 🎨 **Visualização Rica**: Cards coloridos para achados, briefing e especialidades
- 🌐 **API REST**: Backend FastAPI com documentação Swagger
- 🚀 **Deploy em Produção**: Sistema implantado no Render
- 📦 **Sistema de Distribuição**: Scripts para geração de executáveis
- 🧪 **Testes Automatizados**: Cobertura de testes para componentes principais
- 📋 **Documentação Completa**: README, guias de instalação e uso

### Funcionalidades Técnicas
- **Backend (FastAPI)**:
  - Endpoint `/interpret` para análise de laudos
  - Processamento de arquivos PDF
  - Integração com Ollama e OpenAI
  - Sistema de fallback para IA
  - Validação de entrada robusta
  - Tratamento de erros abrangente

- **Frontend (PySide6)**:
  - Interface gráfica moderna e intuitiva
  - Drag & drop para upload de arquivos
  - Formulário de dados do paciente
  - Visualização de resultados em tempo real
  - Sistema de progresso para operações assíncronas
  - Cards interativos para diferentes tipos de resultado

- **Processamento de Dados**:
  - Parser inteligente de PDFs laboratoriais
  - Sistema de regras configurável
  - Mapeamento de diretrizes médicas
  - Classificação de severidade
  - Recomendação de especialidades

- **Infraestrutura**:
  - Deploy automatizado no Render
  - Configuração via variáveis de ambiente
  - Sistema de logs estruturado
  - Monitoramento de saúde da aplicação

### Arquivos de Configuração
- `data/patterns.csv`: Padrões de extração de analitos
- `data/guideline_map.csv`: Mapeamento de diretrizes médicas
- `.env.example`: Exemplo de configuração de ambiente
- `requirements.txt`: Dependências do frontend
- `requirements-backend.txt`: Dependências do backend
- `render.yaml`: Configuração de deploy
- `Dockerfile`: Containerização da aplicação

### Distribuição
- Script `executar.bat` para execução simplificada
- Guia completo de distribuição (`DISTRIBUICAO.md`)
- Suporte para geração de executáveis com PyInstaller
- Instruções para diferentes métodos de deploy

---

## Formato das Versões

### [Unreleased]
- Funcionalidades em desenvolvimento

### Tipos de Mudanças
- **Adicionado** para novas funcionalidades
- **Alterado** para mudanças em funcionalidades existentes
- **Descontinuado** para funcionalidades que serão removidas
- **Removido** para funcionalidades removidas
- **Corrigido** para correções de bugs
- **Segurança** para vulnerabilidades corrigidas

---

**Desenvolvido com ❤️ para a comunidade médica brasileira**