# US — E940T — Cancelar ou bloquear o cartão de referência do aluno

## Estória

Como **servidor da coordenação regional escolar**, quero **tirar de circulação o
cartão de referência de um aluno de um contrato, cancelando-o ou bloqueando-o com o
motivo registrado**, para que **o cartão que não pode mais circular deixe de contar
como entregue ou como pendente e a coordenação enxergue a situação real do contrato**.

O cancelamento e o bloqueio são a baixa do cartão: é por esta tela que se tira o
cartão do aluno quando ele se perde, é usado indevidamente ou o aluno sai da escola.
O que fica gravado é a situação do cartão e o motivo que a provocou — e é esse motivo
que a coordenação e a auditoria leem depois, quando alguém pergunta por que o aluno
ficou sem cartão. Sem a baixa, o contrato continua contando como entregue ou pendente
um cartão que não existe mais, e a cobrança da pendência sai contra quem não deve.

## Contexto

Jornada S000M → E000M → E900M → E940T.

Ator: servidor da CRE — tira de circulação o cartão de referência de um aluno de um
contrato do seu órgão, dizendo se é cancelamento ou bloqueio e por qual motivo.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A tela não é menu e não tem lista: ela trata **um cartão por vez**, identificado pelo
órgão filho (SDI), pela coordenação regional escolar, pelo contrato, pela matrícula do
aluno e pelo número do cartão. Chega-se a ela encadeada pela tela anterior, que já
traz o contrato e o órgão; e é ela que encadeia para a tela das justificativas
(`E935T`) ou reabre ela mesma, para pedir a confirmação e para mostrar o resultado. O
que a origem decide sobre esta tela está na RN-12; o que ela entrega à tela seguinte,
na RN-13.

Esta é a operação inversa da do estorno: esta baixa o cartão e joga a quantidade para
os cancelados; o estorno, feito por outra tela do mesmo menu, devolve a quantidade e a
situação anterior. O cadastro de cartões é o mesmo que as telas irmãs mantêm — a de
entrega registra a entrega, esta baixa o cartão e a do estorno desfaz a baixa.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela baixa o cartão: cancelamento ou bloqueio, com o motivo

A tela tem uma operação só, em duas formas: **cancelar** o cartão de referência do
aluno e **bloquear** o cartão. As duas tiram o cartão de circulação e dizem a mesma
coisa à contagem do contrato; o que muda é a situação que fica gravada no cartão —
**cancelado** ou **bloqueado** — e o motivo informado pelo operador.

A tela guarda também a situação que o cartão tinha antes da baixa, para que o estorno
possa devolvê-lo à situação em que estava. Ela não exclui o cartão, não cria cartão e
não mexe na entrega: ela troca a situação dele e registra o motivo.

### RN-02 — O que a tela mostra e o que ela grava

A tela mostra o órgão filho (SDI) com o seu nome, a coordenação regional escolar, o
contrato — ano e número —, o fornecedor do contrato com a sua razão social, a vigência
do contrato, a matrícula do aluno, o número do cartão, a situação pedida em texto
(*Cancelar* ou *Bloquear*), a descrição do motivo e uma linha de mensagens. A vigência
é montada das datas de início e de limite do contrato, no formato dia/mês/ano, com as
duas datas separadas por " a ".

O que ela grava é a **situação do cartão**, o **motivo** ligado a ele e a **contagem do
contrato** daquela coordenação e daquele órgão. Nada mais é gravado, alterado ou
excluído: nem o contrato, nem o órgão, nem o fornecedor, nem a lista de motivos.

O cadastro de cartões está dimensionado para **2 milhões de registros**; o de contratos,
para **mil**; o de motivos, para **cem**; e o de contagem do contrato, para **dez mil**.
São **capacidades** (o máximo esperado no dimensionamento), não volumes cadastrados.

[?] O fornecedor é um campo da tela que passa pela edição numérica, mas o programa o
sobrescreve com o fornecedor do contrato antes de mostrá-lo. Ou o campo é só de
exibição, ou o que o operador digita nele é descartado sem aviso. Pergunta ao site.

### RN-03 — A tela só aceita a alteração

A operação exige a opção de manutenção em **alteração**. Informada qualquer outra —
inclusive em branco —, o sistema recusa com **\* Operacao nao disponivel. Use ALT \***,
devolve o cursor ao campo da opção e não processa mais nada naquela transmissão. Esta
tela não tem modo de consulta.

[?] A opção de manutenção é preenchida pelo próprio programa a cada exibição da tela,
com o código da alteração. Se o operador não puder sobrescrever esse campo, a recusa
por opção indisponível nunca acontece. O que define se o campo é digitável está na
máscara da tela, que não está no acervo. Pergunta ao site.

### RN-04 — O órgão e a coordenação têm de estar cadastrados e no alcance do usuário

O órgão filho (SDI) é informado pelo operador. Em branco, a recusa é
**\* Informe o Orgao \***; não cadastrado, a recusa é **\* Orgao nao cadastrado \***,
com o cursor no campo do órgão.

A coordenação regional escolar não é conferida do jeito que o operador a digitou: o
sistema lê a coordenação que está no cadastro do órgão filho informado e é ela que vale
dali em diante. Se o vínculo do usuário tem uma coordenação regional escolar, o órgão
informado só passa se a coordenação dele for a mesma; sendo outra, a recusa é
**\* Usuario sem acesso ao grupo deste Orgao \***. E se o vínculo do usuário tem um
órgão filho, informar outro órgão é recusado com
**\* Usuario sem acesso a outro orgao \***.

[?] O órgão filho do vínculo do usuário é gravado no sistema pela entrada, mas a tela o
procura num lugar que, em todo o acervo expandido, só aparece zerado. Ou a recusa por
"outro órgão" nunca dispara — e qualquer órgão cadastrado passa —, ou quem preenche
esse lugar está fora do que se conseguiu ler. Não escolho um dos dois lados. Pergunta ao
site.

[?] A tela tem o rótulo COORD.REG.ESCOLA num campo que o programa sobrescreve com a
coordenação lida no cadastro do órgão. Ou o campo é só de exibição, ou o que o operador
digita ali é descartado sem aviso. E quando o órgão informado é o mesmo da transmissão
anterior, a tela não relê o cadastro do órgão: nesse caso a coordenação digitada é a
conferida. Pergunta ao site.

### RN-05 — O contrato é obrigatório, tem de existir e tem de estar aberto

O contrato de referência é identificado pelo ano e pelo número informados. Sem o
número, a recusa é **\* Informe o Contrato \***, com o cursor de volta ao campo do
contrato. Informado, o sistema procura o contrato pelo tipo de órgão da secretaria da
sessão, pelo ano e pelo número; não achando, recusa com
**\* Contrato nao cadastrado \***.

Só o número é conferido em branco: o ano em branco não gera aviso próprio e faz a
procura por ano zero, que cai na recusa de contrato não cadastrado.

E o cancelamento e o bloqueio não são permitidos em contrato fechado: estando o
contrato marcado como fechado, a recusa é **\* Contrato fechado \***, com o cursor no
campo do contrato. Só contrato aberto aceita a baixa do cartão.

### RN-06 — O cartão sai do cadastro do aluno, e o que já está baixado não se baixa de novo

O operador diz o que quer fazer com o cartão: cancelar ou bloquear. Qualquer outra
coisa é recusada com **\* Informe cancelar ou bloquear com C ou B \***, com o cursor de
volta ao campo.

A matrícula do aluno é obrigatória: em branco, a recusa é
**\* Informe a Matricula do Aluno \***. Informada a matrícula, o sistema percorre os
cartões daquele aluno naquele contrato e naquele órgão. Não encontrando nenhum, a
recusa é **\* Matricula nao cadastrada \***, com o cursor de volta ao campo da
matrícula.

O cartão que já está **cancelado** ou **bloqueado** é pulado na varredura: a baixa
recai sobre um cartão que ainda está em circulação — entregue ou não entregue. Só
quando **todos** os cartões do aluno naquele contrato já estiverem baixados é que a
tela recusa, com **\* Cartao ja cancelado \*** ou **\* Cartao ja bloqueado \***,
conforme a situação do último cartão percorrido.

[?] A mensagem de recusa é a do **último** cartão percorrido, e a varredura segue a
ordem da chave do cadastro: quando o aluno tem cartões cancelados e bloqueados ao mesmo
tempo, qual das duas mensagens aparece depende dessa ordem, e não do conjunto. O
alcance da varredura também depende de parâmetros da rotina de leitura cujo significado
não está no acervo: não concluo se ela percorre mesmo todos os cartões do aluno naquele
contrato. Pergunta ao site.

### RN-07 — O motivo é obrigatório e tem de estar cadastrado

A baixa exige o motivo: em branco, a recusa é **\* Informe a justificativa \***. O
sistema procura o motivo informado na lista de justificativas; não achando, a recusa é
**\* Justificativa nao cadastrada \***, com o cursor de volta ao campo. Achando, a
descrição do motivo é mostrada na tela e vai para o cartão.

### RN-08 — A tela pergunta antes de gravar e reabre ela mesma

Recebidos os dados, a tela não grava: ela confere tudo, mostra o que encontrou — o
órgão com o nome, a coordenação, o contrato, o fornecedor, a vigência, a matrícula, o
número do cartão e a descrição do motivo — e pergunta
**Confirma cancelamento do cartao <S/N> ?** ou **Confirma bloqueio do cartao <S/N> ?**,
com o cursor no campo da resposta, reabrindo ela mesma.

Só a resposta **S** grava, na transmissão seguinte. Qualquer outra resposta deixa a
tela como estava e não grava nada; e se algum dos seis dados que a tela conferiu for
alterado junto com a resposta — órgão, contrato, ano, situação pedida, matrícula ou
motivo — a confirmação é cancelada e o operador recomeça do zero.

[?] O que liga as duas transmissões — a marca da passagem, o motivo encontrado, os
dados conferidos e a mensagem da pergunta — vive na área de trabalho que a tela mantém
de uma transmissão para a outra. Se essa memória não sobreviver à reabertura da tela, a
confirmação nunca fecha e a baixa não acontece. Não escolho um dos dois lados. Pergunta
ao site.

[?] O número do cartão não está entre os seis dados conferidos: alterado junto com a
resposta S, ele não cancela a confirmação e o programa vai procurar o cartão pelo
número novo. Não achando, a tela mostra a mensagem de sucesso — **\* Cartao cancelado \***
ou **\* Cartao bloqueado \*** — sem ter gravado nada. Pergunta ao site.

### RN-09 — O que fica gravado: a situação do cartão e a contagem do contrato

Confirmada a operação, o cartão recebe a nova situação — **cancelado** ou **bloqueado**
— e o motivo informado; a situação que ele tinha antes da baixa fica guardada no
próprio cartão, e é ela que o estorno devolve.

Junto com o cartão, a tela acerta a contagem do contrato para aquela coordenação e
aquele órgão: o cartão sai da quantidade de **entregues** ou da de **não entregues** —
conforme a situação que ele tinha — e entra na quantidade de **cancelados**, que sobe
um. A quantidade total de cartões do contrato não muda: a tela não tira nem põe cartão,
só troca a situação de um.

[?] A quantidade de cancelados sobe um tanto no cancelamento quanto no bloqueio: não há
quantidade separada de bloqueados. Se a secretaria precisa separar cancelados de
bloqueados, esse número não serve. Pergunta ao site.

[?] O cartão que estava em circulação sem situação de entrega gravada não tem caso
próprio: como não é "não entregue", ele sai da quantidade de entregues. Se essa falta
de situação é possível no site, a contagem fica errada. Pergunta ao site.

[?] O ajuste da contagem depende de existir o registro de contagem do contrato naquela
coordenação e naquele órgão. Não existindo, o cartão é baixado do mesmo jeito, a
contagem não é corrigida e o operador ainda vê a mensagem de sucesso. Pergunta ao site.

[?] A tela grava o cartão e, em seguida, ajusta a contagem sem conferir o que a gravação
do cartão devolveu. Se a gravação do cartão falhar e a da contagem não, os dois ficam
fora de passo até alguém corrigir. Pergunta ao site.

### RN-10 — Toda baixa fica registrada na auditoria

Cada cancelamento e cada bloqueio grava um registro na trilha de auditoria das telas: o
cadastro auditado (o cartão), a tela de origem, a operação de alteração, o conteúdo
anterior e o posterior do cartão, a matrícula do funcionário, o terminal, o dia, o mês,
o ano e a hora da sessão, o tipo de órgão e a coordenação regional escolar. O número do
processo levado à auditoria é a **matrícula do aluno**. O conteúdo anterior é o cartão
como estava; o posterior, com a nova situação e o motivo.

[?] O código de manutenção do registro de auditoria sai com o valor "A" enquanto o campo
de operação grava o código da alteração. A rotina que traduziria um no outro nunca é
executada neste programa. Qual dos dois o consumidor da auditoria lê é pergunta ao
site.

### RN-11 — A operação só acontece se a tela e o perfil autorizarem

Antes de conferir e de gravar, a transmissão passa pela rota do sistema, que lê o
cadastro de telas pela tela e confere se ela aceita a operação pedida — e a tela
informa, para isso, que a operação é de alteração. Não estando a tela cadastrada, a
recusa é **\* Tela nao cadastrada \***; não aceitando a tela a operação, a recusa é
**\* Operacao nao disponivel \***. Em seguida a transmissão passa pela conferência de
autorização da operação, que leva em conta a matrícula do funcionário, o código de
acesso, o privilégio, o tipo de órgão e a coordenação regional escolar da sessão. Não
vindo a autorização, a tela para e nada é gravado.

### RN-12 — O código da tela de retorno devolve o controle àquela tela

A tela leva à rota do sistema o código da **tela de retorno** que veio com ela. Quando
esse código vem preenchido, a rota devolve o controle àquela tela e esta não processa
nada: nenhuma conferência de negócio é feita, nada é gravado, e o operador sai daqui
para a tela indicada. Só com esse código em branco é que esta tela segue e processa.

Quem preenche o código da tela de retorno é quem chamou esta tela: ele não é digitado
nem limpo aqui.

[?] O que a tela de retorno faz com o controle, e o que a tela de origem deixa nesse
campo, não se conclui do programa. Se a abertura encadeada carregar junto o código da
tela que chamou a anterior — os campos ficam na mesma posição nas telas da família —,
esta tela devolveria o controle àquela tela e a baixa do cartão nunca seria alcançada
por esse caminho. Não escolho um dos dois lados. Pergunta ao site.

### RN-13 — Pedir a lista de motivos leva à tela de justificativas, em consulta

A tela tem um pedido que não é o de gravar: o de ver a lista de motivos. Feito esse
pedido, a tela não processa a baixa: ela entrega o controle à tela das justificativas
(`E935T`) pedindo a **consulta**, e não grava nada. A tela seguinte abre em consulta por
causa disso, e não em alteração.

O que esta tela entrega é só a operação de consulta: nenhum dado do cartão é levado
junto.

[?] O pedido de consulta é posto na área de trabalho desta tela e levado à área que a
tela seguinte lê; o campo da opção na própria tela não é alterado. Se a tela seguinte
receber a opção em branco, ela abre em consulta do mesmo jeito, por conta própria — o
que não se conclui do acervo é por qual dos dois caminhos a consulta chega. Pergunta ao
site.

---

## Cenários BDD

```gherkin
Funcionalidade: Cancelar ou bloquear o cartão de referência de um aluno de um contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E940T

  Cenário: Cancelar o cartão de um aluno
    Dado que estou na E940T em alteração e o contrato está aberto
    Quando informo o órgão filho, a coordenação, o contrato, a situação cancelar, a matrícula do aluno e o motivo
    E a tela me pede a confirmação
    E respondo S
    Então o cartão do aluno fica cancelado, com o motivo registrado
    E a situação que ele tinha antes fica guardada para o estorno
    E a contagem do contrato tira o cartão dos entregues ou dos não entregues e soma um aos cancelados
    E vejo a mensagem "* Cartao cancelado *"
    E continuo na E940T

  Cenário: Bloquear o cartão de um aluno
    Dado que estou na E940T em alteração e o contrato está aberto
    Quando informo a situação bloquear e confirmo com S
    Então o cartão do aluno fica bloqueado, com o motivo registrado
    E vejo a mensagem "* Cartao bloqueado *"
    E continuo na E940T

  Cenário: A tela mostra os dados do contrato e do motivo antes de gravar
    Dado que os dados informados passaram pelas conferências
    Quando a tela confere a operação
    Então vejo o órgão com o nome, a coordenação, o contrato, o fornecedor do contrato com a razão social, a vigência, a matrícula do aluno, o número do cartão e a descrição do motivo
    E a tela me pede a confirmação, com o cursor no campo da resposta
    E nada foi gravado ainda

  Cenário: A baixa recai sobre um cartão ainda em circulação
    Dado que o aluno tem, nesse contrato e nesse órgão, um cartão cancelado e outro em circulação
    Quando peço a baixa do cartão do aluno
    Então a tela toma o cartão que ainda está em circulação
    E o cartão já cancelado permanece como está

  Cenário: Resposta diferente de S não grava
    Dado que a tela me pediu a confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a tela volta ao estado anterior
    E nada é gravado

  Cenário: Mudar um dado junto com a confirmação cancela a operação
    Dado que a tela me pediu a confirmação
    Quando respondo S alterando um dos dados que a tela conferiu
    Então a confirmação é cancelada
    E nada é gravado

  Cenário: Opção de manutenção diferente de alteração
    Quando informo uma opção de manutenção diferente de alteração
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: Órgão filho não informado
    Quando deixo o órgão filho em branco
    Então vejo a mensagem "* Informe o Orgao *"
    E o cursor fica no campo do órgão filho
    E nada é gravado

  Cenário: Órgão filho não cadastrado
    Quando informo um órgão filho que não existe
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão filho
    E nada é gravado

  Cenário: Órgão filho diferente do vinculado ao usuário
    Dado que o meu vínculo tem um órgão filho
    Quando informo outro órgão filho
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E nada é gravado

  Cenário: Órgão filho de outra coordenação
    Dado que estou vinculado a uma coordenação regional escolar
    Quando informo um órgão filho cuja coordenação é outra
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste Orgao *"
    E nada é gravado

  Cenário: Contrato não informado
    Dado que deixei o número do contrato em branco
    Quando confirmo a tela
    Então vejo a mensagem "* Informe o Contrato *"
    E o cursor fica no campo do contrato
    E nada é gravado

  Cenário: Contrato não cadastrado
    Dado que informei ano e número de contrato que não existem para a minha secretaria
    Quando confirmo a tela
    Então vejo a mensagem "* Contrato nao cadastrado *"
    E o cursor fica no campo do contrato
    E nada é gravado

  Cenário: Contrato fechado
    Dado que o contrato informado está fechado
    Quando confirmo a tela
    Então vejo a mensagem "* Contrato fechado *"
    E o cursor fica no campo do contrato
    E nada é gravado

  Cenário: Situação informada diferente de cancelar e de bloquear
    Quando informo uma situação que não é cancelar nem bloquear
    Então vejo a mensagem "* Informe cancelar ou bloquear com C ou B *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: Matrícula do aluno não informada
    Quando deixo a matrícula do aluno em branco
    Então vejo a mensagem "* Informe a Matricula do Aluno *"
    E o cursor fica no campo da matrícula
    E nada é gravado

  Cenário: Aluno sem cartão no contrato e no órgão
    Dado que não existe cartão do aluno naquele contrato e naquele órgão
    Quando confirmo a tela
    Então vejo a mensagem "* Matricula nao cadastrada *"
    E o cursor fica no campo da matrícula
    E nada é gravado

  Cenário: Todos os cartões do aluno já estão baixados
    Dado que todos os cartões do aluno naquele contrato estão cancelados ou bloqueados
    Quando peço a baixa
    Então vejo a mensagem "* Cartao ja cancelado *" ou "* Cartao ja bloqueado *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: Motivo não informado
    Quando deixo o motivo em branco
    Então vejo a mensagem "* Informe a justificativa *"
    E o cursor fica no campo do motivo
    E nada é gravado

  Cenário: Motivo não cadastrado
    Quando informo um motivo que não existe na lista de justificativas
    Então vejo a mensagem "* Justificativa nao cadastrada *"
    E o cursor fica no campo do motivo
    E nada é gravado

  Cenário: A contagem do contrato acompanha a baixa
    Dado que existe a contagem do contrato para aquela coordenação e aquele órgão
    Quando confirmo o cancelamento de um cartão
    Então a quantidade de cancelados sobe um
    E a quantidade de entregues ou de não entregues desce um, conforme a situação que o cartão tinha
    E a quantidade total de cartões do contrato não muda

  Cenário: Sem registro de contagem, o cartão é baixado e a contagem não muda
    Dado que não existe registro de contagem para o contrato, a coordenação e o órgão
    Quando confirmo a baixa
    Então o cartão é baixado
    E a contagem do contrato não é corrigida
    E vejo a mensagem de sucesso mesmo assim

  Cenário: Toda baixa fica registrada na auditoria
    Quando confirmo um cancelamento ou um bloqueio
    Então fica um registro na auditoria, com a tela de origem, a operação de alteração, o cartão antes e depois, a matrícula do funcionário, a data e a hora da sessão e a matrícula do aluno como número do processo

  Cenário: A tela não está autorizada para a operação
    Dado que a tela não está cadastrada ou não aceita a operação
    Quando confirmo a tela
    Então vejo a mensagem "* Tela nao cadastrada *" ou "* Operacao nao disponivel *"
    E nada é gravado

  Cenário: Operação não autorizada para o perfil
    Dado que o meu perfil não tem a autorização para a operação
    Quando confirmo a tela
    Então o sistema recusa a operação
    E nada é gravado

  Cenário: Tela de retorno preenchida devolve o controle
    Dado que a tela veio com o código da tela de retorno preenchido
    Quando confirmo a tela
    Então o controle volta para aquela tela
    E esta tela não grava nada

  Cenário: Pedir a lista de motivos leva à tela de justificativas
    Dado que estou na E940T
    Quando peço a lista de motivos
    Então a tela de justificativas E935T é aberta em consulta
    E a E940T não grava nada

  Cenário: A tela não inclui nem exclui cartão
    Dado que estou na E940T
    Quando a operação termina
    Então nenhum cartão é incluído ou excluído
    E nenhum contrato, órgão, fornecedor ou motivo é alterado
```
