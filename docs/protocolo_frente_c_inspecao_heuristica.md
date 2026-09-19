# Protocolo de Coleta — Frente C: Inspeção Heurística de Usabilidade

**Projeto:** InterpreteLabBR — Migração PWA → Aplicativo Móvel
**Método:** Avaliação Heurística de Nielsen (inspeção por especialistas)
**Objetivo:** Comparar a usabilidade do cliente **PWA** (web) e do cliente
**móvel** (React Native/Expo) sobre os mesmos cenários de uso, identificando e
classificando violações às heurísticas de usabilidade.

> Este é o **instrumento de coleta** a ser entregue a cada avaliador. Ao final,
> os relatórios individuais são consolidados pelo pesquisador (Seção 8).

---

## 1. Enquadramento metodológico

A Avaliação Heurística (Nielsen, 1994) é um método de inspeção em que
especialistas — e **não** usuários finais — examinam a interface à luz de um
conjunto consagrado de princípios (as 10 heurísticas), registrando problemas e
atribuindo-lhes uma severidade. Por dispensar a participação de usuários, o
método **não requer submissão a Comitê de Ética em Pesquisa (CEP)** e adequa-se
ao horizonte temporal de um TCC (Cardieri & Zaina, 2018).

- **Número de avaliadores:** 5 especialistas com formação/experiência em
  Interação Humano-Computador (IHC). Nielsen (1994) demonstra que 3–5
  avaliadores identificam a expressiva maioria dos problemas de usabilidade;
  adota-se o limite superior (5) para maximizar a cobertura.
- **Independência:** cada avaliador realiza a inspeção **sozinho**, sem
  consultar os demais. A consolidação ocorre somente após todas as inspeções
  individuais.
- **Cobertura dupla:** cada avaliador inspeciona os **dois clientes** (PWA e
  móvel) sobre os **mesmos cenários**, para permitir a comparação.

---

## 2. Objeto de avaliação

| Cliente | Como acessar |
|---|---|
| **PWA (web)** | `[inserir URL do PWA]` — abrir no navegador do dispositivo indicado |
| **Móvel (app)** | `[inserir link/APK ou Expo Go]` — instalar no dispositivo Android indicado |

> Ambos consomem a mesma API; as diferenças observadas devem-se à camada de
> apresentação e ao paradigma de execução.

---

## 3. Cenários de uso (tarefas)

Execute **cada cenário nos dois clientes**. São tarefas reais do sistema.

- **C1 — Acesso e status:** abrir a aplicação e identificar se o servidor está
  disponível (status online/offline).
- **C2 — Interpretação por entrada manual:** selecionar o modo de digitação,
  informar sexo e idade, digitar ao menos 3 valores de hemograma, solicitar a
  análise e **ler o briefing** e as especialidades sugeridas.
- **C3 — Interpretação por PDF:** selecionar o modo de envio de PDF, anexar um
  laudo (arquivo de teste fornecido), solicitar a análise e ler o resultado.
- **C4 — Comparação de referências:** localizar e interpretar a tabela que
  compara a classificação pela **PNS** e pela **referência do laudo**,
  identificando um analito divergente.
- **C5 — Recuperação de erro:** provocar um erro previsível (ex.: analisar sem
  informar a idade, ou enviar um arquivo que não é PDF) e avaliar a mensagem e a
  recuperação.

> **Material de apoio:** use o laudo sintético de teste do projeto
> (`generate_sample_pdf.py`) para C3, evitando qualquer dado pessoal real.

---

## 4. As 10 heurísticas de Nielsen

| # | Heurística | Descrição resumida |
|---|---|---|
| H1 | Visibilidade do estado do sistema | O sistema informa o que está acontecendo (feedback, carregamento, status). |
| H2 | Correspondência com o mundo real | Linguagem e conceitos familiares ao usuário; termos não técnicos quando possível. |
| H3 | Controle e liberdade do usuário | Saídas claras, desfazer/refazer, cancelar operações. |
| H4 | Consistência e padrões | Mesmos termos e ações significam a mesma coisa; segue convenções da plataforma. |
| H5 | Prevenção de erros | O design evita que o erro aconteça (validação, confirmação). |
| H6 | Reconhecimento em vez de memorização | Opções e informações visíveis; não exige lembrar dados entre telas. |
| H7 | Flexibilidade e eficiência de uso | Atalhos e caminhos eficientes para diferentes níveis de usuário. |
| H8 | Estética e design minimalista | Sem informação irrelevante competindo com o essencial. |
| H9 | Reconhecer, diagnosticar e recuperar-se de erros | Mensagens em linguagem clara, indicando o problema e a solução. |
| H10 | Ajuda e documentação | Ajuda acessível quando necessária, focada na tarefa do usuário. |

---

## 5. Escala de severidade (Nielsen, 0–4)

| Grau | Significado |
|---|---|
| **0** | Não é um problema de usabilidade. |
| **1** | Problema **cosmético** — corrigir apenas se houver tempo. |
| **2** | Problema **menor** — baixa prioridade de correção. |
| **3** | Problema **maior** — alta prioridade; importante corrigir. |
| **4** | **Catastrófico** — imperativo corrigir antes de disponibilizar. |

---

## 6. Procedimento para o avaliador

1. Percorra livremente cada cliente uma primeira vez, familiarizando-se.
2. Execute os cenários C1–C5 **em cada cliente**, com atenção às 10 heurísticas.
3. A cada violação percebida, registre **uma linha** no formulário (Seção 7):
   heurística violada, tela/local, descrição do problema, severidade e o cliente
   (PWA ou Móvel).
4. Um mesmo problema pode violar mais de uma heurística — registre a
   predominante e cite as demais na descrição.
5. Seja específico: descreva **onde** e **por que** é um problema, e o **impacto**
   sobre o usuário.

---

## 7. Formulário individual de registro

**Avaliador:** `[identificador anonimizado, ex.: A1]` · **Formação/experiência
em IHC:** `[breve]` · **Data:** `[__/__/____]`

| ID | Cliente (PWA/Móvel) | Cenário (C1–C5) | Tela / Local | Heurística(s) | Descrição do problema | Severidade (0–4) | Recomendação |
|----|---------------------|-----------------|--------------|---------------|------------------------|------------------|--------------|
| 01 |  |  |  |  |  |  |  |
| 02 |  |  |  |  |  |  |  |
| 03 |  |  |  |  |  |  |  |
| 04 |  |  |  |  |  |  |  |
| 05 |  |  |  |  |  |  |  |
| … |  |  |  |  |  |  |  |

> Adicione quantas linhas forem necessárias.

---

## 8. Consolidação (pesquisador)

Após reunir os 5 formulários, consolide em um inventário único e calcule as
métricas comparativas entre os clientes:

- **Número de problemas únicos** por cliente (mesclar duplicatas relatadas por
  avaliadores diferentes).
- **Densidade de problemas** = total de problemas únicos por cliente.
- **Índice médio de severidade** por cliente = média das severidades atribuídas.
- **Distribuição por heurística** (quais heurísticas concentram mais violações).
- **Distribuição por severidade** (quantos problemas de grau 3–4 em cada cliente).
- **Taxa de detecção por avaliador** (quantos dos problemas únicos cada avaliador
  encontrou) — indicador de suficiência do painel.

Para agilizar, use a planilha `tests/inspecao_heuristica_modelo.csv` (mesma
estrutura do formulário) e consolide todos os avaliadores em um único arquivo;
o script `tests/consolidar_inspecao.py` gera as métricas acima e as figuras.

**Tabela-síntese a preencher no capítulo de Resultados:**

| Métrica | PWA | Móvel |
|---|---|---|
| Problemas únicos | `[PENDENTE]` | `[PENDENTE]` |
| Índice médio de severidade | `[PENDENTE]` | `[PENDENTE]` |
| Problemas de severidade 3–4 | `[PENDENTE]` | `[PENDENTE]` |

---

## 9. Termo de concordância do avaliador especialista

> Eu, `[nome]`, na condição de especialista em IHC/usabilidade, concordo em
> participar da inspeção heurística do projeto InterpreteLabBR, de caráter
> acadêmico. Entendo que **não** serão coletados dados pessoais sensíveis, que
> minha identidade será **anonimizada** (identificador do tipo A1–A5) na análise
> e na publicação, e que meus registros serão usados exclusivamente para fins de
> pesquisa deste Trabalho de Conclusão de Curso.
>
> Assinatura: ____________________________  Data: __/__/____

---

## 10. Referências

- NIELSEN, J. **Usability Engineering**. San Francisco: Morgan Kaufmann, 1994.
- NIELSEN, J. **10 Usability Heuristics for User Interface Design**. Nielsen
  Norman Group, 1994. `[confirmar formato de citação exigido]`
- CARDIERI, G. A.; ZAINA, L. A. M. Analyzing the User Experience in Mobile Web,
  Native and Progressive Web Applications: a User and HCI Specialist
  Perspectives. In: **IHC 2018 (XVII Simpósio Brasileiro sobre Fatores Humanos em
  Sistemas Computacionais)**. `[confirmar dados no padrão ABNT/SBC]`
