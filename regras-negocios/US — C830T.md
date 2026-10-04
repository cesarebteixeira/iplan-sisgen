# US — C830T — Estimar os comensais do período por coordenação, segmento e refeição

## Estória

Como **servidor da coordenação regional escolar que responde pela estimativa da
merenda**, quero **registrar, para cada coordenação, segmento e período, a média de
comensais e o total de unidades de cada refeição**, para que **o cálculo do período saiba
quantas refeições servir e a execução da merenda não dependa de quem cadastrou o
cardápio**.

A estimativa é o que transforma um período de merenda em número: sem ela o cálculo
daquele período não fecha — a rotina de cálculo recusa o período cuja média de comensais
não está cadastrada. É esta tela que cria, mantém e apaga essas médias, refeição a
refeição; é ela também que repete em outro período as médias de um período já cadastrado
e que apaga as médias de um período inteiro quando ele foi cadastrado errado.

## Contexto

Jornada S000M → C000M → C800M → C840M → C830T.
Ator: servidor de CRE — registra e mantém a média de comensais e o total de unidades de
cada refeição, por coordenação regional escolar, segmento e período.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os três menus do caminho (`C000M`, `C800M` e `C840M`)
só encaminham: não gravam nada e não decidem nada sobre esta tela — a opção de manutenção
vem do que a própria tela guardou na sessão (RN-02). Esta tela é **terminal**: não
encadeia para nenhuma outra e não passa registro nem operação adiante (RN-19).

Da sessão, esta tela usa o **tipo de órgão** da secretaria, que faz parte da identidade
da média e abre toda leitura de cadastro que ela faz; a **coordenação regional escolar do
vínculo**, que limita a coordenação que o servidor pode consultar (RN-04); e a
**matrícula**, o **código de acesso** e o **privilégio** do vínculo, que entram na
conferência de permissão e na trilha de auditoria. O **órgão filho** que a entrada
carrega não é usado aqui. O que a entrada deixa e esta tela aproveita está no anexo de
evidências, em **Regras que se revelaram da entrada**.

Os cadastros de que a tela se serve — a coordenação regional escolar, o segmento, a
refeição, o vínculo entre o segmento e a refeição, o cardápio do período e o resultado do
cálculo daquele período — são de outras telas e aqui só são lidos.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O que a tela mantém

A tela mantém a **média de comensais** de cada **refeição**, por **coordenação regional
escolar** (2 dígitos — as mensagens da tela a chamam de grupo), **segmento** (2 dígitos) e
**período** (data de início e data limite, cada uma com dia, mês e ano), no **tipo de
órgão** da sessão. Cada registro guarda **13 informações**: a coordenação, o segmento, a
refeição, o dia, o mês e o ano de início do período, o dia, o mês e o ano limite, a
**média de comensais**, o **total de unidades**, a **marca de situação** do período e o
tipo de órgão. Um registro é identificado pelo **tipo de órgão**, pela **coordenação**,
pelo **segmento**, pela **refeição** e pela **data limite** — o dia, o mês e o ano limite;
a data de início é guardada junto, mas **não distingue um registro do outro**. O cadastro
comporta **100.000 registros** — capacidade é o máximo esperado declarado no dicionário de
dados, parâmetro de dimensionamento, não o volume cadastrado.

A **grade** mostra **11 linhas** por vez, e cada linha tem **3 campos**: o **código da
refeição** (2 dígitos), a **média** (7 dígitos) e o **total de unidades** (5 dígitos). Ao
lado da grade a tela exibe o nome do tipo de órgão, a data do sistema, a descrição do
segmento, a **situação do período** (RN-06) e, em cada linha, a descrição da refeição.

Fora da grade, a tela tem **24 campos de entrada**: 5 que identificam a mensagem (a tela,
a origem, o número da transação, a data de entrada e o mês de referência), a **opção de
manutenção**, o **código da tela seguinte** e **17 campos de negócio** — a coordenação, as
três partes de cada uma das duas datas, o segmento, o indicador de novo segmento e as três
partes e o código de segmento do **período de cópia** e do **período de exclusão**. Esses
dois últimos grupos não têm rótulo de negócio: a tela os mostra pelas abreviaturas
internas dos campos.

### RN-02 — A tela abre em consulta, e só ALT e CON passam

A opção de manutenção não vem de quem abriu a tela: ela vem do que a própria tela guardou
na sessão e, quando não há nada guardado, a tela abre em **consulta** — e sem coordenação
nenhuma, com a situação do período mostrada como um traço e nenhuma linha da média
preenchida. Confirmada a transação, a tela aceita apenas **alteração** ou **consulta**;
qualquer outra opção é recusada com **\* Operacao nao disponivel \***, o cursor volta ao
campo da opção e nada é lido nem gravado.

Todas as operações desta tela — incluir, alterar ou apagar a média de uma refeição, copiar
um período, apagar as médias de um período e passar para o segmento seguinte — são feitas
no modo de **alteração**. No modo de **consulta** nada é gravado (RN-08).

[?] A conferência procura os códigos de alteração e de consulta que o sistema usa nos seus
próprios mnemônicos, e a mensagem manda usar "ALT" e "CON". Ou o terminal traduz o que o
servidor digita antes de enviar, ou a mensagem está desalinhada da conferência. Não
concluo qual dos dois; a mesma forma já foi medida em outras telas do acervo. Pergunta ao
site.

### RN-03 — Os campos numéricos passam pela conferência de número antes de tudo

Antes de qualquer conferência de negócio, **19 campos** passam pela conferência de
número: a coordenação, o dia, o mês e o ano de início do período, o dia, o mês e o ano
limite, o segmento, a data de cópia (dia, mês e ano), o segmento de cópia, a data de
exclusão (dia, mês e ano), o segmento de exclusão, a refeição, a média e o total de
unidades. Campo em branco vira **zero**; o que não for número é recusado, e nada mais é
conferido nem gravado por causa desse campo.

[?] O campo recusado devolve o cursor a si mesmo apenas para **15** desses campos: o dia,
o mês e o ano de início do período e a refeição não têm posição de cursor definida. Se o
servidor deveria ser levado de volta a esses quatro campos, é pergunta ao site.

### RN-04 — A coordenação é obrigatória, tem que ser a do servidor e estar cadastrada

São três peneiras, nesta ordem. A coordenação **informada** não pode vir em branco — em
branco a recusa é **\* Informe o grupo \***, com o cursor no campo. Na **consulta**, se o
vínculo do servidor traz uma coordenação regional escolar, a coordenação informada tem que
ser a mesma dele — senão a recusa é **\* Usuario sem acesso a este grupo \***, com o cursor
no campo. E a coordenação tem que estar **cadastrada** — senão a recusa é
**\* Grupo nao cadastrado \***, com o cursor no campo.

[?] A conferência é contra a coordenação que a entrada deixou, e só alcança quem entrou
**com** coordenação: um servidor que entrou sem coordenação na sessão consulta o período
de qualquer coordenação. Se a intenção era que todo servidor consultasse só a própria, a
guarda não cobre quem entrou sem nenhuma. Pergunta ao site.

### RN-05 — Consultar exige data limite, segmento e cardápio no período

Na consulta, os dados informados passam por três peneiras, nesta ordem. A **data limite do
período** tem que estar preenchida nas três partes — senão **\* Informe a data limite de
validade \***, com o cursor no campo. O **segmento** tem que estar cadastrado — e em branco
também é aceito, caso em que a tela adota o **primeiro segmento cadastrado**; quando o
segmento informado não existe, a recusa é **\* Segmento nao cadastrado \***, com o cursor
no campo. E o **período tem que ter pelo menos um cardápio cadastrado** — senão
**\* Nao existem cardapios neste periodo \***, com o cursor na data limite. Cada recusa
para a consulta, e nada é gravado.

Passando por tudo, a consulta passa a valer como o período em foco, e a **data de início
exibida passa a ser a do cardápio** daquele período, não a que foi digitada. Se os dados
informados forem exatamente os da consulta anterior da sessão, a tela não refaz as
peneiras: é a mesma consulta, e ela reaproveita o que já leu.

### RN-06 — A situação do período aparece na tela

A tela exibe a situação do período da estimativa: **FECHADO** quando o cadastro do
cardápio daquele período está fechado, e um traço (**---------**) quando não está.

### RN-07 — Sem nenhuma refeição para aquela coordenação e aquele segmento, a tela avisa e não monta a grade

Quando, ao montar a primeira linha da grade, a tela não encontra nenhuma refeição com
média registrada nem prevista para aquela coordenação e aquele segmento, ela avisa
**\* Grupo sem comensais cadastrados neste seg \*** e não monta as linhas da grade.

### RN-08 — Consultar não grava nada

Na consulta a tela só lê e exibe: o cadastro da coordenação, o do segmento, o da refeição,
o do vínculo entre o segmento e a refeição, o do cardápio do período e o da média,
montando a grade a partir deles. A passagem que grava é desviada de propósito quando a
opção não é alteração: nenhuma gravação e nenhuma exclusão são executadas.

### RN-09 — A tela reabre com a última consulta

A tela guarda na sessão a coordenação, o segmento, o período e a opção de manutenção da
última transação e, ao ser reaberta, mostra o que guardou — inclusive a opção da última
vez e a situação do período daquela consulta. É por isso que a segunda abertura da tela
não é igual à primeira.

### RN-10 — A alteração exige ter consultado antes

Antes de qualquer gravação, o sistema exige que a coordenação, o segmento e a data limite
informados sejam exatamente os da última consulta da sessão. Quem não consultou antes vê
**\* Consulte antes de atualizar \***, com o cursor no campo da coordenação, e nada é lido
nem gravado. A **data de início do período não entra nessa conferência**: ela pode ser
corrigida na alteração, ainda que a consulta a reponha com a do cardápio (RN-05).

### RN-11 — O pedido de novo segmento

Há na tela um indicador de **novo segmento**. Com ele ligado, a consulta exige que a
coordenação informada seja a mesma que já está em foco — senão a recusa é
**\* Consulte antes de solicitar novo seg \***, com o cursor no campo da coordenação.
Passando, a tela passa a trabalhar no **segmento seguinte** ao informado: procura o
cadastro desse segmento seguinte e põe o seu código e a sua descrição no lugar do segmento
em foco; não existindo esse seguinte, adota o **primeiro segmento** cadastrado. Nenhuma
média é gravada por esse caminho.

[?] O que este indicador significa em negócio, o fonte não diz: ele não está entre os
campos que a tela trata como número, não tem rótulo no programa — o rótulo vive na máscara
da tela, que não está no lote — e o programa nunca o preenche, só o lê. Se ninguém o
preenche, o recurso é inalcançável. Pergunta ao site.

### RN-12 — Período fechado não se altera

Antes de gravar, o sistema procura a média daquela coordenação, daquele segmento e daquele
período e, se a encontrar marcada como **fechada**, recusa a alteração com
**\* Cadastro fechado para este periodo \***, com o cursor no campo da data limite. O
fechamento não se faz por esta tela.

### RN-13 — A média e o total de unidades

Numa alteração, cada linha da grade é conferida: com a **média zerada**, o **total de
unidades é zerado** pelo próprio sistema, sem aviso; com a **média preenchida**, o
**total de unidades é obrigatório** — zerado, a recusa é **\* Informe total de unidades \***,
com o cursor no total; e a **média não pode ser menor que o total de unidades** — sendo, a
recusa é **\* Media menor que total de unidades \***, com o cursor na média. Essas duas
conferências **não acontecem** quando o mesmo pedido traz cópia ou exclusão de período
(RN-15 e RN-16).

[?] O corpus mostra o "total de unidades" nas mensagens da tela e na chave do cadastro,
mas não diz o que a unidade é (refeição? porção?), nem por que a média não pode ser menor
que esse total. Pergunta ao site.

### RN-14 — O que a alteração faz com cada refeição

Confirmada a alteração, cada linha da grade é tratada pela média que traz:

- refeição **sem média no período** e média informada — a média é **incluída**;
- refeição **com média no período** e média **diferente** da gravada — a média é
  **alterada**;
- refeição **com média no período** e média **igual** à gravada — nada é gravado;
- refeição **com média no período** e média **zerada** — o registro daquela refeição é
  **apagado do período**;
- refeição **sem média no período** e média zerada — nada é gravado;
- linha **sem o código da refeição** — nada é gravado.

Não há operação de exclusão de uma linha: para tirar uma refeição do período, zera-se a
média dela.

### RN-15 — Copiar um período

Informado o **período de cópia** (a origem), o sistema copia para o período em foco as
médias daquele período, uma linha por refeição e por segmento, com a **data de início
informada** para o período em foco. O **segmento de origem** decide o alcance: **99** traz
todos os segmentos da origem; um segmento traz só aquele — e em branco a origem não é
encontrada, de modo que copiar tudo exige o 99.

A cópia só acontece para um período que **ainda não tem média nenhuma**: se o período em
foco já tem média, a recusa é **\* Nao copiar. Periodo ja cadastrado \***, com o cursor no
período de cópia; e se não existe média no período de origem, a recusa é
**\* Periodo para copia nao cadastrado \***, com o cursor no período de cópia. As linhas
copiadas nascem **abertas**: a marca de período fechado não é copiada.

### RN-16 — Excluir um período

Com o **período de exclusão** preenchido, o sistema apaga as médias daquele período, uma a
uma, deixando o rastro de cada uma. O **segmento de exclusão** decide o alcance: **99**
apaga as médias de todos os segmentos do período; um segmento apaga só as daquele.

A exclusão exige: o **ano** do período de exclusão **igual ao ano limite** do período
informado — diferente, a recusa é **\* Consulte antes de excluir \***, com o cursor no
período de exclusão; o **segmento** informado — em branco, a recusa é
**\* Informe segmento ou 99 para todos \***, com o cursor no segmento de exclusão; o
segmento de exclusão **igual ao segmento em foco** quando não é 99 — diferente, a recusa é
**\* Consulte antes de excluir \***; que o período **não tenha sido calculado** —
calculado, a recusa é **\* Nao exclua. Periodo ja calculado \***, com o cursor no período
de exclusão; e que o período **tenha média** — sem nenhuma, a recusa é
**\* Nao existem registros para este periodo \***, também com o cursor no período de
exclusão.

[?] A conferência do período de exclusão compara **três vezes o ano** e não confere o mês
nem o dia: um período com outro dia e outro mês no mesmo ano passa pela guarda e vai
buscar as médias daquele outro período. Ou a comparação saiu repetida no gerador, ou a
intenção era exigir a data inteira. Pergunta ao site.

### RN-17 — As operações de período têm precedência

Quando o mesmo pedido traz mais de uma operação de período, só a primeira acontece, nesta
ordem: **passar para o segmento seguinte**, depois **excluir as médias do período** e
depois **copiar**. Com a exclusão pedida, a cópia **não é executada** — e nem chega a ser
conferida. Nenhuma dessas operações se combina com a gravação refeição a refeição: pedida
a cópia ou a exclusão, a grade daquele pedido não é gravada linha a linha.

### RN-18 — A tela seguinte preenchida abandona a manutenção

Se a mensagem chegar com o **código da tela seguinte** preenchido, a transação é abandonada
antes de qualquer conferência de negócio: nada é lido, nada é gravado e nenhuma mensagem é
mostrada.

[?] O que preenche o código da tela seguinte nesta tela não está no acervo: o programa não
o atribui em nenhum ponto, só o repassa à rotina de rota, e a máscara que o traria não está
no lote. Se ele puder chegar preenchido, a alteração passa sem as conferências de negócio;
se não puder, é campo morto. Pergunta ao site.

### RN-19 — A tela é o fim da jornada

A tela não encadeia para nenhuma outra: não passa registro nem operação adiante, e o que
ela deixa para as próximas consultas é o que guardou na sessão (RN-09).

### RN-20 — Toda gravação deixa rastro na auditoria

Cada média **incluída**, **alterada** ou **apagada** — e cada linha copiada ou apagada
pelas operações de período — monta um registro na trilha de auditoria com o tipo de órgão,
a coordenação, o cadastro de origem, a operação (inclusão, alteração ou exclusão), a
matrícula, a estação, a data, a hora, o número do processo e os valores antes e depois. Na
inclusão e na cópia o valor anterior vai em branco; na exclusão, o posterior.

### RN-21 — A tela grava a média e a auditoria, e só lê os outros sete cadastros

Para cada um dos **9 cadastros** que a tela enxerga, o gerador declara uma rotina de
gravação e uma de exclusão — **18 rotinas** —, mas declarar não é usar: a tela executa
**3** (cria e grava a média, apaga a média e grava a auditoria). Os outros **7 cadastros**
ela apenas lê. O que o programa não conferir em cada leitura, o banco barra pelas suas
chaves.

### RN-22 — Falha de banco interrompe a transação

Todo acesso a dados testa o erro do banco: o erro de gravação vira uma ação de erro, e o de
leitura e o de exclusão, outra. A transação para ali, sem completar o resto.

---

## Cenários BDD

```gherkin
Funcionalidade: Estimar os comensais do período por coordenação, segmento e refeição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C830T

  Cenário: RN-01, RN-05 e RN-08 — consultar a média de um período
    Dado que estou na tela C830T com a opção CON
    E a coordenação e o segmento estão cadastrados e existe cardápio para a data limite
    Quando informo a coordenação, a data limite do período e o segmento
    Então vejo a descrição do segmento, a situação do período e, em cada uma das 11 linhas, o código e a descrição da refeição, a média e o total de unidades
    E vejo a data de início do período que o cardápio guarda
    E nada é gravado

  Cenário: RN-06 — período fechado na consulta
    Dado que o cardápio do período consultado está fechado
    Quando confirmo a consulta
    Então a situação do período aparece como "FECHADO"

  Cenário: RN-05 — segmento em branco adota o primeiro cadastrado
    Dado que estou na tela C830T com a opção CON
    Quando deixo o código do segmento em branco e informo os demais dados
    Então a consulta é aceita com o primeiro segmento cadastrado

  Cenário: RN-05 — repetir a mesma consulta não refaz as peneiras
    Dado que já consultei uma coordenação, um segmento e um período
    Quando confirmo de novo com os mesmos dados
    Então a tela reaproveita o que já leu e não refaz as conferências

  Cenário: RN-05 — data limite não informada
    Quando deixo a data limite do período sem preencher
    Então vejo "* Informe a data limite de validade *"
    E o cursor volta ao campo da data limite
    E nada é gravado

  Cenário: RN-05 — segmento não cadastrado
    Quando informo um código de segmento que não está cadastrado
    Então vejo "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento
    E nada é gravado

  Cenário: RN-05 — período sem cardápio
    Quando informo um período para o qual não há nenhum cardápio cadastrado
    Então vejo "* Nao existem cardapios neste periodo *"
    E o cursor volta ao campo da data limite
    E nada é gravado

  Cenário: RN-07 — coordenação e segmento sem comensais
    Dado que consultei uma coordenação e um segmento que não têm nenhuma refeição com média nem prevista
    Quando a tela monta a grade
    Então vejo "* Grupo sem comensais cadastrados neste seg *"
    E a grade não é preenchida

  Cenário: RN-02 — a tela abre em consulta
    Dado que abro a tela C830T sem nada guardado da interação anterior
    Então a opção de manutenção vem preenchida como consulta
    E a coordenação vem em branco
    E nenhuma linha da média está preenchida

  Cenário: RN-02 — opção de manutenção não disponível
    Dado que estou na tela C830T
    Quando informo uma opção de manutenção diferente de ALT e CON
    Então vejo "* Operacao nao disponivel *"
    E o cursor volta ao campo da opção
    E nada é lido e nada é gravado

  Cenário: RN-03 — valor não numérico na identificação
    Dado que estou na tela C830T
    Quando digito letras em um dos campos numéricos
    Então o campo é recusado antes de qualquer conferência de negócio
    E o cursor volta ao campo recusado
    E nada é conferido nem gravado por causa dele

  Cenário: RN-04 — coordenação em branco
    Quando confirmo sem informar a coordenação regional escolar
    Então vejo "* Informe o grupo *"
    E o cursor volta ao campo da coordenação
    E nada é gravado

  Cenário: RN-04 — coordenação fora do escopo do servidor
    Dado que o meu vínculo tem uma coordenação regional escolar
    Quando consulto o período de uma coordenação diferente dessa
    Então vejo "* Usuario sem acesso a este grupo *"
    E nada é gravado

  Cenário: RN-04 — coordenação não cadastrada
    Quando informo uma coordenação regional escolar que não está cadastrada
    Então vejo "* Grupo nao cadastrado *"
    E o cursor volta ao campo da coordenação
    E nada é gravado

  Cenário: RN-09 — a tela reabre com a última consulta
    Dado que consultei uma coordenação, um segmento e um período
    Quando reabro a tela
    Então vejo a coordenação, o segmento e o período da última consulta
    E a situação do período daquela consulta

  Cenário: RN-10 — alterar sem consultar antes
    Dado que estou na tela C830T com a opção ALT
    E informo coordenação, segmento ou data limite diferentes dos da consulta que fiz
    Quando confirmo
    Então vejo "* Consulte antes de atualizar *"
    E o cursor volta ao campo da coordenação
    E nada é lido e nada é gravado

  Cenário: RN-10 — a data de início não entra na conferência
    Dado que consultei um período e estou com a opção ALT
    Quando informo uma data de início diferente da que a consulta mostrou
    Então a alteração é aceita quanto a esse campo

  Cenário: RN-11 — novo segmento sem consultar antes
    Dado que estou na tela C830T com o indicador de novo segmento ligado
    E informo uma coordenação diferente da que está em foco
    Quando confirmo
    Então vejo "* Consulte antes de solicitar novo seg *"
    E o segmento em foco não muda
    E nada é gravado

  Cenário: RN-11 — o indicador de novo segmento avança para o segmento seguinte
    Dado que consultei uma coordenação e um segmento
    E ligo o indicador de novo segmento
    Quando confirmo
    Então a tela passa a trabalhar no segmento seguinte ao informado
    E nenhuma média é gravada

  Cenário: RN-11 — não existe segmento seguinte
    Dado que o segmento informado é o último cadastrado
    Quando ligo o indicador de novo segmento e confirmo
    Então a tela volta ao primeiro segmento cadastrado

  Cenário: RN-12 — período fechado
    Dado que a média daquela coordenação, daquele segmento e daquele período está marcada como fechada
    Quando tento alterá-la
    Então vejo "* Cadastro fechado para este periodo *"
    E o cursor volta ao campo da data limite
    E nada é gravado

  Cenário: RN-13 — média zerada zera o total de unidades
    Dado que estou na tela C830T com a opção ALT
    Quando zero a média de uma linha e deixo o total de unidades preenchido
    Então o total de unidades daquela linha é zerado pelo sistema, sem aviso

  Cenário: RN-13 — média informada sem o total de unidades
    Dado que estou na tela C830T com a opção ALT
    Quando preencho a média de uma linha e deixo o total de unidades zerado
    Então vejo "* Informe total de unidades *"
    E o cursor volta ao campo do total de unidades
    E nada é gravado

  Cenário: RN-13 — média menor que o total de unidades
    Quando preencho uma linha com a média menor que o total de unidades
    Então vejo "* Media menor que total de unidades *"
    E o cursor volta ao campo da média
    E nada é gravado

  Cenário: RN-13 — a cópia e a exclusão não conferem as quantidades
    Dado que o pedido traz a cópia ou a exclusão de um período
    Quando uma linha da grade traz a média menor que o total de unidades
    Então a conferência das quantidades não é feita
    E o pedido segue

  Cenário: RN-14 e RN-20 — alterar a média de uma refeição
    Dado que consultei uma coordenação, um segmento e um período que já têm média
    Quando troco a média ou o total de unidades de uma linha com a opção ALT
    E confirmo
    Então a média daquela refeição é regravada
    E a média como estava e como ficou fica registrada na auditoria

  Cenário: RN-14 e RN-20 — incluir a média de uma refeição no período
    Dado que consultei um período que ainda não tem média para aquela refeição
    Quando informo a média e o total de unidades da linha e confirmo a alteração
    Então nasce o registro da média daquela refeição naquele período
    E a inclusão fica registrada na auditoria

  Cenário: RN-14 — apagar a média de uma refeição
    Dado que a refeição tem média naquele período
    Quando zero a média daquela linha com a opção ALT e confirmo
    Então o registro daquela refeição é apagado do período
    E a exclusão fica registrada na auditoria

  Cenário: RN-14 — média repetida
    Dado que a média da refeição está igual ao que a tela mostra
    Quando confirmo a alteração sem mudar nada
    Então nada é gravado para aquela refeição

  Cenário: RN-14 — linha sem refeição é ignorada
    Dado que preencho uma linha da grade sem o código da refeição
    Quando confirmo a alteração
    Então aquela linha não faz nada

  Cenário: RN-15 e RN-20 — copiar um período
    Dado que consultei o período de destino e ele ainda não tem média
    E o período de origem tem média
    Quando preencho o período de cópia e o segmento de origem com a opção ALT
    E confirmo
    Então cada média do período de origem nasce no período informado, com a data de início informada
    E as linhas nascem abertas, mesmo que a origem esteja fechada
    E cada cópia fica registrada na auditoria

  Cenário: RN-15 — copiar de um período sem média
    Quando preencho um período de cópia que não tem média
    Então vejo "* Periodo para copia nao cadastrado *"
    E o cursor volta ao campo do período de cópia
    E nada é copiado

  Cenário: RN-15 — copiar sobre um período que já tem média
    Dado que o período informado no cabeçalho já tem média
    Quando preencho o período de cópia e confirmo
    Então vejo "* Nao copiar. Periodo ja cadastrado *"
    E o cursor volta ao campo do período de cópia
    E nada é copiado

  Cenário: RN-15 — copiar todos os segmentos
    Dado que o período de origem tem média em mais de um segmento
    Quando preencho o segmento de origem com 99 e confirmo
    Então as médias de todos aqueles segmentos nascem no período informado

  Cenário: RN-15 — copiar sem informar o segmento de origem
    Dado que o período de origem tem média, mas não no segmento zero
    Quando deixo o segmento de origem em branco e confirmo
    Então vejo "* Periodo para copia nao cadastrado *"
    E nada é copiado

  Cenário: RN-16 e RN-20 — excluir um período
    Dado que consultei um período que tem média
    E o período ainda não foi calculado
    Quando preencho o período de exclusão e o segmento a excluir com a opção ALT
    E confirmo
    Então as médias daquele período são apagadas
    E cada exclusão fica registrada na auditoria

  Cenário: RN-16 — excluir com período de outro ano
    Quando preencho o período de exclusão com um ano diferente do ano limite
    Então vejo "* Consulte antes de excluir *"
    E o cursor volta ao campo do período de exclusão
    E nada é apagado

  Cenário: RN-16 — excluir sem informar o segmento
    Quando preencho o período de exclusão e deixo o segmento de exclusão zerado
    Então vejo "* Informe segmento ou 99 para todos *"
    E o cursor volta ao campo do segmento de exclusão
    E nada é apagado

  Cenário: RN-16 — excluir com segmento diferente do que está em foco
    Quando informo no segmento de exclusão um segmento diferente do que está em foco e diferente de 99
    Então vejo "* Consulte antes de excluir *"
    E o cursor volta ao campo do segmento de exclusão
    E nada é apagado

  Cenário: RN-16 — excluir um período já calculado
    Dado que o período daquela coordenação já foi calculado
    Quando preencho o período de exclusão e confirmo
    Então vejo "* Nao exclua. Periodo ja calculado *"
    E o cursor volta ao campo do período de exclusão
    E nada é apagado

  Cenário: RN-16 — excluir um período sem registros
    Dado que o período de exclusão não tem nenhuma média
    Quando confirmo a exclusão
    Então vejo "* Nao existem registros para este periodo *"
    E o cursor volta ao campo do período de exclusão
    E nada é apagado

  Cenário: RN-17 — copiar e excluir no mesmo pedido
    Dado que o período tem média e o período de origem também
    Quando informo o período de cópia e o período de exclusão no mesmo pedido
    Então a exclusão é a operação executada
    E a cópia não acontece e nem chega a ser conferida

  Cenário: RN-17 — o pedido de novo segmento vence as operações de período
    Dado que ligo o indicador de novo segmento e preencho também o período de exclusão
    Quando confirmo
    Então a tela apenas passa para o segmento seguinte
    E nada é apagado e nada é copiado

  Cenário: RN-18 — a tela seguinte preenchida abandona a manutenção
    Dado que a mensagem chega à C830T com o código da tela seguinte preenchido
    Quando confirmo
    Então a transação é abandonada
    E nada é lido, gravado ou apagado
    E nenhuma mensagem é mostrada

  Cenário: RN-19 — a tela não encadeia para outra
    Dado que concluí uma consulta ou uma alteração
    Então nenhum registro e nenhuma operação são passados a outra tela
    E a única saída é voltar ao menu

  Cenário: RN-21 — a tela só grava a média e a auditoria
    Dado que consultei uma coordenação, um segmento e um período
    Quando confirmo a consulta
    Então o cadastro da coordenação, o do segmento, o da refeição, o do vínculo entre o segmento e a refeição, o do cardápio do período e o da média são apenas lidos
    E nenhuma rotina de gravação ou de exclusão deles é executada

  Cenário: RN-22 — falha de banco durante a gravação
    Dado que a gravação da média falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E a média não é considerada gravada
```
