# US — C774T — Pedir a cópia dos planejamentos de cardápios de uma origem para outra

## Estória

Como **servidor de CRE**, quero **pedir que o planejamento de cardápios já montado para
um grupo, numa semana, para um segmento de atendimento e dentro de um período seja
repetido em outro grupo, outra semana, outro segmento ou outro período**, para que **a
combinação nova já conte com a mesma composição, sem que eu tenha de remontá-la refeição
por refeição e dia por dia**.

O planejamento de cardápios é montado refeição por refeição e dia por dia, e a mesma
composição costuma valer para vários grupos, semanas e segmentos do mesmo período. Sem
esta tela, cada repetição seria remontada à mão, e a merenda do período novo ficaria
dependente de o servidor lembrar, dia a dia, o que o período antigo servia. Ela não é
tela de cadastro: quem copia é o processamento do sistema, e a tela só recolhe de onde se
copia e para onde, pede a confirmação e registra o pedido.

## Contexto

Jornada S000M → C000M → C070M → C770M → C774T.

Ator: servidor de CRE — pede a cópia do planejamento de cardápios de uma origem para um
destino, informando, em cada ponta, o grupo, a semana, o segmento de atendimento e o
período, além da impressora.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A tela é aberta por um menu, e não encadeada por outra tela que lhe passe o registro e a
operação: o `C000M`, o `C070M` e o `C770M` são menus, não gravam nada e não escolhem nada
por esta tela. Não há nesta jornada comparação da tela que chamou com um código de tela:
a tela abre em alteração por decisão própria, e é o único modo que ela aceita. O contexto
de que ela se serve — a matrícula, o código de acesso, o privilégio, o tipo de órgão e a
coordenação regional da sessão — é o que a entrada deixou na sessão; a tela não o
recalcula nem deixa escolher.

A jornada termina nesta tela: ela não encaminha para nenhuma outra. A única saída é ela
mesma, reexibida para pedir a confirmação e, depois, para dar o aviso final.

## Regras de negócio

### RN-01 — A tela pede a cópia dos planejamentos de uma origem para outra

O servidor informa uma **origem** e um **destino**, e cada ponta é uma combinação
completa: o **grupo** (a coordenação regional escolar), a **semana**, o **segmento de
atendimento** e o **período**, este pelas suas datas de início e limite — dia, mês e ano
em cada uma. Informa também a **impressora**. Passadas as conferências, a tela pergunta se
confirma a cópia e, confirmada, entrega o pedido ao processamento do sistema, que é quem
copia. A tela não espera pelo resultado e não mostra o que foi copiado: o desfecho
acontece no processamento e não volta para ela.

A apresentação tem **vinte e sete campos**: os **sete** do cabeçalho e do controle — entre
eles o da operação —, os **dezoito** das duas pontas (nove por ponta), a impressora e a
resposta da confirmação.

[?] O acervo desta jornada mostra o que a tela entrega ao processamento e onde o pedido é
registrado, mas não o processamento em si: se ele copia mesmo o planejamento da origem
para o destino, o que faz quando a origem não tem composição para a semana ou o segmento
pedidos, e o que ele faz com o que já existir no destino, são perguntas ao site.

### RN-02 — A tela não copia cadastro nenhum: registra o pedido e a auditoria

Esta tela não inclui, não altera e não exclui planejamento, cardápio, grupo, segmento nem
tipo de órgão: o que ela grava é a **solicitação de processamento**, com o número seguinte
da fila, e o **lançamento de auditoria** da operação. Ela enxerga **oito** cadastros e
registros — entre eles o cadastro de telas, os cadastros de grupos e de segmentos de
atendimento, o cadastro de cardápios do período, o cadastro do planejamento, o cadastro de
funcionários e a fila de requisições —, mas as rotinas de gravação, de exclusão e de
travamento existem declaradas para todos e **só duas gravações são executadas**: a da
solicitação e a da auditoria. Não há exclusão nem travamento nenhum. Declarar não é
executar: os demais são só lidos.

### RN-03 — A tela só executa em alteração

A tela abre sempre em **alteração**, fixada por ela mesma ao ser exibida; não há outro
modo, e não há passagem de consulta. Se a operação que chega for diferente da alteração, a
tela recusa com **\* Operacao nao disponivel. Use ALT \***, devolve o cursor ao campo da
operação e para antes de ler qualquer cadastro: nesse caminho nada é lido e nada é
gravado.

[?] A mensagem manda usar "ALT", mas a única operação que a tela aceita é o código de
alteração do próprio sistema, e nenhum valor "ALT" aparece no acervo lido: ou o formulário
traduz o que o servidor digita para esse código, ou quem seguir a mensagem é recusado.
Pergunta ao site.

### RN-04 — O grupo das duas pontas é obrigatório, tem de existir, e "todos os grupos" só vale na origem

O grupo da origem e o do destino são obrigatórios: em branco, a recusa é
**\* Informe o grupo - DE \*** ou **\* Informe o grupo - PARA \***, com o cursor no
campo. Informado, o grupo é procurado no cadastro de grupos daquele tipo de órgão; não
constando, a recusa é **\* Grupo nao cadastrado - DE \*** ou
**\* Grupo nao cadastrado - PARA \***. O código do grupo pode vir como **"todos os
grupos"**: nesse caso a existência não é conferida e o grupo do **destino passa a ser o
mesmo** da origem. Fora disso, "todos os grupos" no destino é recusado com
**\* Nao use 99 para esta opcao - PARA \***, com o cursor no grupo do destino.

[?] Quando a origem vem como "todos os grupos", o destino é fixado no mesmo "todos os
grupos" — isto é, a tela aceita copiar de todos para todos, combinação em que origem e
destino não se distinguem. O mesmo vale para "todas as semanas" na semana e para "todos os
segmentos" no segmento. Ou o código tem outro sentido, ou o processamento trata esses
casos de modo próprio; o acervo desta jornada não mostra. Pergunta ao site.

### RN-05 — A semana das duas pontas tem de ser A, B, C ou D, e "todas as semanas" só vale na origem

A semana informada tem de ser **A**, **B**, **C** ou **D**; qualquer outra coisa é
recusada com **\* Informe a semana A / B / C / D - DE \*** ou
**\* Informe a semana A / B / C / D - PARA \***, com o cursor na semana da respectiva
ponta. A origem aceita ainda a marca **"todas as semanas"**, e nesse caso a semana do
destino é fixada na mesma marca. Fora disso, "todas as semanas" no destino é recusado com
**\* Nao use T para esta opcao - PARA \***, com o cursor na semana do destino.

[?] O que a marca "todas as semanas" significa em negócio — todas as semanas do período,
ou uma semana de tipo especial — não está nos fontes nem nas mensagens: a recusa da origem
nomeia apenas A, B, C e D, e ainda assim a marca é aceita lá. Pergunta ao site.

### RN-06 — O segmento das duas pontas é obrigatório, tem de existir, e "todos os segmentos" só vale na origem

O segmento de atendimento da origem e o do destino são obrigatórios: em branco, a recusa é
**\* Informe o segmento - DE \*** ou **\* Informe o segmento - PARA \***, com o cursor
no campo. Informado, o segmento é procurado no cadastro de segmentos daquele tipo de
órgão; não constando, a recusa é **\* Segmento nao cadastrado - DE \*** ou
**\* Segmento nao cadastrado - PARA \***. O segmento pode vir como **"todos os
segmentos"**: nesse caso a existência não é conferida e o segmento do **destino passa a
ser o mesmo** da origem. Fora disso, "todos os segmentos" no destino é recusado com
**\* Nao use 99 para esta opcao - PARA \***, com o cursor no segmento do destino.

### RN-07 — O cardápio da data-limite define o período, e a data de início exibida vem dele

O período de cada ponta não é escolhido por um código: ele é identificado pela
**data-limite** informada, dentro do tipo de órgão da sessão. A tela procura um cardápio
cadastrado com aquela data-limite; não havendo, a recusa é
**\* Cardapios nao cadastrados para esta data - DE \*** ou
**\* Cardapios nao cad. para esta data - PARA \***, com o cursor no dia da data-limite da
respectiva ponta. A **data de início** que a tela exibe — e que entrega ao processamento —
não é a que o servidor digitou: ela é reposta com a data de início do cardápio encontrado,
em cada ponta.

[?] A data de início é pedida em tela e passa pela edição numérica, mas é descartada assim
que o cardápio é encontrado; os seis campos das duas datas de início, além disso, não têm
posição de cursor. Se ela deveria identificar o cardápio da ponta — ou conferir o que foi
lido —, o caminho não a usa. Pergunta ao site.

[?] As datas-limite também não são conferidas como data, nem contra a data de início da
mesma ponta: do período a tela só confere que existe cardápio naquela data-limite. Se as
datas deveriam ser validadas como data, o caminho não as valida. Pergunta ao site.

### RN-08 — A origem tem de ter planejamento cadastrado

A tela procura um planejamento cadastrado para a origem — pelo tipo de órgão da sessão,
pela data-limite da origem e, quando o grupo da origem não é "todos os grupos", pelo grupo
da origem. Não achando nenhum, a recusa é **\* Planejamentos nao cadastrados - DE \***,
com o cursor no dia da data-limite da origem, e nada é pedido. O destino não é conferido
quanto a já ter planejamento: quem decide o que fazer com o que existe lá é o
processamento.

[?] A procura do planejamento da origem leva a semana, o segmento e a refeição em branco,
de modo que **qualquer** planejamento daquele grupo no período satisfaz a conferência —
mesmo que não haja nada para a semana ou o segmento informados. Se a conferência deveria
ser da combinação informada, o caminho não a faz. Pergunta ao site.

### RN-09 — A impressora é obrigatória

A impressora em branco recusa com **\* Informe a impressora \***, com o cursor no campo,
e nada é pedido. É o último dado conferido antes de a tela pedir a confirmação.

### RN-10 — A cópia só é pedida depois de confirmada, e mudar um dado refaz a conferência

Passadas todas as conferências, a tela mostra
**\* Confirma copia dos planejamentos <S/N> ? \*** e espera a resposta; só a resposta
**S** registra o pedido. Junto com a resposta, **doze** dados têm de continuar iguais ao
que a tela guardou: os dois grupos, as duas semanas, os dois segmentos e as quatro partes
das duas datas-limite (o dia, o mês e o ano de cada uma). Mudando qualquer um deles, as
conferências recomeçam e a confirmação volta a ser pedida, sem nada gravado.

[?] Responder **N** não cancela: a tela limpa a resposta, repõe o que já estava em tela e
**volta a pedir a mesma confirmação**. Não há, no caminho lido, um desfecho que encerre a
operação com a resposta negativa. Se o esperado é que N cancele, o caminho não cancela.
Pergunta ao site.

[?] A impressora não entra na conferência da confirmação nem é guardada com a combinação:
se o servidor trocá-la entre o aviso e a resposta, o pedido sai com a impressora nova. Se
era para congelar a impressora informada, o caminho não a guarda. Pergunta ao site.

### RN-11 — Um pedido do mesmo processamento ainda em aberto impede outro

Antes de registrar, a tela confere se já existe **solicitação de processamento em aberto**
para esta mesma cópia; existindo, recusa com
**\* Relatorio em processamento. Aguarde. \***, com o cursor na resposta da confirmação, e
não registra nada. É essa conferência que impede pedir duas vezes a mesma cópia enquanto a
primeira não foi atendida.

[?] Quem atende a solicitação — e a marca como atendida ou a remove — não está nos fontes
desta jornada: se ninguém a atender, o pedido de cópia só pode ser feito uma vez. A
conferência procura a solicitação com a marca de atendimento em branco e o número do
pedido zerado, mas a solicitação que esta tela grava tem número positivo; e, do registro
que encontra, só confere de volta o código do processamento. Se o número zerado encontra
alguma coisa, e se uma solicitação já atendida também bloqueia, o acervo não permite
concluir. Pergunta ao site.

### RN-12 — O pedido recebe o número seguinte da fila e leva as duas combinações

Confirmada a cópia, o pedido é registrado na fila de requisições com o **número seguinte**
ao último já usado, o código do processamento de cópia, o tipo de órgão da sessão, a
matrícula, a estação e o dia, o mês e o ano da sessão, e **sem marca de atendimento**. É
esse número que identifica o pedido na fila. Ao processamento vão, além disso, as **duas
combinações completas** — grupo, semana, segmento e as duas datas de cada ponta —, a
impressora, **uma via**, a estação, a matrícula e o **e-mail** lido do cadastro do
funcionário.

[?] O e-mail do servidor segue no pedido entregue ao processamento e **não** é gravado na
solicitação da fila: para onde ele vai e o que o processamento faz com ele não está nos
fontes desta jornada. Pergunta ao site.

[?] O disparo do processamento depende de uma marca do ambiente em que a tela roda; o
acervo não mostra o que acontece quando essa marca não está posta — se o pedido fica na
fila apenas registrado, sem ser processado. Pergunta ao site.

### RN-13 — Todo pedido deixa rastro na auditoria

Cada pedido registra **um** lançamento na auditoria, com a tela de origem, a operação de
inclusão, a matrícula, a estação e a data e a hora da sessão, e com o **tipo de órgão e o
grupo da sessão** — não os informados em tela —; o conteúdo registrado é o das duas
combinações pedidas, e o valor posterior fica em branco. O lançamento guarda **o que foi
pedido**, não o que foi copiado.

[?] O lançamento identifica o pedido pelo **dia da data de início do destino** no campo do
número do processo, e nunca recebe um número de processo de verdade: o acervo não diz se
isso é intencional nem o efeito disso na chave da auditoria. Pergunta ao site.

### RN-14 — A digitação dos campos numéricos é editada

Os **dezesseis** campos numéricos da tela — os dois grupos, os dois segmentos e as três
partes de cada uma das quatro datas (duas de início e duas de limite) — passam por edição
numérica antes de qualquer leitura: campo em branco vale zero, os zeros à esquerda são
descartados e o que não for número é recusado. O cursor volta ao campo recusado para
**dez** deles — os dois grupos, os dois segmentos e as seis partes das duas datas-limite;
os **seis** campos das duas datas de início não têm posição de cursor.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não está
nos fontes desta jornada: a rotina que faz a edição numérica é uma rotina comum, a mesma
que a entrada usa nos seus próprios campos. Pergunta ao site.

### RN-15 — A abertura da tela é conferida, e a transação passa pelas conferências do sistema

Ao abrir, a tela lê o cadastro de telas e chama a conferência de acesso da tela; sem essa
conferência ela não segue. Antes das conferências dos dados, a transação ainda passa pela
conferência de rota, que recebe a tela pedida, a matrícula, o código de acesso, o
privilégio, o tipo de órgão e a coordenação regional da sessão, e pela conferência de
permissão da operação, que recebe a operação de alteração. Não estando a operação liberada
para aquele código de acesso, a tela é abandonada sem gravar.

## Cenários BDD

```gherkin
Funcionalidade: Pedir a cópia dos planejamentos de cardápios de uma origem para outra

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C774T

  Cenário: O pedido de cópia dos planejamentos de uma origem para outra
    Dado que informei a origem e o destino, cada um com grupo, semana, segmento e período
    E informei a impressora
    E a origem tem planejamento cadastrado no período
    Quando respondo S à confirmação
    Então vejo a mensagem "* Cadastro sendo atualizado *"
    E a solicitação de processamento é registrada
    E a operação fica registrada na auditoria

  Cenário: A tela não copia cadastro nenhum
    Dado que confirmo a cópia
    Então nenhum planejamento, cardápio, grupo, segmento ou tipo de órgão é incluído, alterado ou excluído por esta tela
    E o que fica registrado é a solicitação de processamento e a auditoria

  Cenário: A operação que chega não é a alteração
    Dado que a tela abre em alteração
    Quando a operação que chega é outra
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT *"
    E o cursor volta para o campo da operação
    E nada é lido nem gravado

  Cenário: Grupo da origem não informado
    Quando envio a tela sem o grupo da origem
    Então vejo a mensagem "* Informe o grupo - DE *"
    E o cursor volta para o grupo da origem
    E nada é pedido

  Cenário: Grupo da origem não cadastrado
    Dado que informei um grupo de origem que não consta do cadastro daquele tipo de órgão
    Quando envio a tela
    Então vejo a mensagem "* Grupo nao cadastrado - DE *"
    E o cursor volta para o grupo da origem
    E nada é pedido

  Cenário: Grupo do destino não informado
    Dado que a origem passou nas conferências
    Quando envio a tela sem o grupo do destino
    Então vejo a mensagem "* Informe o grupo - PARA *"
    E o cursor volta para o grupo do destino
    E nada é pedido

  Cenário: Grupo do destino não cadastrado
    Dado que informei um grupo de destino que não consta do cadastro daquele tipo de órgão
    Quando envio a tela
    Então vejo a mensagem "* Grupo nao cadastrado - PARA *"
    E o cursor volta para o grupo do destino
    E nada é pedido

  Cenário: "Todos os grupos" na origem fixa o destino
    Dado que informei "todos os grupos" na origem
    Quando envio a tela
    Então o grupo do destino passa a ser "todos os grupos"
    E nenhum grupo é procurado no cadastro

  Cenário: "Todos os grupos" no destino é recusado
    Dado que informei um grupo de origem específico e "todos os grupos" no destino
    Quando envio a tela
    Então vejo a mensagem "* Nao use 99 para esta opcao - PARA *"
    E o cursor volta para o grupo do destino
    E nada é pedido

  Cenário: Semana fora de A, B, C e D
    Quando informo, numa das pontas, uma semana diferente de A, B, C e D
    Então vejo a mensagem "* Informe a semana A / B / C / D - DE *" ou "* Informe a semana A / B / C / D - PARA *"
    E o cursor volta para a semana daquela ponta
    E nada é pedido

  Cenário: "Todas as semanas" apenas no destino
    Dado que a semana da origem não é "todas as semanas"
    Quando informo "todas as semanas" na semana do destino
    Então vejo a mensagem "* Nao use T para esta opcao - PARA *"
    E o cursor volta para a semana do destino
    E nada é pedido

  Cenário: Segmento de origem não informado ou não cadastrado
    Quando envio a tela sem o segmento de origem, ou com um segmento que não consta do cadastro
    Então vejo a mensagem "* Informe o segmento - DE *" ou "* Segmento nao cadastrado - DE *"
    E o cursor volta para o segmento de origem
    E nada é pedido

  Cenário: Segmento de destino não informado ou não cadastrado
    Dado que a origem passou nas conferências
    Quando envio a tela sem o segmento de destino, ou com um segmento que não consta do cadastro
    Então vejo a mensagem "* Informe o segmento - PARA *" ou "* Segmento nao cadastrado - PARA *"
    E o cursor volta para o segmento do destino
    E nada é pedido

  Cenário: "Todos os segmentos" no destino é recusado
    Dado que informei um segmento específico na origem e "todos os segmentos" no destino
    Quando envio a tela
    Então vejo a mensagem "* Nao use 99 para esta opcao - PARA *"
    E o cursor volta para o segmento do destino
    E nada é pedido

  Cenário: Sem cardápio cadastrado na data-limite
    Dado que não existe cardápio cadastrado na data-limite de uma das pontas
    Quando envio a tela
    Então vejo a mensagem "* Cardapios nao cadastrados para esta data - DE *" ou "* Cardapios nao cad. para esta data - PARA *"
    E o cursor volta para o dia da data-limite daquela ponta
    E nada é pedido

  Cenário: A data de início exibida é a do cardápio cadastrado
    Dado que digitei uma data de início diferente da do cardápio cadastrado na data-limite
    Quando a tela encontra o cardápio daquela data-limite
    Então a data de início daquela ponta passa a ser a do cardápio cadastrado

  Cenário: Origem sem planejamento cadastrado
    Dado que não existe planejamento cadastrado para a origem no período informado
    Quando envio a tela
    Então vejo a mensagem "* Planejamentos nao cadastrados - DE *"
    E o cursor volta para o dia da data-limite da origem
    E nada é pedido

  Cenário: Impressora não informada
    Dado que todo o resto passou nas conferências
    Quando envio a tela sem a impressora
    Então vejo a mensagem "* Informe a impressora *"
    E o cursor volta para a impressora
    E nada é pedido

  Cenário: A confirmação vem antes de qualquer registro
    Dado que todas as conferências passaram
    Quando a tela pede a confirmação
    Então vejo a mensagem "* Confirma copia dos planejamentos <S/N> ? *"
    E nada foi registrado ainda
    E só a resposta S registra o pedido

  Cenário: Mudar um dado depois do aviso de confirmação
    Dado que a tela já pediu a confirmação
    Quando troco o grupo, a semana, o segmento ou a data-limite de uma das pontas e respondo
    Então as conferências recomeçam
    E a confirmação volta a ser pedida
    E nada é registrado

  Cenário: Resposta diferente de S
    Dado que a tela já pediu a confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então nada é registrado
    E a tela repõe o que já estava em tela e volta a pedir a mesma confirmação

  Cenário: Já existe um pedido em processamento
    Dado que há uma solicitação em aberto para esta mesma cópia
    Quando respondo S à confirmação
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta para a resposta
    E nada é registrado

  Cenário: O pedido recebe o número seguinte da fila
    Dado que confirmo a cópia
    Então o pedido é registrado com o número seguinte ao último usado
    E fica sem marca de atendimento

  Cenário: O processamento recebe as duas combinações
    Dado que confirmo a cópia
    Então o processamento recebe o grupo, a semana, o segmento e as duas datas de cada ponta
    E recebe a impressora, a estação, a matrícula e o meu e-mail lido do cadastro do funcionário

  Cenário: A auditoria do pedido
    Dado que confirmo a cópia
    Então fica registrado um lançamento de auditoria com a tela de origem e a operação de inclusão
    E o conteúdo registrado é o das duas combinações pedidas
    E o valor posterior fica em branco

  Cenário: Digitação não numérica
    Dado que informei, num campo numérico da tela, algo que não é número
    Quando a tela edita os campos
    Então a entrada é recusada
    E o cursor volta ao campo recusado quando ele tem posição de cursor

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu código de acesso não tem liberada a alteração para esta tela
    Quando envio a tela
    Então a operação é recusada com mensagem
    E a tela é abandonada sem gravar
```
