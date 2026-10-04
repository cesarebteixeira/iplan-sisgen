# US — C217T — Manter a tabela de preços por data de referência

## Estória

Como **servidor de CRE**, quero **manter os preços dos gêneros de material na tabela de
uma data de referência**, para que **o preço de cada gênero esteja definido naquela data
quando o sistema for consultá-lo**.

A secretaria precisa do preço de cada gênero de material em uma data. É este cadastro que
guarda isso: uma tabela por data de referência, com uma descrição, e uma linha por gênero,
com o preço. Sem ele, a consulta de preço por data fica sem resposta. É também por aqui
que uma tabela nova nasce copiada da tabela de preços da quinzena, para o servidor ajustar
depois. A tela é de **manutenção**: lê, inclui, altera e exclui linhas, copia os preços de
uma tabela da quinzena e apaga a tabela inteira — e deixa rastro de tudo o que grava.

## Contexto

Jornada S000M → C000M → C020M → C217T.

Ator: servidor de CRE — informa a data de referência, vê as linhas daquela tabela e inclui,
altera ou exclui o preço de cada gênero.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O `C000M` e o `C020M` são menus: só encaminham e não deixam dado de negócio para esta tela.
O que a C217T usa da sessão — a matrícula, o tipo de órgão, a CRE, a estação e a data do
sistema — é o que a entrada deixou; a tela não recalcula nada disso. A consulta do mesmo
cadastro é a tela irmã **C217C**, que lista as tabelas já cadastradas e, quando o servidor
pede o detalhe de uma delas, encaminha para cá já naquela tabela e em consulta.

O que a tela mantém é a **tabela de preços de uma data de referência**: para a data e para um
gênero de material (classe, subclasse e gênero), ela guarda **um preço**, além da descrição
da tabela, de quem a atualizou e de quando. O cadastro dos gêneros de material é outro
(mantido pela tela C050T): é dele que saem a descrição resumida e a unidade de medida que a
tela mostra, e é ele que diz se o gênero está ativo. Os preços que a cópia traz vêm da
**tabela de preços da quinzena**. A base comporta **1.500 linhas**: a capacidade é o máximo
esperado declarado no dicionário de dados — parâmetro de dimensionamento, não o volume
cadastrado. As linhas desta tabela nascem por aqui e também por uma **carga por arquivo**,
que as cria sem preencher a descrição da tabela.

Esta é a última tela da jornada: ela não encadeia com nenhuma outra e não entrega a
transação adiante.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O que a tela mantém

A tela mantém a **tabela de preços de uma data de referência**. No cabeçalho vêm a **data de
referência** (dia, mês e ano), a **descrição da tabela**, a **data de início de uma tabela de
preços da quinzena a copiar**, a **marca de exclusão da tabela inteira** e o **modo de uso**.
A área de linhas é uma grade de **doze linhas**, cada uma com **classe, subclasse, gênero,
descrição resumida do gênero, unidade de medida, preço e ação**; a tela lista as linhas da
tabela na ordem da classificação — classe, subclasse e gênero —, doze por vez. A descrição
resumida e a unidade de medida do gênero são preenchidas pelo sistema a partir do cadastro
de gêneros: não se digitam. No rodapé do cabeçalho a tela ainda mostra a **descrição do tipo
de órgão** do servidor e a **data do sistema**.

Das bases que a tela enxerga — a tabela de preços, o cadastro de gêneros de material, a
tabela de preços da quinzena, o cadastro das telas e a trilha de auditoria — só **duas**
recebem escrita: a **tabela de preços** (inclusão, alteração, exclusão, cópia e troca da
descrição) e a **trilha de auditoria**. O cadastro de gêneros e a tabela da quinzena são
aqui **somente lidos**.

[?] A descrição do tipo de órgão e a data do sistema são copiadas para a tela de uma área
que nenhum dos programas do acervo preenche: os únicos destinos desses dois dados, em todos
os programas lidos, são as duas linhas que os apagam na abertura do sistema. Se o ambiente
não os transportar de fora para dentro, os dois saem em branco. Pergunta ao site.

[?] O preço aparece na tela com o rótulo **PRECO 2001** e o acervo não diz o que o rótulo
designa, nem por que o ano está nele. Pergunta ao site. A mesma dúvida está nas telas irmãs
que mostram esse mesmo preço.

[?] O que a leitura faz ao virar a página — se continua na linha seguinte à última mostrada,
se repete a página ou se termina — não se conclui do acervo: os sinalizadores que a leitura
dos registros usa não estão no corpus nem no manual. Os três comportamentos são compatíveis
com o que o fonte mostra. Pergunta ao site.

### RN-02 — A tela tem dois modos, e qualquer outro é recusado

O **modo de uso** admite **consulta** e **alteração**. Qualquer outro valor é recusado com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta no campo do modo, e
nada é lido nem gravado. O modo é conferido antes de qualquer tratamento de linha.

A tela se apresenta no modo e na tabela que a sessão deixou: se a sessão ainda guarda o modo
da última vez e a última tabela consultada, é com eles que ela abre; sem nada guardado, ela
abre em **consulta**, com a data de referência em branco. É assim que a consulta irmã a
entrega: a C217C encaminha a tabela escolhida e o modo consulta.

[?] A recusa manda usar **ALT** ou **CON** e a conferência compara o campo com os códigos
internos de consulta e de alteração do sistema; nenhum fonte do lote mostra quem traduz o
que o operador digita. A mesma dúvida está registrada nas telas irmãs. Pergunta ao site.

### RN-03 — No modo consulta nada é gravado

Com o modo em **consulta**, o tratamento da linha é abandonado antes de qualquer teste de
ação e a passagem que grava não faz nada: é a garantia de que a consulta é somente leitura.
Quem quer incluir, alterar, excluir, copiar ou apagar a tabela precisa estar no modo de
alteração.

### RN-04 — Os campos informados passam pela conferência de numérico

**Dez** campos passam pela conferência de numérico antes de a leitura que os usa acontecer:
o dia, o mês e o ano da **data de referência**; o dia, o mês e o ano da **data de cópia**; a
classe, a subclasse e o gênero da linha; e o **preço**. Campo em branco vira zero e os zeros
à esquerda são descartados; o que não for número é recusado, com o cursor de volta no próprio
campo, e nada é gravado. O preço é conferido com duas casas decimais.

[?] O que o servidor vê quando um valor não numérico é recusado não está no programa: a
conferência é chamada de uma rotina de biblioteca cujo corpo não veio no lote. Pergunta ao
site.

[?] A conferência está amarrada ao tipo da mensagem que chega, e o que distingue uma mensagem
de operador de uma mensagem automática não está explicado no acervo nem no manual. Se existe
um caminho de entrada em que ela não roda, não foi possível determinar. Pergunta ao site.

### RN-05 — A data de referência identifica a tabela e tem de ser uma data que existe

A **data de referência** identifica a tabela. Na **consulta**, uma data diferente da última
consultada é conferida: o **ano** tem de estar entre **1994** e **2099** e o **dia** tem de
existir naquele mês e ano. Não existindo, a recusa é **\* Data de referencia invalida \***,
com o cursor no dia da data de referência, e nada é gravado. Passando, o sistema guarda
aquela data como a tabela consultada e traz a descrição da tabela do cadastro.

[?] O programa limita o ano de 1994 a 2099 e o acervo não diz de onde vêm esses limites.
Pergunta ao site.

[?] A conferência da data só é executada na consulta: na alteração a data não é reconferida,
porque esse caminho só aceita a data que já foi consultada (RN-07). Se a alteração deveria
reconferir a data que recebe, pergunta ao site.

### RN-06 — Sem linhas na data, a consulta avisa

Sem nenhuma linha para a data de referência na posição em que a lista começa, a tela não
mostra linha e avisa **\* Tabela sem generos cadastrados \***; o aviso aparece uma vez, na
primeira linha da página, e nada mais é feito.

[?] A mesma marca de "não encontrei" serve a dois casos — a data sem tabela nenhuma e a lista
que chegou ao fim das linhas daquele período — e por isso não se sabe se o aviso distingue
"não há tabela para esta data" de "acabaram as linhas desta tabela". Pergunta ao site.

### RN-07 — Para alterar é preciso ter consultado a tabela daquela data

No modo de **alteração**, a data de referência informada tem de ser a mesma que a consulta
deixou guardada na sessão. Se não for, o sistema recusa com
**\* Consulte a tabela antes da atualizacao \***, com o cursor no campo do modo, e nada é
lido nem gravado. É a regra de **consultar antes de atualizar** — e é também por ela que uma
tabela que ainda não existe começa: a consulta mostra a data sem linhas e a data fica
guardada como a tabela consultada, de modo que a alteração seguinte pode incluir as primeiras
linhas.

### RN-08 — A descrição da tabela é obrigatória e vale para a tabela inteira

A **descrição da tabela** tem de estar preenchida em toda mensagem de alteração — inclusive
na cópia e na exclusão da tabela: em branco, a recusa é **\* Informe a descricao da tabela \***,
com o cursor no campo, e nada é gravado. A descrição é **uma só para a tabela**: quando é
trocada, o sistema percorre a tabela e repassa o texto novo a cada linha que ainda não o tem,
renovando a data e a matrícula da atualização e deixando o rastro de cada troca.

### RN-09 — A cópia traz os preços de uma tabela da quinzena para uma tabela nova

Informada a **data de início de uma tabela de preços da quinzena**, o sistema copia para a
tabela em manutenção o **preço de cada gênero** daquela tabela, uma linha por gênero, com a
data de referência e a descrição informadas. A cópia só acontece para uma **tabela que ainda
não tem linha nenhuma**: se a tabela da data de referência já tem linha, a recusa é
**\* Ja existem registros cadastrados nesta tabela \***, com o cursor na data de cópia; e se
não existe tabela de preços da quinzena na data de cópia, a recusa é
**\* Tabela para copia nao cadastrada \***, também com o cursor na data de cópia.

[?] Na cópia o cadastro de gêneros **não** é conferido: entram os gêneros que a tabela da
quinzena tiver, ainda que já não estejam ativos no cadastro — ao contrário da inclusão à mão,
que exige gênero ativo (RN-12). Se a cópia deveria trazer só gêneros ativos, pergunta ao
site.

### RN-10 — A marca de exclusão apaga a tabela inteira

Com a **marca de exclusão da tabela** preenchida, o sistema apaga todas as linhas da data de
referência informada; cada linha apagada deixa o seu rastro. Se a tabela não tem linha
nenhuma, a recusa é **\* Nao existem registros cadastrados nesta tabela \***, com o cursor na
marca, e nada é apagado.

[?] A tela reconhece um único valor para a marca de exclusão e o acervo não diz o que
significam os outros valores, nem qual é o rótulo do campo na tela. Pergunta ao site.

### RN-11 — A linha só é tratada quando traz a subclasse e uma ação conhecida

Uma linha só é processada quando a **ação** é `I` (inclusão), `A` (alteração) ou `E`
(exclusão); ação em branco ou ação que a tela não reconhece simplesmente passa: nada é
recusado e nada é gravado para essa linha. A conferência de permissão da operação só acontece
depois que a ação foi reconhecida. E uma linha sem **subclasse** é ignorada, sem conferência
nenhuma.

[?] A conferência da linha começa abandonando qualquer linha sem subclasse, mas a passagem que
grava abandona a linha apenas quando a **subclasse e o gênero** estão ambos em branco. Uma
linha com a subclasse em branco e o gênero preenchido não passa, portanto, por conferência
nenhuma — nem a do gênero, nem a do preço, nem a da repetição — e ainda assim chega à
gravação: pode entrar uma linha com a subclasse zerada. Ou a conferência deveria cobrir esse
caso, ou a gravação deveria ignorá-lo. Pergunta ao site.

### RN-12 — A inclusão exige gênero cadastrado e ativo, fora da tabela, e o preço

Ao incluir, o sistema confere o cadastro de gêneros de material: o gênero — subclasse e
gênero — tem de estar cadastrado e com uma **versão ativa**, e a classe informada tem de ser
a classe daquele gênero. Faltando qualquer das duas coisas, a recusa é
**\* Genero nao cadastrado \***, com o cursor na classe, e nada é gravado. Em seguida confere
se o gênero já está na tabela daquela data; estando, a recusa é
**\* Genero ja cadastrado nesta tabela \***, com o cursor na classe, e o preço que já estava
gravado não é tocado. Por fim, o **preço** é obrigatório: em branco, a recusa é
**\* Informe o preco do genero \***, com o cursor no preço, e nada é gravado.

[?] A mesma mensagem serve a três situações distintas — gênero inexistente, gênero sem versão
ativa e classe que não é a do gênero — e o operador não fica sabendo qual foi. Pergunta ao
site.

[?] A leitura do cadastro de gêneros leva a **data de referência da tabela** para o campo de
início de vigência da versão, e o que os sinalizadores da leitura fazem não está no corpus nem
no manual: não se conclui se ela exige também uma versão começando exatamente naquela data (e
a inclusão só passaria quando as duas datas coincidissem) ou se a data é ignorada e basta
existir versão ativa do gênero. Pergunta ao site.

### RN-13 — A inclusão grava a linha com a data de referência e a marca de quem atualizou

Passadas as conferências, a inclusão grava a linha com a classe, a subclasse e o gênero
informados, o preço, a **data de referência** da tabela, a descrição em vigor, a **data e a
matrícula de quem operou** e a marca de registro atualizado — a mesma marca que uma linha
copiada da tabela da quinzena recebe.

### RN-14 — A alteração exige a linha na tabela e o preço, e grava os novos valores

A alteração exige o gênero na tabela daquela data — senão
**\* Genero nao cadastrado nesta tabela \***, com o cursor na classe, e nada é gravado — e o
**preço** preenchido — senão **\* Informe o preco do genero \***, com o cursor no preço.
Confirmada, a alteração grava o novo preço na linha; a data de referência e a descrição
continuam as mesmas, e a data e a matrícula da atualização são renovadas. A linha como estava
e como ficou vai para o rastro.

### RN-15 — A exclusão apaga a linha da tabela

A exclusão exige o gênero na tabela daquela data; senão
**\* Genero nao cadastrado nesta tabela \***, com o cursor na classe, e nada é apagado.
Existindo, a linha é **apagada**: o registro deixa a tabela e com ele o preço e a descrição
daquela linha. Não é uma marca de exclusão: aqui o registro desaparece, e o valor que havia
fica no rastro.

### RN-16 — Toda operação confirmada deixa rastro na auditoria

Cada operação confirmada grava um registro na **trilha de auditoria** com o objeto (a tabela
de preços), a operação (inclusão, alteração ou exclusão), o **valor anterior** e o
**posterior** e o contexto da sessão — a matrícula, o tipo de órgão, o terminal, a data e a
hora e o número do processo. Na inclusão o valor anterior vai em branco; na alteração vão a
linha como estava e como ficou; na exclusão vai a linha como estava e o posterior em branco.
A cópia da tabela, a exclusão da tabela inteira e a troca da descrição também deixam os seus
rastros.

[?] Na inclusão de uma linha e na cópia o rastro fica sob uma condição interna que nenhum
ponto do acervo produz; se esse estado aparecer, essas duas operações gravam sem rastro,
enquanto a alteração, a exclusão e a troca da descrição sempre deixam o seu. Pergunta ao
site.

### RN-17 — A tela de destino preenchida abandona a manutenção

Se a mensagem chega com o código da **próxima tela** preenchido, a manutenção é abandonada
antes de qualquer teste de linha, nada é gravado e a sessão é encaminhada para a tela
indicada.

[?] O que preenche o código da próxima tela nesta tela não está no acervo: nenhuma linha do
programa o atribui. A consulta irmã encaminha para cá por outro mecanismo, e não por esse
campo. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manter a tabela de preços por data de referência

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C217T

  Cenário: RN-01 e RN-03 — consultar a tabela de uma data de referência
    Dado que estou na tela C217T no modo consulta
    E informo a data de referência de uma tabela que tem linhas
    Quando percorro a página
    Então vejo a descrição da tabela
    E vejo, em cada linha, a classe, a subclasse, o gênero, a descrição resumida, a unidade de medida, o preço e a ação
    E vejo no máximo doze linhas por página
    E nada é gravado

  Cenário: RN-02 — modo de uso não disponível
    Dado que estou na tela C217T
    Quando informo um modo de uso diferente de consulta e de alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é lido e nada é gravado

  Cenário: RN-02 — reabrir a tela volta ao modo e à tabela da sessão
    Dado que consultei uma tabela na tela C217T
    Quando abro a tela C217T novamente na mesma sessão
    Então ela se apresenta no modo da última vez
    E com a data de referência da última tabela consultada

  Cenário: RN-04 — valor não numérico em um campo informado
    Dado que estou na tela C217T
    Quando informo um valor não numérico em um dos campos da data, da linha ou do preço
    Então a mensagem é recusada
    E o cursor volta ao campo recusado
    E nada é gravado

  Cenário: RN-05 — data de referência que não existe
    Dado que estou na tela C217T no modo consulta
    Quando informo uma data de referência que não existe no calendário
    Então vejo a mensagem "* Data de referencia invalida *"
    E o cursor volta ao dia da data de referência
    E nada é gravado

  Cenário: RN-06 — data de referência sem linhas
    Dado que estou na tela C217T no modo consulta
    E não há linha nenhuma na posição de início daquela data
    Quando a página é apresentada
    Então vejo a mensagem "* Tabela sem generos cadastrados *"
    E a página não mostra linha alguma

  Cenário: RN-07 — alterar sem ter consultado aquela data
    Dado que estou na tela C217T no modo alteração
    E informo uma data de referência diferente da que consultei
    Quando confirmo a mensagem
    Então vejo a mensagem "* Consulte a tabela antes da atualizacao *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-08 — descrição da tabela em branco
    Dado que estou na tela C217T no modo alteração
    E consultei a tabela daquela data
    Quando confirmo a mensagem com a descrição da tabela em branco
    Então vejo a mensagem "* Informe a descricao da tabela *"
    E o cursor fica no campo da descrição
    E nada é gravado

  Cenário: RN-08 — trocar a descrição da tabela
    Dado que estou na tela C217T no modo alteração
    E consultei a tabela daquela data
    Quando informo uma nova descrição da tabela e confirmo
    Então todas as linhas daquela tabela passam a ter a nova descrição
    E cada linha que mudou fica registrada na auditoria

  Cenário: RN-09 — copiar os preços de uma tabela da quinzena
    Dado que estou na tela C217T no modo alteração
    E consultei uma data de referência que ainda não tem linhas
    E existe uma tabela de preços da quinzena na data de cópia que informei
    Quando confirmo a cópia
    Então nasce uma linha na tabela daquela data para cada gênero da tabela da quinzena
    E cada linha fica com o preço que estava na tabela da quinzena
    E cada linha fica registrada na auditoria

  Cenário: RN-09 — copiar para uma tabela que já tem linhas
    Dado que estou na tela C217T no modo alteração
    E a data de referência informada já tem linhas na tabela
    Quando confirmo a cópia
    Então vejo a mensagem "* Ja existem registros cadastrados nesta tabela *"
    E o cursor fica na data de cópia
    E nada é copiado

  Cenário: RN-09 — copiar de uma data sem tabela da quinzena
    Dado que estou na tela C217T no modo alteração
    E não existe tabela de preços da quinzena na data de cópia que informei
    Quando confirmo a cópia
    Então vejo a mensagem "* Tabela para copia nao cadastrada *"
    E o cursor fica na data de cópia
    E nada é copiado

  Cenário: RN-10 — apagar a tabela inteira
    Dado que estou na tela C217T no modo alteração
    E a tabela daquela data tem linhas
    Quando marco a exclusão da tabela e confirmo
    Então todas as linhas daquela tabela são apagadas
    E cada linha apagada fica registrada na auditoria

  Cenário: RN-10 — apagar a tabela sem linhas
    Dado que estou na tela C217T no modo alteração
    E a tabela daquela data não tem linha nenhuma
    Quando marco a exclusão da tabela e confirmo
    Então vejo a mensagem "* Nao existem registros cadastrados nesta tabela *"
    E o cursor fica na marca de exclusão
    E nada é apagado

  Cenário: RN-11 — linha com ação em branco ou desconhecida
    Dado que estou na tela C217T no modo alteração
    Quando preencho a linha com uma ação diferente de I, A e E
    Então aquela linha não é conferida
    E nada é gravado para ela
    E nenhuma mensagem é mostrada

  Cenário: RN-11 — linha sem a subclasse
    Dado que estou na tela C217T no modo alteração
    Quando deixo a subclasse em branco
    Então a linha não passa por nenhuma conferência
    E nenhuma mensagem é mostrada

  Cenário: RN-12 — incluir um gênero não cadastrado ou sem versão ativa
    Dado que estou na tela C217T no modo alteração
    Quando tento incluir um gênero que não está cadastrado, que não tem versão ativa, ou cuja classe não é a do cadastro
    Então vejo a mensagem "* Genero nao cadastrado *"
    E o cursor fica na classe
    E nada é gravado

  Cenário: RN-12 — incluir um gênero que já está na tabela
    Dado que estou na tela C217T no modo alteração
    E o gênero já está na tabela daquela data
    Quando confirmo a inclusão desse gênero
    Então vejo a mensagem "* Genero ja cadastrado nesta tabela *"
    E o cursor fica na classe
    E o preço que já estava gravado não é alterado

  Cenário: RN-12 — incluir sem o preço
    Dado que estou na tela C217T no modo alteração
    E o gênero está cadastrado, com versão ativa, e ainda não está na tabela daquela data
    Quando confirmo a inclusão sem informar o preço
    Então vejo a mensagem "* Informe o preco do genero *"
    E o cursor fica no preço
    E nada é gravado

  Cenário: RN-13 — incluir um gênero na tabela da data
    Dado que estou na tela C217T no modo alteração
    E o gênero está cadastrado, com versão ativa, e ainda não está na tabela daquela data
    Quando informo o preço e confirmo a ação I
    Então a linha é gravada na tabela daquela data de referência
    E a linha fica com a data e a matrícula de quem operou
    E a inclusão fica registrada na auditoria

  Cenário: RN-14 — alterar um gênero fora da tabela da data
    Dado que estou na tela C217T no modo alteração
    Quando confirmo a ação A para um gênero que não está na tabela daquela data
    Então vejo a mensagem "* Genero nao cadastrado nesta tabela *"
    E o cursor fica na classe
    E nada é gravado

  Cenário: RN-14 — alterar sem o preço
    Dado que estou na tela C217T no modo alteração
    E o gênero está na tabela daquela data
    Quando confirmo a ação A sem informar o preço
    Então vejo a mensagem "* Informe o preco do genero *"
    E o cursor fica no preço
    E nada é gravado

  Cenário: RN-14 — alterar o preço de um gênero da tabela
    Dado que estou na tela C217T no modo alteração
    E o gênero está na tabela daquela data
    Quando informo o novo preço e confirmo a ação A
    Então o novo preço fica gravado na linha daquela data
    E a data de referência e a descrição continuam as mesmas
    E a data e a matrícula da atualização são renovadas
    E a linha como estava antes e como ficou fica registrada na auditoria

  Cenário: RN-15 — excluir um gênero da tabela da data
    Dado que estou na tela C217T no modo alteração
    E o gênero está na tabela daquela data
    Quando confirmo a ação E
    Então o registro é apagado da tabela daquela data
    E o gênero deixa de aparecer na consulta daquela data
    E o valor que havia fica registrado na auditoria

  Cenário: RN-15 — excluir um gênero fora da tabela da data
    Dado que estou na tela C217T no modo alteração
    E o gênero não está na tabela daquela data
    Quando confirmo a ação E
    Então vejo a mensagem "* Genero nao cadastrado nesta tabela *"
    E o cursor fica na classe
    E nada é apagado

  Cenário: RN-16 — toda operação confirmada deixa rastro na auditoria
    Dado que confirmei uma inclusão, uma alteração ou uma exclusão na C217T
    Quando a gravação termina
    Então existe um registro de auditoria da tabela de preços
    E com a operação e com o valor anterior e o posterior
    E com a matrícula, o tipo de órgão, o terminal, a data e a hora e o número do processo

  Cenário: RN-17 — a próxima tela preenchida abandona a manutenção
    Dado que a mensagem chega à C217T com o código da próxima tela preenchido
    Quando a manutenção começaria
    Então a linha não é conferida e nada é gravado
    E a sessão é encaminhada para a tela indicada
```
