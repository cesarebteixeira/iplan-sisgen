# US — F153T — Lançar os gêneros da nota fiscal de desconto

## Estória

Como **servidor de CRE que lança a despesa da secretaria**, quero **lançar os gêneros que
compõem a nota fiscal de desconto — com a unidade de medida, a quantidade e o valor de
cada um — e ver o desconto da nota repartido entre eles**, para que **a nota deixe de ser
só a capa e passe a dizer em que gênero o dinheiro foi gasto, com o desconto já
distribuído e o acumulado do convênio do fornecedor fechando com o que foi lançado**.

A nota de desconto só fica completa quando tem gêneros: é por eles que a despesa é
conferida contra o que foi pago, e é por eles que o desconto da nota desce ao item. Sem
esta tela a capa da nota fica sem conteúdo — o desconto não teria como chegar ao gênero,
o valor total dos itens não existiria, e o acumulado do convênio do fornecedor ficaria
com o valor da nota sem saber a que gênero ele se refere.

## Contexto

Jornada S000M → F000M → F100M → F150C → F153T.
Ator: servidor de CRE — lança, altera e exclui os gêneros de uma nota fiscal de desconto e
consulta o que já está lançado nela.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A `F153T` não é menu, e não se abre por opção de menu: ela é a tela dos gêneros da nota, e
quem a abre é sempre uma das duas telas da nota — a **capa** (`F152T`) ou a **lista de
notas** (`F150C`). As duas telas antes dela **não** são menus: `F150C` é uma tela de
consulta que **encadeia** nesta sem passar por menu nenhum, por dentro, e é por isso que o
recorte e a operação com que a `F153T` abre vêm de trás, e não do que se digita aqui. O
`F000M` e o `F100M` são menus e não deixam dado de negócio para esta tela.

O que a `F153T` usa da sessão — a secretaria (o tipo de órgão) e o grupo de coordenação
regional (a CRE) — é o que a entrada deixou; a tela não escolhe nada disso, apenas confere
antes de gravar. O que ela mostra da nota é o que a tela que a chamou deixou, e não uma
nova leitura do cadastro.

O que ela entrega à seguinte: quando a nota fica sem nenhum gênero, ela apaga o acumulado
do convênio, a nota e os gêneros dela e devolve o servidor à **capa**, já em inclusão,
para uma nota nova. Quando falta secretaria ou grupo na sessão, devolve o servidor à capa
**sem avisar** e sem gravar. Vinda de qualquer tela que não seja a capa ou a lista de
notas, devolve o servidor ao **menu de despesas** (`F100M`).

## Regras de negócio

### RN-01 — A tela é o lançamento dos gêneros da nota fiscal

Esta tela mantém os **gêneros** de uma nota fiscal de desconto: inclui, altera e exclui
gênero a gênero, consulta o que está lançado e, por conta disso, regrava o que a nota
passa a acumular e o que o convênio do fornecedor passa a acumular.

O que ela grava é o cadastro de notas fiscais (`F155T` — **20 campos**, capacidade de
**100.000** notas), o cadastro dos gêneros da nota (`F156T` — **13 campos**, **100.000**) e
o acumulado do convênio do fornecedor (`F157T` — **9 campos**, **100.000**). Ela lê o
cadastro dos gêneros (`F011T` — 7 campos, 2.000) para saber o nome do gênero, o cadastro
das unidades de medida de cada gênero (`F016T` — 2 campos, 10.000) para saber se a unidade
informada vale para aquele gênero, e o cadastro de telas (`S030T` — 7 campos, 2.000). Toda
gravação que ela faz deixa rastro na auditoria (`A010T`).

As capacidades acima são **capacidade** — o máximo esperado, parâmetro de dimensionamento
—, não volume cadastrado.

Na tela o servidor vê e digita a operação, os dados da nota — o número, o grupo, as duas
datas, o ano de competência, o número e o ano do convênio, o modelo com a sua descrição, o
fornecedor com a razão social, a unidade com o nome do órgão, o valor total da nota, o
desconto, o total dos gêneros e o que ainda falta lançar — e, gênero por gênero, o código
do gênero, a sua descrição, a unidade de medida, a quantidade, o preço unitário, o valor
total do item e a ação da linha. A **descrição do tipo de órgão** (a secretaria) e a
**data do sistema** também aparecem, mas são informação de saída — o usuário as vê, o
terminal não as devolve — e são apagadas no começo de cada resposta, junto com a descrição
do gênero.

### RN-02 — A tela só abre vinda da capa ou da lista de notas, e herda a operação de quem a chamou

Esta tela não se abre por menu: quem a abre é a **capa da nota** ou a **lista de notas**,
e é delas que vem a operação com que ela trabalha. Vinda da capa (`F152T`), ela abre na
operação que o servidor pediu lá: **inclusão**, **alteração** ou **consulta**. Vinda da
lista de notas (`F150C`), abre sempre em **consulta**. Vinda de qualquer outra tela, ela
não abre: devolve o servidor ao **menu de despesas**.

A operação é reconferida a cada resposta. Só **inclusão**, **alteração** e **consulta**
são aceitas: qualquer outra — inclusive a **exclusão** e inclusive o campo em branco — é
recusada com **\* Opcao nao disponivel. Use INC, ALT ou CON \***, com o cursor de volta ao
campo da operação, antes de qualquer leitura ou gravação.

[?] A exclusão confirmada na capa apaga a nota e, logo depois, abre esta tela com a
operação de exclusão — que ela mesma recusa com * Opcao nao disponivel. Use INC, ALT ou
CON *. Ou o servidor deveria ver essa recusa depois de uma exclusão bem-sucedida, ou o
caminho não deveria abrir esta tela depois de apagar a nota. Pergunta ao site.

### RN-03 — O que a tela mostra da nota vem de trás, não do cadastro

Os dados da nota que aparecem nesta tela não são relidos do cadastro ao abrir: são
exatamente o que a tela anterior — a capa ou a lista de notas — deixou, inclusive o valor
total da nota, o desconto, o total dos gêneros e o valor que ainda falta lançar. Do
cadastro a tela lê só os **gêneros já lançados** na nota.

[?] Como a nota não é relida, o que o servidor vê aqui é o que a tela anterior tinha em
mãos: se a nota mudou por outro caminho no meio do percurso, é o valor antigo que aparece.
Se a tela deveria reler a nota do cadastro ao abrir, pergunta ao site.

### RN-04 — Os gêneros da nota, um por linha, até oito

Aberta em **alteração** ou em **consulta**, a tela percorre os gêneros já lançados na nota
— do primeiro ao último, na ordem do código do gênero — e preenche uma linha por gênero,
até **oito linhas**. Cada linha traz o código do gênero, a descrição lida do cadastro dos
gêneros, a unidade de medida, a quantidade, o preço unitário, o valor total do item e a
ação da linha. A tela mostra também o **total dos gêneros** da nota.

Aberta em **inclusão**, a tela não traz gênero nenhum: as linhas vêm em branco, para o
servidor digitar.

[?] A nota que tiver mais de oito gêneros: a tela preenche oito linhas, não avisa que há
mais e não tem campo de página para ver o resto. Se há como ver os gêneros além dos oito,
não está nesta tela. Pergunta ao site.

### RN-05 — A nota sem nenhum gênero é avisada

Procurados os gêneros da nota e não havendo nenhum, a tela avisa **\* Nota fiscal sem
generos cadastrados \*** e deixa as linhas em branco. O aviso é dado uma vez, na primeira
linha.

[?] Esta tela apaga a nota inteira quando o último gênero sai dela (RN-18), de modo que
uma nota sem gêneros só existe se tiver ficado assim por outro caminho. Se o aviso é
alcançável, e o que o servidor deveria poder fazer com uma nota sem gêneros, pergunta ao
site.

### RN-06 — A ação de cada linha decide o que a tela faz com ela

Cada linha da tela tem a sua **ação**, que o servidor digita: **incluir**, **alterar** ou
**excluir** o gênero daquela linha. A ação é conferida linha a linha e é ela que decide se
o gênero é criado, regravado ou apagado na nota.

Linha sem ação, ou com uma ação que a tela não reconheça, é **ignorada em silêncio**: nada
é lido, nada é gravado e o servidor não vê aviso nenhum. Quando a operação da tela é a
**inclusão**, a linha que tiver gênero informado recebe sozinha a ação de incluir — o
servidor não precisa digitá-la.

### RN-07 — Incluir um gênero que já está na nota soma ao que existe

Se o gênero que o servidor manda incluir já está lançado naquela nota, a tela **não cria
uma segunda linha para ele**: soma a quantidade informada à quantidade que já estava
lançada e o valor informado ao valor que já estava lançado, e passa a tratar a linha como
**alteração**, gravando o gênero com a soma.

### RN-08 — Cada linha passa pela permissão da ação

Antes de tocar em qualquer gênero, a tela confere se o perfil da tela libera a ação daquela
linha — incluir, alterar ou excluir. Não liberando, a operação é recusada com **\* Acesso
negado para esta operacao \*** e nada é gravado.

[?] A permissão conferida é a da ação que o servidor **digitou**, e não a da ação que a
tela acaba **aplicando**: a linha marcada para incluir é conferida como inclusão mesmo
quando o gênero já existe e a tela a transforma em alteração. Se a permissão deveria ser a
da alteração nesse caso, pergunta ao site.

### RN-09 — O gênero tem de estar cadastrado

O gênero é identificado pelo seu **código**. Antes de lançá-lo, a tela procura esse código
no cadastro dos gêneros: não achando, recusa com **\* Cod.FNDE nao cadastrado \***, com o
cursor de volta ao campo do código do gênero, e nada é gravado.

[?] O rótulo do campo fala do **gênero FAE** e as recusas falam do **código FNDE** — e a
recusa da unidade de medida mistura os dois ("unidade de medida não cadastrada para este
código FNDE"). Se FAE e FNDE são o mesmo cadastro com dois nomes, ou dois códigos
diferentes, pergunta ao site.

### RN-10 — A unidade de medida tem de valer para o gênero

A unidade de medida informada na linha é conferida contra o cadastro das unidades de cada
gênero: não estando cadastrada para aquele gênero, a recusa é **\* Unid.medida nao cad.
para este cod.FNDE \***, com o cursor de volta ao campo da unidade, e nada é gravado. A
conferência é feita tanto na inclusão quanto na alteração.

### RN-11 — A quantidade e o valor total do item são obrigatórios

Para lançar um gênero, a **quantidade** e o **valor total do item** têm de estar
informados: quantidade zerada é recusada com **\* Informe a quantidade \***, com o cursor
no campo da quantidade; valor total zerado, com **\* Informe o valor total do item na
nota \***, com o cursor no campo do valor. Nas duas nada é gravado.

### RN-12 — O preço unitário é calculado pela divisão do valor pela quantidade

O preço unitário não é o que o servidor digita: a tela o **calcula**, dividindo o valor
total do item pela quantidade, e grava o gênero com esse preço. Se o preço unitário sair
zerado — porque a conta não coube no campo do preço, ou porque o valor é menor que a
quantidade —, a recusa é **\* Preco unitario zerado \***, com o cursor no campo do valor
total do item, e nada é gravado.

### RN-13 — A soma dos gêneros não pode passar do valor da nota mais o desconto

A tela confere o que a nota vai ficar somando com o gênero que se está lançando: a soma
final dos gêneros da nota não pode passar do **valor total da nota somado ao desconto
dela**. Passando, a recusa é **\* Desconto - vl.itens > vl.nota \***, com o cursor no
campo do valor total do item, e nada é gravado. A conferência vale para incluir e para
alterar.

### RN-14 — Alterar e excluir exigem o gênero já lançado na nota

A alteração e a exclusão são de um gênero **que já está na nota**: se o código informado
não estiver lançado naquela nota, a recusa é **\* Cod.FNDE nao cadastrado nesta nota \***,
com o cursor de volta ao campo do código do gênero, e nada é gravado.

### RN-15 — A tela grava a nota e os gêneros

Passando pelas conferências, a tela grava: **cria a nota** quando ela ainda não existe (a
nota nasce com o gênero que a originou), **cria ou regrava o gênero**, regrava o valor
total dos gêneros da nota com a soma de todos eles, e regrava o acumulado do convênio do
fornecedor. Se o gênero já estava na nota e o servidor mandou incluir, o gênero é gravado
com a **soma** das quantidades e dos valores (RN-07), e não com o que foi digitado.

Cada uma dessas gravações vai para a auditoria (`A010T`), com a operação, o cadastro
mexido, a sessão (a matrícula, o código de acesso e o privilégio), o grupo, a estação de
trabalho, a data e a hora, o tipo de órgão e as imagens anterior e nova do registro.

### RN-16 — O acumulado do convênio do fornecedor acompanha os gêneros

O convênio do fornecedor tem um **acumulado por secretaria, grupo, instituição
beneficente, ano de competência e fornecedor** — com o valor dos gêneros, o valor das
notas, o valor do desconto e o valor dos recursos próprios. Cada gênero que esta tela
inclui, altera ou exclui regrava o acumulado do recorte da nota; e, quando a nota fica sem
gêneros, o acumulado dela é refeito ou apagado junto com a nota.

[?] A conta que a tela faz nesse acumulado, ao mexer num gênero, é **o valor do gênero
gravado menos o acumulado, mais o valor novo** do gênero — o acumulado entra subtraindo, e
não somando e descontando o gênero. Com mais de um gênero no mesmo convênio, o acumulado
só fecha se o que já estava lá for exatamente o valor daquele gênero. Se a conta deveria
ser o acumulado menos o valor antigo mais o valor novo, pergunta ao site.

### RN-17 — O desconto da nota é rateado entre os gêneros

Terminada a resposta, se a operação foi a de incluir ou a de alterar e não houve recusa, a
tela **reparte o desconto da nota entre os gêneros**: calcula quanto o desconto representa
do total dos gêneros e grava, em cada gênero da nota, a parte do desconto que lhe cabe. O
gênero de **maior valor** fica de fora dessa conta e recebe o **resto** do rateio, para que
a soma das partes feche com o desconto da nota.

### RN-18 — Tirando o último gênero, a nota é apagada e o servidor volta à capa

Quando a soma dos gêneros da nota fica zerada — o último gênero saiu —, a tela apaga o
acumulado do convênio da nota, apaga a nota e apaga os gêneros dela, deixando rastro na
auditoria, e devolve o servidor à **capa da nota**, já em **inclusão**, pronta para uma
nota nova (o número da nota vai em branco). Nesse caminho o servidor não vê aviso nenhum.

### RN-19 — Sem a secretaria e o grupo da sessão a gravação não acontece, e a tela não avisa

A gravação só acontece quando a sessão tem **secretaria** (o tipo de órgão) e a nota tem
**grupo**. Faltando um dos dois, a tela não grava, não avisa nada e devolve o servidor à
**capa da nota**.

### RN-20 — A consulta não grava nada

Na **consulta** — que é a operação com que a tela abre vinda da lista de notas —, a tela
mostra os gêneros já lançados e não grava, não altera, não apaga e não trava nada: nem a
nota, nem os gêneros, nem o acumulado do convênio, e nenhum registro de auditoria é
gerado, ainda que o servidor mude o que está vendo na tela. A consulta também não reparte
o desconto.

### RN-21 — A abertura e cada resposta passam pelas conferências comuns

A abertura passa pela conferência de **acesso**: a tela tem de estar cadastrada no cadastro
de telas e o código de acesso de quem opera tem de ter a tela liberada — não tendo, a tela
é abandonada com **\* Tela nao cadastrada \***, **\* Tela nao disponivel \*** ou **\*
Acesso negado para esta matricula \***, e nada é mostrado. Cada resposta passa pela
conferência de **rota** — a tela cadastrada e a operação admitida — e pela conferência de
**permissão** — a operação liberada no perfil da tela —, e a data e a hora do sistema, que
são usadas em cada gravação, vêm da mesma família de conferências. As conferências recebem
o contexto da sessão: a matrícula, o código de acesso, o privilégio, a secretaria e o
grupo, além da operação e da tela.

### RN-22 — Os campos de número são editados a cada resposta

A cada resposta, antes de qualquer conferência, a tela edita os seus **20 campos de
número**: o número da nota fiscal, o grupo, o dia, o mês e o ano de emissão, o dia, o mês e
o ano da nota, o ano de competência, o número e o ano do convênio, o código da instituição
beneficente, o valor total da nota, o desconto, o total dos gêneros, o valor que falta
lançar e, por gênero, o código, a quantidade, o preço unitário e o valor total do item.
Cada um é tratado como número — o que estiver em branco vira zero e os zeros à esquerda
caem — e reescrito; os valores em dinheiro usam a vírgula como separador decimal. No
primeiro campo que não passar pela edição, o cursor volta para ele e a tela não segue.

[?] A tela aponta o cursor por duas contas diferentes para o mesmo campo e a mesma linha:
quando quem recusa é a **edição** do campo, a conta é de **sete** linhas por gênero; quando
quem recusa é uma **regra de negócio** — gênero não cadastrado, unidade, valor —, a conta é
de **seis** linhas por gênero. Para o mesmo campo, as duas posições não coincidem. Uma das
duas está errada. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Lançar os gêneros da nota fiscal de desconto e repartir o desconto entre eles

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F153T

  Cenário: A tela abre em inclusão, vinda da capa, para lançar os gêneros de uma nota nova
    Dado que confirmei a inclusão de uma nota na capa da nota
    Quando a tela dos gêneros abre
    Então ela está em inclusão
    E as linhas de gênero vêm em branco
    E os dados da nota que eu digitei na capa aparecem aqui
    E nada é gravado

  Cenário: A tela abre em consulta, vinda da lista de notas, e mostra os gêneros já lançados
    Dado que selecionei uma nota na lista de notas
    Quando a tela dos gêneros abre
    Então ela está em consulta
    E vejo os gêneros já lançados naquela nota, um por linha, até oito
    E nada é gravado

  Cenário: A tela aberta por outra origem devolve ao menu de despesas
    Dado que chego a esta tela por um caminho que não é a capa da nota nem a lista de notas
    Quando a tela dos gêneros é chamada
    Então sou devolvido ao menu de despesas
    E nada é gravado

  Cenário: A operação de exclusão não é aceita nesta tela
    Dado que a tela abre com a operação de exclusão
    Quando respondo a tela
    Então vejo "* Opcao nao disponivel. Use INC, ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: A nota mostrada é a que a tela anterior deixou
    Dado que a capa da nota me passou o número, o grupo, as datas e os valores da nota
    Quando a tela dos gêneros abre
    Então vejo esses mesmos dados da nota
    E vejo o total dos gêneros e o que ainda falta lançar

  Cenário: Nota sem gêneros é avisada
    Dado que a nota informada não tem nenhum gênero lançado
    Quando a tela dos gêneros abre
    Então vejo "* Nota fiscal sem generos cadastrados *"
    E as linhas de gênero vêm em branco
    E nada é gravado

  Cenário: Lançar um gênero novo na nota
    Dado que informei o código de um gênero cadastrado, a unidade de medida válida para ele, a quantidade e o valor total do item
    E marquei a linha para incluir
    Quando respondo a tela
    Então o gênero passa a fazer parte da nota
    E o preço unitário do gênero fica com o valor dividido pela quantidade
    E o total dos gêneros da nota é refeito
    E a auditoria registra a gravação

  Cenário: Lançar um gênero que já está na nota soma ao que já estava
    Dado que informei o código de um gênero que já está lançado nesta nota
    E informei a quantidade e o valor total do item
    E marquei a linha para incluir
    Quando respondo a tela
    Então o gênero fica com a quantidade que já estava mais a que informei
    E fica com o valor que já estava mais o que informei
    E não aparece uma segunda linha para o mesmo gênero

  Cenário: Linha sem ação é ignorada
    Dado que preenchi um gênero na linha e deixei a ação da linha em branco
    Quando respondo a tela
    Então aquela linha não é lançada
    E não vejo aviso nenhum
    E nada é gravado

  Cenário: Alterar um gênero já lançado
    Dado que informei o código de um gênero que está lançado nesta nota
    E informei a nova quantidade e o novo valor total do item
    E marquei a linha para alterar
    Quando respondo a tela
    Então o gênero fica com a quantidade e o valor que informei
    E o preço unitário é recalculado
    E a auditoria registra a alteração

  Cenário: Excluir um gênero já lançado
    Dado que informei o código de um gênero que está lançado nesta nota
    E marquei a linha para excluir
    Quando respondo a tela
    Então o gênero sai da nota
    E o total dos gêneros da nota é refeito
    E a auditoria registra a exclusão

  Cenário: Alterar ou excluir um gênero que não está na nota
    Dado que informei o código de um gênero que não está lançado nesta nota
    E marquei a linha para alterar ou para excluir
    Quando respondo a tela
    Então vejo "* Cod.FNDE nao cadastrado nesta nota *"
    E o cursor volta ao campo do código do gênero
    E nada é gravado

  Cenário: Gênero não cadastrado
    Dado que informei o código de um gênero que não existe no cadastro dos gêneros
    E marquei a linha para incluir
    Quando respondo a tela
    Então vejo "* Cod.FNDE nao cadastrado *"
    E o cursor volta ao campo do código do gênero
    E nada é gravado

  Cenário: Unidade de medida que não vale para o gênero
    Dado que informei um gênero cadastrado e uma unidade de medida que não está cadastrada para ele
    Quando respondo a tela
    Então vejo "* Unid.medida nao cad. para este cod.FNDE *"
    E o cursor volta ao campo da unidade de medida
    E nada é gravado

  Cenário: Quantidade não informada
    Dado que informei o gênero e a unidade, e deixei a quantidade zerada
    Quando respondo a tela
    Então vejo "* Informe a quantidade *"
    E o cursor volta ao campo da quantidade
    E nada é gravado

  Cenário: Valor total do item não informado
    Dado que informei o gênero, a unidade e a quantidade, e deixei o valor total do item zerado
    Quando respondo a tela
    Então vejo "* Informe o valor total do item na nota *"
    E o cursor volta ao campo do valor total do item
    E nada é gravado

  Cenário: Preço unitário zerado
    Dado que informei um valor total do item que não dá preço unitário para a quantidade informada
    Quando respondo a tela
    Então vejo "* Preco unitario zerado *"
    E o cursor volta ao campo do valor total do item
    E nada é gravado

  Cenário: A soma dos gêneros passa do valor da nota mais o desconto
    Dado que o gênero que estou lançando faz a soma dos gêneros da nota passar do valor total da nota somado ao desconto dela
    Quando respondo a tela
    Então vejo "* Desconto - vl.itens > vl.nota *"
    E o cursor volta ao campo do valor total do item
    E nada é gravado

  Cenário: Sem permissão para a ação da linha
    Dado que o perfil da tela não libera incluir, alterar ou excluir
    E marquei uma linha com essa ação
    Quando respondo a tela
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: O desconto da nota é repartido entre os gêneros
    Dado que a nota tem desconto e mais de um gênero lançado
    Quando respondo a tela pedindo uma inclusão ou uma alteração
    Então cada gênero da nota fica com a parte do desconto que lhe cabe
    E o gênero de maior valor fica com o resto do rateio
    E a soma das partes fecha com o desconto da nota

  Cenário: O total dos gêneros da nota é refeito
    Dado que a nota tem gêneros lançados
    Quando respondo a tela pedindo uma inclusão ou uma alteração
    Então o valor total dos gêneros da nota fica com a soma de todos eles
    E o que falta lançar é refeito a partir do valor da nota, do desconto e dessa soma

  Cenário: O acumulado do convênio do fornecedor acompanha o gênero lançado
    Dado que lancei um gênero na nota
    Quando respondo a tela
    Então o acumulado do convênio do fornecedor daquele recorte é regravado
    E a auditoria registra a gravação

  Cenário: O acumulado do convênio do fornecedor acompanha o gênero excluído
    Dado que excluí um gênero da nota
    Quando respondo a tela
    Então o acumulado do convênio do fornecedor daquele recorte é regravado
    E a auditoria registra a gravação

  Cenário: Tirando o último gênero a nota é apagada e a tela volta à capa em inclusão
    Dado que a nota tem um único gênero
    E marquei esse gênero para excluir
    Quando respondo a tela
    Então o gênero, a nota e o acumulado do convênio dela são apagados
    E sou devolvido à capa da nota, já em inclusão, pronta para uma nota nova
    E nenhum aviso aparece

  Cenário: Sem a secretaria na sessão a gravação não acontece, e a tela não avisa
    Dado que a minha sessão não tem secretaria
    E pedi a inclusão de um gênero na nota
    Quando respondo a tela
    Então o gênero não é gravado
    E sou devolvido à capa da nota
    E não vejo aviso nenhum

  Cenário: Sem o grupo na nota a gravação não acontece, e a tela não avisa
    Dado que a nota não tem grupo
    E pedi a inclusão de um gênero na nota
    Quando respondo a tela
    Então o gênero não é gravado
    E sou devolvido à capa da nota
    E não vejo aviso nenhum

  Cenário: A consulta não grava nada
    Dado que a tela abriu em consulta e mostra os gêneros da nota
    E mudo a quantidade e o valor de um gênero mostrado na tela
    Quando respondo a tela pedindo a consulta
    Então a nota, os gêneros e o acumulado do convênio ficam como estavam
    E nenhum registro de auditoria é gerado
    E o desconto da nota não é repartido de novo

  Cenário: Campo de número recusado na edição
    Dado que informei letras em um dos campos de número da tela
    Quando respondo a tela
    Então a edição recusa aquele campo
    E o cursor volta ao campo recusado
    E a tela não segue
    E nada é gravado

  Cenário: A tela não consta do cadastro de telas
    Dado que a tela F153T não consta do cadastro de telas, ou está desativada
    Quando abro a tela F153T
    Então sou avisado de que a tela não está disponível
    E não consigo operar

  Cenário: Meu código de acesso não tem a tela
    Dado que o meu código de acesso não tem a tela F153T liberada
    Quando abro a tela F153T
    Então vejo "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: A operação informada não é a que o perfil libera
    Dado que o perfil da tela não libera a operação com que a tela abriu
    Quando respondo a tela
    Então vejo "* Acesso negado para esta operacao *"
    E nada é lido nem gravado
```
