# US — C693C — Consulta de contrato do FINCON e grupos de licitação

## Estória

Como **servidor de CRE**, quero **consultar um contrato do FINCON pela coordenadoria
regional, pelo número e pelo ano, e ver os grupos de licitação que o compõem**, para que
**eu escolha o grupo certo e siga para a tela que trata a permissão daquele grupo sem
digitar de novo o contrato, sabendo que ele é o do meu órgão e o da minha regional**.

O contrato do FINCON é o que fixa, para uma coordenadoria regional, o tipo de contrato, o
período e o fornecedor; o que a regional pode licitar e comprar, porém, não pende do
contrato inteiro, e sim de um **grupo de licitação** dele. Esta tela é a ponte entre os
dois: mostra o contrato e lista os grupos, um por linha, com a descrição vigente de cada
um. Nada aqui é decidido nem gravado — é a tela em que o servidor reconhece o grupo que
quer trabalhar. Sem ela, quem trata a permissão teria de saber de cor o grupo e a
vigência, e não teria como conferir se o contrato é mesmo o da sua regional.

## Contexto

Jornada S000M → C000M → C050M → C690M → C693C.

Ator: servidor de CRE — informa a coordenadoria regional, o número e o ano do contrato,
confere os dados que a tela mostra e escolhe na lista o grupo de licitação por onde
segue.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os três passos anteriores — C000M, C050M e C690M — são menus e não gravam nada nem
deixam operação marcada: a C693C abre pelo que a entrada deixou na sessão. Ela é tela de
**consulta** e, escolhido o grupo, **encadeia na C060T**, sem passar por menu.

---

## Regras de negócio

### RN-01 — O que esta tela consulta

A tela consulta um **contrato do FINCON** e o mostra inteiro: a coordenadoria regional, o
número e o ano do contrato, o tipo de contrato, o dia, o mês e o ano de início do
período, o dia, o mês e o ano limite, e a razão social do fornecedor. Junto com o
contrato, ela lista os **grupos de licitação** daquele contrato, um por linha, com a
descrição vigente do grupo na data limite do contrato.

O contrato, a coordenadoria e a permissão só são procurados **no órgão da sessão**: o
servidor vê o que é do órgão em que entrou. Os cadastros de apoio — fornecedor, tipo de
licitação, descrição do grupo e operador — são procurados pelo próprio código que o
contrato ou a permissão trazem.

Dois desses apoios não aparecem nesta tela: a descrição do tipo de licitação e o nome do
operador são lidos apenas para seguir com o servidor (RN-13).

### RN-02 — A tela abre sempre em consulta, e já com a coordenadoria do servidor

A operação de manutenção chega em branco e o sistema a toma por **consulta**. Não há,
nesta jornada, quem abra a tela em alteração: quem a chama é um menu que não deixa
operação marcada, e a própria tela repõe a consulta na primeira montagem — o modo da tela
não depende de quem a chamou.

O campo da **coordenadoria regional** vem preenchido com a coordenadoria do vínculo do
servidor. Quando o vínculo não tem coordenadoria, o campo fica em branco e o servidor
pode informar qualquer uma (RN-06). Fora do contrato, a tela mostra a descrição do órgão
da sessão e a data do sistema, e limpa o que a consulta anterior tinha mostrado do
fornecedor e do grupo.

### RN-03 — A consulta não grava nada

Esta tela só lê. Ela enxerga nove cadastros e traz, para todos eles, os trechos de
gravação, de exclusão e de travamento; **nenhum deles é acionado**: não há um único ponto
em que a tela grave, altere ou exclua registro. O que ela faz é ler — o contrato, a
coordenadoria, a lista de grupos, as descrições de apoio e a tela que a seguinte vai
mostrar.

A consulta também não deixa rastro de negócio: não atualiza o contrato, a permissão nem
qualquer cadastro de apoio. A única escrita que pode acontecer na passagem por esta tela
vem da camada comum a todas as telas e não é da consulta: enviada a operação de **fim de
sessão**, o sistema atualiza o cadastro da sessão com a hora, a data e o fim, e devolve o
terminal à saída.

[?] O que faz chegar até aqui a operação de fim de sessão — uma tecla de saída do
terminal, uma opção do formulário — não está nesta jornada.

### RN-04 — A tela só atende consulta

Qualquer operação diferente de consulta é recusada com
**\* Opcao nao disponivel. Use CON \***, com o cursor de volta no campo da operação,
antes de ler qualquer contrato. Há uma recusa possível antes dessa: se o servidor não tem
a operação liberada no seu código de acesso, a mensagem é
**\* Acesso negado para esta operacao \*** (RN-05); tendo a operação liberada, a recusa é
a da opção indisponível.

A tela se declara apta à manutenção para a rota do sistema e, logo depois, recusa a
manutenção: o único modo que passa é a consulta.

[?] A recusa manda usar "CON", mas o sistema reconhece a consulta por um código interno
de três letras — o mesmo que o acervo usa em todas as telas —, e não há nenhum literal
"CON" nem "ALT" no corpus lido. Ou o formulário traduz o que o servidor digita para esse
código, ou quem seguir a mensagem é recusado. Pergunta ao site.

### RN-05 — A abertura confere a sessão, a tela e o acesso do servidor

Antes de mostrar qualquer dado, a tela passa pelas conferências comuns a todas as telas:
a **estação** da sessão tem de ser a que está gravada no cadastro do funcionário — sendo
outra, a sessão é encerrada e o terminal volta à saída; a requisição marcada como
**página 2** é recusada com **\* Acesso a pagina 2 negado \***; a **tela** tem de estar
cadastrada no cadastro de telas, senão a recusa é **\* Tela nao disponivel \***; e a
**matrícula** precisa ter registro de acesso àquela tela no seu código de acesso, senão a
recusa é **\* Acesso negado para esta matricula \***.

No caminho da operação, a tela chama ainda a lógica de rota e a conferência de operação
por tela: a tela tem de estar ativa no cadastro de telas, senão a recusa é
**\* Tela nao cadastrada \***, e a operação enviada tem de ser uma que o cadastro de
telas reconheça, senão a recusa é **\* Operacao nao disponivel \***. Operação que o
código de acesso do servidor não libera é recusada com
**\* Acesso negado para esta operacao \***. Falhando qualquer uma dessas conferências,
nada é lido e nada é gravado.

### RN-06 — A coordenadoria informada tem de ser a do servidor

A coordenadoria regional informada tem de ser igual à do vínculo do servidor. Sendo
outra, a recusa é **\* Usuario sem acesso a este grupo \***, com o cursor na
coordenadoria, antes de qualquer leitura de contrato. Quando o vínculo do servidor não
tem coordenadoria, essa conferência não barra nada: qualquer coordenadoria é aceita, e aí
é o cadastro de coordenadorias que decide (RN-07).

### RN-07 — A coordenadoria informada tem de existir

A coordenadoria é procurada no cadastro de coordenadorias regionais, junto com o órgão da
sessão. Não existindo, a recusa é **\* Grupo nao cadastrado \***, com o cursor na
coordenadoria, e a tela não procura o contrato. A mensagem fala de "grupo", embora o que
a tela procura nesse ponto seja a coordenadoria regional.

### RN-08 — O número e o ano do contrato andam juntos

A consulta exige **número do contrato e ano do contrato**. Faltando um dos dois, a recusa
é **\* Informe o Contrato FINCON \***, com o cursor no número do contrato. Sem os dois, a
tela não procura o contrato nem lista grupo nenhum.

### RN-09 — O contrato tem de estar cadastrado

O contrato é procurado pelo órgão da sessão, pela coordenadoria regional, pelo número e
pelo ano. Não existindo, a recusa é **\* Contrato FINCON nao cadastrado \***, com o
cursor no número do contrato, e a tela não segue para a lista nem mostra dados do
contrato. Um contrato já consultado não é procurado de novo enquanto a coordenadoria, o
número e o ano em tela forem os mesmos.

### RN-10 — Os campos numéricos passam pela edição numérica

Os doze campos de código e de data da tela — coordenadoria, número, tipo e ano do
contrato, os três pares de dia, mês e ano, o código do fornecedor e o grupo de licitação
— são tratados como número: o que estiver em branco vira zero e o que não for número é
recusado antes de qualquer procura. O cursor volta ao campo quando o erro é na
coordenadoria, no número do contrato ou no ano do contrato; nos outros campos o erro é
acusado sem reposicionamento do cursor.

[?] A rotina que faz a edição numérica e a que separa o campo são importadas de fora do
acervo: a mensagem que o servidor vê ao digitar um valor não numérico não está no corpus
lido. Pergunta ao site.

### RN-11 — A grade tem onze linhas, e a lista continua de onde parou

A lista de grupos ocupa **onze linhas**. Cada linha traz o **grupo de licitação** e a
**descrição do grupo** vigente na data limite do contrato; os grupos listados são os
daquele contrato — mesma coordenadoria, mesmo fornecedor, mesmo tipo de contrato e mesma
data limite. A leitura começa no primeiro grupo do contrato e **continua de onde a
listagem anterior parou**: a chave do último grupo listado fica guardada, e reenviar a
consulta traz os grupos seguintes; grupo repetido não ocupa duas linhas. Quando não há
nenhum grupo para o contrato, a tela avisa **\* Grupamentos nao cadastrados \*** e não
lista nada.

[?] A primeira leitura da lista usa o recurso de posicionamento do dicionário de dados,
cujo efeito exato não está no acervo nem no manual: se ele exige a chave exata, o
contrato só acharia grupo se o grupo tivesse classe, subclasse e gênero zerados — e a
lista responderia "grupamentos não cadastrados" em qualquer contrato; se posiciona no
primeiro registro igual ou posterior, o que foi informado é apenas o ponto de partida da
lista. O site precisa dizer qual é o esperado.

### RN-12 — Para levar um grupo adiante, o servidor marca a linha

O que leva o servidor à tela seguinte é a **marca** numa das linhas da lista: a linha
marcada tem de ter grupo. Marcando uma linha em branco, a recusa é
**\* Consulte linha preenchida \***, com o cursor na marca. Com a linha preenchida e
marcada, a permissão daquele grupo é lida e a tela segue.

[?] A permissão do grupo marcado é procurada, mas o "não encontrado" não gera recusa:
ele apenas marca a linha de status e a tela segue para a tela seguinte assim mesmo, com o
que tiver na área de trabalho. Ou o grupo marcado sempre existe por construção da lista,
ou esse caminho deixa passar uma permissão inexistente. Pergunta ao site.

### RN-13 — O que a tela entrega à tela seguinte

Escolhido o grupo, a tela não volta ao menu: ela **encadeia na C060T**, entregando a
permissão de contrato daquele grupo — a coordenadoria regional, o número e o ano do
contrato, o tipo de contrato, o fornecedor, o grupo de licitação, o início do período e a
data limite do contrato, as duas datas próprias da permissão, o tipo de licitação com a
sua descrição, o operador e os valores que a permissão guarda — e a operação de
**consulta**. Por isso a C060T abre em consulta; chegando a operação em branco, ela
recusaria com a mensagem própria dela.

[?] A tela prepara esses valores, mas o acervo não mostra por que caminho eles chegam à
tela seguinte: os registros das duas telas não guardam os mesmos campos na mesma ordem, e
não dá para afirmar que todos chegam. Pergunta ao site.

### RN-14 — Prefixo de tela preenchido abandona a consulta

Se a transação chega com o **prefixo de tela** preenchido, a consulta é abandonada antes
de qualquer leitura, e a rota leva o servidor à tela indicada. É o mesmo campo que as
outras telas do acervo usam como contexto de rota.

[?] Nenhum programa do acervo preenche esse prefixo para esta tela, e o menu que a abre
não o preenche: não se sabe quem o manda, nem se esse caminho é alcançável pelo terminal.
Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta de um contrato do FINCON e dos grupos de licitação da regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C693C

  Cenário: Consulto um contrato da minha coordenadoria
    Quando informo a coordenadoria regional, o número e o ano de um contrato cadastrado
    Então vejo o tipo de contrato, o início do período, a data limite e a razão social do fornecedor
    E vejo os grupos de licitação daquele contrato, um por linha, com a descrição do grupo

  Cenário: A tela abre em consulta e já com a minha coordenadoria
    Dado que o meu vínculo tem coordenadoria regional
    Quando a tela é aberta
    Então o campo da coordenadoria já está preenchido com a minha
    E a operação já está em consulta
    E nenhuma linha da lista está preenchida, porque o contrato ainda não foi informado

  Cenário: A consulta não grava nada
    Dado que consultei um contrato cadastrado
    Então nada foi gravado, alterado ou excluído no contrato, na permissão ou em qualquer cadastro de apoio
    E nenhuma trilha de auditoria foi deixada pela consulta

  Cenário: Operação diferente de consulta
    Quando informo uma operação de manutenção
    Então vejo "* Opcao nao disponivel. Use CON *"
    E o cursor volta para o campo da operação
    E nenhum contrato é lido

  Cenário: Operação não liberada no meu código de acesso
    Dado que não tenho a operação liberada para esta tela
    Quando envio uma operação de manutenção
    Então vejo "* Acesso negado para esta operacao *"
    E nada é lido nem gravado

  Cenário: Requisição marcada como página 2
    Quando a requisição chega marcada como página 2
    Então vejo "* Acesso a pagina 2 negado *"
    E não sigo na tela

  Cenário: Tela não cadastrada
    Dado que a tela não está cadastrada no cadastro de telas
    Quando tento abri-la
    Então vejo "* Tela nao disponivel *"
    E a consulta não abre

  Cenário: Matrícula sem acesso à tela
    Dado que o meu código de acesso não tem registro para esta tela
    Quando tento abri-la
    Então vejo "* Acesso negado para esta matricula *"
    E a consulta não abre

  Cenário: Sessão aberta em outra estação
    Dado que a sessão da minha matrícula está marcada em outra estação
    Quando tento abri-la
    Então a minha sessão é encerrada
    E o terminal volta à saída

  Cenário: Coordenadoria de outra regional
    Dado que o meu vínculo tem coordenadoria regional
    Quando informo uma coordenadoria regional diferente da minha
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor volta para o campo da coordenadoria
    E nenhum contrato é lido

  Cenário: Coordenadoria não cadastrada
    Quando informo uma coordenadoria regional que não existe no cadastro
    Então vejo "* Grupo nao cadastrado *"
    E o cursor volta para o campo da coordenadoria
    E a tela não procura o contrato

  Cenário: Servidor sem coordenadoria no vínculo informa a coordenadoria
    Dado que o meu vínculo não tem coordenadoria regional
    Quando informo qualquer coordenadoria cadastrada
    Então a tela aceita a coordenadoria informada
    E segue a consulta normalmente

  Cenário: Falta o número ou o ano do contrato
    Quando informo a coordenadoria e deixo o número ou o ano do contrato em branco
    Então vejo "* Informe o Contrato FINCON *"
    E o cursor fica no número do contrato
    E nenhuma linha é listada

  Cenário: Contrato não cadastrado
    Quando informo número e ano de um contrato que não existe na minha coordenadoria
    Então vejo "* Contrato FINCON nao cadastrado *"
    E o cursor fica no número do contrato
    E nenhum dado do contrato é mostrado

  Cenário: Campo não numérico
    Quando informo letras num campo de código ou de data
    Então a tela recusa o campo antes de procurar o contrato
    E nada é listado

  Cenário: Contrato sem grupos de licitação
    Dado que o contrato consultado não tem nenhum grupo de licitação
    Então vejo "* Grupamentos nao cadastrados *"
    E nenhuma linha da lista é preenchida

  Cenário: A lista continua de onde parou
    Dado que o contrato tem mais de onze grupos de licitação
    Quando consulto o contrato
    Então a lista mostra onze grupos
    Quando reenvio a consulta sem mudar nada
    Então a lista traz os grupos seguintes, a partir do último que apareceu

  Cenário: Linha marcada sem grupo
    Dado que consultei um contrato cadastrado
    Quando marco uma linha que não tem grupo
    Então vejo "* Consulte linha preenchida *"
    E o cursor fica na marca da linha
    E não sigo para a tela seguinte

  Cenário: Marco a linha e sigo para a tela da permissão
    Dado que consultei um contrato cadastrado com os grupos listados
    Quando marco a linha de um grupo
    Então a tela seguinte abre em consulta
    E ela recebe aquele contrato, aquela coordenadoria e a permissão daquele grupo

  Cenário: Prefixo de tela preenchido
    Quando a transação chega com o prefixo de tela preenchido
    Então a consulta é abandonada antes de qualquer leitura
    E sou levado à tela indicada no prefixo
```
