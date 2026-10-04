# US — E050T — Requisição de cálculo do órgão filho SDI

## Estória

Como **servidor da CRE que responde pelo preparo da alimentação escolar da sua
coordenadoria**, quero **abrir a requisição de cálculo de um órgão filho SDI, informando a data
de início do preparo e a data de início da entrega, e confirmar o registro**, para que **a
semana de preparo daquele órgão fique reservada no calendário da coordenadoria e a tela
seguinte possa abrir o mapa dos dias de entrega**.

O preparo da alimentação escolar de uma coordenadoria é aberto por uma data: é a partir dela que
os dias de entrega da semana são distribuídos, e é ela que a tela seguinte usa para procurar o
mapa da semana. Enquanto essa requisição não existe, o órgão daquela coordenadoria não tem
semana de preparo aberta e não há como gerar o mapa de entrega. A requisição também é o que
protege o período: uma vez calculada, ela não pode mais ser alterada por esta tela.

## Contexto

Jornada S000M → E000M → E050M → E050T.
Ator: servidor de CRE — abre, altera, exclui ou consulta a requisição de cálculo de um órgão
filho SDI da sua secretaria, para uma coordenação regional escolar e uma data de preparo.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**,
não regra de negócio. O `E000M` e o `E050M` não gravam nada: só encaminham, e não registram
origem nem operação na sessão.

Esta tela **muda de comportamento conforme quem a chamou** — é a regra mais fácil de se perder,
porque não aparece em campo nenhum da tela. Quando ela vem do menu, a operação chega em branco e
a tela abre como **inclusão** e espera os dados (RN-01). Quando ela é reaberta pela tela
seguinte, a operação vem preenchida pela tela que a chamou, e o modo (alterar, excluir ou
consultar) é decidido lá. E há um terceiro caso: alguns caminhos internos fazem a tela reabrir a
si mesma com a operação na sessão, e aí ela é recusada em vez de executada (RN-14).

O que esta tela usa do que veio antes é a **secretaria, a coordenação regional escolar, o vínculo
do servidor com o órgão filho, a matrícula, o código de acesso, o privilégio e a data do
sistema** da sessão; isso é regra da entrada e está no anexo de evidências, em **Regras que se
revelaram da entrada**.

## Regras de negócio

### RN-01 — A tela traz quatro operações, e a permissão de cada uma é conferida antes

A tela serve para **incluir**, **alterar**, **excluir** e **consultar** a requisição de cálculo
de um órgão filho SDI. A operação é conferida com o serviço de permissão antes de qualquer
conferência de dados: sem a permissão da operação pedida, nada segue e nada é gravado. Informada
qualquer outra operação, a recusa é **\* Operacao nao disponivel \***, com o cursor de volta ao
campo da operação e nada gravado.

Quando a tela é aberta pelo menu, a operação chega em branco e a tela abre como **inclusão**.
Quando é reaberta pela tela seguinte, a operação vem preenchida por ela — é essa tela que decide
se a requisição será alterada, excluída ou apenas consultada. O que a tela mostra no rodapé de
situação é limpo a cada ida e volta, e é preenchido só no caminho que grava.

### RN-02 — O órgão filho SDI é obrigatório

O código do órgão filho SDI tem de ser informado. Em branco, a recusa é **\* Informe o orgao \***,
com o cursor de volta ao campo e nada gravado.

### RN-03 — A coordenação regional escolar é obrigatória

O código da coordenação regional escolar tem de ser informado. Em branco, a recusa é **\* Informe
o grupo \***, com o cursor de volta ao campo e nada gravado.

### RN-04 — A data de início do preparo tem de ser uma data válida entre 1994 e 2099

A data de início do preparo (dia, mês e ano) identifica a requisição junto com o órgão filho e a
coordenação. Ela é conferida como data: se não for uma data válida, ou se o ano ficar fora de
1994 a 2099, a recusa é **\* Data de inicio de calculo invalida \***, com o cursor de volta ao
campo e nada gravado. Os campos de data da tela passam também pela edição numérica, e o campo que
não passar recebe a mensagem de digitação no próprio campo.

### RN-05 — A entrega não pode começar antes do preparo

A data de início da entrega tem de ser **igual ou posterior** à data de início do preparo. Se for
anterior, a recusa é **\* Data de entrega maior que data da requisicao \***, com o cursor de volta
ao campo e nada gravado. A conferência só roda quando há uma data de entrega a conferir; a
consulta não a executa.

### RN-06 — Entre o preparo e a entrega não podem passar mais de 7 dias

A diferença, em dias, entre a data de início da entrega e a data de início do preparo não pode
passar de 7. Acima disso, a recusa é **\* Difer.entre preparo e entrega maior que 7 dias \***,
com o cursor de volta ao campo e nada gravado.

### RN-07 — A quantidade de dias de entrega é obrigatória e não passa de 5

A tela pede a quantidade de dias de entrega. Em branco ou zero, a recusa é **\* Informe a
quantidade de dias de entrega \***; acima de 5, a recusa é **\* Quantidade maxima de dias de
entrega = 5 \***. Nas duas, o cursor volta ao campo e nada é gravado. A conferência não roda na
exclusão nem na consulta.

### RN-08 — Os dias de entrega pulam sábado, domingo e feriado

A partir da data de início da entrega, a tela conta os dias de entrega **pulando sábados,
domingos e os feriados da secretaria**, e a última data desse avanço é o **limite da entrega**,
que fica gravado na requisição. O limite é refeito quando a quantidade de dias muda. Quando a
data de início da entrega cai em sabado, a recusa é **\* Inicio da entrega nao deve ser um
sabado \***; em domingo, **\* Inicio da entrega nao deve ser um domingo \***; em dia marcado como
feriado para a secretaria, **\* Inicio da entrega nao deve ser um feriado \***. Nas três, o
cursor volta ao campo e nada é gravado.

[?] As três recusas de início de entrega em sábado, domingo ou feriado são decididas pelo **dia em
que o cálculo roda**, não pela data de início informada. Ou a tela se recusa a calcular quando o
dia do cálculo cai em fim de semana, ou a conferência deveria olhar a data informada. Pergunta ao
site.

### RN-09 — A permissão de entrega da coordenadoria fica fora do caminho

A conferência que confronta o período pedido com a **permissão de entrega** cadastrada para a
coordenação não é executada por nenhuma das quatro operações desta tela. A procura existe — ela
recua meses, até 9 tentativas, e recusaria com **\* Data de entrega fora do limite da permissao \***
—, mas o caminho que a alcança exige que a data de limite da entrega esteja em branco, e a
inclusão e a alteração já a calculam antes de passar por ali.

[?] A procura da permissão só roda quando a data de limite da entrega está em branco; na inclusão
e na alteração essa data já foi calculada (e o fluxo segue para o mapa, RN-10), e a exclusão e a
consulta pulam o trecho do cálculo e chegam com a data em branco, mas desviam para a contagem de
dias. Ou a conferência da permissão vale para outro caminho, ou ficou inalcançável nas quatro
operações. Pergunta ao site.

### RN-10 — A semana de entrega tem de estar coberta por um mapa

A tela procura o **mapa da semana** que contém o período de entrega: o início da entrega não pode
ficar antes do mapa, nem o limite da entrega depois dele. Faltando o mapa, a recusa é
**\* Antes, atualize os mapas ate a data inf. \***, com o cursor no campo próprio da tela e nada
gravado. Sem mapa da semana, não há como distribuir os dias de entrega.

[?] A procura do mapa é alcançada pelo mesmo caminho da RN-09 e depende da mesma condição — a data
de limite da entrega em branco —, que a inclusão e a alteração não satisfazem. Ou a procura do
mapa roda por outro caminho, ou a inclusão e a alteração seguem sem mapa. Pergunta ao site.

### RN-11 — Requisição já calculada não se altera nem se exclui

Se a requisição do órgão, da coordenação e da data de preparo já existir marcada como
**calculada**, a alteração e a exclusão são recusadas com **\* Nao atualize. Requisicao ja
calculada \***, com o cursor de volta ao campo da operação e nada gravado. Para uma requisição
calculada, resta a **consulta**.

### RN-12 — A inclusão é confirmada antes de gravar

Preenchidos os dados e passadas as conferências, a tela pergunta **\* Confirma inclusao do calculo
&lt;S/N&gt; ? \*** e só grava com a resposta afirmativa. Se qualquer dado conferido tiver mudado
entre a pergunta e a resposta, a tela volta ao começo, sem gravar. A alteração e a exclusão são
reabertas pela tela seguinte já com a decisão tomada, e não têm pergunta de confirmação própria.

[?] A tela monta a pergunta de confirmação da inclusão e, logo depois, zera a quantidade de dias
de entrega antes de conferir se os dados continuam os mesmos; a conferência lê justamente a
quantidade de dias, encontra zero onde a tela tinha deixado outro valor e desfaz o passo, voltando
ao começo — em laço. Do lado da alteração e da exclusão, o texto da pergunta existe no programa
mas está dentro de um trecho que a própria decisão anterior torna inalcançável. Ou a confirmação
nunca fecha para nenhuma das operações, ou a leitura do fonte está incompleta. Pergunta ao site.

### RN-13 — A exclusão apaga a requisição e o que ela gerou

Na exclusão, a tela apaga a requisição do órgão, da coordenação e da data de preparo e, em laço,
apaga também os registros derivados daquele período: o mapa dos dias de entrega, os registros de
recesso e as parcelas de pedido e de fornecimento ligadas à requisição. Ao fim, a tela mostra
**Requisicao Excluida**. A exclusão só chega a apagar se a requisição existir e não estiver
calculada (RN-11).

### RN-14 — A consulta não grava nada, e é o único caminho que abre a tela seguinte

Na consulta, a tela **não grava nada**: ela lê a requisição e passa adiante. A consulta é também o
caminho que encaminha para a tela seguinte, com o órgão, a coordenação e a data de preparo da
requisição consultada.

[?] Quando a tela é reaberta por um caminho interno com a operação **consultar** na sessão, ela
recusa a si mesma com **\* Consulta preparo \*** e volta ao começo. Ou o caminho de consulta pela
tela seguinte não existe, ou existe por outro endereço. Pergunta ao site.

### RN-15 — O que a tela entrega à tela seguinte

Ao fim da inclusão e da alteração, a tela passa para a **E051T** a requisição que acabou de
gravar: o órgão, a coordenação e a data de preparo, mais o mapa da semana e os dias de entrega
que ela mesma montou. A tela seguinte abre em **alteração** por causa disso. Ao fim da exclusão,
a tela também passa para a E051T, que **reabre a E051T em consulta** e devolve o fluxo ao menu
`E050M`. A consulta aberta por esta tela encaminha para a **E051T** com a operação de consulta.

## Cenários BDD

```gherkin
Funcionalidade: Requisição de cálculo do órgão filho SDI (ORGAO FILHO SDI / CORD.REG.ESCOLAR)

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E050T

  Cenário: A tela vem do menu e abre como inclusão
    Dado que cheguei à tela pelo menu, sem operação informada
    Quando a tela abre
    Então a operação é inclusão
    E a tela espera o órgão filho, a coordenação e as datas

  Cenário: Inclusão confirmada grava a requisição e encaminha
    Dado um órgão filho SDI, uma coordenação e uma data de início do preparo válida
    E uma data de início de entrega entre o preparo e 7 dias depois dele, em dia útil autorizado
    E uma quantidade de dias de entrega de 1 a 5
    E que a semana de entrega está coberta por mapa
    Quando confirmo a inclusão
    Então a requisição é gravada com o limite de entrega calculado
    E sou encaminhado à tela E051T com a requisição gravada em alteração

  Cenário: Operação não prevista é recusada
    Dado que informei uma operação diferente de incluir, alterar, excluir ou consultar
    Quando a tela confere a operação
    Então vejo "* Operacao nao disponivel *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Sem permissão para a operação, nada segue
    Dado que não tenho permissão para a operação pedida
    Quando a tela confere a permissão
    Então a operação não segue
    E nada é gravado

  Cenário: Órgão filho em branco é recusado
    Dado que deixei o órgão filho SDI em branco
    Quando a tela confere os dados
    Então vejo "* Informe o orgao *"
    E nada é gravado

  Cenário: Coordenação regional escolar em branco é recusada
    Dado que deixei a coordenação regional escolar em branco
    Quando a tela confere os dados
    Então vejo "* Informe o grupo *"
    E nada é gravado

  Cenário: Data de início do preparo inválida é recusada
    Dado uma data de início do preparo que não é uma data válida
    Quando a tela confere a data
    Então vejo "* Data de inicio de calculo invalida *"
    E nada é gravado

  Cenário: Ano do preparo fora de 1994 a 2099 é recusado
    Dado uma data de início do preparo válida, com o ano antes de 1994 ou depois de 2099
    Quando a tela confere a data
    Então vejo "* Data de inicio de calculo invalida *"
    E nada é gravado

  Cenário: Entrega antes do preparo é recusada
    Dado uma data de início de entrega anterior à data de início do preparo
    Quando a tela confere as datas
    Então vejo "* Data de entrega maior que data da requisicao *"
    E nada é gravado

  Cenário: Mais de 7 dias entre preparo e entrega é recusado
    Dado uma data de início de entrega mais de 7 dias depois da data de início do preparo
    Quando a tela confere as datas
    Então vejo "* Difer.entre preparo e entrega maior que 7 dias *"
    E nada é gravado

  Cenário: Quantidade de dias de entrega em branco é recusada
    Dado que não informei a quantidade de dias de entrega
    Quando a tela confere os dados
    Então vejo "* Informe a quantidade de dias de entrega *"
    E nada é gravado

  Cenário: Quantidade de dias de entrega acima de 5 é recusada
    Dado que informei 6 ou mais dias de entrega
    Quando a tela confere os dados
    Então vejo "* Quantidade maxima de dias de entrega = 5 *"
    E nada é gravado

  Cenário: Entrega começando em sábado é recusada
    Dado uma data de início de entrega que cai em sábado
    Quando a tela confere a data
    Então vejo "* Inicio da entrega nao deve ser um sabado *"
    E nada é gravado

  Cenário: Entrega começando em domingo é recusada
    Dado uma data de início de entrega que cai em domingo
    Quando a tela confere a data
    Então vejo "* Inicio da entrega nao deve ser um domingo *"
    E nada é gravado

  Cenário: Entrega começando em feriado é recusada
    Dado uma data de início de entrega marcada como feriado para a secretaria
    Quando a tela confere a data
    Então vejo "* Inicio da entrega nao deve ser um feriado *"
    E nada é gravado

  Cenário: O limite da entrega é gravado junto com a requisição
    Dado um órgão filho SDI, uma coordenação e uma data de início do preparo válida
    E uma data de início de entrega em dia útil, com 3 dias de entrega
    Quando a tela calcula os dias de entrega
    Então o limite da entrega é o terceiro dia contado, pulando sábados, domingos e feriados
    E esse limite fica gravado na requisição

  Cenário: Semana de entrega fora da permissão cadastrada é recusada
    Dado que nenhuma permissão de entrega cadastrada cobre o período pedido
    Quando a tela procura a permissão
    Então vejo "* Data de entrega fora do limite da permissao *"
    E nada é gravado

  Cenário: Semana de entrega sem mapa é recusada
    Dado que o período de entrega não cabe no mapa da semana da coordenadoria
    Quando a tela procura o mapa
    Então vejo "* Antes, atualize os mapas ate a data inf. *"
    E nada é gravado

  Cenário: Requisição já calculada não se altera nem se exclui
    Dado que a requisição do órgão, da coordenação e da data de preparo já está calculada
    Quando peço alterar ou excluir
    Então vejo "* Nao atualize. Requisicao ja calculada *"
    E nada é gravado

  Cenário: Consulta não grava nada
    Dado que a operação é consultar
    Quando a tela lê a requisição
    Então nada é gravado
    E sou encaminhado à tela E051T com a operação de consulta

  Cenário: Exclusão apaga a requisição e o que ela gerou
    Dado que a requisição existe e não está calculada
    Quando peço excluir
    Então a requisição é apagada
    E o mapa dos dias de entrega, os recessos e as parcelas de pedido e fornecimento daquele período também são apagados
    E vejo "Requisicao Excluida"

  Cenário: Exclusão de requisição inexistente é recusada
    Dado que não existe requisição para o órgão, a coordenação e a data de preparo informados
    Quando peço excluir
    Então vejo "* Requisicao nao cadastrada *"
    E nada é apagado
```
