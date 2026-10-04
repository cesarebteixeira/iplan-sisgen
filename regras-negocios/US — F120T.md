# US — F120T — Manter instituições beneficentes da CRE

## Estória

Como **servidor de CRE**, quero **manter o cadastro da instituição beneficente — o código
INEP, o CNPJ dela e o da mantenedora, o nome, o endereço, o número do imóvel e o bairro —
dentro da minha coordenadoria regional escolar**, para que **cada instituição beneficente
fique identificada e endereçada no sistema e as notas fiscais e os convênios dela possam
existir**.

É este cadastro que dá identidade à instituição beneficente: sem ele não há a quem
vincular nota fiscal nem convênio, e o nome, o endereço e o bairro não têm procedência.
É também daqui que sai a mantenedora — quando o CNPJ dela ainda não existe, é esta tela
que o cria, com o nome da própria instituição. E é a coordenadoria guardada aqui que
decide a que grupo pertencem a nota e o convênio daquela instituição.

## Contexto

Jornada S000M → F000M → F100M → F120T (4 passos).
Ator: servidor de CRE — cadastra, altera, exclui e consulta as instituições beneficentes
da sua coordenadoria regional escolar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As duas telas anteriores da jornada são **menus** e só encaminham: não deixam registro nem
operação para a `F120T`. O que a `F120T` usa do que veio antes é o **tipo de órgão (a
secretaria)** e a **coordenadoria regional escolar (o grupo)** da sessão, além da matrícula,
do código de acesso e do privilégio; essa é regra da entrada e está no anexo de evidências,
em **Regras que se revelaram da entrada**.

A `F120T` também é alcançada **encadeada**, sem passar por menu: é assim que a consulta que
lista as instituições de uma coordenadoria a abre. Não é a mesma coisa chegar pelo menu ou
chegar por essa consulta — **o comportamento de abertura é decidido por quem a chamou**
(RN-03) —, e uma abertura que não traz a instituição escolhida não falha: só obriga o
servidor a redigitar tudo. A tela também encadeia na outra direção, e reabre a si mesma
(RN-04 e RN-15).

---

## Regras de negócio

### RN-01 — A tela mantém a instituição beneficente da coordenadoria

Para uma instituição beneficente, a tela guarda o **código INEP** (8 dígitos), a
**coordenadoria regional escolar** (2 dígitos), o **CNPJ da instituição** e o **CNPJ da
mantenedora** (14 posições cada), o **nome** e o **endereço** (40 posições cada), o
**número do imóvel** (5 dígitos) e o **código do bairro** (3 dígitos). No alto, mostra a
**descrição do tipo de órgão da sessão** e a **data do sistema**; ao lado do código do
bairro, o **nome do bairro**; ao lado do CNPJ da mantenedora, o **nome da mantenedora**.

[?] A descrição do tipo de órgão e a data do sistema que a tela mostra são preenchidas pelo
ambiente, e não pela tela: no acervo lido elas só aparecem sendo inicializadas em branco. A
descrição tem origem na entrada, que a lê do cadastro de tipos de órgão, mas o trecho do
ambiente que a transporta não está no acervo lido. Pergunta ao site.

### RN-02 — A tela abre em inclusão e conhece quatro operações

A operação é informada num campo próprio da tela, e são quatro: **inclusão**, **alteração**,
**exclusão** e **consulta**. Qualquer outro valor é recusado com **\* Opcao nao disponivel.
Use INC, ALT, EXC ou CON \***, com o cursor devolvido ao campo da operação, e a tela não
segue. Quando o campo chega em branco — é o caso da abertura da tela pelo menu —, o sistema
o preenche com a **inclusão**.

[?] A mensagem de recusa nomeia as operações como INC, ALT, EXC e CON, e a conferência do
que a tela aceita trabalha com outro jogo de códigos internos. Se a máscara da tela traduz
um jogo no outro, ou se o texto da mensagem saiu trocado, não está no acervo lido. Pergunta
ao site.

### RN-03 — Como a tela abre depende de quem a chamou

Quando quem abre a `F120T` é a `F120C` — a consulta que lista as instituições beneficentes
de uma coordenadoria —, a tela abre com a instituição escolhida **já carregada**: o código
INEP, a coordenadoria, os dois CNPJs, o nome, o endereço, o número do imóvel, o código e o
nome do bairro e o nome da mantenedora. Quando quem abre é o menu, a tela abre **sem nenhum
dado de instituição**: o servidor digita o código e os demais campos.

A diferença não está em campo nenhum da `F120T`: ela vem de a tela conferir **qual tela a
chamou**, na área de trabalho que a sessão transporta. E o efeito de errar essa origem é
silencioso — uma abertura em branco onde deveria vir a instituição escolhida não falha, só
obriga a redigitar tudo.

### RN-04 — A tela encaminha para a consulta quando recebe o indicador preenchido

A tela recebe um **indicador de uma posição**. Chegando em branco ou com **"N"**, ela segue
o cadastro normalmente. Chegando com **qualquer outro valor**, ela não segue: passa adiante
o **código da coordenadoria em uso** e pede a tela `F120C`, a consulta que lista as
instituições daquela coordenadoria. O que ela entrega é apenas a coordenadoria — a operação
em uso não vai junto.

[?] O programa só escreve "N" nesse indicador, e toda abertura da tela o repõe em "N";
nenhum outro ponto do acervo lido o preenche. Ou o valor chega de fora — da máscara da tela
ou de quem a chamou —, ou esse encaminhamento é inalcançável para o servidor. Pergunta ao
site.

### RN-05 — O código INEP identifica a instituição e não se repete

Na inclusão, o código INEP é obrigatório: em branco, a tela recusa com **\*Informe o INEP da
instituicao beneficente \*** e devolve o cursor ao campo. Informado, ele é procurado no
cadastro de instituições beneficentes: já havendo instituição com aquele código, a inclusão
é recusada com **\* Instituicao beneficente ja cadastrada \***.

### RN-06 — O código INEP tem piso

Na inclusão, o código INEP tem de ser **igual ou maior que 30.000.000**; abaixo disso, a
tela recusa com **\* INEP invalido \*** e devolve o cursor ao campo.

[?] O que o piso de 30.000.000 significa — faixa reservada, primeiro dígito do código, ou
erro do próprio cadastro — não está no acervo lido. Pergunta ao site.

### RN-07 — A instituição pertence à coordenadoria do servidor

A coordenadoria é obrigatória: em branco, a recusa é **\* Informe o grupo \***. Com
coordenadoria na sessão, informar outra é recusado com **\* Usuario sem acesso a outro grupo
\***. A coordenadoria informada também tem de estar **cadastrada** para o tipo de órgão da
sessão: não estando, ou estando marcada como excluída, a recusa é **\* Grupo nao cadastrado
\***. Na abertura da tela, o campo da coordenadoria já vem preenchido com a coordenadoria do
servidor, quando ela existe na sessão.

[?] Sem coordenadoria na sessão, a tela aceita qualquer coordenadoria cadastrada —
inclusive uma que não é a do servidor. Se o cadastro de autorizações já limita isso, ou se a
conferência depende de a sessão trazer a coordenadoria, o acervo lido não determina.
Pergunta ao site.

### RN-08 — Nome, endereço e bairro são obrigatórios, e o bairro tem de estar cadastrado

Na inclusão e na alteração: sem **nome**, a recusa é **\* Informe o nome da
inst.beneficente \***; sem **endereço**, **\* Informe o endereco da inst.beneficente \***;
com o **código do bairro** em branco, **\* Informe o codigo do bairro da inst.beneficente
\***. Informado o código do bairro, ele é procurado no cadastro de bairros; não existindo, a
recusa é **\* Bairro nao cadastrado \***.

### RN-09 — O CNPJ é obrigatório e passa pela conferência dos dígitos

Na inclusão e na alteração, o **CNPJ da instituição** e o **CNPJ da mantenedora** passam
pela conferência dos dígitos verificadores; o que não passa é recusado com **\* CNPJ
invalido \***, com o cursor no campo daquele CNPJ. CNPJ em branco não é conferido. Dos dois,
pelo menos um tem de ser informado: com os dois em branco, a tela avisa **\* Informe o CNPJ
da inst.benef ou da mantenedora \*** e devolve o cursor ao CNPJ da instituição.

[?] Esse é o único aviso da tela que **não** interrompe o caminho: depois dele o programa
continua as demais conferências e chega ao ponto de gravação como se nada tivesse
acontecido. Se o aviso sozinho basta para barrar a gravação, ou se a inclusão com os dois
CNPJs em branco chega a ser gravada, o acervo lido não determina — a rotina que emite a
mensagem não está nele. Pergunta ao site.

### RN-10 — O CNPJ da instituição não pode ser de outra instituição nem de uma mantenedora

Informado o CNPJ da instituição, ele é procurado no cadastro de instituições beneficentes:
pertencendo a **outra** instituição, a recusa é **<- CNPJ cadastrado para outro INEP \***,
com o código INEP que já o usa à frente da mensagem. Na alteração, o CNPJ da **própria**
instituição é aceito. O mesmo CNPJ também é procurado no cadastro de mantenedoras: estando
lá, a recusa é **\* CNPJ de Mantenedora \***.

### RN-11 — Mantenedora ainda não cadastrada é criada com o nome da instituição

Informado o CNPJ da mantenedora, ele é procurado no cadastro de mantenedoras. Não havendo
registro com aquele CNPJ, o sistema **cadastra a mantenedora na hora**, com a razão social
igual ao **nome da instituição beneficente** que está sendo mantida. Havendo, nada é criado
e a mantenedora existente é a usada.

[?] A criação da mantenedora é gravada sob uma condição de estado cujo valor ("DATA") não
está explicado no acervo nem no manual; quando ela não se confirma, a tela apenas remonta o
registro e segue. Se existe caso em que a mantenedora é criada sem essa confirmação, ou em
que a criação é descartada, é pergunta ao site.

### RN-12 — Alterar, excluir e consultar exigem a instituição cadastrada, no mesmo órgão e na mesma coordenadoria

Fora da inclusão, o código INEP é procurado no cadastro de instituições beneficentes; não
existindo, a recusa é **\* Instituicao beneficente nao cadastrada \***. Existindo, a
instituição tem de ser **do tipo de órgão da sessão**: sendo de outro, a recusa é **\*
Inst.beneficente cad. em outra secretaria \***. E a coordenadoria da instituição tem de ser
a **do servidor**: sendo de outra, a recusa é **<- Usuario sem acesso ao grupo desta
Inst.benef. \***, com o código da coordenadoria à frente da mensagem.

### RN-13 — A exclusão é recusada quando a instituição tem convênios ou notas fiscais

Antes de excluir, a tela procura os **convênios** da instituição e as **notas fiscais**
dela: havendo convênio, a recusa é **\* Ja existem convenios cadastrados \***; havendo nota
fiscal, **\* Ja existem notas cadastradas \***. A exclusão só passa quando a instituição não
tem nem um nem outro.

### RN-14 — Trocar a coordenadoria leva junto as notas fiscais e os convênios

Na alteração, se a coordenadoria informada é **diferente** da que a instituição tem gravada,
o sistema movimenta o que estava preso à coordenadoria antiga: as **notas fiscais** da
instituição e os **itens de gênero** de cada nota passam a apontar para a coordenadoria nova,
e os **convênios anuais** da instituição na coordenadoria antiga são apagados e recriados na
coordenadoria nova. Cada registro movimentado deixa o seu próprio rastro de auditoria. Não
havendo mudança de coordenadoria, nada disso acontece: a alteração grava só a instituição.

[?] A varredura das notas fiscais não se limita à coordenadoria antiga — ela vai por órgão e
instituição —, de modo que notas da instituição lançadas em outra coordenadoria também
passam para a nova. A varredura dos convênios, essa, é delimitada pela coordenadoria antiga.
Se a diferença é intencional, o acervo lido não determina. Pergunta ao site.

### RN-15 — A consulta mostra a instituição e não grava nada

Em consulta, a tela carrega a instituição informada — o código INEP, a coordenadoria, os
dois CNPJs, o nome, o endereço, o número do imóvel e o código do bairro —, busca o **nome do
bairro** no cadastro de bairros e o **nome da mantenedora** no cadastro de mantenedoras, e
**reabre a própria tela** com esses dados à mostra. Nenhum registro é gravado, nenhum é
travado e nenhuma linha vai para a auditoria.

### RN-16 — Toda operação efetiva deixa registro na auditoria

Inclusão, alteração e exclusão gravam um registro de **auditoria** com a operação (inclusão,
alteração ou exclusão), o **cadastro alterado**, o **teor do registro antes e depois** (300
posições cada), o código INEP da instituição, a coordenadoria, a matrícula do servidor, o
terminal e a data e a hora da sessão. Na inclusão, o "antes" sai em branco e o "depois" é a
instituição gravada; na exclusão, o "antes" é a instituição apagada e o "depois" sai em
branco; na alteração, o "antes" é o que estava gravado e o "depois" é o que foi gravado.

A troca de coordenadoria gera um registro de auditoria **por registro movimentado**, além do
da própria instituição. A consulta não gera auditoria nenhuma — ela não grava.

[?] O campo de tipo de manutenção do registro de auditoria recebe sempre "A", nas três
operações; a distinção entre elas fica no campo de operação. Se o site espera outra letra na
exclusão, é pergunta ao site.

### RN-17 — Nada é lido nem gravado sem a conferência de acesso, de rota e de permissão

Antes de qualquer conferência de campo, a tela passa pela **rota** e pela **segurança**: a
tela tem de estar autorizada para o tipo de órgão, a matrícula tem de ter o código de acesso
àquela tela e a **operação em uso** tem de estar liberada para ela. Não estando, a mensagem
sai das rotinas comuns — **\* Acesso negado para esta matricula \***, **\* Acesso negado para
esta operacao \***, **\* Tela nao disponivel \*** ou **\* Tela nao cadastrada \*** — e nada é
gravado. Na abertura da tela a mesma segurança de tela é conferida; se ela recusar, a
transação é abandonada.

[?] A conferência de permissão usa a operação que o campo da tela traz, e a tela só aceita
quatro operações; se o cadastro de autorizações não tiver a permissão correspondente, toda
operação é recusada e a tela vira consulta. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter o cadastro das instituições beneficentes da coordenadoria regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F120T

  Cenário: Inclusão de uma instituição beneficente
    Dado que estou na F120T com a operação de inclusão
    Quando informo o código INEP, a minha coordenadoria, o nome, o endereço, o número do imóvel, o código do bairro e um CNPJ válido
    Então a instituição beneficente fica cadastrada
    E a inclusão deixa registro na auditoria

  Cenário: Alteração de uma instituição beneficente já cadastrada
    Dado que estou na F120T com a operação de alteração
    E informo o código INEP de uma instituição já cadastrada no meu órgão e na minha coordenadoria
    Quando corrijo o nome, o endereço ou o número do imóvel
    Então o cadastro fica atualizado
    E a alteração deixa registro na auditoria, com o teor anterior e o novo

  Cenário: Exclusão de uma instituição beneficente sem convênios nem notas fiscais
    Dado que estou na F120T com a operação de exclusão
    E informo o código INEP de uma instituição já cadastrada que não tem convênios nem notas fiscais
    Quando confirmo a exclusão
    Então a instituição beneficente é apagada do cadastro
    E a exclusão deixa registro na auditoria

  Cenário: Consulta de uma instituição beneficente
    Dado que estou na F120T com a operação de consulta
    Quando informo o código INEP de uma instituição já cadastrada
    Então a tela se reabre mostrando os dados daquela instituição
    E o nome do bairro e o nome da mantenedora aparecem
    E nada é gravado

  Cenário: Operação não disponível
    Dado que estou na F120T
    Quando informo uma operação que não é inclusão, alteração, exclusão nem consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E o cursor volta para o campo da operação
    E nada é gravado

  Cenário: Abertura pelo menu não traz instituição nenhuma
    Quando abro a F120T pela opção do menu
    Então a tela abre sem nenhum dado de instituição
    E o campo da operação vem preenchido com a inclusão

  Cenário: Abertura pela consulta traz a instituição escolhida
    Dado que escolhi uma instituição na consulta F120C e ela abriu a F120T
    Então a tela abre com o código INEP, a coordenadoria, os dois CNPJs, o nome, o endereço e o número do imóvel daquela instituição
    E o nome do bairro e o nome da mantenedora aparecem

  Cenário: O indicador preenchido encaminha para a consulta
    Dado que a F120T recebe o indicador com um valor diferente de branco e de "N"
    Quando confirmo a tela
    Então ela passa adiante a coordenadoria em uso
    E me encaminha para a F120C
    E nada é gravado por esta tela

  Cenário: Inclusão sem o código INEP
    Quando confirmo a inclusão com o código INEP em branco
    Então vejo "*Informe o INEP da instituicao beneficente *"
    E o cursor volta para o campo do código
    E nada é gravado

  Cenário: Inclusão com código INEP já cadastrado
    Quando confirmo a inclusão com o código INEP de uma instituição que já existe
    Então vejo "* Instituicao beneficente ja cadastrada *"
    E nada é gravado

  Cenário: Inclusão com código INEP abaixo do piso
    Quando confirmo a inclusão com um código INEP menor que 30.000.000
    Então vejo "* INEP invalido *"
    E o cursor volta para o campo do código

  Cenário: Coordenadoria não informada
    Quando confirmo com a coordenadoria em branco
    Então vejo "* Informe o grupo *"
    E o cursor volta para o campo da coordenadoria

  Cenário: Coordenadoria que não é a do servidor
    Dado que a minha sessão tem uma coordenadoria
    Quando informo uma coordenadoria que não é a minha
    Então vejo "* Usuario sem acesso a outro grupo *"
    E nada é gravado

  Cenário: Coordenadoria não cadastrada
    Quando informo uma coordenadoria que não existe para o tipo de órgão da minha sessão
    Então vejo "* Grupo nao cadastrado *"
    E o cursor volta para o campo da coordenadoria

  Cenário: Nome da instituição em branco
    Quando confirmo sem informar o nome da instituição beneficente
    Então vejo "* Informe o nome da inst.beneficente *"
    E o cursor volta para o campo do nome

  Cenário: Endereço da instituição em branco
    Quando confirmo sem informar o endereço da instituição beneficente
    Então vejo "* Informe o endereco da inst.beneficente *"
    E o cursor volta para o campo do endereço

  Cenário: Código do bairro em branco
    Quando confirmo sem informar o código do bairro
    Então vejo "* Informe o codigo do bairro da inst.beneficente *"
    E o cursor volta para o campo do bairro

  Cenário: Bairro não cadastrado
    Quando informo um código de bairro que não existe no cadastro de bairros
    Então vejo "* Bairro nao cadastrado *"
    E o cursor volta para o campo do bairro

  Cenário: CNPJ que não passa na conferência dos dígitos
    Quando informo um CNPJ cujos dígitos verificadores não fecham
    Então vejo "* CNPJ invalido *"
    E o cursor volta para o campo daquele CNPJ

  Cenário: Os dois CNPJs em branco
    Quando confirmo com o CNPJ da instituição e o CNPJ da mantenedora em branco
    Então vejo "* Informe o CNPJ da inst.benef ou da mantenedora *"
    E o cursor volta para o campo do CNPJ da instituição

  Cenário: CNPJ da instituição já usado por outra instituição
    Quando informo um CNPJ que já pertence a outra instituição beneficente
    Então vejo a mensagem "<- CNPJ cadastrado para outro INEP *", com o código INEP que já usa o CNPJ à frente
    E nada é gravado

  Cenário: CNPJ da instituição que é de uma mantenedora
    Quando informo, como CNPJ da instituição, um CNPJ que já está no cadastro de mantenedoras
    Então vejo "* CNPJ de Mantenedora *"
    E nada é gravado

  Cenário: Mantenedora ainda não cadastrada é criada na hora
    Dado que informo um CNPJ de mantenedora que ainda não existe
    Quando confirmo a inclusão da instituição beneficente
    Então a mantenedora fica cadastrada com o nome da instituição beneficente
    E a instituição beneficente fica cadastrada

  Cenário: Instituição não cadastrada
    Quando informo, na alteração, na exclusão ou na consulta, um código INEP que não existe
    Então vejo "* Instituicao beneficente nao cadastrada *"
    E o cursor volta para o campo do código

  Cenário: Instituição de outro tipo de órgão
    Quando informo o código de uma instituição cadastrada em outro tipo de órgão
    Então vejo "* Inst.beneficente cad. em outra secretaria *"
    E nada é gravado

  Cenário: Instituição de outra coordenadoria
    Dado que a minha sessão tem uma coordenadoria
    Quando a instituição informada pertence a outra coordenadoria
    Então vejo a mensagem "<- Usuario sem acesso ao grupo desta Inst.benef. *", com o código da coordenadoria à frente
    E nada é gravado

  Cenário: Exclusão recusada por convênios
    Dado que a instituição informada tem convênios cadastrados
    Quando confirmo a exclusão
    Então vejo "* Ja existem convenios cadastrados *"
    E a instituição não é apagada

  Cenário: Exclusão recusada por notas fiscais
    Dado que a instituição informada tem notas fiscais cadastradas
    Quando confirmo a exclusão
    Então vejo "* Ja existem notas cadastradas *"
    E a instituição não é apagada

  Cenário: Trocar a coordenadoria leva as notas fiscais e os convênios
    Dado que estou alterando uma instituição já cadastrada
    Quando informo uma coordenadoria diferente da que ela tem gravada
    Então as notas fiscais e os itens de gênero dela passam para a coordenadoria nova
    E os convênios anuais dela são recriados na coordenadoria nova
    E cada registro movimentado deixa o seu próprio registro de auditoria

  Cenário: Alterar sem trocar a coordenadoria não movimenta nada além da instituição
    Dado que estou alterando uma instituição já cadastrada
    Quando mantenho a coordenadoria que ela tem gravada
    Então só o cadastro da instituição é gravado
    E as notas fiscais e os convênios dela não são movimentados

  Cenário: Operação sem permissão
    Dado que a minha matrícula não tem a permissão da operação em uso nesta tela
    Quando confirmo a tela
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Tela não autorizada para a matrícula
    Dado que a minha matrícula não tem acesso a esta tela
    Quando abro a F120T
    Então vejo "* Acesso negado para esta matricula *"
    E a transação é abandonada
```
