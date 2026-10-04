# US — P535C — Consulta de empenhos do exercício

## Estória

Como **servidor de CRE**, quero **consultar os empenhos do exercício que estão no
arquivo do ano, pelo próprio número do empenho ou pelo fornecedor, e ver os
contratos de cada um**, para que **eu localize rapidamente o empenho que preciso
conferir e saiba a que contratos ele está amarrado, sem varrer a relação inteira**.

O empenho é o registro que amarra o gasto da CRE ao fornecedor e ao contrato. A
relação do exercício é grande e a CRE precisa de dois caminhos curtos até um
empenho: pelo número dele e pelo fornecedor que o atende. Esta é a tela em que
esses dois caminhos se abrem, com o que já está cadastrado no arquivo do ano — e é
dela que o servidor segue para a tela do empenho quando quer ver o contrato de
perto. Sem ela, a única forma de chegar a um empenho seria pela relação completa,
e o tipo de contrato de cada empenho não teria por onde ser conferido de relance.

## Contexto

Jornada S000M → P000M → P500M → P535C.
Ator: servidor de CRE — nesta tela, consulta o empenho do exercício que está no
arquivo do ano, pelo número do empenho ou pelo fornecedor.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As telas anteriores da jornada não deixam dado de negócio para esta tela: a `P000M`
e a `P500M` são menus e só encaminham. O contexto que a `P535C` usa — a matrícula, a
CRE, o órgão, o tipo de órgão e a data do sistema — é o que a entrada deixou na
sessão. A `P500M` chama a tela já com o pedido de consulta à vista; é por isso que a
tela abre mostrando o exercício e não espera o servidor digitar nada.

A `P535C` também é alcançada encadeada, sem passar por menu: a tela do empenho,
`P535T`, pede a volta para a `P535C` pela mesma passagem — e é para a `P535T` que a
`P535C` encaminha quando o servidor assinala uma linha preenchida (RN-08).

As regras abaixo são só as da tela desta jornada. A conferência de tela cadastrada
e de matrícula habilitada é da entrada e ficou no anexo de evidências, em
`## Regras que se revelaram da entrada`.

## Regras de negócio

### RN-01 — Ao abrir, a tela mostra o exercício e as linhas que o fornecedor já tem no arquivo do ano

Abrir a tela não grava nada. Ela começa mostrando o ano do exercício — o que o
servidor informou ou, não informando nenhum, o ano da data do sistema — e monta as
linhas com o que achar para aquele exercício: os empenhos do órgão da sessão para o
fornecedor já posicionado. Cada linha mostra o número do empenho, o código do
fornecedor, a marca de situação e a razão social do fornecedor, que vem do cadastro
de fornecedores.

[?] A leitura que monta as linhas começa zerando o fornecedor e o número do
empenho; é a busca pelo exercício que posiciona a primeira linha. Se o operador
pode abrir a tela com um fornecedor informado e ver só os empenhos dele, ou se a
primeira linha é sempre a primeira do exercício para o órgão, não se lê nestes
fontes. Pergunta ao site.

### RN-02 — O ano do exercício é obrigatório e, em branco, é o ano do sistema

Informar o ano do exercício é obrigatório. Deixando-o em branco, a tela não recusa:
ela adota o ano da data do sistema e segue a consulta com ele.

### RN-03 — Com o número do empenho preenchido, a tela confere o empenho

Preenchendo o número do empenho, a tela procura o empenho daquele número no
exercício, para o órgão da sessão e o fornecedor informado. Não achando empenho
nenhum, a recusa é **\* Nao existem empenhos cadastrados \***, com o cursor no
campo do número do empenho, e nada é gravado.

### RN-04 — Sem empenho no exercício informado, a abertura avisa

Não achando empenho nenhum para o exercício informado, a abertura avisa
**\* Nao existem empenhos cad para este ano \***, com o cursor no campo do ano, e
não mostra linha nenhuma.

### RN-05 — A linha do empenho mostra os contratos do empenho

Cada linha mostra ainda os tipos de contrato do empenho: a tela percorre os
contratos daquele empenho e lista os códigos, um ao lado do outro, no espaço da
linha. Esse espaço comporta até cinco códigos; havendo mais contratos do que isso,
os que passam do quinto não aparecem.

### RN-06 — O fornecedor sem cadastro não é recusado: a linha sai sem a razão social

A razão social da linha vem do cadastro de fornecedores, pelo código do fornecedor
da linha. Não achando o fornecedor no cadastro, a tela não recusa e não avisa: a
linha é mostrada com a razão social em branco, e a consulta segue.

### RN-07 — A linha preenchida não se abre pela tela: ela é conferida na tela do empenho

Assinalar uma linha que já está preenchida com um número de empenho e com a marca
de consulta pede a abertura da tela do empenho, `P535T`, com a operação de consulta.
O número do empenho e o ano que a linha mostra ficam na tela; a `P535T` é que os
procura e os exibe.

### RN-08 — A linha marcada sem número de empenho é recusada

Assinalando uma linha que está marcada com a situação, mas sem número de empenho, a
recusa é **\* Consulte linha preenchida \***, com o cursor na posição assinalada, e
nada é gravado.

### RN-09 — A tela não inclui, não altera e não exclui

A operação desta tela é a consulta. Informada qualquer outra operação, a recusa é
**\* Opcao nao disponivel. Use CON \***, com o cursor no campo da operação, e nada é
gravado. A tela apenas lê: o cadastro de telas, o cadastro de empenhos, o cadastro
de fornecedores e o cadastro de contratos do empenho. Alterar ou excluir empenho é
na tela do empenho, `P535T`, não aqui.

### RN-10 — Ao mudar de tela, o que segue são a operação e o fornecedor

Pedida a abertura da tela do empenho, a `P535C` não altera o modo da tela seguinte:
ela entrega a operação de consulta e o código do fornecedor, e a `P535T` abre em
consulta.

[?] A tela promete levar o empenho assinalado, e a linha que o servidor escolheu
está na primeira posição da relação no momento da passagem. A `P535C` não leva,
porém, o número do empenho nem a marca de situação da linha escolhida para a área
que a `P535T` lê: leva a operação e o fornecedor, e o número do empenho e o ano com
que a `P535T` vai procurar são os da última leitura que a abertura da `P535C` fez.
Se a `P535T` abre no empenho assinalado ou no primeiro empenho daquele fornecedor no
exercício, não se lê nestes fontes. Pergunta ao site.

### RN-11 — Os campos informados passam pela edição numérica

O ano do exercício, o número do empenho e o código do fornecedor são editados como
número antes de qualquer conferência: o que estiver em branco vira zero, os zeros à
esquerda são descartados e os separadores que o servidor digitar são retirados. O
que não passar pela edição é recusado com o cursor devolvido ao campo, e nada é
gravado.

### RN-12 — A tela não abre sobre a tela, nem sobre uma mensagem já respondida

Chamada de novo por outra tela enquanto o código da tela que a chamou estiver
preenchido, a operação é encerrada em silêncio: nada é mostrado, nada é gravado e
nenhuma mensagem aparece. O mesmo acontece quando a área de trabalho da tela já vem
marcada como processada. Uma mensagem que a tela já respondeu é descartada sem ser
tratada de novo.

## Cenários BDD

```gherkin
Funcionalidade: Consulta do empenho do exercício no arquivo do ano, pelo número do empenho ou pelo fornecedor

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela P535C

  Cenário: Abertura mostra o exercício e as linhas do fornecedor no arquivo do ano
    Dado que o órgão da minha sessão tem empenhos no arquivo do ano
    Quando abro a tela P535C
    Então vejo o ano do exercício
    E vejo as linhas dos empenhos, com o número do empenho, o fornecedor, a marca de situação e a razão social
    E nada é gravado

  Cenário: Sem ano informado, a tela usa o ano do sistema
    Dado que abro a tela P535C sem informar o ano
    Quando confirmo a consulta
    Então a tela consulta o exercício pelo ano da data do sistema
    E nada é gravado

  Cenário: Empenho não encontrado
    Dado que estou na tela P535C
    Quando informo um número de empenho que não existe no exercício e confirmo a consulta
    Então vejo a mensagem "* Nao existem empenhos cadastrados *"
    E o cursor fica no campo do número do empenho
    E nada é gravado

  Cenário: Nenhum empenho no exercício informado
    Dado que o exercício informado não tem empenho cadastrado para o órgão da minha sessão
    Quando confirmo a consulta
    Então vejo a mensagem "* Nao existem empenhos cad para este ano *"
    E o cursor fica no campo do ano
    E nenhuma linha é mostrada

  Cenário: A linha mostra os contratos do empenho
    Dado que o empenho em tela tem contratos cadastrados
    Quando a linha é montada
    Então vejo os códigos dos contratos daquele empenho na linha

  Cenário: Fornecedor sem cadastro não impede a linha
    Dado que o fornecedor da linha não está no cadastro de fornecedores
    Quando a linha é montada
    Então a linha aparece com a razão social em branco
    E a consulta não é recusada

  Cenário: Linha preenchida é conferida na tela do empenho
    Dado que uma linha está preenchida com número de empenho e com a marca de consulta
    Quando assinalo essa linha e confirmo
    Então a tela do empenho, P535T, é aberta com a operação de consulta
    E o número do empenho e o ano que a linha mostra ficam na tela

  Cenário: Linha marcada sem número de empenho é recusada
    Dado que uma linha está marcada com a situação, mas sem número de empenho
    Quando assinalo essa linha e confirmo
    Então vejo a mensagem "* Consulte linha preenchida *"
    E o cursor fica na posição assinalada
    E nada é gravado

  Cenário: A consulta não grava nada
    Dado que o empenho consultado existe no arquivo do ano
    Quando confirmo a consulta
    Então nenhum empenho, fornecedor ou contrato é incluído, alterado ou excluído

  Cenário: Operação diferente da consulta é recusada
    Dado que estou na tela P535C
    Quando informo uma operação que não é a de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: Campo não numérico é recusado
    Dado que informo um número de empenho que não é número
    Quando confirmo a mensagem
    Então a tela recusa o campo antes de consultar o cadastro
    E o cursor volta para o campo
    E nada é gravado

  Cenário: A tela não se abre sobre a tela
    Dado que a tela P535C já está aberta
    Quando outra tela a chama de novo
    Então a operação é encerrada sem mensagem
    E nada é gravado
```
