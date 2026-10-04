# US — E054C — Consultar os pedidos pendentes de distribuição da coordenadoria regional escolar

## Estória

Como **servidor de CRE**, quero **consultar, para a minha coordenadoria regional
escolar, os pedidos de distribuição que continuam pendentes — com o órgão de
destino, o fornecedor e o período de entrega de cada um**, para que **eu saiba o
que ainda falta distribuir, para quem e em que período, e possa acompanhar a
distribuição pelo número do pedido**.

A alimentação escolar só chega ao órgão depois que o pedido deixa de estar
pendente de distribuição. Enquanto ele está pendente, a mercadoria ainda não foi
distribuída, e é esta a visão que mostra, sem abrir pedido por pedido, o que
continua aberto numa coordenadoria. O que a tela informa é o que as telas de
distribuição usam para decidir o próximo passo; sem ela, o acompanhamento vira
tentativa e erro. Ela é só de leitura: não inclui, não altera e não exclui pedido
nenhum.

## Contexto

Jornada S000M → E000M → E050M → E054C.
Ator: servidor de CRE — consulta, na sua coordenadoria, os pedidos que continuam
pendentes de distribuição.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

As regras abaixo são só as da **tela desta jornada**. O `E000M` e o `E050M` não
gravam nada: apenas encaminham, e não registram origem nem operação na sessão. O
contexto que a `E054C` usa — quem é o operador, qual o tipo de órgão, qual o
código de acesso e qual a coordenadoria — é o que a entrada deixou na sessão.

---

## Regras de negócio

### RN-01 — A tela abre em consulta e não aceita outra operação

A tela é de consulta. A cada apresentação ela repõe a consulta como a operação
em vigor, e é essa operação que ela leva à conferência do sistema — qualquer
outra que chegue até lá é recusada, com **\* Operacao nao disponivel \***, antes
de qualquer pedido ser lido. Como ela repõe a consulta por conta própria, a
operação **não** é herdada de quem a chamou: venha a tela do menu ou de outra
tela, ela abre sempre em consulta, e não existe caminho em que esta tela abra em
alteração.

[?] A recusa por operação diferente de consulta pressupõe que a operação chegue
preenchida com outro valor. Esta tela repõe a consulta antes de conferir, e a
ficha extraída do programa não declara nenhuma opção nem campo de operação
visível. Se não existir formulário que mande outro valor, essa recusa é trecho
inalcançável por este caminho. Pergunta ao site.

### RN-02 — Só a minha coordenadoria é consultada

A consulta é sempre de uma coordenadoria regional escolar. Quem está vinculado a
uma coordenadoria na sessão só consulta essa: informando outra, a tela recusa com
**\* Usuario sem acesso a este grupo \***, devolve o cursor ao campo da
coordenadoria e não lista pedido nenhum. Quem não está vinculado a nenhuma — o
usuário da secretaria — pode consultar qualquer coordenadoria, desde que ela
exista no cadastro da sua secretaria para o tipo de órgão da sessão; não
existindo, a recusa é **\* Grupo nao pertence a esta secretaria \***, também com
o cursor no campo da coordenadoria. Quando a coordenadoria informada é a mesma
que já estava em uso, a conferência de cadastro não se repete.

[?] A conferência compara a coordenadoria informada com a que a sessão carrega, e
este acervo não mostra o caminho que leva esse valor da área da sessão até a área
de trabalho que a tela lê. Se ele não for transportado, todo operador cai no ramo
do usuário sem coordenadoria e a regra "só vejo o meu grupo" deixa de valer.
Pergunta ao site.

### RN-03 — A lista sai do cadastro de pedidos e só traz os pendentes de distribuição

Os pedidos vêm do cadastro de pedidos de distribuição, que tem **22 campos** e
capacidade declarada para **10.000.000** de registros (capacidade é o máximo
esperado, parâmetro de dimensionamento, não o que está cadastrado). Cada pedido
tem uma situação — **pendente de distribuição**, já aprovado ou já fechado — e
pode estar marcado como excluído. Esta tela só mostra os **pendentes de
distribuição**: um pedido de outra situação que apareça na posição procurada é
tratado como se não existisse, e os pedidos excluídos ficam fora do conjunto que
a tela percorre. O que ela lista é, portanto, exatamente o que ainda falta
distribuir na coordenadoria.

[?] Depois de ler o pedido, a tela tem uma conferência que manda pular o registro
quando ele está marcado como excluído — mas o conjunto de onde ela lê já deixa os
excluídos de fora. Ou a conferência é defesa redundante, ou a leitura não aplica
o filtro do conjunto. O acervo não decide entre as duas. Pergunta ao site.

### RN-04 — A lista traz até 14 pedidos, com órgão, fornecedor e período

A lista tem **14 linhas**, e cada linha traz **nove informações**: o número do
pedido, o ano da entrega, o órgão de destino, o código e a razão social do
fornecedor, um código de uma posição que vem do próprio pedido, a data de início
do período de distribuição, a letra "a" como separador e a data limite do
período. As duas datas saem no formato **dia/mês/ano**, com dia e mês em dois
dígitos e o ano em quatro. A razão social do fornecedor sai do cadastro de
fornecedores; não havendo o fornecedor, a linha aparece sem a razão social e sem
aviso. Não havendo mais pedido pendente para mostrar, a listagem para e as linhas
restantes ficam em branco.

[?] O código de uma posição que cada linha mostra não tem significado no acervo
lido nem no manual: o dicionário de dados só diz que é um caractere, e nenhum
rótulo do sistema o descreve. Pergunta ao site.

### RN-05 — A consulta começa no pedido informado

Para escolher por onde a lista começa, informa-se o **número do pedido** e o
**ano da entrega**: a tela procura esse pedido dentro da coordenadoria e monta a
lista a partir da posição dele. Não achando — por não existir, por não estar
pendente de distribuição ou por estar excluído — a tela **não avisa nada**: a
posição volta ao início e a lista é refeita desde o primeiro pedido pendente da
coordenadoria. Quando a página se completa com as 14 linhas, a tela guarda a
posição do pedido da última linha, para que a continuação saia dali; quando a
página termina antes da 14ª linha, a posição guardada volta ao início.

[?] O número do pedido e o ano da entrega são procurados por um recurso de
posicionamento do dicionário de dados cujo efeito exato não está no acervo nem no
manual — a rotina que faz a leitura é importada de uma biblioteca que não tem
fonte aqui, e a conferência seguinte nunca compara o ano nem o pedido lido. Se a
leitura exigir a chave exata, a continuação de uma página cheia repete a última
linha mostrada; se ela apenas posicionar na primeira chave igual ou posterior, a
continuação avança. Os dois comportamentos são compatíveis com o que o fonte
mostra, e o acervo não decide entre eles. Pergunta ao site.

### RN-06 — Não havendo pedido pendente, a tela avisa

Não havendo nenhum pedido pendente de distribuição na coordenadoria, a tela avisa
**\* Grupo sem pedidos pendentes de distribuicao \*** e não preenche nenhuma
linha da lista. O aviso é decidido na montagem da **primeira linha** da página e
não é repetido nas demais.

[?] Como o aviso é decidido uma única vez, na primeira linha, e não é recalculado
depois, uma lista que esvazie mais adiante fica em branco sem explicação. Se isso
é o pretendido ou resíduo do gerador, é pergunta ao site.

### RN-07 — A digitação é editada como número, e o campo em branco vale zero

Os campos numéricos da consulta — a coordenadoria, o número do pedido, o ano da
entrega e os dois campos de posição que a tela mantém por conta própria — passam
por edição numérica antes de qualquer leitura: campo em branco é tratado como
zero, e o que não for número é recusado, sem que a consulta siga. O cursor volta
ao campo recusado para a coordenadoria e para os dois campos de posição.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual —
não está nos fontes desta jornada: a rotina que faz a edição numérica é importada
de uma biblioteca que não tem fonte aqui.

[?] O número do pedido e o ano da entrega têm rótulo de negócio e são editados,
mas não têm posição de cursor definida entre os campos de recusa: se a recusa cair
em um deles, o acervo não diz onde o cursor fica. Pergunta ao site.

### RN-08 — Fora da lista, a tela mostra a data do sistema e o tipo de órgão

Fora da lista, a tela exibe a **data do sistema** e a **descrição do tipo de
órgão** da sessão.

[?] Nem a data do sistema nem a descrição do tipo de órgão são preenchidas por
nenhum caminho que este acervo mostre: as duas aparecem sempre como origem de
cópia, e as únicas escritas nesses dois campos são limpezas para espaço em branco
dentro do programa de runtime. A entrada guarda a descrição do tipo de órgão numa
área da sessão enquanto a tela a lê de outra. Se o ambiente transporta o valor de
uma área para a outra — e de onde vem a data do sistema —, é pergunta ao site; se
não transportar, os dois campos saem em branco.

### RN-09 — Cada consulta começa com os campos de resultado limpos

Antes de conferir a digitação e de ler qualquer pedido, a tela apaga os **nove**
campos de resultado que a consulta anterior havia mostrado: a descrição do tipo
de órgão, a data do sistema, o órgão, o código e a razão social do fornecedor, o
código do pedido, as duas datas do período e o separador. Uma consulta recusada,
portanto, não deixa na tela o resultado da consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se
existe um caminho de entrada em que os campos não são limpos, não foi possível
determinar. Pergunta ao site.

### RN-10 — Antes de mostrar a lista, o sistema confere o acesso

A abertura da tela passa por conferências de acesso com o contexto da sessão —
matrícula, código de acesso, privilégio, tipo de órgão e coordenadoria. A tela
precisa estar cadastrada: não estando, o acesso é recusado com **\* Tela nao
disponivel \*** (a lógica de rota usa **\* Tela nao cadastrada \*** para o mesmo
caso). A matrícula precisa ter a tela autorizada no seu código de acesso: não
tendo, a recusa é **\* Acesso negado para esta matricula \***. O contexto da
sessão não é recalculado aqui: é o que a entrada deixou.

[?] A conferência de operação procura os indicadores de inclusão, de alteração e
de exclusão, mas **não** o de consulta: quem tem a tela autorizada consulta sem
precisar do indicador de consulta. Se a intenção era exigir esse indicador por
tela, o caminho não o exige. Pergunta ao site.

[?] A mesma falta — tela não cadastrada — tem duas mensagens diferentes, porque
duas rotinas comuns conferem isso em momentos distintos: a da abertura e a da
rota, que roda quando o operador envia a consulta. Qual das duas o operador vê
depende do momento. Pergunta ao site.

### RN-11 — A consulta não grava nada e não deixa rastro de auditoria

A tela e as rotinas comuns que ela chama só leem. Nenhum pedido, fornecedor,
coordenadoria ou tela é incluído, alterado ou excluído, e nenhum registro de
auditoria é gerado. As operações de gravação, de exclusão e de travamento de
registro existem declaradas para os quatro cadastros que a tela enxerga, mas não
são executadas em nenhum caminho: declarar não é executar.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar os pedidos pendentes de distribuição da coordenadoria regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E054C

  Cenário: A lista dos pedidos pendentes da minha coordenadoria
    Dado que a minha coordenadoria tem pedidos pendentes de distribuição
    Quando abro a tela E054C
    Então vejo as linhas com o número do pedido, o ano da entrega, o órgão de destino, o fornecedor e o período de distribuição

  Cenário: A lista mostra até 14 pedidos
    Dado que a minha coordenadoria tem mais de 14 pedidos pendentes de distribuição
    Quando abro a tela E054C
    Então a lista mostra no máximo 14 linhas
    E as linhas restantes ficam em branco

  Cenário: O período aparece no formato dia/mês/ano
    Dado que um pedido pendente tem período de distribuição registrado
    Quando abro a tela E054C
    Então vejo a data de início e a data limite no formato dia/mês/ano, com o ano em quatro dígitos
    E entre as duas datas vejo a letra "a"

  Cenário: Pedido de fornecedor que não está no cadastro
    Dado que um pedido pendente aponta para um fornecedor que não está no cadastro de fornecedores
    Quando abro a tela E054C
    Então a linha daquele pedido aparece sem a razão social
    E nenhum aviso é mostrado

  Cenário: Fora da lista, a data do sistema e o tipo de órgão
    Dado que entrei no sistema
    Quando abro a tela E054C
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: Consulta a partir de um pedido informado
    Dado que existe um pedido pendente de distribuição com o número e o ano da entrega que informei
    Quando envio a consulta
    Então a lista é montada a partir desse pedido

  Cenário: Pedido informado que não está pendente de distribuição
    Dado que informo o número e o ano da entrega de um pedido aprovado, fechado ou excluído
    Quando envio a consulta
    Então não vejo aviso nenhum
    E a lista é refeita desde o primeiro pedido pendente da coordenadoria

  Cenário: Coordenadoria sem pedidos pendentes
    Dado que a minha coordenadoria não tem nenhum pedido pendente de distribuição
    Quando abro a tela E054C
    Então vejo a mensagem "* Grupo sem pedidos pendentes de distribuicao *"
    E nenhuma linha da lista é preenchida

  Cenário: Coordenadoria fora do meu acesso
    Dado que estou vinculado a uma coordenadoria na sessão
    Quando informo outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenadoria
    E nenhum pedido é listado

  Cenário: Coordenadoria que não pertence à minha secretaria
    Dado que não estou vinculado a nenhuma coordenadoria na sessão
    Quando informo uma coordenadoria que não existe no cadastro da minha secretaria
    Então vejo a mensagem "* Grupo nao pertence a esta secretaria *"
    E o cursor volta ao campo da coordenadoria
    E nenhum pedido é listado

  Cenário: Operação diferente da consulta
    Dado que estou na tela E054C
    Quando a operação que chega ao sistema não é a consulta
    Então vejo a mensagem "* Operacao nao disponivel *"
    E nenhum pedido é lido nesse caminho

  Cenário: A operação não é herdada de quem chamou a tela
    Dado que chego à tela E054C por um caminho que não é o menu
    Quando a tela abre
    Então ela abre em consulta, e não em alteração
    E não há como gravar pedido nenhum por esta tela

  Cenário: Digitação não numérica
    Dado que digito na coordenadoria, no número do pedido ou no ano da entrega algo que não é número
    Quando envio a consulta
    Então o sistema recusa a digitação antes de listar qualquer pedido

  Cenário: O resultado da consulta anterior não fica na tela
    Dado que já abri a tela e ela mostrou pedidos
    Quando volto a consultar
    Então o órgão, o fornecedor, o código do pedido e as datas da consulta anterior não ficam na tela

  Cenário: Tela não cadastrada
    Dado que a tela E054C não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo consultar

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela E054C autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo consultar

  Cenário: A consulta não grava nada
    Dado que abro a tela E054C
    Quando a lista é mostrada
    Então nenhum pedido é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado
```
