# US — E120T — Recuperar pedido excluído

## Estória

Como **servidor de CRE**, quero **recuperar um pedido que não está mais na base,
informando o órgão, o grupo, o número do pedido e o ano da entrega, o fornecedor, a
semana e o período de entrega, e confirmando no fim**, para que **o pedido e os itens
dele voltem a existir para a programação da entrega, com o contrato voltando a responder
pela quantidade que tinha sido devolvida ao saldo**.

Um pedido excluído não deixa rastro útil: ele some da base de pedidos, a quantidade que
consumia volta ao saldo do contrato, e nenhuma tela de consulta o encontra mais. Esta
tela é a porta de volta — ela reconstrói o pedido e os itens dele a partir de um pedido
existente que serve de cópia, reconsome a quantidade no contrato e entrega o pedido à
tela de programação de entrega, que só aceita abrir por este caminho. Sem ela, o órgão
teria de emitir um pedido novo, com número novo, e o que já estava acertado com o
fornecedor se perderia.

## Contexto

Jornada S000M → E000M → E010M → E120T.
Ator: servidor de CRE — informa o órgão filho SDI, o grupo, o pedido e o ano, o
fornecedor, a semana e o período de entrega, responde à confirmação e deixa o pedido
pronto para a programação da entrega.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O `E000M` e o `E010M` são menus: não gravam nada e apenas encaminham. Do vínculo do
servidor a tela usa o **órgão filho**, o **grupo** e o **tipo de órgão** (a secretaria);
da sessão, a **matrícula**, o **código de acesso**, o **privilégio** e a **estação**; e
mostra no cabeçalho a **descrição do tipo de órgão** e a **data do sistema**.

Esta tela **não decide nada pelo código da tela que a chamou**: ela mesma repõe a
operação de inclusão ao ser apresentada e nunca compara a origem com código de tela. O
que ela **entrega à seguinte** está na RN-21: ela passa o pedido adiante, sem menu, e é
o modo que ela deixa nessa passagem que decide como a tela de programação abre. No meio
do caminho ela reabre a si mesma, uma vez, para pedir a confirmação (RN-18).

As regras abaixo são só as da tela desta jornada. O que já está na entrada não se repete
aqui; o que se revelou dela ao ler estes fontes está no anexo de evidências.

---

## Regras de negócio

### RN-01 — A tela só inclui: a operação é sempre a inclusão

A tela serve para trazer um pedido de volta, e isso é uma inclusão. Ao ser apresentada,
ela mesma põe **incluir** no campo da operação, e a operação que a tela que a chamou
tenha deixado na passagem é descartada antes de ser olhada. Se a transação voltar com
outra operação, a recusa é **\* Opcao nao disponivel. Use INC \***, com o cursor de
volta ao campo da operação, e nada mais é conferido, mostrado ou gravado.

[?] A recusa manda usar a tecla **INC**, mas o que a tela põe no campo é o mnemônico
interno da inclusão, que não é o mesmo texto. Se o terminal traduz a tecla para esse
mnemônico antes de enviar, a regra é uma só; se não traduz, ou a mensagem engana quem
opera, ou a guarda recusa exatamente o que ela manda fazer. O corpus não traz essa
tradução. Pergunta ao site.

### RN-02 — O que a tela pede, e como o pedido é identificado

A tela se identifica como ORGAO FILHO SDI e tem **vinte campos de negócio**: a operação,
a tela de destino, o órgão filho SDI, o grupo (CORD.REG.ESCOLAR), o número do pedido, o
ano da entrega, o código do fornecedor, o operador logístico, o dia, o mês e o ano de
início do período, o dia, o mês e o ano limite do período, a semana, o tipo de contrato,
a quantidade de dias de entrega, o número e o ano do pedido para cópia, e a resposta da
confirmação. **Dezesseis** deles — todos menos a operação, a tela de destino, a semana e
a resposta — passam pela edição numérica, e o campo em branco é tratado como zero.

O número do pedido **não é a identificação do pedido por si só**: o pedido é procurado
pelo órgão, pelo grupo e pela **chave formada pelo número do pedido junto com o ano da
entrega** — o número na frente, o ano atrás. É essa chave que a tela usa para procurar o
pedido, para procurar o pedido para cópia e para gravar o pedido recuperado.

### RN-03 — Como a tela abre: órgão e grupo do vínculo, nome do órgão e cinco dias

Ao ser aberta, a tela preenche o **órgão filho SDI e o grupo com os do vínculo do
servidor**, e busca no cadastro de órgãos o **nome do órgão** para mostrar ao lado do
código. Quando o vínculo não carrega órgão, a tela abre com o órgão em branco e o cursor
no campo do órgão, e não mostra nome nenhum até que ele seja informado. O campo da
**quantidade de dias de entrega** abre preenchido com **cinco** dias.

### RN-04 — O órgão filho SDI é obrigatório

O órgão filho SDI tem de vir informado. Em branco, a recusa é **\* Informe o orgao \***,
com o cursor de volta ao campo do órgão, e nada é conferido depois disso.

### RN-05 — Quem tem órgão no vínculo não recupera pedido de outro órgão

O órgão informado tem de ser o do vínculo do servidor. Quem tem um órgão no vínculo e
informa outro é recusado com **\* Usuario sem acesso a outro orgao \*** — a mensagem
leva o código do órgão do vínculo —, com o cursor de volta ao campo do órgão. Quem não
tem órgão no vínculo recupera pedido do órgão que informar.

### RN-06 — O órgão tem de estar cadastrado e ser da secretaria do servidor

Do cadastro de órgãos vêm o nome do órgão e o grupo dele. Órgão que não está no cadastro
é recusado com **\* Orgao nao cadastrado \***, com o cursor de volta ao campo do órgão. E
o órgão informado tem de ser de uma **secretaria igual à do servidor** (o tipo de órgão
do vínculo): sendo de outra, a recusa é **\* Orgao nao pertence a esta secretaria \***,
também com o cursor no campo do órgão.

### RN-07 — O grupo tem de ser o do servidor, e o grupo digitado não decide

Quando a sessão traz um grupo, o **grupo do órgão cadastrado** tem de ser igual ao do
servidor. Sendo de outro grupo, a recusa é
**<- Usuario sem acesso ao grupo deste orgao \*** — a mensagem leva o código do grupo —
com o cursor de volta ao campo do órgão. Quando a sessão não traz grupo, esta
conferência não é feita.

[?] O campo do grupo (CORD.REG.ESCOLAR) é mostrado e pode ser digitado, mas não é ele
que a tela confere: a conferência é entre o grupo do cadastro do órgão e o do vínculo, e
o que estava digitado é substituído pelo do cadastro antes de a tela seguir. Quem digita
um grupo diferente é aceito ou recusado conforme o cadastro do órgão, não conforme o que
digitou, e a tela não avisa. Se o campo existe para o servidor escolher alguma coisa,
essa escolha não é atendida. Pergunta ao site.

### RN-08 — O que a tela exige do pedido a recuperar

O pedido a recuperar tem de ser informado: sem número e sem ano, a recusa é
**\* Informe pedido a ser recuperado \***, com o cursor de volta ao campo do número.
Informado, ele **não pode existir** na base de pedidos — existindo, a recusa é
**\* Pedido nao esta excluido \*** — e **não pode estar com o operador logístico**:
existindo na base do operador logístico, a recusa é
**\* Pedido cad para operador logistico \***. Nos dois casos o cursor volta ao campo do
número e nada é gravado.

### RN-09 — O número do pedido tem de caber no que já foi emitido para o ano

A tela procura, no cadastro de pedidos por ano e secretaria, o registro do **ano da
entrega** informado. Não achando esse registro, a recusa é
**\* Numero do pedido invalido \***. Achando, o número informado **não pode ser maior
que o número guardado naquele registro** — que é o último número emitido para aquele ano
e aquela secretaria; sendo maior, a mesma recusa, **\* Numero do pedido invalido \***,
com o cursor de volta ao campo do número.

### RN-10 — O fornecedor tem de estar cadastrado

O código do fornecedor informado é procurado no cadastro de fornecedores, de onde vem a
**razão social** mostrada na tela. Não estando cadastrado, a recusa é
**\* Fornecedor nao cadastrado \***, com o cursor de volta ao campo do código.

### RN-11 — O início da entrega tem de ser uma data válida, em dia de semana e fora dos feriados

O dia, o mês e o ano de **início do período** têm de formar uma data válida; não
formando, a recusa é **\* Data de inicio da entrega invalida \***. O ano tem de estar
entre **1994 e 2099**. A data ainda tem de cair em **dia de semana**: em sábado a recusa
é **\* Inicio da entrega nao deve ser um sabado \***, em domingo,
**\* Inicio da entrega nao deve ser um domingo \***. E não pode ser **feriado** da
secretaria: sendo, a recusa é **\* Inicio da entrega nao deve ser um feriado \***. Em
todas essas recusas o cursor volta ao campo do dia de início.

[?] A tela descobre o dia da semana da data informada por uma rotina comum de data que
**não tem fonte no acervo**. Que ela devolva o dia da semana da data convertida — e não
o dia de hoje — é conclusão do uso, porque a mesma conferência, no laço que calcula os
dias da entrega (RN-13), serve para pular sábados e domingos; mas isso não está escrito
em lugar nenhum. Pergunta ao site.

### RN-12 — A quantidade de dias de entrega vai de um a cinco

A quantidade de dias de entrega é obrigatória e limitada: em branco (zero), a recusa é
**\* Informe a quantidade de dias de entrega \***; acima de **cinco**,
**\* Quantidade maxima de dias de entrega = 5 \***. Nas duas, o cursor volta ao campo da
quantidade. Como a abertura já traz cinco, o valor máximo é também o valor que a tela
oferece.

### RN-13 — O período de entrega tem de caber no ano da entrega; os dias são contados em dias úteis

A partir do início informado, a tela calcula o **limite do período** avançando a
quantidade de dias pedida **em dias úteis** — pulando sábados, domingos e os feriados da
secretaria — e monta as **até cinco datas de entrega** do pedido, uma por dia do
período. O período é aceito só se o **início e o limite caírem no mesmo ano da entrega**
informado: não caindo, a recusa é **\* Periodo de entrega invalido \***, com o cursor no
campo do ano de início, e nada é gravado.

### RN-14 — A semana de entrega é A, B, C, D ou E

A semana informada tem de ser **A, B, C, D ou E**. Qualquer outra coisa — inclusive em
branco — é recusada com **\* Informe semana com A / B / C / D / E \***, com o cursor de
volta ao campo da semana.

### RN-15 — O tipo de contrato é obrigatório e tem de estar cadastrado para o fornecedor

O tipo de contrato é obrigatório: em branco (zero), a recusa é
**\* Informe tipo contrato \***, com o cursor no campo do tipo. Informado, ele tem de
existir no cadastro de contratos para o **fornecedor, a secretaria e o tipo de órgão** em
uso — e o contrato não pode estar excluído. Não existindo, a recusa é
**\* Contrato nao cad para este fornecedor \***, também com o cursor no campo do tipo. Do
contrato a tela aproveita o **operador logístico** (RN-16) e, na gravação, o saldo de
quantidade contratada (RN-19).

### RN-16 — O operador logístico do contrato é mostrado, e a recusa por falta dele não se alcança

Achado o contrato, a tela copia dele o **código do operador logístico** e procura o
**nome** desse operador no cadastro, para mostrar ao lado do código. Se o operador não
estiver nesse cadastro, o nome sai em branco — sem aviso nenhum.

[?] A recusa **\* Fornecedor nao cadastrado \*** existe nesse ponto da tela, mas está
guardada por um sinal que a etapa anterior já deixou marcado como "achado" quando o
contrato existe — e quando o contrato não existe o fluxo já saiu antes, com outra
mensagem. Lendo os rótulos das duas etapas, essa recusa é **inalcançável por esse
caminho**: ou a guarda queria olhar a leitura do operador, ou o sinal deveria ser
reiniciado antes dela. Não escolho um dos dois lados. Pergunta ao site.

### RN-17 — O pedido para cópia, quando informado, tem de existir, ser do mesmo fornecedor e do mesmo contrato

O **pedido para cópia** é o pedido existente de onde saem os itens do pedido recuperado.
Informado, ele tem de existir na base de pedidos daquele órgão e grupo — senão
**\* Pedido para copia nao cadastrado \*** —, tem de ser **do mesmo fornecedor** —
senão **\* Pedido para copia de outro fornecedor \*** — e tem de ter itens com o **mesmo
tipo de contrato** — sem item cadastrado, **\* Pedido para copia nao cadastrado \***; com
item de outro contrato, **\* Pedido para copia de outro contrato \***. Em todas, o cursor
volta ao campo do número do pedido para cópia, e nada é gravado.

### RN-18 — A recuperação é confirmada antes de qualquer gravação

Passando por todas as conferências, a tela **não grava ainda**: ela guarda o que foi
conferido, reabre a si mesma com a pergunta
**\* Confirma recuperacao do pedido <S/N> ? \*** e deixa o cursor no campo da resposta.
Só a resposta **S** — e com os dados da tela **iguais aos que foram conferidos** —
leva a recuperação adiante. Qualquer outra resposta, ou uma resposta **S** com algum dado
alterado desde a conferência, descarta a confirmação, refaz as conferências com o que
estiver na tela e pergunta de novo; nesse vaivém nada é gravado.

[?] Quem responde **N** à pergunta não vê a tela encerrar nem o pedido ser descartado:
ela volta a conferir tudo e faz a mesma pergunta outra vez. Se a intenção era dar uma
saída pela negativa, ela não existe — só se sai respondendo **S** ou saindo da tela.
Pergunta ao site.

### RN-19 — Confirmada, a recuperação grava o pedido, os itens, o consumo do contrato e a auditoria

Confirmada, a tela monta e grava, **numa só passagem**: o **pedido**, com a situação de
**pedido aprovado**; os **itens** do pedido, um por classe, subclasse e gênero copiados do
pedido para cópia, cada um com as **até cinco datas de entrega** calculadas e com a
quantidade acumulada daquela classe; o **consumo do contrato**, somando à quantidade
entregue a quantidade dos itens recuperados; e o registro de **auditoria** de cada
movimento (o pedido, os itens e o contrato), com a operação, o conteúdo anterior e o
posterior, a matrícula, a estação, o número do processo, a data e a hora da sessão e o
tipo de órgão.

Dois cortes decidem quais itens entram: só entram os itens do contrato cujo **período já
começou** até a data de início do pedido, e o contrato só é consumido enquanto a
quantidade recuperada **couber no saldo inicial** do contrato.

[?] O item que não couber nesse saldo é deixado de fora **em silêncio**: a tela não
avisa, não recusa e grava o pedido sem ele — e o pedido recuperado fica com menos itens
do que o pedido para cópia, sem ninguém saber. Se o silêncio é intencional, é pergunta
ao site.

### RN-20 — Sem pedido para cópia a recuperação não grava nada

O pedido para cópia não é exigido em momento nenhum. Quando ele não é informado (número
e ano em branco), a tela **não grava o pedido, nem os itens, nem o consumo do contrato,
nem auditoria**: passa direto para o encaminhamento da RN-21, entregando à tela seguinte
um pedido que continua não existindo na base.

[?] O caminho sem pedido para cópia termina sem gravar nada e entrega o pedido à tela de
programação de entrega, que responde **\* Pedido sem generos cadastrados \*** porque não
encontra item nenhum daquele pedido. Ou o pedido para cópia é obrigatório e falta a
recusa que o exige, ou esse caminho não deveria existir assim. Não escolho um dos dois
lados. Pergunta ao site.

### RN-21 — A tela entrega o pedido à programação de entrega, em alteração — e é o único caminho até ela

Terminada a recuperação (ou o caminho sem cópia), a tela **não mostra mais nada**: ela
passa a transação para a tela de **programação de entrega**, a `E121T`, levando o
**órgão, o grupo, o pedido, o fornecedor, o contrato, a semana, o período e os dias de
entrega**, com a operação marcada como **alteração** e com a marca de que a passagem vem
desta tela. A tela de programação abre, então, em alteração, com o pedido já carregado.
É a única saída desta tela, além de reabrir a si mesma para a confirmação.

A tela de programação **só abre por este caminho**: aberta por qualquer outro, ela não
processa nada, devolve a transação ao menu `E010M` deixando nele a marca de que a
passagem veio dela, e o menu responde marcando a **opção 16** — a que abre a `E120T` — e
avisando **\* Acesso deve ser feito pela tela E120T \***. É esse aviso que empurra quem
tentou abrir a programação de entrega sem passar por esta tela.

[?] A marca de origem que esta tela deixa para a seguinte viaja pela **área de trabalho
comum** das telas: os campos das duas áreas coincidem na ordem até o tipo de contrato, e
nenhum programa do acervo escreve a marca "E120T" na área da tela de programação. Que
as duas áreas sejam o mesmo espaço é conclusão da leitura das duas declarações, não algo
documentado no acervo. Pergunta ao site.

### RN-22 — Nada é mostrado nem gravado sem a conferência de tela, de sessão, de rota e de acesso

Na abertura, a tela confere que está **registrada** (senão **\* Tela nao disponivel \***)
e que o **código de acesso do servidor** alcança a tela. Ao enviar a transação, a lógica
de rota confere a tela de novo (**\* Tela nao cadastrada \***) e a operação de inclusão
(**\* Operacao nao disponivel \***), e a segurança confere que o **perfil do servidor
libera a inclusão** naquela tela (senão **\* Acesso negado para esta operacao \***) e que
a **estação é a da sessão** — em outra estação o acesso é encerrado e a sessão volta à
entrada. Sem passar por tudo, nada é conferido, mostrado ou gravado.

---

## Cenários BDD

```gherkin
Funcionalidade: Recuperar um pedido excluído do órgão filho SDI da coordenadoria regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, o grupo e o órgão filho do meu vínculo
    E tenho acesso à tela E120T

  Cenário: A operação é sempre a inclusão
    Dado que a transação chega com uma operação que não é a de inclusão
    Quando a tela confere a operação
    Então vejo "* Opcao nao disponivel. Use INC *"
    E o cursor fica no campo da operação
    E nada é conferido, mostrado ou gravado

  Cenário: A tela é identificada pelo órgão filho SDI e identifica o pedido pelo número com o ano
    Quando abro a tela E120T
    Então vejo os vinte campos da tela, com o órgão filho SDI à frente
    E o pedido é procurado pela chave formada pelo número do pedido junto com o ano da entrega
    E os campos numéricos têm o branco tratado como zero antes das conferências

  Cenário: A tela abre com o órgão e o grupo do meu vínculo e com cinco dias de entrega
    Dado que o meu vínculo carrega um órgão filho e um grupo
    Quando abro a tela E120T
    Então o órgão e o grupo já vêm preenchidos com os do meu vínculo
    E vejo o nome do órgão lido do cadastro
    E o campo da quantidade de dias de entrega vem preenchido com cinco

  Cenário: O órgão é obrigatório
    Quando confirmo sem informar o órgão
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão

  Cenário: O servidor não recupera pedido de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo outro órgão e confirmo
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão

  Cenário: O órgão tem de estar cadastrado e ser da minha secretaria
    Quando informo um órgão que não está no cadastro, ou um órgão de outra secretaria
    Então vejo "* Orgao nao cadastrado *" ou "* Orgao nao pertence a esta secretaria *"
    E o cursor fica no campo do órgão
    E nada é conferido depois disso

  Cenário: O órgão tem de ser de um grupo meu
    Dado que a minha sessão carrega um grupo
    Quando informo um órgão de outro grupo e confirmo
    Então vejo "<- Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E o grupo que eu digitei é substituído pelo do cadastro do órgão

  Cenário: O pedido a recuperar tem de ser informado, não pode existir e não pode estar com o operador logístico
    Quando confirmo sem informar o número e o ano do pedido
    Então vejo "* Informe pedido a ser recuperado *"
    E o cursor fica no campo do número
    Quando confirmo com um pedido que ainda existe na base de pedidos
    Então vejo "* Pedido nao esta excluido *"
    Quando confirmo com um pedido que já está na base do operador logístico
    Então vejo "* Pedido cad para operador logistico *"
    E nada é gravado

  Cenário: O número do pedido tem de caber no ano da entrega
    Dado que informo um ano da entrega que não tem registro no cadastro de pedidos
    Quando confirmo
    Então vejo "* Numero do pedido invalido *"
    E o cursor fica no campo do número
    Dado que informo um número maior que o último emitido para aquele ano e secretaria
    Quando confirmo
    Então vejo "* Numero do pedido invalido *"

  Cenário: O fornecedor tem de estar cadastrado
    Quando informo um código de fornecedor que não existe e confirmo
    Então vejo "* Fornecedor nao cadastrado *"
    E o cursor fica no campo do código do fornecedor
    Dado que informo um fornecedor cadastrado
    Então vejo a razão social dele na tela

  Cenário: O início da entrega tem de ser uma data válida, em dia de semana e fora dos feriados
    Quando informo um dia, mês e ano que não formam data válida
    Então vejo "* Data de inicio da entrega invalida *"
    Quando informo um início em sábado ou em domingo
    Então vejo "* Inicio da entrega nao deve ser um sabado *" ou
      "* Inicio da entrega nao deve ser um domingo *"
    Quando informo um início que é feriado da minha secretaria
    Então vejo "* Inicio da entrega nao deve ser um feriado *"
    E o cursor fica no campo do dia de início

  Cenário: A quantidade de dias de entrega vai de um a cinco
    Quando deixo a quantidade de dias de entrega em branco
    Então vejo "* Informe a quantidade de dias de entrega *"
    Quando informo uma quantidade maior que cinco
    Então vejo "* Quantidade maxima de dias de entrega = 5 *"
    E o cursor fica no campo da quantidade

  Cenário: O período de entrega tem de caber no ano da entrega e os dias são contados em dias úteis
    Dado que informo o início e a quantidade de dias de entrega
    Quando confirmo
    Então a tela calcula o limite do período pulando sábados, domingos e feriados
    E monta as datas de entrega do pedido, uma por dia do período
    E, se o início ou o limite caírem em outro ano, vejo "* Periodo de entrega invalido *",
      com o cursor no campo do ano de início

  Cenário: A semana de entrega é A, B, C, D ou E
    Quando informo uma semana diferente de A, B, C, D e E, ou deixo em branco
    Então vejo "* Informe semana com A / B / C / D / E *"
    E o cursor fica no campo da semana

  Cenário: O tipo de contrato é obrigatório e tem de estar cadastrado para o fornecedor
    Quando deixo o tipo de contrato em branco
    Então vejo "* Informe tipo contrato *"
    Quando informo um tipo de contrato que não existe para aquele fornecedor e secretaria
    Então vejo "* Contrato nao cad para este fornecedor *"
    E o cursor fica no campo do tipo de contrato

  Cenário: O operador logístico do contrato é mostrado
    Dado que o contrato existe e traz um operador logístico
    Quando a tela carrega o contrato
    Então vejo o código do operador logístico do contrato e o nome dele lido do cadastro
    E, se o operador não estiver no cadastro, o nome sai em branco e nada é avisado

  Cenário: O pedido para cópia, informado, tem de existir, ser do mesmo fornecedor e do mesmo contrato
    Quando informo um pedido para cópia que não existe
    Então vejo "* Pedido para copia nao cadastrado *"
    Quando informo um pedido para cópia de outro fornecedor
    Então vejo "* Pedido para copia de outro fornecedor *"
    Quando informo um pedido para cópia com item de outro tipo de contrato
    Então vejo "* Pedido para copia de outro contrato *"
    E o cursor fica no campo do número do pedido para cópia
    E nada é gravado

  Cenário: A recuperação é confirmada antes de qualquer gravação
    Dado que passei por todas as conferências
    Quando confirmo a tela
    Então vejo "* Confirma recuperacao do pedido <S/N> ? *", com o cursor no campo da resposta
    E nada foi gravado ainda
    Quando respondo S e nenhum dado mudou
    Então a recuperação segue
    Quando respondo qualquer outra coisa, ou respondo S tendo mudado algum dado
    Então a tela refaz as conferências e pergunta de novo, sem gravar nada

  Cenário: Confirmada, a recuperação grava o pedido, os itens, o consumo do contrato e a auditoria
    Dado que respondi S e o pedido para cópia foi informado
    Quando a recuperação é executada
    Então o pedido é gravado com a situação de pedido aprovado
    E os itens são gravados, um por classe, subclasse e gênero, com as datas de entrega e a
      quantidade acumulada da classe
    E o contrato passa a responder pela quantidade recuperada, somada à já entregue
    E cada movimento fica registrado na auditoria, com a operação, o conteúdo anterior e o
      posterior, a matrícula, a estação, o processo, a data e a hora da sessão e o tipo de órgão
    E só entram os itens do contrato cujo período já começou e cuja quantidade caiba no saldo
      inicial do contrato

  Cenário: Sem pedido para cópia a recuperação não grava nada
    Dado que não informei o número e o ano do pedido para cópia
    Quando confirmo a recuperação com S
    Então nenhum pedido, item, consumo de contrato ou registro de auditoria é gravado
    E a tela passa direto para a programação de entrega
    E a tela de programação responde "* Pedido sem generos cadastrados *"

  Cenário: O pedido é entregue à programação de entrega, em alteração, e é o único caminho até ela
    Dado que a recuperação terminou
    Quando a tela passa a transação adiante
    Então a tela de programação de entrega abre em alteração, com o órgão, o grupo, o pedido,
      o fornecedor, o contrato, a semana, o período e os dias de entrega já carregados
    E a marca de que a passagem veio da E120T vai junto
    Dado que a tela de programação é aberta por qualquer outro caminho
    Então ela não processa nada, volta ao menu E010M e eu vejo
      "* Acesso deve ser feito pela tela E120T *", com a opção 16 marcada

  Cenário: Nada acontece sem a conferência de tela, de sessão, de rota e de acesso
    Dado que estou na tela E120T
    Quando a conferência do registro da tela, do código de acesso, da estação, da rota ou da
      operação de inclusão não passa
    Então vejo "* Tela nao disponivel *", "* Tela nao cadastrada *",
      "* Acesso negado para esta matricula *", "* Acesso negado para esta operacao *",
      "* Operacao nao disponivel *" ou o acesso é encerrado e a sessão volta à entrada
    E nada é conferido, mostrado ou gravado
```
