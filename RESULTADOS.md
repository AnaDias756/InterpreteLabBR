# 4. Resultados Obtidos

> **Documento de trabalho — Etapa 4 (Capítulo dos Resultados).** Este capítulo
> relata os resultados da aplicação da metodologia descrita na proposta
> (Seção 6, Frentes A, B e C). Ele distingue explicitamente **dois tipos de
> resultado**:
>
> 1. **Resultados já apurados** — deriváveis do próprio artefato e de suas
>    tabelas de referência, portanto **determinísticos e reprodutíveis** a
>    qualquer momento (Frente B — concordância da classificação; e a comparação
>    analítica PNS × referência estrangeira). Os números aqui são reais.
> 2. **Resultados pendentes de coleta empírica** — dependem de material que, por
>    exigência de anonimização (LGPD), **não é versionado** no repositório:
>    laudos reais do SUS (Frente A) e respostas de usuários ao questionário SUS
>    (Frente C). Para esses, o capítulo apresenta o **instrumento de medição já
>    construído e validado**, tabelas-modelo com marcadores `[PENDENTE — dados
>    reais]`, e uma **demonstração sintética claramente rotulada** que ilustra o
>    formato final da apuração. **Nenhum número sintético deve ser lido como
>    achado do estudo.**
>
> Toda a apuração é regenerável com um único comando (Seção 4.7), de modo que,
> à medida que os dados reais forem inseridos, tabelas, estatísticas e figuras
> se atualizam automaticamente.

---

## 4.1. O produto: aplicativo móvel InterpreteLabBR

O primeiro resultado é o próprio artefato — o cumprimento do **Objetivo
Específico 2** (portar a solução para aplicativo móvel consumindo a API
existente). O aplicativo foi desenvolvido em **React Native com Expo (SDK 54)**,
em TypeScript, e consome a API **FastAPI** do backend já existente.

**Funcionalidades entregues** (código em `mobile/`):

| Componente | Arquivo | Função |
|---|---|---|
| Entrada manual de valores | `mobile/src/components/ManualEntryForm.tsx` | Digitação dos 14 analitos do hemograma |
| Envio de PDF | `mobile/src/components/PdfUpload.tsx` | Upload do laudo (extração automática via API) |
| Dados do paciente | `mobile/src/components/PatientForm.tsx` | Sexo e idade (estratificação da PNS) |
| Resultados | `mobile/src/components/Results.tsx` | Achados, especialidades e *briefing* ao paciente |
| Comparação de referências | `mobile/src/components/ReferenceComparisonTable.tsx` | PNS × referência do laudo, lado a lado |
| Verificação de disponibilidade | `App.tsx` (`healthCheck`) | Status do servidor (online/offline) |

O aplicativo replica e amplia as capacidades do PWA original, mantendo a
**coerência de base pública**: valores de referência da PNS e leiaute de laudo
do SUS.

> **Figura 1 — Telas do aplicativo.** `[PENDENTE — inserir capturas de tela do
> app em execução: (a) modo de entrada manual; (b) envio de PDF; (c) tela de
> resultados com briefing; (d) tabela de comparação de referências.]`

---

## 4.2. Frente A — Acurácia da extração automática

### 4.2.1. Instrumento de medição

A Frente A é operacionalizada pelo harness `tests/validacao_extracao.py`, que
confronta os valores extraídos automaticamente do PDF com um **gabarito
conferido manualmente** e calcula, por analito e de forma agregada:
**acurácia** (corretos/esperados), **precisão**, **recall** e **F1-score**,
além de discriminar **ausentes**, **incorretos** e **falsos positivos**. A
comparação numérica usa tolerância absoluta/relativa para absorver
arredondamentos de impressão.

### 4.2.2. Resultado com dados reais — pendente de coleta

Os **20–30 laudos reais anonimizados** do SUS e seu gabarito ainda não foram
incorporados (pasta `tests/laudos/`, ignorada pelo Git por LGPD). A Tabela 1
está pronta para receber os números assim que a base for processada.

**Tabela 1 — Desempenho agregado da extração (a preencher).**

| Métrica | Valor |
|---|---|
| Laudos avaliados | `[PENDENTE]` |
| Analitos esperados | `[PENDENTE]` |
| Acurácia de extração | `[PENDENTE]` |
| Precisão | `[PENDENTE]` |
| Recall | `[PENDENTE]` |
| F1-score | `[PENDENTE]` |
| Ausentes / Incorretos / Falsos positivos | `[PENDENTE]` |

**Tabela 2 — Acurácia por analito (a preencher):** hemácias, hemoglobina,
hematócrito, VCM, HCM, CHCM, RDW, leucócitos, neutrófilos, eosinófilos,
basófilos, linfócitos, monócitos, plaquetas — `[PENDENTE — acertos/total por
analito]`.

### 4.2.3. Demonstração do método (dado sintético)

Para evidenciar o funcionamento do instrumento, ele foi executado sobre um
**laudo sintético** (gerado por `generate_sample_pdf.py`, sem dados pessoais).
Nesse laudo — de impressão limpa, sem ruído de digitalização — a extração
atingiu **14/14 analitos corretos (100%)**, com precisão, recall e F1 iguais a
**1,000** (Figura 2). Esse valor **não é um resultado do estudo**: mede apenas o
"caminho feliz" sobre um PDF idealizado, e serve de limite superior teórico. O
desempenho sobre laudos reais — sujeitos a ruído de digitalização e OCR — é
justamente o que a Frente A pretende medir e tende a ser inferior.

> **Figura 2** — `docs/figuras/fig_frente_a_acuracia.png` (demonstração sintética).

---

## 4.3. Frente B — Concordância da classificação

### 4.3.1. Concordância do motor com a aplicação manual da PNS

A Frente B (script `tests/validacao_classificacao.py`) mede a **fidelidade do
motor de regras** (`backend/services/rule_engine.py`) à aplicação manual das
faixas da PNS. Um **leitor independente** das mesmas tabelas
(`data/guideline_map.csv`), reimplementado à parte do motor, funciona como
gabarito. Os casos de teste são gerados sistematicamente **em torno de cada
limite de referência** (bem abaixo, no limite, logo abaixo/acima do limite, no
miolo da faixa), maximizando a densidade de **casos de borda** — onde erros de
classificação costumam surgir.

**Resultados (reais, determinísticos):**

| Indicador | Valor |
|---|---|
| Casos avaliados | **495** (327 em zona de borda) |
| Concordância global | **495/495 (100,0%)** |
| Concordância em zonas de borda | **327/327 (100,0%)** |
| Kappa de Cohen (global) | **1,000** |
| Kappa de Cohen (bordas) | **1,000** |
| Concordância por estrato (M 18–59 / M 60+ / F 18–59 / F 60+) | 100% em todos |

**Tabela 3 — Matriz de confusão (motor × PNS manual).**

| Manual PNS \ Sistema | baixo | normal | alto |
|---|---|---|---|
| **baixo** | 95 | 0 | 0 |
| **normal** | 0 | 288 | 0 |
| **alto** | 0 | 0 | 112 |

> **Figura 3** — `docs/figuras/fig_frente_b_matriz.png` (matriz de confusão).

**Interpretação e ressalva metodológica.** A concordância perfeita
(κ = 1,00; classificação segundo Landis & Koch, 1977: "concordância quase
perfeita") indica que o motor **implementa fielmente** a tabela de decisão da
PNS, inclusive no **tratamento dos limites** (valor exatamente no limite é
classificado como *normal*; abaixo, *baixo*; acima, *alto*), sem defeitos de
borda. Cabe explicitar que se trata de uma **validação de implementação
(consistência interna)**: como o gabarito manual e o motor consultam a mesma
tabela, a concordância elevada é esperada, e o valor científico do teste está em
**detectar eventuais divergências de implementação** (que não ocorreram). Esse
achado **não afirma acurácia clínica** nem valida a PNS em si; atesta que o
software não introduz erros ao aplicar as faixas. Quando os valores reais
extraídos na Frente A estiverem disponíveis, o mesmo harness poderá ser
reexecutado sobre eles, com um segundo avaliador humano, para uma concordância
**inter-avaliador** propriamente dita.

### 4.3.2. Comparação PNS × referência estrangeira (achado real)

Um resultado adicional, central para a **justificativa** do trabalho, decorre da
comparação entre a referência da PNS e a **referência clássica estrangeira**
(Wintrobe; Dacie & Lewis) impressa no laudo do SUS
(`tests/comparacao_referencias.py`). Para cada analito × sexo × faixa etária,
mede-se a faixa de valores em que as duas referências **classificam de modo
diferente**.

**Síntese (real):**

| Indicador | Valor |
|---|---|
| Comparações (analito × sexo × faixa) | **42** |
| Taxa média de discordância (amostragem uniforme) | **18,6%** |
| Kappa médio (PNS × estrangeira) | **0,69** |
| Analitos em que a PNS é menos sensível a valores **baixos** | **38/42** |

Os analitos com **maior divergência** foram basófilos (37,2%), monócitos
(28,1%), plaquetas e RDW (25,2%) e neutrófilos (24,2%) — Figura 4. A direção
predominante da discordância é reveladora: na maioria dos estratos, o **limite
inferior da PNS é mais baixo** que o da referência estrangeira, de modo que
valores que a referência importada classificaria como **"baixo"** são, pela PNS,
**"normais"** para a população adulta brasileira. Isso é coerente com a
literatura hematológica nacional (valores de série vermelha e branca
sistematicamente distintos dos padrões norte-americanos/europeus) e sustenta,
empiricamente, o argumento de **precisão populacional** que motiva o projeto: o
uso de tabelas estrangeiras tenderia a **superdiagnosticar alterações** (sobretudo
citopenias) em brasileiros.

> **Figura 4** — `docs/figuras/fig_pns_vs_lab_discordancia.png` (discordância por analito).

> **Nota:** esta é uma comparação **analítica das tabelas de referência** (não
> depende de laudos coletados) e, portanto, é um resultado real e estável. Ela
> não se confunde com a Frente B da proposta (concordância do sistema com a
> PNS), mas a complementa, quantificando o **impacto clínico** de adotar a
> referência nacional.

---

## 4.4. Frente C — Usabilidade percebida (SUS)

### 4.4.1. Instrumento

A Frente C aplica a **System Usability Scale** (SUS; Brooke, 1996), questionário
psicométrico de 10 itens em escala Likert 1–5. O escore por participante é
calculado por `tests/pontuacao_sus.py` conforme a regra canônica (itens ímpares:
resposta − 1; itens pares: 5 − resposta; soma × 2,5 → 0–100), e reporta-se a
**média**, o **desvio-padrão**, a **classificação adjetiva** (Bangor et al.,
2009) e a **faixa de percentil** (referência de mercado: média ≈ 68).

### 4.4.2. Resultado com usuários reais — pendente de coleta

A coleta com a **amostra por conveniência** de usuários finais ainda não foi
realizada. O modelo de coleta está em `tests/respostas_sus_modelo.csv`
(anonimizado: P01, P02, …).

**Tabela 4 — Resultado SUS (a preencher).**

| Métrica | Valor |
|---|---|
| Participantes (n) | `[PENDENTE]` |
| Escore SUS médio (0–100) | `[PENDENTE]` |
| Desvio-padrão | `[PENDENTE]` |
| Mediana | `[PENDENTE]` |
| Classificação adjetiva | `[PENDENTE]` |
| Principais achados qualitativos | `[PENDENTE]` |

### 4.4.3. Demonstração do método (dado sintético)

Sobre um conjunto **fictício** de 12 respostas (`respostas_sus_exemplo.csv`), a
tubulação produz escore médio **78,3** (DP 18,2; mediana 81,2; faixa 37,5–97,5),
"Bom" na escala de Bangor (Figura 5). **Esses números são ilustrativos e não
representam usuários reais** — servem apenas para demonstrar a apuração e o
formato do gráfico.

> **Figura 5** — `docs/figuras/fig_frente_c_sus.png` (demonstração sintética, rotulada).

---

## 4.5. Síntese: resultados obtidos × resultados esperados

Confronto com os **Resultados Esperados** da proposta (Seção 7):

| Resultado esperado (proposta) | Situação | Evidência |
|---|---|---|
| Aplicativo móvel funcional (PNS) | **Alcançado** | `mobile/` (Seção 4.1) |
| Relatório de acurácia de extração (P/R/F1) | **Instrumento pronto; dados pendentes** | Seção 4.2; harness validado (100% no sintético) |
| Concordância de classificação (kappa/%) | **Alcançado (validação de implementação)** | Seção 4.3.1: κ = 1,00; 495 casos |
| Impacto da referência nacional | **Alcançado (bônus)** | Seção 4.3.2: 18,6% de discordância média |
| Escore de usabilidade (SUS) | **Instrumento pronto; dados pendentes** | Seção 4.4 |
| Identificação de limitações e trabalhos futuros | **Alcançado** | Seção 4.6 |

---

## 4.6. Validade, limitações e extensão dos dados

**Validade interna.** A Frente B (κ = 1,00) demonstra que o motor não introduz
erros na aplicação das faixas da PNS, inclusive nas bordas — a fonte de erro
mais provável. A comparação PNS × estrangeira é puramente analítica e, portanto,
não sujeita a viés amostral.

**Limitações a explicitar (honestidade metodológica):**

1. **Frente A ainda não medida em campo:** o 100% sintético reflete um PDF
   idealizado; laudos reais têm ruído de digitalização/OCR, e o desempenho real
   tende a ser inferior — essa é exatamente a lacuna a preencher.
2. **Frente B é validação de consistência interna:** por construção, gabarito e
   motor leem a mesma tabela; a concordância elevada é esperada e **não** afere
   acurácia clínica nem concordância inter-avaliador com valores reais.
3. **Casos de borda sintéticos** cobrem sistematicamente os limites, mas **não**
   reproduzem padrões multi-analito reais (ex.: perfis de anemia).
4. **Severidade fixa em 1** (simplificação assumida na proposta, Seção 5.2): a
   recomendação de especialidades opera por frequência, não por magnitude do
   desvio — sua validação formal não integra as Frentes A–C.
5. **Frente C pendente**, e, quando realizada, usará **amostra por conveniência**
   (validade externa limitada) e um **único leiaute (SUS)**.

**Extensão dos dados (generalização).** Os resultados se restringem a
**hemogramas de adultos** em **leiaute do SUS**; não se estendem a população
pediátrica, a outros exames, nem a laudos de rede privada com leiautes
proprietários (delimitações da proposta, Seção 2.3).

**Comparação com outros estudos (a consolidar na redação final):**

- **Extração/OCR:** confrontar o F1 obtido na Frente A com faixas relatadas na
  literatura de extração de documentos clínicos. `[PENDENTE — inserir
  referências e valores após a Frente A]`
- **Concordância (kappa):** interpretação por Landis & Koch (1977) — κ > 0,80 =
  "quase perfeita". `[confirmar citação no padrão ABNT da instituição]`
- **SUS:** a média de mercado é ≈ 68 (Sauro, 2011); um escore ≥ 80,3 situa-se
  no percentil ~90. `[PENDENTE — comparar com o escore real da Frente C]`

---

## 4.7. Reprodutibilidade

Todos os resultados deste capítulo são regeneráveis. Pré-requisitos:
`pip install pandas numpy matplotlib pdfplumber PyMuPDF PyPDF2 reportlab`.

```bash
# Demonstração completa (Frentes A e C sobre exemplos sintéticos; B e PNS×Lab reais)
python tests/gerar_resultados.py

# Com dados reais, quando disponíveis:
python tests/gerar_resultados.py \
    --laudos tests/laudos --gabarito tests/meu_gabarito.json \
    --respostas-sus tests/respostas_sus.csv
```

**Artefatos gerados:**

- `tests/saidas/` — CSVs e JSONs com as apurações (extração, classificação,
  comparação de referências, SUS);
- `docs/figuras/` — figuras do capítulo (PNG).

**Scripts:** `tests/validacao_extracao.py` (Frente A), `tests/validacao_classificacao.py`
(Frente B), `tests/comparacao_referencias.py` (PNS × estrangeira),
`tests/pontuacao_sus.py` (Frente C), `tests/gerar_graficos.py` (figuras),
`tests/gerar_resultados.py` (orquestrador).

---

## Referências adicionais deste capítulo

> A serem integradas à lista geral no padrão ABNT/instituição.

- BANGOR, A.; KORTUM, P.; MILLER, J. Determining what individual SUS scores mean:
  adding an adjective rating scale. **Journal of Usability Studies**, v. 4, n. 3,
  p. 114–123, 2009.
- BROOKE, J. SUS: a 'quick and dirty' usability scale. In: JORDAN, P. W. et al.
  (Eds.). **Usability Evaluation in Industry**. London: Taylor & Francis, 1996.
- LANDIS, J. R.; KOCH, G. G. The measurement of observer agreement for
  categorical data. **Biometrics**, v. 33, n. 1, p. 159–174, 1977.
- ROSENFELD, L. G. et al. Valores de referência para exames laboratoriais de
  hemograma da população adulta brasileira: Pesquisa Nacional de Saúde.
  **Revista Brasileira de Epidemiologia**, v. 22, supl. 2, e190003, 2019.
- SAURO, J. **A Practical Guide to the System Usability Scale**. Denver:
  Measuring Usability LLC, 2011. `[confirmar edição/fonte]`
