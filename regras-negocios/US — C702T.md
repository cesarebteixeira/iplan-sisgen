# US — C702T — Consulta das prorrogações da validade do cardápio

## Estória

Como **servidor de CRE**, quero **consultar, pela data limite, as prorrogações da
validade do cardápio**, para que **eu saiba quais cardápios tiveram a validade estendida e
qual é o período de cada um**.

O cardápio vale por um período, com data inicial e data limite, e esse período pode ser
prorrogado. Cada prorrogação fica registrada com o cardápio a que pertence e com o período
estendido. Esta tela é a consulta dessas prorrogações pela data limite, e é só de leitura:
não inclui, não altera e não exclui nada. Sem ela, quem precisa dizer até quando vale o
cardápio de um período não tem onde ver o que já foi prorrogado.

## Contexto

Jornada S000M → C000M → C070M → C702T.
Ator: servidor de CRE — consulta, pela data limite, as prorrogações de validade do
cardápio do seu tipo de órgão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O `C000M` e o `C070M` são menus: nenhum dos dois grava nada, e a `C702T` é aberta pelo
encaminhamento de uma opção da `C070M`, sem que lhe seja passada operação. O modo da
`C702T`, portanto, **não é decidido por quem a chama**: a tela é sempre de consulta. O
contexto que ela usa — matrícula, código de acesso, privilégio, tipo de órgão e CRE — é o
que a entrada deixou na sessão. A `C702T` não encaminha para nenhuma outra tela: ela não
passa registro nem operação adiante.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela é de consulta, e só a consulta é aceita

A `C702T` é a consulta das prorrogações e trabalha em um único modo: a **consulta**. Ao se
apresentar, ela repõe esse modo, e o envio só segue quando a operação informada é a
consulta. Chegando a operação em branco, a tela recusa com
**\* Operacao nao disponivel. Use CON \*** e devolve o cursor ao campo da operação, sem ler
prorrogação nenhuma nesse caminho.

[?] A recusa da própria tela só é alcançada quando a operação chega **em branco**. Para
qualquer outro valor diferente da consulta, quem recusa primeiro é a conferência de rota,
com **\* Operacao nao disponivel \*** — outra mensagem, e mais cedo no caminho. O que a
máscara da tela oferece ao operador não está no material desta jornada; se não há campo de
operação para preencher, a recusa da tela é trecho sem uso. Pergunta ao site.

[?] O valor que a tela aceita é o rótulo com que o sistema nomeia a consulta no idioma da
sessão, carregado em tempo de execução, e não o texto fixo "CON" que a mensagem manda usar.
Ou o formulário traduz o que o operador digita, ou quem seguir a mensagem ao pé da letra é
recusado. Pergunta ao site.

### RN-02 — A consulta é pela data limite, dentro do tipo de órgão da sessão

O operador informa **dia, mês e ano limite**, e toda leitura da tela acontece **dentro do
tipo de órgão da sessão** — ele vem do vínculo do servidor e não é digitado —, de modo que
cada servidor só vê as prorrogações do seu tipo de órgão. Reenviar exatamente a data que já
está em tela não refaz a busca: o que está lá é aceito como está.

Na primeira apresentação da tela numa sessão, a consulta não chega a ser feita e a lista
sai **vazia e sem aviso**: a tela guarda a data da última consulta no estado da sessão e só
lê a partir dela. Enquanto a data não vem desse estado, não há o que listar.

[?] O cadastro das prorrogações guarda **quatro conjuntos** de dia/mês/ano: início e limite
do período e início e limite da atualização. A tela **mostra** o par da atualização e
**procura** pelo par do limite do período, e o que separa um conjunto do outro não está no
material lido nem no manual. Pergunta ao site.

[?] A leitura só acontece a partir da segunda apresentação da tela na sessão, e o que faz
esse estado ser transportado de uma transação para a seguinte não está documentado no
material. Se ele não for transportado, a tela sempre abre sem lista. Pergunta ao site.

### RN-03 — A lista traz o cardápio, a descrição e as duas datas, em 14 linhas

A lista tem **14 linhas**, e cada linha traz **quatro informações**: o **código do
cardápio**, a **descrição do cardápio**, a **data inicial** e a **data limite**. As duas
datas saem no formato **dia/mês/ano**, com o dia e o mês em dois dígitos e o ano em quatro.
As prorrogações de uma mesma data limite saem na ordem do cadastro — o código do cardápio
primeiro e, dentro do mesmo cardápio, a atualização mais antiga antes da mais recente —, e a
lista para quando não há mais registro: as linhas restantes ficam em branco.

[?] A ordem em que a lista sai é a leitura da chave do cadastro — tipo de órgão, data
limite, código do cardápio e data e hora da atualização —, e o material lido não documenta
como cada leitura se posiciona na data informada: se exige a data exata ou se aceita a
primeira data igual ou posterior. Isso muda o que entra na lista. Pergunta ao site.

### RN-04 — A data informada passa por edição numérica, e o cursor volta ao campo recusado

Os três campos informados — dia, mês e ano limite — passam por edição numérica antes de
qualquer leitura: campo em branco é tratado como zero, e o que não for número é recusado,
sem a consulta seguir. O cursor volta ao campo recusado.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não está no
material desta jornada: a rotina que faz a edição numérica não faz parte do lote lido.
Pergunta ao site.

### RN-05 — O cabeçalho mostra a data do sistema e o tipo de órgão da sessão

Fora da lista, a tela exibe a **data do sistema** e a **descrição do tipo de órgão** da
sessão; para isso ela lê o cadastro dos tipos de órgão pela chave do tipo da sessão.

[?] A descrição exibida vem do contexto da sessão, e a que a tela lê do cadastro vai para
um campo que não é mostrado. Se o ambiente não transportar o contexto, o cabeçalho sai em
branco. Pergunta ao site.

### RN-06 — Não havendo prorrogação para a data em tela, a tela avisa

Não havendo nenhuma prorrogação registrada para a data que está em tela, a tela avisa
**\* Nao existem prorrogacoes para esta data \*** e não preenche nenhuma linha da lista. O
aviso é decidido na montagem da **primeira linha** e não se repete nas demais.

[?] Como o aviso é decidido uma única vez, e não é recalculado depois, uma lista que esvazie
mais adiante fica em branco sem explicação. Se isso é o pretendido ou resíduo do gerador, é
pergunta ao site.

### RN-07 — Data que é a data limite de um cardápio é trocada pela data limite inicial dele

Se a data informada não tiver prorrogação, mas for a **data limite de um cardápio
cadastrado**, a tela procura a prorrogação sob a **data limite inicial** daquele cardápio e
passa a mostrar o que estiver registrado sob essa outra data. Só quando não há prorrogação
para a data informada nem cardápio com aquela data limite é que a consulta é recusada com
**\* Nao existem reg de prorrogacao cadastrados \***, com o cursor de volta ao campo do dia.

[?] A troca é **silenciosa**: o operador pede uma data e recebe o resultado de outra, sem
aviso de que a data mudou. Se a máscara marca a troca de alguma forma, o material não diz.
Pergunta ao site.

[?] A segunda busca procura a prorrogação sob a data limite **inicial** do cardápio. O que
esse limite inicial significa em relação ao limite vigente — e por que a prorrogação estaria
registrada sob ele — não está no material lido. Pergunta ao site.

### RN-08 — A abertura da tela passa pelas conferências de acesso

A abertura da tela confere se a `C702T` está cadastrada no cadastro de telas e se a
matrícula tem a tela autorizada no seu código de acesso, com o contexto da sessão. Não
estando a tela cadastrada, a recusa é **\* Tela nao disponivel \***; não tendo a matrícula a
tela autorizada, **\* Acesso negado para esta matricula \***. A estação da sessão também é
conferida contra a estação registrada para a matrícula.

### RN-09 — O envio passa pela conferência de rota e pela permissão da operação

Quando o operador envia a data, a transação passa pela conferência de **rota** — que recusa
a tela não cadastrada, com **\* Tela nao cadastrada \***, e a operação que o sistema não
reconhece, com **\* Operacao nao disponivel \*** — e pela **permissão da operação**, que
exige a tela autorizada para o código de acesso do servidor. Não passando por qualquer
delas, a consulta é abandonada sem ler prorrogação nenhuma.

[?] O cadastro de autorização guarda, por tela e por código de acesso, liberadores separados
para incluir, alterar, excluir e consultar, e a conferência da operação **não lê o liberador
de consulta**: quem tem a tela autorizada consulta sem precisar dele. Como a tela só aceita
a consulta e a rota já recusa as demais operações antes, nenhuma recusa por liberador de
operação é alcançável por esta tela. Se era para a consulta ser liberada por tela, o caminho
não a exige. Pergunta ao site.

### RN-10 — A consulta não grava nada

A tela e as rotinas que ela chama só leem. Nenhuma prorrogação é incluída, alterada ou
excluída, e nenhum registro de auditoria é gerado. As operações de gravação, de exclusão e
de travamento existem declaradas para os cadastros que a tela enxerga, mas **não são
executadas em caminho nenhum**: declarar não é executar.

[?] Nenhum dos programas do material lido grava o cadastro das prorrogações — nem esta tela,
nem as telas anteriores da jornada. De onde as prorrogações vêm (carga, retaguarda ou outro
sistema) é pergunta ao site.

### RN-11 — A tela reapresenta a última data consultada

A data consultada fica guardada no estado da sessão e é reapresentada: voltando à tela na
mesma sessão, o dia, o mês e o ano limite já vêm preenchidos com a última consulta, e a
lista é montada a partir dela. Nada disso vai para cadastro nenhum: o que fica guardado é o
estado da tela na sessão.

## Cenários BDD

```gherkin
Funcionalidade: Consulta das prorrogações da validade do cardápio

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C702T

  Cenário: Consulta das prorrogações de uma data limite
    Dado que existe prorrogação registrada para a data limite que informei
    Quando envio a consulta
    Então vejo as prorrogações daquela data na lista

  Cenário: A lista tem 14 linhas, com quatro informações cada
    Dado que estou consultando uma data limite
    Quando a lista é montada
    Então ela mostra no máximo 14 linhas
    E cada linha traz o código do cardápio, a descrição, a data inicial e a data limite
    E as linhas restantes ficam em branco

  Cenário: As datas da lista saem em dia/mês/ano
    Dado que uma prorrogação listada tem data inicial e data limite registradas
    Quando a lista é montada
    Então vejo as duas datas em dia/mês/ano, com o dia e o mês em dois dígitos e o ano em quatro

  Cenário: As prorrogações saem na ordem do cadastro
    Dado que a data consultada tem mais de uma prorrogação registrada
    Quando a lista é montada
    Então cada linha traz um cardápio, na ordem do código
    E, dentro do mesmo cardápio, a atualização mais antiga vem antes da mais recente

  Cenário: O cabeçalho mostra a data do sistema e o tipo de órgão da sessão
    Dado que entrei no sistema
    Quando abro a tela C702T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: A consulta alcança só o meu tipo de órgão
    Dado que o meu vínculo é de um tipo de órgão
    Quando consulto uma data limite
    Então a lista traz apenas as prorrogações daquele tipo de órgão

  Cenário: A primeira apresentação da tela na sessão sai sem lista
    Dado que ainda não consultei nada nesta sessão
    Quando abro a tela C702T
    Então a lista sai vazia e sem aviso

  Cenário: Reenviar a mesma data não refaz a busca
    Dado que a data em tela não mudou
    Quando reenvio a consulta
    Então a tela aceita a data como está
    E a lista não é refeita

  Cenário: A tela reapresenta a última data consultada
    Dado que já consultei uma data nesta sessão
    Quando volto à tela C702T
    Então o dia, o mês e o ano limite já vêm preenchidos com a última consulta

  Cenário: Data sem prorrogação registrada
    Dado que a data em tela não tem nenhuma prorrogação registrada
    Quando a lista é montada
    Então vejo a mensagem "* Nao existem prorrogacoes para esta data *"
    E nenhuma linha da lista é preenchida

  Cenário: A data informada é trocada pela data limite inicial do cardápio
    Dado que informei a data limite de um cardápio cadastrado e ela não tem prorrogação própria
    Quando envio a consulta
    Então a tela passa a mostrar as prorrogações registradas sob a data limite inicial daquele cardápio

  Cenário: Data sem prorrogação e sem cardápio
    Dado que a data informada não é a data limite de nenhum cardápio cadastrado
    Quando envio a consulta
    Então vejo a mensagem "* Nao existem reg de prorrogacao cadastrados *"
    E o cursor volta ao campo do dia
    E nenhuma prorrogação é listada

  Cenário: Operação em branco
    Dado que envio a consulta com o campo da operação em branco
    Quando a tela confere a operação
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nenhuma prorrogação é lida nesse caminho

  Cenário: Operação diferente da consulta
    Dado que envio a consulta com uma operação que não é a de consulta
    Quando a transação é conferida
    Então vejo a mensagem "* Operacao nao disponivel *"
    E a consulta é abandonada sem ler prorrogação nenhuma

  Cenário: Digitação não numérica na data limite
    Dado que digito no dia, no mês ou no ano limite algo que não é número
    Quando envio a consulta
    Então o sistema recusa a digitação antes de listar qualquer prorrogação
    E o cursor volta ao campo recusado

  Cenário: Tela não cadastrada
    Dado que a tela C702T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo consultar

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela C702T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo consultar

  Cenário: A consulta não grava nada
    Dado que abro a tela C702T
    Quando a lista é mostrada
    Então nenhuma prorrogação é incluída, alterada ou excluída
    E nenhum registro de auditoria é gerado
```
