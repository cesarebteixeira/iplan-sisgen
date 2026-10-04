# US — C768T — Excluir o planejamento sazonal de cardápios de um grupo da coordenação regional escolar

## Estória

Como **servidor de CRE**, quero **informar o grupo e a data limite de validade de um
planejamento sazonal de cardápios e pedir a sua exclusão**, para que **o planejamento
que não vale mais saia do cadastro e deixe de ser considerado nos pedidos de gêneros
do período**.

O planejamento sazonal de cardápios diz quais cardápios estão previstos em cada mês, por
grupo, segmento de atendimento e refeição, e é dele que saem as quantidades usadas nos
pedidos de gêneros. Um planejamento lançado para o período errado não pode continuar no
cadastro, e tirá-lo registro por registro na tela de manutenção é trabalhoso e deixa
sobra. Esta é a tela que resolve isso de uma vez: ela recebe o grupo e a data limite de
validade e pede a exclusão de tudo o que estiver naquele recorte. Ela não apaga nada por
conta própria — registra o pedido e o entrega ao processamento —, e é por isso que a
exclusão não é imediata.

## Contexto

Jornada S000M → C000M → C070M → C760M → C768T.

Ator: servidor de CRE — pede a exclusão do planejamento sazonal de cardápios do seu
grupo, pela data limite de validade.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio.

As regras abaixo são só as da tela desta jornada. Os passos anteriores — o C000M, o
C070M e o C760M — são menus e não gravam nada: apenas encaminham. O que a C768T usa da
sessão — a matrícula, o tipo de órgão, o grupo e a CRE do servidor, a estação e a data
do sistema — é o que a entrada deixou. O grupo que a exclusão alcança **não** vem dos
menus: é o que o servidor informa na própria C768T.

O cadastro tratado é o do **planejamento sazonal de cardápios**: para um tipo de órgão,
um grupo, um segmento de atendimento, uma refeição e um cardápio, ele guarda o período
de validade (data inicial e data limite) e as quantidades previstas mês a mês. Um mesmo
grupo e uma mesma data limite podem ter vários registros, um por segmento, refeição e
cardápio. Quem cadastra e altera é a tela C760T; a C768T não mantém esse cadastro — só
pede a exclusão dele.

## Regras de negócio

### RN-01 — A tela só opera em alteração, e não tem consulta

A tela abre sempre com a operação de alteração e recusa qualquer outra com
**\* Opcao nao disponivel. Use ALT \***, devolvendo o cursor ao campo da resposta.
Não existe operação de consulta: quem quer ver o planejamento usa a tela de manutenção
do cadastro; aqui, a única coisa que se faz é pedir a exclusão. E como a operação é de
alteração, o perfil de acesso do servidor precisa liberar a alteração da C768T — quem
tem a tela liberada apenas para consulta não passa.

[?] A mensagem manda usar "ALT", mas a tela reconhece o código interno de alteração que
o sistema usa, e nenhum valor "ALT" existe no acervo lido. Ou o formulário traduz o que
o servidor digita, ou a mensagem indica um valor que a tela recusa. Pergunta ao site.

### RN-02 — Os códigos e as datas informados são numéricos, e o cursor volta ao campo recusado

Os campos da tela passam pela edição numérica antes de qualquer consulta: o grupo, as
três partes da data inicial e as três partes da data limite. O que não for número não
chega ao cadastro, e o campo em branco vale zero. Quando o grupo, o dia, o mês ou o ano
limite é recusado, o cursor volta ao campo recusado. As três partes da data inicial são
editadas do mesmo modo, mas o cursor nunca vai para elas: quem as preenche é o cadastro,
e o que o servidor digitar ali é substituído pelo valor do cadastro.

[?] A rotina que faz a edição numérica é do ambiente, não do acervo: não se sabe se a
recusa mostra mensagem, e qual. Pergunta ao site.

### RN-03 — O grupo é obrigatório

O grupo é o código da coordenação regional escolar cadastrada para o tipo de órgão da
secretaria. Informado em branco, o sistema recusa com **\* Informe o grupo \*** e devolve
o cursor ao campo do grupo. O código 99 é o único valor especial: vale por todos os
grupos da faixa.

[?] A tela não confere se o grupo informado está cadastrado; sem planejamento para
aquela data a recusa é a mesma, e não há mensagem própria de grupo inexistente. Não se
sabe se a ausência dessa conferência é intencional. Pergunta ao site.

### RN-04 — Sem planejamento para a data limite informada, a tela recusa

A tela procura o planejamento do tipo de órgão do servidor, do grupo informado e da
data limite informada. Se não achar, recusa com
**\* Nao existe planejamento sazonal para esta data \*** e devolve o cursor ao campo do
grupo. Achando, ela traz do cadastro a data inicial do período, que passa a ser mostrada
junto com a data limite: é esse par que define a validade que será conferida e, depois,
excluída. Para o grupo 99, a procura é a primeira que aparecer para aquela data limite.

[?] Com o grupo 99, a data inicial mostrada é a do primeiro planejamento que o sistema
encontrar para aquela data limite, e não necessariamente a de um grupo em particular; o
acervo não diz qual seria a data inicial "certa" nesse caso. Pergunta ao site.

### RN-05 — O que a exclusão remove é todo o planejamento do grupo naquela data limite

Pedida a exclusão, o processamento apaga todos os registros do planejamento sazonal do
tipo de órgão, do grupo informado (de todos os grupos, quando 99) e da data limite
informada — um por segmento de atendimento, refeição e cardápio —, com qualquer data
inicial que eles tenham. A data inicial mostrada na tela é a de um desses registros e
serve para dimensionar a conferência dos pedidos de gêneros (RN-06).

[?] A conferência dos pedidos de gêneros usa uma única data inicial, mas a exclusão
alcança todos os registros daquela data limite, inclusive os que tiverem outra data
inicial. Se isso acontece no cadastro, a conferência não cobre o que a exclusão apaga.
Pergunta ao site.

### RN-06 — A exclusão é recusada quando há pedido de gêneros do grupo no período

A tela percorre os grupos (todos, quando 99) e, para cada um, os pedidos de gêneros do
tipo de órgão do servidor. Se algum pedido não estiver marcado como excluído e o período
de entrega dele cruzar a validade do planejamento — da data inicial mostrada até a data
limite informada —, a exclusão é recusada com
**\* Nao exclua. Ja existem pedidos cadastrados \***, e o cursor volta à data limite.
Pedido já marcado como excluído não conta.

[?] Quando o grupo é 99, a conferência dos pedidos começa pelo código zero dos grupos;
se o sistema não encontrar esse ponto de partida, a exclusão de todos os grupos pode
passar sem que nenhum pedido seja conferido. Pergunta ao site.

### RN-07 — A exclusão é recusada enquanto houver pedido desta rotina em processamento, sem distinguir secretaria nem grupo

Antes de registrar um pedido, a tela verifica se já existe um pedido de exclusão desta
rotina aguardando processamento. Existindo, recusa com
**\* Relatorio em processamento. Aguarde. \*** e devolve o cursor ao campo da resposta.
Essa fila não é consultada por secretaria, tipo de órgão nem grupo: um pedido pendente,
de qualquer secretaria, impede que qualquer servidor peça uma nova exclusão. Quem tira o
pedido da fila é o próprio processamento, ao terminar — se ele não terminar, a tela fica
bloqueada para todos.

[?] O pedido pendente é procurado pelo número zero, que nenhum pedido real tem. Se a
busca exigir a chave exata, a recusa nunca acontece; se ela se posicionar na fila,
qualquer pedido pendente bloqueia a todos. Não concluo qual das duas leituras vale.
Pergunta ao site.

### RN-08 — A exclusão exige confirmação, e só o "S" segue

Antes de registrar o pedido, a tela pergunta
**\* Confirma exclusao do planejamento <S/N> ? \***. Só a resposta "S" segue; qualquer
outra resposta apenas repete a pergunta, com todas as conferências feitas de novo — não
há, na tela, uma resposta de desistência que encerre a operação. A confirmação vale para
o grupo e a data limite que estavam na tela: se o grupo ou a data limite mudarem, ela é
descartada e a tela confere tudo outra vez antes de perguntar de novo.

[?] Como o servidor abandona a operação: pelo acervo, a única saída é deixar a tela, e
não há mensagem de cancelamento. Pergunta ao site.

### RN-09 — A tela não apaga o planejamento: ela registra o pedido e o encaminha ao processamento

Esta tela não exclui nada do cadastro. O que ela grava é o pedido: uma requisição na
fila, endereçada à rotina que apaga o planejamento. Em seguida ela submete essa rotina e
responde **\* Cadastro sendo excluido \***. Quem apaga de fato os registros do
planejamento é a rotina de processamento, que também retira o pedido da fila quando
termina. Quem portar apenas esta tela não apaga planejamento nenhum: o pedido entra na
fila e o cadastro continua como estava.

### RN-10 — O pedido é numerado e leva a matrícula, a estação e a data

Cada pedido recebe o número seguinte ao do último pedido registrado na fila. Junto com
ele ficam o tipo de órgão da sessão, a matrícula e a estação do servidor, o dia e o mês
do pedido e o código da rotina de exclusão; o grupo e o período do planejamento viajam
como parâmetros dessa rotina. O e-mail do servidor é lido do cadastro e segue no
encaminhamento, mas não fica guardado no pedido.

[?] O que o processamento faz com o e-mail não se sabe pelo acervo; nesta tela ele não é
exigido e não é gravado no pedido. Pergunta ao site.

### RN-11 — Todo pedido de exclusão deixa rastro na trilha de auditoria

Antes de registrar o pedido, a tela grava um registro na trilha de auditoria com o tipo
de órgão, o grupo e o período que estão sendo excluídos, a matrícula, a estação, a data
e a hora e o número de processo. A operação fica marcada como inclusão, e não como
exclusão, e o valor anterior é preenchido com o período do planejamento, ficando o
posterior em branco.

[?] A trilha marca a operação como inclusão, embora o pedido seja de exclusão, e não
identifica o grupo em campo próprio — ele vai dentro do valor anterior. Se a trilha
registra o pedido ou a exclusão, o acervo não diz. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Excluir o planejamento sazonal de cardápios de um grupo da coordenação regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C768T

  Cenário: RN-01 — operação diferente de alteração
    Dado que estou na tela C768T
    Quando envio a tela com uma operação diferente de alteração
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E nada é consultado nem gravado

  Cenário: RN-02 — campo informado não numérico
    Quando informo um grupo ou uma parte da data limite que não é número
    Então o campo é recusado e o cursor volta para ele
    E nada é consultado no cadastro

  Cenário: RN-03 — grupo em branco
    Quando envio a tela sem informar o grupo
    Então vejo "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nada é gravado

  Cenário: RN-04 — sem planejamento para a data limite informada
    Dado que informo um grupo e uma data limite sem planejamento cadastrado
    Quando envio a tela
    Então vejo "* Nao existe planejamento sazonal para esta data *"
    E nada é gravado

  Cenário: RN-04 e RN-05 — o planejamento é encontrado e a data inicial vem do cadastro
    Dado que informo o grupo e a data limite de um planejamento cadastrado
    Quando envio a tela
    Então vejo a data inicial do período trazida do cadastro
    E a tela pergunta "* Confirma exclusao do planejamento <S/N> ? *"
    E nada foi gravado ainda

  Cenário: RN-03 e RN-05 — o grupo 99 vale por todos os grupos
    Dado que informo o grupo 99 e uma data limite com planejamento cadastrado
    Quando envio a tela e confirmo com S
    Então o pedido de exclusão alcança os planejamentos de todos os grupos naquela data limite

  Cenário: RN-06 — pedido de gêneros no período
    Dado que existe um pedido de gêneros do grupo cujo período de entrega cruza a validade do planejamento
    Quando envio a tela com o grupo e a data limite
    Então vejo "* Nao exclua. Ja existem pedidos cadastrados *"
    E o cursor volta à data limite
    E nada é gravado

  Cenário: RN-07 — pedido de exclusão em processamento
    Dado que há um pedido de exclusão desta rotina aguardando processamento
    Quando envio a tela com o grupo e a data limite de um planejamento cadastrado
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E nada é gravado

  Cenário: RN-07 — o pedido pendente bloqueia também quem é de outra secretaria
    Dado que há um pedido de exclusão desta rotina aguardando processamento, pedido por outra secretaria
    Quando um servidor de outra secretaria envia a tela com o grupo e a data limite de um planejamento do seu órgão
    Então ele também vê "* Relatorio em processamento. Aguarde. *"
    E nada é gravado

  Cenário: RN-08 — resposta diferente de S não exclui e repete a pergunta
    Dado que a tela já perguntou "* Confirma exclusao do planejamento <S/N> ? *"
    Quando respondo N
    Então a pergunta é feita de novo
    E nada é gravado

  Cenário: RN-08, RN-09, RN-10 e RN-11 — confirmar a exclusão
    Dado que a tela já perguntou "* Confirma exclusao do planejamento <S/N> ? *"
    Quando respondo S
    Então vejo "* Cadastro sendo excluido *"
    E o pedido fica registrado na fila, numerado em seguida ao último, com a minha matrícula, a estação, a data e o tipo de órgão
    E o pedido é encaminhado ao processamento que apaga o planejamento
    E o pedido deixa rastro na trilha de auditoria

  Cenário: RN-09 — o planejamento continua no cadastro até o processamento rodar
    Dado que confirmei a exclusão
    Então o planejamento ainda está no cadastro enquanto o processamento não roda
    E, quando ele roda, os registros do planejamento daquele grupo e daquela data limite são apagados
    E o pedido sai da fila
```
