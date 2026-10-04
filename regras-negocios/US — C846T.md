# US — C846T — Consulta da estimativa da alimentação escolar do grupo

## Estória

Como **servidor de CRE**, quero **consultar a estimativa da alimentação escolar do meu grupo,
por subclasse e gênero, dentro de um período**, para que **eu confira, linha a linha, o que a
estimativa pede em cada refeição e segmento e leve o relatório dela para conferência, sem
risco de alterar o que está gravado**.

A estimativa da alimentação escolar é montada por grupo e por gênero de alimento e é
detalhada por refeição e por segmento de atendimento dentro de um período — que vai de uma
data de início a uma data limite, e é a data limite que distingue um período do outro. Quem
responde pelo grupo precisa poder olhar esse detalhe e levá-lo impresso para conferência; é
isso que esta tela faz, e ela **só lê**: onde é preciso mexer, ela encaminha para as telas que
mantêm. Sem ela, a conferência do grupo dependeria de quem tem a tela de manutenção, que
altera o que está gravado.

## Contexto

Jornada S000M → C000M → C800M → C840M → C846T.

Ator: servidor de CRE — informa o grupo, a subclasse, o gênero e o período, consulta a
estimativa detalhada por refeição e segmento, encomenda o relatório e passa às telas de
manutenção quando precisa de mais.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os três menus do caminho — `C000M`, `C800M` e `C840M` —
só encaminham e não gravam nada.

O contexto de que a C846T se serve — a matrícula, o privilégio, o tipo de órgão, a coordenação
regional escolar e a data do sistema — é o que a entrada deixou na sessão; a tela não
recalcula nada disso. O tipo de órgão da sessão entra na chave de todas as procuras: é ele que
limita o que a tela alcança. A tela guarda na sessão a última seleção consultada e reabre com
ela.

As informações que esta tela mostra são as mesmas que a tela de manutenção da estimativa
altera e que a tela de preços precifica; é para essas duas que ela encaminha.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela é de consulta, e só a consulta passa

Ao se abrir, a tela repõe a operação como **consulta** e deixa a impressora em branco.
Qualquer outra operação é recusada com **\* Operacao nao disponivel. Use CON \***, com o
cursor no campo da operação, e **sem ler cadastro nenhum**. Alteração e exclusão, portanto,
não se fazem por esta tela.

[?] A recusa manda usar **CON**, mas o valor que a tela aceita é o código interno da consulta;
nenhum documento do material lido diz que o terminal traduz o mnemônico antes de enviar. Ou o
formulário traduz, ou quem seguir a mensagem é recusado. Pergunta ao site.

[?] A recusa só é alcançável se a máscara oferecer a quem opera um campo de operação, e a
abertura da tela repõe a consulta sozinha; a ficha da tela não lista rótulo de campo de
operação. Se a máscara não tem esse campo, a recusa é trecho sem uso. Pergunta ao site.

### RN-02 — A consulta é de um grupo, uma subclasse, um gênero e um período

Quem opera informa o **grupo** — a coordenação regional escolar, o campo com rótulo de negócio
**COORD.REG.ESCOLA** —, a **subclasse**, o **gênero** e o **período**, este em dia, mês e ano
de início e dia, mês e ano limite. É essa combinação, junto com o tipo de órgão da sessão, que
identifica a estimativa: **há um registro por grupo, subclasse, gênero e data limite**. O
cadastro da estimativa tem **17 campos** e capacidade para **100.000 registros**; o detalhe
dela tem **18 campos** e capacidade para **500.000** — capacidade é o máximo esperado
declarado, parâmetro de dimensionamento, não o volume cadastrado.

### RN-03 — Sem o dia limite, a tela adota o período do primeiro registro que achar

O dia limite é o que distingue um período do outro. Deixando-o zerado, a tela procura a
estimativa do grupo, da subclasse e do gênero **sem informar o período**, adota o período do
registro que encontrar — as datas vêm para a tela — e segue a consulta com ele.

[?] A procura sem o período não escolhe a estimativa vigente: ela alcança o **primeiro
registro na ordem das datas limite** daquele grupo, daquela subclasse e daquele gênero, que
pode ser o mais antigo. Se o esperado é a estimativa em vigor, o caminho não a garante.
Pergunta ao site.

### RN-04 — O grupo tem de estar cadastrado

Consultando um grupo que ainda não está na sessão, a tela procura o grupo no cadastro de
grupos, dentro do tipo de órgão da sessão. Não achando, a recusa é **\* Grupo nao cadastrado \***,
com o cursor no campo do grupo, e a consulta para ali.

### RN-05 — A subclasse e o gênero têm de estar cadastrados, e o gênero ativo

A subclasse e o gênero informados são procurados no cadastro de gêneros, pelo par subclasse e
gênero, tomando a data limite do período como data de início da vigência. Não achando, ou
achando o gênero **inativo**, a recusa é a mesma — **\* Genero nao cadastrado \*** —, com o
cursor no campo da subclasse. Para a **subclasse 99** a procura é em outro cadastro de
gêneros, pelo mesmo par, e o gênero vem marcado com um asterisco.

[?] O que a subclasse 99 identifica, por que ela usa outro cadastro de gêneros e o que a marca
de asterisco quer dizer em negócio não estão no corpus lido nem no manual. Pergunta ao site.

[?] A data limite do período é usada como **início** da vigência do gênero, na chave da
procura; não se conclui do acervo se isso significa "o gênero vigente no período" ou se é só o
jeito de posicionar a leitura — nenhum rótulo da tela mostra vigência de gênero. Pergunta ao
site.

### RN-06 — Tem de haver estimativa registrada para o grupo, a subclasse e o gênero

A tela procura a estimativa do grupo, da subclasse e do gênero no período informado. Não
achando, a recusa é **\* Genero sem registros de estimativa cadastrados \***, com o cursor no
campo da subclasse. A mesma recusa aparece quando o grupo tem estimativa, mas nenhuma linha de
detalhe para aquela combinação de refeição e segmento.

### RN-07 — O que a tela mostra da estimativa

Achando, a tela mostra o que está gravado: a **situação** da estimativa — **FECHADO** quando
ela está fechada, e um traço quando não está —, a **quantidade estimada**, o **valor
inicial**, o **valor do preço** e a **descrição do gênero**. A tela mostra também o grupo pelo
código e a data do sistema, que vêm da sessão.

[?] O que é, em negócio, uma estimativa **fechada** — quem a fecha, e o que ela fecha — não
está nos fontes desta jornada nem no material lido: a tela só distingue a que está marcada
como fechada das demais. Pergunta ao site.

### RN-08 — A grade: até treze linhas de refeição e segmento

A estimativa é detalhada por **refeição** e por **segmento** de atendimento, e a grade mostra
**até treze linhas**. Cada linha traz o código e a descrição da refeição, o código e a
descrição do segmento, uma quantidade, uma quantidade e um valor pedidos, e a marca **\*** nas
linhas cuja **quantidade calculada é zero**. Cada linha tem também um campo de ação de uma
posição.

[?] A marca **\*** das linhas sem quantidade calculada não tem rótulo nem definição no corpus
lido: não se conclui se ela pede atenção, se indica pendência ou se é só um sinal de
divergência. Pergunta ao site.

### RN-09 — A consulta não grava nada

Os cadastros que a tela enxerga existem declarados para gravação e para exclusão — **dez**
cadastros, com a rotina de gravar e a de apagar cada um —, mas **nenhum caminho desta tela
executa qualquer delas**. A única gravação viva é a do pedido de relatório (RN-10). Consultar,
inclui, não altera e não exclui nada, e não gera lançamento de auditoria: declarar não é
executar.

### RN-10 — Com a impressora informada, a tela encomenda o relatório

Preenchida a **impressora**, e passando por todas as conferências, a tela registra na fila de
pedidos de relatório um pedido do **relatório de estimativa do grupo** — com o tipo de órgão,
o grupo, a data limite, a subclasse, o gênero, a impressora, a estação, a matrícula e o e-mail
de quem opera, lido do cadastro de funcionários — e toma para ele o número seguinte da fila.
Em seguida entrega o processamento à fila de jobs. Deixando a impressora em branco, o pedido
não é feito: a passagem segue para a marca da linha (RN-13).

[?] O caminho que encomenda o relatório não monta aviso nenhum para a tela: quem operou não
recebe confirmação de que o pedido entrou na fila. Se o projeto previa um aviso, ele não está
nos fontes desta jornada. Pergunta ao site.

[?] A entrega à fila de processamento só acontece quando o produto em execução não é o LINC; o
que a tela faz no caso contrário não está nos fontes desta jornada. Pergunta ao site.

### RN-11 — Um pedido do mesmo relatório já na fila recusa o pedido novo

Preenchida a impressora, e antes de registrar, a tela procura na fila de pedidos um pedido
daquele relatório **para o mesmo grupo**. Achando, avisa **\* Relatorio em processamento.
Aguarde. \***, devolve o cursor ao campo do grupo e **não registra nada** — nem o pedido novo,
nem o processamento. A recusa vale para o grupo inteiro: não é preciso que a subclasse e o
gênero sejam os mesmos.

### RN-12 — A tela passa à C845T quando se pede a consulta

Preenchido o campo de consulta com **S**, a tela entrega à **C845T** o grupo, a subclasse e o
gênero que estão em tela e a abre — em consulta, que é a operação que ela mesma tem. A C845T é
a tela que mantém a estimativa.

[?] O campo de consulta tem uma posição e nenhum rótulo no material lido; o corpus não diz o
que a letra **S** significa em negócio, nem quem a preenche. Pergunta ao site.

### RN-13 — A tela passa à C847T em alteração quando se marca a linha

Marcada a linha em foco no campo de ação com **X** e **estando a impressora em branco**, a
tela entrega à **C847T** o grupo, a subclasse, o gênero, o período e a refeição e o segmento
daquela linha — com as quantidades, os valores e a situação lidos da estimativa — e marca a
operação como **alteração**; a C847T abre em alteração. É por aqui que a linha da estimativa
chega à tela onde o preço dela é mantido.

[?] O campo de ação da linha tem uma posição e nenhum rótulo no material lido, e o corpus não
diz o que a letra **X** significa em negócio. Pergunta ao site.

[?] A passagem para a tela de preços só acontece com a impressora em branco; com a impressora
preenchida, a passagem encomenda o relatório e termina. A tela escolhe um desfecho e descarta
o outro na mesma passagem; se o esperado é permitir os dois, o caminho não permite. Pergunta
ao site.

### RN-14 — A digitação passa pela edição numérica, e o cursor volta ao campo recusado

**11 campos** passam pela edição numérica antes de qualquer leitura: o grupo, a subclasse, o
gênero, as três partes do início do período, as três partes do limite e o par de refeição e
segmento da linha em foco. Campo em branco vale zero; o que não for número é recusado, a
passagem não segue e o cursor volta ao campo recusado. A impressora e o campo de consulta não
são numéricos e não passam por essa edição.

[?] O que quem opera vê quando a digitação é recusada — se há mensagem, e qual — não está nos
fontes desta jornada: a rotina que faz a edição numérica é importada e não faz parte do acervo
lido. Pergunta ao site.

### RN-15 — Falha de banco interrompe a passagem e avisa

Todo acesso a dados testa o erro do banco; o erro de leitura e o de gravação viram avisos
diferentes, despachados pela rotina de comunicação — a passagem para ali, sem completar o
resto.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar a estimativa da alimentação escolar do grupo por subclasse e gênero

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C846T

  Cenário: Consulta de uma estimativa existente
    Dado que existe estimativa do meu grupo para a subclasse e o gênero no período informado
    Quando informo o grupo, a subclasse, o gênero e as datas do período
    Então vejo a situação, a quantidade estimada, o valor inicial, o valor do preço e a descrição do gênero
    E vejo, em cada linha da grade, a refeição, o segmento, as quantidades e os valores da estimativa
    E nenhum registro é incluído, alterado ou excluído

  Cenário: Consulta sem informar o dia limite
    Dado que deixo o dia limite zerado
    Quando informo só o grupo, a subclasse e o gênero e envio a consulta
    Então a tela adota o período do primeiro registro que encontrar para essa combinação
    E as datas do período aparecem preenchidas na tela

  Cenário: Estimativa fechada
    Dado que a estimativa do meu grupo para a subclasse e o gênero está fechada
    Quando envio a consulta
    Então vejo a situação FECHADO

  Cenário: Linha sem quantidade calculada
    Dado que uma das linhas do detalhe da estimativa está sem quantidade calculada
    Quando envio a consulta
    Então essa linha aparece marcada com "*"

  Cenário: Operação diferente de consulta
    Dado que estou na tela C846T
    Quando informo uma operação que não é a consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nenhum cadastro é lido nesse caminho

  Cenário: Grupo não cadastrado
    Dado que informo um grupo que não existe no cadastro de grupos do meu tipo de órgão
    Quando envio a consulta
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo do grupo
    E nada é consultado

  Cenário: Gênero não cadastrado ou inativo
    Dado que informo uma subclasse e um gênero que não estão no cadastro de gêneros, ou um gênero inativo
    Quando envio a consulta
    Então vejo a mensagem "* Genero nao cadastrado *"
    E o cursor volta ao campo da subclasse
    E nada é preenchido

  Cenário: Combinação sem estimativa registrada
    Dado que não há estimativa para o meu grupo, a subclasse e o gênero no período informado
    Quando envio a consulta
    Então vejo a mensagem "* Genero sem registros de estimativa cadastrados *"
    E o cursor volta ao campo da subclasse
    E nada é preenchido

  Cenário: Grupo com estimativa, mas sem detalhe
    Dado que existe estimativa do meu grupo para a subclasse e o gênero, mas sem nenhuma linha de refeição e segmento
    Quando envio a consulta
    Então vejo a mensagem "* Genero sem registros de estimativa cadastrados *"
    E nada é preenchido

  Cenário: Impressora informada encomenda o relatório
    Dado que a estimativa do meu grupo existe e não há pedido dela na fila
    Quando informo a impressora e envio a consulta
    Então o pedido do relatório de estimativa do grupo é registrado com o número seguinte da fila
    E o pedido leva a impressora, a estação, a matrícula e o e-mail de quem opera
    E o processamento é entregue à fila

  Cenário: Pedido do mesmo relatório já na fila
    Dado que há um pedido do relatório de estimativa em processamento para o meu grupo
    Quando informo a impressora e envio a consulta
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo do grupo
    E nada é registrado

  Cenário: Pedir a consulta passa para a tela de manutenção
    Dado que estou consultando a estimativa do meu grupo
    Quando preencho o campo de consulta com S
    Então a tela C846T entrega o grupo, a subclasse e o gênero à tela C845T
    E a C845T abre em consulta

  Cenário: Marcar a linha passa para a tela de preços em alteração
    Dado que estou consultando a estimativa do meu grupo e a impressora está em branco
    Quando marco a linha em foco com X no campo de ação
    Então a tela C846T entrega à tela C847T o grupo, a subclasse, o gênero, o período e a refeição e o segmento da linha
    E a C847T abre em alteração

  Cenário: Digitação não numérica
    Dado que digito no grupo, na subclasse, no gênero ou em uma das partes das datas algo que não é número
    Quando envio a consulta
    Então a passagem não segue antes de ler qualquer cadastro
    E o cursor volta ao campo recusado

  Cenário: Falha de banco durante a leitura
    Dado que o banco falha na leitura de um dos cadastros da consulta
    Quando envio a consulta
    Então a passagem para e um aviso é despachado pela rotina de comunicação
```
