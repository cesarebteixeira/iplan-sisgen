# US — E507T — Consultar o pedido de fornecimento de um órgão filho

## Estória

Como **servidor de CRE**, quero **consultar o pedido de fornecimento de um órgão
filho — o órgão, a coordenadoria regional escolar, o mês de referência do cálculo,
os períodos de cálculo e de distribuição, o cardápio da semana e as quantidades
calculadas por grupo**, para que **a secretaria confira, antes de distribuir, para
quais grupos e em que quantidade o preparo daquele órgão foi aprovado, sem ter de
somar permissão por permissão**.

O programa de alimentação escolar precisa, para cada unidade, de um pedido de
fornecimento vigente, com data de início e de limite, um cardápio amarrado ao
calendário da unidade e a quantidade calculada para cada grupo de gêneros. Quem
atende a unidade confere por esta tela se o pedido existe, se o período de
distribuição está completo e se o cardápio e as quantidades conferem com o que foi
pedido. Se essa conferência não existir, a distribuição e a impressão saem sobre um
pedido que ninguém validou — e o erro só aparece depois, no fornecedor ou na
entrega.

A tela é de consulta: ela não inclui, não altera e não exclui nada no acervo. O que
ela entrega é a leitura do pedido — e, quando o pedido consultado já tem o período
de distribuição completo, ela devolve o servidor à tela de origem com essa
indicação, em lugar de seguir adiante.

## Contexto

Jornada S000M → E000M → E500M → E507T.

Ator: servidor de CRE — informa o órgão filho ou a coordenadoria regional escolar e
a data de referência do cálculo, e vê na tela o período, o cardápio da semana e as
quantidades calculadas por grupo; a tela não grava nada.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Da sessão a tela usa o tipo de órgão (a secretaria), a coordenadoria regional
escolar e o órgão filho do vínculo, além da matrícula, do código de acesso e da
estação, que as conferências de acesso leem; e a data e a hora do sistema, que
aparecem no cabeçalho e alimentam os pedidos de impressão. A mesma tela é alcançada
também depois do processamento do cálculo do pedido — outra origem, o mesmo
comportamento.

Para trás, a tela volta à `E500T` quando os dados do período não fecham. Para
frente, quando o pedido tem o período de distribuição completo, ela passa para a
`E505T` — a tela dos pedidos — levando o órgão, a coordenadoria, as datas do
período e o mês de referência do cálculo que consultou. Ela também sabe pedir a
impressão do relatório do preparo e o envio do arquivo digital do órgão.

As regras abaixo são só as da tela desta jornada. O que já está na entrada não se
repete aqui.

---

## Regras de negócio

### RN-01 — A tela é de consulta: ela não inclui, não altera e não exclui nada

A tela só consulta. Ao ser preparada, ela mesma põe a operação de consulta no campo
da operação, e qualquer outra operação que chegue é recusada com
**\* Opcao nao disponivel. Use CON \***, o cursor volta ao campo da operação e nada
mais é lido. A operação não é conferida contra a autorização do código de acesso: a
consulta não tem conferência de operação própria.

Por não escrever, a tela não inclui, não altera e não exclui registro nenhum do
acervo — nem do órgão, nem do pedido, nem da quantidade calculada, nem do
calendário. A simples abertura também não escreve nada.

O que ela pode fazer é **pedir a impressão**: enfileira o pedido do relatório do
preparo, para ser impresso e enviado por correio eletrônico à estação do servidor,
e o pedido do envio do arquivo digital do órgão. Isso é um pedido de serviço, não
uma alteração de cadastro.

[?] A tela repõe a operação de consulta a cada passagem e manda usar a tecla CON; o
programa que a antecede na trilha do cálculo, porém, manda para ela a operação de
alteração. Ou a operação que chega é indiferente para a consulta, ou uma das duas
telas ficou com a operação trocada. Não se escolhe um dos dois lados: pergunta ao
site.

### RN-02 — A tela confere a sessão, o registro da tela e o acesso do servidor

Na abertura, a tela confere que o servidor está na **estação em que a sessão foi
aberta** (em outra, o acesso é encerrado e a sessão volta à entrada), que a tela
está registrada (senão **\* Tela nao disponivel \***), que ela pertence ao módulo
da sessão, que o código de acesso alcança a tela e que existe uma **autorização do
código de acesso** para ela (senão **\* Acesso negado para esta matricula \***).
Sem passar por essas conferências, nada é mostrado e nada é gravado.

[?] A autorização do código de acesso traz, para cada tela, o que é permitido
incluir, alterar e excluir; não há indicação de consulta. Como a tela é de
consulta, não se conclui do acervo o que o servidor vê quando o código de acesso
não alcança a tela para consultar. Pergunta ao site.

### RN-03 — O órgão filho ou a coordenadoria é obrigatório, e o acesso é o do vínculo

O órgão filho ou a coordenadoria regional escolar tem de vir informado. O que
estiver informado serve de ponto de partida: se a área de trabalho já traz um órgão
filho, a tela o usa e não o procura pelo que foi digitado; se traz a coordenadoria,
idem. Sem órgão nenhum, a recusa é **\* Informe o orgao \***, com o cursor no
órgão, e nada é lido.

Com o órgão informado, a tela exige que ele exista. Não existindo, a recusa é
**\* Orgao nao cadastrado \***, com o cursor no órgão, e nada mais é lido. Quando o
vínculo do servidor carrega um órgão filho, o informado tem de ser esse, senão
**\* Usuario sem acesso a outro orgao \***; e, quando carrega uma coordenadoria
regional escolar, a coordenadoria **do órgão cadastrado** tem de ser a mesma, senão
**<- Usuario sem acesso ao grupo deste orgao \***. Nas duas recusas o cursor volta
ao órgão.

Achando o órgão, a tela passa a usar a coordenadoria que está nele em todas as
leituras, mostra a descrição do órgão no cabeçalho e guarda, do cadastro do órgão,
a indicação de creche — que decide, mais adiante, como o período se apresenta.

### RN-04 — A data de referência do cálculo é obrigatória

Se a abertura não encheu as datas do cálculo e o servidor não informou o dia de
início do preparo, a recusa é **\* Informe a data de inicio do preparo \***, com o
cursor no dia, e nada é lido. Só o dia é exigido campo a campo: o mês e o ano da
mesma data, em branco, valem zero e a procura não acha — o servidor vê
**\* Requisicao nao cadastrada \*** no lugar de uma recusa do campo que faltou.

### RN-05 — O período, o cardápio e as quantidades vêm do pedido de fornecimento

Existindo o pedido para o órgão, a coordenadoria, a data de referência do cálculo,
a classe e o gênero, a tela traz para os campos: o **limite do cálculo**, o
**início do período** e o **limite do período** — dia, mês e ano de cada um —, e as
**quantidades calculadas** (sete). Não achando o pedido, a recusa é
**\* Requisicao nao cadastrada \***, no campo do dia, e nada é mostrado.

A tela também compõe e mostra a **classe e o gênero** do pedido, no formato
`classe.gênero`, com a descrição do gênero, e guarda a classe e o gênero da última
leitura como a classe e o gênero de **origem** — que seguirão com as datas do
período para a tela de destino.

Para o cardápio, a tela percorre **sete** dias a partir do primeiro dia do período
de cálculo e, para cada um, procura no **calendário da unidade** o dia da semana
correspondente; o que encontra vai para o campo do dia, junto da data, e a
indicação do calendário vai para o respectivo campo de semana. Achando o calendário
da unidade, ela ainda mostra, no primeiro dia, uma segunda informação do calendário
(um código de uma posição).

[?] O mês de referência do cálculo é guardado e segue para a tela dos pedidos, mas
esta tela não o usa em nenhuma leitura nem em nenhuma conferência. Ou ele serve à
tela seguinte, ou ficou sem uso aqui. Pergunta ao site.

[?] A descrição do gênero e as quantidades são lidas de um cadastro de gênero por
classe que declara, entre os campos usados, apenas os do período (classe, gênero,
ano, mês e dia de início) e uma descrição; não se conclui do acervo de onde vêm as
sete quantidades calculadas que a tela mostra. Pergunta ao site.

### RN-06 — O período é conferido antes de qualquer avanço

Quando o pedido não traz os números do período, a tela não avança: ela volta à
tela anterior com a indicação de que a passagem não terminou. A conferência exige,
campo a campo: a data de início do cálculo; o limite do cálculo, que não pode ser
anterior ao início; o início do período; o limite do período, que não pode ser
anterior ao início; as **sete** indicações de semana do período; as **sete**
descrições dos dias do período; e a informação de creche do órgão. Faltando ou
desrespeitando a ordem qualquer um deles, o servidor é devolvido à tela anterior, e
a tela não segue para a distribuição nem para o pedido de impressão.

A mesma verificação decide se o órgão é o do vínculo: quando o vínculo carrega um
órgão filho e o órgão consultado é outro, a tela também devolve o servidor à tela
anterior.

### RN-07 — O servidor informado tem de ter correio eletrônico cadastrado para a impressão

Para pedir a impressão, a tela exige o correio eletrônico do servidor no cadastro
do servidor. Não havendo, a recusa é **<- Usuario sem e-mail cadastrado \***, com o
cursor no campo da impressão, e nada é impresso nem enviado.

### RN-08 — O pedido de impressão e o envio do arquivo digital só andam com a distribuição em curso

A tela só pede a impressão do relatório do preparo quando a consulta está em curso
e o pedido de distribuição tem o órgão e o período informados; e só pede o envio do
arquivo digital do órgão quando a consulta está em curso e o campo de distribuição
está preenchido. Com o período já completo — o caso em que o pedido existente foi
achado inteiro —, a tela não segue para a distribuição: ela devolve o servidor à
tela anterior.

Antes de pedir, ela confere, para os dois pedidos, que não existe outro pedido do
mesmo tipo **em processamento** para o órgão: havendo, a recusa é
**\* Arquivo em processamento. Aguarde. \*** e
**\* Relatorio em processamento. Aguarde. \***, respectivamente, com o cursor no
campo do pedido, e nada é enfileirado.

[?] O pedido de impressão e o envio do arquivo digital só são enfileirados se os
campos do relatório e do arquivo chegarem preenchidos de fora da tela: a própria
tela os esvazia na cópia em que reproduz a tela inteira, e nada no acervo desta
tela os preenche. Não se conclui do acervo por qual caminho o servidor chega a
esses pedidos. Pergunta ao site.

### RN-09 — O período de distribuição completo devolve o servidor à tela anterior

Quando o pedido achado é montado — as sete descrições dos dias vêm do calendário
da unidade —, a tela **não** segue para a distribuição: ela encerra a passagem
devolvendo o servidor à tela anterior, com a indicação de que a passagem não
terminou, e leva de volta o órgão, a coordenadoria e o período consultados. É o
desfecho da consulta de um pedido que a tela conseguiu montar.

[?] As duas conferências do período não fecham entre si. A tela lê as sete
descrições dos dias do período no calendário da unidade e as preenche — e o
preenchimento das sete é justamente o que a outra conferência trata como passagem
não terminada, mandando o servidor de volta. Ou seja: a tela só avança no caminho
em que as sete descrições ainda estão em branco, e o estado que ela mesma produz é
o que a faz voltar. Não se conclui do acervo qual dos dois lados vale; pergunta ao
site.

### RN-10 — A tela entrega o órgão, a coordenadoria e o período à tela dos pedidos

A tela desta jornada não termina em si: alcançado o ponto de distribuição, ela
passa para a **E505T** — a tela dos pedidos — levando o órgão filho, a
coordenadoria, a classe e o gênero de origem, o mês de referência do cálculo, as
datas do período (início e limite) e as sete indicações de semana. A `E505T` abre,
por causa disso, no órgão e no período que foram consultados aqui, e não em branco
— e é lá que a distribuição acontece.

Voltando à tela anterior, ela leva de volta o órgão, a coordenadoria e o período
que consultou, para que a tela anterior retome o mesmo pedido.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar o pedido de fornecimento de um órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenadoria regional escolar
      e o órgão filho do meu vínculo
    E tenho acesso à tela E507T

  Cenário: Consultar o pedido de fornecimento de um órgão
    Dado que existe um pedido de fornecimento do órgão, com o período de cálculo e
      as quantidades calculadas por grupo
    E que o calendário da unidade cobre os sete dias do período
    Quando informo o órgão e a data de referência do cálculo e consulto
    Então vejo a descrição do órgão e a data do sistema no cabeçalho
    E vejo o limite do cálculo, o início e o limite do período
    E vejo a classe e o gênero do pedido com a descrição do gênero
    E vejo as sete quantidades calculadas
    E vejo o cardápio dos sete dias, com o dia da semana de cada um
    E a tela devolve o servidor à tela anterior com a indicação de que a passagem
      não terminou
    E leva de volta o órgão, a coordenadoria e o período que consultei

  Cenário: A tela só consulta
    Dado que estou na tela E507T
    Quando a transação chega com uma operação que não é a de consulta
    Então vejo "* Opcao nao disponivel. Use CON *"
    E o cursor fica no campo da operação
    E nada é lido e nada é gravado

  Cenário: Consultar não inclui, não altera e não exclui nada
    Dado que estou na tela E507T
    Quando consulto um pedido e encerro a tela
    Então nenhum registro do órgão, do pedido, das quantidades calculadas ou do
      calendário é incluído, alterado ou excluído
    E nenhuma auditoria é gravada

  Cenário: O órgão é obrigatório
    Dado que estou na tela E507T e a minha área de trabalho não traz órgão
    Quando confirmo sem informar o órgão
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é lido e nada é gravado

  Cenário: Órgão não cadastrado
    Dado que estou na tela E507T
    Quando informo um órgão que não está cadastrado e confirmo
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O servidor não consulta pedido de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo outro órgão e confirmo
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão de outro grupo
    Dado que o meu vínculo carrega uma coordenadoria regional escolar
    Quando informo um órgão cadastrado em outra coordenadoria e confirmo
    Então vejo "<- Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: A data de referência do cálculo é obrigatória
    Dado que estou na tela E507T e a abertura não trouxe as datas do cálculo
    Quando confirmo com o dia de início do preparo em branco
    Então vejo "* Informe a data de inicio do preparo *"
    E o cursor fica no campo do dia
    E nada é lido e nada é gravado

  Cenário: Pedido não cadastrado
    Dado que estou na tela E507T
    Quando informo um órgão e uma data de referência que não correspondem a nenhum
      pedido e confirmo
    Então vejo "* Requisicao nao cadastrada *"
    E o cursor fica no campo do dia
    E nada é mostrado e nada é gravado

  Cenário: O período não fecha e a tela volta à tela anterior
    Dado que o pedido achado está sem o limite do cálculo, ou com o limite anterior
      ao início, ou sem o início ou o limite do período, ou com o limite do período
      anterior ao início
    Quando consulto o pedido
    Então a tela devolve o servidor à tela anterior com a indicação de que a
      passagem não terminou
    E nada é mostrado no lugar do período e nada é gravado

  Cenário: O período está sem os sete dias e a tela volta à tela anterior
    Dado que o pedido achado não tem as sete descrições dos dias do período nem as
      sete indicações de semana
    Quando consulto o pedido
    Então a tela devolve o servidor à tela anterior com a indicação de que a
      passagem não terminou
    E nada é gravado

  Cenário: O órgão consultado não é o do vínculo
    Dado que o meu vínculo carrega um órgão filho
    Quando consulto um pedido de outro órgão
    Então a tela devolve o servidor à tela anterior com a indicação de que a
      passagem não terminou
    E nada é gravado

  Cenário: Sem correio eletrônico cadastrado não há impressão
    Dado que estou na tela E507T e o meu cadastro de servidor está sem correio
      eletrônico
    Quando peço a impressão do relatório do preparo
    Então vejo "<- Usuario sem e-mail cadastrado *"
    E o cursor fica no campo da impressão
    E nada é impresso e nada é enviado

  Cenário: Já há um pedido em processamento para o órgão
    Dado que existe um pedido de impressão ou de arquivo digital em processamento
      para o órgão
    Quando peço a impressão ou o envio do arquivo digital
    Então vejo "* Arquivo em processamento. Aguarde. *" ou
      "* Relatorio em processamento. Aguarde. *"
    E o cursor fica no campo do pedido
    E nada é enfileirado

  Cenário: O pedido de impressão e o envio do arquivo digital não são alcançáveis por esta tela
    Dado que estou na tela E507T
    Quando percorro a tela inteira
    Então a tela esvazia os campos do relatório e do arquivo digital e não os
      preenche
    E nenhum pedido de impressão ou de arquivo digital é enfileirado por esta tela

  Cenário: Nada anda sem a conferência de sessão, de tela e de acesso
    Dado que estou na tela E507T
    Quando a conferência da estação, do registro da tela ou do código de acesso não
      passa
    Então vejo "* Tela nao disponivel *" ou "* Acesso negado para esta matricula *"
    E nada é mostrado, nada é gravado e, se a estação não for a da minha sessão, o
      acesso é encerrado

  Cenário: A tela entrega o órgão, a coordenadoria e o período à tela dos pedidos
    Dado que a tela chegou ao ponto de distribuição de um pedido
    Quando ela passa para a tela dos pedidos
    Então a tela dos pedidos abre com o órgão, a coordenadoria, a classe e o gênero
      de origem, o mês de referência do cálculo e as datas do período que consultei
    E não abre em branco
```
