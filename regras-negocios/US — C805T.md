# US — C805T — Atualizar o gênero da alimentação escolar nos cardápios de um período

## Estória

Como **servidor de CRE**, quero **pedir a atualização de um gênero da alimentação
escolar nos cardápios de um período, informando o gênero a ser atualizado, o novo
gênero, o início e o limite do período e a impressora**, para que **os cardápios
daquele período passem a usar o gênero novo sem que ninguém precise redigitar
cardápio por cardápio**.

O gênero é o item da alimentação escolar: é ele que diz de que produto se trata, em
que classe e subclasse se encaixa e em que medida pode ser fracionado. Os cardápios
apontam os gêneros que cada período da merenda usa; quando o item muda, os cardápios
do período continuam apontando o item antigo, e o que se estima e se compra a partir
deles sai errado. Refazer cardápio por cardápio à mão é o trabalho que se quer
evitar. Esta tela é a ponte: liga o item antigo ao item novo, limita a troca ao
período informado, confirma com quem opera e entrega o serviço ao processamento.

## Contexto

Jornada S000M → C000M → C800M → C805T.

Ator: servidor de CRE — pede a atualização de um gênero da alimentação escolar nos
cardápios de um período, indicando o gênero a ser atualizado, o novo gênero, o
período e a impressora.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O `C000M` e o `C800M` são menus: só
encaminham, não gravam nada e não deixam dado de negócio para esta tela.

Do menu que a abre vem a operação: é ele que pede a `C805T` já em **atualização**, e
é essa operação que a tela assume, sem oferecer escolha a quem opera. A entrada deixa
o resto do contexto de que a tela se serve — a matrícula, o privilégio, o tipo de
órgão, a coordenação regional escolar, a estação, a data do sistema e a descrição do
tipo de órgão —, e a tela não recalcula nada disso: apenas o mostra e o repassa às
conferências, ao pedido e à trilha de auditoria.

A tela não abre outra: depois de registrar o pedido, e também depois de cada recusa,
ela volta a si mesma, e o que o operador pode informar é o código de uma próxima
tela, que a lógica de rota da sessão avalia. O que ela entrega adiante é o **pedido
de impressão** que registra e o **processamento do relatório de atualização dos
gêneros**, com o relatório, a impressora, os dois pares de códigos e o período.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela abre em atualização e recusa qualquer outra operação

A tela é de atualização e não pergunta a quem opera qual é a operação: quando o menu
a abre, a operação já vem marcada como **atualização** e as doze respostas que a
própria tela preenche — as descrições dos dois gêneros, a classe, as quatro linhas da
descrição do novo gênero, a descrição do tipo de órgão, a data do sistema e a
mensagem da tela — vêm em branco.

Chegando a transação com operação diferente de atualização, o sistema recusa com
**\* Opcao nao disponivel. Use ALT \***, devolve o cursor ao campo da resposta e não
lê nem registra nada.

### RN-02 — O acesso passa por três conferências, e a operação de atualização precisa estar autorizada

Antes de ler ou gravar qualquer coisa, o sistema confere a estação: a estação da
sessão tem de ser a estação registrada para a matrícula. Em seguida confere se a tela
está no cadastro de telas; não estando, a recusa é **\* Tela nao disponivel \***.
Depois confere, no código de acesso do servidor, a autorização por tela e por
operação. Sem o acesso à tela, a recusa é **\* Acesso negado para esta matricula \***;
sem a autorização da operação de alteração, **\* Acesso negado para esta operacao \***.
Em qualquer dos casos nada é registrado.

O cadastro de telas ainda tem dois códigos — o da tela a que a operação leva e o da
tela de que ela volta — que esta tela não usa: a operação dela não desvia para tela
nenhuma.

### RN-03 — O gênero a ser atualizado tem de ser um gênero cadastrado e ativo

O par informado como **gênero a ser atualizado** — subclasse e código — é procurado no
cadastro de gêneros, entre os registros não excluídos, e tem de estar marcado como
**ativo**. O sistema lê o registro com a data de vigência no valor máximo (ano 9999,
mês 99, dia 99), e a recusa é **\* Genero a ser atualizado nao cadastrado \***, com o
cursor de volta no código do gênero, a passagem voltando à primeira e nada sendo
registrado.

Existindo o registro, o sistema guarda o resumo do gênero lido para mostrá-lo antes
da confirmação.

[?] O texto da recusa não fecha com o caminho que o sistema segue: o sistema recusa
com **\* Genero a ser atualizado nao cadastrado \*** justamente quando o par
informado **está** cadastrado e ativo, e deixa passar quando ele não está. Um dos
dois lados está errado — o texto da mensagem ou a condição que a dispara —, e o
corpus não decide qual. Enquanto isso não se resolve, não se pode afirmar que esta
conferência exige gênero cadastrado: é pergunta ao site.

[?] A leitura posiciona a data de vigência no máximo (ano 9999, mês 99, dia 99). Se
isso alcança o registro vigente do par, ou se não acha nada, é dialeto da leitura, e
o corpus não explica.

### RN-04 — O novo gênero também é procurado no cadastro de gêneros

O par informado como **novo gênero** — subclasse e código — passa exatamente pela
mesma procura, no mesmo cadastro de gêneros, com a data de vigência no valor máximo.
Não sendo encontrado, ou sendo encontrado sem estar ativo, a recusa é
**\* Novo Genero nao cadastrado \***, com o cursor de volta na subclasse do novo
gênero, e nada é registrado. Sendo encontrado, o sistema traz do cadastro o resumo, a
classe e as quatro linhas da descrição do novo gênero, para mostrá-los.

[?] Aqui vale a mesma inversão da RN-03: o sistema recusa com **\* Novo Genero nao
cadastrado \*** quando o novo par **está** no cadastro, e segue quando ele **não
está**. Os dois textos de recusa estão trocados em relação às condições que os
disparam. Pergunta ao site.

### RN-05 — O período precisa ter cardápio cadastrado, e o que o identifica é o dia-limite

O período é informado pelo início e pelo limite, cada um com dia, mês e ano. A
conferência procura, no cadastro de cardápios, um cardápio do **órgão da sessão**
cujo período termine exatamente na **data-limite informada**. Não existindo, a recusa
é **\* Cardapios nao cadastrados neste periodo \***, com o cursor de volta no
dia-limite, a passagem voltando à primeira e nada sendo registrado.

O código do cardápio não é conferido: qualquer cardápio do órgão que termine naquela
data serve, e o sistema não distingue um do outro nesta conferência. O início do
período informado **não participa** de conferência nenhuma.

### RN-06 — O início do período exibido é o do cardápio cadastrado, não o digitado

Encontrado o cardápio do período, o sistema substitui, antes de apresentar a
confirmação, o início que estava na tela pelo início do período do cardápio
cadastrado. É esse início — o do cadastro — que aparece na tela, que segue no pedido
e que fica na trilha de auditoria; o que foi digitado não é usado.

[?] Se a máscara deixa o operador digitar as três datas de início, ou se elas só são
mostradas, o texto da máscara não está no lote. A conferência que decide se a
confirmação ainda vale compara o gênero a ser atualizado, o novo gênero e o limite,
mas **não** compara as três datas de início: um início digitado depois da pergunta
passa sem invalidar a confirmação.

### RN-07 — Sem impressora informada o pedido não anda

A impressora é obrigatória: estando em branco, a recusa é **\* Informe a impressora \***,
com o cursor na impressora, e nada é registrado. A conferência é feita antes e depois
da confirmação. O sistema não confere se a impressora existe em cadastro nenhum:
qualquer código de até dez caracteres é aceito.

### RN-08 — A pergunta de confirmação, e o que a descarta

Passadas as conferências, o sistema apresenta
**\* Confirma atualizacao do genero <S/N> ? \*** e espera. Só a resposta **S**
prossegue. Resposta diferente de **S** não cancela e não registra: o sistema limpa a
resposta, volta à primeira passagem, revalida tudo e pergunta de novo.

Se, entre a pergunta e a resposta, mudarem o **gênero a ser atualizado**, o **novo
gênero** ou o **limite do período**, a confirmação é descartada e a tela revalida
tudo antes de perguntar outra vez. As três datas de **início** não entram nessa
comparação.

### RN-09 — Um pedido do mesmo relatório já na fila bloqueia pedido novo

Antes de registrar, o sistema procura na fila de requisições de impressão, para o
órgão da sessão, um pedido do **relatório de atualização dos gêneros** esperando
processamento. Existindo, a recusa é
**\* Relatorio em processamento. Aguarde. \***, a passagem volta à primeira e nada é
registrado.

### RN-10 — Confirmado o pedido, o sistema lê o e-mail da matrícula e registra o pedido

Com a resposta **S**, o sistema lê o **e-mail** da matrícula no cadastro de
funcionários e toma o **número seguinte** ao último pedido daquela fila. Registra
então **um pedido** de impressão com o relatório de atualização dos gêneros, esse
número, o dia, o mês e o ano do sistema, a matrícula, a estação e o tipo de órgão; o
campo da impressora do pedido é deixado **em branco**. A tela então mostra
**\* Cadastros sendo atualizado \***.

[?] A impressora viaja só no disparo do processamento, não no pedido registrado, e o
dicionário declara esse campo obrigatório. A obrigatoriedade declarada no dicionário
não está definida no material lido.

[?] O número do pedido é o último número da fila mais um; quando a fila está vazia o
sistema apenas marca que não achou, sem limpar a área lida, e a conta sai sobre o que
estiver ali. O primeiro número pode não ser 1.

### RN-11 — O pedido é entregue ao processamento com os dois pares e o período

Ainda na passagem confirmada, o sistema entrega o processamento do relatório de
atualização dos gêneros com o relatório, a **impressora**, a estação, a matrícula, o
**e-mail** lido, o tipo de órgão, os **dois pares de códigos** — o gênero a ser
atualizado e o novo gênero — e o **período**, início e limite. É esse processamento
que troca o gênero nos cardápios do período.

### RN-12 — Todo pedido confirmado deixa trilha de auditoria

Confirmado o pedido, o sistema grava também um registro de auditoria com a tela de
origem, a operação, os **onze valores** do pedido — o tipo de órgão, os dois pares de
códigos e as seis datas do período — como **conteúdo posterior**, o conteúdo anterior
em branco, a matrícula, a estação, a data e a hora da sessão, o tipo de órgão e a
coordenação regional escolar.

[?] A operação fica registrada como **inclusão**, ainda que a operação da tela seja a
atualização e que o que se registre seja um pedido de atualização; o mesmo registro
leva um código de manutenção preenchido com valor fixo. Qual dos campos diz a
operação para quem lê a trilha é pergunta ao site.

### RN-13 — A tela não altera gênero nem cardápio

A tela enxerga seis cadastros — o de telas, o de gêneros, o de cardápios, o de
funcionários, a fila de requisições de impressão e a trilha de auditoria — e **só lê**
os quatro primeiros e a fila. Nenhum gênero e nenhum cardápio é incluído, alterado ou
excluído nesta transação: o que a tela grava é o **pedido** na fila e a trilha de
auditoria da RN-12. A troca do gênero nos cardápios é feita pelo processamento que o
pedido dispara.

### RN-14 — Os dez campos de código e de data passam por edição antes de qualquer conferência

Antes de conferir regra nenhuma, os **dez** campos de código e de data passam por
edição numérica: a subclasse e o código do gênero a ser atualizado, a subclasse e o
código do novo gênero, e o dia, o mês e o ano do início e do limite do período. Campo
em branco vira **zero**; o que não for número é recusado e a transação não segue.

[?] Quando a digitação de um desses campos é recusada, o sistema posiciona o cursor de
volta no campo recusado para **sete** deles — os dois pares de códigos e o dia, o mês
e o ano do limite —, mas não há posição de cursor definida para o dia, o mês e o ano
do início. Se o operador deveria ser levado de volta a esses campos, é pergunta ao
site.

---

## Cenários BDD

```gherkin
Funcionalidade: Atualizar o gênero da alimentação escolar nos cardápios de um período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C805T

  Cenário: Abertura da tela
    Quando a tela C805T é apresentada
    Então a operação já vem marcada como atualização
    E as descrições dos dois gêneros, a classe, a descrição do novo gênero, a descrição do tipo de órgão, a data do sistema e a mensagem vêm em branco

  Cenário: Operação diferente de atualização é recusada
    Dado que a transação chega com a operação diferente de atualização
    Quando a tela processa o pedido
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E o cursor volta para o campo da resposta
    E nada é registrado

  Cenário: Tela não cadastrada
    Dado que a tela C805T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem o acesso à tela
    Dado que a minha matrícula não tem a tela C805T no código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Operação de atualização não autorizada
    Dado que o meu código de acesso não libera a alteração nesta tela
    Quando confirmo o pedido
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é registrado

  Cenário: Gênero a ser atualizado não cadastrado
    Dado que informei como gênero a ser atualizado um par de subclasse e código que não está no cadastro de gêneros
    Quando peço a atualização
    Então vejo a mensagem "* Genero a ser atualizado nao cadastrado *"
    E o cursor volta para o código do gênero
    E nada é registrado

  Cenário: Gênero a ser atualizado cadastrado mas não ativo
    Dado que informei como gênero a ser atualizado um par que está no cadastro e não está marcado como ativo
    Quando peço a atualização
    Então vejo a mensagem "* Genero a ser atualizado nao cadastrado *"
    E o cursor volta para o código do gênero
    E nada é registrado

  Cenário: Novo gênero não cadastrado
    Dado que o gênero a ser atualizado está cadastrado e ativo
    E informei como novo gênero um par que não está no cadastro de gêneros
    Quando peço a atualização
    Então vejo a mensagem "* Novo Genero nao cadastrado *"
    E o cursor volta para a subclasse do novo gênero
    E nada é registrado

  Cenário: Novo gênero cadastrado mas não ativo
    Dado que o gênero a ser atualizado está cadastrado e ativo
    E informei como novo gênero um par que está no cadastro e não está marcado como ativo
    Quando peço a atualização
    Então vejo a mensagem "* Novo Genero nao cadastrado *"
    E o cursor volta para a subclasse do novo gênero
    E nada é registrado

  Cenário: Período sem cardápios cadastrados
    Dado que o gênero a ser atualizado está cadastrado e ativo
    E nenhum cardápio do meu órgão termina na data-limite que informei
    Quando peço a atualização
    Então vejo a mensagem "* Cardapios nao cadastrados neste periodo *"
    E o cursor volta para o dia-limite
    E nada é registrado

  Cenário: Impressora não informada é recusada
    Dado que existe cardápio do meu órgão terminando na data-limite que informei
    E deixo a impressora em branco
    Quando peço a atualização
    Então vejo a mensagem "* Informe a impressora *"
    E o cursor volta para a impressora
    E nada é registrado

  Cenário: A pergunta de confirmação não registra nada
    Dado que informei os dois pares de códigos, o período e a impressora, e tudo foi conferido
    Quando a tela confere os dados
    Então vejo a mensagem "* Confirma atualizacao do genero <S/N> ? *"
    E vejo o resumo do gênero a ser atualizado e o resumo, a classe e a descrição do novo gênero
    E nada foi registrado

  Cenário: Resposta diferente de S não registra e a pergunta volta
    Dado que estou na pergunta de confirmação
    Quando respondo N
    Então o sistema limpa a resposta, revalida os dados e pergunta de novo
    E nada é registrado

  Cenário: Troca do gênero a ser atualizado, do novo gênero ou do limite depois da pergunta descarta a confirmação
    Dado que estou na pergunta de confirmação
    Quando troco o gênero a ser atualizado, ou o novo gênero, ou o limite do período, e respondo S
    Então o sistema revalida os dados antes de aceitar a resposta
    E nada é registrado sem a nova confirmação

  Cenário: Relatório já na fila é recusado
    Dado que já existe um pedido do relatório de atualização dos gêneros esperando processamento
    Quando confirmo o pedido
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E nada é registrado

  Cenário: Pedido registrado e processamento disparado
    Dado que os dois pares de códigos foram conferidos, há cardápio no período e a impressora foi informada
    Quando respondo S à pergunta de confirmação
    Então o sistema registra o pedido com o número seguinte da fila, o relatório de atualização dos gêneros, o dia, o mês e o ano do sistema, a minha matrícula, a estação e o meu órgão
    E entrega o processamento com o relatório, a impressora, o meu e-mail, os dois pares de códigos e o período
    E vejo a mensagem "* Cadastros sendo atualizado *"

  Cenário: O período que segue é o do cardápio cadastrado
    Dado que informei um início de período e existe cardápio do meu órgão terminando na data-limite que informei
    Quando a tela confere os dados
    Então o início que vejo na pergunta de confirmação é o início do período do cardápio cadastrado
    E é esse início que segue no pedido e na trilha de auditoria
    E o início que digitei não é conferido

  Cenário: A impressora não é conferida contra cadastro nenhum
    Dado que informo uma impressora que não está cadastrada
    Quando respondo S à pergunta de confirmação
    Então o pedido é registrado e o processamento é entregue com esse código

  Cenário: A tela não altera gênero nem cardápio
    Dado que os dois pares de códigos foram conferidos, há cardápio no período e a impressora foi informada
    Quando respondo S à pergunta de confirmação
    Então nenhum gênero é incluído, alterado ou excluído nesta transação
    E nenhum cardápio é incluído, alterado ou excluído nesta transação
    E o que a tela grava é o pedido, além da trilha de auditoria

  Cenário: O pedido deixa trilha de auditoria
    Dado que respondi S à pergunta de confirmação
    Então a trilha de auditoria registra a tela de origem, os dois pares de códigos e as seis datas do período como conteúdo posterior, o conteúdo anterior vazio, a minha matrícula, a estação, a data e a hora da sessão, o tipo de órgão e a coordenação regional escolar

  Cenário: Depois do pedido a tela continua na tela
    Dado que acabei de registrar um pedido, ou que a tela recusou o pedido
    Então continuo na C805T
    E nenhuma outra tela é aberta

  Cenário: Digitação não numérica
    Dado que digito letras em um dos campos de código ou de data
    Quando confirmo a transação
    Então a transação não segue
    E nada é registrado
```
