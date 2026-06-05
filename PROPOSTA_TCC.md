# Proposta de Trabalho de Conclusão de Curso (Pós-Graduação)

> Documento de escopo para alinhamento com o(a) orientador(a). Versão inicial — sujeito a refinamento.

## Título provisório

**Aplicativo móvel de apoio à decisão para triagem de hemogramas fundamentado em valores de referência da população adulta brasileira (PNS): validação da extração, da classificação e da usabilidade.**

## Identificação

- **Área/Temas (da lista do curso):** Sistemas de Apoio à Decisão; Aplicativos para plataformas móveis; Processamento e análise de imagens; Inteligência Artificial aplicada à Saúde (camada futura).
- **Natureza:** Desenvolvimento de ferramenta computacional aplicada + estudo de validação.
- **Base de continuidade:** Evolução do projeto **InterpreteLabBR** (PWA desenvolvido na graduação) para aplicativo móvel, com adição de um eixo científico de validação.

---

## 1. Contextualização

O hemograma é um dos exames laboratoriais mais solicitados no Brasil, mas sua interpretação por leigos é difícil e os valores de referência frequentemente impressos nos laudos derivam de populações estrangeiras. O projeto **InterpreteLabBR** já implementa um pipeline que extrai valores de laudos em PDF (via parsing de texto e OCR), classifica cada analito como *normal/alto/baixo* segundo faixas de referência e gera um briefing educativo ao paciente, sugerindo especialidades.

O núcleo científico das classificações é o estudo:

> ROSENFELD, Luiz Gastão et al. **Valores de referência para exames laboratoriais de hemograma da população adulta brasileira: Pesquisa Nacional de Saúde.** Revista Brasileira de Epidemiologia, v. 22, supl. 2, art. e190003, 2019. DOI: 10.1590/1980-549720190003.supl.2.

Trata-se, até o momento, do **único estudo que estabeleceu valores de referência de hemograma para adultos brasileiros pelo método paramétrico, com dados da Pesquisa Nacional de Saúde (PNS)** — o que confere ao sistema uma fundamentação populacional adequada à realidade nacional, diferencial ausente na maioria das ferramentas similares.

## 2. Justificativa

1. **Relevância nacional:** adoção de referência brasileira (PNS) em vez de faixas importadas, aumentando a validade das classificações para a população-alvo.
2. **Acesso e inclusão:** entrega como aplicativo móvel amplia o alcance a usuários que acessam serviços de saúde majoritariamente pelo celular.
3. **Lacuna metodológica:** o projeto de graduação entregou a ferramenta, mas **não submeteu o sistema a validação formal**. Este TCC supre essa lacuna com avaliação quantitativa de extração e de classificação, além de avaliação de usabilidade.
4. **Reaproveitamento responsável:** consolida e valida cientificamente uma base já existente, em vez de partir do zero.

## 3. Problema de pesquisa

> Um sistema de apoio à decisão para triagem de hemogramas, fundamentado nos valores de referência da PNS (Rosenfeld et al., 2019) e entregue como aplicativo móvel, é **confiável** quanto à extração automática dos valores e à classificação dos achados, e **usável** do ponto de vista do usuário final?

### Hipóteses / questões norteadoras
- **Q1 (extração):** qual a acurácia da extração automática de valores a partir de laudos em diferentes formatos de laboratório?
- **Q2 (classificação):** a classificação *normal/alto/baixo* do sistema é concordante com a aplicação direta das faixas da PNS, considerando estratos de sexo e idade?
- **Q3 (usabilidade):** qual o nível de usabilidade percebida do aplicativo móvel por usuários reais?

## 4. Objetivos

### Objetivo geral
Evoluir o InterpreteLabBR para um aplicativo móvel de apoio à decisão na triagem de hemogramas, fundamentado nos valores de referência da população adulta brasileira (PNS), e **validar** seu desempenho de extração, de classificação e de usabilidade.

### Objetivos específicos
1. Consolidar a base de regras de classificação a partir dos valores de referência de Rosenfeld et al. (2019), documentando estratificação por sexo e faixa etária.
2. Desenvolver/portar a interface para aplicativo móvel (ex.: React Native/Expo), consumindo a API existente (FastAPI).
3. **Frente A — Validação da extração:** medir precisão e recall da extração automática de analitos em um conjunto de laudos de formatos variados.
4. **Frente B — Validação da classificação:** avaliar a concordância entre a saída do sistema e a aplicação manual das faixas da PNS, incluindo casos de borda.
5. **Frente C — Avaliação de usabilidade:** aplicar instrumento padronizado (ex.: SUS — System Usability Scale) com usuários, mensurando usabilidade percebida e taxa de conclusão de tarefas.

## 5. Fundamentação teórica (eixos)

- Hemograma e valores de referência populacionais; o estudo PNS (Rosenfeld et al., 2019) e o método paramétrico.
- Sistemas de Apoio à Decisão Clínica (CDSS): conceitos, benefícios e limites.
- Extração de informação de documentos: parsing de PDF, OCR (Tesseract) e pré-processamento de imagem.
- Desenvolvimento mobile e avaliação de usabilidade (SUS; métricas de IHC).

## 6. Metodologia

Pesquisa **aplicada**, de natureza **quantitativa** (frentes A e B) e **quanti-qualitativa** (frente C), com desenvolvimento de artefato (método de pesquisa: *Design Science Research*, opcional como enquadramento).

### 6.1 Materiais
- Base de referência: faixas da PNS (Rosenfeld et al., 2019), já estruturadas em `data/guideline_map.csv`.
- Conjunto de laudos de teste: laudos reais **anonimizados** (sem dados pessoais — apenas valores) de diferentes laboratórios e/ou variações geradas; meta de **20–30 laudos** de formatos diversos.
- Stack: backend FastAPI existente; app móvel (React Native/Expo); pipeline de OCR (Tesseract/PyMuPDF) existente.

### 6.2 Frente A — Validação da extração
Para cada laudo, comparar os valores extraídos automaticamente com um **gabarito conferido manualmente**. Métricas por analito e agregadas: **precisão, recall, F1** de extração; taxa de erro por formato de laudo. Análise de falhas (analitos mais problemáticos, impacto do OCR).

### 6.3 Frente B — Validação da classificação
Aplicar as faixas da PNS manualmente a um conjunto de valores (reais e sintéticos de borda) e comparar com a classificação do sistema. Métrica de **concordância** (ex.: % de acerto e/ou kappa), com atenção a estratos sexo × idade e a valores próximos aos limites.

### 6.4 Frente C — Avaliação de usabilidade
Teste de usabilidade com usuários (amostra por conveniência), execução de tarefas típicas (enviar laudo, interpretar resultado), aplicação do **SUS** e coleta de feedback qualitativo. Reportar escore SUS médio e principais achados.

### 6.5 Aspectos éticos
Uso de dados **anonimizados** e consentimento informado para a etapa de usabilidade, em conformidade com a LGPD. Avaliar necessidade de submissão a Comitê de Ética conforme orientação do(a) orientador(a).

## 7. Resultados esperados

- Aplicativo móvel funcional, fundamentado na referência brasileira (PNS).
- Relatório quantitativo de **acurácia de extração** e de **concordância de classificação**.
- **Escore de usabilidade (SUS)** e recomendações de melhoria.
- Identificação de limitações e direções para trabalhos futuros.

## 8. Cronograma (sugestão — ajustar à duração do curso)

| Etapa | Atividades | Período |
|---|---|---|
| 1 | Revisão bibliográfica; consolidação da fundamentação (PNS, CDSS, OCR, SUS) | Meses 1–2 |
| 2 | Coleta/anonimização de laudos; definição de gabaritos | Meses 2–3 |
| 3 | Port para app móvel; ajustes na API | Meses 3–4 |
| 4 | Frente A (extração) e Frente B (classificação) | Meses 4–5 |
| 5 | Frente C (usabilidade) | Mês 5 |
| 6 | Análise de resultados; escrita; revisão final | Meses 6–7 |

## 9. Delimitação do escopo

- **Inclui:** hemograma de **adultos** (faixa etária coberta pela PNS); classificação por faixas de referência; app móvel; validação A/B/C.
- **Não inclui (trabalhos futuros):** população pediátrica; outros exames; diagnóstico (a ferramenta é de **apoio/triagem**, não substitui avaliação médica).

## 10. Trabalhos futuros

Com a disponibilidade de uma **base rotulada de hemogramas reais**, propõe-se uma camada de **aprendizado de máquina** para (i) reconhecimento de padrões multi-analito (ex.: tipos de anemia) e (ii) robustez a extrações incompletas/ruidosas do OCR, sempre tendo os valores de referência da PNS como padrão-ouro de rotulagem — evoluindo o sistema de baseado em regras para **híbrido (regras + ML)**.

## Referências

ROSENFELD, Luiz Gastão et al. Valores de referência para exames laboratoriais de hemograma da população adulta brasileira: Pesquisa Nacional de Saúde. **Revista Brasileira de Epidemiologia**, v. 22, supl. 2, art. e190003, 2019. DOI: https://doi.org/10.1590/1980-549720190003.supl.2.
