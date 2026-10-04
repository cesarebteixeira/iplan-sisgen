# US — P211T — Pré-liquidar o processo e ver a sua situação

## Estória

Como **servidor de CRE**, quero **pré-liquidar um processo contra o empenho em que ele
corre — informando o número SEI, o empenho e o ano do exercício — e, quando for o caso,
anular essa pré-liquidação**, para que **o aceite do processo chegue ao SIAFIC e a
despesa possa seguir, e para que eu veja, pelo número do processo, em que empenho ele
está e qual é a ordem da sua situação**.

A pré-liquidação é o aceite do processo contra o empenho: é ela que diz que o processo
foi conferido e está autorizado a seguir. Sem esta tela, a despesa fica no empenho sem
esse aceite e o SIAFIC não recebe nada; e desfazer uma pré-liquidação já transmitida só
se faz por aqui. É também por aqui que se vê, pelo número do processo, em que empenho
ele corre, o fornecedor, os valores e a ordem da sua situação.

A tela grava: registra a pré-liquidação e a anulação no cadastro de transmissão ao
SIAFIC e desfaz, nesse mesmo cadastro, o que ainda não foi aceito. Só a consulta não
grava nada. E ela recusa em vez de gravar pela metade: exige o número SEI, exige o
empenho e o exercício, confere o empenho, o fornecedor e o tipo de contrato contra o
seu cadastro, soma as notas fiscais do processo e os seus gêneros — e recusa quando as
duas somas não fecham, quando o processo já está pré-liquidado, liquidado ou pago,
quando já há transmissão ao SIAFIC em curso e quando o processo corre em mais de um
empenho.

**O que o processo traz escrito decide a conversa.** Cada processo guarda, no seu
registro, por qual tela ele passou — e é desse registro que sai a marca de que ele
está em pagamento. Quando o processo carrega essa marca, esta tela não pré-liquida,
não anula e não responde pela via normal: ela recusa, porque pré-liquidar e anular são
operações da via do processo, não da via do pagamento. O operador que insistir não vê
erro nenhum de sistema — vê a recusa de negócio, e nada é gravado.

## Contexto

Jornada S000M → P000M → P211T.

Ator: servidor de CRE — informa o número SEI do processo, o empenho e o ano do
exercício, pré-liquida ou anula a pré-liquidação e consulta a situação do processo.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O passo anterior desta jornada, o `P000M`, é um menu de seis opções: não procura
processo nenhum, não deixa dado de negócio na sessão e não informa operação. Quem
escolhe a operação é o operador, no campo de operação desta tela — e a tela se
apresenta na inclusão. O que ela usa das telas anteriores é o que a entrada deixou na
sessão: o **tipo de órgão**, a **CRE do vínculo**, a **matrícula**, o **código de
acesso** e a **data e a hora do sistema**; e ela relê o **cadastro de tipos de órgão**
para saber a secretaria do tipo de órgão da sessão.

Esta tela **não encadeia em nenhuma outra**: terminada a operação, ela reabre a si
mesma — não entrega processo nem operação a uma tela seguinte. A marca de pagamento
que ela lê vem do registro do processo, escrito por outra tela do sistema, e não de
uma chamada desta jornada.

## Regras de negócio

### RN-01 — Nada é lido nem gravado sem as conferências de tela, de acesso, de rota e de estação

Ao abrir, a tela confere: a sessão tem de estar no terminal em que foi aberta — em
outro, o acesso termina; o registro da tela tem de existir, senão
**\* Tela nao disponivel \***; e o código de acesso do servidor tem de alcançar a tela,
senão **\* Acesso negado para esta matricula \***. Na confirmação ela passa pela
conferência de rota — tela fora do registro é recusada com
**\* Tela nao cadastrada \***, e operação que a tela não prevê, com
**\* Operacao nao disponivel \*** — e pela permissão da operação: a **inclusão** exige a
permissão de inclusão e a **exclusão**, a de exclusão, e quem não tem a permissão vê
**\* Acesso negado para esta operacao \***. A **consulta não é barrada por essa
permissão**. Se a transação chegar com um **prefixo de rota** preenchido, a tela não
faz nada: o prefixo leva o servidor para a tela nele indicado.

### RN-02 — A tela serve a três operações e recusa as demais

A tela trabalha com **inclusão** (pré-liquidar), **exclusão** (anular a pré-liquidação)
e **consulta**, e ao ser aberta apresenta-se na inclusão. Operação diferente dessas
três é recusada com **\* Opcao nao disponivel. Use INC, EXC ou CON \***, o cursor volta
ao campo da operação e nada é lido nem gravado.

[?] A mensagem nomeia as operações como INC, EXC e CON, mas os valores que a tela
aceita no campo da operação são os códigos que o resto do sistema usa para inclusão,
exclusão e consulta. Quem digitar o que a mensagem manda é recusado. Ou a mensagem está
errada, ou a tela traduz o que o operador digita em algum ponto que não está no acervo
lido. Pergunta ao site.

### RN-03 — A tela muda de conversa conforme a tela por que o processo passou

Cada processo guarda, no seu **registro de processo**, o código da **tela por onde ele
passou** — e é esse código que esta tela lê, junto com o número do processo, para saber
de que via ele vem. Quando o código é o da **tela de pagamento (P212T)**, o processo
está em pagamento e é um pagamento de **um único empenho**; quando é o de **outra
tela**, inclusive desta, o processo é tratado pela via da pré-liquidação.

Desse código saem **três** decisões diferentes — e é a única coisa que as separa, a
mesma leitura do mesmo campo:

| Via do processo | Inclusão | Exclusão | Consulta |
| --- | --- | --- | --- |
| **P212T** (em pagamento) | recusa com **\* Processo em mais de 1 empenho \*** | recusa com **\* Processo nao esta pre-liquidado \*** quando a situação não é a de pré-liquidado | segue: o pagamento de um empenho é mostrado |
| **Outra tela** (via da pré-liquidação) | segue, e recusa pela situação do processo | segue, e recusa pela situação do processo | recusa com **\* Pagamento em mais de um empenho \*** quando o processo **não** traz a marca de pagamento |

Quem escreve esse código é a tela que mantém o registro do processo — normalmente a
tela por onde o processo passou. Nesta jornada ninguém o escreve: ele é **lido**.

[?] O código que esta tela procura é o da tela de pagamento, e o acervo lido não tem
fonte que mostre essa tela gravando-o no registro do processo; as outras telas do mesmo
assunto procuram nele o código da **tela de pré-liquidação**, o que reforça que o campo
é escrito pela tela que passou. Se quem o escreve é a tela de pagamento, como o nome do
campo sugere, ou um serviço de manutenção do processo, e em que momento, é pergunta ao
site.

### RN-04 — Ao abrir, a tela propõe o número do processo e o número SEI com o que a sessão conhece

Ao ser aberta, a tela preenche, no **número interno do processo**, a **secretaria** que
o cadastro de tipos de órgão guarda para o **tipo de órgão da sessão** e, na parte do
grupo, a **CRE do vínculo do servidor**; e, no **número SEI**, a parte do ano com o
**ano do sistema**. Fora dos números, ela mostra a **data do sistema** e a **descrição
do tipo de órgão** da sessão. Quando o vínculo do servidor não tem CRE, a parte do
grupo fica em branco — e o operador a informa, se for o caso.

Quando o cadastro de tipos de órgão marca o processo como **sequencial** da secretaria,
a tela propõe também, na parte do grupo, a **CRE do vínculo**: nesse tipo de órgão o
processo corre na CRE do servidor e não na secretaria.

[?] O cadastro de tipos de órgão tem um indicador sobre o processo que a tela consulta
antes de montar o número, e a montagem da parte do grupo acontece tanto para o
indicador ligado quanto para o desligado — o que muda entre os dois é só a origem do
valor. Se o indicador existe para outro caso, é pergunta ao site.

### RN-05 — Os campos informados passam pela edição numérica

Os **vinte e dois campos numéricos** da tela — o tipo de órgão, o dia, o mês e o ano do
processo, as **quatro partes do número interno do processo**, as **quatro partes do
número SEI**, o empenho, o ano de referência, o órgão financeiro, a fonte, o
fornecedor, a ordem, o valor do processo e o valor do imposto — são tratados como
número: o campo em branco conta como zero — a tela faz isso explicitamente no número do
processo, nas quatro partes do SEI, no empenho, no ano, na fonte e na ordem — e o que
não for número é recusado.

[?] O que o operador vê quando o campo não é número não está no acervo lido: a rotina
que faz essa edição aparece no acervo só como declaração, sem corpo, e a mensagem que
ela usa não veio no lote. Dos vinte e dois campos, a tela devolve o cursor às quatro
partes do número SEI, ao empenho e ao ano; para os outros dezesseis não há posição de
cursor definida. Pergunta ao site.

### RN-06 — Toda operação começa pelo número SEI, que tem de existir

As três operações começam pelo **número SEI** do processo. Sem ele, a recusa é
**\* Informe o SEI \***, com o cursor de volta ao campo. Informado um número SEI que
não está em nenhuma nota fiscal do processo, a recusa é **\* SEI nao cadastrado \***,
também com o cursor no campo, e nada é feito. Achado o SEI, a tela toma dele o
**número interno do processo** e passa a trabalhar com esse número.

[?] O número SEI que a tela monta tem **dezoito caracteres**, em quatro partes; o
dicionário de dados declara o campo do SEI com **dezessete** nos cadastros que a tela
lê, e o layout com que o programa lê esses mesmos cadastros declara dezoito. Os dois
não batem, e qual é o tamanho do SEI é pergunta ao site.

### RN-07 — O processo de outra CRE é recusado

Achado o SEI, a tela confere a **CRE da nota fiscal** com a **CRE do vínculo do
servidor**. Quando o vínculo tem CRE e as duas não coincidem, a recusa é
**\<- Usuario sem acesso a este grupo \*** — a mensagem começa com a CRE do processo —
e o cursor volta ao campo do SEI. Quando o vínculo não tem CRE, essa conferência não é
feita.

### RN-08 — O processo em pagamento não é pré-liquidado nem anulado por esta tela

Quando o processo traz a marca da **tela de pagamento**, a via da pré-liquidação está
fechada para ele, e é assim nas duas operações que gravam:

- na **inclusão**, a tela recusa com **\* Processo em mais de 1 empenho \***, com o
  cursor no campo do SEI, e nada é lido nem gravado;
- na **exclusão**, a tela recusa com **\* Processo nao esta pre-liquidado \***
  **sempre que a situação do processo não for a de pré-liquidado** — mesmo que ele já
  esteja liquidado ou pago, e mesmo que já esteja pré-liquidado, se a marca de
  pagamento estiver presente, a recusa é essa.

Vale dizer o que **não** acontece: a tela não avisa que a operação é da via do
pagamento; ela responde como se não houvesse pré-liquidação para tratar. O operador
que tentar pré-liquidar um processo que está em pagamento, ou anular a pré-liquidação
dele, vê a recusa de negócio e nenhum registro é feito.

### RN-09 — A inclusão exige o empenho e o exercício, e a combinação tem de estar cadastrada

Na inclusão, o operador informa o **número do empenho** e o **ano do exercício**. Sem
o empenho, a recusa é **\* Informe o numero do empenho \***; sem o ano, a recusa é
**\* Informe o ano do exercicio \***; cada uma devolve o cursor ao seu campo.

Empenho, fornecedor e tipo de contrato têm de estar cadastrados: a tela procura essa
combinação — tipo de órgão, ano de referência, empenho, fornecedor e tipo de contrato —
e, não achando, recusa com **\* Cad. Empenho/Fornecedor/TC na tela P535T \***, com o
cursor no campo do empenho: é na tela P535T que essa combinação se cadastra.

### RN-10 — A inclusão percorre as notas fiscais do processo e confere a soma dos gêneros

A inclusão percorre as **notas fiscais** do processo: soma os valores, soma o imposto,
toma o fornecedor, o tipo de contrato e a CRE, e a data da última nota passa a ser a
**data do processo**. Sem nenhuma nota fiscal para o processo, a recusa é
**\* Processo nao cadastrado \***, com o cursor no campo do SEI.

Em seguida a tela percorre os **itens do processo, por gênero** — ignorando os que
estão excluídos — e soma os seus valores. Se a soma dos gêneros for diferente do total
das notas fiscais, a recusa é **\* Valor dos generos difere do total do processo \***.

### RN-11 — A inclusão recusa a situação que já andou e a transmissão em curso

Ainda antes de mostrar qualquer coisa, a inclusão procura o processo no **cadastro de
transmissão ao SIAFIC** e no **cadastro de processos**. Todas as recusas abaixo deixam
o cursor no campo do SEI:

| o que a tela acha | a mensagem |
| --- | --- |
| transmissão da pré-liquidação desse processo que ainda não voltou | **\* Processo ja em transmissao ao SIAFIC \*** |
| transmissão da pré-liquidação em outro empenho | **\<- Proc em transmissao em outro empenho \*** |
| transmissão da anulação em outro empenho | **\<- Aguarde. Proc sendo anulado em outro emp \*** |
| registro marcado como processo em mais de um empenho | **\* Processo em mais de 1 empenho \*** |
| registro do processo, naquele empenho e exercício, com a situação de pré-liquidado | **\* Processo ja esta pre-liquidado \*** |
| o mesmo, com a situação de liquidado | **\* Processo ja esta liquidado \*** |
| o mesmo, com a situação de pago | **\* Processo ja esta pago \*** |
| registro do processo em outro empenho | **\<- Processo em outro empenho \*** |

Nas mensagens que começam com a seta, a tela mostra antes do texto o **número do
empenho** que está no registro achado.

### RN-12 — A tela desfaz o que o SIAFIC ainda não aceitou, e recusa o que está em curso

Quando há, para o processo, uma transmissão ao SIAFIC **com o retorno já preenchido**,
a tela apaga a resposta do SIAFIC e o próprio registro da transmissão antes de seguir:
era esse retorno que impedia o reenvio. Quando a transmissão ainda está em curso, isto
é, sem retorno, a recusa é **\* Processo em transmissao \***, com o cursor no campo do
SEI.

Na **inclusão**, quando existe uma **anulação** desse processo naquele mesmo empenho e
exercício ainda não aceita, a tela apaga esse registro e segue para pré-liquidar. Na
**exclusão**, quando a **pré-liquidação** do processo está transmitida e ainda não foi
aceita, a tela apaga o registro dessa transmissão e informa
**\* Pre-liquidacao Anulada \*** — o processo volta a poder ser pré-liquidado do zero.

[?] Esse desfazimento é feito no meio da conferência, antes de a operação ser
aprovada: se uma recusa posterior derrubar a operação, o registro já foi apagado e nada
o repõe. Se o desfazimento deveria acontecer só depois de a operação passar por todas
as conferências, é pergunta ao site.

[?] Entre a exclusão, a tela procura a transmissão da pré-liquidação e, quando a acha
com o processo e o exercício iguais aos informados, **apaga o registro e prossegue como
inclusão** — isto é, anula e pré-liquida de novo no mesmo comando —, mas a mesma
procura, quando o registro é a anulação em transmissão, manda o operador aguardar. Os
dois casos leem a mesma tabela pela mesma chave e são tratados em sentidos opostos; se
o apagamento e a inclusão no mesmo comando são intencionais, é pergunta ao site.

### RN-13 — Antes de concluir a operação, a tela exige o tipo de órgão ativo

Depois das conferências e antes de concluir qualquer das três operações — inclusive a
consulta —, a tela relê o **cadastro de tipos de órgão** pelo tipo de órgão da sessão.
Se o registro estiver marcado como **excluído** ou **expurgado**, a operação é
abandonada e nada é gravado.

[?] A mensagem que o operador vê nessa recusa não está no acervo lido: a tela pede ao
sistema a mensagem de número 126, e o texto dessa mensagem vive num arquivo de
mensagens que não veio no lote. É pergunta ao site qual é o texto e se ele é o mesmo
para os dois casos, o excluído e o expurgado.

### RN-14 — A inclusão mostra o que vai transmitir, pede um segundo comando e só então registra a pré-liquidação

Passadas as conferências, a tela mostra o que vai transmitir: a **data do processo**
(dia, mês e ano), o **empenho**, o **ano de referência**, o **número interno do
processo** nas suas quatro partes, o **fornecedor** com o código, a razão social e o
CNPJ, o **órgão financeiro**, o **valor das notas fiscais** e o **valor do imposto**, e
o rótulo **"Fonte    :"** quando há fonte. Com isso aparece a mensagem
**\* Transmita para autorizar a pre-liquidacao \*** — e **nada foi gravado ainda**: a
gravação depende de o operador transmitir de novo os mesmos dados. Nesse segundo
comando a tela registra a pré-liquidação no **cadastro de transmissão ao SIAFIC** e
mostra **\* Pre-Liquidacao enviada ao SIAFIC \***. O registro sai marcado como
pré-liquidação de um empenho e com a **matrícula do servidor**, a **data e a hora**, a
CRE, o tipo de órgão, o órgão financeiro, o fornecedor e o CNPJ, o tipo de contrato, os
valores, o número do processo, o número SEI, o empenho e o ano de referência.

Se já houver uma pré-liquidação registrada para o mesmo processo, empenho e exercício, a
tela **não duplica**: não grava de novo e não mostra a mensagem de envio.

O **órgão financeiro** sai do cadastro de órgãos financeiros por CRE — pelo tipo de
órgão e a CRE — e é substituído pelo que o cadastro de contratos guardar para o tipo de
contrato, quando esse valor existe.

[?] Entre os dois comandos a tela confere só a operação, o número do processo, o
empenho e o ano. Se o operador trocar, no segundo comando, um dado que não seja um
desses quatro — a justificativa da anulação, por exemplo —, nada é reconferido e o que
fica gravado é o que valia no primeiro. Pergunta ao site se essa é a intenção.

### RN-15 — A exclusão anula a pré-liquidação

A exclusão é a **anulação** da pré-liquidação. Ela exige o empenho, o ano do exercício e
a **justificativa da anulação**: sem a justificativa, a recusa é
**\* Informe a justificativa da anulacao \***, com o cursor no campo.

A tela confere o **cadastro de processos** e recusa, com o cursor no campo do SEI:

| o que a tela acha | a mensagem |
| --- | --- |
| nenhum registro do processo naquele empenho e exercício | **\* Processo nao esta pre-liquidado \*** |
| registro com a situação de liquidado, sem a marca de pagamento | **\* Processo ja esta liquidado \*** |
| registro com a situação de pago, sem a marca de pagamento | **\* Processo ja esta pago \*** |
| registro marcado como processo em mais de um empenho | **\* Processo em mais de 1 empenho \*** |
| registro do processo em outro empenho | **\<- Processo em outro empenho \*** |

Confere também o **cadastro de transmissão ao SIAFIC**: anulação já transmitida,
**\* Anulacao em transmissao ao SIAFIC \***; anulação em outro empenho,
**\<- Proc em anulacao em outro empenho \***; pré-liquidação em transmissão em outro
empenho, **\<- Proc em transmissao em outro emp \***; e registro marcado como processo
em mais de um empenho, **\* Processo em mais de 1 empenho \***.

Passando pelas conferências, a tela mostra a **ordem de anulação** e a mensagem
**\* Transmita para autorizar a anulacao \***; no comando seguinte, registra a anulação
no cadastro de transmissão ao SIAFIC, com a **justificativa**, e mostra
**\* Anulacao enviada ao SIAFIC \***.

### RN-16 — A justificativa da anulação é gravada sem acentos

A justificativa da anulação é gravada **sem acentos**: a tela troca as letras acentuadas
pelas letras simples correspondentes e descarta os caracteres que não estejam previstos
— letras, algarismos, espaço e a pontuação comum. É esse texto, já limpo, que a tela
mostra e que segue para o SIAFIC.

### RN-17 — A consulta mostra o processo e a ordem da sua situação

A consulta exige o número SEI, o empenho e o ano, procura o processo no **cadastro de
processos** e mostra: a **data do processo**, o **empenho**, o **ano**, o **órgão
financeiro**, o **fornecedor** com a razão social e os **valores do processo**. Conforme
a situação do processo, ela mostra a ordem correspondente, com o rótulo do estado:
**"Ordem de pre-liquida :"** com a ordem de pré-liquidação; **"Ordem de liquidacao  :"**
com a ordem de pagamento; **"Ordem de pagamento   :"** com a ordem de pagamento.

Não achando o processo no cadastro de processos, a recusa é
**\* Processo nao cadastrado ou fechado \***, com o cursor no campo do SEI. E quando o
processo **não** traz a marca da tela de pagamento, a recusa é
**\* Pagamento em mais de um empenho \***, com o cursor no campo do SEI: a consulta só
responde pelo processo quando reconhece nele um pagamento de um único empenho.

[?] O rótulo "Ordem de liquidacao" mostra a **ordem de pagamento**: o cadastro do
processo guarda uma ordem de pré-liquidação e uma ordem de pagamento, e não tem campo
de ordem de liquidação. Ou a ordem de liquidação é a mesma da de pagamento, ou falta o
campo. Pergunta ao site.

[?] A consulta recusa os processos **sem** a marca da tela de pagamento, enquanto a
inclusão e a exclusão recusam justamente os processos **com** essa marca — é o mesmo
campo, lido em sentidos opostos pelas três operações da mesma tela. Pode ser que a
consulta tenha sido escrita para a via do pagamento e a inclusão e a exclusão para a via
da pré-liquidação, e que a tela sirva às duas; ou que uma das duas leituras esteja
invertida. Não se escolhe um dos dois lados. Pergunta ao site.

### RN-18 — A consulta não grava nada

A consulta só lê: o cadastro de telas, o de acessos, o de tipos de órgão, o de notas
fiscais, o de processos e o de fornecedores. Nenhum registro é incluído, alterado ou
excluído e nada é enviado ao SIAFIC.

### RN-19 — Depois de gravar, a tela se reabre limpa para o próximo processo

Terminada a gravação — a pré-liquidação enviada, a anulação enviada ou a pré-liquidação
anulada —, a tela **reabre a si mesma**, com o **número do processo** e o **número SEI**
limpos (na primeira parte do número fica a secretaria da sessão) e sem nenhum dado do
processo anterior. Na anulação que apenas desfez uma pré-liquidação ainda não aceita, a
tela volta à **inclusão**; nos demais casos a operação continua a que estava. É a única
saída desta tela: ela não entrega o processo nem a operação a nenhuma tela seguinte.

## Cenários BDD

```gherkin
Funcionalidade: Pré-liquidar o processo e ver a sua situação

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela P211T

  Cenário: Abertura da tela
    Dado que o meu vínculo tem CRE e o meu tipo de órgão está no cadastro de tipos de órgão
    Quando abro a tela P211T
    Então a tela se apresenta na inclusão
    E o número interno do processo vem com a secretaria do meu tipo de órgão
    E vem com a CRE do meu vínculo
    E o número SEI vem com o ano do sistema
    E vejo a data do sistema e a descrição do meu tipo de órgão

  Cenário: Abertura da tela sem CRE no vínculo
    Dado que o meu vínculo não tem CRE
    Quando abro a tela P211T
    Então a parte do grupo do número do processo fica em branco e eu a informo

  Cenário: Operação diferente das três
    Dado que estou na tela P211T
    Quando informo uma operação que não é inclusão, exclusão nem consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use INC, EXC ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: Tela não disponível para o meu acesso
    Dado que o registro da tela P211T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela P211T liberada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Operação não liberada para o meu acesso
    Dado que o meu código de acesso não libera a operação que informei nesta tela
    Quando confirmo
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é lido nem gravado

  Cenário: Consulta não precisa de permissão de operação
    Dado que o meu código de acesso não tem inclusão nem exclusão liberadas nesta tela
    Quando confirmo uma consulta
    Então a consulta é feita normalmente

  Cenário: Estação diferente da da entrada
    Dado que a minha estação não é a mesma do início da sessão
    Quando tento operar
    Então o acesso termina e o sistema volta à tela de entrada

  Cenário: Campo não numérico
    Dado que estou na tela P211T
    Quando informo letras em um dos campos numéricos
    Então o campo é recusado antes de qualquer consulta
    E o cursor volta ao campo
    E nada é gravado

  Cenário: Número SEI não informado
    Dado que estou na tela P211T
    Quando confirmo sem informar o número SEI
    Então vejo a mensagem "* Informe o SEI *"
    E o cursor volta ao campo do número SEI
    E nada é feito

  Cenário: Número SEI que não existe
    Dado que informo um número SEI que não está em nenhuma nota fiscal
    Quando confirmo
    Então vejo a mensagem "* SEI nao cadastrado *"
    E o cursor volta ao campo do número SEI
    E nada é feito

  Cenário: Processo de outra CRE
    Dado que a nota fiscal do processo é de uma CRE diferente da do meu vínculo
    Quando confirmo
    Então vejo a mensagem "<- Usuario sem acesso a este grupo *" com a CRE do processo
    E o cursor volta ao campo do número SEI
    E nada é feito

  Cenário: Pré-liquidar um processo que está em pagamento
    Dado que o registro do processo traz a marca da tela de pagamento
    Quando confirmo a inclusão
    Então vejo a mensagem "* Processo em mais de 1 empenho *"
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Anular a pré-liquidação de um processo que está em pagamento
    Dado que o registro do processo traz a marca da tela de pagamento
    E a situação do processo não é a de pré-liquidado
    Quando confirmo a exclusão com a justificativa
    Então vejo a mensagem "* Processo nao esta pre-liquidado *"
    E nada é gravado

  Cenário: Empenho não informado
    Dado um processo que passou pelas conferências do número SEI
    Quando confirmo a inclusão sem o número do empenho
    Então vejo a mensagem "* Informe o numero do empenho *"
    E o cursor volta ao campo do empenho
    E nada é gravado

  Cenário: Ano do exercício não informado
    Dado um processo que passou pelas conferências do número SEI
    Quando confirmo a inclusão sem o ano do exercício
    Então vejo a mensagem "* Informe o ano do exercicio *"
    E o cursor volta ao campo do ano
    E nada é gravado

  Cenário: Empenho, fornecedor ou tipo de contrato não cadastrado
    Dado que a combinação de empenho, fornecedor e tipo de contrato não está cadastrada
    Quando confirmo a inclusão
    Então vejo a mensagem "* Cad. Empenho/Fornecedor/TC na tela P535T *"
    E o cursor volta ao campo do empenho
    E nada é gravado

  Cenário: Processo sem nota fiscal
    Dado que o processo não tem nenhuma nota fiscal
    Quando confirmo a inclusão
    Então vejo a mensagem "* Processo nao cadastrado *"
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Soma dos gêneros diferente do total das notas fiscais
    Dado que os gêneros do processo somam um valor diferente do total das notas fiscais
    Quando confirmo a inclusão
    Então vejo a mensagem "* Valor dos generos difere do total do processo *"
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Processo já pré-liquidado
    Dado que o processo já tem registro naquele empenho e exercício com a situação de pré-liquidado
    Quando confirmo a inclusão
    Então vejo a mensagem "* Processo ja esta pre-liquidado *"
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Processo já liquidado
    Dado que o registro do processo naquele empenho e exercício tem a situação de liquidado
    Quando confirmo a inclusão
    Então vejo a mensagem "* Processo ja esta liquidado *"
    E nada é gravado

  Cenário: Processo já pago
    Dado que o registro do processo naquele empenho e exercício tem a situação de pago
    Quando confirmo a inclusão
    Então vejo a mensagem "* Processo ja esta pago *"
    E nada é gravado

  Cenário: Processo já em transmissão ao SIAFIC
    Dado que a pré-liquidação do processo já foi transmitida e ainda não voltou
    Quando confirmo a inclusão
    Então vejo a mensagem "* Processo ja em transmissao ao SIAFIC *"
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Pré-liquidação transmitida em outro empenho
    Dado que a transmissão da pré-liquidação do processo é de outro empenho
    Quando confirmo a inclusão
    Então vejo a mensagem "<- Proc em transmissao em outro empenho *" com o empenho da transmissão
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Anulação transmitida em outro empenho, na inclusão
    Dado que a transmissão da anulação do processo é de outro empenho
    Quando confirmo a inclusão
    Então vejo a mensagem "<- Aguarde. Proc sendo anulado em outro emp *" com o empenho da transmissão
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Processo marcado como em mais de um empenho, na inclusão
    Dado que o registro do processo traz a marca de processo em mais de um empenho
    Quando confirmo a inclusão
    Então vejo a mensagem "* Processo em mais de 1 empenho *"
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Processo cadastrado em outro empenho, na inclusão
    Dado que o registro do processo está em outro empenho
    Quando confirmo a inclusão
    Então vejo a mensagem "<- Processo em outro empenho *" com o empenho do registro
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: O retorno anterior do SIAFIC é apagado antes de reenviar
    Dado que a transmissão do processo já tem o retorno do SIAFIC preenchido
    Quando confirmo a inclusão
    Então a resposta do SIAFIC e o registro da transmissão são apagados
    E a tela segue para a transmissão da pré-liquidação

  Cenário: Processo em transmissão, sem retorno
    Dado que existe transmissão do processo ao SIAFIC sem retorno
    Quando confirmo a inclusão
    Então vejo a mensagem "* Processo em transmissao *"
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: A anulação ainda não aceita é desfeita e a inclusão segue
    Dado que existe uma anulação deste processo, neste empenho e exercício, ainda não aceita
    Quando confirmo a inclusão
    Então o registro dessa anulação é apagado
    E a tela segue para a transmissão da pré-liquidação

  Cenário: Tipo de órgão excluído no cadastro
    Dado que o registro do meu tipo de órgão está marcado como excluído
    Quando confirmo a operação
    Então a operação é abandonada com a mensagem de recusa do sistema
    E nada é gravado

  Cenário: Inclusão de um processo que passa por todas as conferências
    Dado que existe um número SEI para o processo
    E as notas fiscais do processo somam o mesmo que os seus gêneros
    E o empenho, o fornecedor e o tipo de contrato estão cadastrados
    E o processo ainda não está pré-liquidado nem em transmissão
    Quando informo o número SEI, o empenho e o ano do exercício e confirmo a inclusão
    Então vejo a data do processo, o empenho, o ano de referência e o número interno do processo
    E vejo o fornecedor com a razão social e o CNPJ, o órgão financeiro e os valores
    E vejo a mensagem "* Transmita para autorizar a pre-liquidacao *"
    E nada foi gravado ainda
    Quando transmito de novo os mesmos dados
    Então a pré-liquidação fica registrada no cadastro de transmissão ao SIAFIC
    E o registro fica marcado com a minha matrícula, a data e a hora
    E vejo a mensagem "* Pre-Liquidacao enviada ao SIAFIC *"

  Cenário: Transmitir de novo a mesma pré-liquidação não duplica
    Dado que a pré-liquidação deste processo, empenho e exercício já está registrada
    Quando confirmo a inclusão e transmito de novo os mesmos dados
    Então nada é gravado de novo
    E não vejo a mensagem de envio ao SIAFIC

  Cenário: Dados diferentes no segundo comando invalidam a confirmação
    Dado que a tela já mostrou o que vai transmitir e pediu o segundo comando
    Quando transmito de novo com o número do processo trocado
    Então a tela refaz as conferências do começo
    E nada foi gravado ainda

  Cenário: Exclusão de uma pré-liquidação já aceita
    Dado que o processo está pré-liquidado naquele empenho e exercício
    E a pré-liquidação já foi aceita, sem transmissão em curso desse processo
    Quando informo a exclusão, o número SEI, o empenho, o ano e a justificativa da anulação
    Então vejo a ordem de anulação e a mensagem "* Transmita para autorizar a anulacao *"
    E nada foi gravado ainda
    Quando transmito de novo os mesmos dados
    Então a anulação fica registrada no cadastro de transmissão ao SIAFIC
    E vejo a mensagem "* Anulacao enviada ao SIAFIC *"

  Cenário: Anulação sem justificativa
    Dado um processo pré-liquidado pronto para ser anulado
    Quando confirmo a exclusão sem a justificativa
    Então vejo a mensagem "* Informe a justificativa da anulacao *"
    E o cursor volta ao campo da justificativa
    E nada é gravado

  Cenário: Anulação de processo que não está pré-liquidado
    Dado que não há registro do processo naquele empenho e exercício
    Quando confirmo a exclusão com a justificativa
    Então vejo a mensagem "* Processo nao esta pre-liquidado *"
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Anulação de processo já liquidado
    Dado que o registro do processo tem a situação de liquidado
    Quando confirmo a exclusão com a justificativa
    Então vejo a mensagem "* Processo ja esta liquidado *"
    E nada é gravado

  Cenário: Anulação de processo já pago
    Dado que o registro do processo tem a situação de pago
    Quando confirmo a exclusão com a justificativa
    Então vejo a mensagem "* Processo ja esta pago *"
    E nada é gravado

  Cenário: Anulação de processo cadastrado em outro empenho
    Dado que o registro do processo está em outro empenho
    Quando confirmo a exclusão com a justificativa
    Então vejo a mensagem "<- Processo em outro empenho *" com o empenho do registro
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Anulação de processo marcado como em mais de um empenho
    Dado que o registro do processo traz a marca de processo em mais de um empenho
    Quando confirmo a exclusão com a justificativa
    Então vejo a mensagem "* Processo em mais de 1 empenho *"
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Anulação já transmitida em outro empenho
    Dado que a transmissão da anulação do processo é de outro empenho
    Quando confirmo a exclusão com a justificativa
    Então vejo a mensagem "<- Proc em anulacao em outro empenho *" com o empenho da transmissão
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Pré-liquidação em transmissão em outro empenho, na exclusão
    Dado que a pré-liquidação do processo está transmitida em outro empenho
    Quando confirmo a exclusão com a justificativa
    Então vejo a mensagem "<- Proc em transmissao em outro emp *" com o empenho da transmissão
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: Anulação já transmitida
    Dado que a anulação deste processo já foi transmitida e ainda não voltou
    Quando confirmo a exclusão com a justificativa
    Então vejo a mensagem "* Anulacao em transmissao ao SIAFIC *"
    E o cursor volta ao campo do número SEI
    E nada é gravado

  Cenário: A exclusão desfaz uma pré-liquidação que ainda não foi aceita
    Dado que a pré-liquidação do processo está transmitida e ainda não voltou
    Quando confirmo a exclusão com a justificativa
    Então o registro dessa transmissão é apagado
    E vejo a mensagem "* Pre-liquidacao Anulada *"
    E a tela volta à inclusão
    E o processo volta a poder ser pré-liquidado

  Cenário: A justificativa é gravada sem acentos
    Dado que escrevo a justificativa da anulação com acentos
    Quando confirmo a anulação e transmito de novo os mesmos dados
    Então a justificativa que fica registrada traz as letras sem acento, no lugar das acentuadas
    E os caracteres não previstos são descartados

  Cenário: Consulta de um processo pré-liquidado
    Dado que o processo existe naquele empenho e exercício
    E o registro do processo traz a marca da tela de pagamento
    Quando informo o número SEI, o empenho e o ano e confirmo a consulta
    Então vejo a data do processo, o empenho, o ano, o órgão financeiro e os valores
    E vejo a razão social do fornecedor
    E vejo o rótulo "Ordem de pre-liquida :" com a ordem de pré-liquidação

  Cenário: Consulta de um processo liquidado
    Dado que o processo existe naquele empenho e exercício com a situação de liquidado
    E o registro do processo traz a marca da tela de pagamento
    Quando confirmo a consulta
    Então vejo o rótulo "Ordem de liquidacao  :" com a ordem de pagamento

  Cenário: Consulta de um processo pago
    Dado que o processo existe naquele empenho e exercício com a situação de pago
    E o registro do processo traz a marca da tela de pagamento
    Quando confirmo a consulta
    Então vejo o rótulo "Ordem de pagamento   :" com a ordem de pagamento

  Cenário: Consulta de processo que não está cadastrado
    Dado que não existe registro do processo naquele empenho e exercício
    Quando confirmo a consulta
    Então vejo a mensagem "* Processo nao cadastrado ou fechado *"
    E o cursor volta ao campo do número SEI
    E nada é mostrado

  Cenário: Consulta de processo que não está em pagamento
    Dado que o registro do processo existe, mas não traz a marca da tela de pagamento
    Quando confirmo a consulta
    Então vejo a mensagem "* Pagamento em mais de um empenho *"
    E o cursor volta ao campo do número SEI
    E os dados do processo não aparecem

  Cenário: A consulta não grava nada
    Dado que o processo existe naquele empenho e exercício
    E o registro do processo traz a marca da tela de pagamento
    Quando consulto o processo
    Então nenhum cadastro é incluído, alterado ou excluído
    E nada é enviado ao SIAFIC

  Cenário: Depois de incluir, a tela reabre limpa
    Dado que a pré-liquidação foi enviada ao SIAFIC
    Então a tela reabre a si mesma com o número do processo e o número SEI limpos
    E o número do processo fica com a secretaria da sessão na primeira parte
    E eu posso pré-liquidar o próximo processo

  Cenário: Depois de anular, a tela reabre limpa
    Dado que a anulação foi enviada ao SIAFIC
    Então a tela reabre a si mesma com o número do processo e o número SEI limpos
    E a operação continua a de exclusão
```
