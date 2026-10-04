# US — C668T — Manter períodos de vigência do contrato

## Estória

Como **servidor da CRE que responde pelos contratos da sua coordenadoria regional escolar**,
quero **registrar, para um grupo escolar e um tipo de contrato, os períodos de vigência com o
tipo de licitação, a descrição do período e, quando o contrato exigir, o operador logístico**,
para que **as despesas do grupo possam ser lançadas dentro do período certo, com o contrato
identificado e com a contrapartida da licitação que o originou**.

O período é a régua de tempo do contrato dentro do grupo escolar: sem ele não se sabe a que
contrato pertence um gasto nem até quando ele vale. Esta tela exige que o grupo escolar, o tipo
de contrato e o tipo de licitação já existam, e que o grupo do próprio servidor seja o dono da
operação — ela não cria nada disso, só amarra o período a eles. Os períodos de um mesmo par
grupo/contrato não podem se sobrepor: o sistema percorre os períodos já cadastrados e recusa
qualquer um que invada o intervalo de outro.

## Contexto

Jornada S000M → C000M → C050M → C060M → C668T.
Ator: servidor de CRE — registra os períodos de vigência do contrato de um grupo escolar da sua
coordenadoria regional escolar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**,
não regra de negócio. Os três passos do caminho (C000M, C050M e C060M) são telas de menu: só
encaminham, não gravam nada e não deixam registro de origem na sessão.

O que esta tela usa do que veio antes é a **secretaria (o tipo de órgão), a coordenadoria regional
escolar, a matrícula, o código de acesso, o privilégio e a data do sistema** da sessão; isso é
regra da entrada e está no anexo de evidências, em **Regras que se revelaram da entrada**.

Esta tela **não** muda de comportamento conforme quem a chamou: o menu não deixa origem na sessão
e a tela abre igual pelos quatro caminhos. O que a muda é um campo da própria tela, o indicador de
consulta (RN-15), que desvia a operação para a tela seguinte em vez de gravá-la.

O que esta tela entrega à seguinte: quando a operação informada é **CON** (ou quando o indicador de
consulta vem preenchido), ela passa o grupo escolar, o tipo de contrato e o período para a tela
**C330C**, e a abre **em consulta** (RN-15 e RN-16). A C330C, por sua vez, é que decide que a
**C330T** abra em consulta por ter sido chamada pela C330C.

## Regras de negócio

### RN-01 — O servidor entra pelo LOGON e a sessão é a chave da tela

O servidor se identifica com a matrícula funcional e a senha e é atendido por uma secretaria. A
sessão que sai da entrada carrega a matrícula, a coordenadoria regional escolar, o privilégio, o
código de acesso, a secretaria e a data do sistema, e é isso que esta tela usa para saber quem
está operando e qual grupo escolar é o dele. A conferência da matrícula e da senha, a escolha da
secretaria e o registro da sessão são regras da entrada.

### RN-02 — A tela registra períodos de contrato por grupo escolar e tipo de contrato

Esta tela mantém a vigência do contrato de um grupo escolar. Cada período informado é do par
formado pela **coordenadoria regional escolar** e pelo **tipo de contrato**, mais o **tipo de
licitação** e a sua descrição, a **data de início**, a **data limite**, a **descrição do período**
e o **operador logístico**. O mesmo par pode ter vários períodos, e é por isso que a tela trabalha
com uma coleção de períodos.

### RN-03 — A operação é uma das quatro, e o sistema também confere a permissão

As operações aceitas são **INC** (inclusão), **ALT** (alteração), **EXC** (exclusão) e **CON**
(consulta). Qualquer outra coisa no campo da operação é recusada com
**\* Operacao nao disponivel.Use INC,ALT,EXC ou CON \*** e nada é gravado. Antes de deixar a
operação seguir, o sistema confere no cadastro de permissões se o servidor pode executá-la nesta
tela; sem a permissão, a operação não segue.

### RN-04 — A coordenadoria regional escolar é obrigatória e tem de ser a do servidor

O código do grupo escolar é obrigatório: em branco ou com texto, a recusa é
**\* Grupo nao cadastrado \***, com o cursor de volta ao campo. O código tem de estar cadastrado
no cadastro dos grupos escolares da secretaria. Quando o servidor tem uma coordenadoria na sessão
e informa outra, a recusa é **\* Usuario sem acesso a este grupo \***, com o cursor de volta ao
campo e nada gravado.

### RN-05 — O tipo de contrato é obrigatório e tem de estar cadastrado

O tipo de contrato tem de ser informado e tem de existir no cadastro dos tipos de contrato da
secretaria. Em branco, inexistente ou não numérico, a recusa é
**\* Tipo de contrato nao cadastrado \***, com o cursor de volta ao campo e nada gravado.

### RN-06 — O tipo de licitação é escolhido no cadastro e traz a sua descrição

O tipo de licitação é um código do cadastro de licitações; informado, ele é lido e a descrição
correspondente aparece na tela e é gravada junto com o período. Não havendo descrição para o
código, a tela não é recusada por isso: a descrição fica em branco.

[?] O código do tipo de licitação é obrigatório na prática, mas o sistema não recusa o período
quando ele não existe no cadastro de licitações — só deixa a descrição em branco. Não está claro
se isso é intencional ou se o cadastro da licitação deveria ser conferido como os demais.

### RN-07 — As datas do período têm de ser válidas e coerentes

A data de início e a data limite são informadas como dia, mês e ano. Cada uma passa por conversão
e conferência de data: data que não existe é recusada com **\* Periodo inicial invalido \*** ou
**\* Periodo final invalido \***, com o cursor de volta ao dia informado. O ano tem de estar entre
**1994 e 2099**; fora disso, o período é recusado como inválido. E a data limite não pode ser
anterior à data de início: nesse caso a recusa é **\* Data final menor que data inicial \***, com
o cursor de volta ao dia de início.

### RN-08 — A descrição do período é obrigatória

A descrição do período tem de ser informada: em branco, a recusa é
**\* Informe descricao do periodo \***, com o cursor de volta ao campo e nada gravado.

### RN-09 — O tipo de contrato sem grupamentos não aceita período novo

Quando o tipo de contrato existe, mas não há grupamentos de licitação cadastrados para ele, a
tela recusa a inclusão com **\* Tipo contrato sem grupamentos cadastrados \*** e nada é gravado.
É preciso cadastrar os grupamentos do contrato antes de abrir os períodos dele.

### RN-10 — Os períodos do mesmo contrato não podem se sobrepor

O sistema percorre os períodos já cadastrados do par grupo/contrato e compara cada um com o
período informado. Encontrando um período cujo intervalo contenha ou cruze o intervalo informado,
a recusa é **\* Contrato ja cadastrado neste intervalo \***, com o cursor de volta ao dia de
início, e nada é gravado. A conferência é feita por dois caminhos — um pelos períodos cujo
**último dia** coincide com a data limite informada, outro pelos períodos cujo **primeiro dia**
coincide com a data de início informada —, e o mesmo intervalo se sobrepõe a um período tanto
quando a data de início cai dentro dele quanto quando a data limite cai dentro dele.

Além da sobreposição, o caminho que procura pelo último dia confere a sequência: quando o período
informado tem a mesma data limite de um já cadastrado, mas a **data de início** diferente da dele,
o sistema também marca o período como já cadastrado e avisa
**\* Dt.inicio diferente do cadastro \***, com o cursor de volta ao dia de início. Quando a data
de início coincide, o sistema traz para a tela a **descrição do período** e o **operador
logístico** do período já cadastrado.

### RN-11 — O operador logístico é exigido pelo tipo de contrato

Cada tipo de contrato diz se trabalha com operador logístico. Trabalhando, o operador é
obrigatório: em branco, a recusa é **\* Informe o operador logistico \***, com o cursor de volta
ao campo. Não trabalhando, o campo tem de ficar vazio: informado, a recusa é
**\* Contrato nao trabalha com oper.logistico \***. Em qualquer dos dois casos, nada é gravado.

### RN-12 — O operador logístico tem de estar cadastrado, e o nome vem do cadastro

Informado o operador logístico, o código é procurado no cadastro de operadores. Não existindo, a
recusa é **\* Operador logistico nao cadastrado \***, com o cursor de volta ao campo. Existindo, a
**razão social** do cadastro vem para a tela.

### RN-13 — O sistema gera o registro do período, um por grupamento, e grava a vigência

Aceitos o grupo, o contrato, a licitação, as datas, a descrição e o operador, o sistema gera o
registro do período com a **secretaria**, o **grupo escolar**, o **tipo de contrato**, o **tipo de
licitação**, o **grupamento de licitação**, o **operador logístico**, as **datas de início e
limite**, a **descrição do período** e a data de limite do contrato como **vigência**. Havendo
mais de um grupamento marcado na tela, é gerado **um período por grupamento**.

[?] A vigência de cada período gerado é gravada com a **data limite do próprio período** nos dois
extremos — início e fim da vigência iguais —, e não com o intervalo do grupamento que o originou.
O corpus não diz se a vigência deveria ser a do grupamento. Pergunta ao site.

### RN-14 — A cópia de grupamentos exige o grupamento de origem cadastrado

O preenchimento do **grupamento para cópia** — o código do grupamento a copiar e o tipo de
contrato dele — só é aceito se existir, para aquele par, um período cadastrado com o grupamento
informado. Não existindo, a recusa é **\* Grupamentos para copia nao cadastrados \***, com o
cursor de volta ao grupamento de cópia e nada gravado.

### RN-15 — O indicador de consulta desvia a operação para a consulta, e não grava

Preenchido o **indicador de consulta** na tela, a operação informada não é executada: o sistema
leva o servidor à tela de consulta dos períodos do contrato (**C330C**), com o grupo escolar e o
tipo de contrato que estavam na tela, e a abre **em consulta**, mesmo que a operação digitada
fosse inclusão, alteração ou exclusão. A consulta não grava nada.

### RN-16 — A operação CON também leva à consulta

Informada a operação **CON**, a tela não grava: ela encaminha para a mesma tela de consulta dos
períodos do contrato (**C330C**), que abre em consulta. Esta é a saída da tela — quem chega aqui
por um período já cadastrado o consulta ali.

### RN-17 — A alteração exige que o período já esteja cadastrado

Para alterar, o período informado tem de existir: o sistema procura o cadastro pela coordenadoria,
pelas datas de início e limite e pelo grupo escolar. Não encontrando, a recusa é
**\* Periodo nao cadastrado para este TC \***, com o cursor de volta ao campo da data limite.
Encontrado, a alteração grava a nova vigência — as datas de início e limite, a descrição do
período e o operador podem mudar, mantendo-se o grupo escolar e o tipo de contrato.

### RN-18 — A alteração exige consulta prévia do mesmo período

Antes de alterar, o sistema confere se o período que está cadastrado é o mesmo que foi consultado
e está na tela — a chave guardada na sessão (grupo escolar, tipo de contrato e data limite). Se o
servidor mudou essa chave, ou se não consultou antes, a recusa é
**\* Consulte antes de atualizar \***, com o cursor de volta ao campo do grupo escolar, e nada é
gravado.

### RN-19 — A exclusão exige consulta prévia, e o sistema ainda confere se o período já foi usado

Para excluir, o sistema confere se o período cadastrado é o que está na tela — a chave guardada na
sessão. Não sendo, a recusa é **\* Consulte antes de excluir \***, com o cursor de volta ao grupo
escolar, e nada é gravado. Passando essa conferência, o sistema ainda verifica se o período já foi
usado, e recusa a exclusão quando houver:

- grupamentos do período, com **\* Grupamentos nao cadastrados \***, cursor de volta à data limite;
- permissões auxiliares do contrato, com **\* Nao exclua. Permiss.auxiliar ja cadastrada \***,
  cursor de volta à data limite;
- permissões de contrato, com **\* Nao exclua. Permissao ja cadastrada \***, cursor de volta à
  data limite.

[?] A mensagem **\* Consulte antes de excluir \*** afirma que a exclusão exige consulta prévia,
mas o caminho da exclusão que segue sem consulta — quando a chave guardada na sessão não é a
informada — chega à mesma gravação: o ramo da exclusão é alcançado sem passar por essa guarda, e
só o ramo da alteração compara a chave (RN-18). Ou a consulta prévia deveria ser exigida também
aqui, ou o caminho ficou alcançável por outro motivo. Pergunta ao site.

### RN-20 — A exclusão apaga o período e os grupamentos dele

Excluindo, o sistema apaga primeiro os grupamentos do período e depois o período. Os demais
cadastros desta jornada — o grupo escolar, o tipo de contrato, a licitação, os auxiliares — não
são apagados: são só lidos.

### RN-21 — Toda operação que grava deixa trilha de auditoria

Nas operações de inclusão, alteração e exclusão, o sistema registra uma linha de auditoria para o
período, com a **secretaria**, o **tipo de contrato**, a **operação**, a **data e a hora** do
sistema, o **terminal**, a **matrícula do servidor**, e o **conteúdo do período antes e depois** da
operação. A consulta (RN-15 e RN-16) não deixa linha de auditoria.

### RN-22 — A inclusão e a alteração conferem os cadastros auxiliares do período

Ao incluir ou alterar um período, o sistema também confere os cadastros auxiliares vinculados ao
período — os registros do grupamento e o do tipo de contrato na vigência — e, quando ainda não
existem, grava o registro auxiliar junto com o período, com a data e a hora do sistema, o terminal
e a matrícula do servidor. É essa passagem que faz o período aparecer para as telas que leem a
vigência do contrato.

[?] No caminho de alteração, o registro auxiliar do tipo de contrato na vigência é gravado sem a
conferência de existência que o caminho de inclusão faz — a alteração lê os grupamentos do período
e, em seguida, grava o auxiliar do contrato sem olhar se ele já existe. O corpus não diz se a
alteração deveria conferir antes de gravar. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Períodos de vigência do contrato de um grupo escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C668T

  Cenário: RN-03 — operação fora das quatro é recusada
    Quando informo no campo da operação algo que não é INC, ALT, EXC nem CON
    Então a operação é recusada com a mensagem de operação não disponível
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: RN-04 — grupo escolar obrigatório e do próprio servidor
    Dado que tenho coordenadoria na sessão
    Quando informo a coordenadoria de outro
    Então a operação é recusada com a mensagem de usuário sem acesso a este grupo
    E o cursor fica no campo do grupo escolar

  Cenário: RN-05 — tipo de contrato tem de estar cadastrado
    Quando informo um tipo de contrato que não existe
    Então a operação é recusada com a mensagem de tipo de contrato não cadastrado
    E o cursor fica no campo do tipo de contrato
    E nada é gravado

  Cenário: RN-07 — data final anterior à data inicial é recusada
    Quando informo uma data limite anterior à data de início
    Então a operação é recusada com a mensagem de data final menor que a data inicial
    E o cursor fica no dia de início

  Cenário: RN-07 — data inexistente é recusada
    Quando informo um dia que não existe no mês da data de início
    Então a operação é recusada com a mensagem de período inicial inválido

  Cenário: RN-08 — descrição do período é obrigatória
    Quando deixo a descrição do período em branco
    Então a operação é recusada com a mensagem de informar a descrição do período
    E o cursor fica no campo da descrição

  Cenário: RN-09 — contrato sem grupamentos não recebe período
    Dado que o tipo de contrato existe mas não tem grupamentos cadastrados
    Quando tento incluir um período
    Então a operação é recusada com a mensagem de tipo de contrato sem grupamentos cadastrados
    E nada é gravado

  Cenário: RN-10 — período que se sobrepõe a outro é recusado
    Dado que o par grupo escolar e contrato já tem um período cadastrado
    Quando informo um período que invade o intervalo do já cadastrado
    Então a operação é recusada com a mensagem de contrato já cadastrado neste intervalo
    E o cursor fica no dia de início

  Cenário: RN-10 — mesma data limite com início diferente é recusada
    Dado que já existe um período com a mesma data limite que informei
    Quando informo uma data de início diferente da do período cadastrado
    Então a operação é recusada com a mensagem de data de início diferente do cadastro
    E o cursor fica no dia de início

  Cenário: RN-11 — operador logístico exigido pelo contrato
    Dado que o tipo de contrato trabalha com operador logístico
    Quando deixo o operador em branco
    Então a operação é recusada com a mensagem de informar o operador logístico
    E o cursor fica no campo do operador

  Cenário: RN-11 — contrato que não usa operador logístico o recusa
    Dado que o tipo de contrato não trabalha com operador logístico
    Quando informo um operador logístico
    Então a operação é recusada com a mensagem de que o contrato não trabalha com operador logístico
    E nada é gravado

  Cenário: RN-12 — operador logístico tem de estar cadastrado
    Quando informo um operador logístico que não existe no cadastro
    Então a operação é recusada com a mensagem de operador logístico não cadastrado
    E o cursor fica no campo do operador

  Cenário: RN-13 — inclusão grava o período e mostra o nome do operador
    Dado que o grupo escolar, o tipo de contrato e a licitação existem
    E o operador logístico existe no cadastro
    Quando incluo um período válido e o sistema processa a inclusão
    Então o período é gravado para o grupo escolar e o tipo de contrato informados
    E a razão social do operador logístico fica visível na tela
    E um período é gravado para cada grupamento marcado na tela

  Cenário: RN-14 — grupamento de cópia tem de existir
    Dado que informo um grupamento para cópia e o tipo de contrato dele
    Quando esse grupamento não tem período cadastrado no par informado
    Então a operação é recusada com a mensagem de grupamentos para cópia não cadastrados
    E o cursor fica no campo do grupamento de cópia

  Cenário: RN-15 — indicador de consulta desvia para a consulta
    Dado que o grupo escolar e o tipo de contrato existem
    Quando registro o indicador de consulta e confirmo a operação
    Então o sistema me leva à consulta dos períodos do contrato
    E essa consulta abre em modo de consulta
    E nada é gravado por esta tela

  Cenário: RN-16 — operação CON é a consulta
    Quando informo a operação CON para um grupo e um contrato existentes
    Então o sistema me leva à consulta dos períodos do contrato
    E nada é gravado

  Cenário: RN-17 — alteração exige período cadastrado
    Quando informo ALT para um período que não existe
    Então a operação é recusada com a mensagem de período não cadastrado para este tipo de contrato
    E o cursor fica no campo da data limite

  Cenário: RN-18 — alteração sem consulta prévia é recusada
    Dado que não consultei o período antes
    Quando informo ALT
    Então a operação é recusada com a mensagem de consultar antes de atualizar
    E o cursor fica no campo do grupo escolar
    E nada é gravado

  Cenário: RN-19 — exclusão sem consulta prévia é recusada
    Dado que a chave do período na tela não é a do período cadastrado
    Quando informo EXC
    Então a operação é recusada com a mensagem de consultar antes de excluir
    E o cursor fica no campo do grupo escolar

  Cenário: RN-19 — período já usado não pode ser excluído
    Dado que o período já tem permissão auxiliar cadastrada
    Quando informo EXC
    Então a exclusão é recusada com a mensagem de que há permissão auxiliar cadastrada
    E o cursor fica no campo da data limite
    E nada é apagado

  Cenário: RN-20 — exclusão apaga o período
    Dado que consultei o período e ele ainda não foi usado
    Quando informo EXC
    Então o período é apagado deste grupo escolar e tipo de contrato
    E os cadastros de grupo, de contrato e de licitação continuam como estavam

  Cenário: RN-21 — a operação que grava deixa trilha de auditoria
    Dado que incluo, altero ou excluo um período
    Quando a operação se conclui
    Então uma linha de auditoria é registrada com a data, a hora, o terminal e a minha matrícula
    E essa linha guarda o conteúdo do período antes e depois da operação

  Cenário: RN-21 — a consulta não deixa rastro
    Dado que consulto os períodos do contrato
    Quando a consulta se conclui
    Então nenhuma linha nova aparece na trilha de auditoria por causa desta tela
```
