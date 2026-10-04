# US — E056T — Cancelamento do cálculo do preparo da alimentação escolar

## Estória

Como **servidor de CRE**, quero **cancelar o cálculo do preparo de um órgão filho, numa
coordenadoria regional escolar e numa data de início de preparo**, para que **tudo o que
aquele cálculo gerou seja desfeito — os itens calculados, as quantidades por gênero, os
pedidos com os seus itens, o acumulado do gênero e o que já tinha sido lançado na quantidade
recebida — e a requisição volte a ficar sem cálculo, pronta para ser refeita**.

O cálculo do preparo é a conta que transforma o período de entrega e os comensais de cada
refeição em quantidades por gênero e, depois, em pedidos. Depois de calculado, ele já mexeu em
outros lugares: criou os itens calculados, gerou pedidos, consumiu o acumulado do fornecedor e
baixou a quantidade recebida. Cancelar, portanto, não é apagar uma linha: é desfazer essa
corrente inteira, e na ordem certa. Um pedido que ficasse para trás viraria pedido sem
cálculo; uma quantidade baixada duas vezes viraria saldo errado no contrato. É a operação que
a CRE usa quando o período de entrega, os comensais ou o cardápio mudaram e o cálculo precisa
ser refeito antes de virar pedido.

## Contexto

Jornada S000M → E000M → E050M → E056T.

Ator: servidor de CRE — informa o órgão filho, a coordenadoria regional escolar e a data de
início do preparo e responde pela confirmação do cancelamento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As duas telas antes desta são menus: elas não passam registro nem operação adiante, e o que
chega à tela é só o que a sessão deixou — o tipo de órgão, a coordenadoria e o órgão do meu
vínculo. A identificação do cálculo é informada aqui, e a operação é marcada pela própria
tela. Esta tela não encadeia para outra: quando a exclusão termina, ela reabre a si mesma.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — O que esta tela cancela e o que ela mostra

A tela cancela **um** cálculo do preparo por vez: o de um órgão filho SDI, numa coordenadoria
regional escolar, numa data de início de preparo. Esses três dados, com o tipo de órgão do meu
vínculo, são o que identifica o cálculo — não existe mais de um cálculo do mesmo órgão na
mesma data.

A tela tem **22 campos de entrada** — os cinco primeiros são do ambiente (a tela, a origem, o
número da transação, a data e o mês de competência) e os outros **17** são de negócio: a
operação, a tela seguinte, o órgão, a coordenadoria, as três partes da data de início do
preparo, as três do limite do cálculo, as três do início do período, as três do limite do
período e a resposta da confirmação. Tem ainda **7 campos de saída**. Dos campos de entrada,
**14** passam pela edição numérica.

Do cálculo, ela mostra o nome do órgão, o tipo de órgão, a data do sistema e três datas que
vêm da requisição: o limite do cálculo, o início do período de entrega e o limite do período.
Essas três são **de leitura**: o que eu escrever nelas é descartado e reposto pelo que está
gravado na requisição.

Abrindo a tela, a única coisa que ela faz é conferir o meu acesso e mostrar o que sabe: o
cursor fica no campo do órgão e **nada é gravado**.

[?] A data do sistema e a descrição do tipo de órgão são lidas de uma área da sessão, e a
entrada grava as duas em outra: no acervo não há caminho que transporte uma para a outra. Se o
ambiente não fizer esse transporte, os dois campos aparecem em branco. Pergunta ao site.

### RN-02 — A tela abre na exclusão e não aceita outra operação

Ao abrir, a tela marca a operação como **exclusão**: é ela mesma que preenche o código da
operação, e é esse código que a conferência aceita. Com qualquer outra operação, a recusa é
**\* Operacao nao disponivel. Use EXC \***, com o cursor de volta ao campo da operação, e nada
é gravado.

Se a passagem que chega trouxer uma **tela seguinte** preenchida, a tela não processa nada: ela
encaminha a sessão para essa outra tela.

[?] O campo da tela seguinte não é preenchido em nenhum ponto do programa — só é levado à
rotina que decide o encaminhamento. Quem o preenche, a máscara da tela ou o ambiente, não está
nesta jornada. Pergunta ao site.

### RN-03 — Antes de tudo, o acesso e a liberação da exclusão

Abrindo a tela, o sistema confere a estação da sessão com a estação do meu cadastro e procura a
tela no cadastro de telas do meu código de acesso: não achando, o acesso é recusado. Ao
processar, confere também se a **exclusão** está liberada para o meu código de acesso naquela
tela — e a rotina de rota confere a tela outra vez, com outra mensagem para a mesma falta.

As recusas que o servidor vê são **\* Tela nao disponivel \***,
**\* Acesso negado para esta matricula \***, **\* Acesso negado para esta operacao \***,
**\* Acesso a pagina 2 negado \*** ou **\* Tela nao cadastrada \***. Em qualquer delas nada é
apagado e nada é gravado.

### RN-04 — O órgão é obrigatório e tem de estar no meu alcance

O órgão filho é obrigatório: sem ele, a recusa é **\* Informe o orgao \***, com o cursor de
volta ao campo, e nada é processado.

Quem tem um órgão no vínculo da sessão não cancela cálculo de outro órgão: informando um órgão
diferente do do vínculo, a recusa é **\* Usuario sem acesso a outro orgao \***, com o cursor no
campo do órgão. Quem não tem órgão no vínculo passa por essa conferência.

O órgão informado ainda tem de existir: não estando cadastrado, a recusa é
**\* Orgao nao cadastrado \***, também com o cursor no campo do órgão.

### RN-05 — A coordenadoria do cálculo tem de ser a minha

O cálculo tem de ser de um órgão do meu grupo. O órgão informado é lido no cadastro, e a
coordenadoria que passa a valer é a do cadastro do órgão, **não** a que eu digitei. Sendo o
cadastro do órgão de outra coordenadoria que não a minha, a recusa é
**<- Usuario sem acesso ao grupo deste orgao \***, com o cursor no campo do órgão, e nada é
processado. Quem não tem coordenadoria no vínculo da sessão passa por essa conferência.

### RN-06 — A data de início do preparo é obrigatória e os códigos são numéricos

A data de início do preparo é obrigatória: com o dia zerado, a recusa é
**\* Informe a data de inicio do preparo \***, com o cursor de volta ao campo, e nada é
processado. O mês e o ano não têm conferência própria: eles entram na procura da requisição e,
errados, caem na recusa de requisição não cadastrada.

Os códigos e as datas que eu informo passam pela edição numérica: o que estiver em branco vira
zero, os zeros à esquerda caem, e o que não for número é recusado — no órgão e na data de
início do preparo o cursor volta ao campo. São **14** campos nessa edição: o órgão, a
coordenadoria e as doze partes das quatro datas (início do preparo, limite do cálculo, início
do período e limite do período).

### RN-07 — A requisição do preparo tem de existir e estar calculada

A tela procura a requisição do preparo pelo tipo de órgão do meu vínculo, pelo órgão, pela
coordenadoria do cadastro do órgão e pelas três partes da data de início. Não achando, a
recusa é **\* Requisicao nao cadastrada \***, com o cursor na data de início, e nada é
processado.

Achando a requisição **sem a marca de calculada**, a recusa é
**\* Requisicao nao calculada \***, também com o cursor na data de início, e nada é processado:
só se cancela o que já foi calculado.

Achando a requisição calculada, a tela traz dela o nome do órgão e repõe as datas do cálculo e
do período.

### RN-08 — Não se cancela cálculo com pedido recebido nem com pedido do acumulado

Antes de pedir a confirmação, a tela percorre os pedidos que aquele cálculo gerou e os itens de
cada um. Os itens já marcados como excluídos não entram na conferência. A recusa vem em dois
casos:

- quando algum item do pedido já tem **quantidade recebida** — a recusa é
  **\* Ja existe pedido com quantidade recebida \***, com o número daquele pedido;
- quando algum item do pedido é do **acumulado** — a recusa é
  **\* Exc pedido *n* do acumulado *m* \***, com o número do pedido e o número do acumulado.

Nas duas, o cursor volta à data de início do preparo e nada é apagado nem gravado.

[?] A tela guarda os pedidos distintos do cálculo numa lista de **20** posições. Um cálculo com
mais de 20 pedidos deixa os excedentes fora da varredura: eles não entram nestas recusas e não
são apagados no cancelamento — a requisição é cancelada e parte dos pedidos que ela gerou fica
no sistema. Se isso pode acontecer, é pergunta ao site.

### RN-09 — O aviso do arquivo do fornecedor

Quando pelo menos um dos pedidos do cálculo está marcado como já enviado ao fornecedor, a tela
avisa **\* Pedidos ja constam do arquivo do fornecedor \***, no campo de aviso, junto com a
pergunta da confirmação. O aviso **não** impede o cancelamento: ele só informa que aquele
pedido já saiu daqui.

### RN-10 — A exclusão só acontece depois da confirmação

Passando pelas conferências, a tela **não apaga nada ainda**: ela mostra
**\* Confirma exclusao do calculo <S/N> ? *\*** e põe o cursor no campo da resposta. A exclusão
só segue quando eu respondo **S** — e com o órgão e a data de início do preparo ainda os
mesmos; mudando qualquer um deles, a confirmação é pedida de novo. Respondendo qualquer outra
coisa, nada é apagado.

[?] Responder N não devolve a tela ao começo: o sistema limpa a resposta, volta a examinar o
cálculo e pede a confirmação outra vez. Se a intenção era permitir desistir da exclusão, não há
caminho para isso no fonte — a saída é encerrar a tela. Pergunta ao site.

### RN-11 — O que o cancelamento desfaz

Confirmada a exclusão, a tela desfaz, nesta ordem:

- para cada **item acumulado** do cálculo, baixa da quantidade recebida do acumulado a
  quantidade que aquele item representa;
- apaga os **itens acumulados** do gênero cujo pedido é um dos pedidos do cálculo;
- apaga os **itens calculados** do cálculo, subclasse a subclasse e gênero a gênero;
- apaga o **cálculo por gênero** — as sete quantidades calculadas de cada par de subclasse e
  gênero do cálculo;
- para cada pedido do cálculo: apaga os **itens do pedido** — devolvendo à **permissão de
  entrega do contrato** a quantidade pendente daquele item, quando ela existe — e apaga o
  **pedido**.

Tudo em varredura: os registros do cálculo são percorridos até o fim, um a um, e um item que já
estava marcado como excluído é apagado direto, sem mexer na permissão.

[?] A recusa por **pedido do acumulado** (RN-08) e este trecho não fecham. A recusa barra o
cancelamento de qualquer cálculo que tenha um item de pedido acumulado, e é exatamente esse o
caso que o trecho da quantidade recebida atende: ou a recusa vale para outro caso, ou aquele
trecho ficou inalcançável por este caminho. Não escolho um dos dois lados. E, se ele for
alcançado, o cancelamento **subtrai** do acumulado a quantidade do item acumulado — o que só é
devolução se o cálculo a tinha somado antes; o que o cálculo grava nesse acumulado não está
nesta jornada. Pergunta ao site.

### RN-12 — O que o cancelamento marca

Ao terminar, a tela marca a requisição como **cancelada** — é assim que ela sai do estado
calculada e volta a poder ser calculada de novo — e mostra **Requisicao Cancelada** no campo de
situação. A requisição **não é apagada**: o que o cálculo tinha gerado é que sai do sistema.

[?] O caminho do cancelamento volta ao começo da varredura depois de marcar a requisição, e a
requisição continua lá. Lendo só o fonte, a mesma requisição é encontrada outra vez e a
varredura não tem fim. Se é o ambiente que encerra o processamento pela marca de reabertura da
tela, isso não está no fonte. Pergunta ao site se o cancelamento termina sozinho.

### RN-13 — Cada operação deixa auditoria

Cada gravação ou exclusão deixa um registro na auditoria **A010T**, com a tela, a operação, o
cadastro atingido, o órgão, a coordenadoria, o número de processo, a minha matrícula, a
estação, a data e a hora da sessão e os valores de antes e depois do registro. O cancelamento
tem **nove** pontos de gravação ou exclusão, e em **sete** deles o registro de auditoria é
montado **antes** da operação — abortando a auditoria, a operação não acontece.

[?] As duas exceções são a exclusão do **item acumulado do gênero** e a dos **itens do pedido
que já estavam marcados como excluídos**: são as duas únicas operações do cancelamento que não
deixam registro de auditoria. Se todas deveriam deixar, é pergunta ao site.

[?] Na auditoria da baixa do acumulado, o número de processo é o que a sessão traz no campo do
pedido — que esta jornada nunca preenche —, e não o número de processo que a tela monta para as
outras gravações. Se a intenção era o número de processo, aquele registro sai sem ele. Pergunta
ao site.

### RN-14 — O que a tela entrega à tela seguinte

Esta tela não encadeia para outra: quando a exclusão termina, ela **reabre a si mesma**, já sem
o cálculo, para que eu confira o resultado — a situação mostra **Requisicao Cancelada** — ou
informe outro cálculo.

---

## Cenários BDD

```gherkin
Funcionalidade: Cancelamento do cálculo do preparo da alimentação escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E056T

  Cenário: A tela mostra o cálculo que eu identifiquei
    Dado que existe requisição calculada para o órgão, a coordenadoria e a data de início do
      preparo
    Quando informo o órgão, a coordenadoria e a data de início e confirmo
    Então vejo o nome do órgão, o tipo de órgão e a data do sistema
    E vejo o limite do cálculo e o início e o limite do período de entrega, repostos da
      requisição
    E nada é gravado

  Cenário: A abertura da tela não grava nada
    Dado que estou na tela E056T
    Quando a tela abre
    Então o cursor fica no campo do órgão
    E nenhum pedido, item calculado, quantidade calculada ou item acumulado é apagado
    E nenhuma requisição, quantidade recebida ou permissão de entrega é alterada
    E nenhuma auditoria é gravada

  Cenário: Operação diferente de exclusão é recusada
    Dado que a passagem chega com uma operação diferente de EXC
    Quando confirmo a passagem
    Então vejo a mensagem "* Operacao nao disponivel. Use EXC *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Passagem com tela seguinte não é processada
    Dado que a passagem chega com a tela seguinte preenchida
    Quando confirmo a passagem
    Então sou encaminhado para essa tela
    E nada é processado nesta tela

  Cenário: Acesso à tela sem autorização
    Dado que o meu código de acesso não tem a tela E056T no seu cadastro
    Quando a tela tenta abrir
    Então vejo a mensagem "* Tela nao disponivel *"
    E nada é gravado

  Cenário: Exclusão não liberada para o meu código de acesso
    Dado que o meu código de acesso não tem a exclusão liberada nesta tela
    Quando confirmo a passagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Órgão não informado
    Dado que deixo o órgão em branco
    Quando confirmo a passagem
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor volta ao campo do órgão
    E nada é gravado

  Cenário: Órgão de outro vínculo é recusado
    Dado que eu tenho um órgão no vínculo da sessão
    Quando informo um órgão diferente
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E o cursor volta ao campo do órgão

  Cenário: Órgão não cadastrado
    Dado que informo um órgão que não existe no cadastro
    Quando confirmo a passagem
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão
    E nada é gravado

  Cenário: Órgão de outra coordenadoria é recusado
    Dado que o cadastro do órgão é de outra coordenadoria que não a minha
    Quando confirmo a passagem
    Então vejo a mensagem "<- Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é processado

  Cenário: A coordenadoria que eu digitei não decide nada
    Dado que informo uma coordenadoria diferente da do órgão cadastrado
    Quando confirmo a passagem
    Então a requisição é procurada pela coordenadoria do órgão, e não pela que eu digitei

  Cenário: Data de início do preparo não informada
    Dado que deixo o dia da data de início do preparo zerado
    Quando confirmo a passagem
    Então vejo a mensagem "* Informe a data de inicio do preparo *"
    E o cursor volta ao campo
    E nada é gravado

  Cenário: Código ou data não numérica é recusada
    Dado que informo um órgão, uma coordenadoria ou uma data que não é número
    Quando confirmo a passagem
    Então o valor é recusado antes de qualquer consulta
    E o cursor volta ao campo do órgão ou da data de início do preparo
    E nada é gravado

  Cenário: Requisição não cadastrada
    Dado que não existe requisição para o órgão, a coordenadoria e a data informados
    Quando confirmo a passagem
    Então vejo a mensagem "* Requisicao nao cadastrada *"
    E o cursor fica na data de início do preparo
    E nada é gravado

  Cenário: Requisição não calculada
    Dado que a requisição existe, mas sem a marca de calculada
    Quando confirmo a passagem
    Então vejo a mensagem "* Requisicao nao calculada *"
    E o cursor fica na data de início do preparo
    E nada é gravado

  Cenário: Pedido com quantidade recebida é recusado
    Dado que um item de um pedido do cálculo já tem quantidade recebida
    Quando confirmo a passagem
    Então vejo a mensagem "* Ja existe pedido com quantidade recebida *", com o número do
      pedido
    E o cursor volta à data de início do preparo
    E nada é apagado

  Cenário: Pedido do acumulado é recusado
    Dado que um item de um pedido do cálculo é do acumulado
    Quando confirmo a passagem
    Então vejo a mensagem "* Exc pedido <pedido> do acumulado <acumulado> *"
    E o cursor volta à data de início do preparo
    E nada é apagado

  Cenário: Aviso de pedidos já enviados ao fornecedor
    Dado que um dos pedidos do cálculo já foi enviado ao fornecedor
    Quando a tela pede a confirmação
    Então vejo o aviso "* Pedidos ja constam do arquivo do fornecedor *"
    E a pergunta da confirmação continua a ser feita

  Cenário: O cancelamento é pedido com confirmação
    Dado que o cálculo passou por todas as conferências
    Quando confirmo a passagem
    Então vejo a mensagem "* Confirma exclusao do calculo <S/N> ? *"
    E o cursor fica no campo da resposta
    E nada foi apagado ainda

  Cenário: Cancelamento do cálculo
    Dado que a tela pediu a confirmação
    E que respondo S com o órgão e a data de início do preparo ainda os mesmos
    Então a quantidade do item acumulado é baixada da quantidade recebida do acumulado
    E os itens acumulados, os itens calculados e as sete quantidades calculadas são apagados
    E os itens de cada pedido são apagados, devolvendo à permissão de entrega do contrato a
      quantidade pendente daquele item
    E os pedidos do cálculo são apagados
    E a requisição é marcada como cancelada, sem ser apagada
    E cada operação deixa um registro na auditoria A010T

  Cenário: Resposta diferente de S não apaga nada
    Dado que a tela pediu a confirmação
    Quando respondo N à pergunta da confirmação
    Então nada é apagado
    E o cálculo continua no sistema
    E a tela confere o cálculo de novo e volta a pedir a confirmação

  Cenário: A exclusão reabre a própria tela
    Dado que a exclusão terminou
    Quando a tela volta
    Então vejo a situação "Requisicao Cancelada"
    E continuo na tela E056T, podendo informar outro cálculo

  Cenário: A recusa não apaga nem grava nada
    Dado que a passagem foi recusada por alguma conferência
    Quando a tela termina a passagem
    Então nenhum pedido, item calculado, quantidade calculada ou item acumulado foi apagado
    E nenhuma requisição, quantidade recebida ou permissão de entrega foi alterada
    E nenhum registro de auditoria foi gravado
```
