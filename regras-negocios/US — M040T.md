# US — M040T — Manter o dia do mapa por grupo de atendimento do órgão filho

## Estória

Como **servidor da CRE**, quero **escolher o dia do mapa de um órgão filho e
registrar, para aquele dia, o grupo de atendimento, o cardápio e as quantidades de
cada refeição e a justificativa**, para que **cada dia do mês fique com o
atendimento que a secretaria prestou — quem foi atendido, o que foi servido e por
que não houve atendimento quando não houve**.

O mapa do dia é a peça que fecha o mês do órgão: é dela que saem, dia a dia, o
grupo de atendimento servido, o cardápio e as quantidades, e é por ela que a
merenda do mês pode ser conferida. Sem o dia registrado, o mês fica com buracos e
não há número que se sustente. Esta tela é também por onde o mês anda: ao incluir
um dia, ela fecha o dia que estava aberto, para que os dias sigam em ordem.

## Contexto

Jornada S000M → M000M → M040T.
Ator: servidor de CRE — escolhe o dia do mapa de um órgão filho da sua
coordenadoria regional escolar e registra, naquele dia, o grupo de atendimento, as
refeições e a justificativa.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O `M000M` é um menu e não grava
nada: apenas encaminha. O contexto que a `M040T` usa — o órgão filho do vínculo, a
coordenadoria, a secretaria e o tipo de órgão — é o que a entrada deixou na sessão.
As conferências de tela, de estação, de rota e de permissão que a `M040T` executa
antes de aceitar a operação são as mesmas de todas as telas e já estão no documento
da entrada: ficam no anexo de evidências, em **Regras que se revelaram da entrada**.
A `M040T` não termina a jornada: ela encadeia em três telas de cadastro e nas duas
telas do dia (a do dia anterior e a do dia seguinte); o que ela entrega a cada uma
está na RN-17.

---

## Regras de negócio

### RN-01 — O que a tela mantém, e o que cada operação grava

A `M040T` é a tela do **dia** do mapa do órgão filho: ela **consulta, inclui,
altera e exclui** o dia. Consultar mostra o dia — o grupo de atendimento e o seu
segmento, o cardápio e as quantidades de cada refeição do grupo, a justificativa do
dia e a do grupo, os grupos de atendimento do dia, a situação do dia (aberto ou
fechado), a semana, o dia da semana e o período do mês.

A **inclusão** registra o dia: grava o cardápio e as quantidades de cada refeição
do grupo, a justificativa do grupo e, quando ainda não existe, o próprio registro
do dia; ao incluir um dia, ela também **fecha o dia que estava aberto antes dele e
o perfil do mês**. A **alteração** regrava o que mudou e apaga o que saiu. A
**exclusão apaga de fato**, não marca: o registro do dia, o cardápio e as
quantidades e a justificativa do grupo são removidos do cadastro, um a um. Quando a
alteração deixa o dia sem nenhuma refeição e sem nenhuma justificativa, o registro
do dia também vai embora.

Dos **22 cadastros que o programa enxerga**, os 22 declaram gravação, mas só
**seis** chegam a receber alguma por esta tela: o registro do dia, o cardápio e as
quantidades, a justificativa do grupo, a situação do perfil do mês, a auditoria e a
solicitação de arquivo (RN-19). A consulta só pode gerar a solicitação de arquivo.

[?] A recusa mostra a mensagem e encerra a passagem, mas quem decide se a passagem
de gravação roda depois é o marcador de erro do sistema, e a rotina comum que
mostra a mensagem não está no acervo. Se ela não marcar o erro, a gravação pode
acontecer apesar da recusa. Pergunta ao site.

[?] O registro do dia só é criado quando já há o que registrar nele — uma refeição
do grupo ou uma justificativa. Não há, no fonte, caminho que crie um dia vazio, e
não se sabe se um dia sem nenhuma refeição e sem justificativa deve existir.
Pergunta ao site.

### RN-02 — O órgão tem de ser o do servidor e estar apto

Antes de qualquer operação, a tela confere o **órgão filho**: se é o do vínculo do
servidor — senão * Usuario sem acesso a outro orgao *; se está cadastrado —
* Orgao nao cadastrado *; se está ativo — * Orgao cadastrado como inativo *; se
tem os dados completos (bairro, órgão pai, nome, endereço, matriculados e pessoas)
— * Orgao cadastrado com dados incompletos *; se é da secretaria da sessão —
* Orgao nao pertence a esta secretaria *; e se o servidor tem acesso à
coordenadoria regional do órgão — <- Usuario sem acesso ao grupo deste orgao *.
Sem órgão informado, a tela pede * Informe o orgao *. A conferência do órgão não
olha se ele é creche: o que a tela faz com a creche é encaminhar o dia para outra
tela de mapa (RN-17).

### RN-03 — A operação tem de ser inclusão, alteração, exclusão ou consulta

O dia só é processado numa dessas quatro operações; qualquer outra é recusada com
* Operacao nao disponivel *, com o cursor de volta no campo da operação. Trocar a
operação para inclusão ou para consulta **limpa o dia e o que dele depende** — a
data, o grupo de atendimento, o segmento e a refeição —, para que o dia que se
estava vendo não se misture com o dia que se vai abrir.

### RN-04 — A data do mapa tem de ser válida e não pode ser posterior a hoje

A data do dia tem de ser uma **data válida**: ano entre 1994 e 2099 e dia e mês
existentes. Informada uma data impossível, a recusa é * Data invalida *; e, quando
o servidor pediu o dia anterior ou o dia seguinte sem informar a data, * Data
Invalida *. A data **não pode ser posterior à data de hoje**: * Data do mapa maior
que data atual *. O dia pedido como **dia novo** também não pode ser posterior a
hoje: * Novo dia maior que data atual *.

[?] O corte de agosto de 2008 é uma data de oito dígitos com o dia zero
(20080800): na prática, a tela deixa de encaminhar o dia para as telas do dia de 1º
de agosto de 2008 em diante. Se a intenção era outro dia-limite, o número não a
expressa. Pergunta ao site.

### RN-05 — A inclusão exige um dia sem mapa e um mês com perfil

A inclusão só vale para um dia que **ainda não tem mapa**: havendo, a recusa é
* Mapa ja cadastrado para esta data *. E o **mês de referência tem de ter perfil
cadastrado para o órgão**: não havendo, a recusa é
* Perfil nao cadastrado para este mes/ano * — e, na consulta em que o mês não tem
perfil, a tela avisa * Cadastrar perfil * e devolve o cursor ao campo do perfil,
que abre o cadastro do perfil do mês (RN-17).

### RN-06 — Alterar e excluir exigem ter consultado aquele mesmo dia

Para **alterar** ou **excluir**, o servidor precisa ter **consultado antes aquele
mesmo dia** — o mesmo órgão e a mesma data — nesta sessão. Não tendo, a recusa é
* Consulte antes de alterar * ou * Consulte antes de excluir *, conforme a
operação.

### RN-07 — Só se altera ou exclui o dia aberto

Só se altera ou exclui um dia **aberto**. Estando o dia fechado, a recusa é
* Mapa fechado para esta data * e nada é gravado. A inclusão não faz essa
conferência: é ela que abre o dia novo e fecha o anterior.

### RN-08 — O período e a semana do dia vêm dos cadastros do órgão

O **período** mostrado — dia, mês e ano de início e de limite — é o que a tabela de
períodos do mapa registra para o mês e o ano de referência. A **semana** do dia
(A, B, C ou D) é a que o calendário de semanas do órgão define para aquela data: a
tela a preenche e não a pergunta. A tela mostra ainda se o órgão está cadastrado
como creche (Sim ou Não) e se o dia está aberto ou fechado.

### RN-09 — O grupo de atendimento e o segmento do dia têm de estar cadastrados

O **grupo de atendimento** informado tem de constar do cadastro de grupos do órgão
— senão * Grupo de atendimento nao cadastrado * — e tem de estar cadastrado **para
aquele órgão** — senão * Grupo atend.nao cadastr. para este orgao *. E, no dia, o
grupo tem de ter o que foi registrado para ele: não tendo, a recusa é
* Grupo atend.nao cadastrado nesta data *. O **segmento** do grupo é o que o
cadastro do órgão define para o grupo, e a tela o mostra junto com a descrição do
grupo.

[?] A tela oferece **dezesseis** posições de grupo de atendimento e marca com um
asterisco as que têm registro no dia, mas o fonte não guarda essa lista em cadastro
nenhum: o que fica gravado é o cardápio e a quantidade de cada refeição do grupo.
O que cada posição e cada marca significam na máscara não está no lote. Pergunta ao
site.

### RN-10 — A refeição do grupo: básica e sobremesa

A refeição informada tem de estar **cadastrada para aquele grupo de atendimento**
— senão * Refeicao nao cad. para este gr.atend *. E a **sobremesa** só é aceita se
a refeição estiver marcada, no cadastro, como refeição que admite sobremesa — senão
* Refeicao nao cadastrada para sobremesa *.

### RN-11 — O cardápio tem de existir e valer para a data, a semana e a refeição

O **cardápio** informado tem de estar cadastrado — senão * Cardapio nao cadastrado *
—, e a sua **vigência** tem de alcançar a data do dia: um cardápio cujo início de
vigência é posterior ao dia é tratado como não cadastrado. Informada a quantidade
sem o cardápio, a recusa é * Informe codigo do cardapio *. O cardápio também tem de
estar cadastrado **na semana** do dia — senão * Cardapio nao cadastrado nesta
semana * — e **para aquela refeição** — senão * Cardapio nao cadastrado nesta
refeicao *. Um cardápio de sobremesa informado numa refeição é recusado com
* Cardapio cadastrado como sobremesa *.

Para a sobremesa vale o mesmo: quantidade sem cardápio de sobremesa é
* Informe codigo da sobremesa *, cardápio não cadastrado é * Cardapio nao
cadastrado * e um cardápio de refeição informado como sobremesa é
* Cardapio nao cadastrado como sobremesa *.

[?] A leitura do cardápio vai pelo **limite de vigência** com a data do dia no
lugar da data-limite, e o que o acervo entende por isso — procurar o registro
daquele dia, ou o primeiro da faixa — não está explicado no dicionário nem no
manual. A conferência de vigência acima é o que o programa compara depois de ler.
Pergunta ao site.

### RN-12 — As quantidades não podem passar o máximo de comensais do segmento

Antes de gravar o cardápio e as quantidades, a tela soma as quantidades **já
registradas no dia para o mesmo segmento e a mesma refeição** — de todos os grupos
do segmento — e compara com o **máximo de comensais do segmento**. Passando, a
recusa é <-Quant. comensais > maximo para o segmento *, com o cursor na
quantidade. Para a sobremesa vale o mesmo, com <-Comensais sobremesa > maximo p/
segmento *. O máximo tem de estar cadastrado — senão * Maximo de comensais nao
cadastrado * — e estar ativo — senão * Maximo de comensais inativo *.

### RN-13 — A justificativa do dia e a do grupo

A tela trabalha com duas justificativas: a **do dia** e a **do grupo**. As duas têm
de constar do cadastro de justificativas do órgão — senão
* Justificativa nao cadastrada *. A justificativa do grupo não pode ser a mesma do
dia: sendo, a recusa é * Justificativa ja cadastrada para o dia *. Informada a
justificativa do grupo sem o grupo de atendimento, a recusa é
* Informe o grupo de atendimento *.

Há ainda duas conferências de conjunto: quando o dia **não** tem refeição que obriga
justificativa (RN-14) mas a justificativa do dia vem preenchida com a do grupo
também, a recusa é * Ja existe refeicao que obriga justificativa *; e quando a
justificativa escolhida é a que o cadastro descreve como **UCG NOVA** e o órgão tem
perfil cadastrado em algum mês anterior àquele, a recusa é
* Use outra justificativa. Perfil cad. meses ant *.

**Feriados e fins de semana.** Sendo o dia do mapa um feriado, ou caindo em sábado
ou domingo, a tela procura no cadastro a justificativa descrita com o nome do
feriado — ou, no fim de semana, com o dia da semana — e adota o código dela como a
justificativa do dia.

[?] "UCG NOVA" é a descrição de uma justificativa no cadastro, e o acervo não diz o
que ela significa — por que ela só serve quando o órgão não tem perfil em mês
anterior é leitura do código, não do dicionário. Pergunta ao site.

### RN-14 — A refeição que obriga justificativa

Algumas refeições obrigam justificativa: quando o cadastro da refeição a marca
assim e o dia **não tem** justificativa informada — a do dia nem a do grupo —, a
recusa é <- Esta refeicao obriga justificativa *, com o cursor na justificativa.
É essa mesma marcação que separa as duas conferências de conjunto da RN-13.

### RN-15 — O dia anterior, o dia seguinte e o dia novo

A tela oferece três teclas de passagem de dia:

- **dia anterior** e **dia seguinte**: a tela procura o dia no cadastro do órgão e,
  não o achando, recusa com * Dia anterior nao cadastrado * ou
  * Proximo dia nao cadastrado *. Achando, ela **posiciona o dia** e passa a
  consultá-lo;
- **a consulta de um dia anterior a 1º de agosto de 2008** encaminha o servidor
  para a tela do dia (RN-17); de 1º de agosto de 2008 em diante esse
  encaminhamento não acontece, e a tela do dia não é acionada por esta passagem;
- **dia novo**: marcado o pedido, a tela exige a **confirmação**. Quando o dia não
  tem grupo de atendimento com nada registrado, ela avisa
  "Dia incompleto. Grupos de atendimento zerados." e pede
  "Confirma novo dia?: <S/N>:". Resposta diferente de S ou N é recusada com
  * Confirme novo dia com S ou N *, com o cursor na confirmação. O dia novo não
  pode ser posterior a hoje (RN-04) e o mês tem de ter perfil (RN-05). Confirmado,
  a tela **fecha o dia que estava aberto e o perfil do mês** e volta pronta para uma
  inclusão limpa.

Quando o dia tem grupo de atendimento marcado mas nenhuma refeição registrada para
ele, a tela pede * Cadastrar NRS para refeicao basica * e devolve o cursor ao grupo.

### RN-16 — A tela muda conforme quem a chamou

A `M040T` **compara a tela de origem** deixada na sessão com as duas telas do dia —
a do dia anterior e a do dia seguinte. Quando foi uma delas que a abriu, a `M040T`
descarta o que estava no contexto (a marca da tela, o indicador de mapa anterior e
o código da refeição) e relê o mapa do dia escolhido. É isso que faz a volta do dia
anterior ou do dia seguinte recomeçar limpa, em vez de misturar o dia que se estava
vendo com o dia que se escolheu. Vindo de qualquer outra origem, a tela segue com o
contexto como está.

O **modo desta tela não se decide pela origem**: a operação (consulta, inclusão,
alteração, exclusão) é a que o servidor informa nela. O que a origem muda é só o
reinício limpo; e o modo em que a tela seguinte abre não vem da operação usada
aqui (RN-17).

### RN-17 — O que a tela entrega às telas seguintes

A `M040T` sai para cinco destinos. Em todos eles ela deixa na sessão o órgão filho,
a coordenadoria, o mês e o ano de referência e o dia escolhido, e a marca de que foi
ela que escolheu o dia:

- **tela do dia anterior** e **tela do dia seguinte** (a segunda quando o órgão
  está cadastrado como creche e a primeira nos demais órgãos): recebem o dia
  escolhido e abrem **já posicionadas nele** — **em inclusão, quando aquele dia
  ainda não tem mapa; em consulta, quando tem**;
- **cadastro de grupos de atendimento** (pelo campo do grupo) e **cadastro de
  justificativas** (pelo campo da justificativa): recebem o órgão filho;
- **cadastro do perfil do mês** (pelo campo do perfil): recebe o órgão e a
  coordenadoria e abre **em consulta** — nunca em alteração, por este caminho.

### RN-18 — A consulta não grava o mapa

Na **consulta**, a tela lê o dia e o mostra. Não cria, não altera, não apaga, não
trava registro e não gera rastro de auditoria do mapa. O que a consulta pode gerar
é a solicitação de arquivo (RN-19).

### RN-19 — O arquivo do dia ou do mês

A consulta pode **pedir o arquivo** do órgão: marcado o campo do arquivo e
informado o período — **do dia** ou **mensal** —, a tela registra a solicitação e
dispara a emissão. A solicitação só acontece **na consulta**; nas outras operações
o campo é ignorado e desmarcado. Para pedir, o servidor tem de ter **e-mail
cadastrado** — senão <- Usuario sem e-mail cadastrado * — e não pode haver um
**pedido igual em processamento** para o mesmo órgão — senão
* Arquivo em processamento. Aguarde. *. O período informado tem de ser do dia (D) ou
mensal (M): qualquer outro valor é recusado com
* Inf.se arquivo do dia <D> ou mensal <M> *, com o cursor no campo do período.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter o dia do mapa por grupo de atendimento do órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M040T

  Cenário: Consulta mostra o dia e não grava nada
    Dado que o dia tem mapa para o órgão
    Quando informo a operação de consulta
    Então vejo o grupo de atendimento, o segmento, os cardápios e as quantidades
    E vejo a situação do dia, a semana e o período do mês
    E nada é gravado

  Cenário: Inclusão registra o dia
    Dado que o órgão do meu vínculo tem perfil cadastrado no mês de referência
    E que aquele dia ainda não tem mapa
    Quando informo a operação de inclusão, o grupo, a refeição e o cardápio com a quantidade
    Então o sistema grava o cardápio e a quantidade da refeição do grupo
    E registra a operação na auditoria

  Cenário: Inclusão de um dia fecha o dia anterior e o perfil do mês
    Dado que o dia anterior está aberto e o perfil do mês está aberto
    Quando incluo o mapa de um dia
    Então o dia anterior fica fechado
    E o perfil do mês fica fechado

  Cenário: Alteração regrava o dia
    Dado que consultei aquele dia nesta sessão
    E o dia está aberto
    Quando informo a operação de alteração e regravo a quantidade da refeição
    Então o sistema grava o dia com o novo número
    E registra a operação na auditoria

  Cenário: Exclusão apaga o dia
    Dado que consultei aquele dia nesta sessão
    E o dia está aberto
    Quando informo a operação de exclusão
    Então o registro do dia, o cardápio com as quantidades e a justificativa do grupo são apagados
    E registra a operação na auditoria

  Cenário: Alteração que deixa o dia vazio apaga o registro do dia
    Dado que consultei aquele dia nesta sessão
    E o dia fica sem nenhuma refeição e sem nenhuma justificativa
    Quando confirmo a alteração
    Então o registro do dia é apagado
    E registra a operação na auditoria

  Cenário: Órgão fora do vínculo do servidor
    Dado que informo um órgão que não é o do meu vínculo
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"

  Cenário: Órgão não cadastrado, inativo ou com dados incompletos
    Dado que informo um órgão que não existe no cadastro
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E quando o órgão está cadastrado como inativo vejo "* Orgao cadastrado como inativo *"
    E quando o órgão está sem bairro, órgão pai, nome, endereço, matriculados ou pessoas vejo "* Orgao cadastrado com dados incompletos *"

  Cenário: Órgão de outra secretaria ou de outra coordenadoria
    Dado que o órgão não é da secretaria da sessão
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E quando o órgão é de uma coordenadoria à qual não tenho acesso vejo "<- Usuario sem acesso ao grupo deste orgao *"

  Cenário: Órgão não informado
    Quando não informo o órgão
    Então vejo a mensagem "* Informe o orgao *"

  Cenário: Operação que não existe
    Dado que informo uma operação diferente de consulta, inclusão, alteração e exclusão
    Então vejo a mensagem "* Operacao nao disponivel *"
    E nada é gravado

  Cenário: Data do mapa impossível
    Dado que informo um dia ou um mês que não existe
    Então vejo a mensagem "* Data invalida *"
    E quando peço o dia anterior ou o dia seguinte sem informar a data vejo "* Data Invalida *"

  Cenário: Data do mapa posterior a hoje
    Dado que informo um dia depois de hoje
    Então vejo a mensagem "* Data do mapa maior que data atual *"
    E quando peço um dia novo depois de hoje vejo "* Novo dia maior que data atual *"

  Cenário: Dia que já tem mapa
    Dado que o dia já tem mapa
    Quando tento incluir
    Então vejo a mensagem "* Mapa ja cadastrado para esta data *"
    E nada é gravado

  Cenário: Mês sem perfil cadastrado para o órgão
    Dado que o mês não tem perfil de atendimento para o órgão
    Quando tento incluir
    Então vejo a mensagem "* Perfil nao cadastrado para este mes/ano *"
    E nada é gravado
    E quando consulto vejo o aviso "* Cadastrar perfil *" com o cursor no campo do perfil

  Cenário: Alterar ou excluir sem ter consultado aquele dia
    Dado que não consultei aquele dia nesta sessão
    Quando tento alterar
    Então vejo a mensagem "* Consulte antes de alterar *"
    E quando tento excluir vejo a mensagem "* Consulte antes de excluir *"

  Cenário: Dia fechado não aceita alteração nem exclusão
    Dado que o dia está fechado
    Quando tento alterar ou excluir
    Então vejo a mensagem "* Mapa fechado para esta data *"
    E o dia continua como está

  Cenário: Período e semana do dia vêm dos cadastros do órgão
    Dado que a tabela de períodos do mapa tem o mês e o ano de referência
    Quando abro o dia
    Então vejo o início e o limite do período
    E vejo a semana que o calendário de semanas do órgão define para aquela data
    E vejo se o órgão está cadastrado como creche

  Cenário: Grupo de atendimento não cadastrado
    Dado que informo um grupo de atendimento que não existe
    Então vejo a mensagem "* Grupo de atendimento nao cadastrado *"
    E quando o grupo não é daquele órgão vejo "* Grupo atend.nao cadastr. para este orgao *"

  Cenário: Grupo sem registro no dia
    Dado que o grupo não tem refeição registrada naquele dia
    Quando consulto o dia
    Então o sistema me avisa com "* Grupo atend.nao cadastrado nesta data *"

  Cenário: Grupo marcado e sem refeição registrada
    Dado que o dia tem grupo de atendimento marcado
    E nenhuma refeição registrada para ele
    Então vejo a mensagem "* Cadastrar NRS para refeicao basica *"
    E o cursor volta ao grupo

  Cenário: Refeição não cadastrada para o grupo
    Dado que informo uma refeição que não está cadastrada para aquele grupo de atendimento
    Então vejo a mensagem "* Refeicao nao cad. para este gr.atend *"
    E quando informo sobremesa numa refeição que não a admite vejo "* Refeicao nao cadastrada para sobremesa *"

  Cenário: Cardápio com quantidade sem o código
    Dado que informo quantidade numa refeição sem o código do cardápio
    Então vejo a mensagem "* Informe codigo do cardapio *"
    E quando informo quantidade de sobremesa sem o código vejo "* Informe codigo da sobremesa *"

  Cenário: Cardápio não cadastrado
    Dado que informo um cardápio que não vale na data do dia
    Então vejo a mensagem "* Cardapio nao cadastrado *"
    E nada é gravado

  Cenário: Cardápio fora da semana ou da refeição
    Dado que informo um cardápio que não está cadastrado na semana do dia
    Então vejo a mensagem "* Cardapio nao cadastrado nesta semana *"
    E quando o cardápio não serve àquela refeição vejo "* Cardapio nao cadastrado nesta refeicao *"

  Cenário: Cardápio trocado entre refeição e sobremesa
    Dado que informo, numa refeição, um cardápio cadastrado como sobremesa
    Então vejo a mensagem "* Cardapio cadastrado como sobremesa *"
    E quando informo um cardápio de refeição na sobremesa vejo "* Cardapio nao cadastrado como sobremesa *"

  Cenário: Quantidade acima do máximo de comensais do segmento
    Dado que a soma das quantidades do segmento naquela refeição passa o máximo cadastrado
    Quando tento gravar
    Então vejo a mensagem "<-Quant. comensais > maximo para o segmento *"
    E quando a sobremesa passa o máximo vejo "<-Comensais sobremesa > maximo p/ segmento *"

  Cenário: Máximo de comensais não cadastrado ou inativo
    Dado que o segmento não tem máximo de comensais cadastrado para a refeição
    Então vejo a mensagem "* Maximo de comensais nao cadastrado *"
    E quando o máximo está inativo vejo "* Maximo de comensais inativo *"

  Cenário: Justificativa não cadastrada
    Dado que informo um código de justificativa que não existe no cadastro do órgão
    Então vejo a mensagem "* Justificativa nao cadastrada *"
    E nada é gravado

  Cenário: Justificativa do grupo igual à do dia
    Dado que informo, no grupo, a mesma justificativa do dia
    Então vejo a mensagem "* Justificativa ja cadastrada para o dia *"

  Cenário: Justificativa do grupo sem o grupo
    Dado que informo a justificativa do grupo e deixo o grupo de atendimento em branco
    Então vejo a mensagem "* Informe o grupo de atendimento *"

  Cenário: Dia sem refeição que obrigue justificativa
    Dado que nenhuma refeição do dia obriga justificativa
    E informo a justificativa do dia e a do grupo
    Então vejo a mensagem "* Ja existe refeicao que obriga justificativa *"

  Cenário: Justificativa que exige perfil de mês anterior
    Dado que a justificativa informada é a descrita como UCG NOVA
    E o órgão tem perfil cadastrado em um mês anterior
    Então vejo a mensagem "* Use outra justificativa. Perfil cad. meses ant *"

  Cenário: Refeição que obriga justificativa e o dia sem justificativa
    Dado que a refeição informada é marcada como refeição que obriga justificativa
    E o dia não tem justificativa informada
    Então vejo a mensagem "<- Esta refeicao obriga justificativa *"
    E nada é gravado

  Cenário: Dia anterior ou dia seguinte não cadastrado
    Dado que o órgão não tem o dia anterior no cadastro
    Quando peço o dia anterior
    Então vejo a mensagem "* Dia anterior nao cadastrado *"
    E quando peço o dia seguinte e ele não existe vejo "* Proximo dia nao cadastrado *"

  Cenário: Dia novo sem confirmação
    Dado que o dia não tem grupo de atendimento com nada registrado
    Quando marco o pedido de dia novo
    Então vejo o aviso "Dia incompleto. Grupos de atendimento zerados."
    E vejo o pedido "Confirma novo dia?: <S/N>:"
    E quando respondo outra coisa vejo "* Confirme novo dia com S ou N *"

  Cenário: Dia novo confirmado
    Dado que respondo S ao pedido de novo dia
    Então o dia que estava aberto fica fechado
    E o perfil do mês fica fechado
    E a tela volta pronta para uma inclusão limpa

  Cenário: A tela recomeça limpa quando vem da tela do dia
    Dado que a tela do dia anterior ou do dia seguinte me devolveu a esta tela
    Quando a tela abre
    Então ela descarta a marca da tela de origem e o código da refeição que estavam no contexto
    E relê o mapa do dia escolhido

  Cenário: O que a tela entrega à tela do dia
    Dado que consulto um dia anterior a 1º de agosto de 2008 que ainda não tem mapa
    Quando a tela encaminha para a tela do dia
    Então a tela do dia abre posicionada naquele dia
    E abre em inclusão
    E quando aquele dia já tem mapa a tela do dia abre em consulta

  Cenário: A tela entrega o órgão aos cadastros de grupo e de justificativa
    Dado que estou no dia de um órgão filho
    Quando peço o cadastro de grupos de atendimento
    Então o cadastro abre com aquele órgão filho
    E quando peço o cadastro de justificativas o cadastro abre com aquele órgão filho

  Cenário: O perfil do mês abre em consulta
    Dado que estou no dia de um órgão filho
    Quando peço o cadastro do perfil do mês
    Então o cadastro abre com o órgão e a coordenadoria daquele dia
    E abre em consulta, sem aceitar alteração por este caminho

  Cenário: Pedido de arquivo sem e-mail cadastrado
    Dado que a minha matrícula não tem e-mail cadastrado
    Quando peço o arquivo do dia na consulta
    Então vejo a mensagem "<- Usuario sem e-mail cadastrado *"
    E nada é gravado

  Cenário: Pedido de arquivo já em processamento
    Dado que já existe um pedido de arquivo em processamento para aquele órgão
    Quando peço o arquivo do dia na consulta
    Então vejo a mensagem "* Arquivo em processamento. Aguarde. *"

  Cenário: Período do arquivo inválido
    Dado que informo um período diferente de do dia ou mensal
    Quando peço o arquivo na consulta
    Então vejo a mensagem "* Inf.se arquivo do dia <D> ou mensal <M> *"
    E o cursor volta ao campo do período
```
