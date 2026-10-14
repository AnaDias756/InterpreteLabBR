# E-mail ao orientador — Etapa 4 (rascunho)

**Para:** Prof. Diogo S. Martins
**Assunto:** Entrega da Etapa 4 — InterpreteLabBR (atualizações desde a última reunião)

---

Prezado Professor Diogo,

Conforme solicitado, segue o acompanhamento assíncrono da Etapa 4. A versão mais
recente da monografia está no meu Google Drive, indicada no nome do arquivo como
Etapa 4: **[inserir link do arquivo no Drive]**.

Abaixo, um resumo das atualizações realizadas desde a última reunião:

**1. Consolidação das três frentes de avaliação.** O capítulo de Resultados foi
estruturado em torno das frentes do artigo: A (desempenho), B (engenharia da
migração) e C (usabilidade por inspeção heurística).

**2. Frente B — Engenharia da migração (concluída, com resultados reais).**
Caracterizei, por análise documental comparativa das duas bases de código, o
reuso arquitetural viabilizado pela estratégia *API-first*:
- reuso integral (100%) de toda a lógica clínica do *backend* (1.654 linhas de
  Python + 145 linhas de regras), consumida pelos mesmos *endpoints* REST, sem
  reescrita;
- esforço de migração confinado à camada de apresentação (portabilidade
  estrutural), com substituições nativas restritas aos pontos de *hardware*;
- eliminação de 1.239 linhas de código de contorno de *webview* (49% do cliente
  web), tornadas desnecessárias pela renderização nativa — correlato, no plano do
  código, do *overhead* apontado por Oliveira et al. (2023).

**3. Frente A — Desempenho (instrumentação pronta).** Elaborei o protocolo
experimental de medição via ADB (tarefas, 10 repetições, controle de variáveis e
comandos de coleta de tempo, CPU, RAM, FPS e energia), além dos scripts de coleta
e de análise estatística. As medições em dispositivo físico estão previstas para
a próxima etapa.

**4. Frente C — Usabilidade (instrumentação pronta).** Elaborei o protocolo de
inspeção heurística de Nielsen (cinco especialistas, dez heurísticas, escala de
severidade 0–4, formulários e consolidação). A aplicação com os especialistas
está prevista para a próxima etapa.

**5. Reprodutibilidade.** Toda a apuração (tabelas e figuras) é regenerável por
*scripts*, e o material está versionado no repositório do projeto.

**Pontos em que agradeço orientação:**
- adequação do recorte da Etapa 4 (Frente B concluída; A e C com instrumentos
  validados e coleta prevista);
- se devo ajustar a redação da metodologia da Frente B de "diário de bordo" para
  "análise documental comparativa", refletindo o procedimento efetivamente
  adotado.

Fico no aguardo do seu retorno e agradeço desde já pelo acompanhamento.

Atenciosamente,
**[Seu nome]**
`[curso/matrícula, se aplicável]`
