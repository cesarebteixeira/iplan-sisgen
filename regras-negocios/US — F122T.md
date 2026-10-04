# US — F122T — Manter os convênios das instituições beneficentes da coordenadoria regional escolar

## Estória

Como **servidor de CRE**, quero **registrar e cancelar, linha a linha, o convênio anual
das instituições beneficentes da minha coordenadoria**, para que **cada instituição
fique com o convênio do ano registrado e a nota fiscal que depende dele possa ser
lançada**.

A tela reúne, para uma coordenadoria e um ano de competência, as instituições
beneficentes daquela coordenadoria e o convênio de cada uma naquele ano. É desse
registro que a tela da nota fiscal depende: sem convênio registrado para a instituição
beneficente da coordenadoria, o lançamento da nota é recusado com
**\* Convenio nao cadastrado \***.

A tela **grava**: inclui e cancela convênios e deixa o rastro de cada operação na
auditoria. Só não grava quando o modo informado é o de consulta.

## Contexto

Jornada S000M → F000M → F100M → F122T (4 passos).

Ator: servidor de CRE — mantém, por coordenadoria e por ano de competência, o convênio
de cada instituição beneficente da sua coordenadoria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada são menus e só encaminham: nenhuma delas passa
registro nem modo de operação para a F122T — a tela abre por si. O contexto que ela usa
— o tipo de órgão, o código de acesso, o privilégio, a matrícula e a coordenadoria da
sessão — é o que a entrada deixou, e a F122T apenas o repassa às rotinas comuns de rota
e de segurança.

---

## Regras de negócio

### RN-01 — A grade tem 13 linhas e cada linha traz a instituição e o convênio dela no ano

A tela apresenta **13 linhas**. Cada linha traz quatro informações — o **código INEP**
da instituição beneficente (8 dígitos), o **nome da instituição** (40 posições), o
**número do convênio** (3 dígitos) e o **ano do convênio** (4 dígitos) — e mais uma
posição: a **marca de ação** da linha. No cabeçalho ficam o **modo de manutenção**, a
**coordenadoria** (2 dígitos), o **ano de competência** (4 dígitos), a **descrição do
tipo de órgão da sessão** e a **data do sistema**.

[?] A descrição do tipo de órgão e a data do sistema que o cabeçalho mostra vêm do
ambiente, e não da tela: no acervo lido elas só aparecem sendo inicializadas em branco.
A descrição tem origem na entrada, que a lê do cadastro de tipos de órgão, mas o trecho
que a transporta até a tela não está no acervo lido. Pergunta ao site.

### RN-02 — A lista sai do cadastro de instituições beneficentes da coordenadoria e anda de 13 em 13

Com a coordenadoria e o ano de competência em uso, a tela percorre o **cadastro de
instituições beneficentes** na ordem da chave do cadastro — a instituição, pelo código
INEP — e monta uma linha por instituição daquela coordenadoria; para cada instituição,
procura o **convênio dela no ano de competência** e exibe o número e o ano achados.
Montadas as 13 linhas, a lista para; não havendo mais instituição, as linhas restantes
ficam em branco.

A tela guarda na área de trabalho da sessão a **última instituição mostrada**, e é dessa
posição que a montagem parte na abertura seguinte: cada abertura continua de onde a
anterior parou. Quando a lista termina antes da 13ª linha, a posição guardada volta ao
início.

A lista só é montada quando já existe **ano de competência em uso**: antes de o operador
informar um ano que passe nas conferências, a tela abre com a grade vazia.

[?] A montagem da lista é a passagem de abertura da transação, e o tratamento da
mensagem do operador não a repete. Se o ano informado só produz lista na abertura
seguinte da tela, ou se existe um caminho que remonta a grade, o acervo lido não
determina. Pergunta ao site.

[?] A leitura que parte da posição guardada usa o recurso de posicionamento do
dicionário de dados, cujo efeito exato não está no acervo nem no manual: se ele exige a
chave exata, a primeira linha da abertura seguinte repete a última instituição da
anterior; se ele posiciona na primeira chave igual ou posterior, a abertura seguinte
avança. Os dois comportamentos são compatíveis com o que o fonte mostra. Pergunta ao
site.

### RN-03 — Não havendo instituição beneficente na coordenadoria, a tela avisa

Não achando nenhuma instituição beneficente para a coordenadoria informada, a tela avisa
**\* Nao existem inst. beneficentes cadastradas \*** e não monta nenhuma linha. O aviso
é decidido na montagem da **primeira linha** e não se repete: uma lista que se esgote
depois da primeira linha fica em branco, sem aviso.

### RN-04 — O modo de manutenção da tela só admite alteração e consulta

O modo da tela aceita dois valores: **alteração** e **consulta** — os que a mensagem
nomeia como **ALT** e **CON**. Qualquer outro valor é recusado com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta ao campo do modo,
e nenhuma linha é processada.

O modo de **inclusão** e o de **exclusão** não são aceitos no cabeçalho, ainda que a
tela inclua e cancele: o que cada linha faz é decidido pela **marca de ação da linha**,
não pelo modo do cabeçalho.

Na abertura da tela o modo é reposto sozinho: com o último modo usado na sessão, quando
houver, e como **consulta** quando não houver.

[?] Os valores que a tela compara com o modo são os códigos internos "CHG" e "INQ",
enquanto a mensagem manda o operador usar "ALT" e "CON"; o campo tem três posições, que
é o tamanho de "ALT" e de "CON". Se a máscara traduz o que o operador digita para o
código interno, ou se o texto da mensagem saiu trocado, é pergunta ao site.

[?] A recusa só é alcançável se a máscara oferecer ao operador o campo do modo, porque
na abertura ele é reposto sozinho. E, mesmo recusando, a tela não levanta por si o
estado de erro que a gravação consulta: a recusa marca a linha e encerra a conferência
das linhas seguintes, enquanto a passagem que grava interroga apenas o modo e a marca de
ação da linha. Quem impede a gravação depois da recusa é o estado de erro que a rotina
de mensagem do ambiente levanta — a rotina é declarada, não definida, no acervo lido.
Se esse estado não for levantado, uma linha marcada grava mesmo depois de a tela mostrar
a recusa. Pergunta ao site.

### RN-05 — No modo de consulta nada é gravado

No modo de consulta a tela só lê: nenhum convênio é registrado ou cancelado e nenhum
registro de auditoria é criado. Gravar exige o modo de alteração.

### RN-06 — A coordenadoria é obrigatória

A coordenadoria em uso é obrigatória na alteração: deixada em branco, a recusa é
**\* Informe o grupo \***, com o cursor de volta ao campo da coordenadoria e sem
processar linha nenhuma. Quando a coordenadoria e o ano de competência são os mesmos da
abertura, a conferência não se repete.

### RN-07 — A coordenadoria informada tem de estar cadastrada e ativa

A coordenadoria informada é procurada no **cadastro de coordenadorias**, pelo tipo de
órgão da sessão e pelo código da coordenadoria. Não estando cadastrada — ou estando
marcada como **excluída** —, a recusa é **\* Grupo nao cadastrado \***, com o cursor de
volta ao campo da coordenadoria e sem processar linha nenhuma. A marca de exclusão é
conferida depois de o registro ser achado: coordenadoria excluída é tratada como não
cadastrada.

[?] Essa procura usa o **tipo de órgão da área de trabalho do módulo**, e o acervo lido
não atribui valor a esse dado: ele só aparece sendo zerado. Se ele não chegar à tela, a
procura é feita com zero e nenhuma coordenadoria é achada — e então a tela recusa toda
operação. A tela irmã que lê o mesmo cadastro usa, para a mesma chave, o tipo de órgão
da área de segurança. Pergunta ao site.

### RN-08 — A coordenadoria da sessão limita o que se pode manter

Quando a sessão carrega uma coordenadoria, só ela pode ser informada: informando outra,
a recusa é **\* Usuario sem acesso a este grupo \***, com o cursor de volta ao campo da
coordenadoria e sem processar linha nenhuma. Quando a sessão não carrega coordenadoria
nenhuma — o caso do usuário de secretaria —, qualquer coordenadoria cadastrada passa.

[?] A coordenadoria da sessão que esta tela lê está na área de trabalho do módulo, que o
acervo lido só inicializa em branco; nenhum programa do acervo atribui valor a ela — a
entrada guarda a coordenadoria do funcionário em outra área, na da sessão. O mesmo vale
para o tipo de órgão, a matrícula, o privilégio e o código de acesso que a tela repassa
às rotinas de segurança. Se esses valores não forem transportados, todo operador cai no
ramo do usuário sem coordenadoria e a regra "só vejo a minha" deixa de valer. Pergunta
ao site.

### RN-09 — O ano de competência não pode ser anterior a 2010

O ano de competência informado tem de ser **2010 ou posterior**. Antes disso, a recusa é
**\* Ano de competencia invalido \***, com o cursor de volta ao campo do ano, e nenhuma
linha é processada.

[?] O piso de 2010 é um valor fixo no programa, sem cadastro que o explique: se é o
começo dos convênios, do exercício ou da base, o acervo não diz. Pergunta ao site.

### RN-10 — A marca da linha decide a operação, e só a linha com marca e número é processada

Cada linha é processada pela **marca de ação** digitada nela: a marca **I** manda
**incluir** o convênio daquela instituição e a marca **E** manda **cancelar** — conforme
a marca, a tela confere a permissão de inclusão ou a de exclusão e segue para a gravação
correspondente.

Uma linha só é processada quando tem a **marca** e o **número do convênio**
preenchidos. Linha em branco, ou com apenas um dos dois, passa batido: não gera recusa e
não grava nada. Marca diferente de **I** e de **E** também não é processada — e, nesse
caso, nem é recusada.

[?] "I" e "E" são os dois valores que o programa compara; a leitura deles como incluir e
excluir vem do que ele faz depois de cada um. O rótulo que a máscara mostra para essa
coluna não está no lote. Pergunta ao site.

### RN-11 — A inclusão exige a instituição na linha e o ano do convênio igual ao da competência

Na inclusão, a linha tem de ter o **código INEP** da instituição preenchido; sem ele, a
recusa é **\* Informe convenio para linha preenchida \*** e o cursor volta à coluna da
marca de ação. E o **ano do convênio** tem de ser igual ao **ano de competência**:
deixado em branco, a tela o preenche com o ano de competência; informado outro ano, a
recusa é **\* Ano convenio deve ser igual ao de competencia \***.

[?] A mensagem pede o convênio, mas a conferência é do código INEP da instituição, e o
cursor volta à coluna da marca de ação — não ao campo do convênio nem ao da instituição.
Se o texto e o cursor são os que o site espera, é pergunta ao site.

### RN-12 — A inclusão é recusada quando a instituição já tem convênio no ano

Se a instituição da linha já tem convênio registrado naquele **ano de competência**, a
inclusão é recusada com **\* Convenio ja cadastrado para este INEP \***. O convênio da
instituição é **um por ano**: para trocar o número, cancela-se o convênio do ano e
inclui-se outro.

### RN-13 — O número do convênio vale por coordenadoria e por ano

O número do convênio, no mesmo ano, é conferido contra os convênios já registrados. Se o
número e o ano forem de **outra linha da mesma instituição**, a recusa é
**\* Convenio ja cadastrado \***. Se forem de **outra instituição beneficente da mesma
coordenadoria**, a recusa é **<- Convenio cadastrado para outro INEP \***, e a tela
mostra, antes da mensagem, o código INEP da instituição que já usa o número. Convênio de
instituição de **outra coordenadoria** não impede a inclusão.

### RN-14 — O cancelamento apaga o convênio da instituição no ano de competência

A marca **E** cancela o convênio da instituição **no ano de competência**. Quem localiza
o convênio a cancelar é a instituição e o ano de competência: o número do convênio
informado na linha não é usado para isso — ele só é exigido para a linha ser processada.

O cancelamento não confere se o convênio existe: uma linha marcada para uma instituição
sem convênio naquele ano segue para o cancelamento assim mesmo, e a tela não avisa nada.

[?] A leitura que procura o convênio a cancelar, quando não acha, apenas marca o estado
de "não encontrado" e continua; o registro de auditoria sai com o que tiver ficado na
área de leitura e o cancelamento é tentado assim mesmo. O que o sistema faz nesse caso —
se apaga alguma coisa, e o que a auditoria registra — não está determinado no acervo
lido. Pergunta ao site.

### RN-15 — Cada operação efetiva deixa registro na auditoria

Toda inclusão e todo cancelamento gravam um registro de **auditoria** com a operação
(inclusão ou exclusão), o **teor do convênio antes e depois** (300 posições cada), o
código INEP da instituição, a coordenadoria, a matrícula do servidor, o terminal, a data
e a hora da sessão e o cadastro alterado. Na inclusão, o "antes" sai em branco e o
"depois" é o convênio registrado; no cancelamento, o "antes" é o convênio apagado e o
"depois" sai em branco. Não havendo gravação de convênio — no modo de consulta —, nenhum
registro de auditoria é criado.

[?] Na inclusão, a auditoria é gravada sob uma condição de estado cujo valor ("DATA") não
está explicado no acervo nem no manual; no cancelamento, essa condição não é conferida.
Se existe caso em que o convênio é gravado e a auditoria não, é pergunta ao site.

[?] O campo de tipo de manutenção do registro de auditoria recebe sempre "A", tanto na
inclusão quanto no cancelamento; a distinção entre as duas fica no campo de operação
("ADD" e "DEL"). Se o site espera "D" no cancelamento, é pergunta ao site.

### RN-16 — Nenhuma operação acontece sem a conferência de acesso e de permissão

Antes de validar e antes de gravar, a transação passa pelas rotinas comuns de
**segurança de perfil**, de **rota** e de **permissão por operação**, com o contexto da
sessão. A tela precisa estar no **cadastro de telas** — não estando, a recusa é
**\* Tela nao disponivel \***; depois, a matrícula precisa ter a tela autorizada no seu
**código de acesso** — não tendo, a recusa é **\* Acesso negado para esta matricula \***.
Se qualquer conferência não devolver "OK", a transação é abandonada: nada é gravado e
nada é auditado.

Além disso, cada linha marcada troca a permissão conferida: a marca de inclusão exige a
permissão de **inclusão** e a de cancelamento exige a de **exclusão**, no cadastro de
autorizações por código de acesso. Sem a permissão, a recusa é
**\* Acesso negado para esta operacao \***.

[?] A permissão da linha é conferida contra o código da **própria tela F122T** — a mesma
tela cujo modo de cabeçalho só aceita alteração e consulta —, e não contra o cadastro do
convênio. Se o cadastro de autorizações não liberar inclusão e exclusão para a F122T,
toda linha marcada é recusada e a tela vira consulta. Pergunta ao site.

[?] A conferência de permissão é feita na passagem de validação e não se repete na
passagem que grava: se ela mudar entre as duas, a gravação não a reconfere. Pergunta ao
site.

## Cenários BDD

```gherkin
Funcionalidade: Manter os convênios das instituições beneficentes da coordenadoria regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F122T

  Cenário: A grade mostra as instituições beneficentes da coordenadoria e o convênio de cada uma no ano
    Dado que a coordenadoria informada tem instituições beneficentes cadastradas
    Quando abro a tela F122T com a coordenadoria e o ano de competência em uso
    Então vejo até 13 linhas
    E cada linha traz o código INEP, o nome da instituição, o número do convênio e o ano do convênio
    E vejo a descrição do tipo de órgão da minha sessão e a data do sistema

  Cenário: A lista avança de 13 em 13
    Dado que a coordenadoria tem mais de 13 instituições beneficentes
    Quando abro a tela F122T
    Então vejo as 13 primeiras instituições
    E a abertura seguinte continua a partir da última que apareceu

  Cenário: Sem o ano de competência em uso, nenhuma linha é montada
    Dado que a tela ainda não tem ano de competência em uso
    Quando abro a tela F122T
    Então nenhuma linha da grade é montada

  Cenário: Coordenadoria sem instituição beneficente cadastrada
    Dado que a coordenadoria informada não tem instituição beneficente cadastrada
    Quando abro a tela F122T com essa coordenadoria e um ano de competência
    Então vejo a mensagem "* Nao existem inst. beneficentes cadastradas *"
    E nenhuma linha é montada

  Cenário: Modo de manutenção diferente de alteração e de consulta
    Dado que estou na tela F122T
    Quando informo um modo de manutenção que não é ALT nem CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo do modo
    E nenhuma linha é processada

  Cenário: A consulta não grava nada
    Dado que informei a coordenadoria e o ano de competência no modo de consulta
    Quando peço a operação
    Então nenhum convênio é registrado ou cancelado
    E nenhum registro de auditoria é criado

  Cenário: Coordenadoria em branco
    Dado que deixo o campo da coordenadoria em branco
    Quando peço a operação
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo da coordenadoria
    E nenhuma linha é processada

  Cenário: Coordenadoria não cadastrada ou excluída
    Dado que a coordenadoria informada não está cadastrada para o tipo de órgão da sessão, ou está marcada como excluída
    Quando peço a operação
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo da coordenadoria
    E nenhuma linha é processada

  Cenário: Coordenadoria fora da minha sessão
    Dado que a minha sessão está vinculada a uma coordenadoria
    Quando informo outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenadoria
    E nenhuma linha é processada

  Cenário: Ano de competência anterior a 2010
    Dado que informo um ano de competência anterior a 2010
    Quando peço a operação
    Então vejo a mensagem "* Ano de competencia invalido *"
    E o cursor volta ao campo do ano
    E nenhuma linha é processada

  Cenário: Linha sem número de convênio não é processada
    Dado que marco uma linha com I ou com E
    E deixo o número do convênio dessa linha em branco
    Quando peço a operação
    Então a linha não é processada
    E nenhuma mensagem é mostrada por causa dela

  Cenário: Linha sem marca de ação não é processada
    Dado que preencho o número do convênio de uma linha
    E deixo a marca de ação dessa linha em branco
    Quando peço a operação
    Então a linha não é processada
    E nenhum convênio é registrado ou cancelado

  Cenário: Linha com marca de ação diferente de I e de E
    Dado que preencho o número do convênio de uma linha
    E informo na marca de ação um valor que não é I nem E
    Quando peço a operação
    Então a linha não é processada
    E nenhuma mensagem de recusa é mostrada por causa dela

  Cenário: Inclusão do convênio de uma instituição beneficente
    Dado que a instituição da linha não tem convênio no ano de competência
    E o número do convênio não está em uso na coordenadoria naquele ano
    Quando marco a linha com I e informo o número e o ano do convênio
    Então o convênio fica registrado para a instituição naquele ano
    E a inclusão fica registrada na auditoria, com o convênio no "depois" e o "antes" em branco

  Cenário: Inclusão sem o ano do convênio igual ao da competência
    Dado que marco uma linha com I
    Quando informo um ano de convênio diferente do ano de competência
    Então vejo a mensagem "* Ano convenio deve ser igual ao de competencia *"
    E nenhum convênio é registrado

  Cenário: Inclusão com o ano do convênio em branco
    Dado que marco uma linha com I
    E deixo o ano do convênio em branco
    Quando peço a operação
    Então o ano do convênio é preenchido com o ano de competência
    E o convênio é registrado com esse ano

  Cenário: Inclusão sem a instituição na linha
    Dado que marco uma linha com I
    E deixo o código INEP da instituição em branco
    Quando peço a operação
    Então vejo a mensagem "* Informe convenio para linha preenchida *"
    E o cursor volta à coluna da marca de ação
    E nenhum convênio é registrado

  Cenário: Inclusão para instituição que já tem convênio no ano
    Dado que a instituição da linha já tem convênio registrado no ano de competência
    Quando marco a linha com I
    Então vejo a mensagem "* Convenio ja cadastrado para este INEP *"
    E nenhum convênio é registrado

  Cenário: Número de convênio já usado por outra instituição da mesma coordenadoria
    Dado que o número e o ano do convênio informados já são de outra instituição beneficente da mesma coordenadoria
    Quando marco a linha com I
    Então vejo, antes da mensagem, o código INEP da instituição que já usa o número
    E vejo a mensagem "<- Convenio cadastrado para outro INEP *"
    E nenhum convênio é registrado

  Cenário: Número de convênio já usado por outra linha da mesma instituição
    Dado que o número e o ano do convênio informados já são de outra linha da mesma instituição
    Quando marco a linha com I
    Então vejo a mensagem "* Convenio ja cadastrado *"
    E nenhum convênio é registrado

  Cenário: Número de convênio de instituição de outra coordenadoria
    Dado que o número e o ano do convênio informados são de uma instituição de outra coordenadoria
    Quando marco a linha com I
    Então o convênio da minha instituição é registrado
    E nenhuma mensagem de recusa é mostrada

  Cenário: Cancelamento do convênio da instituição
    Dado que a instituição da linha tem convênio registrado no ano de competência
    Quando marco a linha com E e informo o número do convênio
    Então o convênio da instituição naquele ano deixa de existir
    E o cancelamento fica registrado na auditoria, com o convênio no "antes" e o "depois" em branco

  Cenário: O que se cancela é o convênio da instituição no ano, não o número informado
    Dado que a instituição da linha tem convênio registrado no ano de competência
    Quando marco a linha com E e informo um número de convênio diferente do registrado
    Então o convênio da instituição naquele ano é o que deixa de existir

  Cenário: Cancelamento de linha sem convênio registrado
    Dado que a instituição da linha não tem convênio registrado no ano de competência
    Quando marco a linha com E e informo um número de convênio
    Então a tela não avisa que não há convênio a cancelar
    E segue para o cancelamento do convênio da instituição naquele ano

  Cenário: A tela não está cadastrada
    Dado que a tela F122T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E nada é gravado nem auditado

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela F122T autorizada no meu código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E nada é gravado nem auditado

  Cenário: Sem permissão de inclusão ou de exclusão
    Dado que o meu código de acesso não tem a permissão de inclusão (ou a de exclusão) liberada para a tela F122T
    Quando marco uma linha com I (ou com E)
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nenhum convênio é registrado ou cancelado
    E nenhum registro de auditoria é criado
```
