# US — C804T — Atualizar o gênero do cadastro pelo gênero oficial

## Estória

Como **servidor de CRE**, quero **pedir a atualização de um gênero do cadastro a partir do
gênero oficial correspondente, informando o gênero a ser atualizado, o gênero oficial e a
impressora**, para que **o cadastro usado no dia a dia passe a refletir o catálogo oficial,
sem refazer item por item**.

O gênero é o item da alimentação escolar: diz de que produto se trata, em que classe e
subclasse se encaixa, em que unidade é comprado e em que medida pode ser fracionado. Esse
cadastro é mantido à mão, item por item; quando o catálogo oficial muda, o cadastro do dia a
dia envelhece e quem opera com ele passa a operar com item desatualizado. Esta tela é a
ponte: liga o item do cadastro ao item oficial, confirma com quem opera e entrega o serviço
ao processamento — a atualização não é feita na tela.

## Contexto

Jornada S000M → C000M → C800M → C804T.

Ator: servidor de CRE — pede a atualização de um gênero do cadastro, indicando qual gênero
deve ser atualizado, por qual gênero oficial e em que impressora o resultado deve sair.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O `C000M` e o `C800M` são menus: só encaminham, não gravam nada e não deixam dado de negócio
para esta tela. A tela anterior abre a `C804T` **sem passar registro nem operação**: os dois
pares de códigos são informados por quem opera, e a `C804T` abre sempre em atualização,
qualquer que tenha sido a tela que a chamou. A identificação da tela e o código de uma
próxima tela, quando informado, seguem para a conferência de rota da sessão (RN-03 e RN-12).

O contexto de que a `C804T` se serve — a matrícula, o privilégio, o tipo de órgão, a
coordenação regional escolar, a estação, a data do sistema e a descrição do tipo de órgão —
é o que a entrada deixou na sessão; a tela não recalcula nada disso: mostra e repassa às
conferências, ao pedido e à trilha de auditoria.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela pede a atualização; quem atualiza é o processamento

A tela é a manutenção identificada por COD.SUB.CLASSE e serve para pedir a atualização de um
gênero do cadastro a partir do gênero oficial correspondente. Ela não inclui, não altera e
não exclui gênero nenhum: o que ela grava é o **pedido** do relatório de atualização dos
gêneros, com os dois pares de códigos, e um registro na trilha de auditoria. A atualização do
cadastro é feita pelo processamento que o pedido dispara.

[?] O programa do processamento que recebe os dois pares de códigos está **fora desta
jornada** — foi lido só para fechar o ciclo do pedido. No trecho que toca o cadastro de
gêneros ele **exclui** o registro do gênero a ser atualizado, e o material lido não mostra
esse registro sendo recriado. Se a atualização deveria reescrevê-lo, ou se o apagamento é o
que se espera, é pergunta ao site.

[?] A ligação entre o trabalho disparado e o programa do processamento é por nome e
convenção: nenhum arquivo lido a declara. Se outro programa consome esse trabalho, é pergunta
ao site.

### RN-02 — Ao abrir, a tela já está em atualização

Ao ser apresentada, a tela já vem com a operação marcada como **atualização** e com a
**subclasse do gênero a ser atualizado** preenchida com **99**. A operação não é escolhida em
um menu — a tela a marca por si mesma — e nenhum dado de negócio vem da tela anterior: ela
abre assim qualquer que tenha sido quem a chamou. Se a mensagem chegar com outra operação, o
sistema recusa com **\* Opcao nao disponivel. Use ALT \***, devolve o cursor ao campo da
resposta e não lê nem registra nada.

[?] O que o **99** da abertura quer dizer — se é apenas o preenchimento máximo usado para
deixar o campo sem valor, ou se aponta para a última subclasse — não está no acervo. Como a
subclasse compõe a identificação do gênero a ser atualizado, isso muda o que o operador vê ao
abrir a tela. Pergunta ao site.

[?] A recusa nomeia a tecla **ALT**, mas o texto da máscara não está no lote: se o que o
operador digita e o que a tela confere não forem o mesmo vocabulário, a recusa alcança toda
mensagem, e o material lido não diz se o campo da operação é editável. Pergunta ao site.

### RN-03 — O acesso à tela e a autorização da operação são conferidos antes de registrar

Na abertura, o sistema confere que a estação da sessão é a estação registrada para a
matrícula, que a tela está no cadastro de telas e que ela consta do código de acesso do
servidor. Não estando a tela cadastrada, a recusa é **\* Tela nao disponivel \***; faltando a
tela no código de acesso, **\* Acesso negado para esta matricula \***.

Ao processar o pedido, o sistema confere o encaminhamento da tela e, no perfil de acesso, a
autorização da operação de atualização. Faltando a autorização, a recusa é
**\* Acesso negado para esta operacao \*** e nada é registrado. Não estando a tela em
condições de receber a operação, a recusa é **\* Operacao nao disponivel \*** ou
**\* Tela nao cadastrada \***, e nada é registrado.

### RN-04 — O gênero a ser atualizado tem de estar cadastrado

O par informado como gênero a ser atualizado — subclasse e código do gênero — tem de existir
no cadastro de gêneros. Não existindo, a recusa é
**\* Genero a ser atualizado nao cadastrado \***, com o cursor de volta no código do gênero,
e nada mais é lido.

### RN-05 — O gênero oficial tem de estar cadastrado e ativo

O par informado como gênero oficial — subclasse e código — tem de existir no cadastro oficial
de gêneros, entre os registros não excluídos, e estar marcado como **ativo**. Não existindo,
ou existindo e não estando ativo, a recusa é **\* Genero oficial nao cadastrado \***, com o
cursor de volta na subclasse do gênero oficial, e nada é registrado.

Existindo, o sistema traz do cadastro oficial o resumo, a classe e a descrição do gênero
oficial e mostra os dois lados na tela — o gênero a ser atualizado com o seu resumo, e o
gênero oficial com o resumo, a classe e a descrição — para que o operador confira antes de
responder.

[?] O cadastro oficial guarda, para cada par, uma data de início de vigência, e a consulta é
feita com essa data no valor máximo (ano 9999, mês 99, dia 99). Se isso alcança o registro
vigente do par, ou se não acha nada, é dialeto da leitura e o corpus não decide. Pergunta ao
site.

### RN-06 — Sem impressora não há pedido

A impressora é obrigatória: em branco, a recusa é **\* Informe a impressora \***, com o
cursor de volta na impressora, e nada é registrado. A conferência é feita nas duas passagens,
antes e depois da confirmação.

A tela não confere se a impressora está cadastrada: qualquer código de até dez caracteres é
aceito.

[?] O cadastro de impressoras existe no dicionário — com o código da impressora obrigatório —
mas esta tela não o lê. Se o código deveria apontar para uma impressora conhecida, o caminho
não verifica. Pergunta ao site.

### RN-07 — O pedido só é registrado depois da confirmação

Passadas as conferências, o sistema apresenta
**\* Confirma atualizacao do genero <S/N> ? \*** e espera. A pergunta, por si, não registra
nada. Somente a resposta **S** prossegue. Resposta diferente de **S** não cancela nem
registra: o sistema limpa a resposta, volta à primeira passagem, revalida os dados e
apresenta a pergunta de novo.

Se o **código do gênero a ser atualizado**, a **subclasse do gênero oficial** ou o **código
do gênero oficial** mudarem entre a pergunta e a resposta, a confirmação é descartada e a
tela revalida tudo antes de perguntar de novo.

[?] A conferência que decide se a confirmação ainda vale cobre três dos quatro códigos do
pedido: a **subclasse do gênero a ser atualizado**, que também é digitada e que também compõe
o par do gênero a ser atualizado, não é comparada. Trocando só ela depois da pergunta, a
confirmação continua valendo e o pedido segue com a subclasse nova emparelhada ao código de
gênero anterior. Se a intenção era exigir a reconfirmação a qualquer troca dos códigos, o
caminho não exige. Pergunta ao site.

[?] Pelo programa, a única saída da pergunta é responder **S**: sem **S** o fluxo volta à
validação e à própria pergunta. Se o operador abandona a tela, é por um recurso tratado fora
do programa, o que o material lido não determina. Pergunta ao site.

### RN-08 — Um pedido do mesmo relatório já na fila bloqueia pedido novo

Na passagem confirmada, antes de registrar, o sistema verifica se já existe pedido do
relatório de atualização dos gêneros esperando processamento na fila de requisições de
impressão. Existindo, a resposta é **\* Relatorio em processamento. Aguarde. \***, a passagem
volta à primeira e nada é registrado.

[?] A leitura da fila posiciona o código do relatório e deixa os demais componentes da chave
em branco ou zerados; se ela alcança qualquer pedido daquele relatório ou exige a chave
inteira é o que os sinalizadores da leitura dizem, e o dialeto não está explicado no corpus.
Pergunta ao site.

### RN-09 — Confirmado, o pedido é registrado e o processamento é disparado

Com a resposta **S**, o sistema lê o **e-mail** da matrícula no cadastro de funcionários, toma
o **número seguinte** ao último pedido da fila e registra **um pedido** de impressão com o
relatório de atualização dos gêneros, esse número, o dia, o mês e o ano do sistema, a
matrícula e a estação. Em seguida entrega o processamento com o relatório, a impressora, a
estação, a matrícula, o e-mail e os **dois pares de códigos** — o gênero a ser atualizado e o
gênero oficial. A tela então mostra **\* Cadastros sendo atualizado \***.

[?] A impressora não vai para o pedido registrado: o campo correspondente do pedido é deixado
em branco e a impressora viaja só na mensagem de disparo do processamento. O dicionário
declara esse campo obrigatório, mas a semântica de obrigatoriedade no dicionário não está
definida no material lido. Pergunta ao site.

[?] O número do pedido é o último número da fila mais um; quando a fila está vazia, o sistema
apenas marca que não achou, sem limpar a área lida, e a conta é feita sobre o que estiver ali
— o primeiro número pode não ser 1 e, se a área guardar valor de leitura anterior, o número
pode repetir. Pergunta ao site.

### RN-10 — Todo pedido deixa trilha de auditoria

Confirmado o pedido, o sistema grava também um registro de auditoria com a tela de origem, a
operação, os dois pares de códigos como **conteúdo posterior** (o conteúdo anterior vai
vazio), a matrícula, a estação, a data e a hora da sessão, o tipo de órgão e a coordenação
regional escolar.

[?] A operação fica registrada como **inclusão**, ainda que a operação da tela seja a
atualização e que o que se registre seja um pedido de atualização, e o número do processo
desse registro recebe o **código do gênero oficial**. Se a inclusão ali significa "inclusão do
pedido", e o que o número do processo representa para quem lê a trilha, é pergunta ao site.

### RN-11 — Os campos de código passam por edição antes de qualquer conferência

Antes de conferir regra nenhuma, os quatro campos de código passam por edição numérica: a
**subclasse** e o **código do gênero a ser atualizado** (2 e 5 dígitos) e a **subclasse** e o
**código do gênero oficial** (2 e 5 dígitos). Campo em branco vira **zero**; o que não for
número é recusado e a transação não segue.

[?] Quando a digitação de um desses campos é recusada, o sistema posiciona o cursor de volta
no campo recusado para três deles — o código do gênero a ser atualizado, a subclasse do
gênero oficial e o código do gênero oficial —, mas não há posição de cursor definida para a
subclasse do gênero a ser atualizado. Se o operador deveria ser levado de volta a esse campo,
é pergunta ao site.

### RN-12 — Depois do pedido a tela continua na própria tela

Depois de registrar o pedido — e também depois de cada recusa — a tela permanece na `C804T` e
é apresentada de novo ao operador; ela não abre outra tela. O campo em que o operador informa
o código de uma próxima tela é avaliado pela conferência de rota da sessão: informado um
código, é essa tela que se abre, e o pedido desta não chega a ser processado.

[?] O rótulo do campo da próxima tela não está no lote — o texto da máscara vive fora do
material lido. Que o campo é o da tela de destino se conclui do nome do campo e do uso que a
conferência de rota faz dele. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Atualizar o gênero do cadastro pelo gênero oficial

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C804T

  Cenário: Abertura da tela
    Quando a tela C804T é apresentada
    Então a operação já vem marcada como atualização
    E a subclasse do gênero a ser atualizado vem com 99

  Cenário: A tela abre em atualização qualquer que seja quem a chamou
    Dado que cheguei à C804T pela tela anterior da jornada
    Quando a tela é apresentada
    Então nenhum dado de negócio veio da tela anterior
    E a operação vem marcada como atualização

  Cenário: Operação diferente de atualização é recusada
    Dado que a mensagem chega com a operação diferente de atualização
    Quando a tela processa o pedido
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E o cursor volta para o campo da resposta
    E nada é registrado

  Cenário: Tela não cadastrada
    Dado que a tela C804T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela C804T no código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Operação não autorizada
    Dado que o meu perfil não tem a autorização da operação de atualização
    Quando confirmo o pedido
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é registrado

  Cenário: Gênero a ser atualizado não cadastrado
    Dado que o par de subclasse e código informado como gênero a ser atualizado não existe no cadastro
    Quando peço a atualização
    Então vejo a mensagem "* Genero a ser atualizado nao cadastrado *"
    E o cursor volta para o código do gênero
    E nada mais é lido

  Cenário: Gênero oficial não cadastrado ou inativo
    Dado que o gênero a ser atualizado existe
    E o par informado como gênero oficial não existe no cadastro oficial, ou não está ativo
    Quando peço a atualização
    Então vejo a mensagem "* Genero oficial nao cadastrado *"
    E o cursor volta para a subclasse do gênero oficial
    E nada é registrado

  Cenário: A pergunta de confirmação mostra os dois lados e não registra nada
    Dado que informei os dois pares de códigos e a impressora
    Quando a tela confere os dados
    Então vejo a mensagem "* Confirma atualizacao do genero <S/N> ? *"
    E vejo o resumo do gênero a ser atualizado e o resumo, a classe e a descrição do gênero oficial
    E nada foi registrado

  Cenário: Impressora não informada é recusada
    Dado que o gênero a ser atualizado existe
    E o gênero oficial existe e está ativo
    E deixo a impressora em branco
    Quando peço a atualização
    Então vejo a mensagem "* Informe a impressora *"
    E o cursor volta para a impressora
    E nada é registrado

  Cenário: Resposta diferente de S não registra e a pergunta volta
    Dado que estou na pergunta de confirmação
    Quando respondo N
    Então o sistema limpa a resposta, revalida os dados e pergunta de novo
    E nada é registrado

  Cenário: Troca de um código depois da pergunta descarta a confirmação
    Dado que estou na pergunta de confirmação
    Quando troco o código do gênero a ser atualizado, ou a subclasse ou o código do gênero oficial, e respondo S
    Então o sistema revalida os dados antes de aceitar a resposta
    E nada é registrado sem a nova confirmação

  Cenário: Troca só da subclasse do gênero a ser atualizado não descarta a confirmação
    Dado que estou na pergunta de confirmação
    Quando troco apenas a subclasse do gênero a ser atualizado e respondo S
    Então o pedido segue com a subclasse que digitei por último
    E o código do gênero é o da pergunta anterior

  Cenário: Relatório já na fila é recusado
    Dado que já existe um pedido do relatório de atualização dos gêneros esperando processamento
    Quando respondo S à pergunta de confirmação
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E nada é registrado

  Cenário: Pedido registrado e processamento disparado
    Dado que os dois pares de códigos existem e a impressora foi informada
    Quando respondo S à pergunta de confirmação
    Então o sistema registra o pedido com o número seguinte da fila, o relatório de atualização dos gêneros, o dia, o mês e o ano do sistema, a minha matrícula e a estação
    E entrega o processamento com a impressora, o e-mail do meu cadastro e os dois pares de códigos
    E vejo a mensagem "* Cadastros sendo atualizado *"

  Cenário: A impressora não é conferida contra o cadastro
    Dado que informo uma impressora que não está cadastrada
    Quando respondo S à pergunta de confirmação
    Então o pedido é registrado e o processamento é disparado com esse código

  Cenário: A tela não atualiza o cadastro de gêneros
    Dado que os dois pares de códigos existem e a impressora foi informada
    Quando respondo S à pergunta de confirmação
    Então nenhum gênero é incluído, alterado ou excluído nesta transação
    E o único registro gravado é o pedido, além da trilha de auditoria

  Cenário: O pedido deixa trilha de auditoria
    Dado que respondi S à pergunta de confirmação
    Então a trilha de auditoria registra a tela de origem, os dois pares de códigos como conteúdo posterior, o conteúdo anterior vazio, a minha matrícula, a estação, a data e a hora da sessão, o tipo de órgão e a coordenação regional escolar

  Cenário: Depois do pedido a tela continua na C804T
    Dado que acabei de registrar um pedido, ou que a tela recusou o pedido
    Então continuo na C804T
    E nenhuma outra tela é aberta

  Cenário: Informar o código de uma próxima tela leva a ela
    Dado que informei o código de outra tela no campo da próxima tela
    Quando a tela processa a mensagem
    Então é essa tela que se abre
    E o pedido desta não chega a ser processado

  Cenário: Digitação não numérica
    Dado que digito letras em um dos campos de código
    Quando confirmo a transação
    Então a transação não segue
    E nada é registrado
```
