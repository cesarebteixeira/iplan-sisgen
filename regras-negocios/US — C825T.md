# US — C825T — Planejar os cardápios do período por segmento e refeição

## Estória

Como **servidor da coordenação regional escolar que responde pelo planejamento da
merenda**, quero **registrar, para um segmento e uma refeição, quais cardápios valem
dentro de um período e quantas vezes cada um se repete em cada mês**, para que **a
execução da merenda saiba o que servir, para quem e em que dias, sem depender de quem
cadastrou o cardápio**.

O cardápio, sozinho, é só um nome no cadastro: é aqui que ele passa a valer para um
segmento e uma refeição, dentro de um período, com a quantidade de repetições de cada
mês. Sem esse registro o cardápio continua cadastrado e não chega a ninguém — e é esta
tela, e só ela, que o cria, o mantém e o apaga.

## Contexto

Jornada S000M → C000M → C800M → C811M → C825T.
Ator: servidor de CRE — planeja os cardápios de cada segmento e de cada refeição
dentro de um período, e os dias de repetição de cada mês.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os três menus do caminho (`C000M`, `C800M` e `C811M`) não gravam nada e não decidem
nada sobre esta tela: a opção de manutenção vem do que a própria tela guardou na
sessão, e não de quem a abriu (RN-02). Esta tela é terminal — não encadeia para
nenhuma outra.

Da sessão, esta tela usa o **tipo de órgão** da secretaria, que entra em toda leitura
de cadastro que ela faz; a **matrícula** do servidor, que vai para a trilha de
auditoria; e o **código de acesso** e o **privilégio** do vínculo, que entram na
conferência de permissão. A **coordenação regional escolar do planejamento é
digitada**: ela é conferida contra o cadastro das coordenações, e não contra a
coordenação do vínculo do servidor. O **órgão filho** que a entrada carrega não é
usado aqui. O que a entrada deixa e esta tela aproveita está no anexo de evidências,
em **Regras que se revelaram da entrada**.

---

## Regras de negócio

### RN-01 — O planejamento é identificado por coordenação, segmento, refeição e data limite

O servidor informa quatro dados, todos numéricos: a **coordenação regional escolar**
(2 dígitos), o **código do segmento** (2), o **código da refeição** (2) e a **data
limite do período** (dia com 2, mês com 2 e ano com 4). O que estiver em branco vira
zero, e o que não for número é recusado antes de qualquer consulta, com o cursor de
volta no campo — nada é lido por causa do que não passou por essa edição.

A **data de início do período** (dia, mês e ano) também aparece na tela, mas não faz
parte da identificação: ela é copiada do cadastro do cardápio daquele período e é só
exibida. A identificação, então, são **sete campos**: os quatro códigos e as três
partes da data limite.

[?] A tela confere o que foi digitado contra o que foi consultado para a coordenação,
o segmento, a refeição e a data limite — e **não** para a data de início —, mas é a
data de início que vai para o registro gravado. Se o servidor digitar uma data de
início diferente da do cadastro do cardápio, a tela não a recusa; e a cada exibição
ela reescreve esse campo a partir da consulta. Não consigo concluir, pelo fonte, se a
data digitada chega a ser gravada. Pergunta ao site.

### RN-02 — A tela abre em consulta e a opção de manutenção só aceita ALT ou CON

A opção de manutenção não vem de quem abriu a tela: ela vem do que a própria tela
guardou na sessão e, quando não há nada guardado, a tela abre em **consulta** — e
mostra a situação do período como "---------" (RN-08). Confirmada a transação, a tela
aceita apenas **alteração** ou **consulta**; qualquer outra opção é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da opção e
nada é gravado. Esse exame é feito uma única vez por transação, na primeira linha da
grade.

[?] A conferência procura os códigos de alteração e de consulta que o sistema usa nos
seus próprios mnemônicos, e a mensagem manda usar "ALT" e "CON". Ou o terminal traduz
o que o servidor digita antes de enviar, ou a mensagem está desalinhada da
conferência. Não concluo qual dos dois; a mesma forma já foi medida em outras telas
do acervo. Pergunta ao site.

### RN-03 — Consultar exige coordenação, segmento, refeição e período cadastrados

Na consulta, os dados digitados passam por quatro peneiras, nesta ordem: a
**coordenação** tem que estar cadastrada; o **segmento** tem que estar cadastrado; a
**refeição** tem que estar cadastrada — e em branco também é aceito, caso em que a
tela passa a chamar aquele cadastro de **cadastro antigo**; e a **data limite** tem
que estar preenchida (dia, mês e ano). Passando as quatro, o sistema ainda exige que
o **período tenha pelo menos um cardápio cadastrado**. Cada peneira tem a sua
mensagem, a consulta para no primeiro erro e o cursor volta ao campo recusado.

Se os dados digitados forem exatamente os da consulta anterior da sessão, a tela não
refaz as peneiras: é a mesma consulta, e ela reaproveita o que já leu.

[?] O cadastro antigo (sem código de refeição) pode ser consultado e o seu nome
aparece na tela, mas nunca pode ser alterado nem excluído (RN-07). O corpus não mostra
nenhuma tela que crie um planejamento sem refeição. Pergunta ao site.

### RN-04 — A grade tem onze linhas, cada uma com o cardápio, as doze quantidades mensais e a ação

A grade mostra no máximo **11 cardápios** por vez — é o limite que a tela fixa — e
cada linha tem **14 campos**: o código do cardápio (5 dígitos), as **doze
quantidades** de dias de repetição, uma por mês (2 dígitos cada), e a **ação** da
linha (1 caractere). A linha ocupa 30 bytes, e o nome do cardápio (16 caracteres)
aparece ao lado, copiado do cadastro.

Fora da grade, o cabeçalho tem **16 itens**: a tela, a origem, o número da transação,
a data de entrada, o mês de referência, a opção de manutenção, a tela seguinte, a
coordenação, o segmento, a refeição, as três partes da data de início e as três da
data limite. A tela exibe ainda o tipo de órgão, a data do sistema, o nome do
segmento, o nome da refeição e a **situação do período**.

A quantidade de cada mês é um número de dois dígitos e **não** há conferência de que
caiba nos dias daquele mês.

### RN-05 — Sem planejamento para o segmento, a tela avisa e não monta a grade

Quando não existe nenhum registro de planejamento para a coordenação, o segmento, a
refeição e o período informados, a tela avisa **\* Segmento sem planejamento
cadastrado \*** e não monta as linhas da grade. Depois da primeira inclusão o aviso
desaparece, porque a leitura do planejamento passa a encontrar o registro criado.

### RN-06 — Consultar não grava nada

Na consulta a tela só lê e exibe: o cadastro da coordenação, o do segmento, o da
refeição, o do cardápio do período, o dos cardápios previstos para o segmento e o
previsto para a refeição, e os registros do planejamento, montando a grade a partir
deles. A passagem que grava é desviada de propósito quando a opção não é alteração.
Nenhuma gravação e nenhuma exclusão são executadas.

### RN-07 — Atualizar exige ter consultado antes, e cadastro antigo não se atualiza

Antes de qualquer gravação, o sistema exige que os dados de identificação digitados
sejam exatamente os da última consulta da sessão — coordenação, segmento, refeição e
data limite. É o que amarra a atualização à consulta que validou aquele segmento e
aquela refeição. Quem não consultou antes vê **\* Consulte o planejamento antes da
atualizacao \***, com o cursor no campo da opção, e nada é gravado.

A mesma guarda recusa a atualização quando a última consulta foi de um **cadastro
antigo**: sem código de refeição, não se altera nem se exclui, e a mensagem é
**\* Nao atualize. Cadastro antigo \***.

### RN-08 — Período fechado não se atualiza

Antes de gravar, o sistema procura o registro do planejamento daquele período e, se
o encontrar marcado como **fechado**, recusa a atualização com **\* Cadastro fechado
para este periodo \***, com o cursor no campo da coordenação. Na exibição, a situação
do período aparece como "FECHADO" quando o cadastro do cardápio do período está
fechado, e como "---------" caso contrário.

[?] A situação exibida e a situação conferida na gravação vêm de cadastros
diferentes: a tela mostra a que leu do cadastro do cardápio do período, e a guarda lê
a do registro do planejamento. Nenhum programa do acervo grava "fechado" nesse
registro: a única atribuição a esse indicador é a cópia de uma área que a própria
tela limpa antes de gravar, e o registro que a guarda procura é sempre lido com o
código do cardápio zerado, que nenhuma gravação desta tela produz. Ou o indicador vem
de carga externa ao acervo, ou a recusa é inalcançável por este caminho. Pergunta ao
site; não escolho um dos dois lados.

### RN-09 — A ação é por linha: I inclui, A altera, E exclui; o resto é ignorado

A ação é da linha, não da tela. O sistema traduz a ação para a operação
correspondente — inclusão, alteração ou exclusão — e pede autorização para aquela
operação antes de validar a linha. Linha sem código de cardápio é ignorada; ação fora
de I, A e E também — em silêncio, sem mensagem nenhuma. Linha cuja operação não
esteja autorizada para o servidor é abandonada igualmente em silêncio.

### RN-10 — Incluir um cardápio exige seis condições

A inclusão de um cardápio no planejamento só passa se todas forem verdadeiras: o
cardápio **ainda não estiver** no planejamento daquele período; ele **existir** no
cadastro de cardápios; ele estiver marcado como **sobremesa** nesse cadastro; estiver
previsto **para aquele segmento** naquele período; estiver previsto **para aquela
refeição** naquele período; e o servidor tiver informado **pelo menos um dia de
repetição** em algum mês. Cada recusa tem a sua mensagem e o cursor vai para o campo
culpado.

[?] Para incluir, o cardápio tem que estar marcado como sobremesa no seu cadastro —
mas alterar e excluir o mesmo registro não exigem isso, e a grade lista os cardápios
já planejados sem essa distinção. Ou o planejamento é só de sobremesas, ou a marcação
de sobremesa está sendo usada aqui como outra coisa. Pergunta ao site.

### RN-11 — Incluir grava o registro do planejamento

Passando as seis condições, a inclusão cria um registro de planejamento com o tipo de
órgão, a coordenação, o segmento, a refeição, o período (data de início e data
limite), o código do cardápio e as doze quantidades de dias por mês. É esse registro
que passa a sustentar a grade das próximas consultas.

[?] A área do registro não é limpa antes da gravação, e só os valores diferentes de
zero são copiados para ela: os meses que o servidor deixou zerados não são copiados
explicitamente. Não consigo concluir, pelo fonte, o que fica gravado nessas posições.
Pergunta ao site.

### RN-12 — Alterar troca as doze quantidades

A alteração exige que o cardápio **já esteja** no planejamento daquele período; não
estando, a recusa é **\* Cardapio nao cadastrado neste planejamento \*** e nada é
gravado. Existindo, o sistema lê o registro, guarda o que estava lá para a auditoria,
trava o registro e substitui as doze quantidades de dias por mês; os demais dados do
registro permanecem. Alterar sem informar nenhum dia de repetição é recusado com
**\* Informe dias de repeticao no mes \***. O cadastro do cardápio é relido, mas, se
ele não for encontrado, a alteração segue assim mesmo, sem aviso.

### RN-13 — Excluir apaga o registro do planejamento

A exclusão exige que o cardápio esteja no planejamento daquele período — senão,
**\* Cardapio nao cadastrado neste planejamento \*** — e apaga o registro. O que
estava lá vai para a auditoria como valor anterior, e o valor posterior vai em
branco. Para excluir não se pede nenhum dia de repetição.

### RN-14 — Toda gravação deixa rastro na auditoria

Cada inclusão, alteração e exclusão de linha monta um registro na trilha de auditoria
(`A010T`) com o tipo de órgão, a coordenação, a matrícula do servidor, a estação, a
data e a hora, o cadastro de origem, a operação (inclusão, alteração ou exclusão) e
os valores antes e depois: na inclusão o valor anterior vai em branco; na exclusão, o
posterior.

### RN-15 — A validação das linhas vem antes da gravação

A tela percorre as onze linhas da grade conferindo cada uma — cadastro do cardápio,
sobremesa, previsão para o segmento e para a refeição, dias de repetição — e só
depois volta a percorrê-las para gravar. A linha cuja conferência falha marca o erro
da transação, e a gravação é desviada enquanto essa marca estiver posta: recusada uma
linha na primeira passagem, nenhuma gravação acontece.

[?] A conferência de cada linha roda de novo na passagem que grava, e a gravação de
uma linha muda o que a conferência da linha seguinte enxerga. Com o mesmo cardápio em
duas linhas, por exemplo: na primeira passagem as duas são aceitas, porque nenhuma
está no planejamento; na segunda, a primeira é gravada e a segunda passa a ser
recusada por já estar no planejamento. Não consigo concluir pelo fonte se a transação
é tudo-ou-nada no banco — se não for, o planejamento fica atualizado pela metade.
Pergunta ao site.

### RN-16 — A tela grava o planejamento e a auditoria, e só lê os outros sete cadastros

Para cada um dos **9 cadastros** que a tela enxerga, o gerador declara uma rotina de
gravação e uma de exclusão — **18 rotinas** —, mas declarar não é usar: a tela
executa **3** (grava o planejamento, exclui o planejamento e grava a auditoria). Os
outros **7 cadastros** ela apenas lê. As passagens de exibição, de conferência e de
gravação são separadas de propósito, e o que o programa não conferir em cada leitura
o banco barra pelas suas chaves.

### RN-17 — Falha de banco interrompe a transação

Todo acesso a dados testa o erro do banco: o erro de gravação vira uma ação de erro,
e o de leitura e o de exclusão, outra. A transação para ali, sem completar o resto.

---

## Cenários BDD

```gherkin
Funcionalidade: Planejar os cardápios do período por segmento e refeição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C825T

  Cenário: RN-01, RN-04 e RN-06 — consultar o planejamento de um segmento e de uma refeição
    Dado que estou na tela C825T com a opção CON
    E informo a coordenação regional escolar, o segmento, a refeição e a data limite do período
    Quando confirmo a consulta
    Então vejo o nome do segmento, o nome da refeição, a situação do período e, em cada uma das 11 linhas, o código e o nome do cardápio e as doze quantidades de dias por mês
    E a data de início do período aparece como está no cadastro do cardápio
    E nada é gravado

  Cenário: RN-01 — dado não numérico na identificação
    Quando informo texto na coordenação, no segmento, na refeição ou numa das datas
    Então o campo é recusado antes de qualquer consulta
    E o cursor fica no campo recusado
    E nada é consultado por causa dele

  Cenário: RN-02 — a tela abre em consulta
    Dado que abro a tela C825T sem nada guardado da interação anterior
    Então a opção de manutenção vem preenchida como consulta
    E a situação do período aparece como "---------"
    E nada é gravado

  Cenário: RN-02 — opção de manutenção não disponível
    Dado que estou na tela C825T
    Quando informo uma opção de manutenção diferente de ALT e CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: RN-03 — coordenação não cadastrada
    Quando informo uma coordenação regional escolar que não está cadastrada
    Então vejo "* Grupo nao cadastrado *"
    E o cursor volta ao campo da coordenação

  Cenário: RN-03 — segmento não cadastrado
    Quando informo um segmento que não está cadastrado
    Então vejo "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento

  Cenário: RN-03 — refeição não cadastrada
    Quando informo uma refeição que não está cadastrada
    Então vejo "* Refeicao nao cadastrada *"
    E o cursor volta ao campo da refeição

  Cenário: RN-03 — data limite não informada
    Quando deixo a data limite do período sem preencher
    Então vejo "* Informe a data limite de validade *"
    E o cursor volta ao campo da data limite

  Cenário: RN-03 — período sem cardápios
    Quando informo um período para o qual não há nenhum cardápio cadastrado
    Então vejo "* Nao existem cardapios neste periodo *"

  Cenário: RN-03 — consultar um cadastro antigo, sem refeição
    Quando deixo o código da refeição em branco e informo os demais dados
    Então a consulta é aceita
    E a tela mostra o cadastro antigo no lugar do nome da refeição

  Cenário: RN-05 — segmento sem planejamento
    Dado que consultei um segmento, uma refeição e um período que ainda não têm planejamento
    Quando a tela monta a grade
    Então vejo "* Segmento sem planejamento cadastrado *"
    E a grade não é preenchida

  Cenário: RN-07 — atualizar sem consultar antes
    Dado que estou na tela C825T com a opção ALT
    E informo dados de identificação diferentes dos da consulta que fiz
    Quando confirmo
    Então vejo "* Consulte o planejamento antes da atualizacao *"
    E nada é gravado

  Cenário: RN-07 — cadastro antigo não se atualiza
    Dado que consultei um planejamento sem código de refeição
    Quando tento atualizá-lo
    Então vejo "* Nao atualize. Cadastro antigo *"
    E nada é gravado

  Cenário: RN-08 — período fechado
    Dado que consultei um planejamento cuja situação do período é fechada
    Quando tento atualizá-lo
    Então vejo "* Cadastro fechado para este periodo *"
    E nada é gravado

  Cenário: RN-09, RN-10 e RN-11 — incluir um cardápio no planejamento
    Dado que consultei o segmento e a refeição no período
    E o cardápio não está no planejamento
    E o cardápio está cadastrado, marcado como sobremesa, previsto para o segmento e para a refeição naquele período
    Quando preencho a linha com o código do cardápio, os dias de repetição de cada mês e a ação I
    E confirmo
    Então o registro do planejamento é gravado com o período e as doze quantidades
    E a operação fica registrada na auditoria

  Cenário: RN-10 — incluir um cardápio que já está no planejamento
    Dado que o cardápio já está no planejamento daquele período
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Cardapio ja cadastrado neste planejamento *"
    E nada é gravado

  Cenário: RN-10 — incluir um cardápio não cadastrado
    Quando incluo um código de cardápio que não existe no cadastro de cardápios
    Então vejo "* Cardapio nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — incluir um cardápio que não é sobremesa
    Dado que o cardápio existe no cadastro mas não está marcado como sobremesa
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Cardapio nao cadastrado como sobremesa *"
    E nada é gravado

  Cenário: RN-10 — incluir um cardápio não previsto para o segmento
    Dado que o cardápio não está previsto para aquele segmento naquele período
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Cardapio nao cadastrado neste planejamento *"
    E nada é gravado

  Cenário: RN-10 — incluir um cardápio não previsto para a refeição
    Dado que o cardápio não está previsto para aquela refeição naquele período
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Cardapio nao cadastrado para esta refeicao *"
    E nada é gravado

  Cenário: RN-10 — incluir sem informar dias de repetição
    Dado que o cardápio passa por todas as conferências de cadastro
    Quando preencho a linha com a ação I e deixo os doze meses zerados
    Então vejo "* Informe dias de repeticao no mes *"
    E nada é gravado

  Cenário: RN-09, RN-12 e RN-14 — alterar as quantidades de um cardápio do planejamento
    Dado que o cardápio já está no planejamento daquele período
    Quando preencho a linha com a ação A e novos dias de repetição
    E confirmo
    Então as doze quantidades do registro são substituídas
    E os demais dados do registro não mudam
    E a operação fica registrada na auditoria

  Cenário: RN-12 — alterar um cardápio que não está no planejamento
    Dado que o cardápio não está no planejamento daquele período
    Quando preencho a linha com a ação A e confirmo
    Então vejo "* Cardapio nao cadastrado neste planejamento *"
    E nada é gravado

  Cenário: RN-12 — alterar sem informar dias de repetição
    Dado que o cardápio está no planejamento daquele período
    Quando preencho a linha com a ação A e deixo os doze meses zerados
    Então vejo "* Informe dias de repeticao no mes *"
    E nada é gravado

  Cenário: RN-09, RN-13 e RN-14 — excluir um cardápio do planejamento
    Dado que o cardápio está no planejamento daquele período
    Quando preencho a linha com a ação E e confirmo
    Então o registro do planejamento é apagado
    E a auditoria guarda o que estava lá, com o valor posterior em branco

  Cenário: RN-13 — excluir um cardápio que não está no planejamento
    Quando preencho a linha com a ação E para um cardápio que não está no planejamento
    Então vejo "* Cardapio nao cadastrado neste planejamento *"
    E nada é apagado

  Cenário: RN-09 — linha em branco ou com ação desconhecida
    Dado que preencho uma linha sem o código do cardápio, ou com uma ação diferente de I, A e E
    Quando confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada

  Cenário: RN-15 — uma linha recusada impede a gravação
    Dado que preenchi três linhas e uma delas é recusada na conferência
    Quando confirmo
    Então nenhuma linha é gravada
    E a linha recusada mostra a sua mensagem

  Cenário: RN-16 — a tela só grava o planejamento e a auditoria
    Dado que consultei o planejamento de um segmento e de uma refeição
    Quando confirmo a consulta
    Então o cadastro da coordenação, o do segmento, o da refeição, o do cardápio do período e os dos cardápios previstos são apenas lidos
    E nenhuma rotina de gravação ou de exclusão deles é executada

  Cenário: RN-17 — falha de banco durante a gravação
    Dado que a gravação do planejamento falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E o planejamento não é considerado gravado
```
