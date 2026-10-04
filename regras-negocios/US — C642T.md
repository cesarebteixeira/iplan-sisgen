# US — C642T — Cessão de quantidade da permissão de contrato a outra coordenadoria regional

## Estória

Como **servidor da CRE que responde pela permissão de contrato**, quero **ceder a outra
coordenadoria regional uma quantidade da permissão de fornecimento de um item**, para
que **a coordenadoria que vai executar a entrega tenha o saldo autorizado no contrato
dela, sem que o saldo continue preso no meu**.

A permissão de contrato é o que autoriza um fornecedor, dentro de um contrato de uma
coordenadoria e de um grupamento de licitação, a entregar uma quantidade de um item —
uma classe, uma subclasse e um gênero — por um valor, num período. Quando a entrega de
parte desse item passa para outra coordenadoria, o saldo tem de sair da permissão de
quem cede e entrar na permissão de quem recebe, acrescido ao aditivo dela. Sem essa
transferência os dois contratos ficam com o saldo errado: um autoriza uma compra que não
vai acontecer, o outro não tem saldo para a compra que vai. A cessão é registrada item a
item e formalizada pelo relatório das duas permissões, que a tela pede ao confirmar.

## Contexto

Jornada S000M → C000M → C050M → C060M → C642T.

Ator: servidor de CRE — cede a quantidade de um item da permissão da sua coordenadoria
para outra coordenadoria regional e pede o relatório da cessão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O que esta tela usa do que veio antes é o que a entrada deixou na sessão: a **secretaria
da sessão** (o tipo de órgão de quem opera), a **coordenação regional escolar** do
vínculo da matrícula, e a matrícula, o acesso e a estação que vão para o rastro de
auditoria. A coordenadoria da sessão é o que limita de qual permissão o servidor pode
ceder; a secretaria da sessão é a chave com que a tela lê a permissão de origem. Isso é
regra da entrada e está no anexo de evidências, em **Regras que se revelaram da
entrada**.

O destino da cessão é identificado pelo tipo de órgão, pela coordenadoria, pelo tipo de
contrato e pelo período da permissão que vai receber. Essa permissão de destino tem de
existir antes, e é a tela C640T que a registra.

A jornada termina nesta tela: ela não encaminha para nenhuma outra.

## Regras de negócio

### RN-01 — A tela registra a cessão de quantidade de um item da permissão de contrato

A cessão é um cadastro próprio, com **20 campos** e capacidade para **1.500** registros
— **capacidade** (o máximo esperado, parâmetro de dimensionamento), não volume
cadastrado. Ele guarda as duas permissões, a de origem e a de destino, e a quantidade e
o valor cedidos.

A tela **grava**, e grava a linha da cessão do item informado em toda passagem aceita,
**antes de qualquer confirmação**: informada uma quantidade, a linha é criada; já
existindo, é regravada quando a quantidade muda; zerada a quantidade, a linha é apagada.
O que a confirmação governa não é o registro da linha, e sim a transferência dos saldos
(RN-11 e RN-12).

A cessão é identificada pela permissão de origem, pela permissão de destino e pelo
**item**; mas o item, na cessão, é só a subclasse e o gênero — a **classe não entra na
identificação**, embora a tela a mostre e a use para procurar a permissão.

A tela é de transação e trabalha com **oito linhas de item por apresentação**.

[?] O cadastro da cessão admite mais de uma linha para a mesma combinação, mas a tela
trata a cessão como única: ela grava na primeira linha que encontra. Se duas linhas
iguais podem existir, a segunda fica com o valor antigo — pergunta ao site.

[?] A linha de cessão é criada na passagem e apagada quando a cessão é confirmada
(RN-13). Se a intenção é que a cessão não confirmada seja um rascunho que desaparece ao
ser aplicada, ou se a linha deveria permanecer como registro da cessão, o acervo não diz
— pergunta ao site.

### RN-02 — A permissão de origem e a de destino são identificadas por dados próprios, e o grupamento é um só

A permissão de **origem** é a da secretaria da sessão, identificada pela coordenação
regional escolar, pelo período (o ano, o mês e o dia limite), pelo tipo de contrato, pelo
grupamento de licitação e pelo item.

A permissão de **destino** é a do tipo de órgão e da coordenação regional escolar
cessionários, identificada pelo tipo de contrato próprio da cessionária e pelo período
da cessão (o ano, o mês e o dia limite informados). O **grupamento é o mesmo da origem**:
a tela tem um só campo de grupamento, e é ele que procura as duas permissões. A classe, a
subclasse e o gênero do destino saem do próprio destino, não do que se digita para a
origem.

O fornecedor é lido da permissão de origem e o nome dele aparece na tela; a descrição por
extenso do tipo de órgão cessionário e a descrição do item também são mostradas.

O início do período da cessão não se digita: vem do período cadastrado para o tipo de
contrato e o grupamento do destino — o que se informa é a data limite.

[?] Como o grupamento do destino é o da origem, um destino cadastrado com outro
grupamento é recusado como se não existisse. Se a intenção era admitir grupamentos
diferentes, falta um campo na tela — pergunta ao site.

### RN-03 — A tela só atende a coordenadoria do servidor

Se a sessão do servidor tem uma coordenação regional escolar e ele informa outra, a tela
recusa com **\* Usuario sem acesso a este grupo \*** e devolve o cursor ao campo da
coordenação regional escolar. Se a sessão não tem coordenação, qualquer coordenação
informada passa nessa conferência.

### RN-04 — O destino tem de estar cadastrado: órgão, grupo, tipo de contrato e período

A tela confere, nesta ordem, que o **tipo de órgão cessionário** existe — recusa
**\* Secretaria nao cadastrada \*** —, que a **coordenação regional escolar cessionária**
existe no cadastro de grupos daquela secretaria — recusa **\* Grupo nao cadastrado \*** —,
que o **tipo de contrato da cessionária** existe para aquela secretaria — recusa
**\* Tipo de Contrato nao cadastrado \*** — e que o **período está cadastrado para aquele
tipo de contrato e grupamento** — recusa
**\* Periodo nao cad. para este TC/grupamento \***. Cada recusa devolve o cursor ao campo
que a provocou.

[?] As recusas chamam a coordenação regional escolar de "grupo" e o tipo de órgão de
"secretaria": é o vocabulário do site. O que cada cadastro representa no dia a dia, a
confirmar.

### RN-05 — A permissão de origem e a de destino têm de estar cadastradas

Não havendo permissão para a combinação informada na origem, a recusa é
**\* Permissao nao cadastrada \***, com o cursor no campo da coordenação regional
escolar. Não havendo permissão cadastrada para o destino, a recusa é
**\* Permissao nao cadastrada. Utilize C640T \***, com o cursor no tipo de contrato da
cessionária: é a tela do cadastro da permissão que tem de ser usada antes.

A tela também não enxerga permissão marcada como excluída no cadastro.

### RN-06 — Os modos da tela são alteração e consulta, e a consulta não grava

O modo só admite **alteração** e **consulta** — os mesmos que a recusa nomeia como
**ALT** e **CON**. Qualquer outro valor é recusado com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no campo do modo. Quando a
tela é apresentada sem que um modo tenha sido informado antes, ela assume sozinha o modo
consulta.

No modo consulta **nada é gravado**: a passagem que gravaria é abandonada antes de
qualquer gravação, e a tela apenas lê e apresenta a permissão, a quantidade já cedida do
item e o valor total já cedido da permissão.

### RN-07 — A alteração exige que a combinação tenha sido consultada

A alteração só é aceita para a combinação que a tela acabou de apresentar. Se a
coordenação regional escolar, o período limite, o tipo de contrato, o grupamento, ou
qualquer dado do destino — tipo de órgão, coordenação regional escolar, tipo de contrato
e período da cessão — não forem os da consulta anterior, a recusa é
**\* Consulte antes de atualizar \***, com o cursor no campo do modo.

### RN-08 — A quantidade cedida não passa do saldo disponível do item

O saldo disponível do item é a quantidade permitida inicial **mais** o que foi acrescido
por aditivo e por prorrogação **menos** o que já foi pedido contra a permissão; o valor
disponível segue a mesma ideia, com o que já foi comprado no lugar do que foi pedido. A
tela apresenta esse saldo e recusa a cessão que o ultrapasse com
**\* Quantidade cedida > disponivel \***, com o cursor no campo da quantidade cedida.

[?] A conferência compara a quantidade informada com o saldo do item e **não desconta as
cessões já registradas** para o mesmo item: várias cessões podem, somadas, passar do
saldo. Se o saldo apresentado deveria vir abatido das cessões ainda não confirmadas, o
acervo não diz — pergunta ao site.

### RN-09 — O valor cedido é a quantidade pelo preço do item, ajustado pelo percentual cadastrado

O valor cedido é calculado: a quantidade cedida vezes o preço do item, com o preço
ajustado pelo percentual cadastrado na permissão — o percentual divide-se por cem e
soma-se um ao resultado antes de multiplicar o preço. É esse valor que fica registrado na
cessão e é ele que sai da permissão de origem.

[?] O percentual é um campo com sinal no cadastro da permissão e, nesta tela, não tem
rótulo de negócio: com o sinal de menos ele reduz o preço e com o de mais o aumenta. Se
na prática ele é só desconto ou admite acréscimo, a confirmar.

### RN-10 — Zerar a quantidade remove a cessão do item

Informada a quantidade zero para uma cessão que existe, a tela apaga a linha daquele
item, em vez de guardá-la com zero. A quantidade igual à que já estava registrada não
muda nada.

### RN-11 — Confirmar abate a origem: primeiro a prorrogação, depois o saldo inicial

Confirmada a cessão, a tela abate a quantidade cedida da permissão de origem: primeiro
do que foi acrescido por prorrogação; o que não couber passa para a quantidade inicial. O
valor segue a mesma ordem. Quando a cessão é maior que a prorrogação do item, a
prorrogação fica zerada e o restante sai do saldo inicial.

As prorrogações do item, registradas uma a uma, são reduzidas na mesma medida; as que
forem inteiramente consumidas são zeradas.

[?] O trecho que abate o registro de prorrogação subtrai os operandos na ordem inversa
quando o saldo da prorrogação é maior que o que se vai abater — e o mesmo trecho aparece
igual, palavra por palavra, na tela C640T, o que indica bloco gerado. Pergunta ao site.

[?] A leitura de que a parcela "prorrogada" é a prorrogação vem do nome do dado e de a
tela irmã que consulta as prorrogações (C666T) usar os mesmos dois campos; nesta tela
eles não têm rótulo de negócio. A confirmar.

### RN-12 — Confirmar credita o destino como aditivo e refaz os totais das duas permissões

Confirmada a cessão, a quantidade cedida entra na permissão de destino como **aditivo**,
item a item, com o valor correspondente. Em seguida a tela refaz os totais: na permissão
de origem, o valor adjudicado e o homologado passam a ser a soma dos valores iniciais dos
itens e o total da prorrogação passa a ser a soma das prorrogações dos itens; na de
destino, o total do aditivo passa a ser a soma dos aditivos dos itens.

[?] O crédito no destino percorre uma lista interna de até cem itens e a montagem dessa
lista não tem limite de tamanho: uma permissão de origem com mais de cem itens já cedidos
poderia estourar a lista. Se esse tamanho é suficiente na prática, o acervo não diz —
pergunta ao site.

### RN-13 — Confirmar apaga as linhas de cessão da permissão de origem; permissão nenhuma é apagada

Confirmada a cessão, a tela percorre os itens da permissão de origem e apaga **todas** as
linhas de cessão daquele item para o destino informado — inclusive a que acabou de ser
gravada. A cessão confirmada deixa de existir como linha; o que fica é o saldo
transferido, o rastro na auditoria e o relatório.

A permissão de contrato, essa, **não** é apagada por esta tela: a operação de exclusão
existe declarada e não é executada em caminho nenhum dela, e o modo de exclusão é
recusado antes de qualquer gravação (RN-06).

### RN-14 — Toda alteração de permissão deixa rastro na auditoria

Cada permissão alterada pela confirmação — a de origem e a de destino — grava um registro
de auditoria: o objeto auditado (a permissão de contrato), a operação de alteração, a
imagem do registro alterado e o contexto da sessão — matrícula, secretaria, coordenação
regional escolar, terminal, data, hora e número do processo. O cadastro de auditoria
comporta **60.000.000** de registros (capacidade).

[?] O rastro cobre as permissões, não as linhas de cessão apagadas (RN-13) nem as
prorrogações reduzidas (RN-11): essas alterações ficam sem registro de auditoria. E nos
registros da permissão de destino a imagem anterior do registro fica em branco — só o da
origem guarda as duas imagens. Pergunta ao site se é isso que a auditoria deve guardar.

### RN-15 — Confirmar exige a impressora e pede o relatório das duas permissões

Confirmar a cessão exige que a impressora esteja informada: sem ela a recusa é
**\* Informe a impressora \***, com o cursor no campo da impressora. Informada a
impressora, a tela confere se já não existe um pedido de relatório pendente para a mesma
secretaria, a mesma coordenação regional escolar e o mesmo relatório; havendo, recusa com
**\* Relatorio ja esta em processamento. Aguarde. \***.

Passando, a tela registra o pedido do **relatório das permissões de contrato de origem e
de destino**, com as duas permissões como dados do pedido, mais a impressora, a matrícula
e a estação, e o entrega à emissão. Ao final a tela escreve **Cadastro Atualizado** no
campo de situação.

[?] A conferência do pedido pendente não olha a situação nem a data do pedido: um pedido
antigo que continue na base bloqueia todos os pedidos seguintes daquela coordenadoria, e
a tela não mostra como tirá-lo dali. Quem remove esses pedidos está fora desta jornada.
Pergunta ao site.

[?] O que o relatório mostra não está no acervo desta jornada: o programa que o emite não
é uma das telas lidas. A confirmar.

### RN-16 — Nada é feito sem a autorização de perfil, de rota e de operação

Antes de apresentar, antes de validar e antes de gravar, a tela chama as rotinas do
sistema que conferem o **perfil** do servidor, a **rota** da transação e a **permissão
por operação**. Se qualquer uma delas não responder "OK", a tela volta sem gravar e sem
auditar.

[?] A regra efetiva de permissão por perfil e por operação não está no acervo: as rotinas
são declaradas em comum, sem corpo nos arquivos lidos. A tela só confere o retorno.

## Cenários BDD

```gherkin
Funcionalidade: Cessão de quantidade da permissão de contrato a outra coordenadoria regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria e a coordenação regional escolar
    E tenho acesso à tela C642T

  Cenário: A tela cede a quantidade de um item da permissão para outra coordenadoria
    Dado que a permissão da minha coordenadoria está cadastrada e tem saldo no item
    E que a permissão de destino está cadastrada
    Quando informo a quantidade a ceder do item e confirmo a cessão
    Então a quantidade cedida sai do saldo da permissão de origem
    E entra como aditivo na permissão de destino, com o valor correspondente
    E o pedido do relatório das duas permissões é registrado

  Cenário: O valor cedido é a quantidade pelo preço do item ajustado
    Dado que o item da permissão tem preço e um percentual cadastrado
    Quando informo a quantidade a ceder
    Então o valor cedido é a quantidade vezes o preço já ajustado pelo percentual
    E é esse valor que sai da permissão de origem e entra na de destino

  Cenário: A permissão de origem e a de destino são identificadas por dados próprios
    Dado que estou na tela C642T
    Quando informo a coordenadoria, o período, o tipo de contrato, o grupamento e o item de origem
    E informo o tipo de órgão, a coordenadoria, o tipo de contrato e o período de destino
    Então a tela localiza as duas permissões
    E o grupamento procurado nas duas é o mesmo
    E o início do período da cessão me aparece vindo do período cadastrado para o destino

  Cenário: A cessão é identificada pela subclasse e pelo gênero do item
    Dado que a tela mostra a classe, a subclasse e o gênero do item
    Quando registro uma cessão para um item
    Então a cessão fica identificada pela permissão, pelo período e pela subclasse e o gênero do item

  Cenário: A tela recusa coordenadoria fora do meu acesso
    Dado que a minha sessão tem uma coordenação regional escolar
    Quando informo outra coordenação regional escolar
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo da coordenação regional escolar
    E nada é gravado

  Cenário: A tela recusa tipo de órgão cessionário não cadastrado
    Quando informo um tipo de órgão cessionário que não existe
    Então vejo "* Secretaria nao cadastrada *"
    E o cursor fica no campo do tipo de órgão
    E nada é gravado

  Cenário: A tela recusa coordenação cessionária sem grupo cadastrado
    Quando informo uma coordenação regional escolar cessionária que não existe para aquele tipo de órgão
    Então vejo "* Grupo nao cadastrado *"
    E o cursor fica no campo da coordenação regional escolar cessionária
    E nada é gravado

  Cenário: A tela recusa o tipo de contrato da cessionária não cadastrado
    Quando informo um tipo de contrato da cessionária que não existe para aquele tipo de órgão
    Então vejo "* Tipo de Contrato nao cadastrado *"
    E o cursor fica no campo do tipo de contrato da cessionária
    E nada é gravado

  Cenário: A tela recusa período não cadastrado para o tipo de contrato e o grupamento
    Quando informo um período que não existe para aquele tipo de contrato e grupamento
    Então vejo "* Periodo nao cad. para este TC/grupamento *"
    E o cursor fica no campo da data limite da cessão
    E nada é gravado

  Cenário: A tela recusa permissão de origem não cadastrada
    Quando a combinação informada não tem permissão cadastrada na minha coordenadoria
    Então vejo "* Permissao nao cadastrada *"
    E o cursor fica no campo da coordenação regional escolar
    E nada é gravado

  Cenário: A tela recusa permissão de destino não cadastrada
    Quando a combinação informada não tem permissão cadastrada para a cessionária
    Então vejo "* Permissao nao cadastrada. Utilize C640T *"
    E o cursor fica no campo do tipo de contrato da cessionária
    E nada é gravado

  Cenário: O modo da tela só admite ALT ou CON
    Dado que estou na tela C642T
    Quando informo um modo diferente de ALT e de CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: A consulta não grava nada
    Dado que estou na tela C642T no modo consulta e a permissão está cadastrada
    Quando percorro a permissão e o item
    Então a tela apresenta o saldo do item, a quantidade já cedida e o total já cedido
    E as duas permissões continuam com os saldos anteriores

  Cenário: A alteração sem consulta prévia é recusada
    Dado que estou na tela C642T e mudei a coordenação, o período, o tipo de contrato ou algum dado do destino
    Quando informo o modo ALT
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: A quantidade acima do saldo disponível é recusada
    Dado que estou na tela C642T no modo ALT e a permissão está cadastrada
    Quando informo uma quantidade maior que o saldo disponível do item
    Então vejo "* Quantidade cedida > disponivel *", com o saldo mostrado ao lado
    E o cursor fica no campo da quantidade cedida
    E nada é gravado

  Cenário: O saldo disponível é o que está livre na permissão
    Dado que a permissão do item tem quantidade acrescida por aditivo e por prorrogação
    E tem quantidade já pedida e valor já comprado
    Quando a tela calcula o saldo disponível
    Então o que foi acrescentado é somado
    E o que já foi pedido, no saldo da quantidade, e o que já foi comprado, no saldo do valor, são descontados

  Cenário: A cessão registrada e não confirmada não move saldo
    Dado que estou na tela C642T no modo ALT
    Quando informo a quantidade a ceder sem confirmar a cessão
    Então a cessão daquele item fica registrada e a tela a mostra como quantidade já cedida
    E as duas permissões continuam com os saldos e os totais anteriores

  Cenário: A cessão registrada é apagada quando a quantidade é zerada
    Dado que existe uma cessão registrada para o item
    Quando informo a quantidade zero para aquele item
    Então a cessão daquele item deixa de existir
    E as duas permissões continuam com os saldos e os totais anteriores

  Cenário: A cessão confirmada abate primeiro a prorrogação do item
    Dado que a permissão de origem tem prorrogação no item
    Quando confirmo uma cessão maior que a prorrogação
    Então a prorrogação do item fica zerada
    E o restante sai da quantidade inicial do item
    E o valor sai na mesma ordem

  Cenário: A cessão confirmada credita o aditivo do destino e refaz os totais
    Dado que confirmei a cessão de um item
    Quando a gravação termina
    Então a quantidade cedida entra como aditivo na permissão de destino, com o valor correspondente
    E o valor adjudicado e o homologado da permissão de origem passam a ser a soma dos valores iniciais dos itens
    E o total da prorrogação da origem passa a ser a soma das prorrogações dos itens
    E o total do aditivo do destino passa a ser a soma dos aditivos dos itens

  Cenário: Confirmar apaga a linha da cessão e mantém as permissões
    Dado que confirmei a cessão de um item
    Quando a gravação termina
    Então a linha de cessão daquele item deixa de existir
    E as duas permissões continuam cadastradas
    E a tela mostra "Cadastro Atualizado"

  Cenário: Toda alteração de permissão deixa rastro na auditoria
    Dado que confirmei uma cessão na C642T
    Quando a gravação termina
    Então existe um registro de auditoria para a permissão de origem e um para a de destino
    E com a operação de alteração e a imagem do registro alterado
    E com a matrícula, a secretaria, a coordenadoria, o terminal, a data e a hora

  Cenário: Confirmar sem a impressora é recusado
    Dado que estou na tela C642T no modo ALT, com a cessão já calculada
    Quando confirmo a cessão sem informar a impressora
    Então vejo "* Informe a impressora *"
    E o cursor fica no campo da impressora
    E nada é gravado

  Cenário: Com um pedido de relatório pendente a confirmação é recusada
    Dado que já existe um pedido de relatório pendente para a minha coordenadoria
    Quando confirmo a cessão
    Então vejo "* Relatorio ja esta em processamento. Aguarde. *"
    E nada é gravado

  Cenário: A exclusão de permissão não existe nesta tela
    Dado que estou na tela C642T
    Quando informo o modo de exclusão
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E nenhuma permissão é apagada

  Cenário: Nada é gravado sem a autorização de perfil, de rota e de operação
    Dado que estou na tela C642T
    Quando a conferência de perfil, de rota ou de permissão por operação não retorna OK
    Então a tela volta sem gravar nada
    E nenhum registro de auditoria é criado
```
