# PROPOSTA DE TRABALHO DE CONCLUSÃO DE CURSO

### Documento de Escopo Temático e Alinhamento de Orientação

> Documento de escopo para alinhamento com o(a) orientador(a). Versão preliminar — sujeita a refinamento.

| Campo | Preenchimento |
|---|---|
| **Aluno(a)** | _[preencher]_ |
| **Orientador(a)** | _[preencher]_ |
| **Curso / Programa** | _[preencher — Pós-Graduação]_ |
| **Instituição** | _[preencher]_ |
| **Data** | _[preencher]_ |

---

## 1. Identificação Geral

- **Título provisório:** Aplicativo móvel de apoio à decisão para triagem de hemogramas fundamentado em valores de referência da população adulta brasileira (PNS): validação da extração, da classificação e da usabilidade.
- **Natureza do trabalho:** Desenvolvimento de ferramenta computacional aplicada + estudo de validação.
- **Áreas/temas correlatos (lista do curso):** Sistemas de Apoio à Decisão; Aplicativos para plataformas móveis; Processamento e análise de imagens; Inteligência Artificial aplicada à Saúde; Inclusão Digital; Software Livre e Administração Pública.
- **Base de continuidade:** Evolução de um ecossistema de software preexistente (**InterpreteLabBR**) com a introdução de um eixo científico de validação metodológica de triagem.

---

## 2. Introdução e Contextualização

Este projeto de pós-graduação baseia-se na evolução incremental de um artefato computacional concebido originalmente no projeto de conclusão de graduação realizado na Universidade Federal Fluminense (UFF). Naquela etapa, foi desenvolvido um protótipo em formato *Progressive Web App* (PWA) denominado **InterpreteLabBR**. O código-fonte original, que serve de alicerce para a presente arquitetura móvel, encontra-se publicado e acessível no repositório público no GitHub: <https://github.com/AnaDias756/InterpreteLabBR>.

O hemograma consolida-se como um dos exames laboratoriais mais requisitados na rotina diagnóstica no Brasil. Contudo, a interpretação das métricas por usuários leigos apresenta barreiras significativas, frequentemente agravadas pelo fato de os valores de referência impressos nos laudos nacionais derivarem de matrizes populacionais estrangeiras. O projeto InterpreteLabBR mitiga essa lacuna ao implementar um *pipeline* automatizado que extrai os valores analíticos de laudos em formato PDF (utilizando técnicas de *parsing* de texto e reconhecimento óptico de caracteres — OCR), classifica cada analito como *normal*, *alto* ou *baixo* e gera um *briefing* educativo ao paciente, sugerindo especialidades quando pertinente.

Há, no projeto, uma **coerência integral de base pública**: tanto os **valores de referência** (PNS / Ministério da Saúde) quanto o **documento de entrada** (laudo padrão do SUS) originam-se do sistema público de saúde brasileiro.

O grande diferencial científico e o núcleo motor de regras das classificações desta proposta reside no seguinte estudo referencial:

> ROSENFELD, Luiz Gastão et al. **Valores de referência para exames laboratoriais de hemograma da população adulta brasileira: Pesquisa Nacional de Saúde.** Revista Brasileira de Epidemiologia, v. 22, supl. 2, art. e190003, 2019. DOI: 10.1590/1980-549720190003.supl.2.

Este consiste no **único estudo que estabeleceu parâmetros hematológicos específicos para adultos brasileiros por meio do método paramétrico**, utilizando dados abrangentes da Pesquisa Nacional de Saúde (PNS), conferindo ao sistema aderência estrita à realidade epidemiológica nacional — diferencial ausente na maioria das ferramentas similares.

### 2.1. Objetivos

**Objetivo geral:** Evoluir a solução InterpreteLabBR para um aplicativo móvel de apoio à decisão na triagem de hemogramas, fundamentado nos valores de referência da PNS, e validar rigorosamente seu desempenho de extração de dados, acurácia de classificação e usabilidade percebida.

**Objetivos específicos:**

1. Consolidar e parametrizar a base de regras de classificação com base nos dados de Rosenfeld et al. (2019), considerando a estratificação por sexo e faixas etárias.
2. Desenvolver e portar a interface do sistema para aplicação móvel utilizando o *framework* React Native (Expo), consumindo a API existente em FastAPI.
3. **Frente A (validação da extração):** mensurar a precisão e o *recall* da extração automatizada de analitos a partir de uma base de laudos reais anonimizados estruturados sob o padrão de leiaute do Sistema Único de Saúde (SUS).
4. **Frente B (validação da classificação):** avaliar estatisticamente o índice de concordância entre os resultados gerados pelo sistema e a aplicação manual das tabelas da PNS, com foco em casos de borda.
5. **Frente C (avaliação de usabilidade):** aplicar a escala psicométrica padronizada SUS (*System Usability Scale*) com usuários finais para determinar a usabilidade percebida e a eficácia na conclusão de tarefas.

### 2.2. Justificativa

A relevância deste trabalho repousa em dois pilares centrais — a **precisão populacional** e a **inclusão em saúde pública** — desdobrados nos pontos a seguir:

1. **Relevância nacional / precisão populacional:** a adoção das faixas de referência da PNS (Rosenfeld et al., 2019), em detrimento de tabelas estrangeiras importadas, eleva de forma expressiva a validade clínica da triagem para o cidadão brasileiro.
2. **Equidade em saúde e impacto social:** ao restringir o *pipeline* de extração e a validação do aplicativo ao ecossistema de laudos da rede pública (padrão SUS), o projeto atende diretamente à parcela da população que mais depende da rede pública e que possui menor acesso a interpretação especializada — alinhando-se aos princípios de **universalidade e equidade** do SUS.
3. **Acesso e inclusão digital:** a entrega como aplicativo móvel amplia o alcance a usuários que acessam serviços de saúde majoritariamente pelo celular, contribuindo para a inclusão digital e para o letramento em saúde de populações vulneráveis.
4. **Lacuna metodológica:** o projeto de graduação entregou a ferramenta, mas **não a submeteu a validação formal**. Este TCC supre essa lacuna com avaliação quantitativa de extração e de classificação, além de avaliação de usabilidade.
5. **Reaproveitamento responsável:** consolida e valida cientificamente uma base já existente, em vez de partir do zero, transformando conhecimento técnico em um ativo compreensível ao paciente.

### 2.3. Escopo e Delimitação

**Inclusões:**
- Hemogramas de indivíduos **adultos** (faixa etária coberta pelo recorte da PNS);
- Classificação automatizada por faixas de referência parametrizadas;
- Entrega via **aplicativo móvel** (híbrido — React Native/Expo), além do PWA já existente;
- Validação em **tripla frente (A, B e C)**, aplicada restritamente a documentos emitidos no padrão SUS.

**Exclusões (delimitação / trabalhos futuros):**
- População **pediátrica**;
- Análise de **outros exames** laboratoriais fora do hemograma;
- Emissão de **diagnósticos clínicos** — a ferramenta atua estritamente como **triagem informativa**, não substituindo o parecer médico;
- Laudos da **rede privada** com leiautes proprietários divergentes do padrão SUS.

---

## 3. Problema de Pesquisa

> Um sistema de apoio à decisão para triagem de hemogramas, fundamentado nos valores de referência da PNS (Rosenfeld et al., 2019) e entregue como aplicativo móvel, é **confiável** quanto à extração automática dos valores e à classificação dos achados, e **usável** do ponto de vista do usuário final?

**Questões norteadoras:**

- **Q1 (extração):** qual a acurácia da extração automática de valores analíticos a partir de laudos estruturados sob o padrão de formatação e leiaute do SUS?
- **Q2 (classificação):** a classificação *normal/alto/baixo* do sistema é concordante com a aplicação direta das faixas da PNS, considerando estratos de sexo e idade?
- **Q3 (usabilidade):** qual o nível de usabilidade percebida do aplicativo móvel por usuários reais?

---

## 4. Fundamentação Teórica (eixos)

A revisão de literatura será organizada nos seguintes eixos:

1. **Hemograma e valores de referência populacionais:** interpretação dos analitos da série vermelha, série branca e plaquetas; o estudo da PNS (Rosenfeld et al., 2019) e o **método paramétrico** de estabelecimento de intervalos de referência; a importância da estratificação por sexo e idade.
2. **Sistemas de Apoio à Decisão Clínica (CDSS):** conceitos, taxonomias, benefícios e limites; o papel de ferramentas de triagem informativa e a fronteira ética com o diagnóstico.
3. **Extração de informação de documentos:** *parsing* de PDF, OCR (Tesseract) e pré-processamento de imagem; métricas de avaliação de extração (precisão, *recall*, F1).
4. **Desenvolvimento mobile e avaliação de usabilidade:** arquitetura híbrida (React Native/Expo) consumindo API REST; Engenharia de Software aplicada à saúde; avaliação de usabilidade pela *System Usability Scale* (SUS) e métricas de Interação Humano-Computador (IHC).
5. **Letramento e inclusão digital em saúde:** equidade, universalidade e o papel das tecnologias móveis no acesso à informação em saúde para populações vulneráveis.

---

## 5. Arquitetura e Componentes do Artefato

Esta seção detalha os componentes centrais do InterpreteLabBR que sustentam suas funções de apoio à decisão, em complemento à descrição metodológica da validação (Seção 6).

### 5.1. Base de conhecimento e modelos de dados

A base de conhecimento do sistema é composta por dois arquivos no formato CSV. O primeiro, `patterns.csv`, atua como um **dicionário de extração**: mapeia cada analito do hemograma (ex.: *hemoglobina*, *leucócitos*) a uma expressão regular (*regex*) específica, permitindo localizar e extrair os valores numéricos do leiaute do laudo do SUS em formato PDF. O segundo, `guideline_map.csv`, constitui o **núcleo do motor de regras**: funciona como uma tabela de decisão que implementa os valores de referência de Rosenfeld et al. (2019), definindo, para cada analito, as faixas de normalidade (limites inferior e superior) condicionadas ao sexo e à idade, além de vincular a(s) especialidade(s) médica(s) recomendada(s) em caso de alteração.

Para garantir a integridade e a padronização da comunicação entre *backend* e *frontend*, o sistema utiliza modelos de dados definidos com a biblioteca **Pydantic**. A classe `LabFinding` modela um "achado" individual, encapsulando o nome do analito, o valor extraído, a classificação do resultado (*Normal/Alto/Baixo*), a severidade e a especialidade associada. A classe `InterpretationResponse` representa a estrutura completa da resposta da API, agregando a lista de `LabFinding`, a lista consolidada de especialidades recomendadas e o texto explicativo destinado ao paciente.

### 5.2. Mecanismo de recomendação de especialidades

A recomendação de especialidades é obtida por um algoritmo de **votação ponderada por severidade**. Cada achado anormal "vota" nas especialidades a ele vinculadas no `guideline_map.csv`, somando sua severidade ao placar de cada especialidade; ao final, o sistema ordena as especialidades por placar e retorna as três mais pontuadas (com placar positivo).

Cabe registrar, em nome da transparência metodológica, que **na implementação atual a severidade de cada achado é fixada em valor unitário** (simplificação assumida), de modo que o ranqueamento opera, na prática, por **frequência de indicação** — prioriza-se a especialidade apontada pelo maior número de analitos alterados. A ponderação efetiva por magnitude do desvio (ex.: distância relativa ao limite de referência) constitui refinamento previsto (Seção 9). Ressalta-se, ainda, que o vínculo *analito → especialidade* é uma **associação clínica heurística parametrizada no projeto** — distinta dos valores de referência, estes derivados da PNS — cuja fundamentação será consolidada com base em literatura clínica e na orientação especializada `[confirmar fonte do mapeamento]`. Em coerência com o caráter descritivo adotado, a validação formal desta recomendação não integra as frentes A–C, sendo tratada como limitação e direção futura.

### 5.3. Geração do briefing ao paciente (NLG)

O texto explicativo entregue ao paciente é produzido por uma camada de **geração de linguagem natural (NLG)** organizada em uma **cascata com degradação graciosa**:

1. **Base curada:** o sistema mantém um repositório interno de explicações educativas, em linguagem acessível, para cada analito, redigidas e revisadas no âmbito do projeto;
2. **Composição do *prompt*:** os achados, as especialidades sugeridas e as explicações curadas são integrados em um *prompt* estruturado;
3. **Geração:** o *prompt* é submetido, prioritariamente, a um **modelo generativo (Google Gemini)** — empregado de forma **opcional**, condicionada à disponibilidade de credencial de API; havendo indisponibilidade, o sistema recorre, sucessivamente, a um modelo local (Ollama) e, por fim, a um **texto-modelo determinístico**, que assegura resposta segura mesmo sem qualquer LLM.

Esse arranjo evidencia uma decisão de projeto relevante para o domínio de saúde: **a lógica clinicamente sensível (classificação pela PNS e recomendação de especialidades) é integralmente determinística e baseada em regras**, ao passo que o modelo generativo atua exclusivamente na **camada de comunicação** (clareza, acolhimento e didatismo do texto), sem interferir na classificação. Como ressalvas a explicitar: (i) saídas de LLM são **não determinísticas** e sujeitas a imprecisões, mitigadas pelo *prompt* ancorado em conteúdo curado, pelo *fallback* determinístico e pelo aviso de que a ferramenta não substitui avaliação médica; e (ii) o uso do Gemini implica **transferência de dados a serviço de terceiros** (Google), aspecto a ser tratado sob a LGPD e refletido na política de privacidade do aplicativo. `[confirmar se a credencial Gemini está ativa em produção]`

---

## 6. Metodologia Proposta

Pesquisa **aplicada**, de natureza **quantitativa** (frentes A e B) e **quanti-qualitativa** (frente C), fundamentada na abordagem metodológica da **Design Science Research (DSR)** para o desenvolvimento e a avaliação do artefato.

### 6.1. Materiais e Ferramentas

- **Base de regras:** faixas da PNS (Rosenfeld et al., 2019) pré-estruturadas em formato tabular (já materializadas nos arquivos de configuração do projeto, `data/`).
- **Massa de testes:** **20 a 30 laudos reais anonimizados** (contendo apenas valores laboratoriais, com omissão de dados pessoais), coletados de emissões do ecossistema público de saúde (SUS). A padronização em um único leiaute (SUS) confere maior controle metodológico à validação da extração.
- **Stack tecnológica:** *backend* em Python (FastAPI); aplicativo móvel em React Native com Expo; *pipeline* de processamento e OCR baseado em bibliotecas abertas (ex.: Tesseract, PyMuPDF/pdfplumber); geração de linguagem natural por modelo generativo (Google Gemini), de uso opcional, com *fallbacks* local (Ollama) e determinístico.

### 6.2. Protocolo das Frentes de Validação

**Frente A — Extração.** Os valores extraídos pelo algoritmo automatizado serão confrontados com um **gabarito elaborado manualmente** por inspeção visual. Serão calculadas as métricas de **Precisão, Recall e F1-Score**, por analito e agregadas, mapeando potenciais fragilidades induzidas por ruídos de impressão comuns nos laudos do SUS e pelo OCR.

**Frente B — Classificação.** Aplicação das regras epidemiológicas da PNS de forma **manual** sobre a base de analitos extraídos (incluindo **dados sintéticos** para simulação de casos de borda). O índice de **concordância** do motor de regras será medido estatisticamente (ex.: percentual de concordância e/ou coeficiente *kappa* de Cohen), com atenção especial aos estratos sexo × idade e aos valores próximos aos limites.

**Frente C — Usabilidade.** Teste de usabilidade direcionado a uma **amostra por conveniência** de usuários finais. Os participantes executarão tarefas de rotina no aplicativo (submissão de laudo e leitura do *briefing* interpretativo) e responderão ao questionário psicométrico padronizado **System Usability Scale (SUS)** para aferição do escore global de satisfação, complementado por coleta de *feedback* qualitativo. Serão reportados o escore SUS médio (escala 0–100) e os principais achados qualitativos.

### 6.3. Aspectos Éticos

Garantia de **total anonimização** de dados de terceiros, em estrita conformidade com a **Lei Geral de Proteção de Dados (LGPD)**, e obtenção de **consentimento informado** dos participantes da etapa de usabilidade. A necessidade de submissão do teste de usabilidade à **Plataforma Brasil / Comitê de Ética em Pesquisa (CEP)** será avaliada conjuntamente com o(a) professor(a) orientador(a).

Atenção adicional recai sobre o componente de NLG (Seção 5.3): quando o modelo generativo (Gemini) está ativo, há **transferência de dados a serviço de terceiros**, o que demanda base legal, minimização de dados e transparência (política de privacidade) sob a LGPD; o *fallback* determinístico permite, quando requerido, operar **sem qualquer envio externo**.

---

## 7. Resultados Esperados

- **Aplicativo móvel funcional**, fundamentado na referência brasileira (PNS), em continuidade ao PWA existente.
- **Relatório quantitativo** de acurácia de extração (Precisão/Recall/F1) e de concordância de classificação (kappa / % de acerto).
- **Escore de usabilidade (SUS)** com usuários reais e recomendações de melhoria de interface e experiência.
- **Identificação de limitações** do sistema e definição de direções para trabalhos futuros.

---

## 8. Cronograma (sugestão — ajustar à duração do curso)

| Etapa | Atividades | Período |
|---|---|---|
| 1 | Revisão bibliográfica; consolidação da fundamentação teórica (PNS, CDSS, OCR, usabilidade) | Meses 1–2 |
| 2 | Coleta e anonimização de laudos; elaboração dos gabaritos de extração | Meses 2–3 |
| 3 | Port/evolução para o aplicativo móvel; ajustes na API | Meses 3–4 |
| 4 | Execução da Frente A (extração) e da Frente B (classificação) | Meses 4–5 |
| 5 | Execução da Frente C (usabilidade) | Mês 5 |
| 6 | Análise dos resultados; redação; revisão final e entrega | Meses 6–7 |

---

## 9. Trabalhos Futuros

Com a disponibilidade de uma **base rotulada de hemogramas reais**, propõe-se uma camada de **aprendizado de máquina** para (i) reconhecimento de padrões multi-analito (ex.: classificação de tipos de anemia) e (ii) maior robustez a extrações incompletas ou ruidosas do OCR, sempre tendo os valores de referência da PNS como **padrão-ouro de rotulagem** — evoluindo o sistema de uma arquitetura **baseada em regras** para uma abordagem **híbrida (regras + ML)**. Prevê-se, ademais, (iii) a **ponderação efetiva da severidade** dos achados (hoje simplificada) na recomendação de especialidades e (iv) a **avaliação sistemática da qualidade e segurança** dos textos gerados pelo LLM (precisão factual, ausência de alucinações e adequação da linguagem). Outras direções incluem a extensão a leiautes da rede privada e à população pediátrica.

---

## 10. Referências

BROOKE, John. SUS: a 'quick and dirty' usability scale. In: JORDAN, P. W. et al. (Eds.). **Usability Evaluation in Industry**. London: Taylor & Francis, 1996. p. 189–194.

HEVNER, Alan R.; MARCH, Salvatore T.; PARK, Jinsoo; RAM, Sudha. Design science in information systems research. **MIS Quarterly**, v. 28, n. 1, p. 75–105, 2004.

ROSENFELD, Luiz Gastão et al. Valores de referência para exames laboratoriais de hemograma da população adulta brasileira: Pesquisa Nacional de Saúde. **Revista Brasileira de Epidemiologia**, v. 22, supl. 2, art. e190003, 2019. DOI: <https://doi.org/10.1590/1980-549720190003.supl.2>.

> _Referências preliminares — a serem ampliadas e ajustadas ao estilo exigido (ABNT/instituição) em conjunto com o(a) orientador(a), incluindo fontes dos eixos de CDSS, OCR e LGPD._
