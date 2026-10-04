# US — E031T — Remarcar as datas de entrega de um pedido de alimentação escolar

## Estória

Como **servidor da CRE que acompanha as entregas dos fornecedores**, quero **informar o
fornecedor, o tipo de contrato, a semana e o período do pedido e a nova data em que a
entrega deve começar**, para que **o pedido passe a ser entregue no novo período, com as
demais datas de entrega recalculadas e o documento da alteração emitido, sem ter de
refazer o pedido**.

O pedido já existe e já está aprovado; o que muda é a janela de entrega dele. É esta tela
que faz a remarcação: o servidor diz por onde a nova entrega começa e a tela recalcula as
datas, uma por entrega prevista no item, pulando fins de semana e feriados, dentro do que
o contrato permite. Sem ela, mudar a data de entrega de um pedido já aprovado teria de
ser feito fora do sistema, e o contrato continuaria apontando para um período que não é
mais o da entrega. A tela **não** altera o pedido, o item nem o contrato durante o
atendimento: ela confere, pede a confirmação e registra o pedido de impressão — é a
rotina que esse pedido dispara que grava as novas datas e emite o documento.

## Contexto

Jornada S000M → E000M → E010M → E031T.

Ator: servidor de CRE — informa a CRE, o fornecedor, o tipo de contrato, o início do
período e a semana do pedido, a impressora e a nova data de início da entrega, confere o
que a tela mostra e confirma.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As duas telas do meio, `E000M` e `E010M`, são menus: têm opções e só encaminham, e nenhuma
das duas grava nada. A `E031T` é aberta pela opção 11 do `E010M`, que a recarrega sem
passar registro nem operação adiante; o que ela aproveita da sessão é o **vínculo do
servidor** — matrícula, código de acesso, privilégio, estação, tipo de órgão, CRE e a data
do sistema —, que é regra da entrada e está no anexo de evidências. O tipo de órgão e a
CRE da sessão são o recorte com que ela procura os pedidos e a permissão do contrato. A
tela **não** muda de comportamento conforme quem a chamou: ela não confere o código da
tela de origem em nenhum ponto e se coloca em alteração por conta própria.

A jornada termina na `E031T`: ela não encaminha registro nem operação para outra tela. O
que ela entrega é a **requisição de impressão**, que é o que dispara a rotina que grava as
novas datas no pedido e no item, deixa a auditoria da alteração e emite o documento.

## Regras de negócio

### RN-01 — A tela remarca a entrega de um pedido aprovado: ela confere, pede confirmação e registra o pedido de impressão

A tela tem uma operação: mudar a janela de entrega de um pedido já aprovado. Para isso ela
lê o pedido, o item do pedido, a permissão do contrato, o cadastro de feriados, o cadastro
de telas, o cadastro de servidores e o registro de impressora do servidor — e não altera
nenhum deles durante o atendimento. Enquanto o servidor está na tela, o que ela grava é a
**impressora do servidor** e, confirmada a alteração, a **requisição de impressão**; a
troca das datas no pedido e no item acontece depois, pela rotina que a requisição dispara
(RN-13).

### RN-02 — A tela só opera em alteração

A cada exibição a tela se coloca em **alteração**. Qualquer outra opção de manutenção é
recusada com **\* Opcao nao disponivel. Use ALT \***, com o cursor de volta no campo da
opção, e a tela não segue: aqui não se inclui nem se exclui pedido.

### RN-03 — A tela só opera na CRE da sessão

A tela abre com a **CRE do vínculo do servidor** já preenchida e só aceita essa. Informar
outra CRE é recusado com **\* Usuario sem acesso a outro grupo \***, com o cursor de volta
no campo, e nada é gravado. Quando o vínculo do servidor não tem CRE, o campo abre em
branco e qualquer CRE informada é aceita — e é a CRE confirmada que recorta a procura dos
pedidos e da permissão do contrato.

### RN-04 — Fornecedor, tipo de contrato, início do período e semana são obrigatórios; a semana vai de A a E

Para remarcar, o servidor tem de informar o **fornecedor**, o **tipo de contrato**, o
**início do período** do pedido e a **semana** dele, além da impressora (RN-05). Sem
fornecedor, a recusa é **\* Informe o fornecedor \***; sem tipo de contrato, **\* Informe o
tipo contrato \***; com o dia do início do período zerado, **\* Informe data inicial do
periodo \***; e com a semana diferente de A, B, C, D ou E, **\* Informe semana com A / B /
C / D / E \***. Cada recusa devolve o cursor ao campo e não grava nada.

Os **quinze** campos numéricos da tela — a CRE, o fornecedor, o tipo de contrato, as três
datas do início do período, as três do limite do período, as três do início da entrega e as
três do limite da entrega — passam por edição numérica antes de qualquer consulta, com o
campo em branco tratado como zero.

[?] A rotina que faz a edição numérica não está no acervo: só aparece chamada. O que o
servidor vê quando digita algo que não é número não se conclui do fonte — e seis dos quinze
campos (os três do limite do período e os três do limite da entrega) não têm posição de
cursor definida para a recusa. Pergunta ao site.

[?] Ao lado do código do fornecedor existe um campo para o nome do fornecedor e ele
aparece na tela, mas nada no programa lhe dá um nome: é só limpo e exibido. O nome existe
no cadastro de fornecedores — a rotina que emite o documento o lê de lá —, de modo que a
tela poderia mostrá-lo e não mostra. Se o campo devia ser preenchido, o caminho não o faz.
Pergunta ao site.

### RN-05 — A impressora é obrigatória e fica registrada para o servidor

Ao abrir, a tela traz a **impressora registrada para a matrícula do servidor**. Deixando o
campo em branco, a recusa é **\* Informe a impressora \***, com o cursor no campo, e nada é
gravado.

A impressora informada passa a ser a do servidor: se já havia um registro para a matrícula,
a tela o atualiza; se não havia, a tela cria um. Isso acontece **antes** das conferências
do fornecedor, do contrato, das datas e da permissão, e antes da confirmação: uma
remarcação recusada depois — ou nem confirmada — já deixou a impressora do servidor
trocada.

[?] O cadastro admite mais de um registro de impressora para a mesma matrícula, e a tela
relê e atualiza um deles — o primeiro que o cadastro devolve. Com mais de um, qual é o
atualizado não se conclui do acervo. Pergunta ao site.

### RN-06 — O pedido tem de existir, aprovado, para aquele fornecedor, semana e período, com item do tipo de contrato

A tela procura, entre os pedidos do tipo de órgão e da CRE da sessão, com o **início do
período exatamente igual** ao informado, um pedido cujo **fornecedor** seja o informado,
cuja **semana** seja a informada e que esteja **aprovado** — pedido em outra situação é
tratado como inexistente. O pedido só conta se tiver um **item** cujo **tipo de contrato**
seja o informado. Não achando, a recusa é **\* Pedidos nao cad. para os dados informados
\***, com o cursor de volta no fornecedor, e nada é gravado.

### RN-07 — O limite do período mostrado vem do pedido

Quando o item ainda não traz limite, a tela assume o **limite do período que está no
pedido** — dia, mês e ano — e o mostra nos campos de limite, que viajam com a remarcação.

[?] Os três campos do limite aparecem na tela, passam pela edição numérica e ficam
guardados na área de trabalho da tela, mas não entram no cálculo das datas, na conferência
da permissão do contrato nem nos parâmetros que a tela envia. Para que servem, o acervo não
diz. Pergunta ao site.

### RN-08 — A nova data de início da entrega tem de ser válida, num ano reconhecido e num dia útil

A **nova data de início da entrega** é conferida antes de qualquer gravação. Se não for uma
data válida — ou se o ano não estiver entre **1994 e 2099** —, a recusa é **\* Data de
inicio da entrega invalida \***. Válida, ela não pode cair em **sábado** — **\* Inicio da
entrega nao deve ser um sabado \*** —, em **domingo** — **\* Inicio da entrega nao deve ser
um domingo \*** — nem em **feriado** do tipo de órgão da sessão — **\* Inicio da entrega
nao deve ser um feriado \***. Em todas, o cursor volta para o dia da entrega e nada é
gravado.

[?] A conferência da data informada depende também de o sistema conseguir converter a data
do dia: se a conversão da data do sistema não passar, a data informada é recusada como
inválida, mesmo sendo boa. Se isso é intencional, o acervo não diz. Pergunta ao site.

[?] A faixa de ano aceita — 1994 a 2099 — não tem explicação no acervo desta jornada.
Pergunta ao site.

### RN-09 — A tela recalcula a grade de entregas do novo período

O número de entregas vem do item: a tela conta **quantas datas de entrega** o primeiro item
que casa com o contrato informado tem preenchidas — de **uma a cinco** — e, a partir da
**data de início informada**, recalcula todas: a primeira é a data informada e as seguintes
são os dias úteis consecutivos, saltando sábados, domingos e os feriados do tipo de órgão da
sessão. A **última data calculada é o limite da entrega**.

[?] A tela conta as datas de entrega do item mas **não** usa as datas gravadas nele:
recalcula tudo por dias úteis consecutivos. Se o período do site entrega em dias alternados
ou em uma data por semana, a remarcação sai com datas diferentes das que estavam no pedido.
Pergunta ao site.

[?] Os três campos do limite da entrega aparecem na tela e passam pela edição numérica como
os demais, mas a tela sempre os substitui pelo resultado do cálculo: o que o servidor
digitar neles é descartado. Se o campo é, na prática, só de leitura, o acervo não diz.
Pergunta ao site.

### RN-10 — A entrega tem de caber na permissão do contrato

A tela procura a permissão do **tipo de órgão da sessão**, da **CRE informada** e do **tipo
de contrato informado**, com item classificado e não excluído, e exige que a **primeira
data de entrega não seja anterior ao início da permissão** e a **última não seja posterior
ao limite dela**. Fora disso, a recusa é **\* Entrega fora dos limites da permissao \***,
com o cursor de volta no dia da entrega, e nada é gravado.

[?] A tela confere **uma única** permissão do grupo: o desvio que deveria passar à próxima
compara a data de início da permissão com uma data que o programa só zera e nunca preenche
— e qualquer data é maior ou igual a zero —, de modo que ele deixa passar sempre na
primeira leitura. Se a intenção era percorrer as permissões do grupo até achar a que cobre
o novo período, o caminho não percorre; e, não achando permissão nenhuma, a tela recusa pela
mesma mensagem. Não escolho um dos dois lados. Pergunta ao site.

### RN-11 — A remarcação é confirmada antes de ser registrada

Passando por todas as conferências, a tela ainda não registra a requisição: ela guarda o que
foi conferido, mostra **\* Confirma alteracao da data <S/N> ? \*** com o cursor na resposta
e **reabre a si mesma**, com os valores guardados de volta nos campos.

Respondendo **S** com os mesmos dados, a tela segue e registra a requisição. Mudando algum
dos dez valores que a confirmação compara — a própria opção de manutenção, o fornecedor, o
tipo de contrato, a semana, o início do período e o início da entrega —, a tela refaz todas
as conferências e pergunta outra vez. Os valores que a comparação não olha — a CRE, o limite
do período e o limite da entrega — voltam do que estava guardado; a impressora não é
guardada, e a que estiver no campo é a que vai para a requisição.

[?] Responder **N** não cancela nada: a tela refaz as conferências e pergunta outra vez. O
acervo desta jornada não tem caminho de desistência. Pergunta ao site.

### RN-12 — A tela registra a requisição de impressão, com o número seguinte da fila

Confirmada a alteração, a tela registra **uma requisição de impressão** na fila: ela leva o
relatório de remarcação, o **número seguinte ao maior já registrado**, a CRE, a impressora,
a matrícula do servidor, a estação, o dia, o mês e o ano do sistema e o tipo de órgão da
sessão, e a operação é marcada como **inclusão**. A solicitação é de **uma cópia**. Quando o
ambiente é o LINC, a tela entrega também o **job de impressão**, com os parâmetros da
remarcação: o tipo de órgão, a CRE, o fornecedor, o tipo de contrato, a semana, o início do
período, as cinco datas de entrega calculadas e a matrícula que pediu.

[?] O que faz o ambiente se identificar como LINC — e o que acontece com a requisição nos
outros ambientes, já que ela fica na fila sem o job — não está no acervo desta jornada.
Pergunta ao site.

### RN-13 — A requisição é o que aplica a alteração, deixa a auditoria e emite o documento

A requisição registrada não é só impressão: é ela que dispara a rotina de remarcação. A
rotina recebe os parâmetros que a tela montou, refaz a mesma procura da tela — pedido do
tipo de órgão e da CRE, com o início do período informado, do fornecedor e da semana
informados, aprovado, com item do tipo de contrato informado — e, para cada pedido
encontrado:

- deixa o **registro de auditoria da alteração** do item e do pedido, com a imagem anterior
  e a posterior;
- grava as **cinco datas de entrega** no item do pedido;
- grava o **período do pedido** com a primeira e a última data de entrega calculadas;
- **emite o documento**, com o grupo, o fornecedor (código e razão social), a semana e o
  tipo de contrato, a janela de entrega que o pedido tinha — **DE** — e a nova — **PARA** —,
  e a relação dos pedidos atingidos;
- ao terminar, **apaga a requisição** da fila.

[?] A rotina grava o novo início do período no próprio pedido, e é por esse início que ela
acabou de localizar o pedido: o conjunto pelo qual ela lê o pedido não declara que aceita
troca de chave, ao contrário do conjunto usado pela tela do pedido. O acervo não permite
concluir se o banco aceita a troca; se não aceitar, a alteração não se completa, e o
documento é emitido assim mesmo. Pergunta ao site.

### RN-14 — A tela não apaga nada, e só a impressora e a requisição recebem gravação

A tela declara, para cada um dos **oito** cadastros que enxerga, as rotinas de gravar, de
travar e de apagar. Só a rotina de gravar do **registro de impressora do servidor** e a da
**requisição de impressão** são executadas; as rotinas de apagar dos oito não são executadas
por caminho nenhum, e a única trava executada fora delas é a do registro de impressora.
Quem apaga a requisição é a rotina que a consome (RN-13).

### RN-15 — Antes de operar, a tela confere o acesso, a rota e a permissão de alteração

Na exibição, a tela chama a rotina comum de segurança do servidor e da tela: ela confere
que o servidor está na **estação em que a sessão foi aberta** (em outra, o acesso é
encerrado e a sessão volta à entrada), que a tela está registrada e que o **código de
acesso** do servidor alcança a tela. Na conferência, chama as rotinas comuns de **rota** e
de **permissão por operação**, com o vínculo da sessão — matrícula, acesso, privilégio, tipo
de órgão e CRE —, e exige a **permissão de alteração** do código de acesso para esta tela.
Retorno diferente de OK limpa o status e interrompe a tela, sem gravar nada.

[?] As regras dessas rotinas comuns e os textos das recusas não estão no acervo desta
jornada: elas aparecem só chamadas, e a tela apenas testa o retorno. Pergunta ao site.

### RN-16 — A tela não muda de modo conforme quem a chamou

A tela é aberta pelo menu `E010M` e não confere em ponto nenhum o código da tela de origem:
ela se coloca em alteração por conta própria e não recebe registro nem operação de quem a
chamou. O único comportamento que depende de fora é o **campo de rota**: se ele chegar
preenchido com o código de uma tela, a rotina comum de rota entrega a sessão a essa tela e
abandona esta.

[?] Quem preenche o campo de rota, e em que situação, não aparece no acervo: nenhum programa
do acervo o preenche no caminho até aqui. Pergunta ao site.

### RN-17 — Falha no banco interrompe a operação e avisa

Erro de banco na leitura ou na gravação interrompe a operação e a tela avisa; a requisição
não é considerada registrada.

[?] Quando a gravação da requisição não se completa — porque o número já está em uso —, a
tela segue e entrega o job de impressão mesmo assim, sem mensagem própria: a rotina é
chamada sobre os pedidos ainda que a requisição não tenha ficado na fila. O acervo não diz
se é isso que se quer. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Remarcar as datas de entrega de um pedido de alimentação escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E031T

  Cenário: RN-06, RN-07, RN-08, RN-09, RN-10, RN-11, RN-12 e RN-13 — remarcar a entrega de um pedido aprovado
    Dado que existe um pedido aprovado do meu tipo de órgão e da minha CRE, iniciado no período informado, do fornecedor e da semana informados, com item do tipo de contrato informado
    E a nova data de início da entrega é um dia útil que não é feriado
    E a nova janela de entrega cabe na permissão do contrato
    Quando informo a impressora e a nova data de início da entrega e confirmo a alteração com S
    Então vejo a requisição de impressão registrada na fila
    E a rotina que aplica a remarcação é disparada
    E as novas datas de entrega ficam gravadas no item do pedido
    E o período do pedido passa a ser o da primeira e o da última data de entrega

  Cenário: RN-03 — ao abrir, a tela propõe a CRE e a impressora da sessão
    Dado que o meu vínculo tem CRE e eu já tenho impressora registrada
    Quando abro a tela E031T
    Então o campo da CRE vem preenchido com a da minha sessão
    E o campo da impressora vem preenchido com a impressora registrada para a minha matrícula
    E nada é gravado

  Cenário: RN-02 — opção de manutenção não disponível
    Dado que estou na tela E031T
    Quando informo uma opção de manutenção diferente de alteração
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor volta para o campo da opção
    E a tela não segue

  Cenário: RN-03 — CRE de outro grupo
    Dado que o meu vínculo carrega uma CRE
    Quando informo outra CRE e confirmo
    Então vejo "* Usuario sem acesso a outro grupo *"
    E o cursor volta para o campo da CRE
    E nada é gravado

  Cenário: RN-05 — impressora não informada
    Dado que não há impressora registrada para a minha matrícula
    Quando deixo a impressora em branco e confirmo
    Então vejo "* Informe a impressora *"
    E o cursor volta para o campo da impressora

  Cenário: RN-04 — fornecedor não informado
    Dado que informei a impressora
    Quando deixo o fornecedor em branco e confirmo
    Então vejo "* Informe o fornecedor *"
    E o cursor volta para o campo do fornecedor

  Cenário: RN-04 — tipo de contrato não informado
    Dado que informei a impressora e o fornecedor
    Quando deixo o tipo de contrato em branco e confirmo
    Então vejo "* Informe o tipo contrato *"
    E o cursor volta para o campo do tipo de contrato

  Cenário: RN-04 — início do período não informado
    Dado que informei a impressora, o fornecedor e o tipo de contrato
    Quando deixo o dia do início do período zerado e confirmo
    Então vejo "* Informe data inicial do periodo *"
    E o cursor volta para o campo do início do período

  Cenário: RN-04 — semana fora de A a E
    Dado que informei a impressora, o fornecedor, o tipo de contrato e o início do período
    Quando informo uma semana diferente de A, B, C, D e E e confirmo
    Então vejo "* Informe semana com A / B / C / D / E *"
    E o cursor volta para o campo da semana

  Cenário: RN-05 — a impressora informada fica registrada para o servidor
    Dado que a impressora que informo é diferente da registrada para a minha matrícula
    Quando confirmo
    Então a impressora informada fica registrada para a minha matrícula

  Cenário: RN-05 — a impressora é acertada mesmo quando a remarcação é recusada
    Dado que a impressora que informo é diferente da registrada para a minha matrícula
    Quando confirmo com o fornecedor em branco
    Então vejo "* Informe o fornecedor *"
    E a impressora informada já ficou registrada para a minha matrícula
    E nenhuma requisição de impressão foi registrada

  Cenário: RN-06 — não há pedido aprovado para os dados informados
    Dado que não existe pedido aprovado do meu tipo de órgão e da minha CRE, iniciado no período informado, do fornecedor e da semana informados
    Quando confirmo
    Então vejo "* Pedidos nao cad. para os dados informados *"
    E o cursor volta para o campo do fornecedor
    E nada é gravado

  Cenário: RN-06 — pedido em outra situação é tratado como inexistente
    Dado que o único pedido do período, do fornecedor e da semana informados não está aprovado
    Quando confirmo
    Então vejo "* Pedidos nao cad. para os dados informados *"
    E nada é gravado

  Cenário: RN-06 — pedido sem item do tipo de contrato informado não conta
    Dado que o único pedido do período, do fornecedor e da semana informados não tem item do tipo de contrato informado
    Quando confirmo
    Então vejo "* Pedidos nao cad. para os dados informados *"
    E nada é gravado

  Cenário: RN-08 — data de início da entrega inválida
    Dado que há pedido e permissão para os dados informados
    Quando informo uma data de início da entrega que não existe, ou com ano fora de 1994 a 2099
    Então vejo "* Data de inicio da entrega invalida *"
    E o cursor volta para o campo do dia da entrega
    E nada é gravado

  Cenário: RN-08 — início da entrega em sábado
    Dado que há pedido e permissão para os dados informados
    Quando informo uma data de início da entrega que cai em sábado
    Então vejo "* Inicio da entrega nao deve ser um sabado *"
    E o cursor volta para o campo do dia da entrega

  Cenário: RN-08 — início da entrega em domingo
    Dado que há pedido e permissão para os dados informados
    Quando informo uma data de início da entrega que cai em domingo
    Então vejo "* Inicio da entrega nao deve ser um domingo *"

  Cenário: RN-08 — início da entrega em feriado
    Dado que a data informada é feriado do meu tipo de órgão
    Quando confirmo
    Então vejo "* Inicio da entrega nao deve ser um feriado *"

  Cenário: RN-09 — a grade do novo período é recalculada
    Dado que o item do pedido encontrado tem três datas de entrega preenchidas
    Quando confirmo
    Então a primeira data de entrega é a data que informei
    E as seguintes são os dias úteis consecutivos, saltando sábados, domingos e os feriados do meu tipo de órgão
    E a última data calculada é o limite da entrega

  Cenário: RN-10 — entrega fora dos limites da permissão
    Dado que a permissão do contrato da minha CRE não cobre o novo período de entrega
    Quando confirmo
    Então vejo "* Entrega fora dos limites da permissao *"
    E o cursor volta para o campo do dia da entrega
    E nada é gravado

  Cenário: RN-10 — não há permissão para o contrato
    Dado que não há permissão do contrato do tipo informado na minha CRE
    Quando confirmo
    Então vejo "* Entrega fora dos limites da permissao *"
    E nada é gravado

  Cenário: RN-11 — a tela pede confirmação antes de registrar
    Dado que todas as conferências passaram
    Quando a tela termina a conferência
    Então vejo "* Confirma alteracao da data <S/N> ? *"
    E o cursor fica no campo da resposta
    E a tela reabre com os valores que guardou
    E nada foi registrado ainda

  Cenário: RN-11 — mudar um valor comparado refaz as conferências
    Dado que estou diante da confirmação
    Quando troco o fornecedor e respondo S
    Então a tela refaz as conferências com o novo fornecedor
    E pergunta a confirmação outra vez

  Cenário: RN-11 — responder N
    Dado que estou diante da confirmação
    Quando respondo N
    Então a tela refaz as conferências
    E pergunta a confirmação outra vez
    E nada é registrado

  Cenário: RN-12 — a requisição de impressão registrada
    Dado que confirmei a alteração com S
    Quando a tela registra a requisição
    Então a requisição fica com o relatório de remarcação, a CRE, a impressora, a minha matrícula, a estação, a data do sistema e o tipo de órgão da sessão
    E o número é o seguinte ao maior já registrado
    E a operação fica marcada como inclusão

  Cenário: RN-12 — o job de impressão no ambiente LINC
    Dado que confirmei a alteração com S
    E o ambiente é o LINC
    Quando a tela registra a requisição
    Então a tela entrega também o job de impressão
    E o job leva os parâmetros da remarcação: tipo de órgão, CRE, fornecedor, tipo de contrato, semana, início do período, as cinco datas de entrega e a minha matrícula

  Cenário: RN-13 — a rotina aplica a alteração e emite o documento
    Dado que confirmei a alteração com S
    Quando a rotina disparada pela requisição procura os pedidos
    Então as novas datas de entrega são gravadas no item do pedido
    E o período do pedido passa a ser o da primeira e o da última data de entrega
    E fica o registro de auditoria da alteração, com a imagem anterior e a posterior
    E o documento é emitido com o grupo, o fornecedor, a semana, o tipo de contrato e a janela de entrega DE e PARA
    E a requisição é apagada da fila

  Cenário: RN-14 — a tela não apaga nada e só grava em dois cadastros
    Dado que faço uma remarcação completa
    Quando o sistema processa
    Então só o registro de impressora do servidor e a requisição de impressão recebem gravação da tela
    E nenhum registro é apagado pela tela
    E nenhum pedido, item, contrato, feriado, tela ou servidor é alterado pela tela

  Cenário: RN-15 — sem permissão de alteração
    Dado que o meu código de acesso não tem a permissão de alteração nesta tela
    Quando confirmo
    Então a tela não opera
    E nada é gravado

  Cenário: RN-17 — falha do banco
    Dado que a leitura ou a gravação falha no banco
    Quando confirmo
    Então a transação é interrompida com o aviso de erro do sistema
    E a requisição não é considerada registrada
```
