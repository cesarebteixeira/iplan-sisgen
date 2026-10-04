# US — C840C — Consultar a janela de cálculo da coordenação regional escolar

## Estória

Como **servidor de CRE**, quero **consultar, para uma coordenação regional escolar, o
início e o limite da janela de cálculo das estimativas daquele grupo**, para que **eu
veja de uma vez o período que a estimativa do grupo cobre, sem percorrer o cadastro
período a período**.

A estimativa de merenda é calculada por período, e cada período é uma janela: começa
numa data e vale até uma data limite. É o limite que identifica o período e é ele que
distingue um período do outro no cadastro. Quem confere o que já foi calculado para uma
coordenação regional escolar precisa saber qual é essa janela — sem esta consulta, a
única forma de descobrir seria abrir o cadastro do cálculo, período a período, até
achar o que vale.

## Contexto

Jornada S000M → C000M → C800M → C840M → C840C (5 passos).
Ator: servidor de CRE — escolhe uma coordenação regional escolar e vê a janela de
cálculo das estimativas daquele grupo.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os três passos do meio do caminho (`C000M`, `C800M` e `C840M`) são menus: só encaminham
a sessão e não deixam dado de negócio para esta tela — o `C840M` apenas indica que a
tela seguinte é esta. O que a tela aproveita da sessão é o **tipo de órgão** da
secretaria, que é a identidade da coordenação regional escolar e o primeiro componente
de toda leitura de cadastro que a tela faz. A tela **não recebe de quem a chamou** a
coordenação regional escolar nem a operação: ela mesma fixa a operação em consulta e
recebe o grupo digitado pelo servidor.

Esta tela é **terminal**: não encadeia para nenhuma outra, não passa registro nem
operação adiante.

O cadastro de que a tela se serve é o **cálculo da estimativa**: há um registro por
período calculado, e o que distingue um período do outro é a **data limite**. O grupo
consultado tem de existir no **cadastro das coordenações regionais escolares** do
mesmo tipo de órgão.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela é só de consulta, e a operação é fixada por ela mesma

A tela sempre se apresenta em consulta: a cada mensagem do operador ela repõe a
operação de consulta antes de qualquer conferência, de modo que não existe caminho,
nesta tela, em que ela se abra para incluir, alterar ou excluir.

[?] O programa tem uma recusa escrita para a hipótese de a operação não ser a consulta
— a mensagem **\* Operacao nao disponivel \***, com o cursor no campo da operação —,
mas esse ramo é **inalcançável**: a operação da tela é reposta em consulta em todas as
passagens, e a única origem da operação guardada pela tela é a própria constante de
consulta. Ou a guarda vale para um caminho que não está no fonte, ou o ramo ficou
inalcançável. Pergunta ao site.

### RN-02 — É a janela de cálculo que a consulta mostra

Para a coordenação regional escolar informada, a consulta mostra a **data de início** e
a **data limite** do cálculo de estimativa daquele grupo — as duas datas da janela.
O cadastro guarda **26 campos** por registro — entre eles o tipo de órgão, a
coordenação regional escolar e as duas datas da janela — e comporta **10.000
registros** (capacidade é o máximo esperado, parâmetro de dimensionamento, não o que
está cadastrado). A identidade de um registro do cálculo é o **tipo de órgão**, a
**coordenação regional escolar** e o **ano, o mês e o dia limite**: há **um registro por
período calculado**, e é a data limite que separa um período do outro.

[?] O cadastro do cálculo guarda ainda outras duas famílias de datas — dois pares de
datas ligados a grupos de dias —, que esta tela não lê nem mostra; o acervo não diz
para que servem. Pergunta ao site.

### RN-03 — O grupo é obrigatório e tem de estar cadastrado

O servidor informa a **coordenação regional escolar** pelo seu código, de até dois
dígitos. O código **não pode ficar em branco**: em branco, o sistema recusa com
**\* Informe o Grupo \*** e devolve o cursor ao campo do grupo. O código informado tem
de existir no **cadastro das coordenações regionais escolares** para o **tipo de órgão
da sessão**; não existindo, a recusa é **\* Informe um grupo valido \***, também com o
cursor no campo do grupo. A conferência de existência acontece na primeira passagem de
cada consulta; nas passagens seguintes o grupo já aceito não é reconferido.

### RN-04 — A tela consulta o cálculo pelo grupo e pela data limite

A leitura do cálculo usa o **tipo de órgão da sessão**, a **coordenação regional
escolar** informada e a **data limite** — ano, mês e dia —, que ordena o cadastro do
menor para o maior. Os quatro campos que o servidor informa — o grupo, o dia, o mês e o
ano limite — passam por edição numérica antes de a leitura acontecer: campo em branco é
tratado como zero, valor não numérico é recusado e a consulta não segue, e o cursor
volta ao campo recusado.

[?] A edição numérica não confere faixa nem calendário: um dia como **32**, num campo de
dois dígitos, ou um mês fora de 1 a 12 passam pela edição e chegam à leitura, se forem
número. Se o esperado é recusá-los, o caminho não os recusa. Pergunta ao site.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não
está nesta jornada: a conferência numérica é feita por uma rotina de biblioteca cujo
corpo não veio na árvore expandida. Pergunta ao site.

### RN-05 — O grupo sem cálculo é recusado na primeira linha

Achando o grupo no cadastro das coordenações, a consulta procura o cálculo. Não achando,
o sistema avisa **\* Sem calculo p/data limite informada  \*** e não apresenta janela
nenhuma; o aviso é decidido na montagem da **primeira** linha e não se repete nas
demais.

[?] O mesmo campo de resultado que o aviso usa como sinal de "não achei" é o que a
consulta também usa como sinal de "não há mais nada a mostrar", e por isso não se
distingue, pelo fonte, o grupo que **não tem cálculo nenhum** do grupo cujo cálculo
começa depois do ponto procurado. Se os dois casos merecem o mesmo aviso, é pergunta ao
site.

### RN-06 — A consulta não grava nada

Esta tela **não grava**. As operações de incluir, apagar e travar registro existem
declaradas para os três cadastros que ela enxerga — o cadastro das telas do sistema, o
cadastro das coordenações regionais escolares e o cadastro do cálculo da estimativa — e
**nenhuma delas é executada em caminho nenhum**: declarar não é executar. Consultar
aqui não inclui, não altera e não apaga registro algum, e não deixa rastro de auditoria:
a trilha de auditoria não está entre os cadastros que a tela enxerga.

### RN-07 — A tela não encadeia, e o que ficou sem resposta

Esta tela **não encadeia**: terminada a consulta, a sessão volta ao menu por onde se
chegou, e nada — registro, operação ou data — é deixado para outra tela. Não há,
também, sinal de continuação no fonte: a tela não guarda o ponto onde parou, e a única
forma de a consulta olhar outro trecho do cadastro é o servidor informar de novo o grupo
e a data limite.

[?] A tela repete a conferência do grupo e a descrição do cálculo dentro de um laço,
mas não deixa marcador de página seguinte; se o servidor informa uma data limite que
fica **depois** de vários períodos do grupo, não se conclui do fonte se a leitura
posiciona no período **igual ou posterior** à data informada ou se exige a data
**exata**, e é isso que decide se o servidor vê o cálculo daquela data ou o aviso de
que não há cálculo. Os dois comportamentos são compatíveis com o que o fonte mostra e
não se escolhe um dos dois. Pergunta ao site.

[?] A área de trabalho em que a tela guarda o grupo e a data limite já aceitos é
reaproveitada entre as telas da mesma sessão e só é zerada na primeira delas. Se a
consulta que o servidor vê depende de uma consulta anterior feita em outra tela, é
pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consultar a janela de cálculo da coordenação regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C840C

  Cenário: RN-01 — a tela só se apresenta em consulta
    Dado que abro a tela C840C
    Quando a tela é apresentada
    Então ela está em modo de consulta
    E nenhuma inclusão, alteração ou exclusão é oferecida
    E nada é gravado

  Cenário: RN-02 — a janela de cálculo do grupo
    Dado que existe cálculo de estimativa para a coordenação regional escolar informada
    Quando envio a consulta
    Então vejo a data de início e a data limite da janela daquele grupo
    E nada é gravado

  Cenário: RN-03 — grupo não informado
    Dado que deixo o campo da coordenação regional escolar em branco
    Quando envio a consulta
    Então vejo a mensagem "* Informe o Grupo *"
    E o cursor volta ao campo do grupo
    E nenhuma leitura de cálculo é feita

  Cenário: RN-03 — grupo não cadastrado
    Dado que informo uma coordenação regional escolar que não existe para o tipo de órgão da minha sessão
    Quando envio a consulta
    Então vejo a mensagem "* Informe um grupo valido *"
    E o cursor volta ao campo do grupo
    E nenhuma leitura de cálculo é feita

  Cenário: RN-04 — digitação não numérica em um campo informado
    Dado que digito, no grupo ou no dia, no mês ou no ano limite, algo que não é número
    Quando envio a consulta
    Então a consulta não segue
    E o cursor volta ao campo recusado
    E nada é gravado

  Cenário: RN-05 — grupo sem cálculo para a data limite informada
    Dado que o grupo existe mas não tem cálculo para a data limite informada
    Quando envio a consulta
    Então vejo a mensagem "* Sem calculo p/data limite informada  *"
    E nenhuma janela é apresentada

  Cenário: RN-06 — a consulta não grava nada
    Dado que estou na tela C840C
    Quando consulto a janela de um grupo
    Então nenhum registro é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: RN-07 — a tela não encadeia
    Dado que consultei a janela de um grupo
    Quando a consulta termina
    Então nenhum registro e nenhuma operação são passados adiante
    E volto ao menu por onde cheguei
```
