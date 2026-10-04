# US — N026T — Consulta da nota fiscal por item

## Estória

Como **servidor de CRE que consulta as notas fiscais lançadas**, quero **ver o que
uma nota fiscal registra — o fornecedor, as datas de emissão, o processo, o pedido e
as linhas de gênero do documento com quantidade e valor — e seguir daí para a
consulta da nota**, para que **a conferência da despesa comece pelo documento certo e
não por uma tela em branco**.

A nota fiscal é lançada por gênero, e é gênero a gênero que a despesa se confere:
cada linha tem a sua quantidade, o seu valor unitário e o seu total. Esta é a tela
em que o servidor vê essas linhas depois de já ter localizado a nota, e é dela que
ele desce para a consulta que abre a nota e os pedidos que a compõem. Sem esta
passagem, quem achou a nota fica sabendo apenas que ela existe — não o que ela
contém.

## Contexto

Jornada S000M → N000M → N060M → N025T → N026T.

Ator: servidor de CRE — vê o que a nota fiscal registra e segue para a consulta da
nota e dos pedidos que a compõem.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A `N026T` não é menu e não tem opção de menu que a abra: ela é **aberta pela tela de
consulta da nota fiscal (`N025T`)**, que lhe entrega a nota já localizada. Por isso o
que a `N025T` deixa — o número da nota, o fornecedor, o ano das datas fiscais e a
própria condição de consulta — entra aqui como **regra desta tela**, e não como
contexto. As telas `N000M` e `N060M` são menus: só encaminham. O contexto da sessão
que esta tela usa — o tipo de órgão, a coordenação regional escolar, a matrícula, o
privilégio e a data do sistema — é o que a entrada deixou; ela não o recalcula.

As regras abaixo são só as da **tela desta jornada**. As da entrada estão em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md` e o que se apurou sobre elas
está no anexo de evidências.

---

## Regras de negócio

### RN-01 — A tela é de consulta e não grava

A tela só mostra: ela lê os cadastros da nota, do processo e do gênero e apresenta o
resultado. Não inclui, não altera e não exclui nota fiscal, item ou pedido, e não
deixa registro de operação. As rotinas de gravação e de exclusão existem no código
porque o gerador as escreve para todo cadastro que o programa enxerga, mas nenhuma
delas é executada por esta tela.

### RN-02 — A matrícula, o órgão do servidor e os demais dados da sessão passam pela conferência de autorização

Antes de ler qualquer cadastro, a tela pede a conferência de autorização do perfil
para a própria tela e para o tipo de órgão da sessão — para isso entrega a matrícula,
o privilégio, o tipo de órgão e a coordenação regional escolar. Não estando
autorizada, a tela é abandonada sem mostrar registro nenhum.

[?] A autorização por operação não é consultada nesta tela: ela não informa qual
operação pretende — se consulta, se alteração. Como a tela só consulta, isso não
muda o que o servidor vê; mas se algum dia a tela passar a alterar, a autorização por
operação teria de existir. Pergunta ao site.

### RN-03 — Os dezesseis campos numéricos da nota passam pela edição numérica antes de qualquer leitura

Os campos que o servidor digita e que são números — o número da nota fiscal, o dia,
o mês e o ano de emissão da nota fiscal, o dia, o mês e o ano de emissão do
documento, o código do fornecedor, o código do operador, a coordenação regional
escolar, o tipo de contrato, o número do pedido, o ano da entrega, o órgão filho, o
código da subclasse e o código do gênero — são todos conferidos como número antes de
a tela procurar qualquer registro. O que se digita é convertido, os zeros à esquerda
caem, o campo em branco vira zero e o campo recusado recebe o cursor de volta.

[?] A conversão que descarta os zeros à esquerda, feita sobre o número da nota fiscal
e sobre a coordenação regional escolar, transforma "0012" em "12": se o número
gravado distingue a quantidade de dígitos, a procura muda de resultado. É pergunta ao
site.

### RN-04 — A tela mostra o que a nota registra

Achada a nota, a tela apresenta 21 campos de dados — contados um a um na declaração
da resposta da tela: o tipo de órgão, a data do sistema, a descrição do tipo de
órgão, o nome do fornecedor, a descrição da situação do documento, o nome do
operador, a indicação de acumulação, o nome do órgão, o valor total da nota, o valor
total retido, a descrição resumida do gênero, a unidade de medida, a quantidade do
gênero, o valor unitário do item e o valor total do item, o código do fornecedor, a
coordenação regional escolar, o tipo de contrato, o número do pedido, o ano da
entrega e o nome do órgão filho.

### RN-05 — O item da nota vem da chave da nota, e o gênero, do cadastro de gêneros

Depois do cabeçalho, a tela lista os **oito** primeiros gêneros da nota — são **8
linhas**, contadas na declaração da tabela de repetição do cadastro de gêneros da
nota. Cada linha tem **7 campos**: código da subclasse, código do gênero, descrição
resumida do gênero, código da unidade de medida, quantidade do gênero, valor unitário
do item e valor total do item.

A linha só aparece quando o cadastro de itens da nota confirma, pela mesma chave com
que foi lida, o tipo de órgão, o fornecedor, o ano, o mês e o dia fiscais da nota e o
número do processo: é assim que a tela garante que o item é daquela nota. A descrição
do gênero e a unidade de medida não vêm do item — vêm do cadastro de gêneros,
procuradas pelo par subclasse e gênero para o ano de emissão da nota.

[?] A tela tem 8 linhas de item e não avisa quando a nota tem mais gêneros do que
isso: se a nona linha some sem mensagem, ou se a tela deveria paginar, não se lê do
acervo. Pergunta ao site.

### RN-06 — O par subclasse e gênero tem de estar cadastrado para o ano da nota

Para mostrar a linha, a tela procura o par subclasse e gênero no cadastro de gêneros
pelo ano de emissão da nota. Não achando o par — ou achando-o excluído, porque o
cadastro esconde o que está marcado como excluído —, a linha não é mostrada.

### RN-07 — O pedido acumulado é condição para a tela seguir, mas a tela desta jornada não alcança essa conferência

A tela confere se o pedido é de pedido acumulado: quando não é, ela recusa com
**\* Pedido nao acumulado \***, marca o pedido como recusado e deixa o cursor no
campo do pedido; e quando o pedido é acumulado e a operação não é consulta, ela
recusa com **\* Use somente com opcao CON \***. Nenhuma das duas recusas é alcançada
quando a tela é aberta pela tela de consulta da nota fiscal: essa abertura já chega
marcada como consulta, e a primeira recusa exige que não seja, enquanto a segunda
exige que o pedido não seja acumulado e a consulta — a operação com que a tela chega
— a dispensa.

[?] A tela de consulta da nota fiscal abre esta tela em consulta, e é a única que a
abre; logo a recusa "Use somente com opcao CON" não tem como aparecer, e a conferência
do pedido acumulado — que existe para barrar a alteração — fica sem efeito prático
aqui. Se a tela deveria abrir também em alteração, ou se essas conferências são
resíduo de outro desenho, é pergunta ao site.

### RN-08 — O item que não confere com o número do processo da nota não entra na linha

Se o item lido não confere com o número do processo da nota, a tela segue sem
aproveitar esse item: zera a subclasse e o gênero da linha e deixa a quantidade e os
valores em branco.

[?] A tela não recusa nem avisa nesse caso: a linha pode ficar com o código do gênero
e sem quantidade e sem valor, o que o servidor pode ler como "este gênero não tem
quantidade". Se essa linha deveria existir, é pergunta ao site.

### RN-09 — Nota sem gênero nenhum é aviso

Não havendo nenhum item para a nota na chave procurada, a tela mostra o aviso
**\* Nota fiscal sem generos cadastrados \*** e encerra a resposta.

[?] O aviso só é montado por um caminho que, na linha de cima, exige que o item da
nota **não** tenha sido encontrado — e é esse mesmo caminho que depois marca o item
como tratado e segue em frente. Ou o aviso pertence a outro caso, ou ele nunca
aparece. Pergunta ao site.

### RN-10 — Achada a nota, a tela encaminha para a consulta da nota

Terminada a consulta, a tela encaminha o servidor para a **consulta da nota fiscal**
(`N124C`) sem passar por menu nenhum, e a nota vai junto: o número da nota fiscal, o
fornecedor, o ano das datas fiscais, o número do processo, o par subclasse e gênero da
última linha lida e a indicação de que aquele é o documento a consultar.

### RN-11 — A tela de consulta da nota fiscal reabre esta tela com a nota apagada e a consulta anterior restabelecida

Quando a consulta da nota fiscal devolve o controle, esta tela reabre com a nota já
apagada — o número da nota fiscal volta a zero — e com o resto da consulta anterior
restabelecido, e sai sem mostrar registro e sem gravar.

### RN-12 — A tela também devolve o controle para a consulta da nota fiscal e para o menu da nota fiscal

Além de seguir para a consulta da nota, a tela também devolve o controle para a
**tela de consulta da nota fiscal** (`N025T`) quando a resposta traz a marca de
consulta, e para o **menu `N060M`** quando o percurso chega ao último item sem que a
nota tenha sido tratada.

[?] A ida para o menu é marcada com o nome `N025E`, que não é código de tela em lugar
nenhum do acervo — não há tela com esse nome no despacho do sistema, nem programa, nem
ficha. O que `N025E` designa é pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta da nota fiscal por item, com saída para a consulta da nota

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N026T

  Cenário: Ver o que a nota fiscal registra
    Dado que a tela de consulta da nota fiscal me entregou uma nota localizada
    Quando a tela abre
    Então vejo o nome do fornecedor, o valor total da nota e o valor total retido
    E vejo o tipo de contrato, o número do pedido, o ano da entrega e o número do processo
    E vejo a descrição do tipo de órgão, a descrição da secretaria e o nome do operador
    E vejo as datas de emissão da nota e do documento

  Cenário: Ver as linhas de gênero da nota
    Dado que a nota tem gêneros cadastrados no seu cadastro de itens
    Quando a tela abre
    Então vejo até 8 linhas, uma por gênero
    E cada linha traz o código da subclasse, o código do gênero, a descrição resumida, a unidade de medida, a quantidade, o valor unitário e o valor total do item

  Cenário: A descrição do gênero vem do cadastro de gêneros
    Dado que o par subclasse e gênero da linha está cadastrado para o ano de emissão da nota
    Quando a tela abre
    Então a linha mostra a descrição resumida do gênero e a unidade de medida do cadastro

  Cenário: Par subclasse e gênero não cadastrado no ano da nota
    Dado que o par subclasse e gênero da linha não está cadastrado para o ano de emissão da nota
    Quando a tela abre
    Então aquela linha não é mostrada

  Cenário: O item lido não confere com o número do processo da nota
    Dado que o item da nota não confere com o número do processo da nota
    Quando a tela abre
    Então aquela linha fica sem quantidade e sem valores
    E a tela segue sem aproveitar o item

  Cenário: Nota sem gêneros cadastrados
    Dado que a nota não tem nenhum item no seu cadastro de itens
    Quando a tela abre
    Então vejo a mensagem "* Nota fiscal sem generos cadastrados *"
    E a tela encerra sem mostrar registro

  Cenário: Campos numéricos são convertidos antes da procura
    Dado que digitei o número da nota fiscal com zeros à esquerda
    Quando respondo a tela
    Então o sistema converte o que digitei e descarta os zeros à esquerda
    E o campo em branco vira zero

  Cenário: A operação não é consulta
    Dado que a operação com que a tela foi acionada não é consulta
    Quando a tela procura o pedido da nota
    Então vejo a mensagem "* Use somente com opcao CON *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: O pedido da nota não é de pedido acumulado
    Dado que o pedido da nota não é de pedido acumulado
    Quando a tela confere o pedido
    Então vejo a mensagem "* Pedido nao acumulado *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: Seguir para a consulta da nota
    Dado que consultei uma nota pela tela de consulta da nota fiscal
    E a nota tem gêneros cadastrados
    Quando a tela termina a consulta
    Então sou encaminhado à consulta da nota fiscal
    E o número da nota, o fornecedor, o ano das datas fiscais, o número do processo e o gênero da última linha vão comigo

  Cenário: Voltar da consulta da nota fiscal
    Dado que fui daqui para a consulta da nota fiscal
    Quando a consulta da nota fiscal devolve o controle
    Então esta tela reabre com o número da nota fiscal apagado
    E o resto da consulta anterior fica restabelecido
    E nenhum registro é mostrado

  Cenário: A tela é só de consulta
    Dado que abri a tela N026T
    Quando respondo a tela
    Então nenhum cadastro é gravado
    E nenhuma nota fiscal, item ou pedido é incluído, alterado ou excluído
```
