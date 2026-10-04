# US — E550T — Manter semana de preparo da unidade

## Estória

Como **servidor da CRE que responde pelo preparo das refeições das unidades da sua
coordenadoria**, quero **abrir o cálculo de uma semana de uma unidade — informando a
coordenação regional escolar e a data de início do preparo —, e também consultá-lo,
alterá-lo e excluí-lo**, para que **a semana fique identificada, com os seus sete dias e
as letras de cardápio, e possa receber, na tela seguinte, os segmentos, as refeições e as
quantidades**.

O cálculo não nasce completo: primeiro é preciso dizer de qual unidade, de qual
coordenação e de qual semana se trata. É esta tela que faz isso — confere a unidade
contra o cadastro, contra a secretaria e contra o alcance do servidor, e busca no
cadastro a letra de cardápio de cada dia. Sem essa abertura a tela seguinte não tem
sobre o que gravar as refeições; e é aqui também que a semana fica reservada, porque
duas semanas da mesma unidade não podem se tocar.

## Contexto

Jornada S000M → E000M → E550M → E550T.
Ator: servidor de CRE — abre, consulta, altera e exclui o cálculo de uma semana de
preparo de uma unidade da sua coordenadoria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As duas telas do caminho são menus: encaminham, não gravam nada e **não registram a
origem** desta tela. O que esta tela usa do que veio antes é a **secretaria (o tipo de
órgão), o órgão filho, a coordenação regional escolar, a matrícula, o código de acesso e
o privilégio** da sessão; isso é regra da entrada e está no anexo de evidências, em
**Regras que se revelaram da entrada**. O **órgão filho da sessão** é o que limita qual
unidade o servidor pode abrir (RN-03).

Esta tela **muda conforme quem a chama** numa situação, e não é a do menu: quando ela
reabre trazendo a marca deixada pela **tela de detalhe** — o que acontece quando o
servidor volta dela —, ela abre forçada em **consulta**, com o registro carregado, e
avisa o que a tela de detalhe encontrou (RN-20). É ela também que decide o modo da tela
seguinte: entrega o registro e a operação à `E551T`, que abre no modo que esta deixou
(RN-19).

## Regras de negócio

### RN-01 — A tela abre o cálculo de uma semana de uma unidade

A tela serve à **requisição de cálculo** de uma unidade (o órgão filho SDI): o servidor
informa a unidade, a coordenação regional escolar e a **data de início** do preparo, e o
sistema identifica a semana — sete dias, cada um com a sua letra de cardápio — para a
tela seguinte detalhar. Esta tela é a porta de entrada do cálculo: ela **não cria nem
altera** a requisição (quem a grava é a tela seguinte) e só conhece quatro operações —
inclusão, alteração, exclusão e consulta. A exclusão apaga (RN-17); a consulta só lê
(RN-18).

### RN-02 — A operação vem como inclusão, e a permissão é conferida antes

Ao abrir sem nenhuma operação deixada pela sessão, a operação é a **inclusão**.
Informada uma operação que não seja uma das quatro, a recusa é
**\* Operacao nao disponivel \***, com o cursor de volta ao campo da operação e nada mais
conferido.

Antes das conferências de dados, a tela entrega a operação informada à rota e à
conferência de autorização por tela e operação: sem a permissão daquela operação, a
operação não segue e nada é gravado. A **consulta** é a exceção: a conferência de
autorização a libera sem olhar marca nenhuma — a marca de consulta existe no cadastro,
mas não é lida nesse caminho.

### RN-03 — A unidade da sessão limita o que o servidor abre

Quando o servidor tem uma **unidade (órgão filho) na sessão**, ela vem preenchida na
abertura e é a única que ele pode abrir: informando outra, a recusa é
**\* Usuario sem acesso a outro orgao \***, com o número da unidade dele na mensagem e o
cursor no campo da unidade.

Quem **não** tem unidade na sessão abre para a unidade que informar — e, nesse caso, a
tela já deixa o cursor no campo da unidade, porque é por ele que o servidor começa.

### RN-04 — A coordenação da sessão limita o que o servidor abre

Quando o servidor tem **coordenação regional escolar na sessão**, ela vem preenchida e a
unidade aberta tem de ser de uma unidade dessa mesma coordenação: se a unidade pertence a
outra, a recusa é **<- Usuario sem acesso ao grupo deste orgao \***, com o número da
coordenação da unidade na mensagem e o cursor no campo da unidade. Quem não tem
coordenação na sessão não passa por essa restrição.

### RN-05 — A unidade é obrigatória e tem de estar cadastrada

A unidade tem de constar do cadastro das unidades. Na **inclusão**, a unidade em branco é
recusada com **\* Informe o orgao \***; nas demais operações a leitura do cadastro vem
primeiro, e a unidade em branco cai na recusa de unidade inexistente. Não achada no
cadastro, a recusa é **\* Orgao nao cadastrado \***. Nas duas, o cursor volta ao campo da
unidade e nada é gravado.

### RN-06 — A unidade tem de ser da secretaria do servidor

A unidade informada tem de pertencer à **secretaria da sessão**. De outra secretaria, a
recusa é **\* Orgao nao pertence a esta secretaria \***, com o cursor no campo da unidade
e nada gravado.

Esta conferência só roda na **inclusão**: a alteração, a exclusão e a consulta leem a
unidade do cadastro e seguem sem conferir a secretaria dela.

### RN-07 — A unidade tem de estar ativa, sem pedido acumulado e com os dados completos

Ainda na **inclusão**, a unidade passa por três conferências, na ordem, cada uma com a
sua recusa e o cursor no campo da unidade:

- marcada como **inativa** — **\* Orgao cadastrado como inativo \***;
- marcada para **pedido acumulado** — **\* Orgao cadastrado para pedido acumulado \***;
- **dados incompletos** — sem bairro, sem órgão pai, sem nome, sem endereço, sem
  matriculados ou sem comensais (são os **seis** dados exigidos) —
  **\* Orgao cadastrado com dados incompletos \***.

Como em RN-06, estas três só barram a inclusão; a alteração, a exclusão e a consulta não
passam por elas.

### RN-08 — A unidade tem de ter segmento cadastrado

Para abrir uma semana nova, a unidade precisa ter pelo menos um **segmento de atendimento**
cadastrado para a secretaria. Sem nenhum, a recusa é
**\* Orgao sem segmentos cadastrados \***, com o cursor no campo da unidade. É a mesma
mensagem que a tela mostra quando reabre vinda da tela de detalhe (RN-20).

### RN-09 — Alterar, excluir e consultar exigem que a requisição exista

A requisição é procurada pela unidade, pela coordenação da unidade e pela data de início
do preparo. Não existindo, a recusa é **\* Requisicao nao cadastrada \***, com o cursor no
campo da data.

Só a inclusão segue sem requisição prévia — e, se já houver requisição naquela data, a
inclusão segue mesmo assim: quem barra é a conferência de sobreposição (RN-14).

[?] A mesma recusa aparece uma segunda vez no fonte, com o cursor no campo da operação,
num caminho que só é alcançado depois de a requisição já ter sido encontrada com a mesma
chave; os dois desfechos se contradizem, e esse segundo não é alcançável. Pergunta ao
site.

### RN-10 — A data de início tem de ser uma data válida

A data de início tem de ser uma data de verdade e num ano entre **1994 e 2099**.
Recusada, a mensagem é **\* Data de inicio de calculo invalida \***, com o cursor no campo
da data. A conferência roda na inclusão; na alteração, na exclusão e na consulta a data é
a da requisição existente.

### RN-11 — A semana do preparo é a semana da data de início, e a segunda-feira tem de ter letra

A semana do preparo é a semana da data de início: o sistema recua dessa data até a
**segunda-feira** e procura, no cadastro das letras de cardápio, a letra daquela
segunda-feira. Sem letra cadastrada, a recusa é
**\* Letra da semana nao cadastrada \***, com o cursor no campo da data. Vale para a
inclusão e para a alteração.

### RN-12 — A semana tem sete dias, e a data limite é calculada

Identificada a semana, o sistema monta os **sete** dias a partir da data de início: a data
limite é a **data de início mais seis dias**, e cada dia fica com o dia do mês, o nome do
dia da semana e a letra de cardápio buscada no cadastro. O servidor **não define** a data
limite: ela é calculada aqui e vai assim para a tela seguinte, mesmo quando a requisição
já existia. A falta de letra em qualquer dia que não a segunda-feira não interrompe nada —
o dia fica sem letra.

[?] A montagem dos sete dias é seguida de uma guarda que reabriria a própria tela se um
critério de cálculo estivesse marcado, mas o programa nunca marca esse critério: o
caminho existe no fonte e não é alcançável. Pergunta ao site.

### RN-13 — A data de início tem de cair no dia de preparo da secretaria

Quando o cadastro de preparo da secretaria define um **dia da semana** para o início, a
data de início informada tem de cair nesse dia; caindo em outro, a recusa é
**\* Inicio de preparo deve ser <dia> \***, com o nome do dia exigido na mensagem e o
cursor no campo da data. Secretaria sem esse dia configurado — ou sem registro no
cadastro — não passa por essa conferência. Vale para a inclusão e para a alteração.

### RN-14 — Duas semanas da mesma unidade não podem se tocar

A tela procura requisição da mesma unidade e coordenação na **véspera** e no **dia
seguinte** à data de início informada. Se a requisição encontrada alcança o novo
intervalo, a recusa é **<- Ja existe requisicao neste intervalo \***, com a data da
requisição que conflita na mensagem e o cursor no campo da data. Vale para a inclusão.

[?] A procura olha só a véspera e o dia seguinte; uma requisição que comece dois dias
antes e termine dentro da nova semana não é vista por essas duas datas. O corpus não diz
se a intenção era varrer o intervalo inteiro. Pergunta ao site.

### RN-15 — A operação só se conclui com a confirmação

Passadas as conferências, a tela pergunta, e só a resposta **S** deixa seguir:

- inclusão — **\* Confirma inclusao do calculo <S/N> ? \***;
- alteração — **\* Confirma alteracao do calculo <S/N> ? \***;
- exclusão — **\* Confirma exclusao do calculo <S/N> ? \***.

A consulta não pergunta nada (RN-18).

A resposta não é livre: a confirmação fica presa à **operação, à unidade e à data de
início** que estavam na tela quando a pergunta foi feita. Se qualquer uma delas mudar
antes da resposta, a confirmação é descartada, e a tela volta a conferir os dados e a
perguntar de novo. Resposta que não seja "S" também não conclui: a pergunta é desfeita e a
tela volta a pedi-la.

### RN-16 — O cálculo da semana é apagado antes da confirmação

Escolhidas a inclusão, a alteração ou a exclusão, a tela apaga as **quantidades calculadas
por subclasse e gênero** daquela unidade e daquela semana **antes** de perguntar a
confirmação. O apagamento não depende da resposta: quem chega à pergunta e não confirma
deixa a semana da unidade sem as quantidades que lá estavam. A consulta não passa por
aqui.

[?] Se o apagamento deveria acontecer só depois do "S" — ou se é intencional, porque a
semana seria recalculada de qualquer modo —, o corpus não diz. Pergunta ao site.

### RN-17 — A exclusão apaga a requisição e o detalhamento, e avisa

Confirmada a exclusão, a tela apaga a **requisição** da unidade e daquela semana e o
**detalhamento por segmento e refeição** dela, e reabre a si mesma mostrando
**Requisicao Excluida** na sua linha de aviso. Nenhuma outra operação apaga a requisição.

### RN-18 — A consulta não grava nada e leva ao detalhamento

A consulta não pergunta confirmação e não apaga nada — nem as quantidades calculadas da
semana —, e leva ao detalhamento a unidade, a coordenação e a semana, com a marca de que a
origem foi esta tela.

### RN-19 — O que a tela entrega à tela seguinte

Concluída a inclusão, a alteração ou a consulta, a tela entrega à **E551T** o registro que
estava na tela — a unidade com o seu nome, a coordenação, os sete dias da semana com as
letras de cardápio e a data de início —, a **operação** e a marca de que a origem foi esta
tela. A E551T abre no **modo que esta deixou**: em inclusão ou alteração, quando a operação
veio da confirmação; em consulta, quando veio da consulta. Quem grava a requisição é a
E551T, não esta tela.

### RN-20 — A tela reabre em consulta quando volta do detalhe, e mostra o que a tela de detalhe encontrou

Quando a sessão traz a marca deixada pela **tela de detalhe** — o que acontece quando o
servidor volta dela —, a tela reabre com a operação forçada para **consulta** e o registro
carregado, de modo que o servidor só vê o que abriu. Nessa volta ela mostra o aviso
**\* Orgao sem segmentos cadastrados \***, que é o que a tela de detalhe encontrou: a
unidade não tem segmento cadastrado.

[?] A tela prevê um segundo aviso, **\* Consulta preparo \***, para quem chega com a marca
de uma outra tela; nenhum programa do acervo grava essa marca, de modo que esse aviso é
inalcançável. Pergunta ao site qual tela deveria deixá-la.

### RN-21 — Os códigos e as datas são conferidos como número

Antes das conferências de negócio, a unidade, a coordenação regional escolar e as duas
datas (início e limite) passam pela edição numérica: o que estiver em branco vira zero, os
zeros à esquerda somem e o que não for número é recusado com o cursor no campo, sem que
nada seja consultado por causa dele.

## Cenários BDD

```gherkin
Funcionalidade: Abrir, alterar, excluir e consultar a semana de preparo de uma unidade

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E550T

  Cenário: RN-01, RN-11 e RN-12 — abrir uma semana nova
    Dado que estou na tela em inclusão
    Quando informo uma unidade da minha coordenação e a data de início do preparo
    Então a semana é identificada a partir da segunda-feira dessa data
    E os sete dias ficam montados, com a letra de cardápio de cada um
    E a data limite fica sendo a data de início mais seis dias

  Cenário: RN-02 — operação que a tela não conhece
    Quando informo uma operação que não é inclusão, alteração, exclusão nem consulta
    Então vejo "* Operacao nao disponivel *"
    E o cursor volta para o campo da operação
    E nada é conferido nem gravado

  Cenário: RN-02 — sem permissão para a operação
    Dado que não tenho a permissão daquela operação no cadastro de autorização
    Quando confirmo
    Então a operação não segue
    E nada é gravado

  Cenário: RN-03 — unidade diferente da minha
    Dado que a minha sessão tem uma unidade
    Quando informo outra unidade
    Então vejo "* Usuario sem acesso a outro orgao *"
    E a mensagem traz o número da minha unidade
    E o cursor volta para o campo da unidade

  Cenário: RN-03 — servidor sem unidade na sessão
    Dado que a minha sessão não tem unidade
    Quando abro a tela
    Então o cursor já está no campo da unidade
    E posso abrir a unidade que eu informar

  Cenário: RN-04 — unidade de outra coordenação
    Dado que a minha sessão tem coordenação regional escolar
    Quando informo uma unidade de outra coordenação
    Então vejo "<- Usuario sem acesso ao grupo deste orgao *"
    E a mensagem traz o número da coordenação da unidade
    E o cursor volta para o campo da unidade

  Cenário: RN-05 — unidade em branco na inclusão
    Dado que estou na tela em inclusão
    Quando confirmo sem informar a unidade
    Então vejo "* Informe o orgao *"
    E o cursor volta para o campo da unidade
    E nada é gravado

  Cenário: RN-05 — unidade que não está cadastrada
    Quando informo uma unidade que não existe no cadastro
    Então vejo "* Orgao nao cadastrado *"
    E o cursor volta para o campo da unidade
    E nada é gravado

  Cenário: RN-06 — unidade de outra secretaria
    Dado que estou incluindo uma semana
    Quando informo uma unidade de outra secretaria
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E nada é gravado

  Cenário: RN-07 — unidade inativa
    Dado que estou incluindo uma semana
    Quando informo uma unidade marcada como inativa
    Então vejo "* Orgao cadastrado como inativo *"
    E nada é gravado

  Cenário: RN-07 — unidade marcada para pedido acumulado
    Dado que estou incluindo uma semana
    Quando informo uma unidade marcada para pedido acumulado
    Então vejo "* Orgao cadastrado para pedido acumulado *"
    E nada é gravado

  Cenário: RN-07 — unidade com dados incompletos
    Dado que estou incluindo uma semana
    Quando informo uma unidade sem os seis dados exigidos
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E nada é gravado

  Cenário: RN-08 — unidade sem segmento cadastrado
    Dado que estou incluindo uma semana
    Quando informo uma unidade sem nenhum segmento de atendimento
    Então vejo "* Orgao sem segmentos cadastrados *"
    E o cursor volta para o campo da unidade

  Cenário: RN-09 — requisição que não existe
    Dado que escolho alterar, excluir ou consultar
    Quando informo uma unidade e uma data sem requisição
    Então vejo "* Requisicao nao cadastrada *"
    E o cursor volta para o campo da data
    E nada é gravado

  Cenário: RN-09 — incluir sobre uma requisição que já existe
    Dado que a unidade já tem requisição naquela data
    Quando escolho incluir e confirmo
    Então a inclusão segue
    E a semana é montada de novo

  Cenário: RN-10 — data de início inválida
    Quando informo uma data que não existe, ou um ano fora de 1994 a 2099
    Então vejo "* Data de inicio de calculo invalida *"
    E o cursor volta para o campo da data
    E nada é gravado

  Cenário: RN-11 — segunda-feira da semana sem letra cadastrada
    Quando informo uma data cuja segunda-feira não tem letra de cardápio
    Então vejo "* Letra da semana nao cadastrada *"
    E o cursor volta para o campo da data

  Cenário: RN-12 — os sete dias e a data limite
    Dado que abro uma semana
    Então os sete dias ficam com o dia do mês, o nome do dia e a letra de cardápio
    E a data limite é calculada, e não informada por mim

  Cenário: RN-13 — data de início fora do dia de preparo
    Dado que a secretaria tem um dia de preparo configurado
    Quando informo uma data de início que não cai nesse dia
    Então vejo "* Inicio de preparo deve ser <dia> *"
    E a mensagem traz o dia exigido
    E o cursor volta para o campo da data

  Cenário: RN-14 — semana que toca outra requisição
    Dado que a unidade já tem requisição na véspera ou no dia seguinte
    Quando abro uma semana que alcança essa requisição
    Então vejo "<- Ja existe requisicao neste intervalo *"
    E a mensagem traz a data da requisição que conflita
    E nada é gravado

  Cenário: RN-15 — inclusão confirmada
    Dado que a tela já me perguntou se confirmo a inclusão
    Quando respondo S sem mudar a operação, a unidade nem a data
    Então a operação segue
    E sou levado ao detalhamento

  Cenário: RN-15 — alteração confirmada
    Dado que a requisição daquela semana existe
    Quando escolho alterar e respondo S à pergunta de alteração
    Então a operação segue
    E sou levado ao detalhamento com a semana alterada

  Cenário: RN-15 — não confirmo
    Dado que a tela já me perguntou se confirmo a inclusão
    Quando respondo N
    Então a confirmação é desfeita
    E a tela volta a conferir os dados e a pedir a confirmação
    E nada é gravado

  Cenário: RN-15 — mudo a data depois da pergunta
    Dado que a tela já me perguntou se confirmo a inclusão
    Quando troco a data de início e respondo S
    Então a confirmação é descartada
    E a tela volta a conferir os dados

  Cenário: RN-16 — o cálculo da semana é apagado antes da pergunta
    Dado que escolho incluir, alterar ou excluir
    Quando chego à pergunta de confirmação
    Então as quantidades calculadas da unidade naquela semana já foram apagadas

  Cenário: RN-17 — exclusão confirmada
    Dado que escolho excluir e respondo S
    Então a requisição e o detalhamento daquela semana são apagados
    E a tela reabre mostrando "Requisicao Excluida"

  Cenário: RN-18 — a consulta não grava nada
    Dado que escolho consultar
    Quando confirmo
    Então sou levado ao detalhamento com a unidade e a semana carregadas
    E a requisição, o detalhamento e as quantidades da semana ficam como estavam

  Cenário: RN-19 — o que a tela entrega à tela seguinte
    Dado que concluí a inclusão ou a alteração
    Quando sou levado à tela de detalhe
    Então ela abre no modo que esta tela deixou
    E recebe a unidade, a coordenação, os sete dias com as letras e a data de início

  Cenário: RN-20 — a volta da tela de detalhe
    Dado que a tela de detalhe me devolve porque a unidade não tem segmento
    Quando esta tela reabre
    Então ela abre em consulta, com o registro carregado
    E vejo "* Orgao sem segmentos cadastrados *"

  Cenário: RN-21 — campo com texto
    Quando informo texto na unidade, na coordenação ou numa das datas
    Então o campo é recusado antes de qualquer conferência de negócio
    E o cursor fica no campo recusado
    E nada é consultado por causa dele
```
