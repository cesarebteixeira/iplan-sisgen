# US — E947T — Estornar o cancelamento ou o bloqueio do cartão de referência do aluno

## Estória

Como **servidor da coordenação regional escolar (CRE)**, quero **desfazer o
cancelamento ou o bloqueio do cartão de referência de um aluno**, para que **o
cartão volte à situação em que estava antes da baixa e a contagem do contrato deixe
de contar como cancelado um cartão que continua com o aluno**.

O cancelamento e o bloqueio — feitos pela tela irmã `E940T` — tiram o cartão de
circulação: ele deixa de contar como entregue ou como não entregue e passa a contar
como cancelado no contrato de referência. Quando essa baixa foi indevida, ou quando
a pendência que a motivou deixou de existir, nada volta sozinho: o aluno fica sem
cartão, o contrato fecha com um cancelado a mais e um entregue ou pendente a menos,
e a coordenação segue cobrando uma pendência que já não existe. O estorno é a
operação que desfaz isso — devolve a situação anterior do cartão e o retira da
contagem dos cancelados —, e é por isso que ele existe ao lado da baixa, e não no
lugar dela.

O preço do estorno é o motivo: desfazer a baixa apaga a justificativa que a
acompanhava. Por isso ele serve para a baixa indevida, e não para reativar um cartão
legitimamente bloqueado — para esse caso existe a substituição do cartão, na
`E945T`, que mantém o bloqueio de pé e emite outro cartão.

## Contexto

Jornada S000M → E000M → E900M → E947T.

Ator: servidor de CRE — desfaz, um cartão por vez, o cancelamento ou o bloqueio de
um cartão de referência do seu órgão, e acerta a contagem do contrato.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas do meio do caminho — a `E000M` e a `E900M` — são menus: elas não
passam registro nem operação para a tela de destino, e a opção que abre a `E947T`
apenas entrega o controle a ela. Por isso a tela abre sem os dados do contrato e do
cartão: quem os informa é o operador. O que ela aproveita da sessão é o perfil do
servidor — a matrícula, o tipo de órgão, o acesso, o privilégio e, se a sessão
mantiver, o órgão filho e a coordenação regional escolar (RN-05).

A tela não é menu e não tem lista: trata **um cartão por vez**, identificado pelo
órgão filho, pela coordenação, pelo contrato, pela situação a estornar, pela
matrícula do aluno e pelo número do cartão. Ela não encadeia para nenhuma outra
tela: reabre a si mesma para pedir a confirmação e para mostrar o resultado, sem
passar registro nem operação adiante (RN-18). Também não há comparação com a tela
de origem que mude o comportamento dela: o único código de tela que ela considera é
o da tela de retorno, que devolve o controle a quem o tiver preenchido (RN-17).

Esta é a operação inversa da baixa: a `E940T` cancela ou bloqueia o cartão e soma
um aos cancelados do contrato; esta devolve a situação anterior, apaga o motivo e
subtrai esse um. Ela não substitui o cartão bloqueado — isso é a `E945T`.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O que a tela pede e o que ela mostra

A tela identifica o cartão por **sete dados digitados**: o **órgão filho (SDI)**,
com 8 dígitos; a **coordenação regional escolar (CRE)**, com 2; o **ano do
contrato**, com 4; o **número do contrato**, com 2; a **situação a estornar** —
cancelado ou bloqueado, com 1 caractere —; a **matrícula do aluno**, com 13; e o
**número do cartão**, com 17. Ao lado deles a tela recebe ainda o **código do
fornecedor** (4) e o **código do motivo** (2), e a **resposta de confirmação**
(1 caractere).

Sem digitação, a tela mostra o **nome do órgão filho**, a **data do sistema**, a
**vigência do contrato** — as datas de início e de limite, no formato dia/mês/ano,
separadas por " a " —, a **razão social do fornecedor do contrato**, a **situação
por extenso** (*Cancelado* ou *Bloqueado*), a **descrição do motivo** e uma **linha
de mensagens**.

### RN-02 — Oito campos digitados passam pela conferência numérica antes de qualquer consulta

O órgão filho, a coordenação, o ano do contrato, o número do contrato, o código do
fornecedor, a matrícula do aluno, o número do cartão e o código do motivo são
tratados como número: o que estiver em branco vira zero, os zeros à esquerda são
descartados e o que não for número é recusado. O que não passa por essa conferência
não chega ao cadastro.

[?] A conferência numérica recusa o campo, mas a rotina que devolve o cursor ao
campo recusado só tem caso para o órgão filho, o número do contrato, o ano do
contrato, a matrícula do aluno e o número do cartão. Recusada a coordenação, o
código do fornecedor ou o código do motivo, o cursor não é reposicionado por essa
rotina, e o corpus não diz onde ele fica. Pergunta ao site.

### RN-03 — A tela desfaz a baixa do cartão: devolve a situação anterior e apaga o motivo

A tela tem uma operação só: o **estorno** do cancelamento ou do bloqueio de um
cartão de referência. Ela devolve ao cartão a situação que ele tinha antes da baixa
e apaga o motivo que a justificou; depois acerta a contagem do contrato.

É uma tela que **grava**: altera o cartão, altera a contagem do contrato e deixa um
registro na auditoria. Ela **não exclui** nada e **não inclui** cartão nenhum — as
rotinas de exclusão existem declaradas para todos os cadastros que a tela enxerga, e
nenhuma delas é executada. Também não altera o contrato, o órgão, o fornecedor nem a
lista de motivos.

### RN-04 — A tela só executa na opção de alteração

O estorno exige a opção de manutenção em **alteração**. Informada qualquer outra —
inclusive em branco —, a recusa é **\* Operacao nao disponivel. Use ALT \***, com o
cursor de volta ao campo da opção, e nada é gravado. Esta tela não tem modo de
consulta.

[?] A opção de manutenção é preenchida pelo próprio programa a cada exibição da
tela, com o código da alteração. Se o operador não puder sobrescrever esse campo, a
recusa por opção indisponível nunca acontece. O que define se o campo é digitável
está na máscara da tela, que não está no acervo. Pergunta ao site.

### RN-05 — O órgão filho é obrigatório, tem de existir, e o alcance do servidor o limita

O órgão filho (SDI) é informado pelo operador. Em branco, a recusa é
**\* Informe o orgao \***; não cadastrado, a recusa é **\* Orgao nao cadastrado \***,
com o cursor no campo do órgão.

Se a sessão tem um **órgão filho** preso ao servidor, a tela só aceita esse órgão:
informar outro é recusado com **\* Usuario sem acesso a outro orgao \***. E se a
sessão tem uma **coordenação regional escolar**, ela tem de ser a do órgão
informado — sendo outra, a recusa é
**\* Usuario sem acesso ao grupo deste Orgao \***. A coordenação conferida nessa
segunda recusa é a do cadastro do órgão, não a digitada (RN-08).

Quando o órgão informado é o mesmo da transmissão anterior, a tela não relê o
cadastro e aproveita o que a abertura já tinha carregado.

[?] O órgão filho e a coordenação presos ao servidor vêm de uma área de trabalho
compartilhada entre os programas, e em todo o acervo expandido nenhum programa
atribui a ela um órgão filho diferente de zero — 53 arquivos citam o campo, e a
única atribuição é a de zerá-lo. Ou as duas recusas de alcance nunca disparam (e
qualquer órgão e qualquer coordenação cadastrados passam), ou quem preenche essa
área está fora do que se conseguiu ler: a conferência de segurança copia a área
inteira de um programa para o outro, o que levaria os valores junto. Não escolho um
dos dois lados. Pergunta ao site.

### RN-06 — O contrato é obrigatório, tem de existir e tem de estar aberto

O contrato de referência é identificado pelo **ano** e pelo **número** informados.
Sem o número, a recusa é **\* Informe o Contrato \***, com o cursor de volta ao
campo do contrato. Informado, o sistema procura o contrato pelo tipo de órgão da
secretaria, pelo ano e pelo número; não achando, a recusa é
**\* Contrato nao cadastrado \***.

Só o número é conferido em branco: o ano em branco não gera aviso próprio e faz a
procura por um contrato de ano zero, que cai na recusa de contrato não cadastrado.

E o estorno não é permitido em contrato fechado: estando o contrato marcado como
**fechado**, a recusa é **\* Contrato fechado \***, com o cursor no campo do
contrato. Só contrato aberto aceita o estorno.

### RN-07 — A situação pedida tem de ser cancelamento ou bloqueio, e tem de ser a do cartão

O operador diz qual das duas baixas ele quer desfazer: o **cancelamento** ou o
**bloqueio**. Qualquer outra coisa é recusada com
**\* Inf.cartao cancelado ou bloqueado com C ou B \***, com o cursor de volta ao
campo.

Encontrado o cartão, a situação pedida é comparada com a que o cartão realmente
tem. Pedindo o estorno de um **cancelamento** para um cartão **bloqueado**, a recusa
é **\* Cartao bloqueado \***; pedindo o estorno de um **bloqueio** para um cartão
**cancelado**, a recusa é **\* Cartao cancelado \***. As duas devolvem o cursor ao
campo da situação.

### RN-08 — A coordenação, o fornecedor e o motivo que a tela mostra vêm dos cadastros

Quando o órgão informado é diferente do órgão da transmissão anterior, o sistema lê
o cadastro do órgão e copia dele a **coordenação regional escolar** e o **nome do
órgão**; achado o contrato, copia do cadastro do fornecedor a **razão social** e
mostra o **código do fornecedor** do contrato; e achado o cartão, mostra o **código
do motivo** e a **descrição do motivo** que estão ligados a ele.

[?] A coordenação regional escolar, o código do fornecedor e o código do motivo são
campos que o operador digita e que a tela confere como número, mas o programa os
sobrescreve com os valores dos cadastros antes de mostrá-los. Ou os três campos são
só de exibição, ou o que o operador digita neles é descartado sem aviso. E quando o
órgão informado é o mesmo da transmissão anterior, a tela não relê o cadastro do
órgão: nesse caso a coordenação digitada é a conferida em RN-05. Pergunta ao site.

### RN-09 — A matrícula é obrigatória, e o aluno não pode ter cartão em circulação

A **matrícula do aluno** é obrigatória: em branco, a recusa é
**\* Informe a Matricula do Aluno \***, com o cursor de volta ao campo.

Informada a matrícula, o sistema percorre os cartões daquele aluno naquele contrato
e naquele órgão e procura algum que **não** esteja cancelado nem bloqueado — isto é,
um cartão em circulação. Achando, o estorno é recusado com
**\* <- Ja existe cartao ativo para esta matricula \***, com o cursor de volta ao
campo da matrícula. O estorno, portanto, só passa quando todos os cartões do aluno
naquele contrato já estiverem baixados.

[?] A varredura que procura um cartão em circulação depende de parâmetros da rotina
de leitura cujo significado não está no acervo: não concluo se ela percorre mesmo
todos os cartões do aluno naquele contrato e naquele órgão. Pergunta ao site.

### RN-10 — O cartão é localizado pelo número, e o motivo é mostrado

O cartão a estornar é identificado pelo **número do cartão** digitado, junto com o
órgão, a coordenação, o contrato e a matrícula. Não achando o cartão, a recusa é
**\* Matricula nao cadastrada \***, com o cursor de volta ao campo da matrícula.
Achando, a descrição do motivo da baixa é mostrada na tela; não existindo o motivo
no cadastro, a tela segue sem mostrá-lo, sem aviso nenhum.

[?] O número do cartão não tem recusa própria para o caso de vir em branco: ele não
é conferido em branco em nenhum ponto, e a procura por um número de cartão zero cai
na recusa de matrícula não cadastrada — mensagem que aponta o campo da matrícula, e
não o do cartão. Não se conclui do acervo se o número do cartão é digitável ou vem
preenchido por outra via. Pergunta ao site.

### RN-11 — A tela pergunta antes de gravar e reabre ela mesma

Passadas as conferências, a tela não grava: ela mostra o que encontrou — o órgão com
o nome, a coordenação, o contrato com o ano e o número, o fornecedor com a razão
social, a vigência, a matrícula do aluno, o número do cartão, a situação por extenso
e a descrição do motivo — e pergunta **Confirma estorno do cancelamento <S/N> ?** ou
**Confirma estorno do bloqueio <S/N> ?**, conforme a situação pedida, com o cursor
no campo da resposta, reabrindo ela mesma.

Só a resposta **S** grava, na transmissão seguinte. Qualquer outra resposta deixa a
tela como estava e não grava nada; e se algum dos **seis dados** que a tela conferiu
for alterado junto com a resposta — órgão filho, número do contrato, ano do
contrato, situação pedida, matrícula do aluno ou número do cartão — a confirmação é
cancelada e o operador recomeça do zero.

[?] O que liga as duas transmissões — a marca da passagem, os dados que a tela
encontrou e a mensagem da pergunta — vive na área de trabalho que a tela mantém de
uma transmissão para a outra. Se essa memória não sobreviver à reabertura da tela, a
confirmação nunca fecha e o estorno não acontece. Não escolho um dos dois lados.
Pergunta ao site.

### RN-12 — O que fica gravado no cartão

Confirmada a operação, o cartão recebe de volta a **situação que ele tinha antes da
baixa** — a que ficou guardada nele quando foi cancelado ou bloqueado — e o **motivo
é apagado**: o código do motivo volta a zero e a guarda da situação anterior é
limpa. A situação de baixa (cancelada ou bloqueada) deixa de existir no cartão, e
nenhum outro dado dele é tocado.

[?] O cartão cuja situação anterior ficou em branco não tem caso próprio: a tela
devolve o branco ao cartão e, na contagem (RN-13), ele passa a contar como entregue.
Se essa falta de situação é possível no site, o cartão volta sem situação nenhuma e
a contagem ganha um entregue que não existe. Pergunta ao site.

### RN-13 — A contagem do contrato acompanha o estorno

Junto com o cartão, a tela acerta a contagem do contrato para aquela coordenação e
aquele órgão: a quantidade de **cancelados desce um** e o cartão entra na quantidade
de **não entregues** quando a situação que ele recuperou é a de não entregue; em
qualquer outra situação — inclusive em branco — ele entra na quantidade de
**entregues**. A quantidade total de cartões do contrato não muda: a tela não tira
nem põe cartão.

### RN-14 — Sem o registro de contagem, o cartão é estornado e a contagem não é corrigida

O acerto da contagem depende de existir o registro de contagem do contrato naquela
coordenação e naquele órgão. Não existindo, o cartão é estornado do mesmo jeito, a
contagem não é corrigida e o operador ainda vê a mensagem de sucesso, sem ser
avisado de que a contagem ficou como estava.

### RN-15 — Toda operação fica registrada na auditoria

Cada estorno grava um registro na trilha de auditoria das telas: o cadastro
auditado (o cartão), a tela de origem, a operação de alteração, o **conteúdo
anterior** e o **posterior** do cartão, a matrícula do funcionário, o terminal, o
dia, o mês, o ano e a hora da sessão, o tipo de órgão e a coordenação regional
escolar. O número do processo levado à auditoria é a **matrícula do aluno**. O
conteúdo anterior é o cartão como estava, com a situação da baixa e o motivo; o
posterior, com a situação devolvida e o motivo apagado.

A auditoria é gravada **antes** do cartão: não passando a auditoria, o cartão não é
gravado.

[?] O código de manutenção do registro de auditoria sai com o valor "A", enquanto o
campo de operação grava o código da alteração. A rotina que traduziria um no outro
nunca é executada neste programa. Qual dos dois o consumidor da auditoria lê é
pergunta ao site.

### RN-16 — A operação só acontece se a tela e o perfil autorizarem

Antes de conferir e de gravar, a transmissão passa pela **rota do sistema**, que lê
o cadastro de telas pela tela e confere se ela aceita a operação pedida — e a tela
informa, para isso, que a operação é de alteração. Não estando a tela cadastrada, a
recusa é **\* Tela nao cadastrada \***; não aceitando a tela a operação, a recusa é
**\* Operacao nao disponivel \***.

Em seguida a transmissão passa pela **conferência de autorização** da operação, que
leva em conta a matrícula do funcionário, o código de acesso, o privilégio, o tipo
de órgão e a coordenação regional escolar da sessão. Não vindo a autorização, a
recusa é uma das mensagens da conferência de acesso —
**\* Acesso negado para esta matricula \***, **\* Acesso negado para esta operacao \***,
**\* Tela nao disponivel \*** ou **\* Acesso a pagina 2 negado \*** — e nada é
gravado.

### RN-17 — O código da tela de retorno devolve o controle àquela tela

A tela leva à rota do sistema o código da **tela de retorno** que veio com ela.
Quando esse código vem preenchido, a rota devolve o controle àquela tela e esta não
processa nada: nenhuma conferência de negócio é feita, nada é gravado, e o operador
sai daqui para a tela indicada. Só com esse código em branco é que esta tela segue e
processa. Quem preenche o código da tela de retorno é quem chamou esta tela: ele não
é digitado nem limpo aqui.

[?] Nesta jornada a única porta até a tela é a opção do menu `E900M`, que não leva
registro nenhum junto; não há, portanto, quem preencha esse código. Se o campo vier
preenchido mesmo assim — os campos das telas da família ficam na mesma posição na
área da transação —, o estorno seria abandonado e o operador iria para aquela tela
sem que nada tivesse sido processado. Não escolho um dos dois lados. Pergunta ao
site.

### RN-18 — A tela não encadeia: ela reabre a si mesma

A tela não passa registro nem operação para nenhuma outra tela. Ela reabre a si
mesma duas vezes: uma para pedir a confirmação, com o que encontrou, e outra ao
terminar, para mostrar a mensagem do resultado — **\* Cancelado estornado \***,
quando a baixa desfeita era o cancelamento, e **\* Bloqueio estornado \***, quando
era o bloqueio.

---

## Cenários BDD

```gherkin
Funcionalidade: Estorno do cancelamento ou do bloqueio do cartão de referência do aluno

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E947T

  Cenário: RN-03 — estornar o cancelamento do cartão de um aluno
    Dado que estou na E947T em alteração e o contrato está aberto
    Quando informo o órgão filho, a coordenação, o contrato, a situação cancelado, a matrícula do aluno e o número do cartão cancelado
    E a tela me pede a confirmação
    E respondo S
    Então o cartão volta à situação que tinha antes do cancelamento
    E o motivo da baixa é apagado
    E vejo a mensagem "* Cancelado estornado *"
    E continuo na E947T

  Cenário: RN-03 — estornar o bloqueio do cartão de um aluno
    Dado que estou na E947T em alteração e o contrato está aberto
    Quando informo a situação bloqueado para um cartão bloqueado e confirmo com S
    Então o cartão volta à situação que tinha antes do bloqueio
    E o motivo da baixa é apagado
    E vejo a mensagem "* Bloqueio estornado *"
    E continuo na E947T

  Cenário: RN-03 — a tela não inclui nem exclui cartão
    Dado que estou na E947T
    Quando a operação termina
    Então nenhum cartão é incluído ou excluído
    E nenhum contrato, órgão, fornecedor ou motivo é alterado

  Cenário: RN-11 — a tela mostra o que encontrou e pergunta antes de gravar
    Dado que os dados informados passaram pelas conferências
    Quando a tela confere a operação
    Então vejo o órgão com o nome, a coordenação, o contrato com o ano e o número, o fornecedor com a razão social, a vigência, a matrícula do aluno, o número do cartão, a situação por extenso e a descrição do motivo
    E a tela me pede a confirmação, com o cursor no campo da resposta
    E nada foi gravado ainda

  Cenário: RN-11 — resposta diferente de S não grava
    Dado que a tela me pediu a confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a tela volta ao estado anterior
    E nada é gravado

  Cenário: RN-11 — mudar um dado junto com a confirmação cancela o estorno
    Dado que a tela me pediu a confirmação
    Quando respondo S alterando o órgão, o número do contrato, o ano do contrato, a situação pedida, a matrícula do aluno ou o número do cartão
    Então a confirmação é cancelada
    E nada é gravado

  Cenário: RN-02 — campo digitado que não é número
    Quando informo um órgão filho, uma coordenação, um contrato, um código de fornecedor, uma matrícula, um número de cartão ou um código de motivo que não é número
    Então a tela recusa o campo antes de consultar o cadastro
    E nada é gravado

  Cenário: RN-04 — opção de manutenção diferente de alteração
    Quando informo uma opção de manutenção diferente de alteração
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: RN-05 — órgão filho não informado
    Quando deixo o órgão filho em branco
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor fica no campo do órgão filho
    E nada é gravado

  Cenário: RN-05 — órgão filho não cadastrado
    Quando informo um órgão filho que não existe
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão filho
    E nada é gravado

  Cenário: RN-05 — órgão filho diferente do vinculado ao servidor
    Dado que a sessão tem um órgão filho preso ao meu usuário
    Quando informo outro órgão filho
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E nada é gravado

  Cenário: RN-05 — órgão filho de outra coordenação
    Dado que estou vinculado a uma coordenação regional escolar
    Quando informo um órgão filho cuja coordenação é outra
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste Orgao *"
    E nada é gravado

  Cenário: RN-06 — contrato não informado
    Dado que deixei o número do contrato em branco
    Quando confirmo a tela
    Então vejo a mensagem "* Informe o Contrato *"
    E o cursor fica no campo do contrato
    E nada é gravado

  Cenário: RN-06 — contrato não cadastrado
    Dado que informei ano e número de contrato que não existem para a minha secretaria
    Quando confirmo a tela
    Então vejo a mensagem "* Contrato nao cadastrado *"
    E nada é gravado

  Cenário: RN-06 — contrato fechado
    Dado que o contrato informado está fechado
    Quando confirmo a tela
    Então vejo a mensagem "* Contrato fechado *"
    E o cursor fica no campo do contrato
    E nada é gravado

  Cenário: RN-07 — situação pedida diferente de cancelamento e de bloqueio
    Quando informo uma situação que não é cancelar nem bloquear
    Então vejo a mensagem "* Inf.cartao cancelado ou bloqueado com C ou B *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: RN-07 — cancelamento pedido para um cartão bloqueado
    Dado que o cartão informado está bloqueado
    Quando peço o estorno de um cancelamento
    Então vejo a mensagem "* Cartao bloqueado *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: RN-07 — bloqueio pedido para um cartão cancelado
    Dado que o cartão informado está cancelado
    Quando peço o estorno de um bloqueio
    Então vejo a mensagem "* Cartao cancelado *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: RN-09 — matrícula do aluno não informada
    Quando deixo a matrícula do aluno em branco
    Então vejo a mensagem "* Informe a Matricula do Aluno *"
    E o cursor fica no campo da matrícula
    E nada é gravado

  Cenário: RN-09 — o aluno ainda tem cartão em circulação
    Dado que o aluno tem, naquele contrato e naquele órgão, um cartão que não está cancelado nem bloqueado
    Quando peço o estorno de outro cartão do mesmo aluno
    Então vejo a mensagem "* <- Ja existe cartao ativo para esta matricula *"
    E o cursor volta ao campo da matrícula
    E nada é gravado

  Cenário: RN-10 — cartão não encontrado
    Dado que não existe cartão com o número informado para aquela matrícula, aquele contrato e aquele órgão
    Quando confirmo a tela
    Então vejo a mensagem "* Matricula nao cadastrada *"
    E o cursor volta ao campo da matrícula
    E nada é gravado

  Cenário: RN-12 — o cartão volta à situação anterior e perde o motivo
    Dado que o cartão está cancelado ou bloqueado, com o motivo registrado
    Quando confirmo o estorno
    Então o cartão recupera a situação que tinha antes da baixa
    E o código do motivo volta a zero
    E nenhum outro dado do cartão é alterado

  Cenário: RN-13 — a contagem do contrato acompanha o estorno
    Dado que existe a contagem do contrato para aquela coordenação e aquele órgão
    Quando confirmo o estorno
    Então a quantidade de cancelados desce um
    E o cartão entra na quantidade de não entregues, se a situação recuperada é a de não entregue
    E entra na quantidade de entregues em qualquer outra situação
    E a quantidade total de cartões do contrato não muda

  Cenário: RN-14 — sem registro de contagem, o cartão é estornado e a contagem não muda
    Dado que não existe registro de contagem para o contrato, a coordenação e o órgão
    Quando confirmo o estorno
    Então o cartão é estornado
    E a contagem do contrato não é corrigida
    E vejo a mensagem de sucesso mesmo assim

  Cenário: RN-15 — toda operação fica registrada na auditoria
    Quando confirmo um estorno
    Então fica um registro na auditoria, com a tela de origem, a operação de alteração, o cartão antes e depois, a matrícula do funcionário, a data e a hora da sessão e a matrícula do aluno como número do processo
    E a auditoria é gravada antes do cartão

  Cenário: RN-16 — a tela não está cadastrada ou não aceita a operação
    Dado que a tela não está cadastrada, ou não aceita a operação de alteração
    Quando confirmo a tela
    Então vejo a mensagem "* Tela nao cadastrada *" ou "* Operacao nao disponivel *"
    E nada é gravado

  Cenário: RN-16 — operação não autorizada para o perfil
    Dado que o meu perfil não tem a autorização para a operação
    Quando confirmo a tela
    Então o sistema recusa a operação com a mensagem da conferência de acesso
    E nada é gravado

  Cenário: RN-17 — tela de retorno preenchida devolve o controle
    Dado que a tela veio com o código da tela de retorno preenchido
    Quando confirmo a tela
    Então o controle volta para aquela tela
    E esta tela não confere nada e não grava nada

  Cenário: RN-18 — a tela reabre a si mesma
    Dado que confirmei o estorno com S
    Quando a operação termina
    Então a tela E947T é reaberta com a mensagem do resultado
    E nenhuma outra tela é aberta no lugar dela
```
