# US — N014T — Manter cabeçalho da nota fiscal

## Estória

Como **servidor de CRE**, quero **informar o cabeçalho da nota fiscal de um pedido —
número, modelo, fornecedor, chave de acesso, datas, pedido e órgão — e confirmá-lo**,
para que **a nota passe a existir para o sistema e os itens dela possam ser lançados,
e para que eu possa corrigi-la ou desfazê-la depois devolvendo ao pedido e ao
contrato o que ela consumia**.

É por esta tela que toda nota de compra entra: ela diz de que fornecedor, de que
pedido e de que datas a nota é, e só depois de passar por aqui os itens dela são
lançados. Sem essa conferência, uma nota poderia ser lançada contra um pedido já
aprovado e fechado, contra um órgão de outra secretaria, contra um fornecedor que não
é o do pedido ou com datas impossíveis — e o valor consumiria um contrato que não é o
dela. Como a nota consome o contrato no momento em que é lançada, é também por aqui
que ela sai quando o lançamento foi errado, e a exclusão devolve as quantidades ao
pedido.

## Contexto

Jornada S000M → N000M → N050M → N014T.

Ator: servidor de CRE — informa o cabeçalho da nota, confere o que a tela devolve
(a razão social do fornecedor, o nome do órgão, o nome do operador e os totais),
responde à pergunta de confirmação e segue para o lançamento dos itens.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada (`N000M` e `N050M`) são menus e não deixam nada
próprio: o que a N014T usa — a matrícula, o código de acesso, o privilégio, o tipo de
órgão (a secretaria) e a coordenadoria regional escolar (o grupo) — é o que a entrada
deixou na sessão. O órgão filho do servidor, que a entrada também carrega, **não**
limita esta tela.

Esta tela é alcançada por dois caminhos, e **o modo como ela abre depende de quem a
chamou** (RN-02). Ela encadeia na tela dos itens da nota e reabre a si mesma, e o que
ela entrega e o que recebe de volta estão na RN-23.

---

## Regras de negócio

### RN-01 — A tela informa o cabeçalho da nota; quem lança os itens é a tela seguinte

A tela reúne o cabeçalho da nota fiscal: o número da nota, o modelo, a chave de
acesso, a data de entrega da nota (dia, mês e ano), a data de emissão (dia, mês e
ano), a coordenadoria regional escolar, o número do pedido, o ano da entrega, o tipo
de contrato, o código do fornecedor, o órgão filho e o código do operador. Ela
mostra, para conferência, a descrição do modelo, a razão social do fornecedor, o nome
do órgão, o nome do operador, o total da nota, o total do IR e a marca de que a nota
está ligada a um pedido acumulado.

Confirmada a inclusão, a tela **não cria a nota**: ela entrega o cabeçalho à tela dos
itens, e é lá que a nota é gravada e os itens são lançados. Sem essa passagem, não há
nota nenhuma — a inclusão desta tela é o começo de um lançamento que só se completa
na tela seguinte.

### RN-02 — Como a tela abre depende de quem a chamou

A tela abre de duas formas, e quem decide é a tela de origem que ficou guardada na
área de trabalho da sessão:

- vinda do **menu**, ela abre em **inclusão** e em branco: só o grupo da sessão e o
  modelo já vêm preenchidos (RN-03), e o número da nota e a chave de acesso vêm
  zerados;
- vinda da **tela dos itens da nota**, ela abre em **inclusão** com o cabeçalho que
  aquela tela devolve — o modelo e a sua descrição, as duas datas, o fornecedor e a
  razão social, o operador e o nome dele, o grupo, o tipo de contrato, o pedido, o ano
  da entrega, o órgão filho e o nome dele — e com o número da nota e a chave de acesso
  zerados, para uma nota nova.

Qualquer outra origem cai no caso do menu. Isso não aparece em campo nenhum da tela —
é a regra mais fácil de se perder.

[?] O acervo não mostra por onde o servidor escolhe a **alteração** ou a **exclusão**
nesta tela: a abertura fixa a inclusão, e a única volta da tela dos itens também é em
inclusão. A tela tem o campo da operação, o cursor vai para ele quando a nota já
existe, e a tela dos itens recusa o que não for inclusão, alteração ou consulta — o
que sugere que o servidor digita a operação, mas o valor que ele digita não aparece
em lugar nenhum do acervo. Pergunta ao site.

### RN-03 — A tela abre em inclusão, com o meu grupo e o modelo 55 já preenchidos

Aberta pelo menu, a tela fixa a operação em **inclusão** e traz a coordenadoria
regional escolar da minha sessão já preenchida; se a minha sessão não carrega grupo, o
campo vem zerado. O modelo da nota vem preenchido com **55** quando o campo chega em
branco.

[?] O acervo não diz por que o modelo 55: a tela apenas o fixa quando o campo chega
em branco, sem nomear o que ele significa. Pergunta ao site.

### RN-04 — Nada anda sem a conferência da sessão, da tela e da permissão da operação

Antes de qualquer regra de negócio, toda página desta tela passa por três
conferências, nesta ordem: a **sessão** (o servidor tem de estar cadastrado e a
estação da sessão tem de ser a do cadastro dele), o **registro da tela** (a tela tem
de existir, e a tela excluída não passa) e a **permissão da operação** no cadastro de
acesso por tela, pela chave do código de acesso, do tipo de tela e da tela.

A operação declarada é o que decide qual permissão é conferida: inclusão pede a
permissão de incluir, alteração pede a de alterar, exclusão pede a de excluir.
Falhando qualquer uma delas, a transação para: a tela que não existe, ou que está
marcada como excluída, é recusada com * Tela nao disponivel *; a falta de permissão
para a tela, com * Acesso negado para esta matricula *; a falta de permissão para a
operação, com * Acesso negado para esta operacao *. A sessão que não bate com o
cadastro do servidor não dá mensagem: devolve a sessão ao menu e, sem matrícula, ao
`LOGON`.

[?] A **consulta** não tem permissão própria conferida: declarada a consulta, a
conferência da operação passa direto, e o cadastro de acesso por tela guarda um
indicador de consulta que ninguém lê. Se consultar esta tela deveria ser conferido
como incluir, alterar e excluir são, pergunta ao site.

### RN-05 — Os campos de código passam pela edição numérica

**Quatorze** campos da tela passam, um a um, pela edição numérica do sistema: os sete
do número e das duas datas (número da nota, dia, mês e ano da emissão da nota, dia,
mês e ano da emissão), os quatro do vínculo (coordenadoria regional escolar, número do
pedido, ano da entrega e tipo de contrato), o código do fornecedor, o órgão filho e o
código do operador. O que vem em branco vira zero, os zeros à esquerda caem e o que
não for número não passa, com o cursor de volta no campo.

São quatorze porque são quatorze os blocos de edição da tela, um por campo; **treze**
deles têm rótulo de negócio na tela e o do operador não tem — o rótulo dele é o
próprio nome interno do campo, e é por isso que ele não entra na lista dos treze.

### RN-06 — O número da nota é obrigatório, e o grupo tem de ser o da minha sessão

Zerado o número da nota, a recusa é * Informe o numero da nota fiscal *, com o cursor
no campo — tanto na inclusão quanto nas demais operações.

Sem grupo na sessão e com o campo em branco, a recusa é * Informe o grupo *, com o
cursor no campo. Com grupo na sessão e um grupo diferente informado, a recusa é
* Usuario sem acesso a outro grupo *. A conferência usa o grupo da sessão; é ele que
entra nas chaves de todas as leituras desta tela.

### RN-07 — A inclusão exige o pedido; a alteração, a exclusão e a consulta exigem o ano e o fornecedor

Na **inclusão**, sem o número do pedido a recusa é * Informe o numero do pedido *,
com o cursor no campo.

Na **alteração**, na **exclusão** e na **consulta**, são exigidos o ano de entrega da
nota e o código do fornecedor, além do número da nota: sem o ano, a recusa é
* Informe o ano de entrega da nota *; sem o fornecedor, * Informe o codigo do
fornecedor *. Nas duas o cursor volta ao campo que falta. Nessas três operações o
fornecedor é informado — é ele que identifica a nota junto com o número e o ano.

### RN-08 — O pedido tem de estar cadastrado e em situação que aceite nota

O pedido é procurado pelo tipo de órgão da sessão, pelo grupo e pelo número do
pedido. Não achando, a recusa é * Pedido nao cadastrado *, com o cursor no número do
pedido. Achando, a situação do pedido decide se a nota entra; em todas as recusas
abaixo o cursor volta ao número do pedido e nada é gravado:

- pedido marcado como excluído → * Pedido excluido *;
- pedido pendente de distribuição → * Pedido pendente de distribuicao *;
- pedido pendente de aprovação → * Pedido pendente de aprovacao *;
- pedido auxiliar de um pedido acumulado já calculado → * Pedido auxiliar do pedido
  acumulado calculado *;
- pedido aprovado e fechado → * Pedido aprovado - fechado *.

### RN-09 — O órgão filho do pedido tem de estar cadastrado, completo, na minha secretaria e no meu grupo

O órgão filho é tomado do pedido (não é digitado). A tela procura o órgão pelo código
informado e despreza os registros marcados como excluídos; não achando nenhum, a
recusa é * Orgao nao cadastrado *. Achando, e faltando no cadastro o bairro, o órgão
pai, o nome, o endereço, o número de matriculados ou o número de comensais, a recusa
é * Orgao cadastrado com dados incompletos *.

Em seguida o órgão tem de ser da secretaria da sessão — senão * Orgao nao pertence a
esta secretaria * — e do grupo informado — senão * Orgao nao pertence a este grupo *.
Todas as recusas devolvem o cursor ao número do pedido.

### RN-10 — O tipo de contrato é o do pedido; contrato de operador logístico não entra por aqui

O tipo de contrato não é digitado: a tela o toma do pedido. Pedido sem tipo de
contrato nenhum é recusado com * Pedido sem tipo de contrato *; tipo de contrato que
não existe para a secretaria da sessão, com * Tipo de contrato nao cadastrado *.

Achado o tipo de contrato, o contrato que exige permissão de operador logístico é
recusado com * Contrato de Oper.Logistico. Use E830T * — a nota desse contrato entra
por outra tela. Nas três recusas o cursor volta ao número do pedido.

### RN-11 — O modelo da nota fiscal tem de estar cadastrado

O modelo informado é procurado no cadastro dos modelos de nota fiscal. Não achando, a
recusa é * Modelo de nota fiscal nao cadastrado *, com o cursor no campo do modelo —
na inclusão e na alteração. Na alteração, apagar o modelo é recusado antes disso, com
* Informe o modelo da nota fiscal *.

### RN-12 — Na inclusão, o fornecedor é o do pedido

Na inclusão o código do fornecedor não identifica a nota: depois de o pedido ser
achado, a tela **substitui** o fornecedor informado pelo fornecedor do pedido, e é
esse que passa a valer para todas as conferências seguintes. Em seguida procura o
fornecedor no cadastro: não achando, ou achando-o excluído, a recusa é
* Fornecedor nao cadastrado *, com o cursor no campo do fornecedor. Achando, a tela
exibe a razão social dele.

[?] O fornecedor digitado na inclusão é usado antes disso numa leitura da nota fiscal
e depois descartado. O acervo não diz se o campo é para conferência ou se a digitação
é simplesmente ignorada. Pergunta ao site.

### RN-13 — As datas: a entrega não pode ser futura nem anterior ao pedido, e a emissão não pode ser anterior ao pedido

São duas datas, cada uma informada em dia, mês e ano: a **data de entrega da nota** e
a **data de emissão**. As recusas, na ordem em que a tela as faz:

- data de entrega que não forma uma data válida (inclusive ano fora de 1994 a 2099) →
  * Data de entrega invalida *, com o cursor no dia da entrega;
- data de entrega posterior à data do sistema → * Data de entrega > que a data atual *,
  com o cursor no dia da entrega;
- data de emissão que não forma uma data válida (mesmo limite de ano) →
  * Data de emissao invalida *, com o cursor no dia da emissão;
- data de emissão posterior à data de entrega → * Data de emissao > data da entrega *,
  com o cursor no dia da emissão;
- data de entrega anterior à data de início do pedido → * Data de entrega menor que
  data do pedido *, com o cursor no número do pedido;
- data de emissão anterior ao início do pedido menos **vinte dias** →
  * Data da emissao invalida *, com o cursor no número do pedido (mensagem com texto
  diferente da outra recusa de emissão, e cursor em outro campo).

[?] O ajuste de vinte dias sobre a data de início do pedido é feito por uma rotina do
ambiente que não está no acervo; o que se lê é a rotina ser chamada com o sinal de
subtrair e o número 20, como em outras telas do acervo. Se o que se pretende é uma
tolerância de vinte dias, ou outro intervalo, pergunta ao site.

[?] Os dois trios de data têm rótulos que não combinam com o uso: o trio rotulado
* DIA/MES/ANO EMISSAO N.F. * é o que as mensagens tratam como **data de entrega da
nota** e o que é comparado com o início do pedido e com a data de hoje; e o trio
rotulado * DIA/MES/ANO EMISSAO * é o que as mensagens tratam como **data de emissão**.
A tela mostra dois rótulos de emissão para datas de papéis diferentes. Pergunta ao
site.

### RN-14 — A chave de acesso só é exigida de fornecedor pessoa jurídica

A chave de acesso é conferida apenas quando o fornecedor é pessoa jurídica; quando é
pessoa física, a tela **zera** a chave informada, e ela não vai adiante.

Para pessoa jurídica a chave tem de ter o número da nota informado e os oito primeiros
dígitos do Cadastro Nacional da Pessoa Jurídica do fornecedor do pedido, e o dígito
verificador dela tem de fechar na conferência de módulo 11 do próprio sistema. Não
fechando qualquer uma das três coisas, a recusa é * Chave de acesso invalida *, com o
cursor na chave.

[?] A conferência olha o número da nota, os oito primeiros dígitos do Cadastro e o
dígito verificador: as demais posições da chave (a unidade da federação, o mês e o ano
de emissão, o modelo, a série, o tipo de emissão e o número do documento) não são
conferidas. Se deveriam ser, pergunta ao site.

### RN-15 — A nota que já existe não entra pela inclusão

Ainda na inclusão, depois de o fornecedor passar a ser o do pedido, a tela procura a
nota pelo tipo de órgão da sessão, pelo fornecedor do pedido, pelo número da nota e
pelo ano de entrega. Achando, a recusa é * Nota ja cadastrada. Use ALT. *, com o
cursor no campo da operação — a nota existe e o caminho é a alteração. Antes disso,
achando a nota e sendo ela de outro grupo, a recusa é * Usuario sem acesso ao grupo
desta nota *, com o cursor no número da nota.

### RN-16 — A nota que já está em um processo é recusada

A tela procura a nota no cadastro das notas fiscais por processo, pelo tipo de órgão
da sessão, pelo fornecedor, pelo número da nota e pelo ano da entrega, com mês e dia
de entrega zerados. Achando, a recusa vem com o número do processo que já tem a nota e
o cursor volta ao número da nota: na **inclusão** é * <- Nota fiscal ja cadastrada
neste processo *; na **alteração** e na **consulta** é * <- Nota fiscal cadastrada
neste processo *, sem o "já". A **exclusão** não faz essa conferência — a nota que já
está em um processo pode ser excluída por aqui.

### RN-17 — A confirmação: a tela pergunta, e só segue com "S" e sem mudanças

Passando por todas as conferências, a tela **não grava**: ela mostra a pergunta de
confirmação e reabre a si mesma com ela na tela.

- na inclusão — * Confirma inclusao da nota <S/N> ? *;
- na alteração — * Confirma alteracao da nota fiscal <S/N> ? *;
- na exclusão — * Confirma exclusao da nota fiscal <S/N> ? *.

A resposta tem de ser "S". Qualquer outra resposta, inclusive em branco, **cancela a
confirmação sem mensagem nenhuma**: a tela esquece a pergunta e volta a tratar o que
estiver na tela como um pedido novo. E se, depois de a pergunta aparecer, algum dos
campos que a pergunta congelou for mudado, a confirmação também é cancelada, sem
mensagem, mesmo que a resposta seja "S".

Confirmada a resposta e pendente a confirmação, a tela ainda exige o grupo e o número
do pedido: sem um dos dois, ela não grava e volta ao começo, **sem mensagem nenhuma**.

### RN-18 — A alteração troca o modelo, a chave de acesso e a data de emissão

A alteração só passa com a nota cadastrada (senão * Nota fiscal nao cadastrada *, com
o cursor no número da nota) e com a nota no meu grupo (senão * Usuario sem acesso ao
grupo desta nota *). Confirmada, ela muda três coisas na nota, uma por vez e cada uma
com o seu registro de auditoria: o **modelo**, quando mudou; a **chave de acesso**,
quando mudou; e a **data de emissão**, quando mudou. Depois de mudar, a tela entrega a
nota à tela dos itens, para o lançamento continuar lá.

### RN-19 — A exclusão devolve ao pedido e ao contrato o que a nota consumia

Confirmada, a exclusão apaga os itens da nota, devolve ao contrato as quantidades e os
valores que a nota comprometia, devolve ao pedido a quantidade que a nota já tinha
recebido — reabrindo o pedido —, desfaz a ligação da nota com o pedido acumulado,
apaga os registros de recebimento da nota e, por fim, apaga a nota.

Antes de perguntar, a tela recusa a exclusão em quatro casos, todos com o cursor no
número da nota:

- nota que não existe → * Nota fiscal nao cadastrada *;
- nota cujo pedido está no acumulado e que tem algum pedido dela em órgão diferente do
  órgão da nota → * Exclua pedidos desta nota do acumulado *;
- nota que já tem quantidade recebida → * Ja existe quantidade recebida *;
- nota com nota de devolução cadastrada → * <- Nota de devolucao cadastrada *.

[?] A recusa * Exclua pedidos desta nota do acumulado * manda o servidor desligar do
acumulado os pedidos da nota — e é o próprio caminho da exclusão que desliga esses
pedidos do acumulado e os reabre. Ou a recusa vale só para o caso do pedido de outro
órgão, ou o caminho que a dispara ficou inalcançável. Pergunta ao site.

### RN-20 — A consulta não confirma nada e entrega os itens à tela seguinte

Em consulta a tela não pergunta nada e não grava nada da operação: ela carrega o que
está cadastrado — número, modelo, descrição do modelo, datas, fornecedor e razão
social, operador e nome, grupo, tipo de contrato, órgão filho e nome, chave de acesso,
total da nota e total do IR — e passa direto para a tela dos itens, para o servidor ver
os itens daquela nota. O que a tela grava antes disso, em qualquer operação, é o que
está na RN-21.

### RN-21 — A tela acerta o total da nota e apaga a nota que ficou sem itens

Antes de qualquer conferência de operação, e em qualquer operação, a tela soma os
itens da nota informada e compara com o total gravado na nota:

- soma **zero** e a nota existe → a tela **apaga a nota**, sem avisar;
- soma diferente do total gravado → a tela **regrava o total** da nota com a soma dos
  itens.

[?] Isso roda antes da pergunta de confirmação e em toda operação, inclusive na
consulta, e nada é dito ao servidor: uma consulta sobre uma nota que perdeu os itens
apaga a nota. Se era esse o desenho, ou se a limpeza deveria estar presa à operação de
exclusão, pergunta ao site.

### RN-22 — A nota de outro tipo de contrato desliga o pedido do acumulado

Sendo o pedido um pedido que está ligado a um acumulado, a tela percorre os itens
daquele pedido. Os itens ligados ao acumulado cujo tipo de contrato não é o do
acumulado são **desligados do acumulado**, e os pedidos deles são reabertos — perdem
a marca de acumulado, ficam sem operador e voltam à situação de disponível. Isso
acontece na primeira passagem, antes de a pergunta de confirmação aparecer.

[?] A comparação é feita contra o tipo de contrato do próprio acumulado, e não contra
o tipo de contrato da nota que está sendo incluída — que a tela só lê mais adiante, do
próprio pedido. Se a intenção era comparar com o da nota, a conferência está no lugar
errado. E essas alterações no pedido e nos itens dele são as únicas gravações desta
tela que **não** deixam registro na auditoria. Pergunta ao site.

### RN-23 — O que a tela entrega à tela dos itens, e o que recebe de volta

A tela entrega à tela dos itens, sem passar por menu, a nota e a operação: o número da
nota, o modelo e a sua descrição, o fornecedor e a razão social, o grupo, o tipo de
contrato, o pedido, o ano da entrega, o órgão filho e o nome dele, o operador e o nome
dele, a chave de acesso, as duas datas, o total da nota, o total do IR e a marca de
pedido acumulado — junto com a operação que estava declarada. É essa entrega que faz a
tela seguinte abrir no mesmo modo e sobre a mesma nota: em inclusão, para lançar os
itens da nota nova; em alteração, para continuar o lançamento; em consulta, para
mostrar os itens.

Na volta, é a tela dos itens que devolve o cabeçalho: em inclusão, com o número da nota
zerado, para uma nota nova.

### RN-24 — O que a tela grava, e o que fica registrado

A tela enxerga **dezesseis** cadastros — o registro das telas, o das notas fiscais, o
das notas fiscais no processo, o dos itens da nota, o dos modelos de nota, o dos
pedidos acumulados, o das notas de devolução, o dos pedidos, o dos itens do pedido, o
dos recebimentos da nota, o dos fornecedores, o dos operadores, o dos órgãos filhos, o
dos tipos de contrato, o dos contratos e a auditoria — além do cadastro do servidor e
do cadastro de acesso por tela, que as conferências de abertura leem. Ela **escreve em
oito**: grava e apaga a nota, apaga os itens da nota, apaga a ligação com o acumulado,
apaga o recebimento, grava o pedido, grava o item do pedido, grava o contrato e cria o
registro de auditoria. Nenhum cadastro de negócio ganha registro novo: a única criação
é o registro de auditoria.

Cada gravação que conclui a operação — a alteração, a exclusão e cada passo da
devolução ao contrato e ao pedido — é precedida do registro de auditoria, com o
cadastro auditado, a operação, a matrícula, a estação, a data e a hora, e o conteúdo
do registro antes e depois. As gravações que a tela faz **antes** da confirmação — o
acerto do total da nota, a limpeza da nota sem itens e a liberação do pedido acumulado
— não passam pela auditoria (isto é a dúvida da RN-22).

Qualquer falha de banco na leitura ou na gravação interrompe a transação e vira o erro
do sistema, e o que já estava gravado não é desfeito.

---

## Cenários BDD

```gherkin
Funcionalidade: Cabeçalho da nota fiscal de um pedido

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o código de acesso, o privilégio, o tipo de órgão e a coordenadoria regional escolar
    E tenho acesso à tela N014T

  Cenário: RN-01 e RN-23 — incluir a nota e entregá-la ao lançamento dos itens
    Dado que abro a tela N014T pelo menu
    E informo o número da nota, o modelo, a chave de acesso, as duas datas, o pedido e o órgão do pedido está cadastrado
    Quando confirmo e respondo "S" à pergunta de confirmação
    Então a tela entrega a nota e a operação de inclusão à tela dos itens
    E a nota só é gravada quando os itens dela forem lançados lá

  Cenário: RN-02 — abrir pelo menu abre em inclusão
    Dado que venho do menu
    Quando abro a tela N014T
    Então a operação já vem fixada em inclusão
    E o número da nota, a chave de acesso e a data de emissão vêm zerados

  Cenário: RN-02 — a volta da tela dos itens reabre em inclusão, para uma nota nova
    Dado que estou na tela dos itens da nota e peço uma nota nova
    Quando volto para a tela N014T
    Então ela reabre em inclusão
    E o número da nota vem zerado
    E os demais dados da nota continuam preenchidos

  Cenário: RN-03 — a tela abre com a minha coordenadoria e o modelo 55
    Dado que a minha sessão carrega uma coordenadoria regional escolar
    Quando abro a tela N014T
    Então o campo do grupo já vem preenchido com a coordenadoria da minha sessão
    E o modelo da nota já vem preenchido com 55

  Cenário: RN-04 — operação que a tela não conhece
    Dado que estou na tela N014T
    Quando peço uma operação que não é inclusão, alteração, exclusão nem consulta
    Então vejo "* Operacao nao disponivel *"
    E nada é gravado

  Cenário: RN-04 — sem permissão para a operação pedida
    Dado que o meu código de acesso não tem a permissão da operação que pedi nesta tela
    Quando confirmo
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-04 — sem permissão para a tela
    Dado que o meu código de acesso não tem esta tela
    Quando abro a tela N014T
    Então vejo "* Acesso negado para esta matricula *"
    E nada é gravado

  Cenário: RN-04 — tela não cadastrada, ou excluída
    Dado que a tela N014T não existe no registro das telas, ou está marcada como excluída
    Quando abro a tela
    Então vejo "* Tela nao disponivel *"
    E nada é gravado

  Cenário: RN-04 — sessão que não bate com o cadastro do servidor
    Dado que a estação da minha sessão não é a do meu cadastro
    Quando confirmo
    Então a sessão é devolvida ao menu principal
    E nada é gravado

  Cenário: RN-05 — campo de código que não é número
    Dado que estou na tela N014T
    Quando informo em um dos códigos algo que não é número
    Então o código não passa pela edição
    E o cursor volta para o campo

  Cenário: RN-06 — número da nota em branco
    Dado que estou na tela N014T
    Quando confirmo sem o número da nota
    Então vejo "* Informe o numero da nota fiscal *"
    E o cursor fica no número da nota
    E nada é gravado

  Cenário: RN-06 — sessão sem grupo e campo em branco
    Dado que a minha sessão não carrega coordenadoria regional escolar
    Quando confirmo sem informar o grupo
    Então vejo "* Informe o grupo *"
    E o cursor fica no grupo
    E nada é gravado

  Cenário: RN-06 — grupo de outra coordenadoria
    Dado que a minha sessão carrega uma coordenadoria regional escolar
    Quando informo outra coordenadoria
    Então vejo "* Usuario sem acesso a outro grupo *"
    E nada é gravado

  Cenário: RN-07 — inclusão sem o número do pedido
    Dado que estou na tela N014T em inclusão
    Quando confirmo sem o número do pedido
    Então vejo "* Informe o numero do pedido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: RN-07 — alteração sem o ano de entrega
    Dado que estou na tela N014T em alteração
    Quando confirmo sem o ano de entrega da nota
    Então vejo "* Informe o ano de entrega da nota *"
    E o cursor fica no ano de entrega
    E nada é gravado

  Cenário: RN-07 — alteração sem o fornecedor
    Dado que estou na tela N014T em alteração
    Quando confirmo sem o código do fornecedor
    Então vejo "* Informe o codigo do fornecedor *"
    E o cursor fica no fornecedor
    E nada é gravado

  Cenário: RN-08 — pedido não cadastrado
    Dado que estou na tela N014T em inclusão
    Quando confirmo com um pedido que não existe para a minha secretaria e o meu grupo
    Então vejo "* Pedido nao cadastrado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: RN-08 — pedido excluído
    Dado que o pedido está marcado como excluído
    Quando confirmo
    Então vejo "* Pedido excluido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: RN-08 — pedido pendente de distribuição
    Dado que o pedido está pendente de distribuição
    Quando confirmo
    Então vejo "* Pedido pendente de distribuicao *"
    E nada é gravado

  Cenário: RN-08 — pedido pendente de aprovação
    Dado que o pedido está pendente de aprovação
    Quando confirmo
    Então vejo "* Pedido pendente de aprovacao *"
    E nada é gravado

  Cenário: RN-08 — pedido auxiliar de um acumulado já calculado
    Dado que o pedido é auxiliar de um pedido acumulado já calculado
    Quando confirmo
    Então vejo "* Pedido auxiliar do pedido acumulado calculado *"
    E nada é gravado

  Cenário: RN-08 — pedido aprovado e fechado
    Dado que o pedido está aprovado e fechado
    Quando confirmo
    Então vejo "* Pedido aprovado - fechado *"
    E nada é gravado

  Cenário: RN-09 — órgão do pedido não cadastrado
    Dado que o órgão filho do pedido não existe no cadastro, ou está excluído
    Quando confirmo
    Então vejo "* Orgao nao cadastrado *"
    E nada é gravado

  Cenário: RN-09 — órgão do pedido com dados incompletos
    Dado que o órgão filho do pedido está sem bairro, órgão pai, nome, endereço, matriculados ou comensais
    Quando confirmo
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E nada é gravado

  Cenário: RN-09 — órgão do pedido de outra secretaria
    Dado que o órgão filho do pedido é de outro tipo de órgão
    Quando confirmo
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E nada é gravado

  Cenário: RN-09 — órgão do pedido de outro grupo
    Dado que o órgão filho do pedido é de outra coordenadoria regional escolar
    Quando confirmo
    Então vejo "* Orgao nao pertence a este grupo *"
    E nada é gravado

  Cenário: RN-10 — pedido sem tipo de contrato
    Dado que o pedido não tem tipo de contrato
    Quando confirmo
    Então vejo "* Pedido sem tipo de contrato *"
    E nada é gravado

  Cenário: RN-10 — tipo de contrato do pedido não cadastrado
    Dado que o tipo de contrato do pedido não existe para a minha secretaria
    Quando confirmo
    Então vejo "* Tipo de contrato nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — contrato de operador logístico
    Dado que o tipo de contrato do pedido é de operador logístico
    Quando confirmo
    Então vejo "* Contrato de Oper.Logistico. Use E830T *"
    E nada é gravado

  Cenário: RN-11 — modelo da nota não cadastrado
    Dado que estou na tela N014T
    Quando informo um modelo que não existe no cadastro dos modelos
    Então vejo "* Modelo de nota fiscal nao cadastrado *"
    E o cursor fica no modelo
    E nada é gravado

  Cenário: RN-11 — modelo apagado na alteração
    Dado que estou na tela N014T em alteração
    Quando apago o modelo da nota
    Então vejo "* Informe o modelo da nota fiscal *"
    E o cursor fica no modelo
    E nada é gravado

  Cenário: RN-12 — o fornecedor que vale na inclusão é o do pedido
    Dado que estou na tela N014T em inclusão e informei um fornecedor
    Quando o pedido é achado
    Então o fornecedor do pedido substitui o que eu informei
    E é ele que a tela confere e entrega à tela dos itens

  Cenário: RN-12 — fornecedor do pedido não cadastrado
    Dado que o fornecedor do pedido não existe no cadastro, ou está excluído
    Quando confirmo
    Então vejo "* Fornecedor nao cadastrado *"
    E o cursor fica no fornecedor
    E nada é gravado

  Cenário: RN-13 — data de entrega inválida
    Dado que estou na tela N014T
    Quando informo uma data de entrega que não forma uma data válida
    Então vejo "* Data de entrega invalida *"
    E o cursor fica no dia da entrega
    E nada é gravado

  Cenário: RN-13 — data de entrega no futuro
    Dado que estou na tela N014T
    Quando informo uma data de entrega posterior a hoje
    Então vejo "* Data de entrega > que a data atual *"
    E nada é gravado

  Cenário: RN-13 — data de entrega anterior ao pedido
    Dado que estou na tela N014T em inclusão
    Quando informo uma data de entrega anterior à data de início do pedido
    Então vejo "* Data de entrega menor que data do pedido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: RN-13 — data de emissão inválida
    Dado que estou na tela N014T
    Quando informo uma data de emissão que não forma uma data válida
    Então vejo "* Data de emissao invalida *"
    E o cursor fica no dia da emissão
    E nada é gravado

  Cenário: RN-13 — data de emissão posterior à entrega
    Dado que estou na tela N014T
    Quando informo uma data de emissão posterior à data de entrega
    Então vejo "* Data de emissao > data da entrega *"
    E nada é gravado

  Cenário: RN-13 — data de emissão muito anterior ao início do pedido
    Dado que estou na tela N014T em inclusão
    Quando informo uma data de emissão anterior ao início do pedido menos vinte dias
    Então vejo "* Data da emissao invalida *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: RN-14 — chave de acesso inválida
    Dado que o fornecedor do pedido é pessoa jurídica
    Quando informo uma chave de acesso que não fecha com o fornecedor, com o número da nota ou no dígito verificador
    Então vejo "* Chave de acesso invalida *"
    E o cursor fica na chave
    E nada é gravado

  Cenário: RN-14 — fornecedor pessoa física não tem chave de acesso
    Dado que o fornecedor do pedido é pessoa física
    Quando confirmo com uma chave de acesso informada
    Então a tela zera a chave
    E a chave não é conferida nem levada adiante

  Cenário: RN-15 — nota já cadastrada
    Dado que estou na tela N014T em inclusão
    Quando confirmo com o número e o ano de uma nota que já está cadastrada para aquele fornecedor
    Então vejo "* Nota ja cadastrada. Use ALT. *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: RN-15 — nota já cadastrada de outro grupo
    Dado que a nota informada está cadastrada em outra coordenadoria regional escolar
    Quando confirmo
    Então vejo "* Usuario sem acesso ao grupo desta nota *"
    E o cursor fica no número da nota
    E nada é gravado

  Cenário: RN-16 — nota já lançada neste processo
    Dado que a nota já está ligada a um processo
    Quando confirmo a inclusão
    Então vejo "* <- Nota fiscal ja cadastrada neste processo *", com o número do processo
    E o cursor fica no número da nota
    E nada é gravado

  Cenário: RN-16 — em alteração ou consulta a mesma recusa muda de texto
    Dado que estou na tela N014T em alteração ou em consulta sobre uma nota já ligada a um processo
    Quando confirmo
    Então vejo "* <- Nota fiscal cadastrada neste processo *", com o número do processo

  Cenário: RN-16 — a exclusão não confere se a nota está em um processo
    Dado que estou na tela N014T em exclusão sobre uma nota já ligada a um processo
    Quando confirmo e respondo "S"
    Então a exclusão segue, sem essa recusa

  Cenário: RN-17 — a pergunta de confirmação não grava nada
    Dado que estou na tela N014T em inclusão, com tudo conferido
    Quando confirmo pela primeira vez
    Então vejo "* Confirma inclusao da nota <S/N> ? *"
    E a tela reabre com a pergunta
    E a nota ainda não foi gravada

  Cenário: RN-17 — resposta diferente de sim
    Dado que a pergunta de confirmação está na tela
    Quando respondo qualquer coisa diferente de "S"
    Então a confirmação é cancelada
    E nenhuma mensagem aparece
    E nada é gravado

  Cenário: RN-17 — mudar um campo depois da pergunta cancela a confirmação
    Dado que a pergunta de confirmação está na tela
    Quando mudo um dos campos da nota e respondo "S"
    Então a confirmação é cancelada
    E a tela trata o que está na tela como um pedido novo
    E nada é gravado

  Cenário: RN-17 — confirmar sem grupo ou sem pedido
    Dado que a pergunta de confirmação está na tela e respondi "S"
    E o grupo ou o número do pedido está zerado
    Quando a tela retoma
    Então nada é gravado
    E nenhuma mensagem aparece

  Cenário: RN-18 — alterar o modelo, a chave e a data de emissão
    Dado que estou na tela N014T em alteração sobre uma nota cadastrada no meu grupo
    E mudo o modelo, a chave de acesso e a data de emissão
    Quando confirmo e respondo "S"
    Então a nota passa a ter o modelo, a chave e a data de emissão novos
    E cada uma das três mudanças fica registrada na auditoria
    E a tela entrega a nota à tela dos itens

  Cenário: RN-18 — nota não cadastrada
    Dado que estou na tela N014T em alteração
    Quando confirmo com o número de uma nota que não existe
    Então vejo "* Nota fiscal nao cadastrada *"
    E o cursor fica no número da nota
    E nada é gravado

  Cenário: RN-19 — excluir a nota devolve as quantidades ao pedido e ao contrato
    Dado que estou na tela N014T em exclusão sobre uma nota sem recebimento e sem nota de devolução
    Quando confirmo e respondo "S"
    Então os itens da nota são apagados
    E o contrato recebe de volta as quantidades e os valores que a nota comprometia
    E o pedido recebe de volta a quantidade recebida e volta à situação de disponível
    E a ligação da nota com o pedido acumulado é desfeita
    E a nota é apagada

  Cenário: RN-19 — exclusão recusada por quantidade recebida
    Dado que a nota já tem quantidade recebida
    Quando peço a exclusão
    Então vejo "* Ja existe quantidade recebida *"
    E o cursor fica no número da nota
    E nada é apagado

  Cenário: RN-19 — exclusão recusada por nota de devolução
    Dado que a nota tem uma nota de devolução cadastrada
    Quando peço a exclusão
    Então vejo "* <- Nota de devolucao cadastrada *"
    E nada é apagado

  Cenário: RN-19 — exclusão recusada por pedido da nota em outro órgão
    Dado que o pedido da nota está no acumulado e tem pedido dela em órgão diferente do órgão da nota
    Quando peço a exclusão
    Então vejo "* Exclua pedidos desta nota do acumulado *"
    E nada é apagado

  Cenário: RN-20 — a consulta não grava nada da operação
    Dado que estou na tela N014T em consulta
    Quando informo a nota e confirmo
    Então a tela mostra o que está cadastrado — modelo, datas, fornecedor, grupo, tipo de contrato, órgão, chave, total da nota e total do IR
    E passa os itens daquela nota para a tela dos itens
    E nenhuma gravação da própria consulta é feita

  Cenário: RN-21 — nota que ficou sem itens é apagada
    Dado que a nota informada existe e os itens dela somam zero
    Quando confirmo
    Então a nota é apagada, sem aviso

  Cenário: RN-21 — total da nota reajustado pela soma dos itens
    Dado que a nota informada existe e a soma dos itens dela é diferente do total gravado
    Quando confirmo
    Então o total da nota é regravado com a soma dos itens

  Cenário: RN-22 — incluir a nota desliga o pedido do acumulado
    Dado que o pedido está ligado a um acumulado
    E há nele item ligado ao acumulado com tipo de contrato diferente do do acumulado
    Quando confirmo
    Então esse item é desligado do acumulado
    E o pedido dele volta à situação de disponível, sem operador

  Cenário: RN-24 — nenhuma gravação confirmada fica sem auditoria
    Dado que confirmei uma alteração ou uma exclusão
    Quando a gravação é feita
    Então cada registro alterado é precedido de um registro de auditoria
    E o registro de auditoria guarda o cadastro, a operação, a matrícula, a estação, a data, a hora e o conteúdo antes e depois

  Cenário: RN-24 — falha do banco
    Dado que a leitura ou a gravação de um cadastro falha no banco
    Quando confirmo
    Então a transação é interrompida com o erro do sistema
    E o que já estava gravado não é desfeito
```
