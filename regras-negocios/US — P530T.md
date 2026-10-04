# US — P530T — Consulta dos registros escolares do grupo no arquivo do ano

## Estória

Como **servidor de CRE**, quero **conferir os registros escolares que o meu grupo
transmitiu no arquivo do ano, com a devolução de cada um, e pedir a impressão dessa
relação**, para que **eu veja registro a registro o que a CRE transmitiu e o que
voltou do SIAFIC com erro, e possa entregar a relação a quem precisa dela**.

O registro escolar de um grupo vive dentro do arquivo de um ano e é transmitido ao
SIAFIC; de cada transmissão pode voltar uma descrição de erro, e é essa devolução que
diz se o registro está regular. Esta é a tela em que a CRE vê essa devolução registro a
registro — o empenho, o ano de referência, o valor do saldo inicial, o tipo de anulação
— e pede a impressão da relação. Sem ela, um registro que voltou com erro não teria por
onde ser visto dentro da relação, e a relação não teria por onde sair do sistema.

## Contexto

Jornada S000M → P000M → P500M → P530T.
Ator: servidor de CRE — nesta tela, confere os registros escolares do grupo no arquivo
do ano e pede a impressão da relação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada — `P000M` e `P500M` — são menus: só encaminham e
não deixam dado de negócio para esta tela. O contexto que a `P530T` usa — a matrícula,
a CRE, o órgão, o código de acesso e a estação — é o que a entrada deixou na sessão; a
tela não recebe da `P500M` nenhum empenho nem nenhum arquivo.

A `P530T` também é alcançada encadeada, sem passar por menu: a tela do arquivo do ano,
`P525T`, passa o grupo e a data do arquivo que conferiu (RN-03), e é para lá que a
`P530T` pede a volta quando o registro em tela vem marcado (RN-11).

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — Ao abrir, a tela mostra os registros escolares do grupo no arquivo do ano

Abrir a tela não grava nada: ela lê os registros escolares já transmitidos do grupo
dentro do arquivo daquele ano e mostra até quatro deles, um por linha, cada um com o
número do processo, o número do empenho, o ano de referência, o número da ordem de
pré-liquidação, o valor do saldo inicial e o tipo de anulação. Quando o registro tem a
devolução do SIAFIC, a linha mostra também a descrição do erro que voltou.

[?] A tela monta as linhas em uma tabela que ela reordena, posição a posição, antes de
mostrar: a linha que o operador vê na primeira posição pode ser a segunda lida. Se o
efeito é só de ordenação, ou se a primeira linha é mostrada trocada, não se lê nos
fontes desta jornada. Pergunta ao site.

[?] Os nomes das colunas que o operador vê não estão no lote: o que se lê no fonte são
os quatro rótulos de conferência — **CORD.REG.ESCOLAR**, **NUM.EMPENHO**,
**ANO REFERENCIA** e **VALOR SALDO INIC** —, e a ficha da tela registra que a máscara
pode ter outros. Pergunta ao site.

### RN-02 — Sem registro do grupo no arquivo do ano, a abertura avisa

Não achando registro do grupo na leitura que monta a primeira linha, a abertura avisa
**\* Nao existem registros neste arquivo \***, encerra a operação sem mostrar linha
nenhuma e não grava nada.

### RN-03 — A data do arquivo vem da tela anterior; sem ela, a do dia

A tela trabalha com a data do arquivo: o dia, o mês e o ano que a tela anterior deixou
na sessão e, quando não vem nenhuma, a data do dia. Não vindo data nenhuma e não
achando registro do grupo na data do dia, a tela não recusa: ela recua para o primeiro
registro do grupo, seja qual for a data, e passa a mostrar a data desse registro.

[?] O recuo se apoia numa leitura pedida com a data em zero, para achar o primeiro
registro do grupo, e o que essa leitura pede ao banco não está no corpus: o recurso de
leitura posicionada vem de fora do acervo. Se a leitura com data zero acha o primeiro
registro do grupo, ou a leitura exata de um registro de data zerada, não se lê nestes
fontes. Pergunta ao site.

### RN-04 — A operação da tela é a consulta

A tela não inclui, não altera e não exclui registro escolar nenhum: a operação que ela
executa é a consulta. Informada outra operação, a recusa é
**\* Opcao nao disponivel. Use CON \***, com o cursor no campo da operação, e nada é
gravado.

### RN-05 — O grupo é conferido contra o alcance do servidor

A consulta só atende o grupo da matrícula do servidor ou o grupo que a tela já
carregou; informando outro, a recusa é **\* Usuario sem acesso a este grupo \***, com o
cursor no campo do grupo, e nada é gravado.

Quem não tem grupo na matrícula alcança os grupos da sua secretaria: o grupo informado
tem de estar cadastrado para a secretaria da sessão — não estando, a recusa é
**\* Grupo nao pertence a esta secretaria \***, com o cursor no mesmo campo.

### RN-06 — O grupo tem de ter registro escolar transmitido

A tela só segue com um grupo que já tenha registro escolar transmitido: não havendo
registro nenhum do grupo, a recusa é **\* Grupo sem registros transmitidos \***, com o
cursor no campo do dia do arquivo, e nada é gravado. Havendo registro do grupo em outra
data que não a informada, a tela não recusa: ela descarta a data informada e segue.

### RN-07 — Com o código de impressão informado, a tela pede a impressão da relação

Além da consulta, a tela aceita um **código de impressão**. Informado, ela confere se
já existe pedido de impressão daquela relação em processamento para o grupo — havendo,
avisa **\* Relatorio em processamento. Aguarde. \***, deixa o cursor no campo do código
de impressão e não pede outro — e confere se o grupo tem registro na data informada —
não havendo, avisa **\* Grupo sem reg transmitidos nesta data \***, com o cursor no
campo do dia, e não pede o relatório.

Passando as duas conferências, a tela cria o pedido de impressão da relação do grupo,
com o relatório, o código de impressão, a matrícula, a CRE, a secretaria, o terminal e
o dia e a hora, e aciona a execução do relatório.

[?] A conferência do pedido já em processamento e a do registro na data ficam só na
passagem de conferência da mensagem; o trecho que cria o pedido não as repete. Depende
da rotina comum de mensagem, que não está no lote, saber se o pedido deixa de ser
criado. Pergunta ao site.

### RN-08 — Fora o pedido de impressão, a consulta não grava nada

Fora o pedido de impressão (RN-07), a tela não inclui, não altera e não exclui nada: o
que ela faz é ler o cadastro de telas, o cadastro dos registros escolares, o cadastro
das devoluções do SIAFIC, o cadastro dos grupos da secretaria, o cadastro de
funcionários e o cadastro de requisições, e mostrar o que leu. O que aparece em cada
linha vem do cadastro, não de cálculo da tela.

### RN-09 — A resposta sai sem a data do sistema, o órgão, o tipo de anulação e o erro do SIAFIC

Ao abrir, a tela mostra a data do sistema e o nome do órgão da sessão. A cada mensagem
respondida, esses dois campos e mais o tipo de anulação e a descrição do erro do SIAFIC
são apagados antes de qualquer conferência e não são repostos: a resposta sai com eles
em branco.

[?] Essa limpeza está amarrada a um tipo de mensagem que o acervo não explica; se
existe um caminho de entrada em que os campos não são limpos, não foi possível
determinar. Pergunta ao site.

### RN-10 — A tela não se abre sobre ela mesma

Chamada de novo por outra tela enquanto o código da tela que a chamou estiver
preenchido, a operação é encerrada em silêncio: nada é mostrado, nada é gravado e
nenhuma mensagem aparece. O mesmo acontece quando a área de trabalho da tela já vem
marcada como errada.

### RN-11 — O registro marcado pede a volta à conferência do arquivo do ano

Quando o registro em tela vem com a marca de situação preenchida como "S", a tela não
segue a consulta: ela pede a volta para a tela do arquivo do ano, `P525T`, entregando o
grupo que conferiu e a área de trabalho, com a operação limpa.

[?] A tela confere essa marca e a mostra, mas nenhum trecho desta jornada a preenche —
no fonte da `P530T` o campo só é lido. O que "S" quer dizer (registro já transmitido?
linha assinalada?) e quem o preenche — a máscara, a tela anterior ou o operador — não
se lê no corpus. A volta ainda entrega a área de trabalho marcada como já processada, e
é essa mesma marca que encerra a `P525T` em silêncio: se a tela seguinte chega a
retomar, não se lê nestes fontes. Pergunta ao site.

### RN-12 — Os campos informados passam pela edição numérica

Os campos que o operador informa — o grupo, o dia, o mês e o ano do arquivo, o número
do empenho, o ano de referência, a ordem de pré-liquidação e o valor do saldo inicial —
são editados como número antes de qualquer conferência. O que não passar pela edição é
recusado com o cursor devolvido ao campo, e nada é gravado.

[?] A tela edita e mostra o número do empenho, o ano de referência, a ordem de
pré-liquidação e o valor do saldo inicial, mas nenhum deles identifica ou filtra o
registro: as leituras usam só o grupo e a data. Se a máscara espera que eles filtrem,
ou se são só informativos, não se lê no corpus. Pergunta ao site.

### RN-13 — Nada acontece sem a tela e a matrícula habilitadas

Ao abrir, o sistema confere, com o contexto da sessão, se a tela está cadastrada e se a
matrícula tem a tela no seu código de acesso; não estando, a recusa é
**\* Tela nao disponivel \*** ou **\* Acesso negado para esta matricula \***, e a
operação não segue. Na operação, a tela passa ainda pela lógica de rota, que recusa a
operação que ela não reconhece (**\* Operacao nao disponivel \***) e a tela retirada do
cadastro (**\* Tela nao cadastrada \***), e o código de acesso da operação exige a
autorização da operação informada (**\* Acesso negado para esta operacao \***).

## Cenários BDD

```gherkin
Funcionalidade: Consulta dos registros escolares do grupo no arquivo do ano, com pedido de impressão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela P530T

  Cenário: Abertura mostra os registros escolares do grupo no arquivo do ano
    Dado que o meu grupo tem registros escolares transmitidos no arquivo do ano
    Quando abro a tela P530T
    Então vejo até quatro registros, um por linha, com o número do processo, o número do empenho, o ano de referência, a ordem de pré-liquidação, o valor do saldo inicial e o tipo de anulação
    E cada linha com devolução do SIAFIC mostra a descrição do erro que voltou
    E nada é gravado

  Cenário: O grupo não tem registro no arquivo do ano
    Dado que o meu grupo não tem registro escolar no arquivo do ano
    Quando abro a tela P530T
    Então vejo a mensagem "* Nao existem registros neste arquivo *"
    E nenhuma linha é mostrada
    E nada é gravado

  Cenário: Sem data da tela anterior, a tela usa a data do dia
    Dado que abro a tela P530T pelo menu, sem data de arquivo
    E o meu grupo tem registro na data do dia
    Quando abro a tela P530T
    Então vejo os registros escolares do grupo na data do dia
    E nada é gravado

  Cenário: Não havendo registro na data do dia, a tela recua para o primeiro registro do grupo
    Dado que abro a tela P530T pelo menu, sem data de arquivo
    E o meu grupo não tem registro na data do dia
    E o meu grupo tem registro em outra data
    Quando abro a tela P530T
    Então vejo os registros do grupo a partir do primeiro que houver, seja qual for a data
    E a data mostrada é a do registro encontrado
    E nada é gravado

  Cenário: A consulta não grava nada
    Dado que o meu grupo tem registros escolares no arquivo do ano
    Quando confirmo a mensagem com a opção de consulta e sem código de impressão
    Então nenhum registro escolar é incluído, alterado ou excluído
    E nenhum pedido de impressão é criado

  Cenário: Operação diferente da consulta é recusada
    Dado que o meu grupo tem registros escolares no arquivo do ano
    Quando informo uma operação que não é a de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: Grupo fora do meu alcance é recusado
    Dado que a minha matrícula tem um grupo
    Quando informo outro grupo e confirmo a consulta
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo do grupo
    E nada é gravado

  Cenário: Grupo de outra secretaria é recusado
    Dado que a minha matrícula não tem grupo
    Quando informo um grupo que não está cadastrado para a minha secretaria
    Então vejo a mensagem "* Grupo nao pertence a esta secretaria *"
    E o cursor fica no campo do grupo
    E nada é gravado

  Cenário: Grupo sem registro transmitido é recusado
    Dado que o grupo informado não tem registro escolar transmitido
    Quando confirmo a consulta
    Então vejo a mensagem "* Grupo sem registros transmitidos *"
    E o cursor fica no campo do dia do arquivo
    E nada é gravado

  Cenário: Grupo com registro em outra data não é recusado
    Dado que o grupo informado tem registro transmitido em outra data
    Quando confirmo a consulta com uma data que não tem registro
    Então a tela descarta a data informada e segue
    E nada é gravado

  Cenário: Pedido de impressão da relação
    Dado que o meu grupo tem registro na data informada
    E não existe pedido de impressão daquela relação em processamento
    Quando confirmo a consulta informando o código de impressão
    Então o pedido de impressão da relação do grupo é criado
    E a execução do relatório é acionada

  Cenário: Relatório já em processamento
    Dado que já existe pedido de impressão daquela relação em processamento para o grupo
    Quando confirmo a consulta informando o código de impressão
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor fica no campo do código de impressão
    E nenhum pedido novo é criado

  Cenário: Sem registro na data informada, o relatório não é pedido
    Dado que o meu grupo não tem registro na data informada
    Quando confirmo a consulta informando o código de impressão
    Então vejo a mensagem "* Grupo sem reg transmitidos nesta data *"
    E o cursor fica no campo do dia
    E nenhum pedido novo é criado

  Cenário: A resposta sai sem a data do sistema, o órgão, o tipo de anulação e o erro do SIAFIC
    Dado que a tela abriu mostrando a data do sistema, o órgão e a devolução do SIAFIC de cada registro
    Quando respondo uma mensagem
    Então a resposta vem com esses campos em branco

  Cenário: A tela não se abre sobre ela mesma
    Dado que a tela P530T já está aberta
    Quando outra tela a chama de novo
    Então a operação é encerrada sem mensagem
    E nada é gravado

  Cenário: O registro marcado pede a volta à conferência do arquivo do ano
    Dado que o registro em tela vem com a marca de situação "S"
    Quando confirmo a consulta
    Então a tela pede a volta para a P525T
    E entrega a ela o grupo conferido, com a operação limpa

  Cenário: Campo não numérico é recusado
    Dado que informo um grupo que não é número
    Quando confirmo a mensagem
    Então a tela recusa o campo antes de consultar o cadastro
    E o cursor volta para o campo
    E nada é gravado

  Cenário: Tela não cadastrada
    Dado que a tela P530T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela P530T no seu código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Sem autorização para a operação
    Dado que o meu código de acesso não tem a operação informada liberada para a tela P530T
    Quando confirmo a mensagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Operação não reconhecida
    Dado que informo uma operação que a tela não reconhece
    Quando confirmo a mensagem
    Então vejo a mensagem "* Operacao nao disponivel *"
    E nada é gravado

  Cenário: Tela retirada do cadastro
    Dado que a tela P530T foi retirada do cadastro de telas
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é gravado
```
