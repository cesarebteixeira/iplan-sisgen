# US — C172T — Cadastro dos períodos de referência mensais

## Estória

Como **servidor de CRE**, quero **registrar o mês de referência em vigor com as datas
de início e de limite que ele abrange e consultar os períodos já registrados**, para
que **as telas que trabalham por mês de referência encontrem o período cadastrado com
a faixa de datas de que precisam**.

O período de referência diz qual é o mês em vigor e em que dia ele começa e termina. É
dele que saem as datas com que as telas do movimento trabalham, e há telas que recusam
o mês quando ele não está cadastrado: sem o período, elas ficam sem a faixa de datas de
que precisam. Esta tela mostra os períodos já registrados — até 13 por página — e
inclui o que falta; período cadastrado não é alterado nem apagado por aqui, e a
consulta não grava nada. O cadastro é um só para todo o sistema: não é por secretaria
nem por coordenação regional.

## Contexto

Jornada S000M → C000M → C028M → C029M → C172T.

Ator: servidor de CRE — registra o período de referência de um mês e consulta os
períodos já registrados, que as demais telas usam para compor as suas datas.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os dois passos do meio do caminho são menus: não passam registro nem operação adiante,
e não impõem modo nenhum à tela de destino — o modo é o campo da própria tela, que ela
repõe em consulta na primeira abertura da sessão. O que a C172T usa do contexto — a
matrícula, o código de acesso, o privilégio, o tipo de órgão e a CRE — vem da entrada,
e nenhum desses valores filtra os períodos mostrados: o cadastro não é por secretaria
nem por órgão.

A tela não encadeia para nenhuma outra: não passa registro nem operação adiante, e a
jornada termina nela.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O cadastro é o dos períodos de referência

Cada período de referência é um registro de **seis dados**: o **ano de referência**, o
**mês de referência**, o **dia e o mês de início** e o **dia e o mês limite** do
período. O par **ano e mês de referência** identifica o registro: não há dois períodos
com a mesma referência. O **ano de referência é obrigatório** no cadastro.

O cadastro é um só para todo o sistema: o registro não guarda secretaria, coordenação
regional nem órgão, de modo que a mesma referência serve a todas as telas que a leem.
A capacidade declarada é de **50.000 períodos** — capacidade é o máximo esperado,
parâmetro de dimensionamento, não o que está cadastrado.

### RN-02 — A página tem 13 linhas, e a lista para no primeiro período que falta

A página mostra **13 linhas**, e cada linha tem os **seis dados do período** mais a
**ação** da linha. Ao apresentar, o sistema lê o cadastro a partir da referência em que
a lista está posicionada e vai preenchendo as linhas, uma a uma, na ordem da chave —
ano e mês de referência. Não achando período para a referência da vez, a lista **para**:
as linhas seguintes ficam em branco, e o sistema não procura períodos mais adiante.

[?] A leitura que posiciona a lista é regida por sinalizadores de acesso a dados que o
acervo não documenta: não dá para afirmar se ela aceita o primeiro período igual ou
posterior à referência informada, nem se a leitura seguinte devolve o mesmo registro ou
o seguinte. A lista pode, por isso, começar ou retomar num período diferente do
esperado. Pergunta ao site.

### RN-03 — Sem período na referência, a tela avisa e não continua a lista

Não havendo período para a referência em que a lista está posicionada, e sendo a
primeira linha da página, o sistema avisa **\* Nao existem periodos cadastrados \*** e
deixa o cursor no campo do mês de referência; nada é gravado. Quando a lista para por
falta de período, a referência de continuação do cabeçalho é zerada no fim da página,
de modo que a apresentação seguinte não retoma do último período mostrado.

### RN-04 — O cabeçalho guarda a referência por onde a lista continua

Quando a lista enche as 13 linhas, o mês e o ano de referência do cabeçalho recebem a
referência do último período mostrado — é essa referência que a conferência seguinte
usa para retomar a lista. Os dois campos do cabeçalho passam pela mesma conferência
numérica dos demais, mas o acervo não lhes dá rótulo de negócio: a tela os apresenta
com o próprio nome do campo.

[?] Com que palavra a tela apresenta esses dois campos ao servidor, o acervo não diz:
os rótulos extraídos do programa são os seis da lista — mês e ano de referência, dia e
mês de início, dia e mês limite —, e os dois campos de continuação ficam de fora.
Pergunta ao site.

### RN-05 — A tela abre em consulta, no primeiro mês do ano corrente

Na primeira abertura da sessão, sem nenhum modo de manutenção ainda informado, a tela
repõe a **consulta** e posiciona-se em **janeiro do ano corrente** — o ano da data do
sistema —, de modo que a lista começa no período daquela referência. No cabeçalho a
tela mostra a **data do sistema** e a **descrição do tipo de órgão** da sessão.

[?] Os dois valores do cabeçalho são copiados de áreas de trabalho da sessão que o
programa apenas lê: não há, no acervo lido, quem os atribua. A entrada guarda a data do
sistema e a descrição do tipo de órgão na área da sessão de entrada, e o transporte
desses valores para a área que a tela lê fica fora do acervo. Se o transporte não
existir, os dois campos saem em branco. Pergunta ao site.

### RN-06 — A tela reabre no modo e na referência da última passagem

A área de trabalho da sessão é inicializada uma só vez, e é nela que ficam guardados o
modo usado e a referência da última leitura. Reabrindo a tela na mesma sessão, ela
volta no **modo** da última passagem — alteração, se foi o último — e apontada para a
**referência** que a última leitura deixou, e não em janeiro do ano corrente.

### RN-07 — A opção de manutenção só admite ALT ou CON

A tela tem um campo próprio de opção de manutenção, e ele aceita **alteração** ou
**consulta** — os mesmos que a mensagem de recusa nomeia como **ALT** e **CON**.
Qualquer outro valor é recusado com **\* Opcao nao disponivel. Use ALT ou CON \***, com
o cursor de volta no campo da opção, e nada é lido nem gravado. Antes dessa
conferência, a rota da transação já recusou, com **\* Operacao nao disponivel \***, os
códigos de operação que ela não reconhece — de modo que à conferência da tela só
chegam códigos de operação conhecidos.

[?] A mensagem manda usar ALT e CON, e a conferência da tela é feita contra os códigos
internos de alteração e de consulta: se o campo recebe exatamente o que a mensagem
manda digitar, a alteração seria recusada. O acervo mostra a conferência, não a
tradução que a camada de apresentação faria entre o que o servidor digita e o que a
conferência compara. Pergunta ao site.

### RN-08 — A consulta não grava nada

Em consulta a tela apenas apresenta os períodos: tanto a conferência da linha quanto a
passagem que grava são desviadas de propósito, e nenhuma gravação — nem do período, nem
do registro de auditoria — chega a ser executada. Uma recusa anterior também barra a
passagem que grava antes de qualquer operação.

### RN-09 — A inclusão exige a alteração, a linha marcada e o mês de referência

A inclusão só acontece quando a opção é **alteração**, a linha traz a **marca de
inclusão** e o **mês de referência** está preenchido. Linha sem o mês de referência é
ignorada em silêncio, e linha sem a marca de inclusão também — nos dois casos não há
mensagem. Só o mês é exigido: o **ano de referência em branco não é recusado**.

[?] Com o ano de referência em branco, o que vai para o cadastro depende da rotina de
criação do registro no banco, que não tem fonte no acervo lido: a tela só confere o
mês. Se o ano é obrigatório no cadastro, a conferência não o exige. Pergunta ao site.

[?] A tela exige que a linha esteja marcada para inclusão, mas não mostra onde essa
marca é preenchida: o campo vem com a linha, e o programa nunca o atribui. Se a marca
não vier do terminal — e o acervo não diz como ela chega —, a inclusão é inalcançável
por este caminho. Pergunta ao site.

### RN-10 — A inclusão recusa período já cadastrado

Antes de incluir, a tela procura o período pela referência informada; achando, recusa
com **\* Periodo ja cadastrado \***, devolve o cursor ao campo do mês de referência e
não grava nada. O próprio cadastro também não admite dois períodos com a mesma
referência.

[?] Essa procura usa a mesma leitura posicionada da lista: se ela devolver o primeiro
período igual ou posterior à referência, uma referência que não existe mas tem um
período posterior cadastrado seria recusada como já cadastrada; se exigir a referência
exata, a recusa só aparece quando o período existe mesmo. Não escolho entre os dois.
Pergunta ao site.

### RN-11 — A inclusão cadastra o mês inteiro

Informado o mês e o ano de referência, a própria tela calcula o resto: o **início é o
dia 1**, o **mês de início é o mês de referência**, o **limite é o último dia daquele
mês** e o **mês limite é o mês de referência**. O que o servidor tiver digitado nos dias
e meses de início e de limite é substituído por esse cálculo: o período cadastrado é
sempre o mês cheio. O limite sai do primeiro dia do mês seguinte, recuado de um dia.

[?] A conta é feita por uma rotina de data chamada por nome, sem fonte no acervo lido;
o recuo de um dia — e portanto o limite ser o último dia do mês — é conclusão a partir
do uso da mesma rotina numa tela irmã, não fato lido. Pergunta ao site.

### RN-12 — A tela não altera nem exclui período

As operações que a tela executa sobre o cadastro são a leitura e a **inclusão**: a
passagem que grava só é alcançada no ramo de inclusão, e as rotinas de exclusão que o
programa traz para os cadastros que ele enxerga não chegam a ser executadas. Período já
cadastrado não é alterado nem apagado por esta tela — quem altera e exclui o mesmo
cadastro é a tela irmã C170T.

### RN-13 — A operação depende da autorização da matrícula

A alteração e a inclusão são conferidas contra a autorização da matrícula: a alteração
exige a autorização de alteração, e a inclusão, a de inclusão. Sem a autorização, o
aviso é **\* Acesso negado para esta operacao \*** e a transação para ali: nada é
gravado. Com a opção de manutenção ainda em branco, e a tela marcada como tela de
manutenção, a conferência da rota usa a autorização de alteração.

### RN-14 — A inclusão grava o período e deixa o rastro na auditoria

Confirmada a inclusão, o período é criado no cadastro e a operação é registrada na
auditoria como **inclusão**, com o cadastro auditado (o dos períodos), a tela de onde
partiu, a matrícula, a secretaria, o tipo de órgão, a CRE, a estação, o dia e a hora da
sessão, e a imagem do registro gravado. O valor anterior vai vazio, porque é uma
inclusão. A consulta não deixa rastro.

[?] O número do processo que compõe a chave da auditoria não é atribuído por esta tela:
ele chega do ambiente, e o acervo lido não mostra quem o preenche. Se o ambiente não o
preencher, o rastro fica com zero nesse campo. Pergunta ao site.

[?] A montagem do rastro está sob uma condição do estado da gravação; no caminho normal
ela é satisfeita, mas o significado desse estado não está no acervo lido. Pergunta ao
site.

### RN-15 — Chegando com a tela de retorno preenchida, a manutenção é abandonada

Se a transação chegar com a indicação de **tela de retorno** preenchida — o dado que a
rota usa para devolver o servidor a outra tela —, a manutenção é abandonada: nada é
validado, nada é gravado e o servidor é levado à tela indicada.

[?] Nada nesta jornada preenche essa indicação, e a rota desvia a transação antes de a
tela conferi-la, de modo que a conferência própria da tela fica inalcançável por esse
caminho. O acervo não diz quem preenche a indicação nem para onde ela levaria. Pergunta
ao site.

### RN-16 — Falha no banco interrompe e avisa

Toda leitura e toda gravação testam o erro do banco; havendo erro, a transação é
interrompida com a mensagem do sistema e o resto não é executado — o período não é
considerado gravado.

[?] O texto da mensagem de erro do banco não está no acervo lido: a tela só entrega ao
despacho o código da ação. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Cadastro dos períodos de referência mensais

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C172T

  Cenário: O período de referência é identificado pelo ano e pelo mês
    Dado que estou na tela C172T
    Quando consulto um período de referência
    Então vejo o ano e o mês de referência, o dia e o mês de início e o dia e o mês limite
    E não existe outro período com a mesma referência
    E o cadastro comporta até 50.000 períodos

  Cenário: A página mostra 13 períodos e para no primeiro que falta
    Dado que estou na tela C172T, posicionado numa referência
    Quando a página é apresentada
    Então vejo até 13 linhas, cada uma com um período e a sua ação
    E as linhas já cadastradas vêm preenchidas pelo sistema, na ordem do ano e do mês
    E ao faltar período para a referência seguinte a lista para, e as linhas restantes ficam em branco

  Cenário: Sem período na referência, a tela avisa e não continua a lista
    Dado que não existe período para a referência em que a lista está posicionada
    Quando abro a tela C172T
    Então vejo "* Nao existem periodos cadastrados *"
    E o cursor fica no campo do mês de referência
    E a lista não continua, e nada é gravado

  Cenário: O cabeçalho guarda a referência por onde a lista continua
    Dado que a lista encheu as 13 linhas
    Então o mês e o ano de referência do cabeçalho mostram a referência do último período da lista
    E a conferência seguinte retoma a lista daquela referência

  Cenário: A tela abre em consulta, em janeiro do ano corrente
    Dado que estou abrindo a tela C172T pela primeira vez na sessão
    Quando a página é apresentada
    Então o modo em tela é a consulta
    E a lista começa no período da referência de janeiro do ano corrente
    E vejo no cabeçalho a data do sistema e a descrição do tipo de órgão da minha sessão

  Cenário: A tela reabre no modo e na referência da última passagem
    Dado que passei pela tela C172T em alteração, sobre uma referência
    Quando volto a abrir a tela na mesma sessão
    Então ela reabre em alteração
    E apontada para a referência que a última leitura deixou

  Cenário: A opção de manutenção só admite ALT ou CON
    Dado que estou na tela C172T
    Quando informo uma opção de manutenção diferente de alteração e de consulta
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é lido nem gravado

  Cenário: A rota recusa o código de operação que não reconhece
    Dado que estou na tela C172T
    Quando informo um código de operação que a rota não conhece
    Então vejo "* Operacao nao disponivel *"
    E a transação para ali, e nada é gravado

  Cenário: A consulta não grava nada
    Dado que abri a tela C172T em consulta
    Quando percorro e confirmo as linhas da página
    Então nenhum período é incluído
    E nenhum registro de auditoria é gravado

  Cenário: A inclusão cadastra o mês que falta, do dia 1 ao último dia
    Dado que estou em alteração e não existe período para o mês e o ano de referência informados
    Quando preencho a linha com o mês e o ano de referência, marco a linha para inclusão e confirmo
    Então o período é cadastrado com início no dia 1 do mês de referência
    E o limite é o último dia daquele mês, e o mês de início e o mês limite são o mês de referência
    E a operação fica registrada na auditoria como inclusão

  Cenário: O dia e o mês digitados são substituídos pelo cálculo
    Dado que estou em alteração sobre um mês que falta
    Quando digito um dia e um mês de início e um dia e um mês limite diferentes do mês cheio, e confirmo
    Então o período fica cadastrado com o início no dia 1 e o limite no último dia do mês de referência
    E o mês de início e o mês limite são o mês de referência

  Cenário: Linha sem o mês de referência ou sem a marca de inclusão é ignorada
    Dado que estou na tela C172T em alteração
    Quando confirmo uma linha sem o mês de referência, ou sem a marca de inclusão
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada, e nada é gravado

  Cenário: A inclusão recusa período já cadastrado
    Dado que já existe período para o mês e o ano de referência informados
    Quando preencho a linha, marco a linha para inclusão e confirmo
    Então vejo "* Periodo ja cadastrado *"
    E o cursor volta ao campo do mês de referência
    E nada é gravado

  Cenário: A tela não altera nem exclui período
    Dado que estou na tela C172T em alteração
    Quando confirmo qualquer linha
    Então nenhum período já cadastrado é alterado ou apagado
    E a única gravação que a tela faz no cadastro é a inclusão de um período novo

  Cenário: Sem a autorização da operação
    Dado que a minha matrícula não tem a operação de inclusão autorizada nesta tela
    Quando confirmo uma linha marcada para inclusão
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: O rastro da inclusão na auditoria
    Dado que confirmei a inclusão de um período
    Quando a gravação termina
    Então existe um registro de auditoria do cadastro de períodos
    E com a operação de inclusão, a imagem do registro gravado e o valor anterior vazio
    E com a matrícula, a secretaria, o tipo de órgão, a CRE, a estação e o dia e a hora da sessão

  Cenário: A tela de retorno preenchida abandona a manutenção
    Dado que a transação chega à C172T com a indicação de tela de retorno preenchida
    Quando a manutenção começaria
    Então o processamento é abandonado e nada é gravado
    E o servidor é levado à tela indicada

  Cenário: Falha no banco durante a gravação
    Dado que a gravação do período falha no banco
    Quando confirmo a inclusão
    Então a transação é interrompida com a mensagem de erro do sistema
    E o período não é considerado cadastrado
```
