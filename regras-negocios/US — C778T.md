# US — C778T — Pedir a exclusão do planejamento de um grupo e período

## Estória

Como **servidor de CRE**, quero **informar um grupo e um período e pedir a exclusão do
planejamento daquele período**, para que **o planejamento encerrado saia do cadastro sem
que eu tenha de apagá-lo dia a dia, e sem que se apague um período que ainda tem pedidos
em uso**.

O planejamento diz o que cada grupo serve em cada dia da semana, por segmento e refeição,
e vale de uma data de início a uma data limite. Encerrado o período, o que ficou no
cadastro precisa sair — e é isso que esta tela pede. Ela não apaga nada por si: confere o
grupo e o período, pede a confirmação e registra o pedido que manda o processamento
apagar o planejamento. Enquanto houver pedido alcançando o período, a exclusão é
recusada: o planejamento só sai quando já não depende dele.

## Contexto

Jornada S000M → C000M → C070M → C770M → C778T.

Ator: servidor de CRE — pede a exclusão do planejamento de um grupo e de um período do
tipo de órgão da sua sessão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As três telas do caminho — o `C000M`, o `C070M` e o `C770M` — são menus e não gravam
nada. O encadeamento tela a tela, em que uma tela de transação passa o registro e a
operação para a seguinte sem passar por menu, não acontece nesta jornada: o que a tela
usa é o contexto que a entrada deixou na sessão — a matrícula, o código de acesso, o
privilégio, a estação, o tipo de órgão e a coordenação regional do servidor. O grupo que
a exclusão alcança, porém, não é o da sessão: é o que o operador informa.

O que a tela manda apagar é o **planejamento** do grupo e do período; o que ela registra
é o **pedido** de um processamento. A tela termina em si mesma: depois de registrar, ela
se reabre, e a jornada não segue para nenhuma outra tela.

---

## Regras de negócio

### RN-01 — A tela pede a exclusão; quem apaga é o processamento

A tela não exclui planejamento nenhum. Ela confere o grupo e o período, pede a
confirmação, registra o pedido do relatório que faz a exclusão, registra a **auditoria**
da operação e entrega o processamento; encerrado o registro, o operador vê
**\* Cadastro sendo excluido \***. O processamento apaga em lote os planejamentos do grupo
e do período e, ao terminar, apaga o próprio pedido.

As rotinas de exclusão existem declaradas para os **sete** cadastros que a tela enxerga,
mas nenhuma delas é executada por caminho nenhum: as duas únicas gravações que a tela faz
são a da auditoria e a do pedido. Declarar não é executar.

### RN-02 — O grupo e o período são informados pelo operador e passam por edição numérica

A tela recebe **sete dados**: o grupo, o dia, o mês e o ano de início do período e o dia,
o mês e o ano limite. Os sete passam por edição numérica antes de qualquer leitura —
campo em branco é tratado como zero e o que não for número é recusado —, e o erro em um
campo não interrompe a edição dos outros; quem não segue é a conferência. O tipo de órgão
não é informado: tudo o que a tela confere é pelo tipo de órgão da sessão.

[?] O que o operador vê quando a digitação é recusada não está nos fontes desta jornada —
a rotina que faz a edição numérica não faz parte do acervo lido —, e a devolução do
cursor ao campo recusado está escrita, no fonte da tela, só para **quatro** dos sete
campos: o grupo e as três partes da data limite. Para o dia, o mês e o ano de início não
há posição de cursor definida. Se a recusa nesses três é silenciosa, o acervo não mostra.
Pergunta ao site.

### RN-03 — Sem grupo informado, nada é conferido

A tela exige o grupo: chegando em branco, recusa com **\* Informe o grupo \*** e devolve o
cursor ao campo do grupo, antes de qualquer leitura de cadastro.

### RN-04 — Sem planejamento para o grupo e a data limite, nada é pedido

A tela procura, no cadastro dos planejamentos do tipo de órgão da sessão, o planejamento
cuja **data limite** é a informada e cujo grupo é o grupo informado. Não achando — ou
achando um registro que não fecha a conferência —, recusa com
**\* Nao existe planejamento para este grupo/data \***, devolve o cursor ao campo do grupo
e não registra pedido nenhum.

### RN-05 — O código de todos os grupos dispensa o grupo na procura

O grupo aceita um código que representa **todos os grupos** — o 99, o mesmo código que
outras telas do sistema legendam como "Todos". Com ele, a procura do planejamento não
exige o grupo e a varredura dos grupos do tipo de órgão vai do primeiro ao 99; com um
grupo determinado, a procura exige aquele grupo e a varredura se limita a ele. O grupo que
vai no pedido é sempre o que o operador informou.

[?] Com o código de todos os grupos, a procura do planejamento passa a exigir um registro
do **grupo zero**, e o grupo zero é também o primeiro grupo percorrido na varredura
seguinte: se não houver grupo zero no cadastro de grupos do órgão, a conferência que
recusa a exclusão por pedidos cadastrados pode não percorrer grupo nenhum, e a exclusão
seguiria sem essa conferência. Se a leitura se posiciona no primeiro grupo existente ou
falha quando não há nenhum, o acervo não explica. O significado de "todos" também não vem
de uma tabela do cadastro: foi lido na legenda do campo em outra tela do sistema. Pergunta
ao site.

### RN-06 — O período é o do planejamento cadastrado: a data de início informada é substituída

Encontrado o planejamento pela data limite, o sistema repõe em tela o **dia, o mês e o ano
de início do próprio planejamento**, e é esse início que passa a valer: é ele que entra
nas conferências seguintes e é ele que vai no pedido. O que o operador digitou no início
não é conferido contra nada nem aproveitado.

[?] Se o início informado deveria limitar a exclusão, ou se a intenção era apenas mostrar
o período, o acervo não responde: o que o fonte mostra é a reposição, sem nenhuma
conferência do que foi digitado. Pergunta ao site.

### RN-07 — Com pedidos alcançando o período, a exclusão é recusada

A tela percorre os grupos do tipo de órgão da sessão e, em cada um, os pedidos
registrados. Se algum pedido alcançar o período — começando dentro dele, terminando
dentro dele ou envolvendo-o por inteiro —, a exclusão é recusada com
**\* Nao exclua. Ja existem pedidos cadastrados \***, com o cursor de volta ao campo do
dia limite, e nada é pedido. Pedido que já foi excluído não conta.

[?] A varredura dos pedidos é posicionada pela data de início do planejamento; um pedido
que comece antes dessa data e termine dentro do período pode não ser visitado, embora a
conferência tenha um ramo escrito exatamente para esse caso. Se a leitura se posiciona no
primeiro pedido do grupo ou só a partir daquela data, o acervo não explica. Pergunta ao
site.

### RN-08 — A exclusão só é pedida depois da confirmação do operador

Passando pelas conferências, a tela guarda o grupo e o período, mostra
**\* Confirma exclusao do planejamento <S/N> ? \*** e espera a resposta. Só a resposta
**S** leva ao registro do pedido; qualquer outra resposta limpa a mensagem e devolve a
tela às conferências, que são refeitas e a confirmação é pedida de novo. A confirmação só
vale para o mesmo grupo e a mesma data limite: mudando qualquer um dos dois, a tela
confere o grupo e o período outra vez. O início do período não entra nessa conferência.

[?] Como a resposta diferente de S volta a pedir a confirmação, quem responde N não
cancela: refaz as conferências e vê a mesma pergunta — não há, no fluxo lido, um caminho
de desistir que não seja abandonar a tela. Se isso é o pretendido, o acervo não diz.
Pergunta ao site.

### RN-09 — Com um pedido do mesmo relatório em processamento, a tela recusa outro

Depois da confirmação e antes de registrar, a tela procura um pedido do mesmo relatório e,
achando um, avisa **\* Relatorio em processamento. Aguarde. \***, com o cursor de volta ao
campo da resposta, e não registra nada. O processamento apaga o próprio pedido ao
terminar, e é isso que libera a tela para o pedido seguinte. Na primeira passagem, antes
da confirmação, essa conferência não é feita.

[?] A procura do pedido pendente é feita com a situação do pedido em branco e o número
zerado, e a conferência que vem depois compara só o código do relatório: se ela alcança
qualquer pedido ainda não processado ou só um de número zero depende do posicionamento da
leitura, que o acervo não explica. Pergunta ao site.

### RN-10 — A tela só trabalha em alteração

Ao ser apresentada, a tela marca a operação como **alteração**, e é essa operação que
segue para as conferências. Se a mensagem do operador chegar com outra operação, a recusa
é **\* Opcao nao disponivel. Use ALT \***, com o cursor no campo da resposta e nada lido
nem registrado. Não há modo de consulta nesta tela: ela não lista planejamento nenhum.

[?] A recusa manda usar ALT, mas o que a tela aceita é o código interno da alteração, e
nenhum valor "ALT" existe no acervo lido. Se o formulário traduz o que o servidor digita
para esse código, o acervo não mostra. Pergunta ao site.

### RN-11 — O pedido é numerado pelo sistema, identificado pela sessão, e a operação fica na auditoria

O pedido recebe o **número seguinte** ao do último pedido registrado — o operador não o
informa — e leva o código do relatório, a matrícula do funcionário, a estação, o dia e o
mês do sistema e o tipo de órgão da sessão; o grupo e o período viajam no parâmetro que
acompanha o processamento, junto com o e-mail do funcionário. A operação também fica na
**auditoria**, que guarda como valor anterior o grupo e o período pedidos e, como
identificação, a matrícula, a estação, a coordenação regional da sessão, a data e a hora
da sessão e o tipo de órgão. Terminado o registro, a tela avisa
**\* Cadastro sendo excluido \*** e se reabre.

[?] O número seguinte é tirado do último pedido registrado com o auxílio de um
posicionamento de leitura cujo efeito exato não está no acervo: se a numeração é sempre a
do último pedido mais um, o site precisa confirmar. Pergunta ao site.

[?] O processamento é chamado por um nome de trabalho literal, o mesmo nas telas irmãs, e
o código do relatório viaja dentro do parâmetro; o acervo não tem catálogo que ligue esse
nome ao programa que apaga os planejamentos, embora exista, no próprio acervo, um programa
de processamento com o mesmo código do relatório que faz exatamente essa exclusão.
Pergunta ao site.

### RN-12 — Nenhuma recusa deixa pedido nem rastro de auditoria

Cada uma das **cinco recusas** da tela — operação diferente de alteração, grupo não
informado, planejamento não encontrado, pedidos alcançando o período e pedido do relatório
em processamento — termina sem gravar: nesses caminhos não há pedido nem registro de
auditoria.

### RN-13 — A tela mostra a data do sistema e a descrição do tipo de órgão da sessão

Fora o grupo, o período e as mensagens, a tela exibe a **data do sistema** e a **descrição
do tipo de órgão** da sessão. A limpeza da apresentação anterior apaga as duas — e a
mensagem — a cada passagem, de modo que uma conferência recusada não deixa em tela o
resultado da anterior.

[?] Nem a data do sistema nem a descrição do tipo de órgão são preenchidas por nenhum
caminho desta tela: ela copia as duas de áreas de trabalho, e a entrada as guarda em
outras. Se o ambiente transporta os valores de uma área para a outra — e de onde vem a
data do sistema —, o acervo não diz; se não transportar, os dois campos saem em branco.
Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedir a exclusão do planejamento de um grupo e período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C778T

  Cenário: Grupo e período com planejamento e sem pedidos alcançando
    Dado que existe planejamento do meu tipo de órgão para o grupo e a data limite que vou informar
    E não há pedido alcançando o período
    Quando informo o grupo, o dia, o mês e o ano de início e de limite e confirmo com S
    Então o sistema registra o pedido da exclusão com o número seguinte ao do último pedido
    E registra a operação na auditoria
    E vejo a mensagem "* Cadastro sendo excluido *"

  Cenário: O processamento recebe o grupo e o período e apaga o planejamento
    Dado que confirmei a exclusão
    Então o processamento é entregue com o meu tipo de órgão, o grupo e o período
    E o planejamento do grupo e do período é apagado
    E o próprio pedido é apagado ao terminar

  Cenário: O período passa a ser o do planejamento
    Dado que informei uma data de início diferente da data de início do planejamento
    Quando o sistema encontra o planejamento pela data limite
    Então o dia, o mês e o ano de início em tela passam a ser os do planejamento
    E é esse início que vale para as conferências e para o pedido

  Cenário: O código de todos os grupos dispensa o grupo
    Dado que informei o código que representa todos os grupos
    Quando o sistema procura o planejamento pela data limite
    Então a procura não exige o grupo
    E a varredura alcança os grupos do meu tipo de órgão
    E o grupo gravado no pedido é o código que informei

  Cenário: Digitação não numérica nos campos informados
    Dado que digitei algo que não é número em um dos sete campos
    Quando envio a tela
    Então a tela recusa a digitação antes de ler qualquer cadastro
    E nada é pedido

  Cenário: Grupo não informado
    Dado que deixei o grupo em branco
    Quando envio a exclusão
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nada é lido nem pedido

  Cenário: Não há planejamento para o grupo e a data limite
    Dado que não existe planejamento do meu tipo de órgão para o grupo e a data limite informados
    Quando envio a exclusão
    Então vejo a mensagem "* Nao existe planejamento para este grupo/data *"
    E o cursor volta ao campo do grupo
    E nada é pedido

  Cenário: Exclusão recusada porque há pedidos alcançando o período
    Dado que existe pedido de algum grupo do meu tipo de órgão alcançando o período
    Quando envio a exclusão
    Então vejo a mensagem "* Nao exclua. Ja existem pedidos cadastrados *"
    E o cursor volta ao campo do dia limite
    E nada é pedido

  Cenário: Pedido já excluído não impede a exclusão do período
    Dado que o único pedido que alcançaria o período já foi excluído
    Quando envio a exclusão
    Então o sistema pede a confirmação
    E o pedido da exclusão pode ser registrado

  Cenário: A confirmação vem antes de qualquer registro
    Dado que o grupo e o período passaram em todas as conferências
    Quando envio a exclusão
    Então vejo a mensagem "* Confirma exclusao do planejamento <S/N> ? *"
    E nada foi gravado ainda

  Cenário: Resposta diferente de S não grava nada
    Dado que vi a pergunta de confirmação
    Quando respondo N
    Então nada é pedido
    E a tela volta às conferências e pede a confirmação de novo

  Cenário: Grupo ou data limite diferentes na confirmação refazem as conferências
    Dado que vi a pergunta de confirmação
    Quando respondo S com outro grupo ou outra data limite
    Então a tela confere o grupo e o período de novo
    E só depois volta a pedir a confirmação

  Cenário: Já existe um pedido do relatório em processamento
    Dado que existe um pedido do mesmo relatório ainda não processado
    Quando confirmo a exclusão
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da resposta
    E nada é pedido

  Cenário: Operação diferente de alteração é recusada
    Quando informo uma operação diferente de alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo da resposta
    E nada é lido nem pedido

  Cenário: Não há modo de consulta
    Quando abro a tela C778T
    Então a tela não lista planejamento nenhum
    E a única operação que ela aceita é a alteração

  Cenário: Nenhuma recusa deixa rastro
    Dado que a exclusão foi recusada por qualquer um dos motivos
    Então nenhum pedido é registrado
    E nenhum registro de auditoria é gerado

  Cenário: A data do sistema e o tipo de órgão da sessão
    Quando abro a tela C778T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão
```
