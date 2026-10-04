# US — C840T — Registrar o cálculo da estimativa da alimentação escolar do grupo e encomendar o processamento

## Estória

Como **servidor de CRE**, quero **registrar o cálculo da estimativa da alimentação escolar do
meu grupo para um período e encomendar o processamento**, para que **a estimativa daquele
período seja apurada com o cardápio, o planejamento, a média de comensais, a tabela de preços e
os períodos de exclusão certos, sem ninguém montar isso à mão a cada período**.

A estimativa é apurada período a período: cada cálculo vale de um início até uma data limite, e
é a data limite que distingue um período do outro. Esta tela é quem abre o período — confere se
tudo de que o cálculo precisa já está cadastrado para o grupo e para aquele período, recolhe as
datas de vigência e os períodos que ficam de fora, pergunta a quem opera e registra o cálculo,
entregando o processamento à fila. Sem ela não existe período de cálculo, e nenhuma estimativa é
apurada para o grupo naquele período.

## Contexto

Jornada S000M → C000M → C800M → C840M → C840T.

Ator: servidor de CRE — informa o grupo, a data limite do cálculo, a data limite da tabela de
preços, os períodos de exclusão e a impressora, e confirma o cálculo.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os três menus do caminho — `C000M`, `C800M` e `C840M` — só
encaminham e não gravam nada.

Nenhuma tela anterior desta jornada encadeia nela: quem a abre é o menu `C840M`, que passa
apenas o código da tela a abrir, sem registro e sem operação. Por isso a C840T não herda modo
de quem a chamou — ela sempre abre em inclusão, e é ela própria que repõe a operação.

O contexto de que a C840T se serve — a matrícula, o privilégio, o tipo de órgão, a coordenação
regional escolar e a data do sistema — é o que a entrada deixou na sessão; a tela não
recalcula nada disso. O tipo de órgão da sessão entra na chave do cálculo e nas procuras dos
cadastros que a tela confere: é ele que limita o que a tela alcança.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela sempre abre em inclusão, e só inclusão e consulta passam

Ao ser apresentada — e ela é sempre apresentada por um menu, que não passa registro nem
operação —, a tela repõe a operação como **inclusão**. Só duas operações seguem: inclusão e
consulta. Qualquer outra é recusada com **\* Operacao nao disponivel. Use INC ou CON \***, com
o cursor no campo da operação e **sem ler cadastro nenhum**. Alteração e exclusão, portanto,
não se fazem por esta tela: um cálculo já registrado não se corrige nem se apaga por aqui.

[?] A recusa manda usar **INC** e **CON**, mas o valor que a tela aceita como inclusão e o que
ela aceita como consulta são os códigos internos dessas duas operações, que não são esses
textos; nenhum documento do material lido diz que o terminal traduz o mnemônico antes de
enviar. Ou o formulário traduz, ou quem seguir a mensagem é recusado. Pergunta ao site.

[?] A recusa só é alcançável se a máscara oferecer a quem opera um campo de operação, e a
abertura da tela repõe a inclusão sozinha; a ficha da tela não lista rótulo de campo de
operação. Se a máscara não tem esse campo, a recusa é trecho sem uso. Pergunta ao site.

### RN-02 — O cálculo é de um grupo e de uma data limite, e é a data limite que distingue um período do outro

Quem opera informa o **grupo** — a coordenação regional escolar, o único campo com rótulo de
negócio na tela (**COORD.REG.ESCOLA**) — e o **dia, o mês e o ano limite** do cálculo. O
cálculo é guardado no cadastro dos cálculos de estimativa por tipo de órgão + grupo + ano, mês
e dia limite: **há um registro por período calculado**, e é a data limite que distingue um
período do outro.

O cadastro tem **26 campos** — o grupo, o tipo de órgão, as quatro datas de vigência (o início e
o limite do cálculo, o início e o limite da tabela de preços), cada uma em dia, mês e ano, e as
doze datas dos seis períodos de exclusão — e capacidade para **10.000 registros** (capacidade é
o máximo esperado, parâmetro de dimensionamento, não o que está cadastrado).

### RN-03 — A consulta mostra o cálculo já registrado, e avisa quando não há

Na consulta o sistema lê o cálculo do grupo pela data limite informada e preenche a tela com o
que está gravado: as datas de vigência do calendário, as datas de vigência da tabela de preços
e as datas dos seis períodos de exclusão. Não achando, avisa **\* Nao existe calc. estimativa
para esta data \***, devolve o cursor ao dia da data limite e não preenche nada.

### RN-04 — A consulta não grava nada

Na consulta a tela só lê. O caminho termina marcado como recusado, e é essa marca que impede a
gravação: nenhum registro é incluído, alterado ou excluído e nenhum lançamento de auditoria é
gerado. O trabalho de gravar o cálculo é de uma rotina que a passagem final executa — a mesma
rotina que a consulta desliga com a marca de recusa. As rotinas de gravação, de exclusão e de
travamento de registro existem para os doze cadastros que a tela enxerga, mas o caminho da
consulta não chega a nenhuma delas: declarar não é executar.

### RN-05 — Incluir exige que o grupo esteja cadastrado no tipo de órgão da sessão

O grupo informado tem de existir no cadastro de grupos **dentro do tipo de órgão da sessão**.
Não existindo, a recusa é **\* Grupo nao cadastrado \***, com o cursor no campo do grupo, e a
inclusão não segue.

### RN-06 — Incluir exige que ainda não exista cálculo para o grupo e a data

Antes das demais conferências, a tela procura no cadastro dos cálculos de estimativa o registro
do grupo para aquela data limite. Achando, recusa com **\* Ja existe estimativa calculada para
esta data \*** e devolve o cursor ao dia da data limite: um período se abre uma vez só, e quem
precisa refazer um cálculo já aberto não o refaz por esta tela.

### RN-07 — Incluir exige o cardápio do período, e é dele que vem o início do calendário

A tela procura o cardápio vigente na data limite informada, para o tipo de órgão da sessão.
Não achando, recusa com **\* Nao existem cardapios neste periodo \*** e devolve o cursor ao dia
da data limite. Achando, é do cardápio que sai o **início do calendário** do cálculo: o início
é o do cardápio cadastrado, não o que estiver digitado na tela — e é contra esse início, junto
com a data limite, que a janela dos períodos de exclusão é conferida.

### RN-08 — Incluir exige o planejamento do grupo no período

A tela procura o planejamento do grupo — o cardápio de cada dia da semana, por segmento de
atendimento e por referência — para a data limite informada. Não achando, recusa com
**\* Planejamento nao cadastrado \*** e devolve o cursor ao campo do grupo.

### RN-09 — Incluir exige a média de comensais do grupo no período

A tela procura a média de comensais do grupo para a data limite informada. Não achando, recusa
com **\* Media de comensais nao cadastrada \*** e devolve o cursor ao dia da data limite. É essa
média que dimensiona quantas refeições o período estima.

### RN-10 — Incluir exige a tabela de preços do período, e é dela que vem o início da tabela

A tela procura a tabela de preços dos gêneros vigente na **data limite da tabela** informada,
para o tipo de órgão da sessão. Não achando, recusa com **\* Tabela de referencia nao
cadastrada \*** e devolve o cursor ao dia da data limite da tabela. Achando, é da tabela que sai
o **início da tabela**: o início é o da tabela cadastrada, não o que estiver digitado na tela.

### RN-11 — Incluir exige as letras da semana do grupo no período

A tela procura as letras da semana cadastradas para o grupo — a letra que diz qual cardápio
vale em cada semana do período. Não achando, recusa com **\* Letras da semana nao cadastr. para
o periodo \*** e devolve o cursor ao dia da data limite.

[?] As letras da semana são cadastradas por período, identificado pelo seu **início**; ao
conferir, porém, a tela procura o registro posicionando-o pela **data limite do cálculo**, não
pelo início, e depois aceita o registro que encontrar para o mesmo grupo. Ou o cadastro usa a
data limite como início do período das letras, ou a conferência olha pela posição errada — e
nesse caso a recusa de letras não cadastradas dispara para períodos que as têm. O que os
sinalizadores da leitura fazem não está no corpus nem no manual. Pergunta ao site.

### RN-12 — Até seis períodos de exclusão, cada um dentro da janela do cálculo

A tela recebe até **seis períodos de exclusão**, e cada um tem **duas datas** — a de início e a
de limite —, cada uma em dia, mês e ano: são **36 campos de data**. Período com o dia de início
zerado é período não informado, e o sistema passa ao seguinte sem reclamar. Período informado é
conferido, nesta ordem: a data de início tem de ser uma data válida, e a de limite também; o
início não pode ser maior que o limite; o início não pode ser anterior ao início do calendário
do cálculo; e o limite não pode passar da data limite do cálculo. Cada recusa tem a sua
mensagem — **\* Data inicial do periodo excluido invalida \***, **\* Data final do periodo
excluido invalida \***, **\* Data inicial maior que data final \*** e **\* Periodo de exclusao
fora do limite de calculo \*** —, e o cursor volta ao campo do período que falhou.

[?] O que é, em negócio, um período de exclusão — e por que são seis, em duas famílias de três
— não está no corpus lido nem no manual: as mensagens só dizem que o período fica fora do
limite de cálculo. Pergunta ao site.

### RN-13 — A impressora é obrigatória

Conferidos os seis períodos, a tela exige a **impressora**. Em branco, recusa com **\* Informe a
impressora \*** e devolve o cursor ao campo. É o destino do relatório que o cálculo vai gerar.

### RN-14 — Antes de registrar, a tela pergunta, e só a resposta S segue

Passando por todas as conferências, a tela guarda o que foi informado, apresenta **\* Confirma
calculo <S/N> ? \*** e volta a se apresentar com o cursor no campo da resposta; nesse passo nada
é gravado. Só a resposta **S** segue para o registro. Se qualquer campo mudou entre a pergunta e
a resposta, as conferências são refeitas desde o começo e a pergunta é feita de novo — o que
mudou não passa por baixo da confirmação dada.

[?] Responder outra coisa que não **S** não cancela: a tela limpa a resposta, repõe o que já
estava em tela e **volta a pedir a mesma confirmação**, sem gravar. Não há, no caminho lido, um
desfecho que encerre a operação com resposta negativa. Se o esperado é que a resposta negativa
cancele, o caminho não cancela. Pergunta ao site.

### RN-15 — Um pedido do mesmo relatório já na fila recusa o pedido novo

Confirmado o cálculo, e antes de registrar, a tela varre a fila de pedidos de relatório à procura
de um pedido do mesmo relatório de cálculo, feito para o mesmo tipo de órgão. Achando, avisa
**\* Relatorio em processamento. Aguarde. \***, devolve o cursor ao campo da resposta e **não
registra nada**: nem o cálculo, nem o lançamento de auditoria, nem o pedido novo.

[?] A varredura é posicionada com o número do pedido zerado, e o pedido que a própria tela
registra leva um número calculado (o último da fila mais um). Se a leitura alcançar qualquer
pedido pendente daquele relatório, a recusa vale; se ela exigir a chave inteira do pedido, a
recusa é praticamente inalcançável — nenhum pedido desta tela tem o número zerado. O acervo lido
não define qual dos dois; não escolho um lado. Pergunta ao site.

### RN-16 — Confirmado, o cálculo é registrado e o processamento é entregue

Com a resposta **S**, a tela registra o cálculo do grupo para a data limite — o tipo de órgão, o
grupo, as datas de vigência do calendário e da tabela de preços e as doze datas dos seis
períodos de exclusão —, lança na auditoria o que foi pedido, com a tela de origem, a operação de
inclusão, a matrícula, a estação, a data e a hora, e toma o número seguinte da fila para
registrar a solicitação do relatório, com a impressora, a estação, a matrícula, o grupo e os
parâmetros do relatório. Em seguida entrega o processamento à fila e mostra **\* Estimativa
sendo calculada \***, voltando a se apresentar. Quem calcula é o processamento entregue, não a
tela: o que a tela faz é abrir o período e encomendar o cálculo.

A tela não entrega o serviço a outra tela: ela reabre a si mesma. O que ela passa adiante é o
pedido do relatório de cálculo, com os parâmetros do período, e o trabalho à fila de
processamento.

[?] A entrega à fila de processamento só acontece quando o produto em execução não é o LINC; o
que a tela faz no caso contrário não está nos fontes desta jornada. Pergunta ao site.

[?] Se o cálculo do grupo depende das datas de vigência e dos períodos de exclusão que a tela
acabou de registrar — e não do que o processamento encontra por conta própria —, esta jornada
não mostra: o processamento roda fora dos fontes lidos. Pergunta ao site.

### RN-17 — Antes de registrar, a tela confere o tipo de órgão da sessão

Imediatamente antes da passagem que grava, e depois de todas as conferências, a tela relê o
cadastro dos tipos de órgão pelo tipo de órgão da sessão. Achando o registro marcado como
**excluído** ou como **purgado**, recusa com o aviso de erro padrão do sistema e interrompe a
passagem. Não achando o registro, a passagem também não grava: o tratamento de registro ausente
assume. Um tipo de órgão vivo — acrescentado, alterado ou apenas consultado — passa.

[?] O texto da recusa não está no material lido: a mensagem é pedida por número a uma rotina de
comunicação que não faz parte do acervo. Pergunta ao site.

### RN-18 — A digitação passa pela edição numérica, e o cursor volta ao campo recusado

**49 campos** da tela passam pela edição numérica antes de qualquer leitura — o grupo, as três
partes do início e as três do limite do cálculo, as três partes do início e as três do limite da
tabela de preços e as **36 datas dos seis períodos de exclusão**. Campo em branco vale zero; o
que não for número é recusado, a passagem não segue e o cursor volta ao campo recusado. A
impressora e o campo da resposta não são numéricos e não passam por essa edição.

[?] O que quem opera vê quando a digitação é recusada — se há mensagem, e qual — não está nos
fontes desta jornada: a rotina que faz a edição numérica é importada e não faz parte do acervo
lido. Pergunta ao site.

### RN-19 — Falha de banco interrompe a passagem e avisa

Todo acesso a dados testa o erro do banco; o erro de leitura e o de gravação viram avisos
diferentes, despachados pela rotina de comunicação — a passagem para ali, sem completar o resto.

---

## Cenários BDD

```gherkin
Funcionalidade: Registrar o cálculo da estimativa da alimentação escolar do grupo e encomendar o processamento

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C840T

  Cenário: Inclusão de um cálculo para o grupo e a data limite
    Dado que o grupo está cadastrado no meu tipo de órgão
    E que o período tem cardápio, planejamento, média de comensais, tabela de preços e letras da semana
    E que ainda não há cálculo registrado para o grupo naquela data limite
    Quando informo o grupo, a data limite, a data limite da tabela de preços e a impressora
    E confirmo o cálculo com S
    Então o cálculo do grupo é registrado para aquela data limite
    E o pedido do relatório de cálculo é registrado com o número seguinte da fila
    E o processamento é entregue à fila
    E vejo a mensagem "* Estimativa sendo calculada *"

  Cenário: O cálculo registrado deixa rastro na auditoria
    Dado que confirmo o cálculo do grupo com S
    Quando o cálculo é registrado
    Então vejo na auditoria um lançamento com a tela de origem, a operação de inclusão, a matrícula, a estação, a data e a hora
    E o lançamento guarda o que foi pedido e deixa em branco o valor posterior

  Cenário: O início do calendário e o início da tabela vêm dos cadastros
    Dado que o período tem cardápio e tabela de preços cadastrados
    Quando informo as datas e confirmo o cálculo com S
    Então o cálculo fica registrado com o início do cardápio e o início da tabela cadastrados
    E não com o início que eu tivesse digitado

  Cenário: Consulta do cálculo registrado do grupo
    Dado que existe um cálculo registrado para o grupo e a data limite
    Quando informo o grupo e a data limite e envio a consulta
    Então vejo as datas de vigência do calendário, as datas de vigência da tabela de preços e as datas dos seis períodos de exclusão
    E nenhum registro é incluído, alterado ou excluído
    E nenhum lançamento de auditoria é gerado

  Cenário: Consulta de um período sem cálculo registrado
    Dado que não existe cálculo para o grupo na data limite informada
    Quando envio a consulta
    Então vejo a mensagem "* Nao existe calc. estimativa para esta data *"
    E o cursor volta ao dia da data limite
    E nenhuma data é preenchida na tela

  Cenário: Operação diferente de inclusão e de consulta
    Dado que estou na tela C840T
    Quando informo uma operação que não é inclusão nem consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use INC ou CON *"
    E o cursor volta ao campo da operação
    E nenhum cadastro é lido nesse caminho

  Cenário: Grupo não cadastrado no meu tipo de órgão
    Dado que informo um grupo que não existe no cadastro de grupos do meu tipo de órgão
    Quando envio a inclusão
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo do grupo
    E nada é registrado

  Cenário: Já existe cálculo para o grupo e a data
    Dado que já existe um cálculo registrado para o grupo na data limite informada
    Quando envio a inclusão
    Então vejo a mensagem "* Ja existe estimativa calculada para esta data *"
    E o cursor volta ao dia da data limite
    E nenhum registro novo é gravado

  Cenário: Período sem cardápio
    Dado que não há cardápio vigente na data limite informada
    Quando envio a inclusão
    Então vejo a mensagem "* Nao existem cardapios neste periodo *"
    E o cursor volta ao dia da data limite
    E nada é registrado

  Cenário: Grupo sem planejamento no período
    Dado que o grupo não tem planejamento para a data limite informada
    Quando envio a inclusão
    Então vejo a mensagem "* Planejamento nao cadastrado *"
    E o cursor volta ao campo do grupo
    E nada é registrado

  Cenário: Período sem média de comensais
    Dado que o grupo não tem média de comensais para a data limite informada
    Quando envio a inclusão
    Então vejo a mensagem "* Media de comensais nao cadastrada *"
    E o cursor volta ao dia da data limite
    E nada é registrado

  Cenário: Período sem tabela de preços
    Dado que não há tabela de preços vigente na data limite da tabela informada
    Quando envio a inclusão
    Então vejo a mensagem "* Tabela de referencia nao cadastrada *"
    E o cursor volta ao dia da data limite da tabela
    E nada é registrado

  Cenário: Período sem letras da semana
    Dado que o grupo não tem letras da semana para o período
    Quando envio a inclusão
    Então vejo a mensagem "* Letras da semana nao cadastr. para o periodo *"
    E o cursor volta ao dia da data limite
    E nada é registrado

  Cenário: Período de exclusão com data inválida
    Dado que informo um período de exclusão com uma data que não existe
    Quando envio a inclusão
    Então vejo a mensagem "* Data inicial do periodo excluido invalida *" ou "* Data final do periodo excluido invalida *"
    E o cursor volta ao campo do período que falhou
    E nada é registrado

  Cenário: Período de exclusão com início depois do limite
    Dado que informo um período de exclusão cuja data de início é maior que a data de limite
    Quando envio a inclusão
    Então vejo a mensagem "* Data inicial maior que data final *"
    E o cursor volta ao campo do período que falhou
    E nada é registrado

  Cenário: Período de exclusão fora da janela do cálculo
    Dado que informo um período de exclusão que começa antes do início do calendário ou termina depois da data limite do cálculo
    Quando envio a inclusão
    Então vejo a mensagem "* Periodo de exclusao fora do limite de calculo *"
    E o cursor volta ao campo do período que falhou
    E nada é registrado

  Cenário: Período de exclusão em branco é ignorado
    Dado que deixo o dia de início de um dos seis períodos de exclusão zerado
    Quando envio a inclusão
    Então o sistema passa ao período seguinte sem reclamar

  Cenário: Impressora não informada
    Dado que deixo a impressora em branco
    Quando envio a inclusão
    Então vejo a mensagem "* Informe a impressora *"
    E o cursor volta ao campo da impressora
    E nada é registrado

  Cenário: A confirmação é pedida antes de registrar
    Dado que todas as conferências passaram
    Quando envio a inclusão
    Então vejo a mensagem "* Confirma calculo <S/N> ? *"
    E o cursor fica no campo da resposta
    E nesse passo nada é gravado

  Cenário: Resposta diferente de S
    Dado que a tela pediu a confirmação do cálculo
    Quando respondo outra coisa que não S
    Então o cálculo não é registrado
    E a tela volta a pedir a mesma confirmação

  Cenário: Campo alterado entre a confirmação e a resposta
    Dado que a tela pediu a confirmação do cálculo
    Quando altero qualquer campo e respondo S
    Então as conferências são refeitas desde o começo
    E a confirmação é pedida de novo

  Cenário: Pedido do mesmo relatório já na fila
    Dado que há um pedido do relatório de cálculo em processamento para o meu tipo de órgão
    Quando confirmo o cálculo com S
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da resposta
    E nem o cálculo, nem a auditoria, nem o pedido novo são registrados

  Cenário: Tipo de órgão da sessão excluído ou purgado
    Dado que o tipo de órgão da minha sessão está marcado como excluído ou como purgado
    Quando confirmo o cálculo com S
    Então vejo o aviso de erro padrão do sistema
    E a passagem é interrompida sem gravar

  Cenário: Digitação não numérica
    Dado que digito no grupo ou em uma das datas algo que não é número
    Quando envio a inclusão
    Então a passagem não segue antes de ler qualquer cadastro
    E o cursor volta ao campo recusado

  Cenário: Falha de banco durante a gravação
    Dado que o banco falha ao gravar o cálculo
    Quando confirmo o cálculo com S
    Então a passagem para e um aviso é despachado pela rotina de comunicação
```
