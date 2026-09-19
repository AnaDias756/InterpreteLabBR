# Validação e Resultados (Etapa 4 do TCC)

Este diretório reúne os instrumentos de validação das três frentes do TCC e a
tubulação que gera as tabelas, estatísticas e figuras do capítulo de Resultados
(`../RESULTADOS.md`).

## Visão geral da tubulação

| Frente | Script | Natureza dos dados | Saída |
|---|---|---|---|
| **A — Extração** | `validacao_extracao.py` | laudos reais (pendente) / exemplo sintético | acurácia, precisão, recall, F1 |
| **B — Classificação** | `validacao_classificacao.py` | sintético (casos de borda) | concordância %, kappa, matriz de confusão |
| **PNS × estrangeira** | `comparacao_referencias.py` | analítico (tabelas) | discordância por analito, kappa |
| **C — Usabilidade** | `pontuacao_sus.py` | respostas reais (pendente) / exemplo sintético | escore SUS, DP, classificação |
| **Figuras** | `gerar_graficos.py` | lê `saidas/` | PNG em `../docs/figuras/` |
| **Orquestrador** | `gerar_resultados.py` | — | roda tudo de ponta a ponta |

## Como rodar tudo

```bash
pip install pandas numpy matplotlib pdfplumber PyMuPDF PyPDF2 reportlab

# Demonstração completa (A e C sobre exemplos sintéticos; B e PNS×Lab reais)
python tests/gerar_resultados.py

# Com dados reais, quando disponíveis:
python tests/gerar_resultados.py \
    --laudos tests/laudos --gabarito tests/meu_gabarito.json \
    --respostas-sus tests/respostas_sus.csv
```

As saídas intermediárias vão para `tests/saidas/` (ignorado pelo Git; é
regenerável) e as figuras para `docs/figuras/` (versionadas).

## Frente A — inserir laudos reais (LGPD)

1. Coloque os PDFs **anonimizados** (sem nome, CPF, Cód.SUS, endereço, nome da
   mãe) em `tests/laudos/` — pasta **ignorada pelo Git**.
2. Crie um gabarito JSON conferido manualmente (veja `gabarito_exemplo.json`),
   mapeando cada arquivo aos valores verdadeiros dos analitos.
3. Rode com `--laudos tests/laudos --gabarito tests/meu_gabarito.json`.

## Frente C — coletar respostas SUS (LGPD)

1. Aplique o questionário SUS (10 itens, escala 1–5) aos participantes.
2. Preencha `tests/respostas_sus.csv` a partir do modelo
   `respostas_sus_modelo.csv` (use identificadores anonimizados: P01, P02, …).
   Esse arquivo de respostas reais é **ignorado pelo Git**.
3. Rode com `--respostas-sus tests/respostas_sus.csv`.

> `respostas_sus_exemplo.csv` contém dados **fictícios** apenas para demonstrar
> a apuração — não são respostas de usuários reais.

## O que é real agora × o que depende de coleta

- **Real e determinístico:** Frente B (motor × PNS) e comparação PNS ×
  referência estrangeira — não dependem de dados coletados.
- **Pendente de coleta empírica:** Frente A (laudos reais) e Frente C (usuários).
  Os instrumentos já estão prontos e validados sobre exemplos sintéticos.
