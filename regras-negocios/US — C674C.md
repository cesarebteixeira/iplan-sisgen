# US — C674C — Consultar período de licitação pela data limite

## Estória

Como **servidor da CRE que responde pela vigência dos contratos da sua
coordenadoria regional escolar**, quero **consultar o período de licitação de um
tipo de contrato pela data limite dele, informando a coordenação, o dia, o mês e o
ano limite**, para que **eu encontre o período certo e o sistema me leve, já com
ele identificado, à tela onde a origem e o saldo inicial daquele período são
mantidos**.

O período de licitação é a vigência do contrato: é ele que diz de quando até
quando o contrato vale, e é por ele que o estoque inicial do gênero é registrado.
O servidor conhece o período pela data limite e pelo tipo de contrato, não por um
número de registro — esta tela é o que traduz esse conhecimento na identificação
do período. Sem ela, o servidor teria de abrir a tela de manutenção do período
sabendo de cor a coordenação, o tipo de contrato e os três números da data, e quem
não os decora não chega ao período. Nada aqui é gravado: o período é mantido na
tela que esta abre.

## Contexto

Jornada S000M → C000M → C050M → C670M → C674C.

Ator: servidor de CRE — consulta o período de licitação pela data limite e chega,
com o período identificado, à tela que o mantém.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e
menus.md`: é **dado de navegação**, não regra de negócio. O menu que abre esta
tela não grava nada: só encaminha.

A tela de destino é a **C674C**. O que ela usa do que veio antes é o **tipo de
órgão, a coordenação regional escolar da sessão, a matrícula, o privilégio e a
data do sistema**; isso é regra da entrada e está no anexo de evidências, em
**Regras que se revelaram da entrada**. O **órgão filho do servidor**, que a
entrada também carrega, **não** limita esta tela: aqui o alcance é a coordenação.

O que esta tela faz é uma passagem: o servidor identifica um período e a tela
**passa o registro do período** para a tela que o mantém, que **abre em consulta**
(RN-07). É por isso que a jornada termina aqui — quem continua o trabalho é a tela
seguinte.

## Regras de negócio

### RN-01 — A tela consulta o período de licitação pela data limite

Esta é uma tela de **consulta**. O servidor informa a **coordenação regional
escolar**, o **dia, o mês e o ano limite** do período e o **tipo de contrato**, e
a tela mostra o **nome da coordenação** e a **data do sistema** e busca, no
cadastro dos períodos, o período que casa com esses dados. Do período encontrado
a tela mostra, quando o cadastro os tiver, a **data de início da vigência**, a
**quantidade inicial do gênero**, o **código do fornecedor** e o **nome do
fornecedor**.

Nada nesta tela é gravado: nem o período, nem travamento de registro, nem linha
de auditoria. Os **códigos de sub-classe e de gênero** e o **tipo de contrato**
não aparecem na tela, mas fazem parte da identificação do período e são levados
com o registro para a tela seguinte.

[?] O campo **dia limite** é gravado e procurado como um dia do mês (de 1 a 31),
e o cadastro não diz se ele é o dia de vencimento do contrato ou um dia de corte
dentro do mês. O material lido não define o significado de negócio; pergunta ao
site.

### RN-02 — A tela só consulta; nenhuma outra operação passa

A tela se apresenta já na **consulta** — a operação que o servidor vê no campo da
operação é a de consulta — e repõe essa operação a cada exibição. Informar
inclusão, alteração ou exclusão é recusado com **\* Operacao nao disponivel \***,
com o cursor de volta ao campo da operação e nada consultado. Não há nesta tela
outra operação além de consultar.

[?] A tela recebe a operação de quem a chamou, e o material lido não mostra nenhum
caminho do sistema que a chame informando outra operação — o menu sempre chega com
o campo em branco. Ou a tela é chamada por um caminho que não está nesta jornada,
ou a recusa é inalcançável por aí. Pergunta ao site.

### RN-03 — O período se identifica pela coordenação, pelo tipo de contrato e pela data limite

Para dizer de qual período se trata, o servidor informa a **coordenação regional
escolar** (2 dígitos), o **dia limite** (2 dígitos), o **mês limite** (2 dígitos)
e o **ano limite** (4 dígitos), e ainda o **tipo de contrato** (3 dígitos), o
**código de sub-classe** (2 dígitos) e o **código de gênero** (5 dígitos). São
esses os dados que formam a identificação do período; sem todos eles não há como
dizer de qual período se fala, e o cadastro não tem outro caminho para encontrá-lo.

### RN-04 — Os códigos desta tela passam pela edição numérica

Cada um dos códigos e das grandezas da data é tratado como **número**: o que
estiver em branco vira zero, e o que não for número é recusado com a mensagem de
erro do sistema, com o cursor de volta ao campo — e o que não passa por essa
edição não chega a consultar o cadastro.

O campo em branco tem significado próprio numa grandeza: **dia limite em branco
vira zero**, e **sem o dia limite a tela não procura período nenhum** — ela fica
na espera, mostrando os dados do que foi informado, sem relacionar registro
algum. Nesse caso a data de início que o sistema conhece — a do dia de hoje — é
o que fica no lugar dos três números da data para efeito de identificação.

### RN-05 — O período tem de estar cadastrado

A consulta procura, no cadastro dos períodos, o registro que casa com o **tipo de
órgão e a coordenação** da sessão, com o **dia, o mês e o ano limite**, com o
**código de sub-classe**, o **código de gênero** e o **tipo de contrato**
informados. Não havendo esse registro, a recusa é **\* Periodo nao cadastrado \***
e nenhum período é identificado.

O cadastro dos períodos é lido por um índice que deixa de fora os registros
marcados como **excluídos**: um período excluído não é encontrado, e a consulta
responde como se ele nunca tivesse existido.

### RN-06 — A coordenação tem de estar cadastrada na secretaria do servidor

A coordenação informada é procurada no cadastro das coordenações da secretaria da
sessão. Não existindo — ou estando marcada como excluída — a recusa é
**\* Grupo nao cadastrado \***, com o cursor de volta ao campo da coordenação e
nada consultado. Antes disso, a coordenação em branco é recusada com
**\* Informe o grupo \***, e uma coordenação diferente da do servidor, quando ele
tem uma na sessão, com **\* Usuario sem acesso a este grupo \*** — as duas com o
cursor de volta ao mesmo campo.

### RN-07 — O período escolhido é entregue à tela seguinte, que abre em consulta

Encontrado o período, a tela entrega o **registro do período** — a coordenação, o
tipo de contrato, o dia, o mês e o ano limite, os códigos de sub-classe e de
gênero e a data de início — à **tela que mantém o período**, e essa tela abre em
**consulta**. O registro entregue é o do período consultado, de modo que a tela
seguinte já mostra os dados daquele período, e a tela seguinte fica sabendo que
veio desta: se lá o servidor tentar alterar ou procurar outro período, o sistema
o traz de volta para cá. A consulta não deixa registro travado nem linha de
auditoria.

### RN-08 — A consulta exige permissão para a tela

A tela confere, para o código de acesso do servidor, se ele tem o registro de
autorização desta tela, e sem esse registro não opera: nada é consultado. A tela
também não segue quando o campo de controle da tela anterior está preenchido — é
a tela de onde o servidor veio que volta a aparecer, e nada é consultado aqui.

## Cenários BDD

```gherkin
Funcionalidade: Consultar o período de licitação pela coordenação, pelo tipo de contrato e pela data limite

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C674C

  Cenário: RN-01 — consultar um período pela data limite
    Dado que informo a coordenação, o tipo de contrato, o dia, o mês e o ano limite de um período cadastrado
    Quando confirmo a consulta
    Então vejo o nome da coordenação e a data do sistema
    E vejo a data de início, a quantidade inicial e o fornecedor do período encontrado

  Cenário: RN-01 — consultar não deixa rastro
    Dado que informo um período cadastrado
    Quando a consulta termina
    Então nenhum registro é travado
    E nenhuma linha nova aparece na trilha de auditoria
    E o cadastro do período continua como estava

  Cenário: RN-02 — operação diferente de consulta
    Dado que informo inclusão, alteração ou exclusão no campo da operação
    Quando confirmo
    Então vejo "* Operacao nao disponivel *"
    E o cursor volta para o campo da operação
    E nada é consultado

  Cenário: RN-02 — a consulta é reposta a cada exibição
    Dado que a tela já está aberta em consulta
    Quando a tela é exibida de novo
    Então o campo da operação volta a mostrar a consulta

  Cenário: RN-03 — identificar o período pelo conjunto dos dados
    Dado que informo a coordenação, o tipo de contrato, o dia, o mês e o ano limite
    E informo o código de sub-classe e o código de gênero
    Quando confirmo a consulta
    Então o período procurado é o que casa com todos esses dados

  Cenário: RN-04 — campo numérico com texto
    Quando informo texto em um dos códigos ou em uma das grandezas da data
    Então o campo é recusado antes de qualquer consulta ao cadastro
    E o cursor volta para o campo
    E nada é consultado

  Cenário: RN-04 — dia limite em branco
    Dado que informo a coordenação e o tipo de contrato
    Quando confirmo a consulta sem informar o dia limite
    Então nenhum período é procurado
    E a tela continua na espera, mostrando o que foi informado

  Cenário: RN-05 — período não cadastrado
    Dado que informo uma coordenação cadastrada
    Quando confirmo uma combinação de tipo de contrato e data limite que não existe no cadastro
    Então vejo "* Periodo nao cadastrado *"
    E nenhum período é identificado

  Cenário: RN-05 — período marcado como excluído é tratado como inexistente
    Dado que o período que casa com os dados informados está marcado como excluído
    Quando confirmo a consulta
    Então vejo "* Periodo nao cadastrado *"
    E nenhum período é identificado

  Cenário: RN-06 — coordenação não informada
    Dado que deixo a coordenação em branco
    Quando confirmo a consulta
    Então vejo "* Informe o grupo *"
    E o cursor volta para o campo da coordenação
    E nada é consultado

  Cenário: RN-06 — coordenação diferente da minha
    Dado que tenho coordenação regional escolar na sessão
    Quando informo uma coordenação que não é a minha
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor volta para o campo da coordenação
    E nada é consultado

  Cenário: RN-06 — coordenação não cadastrada na minha secretaria
    Dado que informo uma coordenação que não existe para a minha secretaria
    Quando confirmo a consulta
    Então vejo "* Grupo nao cadastrado *"
    E o cursor volta para o campo da coordenação
    E nada é consultado

  Cenário: RN-06 — coordenação marcada como excluída
    Dado que informo uma coordenação marcada como excluída
    Quando confirmo a consulta
    Então vejo "* Grupo nao cadastrado *"
    E nada é consultado

  Cenário: RN-07 — o período encontrado é entregue à tela seguinte, em consulta
    Dado que informo um período cadastrado
    Quando confirmo a consulta
    Então a tela do período se abre em consulta
    E ela já mostra o período que eu consultei
    E nada foi gravado por esta tela

  Cenário: RN-07 — tentar alterar na tela seguinte devolve o servidor a esta consulta
    Dado que cheguei à tela do período vindo desta consulta
    Quando tento alterar o período lá
    Então o sistema me traz de volta para esta tela
    E a alteração não é registrada

  Cenário: RN-08 — sem autorização para a tela
    Dado que não tenho o registro de autorização desta tela para o meu código de acesso
    Quando confirmo a consulta
    Então a tela não opera
    E nada é consultado

  Cenário: RN-08 — controle da tela anterior preenchido
    Dado que o controle da tela anterior está preenchido
    Quando confirmo
    Então a tela anterior volta a aparecer
    E nada é consultado aqui
```
