# US — N124C — Consulta de nota fiscal e dos pedidos que a compõem

## Estória

Como **servidor de CRE**, quero **consultar uma nota fiscal pelo número, pelo ano de
emissão, pelo fornecedor e pelo gênero**, para que **eu veja quais pedidos a compõem, a
quantidade e o valor do gênero e em que situação o processamento está**.

A nota fiscal é o documento que amarra o fornecedor, o gênero e o pedido de compra; o que
o órgão recebeu só pode ser conferido se a nota puder ser aberta e os pedidos que a formam
puderem ser vistos um a um, com a quantidade e o valor de cada gênero. Sem esta consulta,
quem acompanha a despesa teria o número da nota e nada dentro dela — sem saber se o que
chegou bate com o que foi pedido, nem por quanto.

A consulta é de leitura: ela não inclui, não altera e não exclui nota nenhuma.

## Contexto

Jornada S000M → N000M → N060M → N124C.
Ator: servidor de CRE — informa o número e o ano da nota, o fornecedor e o gênero, e vê o
que a nota contém.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O
caminho até a tela — qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio.

As duas telas anteriores da jornada, `N000M` e `N060M`, são menus: nenhuma delas deixa
operação ou registro para a `N124C`. A tela não compara quem a chamou com código de tela
nenhum; o que decide o comportamento dela é a operação que a sessão lhe entrega e, se vier
preenchida, a indicação da tela seguinte. Esta é a última tela da jornada: ela não encadeia
em outra.

O que a tela usa da sessão — o tipo de órgão e a secretaria — é o que a entrada deixou do
vínculo da matrícula com a secretaria, e é isso que limita as notas que ela consegue
enxergar. As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela só consulta: não grava, não altera e não exclui

Esta tela é de leitura. Dos **quinze** cadastros que ela enxerga — o cadastro de telas, o
de notas fiscais do processo e o dos itens dessas notas, o das outras notas fiscais e o
dos itens dessas outras notas, o de pedidos e o dos itens dos pedidos acumulados, o da
composição da nota em pedidos, o do andamento do processo, o de fornecedores, o de órgãos,
o de fontes, o de gêneros, o de modalidades e o de operadores —, o programa declara as
operações de gravar, de excluir e de travar registro para todos, e **nenhuma delas é
executada em caminho algum**: todas as operações de dados que a tela executa são leituras.

Também não há registro de auditoria, porque não há gravação para auditar. O desfecho da
consulta é apenas o que a tela mostra.

### RN-02 — A única operação aceita é a consulta, e ela vem de quem chamou a tela

A tela abre na operação que a sessão lhe entrega; não recebendo nenhuma, ela mesma assume a
consulta. Confirmada com qualquer outra operação, ela recusa com
**\* Operacao nao disponivel. Use CON \***, devolve o cursor ao campo da operação e não lê
nota nenhuma.

[?] A tela aceita um único código de operação — o de consulta —, o sistema grava esse
código como **INQ** e o converte para a letra **I** quando o mostra, e o aviso manda usar
**CON**. As três formas não coincidem e não há, no acervo, a conversão de uma para outra: o
que o servidor precisa digitar para ser aceito fica sem resposta. Pergunta ao site.

[?] A operação chega pela área de trabalho da sessão, não por um campo próprio da tela, e
os dois menus desta jornada não limpam essa área — o que a zera está na rotina comum, fora
dos fontes desta jornada. Se ela não for zerada entre uma tela e outra, a operação de uma
tela anterior pode valer nesta. Pergunta ao site.

### RN-03 — Recebendo a indicação da tela seguinte, a tela não consulta nada

Quando a sessão traz preenchida a indicação da tela que deve abrir em seguida, esta tela
não confere nada e não lê nada: ela passa a vez, e quem assume é a tela indicada. A
consulta só acontece quando essa indicação vem em branco.

[?] A indicação da tela seguinte não tem rótulo de negócio no acervo — o rótulo que a tela
carrega para ela é o nome interno do campo, e nenhuma das telas desta jornada a preenche.
Se é um campo que o servidor digita ou só um recado entre telas, pergunta ao site.

### RN-04 — A nota é procurada por cinco dados, e dois deles são obrigatórios

O servidor identifica a nota por cinco dados: o **número da nota fiscal**, o **ano de
emissão**, o **código do fornecedor**, o **código de subclasse** e o **código do gênero**.
O dia e o mês de emissão não são informados: vêm da própria nota.

O número e o ano são obrigatórios. Sem o número, a recusa é
**\* Informe o numero da nota fiscal \***; sem o ano,
**\* Informe o ano de entrega da nota fiscal \***; nos dois casos o cursor volta ao campo e
nada é lido.

Quando os cinco dados são exatamente os mesmos da consulta anterior, a tela não lê de novo:
ela reapresenta o que já tinha. A leitura só é refeita quando algum dos cinco muda.

[?] O aviso que pede o ano chama esse dado de "ano de entrega", mas o rótulo do campo é
"ANO EMISSAO N.F." — são o mesmo campo, e o texto do aviso não bate com o rótulo. Qual dos
dois nomes é o de negócio, pergunta ao site.

### RN-05 — O fornecedor tem de estar cadastrado

O código do fornecedor informado é conferido no cadastro de fornecedores. Não existindo —
ou estando marcado para exclusão — a recusa é **\* Fornecedor nao cadastrado \***, com o
cursor de volta ao campo. Existindo, a tela mostra a razão social dele.

### RN-06 — O gênero tem de ser informado e estar cadastrado no ano da nota

O código de subclasse não pode vir zerado: sem ele, a recusa é **\* Informe o genero \***,
com o cursor no campo. Informado o par de subclasse e gênero, a tela procura a descrição do
gênero no cadastro de gêneros, para o **ano de emissão da nota**; não achando, a recusa é
**\* Genero nao cadastrado \***.

[?] O aviso pede o "gênero", mas quem é conferido é o código de subclasse; o código do
gênero não tem aviso próprio. Se os dois códigos deveriam ter o mesmo tratamento, pergunta
ao site.

### RN-07 — A nota tem de estar em um dos dois cadastros, e o gênero dela também

A tela procura a nota primeiro no cadastro de notas fiscais do processo (`N011T`) e, não
estando lá, no cadastro de notas fiscais (`N013T`). As duas buscas são feitas dentro do
**tipo de órgão da sessão**: nota de outro tipo de órgão simplesmente não é encontrada. Não
achando a nota em nenhum dos dois, a recusa é **\* Nota fiscal nao cadastrada \***.

Achada a nota, a tela procura o gênero informado entre os itens daquela nota; não achando,
a recusa é **\* Genero nao cadastrado nesta nota \***. É desse item que saem o valor
unitário e a quantidade e o valor do gênero.

O número que encabeça a lista de pedidos aparece rotulado de **Processo** quando a nota vem
do primeiro cadastro e de **Lote** quando vem do segundo.

### RN-08 — A nota tem de ser de pedido acumulado

O pedido a que a nota pertence tem de estar marcado como pedido acumulado. Não estando, a
recusa é **\* Nota nao e de pedido acumulado \***, com o cursor de volta ao número da nota.
É essa marcação que libera o resto da consulta: sem ela a tela não segue, e é ela que a tela
assinala como consulta de pedido acumulado.

### RN-09 — A nota tem de ser da secretaria do servidor

A nota carrega a secretaria a que pertence. Quando a sessão do servidor tem secretaria, ela
tem de ser a mesma da nota; sendo outra, a recusa é
**\* Usuario sem acesso a outro grupo \***, com o cursor de volta ao número da nota. Quando
a sessão não tem secretaria, a conferência não é feita e a nota de qualquer secretaria é
mostrada.

### RN-10 — A tela lista até nove pedidos da nota e os totais do gênero

Achadas a nota e o gênero, a tela monta a lista dos pedidos que compõem a nota, **um por
linha**, até **nove** linhas. Cada linha traz o número do pedido, o ano de entrega, o código
e o nome do órgão que recebeu, a data de início do pedido, a quantidade e o valor do gênero
naquele pedido, e ainda um código de uma posição que o pedido carrega.

Fora da lista, a tela mostra os totais do gênero na nota: a **quantidade** e o **valor**
somados por todos os pedidos.

Quando a nota não tem composição de pedidos nenhuma, a tela recusa com
**\* Nota fiscal sem composicao de pedidos \*** e não apresenta lista.

[?] O rodapé da tela é rotulado como total da nota fiscal, mas a soma é feita só sobre os
pedidos do gênero informado — trocando o gênero, o total muda. Se o número que a tela mostra
é o total da nota ou o total do gênero, pergunta ao site.

[?] O código de uma posição que cada linha do pedido mostra não tem rótulo nem domínio no
acervo. O que ele significa é pergunta ao site.

### RN-11 — A situação da nota vem do andamento do processo

Quando a nota está marcada com a abreviatura **P** do cadastro, a tela mostra a situação do
andamento do processo a que a nota pertence: **Pre Liq** para pré-liquidado, **Liquida**
para liquidado e **Paga** para as demais. Nas notas sem essa marcação, ela mostra
**Fechada**.

[?] O que a abreviatura **P** marca na nota não está no acervo: a tela só a compara com esse
valor e nada a descreve em negócio. Pergunta ao site.

[?] Não achando o andamento do processo — ou achando-o numa situação que não seja
pré-liquidado nem liquidado — a tela mostra **Paga**: não há desfecho próprio para o
andamento ausente. Se uma nota sem andamento deve aparecer como paga, pergunta ao site.

### RN-12 — Cada código da nota é mostrado com o nome do seu cadastro

A tela não inventa nome nenhum: a razão social do fornecedor vem do cadastro de
fornecedores; o nome do órgão que recebeu, do cadastro de órgãos, tomado do primeiro
registro daquele código que não esteja marcado para exclusão; a descrição da fonte, do
cadastro de fontes; a descrição da modalidade da nota, do cadastro de modalidades; a
descrição do gênero, do cadastro de gêneros; e o nome do operador, do cadastro de
operadores. O número do processo é apresentado em partes, separadas por barra. Também vêm
da sessão a descrição do tipo de órgão e a data do sistema.

[?] O cadastro de fontes e o de operadores são lidos pelo código sem que a tela confira se
estão marcados para exclusão — o fornecedor e o órgão são conferidos. Se a tela deve mostrar
a descrição de um registro excluído, pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consulta de nota fiscal e dos pedidos que a compõem

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N124C

  Cenário: Consulta de uma nota fiscal com os cinco dados preenchidos
    Dado que informo o número, o ano de emissão, o fornecedor, o código de subclasse e o código do gênero de uma nota existente
    Quando confirmo a consulta
    Então vejo a razão social do fornecedor, a modalidade, o operador, o órgão, a fonte, o valor unitário e a descrição do gênero
    E vejo a lista dos pedidos que compõem a nota, com o número do pedido, o ano de entrega, o órgão, a data de início, a quantidade e o valor do gênero
    E vejo a quantidade e o valor totais do gênero na nota

  Cenário: A consulta não grava nada
    Dado que consultei uma nota fiscal
    Então nada é incluído, alterado ou excluído em nenhum cadastro
    E nenhum registro de auditoria é gravado

  Cenário: Confirmação com uma operação que não é a de consulta
    Dado que a tela chegou com uma operação diferente da de consulta
    Quando confirmo
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nenhuma nota é lida

  Cenário: Confirmação com a indicação da tela seguinte preenchida
    Dado que a sessão traz preenchida a indicação da tela que deve abrir em seguida
    Quando confirmo
    Então esta tela não confere nada e não lê nada
    E quem assume é a tela indicada

  Cenário: Número da nota em branco
    Dado que deixo o número da nota fiscal em branco
    Quando confirmo a consulta
    Então vejo "* Informe o numero da nota fiscal *"
    E o cursor volta ao campo do número

  Cenário: Ano de emissão em branco
    Dado que informo o número da nota e deixo o ano em branco
    Quando confirmo a consulta
    Então vejo "* Informe o ano de entrega da nota fiscal *"
    E o cursor volta ao campo do ano

  Cenário: Repetir a consulta dos mesmos cinco dados
    Dado que acabei de consultar uma nota
    Quando confirmo de novo os mesmos cinco dados
    Então a tela reapresenta o que já tinha
    E não faz nova leitura

  Cenário: Fornecedor não cadastrado
    Quando informo um fornecedor que não existe no cadastro de fornecedores
    Então vejo "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo do fornecedor

  Cenário: Código de subclasse em branco
    Dado que informo o número, o ano e o fornecedor e deixo o código de subclasse em branco
    Quando confirmo a consulta
    Então vejo "* Informe o genero *"

  Cenário: Gênero não cadastrado no ano da nota
    Quando informo um par de subclasse e gênero que não existe no cadastro para o ano da nota
    Então vejo "* Genero nao cadastrado *"

  Cenário: Nota não encontrada em nenhum dos dois cadastros
    Quando informo uma nota que não existe
    Então vejo "* Nota fiscal nao cadastrada *"

  Cenário: Nota de outro tipo de órgão
    Dado que a nota pertence a um tipo de órgão diferente do da minha sessão
    Quando confirmo a consulta
    Então vejo "* Nota fiscal nao cadastrada *"

  Cenário: Gênero não cadastrado na nota
    Dado que a nota existe e não tem item para o gênero informado
    Quando confirmo a consulta
    Então vejo "* Genero nao cadastrado nesta nota *"

  Cenário: Nota de pedido que não é acumulado
    Dado que a nota pertence a um pedido não marcado como acumulado
    Quando confirmo a consulta
    Então vejo "* Nota nao e de pedido acumulado *"

  Cenário: Nota de outra secretaria
    Dado que a minha sessão tem secretaria
    E a nota pertence a outra secretaria
    Quando confirmo a consulta
    Então vejo "* Usuario sem acesso a outro grupo *"

  Cenário: Sessão sem secretaria alcança a nota de qualquer secretaria
    Dado que a minha sessão não tem secretaria
    Quando consulto uma nota de qualquer secretaria
    Então a nota é mostrada normalmente

  Cenário: Nota sem composição de pedidos
    Dado que a nota existe e não tem nenhum pedido em sua composição
    Quando confirmo a consulta
    Então vejo "* Nota fiscal sem composicao de pedidos *"
    E nenhuma lista é apresentada

  Cenário: A lista mostra no máximo nove pedidos
    Dado que a nota tem mais pedidos do que cabem na lista
    Quando confirmo a consulta
    Então vejo no máximo nove linhas de pedido
    E vejo os totais do gênero somados por todos os pedidos da nota

  Cenário: Nota marcada e processo pré-liquidado
    Dado que a nota está marcada com a abreviatura P
    E o andamento do processo está pré-liquidado
    Quando confirmo a consulta
    Então a situação mostrada é "Pre Liq"

  Cenário: Nota marcada e processo liquidado
    Dado que a nota está marcada com a abreviatura P
    E o andamento do processo está liquidado
    Quando confirmo a consulta
    Então a situação mostrada é "Liquida"

  Cenário: Nota marcada e processo em qualquer outra situação
    Dado que a nota está marcada com a abreviatura P
    E o andamento do processo não está pré-liquidado nem liquidado
    Quando confirmo a consulta
    Então a situação mostrada é "Paga"

  Cenário: Nota sem a marcação
    Dado que a nota não está marcada com a abreviatura P
    Quando confirmo a consulta
    Então a situação mostrada é "Fechada"

  Cenário: Nota achada no outro cadastro é rotulada de Lote
    Dado que a nota só existe no cadastro de notas fiscais N013T
    Quando confirmo a consulta
    Então o número que encabeça a lista aparece rotulado de "Lote"

  Cenário: Os nomes mostrados vêm dos cadastros
    Dado que consultei uma nota com fornecedor, órgão, fonte, modalidade, gênero e operador cadastrados
    Então cada nome mostrado é o que está no cadastro correspondente
    E o número do processo aparece em partes, separadas por barra
```
