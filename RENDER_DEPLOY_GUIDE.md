# 🚀 Guia de Deploy no Render - API Interpretador de Laudos

## ✅ Problemas Resolvidos

Este guia documenta as correções implementadas para resolver o erro **502 Bad Gateway** e melhorar a estabilidade da API no Render.

### 🔧 Melhorias Implementadas

1. **Configuração Otimizada do render.yaml**
   - Timeouts mais generosos para cold start
   - Configuração de disco para melhor performance
   - Variáveis de ambiente otimizadas
   - Build command melhorado

2. **Health Check Robusto**
   - Monitoramento de recursos do sistema
   - Verificação de serviços críticos
   - Informações detalhadas de status
   - Endpoint de debug para troubleshooting

3. **Logging Melhorado**
   - Eventos de startup e shutdown
   - Logs detalhados de inicialização
   - Verificação de dependências na inicialização

4. **Dependências Atualizadas**
   - Adicionado `psutil` para monitoramento
   - Todas as dependências testadas localmente

## 🚀 Como Fazer o Deploy

### 1. Verificar Localmente

Antes de fazer o deploy, sempre teste localmente:

```bash
# Instalar dependências
pip install -r requirements-backend.txt

# Executar teste completo
python test_backend_local.py
```

### 2. Commit das Alterações

```bash
git add .
git commit -m "fix: resolver erro 502 - melhorar configuração Render e health checks"
git push origin main
```

### 3. Deploy Automático

O Render fará o deploy automaticamente quando detectar mudanças na branch `main`.

### 4. Verificar Deploy

Após o deploy, verifique:

1. **Health Check**: `https://interpretador-lab-backend.onrender.com/health`
2. **Debug Info**: `https://interpretador-lab-backend.onrender.com/debug`
3. **Logs no Dashboard do Render**

## 🔍 Endpoints de Monitoramento

### `/health`
Retorna status detalhado da API:
```json
{
  "status": "healthy",
  "message": "API esta funcionando corretamente",
  "timestamp": 1755830740.0042317,
  "version": "1.0.0",
  "system": {
    "memory_usage_percent": 85.7,
    "disk_usage_percent": 64.77,
    "python_version": "3.11.0",
    "port": "10000"
  },
  "services": {
    "imports_working": true,
    "pdf_processing": true
  }
}
```

### `/debug`
Informações técnicas para troubleshooting:
```json
{
  "python_version": "3.11.0",
  "working_directory": "/opt/render/project/src",
  "environment_variables": {
    "PYTHON_VERSION": "3.11.0",
    "PORT": "10000",
    "PYTHONPATH": "."
  },
  "files_exist": {
    "data/patterns.csv": true,
    "data/guideline_map.csv": true,
    "backend/services/pdf_parser.py": true
  }
}
```

## 🛠️ Troubleshooting

### Erro 502 Bad Gateway

**Possíveis Causas:**
1. Cold start demorado (normal no plano gratuito)
2. Timeout durante inicialização
3. Erro de dependências
4. Problemas de memória

**Soluções:**
1. Aguardar 2-3 minutos para cold start
2. Verificar logs no dashboard do Render
3. Verificar `/health` endpoint
4. Usar `/debug` para informações técnicas

### Erro de Dependências

**Verificar:**
1. `requirements-backend.txt` está atualizado
2. Todas as dependências são compatíveis
3. Não há conflitos de versão

**Solução:**
```bash
# Testar localmente primeiro
pip install -r requirements-backend.txt
python test_backend_local.py
```

### Problemas de Memória

**Monitorar:**
- Usar endpoint `/health` para verificar uso de memória
- Logs do Render para mensagens de OOM (Out of Memory)

**Otimizações:**
- Plano gratuito tem limite de 512MB RAM
- Evitar carregar dados grandes na memória
- Usar processamento streaming quando possível

## 📊 Configurações do render.yaml

```yaml
services:
  - type: web
    name: interpretador-lab-backend
    env: python
    plan: free
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements-backend.txt
    startCommand: |
      uvicorn backend.main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 300 --timeout-graceful-shutdown 30
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        value: 10000
      - key: PYTHONPATH
        value: .
      - key: UVICORN_WORKERS
        value: 1
    healthCheckPath: /health
    autoDeploy: true
    branch: main
    rootDir: .
    region: oregon
    disk:
      name: interpretador-lab-disk
      size: 1GB
    maxShutdownDelaySeconds: 30
```

## 🔄 Processo de Cold Start

O Render (plano gratuito) "hiberna" serviços após 15 minutos de inatividade:

1. **Primeira requisição**: 30-60 segundos para "acordar"
2. **Inicialização**: Carregamento de dependências
3. **Health check**: Verificação automática
4. **Pronto**: API disponível

**Dica**: Use um serviço de ping para manter a API ativa em produção.

## 📝 Logs Importantes

Procurar por estas mensagens nos logs:

✅ **Sucesso:**
```
🚀 Iniciando API do Interpretador de Laudos...
✅ Todos os serviços importados com sucesso
✅ Arquivo encontrado: data/patterns.csv
✅ Arquivo encontrado: data/guideline_map.csv
🎉 API inicializada com sucesso!
```

❌ **Problemas:**
```
❌ Erro durante inicialização: [erro]
⚠️ Arquivo não encontrado: [arquivo]
❌ Erro no health check: [erro]
```

## 🎯 Próximos Passos

1. **Monitoramento**: Configurar alertas para downtime
2. **Performance**: Otimizar tempo de cold start
3. **Escalabilidade**: Considerar upgrade para plano pago
4. **Backup**: Implementar estratégia de backup dos dados

---

**Status**: ✅ API funcionando corretamente  
**Última atualização**: Janeiro 2025  
**Versão**: 1.0.0