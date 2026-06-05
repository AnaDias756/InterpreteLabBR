// URL base da API (backend FastAPI).
//
// DESENVOLVIMENTO LOCAL (em uso): aponta para o backend rodando na sua
// máquina, acessível pelo celular via IP da rede local. "localhost" NÃO
// funciona a partir do celular — tem que ser o IP do PC na Wi-Fi.
// Se o IP do seu PC mudar, ajuste aqui (veja com `ipconfig` no Windows).
export const API_BASE_URL = 'http://192.168.0.74:8000';

// PRODUÇÃO (Render): só funciona depois que o backend novo (com a rota
// /interpret-manual) for deployado no Render. Enquanto não houver deploy,
// usar o local acima.
// export const API_BASE_URL = 'https://interpretador-lab-backend.onrender.com';
