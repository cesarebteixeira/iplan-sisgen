# US — E027T — ORGAO FILHO SDI / CORD.REG.ESCOLAR

## Estória

Como **servidor de CRE**, quero **aprovar um pedido de alimentação escolar depois de
conferir os seus gêneros e as quantidades que voltaram**, para que **o pedido saia
como aprovado, o que voltou pare de contar como quantidade a entregar e o pedido
siga para o fechamento**.

O pedido é montado com o fornecedor, o período e os dias em que a entrega deve
acontecer, e as escolas devolvem parte do que receberam. Essa devolução precisa
voltar ao pedido: enquanto ela continua contando como quantidade a entregar, o
fornecedor segue comprometido com o que já retornou e a secretaria não consegue
fechar o pedido. A aprovação é o momento em que a devolução é acertada e o pedido
destrava — depois dela o pedido só sai para entrega.

## Contexto

Jornada S000M → E000M → E010M → E027T.
Ator: servidor de CRE — informa o órgão, a coordenadoria regional escolar, o número
do pedido e o ano da entrega, confere os gêneros e as quantidades que voltaram e
aprova o pedido, que segue daí para o seu fechamento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Da sessão a tela usa a matrícula, o código de acesso, a estação, a secretaria, a
coordenadoria regional escolar e o órgão filho do vínculo, além da descrição do
órgão e da data do sistema para o cabeçalho. O número do pedido e o ano da entrega
podem chegar preenchidos pela tela que a abriu ou ser informados na própria tela.
Esta tela **não termina nela mesma**: aprovado o pedido, ela o encaminha à tela de
fechamento, que abre já sobre o pedido aprovado.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela trabalha sobre o pedido que existe, informado na tela ou deixado pela tela anterior

A tela só faz alguma coisa sobre um pedido que já esteja cadastrado. O número do
pedido (6 dígitos) e o ano da entrega (4 dígitos) formam juntos o número de dez
dígitos que identifica o pedido, e é esse número que a tela procura. Quando os dois
chegam zerados, a tela **abre em consulta** e trabalha com o órgão filho e a
coordenadoria do vínculo da sessão: quem digitou o número e o ano no próprio
cabeçalho tem esse pedido procurado normalmente. A tela não inclui pedido nenhum.

[?] O número do pedido e o ano da entrega não têm conferência própria de campo em
branco: com os dois zerados a tela procura um pedido com o número zero e responde
que o pedido não está cadastrado — o que não distingue "não informei" de "não
existe". Pergunta ao site.

### RN-02 — A tela consulta e aprova, e só a aprovação grava

A tela aceita duas operações: **consultar** o pedido, que mostra o pedido e os seus
gêneros sem gravar nada, e **aprovar**, que é a alteração. Qualquer outra operação
é recusada com **\* Operacao nao disponivel. Use ALT ou CON \***, o cursor volta ao
campo da operação e nada é gravado. Quando o número do pedido não vem preenchido, a
própria tela repõe a consulta no campo da operação.

[?] A recusa manda usar ALT ou CON, mas a tela compara o campo da operação com
códigos internos de três letras e repõe o código da consulta ao abrir sem pedido
informado. Nada no acervo escreve o código da alteração nesse campo — nem a tela,
nem os menus que a abrem. Não se conclui do acervo como a operação de aprovação
chega ao campo; se ela chegar escrita como ALT, a aprovação seria recusada. Ou a
operação vem do terminal por uma tecla que o acervo não mostra, ou o caminho de
aprovação não é alcançável por menu. Pergunta ao site; não escolho um dos dois
lados.

### RN-03 — A aprovação exige que o pedido seja do grupo da sessão, que não esteja excluído e que ainda esteja em aberto

Antes de aprovar, a tela confere o pedido: o órgão filho informado tem de ser o do
vínculo da sessão, senão **\* Usuario sem acesso a outro orgao \***; o órgão tem de
estar cadastrado, senão **\* Orgao nao cadastrado \***; o pedido tem de existir,
senão **\* Pedido nao cadastrado \***; quando o vínculo carrega uma coordenadoria e
o pedido é de outra, a recusa é
**\* Usuario sem acesso ao grupo deste pedido \***; pedido excluído é recusado com
**\* Pedido excluido \***; e o pedido tem de estar em aberto — qualquer situação
diferente de "ainda não aprovado" é recusada com **\* Pedido acumulado \***,
**\* Pedido pendente de distribuicao \***, **\* Pedido pendente de aprovacao \*** ou
**\* Pedido aprovado - em aberto \***, conforme o caso. Nas recusas o cursor fica no
órgão ou no número do pedido e nada é gravado.

### RN-04 — A aprovação exige que o pedido tenha devolução a acertar

Aprovar um pedido cujos gêneros não têm nenhuma quantidade devolvida é recusado com
**\* Nao existem quantidades estornadas \***, com o cursor na marca da linha, e
nada é gravado. É a devolução pendente de um gênero que libera a aprovação.

### RN-05 — A tela mostra o pedido e até dez gêneros

Consultado o pedido, o cabeçalho mostra a descrição do tipo de órgão e a data do
sistema, o órgão filho com a sua descrição, a coordenadoria regional escolar, o
número do pedido, o ano da entrega, o código e a razão social do fornecedor, o
período de entrega e o cartão. Abaixo, em até **dez linhas**, a tela mostra de cada
gênero do pedido a subclasse, o código e a descrição, o tipo de contrato e as
quantidades **pedida**, **recebida** e **a devolver**. Um asterisco marca as linhas
de um pedido acumulado. A tela sempre mostra as dez linhas do pedido.

[?] Uma passagem de aprovação sobre um pedido sem nenhum gênero é recusada com
**\* Pedido sem generos cadastrados \***, mas a tela não pergunta se o pedido tem
gêneros antes de exibir: a mensagem sai sempre que a passagem de aprovação termina,
mesmo com o pedido mostrando gêneros, e some depois que a devolução é acertada.
Pergunta ao site; não escolho um dos dois lados.

### RN-06 — A aprovação acerta a devolução de cada gênero e dá o pedido por aprovado

Passando por todas as conferências, a tela percorre os gêneros do pedido e, para
cada um que ainda tenha quantidade a devolver, acerta o item: a quantidade devolvida
é zerada, o item é marcado como pendente e ficam registradas a matrícula e a data de
quem fez o acerto. Se o vínculo do fornecedor tiver um registro para aquele gênero,
com o mesmo órgão filho, tipo de contrato, fornecedor, coordenadoria, subclasse,
gênero e data limite, a quantidade pendente desse registro passa a ser o total
devido. Ao fim da passagem a tela marca o pedido como **aprovado** e o grava.

### RN-07 — Ao aprovar, a tela encaminha o pedido para o fechamento

Terminada a gravação, a tela encaminha o pedido à tela de fechamento — a mesma que o
menu abre para fechar pedidos —, deixando para ela o órgão filho do pedido, o número
do pedido, a coordenadoria e a situação **APROVADO**. A tela seguinte abre sobre o
pedido aprovado, e é lá que a entrega é fechada. A passagem termina nessa tela
seguinte.

### RN-08 — A consulta e cada recusa não gravam nada

Consultar o pedido não altera o pedido, não altera nenhum gênero e não deixa
registro de auditoria — e mostrar o pedido não é uma dessas operações: os gêneros e
as quantidades que aparecem na tela não são gravados de volta. Cada recusa encerra a
passagem **antes** das gravações, de modo que um pedido recusado continua
exatamente como estava. A simples abertura da tela também não escreve nem apaga
nada.

### RN-09 — Nada é gravado sem a conferência de sessão, de tela, de acesso e de aprovação

Na abertura, a tela confere que o servidor está na **estação em que a sessão foi
aberta** (em outra, o acesso é encerrado e a sessão volta à entrada), que a tela
está registrada (senão **\* Tela nao disponivel \***) e que o código de acesso do
servidor alcança a tela (senão **\* Acesso negado para esta matricula \***). Na
passagem da aprovação ela confere a rota e a **permissão de aprovação** para esta
tela, senão **\* Acesso negado para esta operacao \***; a consulta não passa por
essa permissão. Esta tela **não** confere o grupo do pedido no acesso: a recusa de
grupo é a do pedido (RN-03).

### RN-10 — Os campos numéricos passam por edição numérica antes das conferências

Antes de qualquer conferência sobre o pedido, os **treze campos numéricos** — o
órgão filho, a coordenadoria regional escolar, o número do pedido, o ano da
entrega, o código do fornecedor, dia, mês e ano do início do período, dia, mês e
ano do limite, o código da subclasse e o código do gênero — passam por edição
numérica, e o campo em branco é tratado como zero. A operação, a próxima tela, o
cartão, o código do operador e a marca da linha não passam por essa edição.
[?] A tela só sabe devolver o cursor ao órgão filho, ao número do pedido e ao ano da
entrega; um erro de digitação na coordenadoria, no fornecedor, no código do operador
ou em qualquer uma das seis datas não tem posição de cursor definida, e o que o
servidor vê nesse caso não se conclui desta tela. Pergunta ao site.

### RN-11 — A tela grava o pedido, os gêneros acertados e o registro do fornecedor, e não apaga nada

A tela enxerga **nove cadastros** e nenhum outro: o registro das telas, o cadastro
dos órgãos, o cadastro dos pedidos, o cadastro dos gêneros do pedido, o cadastro dos
gêneros, o cadastro das permissões do fornecedor, o cadastro dos fornecedores, o
cadastro dos operadores e o registro de auditoria. Ela **grava em quatro** — o
pedido (a situação passa a aprovado), cada gênero cuja devolução foi acertada, o
registro de permissão do fornecedor cuja quantidade pendente mudou e um registro de
auditoria para cada registro alterado — e **não apaga registro nenhum**. Ler a
descrição do órgão, do fornecedor, do operador, do gênero e do registro do
fornecedor não grava nada.

Os cadastros são dimensionados para: pedidos **10 milhões**; gêneros do pedido
**200 milhões**; gêneros **150 mil**; permissões do fornecedor **1 milhão**;
órgãos **12 mil**; fornecedores **10 mil**; operadores **100**; telas **2 mil**;
auditoria **60 milhões**. São capacidades (o máximo esperado no dimensionamento),
não volumes cadastrados.

### RN-12 — O acerto da devolução grava a quantidade do fornecedor inteira, não o que voltou

Ao acertar a devolução de um gênero, a quantidade que a tela grava no registro de
permissão do fornecedor é o total devido — a quantidade pedida somada à devolvida —,
e não a devolvida sozinha. Depois do acerto a devolvida fica zerada no gênero.

[?] A quantidade devolvida do gênero é somada à pedida e o resultado é gravado como
a quantidade pendente do fornecedor. Se a leitura esperada é que o compromisso do
fornecedor passe a ser só o que foi pedido, a conta está somando o que já voltou.
Pergunta ao site; não escolho um dos dois lados.

### RN-13 — O que a tela entrega à tela seguinte

Esta tela não termina nela mesma. Ao aprovar, ela encaminha para a tela de
fechamento: entrega o **órgão filho do pedido**, a **coordenadoria** e o **número do
pedido** (que a tela seguinte recompõe do número de dez dígitos que ficou na área de
trabalho), a **situação APROVADO**, um indicador de que a tela de origem é esta e
que a operação é a de alteração. É com isso que a tela de fechamento abre já sobre o
pedido aprovado, sem passar por menu.

---

## Cenários BDD

```gherkin
Funcionalidade: Aprovação do pedido de alimentação escolar e acerto das quantidades devolvidas

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E027T

  Cenário: Consultar um pedido
    Dado que existe um pedido da minha coordenadoria, com gêneros, ainda não aprovado
    Quando informo o órgão, a coordenadoria, o número do pedido e o ano da entrega e
      confirmo a consulta
    Então vejo a descrição do tipo de órgão e a data do sistema, o órgão filho com a
      sua descrição, a coordenadoria, o número do pedido, o ano da entrega, o código
      e a razão social do fornecedor, o período de entrega e o cartão
    E vejo até dez gêneros do pedido com a subclasse, o código e a descrição, o tipo
      de contrato e as quantidades pedida, recebida e a devolver
    E nada é gravado

  Cenário: A tela não inclui pedido nenhum
    Dado que o número do pedido que informo não está cadastrado
    Quando confirmo
    Então vejo "* Pedido nao cadastrado *"
    E o cursor fica no número do pedido
    E nenhum pedido é incluído

  Cenário: A operação não é a consulta nem a aprovação
    Dado que estou na tela E027T
    Quando a transação chega com uma operação que não é a de consulta nem a de
      aprovação
    Então vejo "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: O servidor não aprova pedido de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo outro órgão e confirmo a aprovação
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no órgão
    E nada é gravado

  Cenário: Órgão não cadastrado
    Dado que estou na tela E027T
    Quando informo um órgão que não está cadastrado e confirmo
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no órgão
    E nada é gravado

  Cenário: O servidor não aprova pedido de outro grupo
    Dado que o meu vínculo carrega uma coordenadoria
    Quando confirmo a aprovação de um pedido de outra coordenadoria
    Então vejo "* Usuario sem acesso ao grupo deste pedido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido excluído
    Dado que o pedido está excluído
    Quando confirmo a aprovação
    Então vejo "* Pedido excluido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido acumulado
    Dado que o pedido é um pedido acumulado
    Quando confirmo a aprovação
    Então vejo "* Pedido acumulado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido pendente de distribuição
    Dado que o pedido está pendente de distribuição
    Quando confirmo a aprovação
    Então vejo "* Pedido pendente de distribuicao *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido pendente de aprovação
    Dado que o pedido está pendente de aprovação
    Quando confirmo a aprovação
    Então vejo "* Pedido pendente de aprovacao *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido já aprovado
    Dado que o pedido já está aprovado
    Quando confirmo a aprovação
    Então vejo "* Pedido aprovado - em aberto *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: O pedido não tem devolução a acertar
    Dado que nenhum gênero do pedido tem quantidade devolvida
    Quando confirmo a aprovação
    Então vejo "* Nao existem quantidades estornadas *"
    E o cursor fica na marca da linha
    E nada é gravado

  Cenário: Aprovar o pedido
    Dado que o pedido está em aberto e tem gênero com quantidade devolvida
    Quando confirmo a aprovação
    Então o pedido fica gravado como APROVADO
    E cada gênero com quantidade a devolver fica com a devolvida zerada, marcado
      como pendente e com a minha matrícula e a data do acerto
    E o registro de permissão do fornecedor daquele gênero fica com a quantidade
      pendente acertada
    E fica um registro de auditoria de cada registro alterado

  Cenário: O pedido aprovado segue para o fechamento
    Dado que aprovei o pedido
    Quando a tela termina a passagem
    Então sou levado à tela de fechamento, que abre sobre esse pedido
    E a tela de fechamento recebe o órgão filho do pedido, a coordenadoria, o número
      do pedido e a situação APROVADO
    E a tela de fechamento abre na operação de alteração

  Cenário: A consulta não grava nada
    Dado que consultei um pedido
    Quando a tela termina a passagem da consulta
    Então o pedido continua como estava
    E nenhum gênero do pedido foi alterado
    E nenhum registro de permissão do fornecedor foi alterado
    E nenhum registro de auditoria foi incluído

  Cenário: A recusa não grava nada
    Dado que estou na tela E027T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então o pedido continua como estava
    E nenhum gênero do pedido foi alterado
    E nenhum registro de auditoria foi incluído

  Cenário: A abertura da tela não grava nada
    Dado que abro a tela E027T
    Quando a tela termina a passagem de abertura
    Então nenhum pedido é alterado
    E nenhum gênero do pedido é alterado
    E nenhuma auditoria é gravada

  Cenário: Nada é gravado sem a conferência de sessão, de tela, de acesso e de aprovação
    Dado que estou na tela E027T
    Quando a conferência da estação, do registro da tela, do código de acesso, da
      rota ou da permissão de aprovação não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *"
      ou "* Acesso negado para esta operacao *"
    E nada é gravado
    E, se a estação não for a da minha sessão, o acesso é encerrado

  Cenário: Os campos numéricos passam por edição numérica antes das conferências
    Dado que estou na tela E027T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências do pedido
    E a digitação que não é número é barrada antes das conferências do pedido
```
