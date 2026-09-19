# 5. Resultados Obtidos

> **Documento de trabalho — Capítulo de Resultados (enquadramento do TCC/Overleaf:
> "Migração PWA → Mobile: Análise de Engenharia de Software").** As Frentes aqui
> seguem a metodologia do TCC atual: **A — Desempenho** (ADB), **B — Engenharia
> da migração** (reuso) e **C — Usabilidade** (inspeção heurística de Nielsen).
>
> O capítulo distingue dois tipos de resultado:
>
> 1. **Já apurados (reais):** a Frente B é derivada da análise do próprio código
>    e é **determinística e reprodutível** — os números são reais.
> 2. **Pendentes de coleta empírica:** a Frente A depende dos ensaios com ADB em
>    dispositivo físico, e a Frente C depende das inspeções dos 5 especialistas.
>    Para essas, apresenta-se o **instrumento já construído**, tabelas-modelo com
>    `[PENDENTE — dados reais]`, e uma **demonstração sintética claramente
>    rotulada** que ilustra o formato final. **Nenhum número sintético deve ser
>    lido como achado do estudo.**
>
> A apuração é regenerável (Seção 5.7).

---

## 5.1. O produto: aplicativo móvel InterpreteLabBR

O primeiro resultado é o artefato: o cliente móvel em **React Native/Expo**
(TypeScript), que consome a mesma API **FastAPI** do PWA. As funcionalidades da
versão web foram preservadas (entrada manual de valores, envio de PDF,
verificação de disponibilidade do servidor, exibição de resultados/briefing e
tabela de comparação de referências PNS × laudo), com a interface reconstruída
em primitivas nativas. A caracterização técnica dessa migração é o objeto da
Frente B (Seção 5.3).

> **Figura 1 — Telas do aplicativo.** `[PENDENTE — capturas de tela: entrada
> manual; envio de PDF; resultados/briefing; comparação de referências.]`

---

## 5.2. Frente A — Desempenho comparativo (ADB)

### 5.2.1. Instrumento e protocolo

A Frente A compara PWA e cliente móvel sobre as mesmas tarefas (T1 inicialização;
T2 submissão de PDF; T3 rolagem; T4 renderização de tabelas), no **mesmo
dispositivo Android**, com **10 execuções por tarefa e cliente**, alternadas para
diluir efeitos térmicos e de processos concorrentes. As métricas — tempo de
resposta, uso de CPU, memória (RAM), taxa de quadros (FPS) e energia estimada —
são coletadas via **Android Debug Bridge (ADB)** e `dumpsys`
(`gfxinfo`/`meminfo`/`batterystats`). O protocolo completo, com os comandos, está
em `docs/protocolo_frente_a_desempenho_adb.md`; a coleta é apoiada por
`tests/coletar_desempenho.sh` e a análise por `tests/analisar_desempenho.py`.

### 5.2.2. Resultado com dados reais — pendente de coleta

Os ensaios em dispositivo físico ainda não foram executados. A Tabela 1 está
pronta para receber os valores (média ± desvio-padrão).

**Tabela 1 — Desempenho PWA × Móvel (a preencher).**

| Métrica (direção) | PWA | Móvel | Δ |
|---|---|---|---|
| Tempo de inicialização — T1 (ms, ↓) | `[PENDENTE]` | `[PENDENTE]` | |
| Tempo de submissão de PDF — T2 (ms, ↓) | `[PENDENTE]` | `[PENDENTE]` | |
| CPU em rolagem — T3 (%, ↓) | `[PENDENTE]` | `[PENDENTE]` | |
| Memória — T2 (MB, ↓) | `[PENDENTE]` | `[PENDENTE]` | |
| FPS em rolagem — T3 (fps, ↑) | `[PENDENTE]` | `[PENDENTE]` | |
| Energia estimada — T3 (mAh, ↓) | `[PENDENTE]` | `[PENDENTE]` | |

### 5.2.3. Demonstração do método (dado sintético)

A Figura 2 ilustra a apuração sobre um conjunto **fictício** de medições (10 por
célula), com um painel por métrica (barras = média; hastes = desvio-padrão).
**Esses valores não são resultados do estudo** — servem apenas para demonstrar o
formato e a leitura da análise. A hipótese do trabalho (ganho de desempenho do
cliente nativo sobre o PWA baseado em *webview*) só será confirmada ou refutada
com as medições reais.

> **Figura 2** — `docs/figuras/fig_frente_a_desempenho_adb.png` (demonstração sintética).

---

## 5.3. Frente B — Engenharia da migração (resultados reais)

Esta frente caracteriza, por **análise documental comparativa** das duas bases de
código, o reuso arquitetural viabilizado pela estratégia *API-first*. A seção
completa, formatada para o TCC, está em `docs/frente_b_engenharia_migracao.tex`
(tabelas de *endpoints*, mapa de migração e taxa de reuso). Os principais
achados, **reais e extraídos do repositório**, são:

**Tabela 2 — Taxa de reuso por camada (migração PWA → Mobile).**

| Camada | Reuso | Evidência |
|---|---|---|
| Lógica de negócio (*backend* + regras) | **100%** | 1.654 LOC Python + 145 linhas CSV, sem alteração |
| Contrato de dados (interfaces TS) | **≈100%** | 5 interfaces de domínio migradas *verbatim* |
| Serviços de comunicação (rede) | **3/3 operações** | Semântica preservada; transporte adaptado (File → FormData nativo) |
| Apresentação (componentes de UI) | Reescrita estrutural | Padrão (ii): estrutura/estado preservados, primitivas nativas |
| Utilitários de contorno de *webview* | **0% (eliminados)** | 1.239 LOC descartadas |

**Achados centrais:**

1. A arquitetura *API-first* permitiu **reuso integral (100%) de toda a lógica
   clinicamente sensível** — extração, classificação pela PNS, seleção de
   especialidades e *briefing* —, consumida pelos mesmos três *endpoints* REST
   (`/health`, `/interpret`, `/interpret-manual`) sem uma linha reescrita.
2. O esforço de reengenharia **confinou-se à camada de apresentação**,
   majoritariamente sob portabilidade estrutural; substituições nativas
   restringiram-se aos pontos de contato com *hardware*/ambiente (seletor de
   arquivos, indicador de carregamento, *bootstrap*).
3. A migração **eliminou 1.239 linhas** de utilitários de contorno de *webview*
   (`polyfills`, `mobileDetection`, `mobileOptimizations`) — **49% de todo o
   código do cliente web** —, tornadas desnecessárias pela renderização nativa.
   Esse é o correlato, no plano do código, do *overhead* que a literatura atribui
   às soluções baseadas em *webview*.

Confirma-se, assim, a hipótese de reuso: a separação *API-first* preserva o
núcleo funcional (o ativo de maior valor e risco) e localiza a migração na
interface.

---

## 5.4. Frente C — Usabilidade (inspeção heurística)

### 5.4.1. Instrumento

A Frente C avalia a usabilidade por **inspeção heurística** (Nielsen, 1994): 5
especialistas em IHC inspecionam, de forma independente, os dois clientes (PWA e
móvel) sobre os mesmos cenários, registrando violações às 10 heurísticas e
classificando cada problema em uma escala de severidade **0–4**. O protocolo de
coleta está em `docs/protocolo_frente_c_inspecao_heuristica.md`; a consolidação
e as métricas são geradas por `tests/consolidar_inspecao.py`. Por dispensar
usuários finais, o método não requer submissão a CEP.

### 5.4.2. Resultado com especialistas — pendente de coleta

As inspeções ainda não foram realizadas. A Tabela 3 está pronta para os dados
consolidados.

**Tabela 3 — Síntese comparativa da inspeção (a preencher).**

| Métrica | PWA | Móvel |
|---|---|---|
| Problemas registrados | `[PENDENTE]` | `[PENDENTE]` |
| Índice médio de severidade | `[PENDENTE]` | `[PENDENTE]` |
| Problemas de severidade 3–4 | `[PENDENTE]` | `[PENDENTE]` |
| Heurísticas mais violadas | `[PENDENTE]` | `[PENDENTE]` |

### 5.4.3. Demonstração do método (dado sintético)

A Figura 3 ilustra a consolidação sobre registros **fictícios** de 5 avaliadores,
com a distribuição de problemas por heurística em cada cliente. **Os números são
ilustrativos** e não representam inspeções reais.

> **Figura 3** — `docs/figuras/fig_frente_c_inspecao_heuristica.png` (demonstração sintética).

---

## 5.5. Síntese: resultados obtidos × hipóteses

| Dimensão (hipótese) | Situação | Evidência |
|---|---|---|
| Artefato móvel funcional | **Alcançado** | Seção 5.1 (`mobile/`) |
| Ganho de desempenho (A) | **Instrumento pronto; dados pendentes** | Seção 5.2 |
| Reuso arquitetural *API-first* (B) | **Alcançado (real)** | Seção 5.3: 100% da lógica; −1.239 LOC de *webview* |
| Ganho de usabilidade (C) | **Instrumento pronto; dados pendentes** | Seção 5.4 |

A hipótese de **reuso** (Frente B) está empiricamente confirmada. As hipóteses de
**desempenho** (A) e **usabilidade** (C) têm instrumentos validados e aguardam a
coleta em dispositivo/painel de especialistas.

---

## 5.6. Validade, limitações e extensão dos dados

**Validade interna.** A Frente B baseia-se na inspeção direta do código-fonte, não
sujeita a viés amostral. As Frentes A e C controlam variáveis por desenho
(dispositivo único e execução alternada em A; heurísticas consagradas e severidade
padronizada em C).

**Limitações a explicitar:**

1. **Frente A:** medida em **um único dispositivo** de entrada e 10 repetições —
   limita a generalização das métricas absolutas; interessa o resultado
   **relativo** (sentido e magnitude da diferença). Há **assimetria de medição**
   PWA × nativo (p. ex., *cold start*/FPS por mecanismos distintos), a descrever
   no relatório.
2. **Frente B:** classificação por **análise documental comparativa** do estado
   final do código (não por diário de bordo em tempo real); trata-se de
   reconstrução retrospectiva do mapa de migração.
3. **Frente C:** **inspeção por especialistas**, não por usuários finais — capta
   problemas de conformidade heurística, mas **não** mede aceitação subjetiva no
   ponto de cuidado; painel limitado a 5 avaliadores.

**Extensão (generalização).** Os resultados restringem-se ao domínio específico
(interpretação de hemogramas no padrão do SUS), à *stack* adotada (React Native,
Expo, FastAPI) e ao perfil de dispositivo testado. As conclusões **relativas**
sobre reuso e desempenho têm potencial de transferência para migrações
arquiteturais correlatas.

---

## 5.7. Reprodutibilidade

Pré-requisitos: `pip install pandas numpy matplotlib` (e, para a Frente A real,
`android platform-tools`/ADB e um dispositivo).

```bash
# Frente B — regenera métricas de reuso a partir do código (determinístico)
#   (ver docs/frente_b_engenharia_migracao.tex; números conferidos no repositório)

# Frente A — análise das medições (após coleta com ADB)
python tests/analisar_desempenho.py --entrada tests/desempenho.csv \
    --relatorio-json tests/saidas/desempenho_resumo.json

# Frente C — consolidação das inspeções (após coleta)
python tests/consolidar_inspecao.py --entrada tests/inspecao_heuristica.csv \
    --relatorio-json tests/saidas/inspecao_resumo.json

# Figuras do capítulo (usa os exemplos sintéticos se não houver dados reais)
python tests/gerar_graficos.py
```

**Figuras:** `docs/figuras/`. **Saídas intermediárias:** `tests/saidas/`
(regeneráveis). **Instrumentos:** `docs/protocolo_frente_a_desempenho_adb.md`,
`docs/frente_b_engenharia_migracao.tex`,
`docs/protocolo_frente_c_inspecao_heuristica.md`.

---

## Referências adicionais deste capítulo

> A integrar à bibliografia no padrão ABNT/SBC do trabalho.

- NIELSEN, J. **Usability Engineering**. San Francisco: Morgan Kaufmann, 1994.
- OLIVEIRA, W. et al. *Overhead* de recursos em *frameworks* de desenvolvimento
  móvel, 2023. `[completar no padrão do trabalho]`
- CARDIERI, G. A.; ZAINA, L. A. M. Analyzing the User Experience in Mobile Web,
  Native and PWAs. **IHC 2018**. `[confirmar dados]`
