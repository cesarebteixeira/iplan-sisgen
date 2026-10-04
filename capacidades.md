# As 12 capacidades e as estórias que as compõem

Este documento relaciona **cada estória de usuário** de `Documents/jornadas/` com as **12 capacidades** de `VDP — leitura estendida.md`, na seção *O que o produto precisa fazer*. As capacidades e os seus nomes são os do VDP; a **atribuição de cada estória** é o que este documento acrescenta — o VDP declara quantas telas cada capacidade tem, não quais.

Cada estória está em `US — <código>.md`, nesta mesma pasta. A entrada — `US — 00 Entrada (LOGON, S000M).md` — é a jornada comum a todas as outras e **não** está entre as 223: o VDP a conta à parte, como a porta de entrada (a autenticação e a sessão que todas as 223 usam).

## Como a atribuição foi feita

- **Uma capacidade por estória.** O VDP exige que cada tela pertença a uma só, e a soma feche.
- **Pelo objetivo de negócio, não pelo menu.** Duas estórias do mesmo menu podem estar em capacidades diferentes, e duas do mesmo assunto podem estar em menus diferentes — foi assim que o VDP agrupou.
- **O que decide é o que a tela faz**, lido do `## Estória` de cada uma. O pedido de impressão que algumas fazem não muda o assunto delas.
- **As contagens conferem.** As 12 capacidades deste documento reproduzem, uma a uma, os números declarados no VDP, e somam as 223. Isso não prova que a atribuição é a mesma que o VDP usou — prova que ela é consistente com ele, que é o que dá para conferir. Os casos em que houve dúvida estão em *Onde a atribuição foi julgada*, no fim.

## Quadro geral — na ordem de dependência

As seções deste documento seguem **esta** ordem, e não a numeração do VDP. A numeração, porém, **não muda**: `dominio.md` e `vdp_novo.md` citam “capacidade 4” e continuam valendo. O número é rótulo; a ordem é a de implementação.

| degrau | # | capacidade | estórias | confere | depende de |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | **Estrutura da rede e do gasto** | 15 | 15 | — *(é base)* |
| 1 | 2 | **Catálogo de compras: gêneros, medidas e preços** | 13 | 13 | — *(é base)* |
| 1 | 3 | **Classificação do atendimento escolar** | 15 | 15 | — *(é base)* |
| 1 | 12 | **Segurança, acesso e administração** | 9 | 9 | — *(é base)* |
| 2 | 5 | **Planejamento do cardápio e estimativa de custos** | 41 | 41 | 3, 12 |
| 3 | 9 | **Fornecedores, agricultores e a despesa** | 16 | 16 | 1, 4 |
| 3 | 4 | **Contratos, permissões e a sua execução** | 38 | 38 | 9, 1 |
| 4 | 6 | **Pedidos e entregas da alimentação escolar** | 17 | 17 | 4, 1, 9, 2 |
| 4 | 7 | **Cartões de alimentação escolar** | 7 | 7 | 9 |
| 4 | 8 | **Conferência fiscal: notas fiscais e lotes** | 24 | 24 | 1, 4, 9, 2 |
| 4 | 10 | **Mapa de atendimento e prestação de contas** | 13 | 13 | 5, 9 |
| 4 | 11 | **Relatórios, impressão e processamento em lote** | 15 | 15 | 1, 4, 9 |
| | | **total** | **223** | **223** | |

A entrada — `LOGON → S000M` — fica fora deste quadro: ela é a jornada comum, e o VDP a trata como a porta de entrada das 223, não como uma delas.

---

## Dependência entre as capacidades

### O que “depender” quer dizer aqui

**Dependência de dados**: a capacidade X não funciona sem dados que a Y mantém. Não é ordem de construção — dá para implementar a 5 antes da 3, com dado semeado ou stub. O que não dá é **entrar em produção** com a 5 antes de a 3 existir e estar populada. Dependência de dados trava o *go-live*, não a *ordem de construção*, e tratar as duas como a mesma coisa é o que transforma um cronograma em fila única.

Há uma terceira relação, que não é capacidade→capacidade e vale para as 12: **a plataforma** — autenticação e sessão, autorização por operação, auditoria, validação de entrada e devolução do cursor, fila de impressão. Precisa vir antes de todas, e o VDP já a nomeia como serviço da plataforma, não como operação.

### Como a dependência foi derivada

**Não** veio das citações entre estórias — elas quase não existem. Nas 223 estórias há **1864** citações de tela, e a conta não fecha:

| a citação aponta para | citações |
| --- | --- |
| menus e telas fora das 223 | 1736 |
| telas da **mesma** capacidade | 75 |
| telas de **outra** capacidade | **53** |

Cinquenta e três não fazem um grafo. As estórias foram escritas para não citar código — o que é bom para quem as lê e inútil para quem quer extrair dependência delas.

Veio do **modelo de dados**. O `dominio.md` traz **707 linhas de atributo** nas tabelas por entidade, e um atributo que nomeia outra entidade é chave estrangeira: são **80** delas. Cada aresta abaixo diz quantas chaves a sustentam e um exemplo.

### As arestas, com a evidência

| a capacidade | depende da | chaves | evidência (entidade que aponta → entidade apontada) |
| --- | --- | --- | --- |
| **5** | **3** | 1 | Planejamento de cardápios → Segmento de atendimento |
| **5** | **12** | 1 | Auditoria do cardápio → Sessão |
| **9** | **1** | 1 | Geração dos processos → Órgão |
| **9** | **4** | 1 | Fornecedor por coordenação regional → Tipo de contrato |
| **4** | **9** | 6 | Contrato registrado → Fornecedor; Empenho vinculado ao contrato → Fornecedor; Grupamento de licitação do tipo de contrato → Fornecedor |
| **4** | **1** | 1 | Tipo de contrato → Unidade orçamentária |
| **6** | **4** | 2 | Pedido de alimentação escolar → Tipo de contrato; Distribuição das quantidades do pedido → Tipo de contrato |
| **6** | **1** | 1 | Pedido acumulado → Órgão |
| **6** | **9** | 1 | Pedido de alimentação escolar → Fornecedor |
| **6** | **2** | 1 | Percentual de arredondamento por subclasse e gênero → Unidade de medida |
| **7** | **9** | 1 | Contrato de referência dos cartões → Fornecedor |
| **8** | **1** | 4 | Item da nota fiscal → Fonte de recursos e → Tipo de processo; Processo → Fonte de recursos |
| **8** | **4** | 4 | Nota fiscal → Tipo de contrato; Lote de notas fiscais → Tipo de contrato |
| **8** | **9** | 4 | Nota fiscal → Fornecedor; Lote de notas fiscais → Fornecedor |
| **8** | **2** | 1 | Item da nota fiscal → Unidade de medida |
| **10** | **5** | 3 | Mapa diário de atendimento do órgão filho → Cardápio; Alterações da merenda do mês → Cardápio |
| **10** | **9** | 1 | Movimentação de estoque do mês → Fornecedor |
| **11** | **1** | 2 | Parâmetros do relatório → Fonte de recursos; Processamento em lote → Órgão |
| **11** | **4** | 1 | Parâmetros do relatório → Tipo de contrato |
| **11** | **9** | 1 | Parâmetros do relatório → Fornecedor |

**São relações confirmadas por leitura, não inferidas por casamento de nome.** Duas delas, as que criam o ciclo, foram abertas no `dominio.md` para conferir a frase inteira:

> **Contrato registrado** (cap. 4) — atributo `fornecedor · quem executa · sim · *o nome vem do cadastro de fornecedores*`
> **Fornecedor por coordenação regional** (cap. 9) — atributo `tipo de contrato · o tipo de contrato da permissão · sim`

### O ciclo: 4 ↔ 9

**O grafo não é acíclico, e isso é o achado mais consequente.** O contrato (4) precisa do fornecedor (9) para existir; o fornecedor por coordenação (9) precisa do tipo de contrato (4). Não existe “implemente um antes do outro” para este par: ou as duas se desenvolvem juntas, ou o ciclo se quebra com dado semeado.

### Arestas que eu descartei

Estas apareceram nas chaves e **não** entram na ordem. Ficam nomeadas para poderem ser contestadas, em vez de sumirem numa contagem:

| aresta | evidência | por que ficou de fora |
| --- | --- | --- |
| 1 → 6 | Órgão → Pedido acumulado | leitura invertida: é o órgão que é apontado pelo pedido, não o contrário |
| 4 → 8 | Tipo de contrato → Operador logístico | é a classificação do tipo de contrato, não um dado que precise existir antes |
| 4 → 11 | Cessão e transferência da permissão → Impressora | a impressora é preferência do servidor, não cadastro de negócio |
| 8 → 11 | Movimento do lote → Impressora | idem: preferência de impressão |

### Onde isto contraria o VDP

| o que o VDP afirma sobre as dependências | o que o grafo mostra |
| --- | --- |
| A **1** e a **2** são pré-requisito de quase todas as demais | A 1 confere: cinco capacidades dependem dela (4, 6, 8, 9, 11). A **2** é pré-requisito de **duas** (6 e 8) — “quase todas” é mais do que o dado mostra. |
| A **3** é pré-requisito do cardápio (5) e do pedido (6) | Confere para a **5** (`Planejamento de cardápios → Segmento de atendimento`). Para a **6** não há chave: se a ligação existe, ela não está nos atributos. |
| A **9** não aparece entre os pré-requisitos | A 9 (fornecedores e a despesa) é o **maior hub** do grafo: **seis** capacidades dependem dela (4, 6, 7, 8, 10, 11) — mais que a 1, que o VDP nomeia. |

### O limite deste grafo

**Ele é um piso, não o retrato completo.** Pega “esta entidade aponta para aquela” e **não** pega “este cadastro precisa existir para aquela recusa passar” — que é o caso da maioria das mensagens `* … nao cadastrado *`. Ausência de aresta aqui **não** é ausência de dependência. Fechar a lacuna exige ler as 119 entidades uma a uma, nas seções *Quem mantém* e nas invariantes de exclusão.

---

## Capacidade 1 — Estrutura da rede e do gasto

**15 estórias.** O que a capacidade entrega, no VDP: bairros, unidades orçamentárias, grupos (coordenações regionais), fontes de recursos, contas por fonte e creche, tipos de processo, períodos de referência, feriados do órgão, projetos e o vínculo projeto–órgão, justificativas; transferência e substituição de órgãos entre coordenações.

**Não depende de nenhuma capacidade:** é base.

**É pré-requisito de:** 9 — Fornecedores, agricultores e a despesa; 4 — Contratos, permissões e a sua execução; 6 — Pedidos e entregas da alimentação escolar; 8 — Conferência fiscal: notas fiscais e lotes; 11 — Relatórios, impressão e processamento em lote.

| código | estória |
| --- | --- |
| **C023T** | Manter bairros |
| **C025T** | Manutenção das unidades orçamentárias |
| **C126T** | Manter os grupos da secretaria e a sua unidade orçamentária |
| **C144T** | Manutenção das fontes de recursos da secretaria |
| **C147T** | Classificar as contas da secretaria por fonte de recursos e creche |
| **C162T** | Manter os tipos de processo do órgão |
| **C172T** | Manter os períodos de referência mensais e as suas datas de início e limite |
| **C192T** | Manter os feriados e recessos do órgão |
| **C205T** | Manutenção dos projetos da Secretaria |
| **C207T** | Projetos vinculados ao órgão |
| **C225T** | Transferir órgãos de uma Coordenação Regional Escolar para outra |
| **C226C** | Consultar os órgãos definitivo e provisório do grupo e pedir a relação |
| **C226T** | Substituir o órgão provisório pelo órgão definitivo SDI da coordenadoria regional |
| **C250C** | Consultar as justificativas do tipo de órgão |
| **C806T** | Manter os feriados do órgão |

---

## Capacidade 2 — Catálogo de compras: gêneros, medidas e preços

**13 estórias.** O que a capacidade entrega, no VDP: gêneros de compra e sua vigência, gêneros orgânicos e acréscimo, unidades de medida, grupamentos de licitação e vigências, tabelas de preço (quinzena, especial e por data de referência), gêneros da alimentação escolar e vínculo com o gênero FAE.

**Não depende de nenhuma capacidade:** é base.

**É pré-requisito de:** 6 — Pedidos e entregas da alimentação escolar; 8 — Conferência fiscal: notas fiscais e lotes.

| código | estória |
| --- | --- |
| **C050T** | Manter o cadastro de gêneros e o período de vigência de cada versão |
| **C054T** | Manter o relacionamento dos gêneros orgânicos e o acréscimo sobre o preço |
| **C111T** | Manter as unidades de medida |
| **C213C** | Consulta da tabela de preços do período |
| **C213T** | Manutenção da tabela de preços da quinzena |
| **C217T** | Manter a tabela de preços de gêneros por data de referência |
| **C219T** | Manter os preços da tabela especial da quinzena |
| **C240T** | Manter os grupamentos de classificação de licitação e suas vigências |
| **C241C** | Consultar os grupamentos de classificação de licitação |
| **C802T** | Manter os gêneros da alimentação escolar |
| **C804T** | Atualizar os gêneros da alimentação escolar pelo gênero oficial |
| **F020T** | Manter o vínculo do gênero com o gênero FAE |
| **F022T** | Consultar o vínculo do gênero com o gênero FAE |

---

## Capacidade 3 — Classificação do atendimento escolar

**15 estórias.** O que a capacidade entrega, no VDP: segmentos de atendimento, grupos de atendimento, atendimentos e horários, refeições por tipo de órgão, oferta de refeições por segmento e por grupo, sábado/domingo, comensais por refeição e os percentuais que rateiam o atendimento.

**Não depende de nenhuma capacidade:** é base.

**É pré-requisito de:** 5 — Planejamento do cardápio e estimativa de custos.

| código | estória |
| --- | --- |
| **C022T** | Manter segmentos de atendimento do órgão filho |
| **C101T** | Manter as refeições do tipo de órgão |
| **C102T** | Manter os grupos de atendimento de cada segmento do órgão |
| **C104T** | Manter os atendimentos de cada segmento da secretaria |
| **C106T** | Manter os grupos de atendimento do órgão filho |
| **C108T** | Manter as refeições e a sobremesa do grupo de atendimento |
| **C112T** | Manter os grupos de atendimento de cada refeição |
| **C116T** | Manter as refeições de cada segmento de atendimento |
| **C161T** | Manter o cadastro dos segmentos de atendimento da secretaria |
| **C200T** | Comensais por refeição do segmento do órgão filho SDI |
| **C203T** | Referência mensal de matriculados e comensais do órgão filho |
| **C270T** | Percentual do atendimento por segmento e tipo de refeição |
| **C272T** | Percentual do atendimento por órgão filho, segmento e tipo de refeição |
| **C275T** | Percentual do atendimento por tipo de refeição |
| **C277T** | Atualização do cadastro de atendimento por percentual |

---

## Capacidade 12 — Segurança, acesso e administração

**9 estórias.** O que a capacidade entrega, no VDP: catálogo de telas e relatórios, níveis de acesso e cópia de permissões, autorizações e liberações por tela e por operação, encerramento de sessão, redefinição de senha, origens do funcionário, exclusão de requisições.

**Não depende de nenhuma capacidade:** é base.

**É pré-requisito de:** 5 — Planejamento do cardápio e estimativa de custos.

| código | estória |
| --- | --- |
| **S012T** | Encerramento da sessão de um servidor |
| **S013T** | Redefinição da senha inicial de acesso do funcionário |
| **S014T** | Manter as descrições de origem dos funcionários |
| **S030T** | Cadastro das telas e relatórios do sistema |
| **S031C** | Consulta das telas e relatórios de um módulo do sistema |
| **S059T** | Manter os níveis de acesso e copiar as permissões de outro nível |
| **S062T** | Autorizações de um nível de acesso nas telas e relatórios |
| **S065T** | Liberação de telas e relatórios por nível de acesso |
| **S070T** | Exclusão das requisições de um relatório |

---

## Capacidade 5 — Planejamento do cardápio e estimativa de custos

**41 estórias.** O que a capacidade entrega, no VDP: períodos semanais e validades, composição do cardápio por refeição e semana, planejamento sazonal e semanal, cópia e prorrogação entre períodos, exclusão de períodos encerrados, auditoria do cardápio, médias de comensais e preços por período, cálculo da estimativa e a sua soma, geração do cardápio e do planejamento a partir da estimativa.

**Depende de:** 3 — Classificação do atendimento escolar; 12 — Segurança, acesso e administração.

**É pré-requisito de:** 10 — Mapa de atendimento e prestação de contas.

| código | estória |
| --- | --- |
| **C070C** | Consultar as validades do cardápio |
| **C071C** | Consultar os cardápios de uma data limite e pedir a listagem |
| **C075T** | Manter os períodos semanais do cardápio da coordenação regional |
| **C076T** | Manter as refeições e as semanas do cardápio de um período |
| **C079T** | Atualizar o gênero dos cardápios de um período |
| **C700T** | Prorrogar o período do cardápio da alimentação escolar |
| **C702T** | Consultar as prorrogações da validade do cardápio |
| **C760T** | Manter o planejamento sazonal de cardápios |
| **C764T** | Pedir a cópia do planejamento sazonal de uma origem para um destino |
| **C768T** | Excluir o planejamento sazonal de cardápios de um grupo da coordenação regional escolar |
| **C770T** | Montar o planejamento de cardápios de um grupo, semana, segmento e período |
| **C772T** | Pedir a cópia dos cardápios de um período para outro |
| **C774T** | Pedir a cópia do planejamento de cardápios de um grupo e período para outro |
| **C775T** | Pedir a cópia dos cardápios e dos planejamentos de um período para outro |
| **C776T** | Pedir a exclusão do cardápio de um período |
| **C778T** | Pedir a exclusão do planejamento de um grupo e período |
| **C782C** | Consultar a auditoria de cardápios e planejamentos e solicitar o relatório |
| **C805T** | Atualizar o gênero da alimentação escolar nos cardápios de um período |
| **C810C** | Consultar os cardápios do órgão pela validade e pedir a relação |
| **C825T** | Planejar os cardápios do período por segmento e refeição |
| **C830T** | Manter a média de comensais das refeições em cada período da estimativa |
| **C835T** | Manter os preços dos gêneros em cada período da estimativa |
| **C840C** | Consultar os cálculos de estimativa do grupo pela data limite |
| **C840T** | Registrar o cálculo da estimativa da alimentação escolar do grupo e encomendar o processamento |
| **C848T** | Somar os cálculos de estimativa do grupo e mandar imprimir o resultado |
| **C849T** | Somar os cálculos de estimativa do grupo e receber o resultado por e-mail |
| **C850T** | Gerar os cardápios oficiais de um período a partir da estimativa |
| **C855T** | Gerar o planejamento de um período a partir da estimativa fechada do grupo |
| **C866T** | Copiar cardápios de estimativa entre secretarias e segmentos |
| **C868T** | Copiar o planejamento de estimativa de um período para outro, por grupo, semana e segmento |
| **C870T** | Copiar cardápios oficiais para a estimativa de um novo período |
| **C875T** | Copiar o planejamento oficial de um período para a estimativa de outro |
| **C880T** | Alterar o período da estimativa do órgão |
| **C885T** | Excluir os cadastros de estimativa de um período |
| **C890T** | Excluir o planejamento de estimativa de um período |
| **C895T** | Reabrir os cálculos de estimativa fechados da coordenação regional escolar |
| **C910C** | Consultar os cardápios pela data limite de validade |
| **C922T** | Consultar o planejamento sazonal de cardápios de um grupo |
| **C940T** | Cópia dos cadastros da estimativa para o cardápio de um período |
| **C942T** | Cópia dos cadastros do cardápio para a estimativa de um novo período |
| **C944T** | Excluir os cadastros do cardápio de um período |

---

## Capacidade 9 — Fornecedores, agricultores e a despesa

**16 estórias.** O que a capacidade entrega, no VDP: fornecedores por CNPJ/CPF, mantenedoras e convênios das instituições beneficentes, agricultores e a repartição da nota, documentos de pagamento, desconto, processos e contratos por fornecedor, pré-liquidação e transmissão ao SIAFIC, liquidação, pagamento, consulta de processo e de empenho, arquivo de processos.

**Depende de:** 1 — Estrutura da rede e do gasto; 4 — Contratos, permissões e a sua execução.

**É pré-requisito de:** 4 — Contratos, permissões e a sua execução; 6 — Pedidos e entregas da alimentação escolar; 7 — Cartões de alimentação escolar; 8 — Conferência fiscal: notas fiscais e lotes; 10 — Mapa de atendimento e prestação de contas; 11 — Relatórios, impressão e processamento em lote.

| código | estória |
| --- | --- |
| **F030T** | Pedido de impressão da relação de pagamentos por fonte |
| **F042T** | Trocar a fonte de recurso e a conta bancária de um pagamento |
| **F047T** | Manter o documento de pagamento de cada data do ano |
| **F115T** | Manter o cadastro de mantenedoras das instituições beneficentes |
| **F122T** | Manter os convênios das instituições beneficentes da coordenadoria regional escolar |
| **F130T** | Manter o cadastro de fornecedores por CNPJ ou CPF |
| **F158T** | Registrar o desconto da nota fiscal de recursos próprios |
| **F210T** | Manter os agricultores vinculados ao fornecedor |
| **F220T** | Consultar a nota fiscal e a sua composição de agricultores |
| **F310T** | Registrar o processo, o contrato e a NAD de cada fornecedor da permissão de fornecimento |
| **P211T** | Pré-liquidar o processo e transmitir a pré-liquidação ao SIAFIC |
| **P215T** | Consultar um processo pelo número |
| **P220T** | Consultar os processos de um empenho |
| **P230T** | Pré-liquidação, liquidação e pagamento de processos de despesa |
| **P510T** | Consulta dos anos de arquivo e atualização do número do arquivo |
| **P520T** | Consulta e exclusão dos processos da CRE, com pedido de impressão |

---

## Capacidade 4 — Contratos, permissões e a sua execução

**38 estórias.** O que a capacidade entrega, no VDP: tipos de contrato e permissões, vigências e prioridades, liberação por tipo de licitação, cópia e transferência de permissões entre coordenações e secretarias, rescisão, prorrogação, redução, aditivo de quantidade e de valor, apostilamento e estorno, troca de gênero/autorização, empenhos vinculados e o registro do contrato no FINCON.

**Depende de:** 9 — Fornecedores, agricultores e a despesa; 1 — Estrutura da rede e do gasto.

**É pré-requisito de:** 9 — Fornecedores, agricultores e a despesa; 6 — Pedidos e entregas da alimentação escolar; 8 — Conferência fiscal: notas fiscais e lotes; 11 — Relatórios, impressão e processamento em lote.

| código | estória |
| --- | --- |
| **C060C** | Consultar as permissões de contrato da coordenadoria regional |
| **C060T** | Manter os gêneros das permissões de contrato da coordenadoria regional |
| **C064T** | Estorno do apostilamento por item das permissões da CRE |
| **C066T** | Lançamento do apostilamento por item das permissões da CRE |
| **C067T** | Consultar o apostilamento por item das permissões da CRE |
| **C068T** | Registrar o aditivo de quantidade de um item da permissão |
| **C139T** | Consultar os períodos registrados de um tipo de contrato |
| **C141T** | Manter os tipos de contrato da secretaria e a permissão de cada tipo |
| **C148T** | Manter as telas de uso de cada tipo de licitação |
| **C341T** | Manter a prioridade dos contratos de um gênero na coordenadoria regional |
| **C562T** | Transferir quantidade e valor do gênero em uso para o gênero novo da permissão de fornecimento |
| **C568T** | Alterar as datas de vigência do período de contrato da coordenadoria regional |
| **C640T** | Transferência de parte da permissão de contrato para outra secretaria |
| **C642T** | Cessão de quantidade da permissão de contrato a outra coordenadoria regional |
| **C648T** | Redução da quantidade e do valor da permissão de contrato |
| **C650T** | Cadastro das permissões do operador logístico a partir do contrato de cooperativa |
| **C655T** | Rescisão da permissão de fornecimento e registro em outro tipo de contrato e fornecedor |
| **C658T** | Manter as quantidades e os valores dos itens da permissão auxiliar da coordenadoria regional |
| **C659T** | Permissão de períodos de estimativa do contrato |
| **C660T** | Lançamento dos grupamentos de licitação do tipo de contrato |
| **C662T** | Substituir a gramatura do item da permissão de fornecimento |
| **C664T** | Prorrogação da data limite das permissões de contrato das coordenações regionais |
| **C666T** | Consulta das prorrogações da permissão de contrato da coordenação regional escolar |
| **C667T** | Prorrogação de quantidade e valor da permissão de contrato da coordenação regional escolar |
| **C670T** | Solicitar a alteração do período de licitação da coordenação regional escolar |
| **C671T** | Correção do período do contrato |
| **C677T** | Saldo mínimo da permissão de contrato por gênero |
| **C680T** | Registrar o aditivo de valor do grupamento da permissão |
| **C681T** | Calcular e aplicar o aditivo do contrato |
| **C684T** | Exclusão da prorrogação da permissão de contrato por coordenação regional escolar |
| **C685T** | Itens iniciais do contrato por classe, subclasse e gênero |
| **C687T** | Cancelamento da prorrogação da permissão de contrato da coordenação regional escolar |
| **C690T** | Registrar o contrato do FINCON dos fornecedores de cada coordenação regional escolar |
| **C692C** | Consultar os valores do contrato e o total das permissões da coordenação regional escolar |
| **C694T** | Manter os empenhos vinculados a um contrato da coordenação regional escolar |
| **C697T** | Prorrogação do saldo das permissões de contrato da coordenação regional escolar |
| **C698T** | Copiar o cadastro da permissão de um tipo de contrato para outro, num conjunto de coordenações regionais |
| **C699T** | Transferir a permissão de um grupamento de licitação para outro fornecedor e outro tipo de contrato |

---

## Capacidade 6 — Pedidos e entregas da alimentação escolar

**17 estórias.** O que a capacidade entrega, no VDP: montagem, aprovação, distribuição por dia de entrega, estorno, exclusão, remarcação de período e semana, troca de fornecedor e de contrato, cancelamento do cálculo, renumeração, parâmetros de prazo e arredondamento.

**Depende de:** 4 — Contratos, permissões e a sua execução; 1 — Estrutura da rede e do gasto; 9 — Fornecedores, agricultores e a despesa; 2 — Catálogo de compras: gêneros, medidas e preços.

| código | estória |
| --- | --- |
| **E021T** | Distribuir as quantidades do pedido de alimentação escolar pelos dias de entrega |
| **E023T** | Montar e aprovar um pedido de alimentação escolar |
| **E025T** | Estornar quantidades de um pedido de alimentação escolar |
| **E028T** | Excluir um pedido de alimentação escolar |
| **E029T** | Alterar o período de entrega de um pedido de alimentação escolar |
| **E030T** | Cópia dos pedidos de alimentação escolar para o novo período |
| **E031T** | Alteração das datas de entrega dos pedidos de alimentação escolar |
| **E041T** | Alteração do fornecedor, do período de entrega e da semana do pedido de alimentação escolar |
| **E049T** | Período de entrega da alimentação escolar por coordenadoria regional escolar |
| **E054C** | Consultar os pedidos pendentes de distribuição da coordenadoria regional escolar |
| **E056T** | Cancelar o cálculo de uma requisição de alimentação escolar |
| **E059T** | Alteração do fornecedor e do tipo de contrato dos pedidos |
| **E060T** | Parâmetros de prazo, dia da semana e arredondamento por tipo de órgão |
| **E061T** | Renumeração do pedido de requisição |
| **E065T** | Percentual de arredondamento por subclasse e gênero |
| **E121T** | Lançar os gêneros e as quantidades por dia de entrega de um pedido de alimentação escolar |
| **E506T** | Cancelar o cálculo de uma requisição |

---

## Capacidade 7 — Cartões de alimentação escolar

**7 estórias.** O que a capacidade entrega, no VDP: contrato de referência, entrega de cartões por órgão, justificativas, substituição de cartão bloqueado, estorno de cancelamento e bloqueio, transferência entre órgãos, consulta da entrega.

**Depende de:** 9 — Fornecedores, agricultores e a despesa.

| código | estória |
| --- | --- |
| **E920T** | Manter o contrato de referência e o período de entrega dos cartões |
| **E930T** | Registrar a entrega dos cartões de um contrato |
| **E935T** | Manter as justificativas de cartão |
| **E945T** | Substituir o cartão de referência bloqueado do aluno |
| **E947T** | Estornar o cancelamento e o bloqueio do cartão de referência do aluno |
| **E950T** | Transferir os cartões de referência da matrícula para outro órgão filho (SDI) |
| **E960T** | Consultar a entrega de cartões por órgão filho (SDI) da coordenação regional escolar |

---

## Capacidade 8 — Conferência fiscal: notas fiscais e lotes

**24 estórias.** O que a capacidade entrega, no VDP: registro e consulta de notas, gêneros e quantidades, sequência, lotes e movimentos, exclusão e devolução, troca da fonte do recurso, número do processo no SEI, modelos de nota, entrega dos pedidos, operador logístico.

**Depende de:** 1 — Estrutura da rede e do gasto; 4 — Contratos, permissões e a sua execução; 9 — Fornecedores, agricultores e a despesa; 2 — Catálogo de compras: gêneros, medidas e preços.

| código | estória |
| --- | --- |
| **E223T** | Registrar as notas fiscais das entregas do pedido acumulado |
| **E225T** | Registrar a quantidade da nota fiscal por gênero no pedido acumulado |
| **E233C** | Consultar os pedidos pendentes de fechamento de um pedido acumulado |
| **E234C** | Consultar as quantidades recebidas de uma permissão |
| **E235T** | Abrir o pedido de entrega de um órgão filho a partir do saldo de uma nota fiscal |
| **N011C** | Consulta das notas fiscais de um processo |
| **N019T** | Sequência das notas fiscais do processo |
| **N027T** | Exclusão do lote de notas fiscais |
| **N031C** | Consultar as notas fiscais do órgão filho |
| **N031T** | Exclusão de nota fiscal de fornecedor |
| **N032T** | Troca da fonte de recursos das notas fiscais de um processo |
| **N033T** | Registrar o número SEI do processo |
| **N034T** | Consulta das notas fiscais e das quantidades de um pedido |
| **N035T** | Manutenção dos modelos de nota fiscal |
| **N043T** | Registrar a entrega dos pedidos da nota fiscal |
| **N116T** | Pedido de inclusão automática das notas de um processo |
| **N124C** | Consultar a nota fiscal e os pedidos que a compõem |
| **N224T** | Confirmar a devolução de gênero da nota fiscal |
| **N316T** | Pedidos e notas fiscais do operador logístico por tipo de contrato |
| **N324T** | Manter os gêneros e as quantidades da nota fiscal |
| **N326T** | Consultar a nota fiscal e os gêneros entregues |
| **N327T** | Confirmar a entrega das notas fiscais de um lote |
| **N331T** | Confirmar a entrada das notas fiscais do operador logístico |
| **N334T** | Consulta das notas fiscais e das quantidades de um pedido de operador logístico |

---

## Capacidade 10 — Mapa de atendimento e prestação de contas

**13 estórias.** O que a capacidade entrega, no VDP: mapa mensal e diário de atendimento e de refeições da creche, perfil mensal, atualização de matriculados, movimentações de estoque, justificativas por período, fechamento e reabertura do mês, situação dos mapas da coordenação.

**Depende de:** 5 — Planejamento do cardápio e estimativa de custos; 9 — Fornecedores, agricultores e a despesa.

| código | estória |
| --- | --- |
| **M010C** | Consultar a situação do mapa mensal dos órgãos filhos da coordenadoria |
| **M015C** | Consultar o quadro mensal de matriculados e pessoas do órgão filho |
| **M020T** | Lançar as alterações da merenda do mês de uma unidade |
| **M023T** | Pedir a atualização dos matriculados de um período |
| **M030T** | Manter as movimentações de estoque do mês de um órgão filho da coordenadoria |
| **M040C** | Consultar a situação diária do mapa de um órgão filho da coordenadoria |
| **M047T** | Lançar as justificativas do período no mapa do mês de um órgão filho |
| **M049T** | Pedir a geração do mapa do mês de referência da coordenadoria |
| **M050T** | Fechar o mapa do mês de referência de um órgão filho |
| **M060T** | Reabrir o mapa do mês de referência de um órgão filho |
| **M100T** | Manter o perfil mensal de atendimento do órgão filho |
| **M400T** | Manter o mapa diário de atendimento do órgão filho |
| **M420T** | Manter o mapa diário de refeições da creche |

---

## Capacidade 11 — Relatórios, impressão e processamento em lote

**15 estórias.** O que a capacidade entrega, no VDP: portas de pedido de relatório e de listagem, escolha de impressora, fila de requisições, reimpressão de movimento de lote e geração de processos.

**Depende de:** 1 — Estrutura da rede e do gasto; 4 — Contratos, permissões e a sua execução; 9 — Fornecedores, agricultores e a despesa.

| código | estória |
| --- | --- |
| **C098P** | Pedir a emissão do relatório de permissões de contrato (origem e destino) |
| **C099P** | Informar os parâmetros do relatório e pedir a sua emissão |
| **C100P** | Emissão do relatório de contratos do período |
| **C210T** | Pedido de processamento da quinzena |
| **C672C** | Solicitar a impressão das alterações de período de licitação |
| **E099P** | Solicitar a emissão do relatório de pedidos por data de entrega |
| **E224T** | Emitir o resumo da carga de um lote |
| **F099P** | Parâmetros e pedido de processamento do relatório |
| **F400T** | Requisitar a geração dos processos SME e INSBE |
| **M099P** | Solicitar o processamento dos relatórios da merenda escolar |
| **N030T** | Emissão e reimpressão do movimento do lote |
| **N099P** | Solicitar o processamento dos relatórios fiscais |
| **N330T** | Emissão do movimento do lote de notas fiscais |
| **P099P** | Emissão dos relatórios de empenhos e pagamentos |
| **S099P** | Requisitar o processamento do relatório com os parâmetros informados |

---

## Índice reverso — da estória para a capacidade

| código | capacidade |
| --- | --- |
| LOGON → S000M | *a entrada, comum a todas* |
| C022T | 3 — Classificação do atendimento escolar |
| C023T | 1 — Estrutura da rede e do gasto |
| C025T | 1 — Estrutura da rede e do gasto |
| C050T | 2 — Catálogo de compras: gêneros, medidas e preços |
| C054T | 2 — Catálogo de compras: gêneros, medidas e preços |
| C060C | 4 — Contratos, permissões e a sua execução |
| C060T | 4 — Contratos, permissões e a sua execução |
| C064T | 4 — Contratos, permissões e a sua execução |
| C066T | 4 — Contratos, permissões e a sua execução |
| C067T | 4 — Contratos, permissões e a sua execução |
| C068T | 4 — Contratos, permissões e a sua execução |
| C070C | 5 — Planejamento do cardápio e estimativa de custos |
| C071C | 5 — Planejamento do cardápio e estimativa de custos |
| C075T | 5 — Planejamento do cardápio e estimativa de custos |
| C076T | 5 — Planejamento do cardápio e estimativa de custos |
| C079T | 5 — Planejamento do cardápio e estimativa de custos |
| C098P | 11 — Relatórios, impressão e processamento em lote |
| C099P | 11 — Relatórios, impressão e processamento em lote |
| C100P | 11 — Relatórios, impressão e processamento em lote |
| C101T | 3 — Classificação do atendimento escolar |
| C102T | 3 — Classificação do atendimento escolar |
| C104T | 3 — Classificação do atendimento escolar |
| C106T | 3 — Classificação do atendimento escolar |
| C108T | 3 — Classificação do atendimento escolar |
| C111T | 2 — Catálogo de compras: gêneros, medidas e preços |
| C112T | 3 — Classificação do atendimento escolar |
| C116T | 3 — Classificação do atendimento escolar |
| C126T | 1 — Estrutura da rede e do gasto |
| C139T | 4 — Contratos, permissões e a sua execução |
| C141T | 4 — Contratos, permissões e a sua execução |
| C144T | 1 — Estrutura da rede e do gasto |
| C147T | 1 — Estrutura da rede e do gasto |
| C148T | 4 — Contratos, permissões e a sua execução |
| C161T | 3 — Classificação do atendimento escolar |
| C162T | 1 — Estrutura da rede e do gasto |
| C172T | 1 — Estrutura da rede e do gasto |
| C192T | 1 — Estrutura da rede e do gasto |
| C200T | 3 — Classificação do atendimento escolar |
| C203T | 3 — Classificação do atendimento escolar |
| C205T | 1 — Estrutura da rede e do gasto |
| C207T | 1 — Estrutura da rede e do gasto |
| C210T | 11 — Relatórios, impressão e processamento em lote |
| C213C | 2 — Catálogo de compras: gêneros, medidas e preços |
| C213T | 2 — Catálogo de compras: gêneros, medidas e preços |
| C217T | 2 — Catálogo de compras: gêneros, medidas e preços |
| C219T | 2 — Catálogo de compras: gêneros, medidas e preços |
| C225T | 1 — Estrutura da rede e do gasto |
| C226C | 1 — Estrutura da rede e do gasto |
| C226T | 1 — Estrutura da rede e do gasto |
| C240T | 2 — Catálogo de compras: gêneros, medidas e preços |
| C241C | 2 — Catálogo de compras: gêneros, medidas e preços |
| C250C | 1 — Estrutura da rede e do gasto |
| C270T | 3 — Classificação do atendimento escolar |
| C272T | 3 — Classificação do atendimento escolar |
| C275T | 3 — Classificação do atendimento escolar |
| C277T | 3 — Classificação do atendimento escolar |
| C341T | 4 — Contratos, permissões e a sua execução |
| C562T | 4 — Contratos, permissões e a sua execução |
| C568T | 4 — Contratos, permissões e a sua execução |
| C640T | 4 — Contratos, permissões e a sua execução |
| C642T | 4 — Contratos, permissões e a sua execução |
| C648T | 4 — Contratos, permissões e a sua execução |
| C650T | 4 — Contratos, permissões e a sua execução |
| C655T | 4 — Contratos, permissões e a sua execução |
| C658T | 4 — Contratos, permissões e a sua execução |
| C659T | 4 — Contratos, permissões e a sua execução |
| C660T | 4 — Contratos, permissões e a sua execução |
| C662T | 4 — Contratos, permissões e a sua execução |
| C664T | 4 — Contratos, permissões e a sua execução |
| C666T | 4 — Contratos, permissões e a sua execução |
| C667T | 4 — Contratos, permissões e a sua execução |
| C670T | 4 — Contratos, permissões e a sua execução |
| C671T | 4 — Contratos, permissões e a sua execução |
| C672C | 11 — Relatórios, impressão e processamento em lote |
| C677T | 4 — Contratos, permissões e a sua execução |
| C680T | 4 — Contratos, permissões e a sua execução |
| C681T | 4 — Contratos, permissões e a sua execução |
| C684T | 4 — Contratos, permissões e a sua execução |
| C685T | 4 — Contratos, permissões e a sua execução |
| C687T | 4 — Contratos, permissões e a sua execução |
| C690T | 4 — Contratos, permissões e a sua execução |
| C692C | 4 — Contratos, permissões e a sua execução |
| C694T | 4 — Contratos, permissões e a sua execução |
| C697T | 4 — Contratos, permissões e a sua execução |
| C698T | 4 — Contratos, permissões e a sua execução |
| C699T | 4 — Contratos, permissões e a sua execução |
| C700T | 5 — Planejamento do cardápio e estimativa de custos |
| C702T | 5 — Planejamento do cardápio e estimativa de custos |
| C760T | 5 — Planejamento do cardápio e estimativa de custos |
| C764T | 5 — Planejamento do cardápio e estimativa de custos |
| C768T | 5 — Planejamento do cardápio e estimativa de custos |
| C770T | 5 — Planejamento do cardápio e estimativa de custos |
| C772T | 5 — Planejamento do cardápio e estimativa de custos |
| C774T | 5 — Planejamento do cardápio e estimativa de custos |
| C775T | 5 — Planejamento do cardápio e estimativa de custos |
| C776T | 5 — Planejamento do cardápio e estimativa de custos |
| C778T | 5 — Planejamento do cardápio e estimativa de custos |
| C782C | 5 — Planejamento do cardápio e estimativa de custos |
| C802T | 2 — Catálogo de compras: gêneros, medidas e preços |
| C804T | 2 — Catálogo de compras: gêneros, medidas e preços |
| C805T | 5 — Planejamento do cardápio e estimativa de custos |
| C806T | 1 — Estrutura da rede e do gasto |
| C810C | 5 — Planejamento do cardápio e estimativa de custos |
| C825T | 5 — Planejamento do cardápio e estimativa de custos |
| C830T | 5 — Planejamento do cardápio e estimativa de custos |
| C835T | 5 — Planejamento do cardápio e estimativa de custos |
| C840C | 5 — Planejamento do cardápio e estimativa de custos |
| C840T | 5 — Planejamento do cardápio e estimativa de custos |
| C848T | 5 — Planejamento do cardápio e estimativa de custos |
| C849T | 5 — Planejamento do cardápio e estimativa de custos |
| C850T | 5 — Planejamento do cardápio e estimativa de custos |
| C855T | 5 — Planejamento do cardápio e estimativa de custos |
| C866T | 5 — Planejamento do cardápio e estimativa de custos |
| C868T | 5 — Planejamento do cardápio e estimativa de custos |
| C870T | 5 — Planejamento do cardápio e estimativa de custos |
| C875T | 5 — Planejamento do cardápio e estimativa de custos |
| C880T | 5 — Planejamento do cardápio e estimativa de custos |
| C885T | 5 — Planejamento do cardápio e estimativa de custos |
| C890T | 5 — Planejamento do cardápio e estimativa de custos |
| C895T | 5 — Planejamento do cardápio e estimativa de custos |
| C910C | 5 — Planejamento do cardápio e estimativa de custos |
| C922T | 5 — Planejamento do cardápio e estimativa de custos |
| C940T | 5 — Planejamento do cardápio e estimativa de custos |
| C942T | 5 — Planejamento do cardápio e estimativa de custos |
| C944T | 5 — Planejamento do cardápio e estimativa de custos |
| E021T | 6 — Pedidos e entregas da alimentação escolar |
| E023T | 6 — Pedidos e entregas da alimentação escolar |
| E025T | 6 — Pedidos e entregas da alimentação escolar |
| E028T | 6 — Pedidos e entregas da alimentação escolar |
| E029T | 6 — Pedidos e entregas da alimentação escolar |
| E030T | 6 — Pedidos e entregas da alimentação escolar |
| E031T | 6 — Pedidos e entregas da alimentação escolar |
| E041T | 6 — Pedidos e entregas da alimentação escolar |
| E049T | 6 — Pedidos e entregas da alimentação escolar |
| E054C | 6 — Pedidos e entregas da alimentação escolar |
| E056T | 6 — Pedidos e entregas da alimentação escolar |
| E059T | 6 — Pedidos e entregas da alimentação escolar |
| E060T | 6 — Pedidos e entregas da alimentação escolar |
| E061T | 6 — Pedidos e entregas da alimentação escolar |
| E065T | 6 — Pedidos e entregas da alimentação escolar |
| E099P | 11 — Relatórios, impressão e processamento em lote |
| E121T | 6 — Pedidos e entregas da alimentação escolar |
| E223T | 8 — Conferência fiscal: notas fiscais e lotes |
| E224T | 11 — Relatórios, impressão e processamento em lote |
| E225T | 8 — Conferência fiscal: notas fiscais e lotes |
| E233C | 8 — Conferência fiscal: notas fiscais e lotes |
| E234C | 8 — Conferência fiscal: notas fiscais e lotes |
| E235T | 8 — Conferência fiscal: notas fiscais e lotes |
| E506T | 6 — Pedidos e entregas da alimentação escolar |
| E920T | 7 — Cartões de alimentação escolar |
| E930T | 7 — Cartões de alimentação escolar |
| E935T | 7 — Cartões de alimentação escolar |
| E945T | 7 — Cartões de alimentação escolar |
| E947T | 7 — Cartões de alimentação escolar |
| E950T | 7 — Cartões de alimentação escolar |
| E960T | 7 — Cartões de alimentação escolar |
| F020T | 2 — Catálogo de compras: gêneros, medidas e preços |
| F022T | 2 — Catálogo de compras: gêneros, medidas e preços |
| F030T | 9 — Fornecedores, agricultores e a despesa |
| F042T | 9 — Fornecedores, agricultores e a despesa |
| F047T | 9 — Fornecedores, agricultores e a despesa |
| F099P | 11 — Relatórios, impressão e processamento em lote |
| F115T | 9 — Fornecedores, agricultores e a despesa |
| F122T | 9 — Fornecedores, agricultores e a despesa |
| F130T | 9 — Fornecedores, agricultores e a despesa |
| F158T | 9 — Fornecedores, agricultores e a despesa |
| F210T | 9 — Fornecedores, agricultores e a despesa |
| F220T | 9 — Fornecedores, agricultores e a despesa |
| F310T | 9 — Fornecedores, agricultores e a despesa |
| F400T | 11 — Relatórios, impressão e processamento em lote |
| M010C | 10 — Mapa de atendimento e prestação de contas |
| M015C | 10 — Mapa de atendimento e prestação de contas |
| M020T | 10 — Mapa de atendimento e prestação de contas |
| M023T | 10 — Mapa de atendimento e prestação de contas |
| M030T | 10 — Mapa de atendimento e prestação de contas |
| M040C | 10 — Mapa de atendimento e prestação de contas |
| M047T | 10 — Mapa de atendimento e prestação de contas |
| M049T | 10 — Mapa de atendimento e prestação de contas |
| M050T | 10 — Mapa de atendimento e prestação de contas |
| M060T | 10 — Mapa de atendimento e prestação de contas |
| M099P | 11 — Relatórios, impressão e processamento em lote |
| M100T | 10 — Mapa de atendimento e prestação de contas |
| M400T | 10 — Mapa de atendimento e prestação de contas |
| M420T | 10 — Mapa de atendimento e prestação de contas |
| N011C | 8 — Conferência fiscal: notas fiscais e lotes |
| N019T | 8 — Conferência fiscal: notas fiscais e lotes |
| N027T | 8 — Conferência fiscal: notas fiscais e lotes |
| N030T | 11 — Relatórios, impressão e processamento em lote |
| N031C | 8 — Conferência fiscal: notas fiscais e lotes |
| N031T | 8 — Conferência fiscal: notas fiscais e lotes |
| N032T | 8 — Conferência fiscal: notas fiscais e lotes |
| N033T | 8 — Conferência fiscal: notas fiscais e lotes |
| N034T | 8 — Conferência fiscal: notas fiscais e lotes |
| N035T | 8 — Conferência fiscal: notas fiscais e lotes |
| N043T | 8 — Conferência fiscal: notas fiscais e lotes |
| N099P | 11 — Relatórios, impressão e processamento em lote |
| N116T | 8 — Conferência fiscal: notas fiscais e lotes |
| N124C | 8 — Conferência fiscal: notas fiscais e lotes |
| N224T | 8 — Conferência fiscal: notas fiscais e lotes |
| N316T | 8 — Conferência fiscal: notas fiscais e lotes |
| N324T | 8 — Conferência fiscal: notas fiscais e lotes |
| N326T | 8 — Conferência fiscal: notas fiscais e lotes |
| N327T | 8 — Conferência fiscal: notas fiscais e lotes |
| N330T | 11 — Relatórios, impressão e processamento em lote |
| N331T | 8 — Conferência fiscal: notas fiscais e lotes |
| N334T | 8 — Conferência fiscal: notas fiscais e lotes |
| P099P | 11 — Relatórios, impressão e processamento em lote |
| P211T | 9 — Fornecedores, agricultores e a despesa |
| P215T | 9 — Fornecedores, agricultores e a despesa |
| P220T | 9 — Fornecedores, agricultores e a despesa |
| P230T | 9 — Fornecedores, agricultores e a despesa |
| P510T | 9 — Fornecedores, agricultores e a despesa |
| P520T | 9 — Fornecedores, agricultores e a despesa |
| S012T | 12 — Segurança, acesso e administração |
| S013T | 12 — Segurança, acesso e administração |
| S014T | 12 — Segurança, acesso e administração |
| S030T | 12 — Segurança, acesso e administração |
| S031C | 12 — Segurança, acesso e administração |
| S059T | 12 — Segurança, acesso e administração |
| S062T | 12 — Segurança, acesso e administração |
| S065T | 12 — Segurança, acesso e administração |
| S070T | 12 — Segurança, acesso e administração |
| S099P | 11 — Relatórios, impressão e processamento em lote |

---

## Onde a atribuição foi julgada

Nem toda estória diz a que capacidade pertence. Estas exigiram decisão, e o critério fica registrado para poder ser contestado:

| estória(s) | capacidade | por quê |
| --- | --- | --- |
| C203T | 3 | A estória declara comensais e matriculados **mês a mês**, e o mês é assunto da capacidade 10; fica na 3 porque o que ela define é o **número de comensais** que a classificação do atendimento usa, e porque a 10 fecha em 13 sem ela e a 3 fecha em 15 com ela. É a atribuição mais discutível do conjunto. |
| C672C | 11 | Pede a **impressão** de alterações de período de licitação. O conteúdo é de contrato (4), mas a tela não opera contrato nenhum: é porta de relatório. |
| C210T | 11 | Pede o **processamento do relatório** da quinzena. A quinzena é assunto do catálogo de preços (2), mas a tela não mantém preço: é porta de relatório. |
| E224T | 11 | Emite o resumo da carga de um **lote**. Fica em lote/processamento em lote (11), e não em conferência fiscal (8), porque não confere nota: manda o lote rodar. |
| E099P | 11 | O relatório é de pedidos por data de entrega (6), mas a tela é a porta genérica de relatório: recebe os parâmetros e registra a solicitação. |
| C071C / C810C / C226C | 5 / 5 / 1 | Consultam e **pedem a listagem**. Ficam na capacidade do conteúdo consultado, e não na 11, porque o que a tela mostra é o cadastro de negócio; o pedido de papel é o fim da jornada, não o assunto dela. |
| C782C | 5 | Consulta a **auditoria do cardápio** e pede o relatório. A auditoria do cardápio está nomeada na capacidade 5, e é o que a tela mostra. |
| S070T | 12 | Apaga as **requisições** de um relatório. A fila é assunto da 11, mas a exclusão de requisições está nomeada na 12 — e é ela que fecha as 9. |
| F030T | 9 | Pede a impressão da **relação de pagamentos** por fonte. Fica em despesa (9), não em relatórios (11): o recorte é a despesa, e a fonte é entidade da 9. |
| F310T | 9 | Registra processo, contrato e NAD **por fornecedor**. Fica em fornecedores e a despesa (9), e não em contratos (4), porque o que ela amarra é o fornecedor da permissão. |
| C650T | 4 | Cadastra as permissões do **operador logístico** — e o operador logístico aparece na capacidade 8. Fica na 4 porque o que a tela faz é criar permissão. |
| C805T | 5 | Troca o gênero **nos cardápios** de um período, e o gênero é catálogo (2). Fica na 5 porque quem é reescrito é o cardápio. |
| C806T | 1 | Segundo cadastro de **feriados do órgão**, ao lado da C192T. Os dois ficam na 1: feriados estão nomeados lá, e separá-los por tela seria inventar um recorte que o VDP não faz. |
| M049T | 10 | Pede a **geração** do mapa do mês. Fica na 10, e não em processamento em lote (11), porque o que ela gera é o mapa, conteúdo de negócio da 10. |

## Se o agrupamento ou a ordem forem outros

A leitura do VDP é uma proposta, e a validação é da Secretaria — este documento herda isso. Se o agrupamento preferido for outro, o que é preciso refazer é a tabela `ATRIBUICAO` de `gerar_capacidades.py`, que gera este arquivo — não a leitura das 223 estórias: nenhuma estória foi resumida nem reescrita aqui, e todas continuam nos seus arquivos.

O mesmo vale para a dependência: `DEPENDE` são as arestas aceitas, `EVIDENCIA` é o que sustenta cada uma, `FRACAS` são as descartadas e `ORDEM` é o resultado em degraus. O programa **recusa gerar** uma ordem em que uma capacidade apareça antes de outra de que depende — a não ser no ciclo declarado em `CICLOS`. Discordar da ordem é mudar `DEPENDE` ou `ORDEM`, e o programa diz na hora se a ordem nova viola uma aresta.
