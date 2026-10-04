# US — N024T — Lançamento dos gêneros da nota fiscal

## Estória

Como **servidor de CRE**, quero **lançar os gêneros que compõem a nota fiscal —
quantidade e preço de cada um, contra o pedido e o contrato que os autorizam — e
conferir o que já está lançado**, para que **a nota deixe de ser só um cabeçalho, a
despesa fique registrada item a item e o pedido e o contrato recebam de volta o que a
nota consome**.

A nota fiscal só passa a existir de verdade depois desta tela: o cabeçalho vem da tela
anterior, mas é aqui que a nota é gravada e que cada gênero entra com a sua quantidade,
o seu preço e o seu pedido. É por isso que o pedido, o contrato e o recebimento da nota
só andam quando um item é lançado — e é por aqui que o lançamento errado se desfaz,
devolvendo ao pedido e ao contrato o que a nota tinha comprometido. Sem esta tela, a
nota ficaria sem itens e o valor não chegaria a lugar nenhum.

## Contexto

Jornada S000M → N000M → N050M → N014T → N024T (5 passos).
Ator: servidor de CRE — lança, corrige e exclui os gêneros da nota fiscal e confere os
que já estão lançados.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Das telas anteriores, o `N000M` e o `N050M` são menus e não deixam nada de próprio: o
que esta tela usa da sessão — a matrícula, o código de acesso, o privilégio, o tipo de
órgão (a secretaria) e a coordenadoria regional escolar — é o que a entrada deixou. A
`N014T` **não é menu**: é a tela do cabeçalho da nota, e encadeia nesta sem passar por
menu nenhum, entregando a nota e a operação. É essa entrega que abre esta tela no modo
certo e sobre a nota certa (RN-05).

---

## Regras de negócio

### RN-01 — A tela lança os gêneros da nota, e é aqui que a nota é gravada

A tela mostra o cabeçalho da nota que recebeu — número, os dois trios de data, a
coordenadoria regional escolar, o pedido, o ano da entrega, o tipo de contrato, o
fornecedor e a sua razão social, o órgão filho e o nome dele, o operador e o nome dele,
a chave de acesso, o total da nota, o total do IR e a marca de pedido acumulado — e,
abaixo dele, **oito linhas de item**. Cada linha traz o código de subclasse, o código de
gênero (com a descrição resumida e a unidade de medida), a quantidade, o preço unitário,
o valor total, a operação da linha e a marca de pedido acumulado.

A confirmação da inclusão feita na tela do cabeçalho **não cria a nota**: é o primeiro
item lançado aqui que faz a nota existir, e é esta tela que passa a manter o total dela,
regravando-o pela soma dos itens (RN-14).

### RN-02 — A tela só prossegue quando a área de trabalho traz a N014T como origem

Antes de qualquer regra de negócio, a tela confere de onde veio: só segue se a área de
trabalho que ela recebeu trouxer a tela do cabeçalho da nota identificada como origem.
Vinda de qualquer outro lugar, ela leva o servidor ao menu da nota fiscal, que mostra
**\* Acesso deve ser feito pela tela N014T \*** e o encaminha à tela do cabeçalho.

É assim que as telas que encadeiam aqui escrevem essa origem antes de chamar: quem
entrega a nota a esta tela se identifica como a tela do cabeçalho, mesmo sendo outra.
Sem isso, o encadeamento não anda.

### RN-03 — A tela trabalha em inclusão, alteração e consulta, e cada linha tem a sua operação

A operação da tela é inclusão, alteração ou consulta. Qualquer outra coisa é recusada
com **\* Opcao nao disponivel. Use INC, ALT ou CON \***, com o cursor no campo da
operação, e nada é gravado.

Além da operação da tela, **cada linha carrega a sua própria operação**: incluir,
alterar ou excluir. A linha sem gênero informado não faz nada — nem confere, nem grava.
E é a operação da linha que decide qual manutenção acontece e qual permissão é conferida
para ela (RN-04).

### RN-04 — Nada anda sem a conferência da sessão, da tela e das permissões

Toda passagem pela tela passa por três conferências, nesta ordem: a **sessão** (o
servidor tem de estar cadastrado e a estação da sessão tem de ser a do cadastro dele), o
**registro da tela** (a tela tem de existir, e a tela marcada como excluída não passa) e
a **permissão da tela e da operação** no cadastro de acesso por tela.

A operação declarada decide qual permissão é conferida: inclusão pede a permissão de
incluir, alteração a de alterar, exclusão a de excluir. E a operação de **cada linha**
passa por uma segunda conferência de permissão, com a mesma regra, antes de a linha ser
tratada.

Falhando qualquer uma delas: a tela que não existe, ou marcada como excluída, é recusada
com * Tela nao disponivel *; a falta de permissão para a tela, com * Acesso negado para
esta matricula *; a falta de permissão para a operação, com * Acesso negado para esta
operacao *; a operação que a rota não conhece, com * Operacao nao disponivel *. A sessão
que não bate com o cadastro do servidor não dá mensagem: devolve a sessão ao menu e, sem
matrícula, à entrada.

### RN-05 — O que a tela recebe e o que ela devolve

Da tela do cabeçalho a tela recebe **a nota e a operação**: o número, o modelo, as duas
datas, o fornecedor e a razão social, a coordenadoria regional escolar, o tipo de
contrato, o pedido, o ano da entrega, o órgão filho e o nome dele, o operador e o nome
dele, a chave de acesso, o total da nota, o total do IR, a marca de pedido acumulado e o
número do processo. É isso que a abre em **inclusão** (para lançar os itens de uma nota
nova), em **alteração** (para continuar o lançamento) ou em **consulta** (para mostrar
os itens). Em alteração e em consulta, a tela lê o primeiro item já lançado na nota com
os códigos que vieram na área de trabalho, mostra-o, e é por ele que começa a leitura das
linhas.

De volta, a tela devolve à tela do cabeçalho os mesmos dados, para ela reabrir sobre a
mesma nota. Ela também:

- **reabre a si mesma** quando mostra a pergunta de confirmação da inclusão (RN-13);
- **passa à consulta do pedido acumulado** quando o servidor usa a marca de pedido
  acumulado numa consulta (RN-11);
- **leva ao menu da nota fiscal** quando a origem não é o cabeçalho (RN-02);
- **devolve ao cabeçalho, sem mensagem**, quando a nota chega sem a coordenadoria
  regional escolar ou sem o pedido: não há item a tratar e nada é gravado.

### RN-06 — O gênero da linha tem de existir no cadastro e não pode repetir na nota

O gênero informado na linha é procurado no cadastro de gêneros e, antes disso, na
própria nota. As recusas, com o cursor de volta na linha:

- gênero que a nota já tem lançado, quando a operação da linha é incluir →
  **\* Genero ja cadastrado nesta nota \***;
- gênero que não existe no cadastro → **\* Genero nao cadastrado \***;
- gênero que a nota não tem lançado, quando a operação da linha é alterar ou excluir →
  **\* Genero nao cadastrado nesta nota \***;
- nota sem nenhum gênero lançado, quando a tela é aberta em alteração ou em consulta →
  **\* Nota fiscal sem generos cadastrados \***.

### RN-07 — A quantidade é obrigatória e tem de respeitar a fração do gênero

A quantidade do item não pode ser zero: sem ela, a recusa é **\* Informe a quantidade
\***, com o cursor na quantidade.

E a quantidade tem de ser um múltiplo da fração em que aquele gênero é comprado — a
fração vem do cadastro de gêneros. Quantidade que não fecha nessa fração é recusada com
**\* Quant. fracionada invalida para este genero \***, também com o cursor na
quantidade.

### RN-08 — O preço do item vem do contrato ou da tabela de preços, e não pode passar dela

O preço unitário do item tem dois caminhos, escolhidos pelo contrato:

- quando o contrato fixa o preço, é esse preço fixo que vale, e a tela o preenche
  sozinha quando o campo chega em branco;
- quando não fixa, o preço vem da **tabela de preços** vigente na data da nota — a
  tabela que o tipo de contrato indicar —, e a tela também o preenche quando o campo
  chega em branco.

O preço digitado é **teto**: ele não pode passar do preço da tabela acrescido do
percentual do contrato, e passar é recusado com **\* Preco unitario maior que o da
tabela \***, com o cursor no preço unitário.

Sem tabela de preços que cubra a data da nota, o item não entra: **\* Tabela de precos
nao cadastrada \***. Com a tabela vigente mas o gênero sem preço nela — linha ausente ou
preço zerado —, a recusa é **\* Genero sem cotacao na tabela de precos \***. Nas duas o
cursor volta para a linha do gênero, e nada é gravado.

O valor total do item é a quantidade multiplicada pelo preço unitário.

### RN-09 — O item é lançado contra um pedido aprovado, e o gênero tem de estar nele

O pedido informado no cabeçalho é procurado; não achado, a recusa é **\* Pedido invalido
\***, com o cursor no número do pedido. Achado, o gênero do item tem de estar naquele
pedido; não estando, a recusa é **\* Genero nao cadastrado neste pedido \***.

Com o pedido e o gênero achados, o item só entra se o pedido estiver em condições de
receber:

| o que a tela encontra | o que o servidor vê |
| --- | --- |
| o item do pedido ainda não liberado | * Pedido nao aprovado * |
| o item do pedido já recebeu tudo o que pedia | * Genero fechado neste pedido * |
| o item do pedido é de outro tipo de contrato | * Genero em outro tipo contrato no pedido * |
| a quantidade lançada passa do que o pedido ainda aguarda | * Quantidade excede a solicitada no pedido * |

Todas devolvem o cursor à linha do gênero, e nada é gravado.

Lançado o item, é esta tela que acerta a situação do pedido e do item dele: o item volta
a **aberto** enquanto faltar receber e fica **fechado** quando recebeu tudo; o pedido
fica **fechado** quando todos os itens dele estiverem fechados e volta a **aberto** se
algum não estiver. Excluir ou reduzir um item devolve ao pedido a quantidade que a nota
tinha recebido.

### RN-10 — A compra não pode passar do que o contrato ainda autoriza

O contrato que o item consome é procurado pelo tipo de órgão, pelo tipo de contrato,
pelo fornecedor, pela coordenadoria regional escolar, pelo gênero e pela data de início
do contrato que cobre a data da nota. Sem esse contrato para o meu grupo — ou com o
gênero fora dele —, a recusa é **\* Genero sem permissao de compra \***.

Duas outras conferências barram o item antes de comprar:

- a permissão do contrato do pedido e a da nota têm de ser as mesmas — o contrato achado
  pela data da nota e o achado pelo pedido têm de começar na mesma data; diferentes, a
  recusa é **\* Permissao do pedido difere da nota \***;
- contrato que começou depois de **30/04/2005** sem número de pedido no item é recusado
  com **\* Informe o numero do pedido \***.

Achado o contrato, ele fixa o quanto ainda pode ser comprado naquele gênero. A tela soma
ao que o item consome o que o contrato já tem comprometido e recusa quando passa:

- quantidade acima do autorizado → **\* Quantidade excede a permitida para compra \***;
- valor acima do autorizado → **\* Valor excede o permitido para compra \***.

Nas recusas o cursor volta à linha do gênero (na do valor, ao valor total), e nada é
gravado. Passando, a tela soma ao contrato a quantidade e o valor do item — e os devolve
ao contrato quando o item é reduzido ou excluído.

### RN-11 — A marca de pedido acumulado na linha

A linha tem uma marca de **pedido acumulado**, que o servidor preenche para tratar o
item pelo acúmulo. Com a marca preenchida, a tela decide pelo tipo de acúmulo do pedido:

- pedido que não é de acúmulo nenhum → **\* Pedido nao acumulado \***;
- pedido do acúmulo que o servidor digita → **\* Pedido acumulado digitado \***;
- pedido do acúmulo já calculado → só em **consulta**: a tela passa à tela da consulta
  da nota e dos pedidos que a compõem (`N124C`). Fora da consulta, a recusa é
  **\* Use somente com opcao CON \***.

Sem a marca, a linha segue o caminho normal de lançamento.

O item cujo pedido é de acúmulo, mas cujo gênero não entrou no acúmulo, é recusado no
lançamento comum com **<- Genero de pedido acumulado \***: o caminho dele é o do pedido
acumulado. E quando o pedido é do acúmulo já calculado, a tela trata também o pedido do
órgão ligado a ele — dando baixa na quantidade recebida por órgão e no recebimento
acumulado da nota.

[?] O acervo distingue duas formas de acúmulo — a que já foi calculada e a que ainda
não —, e cada uma segue por um caminho diferente de gravação, mas o que cada forma
significa no negócio não está escrito em lugar nenhum do programa nem do dicionário. O
que se lê é a tela dar baixa em quantidades diferentes conforme a forma. Pergunta ao
site.

### RN-12 — O que os órgãos já pediram barra a redução e a exclusão do item; a nota de devolução barra a exclusão

Reduzir a quantidade de um item abaixo do que os órgãos já pediram naquele acúmulo é
recusado com **\* Quant.pedida pelos Orgaos > quant.da nota \***.

Excluir um item é recusado em dois casos, com o cursor na linha do gênero:

- o item tem quantidade pedida pelos órgãos registrada → **\* Ja existem quant. pedidas
  pelos Orgaos \***;
- o item está em uma nota de devolução → **\* <- Genero em nota de devolucao \***.

Passando as duas, a exclusão apaga o item, devolve ao acúmulo e ao pedido do órgão as
quantidades que ele consumia e apaga o registro de recebimento acumulado da nota.

### RN-13 — A inclusão pergunta, e só grava com "S"

Passando por todas as conferências, a inclusão **ainda não grava**: a tela mostra
**\*Confirma inclusao <S/N>?*\** e reabre a si mesma com a pergunta. A resposta é "S".
Qualquer outra resposta, inclusive em branco, **cancela a confirmação sem mensagem** e
nada é gravado. Só com a confirmação pendente e respondida é que a gravação acontece.

A alteração e a exclusão desta tela não perguntam: quem pergunta por elas é a tela do
cabeçalho, antes de entregar a nota.

### RN-14 — A tela acerta o total da nota e o IR, e apaga a nota que ficou sem itens

Antes de encerrar a operação, em inclusão e em alteração, a tela soma os itens da nota e
compara com o total gravado:

- soma **zero** → a nota é **apagada**;
- soma diferente do total gravado → a nota é regravada com a soma dos itens.

O **total do IR** da nota é o total da nota multiplicado pela alíquota do tipo de
contrato, e só a partir de **18/10/2021**: nota anterior a essa data não tem IR nesta
tela. Alíquota zerada também deixa o IR zerado. Quando o IR da nota muda, a tela regrava
o IR de cada item da nota e acerta o total do IR dela.

[?] Os itens regravados no acerto do IR, e o campo de valor que a tela regrava no fim da
inclusão e da alteração (ver o anexo), **não passam pela auditoria**: são as únicas
gravações desta tela sem registro. Se o acerto deveria ser auditado como as demais,
pergunta ao site.

### RN-15 — O que a tela grava, e o que fica registrado

A tela enxerga dezesseis cadastros — o registro das telas, a nota fiscal, o item da
nota, o item da nota por pedido do órgão, o pedido, o item do pedido, o recebimento
acumulado da nota, o contrato, o gênero, o tipo de contrato, as duas tabelas de preços, o
tipo de órgão, as notas de devolução, os itens das notas de devolução e a auditoria —
além do cadastro do servidor e do cadastro de acesso por tela, que as conferências de
abertura leem. Ela **escreve em oito**: grava e apaga a nota, grava e apaga o item da
nota, grava e apaga o item por pedido do órgão, grava e apaga o recebimento acumulado,
grava o pedido, grava o item do pedido e grava o contrato.

Cada gravação de negócio é precedida do registro de auditoria, com o cadastro auditado,
a operação, a matrícula, a estação, a data, a hora e o conteúdo do registro antes e
depois. As exceções são as gravações da RN-14.

Qualquer falha de banco na leitura ou na gravação interrompe a transação e vira o erro
do sistema, e o que já estava gravado não é desfeito.

### RN-16 — A consulta não grava nada

Em consulta a tela só mostra: ela carrega o cabeçalho e os itens da nota, linha a linha,
e **não grava nada** — nem o total da nota, nem o pedido, nem o contrato. É essa a
diferença que o servidor percebe entre consultar e lançar.

### RN-17 — A nota nova volta para a tela do cabeçalho

Quando a nota que a tela está tratando é uma **nota nova**, ela volta para a tela do
cabeçalho em modo de inclusão e com o número da nota zerado, para uma nota nova ser
começada.

[?] A marca de "nota nova" é um campo da tela que o programa **só limpa**: ele nunca a
preenche. Se a marca deveria vir do ambiente ou de quem chama a tela, ou se esse caminho
de volta ficou inalcançável, não está no programa. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Lançamento dos gêneros da nota fiscal pelo N024T

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N024T

  Cenário: RN-01 — a tela mostra o cabeçalho recebido e as oito linhas de item
    Dado que a tela do cabeçalho me entregou uma nota com o número, as datas, o fornecedor, o pedido e o contrato
    Quando abro a tela N024T
    Então vejo o cabeçalho da nota que recebi
    E vejo oito linhas de item, cada uma com subclasse, gênero, quantidade, preço unitário, valor total e operação

  Cenário: RN-01 — o primeiro item lançado é que faz a nota existir
    Dado que confirmei a inclusão na tela do cabeçalho
    Quando lanço o primeiro gênero da nota e confirmo
    Então a nota passa a existir com esse item
    E o total da nota passa a ser a soma dos itens dela

  Cenário: RN-02 — vinda de outra tela, a tela desvia o acesso
    Dado que chego à tela N024T sem que a área de trabalho traga a tela do cabeçalho como origem
    Quando a tela é aberta
    Então sou levado ao menu da nota fiscal
    E vejo "* Acesso deve ser feito pela tela N014T *"
    E o menu me encaminha à tela do cabeçalho

  Cenário: RN-03 — operação que a tela não conhece
    Dado que estou na tela N024T
    Quando peço uma operação que não é inclusão, alteração nem consulta
    Então vejo "* Opcao nao disponivel. Use INC, ALT ou CON *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: RN-03 — cada linha carrega a sua operação
    Dado que estou na tela N024T com a nota já lançada
    Quando informo em uma linha o gênero e a operação de alterar
    Então é a alteração daquela linha que a tela trata
    E a permissão conferida é a de alterar

  Cenário: RN-03 — linha sem gênero não faz nada
    Dado que estou na tela N024T
    Quando deixo as duas colunas de código de uma linha em branco e confirmo
    Então nada é conferido para essa linha
    E nada é gravado por ela

  Cenário: RN-04 — sem permissão para a operação da linha
    Dado que o meu código de acesso não tem a permissão da operação que informei em uma linha
    Quando confirmo
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-04 — sem permissão para a tela
    Dado que o meu código de acesso não tem esta tela
    Quando abro a tela N024T
    Então vejo "* Acesso negado para esta matricula *"
    E nada é gravado

  Cenário: RN-04 — tela não cadastrada, ou excluída
    Dado que a tela N024T não existe no registro das telas, ou está marcada como excluída
    Quando abro a tela
    Então vejo "* Tela nao disponivel *"
    E nada é gravado

  Cenário: RN-04 — sessão que não bate com o cadastro do servidor
    Dado que a estação da minha sessão não é a do meu cadastro
    Quando confirmo
    Então a sessão é devolvida ao menu principal
    E nada é gravado

  Cenário: RN-05 — o modo como a tela abre vem de quem a chamou
    Dado que a tela do cabeçalho me entregou a nota e a operação
    Quando abro a tela N024T
    Então ela abre no mesmo modo e sobre a mesma nota
    E em alteração e em consulta ela começa pelo primeiro item que veio com a nota

  Cenário: RN-05 — nota sem coordenadoria regional escolar ou sem pedido volta ao cabeçalho
    Dado que a nota que recebi chegou sem a coordenadoria regional escolar ou sem o pedido
    Quando a tela vai tratar os itens
    Então ela me devolve à tela do cabeçalho
    E nenhuma mensagem aparece
    E nada é gravado

  Cenário: RN-06 — gênero já lançado na nota
    Dado que estou na tela N024T em inclusão
    Quando informo a operação de incluir em um gênero que a nota já tem lançado
    Então vejo "* Genero ja cadastrado nesta nota *"
    E o cursor volta à linha do gênero
    E nada é gravado

  Cenário: RN-06 — gênero não cadastrado
    Dado que estou na tela N024T
    Quando informo um gênero que não existe no cadastro de gêneros
    Então vejo "* Genero nao cadastrado *"
    E o cursor volta à linha do gênero
    E nada é gravado

  Cenário: RN-06 — gênero que a nota não tem
    Dado que estou na tela N024T em alteração ou em exclusão
    Quando informo um gênero que a nota não tem lançado
    Então vejo "* Genero nao cadastrado nesta nota *"
    E o cursor volta à linha do gênero
    E nada é gravado

  Cenário: RN-06 — nota sem gêneros lançados
    Dado que a nota não tem nenhum gênero lançado
    Quando abro a tela N024T em alteração ou em consulta
    Então vejo "* Nota fiscal sem generos cadastrados *"
    E nada é gravado

  Cenário: RN-07 — quantidade em branco
    Dado que estou na tela N024T lançando um gênero
    Quando confirmo sem informar a quantidade
    Então vejo "* Informe a quantidade *"
    E o cursor fica na quantidade
    E nada é gravado

  Cenário: RN-07 — quantidade fora da fração do gênero
    Dado que o gênero é comprado em fração
    Quando informo uma quantidade que não fecha nessa fração
    Então vejo "* Quant. fracionada invalida para este genero *"
    E o cursor fica na quantidade
    E nada é gravado

  Cenário: RN-08 — o preço que faltou vem do contrato ou da tabela
    Dado que estou na tela N024T lançando um gênero
    Quando deixo o preço unitário em branco e confirmo
    Então a tela preenche o preço com o preço fixo do contrato ou com o da tabela de preços vigente
    E o valor total passa a ser a quantidade multiplicada por esse preço

  Cenário: RN-08 — sem tabela de preços para a data da nota
    Dado que o contrato não fixa o preço
    E não há tabela de preços que cubra a data da nota
    Quando confirmo o item
    Então vejo "* Tabela de precos nao cadastrada *"
    E o cursor volta à linha do gênero
    E nada é gravado

  Cenário: RN-08 — gênero sem cotação na tabela de preços
    Dado que há tabela de preços para a data da nota
    E o gênero não tem preço nela
    Quando confirmo o item
    Então vejo "* Genero sem cotacao na tabela de precos *"
    E o cursor volta à linha do gênero
    E nada é gravado

  Cenário: RN-08 — preço acima do da tabela
    Dado que estou na tela N024T lançando um gênero
    Quando informo um preço unitário maior que o preço da tabela acrescido do percentual do contrato
    Então vejo "* Preco unitario maior que o da tabela *"
    E o cursor fica no preço unitário
    E nada é gravado

  Cenário: RN-09 — pedido inválido
    Dado que estou na tela N024T lançando um gênero
    Quando confirmo com um pedido que não existe
    Então vejo "* Pedido invalido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: RN-09 — gênero fora do pedido
    Dado que o gênero não está lançado no pedido informado
    Quando confirmo o item
    Então vejo "* Genero nao cadastrado neste pedido *"
    E o cursor volta à linha do gênero
    E nada é gravado

  Cenário: RN-09 — item do pedido ainda não liberado
    Dado que o item do pedido ainda não foi liberado
    Quando confirmo o item
    Então vejo "* Pedido nao aprovado *"
    E nada é gravado

  Cenário: RN-09 — gênero já fechado no pedido
    Dado que o item do pedido já recebeu tudo o que pedia
    Quando confirmo o item
    Então vejo "* Genero fechado neste pedido *"
    E nada é gravado

  Cenário: RN-09 — gênero em outro tipo de contrato no pedido
    Dado que o item do pedido é de outro tipo de contrato
    Quando confirmo o item
    Então vejo "* Genero em outro tipo contrato no pedido *"
    E nada é gravado

  Cenário: RN-09 — quantidade acima do que o pedido aguarda
    Dado que a quantidade que informei passa do que o pedido ainda aguarda receber
    Quando confirmo o item
    Então vejo "* Quantidade excede a solicitada no pedido *"
    E nada é gravado

  Cenário: RN-09 — o item lançado acerta a situação do pedido
    Dado que lançei um item contra um pedido aprovado
    Quando a gravação acontece
    Então a quantidade recebida do item do pedido é somada à quantidade que a nota recebeu
    E o item fica aberto enquanto faltar receber e fechado quando receber tudo
    E o pedido fica fechado quando todos os itens dele estiverem fechados

  Cenário: RN-09 — excluir o item devolve a quantidade ao pedido
    Dado que excluo um item já lançado
    Quando a exclusão acontece
    Então o item do pedido perde a quantidade que a nota tinha recebido
    E o pedido volta à situação de aberto quando ainda faltar receber

  Cenário: RN-10 — gênero sem permissão de compra
    Dado que não há contrato para o meu grupo que cubra o gênero e a data da nota
    Quando confirmo o item
    Então vejo "* Genero sem permissao de compra *"
    E o cursor volta à linha do gênero
    E nada é gravado

  Cenário: RN-10 — permissão do pedido diferente da da nota
    Dado que a permissão do contrato do pedido difere da permissão do contrato da nota
    Quando confirmo o item
    Então vejo "* Permissao do pedido difere da nota *"
    E nada é gravado

  Cenário: RN-10 — nota recente sem número de pedido
    Dado que a nota é de data a partir de maio de 2005
    E o número do pedido está zerado
    Quando confirmo o item
    Então vejo "* Informe o numero do pedido *"
    E nada é gravado

  Cenário: RN-10 — quantidade acima do que o contrato autoriza
    Dado que a quantidade do item passa do que o contrato ainda permite comprar naquele gênero
    Quando confirmo
    Então vejo "* Quantidade excede a permitida para compra *"
    E o cursor volta à linha do gênero
    E nada é gravado

  Cenário: RN-10 — valor acima do que o contrato autoriza
    Dado que o valor do item passa do que o contrato ainda permite comprar naquele gênero
    Quando confirmo
    Então vejo "* Valor excede o permitido para compra *"
    E nada é gravado

  Cenário: RN-10 — o item lançado consome o contrato
    Dado que lançei um item contra um contrato
    Quando a gravação acontece
    Então a quantidade e o valor do item são somados ao que o contrato já comprometeu

  Cenário: RN-11 — gênero de pedido acumulado no lançamento comum
    Dado que o pedido é de acúmulo
    E o gênero que informei não entrou no acúmulo
    Quando confirmo o lançamento comum do item
    Então vejo "* <- Genero de pedido acumulado *"
    E nada é gravado

  Cenário: RN-11 — pedido que não é de acúmulo
    Dado que estou na tela N024T em consulta
    E preencho a marca de pedido acumulado em uma linha
    Quando confirmo
    Então vejo "* Pedido nao acumulado *"
    E nada é gravado

  Cenário: RN-11 — pedido do acúmulo que o servidor digita
    Dado que o item pertence ao acúmulo que eu mesmo digitei
    Quando confirmo com a marca de pedido acumulado
    Então vejo "* Pedido acumulado digitado *"
    E nada é gravado

  Cenário: RN-11 — a marca só vale em consulta
    Dado que o item pertence ao acúmulo já calculado
    Quando confirmo com a marca de pedido acumulado fora da consulta
    Então vejo "* Use somente com opcao CON *"
    E nada é gravado

  Cenário: RN-11 — em consulta a marca passa à consulta do pedido acumulado
    Dado que estou na tela N024T em consulta
    E o item pertence ao acúmulo já calculado
    Quando confirmo com a marca de pedido acumulado
    Então a tela passa à consulta da nota e dos pedidos que a compõem

  Cenário: RN-12 — reduzir abaixo do que os órgãos pediram
    Dado que os órgãos já pediram uma quantidade daquele item no acúmulo
    Quando reduzo a quantidade do item abaixo daquela já pedida
    Então vejo "* Quant.pedida pelos Orgaos > quant.da nota *"
    E nada é gravado

  Cenário: RN-12 — excluir item com quantidade pedida pelos órgãos
    Dado que o item tem quantidade pedida pelos órgãos registrada
    Quando peço a exclusão do item
    Então vejo "* Ja existem quant. pedidas pelos Orgaos *"
    E o cursor fica na linha do gênero
    E nada é apagado

  Cenário: RN-12 — excluir item que está em nota de devolução
    Dado que o item está em uma nota de devolução
    Quando peço a exclusão do item
    Então vejo "* <- Genero em nota de devolucao *"
    E nada é apagado

  Cenário: RN-12 — a exclusão devolve o que o item consumia
    Dado que excluo um item com acúmulo e pedido de órgão
    Quando a exclusão acontece
    Então o acúmulo e o pedido do órgão recebem de volta as quantidades que o item consumia
    E o registro de recebimento acumulado da nota é apagado
    E o item é apagado

  Cenário: RN-13 — a inclusão pergunta e não grava
    Dado que estou na tela N024T em inclusão e tudo passou pelas conferências
    Quando confirmo pela primeira vez
    Então vejo "*Confirma inclusao <S/N>?*"
    E a tela reabre com a pergunta
    E o item ainda não foi gravado

  Cenário: RN-13 — resposta diferente de sim cancela a inclusão
    Dado que a pergunta de confirmação está na tela
    Quando respondo qualquer coisa diferente de "S"
    Então a confirmação é cancelada
    E nenhuma mensagem aparece
    E nada é gravado

  Cenário: RN-13 — confirmada a resposta, a inclusão grava
    Dado que a pergunta de confirmação está na tela
    Quando respondo "S"
    Então o item é gravado na nota
    E o pedido e o contrato são acertados

  Cenário: RN-13 — a alteração e a exclusão não perguntam nesta tela
    Dado que estou na tela N024T em alteração ou em exclusão
    Quando confirmo a linha
    Então a pergunta de confirmação não aparece aqui
    E a tela do cabeçalho é quem perguntou antes de me entregar a nota

  Cenário: RN-14 — o total da nota é reajustado pela soma dos itens
    Dado que a soma dos itens da nota é diferente do total gravado
    Quando a tela encerra a operação
    Então o total da nota é regravado com a soma dos itens

  Cenário: RN-14 — a nota que ficou sem itens é apagada
    Dado que a soma dos itens da nota é zero
    Quando a tela encerra a operação
    Então a nota é apagada

  Cenário: RN-14 — o total do IR da nota
    Dado que a nota é de data a partir de 18/10/2021
    E o tipo de contrato tem alíquota de IR
    Quando a tela encerra a operação
    Então o total do IR da nota é o total da nota multiplicado pela alíquota
    E o IR de cada item da nota é regravado

  Cenário: RN-14 — nota anterior a 18/10/2021 não tem IR
    Dado que a nota é de data anterior a 18/10/2021
    Quando a tela encerra a operação
    Então o total do IR da nota fica zerado

  Cenário: RN-15 — as gravações da operação ficam registradas
    Dado que confirmei a inclusão, a alteração ou a exclusão de um item
    Quando a gravação de negócio é feita
    Então cada registro alterado é precedido de um registro de auditoria
    E o registro de auditoria guarda o cadastro, a operação, a matrícula, a estação, a data, a hora e o conteúdo antes e depois

  Cenário: RN-15 — falha do banco
    Dado que a leitura ou a gravação de um cadastro falha no banco
    Quando confirmo
    Então a transação é interrompida com o erro do sistema
    E o que já estava gravado não é desfeito

  Cenário: RN-16 — a consulta não grava nada
    Dado que estou na tela N024T em consulta sobre uma nota já lançada
    Quando a tela mostra o cabeçalho e os itens
    Então nenhum registro é gravado
    E nem o total da nota, nem o pedido, nem o contrato são tocados

  Cenário: RN-17 — a nota nova volta ao cabeçalho
    Dado que a nota que estou tratando é uma nota nova
    Quando a tela encerra a operação
    Então volto à tela do cabeçalho em inclusão
    E o número da nota vem zerado, para uma nota nova
```
