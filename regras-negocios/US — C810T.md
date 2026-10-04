# US — C810T — Manter cardápios e gêneros por segmento

## Estória

Como **servidor de CRE**, quero **manter o cardápio do meu órgão — a validade, a
descrição e os gêneros de cada segmento, com as quantidades — e, quando for o caso,
passar o cardápio para a tela das refeições**, para que **o que se serve em cada
segmento, em cada período, esteja cadastrado com os gêneros e as quantidades certas, e
as refeições daquele período possam ser ligadas a ele**.

O cardápio é o que amarra um período de validade aos gêneros que serão servidos,
segmento por segmento. É dele que o planejamento da alimentação escolar se serve: o
planejamento do segmento guarda, por dia da semana e por mês, o código do cardápio de
cada data — e é essa ligação que faz a exclusão de um cardápio ser recusada enquanto
ele estiver no planejamento. Quem cadastra cardápio sem gênero nenhum não tem o que
servir; quem exclui um cardápio que já está no planejamento derruba o que estava
montado. Por isso esta tela confere as duas pontas antes de gravar.

## Contexto

Jornada S000M → C000M → C800M → C811M → C810T (5 passos).
Ator: servidor de CRE — cadastra e mantém os cardápios do seu órgão e os gêneros de
cada segmento, pela validade do período.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O caminho até aqui é todo por menu: o C000M, o C800M e o C811M são menus, não gravam
nada e só encaminham. Nenhum deles deixa cardápio nem operação na sessão; o contexto
que esta tela usa — o tipo de órgão, a matrícula, o código de acesso, o privilégio, a
coordenação regional, a estação e a data do sistema — é o que a entrada deixou.

Esta é a tela de **manutenção** dos cardápios; a consulta sem manutenção é a C810C,
sua irmã no mesmo menu. Quando o servidor pede a passagem para as refeições, esta tela
**encadeia** na C815T e entrega o cardápio, com a operação de alteração (§RN-20).

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O que a tela mantém: o cardápio do órgão, a validade e os gêneros de cada segmento

O assunto é o cadastro dos cardápios do **tipo de órgão da sessão**. Cada cardápio tem
código, descrição, uma data de início e uma data limite de validade, e duas marcas: se
é cardápio de sobremesa e se tem fruta. Dentro de cada validade, o cardápio tem
**gêneros**, um a um por segmento, cada gênero com a sua subclasse, o seu código e uma
**quantidade** — e é essa quantidade que diz quanto daquele gênero entra no cardápio
daquele segmento.

A tela enxerga **onze** cadastros. **Seis** ela só lê: o título das telas (2.000
registros de capacidade), o segmento (200.000), o gênero (150.000), o cadastro de
conversão do gênero (100.000), o planejamento do segmento por dia da semana (200.000) e
o planejamento do segmento por mês (100.000). Em **cinco** ela grava: o cardápio
(100.000), o gênero do cardápio (500.000), o contador de códigos de cardápio por órgão
(100.000), as ligações do cardápio com as refeições (100.000 — esta só se apaga) e a
auditoria (60.000.000). Os números são de **dimensionamento**: o máximo esperado que o
dicionário de dados declara, não o volume cadastrado.

O tipo de órgão não se digita: é o da sessão, e ele entra na identificação de tudo o
que a tela lê e grava.

[?] O cadastro do cardápio tem quatro marcas de um caractere e um segundo código de
cardápio que esta tela nunca lê: ao criar o cardápio ela os deixa em branco (as marcas)
e zerados (o código). O que eles significam no negócio não vem do material lido.
Pergunta ao site.

### RN-02 — A abertura: em branco na consulta; com o que a sessão guardar, reposto

Ao abrir, a tela mostra a descrição do tipo de órgão e a data do sistema e olha a área
de trabalho da sessão. **Se não houver operação guardada ali, ela abre na consulta** e
com os campos do cardápio em branco. Se houver operação guardada — porque uma
mensagem anterior desta mesma tela já a deixou —, ela repõe essa operação e repõe
também o cardápio, o segmento, as duas datas e as marcas de sobremesa e fruta que
estiverem na área de trabalho.

A validade vem com uma marca de período fechado: estando fechado, a tela mostra
**FECHADO** no lugar da estimativa; não estando, mostra um traço.

[?] A área de trabalho é a mesma para todas as telas da sessão e nenhuma das telas
deste caminho a zera: se ela chegar com resíduo de outra tela — um cardápio, uma
operação de alteração —, esta tela abre com aquele conteúdo em vez de abrir em branco
na consulta. Se o ambiente limpa essa área a cada transação, o material não diz.
Pergunta ao site.

[?] A descrição do tipo de órgão e a data do sistema que a tela mostra saem de uma
área de trabalho que nenhum programa deste lote preenche: a entrada guarda os dois na
área da **sessão**, com outros nomes, e a única escrita na área que esta tela lê é a
inicialização em branco do programa de execução. Se o ambiente transporta um valor para
o outro, o material não diz. Pergunta ao site.

### RN-03 — São quatro operações, e nenhuma outra é aceita

A tela reconhece **quatro** operações no campo da operação: incluir, alterar, excluir e
consultar. Qualquer outra coisa informada nesse campo é recusada com
**\* Opcao nao disponivel. Use INC, ALT, EXC ou CON \***, o cursor volta ao campo da
operação e nada é lido nem gravado.

[?] A recusa manda usar INC, ALT, EXC ou CON, mas o que a tela repõe nesse campo, ao
abri-lo, é o código interno da operação — as quatro palavras em inglês que ela mesma
compara — e nenhum dos quatro mnemônicos da mensagem é reconhecido por ela. Ou o
formulário traduz o que o servidor digita antes de enviar, ou quem seguir a mensagem é
recusado. Pergunta ao site.

### RN-04 — A grade tem doze linhas, uma por gênero do segmento

Fora da grade a tela mostra o tipo de órgão, a data do sistema, o código e a descrição
do cardápio, a descrição do segmento, as duas datas e as marcas de sobremesa e fruta
(mostradas como **Sim** e **Nao**). A grade é uma página de **doze** linhas, uma por
gênero daquele cardápio naquele segmento; cada linha traz o código da subclasse, o
código do gênero, a descrição resumida do gênero, a sua unidade de conversão, a
quantidade do gênero no cardápio e o campo onde o servidor escreve o que fazer com a
linha. Não achando nenhum gênero, a tela avisa
**\* Cardapio sem generos cadastrados \*** e não monta a linha.

### RN-05 — O código do cardápio: informado, ou dado pelo sistema

O código do cardápio pode ser informado pelo servidor ou deixado em branco. Em branco,
na inclusão, o sistema **dá o número**: toma o contador de códigos do tipo de órgão,
soma um, e vai somando enquanto aquele código já estiver em uso por qualquer cardápio
do órgão; achado o primeiro livre, grava o contador com ele e usa esse código no
cardápio novo. Não existindo ainda o contador do órgão, o sistema levanta o maior
código de cardápio já usado pelo órgão, soma um e cria o contador com esse valor.

### RN-06 — A inclusão confere o segmento, a descrição e as duas datas

Para incluir, a descrição do cardápio é obrigatória: em branco, a recusa é
**\* Informe a descricao do cardapio \***. O segmento informado tem de existir no
cadastro de segmentos — não existindo, **\* Segmento nao cadastrado \***. As duas
datas são conferidas: data de início que não existe no calendário, com o ano fora de
1994 a 2099, é **\* Data inicial da validade invalida \***; data limite inválida é
**\* Data final da validade invalida \***; e início posterior ao limite é
**\* Data inicial maior que data final \***. Cada recusa devolve o cursor ao campo
recusado e nada é gravado.

### RN-07 — A inclusão recusa validade sobreposta, período fechado e início fora da validade

Um cardápio não pode ter duas validades que se cruzem. A tela procura os cardápios do
mesmo código com data limite imediatamente antes e imediatamente depois da informada e,
se a validade informada invadir qualquer uma delas, recusa com
**\* Cardapio ja cadastrado neste intervalo \***, com o cursor na data limite.

Ainda na inclusão, a tela olha o mês e o ano da data limite informada: se já existe
cardápio do órgão naquela validade com a marca de **fechado**, a inclusão é recusada
com **\* Cadastro fechado para este periodo \***; e se o cardápio achado começou em
outra data, a recusa é **\* <- Dt.inicio para esta validade \***, com a data do
cardápio achado à frente e o cursor no início da validade.

### RN-08 — Sobremesa e fruta: as duas marcas e a dependência entre elas

A marca de sobremesa e a de fruta são informadas com **S** ou **N**. Sobremesa fora
disso é **\* Inf.se card. de sobremesa ou nao com S ou N \***. Marcando que o cardápio
**não** é de sobremesa, a marca de fruta é forçada a **N** — cardápio que não é de
sobremesa não tem fruta. Marcando que **é** de sobremesa, a fruta tem de ser **S** ou
**N**; qualquer outra coisa é **\* Inf.se fruta ou nao com S ou N \***. Na alteração a
fruta só se mantém se estiver marcada como **S**; qualquer outro valor vira **N**.

### RN-09 — A cópia: um cardápio novo pode nascer dos gêneros de outro

Além de digitar os gêneros um a um, a inclusão aceita **copiar** de um cardápio que já
existe. Para isso o servidor informa três coisas: o código do cardápio de origem, o
segmento de origem e a data limite de origem. Informado o código de origem sem o
segmento, a recusa é **\* Informe segmento para copia \***; informado sem a data
limite de origem, **\* Informe dt.limite para copia \***. A origem tem de existir como
cardápio com gênero naquele segmento e naquela validade — não existindo, a recusa é
**\* Cardapio nao cadastrado \***, com o cursor no código de origem e nada é gravado.

E, antes de tudo isso, a inclusão verifica se o cardápio informado **já existe** com
aquele segmento e aquela validade: existindo, recusa com **\* Cardapio ja cadastrado \***
e o cursor volta ao código do cardápio. Passando, o sistema cria o cabeçalho do
cardápio novo (se ainda não houver um com aquele código e validade) e copia os gêneros
da origem para ele, um a um.

### RN-10 — Alterar e excluir exigem ter consultado o cardápio antes

A alteração só passa se o cardápio, o segmento e as datas que estão em tela forem os
mesmos do último cardápio que a sessão guardou — em geral, o que o servidor acabou de
consultar. Não sendo, a recusa é **\* Consulte o cardapio antes da atualizacao \***,
com o cursor no campo da operação e nada é lido nem gravado. A exclusão exige a mesma
coisa, com a recusa **\* Consulte o cardapio antes da exclusao \***. A consulta não
exige: ela mesma é que deixa o cardápio guardado para as outras duas.

### RN-11 — A alteração não muda o período do cardápio

Na alteração, o período informado tem de ser exatamente o do cardápio achado: mudando
qualquer uma das seis partes das duas datas, a recusa é
**\* Nao altere o periodo do cardapio \***, com o cursor no campo da operação. A
descrição continua obrigatória — em branco, **\* Informe a descricao do cardapio \*** —
e o período tem de estar aberto: estando **fechado**, a recusa é
**\* Cadastro fechado para este periodo \***. Passando, a alteração grava a descrição,
a marca de sobremesa e a de fruta; **o código, o segmento e as duas datas não mudam**.

### RN-12 — A exclusão apaga os gêneros, o cabeçalho e as ligações com as refeições

Excluído o cardápio, o sistema apaga os gêneros daquele cardápio **no segmento que
estava em tela**, uma linha por vez, e só depois disso apaga o cabeçalho do cardápio —
e, com ele, as ligações daquele cardápio com as refeições. O cabeçalho e as ligações
**não** são apagados enquanto sobrar qualquer gênero daquele cardápio e daquela
validade em qualquer segmento: nesse caso a exclusão apaga os gêneros do segmento em
tela e para aí. A exclusão também exige o período **aberto** — fechado, a recusa é
**\* Cadastro fechado para este periodo \***.

[?] A exclusão apaga os gêneros de **um** segmento — o que estava em tela —, mas só
apaga o cabeçalho e as ligações quando não sobra gênero em segmento nenhum. Se o
cardápio tem gêneros em dois segmentos, a exclusão deixa o cabeçalho e os gêneros do
outro segmento no cadastro, e nada em tela avisa disso. Se a intenção era apagar o
cardápio inteiro de uma vez, o caminho não faz. Pergunta ao site.

### RN-13 — O planejamento do segmento barra a exclusão do último gênero

O cardápio que está no planejamento do segmento — no planejamento por dia da semana ou
no planejamento por mês — não pode perder o **último** gênero: tirando o último, o
sistema procura o cardápio nos dois planejamentos daquele segmento e daquela validade
e, achando, recusa com a mensagem que traz o código da coordenação regional à frente e
o texto **<- Grupo - Card.no planejamento deste seg. \***. Enquanto restar mais de um
gênero, a retirada passa sem essa conferência, porque o cardápio continua no ar. A
exclusão do cardápio inteiro passa pela mesma conferência.

### RN-14 — Cada linha da grade pede uma ação: incluir, alterar ou excluir o gênero

Na linha da grade o servidor escreve o que fazer com aquele gênero: **I** para incluir o
gênero no cardápio, **A** para alterar a quantidade dele, **E** para retirá-lo do
cardápio. Linha em branco, ou com outra coisa escrita, não é tocada: o sistema lê e
confere aquela linha e nada grava nela. A marca da linha é digitada a cada mensagem — a
tela nunca a repõe — e a ação vale só para a linha em que estiver.

### RN-15 — Incluir um gênero exige que ele exista, esteja ativo e tenha as quantidades de conversão

Para incluir um gênero no cardápio, a subclasse e o gênero informados têm de existir no
cadastro de gêneros **na data limite da validade** — não existindo, ou existindo sem a
marca de **ativo**, a recusa é **\* Genero nao cadastrado \***, com o cursor na
subclasse. Achado, o gênero tem de ter as duas quantidades de conversão diferentes de
zero: a unidade de conversão zerada recusa com **\* Unidade de conversao zerada \*** e a
quantidade a fracionar zerada com **\* Quantidade a fracionar zerada \***, com o cursor
na subclasse. Por fim, a quantidade do gênero no cardápio é obrigatória: zerada, a
recusa é **\* Informe a Quantidade \***, com o cursor na quantidade.

Há um cadastro separado de conversão, usado quando a subclasse informada é a de código
**99**: nesse caso as duas quantidades de conversão vêm dele, e não do gênero.

[?] O que a subclasse de código 99 significa no negócio — e por que ela usa um cadastro
de conversão próprio — não vem do material lido. Pergunta ao site.

### RN-16 — O gênero que já está no cardápio não entra de novo

A mesma subclasse e o mesmo gênero não podem estar duas vezes no cardápio daquele
segmento e daquela validade. Já estando, a inclusão é recusada com
**\* Genero ja cadastrado neste cardapio \***, com o cursor na subclasse da linha, e
nada é gravado.

[?] A conferência que decide isso procura pela chave inteira do gênero no cardápio, e a
conferência irmã — a que decide se o gênero **está** no cardápio para alterar ou
excluir — não confere de volta o código lido, ao contrário das conferências do
cardápio. Se a leitura se posiciona no registro igual ou seguinte em vez de exigir a
chave exata, um gênero novo pode ser confundido com o gênero vizinho e a inclusão ser
recusada; se ela exige a chave exata, o gênero vizinho de um código pedido não é achado
e as recusas saem como se o gênero não existisse. Os dois comportamentos são compatíveis
com o que o material mostra. Pergunta ao site.

### RN-17 — Alterar e excluir gênero exigem que ele esteja no cardápio

Para alterar a quantidade de um gênero ou para retirá-lo, a subclasse e o gênero têm de
estar no cardápio daquele segmento e daquela validade. Não estando, a recusa é
**\* Genero nao cadastrado neste cardapio \***, com o cursor na subclasse. Retirar o
gênero que está lá passa pela conferência do planejamento (§RN-13) quando é o último.
Alterar exige a quantidade: zerada, **\* Informe a quantidade \***, com o cursor na
quantidade.

### RN-18 — A consulta não grava nada

A operação de consulta (ou a abertura sem operação guardada) mostra o cardápio e a sua
grade e **não grava nada**: nenhum gênero é criado, alterado ou apagado e nenhum
registro de auditoria é deixado. Para consultar, o código do cardápio é obrigatório —
em branco, **\* Informe o codigo do cardapio \*** —, o segmento tem de existir
(**\* Segmento nao cadastrado \***), a data limite tem de estar informada
(**\* Informe a data limite de validade \***), o cardápio tem de existir naquela
validade (**\* Cardapio nao cadastrado \***) e o cardápio tem de ter gênero naquele
segmento (**\* Segmento nao cadastrado neste cardapio \***). Em todas, o cursor volta ao
campo recusado e nada é gravado.

### RN-19 — Cada gravação deixa rastro na auditoria

Toda criação, alteração e exclusão — do cardápio, do gênero do cardápio e das ligações
com as refeições — é acompanhada de um registro de auditoria, com o tipo de órgão, o
código do cadastro que mudou, o registro antes e o depois, a operação, a matrícula, o
código de acesso, a estação, a data e a hora. O código da tela que provocou a mudança
também vai no registro. O contador de códigos é gravado sem esse rastro.

### RN-20 — A tela entrega o cardápio à tela das refeições

Quando a marca de passagem para as refeições está posta, esta tela **não faz a
manutenção**: ela confere que o cardápio existe naquela validade — não existindo, recusa
com **\* Cardapio nao cadastrado \*** e o cursor no código do cardápio — e entrega a
transação à tela das refeições (C815T).

O que ela entrega: a identificação de que a tela de origem é ela, a operação de
**alteração**, o cardápio e a sua descrição, o segmento e a sua descrição, as duas
datas, as marcas de sobremesa e fruta, a marca de período fechado e os códigos de
cardápio dos dias da semana. A tela das refeições abre em **alteração** com esse
cardápio carregado, porque a operação vem da entrega — é esse o efeito de encadear tela
em tela, sem menu no meio.

[?] A marca de passagem é um campo de um caractere que a tela só escreve como **N**, na
montagem da última linha da grade, e nunca como **S**; nenhum rótulo da ficha da tela
corresponde a ele. Quem a preenche com **S** — o formulário, um comando, ou outra tela —
o material não diz. Pergunta ao site.

### RN-21 — O acesso e a rota são conferidos antes de qualquer leitura

Na abertura, e de novo a cada mensagem do servidor, o sistema confere o acesso antes de
ler qualquer cadastro: primeiro a permissão de segurança do perfil para esta tela, na
abertura; depois o contexto da sessão, a rota e, na confirmação, a permissão da
operação. Sem isso, a tela não lê nada e não grava nada.

[?] O texto das recusas de acesso não está no material: as conferências são rotinas de
biblioteca, sem corpo no lote, e o texto sai da tabela de mensagens do sistema, que
também não está no lote. Pergunta ao site.

### RN-22 — O que se digita é conferido antes de qualquer leitura

Nenhum dos campos com rótulo é texto livre. Passam pela edição numérica, antes de
qualquer leitura de cadastro — em branco valendo zero —, **dezesseis** campos: o código
do cardápio, o código do segmento, as três partes da data de início, as três partes da
data limite, o código do cardápio de origem, o código do segmento de origem, as três
partes da data limite de origem, a subclasse, o gênero e a quantidade. O que não for
número é recusado no próprio campo, com o cursor de volta a ele. A quantidade admite
**vírgula** como separador decimal. Não passam por essa edição: o campo da operação, a
marca de sobremesa, a marca de fruta e a ação da linha.

[?] O texto dessa recusa não está no material: a edição é uma rotina de biblioteca, cujo
corpo não faz parte do lote, e o texto sai da tabela de mensagens do idioma, que também
não está no lote.

---

## Cenários BDD

```gherkin
Funcionalidade: Manutenção dos cardápios do órgão e dos gêneros de cada segmento

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C810T

  Cenário: RN-01 — o que a tela grava e o que ela só lê
    Dado que incluo um cardápio com um gênero
    Quando confirmo
    Então o cardápio e o gênero entram nos cadastros próprios, no tipo de órgão da minha sessão
    E cada mudança deixa o seu rastro na auditoria
    E o segmento, o gênero, o cadastro de conversão e os dois planejamentos não são alterados

  Cenário: RN-02 — abrir a tela sem operação guardada
    Dado que nenhuma tela desta sessão deixou operação nem cardápio guardados
    Quando abro a tela C810T
    Então ela abre na consulta
    E o código do cardápio, o segmento e as duas datas estão em branco
    E a grade não está montada

  Cenário: RN-02 — abrir a tela com o cardápio guardado na sessão
    Dado que já consultei um cardápio nesta sessão
    Quando abro a tela C810T de novo
    Então o cardápio, o segmento e as duas datas daquele cardápio voltam em tela
    E a operação guardada volta no campo da operação

  Cenário: RN-02 — o período fechado
    Dado que o cardápio em tela está com a validade fechada para estimativa
    Quando a tela é apresentada
    Então no lugar da estimativa aparece FECHADO
    E, não estando fechado, aparece um traço

  Cenário: RN-03 — operação que a tela não reconhece
    Quando informo no campo da operação uma operação que não é incluir, alterar, excluir nem consultar
    Então vejo "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: RN-04 — a grade do segmento
    Dado que o cardápio tem gêneros naquele segmento
    Quando consulto o cardápio
    Então vejo a grade com até doze linhas, uma por gênero
    E cada linha traz a subclasse, o gênero, a descrição resumida, a unidade de conversão e a quantidade
    E cada linha tem o seu campo de ação

  Cenário: RN-04 — cardápio sem gêneros
    Dado que o cardápio não tem nenhum gênero a mostrar
    Quando a tela é apresentada
    Então vejo "* Cardapio sem generos cadastrados *"
    E nenhuma linha da grade é montada

  Cenário: RN-05 — incluir sem informar o código
    Dado que deixo o código do cardápio em branco
    E informo a descrição, o segmento, o início e o limite da validade
    E marco que não é cardápio de sobremesa
    Quando confirmo a inclusão
    Então o sistema dá o próximo código livre do tipo de órgão
    E grava o contador de códigos com esse código

  Cenário: RN-05 — incluir informando o código
    Dado que informo um código de cardápio que ainda não existe no órgão
    E o restante do cabeçalho está preenchido
    Quando confirmo a inclusão
    Então o cardápio é criado com o código que informei

  Cenário: RN-06 — inclusão sem a descrição
    Quando confirmo a inclusão com a descrição do cardápio em branco
    Então vejo "* Informe a descricao do cardapio *"
    E o cursor volta ao campo da descrição
    E nada é gravado

  Cenário: RN-06 — segmento não cadastrado
    Dado que informo um código de segmento que não existe
    Quando confirmo a inclusão
    Então vejo "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento
    E nada é gravado

  Cenário: RN-06 — datas inválidas
    Quando confirmo a inclusão com uma data de início que não existe no calendário
    Então vejo "* Data inicial da validade invalida *"
    E o cursor volta ao campo do dia de início
    E nada é gravado

  Cenário: RN-06 — data limite inexistente
    Quando confirmo a inclusão com uma data limite que não existe no calendário
    Então vejo "* Data final da validade invalida *"
    E o cursor volta ao campo do dia limite
    E nada é gravado

  Cenário: RN-06 — início depois do limite
    Dado que informo a data de início posterior à data limite
    Quando confirmo a inclusão
    Então vejo "* Data inicial maior que data final *"
    E o cursor volta ao campo do dia de início
    E nada é gravado

  Cenário: RN-07 — validade que se cruza com outro cardápio do mesmo código
    Dado que já existe um cardápio com este código numa validade vizinha
    E a validade que informei invade aquela
    Quando confirmo a inclusão
    Então vejo "* Cardapio ja cadastrado neste intervalo *"
    E o cursor volta ao campo do dia limite
    E nada é gravado

  Cenário: RN-07 — período fechado
    Dado que a validade daquele mês está fechada para estimativa
    Quando confirmo a inclusão de um cardápio naquela validade
    Então vejo "* Cadastro fechado para este periodo *"
    E o cursor volta ao campo do dia de início
    E nada é gravado

  Cenário: RN-07 — início diferente do da validade
    Dado que já existe cardápio do órgão naquela validade, começando em outra data
    Quando confirmo a inclusão
    Então vejo, com a data daquele cardápio à frente, "* <- Dt.inicio para esta validade *"
    E o cursor volta ao campo do dia de início
    E nada é gravado

  Cenário: RN-08 — sobremesa não informada como S ou N
    Quando confirmo a inclusão com a marca de sobremesa fora de S e N
    Então vejo "* Inf.se card. de sobremesa ou nao com S ou N *"
    E o cursor volta ao campo da marca de sobremesa
    E nada é gravado

  Cenário: RN-08 — fruta não informada como S ou N
    Dado que marquei o cardápio como de sobremesa
    Quando confirmo a inclusão com a marca de fruta fora de S e N
    Então vejo "* Inf.se fruta ou nao com S ou N *"
    E o cursor volta ao campo da marca de fruta
    E nada é gravado

  Cenário: RN-08 — cardápio que não é de sobremesa não tem fruta
    Dado que marquei que o cardápio não é de sobremesa
    E deixei a marca de fruta em S
    Quando confirmo a inclusão
    Então o cardápio é gravado com a marca de fruta em N

  Cenário: RN-09 — incluir copiando os gêneros de outro cardápio
    Dado que informo um código de cardápio que ainda não existe
    E informo o código do cardápio de origem, o segmento de origem e a data limite de origem, com gêneros
    Quando confirmo a inclusão
    Então o cardápio novo é criado com o meu cabeçalho
    E os gêneros da origem são copiados para ele

  Cenário: RN-09 — cópia sem o segmento de origem
    Dado que informo o código do cardápio de origem e deixo o segmento de origem em branco
    Quando confirmo a inclusão
    Então vejo "* Informe segmento para copia *"
    E o cursor volta ao campo do segmento de origem
    E nada é gravado

  Cenário: RN-09 — cópia sem a data limite de origem
    Dado que informo o código e o segmento de origem e deixo a data limite de origem em branco
    Quando confirmo a inclusão
    Então vejo "* Informe dt.limite para copia *"
    E o cursor volta ao campo do dia limite de origem
    E nada é gravado

  Cenário: RN-09 — origem da cópia que não existe
    Dado que o cardápio de origem informado não tem gênero naquele segmento e naquela validade
    Quando confirmo a inclusão
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor volta ao campo do código do cardápio de origem
    E nada é gravado

  Cenário: RN-09 — cardápio que já existe
    Dado que já existe cardápio com aquele código, aquele segmento e aquela validade
    Quando confirmo a inclusão
    Então vejo "* Cardapio ja cadastrado *"
    E o cursor volta ao campo do código do cardápio
    E nada é gravado

  Cenário: RN-10 — alterar sem ter consultado
    Dado que o cardápio em tela não é o último que a sessão guardou
    Quando confirmo a alteração
    Então vejo "* Consulte o cardapio antes da atualizacao *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: RN-10 — excluir sem ter consultado
    Dado que o cardápio em tela não é o último que a sessão guardou
    Quando confirmo a exclusão
    Então vejo "* Consulte o cardapio antes da exclusao *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: RN-11 — alterar a descrição, a sobremesa e a fruta
    Dado que consultei o cardápio, que a validade dele está aberta e que não mexi no período
    Quando altero a descrição e as marcas e confirmo
    Então a descrição, a marca de sobremesa e a de fruta passam a ser as que informei
    E o código, o segmento e as duas datas continuam os mesmos

  Cenário: RN-11 — alterar o período do cardápio
    Dado que consultei o cardápio e mudei uma das datas
    Quando confirmo a alteração
    Então vejo "* Nao altere o periodo do cardapio *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: RN-11 — alterar sem a descrição
    Dado que consultei o cardápio e deixei a descrição em branco
    Quando confirmo a alteração
    Então vejo "* Informe a descricao do cardapio *"
    E o cursor volta ao campo da descrição
    E nada é gravado

  Cenário: RN-12 — excluir o cardápio consultado
    Dado que consultei o cardápio, que a validade dele está aberta e que ele não está no planejamento do segmento
    Quando confirmo a exclusão
    Então os gêneros daquele cardápio naquele segmento são apagados
    E o cabeçalho do cardápio é apagado
    E as ligações daquele cardápio com as refeições são apagadas

  Cenário: RN-12 — validade fechada
    Dado que consultei o cardápio e a validade dele está fechada para estimativa
    Quando confirmo a exclusão
    Então vejo "* Cadastro fechado para este periodo *"
    E o cursor volta ao campo do dia de início
    E nada é apagado

  Cenário: RN-13 — retirar o último gênero de um cardápio que está no planejamento
    Dado que consultei o cardápio e ele tem um único gênero naquele segmento
    E o cardápio está no planejamento daquele segmento
    Quando marco a linha para excluir e confirmo
    Então vejo, com o código da coordenação regional à frente, "<- Grupo - Card.no planejamento deste seg. *"
    E o cursor volta à ação da linha
    E nada é apagado

  Cenário: RN-13 — retirar um gênero quando ainda restam outros
    Dado que consultei o cardápio e ele tem mais de um gênero naquele segmento
    E o cardápio está no planejamento daquele segmento
    Quando marco a linha para excluir e confirmo
    Então o gênero é retirado do cardápio
    E nenhuma conferência de planejamento é feita

  Cenário: RN-14 — linha sem ação
    Dado que consultei o cardápio e deixei a ação de todas as linhas em branco
    Quando confirmo
    Então nenhum gênero é criado, alterado ou apagado

  Cenário: RN-14 — linha com ação que a tela não reconhece
    Dado que escrevi na linha uma ação que não é I, A nem E
    Quando confirmo
    Então aquela linha não é tocada
    E nada é gravado nela

  Cenário: RN-15 — incluir um gênero no cardápio
    Dado que a subclasse e o gênero informados existem, estão ativos e têm as quantidades de conversão
    E que o gênero ainda não está neste cardápio
    E que informei a quantidade
    Quando marco a linha para incluir e confirmo
    Então o gênero entra no cardápio daquele segmento e daquela validade, com a quantidade informada

  Cenário: RN-15 — gênero não cadastrado
    Dado que a subclasse e o gênero informados não existem no cadastro de gêneros
    Quando marco a linha para incluir e confirmo
    Então vejo "* Genero nao cadastrado *"
    E o cursor volta à subclasse da linha
    E nada é gravado

  Cenário: RN-15 — gênero sem a marca de ativo
    Dado que o gênero existe, mas não está ativo
    Quando marco a linha para incluir e confirmo
    Então vejo "* Genero nao cadastrado *"
    E nada é gravado

  Cenário: RN-15 — unidade de conversão zerada
    Dado que o gênero está cadastrado com a unidade de conversão zerada
    Quando marco a linha para incluir e confirmo
    Então vejo "* Unidade de conversao zerada *"
    E o cursor volta à subclasse da linha
    E nada é gravado

  Cenário: RN-15 — quantidade a fracionar zerada
    Dado que o gênero está cadastrado com a quantidade a fracionar zerada
    Quando marco a linha para incluir e confirmo
    Então vejo "* Quantidade a fracionar zerada *"
    E o cursor volta à subclasse da linha
    E nada é gravado

  Cenário: RN-15 — incluir sem a quantidade
    Dado que deixei a quantidade do gênero zerada
    Quando marco a linha para incluir e confirmo
    Então vejo "* Informe a Quantidade *"
    E o cursor volta à quantidade da linha
    E nada é gravado

  Cenário: RN-16 — incluir um gênero que já está no cardápio
    Dado que o gênero já está neste cardápio, naquele segmento e naquela validade
    Quando marco a linha para incluir e confirmo
    Então vejo "* Genero ja cadastrado neste cardapio *"
    E o cursor volta à subclasse da linha
    E nada é gravado

  Cenário: RN-17 — alterar a quantidade de um gênero do cardápio
    Dado que consultei o cardápio e o gênero está nele
    E informei uma quantidade nova
    Quando marco a linha para alterar e confirmo
    Então a quantidade daquele gênero no cardápio passa a ser a nova

  Cenário: RN-17 — alterar sem a quantidade
    Dado que o gênero está no cardápio e deixei a quantidade zerada
    Quando marco a linha para alterar e confirmo
    Então vejo "* Informe a quantidade *"
    E o cursor volta à quantidade da linha
    E nada é gravado

  Cenário: RN-17 — retirar um gênero do cardápio
    Dado que consultei o cardápio, que o gênero está nele e que ainda restam outros gêneros
    Quando marco a linha para excluir e confirmo
    Então o gênero sai do cardápio daquele segmento e daquela validade

  Cenário: RN-17 — gênero que não está no cardápio
    Dado que a subclasse e o gênero informados não estão neste cardápio
    Quando marco a linha para excluir e confirmo
    Então vejo "* Genero nao cadastrado neste cardapio *"
    E o cursor volta à subclasse da linha
    E nada é apagado

  Cenário: RN-18 — consultar o cardápio
    Dado que informo a consulta com o código do cardápio, o segmento e a data limite
    Quando confirmo
    Então a tela mostra o cardápio com a grade de gêneros
    E nada é gravado: nenhum gênero é criado, alterado ou apagado e nenhum registro de auditoria é deixado

  Cenário: RN-18 — consulta sem o código do cardápio
    Quando confirmo a consulta com o código do cardápio em branco
    Então vejo "* Informe o codigo do cardapio *"
    E o cursor volta ao campo do código do cardápio
    E nada é gravado

  Cenário: RN-18 — consulta sem a data limite
    Quando confirmo a consulta com a data limite em branco
    Então vejo "* Informe a data limite de validade *"
    E o cursor volta ao campo do dia limite
    E nada é gravado

  Cenário: RN-18 — cardápio não cadastrado naquela validade
    Dado que não existe cardápio com aquele código naquela validade
    Quando confirmo a consulta
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor volta ao campo do código do cardápio
    E nada é gravado

  Cenário: RN-18 — cardápio sem gênero naquele segmento
    Dado que o cardápio existe, mas não tem gênero naquele segmento
    Quando confirmo a consulta
    Então vejo "* Segmento nao cadastrado neste cardapio *"
    E o cursor volta ao campo do segmento
    E nada é gravado

  Cenário: RN-19 — o rastro da gravação
    Dado que incluí um gênero no cardápio
    Quando confirmo
    Então o sistema deixa um registro de auditoria com o tipo de órgão, o cadastro que mudou, o registro antes e o depois, a operação, a matrícula, o código de acesso, a estação, a data e a hora
    E o código da tela que provocou a mudança vai nesse registro

  Cenário: RN-20 — a passagem para as refeições
    Dado que consultei um cardápio e que a marca de passagem para as refeições está posta
    Quando confirmo
    Então a transação passa para a tela C815T
    E ela abre em alteração com o cardápio, o segmento, as duas datas e as marcas que esta tela entregou
    E nenhuma manutenção é feita nesta confirmação

  Cenário: RN-20 — passagem com cardápio que não existe
    Dado que a marca de passagem está posta e o cardápio informado não existe naquela validade
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor volta ao campo do código do cardápio
    E nada é gravado

  Cenário: RN-21 — sem a permissão de acesso
    Dado que o meu perfil não tem esta tela
    Quando entro na tela
    Então vejo a recusa de acesso do sistema
    E nenhum cadastro é lido

  Cenário: RN-22 — campo não numérico
    Quando preencho o código do cardápio, o segmento, uma das datas, a subclasse, o gênero ou a quantidade com letra
    Então a tela recusa o campo antes de qualquer leitura de cadastro
    E o cursor volta ao campo recusado
    E nada é gravado
```
