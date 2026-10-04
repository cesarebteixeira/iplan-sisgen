# US — E049T — Período de entrega da alimentação escolar por coordenadoria regional escolar

## Estória

Como **servidor de CRE da secretaria de educação**, quero **definir e corrigir o
período de entrega da alimentação escolar da minha coordenadoria para cada data de
preparo, informando a data de início, a quantidade de dias de entrega e, quando
houver, um segundo período**, para que **as entregas caiam em dias úteis e os órgãos
da coordenadoria não fiquem com requisição marcada para um dia em que não há
entrega**.

O período de entrega de uma coordenadoria é aberto por uma data de preparo e vale uma
semana: é a partir dela que a tela distribui os dias de entrega, pulando sábados,
domingos e os feriados da secretaria. É esse calendário que as requisições dos órgãos
encontram pela frente — por isso uma data de preparo que já tem requisição de órgão não
pode ser apagada, e uma data que encoste no período de outro registro não pode ser
incluída. Quando a data de início, a quantidade de dias ou o segundo período saem
errados, as requisições daquela coordenadoria caem em dias sem entrega, e o acerto só
existe se o calendário puder ser corrigido no lugar.

Esta tela é o único lugar do sistema que cria, corrige e apaga esse calendário, uma
data de preparo por linha. Ela não pergunta confirmação antes de gravar, não avisa
depois que gravou e não grava nada quando a operação é de consulta: o que estiver na
tela quando eu mandar alterar é o que fica.

## Contexto

Jornada S000M → E000M → E050M → E049T.

Ator: servidor de CRE — informa a coordenadoria regional escolar e a data de preparo,
diz em cada período mostrado o que quer fazer com ele (incluir, alterar ou excluir),
informa as datas e as quantidades de entrega e manda alterar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. A tela é aberta por um menu, e o menu não
passa registro nem operação: a operação é escolhida na própria tela, que abre em
consulta.

Da sessão a tela usa a matrícula funcional, o código de acesso, o privilégio, a
estação, a secretaria (o tipo de órgão), a coordenadoria regional escolar do vínculo e
a data do sistema. A tela não encadeia em outra por conta própria: termina nela mesma,
e o que ela deixa é o calendário de entrega da coordenadoria gravado. Ela também não
muda de comportamento conforme a tela que a abriu.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O que esta tela mantém

Para cada coordenadoria regional escolar e cada data de preparo, a tela mantém o
período de entrega daquela semana: a data de início, as datas de entrega calculadas e
a data limite do período — e, quando houver, um segundo conjunto de datas com o mesmo
conteúdo. Mantém também o intervalo de cálculo aberto pela data de preparo, que vai
dela até seis dias depois. Os dois conjuntos são independentes: um período pode
existir sem o segundo, e o segundo pode ser trocado sem mexer no primeiro.

A quantidade de dias de entrega não fica guardada: ela é o que eu informo para a tela
calcular, e o que sobra no cadastro são as datas.

[?] A inclusão leva ao cadastro apenas os valores que a tela calculou ou que eu
informei; os campos que ficaram de fora recebem o que o cadastro atribui no momento em
que o registro é criado. O acervo lido não documenta essa inicialização, e é ela que
decide se um dia de entrega não usado fica zerado ou com sobra de outro registro.
Pergunta ao site.

### RN-02 — A tela abre em consulta e lista os períodos a partir da data do sistema

Ao ser aberta, a operação que a tela mostra é a de consulta e a coordenadoria que ela
traz é a do meu vínculo. A tela lista os períodos dessa coordenadoria a partir da data
do sistema e mostra até quatro deles por vez. Não havendo nenhum a partir dali, ela avisa
**\* Nao existem registros a partir da data inf \***. Sem coordenadoria no vínculo, a
lista não é montada.

Cada período mostrado vem com os seus valores à vista e com os campos de digitação em
branco: o que eu não redigitar não vale como informado.

[?] A descrição da secretaria e a data do sistema que a tela mostra no cabeçalho são
preenchidas na abertura e limpas a cada digitação, sem que nenhuma passagem seguinte
as reponha. Se o ambiente do quadro comum as repõe antes de mostrar a tela, o acervo
lido não mostra. Pergunta ao site.

[?] A lista é montada por uma leitura posicionada pelo ambiente, cujo efeito exato não
está no acervo lido: não se conclui dele o que a tela mostra quando não existe período
exatamente na data do sistema — se a lista começa no primeiro período posterior ou se
ela fica vazia com o aviso. Pergunta ao site.

### RN-03 — A operação é uma só para a tela; a ação, para cada período

A operação é uma só para a tela inteira: ou eu consulto, ou eu altero. Qualquer outra
coisa é recusada com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de
volta ao campo da operação, antes de o cadastro do período ser lido.

Para cada período mostrado eu digo o que quero fazer — incluir, alterar ou excluir —, e
a ação vale só para aquele período: os períodos que eu não marcar não são tocados. Sem
a operação de alteração, nenhuma ação é executada.

[?] A mensagem manda usar "ALT" ou "CON", mas a tela só deixa passar quando o campo da
operação casa com o código interno da alteração ou da consulta, e é ela mesma que
repõe a consulta a cada transação. O que "ALT" e "CON" significam para o operador, e se
existe outra forma de escolher a operação, não está no acervo lido. Pergunta ao site.

[?] A tela consulta, antes de tudo, um campo de "próxima tela": preenchido, a passagem
termina ali e a tela entrega a transação ao código informado, sem conferir nada mais.
Quem preenche esse campo — se o operador, se o ambiente — não se conclui desta tela, e
sem isso não se sabe se uma transação desta tela pode sair para outra. Pergunta ao
site.

### RN-04 — A consulta não grava nada

Na consulta a tela só mostra: ela não inclui, não altera e não apaga período nenhum, e
não gera registro de auditoria. Se eu digitar uma ação de incluir, alterar ou excluir
numa consulta, ela é ignorada, e nenhuma conferência de data é feita.

### RN-05 — Acesso à tela, à operação e ao recorte da coordenadoria

A tela só é usada se estiver cadastrada e liberada para o meu código de acesso, e a
estação tem de ser a mesma da minha sessão. A operação escolhida para cada período
também é conferida: sem a liberação de inclusão, de alteração ou de exclusão para
aquele código de acesso naquela tela, a operação correspondente não é aceita. A
consulta não pede liberação própria: quem tem a tela cadastrada consulta.

A coordenadoria informada tem de ser a da minha sessão. Ao consultar, se o meu vínculo
já traz uma coordenadoria e eu informo outra, a recusa é
**\* Usuario sem acesso a este grupo \***. Quando o meu vínculo não traz nenhuma, a
coordenadoria informada é conferida no cadastro de coordenadorias da minha secretaria
e, não pertencendo a ela, a recusa é **\* Grupo nao pertence a esta secretaria \***.
Para alterar, a coordenadoria informada tem de ser a que ficou corrente na tela; sendo
outra, a recusa é **\* Consulte antes de atualizar \***.

[?] A recusa "Consulte antes de atualizar" manda consultar a coordenadoria antes de
alterá-la, mas para quem tem coordenadoria no vínculo a consulta de outra
coordenadoria já é recusada antes, e o acervo lido não mostra se a coordenadoria
corrente sobrevive de uma transação para a outra — que é o que a mensagem pede.
Pergunta ao site.

[?] O cadastro que libera a operação tem um campo próprio para a consulta, e nenhum
ponto do caminho lido o consulta: quem tem a tela cadastrada consulta sem ele. Se a
intenção era exigir essa liberação, o caminho não a exige. Pergunta ao site.

### RN-06 — A data de preparo identifica o período

Junto com a coordenadoria, a data de preparo identifica o período. Para incluir, a
data não pode existir ainda: se já existir, a recusa é
**\* Data de preparo ja cadastrada \***. Para alterar ou excluir, ela tem de existir:
se não existir, a recusa é **\* Data de preparo nao cadastrada \***. A data tem de ser
um dia válido de 1994 a 2099; fora disso, a recusa é
**\* Data de inicio de calculo invalida \***.

[?] O cadastro admite mais de um registro com a mesma coordenadoria e a mesma data de
preparo, e a decisão de que o período existe não compara a data lida com a digitada: a
inclusão, a alteração e a exclusão só olham se a leitura achou algum registro, e a
leitura é posicionada pelo ambiente, cujo efeito exato não está no acervo lido. Se ela
puder devolver um registro de outra data, a inclusão recusa uma data livre e a alteração
mexe no registro errado; o acervo não decide. Pergunta ao site.

### RN-07 — O intervalo aberto por uma data de preparo

O período aberto por uma data de preparo vai dela até seis dias depois, e é esse
intervalo que a data nova não pode invadir. Incluir uma data de preparo que caia dentro
do intervalo aberto por outro registro da mesma coordenadoria é recusado com
**\* <- Ja existe requisicao neste intervalo \***, mostrando a data que está no meio do
caminho.

[?] A conferência procura o registro imediatamente anterior pela data e o
imediatamente seguinte, e para em cada um deles; um período mais antigo, que comece
antes e ainda alcance a data nova, pode escapar. O acervo lido não permite afirmar que
essa procura alcança todos os vizinhos. Pergunta ao site.

### RN-08 — A data de preparo cai no dia da semana configurado para a secretaria

Cada secretaria tem, no seu cadastro de parâmetros, o dia da semana em que o preparo
começa. Se a data de preparo informada não cair nesse dia, a recusa mostra o dia
exigido: **\* Inicio de preparo deve ser \<dia\> \***, com o cursor na data de preparo.
Quando o cadastro da secretaria não tem o dia configurado, essa conferência não é
feita.

[?] O dia é guardado por extenso no cadastro de parâmetros da secretaria; o acervo lido
não mostra os valores gravados nem de onde eles vêm, e não diz se todas as secretarias
têm esse dia preenchido — sem ele, a conferência simplesmente não acontece. Pergunta ao
site.

### RN-09 — A data de início da entrega

A data de início do período tem de ser um dia que exista no calendário: impossível, ou
em branco, a recusa é **\* Data de inicio da entrega invalida \***, com o cursor no
início do período.

O início não pode ser posterior à data de preparo: informado depois dela, a recusa é
**\* Data de entrega maior que data do preparo \***, com o cursor no início.

O início também não pode cair em dia sem entrega: sábado dá
**\* Inicio da entrega nao deve ser um sabado \***, domingo dá
**\* Inicio da entrega nao deve ser um domingo \***, e um feriado da secretaria dá
**\* Inicio da entrega nao deve ser um feriado \*** — sempre com o cursor no início do
período.

[?] A tela traz ainda uma recusa por "diferença entre o preparo e a entrega maior que
7 dias", que mede a distância entre as duas datas no sentido entrega menos preparo. Como
a conferência imediatamente anterior já recusa a entrega posterior ao preparo, essa
distância nunca pode passar de sete, e a recusa não tem como aparecer por esse caminho.
Ou a primeira conferência está invertida, ou a segunda mede a diferença no sentido
errado; e a rotina comum que calcula a distância entre duas datas não faz parte do
acervo lido, de modo que também não se sabe o que ela devolve quando as duas datas caem
em anos diferentes. Não escolho um dos dois lados. Pergunta ao site.

### RN-10 — Da quantidade de dias saem as datas de entrega

A quantidade de dias de entrega vai de um a cinco. Em branco, a recusa é
**\* Informe a quantidade de dias de entrega \***; acima de cinco, a recusa é
**\* Quantidade maxima de dias de entrega = 5 \***, com o cursor na quantidade.

É dessa quantidade que saem as datas de entrega: a tela parte do início informado e
anda para a frente, pulando sábados, domingos e feriados da secretaria, até completar a
quantidade pedida. A primeira data é o próprio início e a última vira o limite do
período.

[?] Os campos de limite do período são de saída: o que eu digitar neles é substituído
pelo que a tela calculou, e o valor calculado é o que vai para o cadastro. O acervo
lido não diz se a tela deveria recusar a digitação nesses campos em vez de
sobrescrevê-la. Pergunta ao site.

### RN-11 — O período inteiro tem de caber na permissão de entrega da coordenadoria

O período, do início ao limite calculado, tem de caber em uma permissão de entrega
vigente da coordenadoria. Não havendo nenhuma permissão que o contenha, a recusa é
**\* Data de entrega fora do limite da permissao \***, com o cursor no início do
período.

[?] A procura da permissão é posicionada pela data de limite do período e anda a partir
dali, pelas permissões da coordenadoria. Sem o manual do banco, o acervo lido não
permite afirmar que essa caminhada alcança todas as permissões com limite igual ou
posterior — em especial as que tiverem contrato, classe, subclasse ou gênero
preenchidos, que também fazem parte da chave da procura. Pergunta ao site.

### RN-12 — O segundo período tem o mesmo tratamento

Além do período da semana, a tela guarda um segundo conjunto de datas. Ele passa pelas
mesmas conferências do período regular: início que exista no calendário, não posterior
à data de preparo, fora de sábado, domingo e feriado, quantidade de dias até cinco — e
o conjunto inteiro também tem de caber na permissão de entrega da coordenadoria.

Informar a data de início do segundo período sem a quantidade de dias é recusado com
**\* Informe dias de entrega. Maximo = 5 \***, com o cursor na quantidade. Deixar o
início do segundo período em branco apaga o segundo período do cadastro: ele não fica
como estava.

[?] Este segundo conjunto de datas não tem rótulo de negócio no acervo lido — nem no
programa, nem no cadastro, onde os campos só se distinguem por um sufixo. O que ele
representa na entrega da alimentação escolar não está no corpus. Pergunta ao site.

[?] A tela mostra o segundo período, mas limpa o que eu poderia digitar nele a cada
apresentação: para conservá-lo tenho de redigitá-lo. Se a intenção era essa, ou se o
segundo período deveria continuar valendo quando eu não o toco, o acervo lido não diz.
Pergunta ao site.

[?] Quando a quantidade de dias do segundo período passa de cinco, a tela escolhe a
mensagem olhando a quantidade de dias do período regular: não havendo quantidade no
período regular, ela pede que eu informe uma quantidade que eu já informei, em vez de
avisar do limite de cinco. As duas guardas leem campos diferentes. Pergunta ao site.

### RN-13 — Na alteração, o que eu não redigitar não é recalculado

A quantidade de dias não fica guardada no cadastro: só as datas ficam. Por isso, ao
alterar o período regular, a tela só refaz o cálculo e regrava as datas se eu informar
a quantidade de dias de novo; não informando, o período que já estava fica como está —
inclusive as datas de entrega e o limite. Informando, a tela recalcula tudo e substitui
o que estava.

### RN-14 — A exclusão é recusada quando a data de preparo já foi requisitada

Não se apaga o período de uma data de preparo quando algum órgão da coordenadoria já
tem requisição para aquela data. A recusa é
**\* Ja existem orgaos com esta data de preparo \***, com o cursor na data de preparo,
e nada é apagado.

Não havendo requisição de órgão para aquela data, a exclusão apaga o período do
cadastro.

### RN-15 — O que a tela grava e o que fica registrado

Ao incluir, a tela cria o registro do período; ao alterar, regrava o registro; ao
excluir, apaga-o do cadastro. Cada uma dessas três operações deixa um registro de
auditoria com a tela de origem, o cadastro atingido, a operação, a coordenadoria, a data
de preparo, a minha matrícula, a estação, a secretaria, a data e a hora da sessão e os
valores de antes e de depois.

A tela não cria nem apaga nenhum outro cadastro — nem órgão, nem permissão de entrega,
nem feriado, nem requisição. E ela não pergunta confirmação antes de gravar nem avisa
que gravou: uma operação recusada não deixa registro de auditoria, e a tela está escrita
para que a recusa chegue antes da passagem que grava.

[?] No registro de auditoria da exclusão, o número do processo é a data de preparo do
período. A exclusão não recalcula essa data a partir do que está na tela, e o acervo
lido não mostra de onde ela viria nesse caminho: pode sair zerada ou ser a de outro
período processado na mesma passagem. Pergunta ao site.

[?] O encerramento da transação numa recusa é marcado pela rotina comum que exibe a
mensagem, e essa rotina não faz parte do acervo lido. A tela está escrita para que a
recusa chegue antes da passagem que grava, mas quem grava não reconfere as datas: sem
essa marca, uma operação recusada ainda seria gravada. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Período de entrega da alimentação escolar por coordenadoria regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar do meu
      vínculo e a data do sistema
    E tenho acesso à tela E049T

  Cenário: Incluir o período de entrega de uma data de preparo
    Dado que a data de preparo informada ainda não está cadastrada
    E que ela cai no dia da semana configurado para a minha secretaria
    E que ela não cai dentro do período aberto por outro registro da coordenadoria
    Quando informo a coordenadoria, a data de preparo, a data de início da entrega e a
      quantidade de dias de entrega
    E marco a ação de incluir
    E escolho a operação de alterar
    Então o período é criado no cadastro, com as datas de entrega e o limite calculados
    E as entregas são distribuídas a partir do início, pulando sábado, domingo e os
      feriados da minha secretaria
    E fica um registro de auditoria da inclusão

  Cenário: A tela abre em consulta e mostra os períodos da minha coordenadoria
    Dado que existe mais de um período cadastrado para a minha coordenadoria
    Quando abro a tela E049T
    Então a operação mostrada é a de consulta
    E vejo os períodos a partir da data do sistema, até quatro por vez
    E os campos de digitação vêm em branco, com os valores à mostra

  Cenário: A tela abre sem períodos a partir da data do sistema
    Dado que não existe período cadastrado para a minha coordenadoria a partir da data
      do sistema
    Quando abro a tela E049T
    Então vejo "* Nao existem registros a partir da data inf *"

  Cenário: Consultar não grava nada
    Dado que existe um período cadastrado para a coordenadoria
    Quando escolho a operação de consultar e marco uma ação de incluir, alterar ou
      excluir
    Então a tela mostra os períodos e nada mais
    E nenhuma conferência de data é feita
    E nenhum período é criado, alterado ou apagado
    E nenhum registro de auditoria é gerado

  Cenário: Operação fora da alteração e da consulta
    Quando informo uma operação diferente de alterar e de consultar
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Coordenadoria fora do meu grupo
    Dado que o meu vínculo carrega uma coordenadoria
    Quando escolho a operação de consultar e informo outra coordenadoria
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Coordenadoria que não pertence à minha secretaria
    Dado que o meu vínculo não carrega coordenadoria
    Quando escolho a operação de consultar e informo uma coordenadoria que não pertence
      à minha secretaria
    Então vejo "* Grupo nao pertence a esta secretaria *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Alterar sem ter consultado antes
    Dado que informei uma coordenadoria que não é a corrente da tela
    Quando escolho a operação de alterar
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Data de preparo já cadastrada
    Dado que já existe um período para a coordenadoria naquela data de preparo
    Quando marco a ação de incluir e escolho a operação de alterar
    Então vejo "* Data de preparo ja cadastrada *"
    E o cursor fica na data de preparo
    E nada é gravado

  Cenário: Data de preparo não cadastrada
    Quando marco a ação de alterar ou de excluir uma data de preparo que não existe
    Então vejo "* Data de preparo nao cadastrada *"
    E o cursor fica na data de preparo
    E nada é gravado

  Cenário: Data de preparo inválida
    Quando informo uma data de preparo que não existe no calendário ou um ano fora da
      faixa que o sistema aceita
    Então vejo "* Data de inicio de calculo invalida *"
    E o cursor fica na data de preparo
    E nada é gravado

  Cenário: Data de preparo dentro do período aberto por outro registro
    Dado que a data de preparo informada cai dentro do período aberto por outro
      registro da mesma coordenadoria
    Quando marco a ação de incluir e escolho a operação de alterar
    Então vejo "* <- Ja existe requisicao neste intervalo *", com a data do outro
      registro
    E o cursor fica na data de preparo
    E nada é gravado

  Cenário: Data de preparo em dia da semana não permitido
    Dado que a minha secretaria tem configurado o dia da semana do preparo
    Quando informo uma data de preparo que não cai nesse dia
    Então vejo "* Inicio de preparo deve ser <o dia configurado> *"
    E o cursor fica na data de preparo
    E nada é gravado

  Cenário: Data de início da entrega inválida
    Quando deixo a data de início da entrega em branco ou informo um dia que não existe
    Então vejo "* Data de inicio da entrega invalida *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: Início da entrega posterior à data de preparo
    Quando informo um início de entrega depois da data de preparo
    Então vejo "* Data de entrega maior que data do preparo *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: Início da entrega em dia sem entrega
    Quando informo um início que cai em sábado, domingo ou feriado da minha secretaria
    Então vejo "* Inicio da entrega nao deve ser um sabado *",
      "* Inicio da entrega nao deve ser um domingo *" ou
      "* Inicio da entrega nao deve ser um feriado *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: Quantidade de dias de entrega em branco
    Quando marco a ação de incluir e deixo a quantidade de dias de entrega em branco
    Então vejo "* Informe a quantidade de dias de entrega *"
    E o cursor fica na quantidade
    E nada é gravado

  Cenário: Quantidade de dias de entrega acima de cinco
    Quando informo mais de cinco dias de entrega
    Então vejo "* Quantidade maxima de dias de entrega = 5 *"
    E o cursor fica na quantidade
    E nada é gravado

  Cenário: Período fora da permissão de entrega da coordenadoria
    Dado que não existe permissão de entrega vigente que contenha o período informado
    Quando marco a ação de incluir ou de alterar e escolho a operação de alterar
    Então vejo "* Data de entrega fora do limite da permissao *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: Segundo período sem a quantidade de dias
    Quando informo a data de início do segundo período e deixo a quantidade de dias
      dele em branco
    Então vejo "* Informe dias de entrega. Maximo = 5 *"
    E o cursor fica na quantidade do segundo período
    E nada é gravado

  Cenário: Segundo período com início posterior à data de preparo
    Quando informo um início do segundo período depois da data de preparo
    Então vejo "* Data de entrega maior que data do preparo *"
    E o cursor fica no início do segundo período
    E nada é gravado

  Cenário: Segundo período fora da permissão de entrega
    Dado que o segundo período informado não cabe em nenhuma permissão vigente
    Quando marco a ação de incluir ou de alterar e escolho a operação de alterar
    Então vejo "* Data de entrega fora do limite da permissao *"
    E o cursor fica no início do segundo período
    E nada é gravado

  Cenário: Alterar o período informando a quantidade de dias
    Dado que existe um período cadastrado
    Quando marco a ação de alterar e informo a data de início e a quantidade de dias
    Então as datas de entrega e o limite são calculados de novo
    E o período no cadastro passa a ter as datas novas
    E fica um registro de auditoria da alteração

  Cenário: Alterar o período sem informar a quantidade de dias
    Dado que existe um período cadastrado
    Quando marco a ação de alterar, informo a data de início e deixo a quantidade de
      dias em branco
    Então as datas de entrega e o limite que já estavam cadastrados não são recalculados
    E o período continua como estava

  Cenário: O segundo período não redigitado é apagado
    Dado que existe um período com o segundo período cadastrado
    Quando marco a ação de alterar e deixo o início do segundo período em branco
    Então o segundo período é apagado do cadastro
    E o período regular continua como estava

  Cenário: Excluir um período sem requisição de órgão
    Dado que existe um período para a coordenadoria naquela data de preparo
    E que nenhum órgão da coordenadoria tem requisição para aquela data
    Quando marco a ação de excluir e escolho a operação de alterar
    Então o período é apagado do cadastro
    E fica um registro de auditoria da exclusão

  Cenário: Excluir um período já requisitado por um órgão
    Dado que um órgão da coordenadoria já tem requisição para aquela data de preparo
    Quando marco a ação de excluir e escolho a operação de alterar
    Então vejo "* Ja existem orgaos com esta data de preparo *"
    E o cursor fica na data de preparo
    E nada é apagado

  Cenário: Sem autorização para a operação
    Dado que o meu código de acesso não tem a operação escolhida liberada nesta tela
    Quando marco uma ação e escolho a operação de alterar
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: A recusa não grava nem apaga nada
    Dado que a minha operação foi recusada por alguma conferência
    Quando a tela termina a transação
    Então nenhum período foi criado, alterado ou apagado
    E nenhum registro de auditoria foi gerado
    E nenhum órgão, permissão, feriado ou requisição foi tocado
```
