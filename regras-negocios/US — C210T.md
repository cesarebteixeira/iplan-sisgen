# US — C210T — Pedido de processamento da quinzena

## Estória

Como **servidor de CRE**, quero **pedir o processamento do relatório de uma quinzena —
normal ou especial — para uma impressora**, para que **o relatório daquele período seja
gerado e impresso sem depender de chamado ao suporte**.

O relatório da quinzena não roda sozinho: ele é gerado a pedido, e é o pedido que o coloca
na fila de processamento. A quinzena é a metade do mês — começa no dia 1 ou no dia 16 —, e
como o fim é sempre o fim da metade, quem pede informa só o começo: a secretaria não
depende de o operador acertar a data final. Enquanto houver um pedido do mesmo relatório
esperando processamento, o sistema recusa um segundo, para que o mesmo período não seja
impresso duas vezes. Sem esta tela, o relatório da quinzena não sai.

## Contexto

Jornada S000M → C000M → C015M → C210T.
Ator: servidor de CRE — pede o processamento do relatório da quinzena, informando o início
do período, o tipo de quinzena e a impressora.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O `C000M` e o `C015M` são menus: só encaminham, não gravam nada e não deixam dado de
negócio para esta tela. A opção que abre a `C210T` entrega o destino e mais nada — não
informa operação nem registro —, e esta tela não compara a origem com nada: ela abre igual,
venha do menu ou de qualquer outra tela, e é ela própria que fixa a operação ao se
apresentar (RN-01). O contexto de que ela se serve — a matrícula, o privilégio, o tipo de
órgão, a CRE, a estação e a data do sistema — é o que a entrada deixou na sessão; a tela
não o recalcula.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela só trabalha em alteração

A tela não oferece escolha de operação: ao ser apresentada, o sistema marca a operação como
**alteração**, e é essa operação que segue para as conferências de acesso. Se a mensagem do
operador chegar com outra operação no campo, o pedido é recusado com
* Opcao nao disponivel. Use ALT *, o cursor volta para o campo da operação e nada é lido
nem registrado.

[?] A recusa nomeia **ALT**, mas a conferência compara o que chegou com o código interno da
alteração; o texto da máscara não está no lote, de modo que a correspondência entre o que o
operador digita e o que a tela confere não pôde ser verificada. Pergunta ao site.

### RN-02 — O acesso à tela e a permissão de alteração são conferidos antes de registrar

Na abertura, o sistema confere que a estação da sessão é a estação registrada para a
matrícula, que a tela consta do cadastro de telas e que o código de acesso do servidor tem
esta tela. Faltando a tela no cadastro, o aviso é * Tela nao disponivel *; faltando no
código de acesso, a recusa é * Acesso negado para esta matricula * — e nos dois casos nada
é registrado. Ao confirmar o pedido, o sistema confere de novo o cadastro de telas — tela
retirada dele é recusada com * Tela nao cadastrada * — e, no código de acesso, a
autorização da operação de alteração: faltando, a recusa é
* Acesso negado para esta operacao *. As conferências recebem o contexto que a entrada
deixou na sessão: a matrícula, o código de acesso, o privilégio, a CRE, o tipo de órgão e a
estação.

### RN-03 — A quinzena começa no dia 1 ou no dia 16

O operador informa o início do período: dia, mês e ano. O dia tem de ser **1** ou **16** —
a quinzena é a metade do mês. Qualquer outro dia é recusado com * Dia invalido *, o cursor
volta para o dia do início e nada é registrado.

### RN-04 — A data inicial tem de ser uma data que existe

A data de início é conferida como data: o ano tem de estar entre **1994** e **2099** e o
dia tem de existir naquele mês e ano. Não existindo, a recusa é * Data inicial invalida *,
com o cursor no dia do início e sem nada registrado.

### RN-05 — O fim do período é calculado pelo sistema

A tela mostra o início e o limite do período, mas o **limite é do sistema**: começando a
quinzena no dia **1**, o limite é o dia **15** do mesmo mês e ano; começando no dia **16**,
o limite é o **último dia daquele mês** (28, 29, 30 ou 31, conforme o mês). Os campos do
limite voltam preenchidos com o que o sistema calculou — o que for digitado neles é
substituído.

[?] A máscara pode deixar o operador digitar o limite (os seis campos do período são
tratados como campos de entrada), mas o sistema os substitui pelo cálculo; se o operador
espera que o que ele digitou seja respeitado, o comportamento é outro. Pergunta ao site.

[?] O último dia do mês é alcançado partindo do primeiro dia do mês seguinte e recuando um
dia. A leitura do recuo vem dos parâmetros que a rotina de data recebe e das duas telas
irmãs que usam a mesma sequência; a rotina em si está declarada como procedimento de
biblioteca e o corpo não veio no lote. Confirmar no site se o limite é o último dia do
período ou o primeiro dia fora dele.

### RN-06 — A quinzena tem de ser informada como normal ou especial

O operador informa a indicação da tabela quinzena: **N** para normal ou **E** para
especial. Qualquer outro valor — inclusive em branco — é recusado com
* Informe Quinzena com N=Normal ou E=Especial *, o cursor volta para a indicação e nada é
registrado.

[?] O que distingue a quinzena especial é o relatório que é processado (o `C21104` em lugar
do `C21103`), com o mesmo período. Se a diferença está na tabela de preços aplicada, o
material desta jornada não diz. Pergunta ao site.

### RN-07 — Sem impressora não há pedido

A impressora é obrigatória: em branco, a recusa é * Informe a impressora *, com o cursor na
impressora e nada registrado.

[?] A tela exige apenas que a impressora esteja preenchida: não confere se ela está
cadastrada. Se o código deveria apontar para uma impressora conhecida, esta tela não o
verifica. Pergunta ao site.

### RN-08 — O pedido só é registrado depois da confirmação

Passadas as conferências, o sistema apresenta
* Confirma atualizacao da quinzena <S/N> ? * e espera. Somente a resposta **S** prossegue.
A resposta **N** não cancela nem registra: o sistema limpa a resposta e volta a pedir a
confirmação. Se a data de início for alterada entre a pergunta e a resposta, a confirmação
é descartada e a tela revalida tudo antes de perguntar de novo.

[?] Pelo programa, a única saída da pergunta é responder **S**: com **N** o fluxo volta à
validação e à própria pergunta. Se o operador abandona a tela, é por uma tecla tratada fora
do programa, o que não foi possível determinar. Pergunta ao site.

### RN-09 — Um relatório já na fila bloqueia pedido novo

Antes de registrar, o sistema verifica se já existe pedido daquele relatório na fila de
requisições de impressão. Existindo, a resposta é
* Relatorio em processamento. Aguarde. * e **nada é registrado**. A conferência é por
relatório, e o pedido sai da fila quando o relatório roda — o próprio processamento apaga
os pedidos que atende.

[?] A leitura da fila posiciona o código do relatório e deixa os demais componentes da
chave em branco ou zerados; se ela alcança qualquer pedido daquele relatório ou exige a
chave inteira é o que os sinalizadores da leitura dizem, e o dialeto não está explicado no
corpus. Pergunta ao site.

### RN-10 — Confirmado, o pedido é registrado e o relatório é processado

Confirmada a atualização, o sistema registra **um pedido** na fila com o **número
seguinte** ao último pedido, o relatório da quinzena (`C21103` para a normal, `C21104`
para a especial), a impressora, o dia, o mês e o ano do sistema, a matrícula, a estação e o
tipo de órgão; e entrega o processamento do relatório com o período informado e o e-mail
do servidor, lido do cadastro de funcionários. A tela então mostra
* Cadastro sendo atualizado *.

[?] O período, a impressora e o e-mail viajam na mensagem de disparo do processamento, não
no pedido registrado: o registro guarda o relatório, a impressora, o número, as datas e os
identificadores, mas não o período. Como o processamento recebe o período não fecha só com
o material desta jornada. Pergunta ao site.

[?] O número do pedido é o último número da fila mais um; quando a fila está vazia, o
sistema apenas marca que não achou, sem limpar a área lida — e a contagem pode repetir um
número já usado. Pergunta ao site.

### RN-11 — A tela não altera nem exclui cadastro nenhum e não deixa auditoria

A tela enxerga o cadastro de telas, o cadastro de funcionários e a fila de requisições de
impressão, mas a **única gravação** que executa é a do pedido na fila. Nenhum registro é
alterado ou excluído e a operação não deixa rastro de auditoria. Consulta pura também não
é: o que a tela faz é registrar o pedido e disparar o relatório.

### RN-12 — A tela não encaminha para outra: ela reabre a si mesma

A tela não entrega o serviço a outra tela. Depois de apresentar a pergunta de confirmação e
depois de registrar o pedido, ela reabre a si mesma, com o período informado e a operação
de alteração, e é nela que a jornada termina.

[?] A máscara tem um campo de "próxima tela" que, se vier preenchido, leva a sessão para a
tela ali indicada em vez de reabrir esta; nenhum ponto do material desta jornada o
preenche. Se algum caminho do sistema o preenche, o desfecho é outro. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Pedido de processamento da quinzena

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C210T

  Cenário: RN-01 — a tela abre pronta para a alteração
    Quando a tela C210T é apresentada
    Então a operação já vem marcada como alteração
    E nada foi registrado

  Cenário: RN-01 — operação diferente de alteração é recusada
    Dado que a mensagem chega com a operação diferente de ALT
    Quando a tela processa o pedido
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E o cursor volta para o campo da operação
    E nada é registrado

  Cenário: RN-02 — sem autorização para a operação de alteração
    Dado que a minha matrícula tem a tela C210T, mas o meu código de acesso não tem a autorização de alteração
    Quando confirmo o pedido
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é registrado

  Cenário: RN-02 — sem a tela no meu código de acesso
    Dado que o meu código de acesso não tem a tela C210T
    Quando abro a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E nada é registrado

  Cenário: RN-02 — tela fora do cadastro de telas
    Dado que a tela C210T não consta do cadastro de telas
    Quando abro a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E nada é registrado

  Cenário: RN-02 — tela retirada do cadastro de telas
    Dado que a tela C210T foi retirada do cadastro de telas
    Quando confirmo o pedido
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é registrado

  Cenário: RN-03 — dia de início diferente de 1 e de 16 é recusado
    Dado que informo o início do período em um dia diferente de 1 e de 16
    Quando peço o processamento
    Então vejo a mensagem "* Dia invalido *"
    E o cursor volta para o dia do início
    E nada é registrado

  Cenário: RN-04 — data inicial que não existe é recusada
    Dado que informo um início de período com dia ou mês que não existem
    Quando peço o processamento
    Então vejo a mensagem "* Data inicial invalida *"
    E o cursor volta para o dia do início
    E nada é registrado

  Cenário: RN-05 — começando no dia 1, o limite é o dia 15
    Dado que informo o início do período no dia 1
    Quando a tela calcula o período
    Então o limite fica no dia 15 do mesmo mês e ano

  Cenário: RN-05 — começando no dia 16, o limite é o último dia do mês
    Dado que informo o início do período no dia 16
    Quando a tela calcula o período
    Então o limite fica no último dia daquele mês

  Cenário: RN-06 — quinzena não informada é recusada
    Dado que informo o início do período e deixo a indicação da quinzena em branco, ou com valor diferente de N e de E
    Quando peço o processamento
    Então vejo a mensagem "* Informe Quinzena com N=Normal ou E=Especial *"
    E o cursor volta para a indicação da quinzena
    E nada é registrado

  Cenário: RN-07 — impressora não informada é recusada
    Dado que informo o início do período e a quinzena, e deixo a impressora em branco
    Quando peço o processamento
    Então vejo a mensagem "* Informe a impressora *"
    E o cursor volta para a impressora
    E nada é registrado

  Cenário: RN-08 — a pergunta de confirmação não registra nada
    Dado que informei um período válido, a quinzena e a impressora
    Quando a tela confere os dados
    Então vejo a mensagem "* Confirma atualizacao da quinzena <S/N> ? *"
    E nada foi registrado na fila de requisições

  Cenário: RN-08 — resposta N não registra e a pergunta volta
    Dado que estou na pergunta de confirmação
    Quando respondo N
    Então o sistema limpa a resposta, revalida os dados e pergunta de novo
    E nada é registrado na fila de requisições

  Cenário: RN-08 — data de início alterada depois da pergunta descarta a confirmação
    Dado que estou na pergunta de confirmação
    Quando altero a data de início e respondo S
    Então o sistema revalida o período antes de aceitar a resposta
    E nada é registrado sem a nova confirmação

  Cenário: RN-09 — relatório já na fila é recusado
    Dado que já existe um pedido daquele relatório esperando processamento
    Quando respondo S à pergunta de confirmação
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E nada é registrado na fila de requisições

  Cenário: RN-10 — pedido da quinzena normal é registrado e processado
    Dado que informei o dia 1, a quinzena N e a impressora
    Quando respondo S à pergunta de confirmação
    Então o sistema registra o pedido com o número seguinte da fila, o relatório C21103, a impressora, a data do sistema, a minha matrícula e a estação
    E entrega o relatório daquele período ao processamento
    E vejo a mensagem "* Cadastro sendo atualizado *"

  Cenário: RN-10 — pedido da quinzena especial usa o outro relatório
    Dado que informei a quinzena E
    Quando respondo S à pergunta de confirmação
    Então o pedido registrado é o do relatório C21104
    E o período informado é o mesmo da quinzena normal

  Cenário: RN-11 — a tela não grava mais nada
    Dado que registrei um pedido
    Quando a tela termina a operação
    Então a única gravação foi a do pedido na fila de requisições
    E nenhum cadastro foi alterado ou excluído
    E nenhum rastro de auditoria foi deixado

  Cenário: RN-12 — a tela reabre a si mesma
    Dado que registrei o pedido
    Quando a tela termina
    Então ela reabre a si mesma com o período informado e a operação de alteração
    E não encaminha para outra tela
```
