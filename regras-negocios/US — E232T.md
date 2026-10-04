# US — E232T — Manter os pedidos de origem de um pedido acumulado, gênero por gênero

## Estória

Como **servidor da CRE**, quero **conferir e excluir, gênero por gênero, os pedidos de
origem que compõem um pedido acumulado**, para que **o acumulado fique apenas com os
pedidos que continuam valendo e o que saiu dele não se perca: passa a contar no pedido
auxiliar do acumulado, com a nota fiscal e os registros de cálculo ajustados**.

O pedido acumulado reúne, sob um único número, o que várias unidades pediram de um mesmo
gênero ao mesmo fornecedor. Quando um desses pedidos deixa de valer, é preciso tirá-lo do
acumulado sem perder o que ele já tinha: as quantidades, a nota fiscal que o acompanhava e
os cálculos daquele pedido vão para o pedido auxiliar do acumulado, que é o que continua
valendo para aquela unidade. Sem essa passagem, o acumulado conta a mais e o que chegou
pela nota some do sistema. A mesma tela serve para consultar o que compõe o acumulado e,
nesse caso, não grava nada.

## Contexto

Jornada S000M → E000M → E200M → E230M → E232T.

Ator: servidor de CRE — informa o órgão filho, o pedido acumulado com o ano da entrega, a
subclasse e o gênero, confere os pedidos de origem daquele gênero e exclui os que não
valem mais.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Os três passos do meio — E000M, E200M e E230M — são menus: não gravam nada e não deixam
pedido, nota nem valor para esta tela, que busca tudo nos cadastros. Da sessão ela usa a
matrícula, o código de acesso, o privilégio, o tipo de órgão, a coordenação regional
escolar, o órgão filho, a estação e a data e a hora do sistema.

Esta tela **abre outra**: quando o campo de indicação da passagem vem preenchido, ela
entrega o pedido acumulado à tela dos gêneros do acumulado (`E231T`), que abre em consulta
— é a regra RN-15. Quem chega aqui pela tela dos gêneros recebe dela o pedido e o gênero em
contexto, e é isso que decide o que esta tela mostra ao abrir (RN-09).

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela trabalha um gênero de um pedido acumulado do órgão filho

A tela identifica o pedido acumulado pelo **número do pedido** (6 dígitos) com o **ano da
entrega** (4) — os dois formam a chave do acumulado —, pelo **órgão filho** (8 dígitos) com
a **coordenação regional escolar** (2) e por **subclasse** (2) e **gênero** (5). Fora
disso, o cabeçalho traz o número e o ano do **pedido auxiliar do acumulado**, que o
servidor pode informar, e mostra o período do pedido (dia, mês e ano de início e de
limite), o tipo de contrato, o cartão e a situação.

### RN-02 — A tela só atende consulta e alteração; sem operação informada, adota a consulta

A operação informada só pode ser **consulta** ou **alteração**. Qualquer outra é recusada
com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta ao campo da
operação, antes de qualquer leitura do órgão, do pedido ou do gênero. Chegando sem
operação informada — como acontece quando a tela é aberta pelo menu —, ela adota a
consulta. Quando a tela é aberta para passar o pedido adiante, a operação vai forçada à
consulta (RN-15).

[?] A recusa manda usar **ALT** e **CON**, mas a guarda compara a operação com os códigos
internos de alteração e de consulta, que são outros. Ou o formulário traduz o que o
servidor digita, ou a mensagem indica valores que a tela não aceita — e, neste segundo
caso, a alteração e a exclusão inteiras ficam inalcançáveis por este caminho. Pergunta ao
site; não concluo qual dos dois.

### RN-03 — A alteração exige ter consultado antes o mesmo pedido e o mesmo gênero

Para alterar, o pedido e o gênero informados têm de ser **os mesmos da última consulta**: a
tela compara a coordenação regional escolar, a chave do pedido acumulado, a subclasse e o
gênero com o que ela guardou da consulta anterior. Não batendo, a recusa é
**\* Consulte antes de atualizar \***, com o cursor de volta ao campo da operação, e nada é
lido adiante. É por isso que a conferência do órgão, do pedido e do gênero roda no caminho
da consulta — e é ela que carrega o que a alteração vai usar.

### RN-04 — O órgão filho é obrigatório e passa por quatro conferências

O órgão filho é exigido: em branco, a recusa é **\* Informe o orgao \***, com o cursor no
campo. Informado, ele tem de estar **cadastrado** (senão **\* Orgao nao cadastrado \***),
o cadastro não pode estar marcado como excluído — a tela segue procurando —, tem de ser do
**tipo de órgão da sessão** (senão **\* Orgao nao pertence a esta secretaria \***) e,
quando o vínculo do servidor tem coordenação regional escolar, tem de ser **daquela
coordenação** (senão **\* Usuario sem acesso ao grupo deste orgao \***). Em todas as
recusas o cursor volta ao campo do órgão filho e nada é lido adiante.

### RN-05 — O pedido acumulado tem de existir e estar marcado como acumulado

O número do pedido acumulado é exigido — em branco, a recusa é
**\* Informe o numero do pedido \***, com o cursor no campo do número. Informado, o pedido
tem de estar **cadastrado** para aquela coordenação (senão
**\* Pedido nao cadastrado \***) e tem de estar marcado como **acumulado consolidado**: o
pedido que não está marcado como acumulado é recusado com **\* Pedido nao acumulado \***, o
acumulado ainda em digitação com **\* Pedido acumulado digitado \***, e o **auxiliar
calculado** do acumulado com **\* Pedido auxiliar do acumulado calculado \***. Em todas as
recusas o cursor volta ao número do pedido e nada é lido adiante.

### RN-06 — O pedido tem de ser do órgão filho do servidor

Quando o vínculo do servidor tem órgão filho, o pedido acumulado tem de ser **daquele
órgão**: sendo de outro, a recusa é **\* Pedido de outro orgao \***, com o cursor de volta
ao campo do órgão filho, e nada é lido adiante.

### RN-07 — O gênero é obrigatório, tem de estar cadastrado e tem de constar do pedido

A subclasse e o gênero identificam o item do acumulado. Em branco, a recusa é
**\* Informe o genero \***, com o cursor no campo; informados, o gênero tem de estar
**cadastrado** para aquela subclasse e para o período do pedido (senão
**\* Genero nao cadastrado \***) e tem de **constar do pedido acumulado** (senão
**\* Genero nao cadastrado neste pedido \***). Nas três recusas nada é lido adiante.

### RN-08 — O fornecedor e o operador são mostrados, mas não recusam

O fornecedor do pedido é lido apenas para a tela mostrar a **razão social**; o operador do
pedido, para mostrar o **nome** — o operador zerado nem é procurado. Nenhum dos dois é
exigido e nenhum dos dois recusa a passagem quando não é encontrado: o campo simplesmente
fica em branco. A descrição resumida do gênero vem do cadastro do gênero e o tipo de
contrato, do pedido: são apenas mostrados. A situação do pedido aparece como **Aprovado**,
ou como **Fechado** quando o pedido está marcado como fechado.

### RN-09 — Ao abrir com um pedido em contexto, a tela repõe o que a tela anterior deixou

A tela pode ser aberta com um **pedido já em contexto** — é o que acontece quando o
servidor chega pela tela dos gêneros do acumulado: esta repõe no cabeçalho o que o contexto
trouxer — o pedido acumulado, o órgão filho, a coordenação regional escolar, o fornecedor
com a razão social, o operador com o nome, o período, o cartão, o tipo de contrato, a
situação, a subclasse, o gênero e a descrição resumida do gênero — e monta a grade a partir
do gênero que veio, sem exigir digitação. Sem nada em contexto — como quando é aberta pelo
menu —, ela abre em branco, com a operação em consulta, e espera que o servidor digite a
chave. Quando o gênero em contexto não tem nenhum pedido no acumulado, a tela avisa
**\* Nao existem pedidos cadastrados \*** e não mostra linha nenhuma. Antes de conferir o
que o servidor digitou, a tela apaga **treze campos de resultado** — a descrição do órgão da
sessão, a data do sistema, a descrição do órgão filho, a razão social do fornecedor, o nome
do operador, a descrição da situação do pedido, a descrição resumida do gênero, o código do
órgão do pedido, a sigla do órgão, o número da nota fiscal, a data de início, a marca do
cartão e a situação do pedido de origem —, de modo que uma mensagem recusada não deixa na
tela o resultado da mensagem anterior.

### RN-10 — A grade tem dez linhas e onze informações por linha, e os totais do gênero

A grade mostra até **dez** pedidos do gênero no acumulado, uma linha por registro. Cada
linha traz **onze** informações: o número do pedido e o ano da entrega, o código e a sigla
do órgão do pedido, a nota fiscal que o acompanha, a data de início, a marca do cartão, a
situação, a **quantidade pedida**, a **quantidade recolhida** e o campo da **ação**. Das
onze, cinco são digitáveis — o número do pedido, o ano, as duas quantidades e a ação —; as
outras seis vêm do cadastro. Fora da grade a tela mostra o **total pedido** e o **total
recolhido** do gênero no acumulado, somados registro a registro.

[?] O acervo não diz como o formulário rotula os campos da linha: os rótulos que a tela usa
para eles são as próprias siglas internas do programa, e o acervo não diz o que elas abrem.
Pergunta ao site.

[?] Uma das linhas da grade aparece sem nota fiscal. A leitura da nota é saltada quando o
registro é o do próprio pedido auxiliar do acumulado, e o acervo não diz se é para essa linha
ficar sem nota de propósito. Pergunta ao site.

### RN-11 — Só a linha marcada com a ação de exclusão é excluída

A ação é por linha, não pela tela. Só a linha marcada com a ação de **exclusão** entra no
caminho da exclusão: linha sem ação, ou com ação diferente, é ignorada — não é excluída e
não produz mensagem. A mesma tela trata mais de uma linha na mesma mensagem, uma a uma, na
ordem da grade.

### RN-12 — A exclusão tira o pedido do acumulado e passa o que ele tinha ao auxiliar

Confirmada a exclusão de uma linha, a tela tira aquele **pedido de origem** do acumulado:
exclui o item daquele pedido no gênero, a **nota fiscal** que o acompanhava e os
**registros de cálculo** daquele pedido; se o pedido não tiver mais nenhum item, o próprio
pedido é excluído — restando itens, a situação dele é refeita (fechado, se algum item
continua fechado; senão aprovado) e corrigida. O que o pedido excluído tinha passa a contar
no **pedido auxiliar do acumulado** daquele gênero, com a nota fiscal correspondente: a
linha do auxiliar e a nota dele recebem as quantidades e os valores do que saiu, e são
**criadas** quando ainda não existem. A quantidade recolhida do registro de entrega daquela
nota também é ajustada. Cada operação — exclusão ou alteração — deixa o seu **registro de
auditoria**.

[?] A direção das contas não fecha. O que sai é **somado** ao que já está no pedido
auxiliar e na nota dele, como se a exclusão devolvesse ao auxiliar; e a quantidade
recolhida do registro de entrega é refeita como a diferença entre a quantidade recolhida do
item excluído e a que já estava naquele registro, o que zera quando as duas são iguais. Ou
o que sai é devolvido ao auxiliar e a soma é intencional, ou a soma deveria ser subtração e
a conta do registro de entrega está invertida. Pergunta ao site; não escolho um dos dois.

[?] A tela **cria** o pedido auxiliar do acumulado — e o item e a nota dele — quando não os
encontra, com as quantidades do pedido excluído. O acervo não diz se a exclusão deve mesmo
criar esses registros, ou se eles deveriam existir desde a consolidação do acumulado.
Pergunta ao site.

### RN-13 — A exclusão é recusada em três casos

A exclusão é recusada, sempre com o cursor de volta ao campo da ação da linha e sem gravar
nada: quando o pedido da linha é o **auxiliar do acumulado** (**\* Nao exclua.Pedido
auxiliar do acumulado \***); quando aquele pedido **não consta do acumulado** naquele
gênero (**\* Pedido nao cadastrado neste acumulado \***); e quando a **entrega daquele
pedido já foi confirmada** pelo órgão — a nota traz o número com que o órgão a confirmou
(**\* Nao exclua. Entrega confirmada \***).

### RN-14 — A consulta não grava nada

Confirmada a consulta, a tela encerra a passagem sem excluir, sem criar, sem alterar e sem
deixar registro de auditoria. Também não grava quando a passagem é recusada: qualquer
recusa marca a passagem de modo que a exclusão daquela linha não acontece.

### RN-15 — A tela entrega o pedido acumulado à tela dos gêneros

Quando o campo de indicação da passagem vem preenchido, a tela não exclui nada: ela confere
o pedido acumulado, a operação vai forçada a **consulta**, a subclasse e o gênero são
zerados no que passa adiante, e a tela entrega o pedido à tela dos gêneros do acumulado
(`E231T`). A tela seguinte abre em **consulta** e mostra os gêneros daquele pedido
acumulado, sem gênero escolhido — é o caminho de volta de quem veio de lá.

[?] O acervo não diz como o formulário apresenta esse campo de indicação da passagem — o
rótulo dele não está no acervo — nem se ele é digitado pelo servidor ou preenchido pela
tela. Pergunta ao site.

### RN-16 — Os campos numéricos passam pela edição numérica

Os **vinte e três** campos numéricos do cabeçalho e da grade passam pela edição numérica
antes de qualquer conferência de negócio; o que chega em branco é tratado como zero. As
quantidades — a pedida e a recolhida de cada linha e os dois totais — são as únicas
conferidas com **três casas decimais**.

[?] O que o servidor vê quando a digitação é recusada não se conclui desta tela: a rotina
que faz a edição não faz parte do acervo lido. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os pedidos de origem de um pedido acumulado, gênero por gênero

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenação regional escolar e o órgão filho
    E tenho acesso à tela E232T

  Cenário: Consultar os pedidos de origem de um gênero do acumulado
    Dado que informo o órgão filho, o pedido acumulado com o ano da entrega, a subclasse e o gênero
    Quando confirmo a consulta
    Então vejo o cabeçalho do pedido acumulado e as linhas dos pedidos de origem daquele gênero
    E vejo o total pedido e o total recolhido daquele gênero
    E nada é gravado

  Cenário: Excluir um pedido de origem do acumulado
    Dado que consultei o pedido acumulado e o gênero
    E que a linha traz o pedido de origem e a ação de exclusão
    Quando confirmo a alteração
    Então o item daquele pedido no gênero, a nota fiscal e os registros de cálculo dele são excluídos
    E o que ele tinha passa a contar no pedido auxiliar do acumulado
    E a exclusão deixa o seu registro de auditoria

  Cenário: O pedido de origem que não tem mais nenhum item é excluído
    Dado que consultei o pedido acumulado e o gênero
    E que o pedido de origem não tem itens em nenhum outro gênero
    Quando excluo a linha daquele gênero
    Então aquele pedido deixa de existir

  Cenário: O pedido de origem que ainda tem itens continua, com a situação refeita
    Dado que consultei o pedido acumulado e o gênero
    E que o pedido de origem tem itens em outro gênero
    Quando excluo a linha daquele gênero
    Então o pedido continua cadastrado
    E a situação dele é refeita e corrigida

  Cenário: O pedido auxiliar do acumulado é criado quando ainda não existe
    Dado que consultei o pedido acumulado e o gênero
    E que aquele gênero ainda não tem o pedido auxiliar do acumulado
    Quando excluo um pedido de origem daquele gênero
    Então o pedido auxiliar do acumulado é criado com o que saiu

  Cenário: A consulta não grava nada
    Dado que consultei o pedido acumulado e o gênero
    Quando a tela termina a passagem
    Então nenhum registro é criado, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: A exclusão recusada não grava nada
    Dado que consultei o pedido acumulado e o gênero
    Quando a minha exclusão é recusada
    Então nenhum registro daquela linha é criado, alterado ou excluído

  Cenário: Operação diferente de consulta e alteração
    Quando confirmo com uma operação que não é consulta nem alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido adiante

  Cenário: Alteração sem ter consultado antes
    Dado que não consultei antes aquele pedido e aquele gênero
    Quando confirmo a alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo da operação
    E nada é lido adiante

  Cenário: Linha sem a ação de exclusão não é excluída
    Dado que consultei o pedido acumulado e o gênero
    Quando confirmo deixando uma linha sem ação, ou com ação diferente
    Então aquela linha não é excluída
    E nenhuma mensagem é mostrada por causa dela

  Cenário: Órgão filho não informado
    Quando confirmo sem informar o órgão filho
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor volta ao campo do órgão filho

  Cenário: Órgão filho não cadastrado
    Quando informo um órgão filho que não está cadastrado
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão filho
    E nada é lido adiante

  Cenário: Órgão filho de outra secretaria
    Quando informo um órgão filho que não é do tipo de órgão da minha sessão
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E o cursor volta ao campo do órgão filho

  Cenário: Órgão filho fora da minha coordenação
    Dado que o meu vínculo tem coordenação regional escolar
    Quando informo um órgão filho de outra coordenação
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor volta ao campo do órgão filho

  Cenário: Pedido acumulado não informado
    Dado que informei o órgão filho
    Quando confirmo sem informar o número do pedido acumulado
    Então vejo a mensagem "* Informe o numero do pedido *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido acumulado não cadastrado
    Dado que informei o órgão filho
    Quando informo um pedido que não está cadastrado
    Então vejo a mensagem "* Pedido nao cadastrado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido que não é acumulado
    Dado que informei o órgão filho
    Quando informo um pedido que não está marcado como acumulado
    Então vejo a mensagem "* Pedido nao acumulado *"

  Cenário: Acumulado ainda em digitação
    Dado que informei o órgão filho
    Quando informo um pedido acumulado ainda em digitação
    Então vejo a mensagem "* Pedido acumulado digitado *"

  Cenário: Auxiliar calculado do acumulado
    Dado que informei o órgão filho
    Quando informo o auxiliar calculado de um acumulado
    Então vejo a mensagem "* Pedido auxiliar do acumulado calculado *"

  Cenário: Pedido acumulado de outro órgão
    Dado que o meu vínculo tem órgão filho
    Quando informo um pedido acumulado de outro órgão filho
    Então vejo a mensagem "* Pedido de outro orgao *"
    E o cursor volta ao campo do órgão filho

  Cenário: Gênero não informado
    Dado que informei o órgão filho e o pedido acumulado
    Quando confirmo sem informar a subclasse e o gênero
    Então vejo a mensagem "* Informe o genero *"

  Cenário: Gênero não cadastrado
    Dado que informei o órgão filho e o pedido acumulado
    Quando informo um gênero que não está cadastrado para aquela subclasse e aquele período
    Então vejo a mensagem "* Genero nao cadastrado *"
    E nada é lido adiante

  Cenário: Gênero que não consta do pedido acumulado
    Dado que informei o órgão filho e o pedido acumulado
    Quando informo um gênero que não consta daquele pedido
    Então vejo a mensagem "* Genero nao cadastrado neste pedido *"
    E nada é lido adiante

  Cenário: Gênero sem nenhum pedido no acumulado
    Dado que cheguei pela tela dos gêneros do acumulado com um gênero selecionado
    Quando aquele gênero não tem nenhum pedido no acumulado
    Então vejo a mensagem "* Nao existem pedidos cadastrados *"
    E nenhuma linha é mostrada

  Cenário: Excluir o pedido auxiliar do acumulado
    Dado que consultei o pedido acumulado e o gênero
    E que a linha traz o pedido auxiliar do acumulado
    Quando confirmo a exclusão daquela linha
    Então vejo a mensagem "* Nao exclua.Pedido auxiliar do acumulado *"
    E o cursor volta ao campo da ação da linha
    E nada é gravado

  Cenário: Excluir um pedido que não consta do acumulado
    Dado que consultei o pedido acumulado e o gênero
    E que a linha traz um pedido que não consta daquele acumulado naquele gênero
    Quando confirmo a exclusão daquela linha
    Então vejo a mensagem "* Pedido nao cadastrado neste acumulado *"
    E o cursor volta ao campo da ação da linha
    E nada é gravado

  Cenário: Excluir um pedido com a entrega já confirmada
    Dado que consultei o pedido acumulado e o gênero
    E que a entrega daquele pedido de origem já foi confirmada pelo órgão
    Quando confirmo a exclusão daquela linha
    Então vejo a mensagem "* Nao exclua. Entrega confirmada *"
    E o cursor volta ao campo da ação da linha
    E nada é gravado

  Cenário: Fornecedor ou operador não cadastrado não recusa a passagem
    Dado que consultei o pedido acumulado e o gênero
    Quando o fornecedor ou o operador do pedido não está cadastrado
    Então a tela segue sem mostrar a razão social ou o nome
    E nenhuma mensagem de recusa é mostrada por causa disso

  Cenário: A grade tem dez linhas e onze informações por linha
    Dado que abri a tela E232T com um pedido acumulado e um gênero
    Então vejo até dez linhas
    E cada linha tem o número do pedido, o ano da entrega, o código e a sigla do órgão,
      a nota fiscal, a data de início, a marca do cartão, a situação, a quantidade pedida,
      a quantidade recolhida e a ação
    E vejo o total pedido e o total recolhido do gênero

  Cenário: A recusa não deixa o resultado anterior na tela
    Dado que uma confirmação foi recusada
    Quando a tela me mostra a mensagem
    Então os campos de resultado da mensagem anterior foram apagados
    E a tela repõe a descrição do órgão da sessão e a data do sistema

  Cenário: A tela entrega o pedido acumulado à tela dos gêneros
    Dado que abri a tela E232T com um pedido acumulado no contexto
    Quando confirmo com o campo de indicação da passagem preenchido
    Então o pedido acumulado é entregue à tela E231T
    E a tela E231T abre em consulta
    E nenhum gênero vai escolhido
    E nada é gravado

  Cenário: Campo numérico recusado pela edição
    Quando informo, em um campo numérico da tela, algo que não é número
    Então a tela recusa antes de qualquer conferência de negócio
    E o que estava em branco é tratado como zero
```
