# US — C062T — Montagem da lista de itens a apostilar das permissões da CRE

## Estória

Como **servidor da Coordenação Regional Escolar (CRE)**, quero **decidir, item por item,
quais classes, subclasses e gêneros das permissões de fornecimento da minha coordenação
entram no apostilamento**, para que o reajuste alcance exatamente os itens que devem ser
apostilados, com a variação de preço de cada um à vista antes da decisão.

O apostilamento é o reajuste posterior de uma permissão de fornecimento, e ele é lançado
item por item. Antes de qualquer valor ser apostilado, é preciso dizer **quais** itens
serão — e é isso que esta tela faz: ela calcula a variação de preço de cada item
candidato, monta a lista dos que o servidor escolher e a entrega à tela que consolida e
aplica o apostilamento. Sem esta tela não há lista; e sem lista o apostilamento não tem
por onde começar.

## Contexto

Jornada S000M → C000M → C050M → C066M → C062T (5 passos).
Ator: servidor de CRE — calcula e seleciona os itens das permissões da sua coordenação
regional que vão para o apostilamento e confere a variação de preço de cada um.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A tela é alcançada por **encadeamento**, sem menu no meio: quem a antecede entrega a
transação direto a ela, e ela mesma, quando o servidor manda seguir, entrega o contrato à
tela do apostilamento (`C065T`) — que chama a que lança o apostilamento item a item
(`C066T`). O que chega pela sessão e o que sai na entrega são regras desta estória
(§RN-02 e §RN-13).

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — Esta tela calcula e monta a lista de itens a apostilar; é a única que a cria e a esvazia

A tela é onde o apostilamento nasce: ela calcula a variação de preço de cada item —
grupo de licitação, classe, subclasse e gênero — das permissões de fornecimento de um
contrato e mantém a **lista** dos itens que vão ser apostilados. Ela enxerga dez
cadastros — o título das telas, o tipo de órgão, a permissão de fornecimento, o gênero, o
tipo de contrato, as duas tabelas de preço, o tipo de licitação, a lista de itens a
apostilar e a liberação das telas por tipo de licitação —, mas **grava em um só**: na
lista. Nela a tela cria o item marcado para incluir e apaga o item marcado para retirar;
a permissão, o preço e o contrato ela só lê. Para cada cadastro que enxerga, o sistema
traz prontas uma operação de gravar e uma de apagar; aqui só as duas da lista são
executadas.

A tela **não** grava no cadastro de auditoria: ele não está entre os que ela enxerga.

Os números de capacidade são de dimensionamento — o máximo esperado declarado no
dicionário de dados —, não volume cadastrado: a permissão de fornecimento e a lista de
itens comportam 1.000.000 de registros cada uma; o gênero e a tabela de preço de maior
capacidade, 150.000 cada um; a outra tabela de preço, 10.000; o título, 2.000; o tipo de
contrato, 1.000; o tipo de licitação e a liberação das telas por licitação, 1.000 cada
um; e o tipo de órgão, 200.

[?] A tela monta um registro de rastro antes de gravar o item, mas não tem o cadastro de
auditoria entre os que enxerga. Se esse rastro sai por uma rotina externa de registro ou
se a operação fica sem rastro, o material não diz.

### RN-02 — O que a tela mostra vem do que está guardado na sessão; sem nada guardado, ela abre em alteração e em branco

Quem chega pelo caminho desta jornada chega sem contrato nenhum guardado na sessão: as
telas do caminho não deixam ali a coordenação regional, o tipo de contrato nem as datas.
Nesse caso a tela assume a **alteração** e encerra a montagem — o cabeçalho fica em
branco para ser digitado e nenhuma linha é montada. Quando existe um contrato guardado na
sessão — deixado por quem a chamou ou pela própria tela numa confirmação anterior —, ela
aproveita: preenche o cabeçalho com a coordenação regional, o tipo de contrato e as
datas, carrega a permissão e monta as linhas a partir dela — as que não tiverem item
correspondente ficam em branco.

[?] A área da sessão de onde a tela lê o contrato é comum a todas as telas e não é
zerada por nenhuma das telas deste caminho: se ela chega com resíduo de outra tela da
mesma sessão, a tela abre com aquele contrato em vez de abrir em branco. O material não
diz quem zera essa área.

### RN-03 — O contrato se identifica pela coordenação regional, pelo tipo de contrato e pela data limite; o tipo de órgão vem da sessão

O que se informa para chegar ao contrato é a coordenação regional escolar, o tipo de
contrato e a data limite do período — dia, mês e ano. O tipo de órgão não se digita: é o
da secretaria que o vínculo da matrícula escolheu na entrada e ficou na sessão, e ele
entra na identificação de tudo o que a tela lê e grava. O item acrescenta à identificação
os códigos de grupo de licitação, de classe, de subclasse e de gênero.

Duas coisas aparecem no cabeçalho e **não** identificam o contrato: a data de início do
período, que é mostrada mas não distingue um contrato de outro — e o período que as
conferências usam é o da permissão achada, não o que estiver no campo —, e o tipo de
licitação, que é o do contrato achado, não um dado informado. A data base também não
identifica: ela entra nas conferências.

### RN-04 — A lista tem treze linhas, uma por item

A grade da tela tem **treze** linhas, uma por item. Cada linha traz os códigos do item —
grupo de licitação, classe, subclasse e gênero —, a descrição resumida do gênero, a
variação de preço calculada e a marca **Sim**, que diz que aquele item já está na lista a
apostilar. A descrição resumida é a do gênero vigente no início do período, lida do
cadastro de gêneros; não achando, a linha fica sem ela. Cada linha tem o seu próprio
campo de ação; fora da grade há um único campo de decisão — o de seguir para o
apostilamento.

### RN-05 — A variação da linha compara o preço vigente na tabela de preços com o preço de referência da permissão

Para cada item, a tela procura o preço na tabela de preços e compara com o preço de
referência da permissão daquele item. Qual tabela usar é decidido por um código que o
tipo de contrato traz: um dos valores manda à tabela de maior capacidade, o outro à
menor. O que a linha mostra é a diferença em percentual; sendo o preço vigente menor que
o de referência, a linha mostra o sinal de menos.

A procura é por quinzena: o início do período usado é o dia 1º ou o dia 16 do mês da data
base, conforme a data base caia na primeira ou na segunda metade do mês. A tela examina
até cinco lançamentos da tabela e só aceita aquele cuja vigência termine a menos de
**75 dias** desse início e cujo preço não seja zero; não achando nessas condições, a
linha fica sem variação. O preço de referência sai da permissão: a tela não pergunta
preço.

[?] O percentual de desconto que a permissão traz entra na conta dos **dois** lados — no
preço de referência e no preço de comparação —, de modo que se cancela e não altera o
percentual mostrado. Se a intenção era aplicar o desconto de um só lado, o material não
diz.

[?] Os dois códigos que escolhem a tabela de preço são uma letra cada e não têm rótulo
validado como os demais campos; o material não diz o que cada um significa nem o que a
tela faz quando o tipo de contrato traz um código que não é nenhum dos dois — e, nesse
caso, a linha fica sem variação.

### RN-06 — Cada linha aceita duas ações: incluir o item na lista e retirá-lo

Na linha, o servidor marca o que fazer com aquele item. São duas ações: **incluir** o
item na lista a apostilar e **retirar** o item da lista. Linha sem ação não é tocada: a
confirmação lê e confere, e nada é gravado naquele item.

[?] A ação é um caractere sem rótulo validado e o material só nomeia os dois valores que
a tela testa; como a coluna aparece para o servidor e se existe um terceiro valor usado,
o material não diz.

### RN-07 — Incluir exige que o item tenha permissão e que ainda não esteja na lista

Para incluir, o item precisa existir como permissão de fornecimento daquele contrato —
não existindo, a tela recusa com **\* Genero nao cadastrado nesta permissao \*** — e não
pode estar já na lista a apostilar — estando, recusa com **\* Genero ja cadastrado na
lista a apostilar \***. Passando pelas duas, o item é criado na lista com o tipo de
órgão, a coordenação regional, o tipo de contrato, o período (início e limite), os
códigos do item, o fornecedor que consta da permissão e o tipo de licitação do contrato.
O valor a apostilar e a data de atualização ficam zerados: quem os preenche é a etapa
seguinte. Nas duas recusas o cursor volta à marca da linha e nada é gravado.

### RN-08 — Retirar exige que o item tenha permissão e que esteja na lista

Para retirar, o item precisa existir como permissão de fornecimento daquele contrato —
não existindo, recusa com **\* Genero nao cadastrado nesta permissao \*** — e precisa
estar na lista a apostilar — não estando, recusa com **\* Genero nao cadastrado na lista
a apostilar \***. Passando pelas duas, o item é apagado da lista. Nas duas recusas o
cursor volta à marca da linha e nada é apagado.

### RN-09 — Confirmar de novo o mesmo contrato não refaz as conferências

Confirmado um contrato, a tela guarda a coordenação regional, o tipo de contrato, a data
limite e a data base na sessão. Numa confirmação seguinte, se esses dados forem
exatamente os mesmos, a tela **pula** todas as conferências de contrato — permissão
cadastrada, tela liberada para a licitação e data base — e vai direto ao que foi marcado
na linha. Mudando qualquer um deles, ela reconfere tudo.

[?] Como a conferência é pulada quando a chave não muda, uma permissão apagada ou uma
liberação retirada entre duas confirmações iguais não são percebidas. Se é intencional, o
material não diz.

### RN-10 — Confirmar o contrato exige a permissão cadastrada

Aceita a confirmação, o sistema procura a permissão de fornecimento da coordenação
regional, do tipo de contrato e da data limite informados. Não achando, recusa com
**\* Permissao nao cadastrada \***, devolve o cursor ao campo da coordenação regional e
não segue: nada é lido adiante e nada é gravado.

[?] A procura é feita sem os códigos do item e, depois dela, o sistema confere de volta
só a coordenação regional, o tipo de contrato e as datas — sem os códigos. Se a procura
exigir a chave exata, a permissão de um item não seria achada; se ela se posicionar no
registro igual ou seguinte, a tela pode estar respondendo por mais de um. Pergunta ao
site.

### RN-11 — A tela precisa estar liberada para o tipo de licitação do contrato

Achada a permissão, o sistema verifica se **esta tela** está liberada para o tipo de
licitação daquela permissão, no cadastro de liberação das telas por tipo de licitação.
Não estando, recusa com **\* Tela nao disponivel para esta licitacao \***, devolve o
cursor ao campo da coordenação regional e não segue: nada é lido adiante e nada é
gravado.

### RN-12 — A data base é conferida contra o período da permissão

A data base informada tem de ser uma data válida, com o ano entre 1994 e 2099 — senão a
recusa é **\* Data base invalida \*** — e tem de cair dentro do período da permissão:
antes do início, **\* Data base menor que data inicio da permissao \***; depois do
limite, **\* Data base maior que data limite da permissao \***. Nas três recusas o cursor
volta ao campo da data base e nada é lido nem gravado. O período usado nessas
comparações é o da permissão achada, não o início que estiver no cabeçalho.

### RN-13 — A marca de seguir entrega o contrato à tela do apostilamento, e exige que a lista exista

Com a marca de seguir preenchida, a tela não toca nas linhas: ela procura a lista de
itens daquele contrato. Não existindo nenhum item, recusa com **\* Nao existe lista para
esta permissao \***, devolve o cursor ao campo da coordenação regional e não segue.
Existindo, ela **entrega a transação à tela do apostilamento** (`C065T`), que abre em
alteração com o contrato no cabeçalho.

O que esta tela entrega: a marca de que a tela de origem é ela, a operação de alteração,
a coordenação regional, o tipo de contrato, o início e o limite do período, a data base,
o tipo de licitação com a sua descrição e a marca de que a transação vai encadeada. A
ação marcada na linha **não** é gravada nesse caso: a tela segue para a seguinte e não
escreve na lista.

[?] A marca de seguir é um caractere sem rótulo validado, o programa nunca a escreve e só
reconhece o valor **S**. O que ela significa e o que a ausência dela significa é digitação
do servidor; o material não define o rótulo.

[?] A tela seguinte exige, para cada item da lista, um valor apostilado maior que zero,
mas esta tela cria o item com esse valor zerado e nenhum dos programas que tocam essa
lista o escreve. De onde vem o valor que a etapa seguinte exige, o material não diz.

### RN-14 — A tela do apostilamento muda conforme quem a chamou

A tela que recebe a entrega (`C065T`) compara a marca da tela de origem com o código
desta tela: vindo **desta** tela, ela preenche o cabeçalho com o que recebeu e abre em
alteração; vindo do menu, sem essa marca, ela abre em branco. É esse o efeito de encadear
tela em tela: o mesmo programa se comporta de dois jeitos conforme a origem — e a origem
só se percebe pela marca que esta tela deixa.

### RN-15 — A tela só aceita a alteração

A operação informada tem de ser a de alteração. Qualquer outra — inclusive a consulta — é
recusada com **\* Operacao nao disponivel. Use ALT \***, com o cursor de volta ao campo
da operação, e nada é lido nem gravado. Antes disso, o roteamento recusa um código de
operação que o sistema não conhece, com **\* Operacao nao disponivel \***, e a transação
não segue.

[?] A recusa manda usar ALT, mas a conferência da tela compara o que foi informado com o
código interno de alteração — o mesmo valor que a própria tela escreve nesse campo quando
ninguém deixou operação. Ou o terminal traduz o mnemônico antes de enviar, ou a mensagem
está desalinhada da conferência. Pergunta ao site; não concluo qual dos dois.

### RN-16 — O acesso passa pela segurança, e a alteração depende do perfil

Antes de ler qualquer cadastro, a tela pede ao sistema de segurança que confira a
**matrícula** e a **tela**; na confirmação do que foi informado, pede a conferência da
**operação**. Sem o perfil de acesso à tela, a operação é recusada com **\* Acesso negado
para esta matricula \***; sem a tela cadastrada, com **\* Tela nao disponivel \***; e,
faltando o flag de alteração no perfil, com **\* Acesso negado para esta operacao \***. A
segurança recebe o contexto da sessão: o tipo de órgão, a matrícula, o código de acesso,
o privilégio, a coordenação regional e a operação.

[?] A conferência da operação só examina inclusão, alteração e exclusão: a consulta cai
no caminho sem flag — o que, nesta tela, é indiferente, porque só a alteração passa
daqui. Se a consulta é livre por desenho ou se a conferência ficou incompleta, o material
não diz.

### RN-17 — A volta devolve o servidor à tela de onde veio, e nada é processado

Quando a transação traz o código da tela anterior, o sistema devolve o servidor àquela
tela e esta não faz mais nada: nenhuma conferência de cadastro, nenhuma leitura e
nenhuma gravação na lista.

### RN-18 — O que não grava nada: confirmar sem ação de linha

Confirmar o contrato sem marcar ação em nenhuma linha lê e confere apenas: nenhum item é
criado e nenhum item é apagado. O mesmo vale para a confirmação que só repete o contrato
já confirmado e para a entrega à tela do apostilamento — que também não grava nada nesta
lista.

### RN-19 — O que se digita é conferido antes de qualquer leitura: os campos são numéricos

Nenhum dos campos com rótulo é texto livre: a coordenação regional, o tipo de contrato, as
três partes do início do período, as três partes da data limite, as três partes da data
base, o tipo de licitação e os quatro códigos do item de cada linha — **dezesseis** campos
— passam pela edição numérica antes de qualquer leitura de cadastro; o que não for número
é recusado no próprio campo, com o cursor de volta a ele. A marca de ação da linha e a
marca de seguir não passam por essa edição.

[?] O texto dessa recusa não está no material: a edição é uma rotina de biblioteca, cujo
corpo não faz parte do lote, e o texto sai da tabela de mensagens do idioma, que também
não está no lote.

---

## Cenários BDD

```gherkin
Funcionalidade: Cálculo e montagem da lista de itens a apostilar das permissões da CRE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C062T

  Cenário: RN-02 — abrir a tela sem contrato guardado
    Dado que nenhuma tela deste caminho deixou contrato guardado na minha sessão
    Quando abro a tela C062T
    Então ela assume a alteração
    E o cabeçalho está em branco e nenhuma linha está montada

  Cenário: RN-02, RN-03 e RN-04 — abrir a tela com o contrato guardado
    Dado que já confirmei um contrato nesta sessão
    Quando abro a tela C062T de novo
    Então o cabeçalho volta com a coordenação regional, o tipo de contrato e as datas daquele contrato
    E a grade volta montada com até treze linhas, uma por item, com os códigos, a descrição resumida do gênero, a variação de preço e a marca Sim onde o item já está na lista

  Cenário: RN-05 — a variação de preço da linha
    Dado que o item tem permissão de fornecimento e a tabela de preços tem um lançamento vigente dentro dos 75 dias seguintes ao início do período
    Quando a grade é montada
    Então a linha mostra a variação percentual entre o preço da tabela e o preço de referência da permissão
    E mostra o sinal de menos quando o preço da tabela é menor que o de referência
    E, não havendo lançamento nessas condições, a linha fica sem variação

  Cenário: RN-05 — a tabela escolhida pelo código do tipo de contrato
    Dado que o tipo de contrato traz um dos dois códigos de tabela de preço
    Quando a grade é montada
    Então a tela procura o preço na tabela correspondente àquele código
    E, trazendo o tipo de contrato um código que não é nenhum dos dois, a linha fica sem variação

  Cenário: RN-07 — incluir um item na lista
    Dado que o item que informei tem permissão de fornecimento neste contrato
    E que ele ainda não está na lista a apostilar
    Quando marco a linha para incluir e confirmo
    Então o item entra na lista a apostilar deste contrato, com o período, o tipo de licitação e o fornecedor da permissão
    E o valor a apostilar dele fica zerado, para a etapa seguinte

  Cenário: RN-07 — o item não tem permissão
    Dado que o item que informei não é permissão de fornecimento deste contrato
    Quando marco a linha para incluir e confirmo
    Então vejo "* Genero nao cadastrado nesta permissao *"
    E o cursor volta à marca da linha
    E nada é gravado

  Cenário: RN-07 — o item já está na lista
    Dado que o item já está na lista a apostilar deste contrato
    Quando marco a linha para incluir e confirmo
    Então vejo "* Genero ja cadastrado na lista a apostilar *"
    E o cursor volta à marca da linha
    E nada é gravado

  Cenário: RN-08 — retirar um item da lista
    Dado que o item que informei tem permissão e já está na lista a apostilar
    Quando marco a linha para retirar e confirmo
    Então o item sai da lista a apostilar deste contrato

  Cenário: RN-08 — retirar item que não está na lista
    Dado que o item tem permissão, mas não está na lista a apostilar
    Quando marco a linha para retirar e confirmo
    Então vejo "* Genero nao cadastrado na lista a apostilar *"
    E o cursor volta à marca da linha
    E nada é apagado

  Cenário: RN-08 — retirar item sem permissão
    Dado que o item que informei não é permissão de fornecimento deste contrato
    Quando marco a linha para retirar e confirmo
    Então vejo "* Genero nao cadastrado nesta permissao *"
    E o cursor volta à marca da linha
    E nada é apagado

  Cenário: RN-09 — confirmar de novo o mesmo contrato
    Dado que já confirmei este contrato
    Quando confirmo de novo sem mudar a coordenação regional, o tipo de contrato, a data limite nem a data base
    Então a tela não reconfere a permissão, a liberação da tela para a licitação nem a data base
    E o que foi marcado na linha é executado

  Cenário: RN-10 — contrato sem permissão cadastrada
    Dado que não existe permissão de fornecimento para a coordenação regional, o tipo de contrato e a data limite que informei
    Quando confirmo o contrato
    Então vejo "* Permissao nao cadastrada *"
    E o cursor volta ao campo da coordenação regional
    E nada é lido adiante e nada é gravado

  Cenário: RN-11 — a tela não está liberada para o tipo de licitação
    Dado que a permissão existe, mas esta tela não está liberada para o tipo de licitação dela
    Quando confirmo o contrato
    Então vejo "* Tela nao disponivel para esta licitacao *"
    E o cursor volta ao campo da coordenação regional
    E nada é gravado

  Cenário: RN-12 — data base inválida
    Quando informo como data base uma data que não existe
    E confirmo o contrato
    Então vejo "* Data base invalida *"
    E o cursor volta ao campo da data base
    E nada é lido nem gravado

  Cenário: RN-12 — data base fora do período da permissão
    Dado que a data base que informei está fora do período da permissão
    Quando confirmo o contrato
    Então, sendo anterior ao início da permissão, vejo "* Data base menor que data inicio da permissao *"
    E, sendo posterior ao limite da permissão, vejo "* Data base maior que data limite da permissao *"
    E o cursor volta ao campo da data base
    E nada é lido nem gravado

  Cenário: RN-13 — a marca de seguir leva o contrato à tela do apostilamento
    Dado que o contrato tem itens na lista a apostilar
    Quando preencho a marca de seguir e confirmo
    Então a transação passa para a tela C065T
    E ela abre em alteração com a coordenação regional, o tipo de contrato, o período, a data base e o tipo de licitação que esta tela entregou
    E nenhuma ação de linha é gravada nesta confirmação

  Cenário: RN-13 — não existe lista para o contrato
    Dado que o contrato não tem nenhum item na lista a apostilar
    Quando preencho a marca de seguir e confirmo
    Então vejo "* Nao existe lista para esta permissao *"
    E o cursor volta ao campo da coordenação regional
    E nada é gravado

  Cenário: RN-14 — a tela do apostilamento aberta pelo menu
    Dado que abro a C065T pelo menu, e não pela C062T
    Quando a tela é apresentada
    Então ela abre em alteração e com o cabeçalho em branco

  Cenário: RN-15 — operação diferente da alteração
    Quando informo no campo da operação uma operação que não é a de alteração, inclusive a consulta
    Então vejo "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: RN-15 — operação que o sistema não conhece
    Quando a transação chega com um código de operação desconhecido
    Então vejo "* Operacao nao disponivel *"
    E a transação não segue

  Cenário: RN-16 — sem a tela no perfil
    Dado que o meu perfil não tem esta tela
    Quando entro na tela
    Então vejo "* Tela nao disponivel *"
    E nada é lido

  Cenário: RN-16 — sem o flag de alteração no perfil
    Dado que o meu perfil não tem o flag de alteração desta tela
    Quando confirmo o contrato
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-17 — a volta
    Dado que a transação traz o código da tela anterior
    Quando confirmo
    Então volto à tela de onde vim
    E nenhuma conferência é feita e nada é gravado

  Cenário: RN-18 — confirmar sem ação de linha não grava nada
    Dado que o contrato tem permissão e a tela está liberada para o tipo de licitação dele
    Quando confirmo sem marcar ação em nenhuma linha
    Então nenhum item é criado na lista e nenhum item é apagado

  Cenário: RN-19 — campo não numérico
    Quando preencho a coordenação regional, o tipo de contrato, uma das datas, o tipo de licitação, o grupo de licitação ou um código de item com letra
    Então a tela recusa o campo antes de qualquer leitura de cadastro
    E o cursor volta ao campo recusado
    E nada é gravado
```
