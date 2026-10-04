# US — C030C — Consultar fornecedores ativos da secretaria

## Estória

Como **servidor da CRE que responde pelo cadastro de fornecedores da sua secretaria**, quero
**procurar os fornecedores ativos e escolher um deles para ver a ficha completa**, para que **eu
chegue ao fornecedor certo pelo nome ou pelo CNPJ, sem ter de decorar o código dele**.

Esta tela existe porque o cadastro do fornecedor é grande: o servidor reconhece o fornecedor pelo
nome, não pelo número. A tela lista os fornecedores ativos da secretaria, cada um com o código, o
nome, o CNPJ e a marca de situação, e deixa escolher um deles para abrir a ficha. Sem esta lista, a
conferência do cadastro vira tentativa por código, e quem não decora o número não chega à ficha.
Nada aqui é gravado: a ficha é mantida na tela que esta abre.

## Contexto

Jornada S000M → C000M → C015M → C030C.

Ator: servidor de CRE — procura o fornecedor ativo dentro do conjunto da sua secretaria e escolhe
um deles para abrir a ficha completa em consulta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio. Os dois menus do caminho não gravam nada: só encaminham.

A tela recebe da sessão a **secretaria (o tipo de órgão)**, a **coordenação regional escolar**, a
**matrícula**, o **código de acesso**, o **privilégio** e a **estação**; o **órgão filho do
servidor**, que a entrada também carrega, **não** limita esta tela — o alcance aqui é a ficha do
fornecedor, que não pertence a órgão. A data do sistema e o nome da secretaria que ela exibe também
vêm da sessão. Essa carga é regra da entrada e está no anexo, em **Regras que se revelaram da
entrada**.

O que esta tela faz é uma passagem: ela lista os fornecedores e, escolhido um, **passa o registro e
a operação para a tela de cadastro do fornecedor, que abre em consulta** (RN-08). É por isso que a
jornada termina aqui — quem mostra a ficha é a tela seguinte, e a tela desta jornada é o índice
dela.

## Regras de negócio

### RN-01 — A tela consulta os fornecedores ativos da secretaria da sessão

Esta é uma tela de **consulta**. Ela lista os fornecedores **ativos** do cadastro de fornecedores e,
de cada um, mostra **quatro dados**: o **código do fornecedor**, a **marca de situação**, o **nome
do fornecedor** e o **CNPJ**. No alto ela mostra o **nome da secretaria** e a **data do sistema**.

O conjunto é o da secretaria da sessão — não há filtro de órgão na tela, e o cadastro de fornecedor
não tem dono por unidade. Nada nesta tela é gravado: nem cadastro, nem travamento de registro, nem
linha de auditoria. A tela também não aceita inclusão, alteração nem exclusão: o único uso é achar
o fornecedor e abrir a ficha dele.

### RN-02 — A lista é ordenada pelo nome do fornecedor e cabe em treze posições

A lista é lida na ordem do **nome do fornecedor**, e não do código. Por isso a busca começa pelo
nome: o que se digita como ponto de partida é procurado dentro dessa ordem.

A tela trabalha com **treze posições** de fornecedor. O programa lê uma posição de cada vez e avança
na ordem até a última posição da página; a capacidade declarada do cadastro é de **dez mil**
fornecedores, muito maior que a página.

Da leitura saem apenas as fichas **ativas**: a ficha marcada como logicamente excluída é saltada e a
leitura segue para a próxima, sem aviso. A tela também **não** relaciona por CNPJ nem oferece
página seguinte.

### RN-03 — A consulta aceita um ponto de partida, e ele é o próprio código do fornecedor

Em branco o campo do código, a lista começa **no começo** do cadastro e mostra os primeiros
fornecedores na ordem do nome. Preenchido, a lista **começa naquele fornecedor** e segue a partir
dele.

O mesmo campo serve para as duas coisas: é o **ponto de partida** da leitura enquanto o servidor
ainda não escolheu ninguém, e passa a ser o **fornecedor escolhido** quando ele confirma. Não há
segundo campo para dizer onde a lista começa.

[?] O campo do código é o mesmo nas duas funções, e com um código que não corresponde a nenhum
fornecedor ativo a lista parece avançar até o fornecedor seguinte na ordem do nome: ou o código
funciona como posição na ordem alfabética dos nomes, ou o ponto de partida só vale quando existe
ficha ativa naquele código. A condição que a tela usa para decidir isso não fecha no material lido —
os dois lados apontam para o mesmo rótulo e o mesmo destino, e não há mensagem de recusa para esse
caso. Pergunta ao site.

### RN-04 — Marcado o fornecedor, a ficha dele se abre em consulta

Marcado o fornecedor, a tela **não** segue com uma operação própria: ela passa o **código do
fornecedor escolhido** e a **operação de consulta** para a tela de cadastro do fornecedor, que abre
**em consulta** sobre ele. Nada é gravado por esta tela nessa passagem.

A passagem exige as duas marcas: o **código do fornecedor preenchido** e o **indicador de seleção da
linha** com o valor que o dispara. Sem fornecedor marcado, ou com o indicador em branco, a tela
apenas segue mostrando a lista, recolhe o nome do último fornecedor exibido como ponto de partida da
leitura seguinte e não abre nada.

### RN-05 — A consulta exige permissão de operação, e a permissão lida é a de alteração

A tela monta a operação de **consulta** e a submete à conferência de permissão do código de acesso
do servidor. Sem o registro de autorização daquela tela para aquele código de acesso, a tela não
opera.

[?] Na conferência de permissão, a operação de consulta cai no ramo que confere a permissão de
**alteração**, e não a de consulta — o cadastro de telas guarda as quatro permissões separadas
(consulta, inclusão, alteração e exclusão), e a permissão de consulta não é lida em nenhum ponto da
rotina. Ou uma tela de consulta exige mesmo a permissão de alteração, ou a conferência está lendo a
permissão errada. É o mesmo defeito já registrado na C020C. Pergunta ao site.

### RN-06 — Fornecedor excluído ou fora do alcance da leitura não aparece na lista

A tela só conta como **achado** o fornecedor **ativo**. A ficha marcada como logicamente excluída é
saltada — o conteúdo exibido é limpo e a leitura segue para a próxima —, e o fornecedor que a
consulta do ponto de partida não encontrar também não é exibido: quando o código informado não
existe naquele ramo do cadastro, a tela simplesmente não mostra ficha nenhuma naquele ponto e
continua a leitura.

[?] A leitura que trata a inexistência do ponto de partida tem uma rotina que limpa a exibição e
volta para trás, e essa limpeza parece **inalcançável**: a guarda imediatamente anterior barra
exatamente a combinação em que a limpeza seria executada. Sem ela, o nome exibido pode ficar
repetido de uma consulta para a seguinte. Ou a limpeza vale para outra leitura, ou o caminho ficou
sem efeito. Pergunta ao site.

### RN-07 — Sem fornecedor ativo, a tela avisa que não há fornecedores cadastrados

Quando a **primeira posição** da lista não traz nenhum fornecedor, a tela avisa
**\* Nao existem fornecedores cadastrados \*** e não lista nada. O aviso é o do topo da lista: ele
não se repete a cada posição vazia, e sim uma vez, na montagem da primeira posição.

A mesma posição serve para dizer onde a leitura começa e para dizer que ela não achou nada: quando o
aviso sai, o conteúdo exibido é limpo.

### RN-08 — O código do fornecedor é conferido antes de qualquer uso

O código do fornecedor informado passa por uma conferência de número **antes** de qualquer uso: o
que não for número é recusado no próprio campo, com o cursor de volta nele, e nada é listado por
causa disso. O código em branco é tratado como zero, isto é, a lista começa no começo.

### RN-09 — Falha de leitura ou registro travado interrompe a consulta e avisa

Toda leitura desta tela testa o erro do banco. Erro de leitura que não seja "não achado" vira a ação
de erro de acesso, com a mensagem de erro do sistema, e a operação para ali, sem completar a lista.
O **registro travado** por outra pessoa, quando aparece na leitura, cai na mesma interrupção: o
fornecedor simplesmente não é mostrado.

### RN-10 — A tela não grava, não exclui e não trava registro

Nenhuma das operações de gravação, exclusão ou travamento que o programa carrega é executada por
esta tela. As declarações existem para todos os cadastros que ela enxerga — é assim que o gerador
monta o programa —, mas a tela não as aciona: a única execução é a de **consulta**. O travamento de
registro aparece apenas dentro dos caminhos de exclusão, que a tela não percorre.

### RN-11 — O que a tela entrega à seguinte depende de quem a chamou

A tela de cadastro do fornecedor **abre em consulta** por causa desta tela: a operação passada é a de
consulta e a tela de origem fica registrada na área de trabalho da sessão. Quando o cadastro do
fornecedor é aberto pela **opção 4 do mesmo menu**, ele abre pedindo o cadastro, não a consulta.

A tela desta jornada deixa ainda o **fornecedor escolhido** na área de trabalho da sessão e o
**indicador de continuação** ligado, o que faz a tela seguinte voltar para cá com o resultado da
consulta. Sem esse indicador, a tela seguinte não devolve o controle e o servidor não volta à lista.

[?] A tela de cadastro do fornecedor também é aberta **pelo menu, na opção 4**, sem passar por aqui:
nesse caso não há fornecedor escolhido nem indicador de continuação, e o material lido não mostra
como ela se comporta — se abre em inclusão, se exige que o servidor informe o código, ou se recusa.
Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consultar os fornecedores ativos da secretaria e abrir a ficha do fornecedor escolhido

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C030C

  Cenário: RN-01 — consultar os fornecedores ativos da secretaria
    Quando confirmo a consulta
    Então vejo o nome da secretaria e a data do sistema
    E vejo, de cada fornecedor ativo, o código, a marca de situação, o nome e o CNPJ
    E nada é gravado

  Cenário: RN-01 — consultar não deixa rastro
    Dado que faço uma consulta
    Quando a consulta termina
    Então nenhum registro é travado
    E nenhuma linha nova aparece na trilha de auditoria

  Cenário: RN-02 — fornecedor excluído não entra na lista
    Dado que existe um fornecedor marcado como logicamente excluído
    Quando confirmo a consulta
    Então esse fornecedor não aparece na lista
    E os fornecedores ativos continuam sendo mostrados

  Cenário: RN-03 — começar a lista por um fornecedor escolhido
    Dado que informo o código de um fornecedor ativo como ponto de partida
    Quando confirmo a consulta
    Então a lista começa naquele fornecedor
    E segue mostrando os fornecedores ativos seguintes

  Cenário: RN-03 — consulta sem ponto de partida
    Dado que deixo o código do fornecedor em branco
    Quando confirmo a consulta
    Então a lista começa no começo do cadastro
    E mostra os primeiros fornecedores ativos, na ordem do nome

  Cenário: RN-04 — marcar um fornecedor e abrir a ficha dele
    Dado que a lista mostra os fornecedores ativos
    E marco o indicador de seleção de um fornecedor
    Quando confirmo
    Então a ficha daquele fornecedor se abre em consulta
    E nada é gravado por esta tela

  Cenário: RN-04 — a lista sem fornecedor marcado não abre ficha
    Dado que a lista mostra os fornecedores ativos
    Quando confirmo sem marcar nenhum fornecedor
    Então a tela segue mostrando a lista
    E nenhuma ficha se abre

  Cenário: RN-05 — sem autorização para a tela
    Dado que não tenho o registro de autorização desta tela para o meu código de acesso
    Quando confirmo a consulta
    Então a tela não opera
    E nada é listado

  Cenário: RN-06 — fornecedor excluído procurado pelo código
    Dado que informo o código de um fornecedor marcado como excluído
    Quando confirmo a consulta
    Então esse fornecedor não é exibido
    E a leitura segue para o fornecedor seguinte

  Cenário: RN-07 — nenhum fornecedor ativo
    Quando confirmo a consulta e não há fornecedor ativo
    Então vejo "* Nao existem fornecedores cadastrados *"
    E nenhum fornecedor é listado

  Cenário: RN-08 — código com texto
    Quando informo texto no código do fornecedor
    Então o campo é recusado antes de qualquer uso
    E o cursor volta para o campo
    E nada é listado

  Cenário: RN-09 — falha do banco durante a consulta
    Dado que a leitura do cadastro falha no banco
    Quando confirmo a consulta
    Então a operação é interrompida com a mensagem de erro do sistema
    E a lista não é completada

  Cenário: RN-09 — registro travado por outra pessoa
    Dado que o fornecedor procurado está travado por outra pessoa
    Quando confirmo a consulta
    Então esse fornecedor não é mostrado
    E a operação para com o aviso do sistema

  Cenário: RN-11 — a ficha aberta a partir da lista
    Dado que escolho um fornecedor na lista
    Quando confirmo
    Então a tela de cadastro do fornecedor abre em consulta sobre ele
    E ela volta para esta lista com o resultado da consulta

  Cenário: RN-11 — a ficha aberta pelo menu
    Dado que abro o cadastro do fornecedor pela opção do menu, sem passar pela lista
    Quando confirmo
    Então a tela de cadastro não abre em consulta sobre um fornecedor escolhido
```
