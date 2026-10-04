# US — C213T — Manutenção da tabela de preços da quinzena

## Estória

Como **servidor de CRE**, quero **manter os preços dos gêneros de material na tabela da
quinzena**, para que **a secretaria publique e corrija os preços de cada metade do mês antes de
eles valerem para os pedidos**.

Os preços dos gêneros de material são tabelados por quinzena: cada metade do mês tem a sua
tabela, com um preço por gênero. É essa tabela que a consulta de preços mostra e que a impressão
da tabela leva para o relatório — sem esta manutenção, a quinzena simplesmente não tem preço para
os gêneros. A tela exige o preço do gênero e recusa incluí-lo duas vezes no mesmo período, para
que não existam dois preços para o mesmo gênero na mesma quinzena.

## Contexto

Jornada S000M → C000M → C015M → C213T.
Ator: servidor de CRE — escolhe a quinzena, vê os gêneros da tabela daquele período e inclui,
altera ou exclui o preço de cada um.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

As duas telas antes desta são menus: elas só encaminham e não deixam dado de negócio para a
`C213T`. O que a tela usa da sessão — a matrícula, o código de acesso e o privilégio, o tipo de
órgão e a sua descrição, a CRE e a data do sistema — é o que a entrada deixou; a tela não
recalcula nada disso. A tela irmã **C213C** consulta a mesma tabela daquele período e é ela que
pede a impressão da tabela; a **C215T** é a tela que marca o preço como publicado na internet.

Esta é a última tela da jornada: ela não encadeia com nenhuma outra e não entrega a transação
adiante. O que ela mantém é a tabela de preços da quinzena; a consulta e a impressão dela são
outras telas.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — O que a tela mantém

O que a tela mantém é a **tabela de preços da quinzena**. Informado o **início do período** — dia,
mês e ano —, ela lista os **gêneros de material** daquela quinzena, **treze por página**, um por
linha, na ordem do cadastro: a **classe, a subclasse e o gênero**, a **descrição resumida do
gênero**, a **unidade de medida** e os **três preços** do gênero — o preço unitário de atacado, o
preço do gênero no varejo e o preço da tabela (o mesmo que a consulta de preços mostra) —, cada
preço com duas casas decimais, além da **ação** da linha. No cabeçalho vêm o **limite de vigência**
da quinzena, a **data do sistema** e a **descrição do tipo de órgão** da sessão. A tabela comporta
**150.000 registros**; a capacidade é o máximo esperado (parâmetro de dimensionamento), não o
volume cadastrado.

[?] Os três preços aparecem na tela como PRECO UNIT.ATACA, PREC.GEN. VAREJO e PRECO 2001. O que o
rótulo **PRECO 2001** designa, e por que é ele o preço que a consulta de preços mostra e o único
exigido na inclusão, não está no corpus nem no manual. Pergunta ao site.

### RN-02 — A quinzena é identificada pelo início, e o fim é calculado pelo sistema

O dia, o mês e o ano do início identificam a tabela da quinzena. Por ser a quinzena a metade do
mês, o dia tem de ser **1** ou **16**: qualquer outro dia é recusado com
* Dia de inicio deve ser 01 ou 16 *, com o cursor de volta no dia do início, e nada é gravado.
Informado o dia **1**, o limite é o dia **15** do mesmo mês e ano; informado o dia **16**, o limite
é o **último dia daquele mês** — 28, 29, 30 ou 31, conforme o mês. O limite é do sistema: o que
estiver no campo é o que ele calculou.

[?] A conferência do dia 1 ou 16 e o cálculo do limite só são executados na **inclusão**. Na
alteração e na exclusão o período não passa por essa conferência: o sistema procura a linha pelo
que foi informado e, não achando, recusa pela regra do gênero não cadastrado na tabela. Se essas
duas operações deveriam conferir o período, pergunta ao site.

### RN-03 — O início tem de ser uma data que existe

A data de início é conferida como data de calendário: o ano tem de estar entre **1994** e **2099**
e o dia tem de existir naquele mês e ano. Não existindo, a recusa é * Data invalida *, com o
cursor no dia do início, e nada é gravado.

### RN-04 — Os campos informados são conferidos

**Nove** campos são conferidos como numéricos — o dia, o mês e o ano do início, a classe, a
subclasse, o gênero e os três preços —, o que estiver em branco é tratado como zero e os zeros à
esquerda são descartados; o campo recusado devolve o cursor a si mesmo e a gravação não segue.

[?] O texto que o operador vê quando um valor não numérico é recusado não está no programa: a
conferência é chamada de uma rotina de biblioteca cujo corpo não veio no lote. Pergunta ao site.

[?] A conferência roda a cada uma das treze linhas e está amarrada ao tipo da mensagem que chega;
o que distingue uma mensagem de operador de uma mensagem automática não está explicado no corpus
nem no manual. Se existe um caminho de entrada em que ela não roda, não foi possível determinar.
Pergunta ao site.

### RN-05 — A página tem treze linhas

A tela apresenta **treze linhas** por página; cada linha é um gênero daquela quinzena, com os seus
preços e com a sua ação.

### RN-06 — O modo da página: alteração ou consulta

A página tem um único **modo de manutenção**, que admite dois valores — **alteração** e
**consulta**, os mesmos que a recusa nomeia como **ALT** e **CON**. Qualquer outro valor é recusado
com * Opcao nao disponivel. Use ALT ou CON *, com o cursor no campo do modo, e nada é lido nem
gravado. O modo não se digita a cada linha: quando a tela abre sem nenhum modo guardado, ela abre
em **consulta**; do uso anterior na mesma sessão ela repõe o modo que ficou guardado.

[?] A recusa manda usar **ALT** ou **CON** e a conferência compara o campo com os códigos internos
de alteração e de consulta; nenhum fonte do lote mostra quem traduz o que o operador digita. A
mesma dúvida está registrada na consulta C213C e no pedido da C210T. Pergunta ao site.

[?] O modo guardado vive na área de trabalho que as telas compartilham na sessão: uma tela anterior
pode deixá-lo preenchido, e a C213T abrir já em alteração sem que o operador escolha. Quem, nesta
jornada, o deixaria preenchido não está na fonte desta tela. Pergunta ao site.

### RN-07 — Na consulta nada é gravado

Com o modo em **consulta**, a linha é abandonada antes de qualquer teste de ação — tanto na
passagem de conferência quanto na passagem de gravação — e a página volta. É a garantia de que a
consulta é somente leitura: ela percorre a tabela, mas não toca em nada.

### RN-08 — A linha sem ação é ignorada

Uma linha só é processada se a classificação estiver preenchida **e** a ação for `I` (inclusão),
`A` (alteração) ou `E` (exclusão). Classificação zerada, ação em branco ou ação que a tela não
reconhece passam batido: nada é recusado e nada é gravado para essa linha.

### RN-09 — Incluir exige o gênero cadastrado e ativo

Ao incluir, o sistema confere o cadastro de gêneros de material: o gênero — subclasse e gênero —
tem de existir no cadastro e estar **ativo** na data-limite daquele período, e a classe informada
tem de ser a classe cadastrada para aquele gênero. Faltando qualquer das duas coisas, a recusa é
* Genero nao cadastrado *, com o cursor na classe, e nada é gravado.

[?] A mesma mensagem serve a dois casos distintos — gênero inexistente ou inativo e classe que não
é a do gênero —, e o operador não fica sabendo qual dos dois foi. Pergunta ao site.

### RN-10 — Incluir recusa gênero já na tabela do período

Antes de incluir, o sistema confere se aquele gênero já está na tabela daquela quinzena. Estando, a
recusa é * Genero ja cadastrado nesta tabela *, com o cursor na classe, e nada é gravado.

### RN-11 — Incluir exige o preço da tabela

O **preço da tabela** é obrigatório na inclusão: em branco — que a conferência trata como zero —, a
recusa é * Informe o preco do genero *, com o cursor no preço, e nada é gravado. Os outros dois
preços não são exigidos.

### RN-12 — A inclusão grava a linha, o limite calculado e a variação

Passadas as conferências, a inclusão grava o gênero na tabela da quinzena com o início informado, o
**limite calculado pelo sistema**, os três preços informados, a **data e a matrícula** de quem
operou; calcula e guarda a **variação percentual** entre o preço do varejo e o preço unitário de
atacado; e marca a **indicação de publicação na internet** como **não** — o operador não escolhe
esse valor nesta tela.

[?] A variação é calculada como (preço do varejo ÷ preço de atacado − 1) × 100 e fica em zero
quando qualquer dos dois preços é zero ou quando a divisão estoura. O que o sistema faz com esse
número não está nesta jornada. Pergunta ao site.

[?] O que a indicação de publicação na internet governa não está no corpus nem no manual. Outra
tela do sistema — a C215T — é quem a marca, pelo limite do período; nenhuma tela desta jornada a
mostra ou a lê. Pergunta ao site.

### RN-13 — Alterar exige o gênero na tabela e o preço

Para alterar, o sistema exige que o gênero esteja na tabela daquela quinzena: não estando, a recusa
é * Genero nao cadastrado nesta tabela *, com o cursor na classe, e nada é gravado. E o preço da
tabela tem de estar preenchido: em branco, a recusa é * Informe o preco *, com o cursor no preço, e
nada é gravado.

### RN-14 — A alteração grava os novos preços e guarda os anteriores

Confirmada, a alteração grava os novos preços na linha da quinzena — o início e o limite são os que
já estavam gravados, não são recalculados —, atualiza a data e a matrícula de quem operou, e deixa
na auditoria a linha como estava antes e como ficou.

### RN-15 — A exclusão marca o gênero como excluído

A exclusão **não apaga** a linha da tabela: o sistema a marca como **excluída**, atualiza a data e
a matrícula e grava o registro de volta. Daí em diante o gênero não aparece mais na tabela daquela
quinzena — a leitura da tabela ignora os registros marcados como excluídos —, mas o registro
continua na base e ocupa a mesma capacidade da tabela.

[?] O registro excluído permanece na base e apenas deixa de ser lido: se existe rotina de expurgo e
se o mesmo gênero pode ser reincluído na mesma quinzena — a conferência da inclusão não o encontra
mais — não está na fonte desta jornada. Pergunta ao site.

### RN-16 — Toda operação confirmada deixa rastro na auditoria

Cada inclusão, alteração ou exclusão confirmada grava um registro na **auditoria**: o que foi
auditado (a tabela de preços), a **operação**, o **valor anterior e o posterior** — na inclusão não
há anterior — e o contexto da sessão: matrícula, tipo de órgão, CRE, terminal, data e hora, número
do processo e a tela de origem.

[?] Na inclusão o rastro está sob a condição de a gravação não devolver um certo estado de retorno
que nenhum arquivo do lote atribui. Pelo fonte, a inclusão é auditada; se o ambiente atribuir esse
estado em algum caminho, ela fica sem rastro — a alteração e a exclusão não têm essa condição.
Pergunta ao site.

### RN-17 — Nada é gravado sem acesso e permissão

Antes de apresentar e antes de gravar, a tela confere a sessão — a estação registrada para a
matrícula, o código de acesso e a situação da tela no cadastro de telas — e, **por operação**, a
permissão do perfil: a inclusão exige a autorização de inclusão, a alteração a de alteração e a
exclusão a de exclusão. Sem a permissão, a resposta é * Acesso negado para esta operacao * — ou a
recusa de acesso correspondente — e nada é gravado nem auditado.

[?] A conferência de permissão por operação só é chamada nas operações de manutenção: a consulta
passa por fora dela, e o cadastro de permissões guarda uma marca de consulta que nenhuma rotina do
lote lê. O que uma consulta deveria exigir não está na fonte. Pergunta ao site.

### RN-18 — A próxima tela preenchida abandona a manutenção

Se a mensagem chega com o código da **próxima tela** preenchido, a manutenção é abandonada antes de
qualquer teste de ação: a linha não é conferida, nada é gravado e a sessão é encaminhada para a
tela indicada. O mesmo campo é o que leva o operador de uma tela a outra. Esta tela é o fim da
trilha: ela não devolve nenhuma próxima tela.

[?] O que preenche o código da próxima tela na C213T não está no corpus; o caminho declarado desta
jornada chega pelo menu, de modo que o campo chega em branco. Pergunta ao site.

### RN-19 — A quinzena sem gêneros na posição de início é avisada

Quando a posição de início do período mostrado não encontra gênero nenhum, a tela não mostra linha
alguma e avisa * Tabela sem generos cadastrados *.

[?] Se o aviso distingue "quinzena sem tabela" de "acabaram os gêneros do período": a mesma marca
de "não encontrei" serve aos dois casos, e a posição pode estar depois do último gênero da
quinzena. A mesma dúvida está registrada na consulta C213C. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manutenção da tabela de preços da quinzena

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C213T

  Cenário: A tela lista os gêneros da tabela da quinzena
    Dado que existe a tabela de preços da quinzena informada
    Quando apresento a tela com o início do período
    Então vejo treze gêneros por página, na ordem do cadastro
    E de cada gênero vejo a classe, a subclasse, o gênero, a descrição, a unidade de medida e os três preços
    E vejo o limite de vigência da quinzena, a data do sistema e a descrição do tipo de órgão
    E nada foi gravado

  Cenário: Dia de início diferente de 1 e de 16 é recusado
    Dado que estou na tela C213T no modo ALT
    Quando informo o início do período em um dia diferente de 1 e de 16 e confirmo a inclusão
    Então vejo a mensagem "* Dia de inicio deve ser 01 ou 16 *"
    E o cursor volta para o dia do início
    E nada é gravado

  Cenário: O fim da quinzena é calculado pelo sistema
    Dado que estou na tela C213T no modo ALT
    Quando informo o início do período no dia 1
    Então o limite da quinzena fica no dia 15 do mesmo mês e ano
    E se informo o dia 16, o limite fica no último dia daquele mês

  Cenário: Início que não existe no calendário é recusado
    Dado que estou na tela C213T no modo ALT
    Quando informo uma data de início que não existe no calendário e confirmo a inclusão
    Então vejo a mensagem "* Data invalida *"
    E o cursor volta para o dia do início
    E nada é gravado

  Cenário: Valor não numérico em um campo informado é recusado
    Dado que estou na tela C213T
    Quando informo um valor não numérico no mês do início do período
    Então a linha é recusada antes da gravação
    E o cursor volta para o campo do mês do início
    E nada é gravado

  Cenário: O modo da página só admite ALT ou CON
    Dado que estou na tela C213T
    Quando informo um modo de manutenção diferente de ALT e de CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo de manutenção
    E nada é gravado

  Cenário: Sem modo guardado, a tela abre em consulta
    Dado que a área de trabalho da sessão não tem modo de manutenção guardado
    Quando a tela C213T é apresentada
    Então ela abre em consulta
    E o modo apresentado é a consulta

  Cenário: A consulta não grava nada
    Dado que estou na tela C213T no modo CON
    Quando percorro a quinzena e confirmo as linhas da página
    Então nenhum preço é incluído, alterado ou excluído
    E a tabela da quinzena continua como estava

  Cenário: Linha sem ação é ignorada
    Dado que estou na tela C213T no modo ALT
    Quando deixo a classificação em branco ou a ação em branco
    Então a linha não é conferida e nada é gravado para ela

  Cenário: Gênero não cadastrado ou inativo é recusado
    Dado que estou na tela C213T no modo ALT
    Quando tento incluir um gênero que não existe no cadastro ou que não está ativo
    Então vejo a mensagem "* Genero nao cadastrado *"
    E o cursor fica na classe
    E nada é gravado

  Cenário: Inclusão recusa gênero já na tabela da quinzena
    Dado que estou na tela C213T no modo ALT
    E que o gênero já está na tabela daquela quinzena
    Quando confirmo a inclusão desse gênero
    Então vejo a mensagem "* Genero ja cadastrado nesta tabela *"
    E o cursor fica na classe
    E o preço que já estava na tabela não é alterado

  Cenário: Inclusão sem o preço da tabela é recusada
    Dado que estou na tela C213T no modo ALT
    E que o gênero está cadastrado, ativo e ainda não está na tabela da quinzena
    Quando confirmo a inclusão sem informar o preço da tabela
    Então vejo a mensagem "* Informe o preco do genero *"
    E o cursor fica no preço
    E nada é gravado

  Cenário: A inclusão grava a linha da quinzena
    Dado que estou na tela C213T no modo ALT
    E que o gênero está cadastrado, ativo e ainda não está na tabela da quinzena
    Quando informo o preço da tabela e confirmo a ação I
    Então a linha é gravada na tabela daquela quinzena
    E o limite gravado é o que o sistema calculou para o período
    E a variação entre o preço do varejo e o preço unitário de atacado fica calculada
    E o preço fica marcado como não publicado na internet
    E a inclusão fica registrada na auditoria

  Cenário: Alteração de gênero fora da tabela é recusada
    Dado que estou na tela C213T no modo ALT
    Quando confirmo a ação A para um gênero que não está na tabela daquela quinzena
    Então vejo a mensagem "* Genero nao cadastrado nesta tabela *"
    E o cursor fica na classe
    E nada é gravado

  Cenário: Alteração sem o preço é recusada
    Dado que estou na tela C213T no modo ALT
    E que o gênero está na tabela daquela quinzena
    Quando confirmo a ação A sem informar o preço da tabela
    Então vejo a mensagem "* Informe o preco *"
    E o cursor fica no preço
    E nada é gravado

  Cenário: A alteração grava os novos preços e guarda os anteriores
    Dado que estou na tela C213T no modo ALT
    E que o gênero está na tabela daquela quinzena
    Quando informo os novos preços e confirmo a ação A
    Então os novos preços ficam gravados na linha daquela quinzena
    E o início e o limite da quinzena continuam os mesmos
    E a linha como estava antes e como ficou fica registrada na auditoria

  Cenário: A exclusão marca o gênero como excluído
    Dado que estou na tela C213T no modo ALT
    E que o gênero está na tabela daquela quinzena
    Quando confirmo a ação E
    Então o gênero deixa de aparecer na tabela daquela quinzena
    E o registro continua na base marcado como excluído
    E a exclusão fica registrada na auditoria

  Cenário: Toda operação confirmada deixa rastro na auditoria
    Dado que confirmei uma inclusão, uma alteração ou uma exclusão na C213T
    Quando a gravação termina
    Então existe um registro de auditoria da tabela de preços
    E com a operação e com o valor anterior e o posterior
    E com a matrícula, o tipo de órgão, a CRE, o terminal, a data e a hora e o número do processo

  Cenário: Sem autorização de perfil para a operação
    Dado que estou na tela C213T no modo ALT
    E que o meu perfil não tem a autorização da operação que confirmo
    Quando confirmo a linha
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado e nada é auditado

  Cenário: A próxima tela preenchida abandona a manutenção
    Dado que a mensagem chega à C213T com o código da próxima tela preenchido
    Quando a manutenção começaria
    Então a linha não é conferida e nada é gravado
    E a sessão é encaminhada para a tela indicada

  Cenário: A quinzena sem gêneros na posição de início é avisada
    Dado que estou na tela C213T e não há gênero nenhum na posição de início do período
    Quando a página é apresentada
    Então vejo a mensagem "* Tabela sem generos cadastrados *"
    E a página não mostra linha alguma
```
