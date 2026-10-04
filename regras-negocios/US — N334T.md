# US — N334T — Consulta das notas fiscais e das quantidades de um pedido de operador logístico

## Estória

Como **servidor da CRE**, quero **consultar um pedido de operador logístico pelo
número e pelo ano da entrega e ver, item por item, as notas fiscais e as
quantidades**, para que **eu confira o que o pedido compreende, o que já foi
recebido e o que continua em estoque, sem depender de relação impressa nem de
informação pedida a quem opera o processamento**.

O pedido de operador logístico não se consulta na tela dos pedidos comuns: aquela o
recusa e manda para esta, e esta recusa o pedido comum. Depois de liberado, o pedido
é acompanhado pela CRE até a entrega, e é nesta consulta que se vê a que nota fiscal
cada parcela do item foi lançada e quanto ainda falta receber. A tela não devolve
nada: ela só lê, e o que mostra é o que está registrado no momento em que a consulta
é confirmada.

## Contexto

Jornada S000M → N000M → N050M → N300M → N334T.

Ator: servidor de CRE — informa a coordenadoria regional escolar, o número do pedido,
o ano da entrega e o código do operador logístico, e vê as notas fiscais e as
quantidades de cada item do pedido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As telas do meio do caminho são menus: não deixam nada de próprio para a tela de
destino, apenas dizem qual tela abrir. O que a N334T usa da sessão — a matrícula, o
código de acesso, o privilégio, a secretaria (o tipo de órgão) e a coordenadoria
regional escolar — foi deixado pela entrada. Esta é a consulta irmã da N034T: o
pedido de operador logístico só se consulta aqui, e o pedido comum só se consulta
lá. A tela não encadeia para nenhuma outra: não passa registro nem operação adiante,
e a jornada termina nela.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela consulta as notas fiscais e as quantidades de um pedido de operador logístico

A tela mostra um pedido — a coordenadoria regional escolar, o número, o ano da
entrega e o código e a razão social do operador logístico — e, para cada nota fiscal
do pedido, uma linha com a sub-classe e o gênero do material, a descrição do gênero,
o número da nota, a quantidade do gênero e as três quantidades de saldo do item. É
uma leitura de tela: ela não monta documento para impressão nem entrega trabalho ao
processamento em lote.

A lista é montada em até **15 linhas** por passagem — 15 é o dimensionamento da
lista, não o limite de notas de um pedido.

[?] Os títulos das colunas da linha e o que cada uma das três quantidades de saldo
representa não estão no acervo desta jornada: a máscara da tela não veio no lote e o
programa só rotula os campos de entrada. Pergunta ao site.

### RN-02 — A tela não altera cadastro nenhum

Nenhum dos **oito** conjuntos que a tela enxerga é incluído, alterado ou excluído: as
notas fiscais do pedido, as notas com entrada ainda não confirmada, o cadastro de
gêneros, os itens do pedido com os saldos, o pedido, o cadastro de tipos de
contrato, o cadastro de operadores logísticos e o registro das telas ficam como
estavam. A tela também não deixa rastro de auditoria.

O único lugar em que ela deixa marca é a área de trabalho da sessão, que guarda o
pedido consultado (RN-12).

### RN-03 — A consulta é a única operação aceita

Confirmar com uma operação que não seja a consulta é recusado com
**\* Operacao nao disponivel. Use CON \*** e o cursor volta ao campo da operação;
nada é consultado. Ao montar a tela, o sistema já fixa a operação em consulta.

[?] O que o terminal devolve no campo da operação não está no lote — a máscara da
tela não veio, e o programa apenas compara o que chega com o código de consulta. Se
o campo volta sempre com a consulta, esta recusa é inalcançável. Pergunta ao site.

[?] A tela se apresenta ao controle de acesso como tela de manutenção, embora só
consulte, e por isso uma confirmação **sem** operação informada passa a exigir a
permissão de alteração antes de chegar à recusa da própria tela. Se isso é
intencional, pergunta ao site.

### RN-04 — A coordenadoria regional escolar é obrigatória e é a da sessão

A consulta só corre na coordenadoria regional escolar da sessão. Se a sessão carrega
uma coordenadoria e o servidor informa outra — ou deixa o campo em branco —, a recusa
é **\* Usuario sem acesso a outro grupo \***, com o cursor de volta no campo da
coordenadoria. Se a sessão não carrega coordenadoria nenhuma e o campo vem em branco,
a recusa é **\* Informe o grupo \***, também com o cursor no campo. Em qualquer das
duas, nada é consultado. Ao abrir, a tela apresenta a coordenadoria da sessão no
campo.

### RN-05 — O pedido é identificado pelo número, pelo ano da entrega e pela secretaria da sessão

O pedido é informado em duas partes — o número, com **6 dígitos**, e o ano da
entrega, com **4** — e é a junção das duas que identifica o pedido no resto do
sistema. A consulta corre dentro da secretaria da sessão: o pedido procurado é o
daquela secretaria, nunca o de outra. O ano não é conferido contra a data do
sistema: o que se informa é o que se procura. Não encontrando, a recusa é
**\* Pedido nao cadastrado \***, com o cursor no número do pedido, e nada é mostrado.

[?] O que a tela mostra como número do pedido são 6 dígitos, e o pedido do resto do
sistema tem 10; os outros 4 são o ano da entrega. Se algum pedido do acervo não
seguir essa composição, o acervo desta jornada não mostra. Pergunta ao site.

### RN-06 — A consulta exige um pedido liberado

Pedido ainda não aprovado — a situação em branco — é recusado com
**\* Pedido pendente de aprovacao \***; pedido pendente de distribuição, com
**\* Pedido pendente de distribuicao \***. Nas duas, o cursor volta ao número do
pedido e nada é mostrado. Pedido aprovado e pedido fechado são consultáveis.

[?] O acervo desta jornada não lista todos os valores possíveis da situação do
pedido: os trechos que recusam tratam o valor em branco e um valor específico, e
deixam passar os demais. Se existe outra situação que passe em silêncio, pergunta ao
site.

[?] A tela não confere a marca de exclusão do pedido: a consulta irmã dos pedidos
comuns confere e recusa com **\* Pedido excluido \***, e esta não. O pedido marcado
como excluído, se ainda estiver no cadastro, é consultado como qualquer outro. Se é
intencional, pergunta ao site.

### RN-07 — Só o pedido de contrato de operador logístico é consultado aqui

A tela lê o tipo de contrato do pedido e exige que ele esteja cadastrado para a
secretaria da sessão: não estando, a recusa é **\* Tipo contrato nao cadastrado \***.
Exige também que o tipo de contrato seja de operador logístico: qualquer outro é
recusado com **\* Pedido nao e de oper.logistico. Use N034T \***. Nas duas, o cursor
volta ao número do pedido e nada é mostrado.

### RN-08 — A descrição do gênero vem do cadastro de gêneros

A descrição que a tela mostra em cada linha sai do cadastro de gêneros, lida pela
sub-classe, pelo gênero e pela data de emissão da nota fiscal daquela linha. O gênero
marcado como excluído fica fora do conjunto que a tela lê.

[?] O cadastro guarda mais de uma descrição para o mesmo gênero, separadas pela data
de início de vigência, e a tela informa a data da nota no pedido de leitura; o acervo
não documenta como essa leitura escolhe entre as versões. Não dá para afirmar se a
tela busca a descrição vigente na data da nota ou apenas a primeira do gênero.
Pergunta ao site.

### RN-09 — As quantidades da linha são as do item, e não as da nota

A quantidade do gênero é a da nota fiscal da linha; as três quantidades de saldo são
as do item do pedido — a sub-classe e o gênero —, e não as da nota. Quando duas notas
do pedido são do mesmo item, as duas linhas repetem os mesmos saldos.

### RN-10 — O pedido tem de ter notas

Sem nota nenhuma para o pedido, a recusa é **\* Pedido sem notas cadastradas \***,
com o cursor no número do pedido, e nada é mostrado. Se o pedido não tem nota lançada
mas tem nota com entrada ainda não confirmada, a recusa prevista é
**\* Pedido com notas pendentes de confirmacao \***.

[?] A conferência das notas com entrada não confirmada está atrás de uma guarda que
exige que o pedido não tenha nota nenhuma lançada, e o caminho que monta a tela já
recusa, para essa mesma condição, com a mensagem de "sem notas cadastradas". Além
disso, o trecho que faz essa conferência só é alcançado quando a coordenadoria
guardada na sessão difere da informada — e a tela exige que sejam iguais. Ou a
mensagem de notas pendentes é inalcançável por esta tela, ou existe um estado da
sessão que este acervo não mostra. Pergunta ao site.

### RN-11 — O nome do operador logístico acompanha o pedido

A tela mostra a razão social do operador logístico lida no cadastro de operadores
pelo código de operador do pedido. Ao abrir, o que aparece é o que ficou guardado da
última consulta; ao confirmar, a tela relê o cadastro pelo código do pedido e é esse
nome que fica guardado.

### RN-12 — A tela retoma o pedido da última consulta

O pedido consultado fica guardado na área de trabalho da sessão: ao reabrir a tela, é
ele que aparece, com a coordenadoria, o código e o nome do operador logístico, sem o
servidor precisar informá-lo de novo. Se a sessão não tem pedido guardado, a tela
abre com os campos do pedido em branco e só com a coordenadoria da sessão.

### RN-13 — Os campos informados são numéricos

Os **sete** campos informados — a coordenadoria, o número do pedido, o ano da
entrega, o código do operador logístico, a sub-classe, o gênero e o número da nota
fiscal — são numéricos, e a tela os converte antes de usá-los; o que não for número é
recusado antes de qualquer consulta.

[?] A mensagem do erro de digitação não está no acervo: a conversão é feita por uma
rotina do ambiente, que só aparece declarada, sem corpo, no lote. O posicionamento do
cursor desse erro está definido só para a coordenadoria, o número do pedido e o ano
da entrega; para o código do operador, a sub-classe, o gênero e o número da nota
fiscal a tela não define posição. Pergunta ao site.

### RN-14 — Nada é consultado sem as conferências de sessão, de tela, de acesso, de rota e de operação

Ao abrir, a tela confere: o servidor tem de estar no terminal em que a sessão foi
aberta — em outro, o acesso é encerrado; a tela tem de estar disponível, senão
**\* Tela nao disponivel \***; e o código de acesso do servidor tem de alcançar a
tela, senão **\* Acesso negado para esta matricula \***. Na confirmação são
conferidas a rota — tela fora do registro é recusada com
**\* Tela nao cadastrada \***, e operação não prevista para a tela com
**\* Operacao nao disponivel \*** — e a permissão da operação, cuja recusa é
**\* Acesso negado para esta operacao \***. Sem passar por tudo, nada é consultado.

### RN-15 — Prefixo de rota preenchido desvia a tela

Se a transação chega com o prefixo de rota preenchido, a tela não consulta nada: a
rota leva o servidor para a tela indicada nesse prefixo.

[?] Não se sabe quem preenche esse prefixo nas transações que chegam a esta tela.
Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta das notas fiscais e das quantidades de um pedido de operador logístico

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a coordenadoria regional escolar
    E tenho acesso à tela N334T

  Cenário: A tela mostra as notas do pedido consultado
    Dado que estou na tela N334T
    Quando informo a coordenadoria, o número do pedido, o ano da entrega e o código
      do operador logístico e confirmo
    Então vejo a coordenadoria, o número do pedido, o ano da entrega e o operador
      logístico, com a razão social
    E vejo uma linha por nota fiscal, com a sub-classe, o gênero, a descrição do
      gênero, o número da nota, a quantidade do gênero e as três quantidades de saldo

  Cenário: A lista é montada em 15 linhas
    Dado que consultei um pedido na tela N334T
    Então a lista de notas é montada em 15 linhas, uma por nota
    E 15 é o dimensionamento da lista, não o número de notas do pedido

  Cenário: A consulta não altera nada
    Dado que consultei um pedido na tela N334T
    Quando a consulta termina
    Então nenhum dos cadastros lidos é incluído, alterado ou excluído
    E nenhum registro de auditoria é criado
    E o único lugar em que a tela deixa marca é a área de trabalho da sessão

  Cenário: A tela aceita apenas a consulta
    Dado que estou na tela N334T
    Quando confirmo com uma operação que não é a consulta
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor fica no campo da operação
    E nada é consultado

  Cenário: A coordenadoria regional escolar é obrigatória
    Dado que a minha sessão não carrega coordenadoria
    Quando confirmo sem informar a coordenadoria
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é consultado

  Cenário: A consulta só vale para a coordenadoria da sessão
    Dado que a minha sessão carrega uma coordenadoria
    Quando informo outra coordenadoria
    Então vejo "* Usuario sem acesso a outro grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é consultado

  Cenário: O pedido é identificado pelo número e pelo ano da entrega
    Dado que estou na tela N334T
    Quando informo o número com 6 dígitos e o ano da entrega com 4 e confirmo
    Então a tela procura o pedido da minha secretaria formado por esses dois números

  Cenário: Pedido não cadastrado é recusado
    Dado que estou na tela N334T
    Quando confirmo um pedido que não existe na minha secretaria
    Então vejo "* Pedido nao cadastrado *"
    E o cursor fica no campo do número do pedido
    E nada é mostrado

  Cenário: Pedido ainda não aprovado é recusado
    Dado que estou na tela N334T
    Quando confirmo um pedido que ainda não foi aprovado
    Então vejo "* Pedido pendente de aprovacao *"
    E o cursor fica no campo do número do pedido
    E nada é mostrado

  Cenário: Pedido pendente de distribuição é recusado
    Dado que estou na tela N334T
    Quando confirmo um pedido pendente de distribuição
    Então vejo "* Pedido pendente de distribuicao *"
    E o cursor fica no campo do número do pedido
    E nada é mostrado

  Cenário: Tipo de contrato não cadastrado é recusado
    Dado que estou na tela N334T
    Quando confirmo um pedido cujo tipo de contrato não está cadastrado
    Então vejo "* Tipo contrato nao cadastrado *"
    E o cursor fica no campo do número do pedido
    E nada é mostrado

  Cenário: Pedido de contrato comum é encaminhado a outra tela
    Dado que estou na tela N334T
    Quando confirmo um pedido cujo contrato não é de operador logístico
    Então vejo "* Pedido nao e de oper.logistico. Use N034T *"
    E o cursor fica no campo do número do pedido
    E nada é consultado aqui

  Cenário: A descrição do gênero vem do cadastro de gêneros
    Dado que consultei um pedido na tela N334T
    Quando olho a linha de uma nota fiscal
    Então a descrição do gênero é a do cadastro de gêneros para a sub-classe, o
      gênero e a data de emissão daquela nota
    E o gênero marcado como excluído não é considerado

  Cenário: As quantidades de saldo são as do item
    Dado que consultei um pedido na tela N334T
    E que duas notas do pedido são do mesmo item
    Então as duas linhas repetem as mesmas quantidades de saldo do item
    E a quantidade do gênero é a de cada nota

  Cenário: Pedido sem notas é recusado
    Dado que estou na tela N334T
    Quando confirmo um pedido que não tem nota nenhuma lançada
    Então vejo "* Pedido sem notas cadastradas *"
    E o cursor fica no campo do número do pedido
    E nada é mostrado

  Cenário: Pedido com notas pendentes de confirmação é recusado
    Dado que estou na tela N334T
    Quando confirmo um pedido que não tem nota lançada mas tem nota com entrada
      ainda não confirmada
    Então vejo "* Pedido com notas pendentes de confirmacao *"
    E o cursor fica no campo do número do pedido
    E nada é mostrado

  Cenário: O nome do operador logístico acompanha o pedido
    Dado que consultei um pedido na tela N334T
    Então vejo o código do operador logístico do pedido
    E vejo a razão social desse operador, lida no cadastro de operadores logísticos

  Cenário: Digitação não numérica é recusada
    Dado que estou na tela N334T
    Quando digito letra em um dos campos numéricos e confirmo
    Então o campo é recusado antes de qualquer consulta

  Cenário: Nada é consultado sem as conferências de sessão, de tela, de acesso, de rota e de operação
    Dado que estou na tela N334T
    Quando a conferência do terminal, do registro da tela, do código de acesso, da
      rota ou da operação não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *",
      "* Tela nao cadastrada *", "* Operacao nao disponivel *" ou
      "* Acesso negado para esta operacao *"
    E nada é consultado
    E, se o terminal não for o da sessão, o acesso é encerrado

  Cenário: Prefixo de rota preenchido desvia a tela
    Dado que a transação chega à tela N334T com o prefixo de rota preenchido
    Quando a tela começaria a consultar
    Então sou levado para a tela indicada no prefixo
    E nada é consultado

  Cenário: A tela retoma o pedido da última consulta
    Dado que consultei um pedido na tela N334T
    Quando abro a tela N334T de novo
    Então o pedido da última consulta já aparece, com a coordenadoria, o operador
      logístico e o seu nome
    E não preciso informá-lo outra vez

  Cenário: Sem pedido guardado a tela abre em branco
    Dado que a minha sessão não tem pedido guardado
    Quando abro a tela N334T
    Então os campos do pedido vêm em branco
    E a coordenadoria vem preenchida com a da sessão
```
