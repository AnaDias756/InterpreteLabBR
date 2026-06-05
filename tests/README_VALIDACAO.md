# Validação da Extração (Frente A do TCC)

Este diretório contém o instrumento de avaliação da **acurácia da extração**
automática de valores de hemograma a partir de laudos em PDF.

## Como executar

```bash
# Roda sobre o exemplo sintético (sem dados pessoais)
python tests/validacao_extracao.py

# Roda sobre seus próprios laudos (anonimizados), salvando um relatório CSV
python tests/validacao_extracao.py \
    --gabarito tests/meu_gabarito.json \
    --laudos tests/laudos \
    --relatorio relatorio_extracao.csv
```

## Como adicionar seus laudos do SUS

1. Coloque os PDFs **anonimizados** (sem nome, CPF, Cód.SUS, endereço, nome da
   mãe) na pasta `tests/laudos/` — essa pasta é **ignorada pelo Git** por
   privacidade (LGPD).
2. Crie um gabarito JSON conferido manualmente, no formato:

```json
{
  "laudo01.pdf": {
    "hemacias": 4.69, "hemoglobina": 14.6, "hematocrito": 42.9,
    "vcm": 91.5, "hcm": 31.1, "chcm": 34.0, "rdw": 11.8,
    "leucocitos": 3100, "neutrofilos": 1073, "eosinofilos": 22,
    "basofilos": 6, "linfocitos": 1798, "monocitos": 202,
    "plaquetas": 116000
  }
}
```

3. Rode o harness apontando para a pasta e o gabarito.

## O que o harness mede

- **Acurácia de extração** (corretos / esperados), por laudo e agregada.
- **Precisão, Recall e F1** (tratando a extração correta como verdadeiro positivo).
- **Ausentes** (analito não extraído), **Incorretos** (valor errado) e
  **Falsos positivos** (extraído sem constar no gabarito).
- **Desempenho por analito**, para identificar os mais problemáticos.

Esses números alimentam diretamente o capítulo de Resultados do TCC.
