# US — E506T — Cancelamento do cálculo da requisição

## Estória

Como **servidor de CRE**, quero **cancelar o cálculo de uma requisição que não vai
ser cumprida, informando o órgão filho e a data em que o cálculo começa**, para que
**a requisição pare de valer e tudo o que o cálculo gerou — os pedidos e as
quantidades reservadas — volte atrás sem que ninguém tenha de desfazer pedido por
pedido**.

O cálculo de uma requisição reserva as quantidades e gera os pedidos que o
fornecedor vai atender. Quando ele sai errado — período trocado, órgão errado,
quantidade a mais —, deixá-lo valer é comprar o que não é preciso; corrigi-lo à mão
seria apagar pedido por pedido e devolver cada quantidade à permissão de
fornecimento, uma a uma. Esta tela desfaz o cálculo de uma vez: apaga o que ele
gerou, devolve as quantidades ao recebimento e à permissão, e marca a requisição
como cancelada. E ela só deixa fazer isso enquanto nada do que foi gerado já tiver
sido recebido — a partir do primeiro recebimento, o que o cálculo gerou já entrou na
conta da entrega, e desfazê-lo deixaria o que chegou sem pedido que o sustente.

## Contexto

Jornada S000M → E000M → E500M → E506T.

Ator: servidor de CRE — informa o órgão, a coordenadoria regional escolar e a data
de início do cálculo, confere o que a tela mostra da requisição e confirma o
cancelamento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O menu que abre esta tela não deixa com ela dado nenhum da requisição: quem chega
encontra a tela já na operação de exclusão e nenhuma requisição carregada. Da sessão
a tela usa o tipo de órgão, a coordenadoria regional escolar e o órgão filho do
vínculo, além da descrição do tipo de órgão e da data do sistema para o cabeçalho; a
matrícula, o código de acesso, a estação e o privilégio são o que as conferências de
acesso leem. Ela não abre outra tela: termina reabrindo a si mesma.

As regras abaixo são só as da **tela desta jornada**. O que já está na entrada não
se repete aqui.

---

## Regras de negócio

### RN-01 — A tela cancela o cálculo, e só isso

Esta tela tem uma única operação: **excluir**. Ao ser aberta, ela mesma põe a
operação de exclusão no campo da operação e passa a exigi-la de volta; qualquer
outra operação é recusada com **\* Operacao nao disponivel. Use EXC \***, com o
cursor de volta ao campo da operação, antes de qualquer leitura. Não há caminho de
consulta nem de alteração por aqui: o que se lê, lê-se no caminho do cancelamento.

[?] O campo da operação é preenchido pela própria tela na abertura; o acervo lido não
mostra se a máscara pode sobrescrevê-lo com o código de outra tecla — e, nesse caso,
o servidor veria a recusa sem ter pedido nada —, nem o que a mensagem quer dizer com
"EXC". Pergunta ao site.

### RN-02 — A tela enxerga treze cadastros e escreve em nove

Para cancelar, a tela enxerga **onze cadastros** — o registro das telas, o cadastro
dos órgãos filho, o das requisições, o dos itens calculados, o dos pedidos, o dos
gêneros dos pedidos, o dos pedidos acumulados, o do que já foi recebido, o das
quantidades calculadas, o das permissões de fornecimento e a auditoria — e ainda o
cadastro do servidor e o das autorizações do código de acesso, que as conferências
de acesso leem (RN-12). Lê **dez** deles e escreve em **nove**: apaga os pedidos
acumulados, os itens calculados, as quantidades calculadas, os gêneros e os pedidos;
altera o que já foi recebido, as permissões de fornecimento e a situação da própria
requisição; e **inclui** um registro de auditoria para cada operação. Nenhum outro
cadastro é incluído, alterado ou excluído — e a simples abertura da tela não escreve
nada.

Os cadastros estão dimensionados para: telas **2 mil**; órgãos filho **12 mil**;
requisições **10 mil**; itens calculados **100 mil**; pedidos **10 milhões**; gêneros
dos pedidos **200 milhões**; pedidos acumulados **100 mil**; o que já foi recebido
**10 mil**; quantidades calculadas **100 mil**; permissões de fornecimento **1
milhão**; auditoria **60 milhões**. São **capacidades** — o máximo esperado no
dimensionamento —, não volumes cadastrados.

### RN-03 — Ao abrir, a tela mostra o cabeçalho e não grava nada

Ao ser aberta, a tela mostra no cabeçalho a descrição do tipo de órgão da sessão e a
data do sistema, põe a operação de exclusão no campo da operação, guarda a
coordenadoria da sessão para as conferências seguintes e deixa o cursor no campo do
órgão filho. Ela **não** propõe o órgão nem as datas: quem informa o órgão, a
coordenadoria e as doze partes de data (as do início e as do limite do cálculo, as do
início e as do limite do período) é o servidor. Abrir a tela só lê: não apaga nem
grava nada.

[?] A data do sistema e a descrição do tipo de órgão são preenchidas na abertura e
limpas a cada digitação, sem que a tela as reponha; se o ambiente as repõe por fora,
o acervo lido não mostra. Pergunta ao site.

### RN-04 — O órgão é obrigatório, e o acesso é o do vínculo

O órgão filho tem de vir informado: em branco, a recusa é **\* Informe o orgao \***,
com o cursor no órgão, e nada mais é lido. Quando o vínculo do servidor carrega um
órgão filho, o informado tem de ser esse mesmo, senão
**\* Usuario sem acesso a outro orgao \***. O órgão tem de estar cadastrado — senão
**\* Orgao nao cadastrado \*** — e, quando o vínculo carrega uma coordenadoria
regional escolar, a coordenadoria **do órgão cadastrado** tem de ser a mesma, senão
**<- Usuario sem acesso ao grupo deste orgao \***. Em todas essas recusas o cursor
volta ao campo do órgão e nada é apagado.

A coordenadoria digitada não decide nada: a partir do cadastro do órgão, a tela passa
a usar a coordenadoria que está nele, em todas as leituras e em todas as gravações, e
é também de lá que sai o nome do órgão que ela mostra.

[?] A coordenadoria é pedida ao servidor, aceita na edição numérica e depois
descartada — não é comparada nem com a da sessão nem com a do órgão. Ou o campo é de
enfeite, ou a conferência deveria comparar o que foi digitado. Pergunta ao site.

### RN-05 — A requisição é procurada pelo órgão, pelo grupo e pela data de início do cálculo

A tela procura a requisição pelo tipo de órgão da sessão, pelo órgão informado, pela
coordenadoria do órgão cadastrado e pela data de início do cálculo — dia, mês e ano.
Exige o **dia**: sem ele, a recusa é **\* Informe a data de inicio do preparo \***,
com o cursor no dia. Não achando a requisição, a recusa é
**\* Requisicao nao cadastrada \***, no mesmo campo. Achando, ela exige que a
requisição esteja **calculada**: uma requisição ainda não calculada é recusada com
**\* Requisicao nao calculada \***, também no campo da data. Achada e calculada, a
requisição vem para a tela: o limite do cálculo e o início e o limite do período —
dia, mês e ano de cada um — passam a ser os da requisição, e a descrição do órgão vai
para o cabeçalho.

[?] Só o dia é exigido campo a campo; o mês e o ano da mesma data, em branco, valem
zero e a procura não acha — o servidor vê "requisição não cadastrada" no lugar de uma
recusa do campo que faltou. Pergunta ao site.

### RN-06 — Os campos numéricos passam por edição antes das conferências

Antes de qualquer conferência, os **catorze** campos numéricos — o órgão filho, a
coordenadoria regional escolar, as três partes da data de início do cálculo, as três
do limite do cálculo, as três do início do período e as três do limite do período —
passam pela edição numérica, e o campo em branco é tratado como zero. A operação, a
tela de origem e a resposta da confirmação não passam por essa edição.

[?] O que o servidor vê quando digita algo que não é número não se conclui desta
tela: a rotina que faz a edição não tem corpo no acervo. E a tela só sabe devolver o
cursor ao órgão filho, às três partes da data de início do cálculo e às três do
início do período — um erro de digitação na coordenadoria, no limite do cálculo ou no
limite do período não tem posição de cursor definida. Pergunta ao site.

### RN-07 — Só o cálculo cujos pedidos ainda não foram atendidos pode ser cancelado

Antes de perguntar, a tela percorre os pedidos que o cálculo gerou e confere os
gêneros de cada um. Se algum gênero já tem **quantidade recebida**, a recusa é
**\* Ja existe pedido com quantidade recebida \***, nomeando o pedido. Se algum
gênero pertence a um **pedido acumulado**, a recusa é
"Exc pedido *pedido* do acumulado *pedido acumulado*". Os gêneros já marcados como
excluídos não entram na conferência. Nas duas recusas o cursor fica na data do
cálculo e nada é apagado.

A tela examina no máximo **vinte** pedidos distintos por requisição.

[?] O que passar de vinte pedidos não entra na relação conferida nem é apagado depois:
se uma requisição puder alcançar mais de vinte pedidos distintos, o cancelamento fica
pela metade — a requisição é cancelada e parte dos pedidos que ela gerou fica no
sistema. Pergunta ao site.

### RN-08 — O que já foi para o arquivo do fornecedor é avisado, não recusado

Quando algum dos pedidos envolvidos já consta do arquivo enviado ao fornecedor, a
tela mostra **\* Pedidos ja constam do arquivo do fornecedor \*** junto da pergunta de
confirmação. O aviso não impede o cancelamento: a tela pede a confirmação do mesmo
jeito e, confirmada, cancela.

### RN-09 — O cancelamento é confirmado antes de acontecer

Passando por todas as conferências, a tela ainda não apaga: ela mostra
**\* Confirma exclusao do calculo <S/N> ? \***, com o cursor na resposta, e encerra a
passagem. Só a resposta afirmativa, com o órgão e a data de início do cálculo ainda
os mesmos que foram conferidos, leva ao cancelamento. Qualquer outra resposta — ou a
troca do órgão e da data entre a pergunta e a resposta — descarta a confirmação
pendente e a tela refaz todas as conferências, voltando à mesma pergunta. Informar os
dados e ver a requisição, por si só, não apaga nada.

[?] A resposta negativa não devolve o servidor ao começo nem encerra a tela: ela só
descarta a pendência, e a tela confere tudo de novo e pergunta outra vez. Se a
intenção era poder desistir com a resposta negativa, o caminho não faz isso — quem
responde "N" só sai encerrando a tela. Pergunta ao site.

[?] A pendência é guardada de um modo que impede o cancelamento na mesma passagem,
e quem desfaz essa marca entre uma digitação e outra não está no acervo lido; sem
isso, a tela ficaria presa na pergunta. Pergunta ao site.

### RN-10 — Confirmado, a tela apaga o que o cálculo gerou e devolve as quantidades

Confirmado o cancelamento, a tela apaga, um a um, os **pedidos acumulados** da
requisição e os **itens calculados**, apaga as **quantidades calculadas** por
classificação e gênero e, para cada pedido envolvido, apaga os **gêneros** e depois o
**próprio pedido**. Ao passar por cada pedido acumulado, devolve ao registro do que
já foi recebido a quantidade daquele acumulado, reduzindo a quantidade recebida na
mesma medida. Ao apagar um gênero que ainda não tinha sido atendido, devolve à
**permissão de fornecimento** a quantidade pendente — a diferença entre a quantidade
pedida e a já estornada. O pedido cujo registro não é encontrado é saltado, e o
gênero já marcado como excluído é apagado de novo, sem ajuste na permissão. Nada é
criado por esta tela.

[?] A recusa por gênero de pedido acumulado (RN-07) e este trecho não fecham. Quem
gera o gênero a partir de um pedido acumulado marca esse gênero como de acumulado, de
modo que a recusa barraria justamente o caso que este trecho trata — devolver ao
recebimento a quantidade do acumulado. Ou a recusa vale para outro caso, ou o trecho
ficou inalcançável por este caminho. Não escolho um dos dois lados. Pergunta ao site.

[?] A exclusão dos pedidos acumulados não é precedida de registro de auditoria,
embora as outras seis exclusões e alterações desta tela o sejam. Se a ausência é
intencional, é pergunta ao site.

### RN-11 — No fim, a requisição fica cancelada — e não é apagada

Terminado o serviço, a tela grava a requisição com a marca de calculada em branco: a
requisição continua no cadastro, sem valer, e o campo da situação passa a mostrar
**Requisicao Cancelada**. É essa marca, agora em branco, que faz um segundo pedido de
cancelamento sobre a mesma requisição ser recusado com
**\* Requisicao nao calculada \*** (RN-05). Nenhum outro cadastro é incluído ou
alterado além do que as regras acima descrevem.

[?] O caminho que conclui o cancelamento volta a ler a requisição em vez de encerrar,
e o acervo lido não mostra guarda que interrompa essa volta: como a requisição
continua cadastrada, a leitura seguinte a encontra de novo. Não consigo determinar se
a transação encerra aí — reabrindo a tela com o aviso de cancelada — ou se a volta se
repete. Pergunta ao site.

### RN-12 — Nada é cancelado sem a conferência de sessão, de tela, de acesso e de operação

Na abertura, a tela confere que o servidor está na **estação em que a sessão foi
aberta** (em outra, o acesso é encerrado e a sessão volta à entrada), que a tela está
registrada (senão **\* Tela nao disponivel \***), que ela pertence ao módulo da
sessão e que o código de acesso do servidor alcança a tela e a operação de exclusão
(senão **\* Acesso negado para esta matricula \*** ou
**\* Acesso negado para esta operacao \***). Também é recusada a requisição da segunda
página da tela (**\* Acesso a pagina 2 negado \***). Sem passar por tudo, nada é
apagado e nada é gravado.

### RN-13 — Cada operação do cancelamento fica na auditoria

Cada registro apagado e cada quantidade devolvida deixa um registro de auditoria, com
a tela e o cadastro de origem, a operação, o conteúdo do registro antes e depois, a
matrícula, a estação, a data e a hora da sessão, o tipo de órgão, a coordenadoria, o
número do processo do cálculo — o órgão e a data de início — e o mês de atividade da
transação. Só a passagem que apaga e devolve gera registro: a recusa, a abertura da
tela e o cancelamento cuja confirmação não veio não geram nenhum.

[?] Além da operação, cada registro de auditoria leva uma marca de manutenção fixa, e o
registro de auditoria do recebimento é montado com um campo de número de processo que
a tela apenas zera, enquanto os demais levam o número do processo do cálculo. O que a
marca significa e se o zero é intencional não está no acervo lido. Pergunta ao site.

### RN-14 — Se outra tela abriu esta, o operador volta para ela

Se a tela for aberta em cadeia por outra tela — que deixa o seu código no campo da
tela de origem —, a operação não acontece: o operador é devolvido à tela que a
chamou. Com esse campo em branco, que é como o menu a abre, a tela segue a operação
normalmente — a tela não muda de comportamento por ter vindo do menu.

[?] O acervo lido não mostra nenhum programa que preencha o campo da tela de origem
para esta tela, e a máscara não veio junto: não se conclui quem o preenche, nem em que
casos ele chega preenchido. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Cancelamento do cálculo da requisição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E a minha sessão carrega o tipo de órgão, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E506T

  Cenário: Cancelar o cálculo de uma requisição calculada
    Dado que existe uma requisição calculada, do meu órgão e da minha coordenadoria,
      com a data de início do cálculo que vou informar
    E que nenhum dos pedidos que o cálculo gerou tem quantidade recebida nem pertence
      a um pedido acumulado
    Quando informo o órgão, a coordenadoria e a data de início do cálculo
    Então a tela mostra a requisição e me pergunta se confirmo a exclusão
    Quando respondo "S"
    Então os pedidos acumulados da requisição são apagados, com a quantidade
      devolvida ao registro do que já foi recebido
    E os itens calculados e as quantidades calculadas são apagados
    E cada gênero é apagado, com a quantidade pendente devolvida à permissão de
      fornecimento
    E cada pedido é apagado
    E vejo "Requisicao Cancelada" no campo da situação
    E a requisição continua cadastrada, sem a marca de calculada

  Cenário: A tela só cancela
    Dado que estou na tela E506T
    Quando a transação chega com uma operação que não é a de exclusão
    Então vejo "* Operacao nao disponivel. Use EXC *"
    E o cursor fica no campo da operação
    E nada é lido, apagado nem gravado

  Cenário: A abertura da tela não busca requisição nem grava nada
    Dado que estou na tela E506T
    Quando abro a tela
    Então vejo a descrição do tipo de órgão da minha sessão e a data do sistema
    E o campo da operação mostra a exclusão
    E o cursor fica no campo do órgão filho
    E nenhuma requisição foi lida
    E nenhum cadastro foi apagado, alterado ou incluído

  Cenário: O órgão é obrigatório
    Dado que estou na tela E506T
    Quando confirmo sem informar o órgão
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é apagado nem gravado

  Cenário: O servidor não cancela requisição de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo outro órgão e confirmo
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão
    E nada é apagado nem gravado

  Cenário: Órgão não cadastrado
    Dado que estou na tela E506T
    Quando informo um órgão que não está cadastrado e confirmo
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é apagado nem gravado

  Cenário: Órgão de outra coordenadoria
    Dado que o meu vínculo carrega uma coordenadoria regional escolar
    Quando informo um órgão cadastrado em outra coordenadoria e confirmo
    Então vejo "<- Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é apagado nem gravado

  Cenário: A coordenadoria que eu digito não é a que procura a requisição
    Dado que informo o órgão e uma coordenadoria diferente da do órgão
    Quando confirmo
    Então a tela procura a requisição pela coordenadoria do órgão cadastrado
    E a coordenadoria que eu digitei não é usada

  Cenário: A data de início do cálculo é obrigatória
    Dado que estou na tela E506T
    Quando confirmo com o dia do início do cálculo em branco
    Então vejo "* Informe a data de inicio do preparo *"
    E o cursor fica no campo do dia
    E nada é apagado nem gravado

  Cenário: O mês e o ano da data de início do cálculo
    Dado que estou na tela E506T e informo o dia do início do cálculo
    Quando deixo o mês ou o ano em branco e confirmo
    Então a requisição é procurada com eles valendo zero
    E, não sendo achada, vejo "* Requisicao nao cadastrada *"

  Cenário: Requisição não cadastrada
    Dado que estou na tela E506T
    Quando informo um órgão e uma data de início de cálculo que não correspondem a
      nenhuma requisição e confirmo
    Então vejo "* Requisicao nao cadastrada *"
    E o cursor fica no campo do dia
    E nada é apagado nem gravado

  Cenário: Requisição ainda não calculada
    Dado que existe uma requisição do meu órgão e da minha coordenadoria, mas ainda
      não calculada
    Quando informo o órgão e a data e confirmo
    Então vejo "* Requisicao nao calculada *"
    E o cursor fica no campo do dia
    E nada é apagado nem gravado

  Cenário: A requisição cancela-se uma vez só
    Dado que a requisição já foi cancelada nesta ou em outra sessão
    Quando informo o órgão e a data e confirmo
    Então a requisição é achada, mas está sem a marca de calculada
    E vejo "* Requisicao nao calculada *"
    E nada é apagado nem gravado

  Cenário: Os campos numéricos passam por edição antes das conferências
    Dado que estou na tela E506T
    Quando deixo um dos catorze campos numéricos em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências
    E a digitação que não é número é barrada antes das conferências da requisição

  Cenário: Pedido com quantidade recebida
    Dado que um dos gêneros de um pedido gerado pelo cálculo já tem quantidade
      recebida
    Quando confirmo o cancelamento
    Então vejo "* Ja existe pedido com quantidade recebida *", com o pedido nomeado
    E o cursor fica na data do cálculo
    E nada é apagado nem gravado

  Cenário: Gênero de pedido acumulado
    Dado que um dos gêneros de um pedido gerado pelo cálculo pertence a um pedido
      acumulado
    Quando confirmo o cancelamento
    Então vejo "Exc pedido <pedido> do acumulado <pedido acumulado>"
    E o cursor fica na data do cálculo
    E nada é apagado nem gravado

  Cenário: Mais de vinte pedidos na requisição
    Dado que a requisição alcança mais de vinte pedidos distintos
    Quando confirmo o cancelamento
    Então só os vinte primeiros entram na relação de pedidos que a tela monta
    E os pedidos que passarem disso não entram nessa relação

  Cenário: O que já foi para o arquivo do fornecedor é avisado, mas não impede
    Dado que um dos pedidos envolvidos já consta do arquivo enviado ao fornecedor
    Quando a tela chega à confirmação
    Então vejo "* Pedidos ja constam do arquivo do fornecedor *"
    E a tela pede a confirmação do mesmo jeito

  Cenário: O cancelamento é pedido com confirmação
    Dado que a requisição passou por todas as conferências
    Quando confirmo
    Então vejo "* Confirma exclusao do calculo <S/N> ? *"
    E o cursor fica na resposta
    E nada foi apagado ainda

  Cenário: Informar os dados e ver a requisição não apaga nada
    Dado que existe uma requisição calculada, do meu órgão e da minha coordenadoria,
      sem pedido recebido nem acumulado
    Quando informo o órgão e a data e confirmo
    Então vejo a pergunta de confirmação
    E nenhum pedido, gênero, item calculado, quantidade calculada ou pedido
      acumulado foi apagado
    E a requisição continua com a marca de calculada

  Cenário: A resposta negativa não cancela
    Dado que a tela me pediu a confirmação do cancelamento
    Quando respondo algo diferente de "S"
    Então o cancelamento não acontece
    E a tela confere a requisição de novo e volta a pedir a confirmação

  Cenário: Trocar o órgão ou a data depois da pergunta
    Dado que a tela já me pediu a confirmação
    Quando troco o órgão ou a data de início do cálculo e respondo "S"
    Então a confirmação é descartada
    E a tela confere tudo de novo, perguntando outra vez

  Cenário: Cada exclusão e cada alteração do cancelamento deixa auditoria
    Dado que o cancelamento foi confirmado
    Quando a tela executa as exclusões e as alterações
    Então cada uma deixa um registro de auditoria com a operação, o cadastro
      atingido, o número do processo, a minha matrícula, a estação, o tipo de órgão,
      a coordenadoria, o mês de atividade e a data e a hora da sessão, com o
      conteúdo do registro antes e depois
    E a exclusão dos pedidos acumulados não deixa registro

  Cenário: Nada é cancelado sem a conferência de sessão, de tela, de acesso e de operação
    Dado que estou na tela E506T
    Quando a conferência da estação, do registro da tela, do módulo, do código de
      acesso ou da operação não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *",
      "* Acesso negado para esta operacao *" ou "* Acesso a pagina 2 negado *"
    E nada é apagado e nada é gravado
    E, se a estação não for a da minha sessão, o acesso é encerrado

  Cenário: A tela aberta em cadeia por outra tela
    Dado que chego à tela E506T com o campo da tela de origem preenchido
    Quando confirmo
    Então a operação não acontece
    E sou devolvido à tela que me chamou

  Cenário: A tela aberta pelo menu segue a operação
    Dado que chego à tela E506T pelo menu, com o campo da tela de origem em branco
    Quando confirmo
    Então a tela segue a operação de cancelamento normalmente

  Cenário: A recusa não apaga nem grava nada
    Dado que estou na tela E506T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então nenhum pedido acumulado, item calculado, quantidade calculada, gênero ou
      pedido foi apagado
    E a requisição, o que já foi recebido e as permissões de fornecimento continuam
      como estavam
    E nenhum registro de auditoria foi incluído
```
