# InterpreteLabBR — App Móvel (Expo / React Native)

Aplicativo móvel do Interpretador de Hemograma. Consome o mesmo backend
(FastAPI) do projeto e classifica os valores segundo a referência da
população adulta brasileira (PNS), exibindo também a comparação com a
referência laboratorial clássica.

> **Status:** primeiro incremento — fluxo de **entrada manual** completo
> (digitação dos valores). O upload de PDF será adicionado em seguida
> (requer `expo-document-picker`).

## Pré-requisitos

- Node.js 18+
- Aplicativo **Expo Go** instalado no seu celular (Android ou iOS), OU um
  emulador Android/iOS.

## Como rodar (no seu celular, via Expo Go)

```bash
cd mobile
npm install        # caso ainda não tenha as dependências
npx expo start
```

Será exibido um **QR Code** no terminal. Abra o app **Expo Go** no celular e
escaneie o QR Code (o celular e o computador precisam estar na mesma rede
Wi‑Fi). O app abre direto no seu telefone.

## Configuração da API

O app aponta, por padrão, para o backend publicado no Render
(veja `src/config.ts`). Para usar um backend **local**, edite `API_BASE_URL`
com o IP da sua máquina na rede (não use `localhost`, pois o celular não
enxerga o `localhost` do computador):

```ts
export const API_BASE_URL = 'http://192.168.0.10:8000';
```

> Observação: o backend no Render pode levar alguns segundos para "acordar"
> no primeiro acesso (cold start). Se aparecer "Servidor offline", aguarde e
> reabra o app.

## Estrutura

```
mobile/
├── App.tsx                       # Tela principal (orquestra o fluxo)
└── src/
    ├── config.ts                 # URL da API
    ├── types.ts                  # Tipos compartilhados
    ├── api.ts                    # Chamadas ao backend (axios)
    ├── theme.ts                  # Cores e helpers de classificação
    └── components/
        ├── PatientForm.tsx       # Sexo e idade
        ├── ManualEntryForm.tsx   # Digitação dos analitos
        ├── Results.tsx           # Achados, especialidades, briefing
        └── ReferenceComparisonTable.tsx  # Comparação PNS × laboratorial
```

## Gerar APK (instalável, sem Expo Go)

Quando quiser um APK para distribuir/instalar diretamente, use o EAS Build
(build na nuvem da Expo):

```bash
npm install -g eas-cli
eas login
eas build -p android --profile preview
```
