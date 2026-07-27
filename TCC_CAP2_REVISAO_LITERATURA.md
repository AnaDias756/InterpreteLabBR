# 2 REVISÃO DE LITERATURA

---

## 2.1 Sistemas de Apoio à Decisão Clínica na Saúde Digital Brasileira

Os Sistemas de Apoio à Decisão Clínica (*Clinical Decision Support Systems* — CDSS) são ferramentas computacionais projetadas para auxiliar profissionais de saúde e pacientes no processo de tomada de decisão, fornecendo informações baseadas em evidências em contextos clínicos específicos. De acordo com a literatura, essas ferramentas integram dados do paciente com bases de conhecimento estruturadas para gerar recomendações, alertas ou interpretações que auxiliam na triagem e no diagnóstico (BAUERMANN et al., 2024).

No contexto brasileiro, a saúde digital tem sido avaliada por iniciativas como o *Brazilian Digital Health Index* (BDHI), instrumento desenvolvido para mensurar o nível de maturidade da saúde digital no país. Cruz et al. (2022) demonstram que o Brasil apresenta avanços significativos em alguns eixos — como conectividade e infraestrutura —, mas ainda enfrenta lacunas expressivas no eixo de cidadania e inclusão, que abrange o acesso da população a ferramentas digitais de saúde. Esse diagnóstico evidencia a necessidade de soluções que priorizem a acessibilidade e a inclusão digital como critério de projeto, e não apenas como efeito secundário.

No campo dos CDSS aplicados à saúde pública brasileira, destaca-se o trabalho de Bauermann et al. (2024), que desenvolveram um sistema de apoio à decisão clínica voltado a cuidadores de pacientes pediátricos hemofílicos. Esse trabalho exemplifica como sistemas computacionais podem ser projetados para mediar o conhecimento clínico especializado e o leigo, reduzindo barreiras de interpretação para familiares e cuidadores sem formação na área da saúde — desafio análogo ao do InterpreteLabBR, que busca traduzir resultados laboratoriais de hemogramas para o paciente comum do SUS.

A relevância de soluções móveis nesse contexto é reforçada por Torrente et al. (2024), que analisam a relação entre tecnologia e atendimento pré-hospitalar móvel, evidenciando que a adoção de aplicativos instaláveis no contexto de saúde pública contribui para a agilidade e a qualidade do atendimento. A disponibilização de sistemas de saúde em plataformas móveis instaláveis configura, portanto, não apenas uma decisão técnica, mas uma estratégia de alcance e equidade no acesso à informação clínica.

---

## 2.2 Hemograma e Valores de Referência Populacionais Brasileiros

O hemograma é um dos exames laboratoriais mais solicitados na rotina clínica do Sistema Único de Saúde (SUS), permitindo a avaliação de componentes do sangue como eritrócitos, leucócitos e plaquetas. Apesar de sua ampla utilização, a interpretação dos resultados por pacientes leigos é frequentemente dificultada pela ausência de contextualização adequada nos laudos e, sobretudo, pelo fato de que os valores de referência impressos na maioria dos laudos brasileiros derivam de estudos populacionais estrangeiros, que não refletem as especificidades demográficas, nutricionais e epidemiológicas da população brasileira.

Essa lacuna foi endereçada de forma expressiva pela Pesquisa Nacional de Saúde (PNS), cujos resultados para exames laboratoriais de hemograma foram publicados por Rosenfeld et al. (2019). O estudo, de abrangência nacional, estabeleceu valores de referência para a população adulta brasileira estratificados por sexo e faixa etária, constituindo o primeiro levantamento paramétrico de grande escala conduzido com amostra representativa do Brasil. A adoção desses parâmetros como base classificatória confere ao InterpreteLabBR validade epidemiológica superior às ferramentas que utilizam tabelas de referência importadas, tornando-o mais adequado à realidade do sistema público de saúde nacional.

A importância de se utilizar valores de referência populacionalmente ajustados reside no fato de que a classificação equivocada de um analito como anormal — ou, inversamente, a não detecção de um valor limítrofe — pode gerar ansiedade desnecessária no paciente ou, em casos mais graves, retardar a busca por atendimento médico. A fundamentação do sistema na PNS representa, portanto, um diferencial de segurança e de relevância clínica para a população usuária do SUS, público-alvo primário do projeto.

---

## 2.3 *Progressive Web Apps*: Características e Limitações

As *Progressive Web Apps* (PWAs) constituem uma abordagem de desenvolvimento de software que busca combinar as vantagens das aplicações web — acessibilidade via navegador, sem necessidade de instalação — com características típicas de aplicativos nativos, como comportamento responsivo, suporte a notificações e capacidade de funcionamento *offline* por meio de *Service Workers*. A proposta das PWAs é reduzir a fricção de acesso ao usuário, permitindo que uma aplicação seja utilizada diretamente por uma URL, sem as etapas de instalação em lojas de aplicativos.

No contexto do InterpreteLabBR, a escolha inicial pela arquitetura PWA justificou-se pela praticidade de distribuição e pela dispensa de contas em plataformas como Google Play ou App Store. No entanto, essa abordagem impõe restrições estruturais que limitam o desempenho e a experiência do usuário. As PWAs executam sobre o motor de renderização do navegador (*web view*), o que introduz uma camada de abstração entre o código da aplicação e os componentes nativos do sistema operacional. Essa camada adicional implica *overhead* de processamento, especialmente em operações que demandam alta responsividade de interface, como rolagem de listas extensas, animações ou interações rápidas com o teclado.

Adicionalmente, PWAs enfrentam limitações de integração com recursos de *hardware* do dispositivo — como acesso ao sistema de arquivos, câmera e sensores — de forma mais restrita do que aplicativos nativos, por estarem sujeitas às permissões e às políticas de segurança impostas pelo navegador. No contexto do InterpreteLabBR, onde o carregamento de documentos PDF via seletor de arquivos nativo é uma operação central, essas restrições impactam diretamente a experiência do usuário e motivam a evolução para uma arquitetura móvel dedicada.

---

## 2.4 *Frameworks* de Desenvolvimento Móvel e *Overhead* de Recursos

O desenvolvimento de aplicativos móveis pode ser realizado por meio de três abordagens principais: (i) desenvolvimento nativo, em que a aplicação é escrita nas linguagens oficiais da plataforma (Kotlin/Java para Android, Swift/Objective-C para iOS), com acesso irrestrito às APIs do sistema operacional; (ii) desenvolvimento híbrido baseado em *web view*, em que o código web é encapsulado em um contêiner nativo e renderizado por um motor de navegador embutido; e (iii) *frameworks* de renderização nativa, como o React Native, que traduzem componentes escritos em JavaScript/TypeScript em componentes nativos da plataforma, sem o uso de *web views*.

A distinção entre essas abordagens tem implicações diretas no desempenho e no consumo de recursos do dispositivo. Oliveira et al. (2023) conduziram um estudo empírico sobre o *overhead* de recursos em *frameworks* de desenvolvimento móvel, comparando soluções baseadas em *web views* com aquelas baseadas em componentes nativos. Os resultados demonstram que *frameworks* baseados em *web views* podem demandar até 8 vezes mais energia do que soluções estruturadas sobre componentes nativos em interações básicas, como a rolagem de listas. Esse *overhead* impacta diretamente a experiência do usuário em dispositivos com recursos limitados de bateria e processamento — cenário comum entre usuários do SUS, que frequentemente utilizam aparelhos Android de entrada.

O React Native, *framework* adotado no InterpreteLabBR para a camada móvel, posiciona-se como uma solução intermediária que combina a produtividade do desenvolvimento em JavaScript/TypeScript com a eficiência de renderização de componentes nativos. Ao contrário de soluções como o Apache Cordova ou o Ionic — que encapsulam *web views* —, o React Native mapeia os componentes declarativos da aplicação diretamente para os componentes visuais do sistema operacional, favorecendo uma execução mais fluida e um menor consumo de recursos. O Expo, utilizado em conjunto com o React Native no projeto, fornece uma camada de abstração que simplifica o processo de *build* e distribuição, incluindo a geração de APKs por meio do serviço EAS Build sem a necessidade de ambiente nativo configurado localmente.

---

## 2.5 Arquitetura API-first e Reuso Arquitetural em Migrações de Software

A arquitetura API-first é uma abordagem de *design* de software na qual a interface de programação de aplicações (API) é concebida e documentada antes da implementação dos clientes que a consomem. Nesse modelo, toda a lógica de negócio e processamento de dados é centralizada no servidor (*backend*), exposta por meio de *endpoints* REST ou GraphQL, e consumida por diferentes clientes — web, mobile, *desktop* — de forma independente. Essa separação de responsabilidades constitui um princípio fundamental de Engenharia de Software, alinhado ao conceito de baixo acoplamento e alta coesão.

No contexto de migrações de sistema, a arquitetura API-first apresenta vantagem expressiva: ao concentrar a lógica clínica no *backend*, ela permite que a substituição ou a evolução da camada de apresentação — de uma PWA para um aplicativo móvel, por exemplo — ocorra sem que o núcleo funcional do sistema precise ser reescrito. No caso do InterpreteLabBR, todo o processamento crítico, incluindo a extração de valores via OCR e a classificação dos analitos segundo as faixas da PNS, reside no *backend* implementado em FastAPI (Python), exposto como serviço REST. Isso permite que tanto o cliente web (PWA) quanto o cliente móvel (React Native) consumam os mesmos *endpoints*, garantindo consistência nos resultados e eliminando a necessidade de duplicação de lógica clínica.

Esse padrão arquitetural é também relevante do ponto de vista da manutenibilidade e da evolução do sistema. Rampinelli et al. (2026) propõem um *framework* de avaliação de sistemas de informação sob a perspectiva do usuário, destacando que sistemas bem estruturados arquiteturalmente tendem a apresentar maior facilidade de adaptação a novos contextos de uso e plataformas. A documentação e a caracterização formal do reuso arquitetural — quantificando o que foi reaproveitado e o que precisou ser reescrito na migração — constituem, portanto, uma contribuição relevante deste trabalho para a literatura de Engenharia de Software aplicada à saúde.

---

## 2.6 Reconhecimento Óptico de Caracteres em Documentos de Saúde

O Reconhecimento Óptico de Caracteres (*Optical Character Recognition* — OCR) é uma tecnologia que converte imagens de texto em texto digital estruturado, possibilitando o processamento computacional de documentos digitalizados ou gerados por impressão. No contexto de sistemas de saúde, o OCR viabiliza a extração automatizada de dados a partir de laudos, prescrições e prontuários, reduzindo a necessidade de entrada manual de informações e ampliando a escalabilidade de soluções de triagem e análise clínica.

A qualidade da extração por OCR em documentos de saúde está sujeita a desafios específicos, incluindo variações no *layout* de impressão, presença de ruídos gráficos, diferenças tipográficas entre unidades de saúde e inconsistências na qualidade de digitalização. Most et al. (2025) abordam abordagens baseadas em visão computacional para recuperação robusta de documentos, evidenciando que estratégias que combinam OCR com técnicas de pré-processamento de imagem tendem a apresentar maior resiliência a variações de qualidade. No contexto do InterpreteLabBR, o leiaute padronizado do laudo do SUS representa tanto uma vantagem — ao permitir o desenvolvimento de heurísticas de *parsing* específicas para esse formato — quanto um desafio, dado que pequenas variações entre laboratórios da rede pública podem introduzir erros de extração.

Bhaskaran e Pardos (2025) investigaram a aplicação de OCR para avaliação automatizada de transcrições acadêmicas, demonstrando que a combinação de técnicas de extração com estratégias de validação pós-OCR aumenta significativamente a precisão dos dados estruturados obtidos. Essa abordagem é análoga à adotada no InterpreteLabBR, que combina *parsing* de texto com OCR como estratégia de *fallback*, e aplica regras de validação para verificar se os valores extraídos estão dentro de faixas plausíveis antes de submetê-los ao motor de classificação.

A questão do pós-processamento de texto extraído por OCR em língua portuguesa é endereçada por Osório e Cardoso (2025), que propõem recursos específicos para otimização de texto em português após extração por OCR. Essa contribuição é particularmente relevante para o contexto do InterpreteLabBR, cujos laudos são emitidos em português e podem conter termos técnicos da nomenclatura hematológica que ferramentas genéricas de OCR tendem a interpretar de forma equivocada.

---

## 2.7 Avaliação de Usabilidade por Inspeção Heurística

A usabilidade é um atributo de qualidade de *software* que mede a facilidade com que usuários conseguem aprender e utilizar uma interface para alcançar seus objetivos, bem como o grau de satisfação proporcionado durante o uso. No contexto de sistemas de saúde voltados ao paciente leigo, a usabilidade assume dimensão crítica: interfaces confusas ou que exigem conhecimento técnico prévio podem resultar em interpretações equivocadas dos dados clínicos, comprometendo o propósito informativo do sistema.

Entre os métodos de avaliação de usabilidade, a Avaliação Heurística, proposta por Jakob Nielsen, é amplamente utilizada na prática de Engenharia de Software por sua eficiência e pelo baixo custo de aplicação. O método consiste na inspeção sistemática da interface por especialistas em usabilidade ou interação humano-computador (IHC), que avaliam a adequação da interface a um conjunto de princípios estabelecidos — as heurísticas de Nielsen —, registrando e classificando os problemas encontrados segundo uma escala de severidade de 0 a 4. A ausência de usuários reais no processo de avaliação, substituídos por especialistas que atuam como juízes inspetores, é uma característica que distingue a avaliação heurística dos testes de usabilidade com usuários, dispensando aprovação de comitê de ética e viabilizando a execução dentro de prazos acadêmicos mais curtos.

Cardieri e Zaina (2018) realizaram um estudo comparativo da experiência do usuário em aplicações web móveis, nativas e PWAs, sob as perspectivas de usuários reais e especialistas em IHC. Os resultados evidenciam diferenças perceptíveis de qualidade de interação entre os paradigmas, com aplicações nativas e PWAs bem implementadas tendendo a superar aplicações web móveis em critérios como responsividade, fluidez e consistência de navegação. Esse achado fundamenta a hipótese central deste trabalho, de que a migração do InterpreteLabBR para um aplicativo móvel resultará em ganhos mensuráveis de usabilidade, verificáveis pela inspeção heurística comparativa.

Rampinelli et al. (2026) propõem um *framework* de avaliação de sistemas de informação sob a perspectiva do usuário, reforçando a necessidade de metodologias estruturadas para a avaliação da qualidade percebida em sistemas de saúde digital. Torkamaan et al. (2026) reforçam essa perspectiva ao evidenciar a crescente relevância de interfaces inteligentes e interativas em saúde, destacando que a qualidade da interação humano-computador em sistemas clínicos impacta diretamente a efetividade e a segurança do uso.

---

## 2.8 *Design Science Research* como Abordagem Metodológica

A *Design Science Research* (DSR) é uma abordagem metodológica originada na área de Sistemas de Informação, utilizada para orientar a concepção, o desenvolvimento e a avaliação de artefatos que resolvem problemas práticos identificados. Diferentemente das metodologias de pesquisa baseadas em observação de fenômenos existentes, a DSR parte da construção de um artefato — seja um sistema, um modelo, um método ou um constructo — e avalia sua efetividade no contexto do problema que motivou sua criação.

A DSR é especialmente adequada a trabalhos de pós-graduação em Tecnologia e Sistemas de Informação que envolvem o desenvolvimento de soluções computacionais, pois confere rigor científico ao processo de construção e validação do artefato, exigindo que o problema seja claramente identificado, que a solução seja fundamentada na literatura e que sua avaliação seja conduzida de forma sistemática e reprodutível. No caso do InterpreteLabBR, o artefato é o aplicativo móvel resultante da migração do PWA original, e sua avaliação ocorre nas três frentes metodológicas previstas: desempenho comparativo (Frente A), caracterização da engenharia da migração (Frente B) e inspeção de usabilidade (Frente C).

---

## 2.9 Trabalhos Relacionados

A presente seção situa o InterpreteLabBR em relação a trabalhos recentes que investigam desempenho, migração e desafios de desenvolvimento em frameworks de aplicativos móveis cross-platform, identificando as contribuições específicas que o diferenciam da literatura existente.

Sokolov (2025) conduziu um estudo experimental quantitativo comparando o consumo de memória e a eficiência de tempo de execução entre uma aplicação React Native e seu equivalente nativo em Kotlin, utilizando criptografia e decriptografia AES como carga computacional de referência e o Android Debug Bridge (ADB) como instrumento de coleta de métricas. Os resultados demonstraram que a implementação nativa superou o React Native em eficiência de CPU e crescimento de memória ao longo do tempo, embora em determinados cenários de decriptografia o React Native tenha apresentado desempenho superior. O trabalho contribui com evidências empíricas sobre o overhead de execução do React Native em tarefas computacionalmente intensivas, mas restringe-se a um benchmark sintético — criptografia de arquivos — sem qualquer vínculo com aplicações de domínio específico ou com o processo de migração de sistemas existentes. O InterpreteLabBR complementa essa perspectiva ao avaliar o overhead de desempenho em um cenário real de uso, com operações predominantemente I/O-bound e rede-bound (submissão de PDF e retorno de JSON da API), sobre dispositivos Android de entrada representativos do perfil de usuários do SUS.

Zhou (2024) realizou um estudo qualitativo com 20 desenvolvedores experientes em React Native e Flutter, por meio de entrevistas semiestruturadas, para mapear os desafios e soluções em projetos de desenvolvimento cross-platform. Entre os desafios mais recorrentes identificados, destacam-se a otimização de desempenho de renderização, a consistência da interface entre plataformas, a integração com módulos nativos e a curva de aprendizado associada às atualizações frequentes dos frameworks. O trabalho oferece uma perspectiva valiosa sobre a experiência do desenvolvedor (DX), mas opera exclusivamente no plano qualitativo e não documenta o processo de migração de um sistema preexistente de um paradigma para outro. O InterpreteLabBR avança nessa direção ao registrar empiricamente o processo de migração de um PWA em produção para React Native, quantificando o reuso de componentes, identificando os padrões de portabilidade adotados e caracterizando o esforço de adaptação por categoria de artefato — informação ausente na literatura revisada por Zhou.

Karin (2025) conduziu uma revisão sistemática da literatura sobre o impacto de frameworks cross-platform no desempenho de aplicações móveis, sintetizando evidências que posicionam soluções baseadas em WebView — incluindo PWAs — como as de maior overhead dentre as abordagens analisadas, com médias de 30 a 60 quadros por segundo e consumo muito elevado de CPU, enquanto o React Native se mostrou mais eficiente para aplicações orientadas a dados, com 45 a 60 quadros por segundo. A revisão conclui que, para 80% das aplicações de negócio com perfil CRUD, a diferença de desempenho entre paradigmas é imperceptível ao usuário final. Embora o trabalho consolide evidências comparativas relevantes, trata-se de uma síntese da literatura existente, sem coleta primária de dados e sem estudo de caso aplicado a um sistema real. O InterpreteLabBR posiciona-se como um estudo de caso primário que instancia, em um sistema de saúde pública real, exatamente a transição de paradigma identificada por Karin como teoricamente vantajosa — de PWA para React Native —, verificando empiricamente se os ganhos de desempenho previstos pela literatura se manifestam no contexto específico de laudos hematológicos no SUS.

Em síntese, os três trabalhos relacionados abordam, de formas complementares, questões de desempenho e experiência de desenvolvimento em frameworks cross-platform, mas nenhum deles trata simultaneamente de: (i) um sistema real de apoio à decisão clínica como objeto de avaliação; (ii) o processo de migração de um PWA em produção para React Native como fenômeno de pesquisa; (iii) a avaliação tripartite que integra desempenho técnico, caracterização da engenharia de migração e inspeção de usabilidade. A originalidade do InterpreteLabBR reside precisamente nessa intersecção, ao conduzir um estudo de caso empírico e reprodutível em um sistema de saúde pública nacional, utilizando ferramentas gratuitas e metodologia verificável, que possa servir de referência para migrações similares no contexto da saúde digital brasileira.

---

## 2.10 Síntese e Posicionamento do Trabalho

A revisão da literatura apresentada neste capítulo evidencia a confluência de múltiplos campos do conhecimento que fundamentam o InterpreteLabBR: a saúde digital brasileira e seus desafios de inclusão (CRUZ et al., 2022), a epidemiologia hematológica nacional e a necessidade de parâmetros populacionais próprios (ROSENFELD et al., 2019), a Engenharia de Software de sistemas móveis e os *trade-offs* entre paradigmas de distribuição (OLIVEIRA et al., 2023; CARDIERI; ZAINA, 2018), as técnicas de extração automatizada de documentos em saúde (MOST et al., 2025; BHASKARAN; PARDOS, 2025; OSÓRIO; CARDOSO, 2025) e os métodos de avaliação de qualidade de sistemas de informação em saúde (RAMPINELLI et al., 2026; TORKAMAAN et al., 2026).

A lacuna identificada na literatura é a escassez de estudos de caso que quantifiquem, em um sistema real de saúde pública, os efeitos de uma migração de paradigma arquitetural — de PWA para aplicativo móvel — sobre métricas concretas de desempenho, reuso de código e usabilidade de interface. O presente trabalho posiciona-se precisamente nessa lacuna, contribuindo com um estudo de caso empírico e reprodutível, fundamentado em ferramentas gratuitas e acessíveis, que possa servir de referência para futuras migrações de sistemas de informação em saúde entre paradigmas de distribuição.

---

## Referências

BAUERMANN, Gabriela Gräwer et al. Desenvolvimento de um sistema de apoio à decisão clínica para cuidadores de pacientes pediátricos hemofílicos. **Journal of Health Informatics**, v. 16, Número Especial SBIS, p. 1-15, 2024.

BHASKARAN, Miha; PARDOS, Zachary A. Automating Academic Transcript Evaluation: A Comparative Study of OCR Techniques for Course and Grade Evaluation. In: ACM CONFERENCE ON LEARNING @ SCALE (L@S '25), 12., 2025, Palermo. **Proceedings...** New York: ACM, 2025. p. 366-370.

CARDIERI, Giulia de Andrade; ZAINA, Luciana Martinez. Analyzing User Experience in Mobile Web, Native and Progressive Web Applications: A User and HCI Specialist Perspectives. In: BRAZILIAN SYMPOSIUM ON HUMAN FACTORS IN COMPUTING SYSTEMS (IHC), 17., 2018, Belém. **Proceedings...** New York: ACM, 2018. p. 1-11.

CRUZ, Tatiana Patricia Farias da et al. Brazilian Digital Health Index (BDHI): avaliação da maturidade da saúde digital do Brasil. **Journal of Health Informatics**, v. 14, Número Especial SBIS, p. 64-69, 2022.

MOST, Alexander et al. Lost in OCR Translation? Vision-Based Approaches to Robust Document Retrieval. In: ACM SYMPOSIUM ON DOCUMENT ENGINEERING 2025 (DocEng '25), 2025, Nottingham. **Proceedings...** New York: ACM, 2025. p. 1-10.

OLIVEIRA, Wellington; MORAES, Bernardo; CASTOR, Fernando; FERNANDES, João Paulo. Analyzing the Resource Usage Overhead of Mobile App Development Frameworks. In: INTERNATIONAL CONFERENCE ON EVALUATION AND ASSESSMENT IN SOFTWARE ENGINEERING (EASE '23), 2023, Oulu. **Proceedings...** New York: ACM, 2023. p. 152-161.

OSÓRIO, Tomás Freitas; CARDOSO, Henrique Lopes. Portuguese post-OCR Resources for Text Optimisation. In: ACM INTERNATIONAL CONFERENCE ON INFORMATION AND KNOWLEDGE MANAGEMENT (CIKM), 34., 2025, Seoul. **Proceedings...** New York: ACM, 2025. p. 1-6.

RAMPINELLI, Vanessa P. C. et al. An evaluation framework for information systems from the users' perspective: a scoping review. **Journal of Health Informatics**, v. 18, p. 1-6, 2026.

ROSENFELD, Luiz Gastão et al. Valores de referência para exames laboratoriais de hemograma da população adulta brasileira: Pesquisa Nacional de Saúde. **Revista Brasileira de Epidemiologia**, v. 22, supl. 2, art. e190003, 2019.

KARIN, Juliana. The Impact of Cross-Platform Frameworks on Mobile Web Application Performance: A Systematic Review. **International Journal of Research and Applied Technology**, v. 5, n. 2, p. 407-411, 2025.

SOKOLOV, Roman. **Comparing Memory Usage and Runtime Efficiency of Cross-Platform vs. Native Mobile Apps**. 2025. Trabalho de Conclusão de Curso (Graduação em Desenvolvimento de Software e Empreendedorismo) — Estonian University of Applied Sciences, Tallinn, 2025.

TORKAMAAN, Helma et al. HealthIUI: Workshop on Intelligent and Interactive Health User Interfaces. In: INTERNATIONAL CONFERENCE ON INTELLIGENT USER INTERFACES COMPANION (IUI Companion '26), 31., 2026, Paphos. **Companion Proceedings...** New York: ACM, 2026. p. 248-252.

TORRENTE, Gisele et al. Atendimento pré-hospitalar móvel e tecnologia: um estudo de validação. **Journal of Health Informatics**, v. 16, Número Especial SBIS, p. 1-14, 2024.

ZHOU, Changkong. **Challenges and Solutions in Cross-Platform Mobile Development: A Qualitative Study of Flutter and React Native**. 2024. Dissertação (Mestrado em Computer, Communication and Information Sciences) — Aalto University, Otaniemi, 2024.
