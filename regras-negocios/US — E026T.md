# US — E026T — Escolha do pedido de alimentação escolar fechado do grupo

## Estória

Como **servidor de CRE**, quero **ver os pedidos de alimentação escolar já fechados
do meu grupo e escolher um deles**, para que **eu chegue ao pedido certo sem
depender de saber de cor o número e o ano da entrega**.

O pedido de alimentação escolar é identificado por um número de seis dígitos junto
com o ano da entrega, em quatro — dez dígitos que ninguém decora. Depois de fechado,
o pedido não se corrige mais: o que resta é consultá-lo, e é por esta lista que se
chega até ele. No dia a dia da coordenadoria há vários pedidos fechados ao mesmo
tempo, de escolas e fornecedores diferentes: sem a lista, quem consulta teria de
conhecer o número exato, e o engano só apareceria depois de a tela do pedido já
estar aberta.

## Contexto

Jornada S000M → E000M → E010M → E026T.

Ator: servidor de CRE — informa a coordenadoria regional escolar, vê os pedidos
fechados do grupo e marca o pedido que vai abrir na tela seguinte.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Da sessão a tela usa a coordenadoria regional escolar e o órgão filho do vínculo,
além da descrição do órgão da sessão e da data do sistema para o cabeçalho. A tela é
do tipo transação e não termina nela: a linha marcada a leva para a tela do pedido
(`E027T`), e a passagem está descrita em RN-08.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela não inclui, não altera e não exclui nada

A tela é de consulta. Para montar a lista e escolher o pedido ela lê **seis
cadastros** — o registro das telas, o cadastro dos pedidos, o cadastro dos
fornecedores, o cadastro dos órgãos, o cadastro dos operadores e o cadastro das
coordenadorias regionais escolares da secretaria — e não escreve em nenhum deles:
nada é criado, alterado ou apagado. Ela nem declara o cadastro de auditoria, porque
não há alteração a registrar. As conferências de acesso leem ainda o cadastro do
funcionário e o cadastro das autorizações do código de acesso.

Os cadastros são dimensionados para: pedidos **10 milhões**; órgãos **12 mil**;
fornecedores **10 mil**; telas **2 mil**; coordenadorias **1 mil**; operadores
**100**. São capacidades — o máximo esperado no dimensionamento —, não volumes
cadastrados.

### RN-02 — Ao abrir, a tela propõe a consulta e a coordenadoria do vínculo

Ao ser aberta, a tela põe a consulta no campo da operação e preenche a coordenadoria
regional escolar com a do vínculo da sessão; quando o vínculo não traz coordenadoria,
o campo fica em branco, para o servidor informar e, sem ela, a lista nem é
percorrida. No cabeçalho ela mostra a descrição do órgão da sessão e a data do
sistema, e deixa o cursor no campo da coordenadoria. Abrir a tela não grava nem apaga
nada.

[?] Nenhum programa desta jornada preenche a coordenadoria do vínculo: o que existe
no acervo são reinicializações e duas telas de outros módulos. Se isso valer no site,
a coordenadoria nunca vem proposta, a conferência de grupo (RN-04) não tem como
barrar ninguém e a lista depende inteiramente do que o servidor digitar. Pergunta ao
site; não escolho um dos dois lados.

### RN-03 — A lista: os pedidos fechados do grupo, até treze por vez

Informada a coordenadoria, a tela percorre os pedidos do grupo na ordem da coleção —
por tipo de órgão, coordenadoria, situação e, dentro dela, do ano e do número mais
antigos para os mais novos —, descartando os pedidos marcados como excluídos, e
mostra até **13** pedidos cuja situação é **fechado**. De cada pedido a lista traz o
número, o ano da entrega, o órgão filho, o fornecedor e a sua razão social, o cartão,
o início e o limite do período de entrega e a marca da linha; um asterisco marca as
linhas de um pedido acumulado. Quando o grupo não tem nenhum pedido fechado, a recusa
é **\* Grupo sem pedidos aprovados - fechados \***, e nada é gravado.

A lista começa no ano em que o grupo tem pedido: aberta a tela pela primeira vez, ela
procura o pedido do grupo no ano do sistema e adota o ano achado como ponto de
partida; depois disso continua de onde parou, guardado o par número/ano do último
pedido mostrado. Esse par fica fora das linhas: a tela mesma o preenche e o servidor
também pode informá-lo, para posicionar a lista; o pedido informado é conferido no
grupo antes de a posição ser adotada, e o que não existe é descartado em silêncio.

[?] Nada no fonte diz o que acontece quando o grupo tem mais pedidos fechados do que
cabem nas 13 linhas: a tela pede a continuação da lista e a conferência de acesso
recusa a requisição da segunda página (**\* Acesso a pagina 2 negado \***). Ou os
grupos do site nunca passam de 13 pedidos fechados, ou o resto da lista não é
alcançável. Pergunta ao site; não escolho um dos dois lados.

[?] O par número/ano de fora das linhas posiciona a lista, mas quem decide adotá-lo é
uma comparação entre dois valores que a própria tela guardou de uma digitação para a
seguinte, e não entre o que o servidor digitou e o que está na linha marcada: em que
momento a lista é reposicionada — e o que o servidor vê enquanto isso — não se
conclui do fonte. Pergunta ao site.

### RN-04 — A coordenadoria informada tem de ser a do vínculo

Quando o vínculo da sessão traz uma coordenadoria regional escolar e o campo
informado traz outra, a tela recusa com **\* Usuario sem acesso a este grupo \***,
com o cursor de volta no campo da coordenadoria, e nada é gravado. A conferência só
vale quando a sessão traz coordenadoria.

### RN-05 — Sem coordenadoria no vínculo, a coordenadoria tem de pertencer à secretaria

Quando o vínculo da sessão não traz coordenadoria, a informada é procurada no
cadastro das coordenadorias da secretaria. Não existindo para o tipo de órgão da
sessão, a recusa é **\* Grupo nao pertence a esta secretaria \***, com o cursor no
campo da coordenadoria, e nada é gravado. Achada, ela é adotada como a coordenadoria
da consulta.

[?] A conferência é dispensada quando a coordenadoria informada é igual à que a tela
já tinha — inclusive quando as duas estão zeradas, isto é, nada informado. Nesse caso
a tela segue para a escolha sem conferir grupo nenhum, e não se conclui do acervo o
que o servidor vê. Pergunta ao site.

### RN-06 — A linha marcada tem de estar preenchida

A escolha é feita na linha: o servidor marca a linha e informa nela o número do
pedido e o ano da entrega. Linha marcada e com o número e o ano zerados é recusada
com **\* A linha deve estar preenchida \***, com o cursor na marca daquela linha, e
nada é gravado. Linha não marcada não faz nada: a passagem termina sem levar a lugar
nenhum e a tela continua onde estava.

### RN-07 — O pedido escolhido tem de ser do órgão do vínculo

Achado o pedido da linha marcada, a tela o recusa quando ele é de um órgão filho
diferente do órgão do vínculo da sessão: **\* Usuario sem acesso a este orgao \***,
com o cursor na marca daquela linha, e nada é gravado. A conferência só vale quando o
vínculo da sessão carrega um órgão filho.

[?] A tela procura o pedido marcado pela secretaria, pela coordenadoria e pelo
número, mas não recusa quando não o acha: segue com os dados que ficaram da leitura
anterior, de modo que um número que não existe pode ser levado adiante como se
existisse. Ou a escolha deveria recusar, ou a procura serve para outra coisa. Pergunta
ao site; não escolho um dos dois lados.

[?] A procura do pedido marcado também não é limitada à situação fechado, embora a
lista seja: um pedido que ainda não fechou pode ser levado à tela seguinte. Pergunta
ao site.

### RN-08 — A escolha entrega o pedido à tela do pedido, em consulta

Escolhida a linha, a tela abre a `E027T` — a tela do pedido — e deixa para ela, na
área de trabalho, o pedido escolhido: a coordenadoria, o número de dez dígitos do
pedido, o órgão filho, o fornecedor e a razão social, o operador e o seu nome, o
cartão, o dia, o mês e o ano do início e do limite do período de entrega, e a tela que
a chamou. Deixa também, junto com isso, a operação **consulta**.

É essa operação que decide o modo da tela seguinte: aberta por esta passagem, a tela
do pedido abre com o pedido já carregado, em consulta; aberta pelo menu, sem o pedido
em contexto, ela abre em consulta também, mas sem pedido nenhum. A tela percorre as
linhas na ordem em que aparecem e segue com a **primeira** que estiver marcada.

### RN-09 — A tela só atende na consulta

Ao abrir, a tela escreve a consulta no campo da operação. Na passagem da escolha, a
conferência de rota recusa a inclusão, a alteração e a exclusão para esta tela — ela
não as faz — e recusa qualquer operação que não seja a consulta, sempre com
**\* Operacao nao disponivel \***, antes de a tela olhar o grupo ou a linha. A
conferência da tela, que vem depois, não exige permissão de operação alguma, porque
não há o que gravar. Nada é mostrado, escolhido ou gravado sem passar por ela.

[?] A operação em branco passa pelas duas conferências e a escolha chega a acontecer;
como a tecla do terminal chega escrita nesse campo não se conclui do acervo. Pergunta
ao site.

[?] A tela devolve à rota o campo do código da próxima tela, e só depois o examina: se
ele chegar preenchido, a rota já desviou a transação para essa tela e a passagem
termina — a guarda da própria tela, nesse caso, nunca é alcançada. Quem preenche esse
campo fora desta tela não está no acervo. Pergunta ao site.

### RN-10 — Os campos numéricos passam por edição numérica antes das conferências

Antes de qualquer conferência de negócio, os **cinco** campos numéricos — a
coordenadoria regional escolar, o par número/ano que a tela guarda fora das linhas, o
número do pedido e o ano da entrega da linha — passam por edição numérica, e o campo
em branco é tratado como zero. A operação, a tela de destino e a marca da linha não
passam por essa edição.

[?] A tela só sabe devolver o cursor à coordenadoria e ao par número/ano de fora das
linhas; um erro de digitação no número ou no ano da linha marcada não tem posição de
cursor definida, e o que o servidor vê nesse caso não se conclui da tela. Pergunta ao
site.

### RN-11 — Nada é gravado nem escolhido sem a conferência de sessão, de tela e de acesso

Na abertura, a tela confere que o servidor está na **estação em que a sessão foi
aberta** (em outra, o acesso é encerrado e a sessão volta à entrada), que a tela está
registrada (senão **\* Tela nao disponivel \***), que ela pertence ao módulo da
sessão e que o código de acesso do servidor alcança a tela (senão
**\* Acesso negado para esta matricula \***). Também é recusada a requisição da
segunda página da tela (**\* Acesso a pagina 2 negado \***). Na passagem da escolha a
rota e o acesso à tela são conferidos de novo. Sem passar por tudo, nada é gravado e a
tela do pedido não abre.

### RN-12 — A recusa não grava nada e não leva a lugar nenhum

Cada recusa encerra a passagem antes de qualquer gravação e antes da abertura da tela
do pedido: nenhum dos seis cadastros é tocado e nenhum registro de auditoria é
incluído. Uma recusa registrada numa linha impede que as linhas seguintes sejam
examinadas na mesma passagem. A simples abertura da tela também não escreve nem apaga
nada.

---

## Cenários BDD

```gherkin
Funcionalidade: Escolha do pedido de alimentação escolar fechado do grupo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E026T

  Cenário: A tela lista os pedidos fechados do grupo
    Dado que a minha coordenadoria tem pedidos fechados
    Quando abro a tela E026T
    Então o campo da coordenadoria vem com a coordenadoria do meu vínculo
    E vejo até 13 pedidos do grupo, com o número, o ano da entrega, o órgão filho, o
      fornecedor e a sua razão social, o cartão, o início e o limite do período de
      entrega e a marca da linha
    E um asterisco marca as linhas de um pedido acumulado
    E os pedidos excluídos não aparecem
    E nada é gravado

  Cenário: O grupo não tem pedidos fechados
    Dado que não há pedido fechado para a minha coordenadoria
    Quando abro a tela E026T
    Então vejo "* Grupo sem pedidos aprovados - fechados *"
    E nada é gravado

  Cenário: A abertura propõe a consulta e a coordenadoria do vínculo
    Dado que o meu vínculo carrega uma coordenadoria regional escolar
    Quando abro a tela E026T
    Então o campo da operação vem com a consulta
    E o campo da coordenadoria vem com a coordenadoria do meu vínculo
    E vejo a descrição do órgão da minha sessão e a data do sistema
    E o cursor fica no campo da coordenadoria
    E nada é gravado nem apagado

  Cenário: Sem coordenadoria no vínculo, o campo fica para eu informar
    Dado que o meu vínculo não carrega coordenadoria regional escolar
    Quando abro a tela E026T
    Então o campo da coordenadoria fica em branco, para eu informar
    E a lista só é percorrida depois que eu informo a coordenadoria do meu grupo
    E nada é gravado nem apagado

  Cenário: A lista começa no ano em que o grupo tem pedido
    Dado que o grupo tem pedidos fechados de mais de um ano
    Quando abro a tela E026T
    Então a lista parte do ano do sistema, quando o grupo tem pedido nele
    E continua de onde parou a cada consulta seguinte, pelo par número/ano do último
      pedido mostrado
    E nada é gravado

  Cenário: A posição informada fora das linhas é conferida antes de ser adotada
    Dado que a lista mostra os pedidos fechados do meu grupo
    Quando informo fora das linhas o número de um pedido e o seu ano da entrega
    Então a tela confere esse pedido no grupo
    E, não o achando, descarta a posição informada sem me avisar
    E nada é gravado

  Cenário: Escolher um pedido e ir para a tela do pedido
    Dado que a lista mostra os pedidos fechados do meu grupo
    Quando marco a linha de um pedido, informo nela o número do pedido e o ano da
      entrega e confirmo
    Então a tela E027T abre com esse pedido já carregado
    E ela abre na operação de consulta
    E nada é gravado por esta tela

  Cenário: A primeira linha marcada é a que segue
    Dado que marquei duas linhas da lista
    Quando confirmo
    Então a tela leva adiante a primeira linha marcada, na ordem em que ela aparece
    E a segunda linha marcada não é examinada nesta passagem

  Cenário: A linha não marcada não faz nada
    Dado que não marquei nenhuma linha da lista
    Quando confirmo
    Então a passagem termina sem levar a lugar nenhum
    E a tela do pedido não abre
    E nada é gravado

  Cenário: Coordenadoria que não é a do servidor
    Dado que o vínculo da minha sessão traz uma coordenadoria regional escolar
    Quando confirmo uma coordenadoria diferente
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Coordenadoria de outra secretaria
    Dado que o vínculo da minha sessão não traz coordenadoria regional escolar
    Quando informo uma coordenadoria que não existe para a secretaria da minha sessão
    Então vejo "* Grupo nao pertence a esta secretaria *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: A linha marcada e sem o número e o ano
    Dado que marquei uma linha da lista
    Quando confirmo com o número do pedido e o ano da entrega zerados
    Então vejo "* A linha deve estar preenchida *"
    E o cursor fica na marca daquela linha
    E nada é gravado

  Cenário: Pedido de outro órgão
    Dado que o vínculo da minha sessão carrega um órgão filho
    Quando marco a linha de um pedido de outro órgão e confirmo
    Então vejo "* Usuario sem acesso a este orgao *"
    E o cursor fica na marca daquela linha
    E nada é gravado

  Cenário: A tela só atende na consulta
    Dado que estou na tela E026T
    Quando a transação chega com a operação de inclusão, de alteração ou de exclusão
    Então vejo "* Operacao nao disponivel *"
    E a tela não olha o grupo nem a linha
    E nada é gravado

  Cenário: Operação diferente da consulta é recusada antes da tela
    Dado que estou na tela E026T
    Quando a transação chega com uma operação que não é a consulta
    Então vejo "* Operacao nao disponivel *"
    E a conferência da própria tela não chega a ser feita
    E nada é gravado

  Cenário: Os campos numéricos passam por edição numérica antes das conferências
    Dado que estou na tela E026T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências de negócio
    E a digitação que não é número é barrada antes das conferências de negócio

  Cenário: Nada é escolhido nem gravado sem a conferência de sessão, de tela e de acesso
    Dado que estou na tela E026T
    Quando a conferência da estação, do registro da tela, do módulo ou do código de
      acesso não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *" ou
      "* Acesso a pagina 2 negado *"
    E nada é gravado
    E, se a estação não for a da minha sessão, o acesso é encerrado

  Cenário: A recusa não grava nada e não leva à tela do pedido
    Dado que estou na tela E026T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então nenhum pedido, fornecedor, órgão, operador, tela ou coordenadoria foi
      criado, alterado ou apagado
    E nenhum registro de auditoria foi incluído
    E a tela do pedido não abre

  Cenário: A abertura da tela não grava nada
    Dado que a minha coordenadoria tem pedidos fechados
    Quando abro a tela E026T
    Então nenhum dos seis cadastros que ela lê é tocado
    E nenhum registro de auditoria é incluído
```
