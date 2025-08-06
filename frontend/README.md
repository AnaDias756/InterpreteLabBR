# 🖥️ Interface Desktop - Interpretador de Laudos

Interface desktop moderna desenvolvida em PySide6 para análise de laudos laboratoriais.

## 🚀 Funcionalidades

### 📋 Upload de Arquivos
- **Drag & Drop**: Arraste arquivos PDF diretamente para a interface
- **Seleção manual**: Botão para navegar e selecionar arquivos
- **Validação**: Verificação automática de formato PDF

### 👤 Dados do Paciente
- **Gênero**: Seleção entre Masculino/Feminino
- **Idade**: Campo numérico com validação (0-120 anos)
- **Interface intuitiva**: Controles simples e claros

### 🔬 Análise Inteligente
- **Processamento assíncrono**: Interface não trava durante análise
- **Barra de progresso**: Feedback visual do progresso
- **Tratamento de erros**: Mensagens claras em caso de problemas

### 📊 Visualização de Resultados

#### 🧪 Aba "Achados"
- **Cards visuais** para cada analito encontrado
- **Código de cores**:
  - 🟢 **Verde**: Valores normais
  - 🟡 **Amarelo**: Valores altos
  - 🔴 **Vermelho**: Valores baixos
- **Informações detalhadas**:
  - Nome do analito
  - Valor encontrado
  - Status (normal/alto/baixo)
  - Especialidade recomendada
  - Descrição do achado

#### 📝 Aba "Briefing"
- **Texto personalizado** gerado por IA (Gemini)
- **Linguagem acessível** para o paciente
- **Orientações específicas** para preparação da consulta
- **Formatação rica** com HTML

#### 👨‍⚕️ Aba "Especialidades"
- **Lista organizada** de especialidades recomendadas
- **Baseada nos achados** laboratoriais
- **Priorização inteligente** conforme severidade

## 🛠️ Instalação

### Pré-requisitos
```bash
# Instalar dependências
pip install PySide6>=6.6.0 requests
```

### Execução

#### Método 1: Script automático (Recomendado)
```bash
# Executa backend + frontend automaticamente
python run_desktop.py
```

#### Método 2: Manual
```bash
# Terminal 1: Backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
python frontend/main.py
```

## 🎨 Interface

### Layout Responsivo
- **Painel esquerdo**: Controles de upload e configuração
- **Painel direito**: Resultados em abas organizadas
- **Splitter ajustável**: Redimensione conforme necessário

### Tema Moderno
- **Cores profissionais**: Azul médico e tons neutros
- **Ícones intuitivos**: Emojis para facilitar navegação
- **Tipografia clara**: Fontes legíveis e hierarquia visual
- **Feedback visual**: Estados hover, disabled, loading

## 🔧 Configuração

### Conexão com Backend
- **URL padrão**: `http://localhost:8000`
- **Timeout**: 30 segundos para análise
- **Retry automático**: Em caso de falha temporária

### Tratamento de Erros
- **Conexão**: Verifica se backend está rodando
- **Timeout**: Mensagem clara se análise demorar muito
- **Formato**: Valida se arquivo é PDF válido
- **Dados**: Verifica campos obrigatórios

## 🧪 Teste

### Arquivo de Exemplo
Use o arquivo em `tests/exemplos/Laudo_Exemplo.pdf` para testar:

1. **Abra a aplicação**
2. **Clique em "📁 Selecionar PDF"**
3. **Navegue até** `tests/exemplos/Laudo_Exemplo.pdf`
4. **Configure** gênero e idade
5. **Clique em "🔬 Analisar Laudo"**
6. **Aguarde** os resultados aparecerem

### Dados de Teste Sugeridos
- **Gênero**: Feminino
- **Idade**: 35 anos

## 🚨 Solução de Problemas

### Erro: "Não foi possível conectar ao servidor"
**Solução**: Verifique se o backend está rodando:
```bash
curl http://localhost:8000/health
```

### Erro: "ImportError: cannot import name 'QSignal'"
**Solução**: Atualize o PySide6:
```bash
pip install --upgrade PySide6
```

### Interface não abre
**Solução**: Verifique se tem display disponível (Linux/WSL):
```bash
export DISPLAY=:0
```

### Análise muito lenta
**Possíveis causas**:
- PDF muito grande (>10MB)
- Conexão lenta com API Gemini
- Backend sobrecarregado

## 📱 Compatibilidade

- **Windows**: ✅ Totalmente suportado
- **macOS**: ✅ Suportado
- **Linux**: ✅ Suportado (requer display)
- **Python**: 3.8+ requerido

## 🔮 Próximas Funcionalidades

- [ ] **Histórico**: Salvar análises anteriores
- [ ] **Exportação**: PDF/Word dos resultados
- [ ] **Configurações**: Personalizar API endpoints
- [ ] **Temas**: Modo escuro/claro
- [ ] **Múltiplos arquivos**: Análise em lote
- [ ] **Gráficos**: Visualização de tendências

## 🤝 Contribuição

Para contribuir com melhorias na interface:

1. **Fork** o repositório
2. **Crie** uma branch para sua feature
3. **Teste** em diferentes sistemas operacionais
4. **Documente** mudanças na interface
5. **Submeta** um Pull Request

---

**Desenvolvido com ❤️ usando PySide6**