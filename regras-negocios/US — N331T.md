# US — N331T — Confirmar a entrada das notas fiscais do operador logístico

## Estória

Como **servidor da CRE que confere a entrada das notas fiscais**, quero **ver na tela as
notas fiscais ainda não confirmadas de um operador logístico e marcar cada uma para
confirmar a sua entrada ou retirá-la da relação de pendentes**, para que **o contrato e o
pedido passem a refletir o que de fato entrou e ninguém continue esperando por uma nota que
já foi tratada**.

A nota fiscal lançada como pendente não vale sozinha: é nesta conferência que a quantidade
do item sai do saldo do contrato e do saldo do pedido, e é ela que registra a nota como
entrada confirmada. Sem essa passagem, o mesmo item continua pendente, o saldo do contrato
continua cheio e a secretaria perde o rastro do que entrou. Cada marcação fica registrada
na auditoria, porque é ela que sustenta a conferência depois.

## Contexto

Jornada S000M → N000M → N050M → N300M → N331T.

Ator: servidor de CRE — confere as notas fiscais pendentes de entrada dos operadores
logísticos da sua coordenadoria e marca cada uma delas.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As três telas anteriores da jornada (`N000M`, `N050M` e `N300M`) são menus: não deixam
regra nesta jornada, só a rota. O que a tela consome — o tipo de órgão, a coordenadoria, a
matrícula, a estação e a data do sistema — vem da sessão, carregado na entrada; a
coordenadoria e o tipo de órgão são o filtro de tudo o que ela lê e grava.

Esta é a última tela da jornada: ela não encaminha para nenhuma outra. E o modo como ela
opera **não** é decidido por quem a chama — os menus apenas a abrem, sem passar operação
nenhuma; o modo é o que o servidor informa na própria tela (RN-02).

A tela é de conferência e **grava**: registra a nota como entrada confirmada, abate
quantidades do contrato e do pedido, retira da relação de pendentes a nota e os seus itens
e deixa rastro na auditoria em cada uma dessas passagens. Ela não emite nem corrige nota
fiscal: o que ela trata é a nota que já está lançada como pendente.

---

## Regras de negócio

### RN-01 — A tela confere, em uma página de 12 linhas, as notas pendentes de um operador logístico

A tela trabalha sobre uma coordenadoria (o grupo, sob o rótulo COORD.REG.ESCOLA) e um
operador logístico, e mostra **até 12 notas fiscais por página**. Cada uma das 12 linhas
traz o número da nota fiscal (9 dígitos), a marcação de uma letra, o pedido seguido de uma
barra e do ano de entrega, o órgão e o seu nome, o fornecedor e a sua razão social e o tipo
de contrato. O nome do operador logístico vem do cadastro de operadores e fica no alto da
página.

[?] O terceiro rótulo da máscara, NRPEDAUX, está preso ao campo que o programa preenche com
o número da nota fiscal da última linha da página e usa para retomar a lista; o que a
máscara nomeia com esse rótulo não está no acervo.

[?] Havendo mais notas pendentes do que cabem na página, a lista é retomada a partir da
última nota exibida; como o servidor pede a página seguinte — e se ele a vê — não está na
fonte.

### RN-02 — A tela só trabalha em alteração (ALT) ou consulta (CON); sem opção informada, ela abre em consulta

Entrando sem informar a opção de manutenção, a tela assume **consulta (CON)** — e lembra
dessa escolha nas passagens seguintes. Se for informada uma opção diferente de **alteração
(ALT)** e de **consulta (CON)**, o sistema recusa, diz quais são as válidas e devolve o
cursor à opção.

Se o campo de próxima tela vier preenchido, a tela abandona a conferência das linhas.

[?] A guarda do campo de próxima tela está só na passagem que confere; a passagem que grava
não a repete. Pela fonte não dá para afirmar que preencher esse campo impeça a gravação — e
o que a máscara nomeia com ele também não está no acervo. Pergunta ao site.

[?] A correspondência entre os rótulos da máscara (ALT e CON) e as opções internas de
alteração e consulta é conclusão tirada do texto da mensagem, não verificada no acervo.

### RN-03 — A coordenadoria é obrigatória, e o usuário só altera nota da coordenadoria dele

A coordenadoria tem de ser informada: sem ela a tela recusa com * Informe o grupo * e
devolve o cursor ao campo. E quando a sessão traz uma coordenadoria, o que for digitado tem
de ser a mesma — outra coordenadoria é recusada com * usuario sem acesso a outro grupo *.

### RN-04 — A consulta exige o operador logístico e lista o que está pendente

Na consulta, o operador logístico é obrigatório: em branco, a tela recusa com * Informe o
operador logistico * e devolve o cursor ao campo. Informado, a tela lista as notas com
entrada não confirmada daquela coordenadoria e daquele operador, com o nome do operador no
alto da página. Não havendo nenhuma, avisa * Nao existem notas com ent.nao confirmada * e
posiciona o cursor no operador.

### RN-05 — A consulta não grava nada

Na consulta a tela lista e para: nenhuma nota é registrada como entrada confirmada, nenhuma
quantidade é abatida, nenhuma nota nem item sai da relação de pendentes.

### RN-06 — Não se altera sem ter consultado antes

Para alterar, a coordenadoria e o operador logístico digitados têm de ser os mesmos da
consulta feita na sessão. Não sendo, a tela recusa com * Consulte antes de atualizar * e
devolve o cursor à opção. A conferência é pelo par: trocar a coordenadoria ou o operador
exige nova consulta.

[?] A dupla consultada fica guardada na área comum da sessão e é zerada na primeira
passagem do programa, sob um marcador cujo significado o acervo não define. Se esse marcador
for reiniciado a cada transação, a dupla nunca chega à alteração e **a alteração fica
inalcançável**: toda tentativa de alterar cairia em * Consulte antes de atualizar *.
Pergunta ao site.

### RN-07 — A marcação da linha decide o destino da nota

Cada linha é processada por si, na ordem da página. Linha sem número de nota não faz nada.
Com a marcação de **confirmação**, a nota segue o caminho que registra a entrada; com a
**outra marcação**, o caminho que apenas retira a nota da relação de pendentes. Qualquer
outra marca é ignorada, e a linha não produz efeito nenhum.

[?] O que a outra marcação significa no negócio — cancelamento, estorno, nota que não deve
ser confirmada — não está no acervo: a fonte mostra o que ela faz (RN-11), não o que ela
nomeia.

### RN-08 — Confirmar registra a entrada da nota e retira a nota da relação de pendentes

Ao confirmar, a tela verifica se a nota já consta do registro de entradas confirmadas. Não
constando, registra a nota — com a sua situação de confirmada — junto com os itens da nota.
Depois, a nota e os seus itens saem da relação de pendentes, item a item, com o registro de
cada retirada na auditoria.

[?] A procura pela nota já confirmada leva o ano da nota na chave; a tela leva o ano
zerado, e o acervo não diz se um campo zerado deixa de restringir a procura ou exige o
valor zero. Se exigir, nenhuma nota confirmada seria encontrada e a confirmação registraria
a nota outra vez, sem limite.

[?] Os quatro cadastros de notas fiscais (pendentes, itens pendentes, entradas confirmadas e
itens confirmados) não constam do dicionário de dados do acervo: não há, no corpus, nem
chave declarada, nem regra de duplicidade, nem capacidade para eles.

### RN-09 — Confirmar abate a quantidade do item do saldo do contrato e do saldo pendente do pedido

Ao confirmar, a quantidade do item é subtraída do saldo de notas fiscais do contrato (o
contrato do fornecedor, daquela coordenadoria, daquela subclasse e daquele gênero) e do
saldo pendente do item do pedido; os dois registros são travados antes de regravar. Quando
a data da nota é anterior ao início da vigência do contrato encontrado, o contrato **não**
é abatido — só o pedido segue o caminho normal.

[?] O contrato é procurado pela combinação que inclui o ano, o mês e o dia do **limite** do
contrato iguais à data da nota. Se a data da nota tem de coincidir com o limite do contrato
para que o abatimento aconteça, isso não está explicado no corpus. E a leitura do item da
nota leva a subclasse e o gênero zerados, sem que o acervo diga se zero restringe ou libera
esses campos.

[?] Fora da vigência do contrato o contrato não é abatido, mas o item e o cabeçalho do
pedido são: não dá para concluir, pela fonte, se a intenção era não abater nada nesse caso.

### RN-10 — O cabeçalho do pedido só é reescrito quando o pedido está na situação F

O pedido da nota só tem o cabeçalho reescrito quando está marcado com a situação **F**;
nesse caso ele passa a **A** e recebe a matrícula de quem confirmou. Pedido em qualquer
outra situação tem só o item abatido, sem tocar no cabeçalho.

[?] O que as situações F e A significam no negócio não está no acervo.

### RN-11 — A outra marcação retira a nota sem registrá-la como entrada confirmada — e abate as mesmas quantidades

Com a outra marcação, a nota e os seus itens saem da relação de pendentes e a quantidade do
item é abatida do contrato e do pedido como na confirmação; o que não acontece é o registro
da nota como entrada confirmada, que só o caminho da confirmação monta.

[?] Se a marcação é um estorno ou um cancelamento, o esperado seria devolver as quantidades,
e não abatê-las; se é apenas "não registrar", o abatimento é igual ao da confirmação por
desenho. As duas leituras cabem na fonte e o acervo não escolhe uma. Pergunta ao site.

### RN-12 — Nota sem item cadastrado sai da relação de pendentes sem abatimento e sem confirmação

Quando o item da nota não é encontrado, a nota sai da relação de pendentes assim mesmo:
nada é abatido e nada é registrado como entrada confirmada. A retirada deixa o seu registro
de exclusão na auditoria, nos dois caminhos.

[?] A nota desaparece da relação de pendentes sem que a entrada tenha sido confirmada. Pela
fonte não dá para dizer se isso é a limpeza pretendida de notas sem item ou perda de
registro. Pergunta ao site.

### RN-13 — Toda gravação deixa rastro na auditoria

Cada abatimento de contrato ou de pedido, cada nota registrada como entrada confirmada,
cada item registrado e cada retirada de nota ou de item gravam um registro de auditoria com
a operação (inclusão, alteração ou exclusão), a tela de origem (N331T), o cadastro tocado,
a matrícula do funcionário, a estação, a sessão (dia, mês, ano e hora), o tipo de órgão, o
número do processo — a nota fiscal — e o conteúdo anterior e o posterior.

### RN-14 — Falha no banco interrompe a operação

Toda leitura, travamento, gravação ou exclusão que o banco recuse é despachada para a
rotina de comunicação do sistema e interrompe a transação; a operação da linha não é dada
por concluída.

### RN-15 — O acesso do usuário é conferido antes de a tela operar

A tela lê o seu registro de autorização e passa pelas rotinas de segurança e de rota da
sessão antes de qualquer conferência de negócio. Não estando autorizado, a operação não
acontece.

[?] O texto da recusa por falta de permissão não está neste programa: as rotinas de
segurança são comuns, declaradas sem corpo, e a tela só testa o retorno. Por isso o cenário
de recusa por permissão não cita mensagem.

### RN-16 — A conferência da página vem antes da gravação

A tela tem três passagens: a de exibição, que monta as 12 linhas; a de conferência, que só
produz as recusas; e a de gravação. O controlador percorre as 12 linhas na conferência e só
depois repete a volta, linha a linha, quando cada linha é efetivamente executada.

---

## Cenários BDD

```gherkin
Funcionalidade: Confirmar a entrada das notas fiscais do operador logístico

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N331T

  Cenário: RN-01 — a página mostra as notas pendentes do operador logístico
    Dado que o operador logístico tem notas com entrada não confirmada
    Quando abro a N331T informando o grupo e o operador logístico
    Então vejo até 12 notas, cada uma com o número da nota e a marcação
    E em cada linha vejo o pedido com o ano de entrega, o órgão, o fornecedor e o tipo de contrato
    E vejo o nome do operador logístico

  Cenário: RN-02 — abrir a tela sem informar a opção de manutenção
    Quando abro a tela sem informar a opção
    Então a tela abre em consulta

  Cenário: RN-02 — opção de manutenção indisponível
    Quando informo uma opção diferente de ALT e de CON
    Então vejo "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor volta para a opção

  Cenário: RN-03 — grupo não informado
    Quando deixo o grupo em branco
    Então vejo "* Informe o grupo *"
    E o cursor volta para o grupo

  Cenário: RN-03 — grupo de outra coordenadoria
    Dado que a minha sessão tem uma coordenadoria
    Quando informo o grupo de outra coordenadoria
    Então vejo "* usuario sem acesso a outro grupo *"
    E nada é gravado

  Cenário: RN-04 — consulta sem operador logístico
    Quando peço a consulta sem informar o operador logístico
    Então vejo "* Informe o operador logistico *"
    E o cursor volta para o operador logístico

  Cenário: RN-04 — operador logístico sem notas pendentes
    Dado que o operador logístico não tem nenhuma nota com entrada não confirmada
    Quando peço a consulta
    Então vejo "* Nao existem notas com ent.nao confirmada *"

  Cenário: RN-05 — a consulta não grava nada
    Dado que o operador logístico tem notas com entrada não confirmada
    Quando peço a consulta
    Então vejo as notas pendentes
    E nenhuma quantidade é abatida
    E nenhuma nota é registrada como entrada confirmada
    E nenhuma nota nem item sai da relação de pendentes

  Cenário: RN-06 — alterar sem ter consultado antes
    Dado que não consultei essa coordenadoria com esse operador logístico
    Quando peço a alteração
    Então vejo "* Consulte antes de atualizar *"
    E nada é abatido

  Cenário: RN-07 — linha em branco ou com marca desconhecida
    Dado que preenchi uma linha sem número de nota, ou com uma marca que não é C nem E
    Quando a tela processa as linhas
    Então aquela linha não produz efeito nenhum

  Cenário: RN-08 — confirmar a entrada de uma nota pendente
    Dado que a nota está com a entrada não confirmada
    Quando marco a linha com C e confirmo
    Então a nota é registrada como entrada confirmada, com os seus itens
    E a nota e os seus itens saem da relação de pendentes
    E cada retirada fica na auditoria

  Cenário: RN-08 — confirmar uma nota que já está confirmada
    Dado que a nota já consta do registro de entradas confirmadas
    E a nota ainda está na relação de pendentes
    Quando marco a linha com C e confirmo
    Então a nota não é registrada de novo
    E as quantidades são abatidas como na confirmação
    E a nota sai da relação de pendentes

  Cenário: RN-09 — confirmar abate o contrato e o pedido
    Dado que a nota está na vigência do contrato
    Quando marco a linha com C e confirmo
    Então a quantidade do item sai do saldo de notas fiscais do contrato
    E a quantidade pendente do item do pedido é reduzida
    E os dois registros ficam travados e regravados
    E a operação fica na auditoria

  Cenário: RN-09 — nota anterior ao início da vigência do contrato
    Dado que a data da nota é anterior ao início da vigência do contrato
    Quando marco a linha com C e confirmo
    Então o saldo do contrato não é abatido
    E o item do pedido é reduzido assim mesmo

  Cenário: RN-10 — pedido na situação F
    Dado que o pedido da nota está na situação F
    Quando marco a linha com C e confirmo
    Então a quantidade do item do pedido é reduzida
    E o cabeçalho do pedido passa para a situação A, com a matrícula de quem confirmou

  Cenário: RN-10 — pedido em outra situação
    Dado que o pedido da nota não está na situação F
    Quando marco a linha com C e confirmo
    Então só o item do pedido é reduzido
    E o cabeçalho do pedido não é tocado

  Cenário: RN-11 — retirar a nota sem confirmar a entrada
    Dado que a nota está com a entrada não confirmada
    Quando marco a linha com E e confirmo
    Então a nota e os seus itens saem da relação de pendentes
    E a quantidade do item é abatida do contrato e do pedido
    E a nota não é registrada como entrada confirmada

  Cenário: RN-12 — nota sem item cadastrado
    Dado que o item da nota não é encontrado
    Quando marco a linha e confirmo
    Então a nota sai da relação de pendentes
    E nada é abatido
    E nada é registrado como entrada confirmada

  Cenário: RN-14 — falha no banco durante a gravação
    Dado que o banco recusa a gravação
    Quando confirmo a linha
    Então a transação é interrompida com a mensagem de erro do sistema
    E a operação daquela linha não é dada por concluída

  Cenário: RN-15 — operação sem permissão do perfil
    Dado que o meu perfil não autoriza a operação
    Quando confirmo a linha
    Então a tela é abandonada sem gravar
```
