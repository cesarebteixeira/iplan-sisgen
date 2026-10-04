# US — P535T — Manter tipos de contrato do empenho do exercício

## Estória

Como **servidor de CRE**, quero **manter os tipos de contrato que estão amarrados a um
empenho do exercício — incluindo e tirando tipo a tipo — e consultá-los**, para que
**o empenho do arquivo do ano aponte para os contratos certos do fornecedor e a CRE
possa conferir, empenho a empenho, a que contratos ele está preso**.

O empenho do exercício é registrado por órgão, ano, número do empenho e fornecedor, e
cada registro dele vale por um tipo de contrato: é o conjunto desses registros que diz
a que contratos o empenho atende. Esta é a tela em que esse conjunto é montado — o
servidor da CRE abre o empenho, vê os tipos de contrato que ele já tem e inclui ou
retira os que faltam ou sobram. Sem ela, o empenho nasceria sem tipo de contrato
nenhum, e a consulta dos empenhos do exercício não teria contrato nenhum para mostrar
ao lado de cada linha.

## Contexto

Jornada S000M → P000M → P500M → P535T.
Ator: servidor de CRE — nesta tela, monta e confere os tipos de contrato de cada
empenho do exercício.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada — `P000M` e `P500M` — são menus: só encaminham e
não deixam dado de negócio para esta tela. O contexto que a `P535T` usa — a matrícula,
a CRE, o órgão da sessão, o tipo de órgão, o código de acesso, a estação e a data do
sistema — é o que a entrada deixou na sessão; a `P500M` é quem pede a abertura desta
tela.

A `P535T` também é alcançada encadeada, sem passar por menu: a tela dos empenhos do
exercício, `P535C`, pede a abertura dela quando o servidor assinala uma linha
preenchida — e é para a `P535C` que a `P535T` encaminha de volta quando o campo de
consulta da tela vem marcado (RN-13). Como ela recebe de quem a chamou a operação e o
empenho com que abre, o modo dela depende da origem (RN-03).

As regras abaixo são só as da tela desta jornada. A conferência de tela cadastrada e
de matrícula habilitada é da entrada e ficou no anexo de evidências, em
`## Regras que se revelaram da entrada`.

## Regras de negócio

### RN-01 — Ao abrir, a tela mostra os tipos de contrato do empenho

Abrir a tela não grava nada: ela mostra o número do empenho, o ano de referência e o
código do fornecedor que quem a chamou deixou, mais a data do sistema e o órgão da
sessão, e monta as linhas com os tipos de contrato que aquele empenho tem no arquivo
do ano — até treze linhas, cada uma com o tipo de contrato e a marca da linha. Não
havendo contrato nenhum para aquele empenho, a abertura avisa (RN-02).

[?] A tela monta as linhas em uma tabela que ela reordena, posição a posição, antes de
mostrar: a linha que o operador vê na primeira posição pode ser outra da leitura. Se o
efeito é só de ordenação, ou se a primeira linha é mostrada trocada, não se lê nos
fontes desta jornada. Pergunta ao site.

[?] A leitura que percorre os contratos do empenho é uma leitura posicionada, e é ela
que diz se a tela percorre todos os contratos daquele empenho ou para no primeiro. O
recurso de leitura posicionada vem de fora do acervo; quantos contratos a tela alcança
não se lê nestes fontes. Pergunta ao site.

[?] Os nomes das colunas que o operador vê não estão no lote: o que se lê no fonte são
os quatro rótulos de conferência — **NUM.EMPENHO**, **ANO REFERENCIA**,
**COD.FORNECEDOR** e **TIPO DE CONTRATO** —, e a ficha da tela registra que a máscara
pode ter outros. Pergunta ao site.

### RN-02 — Sem contrato cadastrado para o empenho, a abertura avisa

Não achando contrato nenhum para o empenho, o ano e o fornecedor que a tela recebeu, a
abertura avisa **\* Nao existem contratos cadastrados \***, não mostra linha nenhuma e
não grava nada. O aviso não sai quando a tela abre pelo menu, sem empenho informado:
nesse caso ela nem procura contrato.

### RN-03 — O modo da tela é o que a tela que a chamou deixou

A tela não decide sozinha se abre em consulta ou em alteração: ela recebe a operação, o
empenho, o ano e o fornecedor de quem a chamou, pela área de passagem da sessão. Vinda
do menu, sem operação nenhuma, ela abre em consulta e adota o ano da data do sistema,
sem procurar contrato e sem mostrar linha — é o servidor que informa o empenho e o
fornecedor e confirma. Vinda da tela dos empenhos, encadeada, ela abre com a operação
e o empenho que aquela tela deixou e já mostra os contratos daquele empenho (RN-01).

[?] A área de passagem da sessão é inicializada uma única vez, no começo da sessão, e o
acervo não diz quando ela é reiniciada. Se a operação de uma transação anterior
sobrevive até a abertura seguinte pelo menu, a tela pode abrir em alteração com o
empenho da transação anterior. Pergunta ao site.

### RN-04 — As operações da tela são a consulta e a alteração

A tela só aceita a consulta e a alteração; é pela alteração, com a marca da linha, que
se inclui e se exclui tipo de contrato (RN-06 e RN-07). Informada outra operação, a
recusa é **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no campo da
operação, e nada é gravado.

[?] A tela manda usar ALT e CON, mas compara o que foi informado com os códigos de
operação do sistema, e a máscara, que poderia traduzir um vocabulário no outro, não
está no acervo. Se o servidor digitar exatamente o que a mensagem manda, a operação
pode ser recusada na conferência. Pergunta ao site.

### RN-05 — Alterar exige ter consultado antes

Para alterar, o número do empenho, o ano de referência e o código do fornecedor
informados têm de ser os mesmos que a tela carregou na abertura. Informando outro, a
recusa é **\* Consulte antes de atualizar \***, com o cursor no campo do número do
empenho, e nada é gravado: a alteração só age sobre o empenho que a tela já trouxe.

### RN-06 — A linha marcada para incluir acrescenta o tipo de contrato ao empenho

Marcando a linha com a marca de inclusão e confirmando com a alteração, a tela
acrescenta aquele tipo de contrato ao empenho do fornecedor em tela. A inclusão passa
por quatro conferências, nesta ordem: o tipo de contrato tem de estar preenchido —
senão **\* Atualize linha preenchida \***, com o cursor na marca da linha, e nada é
gravado; aquele tipo não pode já estar ligado àquele empenho daquele fornecedor —
senão **\* Tipo contrato ja cadastrado \***, no mesmo cursor; o tipo tem de estar
cadastrado para o órgão da sessão — senão **\* Tipo contrato nao cadastrado \***; e o
fornecedor tem de ter contrato daquele tipo — senão
**\* Tipo contrato nao cad. para este fornecedor \***.

Passando as quatro, a tela grava o vínculo entre o órgão, o ano, o empenho, o
fornecedor e o tipo de contrato, e registra a inclusão na auditoria com o vínculo
novo, a matrícula, a CRE, o órgão, a estação e o dia e a hora da sessão.

[?] A tela não confere se o empenho existe antes de ligar o primeiro tipo de contrato a
ele: o vínculo é gravado pela chave do empenho que a tela carregou, sem leitura que
comprove que aquele empenho já está no arquivo do ano. Se a máscara ou a tela que a
chamou garantem esse empenho, não se lê nestes fontes. Pergunta ao site.

### RN-07 — A linha marcada para excluir tira o tipo de contrato do empenho

Marcando a linha com a marca de exclusão e confirmando com a alteração, a tela tira
aquele tipo de contrato do empenho. A exclusão exige o tipo de contrato preenchido —
senão **\* Atualize linha preenchida \***, com o cursor na marca da linha — e exige o
vínculo existente para aquele empenho, aquele fornecedor e aquele tipo — senão
**\* Tipo contrato nao cadastrado \***, no mesmo cursor, e nada é apagado.

Passando, a tela apaga o vínculo daquele empenho com aquele fornecedor e aquele tipo de
contrato e registra a exclusão na auditoria com o vínculo como estava — o ano, o
empenho, o fornecedor e o tipo de contrato —, a matrícula, a CRE, o órgão, a estação e
o dia e a hora da sessão.

[?] A mesma mensagem, **\* Tipo contrato nao cadastrado \***, sai em duas situações
diferentes: quando o tipo informado não está cadastrado para o órgão (na inclusão) e
quando o empenho não tem aquele tipo de contrato (na exclusão). O operador não
distingue as duas pela mensagem. Se é para distinguir, não se lê nestes fontes.
Pergunta ao site.

### RN-08 — A consulta exige o empenho, o ano e o fornecedor

Na consulta, o número do empenho, o ano de referência e o código do fornecedor têm de
estar informados. Sem o número do empenho, a recusa é
**\* Informe o numero do empenho \***, com o cursor no campo do empenho; sem o ano,
**\* Informe o ano do exercicio \***, com o cursor no campo do ano; sem o fornecedor,
**\* Informe o fornecedor \***, com o cursor no campo do fornecedor. Em qualquer dos
casos nada é gravado.

### RN-09 — A consulta não inclui nem altera contrato

A consulta só mostra: ela lê o cadastro dos empenhos do exercício e o cadastro de
fornecedores e monta a tela — o tipo de contrato de cada linha, a razão social do
fornecedor e o código que a tela mostra ao lado dele vêm do cadastro, não de cálculo da
tela. Nenhum tipo de contrato é incluído ou alterado por uma consulta; incluir e
excluir é na alteração (RN-06 e RN-07).

[?] Há, no caminho da consulta, um trecho que apaga o registro sem tipo de contrato
quando o empenho tem, ao mesmo tempo, registro sem tipo de contrato e registro com
tipo — e esse trecho está no caminho da consulta, não no da alteração. A leitura que o
alimenta é posicionada e vem de fora do acervo: se ela alcança os dois tipos de
registro, a consulta apaga um registro sem que o operador tenha pedido. Não se lê
nestes fontes se o trecho é alcançado. Pergunta ao site.

### RN-10 — Os campos informados passam pela edição numérica

O número do empenho, o ano de referência, o código do fornecedor e o tipo de contrato
são editados como número antes de qualquer conferência: o que estiver em branco vira
zero, os zeros à esquerda são descartados e os separadores que o servidor digitar são
retirados. O que não passar pela edição é recusado com o cursor devolvido ao campo, e
nada é gravado.

### RN-11 — A tela não se abre sobre ela mesma

Chamada de novo por outra tela enquanto o código da tela que a chamou estiver
preenchido, a operação é encerrada em silêncio: nada é mostrado, nada é gravado e
nenhuma mensagem aparece. O mesmo acontece quando a área de passagem da tela já vem
marcada como processada.

### RN-12 — Nada acontece sem a tela e a matrícula habilitadas

Ao abrir, o sistema confere, com o contexto da sessão, se a tela está cadastrada e se a
matrícula tem a tela no seu código de acesso; não estando, a recusa é
**\* Tela nao disponivel \*** ou **\* Acesso negado para esta matricula \***, e a
operação não segue. Na operação, a tela passa ainda pela lógica de rota, que recusa a
operação que ela não reconhece (**\* Operacao nao disponivel \***) e a tela retirada do
cadastro (**\* Tela nao cadastrada \***), e o código de acesso da operação exige a
autorização da operação informada (**\* Acesso negado para esta operacao \***).

### RN-13 — O campo de consulta marcado entrega o empenho à tela dos empenhos

Marcando o campo de consulta da tela, a operação não segue nesta tela: ela pede a
abertura da tela dos empenhos do exercício, `P535C`, entregando o ano e o número do
empenho que achou — com o código do fornecedor em branco — e a operação que já estava
na sessão. É essa entrega que decide o que a tela dos empenhos mostra; e, como aquela
tela só aceita a consulta, ela recusa a entrega feita em alteração.

[?] Nenhum trecho desta jornada preenche o campo de consulta: a tela só o lê e o
mostra. Se quem o preenche é o operador, a máscara ou a tela que a chamou, não se lê
nestes fontes. Pergunta ao site.

[?] O empenho que segue pode não ser o que está na tela: a leitura que antecede a
entrega confere só o órgão e o ano, e o número do empenho que ela leva é o do registro
que a leitura achou. Se a leitura está posicionada no empenho informado ou apenas no
ano — e, portanto, se a tela seguinte abre no empenho em tela ou no primeiro empenho do
exercício para o órgão —, não se lê nestes fontes. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manutenção e consulta dos tipos de contrato do empenho do exercício

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela P535T

  Cenário: Abertura mostra os tipos de contrato do empenho
    Dado que o empenho que a tela recebeu tem tipos de contrato no arquivo do ano
    Quando abro a tela P535T
    Então vejo o número do empenho, o ano de referência e o código do fornecedor
    E vejo as linhas com os tipos de contrato daquele empenho, cada uma com a sua marca
    E nada é gravado

  Cenário: O empenho não tem tipo de contrato
    Dado que o empenho que a tela recebeu não tem tipo de contrato no arquivo do ano
    Quando abro a tela P535T
    Então vejo a mensagem "* Nao existem contratos cadastrados *"
    E nenhuma linha é mostrada
    E nada é gravado

  Cenário: Abertura pelo menu entra em consulta com o ano do sistema
    Dado que quem me chamou não deixou operação nenhuma
    Quando abro a tela P535T
    Então a tela abre em consulta
    E o ano de referência é o ano da data do sistema
    E nenhuma linha é mostrada
    E nada é gravado

  Cenário: Abertura encadeada pela tela dos empenhos
    Dado que a tela dos empenhos me encaminhou com o empenho e a operação de consulta
    Quando abro a tela P535T
    Então vejo os tipos de contrato daquele empenho
    E nada é gravado

  Cenário: Operação diferente de consulta e alteração é recusada
    Dado que estou na tela P535T
    Quando informo uma operação que não é a de consulta nem a de alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: Alteração de um empenho que a tela não carregou é recusada
    Dado que informo um número de empenho diferente do que a tela carregou
    Quando confirmo a alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor fica no campo do número do empenho
    E nada é gravado

  Cenário: Inclusão de um tipo de contrato no empenho
    Dado que o empenho em tela não tem o tipo de contrato que quero incluir
    E o tipo de contrato está cadastrado para o órgão da minha sessão
    E o fornecedor em tela tem contrato daquele tipo
    Quando marco a linha com a marca de inclusão, informo o tipo de contrato e confirmo com a alteração
    Então o tipo de contrato passa a estar ligado àquele empenho daquele fornecedor
    E a inclusão fica registrada na auditoria com o vínculo novo e com quem operou, a CRE, o órgão, a estação e o dia e a hora da sessão

  Cenário: Inclusão com a linha sem tipo de contrato é recusada
    Dado que marco a linha com a marca de inclusão e deixo o tipo de contrato em branco
    Quando confirmo com a alteração
    Então vejo a mensagem "* Atualize linha preenchida *"
    E o cursor fica na marca da linha
    E nada é gravado

  Cenário: Tipo de contrato já ligado ao empenho é recusado
    Dado que o empenho em tela já tem o tipo de contrato que informo
    Quando marco a linha com a marca de inclusão e confirmo com a alteração
    Então vejo a mensagem "* Tipo contrato ja cadastrado *"
    E o cursor fica na marca da linha
    E nada é gravado

  Cenário: Tipo de contrato não cadastrado para o órgão é recusado
    Dado que informo um tipo de contrato que não está cadastrado para o órgão da minha sessão
    Quando marco a linha com a marca de inclusão e confirmo com a alteração
    Então vejo a mensagem "* Tipo contrato nao cadastrado *"
    E o cursor fica na marca da linha
    E nada é gravado

  Cenário: Tipo de contrato sem contrato do fornecedor é recusado
    Dado que o fornecedor em tela não tem contrato do tipo de contrato informado
    Quando marco a linha com a marca de inclusão e confirmo com a alteração
    Então vejo a mensagem "* Tipo contrato nao cad. para este fornecedor *"
    E o cursor fica na marca da linha
    E nada é gravado

  Cenário: Exclusão de um tipo de contrato do empenho
    Dado que o empenho em tela tem o tipo de contrato que quero excluir
    Quando marco a linha com a marca de exclusão, informo o tipo de contrato e confirmo com a alteração
    Então o tipo de contrato deixa de estar ligado àquele empenho daquele fornecedor
    E a exclusão fica registrada na auditoria com o vínculo como estava e com quem operou, a CRE, o órgão, a estação e o dia e a hora da sessão

  Cenário: Exclusão com a linha sem tipo de contrato é recusada
    Dado que marco a linha com a marca de exclusão e deixo o tipo de contrato em branco
    Quando confirmo com a alteração
    Então vejo a mensagem "* Atualize linha preenchida *"
    E o cursor fica na marca da linha
    E nada é apagado

  Cenário: Exclusão de tipo de contrato que o empenho não tem é recusada
    Dado que o empenho em tela não tem o tipo de contrato que informo
    Quando marco a linha com a marca de exclusão e confirmo com a alteração
    Então vejo a mensagem "* Tipo contrato nao cadastrado *"
    E o cursor fica na marca da linha
    E nada é apagado

  Cenário: Consulta sem o número do empenho é recusada
    Dado que deixo o número do empenho em branco
    Quando confirmo a consulta
    Então vejo a mensagem "* Informe o numero do empenho *"
    E o cursor fica no campo do número do empenho
    E nada é gravado

  Cenário: Consulta sem o ano do exercício é recusada
    Dado que deixo o ano de referência em branco
    Quando confirmo a consulta
    Então vejo a mensagem "* Informe o ano do exercicio *"
    E o cursor fica no campo do ano
    E nada é gravado

  Cenário: Consulta sem o fornecedor é recusada
    Dado que deixo o código do fornecedor em branco
    Quando confirmo a consulta
    Então vejo a mensagem "* Informe o fornecedor *"
    E o cursor fica no campo do fornecedor
    E nada é gravado

  Cenário: A consulta não inclui nem altera contrato
    Dado que consulto um empenho cadastrado no arquivo do ano
    Quando confirmo a consulta
    Então nenhum tipo de contrato é incluído ou alterado naquele empenho
    E vejo os tipos de contrato que o empenho já tinha, com a razão social do fornecedor
    E nada é gravado

  Cenário: Campo não numérico é recusado
    Dado que informo um número de empenho que não é número
    Quando confirmo a mensagem
    Então a tela recusa o campo antes de ler o cadastro
    E o cursor volta para o campo
    E nada é gravado

  Cenário: A tela não se abre sobre ela mesma
    Dado que a tela P535T já está aberta
    Quando outra tela a chama de novo
    Então a operação é encerrada sem mensagem
    E nada é gravado

  Cenário: Tela não cadastrada
    Dado que a tela P535T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela P535T no seu código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Sem autorização para a operação
    Dado que o meu código de acesso não tem a operação informada liberada para a tela P535T
    Quando confirmo a mensagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Operação não reconhecida
    Dado que informo uma operação que a tela não reconhece
    Quando confirmo a mensagem
    Então vejo a mensagem "* Operacao nao disponivel *"
    E nada é gravado

  Cenário: Tela retirada do cadastro
    Dado que a tela P535T foi retirada do cadastro de telas
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é gravado

  Cenário: O campo de consulta marcado entrega o empenho à tela dos empenhos
    Dado que marco o campo de consulta da tela
    Quando confirmo a consulta
    Então a tela dos empenhos do exercício, P535C, é aberta
    E ela recebe o ano e o número do empenho, com o código do fornecedor em branco
```
