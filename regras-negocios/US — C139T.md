# US — C139T — Consultar os períodos registrados de um tipo de contrato

## Estória

Como **servidor de CRE**, quero **consultar, pelo tipo de contrato, os períodos que estão
registrados no histórico daquele tipo na minha secretaria**, para que **eu veja, num lugar
só, desde quando e até quando cada período vale e o que a versão registrada carrega**.

O período é a faixa de vigência do contrato: o dia, o mês e o ano em que ele começa e o dia,
o mês e o ano em que ele termina. Como essa faixa muda ao longo da vida do contrato, o
sistema guarda uma versão nova a cada mudança, e é esse conjunto de versões que forma o
histórico do tipo de contrato. Quem presta contas, refaz um cálculo ou responde a um órgão de
controle depende dessa lista: sem ela, saber o que ficou registrado sobre a vigência de um
tipo de contrato exigiria percorrer os registros um a um. Esta tela só mostra — quem registra
as versões não é ela.

## Contexto

Jornada S000M → C000M → C020M → C139T (4 passos).

Ator: servidor de CRE — consulta, pelo tipo de contrato, os períodos registrados no histórico
daquele tipo dentro do tipo de órgão da sua sessão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O `C000M` e o `C020M` são menus: só encaminham para a tela e não deixam dado de negócio
nenhum — o modo de operação da `C139T` não vem deles, e a própria tela só opera em consulta.
O que ela usa da sessão — o **tipo de órgão** do vínculo, a matrícula, o código de acesso, o
privilégio e a CRE de quem opera — foi deixado pela entrada; é o tipo de órgão que delimita o
histórico que ela percorre.

A `C139T` termina nela mesma: não encadeia para outra tela, não passa registro nem operação
adiante, e não tem opções de saída. Chegando com a indicação de uma **tela de retorno**
preenchida, ela abandona a consulta e devolve o servidor à tela indicada (RN-11).

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela é de consulta: a única opção aceita é a de consulta

A tela abre em modo de consulta e repõe esse modo sozinha quando não há opção lembrada, de
modo que quem apenas abre a tela consulta. Se o servidor informar qualquer outra opção de
manutenção, a tela recusa com **\* Opcao nao disponivel. Use CON \***, devolve o cursor ao
campo da opção e para ali: nada é lido nesse caminho. Não há nesta tela inclusão, alteração
nem exclusão de período — a lógica de rota, que toda mensagem atravessa, também recusa a
opção que não reconhece (RN-09).

[?] A mensagem manda usar **CON**, e a conferência compara o que foi informado com o código
de consulta que a tabela de mensagens do idioma define — a mesma tabela de que a mensagem tira
a palavra "CON". Essa tabela não está no lote. Se ela não trouxer **CON** como código da
consulta, a conferência recusa toda opção — inclusive a consulta que a própria mensagem pede
— e a tela não consulta nada. Pergunta ao site.

### RN-02 — O histórico percorrido é o dos períodos daquele tipo de contrato, no tipo de órgão da sessão

A consulta é pelo **tipo de contrato**; não se informa contrato, fornecedor, CRE nem data. O
sistema percorre o histórico **do tipo de órgão que veio do vínculo do servidor** — os
períodos de um tipo de contrato de outra secretaria não aparecem — na ordem em que o próprio
histórico é chaveado: **tipo de órgão, tipo de contrato e a data de início do período**. Cada
leitura preenche **um bloco**, e a tela monta **três blocos**, parando no terceiro.

O histórico comporta **10.000 registros** — capacidade declarada (máximo esperado, parâmetro
de dimensionamento), não o volume já registrado. Quem o alimenta é a geração do contrato e do
período do tipo de contrato: a cada mudança da data limite ela registra uma versão nova, com
a matrícula de quem operou e a data e a hora. Esta tela não registra versão nenhuma.

[?] O efeito do recurso de posicionamento usado nas leituras não está no corpus nem no
manual: a procura vai montada com o **ano de início zerado**, e os blocos seguintes são lidos
sem remarcar essa posição. Se a procura exigir a **data exata**, um período com o ano zerado
não existe, a tela não acha nada e nunca mostra período; se ela aceitar a **primeira posição
igual ou posterior**, a tela mostra os primeiros períodos daquele tipo de contrato. Também
não se sabe se cada bloco seguinte **avança** na lista ou **repete** o período anterior — ou
seja, se os três blocos trazem três períodos diferentes. **Disso depende a consulta existir.**
Pergunta ao site.

[?] Como se vê o quarto período: a tela monta três blocos e para, e o material lido não
descreve nenhum caminho de continuação da lista. Se existe forma de ver os períodos
seguintes, ela não foi determinada. Pergunta ao site.

[?] De onde a tela tira o tipo de órgão: ela o lê da área de trabalho da sessão — a mesma
de onde lê a matrícula, o código de acesso e a CRE —, e o lote só inicializa essa área em
branco; os únicos pontos do acervo que lhe dão valor são de rotinas de outras telas, fora
deste caminho. Se em execução ela chegar vazia, o tipo de órgão fica zero e a consulta
procura o histórico de um órgão que não existe. Pergunta ao site.

### RN-03 — De cada período a tela aproveita doze dados

De cada registro do histórico a tela aproveita **doze dados**: o dia, o mês e o ano de início
do período; o dia, o mês e o ano limite; o tipo de licitação; a descrição do contrato; a
descrição do período; a indicação do pedido de cálculo; a indicação da tabela quinzena; e o
número com sinal e duas casas decimais.

A **descrição do tipo de licitação** não está no histórico: a tela a busca no cadastro dos
tipos de licitação e, não achando, deixa essa descrição em branco sem apresentar recusa
nenhuma. A indicação do **pedido de cálculo** o histórico guarda como uma letra, e a tela a
apresenta como **Sim** ou **Nao**; a indicação da **tabela quinzena** o histórico guarda como
uma letra, **N** (normal) ou **E** (especial). O número com sinal e duas casas decimais é
mostrado com o seu sinal.

O histórico guarda ainda outros dados que esta consulta não aproveita: a outra data do
período, a matrícula de quem registrou a versão e a data e a hora em que ela foi registrada.

[?] O que o número com sinal e duas casas decimais representa no negócio — se é um
percentual, um valor de desconto ou outra grandeza — não está no material lido: o cadastro
não traz rótulo nem mensagem que o nomeie. Pergunta ao site.

### RN-04 — Informar o tipo de contrato é obrigatório

Chegando sem tipo de contrato, o sistema recusa com **\* Informe o tipo contrato \*** e
devolve o cursor ao campo do tipo de contrato. A conferência é feita uma vez por mensagem,
não uma vez por bloco.

### RN-05 — O tipo de contrato informado precisa ter período registrado

Ao receber o tipo de contrato, o sistema procura no histórico um período daquele tipo dentro
do tipo de órgão da sessão. Não achando nenhum, recusa com
**\* Tipo contrato sem historico cadastrado \*** e devolve o cursor ao campo do tipo de
contrato. Achando, aceita o tipo, **lembra-o** para as apresentações seguintes e devolve a
posição da leitura ao começo do histórico.

A procura é dispensada quando o tipo informado é o mesmo que já está lembrado: nesse caso a
tela aceita o tipo sem reler o histórico para conferi-lo.

### RN-06 — Ao ser apresentada, a tela mostra o histórico do tipo de contrato lembrado

A montagem da tela lê o histórico do **tipo de contrato que ela tem lembrado** e preenche os
três blocos. Na primeira abertura da sessão não há tipo lembrado: nenhum período é lido e a
tela abre em branco, já em consulta. Havendo tipo lembrado e nenhum período no histórico, o
aviso é **\* Nao existe historico cadastrado \***, com o cursor no campo do tipo de contrato.

Fora dos blocos a tela mostra a **data do sistema** e a **descrição do tipo de órgão** da
sessão.

[?] O aviso de que não existe histórico só aparece depois de a tela ter aceitado o tipo de
contrato — e aceitá-lo exige ter achado um período daquele tipo no mesmo histórico. Se o tipo
só passa quando o período existe, esse aviso não tem como aparecer pelo caminho normal: ou
ele serve a outra situação, ou o caminho ficou inalcançável. Pergunta ao site.

[?] Quem preenche a data do sistema e a descrição do tipo de órgão: a tela as recebe da área
da sessão, e a árvore expandida só as inicializa em branco. Se ninguém as preencher, os dois
campos saem vazios. Pergunta ao site.

[?] O que o servidor vê na resposta à mensagem em que informa o tipo de contrato depende de o
ambiente remontar a tela depois de responder, e isso não está no lote: a leitura do histórico
está no caminho da montagem, e o caminho da mensagem só confere o tipo, o lembra e limpa as
descrições. Se o ambiente não remontar, a resposta sai com os blocos como foram digitados e
com as descrições em branco. Pergunta ao site.

### RN-07 — Os dados dos blocos não comandam a consulta

Os campos de dia, mês e ano de início e de limite, o tipo de licitação, o número e as
indicações passam por edição quando a mensagem chega — data e número são conferidos —, mas
**não escolhem o que é mostrado**: quem decide o que aparece é o tipo de contrato lembrado, e
a tela reescreve nesses campos o que leu do histórico. Nenhuma data digitada entra na procura.
O único campo ao qual a tela devolve o cursor por erro de digitação é o do tipo de contrato.

[?] Se a máscara deixa o servidor digitar nesses campos, não está no material lido: o texto
da tela está na máscara, que não faz parte do lote, e a tela os reescreve com o que veio do
histórico. Pergunta ao site.

### RN-08 — Cada mensagem começa com as descrições e o contexto em branco

Antes de conferir a digitação e de ler qualquer período, a tela apaga a descrição do contrato,
a descrição do período, a descrição da licitação, a indicação do pedido de cálculo, a
descrição do tipo de órgão e a data do sistema. Uma mensagem recusada não deixa na tela o
resultado da consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe um
caminho de entrada em que esses campos não são limpos, não foi possível determinar. Pergunta
ao site.

### RN-09 — Antes de consultar, o sistema confere o acesso

Toda apresentação da tela passa por duas conferências, com o contexto da sessão. A tela
precisa estar no cadastro de telas e relatórios — não estando, a recusa é
**\* Tela nao disponivel \*** — e a matrícula precisa ter a tela no seu código de acesso —
não tendo, a recusa é **\* Acesso negado para esta matricula \***. A mensagem do servidor
passa ainda pela lógica de rota, que recusa a tela retirada do cadastro
(**\* Tela nao cadastrada \***) e a opção que ela não reconhece
(**\* Operacao nao disponivel \***), e pela conferência de permissão por operação. Em
qualquer dessas recusas nada é lido e nada é mostrado.

[?] A conferência de permissão por operação não procura a autorização de consulta: as marcas
que ela lê são as de inclusão, alteração e exclusão, e a consulta passa sem conferência
nenhuma. Quem tem a tela autorizada consulta mesmo sem a permissão de consulta. Se a intenção
era exigi-la, o caminho não a exige. Pergunta ao site.

### RN-10 — A consulta não grava nada e não deixa rastro de auditoria

A tela e as rotinas comuns que ela chama só leem: nenhum registro é incluído, alterado ou
excluído e nenhum registro de auditoria é gerado. As operações de gravação, de exclusão e de
travamento existem declaradas para os cadastros que a tela enxerga, mas **não são executadas
em nenhum caminho** — declarar não é executar.

### RN-11 — Chegando com a tela de retorno indicada, a consulta é abandonada

Se a transação chegar com a indicação de **tela de retorno** preenchida — o dado que a rota
usa para devolver o servidor a outra tela —, a consulta é abandonada: nada é lido, nada é
validado e o servidor é levado à tela indicada.

[?] Nada nesta jornada preenche essa indicação — o caminho até a tela é a opção de um menu,
que só nomeia a tela —, e o lote não diz quem a preenche nem para onde ela levaria. Pergunta
ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar os períodos registrados de um tipo de contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C139T

  Cenário: A consulta mostra os períodos do tipo de contrato informado
    Dado que o tipo de contrato tem períodos registrados no meu tipo de órgão
    Quando consulto
    Então vejo os períodos em três blocos
    E cada bloco traz o dia, o mês e o ano de início do período e o dia, o mês e o ano limite
    E cada bloco traz a descrição do contrato, a descrição do período e o tipo de licitação com a sua descrição
    E cada bloco traz a indicação do pedido de cálculo, mostrada como Sim ou Nao
    E cada bloco traz a indicação da tabela quinzena e o número com sinal e duas casas decimais

  Cenário: A consulta é a do meu tipo de órgão
    Dado que existem períodos do tipo de contrato informado em outro tipo de órgão
    Quando consulto
    Então vejo apenas os períodos do tipo de órgão da minha sessão

  Cenário: A tela apresenta até três períodos por vez
    Dado que o tipo de contrato tem períodos registrados
    Quando consulto
    Então a tela apresenta três blocos e para no terceiro

  Cenário: A tela abre em consulta e sem períodos
    Dado que ainda não usei a tela nesta sessão
    Quando abro a tela C139T
    Então a tela abre em consulta
    E nenhum período é lido, porque ainda não há tipo de contrato lembrado

  Cenário: Opção diferente da consulta é recusada
    Dado que estou na tela C139T
    Quando informo uma opção diferente da consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nenhum período é lido nesse caminho

  Cenário: Tipo de contrato em branco é recusado
    Dado que estou na tela C139T
    Quando envio a mensagem sem informar o tipo de contrato
    Então vejo a mensagem "* Informe o tipo contrato *"
    E o cursor volta ao campo do tipo de contrato

  Cenário: Tipo de contrato sem período registrado é recusado
    Dado que o tipo de contrato informado não tem período registrado no meu tipo de órgão
    Quando informo esse tipo de contrato
    Então vejo a mensagem "* Tipo contrato sem historico cadastrado *"
    E o cursor volta ao campo do tipo de contrato

  Cenário: Tipo de contrato já lembrado é aceito sem nova procura
    Dado que informei um tipo de contrato e ele foi aceito
    Quando informo outra vez o mesmo tipo de contrato
    Então a tela aceita o tipo sem reler o histórico para conferi-lo

  Cenário: O tipo de contrato lembrado não tem período no histórico
    Dado que a tela tem um tipo de contrato lembrado
    E nenhum período desse tipo existe no meu tipo de órgão
    Quando a tela é apresentada
    Então vejo a mensagem "* Nao existe historico cadastrado *"
    E o cursor fica no campo do tipo de contrato

  Cenário: O período aponta um tipo de licitação que não existe no cadastro
    Dado que o período registrado aponta um tipo de licitação que não existe no cadastro
    Quando consulto
    Então o bloco do período aparece com a descrição da licitação em branco
    E nenhuma recusa é apresentada

  Cenário: O que aparece nos blocos não vem do que foi digitado
    Dado que estou na tela C139T com períodos mostrados
    Quando altero as datas de um bloco e envio a mensagem
    Então a consulta continua sendo a do tipo de contrato lembrado
    E os campos dos blocos são reescritos com o que está no histórico

  Cenário: Cada mensagem começa com as descrições e o contexto em branco
    Dado que a tela mostrou a descrição do contrato, a do período e a da licitação
    Quando respondo uma mensagem
    Então essas descrições, a indicação do pedido de cálculo, a descrição do tipo de órgão e a data do sistema voltam em branco

  Cenário: A consulta não grava nada
    Dado que abro a tela C139T e os períodos são mostrados
    Quando a consulta termina
    Então nenhum período é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Tela não cadastrada
    Dado que a tela C139T não está no cadastro de telas e relatórios
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo consultar

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela C139T no seu código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo consultar

  Cenário: Tela retirada do cadastro de telas e relatórios
    Dado que a tela C139T foi retirada do cadastro de telas e relatórios
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"
    E não consigo consultar

  Cenário: Opção não reconhecida pela rota
    Dado que estou na tela C139T
    Quando confirmo uma mensagem com uma opção que a rota não reconhece
    Então vejo a mensagem "* Operacao nao disponivel *"
    E não consigo consultar

  Cenário: Consulta sem autorização específica de operação
    Dado que o meu código de acesso tem a tela C139T autorizada
    Quando consulto
    Então nenhuma autorização de operação me é exigida

  Cenário: Tela de retorno preenchida abandona a consulta
    Dado que a transação chega à C139T com a indicação de tela de retorno preenchida
    Quando a consulta começaria
    Então o processamento é abandonado e nada é lido
    E o servidor é levado à tela indicada
