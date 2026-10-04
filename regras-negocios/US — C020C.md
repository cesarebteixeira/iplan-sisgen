# US — C020C — Consultar unidades da coordenadoria regional escolar

## Estória

Como **servidor de CRE que responde pelas unidades da sua coordenadoria regional escolar**, quero
**consultar a relação das unidades da minha coordenadoria, escolhendo o ponto de partida da
relação, e abrir o cadastro completo da unidade que eu marcar**, para que **eu encontre a unidade
certa pelo código, pelo nome, pelo contato e pelo telefone, e chegue ao cadastro dela sem digitar
o código de memória**.

Esta tela existe porque o cadastro da unidade é grande demais para se abrir sabendo só o código:
o servidor conhece a escola pelo nome e pelo contato, não pelo número. A relação mostra, de cada
unidade da coordenadoria, o código, o nome, o nome da pessoa de contato e o telefone; marcada a
unidade, o cadastro dela se abre em consulta. Quem depende disto é a conferência do dia a dia da
coordenadoria: sem esta relação, achar a unidade passa a ser tentativa por código, e o servidor
que não decora o número do órgão não chega ao cadastro. Nada aqui é gravado — o cadastro é
mantido na tela que esta abre.

## Contexto

Jornada S000M → C000M → C200M → C020C.

Ator: servidor de CRE — consulta a relação das unidades da sua coordenadoria regional escolar e
escolhe uma delas para abrir o cadastro completo em consulta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**,
não regra de negócio. Os dois menus do caminho não gravam nada: só encaminham.

A tela recebe da sessão a **secretaria (o tipo de órgão)**, a **coordenação regional escolar da
sessão (o grupo)** e o **código de acesso**; essa é regra da entrada e está no anexo de
evidências, em **Regras que se revelaram da entrada**. O **órgão filho do servidor**, que a
entrada também carrega, **não** limita esta tela: aqui o alcance é a secretaria e o grupo.

O que esta tela faz é uma passagem: ela mostra a relação das unidades do grupo e, marcada uma
unidade, **passa o registro e a operação para a tela de cadastro da unidade, que abre em
consulta** (RN-05). É por isso que a jornada termina aqui — a tela de destino é um encaminhamento,
e quem mostra o cadastro é a tela seguinte.

## Regras de negócio

### RN-01 — A tela consulta a relação das unidades da coordenadoria regional escolar

Esta é uma tela de **consulta**. Ela mostra a relação das unidades de uma **coordenação regional
escolar** — o grupo —, cada uma com o **código da unidade**, o **nome da unidade**, o **nome da
pessoa de contato** e o **telefone**, e mostra também o **nome da coordenação**, o **nome da
secretaria** e a **data do sistema**. Nada nesta tela é gravado: nem cadastro, nem travamento de
registro, nem linha de auditoria.

O grupo é o filtro da relação: só aparecem as unidades daquele grupo. A tela também aceita um
**ponto de partida** — o código da unidade por onde a relação começa —, que é o que permite abrir
a relação já na altura desejada em vez de sempre no começo.

### RN-02 — O grupo vem da sessão quando o servidor não o informa

Quando o servidor não informa a coordenação regional escolar, a tela adota a **coordenação da
sessão**, que veio do vínculo da matrícula com a secretaria. Quando o servidor **tem** coordenação
na sessão e informa **outra**, a tela recusa com **\* Usuario sem acesso a este grupo \*** e nada
é consultado.

### RN-03 — O grupo informado tem de estar cadastrado na secretaria da sessão

A coordenação regional escolar informada é procurada no cadastro de grupos **da secretaria da
sessão**. Quando ela não existe nesse cadastro, ou está marcada como excluída, a tela recusa com
**\* Grupo nao cadastrado \*** e nenhuma unidade é relacionada.

### RN-04 — Sem grupo informado por quem não tem grupo, a consulta para

Quando o servidor **não tem** coordenação regional escolar na sessão e também não informa
nenhuma, a tela recusa com **\* Informe o grupo \*** e o cursor volta para o campo da coordenação.
Sem esse campo não há como saber de que conjunto de unidades se trata.

### RN-05 — Marcada uma unidade, o cadastro dela se abre em consulta

Marcada uma unidade da relação, a tela **não** segue com uma operação própria: ela passa o
**registro da unidade escolhida** e a **operação de consulta** para a tela de cadastro da unidade,
que abre **em consulta** sobre essa unidade. É essa passagem que dá sentido à tela — a relação é o
índice, o cadastro é o conteúdo —, e é por ela que a jornada termina na tela de cadastro.

A passagem só acontece nessa combinação: **unidade marcada** e **indicador de seleção da linha
marcado**. Sem unidade marcada, a tela apenas segue mostrando a relação; com a unidade marcada e
o indicador em branco, a tela também apenas segue, sem abrir nada.

[?] O campo que marca a linha selecionada é lido e exibido, mas o corpus não traz o rótulo que o
servidor vê nem o valor que ele digita: a tela não tem conferência de valor para esse campo, não
tem mensagem própria para ele, e o material lido só mostra o literal que dispara a passagem.
Pergunta ao site.

### RN-06 — A tela recusa a operação quando uma tela anterior está por terminar

Quando o controle da tela anterior está preenchido, a tela **não** segue com a consulta: ela
devolve o controle e nada é mostrado nem gravado. É a guarda que impede a relação de se abrir por
cima de outra tela que ainda está no meio de uma operação.

[?] A guarda é a primeira da tela, antes de qualquer conferência de grupo, e o corpus não diz o
que preenche o controle da tela anterior nem o que o servidor vê quando isso acontece. Ou ele é
uma tela em fim de operação, ou é um caminho que não deveria existir. Pergunta ao site.

### RN-07 — Sem unidade ativa no grupo, a tela avisa que não há órgãos cadastrados

Quando o grupo existe mas **nenhuma unidade ativa** aparece na relação, a tela avisa
**\* Nao existem orgaos cadastrados \*** e não relaciona nada. Unidade inativa não entra na
relação.

### RN-08 — O código da coordenação, o da unidade marcada e o inicial são conferidos antes de tudo

Os três códigos que o servidor digita nesta tela — a **coordenação regional escolar**, o **código
da unidade marcada** e o **código inicial da relação** — passam por uma conferência de número
**antes** de qualquer consulta ao cadastro: o que não for número é recusado no próprio campo, com
o cursor de volta nele, e nada é consultado por causa disso. O código inicial em branco é tratado
como zero, isto é, a relação começa no começo do grupo.

### RN-09 — A consulta exige permissão de operação, e a operação consultada é a de consulta

A tela monta a operação de **consulta** e a submete à conferência de permissão do código de acesso
do servidor. Sem o registro de autorização daquela tela para aquele código de acesso, a tela não
opera.

[?] Na conferência de permissão, a operação de consulta cai no ramo que confere a permissão de
**alteração**, e não a de consulta — o cadastro de telas guarda as quatro permissões separadas
(consulta, inclusão, alteração e exclusão). Ou uma tela de consulta exige mesmo a permissão de
alteração, ou a conferência está lendo a permissão errada. Pergunta ao site.

### RN-10 — Falha do banco interrompe a consulta e avisa

Toda leitura desta tela testa o erro do banco. Erro de leitura vira a ação de erro de acesso,
com a mensagem de erro do sistema, e a operação para ali, sem completar a relação.

## Cenários BDD

```gherkin
Funcionalidade: Consultar a relação das unidades da coordenadoria regional escolar e abrir o cadastro da unidade escolhida

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C020C

  Cenário: RN-01 — consultar a relação das unidades do grupo
    Dado que informo a coordenação regional escolar
    Quando confirmo a consulta
    Então vejo o nome da coordenação, o nome da secretaria e a data do sistema
    E vejo o código, o nome, o contato e o telefone de cada unidade do grupo
    E nada é gravado

  Cenário: RN-01 — escolher o ponto de partida da relação
    Dado que informo o código de uma unidade do grupo como ponto de partida
    Quando confirmo a consulta
    Então a relação começa naquela unidade

  Cenário: RN-01 — consultar não deixa rastro
    Dado que faço uma consulta
    Quando a consulta termina
    Então nenhum registro é travado
    E nenhuma linha nova aparece na trilha de auditoria

  Cenário: RN-02 — grupo não informado por quem tem grupo
    Dado que tenho coordenação regional escolar na sessão
    Quando confirmo a consulta sem informar a coordenação
    Então a coordenação da minha sessão é adotada
    E vejo as unidades dela

  Cenário: RN-02 — coordenação informada diferente da minha
    Dado que tenho coordenação regional escolar na sessão
    Quando informo uma coordenação que não é a minha
    Então vejo "* Usuario sem acesso a este grupo *"
    E nada é consultado

  Cenário: RN-03 — coordenação não cadastrada
    Dado que informo uma coordenação que não existe para a minha secretaria
    Quando confirmo a consulta
    Então vejo "* Grupo nao cadastrado *"
    E nenhuma unidade é relacionada

  Cenário: RN-03 — coordenação marcada como excluída
    Dado que informo uma coordenação marcada como excluída
    Quando confirmo a consulta
    Então vejo "* Grupo nao cadastrado *"
    E nenhuma unidade é relacionada

  Cenário: RN-04 — grupo em branco por quem não tem grupo
    Dado que o meu usuário não tem coordenação regional escolar
    Quando confirmo a consulta sem informar a coordenação
    Então vejo "* Informe o grupo *"
    E o cursor volta para o campo da coordenação
    E nada é consultado

  Cenário: RN-05 — marcar uma unidade e abrir o cadastro dela
    Dado que a relação mostra as unidades do meu grupo
    E marco o indicador de seleção de uma unidade
    Quando confirmo
    Então o cadastro daquela unidade se abre em consulta
    E nada é gravado por esta tela

  Cenário: RN-05 — a relação sem unidade marcada não abre cadastro
    Dado que a relação mostra as unidades do meu grupo
    Quando confirmo sem marcar nenhuma unidade
    Então a tela segue mostrando a relação
    E nenhum cadastro se abre

  Cenário: RN-06 — controle da tela anterior preenchido
    Dado que o controle da tela anterior está preenchido
    Quando confirmo
    Então a tela não segue com a consulta
    E nada é mostrado nem gravado

  Cenário: RN-07 — grupo sem unidade ativa
    Dado que informo uma coordenação cadastrada que não tem unidade ativa
    Quando confirmo a consulta
    Então vejo "* Nao existem orgaos cadastrados *"
    E nenhuma unidade é relacionada

  Cenário: RN-08 — código com texto
    Quando informo texto em um dos códigos desta tela
    Então o campo é recusado antes de qualquer consulta ao cadastro
    E o cursor volta para o campo
    E nada é consultado

  Cenário: RN-09 — sem autorização para a tela
    Dado que não tenho o registro de autorização desta tela para o meu código de acesso
    Quando confirmo a consulta
    Então a tela não opera
    E nada é consultado

  Cenário: RN-10 — falha do banco durante a consulta
    Dado que a leitura do cadastro falha no banco
    Quando confirmo a consulta
    Então a operação é interrompida com a mensagem de erro do sistema
    E a relação não é completada
```
