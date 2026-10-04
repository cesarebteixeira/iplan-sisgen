# US — E022T — Pedidos pendentes de alimentação escolar

## Estória

Como **servidor de CRE**, quero **percorrer os pedidos de alimentação escolar do
meu grupo que ainda estão pendentes de aprovação, informando a coordenadoria, o
número do pedido, o ano da entrega e o tipo de contrato — e pedir a impressão do
relatório quando precisar**, para que **a secretaria enxergue o que espera
aprovação e acompanhe, em papel, os pedidos e o contrato a que cada um se
liga**.

A aprovação do pedido de alimentação escolar passa por esta tela: é aqui que o
servidor escolhe o tipo de contrato e o pedido é conferido contra o que aquele
contrato ainda permite, gênero por gênero, antes de o pedido seguir adiante. Sem
esta passagem, o trabalho de distribuir os gêneros pelos dias de entrega não tem
como ser conferido contra a quantidade permitida, e o relatório de
acompanhamento sai sem o vínculo do pedido com o contrato.

## Contexto

Jornada S000M → E000M → E010M → E022T.
Ator: servidor de CRE — abre a tela pela opção do menu do pedido, vê os pedidos do
seu grupo que aguardam aprovação, percorre a lista, informa o tipo de contrato,
pede a impressão do relatório e passa para a tela de registro do pedido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A tela é do tipo transação e a última da jornada: ela não volta ao menu. Ao sair,
passa para a tela `E023T`, que registra o pedido de entrega; a passagem está
descrita em RN-14. A tela anterior da jornada, que levantou a quantidade de dias de
entrega, não deixa nesta o número do pedido nem o ano da entrega: esta tela os
reinicia na abertura e trabalha com a lista de pedidos do grupo.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — Como o pedido é identificado

O pedido é identificado pelo conjunto de quatro dados: a **coordenadoria regional
escolar** (2 dígitos), o **número do pedido** (6 dígitos), o **ano da entrega** (4
dígitos) e o **tipo de contrato** (3 dígitos). É por esse conjunto, junto com a
secretaria da sessão, que o sistema procura o pedido a mostrar; sem ele não há como
dizer de que pedido se está falando.

### RN-02 — A edição numérica dos campos, antes das conferências

Antes de qualquer conferência de negócio, quatro campos passam por edição numérica:
a coordenadoria regional escolar, o número do pedido, o ano da entrega e o tipo de
contrato. O campo em branco é tratado como zero, e o que não for número é recusado
antes das conferências. O indicador de operação, a tela de destino, a estação de
trabalho e o código de impressão **não** passam por essa edição.

### RN-03 — A coordenadoria da consulta vem da tela anterior; a lista vem do
registro de pedidos

Abrindo a tela, o sistema adota a coordenadoria regional escolar que a tela anterior
deixou, e lê a **coleção de pedidos da secretaria da sessão**, na ordem em que ela
está organizada — por tipo de órgão, coordenadoria, situação e, dentro deles, do ano
e do número mais antigos para os mais novos —, descartando os pedidos marcados como
excluídos. O primeiro pedido vivo que atende a essa ordem é o que a lista mostra, no
número do pedido e no ano da entrega.

[?] A tela percorre essa coleção de um pedido para o outro até doze vezes antes de
listar, e o pedido a mostrar é sempre o primeiro da ordem. Não se conclui do acervo
se o servidor consegue percorrer a lista inteira pedido a pedido, nem o que ele vê
quando o grupo tem mais de doze pendentes. Pergunta ao site.

### RN-04 — A coordenadoria informada tem de ser a do servidor

Se o vínculo da sessão traz uma coordenadoria regional escolar e o campo informado
traz outra, a tela recusa com **\* Usuario sem acesso a este grupo \***, com o cursor
de volta no campo da coordenadoria, e não grava nada. A conferência só vale quando a
sessão traz coordenadoria: o sistema não aceita uma coordenadoria que não seja a do
servidor, e a coordenadoria informada tem de pertencer à secretaria da sessão.

### RN-05 — A coordenadoria tem de pertencer a esta secretaria

A coordenadoria informada é procurada no cadastro de grupos. Não existindo para o
tipo de órgão da sessão, a tela recusa com **\* Grupo nao pertence a esta secretaria
\***, com o cursor no campo da coordenadoria, e não grava nada. Achada, ela é adotada
como a coordenadoria da consulta.

### RN-06 — Sem pedidos pendentes de aprovação, a tela para

Quando não há pedido pendente de aprovação para o grupo, a tela recusa com
**\* Grupo sem pedidos pendentes de aprovacao \***, com o cursor de volta no campo da
coordenadoria, e não grava nada. É por esta recusa que a tela diz que não há trabalho
de aprovação no grupo.

### RN-07 — A estação de trabalho tem de estar preenchida

Quando o código da estação de trabalho está marcado, o campo da estação de trabalho
tem de estar preenchido: em branco, a tela recusa com **\* A linha deve estar
preenchida \***, na linha que estava sendo conferida, e não grava nada. O mesmo
acontece quando o pedido é de um órgão fora do alcance do servidor (RN-08).

### RN-08 — O pedido tem de estar no alcance do servidor

Achado o pedido, a tela recusa, sem gravar nada, quando o órgão do pedido não é o do
vínculo da sessão: **\* Usuario sem acesso a este orgao \***. A conferência só vale
quando o vínculo da sessão traz órgão filho.

### RN-09 — O tipo de contrato é obrigatório

Para seguir, o servidor informa o tipo de contrato. Em branco ou zerado, a tela
recusa com **\* Informe tipo de contrato \***, com o cursor no campo do tipo de
contrato, e não grava nada.

### RN-10 — O tipo de contrato tem de estar cadastrado

O tipo de contrato informado é procurado no cadastro de tipos de contrato. Não
existindo para o tipo de órgão da sessão, a tela recusa com **\* Tipo de contrato nao
cadastrado \***, com o cursor no campo, e não grava nada.

### RN-11 — Cooperativa e SICI CRE se recusam: cada pedido é de um dos dois caminhos

O cadastro do tipo de contrato diz se ele é de cooperativa. Conforme esse dado e o
órgão do pedido, a tela recusa, sempre no campo do tipo de contrato e sem gravar
nada:

- **\* Nao use SICI CRE. Contrato nao Cooperativa \*** — quando o contrato **não** é
  de cooperativa e o pedido é de outro órgão que não o do grupo;
- **<- Use SICI CRE. Contrato Cooperativa \*** — quando o contrato **é** de
  cooperativa e o pedido é do mesmo órgão do grupo.

Ou seja: pelo caminho do SICI CRE só entram os pedidos do próprio grupo, e pelo
caminho da cooperativa só entram os de outro órgão. Não há combinação aceita.

### RN-12 — O pedido tem de ter gêneros cadastrados

O pedido é conferido gênero por gênero. Não havendo nenhum gênero vivo no pedido, a
tela recusa com **\* Pedido sem generos cadastrados \*** e não grava nada.

### RN-13 — A escolha do tipo de contrato é descartada: a operação da tela vira
consulta

Ao abrir, a tela escreve no próprio campo da operação o valor de **consultar**,
quaisquer que sejam a tela de origem e o indicador que ela tenha entregue. É esse
valor que a passagem de negócio lê depois: qualquer operação que não seja a consulta
encerra a passagem antes de chegar às conferências do tipo de contrato e do pedido.
Na prática, o servidor informa o tipo de contrato, a tela confere se ele é válido e
volta — **nada é aprovado, nada é gravado e a escolha do tipo de contrato é
descartada**.

[?] A tela prevê recusar, no campo da operação, quem não usar alterar ou consultar
(**\* Opcao nao disponivel. Use ALT ou CON \***), e a passagem de negócio logo abaixo
tem todo o caminho de conceder o contrato ao pedido e baixar a quantidade permitida —
mas o campo da operação é reescrito para consulta, pela própria tela, antes dessa
conferência, e a operação que ali chega nunca é a alteração. Ou a reescrita é o
defeito, ou o caminho de aprovação foi desativado de propósito. Não se conclui do
acervo qual dos dois. Pergunta ao site.

### RN-14 — O que a tela entrega à tela seguinte

Terminada a passagem, a tela abre a `E023T` e deixa na área de trabalho, para ela, a
coordenadoria regional escolar, o número do pedido e o ano da entrega da lista, e o
tipo de contrato informado. A tela seguinte, porém, abre sem o pedido em contexto:
não se conclui do acervo que ela aproveite esse número, e o servidor informa o pedido
lá.

### RN-15 — A tela só grava por causa da impressão; nenhuma outra operação grava

Das passagens desta tela, só a requisição de impressão grava. A consulta não cria,
não altera e não apaga nada: não toca no pedido, nos gêneros do pedido, no cadastro
de tipos de contrato nem no contador do número do pedido. Cada recusa encerra a
passagem antes de qualquer gravação, de modo que o pedido continua exatamente como
estava. Antes de qualquer uma delas, a tela confere se o servidor está na estação da
sessão, se a tela está registrada, se o código de acesso alcança a tela, se a rota
está certa e se ele tem a permissão da operação; qualquer uma dessas conferências
recusando encerra a passagem e nada é gravado.

### RN-16 — A requisição de impressão do relatório

Percorrida a lista, o servidor pode preencher o código de impressão. Achando o
relatório para o tipo de órgão, a coordenadoria e o código informado, a tela toma o
próximo número de requisição, registra a requisição com o ano, a coordenadoria, o
código de impressão, a matrícula do servidor, o relatório, o número da requisição, a
estação, a data, a operação de inclusão, a hora, o número do pedido da lista e o tipo
de órgão, e a entrega ao serviço de requisições do sistema, mostrando **\* Relatorio
em processamento. Aguarde. \***. Nenhum outro cadastro é tocado.

### RN-17 — Quando já há relatório em processamento para o servidor

A requisição é procurada pelo número que a sessão já reservou. Já existindo o
relatório para aquele número, a tela recusa com **\* Relatorio em processamento.
Aguarde. \***, com o cursor no campo do código de impressão, e não grava nada.

### RN-18 — Sem código de impressão, a tela termina a passagem

Não informado o código de impressão, a tela não segue para a tela seguinte nem grava
nada: ela encerra a passagem e volta a exibir a lista.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta e aprovação dos pedidos de alimentação escolar pendentes no grupo da CRE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenadoria regional escolar
      e o código de acesso
    E tenho acesso à tela E022T

  Cenário: A tela lista os pedidos pendentes do grupo
    Dado que vim da tela de pedidos do menu e a coordenadoria regional escolar da
      minha sessão tem pedidos pendentes de aprovação
    Quando a tela abre
    Então vejo o número do pedido e o ano da entrega do primeiro pedido pendente do
      grupo, na ordem em que a coleção de pedidos está organizada
    E os pedidos marcados como excluídos não aparecem
    E nada é gravado

  Cenário: O grupo não tem pedidos pendentes de aprovação
    Dado que não há pedido pendente de aprovação para a minha coordenadoria
    Quando confirmo a consulta
    Então vejo "* Grupo sem pedidos pendentes de aprovacao *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Coordenadoria que não é a do servidor
    Dado que o vínculo da minha sessão traz uma coordenadoria regional escolar
    Quando confirmo uma coordenadoria diferente
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Coordenadoria de outra secretaria
    Dado que informei uma coordenadoria que não existe para o tipo de órgão da minha
      sessão
    Quando confirmo a consulta
    Então vejo "* Grupo nao pertence a esta secretaria *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Campo numérico em branco antes das conferências
    Dado que estou na tela E022T
    Quando deixo um dos campos numéricos em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências de negócio
    E nenhuma conferência de negócio é feita sobre um valor não numérico

  Cenário: A operação da tela é sempre a consulta
    Dado que cheguei à tela E022T por qualquer caminho e com qualquer indicador de
      operação
    Quando a tela abre
    Então a operação que a passagem de negócio lê é a consulta
    E a conferência que recusa quem não usa alterar ou consultar não é alcançada

  Cenário: O tipo de contrato não foi informado
    Dado que há pedido pendente de aprovação para o meu grupo
    Quando confirmo sem informar o tipo de contrato
    Então vejo "* Informe tipo de contrato *"
    E o cursor fica no campo do tipo de contrato
    E nada é gravado

  Cenário: Tipo de contrato não cadastrado
    Dado que há pedido pendente de aprovação para o meu grupo
    Quando confirmo um tipo de contrato que não existe para o tipo de órgão da
      minha sessão
    Então vejo "* Tipo de contrato nao cadastrado *"
    E o cursor fica no campo do tipo de contrato
    E nada é gravado

  Cenário: Contrato que não é de cooperativa em pedido de outro órgão
    Dado que o tipo de contrato informado não é de cooperativa
    E que o pedido é de outro órgão que não o do meu grupo
    Quando confirmo
    Então vejo "* Nao use SICI CRE. Contrato nao Cooperativa *"
    E o cursor fica no campo do tipo de contrato
    E nada é gravado

  Cenário: Contrato de cooperativa em pedido do próprio grupo
    Dado que o tipo de contrato informado é de cooperativa
    E que o pedido é do mesmo órgão do meu grupo
    Quando confirmo
    Então vejo "<- Use SICI CRE. Contrato Cooperativa *"
    E o cursor fica no campo do tipo de contrato
    E nada é gravado

  Cenário: Pedido sem gêneros cadastrados
    Dado que há pedido pendente de aprovação para o meu grupo
    E que o pedido não tem nenhum gênero vivo
    Quando confirmo com o tipo de contrato válido
    Então vejo "* Pedido sem generos cadastrados *"
    E nada é gravado

  Cenário: Estação de trabalho em branco
    Dado que o código da estação de trabalho está marcado
    E que há pedido pendente de aprovação para o meu grupo
    Quando confirmo com o campo da estação em branco
    Então vejo "* A linha deve estar preenchida *"
    E o cursor fica na linha do pedido
    E nada é gravado

  Cenário: Pedido de outro órgão
    Dado que o vínculo da minha sessão traz um órgão filho
    E que o pedido é de outro órgão
    Quando confirmo
    Então vejo "* Usuario sem acesso a este orgao *"
    E o cursor fica na linha do pedido
    E nada é gravado

  Cenário: A escolha do tipo de contrato não grava nada
    Dado que há pedido pendente de aprovação para o meu grupo
    E que informei um tipo de contrato cadastrado e compatível com o pedido
    Quando confirmo a passagem
    Então o pedido não recebe o tipo de contrato
    E a quantidade permitida do contrato não é baixada
    E nenhum pedido, gênero ou contador é criado, alterado ou apagado
    E nada é gravado

  Cenário: A consulta e a recusa não gravam nada
    Dado que consultei a lista ou que a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então nenhum pedido, gênero ou contador foi tocado
    E nenhum registro de auditoria foi incluído
    E nenhuma requisição de impressão foi criada

  Cenário: A requisição de impressão do relatório
    Dado que percorri a lista
    E que a sessão ainda não reservou número de requisição para um relatório
    Quando informo o código de impressão e confirmo
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E fica registrada uma requisição com a minha matrícula, a estação, o ano, a
      coordenadoria, o código de impressão, o relatório, o número do pedido da lista
      e o tipo de órgão, na operação de inclusão
    E a requisição é entregue ao serviço de requisições do sistema
    E nenhum outro cadastro é tocado

  Cenário: Já há relatório em processamento
    Dado que o número de requisição reservado pela sessão já tem relatório
    Quando informo o código de impressão e confirmo
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor fica no campo do código de impressão
    E nada é gravado

  Cenário: Sem código de impressão a tela não segue
    Dado que não informei o código de impressão
    Quando confirmo a passagem
    Então a tela não abre a tela seguinte
    E volta a exibir a lista
    E nada é gravado

  Cenário: O que a tela entrega à tela seguinte
    Dado que terminei a passagem com um pedido da lista e um tipo de contrato
    Quando a tela abre a E023T
    Então deixa para a tela seguinte a coordenadoria regional escolar, o número do
      pedido e o ano da entrega da lista e o tipo de contrato informado
    E a E023T abre sem o pedido em contexto: o servidor informa o pedido lá
```
