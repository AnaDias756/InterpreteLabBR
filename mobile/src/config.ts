// URL base da API (backend FastAPI).
//
// PRODUÇÃO (Render, em uso): backend público em interpretador-lab-backend.
// É o mesmo serviço usado pelo PWA. Funciona com o app instalado em qualquer
// rede (não depende do PC na Wi-Fi local). O primeiro acesso pode demorar
// ~50s por causa do "cold start" do plano grátis do Render.
export const API_BASE_URL = 'https://interpretador-lab-backend.onrender.com';

// DESENVOLVIMENTO LOCAL: aponta para o backend rodando na sua máquina,
// acessível pelo celular via IP da rede local. "localhost" NÃO funciona a
// partir do celular — tem que ser o IP do PC na Wi-Fi. Ajuste o IP conforme
// sua rede (veja com `ipconfig` no Windows) e descomente para testar local.
// export const API_BASE_URL = 'http://192.168.0.74:8000';
