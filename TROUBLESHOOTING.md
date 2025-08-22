# Guia de Solução de Problemas - Interpretador de Laudos

## Problema: Frontend não conecta com a API

### Soluções Implementadas:

1. **✅ Rebuild do Frontend**
   - Executado `npm run build` para aplicar as variáveis de ambiente
   - Variável `REACT_APP_API_URL` configurada corretamente

2. **✅ Configuração de CORS**
   - Backend atualizado para permitir conexões do Netlify
   - CORS configurado para aceitar todas as origens temporariamente

3. **✅ Variáveis de Ambiente no Netlify**
   - `netlify.toml` atualizado com `REACT_APP_API_URL`
   - Garantia de que o Netlify usa a URL correta da API

4. **✅ Teste de Conexão**
   - Arquivo `test-api-connection.html` criado para testar diretamente
   - Permite verificar se a API está acessível

### Próximos Passos para o Usuário:

#### 1. Limpar Cache do Navegador
```
- Chrome/Edge: Ctrl + Shift + Delete
- Firefox: Ctrl + Shift + Delete
- Safari: Cmd + Option + E
```

#### 2. Forçar Atualização da Página
```
- Ctrl + F5 (Windows)
- Cmd + Shift + R (Mac)
```

#### 3. Verificar Console do Navegador
```
- F12 → Console
- Procurar por erros de CORS ou conexão
```

#### 4. Testar em Modo Incógnito
```
- Ctrl + Shift + N (Chrome)
- Ctrl + Shift + P (Firefox)
```

#### 5. Verificar Status da API
```
Acesse: https://interpretador-lab-backend.onrender.com/health
Deve retornar: {"status": "healthy", "message": "API esta funcionando corretamente"}
```

### URLs Importantes:
- **Frontend**: https://interpretlabbr.netlify.app
- **API**: https://interpretador-lab-backend.onrender.com
- **Health Check**: https://interpretador-lab-backend.onrender.com/health

### Se o Problema Persistir:
1. Aguarde 5-10 minutos (cold start do Render)
2. Verifique se ambos os serviços estão online
3. Teste a conexão usando o arquivo `test-api-connection.html`
4. Contate o suporte técnico com detalhes do console do navegador