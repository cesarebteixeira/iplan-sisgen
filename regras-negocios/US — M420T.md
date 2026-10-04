# US — M420T — Manter o mapa diário de refeições da creche

## Estória

Como **servidor da CRE**, quero **registrar e conferir, para uma creche e um dia de
um mês de referência, o mapa de refeições daquele dia — o cardápio e o número de
refeições de cada refeição e de cada faixa de alunos —**, para que **aquele dia
tenha os números com que a secretaria presta contas da merenda da creche**.

O mapa do dia é o que fecha o mês da creche: é dele que saem as refeições servidas
em cada dia, e sem ele o dia não tem como ser conferido. Os números informados não
podem passar os do perfil mensal da creche, e o cardápio de cada refeição tem de
estar cadastrado para a semana e servir àquela refeição. Quando não houve
atendimento, o sistema exige o motivo e a justificativa — a ausência fica
explicada. Incluir o mapa de um dia fecha os mapas abertos do mês anterior: é
assim que um mês se encerra, e depois disso ele não se altera mais por aqui.

## Contexto

Jornada S000M → M000M → M040T → M420T.

Ator: servidor da CRE — registra e confere o mapa diário de refeições de uma
creche da sua coordenadoria regional escolar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio. O `M000M` é um menu e não grava
nada: apenas encaminha. O `M040T` é a tela que escolhe o dia do mapa e que
encaminha a creche para esta tela e os demais órgãos para a `M400T`; o dia
escolhido e o órgão ficam na sessão e são o que esta tela usa. As conferências de
tela, de estação, de rota e de permissão que a `M420T` executa antes de aceitar a
operação são as mesmas de todas as telas e já estão no documento da entrada: ficam
no anexo de evidências, em **Regras que se revelaram da entrada**.

As regras abaixo são só as desta tela. A jornada termina nesta tela: ela reexibe a
si mesma depois de processar o dia e, quando o dia passa do corte de julho de
2008, devolve o servidor à tela do mapa do mês (a `M040T`) — o que ela entrega em
cada caso, e em que modo a tela seguinte reabre, está na RN-22.

---

## Regras de negócio

### RN-01 — A tela mantém o mapa do dia; a exclusão não apaga o registro

A `M420T` **inclui, altera, exclui e consulta** o mapa de refeições de um dia da
creche. A inclusão cria o mapa do dia; a alteração regrava os cardápios e as
quantidades; a exclusão **não apaga o registro** — marca-o como excluído, e o dia
sai das leituras seguintes; a consulta não grava nada. Cada inclusão, alteração e
exclusão deixa rastro na auditoria; a consulta não deixa. Nenhuma exclusão física
é executada por esta tela: a rotina de apagar existe declarada e não é chamada por
caminho nenhum.

[?] A alteração grava o mapa por cima do que estava lá, e a auditoria registra o
conteúdo posterior: o conteúdo anterior do mapa vai em branco, mesmo o programa
tendo lido o registro antes de alterá-lo. Se a intenção era guardar o antes e o
depois, o antes está faltando. Pergunta ao site.

### RN-02 — O mapa é de uma creche, de um mês de referência e de um dia

O mapa é identificado pela **creche (o órgão filho)**, pela **coordenação regional
escolar a que ela pertence** e pelo **dia**, informado por dia e mês dentro do
**ano de referência**. O mês e o ano de referência são os que localizam o
**período do mapa**; o dia é o que se está mapeando. No cabeçalho a tela mostra o
nome da creche, o tipo de órgão da secretaria, a data do sistema, o dia da semana
e a **situação do mapa daquele dia** — aberto ou fechado.

[?] A coordenadoria é digitável na tela, mas o programa a substitui pela do
cadastro da creche depois de achar o órgão. Ou o campo serve para conferência, ou
o que o servidor digita é ignorado. Pergunta ao site.

### RN-03 — O que o mapa do dia registra

Para cada dia a tela guarda, por **refeição** e por **faixa de alunos**, o
**código do cardápio** e o **número de refeições** servidas. São **cinco
refeições** — as que o cadastro de refeições da creche define, e cujos nomes a
tela exibe para elas — e **nove faixas de idade**, as do perfil mensal da creche:
1, 2, 3, 4, 5, 6, 7, 9 e 12 meses. Fora dessas linhas há **uma décima coluna**,
que só é usada em duas das refeições. **Duas linhas de sobremesa** completam o
quadro: os seus cardápios só existem para as quatro faixas mais velhas (6, 7, 9 e
12 meses), e a segunda delas também para a décima coluna. Ao todo são **55 células
de cardápio e 55 de quantidade**. O mapa guarda ainda a semana do cardápio, a
justificativa e o motivo de não atendimento, e o registro de quem o gravou e
quando.

[?] O que é, em negócio, a décima coluna? O programa a compara com o número de
matriculados do perfil do mês, e ela só aparece no almoço e numa das sobremesas; o
acervo não a nomeia. Pergunta ao site.

[?] O que distingue as duas linhas de sobremesa, e por que as sobremesas só valem
para as quatro faixas mais velhas? O corpus mostra as duas linhas e os seus
limites, não o que cada uma significa. Pergunta ao site.

[?] O acervo não nomeia as cinco refeições: elas vêm do cadastro da creche, e os
rótulos técnicos que o programa usa não são vocabulário de negócio. Pergunta ao
site quais são os nomes que o operador lê.

### RN-04 — A tela abre conforme quem a chamou e o que o dia tem

Ao ser aberta pela **tela do mapa do mês** com um dia escolhido, a `M420T` procura
o mapa daquele dia: **achando, abre em consulta**, mostrando o que está gravado;
**não achando, abre em inclusão**, pronta para o servidor informar o dia. Vindo de
**qualquer outra origem** — a própria tela reexibida depois de processar um dia,
ou qualquer outra entrada —, ela **não carrega dia nenhum**: abre em inclusão, com
a creche e a coordenadoria do vínculo do servidor. Em qualquer dos casos o
servidor pode trocar a operação na própria tela.

### RN-05 — A tela só serve dias até julho de 2008

A tela só trabalha com dias **até julho de 2008**. Informado um dia de **1º de
agosto de 2008 em diante**, ela não processa: atualiza o contexto do mês com
aquele dia e **devolve o servidor à tela que escolhe o dia**, sem gravar nada.
Isso vale para incluir, alterar, excluir e consultar.

[?] O corte é uma data gravada como `20080800` — um dia zero —, e a comparação é
feita contra ela; na prática, barra de 1º de agosto de 2008 em diante. Se a
intenção era outro dia-limite, o número não a expressa; e qual tela passa a
atender esses dias não está nesta jornada. Pergunta ao site.

### RN-06 — A creche tem de ser a do servidor, estar apta e ser creche

Antes de qualquer operação, a tela confere o **órgão**: se é o do vínculo do
servidor — senão * Usuario sem acesso a outro orgao *; se está cadastrado — senão
* Orgao nao cadastrado *; se está ativo — senão * Orgao cadastrado como inativo *;
se está cadastrado como **creche** — senão * Orgao nao cadastrado como Creche *;
se tem os dados completos (bairro, órgão pai, nome, endereço, matriculados e
pessoas) — senão * Orgao cadastrado com dados incompletos *; se é da secretaria da
sessão — senão * Orgao nao pertence a esta secretaria *; e se o servidor tem
acesso à coordenadoria regional do órgão — senão * Usuario sem acesso ao grupo
deste orgao *. Sem órgão informado, a tela pede * Informe o orgao *.

[?] Se a recusa barra a gravação. A recusa mostra a mensagem e desvia para o fim
da lógica, e quem decide se a passagem de gravação roda depois é o marcador de
erro do sistema; nenhuma recusa por mensagem deste programa marca esse erro, e a
rotina que mostra a mensagem não está no acervo. Se ela não marcar o erro, a
recusa não impede a gravação. Pergunta ao site.

### RN-07 — O mês de referência e o dia têm de estar no período do mapa

O mês e o ano de referência têm de estar informados e válidos, e o mês tem de
constar da **tabela de períodos do mapa**, que define o início e o limite do
período. O dia do mapa também: precisa ser uma data válida, **não pode ser
posterior à data de hoje** e tem de cair **dentro do intervalo do período**.
Faltando o mês ou o ano, a tela pede * Informe o Mes/Ano *; faltando o dia,
* Informe o Dia/Mes *; data de mês ou ano impossível, * Mes/Ano invalidos *; mês
fora da tabela, * Mes/Ano nao cadastr.na tab.de periodos do mapa *; dia
impossível, * Dia/Mes invalidos *; data futura, * Data do mapa maior que data
atual *; fora do período, * Dia/Mes fora do intervalo do periodo *.

### RN-08 — A semana do dia vem do calendário de semanas da coordenadoria

A semana do cardápio (A, B, C ou D) que a tela apresenta é a que o **calendário de
semanas da coordenadoria regional escolar** define para aquele dia. Ao processar,
a tela apenas exige que a semana informada seja uma das quatro letras: qualquer
outra coisa é recusada com * Informe semana com A / B / C / D *.

[?] A tela traz a semana do calendário, mas aceita que o servidor informe outra
das quatro letras, e a alteração nem chega a conferir a semana. Ou o calendário é
só uma sugestão, ou a conferência devia amarrar o dia à semana do calendário.
Pergunta ao site.

### RN-09 — O mês tem de ter perfil cadastrado para a creche

A inclusão e a alteração exigem que o **mês tenha perfil de atendimento cadastrado
para a creche** — aberto ou fechado. Não havendo, a operação é recusada com
* Nao existe perfil cadastrado para o Orgao *. A exclusão e a consulta não fazem
essa conferência.

### RN-10 — A inclusão recusa um dia que já tem mapa

A inclusão é recusada se **já existir mapa para aquele dia**: * Mapa ja cadastrado
para este Dia/Mes *. A conferência não enxerga os mapas já marcados como
excluídos.

[?] Como o mapa excluído continua guardando a mesma identificação do dia, não se
sabe se a nova inclusão convive com ele ou o substitui. Pergunta ao site.

### RN-11 — Alterar e excluir exigem ter consultado aquele dia

Para **alterar** ou **excluir**, o servidor precisa ter **consultado antes aquele
mesmo dia** — a mesma creche, o mesmo mês de referência e o mesmo dia. Não tendo,
a recusa é * Consulte antes de alterar * ou * Consulte antes de excluir *,
conforme a operação. E o dia consultado precisa estar cadastrado: não estando, a
recusa é * Mapa nao cadastrado para este Dia/Mes *.

### RN-12 — Só se altera ou exclui mapa aberto, e a tela mostra a situação

A tela mostra, no cabeçalho, se o mapa do dia está **aberto** ou **fechado**. Só
se altera ou exclui **mapa aberto**: estando o mapa fechado, a recusa é * Mapas
fechados para este Mes/Ano *. O mapa nasce aberto e é fechado pela inclusão de um
dia do mês seguinte (RN-18).

[?] A recusa fala do mês e do ano, mas a conferência olha a situação do mapa
**daquele dia**; se o que se quer barrar é o mês fechado, o alvo é outro.
Pergunta ao site.

### RN-13 — O cardápio tem de existir e valer para a data, a semana e a refeição

O cardápio informado tem de **estar cadastrado e valer na data do mapa** — senão
* Cardapio nao cadastrado *; tem de **estar cadastrado na semana** do dia — senão
* Cardapio nao cadastrado nesta semana *; e a **refeição** a que ele pertence tem
de estar cadastrada — senão * Refeicao nao cadastrada * — e o cardápio tem de
servir àquela refeição — senão * Cardapio nao cadastrado nesta refeicao *. Há
ainda duas recusas de tipo: * Cardapio cadastrado como sobremesa *, quando um
cardápio de sobremesa é informado numa das cinco refeições, e * Cardapio nao
cadastrado como sobremesa *, quando um cardápio de refeição é informado numa das
duas linhas de sobremesa.

### RN-14 — Cada cardápio informado exige a quantidade, e a quantidade exige o cardápio

Cada **cardápio informado** tem de ter a sua **quantidade** — sem ela, a recusa é
* Informe o NRP para esta refeicao * —, e cada **quantidade informada** tem de ter
o seu **cardápio** — sem ele, * Nao informe o NRP para esta refeicao *. A célula
com **nenhum dos dois é simplesmente ignorada**: não gera conferência e não vai
para o mapa.

### RN-15 — As quantidades não podem passar as do perfil mensal

As quantidades informadas **não podem passar as do perfil mensal da creche**.
Para cada refeição, o sistema soma as quantidades de todas as faixas e compara com
o **total geral do perfil**, que é a soma das duas formas de todas as idades; e a
décima coluna, quando usada, é comparada com o **número de matriculados** do
perfil. Passando, a recusa é * <- Somatorio NRP's maior que perfil *.

[?] O acervo chama as quantidades de NRP e não traz o que a sigla abre. Pergunta
ao site.

### RN-16 — Sem atendimento, o motivo e a justificativa

Quando **nenhuma refeição tem cardápio** — nenhuma célula do quadro foi
preenchida —, a tela exige que se informe o **motivo do não atendimento**, uma das
quatro marcações da máscara: sem nenhuma, a recusa é * Informe motivo do nao
atendimento *. A marcação do motivo é única: informada uma das três primeiras, as
demais são limpas e o código da justificativa é zerado; o código preenchido marca
a quarta. A quarta marcação exige o **código da justificativa**: sem o código,
* Informe o codigo da justificativa *; e o código tem de estar cadastrado para a
creche — senão * Justificativa nao cadastrada *.

[?] A marca de "houve atendimento" só é ligada pelas cinco refeições: um dia em
que só as sobremesas foram informadas ainda exige o motivo do não atendimento.
Pergunta ao site.

[?] Os quatro motivos e o que cada um significa. A tela usa quatro marcações e só
a quarta carrega a justificativa, mas o acervo não diz o nome de cada motivo nem
qual deles é o da quarta marcação. Pergunta ao site.

### RN-17 — A consulta não grava nada

Na **consulta**, a tela lê o mapa do dia e o mostra — situação, semana, cardápios
e quantidades — e traz a descrição da justificativa. Não grava, não trava
registro, não fecha mapa e não gera rastro de auditoria. A consulta também não
confere os cardápios informados nem as quantidades: ela só exibe.

### RN-18 — Ao incluir o mapa de um dia, os mapas abertos do mês anterior são fechados

Ao **incluir** o mapa de um dia, o sistema **fecha os mapas abertos do mês
anterior** da mesma creche e da mesma coordenadoria: percorre-os e grava cada um
como fechado, com a matrícula, a estação, a data e a hora. Depois disso, aquele
mês anterior não aceita mais alteração nem exclusão por esta tela (RN-12).

### RN-19 — Toda gravação deixa rastro na auditoria

Toda inclusão, alteração e exclusão grava, além do mapa, um registro de auditoria
com a tela de origem, a operação, o cadastro que a originou, o conteúdo posterior
do mapa, a matrícula do funcionário, a estação, a sessão (dia, mês, ano e hora) e
o tipo de órgão. A consulta não gera registro.

### RN-20 — O que a tela enxerga e o que ela grava

O programa declara, para cada um dos **treze** cadastros que enxerga, as rotinas
de incluir, apagar e travar — e isso é declaração, não uso. **Onze** desses
cadastros são lidos do cadastro, **um** — o mapa dos órgãos que não são creche —
não chega a ser lido, e só **dois recebem gravação**: o mapa do dia e a auditoria.
Nenhuma rotina de apagar é executada.

[?] O cadastro do mapa dos órgãos que não são creche é declarado e não é lido,
mas a descrição da justificativa do dia é procurada a partir do campo de
justificativa **desse** cadastro ao reabrir um dia que já tem mapa, e a partir do
campo do mapa da creche na consulta. Ou os dois campos compartilham o mesmo
espaço, ou uma das passagens procura no lugar errado. Pergunta ao site.

### RN-21 — Ao abrir um dia sem mapa, a tela já propõe os cardápios

Quando o dia ainda não tem mapa, a tela chega preenchida com o **cardápio
previsto** para cada refeição e cada faixa: o do **cadastro de cardápios por
faixa e refeição** da creche, para a semana do dia. O servidor pode trocar o que
vier proposto.

[?] O cardápio proposto é o do **dia da semana de hoje**, e não o do dia que está
sendo mapeado — o cadastro é lido para a data do mapa, mas a coluna escolhida é a
do dia da semana corrente. Se o servidor mapeia um dia passado, a sugestão pode
não ser a daquele dia. Pergunta ao site.

### RN-22 — O que a tela entrega à tela seguinte

A `M420T` não termina em menu. Ao processar o dia — na inclusão, na alteração, na
exclusão e também na consulta —, ela **reexibe a si mesma**, deixando na sessão a
creche, o mês e o ano de referência, o dia e a semana do dia processado: é assim
que a tela reabre no mesmo dia. Quando o dia informado passa de julho de 2008, ela
em vez disso **devolve o servidor à tela do mapa do mês** (a `M040T`), deixando na
sessão o mês e o dia daquele dia, junto com a operação informada, para que aquela
tela reabra posicionada nele — e sem gravar nada (RN-05). Em qualquer dos casos a
tela seguinte reconhece, pela marca de origem deixada na sessão, que foi esta tela
que a chamou.

[?] A tela entrega a operação junto com o dia, mas a tela do mapa do mês decide o
próprio modo pela existência do mapa daquele dia; não se sabe se a operação
entregue chega a ser usada, ou se é sobrescrita. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter o mapa diário de refeições da creche

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M420T

  Cenário: RN-04 — abrir um dia que já tem mapa
    Dado que a creche do meu vínculo tem mapa para o dia escolhido
    Quando chego à tela M420T vindo da tela do mapa do mês
    Então a tela abre em consulta, com os cardápios e as quantidades daquele dia
    E vejo a situação do mapa e a semana do dia

  Cenário: RN-04 — abrir um dia que ainda não tem mapa
    Dado que a creche do meu vínculo não tem mapa para o dia escolhido
    Quando chego à tela M420T vindo da tela do mapa do mês
    Então a tela abre em inclusão, pronta para eu informar o dia

  Cenário: RN-04 — abrir a tela sem vir da tela do mapa do mês
    Dado que chego à tela M420T sem vir da tela do mapa do mês
    Quando a tela abre
    Então ela abre em inclusão, com a creche e a coordenadoria do meu vínculo
    E não há dia nem mês de referência carregados

  Cenário: RN-21 — o dia em inclusão já vem com os cardápios propostos
    Dado que o dia ainda não tem mapa
    Quando a tela abre em inclusão
    Então cada refeição e cada faixa já trazem o cardápio previsto no cadastro
    E eu posso trocar o que veio proposto

  Cenário: RN-01, RN-19 — incluir o mapa de um dia
    Dado que a creche tem perfil cadastrado no mês de referência
    E o dia está dentro do período do mapa
    E aquele dia ainda não tem mapa
    Quando informo a inclusão, o dia, a semana e os cardápios com as quantidades
    Então o sistema cria o mapa daquele dia, aberto
    E registra a operação na auditoria

  Cenário: RN-01, RN-19 — alterar as quantidades de um dia
    Dado que consultei aquele dia nesta sessão
    E o mapa do dia está aberto
    Quando informo a alteração e regravo os cardápios e as quantidades
    Então o sistema grava o mapa com os novos números
    E registra a operação na auditoria

  Cenário: RN-01, RN-19 — excluir o mapa de um dia
    Dado que consultei aquele dia nesta sessão
    E o mapa do dia está aberto
    Quando informo a exclusão
    Então o sistema marca o mapa como excluído
    E o dia sai das leituras
    E registra a operação na auditoria

  Cenário: RN-17 — a consulta não grava nada
    Dado que o dia tem mapa
    Quando informo a consulta
    Então vejo a situação, a semana, os cardápios e as quantidades do dia
    E não há gravação, nem trava de registro, nem rastro de auditoria

  Cenário: RN-05 — dia de agosto de 2008 em diante
    Dado que informo um dia de 1º de agosto de 2008 em diante
    Quando tento incluir, alterar, excluir ou consultar
    Então o sistema me devolve à tela que escolhe o dia
    E nada é gravado

  Cenário: RN-06 — órgão que não é creche
    Dado que o órgão informado não está cadastrado como creche
    Quando informo qualquer operação
    Então vejo a mensagem "* Orgao nao cadastrado como Creche *"
    E nada é gravado

  Cenário: RN-06 — órgão não cadastrado, inativo ou com dados incompletos
    Dado que o órgão informado não existe no cadastro
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E quando o órgão está cadastrado como inativo vejo "* Orgao cadastrado como inativo *"
    E quando falta bairro, órgão pai, nome, endereço, matriculados ou pessoas vejo "* Orgao cadastrado com dados incompletos *"

  Cenário: RN-06 — órgão de outra secretaria ou de outra coordenadoria
    Dado que o órgão informado não é da secretaria da sessão
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E quando o órgão é de uma coordenadoria à qual não tenho acesso vejo "* Usuario sem acesso ao grupo deste orgao *"

  Cenário: RN-06 — órgão fora do vínculo do servidor
    Dado que o meu vínculo tem uma creche
    Quando informo outra creche
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"

  Cenário: RN-06 — órgão em branco
    Dado que o meu vínculo não tem órgão e eu não informo nenhum
    Quando confirmo a operação
    Então vejo a mensagem "* Informe o orgao *"

  Cenário: RN-07 — mês, ano e dia não informados
    Quando deixo o mês e o ano de referência em branco
    Então vejo a mensagem "* Informe o Mes/Ano *"
    E quando deixo o dia em branco vejo "* Informe o Dia/Mes *"

  Cenário: RN-07 — mês, ano ou dia impossíveis
    Dado que informo um mês ou um ano que não existem
    Então vejo a mensagem "* Mes/Ano invalidos *"
    E quando informo um dia que não existe vejo "* Dia/Mes invalidos *"

  Cenário: RN-07 — mês fora da tabela de períodos do mapa
    Dado que informo um mês e um ano que não constam da tabela de períodos
    Quando tento abrir o mapa do dia
    Então vejo a mensagem "* Mes/Ano nao cadastr.na tab.de periodos do mapa *"

  Cenário: RN-07 — dia posterior a hoje
    Dado que informo um dia depois de hoje
    Quando tento abrir o mapa do dia
    Então vejo a mensagem "* Data do mapa maior que data atual *"

  Cenário: RN-07 — dia fora do intervalo do período
    Dado que informo um dia fora do início e do limite do período do mês
    Então vejo a mensagem "* Dia/Mes fora do intervalo do periodo *"

  Cenário: RN-08 — semana diferente de A, B, C ou D
    Dado que informo na semana algo diferente de A, B, C e D
    Quando tento incluir o mapa do dia
    Então vejo a mensagem "* Informe semana com A / B / C / D *"

  Cenário: RN-09 — mês sem perfil cadastrado para a creche
    Dado que o mês de referência não tem perfil de atendimento para a creche
    Quando tento incluir ou alterar
    Então vejo a mensagem "* Nao existe perfil cadastrado para o Orgao *"
    E nada é gravado

  Cenário: RN-10 — incluir um dia que já tem mapa
    Dado que aquele dia já tem mapa
    Quando tento incluir
    Então vejo a mensagem "* Mapa ja cadastrado para este Dia/Mes *"
    E nada é gravado

  Cenário: RN-11 — alterar ou excluir sem ter consultado aquele dia
    Dado que não consultei aquele dia nesta sessão
    Quando tento alterar
    Então vejo a mensagem "* Consulte antes de alterar *"
    E quando tento excluir vejo "* Consulte antes de excluir *"

  Cenário: RN-11 — dia sem mapa cadastrado
    Dado que o dia não tem mapa
    Quando tento alterar, excluir ou consultar
    Então vejo a mensagem "* Mapa nao cadastrado para este Dia/Mes *"

  Cenário: RN-12 — mapa fechado não aceita alteração nem exclusão
    Dado que o mapa do dia está fechado
    Quando tento alterar ou excluir
    Então vejo a mensagem "* Mapas fechados para este Mes/Ano *"
    E o mapa continua como está

  Cenário: RN-13 — cardápio não cadastrado ou fora da semana
    Dado que informo um cardápio que não vale na data do mapa
    Então vejo a mensagem "* Cardapio nao cadastrado *"
    E quando informo um cardápio que não está cadastrado na semana do dia vejo "* Cardapio nao cadastrado nesta semana *"

  Cenário: RN-13 — cardápio de sobremesa numa refeição, e o contrário
    Dado que informo, numa das cinco refeições, um cardápio cadastrado como sobremesa
    Então vejo a mensagem "* Cardapio cadastrado como sobremesa *"
    E quando informo um cardápio de refeição numa das linhas de sobremesa vejo "* Cardapio nao cadastrado como sobremesa *"

  Cenário: RN-13 — refeição não cadastrada ou cardápio que não serve à refeição
    Dado que a refeição da coluna não está cadastrada para a creche
    Então vejo a mensagem "* Refeicao nao cadastrada *"
    E quando o cardápio não serve àquela refeição vejo "* Cardapio nao cadastrado nesta refeicao *"
    E nada é gravado

  Cenário: RN-14 — quantidade sem cardápio e cardápio sem quantidade
    Dado que informo uma quantidade numa célula sem cardápio
    Então vejo a mensagem "* Nao informe o NRP para esta refeicao *"
    E quando informo um cardápio sem nenhuma quantidade vejo "* Informe o NRP para esta refeicao *"
    E nada é gravado

  Cenário: RN-14 — célula sem cardápio e sem quantidade é ignorada
    Dado que deixo uma célula sem cardápio e sem quantidade
    Quando confirmo a operação
    Então aquela célula não gera conferência nenhuma
    E não vai para o mapa

  Cenário: RN-15 — quantidade acima do perfil do mês
    Dado que a soma das quantidades de uma refeição passa o total geral do perfil
    Quando tento incluir ou alterar
    Então vejo a mensagem "* <- Somatorio NRP's maior que perfil *"
    E nada é gravado

  Cenário: RN-15 — a décima coluna acima do número de matriculados
    Dado que a quantidade da décima coluna passa o número de matriculados do perfil
    Quando tento incluir ou alterar
    Então vejo a mensagem "* <- Somatorio NRP's maior que perfil *"
    E nada é gravado

  Cenário: RN-16 — dia sem atendimento e sem motivo informado
    Dado que nenhuma célula do quadro tem cardápio
    E não marco nenhum motivo
    Quando confirmo a operação
    Então vejo a mensagem "* Informe motivo do nao atendimento *"
    E nada é gravado

  Cenário: RN-16 — motivo que exige o código da justificativa
    Dado que nenhuma célula do quadro tem cardápio
    E marco o motivo que exige a justificativa
    E deixo o código em branco
    Então vejo a mensagem "* Informe o codigo da justificativa *"
    E quando informo um código que não está cadastrado para a creche vejo "* Justificativa nao cadastrada *"

  Cenário: RN-16 — o motivo é único
    Dado que marco um dos três primeiros motivos
    Quando confirmo a operação
    Então as outras marcações são limpas
    E o código da justificativa é zerado

  Cenário: RN-18 — incluir um dia fecha os mapas abertos do mês anterior
    Dado que o mês anterior tem mapas abertos para a creche
    Quando incluo o mapa de um dia deste mês
    Então os mapas abertos do mês anterior ficam fechados
    E não aceitam mais alteração nem exclusão por esta tela

  Cenário: RN-20 — o que a tela grava
    Dado que faço uma inclusão, uma alteração e uma exclusão
    Quando o sistema processa cada operação
    Então só o mapa do dia e a auditoria recebem gravação
    E nenhum registro é apagado fisicamente

  Cenário: RN-22 — depois de processar, a tela reabre no mesmo dia
    Dado que incluí, alterei, excluí ou consultei o mapa de um dia
    Quando a operação termina
    Então a tela reabre com a creche, o mês de referência, o dia e a semana daquele dia

  Cenário: RN-22 — a volta à tela do mapa do mês posiciona no dia informado
    Dado que informo um dia que passa de julho de 2008
    Quando tento incluir, alterar, excluir ou consultar
    Então volto à tela do mapa do mês já posicionada naquele mês e naquele dia
    E a operação que informei vai junto
    E nada é gravado
```
