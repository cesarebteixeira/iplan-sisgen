# US — E040T — Consulta dos pedidos de alimentação escolar do órgão e escolha do pedido a abrir

## Estória

Como **servidor de CRE**, quero **ver os pedidos de alimentação escolar do meu órgão e da
minha coordenadoria regional escolar e abrir o pedido que eu escolher**, para que **eu
encontre o pedido certo sem ter de digitar de memória a combinação que o identifica, e
chegue direto à tela em que ele é tratado**.

O pedido de alimentação escolar é identificado por um número, um ano de entrega, um órgão
e uma coordenadoria — combinação que ninguém decora. Antes de distribuir os gêneros,
acumular ou conferir um pedido, é preciso achá-lo. Esta tela é essa porta de entrada: ela
varre os pedidos do órgão e da coordenadoria da sessão e mostra, de cada um, o fornecedor,
a semana do cardápio, o período de entrega, o tipo de contrato e a situação, para que o
servidor reconheça o pedido e abra o certo.

Sem ela, o pedido ficaria inacessível a quem não sabe o número de cor — e é por ela que
passam as telas em que o pedido é distribuído e acumulado.

## Contexto

Jornada S000M → E000M → E010M → E040T.

Ator: servidor de CRE — confirma ou informa o órgão e a coordenadoria, percorre a grade dos
pedidos daquele órgão e marca a linha do pedido que quer abrir.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Da sessão a tela usa a matrícula, o código de acesso, o privilégio, a estação, a secretaria
(o tipo de órgão), a coordenadoria regional escolar e o órgão filho do vínculo, além da
descrição da secretaria e da data do sistema para o cabeçalho. Ela não termina em si mesma:
abre a tela do pedido — a de distribuição ou uma das duas de acumulação — e o que ela
entrega a essa tela é regra desta estória.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela só faz consulta

Esta tela só consulta. Ela se apresenta já com a consulta no campo da operação, e qualquer
outra operação é recusada com **\* Operacao nao disponivel. Use CON \***, com o cursor de
volta ao campo da operação, antes de qualquer leitura dos pedidos. Nessa recusa nada é
mostrado nem gravado: a grade não chega a ser montada.

[?] A mensagem manda usar "CON", e a tela só deixa passar quando o campo da operação casa
com o código interno da consulta — que é a própria tela que põe ali. O que o operador
digitaria para escolher a consulta, e se existe outra forma de informá-la, não está no
acervo lido. Pergunta ao site.

### RN-02 — A tela abre sem procurar pedido nenhum

Ao ser aberta, a tela não procura pedido: ela mostra no cabeçalho a data do sistema e a
descrição da secretaria da sessão, põe no órgão filho e na coordenadoria regional escolar
os valores do vínculo do servidor e lê o cadastro de órgãos apenas para exibir o nome
daquele órgão. O cursor começa no campo do órgão filho. O pedido só é procurado depois, para
montar a grade.

[?] A data do sistema e a descrição da secretaria são preenchidas na abertura e limpas a
cada digitação, sem que a tela as reponha. Se o ambiente comum as repõe antes de mostrar a
tela, o acervo lido não mostra. Pergunta ao site.

O comportamento da tela não muda conforme a tela que a chamou: ela não compara a sua origem
com código de tela nenhum. A única conferência que olha para quem a chamou é a do campo em
que a tela anterior pede a tela seguinte — e, vindo esse campo preenchido, esta tela não faz
nada.

[?] A tela só segue quando o campo da próxima tela está em branco, e nenhuma tela do caminho
o preenche antes de chamá-la. Se alguém o preenche em algum caminho do acervo, o acervo lido
não mostra, e a tela ficaria inerte. Pergunta ao site.

### RN-03 — Os campos numéricos passam por edição antes das conferências

Seis campos da tela são tratados como número: o órgão filho, a coordenadoria regional
escolar, o número do pedido, o ano da entrega e um segundo par de número do pedido e ano
que a tela usa para reposicionar a lista. O que estiver em branco vira zero, os zeros à
esquerda são descartados e o que não for número é recusado. Nenhuma conferência de pedido
acontece antes dessa edição.

[?] A rotina que faz a edição não faz parte do acervo lido, e a tela só tem posição de
cursor para quatro desses seis campos: a digitação recusada no número do pedido e no ano da
entrega não leva o cursor até eles. Também não se conclui do acervo se a edição interrompe o
processamento ou apenas corrige o valor e segue. Pergunta ao site.

### RN-04 — A grade mostra, onze por vez, os pedidos do órgão e da coordenadoria

A grade tem **onze linhas**, e cada linha mostra de um pedido: um asterisco quando o pedido
é acumulado, o número e o ano da entrega, o código do fornecedor e a razão social, a semana
do cardápio, o período de entrega — a data de início, um "a" e a data limite —, o tipo de
contrato e a situação, que aparece como **Aprovado** quando o pedido está aprovado e como
**Fechado** quando está aprovado e fechado.

A tela percorre os pedidos do órgão e da coordenadoria que ela tem no momento — os do
vínculo quando abre, os que o servidor informou depois — e **não mostra os pedidos pendentes
de distribuição**. Quando a primeira linha não acha nenhum pedido, a recusa é
**\* Orgao sem pedidos cadastrados \***, sem cursor em campo nenhum. Se o vínculo não traz
órgão filho e o servidor ainda não informou um, a grade não é montada.

[?] O asterisco do pedido acumulado e o tipo de contrato não são zerados de uma linha para
a outra: achado um pedido acumulado, ou um gênero com tipo de contrato, as linhas seguintes
podem continuar exibindo a mesma marca. O acervo lido não diz se é assim de propósito.
Pergunta ao site.

[?] A tela guarda, ao terminar a décima primeira linha, o pedido seguinte, para continuar a
lista adiante. O acervo lido não mostra como essa continuação é pedida pelo servidor nem se
ela chega a refazer a grade a partir do pedido guardado. Pergunta ao site.

### RN-05 — O órgão filho é conferido contra o vínculo e contra o cadastro

Quando o vínculo do servidor traz um órgão filho, ele só pode trabalhar nesse órgão: se o
órgão informado for outro, a recusa é **\* Usuario sem acesso a outro orgao \***, com o
cursor no campo do órgão. Quando o vínculo não traz órgão, é o servidor que informa um; se
não informar, a recusa é **\* Informe o orgao \***, também com o cursor no campo do órgão.

O órgão informado ainda tem de estar no cadastro de órgãos: não estando, a recusa é
**\* Orgao nao cadastrado \***, com o cursor no campo do órgão. Nenhuma dessas recusas
grava ou apaga nada.

### RN-06 — A coordenadoria informada cede lugar à do cadastro do órgão

Informada uma coordenadoria, ela só prevalece quando o órgão tem pedido naquela
coordenadoria; quando não tem, a tela passa a usar a coordenadoria do cadastro do órgão e
remonta a grade por ela — a coordenadoria digitada é descartada. O servidor cujo vínculo já
traz coordenadoria não consegue trabalhar em outra: a recusa é
**\* Usuario sem acesso ao grupo deste Orgao \***, com o cursor no campo do órgão.

### RN-07 — O pedido que ficou sem nenhum gênero é apagado do cadastro

Enquanto monta a grade, a tela percorre os gêneros de cada pedido que exibe. Se o pedido não
tem nenhum gênero cadastrado, ele é **apagado do cadastro** — não é só um efeito de tela —,
e deixa de aparecer. Esse apagamento não deixa registro de auditoria: esta tela não escreve
no cadastro de auditoria.

[?] O apagamento acontece durante a simples exibição da grade, antes de o servidor escolher
qualquer coisa. Se a tela terminar recusando — por exemplo por não haver pedido na
coordenadoria informada —, o apagamento já foi feito. O acervo lido não diz se a transação é
desfeita quando a tela termina com recusa. Pergunta ao site.

### RN-08 — Marcar a linha abre o pedido dela

Para abrir um pedido, o servidor marca a linha dele na coluna de ação com "X". A tela então
lê o pedido pelo número e pelo ano daquela linha, com a coordenadoria que está usando, e o
abre.

Três recusas caem antes de abrir, todas com o cursor no campo de ação da linha marcada e
sem abrir nada. Linha marcada e vazia dá **\* A linha deve estar preenchida \***; pedido que
não é do órgão do vínculo dá **\* Usuario sem acesso a este orgao \***; e pedido cujos
gêneros estão todos marcados como excluídos dá
**\* Pedido sem generos cadastrados \***.

[?] A tela guarda, na área de trabalho, um par de anos para saber se já passou pela primeira
linha, e é essa marca que decide se a linha marcada é tratada: no primeiro passo de cada
transação ela é consumida pela própria marca, de modo que uma linha "X" na primeira linha da
grade pode não abrir nada. Se é defeito ou se o ambiente a repõe antes, o acervo lido não
fecha. Pergunta ao site.

[?] Ao abrir o pedido, a tela lê também o cadastro do operador que digitou o pedido, para o
nome dele, e não o exibe em campo nenhum da tela. Se o nome deveria aparecer, o acervo lido
não mostra onde. Pergunta ao site.

### RN-09 — A tela que abre depende do indicador de acumulação do pedido

Aberto o pedido, a tela o entrega à tela de distribuição dos gêneros — a E021T. Se o pedido
for um pedido acumulado, ela entrega a uma das duas telas de acumulação — a E221T ou a
E231T —, conforme o indicador de acumulação que o pedido tem gravado.

[?] O indicador de acumulação tem dois valores, e cada um abre uma tela diferente, mas o
acervo lido não permite dizer com segurança o que cada valor significa para o negócio.
Pergunta ao site.

### RN-10 — O que a tela entrega à tela seguinte

A tela não abre a seguinte por menu: ela mesma a chama — a E021T, a E221T ou a E231T,
conforme a RN-09 — e entrega a operação de **consulta** junto com a identificação do pedido:
o órgão filho, a coordenadoria regional escolar, o número do pedido e o ano da entrega da
linha marcada. A tela de distribuição, por sua vez, só atende a transação quando ela vem da
tela do pedido ou desta tela — qualquer outra origem é devolvida ao menu.

[?] As duas telas de acumulação procuram, na área de trabalho delas, o pedido acumulado a
que se referem, e não se vê, no acervo lido, quem preenche essa área quando a chamada vem
desta tela. Se ela não for preenchida, o pedido pode não ser encontrado pela tela seguinte.
Pergunta ao site.

### RN-11 — Sem autorização para a tela ou para a operação, nada acontece

A tela só abre para o código de acesso que a tem no cadastro de telas por código de acesso;
não tendo, a recusa é **\* Acesso negado para esta matricula \***. E, antes de qualquer
leitura de pedido, a operação informada tem de estar liberada para aquele código de acesso
naquela tela; não estando, a recusa é **\* Acesso negado para esta operacao \***. Nos dois
casos nada é mostrado nem gravado.

[?] O cadastro de telas por código de acesso guarda, separadamente, a liberação da consulta,
e nenhuma rotina do acervo lido compara esse campo: a consulta entra sem essa conferência, e
só a operação de manutenção que o servidor informe por engano é que passa por ela (e é
recusada, de todo modo, pela RN-01). Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta dos pedidos de alimentação escolar do órgão e escolha do pedido a abrir

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E040T

  Cenário: Abrir a tela e ver a grade dos pedidos do meu órgão
    Dado que existem pedidos do meu órgão e da minha coordenadoria
    Quando abro a tela E040T
    Então vejo no cabeçalho a data do sistema, a descrição da secretaria e o nome do
      meu órgão
    E vejo até onze linhas, cada uma com o número e o ano da entrega de um pedido, o
      fornecedor, a semana, o período de entrega, o tipo de contrato e a situação
    E o cursor fica no campo do órgão filho
    E nenhum pedido foi procurado, gravado ou apagado por causa da abertura

  Cenário: O asterisco marca o pedido acumulado
    Dado que um dos pedidos da grade é um pedido acumulado
    Quando abro a tela E040T
    Então a linha desse pedido traz um asterisco
    E as linhas dos pedidos não acumulados não trazem

  Cenário: A situação do pedido na grade
    Dado que um pedido da grade está aprovado e outro está aprovado e fechado
    Quando abro a tela E040T
    Então o primeiro mostra a situação "Aprovado"
    E o segundo mostra a situação "Fechado"

  Cenário: Pedido pendente de distribuição não aparece na grade
    Dado que existe um pedido do meu órgão e da minha coordenadoria pendente de
      distribuição
    Quando abro a tela E040T
    Então esse pedido não aparece em nenhuma linha da grade

  Cenário: Órgão sem pedidos cadastrados
    Dado que o meu órgão e a minha coordenadoria não têm nenhum pedido
    Quando abro a tela E040T
    Então vejo "* Orgao sem pedidos cadastrados *"
    E a grade fica vazia

  Cenário: Sem órgão filho no vínculo a grade não é montada
    Dado que o meu vínculo não tem órgão filho
    Quando abro a tela E040T
    Então o campo do órgão fica em branco, para eu informar
    E o cursor fica no campo do órgão
    E nenhum pedido é procurado, gravado ou apagado

  Cenário: Marcar a linha e abrir o pedido
    Dado que estou na tela E040T, com a grade montada
    Quando marco com "X" a linha de um pedido da minha coordenadoria
    Então a tela abre o pedido daquela linha
    E a operação que segue com o pedido é a consulta

  Cenário: Marcar uma linha vazia
    Dado que estou na tela E040T, com a grade montada
    Quando marco com "X" uma linha sem pedido
    Então vejo "* A linha deve estar preenchida *"
    E o cursor fica no campo de ação daquela linha
    E nenhum pedido é aberto

  Cenário: Pedido de outro órgão
    Dado que marco um pedido que não é do órgão do meu vínculo
    Quando confirmo
    Então vejo "* Usuario sem acesso a este orgao *"
    E o cursor fica no campo de ação da linha
    E nenhum pedido é aberto

  Cenário: Pedido cujos gêneros estão todos excluídos
    Dado que todos os gêneros do pedido marcado estão marcados como excluídos
    Quando confirmo
    Então vejo "* Pedido sem generos cadastrados *"
    E o cursor fica no campo de ação da linha
    E nenhum pedido é aberto

  Cenário: O indicador de acumulação decide a tela seguinte
    Dado que marco um pedido acumulado com um dos dois valores do indicador
    Quando confirmo
    Então a tela abre a tela de acumulação que corresponde àquele valor
    Quando marco um pedido acumulado com o outro valor do indicador
    Então a tela abre a outra tela de acumulação
    Quando marco um pedido sem indicador de acumulação
    Então a tela abre a tela de distribuição dos gêneros

  Cenário: Operação diferente da consulta
    Quando informo uma opção diferente da consulta
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E a grade não é montada e nada é gravado

  Cenário: A consulta não grava nada
    Dado que abri a tela, percorri a grade e não marquei nenhuma linha
    Quando a tela termina a passagem
    Então nenhum cadastro foi incluído, alterado ou apagado por isso
    E nenhum registro de auditoria foi gerado

  Cenário: O servidor não informa pedido de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo outro órgão e confirmo
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O órgão é obrigatório quando o vínculo não traz órgão
    Dado que o meu vínculo não tem órgão filho
    Quando confirmo sem informar o órgão
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão não cadastrado
    Dado que o meu vínculo não tem órgão filho
    Quando informo um órgão que não está cadastrado e confirmo
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: A coordenadoria digitada não sobrepõe a do cadastro do órgão
    Dado que o meu vínculo não tem coordenadoria
    Quando informo um órgão cadastrado em uma coordenadoria e digito outra
    Então a tela procura os pedidos pela coordenadoria do cadastro do órgão
    E a coordenadoria digitada é descartada

  Cenário: Órgão de outra coordenadoria
    Dado que o meu vínculo carrega uma coordenadoria
    Quando informo um órgão cadastrado em outra coordenadoria e confirmo
    Então vejo "* Usuario sem acesso ao grupo deste Orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: A tela apaga o pedido que ficou sem gênero
    Dado que existe um pedido do meu órgão e da minha coordenadoria sem nenhum gênero
    Quando abro a tela E040T
    Então esse pedido é apagado do cadastro
    E ele não aparece em nenhuma linha da grade
    E o apagamento não deixa registro de auditoria

  Cenário: A edição numérica dos campos
    Dado que estou na tela E040T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências
    E a digitação que não é número é barrada antes das conferências do pedido

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem esta tela no cadastro de telas por código
      de acesso
    Quando abro a tela E040T
    Então vejo "* Acesso negado para esta matricula *"
    E nada é mostrado nem gravado

  Cenário: Sem autorização para a operação informada
    Dado que informo uma operação de manutenção no campo da operação
    E o meu código de acesso não tem essa operação liberada nesta tela
    Quando confirmo
    Então vejo "* Acesso negado para esta operacao *"
    E nada é mostrado nem gravado

  Cenário: A recusa não grava nem apaga nada
    Dado que a minha passagem foi recusada por alguma conferência
    Quando a tela termina a passagem
    Então nenhum cadastro foi incluído, alterado ou apagado por causa dela
    E nenhum registro de auditoria foi gerado
```
