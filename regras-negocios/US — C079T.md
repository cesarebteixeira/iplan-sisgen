# US — C079T — Atualizar o gênero dos cardápios de um período

## Estória

Como **servidor de CRE**, quero **informar o gênero que está em uso e o gênero que
deve substituí-lo, junto com o período e a impressora, e pedir a atualização**, para
que **os cardápios daquele período passem a contar com o gênero novo, sem que eu
tenha de corrigir cardápio por cardápio**.

A composição do cardápio escolar guarda, para cada período, os gêneros que entram
naquele cardápio. Quando um gênero é corrigido — o código muda, ou o gênero é
reclassificado —, os cardápios do período que ainda apontam para o gênero antigo
ficam desatualizados, e alguém teria de corrigi-los um a um. Esta tela existe para
trocar o gênero de um período inteiro de uma vez: ela recolhe o gênero em uso, o
gênero novo, o período e a impressora, confere o que foi informado contra os
cadastros e registra a solicitação; a troca nos cardápios é feita pelo processamento
do sistema, depois. Não é uma tela de cadastro.

## Contexto

Jornada S000M → C000M → C070M → C079T.

Ator: servidor de CRE — pede a atualização do gênero dos cardápios de um período do
seu órgão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio. Nem o C000M nem o C070M gravam nada
do que esta tela faz; o contexto que ela usa — matrícula, acesso, privilégio, tipo
de órgão e CRE — é o que a entrada deixou na sessão. O C070M apenas abre esta tela,
pelo nome dela, sem lhe passar registro nem operação; por isso a operação desta tela
não vem de quem a chamou.

Quem mantém o cadastro dos gêneros é a **C050T** e o dos cardápios é a **C070T**;
esta tela não é nenhuma das duas: ela lê os dois cadastros para conferir o que foi
informado.

---

## Regras de negócio

### RN-01 — A tela sempre abre na atualização

A tela abre no modo de atualização e exige esse modo, qualquer que seja a tela que a
abriu. Quem a chamou não escolhe a operação: o modo é reposto pela própria tela
antes de qualquer leitura. Se a operação que chegar não for a atualização, o sistema
recusa com **\* Opcao nao disponivel. Use ALT \***, devolve o cursor ao campo da
resposta e não lê nem registra nada.

[?] A mensagem manda usar "ALT", mas a operação que a tela aceita é o código interno
de alteração do sistema; nenhum valor "ALT" existe no acervo lido. Ou o formulário
traduz o que o servidor digita para esse código, ou quem seguir a mensagem é
recusado. Pergunta ao site.

[?] Como a tela repõe a atualização sozinha, a recusa só é alcançável por quem
chegue com outra operação já gravada no contexto — caminho que, no acervo desta
jornada, nenhuma tela usa. Se a recusa é trecho sem uso, o acervo não diz. Pergunta
ao site.

### RN-02 — O que a tela pede, e o que ela não pede

O servidor informa **onze campos**: o gênero que está em uso — a subclasse e o
gênero —, o gênero que deve substituí-lo — a subclasse e o gênero novos —, a **data
de início do período** — dia, mês e ano —, a **data limite do período** — dia, mês e
ano — e a **impressora**. A resposta da confirmação é um campo à parte, que não
entra na conferência dos onze. Nenhum campo de classe é pedido: a classe vem do
cadastro, na leitura do gênero.

### RN-03 — O gênero em uso e o gênero novo precisam estar cadastrados e ativos

O gênero em uso e o gênero novo têm de constar do cadastro de gêneros e estar
**ativos**; gênero inativo conta como não cadastrado. Não constando o gênero em uso,
a tela recusa com **\* Genero a ser atualizado nao cadastrado \*** e devolve o
cursor ao campo do gênero; não constando o novo, a recusa é
**\* Novo Genero nao cadastrado \***, com o cursor no campo da subclasse. A
conferência é a mesma dos dois lados: o par subclasse/gênero tem de ser o que voltou
do cadastro.

[?] A tela aceita informar o **mesmo gênero nos dois lados**: o par em uso e o par
novo são conferidos separadamente e nunca comparados entre si. Se a intenção era
recusar uma substituição sem efeito, o caminho não recusa. Pergunta ao site.

[?] O gênero inativo recebe a mesma mensagem de "não cadastrado". Se o servidor devia
ser avisado de que o gênero existe mas está inativo, o acervo não diz. Pergunta ao
site.

[?] Para achar cada par, a tela procura a vigência com o ano **9999** e o mês e o dia
**99** — valores-limite, não datas —, e depois confere se o par que voltou do
cadastro é o informado. O acervo não diz o que o cadastro faz com esses limites (se
devolve a vigência mais recente do par, se apenas se posiciona na primeira, ou se
não devolve nada). O desfecho lido vale nos dois casos, mas **qual** é o esperado é
pergunta ao site.

### RN-04 — O período precisa ter cardápio cadastrado

O período é identificado pelo **dia, o mês e o ano limite** informados, dentro do
tipo de órgão da sessão: a tela confere se há cardápio cadastrado para esse tipo de
órgão com essa data limite. Não havendo, recusa com
**\* Cardapios nao cadastrados neste periodo \*** e devolve o cursor ao campo do dia
limite. Só a data limite entra nessa conferência: o dia, o mês e o ano de início do
período não são conferidos contra nada — nem entre si, nem contra a data limite.

[?] A conferência procura o cardápio pela data limite, mas o código do cardápio que
a leitura usa vai zerado e o resultado não é conferido: se ela exige um cardápio com
aquela data limite exata, ou se apenas se posiciona no primeiro cardápio do período,
depende do recurso de posicionamento do dicionário de dados, cujo efeito exato não
está no acervo lido. O site precisa dizer qual é o esperado.

[?] Não há conferência de dia e mês válidos nem de ordem entre a data de início e a
data limite: qualquer combinação de números passa. Se a tela devia validar a data de
início, o caminho não valida. Pergunta ao site.

### RN-05 — A data de início do período que a tela mostra é a do cardápio cadastrado

A data de início do período que a tela exibe — e que manda ao processamento — não é
a que o servidor digitou: ela é reposta com a **data de início do cardápio
cadastrado** no período, lida do cadastro na conferência. O servidor pode digitar
uma data de início, mas ela é substituída antes de a confirmação aparecer.

[?] Se a data de início é sempre reposta pelo cadastro, por que a tela a pede ao
servidor? O acervo não responde; se o esperado é usar o que foi digitado, o caminho
não usa. Pergunta ao site.

### RN-06 — A impressora é obrigatória

Sem impressora informada, a tela recusa com **\* Informe a impressora \*** e devolve
o cursor ao campo da impressora. A conferência existe duas vezes — antes da
confirmação e depois dela —, de modo que a impressora continua obrigatória no passo
que registra a solicitação. A impressora informada vai para a solicitação de
processamento.

### RN-07 — Não se pede o processamento de novo enquanto o anterior não termina

Depois da confirmação, antes de registrar a solicitação, a tela confere se já existe
**solicitação de processamento pendente** para o mesmo relatório e o mesmo tipo de
órgão. Existindo, recusa com **\* Relatorio em processamento. Aguarde. \***, sem
registrar nada e sem entregar o pedido.

[?] Essa conferência procura a solicitação pendente com a **coordenação regional
zerada**, e a solicitação que a tela registra também é gravada com ela zerada. Se
outra tela registra a mesma solicitação com a coordenação preenchida, o pedido
anterior pode não ser visto e o processamento ser pedido duas vezes. Pergunta ao
site.

### RN-08 — A troca só acontece depois da confirmação

Depois de todas as conferências, a tela mostra
**\* Confirma atualizacao do genero <S/N> ? \*** e espera a resposta. Só a resposta
**S** registra a solicitação e entrega o processamento; nesse momento a mensagem
passa a **\* Cadastros sendo atualizado \***. A confirmação volta a ser pedida
sempre que o servidor mudar o gênero em uso, o gênero novo ou a data limite depois
de ela já ter sido mostrada; mudar a data de início não faz a confirmação voltar.

[?] Responder **N** não cancela: a tela limpa a resposta, repõe o que já estava em
tela e **volta a pedir a mesma confirmação**. Não há, no caminho lido, um desfecho
que encerre a operação com a resposta negativa. Se o esperado é que N cancele, o
caminho não cancela. Pergunta ao site.

[?] Depois de entregue, o processamento não dá retorno a esta tela. O que ele faz com
os cardápios do período — se troca o gênero em todos, se ignora os cardápios em que o
gênero em uso não aparece, e por que ele revalida o mesmo período e o mesmo cadastro
antes de gravar — não está nos fontes desta jornada. Pergunta ao site.

### RN-09 — A tela não altera cadastro nenhum: registra a solicitação e a auditoria

Esta tela não inclui, não altera e não exclui registro no cadastro dos gêneros nem no
cadastro dos cardápios: o que ela grava é a **solicitação de processamento**, com o
número seguinte da fila de pedidos, e o **registro de auditoria** da operação. As
rotinas de gravação, de exclusão e de travamento existem declaradas para os seis
cadastros que a tela enxerga, mas **só duas gravações são executadas** — a da
solicitação e a da auditoria —, e nenhuma exclusão. Declarar não é executar.

[?] A tela lê o **e-mail do funcionário** no cadastro de funcionários e não o usa
para nada: não o leva para a solicitação nem para os parâmetros entregues ao
processamento. Se o e-mail devia acompanhar o pedido, o caminho o descarta.
Pergunta ao site.

### RN-10 — O que o processamento recebe, e o que volta para a tela

Confirmada a solicitação, a tela entrega ao processamento o **relatório C79001** com
o **tipo de órgão da sessão**, o **gênero em uso**, o **gênero novo**, as **duas
datas do período** e a **impressora**; a solicitação registrada guarda o mesmo
relatório, o número do pedido, a estação, a matrícula e a impressora. Em seguida a
tela limpa a resposta, repõe em tela o que ficou registrado e **volta a se apresentar
para um novo pedido**, sem sair da tela.

### RN-11 — Ao abrir, a tela apaga a apresentação anterior e mostra o contexto da sessão

Antes de conferir a digitação e de ler qualquer cadastro, a tela apaga os **doze
campos de resultado** da apresentação anterior — o cabeçalho, as descrições e a
mensagem —, de modo que uma conferência recusada não deixa em tela o resultado da
anterior. Fora dos campos informados, a tela exibe a **data do sistema** e a
**descrição do tipo de órgão** da sessão, e as descrições da classe e dos gêneros
lidas do cadastro.

[?] Nem a data do sistema nem a descrição do tipo de órgão são preenchidas por
nenhum caminho desta tela: ela copia as duas de áreas de trabalho, e a entrada as
guarda em outras áreas. Se o ambiente transporta os valores de uma área para a
outra — e de onde vem a data do sistema —, é pergunta ao site; se não transportar,
os dois campos saem em branco.

---

## Cenários BDD

```gherkin
Funcionalidade: Atualizar o gênero dos cardápios de um período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C079T

  Cenário: Pedido de atualização do gênero do período
    Dado que o gênero em uso e o gênero novo estão cadastrados e ativos
    E o período informado tem cardápio cadastrado
    E informei a impressora
    Quando confirmo a atualização
    Então vejo a mensagem "* Cadastros sendo atualizado *"
    E a solicitação de processamento é registrada com o número seguinte da fila
    E o registro de auditoria da operação é gravado

  Cenário: O processamento recebe a troca, o período e a impressora
    Dado que confirmo a atualização
    Então o processamento recebe o relatório C79001 com o meu tipo de órgão, o gênero em uso, o gênero novo, as duas datas do período e a impressora

  Cenário: A tela não altera os cadastros de gênero nem de cardápio
    Dado que confirmo a atualização
    Então nenhum gênero é incluído, alterado ou excluído
    E nenhum cardápio é incluído, alterado ou excluído
    E o que fica registrado é a solicitação de processamento e a auditoria da operação

  Cenário: Gênero em uso não cadastrado
    Dado que informei um gênero em uso que não consta do cadastro de gêneros
    Quando confirmo a atualização
    Então vejo a mensagem "* Genero a ser atualizado nao cadastrado *"
    E o cursor volta ao campo do gênero
    E nada é registrado

  Cenário: Gênero em uso inativo
    Dado que informei um gênero em uso que existe no cadastro mas está inativo
    Quando confirmo a atualização
    Então vejo a mensagem "* Genero a ser atualizado nao cadastrado *"
    E nada é registrado

  Cenário: Novo gênero não cadastrado
    Dado que informei um gênero novo que não consta do cadastro de gêneros
    Quando confirmo a atualização
    Então vejo a mensagem "* Novo Genero nao cadastrado *"
    E o cursor volta ao campo da subclasse
    E nada é registrado

  Cenário: O mesmo gênero nos dois lados é aceito
    Dado que informei o mesmo gênero em uso e gênero novo
    Quando confirmo a atualização
    Então a tela aceita o pedido
    E o processamento é entregue

  Cenário: Período sem cardápio cadastrado
    Dado que não há cardápio cadastrado para o meu tipo de órgão na data limite que informei
    Quando confirmo a atualização
    Então vejo a mensagem "* Cardapios nao cadastrados neste periodo *"
    E o cursor volta ao campo do dia limite
    E nada é registrado

  Cenário: A data de início do período vem do cardápio cadastrado
    Dado que digitei uma data de início de período diferente da do cardápio cadastrado
    Quando envio a tela
    Então a data de início em tela passa a ser a do cardápio cadastrado
    E é essa data que vai para o processamento

  Cenário: Impressora não informada
    Dado que deixei o campo da impressora em branco
    Quando confirmo a atualização
    Então vejo a mensagem "* Informe a impressora *"
    E o cursor volta ao campo da impressora
    E nada é registrado

  Cenário: Já existe processamento pendente para o mesmo relatório
    Dado que existe uma solicitação de processamento pendente para o meu tipo de órgão e este relatório
    Quando confirmo a atualização
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E uma segunda solicitação não é registrada

  Cenário: A confirmação vem antes de qualquer registro
    Dado que todas as conferências passaram
    Quando envio o pedido
    Então vejo a mensagem "* Confirma atualizacao do genero <S/N> ? *"
    E nenhuma solicitação foi registrada ainda

  Cenário: A resposta negativa não cancela e não registra nada
    Dado que a tela pediu a confirmação
    Quando respondo N
    Então a tela volta a pedir a confirmação
    E nenhuma solicitação é registrada

  Cenário: Mudar o gênero depois de a confirmação aparecer faz a confirmação voltar
    Dado que a tela pediu a confirmação
    Quando altero o gênero em uso, o gênero novo ou a data limite e envio de novo
    Então a tela volta a pedir a confirmação
    E a data de início do período aparece com a do cardápio cadastrado

  Cenário: Confirmada a atualização, a tela volta a se apresentar para um novo pedido
    Dado que confirmei a atualização
    Então vejo a mensagem "* Cadastros sendo atualizado *"
    E a tela reabre no modo de atualização, com os campos do último pedido

  Cenário: Operação diferente da atualização
    Dado que a operação informada não é a atualização
    Quando envio a tela
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo da resposta
    E nenhum gênero e nenhum cardápio são lidos

  Cenário: Digitação não numérica nos campos informados
    Dado que digitei algo que não é número em um dos campos informados
    Quando envio a tela
    Então o sistema recusa a digitação antes de ler qualquer cadastro
    E o cursor volta ao campo recusado, quando o campo tem posição de cursor
    E nada é registrado

  Cenário: O resultado da apresentação anterior é apagado
    Dado que a apresentação anterior mostrou as descrições e a mensagem
    Quando envio uma conferência que é recusada
    Então as descrições e a mensagem anteriores não ficam em tela

  Cenário: O contexto da sessão na tela
    Dado que entrei no sistema
    Quando abro a tela C079T
    Então vejo a descrição do tipo de órgão da minha sessão
    E vejo a classe e as descrições do gênero lidas do cadastro
```
