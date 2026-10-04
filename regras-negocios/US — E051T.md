# US — E051T — Manter comensais por refeição e dia da semana

## Estória

Como **servidor da CRE que responde pelo preparo da alimentação escolar da sua
coordenadoria**, quero **dizer quantos comensais cada refeição atende em cada um dos sete
dias da semana de um segmento do órgão filho, e corrigir, apagar ou consultar o que já
estava dito**, para que **o dimensionamento da merenda daquele órgão fique registrado dia a
dia e a tela seguinte possa abrir o mapa da semana**.

A quantidade de comensais de um dia é o que dimensiona a refeição servida naquele dia: é por
segmento e por refeição que a rede declara quantas pessoas são atendidas, e é esse número
que o planejamento e o mapa consomem. Enquanto ele não existe, o órgão tem a semana aberta
mas não tem o que servir. A tela trabalha **um segmento por vez**, dentro de uma requisição
de cálculo já aberta: a requisição diz de qual órgão, de qual coordenadoria e de qual semana
se trata, e o segmento diz qual conjunto de escolas daquele órgão está sendo dimensionado.
Os dias da semana não são livres — eles vêm do planejamento da semana, e o dia que o
planejamento não previu não recebe comensais.

## Contexto

Jornada S000M → E000M → E050M → E050T → E051T.
Ator: servidor de CRE — informa, corrige, apaga ou consulta os comensais de cada refeição,
nos sete dias da semana, de um segmento do órgão filho da sua secretaria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. O `E000M` e o `E050M` não gravam nada: só encaminham, e
não registram origem nem operação na sessão.

Esta tela **não é aberta pelo menu**: ela é a continuação da tela de cálculo de uma
requisição, e o `E050T` encadeia nela sem passar por menu nenhum. É a tela de cálculo que
decide com que **operação** ela abre — inclusão, alteração, exclusão ou consulta (RN-02) —,
e é por isso que o menu não a alcança (RN-01). Esta tela, por sua vez, também encadeia para a
frente: ela passa o segmento para a `E052T` quando o fluxo continua, e devolve o fluxo à tela
de cálculo quando a requisição volta incompleta (RN-18).

O que esta tela usa do que veio antes é a **secretaria (o tipo de órgão), a coordenação
regional escolar, a matrícula, o código de acesso, o privilégio e a data do sistema** da
sessão, além do **vínculo do servidor com o órgão filho**; isso é regra da entrada e está no
anexo de evidências, em **Regras que se revelaram da entrada**. Da tela de cálculo vêm a
requisição (órgão, coordenação, datas do cálculo e do período), o segmento corrente e os sete
dias da semana com o dia da semana e o cardápio de cada um.

## Regras de negócio

### RN-01 — A tela só abre pela requisição de cálculo; de outra origem volta ao menu

Esta tela é a continuação da requisição de cálculo e **só trabalha quando o fluxo chega
dela**. Chegando por qualquer outro caminho — outro encadeamento, ou uma reabertura que não
seja aquela —, a tela não executa nada: descarta o que estava em preparo e devolve o fluxo ao
menu `E050M`. O que fica descartado é a área de trabalho da sessão: a tela a limpa antes de
sair.

### RN-02 — A operação vem decidida pela tela de cálculo, e são quatro

Quem escolhe a operação é a **tela de cálculo**: inclusão, alteração, exclusão ou consulta. A
tela desta jornada não pede a operação ao servidor; ela a recebe, e é com essa operação que
trabalha do começo ao fim. Informada qualquer outra operação, a recusa é **\* Opcao nao
disponivel. Use INC, ALT, EXC ou CON \***, com o cursor de volta ao campo da operação e nada
executado.

[?] A tela confere a operação contra quatro códigos internos, e a mensagem de recusa manda o
servidor usar **INC, ALT, EXC e CON**. Ou o que ele digita é traduzido antes de chegar à
conferência, ou a mensagem está desalinhada dela. Pergunta ao site.

### RN-03 — O vínculo do servidor limita a tela ao órgão filho dele

A tela reconfere o **vínculo entre a matrícula do servidor e a secretaria** e só opera
requisição do **órgão filho desse vínculo**. Não achando o vínculo, ou sendo o órgão da
requisição outro, a tela abandona o que estava fazendo e devolve o fluxo ao menu `E050M`, sem
mensagem própria. É a mesma limitação que a tela de cálculo aplica: a requisição só é do
órgão do servidor.

[?] A comparação do órgão da requisição com o vínculo do servidor é feita **duas vezes**, por
duas fontes diferentes, e os dois desfechos não são o mesmo: numa delas o órgão vem da sessão
e o fluxo volta à tela de cálculo já como inclusão; na outra o vínculo é lido de novo no
cadastro e o fluxo volta ao menu. Ou uma das duas é a que vale, ou as duas valem para
situações diferentes. Pergunta ao site.

### RN-04 — A requisição tem de vir completa

A requisição chega da tela de cálculo já preparada, e a tela confere que ela está inteira: as
**duas datas do cálculo** (a inicial e a limite), o **período** (início e limite, com o limite
nunca anterior ao início), os **sete dias da semana** (cada um com o seu dia da semana e o seu
cardápio) e a **marca de creche**. Faltando qualquer um desses dados, ou sendo as datas
incoerentes, a operação passa a ser **inclusão** e o fluxo volta à tela de cálculo, para que a
requisição seja refeita.

[?] A tela devolve a requisição incompleta à tela de cálculo com a operação de inclusão, mas a
tela de cálculo, reaberta com uma operação já na área da sessão e uma origem que ela não
reconhece, copia os dados para a sua tela e encerra sem executar nada. Ou a devolução se dá
por outro caminho, ou a requisição incompleta não é retomada. Pergunta ao site.

### RN-05 — O segmento tem de estar cadastrado para o órgão

O segmento em que a tela está trabalhando tem de existir no cadastro de segmentos daquele
órgão. Não existindo, a recusa é **\* Orgao nao pertence mais a este segmento \*** — e, quando
a requisição já tem comensais registrados naquele segmento, a recusa é **\* Org.nao pertence
mais a este segmento. Use EXC \***, que orienta a apagar o registro pela exclusão. Nas duas, o
cursor volta ao campo da operação e nada é gravado.

### RN-06 — Requisição já processada não se altera nem se exclui

Quando a requisição do período já está marcada como **processada**, a alteração e a exclusão
são recusadas com **\* Nao atualize. Calculo ja processado \***, com o cursor de volta ao
campo da operação e nada gravado. Para uma requisição processada, resta a **consulta**. É
também o que a faixa de situação da tela mostra: uma requisição processada exibe **\*
REQUISICAO PROCESSADA \*** no lugar da linha de situação.

### RN-07 — A consulta só lê

Na consulta, a tela lê os comensais registrados e os mostra; **não grava, não altera e não
apaga nada**. Ela é a única operação que atravessa a tela inteira sem passar por nenhum
trecho de gravação ou de exclusão.

### RN-08 — A refeição tem de estar cadastrada

Para cada refeição que a tela mostra, ela confere se a refeição está cadastrada. Não estando, a
recusa é **\* Segmento sem comensais cadastr. para refeicao \***, com o cursor de volta ao
campo da operação e nada gravado: sem o cadastro da refeição, não há onde lançar comensais.

### RN-09 — A refeição tem de ter teto de comensais cadastrado e ativo

A tela procura o **teto de comensais** cadastrado para aquela refeição naquele segmento — o
mesmo cadastro que a tela de comensais mantém. Sem o teto cadastrado, a recusa é **\* Maximo
comensais nao cad. para esta refeicao \***; com o teto cadastrado mas **inativo**, a recusa é
**\* Maximo de comensais inativo \***. Nas duas, nada é gravado.

### RN-10 — A quantidade de um dia não passa do teto de comensais

A quantidade informada para um dia é comparada com o teto de comensais da refeição naquele
segmento. Acima do teto, a recusa é **\* <-Quant. comensais maior que o maximo permitido \***,
que mostra o teto, com o cursor de volta ao campo daquele dia e nada gravado. A conferência só
roda nos dias que têm quantidade informada: dia deixado em branco passa direto.

### RN-11 — Sábado e domingo só recebem comensais se o segmento os atender

Quando o dia da semana é sábado ou domingo, a tela confere se o segmento está cadastrado como
**atendendo sábado e domingo**. Não estando, a recusa é **\* Segmento nao recebe refeic.
sabados e domingos \*** — a mensagem identifica a refeição —, com o cursor de volta ao campo
daquele dia e nada gravado.

### RN-12 — Feriado da secretaria não recebe comensais

Cada dia informado é conferido contra o **cadastro de feriados da secretaria**, pela data
daquele dia. Sendo feriado, a recusa é **\* Feriado - nao informe comensais \***, com o cursor
de volta ao campo daquele dia e nada gravado. Como na regra anterior, só os dias com
quantidade informada passam por essa conferência.

### RN-13 — A semana tem de ter planejamento, e cada dia o seu cardápio

A tela procura o **planejamento da semana** daquela refeição naquele segmento — o
planejamento identificado pela data de início do cálculo da requisição. Faltando o
planejamento, a recusa é **\* Nao existe planejamento para esta semana \***. Existindo o
planejamento, cada dia da semana tem de ter o seu **cardápio** previsto: o dia que o
planejamento não previu é recusado com **\* Dia sem planejamento para esta refeicao \***. Nas
duas, o cursor volta ao campo do dia e nada é gravado.

### RN-14 — Refeição já lançada no pedido extra bloqueia

Quando a refeição daquela requisição e daquele segmento já aparece no **pedido extra**, a
tela recusa: **\* Refeicao cadastrada no pedido extra \***, com o cursor no primeiro dia que
tem quantidade informada e nada gravado. A inclusão e a alteração não passam por cima do que
o pedido extra já lançou.

### RN-15 — O que a inclusão e a alteração gravam

Passando pelas conferências, a tela grava, para o segmento e para cada refeição, a
**quantidade de comensais de cada um dos sete dias**. O registro é identificado pelo órgão, pela
coordenação, pela data de início do cálculo, pelo segmento e pela refeição — e é essa
combinação que o distingue de todos os outros. O dia que o servidor deixar em branco **fica
sem comensais**: a tela limpa o que aquele dia tinha. Quando a requisição já tem exatamente as
mesmas quantidades informadas, a tela **não grava nada** — não há o que mudar.

Apagando as **sete** quantidades de uma refeição, o registro de comensais daquela refeição no
segmento é **excluído** — e com ele os pedidos extras lançados para os dias que tinham sobra
naquela refeição. É assim que a refeição sai do segmento.

Para a refeição marcada no cadastro como **tendo sobra**, a tela guarda também, por dia, o
cardápio de sobra e a quantidade de sobra: o cardápio de sobra é procurado no cadastro de
cardápios daquele dia e a quantidade de sobra é a quantidade informada para o dia. Para as
outras refeições, esses dois campos ficam zerados.

[?] A quantidade de sobra acaba sendo sempre igual à quantidade de comensais informada para o
dia — a tela não pede uma quantidade de sobra própria, e o campo só é preenchido quando o
cardápio de sobra existe no cadastro. Se a sobra deveria ter número próprio, esse caminho não
existe nesta tela. Pergunta ao site.

### RN-16 — A exclusão apaga os comensais do segmento e, sendo o último, a requisição do período

Na exclusão, a tela apaga, em laço, **todos os registros de comensais daquele segmento** e
também os registros de **pedido extra** daquele segmento e daquela data de cálculo. Apagados os
comensais, se **não sobrou nenhum** para aquela requisição, a tela apaga também a **requisição
do período** (a que guarda as datas do cálculo, o período e a situação). Em toda exclusão a
tela deixa a **trilha de auditoria** do que foi apagado, com a operação e o registro anterior à
exclusão.

### RN-17 — A tela navega entre os segmentos do órgão

A tela tem um campo para o **segmento anterior** e outro para o **segmento seguinte**. O
segmento anterior é o de número imediatamente menor: a tela recua o número, procura o cadastro
do segmento e os comensais dele e, quando nenhum dos dois existe, recusa com **\* Nao existem
segmentos anteriores \***, com o cursor de volta ao campo do segmento anterior. O caminho do
segmento seguinte é o que continua o fluxo para a tela seguinte (RN-18).

### RN-18 — O que a tela entrega às telas seguintes

Esta tela encadeia, sem passar por menu:

- para a **E052T**, quando o fluxo continua no segmento seguinte. Ela passa o que estava
  trabalhando — órgão, coordenação, data do cálculo, segmento e os dias — e **preserva a marca
  de origem**, para que a tela seguinte se reconheça na mesma cadeia e abra no modo próprio;
- de volta para a **tela de cálculo (`E050T`)**: quando a requisição volta incompleta (RN-04),
  já com a operação de inclusão; e quando o órgão **perdeu o último segmento** por causa da
  exclusão, e então a tela de cálculo é reaberta **em consulta**;
- de volta para o **menu `E050M`**, quando a requisição não é do órgão do vínculo do servidor
  ou quando a operação não é uma das quatro.

Pela porta de entrada, a tela também pode ser **reaberta pela tela seguinte em exclusão**,
quando os comensais do segmento existem mas o cadastro do segmento não existe mais.

[?] A tela devolve o fluxo ao menu sem marcar a origem da devolução, e o menu `E050M` só
aceita ser reaberto por duas marcas conhecidas — fora delas, ele responde com **\* Acesso deve
ser feito pela tela E050T \***. Ou o menu mostra essa recusa por engano nessas devoluções, ou
a devolução deveria marcar a origem. Pergunta ao site.

[?] A tela reabre a tela de cálculo em consulta quando o órgão fica sem segmentos, mas a tela
de cálculo reconhece essa reabertura e recusa a si mesma em vez de consultar. Ou a consulta se
dá por outro endereço, ou a reabertura não é alcançável. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Comensais por refeição e por dia da semana do segmento (ORGAO FILHO SDI / CORD.REG.ESCOLAR)

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E051T

  Cenário: A tela chega por outro caminho e volta ao menu
    Dado que cheguei à tela sem passar pela tela de cálculo
    Quando a tela confere a origem
    Então o que estava em preparo é descartado
    E sou devolvido ao menu E050M
    E nada é gravado

  Cenário: Operação não prevista é recusada
    Dado que a tela recebeu uma operação diferente de incluir, alterar, excluir ou consultar
    Quando a tela confere a operação
    Então vejo "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Requisição de outro órgão filho devolve ao menu
    Dado que a requisição é de um órgão filho diferente do meu vínculo
    Quando a tela reconfere o vínculo
    Então a tela abandona a requisição
    E sou devolvido ao menu E050M
    E nada é gravado

  Cenário: Requisição incompleta volta à tela de cálculo como inclusão
    Dado que a requisição chegou sem os sete dias da semana, ou sem as datas, ou sem a marca de creche
    Quando a tela confere a requisição
    Então a operação passa a ser inclusão
    E o fluxo volta à tela de cálculo
    E nada é gravado

  Cenário: Segmento não cadastrado para o órgão é recusado
    Dado que o segmento em que estou trabalhando não está cadastrado para o órgão
    Quando a tela procura o segmento
    Então vejo "* Orgao nao pertence mais a este segmento *"
    E nada é gravado

  Cenário: Segmento que já tem comensais e sumiu do cadastro é recusado com orientação de exclusão
    Dado que o segmento não está mais cadastrado para o órgão
    E a requisição já tem comensais registrados nesse segmento
    Quando a tela procura o segmento
    Então vejo "* Org.nao pertence mais a este segmento. Use EXC *"
    E nada é gravado

  Cenário: Requisição já processada não se altera nem se exclui
    Dado que a requisição do período já está processada
    Quando peço alterar ou excluir
    Então vejo "* Nao atualize. Calculo ja processado *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Consulta não grava nada
    Dado que a operação é consultar
    Quando a tela lê os comensais registrados
    Então eles são mostrados
    E nada é gravado, alterado ou apagado

  Cenário: Refeição sem cadastro é recusada
    Dado que uma das refeições mostradas não está cadastrada
    Quando a tela confere a refeição
    Então vejo "* Segmento sem comensais cadastr. para refeicao *"
    E nada é gravado

  Cenário: Refeição sem teto de comensais cadastrado é recusada
    Dado que a refeição não tem teto de comensais cadastrado para o segmento
    Quando a tela procura o teto
    Então vejo "* Maximo comensais nao cad. para esta refeicao *"
    E nada é gravado

  Cenário: Teto de comensais inativo é recusado
    Dado que o teto de comensais da refeição está inativo
    Quando a tela procura o teto
    Então vejo "* Maximo de comensais inativo *"
    E nada é gravado

  Cenário: Quantidade acima do teto é recusada
    Dado que informei para um dia uma quantidade maior que o teto de comensais da refeição
    Quando a tela confere a quantidade do dia
    Então vejo "* <-Quant. comensais maior que o maximo permitido *", com o teto na mensagem
    E o cursor volta ao campo daquele dia
    E nada é gravado

  Cenário: Dia de sábado ou domingo sem autorização do segmento é recusado
    Dado que o segmento não atende sábado e domingo
    E informei quantidade num sábado ou num domingo
    Quando a tela confere o dia da semana
    Então vejo "* Segmento nao recebe refeic. sabados e domingos *"
    E o cursor volta ao campo daquele dia
    E nada é gravado

  Cenário: Dia de feriado é recusado
    Dado que o dia informado está marcado como feriado para a secretaria
    Quando a tela confere o calendário
    Então vejo "* Feriado - nao informe comensais *"
    E o cursor volta ao campo daquele dia
    E nada é gravado

  Cenário: Semana sem planejamento é recusada
    Dado que não existe planejamento da semana para a refeição naquele segmento
    Quando a tela procura o planejamento
    Então vejo "* Nao existe planejamento para esta semana *"
    E nada é gravado

  Cenário: Dia sem cardápio no planejamento é recusado
    Dado que o planejamento da semana não previu cardápio para um dos dias informados
    Quando a tela confere o dia
    Então vejo "* Dia sem planejamento para esta refeicao *"
    E o cursor volta ao campo daquele dia
    E nada é gravado

  Cenário: Refeição já lançada no pedido extra é recusada
    Dado que a refeição daquele segmento já está lançada no pedido extra
    Quando a tela procura o pedido extra
    Então vejo "* Refeicao cadastrada no pedido extra *"
    E o cursor volta ao primeiro dia com quantidade informada
    E nada é gravado

  Cenário: Inclusão grava os comensais de cada dia
    Dado um segmento da requisição com as refeições e as quantidades informadas por dia
    E que todas as conferências passaram
    Quando confirmo a inclusão
    Então a quantidade de cada dia fica gravada para aquela refeição e aquele segmento
    E a tela deixa a trilha de auditoria da gravação

  Cenário: Dia deixado em branco fica sem comensais
    Dado que a refeição já tinha quantidade num dia
    Quando deixo aquele dia em branco e confirmo a alteração
    Então aquele dia fica sem comensais gravados

  Cenário: Nada é gravado quando as quantidades são as mesmas
    Dado que a requisição já tem exatamente as quantidades informadas para aquela refeição
    Quando confirmo
    Então nada é gravado

  Cenário: Apagar os sete dias exclui a refeição do segmento
    Dado que a refeição tem comensais gravados nos sete dias
    Quando apago as sete quantidades e confirmo
    Então o registro de comensais daquela refeição é excluído
    E os pedidos extras lançados para os dias que tinham sobra daquela refeição também são excluídos

  Cenário: Refeição com sobra guarda também a sobra do dia
    Dado que a refeição está marcada como tendo sobra
    E que existe o cardápio de sobra daquele dia no cadastro de cardápios
    Quando a tela grava a refeição
    Então o cardápio de sobra e a quantidade de sobra do dia ficam gravados junto
    E a quantidade de sobra é a quantidade informada para o dia

  Cenário: Exclusão apaga os comensais do segmento
    Dado que o segmento tem comensais registrados naquela requisição
    Quando peço excluir
    Então os comensais daquele segmento são apagados
    E os registros de pedido extra daquele segmento também são apagados
    E a tela deixa a trilha de auditoria do que foi apagado

  Cenário: Exclusão do último segmento apaga a requisição do período
    Dado que o segmento excluído era o último com comensais naquela requisição
    Quando peço excluir
    Então os comensais daquele segmento são apagados
    E a requisição do período também é apagada

  Cenário: Não existem segmentos anteriores
    Dado que não existe cadastro nem comensais para o segmento anterior
    Quando peço o segmento anterior
    Então vejo "* Nao existem segmentos anteriores *"
    E o cursor volta ao campo do segmento anterior
    E nada é gravado

  Cenário: Vou para o segmento seguinte
    Dado que o órgão tem um segmento seguinte cadastrado
    Quando peço o segmento seguinte
    Então a tela recarrega os dados daquele segmento
    E nada é gravado

  Cenário: A tela passa para a E052T
    Dado que o fluxo continua no segmento seguinte
    Quando a tela encerra o seu trabalho
    Então sou encaminhado à tela E052T
    E ela abre na mesma cadeia, com a mesma origem e o mesmo segmento

  Cenário: Sem segmentos, a tela reabre a tela de cálculo em consulta
    Dado que a exclusão deixou o órgão sem nenhum segmento cadastrado
    Quando a tela encerra o seu trabalho
    Então o fluxo volta à tela de cálculo, em consulta
```
