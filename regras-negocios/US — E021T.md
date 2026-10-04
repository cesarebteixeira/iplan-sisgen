# US — E021T — Distribuir as quantidades do pedido de alimentação escolar pelos dias de entrega

## Estória

Como **servidor de CRE**, quero **distribuir a quantidade de cada gênero do pedido de
alimentação escolar pelos dias de entrega previstos, e poder incluir ou tirar gêneros do
pedido**, para que **o fornecedor saiba o que entregar em cada dia e a secretaria possa
conferir o recebimento e repartir os gêneros entre as escolas**.

O pedido nasce com o órgão, o fornecedor, o período e os dias em que a entrega deve
acontecer — mas isso ainda não diz quanto de cada gênero sai em cada um desses dias, e é
esse número que o fornecedor segue e que a escola confere quando recebe. Enquanto a
distribuição não existe, o pedido carrega quantidade sem data: não fecha contra o que
chega e não pode seguir para aprovação. É também aqui que o pedido se corrige antes de
seguir: o gênero que faltou entra e o que sobrou sai.

## Contexto

Jornada S000M → E000M → E010M → E020T → E021T.
Ator: servidor de CRE — abre o pedido que a tela do pedido deixou, percorre os gêneros
desse pedido e distribui as quantidades pelos dias de entrega, incluindo, alterando ou
excluindo gêneros.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Esta tela não é aberta por menu: ela é encadeada pela tela do pedido (`E020T`), que deixa
na sessão o pedido, o órgão, a coordenadoria, o fornecedor, o período e os dias de entrega,
e é essa mesma área que a tela usa para saber em que modo abrir. No fim, ou o servidor
volta ao menu `E010M`, ou é devolvido à tela do pedido para montar outro pedido.

As regras abaixo são só as desta tela.

## Regras de negócio

### RN-01 — A tela só abre pela tela do pedido, e trabalha sobre o pedido que ela deixou

Esta tela não procura pedido. Ela mostra e altera o pedido que a tela do pedido deixou: o
órgão filho, a coordenadoria regional escolar, o número e o ano do pedido, o fornecedor e a
sua razão social, o período de entrega, o cartão e os dias de entrega. O número do pedido
aparece separado em número (seis dígitos) e ano (quatro dígitos), e digitar outro número ou
outro ano no cabeçalho não troca o pedido em tela: o que se mostra e o que se grava
continua sendo o pedido que foi deixado. A tela só aceita ser aberta pela tela do pedido
(`E020T`) ou pela tela do pedido acumulado (`E040T`); chegando de qualquer outra tela, ela
não mostra nem grava nada e devolve o servidor ao menu `E010M`, que avisa
* Acesso deve ser feito pela tela E020T * e o encaminha para a tela do pedido.

### RN-02 — A tela abre no modo que a tela de origem deixou

A tela abre em **consulta** quando vem da consulta da tela do pedido ou da tela do pedido
acumulado: nesse modo ela só mostra. Abre em **alteração** quando vem da tela do pedido
logo depois de o pedido ter sido gravado. Na alteração, cada linha traz uma ação, e há
três: **incluir** o gênero no pedido, **alterar** as quantidades daquele gênero e
**excluir** o gênero do pedido. Linha sem ação, ou com ação diferente dessas três, é
ignorada. Uma operação que não seja consulta, inclusão, alteração ou exclusão é recusada
com * Operacao nao disponivel *, e nesse caso nada é mostrado nem gravado.

[?] A tela trata a inclusão como operação própria, mas nenhuma das duas telas que a abrem
entrega essa operação: a inclusão que o servidor percebe é a ação de incluir marcada na
linha, dentro da alteração. Como o servidor chegaria à tela já em inclusão não se conclui
do acervo. Pergunta ao site.

### RN-03 — A tela mostra o pedido e até treze gêneros

Aberta a tela, o cabeçalho mostra a descrição do tipo de órgão e a data do sistema, o órgão
filho com a sua descrição, a coordenadoria, o número e o ano do pedido, o fornecedor com a
razão social, o período de entrega, o cartão, a situação do pedido — **Aprovado** ou
**Fechado**, quando for o caso — e os cinco dias de entrega. Abaixo, em até **treze
linhas**, a tela mostra de cada gênero do pedido: a subclasse, o código e a descrição do
gênero, as quantidades por dia de entrega e a ação da linha; um asterisco marca as linhas
de um pedido acumulado. Os gêneros já excluídos do pedido não aparecem. Um pedido sem
nenhum gênero é recusado com * Pedido sem generos cadastrados *, e nada é gravado.

### RN-04 — Só um pedido ainda não aprovado pode ser alterado

Quando a situação do pedido já saiu de "ainda não aprovado" — quando ele já está aprovado
ou já está fechado —, a tela avisa, mostrando a situação e, respectivamente,
* Pedido aprovado nao pode ser alterado * ou * Pedido fechado nao pode ser alterado *.
Nesse caso o pedido continua visível, mas a tela não sai da consulta: a alteração não é
feita e nada é gravado. O mesmo vale quando o pedido não é encontrado.

[?] A situação do pedido só é conferida no caminho que promove a consulta a alteração. Uma
alteração que já chegue como alteração não passa por essa conferência, e a passagem que
grava devolve o pedido a "não aprovado" sem reclamar. Não se conclui do acervo se a tela do
pedido barra essa entrada antes. Pergunta ao site.

### RN-05 — Os cinco dias de entrega e as quantidades de cada dia

Os dias de entrega que a tela mostra são os que a tela do pedido calculou, e são no máximo
cinco. Cada linha tem uma quantidade para cada um desses dias, e o total da linha é a soma
das cinco. A quantidade só pode ser informada para um dia que o pedido tem: em um dia que o
pedido não tem, a recusa é * Inf. quantidade para dias de entrega validos *, com o cursor na
quantidade daquele dia. O total das cinco quantidades tem de ser maior que zero, senão
* Informe quantidade *, com o cursor na primeira quantidade. E cada quantidade informada
tem de ser um múltiplo inteiro da quantidade de fracionamento do gênero, senão
* Quant. fracionada invalida para este genero *.

[?] A tela exibe os dias de entrega e decide por eles, mas nunca lhes dá valor: eles só
podem chegar da tela anterior, pela área da sessão. Não se conclui do acervo o que acontece
se essa área chegar vazia — nesse caso nenhuma quantidade passaria pela conferência do dia
de entrega e nem incluir nem alterar gênero funcionaria. Pergunta ao site.

[?] A conferência do fracionamento divide a quantidade informada pela quantidade de
fracionamento do gênero e decide pelo resto; nada no acervo diz o que acontece quando esse
fracionamento está zerado. Pergunta ao site.

### RN-06 — Incluir um gênero no pedido

Para incluir, o servidor informa a subclasse, o gênero e as quantidades por dia de entrega.
O par subclasse e gênero tem de estar no cadastro de gêneros, senão
* Sub/Genero nao cadastrado *; o gênero não pode já estar no pedido, senão
* Genero ja cadastrado neste pedido *; e valem o total maior que zero, os dias de entrega
válidos e o fracionamento (RN-05). Passando por isso, a tela inclui o gênero no pedido com
as quantidades informadas, com a classificação lida do cadastro de gêneros, com a matrícula
e a data de quem digitou, e com o registro de auditoria. Nas recusas o cursor volta à
subclasse ou à quantidade do primeiro dia.

### RN-07 — Alterar as quantidades de um gênero

Para alterar, o servidor marca a ação de alteração na linha e informa as novas quantidades.
O gênero tem de estar no pedido, senão * Genero nao cadastrado neste pedido *; não pode
estar excluído do pedido, senão * Genero excluido deste pedido *; e não pode ser de um
pedido acumulado, senão <- Genero acumulado neste pedido *. Valem o total maior que zero,
os dias de entrega válidos e o fracionamento (RN-05). A alteração regrava as cinco
quantidades e o total daquele gênero no pedido e zera o que já estava registrado como
recebido ou estornado nele.

### RN-08 — Excluir um gênero do pedido

Para excluir, o servidor marca a ação de exclusão na linha. O gênero tem de estar no pedido
e não pode estar excluído nem ser de um pedido acumulado (RN-07). A exclusão não pede
quantidade nenhuma e tira o gênero do pedido: não é uma marca de exclusão, o registro sai.
Fica o registro de auditoria com o que havia antes.

### RN-09 — O pedido que tem gênero de contrato não pode ser atualizado

Se qualquer gênero do pedido tem tipo de contrato, a alteração é recusada por inteiro com
* Pedido nao pode ser atualizado *, com o cursor no campo da operação, e nada é gravado. É
por isso que as recusas por gênero "não pode ser alterado" e "não pode ser excluído" não
chegam a aparecer: quando o gênero tem tipo de contrato, a recusa que o servidor vê é a do
pedido inteiro.

[?] A conferência que recusa o pedido inteiro percorre os gêneros do pedido sem descartar os
já excluídos, de modo que um gênero excluído, com tipo de contrato, recusa a alteração de um
gênero que não tem contrato nenhum. Se o site espera ver as recusas por gênero, é esta
conferência que está larga demais. Pergunta ao site.

### RN-10 — O que fica gravado

Confirmada a inclusão ou a alteração, a tela grava no gênero do pedido as cinco quantidades
por dia de entrega, o total, a matrícula e a data de quem digitou, e deixa em branco a
situação do item; o tipo de contrato não é gravado — fica zero — e o que havia de recebido
ou estornado é zerado. Para cada registro que muda, a tela inclui um registro de auditoria
com a operação, o cadastro atingido, o número do pedido, a coordenadoria, a matrícula do
servidor, a estação, o dia, a hora e o minuto da sessão, e o conteúdo do registro antes e
depois da alteração. Nenhum outro cadastro é tocado.

### RN-11 — No fim da alteração a tela acerta o pedido

Terminada a passagem, a tela percorre os gêneros do pedido. Se sobrou algum gênero vivo, ela
devolve o pedido ao estado "não aprovado" — apaga a situação, a matrícula e a data da
aprovação — e grava o pedido. Se não sobrou nenhum, porque o último gênero foi excluído, ela
apaga o pedido. Nessa mesma passagem a tela apaga definitivamente os gêneros que já estavam
marcados como excluídos.

[?] A passagem final apaga os gêneros que já estavam excluídos em toda alteração, e não só
quando o pedido fica sem gênero nenhum, e apaga o pedido em vez de marcá-lo como excluído.
Não se conclui do acervo se essa limpeza definitiva dos gêneros excluídos por outras telas é
o esperado. Pergunta ao site.

### RN-12 — A consulta e as recusas não gravam nada

A consulta termina antes de qualquer gravação: não altera o gênero do pedido, não altera o
pedido e não deixa registro de auditoria. Cada recusa também encerra a passagem antes das
gravações, de modo que um pedido recusado continua exatamente como estava.

### RN-13 — Nada é gravado sem a conferência de sessão, de tela, de acesso e da operação

Na abertura, a tela confere que o servidor está na **estação em que a sessão foi aberta**
(em outra, o acesso é encerrado e a sessão volta ao `LOGON`), que a tela está registrada
(senão * Tela nao disponivel *) e que o código de acesso do servidor alcança a tela (senão
* Acesso negado para esta matricula *). Na passagem da alteração ela confere a rota e a
**permissão de alteração** para esta tela (senão * Acesso negado para esta operacao *) e, por
linha, a permissão da ação: incluir exige a permissão de inclusão, alterar as quantidades
exige a de alteração e excluir exige a de exclusão. A consulta não passa por essa permissão
de operação. Esta tela **não** confere o vínculo do servidor com o órgão: ela trabalha com a
coordenadoria que a tela anterior deixou.

### RN-14 — Os campos numéricos passam por edição numérica antes das conferências

Antes de qualquer conferência, os **dezoito campos numéricos** — o órgão filho, a
coordenadoria regional escolar, o número do pedido, o ano da entrega, o código do
fornecedor, o dia, o mês e o ano do início do período, o dia, o mês e o ano do limite, o
código da subclasse, o código do gênero e as cinco quantidades — passam por edição numérica,
e o campo em branco é tratado como zero. As quantidades aceitam vírgula como separador
decimal. A operação, a próxima tela, o cartão e a ação da linha não passam por essa edição.

[?] A tela só sabe devolver o cursor à subclasse, ao gênero e às cinco quantidades; um erro
de digitação na coordenadoria, no fornecedor ou em qualquer uma das seis datas não tem
posição de cursor definida, e o que o servidor vê nesse caso não se conclui desta tela.
Pergunta ao site.

### RN-15 — O que a tela entrega: o pedido novo

Ao terminar, a tela devolve o servidor ao menu `E010M` — ou à tela do pedido, quando o
servidor marcou o campo de pedido novo. Nesse caso ela deixa para a tela do pedido a
indicação de que a chamada vem desta tela, a operação de inclusão e o número do pedido
zerado; a tela do pedido reabre então em inclusão, com o número e o ano do pedido em branco,
pronta para montar outro pedido e mantendo o órgão e a coordenadoria do anterior.

[?] O campo que pede o pedido novo é reiniciado na primeira linha da tela e nenhuma linha do
programa o alimenta: ele só pode vir da digitação. O rótulo que a tela mostra para esse
campo não está no corpus desta jornada, e não se conclui daqui se o servidor o marca ou se
ele já chega marcado. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Distribuir as quantidades do pedido de alimentação escolar pelos dias de entrega

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria em que atuo
    E que vim da tela E020T, que deixou na área de trabalho o pedido, o órgão, a
      coordenadoria, o fornecedor, o período e os cinco dias de entrega
    E tenho acesso à tela E021T

  Cenário: Consultar um pedido
    Dado que existe um pedido do meu órgão, com gêneros, cuja situação ainda está em branco
    Quando abro a tela E021T em consulta
    Então vejo no cabeçalho o órgão filho, a coordenadoria, o número e o ano do pedido,
      o fornecedor com a razão social, o período, o cartão e os cinco dias de entrega
    E vejo até treze gêneros do pedido com a subclasse, o código e a descrição, as
      quantidades de cada dia de entrega e a ação da linha
    E nada é gravado

  Cenário: A consulta não grava nada
    Dado que estou na E021T em modo de consulta
    Quando a tela percorre os gêneros do pedido
    Então nenhum gênero é incluído, alterado ou excluído
    E o pedido não é alterado
    E nenhum registro de auditoria é gerado

  Cenário: A tela não abre vinda de outra tela
    Dado que a transação chegou de uma tela que não é a do pedido nem a do pedido acumulado
    Quando abro a tela E021T
    Então a tela não mostra nem grava nada
    E sou devolvido ao menu E010M
    E o menu avisa "* Acesso deve ser feito pela tela E020T *" e me encaminha para a tela
      do pedido

  Cenário: A tela abre em alteração quando vem da tela do pedido
    Dado que a tela do pedido acabou de gravar o pedido e me passou a chamada em alteração
    Quando abro a tela E021T
    Então a tela abre em modo de alteração
    E cada linha aceita a ação de incluir, de alterar ou de excluir

  Cenário: Operação não disponível
    Dado que cheguei à E021T com uma operação que não é consulta, inclusão, alteração
      nem exclusão
    Quando a tela confere a operação
    Então vejo "* Operacao nao disponivel *"
    E nada é mostrado nem gravado

  Cenário: Pedido sem gêneros
    Dado que o pedido não tem nenhum gênero
    Quando abro a tela E021T
    Então vejo "* Pedido sem generos cadastrados *"
    E nada é gravado

  Cenário: Pedido já aprovado
    Dado que a situação do pedido já é aprovado
    Quando abro a tela E021T e tento alterar
    Então vejo a situação Aprovado e o aviso "* Pedido aprovado nao pode ser alterado *"
    E a tela não sai da consulta e a alteração não é feita
    E nada é gravado

  Cenário: Pedido já fechado
    Dado que a situação do pedido já é fechado
    Quando abro a tela E021T e tento alterar
    Então vejo a situação Fechado e o aviso "* Pedido fechado nao pode ser alterado *"
    E a tela não sai da consulta e a alteração não é feita
    E nada é gravado

  Cenário: Incluir um gênero novo no pedido
    Dado que o pedido é de um órgão com acesso liberado e ainda não está aprovado
    E que o par subclasse e gênero está no cadastro de gêneros e ainda não está neste pedido
    Quando marco a ação de incluir na linha, informo a subclasse, o gênero e as quantidades
      por dia de entrega, e confirmo
    Então o gênero passa a fazer parte do pedido com as quantidades informadas
    E o gênero fica com a classificação do cadastro, com a minha matrícula e a data do dia
    E fica um registro de auditoria da inclusão

  Cenário: Subclasse ou gênero não cadastrado
    Dado que consultei o pedido
    Quando incluo um gênero cujo par subclasse e gênero não está no cadastro de gêneros
      e confirmo
    Então vejo "* Sub/Genero nao cadastrado *"
    E o cursor fica na subclasse
    E nada é gravado

  Cenário: Gênero já cadastrado neste pedido
    Dado que consultei o pedido
    Quando incluo um gênero que já faz parte deste pedido e confirmo
    Então vejo "* Genero ja cadastrado neste pedido *"
    E o cursor fica na subclasse
    E nada é gravado

  Cenário: O total das quantidades é obrigatório
    Dado que consultei o pedido e marquei a ação de incluir na linha
    Quando confirmo com as cinco quantidades zeradas
    Então vejo "* Informe quantidade *"
    E o cursor fica na quantidade do primeiro dia de entrega
    E nada é gravado

  Cenário: Quantidade informada para um dia que o pedido não tem
    Dado que consultei o pedido e informei a quantidade em um dia de entrega que este
      pedido não tem
    Quando confirmo
    Então vejo "* Inf. quantidade para dias de entrega validos *"
    E o cursor fica na quantidade daquele dia
    E nada é gravado

  Cenário: Quantidade fracionada inválida
    Dado que consultei o pedido
    E que a quantidade informada em um dia não é um múltiplo inteiro da quantidade de
      fracionamento do gênero
    Quando confirmo
    Então vejo "* Quant. fracionada invalida para este genero *"
    E o cursor fica na quantidade daquele dia
    E nada é gravado

  Cenário: Alterar as quantidades de um gênero do pedido
    Dado que consultei o pedido e o gênero está nele, não está excluído e não é de pedido
      acumulado
    Quando marco a ação de alterar na linha, informo as novas quantidades por dia de
      entrega e confirmo
    Então o gênero do pedido fica com as quantidades informadas e com o novo total
    E o que havia de recebido ou estornado naquele gênero é zerado
    E fica um registro de auditoria da alteração

  Cenário: Gênero que não está neste pedido
    Dado que consultei o pedido e marquei a ação de alterar ou de excluir na linha
    Quando confirmo com um par subclasse e gênero que não faz parte deste pedido
    Então vejo "* Genero nao cadastrado neste pedido *"
    E o cursor fica na subclasse
    E nada é gravado

  Cenário: Gênero já excluído do pedido
    Dado que consultei o pedido e o gênero da linha já está excluído do pedido
    Quando confirmo a alteração ou a exclusão daquela linha
    Então vejo "* Genero excluido deste pedido *"
    E o cursor fica na subclasse
    E nada é gravado

  Cenário: Gênero de pedido acumulado
    Dado que consultei o pedido e o gênero da linha é de um pedido acumulado
    Quando confirmo a alteração ou a exclusão daquela linha
    Então vejo "<- Genero acumulado neste pedido *"
    E o cursor fica na subclasse
    E nada é gravado

  Cenário: Excluir um gênero do pedido
    Dado que consultei o pedido e o gênero está nele, não está excluído e não é de pedido
      acumulado
    Quando marco a ação de excluir na linha e confirmo
    Então o gênero sai do pedido
    E fica um registro de auditoria com o que havia antes
    E nenhuma quantidade é exigida

  Cenário: Linha sem ação não faz nada
    Dado que estou na E021T em modo de alteração e deixei uma linha preenchida sem ação
    Quando confirmo
    Então aquela linha não gera operação nenhuma
    E nada é gravado para ela

  Cenário: O pedido tem gênero com tipo de contrato
    Dado que consultei um pedido que tem ao menos um gênero com tipo de contrato
    Quando confirmo uma inclusão, uma alteração ou uma exclusão de gênero
    Então vejo "* Pedido nao pode ser atualizado *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: A alteração devolve o pedido a não aprovado
    Dado que consultei um pedido que ainda não está aprovado e alterei as quantidades de
      um gênero
    Quando a tela termina a passagem
    Então o pedido continua com pelo menos um gênero
    E a situação, a matrícula e a data da aprovação do pedido ficam apagadas
    E o pedido é gravado

  Cenário: Excluir o último gênero apaga o pedido
    Dado que o pedido tem um único gênero e eu o excluí
    Quando a tela termina a passagem
    Então o pedido não tem mais nenhum gênero
    E o pedido é apagado
    E fica o registro de auditoria do pedido

  Cenário: Toda gravação fica registrada na auditoria
    Dado que incluí, alterei ou excluí um gênero do pedido
    Quando a gravação termina
    Então fica um registro de auditoria com a operação, o cadastro atingido, o número do
      pedido, a coordenadoria, a minha matrícula, a estação e a data e a hora da sessão
    E o registro guarda o conteúdo anterior e o posterior

  Cenário: A recusa não grava nada
    Dado que estou na tela E021T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então o gênero do pedido continua como estava
    E o pedido continua como estava
    E nenhum registro de auditoria foi incluído

  Cenário: Nada é gravado sem a conferência de sessão, de tela, de acesso e da operação
    Dado que estou na tela E021T
    Quando a conferência da estação, do registro da tela, do código de acesso, da rota ou
      da permissão da operação não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *" ou
      "* Acesso negado para esta operacao *"
    E nada é gravado
    E, se a estação não for a da minha sessão, o acesso é encerrado

  Cenário: Os campos numéricos passam por edição numérica antes das conferências
    Dado que estou na tela E021T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências
    E a quantidade aceita a vírgula como separador decimal

  Cenário: Pedir um pedido novo
    Dado que terminei de distribuir as quantidades do pedido em tela
    Quando marco o campo de pedido novo e confirmo
    Então sou devolvido à tela do pedido
    E a tela do pedido reabre em inclusão, com o número e o ano do pedido em branco
    E ela mantém o órgão e a coordenadoria do pedido anterior

  Cenário: Terminar sem pedir pedido novo
    Dado que terminei de distribuir as quantidades do pedido em tela
    Quando confirmo sem marcar o campo de pedido novo
    Então a tela termina e sou devolvido ao menu E010M
```
