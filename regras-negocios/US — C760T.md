# US — C760T — Consultar o planejamento de cartões por CRE, segmento e refeição

## Estória

Como **servidor da CRE**, quero **consultar o planejamento de cartões de uma coordenação
regional, por segmento e por refeição, num período**, para que **eu saiba quantos cartões
cada mês do período prevê e quantos já estão distribuídos aos órgãos da coordenação**.

O planejamento de cartões liga o cardápio do período à quantidade diária que a coordenação
prevê em cada mês; é dele que a Secretaria tira o número contratado. Esta tela é a leitura
desse planejamento: ela reúne o cardápio do período, a quantidade diária de cartões de cada
mês e o total de cartões dos órgãos subordinados que já recebem. Como a tela abre em
consulta e exige uma consulta antes de qualquer atualização, sem ela a CRE não tem como
conferir o que está previsto — e é essa conferência que sustenta a atualização.

## Contexto

Jornada S000M → C000M → C070M → C760M → C760T.

Ator: servidor de CRE — confere, na `C760T`, o planejamento mensal de cartões da sua
coordenação, por segmento de atendimento e por refeição, e o total de cartões dos órgãos
que já recebem.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A `C760T` é o último passo da jornada e a `C760M`, que a antecede, não é menu de opções: ela
avisa o sistema de que a tela seguinte é esta, sem passar por menu nenhum. A `C760T`
**não tem saída**: terminada a consulta, a tela é abandonada e a transação acaba. O que a
`C760M` deixa para esta tela é o contexto da sessão e a operação pretendida, e é isso que
decide em que modo a `C760T` abre — por isso esse contexto é regra desta tela, e está na
RN-01. A tela também confere se a coordenação regional e o segmento de atendimento
informados existem, e recusa a consulta quando não existem.

## Regras de negócio

### RN-01 — O modo da tela vem de quem a abriu e, em branco, é consulta

A tela executa numa de duas operações: **alteração** ou **consulta**. A operação não é
perguntada nesta tela: ela chega do contexto da sessão, montado por quem abriu a tela.
Quando chega **em branco**, a tela assume **consulta**. Operação diferente de alteração e de
consulta — inclusão e exclusão, por exemplo — é recusada com
`* Opcao nao disponivel. Use ALT ou CON *`, o cursor volta para o campo da opção e nada é
lido nem gravado.

Consequência disso, e é o ponto que mais fácil se perde: com o modo em branco a tela abre
**em consulta**, e em consulta ela não inclui, não altera e não exclui nada.

[?] A tela anterior manda abrir a `C760T`, mas não encontrei nos fontes desta jornada o
ponto em que o modo de **alteração** é gravado antes disso. Ou ele chega de uma tela que a
jornada não percorre, ou por este caminho a `C760T` só abre em consulta — e nesse caso todo
o caminho de atualização que a tela tem fica sem ter como ser alcançado. Pergunta ao site.

### RN-02 — A tela mostra o planejamento do período e as quantidades de cada mês

A tela identifica-se por `COORD.REG.ESCOLA`, `COD.SEGMENTO`, `COD.REFEICAO`,
`DIA INICIO PERIO`, `MES INICIO PERIO` e `ANO INICIO PERIO`, e o período vai do início
informado até **`DIA LIMITE` / `MES LIMITE` / `ANO LIMITE`**. Ela mostra **11 linhas de
cardápio**; cada linha traz o código do cardápio, o nome do cardápio e a quantidade diária
de cartões de cada um dos **doze meses**, de janeiro a dezembro.

Ao lado das quantidades do período, e linha a linha, a tela mostra o **total de cartões dos
órgãos subordinados** que já recebem naquele mês, apurado a partir dos registros diários
dos órgãos da coordenação. A coordenação regional, o segmento, a refeição e o cardápio são
descritos pelo sistema a partir dos códigos informados: a tela acrescenta o nome da
coordenação, o do segmento, o da refeição e o do cardápio.

A tela também avisa quando a coordenação regional informada não consta do cadastro de
grupos — `* Grupo nao cadastrado *` — e quando o segmento de atendimento informado não
consta do cadastro de segmentos — `* Segmento nao cadastrado *` —, devolvendo o cursor ao
campo recusado. A refeição, ao contrário, é buscada só para ser descrita: não há recusa
quando ela não está cadastrada.

### RN-03 — Período sem planejamento cadastrado é avisado, e a tela não mostra linhas

Percorrido o período sem encontrar o planejamento do segmento, a tela avisa
`* Segmento sem planejamento cadastrado *` e encerra a consulta, sem apresentar cardápio
nem quantidades. O aviso é dado uma única vez, na primeira linha do período.

### RN-04 — A consulta não grava nada

Em consulta a tela só lê. Nenhuma linha de cardápio é incluída, alterada ou excluída e
nenhum lançamento de auditoria é gerado. A tela lê o planejamento, o cardápio do período,
o cadastro de segmentos, o cadastro de refeições, o cadastro da coordenação regional, o
vínculo entre cardápio e refeição, o vínculo entre cardápio e segmento e os registros
diários dos órgãos subordinados; nada disso é modificado.

### RN-05 — São vinte e dois dados conferidos, e a data limite é obrigatória

A tela confere, um a um, **22 dados**: a coordenação regional, o segmento, a refeição, o
dia, o mês e o ano de início do período, o dia, o mês e o ano limite, o código do cardápio
e as doze quantidades mensais. Cada um é tratado como número: campo em branco vale zero, os
zeros à esquerda e a formatação de sinal são descartados. A leitura do período **exige dia,
mês e ano limite**; faltando qualquer um dos três, a consulta para com
`* Informe a data limite de validade *`, com o cursor no campo.

### RN-06 — Para atualizar, é preciso ter consultado antes a mesma combinação

A tela só atualiza o planejamento que ela mesma acabou de consultar. Se a coordenação
regional, o segmento, a refeição, o dia, o mês e o ano limite informados não forem
exatamente os da consulta anterior, a operação para com
`* Consulte o planejamento antes da atualizacao *` e nada é gravado. Na prática, incluir,
alterar ou excluir exige consultar primeiro a coordenação, o segmento, a refeição e o
período com que se vai trabalhar.

[?] Isso cria um passo obrigatório que a tela não explica: quem entra em alteração e digita
um período novo é recusado e precisa voltar à consulta. Se é regra de negócio ou limitação
da tela antiga, é pergunta ao site.

### RN-07 — A inclusão exige o período anterior, cujo limite termina onde este começa

A inclusão de um cardápio no planejamento não grava só no período informado: para gravar, o
sistema procura o planejamento **anterior**, aquele cujo limite termina no dia, no mês e no
ano em que este período começa, e toma dele o dia, o mês e o ano de início. É com esse
início anterior que o cardápio e a quantidade do primeiro mês do período novo são
gravados. Não encontrando esse planejamento anterior, ou encontrando um cujo limite não
seja o início do período informado, a atualização não acontece: a tela fica fora do
tratamento de atualização e nada é gravado nem confirmado.

### RN-08 — Inclusão exige cardápio que atenda ao período, ao segmento e à refeição

Para incluir um cardápio no planejamento, todas as condições abaixo precisam valer; a
primeira que faltar interrompe a inclusão e nada é gravado:

- o cardápio precisa **existir no período informado** — senão
  `* Cardapio nao cadastrado *`;
- o cardápio precisa **existir no segmento de atendimento informado** — senão
  `* Cardapio nao cadastrado neste segmento *`;
- o cardápio precisa **estar cadastrado para a refeição informada** — senão
  `* Cardapio nao cadastrado para esta refeicao *`;
- o cardápio precisa **estar cadastrado como sobremesa** — senão
  `* Cardapio nao cadastrado como sobremesa *`;
- o cardápio **não** pode já estar no planejamento do período — senão
  `* Cardapio ja cadastrado neste planejamento *`.

[?] A inclusão exige que o cardápio esteja cadastrado como sobremesa, e não encontrei no
fonte desta jornada a razão de negócio dessa exigência: ela recusa cardápios que são prato
principal. O site confirma se a exigência é intencional.

### RN-09 — Alteração exige que o cardápio já esteja no planejamento

Para alterar, o cardápio precisa estar no planejamento do período consultado. Não estando,
a operação para com `* Cardapio nao cadastrado neste planejamento *` e nada é gravado.
Estando, o registro é travado, as doze quantidades mensais informadas substituem as que
estavam gravadas — em cada mês, a quantidade do período informado passa a valer — e a
alteração é confirmada com `* Alteracao confirmada *`.

### RN-10 — Exclusão não exclui: a conferência que a precede contradiz o caminho

A tela tem um caminho para excluir o cardápio do planejamento, e ele só age **quando o
cardápio não está no planejamento**; mas o caminho de exclusão só é alcançado depois de a
tela confirmar que o cardápio **está** no planejamento, e é essa confirmação que o
direciona. Os dois lados se contradizem sobre o mesmo cardápio: estando no planejamento, a
conferência manda para a exclusão e a guarda do caminho recusa; não estando, a conferência
já recusou antes. A exclusão é **inalcançável por este caminho**, e nada é excluído.

### RN-11 — Toda gravação fica registrada na auditoria

Inclusão e alteração gravam um lançamento de auditoria com o cadastro de origem, a tela de
origem (`C760T`), a operação, o conteúdo anterior e o posterior, a coordenação regional, a
matrícula do funcionário, a estação, o dia, o mês, o ano e a hora da sessão, o tipo de
órgão e o número do processo — que recebe o código do cardápio. O cadastro de auditoria tem
**15 campos** e admite 60 milhões de registros, que é **capacidade** declarada — quanto
existe de fato, o acervo não informa.

### RN-12 — A tela não encadeia nada

A `C760T` é o último passo da jornada e **não passa registro nem operação** para tela
nenhuma. Encerrada a consulta, a tela é abandonada e a transação termina.

## Cenários BDD

```gherkin
Funcionalidade: Consultar o planejamento de cartões por CRE, segmento e refeição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C760T

  Cenário: A tela abre em consulta quando o modo chega em branco
    Dado que cheguei à C760T sem que a operação pretendida tenha sido informada
    Quando a tela confere o modo
    Então ela assume a consulta
    E não inclui, não altera e não exclui nada

  Cenário: Operação diferente de alteração e de consulta é recusada
    Dado que cheguei à C760T com uma operação diferente de alteração e de consulta
    Quando a tela confere o modo
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo da opção
    E nada é lido nem gravado

  Cenário: Consulta mostra o planejamento do período com as quantidades de cada mês
    Dado que existe planejamento cadastrado para a coordenação, o segmento, a refeição e o período informados
    Quando abro a C760T
    Então vejo até 11 linhas de cardápio, com o código e o nome de cada uma
    E vejo a quantidade diária de cartões de cada mês, de janeiro a dezembro
    E vejo, por mês, o total de cartões dos órgãos que já recebem
    E vejo o nome da coordenação, do segmento, da refeição e do cardápio

  Cenário: A consulta não grava nada
    Dado que estou na C760T em consulta
    Quando a tela percorre o planejamento e os cadastros que ele usa
    Então nenhuma linha é incluída, alterada ou excluída
    E nenhum lançamento de auditoria é gerado

  Cenário: Coordenação regional não cadastrada
    Dado que informei uma coordenação regional que não consta do cadastro de grupos
    Quando abro a C760T
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo da coordenação regional
    E nada é gravado

  Cenário: Segmento de atendimento não cadastrado
    Dado que informei um segmento de atendimento que não consta do cadastro de segmentos
    Quando abro a C760T
    Então vejo a mensagem "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento
    E nada é gravado

  Cenário: Período sem planejamento cadastrado
    Dado que não existe planejamento cadastrado para o segmento no período informado
    Quando abro a C760T
    Então vejo a mensagem "* Segmento sem planejamento cadastrado *"
    E não vejo cardápio nem quantidades
    E nada é gravado

  Cenário: Falta a data limite de validade
    Dado que deixei em branco o dia, o mês ou o ano limite
    Quando abro a C760T
    Então vejo a mensagem "* Informe a data limite de validade *"
    E nada é gravado

  Cenário: Não existem cardápios no período
    Dado que não existe cardápio cadastrado para o período limite informado
    Quando abro a C760T
    Então vejo a mensagem "* Nao existem cardapios neste periodo *"
    E nada é gravado

  Cenário: Atualização sem consultar antes a mesma combinação
    Dado que estou em alteração e mudo a coordenação, o segmento, a refeição ou o período
    Quando confirmo a atualização
    Então vejo a mensagem "* Consulte o planejamento antes da atualizacao *"
    E nada é gravado

  Cenário: Inclusão de cardápio que não está cadastrado no período é recusada
    Dado que o cardápio informado não está cadastrado no período
    Quando informo a situação de inclusão com esse cardápio
    Então vejo a mensagem "* Cardapio nao cadastrado *"
    E nada é gravado

  Cenário: Inclusão de cardápio que não existe no segmento é recusada
    Dado que o cardápio informado não está cadastrado no segmento informado
    Quando tento incluir o cardápio no planejamento
    Então vejo a mensagem "* Cardapio nao cadastrado neste segmento *"
    E nada é gravado

  Cenário: Inclusão de cardápio que não atende à refeição é recusada
    Dado que o cardápio informado não está cadastrado para a refeição informada
    Quando tento incluir o cardápio no planejamento
    Então vejo a mensagem "* Cardapio nao cadastrado para esta refeicao *"
    E nada é gravado

  Cenário: Inclusão de cardápio que não está cadastrado como sobremesa é recusada
    Dado que o cardápio informado não está cadastrado como sobremesa
    Quando tento incluir o cardápio no planejamento
    Então vejo a mensagem "* Cardapio nao cadastrado como sobremesa *"
    E nada é gravado

  Cenário: Inclusão de cardápio que já está no planejamento é recusada
    Dado que o cardápio informado já está no planejamento do período
    Quando tento incluir o cardápio no planejamento
    Então vejo a mensagem "* Cardapio ja cadastrado neste planejamento *"
    E nada é gravado

  Cenário: Inclusão exige o planejamento anterior que termina onde este período começa
    Dado que o período anterior não existe, ou o limite dele não é o início do período informado
    Quando tento incluir o cardápio no planejamento
    Então a atualização não acontece
    E nada é gravado nem confirmado

  Cenário: Inclusão de um cardápio no planejamento
    Dado que o cardápio existe no período, no segmento e para a refeição, e está cadastrado como sobremesa
    E que o cardápio ainda não está no planejamento do período
    E que existe o planejamento anterior, cujo limite termina onde este período começa
    Quando incluo o cardápio no planejamento
    Então o período novo recebe o cardápio e a quantidade do primeiro mês
    E a alteração e a exclusão do registro também são gravadas
    E a operação é registrada na auditoria

  Cenário: Alteração exige o cardápio já planejado
    Dado que o cardápio informado não está no planejamento do período
    Quando tento alterar
    Então vejo a mensagem "* Cardapio nao cadastrado neste planejamento *"
    E nada é gravado

  Cenário: Alteração das quantidades de um cardápio planejado
    Dado que o cardápio está no planejamento do período consultado
    Quando altero as quantidades dos meses
    Então as quantidades do período informado passam a ser as que eu informei
    E vejo a mensagem "* Alteracao confirmada *"
    E a operação é registrada na auditoria

  Cenário: Exclusão não exclui nada
    Dado que o cardápio está no planejamento do período
    Quando tento excluir o cardápio do planejamento
    Então a conferência que precede o caminho de exclusão manda seguir
    E o caminho de exclusão recusa, porque o cardápio está no planejamento
    E o cardápio continua no planejamento
    E nada é excluído

  Cenário: Falha de banco interrompe a operação
    Dado que o banco falha durante a leitura ou a gravação
    Quando a tela lê ou grava
    Então a tela avisa da falha
    E a gravação não é completada
```
