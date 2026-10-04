# US — E029T — Alterar o período de entrega de um pedido de alimentação escolar

## Estória

Como **servidor de CRE**, quero **remarcar os dias de entrega de um pedido de
alimentação escolar já aprovado, informando o órgão, a coordenadoria regional
escolar, o número do pedido, o ano da entrega e o novo período**, para que **uma
entrega que não pode sair nas datas previstas — porque caiu em feriado, porque o
preparo mudou, porque o fornecedor não entrega naquele dia — seja reprogramada
para os dias certos sem ter de refazer o pedido**.

O período de entrega é o compromisso que o fornecedor tem de cumprir, e ele nasce
junto com o preparo do pedido: depois de aprovado, quem lançou o pedido não o
corrige mais, e é esta tela que o reprograma. A alteração não fica presa ao
pedido informado: os pedidos preparados no mesmo momento saem juntos para o mesmo
fornecedor, e o período deles é reescrito junto — deixar um deles no período velho
partiria a entrega em duas. Quando algum deles já andou mais longe, a alteração
recua e fica só no pedido informado, para não desmanchar o que já foi entregue.

## Contexto

Jornada S000M → E000M → E010M → E029T.

Ator: servidor de CRE — informa o órgão, a coordenadoria regional escolar, o
número do pedido, o ano da entrega e o novo período de entrega, confere o que a
tela mostra e confirma a alteração.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio.

Da sessão a tela usa a matrícula, o código de acesso, a estação, o tipo de órgão,
a coordenadoria regional escolar e o órgão filho do vínculo, além da descrição do
tipo de órgão e da data do sistema para o cabeçalho. As três telas anteriores da
jornada não passam registro nem operação adiante: elas apenas levam a esta tela,
e **não deixam período, pedido nem operação prontos** — o pedido é montado aqui, a
partir do ano da entrega e do número do pedido que o servidor digita, e a operação
é a própria tela que põe. Por isso nada do que a tela faz no modo de alteração vem
de quem a chamou.

A tela não encadeia para outra: ela não passa registro nem operação adiante, e
depois de gravar volta a ela mesma, com a mensagem de sucesso. O campo de código
da próxima tela existe e é repassado adiante, mas esta tela não o preenche; se
alguma coisa de fora o trouxer preenchido, a transação é desviada para a tela
indicada antes de qualquer gravação — e não se conclui do acervo quem o preenche.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela altera o período de entrega, e só isso

A tela não inclui e não exclui nada: a única operação que ela executa é a
alteração. Ao ser aberta, ela mesma põe a operação de alteração no campo da
operação e exige que a transação volte com ela; qualquer outra é recusada com
**\* Opcao nao disponivel. Use ALT \***, o cursor volta ao campo da operação e nada
é gravado. Nenhuma exclusão é executada por esta tela, em caminho nenhum.

[?] A tela repõe a operação de alteração a cada abertura e manda usar a tecla ALT;
não se conclui do acervo se a tecla de outra operação sobrescreve esse campo — e,
nesse caso, o servidor veria a recusa. Pergunta ao site.

### RN-02 — A tela não mantém cadastro: lê doze cadastros e escreve em cinco

Para alterar, a tela consulta **doze cadastros**: o das telas, o dos órgãos, o dos
pedidos, o das linhas de gênero do pedido, o das permissões de entrega do
contrato, o da quantidade calculada do pedido, o dos fornecedores, o dos
operadores, o calendário de feriados, o das requisições de cálculo, e ainda os
dois que as conferências de acesso leem (o cadastro do servidor e o das
autorizações do código de acesso, RN-16). Escreve em **cinco**: grava o novo
período em cada linha de gênero dos pedidos alcançados, no próprio pedido, no
preparo dos pedidos alcançados e na requisição do pedido informado, e inclui um
registro de auditoria de cada linha de gênero e de cada pedido gravado, e da
requisição. Nenhum outro cadastro é incluído, alterado ou excluído, e a simples
abertura da tela não escreve nada.

Os cadastros são dimensionados para: pedidos **10 milhões**; linhas de gênero do
pedido **200 milhões**; requisições de cálculo **500 mil**; quantidade calculada
do pedido **80 milhões**; permissões de entrega **1 milhão**; feriados **10 mil**;
fornecedores **10 mil**; operadores **100**; telas **2 mil**; órgãos **12 mil**;
auditoria **60 milhões**. São capacidades — o máximo esperado no dimensionamento —,
não volumes cadastrados.

### RN-03 — Ao abrir, a tela propõe o órgão e a coordenadoria da sessão

Ao ser aberta, a tela preenche o órgão filho e a coordenadoria regional escolar
com os do vínculo da sessão, lê o cadastro do órgão para mostrar o nome, e mostra
no cabeçalho a descrição do tipo de órgão e a data do sistema. Quando o vínculo
não tem órgão filho, o campo do órgão fica em branco, para o servidor informar, e
o cursor fica nele; quando tem, o cursor fica no número do pedido; quando não tem
coordenadoria, o campo da coordenadoria fica em branco. Abrir a tela só lê: não
grava nem apaga nada.

[?] O órgão filho do vínculo não é preenchido por nenhuma das telas desta jornada,
e quem o preenche não está no acervo; a coordenadoria da sessão também não vem
destas telas. Sem os dois, a tela não tem por onde restringir o órgão informado
(RN-04): o recorte passa a ser só o que o servidor digitar. Pergunta ao site.

### RN-04 — O servidor só altera pedido do seu órgão e do seu grupo

Quando o vínculo da sessão carrega um órgão filho, o órgão informado tem de ser
esse; outro é recusado com **\* Usuario sem acesso a outro orgao \*** e o cursor
volta ao órgão. Passando por essa conferência, a coordenadoria usada nas demais é
a **do órgão cadastrado**, e não a que o servidor digitou: se o órgão estiver em
outra coordenadoria e o vínculo carregar uma, a recusa é
**\* Usuario sem acesso ao grupo deste orgao \***. Quando o vínculo não carrega
coordenadoria, é preciso informar órgão ou coordenadoria: com o órgão **e** a
coordenadoria em branco, a recusa é **\* Informe o orgao \***.

[?] Quando o vínculo tem coordenadoria mas **não** tem órgão filho, a
coordenadoria digitada não é comparada com a da sessão: as conferências que
impõem a coordenadoria do órgão e a comparam com a da sessão só são percorridas
se o órgão for informado, e o caminho que confere o pedido aceita o órgão em
branco. Assim, com o órgão em branco, um servidor do grupo 1 pode informar o
grupo 2 e alterar o pedido do grupo 2. Ou a sessão sempre traz o órgão filho — e
o caminho não acontece no site —, ou a recusa de grupo não vale nesse caso.
Pergunta ao site; não escolho um dos dois lados.

### RN-05 — O órgão informado tem de existir e ser da secretaria

O órgão tem de estar cadastrado: senão **\* Orgao nao cadastrado \***. E o tipo de
órgão tem de ser o da sessão (a secretaria do servidor), senão
**\* Orgao nao pertence a esta secretaria \***. Nas duas recusas o cursor volta ao
campo do órgão e nada é gravado. Na abertura, a tela salta os órgãos marcados como
excluídos; na conferência do órgão que o servidor informa essa marca não é
testada. A tela também não confere se o cadastro do órgão está completo.

[?] Há uma recusa que compara o nome do órgão com o texto "NAO CADASTRADO" para
dizer "**\* Orgao nao cadastrado \***", mas esta tela nunca escreve esse texto no
nome do órgão, e quem o escreveria não está no acervo. Ou a recusa vale para um
caso que já não acontece, ou ela depende de um caminho que não está no fonte.
Pergunta ao site.

[?] A abertura da tela salta os órgãos marcados como excluídos, mas a conferência
do órgão que o servidor informa não testa essa marca: um órgão excluído passa pela
conferência. Se isso é intencional, é pergunta ao site.

### RN-06 — O pedido é procurado pela coordenadoria, pelo número e pelo ano da entrega

O número do pedido (6 dígitos) e o ano da entrega (4 dígitos) formam juntos o
número de **10 dígitos** que identifica o pedido. A tela exige ao menos um dos
dois: com os dois zerados, a recusa é **\* Informe o numero do pedido \***, com o
cursor no número. A procura é feita pela secretaria da sessão, pela coordenadoria
(a do órgão, quando ele foi informado) e por esse número; não achando, a recusa é
**\* Pedido nao cadastrado \***. O órgão informado **não** faz parte da
identificação do pedido: ele serve para chegar à coordenadoria e para as
conferências de acesso — o pedido pertence à coordenadoria, e não ao órgão.

[?] O ano da entrega sozinho já faz a tela procurar o pedido (e responder "não
cadastrado"); a recusa de campo em branco só aparece com o número **e** o ano
zerados. Se o site espera a mensagem sempre que faltar o número, é pergunta ao
site.

### RN-07 — Os campos numéricos passam por edição numérica antes das conferências

Antes de qualquer conferência sobre o pedido, os **12 campos numéricos** — órgão
filho, coordenadoria, número do pedido, ano da entrega, código do fornecedor,
código do operador, dia, mês e ano do início do período e dia, mês e ano do
limite — passam por edição numérica, e o campo em branco é tratado como zero. A
operação e a resposta da confirmação não passam por essa edição.

[?] O que o servidor vê quando digita algo que não é número não se conclui desta
tela: a rotina que faz a edição não está no acervo. E a tela só sabe devolver o
cursor a nove desses campos — órgão, número do pedido, ano da entrega, as três
partes do início e as três do limite; um erro de digitação na coordenadoria, no
fornecedor ou no operador não tem posição de cursor definida. Pergunta ao site.

### RN-08 — Só um pedido aprovado, e não auxiliar de acumulado, pode ser alterado

O pedido não pode ser um auxiliar de pedido acumulado já calculado (senão
**\* Pedido auxiliar do acumulado calculado \***) e a sua situação tem de ser a de
aprovado: o pedido excluído é recusado com **\* Pedido excluido \***, o que já
saiu para distribuição com **\* Pedido pendente de distribuicao \***, o já fechado
com **\* Pedido aprovado - fechado \*** e o que ainda espera aprovação com
**\* Pedido pendente de aprovacao \***. Em todas as recusas o cursor fica no
número do pedido e nada é gravado.

[?] A tela recusa as quatro situações que conhece e deixa passar qualquer outra:
só uma situação diferente dessas chega às conferências seguintes. Se o site usar
outra, ela entra sem conferência. Pergunta ao site.

### RN-09 — O pedido não pode ter linha de gênero acumulada nem quantidade já recebida

Nenhuma das linhas de gênero do pedido pode estar marcada como de pedido
acumulado quando o próprio pedido é de um acumulado (senão
**\* Pedido com genero de pedido acumulado \***), e nenhuma linha pode ter
quantidade já recebida (senão **\* Pedido ja tem quantidades recebidas \***). Nas
duas recusas o cursor fica no número do pedido e nada é gravado.

### RN-10 — O novo período tem de ser válido, em dia útil, no ano do pedido e de até cinco dias

A data de início é obrigatória e tem de ser uma data válida (senão
**\* Data de inicio da entrega invalida \***) e o seu ano tem de ser o ano da
entrega do pedido (senão **\* Ano da entrega difere do ano do pedido \***). A
data limite, quando deixada em branco, é completada pela própria tela: o período
passa a terminar no **quinto dia de entrega**, contados só os dias úteis. Informar
exatamente o período que o pedido já tem é recusado com
**\* Informe o novo periodo de entrega \***.

Nem o início nem o fim podem cair em sábado ou domingo (senão
**\* Inicio da entrega nao deve ser um sabado \***,
**\* Inicio da entrega nao deve ser um domingo \***,
**\* Final da entrega nao deve ser um sabado \*** ou
**\* Final da entrega nao deve ser um domingo \***) nem em feriado do calendário
(senão **\* Inicio da entrega nao deve ser um feriado \*** ou
**\* Final da entrega nao deve ser um feriado \***). A data final tem de ser
válida (senão **\* Data final da entrega invalida \***) e não pode ser anterior à
inicial (senão **\* Data final menor que a data inicial \***). E o período,
contados só os dias de entrega, não pode passar de **cinco** (senão
**\* Periodo de entrega nao pode ultrapassar 5 dias \***). Na recusa da data final
inválida e nas de fim de semana ou feriado no fim o cursor fica no limite do
período; em todas as outras, no início do período; e nada é gravado.

### RN-11 — A entrega tem de caber na permissão de entrega do contrato

A tela percorre as permissões de entrega cadastradas para o tipo de contrato do
pedido e só deixa passar o período que **começa exatamente no início de uma dessas
permissões** e termina dentro dela (o fim não pode passar do fim da permissão).
Fora disso, a recusa é **\* Entrega fora dos limites da permissao \***, com o
cursor no início do período, e nada é gravado.

[?] Essa leitura sai de duas conferências que, juntas, obrigam o início da entrega
a ser igual ao início de uma permissão: o laço que procura a permissão para na
primeira cujo início **não é anterior** ao início informado, e a conferência
seguinte exige que o início informado **não seja posterior** ao início dessa
permissão. Se a intenção era só a de que o período coubesse **dentro** de uma
permissão, o laço teria de parar na permissão anterior — e um período que começa
no meio de uma permissão seria aceito. Não escolho um dos dois lados; pergunta ao
site.

[?] A permissão conferida é a do tipo de contrato do pedido, mas a tela vai
guardando o tipo de contrato de cada linha de gênero à medida que a lê: se um
pedido puder ter linhas de tipos de contrato diferentes, vale o da última linha
lida, e não necessariamente o de todas. Pergunta ao site.

### RN-12 — A alteração alcança todos os pedidos preparados no mesmo momento

A tela procura o preparo do pedido informado e monta, com ele, a lista dos pedidos
que compartilham aquele preparo — até **10** pedidos. A alteração é de todos eles:
cada pedido da lista é conferido (situação e quantidades recebidas, RN-08 e RN-09)
antes de a alteração ser oferecida. Quando algum pedido da lista já está fechado, a
alteração recua e fica **só no pedido informado** — e a lista de pedidos não é
mostrada na confirmação. A confirmação mostra o período do preparo do pedido
informado e, quando a alteração alcança o grupo, o número e o ano dos pedidos
alcançados.

### RN-13 — O novo período não pode encurtar um dia que já tem quantidade cadastrada

Se o novo período deixa de fora um dos cinco dias possíveis e aquele dia já tem
quantidade cadastrada para o pedido, a alteração é recusada com
**\* <- Nao diminua dias entrega. Ja existem qt.cad \***, com o cursor no limite do
período, e nada é gravado.

### RN-14 — A entrega não pode começar depois do preparo

A data de início do novo período não pode ser posterior à data do preparo do
pedido: senão **\* Data de entrega maior que data do preparo \***, com o cursor no
início do período, e nada é gravado.

[?] A conferência que vem logo depois limita a diferença entre o preparo e a
entrega a **7 dias** (**\* Difer.entre preparo e entrega maior que 7 dias \***),
mas ela não tem como disparar: a conferência anterior já recusou toda entrega que
comece depois do preparo. Ou a primeira conferência está invertida — e a intenção
era permitir a entrega depois do preparo, dentro dos 7 dias —, ou a segunda é
resto de geração e a mensagem nunca aparece. Não escolho um dos dois lados;
pergunta ao site.

### RN-15 — A alteração é pedida com confirmação

Passando por todas as conferências, a tela ainda não grava: ela mostra o código e a
razão social do fornecedor, o código e o nome do operador, o cartão, o indicador de
pedido acumulado, o período do preparo do pedido e a lista dos pedidos alcançados,
e pergunta **\* Confirma alteracao da entrega <S/N> ? \***, com o cursor na
resposta. Só a resposta afirmativa leva à gravação. A resposta negativa não sai da
tela: ela descarta a confirmação pendente, a tela refaz todas as conferências e
volta à mesma pergunta. Uma resposta afirmativa com qualquer período ou pedido
diferente do que foi oferecido também descarta a pendência e refaz as
conferências.

[?] Quando o fornecedor não está cadastrado, a tela não avisa: a razão social
aparece em branco na confirmação e a alteração segue assim mesmo; o mesmo vale
para o operador. Se existe outro cadastro que devesse ser consultado, o fonte não
o mostra. Pergunta ao site.

### RN-16 — Nada é gravado sem a conferência de sessão, de tela, de acesso e de operação

Na abertura, a tela confere que o servidor está na **estação em que a sessão foi
aberta** (em outra, o acesso é encerrado e a sessão volta à entrada), que a tela
está registrada e não está marcada como excluída (senão **\* Tela nao
cadastrada \***), e que o código de acesso do servidor alcança a tela (senão
**\* Acesso negado para esta matricula \***). Na alteração, confere também a
operação: é preciso que o código de acesso tenha a **permissão de alteração** para
esta tela, senão **\* Acesso negado para esta operacao \***, e que a transação não
peça a segunda página da tela, senão **\* Acesso a pagina 2 negado \***. Sem passar
por tudo, nada é gravado.

[?] A rota da transação é decidida por um campo da própria tela — o código da
próxima tela — que chega preenchido de fora dela e, quando preenchido, desvia a
transação antes de qualquer gravação: não se conclui desta tela quem o preenche,
nem se ele pode levar a transação para outra tela. Pergunta ao site.

### RN-17 — A recusa e a abertura não gravam nada

Cada recusa encerra a passagem **antes** das gravações e antes da auditoria, de
modo que uma alteração recusada não grava o período em nenhum pedido, nem nas
linhas de gênero, nem no preparo, nem na requisição, e não inclui registro de
auditoria. A simples abertura da tela também não escreve nem apaga nada.

---

## Cenários BDD

```gherkin
Funcionalidade: Alterar o período de entrega de um pedido de alimentação escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E029T

  Cenário: Remarcar a entrega de um pedido aprovado
    Dado que existe um pedido aprovado, não acumulado, sem quantidade recebida
    E que o pedido é da coordenadoria do meu vínculo
    E que o novo período começa em um dia útil, não é feriado e termina dentro da
      permissão de entrega do contrato
    Quando informo o órgão, a coordenadoria, o número do pedido, o ano da entrega e
      o novo período e confirmo a alteração
    Então as linhas de gênero do pedido passam a ter os novos dias de entrega
    E o pedido passa a ter o novo período
    E vejo "* Periodo alterado com sucesso *"

  Cenário: A alteração alcança os pedidos preparados no mesmo momento
    Dado que existem três pedidos aprovados preparados no mesmo momento, sem
      quantidade recebida
    Quando altero o período de um deles e confirmo
    Então os três pedidos passam a ter os novos dias de entrega
    E o preparo e a requisição do pedido também recebem o novo período

  Cenário: A alteração recua quando um pedido do preparo já está fechado
    Dado que um dos pedidos preparados no mesmo momento já está fechado
    Quando confirmo a alteração do período do pedido informado
    Então só o pedido informado passa a ter o novo período
    E os outros pedidos do preparo continuam com o período antigo

  Cenário: A tela só altera
    Dado que estou na tela E029T
    Quando a transação chega com uma operação que não é a de alteração
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: A abertura propõe o órgão e a coordenadoria da sessão
    Dado que o meu vínculo tem órgão filho e coordenadoria
    Quando abro a tela E029T
    Então o campo do órgão vem preenchido com o órgão do meu vínculo
    E o campo da coordenadoria vem preenchido com a coordenadoria do meu vínculo
    E o cursor fica no número do pedido
    E vejo a descrição do órgão, a descrição do tipo de órgão e a data do sistema
    E nada é gravado

  Cenário: A abertura sem órgão no vínculo
    Dado que o meu vínculo não tem órgão filho
    Quando abro a tela E029T
    Então o campo do órgão fica em branco, para eu informar
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O servidor não altera pedido de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo outro órgão e confirmo
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O servidor não altera pedido de outro grupo
    Dado que o meu vínculo carrega uma coordenadoria
    Quando informo um órgão cadastrado em outra coordenadoria e confirmo
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Sem coordenadoria no vínculo, um dos dois é obrigatório
    Dado que o meu vínculo não tem coordenadoria
    Quando confirmo sem informar o órgão e sem informar a coordenadoria
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão não cadastrado
    Dado que estou na tela E029T
    Quando informo um órgão que não está cadastrado e confirmo
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão de outra secretaria
    Dado que o órgão informado é de um tipo de órgão diferente do da minha sessão
    Quando confirmo
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O número do pedido é obrigatório
    Dado que estou na tela E029T
    Quando confirmo com o número do pedido e o ano da entrega zerados
    Então vejo "* Informe o numero do pedido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: O número do pedido é a junção do número com o ano da entrega
    Dado que estou na tela E029T
    Quando informo apenas o ano da entrega e confirmo
    Então a tela procura o pedido pelo número de 10 dígitos formado pelo número e
      pelo ano
    E não encontrando, vejo "* Pedido nao cadastrado *"

  Cenário: Pedido não cadastrado
    Dado que estou na tela E029T
    Quando informo um pedido que não existe para a coordenadoria e confirmo
    Então vejo "* Pedido nao cadastrado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido auxiliar do acumulado calculado
    Dado que o pedido é um auxiliar de pedido acumulado calculado
    Quando confirmo a alteração
    Então vejo "* Pedido auxiliar do acumulado calculado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido que ainda espera aprovação
    Dado que o pedido ainda não foi aprovado
    Quando confirmo a alteração
    Então vejo "* Pedido pendente de aprovacao *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido que já saiu para distribuição
    Dado que o pedido já foi para distribuição
    Quando confirmo a alteração
    Então vejo "* Pedido pendente de distribuicao *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido já fechado
    Dado que o pedido já está fechado
    Quando confirmo a alteração
    Então vejo "* Pedido aprovado - fechado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido excluído
    Dado que o pedido está excluído
    Quando confirmo a alteração
    Então vejo "* Pedido excluido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Linha de gênero de pedido acumulado
    Dado que uma das linhas de gênero do pedido é de pedido acumulado
    Quando confirmo a alteração
    Então vejo "* Pedido com genero de pedido acumulado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido com quantidade já recebida
    Dado que uma das linhas de gênero do pedido tem quantidade recebida
    Quando confirmo a alteração
    Então vejo "* Pedido ja tem quantidades recebidas *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Data de início inválida
    Dado que estou na tela E029T
    Quando informo o período sem a data de início e confirmo
    Então vejo "* Data de inicio da entrega invalida *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: O ano da entrega tem de ser o do pedido
    Dado que o pedido é do ano da entrega que eu informei
    Quando informo um período que começa em outro ano
    Então vejo "* Ano da entrega difere do ano do pedido *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: Informar o mesmo período que o pedido já tem
    Dado que o pedido está no período que eu informo, sem alteração
    Quando confirmo a alteração
    Então vejo "* Informe o novo periodo de entrega *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: O período é completado quando o limite fica em branco
    Dado que estou na tela E029T e deixo o limite do período em branco
    Quando confirmo a alteração
    Então a tela completa o limite com o quinto dia de entrega do novo período

  Cenário: A entrega não pode começar ou terminar em fim de semana
    Dado que estou na tela E029T
    Quando informo um início em sábado ou domingo
    Então vejo "* Inicio da entrega nao deve ser um sabado *" ou
      "* Inicio da entrega nao deve ser um domingo *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: A entrega não pode começar ou terminar em feriado
    Dado que estou na tela E029T
    Quando informo um início que é feriado no calendário
    Então vejo "* Inicio da entrega nao deve ser um feriado *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: A data final é inválida
    Dado que estou na tela E029T
    Quando informo um limite que não é data válida e confirmo
    Então vejo "* Data final da entrega invalida *"
    E o cursor fica no limite do período
    E nada é gravado

  Cenário: A data final menor que a inicial
    Dado que estou na tela E029T
    Quando informo um limite anterior ao início do período
    Então vejo "* Data final menor que a data inicial *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: Período com mais de cinco dias de entrega
    Dado que estou na tela E029T
    Quando informo um período que abrange mais de cinco dias de entrega
    Então vejo "* Periodo de entrega nao pode ultrapassar 5 dias *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: Entrega fora dos limites da permissão do contrato
    Dado que o pedido é de um tipo de contrato que tem permissões de entrega
      cadastradas
    Quando informo um período que não começa no início de nenhuma delas
    Então vejo "* Entrega fora dos limites da permissao *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: Não diminuir dias de entrega que já têm quantidade cadastrada
    Dado que um dos dias do período atual do pedido já tem quantidade cadastrada
    Quando informo um período que deixa aquele dia de fora
    Então vejo "* <- Nao diminua dias entrega. Ja existem qt.cad *"
    E o cursor fica no limite do período
    E nada é gravado

  Cenário: A entrega não pode começar depois do preparo
    Dado que o pedido tem uma data de preparo
    Quando informo um período que começa depois dela
    Então vejo "* Data de entrega maior que data do preparo *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: A alteração é pedida com confirmação
    Dado que o pedido passou por todas as conferências
    Quando confirmo a alteração
    Então vejo o fornecedor, o operador, o cartão, o período do preparo e os pedidos
      alcançados
    E vejo "* Confirma alteracao da entrega <S/N> ? *"
    E o cursor fica na resposta
    E nada foi gravado ainda

  Cenário: A resposta negativa não altera
    Dado que a tela me pediu a confirmação da alteração
    Quando respondo algo diferente de "S"
    Então a alteração não acontece
    E a tela confere o pedido de novo e volta a pedir a confirmação

  Cenário: A alteração é gravada no pedido, nas linhas de gênero, no preparo e na requisição
    Dado que confirmei a alteração
    Quando a gravação é executada
    Então cada linha de gênero dos pedidos alcançados recebe os novos dias de
      entrega, uma a uma
    E cada pedido alcançado recebe o novo período
    E o preparo e a requisição do pedido recebem o novo período
    E cada linha de gênero, cada pedido e a requisição deixam um registro de
      auditoria com a operação de alteração, o cadastro atingido, o número do
      pedido, a minha matrícula, a estação, a coordenadoria, a secretaria e a data
      e a hora da sessão
    E nenhum outro cadastro é incluído ou alterado

  Cenário: Nada é gravado sem a conferência de sessão, de tela, de acesso e de operação
    Dado que estou na tela E029T
    Quando a conferência da estação, do registro da tela, do código de acesso ou da
      permissão de alteração não passa
    Então vejo "* Tela nao cadastrada *", "* Acesso negado para esta matricula *",
      "* Acesso negado para esta operacao *" ou "* Acesso a pagina 2 negado *"
    E nada é gravado
    E, se a estação não for a da minha sessão, o acesso é encerrado

  Cenário: A recusa não grava nada
    Dado que estou na tela E029T e a minha alteração foi recusada
    Quando a tela termina a passagem
    Então nenhum pedido foi alterado
    E nenhuma linha de gênero recebeu novos dias de entrega
    E nenhum registro de auditoria foi incluído

  Cenário: A abertura da tela não grava nada
    Dado que o meu vínculo tem órgão filho e coordenadoria
    Quando abro a tela E029T
    Então nenhum pedido é alterado, nenhuma linha de gênero é gravada, o preparo e a
      requisição ficam como estavam e nenhuma auditoria é gravada
```
