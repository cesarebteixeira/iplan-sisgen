# US — C219T — Manter os preços da tabela especial da quinzena

## Estória

Como **servidor de CRE**, quero **manter os preços dos gêneros de material na tabela
especial da quinzena**, para que **cada gênero tenha, naquele período, os seus preços
definidos antes de a regional usar essa tabela**.

A secretaria trabalha com duas tabelas de preços por quinzena: a de referência e a
especial. Quando a permissão de contrato aponta a quinzena como especial, é esta tabela
que responde pelo preço de cada gênero — e é o **preço corrente** dela que a transação
dos gêneros das permissões de contrato leva para o gênero da regional. Sem esse preço,
aquela transação recusa o gênero com **\* Genero sem preco na tabela especial \*** e a
regional fica sem o que licitar, comprar e pedir naquele período. É uma manutenção: além
de listar os gêneros do período, a tela inclui, altera e exclui esses preços — e recusa
incluir o mesmo gênero duas vezes na mesma quinzena.

## Contexto

Jornada S000M → C000M → C015M → C219T.
Ator: servidor de CRE — informa o início da quinzena, vê os gêneros da tabela especial
daquele período e inclui, altera ou exclui o preço de cada um.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os dois passos antes do destino são **menus**: eles encaminham a sessão e não deixam
período, ação nem modo para esta tela. O contexto de que a C219T se serve — a matrícula,
o código de acesso, o privilégio, o tipo de órgão, a CRE e a estação — é o que a entrada
deixou na sessão; a tela não o recalcula. A consulta da mesma tabela é a tela irmã
`C219C`, que também encaminha para cá.

O que a tela mantém é a **tabela especial de preços da quinzena**. Para o início de uma
quinzena e para um gênero de material — classe, subclasse e gênero —, ela guarda o
**limite de vigência** do período e **três preços**: o preço unitário de atacado, o
preço do gênero no varejo e o preço corrente. Guarda também a **variação** calculada
entre os dois primeiros, a data e a matrícula de quem atualizou e a marca de publicação
na internet. O cadastro dos gêneros de material é outro, e é dele que saem a descrição
resumida e a unidade de medida que a tela mostra. A tabela comporta **10.000**
registros: a capacidade é o máximo esperado declarado no dicionário de dados — parâmetro
de dimensionamento, não o volume cadastrado. Os preços desta tabela chegam por **dois
caminhos**: a **importação da quinzena especial**, disparada quando a atualização da
quinzena é do tipo especial, e a manutenção à mão, que é esta tela. A tela não encadeia
para outra: a jornada termina nela.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — O que a tela mantém e o que ela mostra

A tela mantém a **tabela especial de preços da quinzena**. O cabeçalho traz a **data do
sistema**, a **descrição do tipo de órgão** da sessão e o **limite de vigência** do
período; a área de linhas é uma grade de **treze linhas**, e cada linha tem a classe, a
subclasse, o gênero, a **descrição resumida** e a **unidade de medida** do gênero, os
**três preços** e a **ação** da linha. O sistema lista os gêneros daquela quinzena na
ordem da classificação de material — classe, subclasse e gênero —, treze por vez.

É uma tela de **manutenção**, não de consulta: além de ler, ela **grava** — inclui,
altera e exclui linhas. É a **única tela** que mexe nesta tabela à mão: nenhum outro
programa do lote executa gravação ou exclusão nela, embora **oito** outros a leiam (a
consulta `C219C` e os programas que usam o preço).

[?] A tela não nomeia a tabela que mantém: o nome "tabela especial" vem de fora — é
assim que a transação dos gêneros das permissões de contrato a chama ao recusar o gênero
sem preço. O acervo não diz, em termos de negócio, o que distingue esta tabela da de
referência da mesma quinzena, além do tipo de tabela que a permissão guarda. Pergunta ao
site.

### RN-02 — A quinzena é identificada pelo início, e o limite é calculado pelo sistema

O dia, o mês e o ano do início identificam a quinzena. Como a quinzena é a metade do
mês, o dia tem de ser **1** ou **16**: qualquer outro dia é recusado com
**\* Dia de inicio deve ser 01 ou 16 \***, com o cursor de volta no dia do início, e
nada é gravado. Informado o dia **1**, o limite é o dia **15** do mesmo mês e ano;
informado o dia **16**, o limite é o **último dia daquele mês** — 28, 29, 30 ou 31,
conforme o mês e o ano. O limite é do sistema: o que aparecer no campo é o que ele
calculou, e é esse limite que fica gravado na linha.

[?] A conferência do dia 1 ou 16 e o cálculo do limite só são executados na **inclusão**.
Na alteração e na exclusão o período não passa por essa conferência: o sistema procura a
linha pelo que foi informado e, não achando, recusa pela regra do gênero que não está na
tabela (RN-12 e RN-14). Se as três operações deveriam conferir o período, pergunta ao
site.

### RN-03 — O início tem de ser uma data que existe

A data de início é conferida como data: o ano tem de estar entre **1994** e **2099** e o
dia tem de existir naquele mês e ano. Não existindo, a recusa é **\* Data invalida \***,
com o cursor no dia do início, e nada é gravado.

[?] O programa limita o ano de 1994 a 2099 e o acervo não diz de onde vêm esses limites.
Pergunta ao site.

### RN-04 — Os campos informados passam pela conferência numérica

**Nove** campos passam pela conferência de numérico — o dia, o mês e o ano do início, a
classe, a subclasse, o gênero e os três preços — e o campo recusado devolve o cursor a si
mesmo; nada é gravado. Os três preços são conferidos com duas casas decimais.

[?] O texto que o operador vê quando um valor não numérico é recusado não está no
programa: a conferência é chamada de uma rotina de biblioteca cujo corpo não veio no
lote. Pergunta ao site.

### RN-05 — O modo da página decide se a tela grava, e ele chega na mensagem

A página tem um **modo de manutenção**, no cabeçalho, que admite dois valores —
**alteração** e **consulta**, os mesmos que a recusa nomeia como **ALT** e **CON**.
Qualquer outro valor é recusado com **\* Opcao nao disponivel. Use ALT ou CON \***, com o
cursor no campo do modo, e nada é lido nem gravado. Quando a mensagem chega **sem** o
modo preenchido, a tela adota a **consulta** — é o caso desta jornada, em que os menus do
caminho não deixam modo algum. Quem quer incluir, alterar ou excluir precisa mudar o modo
para **alteração**.

[?] A recusa manda usar **ALT** ou **CON** e a conferência compara o que o operador
informou com os códigos internos de alteração e de consulta; nenhum fonte do lote mostra
quem traduz um no outro — a máscara da tela não veio no lote. Pergunta ao site.

[?] O modo é um campo que chega na mensagem, e o acervo não mostra quem, além do
operador, o preenche: a tela irmã `C219C`, que consulta a mesma tabela e encaminha para
cá, só opera em consulta e não escreve campo nenhum desta tela. Se alguma chamada chega
com o modo em alteração, não foi possível determinar de onde vem. Pergunta ao site.

### RN-06 — No modo consulta nada é gravado

Com o modo de manutenção em **consulta**, o processamento da linha é abandonado antes de
qualquer teste de ação — tanto na passagem de conferência quanto na de gravação — e a
página volta. É a garantia de que a consulta é somente leitura: ela percorre a tabela,
mas não toca em nada.

### RN-07 — A linha sem ação é ignorada

Uma linha só é processada se a classificação estiver preenchida **e** a ação for **I**
(inclusão), **A** (alteração) ou **E** (exclusão). Classificação zerada passa batido;
ação em branco ou ação que a tela não reconhece também: nada é recusado e nada é gravado
para essa linha. A conferência de permissão da operação só acontece depois que a ação foi
reconhecida.

### RN-08 — O gênero tem de estar cadastrado e ativo, e a classe tem de ser a dele

Ao incluir, o sistema confere o cadastro de gêneros de material: o gênero — subclasse e
gênero — tem de existir **no limite do período**, estar **ativo**, e a classe informada
tem de ser a classe cadastrada para aquele gênero. Faltando qualquer das duas coisas, a
recusa é **\* Genero nao cadastrado \***, com o cursor na classe, e nada é gravado. O
sistema percorre as versões do gênero até achar a ativa, e a leitura não expõe os gêneros
marcados como excluídos no cadastro.

[?] A mesma mensagem serve a três situações distintas — gênero inexistente, gênero
inativo e classe que não é a do gênero — e o operador não fica sabendo qual foi. Pergunta
ao site.

### RN-09 — A inclusão recusa gênero que já está na tabela da quinzena

A inclusão confere se o gênero já está na tabela daquela quinzena; estando, recusa com
**\* Genero ja cadastrado nesta tabela \***, com o cursor na classe, e o preço que já
estava gravado não é tocado.

[?] O dicionário de dados admite repetição nessa combinação — a chave desta tabela é
declarada aceitando registros repetidos, ao contrário das chaves da tabela de referência,
que não os admitem —, de modo que a unicidade que a mensagem anuncia depende só desta
conferência da tela. Se outro caminho gravar nesta tabela sem passar por aqui, pode haver
dois preços para o mesmo gênero na mesma quinzena. Pergunta ao site.

### RN-10 — A inclusão exige o preço corrente

O **preço corrente** é obrigatório na inclusão; em branco (zero), a recusa é
**\* Informe o preco do genero \***, com o cursor no preço, e nada é gravado. Os outros
dois preços — o unitário de atacado e o do gênero no varejo — podem ficar zerados sem
recusa. É o preço corrente que a transação dos gêneros das permissões de contrato leva
para o gênero da regional e que, faltando, faz aquela transação recusar o gênero.

[?] O preço corrente é o rotulado como **PRECO 2001** e o acervo não diz o que o ano 2001
significa ali — se é a data-base da tabela ou o nome de uma coluna antiga. Pergunta ao
site.

### RN-11 — A inclusão grava a linha, o limite calculado e a variação

Passadas as conferências, a inclusão grava o gênero na tabela daquela quinzena com o
início informado, o **limite que o sistema calculou**, os três preços, e a data e a
matrícula de quem operou; calcula a **variação percentual entre o preço do varejo e o
preço unitário de atacado** — zero quando algum dos dois é zero, negativa quando o varejo
é menor — e grava junto; deixa a linha com a marca de registro atualizado e marca a
**publicação na internet** como **"não"**.

[?] A marca de publicação na internet é gravada sempre como "não" e **nada no acervo a
lê**: nem esta tela, nem as que consultam a tabela, nem as que usam o preço. Se algum
processo externo espera que ela vire "sim", ele nunca recebe isso. Pergunta ao site.

### RN-12 — A alteração exige o gênero na tabela e o preço

A alteração exige o gênero na tabela daquela quinzena — senão
**\* Genero nao cadastrado nesta tabela \***, com o cursor na classe, e nada é gravado —
e o preço corrente preenchido — senão **\* Informe o preco \***, com o cursor no preço. O
limite considerado é o que já está gravado na linha, não um limite recalculado.

### RN-13 — A alteração grava os novos preços e guarda os anteriores

Confirmada, a alteração grava os novos preços na linha da quinzena; o início e o limite
são os que já estavam gravados — o limite não é recalculado —, e a data e a matrícula da
atualização são renovadas. Na trilha de auditoria ficam a linha como estava e a linha
como ficou.

### RN-14 — A exclusão apaga a linha da tabela

A exclusão exige o gênero na tabela daquela quinzena; senão
**\* Genero nao cadastrado nesta tabela \***, com o cursor na classe. Existindo, a linha
é **apagada**: o registro deixa a tabela, e com ele o preço, o limite e a variação. Não é
uma marca de exclusão como na tabela de referência, irmã desta, que continua na base
marcada e some das leituras por causa da marca — aqui o registro desaparece, e a única
memória do que havia é o valor anterior guardado na trilha de auditoria.

[?] A exclusão desta tabela é definitiva, enquanto a da tabela de referência apenas marca
o registro. Se o histórico do preço tem de sobreviver à exclusão — para relatório, para
auditoria fiscal ou para reincluir o mesmo gênero depois —, o acervo não diz onde ele
ficaria. E como a importação da quinzena também cria linhas nesta tabela sem consultar
esta tela, uma linha apagada aqui pode voltar na próxima importação do mesmo período.
Pergunta ao site.

### RN-15 — Toda operação confirmada deixa rastro na auditoria

Cada operação confirmada grava um registro na **trilha de auditoria** com o objeto
auditado (a tabela de preços), a tela, a operação (inclusão, alteração ou exclusão), o
**valor anterior** e o **posterior** e o contexto da sessão: a matrícula, o tipo de
órgão, o terminal, a data e a hora e o número do processo, montado a partir do período.
Na inclusão o valor anterior vai em branco; na alteração vão a linha como estava e como
ficou; na exclusão vai a linha como estava e o posterior em branco.

[?] Antes de montar o registro de auditoria a tela **zera a CRE**, nas três operações, de
modo que a trilha desta tela não registra a coordenadoria regional — ao contrário da tela
irmã da tabela de referência, que grava a CRE da sessão. Se a CRE é necessária para saber
de quem era o preço, a trilha está incompleta. Pergunta ao site.

### RN-16 — Nada é gravado sem acesso e permissão

A tela confere a sessão antes de se apresentar — a estação, o cadastro da tela e o código
de acesso do usuário — e, **por operação**, a permissão do perfil antes de processar a
linha: a inclusão exige a autorização de inclusão, a alteração a de alteração e a
exclusão a de exclusão. Faltando, a resposta é
**\* Acesso negado para esta operacao \*** — ou a recusa de acesso correspondente —, e
nada é gravado nem auditado.

[?] A permissão é conferida na passagem de conferência e não se repete na de gravação: se
ela mudar entre as duas, a gravação não a reconfere. Pergunta ao site.

### RN-17 — A próxima tela preenchida abandona a manutenção

Se a mensagem chega com o **código da próxima tela** preenchido, a manutenção é
abandonada antes de qualquer teste de ação, nada é gravado e a sessão é encaminhada para
a tela indicada pela rota.

[?] O que preenche o código da próxima tela nesta tela não está no acervo: nenhum
programa do lote manda próxima tela para a C219T. Pergunta ao site.

### RN-18 — A quinzena sem gêneros na posição é avisada

Sem gênero nenhum na posição em que a lista começa, a tela não mostra linha e avisa
**\* Tabela sem generos cadastrados \***; o aviso aparece uma vez, na primeira linha da
página.

[?] A mesma marca de "não encontrei" serve a dois casos — a quinzena sem tabela nenhuma e
a lista que chegou ao fim dos gêneros do período — e por isso não se sabe se o aviso
distingue "não há tabela para esta quinzena" de "acabaram os gêneros desta quinzena".
Pergunta ao site.

### RN-19 — A tela lê dois cadastros e não os altera

A tela traz prontas as rotinas de gravação, de exclusão e de travamento para os quatro
cadastros que enxerga — a tabela de preços, o cadastro de gêneros, o cadastro das telas e
a trilha de auditoria —, mas **declarar não é executar**: das oito rotinas de gravação e
de exclusão, só três são executadas — a gravação e a exclusão da tabela de preços e a
gravação da trilha. O cadastro de gêneros e o cadastro das telas são aqui **somente
lidos**. E o que a tela não checar, o dicionário não barra nesta tabela: a chave admite
registros repetidos (RN-09).

### RN-20 — A tela não é a única origem dos preços desta tabela

Os preços desta tabela chegam por dois caminhos. Além da manutenção à mão, feita aqui, a
**atualização da quinzena** dispara, quando a quinzena é do **tipo especial**, um
trabalho de importação que **cria linhas nesta tabela** sem passar por esta tela — sem
conferir gênero repetido e sem passar pela conferência de preço. Por isso uma linha desta
tabela pode ter vindo de fora, e a exclusão feita aqui apaga o que a importação criou
(RN-14).

[?] Quem garante que o preço importado e o preço mantido à mão não se sobreponham, o
acervo não diz: a importação grava a mesma combinação de período e gênero sem consultar
esta tela. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manter os preços da tabela especial da quinzena

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C219T

  Cenário: RN-01 — consultar a tabela especial de uma quinzena
    Dado que estou na tela C219T e o modo de manutenção é a consulta
    E informo o início de uma quinzena que tem gêneros na tabela
    Quando percorro a página
    Então vejo a data do sistema, o tipo de órgão e o limite de vigência que o sistema calculou
    E vejo, em cada linha, a classe, a subclasse, o gênero, a descrição resumida, a unidade de medida, o preço unitário de atacado, o preço do gênero no varejo, o preço corrente e a ação
    E vejo no máximo treze linhas por página
    E nada é gravado

  Cenário: RN-05 — a tela abre em consulta quando a mensagem chega sem o modo
    Dado que chego à C219T pelo caminho dos menus
    Quando a página é apresentada
    Então o modo de manutenção está em consulta
    E preciso mudá-lo para alteração antes de qualquer gravação

  Cenário: RN-05 — modo de manutenção não disponível
    Dado que estou na tela C219T
    Quando informo um modo de manutenção diferente de ALT e de CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo de manutenção
    E nada é gravado

  Cenário: RN-06 — no modo consulta nada é gravado
    Dado que estou na tela C219T com o modo de manutenção em consulta
    Quando informo uma linha com uma ação de inclusão, alteração ou exclusão e confirmo
    Então aquela linha não é conferida
    E nada é gravado
    E a página volta

  Cenário: RN-02, RN-03 e RN-04 — o período informado é conferido
    Dado que estou na tela C219T no modo de alteração
    E que vou incluir um gênero
    Quando o dia do início não é 1 nem 16
    Então vejo a mensagem "* Dia de inicio deve ser 01 ou 16 *"
    E o cursor volta ao dia do início
    E nada é gravado

  Cenário: RN-03 — data de início que não existe
    Dado que estou na tela C219T no modo de alteração
    E que vou incluir um gênero
    Quando a data de início não existe naquele mês e ano, ou o ano está fora de 1994 a 2099
    Então vejo a mensagem "* Data invalida *"
    E o cursor volta ao dia do início
    E nada é gravado

  Cenário: RN-04 — valor não numérico em um dos nove campos informados
    Dado que estou na tela C219T
    Quando informo um valor não numérico em um dos campos do período, da classificação ou dos preços
    Então a tela é recusada
    E o cursor volta ao campo recusado
    E nada é gravado

  Cenário: RN-07 — linha sem ação ou com ação desconhecida
    Dado que estou na tela C219T no modo de alteração
    Quando deixo a classificação em branco, ou preencho a linha com uma ação diferente de I, A e E
    Então aquela linha não é conferida
    E nada é gravado para ela
    E nenhuma mensagem é mostrada

  Cenário: RN-08 — gênero não cadastrado, inativo ou com classe divergente
    Dado que estou na tela C219T no modo de alteração
    Quando tento incluir um gênero que não existe no cadastro no limite do período, que não está ativo, ou cuja classe não é a do cadastro
    Então vejo a mensagem "* Genero nao cadastrado *"
    E o cursor fica na classe
    E nada é gravado

  Cenário: RN-09 — incluir um gênero que já está na tabela da quinzena
    Dado que estou na tela C219T no modo de alteração
    E que o gênero já está na tabela especial daquela quinzena
    Quando confirmo a inclusão desse gênero
    Então vejo a mensagem "* Genero ja cadastrado nesta tabela *"
    E o cursor fica na classe
    E o preço que já estava gravado não é alterado

  Cenário: RN-10 — incluir sem o preço corrente
    Dado que estou na tela C219T no modo de alteração
    E que o gênero está cadastrado, ativo e ainda não está na tabela da quinzena
    Quando confirmo a inclusão sem informar o preço corrente
    Então vejo a mensagem "* Informe o preco do genero *"
    E o cursor fica no preço
    E nada é gravado

  Cenário: RN-11 — incluir um gênero na tabela especial da quinzena
    Dado que estou na tela C219T no modo de alteração
    E que o gênero está cadastrado, ativo e ainda não está na tabela da quinzena
    Quando informo os preços e confirmo a ação I
    Então a linha é gravada na tabela especial daquela quinzena
    E o limite gravado é o que o sistema calculou para o período
    E a variação entre o preço do varejo e o preço unitário de atacado fica calculada
    E a linha fica com a marca de registro atualizado e com a publicação na internet em "não"
    E a inclusão fica registrada na auditoria

  Cenário: RN-12 — alterar um gênero fora da tabela da quinzena
    Dado que estou na tela C219T no modo de alteração
    Quando confirmo a ação A para um gênero que não está na tabela daquela quinzena
    Então vejo a mensagem "* Genero nao cadastrado nesta tabela *"
    E o cursor fica na classe
    E nada é gravado

  Cenário: RN-12 — alterar sem o preço corrente
    Dado que estou na tela C219T no modo de alteração
    E que o gênero está na tabela daquela quinzena
    Quando confirmo a ação A sem informar o preço corrente
    Então vejo a mensagem "* Informe o preco *"
    E o cursor fica no preço
    E nada é gravado

  Cenário: RN-13 — alterar os preços de um gênero da quinzena
    Dado que estou na tela C219T no modo de alteração
    E que o gênero está na tabela daquela quinzena
    Quando informo os novos preços e confirmo a ação A
    Então os novos preços ficam gravados na linha daquela quinzena
    E o início e o limite da quinzena continuam os mesmos
    E a data e a matrícula da atualização são renovadas
    E a linha como estava antes e como ficou fica registrada na auditoria

  Cenário: RN-14 — excluir um gênero da tabela da quinzena
    Dado que estou na tela C219T no modo de alteração
    E que o gênero está na tabela daquela quinzena
    Quando confirmo a ação E
    Então o registro é apagado da tabela especial daquela quinzena
    E o gênero deixa de aparecer na consulta daquela quinzena
    E o valor que havia fica registrado na auditoria

  Cenário: RN-14 — excluir um gênero fora da tabela da quinzena
    Dado que estou na tela C219T no modo de alteração
    E que o gênero não está na tabela daquela quinzena
    Quando confirmo a ação E
    Então vejo a mensagem "* Genero nao cadastrado nesta tabela *"
    E o cursor fica na classe
    E nada é apagado

  Cenário: RN-15 — toda operação confirmada deixa rastro na auditoria
    Dado que confirmei uma inclusão, uma alteração ou uma exclusão na C219T
    Quando a gravação termina
    Então existe um registro de auditoria da tabela de preços
    E com a tela, a operação e o valor anterior e o posterior
    E com a matrícula, o tipo de órgão, o terminal, a data e a hora e o número do processo

  Cenário: RN-16 — sem autorização de perfil para a operação
    Dado que estou na tela C219T no modo de alteração
    E que o meu perfil não tem a autorização da operação que confirmo
    Quando confirmo a linha
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado e nada é auditado

  Cenário: RN-17 — a próxima tela preenchida abandona a manutenção
    Dado que a mensagem chega à C219T com o código da próxima tela preenchido
    Quando a manutenção começaria
    Então a linha não é conferida e nada é gravado
    E a sessão é encaminhada para a tela indicada pela rota

  Cenário: RN-18 — quinzena sem gêneros na posição
    Dado que estou na tela C219T
    E não há gênero nenhum na posição de início do período
    Quando a página é apresentada
    Então vejo a mensagem "* Tabela sem generos cadastrados *"
    E a página não mostra linha alguma

  Cenário: RN-20 — o preço pode ter vindo da importação da quinzena
    Dado que a quinzena é do tipo especial e a atualização da quinzena já rodou
    Quando consulto a tabela dessa quinzena na C219T
    Então vejo linhas que a importação criou sem passar por esta tela
    E essas linhas podem ser alteradas ou apagadas aqui como as demais
```
