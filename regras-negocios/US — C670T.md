# US — C670T — Solicitar a alteração do período do contrato por coordenação regional

## Estória

Como **servidor da coordenação regional de ensino (CRE)**, quero **pedir a alteração da
data-limite do período de um tipo de contrato e de um grupo de licitação da minha área**,
para que **a vigência passe a acompanhar o novo prazo, com o ofício que a motivou guardado
e o pedido entregue ao processamento que o aplica**.

O período é a faixa de datas que o sistema guarda por coordenação regional, tipo de
contrato e grupo de licitação — com uma data inicial e uma data-limite. É essa data-limite
que o sistema confronta com os pedidos já cadastrados: encurtá-la por baixo de um pedido
em vigor é o que a tela recusa. A alteração não acontece na hora: a tela confere o que foi
informado, pede a confirmação e entrega o pedido com a justificativa ao processamento, que
é quem altera o cadastro do período. Enquanto um pedido do relatório desta tela não
termina de ser processado, o sistema não aceita outro — é por isso que a alteração não
aparece no cadastro no instante em que o servidor a confirma.

## Contexto

Jornada S000M → C000M → C050M → C670T (4 passos).
Ator: servidor de CRE — informa a coordenação regional, o tipo de contrato, o grupo de
licitação e o período vigente, e pede a alteração da data-limite desse período.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Os dois passos do meio da jornada são **menus**: não gravam nada, não consultam cadastro
algum além do título da própria tela e **não deixam nada de seu** para esta tela — o que a
C670T usa vem da sessão, carregada na entrada. Nenhum deles encadeia a tela de destino: a
C670T não recebe registro nem operação de outra tela, e o modo de operação dela é decidido
por ela mesma, não por quem a chamou.

A jornada termina nesta tela: a C670T não abre outra — ela reabre a si mesma, e é por isso
que a navegação a registra como tela que reabre a própria tela.

As regras abaixo são só as desta tela; o que a leitura revelou pertencer à entrada está no
anexo de evidências.

## Regras de negócio

### RN-01 — A tela é de alteração, e só de alteração

Ao abrir, a tela repõe a **alteração** na operação, venha ela do menu ou de onde vier: a
operação não é escolhida por quem chama. Se a operação que chegou for outra — consulta,
inclusão, exclusão —, a recusa é **\* Opcao nao disponivel. Use ALT \***, com o cursor de
volta no campo da operação, e nada é lido e nada é gravado.

O comportamento da tela **não muda conforme a tela que a abriu**: o que a tela anterior
deixou é apenas repassado à rotina de rota, e nada nesta tela interrompe a conferência por
causa disso.

[?] A recusa manda usar **ALT**, mas o que a tela compara é o código interno da alteração
que o próprio sistema carrega. Ou o terminal traduz o que o servidor digita antes de
entregar, ou a mensagem ensina o que a guarda recusa. Pergunta ao site.

[?] As rotinas de rota, de segurança da tela e de data e hora só aparecem declaradas no
material, sem corpo: se alguma delas pode barrar a alteração, e com que aviso, não se lê
nesta jornada. A tela ainda se anuncia a elas como tela que mantém dados — marca que os
menus da jornada não usam —, e o que elas fazem com essa marca também não está no material.
Pergunta ao site.

### RN-02 — O que identifica o período, e o que é obrigatório

Para pedir a alteração, o servidor informa a **coordenação regional**, o **tipo de
contrato**, o **grupo de licitação** e as duas datas do período vigente — a **data
inicial** e a **data-limite**. A coordenação regional aceita **99**, que alcança todas as
coordenações do órgão; o grupo de licitação aceita **9999**, que alcança todos os
grupamentos; e o tipo de contrato é sempre um só.

Em branco, a coordenação regional não passa — a recusa é **\* Informe o grupo ou 99 para
todos \*** — e o grupo de licitação também não — a recusa é **\* Informe o grupamento ou
9999 para todos \***. As duas recusas devolvem o cursor ao campo que faltou.

Os códigos e as partes das datas passam pela edição numérica do sistema antes de qualquer
conferência: o que estiver em branco vira zero, os zeros à esquerda somem e o que não for
número é recusado, com o cursor de volta ao campo. O que não passa por essa edição não
chega a nenhuma consulta.

A coordenação regional informada **não é confrontada com a da sessão**: a tela aceita
qualquer coordenação cadastrada para o tipo de órgão do servidor, e também 99.

[?] Os campos desta tela não têm rótulo de negócio no material — os nomes que o próprio
programa usa para apontar o campo recusado são os nomes internos, e as datas aparecem sem
rótulo nenhum. Os nomes de negócio usados nesta estória (coordenação regional, data
inicial, data-limite, nova data-limite) são leitura de negócio, não transcrição. Pergunta
ao site.

[?] O texto da recusa por campo não numérico não está no fonte da tela: ele vem da rotina
de edição, que o material só declara. O que o servidor lê nesse caso não pôde ser
conferido. Pergunta ao site.

[?] Se um servidor de uma coordenação regional pode pedir a alteração de outra — a tela
aceita —, o material desta jornada não decide: a rotina de segurança, que poderia
restringi-la, não tem corpo no material. Pergunta ao site.

### RN-03 — O período tem de estar cadastrado

Conferidos os campos, a tela procura o **período** pela coordenação regional (ou por todas,
quando 99), pelo tipo de contrato, pela data-limite informada e pelo grupo de licitação (ou
por todos, quando 9999), e exige que a **data inicial** registrada no período seja a data
inicial informada. Não achando, a recusa é **\* Periodo nao cadastrado \***, com o cursor
de volta no campo da data-limite, e nada é gravado.

[?] Com 99, a tela percorre as coordenações do órgão e adota o **primeiro** período que
encontra, mandando o pedido com a coordenação 99 no bloco entregue ao processamento; se as
coordenações do alcance tiverem períodos diferentes para o mesmo tipo de contrato e
grupamento, o material desta jornada não diz qual deles a alteração alcança. Pergunta ao
site.

### RN-04 — A nova data-limite e os seus limites

A **nova data-limite** tem de ser uma data que o sistema aceite, com o **ano entre 1994 e
2099**; fora disso, a recusa é **\* Nova Data final invalida \***, com o cursor de volta no
campo da nova data-limite.

Ela também não pode ser **anterior à data inicial do período**: nesse caso a recusa é
**\* Data inicial maior que data final \***, com o cursor no mesmo campo.

Há ainda um **teto**: a nova data-limite não pode passar do máximo que o sistema admite a
partir da data inicial do período — para obter esse máximo o sistema soma **2 190** à data
inicial. Passando, a recusa é **<- Maior data limite permitida \***, com a data máxima na
frente da mensagem e o cursor de volta no campo da nova data-limite.

[?] O teto só é conferido quando a data-limite vigente do período já é diferente da
data-limite inicial dele; coincidindo as duas, a nova data-limite passa sem esse teto. Por
que a primeira alteração não é limitada, o material não explica. Pergunta ao site.

[?] O que os 2 190 representam não está declarado no material: se a unidade for o dia, são
seis anos. A rotina que faz a conta é do ambiente de execução e não tem corpo nos fontes.
Pergunta ao site.

### RN-05 — A nova data inicial é a própria data inicial informada

A tela repõe o par da **nova data inicial** com a data inicial que o servidor informou para
o período vigente: o que ele digitar no par novo é substituído, e é a data inicial
informada que vai no pedido. Depois disso, a tela confere que a nova data inicial não é
maior que a nova data-limite.

[?] Se os dois pares de datas servem para o servidor conferir o que está vigente, ou se o
sistema simplesmente ignora o que ele digita no par novo, o material não diz — o par novo
é sempre reescrito com o par informado. Pergunta ao site.

### RN-06 — A impressora é obrigatória

A **impressora** faz parte do pedido: é nela que o relatório da alteração é impresso, e é
por ela que o pedido chega à fila. Em branco, a recusa é **\* Informe a impressora \***,
com o cursor de volta no campo da impressora, e nada é gravado.

### RN-07 — Nenhum pedido em vigor pode passar da nova data-limite

Antes de pedir a confirmação, a tela percorre os **pedidos** da coordenação regional — a
partir de **dez dias antes da nova data-limite** — e, para cada pedido cuja data-limite
seja **posterior à nova data-limite**, confere se algum item dele é do **tipo de contrato**
informado e, quando o grupo informado não é 9999, do **mesmo grupamento**. Achando, a
recusa é **<- Grupo/Pedido nesta data \***, com a coordenação e o número do pedido na
frente da mensagem e o cursor de volta no campo da nova data-limite, e nada é gravado.

[?] De onde vêm os dez dias antes da nova data-limite — prazo de antecedência, janela de
segurança ou regra do contrato — o material não diz. A conferência só percorre os pedidos
que começam dessa data em diante: um pedido que comece antes da janela e termine depois da
nova data-limite não é visto por ela. Pergunta ao site.

### RN-08 — O motivo da atualização é obrigatório

O pedido tem de levar o **motivo da atualização** — o ofício que a autoriza. Em branco, a
recusa é **\* Informe o motivo da atualizacao \***, com o cursor de volta no campo do
motivo, e nada é gravado.

### RN-09 — A alteração só segue com a confirmação do servidor

Passando por todas as conferências, a tela guarda os campos informados, **repõe os campos
como estavam** e pede a confirmação: **\* Confirma alteracao do periodo <S/N> ? \***, com
o cursor no campo da confirmação. Nessa passagem **nada é gravado** — a tela apenas pede a
marca.

Só a marca **afirmativa** leva o pedido adiante. E a confirmação vale para os campos que
foram guardados: se, entre o pedido de confirmação e a marca, algum dos campos guardados
mudar — a coordenação regional, as datas do período, a nova data-limite, o tipo de
contrato, o grupo de licitação ou o motivo —, a tela esquece a confirmação anterior,
confere tudo de novo e volta a pedir a confirmação. A marca negativa, ou ausente, para o
pedido sem gravar nada.

### RN-10 — Enquanto houver requisição do relatório em processamento, não se altera

Confirmada a alteração, a tela procura uma **requisição do relatório da alteração de
período** já registrada. Havendo, a recusa é **\* Relatorio em processamento. Aguarde. \***,
com o cursor de volta no campo da confirmação, e nada é gravado.

[?] A procura olha **só o código do relatório**: uma requisição pendente de qualquer
origem, de qualquer coordenação regional, bloqueia o pedido desta tela. E a própria tela
registra a requisição com esse mesmo código; se o processamento não apagar a requisição ao
terminar, a alteração seguinte seria recusada por essa guarda. O material desta jornada não
mostra quem apaga a requisição — nem se alguém a apaga. Pergunta ao site.

### RN-11 — O que a tela grava, o que ela entrega e o que ela não altera

Confirmada a alteração, a tela **não altera o cadastro do período**. O que ela deixa é:

- a **trilha de auditoria** da operação, com a identificação do novo período, a matrícula e
  a coordenação regional do servidor, a estação, a data e a hora da sessão e um número de
  processo;
- a **requisição do relatório** da alteração de período, numerada na sequência do cadastro
  de requisições, com a data da sessão, a matrícula, a estação e o tipo de órgão do
  servidor.

E entrega ao **processamento** o bloco com o novo período (coordenação regional, tipo de
contrato, tipo de licitação, grupo de licitação, datas e ofício), junto com a impressora, o
número de cópias (uma), a estação de trabalho e o **e-mail do servidor**. Encerrada a
gravação, a tela mostra **\* Cadastro sendo atualizado \*** e volta a ser apresentada.

[?] A trilha registra a operação com a marca de **inclusão**, e não com a de alteração, e
guarda a identificação do novo período no bloco do valor anterior, deixando o bloco do
valor posterior em branco. Se é essa a trilha pretendida para uma alteração, o material não
diz. Pergunta ao site.

[?] O número da requisição sai do maior número já registrado no cadastro de requisições mais
um; se a leitura não achar nenhum, o material não diz com que número o pedido sai. E a
impressora e a coordenação regional **não** vão nos campos próprios da requisição — seguem
apenas no bloco entregue ao processamento: se a fila reprocessar a requisição sem esse
bloco, a impressora pode faltar. Pergunta ao site.

[?] O que o processamento faz com o pedido — como altera o período, onde registra o ofício
e se apaga a requisição da fila — não está nesta jornada: a tela apenas entrega o pedido e
não escreve no cadastro do período. Pergunta ao site.

### RN-12 — O que a tela mostra

A tela reexibe os campos informados. O **tipo de licitação** que ela mostra é o do
**período cadastrado**, e não o que o servidor tenha digitado; a **descrição do tipo de
contrato** e a **descrição do tipo de licitação** vêm dos cadastros, pelo código que o
período guarda. No cabeçalho, a tela mostra a **descrição do órgão** e a **data do
sistema**, ambas da sessão.

### RN-13 — A jornada termina nesta tela

Esta tela não passa registro nem operação para nenhuma outra: a única tela que ela abre é
ela mesma. Depois da confirmação e depois da gravação, ela volta a ser apresentada com a
mensagem daquele momento, e é por isso que esta jornada termina neste passo e não tem
saída.

## Cenários BDD

```gherkin
Funcionalidade: Solicitar a alteração do período do contrato por coordenação regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C670T

  Cenário: RN-01 — a tela abre no modo de alteração
    Dado que venho do menu C050M
    Quando a tela C670T abre
    Então ela abre com a alteração na operação
    E o cabeçalho traz a descrição do órgão e a data do sistema
    E nada é gravado

  Cenário: RN-01 — operação diferente da alteração
    Dado que estou na tela C670T
    Quando a operação que chegou não é a de alteração
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor volta para o campo da operação
    E nada é lido e nada é gravado

  Cenário: RN-02 — identificar o período com todos os campos
    Dado que informo a coordenação regional, o tipo de contrato, o grupo de licitação, a data inicial e a data-limite de um período cadastrado
    Quando confirmo a transação
    Então a tela admite a identificação e segue para as conferências
    E nada é gravado nessa passagem

  Cenário: RN-02 — coordenação regional não informada
    Dado que estou na tela C670T
    Quando deixo a coordenação regional em branco
    Então vejo "* Informe o grupo ou 99 para todos *"
    E o cursor volta para o campo da coordenação regional
    E nada é gravado

  Cenário: RN-02 — grupo de licitação não informado
    Dado que estou na tela C670T
    Quando deixo o grupo de licitação em branco
    Então vejo "* Informe o grupamento ou 9999 para todos *"
    E o cursor volta para o campo do grupo de licitação
    E nada é gravado

  Cenário: RN-02 — campo não numérico
    Dado que estou na tela C670T
    Quando informo letra em um dos códigos ou em uma das partes das datas
    Então a edição numérica recusa o campo
    E o cursor volta para o campo recusado
    E nada é consultado e nada é gravado

  Cenário: RN-02 — 99 e 9999 alcançam todas as coordenações e todos os grupamentos
    Dado que estou na tela C670T
    Quando informo 99 na coordenação regional, 9999 no grupo de licitação e os demais campos de um período cadastrado
    Então a tela procura o período em todas as coordenações do meu órgão e em todos os grupamentos
    E o pedido segue com o que foi informado

  Cenário: RN-03 — período não cadastrado
    Dado que não existe período para a coordenação regional, o tipo de contrato, o grupo de licitação e a data-limite informados
    Quando confirmo a transação
    Então vejo "* Periodo nao cadastrado *"
    E o cursor volta para o campo da data-limite
    E nada é gravado

  Cenário: RN-04 — a nova data-limite fora do calendário aceito
    Dado que o período está cadastrado
    Quando informo uma nova data-limite que o sistema não aceita como data
    Então vejo "* Nova Data final invalida *"
    E o cursor volta para o campo da nova data-limite
    E nada é gravado

  Cenário: RN-04 — a nova data-limite acima do teto
    Dado que o período está cadastrado e a data-limite vigente já é diferente da data-limite inicial do período
    Quando informo uma nova data-limite maior que o máximo permitido a partir da data inicial
    Então vejo "<- Maior data limite permitida *", com a data máxima na frente
    E o cursor volta para o campo da nova data-limite
    E nada é gravado

  Cenário: RN-04 — a nova data-limite antes da data inicial
    Dado que o período está cadastrado
    Quando informo uma nova data-limite anterior à data inicial do período
    Então vejo "* Data inicial maior que data final *"
    E o cursor volta para o campo da nova data-limite
    E nada é gravado

  Cenário: RN-05 — a nova data inicial é reposta pela data inicial informada
    Dado que o período está cadastrado
    Quando informo uma data qualquer no campo da nova data inicial
    Então a tela segue com a data inicial do período no lugar do que digitei
    E é essa data que vai no pedido

  Cenário: RN-06 — impressora não informada
    Dado que o período está cadastrado
    Quando deixo a impressora em branco
    Então vejo "* Informe a impressora *"
    E o cursor volta para o campo da impressora
    E nada é gravado

  Cenário: RN-07 — pedido em vigor que passa da nova data-limite
    Dado que existe pedido da mesma coordenação regional, com a data-limite posterior à nova data-limite, e um item dele é do mesmo tipo de contrato e do mesmo grupamento
    Quando confirmo a transação
    Então vejo "<- Grupo/Pedido nesta data *", com a coordenação e o número do pedido na frente
    E o cursor volta para o campo da nova data-limite
    E nada é gravado

  Cenário: RN-07 — nenhum pedido em vigor passa da nova data-limite
    Dado que o período está cadastrado e nenhum pedido daquela coordenação regional passa da nova data-limite
    Quando confirmo a transação
    Então a tela segue para o pedido do motivo da atualização
    E nada é gravado nessa passagem

  Cenário: RN-08 — motivo da atualização não informado
    Dado que o período está cadastrado e as datas conferem
    Quando deixo o motivo da atualização em branco
    Então vejo "* Informe o motivo da atualizacao *"
    E o cursor volta para o campo do motivo
    E nada é gravado

  Cenário: RN-09 — a tela pede a confirmação e não grava nada
    Dado que informei um período cadastrado, a nova data-limite, a impressora e o motivo
    Quando confirmo a transação
    Então vejo "* Confirma alteracao do periodo <S/N> ? *"
    E os campos informados voltam como estavam
    E nada é gravado

  Cenário: RN-09 — a alteração segue com a confirmação afirmativa
    Dado que vi o pedido de confirmação
    Quando marco a confirmação com S
    Então a alteração é entregue ao processamento
    E o cadastro do período ainda não está alterado

  Cenário: RN-09 — a confirmação é descartada quando os campos mudam
    Dado que vi o pedido de confirmação
    Quando mudo a nova data-limite ou o motivo e marco a confirmação
    Então a tela esquece a confirmação anterior
    E confere tudo de novo
    E volta a pedir a confirmação
    E nada é gravado

  Cenário: RN-10 — requisição do relatório em processamento
    Dado que existe requisição do relatório da alteração de período ainda não processada
    Quando marco a confirmação com S
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor volta para o campo da confirmação
    E nada é gravado

  Cenário: RN-11 — o pedido é registrado e o processamento é disparado
    Dado que o período está cadastrado, as datas conferem, nenhum pedido passa da nova data-limite e não há requisição pendente
    Quando marco a confirmação com S
    Então a tela registra a requisição do relatório e a trilha de auditoria
    E entrega ao processamento o novo período com a impressora, uma cópia, a estação e o meu e-mail
    E vejo "* Cadastro sendo atualizado *"
    E a tela volta a ser apresentada

  Cenário: RN-11 — a tela não altera o cadastro do período
    Dado que a alteração foi confirmada e o pedido foi registrado
    Quando o processamento ainda não rodou
    Então o cadastro do período continua com a data-limite antiga
    E o que a tela gravou foi a requisição do relatório e a trilha de auditoria

  Cenário: RN-12 — o que a tela mostra do período
    Dado que o período está cadastrado
    Quando informo a identificação do período
    Então o tipo de licitação mostrado é o do período cadastrado, e não o que digitei
    E vejo a descrição do tipo de contrato e a do tipo de licitação, vindas dos cadastros
    E o cabeçalho traz a descrição do órgão e a data do sistema

  Cenário: RN-13 — a jornada termina na tela
    Dado que a alteração foi entregue ao processamento
    Quando a transação termina
    Então a tela reabre a si mesma
    E não abre nenhuma outra tela
```
