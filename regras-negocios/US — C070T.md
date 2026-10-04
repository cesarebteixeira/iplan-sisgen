# US — C070T — Manter o cardápio do período

## Estória

Como **servidor de CRE**, quero **manter o cardápio de um período — a validade, a
descrição, as marcas de sobremesa e de fruta e os gêneros que ele oferece, com a
quantidade de cada um —**, para que **a alimentação servida no período use
exatamente os gêneros que a minha coordenação definiu**.

O cardápio de um período não vale pelo código: vale pela lista dos gêneros que ele
oferece e pela quantidade de cada um, dentro de uma validade. É essa lista que a
montagem do cardápio semanal consome; um período registrado sem os gêneros fica sem o
que servir, e quem for montar a semana não tem de onde partir. A tela é também quem
guarda a validade de cada versão do mesmo cardápio — o mesmo código pode ter mais de
uma, e é a data limite que as distingue — e quem impede que uma versão seja desfeita
depois de já estar no planejamento semanal. Quando o novo período repete um cardápio
que já existe, a tela copia os gêneros dele, para que a montagem não seja
redigitada.

## Contexto

Jornada S000M → C000M → C070M → C070T.

Ator: servidor de CRE — mantém, no âmbito do tipo de órgão da sua sessão, o cardápio
de um período: a validade, a descrição, as marcas de sobremesa e de fruta e os
gêneros que ele oferece, com as quantidades.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O C000M e o C070M são menus e não
gravam nada: o contexto que esta tela usa — matrícula, código de acesso, privilégio,
tipo de órgão e coordenação regional — é o que a entrada deixou na sessão. O que os
menus **não** deixam é a operação de manutenção, e é por isso que, entrando pela
jornada, a tela abre em consulta (RN-02).

Quem mantém o cadastro dos gêneros e o dos segmentos são outras telas; as ligações
do cardápio com as refeições são mantidas pela **C076T** — que é também a tela para
onde esta encadeia (RN-16). O cadastro dos cardápios é gravado por esta tela, pela
C073T e pela C076T.

---

## Regras de negócio

### RN-01 — A tela mantém o cardápio de um período e os gêneros que ele oferece

O que a tela mantém são dois cadastros ligados. O **cardápio** é uma **validade**: o
mesmo código de cardápio pode ter várias versões, e cada versão é um registro
identificado pelo tipo de órgão, pelo código do cardápio e pelo dia, o mês e o ano
limite — não existem duas versões iguais. O cardápio tem **19 campos**, entre eles a
descrição, a data de início e a data limite, as marcas de sobremesa e de fruta, as
**quatro letras de semana** e o código do cardápio de sobremesa do período, e o
cadastro tem capacidade para **1.000.000** de registros (capacidade é o máximo
esperado, parâmetro de dimensionamento, não o que está cadastrado).

Os **gêneros do cardápio** dizem o que aquele cardápio, naquele segmento e naquela
validade, oferece: são **13 campos** — o tipo de órgão, o código do cardápio, o
segmento, a subclasse, o gênero, a quantidade, a classe do gênero e o dia, o mês e o
ano de início e de limite do período —, com capacidade para **800.000** registros, e
a chave não admite dois registros para o mesmo par cardápio, segmento, validade,
subclasse e gênero.

A grade da tela tem **12 linhas**, e cada linha traz o **código da subclasse**, o
**código do gênero**, a **descrição do gênero**, a **conversão do gênero** (a
quantidade e o seu código), a **quantidade** do gênero no cardápio e a **situação**
da linha. Fora da grade a tela mostra a descrição do cardápio, o código e a descrição
do segmento, as duas datas da validade, as marcas de sobremesa e de fruta e os três
campos da cópia. Esta tela **não** mantém as quatro letras de semana nem o cardápio
de sobremesa do período: aqui eles apenas passam adiante (RN-16).

### RN-02 — A operação em tela vem de quem abriu a tela; sem operação, a tela abre em consulta

A tela procura a **operação de manutenção** na área de trabalho da sessão. Achando
uma, ela abre nessa operação e repõe em tela o que a área guardou — o cardápio, a
descrição, o segmento e a sua descrição, as duas datas da validade e as marcas de
sobremesa e de fruta, com "Sim" ou "Nao". Não achando — área em branco —, a tela abre
em **consulta**.

Esta tela **não** compara quem a chamou com código de tela nenhum: o modo não vem da
tela de origem, vem da operação que ficou na área de trabalho. E os dois menus desta
jornada não gravam operação nenhuma ali — a área que eles mantêm guarda só a
identificação da tela. Por isso, entrando pela jornada S000M → C000M → C070M → C070T,
a tela abre em consulta: para incluir, alterar ou excluir, a operação tem de ser
informada.

[?] A área de trabalho é limpa **uma única vez por sessão**, na primeira abertura
desta tela; depois disso, cada conferência regrava nela a operação que estava em
tela. Se outra tela da sessão gravar uma operação na mesma posição dessa área, é ela
que decide em que modo a C070T abre. O acervo lido não mostra quem mais escreve ali.
Pergunta ao site.

[?] O que o formulário apresenta no campo da operação e o que decide a abertura são
coisas diferentes: a abertura olha a área de trabalho e **sobrescreve** a operação em
tela com ela — inclusive quando a área está em branco, e aí a operação passa a ser a
consulta. Se o servidor puder digitar a operação nesse campo, o que ele digitar não é
o que decide a abertura. Pergunta ao site.

### RN-03 — A tela só aceita incluir, alterar, excluir e consultar

Se a operação em tela não for uma dessas quatro, a tela recusa com
**\* Operacao nao disponivel \***, devolve o cursor ao campo da operação e **não lê
nem grava nada**. A conferência é feita uma vez, na **primeira linha**, antes de
qualquer leitura do cardápio.

### RN-04 — A consulta é pelo código do cardápio e pela data limite, dentro do tipo de órgão

O servidor informa o **código do cardápio** e o **dia, o mês e o ano limite** da
validade. A tela procura, no cadastro dos cardápios e dentro do **tipo de órgão da
sessão**, a versão registrada para essa combinação. As recusas:

- sem o código do cardápio: **\* Informe o codigo do cardapio \***, com o cursor no
  próprio código;
- com um segmento que não consta do cadastro de segmentos: **\* Segmento nao
  cadastrado \***, com o cursor no segmento;
- sem a data limite: **\* Informe a data limite de validade \***, com o cursor no dia
  limite;
- cardápio que não existe naquele período: **\* Cardapio nao cadastrado \***, com o
  cursor no código do cardápio;
- cardápio que existe no período, mas sem aquele segmento: **\* Segmento nao
  cadastrado neste cardapio \***, com o cursor no segmento.

Achando, aquele passa a ser o cardápio em tela, e a grade é montada com os gêneros
dele, uma linha por gênero, com a descrição e a conversão tiradas do cadastro de
gêneros. Não havendo gênero nenhum, a tela avisa
**\* Cardapio sem generos cadastrados \***, com o cursor no código do cardápio, e
nenhuma linha é preenchida — o aviso é decidido na montagem da **primeira linha** e
não é repetido nas demais.

[?] A leitura que monta a grade usa o recurso de **posicionamento** do dicionário de
dados, com parte da chave ignorada; o efeito exato das marcas de chave não está no
acervo nem no manual. Se ela posiciona no primeiro gênero do cardápio e caminha para
os seguintes, o comportamento é o descrito; se exigisse a chave exata, a grade sairia
vazia. Pergunta ao site.

### RN-05 — A alteração e a exclusão exigem que o cardápio já esteja em tela

A **alteração** só segue quando o código do cardápio e o segmento informados são os
mesmos que a área de trabalho guardou — isto é, os do cardápio já consultado. Sendo
outros, a tela recusa **\* Consulte o cardapio antes da atualizacao \*** e devolve o
cursor ao campo da operação. A **exclusão** exige, além dos dois, o **dia, o mês e o
ano limite** iguais aos do cardápio em tela; sendo outros, recusa
**\* Consulte o cardapio antes da exclusao \***, com o cursor no campo da operação.
Nos dois caminhos nada é conferido nem gravado.

### RN-06 — O segmento tem de estar cadastrado e a descrição do cardápio é obrigatória

Na inclusão e na alteração, a **descrição do cardápio** é obrigatória: em branco, a
tela recusa **\* Informe a descricao do cardapio \*** e devolve o cursor ao campo da
descrição. E o **segmento** informado tem de constar do cadastro de segmentos, no
tipo de órgão da sessão; não constando, a recusa é
**\* Segmento nao cadastrado \***, com o cursor no campo do segmento. A conferência
do segmento acontece também na consulta.

### RN-07 — A validade: datas válidas, início não posterior ao limite, e sem invadir outro período do mesmo cardápio

As duas datas passam pelo calendário do sistema: data que não existe é recusada com
**\* Data inicial da validade invalida \*** ou
**\* Data final da validade invalida \***, conforme a data, com o cursor na data
recusada. O ano tem de estar entre **1994 e 2099**. A data de início não pode ser
posterior à data limite: sendo, a tela recusa
**\* Data inicial maior que data final \***, com o cursor na data de início.

Depois disso, a tela confere o **período** contra as outras versões do **mesmo
cardápio**: duas versões não podem se sobrepor. A conferência olha as versões cujo
dia limite é o **anterior** e o **seguinte** ao limite informado, dentro do mesmo mês
e ano, e recusa com **\* Cardapio ja cadastrado neste intervalo \*** — com o cursor
no dia limite, ou na data de início, conforme o lado em que a sobreposição foi
achada. Na alteração, as conferências de data só rodam quando alguma das duas datas
muda em relação ao cardápio em tela.

[?] A conferência de sobreposição só olha as duas versões vizinhas **pelo dia
limite**, no mesmo mês e ano. Uma versão do mesmo cardápio que termine duas semanas
antes do início informado não é consultada, e o período novo pode invadir o dela sem
recusa; o que barra o caso de duas versões com o **mesmo** limite é a chave do
cadastro, que não admite duas versões iguais — e aí a recusa não é a mensagem, é o
erro da gravação. Se a intenção é impedir qualquer sobreposição com uma mensagem, a
conferência não a alcança. Pergunta ao site.

[?] Há uma terceira recusa, **\* <- Dt.inicio para esta validade \***, que mostra na
mensagem a data de início da versão achada; ela é decidida por uma leitura feita com
o **código do cardápio zerado** — o programa nunca preenche esse código nessa
leitura. Se zero não é um código de cardápio válido, a leitura nunca acha nada e a
mensagem não é alcançável. Pergunta ao site.

[?] O cadastro guarda um **terceiro trio de dia, mês e ano** além do início e do
limite, e esta tela o grava **sempre igual à data limite**, na inclusão e na
alteração. O que esse terceiro trio significa não está no acervo lido nem no manual.
Pergunta ao site.

### RN-08 — As marcas de sobremesa e de fruta do cardápio

A marca de **sobremesa** só aceita **S** ou **N**; outra coisa é recusada com
**\* Inf.se card. de sobremesa ou nao com S ou N \*** e o cursor volta à marca.
Marcando **N**, a marca de **fruta** é forçada para **N** — um cardápio sem sobremesa
não tem fruta. Marcando **S**, a marca de fruta passa a ser exigida e só aceita **S**
ou **N**; outra coisa é recusada com
**\* Inf.se fruta ou nao com S ou N \***, com o cursor na marca de fruta. As duas
conferências valem na inclusão e na alteração, e na hora de gravar a marca de fruta é
novamente forçada a **N** quando a de sobremesa não é **S**.

### RN-09 — Na inclusão, o código do cardápio em branco é atribuído pelo sistema

Deixando o **código do cardápio em branco** na inclusão, o sistema atribui o
**próximo código livre do tipo de órgão da sessão** e o coloca em tela no lugar do
branco — é esse código que vai para o cadastro. A atribuição lê o **contador de
códigos do órgão** e soma um; não havendo contador para o órgão, ela varre os
cardápios do órgão e toma o **maior código existente mais um**. Em qualquer dos
casos, enquanto o código já existir no cadastro, ela avança um a um até achar um
livre, e grava no contador o código que usou.

[?] A varredura do maior código começa por um **ano fixo** e o acervo não diz por
quê. Se existirem cardápios com ano limite anterior a esse, os códigos deles não
entram na conta. Pergunta ao site.

[?] O contador do órgão é **gravado antes** de se saber se o cardápio será criado:
uma inclusão que não chega a gerar cardápio nenhum deixa o contador avançado, e o
código atribuído se perde. Pergunta ao site.

[?] Uma inclusão com toda a grade em branco **não cria nada e não avisa nada**: o
cardápio novo só é criado quando alguma linha traz um gênero. Se o servidor pode
querer registrar o cardápio antes de decidir os gêneros, o acervo desta jornada não
responde. Pergunta ao site.

### RN-10 — Na inclusão, a tela pode copiar os gêneros de um cardápio já cadastrado

Na inclusão, o servidor pode apontar um **cardápio de origem** — o código de um
cardápio já cadastrado, o segmento dele e a data limite dele — para não redigitar a
montagem. Os três campos andam juntos: informado o código, o segmento e a data limite
passam a ser obrigatórios, e a tela recusa **\* Informe segmento para copia \*** e
**\* Informe dt.limite para copia \*** enquanto faltar um deles; e a origem tem de
ter gêneros cadastrados, senão a recusa é
**\* Cardapio para copia nao cadastrado \***, com o cursor no código do cardápio de
cópia.

Passando, a tela cria o cardápio informado — se ele ainda não existir — com a
descrição e as datas de tela, e **copia, um a um, os gêneros da origem** para ele, no
segmento da tela e com a validade informada. **Preenchida a cópia, a grade digitada é
ignorada**: entram só os gêneros copiados.

### RN-11 — Cada linha da grade é uma operação sobre um gênero do cardápio

Na **inclusão**, toda linha preenchida com um gênero é uma linha a incluir — a
situação da linha não é olhada. Na **alteração**, é a situação que decide: **I**
inclui o gênero no cardápio, **A** atualiza a quantidade do gênero que já está lá,
**E** exclui o gênero do cardápio; linha com outra situação — inclusive em branco —
**não gera operação nenhuma**. Linha sem gênero informado é ignorada nas duas
operações.

### RN-12 — O gênero tem de estar cadastrado, ativo e conversível, e não pode repetir no cardápio

Numa linha de **inclusão** (inclusão de cardápio, ou alteração com situação **I**), a
tela procura o gênero no cadastro de gêneros pela subclasse, pelo gênero e pela data
limite do período. As recusas:

- gênero que não está cadastrado, ou que está cadastrado **inativo**:
  **\* Genero nao cadastrado \***, com o cursor na subclasse da linha;
- gênero com a **conversão zerada**: **\* Unidade de conversao zerada \***;
- gênero com a **quantidade a fracionar zerada**:
  **\* Quantidade a fracionar zerada \***;
- par de subclasse e gênero que **já está no cardápio**, no mesmo segmento e validade:
  **\* Genero ja cadastrado neste cardapio \***;
- **quantidade em branco**: **\* Informe a Quantidade \*** (na inclusão) ou
  **\* Informe a quantidade \*** (na alteração com situação A), com o cursor na
  quantidade da linha.

Numa linha de alteração com situação **A** ou **E**, o gênero tem de estar no
cardápio; não estando, a recusa é **\* Genero nao cadastrado neste cardapio \***.

### RN-13 — O gênero que já está no planejamento semanal não sai, e o cardápio que fica sem gênero é excluído por inteiro

A **exclusão do cardápio** é recusada quando ele está no **planejamento semanal** do
período, naquele segmento, em qualquer dia da semana e em qualquer coordenação
regional: **\* <- Grupo - Card.no planejamento deste seg. \***, com o código da
coordenação na mensagem. A tela varre o planejamento do período inteiro, dia a dia,
até achar ou acabar.

A **exclusão de um gênero** pela grade (alteração com situação **E**) passa pela
mesma recusa, mas só quando aquele gênero é o **único** do cardápio — é aí que o
cardápio ficaria sem gênero nenhum; havendo dois ou mais, o gênero sai sem
conferência do planejamento.

E o cardápio que fica **sem nenhum gênero** — porque o último gênero saiu, ou porque
o cardápio inteiro foi excluído — tem o **cabeçalho e as ligações com as refeições
excluídos junto**: esta tela não deixa cardápio sem gênero no cadastro.

### RN-14 — A alteração da validade se propaga aos gêneros e às ligações, e toda gravação é auditada

Mudando a **data de início** ou a **data limite** do cardápio, a tela regrava as
novas datas em **todos os gêneros** daquele cardápio e em **todas as ligações dele
com as refeições** do período — é assim que o cardápio inteiro muda de período. O
cabeçalho do cardápio só é gravado quando algo mudou nele: a descrição, a marca de
sobremesa, a de fruta ou as datas.

Toda gravação e toda exclusão desta tela deixa um registro na **auditoria geral**: a
origem, a operação, o registro antes e o registro depois, a matrícula, a estação, o
tipo de órgão, a coordenação regional e a sessão. As mudanças de campo do cardápio —
descrição, sobremesa, fruta, data de início e data limite —, a mudança de quantidade
do gênero e as inclusões deixam **também** um registro na **auditoria de campos**,
com o campo alterado e as duas imagens.

### RN-15 — A consulta não grava nada, e quatro dos dez cadastros que a tela enxerga são só lidos

A consulta termina antes de qualquer gravação: nenhum cardápio, nenhum gênero,
nenhuma ligação com as refeições e nenhum registro de auditoria. As rotinas de
gravação, de exclusão e de travamento existem declaradas para os **dez cadastros**
que a tela enxerga, mas só são executadas as do **cardápio**, das **ligações com as
refeições**, dos **gêneros do cardápio**, do **contador de códigos** e das **duas
auditorias**. O cadastro de telas, o cadastro de gêneros, o cadastro de segmentos e o
**planejamento semanal** são apenas lidos — declarar não é executar.

### RN-16 — A tela encadeia na C076T quando a marca de nova referência está posta

Quando a **marca de nova referência** vem posta, a tela **não mantém nada**: ela
procura o cardápio do período — pelo tipo de órgão, pelo código do cardápio e pelas
três partes da data limite — e, não achando, recusa **\* Cardapio nao cadastrado \***,
com o cursor no código do cardápio. Achando, ela entrega à tela seguinte:

- o **registro**: o cardápio achado no cadastro — código, descrição, as datas de
  início e de limite **do registro**, as quatro letras de semana e as marcas de
  sobremesa e de fruta;
- a **operação**: a alteração;
- e a **identificação da tela de origem**, que faz a C076T recomeçar a lista de
  refeições do zero e abrir já com o cardápio carregado.

A passagem é direta, **sem menu**: a C076T abre em **alteração**, com o cardápio do
período em tela, e é lá que as refeições e as semanas do cardápio são mantidas.

[?] O que marca a "nova referência" não está no acervo: o campo só é comparado com
**S**, e a própria tela nunca o escreve. Nenhum rótulo da ficha do programa
corresponde a ele. Se é o formulário que o preenche, ou se é resto do gerador, o
acervo não diz. Pergunta ao site.

[?] As duas marcas de sobremesa e de fruta ficam **trocadas** na passagem: esta tela
e a C076T declaram esses dois campos em **ordem inversa** na área de trabalho, e a
C076T lê a marca de sobremesa da posição em que esta tela grava a de fruta — de modo
que um cardápio com fruta pode ser lido pela C076T como um cardápio de sobremesa, e a
C076T pode recusar apontar a sobremesa do período por causa disso. O acervo não
responde. Pergunta ao site.

### RN-17 — A digitação é editada, o resultado anterior é apagado, e a tela mostra a data do sistema e o tipo de órgão

Os **16 campos** informados — o código do cardápio, o código do segmento, o dia, o
mês e o ano de início, o dia, o mês e o ano limite, o código do segmento de cópia, o
dia, o mês e o ano limite da cópia, o código da subclasse, o código do gênero e a
quantidade — passam por **edição numérica** antes de qualquer leitura: campo em branco
é tratado como zero e o que não for número é recusado, com o cursor de volta ao campo
recusado (a rotina que devolve o cursor conhece os **16**).

Antes de cada conferência, a tela **apaga o resultado anterior**: a descrição do tipo
de órgão, a data do sistema, a descrição do segmento, o texto da marca de sobremesa,
o da fruta, a descrição do gênero e a conversão. Uma consulta recusada, portanto, não
deixa em tela o resultado da anterior.

Fora da grade a tela exibe a **data do sistema** e a **descrição do tipo de órgão** da
sessão.

[?] Nem a data do sistema nem a descrição do tipo de órgão são preenchidas por um
caminho que o acervo mostre: a tela as copia de áreas de trabalho do módulo, e a
entrada guarda os dois valores em áreas da sessão. Se o ambiente transporta os valores
de uma área para a outra — e de onde vem a data do sistema —, o acervo não diz; se
não transportar, os dois campos saem em branco. Pergunta ao site.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não
está nos fontes desta jornada: a rotina que faz a edição numérica não faz parte do
acervo lido; a tela só devolve o cursor. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter o cardápio de um período e os gêneros que ele oferece

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C070T

  Cenário: A tela abre em consulta
    Quando abro a tela C070T
    Então a operação de manutenção em tela é a consulta

  Cenário: Consulta do cardápio de um período
    Dado que existe um cardápio com o código e a data limite que vou informar, no meu tipo de órgão
    Quando envio a consulta com o código do cardápio e a data limite
    Então vejo a descrição do cardápio e a descrição do segmento
    E vejo os gêneros daquele cardápio, um por linha, com a descrição e a conversão de cada um
    E nada é gravado

  Cenário: Consulta sem o código do cardápio
    Quando envio a consulta deixando o código do cardápio em branco
    Então vejo a mensagem "* Informe o codigo do cardapio *"
    E o cursor volta ao campo do código do cardápio

  Cenário: Consulta com segmento que não está cadastrado
    Dado que informei um código de segmento que não consta do cadastro
    Quando envio a consulta
    Então vejo a mensagem "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento

  Cenário: Consulta sem a data limite
    Quando envio a consulta deixando o dia, o mês e o ano limite em branco
    Então vejo a mensagem "* Informe a data limite de validade *"
    E o cursor volta ao campo do dia limite

  Cenário: Consulta de cardápio que não existe no período
    Dado que não existe cardápio com o código e a data limite que informei
    Quando envio a consulta
    Então vejo a mensagem "* Cardapio nao cadastrado *"
    E o cursor volta ao campo do código do cardápio
    E nenhuma linha é listada

  Cenário: Consulta de um segmento que o cardápio não tem
    Dado que o cardápio existe no período, mas não naquele segmento
    Quando envio a consulta
    Então vejo a mensagem "* Segmento nao cadastrado neste cardapio *"
    E o cursor volta ao campo do segmento

  Cenário: Consulta de cardápio sem gêneros
    Dado que o cardápio existe no período, mas não tem gênero nenhum
    Quando envio a consulta
    Então vejo a mensagem "* Cardapio sem generos cadastrados *"
    E o cursor volta ao campo do código do cardápio
    E nenhuma linha é preenchida

  Cenário: Operação de manutenção indisponível
    Quando informo uma operação que não é incluir, alterar, excluir nem consultar
    Então vejo a mensagem "* Operacao nao disponivel *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: Alteração sem consultar antes
    Dado que o cardápio informado não é o que está em tela
    Quando envio a alteração
    Então vejo a mensagem "* Consulte o cardapio antes da atualizacao *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Exclusão sem consultar antes
    Dado que o período informado não é o do cardápio que está em tela
    Quando envio a exclusão
    Então vejo a mensagem "* Consulte o cardapio antes da exclusao *"
    E o cursor volta ao campo da operação
    E o cardápio continua cadastrado

  Cenário: Inclusão ou alteração sem a descrição do cardápio
    Quando envio a manutenção deixando a descrição do cardápio em branco
    Então vejo a mensagem "* Informe a descricao do cardapio *"
    E o cursor volta ao campo da descrição
    E nada é gravado

  Cenário: Data de início da validade inválida
    Quando informo uma data de início que não existe no calendário
    Então vejo a mensagem "* Data inicial da validade invalida *"
    E o cursor volta ao dia de início

  Cenário: Data limite da validade inválida
    Quando informo uma data limite que não existe no calendário
    Então vejo a mensagem "* Data final da validade invalida *"
    E o cursor volta ao dia limite

  Cenário: Data de início posterior à data limite
    Dado que informei uma data de início maior que a data limite
    Quando envio a manutenção
    Então vejo a mensagem "* Data inicial maior que data final *"
    E o cursor volta ao dia de início
    E nada é gravado

  Cenário: Validade que invade outro período do mesmo cardápio
    Dado que o cardápio já tem uma versão no período vizinho ao que informei
    Quando envio a inclusão
    Então vejo a mensagem "* Cardapio ja cadastrado neste intervalo *"
    E o cursor volta ao campo do dia limite
    E nada é gravado

  Cenário: Marca de sobremesa diferente de S e de N
    Quando informo outra coisa na marca de sobremesa
    Então vejo a mensagem "* Inf.se card. de sobremesa ou nao com S ou N *"
    E o cursor volta à marca de sobremesa
    E nada é gravado

  Cenário: Marca de fruta diferente de S e de N
    Dado que marquei o cardápio como de sobremesa
    Quando informo outra coisa na marca de fruta
    Então vejo a mensagem "* Inf.se fruta ou nao com S ou N *"
    E o cursor volta à marca de fruta

  Cenário: Cardápio sem sobremesa não tem fruta
    Dado que marquei o cardápio como sem sobremesa
    E que marquei a fruta
    Quando envio a manutenção
    Então a marca de fruta é gravada como N

  Cenário: Inclusão de cardápio com o código atribuído pelo sistema
    Dado que deixei o código do cardápio em branco
    E que informei o segmento, a descrição, a validade e ao menos um gênero
    Quando envio a inclusão
    Então o sistema atribui o próximo código livre do meu tipo de órgão
    E o código atribuído aparece em tela
    E o cardápio e os gêneros passam a estar cadastrados no período

  Cenário: Inclusão de cardápio copiando os gêneros de outro
    Dado que informei o código, o segmento e a data limite de um cardápio que já tem gêneros
    Quando envio a inclusão do cardápio novo
    Então o cardápio novo é criado com a descrição e a validade informadas
    E ele passa a ter os mesmos gêneros da origem, no segmento e na validade informados

  Cenário: Cópia sem o segmento de origem
    Dado que informei o código do cardápio de cópia e deixei o segmento de cópia em branco
    Quando envio a inclusão
    Então vejo a mensagem "* Informe segmento para copia *"
    E o cursor volta ao campo do segmento de cópia
    E nada é gravado

  Cenário: Cópia sem a data limite de origem
    Dado que informei o código e o segmento de cópia e deixei a data limite de cópia em branco
    Quando envio a inclusão
    Então vejo a mensagem "* Informe dt.limite para copia *"
    E o cursor volta ao dia limite de cópia
    E nada é gravado

  Cenário: Cópia de cardápio que não tem gêneros
    Dado que o cardápio de origem informado não tem gênero nenhum
    Quando envio a inclusão
    Então vejo a mensagem "* Cardapio para copia nao cadastrado *"
    E o cursor volta ao campo do código do cardápio de cópia
    E nada é gravado

  Cenário: Inclusão de um gênero no cardápio
    Dado que o cardápio está em tela
    E que o gênero informado está cadastrado e ativo, com conversão
    E que ele ainda não está nesse cardápio
    Quando informo a quantidade e envio a inclusão
    Então aquele gênero passa a fazer parte do cardápio, com a quantidade informada

  Cenário: Linha sem gênero ou com situação desconhecida não gera operação
    Dado que deixei uma linha em branco e outra com uma situação desconhecida
    Quando envio a alteração
    Então nenhuma das duas gera operação

  Cenário: Alteração da quantidade de um gênero
    Dado que o gênero já está no cardápio em tela
    Quando informo a situação A e a nova quantidade
    Então o gênero passa a ter a quantidade informada
    E a alteração é registrada nas duas auditorias

  Cenário: Inclusão de gênero que já está no cardápio
    Dado que o gênero informado já está nesse cardápio
    Quando envio a inclusão
    Então vejo a mensagem "* Genero ja cadastrado neste cardapio *"
    E o cursor volta ao campo da subclasse daquela linha
    E nada é gravado

  Cenário: Inclusão de gênero que não está cadastrado
    Dado que o código de gênero informado não consta do cadastro de gêneros
    Quando envio a inclusão
    Então vejo a mensagem "* Genero nao cadastrado *"
    E o cursor volta ao campo da subclasse daquela linha

  Cenário: Gênero com a conversão zerada
    Dado que o gênero informado está cadastrado com a conversão zerada
    Quando envio a inclusão
    Então vejo a mensagem "* Unidade de conversao zerada *"
    E nada é gravado

  Cenário: Gênero com a quantidade a fracionar zerada
    Dado que o gênero informado está cadastrado com a quantidade a fracionar zerada
    Quando envio a inclusão
    Então vejo a mensagem "* Quantidade a fracionar zerada *"
    E nada é gravado

  Cenário: Linha de operação sem a quantidade
    Dado que informei o gênero numa linha e deixei a quantidade em branco
    Quando envio a manutenção
    Então vejo a mensagem "* Informe a Quantidade *"
    E o cursor volta ao campo da quantidade daquela linha
    E nada é gravado

  Cenário: Alteração de gênero que não está no cardápio
    Dado que o gênero informado não faz parte do cardápio em tela
    Quando envio a alteração com a situação A ou com a situação E
    Então vejo a mensagem "* Genero nao cadastrado neste cardapio *"
    E o cursor volta ao campo da subclasse daquela linha

  Cenário: Exclusão de um gênero do cardápio
    Dado que o cardápio está em tela e tem mais de um gênero
    E que o gênero informado está nele
    Quando informo a situação E e envio a alteração
    Então aquele gênero deixa o cardápio
    E o cardápio continua cadastrado

  Cenário: Exclusão do último gênero apaga o cardápio
    Dado que o cardápio em tela tem um único gênero
    E que esse cardápio não está no planejamento semanal
    Quando informo a situação E e envio a alteração
    Então o gênero deixa o cardápio
    E o cardápio e as ligações dele com as refeições são excluídos junto

  Cenário: Exclusão de cardápio que está no planejamento semanal
    Dado que o cardápio em tela está no planejamento semanal do período, naquele segmento
    Quando envio a exclusão
    Então vejo a mensagem "* <- Grupo - Card.no planejamento deste seg. *"
    E o cursor volta ao campo do código do cardápio
    E o cardápio continua cadastrado

  Cenário: Exclusão do último gênero que está no planejamento semanal
    Dado que o cardápio em tela tem um único gênero
    E que o cardápio está no planejamento semanal daquele segmento
    Quando informo a situação E e envio a alteração
    Então vejo a mensagem "* <- Grupo - Card.no planejamento deste seg. *"
    E o gênero continua no cardápio

  Cenário: Exclusão do cardápio de um período
    Dado que o cardápio está em tela e não está no planejamento semanal
    Quando envio a exclusão
    Então o cardápio deixa de estar cadastrado naquele período
    E os gêneros dele são excluídos junto
    E as ligações dele com as refeições são excluídas junto

  Cenário: A alteração da validade muda o período dos gêneros e das ligações
    Dado que o cardápio em tela tem gêneros e ligações com as refeições
    Quando altero a data limite e envio a alteração
    Então os gêneros do cardápio passam a ter a nova data limite
    E as ligações dele com as refeições passam a ter a nova data limite

  Cenário: Cada gravação é registrada nas auditorias
    Dado que confirmo uma inclusão, uma alteração ou uma exclusão
    Então a auditoria geral guarda a origem, a operação e os registros anterior e posterior
    E a auditoria de campos guarda o campo alterado e os registros anterior e posterior

  Cenário: A consulta não grava nada
    Dado que estou em modo de consulta
    Quando envio a consulta
    Então nenhum cardápio e nenhum gênero é gravado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: A tela passa para a C076T quando a marca de nova referência está posta
    Dado que o cardápio do período existe
    E que a marca de nova referência veio posta
    Quando envio a tela
    Então a C076T abre com o cardápio do período em tela
    E abre em alteração
    E nada é gravado por esta tela

  Cenário: Nova referência sem o cardápio no período
    Dado que a marca de nova referência veio posta
    E que não existe cardápio com o código e a data limite informados
    Quando envio a tela
    Então vejo a mensagem "* Cardapio nao cadastrado *"
    E o cursor volta ao campo do código do cardápio

  Cenário: Digitação não numérica é recusada
    Dado que digitei uma letra num campo numérico
    Quando envio a tela
    Então a tela recusa a digitação
    E a manutenção não segue
    E o cursor volta ao campo recusado

  Cenário: O resultado anterior é apagado antes da conferência
    Dado que a apresentação anterior mostrou um cardápio com os seus gêneros
    Quando envio uma consulta que é recusada
    Então a descrição do cardápio, a do segmento e os gêneros não ficam em tela

  Cenário: A data do sistema e o tipo de órgão da sessão
    Dado que entrei no sistema
    Quando abro a tela C070T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão
```
