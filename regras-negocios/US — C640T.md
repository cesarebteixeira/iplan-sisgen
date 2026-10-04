# US — C640T — Transferência de parte da permissão de contrato para outra secretaria

## Estória

Como **servidor da CRE que responde pelo contrato**, quero **transferir para outra
secretaria uma parte da permissão de contrato de um fornecedor**, para que **a secretaria
que passa a executar aquele trecho tenha, em seu nome, a quantidade e o valor cedidos, e a
minha coordenadoria deixe de autorizar o que já não é dela**.

A permissão de contrato é o que autoriza um fornecedor, dentro de um contrato de uma
coordenadoria, de um grupo de licitação e de um período, a entregar certa quantidade de um
item — uma classe, uma subclasse e um gênero — por um valor. Quando parte dessa permissão
passa a ser executada por outra secretaria, o saldo tem de mudar de mãos: o que sai daqui
não pode continuar autorizando compra na origem, e o que chega lá precisa existir como
permissão para poder ser pedido. Sem isso, a secretaria que recebe não consegue comprar o
que lhe foi transferido, e a origem continua com um saldo que já não é o seu.

## Contexto

Jornada S000M → C000M → C050M → C060M → C640T.

Ator: servidor de CRE — transfere parte da permissão de contrato da sua coordenadoria para
outra secretaria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O que esta tela usa do que veio antes é a **secretaria e a coordenadoria da sessão**,
tiradas do vínculo da matrícula com a secretaria escolhida na entrada: são o lado de origem
da transferência. Essa é regra da entrada e está no anexo de evidências, em **Regras que se
revelaram da entrada**.

Os dois passos imediatamente anteriores são menus: não entregam a esta tela nem registro
nem modo de operação. Esta tela **não lê a tela que a chamou** — não há comparação com
código de tela chamadora — e o modo dela é decidido pelo próprio campo de opção, que chega
em branco: ela abre em consulta.

A jornada termina nesta tela: ela não encaminha para nenhuma outra.

---

## Regras de negócio

### RN-01 — A tela transfere parte da permissão de contrato de uma coordenadoria para outra secretaria

A permissão de contrato fixa, para uma coordenadoria, um período, um tipo de contrato e um
grupo de licitação, o fornecedor e o que cada item — uma classe, uma subclasse e um gênero —
carrega de quantidade e de valor. Esta tela toma uma parte desses itens, na quantidade que o
servidor ceder, e a entrega a outra secretaria: o saldo da permissão de origem é reduzido e
uma permissão de destino é criada com o que foi cedido. A origem é a secretaria e a
coordenadoria da sessão; o destino é informado na tela.

### RN-02 — A permissão de origem é localizada pela coordenadoria, pelo período limite, pelo tipo de contrato e pelo grupo de licitação

Para chegar à permissão, o servidor informa a **coordenadoria regional escolar**, o **tipo
de contrato**, o **grupo de licitação** e o dia, o mês e o ano do **período limite**; a
secretaria vem da sessão. O item não se informa: a tela traz da permissão os itens que ela
tem. Não havendo permissão para a combinação informada, a recusa é
**\* Permissao nao cadastrada \***, com o cursor de volta à coordenadoria.

### RN-03 — A tela só atende a coordenadoria do servidor

Se a sessão tem uma coordenadoria e a coordenadoria informada é outra, a tela recusa com
**\* Usuario sem acesso a este grupo \*** e devolve o cursor à coordenadoria; nada é
gravado. Se a sessão não tem coordenadoria, a tela aceita a que for informada.

[?] A conferência compara a coordenadoria informada com uma área de trabalho da sessão que o
acervo só mostra zerada no início da sessão ou preenchida por telas de nota fiscal, que não
fazem parte desta jornada — e não com a coordenadoria da sessão, que é a que a tela usa no
resto da lógica. Ou a recusa nunca acontece, ou ela acontece para qualquer coordenadoria que
o servidor informe. Pergunta ao site.

### RN-04 — O destino é uma outra secretaria, com a sua coordenadoria, o seu tipo de contrato e o seu período

O destino tem secretaria, coordenadoria regional escolar, tipo de contrato e período limite
próprios, e a tela confere cada um deles no cadastro correspondente antes de aceitar a
cessão (RN-11). O **período inicial do destino não se digita**: vem do cadastro do período
daquele tipo de contrato e daquele grupo (RN-13). Diferente da origem, o destino é um
contrato que ainda não existe; se já houver permissão para ele, a tela recusa (RN-12).

[?] Os dados do destino não têm nome de negócio no acervo: nenhuma descrição de tela os
rotula e o corpus não diz o que eles designam em negócio, além do que a própria
transferência faz com eles. Pergunta ao site.

### RN-05 — A grade mostra até oito itens, e cada item traz o que ainda é permitido e o que se cede

A grade tem **oito linhas**, uma por item da permissão. Cada linha traz a **classe**, a
**subclasse**, o **gênero** e a descrição do gênero, a **quantidade ainda permitida**, o
**valor ainda permitido**, a **quantidade cedida** e o **valor cedido**. A descrição do
gênero é buscada no cadastro. Linha sem item é ignorada, em silêncio.

### RN-06 — O que a tela mostra como ainda permitido é o saldo livre do item

A **quantidade ainda permitida** é a quantidade inicial do item **mais** o que foi acrescido
por aditivo e por prorrogação, **menos** o que já foi pedido. O **valor ainda permitido** é o
valor inicial **mais** o do aditivo e o da prorrogação, **menos** o que já foi comprado. É
esse saldo livre que limita a cessão.

### RN-07 — O valor cedido é calculado pela tela

O servidor informa só a **quantidade cedida** de cada item; o **valor cedido** a tela
calcula, multiplicando a quantidade cedida pelo preço do item ajustado pelo percentual
cadastrado no próprio item. O valor que a tela apresenta é sempre o calculado — o que
estiver no campo do valor cedido é descartado.

[?] O percentual do item é um número com sinal e a tela sempre o soma a um: percentual
positivo acrescenta ao preço, negativo desconta. O acervo não mostra o sinal em uso no dia a
dia (se o cadastro guarda desconto ou acréscimo, e com que sinal). Pergunta ao site.

### RN-08 — Ceder mais do que o item ainda permite é recusado

Se a quantidade cedida de uma linha passar da quantidade ainda permitida daquele item, a
tela recusa com **\* Quantidade cedida > disponivel \*** e devolve o cursor à quantidade
cedida daquela linha. Nada é transferido.

### RN-09 — A tela só trabalha em alteração e consulta, e abre em consulta

A tela atende **alteração** e **consulta** — as mesmas que a recusa chama de **ALT** e
**CON**. Qualquer outra opção é recusada com **\* Opcao nao disponivel. Use ALT ou CON \***,
com o cursor no campo da opção. Quando a tela abre sem opção informada, ela assume sozinha a
consulta, e depois de uma transferência concluída ela volta em consulta.

### RN-10 — A alteração exige que a permissão tenha sido consultada antes

Ao alterar, os dados que identificam a permissão e o destino — a coordenadoria, o período
limite, o tipo de contrato, o grupo de licitação e os quatro dados do destino — têm de ser
os mesmos da consulta anterior. Se algum deles mudou, a recusa é
**\* Consulte antes de atualizar \***, com o cursor no campo da opção.

[?] O código do fornecedor não entra nessa conferência: a tela compara todos os demais
campos do cabeçalho e não esse. Ou a conferência do fornecedor está em outro ponto, ou ela
falta. Pergunta ao site.

### RN-11 — A consulta confere a permissão de origem, a liberação da tela pela licitação e todo o destino

Na consulta, cada recusa tem a sua mensagem e o seu cursor:

- a permissão de origem tem de existir — **\* Permissao nao cadastrada \***, cursor na
  coordenadoria;
- a tela tem de estar liberada para o **tipo de licitação** da permissão —
  **\* Tela nao disponivel para esta licitacao \***, cursor no campo da opção;
- a **secretaria de destino** tem de existir — **\* Secretaria nao cadastrada \***, cursor
  na secretaria de destino;
- a **coordenadoria de destino** tem de existir — **\* Grupo nao cadastrado \***, cursor na
  coordenadoria de destino;
- o **tipo de contrato de destino** tem de existir — **\* Tipo de Contrato nao cadastrado \***,
  cursor no tipo de contrato de destino;
- o **período de destino** tem de estar cadastrado para aquele tipo de contrato e aquele
  grupo — **\* Periodo nao cad. para este TC/grupamento \***, cursor no período de destino.

Como essa conferência toda é da consulta, a alteração depende de a consulta ter passado.

### RN-12 — Esta tela serve à primeira cessão; se o destino já tem permissão, o caminho é a C642T

Se já existir permissão para o destino informado, a consulta recusa com
**\* Permissao ja cadastrada. Utilize C642T \*** e manda usar a tela irmã. É isso que faz
desta tela a da **primeira** transferência de um contrato: a C642T, ao contrário, só atende
quando a permissão de destino já existe.

[?] A tela procura a permissão de destino com o **item em branco**. Se o item em branco
significa "qualquer item", a recusa aparece assim que existir uma permissão qualquer no
destino, e a regra fecha; se significa "o item é zero", ela nunca aparece — porque a cessão
sempre cria a permissão de destino com o item — e a segunda transferência passaria por cima
da primeira, sem a C642T. O acervo não declara qual das duas leituras vale para a busca com
o item em branco. Pergunta ao site.

### RN-13 — O fornecedor, a razão social, a descrição da secretaria de destino e o período inicial do destino vêm dos cadastros

A tela não aceita esses valores do servidor: o **código do fornecedor** é o da permissão, a
**razão social** é buscada no cadastro de fornecedores por esse código, a **descrição da
secretaria de destino** é buscada no cadastro de órgãos pelo tipo de órgão de destino, e o
**período inicial do destino** é o que o cadastro do período guarda para aquele tipo de
contrato e aquele grupo.

### RN-14 — A transferência só se conclui com a confirmação no pé da tela

No pé da tela existe um campo de **confirmação**. Enquanto ele não vem marcado, a tela grava
apenas a **cessão de cada item** (o que se pretende ceder, item a item) e **não transfere
nada**: o saldo da permissão de origem não é reduzido, a permissão de destino não é criada, a
cessão por item não é apagada e o relatório não é pedido. Marcado, e tratando-se de
alteração, a tela conclui a transferência.

[?] Nenhum programa do acervo marca esse campo: ele só é lido pela tela e devolvido no
registro da transação. Quem o marca é a estação de trabalho, e o acervo não tem a máscara da
tela, de modo que não se sabe se ele é digitável pelo servidor. Se ele não puder ser marcado,
a transferência nunca se conclui. Pergunta ao site.

### RN-15 — Confirmada, a cessão sai da prorrogação e depois do saldo inicial, e alcança também as prorrogações do item

A quantidade e o valor cedidos saem primeiro da parcela **prorrogada** do item; o que passar
disso sai do **saldo inicial**. A parcela acrescida por **aditivo** não é tocada. A mesma
redução é feita nos registros de **prorrogação** daquele item, que guardam o saldo por
período.

[?] Quando um registro de prorrogação tem quantidade maior do que o que resta a ceder, a
tela grava nesse registro a diferença na direção contrária — o que resta menos o que o
registro tem —, resultado negativo. Ou a comparação está invertida, ou o valor gravado
deveria ser o do registro menos o cedido. Por esse ramo, o saldo da prorrogação sai
corrompido. Pergunta ao site.

### RN-16 — A permissão de destino é criada com o que foi cedido, e os totais do contrato são recalculados nos dois lados

Concluída a cessão, cada item cedido ganha uma permissão de destino com a **mesma
secretaria, coordenadoria, tipo de contrato e período informados**, o **mesmo fornecedor**,
o **mesmo grupo de licitação** e o **mesmo item**, com a quantidade e o valor cedidos. Em
seguida a tela recalcula, item a item, os totais do contrato de origem — o valor ajustado e o
homologado passam a ser a soma dos valores iniciais dos itens, e o valor da prorrogação, a
soma das prorrogações — e faz o mesmo com os totais do contrato de destino.

### RN-17 — Nenhuma permissão é apagada; a exclusão só alcança o rascunho da própria cessão

Esta tela **não apaga permissão nenhuma**: ela reduz saldo e cria permissão. A única
exclusão que ela executa é sobre a **cessão por item** que ela mesma gravou, apagada ao fim
da transferência concluída — inclusive a de um item cuja quantidade cedida foi zerada.

### RN-18 — A cessão é documentada por um relatório, que exige a impressora

A transferência concluída pede um **relatório** com os dados da origem e do destino e com os
itens cedidos, e o manda para a **impressora** informada na tela. Sem a impressora, a tela
recusa com **\* Informe a impressora \***, com o cursor nesse campo. Se já houver um
relatório em processamento para a mesma coordenadoria, a tela recusa com
**\* Relatorio ja esta em processamento. Aguarde. \***.

[?] O acervo não liga o relatório ao programa que o imprime: a entrega passa pela rotina de
emissão do ambiente, que não tem corpo no lote, e o programa do relatório existe à parte,
sem ligação formal com a tela. Pergunta ao site.

### RN-19 — Toda gravação deixa rastro na auditoria

Cada mudança durável — a redução do saldo da permissão de origem e a criação da permissão de
destino — monta um registro de auditoria com o contexto da sessão (matrícula, secretaria,
coordenadoria, terminal, data e hora e número do processo), a operação de alteração e os
valores antes e depois. A cessão por item, que é rascunho, não é auditada.

### RN-20 — Nada é gravado sem a autorização de perfil, de rota e de operação

Antes de apresentar e antes de validar, a tela chama as rotinas do sistema que conferem o
**perfil** do servidor, a **rota** da transação e a **permissão por operação**. Se qualquer
uma delas não responder "OK", a tela volta sem gravar e sem auditar.

[?] A regra efetiva de permissão por perfil e por operação não está no acervo: as rotinas
são declaradas em comum, sem corpo no lote. A tela só confere o retorno.

### RN-21 — Consultar não grava nada

Na consulta a tela apenas lê e apresenta: a permissão, os itens, a descrição do gênero, a
razão social do fornecedor, os cadastros do destino e a cessão por item que já esteja
gravada. A passagem que grava é abandonada de propósito quando a opção é consulta, antes de
qualquer teste de valor, e nenhuma permissão é criada, reduzida ou apagada.

### RN-22 — O que o gerador declara não é o que a tela executa

O código gerado declara, para cada um dos **14 cadastros** que a tela enxerga, uma rotina de
gravação e uma de exclusão. A tela **escreve em cinco**: a permissão (C061T), a cessão por
item (C641T), a prorrogação (C665T), a auditoria (A010T) e o pedido de relatório (S040T). Os
outros **nove** — entre eles o cadastro do órgão, o dos fornecedores, o do gênero, o do
período, o da licitação e o do usuário — são **só de leitura**; as suas rotinas de gravação
e de exclusão existem declaradas e nunca são executadas.

---

## Cenários BDD

```gherkin
Funcionalidade: Transferência de parte da permissão de contrato para outra secretaria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C640T

  Cenário: RN-01, RN-05, RN-06 e RN-21 — consultar a permissão e ver os itens com o que ainda permitem
    Dado que estou na tela C640T com a opção CON
    E informo a coordenadoria, o período limite, o tipo de contrato e o grupo de licitação
    Quando confirmo a consulta
    Então vejo a razão social do fornecedor e, em cada uma das oito linhas, a classe, a subclasse, o gênero com a descrição, a quantidade ainda permitida, o valor ainda permitido, a quantidade cedida e o valor cedido
    E a quantidade ainda permitida é o saldo inicial mais o aditivo mais a prorrogação, menos o pedido
    E nada é gravado

  Cenário: RN-02 — permissão não cadastrada
    Dado que estou na tela C640T com a opção CON
    Quando informo uma combinação de coordenadoria, período, tipo de contrato e grupo de licitação que não tem permissão
    Então vejo "* Permissao nao cadastrada *"
    E o cursor fica na coordenadoria
    E nada é gravado

  Cenário: RN-03 — coordenadoria fora do meu acesso
    Dado que a minha sessão tem uma coordenadoria
    Quando informo outra coordenadoria
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica na coordenadoria
    E nada é gravado

  Cenário: RN-09 — opção de manutenção não disponível
    Dado que estou na tela C640T
    Quando informo uma opção diferente de ALT e de CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo da opção
    E nada é gravado

  Cenário: RN-09 — a tela abre em consulta
    Dado que entro na tela C640T sem informar a opção de manutenção
    Então a tela abre em consulta
    E, depois de uma transferência concluída, ela volta em consulta

  Cenário: RN-10 — alterar sem consultar antes
    Dado que estou na tela C640T com a opção ALT
    E informo uma coordenadoria, um período, um tipo de contrato, um grupo de licitação ou um destino diferente do da consulta anterior
    Quando confirmo
    Então vejo "* Consulte antes de atualizar *"
    E nada é transferido

  Cenário: RN-11 — tela não liberada para a licitação da permissão
    Dado que consultei uma permissão cujo tipo de licitação não tem esta tela liberada
    Quando confirmo a consulta
    Então vejo "* Tela nao disponivel para esta licitacao *"
    E nada é gravado

  Cenário: RN-04 e RN-11 — secretaria de destino não cadastrada
    Quando informo um tipo de órgão de destino que não existe
    Então vejo "* Secretaria nao cadastrada *"
    E o cursor fica na secretaria de destino
    E nada é gravado

  Cenário: RN-04 e RN-11 — coordenadoria de destino não cadastrada
    Quando informo uma coordenadoria de destino que não existe para a secretaria de destino
    Então vejo "* Grupo nao cadastrado *"
    E o cursor fica na coordenadoria de destino
    E nada é gravado

  Cenário: RN-04 e RN-11 — tipo de contrato de destino não cadastrado
    Quando informo um tipo de contrato de destino que não existe para a secretaria de destino
    Então vejo "* Tipo de Contrato nao cadastrado *"
    E o cursor fica no tipo de contrato de destino
    E nada é gravado

  Cenário: RN-04 e RN-11 — período de destino não cadastrado
    Dado que o tipo de contrato e o grupo de destino não têm aquele período cadastrado
    Quando confirmo a consulta
    Então vejo "* Periodo nao cad. para este TC/grupamento *"
    E o cursor fica no período de destino
    E nada é gravado

  Cenário: RN-12 — o destino já tem permissão
    Dado que o destino informado já tem uma permissão
    Quando confirmo a consulta
    Então vejo "* Permissao ja cadastrada. Utilize C642T *"
    E sou mandado para a tela C642T
    E nada é transferido

  Cenário: RN-13 — o fornecedor, a descrição da secretaria e o período inicial do destino vêm dos cadastros
    Dado que consultei uma permissão
    Quando a tela apresenta o cabeçalho
    Então a razão social é a do fornecedor da permissão
    E a descrição da secretaria de destino vem do cadastro de órgãos
    E o período inicial do destino vem do cadastro do período daquele tipo de contrato e daquele grupo

  Cenário: RN-05 e RN-07 — o valor cedido é calculado
    Dado que consultei a permissão e o item tem preço cadastrado
    Quando informo a quantidade cedida de uma linha
    Então o valor cedido daquela linha é a quantidade cedida multiplicada pelo preço do item ajustado pelo percentual cadastrado
    E o valor que a tela apresenta é o calculado, e não o que estiver no campo

  Cenário: RN-08 — quantidade cedida acima do permitido
    Dado que consultei a permissão
    Quando informo, numa linha, uma quantidade cedida maior que a quantidade ainda permitida daquele item
    Então vejo "* Quantidade cedida > disponivel *"
    E o cursor fica na quantidade cedida daquela linha
    E nada é transferido

  Cenário: RN-14 — sem a confirmação nada é transferido
    Dado que consultei a permissão e informei as quantidades a ceder
    Quando confirmo a alteração sem marcar a confirmação no pé da tela
    Então a cessão de cada item fica registrada
    E o saldo da permissão de origem continua o mesmo
    E nenhuma permissão de destino é criada
    E nenhum relatório é pedido

  Cenário: RN-15, RN-16, RN-18, RN-19 e RN-20 — a transferência confirmada
    Dado que consultei a permissão, informei as quantidades a ceder e a impressora
    E marco a confirmação no pé da tela
    Quando confirmo a alteração
    Então a quantidade e o valor cedidos saem da parcela prorrogada do item e, do que passar, do saldo inicial
    E a parcela acrescida por aditivo não é tocada
    E cada item cedido ganha uma permissão na secretaria de destino, com o mesmo fornecedor, o mesmo grupo de licitação e o mesmo item, pela quantidade e pelo valor cedidos
    E os totais do contrato de origem e do de destino são recalculados em todos os seus itens
    E cada mudança deixa um registro na auditoria
    E o relatório da cessão é pedido para a impressora informada

  Cenário: RN-17 — nenhuma permissão é apagada
    Dado que concluí uma transferência
    Quando a gravação termina
    Então a permissão de origem continua no cadastro, com o saldo reduzido
    E a permissão de destino passa a existir
    E a única coisa apagada é a cessão por item que a própria tela gravou

  Cenário: RN-18 — falta a impressora
    Dado que consultei a permissão, informei as quantidades a ceder e marco a confirmação
    Quando confirmo a alteração sem informar a impressora
    Então vejo "* Informe a impressora *"
    E o cursor fica no campo da impressora
    E nada é transferido

  Cenário: RN-18 — relatório já em processamento
    Dado que já existe um relatório desta cessão em processamento para a minha coordenadoria
    Quando confirmo a alteração com a impressora informada
    Então vejo "* Relatorio ja esta em processamento. Aguarde. *"
    E nada é transferido

  Cenário: RN-20 — sem a autorização de perfil, de rota ou de operação
    Dado que estou na tela C640T
    Quando a conferência de perfil, de rota ou de permissão por operação não retorna OK
    Então a tela volta sem gravar nada
    E nenhum registro de auditoria é criado

  Cenário: RN-22 e RN-21 — a tela não escreve nos cadastros que só lê
    Dado que consultei a permissão
    Quando a consulta termina
    Então o cadastro de órgãos, o dos fornecedores, o do gênero, o do período, o da licitação e o do usuário continuam como estavam
    E nenhuma de suas rotinas de gravação ou de exclusão é executada
```
