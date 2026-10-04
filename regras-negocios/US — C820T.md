# US — C820T — Planejamento semanal da merenda

## Estória

Como **servidor de CRE que monta a merenda do período**, quero **dizer, para cada refeição
de um segmento, em qual semana do rodízio e dentro de qual período ela é servida e qual
cardápio vai em cada dia dessa semana**, para que **o preparo da merenda saiba, dia a dia,
o que servir, e o planejamento do período encontre o cardápio no lugar certo**.

Um cardápio cadastrado sozinho não diz o que serve em cada dia: é este planejamento que
amarra, para uma coordenação regional escolar, uma semana do rodízio, um segmento e um
período, o cardápio de cada dia da semana e a refeição que o serve. É a única tela do
sistema que cria, altera e apaga esses registros — as outras telas que os enxergam apenas
os leem —, e é ele que a tela de ligação do cardápio com a refeição consulta antes de
deixar desfazer o vínculo: ela recusa retirar da refeição um cardápio que está neste
planejamento.

## Contexto

Jornada S000M → C000M → C800M → C811M → C820T.

Ator: servidor de CRE — diz, para cada refeição de um segmento, qual cardápio vai em cada
dia de cada semana do rodízio, dentro do período do cardápio.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os três menus do caminho (o `C000M`, o `C800M` e o
`C811M`) não gravam nada e só encaminham; o último esvazia a área de trabalho da sessão
antes de encaminhar, e é por isso que esta tela abre em consulta e em branco (§RN-15).

O que esta tela usa do que veio antes é o **contexto da sessão** — o tipo de órgão, a
matrícula, o código de acesso, o privilégio, a coordenação regional escolar e a estação —,
que é regra da entrada e está no anexo de evidências, em **Regras que se revelaram da
entrada**. Do contexto vêm também a data do sistema e o tipo de órgão que a tela mostra; o
grupo, a semana, o segmento e o período o servidor digita.

Esta tela **encadeia** na consulta do cardápio, a `C815T`, quando a marca de novo cardápio
está posta (§RN-16): é a única saída dela para outra tela, e não há menu no meio.

## Regras de negócio

### RN-01 — O que a tela mantém: o planejamento semanal da refeição

Para uma **coordenação regional escolar** (o grupo), uma **semana do rodízio** (A, B, C ou
D), um **segmento** e um **período** — a data limite da validade, com o início que o
cadastro do cardápio daquele período informa —, esta tela mantém **o cardápio de cada um
dos sete dias da semana, refeição por refeição**. O registro do planejamento guarda o tipo
de órgão, o grupo, a letra da semana, o segmento, a refeição, as duas datas do período, os
sete cardápios (de segunda a domingo) e a situação do período.

A tela enxerga **dez** cadastros. **Oito** ela só lê: o título das telas (2.000 registros
de capacidade), o cadastro das refeições (1.200), a ligação da refeição com o segmento
(10.000), o cadastro dos grupos (1.000), o cadastro dos segmentos (200.000), o cardápio da
validade (100.000), o cardápio no segmento (500.000) e a ligação do cardápio com a refeição
(100.000). Em **dois** ela grava: o planejamento semanal (200.000) e a auditoria
(60.000.000). Os números são de **dimensionamento** — o máximo esperado que o dicionário de
dados declara, não o volume cadastrado.

O tipo de órgão não se digita: é o da sessão, e ele entra na identificação de tudo o que a
tela lê e grava.

### RN-02 — A consulta não grava nada

Em **consulta**, a tela apenas mostra: o grupo, a semana, o segmento, o início e o limite do
período, a situação do período e, linha a linha, o código e a descrição da refeição e os
**sete** cardápios da semana. Não grava, não trava registro e não deixa rastro na auditoria.

### RN-03 — A tela só trabalha em alterar e consultar

A tela reconhece **duas** operações no campo da operação: **alterar** e **consultar**.
Qualquer outra coisa informada nesse campo é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta ao campo, e nada é
lido nem gravado.

[?] A recusa manda usar ALT ou CON e o que a tela compara são os códigos internos das duas
operações — a alteração e a consulta —; é a mesma dúvida já registrada nas outras telas
desta jornada. Ou o terminal traduz o que o servidor digita antes de enviar, ou quem seguir
a mensagem é recusado. Pergunta ao site.

### RN-04 — A identificação: o grupo, a semana, o segmento e a data limite

O planejamento de uma refeição é identificado por **seis** dados: o tipo de órgão (da
sessão), o **grupo** (2 dígitos), a **letra da semana do rodízio** (A, B, C ou D), o
**segmento** (2 dígitos), a **refeição** (2 dígitos) e as três partes da **data limite** do
período (dia com 2, mês com 2 e ano com 4).

A **data de início** do período aparece na tela e vai para o registro do planejamento, mas
**não** entra na identificação: a tela a repõe a partir do cadastro do cardápio daquele
período a cada exibição.

[?] A data de início é editável e a tela a grava no planejamento quando a refeição é
incluída, mas a conferência de "consultou antes" não a compara, e a exibição a reescreve a
partir da consulta. Não consigo concluir, pelo fonte, se o que o servidor digita ali chega
a ser gravado. Pergunta ao site.

### RN-05 — A consulta confere o grupo, a semana, o segmento e a data limite

Antes de mostrar qualquer coisa, a consulta passa por **quatro** peneiras, nesta ordem:

- o **grupo** tem de estar cadastrado — não estando, a recusa é **\* Grupo nao cadastrado \***,
  com o cursor no grupo;
- a **semana** tem de ser A, B, C ou D — não sendo, a recusa é
  **\* Informe semana com A, B, C ou D \***, com o cursor na semana;
- o **segmento** tem de estar cadastrado — não estando, a recusa é
  **\* Segmento nao cadastrado \***, com o cursor no segmento;
- a **data limite** tem de estar preenchida, dia, mês e ano — não estando, a recusa é
  **\* Informe a data limite de validade \***, com o cursor no dia limite.

Se os dados digitados forem exatamente os da consulta anterior da sessão, a tela não refaz
as conferências: é a mesma consulta, e ela só repõe o que já estava guardado.

### RN-06 — O período precisa ter cardápio cadastrado

Passando as quatro peneiras, o sistema ainda exige que o **período tenha pelo menos um
cardápio cadastrado**: não havendo, a consulta é recusada com
**\* Nao existem cardapios neste periodo \***, com o cursor no dia limite. É do cardápio do
período que a tela traz a data de início e a situação que exibe.

### RN-07 — A lista: treze linhas, uma por refeição, com os sete dias e a ação

A lista é uma página de **treze** linhas. Cada linha mostra o código da refeição, a
descrição curta dela e os **sete** cardápios da semana (segunda a domingo), e cada linha tem
o campo onde o servidor escreve o que fazer naquela linha: **I** para incluir a refeição no
planejamento daquela semana, **A** para alterar e **E** para excluir.

Cada linha ocupa **38 bytes** e tem **nove** campos: o código da refeição, os sete códigos de
cardápio e a ação. Linha deixada com o código de refeição em branco não é tocada. Ação fora
de I, A e E também não é tocada — em silêncio, sem mensagem nenhuma.

### RN-08 — A lista vazia avisa

Quando não há nenhuma refeição para listar — nem planejamento para aquele grupo, semana,
segmento e período, nem refeição ligada àquele segmento —, a tela avisa
**\* Grupo/Semana/Segmento sem planejamento cadastr \*** e não monta linha nenhuma.

### RN-09 — Incluir uma refeição no planejamento

Para incluir, duas conferências antes das conferências de cardápio: a refeição **não pode**
já estar no planejamento daquele grupo, semana, segmento e período — estando, a recusa é
**\* Refeicao ja cadastrada neste grupo/sem/seg.\***, com o cursor na ação da linha —, e o
servidor tem de informar **pelo menos um** cardápio entre os sete dias — não informando
nenhum, a recusa é **\* Informe cardapios para os dias \***, com o cursor no primeiro dia.

Passando, cada dia informado é conferido (RN-12) e o planejamento é criado com o tipo de
órgão, o grupo, a semana, o segmento, a refeição, as duas datas do período e os sete
cardápios da semana.

### RN-10 — Alterar o planejamento de uma refeição

Para alterar, a refeição **tem de estar** no planejamento daquele grupo, semana, segmento e
período — não estando, a recusa é **\* Refeicao nao cadastrada neste grupo/sem/seg \***, com
o cursor na ação da linha —, e o servidor tem de informar pelo menos um cardápio entre os
sete dias, com a mesma recusa e o mesmo cursor da inclusão.

Passando, cada dia informado é conferido (RN-12) e a alteração **substitui os sete cardápios
do registro**; os demais dados do planejamento — o grupo, a semana, o segmento, a refeição e
as duas datas — não mudam.

### RN-11 — Excluir o planejamento de uma refeição

Para excluir, a refeição tem de estar no planejamento daquele grupo, semana, segmento e
período — não estando, a recusa é **\* Refeicao nao cadastrada neste grupo/sem/seg \***, com
o cursor na ação da linha. Passando, o registro do planejamento é apagado. A exclusão não
confere mais nada além disso — nem se o cardápio continua ligado à refeição, nem se ele
aparece em outro planejamento.

### RN-12 — Cada cardápio informado num dia é conferido antes de gravar

Antes de gravar, **cada** cardápio informado nos sete dias passa por **cinco** conferências,
uma após a outra:

- tem de **existir** no período — não existindo, a recusa é **\* Cardapio nao cadastrado \***;
- **não pode** estar marcado como cardápio de sobremesa — estando, a recusa é
  **\* Cardapio cadastrado como sobremesa \***;
- tem de estar **previsto para aquele segmento** no período — não estando, a recusa é
  **\* Cardapio nao cadastrado neste segmento \***;
- tem de estar **marcado para aquela semana do rodízio** no cardápio da validade — não
  estando, a recusa é **\* Cardapio nao cadastrado nesta semana \***;
- tem de estar **ligado àquela refeição**, pela ligação que a tela `C815T` mantém — não
  estando, a recusa é **\* Cardapio nao cadastrado nesta refeicao \***.

Dia deixado em branco é pulado: não é conferido nem gravado. Qualquer uma das cinco recusas
devolve o cursor ao **dia** que recusou, na linha em que ele está, e nada é gravado.

### RN-13 — Alterar exige ter consultado antes

A alteração só passa com o **mesmo grupo, a mesma semana, o mesmo segmento e a mesma data
limite** que a consulta deixou guardados na sessão. Divergindo, a recusa é
**\* Consulte o planejamento antes da atualizacao \***, com o cursor de volta ao campo da
operação, e nada é lido nem gravado. A consulta não exige nada disso: é ela que deixa o
planejamento guardado para a alteração.

### RN-14 — O período fechado barra a alteração

Alterando, o planejamento daquele grupo, semana, segmento e período tem de estar com o
período **aberto**: estando fechado para estimativa, a alteração é recusada com
**\* Cadastro fechado para este periodo \***, com o cursor no campo da operação, e nada é
gravado. A consulta a um período fechado é permitida, a tela mostra **FECHADO** no lugar da
situação, e o planejamento que ela cria nasce com a situação em branco.

[?] A situação conferida aqui é a do **planejamento**, e não a do cardápio do período que a
tela exibe. Nenhuma tela do acervo analisado grava "fechado" nesse registro — a tela cria o
planejamento com a situação em branco e a única atribuição a esse indicador nunca recebe
"F". Ou o indicador vem de carga externa ao acervo, ou a recusa é inalcançável. Pergunta ao
site; não escolho um dos dois lados.

### RN-15 — A abertura depende da área de trabalho da sessão

A operação da tela não é escolhida por quem a abre: ela vem da **área de trabalho da
sessão**, e quem a preenche é a própria tela, a cada mensagem.

- Aberta **pelo menu**, a área chega em branco — os três menus do caminho a esvaziam antes
  de encaminhar —, e a tela abre em **consulta**, com o grupo, a semana, o segmento, as
  datas e a lista em branco, e sem ler cadastro nenhum.
- Depois de uma **consulta**, a área guarda a operação de consulta e os dados consultados, e
  é deles que a exibição seguinte repõe o grupo, a semana, o segmento, as datas e a lista
  das refeições.
- Para **alterar**, o servidor troca a operação e repete os mesmos dados: é a área que diz
  se aquela combinação já foi consultada (RN-13).

[?] A vida da área de trabalho comum não vem do acervo: o menu desta jornada a esvazia
escrevendo nela um campo de seis caracteres, e a troca entre a área que o programa usa e a
área comum é do ambiente. Se o ambiente a limpa a cada transação, o material não diz.
Pergunta ao site.

### RN-16 — A tela entrega a transação à consulta do cardápio

Quando a **marca de novo cardápio** está posta, esta tela não faz manutenção: ela esvazia a
área de trabalho, deixa a operação em **consulta** e entrega a transação à tela `C815T` — a
mesma que liga o cardápio às refeições. A operação que ela entrega é a de **consulta**, e é
assim que a `C815T` abre por causa da entrega. É a única saída desta tela para outra.

[?] A marca de novo cardápio é um campo de um caractere que esta tela só **lê** — nunca a
escreve — e que não tem rótulo nenhum na ficha da tela. Quem a preenche com **S** — o
formulário, um comando, ou outra tela — o material não diz. Pergunta ao site.

### RN-17 — Toda mudança deixa rastro na auditoria

Cada gravação é acompanhada de um registro de auditoria: a criação do planejamento, a
alteração dos cardápios da semana e o apagamento do registro. O registro leva o órgão, o
**cadastro que mudou** — o planejamento semanal —, a imagem do registro antes e a depois, a
operação (inclusão, alteração ou exclusão), a matrícula, o código de acesso, a estação, a
data e a hora, o número do processo e o código da tela que provocou a mudança. A consulta
não deixa registro.

### RN-18 — O acesso, a rota e a permissão são conferidos antes de qualquer leitura

Na abertura, o sistema confere a permissão de segurança do perfil para esta tela; a cada
mensagem do servidor ele confere a rota e a permissão; e, antes de incluir, alterar ou
excluir a linha, confere de novo a permissão, agora para a operação que a linha pediu. Sem
isso, a tela não lê nada e não grava nada.

[?] O texto das recusas de acesso não está no material: as conferências são rotinas de
biblioteca, sem corpo no lote, e o texto sai da tabela de mensagens do sistema, que também
não está no lote. Pergunta ao site.

### RN-19 — O que se digita é conferido antes de qualquer leitura

Nenhum dos campos numéricos é texto livre. Passam pela edição numérica, antes de qualquer
leitura de cadastro — em branco valendo zero —, **dezesseis** campos: o grupo, o segmento,
as três partes da data de início, as três partes da data limite, a refeição e os sete
cardápios dos dias. O que não for número é recusado no próprio campo, com o cursor de volta
a ele.

Não passam por essa edição: o campo da operação, o da próxima tela, a **letra da semana**
(que é conferida depois, na consulta), a ação da linha e a marca de novo cardápio.

[?] O texto dessa recusa não está no material: a edição é uma rotina de biblioteca, cujo
corpo não faz parte do lote, e o texto sai da tabela de mensagens do idioma, que também não
está no lote. Pergunta ao site.

### RN-20 — Falha no banco interrompe a operação e avisa

Erro de leitura vira a ação 53 e erro de gravação a ação 55, despachadas pela rotina comum
de comunicação; cada gravação é seguida do teste de aborto, que interrompe a transação antes
de seguir para a gravação seguinte.

## Cenários BDD

```gherkin
Funcionalidade: O planejamento semanal da merenda por grupo, segmento e refeição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C820T

  Cenário: RN-01 — o que a tela grava e o que ela só lê
    Dado que incluo uma refeição no planejamento, altero os cardápios de outra e excluo uma terceira
    Quando confirmo cada operação
    Então só o planejamento semanal e a auditoria recebem gravação
    E o título das telas, o cadastro das refeições, a ligação da refeição com o segmento, os cadastros de grupo e de segmento, o cardápio da validade, o cardápio no segmento e a ligação do cardápio com a refeição não são alterados

  Cenário: RN-02, RN-04 e RN-06 — consultar o planejamento de uma semana
    Dado que estou na tela C820T com a opção de consulta
    E informo o grupo, a semana do rodízio, o segmento e a data limite do período
    Quando confirmo a consulta
    Então vejo o grupo, a semana, o segmento, o início e o limite do período e a situação dele
    E vejo, em cada linha, o código e a descrição da refeição e os sete cardápios da semana
    E a data de início aparece como está no cadastro do cardápio daquele período
    E nada é gravado e nenhum registro de auditoria é deixado

  Cenário: RN-03 — operação que a tela não reconhece
    Quando informo no campo da operação uma operação que não é alterar nem consultar
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: RN-05 — grupo não cadastrado
    Dado que informo um grupo que não está cadastrado
    Quando confirmo a consulta
    Então vejo "* Grupo nao cadastrado *"
    E o cursor volta ao campo do grupo

  Cenário: RN-05 — semana fora de A, B, C e D
    Dado que informo na semana uma letra que não é A, B, C nem D
    Quando confirmo a consulta
    Então vejo "* Informe semana com A, B, C ou D *"
    E o cursor volta ao campo da semana

  Cenário: RN-05 — segmento não cadastrado
    Dado que informo um segmento que não está cadastrado
    Quando confirmo a consulta
    Então vejo "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento

  Cenário: RN-05 — data limite não informada
    Dado que deixo a data limite do período sem preencher
    Quando confirmo a consulta
    Então vejo "* Informe a data limite de validade *"
    E o cursor volta ao campo do dia limite

  Cenário: RN-06 — período sem cardápios
    Dado que informo um período para o qual não há nenhum cardápio cadastrado
    Quando confirmo a consulta
    Então vejo "* Nao existem cardapios neste periodo *"
    E o cursor volta ao campo do dia limite

  Cenário: RN-07 — a lista tem treze linhas, uma por refeição
    Dado que consultei um grupo, uma semana, um segmento e um período com planejamento
    Quando a tela é apresentada
    Então cada linha traz o código e a descrição de uma refeição, os sete cardápios da semana e o campo da ação
    E nenhuma linha passa de treze

  Cenário: RN-07 — linha sem refeição ou com ação fora de I, A e E
    Dado que consultei o planejamento
    E deixo uma linha sem código de refeição, ou escrevo nela uma ação que não é I, A nem E
    Quando confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada e nada é gravado nela

  Cenário: RN-08 — grupo, semana e segmento sem planejamento
    Dado que consultei um grupo, uma semana, um segmento e um período que ainda não têm planejamento
    Quando a tela monta a lista
    Então vejo "* Grupo/Semana/Segmento sem planejamento cadastr *"
    E nenhuma linha é montada

  Cenário: RN-09 e RN-12 — incluir uma refeição no planejamento
    Dado que consultei o grupo, a semana, o segmento e o período
    E a refeição ainda não está no planejamento
    E informo nos dias cardápios que existem no período, não são de sobremesa, estão previstos no segmento, estão marcados para aquela semana e estão ligados àquela refeição
    Quando escrevo a ação I na linha e confirmo
    Então o planejamento daquela refeição naquela semana é gravado com os sete cardápios
    E a operação fica registrada na auditoria

  Cenário: RN-09 — refeição que já está no planejamento
    Dado que a refeição já está no planejamento daquele grupo, semana, segmento e período
    Quando escrevo a ação I na linha e confirmo
    Então vejo "* Refeicao ja cadastrada neste grupo/sem/seg.*"
    E o cursor volta à ação daquela linha
    E nada é gravado

  Cenário: RN-09 e RN-10 — nenhum cardápio informado nos dias
    Dado que consultei o planejamento e deixei os sete dias da linha em branco
    Quando escrevo nela a ação I ou a ação A e confirmo
    Então vejo "* Informe cardapios para os dias *"
    E o cursor volta ao primeiro dia daquela linha
    E nada é gravado

  Cenário: RN-12 — cardápio que não existe no período
    Dado que informo num dia um cardápio que não existe naquele período
    Quando confirmo a linha
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor volta ao dia recusado
    E nada é gravado

  Cenário: RN-12 — cardápio marcado como sobremesa
    Dado que informo num dia um cardápio que está marcado como cardápio de sobremesa
    Quando confirmo a linha
    Então vejo "* Cardapio cadastrado como sobremesa *"
    E o cursor volta ao dia recusado
    E nada é gravado

  Cenário: RN-12 — cardápio não previsto no segmento
    Dado que informo num dia um cardápio que não está previsto para aquele segmento
    Quando confirmo a linha
    Então vejo "* Cardapio nao cadastrado neste segmento *"
    E o cursor volta ao dia recusado
    E nada é gravado

  Cenário: RN-12 — cardápio não marcado naquela semana do rodízio
    Dado que informo num dia um cardápio que não está marcado para aquela semana
    Quando confirmo a linha
    Então vejo "* Cardapio nao cadastrado nesta semana *"
    E o cursor volta ao dia recusado
    E nada é gravado

  Cenário: RN-12 — cardápio não ligado àquela refeição
    Dado que informo num dia um cardápio que não está ligado àquela refeição
    Quando confirmo a linha
    Então vejo "* Cardapio nao cadastrado nesta refeicao *"
    E o cursor volta ao dia recusado
    E nada é gravado

  Cenário: RN-12 — dia deixado em branco
    Dado que preencho só alguns dos sete dias da linha
    Quando confirmo a linha
    Então só os dias preenchidos são conferidos e gravados
    E os dias em branco não são conferidos nem apagados

  Cenário: RN-10 e RN-12 — alterar os cardápios da semana de uma refeição
    Dado que a refeição já está no planejamento daquele grupo, semana, segmento e período
    E informo dias que passam por todas as conferências de cardápio
    Quando escrevo a ação A na linha e confirmo
    Então os sete cardápios daquela refeição são substituídos pelos informados
    E o grupo, a semana, o segmento, a refeição e as duas datas continuam como estavam
    E a operação fica registrada na auditoria

  Cenário: RN-10 — alterar refeição que não está no planejamento
    Dado que a refeição não está no planejamento daquele grupo, semana, segmento e período
    Quando escrevo a ação A na linha e confirmo
    Então vejo "* Refeicao nao cadastrada neste grupo/sem/seg *"
    E o cursor volta à ação daquela linha
    E nada é gravado

  Cenário: RN-11 — excluir o planejamento de uma refeição
    Dado que a refeição está no planejamento daquele grupo, semana, segmento e período
    Quando escrevo a ação E na linha e confirmo
    Então o registro do planejamento daquela refeição naquela semana é apagado
    E a auditoria guarda o que estava lá, com o valor posterior em branco

  Cenário: RN-11 — excluir refeição que não está no planejamento
    Dado que a refeição não está no planejamento daquele grupo, semana, segmento e período
    Quando escrevo a ação E na linha e confirmo
    Então vejo "* Refeicao nao cadastrada neste grupo/sem/seg *"
    E o cursor volta à ação daquela linha
    E nada é apagado

  Cenário: RN-13 — alterar sem ter consultado antes
    Dado que estou na tela C820T com a opção de alteração
    E informo grupo, semana, segmento ou data limite diferentes dos da consulta que fiz
    Quando confirmo
    Então vejo "* Consulte o planejamento antes da atualizacao *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: RN-14 — alterar um período fechado
    Dado que consultei o planejamento e o período dele está fechado para estimativa
    Quando confirmo a alteração
    Então vejo "* Cadastro fechado para este periodo *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: RN-15 — abrir a tela pelo menu
    Dado que abro a tela C820T pela opção do menu
    Quando a tela é apresentada
    Então ela abre na consulta
    E o grupo, a semana, o segmento, as datas e a lista estão em branco
    E nenhum cadastro é lido

  Cenário: RN-15 — a tela repõe o que a consulta deixou
    Dado que consultei um grupo, uma semana, um segmento e um período
    Quando a tela é apresentada de novo
    Então o grupo, a semana, o segmento e as datas voltam preenchidos
    E a lista das refeições é montada de novo a partir do planejamento

  Cenário: RN-16 — a passagem para a consulta do cardápio
    Dado que a marca de novo cardápio está posta
    Quando confirmo
    Então a transação passa para a tela C815T
    E ela abre na consulta, sem cardápio nenhum
    E nenhuma manutenção é feita nesta confirmação

  Cenário: RN-17 — o rastro da gravação
    Dado que incluí uma refeição, alterei os cardápios de outra e excluí uma terceira
    Quando o sistema processa cada operação
    Então o sistema deixa um registro de auditoria por mudança, dizendo qual cadastro mudou
    E cada registro leva o órgão, o antes e o depois, a operação, a matrícula, o código de acesso, a estação, a data, a hora e a tela que provocou a mudança

  Cenário: RN-18 — sem a permissão de acesso
    Dado que o meu perfil não tem esta tela, ou eu não tenho a permissão da operação
    Quando entro na tela ou confirmo a operação de uma linha
    Então vejo a recusa de acesso do sistema
    E nenhum cadastro é lido e nada é gravado

  Cenário: RN-19 — campo não numérico
    Quando preencho o grupo, o segmento, uma das partes das datas, a refeição ou um dos cardápios dos dias com letra
    Então a tela recusa o campo antes de qualquer leitura de cadastro
    E o cursor volta ao campo recusado
    E nada é gravado

  Cenário: RN-20 — falha do banco durante a gravação
    Dado que a gravação do planejamento falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E a gravação não é considerada feita
```
