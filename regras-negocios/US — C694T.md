# US — C694T — Manter os empenhos de um contrato da coordenação regional escolar

## Estória

Como **servidor de CRE**, quero **lançar, corrigir e apagar os empenhos que correram
contra um contrato da minha coordenação regional escolar**, para que **o contrato mostre,
empenho por empenho, quanto já está comprometido e quanto ainda resta disponível antes de
qualquer gasto correr contra ele**.

O empenho é o valor que o contrato reserva para um gasto: o contrato vem primeiro e os
empenhos vão sendo presos a ele, cada um com o seu número, o seu ano de referência e o seu
valor. É isso que esta tela mantém — ela abre um contrato, lista os empenhos que ele já
tem e deixa incluir um empenho novo, corrigir o valor de um empenho lançado e apagar um
empenho que não vai mais ser usado. Junto de cada empenho ela mostra o total que os
processos já consumiram dele e o saldo que sobra, e é esse total que decide se o empenho
ainda pode ser apagado. Sem isso, o contrato ficaria com um empenho amarrado por um valor
errado, ou perderia um empenho que ainda tem gasto correndo contra ele — e o valor
comprometido não teria como ser conferido por quem autoriza o gasto.

## Contexto

Jornada S000M → C000M → C050M → C690M → C694T.

Ator: servidor de CRE — abre um contrato da sua coordenação regional escolar e mantém os
empenhos vinculados a ele.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O `C000M`, o `C050M` e o `C690M` são menus e não gravam nada: apenas encaminham. A `C694T`
é aberta por esse caminho de menu, e **não** é encadeada por uma tela que lhe passe o
registro e a operação — quem chega escolhe na própria tela a opção e marca as linhas, e o
que a tela recebe de quem a chamou é só a identificação da tela de origem, levada à
conferência de rota. A `C694T` é o fim da jornada: ela não manda o usuário para outra
tela.

O contexto que a tela usa — a matrícula, o código de acesso, o privilégio, o tipo de
órgão, a coordenação regional escolar, a descrição do tipo de órgão e a data do sistema —
é o que a sessão já trazia; a tela não o recalcula.

As regras abaixo são só as da **tela desta jornada**.

## Regras de negócio

### RN-01 — Esta tela mantém os empenhos de um contrato; o contrato e o fornecedor ela só lê

A tela inclui um empenho, troca o valor de um empenho lançado e apaga um empenho. O
contrato em si, o fornecedor e os processos lançados contra o empenho não são incluídos,
alterados nem apagados por aqui: de uns e de outros a tela só lê e mostra o que eles
dizem — o tipo de órgão, a coordenação regional escolar, o tipo de contrato, o período, o
fornecedor e a razão social do contrato, e os valores de cada empenho. Por cada empenho
mexido ela deixa ainda um registro na trilha de auditoria. O cadastro de empenhos admite
**170.000 registros** e a trilha de auditoria **60 milhões** — capacidade declarada no
dicionário de dados, que é parâmetro de dimensionamento, não o que existe de fato.

### RN-02 — A tela trata um contrato e até doze empenhos por vez, em noventa campos de edição

A parte digitável da tela tem **noventa campos**: cinco de identificação da transação, a
opção de manutenção, o campo da tela seguinte, onze do contrato e as doze linhas de
empenho. Os onze do contrato são a coordenação regional escolar, o tipo de contrato, o
dia, o mês e o ano do início do período, o dia, o mês e o ano limite, o fornecedor, o
número e o ano do contrato. Cada uma das doze linhas tem **seis campos**: o número do
empenho, o ano de referência, o valor informado, o valor já comprometido, o saldo e a
marca da operação daquela linha. Fora da edição a tela mostra **quatro** campos: a
descrição do tipo de órgão, a data do sistema, a razão social do fornecedor e a linha de
mensagens.

[?] Os nomes que a máscara escreve ao lado de cada campo e de cada coluna não vieram no
lote, e a ficha do programa lista os rótulos truncados. Os nomes usados nesta estória são
os rótulos de negócio que o próprio programa carrega ao conferir cada campo; quatro
deles — o valor informado, o comprometido, o saldo e a marca da linha — aparecem no
próprio programa sem tradução. Pergunta ao site.

### RN-03 — O contrato é identificado pela coordenação regional escolar, pelo tipo de contrato, pelo período limite e pelo fornecedor

O contrato é procurado pelo tipo de órgão da sessão mais quatro dados informados na tela:
a coordenação regional escolar, o tipo de contrato, o dia, o mês e o ano **limite** do
período, e o fornecedor. Contrato de outro tipo de órgão não é encontrado.

### RN-04 — O início do período, o número e o ano do contrato são digitáveis, mas quem manda é o contrato

O dia, o mês e o ano do **início** do período, o número e o ano do contrato passam pela
conferência de número, mas não escolhem contrato nenhum. Achado o contrato, a tela devolve
a esses campos o que está gravado nele, e é esse início que vai para o empenho incluído.
Quem digitar um início, um número ou um ano diferente do que o contrato tem vê o campo
voltar com o valor do cadastro.

[?] Ou esses cinco campos são, na prática, só de leitura — e a máscara os apresenta como
digitáveis porque a conferência de número os aceita —, ou a tela deveria usá-los e ignora
o que o operador informa. Pergunta ao site.

### RN-05 — A tela só aceita consultar ou alterar, e a opção já vem preenchida

Ao abrir, se a sessão não traz opção nenhuma, a tela assume a **consulta**; voltando à
tela, ela repõe a última opção usada. Só a **consulta** e a **alteração** são aceitas:
qualquer outra opção é recusada com * Opcao nao disponivel. Use ALT ou CON *, com o cursor
de volta ao campo da opção, e nada é lido nem gravado.

[?] A conferência compara a opção recebida com os códigos internos de consulta e de
alteração do sistema, e a mensagem manda o usuário usar "ALT" ou "CON". Ou a máscara
traduz o que o operador digita antes de enviar, ou a mensagem está desalinhada da
conferência — e, no segundo caso, a alteração fica inalcançável, porque tudo o que a
mensagem ensina a digitar é recusado. O mesmo desencontro já está registrado em outras
telas deste acervo. Pergunta ao site.

### RN-06 — A coordenação regional escolar da tela é a do próprio usuário

Ao abrir, a tela preenche a coordenação regional escolar com a da sessão. Informada uma
coordenação diferente da do usuário, a recusa é * Usuario sem acesso a este grupo *, com o
cursor de volta ao campo da coordenação, e nada é consultado. Se a sessão não traz
coordenação, a tela não faz essa conferência e aceita qualquer uma.

[?] A coordenação que a tela usa vem da área da sessão, e nenhum programa desta jornada
mostra a passagem do vínculo da matrícula com a secretaria para essa área. Se ela chegar
zerada, a conferência nunca recusa e o servidor opera sobre contrato de qualquer
coordenação. Pergunta ao site.

### RN-07 — Consultar antes de alterar: a chave tem de ser a mesma da última consulta

Para **alterar** — não para consultar —, a coordenação regional escolar, o tipo de
contrato, o limite do período e o fornecedor informados têm de ser exatamente os do último
contrato que esta tela mostrou. Mudando qualquer um deles, a recusa é
* Consulte antes de atualizar *, com o cursor de volta ao campo da opção, e a tela não lê
nada. É essa conferência que obriga a consultar o contrato antes de mexer nos empenhos
dele. Na consulta, a leitura do contrato é até dispensada quando a chave informada é a
mesma da última leitura.

### RN-08 — O contrato tem de estar registrado no FINCON

Não achado o contrato, a recusa é * Contrato FINCON nao cadastrado *, com o cursor de
volta ao campo da coordenação regional escolar, e nenhuma linha de empenho é lida.

### RN-09 — O fornecedor do contrato é lido e a razão social aparece

Achado o contrato, a tela lê o cadastro do fornecedor pelo código que o contrato traz e
mostra a razão social no cabeçalho. Fornecedor não cadastrado não gera recusa nem
mensagem: a tela segue.

[?] Quando o fornecedor não está cadastrado, o fonte não permite concluir o que o
cabeçalho mostra: o caminho de "não achado" segue adiante levando adiante o conteúdo da
área do cadastro do fornecedor, que pode estar vazia ou ser o do fornecedor anterior.
Pergunta ao site.

### RN-10 — O cabeçalho traz a descrição do tipo de órgão e a data do sistema da sessão

A tela mostra no cabeçalho a descrição do tipo de órgão e a data do sistema que a sessão
carrega. Se a área da tela ainda não tem a descrição do tipo de órgão, ela vai buscá-la no
cadastro dos tipos de órgão.

### RN-11 — Todo campo digitado é conferido como número antes de qualquer leitura

Os **dezesseis** campos de negócio da tela — os onze do contrato e os cinco de cada linha
— passam pela conferência de número antes de qualquer consulta: o que não for número é
recusado, e nada é lido nem gravado. Campo deixado em branco passa por essa conferência
como zero; são as exigências de cada operação que decidem se o branco pode seguir. Dos
dezesseis, só **nove** têm posição de cursor definida: o início do período, o número e o
ano do contrato, o valor comprometido e o saldo não têm, e neles o cursor não volta ao
campo recusado.

[?] A mensagem dessa conferência e o aviso que o usuário vê ao digitar uma letra vivem
numa rotina do ambiente que não faz parte do lote lido. Pergunta ao site.

### RN-12 — A tela mostra os empenhos do contrato, com o valor comprometido e o saldo de cada um

Consultado o contrato, a tela percorre os empenhos lançados contra ele e mostra, em cada
linha, o número do empenho, o ano de referência, o valor informado, o valor já
comprometido e o saldo. O **valor comprometido** é o total dos processos daquele empenho
— os processos marcados como excluídos não entram nessa soma — e o **saldo** é o valor
informado menos o comprometido. Contrato sem empenho nenhum mostra
* Empenhos nao cadastrados *.

[?] O que é, em negócio, um processo lançado contra um empenho: a tela soma os valores
deles e não mostra nenhum campo deles, e o material lido não define o conceito. Pergunta
ao site.

[?] Contrato com mais empenhos do que as doze linhas: a tela guarda o ano e o número do
último empenho mostrado em vez de reiniciar a procura, o que sugere que a exibição
seguinte continua de onde parou — mas a leitura que avança de um empenho para o outro é do
dialeto do banco e não está no material lido, e não há aviso ao usuário nem caminho de
volta ao começo. Pergunta ao site.

### RN-13 — Toda linha marcada precisa do número do empenho

A linha que traz a marca da operação — incluir, alterar ou excluir — tem de trazer também
o número do empenho: sem ele, a recusa é * Atualize linha preenchida *, com o cursor de
volta à marca da linha. Linha sem marca é ignorada, mesmo que esteja preenchida.

[?] Como o operador marca a linha: o material lido guarda os três códigos que a tela testa
(inclusão, alteração e exclusão) e apaga o campo quando monta a exibição. Se a máscara
mostra outra palavra, ou se a marca vem de uma tecla de função, isso não está no lote.
Pergunta ao site.

### RN-14 — Incluir: o ano do empenho tem de caber no contrato e no ano corrente

O ano de referência de um empenho novo não pode ser anterior ao ano do início do período
do contrato — * Ano empenho invalido * — nem posterior ao ano corrente —
* Ano do empenho maior que ano atual * —, sempre com o cursor de volta ao ano de
referência.

### RN-15 — Incluir: o empenho não pode já existir, nem para este fornecedor nem para outro

Um empenho novo é recusado se aquele número, naquele ano e naquela coordenação, já estiver
lançado para o fornecedor do contrato — * Empenho ja cadastrado * — e também se estiver
lançado para qualquer outro fornecedor — * <- Empenho cadastrado para outro fornecedor * —
, com o cursor de volta ao número do empenho. Um mesmo empenho só pode estar preso a um
fornecedor.

### RN-16 — Incluir e alterar: o valor do empenho é obrigatório e não pode ser menor que o comprometido

O valor informado de um empenho tem de ser diferente de zero; em branco, a recusa é
* Informe valor do empenho *, com o cursor de volta ao valor. Na alteração, além disso, o
valor informado não pode ser menor que o total já comprometido daquele empenho: sendo
menor, a recusa é * <- Valor < que valor comprometido *. O valor pode ficar exatamente
igual ao comprometido — o saldo fica zero e o empenho continua existindo.

### RN-17 — Alterar e excluir exigem que o empenho exista; excluir exige que nada esteja comprometido

Para alterar um empenho, ele tem de estar lançado para o fornecedor e o contrato
informados; não estando, a recusa é * Empenho nao cadastrado *, com o cursor de volta ao
número do empenho. Para excluir, além de ele ter de existir, o total comprometido daquele
empenho tem de ser zero: havendo qualquer valor comprometido, a recusa é
* Ja existe valor comprometido *. Empenho com valor comprometido não pode ser apagado, e
esta tela não mexe nos processos que formam esse total — ela só lê a soma.

### RN-18 — A gravação: incluir cria a linha, alterar troca o valor e excluir apaga a linha

Na gravação, o empenho novo é criado com os dados do contrato — tipo de órgão, coordenação
regional escolar, tipo de contrato, início e limite do período e fornecedor — mais o
número do empenho, o ano de referência e o valor informados. Na alteração só o valor é
substituído: o número e o ano do empenho não mudam. Na exclusão o empenho é apagado do
cadastro. As linhas sem marca não são tocadas.

### RN-19 — A recusa de uma linha cancela a gravação de todas

Todas as linhas são conferidas antes de qualquer gravação; recusada uma linha, a tela
marca a transação como recusada e a passagem que grava não roda — nem para as linhas que
estavam certas. A marca é limpa no começo de cada transação.

### RN-20 — Toda gravação deixa rastro na auditoria

Cada empenho incluído, alterado ou apagado deixa um registro na trilha de auditoria com a
tela de origem, a operação, o cadastro de origem, a matrícula do usuário, a estação, o dia,
a hora e o minuto da sessão, o tipo de órgão, a coordenação regional escolar e o conteúdo
do empenho antes e depois da operação — vazio quando não havia empenho antes, e vazio
quando o empenho foi apagado. O número de processo que a auditoria guarda é montado com o
tipo de contrato, o fornecedor, o ano de referência e o número do empenho. As consultas e
as recusas não deixam rastro.

[?] As quatro partes que a tela junta para formar o número de processo somam dezessete
dígitos num campo de quatorze, e a segunda parte começa sobre a última posição da
primeira: o que fica gravado depende de como a montagem trunca, e o material lido não traz
esse detalhe. Se o número da auditoria não identificar o empenho, a trilha não serve para
achar o que foi mexido. Pergunta ao site.

### RN-21 — A consulta e a abertura da tela não gravam nada

Quando a opção é consultar, a passagem que grava termina sem tocar em cadastro nenhum.
Abrir a tela lê apenas o cadastro das telas e, quando falta, o do tipo de órgão: não
procura contrato nem empenho e não grava. Nenhuma recusa das conferências grava.

### RN-22 — O acesso à tela, à operação e à rota é conferido antes de gravar

Antes de gravar, a tela passa pela conferência de acesso: o sistema verifica a inscrição da
tela para o usuário, confere a estação da sessão com a estação registrada para a matrícula
e procura, no código de acesso do usuário, a liberação daquela operação para aquela tela.
Não estando liberada, a operação é interrompida e a tela é abandonada sem gravar —
* Acesso negado para esta matricula *, * Acesso negado para esta operacao *,
* Acesso a pagina 2 negado * ou * Tela nao disponivel *, conforme o caso. A conferência
recebe o contexto da sessão — a tela de origem, a matrícula, o código de acesso, o
privilégio, o tipo de órgão e a coordenação regional escolar —, e a rota é conferida
contra a tela de origem: tela não cadastrada é recusada com * Tela nao cadastrada *, e o
campo da tela seguinte, quando vem preenchido, devolve o controle à tela indicada em vez
de processar.

[?] A liberação de cada operação é procurada no código de acesso do usuário, mas o
encadeamento da conferência não deixa concluir, só pelo fonte, qual liberação vale para
cada opção desta tela — em particular se consultar também exige liberação e se a liberação
de alterar cobre a de excluir. O que o usuário vê quando a liberação falta, isso sim está
no lote. Pergunta ao site.

### RN-23 — Falha de banco interrompe a transação

Toda leitura e toda gravação testam o erro do banco; quando ele acontece, a transação é
despachada para o tratamento de erro do sistema e a gravação que falhou não é considerada
feita.

[?] O que a rotina de comunicação do sistema faz com a transação não está no acervo lido;
se ela não interromper, o aviso é dado e o processamento pode seguir para a linha seguinte.
Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manter os empenhos de um contrato da coordenação regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenação regional escolar e a data do sistema
    E tenho acesso à tela C694T

  Cenário: RN-01 e RN-02 — a tela trata um contrato e até doze empenhos, e não o contrato
    Quando abro a tela C694T
    Então vejo o formulário com os onze campos do contrato e doze linhas de empenho, de seis campos cada
    E vejo a descrição do tipo de órgão, a data do sistema e a razão social do fornecedor
    E posso incluir, alterar e excluir empenhos deste contrato
    E não há como incluir, alterar ou excluir o contrato nem o fornecedor por esta tela

  Cenário: RN-05 e RN-21 — abrir a tela assume a consulta e não grava nem procura contrato
    Quando abro a tela C694T sem informar opção
    Então a opção de manutenção vem preenchida com a consulta
    E nenhum contrato e nenhum empenho é procurado
    E nada é gravado

  Cenário: RN-03, RN-06, RN-08, RN-09 e RN-12 — consultar o contrato e ver os empenhos dele
    Dado que o contrato da minha coordenação regional escolar existe, com o tipo de contrato, o período limite e o fornecedor informados
    E que ele tem empenhos lançados
    Quando informo a coordenação regional escolar, o tipo de contrato, o limite do período e o fornecedor
    Então vejo o número e o ano do contrato, o início e o limite do período e a razão social do fornecedor
    E vejo cada empenho com o número, o ano de referência, o valor informado, o valor já comprometido com os processos e o saldo
    E o saldo é o valor informado menos o comprometido
    E nada é gravado

  Cenário: RN-12 — contrato sem empenho lançado
    Dado que o contrato consultado não tem empenho lançado
    Quando consulto o contrato
    Então vejo "* Empenhos nao cadastrados *"
    E nada é gravado

  Cenário: RN-18, RN-13, RN-14, RN-15 e RN-16 — incluir um empenho no contrato
    Dado que o contrato já foi consultado nesta sessão e continua o mesmo
    E que o empenho ainda não existe para nenhum fornecedor
    Quando marco uma linha com a inclusão, informo o número do empenho, o ano de referência e o valor, e confirmo
    Então o empenho é criado preso ao contrato, com o tipo de órgão, a coordenação regional escolar, o tipo de contrato, o período e o fornecedor do contrato
    E ele guarda o número, o ano de referência e o valor informados
    E nada mais é criado ou apagado

  Cenário: RN-18 e RN-16 — alterar o valor de um empenho
    Dado que o contrato já foi consultado nesta sessão e continua o mesmo
    E que o empenho está lançado para este fornecedor
    E que o valor informado não é menor que o total comprometido daquele empenho
    Quando marco a linha com a alteração, informo o valor e confirmo
    Então só o valor daquele empenho é substituído
    E o número e o ano do empenho não mudam

  Cenário: RN-18 e RN-17 — excluir um empenho sem nada comprometido
    Dado que o contrato já foi consultado nesta sessão e continua o mesmo
    E que o empenho está lançado e não tem nenhum valor comprometido
    Quando marco a linha com a exclusão e confirmo
    Então o empenho é apagado do cadastro
    E o contrato continua como estava

  Cenário: RN-05 — opção de manutenção diferente de consultar ou alterar
    Quando troco a opção de manutenção da tela por outra
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é lido e nada é gravado

  Cenário: RN-06 — coordenação regional escolar de outro grupo
    Quando informo uma coordenação regional escolar diferente da minha
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenação
    E nada é consultado

  Cenário: RN-07 — alterar sem consultar antes, ou com a chave trocada
    Dado que ainda não consultei este contrato nesta sessão, ou que troquei a coordenação, o tipo de contrato, o limite do período ou o fornecedor
    Quando confirmo com a opção de alteração
    Então vejo "* Consulte antes de atualizar *"
    E o cursor volta ao campo da opção
    E nada é lido e nada é gravado

  Cenário: RN-08 — contrato não registrado no FINCON
    Quando informo a coordenação, o tipo de contrato, o limite do período e o fornecedor de um contrato que não existe
    Então vejo "* Contrato FINCON nao cadastrado *"
    E o cursor volta ao campo da coordenação regional escolar
    E nenhuma linha de empenho é lida

  Cenário: RN-04 — início do período, número e ano do contrato informados diferentes do cadastro
    Dado que informo um início de período, um número ou um ano de contrato diferente do que o contrato tem
    Quando consulto o contrato
    Então esses campos voltam com o que está gravado no contrato
    E é o início do contrato que fica no empenho incluído

  Cenário: RN-10 — cabeçalho com a descrição do tipo de órgão e a data do sistema
    Quando abro a tela C694T
    Então vejo a descrição do tipo de órgão da minha sessão
    E vejo a data do sistema que a sessão carrega

  Cenário: RN-11 — campo preenchido com letra
    Quando preencho com letra um dos campos do contrato ou de uma linha
    Então a tela recusa o campo antes de qualquer consulta
    E nada é lido e nada é gravado
    E, se o campo recusado for o início do período, o número ou o ano do contrato, o valor comprometido ou o saldo, o cursor não volta a ele

  Cenário: RN-13 — linha marcada sem o número do empenho
    Quando marco uma linha e confirmo sem informar o número do empenho
    Então vejo "* Atualize linha preenchida *"
    E o cursor volta à marca da linha
    E nada é gravado

  Cenário: RN-13 — linha sem marca é ignorada
    Dado que preenchi uma linha sem marcar a operação
    Quando confirmo
    Então aquela linha não gera operação nenhuma

  Cenário: RN-14 — ano de referência anterior ao início do contrato
    Quando marco uma linha com a inclusão e informo um ano de referência anterior ao ano do início do período do contrato
    Então vejo "* Ano empenho invalido *"
    E o cursor volta ao ano de referência
    E nada é gravado

  Cenário: RN-14 — ano de referência posterior ao ano corrente
    Quando marco uma linha com a inclusão e informo um ano de referência maior que o ano atual
    Então vejo "* Ano do empenho maior que ano atual *"
    E o cursor volta ao ano de referência
    E nada é gravado

  Cenário: RN-15 — empenho já lançado para o fornecedor do contrato
    Quando marco uma linha com a inclusão e informo um empenho que já está lançado para o fornecedor do contrato
    Então vejo "* Empenho ja cadastrado *"
    E o cursor volta ao número do empenho
    E nada é gravado

  Cenário: RN-15 — empenho lançado para outro fornecedor
    Quando marco uma linha com a inclusão e informo um empenho que já está lançado para outro fornecedor
    Então vejo "<- Empenho cadastrado para outro fornecedor *"
    E o cursor volta ao número do empenho
    E nada é gravado

  Cenário: RN-16 — valor do empenho em branco
    Dado que marco uma linha com a inclusão ou com a alteração
    Quando confirmo sem informar o valor
    Então vejo "* Informe valor do empenho *"
    E o cursor volta ao valor
    E nada é gravado

  Cenário: RN-16 — valor menor que o comprometido
    Dado que marco uma linha com a alteração
    Quando informo um valor menor que o total já comprometido daquele empenho
    Então vejo "<- Valor < que valor comprometido *"
    E o cursor volta ao valor
    E nada é gravado

  Cenário: RN-17 — empenho não lançado, na alteração e na exclusão
    Dado que marco uma linha com a alteração, ou com a exclusão, e informo um empenho que não está lançado para este fornecedor
    Quando confirmo
    Então vejo "* Empenho nao cadastrado *"
    E o cursor volta ao número do empenho
    E nada é gravado

  Cenário: RN-17 — empenho com valor comprometido não pode ser apagado
    Dado que marco uma linha com a exclusão
    E que aquele empenho tem valor comprometido com processos
    Quando confirmo
    Então vejo "* Ja existe valor comprometido *"
    E o empenho continua lançado

  Cenário: RN-19 — uma linha recusada cancela a gravação das outras
    Dado que marco duas linhas, uma delas com um dado que a tela recusa
    Quando confirmo
    Então vejo a mensagem da recusa daquela linha
    E nenhuma das duas linhas é gravada

  Cenário: RN-20 — rastro na auditoria
    Dado que incluí, alterei ou apaguei um empenho
    Então a auditoria guarda um registro daquela operação com a tela de origem, a operação, o cadastro de origem, a matrícula, a estação, a data, a hora, o tipo de órgão e a coordenação regional escolar
    E guarda o conteúdo do empenho antes e depois da operação
    E a consulta e as recusas não deixam registro

  Cenário: RN-22 — operação não liberada para o meu código de acesso
    Dado que o meu código de acesso não tem a operação liberada para a tela C694T
    Quando confirmo a operação
    Então vejo "* Acesso negado para esta operacao *"
    E a operação é interrompida sem gravar

  Cenário: RN-22 — tela não cadastrada ou rota não esperada
    Dado que a tela não está cadastrada, ou que o campo da tela seguinte vem preenchido
    Quando confirmo
    Então vejo "* Tela nao cadastrada *", no primeiro caso
    E o controle volta à tela indicada, no segundo
    E nada é gravado

  Cenário: RN-23 — falha de banco durante a gravação
    Dado que a gravação de um empenho falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com o tratamento de erro do sistema
    E o empenho que falhou não é considerado gravado
```
