# US — N327T — Confirmação da entrega das notas fiscais de um lote

## Estória

Como **servidor de CRE que confere a entrega das notas fiscais**, quero **informar o
lote de entrega, ver as notas fiscais pendentes daquele lote e confirmar a entrada
das que foram entregues — ou retirá-las da relação de pendentes**, para que **o
contrato e o pedido passem a refletir o que de fato entrou e ninguém continue
esperando por uma nota já tratada**.

A nota fiscal entregue chega ao sistema pendente, presa a um lote. É nesta tela que
a CRE percorre as notas de um lote e decide o destino de cada uma: o que foi
conferido fica registrado como entrada confirmada e sai da relação de pendentes,
junto com os seus itens; o que não for conferido continua pendente e continua sendo
cobrado de quem deve entregar. Sem esta tela, o lote ficaria preso para sempre, e a
quantidade entregue não chegaria ao saldo do contrato nem ao do pedido.

## Contexto

Jornada S000M → N000M → N050M → N300M → N327T.

Ator: servidor de CRE — informa o lote de entrega, confere as notas pendentes
daquele lote e registra a confirmação ou a exclusão das notas.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada são menus: elas só encaminham e não deixam dado
de negócio para esta tela. O que a `N327T` usa — o tipo de órgão, a coordenação
regional escolar, a matrícula, o privilégio e a data do sistema — é o que a entrada
deixou na sessão. Esta tela é a última da jornada: não abre outra tela e não
encaminha registro nem operação adiante, e nada lhe chega de quem a chamou além da
sessão, porque quem a abre é o menu.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela confere, por lote, as notas fiscais pendentes

O operador informa o número do lote de entrega — **14 posições**, informadas em
**quatro grupos** de 2, 2, 6 e 4 — e a tela apresenta as notas fiscais que estão
pendentes naquele lote. A tela abre com o lote que ficou na sessão — o último que o
operador consultou — e ele pode trocá-lo.

A página traz **10 linhas**, e cada linha traz **10 posições**: o número da nota, o
número do pedido, a barra, o ano da entrega, o código e o nome do órgão, o código e
a razão social do fornecedor, o tipo de contrato e a marcação da linha. No alto
ficam o tipo de órgão, a data do sistema, a coordenação regional escolar e o
operador do lote, com o seu nome.

### RN-02 — A tela só trabalha em alteração ou consulta, e abre em consulta

O operador informa em que modo quer trabalhar: **alteração** ou **consulta**. Sem
modo informado, a tela abre em **consulta**. Qualquer outro modo é recusado com
**\* Operacao nao disponivel. Use ALT ou CON \***, com o cursor de volta no campo do
modo, e nada é gravado.

Depois de tratar um lote inteiro, a tela volta sozinha ao modo de consulta: a
alteração vale para a passagem, não fica ligada.

[?] A mensagem da tela chama os dois modos de **ALT** e **CON**, e a sessão guarda
os dois com outros códigos; o corpus não declara a correspondência entre as duas
nomenclaturas. A leitura de que ALT é a alteração e CON é a consulta sai do próprio
texto da mensagem, não de uma declaração da fonte.

### RN-03 — Sem o lote não há o que processar

Sem o número do lote a tela não lista nada e não grava nada: a tentativa é recusada
com **\* Informe o numero do lote \***, com o cursor no lote.

### RN-04 — Em alteração, só o lote que já foi consultado

Em alteração, se o lote informado não for o mesmo que já está na sessão, a recusa é
**\* Consulte antes de atualizar \***, com o cursor no campo do modo. A tela só
altera o lote que já mostrou.

### RN-05 — O lote tem de existir e ser do grupo do servidor

O lote informado é procurado entre as notas pendentes. Se não houver nenhuma nota
pendente com aquele lote, a recusa é **\* Lote nao cadastrado \***. Se o lote
existir, mas estiver registrado para outra coordenação, a recusa é
**\<- Lote de outro grupo \***, com o cursor no lote.

O servidor que chega à tela sem coordenação na sessão não passa por essa conferência
de grupo.

[?] Se um servidor sem coordenação alcança a tela, a conferência de grupo
simplesmente não é feita e qualquer lote passa. Ou esse servidor não chega aqui, ou
a conferência fica em aberto. Pergunta ao site.

### RN-06 — O lote que já não tem nota pendente é avisado

Quando o lote que a tela vai mostrar já não tem nota pendente — por exemplo, logo
depois de todas as suas notas terem sido confirmadas ou excluídas —, a página vem
sem linha alguma e a tela avisa **\* Lote sem notas cadastradas \***, na primeira
linha da página.

### RN-07 — As duas chaves do lote inteiro são alternativas entre si

Além da marcação de cada linha, a tela tem duas chaves que agem sobre o **lote
inteiro**: **confirmar entrega** e **excluir notas**. Marcar as duas é recusado com
**\* Inf.confirmar entrega ou excluir notas \***, com o cursor na chave, e nada é
gravado. Marcar uma delas faz a tela percorrer todas as notas pendentes do lote;
não marcar nenhuma deixa a decisão por conta da marcação de cada linha.

A chave do lote inteiro é lida na primeira linha da página: marcando-a, é o lote
inteiro que é tratado, e não a marcação daquela linha.

### RN-08 — A marcação de cada linha decide o destino daquela nota

Sem nenhuma das duas chaves marcada, quem decide é a marcação da linha, que é
informada junto com o número da nota: **confirmar** aquela nota ou **excluir**
aquela nota. Linha sem número de nota, ou com marcação diferente dessas duas, não
produz efeito nenhum — e não impede as outras linhas da página de seguirem o seu
próprio destino.

### RN-09 — Confirmar registra a entrada da nota que ainda não constava

Ao confirmar, para cada nota, a tela procura a nota no registro das entradas
confirmadas, pelo tipo de órgão, pelo operador e pelo número da nota. Não a
encontrando, ela **registra a entrada confirmada** daquela nota, com a situação de
confirmada, e registra os itens da nota, um a um, a partir dos itens pendentes; ao
final, o item e a nota pendentes são apagados. Nesse caminho os saldos não são
abatidos.

[?] A procura pela entrada já confirmada leva o ano da nota zerado, e o corpus não
diz se um componente zerado deixa de restringir a procura ou exige o zero. Se exigir
o zero, nenhuma entrada confirmada seria encontrada e toda confirmação registraria a
nota de novo — sem limite de repetição.

### RN-10 — Confirmar a nota que já constava abate os saldos

Quando a nota **já constava** do registro das entradas confirmadas, a confirmação
não a registra de novo: ela percorre os itens pendentes da nota e, para cada item,
**abate** a quantidade do saldo de notas fiscais do contrato e do saldo do item do
pedido, reescreve o cabeçalho do pedido quando ele está na situação F e apaga o item
e a nota pendentes.

[?] A guarda que separa os dois caminhos manda **registrar** a nota quando ela ainda
não está confirmada, e esse caminho apaga a nota pendente; o abatimento dos saldos
só existe no caminho da nota que já estava confirmada. Ou a primeira confirmação
deveria abater e as duas guardas ficaram trocadas, ou o abatimento pertence mesmo a
esse outro caso — e a combinação que o alcança, nota já confirmada e ainda pendente,
é resíduo de uma passagem interrompida. A fonte não decide, e as duas leituras cabem
nela. Pergunta ao site.

### RN-11 — Excluir retira as notas e abate os saldos, sem registrar entrada confirmada

Na exclusão, a tela percorre as notas pendentes do lote e, para cada item de cada
nota, abate a quantidade do saldo de notas fiscais do contrato e do saldo do item do
pedido, reescreve o cabeçalho do pedido quando ele está na situação F e apaga o item
e a nota pendentes. O que a exclusão **não** faz é registrar a nota como entrada
confirmada — nem os seus itens.

[?] Se excluir é cancelar uma entrega que não vale mais, o esperado seria devolver as
quantidades ao saldo, e a tela as abate, exatamente como na confirmação da nota já
registrada; se excluir é só "não confirmar", o abatimento igual nos dois caminhos é
por desenho. As duas leituras cabem na fonte. Pergunta ao site.

### RN-12 — O contrato só é abatido quando a data da nota não é anterior ao início da vigência

O contrato é procurado pelo tipo de contrato, pelo fornecedor, pela coordenação,
pela classificação e pelo gênero do item, e pela data-limite igual à data da nota.
Se a data da nota for **anterior** ao início da vigência do contrato, o contrato não
é abatido — mas o item do pedido e o cabeçalho do pedido são tratados do mesmo jeito.

[?] Fora da vigência, não abater o contrato e ainda assim abater o item do pedido não
fecha: ou a intenção era não abater nada nesse caso, ou o contrato fora da vigência
não deveria nem ter sido encontrado. Pergunta ao site.

### RN-13 — O cabeçalho do pedido só é reescrito quando o pedido está na situação F

O cabeçalho do pedido só é tocado quando o pedido está na **situação F**: nesse caso
ele passa à **situação A**. Em qualquer outra situação o cabeçalho fica como está,
embora o item do pedido seja abatido do mesmo jeito. A matrícula de quem operou e a
data da passagem ficam no rastro da operação, não no pedido.

[?] O significado de **F** e de **A** na situação do pedido não está declarado no
corpus, e a tela não os explica ao operador.

### RN-14 — Nota sem item cadastrado não trava a tela

Quando a nota pendente não tem item cadastrado, a tela não recusa e não trava: no
caminho que registra a entrada confirmada, a nota é registrada como confirmada, sem
itens; no caminho do abatimento e nos caminhos de exclusão, a nota é apenas apagada,
sem que nada seja abatido e sem que nenhuma entrada confirmada seja registrada.

[?] A nota desaparecer da relação de pendentes sem entrada confirmada e sem
abatimento pode ser a limpeza pretendida de uma nota sem item, ou perda de registro.
Pela fonte não dá para decidir. Pergunta ao site.

### RN-15 — Toda passagem deixa rastro na auditoria

Cada registro de entrada confirmada, cada abatimento e cada exclusão deixam um
registro na auditoria (`A010T`), com o objeto tratado (a nota, o item, o contrato ou
o pedido), a operação, o valor anterior e o valor posterior — os dois como imagens
do registro, de 300 posições cada — e o contexto da sessão: tipo de órgão,
coordenação, matrícula, terminal, data e hora e o número do processo.

### RN-16 — A consulta não grava nada

Em consulta, a passagem da página é abandonada antes de qualquer gravação: nada é
registrado, nada é abatido e nada é apagado. A consulta também não decide nada por
conta própria — ela só confere o lote e o acesso.

### RN-17 — O acesso e a permissão são conferidos antes de a tela operar

Na abertura, a tela confere se ela existe no cadastro de telas e se a matrícula tem
acesso a ela. Na passagem da mensagem, antes de gravar, ela chama a rota e a
permissão por operação. Se qualquer uma dessas conferências não devolver OK, a
passagem é abandonada: nada é validado, nada é gravado e nada é auditado.

### RN-18 — A página inteira é conferida antes de a gravação começar

A tela percorre as 10 linhas da página conferindo cada uma, e só depois de a
conferência passar é que a gravação começa. Recusada a conferência de qualquer
linha, a gravação não começa e a tela termina sem gravar.

[?] A separação entre a passagem que confere e a passagem que grava vive na rotina
comum de tela, que não veio no lote; pelo programa não dá para afirmar se a primeira
passagem chega a escrever no banco. O que o programa mostra é o portão: errada a
conferência, ele sai antes da passagem de gravação.

---

## Cenários BDD

```gherkin
Funcionalidade: Confirmação da entrega das notas fiscais de um lote

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E a minha sessão carrega o tipo de órgão, a coordenação regional escolar, a matrícula e a data do sistema
    E tenho acesso à tela N327T

  Cenário: A tela lista as notas pendentes do lote
    Dado que estou na tela N327T em consulta
    Quando informo o número de um lote de entrega existente da minha coordenação
    Então vejo até 10 notas pendentes daquele lote, cada uma com o número da nota, o pedido com o ano da entrega, o órgão, o fornecedor e o tipo de contrato
    E vejo no alto o tipo de órgão, a data do sistema, a coordenação e o operador do lote

  Cenário: A tela abre em consulta
    Dado que abro a tela N327T sem informar o modo
    Então ela abre em consulta
    E nada é gravado

  Cenário: Modo diferente de alteração e de consulta
    Dado que estou na tela N327T
    Quando informo um modo que não é alteração nem consulta
    Então vejo "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo do modo
    E nada é gravado

  Cenário: Sem o lote não há o que processar
    Dado que estou na tela N327T
    Quando processo a página sem informar o número do lote
    Então vejo "* Informe o numero do lote *"
    E o cursor fica no lote
    E nada é gravado

  Cenário: Em alteração, só o lote que já foi consultado
    Dado que estou na tela N327T em alteração
    Quando informo um lote diferente do que já está na sessão
    Então vejo "* Consulte antes de atualizar *"
    E o cursor volta ao campo do modo
    E nada é gravado

  Cenário: Lote sem nota pendente
    Dado que estou na tela N327T
    Quando informo um lote que não tem nenhuma nota pendente
    Então vejo "* Lote nao cadastrado *"
    E o cursor fica no lote
    E nada é gravado

  Cenário: Lote de outra coordenação
    Dado que estou na tela N327T
    E tenho coordenação na sessão
    Quando informo um lote registrado para outra coordenação
    Então vejo "* <- Lote de outro grupo *"
    E o cursor fica no lote
    E nenhuma nota do lote é tocada

  Cenário: Lote que ficou sem nota pendente é avisado
    Dado que o lote que está na sessão já não tem nota pendente
    Quando a página da N327T é apresentada
    Então vejo "* Lote sem notas cadastradas *"
    E nenhuma linha da página é preenchida

  Cenário: As duas chaves do lote inteiro não podem ser marcadas juntas
    Dado que estou na tela N327T em alteração
    E o lote já está na sessão
    Quando marco confirmar entrega e excluir notas na mesma página
    Então vejo "* Inf.confirmar entrega ou excluir notas *"
    E o cursor fica na chave
    E nada é gravado

  Cenário: Confirmar a entrega do lote inteiro
    Dado que estou na tela N327T em alteração
    E o lote já está na sessão, com notas pendentes da minha coordenação
    Quando marco confirmar entrega
    Então cada nota pendente do lote que ainda não constava como entrada confirmada passa a constar, com os seus itens
    E as notas e os itens saem da relação de pendentes
    E cada passagem fica registrada na auditoria
    E a tela volta ao modo de consulta

  Cenário: Confirmar a nota que já constava como entrada confirmada abate os saldos
    Dado que a nota pendente do lote já consta do registro das entradas confirmadas
    Quando confirmo a entrega do lote
    Então a quantidade de cada item é abatida do saldo de notas fiscais do contrato e do saldo do item do pedido
    E o cabeçalho do pedido é reescrito quando o pedido está na situação F
    E a nota e os seus itens saem da relação de pendentes
    E nenhuma entrada confirmada é registrada de novo

  Cenário: Excluir as notas do lote inteiro
    Dado que estou na tela N327T em alteração
    E o lote já está na sessão, com notas pendentes da minha coordenação
    Quando marco excluir notas
    Então a quantidade de cada item é abatida do saldo de notas fiscais do contrato e do saldo do item do pedido
    E o cabeçalho do pedido é reescrito quando o pedido está na situação F
    E as notas e os itens saem da relação de pendentes
    E nenhuma nota é registrada como entrada confirmada
    E a tela volta ao modo de consulta

  Cenário: A marcação de uma linha confirma a entrada daquela nota
    Dado que estou na tela N327T em alteração
    E o lote já está na sessão, sem nenhuma das duas chaves marcada
    Quando marco a confirmação na linha de uma nota pendente
    Então aquela nota passa a constar como entrada confirmada, com os seus itens
    E ela e os seus itens saem da relação de pendentes
    E a auditoria registra a passagem

  Cenário: A marcação de uma linha exclui aquela nota
    Dado que estou na tela N327T em alteração
    E o lote já está na sessão, sem nenhuma das duas chaves marcada
    Quando marco a exclusão na linha de uma nota pendente
    Então aquela nota e os seus itens saem da relação de pendentes
    E a quantidade de cada item é abatida do saldo de notas fiscais do contrato e do saldo do item do pedido
    E nenhuma entrada confirmada é registrada para ela

  Cenário: Linha sem marcação não produz efeito
    Dado que estou na tela N327T em alteração
    E o lote já está na sessão
    Quando deixo uma linha sem número de nota ou com uma marcação diferente de confirmar e de excluir
    Então nada é gravado para aquela linha
    E as outras linhas da página seguem o seu próprio destino

  Cenário: O contrato só é abatido quando a data da nota não é anterior ao início da vigência
    Dado que uma nota pendente tem data anterior ao início da vigência do contrato
    Quando essa nota é confirmada já registrada ou excluída
    Então o saldo de notas fiscais do contrato não é abatido
    E o item do pedido e o cabeçalho do pedido são tratados do mesmo jeito

  Cenário: O cabeçalho do pedido só é reescrito quando o pedido está na situação F
    Dado que o pedido de uma nota pendente está na situação F
    Quando essa nota é confirmada já registrada ou excluída
    Então o pedido passa à situação A
    E um pedido em outra situação tem o item abatido sem que o cabeçalho mude

  Cenário: Nota sem item cadastrado não trava a tela
    Dado que a nota pendente não tem item cadastrado
    Quando confirmo a entrada dessa nota ainda não confirmada
    Então a nota é registrada como entrada confirmada, sem itens
    E quando a nota sem item é excluída ou confirmada já registrada, ela sai da relação de pendentes sem abatimento

  Cenário: A consulta não grava nada
    Dado que estou na tela N327T em consulta
    E o lote já está na sessão, com notas pendentes
    Quando percorro a página
    Então nenhuma nota é registrada como entrada confirmada
    E nenhuma quantidade é abatida
    E nenhuma nota nem item sai da relação de pendentes

  Cenário: Nada é gravado quando a conferência de acesso não devolve OK
    Dado que estou na tela N327T
    Quando a conferência da tela, a rota ou a permissão por operação não devolve OK
    Então a passagem é abandonada
    E nada é gravado
    E nenhum registro de auditoria é criado

  Cenário: A conferência da página vem antes da gravação
    Dado que estou na tela N327T em alteração
    E uma linha da página é recusada na conferência
    Quando a página termina de ser conferida
    Então a gravação não começa
    E nada é gravado para a página

  Cenário: Toda passagem deixa rastro na auditoria
    Dado que confirmei ou excluí notas na tela N327T
    Quando a gravação termina
    Então existe um registro de auditoria para cada nota, item, contrato e pedido tratado
    E cada registro traz a operação, o valor anterior e o valor posterior
    E o tipo de órgão, a coordenação, a matrícula, o terminal, a data e a hora
```
