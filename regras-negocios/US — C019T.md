# US — C019T — Incluir unidade da coordenação regional escolar

## Estória

Como **servidor da CRE que responde pelo cadastro das unidades da sua coordenadoria**, quero
**incluir uma unidade nova (o órgão filho SDI), informando a coordenação regional escolar e o
código do órgão e confirmando o nome que o sistema busca na base central**, para que **a unidade
passe a existir no cadastro da secretaria e possa receber, na tela seguinte e por quem cuida
dela, o endereço, os contatos, a classificação e as quantidades**.

A unidade da rede não nasce completa: primeiro ela precisa existir no cadastro, com o seu código
e a sua coordenação, para que as outras telas possam apontar para ela. É esta tela que faz a
unidade existir — e ela só a cria se o código já constar da base central do sistema, porque o
que se faz aqui é trazer para a secretaria uma unidade que já é reconhecida lá fora. Sem esse
registro não há como completar a unidade nem usá-la: o nome, a marca de ativação e a data de
entrada ficam gravados já na inclusão, e o resto do cadastro fica em branco, esperando a tela de
manutenção.

## Contexto

Jornada S000M → C000M → C200M → C019T.
Ator: servidor de CRE — inclui, para a coordenação regional escolar a que pertence, a unidade
(órgão filho SDI) que ainda não existe no cadastro.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**,
não regra de negócio. Os dois menus do caminho não gravam nada: só encaminham, e não deixam
registro nem origem na sessão.

O que esta tela usa do que veio antes é a **secretaria (o tipo de órgão), a coordenação regional
escolar, a matrícula, o código de acesso, o privilégio e a data do sistema** da sessão; isso é
regra da entrada e está no anexo de evidências, em **Regras que se revelaram da entrada**. O
**órgão filho do servidor**, que a entrada também carrega, **não** limita esta tela: o alcance
aqui é a coordenação, e a unidade que se inclui é a que o servidor informar.

Esta tela não muda de comportamento conforme quem a chamou: ela abre sempre do mesmo jeito e é
ela que decide como a **tela de cadastro do órgão filho** (`C020T`) abre depois (RN-09) — é por
esse caminho que a unidade incluída chega ao cadastro para ser completada.

## Regras de negócio

### RN-01 — A tela inclui uma unidade nova (órgão filho SDI) da coordenação regional escolar

A tela serve para incluir. O servidor informa a coordenação regional escolar e o código de uma
unidade (o órgão filho SDI) e o sistema cria o registro dessa unidade no cadastro, ligado à
secretaria e à coordenação da sessão. A unidade nasce aqui: as outras telas desta jornada leem e
completam o que esta cria, e nenhuma delas a cria de novo. A operação que esta tela executa é,
sempre, a inclusão.

### RN-02 — A única operação é incluir, e a permissão é conferida antes

A operação já vem preenchida como inclusão quando a tela abre, e não há outra que a tela execute.
Informada qualquer outra operação, a recusa é **\* Operacao nao disponivel. Use INC \***, com o
cursor de volta ao campo da operação e nada gravado. Antes disso a tela confere se o servidor tem
a **permissão de inclusão** para ela: sem essa permissão a operação não segue e nada é gravado.

### RN-03 — O órgão filho é obrigatório

O código da unidade tem de ser informado. Em branco, a recusa é **\* Informe o Orgao \***, com o
cursor de volta ao campo do órgão, e nada é conferido nem gravado.

### RN-04 — A coordenação regional escolar é obrigatória e tem de ser a do servidor

A coordenação vem preenchida com a do próprio servidor. Em branco, a recusa é
**\* Informe o grupo \***, com o cursor de volta ao campo. Quando o servidor tem coordenação na
sessão e informa outra, a recusa é **\* Usuario sem acesso a outro grupo \***, com o número da
coordenação dele na mensagem, e nada é gravado. Só quem **não** tem coordenação na sessão
informa uma coordenação qualquer sem passar por essa restrição.

### RN-05 — A unidade não pode já estar cadastrada

O código informado é procurado no cadastro das unidades antes de a inclusão seguir. Havendo já um
registro com aquele código — a procura é feita só pelo código da unidade, sem considerar a
secretaria nem a coordenação —, a recusa é **<- Orgao ja cadastrado \***, com o cursor de volta
ao campo do órgão e com a coordenação em que a unidade já está cadastrada na mensagem; nada é
gravado.

### RN-06 — O código tem de existir na base central, e o nome da unidade vem de lá

Aceito o código, o sistema consulta a base central (o SICI) com ele. Existindo a unidade lá, o
sistema traz o **nome** dela: é esse nome que o servidor vê a partir daí e é ele que fica
gravado — o servidor não digita o nome. Não existindo o código na base central, a recusa traz a
mensagem devolvida por aquela base e nada é gravado.

[?] Quando a base central não responde, a mensagem de erro da consulta **não** interrompe a tela:
o caminho segue para a pergunta de confirmação e, confirmada, a unidade é criada sem a
conferência de existência e sem que a base central tenha fornecido o nome — o nome fica em branco,
ou o da última unidade incluída na mesma sessão. Ou a falha deveria parar a tela, ou esse caminho
é inalcançável por outro motivo. Pergunta ao site.

### RN-07 — A inclusão só se conclui com a confirmação, e a confirmação é do que foi perguntado

Aceito o código e trazido o nome, a tela pergunta **\* Confirma inclusao do Orgao <S/N> ? \***,
com o cursor no campo da resposta. Só **S** deixa a inclusão seguir. Qualquer outra resposta —
em branco, "N" ou outra coisa — cancela: a pergunta desaparece, a tela volta a esperar os dados e
nada é gravado.

A confirmação fica presa à coordenação e à unidade que estavam na tela quando a pergunta foi
feita: se qualquer uma das duas mudar antes da resposta, a confirmação é descartada e nada é
gravado — o servidor precisa informar o par de novo e responder à pergunta outra vez.

### RN-08 — O que a inclusão grava

A unidade é criada com a **secretaria** e a **coordenação regional escolar** da sessão, com o
**código** que o servidor informou como órgão filho, com esse mesmo código como **órgão pai**,
com o **nome** trazido da base central, com a **data de entrada** (a data do sistema) e com a
marca de **não ativa**. A **operação** gravada no cadastro é a inclusão.

Todo o resto fica em branco ou zerado para a tela de cadastro completar (RN-09): endereço,
complemento, número do imóvel, extensão, bairro, código postal, pessoa de contato, os dois
telefones e o ramal, segmento de atendimento, tipo de apoio, marca de creche, unidade
orçamentária, marca de pedido acumulado, matriculados e comensais.

[?] A unidade é gravada como seu **próprio órgão pai** — o vínculo de subordinação nasce
apontando para ela mesma. O corpus não diz o que o órgão pai significa aqui nem se ele deveria
nascer com outra unidade. Pergunta ao site.

### RN-09 — Concluída a inclusão, o servidor é levado ao cadastro da unidade, que abre em alteração

Criado o registro, a tela entrega a unidade recém-criada à **tela de cadastro do órgão filho**
(`C020T`) e deixa registrado, na sessão, que a origem foi esta tela. É essa origem que faz a tela
seguinte abrir **em alteração**, com o registro criado já carregado, para o servidor completar o
endereço, os contatos, a classificação e as quantidades (RN-08). Sem essa passagem a unidade
ficaria criada e sem lugar para ser completada.

### RN-10 — A tela não muda conforme quem a chamou; ela é que decide a origem da seguinte

A tela não consulta de onde veio, e o menu que a abre não deixa registro nem origem na sessão:
ela abre sempre em inclusão, com a coordenação do servidor, e se comporta sempre do mesmo jeito.
A dependência da origem é da tela **seguinte**, não desta (RN-09).

Enquanto espera uma resposta, a tela reabre a si mesma: em cada recusa e na pergunta de
confirmação o servidor continua nesta tela, com o cursor no campo que precisa ser corrigido ou
respondido, e nada avança sem isso.

[?] A tela exibe e repassa adiante um campo de **tela anterior** que o menu não preenche; o
corpus não traz o rótulo que o servidor vê nesse campo nem o que ele deve fazer com ele. Pergunta
ao site.

### RN-11 — A tela grava um registro, e só ele

Dois cadastros estão ao alcance desta tela: o **cadastro do órgão filho** e o **cadastro dos
títulos das telas**. Só o cadastro do órgão filho recebe gravação — **um** registro, a criação da
unidade. O título é apenas lido, para a tela se identificar. Nenhum registro é apagado por esta
tela.

[?] A inclusão não deixa linha na **trilha de auditoria**, e nenhum outro ponto desta tela
produz uma; o rastro da mudança só aparece depois, na alteração feita na tela de cadastro. Se a
inclusão deveria deixar a sua própria linha, o corpus não diz. Pergunta ao site.

### RN-12 — Os dois códigos são conferidos como número antes de qualquer conferência de negócio

A coordenação regional escolar e o código da unidade passam por uma conferência numérica **antes**
das regras de negócio desta tela: texto informado em qualquer dos dois é recusado no próprio
campo, com o cursor nele, e nada é consultado por causa disso.

## Cenários BDD

```gherkin
Funcionalidade: Incluir a unidade (órgão filho SDI) da coordenação regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C019T

  Cenário: RN-01, RN-03 a RN-08 — incluir uma unidade nova
    Dado que estou na tela em inclusão, com a minha coordenação regional escolar preenchida
    E informo o código de uma unidade que existe na base central e ainda não está cadastrada
    Quando respondo S à pergunta de confirmação
    Então a unidade é criada no cadastro da secretaria, ligada à minha coordenação
    E o nome da unidade é o que veio da base central
    E a unidade fica marcada como não ativa, com a data do dia

  Cenário: RN-02 — operação diferente de incluir
    Quando informo uma operação que não é a inclusão
    Então vejo "* Operacao nao disponivel. Use INC *"
    E o cursor volta para o campo da operação
    E nada é gravado

  Cenário: RN-02 — sem permissão de inclusão
    Dado que não tenho permissão de inclusão nesta tela
    Quando confirmo
    Então a operação não segue
    E nada é gravado

  Cenário: RN-03 — órgão filho em branco
    Quando confirmo sem informar o código da unidade
    Então vejo "* Informe o Orgao *"
    E o cursor volta para o campo do órgão
    E nada é gravado

  Cenário: RN-04 — coordenação em branco
    Dado que apago a coordenação que veio preenchida
    Quando confirmo
    Então vejo "* Informe o grupo *"
    E o cursor volta para o campo da coordenação
    E nada é gravado

  Cenário: RN-04 — coordenação que não é a minha
    Dado que tenho coordenação regional escolar na sessão
    Quando informo uma coordenação diferente da minha
    Então vejo "* Usuario sem acesso a outro grupo *"
    E a mensagem traz o número da minha coordenação
    E nada é gravado

  Cenário: RN-04 — servidor sem coordenação informa uma
    Dado que o meu usuário não tem coordenação regional escolar
    Quando informo uma coordenação cadastrada
    Então a tela aceita a coordenação informada e segue a inclusão

  Cenário: RN-05 — unidade já cadastrada
    Quando informo o código de uma unidade que já existe no cadastro
    Então vejo "<- Orgao ja cadastrado *"
    E a mensagem traz a coordenação em que ela já está cadastrada
    E o cursor volta para o campo do órgão
    E nada é gravado

  Cenário: RN-06 — código que não existe na base central
    Quando informo o código de uma unidade que não existe na base central
    Então vejo a mensagem devolvida pela base central
    E nada é gravado

  Cenário: RN-06 — a consulta à base central não grava nada
    Dado que informo um código que existe na base central
    Quando a consulta à base central termina
    Então o nome da unidade é trazido para a tela
    E nenhum registro é gravado por causa da consulta

  Cenário: RN-07 — respondo que não à confirmação
    Dado que a tela já me perguntou se confirmo a inclusão
    Quando respondo N
    Então a pergunta desaparece e a tela volta a esperar os dados
    E nada é gravado

  Cenário: RN-07 — troco a unidade depois da pergunta
    Dado que a tela já me perguntou se confirmo a inclusão
    Quando troco o código da unidade e respondo S
    Então a confirmação é descartada
    E nada é gravado
    E preciso informar a unidade e responder de novo

  Cenário: RN-08 — o que fica gravado na unidade nova
    Dado que incluo uma unidade
    Quando a inclusão se conclui
    Então a unidade fica com a secretaria e a coordenação da sessão, com o código informado
    E fica com o nome vindo da base central, a data do dia e a marca de não ativa
    E o endereço, os contatos, a classificação e as quantidades ficam em branco ou zerados

  Cenário: RN-09 — a tela seguinte abre em alteração com a unidade carregada
    Dado que acabo de incluir uma unidade
    Quando sou levado à tela de cadastro do órgão filho
    Então ela abre em alteração
    E o registro recém-criado já está carregado para eu completá-lo

  Cenário: RN-10 — a tela reabre a si mesma enquanto espera
    Quando confirmo com um dado que a tela recusa
    Então continuo nesta tela, com a mensagem da recusa
    E o cursor fica no campo que precisa ser corrigido

  Cenário: RN-10 — a tela abre sempre do mesmo jeito
    Dado que chego a esta tela pela opção do menu de órgãos
    Então ela abre em inclusão
    E o formulário vem sem registro e com a coordenação da minha sessão

  Cenário: RN-11 — o que a tela grava
    Dado que incluo uma unidade
    Quando o sistema processa a inclusão
    Então só o cadastro do órgão filho recebe gravação
    E o cadastro dos títulos das telas é apenas lido
    E nenhum registro é apagado

  Cenário: RN-11 — a inclusão não deixa rastro na auditoria
    Dado que incluo uma unidade
    Quando a inclusão se conclui
    Então nenhuma linha nova aparece na trilha de auditoria por causa desta tela

  Cenário: RN-12 — código com texto
    Quando informo texto na coordenação ou no código da unidade
    Então o campo é recusado antes de qualquer conferência de negócio
    E o cursor fica no campo recusado
    E nada é consultado por causa dele
```
