# US — E099P — Solicitar o relatório de pedidos por data de entrega

## Estória

Como **servidor da CRE que acompanha a entrega dos pedidos**, quero **informar os
parâmetros e pedir o processamento do relatório de pedidos por data de entrega**,
para que o relatório saia na impressora e no meu e-mail com os pedidos que
interessam à minha coordenação, no período e no tipo de atendimento que eu escolher.

O relatório não é montado na tela: ela confere os parâmetros, registra a solicitação
com um número próprio e dispara o processamento, e o resultado sai depois, pela
impressora e pelo e-mail do servidor. Por isso a tela só aceita quando a data de
entrega, a coordenação, o intervalo de pedidos e as marcações de atendimento estão
completos — sem eles o processamento não teria como selecionar os pedidos. E
enquanto a solicitação daquele relatório para aquela coordenação estiver registrada,
a tela não deixa pedir de novo.

## Contexto

Jornada S000M → E000M → E001M → E099P.

Ator: servidor de CRE — pede a emissão de um relatório do módulo de pedidos,
informando a coordenação regional escolar, o intervalo de pedidos e a data de
entrega.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio.

A `E099P` é uma só para **35 relatórios**: o menu anterior escolhe o relatório e a
impressora, deixa os dois na sessão, e a tela monta os campos daquele relatório. O
menu e a entrada também deixam na sessão a matrícula, o acesso, o vínculo com a
secretaria e a coordenação do servidor. O caminho desta jornada é o do **relatório
de pedidos por data de entrega**, o primeiro daquele menu.

---

## Regras de negócio

### RN-01 — A E099P é tela de processamento: ela pede o relatório e não mantém cadastro

A tela não inclui, não altera e não exclui cadastro nenhum. Ela recebe do menu
anterior o relatório escolhido e a impressora, exibe os campos daquele relatório e,
no aceite, registra a solicitação. Tudo o que ela lê — pedidos, itens, órgãos,
cadastro do servidor — é leitura; o que ela grava é a solicitação e a trilha de
auditoria (A010T). Só abrir a tela e sair não grava nem apaga nada.

[?] O fonte não dá o nome de negócio do relatório desta jornada, e a jornada não
registra qual opção do menu anterior a abriu. Descrevi o primeiro relatório daquele
menu; os outros 34 que a mesma tela serve não foram lidos.

### RN-02 — O acesso à tela e ao relatório é conferido antes de qualquer processamento

Antes de montar os campos, a tela confere a autorização do servidor para ela própria
e para o relatório escolhido. Se qualquer uma das duas não retornar liberada, a tela
encerra sem processar nada.

[?] As duas conferências de acesso são rotinas externas à tela: o que está nela é a
chamada e o desfecho. Por isso não dá para saber, por este fonte, qual é o critério
da conferência do relatório nem o que o servidor vê quando ela recusa — esta tela não
traz mensagem de recusa de acesso. Pergunta ao site.

### RN-03 — A coordenação é obrigatória e limitada à do servidor

A coordenação regional escolar é o campo que diz de quem são os pedidos. Quem entrou
vinculado a uma coordenação já a encontra preenchida, e a tela recusa qualquer outra
com * Usuario sem acesso a outro grupo *. Quem não tem coordenação no vínculo pode
digitá-la, mas não pode deixá-la em branco: a recusa é * Informe o grupo *, e o
cursor volta ao campo.

### RN-04 — Um relatório por vez para a mesma coordenação

Se já existe uma solicitação registrada daquele relatório para aquela coordenação, a
tela recusa a nova com * Relatorio em processamento. Aguarde. * e não segue para as
demais conferências.

[?] A conferência olha só a existência da solicitação — não olha a data nem a
situação dela — e é a própria tela que a cria no aceite; nada nesta tela a apaga. A
entrada apaga as solicitações anteriores à data do sistema, e outras telas do acervo
também apagam. Pergunta ao site: o que, e quando, libera a coordenação para pedir o
mesmo relatório outra vez?

### RN-05 — A trilha de auditoria do dia é apagada antes das conferências

Passadas a conferência de acesso e a de solicitação em andamento, e antes de
conferir qualquer campo, a tela varre a trilha de auditoria (A010T) do dia para
aquele relatório e apaga os registros da coordenação informada.

[?] A limpeza vem antes das conferências: uma solicitação recusada depois dela —
intervalo inválido, data em branco, marcação faltando — já apagou a trilha do dia
daquele relatório para aquela coordenação, e não deixa solicitação no lugar. Pelo
fonte não dá para saber se a ordem é intencional. Pergunta ao site.

### RN-06 — O intervalo de pedidos: inicial, final, e o 999999 valendo por "todos"

A tela pede o número do pedido inicial e o número do pedido final. No inicial,
999999 vale por "todos" — a tela o toma como o começo. O final é obrigatório: em
branco, a recusa é * Inf. ped.final intervalo ou 999999 para todos *; menor que o
inicial, a recusa é * Intervalo de pedidos invalido *. O intervalo informado segue
na solicitação, para o processamento do relatório.

### RN-07 — A data inicial de entrega é obrigatória e manda no ano da entrega

É a data inicial de entrega — dia, mês e ano — que seleciona os pedidos. Se os três
estiverem zerados, a recusa é * Informe a data inicial de entrega *. O "ano da
entrega" digitado é substituído pelo ano da data inicial, e é esse par que segue
para o processamento.

[?] Os campos "ano da entrega" e "ano final" estão na tela e passam pela edição
numérica, mas o processamento os descarta: o ano da entrega vira o ano da data
inicial. Ou os campos são só de exibição, ou a tela ignora o que o servidor digita —
o fonte não diz. Pergunta ao site.

### RN-08 — A marcação de creche e o tipo de pedido

A tela exige que o servidor diga se é creche, com "S" ou "N" — senão, * Informe se
creche ou nao com S ou N * — e qual o tipo de pedido, entre semana, extras, troca de
fornecedor e todos, com "S", "E", "F" ou "T" — senão, * Inf. S=Semana/E=Extras/F=Troca
Forn ou T=Todos *.

### RN-09 — Impressão e arquivo: pelo menos uma saída

A tela exige que o servidor diga se gera impressão e se gera arquivo, cada um com
"S" ou "N" — * Informe se gera impressao com S ou N * e * Informe se gera arquivo com
S ou N *. E recusa quando as duas respostas são "não", com * Informe se gera arquivo
ou impressao *: é preciso escolher pelo menos uma saída. A tela abre com as duas em
"não".

### RN-10 — Quatro peneiras nos pedidos; sem nenhum, não há relatório

A tela percorre os pedidos da data de entrega informada e só deixa passar os que
estão na situação que ela trata como liberada; os do tipo de pedido escolhido —
semana e extras se separam por uma marcação do próprio pedido, e troca de fornecedor
por outra; os da creche marcada, conforme o cadastro do órgão do pedido; e os que têm
tipo de contrato definido. Se nenhum pedido passar, a recusa é * Nao existem pedidos
nesta data de entrega *.

O intervalo de pedidos informado não é usado nessa varredura: a tela lê todos os
pedidos da data de entrega e repassa o intervalo ao processamento.

[?] O que a situação "A" do pedido significa — aprovado, em aberto — não está neste
corpus; em outros relatórios da mesma tela a mesma peneira aceita "A" ou "F".
Pergunta ao site.

### RN-11 — O relatório vai pela impressora e pelo e-mail do servidor

O relatório é entregue pela impressora indicada no menu anterior e pelo e-mail do
servidor: sem e-mail cadastrado, a tela recusa com * <- Usuario sem e-mail cadastrado *
e devolve o cursor à coordenação. O e-mail, a matrícula, a impressora, o número de
cópias e o código do relatório seguem junto com a solicitação.

[?] O texto da recusa vem com uma seta à esquerda, como se fosse a continuação de
uma mensagem maior — que não está no fonte. Pergunta ao site.

### RN-12 — No aceite: número, gravação, auditoria e disparo do processamento

Passando por todas as conferências, a tela toma o próximo número da solicitação — o
último número gravado mais um —, grava a solicitação com o relatório, a coordenação,
a impressora, o servidor, a data e os parâmetros informados, grava a trilha de
auditoria e dispara o processamento do relatório. Não há impressão na hora nem
confirmação na tela: neste caminho, as 13 mensagens que o servidor pode ver são
todas de recusa.

### RN-13 — Ao terminar, três relatórios voltam ao menu e o desta jornada encerra

Depois de registrada a solicitação, a tela volta ao menu `E001M` apenas para três
relatórios; para o relatório desta jornada ela simplesmente encerra. A tela não
encadeia em nenhuma outra tela de transação: o que ela deixa para o processamento é
a solicitação gravada, não uma passagem.

---

## Cenários BDD

```gherkin
Funcionalidade: Solicitar o relatório de pedidos por data de entrega

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E099P
    E o menu anterior escolheu o relatório de pedidos por data de entrega e a impressora

  Cenário: Só abrir a tela e sair não grava nem apaga nada
    Dado que abri a tela E099P com os campos daquele relatório
    Quando saio sem confirmar a solicitação
    Então nenhuma solicitação é registrada
    E a trilha de auditoria fica como estava

  Cenário: Sem autorização para o relatório, a tela encerra
    Dado que não tenho autorização para o relatório escolhido pelo menu anterior
    Quando a tela E099P abre
    Então ela encerra sem processar
    E nenhuma solicitação é registrada e a trilha de auditoria fica como estava

  Cenário: Pedido do relatório aceito
    Dado que estou vinculado à coordenação regional escolar 12
    E informei a data inicial de entrega 15/03/2004
    E informei o intervalo de pedidos de 000001 a 000900
    E marquei creche "N", tipo de pedido "T", impressão "S" e arquivo "N"
    E existem pedidos que passam nas quatro peneiras
    Quando confirmo a solicitação
    Então a solicitação é registrada com o próximo número, com a coordenação, a impressora e a data
    E a trilha de auditoria recebe o registro da solicitação
    E o processamento do relatório é disparado
    E a tela não mostra mensagem de confirmação

  Cenário: Nada é gravado nem apagado quando a coordenação é recusada
    Dado que estou vinculado à coordenação regional escolar 12
    Quando informo a coordenação 13
    Então vejo * Usuario sem acesso a outro grupo *
    E o cursor volta à coordenação
    E nenhuma solicitação é registrada e a trilha de auditoria fica como estava

  Cenário: Sem coordenação informada, a tela recusa
    Dado que não tenho coordenação no vínculo
    E deixo a coordenação em branco
    Quando confirmo a solicitação
    Então vejo * Informe o grupo *
    E nenhuma solicitação é registrada e a trilha de auditoria fica como estava

  Cenário: Relatório já solicitado para a mesma coordenação
    Dado que existe uma solicitação registrada deste relatório para a minha coordenação
    Quando confirmo uma nova solicitação
    Então vejo * Relatorio em processamento. Aguarde. *
    E nenhuma solicitação é registrada e a trilha de auditoria fica como estava

  Cenário: A recusa depois da limpeza apaga a trilha do dia
    Dado que existe trilha de auditoria do dia para este relatório e a minha coordenação
    E não existe solicitação registrada dele
    E deixei a data inicial de entrega em branco
    Quando confirmo a solicitação
    Então vejo * Informe a data inicial de entrega *
    E a solicitação não é registrada
    Mas a trilha de auditoria do dia daquele relatório para a minha coordenação já foi apagada

  Cenário: Pedido final menor que o inicial
    Dado que informei o intervalo de pedidos de 000500 a 000100
    Quando confirmo a solicitação
    Então vejo * Intervalo de pedidos invalido *
    E o cursor volta ao número do pedido inicial

  Cenário: Pedido final em branco
    Dado que deixei o número do pedido final em branco
    Quando confirmo a solicitação
    Então vejo * Inf. ped.final intervalo ou 999999 para todos *
    E o cursor volta ao número do pedido final

  Cenário: 999999 no pedido inicial vale por todos
    Dado que informei 999999 como número do pedido inicial
    E os demais parâmetros estão completos
    Quando a solicitação é aceita
    Então o relatório é processado do primeiro pedido em diante

  Cenário: Data inicial de entrega em branco
    Dado que deixei dia, mês e ano iniciais em branco
    Quando confirmo a solicitação
    Então vejo * Informe a data inicial de entrega *
    E o cursor volta à data inicial

  Cenário: O ano da entrega digitado é substituído
    Dado que informei o ano da entrega 2005 e a data inicial de entrega 15/03/2004
    E os demais parâmetros estão completos
    Quando a solicitação é aceita
    Então o processamento recebe 2004 como ano da entrega

  Cenário: Creche não informada
    Dado que deixei a marcação de creche em branco
    Quando confirmo a solicitação
    Então vejo * Informe se creche ou nao com S ou N *

  Cenário: Tipo de pedido inválido
    Dado que informei "X" como tipo de pedido
    Quando confirmo a solicitação
    Então vejo * Inf. S=Semana/E=Extras/F=Troca Forn ou T=Todos *

  Cenário: Sem impressão e sem arquivo
    Dado que deixei a impressão e o arquivo marcados com "N"
    Quando confirmo a solicitação
    Então vejo * Informe se gera arquivo ou impressao *

  Cenário: Nenhum pedido passa nas peneiras
    Dado que os parâmetros estão completos
    E nenhum pedido daquela data de entrega passa nas quatro peneiras
    Quando confirmo a solicitação
    Então vejo * Nao existem pedidos nesta data de entrega *
    E nenhuma solicitação é registrada

  Cenário: Sem e-mail cadastrado
    Dado que existem pedidos e eles passam nas quatro peneiras
    E o meu cadastro está sem e-mail
    Quando confirmo a solicitação
    Então vejo * <- Usuario sem e-mail cadastrado *
    E nenhuma solicitação é registrada

  Cenário: O fim da tela depende do relatório escolhido
    Dado que a solicitação foi aceita para o relatório desta jornada
    Quando a tela termina
    Então ela encerra sem voltar ao menu
    Mas para três dos relatórios da mesma tela ela volta ao menu E001M
```
