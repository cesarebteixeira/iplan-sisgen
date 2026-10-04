# US — E221T — Gêneros do pedido acumulado de alimentação escolar

## Estória

Como **servidor de CRE**, quero **ver os gêneros que formam o pedido de alimentação
escolar acumulado do meu órgão e da minha coordenadoria regional escolar, com as
quantidades de cada um, e abrir o gênero que eu escolher**, para que **eu confira o que
já foi pedido, recebido e entregue daquele acumulado e chegue direto ao gênero que
precisa ser tratado**.

A alimentação escolar é distribuída por gênero, e um pedido acumulado é a soma dos
gêneros de vários pedidos do mesmo fornecedor. Quem confere o acumulado precisa ver,
gênero a gênero, quanto foi pedido, quanto já chegou e quanto ainda falta receber — e, do
que vê, abrir o gênero para tratá-lo. Sem esta lista, o acumulado seria uma caixa fechada:
o número do pedido, e nada dentro dele.

## Contexto

Jornada S000M → E000M → E010M → E040T → E221T.

Ator: servidor de CRE — confere o pedido acumulado que abriu na tela anterior, percorre a
lista dos seus gêneros e marca a linha do gênero que quer abrir.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Esta tela não se alcança por menu: quem a chama é a tela do pedido (`E040T`), quando o
pedido aberto é um pedido acumulado, e a chamada leva junto a operação de consulta e a
identificação do pedido. Da sessão a tela usa a matrícula, o código de acesso, o
privilégio, a estação, o tipo de órgão, a coordenadoria regional escolar e o órgão filho
do vínculo. Ela também não termina em si mesma: abre a tela do gênero — a `E222T` —, e o
que entrega a ela é regra desta estória.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela abre no pedido acumulado que a tela anterior entregou

O pedido não é procurado por esta tela. Ele chega pronto da tela anterior, que entrega a
operação e a identificação do pedido — o órgão filho, a coordenadoria regional escolar, o
número do pedido e o ano da entrega. Com isso a tela repõe o cabeçalho, mostra a razão
social do fornecedor, o nome do operador e o período de entrega, e monta a lista dos
gêneros daquele acumulado.

Quando a chamada não traz pedido nenhum, a tela fica em consulta, sem pedido e sem lista:
ela não varre o cadastro atrás de um.

[?] A situação que o cabeçalho mostra não vem do cadastro do pedido: ela é lida da posição
da área de trabalho que a tela anterior, por esta jornada, não preenche — ali está um
dígito do ano da entrega. O cabeçalho mostra **Aprovado** mesmo para um pedido fechado, e
o pedido fechado só é recusado quando o servidor confirma. Se a tela anterior deveria
entregar a situação, o acervo lido não mostra. Pergunta ao site.

### RN-02 — A operação: consulta ou alteração

A tela atende a duas operações, **consulta** e **alteração**. Vinda da tela do pedido, ela
abre em consulta. Antes de qualquer leitura, qualquer outra operação é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \*** e o cursor de volta ao campo da operação.

A operação governa o que a tela deixa fazer. Em consulta, a única coisa que o servidor
consegue fazer com a lista é abrir um gênero: marcar uma linha para incluir ou para
excluir não faz efeito nenhum. Incluir e excluir gênero exigem a alteração.

Em alteração, o órgão e o pedido que estão na tela têm de ser os mesmos que a tela
anterior entregou; mudando um deles, a recusa é **\* Consulte antes de atualizar \***, com
o cursor no campo da operação — o servidor tem de reabrir o pedido antes de alterá-lo.

[?] A mensagem manda usar "ALT" ou "CON", e a tela confere o campo da operação contra dois
códigos internos de três letras, o da consulta e o da alteração. Quem traduziria o que o
servidor digita nesses códigos não está no acervo lido. Pergunta ao site.

### RN-03 — A lista traz os gêneros do acumulado, nove por vez, com as quantidades

A lista mostra os gêneros que formam o pedido acumulado, **nove linhas por vez**, e cada
linha traz a subclasse e o gênero, a descrição do gênero, a quantidade pedida no
acumulado, a quantidade recebida, a quantidade a receber e a quantidade entregue, além da
coluna de ação da linha. A quantidade a receber é o que sobra da quantidade pedida depois
de descontadas a recebida e a entregue.

Quando o acumulado não tem nenhum gênero, a recusa é
**\* Pedido sem generos cadastrados \***.

### RN-04 — O órgão é conferido contra a secretaria e contra o grupo do servidor

O órgão filho tem de estar informado; em branco, a recusa é **\* Informe o orgao \***. Ele
é procurado no cadastro de órgãos e os órgãos marcados como excluídos são pulados; não
estando no cadastro, a recusa é **\* Orgao nao cadastrado \***. O órgão tem de ser da
secretaria da sessão: sendo de outra, a recusa é
**\* Orgao nao pertence a esta secretaria \***. E, quando o vínculo do servidor traz uma
coordenadoria regional escolar, o órgão tem de ser daquela coordenadoria: sendo de outra,
a recusa é **\* Usuario sem acesso ao grupo deste orgao \***.

Todas essas recusas devolvem o cursor ao campo do órgão, e nenhuma delas grava nada.

### RN-05 — O pedido é conferido contra o cadastro e contra o tipo de acumulação

O número do pedido tem de estar informado; em branco, a recusa é
**\* Informe o numero do pedido \***. O pedido é procurado no cadastro pela combinação do
órgão da tela, da coordenadoria do cadastro desse órgão e do número e do ano da entrega;
não estando, a recusa é **\* Pedido nao cadastrado \***.

Achado, o pedido tem de ser um pedido acumulado do tipo que esta tela trata. Faltando o
indicador de acumulação, a recusa é **\* Pedido nao acumulado \***; com o indicador de
acumulado calculado, **\* Pedido acumulado calculado \***; com o de auxiliar do acumulado
calculado, **\* Pedido auxiliar do acumulado calculado \***. Quando o vínculo do servidor
traz órgão filho e o pedido é de outro órgão, a recusa é **\* Pedido de outro orgao \***,
com o cursor no campo do órgão. E o pedido tem de ter pelo menos um gênero: sem nenhum, a
recusa é **\* Pedido sem generos cadastrados \***.

Todas as recusas desta regra devolvem o cursor ao campo do pedido — menos a do pedido de
outro órgão, que o devolve ao campo do órgão — e nenhuma delas grava nada.

As conferências desta regra e da anterior são as da passagem de consulta — a que esta
jornada usa. Passando para a alteração, a tela não as repete: exige apenas que o órgão e o
pedido continuem sendo os que a tela anterior entregou, mais a existência, a situação e as
datas do pedido.

[?] O indicador de acumulação tem três valores no acervo: um que esta tela aceita e dois
que ela recusa, com as mensagens acima. O que cada valor significa para o negócio, e o que
separa o acumulado que esta tela trata do "calculado" que ela recusa, o acervo lido não
diz. Pergunta ao site.

[?] Na consulta o pedido é procurado duas vezes: primeiro pela coordenadoria que está na
tela, depois pela coordenadoria do cadastro do órgão. Se as duas não forem a mesma,
nenhum registro satisfaz as duas leituras, e a recusa é **\* Pedido nao cadastrado \***
mesmo para um pedido que exista na coordenadoria do órgão. Se a intenção era aceitar as
duas, ou usar só a do órgão, o acervo lido não diz. Pergunta ao site.

### RN-06 — O pedido fechado não é tratado em operação nenhuma

Quando a situação gravada do pedido é **Fechado**, a tela recusa a passagem com
**\* Pedido fechado \*** e o cursor no campo da operação, antes de montar a lista e sem
gravar nada. A recusa vale também para a consulta: o acumulado fechado não se abre por
aqui.

[?] A tela recusa o pedido fechado em qualquer operação, mas é ela mesma que fecha o
pedido quando todos os itens se fecham (RN-12). Não se vê, no acervo lido, como o servidor
voltaria a consultar um acumulado já fechado. Pergunta ao site.

### RN-07 — A data informada não pode ser anterior ao início do período de entrega

Quando o servidor informa no cabeçalho a data do pedido, ela não pode ser anterior ao
início do período de entrega do pedido: sendo, a recusa é
**\* Data menor que a data da entrega \***, com o cursor de volta ao campo da data, e nada
é gravado. Sem data informada, nenhuma conferência de data é feita.

[?] A data do pedido é a mesma que a tela usa para religar os itens ao acumulado (RN-13) e
é ela que recorta a soma da quantidade da RN-08. Se a data é a do pedido, a do recebimento
ou uma data de referência do acumulado, o acervo lido não diz. Pergunta ao site.

### RN-08 — O gênero tem um teto de 100.000

Ao tratar o pedido, a tela percorre os gêneros que o acumulado tem e soma, para cada um, a
quantidade do gênero no próprio acumulado com a quantidade dos itens ainda abertos — sem
recebimento e sem entrega — do mesmo gênero e do mesmo fornecedor, na mesma data informada
e dentro do período do contrato.

Alcançando 100.000, a passagem é recusada com **<- Quantidade deve ser < 100000 \***,
precedida do código do gênero que estourou, e o cursor vai para o campo da data. Nada é
gravado nessa recusa.

[?] A soma procura os itens pela data informada no cabeçalho; com a data em branco ela
procura itens de data zero. Se a intenção era somar todos os itens abertos do gênero, a
data não deveria entrar na conta — e a mensagem aponta para o campo da data, não para a
linha do gênero. O acervo lido não permite decidir. Pergunta ao site.

### RN-09 — Incluir um gênero no acumulado

Com a operação de alteração, o servidor pode incluir no acumulado um gênero que ainda não
está lá: informa a subclasse e o gênero na linha e marca a linha para incluir. Antes de
gravar, a tela confere duas coisas: que o acumulado já tenha pelo menos um gênero — não
tendo, a recusa é **\* Pedido acumulado nao cadastrado \*** — e que o gênero informado
ainda não esteja no acumulado — estando, a recusa é
**\* Genero ja cadastrado neste acumulado \***. As duas devolvem o cursor ao campo de ação
da linha e não gravam nada.

Passando, a tela cria o gênero no pedido acumulado, com a matrícula de quem o incluiu, a
data de digitação do dia e o item em aberto, e registra a inclusão na auditoria.

### RN-10 — Excluir um gênero do acumulado

Em alteração, o servidor pode excluir do acumulado um gênero da lista, marcando a linha.
Antes de excluir, a tela exige que o gênero esteja no acumulado — não estando,
**\* Genero nao cadastrado neste acumulado \*** —, que o item não esteja fechado — estando,
**\* Item fechado neste pedido \*** — e que não haja quantidade recebida — havendo,
**\* Ja existe quantidade recebida \***. As três devolvem o cursor ao campo de ação da
linha e nada gravam nem apagam.

Passando, a exclusão tem dois efeitos: os itens que outros pedidos tinham acumulado neste
voltam a ser itens comuns dos pedidos de origem, e o gênero do próprio acumulado é apagado
do cadastro. A tela registra a alteração e a exclusão na auditoria.

[?] A conferência da quantidade recebida olha só o gênero do próprio acumulado, e a
devolução dos itens acumulados não confere se algum deles já tem recebimento. Se um item
devolvido com recebimento deveria barrar a exclusão, o acervo lido não diz. Pergunta ao
site.

### RN-11 — Marcar a linha abre a tela do gênero

Com a linha marcada para abrir, a tela lê a descrição do gênero e chama a tela do gênero —
a `E222T` —, entregando o pedido acumulado com o qual está trabalhando, a subclasse e o
gênero daquela linha e a operação em que ela está: vinda em consulta, a tela seguinte abre
em consulta naquele gênero. A marcação, por si só, não grava cadastro nenhum.

Uma linha sem gênero informado não abre nada.

### RN-12 — O item e o pedido se fecham sozinhos, e o acumulado que fica sem item é apagado

Na alteração, depois de mexer nos gêneros, a tela refaz a conta de cada gênero do
acumulado: soma as quantidades dos itens que o formam, calcula o recebido e o entregue, e
**fecha o item** quando a quantidade pedida fica igual à recebida mais a entregue. Fechados
todos os itens, o pedido passa a **Fechado** no cadastro; com qualquer item aberto, ele
fica **Aprovado**.

O pedido acumulado que fica sem nenhum gênero é **apagado do cadastro** — não é efeito de
lista. Tanto o fechamento quanto o apagamento deixam registro na auditoria.

E isso não é privilégio da alteração: a tela refaz a conferência da situação do pedido
mesmo numa passagem de consulta e, se a situação gravada não for a que resulta dos seus
itens, ela grava a situação nova. A consulta desta tela não é inerte.

[?] Numa passagem de consulta a tela pode gravar a situação do pedido — e é justamente a
consulta que esta jornada usa. Se a intenção era que a consulta só lesse, o acervo lido
não diz. Pergunta ao site.

### RN-13 — Informar a data do pedido religa os itens ao acumulado

Em alteração, quando o servidor informa no cabeçalho a data do pedido, a tela percorre cada
gênero da lista e procura os itens daquela data, daquele gênero e daquele fornecedor que
ainda estão abertos, sem quantidade recebida nem entregue e ainda não acumulados. O que
acha, ela liga ao pedido acumulado — gravando o item e o registro de nota fiscal
correspondente — e registra a operação na auditoria.

[?] O caminho inverso — desligar do acumulado os itens sem recebimento e apagar o registro
de nota fiscal deles — só roda quando um campo de controle da tela está preenchido e a
data está em branco; e a tela só limpa esse campo, nunca o preenche. Ou o campo vem
preenchido de fora do acervo lido, ou esse caminho é inalcançável por aqui. Pergunta ao
site.

### RN-14 — Sem autorização para a tela ou para a operação, nada acontece

A tela só abre para o código de acesso que a tem no cadastro de telas por código de acesso
— não tendo, a recusa é **\* Acesso negado para esta matricula \*** —, e a passagem passa
pela conferência de sessão, pela lógica de rota e pela conferência da operação antes de
qualquer leitura do pedido — sem a operação liberada, a recusa é
**\* Acesso negado para esta operacao \***. Nos dois casos nada é mostrado nem gravado.

A exclusão de gênero tem conferência própria: antes de apagar, a tela confere de novo a
liberação da operação de exclusão para aquele código de acesso naquela tela.

[?] O cadastro de telas por código de acesso guarda, separadamente, a liberação da
consulta, e nenhuma rotina do acervo lido compara esse campo: a consulta passa sem essa
conferência. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Gêneros do pedido de alimentação escolar acumulado

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E221T

  Cenário: Abrir a tela no acumulado que a tela do pedido entregou
    Dado que na tela E040T abri um pedido acumulado do meu órgão
    Quando chego à tela E221T
    Então vejo no cabeçalho o órgão, a coordenadoria, o número e o ano da entrega
      daquele pedido, o fornecedor, o operador e o período de entrega
    E vejo a lista dos gêneros daquele acumulado
    E nenhum pedido é procurado por conta da abertura

  Cenário: A tela não procura pedido por conta própria
    Dado que chego à tela E221T sem que a tela anterior tenha entregado um pedido
    Então a tela fica em consulta, sem pedido e sem lista
    E nenhum pedido é procurado

  Cenário: A lista mostra os gêneros do acumulado com as quantidades
    Dado que o acumulado que a tela anterior entregou tem gêneros cadastrados
    Quando abro a tela E221T
    Então cada linha traz a subclasse, o gênero, a descrição do gênero, a quantidade
      pedida, a recebida, a entregue e a que falta receber
    E a quantidade a receber é a pedida menos a recebida e a entregue
    E vejo no máximo nove linhas por vez

  Cenário: A lista de um acumulado sem gênero
    Dado que o acumulado que a tela anterior entregou não tem nenhum gênero
    Quando chego à tela E221T
    Então vejo "* Pedido sem generos cadastrados *"
    E a lista fica vazia

  Cenário: Operação diferente de consulta e de alteração
    Quando informo uma operação que não é consulta nem alteração e confirmo
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é mostrado nem gravado

  Cenário: Alterar sem reabrir o pedido
    Dado que estou na tela E221T em consulta
    Quando troco o órgão ou o pedido mostrado e passo para a alteração
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: Em consulta, marcar uma linha para incluir ou excluir não faz nada
    Dado que estou na tela E221T em consulta, com a lista montada
    Quando marco uma linha para incluir ou para excluir um gênero
    Então a lista continua igual
    E nenhum gênero é incluído ou excluído

  Cenário: Alterar o acumulado que a tela do pedido entregou
    Dado que cheguei à tela E221T com um pedido acumulado do meu órgão
    Quando passo para a alteração sem trocar o órgão nem o pedido
    Então a tela aceita a operação
    E passa a tratar os gêneros marcados na lista

  Cenário: Órgão em branco
    Dado que o meu vínculo não traz órgão filho
    Quando confirmo sem informar o órgão
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão não cadastrado
    Quando informo um órgão que não está no cadastro de órgãos e confirmo
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão excluído no cadastro não é aceito
    Quando informo um órgão marcado como excluído no cadastro e confirmo
    Então a tela procura o próximo órgão e me recusa como órgão não cadastrado
    E nada é gravado

  Cenário: Órgão de outra secretaria
    Quando informo um órgão de outra secretaria e confirmo
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão de outra coordenadoria
    Dado que o meu vínculo carrega uma coordenadoria regional escolar
    Quando informo um órgão de outra coordenadoria e confirmo
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Pedido em branco
    Quando confirmo sem informar o número do pedido
    Então vejo "* Informe o numero do pedido *"
    E o cursor fica no campo do pedido
    E nada é gravado

  Cenário: Pedido não cadastrado
    Quando informo um pedido que não existe no cadastro e confirmo
    Então vejo "* Pedido nao cadastrado *"
    E o cursor fica no campo do pedido
    E nada é gravado

  Cenário: Pedido sem indicador de acumulação
    Dado que o pedido informado não tem indicador de acumulação
    Quando confirmo
    Então vejo "* Pedido nao acumulado *"
    E o cursor fica no campo do pedido
    E nada é gravado

  Cenário: Pedido acumulado calculado
    Dado que o pedido informado tem o indicador de acumulado calculado
    Quando confirmo
    Então vejo "* Pedido acumulado calculado *"
    E o cursor fica no campo do pedido
    E nada é gravado

  Cenário: Pedido auxiliar do acumulado calculado
    Dado que o pedido informado tem o indicador de auxiliar do acumulado calculado
    Quando confirmo
    Então vejo "* Pedido auxiliar do acumulado calculado *"
    E o cursor fica no campo do pedido
    E nada é gravado

  Cenário: Pedido de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo um pedido de outro órgão e confirmo
    Então vejo "* Pedido de outro orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Pedido fechado
    Dado que o pedido acumulado está com a situação "Fechado" no cadastro
    Quando confirmo a passagem
    Então vejo "* Pedido fechado *"
    E o cursor fica no campo da operação
    E a lista não é tratada e nada é gravado

  Cenário: Data do pedido anterior ao início do período de entrega
    Quando informo uma data anterior ao início do período de entrega e confirmo
    Então vejo "* Data menor que a data da entrega *"
    E o cursor fica no campo da data
    E nada é gravado

  Cenário: O gênero no teto de 100.000
    Dado que a quantidade do gênero no acumulado somada à dos itens abertos do mesmo
      gênero e fornecedor alcança 100.000
    Quando confirmo a passagem
    Então vejo "<- Quantidade deve ser < 100000 *" com o código do gênero
    E o cursor fica no campo da data
    E nada é gravado

  Cenário: Incluir um gênero no acumulado
    Dado que estou em alteração no acumulado
    Quando informo a subclasse e o gênero de um gênero que ainda não está lá e marco a
      linha para incluir
    Então o gênero passa a fazer parte do acumulado, com o item em aberto
    E a inclusão fica registrada na auditoria

  Cenário: Incluir um gênero que já está no acumulado
    Dado que estou em alteração no acumulado
    Quando informo a subclasse e o gênero de um gênero que já está lá e marco a linha
      para incluir
    Então vejo "* Genero ja cadastrado neste acumulado *"
    E o cursor fica no campo de ação da linha
    E nada é gravado

  Cenário: Incluir quando o acumulado não tem gênero nenhum
    Dado que estou em alteração e o acumulado não tem nenhum gênero cadastrado
    Quando marco uma linha para incluir um gênero
    Então vejo "* Pedido acumulado nao cadastrado *"
    E o cursor fica no campo de ação da linha
    E nada é gravado

  Cenário: Excluir um gênero do acumulado
    Dado que estou em alteração no acumulado, com um gênero aberto e sem recebimento
    Quando marco a linha desse gênero para excluir
    Então os itens que outros pedidos tinham acumulado neste voltam a ser itens dos seus
      pedidos de origem
    E o gênero sai do acumulado
    E a exclusão fica registrada na auditoria

  Cenário: Excluir um gênero que não está no acumulado
    Dado que estou em alteração no acumulado
    Quando marco para excluir uma linha cujo gênero não está no acumulado
    Então vejo "* Genero nao cadastrado neste acumulado *"
    E o cursor fica no campo de ação da linha
    E nada é apagado

  Cenário: Excluir um item fechado
    Dado que estou em alteração no acumulado, com um gênero cujo item está fechado
    Quando marco a linha desse gênero para excluir
    Então vejo "* Item fechado neste pedido *"
    E o cursor fica no campo de ação da linha
    E nada é apagado

  Cenário: Excluir um gênero com quantidade recebida
    Dado que estou em alteração no acumulado, com um gênero que já tem quantidade
      recebida
    Quando marco a linha desse gênero para excluir
    Então vejo "* Ja existe quantidade recebida *"
    E o cursor fica no campo de ação da linha
    E nada é apagado

  Cenário: Marcar a linha e abrir o gênero na tela seguinte
    Dado que estou na tela E221T em consulta, com a lista montada
    Quando marco para abrir a linha de um gênero
    Então a tela abre a E222T naquele gênero
    E a tela seguinte abre em consulta, no mesmo acumulado, com a subclasse e o gênero
      daquela linha
    E nenhum cadastro é gravado pela marcação

  Cenário: Linha sem gênero não abre nada
    Dado que estou na tela E221T, com a lista montada
    Quando marco para abrir uma linha que não tem gênero informado
    Então a tela não abre a tela seguinte
    E nada é gravado

  Cenário: O item e o pedido se fecham quando tudo foi recebido e entregue
    Dado que estou em alteração no acumulado
    Quando a quantidade pedida de um gênero fica igual à recebida mais a entregue e
      confirmo
    Então esse item fica fechado
    E, com todos os itens fechados, a situação do pedido passa a "Fechado"

  Cenário: O acumulado que fica sem gênero é apagado
    Dado que estou em alteração no acumulado e excluo o seu último gênero
    Quando confirmo
    Então o pedido acumulado é apagado do cadastro
    E o apagamento fica registrado na auditoria

  Cenário: A consulta não mexe nos gêneros, mas confere a situação do pedido
    Dado que estou na tela E221T em consulta
    Quando confirmo sem marcar nenhuma linha
    Então nenhum gênero é incluído, alterado ou excluído
    E, se a situação gravada do pedido não for a que resulta dos seus itens, a tela
      grava a situação nova

  Cenário: Informar a data do pedido religa os itens ao acumulado
    Dado que estou em alteração no acumulado, com a data do pedido em branco
    Quando informo a data de um pedido e confirmo
    Então os itens daquela data, do mesmo gênero e fornecedor, ainda abertos e sem
      recebimento, passam a pertencer ao acumulado
    E o registro de nota fiscal deles é gravado
    E a operação fica registrada na auditoria

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem esta tela no cadastro de telas por código
      de acesso
    Quando abro a tela E221T
    Então vejo "* Acesso negado para esta matricula *"
    E nada é mostrado nem gravado

  Cenário: Tela fora do cadastro de telas
    Dado que esta tela não está no cadastro de telas
    Quando abro a tela E221T
    Então vejo "* Tela nao disponivel *"
    E nada é mostrado nem gravado

  Cenário: Sem autorização para excluir o gênero
    Dado que estou em alteração no acumulado
    E o meu código de acesso não tem a exclusão liberada nesta tela
    Quando marco uma linha para excluir
    Então vejo "* Acesso negado para esta operacao *"
    E o gênero não é excluído
```
