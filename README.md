# 🩺 Interpretador de Laudos Laboratoriais

Sistema inteligente para análise de laudos laboratoriais em PDF, com interpretação automática dos resultados e geração de briefings personalizados usando IA.

## 🚀 Funcionalidades

- **Upload de PDF**: Recebe laudos laboratoriais em formato PDF
- **Extração automática**: Identifica e extrai valores de exames automaticamente
- **Análise inteligente**: Compara resultados com diretrizes médicas
- **Recomendação de especialistas**: Sugere especialidades médicas baseadas nos achados
- **Briefing com IA**: Gera texto personalizado usando Google Gemini para preparar o paciente para a consulta

## 📋 Pré-requisitos

- Python 3.8+
- Chave API do Google Gemini (opcional, mas recomendado)

## ⚙️ Instalação

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd InterpreteLabBR
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure a API do Gemini** (opcional):
   - Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Gere sua chave API gratuita
   - Copie o arquivo `.env.example` para `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edite o arquivo `.env` e adicione sua chave:
     ```
     GEMINI_API_KEY=sua_chave_api_aqui
     ```

## 🏃‍♂️ Como usar

1. **Inicie o servidor**:
   ```bash
   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Acesse a interface**:
   - Documentação da API: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

3. **Faça upload de um laudo**:
   - Use o endpoint `/interpret`
   - Envie o arquivo PDF do laudo
   - Informe gênero e idade do paciente
   - Receba a análise completa

## 📊 Exemplo de resposta

```json
{
  "lab_findings": [
    {
      "analito": "hemoglobina",
      "valor": 10.5,
      "resultado": "baixo",
      "severidade": 2,
      "especialidade": "Hematologia",
      "descricao_achado": "Anemia",
      "diretriz": "SBHH"
    }
  ],
  "recommended_specialties": ["Hematologia"],
  "patient_briefing": "Texto personalizado gerado pela IA..."
}
```

## 🧪 Testes

```bash
# Teste o parser de PDF
python -m pytest tests/test_pdf_parser.py -v

# Teste o gerador de briefing
python -m pytest tests/test_olla.py -v
```

## 🔧 Configuração

### Fallbacks de IA

O sistema possui 3 níveis de fallback para geração de briefings:

1. **Google Gemini** (principal) - Requer chave API
2. **Ollama local** (fallback) - Requer Ollama rodando localmente
3. **Texto estático** (último recurso) - Sempre funciona

### Adicionando novos analitos

1. **Padrões de extração** (`data/patterns.csv`):
   ```csv
   analito,pattern,grupo_decimal
   glicose,"Glicose\s+([0-9]+,[0-9]+)",1
   ```

2. **Regras de interpretação** (`data/guideline_map.csv`):
   ```csv
   analito_id,sexo,idade_min,idade_max,limite_inferior,limite_superior,severidade_baixa,severidade_alta,especialidade,descricao_achado,diretriz
   glicose,Todos,18,120,70,99,2,3,"Endocrinologia","Alteração glicêmica","SBD"
   ```

## 🛡️ Segurança

- Nunca commite chaves API no repositório
- Use variáveis de ambiente para configurações sensíveis
- Valide todos os inputs de usuário
- Implemente rate limiting em produção

## 📝 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.