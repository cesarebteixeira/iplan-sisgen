# US — E024T — Escolha do pedido para estornar

## Estória

Como **servidor de CRE**, quero **ver os pedidos de alimentação escolar do meu
grupo que estão aprovados e ainda em aberto e escolher um deles**, para que **eu
chegue ao pedido certo para estornar sem depender de saber de cor o número e o ano
da entrega**.

O pedido de alimentação escolar é identificado por um número de seis dígitos junto
com o ano da entrega, em quatro — dez dígitos que ninguém decora. No dia a dia da
coordenadoria há vários pedidos em aberto ao mesmo tempo, de escolas e fornecedores
diferentes: esta tela é o que evita procurar o pedido às cegas e o que garante que
o escolhido é de uma escola que o servidor alcança. É por ela que se entra no
estorno do pedido — sem ela, quem estorna teria de conhecer o número exato, e um
engano só apareceria depois de a tela de estorno já estar aberta.

## Contexto

Jornada S000M → E000M → E010M → E024T.

Ator: servidor de CRE — informa a coordenadoria regional escolar, vê os pedidos
aprovados e em aberto do grupo e marca o pedido que vai estornar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Da sessão a tela usa a coordenadoria regional escolar e o órgão filho do vínculo,
além da descrição da secretaria e da data do sistema para o cabeçalho. A tela é do
tipo transação e não termina nela: a linha marcada a leva para a tela de estorno
(`E025T`), e a passagem está descrita em RN-09.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela não inclui, não altera e não exclui nada

A tela é de consulta. Para montar a lista e escolher o pedido ela lê **sete
cadastros** — o registro das telas, o cadastro dos pedidos, o cadastro dos
fornecedores, o cadastro dos gêneros do pedido, o cadastro dos órgãos, o cadastro
dos operadores e o cadastro das coordenadorias regionais escolares da secretaria —,
e não escreve em nenhum deles: nada é criado, alterado ou apagado, e nenhum registro
de auditoria é incluído, porque não há alteração a registrar. As conferências de
acesso leem ainda o cadastro do funcionário e o cadastro das autorizações do código
de acesso.

Os cadastros são dimensionados para: pedidos **10 milhões**; gêneros do pedido
**200 milhões**; órgãos **12 mil**; fornecedores **10 mil**; telas **2 mil**;
coordenadorias **1 mil**; operadores **100**. São capacidades — o máximo esperado no
dimensionamento —, não volumes cadastrados.

### RN-02 — Ao abrir, a tela propõe a consulta e a coordenadoria do vínculo

Ao ser aberta, a tela põe a consulta no campo da operação e preenche a coordenadoria
regional escolar com a do vínculo da sessão; quando o vínculo não traz coordenadoria,
o campo fica em branco, para o servidor informar. No cabeçalho ela mostra a descrição
da secretaria da sessão e a data do sistema. Abrir a tela não grava nem apaga nada.

[?] Nenhum programa desta jornada preenche a coordenadoria do vínculo: o que existe
no acervo são reinicializações e duas telas de outro módulo. Se isso valer no site,
a coordenadoria nunca vem proposta, a conferência de grupo (RN-04) não tem como
barrar ninguém e a lista depende inteiramente do que o servidor digitar. Pergunta ao
site; não escolho um dos dois lados.

### RN-03 — A lista: os pedidos aprovados e em aberto do grupo

Informada a coordenadoria, a tela percorre os pedidos do grupo na ordem da coleção —
por tipo de órgão, coordenadoria, situação e, dentro dela, do ano e do número mais
antigos para os mais novos —, descartando os pedidos marcados como excluídos, e
mostra até **13** pedidos cuja situação é **aprovado e em aberto**. De cada pedido a
lista traz o número, o ano da entrega, o órgão filho, o fornecedor, o cartão, o
período de entrega e o tipo de contrato; um asterisco marca as linhas de um pedido
acumulado. Quando o grupo não tem nenhum pedido nessa situação, a recusa é
**\* Grupo sem pedidos aprovados - em aberto \***, e nada é gravado.

A tela guarda ainda, fora das linhas, um par número/ano que ela mesma preenche com o
último pedido da lista e que o servidor também pode digitar.

[?] Nada no fonte diz o que acontece quando o grupo tem mais pedidos abertos do que
cabem nas 13 linhas: a tela pede a continuação da lista e a conferência de acesso
recusa a requisição da segunda página (**\* Acesso a pagina 2 negado \***). Ou os
grupos do site nunca passam de 13 pedidos aprovados e em aberto, ou o resto da lista
não é alcançável. Pergunta ao site; não escolho um dos dois lados.

[?] O par número/ano de fora das linhas é o que a tela usa para localizar o pedido
nas conferências de grupo, enquanto a escolha usa o número e o ano da linha marcada,
e nada no fonte obriga os dois a serem o mesmo. Também não se conclui do acervo com
que valor esse par fica quando a tela é aberta pelo menu — e é ele que decide se a
lista começa no primeiro pedido do grupo ou no meio dela. Pergunta ao site.

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
já tinha — inclusive quando as duas estão zeradas, isto é, nada informado. Nesse
caso a tela segue para a escolha sem conferir grupo nenhum, e não se conclui do
acervo o que o servidor vê. Pergunta ao site.

### RN-06 — A linha marcada tem de estar preenchida

A escolha é feita na linha: o servidor marca a linha e informa nela o número do
pedido e o ano da entrega. Linha marcada e com o número e o ano zerados é recusada
com **\* A linha deve estar preenchida \***, com o cursor na marca daquela linha, e
nada é gravado. Linha não marcada não faz nada: a passagem termina sem levar a lugar
nenhum e a tela continua onde estava.

### RN-07 — O pedido escolhido tem de ser do órgão do vínculo

Achado o pedido da linha marcada, a tela o recusa quando ele é de um órgão filho
diferente do órgão do vínculo da sessão: **\* Usuario sem acesso a este orgao \***,
com o cursor na marca daquela linha, e nada é gravado. A conferência só vale quando
o vínculo da sessão carrega um órgão filho.

[?] A tela procura o pedido informado fora das linhas para saber se ele existe e está
aprovado e em aberto, mas a escolha feita na linha não repete essa procura: ela
procura o pedido apenas pela secretaria, pela coordenadoria e pelo número. Um número
que não existe segue adiante com os dados que ficaram da leitura anterior, e a tela
abre o estorno com um pedido que não é o que o servidor marcou. Ou a escolha deveria
repetir a procura, ou a leitura de apoio serve para outra coisa. Pergunta ao site;
não escolho um dos dois lados.

[?] A escolha também não repete a conferência de situação: como a leitura do pedido
marcado não é limitada aos aprovados e em aberto, um pedido que já está fechado ou
que ainda aguarda aprovação pode ser levado à tela de estorno. Pergunta ao site.

### RN-08 — Um pedido acumulado não pode ser escolhido

Achado o pedido da linha marcada, se ele é um pedido acumulado a tela recusa com
**\* Pedido acumulado \***, com o cursor na marca daquela linha, e nada é gravado.

### RN-09 — A escolha entrega o pedido à tela de estorno, já em alteração

Escolhida a linha, a tela abre a `E025T` — a tela de estorno — e deixa para ela, na
área de trabalho, o pedido escolhido: a coordenadoria, o número de dez dígitos do
pedido, o órgão filho, o fornecedor, o operador e os respectivos nomes, o cartão, o
dia, o mês e o ano do início e do limite do período de entrega, e a tela que a
chamou. Deixa também, junto com isso, a operação **alterar**.

É essa operação que decide o modo da tela seguinte: aberta por esta passagem, a tela
de estorno abre com o pedido já carregado e pronta para estornar; aberta pelo menu,
sem o pedido em contexto, ela abre em consulta. A tela percorre as linhas na ordem
em que aparecem e segue com a **primeira** que estiver marcada.

### RN-10 — A tela só atende na consulta

Ao abrir, a tela escreve a consulta no campo da operação. Antes da conferência da
própria tela, a passagem passa pela conferência de rota, que recusa a inclusão, a
alteração e a exclusão para esta tela — ela é de consulta, e não as faz — com
**\* Operacao nao disponivel \***, e que trata as operações de menu, de retorno e de
fim do acesso. A conferência da própria tela recusa qualquer operação que não seja a
consulta com **\* Opcao nao disponivel. Use CON \***, com o cursor no campo da
operação, e nada é gravado.

[?] A recusa própria da tela, que manda usar CON, só é alcançada com o campo da
operação em branco: qualquer outra operação já foi recusada antes pela conferência
de rota. Como a tecla do terminal chega escrita nesse campo não se conclui do
acervo; se chegasse escrita como a sigla que a mensagem usa, a consulta seria
recusada. Pergunta ao site.

### RN-11 — Os campos numéricos passam por edição numérica antes das conferências

Antes de qualquer conferência de negócio, os **cinco** campos numéricos — a
coordenadoria regional escolar, o par número/ano que a tela guarda fora das linhas,
o número do pedido e o ano da entrega da linha — passam por edição numérica, e o
campo em branco é tratado como zero. A operação, a tela de destino e a marca da
linha não passam por essa edição.

[?] A tela só sabe devolver o cursor à coordenadoria e ao par número/ano de fora das
linhas; um erro de digitação no número ou no ano da linha marcada não tem posição de
cursor definida, e o que o servidor vê nesse caso não se conclui da tela. Pergunta
ao site.

### RN-12 — Nada é gravado nem escolhido sem a conferência de sessão, de tela e de acesso

Na abertura, a tela confere que o servidor está na **estação em que a sessão foi
aberta** (em outra, o acesso é encerrado e a sessão volta à entrada), que a tela está
registrada (senão **\* Tela nao disponivel \***), que ela pertence ao módulo da
sessão e que o código de acesso do servidor alcança a tela (senão
**\* Acesso negado para esta matricula \***). Também é recusada a requisição da
segunda página da tela (**\* Acesso a pagina 2 negado \***). Na passagem da escolha
a rota e o acesso à tela são conferidos de novo. A tela não exige permissão de
alteração, porque não altera nada. Sem passar por tudo, nada é gravado e a tela de
estorno não abre.

### RN-13 — A recusa não grava nada e não leva a lugar nenhum

Cada recusa encerra a passagem antes de qualquer gravação e antes da abertura da
tela de estorno: nenhum dos sete cadastros é tocado e nenhum registro de auditoria é
incluído. Uma recusa registrada numa linha impede que as linhas seguintes sejam
examinadas na mesma passagem. A simples abertura da tela também não escreve nem
apaga nada.

---

## Cenários BDD

```gherkin
Funcionalidade: Escolha do pedido de alimentação escolar do grupo para estornar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E024T

  Cenário: A tela lista os pedidos aprovados e em aberto do grupo
    Dado que a minha coordenadoria tem pedidos aprovados e ainda em aberto
    Quando abro a tela E024T
    Então o campo da coordenadoria vem com a coordenadoria do meu vínculo
    E vejo até 13 pedidos do grupo, com o número, o ano da entrega, o órgão filho, o
      fornecedor, o cartão, o período de entrega e o tipo de contrato
    E um asterisco marca as linhas de um pedido acumulado
    E os pedidos excluídos não aparecem
    E nada é gravado

  Cenário: O grupo não tem pedidos aprovados e em aberto
    Dado que não há pedido aprovado e em aberto para a minha coordenadoria
    Quando abro a tela E024T
    Então vejo "* Grupo sem pedidos aprovados - em aberto *"
    E nada é gravado

  Cenário: A abertura propõe a consulta e a coordenadoria do vínculo
    Dado que o meu vínculo carrega uma coordenadoria regional escolar
    Quando abro a tela E024T
    Então o campo da operação vem com a consulta
    E o campo da coordenadoria vem com a coordenadoria do meu vínculo
    E vejo a descrição da secretaria da minha sessão e a data do sistema
    E nada é gravado nem apagado

  Cenário: Sem coordenadoria no vínculo, o campo fica para eu informar
    Dado que o meu vínculo não carrega coordenadoria regional escolar
    Quando abro a tela E024T
    Então o campo da coordenadoria fica em branco, para eu informar
    E informo a coordenadoria do meu grupo
    E a tela confere que esse grupo pertence à minha secretaria
    E nada é gravado nem apagado

  Cenário: Escolher um pedido e ir para o estorno
    Dado que a lista mostra os pedidos aprovados e em aberto do meu grupo
    Quando marco a linha de um pedido, informo nela o número do pedido e o ano da
      entrega e confirmo
    Então a tela E025T abre com esse pedido já carregado
    E ela abre na operação de alteração, pronta para estornar
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
    E a tela de estorno não abre
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

  Cenário: Pedido acumulado
    Dado que o pedido da linha marcada é um pedido acumulado
    Quando confirmo
    Então vejo "* Pedido acumulado *"
    E o cursor fica na marca daquela linha
    E nada é gravado

  Cenário: A tela só atende na consulta
    Dado que estou na tela E024T
    Quando a transação chega com o campo da operação em branco
    Então vejo "* Opcao nao disponivel. Use CON *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: Inclusão, alteração e exclusão são recusadas antes da tela
    Dado que estou na tela E024T
    Quando a transação chega com a operação de inclusão, de alteração ou de exclusão
    Então vejo "* Operacao nao disponivel *"
    E a conferência da própria tela não chega a ser feita
    E nada é gravado

  Cenário: Os campos numéricos passam por edição numérica antes das conferências
    Dado que estou na tela E024T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências de negócio
    E a digitação que não é número é barrada antes das conferências de negócio

  Cenário: Nada é escolhido nem gravado sem a conferência de sessão, de tela e de acesso
    Dado que estou na tela E024T
    Quando a conferência da estação, do registro da tela, do módulo ou do código de
      acesso não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *" ou
      "* Acesso a pagina 2 negado *"
    E nada é gravado
    E, se a estação não for a da minha sessão, o acesso é encerrado

  Cenário: A recusa não grava nada e não leva à tela de estorno
    Dado que estou na tela E024T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então nenhum pedido, gênero, fornecedor, órgão, operador, tela ou coordenadoria
      foi criado, alterado ou apagado
    E nenhum registro de auditoria foi incluído
    E a tela de estorno não abre

  Cenário: A abertura da tela não grava nada
    Dado que a minha coordenadoria tem pedidos aprovados e em aberto
    Quando abro a tela E024T
    Então nenhum dos sete cadastros que ela lê é tocado
    E nenhum registro de auditoria é incluído
```
