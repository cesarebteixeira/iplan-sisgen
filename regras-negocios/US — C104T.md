# US — C104T — Manter os atendimentos de cada segmento do órgão

## Estória

Como **servidor da CRE**, quero **registrar e manter os atendimentos que a minha
secretaria oferece em cada segmento de atendimento, com a descrição, a situação e o
grupo que cobre cada horário**, para que **o atendimento prestado possa ser
identificado e classificado — e para que nada que esteja em uso seja apagado por
engano**.

O atendimento é a peça que amarra o segmento ao grupo de atendimento: é aqui que a
secretaria declara que aquele atendimento existe naquele segmento e, em cada horário —
o parcial, o integral e o de 24 horas —, qual grupo o cobre. Enquanto houver atendimento
num segmento, o segmento não pode ser excluído; enquanto um atendimento apontar para um
grupo, o grupo não pode ser excluído. Sem este cadastro, as telas que classificam o
atendimento ficam sem nada a que apontar.

## Contexto

Jornada S000M → C000M → C028M → C104T.

Ator: servidor de CRE — mantém, para a secretaria em que atua, os atendimentos de cada
segmento de atendimento do órgão, com os horários e os grupos que os cobrem.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. As duas telas antes desta são menus,
mas nenhuma delas fica esperando resposta: cada uma **entrega a transação** à seguinte, e
é a mesma transação que chega aqui — o mesmo registro e a mesma área de trabalho da
sessão. Esta é a última tela da jornada: ela não entrega a transação a nenhuma outra.

## Regras de negócio

### RN-01 — A tela trabalha sobre o tipo de órgão da secretaria do usuário; o órgão não se digita

O tipo de órgão não se digita nesta tela: é o tipo de órgão que o vínculo da matrícula com
a secretaria escolhida na entrada deixou na sessão, e é a chave de tudo o que a tela lê e
grava. O cabeçalho apenas mostra a descrição desse tipo de órgão e a data do sistema, e o
usuário não tem como operar outra secretaria.

### RN-02 — A tela reapresenta a opção de manutenção guardada na sessão e continua a lista de onde parou

Ao abrir, a tela mostra a opção de manutenção que ficou guardada do uso anterior na mesma
sessão; quando não há nenhuma guardada, ela abre em consulta. A opção que chegar dentro do
registro de quem chamou é substituída, antes da exibição, pela que a própria tela guardou. A
lista também retoma da posição em que a sessão parou: a tela guarda o último atendimento
mostrado e recomeça por ele.

[?] O que o chamador deixar na área de trabalho livre da sessão pode chegar à posição em
que a tela lê a sua opção, porque essa área passa de tela em tela. A fonte não diz o que
as telas desta jornada deixam ali; se deixarem algo, a opção de abertura poderá não ser a
da própria tela. Pergunta ao site.

[?] A posição guardada é a do último atendimento da página, e a retomada começa por esse
mesmo atendimento. Ou a passagem de página repete esse atendimento, ou o sistema o pula —
a fonte não permite concluir qual dos dois, porque a retomada depende de sinalizadores de
leitura que o acervo não documenta. Pergunta ao site.

### RN-03 — A grade tem 7 linhas, e cada linha informa 11 dados

São 7 linhas por vez. Cada linha informa onze dados: o código do segmento (2 dígitos), o
código do atendimento (2), a descrição do atendimento (20 caracteres), a marca de cada um
dos três horários — parcial, integral e 24 horas —, a ação (1), a situação (1) e o código
do grupo de atendimento de cada horário (2 cada). Sem que se digite, a tela mostra ainda,
por linha, a descrição resumida do segmento, o "Sim" ou o "Nao" de cada horário e da
situação, e a descrição resumida de cada grupo. Fora da grade, o cabeçalho traz sete dados
vindos do terminal (a tela, a origem, o número da transação, a data de entrada, o mês de
referência, a opção de manutenção e o prefixo de tela), mais a descrição do tipo de órgão,
a data do sistema e a linha de mensagem.

### RN-04 — Os códigos da linha passam pela edição numérica antes de qualquer conferência

O código do segmento, o do atendimento e os três códigos de grupo passam pela edição
numérica antes de qualquer conferência de negócio: o que não for número é recusado no
próprio campo, com o cursor devolvido a ele, e não chega a ser conferido. Os dois
marcadores de posição da lista — o segmento e o atendimento por onde ela retoma — passam
pela mesma edição: são sete campos ao todo.

### RN-05 — A opção de manutenção só aceita alteração e consulta; sem opção, a tela abre em consulta

A opção aceita apenas alteração e consulta. Qualquer outra é recusada com
"* Opcao nao disponivel. Use ALT ou CON *". Quando o campo chega em branco, a tela adota a
consulta.

[?] A guarda interna compara a opção com os códigos de alteração e de consulta, enquanto a
mensagem manda usar "ALT" e "CON". Ou o terminal traduz o mnemônico antes de enviar, ou a
mensagem está desalinhada da guarda. Pergunta ao site; não concluo qual dos dois.

### RN-06 — A consulta não confere e não grava nada

Com a opção de consulta, a tela apenas mostra a lista: as linhas informadas não passam por
nenhuma conferência e nenhuma gravação é executada. O único acesso que a consulta ainda faz
ao cadastro é a leitura dos marcadores de posição, para saber por onde a lista retoma —
leitura, não gravação.

### RN-07 — A ação é por linha: I inclui, A altera, E exclui; o resto não faz nada

A ação é da linha, não da tela: I inclui, A altera e E exclui, e a tela traduz a letra para
a operação correspondente antes de pedir autorização. Linha sem código de atendimento é
ignorada, e ação fora de I, A e E também — em silêncio, sem mensagem.

### RN-08 — Cada linha executável passa antes pela conferência de acesso do usuário

Antes de tocar no cadastro, a operação da linha — incluir, alterar ou excluir — é conferida
contra o perfil de acesso do usuário àquela tela: sem a permissão da operação, a tela mostra
"* Acesso negado para esta operacao *" e nada é executado. Sem perfil de acesso à tela, a
recusa é "* Acesso negado para esta matricula *". A abertura da tela passa pela conferência
do perfil, e a opção de alteração passa pela conferência da operação de alteração.

### RN-09 — Consultar lista os atendimentos da secretaria, na ordem do segmento e do código, até 7 linhas

Na consulta a tela percorre os atendimentos da secretaria e mostra um por linha, até 7, na
ordem do segmento e, dentro dele, do código do atendimento. Cada linha traz ainda a
descrição resumida do segmento a que aquele atendimento pertence e a descrição resumida do
grupo de cada horário, lidas dos cadastros. Quando não há nenhum atendimento para mostrar, a
tela avisa "* Nao existem atendimentos cadastrados *".

### RN-10 — Incluir exige que o código do atendimento ainda não exista em nenhum segmento da secretaria

Ao incluir, a tela procura primeiro o par segmento×atendimento: existindo, recusa com
"* Atendimento ja cadastrado *". Em seguida procura o código do atendimento em qualquer
segmento do mesmo tipo de órgão: existindo — isto é, já usado em outro segmento —, recusa
com a mesma mensagem. O código do atendimento é, portanto, único dentro da secretaria, e
não se repete em dois segmentos.

### RN-11 — Incluir exige o segmento informado e cadastrado

Na inclusão o segmento é obrigatório: em branco, a tela recusa com "* Informe o segmento *".
Informado, ele tem de existir no cadastro de segmentos de atendimento da secretaria; não
existindo, "* Segmento nao cadastrado *".

### RN-12 — Incluir e alterar exigem a descrição e a situação

Para incluir ou alterar, a descrição do atendimento tem de vir preenchida: em branco, a tela
recusa com "* Informe a descricao *". A situação só aceita "S" ou "N": qualquer outra coisa
é recusada com "* Informe ativo com S ou N *". A exclusão não pede nenhuma das duas.

### RN-13 — Cada horário marcado exige o grupo, e o grupo tem de estar cadastrado naquele segmento

Para incluir ou alterar, cada horário marcado tem de trazer o código do grupo de atendimento
que o cobre; sem ele, a tela recusa com "* Inf.grupo de atendimento - horario parcial *",
"* Inf.grupo de atendimento - horario integral *" ou "* Inf.grupo de atendimento - horario
24 H *", conforme o horário. Informado, o grupo tem de estar cadastrado naquele segmento;
não estando, a recusa é "* Grupo atendimento nao cadastr.neste segmento *". Horário não
marcado não pede grupo, e a exclusão não passa por nenhuma dessas conferências.

### RN-14 — Alterar e excluir exigem que o atendimento exista

Ao alterar ou excluir, o atendimento informado tem de existir para aquele segmento: não
existindo, a tela recusa com "* Atendimento nao cadastrado *" e nada é gravado. A inclusão,
que não exige existência, é a única que cria.

### RN-15 — A alteração troca a descrição, a situação, os horários e os grupos; o segmento e o código não mudam

Existindo o atendimento, a alteração substitui apenas a descrição, a situação, as marcas de
horário e os três grupos. O segmento e o código do atendimento permanecem os que estavam
gravados — a alteração não move o atendimento de segmento nem lhe troca o código.

### RN-16 — Ao gravar, os três horários saem marcados; o horário que chegou em branco não tem o grupo apagado

Numa linha executada, os três horários são gravados como oferecidos: a marca que chegou em
branco é convertida em "S", e o grupo que veio com ela é mantido como está. A tela tem um
passo que apagaria o grupo quando a marca chegasse em branco, mas ele vem depois do passo
que preenche a marca, e por isso nunca é alcançado.

[?] Os dois passos se contradizem: um preenche a marca em branco, o outro só apagaria o
grupo se a marca continuasse em branco — e o segundo nunca chega a rodar. Ou o horário em
branco significa oferecido, e o apagamento é um passo morto; ou significava não oferecido, e
a gravação não faz o que pretendia. Pergunta ao site; não escolho um dos dois.

### RN-17 — A conferência vem toda antes da gravação

A tela percorre as linhas duas vezes: numa primeira passagem só confere e produz as recusas;
é a última passagem que grava. A passagem que grava não repete nenhuma conferência — se uma
delas recusou, a gravação não chega a acontecer.

### RN-18 — Toda inclusão, alteração e exclusão deixam rastro na auditoria

Cada uma das três operações grava um registro na trilha de auditoria com o tipo de órgão, a
CRE, a matrícula, a estação, a data e a hora, o cadastro de origem, a operação e os valores
antes e depois — e só então grava (ou apaga) o atendimento. Na inclusão os valores anteriores
vão em branco e os posteriores levam o atendimento gravado; na alteração vão os dois, o
registro antigo e o novo; na exclusão os anteriores levam o atendimento e os posteriores vão
em branco.

### RN-19 — A tela grava no cadastro de atendimentos e na auditoria e lê três cadastros; das operações prontas, executa três

A tela inclui, altera e exclui somente no cadastro de atendimentos (C105T), e grava também a
trilha de auditoria (A010T). Os outros três cadastros que ela enxerga — o de títulos de tela
(S030T), o de segmentos de atendimento (C160T) e o catálogo de grupos de atendimento (C103T)
— são apenas lidos. Para cada cadastro que enxerga, o sistema traz prontas uma operação de
gravar e uma de apagar: das dez, a tela executa três.

### RN-20 — Falha no banco interrompe a operação

Todo acesso ao banco testa o erro: o erro de leitura e o de gravação são levados à rotina de
comunicação do sistema, e a transação para ali, sem completar o resto. Uma gravação abortada
não segue para o passo seguinte.

### RN-21 — A tela não escolhe o comportamento pela tela que a chamou, e não entrega a transação a outra tela

A tela não compara a tela de origem com nenhum código: nada no comportamento dela é escolhido
por quem a chamou. O que pode mudar o comportamento dela é o que chega dentro do próprio
registro — a opção de manutenção e o prefixo de tela —, e a opção é reposta pela própria tela
na abertura. Esta também é a última tela da jornada: não há tela seguinte, e nada é entregue
adiante sem que o prefixo de tela peça.

### RN-22 — O prefixo de tela, quando vem preenchido, encaminha a transação e a conferência não roda

Se o prefixo de tela chegar preenchido com o código de uma tela, a transação é encaminhada
para essa tela antes de qualquer conferência desta, e a conferência desta não roda: nada é
conferido nem gravado aqui. Chegando em branco, a tela segue e confere a entrada — é por isso
que a conferência inteira fica atrás desse teste.

## Cenários BDD

```gherkin
Funcionalidade: Manter os atendimentos de cada segmento do órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C104T

  Cenário: RN-01, RN-03 e RN-09 — consultar os atendimentos da secretaria
    Dado que abro a tela C104T
    Quando confirmo sem informar nada
    Então a tela abre em consulta, com a descrição do meu tipo de órgão e a data do sistema no cabeçalho
    E vejo, em cada uma das 7 linhas, o segmento, a descrição resumida do segmento, o atendimento, a descrição do atendimento, as marcas de horário com os grupos e a situação
    E nenhum outro tipo de órgão pode ser informado ou operado

  Cenário: RN-06 — a consulta não grava nada
    Dado que estou na tela C104T com a opção de consulta
    Quando preencho qualquer linha, com qualquer ação, e confirmo
    Então nada é conferido e nada é gravado
    E a lista continua sendo o que o cadastro tem

  Cenário: RN-02 — a tela reapresenta a última opção da sessão e retoma a lista
    Dado que já usei a tela nesta sessão com a opção de alteração
    Quando abro a tela C104T de novo
    Então a opção de manutenção é a da última utilização
    E a lista retoma da posição em que a sessão parou

  Cenário: RN-21 — a opção de abertura vem da própria tela, não de quem a chamou
    Dado que chego a esta tela sem nunca tê-la usado nesta sessão
    Quando abro a tela C104T
    Então ela abre em consulta
    E nada do que a tela anterior deixou no registro decide a opção

  Cenário: RN-09 — secretaria sem atendimentos
    Dado que a secretaria não tem nenhum atendimento para mostrar
    Quando confirmo a consulta
    Então vejo "* Nao existem atendimentos cadastrados *"

  Cenário: RN-04 — código não numérico
    Quando preencho o segmento, o atendimento ou um dos grupos com letra
    Então a tela recusa o campo antes de qualquer conferência
    E nada é gravado

  Cenário: RN-05 — opção de manutenção não disponível
    Quando informo uma opção de manutenção diferente de ALT e CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E nada é gravado

  Cenário: RN-07 — linha sem atendimento ou com ação desconhecida
    Dado que preencho uma linha sem o código do atendimento, ou com uma ação diferente de I, A e E
    Quando confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada

  Cenário: RN-08 — acesso negado para a operação da linha
    Dado que o meu perfil de acesso não permite incluir, alterar ou excluir nesta tela
    Quando confirmo a linha com a ação correspondente
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-08 — sem perfil de acesso à tela
    Dado que a minha matrícula não tem perfil de acesso a esta tela
    Quando abro a tela C104T
    Então vejo "* Acesso negado para esta matricula *"
    E nada é gravado

  Cenário: RN-10, RN-11, RN-12, RN-13, RN-15, RN-16, RN-18 e RN-19 — incluir um atendimento
    Dado que estou na tela C104T com a opção ALT
    E o segmento informado está cadastrado para a minha secretaria
    E o código do atendimento ainda não é usado em nenhum segmento dela
    E informo a descrição, a situação S ou N e, para cada horário marcado, um grupo cadastrado naquele segmento
    Quando preencho a linha com a ação I e confirmo
    Então o atendimento fica gravado para a secretaria naquele segmento
    E a inclusão fica registrada na auditoria, com os valores posteriores preenchidos

  Cenário: RN-10 — incluir um atendimento que o segmento já tem
    Dado que aquele segmento já tem aquele código de atendimento
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Atendimento ja cadastrado *"
    E nada é gravado

  Cenário: RN-10 — incluir um código de atendimento já usado em outro segmento
    Dado que aquele código de atendimento já existe em outro segmento da mesma secretaria
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Atendimento ja cadastrado *"
    E nada é gravado

  Cenário: RN-11 — incluir sem o segmento
    Quando preencho a linha com a ação I, o atendimento e nenhum segmento
    Então vejo "* Informe o segmento *"
    E nada é gravado

  Cenário: RN-11 — incluir com segmento não cadastrado
    Dado que o segmento informado não está cadastrado para a minha secretaria
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Segmento nao cadastrado *"
    E nada é gravado

  Cenário: RN-12 — incluir ou alterar sem a descrição
    Dado que preencho a linha com a ação I ou A e deixo a descrição em branco
    Quando confirmo
    Então vejo "* Informe a descricao *"
    E nada é gravado

  Cenário: RN-12 — situação fora de S e N
    Dado que preencho a linha com a ação I ou A e uma situação diferente de S e N
    Quando confirmo
    Então vejo "* Informe ativo com S ou N *"
    E nada é gravado

  Cenário: RN-13 — horário marcado sem o grupo
    Dado que marco o horário parcial e não informo o grupo dele
    Quando confirmo a inclusão
    Então vejo "* Inf.grupo de atendimento - horario parcial *"
    E nada é gravado

  Cenário: RN-13 — grupo não cadastrado no segmento
    Dado que informo, para um horário marcado, um grupo que não está cadastrado naquele segmento
    Quando confirmo a inclusão
    Então vejo "* Grupo atendimento nao cadastr.neste segmento *"
    E nada é gravado

  Cenário: RN-14 — alterar ou excluir um atendimento que não existe
    Quando preencho a linha com a ação A ou E em um segmento e um código de atendimento que não existem
    Então vejo "* Atendimento nao cadastrado *"
    E nada é gravado

  Cenário: RN-15 e RN-18 — alterar um atendimento
    Dado que o atendimento existe naquele segmento
    Quando preencho a linha com a ação A, troco a descrição, a situação e os grupos, e confirmo
    Então a descrição, a situação, os horários e os grupos ficam atualizados
    E o segmento e o código do atendimento continuam os mesmos
    E a alteração fica registrada na auditoria, com os valores anteriores e os posteriores

  Cenário: RN-16 — o horário que chegou em branco é gravado como oferecido
    Dado que altero um atendimento deixando a marca do horário parcial em branco
    Quando confirmo
    Então o horário parcial fica gravado como oferecido
    E o grupo que veio na linha daquele horário não é apagado

  Cenário: RN-14, RN-18 e RN-19 — excluir um atendimento
    Dado que o atendimento existe naquele segmento
    Quando preencho a linha com a ação E e confirmo
    Então o atendimento deixa de existir
    E a exclusão fica registrada na auditoria, com os valores anteriores preenchidos

  Cenário: RN-17 — a recusa impede a gravação
    Dado que uma das linhas informadas é recusada
    Quando confirmo
    Então vejo a mensagem da recusa
    E nenhuma gravação daquela entrada é executada

  Cenário: RN-20 — falha no banco durante a gravação
    Dado que a gravação do atendimento falha no banco
    Quando confirmo a inclusão
    Então a transação é interrompida com a mensagem de erro do sistema
    E o atendimento não é considerado incluído

  Cenário: RN-22 — o prefixo de tela encaminha a transação
    Dado que informo no prefixo de tela o código de outra tela
    Quando confirmo
    Então a transação é encaminhada para a tela informada
    E nenhuma conferência desta tela é executada
    E nada é gravado por esta tela
```
