# US — E023T — Manter o pedido de alimentação escolar de um órgão

## Estória

Como **servidor de CRE**, quero **montar o pedido de alimentação escolar de um
órgão, gênero por gênero, com as quantidades de cada dia de entrega, e
aprová-lo**, para que **o pedido valha para a entrega e o fornecedor só tenha
comprometida, na permissão que a secretaria lhe deu, a quantidade que este
pedido lançou**.

O pedido nasce nesta tela. É aqui que cada gênero entra com a quantidade de cada
um dos cinco dias de entrega, que o sistema confere se ele cabe na permissão
daquele fornecedor para aquela escola, aquele contrato e aquele período, e que o
pedido é dado por aprovado. Sem essa aprovação o pedido não vale para a entrega,
não pode ser estornado nem excluído depois, e o relatório dele não sai; e é a
quantidade lançada aqui que fica comprometida na permissão, de modo que um erro
de digitação não fica só na tela — ele mexe no que o fornecedor pode entregar.

## Contexto

Jornada S000M → E000M → E010M → E023T (4 passos).

Ator: servidor de CRE — informa o órgão, a coordenadoria regional escolar, o
número do pedido e o ano da entrega, lê o fornecedor, o operador e o período de
entrega que o pedido já tem, monta os gêneros com as quantidades de cada dia,
aprova o pedido ou pede o relatório dele.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

A tela desta jornada não é aberta por menu: quem a abre é a **E010M**, passando
adiante a operação em que ela mesma está. Por isso a operação com que a E023T
abre — e, com ela, a possibilidade de gravar — depende de quem a chamou, e isso
é regra desta tela (RN-02 e RN-03). A E023T não encadeia em outra tela: ela
termina nela mesma.

Da sessão a tela usa a matrícula, o código de acesso, a estação, a secretaria (o
tipo de órgão), a coordenadoria regional escolar e o órgão filho do vínculo,
além da descrição do órgão e da data do sistema para o cabeçalho.

As regras abaixo são só as da tela desta jornada. O que encontrei que pertence à
entrada está no **anexo de evidências**, na seção
`## Regras que se revelaram da entrada` — o documento de negócio termina nos
cenários.

---

## Regras de negócio

### RN-01 — A tela mantém o pedido: o cabeçalho e até cinco gêneros com as quantidades do período

A tela é a manutenção do pedido de alimentação escolar de um órgão. No cabeçalho
ela mostra o órgão filho, a coordenadoria regional escolar, o número do pedido,
o ano da entrega, o fornecedor com a razão social, o operador com o nome, o
período de entrega (dia, mês e ano do início e do limite), o tipo de contrato do
pedido e a quantidade de vias do relatório, além da descrição do órgão e da data
do sistema.

Abaixo, em **até cinco linhas**, cada linha traz o código da subclasse, o código
do gênero, a descrição do gênero, as **quantidades de cada um dos cinco dias de
entrega**, o tipo de contrato, a situação da linha e a crítica do gênero. A
quantidade é informada com duas casas decimais separadas por vírgula, e a tela
repete ao lado das quantidades as datas dos cinco dias de entrega do pedido.

### RN-02 — A tela só aceita a consulta e a alteração, e a consulta não grava

A operação só pode ser a de **consulta** ou a de **alteração**. Qualquer outra
coisa — inclusive o campo em branco — é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da
operação e nada é lido nem gravado.

Na consulta a tela não inclui, não altera e não exclui gênero, não aprova o
pedido e não emite o relatório: só mostra o que existe. A limpeza e as exclusões
de RN-08 são a exceção e valem nas duas operações.

[?] A recusa manda usar ALT e CON, mas a tela compara o campo com o código
interno da consulta e o da alteração — os mesmos códigos que ela repõe e usa em
todo o resto da tela, e não os rótulos da mensagem. Nada no acervo mostra o
terminal traduzindo "ALT" e "CON" antes de enviar, nem a tela aceitando esses
rótulos. Pergunta ao site.

### RN-03 — O modo da tela vem de quem a chamou: a E010M decide entre consultar e alterar

Esta tela não é aberta por menu; quem a abre é a **E010M**, e ela entra com a
operação em que a E010M estava. Quando a E010M abre por consulta, a E023T abre
por consulta: o pedido é mostrado e nenhuma linha é operada, mesmo que o
servidor informe situações nas linhas, e não há como trocar para alteração
dentro da tela. Quando a E010M abre por alteração e traz um pedido, a E023T abre
pronta para operar as linhas. Quando não há tela de origem identificada, a tela
só propõe o órgão e a coordenadoria do vínculo do servidor e não carrega pedido
nenhum.

A tela também **não passa nada adiante**: ela não encadeia em outra tela.

### RN-04 — O órgão é obrigatório e depende do vínculo do servidor

O órgão é obrigatório: sem órgão nem coordenadoria informados, a recusa é
**\* Informe o orgao \***, com o cursor no órgão. Quando o vínculo do servidor
carrega um órgão filho, o órgão informado tem de ser esse — outro é recusado com
**\* Usuario sem acesso a outro orgao \***. Quando o vínculo carrega uma
coordenadoria regional escolar, o cadastro do órgão informado tem de ser daquela
coordenadoria, senão a recusa é
**\* Usuario sem acesso ao grupo deste orgao \***.

Em todas elas o cursor volta ao órgão e nada é gravado. Passando por elas, a
coordenadoria que a tela usa daí em diante é a **do cadastro do órgão**, e não a
que o servidor digitou.

### RN-05 — O órgão tem de estar cadastrado, completo e ser da secretaria da sessão

O órgão tem de existir no cadastro e não estar excluído — senão
**\* Orgao nao cadastrado \***. O cadastro tem de estar completo: bairro, órgão
pai, nome, endereço, número de matrículas e número de pessoas — faltando
qualquer um deles, a recusa é
**\* Orgao cadastrado com dados incompletos \***. E o órgão tem de ser do tipo de
órgão da sessão, senão **\* Orgao nao pertence a esta secretaria \***.

Em todas o cursor volta ao órgão e nada é gravado.

### RN-06 — O pedido é identificado pela secretaria, pela coordenadoria, pelo número e pelo ano da entrega

O número do pedido (6 dígitos) e o ano da entrega (4 dígitos) formam juntos o
número de **10 dígitos** que identifica o pedido. Com os dois zerados a recusa é
**\* Informe numero do pedido \***, com o cursor no número. A procura é feita
pelo tipo de órgão da sessão, pela coordenadoria do órgão e por esse número; não
achando, a recusa é **\* Pedido nao cadastrado \***, com o cursor no número. O
órgão não faz parte da identificação do pedido: ele serve para chegar à
coordenadoria. Quando o vínculo carrega um órgão filho e o pedido é de outro
órgão, a recusa é **\* Usuario sem acesso a este orgao \***.

[?] O ano da entrega sozinho já faz a tela procurar o pedido e responder "não
cadastrado"; a recusa de campo em branco só aparece com o número **e** o ano
zerados. Se o site espera a mensagem sempre que faltar o número, é pergunta ao
site.

### RN-07 — O estado e o acúmulo do pedido limitam o que a tela deixa fazer

Encontrado o pedido, a tela o recusa quando ele está excluído
(**\* Pedido excluido \***), quando é um pedido acumulado
(**\* Pedido acumulado \***), quando está pendente de distribuição
(**\* Pedido pendente de distribuicao \***), quando está fechado e a operação é
a de alteração (**\* Pedido fechado nao pode ser alterado \***), quando não tem
nenhum gênero (**\* Pedido sem generos cadastrados \***) e quando os gêneros
dele são de outro tipo de contrato
(**\* Pedido com outro tipo de contrato \***). Em todas o cursor fica no número
do pedido e nada é gravado.

Um pedido fechado ainda pode ser consultado; a consulta o mostra com o aviso
**\* Pedido fechado \***.

### RN-08 — Abrir o pedido apaga o que já estava marcado, e apaga o pedido que fica sem gênero

Percorrer o pedido não é inofensivo. Ao montar a lista, a tela **apaga do
cadastro** as linhas de gênero que já estavam marcadas como excluídas e as que
ficaram com quantidade pedida zero e sem marca de acumulado. O mesmo laço de
limpeza roda na passagem de alteração.

E quando o pedido não tem **nenhuma** linha de gênero viva, a tela **apaga o
próprio pedido** e avisa **\* Pedido excluido \***. Isso acontece em três
situações: pedindo o relatório de um pedido sem gêneros, trabalhando um pedido
sem gêneros (inclusive numa simples consulta) e quando o pedido fica sem gênero
vivo depois de uma recusa.

[?] A conferência que decide se o pedido tem gêneros procura a primeira linha do
pedido informando a subclasse e o gênero zerados; o acervo não documenta essa
leitura parcial. Se ela não achar a primeira linha, todo pedido consultado é
apagado. Pergunta ao site.

### RN-09 — A situação de cada linha diz o que fazer com ela

Em cada linha, a **situação** decide a operação: **I** inclui, **A** altera,
**E** exclui. Linha sem gênero informado, ou com situação diferente de I, A e E,
não gera operação nenhuma. Cada operação passa pela segurança da tela com o
código da operação correspondente — inclusão, alteração ou exclusão — e, não
estando autorizada para este servidor, é recusada e a tela é abandonada sem
gravar.

### RN-10 — Inclusão de gênero: o que a tela exige

Para incluir, o gênero tem de estar cadastrado — senão
**\* Genero nao cadastrado \*** — e não pode já estar no pedido — senão
**\* Genero ja cadastrado neste pedido \***. A quantidade total do gênero é
obrigatória (**\* Informe quantidade \***), cada quantidade informada tem de
cair em um dia de entrega que o pedido tenha
(**\* Inf. quantidade para dias de entrega validos \***), a quantidade tem de
respeitar o fracionamento do gênero
(**\* Quant. fracionada invalida para este genero \***) e, num pedido já
aprovado, o tipo de contrato é obrigatório
(**\* Informe o tipo de contrato \***).

O tipo de contrato informado tem de ser o mesmo dos gêneros que o pedido já tem
— senão **\* Pedido com outro tipo de contrato \***. Nas recusas o cursor volta
à linha recusada e nada é gravado.

### RN-11 — O gênero só entra com permissão do fornecedor, e dentro dela

A quantidade pedida é conferida contra a **permissão do fornecedor** para aquele
tipo de contrato, aquela coordenadoria, aquele fornecedor, aquela subclasse e
aquele gênero, no limite de entrega do pedido. Não havendo permissão, a recusa é
**\* Genero sem permissao \***. Se o grupamento do gênero for diferente do
grupamento da permissão, a recusa é
**\<- Genero de outro grupamento \***. E a quantidade já pedida mais a que se
está pedindo não pode passar do total permitido — senão
**\* Quantidade insuficiente na permissao \***.

Confirmada a inclusão, a quantidade comprometida da permissão passa a ser a que
estava mais a nova; na alteração ela é trocada pela nova quantidade da linha; e
na exclusão ela é diminuída pela quantidade da linha.

[?] Quando o pedido ainda não está aprovado e o servidor informa o tipo de
contrato, a tela recalcula a crítica de **todos** os gêneros do pedido e, nessa
passagem, soma de novo a quantidade de cada linha à quantidade comprometida da
permissão — a mesma quantidade já comprometida quando a linha foi incluída, sem
desconto. Se a quantidade comprometida fica inflada a cada alteração, é pergunta
ao site.

### RN-12 — A crítica que fica gravada na linha

A tela grava em cada linha de gênero uma **crítica** dizendo como ele ficou
diante da permissão, e a mostra na lista: sem permissão; quantidade insuficiente
na permissão; quantidade permitida totalmente consumida; e o **percentual
consumido** da quantidade permitida, quando o comprometido passou de 70% do
permitido sem consumi-lo todo.

### RN-13 — A quantidade calculada limita o que se pede

Quando o pedido não é do tipo que dispensa o cálculo, a quantidade pedida de
cada gênero é conferida contra a quantidade calculada para aquele pedido e
aquele gênero. Não havendo cálculo, a recusa é
**\* Genero nao calculado para este pedido \***; e a quantidade pedida não pode
passar da calculada — senão **\<- Quantidade maior que a calculada \***.

### RN-14 — Contrato de cooperativa só se atende pelo órgão acumulador da coordenadoria

O tipo de contrato informado tem de estar cadastrado para a secretaria — senão
**\* Tipo de contrato nao cadastrado \***. O cadastro do tipo de contrato diz se
ele é de cooperativa, e isso muda o órgão que pode receber o pedido: o contrato
de cooperativa só vale para o órgão do pedido que a coordenadoria marca como
acumulador, e um contrato que não é de cooperativa não vale para esse órgão.
Fora disso as recusas são
**\* Nao use SICI CRE. Contrato nao Cooperativa \*** e
**\<- Use SICI CRE. Contrato Cooperativa \***.

[?] O que é, no negócio, o órgão que a coordenadoria marca como acumulador — e
se o SICI CRE é esse órgão — não se conclui do acervo. Pergunta ao site.

### RN-15 — Alteração de um gênero do pedido

Para alterar, o gênero tem de estar no pedido e não estar excluído — senão
**\* Genero nao cadastrado neste pedido \***. A linha não pode ser de um pedido
acumulado (**\<- Genero acumulado neste pedido \***), não pode estar fechada
(**\* Quantidade fechada para este genero \***) e o tipo de contrato da linha
não pode ser trocado (**\* Nao altere o tipo de contrato \***). O tipo de
contrato informado também tem de ser o mesmo dos gêneros do pedido
(**\* Pedido com outro tipo de contrato \***).

As quantidades passam pelas mesmas conferências da inclusão (quantidade
obrigatória, dias de entrega válidos e fracionamento) e a quantidade pedida não
pode ser menor do que a quantidade já recebida somada à estornada — senão
**\* Qt recebida + estornada maior que pedida \***. Nas recusas nada é gravado.

[?] A conferência do fracionamento por dia de entrega decide com o resto da
divisão que a passagem anterior deixou: o resto só é calculado no fim da
passagem, depois dessas conferências, e a divisão não protege o resto quando o
fracionamento do gênero é zero. Na primeira linha da transação o resto é zero e
essa recusa não aparece. Pergunta ao site.

### RN-16 — Exclusão de um gênero do pedido: o que a tela exige e o que ela faz

Para excluir, o gênero tem de estar no pedido e não estar excluído — senão
**\* Genero nao cadastrado neste pedido \***. A linha não pode ser de um pedido
acumulado (**\<- Genero acumulado neste pedido \***), não pode estar fechada
(**\* Quantidade fechada para este genero \***), não pode ter quantidade
estornada (**\* Genero ja tem quantidade estornada \***) nem recebida
(**\* Genero ja tem quantidade recebida \***), e a quantidade da linha tem de
respeitar o fracionamento do gênero
(**\* Quantidade fracionada invalida \***).

Passando por tudo, a quantidade da linha é liberada da permissão do fornecedor e
a linha sai do pedido de duas formas, conforme o pedido já esteja aprovado ou
não: num pedido **aprovado** a linha apenas fica **marcada como excluída**, e
num pedido **não aprovado** ela é **apagada** do cadastro. As duas formas deixam
registro na auditoria.

### RN-17 — Aprovação do pedido

Marcada a aprovação e estando o pedido pendente de aprovação, a tela aprova: dá
por aprovados todos os gêneros vivos, apaga as linhas que estavam marcadas como
excluídas e grava no pedido a situação **APROVADO**, com a matrícula de quem
aprovou e a data. Um pedido que não está pendente de aprovação é recusado com
**\* Pedido nao esta pendente de aprovacao \***, e um pedido com gênero sem tipo
de contrato não é aprovado —
**\* Generos sem tipo de contrato. Nao aprovado. \***. A lista mostra a situação
do pedido, APROVADO ou FECHADO.

[?] Quem marca a aprovação não se conclui da tela: o campo é de entrada e saída,
a abertura o repõe em "N" e nenhuma linha do programa escreve "S" nele. Se a
máscara não oferece a marca, o pedido nunca é aprovado nem fechado por esta
tela — e, sem aprovação, não pode ser estornado nem excluído depois. Pergunta ao
site.

[?] A tela refaz a situação do pedido a partir dos gêneros — e é aí que o pedido
vira FECHADO quando todos os gêneros estão fechados — só na passagem que roda
depois de alguma recusa. Quando a transação termina sem recusa, a situação não é
refeita. Se o site espera o pedido fechar ao confirmar a última linha, é pergunta
ao site.

### RN-18 — Emissão do relatório do pedido

Informado o código de impressão, a tela emite o relatório do pedido. Antes disso
ela confere que não há um relatório daquele tipo em processamento para a
coordenadoria (**\* Relatorio em processamento. Aguarde. \***), que o pedido
está cadastrado (**\* Pedido nao cadastrado \***), não está excluído
(**\* Pedido excluido \***), não está pendente de distribuição
(**\* Pedido pendente de distribuicao \***) e está aprovado
(**\* Pedido nao aprovado \***). A quantidade de vias é obrigatória e vai até
três (**\* Informe a quantidade de vias do relatorio \*** e
**\* Maximo de 3 vias por relatorio \***).

Passando por tudo, a tela monta a requisição de impressão com o órgão, a
coordenadoria, o fornecedor, o período de entrega, o número de vias, a estação e
a matrícula de quem pediu.

### RN-19 — Toda operação fica registrada na auditoria

Cada gravação ou exclusão de gênero, de pedido e de permissão inclui um registro
de auditoria com a operação (inclusão, alteração ou exclusão), o cadastro
atingido, a tela de origem, o número do processo, a coordenadoria, a secretaria,
a matrícula do servidor, a estação, a data e a hora da sessão e o conteúdo do
registro antes e depois da alteração. Nenhum outro cadastro é tocado pela tela.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter o pedido de alimentação escolar de um órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E023T

  Cenário: A tela mostra o pedido e até cinco gêneros
    Dado que existe um pedido de alimentação escolar do meu órgão
    Quando abro a tela pela E010M e informo o número do pedido e o ano da entrega
    Então vejo o órgão, a coordenadoria, o fornecedor com a razão social, o operador
      com o nome, o período de entrega, o tipo de contrato do pedido e as vias
    E vejo até cinco gêneros, cada um com a subclasse, o gênero, a descrição, as
      quantidades dos cinco dias de entrega, o tipo de contrato, a situação e a crítica

  Cenário: Operação não disponível
    Quando a tela recebe uma operação que não é a de consulta nem a de alteração
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo da operação
    E nada é lido e nada é gravado

  Cenário: A consulta não altera o pedido
    Dado que estou na tela E023T em modo de consulta
    Quando confirmo o pedido
    Então o pedido é mostrado
    E nenhum gênero é incluído, alterado ou excluído
    E o pedido não é aprovado nem impresso

  Cenário: O modo da tela vem de quem a chamou
    Dado que a E010M me abriu a E023T por consulta
    Quando tento incluir, alterar ou excluir um gênero
    Então nenhuma linha é operada
    E para gravar eu preciso que a E010M abra a E023T por alteração

  Cenário: A tela não encadeia em outra tela
    Dado que terminei de trabalhar o pedido
    Quando confirmo
    Então a tela não abre nenhuma outra tela

  Cenário: O órgão é obrigatório e depende do vínculo
    Dado que o meu vínculo carrega um órgão filho e uma coordenadoria
    Quando informo outro órgão, ou deixo o órgão em branco
    Então vejo "* Usuario sem acesso a outro orgao *" ou "* Informe o orgao *"
    E o cursor fica no órgão
    E nada é gravado

  Cenário: Órgão fora do cadastro da coordenadoria do vínculo
    Dado que o meu vínculo carrega uma coordenadoria
    Quando informo um órgão que não é daquela coordenadoria
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no órgão
    E nada é gravado

  Cenário: Órgão não cadastrado, incompleto ou de outra secretaria
    Quando informo um órgão que não existe, ou cujo cadastro está incompleto, ou que
      não é do tipo de órgão da minha sessão
    Então vejo "* Orgao nao cadastrado *", "* Orgao cadastrado com dados incompletos *"
      ou "* Orgao nao pertence a esta secretaria *"
    E o cursor fica no órgão
    E nada é gravado

  Cenário: Pedido não informado ou não cadastrado
    Quando deixo o número do pedido e o ano da entrega zerados, ou informo um pedido
      que não existe
    Então vejo "* Informe numero do pedido *" ou "* Pedido nao cadastrado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo um pedido que é de outro órgão
    Então vejo "* Usuario sem acesso a este orgao *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Estados do pedido que a tela recusa
    Quando o pedido está excluído, acumulado, pendente de distribuição, fechado numa
      alteração, sem gêneros, ou tem gêneros de outro tipo de contrato
    Então vejo "* Pedido excluido *", "* Pedido acumulado *",
      "* Pedido pendente de distribuicao *", "* Pedido fechado nao pode ser alterado *",
      "* Pedido sem generos cadastrados *" ou "* Pedido com outro tipo de contrato *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido fechado ainda é consultado
    Dado que o pedido está fechado
    Quando o abro em modo de consulta
    Então o pedido é mostrado com o aviso "* Pedido fechado *"

  Cenário: Pedido sem gênero é apagado
    Dado que existe um pedido do meu órgão sem nenhuma linha de gênero viva
    Quando abro esse pedido, mesmo só para consultar
    Então vejo "* Pedido excluido *"
    E o pedido deixa de existir no cadastro

  Cenário: Linhas marcadas ou zeradas são apagadas ao abrir o pedido
    Dado que o pedido tem linhas de gênero marcadas como excluídas, ou com quantidade
      zero e sem acumulado
    Quando abro o pedido
    Então essas linhas são apagadas do cadastro

  Cenário: Linha sem gênero ou com situação desconhecida é ignorada
    Dado que preenchi uma linha sem o código do gênero, ou com situação diferente de
      I, A e E
    Quando a tela processa as linhas
    Então aquela linha não gera operação nenhuma

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu código de acesso não tem a operação pretendida para esta tela
    Quando tento incluir, alterar ou excluir um gênero
    Então o sistema recusa a operação
    E nada é gravado

  Cenário: Inclusão de um gênero no pedido
    Dado que o gênero está cadastrado e ainda não está no pedido
    E que o pedido é aprovado e o tipo de contrato informado é o dele
    Quando informo a situação I, o gênero, o tipo de contrato e as quantidades de cada
      dia de entrega
    Então a quantidade comprometida da permissão do fornecedor passa a ser a que estava
      mais a pedida
    E o gênero entra no pedido

  Cenário: Inclusão recusada pelas conferências do gênero
    Quando tento incluir um gênero não cadastrado, ou um gênero que já está no pedido,
      ou sem quantidade, ou com quantidade em dia de entrega que o pedido não tem, ou
      com quantidade fora do fracionamento do gênero, ou sem tipo de contrato num
      pedido aprovado, ou com tipo de contrato diferente do pedido
    Então vejo "* Genero nao cadastrado *", "* Genero ja cadastrado neste pedido *",
      "* Informe quantidade *", "* Inf. quantidade para dias de entrega validos *",
      "* Quant. fracionada invalida para este genero *",
      "* Informe o tipo de contrato *" ou "* Pedido com outro tipo de contrato *"
    E o cursor fica na linha recusada
    E nada é gravado

  Cenário: Inclusão sem permissão do fornecedor
    Dado que não há permissão para o gênero naquele fornecedor, contrato e limite de
      entrega, ou que o pedido já comprometeu tudo o que a permissão permite, ou que o
      grupamento do gênero é outro
    Quando tento incluir o gênero
    Então vejo "* Genero sem permissao *", "<- Genero de outro grupamento *" ou
      "* Quantidade insuficiente na permissao *"
    E o gênero não entra no pedido
    E nada é gravado

  Cenário: Crítica do gênero diante da permissão
    Dado que a quantidade pedida passa de 70% do que a permissão permite
    Quando o gênero é gravado
    Então a linha mostra a crítica do gênero com o percentual consumido da quantidade
      permitida

  Cenário: Quantidade maior que a calculada
    Dado que o pedido não dispensa o cálculo
    Quando a quantidade pedida passa da quantidade calculada para o gênero, ou não há
      cálculo para ele
    Então vejo "<- Quantidade maior que a calculada *" ou
      "* Genero nao calculado para este pedido *"
    E nada é gravado

  Cenário: Contrato de cooperativa no órgão errado
    Quando informo um contrato de cooperativa para um pedido que não é do órgão
      acumulador da coordenadoria, ou um contrato que não é de cooperativa para esse
      órgão, ou um tipo de contrato que não existe
    Então vejo "* Nao use SICI CRE. Contrato nao Cooperativa *",
      "<- Use SICI CRE. Contrato Cooperativa *" ou
      "* Tipo de contrato nao cadastrado *"
    E nada é gravado

  Cenário: Alteração das quantidades de um gênero
    Dado que o gênero está no pedido, não está acumulado nem fechado, e a nova
      quantidade não é menor que a recebida somada à estornada
    Quando informo a situação A e as novas quantidades
    Então a quantidade comprometida da permissão passa a ser a nova quantidade da linha
    E o gênero é regravado

  Cenário: Alteração recusada
    Quando altero um gênero que não está no pedido, ou um gênero de pedido acumulado,
      ou um gênero já fechado, ou troco o tipo de contrato, ou informo quantidade menor
      que a recebida somada à estornada
    Então vejo "* Genero nao cadastrado neste pedido *",
      "<- Genero acumulado neste pedido *", "* Quantidade fechada para este genero *",
      "* Nao altere o tipo de contrato *" ou
      "* Qt recebida + estornada maior que pedida *"
    E nada é gravado

  Cenário: Exclusão de um gênero de um pedido aprovado
    Dado que o pedido está aprovado e o gênero não tem quantidade recebida nem
      estornada
    Quando informo a situação E
    Então a quantidade da linha é liberada da permissão do fornecedor
    E o gênero fica marcado como excluído no pedido
    E a operação fica registrada na auditoria

  Cenário: Exclusão de um gênero de um pedido ainda não aprovado
    Dado que o pedido não está aprovado
    Quando informo a situação E
    Então a quantidade da linha é liberada da permissão do fornecedor
    E o gênero é apagado do pedido

  Cenário: Exclusão recusada
    Quando excluo um gênero que não está no pedido, ou de pedido acumulado, ou já
      fechado, ou com quantidade estornada, ou com quantidade recebida, ou com
      quantidade fora do fracionamento
    Então vejo "* Genero nao cadastrado neste pedido *",
      "<- Genero acumulado neste pedido *", "* Quantidade fechada para este genero *",
      "* Genero ja tem quantidade estornada *",
      "* Genero ja tem quantidade recebida *" ou
      "* Quantidade fracionada invalida *"
    E o gênero continua no pedido

  Cenário: Aprovação do pedido
    Dado que o pedido está pendente de aprovação e todos os gêneros têm tipo de contrato
    Quando marco a aprovação numa alteração
    Então o pedido fica APROVADO, com a matrícula de quem aprovou e a data
    E todos os gêneros ficam aprovados
    E os gêneros marcados como excluídos são apagados

  Cenário: Aprovação recusada
    Quando marco a aprovação de um pedido que não está pendente de aprovação, ou de um
      pedido com gênero sem tipo de contrato
    Então vejo "* Pedido nao esta pendente de aprovacao *" ou
      "* Generos sem tipo de contrato. Nao aprovado. *"
    E o pedido continua como estava

  Cenário: Emissão do relatório do pedido
    Dado que o pedido está aprovado e não há relatório em processamento para a
      coordenadoria
    Quando informo o código de impressão e a quantidade de vias
    Então a tela monta a requisição de impressão do pedido com o órgão, a
      coordenadoria, o fornecedor, o período e as vias informadas

  Cenário: Emissão recusada
    Quando peço o relatório de um pedido não cadastrado, excluído, pendente de
      distribuição ou não aprovado, ou sem a quantidade de vias, ou com mais de três
      vias, ou quando já há um relatório em processamento
    Então vejo "* Pedido nao cadastrado *", "* Pedido excluido *",
      "* Pedido pendente de distribuicao *", "* Pedido nao aprovado *",
      "* Informe a quantidade de vias do relatorio *",
      "* Maximo de 3 vias por relatorio *" ou
      "* Relatorio em processamento. Aguarde. *"
    E nenhuma requisição é montada

  Cenário: Toda operação fica registrada
    Dado que incluí, alterei ou excluí um gênero, ou aprovei o pedido
    Quando a operação é confirmada
    Então fica um registro de auditoria com a operação, o cadastro atingido, a tela, a
      matrícula, a estação, a data e a hora, e o antes e o depois
```
