# US — C213C — Consulta da tabela de preços do período

## Estória

Como **servidor de CRE com a tela C213C autorizada**, quero **consultar a tabela de preços
de um período — vendo, gênero por gênero, a descrição, a unidade de medida e o preço, e até
quando aquela tabela vale — e, quando precisar, pedir a impressão dela para o período que eu
indicar**, para que **a secretaria confira e divulgue os preços vigentes sem abrir o cadastro
e sem depender de chamado ao suporte**.

Os preços dos gêneros de material são tabelados por período de vigência: cada tabela começa
numa data e vale até um limite. Quem precisa do preço de um gênero precisa saber de que
período está falando, e é isto que esta tela resolve — informado o início do período, ela
mostra os gêneros daquela tabela com o preço de cada um, na ordem do cadastro. Ela é também
a porta da impressão: com a impressora informada, a tela pede a impressão da tabela para o
período escolhido, e é esse pedido que coloca o relatório na fila — e se a data informada não
tiver tabela, ou se o período da impressão estiver errado, nada é mostrado nem pedido.

## Contexto

Jornada S000M → C000M → C015M → C213C.
Ator: servidor de CRE — consulta a tabela de preços de um período, percorre a lista de gêneros
e, quando precisa, pede a impressão dela.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A `C213C` é uma tela de consulta e termina nela mesma: não abre outra tela e não mantém
cadastro nenhum. O que ela usa da sessão — a matrícula de quem opera, a estação, o tipo de
órgão, as datas do sistema e o e-mail do servidor — é o que a entrada deixou; a tela não
recalcula. A única gravação que ela executa é o pedido de impressão (RN-09).

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O que a tela mostra

A consulta é a **tabela de preços de um período**. Informada a data de início da vigência —
dia, mês e ano —, a tela mostra os **gêneros de material** daquela tabela, um por linha, com
o **código do gênero** (classe, subclasse e gênero), a **descrição resumida do gênero**, a
**unidade de medida** e o **preço**, com duas casas decimais. Junto vêm o **limite de
vigência** da tabela — dia, mês e ano — e a **data do sistema**. São **doze gêneros por vez**,
na ordem do cadastro.

### RN-02 — A tela não altera a tabela de preços nem o cadastro de gêneros

A tela é de consulta: lê a tabela de preços e o cadastro de gêneros de material, e não
inclui, não altera e não exclui nada em nenhum dos dois. A operação que ela apresenta é
sempre a consulta, e o único caminho que grava é o do pedido de impressão (RN-09).

### RN-03 — A data de início escolhe a tabela

A data de início do período identifica a tabela. Quando o operador informa uma data
diferente da que está sendo mostrada, a tela procura a tabela daquela data; não existindo, a
recusa é **\* Tabela nao cadastrada para esta data \***, com o cursor de volta no dia do
início, e nada é pedido para impressão.

[?] Existe um segundo aviso, **\* Tabela sem generos cadastrados \***, que não foi possível
alcançar: o caminho que o exibiria só é percorrido depois de a tela já ter marcado que achou
a tabela, e a marca que o dispararia nunca sobrevive até lá. Ou ele vale para um caso que não
passa por este caminho, ou ficou inalcançável. Pergunta ao site.

### RN-04 — Cada campo informado é conferido antes de a consulta seguir

Os campos de data e de classificação são conferidos como numéricos — são **dez**: o dia, o
mês e o ano do início do período, a classe, a subclasse, o gênero e os quatro campos do
período de impressão (mês e ano iniciais, mês e ano limites). O que estiver em branco é
tratado como zero e os zeros à esquerda são descartados. O campo recusado devolve o cursor a
si mesmo e a consulta não segue.

[?] O texto que o operador vê quando um valor não numérico é recusado não está na tela: a
conferência é de uma rotina de biblioteca, que não veio no lote. Pergunta ao site.

[?] A tela confere se o que foi digitado é **número**, mas não se é **data**: mês treze,
dia trinta e dois e ano fora de faixa passam pela conferência e só aparecem como "tabela não
cadastrada" mais adiante. Se existe conferência de data válida em outro ponto, o fonte desta
tela não mostra. Pergunta ao site.

### RN-05 — Preenchida a impressora, a tela exige o período da impressão

Preenchendo a **impressora**, o operador pede a impressão da tabela do período e a tela passa
a exigir o **período da impressão** — mês e ano iniciais e mês e ano limites —, conferindo-o.
Faltando o período, a recusa é **\* Informe periodo para impressao \***, com o cursor de volta
na impressora; com o início posterior ao limite, é
**\* Periodo inicial maior que final \***, com o cursor no mês inicial da impressão; com mais
de **doze meses**, contados do mês inicial, é **\* Periodo maximo = 12 meses \***, com o
cursor no mês limite da impressão. Em qualquer das três nada é registrado. Com a impressora
em branco, nada disso é conferido e nenhum pedido é feito.

### RN-06 — Um pedido do mesmo relatório já na fila bloqueia o novo

Antes de registrar, a tela verifica se já existe, na fila de requisições de impressão, um
pedido do relatório da tabela de preços ainda esperando processamento. Existindo, a resposta
é **\* Relatorio em processamento. Aguarde. \***, com o cursor de volta na impressora, e nada
é registrado. O pedido deixa a fila quando o relatório roda.

[?] A leitura da fila posiciona o código do relatório e deixa o número do pedido em branco e
zerado; o que a leitura casa de fato, e se ela distingue "pedido daquele relatório ainda
esperando" de "pedido daquele relatório já atendido", é o que os sinalizadores da leitura
dizem — e o dialeto não está explicado no corpus. Pergunta ao site.

### RN-07 — O operador só tem a consulta

A tela só opera em consulta. Se a mensagem chegar com outra operação no campo da opção, a
recusa é **\* Operacao nao disponivel, Use CON \***, com o cursor no campo da opção, e nada é
lido nem pedido.

[?] Esta recusa não fecha com o fonte: o caminho que a exibiria começa por comparar a opção
com o código interno da consulta, e a tela acabou de forçar esse mesmo código. Do jeito que
está, a comparação é sempre verdadeira e a recusa fica inalcançável: ou ela vale para outro
caso, ou o caminho ficou morto, e isso importa porque é ele que hoje garantiria a consulta.
Pergunta ao site.

### RN-08 — A tela não encadeia: não abre outra tela

A consulta termina na própria tela. Mesmo que a mensagem traga outra tela no campo da próxima
tela, a tela não a abre e o fluxo termina ali — a tela de destino da jornada é um ponto final.

### RN-09 — A impressão pedida é registrada e o relatório é despachado

Passadas as conferências, a tela registra **um pedido** na fila de requisições de impressão,
com o **número seguinte** ao do último pedido, o relatório da tabela de preços do período, a
**matrícula** de quem opera, o **terminal**, a **estação**, o **tipo de órgão** e a data da
requisição, e entrega o processamento do relatório com o **período informado** e a
**impressora**, para o **e-mail** do servidor, lido do cadastro de funcionários; o pedido sai
com **uma cópia**. É esta a única gravação que a tela executa.

[?] Quem é o relatório, para o negócio, não foi possível dizer: o código do relatório está
fixo na tela e não há, no dicionário de dados nem no despacho das telas que vieram no lote,
o nome com que a secretaria o conhece. O que se pode afirmar é que ele lê a mesma tabela de
preços que a consulta. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consulta e impressão da tabela de preços do período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C213C

  Cenário: Consulta da tabela do período
    Dado que existe tabela de preços para a data de início informada
    Quando informo a data de início e consulto
    Então vejo o código, a descrição, a unidade de medida e o preço de cada gênero daquela tabela
    E vejo o limite de vigência da tabela
    E nada foi gravado

  Cenário: A lista traz doze gêneros por vez
    Dado que a tabela do período tem mais de doze gêneros
    Quando consulto o período
    Então vejo doze gêneros, na ordem do cadastro
    E nada foi gravado

  Cenário: A consulta não muda a tabela de preços
    Dado que consulto o período e informo classe, subclasse e gênero
    Quando a tela apresenta a consulta
    Então nenhum preço é incluído, alterado ou excluído
    E nenhum gênero de material é incluído, alterado ou excluído
    E a operação apresentada é a consulta

  Cenário: Data de início sem tabela cadastrada
    Dado que informo uma data de início diferente da que está sendo mostrada
    E não existe tabela de preços para essa data
    Quando consulto
    Então vejo a mensagem "* Tabela nao cadastrada para esta data *"
    E o cursor volta para o dia do início
    E nada é pedido para impressão

  Cenário: Valor não numérico em um campo do período
    Dado que informo um valor não numérico no mês do início do período
    Quando consulto
    Então a consulta é recusada
    E o cursor volta para o campo do mês do início
    E nada foi gravado

  Cenário: Impressora informada sem o período de impressão
    Dado que informo a impressora e deixo o período da impressão em branco
    Quando peço a impressão
    Então vejo a mensagem "* Informe periodo para impressao *"
    E o cursor volta para a impressora
    E nada é registrado

  Cenário: Período de impressão com o início depois do limite
    Dado que informo a impressora e um período de impressão com o início depois do limite
    Quando peço a impressão
    Então vejo a mensagem "* Periodo inicial maior que final *"
    E o cursor volta para o mês inicial da impressão
    E nada é registrado

  Cenário: Período de impressão maior que doze meses
    Dado que informo a impressora e um período de impressão maior que doze meses
    Quando peço a impressão
    Então vejo a mensagem "* Periodo maximo = 12 meses *"
    E o cursor volta para o mês limite da impressão
    E nada é registrado

  Cenário: Relatório da tabela já na fila
    Dado que já existe um pedido do relatório da tabela esperando processamento
    E informo a impressora e um período de impressão válido
    Quando peço a impressão
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta para a impressora
    E nada é registrado

  Cenário: Sem impressora, nenhuma impressão é pedida
    Dado que deixo a impressora em branco
    Quando consulto o período
    Então a tabela é mostrada
    E nenhum pedido é registrado na fila

  Cenário: Impressão pedida e registrada
    Dado que informo a impressora e um período de impressão válido
    E não há pedido do relatório da tabela na fila
    Quando peço a impressão
    Então um pedido é registrado na fila, com o número seguinte ao último
    E o relatório do período é entregue para processamento com a impressora e o meu e-mail
    E nenhum preço da tabela é alterado

  Cenário: A consulta termina na própria tela
    Dado que a mensagem traz outra tela no campo da próxima tela
    Quando a tela processa a consulta
    Então nenhuma outra tela é aberta
    E o fluxo termina ali
```
