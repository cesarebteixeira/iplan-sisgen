# US — E222T — Manter pedido acumulado do órgão filho

## Estória

Como **servidor da coordenação regional escolar**, quero **montar e manter o pedido
acumulado de um órgão filho — acumulando os gêneros dos pedidos de origem, ajustando
a quantidade a estornar de cada gênero e desfazendo o que não deve ficar acumulado**,
para que a secretaria tenha, num só pedido, todos os gêneros que as escolas pediram e
a quantidade que ainda pode ser estornada.

O acúmulo é o que dá ao gênero o seu lugar no pedido: enquanto o gênero não está
acumulado, ele não segue para o fornecimento, e é do acumulado que sai a quantidade
que ainda pode ser estornada. Sem esta tela, o acúmulo fica pela metade — o gênero não
entra, entra duas vezes, ou a quantidade a estornar fica acima do que foi pedido ou
acima do que ainda não foi recebido. É aqui que o servidor da CRE decide, gênero a
gênero, o que o órgão filho recebe.

## Contexto

Jornada S000M → E000M → E200M → E220M → E222T.

Ator: servidor de CRE — monta e mantém o pedido acumulado do órgão filho.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os três passos anteriores (E000M, E200M e E220M) são menus de opções: nenhum deles
tem pedido, gênero ou quantidade para passar adiante, e o que esta tela aproveita da
sessão é o que o LOGON deixou — a matrícula, a secretaria e, para quem tem, a
coordenação regional escolar e o órgão filho do vínculo do usuário. Esta tela também
é alcançada de outro jeito: a E221T, a tela dos gêneros do acumulado, pode chamá-la —
e é isso que decide se ela abre em consulta ou em alteração (RN-20).

## Regras de negócio

### RN-01 — O acumulado se identifica por órgão filho, coordenação, número do pedido e ano da entrega

O pedido sobre o qual se opera é identificado por quatro dados: o **órgão filho**
(oito dígitos), a **coordenação regional escolar** (dois dígitos), o **número do
pedido** (seis dígitos) e o **ano da entrega** (quatro dígitos). O número do pedido
que o sistema usa por dentro é o número justaposto ao ano da entrega — seis dígitos
seguidos de quatro —, e é essa chave de dez dígitos que liga o acumulado aos pedidos
de origem e aos gêneros. O mesmo desenho vale para o pedido auxiliar, que também é
informado como número mais ano.

### RN-02 — A tela edita 28 campos rotulados, e a grade tem 10 linhas de 6 campos

A tela edita **28 campos rotulados**: 23 no cabeçalho e 5 em cada linha da grade. Os do
cabeçalho são os quatro da identificação (RN-01); o código do fornecedor, o tipo de
contrato e o operador do pedido; o período (dia, mês e ano do início, dia, mês e ano do
limite); o código da subclasse e o código do gênero; a data de início do pedido (dia,
mês e ano) e o pedido auxiliar (número e ano); e os três totais, de quantidade pedida,
recebida e a estornar. Os da grade são o número do pedido de origem, o ano de entrega
do pedido de origem, a quantidade pedida, a quantidade recebida e a quantidade a
estornar.

A grade mostra **10 linhas** por vez e cada linha tem **6 campos**: os cinco da edição
mais a **ação** da linha — um código de uma posição, que não passa pela edição
numérica: `I` para incluir o pedido no acumulado, `A` para alterar a quantidade a
estornar e `E` para tirar o gênero do acumulado.

### RN-03 — A tela só trabalha em ALT (alterar) ou CON (consultar)

A opção de manutenção aceita apenas alteração e consulta; qualquer outra é recusada
com a mensagem de opção indisponível.

[?] A guarda interna compara o campo com os códigos de alteração e de consulta, mas a
mensagem manda usar "ALT" e "CON". Ou o terminal traduz o mnemônico antes de enviar,
ou a mensagem está desalinhada da guarda. Pergunta ao site; não concluo qual dos dois.

### RN-04 — Alterar exige ter consultado antes, e o acumulado tem que estar aberto

Para alterar, os quatro dados da identificação (RN-01) têm que ser exatamente os
mesmos da última consulta da sessão; se não forem, o sistema recusa e manda consultar
antes de atualizar. E um acumulado já fechado não se altera: a tentativa é recusada
com o aviso de pedido fechado.

### RN-05 — O órgão filho é obrigatório e passa por três peneiras

Sem o órgão filho informado, o sistema recusa e pede o órgão. Informado, ele é lido no
cadastro de órgãos e tem que passar por três peneiras, nesta ordem: existir e não
estar excluído; pertencer à mesma secretaria do usuário; e — quando o usuário tem
coordenação regional escolar no vínculo — ser do mesmo grupo dessa coordenação. Cada
peneira tem a sua própria mensagem.

### RN-06 — O pedido acumulado é obrigatório, tem que existir e estar marcado como acumulado

Sem número de pedido, o sistema recusa e pede o número. Informado, o pedido é lido na
secretaria do usuário; se não existir, a mensagem é de pedido não cadastrado. Depois
vêm as marcas de acúmulo: o pedido tem que estar marcado como acumulado — se a marca
estiver vazia, a recusa é de pedido não acumulado; e as duas marcas especiais, a de
acúmulo calculado e a de auxiliar do acúmulo calculado, são recusadas com mensagem
própria cada uma.

### RN-07 — O pedido acumulado tem que ser do órgão filho do usuário

Quando o servidor tem um órgão filho preso ao seu vínculo, o acumulado tem que ser de
pedido desse órgão: qualquer outro é recusado como pedido de outro órgão. Para quem
não tem órgão preso, a checagem não se aplica.

### RN-08 — O gênero é obrigatório, tem que estar cadastrado e pertencer ao acumulado

Sem a subclasse e o gênero, o sistema recusa e pede o gênero. Informado, o par
subclasse e gênero é lido no cadastro de gêneros — que esconde os excluídos, de modo
que um gênero excluído cai na mesma recusa de gênero não cadastrado. Por fim, o gênero
tem que estar no acumulado informado; se não estiver, a recusa é de gênero não
cadastrado neste pedido.

### RN-09 — A consulta não mexe nos vínculos do acumulado

Em consulta, o sistema pula todo o bloco de acúmulo e desacúmulo: nenhum gênero é
acumulado, nenhuma quantidade é alterada e nenhum registro de origem é apagado. A
consulta mostra o acumulado com o período, o fornecedor, o operador, a situação, os
gêneros e os três totais de quantidade do acumulado; e um acumulado que não tem
gênero nenhum avisa que não existem pedidos cadastrados.

[?] A passagem de gravação da tela, em consulta, é desviada para o mesmo ponto em que
a tela recalcula e regrava os totais do acumulado e a sua situação (RN-19) — se esse
trecho roda na consulta, consultar um acumulado pode mudar os totais e a situação do
pedido sem que ninguém tenha pedido alteração. O fonte não fecha isso com a guarda da
consulta; não concluo qual dos dois acontece. Pergunta ao site.

### RN-10 — Inclusão no acumulado: o pedido de origem passa por cinco peneiras

Na linha com ação `I`, o número do pedido e o ano de entrega informados apontam o
**pedido de origem**, cujos gêneros vão ser acumulados neste acumulado. O pedido de
origem tem que ser do mesmo ano da entrega do acumulado; existir na secretaria do
usuário; estar aprovado e não estar fechado; ser do mesmo fornecedor do acumulado; e
ter o início do seu período de entrega não anterior ao início do período do acumulado.
Cada peneira tem a sua mensagem.

### RN-11 — Inclusão: o gênero do pedido de origem tem que estar livre para ser acumulado

Dentro do pedido de origem, o gênero informado tem que existir; estar aprovado; não ter
quantidade recebida; não ter quantidade estornada; estar no mesmo tipo de contrato do
acumulado; e ainda não estar acumulado em outro pedido. Cada uma dessas condições tem
mensagem própria.

### RN-12 — Inclusão: o pedido de origem tem que caber na permissão de fornecimento

O fornecedor tem uma permissão de fornecimento por órgão, tipo de contrato,
coordenação regional escolar, subclasse e gênero, com uma janela de datas e um limite.
O período do acumulado tem que estar dentro de uma permissão dessas — o sistema
procura entre as permissões do par — e o limite de entrega do pedido de origem não
pode passar do limite da permissão encontrada. Se passar, a recusa é de pedido fora do
período da permissão; e se não existir permissão nenhuma para o par, a mesma recusa
aparece.

### RN-13 — Inclusão: a quantidade pedida do gênero no acumulado tem que ficar abaixo de 100.000

O sistema soma as quantidades pedidas daquele gênero em todas as linhas já acumuladas
e no pedido que está entrando. Enquanto o total fica abaixo de 100.000, a inclusão
segue; ao alcançar 100.000, a recusa é que a quantidade deve ser menor que 100.000.

### RN-14 — Alteração: a nova quantidade a estornar, diferente da atual e dentro do disponível

Na linha com ação `A`, o sistema localiza o gênero no acumulado; ele tem que estar
aprovado. A quantidade a estornar informada tem que ser **diferente** da que está
gravada — informar o mesmo valor é recusado com o pedido de informar nova quantidade —
e não pode passar do que ainda não foi recebido, isto é, da quantidade pedida menos a
recebida. Passando o que o gênero tem disponível para estorno, a recusa é própria.
Aceita, a quantidade informada passa a ser a quantidade a estornar do gênero, e o
total do gênero no acumulado é reajustado (RN-19).

[?] A alteração também reajusta a quantidade anotada na permissão de fornecimento do
gênero, mas a conta do programa não fecha com a variação da quantidade: ele soma a
quantidade antiga ao que já estava na permissão e desconta esse total do valor
informado. Não concluo o que a permissão passa a valer depois da alteração. Pergunta
ao site.

### RN-15 — Remoção: o gênero tem que estar acumulado, aberto e sem nada recebido

Na linha com ação `E`, o sistema localiza o gênero no acumulado; ele tem que estar
cadastrado neste acumulado; não estar fechado; e não ter quantidade recebida. Passando
pelas três, o gênero deixa de estar acumulado e o registro de origem dele é apagado.
Cada recusa tem a sua mensagem.

### RN-16 — Linha sem pedido ou com ação desconhecida é ignorada

Uma linha com o número do pedido zerado, ou com uma ação diferente de `I`, `A` e `E`,
é ignorada em silêncio: nenhuma mensagem é mostrada e nada é gravado por causa dela.

### RN-17 — O acerto em bloco pela data de início do pedido

Informando no cabeçalho a **data de início do pedido** (dia, mês e ano), o sistema não
trabalha linha a linha: ele acumula de uma vez todos os gêneros daquele tipo de
contrato cujo pedido de origem tem essa data de início, desde que o fornecedor do
pedido de origem seja o mesmo do acumulado e que os gêneros estejam livres — aprovados,
sem quantidade recebida, sem quantidade estornada e ainda não acumulados — e desde que
o limite de entrega de cada pedido de origem não passe do limite da permissão. A data
informada não pode ser anterior ao início do período do acumulado. Se nenhum gênero
servir, o sistema avisa que não há pedidos cadastrados ou aprovados; e se o total já
acumulado do gênero alcançar 100.000, vale a recusa de quantidade (RN-13).

### RN-18 — A remoção do gênero inteiro pela marca de exclusão

Quando a tela recebe ligada a marca de exclusão do acumulado, ela desfaz o acúmulo de
todos os gêneros informados no cabeçalho (a subclasse e o gênero) que não têm
quantidade recebida, e apaga os registros de origem deles. É o caminho inverso do
acerto em bloco e só vale quando a data de início do pedido não foi informada — com a
data informada, o acerto em bloco tem precedência.

[?] A marca de exclusão é um campo de entrada da tela que nenhum programa desta
jornada preenche: o programa apenas a lê e, na montagem da tela, a limpa. Sem saber
quem a liga — o mapa da tela, uma tecla de função ou a tela anterior —, o caminho de
remoção do gênero inteiro não é alcançável pelo caminho de menu. Pergunta ao site.

### RN-19 — A situação e os totais do acumulado são recalculados ao fim da passagem

Ao terminar a passagem, o sistema refaz as contas do acumulado: soma as quantidades
pedidas, recebidas e a estornar de todos os gêneros acumulados e grava esse resumo no
próprio acumulado. E recalcula a **situação**: o resumo do acumulado fica fechado
quando a quantidade pedida é igual à soma da recebida com a estornada, e aprovado
enquanto não for; a situação do pedido acumulado, por sua vez, é recalculada a partir
da situação dos gêneros e fica fechada quando não sobra gênero aberto. Se um gênero
acumulado estiver num tipo de contrato diferente do acumulado, o acúmulo desse gênero
é desfeito e o pedido acumulado volta a aprovado, sem operador.

### RN-20 — A tela se comporta diferente conforme quem a chamou, e entrega a vez à E221T

Quando a tela é chamada pela E221T — a tela dos gêneros do acumulado —, ela abre
forçada em consulta, mesmo que a opção informada seja de alteração, e devolve a vez à
E221T levando o acumulado no contexto e com a subclasse e o gênero zerados, para que a
E221T liste os gêneros daquele acumulado. Quando a tela chega com o código da tela
seguinte preenchido — isto é, está sendo encaminhada para a tela seguinte —, a
passagem de edição não faz nada.

[?] Nem a marca de "chamada por outra tela" nem o código da tela seguinte vêm de campo
digitável: são campos de entrada da tela que nenhum programa desta jornada preenche, e
o programa só os lê. Sem saber quem os liga, não é possível dizer, pelo caminho de
menu, quando a tela abre em consulta por ter sido chamada pela E221T. Pergunta ao site.

### RN-21 — Toda gravação deixa rastro na auditoria e trava o registro

Antes de gravar, o sistema trava o registro que vai alterar e registra a operação na
auditoria, com a matrícula do usuário, a data e a hora da sessão, a operação e o valor
anterior e o novo do registro. É assim para o acumulado, para o gênero, para a
permissão ajustada e para o registro de origem do gênero.

### RN-22 — Passagem que termina com recusa não grava nada

Se qualquer uma das recusas desta tela aparecer na passagem de edição, a passagem de
gravação é interrompida: o usuário vê a mensagem e nada do que ele informou é gravado.

## Cenários BDD

```gherkin
Funcionalidade: Montar e manter o pedido acumulado do órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E222T

  Cenário: RN-01 — consultar o acumulado pela identificação
    Dado que informo o órgão filho, a coordenação regional escolar, o número do pedido e o ano da entrega
    E a opção de manutenção CON
    Quando confirmo
    Então o sistema mostra o acumulado daquele pedido

  Cenário: RN-02 — a grade do acumulado
    Dado que consultei o acumulado
    Quando a tela é exibida
    Então vejo 10 linhas de grade
    E cada linha tem o pedido de origem, o ano de entrega, as quantidades pedida, recebida e a estornar, e a ação
    E vejo os três totais de quantidade do acumulado

  Cenário: RN-03 — opção de manutenção não disponível
    Dado que estou na tela E222T
    Quando informo uma opção de manutenção diferente de ALT e CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E nada é gravado

  Cenário: RN-04 — alterar sem consultar antes
    Dado que estou na tela E222T com a opção ALT
    E informo um pedido diferente do que consultei
    Quando confirmo
    Então vejo "* Consulte antes de atualizar *"
    E nada é gravado

  Cenário: RN-04 — alterar um acumulado fechado
    Dado que consultei um acumulado cuja situação é fechada
    Quando confirmo em ALT
    Então vejo "* Pedido fechado *"
    E nada é gravado

  Cenário: RN-05 — órgão filho não informado
    Dado que estou na tela E222T
    Quando deixo o órgão filho zerado e confirmo
    Então vejo "* Informe o orgao *"
    E nada é gravado

  Cenário: RN-05 — órgão filho não cadastrado
    Dado que estou na tela E222T
    Quando informo um órgão filho que não existe no cadastro, ou que está excluído
    Então vejo "* Orgao nao cadastrado *"
    E nada é gravado

  Cenário: RN-05 — órgão filho de outra secretaria
    Dado que estou na tela E222T
    Quando informo um órgão filho que pertence a outra secretaria
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E nada é gravado

  Cenário: RN-05 — órgão filho de outro grupo
    Dado que o meu usuário tem coordenação regional escolar
    Quando informo um órgão filho de outra coordenação
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E nada é gravado

  Cenário: RN-06 — número do pedido não informado
    Dado que informei um órgão filho válido
    Quando deixo o número do pedido zerado e confirmo
    Então vejo "* Informe o numero do pedido *"
    E nada é gravado

  Cenário: RN-06 — pedido não cadastrado
    Dado que informei um órgão filho válido
    Quando informo um número de pedido que não existe
    Então vejo "* Pedido nao cadastrado *"
    E nada é gravado

  Cenário: RN-06 — pedido sem marca de acúmulo
    Dado que informei um pedido que existe e não está acumulado
    Quando confirmo
    Então vejo "* Pedido nao acumulado *"
    E nada é gravado

  Cenário: RN-06 — pedido cujo acúmulo é calculado
    Dado que informei um pedido marcado como acúmulo calculado
    Quando confirmo
    Então vejo "* Pedido acumulado calculado *"
    E nada é gravado

  Cenário: RN-06 — pedido auxiliar do acúmulo calculado
    Dado que informei um pedido marcado como auxiliar do acúmulo calculado
    Quando confirmo
    Então vejo "* Pedido auxiliar do acumulado calculado *"
    E nada é gravado

  Cenário: RN-07 — pedido de outro órgão filho
    Dado que o meu vínculo tem um órgão filho
    Quando informo um acumulado que é de outro órgão filho
    Então vejo "* Pedido de outro orgao *"
    E nada é gravado

  Cenário: RN-08 — gênero não informado
    Dado que consultei o acumulado
    Quando deixo a subclasse e o gênero zerados e confirmo
    Então vejo "* Informe o genero *"
    E nada é gravado

  Cenário: RN-08 — gênero não cadastrado
    Dado que consultei o acumulado
    Quando informo uma subclasse e um gênero que não existem no cadastro
    Então vejo "* Genero nao cadastrado *"
    E nada é gravado

  Cenário: RN-08 — gênero que não está no acumulado
    Dado que consultei o acumulado
    Quando informo um gênero cadastrado que não pertence a esse acumulado
    Então vejo "* Genero nao cadastrado neste pedido *"
    E nada é gravado

  Cenário: RN-09 — o caminho feliz da consulta
    Dado que consultei um acumulado com gêneros
    Quando confirmo em CON
    Então vejo o período, o fornecedor, o operador, a situação e os gêneros do acumulado
    E vejo os totais de quantidade pedida, recebida e a estornar
    E nenhum gênero é acumulado, alterado ou apagado

  Cenário: RN-09 — acumulado sem gêneros
    Dado que informei um acumulado que não tem gênero nenhum
    Quando ele é aberto
    Então vejo "* Nao existem pedidos cadastrados *"

  Cenário: RN-10 — o caminho feliz da inclusão
    Dado que consultei o acumulado e informei um gênero
    E informo uma linha com o pedido de origem do mesmo ano, aprovado, aberto, do mesmo fornecedor e dentro do período
    Quando preencho a linha com a ação I e confirmo
    Então os gêneros daquele pedido de origem passam a estar acumulados neste acumulado
    E o total do acumulado é recalculado
    E a operação fica registrada na auditoria

  Cenário: RN-10 — pedido de origem de outro ano
    Dado que consultei o acumulado
    Quando incluo uma linha cujo ano de entrega é diferente do ano do acumulado
    Então vejo "* Pedidos devem ser do mesmo ano *"
    E nada é gravado

  Cenário: RN-10 — pedido de origem não cadastrado
    Dado que consultei o acumulado
    Quando incluo uma linha com um pedido de origem que não existe
    Então vejo "* Pedido nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — pedido de origem com início anterior ao período
    Dado que consultei o acumulado
    Quando incluo um pedido de origem cujo início é anterior ao início do período do acumulado
    Então vejo "* Data menor que a data da entrega *"
    E nada é gravado

  Cenário: RN-10 — pedido de origem fechado
    Dado que consultei o acumulado
    Quando incluo um pedido de origem que está fechado
    Então vejo "* Pedido fechado *"
    E nada é gravado

  Cenário: RN-10 — pedido de origem não aprovado
    Dado que consultei o acumulado
    Quando incluo um pedido de origem que não está aprovado
    Então vejo "* Pedido nao aprovado *"
    E nada é gravado

  Cenário: RN-10 — pedido de origem de outro fornecedor
    Dado que consultei o acumulado
    Quando incluo um pedido de origem de outro fornecedor
    Então vejo "* Pedido de outro fornecedor *"
    E nada é gravado

  Cenário: RN-11 — gênero que não está no pedido de origem
    Dado que consultei o acumulado
    Quando incluo um pedido de origem que não tem o gênero informado
    Então vejo "* Genero nao cadastrado neste pedido *"
    E nada é gravado

  Cenário: RN-11 — gênero já acumulado
    Dado que consultei o acumulado
    Quando incluo um gênero que já está acumulado em outro pedido
    Então vejo "* <- Genero ja acumulado *"
    E nada é gravado

  Cenário: RN-11 — gênero com quantidade recebida
    Dado que consultei o acumulado
    Quando incluo um gênero que já tem quantidade recebida
    Então vejo "* Genero com quantidade recebida *"
    E nada é gravado

  Cenário: RN-11 — gênero com quantidade estornada
    Dado que consultei o acumulado
    Quando incluo um gênero que já tem quantidade estornada
    Então vejo "* Genero com quantidade estornada *"
    E nada é gravado

  Cenário: RN-11 — gênero em outro tipo de contrato
    Dado que consultei o acumulado
    Quando incluo um gênero cujo tipo de contrato é diferente do acumulado
    Então vejo "* Genero em outro tipo contrato *"
    E nada é gravado

  Cenário: RN-11 — gênero não aprovado
    Dado que consultei o acumulado
    Quando incluo um gênero que não está aprovado
    Então vejo "* Genero nao aprovado *"
    E nada é gravado

  Cenário: RN-12 — pedido fora da permissão de fornecimento
    Dado que consultei o acumulado
    Quando incluo um pedido de origem cujo limite de entrega passa do limite da permissão do fornecedor
    Então vejo "* Pedido fora do periodo da permissao *"
    E nada é gravado

  Cenário: RN-13 — quantidade do gênero acima do limite
    Dado que consultei o acumulado
    Quando a soma das quantidades pedidas do gênero alcança 100.000
    Então vejo "* Quantidade deve ser < 100000 *"
    E nada é gravado

  Cenário: RN-14 — o caminho feliz da alteração da quantidade a estornar
    Dado que consultei o acumulado e o gênero está aprovado
    Quando preencho a linha com a ação A e uma quantidade a estornar diferente da atual e dentro do que ainda não foi recebido
    Então a quantidade a estornar do gênero passa a ser a informada
    E o total do acumulado é recalculado
    E a operação fica registrada na auditoria

  Cenário: RN-14 — quantidade igual à que está gravada
    Dado que consultei o acumulado
    Quando altero a quantidade a estornar informando o mesmo valor que está gravado
    Então vejo "* Informe nova quantidade *"
    E nada é gravado

  Cenário: RN-14 — quantidade acima da disponível para estorno
    Dado que consultei o acumulado
    Quando altero a quantidade a estornar para mais do que a quantidade pedida menos a recebida
    Então vejo "* Quantidade > que a disponivel para estorno *"
    E nada é gravado

  Cenário: RN-14 — gênero não cadastrado no acumulado
    Dado que consultei o acumulado
    Quando altero a quantidade de um gênero que não está acumulado
    Então vejo "* Pedido nao cadastrado neste acumulado *"
    E nada é gravado

  Cenário: RN-14 — gênero não aprovado no acumulado
    Dado que consultei o acumulado
    Quando altero a quantidade de um gênero que não está aprovado
    Então vejo "* Pedido nao aprovado *"
    E nada é gravado

  Cenário: RN-15 — o caminho feliz da remoção
    Dado que consultei o acumulado e o gênero está aberto e sem quantidade recebida
    Quando preencho a linha com a ação E e confirmo
    Então o gênero deixa de estar acumulado
    E o registro de origem daquele gênero é apagado
    E o total do acumulado é recalculado

  Cenário: RN-15 — gênero fechado
    Dado que consultei o acumulado
    Quando removo um gênero que está fechado
    Então vejo "* Pedido fechado *"
    E nada é gravado

  Cenário: RN-15 — gênero com quantidade recebida
    Dado que consultei o acumulado
    Quando removo um gênero que tem quantidade recebida
    Então vejo "* Pedido com quantidade recebida *"
    E nada é gravado

  Cenário: RN-16 — linha ignorada
    Dado que consultei o acumulado
    Quando preencho uma linha sem o número do pedido, ou com uma ação diferente de I, A e E
    E confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada por causa dela
    E nada é gravado por causa dela

  Cenário: RN-17 — o acerto em bloco pela data de início
    Dado que consultei o acumulado
    E informei a data de início do pedido no cabeçalho
    Quando confirmo em ALT
    Então todos os gêneros daquele tipo de contrato, pedidos naquela data e ainda livres, passam a estar acumulados
    E os gêneros que já têm quantidade recebida, quantidade estornada ou acúmulo não são tocados
    E o total do acumulado é recalculado

  Cenário: RN-17 — nenhum gênero na data informada
    Dado que consultei o acumulado
    E informei uma data de início de pedido em que não há gênero livre
    Quando confirmo em ALT
    Então vejo "* Pedidos nao cadastrados ou nao aprovados *"
    E nada é gravado

  Cenário: RN-18 — a remoção do gênero inteiro pela marca de exclusão
    Dado que consultei o acumulado e informei a subclasse e o gênero
    E a tela chega com a marca de exclusão ligada
    Quando confirmo em ALT
    Então o acúmulo daquele gênero é desfeito em todos os pedidos de origem
    E os registros de origem daqueles gêneros são apagados
    E os gêneros que têm quantidade recebida não são tocados

  Cenário: RN-19 — a situação vira fechada
    Dado que consultei o acumulado
    Quando a quantidade pedida passa a ser igual à soma da recebida com a estornada em todos os gêneros
    Então a situação do acumulado fica fechada
    E os totais de quantidade pedida, recebida e a estornar ficam gravados no acumulado

  Cenário: RN-19 — gênero de outro tipo de contrato dentro do acumulado
    Dado que existe no acumulado um gênero cujo tipo de contrato é diferente do acumulado
    Quando a passagem termina
    Então o acúmulo daquele gênero é desfeito
    E o pedido acumulado volta a aprovado e sem operador

  Cenário: RN-20 — a tela chamada pela E221T
    Dado que a tela foi chamada pela E221T
    Quando ela é aberta, mesmo com a opção ALT
    Então ela abre em consulta
    E devolve a vez à E221T levando o acumulado no contexto, com a subclasse e o gênero zerados

  Cenário: RN-20 — a tela chegando para a tela seguinte
    Dado que a tela chegou com o código da tela seguinte preenchido
    Quando a passagem de edição roda
    Então ela não edita nem grava nada

  Cenário: RN-21 — a auditoria de cada gravação
    Dado que uma operação desta tela vai gravar
    Quando ela é gravada
    Então fica registrada a matrícula, a data e a hora, a operação e o valor anterior e o novo do registro

  Cenário: RN-22 — passagem com recusa não grava
    Dado que a passagem de edição terminou com uma das recusas desta tela
    Quando a passagem de gravação roda
    Então nada do que eu informei é gravado
```
