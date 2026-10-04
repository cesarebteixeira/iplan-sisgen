# US — C030T — Manter a ficha do fornecedor

## Estória

Como **servidor da CRE que responde pelo cadastro de fornecedores da sua secretaria**, quero
**manter a ficha do fornecedor com o CNPJ, a razão social e o endereço dele**, para que **a
secretaria tenha o endereço de correspondência do fornecedor no mesmo cadastro em que ele já está
identificado pelo CNPJ**.

O fornecedor entra no sistema pelo CNPJ: é ele que identifica a empresa, e é dele que a tela busca o
endereço, em vez de pedir ao servidor que digite o que a base do estado já sabe. O que a tela
acrescenta é o que falta naquela base: o número do imóvel, o complemento, o contato, o telefone, o
ramal e o bairro. Sem esta ficha, a secretaria não tem para onde endereçar o que envia ao fornecedor
— e o mesmo fornecedor passa a ser procurado pelo nome, que não é único.

## Contexto

Jornada S000M → C000M → C015M → C030T.

Ator: servidor de CRE — mantém a ficha do fornecedor no cadastro de fornecedores: inclui pelo CNPJ,
altera, exclui logicamente e consulta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio. Os dois menus do caminho (`C000M` e `C015M`) não gravam nada: só encaminham.

Da sessão a tela usa a **secretaria (o tipo de órgão)**, a **coordenação regional escolar**, a
**matrícula**, o **código de acesso**, o **privilégio**, a **estação**, a **data do sistema** e o
**nome da secretaria**. O **órgão filho** do servidor, que a entrada também carrega, **não** limita
esta tela: a ficha do fornecedor não pertence a órgão. Essa carga é regra da entrada e está no anexo,
em **Regras que se revelaram da entrada**.

Esta é uma das telas que **mudam conforme quem a chamou**: chegando pela lista de fornecedores
(`C030C`), com um fornecedor escolhido, ela abre **em consulta** sobre ele, com a ficha carregada;
chegando pela opção 4 do menu, abre **em inclusão**, com os campos em branco (RN-02). Ao terminar,
ela devolve o controle a si mesma — com o registro carregado — ou à lista, pelo indicador de retorno
(RN-15).

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela mantém a ficha do fornecedor no cadastro de fornecedores

Esta é a tela de manutenção do cadastro de fornecedores: por ela se **inclui**, se **altera**, se
**exclui** e se **consulta** o fornecedor. A ficha guarda **dezenove dados**: os **dezessete que a
tela mostra e edita** — o código do fornecedor, o CNPJ, o indicador de CPF/CNPJ (1 para CPF, 2 para
CNPJ), a razão social, o endereço, o complemento, o número do imóvel, o código do bairro, o nome do
bairro, o CEP, a cidade, o estado, o contato, o DDD, o telefone, a inscrição estadual e o número do
ramal —, mais a **marca de situação** (que diz se a ficha está ativa ou logicamente excluída) e a
**forma numérica do CNPJ**, derivada do CNPJ informado.

O **código do fornecedor** é a chave do cadastro: é por ele que a ficha é procurada. O CNPJ tem uma
segunda entrada, e essa entrada **admite repetição** — dois fornecedores podem figurar nela com o
mesmo CNPJ —, e é por isso que a tela confere o CNPJ repetido antes de gravar (RN-05).

A tela grava **dois** cadastros: a ficha do fornecedor e a trilha de auditoria. Nenhum outro cadastro
é escrito por ela.

[?] A forma numérica do CNPJ existe na ficha, mas esta tela **zera** esse dado a cada transmissão e
nunca o preenche a partir do CNPJ informado: quem o mantém não está nesta jornada, e a ficha fica com
ele zerado. Pergunta ao site.

### RN-02 — A tela abre em inclusão ou em consulta conforme a tela que a chamou

Chegando pela **lista de fornecedores (`C030C`)**, com um fornecedor escolhido, a tela abre **em
consulta** sobre ele: os campos vêm preenchidos com a ficha, e a operação já é a de consulta.
Chegando **pela opção 4 do menu**, a tela abre **em inclusão**, com os campos em branco.

Quem decide é a **tela de origem**, deixada na área de trabalho da sessão pelo programa que chamou: a
tela compara essa origem com o código da lista e, sendo ela, troca a operação por consulta e carrega
a ficha do fornecedor escolhido; a marca da origem é consumida em seguida, para não valer na próxima
abertura. Aberta pelo menu, a operação fica a de inclusão e nada é carregado.

### RN-03 — A operação tem de ser inclusão, alteração, exclusão ou consulta

O campo da operação aceita as quatro opções que a própria tela anuncia quando recusa: **INC**
(inclusão), **ALT** (alteração), **EXC** (exclusão) e **CON** (consulta). O que for digitado em
minúsculas é convertido para maiúsculas antes da conferência. Qualquer outro valor é recusado com
**\* Opcao nao disponivel. Use INC, ALT, EXC ou CON \***, com o cursor de volta ao campo da operação,
e nada é gravado.

[?] As quatro opções são as que a mensagem da tela declara; o que a tela compara vem da tabela de
mensagens do sistema, que o acervo não traz — de modo que a correspondência entre cada opção e cada
operação é a que a mensagem declara, não uma que se possa ler na tabela.

[?] Além da conferência pelas quatro opções, o programa recusa a operação quando ela casa com cinco
valores de operação que também vêm da tabela de mensagens do sistema, e nesse caso o aviso seria o
daquela tabela. Se esses valores são operações antigas da máscara, ou se a conferência deveria testar
o contrário (recusar o que **não** é uma das quatro), é pergunta ao site.

### RN-04 — Os campos de número passam pela edição numérica antes de qualquer uso

**Nove campos** são conferidos como número antes de qualquer uso: o **código do fornecedor**, o
**indicador de CPF/CNPJ**, o **número do imóvel**, o **código do bairro**, o **CEP**, o **DDD**, o
**telefone**, a **inscrição estadual** e o **número do ramal**. O que não for número é recusado no
próprio campo, com o cursor de volta nele, e a operação não segue. O campo em branco é tratado como
zero, e os zeros à esquerda são descartados.

Os campos de texto (razão social, endereço, complemento, nome do bairro, cidade, estado e contato)
não passam por essa edição.

### RN-05 — A inclusão começa pelo CNPJ, e o CNPJ já cadastrado é recusado

Na inclusão, o primeiro dado é o **CNPJ**. A tela procura o CNPJ no cadastro de fornecedores e,
achando já uma ficha com aquele CNPJ, recusa mostrando o **código do fornecedor encontrado** antes do
aviso **\* <- CNPJ ja cadastrado neste codigo \***, com o cursor de volta ao CNPJ. Nada é gravado.

[?] O aviso **\* Informe o CNPJ do fornecedor \*** só sai quando o campo está preenchido com
**quatorze zeros**: a conferência compara o campo (que é de texto, com catorze posições) com o valor
zero, e essa comparação só é verdadeira para quatorze zeros. Com o CNPJ em branco a inclusão **segue**
para a consulta ao SIGMA, e o material lido não diz qual recusa o servidor vê nesse caso. Pergunta ao
site.

### RN-06 — O endereço do fornecedor é buscado na base do SIGMA

Passando a conferência do CNPJ, a tela consulta a **base do SIGMA** com aquele CNPJ e traz de lá
**doze dados**, já preenchidos para o servidor conferir e completar: a **razão social**, o
**endereço**, o **complemento**, o **número do imóvel**, o **bairro**, a **cidade**, o **estado**, o
**CEP**, o **contato**, o **telefone**, o **ramal** e a **inscrição estadual**.

Três recusas podem sair daí e, nas três, nada é gravado e o cursor volta ao campo do CNPJ:

- sem acesso à base: **\* Banco SIGMA sem acesso \***;
- acesso com problema na resposta: **\* Problemas no acesso ao SIGMA \***;
- CNPJ que não está na base: **\* CNPJ nao cadastrado \***.

### RN-07 — O código do fornecedor é atribuído pelo sistema, e a inclusão é transmitida em dois passos

O código do fornecedor **não é digitado**: a tela toma o **último código** do cadastro e atribui o
**seguinte**; não havendo nenhum fornecedor, começa em **1**. Em seguida a tela **se reabre** com o
código novo, o CNPJ e os dados trazidos do SIGMA, e com o aviso
**\* Transmita para a Inclusao \***.

A inclusão, portanto, tem **dois passos**: o primeiro só busca e monta — **nada é gravado** nele —, e
é a **segunda transmissão** que grava a ficha. Enquanto o aviso está na tela, a inclusão ainda não
aconteceu.

### RN-08 — O CPF ou o CNPJ é conferido pelo dígito verificador

Na transmissão que grava a inclusão, o documento passa pela conferência do **dígito verificador**: o
indicador diz se o documento é **CPF** (1) ou **CNPJ** (2). Reprovando, a recusa é
**\* CPF invalido \*** ou **\* CNPJ invalido \***, com o cursor de volta ao campo do indicador, e nada
é gravado. Indicador diferente de 1 e de 2 cai na recusa de **CPF inválido**.

### RN-09 — O bairro: código no Rio de Janeiro, nome nas demais cidades

Quando a **cidade é RIO DE JANEIRO**, o bairro é informado pelo **código**, e o código tem de existir
no cadastro de bairros: em branco, a recusa é **\* Informe o codigo do Bairro \***; não achado,
**\* Bairro nao cadastrado \***. Nas **demais cidades**, o bairro é o **nome**, escrito livremente: em
branco, a recusa é **\* Informe o Bairro \***, e o código do bairro é zerado, porque a ficha guarda
só o nome.

Na inclusão, o bairro que veio do SIGMA é procurado no cadastro de bairros **pelo nome**, para achar
o código: achando, o código vai para a ficha; não achando, o código fica em branco e — sendo o Rio de
Janeiro — o servidor tem de informá-lo.

### RN-10 — Endereço, CEP, cidade e estado são obrigatórios

Nas operações que gravam, quatro dados do endereço são obrigatórios, cada um com a sua recusa e o
cursor de volta ao campo:

| o que falta | o que a tela diz |
| --- | --- |
| o endereço | **\* Informe o endereco \*** |
| o CEP | **\* Informe o CEP \*** |
| a cidade | **\* Informe a Cidade \*** |
| o estado | **\* Informe o Estado \*** |

A conferência é a mesma na inclusão e na alteração.

### RN-11 — O estado tem de ser uma das unidades da lista

O estado informado é conferido contra uma **lista fixa de vinte e quatro unidades da federação**:
AC, AL, AM, BA, CE, ES, GO, MA, MG, MS, MT, PA, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, SP e TO.
Fora da lista a recusa é **\* Estado invalido \***, com o cursor de volta ao campo. **Não estão na
lista o Distrito Federal, o Amapá e a Paraíba.**

### RN-12 — A alteração exige ter consultado o fornecedor antes e não deixa trocar o CNPJ

Para alterar, o servidor precisa **ter consultado aquele fornecedor antes, na mesma sessão**: se o
código informado não é o do fornecedor que a tela acabou de mostrar, a recusa é
**\* Consulte o fornecedor antes de atualizar \***. Passando, a **razão social** tem de estar
preenchida (**\* Informe a razao social \***) e o **CNPJ não pode ser trocado**
(**\* Nao atualize CNPJ do fornecedor \***). O endereço, o bairro, o CEP, a cidade e o estado passam
pelas mesmas conferências da inclusão.

[?] A conferência do CNPJ compara o que está na tela com o CNPJ que ficou na área de trabalho da
sessão — e a **consulta** não deixa o CNPJ do fornecedor mostrado lá; só a **inclusão** deixa. Do jeito
que está, a alteração passa depois de uma inclusão do mesmo fornecedor na mesma sessão e cai em
**\* Nao atualize CNPJ do fornecedor \*** depois de uma consulta. Ou a consulta deveria deixar o CNPJ
na área de trabalho, ou a conferência compara com outro dado. Pergunta ao site.

A ficha precisa existir no cadastro: a alteração e a exclusão não acham a ficha e param sem gravar.

[?] Quem confere a existência da ficha, na alteração e na exclusão, é a rotina comum do sistema, e a
mensagem que ela monta vem da tabela de mensagens, que o acervo não traz — o texto que o servidor vê
nessa recusa é pergunta ao site.

### RN-13 — A exclusão é lógica e é recusada quando há contrato para o fornecedor

A exclusão **não apaga** a ficha: ela marca a situação do registro como **excluída**, e a ficha deixa
de aparecer nas listas. Antes de marcar, a tela procura o fornecedor nos **itens de contrato**,
percorrendo os órgãos, os contratos de cada órgão e os itens de cada contrato; achando algum item
daquele fornecedor, recusa com **\* Nao exclua. Permissao cad. para o fornecedor \*** e o cursor volta
ao campo da operação. O item de contrato já marcado como excluído **não** conta.

Como na alteração, só se exclui o fornecedor que foi consultado antes na mesma sessão: senão a recusa
é **\* Consulte o fornecedor antes de alterar \***.

A exclusão desta tela também **não trava** o registro: o travamento só existe no caminho do
apagamento físico, que esta tela não aciona.

### RN-14 — A consulta mostra a ficha e não grava nada

A consulta procura a ficha **pelo código** e a mostra: os dados vêm do cadastro e a tela se reabre
com eles — é assim que a consulta se atualiza. Não achando, o aviso é
**\* Fornecedor nao cadastrado \*** e o cursor volta ao campo do código.

A consulta **não grava, não altera, não exclui e não trava** registro nenhum.

### RN-15 — A tela devolve o controle à lista pelo indicador de retorno

Quando o **indicador de retorno** da tela vem preenchido com um valor diferente de **N**, a tela não
segue com a operação: devolve o controle à **lista de fornecedores (`C030C`)**. Aberta normalmente,
ela repõe esse indicador em **N** e segue.

[?] O material lido mostra o desvio, mas não mostra **quem preenche** o indicador: o programa o repõe
em N a cada abertura, e nenhum programa desta jornada o preenche. Se é um campo que o servidor digita,
ou um valor que a máscara manda, é pergunta ao site.

### RN-16 — A operação só acontece com a permissão da tela

Antes de seguir, a cada transmissão, a tela confere a autorização do **código de acesso** do servidor
para aquela tela e para aquela operação, no cadastro de telas por código de acesso — que guarda as
permissões separadas (inclusão, alteração, exclusão e consulta). **Sem o registro** de autorização da
tela para o código de acesso, o aviso é **\* Acesso negado para esta matricula \***; **com o registro**
e sem a permissão da operação, **\* Acesso negado para esta operacao \***. Nas duas, a operação para
ali e nada é gravado.

[?] A conferência nunca lê a permissão de **consulta**: o cadastro guarda as quatro permissões
separadas, mas a rotina comum só testa a de inclusão, a de alteração e a de exclusão, e a consulta cai
no ramo das operações que não são nenhuma dessas três — ali ela passa sem que permissão nenhuma seja
lida. Se a consulta deve mesmo ser livre, ou se falta conferir a permissão dela, é pergunta ao site. É
o mesmo defeito já registrado na C020C.

### RN-17 — Inclusão, alteração e exclusão ficam na trilha de auditoria

Toda transmissão que grava deixa um registro na **trilha de auditoria**, com a **tela** de origem
(`C030T`), a **operação** (inclusão, alteração ou exclusão), o **conteúdo anterior** e o **conteúdo
posterior** da ficha, a **matrícula** do funcionário, a **estação**, o **número do processo**, a
**sessão** (dia, mês, ano e hora) e o **tipo de órgão**. Na inclusão o conteúdo anterior vai em
branco; na exclusão, o posterior vai em branco. A **consulta não gera registro**.

[?] O registro de auditoria é montado e gravado **antes** de a ficha ser gravada: se a gravação da
ficha falhar, a trilha registra uma operação que não aconteceu. Se a ordem é intencional, é pergunta
ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manter a ficha do fornecedor (CNPJ, razão social e endereço) no cadastro de fornecedores

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C030T

  Cenário: RN-01 — incluir um fornecedor com o endereço completo
    Dado que estou na C030T em modo de inclusão
    Quando informo o CNPJ e transmito
    Então o sistema busca o endereço e atribui o código do fornecedor
    E na segunda transmissão a ficha é gravada
    E a operação fica registrada na trilha de auditoria

  Cenário: RN-01 — alterar a ficha de um fornecedor
    Dado que a ficha do fornecedor está carregada na tela
    E o CNPJ informado continua o mesmo
    Quando informo a operação ALT com os dados corrigidos e transmito
    Então a ficha é regravada
    E a operação fica registrada na trilha de auditoria

  Cenário: RN-01 — excluir logicamente um fornecedor
    Dado que consultei o fornecedor na mesma sessão
    E não há item de contrato que use esse fornecedor
    Quando informo a operação EXC e transmito
    Então a ficha fica marcada como excluída
    E deixa de aparecer nas listas
    E a operação fica registrada na trilha de auditoria

  Cenário: RN-02 — aberta pela lista, a tela vem em consulta
    Dado que escolhi um fornecedor na lista C030C
    Quando a C030T abre
    Então ela mostra a ficha daquele fornecedor
    E a operação já é a de consulta

  Cenário: RN-02 — aberta pelo menu, a tela vem em inclusão
    Dado que abro a C030T pela opção 4 do menu, sem passar pela lista
    Quando a C030T abre
    Então os campos estão em branco
    E a operação é a de inclusão

  Cenário: RN-03 — opção de operação indisponível
    Quando informo uma operação diferente de INC, ALT, EXC e CON
    Então vejo a mensagem "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E o cursor volta para o campo da operação
    E nada é gravado

  Cenário: RN-04 — campo de número com texto
    Quando informo texto em um dos campos de número
    Então o campo é recusado antes de qualquer uso
    E o cursor volta para o campo
    E nada é gravado

  Cenário: RN-05 — inclusão de CNPJ já cadastrado
    Dado que já existe um fornecedor com o CNPJ informado
    Quando transmito a inclusão
    Então vejo o código do fornecedor encontrado e a mensagem "* <- CNPJ ja cadastrado neste codigo *"
    E o cursor volta para o campo do CNPJ
    E nada é gravado

  Cenário: RN-06 — endereço buscado na base do SIGMA
    Dado que o CNPJ está na base do SIGMA
    Quando transmito a inclusão
    Então a tela mostra a razão social e o endereço trazidos de lá
    E o servidor completa o que falta

  Cenário: RN-06 — sem acesso à base do SIGMA
    Dado que a base do SIGMA está sem acesso
    Quando transmito a inclusão
    Então vejo a mensagem "* Banco SIGMA sem acesso *"
    E o cursor volta para o campo do CNPJ
    E nada é gravado

  Cenário: RN-06 — problema no acesso ao SIGMA
    Dado que o acesso ao SIGMA tem problema
    Quando transmito a inclusão
    Então vejo a mensagem "* Problemas no acesso ao SIGMA *"
    E nada é gravado

  Cenário: RN-06 — CNPJ que não está na base do SIGMA
    Dado que o CNPJ informado não está na base do SIGMA
    Quando transmito a inclusão
    Então vejo a mensagem "* CNPJ nao cadastrado *"
    E o cursor volta para o campo do CNPJ
    E nada é gravado

  Cenário: RN-07 — o código é atribuído e a tela pede a transmissão
    Dado que o CNPJ foi aceito
    Quando a tela volta com os dados do SIGMA
    Então vejo o código novo do fornecedor
    E vejo o aviso "* Transmita para a Inclusao *"
    E nada foi gravado ainda

  Cenário: RN-08 — CPF inválido
    Dado que o indicador diz que o documento é um CPF
    Quando o CPF informado não passa no dígito verificador
    Então vejo a mensagem "* CPF invalido *"
    E o cursor volta para o campo do indicador
    E nada é gravado

  Cenário: RN-08 — CNPJ inválido
    Dado que o indicador diz que o documento é um CNPJ
    Quando o CNPJ informado não passa no dígito verificador
    Então vejo a mensagem "* CNPJ invalido *"
    E nada é gravado

  Cenário: RN-09 — cidade do Rio de Janeiro sem o código do bairro
    Dado que a cidade é RIO DE JANEIRO
    Quando transmito sem o código do bairro
    Então vejo a mensagem "* Informe o codigo do Bairro *"
    E o cursor volta para o campo do código do bairro

  Cenário: RN-09 — código de bairro que não existe
    Dado que a cidade é RIO DE JANEIRO
    Quando informo um código de bairro que não está no cadastro de bairros
    Então vejo a mensagem "* Bairro nao cadastrado *"
    E nada é gravado

  Cenário: RN-09 — bairro pelo nome fora do Rio de Janeiro
    Dado que a cidade não é RIO DE JANEIRO
    Quando transmito sem o nome do bairro
    Então vejo a mensagem "* Informe o Bairro *"
    E o cursor volta para o campo do bairro

  Cenário: RN-10 — dado obrigatório do endereço em branco
    Dado que deixo o endereço, o CEP, a cidade ou o estado em branco
    Quando transmito
    Então vejo a mensagem daquele campo ("* Informe o endereco *", "* Informe o CEP *",
      "* Informe a Cidade *" ou "* Informe o Estado *")
    E o cursor volta para o campo
    E nada é gravado

  Cenário: RN-11 — estado fora da lista
    Quando informo um estado que não está na lista das vinte e quatro unidades
    Então vejo a mensagem "* Estado invalido *"
    E o cursor volta para o campo do estado
    E nada é gravado

  Cenário: RN-12 — alterar sem ter consultado antes
    Dado que não consultei o fornecedor nesta sessão
    Quando informo a operação ALT e transmito
    Então vejo a mensagem "* Consulte o fornecedor antes de atualizar *"
    E nada é gravado

  Cenário: RN-12 — alterar sem a razão social
    Dado que a ficha do fornecedor está carregada na tela com a razão social em branco
    Quando transmito a alteração
    Então vejo a mensagem "* Informe a razao social *"
    E nada é gravado

  Cenário: RN-12 — tentar trocar o CNPJ na alteração
    Dado que o CNPJ informado não é o do fornecedor carregado na tela
    Quando transmito a alteração
    Então vejo a mensagem "* Nao atualize CNPJ do fornecedor *"
    E nada é gravado

  Cenário: RN-13 — exclusão recusada porque há contrato para o fornecedor
    Dado que existe um item de contrato daquele fornecedor
    Quando transmito a exclusão
    Então vejo a mensagem "* Nao exclua. Permissao cad. para o fornecedor *"
    E o cursor volta para o campo da operação
    E a ficha continua ativa

  Cenário: RN-13 — excluir sem ter consultado antes
    Dado que não consultei o fornecedor nesta sessão
    Quando informo a operação EXC e transmito
    Então vejo a mensagem "* Consulte o fornecedor antes de alterar *"
    E a ficha continua ativa

  Cenário: RN-14 — consultar um fornecedor cadastrado
    Dado que informo o código de um fornecedor cadastrado
    Quando transmito a consulta
    Então a tela mostra a ficha daquele fornecedor
    E nada é gravado, alterado, excluído ou travado

  Cenário: RN-14 — consultar um fornecedor que não existe
    Quando transmito a consulta com um código que não está no cadastro
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E o cursor volta para o campo do código
    E nada é gravado

  Cenário: RN-15 — o indicador de retorno devolve o controle à lista
    Dado que o indicador de retorno da tela está preenchido com um valor diferente de N
    Quando transmito
    Então a tela não segue com a operação
    E o controle volta para a lista de fornecedores C030C

  Cenário: RN-16 — sem autorização para a tela
    Dado que não tenho o registro de autorização desta tela para o meu código de acesso
    Quando transmito qualquer operação
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E nada é gravado

  Cenário: RN-16 — sem a permissão da operação
    Dado que tenho o registro da tela, mas não a permissão da operação pretendida
    Quando transmito a operação
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-17 — a operação fica na trilha de auditoria
    Dado que incluo, altero ou excluo um fornecedor
    Quando a operação termina
    Então a trilha registra a tela, a operação, o conteúdo anterior e o posterior, a matrícula,
      a estação, o processo, a sessão e o tipo de órgão
    E a consulta não deixa registro nenhum
```
