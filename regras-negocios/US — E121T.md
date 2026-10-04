# US — E121T — Programar a entrega do pedido

## Estória

Como **servidor de CRE**, quero **programar a entrega do pedido, dizendo para cada
gênero quanto será entregue em cada dia do período e marcando cada gênero para
incluir, alterar ou excluir**, para que **o pedido fique com os itens e as
quantidades por dia de entrega que o órgão vai receber e passe a valer como pedido
aprovado, dentro do que o contrato do fornecedor permite**.

Um pedido é um cabeçalho e os itens dele: sem item não há gênero nem quantidade por
dia para entregar, e o pedido não existe na base de pedidos. Esta tela é onde o
pedido que a recuperação trouxe ganha os itens — e é a única porta por onde ele passa
a existir: ao fim da programação, o pedido com ao menos um item é criado como
**aprovado**, e o pedido sem item nenhum é excluído. Cada quantidade lançada consome o
saldo inicial do contrato daquele gênero, e todo movimento fica registrado na
auditoria. Sem esta tela, o pedido recuperado continuaria um cabeçalho sem itens, e o
contrato do fornecedor não teria pelo que responder.

## Contexto

Jornada S000M → E000M → E010M → E120T → E121T.
Ator: servidor de CRE — confere o pedido que veio da recuperação, lança por gênero a
quantidade de cada dia de entrega e marca cada gênero para incluir, alterar ou
excluir.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O `E000M` e o `E010M` são menus: não gravam nada e apenas encaminham. Da sessão a tela
usa a **secretaria** (o tipo de órgão do vínculo), a **matrícula**, o **código de
acesso**, o **privilégio** e a **estação**; e mostra no cabeçalho a **descrição da
secretaria** e a **data do sistema**.

Esta tela **não se abre por menu**: ela só atende quando vem da `E120T`, que a chama
passando o pedido já conferido e a operação marcada como **alteração**. É essa
passagem que decide o modo da tela — regra daqui, e a mais fácil de se perder, porque
não aparece em campo nenhum da tela nova. A tela também **não encadeia para outra**:
ao recusar, devolve a transação ao menu `E010M`; ao processar, reexibe a si mesma com
o pedido relido da base.

As regras abaixo são só as da tela desta jornada. O que já está na entrada não se
repete aqui; o que se revelou dela ao ler estes fontes está no anexo de evidências.

---

## Regras de negócio

### RN-01 — A tela só abre e só roda pelo caminho da recuperação do pedido

Esta tela não tem menu nem opção: ela só atende quando a passagem vem da `E120T`. A
marca de que a passagem veio de lá viaja junto com o pedido, e é a primeira coisa que
a tela olha. Vindo de qualquer outra origem, ela **não processa nada**: devolve a
transação ao menu `E010M` deixando nele a marca de que a passagem passou por aqui, e o
menu marca a **opção 16** — a que abre a `E120T` — e avisa
**\* Acesso deve ser feito pela tela E120T \***. É esse aviso que empurra de volta quem
tentou programar a entrega sem passar pela recuperação.

[?] A marca viaja pela área de trabalho comum das telas: os campos das duas áreas
coincidem, na mesma ordem, do modo de operação até o tipo de contrato, e nenhum
programa do acervo escreve o nome da `E120T` na área da tela de programação. Que as
duas áreas sejam o mesmo espaço é conclusão da leitura das duas declarações, não algo
documentado no acervo. Pergunta ao site.

### RN-02 — A tela só altera: qualquer outra operação é recusada

Programar a entrega é uma alteração do pedido. A tela confere a operação que veio na
transação e só segue com a **alteração**; com qualquer outra, a recusa é
**\* Opcao nao disponivel. Use ALT \***, com o cursor de volta ao campo da operação, e
nada mais é conferido, mostrado ou gravado. A operação também vem decidida por quem
chama: a recuperação passa sempre a alteração.

[?] A recusa manda usar a tecla **ALT**, mas a operação que a tela aceita é o
mnemônico interno da alteração, que não é o mesmo texto. Se o terminal traduz a tecla
para esse mnemônico antes de enviar, a regra é uma só; se não traduz, a mensagem
engana quem opera. O corpus não traz essa tradução. Pergunta ao site.

### RN-03 — O que a tela pede, e como o pedido é identificado

A tela se identifica como ORGAO FILHO SDI e trabalha com **dezenove campos
numéricos**: doze do cabeçalho — o órgão filho SDI, o grupo (CORD.REG.ESCOLAR), o
número do pedido, o ano da entrega, o código do fornecedor, o dia, o mês e o ano de
início do período, o dia, o mês e o ano limite do período e o tipo de contrato — e
sete de cada linha — a subclasse, o gênero e as **cinco quantidades de entrega**.
Todos passam pela edição numérica, e o campo em branco é tratado como zero.

O pedido **não é identificado pelo número sozinho**: a chave é o **número do pedido
junto com o ano da entrega** — o número na frente, o ano atrás. É essa chave que a
recuperação deixou e é ela que a tela usa para procurar os itens do pedido. Na tela, o
número e o ano aparecem separados, um desmembrado do outro.

### RN-04 — Como a tela abre: o cabeçalho e os dias vêm da recuperação

Ao ser aberta, a tela copia do que a recuperação deixou o **órgão filho SDI e o nome
do órgão**, o **grupo**, o **fornecedor e a razão social**, o **número do pedido**, o
**ano da entrega**, a **semana**, o **tipo de contrato** e o **período de entrega**
(início e limite). Para cada um dos até **cinco dias de entrega** que a recuperação
calculou, ela monta o texto **Dia DD/MM/AA** que aparece no cabeçalho. Abrir a tela
só lê: nada é gravado nem apagado.

A tela **não reconfere nada disso**: o cabeçalho vale como veio, e é ele que ela
entrega de volta. Ao longo de todo o trabalho ela lê **cinco cadastros** — o registro
das telas, os itens do pedido, o cadastro de gêneros, o cadastro de contratos e a base
de pedidos — e grava em **quatro**: os itens do pedido, o cadastro de contratos, a
base de pedidos e a auditoria `A010T`. Nenhum cadastro de órgão ou de fornecedor é
lido, e o cadastro de contratos só é lido para a permissão de cada gênero — nunca para
reconferir o fornecedor, o tipo de contrato ou o período do cabeçalho.

[?] Os campos do cabeçalho que a tela mostra **não voltam** para o trabalho: o grupo,
o fornecedor, o tipo de contrato, o período e os dias de entrega que a tela usa para
procurar o contrato, para gravar o item e para criar o pedido são sempre os que a
recuperação deixou, não os que estiverem na tela. O COBOL não diz quais desses campos
o formulário deixa digitar; se algum deles for de digitação, o que for digitado nele é
mostrado e ignorado. Pergunta ao site.

### RN-05 — Cada linha é um gênero do pedido, e a tela comporta treze

A tela percorre os itens do pedido um a um e mostra, em cada linha, a **subclasse**, o
**gênero**, a **descrição do gênero** lida do cadastro e as **cinco quantidades** já
programadas. A linha é a unidade de trabalho: é nela que se digita a quantidade de
cada dia e a marca da ação. As linhas que sobram depois do último item do pedido ficam
em branco, para receber gêneros novos.

A tela comporta **treze linhas**.

[?] O que acontece com o pedido que tiver mais de treze gêneros não está no fonte: os
que não couberem não aparecem, a tela não avisa e não recusa. Se existe outra tela ou
outra passagem para eles, o acervo não diz. Pergunta ao site.

### RN-06 — Pedido sem gêneros: não há o que programar

Quando o pedido que chegou não tem item nenhum, a tela avisa
**\* Pedido sem generos cadastrados \*** e não há linha para programar. É o que
acontece com o pedido que a recuperação entregou sem informar o pedido de cópia.

### RN-07 — Cada linha precisa de uma marca, e a marca decide o que acontece

A marca da linha diz o que fazer com aquele gênero: **incluir** um gênero novo no
pedido, **alterar** as quantidades de um gênero que já está nele, ou **excluir** o
gênero do pedido. A marca é conferida gênero a gênero, e a linha **sem gênero algum**
não é conferida nem gravada.

[?] A marca é de uma posição só e a tela não a exige nem diz quais marcas existem: a
linha com gênero e quantidade, mas com a marca em branco ou com outra letra, é
ignorada em silêncio — nada é conferido, nada é gravado e nada é avisado. Ou falta a
recusa que exige a marca, ou o silêncio é intencional. Pergunta ao site.

### RN-08 — Incluir: o gênero tem de existir no cadastro e ainda não estar no pedido

Para incluir, o gênero informado tem de estar no **cadastro de gêneros** — não
estando, a recusa é **\* Genero nao cadastrado \***, com o cursor no campo da
subclasse — e **não pode já estar no pedido** — estando, a recusa é
**\* Genero ja cadastrado neste pedido \***, também com o cursor no campo da
subclasse. Em nenhuma das duas nada é gravado.

### RN-09 — Alterar e excluir valem só para gênero que já está no pedido

Quem marca uma linha para alterar ou para excluir está dizendo que aquele gênero já
está no pedido. Não estando, a recusa é **\* Genero nao cadastrado neste pedido \***,
com o cursor no campo da subclasse, e nada é gravado.

### RN-10 — A quantidade é obrigatória

As cinco quantidades da linha são somadas, e a soma tem de ser maior que zero. Ficando
em branco, a recusa é **\* Informe quantidade \***, com o cursor no primeiro campo de
quantidade da linha.

### RN-11 — Só se informa quantidade nos dias de entrega que têm data

Cada quantidade da linha corresponde a um dia de entrega, na ordem do período. Se a
linha traz quantidade em um dia para o qual a recuperação não calculou data, a recusa
é **\* Inf. quantidade para dias de entrega validos \***, com o cursor no campo
daquela quantidade. O pedido não tem mais dias de entrega do que os que a recuperação
calculou.

### RN-12 — A quantidade tem de respeitar a fração do gênero

Cada quantidade informada tem de ser um **múltiplo exato da fração em que aquele
gênero é fornecido**, lida do cadastro de gêneros. Sobrando resto na divisão, a recusa
é **\* Quant. fracionada invalida para este genero \***, com o cursor no campo daquela
quantidade.

[?] Nada no acervo garante que a fração do gênero seja maior que zero: se ela vier
zerada, a divisão termina em erro de tamanho e o resto fica indefinido, de modo que a
tela pode recusar qualquer quantidade pelo mesmo motivo. Se o cadastro impede a fração
zerada, a dúvida não existe — o acervo não diz. Pergunta ao site.

### RN-13 — O gênero precisa de contrato vigente para aquele fornecedor

A permissão de entregar aquele gênero vem do **contrato**. **Na inclusão e na
alteração**, a tela procura, no cadastro de contratos, o contrato do **fornecedor**,
do **grupo**, do **tipo de contrato**, da **subclasse e do gênero** da linha e do
**limite de entrega** do pedido, e o contrato **não pode estar excluído**. Não
achando, ou achando um contrato cujo **período ainda não começou** na data de início
do pedido, a recusa é **\* Genero sem permissao \***, com o cursor no campo da marca,
e nada é gravado.

### RN-14 — A quantidade não pode passar do saldo inicial do contrato

Do contrato saem o **saldo inicial** — a soma das três parcelas de saldo que ele
guarda — e a **quantidade já pedida**. **Na inclusão e na alteração**, a quantidade já
pedida, somada ao que esta linha programa, não pode passar do saldo inicial; passando,
a recusa é **\* Quantidade insuficiente na permissao \***, com o cursor no campo da
marca, e nada é gravado. Na alteração, o que já estava programado no item é descontado
antes da soma; na exclusão, nem esta conferência nem a da RN-13 são feitas.

### RN-15 — Incluir grava o item e consome o contrato

Passadas as conferências, a inclusão grava, numa passagem, o **item do pedido** — com
as classes do gênero lidas do cadastro, a secretaria, o grupo, o gênero e a subclasse,
a matrícula de quem digitou, a data do dia, as **até cinco datas de entrega**, as
cinco quantidades e a soma delas e o tipo de contrato — e acerta o **contrato**,
somando à quantidade já pedida a que foi programada. Cada um dos dois movimentos deixa
um registro na **auditoria A010T**, com a operação, o conteúdo anterior e o posterior,
a matrícula, a estação, o número do processo, a data e a hora da sessão e a
secretaria.

### RN-16 — Alterar reescreve o item e acerta o contrato

A alteração reescreve as cinco quantidades e a soma do item que já está no pedido e
**devolve ao contrato a quantidade que o item tinha antes**, somando em seguida a
nova. O item e o contrato deixam, cada um, um registro na **auditoria A010T** com a
operação de alteração, o conteúdo anterior e o posterior e os dados da sessão.

### RN-17 — Excluir apaga o item e devolve a quantidade ao contrato

A exclusão apaga o item do pedido e **subtrai do contrato** a quantidade que ele
reservava, de modo que o saldo volte a ficar livre para outro item. O item excluído e
o contrato deixam, cada um, um registro na **auditoria A010T**, o item com a operação
de exclusão.

[?] A exclusão não confere contrato nenhum: o gênero sai do pedido e a devolução ao
saldo só acontece se, na hora de gravar, a leitura achar o contrato com o período já
começado. Não achando, o item some e a quantidade não volta a saldo nenhum, sem aviso
— e nada no fonte garante que o contrato seja achado, porque a exclusão nunca o
exigiu. Se a devolução é obrigatória, falta a recusa; se esse caminho é impossível, o
acervo não diz. Pergunta ao site.

### RN-18 — Sem item o pedido é excluído; com item, o pedido passa a existir aprovado

Ao fim da programação, a tela olha o pedido inteiro. Se ele **não tem nenhum item**,
apaga o pedido — se ele existir —, deixando o registro de exclusão na auditoria. Se
ele **tem ao menos um item** e ainda **não existe** na base de pedidos, a tela o cria
com a situação de **pedido aprovado**, com a data de aprovação e a data de digitação
do dia, e deixa o registro de inclusão na auditoria. Pedido que já existe e tem item
não é tocado.

[?] A tela grava os itens antes de fazer o pedido existir — e antes de apagá-lo: quem
for interrompido no meio da programação deixa item de pedido sem o cabeçalho do
pedido, e o acervo não mostra nada que junte os dois depois. Se a passagem completa é
premissa do desenho, ela não está escrita. Pergunta ao site.

### RN-19 — A tela não encadeia: ela devolve ao menu ou se reexibe

Esta tela não passa o pedido adiante. Quando recusa — isto é, quando a passagem não
vem da recuperação —, ela devolve a transação ao menu `E010M`, que responde marcando a
**opção 16** e avisando **\* Acesso deve ser feito pela tela E120T \***. Fora desse
caso a tela termina em si mesma: ela **se reexibe** com o pedido relido da base, já
com o que foi gravado.

[?] A jornada registra esta tela como quem "passa para E010M", e a única devolução ao
`E010M` no fonte é essa, que exige uma origem diferente da recuperação. Se existem
outros caminhos de saída, é pergunta ao site.

### RN-20 — Nada é mostrado nem gravado sem a conferência de tela, de sessão, de rota e de acesso

Na abertura, a tela confere que está **registrada** (senão **\* Tela nao disponivel \***)
e que o **código de acesso do servidor** alcança a tela. Ao enviar a transação, a
lógica de rota confere a tela de novo (**\* Tela nao cadastrada \***) e a operação de
alteração (**\* Operacao nao disponivel \***), e a segurança confere que o **perfil do
servidor libera a alteração** naquela tela (senão
**\* Acesso negado para esta operacao \***) e que a **estação é a da sessão** — em
outra estação o acesso é encerrado e a sessão volta à entrada. Sem passar por tudo,
nada é conferido, mostrado ou gravado.

---

## Cenários BDD

```gherkin
Funcionalidade: Programar a entrega do pedido do órgão filho SDI da coordenadoria regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, o grupo e a matrícula do meu vínculo
    E tenho acesso à tela E121T

  Cenário: A tela só abre pelo caminho da recuperação do pedido
    Dado que chego à tela E121T por qualquer caminho que não seja a E120T
    Quando a tela olha a marca da passagem
    Então ela não processa nada
    E a transação volta ao menu E010M
    E o menu marca a opção 16 e eu vejo "* Acesso deve ser feito pela tela E120T *"

  Cenário: A tela só altera
    Dado que a transação chega com uma operação que não é a alteração
    Quando a tela confere a operação
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor fica no campo da operação
    E nada é conferido, mostrado ou gravado

  Cenário: A tela se identifica pelo órgão filho SDI e identifica o pedido pelo número com o ano
    Quando abro a tela E121T
    Então vejo os dezenove campos numéricos da tela, com o órgão filho SDI à frente
    E o número do pedido e o ano da entrega aparecem separados, desmembrados da chave do pedido
    E os campos numéricos têm o branco tratado como zero antes das conferências

  Cenário: A tela abre com o cabeçalho e os dias que a recuperação deixou
    Dado que a E120T passou o pedido já conferido
    Quando abro a tela E121T
    Então vejo o órgão filho SDI com o nome do órgão, o grupo, o fornecedor com a razão
      social, o número do pedido, o ano da entrega, a semana, o tipo de contrato e o período
    E vejo o texto "Dia DD/MM/AA" para cada dia de entrega que a recuperação calculou
    E a tela não relê cadastro nenhum para reconferir esse cabeçalho
    E abrir a tela não grava nem apaga nada

  Cenário: Cada linha é um gênero do pedido, e a tela comporta treze
    Dado que o pedido tem gêneros
    Quando abro a tela E121T
    Então vejo uma linha por gênero do pedido, com a subclasse, o gênero, a descrição do
      gênero lida do cadastro e as quantidades já programadas
    E as linhas que sobram depois do último item ficam em branco, para os gêneros novos
    E a tela comporta treze linhas

  Cenário: Pedido sem gêneros
    Dado que o pedido que chegou não tem item nenhum
    Quando abro a tela E121T
    Então vejo "* Pedido sem generos cadastrados *"
    E não há linha para programar

  Cenário: A marca da linha decide o que acontece
    Dado que informei a subclasse, o gênero e as quantidades de uma linha
    Quando marco a linha para incluir, para alterar ou para excluir
    Então a linha é conferida como inclusão, como alteração ou como exclusão daquele gênero
    E a linha sem gênero algum não é conferida nem gravada

  Cenário: A linha com a marca em branco é ignorada em silêncio
    Dado que informei o gênero e as quantidades de uma linha
    Quando deixo a marca da ação em branco, ou escrevo outra coisa que não seja a marca de
      incluir, de alterar ou de excluir
    Então nada é conferido, nada é gravado e nada é avisado

  Cenário: Incluir exige gênero cadastrado
    Dado que marco a linha para incluir
    Quando informo um gênero que não está no cadastro de gêneros
    Então vejo "* Genero nao cadastrado *"
    E o cursor fica no campo da subclasse
    E nada é gravado

  Cenário: Incluir recusa gênero que já está no pedido
    Dado que marco a linha para incluir
    Quando informo um gênero que já está no pedido
    Então vejo "* Genero ja cadastrado neste pedido *"
    E o cursor fica no campo da subclasse
    E nada é gravado

  Cenário: Alterar e excluir exigem gênero que já está no pedido
    Dado que marco a linha para alterar ou para excluir
    Quando informo um gênero que não está no pedido
    Então vejo "* Genero nao cadastrado neste pedido *"
    E o cursor fica no campo da subclasse
    E nada é gravado

  Cenário: A quantidade é obrigatória
    Quando deixo as cinco quantidades da linha em branco
    Então vejo "* Informe quantidade *"
    E o cursor fica no primeiro campo de quantidade da linha

  Cenário: Só se informa quantidade nos dias de entrega que têm data
    Dado que informo quantidade em um dia de entrega para o qual não há data
    Quando confirmo a linha
    Então vejo "* Inf. quantidade para dias de entrega validos *"
    E o cursor fica no campo daquela quantidade

  Cenário: A quantidade tem de respeitar a fração do gênero
    Dado que informo uma quantidade que não é múltipla da fração daquele gênero
    Quando confirmo a linha
    Então vejo "* Quant. fracionada invalida para este genero *"
    E o cursor fica no campo daquela quantidade

  Cenário: O gênero precisa de contrato vigente para aquele fornecedor
    Dado que marco a linha para incluir ou para alterar
    Quando informo um gênero que não tem contrato para aquele fornecedor, grupo, tipo de
      contrato e limite de entrega
    Então vejo "* Genero sem permissao *"
    Quando o contrato existe mas o período dele ainda não começou na data de início do pedido
    Então vejo "* Genero sem permissao *"
    E o cursor fica no campo da marca
    E nada é gravado

  Cenário: A quantidade não pode passar do saldo inicial do contrato
    Dado que marco a linha para incluir ou para alterar e o contrato já tem quantidade pedida
    Quando a quantidade já pedida somada à que eu programo passa do saldo inicial do contrato
    Então vejo "* Quantidade insuficiente na permissao *"
    E o cursor fica no campo da marca
    E nada é gravado
    E na alteração o que já estava programado no item é descontado antes da soma
    E na exclusão nem esta conferência nem a do contrato são feitas

  Cenário: Incluir grava o item e consome o contrato
    Dado que incluí um gênero novo no pedido, com quantidade em cada dia de entrega
    Quando a programação é gravada
    Então o item do pedido é gravado com as datas, as quantidades dos dias e a soma delas
    E o contrato passa a responder pela quantidade programada, somada à já pedida
    E o item e o contrato deixam, cada um, um registro na auditoria A010T

  Cenário: Alterar reescreve o item e acerta o contrato
    Dado que alterei as quantidades de um gênero que já está no pedido
    Quando a programação é gravada
    Então o item passa a valer com as novas quantidades e a nova soma
    E o contrato devolve a quantidade que o item tinha antes e recebe a nova
    E o item e o contrato deixam, cada um, um registro na auditoria A010T

  Cenário: Excluir apaga o item e devolve a quantidade ao contrato
    Dado que marquei para excluir um gênero que está no pedido
    Quando a programação é gravada
    Então o item é apagado do pedido
    E a quantidade que ele reservava volta ao contrato, se o contrato for encontrado
    E a exclusão do item e o acerto do contrato deixam registros na auditoria A010T

  Cenário: O pedido sem item é excluído
    Dado que ao fim da programação o pedido não tem nenhum item e existe na base de pedidos
    Quando a tela olha o pedido
    Então o pedido é apagado
    E a exclusão do pedido deixa um registro na auditoria A010T

  Cenário: O pedido com item passa a existir aprovado
    Dado que ao fim da programação o pedido tem ao menos um item e ainda não existe na base
      de pedidos
    Quando a tela olha o pedido
    Então o pedido é criado com a situação de pedido aprovado, com a data de aprovação e a
      data de digitação do dia
    E a inclusão do pedido deixa um registro na auditoria A010T
    Dado que o pedido já existe e tem item
    Então nada é feito com ele

  Cenário: A tela não encadeia
    Dado que a programação terminou
    Quando a tela encerra
    Então ela se reexibe com o pedido relido da base
    E o pedido não é passado para nenhuma tela seguinte

  Cenário: Nada acontece sem a conferência de tela, de sessão, de rota e de acesso
    Dado que estou na tela E121T
    Quando a conferência do registro da tela, do código de acesso, da estação, da rota ou
      da operação de alteração não passa
    Então vejo "* Tela nao disponivel *", "* Tela nao cadastrada *",
      "* Acesso negado para esta matricula *", "* Acesso negado para esta operacao *",
      "* Operacao nao disponivel *" ou o acesso é encerrado e a sessão volta à entrada
    E nada é conferido, mostrado ou gravado
```
