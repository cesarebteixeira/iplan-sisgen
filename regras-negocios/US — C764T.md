# US — C764T — Pedir a cópia do planejamento sazonal de uma origem para um destino

## Estória

Como **servidor de CRE**, quero **pedir que o planejamento sazonal já cadastrado numa origem seja
repetido num destino, informando em cada ponta o grupo, o segmento de atendimento, a refeição e o
período, e indicando também a impressora**, para que **o período novo já conte com o mesmo
planejamento — ou outra combinação de grupo, segmento e refeição passe a seguir a de outro — sem
eu ter de remontar o planejamento combinação por combinação, mês a mês**.

O planejamento sazonal diz o que cada combinação de tipo de órgão, grupo, segmento de atendimento
e refeição prevê em cada mês do período, e é ele que sustenta a oferta de refeições ao longo do
ano. Quando o período novo repete o anterior, ou quando uma combinação deve passar a seguir a de
outro grupo ou de outro segmento, esse planejamento poderia ser aproveitado; sem esta tela, cada
combinação teria de ser remontada do zero, mês a mês. Esta tela recolhe de onde se copia, para
onde se copia e em que impressora, pede a confirmação e entrega o pedido ao processamento do
sistema, que é quem copia. Ela não é tela de cadastro, não copia nada por si mesma, e o resultado
não volta para ela.

## Contexto

Jornada S000M → C000M → C070M → C760M → C764T.

Ator: servidor de CRE — pede a cópia do planejamento sazonal de uma origem para um destino,
informando, em cada ponta, o grupo, o segmento de atendimento, a refeição e o período, e
indicando a impressora.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio. O `C000M`, o `C070M` e o `C760M` são menus e não gravam nada; o contexto que
esta tela usa — a matrícula, o tipo de órgão, o código de acesso, a CRE e o órgão — é o que a
entrada deixou na sessão. A chegada, aqui, é por **encadeamento**: o `C760M` não abre a tela por
navegação comum, ele passa a chamada adiante, e a tela de destino se abre já com o seu próprio
modo reposto e sem receber da tela anterior nenhum valor das duas pontas.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — Esta tela pede a cópia; quem copia é o processamento do sistema

O servidor informa a **origem** e o **destino** — em cada ponta o grupo, o segmento de
atendimento, a refeição e o período — e também a impressora, e a tela confere as duas pontas antes
de registrar coisa alguma. Passando todas as conferências, ela pergunta
**\* Confirma copia planejamentos sazonais <S/N> ? \*** e, só com a resposta **S**, registra a
**solicitação de processamento** e o **lançamento de auditoria** e avisa
**\* Cadastro sendo atualizado \***. A tela **não copia** planejamento nenhum e não espera pelo
resultado: quem apaga e regrava o planejamento sazonal é o processamento do sistema, e o que ele
copiou não volta para cá.

[?] A tela entrega o pedido e não acompanha o desfecho: nada volta do processamento e a tela não
relê a solicitação depois de gravá-la. Como o servidor fica sabendo do resultado — e o que
acontece com o pedido que sobrar de um processamento que falhou ou não terminou — não está nos
fontes desta jornada. Pergunta ao site.

### RN-02 — A tela não copia cadastro nenhum: registra o pedido e a auditoria

Esta tela não inclui, não altera e não exclui planejamento sazonal, cardápio, grupo, segmento de
atendimento, refeição nem tipo de órgão. O que ela grava são **duas** coisas: a **solicitação de
processamento**, com o número seguinte da fila de pedidos, e o **lançamento de auditoria** da
operação. Das **nove** gravações e das **nove** exclusões que o programa declara para os **nove**
cadastros que enxerga, **duas gravações são executadas** — a da solicitação e a da auditoria — e
**nenhuma exclusão**. A gravação do planejamento sazonal existe declarada e nunca é executada:
declarar não é executar, e os outros sete cadastros são só lidos.

### RN-03 — Só a alteração; esta tela não tem consulta

A tela abre repondo o modo de operação na **alteração** e só segue nesse modo. Qualquer outro modo
é recusado com **\* Operacao nao disponivel. Use ALT \***, com o cursor no campo do modo, antes de
ler qualquer cadastro; nesse caminho nada é lido e nada é registrado. Não há passagem de consulta:
uma vez por abertura, a tela lê o registro da própria tela, confere o acesso e sai. O modo
**não** vem de quem chamou: a tela o repõe por conta própria na abertura, e a tela anterior passa
a chamada sem informar qualquer modo.

[?] A mensagem manda usar "ALT", mas o modo que a tela aceita é o código interno de alteração do
sistema, e nenhum valor "ALT" existe no acervo lido; além disso, a própria abertura repõe o modo,
de modo que a recusa só aparece se o campo voltar diferente do que a tela repôs. Ou o formulário
traduz o que o servidor digita para esse código, ou quem seguir a mensagem é recusado, ou a recusa
é inalcançável. Pergunta ao site.

### RN-04 — As duas pontas têm nove valores cada

Cada ponta tem **nove valores**: o grupo, o segmento de atendimento, a refeição e as três partes da
data de início e as três da data-limite do período — dia, mês e ano em cada uma. Fora das duas
pontas a tela tem a impressora e a resposta da confirmação. Ao todo são **27 campos** na
apresentação: os sete do cabeçalho e do controle, os **18 valores** das duas pontas, a impressora
e a resposta.

### RN-05 — O grupo das duas pontas tem de estar cadastrado

O grupo informado tem de constar do cadastro de grupos daquele tipo de órgão. Em branco, a recusa
é **\* Informe o grupo - DE \*** ou **\* Informe o grupo - PARA \***; não constando,
**\* Grupo nao cadastrado - DE \*** ou **\* Grupo nao cadastrado - PARA \***. A origem é conferida
antes do destino, e o cursor volta ao campo recusado.

### RN-06 — O segmento de atendimento das duas pontas tem de estar cadastrado

O segmento de atendimento informado tem de constar do cadastro de segmentos daquele tipo de órgão.
Em branco, a recusa é **\* Informe o segmento - DE \*** ou **\* Informe o segmento - PARA \***;
não constando, **\* Segmento nao cadastrado - DE \*** ou
**\* Segmento nao cadastrado - PARA \***, com o cursor no campo. O segmento da origem é conferido
antes do do destino.

### RN-07 — A refeição das duas pontas tem de estar cadastrada

A refeição informada tem de constar do cadastro de refeições daquele tipo de órgão. Em branco, a
recusa é **\* Informe a refeicao - DE \*** ou **\* Informe a refeicao - PARA \***; não constando,
**\* Refeicao nao cadastrada - DE \*** ou **\* Refeicao nao cadastrada - PARA \***, com o cursor
no campo. A refeição da origem é conferida antes da do destino.

### RN-08 — O código 99 significa todos, e só vale na origem

O código **99** no grupo, no segmento de atendimento e na refeição significa **todos**: é a
convenção que as próprias mensagens do sistema registram nas telas irmãs ("Informe o grupo ou 99
para todos"). Ele só se admite na **origem**: quando um desses três códigos da origem é 99, a tela
repõe o código do destino com 99, e o mesmo acontece com os outros dois. Digitando 99 apenas no
destino, a recusa é **\* Nao use 99 para esta opcao - PARA \***, no campo do grupo, do segmento ou
da refeição, conforme o caso. Com 99 não se procura no cadastro aquele grupo, aquele segmento nem
aquela refeição: o "todos" dispensa a procura.

[?] A conferência seguinte, que decide se o cadastro existe, olha um indicador que só a própria
leitura do cadastro preenche; no caminho do 99 essa leitura é saltada, e o acervo não mostra o que
o indicador vale ali. Se um 99 na origem pode ser recusado como "grupo não cadastrado" por causa
do que uma tentativa anterior deixou no indicador, o caminho não sustenta a regra sozinho. Pergunta
ao site.

### RN-09 — O período é o do cardápio em vigor na data-limite informada

O período não é escolhido por um código: ele é identificado pela **data-limite** que o servidor
informa, dentro do tipo de órgão, e isso vale para as duas pontas. A tela procura um cardápio com
essa data-limite; não havendo, recusa com **\* Cardapios nao cadastrados para esta data - DE \***
na origem ou **\* Cardapios nao cad. para esta data - PARA \*** no destino, devolvendo o cursor ao
campo da data-limite. A **data de início** que a tela exibe — e que entrega ao processamento — não
é a que o servidor digitou: ela é reposta com a data de início do cardápio encontrado, nas duas
pontas.

[?] As duas datas de início são pedidas e passam pela edição numérica, mas são descartadas assim
que o cardápio é encontrado, e os seus seis campos não têm posição de cursor. Se elas deveriam
identificar o cardápio ou conferir o que foi lido, o caminho não as usa. Pergunta ao site.

[?] Nenhuma das seis datas das duas pontas é conferida como data: não há, nesta tela, a recusa de
data inválida nem a de data de início maior que a data-limite, que as telas irmãs têm. A tela só
confere a existência do cardápio naquela data-limite. Se as datas deveriam ser validadas aqui, o
caminho não valida. Pergunta ao site.

### RN-10 — A origem tem de ter planejamento sazonal para a data-limite informada

Além do cardápio, a origem tem de ter **planejamento sazonal** para a data-limite informada: não
havendo, a recusa é **\* Planejamentos sazonais nao cadastrados - DE \***, com o cursor no campo da
data-limite da origem. É a última conferência antes da impressora: o destino **não** é conferido
quanto a já ter planejamento — quem decide o que fazer com o que existe lá é o processamento.

[?] A procura do planejamento leva na chave o tipo de órgão, as três partes da data-limite e o
grupo (ou o registro de "todos", quando o grupo da origem é 99), mas a conferência que compara de
volta só olha o tipo de órgão e a data-limite: o segmento, a refeição e o cardápio não entram. Se a
leitura exige a chave inteira ou apenas se posiciona no primeiro planejamento a partir dela — e se
a origem de "todos" aceita o planejamento de outro segmento —, o acervo não permite concluir.
Pergunta ao site.

### RN-11 — A impressora é obrigatória

Sem a impressora informada, a tela não segue: a recusa é **\* Informe a impressora \***, com o
cursor no campo. É a última conferência antes da pergunta de confirmação.

### RN-12 — A cópia só é pedida depois de confirmada, e mudar um valor refaz a conferência

Passadas todas as conferências, a tela mostra
**\* Confirma copia planejamentos sazonais <S/N> ? \*** e espera a resposta; só a resposta **S**
registra o pedido. Junto com a resposta, os **doze** valores que identificam as duas pontas — o
grupo, o segmento de atendimento e a refeição de cada uma e as três partes da data-limite de cada
uma — têm de continuar iguais aos que a tela guardou; mudando qualquer um deles, as conferências
recomeçam e a confirmação volta a ser pedida. As seis partes das datas de início não entram nessa
comparação.

[?] Responder **N** não cancela: a tela limpa a resposta, repõe o que já estava em tela e **volta a
pedir a mesma confirmação**. Não há, no caminho lido, um desfecho que encerre a operação com a
resposta negativa — a única saída é abandonar a tela ou tornar algum dado inválido. Se o esperado é
que N cancele, o caminho não cancela. Pergunta ao site.

### RN-13 — Um pedido já registrado para esta cópia impede outro

Antes de registrar, a tela confere se já existe **solicitação de processamento registrada** para
esta mesma cópia; existindo, recusa com **\* Relatorio em processamento. Aguarde. \***, com o
cursor na resposta, e não registra nada. Quem apaga a solicitação da fila é o próprio
processamento, ao terminar: o impedimento dura enquanto a cópia estiver pendente.

[?] A conferência procura as solicitações com a marca de atendimento em branco e o número do
pedido **zerado**, mas a solicitação que esta tela grava tem número positivo; e, do registro que
encontra, só confere de volta o código da cópia, nunca a marca de atendimento. Se uma solicitação
já atendida também bloqueia — e se o número zerado encontra alguma coisa —, o acervo não permite
concluir. Pergunta ao site.

### RN-14 — O pedido leva as duas pontas, a impressora, quem pediu e de onde

A solicitação é registrada na fila de processamento com o **número seguinte** ao último já usado, o
código da cópia, o tipo de órgão, a matrícula, a estação e o dia, o mês e o ano da sessão, e **sem
marca de atendimento**. Junto vão, para o processamento, a impressora, uma via, a estação, a
matrícula, o **e-mail lido do cadastro do funcionário** e os 18 valores das duas pontas. É por essa
entrega que o processamento sabe o que copiar e para onde.

[?] O e-mail do servidor segue no pedido entregue ao processamento e **não** é gravado na
solicitação da fila: para onde ele vai e o que o processamento faz com ele não está nos fontes
desta jornada. Pergunta ao site.

### RN-15 — Todo pedido deixa rastro na auditoria

Cada pedido registra um lançamento na auditoria com o tipo de órgão e a CRE da sessão, os 18
valores das duas pontas pedidos, precedidos do tipo de órgão, a tela de origem, a operação, a
matrícula, a estação e a data e a hora da sessão, e com o valor posterior em branco. O lançamento
guarda **o que foi pedido**, não o que foi copiado.

[?] A trilha registra a operação como **inclusão** e identifica o cadastro alterado pela própria
tela, não pelo planejamento; além disso, o número do processo do lançamento recebe o **dia da data
de início do destino**, e nunca um número de processo de verdade. O acervo não diz se isso é
intencional nem o efeito na chave da auditoria, que usa justamente o número do processo. Pergunta
ao site.

### RN-16 — A digitação dos dezoito campos numéricos é editada, e o cursor volta a doze deles

Os **dezoito campos numéricos** — os dois grupos, os dois segmentos de atendimento, as duas
refeições e as doze partes das datas — passam pela edição numérica antes de qualquer leitura: campo
em branco é tratado como zero, e o que não for número é recusado. O cursor volta ao campo recusado
para **doze** deles: os dois grupos, os dois segmentos, as duas refeições e as seis partes das
datas-limite. As seis partes das datas de início não têm posição de cursor.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não está nos
fontes desta jornada: a rotina que faz a edição numérica é declarada no programa de runtime e não
tem corpo no acervo lido. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Cópia do planejamento sazonal de uma origem para um destino

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C764T

  Cenário: O pedido de cópia das duas pontas
    Dado que informei a origem com grupo, segmento, refeição e um período que tem cardápio e planejamento
    E informei o destino com grupo, segmento, refeição e um período que tem cardápio
    E informei a impressora
    Quando respondo S à confirmação
    Então vejo a mensagem "* Cadastro sendo atualizado *"
    E a solicitação de processamento é registrada
    E a operação fica registrada na auditoria

  Cenário: A tela não copia o planejamento sazonal
    Dado que confirmo a cópia
    Então nenhum planejamento sazonal, cardápio, grupo, segmento de atendimento, refeição ou tipo de órgão é incluído, alterado ou excluído por esta tela
    E o que fica registrado é a solicitação de processamento e a auditoria

  Cenário: O processamento recebe as duas pontas
    Dado que confirmo a cópia
    Então o processamento recebe o grupo, o segmento, a refeição e as duas datas de cada ponta
    E recebe a impressora, uma via, a estação, a matrícula e o meu e-mail lido do cadastro do funcionário

  Cenário: O pedido recebe o número seguinte da fila
    Dado que confirmo a cópia
    Então a solicitação é registrada com o número seguinte ao último já usado
    E fica sem marca de atendimento

  Cenário: Todo pedido deixa rastro na auditoria
    Dado que confirmei o pedido de cópia
    Quando o registro termina
    Então existe um lançamento de auditoria com o tipo de órgão, a CRE e os 18 valores das duas pontas pedidos
    E com a operação, a tela de origem, a matrícula, a estação e a data e a hora da sessão
    E com o valor posterior em branco

  Cenário: Modo diferente da alteração
    Dado que o modo informado não é a alteração
    Quando envio a tela
    Então vejo "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo do modo
    E nenhum cadastro é lido

  Cenário: Esta tela não tem consulta
    Dado que envio a tela no modo de consulta
    Então nenhum cadastro é lido e nada é registrado
    E o único modo que a tela aceita é a alteração, reposta por ela mesma na abertura

  Cenário: Grupo não cadastrado
    Quando informo um grupo que não consta do cadastro daquele tipo de órgão
    Então vejo "* Grupo nao cadastrado - DE *" ou "* Grupo nao cadastrado - PARA *"
    E o cursor volta ao campo do grupo recusado
    E nada é registrado

  Cenário: Grupo em branco
    Quando envio a tela sem informar o grupo de uma das pontas
    Então vejo "* Informe o grupo - DE *" ou "* Informe o grupo - PARA *"
    E o cursor volta ao campo do grupo
    E nada é registrado

  Cenário: Segmento não cadastrado
    Quando informo um segmento que não consta do cadastro daquele tipo de órgão
    Então vejo "* Segmento nao cadastrado - DE *" ou "* Segmento nao cadastrado - PARA *"
    E o cursor volta ao campo do segmento recusado
    E nada é registrado

  Cenário: Segmento em branco
    Quando envio a tela sem informar o segmento de atendimento de uma das pontas
    Então vejo "* Informe o segmento - DE *" ou "* Informe o segmento - PARA *"
    E o cursor volta ao campo do segmento
    E nada é registrado

  Cenário: Refeição não cadastrada
    Quando informo uma refeição que não consta do cadastro daquele tipo de órgão
    Então vejo "* Refeicao nao cadastrada - DE *" ou "* Refeicao nao cadastrada - PARA *"
    E o cursor volta ao campo da refeição recusada
    E nada é registrado

  Cenário: Refeição em branco
    Quando envio a tela sem informar a refeição de uma das pontas
    Então vejo "* Informe a refeicao - DE *" ou "* Informe a refeicao - PARA *"
    E o cursor volta ao campo da refeição
    E nada é registrado

  Cenário: A origem é conferida antes do destino
    Dado que nem a origem nem o destino estão cadastrados
    Quando envio a tela
    Então vejo a recusa da origem
    E só depois de corrigir a origem a tela confere o destino

  Cenário: 99 apenas no destino
    Dado que o grupo, o segmento ou a refeição da origem não é 99
    Quando informo 99 no grupo, no segmento ou na refeição do destino
    Então vejo "* Nao use 99 para esta opcao - PARA *"
    E o cursor volta ao campo do destino
    E nada é registrado

  Cenário: 99 na origem vale para as duas pontas
    Dado que informo 99 no grupo da origem
    Quando envio a tela
    Então o grupo do destino passa a ser 99 também
    E nenhum grupo é procurado no cadastro

  Cenário: 99 na origem dispensa a procura dos três códigos
    Dado que informo 99 no grupo, no segmento e na refeição da origem
    Quando envio a tela
    Então os três códigos do destino passam a ser 99
    E nenhum grupo, segmento ou refeição é procurado no cadastro

  Cenário: Período de origem sem cardápio na data-limite
    Quando informo uma data-limite de origem que não tem cardápio cadastrado
    Então vejo "* Cardapios nao cadastrados para esta data - DE *"
    E o cursor volta ao campo da data-limite de origem
    E nada é registrado

  Cenário: Período de destino sem cardápio na data-limite
    Quando informo uma data-limite de destino que não tem cardápio cadastrado
    Então vejo "* Cardapios nao cad. para esta data - PARA *"
    E o cursor volta ao campo da data-limite de destino
    E nada é registrado

  Cenário: As datas de início vêm do cardápio cadastrado
    Dado que digitei datas de início diferentes das dos cardápios cadastrados
    Quando envio a tela
    Então a data de início de cada ponta passa a ser a do cardápio cadastrado
    E são essas datas que vão para o processamento

  Cenário: Origem sem planejamento sazonal para a data-limite
    Dado que a origem tem cardápio mas não tem planejamento sazonal para aquela data-limite
    Quando envio a tela
    Então vejo "* Planejamentos sazonais nao cadastrados - DE *"
    E o cursor volta ao campo da data-limite de origem
    E nada é registrado

  Cenário: Destino sem planejamento não impede o pedido
    Dado que o destino não tem planejamento sazonal para a data-limite informada
    E a origem tem cardápio e planejamento
    Quando confirmo a cópia
    Então o pedido é registrado
    E o que fazer com o planejamento que já existe no destino fica por conta do processamento

  Cenário: Impressora em branco
    Quando envio a tela sem informar a impressora
    Então vejo "* Informe a impressora *"
    E o cursor volta ao campo da impressora
    E nada é registrado

  Cenário: A confirmação vem antes de qualquer registro
    Dado que todas as conferências passaram
    Quando envio o pedido
    Então vejo "* Confirma copia planejamentos sazonais <S/N> ? *"
    E nenhuma solicitação foi registrada ainda

  Cenário: A resposta negativa não cancela e não grava nada
    Dado que a tela pediu a confirmação
    Quando respondo N
    Então a tela volta a pedir a confirmação
    E nenhuma solicitação é registrada
    E nenhum planejamento é copiado

  Cenário: Mudar um valor depois da confirmação faz a confirmação voltar
    Dado que a tela pediu a confirmação
    Quando mudo a data-limite do destino e respondo S
    Então a tela volta a conferir o pedido
    E volta a pedir a confirmação, sem registrar nada

  Cenário: Mudar só a data de início não desfaz a confirmação
    Dado que a tela pediu a confirmação
    Quando mudo a data de início da origem e respondo S
    Então a tela registra o pedido
    E a data de início que segue para o processamento é a do cardápio cadastrado

  Cenário: Já existe pedido desta cópia
    Dado que existe solicitação de processamento registrada para esta cópia
    Quando respondo S à confirmação
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da resposta
    E uma segunda solicitação não é registrada

  Cenário: Digitação não numérica nos campos informados
    Dado que digitei algo que não é número em um dos dezoito campos numéricos
    Quando envio a tela
    Então o sistema recusa a digitação antes de ler qualquer cadastro
    E o cursor volta ao campo recusado, quando ele tem posição de cursor

  Cenário: Datas de início impossíveis
    Dado que digitei uma data de início que não existe no calendário
    Quando envio a tela
    Então nenhuma recusa de data inválida aparece
    E a tela só decide pela existência do cardápio na data-limite informada
```
