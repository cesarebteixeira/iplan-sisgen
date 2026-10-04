# US — M060T — Reabrir o mapa do mês de referência de um órgão filho

## Estória

Como **servidor de CRE**, quero **reabrir o mapa do mês de referência de uma unidade da
minha coordenadoria**, para que **os registros daquele mês voltem a aceitar lançamento e a
unidade possa corrigir ou completar o que já tinha sido encerrado**.

O mapa é o registro da unidade no mês, e é por ele que a coordenação regional acompanha o
que já foi lançado e o que falta. Fechar o mês é o que encerra o lançamento de uma vez;
reabrir é o que devolve o mês ao trabalho, quando a unidade precisa acertar o que foi
encerrado. Como reabrir desfaz um encerramento, o sistema não o executa sem antes mostrar o
que entendeu e ouvir a confirmação de quem pediu; e, quando não há nada fechado naquele mês,
ele não reabre e avisa. A reabertura vale para o mês inteiro de uma unidade e alcança tudo o
que o mês tem: o mapa, os registros diários, os registros da geração anterior do mapa e os
registros de merenda.

## Contexto

Jornada S000M → M000M → M060T.

Ator: servidor de CRE — reabre o mês de referência de uma unidade (escola ou creche) da sua
coordenadoria regional, dizendo de qual unidade e de qual mês se trata e confirmando a
reabertura.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O M000M é um menu e não grava nada: apenas
encaminha. O contexto que a M060T usa — a matrícula, o acesso, o tipo de órgão, a
coordenadoria e o órgão filho do servidor — é o que a entrada deixou na sessão. Esta tela é o
outro lado da M050T: aquela encerra o mês de uma unidade; esta o devolve ao trabalho. A M060T
não muda de comportamento conforme a tela que a abriu: ela é sempre a mesma, venha do menu ou
de uma chamada automática, e o que a decide é o que a sessão traz e o que o servidor informa.
A jornada termina nesta tela — ela não encadeia em outra: terminada a reabertura, a tela volta
a si mesma.

---

## Regras de negócio

### RN-01 — A tela reabre o mês de uma unidade; não inclui, não exclui e não é de consulta

Reabrir é trocar a **situação** dos registros **fechados** daquela unidade naquele mês de
volta para **aberta**: o **mapa do mês**, os **registros diários do mapa**, os **registros do
mês da geração anterior do mapa** e os **registros de merenda do mês** — o cardápio da semana,
os gêneros com fornecedor e nota fiscal e as quantidades de refeições por categoria. Nada do
mês é apagado e nada do mês é criado: o que a tela grava é o próprio registro que já existia,
com a situação trocada. Fora desses, a tela cria apenas o **registro da fila do processamento
do mapa** (RN-12) e os **rastros de auditoria** (RN-13). Ela não tem consulta nem manutenção de
cadastro: só reabre, e termina nela mesma.

### RN-02 — A reabertura é confirmada antes de acontecer

Conferido tudo, a tela não reabre: ela mostra **\* Confirma reabertura do mapa <S/N> ? \*** e
espera. Só a resposta **S** leva à reabertura, e ela vale para o que estava na tela: se o
órgão, o ano ou o mês já não forem os mesmos, a resposta é descartada, o que está na tela é
validado de novo e a mesma pergunta volta. Qualquer outra resposta, inclusive **N**, não
reabre nada e a tela volta a perguntar.

[?] Responder **N** não cancela a reabertura: não há no programa resposta de cancelamento e a
tela insiste até vir um **S**. Se é o desenho, ou se o ramo ficou sem caminho de saída,
pergunta ao site.

[?] A reabertura não acontece na resposta: ela depende de a marca de confirmação continuar
valendo e de o marcador de erro não ter ficado do pedido anterior. O material lido não mostra
onde esses marcadores são limpos entre uma entrada e outra. Pergunta ao site.

### RN-03 — O órgão filho é obrigatório e tem de existir no cadastro

O servidor diz de quem é o mês informando o **órgão filho** — uma escola ou uma creche. Sem
ele, a recusa é **\* Informe o orgao \***, com o cursor no campo, e nada é validado depois
disso. O órgão é procurado no cadastro de órgãos; não existindo, ou estando excluído, a recusa
é **\* Orgao nao cadastrado \***. O órgão da própria sessão passa pela mesma conferência: se
ele não estiver no cadastro, a recusa é a mesma e a tela não segue.

[?] Quando a sessão não traz coordenadoria, a tela admite que o servidor informe a
coordenadoria em vez do órgão, mas exige o órgão logo em seguida, com a mesma mensagem: a
coordenadoria digitada não substitui o órgão. Se a intenção era permitir reabrir por
coordenadoria, o caminho não permite. Pergunta ao site.

### RN-04 — O servidor reabre o órgão que a sessão lhe dá, e o órgão tem de ser da sua coordenadoria e do seu tipo de órgão

Se a sessão carrega um **órgão filho**, a tela abre o campo com ele e recusa qualquer outro:
**\* Usuario sem acesso a outro orgao \***. O órgão informado tem ainda de ser do mesmo **tipo
de órgão** da sessão — fora disso, **\* Orgao nao pertence a esta secretaria \*** — e, quando a
sessão tem **coordenadoria**, o órgão tem de ser daquela coordenadoria: **\* Usuario sem acesso
ao grupo deste orgao \***. A coordenadoria mostrada na tela não é digitada: ela é reposta com a
do cadastro do órgão.

[?] Com a sessão sem coordenadoria, a conferência da coordenadoria não roda e o que sobra é o
tipo de órgão. Se isso libera a reabertura de unidades de qualquer coordenadoria da mesma rede,
pergunta ao site.

### RN-05 — O cadastro do órgão tem de estar completo

Antes de reabrir, a tela confere **seis** dados do cadastro do órgão: o **bairro**, o **órgão
pai**, o **nome**, o **endereço**, o **número de matriculados** e o **número de pessoas**.
Faltando qualquer um deles, a recusa é **\* Orgao cadastrado com dados incompletos \***, com o
cursor no órgão, e o mês não é reaberto.

[?] Não está no material lido por que a reabertura do mês depende de dados de endereço e de
quantitativos da unidade. Pergunta ao site.

### RN-06 — O mês e o ano de referência são obrigatórios e têm de formar uma data do calendário

Faltando o mês ou o ano, a recusa é **\* Informe Mes/Ano para a reabertura \***, com o cursor
no mês. Informados os dois, o par tem de ser uma data do calendário — o dia 1º daquele mês —,
com o ano entre **1994** e **2099**: fora disso, **\* Mes/ano invalido \***, também com o cursor
no mês.

### RN-07 — O período do mês vem da tabela de períodos do mapa, e não do teclado

Para o mês e o ano informados, a tela lê a **tabela de períodos do mapa** e repõe nos campos de
período o **dia, o mês e o ano do início** e do **limite** do período: o servidor não informa
esses campos, e o que digitar neles é descartado. Existindo o período, é o **início** dele que
separa os registros diários que a reabertura alcança. Não existindo o mês na tabela, a tela
**não recusa**: segue com o período em branco.

[?] A tela irmã, que pede a geração do mapa, recusa o mês que não está na tabela de períodos do
mapa. Aqui ele passa. Se a intenção era exigir a tabela também na reabertura, o caminho não
exige. Pergunta ao site.

[?] Sem o período da tabela, o que separa os registros diários do mês fica zerado, e qualquer
registro diário fechado da unidade entra na reabertura. Se é isso que se espera de um mês que a
tabela não tem, pergunta ao site.

### RN-08 — A tela não reabre um mês que não tenha registro fechado

Antes de pedir a confirmação, a tela procura registro **fechado** daquela unidade naquele mês:
o mapa do mês, algum registro diário a partir do início do período, ou os registros do mês da
unidade. Não achando nenhum, a recusa é **\* Nao existem reg.fechados para esta Escola \*** ou
**\* Nao existem reg.fechados para esta Creche \***, conforme a unidade seja creche, e nada é
reaberto. É também por isso que um mês já reaberto não se reabre duas vezes: ele deixa de ter
registro fechado.

[?] Para a **creche**, a conferência que procura o **mapa do mês da geração anterior** procura
no cadastro que é o da **escola**, e não no da creche — que é justamente o que a reabertura
depois devolve ao trabalho. Uma creche cujo único registro fechado seja o mapa da geração
anterior dela ouve que não há registros fechados e não reabre. A tela irmã de fechamento, feita
do mesmo molde, procura no cadastro da creche. Pergunta ao site.

### RN-09 — Escola e creche não têm os mesmos registros do mês

A unidade é tratada como **creche** quando o cadastro do órgão a marca assim, e como **escola**
em qualquer outro caso. O mapa do mês, os registros diários, o cardápio da semana e os gêneros
com fornecedor e nota fiscal são reabertos nos dois casos; os **registros do mês da geração
anterior do mapa** e as **quantidades de refeições por categoria** existem em cadastros
separados para escola e para creche, e a tela reabre o do tipo da unidade. A mensagem final diz
qual dos dois foi reaberto.

[?] O único valor que a tela distingue é a marca de creche; qualquer outro valor do campo cai no
caso "escola", e o que o campo aceita além da marca não está no material lido. Pergunta ao
site.

### RN-10 — A reabertura dos registros diários percorre o mês a partir do limite do período

O mapa do mês é reaberto direto, achado que seja. Os registros diários são percorridos em
sequência: a leitura começa posicionada no **limite** do período e reabre cada registro fechado
daquela unidade cuja data não seja anterior ao **início** do período, até encontrar um registro
que não seja daquela unidade, daquela coordenadoria ou daquele estado — e para ali.

[?] A leitura começa no limite do período, mas a conferência aceita qualquer data a partir do
início: o início não barra nada que a leitura já não tivesse deixado de fora. Se a reabertura
deveria alcançar os dias anteriores ao limite, o caminho não os alcança. Pergunta ao site.

[?] A varredura para no primeiro registro que não esteja fechado: um registro já reaberto no
meio do mês deixa os seguintes fechados. Se é intenção reabrir por blocos ou se é defeito,
pergunta ao site.

### RN-11 — A reabertura devolve a situação dos registros e grava quem reabriu, de onde e quando

Cada registro fechado que a tela alcança volta a **aberta**, um a um, no próprio registro: a
tela trava o registro, troca a situação e o regrava. Além da situação, os registros que têm
esses campos levam a **matrícula** de quem reabriu, a **estação** e a **data e hora** da
gravação, e a data de atualização é a do sistema. Nada é apagado e nenhum registro novo do mês
é criado por essa troca.

### RN-12 — A reabertura devolve o mês de uma unidade à fila do processamento do mapa

Quando a unidade ainda não tem, para aquele mês, o registro que o **processamento do mapa** usa
como fila de trabalho, a reabertura **cria** esse registro. É a única criação de registro de
negócio que esta tela faz, e ela é registrada na auditoria como **inclusão**. Como é esse mesmo
registro que o processamento em lote do mapa percorre e apaga ao terminar cada unidade, reabrir
um mês também devolve aquela unidade e aquele mês à fila daquele processamento.

[?] Nenhuma outra tela do acervo lido cria esse registro: a tela que pede a geração do mapa
grava o pedido em outro lugar, e quem mais toca o registro é o próprio processamento em lote,
que só o apaga. Se a criação por esta tela era o desenho, ou se a fila deveria ser alimentada
só por quem pede a geração, não se decide pelo corpus. Pergunta ao site.

[?] O nome de negócio desse registro não está no material: ele guarda apenas o órgão, a
coordenadoria, o tipo de órgão e o mês e o ano de referência, e o documento que descreve a fila
não veio no lote. Pergunta ao site.

### RN-13 — Só parte dos registros reabertos deixa auditoria

Cada reabertura do **mapa do mês**, de cada **registro diário**, do **cardápio da semana** e dos
**gêneros com fornecedor e nota fiscal** grava uma **auditoria** da operação como
**alteração**, com o conteúdo anterior e o posterior, a matrícula de quem reabriu, a estação, a
data e a hora da sessão, o tipo de órgão, a coordenadoria e o **número do processo**, montado
com o órgão, o ano e o mês de referência. Os **registros do mês da geração anterior do mapa** e
as **quantidades de refeições por categoria** são reabertos **sem** auditoria: deles ficam
apenas a situação, a data, a hora e a matrícula gravadas no próprio registro. A criação do
registro da fila (RN-12) é auditada como **inclusão**.

[?] Se a auditoria deveria cobrir o mês inteiro da unidade, e não só esses registros, pergunta
ao site.

### RN-14 — A reabertura exige a permissão de inclusão e passa pela tela, pela estação e pela rota

Ao ser aberta, a tela confere o **cadastro de telas** e a sessão: a estação do servidor tem de
ser a registrada no cadastro dele, e uma requisição marcada como segunda página é recusada.
Antes de reabrir, confere a **rota** — a tela tem de estar cadastrada e não excluída — e a
**permissão**: o cadastro de acessos tem de liberar a **inclusão** para esta tela. Falhando
qualquer conferência, a tela devolve o controle sem reabrir nada, com a mensagem do catálogo. A
opção de manutenção da tela é reposta com a **inclusão** ao abrir, e é essa operação que a
permissão confere.

[?] Esta tela não tem recusa de "opção não disponível": a reabertura não olha a opção, e a
permissão conferida é a da opção que estiver no campo. Se a máscara deixa o servidor trocar
essa opção, a operação que ele autoriza não é a que a tela executa. Pergunta ao site.

### RN-15 — Terminada a reabertura, a tela avisa e o mês só se reabre de novo com nova confirmação

Reaberto o mês, a tela avisa **\* Mapa da Escola reaberto com sucesso \*** ou **\* Mapa da
Creche reaberto com sucesso \***, conforme a unidade, fica na própria tela e descarta o estado
de confirmação: uma nova reabertura exige nova confirmação.

---

## Cenários BDD

```gherkin
Funcionalidade: Reabrir o mapa do mês de referência de um órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a matrícula, o acesso, o tipo de órgão, a coordenadoria e o órgão filho
    E tenho acesso à tela M060T
    E tenho permissão de inclusão nesta tela

  Cenário: O mês de uma escola é reaberto
    Dado que a escola tem o mapa daquele mês fechado
    Quando informo o órgão filho, o mês e o ano de referência e respondo S à confirmação
    Então a situação do mapa do mês e dos registros diários daquela unidade passa a aberta
    E vejo "* Mapa da Escola reaberto com sucesso *"

  Cenário: O mês de uma creche é reaberto
    Dado que o cadastro do órgão o marca como creche e ele tem o mapa daquele mês fechado
    Quando informo o órgão, o mês e o ano e respondo S à confirmação
    Então o mês da creche é reaberto
    E vejo "* Mapa da Creche reaberto com sucesso *"

  Cenário: A reabertura não inclui nem exclui registro do mês
    Dado que confirmei uma reabertura
    Quando o mês é reaberto
    Então nenhum registro do mês é criado
    E nenhum registro é excluído
    E o que muda é a situação dos registros que já existiam e estavam fechados

  Cenário: A reabertura devolve o mês à fila do processamento do mapa
    Dado que a unidade ainda não tem, para aquele mês, o registro que o processamento do mapa usa como fila
    Quando o mês é reaberto
    Então esse registro é criado
    E a criação fica registrada na auditoria como inclusão

  Cenário: Só parte dos registros reabertos deixa auditoria
    Dado que confirmei uma reabertura
    Quando o mês é reaberto
    Então o mapa do mês e cada registro diário reaberto ficam registrados na auditoria como alteração, com o conteúdo anterior e o posterior
    E o mesmo acontece com o cardápio da semana e com cada gênero com fornecedor e nota fiscal reaberto
    E os registros do mês da geração anterior do mapa e as quantidades de refeições por categoria são reabertos sem registro de auditoria

  Cenário: A tela pede confirmação antes de reabrir
    Dado que informei o órgão e o mês de referência e há registro fechado
    Quando a validação termina
    Então vejo "* Confirma reabertura do mapa <S/N> ? *"
    E nada foi reaberto ainda

  Cenário: A confirmação vale para o que foi mostrado
    Dado que a tela pediu a confirmação da reabertura de um mês
    Quando troco o órgão, o ano ou o mês e respondo
    Então a minha resposta é descartada
    E o sistema valida o que está na tela e pede a confirmação outra vez

  Cenário: Responder N não reabre, e a tela volta a perguntar
    Dado que a tela pediu a confirmação da reabertura de um mês
    Quando respondo N
    Então nada é reaberto
    E vejo o mesmo pedido de confirmação outra vez

  Cenário: Sem o órgão filho
    Quando deixo o campo do órgão filho em branco
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é reaberto

  Cenário: Órgão filho não cadastrado
    Quando informo um órgão que não existe no cadastro de órgãos
    Então vejo "* Orgao nao cadastrado *"
    E nada é reaberto

  Cenário: O órgão da própria sessão não está no cadastro
    Dado que o órgão filho que a minha sessão carrega não existe mais no cadastro
    Quando a tela é validada
    Então vejo "* Orgao nao cadastrado *"
    E nada é reaberto

  Cenário: Órgão fora do alcance do servidor
    Dado que a minha sessão carrega um órgão filho
    Quando informo outro órgão
    Então vejo "* Usuario sem acesso a outro orgao *"
    E nada é reaberto

  Cenário: Órgão de outra coordenadoria
    Dado que a minha sessão carrega uma coordenadoria
    Quando informo um órgão de outra coordenadoria
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E nada é reaberto

  Cenário: Órgão de outro tipo de órgão
    Quando informo um órgão que não é da rede da minha secretaria
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E nada é reaberto

  Cenário: Cadastro do órgão incompleto
    Dado que falta no cadastro do órgão o bairro, o órgão pai, o nome, o endereço, os matriculados ou as pessoas
    Quando tento reabrir o mês dele
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E o cursor fica no campo do órgão
    E nada é reaberto

  Cenário: Sem o mês e o ano de referência
    Quando deixo o mês ou o ano de referência em branco
    Então vejo "* Informe Mes/Ano para a reabertura *"
    E o cursor fica no mês
    E nada é reaberto

  Cenário: Mês e ano que não formam uma data do calendário
    Quando informo um mês ou um ano fora do calendário
    Então vejo "* Mes/ano invalido *"
    E o cursor fica no mês
    E nada é reaberto

  Cenário: O período do mês vem da tabela de períodos do mapa
    Dado que informei um mês que existe na tabela de períodos do mapa
    Quando a tela valida o mês
    Então o início e o limite do período aparecem preenchidos com os da tabela
    E o que eu tiver digitado nesses campos é descartado

  Cenário: Mês que não está na tabela de períodos do mapa
    Dado que informei um mês e um ano que a tabela não tem
    Quando a tela valida o mês
    Então ela não recusa
    E os campos do período ficam em branco
    E a reabertura segue, se houver registro fechado da unidade naquele mês

  Cenário: Sem registro fechado para a escola
    Dado que a escola não tem registro fechado naquele mês
    Quando tento reabrir
    Então vejo "* Nao existem reg.fechados para esta Escola *"
    E nada é reaberto

  Cenário: Sem registro fechado para a creche
    Dado que a creche não tem registro fechado naquele mês
    Quando tento reabrir
    Então vejo "* Nao existem reg.fechados para esta Creche *"
    E nada é reaberto

  Cenário: Uma creche com o mapa da geração anterior fechado
    Dado que a creche só tem fechado o mapa do mês da geração anterior
    Quando tento reabrir
    Então a conferência procura esse mapa no cadastro da escola, e não no da creche
    E vejo "* Nao existem reg.fechados para esta Creche *"
    E nada é reaberto

  Cenário: Um mês já reaberto não se reabre duas vezes
    Dado que o mês da unidade já foi reaberto
    Quando tento reabri-lo de novo
    Então vejo o aviso de que não existem registros fechados
    E nada é reaberto

  Cenário: Um registro diário já reaberto no meio do mês
    Dado que há um registro diário já reaberto e outros fechados depois dele
    Quando o mês é reaberto
    Então a varredura para no registro já reaberto
    E os registros diários que vêm depois dele continuam fechados

  Cenário: A reabertura grava quem reabriu, de onde e quando
    Dado que confirmei uma reabertura
    Quando o mês é reaberto
    Então cada registro reaberto que tem esses campos fica com a minha matrícula, a minha estação e a data e a hora da gravação
    E a data de atualização é a do sistema

  Cenário: Sem permissão de inclusão para esta tela
    Dado que o meu cadastro de acessos não libera a inclusão nesta tela
    Quando tento reabrir o mês
    Então vejo "* Acesso negado para esta operacao *"
    E nada é validado e nada é reaberto

  Cenário: Tela não disponível ou fora da rota
    Dado que a tela M060T não está no cadastro de telas, ou está excluída
    Quando ela é aberta
    Então vejo "* Tela nao disponivel *" ou "* Tela nao cadastrada *"
    E nada é validado e nada é reaberto

  Cenário: Acesso negado para esta matrícula
    Dado que o meu cadastro não tem acesso a esta tela
    Quando ela é aberta
    Então vejo "* Acesso negado para esta matricula *"
    E nada é validado e nada é reaberto

  Cenário: A sessão está em outra estação
    Dado que a estação da minha sessão não é a registrada no meu cadastro
    Quando a tela M060T é aberta
    Então o meu acesso é encerrado
    E nada é reaberto

  Cenário: Requisição de segunda página é negada
    Dado que a minha requisição está marcada como página 2
    Quando a tela M060T é aberta
    Então vejo "* Acesso a pagina 2 negado *"
    E nada é reaberto

  Cenário: Depois da reabertura, o estado de confirmação é descartado
    Dado que reabri o mês de uma unidade
    Quando quero reabrir outro mês
    Então preciso de uma nova confirmação

  Cenário: Nada é reaberto antes da confirmação
    Dado que informei o órgão e o mês de referência, e há registro fechado
    Quando não respondo S
    Então nenhum registro do mês muda de situação
    E nenhum registro é criado
    E nenhum rastro de auditoria é deixado
```
