# US — M050T — Fechar o mapa do mês de referência de um órgão filho

## Estória

Como **servidor de CRE**, quero **fechar o mapa do mês de referência de uma unidade da
minha coordenadoria**, para que **o mês daquela unidade fique encerrado — com os
registros marcados como fechados — e ninguém continue lançando ou alterando o que já
passou**.

O mapa é o registro da unidade no mês, e é por ele que a coordenação regional acompanha
o que já foi lançado e o que falta. Enquanto o mês está aberto, a unidade continua
digitando os dias, o cardápio e a merenda; fechar é o que encerra o mês inteiro de uma
vez, para o lançamento parar e o mês poder ser conferido. Como o fechamento encerra um
mês de uma unidade, o sistema não o executa sem antes mostrar o que entendeu e ouvir a
confirmação de quem fechou; e, quando não há nada aberto para aquela unidade naquele mês,
ele não fecha e avisa.

## Contexto

Jornada S000M → M000M → M050T.

Ator: servidor de CRE — fecha o mês de referência de uma unidade (escola ou creche) da
sua coordenadoria regional.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O M000M é um menu e não grava nada:
apenas encaminha. O contexto que a M050T usa — a matrícula, o acesso, o tipo de órgão, a
coordenadoria e o órgão filho do servidor — é o que a entrada deixou na sessão. Esta tela
é o outro lado da M049T: aquela pede a geração do mapa do mês das unidades da
coordenadoria; esta encerra o mês de uma unidade. A jornada termina aqui: depois do
fechamento a tela fica nela mesma.

---

## Regras de negócio

### RN-01 — A tela fecha o mês de uma unidade; não é de consulta nem de manutenção

A M050T não consulta nem mantém cadastro: ela **fecha** o mês de referência de **uma**
unidade. Fechar é trocar a **situação** dos registros daquela unidade naquele mês, de
aberta para fechada: o mapa do mês, os registros diários do mapa, os registros do mês da
geração anterior do mapa e os registros de merenda do mês — o cardápio da semana, os
gêneros com fornecedor e nota fiscal e as quantidades de refeições por categoria. Nada é
incluído e nada é excluído: o que a tela grava é o próprio registro que já existia, com a
situação trocada e, onde o registro tem esses campos, quem fechou, em que estação e
quando.

### RN-02 — O fechamento é confirmado antes de acontecer

Conferido tudo, a tela não fecha: ela mostra
**\* Confirma fechamento do mapa <S/N> ? \*** e espera. Só a resposta **S** leva ao
fechamento, e ela vale para o que estava na tela: se o órgão, o ano ou o mês já não forem
os mesmos, a resposta é descartada, o que está na tela é validado de novo e a mesma
pergunta volta. Qualquer outra resposta, inclusive **N**, não fecha nada e a tela volta a
perguntar.

[?] Responder **N** não cancela o fechamento: não há no programa resposta de cancelamento
e a tela insiste até vir um **S**. Se é o desenho, ou se o ramo ficou sem caminho de
saída, pergunta ao site.

### RN-03 — O órgão filho é obrigatório e tem de existir no cadastro

O servidor diz de quem é o mês informando o **órgão filho** — uma escola ou uma creche.
Sem ele, a recusa é **\* Informe o orgao \***, com o cursor no campo, e nada é validado
depois disso. O órgão é procurado no cadastro de órgãos; não existindo, ou estando
excluído, a recusa é **\* Orgao nao cadastrado \***.

[?] Quando a sessão não traz coordenadoria, a tela admite que o servidor informe a
coordenadoria em vez do órgão, mas exige o órgão logo em seguida, com a mesma mensagem: a
coordenadoria digitada não substitui o órgão. Se a intenção era permitir fechar por
coordenadoria, o caminho não permite. Pergunta ao site.

### RN-04 — O servidor fecha o órgão que a sessão lhe dá, e o órgão tem de ser da sua coordenadoria e do seu tipo de órgão

Se a sessão carrega um **órgão filho**, a tela abre o campo com ele e recusa qualquer
outro: **\* Usuario sem acesso a outro orgao \***. O órgão informado tem ainda de ser do
mesmo **tipo de órgão** da sessão — fora disso, **\* Orgao nao pertence a esta
secretaria \*** — e, quando a sessão tem **coordenadoria**, o órgão tem de ser daquela
coordenadoria: **\* Usuario sem acesso ao grupo deste orgao \***. A coordenadoria
mostrada na tela não é digitada: ela é reposta com a do cadastro do órgão.

[?] Com a sessão sem coordenadoria, a conferência da coordenadoria não roda e o que sobra
é o tipo de órgão. Se isso libera o fechamento de unidades de qualquer coordenadoria da
mesma rede, pergunta ao site.

### RN-05 — O cadastro do órgão tem de estar completo

Antes de fechar, a tela confere **seis** dados do cadastro do órgão: o **bairro**, o
**órgão pai**, o **nome**, o **endereço**, o **número de matriculados** e o **número de
pessoas**. Faltando qualquer um deles, a recusa é
**\* Orgao cadastrado com dados incompletos \***, com o cursor no órgão, e o mês não é
fechado.

[?] Não está no material lido por que o fechamento do mês depende de dados de endereço e
de quantitativos da unidade. Pergunta ao site.

### RN-06 — O mês e o ano de referência são obrigatórios e têm de formar uma data do calendário

Faltando o mês ou o ano, a recusa é **\* Informe Mes/Ano para o fechamento \***, com o
cursor no mês. Informados os dois, o par tem de ser uma data do calendário — o dia 1º
daquele mês —, com o ano entre **1994** e **2099**: fora disso, **\* Mes/ano invalido \***,
também com o cursor no mês.

### RN-07 — O período do mês vem da tabela de períodos do mapa, e não do teclado

Para o mês e o ano informados, a tela lê a **tabela de períodos do mapa** e repõe nos
campos de período o **dia, o mês e o ano do início** e do **limite** do período: o
servidor não informa esses campos, e o que digitar neles é descartado. Existindo o
período, é o **início** dele que separa os registros diários que pertencem ao fechamento.
Não existindo o mês na tabela, a tela **não recusa**: segue com o período em branco.

[?] A tela irmã, que pede a geração do mapa, recusa o mês que não está na tabela de
períodos do mapa. Aqui ele passa. Se a intenção era exigir a tabela também no fechamento,
o caminho não exige. Pergunta ao site.

[?] Sem o período da tabela, o que separa os registros diários do mês fica zerado, e
qualquer registro diário aberto da unidade entra no fechamento. Se é isso que se espera de
um mês que a tabela não tem, pergunta ao site.

### RN-08 — A tela não fecha um mês que não tenha registro aberto

Antes de pedir a confirmação, a tela procura registro **aberto** daquela unidade naquele
mês: o mapa do mês, algum registro diário a partir do início do período, ou os registros
do mês da unidade. Não achando nenhum, a recusa é
**\* Nao existem registros abertos para esta Escola \*** ou
**\* Nao existem registros abertos para esta Creche \***, conforme a unidade seja creche,
e nada é fechado. É por isso que um mês já fechado não se fecha duas vezes: ele deixa de
ter registro aberto.

### RN-09 — Escola e creche não têm os mesmos registros do mês

A unidade é tratada como **creche** quando o cadastro do órgão a marca assim, e como
**escola** em qualquer outro caso. O mapa do mês, os registros diários, o cardápio da
semana e os gêneros com fornecedor e nota fiscal são fechados nos dois casos; os
**registros do mês da geração anterior do mapa** e as **quantidades de refeições por
categoria** existem em cadastros separados para escola e para creche, e a tela fecha o do
tipo da unidade. A mensagem final diz qual dos dois foi fechado.

[?] O único valor que a tela distingue é a marca de creche; qualquer outro valor do campo
cai no caso "escola", e o que o campo aceita além da marca não está no material lido.
Pergunta ao site.

### RN-10 — O fechamento dos registros diários percorre o mês a partir do limite do período e para no primeiro registro que não esteja aberto

O mapa do mês é fechado direto, achado que seja. Os registros diários são percorridos em
sequência: a leitura começa posicionada no **limite** do período e fecha cada registro
aberto daquela unidade cuja data não seja anterior ao **início** do período, até encontrar
um registro que não seja daquela unidade, daquela coordenadoria ou daquele estado — e para
ali.

[?] A leitura começa no limite do período, mas a conferência aceita qualquer data a partir
do início: o início não barra nada que a leitura já não tivesse deixado de fora. Se o
fechamento deveria alcançar os dias anteriores ao limite, o caminho não os alcança.
Pergunta ao site.

[?] A varredura para no primeiro registro que não esteja aberto: um registro já fechado no
meio do mês deixa os seguintes abertos. Se é intenção fechar por blocos ou se é defeito,
pergunta ao site.

### RN-11 — Só o mapa e os registros diários deixam auditoria

Cada fechamento do mapa do mês e de cada registro diário grava uma **auditoria** da
operação como **alteração**, com o conteúdo anterior e o posterior, a matrícula de quem
fechou, a estação, a data e a hora da sessão, o tipo de órgão, a coordenadoria e o
**número do processo**, montado com o órgão, o ano e o mês de referência. Os registros do
mês da merenda e o da geração anterior do mapa são fechados **sem** auditoria: deles
ficam apenas a situação, a data, a hora e a matrícula gravadas no próprio registro.

[?] Se a auditoria deveria cobrir o mês inteiro da unidade, e não só o mapa do mês e os
registros diários, pergunta ao site.

### RN-12 — O fechamento exige a permissão de inclusão e passa pela tela, pela estação e pela rota

Ao ser aberta, a tela confere o **cadastro de telas** e a sessão: a estação do servidor
tem de ser a registrada no cadastro dele, e uma requisição marcada como segunda página é
recusada. Antes de fechar, confere a **rota** — a tela tem de estar cadastrada e não
excluída — e a **permissão**: o cadastro de acessos tem de liberar a **inclusão** para
esta tela. Falhando qualquer conferência, a tela devolve o controle sem fechar nada, com a
mensagem do catálogo. A opção de manutenção da tela é reposta com a **inclusão** ao abrir,
e é essa operação que a permissão confere.

[?] Esta tela não tem recusa de "opção não disponível": o fechamento não olha a opção, e a
permissão conferida é a da opção que estiver no campo. Se a máscara deixa o servidor
trocar essa opção, a operação que ele autoriza não é a que a tela executa. Pergunta ao
site.

### RN-13 — Terminado o fechamento, a tela avisa e o mês só se fecha de novo com nova confirmação

Fechado o mês, a tela avisa **\* Mapa da Escola fechado com sucesso \*** ou
**\* Mapa da Creche fechado com sucesso \***, conforme a unidade, fica na própria tela e
descarta o estado de confirmação: um novo fechamento exige nova confirmação.

---

## Cenários BDD

```gherkin
Funcionalidade: Fechar o mapa do mês de referência de um órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a matrícula, o acesso, o tipo de órgão, a coordenadoria e o órgão filho
    E tenho acesso à tela M050T
    E tenho permissão de inclusão nesta tela

  Cenário: O mês de uma escola é fechado
    Dado que a unidade tem o mapa daquele mês aberto
    Quando informo o órgão filho, o mês e o ano de referência e respondo S à confirmação
    Então a situação do mapa do mês e dos registros diários daquela unidade passa a fechada
    E vejo "* Mapa da Escola fechado com sucesso *"

  Cenário: O mês de uma creche é fechado
    Dado que o cadastro do órgão o marca como creche e ele tem o mapa daquele mês aberto
    Quando informo o órgão, o mês e o ano e respondo S à confirmação
    Então o mês da creche é fechado
    E vejo "* Mapa da Creche fechado com sucesso *"

  Cenário: O fechamento não inclui nem exclui registro nenhum
    Dado que confirmei um fechamento
    Quando o mês é fechado
    Então nenhum registro do mês é criado
    E nenhum registro é excluído
    E o que muda é a situação dos registros que já existiam e estavam abertos

  Cenário: Só o mapa e os registros diários deixam auditoria
    Dado que confirmei um fechamento
    Quando o mês é fechado
    Então o mapa do mês e cada registro diário fechado ficam registrados na auditoria como alteração, com o conteúdo anterior e o posterior
    E os demais registros do mês são fechados sem registro de auditoria

  Cenário: A tela pede confirmação antes de fechar
    Dado que informei o órgão e o mês de referência e há registro aberto
    Quando a validação termina
    Então vejo "* Confirma fechamento do mapa <S/N> ? *"
    E nada foi fechado ainda

  Cenário: A confirmação vale para o que foi mostrado
    Dado que a tela pediu a confirmação do fechamento de um mês
    Quando troco o órgão, o ano ou o mês e respondo
    Então a minha resposta é descartada
    E o sistema valida o que está na tela e pede a confirmação outra vez

  Cenário: Responder N não fecha, e a tela volta a perguntar
    Dado que a tela pediu a confirmação do fechamento de um mês
    Quando respondo N
    Então nada é fechado
    E vejo o mesmo pedido de confirmação outra vez

  Cenário: Sem o órgão filho
    Quando deixo o campo do órgão filho em branco
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é fechado

  Cenário: Órgão filho não cadastrado
    Quando informo um órgão que não existe no cadastro de órgãos
    Então vejo "* Orgao nao cadastrado *"
    E nada é fechado

  Cenário: Órgão fora do alcance do servidor
    Dado que a minha sessão carrega um órgão filho
    Quando informo outro órgão
    Então vejo "* Usuario sem acesso a outro orgao *"
    E nada é fechado

  Cenário: Órgão de outra coordenadoria
    Dado que a minha sessão carrega uma coordenadoria
    Quando informo um órgão de outra coordenadoria
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E nada é fechado

  Cenário: Órgão de outro tipo de órgão
    Quando informo um órgão que não é da rede da minha secretaria
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E nada é fechado

  Cenário: Cadastro do órgão incompleto
    Dado que falta no cadastro do órgão o bairro, o órgão pai, o nome, o endereço, os matriculados ou as pessoas
    Quando tento fechar o mês dele
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E o cursor fica no campo do órgão
    E nada é fechado

  Cenário: Sem o mês e o ano de referência
    Quando deixo o mês ou o ano de referência em branco
    Então vejo "* Informe Mes/Ano para o fechamento *"
    E o cursor fica no mês
    E nada é fechado

  Cenário: Mês e ano que não formam uma data do calendário
    Quando informo um mês ou um ano fora do calendário
    Então vejo "* Mes/ano invalido *"
    E o cursor fica no mês
    E nada é fechado

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
    E o fechamento segue, se houver registro aberto da unidade naquele mês

  Cenário: Sem registro aberto para a escola
    Dado que a unidade não tem mapa aberto naquele mês
    Quando tento fechar
    Então vejo "* Nao existem registros abertos para esta Escola *"
    E nada é fechado

  Cenário: Sem registro aberto para a creche
    Dado que a creche não tem mapa aberto naquele mês
    Quando tento fechar
    Então vejo "* Nao existem registros abertos para esta Creche *"
    E nada é fechado

  Cenário: Um mês já fechado não se fecha duas vezes
    Dado que o mês da unidade já foi fechado
    Quando tento fechá-lo de novo
    Então vejo o aviso de que não existem registros abertos
    E nada é fechado

  Cenário: Um registro diário já fechado no meio do mês
    Dado que há um registro diário já fechado e outros abertos depois dele
    Quando o mês é fechado
    Então a varredura para no registro já fechado
    E os registros diários que vêm depois dele continuam abertos

  Cenário: Sem permissão de inclusão para esta tela
    Dado que o meu cadastro de acessos não libera a inclusão nesta tela
    Quando tento fechar o mês
    Então vejo "* Acesso negado para esta operacao *"
    E nada é validado e nada é fechado

  Cenário: Tela não disponível ou fora da rota
    Dado que a tela M050T não está no cadastro de telas, ou está excluída
    Quando ela é aberta
    Então vejo "* Tela nao disponivel *" ou "* Tela nao cadastrada *"
    E nada é validado e nada é fechado

  Cenário: Acesso negado para esta matrícula
    Dado que o meu cadastro não tem acesso a esta tela
    Quando ela é aberta
    Então vejo "* Acesso negado para esta matricula *"
    E nada é validado e nada é fechado

  Cenário: A sessão está em outra estação
    Dado que a estação da minha sessão não é a registrada no meu cadastro
    Quando a tela M050T é aberta
    Então o meu acesso é encerrado
    E nada é fechado

  Cenário: Requisição de segunda página é negada
    Dado que a minha requisição está marcada como página 2
    Quando a tela M050T é aberta
    Então vejo "* Acesso a pagina 2 negado *"
    E nada é fechado

  Cenário: Depois do fechamento, o estado de confirmação é descartado
    Dado que fechei o mês de uma unidade
    Quando quero fechar outro mês
    Então preciso de uma nova confirmação

  Cenário: Nada é fechado antes da confirmação
    Dado que informei o órgão e o mês de referência, e há registro aberto
    Quando não respondo S
    Então nenhum registro do mês muda de situação
```
