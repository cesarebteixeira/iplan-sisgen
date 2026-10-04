# US — C330C — Consultar operadores cadastrados

## Estória

Como **servidor de CRE que responde pelo cadastro de operadores da sua secretaria**, quero
**consultar a lista de operadores cadastrados, com o código, o nome e o CNPJ de cada um**, para que
**eu encontre o operador certo sem ter de decorar o código dele e possa abrir a ficha completa em
consulta**.

Esta tela existe porque o cadastro do operador é grande — ele guarda a razão social, o CNPJ, o
endereço, o bairro, o CEP, a cidade, o estado, o contato, o telefone, o ramal, a inscrição estadual e
o CPF/CGC. O servidor reconhece o operador pelo nome, não pelo número. É a lista desta tela que dá o
ponto de partida: sem ela, quem não decora o código não chega à ficha. Nada aqui é gravado — a ficha
é mantida na tela que esta abre, e a lista só a consulta.

## Contexto

Jornada S000M → C000M → C015M → C330C.

Ator: servidor de CRE — percorre a lista dos operadores cadastrados dentro do conjunto da sua
secretaria e escolhe um deles para abrir a ficha completa em consulta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio. Os dois menus do caminho não gravam nada: só encaminham.

A tela recebe da sessão a **secretaria (o tipo de órgão)**, a **coordenação regional escolar**, a
**matrícula**, o **código de acesso**, o **privilégio** e a **estação**, e exibe a **data do
sistema** e o **nome da secretaria** que vêm dessa carga. O **órgão filho do servidor**, que a
entrada também carrega, **não** limita esta tela: o cadastro de operador não pertence a órgão. Essa
carga é regra da entrada e está no anexo, em **Regras que se revelaram da entrada**.

O que esta tela faz é uma passagem: ela lista os operadores e, marcado um deles, **passa o registro
e a operação para a ficha do operador, que abre em consulta** (RN-10 e RN-11). É por isso que a
jornada termina aqui — quem mostra a ficha é a tela seguinte, e a tela desta jornada é o índice
dela. A tela seguinte não abre esta em consulta: ela **devolve o controle** para cá.

## Regras de negócio

### RN-01 — A tela consulta os operadores cadastrados e mostra cada um em uma posição da lista

Esta é uma tela de **consulta**. Ela lista os operadores cadastrados e, de cada um, mostra o
**código do operador**, o **nome (razão social)** e o **CNPJ**, com a **marca de situação**. A
primeira posição da página é também o ponto de partida da leitura e carrega a **coordenação regional
escolar** informada.

No alto a tela exibe o **nome da secretaria** e a **data do sistema**, que vêm da sessão. Nada nesta
tela é gravado: nem cadastro, nem travamento de registro, nem linha de auditoria. A tela também não
aceita inclusão, alteração nem exclusão: o único uso é encontrar o operador e abrir a ficha dele.

### RN-02 — A lista é lida na ordem do código do operador e cabe em quinze posições

A lista é lida na ordem do **código do operador**, e não do nome. O que se informa na primeira
posição é o ponto de partida dessa ordem: **em branco, a lista começa no começo do cadastro**;
preenchido, a leitura começa naquele código. Cada posição seguinte é o operador seguinte a ela.

A tela trabalha com **quinze posições** de operador, e a leitura avança de uma em uma até a última
posição da página. Se o cadastro tiver mais operadores do que isso, a página cobre os quinze
primeiros da ordem, e o que sobra não aparece.

### RN-03 — De cada operador a lista mostra três dados, mais a marca de situação

De cada operador registrado, o que o servidor vê na posição é o **código**, o **nome (razão
social)** e o **CNPJ**. A **marca de situação** guardada no cadastro do operador também é exibida,
como um campo de um caractere.

[?] A marca de situação é exibida exatamente como está guardada no cadastro, sem que a tela decida o
que o conteúdo significa, e o material lido não traz nem o rótulo do campo na máscara da tela nem a
tabela de valores possíveis. O que ela quer dizer para quem usa a tela, e qual conteúdo ela pode
ter, só se responde no site.

### RN-04 — O código do operador é conferido antes de qualquer uso

O código do operador informado passa por uma conferência de número **antes** de qualquer uso: o que
não for número é recusado no próprio campo, com o cursor de volta nele, e nada é listado por causa
disso. O código em branco é tratado como zero, isto é, a lista começa no começo.

### RN-05 — A consulta exige permissão de operação para a tela

A consulta só roda para quem tem o código de acesso autorizado nesta tela: o sistema lê o cadastro
de telas por código de acesso e confere a permissão da operação de **consulta**. Sem essa permissão,
o aviso correspondente é apresentado e nada é listado.

[?] Na conferência por operação, a consulta cai no ramo que exige a permissão de **alteração**, e a
permissão de consulta declarada no cadastro de telas não é lida em nenhum ponto da rotina. Ou uma
tela de consulta exige mesmo a permissão de alteração, ou o ramo está conferindo a permissão errada.
É o mesmo defeito já registrado na tela C030C. Pergunta ao site.

### RN-06 — Sem operador cadastrado, a tela avisa e não lista

Quando a **primeira posição** da lista não traz nenhum operador, a tela avisa
**\* Nao existem operadores cadastrados \*** e não lista nada. O aviso é o do topo da lista: ele não
se repete a cada posição vazia, e sim uma vez, na montagem da primeira posição.

A mesma posição serve para dizer onde a leitura começa e para dizer que ela não achou nada.

### RN-07 — A lista não avança sem um código de operador no ponto de partida

A consulta só procura um operador adiante quando **há um código informado** na posição de partida.
Com o código zerado — em branco ou zero —, a tela não procura operador nenhum: a lista se encerra
sem mostrar nada e sem acusar falta de operador cadastrado.

[?] A posição de partida é a **primeira da página**, e não há no fonte nenhum caminho que a
preencha: o código informado na primeira posição é descartado ao fim de cada operação, e o que a
tela guarda na sessão é o código da posição **seguinte**. Ou seja, a lista só avança quando há um
código informado, e o material lido não mostra como o servidor informa esse código. Pergunta ao
site.

### RN-08 — Falha de leitura ou registro travado interrompe a consulta e avisa

Toda leitura desta tela testa o erro do banco. Erro de leitura que não seja "não achado" vira a ação
de erro de acesso, com a mensagem de erro do sistema, e a operação para ali, sem completar a lista.
O **registro travado** por outra pessoa, quando aparece na leitura, cai na mesma interrupção: o
operador simplesmente não é mostrado.

### RN-09 — A tela não grava, não exclui e não trava registro

Nenhuma das operações de gravação, exclusão ou travamento que o programa carrega é executada por
esta tela. As declarações existem para todos os cadastros que ela enxerga — é assim que o gerador
monta o programa —, mas a tela não as aciona: a única execução é a de **consulta**. O travamento de
registro aparece apenas dentro dos caminhos de exclusão, que a tela não percorre.

### RN-10 — Marcado o operador, a tela passa o registro e a operação de consulta

Marcado um operador na lista, a tela deixa o registro dele e a operação de **consulta** na área de
trabalho da sessão, marca a tela de origem e passa o controle para a **ficha do operador**. É esse
registro deixado na sessão que dispensa o servidor de informar o código na tela seguinte.

[?] A marcação é lida como o **indicador de seleção** da linha, e o fonte exige o valor **X** nele.
O programa **não escreve X em nenhum ponto**: o campo só é exibido e só é apagado por ocasião das
mensagens do operador. Como o material lido não traz a máscara da tela, não é possível decidir se é
a máscara que preenche esse indicador. Se não for, a passagem para a ficha não se completa por este
caminho e a operação fica inalcançável. Pergunta ao site.

### RN-11 — O que a ficha do operador recebe depende de quem a chamou

A ficha do operador recebe a operação de **consulta** quando vem desta lista, e não a recebe quando é
aberta pelo **menu**: nesse caso a ficha fica preparada para a **inclusão**, e é o menu que troca a
operação para consulta, zerando antes o operador que viesse da sessão.

Por isso esta tela deixa, além do **registro escolhido** e da **operação de consulta**, o
**indicador de continuação** ligado na área de trabalho da sessão: é ele que faz a ficha devolver o
controle para a lista com o resultado.

### RN-12 — Do menu, a tela desta jornada abre pronta para consultar

A tela desta jornada é alcançada por menu, e não por encadeamento de outra tela. Ela mesma fixa a
operação de **consulta**: independentemente do que houvesse na sessão, a leitura da lista é uma
consulta e não grava nada.

[?] O que a tela anterior da jornada deixa na sessão é o **tipo de órgão**, a **coordenação
regional escolar**, a **matrícula**, o **código de acesso**, o **privilégio** e a **estação**, e o
fonte não mostra que ela passe a operação: cada tela do caminho tem guarda de origem própria. O
material lido não permite afirmar que a C015M decida o modo desta tela. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consulta dos operadores cadastrados, por código, nome e CNPJ

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C330C

  Cenário: RN-01 — abrir a lista de operadores cadastrados
    Quando abro a tela C330C
    Então vejo, em cada posição, o código, o nome e o CNPJ do operador
    E vejo o nome da minha secretaria e a data do sistema

  Cenário: RN-01 — consultar não deixa rastro
    Dado que faço uma consulta
    Quando a consulta termina
    Então nenhum registro é travado
    E nenhuma linha nova aparece na trilha de auditoria

  Cenário: RN-02 — a lista é lida na ordem do código do operador
    Dado que existem operadores cadastrados
    Quando a lista é montada
    Então os operadores aparecem na ordem do código
    E cada posição seguinte é o operador seguinte ao da posição anterior

  Cenário: RN-02 — a lista cabe em quinze posições
    Dado que o cadastro tem mais operadores do que a página
    Quando a lista é montada
    Então vejo os quinze primeiros operadores da ordem
    E a leitura para na última posição da página

  Cenário: RN-03 — o que cada posição mostra do operador
    Dado que a lista mostra um operador cadastrado
    Quando leio a posição dele
    Então vejo o código, o nome, o CNPJ e a marca de situação do cadastro

  Cenário: RN-04 — código do operador com texto
    Quando informo texto no código do operador
    Então o campo é recusado antes de qualquer uso
    E o cursor volta para o campo
    E nada é listado

  Cenário: RN-04 — código do operador em branco
    Quando deixo o código do operador em branco na posição de partida
    Então o código é tratado como zero
    E a lista começa no começo da ordem

  Cenário: RN-05 — sem autorização para a tela
    Dado que não tenho o registro de autorização desta tela para o meu código de acesso
    Quando confirmo a consulta
    Então a tela não opera
    E nada é listado

  Cenário: RN-06 — nenhum operador cadastrado
    Quando confirmo a consulta e não há operador cadastrado
    Então vejo "* Nao existem operadores cadastrados *"
    E nenhum operador é listado

  Cenário: RN-06 — lista vazia no meio da página
    Dado que a lista começou em um operador cadastrado
    E a leitura chegou ao fim do cadastro antes da última posição
    Então as posições restantes ficam vazias
    E o aviso de nenhum operador cadastrado não aparece

  Cenário: RN-07 — posição de partida sem código
    Dado que a posição de partida está sem código de operador
    Quando confirmo a consulta
    Então nenhum operador é procurado
    E a lista se encerra sem mostrar nada

  Cenário: RN-08 — falha do banco durante a consulta
    Dado que a leitura do cadastro de operador falha no banco
    Quando confirmo a consulta
    Então a operação é interrompida com a mensagem de erro do sistema
    E a lista não é completada

  Cenário: RN-08 — registro travado por outra pessoa
    Dado que o operador procurado está travado por outra pessoa
    Quando confirmo a consulta
    Então esse operador não é mostrado
    E a operação para com o aviso do sistema

  Cenário: RN-09 — a consulta não grava
    Dado que a lista é montada e mostrada
    Quando a consulta termina
    Então o cadastro do operador não é alterado
    E nenhum registro é excluído nem travado

  Cenário: RN-10 — marcado o operador, a ficha dele se abre em consulta
    Dado que a lista mostra os operadores cadastrados
    E marco o indicador de seleção de um operador
    Quando confirmo
    Então a ficha daquele operador se abre em consulta
    E ela volta para esta lista com o resultado da consulta
    E nada é gravado por esta tela

  Cenário: RN-10 — a lista sem operador marcado não abre ficha
    Dado que a lista mostra os operadores cadastrados
    Quando confirmo sem marcar nenhum operador
    Então a tela segue mostrando a lista
    E nenhuma ficha se abre

  Cenário: RN-10 — a ficha não abre para quem não marcou
    Dado que a lista mostra os operadores cadastrados
    E o indicador de seleção da linha não está marcado
    Quando confirmo
    Então nenhum operador é passado adiante
    E a ficha não se abre por este caminho

  Cenário: RN-11 — a ficha aberta a partir da lista
    Dado que escolho um operador na lista
    Quando confirmo
    Então a ficha do operador abre em consulta sobre ele
    E ela volta para esta lista com o resultado da consulta

  Cenário: RN-11 — a ficha aberta pelo menu
    Dado que abro a ficha do operador pela opção do menu, sem passar pela lista
    Quando confirmo
    Então a ficha abre preparada para a inclusão
    E o menu troca a operação para consulta antes de abri-la

  Cenário: RN-12 — a tela desta jornada abre em consulta
    Dado que chego à tela C330C pela opção do menu da jornada
    Quando a tela monta a lista
    Então a operação é a de consulta
    E nada é gravado
```
