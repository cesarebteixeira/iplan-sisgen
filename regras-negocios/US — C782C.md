# US — C782C — Consultar a auditoria dos cardápios e planejamentos

## Estória

Como **servidor de CRE**, quero **ver quem alterou os cardápios e os planejamentos
do meu órgão, quando e em que registro, e pedir a listagem da auditoria de um
dia**, para que **eu saiba o que mudou na alimentação escolar e possa levar a
auditoria para conferência sem procurar a alteração registro a registro**.

Toda alteração feita num cardápio ou num planejamento deixa um registro de
auditoria com a data e a hora da sessão, a matrícula de quem a fez e o registro
tocado. Esta é a tela que reúne esses registros numa lista legível e que permite
pedir a listagem numa impressora. Sem ela, quem precisa apurar uma alteração teria
de procurá-la registro a registro, sem lista e sem relatório.

## Contexto

Jornada S000M → C000M → C070M → C782C.

Ator: servidor de CRE — consulta a auditoria das alterações de cardápio e de
planejamento do seu órgão e, informando a impressora, pede o relatório da
auditoria de um dia.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e
menus.md`: é **dado de navegação**, não regra de negócio.

O C000M e o C070M são telas de encaminhamento: não gravam nada e entregam à C782C
o que a sessão já trazia — a matrícula, o tipo de órgão, a coordenação regional, o
código de acesso e a estação. A C070M encadeia a C782C sem passar por menu, e a
C782C também se abre pelo código de transação dela; por isso a sessão que a tela
mostra e o modo com que ela abre são regra daqui, e não regra da entrada. A
jornada termina nesta tela: a C782C não encadeia para outra, e o que ela entrega é
o pedido do relatório ao serviço de relatórios.

## Regras de negócio

### RN-01 — A tela só consulta: não altera cadastro nem auditoria

A C782C é de consulta. Ela lê a auditoria, o cadastro de telas, o cadastro do
funcionário e a fila de requisições de impressão; não inclui, não altera e não
exclui cardápio, planejamento nem registro de auditoria — e, como não grava,
também não deixa rastro na auditoria. As rotinas de gravar, de excluir e de
travar existem declaradas para cada cadastro que a tela enxerga, mas só o pedido
do relatório é executado: declarar não é executar.

### RN-02 — A lista tem até 14 linhas, uma por sessão de auditoria

A auditoria guarda **um registro por campo alterado**, com a operação, o valor
anterior e o novo, a data e a hora da sessão, a matrícula de quem alterou e o
registro tocado; são **19 campos** por registro, e a capacidade declarada do
cadastro é de **1.000.000** de registros — capacidade é o máximo esperado,
parâmetro de dimensionamento, não o que está cadastrado.

A tela apresenta até **14 linhas**, e cada linha é uma **sessão de auditoria**,
não um registro. A linha traz a **data** e a **hora** em que a alteração foi
registrada, a **matrícula** e o **nome** de quem a fez, o **módulo de origem**
(RN-03) e a **identificação do registro auditado**. A data sai no formato
dia/mês/ano e a hora no formato hora:minuto:segundo. A identificação é montada por
partes — o código do cardápio, a coordenação regional, a letra da semana e o
segmento —, e cada parte só aparece quando o registro a tem; as que faltam ficam
em branco.

Os vários registros gravados numa mesma sessão cabem numa linha só: a tela não
repete a sessão. A ordem é a da sessão — ano, mês, dia, hora e campo alterado —,
e a leitura é um ponto de partida, não um filtro: começada numa sessão, a lista
segue até o fim da auditoria do órgão. A linha é montada com o registro de
auditoria que abre aquela sessão. O nome vem do cadastro de funcionários, pela
matrícula que está no próprio registro de auditoria; não achando o funcionário, a
linha aparece sem o nome e nada é recusado. A lista é remontada a cada
confirmação, e os campos de resultado — a descrição do órgão, a data do sistema e
tudo o que as linhas mostravam — são apagados antes de ela ser montada.

[?] Como a tela resume a sessão em uma única linha, os demais registros de
auditoria daquela sessão não aparecem um a um — só o primeiro. Se a intenção é
que o detalhe saia apenas no relatório, o acervo desta jornada não diz. Pergunta
ao site.

[?] A leitura avança de registro em registro pelo mesmo conjunto, mas os
sinalizadores de posicionamento vêm de biblioteca sem fonte no lote: se a segunda
leitura da página é a leitura seguinte do mesmo conjunto, o descarte dos registros
da mesma sessão vale como descrito; se for uma nova leitura posicionada, a página
repetiria a mesma linha. Os dois comportamentos não se distinguem pelo que o
fonte mostra. Pergunta ao site.

### RN-03 — "Cardapio" ou "Planejamento": quem decide é a origem da alteração

O registro de auditoria guarda a tela que o originou, e a C782C confere essa
origem ao montar cada linha. Vindo a alteração da tela do **planejamento**
(`C770T`), a linha é descrita como **Planejamento**; vindo de qualquer outra
origem, como **Cardapio**. Na prática, quem altera pelo cadastro do cardápio
(`C070T` e as telas do módulo) grava a origem do cardápio, e quem altera pelo
planejamento (`C770T`) grava a origem do planejamento.

A origem não muda mais nada nesta tela: o modo com que ela abre, a operação aceita
e as leituras são os mesmos para as duas procedências. O que se nota é o conteúdo
da identificação: as linhas do cardápio trazem o código do cardápio e, quando a
alteração foi por segmento, o segmento; as do planejamento trazem a coordenação
regional, a letra da semana e o segmento.

[?] A identificação mostra, numa posição, uma marca de um caractere que a tela do
planejamento preenche e as do cardápio deixam em branco; o dicionário desta
jornada não diz o que ela significa — a leitura de que é a letra da semana vem das
telas irmãs. Pergunta ao site.

### RN-04 — A lista é a da sessão e do órgão do servidor; sessão sem auditoria é avisada

A consulta é sempre dentro do **tipo de órgão da sessão**, e a varredura termina
quando os registros daquele órgão acabam: auditoria de outro órgão não aparece,
ainda que exista. O servidor pode informar o dia, o mês, o ano, a hora, o minuto e
o segundo de uma sessão, e a lista começa nela.

Não havendo auditoria para mostrar, o sistema avisa
**\* Cardapios/Planejamentos sem auditoria \*** e nenhuma linha é preenchida. O
aviso é decidido na montagem da **primeira linha** da página e não é repetido nas
demais.

[?] O aviso é decidido uma única vez, na montagem da primeira linha, e não é
recalculado depois: quando a auditoria do órgão acaba antes de a página completar,
as linhas restantes ficam em branco sem nenhum aviso. Se é o pretendido, o acervo
não diz. Pergunta ao site.

[?] A sessão com que a tela abre vem da área de trabalho compartilhada da
transação, que é a mesma que as telas anteriores usam; o acervo não mostra se a
passagem pela C070M sempre deixa uma sessão ali. Se não deixar, a abertura cai no
aviso de sessão sem auditoria e o servidor precisa informar a sessão. Pergunta ao
site.

### RN-05 — Só a consulta passa; as outras operações são recusadas

A abertura repõe a operação como **consulta**. Se a tela chegar com outra operação
— informada ou trazida por quem a encadeou —, a confirmação recusa com
**\* Operacao nao disponivel. Use CON \*** e devolve o cursor ao campo da
operação, sem ler e sem gravar nada nesse caminho. Uma operação que não seja
inclusão, alteração, exclusão nem consulta é recusada antes disso, pelo
roteamento, com **\* Operacao nao disponivel \***.

[?] A mensagem manda usar "CON", mas a tela confere a operação contra o código
interno de consulta do sistema, e nenhum valor "CON" existe no acervo lido. Ou o
formulário traduz o que o servidor digita, ou quem seguir a mensagem é recusado.
Além disso, como a abertura repõe a consulta sozinha, essa recusa só é alcançada
numa mensagem seguinte do servidor — e só se o formulário lhe oferecer o campo da
operação. Pergunta ao site.

### RN-06 — A data e a hora informadas são editadas como número; em branco vale zero

Os **nove** campos informados como número — o dia, o mês, o ano, a hora, o minuto
e o segundo da sessão, e o dia, o mês e o ano da data de auditoria do relatório —
passam por edição numérica antes de qualquer leitura: campo em branco é tratado
como zero, o que não for número é recusado e a consulta não segue, e o cursor volta
ao campo recusado, na ordem em que a tela os confere. O campo da impressora é
texto e não passa por essa edição.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual —
não está nos fontes desta jornada: a rotina que faz a edição é importada e não tem
fonte no lote. Pergunta ao site.

[?] A tela não confere se o dia existe no mês informado, em nenhum dos dois grupos
de data; se alguém faz essa conferência fora da tela, o acervo lido não mostra.
Pergunta ao site.

### RN-07 — Preenchido o campo de próxima tela, a tela encaminha e não faz mais nada

O campo de próxima tela é o que faz uma tela passar o servidor para outra sem
passar por menu nenhum. Chegando preenchido, o roteamento do sistema leva o
servidor à tela indicada e a confirmação da C782C termina ali: ela não confere a
operação, não confere o pedido de relatório e não lê auditoria nenhuma.

[?] O campo de próxima tela faz parte do registro da tela, mas não tem rótulo na
ficha da C782C; se ele é visível e digitável pelo servidor, ou se só a tela que a
chamou o preenche, o acervo não mostra. Pergunta ao site.

### RN-08 — O código de impressão pede o relatório da auditoria; sem ele, a tela só consulta

A impressora é o que pede o relatório. Em branco, a confirmação não registra
pedido nenhum e a tela só lê a auditoria e mostra a lista.

Informado um código de impressão junto com a data de auditoria — dia, mês e ano —,
a tela monta o pedido do relatório de auditoria e o entrega ao serviço de
relatórios. O pedido leva o código do relatório, o código de impressão, uma
cópia, a estação e a matrícula do servidor, o endereço de correio do cadastro do
funcionário, a data de auditoria informada, a data do sistema e o tipo de órgão da
sessão; o número do pedido é o seguinte ao último pedido registrado na fila. O
relatório é o que detalha a auditoria do dia: a lista da tela mostra até 14
sessões, e o relatório traz o que elas contêm.

[?] O número do pedido é o último número da fila mais um; quando a fila está
vazia, o sistema apenas marca que não achou o último pedido, sem limpar a área
lida, e o número pode repetir um já usado. Se existe um caminho que garanta a
limpeza, não está nos fontes desta jornada. Pergunta ao site.

[?] A tela não emite mensagem própria de sucesso: as mensagens do programa são as
recusas e o aviso de lista vazia. O que o servidor vê depois de registrar o
pedido, se a entrega ao processamento devolve algum aviso, não está nos fontes
desta jornada. Pergunta ao site.

### RN-09 — O pedido é recusado com o relatório em processamento ou com a data sem auditoria

Antes de registrar o pedido, a tela faz duas conferências, e cada uma tem a sua
recusa, com o cursor no campo que a provocou:

- havendo **pedido do mesmo relatório já em processamento** para o tipo de órgão
  da sessão, a recusa é **\* Relatorio em processamento. Aguarde. \*** e o cursor
  volta ao campo da impressora. A conferência é por tipo de órgão e relatório, e
  o pedido é registrado **sem coordenação regional**: como a conferência também
  não distingue a coordenação, o pedido de uma coordenação bloqueia o das outras
  do mesmo órgão;
- **não havendo registro de auditoria para a data informada** no tipo de órgão da
  sessão, a recusa é **\* Data sem registros de auditoria \*** e o cursor volta ao
  dia da data de auditoria.

[?] A conferência da data informada procura a auditoria do dia com a hora zerada e
o campo auditado em branco; se essa leitura alcança qualquer registro do dia ou
exige essa combinação exata, o acervo desta jornada não mostra. Se exigir a hora
zero, nenhuma data teria registro e todo pedido seria recusado. Pergunta ao site.

[?] As duas recusas são emitidas numa passagem de conferência da tela, e o
registro do pedido acontece numa passagem posterior, que não reconfere nem a fila
nem a data. O que impede o registro nesse caminho é a marca de aborto da
transação, e a rotina que emite a mensagem não tem fonte no lote: se ela também
aborta a transação, as recusas valem e nada é registrado; se não, o pedido entra
na fila apesar do aviso. Não se escolhe um dos dois. Pergunta ao site.

### RN-10 — A tela mostra a data do sistema e a descrição do tipo de órgão da sessão

Fora da lista, a tela exibe a **data do sistema** e a **descrição do tipo de
órgão** da sessão, cada uma em dez posições.

### RN-11 — Ao abrir a tela o sistema confere o acesso; na confirmação, confere a operação

Ao abrir, a tela confere o acesso do servidor ao cadastro de telas antes de ler
qualquer auditoria; na confirmação, confere a rota e, depois, a permissão de
operação do código de acesso. Tela não cadastrada sai
**\* Tela nao cadastrada \***; tela fora do quadro de telas liberadas para o
código de acesso sai **\* Tela nao disponivel \***; par de código de acesso e tela
não autorizado sai **\* Acesso negado para esta matricula \***; operação não
permitida ao código de acesso sai **\* Acesso negado para esta operacao \***.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar a auditoria dos cardápios e planejamentos

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C782C

  Cenário: Consulta da auditoria do meu órgão
    Dado que o meu órgão tem alterações de cardápios e planejamentos registradas
    Quando abro a tela C782C
    Então vejo as sessões em linhas, cada uma com a data, a hora, a matrícula, o nome, o módulo de origem e a identificação do registro auditado
    E a data sai no formato dia/mês/ano e a hora no formato hora:minuto:segundo

  Cenário: A lista mostra no máximo 14 sessões
    Dado que o meu órgão tem mais de catorze sessões de alteração para mostrar
    Quando abro a tela C782C
    Então a lista mostra catorze linhas
    E as linhas restantes ficam em branco

  Cenário: A lista traz uma linha por sessão de alteração
    Dado que a mesma sessão alterou vários campos do mesmo cadastro
    Quando abro a tela C782C
    Então aquela sessão aparece uma única vez na lista
    E os demais registros daquela mesma sessão não aparecem um a um

  Cenário: A lista começa pela sessão informada
    Dado que informo o dia, o mês, o ano, a hora, o minuto e o segundo de uma sessão
    Quando confirmo a consulta
    Então a lista parte daquela sessão
    E segue adiante até o fim da auditoria do meu órgão

  Cenário: A lista é a do meu órgão
    Dado que há auditoria de cardápios de outro órgão
    Quando abro a tela C782C
    Então nenhuma alteração de outro órgão aparece na lista

  Cenário: Cada linha diz se a alteração foi num cardápio ou num planejamento
    Dado que a alteração foi feita pelo cadastro do cardápio
    Quando consulto a sessão em que ela foi feita
    Então a linha é descrita como "Cardapio"
    E a identificação traz o código do cardápio

  Cenário: Linha de auditoria vinda do planejamento
    Dado que a alteração foi feita pelo planejamento
    Quando consulto a sessão em que ela foi feita
    Então a linha é descrita como "Planejamento"
    E a identificação traz a coordenação regional, a letra da semana e o segmento

  Cenário: Sem auditoria para mostrar
    Dado que o meu órgão não tem nenhum registro de auditoria
    Quando abro a tela C782C
    Então vejo a mensagem "* Cardapios/Planejamentos sem auditoria *"
    E nenhuma linha da lista é preenchida

  Cenário: Operação diferente da consulta
    Dado que estou na tela C782C
    Quando informo uma opção diferente da consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta para o campo da opção
    E nenhum registro de auditoria é lido nem gravado nesse caminho

  Cenário: Operação fora das quatro do sistema
    Dado que a tela chega com uma operação que não é inclusão, alteração, exclusão nem consulta
    Quando confirmo
    Então vejo a mensagem "* Operacao nao disponivel *"

  Cenário: Digitação não numérica na data ou na hora
    Dado que digito no dia, no mês, no ano, na hora, no minuto ou no segundo algo que não é número
    Quando envio a consulta
    Então o sistema recusa a digitação antes de ler qualquer registro de auditoria
    E o cursor volta ao campo recusado

  Cenário: Encaminhamento pela próxima tela
    Dado que a tela chega com o campo de próxima tela preenchido
    Quando confirmo
    Então o sistema me leva à tela indicada
    E a C782C não confere operação nem pedido de relatório
    E nada é gravado

  Cenário: A data do sistema e a descrição do tipo de órgão da sessão
    Dado que entrei no sistema
    Quando abro a tela C782C
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: O resultado da consulta anterior não fica na tela
    Dado que já abri a tela e ela mostrou alterações
    Quando volto a consultar
    Então a data, a hora, a matrícula, o nome, o módulo e a identificação da consulta anterior não ficam na tela

  Cenário: Sem a impressora, a tela só consulta
    Dado que deixo o campo da impressora em branco
    Quando envio a consulta
    Então vejo a lista de auditoria
    E nenhum pedido de relatório é registrado

  Cenário: Pedido do relatório da auditoria de um dia
    Dado que informo uma data com registros de auditoria e a impressora
    Quando envio o pedido
    Então um pedido do relatório da auditoria daquela data entra na fila de requisições de impressão
    E o pedido leva o número seguinte ao último da fila
    E o relatório é entregue ao processamento com o meu correio eletrônico

  Cenário: Relatório já em processamento
    Dado que já existe um pedido daquele relatório na fila para o meu órgão
    Quando informo a impressora e envio o pedido
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta para o campo da impressora
    E nenhum pedido é registrado

  Cenário: Data sem registros de auditoria
    Dado que informo a impressora e uma data sem nenhum registro de auditoria
    Quando envio o pedido
    Então vejo a mensagem "* Data sem registros de auditoria *"
    E o cursor volta para o campo do dia da data de auditoria
    E nenhum pedido é registrado

  Cenário: A consulta não grava nada
    Dado que abro a tela C782C com o campo da impressora em branco
    Quando a lista é mostrada
    Então nenhum cardápio, nenhum planejamento e nenhum registro de auditoria é incluído, alterado ou excluído
    E nenhum registro de auditoria novo é gerado pela tela

  Cenário: Recusa quando a tela não está cadastrada
    Dado que a tela C782C não está no cadastro de telas
    Quando abro a tela
    Então o sistema recusa com "* Tela nao cadastrada *"

  Cenário: Recusa de acesso, quando a tela não está liberada
    Dado que a tela C782C não está liberada para o meu código de acesso
    Quando abro a tela
    Então o sistema recusa com "* Tela nao disponivel *"

  Cenário: Recusa quando o meu código de acesso não está autorizado na tela
    Dado que o par do meu código de acesso com a tela C782C não está autorizado
    Quando abro a tela
    Então o sistema recusa com "* Acesso negado para esta matricula *"

  Cenário: Recusa de operação não permitida ao meu código de acesso
    Dado que o meu código de acesso não permite a operação informada
    Quando confirmo
    Então o sistema recusa com "* Acesso negado para esta operacao *"
```
