# US — N317T — Tratar notas fiscais do contrato

## Estória

Como **servidor da CRE**, quero **tratar as notas fiscais de um contrato de operador
logístico — vendo as notas daquele contrato com os pedidos a que elas pertencem,
encaminhando cada nota para a tela que a detalha ou estornando-a —**, para que
**nenhuma nota fique pendurada sem destino e o saldo do contrato acompanhe o que já
foi entregue**.

A nota fiscal de um contrato de operador logístico não se resolve sozinha: ou ela
segue para ser detalhada, ou é estornada quando não vale mais. É aqui que isso
acontece, e só aqui. E o que a tela faz ao tratar uma nota não é consulta: ela
devolve as quantidades ao saldo do contrato e aos pedidos, marca os pedidos, apaga os
itens da nota e apaga a própria nota. Sem isso, o contrato continuaria mostrando como
disponível uma quantidade já entregue, e a nota continuaria presa no contrato sem
ninguém para tirá-la.

## Contexto

Jornada S000M → N000M → N050M → N300M → N317T.

Ator: servidor de CRE — informa a coordenadoria regional escolar, o tipo de contrato
e o operador logístico, vê as notas daquele contrato e dá destino a cada nota.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As telas anteriores da jornada — a `N000M`, a `N050M` e a `N300M` — só encaminham: o
que a `N317T` usa da sessão (a matrícula, o tipo de órgão, a coordenadoria regional
escolar) é o que a entrada deixou. As regras abaixo são só as da tela desta jornada.

A `N317T` **não é folha**: ela encadeia na `N326T` sem passar por menu nenhum. O que
ela entrega à tela seguinte é regra desta estória tanto quanto da outra — está na
RN-11.

---

## Regras de negócio

### RN-01 — A tela trata as notas de um contrato e mostra até 13 delas de uma vez

O assunto da tela é a **nota fiscal de um contrato de operador logístico**. O servidor
informa a **coordenadoria regional escolar**, o **tipo de contrato** e o **operador
logístico** e vê, para essa combinação, as notas que existem.

A tela mostra **até 13 notas ao mesmo tempo**, uma por linha. De cada linha se vê o
**número da nota fiscal**, o **número do pedido**, a barra separadora, o **ano da
entrega**, o **órgão filho** (código e nome), o **fornecedor** (código e nome) e a
**situação da nota**. E é na mesma linha que o servidor informa a nota com que quer
trabalhar: o **número da nota** e a **situação** são campos da linha.

O número do pedido e o ano da entrega que a linha mostra **não são digitados**: saem
do próprio número do pedido que a nota carrega — os seis primeiros dígitos viram o
número do pedido e os quatro últimos, o ano da entrega — e é por isso que a linha
traz a barra entre os dois.

Fora da lista a tela mostra a **data do sistema**, o **órgão** do servidor e o
**nome do operador logístico**, e recebe o campo **NRPEDAUX**.

São **dez** os campos de resultado que a tela limpa antes de procurar qualquer coisa
— a data, o órgão, o nome do operador, o número do pedido, a barra, o ano da entrega,
o código e o nome do órgão filho e o código e o nome do fornecedor. O que aparece na
tela é sempre o que a leitura desta vez encontrou, nunca o resto da leitura anterior.

[?] O campo NRPEDAUX é o único, fora os cinco conferidos na RN-03, que o servidor
digita — e o fonte não fecha o que ele faz. Ele é preenchido pela própria tela com o
**número da última nota que ela leu**, e com esse número a tela procura de novo a
nota; mas o resultado dessa procura vai para a memória da sessão, e a confirmação
depois decide por outro campo, o número da nota digitado na linha. Ou o campo é a
posição da leitura e a confirmação deveria usá-lo, ou é só o retrato da última nota
lida e a procura é resto de geração. Pergunta ao site.

### RN-02 — A tela abre em consulta e retoma a combinação da última vez

Ao abrir, se a sessão não tem modo guardado, a tela **adota a consulta**; ela só
troca o modo quando a sessão já traz outro.

A **coordenadoria regional escolar, o tipo de contrato e o operador logístico** são
guardados na área da sessão a cada confirmação e **repostos nos campos na abertura
seguinte**. Por isso reabrir a tela sem mudar nada não gera recusa: ela reabre no
mesmo ponto em que ficou.

A tela também repõe a coordenadoria que a sessão carrega quando a área ainda não tem
nenhuma.

### RN-03 — Cinco campos são conferidos como número antes de qualquer leitura

São **cinco** os campos que a tela edita antes de procurar qualquer cadastro: a
**coordenadoria regional escolar** (2 dígitos), o **tipo de contrato** (3), o
**operador logístico** (4), o **número da nota fiscal** (9) e o **NRPEDAUX** (9). O
que não for número é recusado **antes** de a tela ler qualquer cadastro, com o campo
de volta para ser corrigido.

[?] Dos cinco, **quatro** têm posição de cursor definida — a coordenadoria, o tipo de
contrato, o operador e o NRPEDAUX. Para o **número da nota fiscal** a tela não define
posição nenhuma: o erro é registrado no campo, mas o cursor não volta até ele. Se é
defeito ou se o cursor fica onde estava por desenho, o fonte não diz.

[?] O campo do operador logístico é o único dos cinco que a tela não nomeia em
português: ela o confere pelo próprio identificador interno do campo. A máscara da
tela não veio no lote, e o rótulo que o servidor lê nesse campo é pergunta ao site.

### RN-04 — A tela só aceita alteração e consulta

Se a transação chegar em qualquer outro modo, a tela recusa com **\* Opcao nao
disponivel. Use ALT ou CON \***, com o cursor no campo do modo, e **nada é lido nem
gravado**. Inclusão, exclusão e qualquer outro modo ficam de fora: o que a tela faz
com uma nota ela faz em alteração, e o que ela mostra ela mostra em consulta.

### RN-05 — Em alteração, a combinação tem de ser a última consultada

Confirmar em **alteração** com uma coordenadoria, um tipo de contrato ou um operador
**diferentes** dos da última consulta é recusado com **\* Consulte antes de atualizar
\***, com o cursor na coordenadoria, e nada é lido nem gravado.

É a regra que explica a alteração inteira: só se altera o que já se consultou. E por
isso, quando a combinação é a mesma, a tela **não reconfere** a coordenadoria, o tipo
de contrato nem o operador — eles já passaram pela conferência na consulta em que
foram informados. A reconferência destes três cadastros, nas RN-06 a RN-08, só
acontece quando a combinação **muda** — o que, em alteração, a regra desta seção já
impede.

### RN-06 — A coordenadoria regional escolar é a da sessão, e tem de existir

Três guardas, todas com o cursor de volta ao campo da coordenadoria e sem ler nem
gravar mais nada:

- informar uma coordenadoria **diferente da que a sessão carrega** é recusado com
  **\* Usuario sem acesso a este grupo \***;
- com a sessão **sem coordenadoria**, deixar o campo em branco é recusado com
  **\* Informe o grupo \*** — o sistema não escolhe pelo servidor;
- a coordenadoria informada tem de **existir para o tipo de órgão da sessão**; não
  existindo, a recusa é **\* Grupo nao cadastrado \***.

### RN-07 — O tipo de contrato tem de existir e ser de operador logístico

O tipo de contrato é exigido e procurado no cadastro de tipos de contrato **pelo tipo
de órgão da sessão**. Não existindo, a recusa é **\* Tipo de contrato nao cadastrado
\***. Existindo, ele ainda tem de estar marcado como de **operador logístico**; não
estando, a recusa é **\* TC nao e de operador logistico \***. Nas duas o cursor volta
ao campo do tipo de contrato e nada é gravado.

### RN-08 — O operador logístico tem de estar cadastrado

O operador informado é procurado no cadastro de operadores logísticos. Não existindo,
a recusa é **\* Ope.logisitico nao cadastrado \***, com o cursor de volta ao campo e
sem gravar nada. Em branco, cai na mesma recusa. Passando, é o **nome** do operador
que passa a aparecer na tela, e é a combinação confirmada — coordenadoria, tipo de
contrato e operador — que fica guardada na sessão para a abertura seguinte.

### RN-09 — Sem nota para a combinação, a tela avisa

Ao abrir, a tela procura a nota daquela combinação. Não achando nenhuma, ela avisa
**\* TC sem notas cadastradas \***, esquece a nota guardada e não mostra nada. É o
desfecho natural de um contrato que ainda não tem nota lançada, ou de uma combinação
que nunca foi usada.

### RN-10 — A consulta não grava nada

Em **consulta**, a confirmação sai da tela sem tocar em registro nenhum: nem no saldo
do contrato, nem nos pedidos, nem nos itens, nem na nota, nem no rastro de auditoria.
A única coisa que muda é a memória da sessão, que é o que a RN-02 descreve.

É a mesma regra vista dos dois lados: a consulta é o modo em que a tela **mostra**, e
é na **alteração** que ela escreve (RN-12 e RN-13).

### RN-11 — A nota marcada com a situação C é entregue à tela N326T, em consulta

Preenchida a linha com o número de uma nota e a **situação C**, a tela não altera
nada: ela **lê a nota, os itens e os cadastros que a cercam** — o órgão filho, o
fornecedor, o operador, a modalidade da nota — e **entrega tudo à tela `N326T`**,
deixando-a abrir em **consulta**. Os dados que ela entrega são exatamente os que a
`N326T` espera encontrar: a nota, a modalidade da nota e a sua descrição, o tipo de
órgão, a coordenadoria, o tipo de contrato, o operador e o seu nome, o fornecedor e a
sua razão social, o órgão filho e o seu nome, o pedido, o ano da entrega, o número da
chamada da nota fiscal e as três datas de emissão.

A tela seguinte **só aceita a nota em consulta**: chegando em alteração, a `N326T`
não mostra nada e devolve o controle. E ela ainda confere um **carimbo da tela de
origem** — a `N317T` grava na área da sessão o código `N314T` justamente para que a
`N326T` reconheça de onde a nota veio; sem esse carimbo, a `N326T` manda o servidor
de volta ao menu `N300M` em vez de abrir a nota.

[?] O carimbo e a `N326T` não fecham. A `N326T` apaga esse mesmo campo ao inicializar
o programa e só confere o carimbo no caminho de abertura — que não é o caminho pelo
qual a `N317T` a chama, porque a chamada entra como transação. Ou a guarda do carimbo
não roda no encadeamento e a conferência é inútil, ou ela roda e, na primeira vez que
a `N326T` abre na sessão, a nota volta para o menu. A leitura do acervo não decide
qual dos dois, e a operação é inalcançável por um dos dois caminhos: escolher um lado
seria inventar. Pergunta ao site.

### RN-12 — Confirmar com a situação E devolve as quantidades e apaga a nota

Em **alteração**, preenchida a linha com o número de uma nota e a **situação E**,
quando a nota **já está no registro de destino**, a tela desfaz o que a nota
representava:

- para **cada item** da nota, a quantidade do item é **subtraída do saldo do
  contrato** — no registro de saldo daquele tipo de órgão, tipo de contrato,
  fornecedor, coordenadoria, subclasse, gênero e data limite — e o saldo é regravado;
- a mesma quantidade é **subtraída do saldo do item no pedido**, o item do pedido é
  regravado e marcado com a situação de estorno;
- o **pedido** é marcado; se ele estava com a situação de fechado, passa para a de
  estorno;
- o **item da nota** é apagado, e o laço segue para o item seguinte;
- terminados os itens, a **própria nota é apagada**.

Cada uma dessas mudanças deixa o seu registro de auditoria.

Há um limite: se a **data de emissão da nota for anterior à data de início do
contrato**, a tela **não mexe no saldo do contrato** — segue adiante e ainda apaga os
itens e a nota. Não há aviso nenhum nesse caso.

[?] O **fornecedor** que a tela usa para achar o saldo do contrato não sai da nota
que está sendo estornada: sai da memória da sessão, onde só foi posto quando uma nota
daquele contrato foi **entregue** à tela seguinte (a situação C da RN-11). Se o
servidor confirmar o estorno sem ter entregue nenhuma nota antes — ou se a nota for de
outro fornecedor —, a procura do saldo não acha nada e o saldo do contrato **não é
devolvido, sem aviso nenhum**. Se é o que se pretende, ou se a tela deveria tirar o
fornecedor da própria nota, o fonte não diz. Pergunta ao site.

### RN-13 — A nota com a situação E que ainda não está no registro de destino é transferida para ele

Em **alteração**, com a **situação E**, quando a nota **ainda não está no registro de
destino**, a tela não devolve quantidade nenhuma: ela **cria o registro de destino**
— a nota e os seus itens, copiados da nota e dos itens de origem — e **apaga os
originais**. É a passagem da nota para o estágio seguinte, feita pela própria tela.

Também aqui cada escrita deixa o seu registro de auditoria, e o desfecho para quem
usa é o mesmo da RN-12: a nota sai da lista.

[?] As duas leituras — a RN-12 e a RN-13 — se distinguem só por a nota já estar ou
não no registro de destino, e é essa diferença que decide entre **devolver as
quantidades e apagar** e **transferir e apagar**. O acervo não traz o cadastro desses
dois registros (nem o da nota, nem o dos itens da nota, nem os dois de destino): sem
eles não se sabe qual dos dois é o estágio anterior e qual é o seguinte, nem por que
a passagem de estágio não devolve as quantidades. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Notas fiscais do contrato do operador logístico — consultar, entregar e estornar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão e a coordenadoria regional escolar
    E tenho acesso à tela N317T

  Cenário: A tela abre em consulta, com a combinação da última vez, e mostra as notas
    Dado que a sessão já guardou uma coordenadoria, um tipo de contrato e um operador logístico
    Quando abro a tela N317T
    Então o modo já vem como consulta
    E a coordenadoria, o tipo de contrato e o operador já vêm com os da última vez
    E vejo até 13 linhas, uma por nota, com o número da nota, o número do pedido, a
      barra, o ano da entrega, o órgão filho, o fornecedor e a situação
    E nada é gravado por essa abertura

  Cenário: O número do pedido e o ano da entrega da linha saem da própria nota
    Dado que estou na tela N317T
    E que uma das notas do contrato tem número de pedido informado
    Quando a tela mostra essa nota
    Então o número do pedido que aparece são os seis primeiros dígitos do número do pedido da nota
    E o ano da entrega que aparece são os quatro últimos
    E os dois vêm separados pela barra

  Cenário: Consultar não grava nada
    Dado que estou na tela N317T em consulta
    E que a combinação informada está válida
    Quando confirmo
    Então nenhum saldo de contrato é alterado
    E nenhum pedido, item ou nota é incluído, alterado ou excluído
    E nenhum registro de auditoria é criado

  Cenário: Valor não numérico é recusado antes das leituras
    Dado que estou na tela N317T
    Quando informo letras em um dos cinco campos conferidos
    Então a tela recusa o campo antes de procurar qualquer cadastro
    E o campo volta para ser corrigido
    E nada é gravado

  Cenário: Modo diferente de alteração e de consulta é recusado
    Dado que a transação chega à tela N317T em modo de inclusão ou de exclusão
    Quando a tela abre
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é lido e nada é gravado

  Cenário: Em alteração, combinação diferente da última consulta é recusada
    Dado que estou na tela N317T em alteração
    E que a coordenadoria, o tipo de contrato e o operador não são os da última consulta
    Quando confirmo
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo da coordenadoria
    E nada é lido e nada é gravado

  Cenário: Em alteração, a combinação da última consulta passa sem reconferir os cadastros
    Dado que estou na tela N317T em alteração
    E que a coordenadoria, o tipo de contrato e o operador são os da última consulta
    Quando confirmo
    Então a tela não reconfere a coordenadoria, o tipo de contrato nem o operador
    E segue para o tratamento da nota

  Cenário: O servidor só usa a coordenadoria da sua sessão
    Dado que a minha sessão carrega uma coordenadoria
    Quando informo outra coordenadoria
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Sem coordenadoria na sessão, o campo em branco é recusado
    Dado que a minha sessão não carrega coordenadoria
    Quando deixo a coordenadoria em branco e confirmo
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Coordenadoria não cadastrada é recusada
    Dado que estou na tela N317T
    Quando informo uma coordenadoria que não existe para o tipo de órgão da minha sessão
    Então vejo "* Grupo nao cadastrado *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Tipo de contrato não cadastrado é recusado
    Dado que estou na tela N317T
    Quando informo um tipo de contrato que não existe para o tipo de órgão da minha sessão
    Então vejo "* Tipo de contrato nao cadastrado *"
    E o cursor fica no campo do tipo de contrato
    E nada é gravado

  Cenário: Tipo de contrato que não é de operador logístico é recusado
    Dado que estou na tela N317T
    Quando informo um tipo de contrato que não está marcado como de operador logístico
    Então vejo "* TC nao e de operador logistico *"
    E o cursor fica no campo do tipo de contrato
    E nada é gravado

  Cenário: Operador logístico não cadastrado é recusado
    Dado que estou na tela N317T
    Quando informo um operador logístico que não está cadastrado
    Então vejo "* Ope.logisitico nao cadastrado *"
    E o cursor fica no campo do operador
    E nada é gravado

  Cenário: Sem nota para a combinação, a tela avisa
    Dado que estou na tela N317T
    E que não há nota para a combinação informada
    Quando a tela abre
    Então vejo "* TC sem notas cadastradas *"
    E a tela não mostra nota nenhuma
    E nada é gravado

  Cenário: A nota marcada com a situação C é entregue à tela seguinte, em consulta
    Dado que estou na tela N317T
    E que informei uma nota que existe para a combinação
    Quando preencho a linha dessa nota com a situação C e confirmo
    Então a tela entrega a nota com a modalidade, as datas de emissão, o pedido, o ano
      da entrega, o órgão filho, o fornecedor, o operador e a coordenadoria
    E a tela N326T abre com essa nota em consulta
    E nada é gravado na base por essa passagem

  Cenário: A nota marcada com a situação E tem as quantidades devolvidas e é apagada
    Dado que estou na tela N317T em alteração
    E que a nota informada está no registro de destino
    E que a data de emissão da nota não é anterior à data de início do contrato
    Quando preencho a linha com a situação E e confirmo
    Então a quantidade de cada item é subtraída do saldo do contrato e o saldo é regravado
    E a mesma quantidade é subtraída do saldo do item no pedido e o item é marcado
    E o pedido é marcado e, se estava fechado, passa para a situação de estorno
    E os itens da nota são apagados
    E a nota é apagada
    E cada mudança deixa o seu registro de auditoria

  Cenário: Nota emitida antes do início do contrato não mexe no saldo do contrato
    Dado que estou na tela N317T em alteração
    E que a data de emissão da nota é anterior à data de início do contrato
    Quando preencho a linha com a situação E e confirmo
    Então o saldo do contrato não é alterado
    E os itens da nota e a nota são apagados do mesmo jeito
    E nenhum aviso é dado

  Cenário: A nota marcada com a situação E que ainda não está no registro de destino é transferida
    Dado que estou na tela N317T em alteração
    E que a nota informada ainda não está no registro de destino
    Quando preencho a linha com a situação E e confirmo
    Então o registro de destino passa a ter a nota e os seus itens, copiados da origem
    E a nota e os itens de origem são apagados
    E nenhuma quantidade é devolvida ao saldo do contrato
    E cada escrita deixa o seu registro de auditoria
```
