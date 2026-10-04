# US — C065T — Apostilamento das permissões da CRE

## Estória

Como **servidor da Coordenação Regional Escolar (CRE)**, quero **pedir o processamento do
apostilamento das permissões de um contrato para os grupos da minha coordenação** — e, quando
ele já estiver calculado, **abrir os itens do contrato para lançá-lo** —, para que **o valor
apostilado das permissões seja calculado e registrado, e os itens possam ser lançados e
conferidos**.

O apostilamento é o reajuste posterior de uma permissão de fornecimento, e ele não acontece
sozinho: alguém tem de pedir que ele seja processado para um contrato, dentro do período da
permissão e a partir de uma data base escolhida. É isso que esta tela faz, e é por ela que o
pedido alcança os grupos da coordenação. **Sem o pedido, o processamento não roda para aqueles
grupos e o valor apostilado das permissões não é calculado**; e, quando o cálculo já existe, é
por esta mesma tela que se chega aos itens do contrato, onde o apostilamento é lançado.

## Contexto

Jornada S000M → C000M → C050M → C066M → C065T (5 passos).
Ator: servidor de CRE — informa o tipo de contrato, o período da permissão, a data base, os
grupos e a impressora, e emite o pedido de processamento do apostilamento; ou abre os itens do
contrato para lançá-lo.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Além do menu, esta tela também é alcançada por **encadeamento**, sem menu no meio: a tela de
cálculo do apostilamento (`C062T`) entrega a transação direto a ela, já com o contrato montado
a partir da permissão que estava sendo trabalhada — e ela, por sua vez, entrega a transação à
tela de itens do contrato (`C066T`) quando o apostilamento já está calculado. O que chega pela
entrega da `C062T` e o que sai na entrega à `C066T` são regras desta estória (RN-08 e RN-16).

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — Esta tela pede o apostilamento, e o único registro que ela cria é a requisição

Esta tela não lança valor, não corrige contrato e não mexe em permissão: ela **pede** o
processamento do apostilamento de um contrato para um conjunto de coordenações regionais, e o
único registro que ela cria é a **requisição** desse pedido. O que ela enxerga são cinco
cadastros — o das telas do sistema, o das requisições, o das permissões de contrato, o da
liberação das telas por tipo de licitação e o dos funcionários com as suas sessões — e, para
cada um deles, o sistema traz prontas uma operação de gravar e uma de apagar. Aqui **nenhuma
dessas operações prontas é executada**: a única gravação é a da requisição, feita depois de
todas as conferências.

Os números de capacidade são de dimensionamento, não volume cadastrado: as telas do sistema
comportam 2.000 registros, as requisições 90.000, as permissões de contrato 1.000.000, a
liberação das telas por tipo de licitação 1.000 e os funcionários 20.000.

### RN-02 — O órgão e o servidor vêm da sessão, e não se digitam

O tipo de órgão é o da secretaria que o vínculo da matrícula escolheu na entrada e que ficou
na sessão; é ele que identifica o acervo consultado e o pedido criado, e não há campo para
informá-lo. Da sessão vêm também a **matrícula** que assina o pedido, o **código de acesso**,
o **privilégio**, a **coordenação regional** e a **estação**; do relógio do sistema vêm a data
e a hora. O cabeçalho da tela apenas mostra a descrição do tipo de órgão e a data do sistema.

### RN-03 — O que se informa: o contrato, o período, a data base, os grupos e a impressora

Os campos com rótulo na tela são **sete**: o tipo de contrato, as três partes do início do
período da permissão (dia, mês e ano) e as três partes da data limite. Além deles informam-se
o **tipo de licitação**, as três partes da **data base**, até **doze códigos de coordenação
regional escolar** — os grupos para os quais o apostilamento deve ser processado — e a
**impressora**. A descrição do tipo de licitação é mostrada ao lado do código.

[?] A descrição do tipo de licitação não é buscada em cadastro nenhum por esta tela: ela só
chega preenchida quando a tela anterior a entrega. Vinda do menu, não se lê de onde o código
da descrição sairia. Pergunta ao site.

### RN-04 — Os campos informados são conferidos como número antes de qualquer consulta

Os **vinte e três** campos informados — o tipo de contrato, as três partes do início do
período, as três partes da data limite, o tipo de licitação, as três partes da data base e os
doze grupos — passam pela edição numérica antes de o sistema ler qualquer cadastro. O que
estiver em branco é tratado como zero, e o que não for número é recusado no próprio campo,
com o cursor de volta a ele, sem que nenhum cadastro seja consultado.

[?] A recusa devolve o cursor sozinha para **dezenove** desses campos; para as três partes do
início do período e para o tipo de licitação isso não acontece. A fonte não diz onde o cursor
fica nesses quatro casos. Pergunta ao site se é intencional.

### RN-05 — A tela só executa a alteração

A operação informada tem de ser a de **alteração**. Um código de operação que o sistema não
conhece é recusado pelo próprio roteamento, com **\* Operacao nao disponivel \***, e a
transação não segue; um código conhecido que não seja o de alteração é recusado por esta tela,
com **\* Operacao nao disponivel. Use ALT \*** e o cursor de volta ao campo da operação — e
nada é gravado. Ao se apresentar, é a própria tela que escreve a operação como alteração.

[?] A recusa manda usar ALT, mas a conferência compara o que foi informado com o código
interno de alteração — o mesmo valor que a tela escreve nesse campo quando ninguém deixou
operação. Ou o terminal traduz o mnemônico antes de enviar, ou a mensagem está desalinhada da
conferência. Pergunta ao site; não concluo qual dos dois.

### RN-06 — Só quem tem a tela no perfil e a alteração liberada passa

Antes de ler qualquer cadastro, a tela pede ao sistema de segurança que confira a **matrícula**
e a **tela**; na confirmação do que foi informado, pede a conferência da **operação**. Sem o
perfil de acesso à tela, a transação é recusada com **\* Acesso negado para esta matricula \***;
sem a tela cadastrada, com **\* Tela nao disponivel \***; e, faltando a liberação de alteração
no perfil, com **\* Acesso negado para esta operacao \***. Em qualquer dos casos nada é lido e
nada é gravado.

### RN-07 — Uma requisição pendente para o órgão bloqueia o pedido novo

Antes de conferir o que foi informado, a tela procura no cadastro de requisições uma
requisição de apostilamento **ainda pendente para o órgão da sessão**, seja qual for a
coordenação regional. Existindo, o pedido é recusado com
**\* Relatorio em processamento. Aguarde. \***, com o cursor de volta ao campo do tipo de
contrato, e nada é lido nem gravado. É uma requisição por órgão: o próprio processamento apaga
a requisição quando a executa, e só então a tela volta a aceitar pedido.

### RN-08 — A tela muda conforme quem a chamou: da tela de cálculo ela abre preenchida

A tela compara a marca da tela de origem com o código da tela de cálculo do apostilamento
(`C062T`). Vindo de lá, ela abre **preenchida** com o tipo de contrato, o início e o limite do
período, a data base, o tipo de licitação com a sua descrição e a coordenação regional da
permissão que estava sendo trabalhada — esta vai para o **primeiro** dos doze grupos, e o
cursor fica no segundo, convidando o servidor a informar os demais. Vindo do menu, sem essa
marca, ela abre **em branco**, e é o servidor que informa tudo. Nos dois casos ela abre em
alteração.

### RN-09 — O pedido exige pelo menos um grupo informado

Sem nenhum dos doze grupos preenchido, a tela não pede nada: recusa com
**\* Informe os grupos para o calculo \***, com o cursor de volta ao primeiro grupo, e nada é
lido nem gravado.

### RN-10 — Cada grupo informado tem de ter permissão para o contrato e o período

Para cada grupo informado, o sistema procura a permissão de contrato do órgão da sessão com
aquele tipo de contrato e aquela data limite. Encontrando, ele guarda o **início** e o
**limite** do período da permissão, que passam a valer para as conferências seguintes.
Não encontrando — grupo sem permissão para esse contrato e essa data limite —, o pedido é
recusado com **\* Grupo sem registros para o apostilamento \***, com o cursor de volta ao grupo
culpado, e nada é gravado. Basta **um** grupo sem permissão para o pedido inteiro não sair.

[?] A coordenação regional, o tipo de contrato e as três partes da data limite são conferidos
contra a permissão lida; como a classe, a subclasse e o gênero participam dessa procura não se
sustenta pelo material desta jornada — a tela não informa esses códigos e o que se lê depois
não os compara.

### RN-11 — O tipo de licitação da permissão tem de ter esta tela liberada

Cada permissão tem um tipo de licitação, e a liberação desta tela por tipo de licitação é um
cadastro à parte. Não estando a tela liberada para o tipo de licitação da permissão, o pedido é
recusado com **\* Tela nao disponivel para esta licitacao \***, com o cursor de volta ao grupo,
e nada é gravado.

### RN-12 — A data base tem de cair dentro do período da permissão

Montada a data base, ela é comparada com o início e com o limite do período lidos da permissão.
Antes do início, a recusa é **\* Data base menor que data inicio da permissao \***; depois do
limite, **\* Data base maior que data limite da permissao \***. Nas duas o cursor volta ao
campo da data base, e nada é lido nem gravado. O período usado nessas comparações é o da
permissão achada, não o que estiver no cabeçalho.

### RN-13 — A impressora é obrigatória

Sem impressora informada, o pedido é recusado com **\* Informe a impressora \***, com o cursor
de volta ao campo, e nada é gravado.

[?] O pedido leva duas impressoras: a que o servidor informa aqui vai no pedido de
processamento, e a requisição criada guarda outra — a última usada na sessão por qualquer tela
que imprima. O material não diz qual das duas o processamento usa para imprimir. Pergunta ao
site.

### RN-14 — O que o pedido registra e o que ele manda processar

Passando por todas as conferências, o sistema cria a requisição do pedido com o **número
seguinte ao da última requisição**, o órgão da sessão, a matrícula do servidor, a estação, a
data do dia, a impressora informada, o tipo de contrato, a data limite do período, a data base
e os grupos informados — juntos, em até doze códigos de duas posições. A operação registrada é
a de **inclusão**, porque é uma requisição nova.

Em seguida a tela manda processar o **relatório de apostilamento do contrato** (relatório
C61007), levando a mesma relação de grupos e a mesma chave do contrato, **uma cópia**, a
estação e o correio eletrônico do servidor, buscado no cadastro de funcionários pela matrícula.
A tela não tem mensagem própria de sucesso: ela reapresenta o estado devolvido pelo
processamento. A partir daí o pedido está pendente, e é a requisição criada que segura a tela
(§RN-07) até o processamento executá-lo.

### RN-15 — A marca de apostilamento troca o pedido pela abertura dos itens

A tela tem uma marca de apostilamento, de um caractere. Preenchida com **S**, ela não emite
pedido nenhum: procura, para a coordenação regional, o tipo de contrato e o período que
**recebeu de quem a chamou**, as permissões que já têm valor apostilado. Havendo pelo menos
uma, ela entrega a transação à tela de itens do contrato (`C066T`), sem gravar nada aqui. Não
havendo nenhuma, recusa com **\* Nao existem registros a atualizar \***, com o cursor de volta
ao campo do tipo de contrato. Em branco, a marca não interfere: a tela emite o pedido (RN-14).

[?] A marca não tem rótulo validado e a fonte não mostra quem a preenche — se o servidor a
digita ou se ela chega com a transação. O que se lê é o efeito de cada valor: com S a tela abre
os itens; em branco, ela emite o pedido.

[?] Por esse caminho a tela confere e entrega os dados que **recebeu de quem a chamou**, e não
os que estão na tela: se o servidor corrigir um campo antes de confirmar, a correção não vale
neste caminho — ele segue com os dados da entrega, e os da tela só valem para o pedido. Se é
intencional, pergunta ao site.

### RN-16 — O que a tela entrega à tela de itens do contrato

Na entrega, a tela passa o **código dela como origem**, a **operação de alteração**, o tipo de
contrato, o **início e o limite do período**, a data base, o tipo de licitação com a sua
descrição e a coordenação regional. A tela de itens do contrato (`C066T`) abre em alteração com
esses dados e limpa os códigos de item, para o servidor escolher, item a item, o que apostilar.
Sem essa entrega, quem lesse a tela de itens isolada não teria como refazer o caminho.

### RN-17 — O que não grava nada: a apresentação e as recusas

Ao se apresentar, antes de o servidor informar qualquer coisa, a tela **não grava nada**: lê o
nome da tela, monta o cabeçalho com a descrição do tipo de órgão e a data do sistema e marca a
operação como alteração. Também não gravam nada as recusas de RN-05 a RN-13 e a abertura dos
itens de RN-15: a única gravação da tela é a requisição do pedido (RN-14), e nada mais.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedido de processamento do apostilamento das permissões da CRE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C065T

  Cenário: RN-01, RN-02 e RN-14 — o pedido de apostilamento é emitido
    Dado que não há requisição de apostilamento pendente para o meu órgão
    E existe permissão para o tipo de contrato, a data limite e o grupo que informei
    E esta tela está liberada para o tipo de licitação da permissão
    E a data base que informei cai dentro do período da permissão
    Quando informo o tipo de contrato, o período, a data base, o grupo e a impressora
    Então o sistema cria a requisição do pedido, com o número seguinte ao da última requisição
    E a requisição é do órgão da minha sessão, com a minha matrícula, a estação e a data do dia
    E o processamento do relatório de apostilamento é mandado rodar com os mesmos grupos e a mesma chave
    E nenhum contrato e nenhuma permissão são alterados por esta tela

  Cenário: RN-02 — o órgão do pedido é o da minha sessão
    Dado que estou na tela com o vínculo da minha matrícula
    Quando confirmo o pedido
    Então ele vale para o acervo do órgão da minha sessão
    E não há campo na tela para eu informar outro órgão

  Cenário: RN-03 — os grupos do pedido
    Dado que informei doze grupos de coordenação regional
    Quando confirmo o pedido
    Então os doze códigos vão juntos na requisição e no processamento
    E os grupos que deixei em branco não entram

  Cenário: RN-04 — campo não numérico
    Quando preencho o tipo de contrato, uma das datas, o tipo de licitação ou um grupo com letra
    Então a tela recusa o campo antes de qualquer consulta de cadastro
    E o cursor volta ao campo
    E nada é gravado

  Cenário: RN-05 — operação que não é a alteração
    Quando informo no campo da operação um código de inclusão, de exclusão ou de consulta
    Então vejo "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: RN-05 — operação desconhecida
    Quando informo no campo da operação um valor que o sistema não conhece
    Então vejo "* Operacao nao disponivel *"
    E a transação não segue

  Cenário: RN-06 — sem perfil de acesso à tela
    Dado que a minha matrícula não tem perfil de acesso a esta tela
    Quando confirmo o pedido
    Então vejo "* Acesso negado para esta matricula *"
    E nada é lido e nada é gravado

  Cenário: RN-06 — sem permissão para alterar
    Dado que o meu perfil tem esta tela, mas não permite alterar
    Quando confirmo o pedido
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-07 — já existe uma requisição de apostilamento pendente
    Dado que o meu órgão tem uma requisição de apostilamento ainda pendente
    Quando confirmo o pedido
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo do tipo de contrato
    E nenhuma requisição nova é criada

  Cenário: RN-08 — a tela aberta pela tela de cálculo do apostilamento
    Dado que vim da tela de cálculo do apostilamento C062T, com uma permissão trabalhada
    Quando a tela C065T se apresenta
    Então ela já está preenchida com o tipo de contrato, o período, a data base, o tipo de licitação e a coordenação regional daquela permissão
    E o cursor está no segundo grupo

  Cenário: RN-08 — a tela aberta pelo menu
    Dado que vim do menu, sem permissão entregue por outra tela
    Quando a tela C065T se apresenta
    Então ela está em branco
    E sou eu que informo o tipo de contrato, o período, a data base, os grupos e a impressora

  Cenário: RN-09 — nenhum grupo informado
    Quando confirmo o pedido sem informar nenhum dos doze grupos
    Então vejo "* Informe os grupos para o calculo *"
    E o cursor volta ao primeiro grupo
    E nada é gravado

  Cenário: RN-10 — grupo sem permissão para o contrato e o período
    Dado que um dos grupos que informei não tem permissão para aquele tipo de contrato e aquela data limite
    Quando confirmo o pedido
    Então vejo "* Grupo sem registros para o apostilamento *"
    E o cursor volta ao grupo culpado
    E nenhuma requisição é criada

  Cenário: RN-11 — a tela não está liberada para o tipo de licitação da permissão
    Dado que a permissão existe, mas esta tela não está liberada para o tipo de licitação dela
    Quando confirmo o pedido
    Então vejo "* Tela nao disponivel para esta licitacao *"
    E o cursor volta ao grupo
    E nada é gravado

  Cenário: RN-12 — data base antes do início do período
    Dado que a data base que informei é anterior ao início do período da permissão
    Quando confirmo o pedido
    Então vejo "* Data base menor que data inicio da permissao *"
    E o cursor volta ao campo da data base
    E nada é gravado

  Cenário: RN-12 — data base depois do limite do período
    Dado que a data base que informei é posterior ao limite do período da permissão
    Quando confirmo o pedido
    Então vejo "* Data base maior que data limite da permissao *"
    E o cursor volta ao campo da data base
    E nada é gravado

  Cenário: RN-13 — sem impressora
    Quando confirmo o pedido sem informar a impressora
    Então vejo "* Informe a impressora *"
    E o cursor volta ao campo da impressora
    E nada é gravado

  Cenário: RN-14 — o que a requisição do pedido registra
    Dado que confirmei o pedido com os grupos e a impressora informados
    Então a requisição guarda o órgão, a minha matrícula, a estação, a data do dia e a impressora informada
    E guarda o tipo de contrato, a data limite do período, a data base e os grupos informados
    E o processamento do relatório de apostilamento é enviado com uma cópia e com o meu correio eletrônico

  Cenário: RN-15 — a marca de apostilamento, com valor apostilado na permissão
    Dado que vim da tela de cálculo do apostilamento, com o contrato entregue
    E a permissão daquele contrato já tem valor apostilado
    Quando confirmo com a marca de apostilamento preenchida
    Então a transação passa para a tela de itens do contrato C066T
    E nada é gravado por esta tela

  Cenário: RN-15 — a marca de apostilamento, sem valor apostilado
    Dado que a permissão do contrato que recebi ainda não tem valor apostilado
    Quando confirmo com a marca de apostilamento preenchida
    Então vejo "* Nao existem registros a atualizar *"
    E o cursor volta ao campo do tipo de contrato
    E a transação não segue

  Cenário: RN-16 — o que a tela entrega à tela de itens do contrato
    Dado que a tela entregou a transação à C066T
    Então a C066T abre em alteração, com o tipo de contrato, o período, a data base, o tipo de licitação e a coordenação regional recebidos
    E os códigos de item chegam limpos, para eu escolher o que apostilar

  Cenário: RN-17 — a apresentação e as recusas não gravam nada
    Dado que abri a tela e não confirmei nada
    Então nenhuma requisição é criada
    E o cabeçalho mostra a descrição do tipo de órgão e a data do sistema
    Quando confirmo um pedido que é recusado
    Então nenhuma requisição é criada
    E nenhuma permissão é alterada
```
