# US — N016T — Manter processo de prestação de contas

## Estória

Como **servidor da Coordenadoria Regional de Ensino que trabalha com a prestação de
contas**, quero **reunir, conferir e manter o processo que agrupa as notas fiscais,
o contrato e os empenhos da minha secretaria**, para que **as notas saibam a que
processo pertencem e o processo possa seguir para o lançamento e a impressão sem
que alguém redigite o que a secretaria já formalizou**.

O processo é a pasta que amarra vários documentos: sem a identificação dele não há
como dizer de que prestação de contas uma nota faz parte, nem separar o que já foi
liquidado do que ainda corre. A tela em si não lança nota: ela reúne o processo,
confere se ele existe e se o servidor pode mexer nele, e entrega a pasta pronta à
tela seguinte, que é onde o conteúdo é digitado. Se o processo não estiver
formalizado, a tela recusa qualquer operação — inclusive a simples leitura —, e o
trabalho para.

## Contexto

Jornada S000M → N000M → N050M → N016T.
Ator: servidor de CRE — escolhe o processo de prestação de contas da sua
coordenadoria, confere o que ele já reúne e decide sobre a inclusão, a alteração, a
exclusão ou a consulta do processo.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US —
00 Entrada (LOGON, S000M).md`. O caminho até a tela é dado de navegação e está em
`Documents/jornadas/00 Navegação e menus.md`.

Os dois passos anteriores (`N000M` e `N050M`) são menus e não gravam nada: eles
apenas repassam o contexto que a entrada deixou — a matrícula do servidor, a
secretaria e o órgão da sessão, a coordenadoria regional escolar e o privilégio —
e é desse contexto que esta tela tira o órgão com que lê os cadastros, a
coordenadoria com que confere a permissão e a matrícula que assina o pedido de
impressão. Nesta tela a secretaria é um **código próprio da prestação de contas**,
e não a secretaria escolhida na entrada: o valor vem do cadastro do órgão da sessão
e é ele que limita a lista de códigos aceitos.

Esta tela não é o fim da jornada: confirmada a operação, ela mesma abre a tela
seguinte e entrega o processo e a operação, sem passar por menu nenhum.

## Regras de negócio

### RN-01 — A tela trabalha com um único processo por vez, identificado por três códigos

O processo de prestação de contas é identificado por três informações que o
servidor digita:

- o **código da secretaria** — o código interno da prestação de contas, de dois
  dígitos;
- o **código do lote** — o número do lote do processo dentro da secretaria, de seis
  dígitos;
- o **número do processo** — o número central, de quatro dígitos.

Essas três partes formam, junto com mais dois dígitos de controle que a própria
tela preenche, o número de processo de catorze dígitos que dá nome ao processo em
todo o sistema. É esse número que a tela lê, grava e entrega adiante — e é por ele
que as notas fiscais referenciam o processo. O lote e o número do processo são
obrigatórios: se um deles chega vazio, a tela recusa com **\* Numero do processo
invalido \***.

### RN-02 — A tela abre em branco na inclusão e separa as três operações de consulta

Ao abrir, a tela decide entre quatro caminhos: inclusão, alteração, exclusão e
consulta. Quem abre a tela pelo menu entra em **inclusão**, com os campos de
processo em branco e o código da secretaria já preenchido com o do cadastro do
órgão da sessão; vindo da tela seguinte, a tela respeita a operação que aquela
tela deixou. Qualquer outra operação é recusada com **\* Opcao nao disponivel. Use
INC, ALT, EXC ou CON \***.

Uma **consulta** não grava nada: ela apenas lê o processo e o mostra na tela. A
**alteração** e a **exclusão** não gravam no primeiro envio: elas exibem a
pergunta de confirmação e só gravam depois que o servidor responde **S**; se ele
responde qualquer outra coisa, a tela volta ao estado inicial — operação em
inclusão, campos limpos — e nada mudou. Retirado o código de impressão, a
alteração gravada é descartada da mesma forma.

### RN-03 — O código da secretaria tem de estar entre os seis do órgão da sessão

A tela não aceita qualquer código de secretaria: ela lê o cadastro do órgão da
sessão e compara o código digitado com o código principal e com mais cinco códigos
alternativos que esse mesmo cadastro guarda. Se o código não estiver entre os seis,
a recusa é **\* Inicio do processo invalido \*** e a tela não segue. Quando o
cadastro do órgão manda o processo ser numerado pela coordenadoria regional, a
coordenadoria da sessão entra no lugar do código de lote.

### RN-04 — A coordenadoria regional escolar tem de existir, e o servidor só mexe no que é dela

A coordenadoria regional escolar digitada é conferida contra o cadastro de
coordenadorias. Não existindo, a recusa é **\* Grupo nao cadastrado \***.

Quando a sessão tem uma coordenadoria fixa, a tela exige que o processo seja
**dessa** coordenadoria; a recusa é **\* Usuario sem acesso a este grupo \***.
Quando a sessão não tem coordenadoria fixa, a tela exige que uma seja informada —
**\* Informe o grupo \*** — e confere, no cadastro do processo, que o grupo dele é
o mesmo; sendo outro, a recusa é **\* Usuario sem acesso ao grupo deste processo
\***. Essa conferência vale inclusive na consulta: sem ela o servidor de uma
coordenadoria não vê o processo de outra.

### RN-05 — O tipo de contrato tem de existir e o fornecedor tem de existir

O tipo de contrato digitado é conferido contra o cadastro de tipos de contrato.
Não existindo, ou estando o cadastro marcado para exclusão, a recusa é **\* Tipo de
contrato nao cadastrado \***. O fornecedor digitado é conferido contra o cadastro
de fornecedores; não existindo, ou estando marcado para exclusão, a recusa é
**\* Fornecedor nao cadastrado \***.

### RN-06 — A fonte de recursos tem de existir e ter código a partir de 1000

O código da fonte de recursos digitado é conferido contra o cadastro de fontes.
Código menor que 1000 é recusado de saída, com **\* Fonte invalida \***; código
válido que não exista no cadastro, ou que esteja marcado para exclusão, é recusado
com **\* Fonte nao cadastrada \***.

### RN-07 — O tipo de processo é conferido quando informado, e vem do processo quando não é

O tipo de processo digitado é conferido contra o cadastro de tipos de processo; não
existindo, a recusa é **\* Tipo processo nao cadastrado \***. Quando o servidor não
informa o tipo, a tela adota o que o processo já tem registrado — e, se o processo
ainda não tiver nenhum, deixa o campo em branco.

### RN-08 — O processo tem de existir; a tela não cria processo

Com as conferências anteriores passadas, a tela lê o processo pelo número de catorze
dígitos. Se ele não existir, a recusa é **\* Processo nao cadastrado \*** e a tela
para — em qualquer das operações, inclusive na consulta. É por isso que a tela não
é porta de entrada de processo: ela pressupõe que o processo já foi formalizado
antes, e cuida de conferi-lo e de encaminhá-lo.

### RN-09 — Estar com o processo já cadastrado não impede a alteração

Se o processo existe e a operação é **alteração**, a tela segue normalmente: é
exatamente o caso de alterar o que já está cadastrado. Mas, se o processo não
existe e a operação é **inclusão**, a recusa é **\* Processo ja cadastrado. Use ALT.
\***. Para a **exclusão** e para a **consulta**, basta o processo existir.

[?] A recusa **\* Processo ja cadastrado. Use ALT. \*** não diz o que ela quer
dizer quando o processo acaba de ser dado como não cadastrado, e a comparação que
decide por ela depende de um número que a tela reconstrói de várias fontes. Não
ficou claro, pelo fonte, em que situação real o servidor vê essa mensagem. Pergunta
ao site.

### RN-10 — Só se exclui processo ainda não lançado

Para excluir, a tela exige que o processo ainda não tenha sido lançado: quando o
processo já foi lançado, a recusa é **\* Processo nao pode ser excluido \***. A
alteração, ao contrário, exige o oposto — que o processo **já esteja lançado** — e
recusa o que ainda não foi lançado com **\* Processo nao pode ser alterado \***.

[?] As duas exigências são opostas e saem da mesma situação lida do processo. Ou a
exclusão vale para um caso que não é o da alteração, ou uma das duas operações é
inalcançável. Pergunta ao site.

### RN-11 — Processo integrado com o SIAFIC não se altera nem se exclui

Existem processos que já estão em integração com o SIAFIC. Em qualquer um deles, a
alteração e a exclusão são recusadas com **\* Processo na integracao com SIAFIC \***.
A consulta continua liberada.

### RN-12 — A nova fonte não retroage a exercício anterior

Ao trocar a fonte de recursos do processo, a tela confere o exercício do processo:
processos de exercícios anteriores a 2004 mantêm a fonte antiga; para os mais
recentes, a tela compara a fonte digitada com a que o processo já tem e, sendo
outra, recusa com **\* Fonte invalida \*** quando o novo código não alcança o
cadastro. Trocada a fonte, o processo passa a apontar para a fonte nova e os
lançamentos ligados a ele são atualizados.

### RN-13 — A tela mostra o que o processo já reúne: quantidade de notas e três totais

Depois de conferir o processo, a tela percorre os lançamentos ligados a ele e mostra
na própria tela três números: a **quantidade de notas** do processo e os **valores
totais** lançados, em três naturezas. É essa soma que o servidor confere antes de
decidir — e ela é recalculada a cada leitura, não é digitada.

### RN-14 — A tela mostra a situação de cada nota do processo

Além dos totais, a tela mostra, para cada nota ligada ao processo, a situação do
processo correspondente — **fechado**, **pré-liquidado**, **liquidado** ou
**pago** —, tirada do andamento do lançamento. Na entrada em branco, sem lançamento
nenhum, a situação mostrada é **fechado**.

### RN-15 — Processo lançado tem de ser lido antes, e a tela lança os números das notas

Quando o servidor confirma uma alteração ou uma consulta de um processo que tem nota
lançada, a tela faz duas coisas antes de mostrar o resultado. Primeiro, relê o
processo lançado para checar se ele mudou no meio do caminho — se os dados que o
servidor tinha na tela não são mais os do processo, a tela descarta aquele envio e
volta ao começo, sem gravar. Depois, percorre os lançamentos do processo até o
último número de lançamento, abrindo um **novo número de lançamento** para cada
nota que entra no processo.

[?] Essa abertura de número de lançamento é gravada na base, mas a tela não mostra
ao servidor quantos números abriu nem por quê; a contagem exata de lançamentos
criados não fecha com o número de notas do processo. Pergunta ao site.

### RN-16 — O servidor que pede a impressão precisa de e-mail e do número de vias

Pedida a impressão a partir da tela (o campo do código de impressão preenchido), a
tela exige que o processo já tenha **SEI associado** — recusa **\* SEI ainda nao
associado ao processo \*** —, que o **servidor tenha e-mail cadastrado** — recusa
**\* Usuario sem e-mail cadastrado \*** — e que o **número de vias** tenha sido
informado — recusa **\* Informe o numero de vias \***. Por fim, se já existe uma
requisição de impressão da mesma natureza em processamento, a recusa é
**\* Relatorio em processamento. Aguarde. \***. Passando por tudo, a tela cria o
pedido de impressão com o número de vias, o e-mail do servidor, a matrícula, o
órgão e o processo.

### RN-17 — A exclusão desfaz o lançamento do processo e devolve o que ele consumiu

Confirmada a exclusão de um processo, a tela percorre cada nota ligada a ele e, para
cada uma: apaga os itens da nota, apaga o lançamento da nota, faz o lançamento sair
dos empenhos e devolve ao contrato a quantidade e o valor que aquela nota havia
consumido; a nota em si volta à condição de nota sem processo, e o processo é
apagado. É uma volta completa: nada do que o processo reuniu fica para trás.

### RN-18 — Deixar o processo fechado é o desfecho de toda operação confirmada

Terminada a operação — inclusão, alteração, exclusão ou consulta —, a tela devolve
o processo com a situação **fechado** e entrega o número do processo e a operação
para a tela seguinte, que é onde as notas são lançadas. Se, em vez disso, a tela
estiver sendo apenas reaberta pela tela seguinte, ela se apresenta como origem e
não mexe em nada.

### RN-19 — Toda operação confirmada fica registrada

Toda operação confirmada — inclusão, alteração, exclusão e também a leitura da
consulta — deixa um registro de auditoria com o processo, a matrícula, a estação, a
data, a hora, o órgão e a operação, além do valor antes e do valor depois do
registro tocado. É esse rastro que permite reconstruir quem mexeu em quê.

[?] A auditoria da inclusão está sob uma conferência de situação que vem do
ambiente de execução, e não do programa da tela. Não foi possível concluir, pelo
fonte, se essa conferência deixa ou barra o registro. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Processo de prestação de contas — identificação, conferência e manutenção

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N016T

  Cenário: A tela abre em branco para incluir
    Dado que abri a tela pela opção de menu
    Então a tela abre em inclusão, com o código da secretaria do meu órgão preenchido
    E os campos de lote e de número do processo em branco
    E o processo mostrado está fechado, sem quantidade de notas e sem totais

  Cenário: Recusa quando o lote ou o número do processo fica vazio
    Dado que escolhi incluir
    Quando deixo o lote ou o número do processo em branco e envio
    Então vejo * Numero do processo invalido *
    E nada é gravado

  Cenário: Recusa uma operação que não é inclusão, alteração, exclusão nem consulta
    Dado que enviei a tela com uma operação diferente das quatro
    Então vejo * Opcao nao disponivel. Use INC, ALT, EXC ou CON *
    E nada é gravado

  Cenário: Recusa código de secretaria que não é um dos seis do meu órgão
    Quando informo um código de secretaria que não está entre os seis do cadastro do meu órgão e envio
    Então vejo * Inicio do processo invalido *
    E nada é gravado

  Cenário: Recusa coordenadoria regional escolar que não existe
    Quando informo uma coordenadoria regional escolar que não está cadastrada e envio
    Então vejo * Grupo nao cadastrado *
    E nada é gravado

  Cenário: Recusa processo de coordenadoria que não é a minha
    Dado que a minha sessão está presa a uma coordenadoria regional escolar
    Quando abro um processo de outra coordenadoria e envio
    Então vejo * Usuario sem acesso a este grupo *
    E nada é gravado

  Cenário: Recusa quando eu não tenho coordenadoria e não informo nenhuma
    Dado que a minha sessão não está presa a uma coordenadoria regional escolar
    Quando deixo a coordenadoria em branco e envio
    Então vejo * Informe o grupo *
    E nada é gravado

  Cenário: Recusa tipo de contrato que não existe
    Quando informo um tipo de contrato que não está cadastrado e envio
    Então vejo * Tipo de contrato nao cadastrado *
    E nada é gravado

  Cenário: Recusa fornecedor que não existe
    Quando informo um fornecedor que não está cadastrado e envio
    Então vejo * Fornecedor nao cadastrado *
    E nada é gravado

  Cenário: Recusa código de fonte abaixo de 1000
    Quando informo um código de fonte menor que 1000 e envio
    Então vejo * Fonte invalida *
    E nada é gravado

  Cenário: Recusa fonte que não existe, e recusa tipo de processo que não existe
    Quando informo uma fonte válida que não está no cadastro e envio
    Então vejo * Fonte nao cadastrada *
    Quando informo um tipo de processo que não está cadastrado e envio
    Então vejo * Tipo processo nao cadastrado *
    E nada é gravado

  Cenário: Recusa consultar, alterar ou excluir processo que não existe
    Quando informo um processo que não está cadastrado e envio, em consulta, alteração ou exclusão
    Então vejo * Processo nao cadastrado *
    E nada é gravado

  Cenário: Recusa incluir processo que já está cadastrado
    Dado que o processo que informei já está cadastrado
    Quando escolho incluir e envio
    Então vejo * Processo ja cadastrado. Use ALT. *
    E nada é gravado

  Cenário: A consulta mostra o processo e não grava nada
    Dado que o processo existe e é da minha coordenadoria
    Quando escolho consultar e envio
    Então a tela mostra o processo, a quantidade de notas e os três valores totais
    E mostra a situação de cada nota do processo
    E nada é gravado

  Cenário: A alteração pergunta antes de gravar e desiste se eu não confirmar
    Dado que o processo existe e ainda não foi lançado
    Quando escolho alterar e envio
    Então vejo * Confirma alteracao do processo <S/N> ? *
    Quando respondo N
    Então a tela volta ao estado inicial, sem ter gravado nada

  Cenário: Recusa alterar processo que ainda não foi lançado
    Dado que o processo existe e ainda não foi lançado
    Quando escolho alterar e envio
    Então vejo * Processo nao pode ser alterado *
    E nada é gravado

  Cenário: Recusa alterar processo já integrado com o SIAFIC
    Dado que o processo existe e está em integração com o SIAFIC
    Quando escolho alterar e envio
    Então vejo * Processo na integracao com SIAFIC *
    E nada é gravado

  Cenário: A exclusão pergunta antes de gravar e desiste se eu não confirmar
    Dado que o processo existe e ainda não foi lançado
    Quando escolho excluir e envio
    Então vejo * Confirma exclusao do processo <S/N> ? *
    Quando respondo N
    Então a tela volta ao estado inicial, sem ter apagado nada

  Cenário: Recusa excluir processo que já foi lançado
    Dado que o processo já foi lançado
    Quando escolho excluir e envio
    Então vejo * Processo nao pode ser excluido *
    E nada é apagado

  Cenário: A exclusão confirmada devolve o que o processo consumiu
    Dado que o processo existe, ainda não foi lançado e tem notas ligadas a ele
    Quando escolho excluir e respondo S à confirmação
    Então as notas saem do processo, os itens delas são apagados
    E o contrato recebe de volta a quantidade e o valor que elas haviam consumido
    E o processo é apagado

  Cenário: A troca de fonte atualiza o processo e os lançamentos ligados a ele
    Dado que o processo existe, já foi lançado e tem uma fonte diferente da que informei
    Quando informo a nova fonte e respondo S à confirmação da alteração
    Então o processo passa a apontar para a fonte nova
    E os lançamentos do processo são atualizados para a fonte nova

  Cenário: A impressão exige SEI, e-mail e número de vias
    Dado que informei o código de impressão em um processo que já foi lançado
    Quando o processo não tem SEI associado
    Então vejo * SEI ainda nao associado ao processo *
    Quando o meu cadastro não tem e-mail
    Então vejo * Usuario sem e-mail cadastrado *
    Quando não informo o número de vias
    Então vejo * Informe o numero de vias *
    Quando já existe requisição da mesma natureza em processamento
    Então vejo * Relatorio em processamento. Aguarde. *
    E nada é impresso

  Cenário: Operação confirmada segue para o lançamento das notas
    Dado que o processo existe e confirmei a operação
    Então a tela entrega o processo com a situação fechado
    E abre a tela seguinte para lançar as notas do processo

  Cenário: Operação confirmada deixa registro de auditoria
    Dado que confirmei a operação
    Então fica registrado o processo, a minha matrícula, a estação, a data, a hora e a operação
    E ficam registrados o valor antes e o valor depois
```
