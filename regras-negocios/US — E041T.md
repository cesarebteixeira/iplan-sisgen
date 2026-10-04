# US — E041T — Alteração do fornecedor, do período e da semana do pedido de alimentação escolar

## Estória

Como **servidor de CRE**, quero **corrigir o fornecedor, o período de entrega e a semana de
um pedido de alimentação escolar que ainda não foi aprovado**, para que **o pedido siga para
distribuição e aprovação com o fornecedor certo e com os dias de entrega certos, sem perder
os gêneros que ele já tem**.

O pedido de alimentação escolar nasce com o órgão, o fornecedor, o período e os dias em que
a entrega deve acontecer, e é por esses dias que os gêneros e as quantidades são
distribuídos. Quando o fornecedor sai trocado, quando o período não fecha com a semana de
entrega ou quando a semana do cardápio está errada, o pedido não pode seguir — e excluí-lo
levaria junto todos os gêneros que ele já tem, obrigando a redigitar item por item. Esta
tela acerta esses três dados no próprio pedido e leva o período novo a todos os gêneros
dele, sem mexer no número, no órgão, na coordenadoria, no ano da entrega nem na situação.

A alteração não é silenciosa: a tela confere tudo antes, pergunta e só grava depois da
resposta — e cada pedido e cada gênero que ela toca deixa registro para auditoria.

## Contexto

Jornada S000M → E000M → E010M → E041T.
Ator: servidor de CRE — informa o órgão, a coordenadoria regional escolar, o número do
pedido e o ano da entrega, corrige o fornecedor, o período de entrega e a semana, e
confirma a alteração.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As duas telas que antecedem esta na jornada, o `E000M` e o `E010M`, são **menus**: chega-se
aqui por uma opção do `E010M`, e de um passo para o outro nada é passado — nem registro, nem
operação. O que esta tela usa vem todo da entrada: o tipo de órgão (a secretaria), a
coordenadoria regional escolar e o órgão filho do vínculo do servidor, além da matrícula.
Esta tela **não muda de comportamento conforme a tela que a abriu** — não há, nela,
comparação com a tela de origem — e ela não encadeia em outra tela ao terminar.

O que ela entrega é a si própria: depois de conferir, ela **se reabre** com o pedido em tela
e com a marca de que está esperando a resposta à pergunta de confirmação (RN-16). É nessa
passagem — o pedido e a resposta pendente — que a alteração se completa; sem ela, quem lê a
estória isolada não tem como reproduzir a confirmação.

As regras abaixo são só as desta tela.

## Regras de negócio

### RN-01 — Esta tela é de alteração, e de mais nada

Nesta tela só existe uma operação: **alterar**. Ao ser aberta, ela já se apresenta com a
alteração no campo da operação, e não inclui pedido, não exclui pedido e não serve para
consultar.

Chegando ao campo da operação qualquer outra das operações conhecidas — a consulta, a
inclusão, a exclusão —, ou o campo em branco, a recusa é
**\* Opcao nao disponivel. Use ALT \***, com o cursor de volta nesse campo, antes de
qualquer leitura de pedido; nada é gravado. Uma operação que não seja nenhuma das quatro
conhecidas é recusada antes disso, com **\* Operacao nao disponivel \***.

[?] A mensagem manda usar "ALT", mas a conferência desta tela é contra o código interno da
alteração, e é a própria tela que põe esse código no campo na abertura; o que o servidor
digita nesse campo, e se o rótulo que a máscara mostra é "ALT", não está no lote. Pergunta
ao site.

### RN-02 — A abertura da tela não procura pedido

Ao ser aberta, a tela mostra a data do sistema e a descrição da secretaria da sessão; põe
no órgão filho e na coordenadoria regional escolar os valores do vínculo do servidor, e
procura no cadastro de órgãos somente o nome desse órgão do vínculo, para exibi-lo. Nenhum
pedido é lido, gravado ou apagado nessa abertura. O cursor começa no número do pedido quando
o vínculo traz coordenadoria; quando o vínculo não traz coordenadoria nem órgão, o cursor
fica no campo do órgão.

[?] Quando o vínculo traz órgão filho e não traz coordenadoria, esta tela não posiciona o
cursor em campo nenhum; se o quadro comum o posiciona, o acervo lido não mostra. Pergunta ao
site.

### RN-03 — Os campos numéricos passam por edição antes das conferências

**Onze** campos desta tela são tratados como número: o órgão filho, a coordenadoria regional
escolar, o número do pedido, o ano da entrega, o fornecedor e as seis partes do período de
entrega (dia, mês e ano do início; dia, mês e ano do limite). O que vier em branco vira
zero, os zeros à esquerda são descartados e o que não for número é recusado, com o cursor de
volta ao campo. Nenhuma conferência de pedido acontece antes dessa edição.

[?] A rotina que faz essa edição não faz parte dos fontes lidos, e a coordenadoria regional
escolar é o único dos onze campos sem posição de cursor definida por esta tela: recusada a
digitação dela, o cursor não é levado até lá. O acervo lido também não mostra se a edição
interrompe a passagem ou apenas corrige o valor e segue. Pergunta ao site.

### RN-04 — O pedido é identificado pela secretaria, pelo órgão, pela coordenadoria e por um código de dez dígitos

Dentro de uma secretaria (o tipo de órgão), um pedido é identificado pelo órgão filho, pela
coordenadoria regional escolar e por um código de **dez dígitos** formado pelo número do
pedido (seis) e pelo ano da entrega (quatro). O número sozinho não identifica nada: o mesmo
número pode existir em anos de entrega e em coordenadorias diferentes.

O número e o ano são digitados em campos separados, e é a tela que os junta num código; ao
reabrir, é ela que os separa de novo. Quando o vínculo do servidor traz órgão filho e
coordenadoria, é esse o recorte da procura. Quando não traz, o servidor informa o órgão — e
a coordenadoria que a tela usa é a do cadastro desse órgão, não a que ele digitou. A
coordenadoria digitada só vale quando o órgão não é informado.

### RN-05 — O órgão filho é conferido contra o vínculo e contra o cadastro

Se o vínculo do servidor traz um órgão filho e o órgão informado é outro, a recusa é
**\* Usuario sem acesso a outro orgao \***, com o cursor no campo do órgão. Se o vínculo não
traz coordenadoria e nem o órgão nem a coordenadoria foram informados, a recusa é
**\* Informe o orgao \***, também com o cursor no campo do órgão.

Informado o órgão, ele ainda tem de passar por quatro conferências no cadastro de órgãos,
todas com o cursor no campo do órgão e sem gravar nada: não existir, ou estar marcado como
excluído, dá **\* Orgao nao cadastrado \***; estar cadastrado sem bairro, sem órgão pai, sem
nome, sem endereço, sem número de matrículas ou sem número de pessoas dá
**\* Orgao cadastrado com dados incompletos \***; ser de um tipo de órgão diferente do da
sessão dá **\* Orgao nao pertence a esta secretaria \***; e ser de uma coordenadoria
diferente da do vínculo dá **\* Usuario sem acesso ao grupo deste orgao \***.

[?] A tela tem ainda uma recusa **\* Orgao nao cadastrado \*** que compara o nome do órgão
guardado com o marcador "NAO CADASTRADO", e nenhuma linha desta tela grava esse marcador: o
nome guardado só recebe o nome de um órgão encontrado no cadastro, ou fica em branco. Ou
essa recusa vale para um caso que esta tela não alcança, ou o marcador vem de fora. Pergunta
ao site.

### RN-06 — O pedido tem de existir e não pode estar aprovado nem excluído

Sem o número do pedido (número e ano zerados), a recusa é
**\* Informe o numero do pedido \***, com o cursor no número do pedido. Procurando o pedido
pela secretaria, pela coordenadoria e pelo código de dez dígitos, se ele não estiver
cadastrado a recusa é **\* Pedido nao cadastrado \***, também com o cursor no número do
pedido.

Achado o pedido, quatro situações são recusadas, todas com o cursor no número do pedido:
pedido excluído dá **\* Pedido excluido \***; pendente de distribuição dá
**\* Pedido pendente de distribuicao \***; aprovado e fechado dá
**\* Pedido aprovado - fechado \***; e aprovado e em aberto dá
**\* Pedido aprovado - em aberto \***. Na prática, só o pedido que ainda não foi aprovado
pode ser alterado por esta tela.

### RN-07 — Um pedido que já tem gênero com tipo de contrato não é alterado aqui

A tela percorre os gêneros do pedido; se algum deles já tem tipo de contrato, a alteração é
recusada com **\* Ja existem generos com tipo de contrato \***, com o cursor no número do
pedido. É o tipo de contrato no gênero que barra, mesmo que a alteração pretendida seja só
de datas.

### RN-08 — Ao menos um campo de alteração tem de ser informado

Se o fornecedor, as seis partes do período e a semana vierem todos em branco, a recusa é
**\* Informe os campos a alterar \***, com o cursor no fornecedor: a tela não aceita uma
alteração sem nada a alterar.

O que for deixado em branco é completado com o que o pedido já tem — o fornecedor, a semana
e as duas datas do período. Cada data é completada por inteiro, as três partes de uma vez:
informada só uma parte de uma data, a tela usa o que foi digitado e o resto fica zerado, e a
data não passa nas conferências seguintes.

### RN-09 — O fornecedor informado tem de existir

Informado o fornecedor, ele tem de estar no cadastro de fornecedores; não estando, a recusa
é **\* Fornecedor nao cadastrado \***, com o cursor no fornecedor. Não informado, vale o
fornecedor que o pedido já tem. Achado o fornecedor, a tela mostra a razão social dele.

### RN-10 — As duas datas do período de entrega e o ano da entrega são conferidos um a um

A data de início é conferida primeiro, com o cursor no campo do início: data impossível, ou
com o ano fora da faixa que o sistema aceita, dá **\* Data de inicio da entrega invalida \***;
ano diferente do ano da entrega informado dá
**\* Ano da entrega difere do ano do pedido \***; cair em sábado dá
**\* Inicio da entrega nao deve ser um sabado \***; em domingo,
**\* Inicio da entrega nao deve ser um domingo \***; e em feriado,
**\* Inicio da entrega nao deve ser um feriado \***.

Depois é a data limite, com o cursor no campo do limite: data impossível dá
**\* Data final da entrega invalida \***; sábado, domingo e feriado dão
**\* Final da entrega nao deve ser um sabado \***,
**\* Final da entrega nao deve ser um domingo \*** e
**\* Final da entrega nao deve ser um feriado \***; e ser anterior ao início dá
**\* Data final menor que a data inicial \***, com o cursor de volta ao início.

Os feriados considerados são os da secretaria (o tipo de órgão) da sessão. As datas não
informadas são as do pedido.

### RN-11 — O período de entrega não pode passar de cinco dias úteis

A partir do início, a tela anda dia a dia na direção do limite, pula sábados, domingos e
feriados da secretaria — os mesmos que ela recusou nas duas datas — e recolhe as datas de
entrega do período. Se forem precisos mais de **cinco** dias úteis, a recusa é
**\* Periodo de entrega nao pode ultrapassar 5 dias \***, com o cursor no início. São essas
datas de entrega que a alteração leva aos gêneros do pedido.

### RN-12 — A semana do cardápio vai de A a E

A semana não informada é a do pedido. Fora de A, B, C, D ou E, a recusa é
**\* Informe semana com A / B / C / D / E \***, com o cursor no campo da semana.

[?] A semana **E** é tratada como um grupo à parte: quando a semana informada é E, a tela
só compara o período com outros pedidos de semana E; quando é de A a D, ela ignora os
pedidos de semana E. Não se conclui do acervo lido o que a semana E significa no negócio, e
essa separação também aparece na limpeza e nas recusas da RN-13 e da RN-14. Pergunta ao
site.

### RN-13 — Ao alterar, a tela apaga do cadastro os pedidos já excluídos do mesmo fornecedor e da mesma data de início

Enquanto confere, a tela varre os pedidos do mesmo órgão, do mesmo fornecedor e da mesma
data de início informada e **apaga definitivamente do cadastro** — não é só um efeito de
tela — os que já estão marcados como excluídos, junto com todos os gêneros deles. Cada
pedido e cada gênero apagados deixam registro para auditoria.

[?] Essa limpeza acontece na passagem de conferência, antes da pergunta de confirmação e
antes de qualquer gravação da alteração. Se a alteração for recusada depois disso, ou se o
servidor não confirmar, a limpeza já foi feita. O acervo lido não diz se a transação é
desfeita quando a tela recusa. Pergunta ao site.

### RN-14 — Um pedido do mesmo fornecedor no mesmo período impede a alteração

Ainda na varredura, se existir outro pedido do mesmo órgão, do mesmo fornecedor e da mesma
data de início informada, e que **não** esteja excluído, a alteração é recusada mostrando o
número e o ano da entrega desse outro pedido: **\* <- Dados cadastrados neste pedido \***;
se ele já estiver aprovado e em aberto, **\* <- Pedido aprovado - em aberto \***; se já
estiver aprovado e fechado, **\* <- Pedido aprovado - fechado \***. O cursor vai para o
campo da operação.

Depois, a tela procura os períodos que se encostam: se existe um pedido do mesmo fornecedor
começando no dia anterior ao início informado e ainda em entrega, ou começando no dia
seguinte ao início informado e dentro do período informado, a recusa é
**\* Ja existe pedido neste intervalo de entrega \***, com o número e o ano do outro pedido,
e o cursor no início.

[?] Um pedido em situação **pendente de distribuição** na mesma data de início não dispara
nenhuma dessas recusas: a tela o deixa passar. Como essa é justamente uma das situações que
a RN-06 recusa no pedido que está sendo alterado, não se conclui do acervo se a passagem é
intencional. Pergunta ao site.

[?] A conferência de choque de período só consulta os pedidos que começam exatamente um dia
antes ou um dia depois do início informado, e para cada uma dessas duas datas considera
apenas o primeiro pedido que encontra. Um pedido de período mais longo, que comece antes e
ainda esteja em entrega, pode passar por ela. Pergunta ao site.

### RN-15 — Não se tira um dia de entrega que já tem quantidade lançada

Ao recalcular as datas de entrega, a tela percorre os gêneros do pedido: se o período novo
deixa de usar um dia em que aquele gênero já tem quantidade lançada, a alteração é recusada
com **\* Nao diminua dias entrega. Ja existem quant.cad.\***, com o cursor no campo da data
limite.

### RN-16 — A tela pergunta antes de gravar, e só o "S" grava

Passando todas as conferências, a tela reabre com a pergunta
**\* Confirma alteracao do pedido <S/N> ? \***, com o cursor no campo da resposta, e o pedido
em tela. Nada é gravado nessa passagem; é a marca da resposta pendente que faz a gravação
acontecer na passagem seguinte.

Respondendo "S", e não tendo mudado nada nos campos desde a pergunta, a tela grava. Qualquer
outra resposta — inclusive em branco — desfaz a marca e
**não grava**: a tela confere tudo de novo e volta a perguntar. Se, entre a pergunta e a
resposta, o servidor mudar qualquer um dos campos do pedido, do fornecedor, do período ou da
semana, a confirmação é desfeita e a tela confere tudo de novo antes de perguntar outra vez.

### RN-17 — Confirmando, o período novo vai para os gêneros e o resto para o pedido

Respondendo "S", a tela regrava, um a um, todos os gêneros do pedido com as novas datas de
entrega e, em seguida, o próprio pedido: o fornecedor, as duas datas do período, a semana e
a data de digitação. Quando o novo início é anterior à data de digitação que o pedido tinha,
é o novo início que passa a valer como data de digitação.

O número do pedido, o órgão, a coordenadoria, o ano da entrega, a situação e os demais dados
do pedido não mudam, e nenhum cadastro é criado por esta tela. Ao terminar, a tela se limpa
e avisa **\* Pedido alterado com sucesso \***.

[?] A matrícula de quem digitou é gravada sempre com a do servidor que está alterando, mas o
registro de auditoria do pedido continua dizendo que o digitador é o anterior, salvo quando
o novo início é anterior à data de digitação. O acervo lido não diz qual dos dois é o
digitador do pedido depois da alteração. Pergunta ao site.

### RN-18 — Tudo o que a tela altera ou apaga fica registrado

Cada gênero regravado, o pedido alterado e cada pedido (com os gêneros dele) apagado na
limpeza da RN-13 deixam um registro de auditoria com a tela de origem, o cadastro atingido,
a operação, a coordenadoria, o número do pedido, a matrícula do servidor, a estação, a
secretaria, a data e a hora da sessão, e os valores de antes e de depois. Informar os dados,
ver a pergunta e responder "N" não geram registro.

[?] Todo registro de auditoria desta tela leva a marca de manutenção fixa da inclusão — a
mesma na alteração e na exclusão —, embora a operação gravada seja a que a tela executou. O
que essa marca significa não está no acervo lido. Pergunta ao site.

### RN-19 — Sem autorização para a tela ou para a operação, nada acontece

A tela só abre se ela própria estiver no cadastro de telas; não estando, a recusa é
**\* Tela nao cadastrada \*** e a tela é abandonada. Ela só abre também para o código de
acesso que a tem no cadastro de telas por código de acesso; não tendo, a recusa é
**\* Acesso negado para esta matricula \*** e o acesso termina ali.

E, antes de qualquer leitura de pedido, a operação de alteração tem de estar liberada para
aquele código de acesso naquela tela; não estando, a recusa é
**\* Acesso negado para esta operacao \***. Nos dois casos nada é gravado.

## Cenários BDD

```gherkin
Funcionalidade: Alteração do fornecedor, do período e da semana do pedido de alimentação escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E041T

  Cenário: Alterar o fornecedor, o período e a semana de um pedido
    Dado que existe um pedido ainda não aprovado, com gêneros, na minha coordenadoria
    E que nenhum gênero dele tem tipo de contrato
    Quando informo o órgão, a coordenadoria, o número do pedido e o ano da entrega
    E informo o fornecedor novo, o período novo e a semana nova
    Então a tela reabre mostrando os dados do pedido e a pergunta de confirmação
    Quando respondo "S"
    Então todos os gêneros do pedido passam a ter as novas datas de entrega
    E o pedido passa a ter o fornecedor, o período e a semana informados
    E o número, o órgão, a coordenadoria, o ano da entrega e a situação não mudam
    E vejo "* Pedido alterado com sucesso *"

  Cenário: Informar os dados e ver a pergunta não grava nada
    Dado que existe um pedido que passa por todas as conferências
    Quando informo os campos a alterar
    Então vejo os dados do pedido e a pergunta de confirmação
    E nada foi gravado: o pedido e os gêneros continuam como estavam
    E nenhum registro de auditoria foi gerado

  Cenário: Responder outra coisa que não "S"
    Dado que a tela já me pediu a confirmação
    Quando respondo algo diferente de "S", inclusive em branco
    Então a alteração não acontece
    E a tela confere tudo de novo e volta a pedir a confirmação

  Cenário: Mudar um campo depois da pergunta
    Dado que a tela já me pediu a confirmação
    Quando mudo o fornecedor, o período, a semana ou o próprio pedido e respondo "S"
    Então a confirmação é desfeita
    E a tela confere tudo de novo
    E, estando os dados corretos, me pergunta outra vez
    E nada foi gravado

  Cenário: A abertura da tela não procura pedido nem grava
    Dado que o meu vínculo tem órgão filho e coordenadoria
    Quando abro a tela E041T
    Então o campo do órgão vem preenchido com o órgão do meu vínculo
    E o campo da coordenadoria vem preenchido com a coordenadoria do meu vínculo
    E o cursor fica no número do pedido
    E vejo a data do sistema, a descrição da secretaria e o nome do meu órgão
    E nenhum pedido é procurado, gravado ou apagado

  Cenário: A abertura sem órgão e sem coordenadoria no vínculo
    Dado que o meu vínculo não tem órgão filho nem coordenadoria
    Quando abro a tela E041T
    Então o campo do órgão fica em branco, para eu informar
    E o cursor fica no campo do órgão
    E nenhum pedido é procurado, gravado ou apagado

  Cenário: Operação diferente da alteração
    Quando informo a consulta, a inclusão ou a exclusão no campo da operação e confirmo
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo da operação
    E nenhum pedido é procurado, gravado ou apagado

  Cenário: Operação desconhecida
    Quando informo uma operação que não é nenhuma das quatro conhecidas
    Então vejo "* Operacao nao disponivel *"
    E nada é gravado

  Cenário: A edição numérica dos campos
    Dado que estou na tela E041T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências
    E a digitação que não é número é recusada, com o cursor de volta ao campo

  Cenário: O servidor não altera pedido de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo outro órgão e confirmo
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Sem órgão e sem coordenadoria no vínculo, o órgão é obrigatório
    Dado que o meu vínculo não tem órgão filho nem coordenadoria
    Quando confirmo sem informar o órgão e sem informar a coordenadoria
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão não cadastrado
    Quando informo um órgão que não está cadastrado, ou que está marcado como excluído
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão com cadastro incompleto
    Dado que o órgão informado não tem bairro, órgão pai, nome, endereço, número de
      matrículas ou número de pessoas
    Quando confirmo
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão de outra secretaria
    Dado que o órgão informado é de um tipo de órgão diferente do da minha sessão
    Quando confirmo
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão de outra coordenadoria
    Dado que o meu vínculo carrega uma coordenadoria
    Quando informo um órgão cadastrado em outra coordenadoria e confirmo
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: A coordenadoria digitada não sobrepõe a do cadastro do órgão
    Dado que o meu vínculo não tem coordenadoria
    Quando informo um órgão cadastrado em uma coordenadoria e digito outra
    Então a tela procura o pedido pela coordenadoria do cadastro do órgão
    E a coordenadoria digitada é descartada

  Cenário: O número do pedido é obrigatório
    Quando confirmo com o número do pedido e o ano da entrega zerados
    Então vejo "* Informe o numero do pedido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido não cadastrado
    Quando informo um pedido que não existe para o órgão e a coordenadoria
    Então vejo "* Pedido nao cadastrado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido excluído
    Dado que o pedido está marcado como excluído
    Quando confirmo a alteração
    Então vejo "* Pedido excluido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido pendente de distribuição
    Dado que o pedido está pendente de distribuição
    Quando confirmo a alteração
    Então vejo "* Pedido pendente de distribuicao *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido aprovado e fechado
    Dado que o pedido está aprovado e fechado
    Quando confirmo a alteração
    Então vejo "* Pedido aprovado - fechado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido aprovado e em aberto
    Dado que o pedido está aprovado e em aberto
    Quando confirmo a alteração
    Então vejo "* Pedido aprovado - em aberto *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Gênero do pedido já com tipo de contrato
    Dado que um dos gêneros do pedido já tem tipo de contrato
    Quando confirmo a alteração
    Então vejo "* Ja existem generos com tipo de contrato *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Nenhum campo a alterar
    Dado que o pedido passa pelas conferências
    Quando confirmo sem informar o fornecedor, o período e a semana
    Então vejo "* Informe os campos a alterar *"
    E o cursor fica no fornecedor
    E nada é gravado

  Cenário: Fornecedor não cadastrado
    Quando informo um fornecedor que não está no cadastro e confirmo
    Então vejo "* Fornecedor nao cadastrado *"
    E o cursor fica no fornecedor
    E nada é gravado

  Cenário: Data de início impossível ou em ano diferente
    Quando informo um dia que não existe no mês, ou um ano fora da faixa aceita
    Então vejo "* Data de inicio da entrega invalida *"
    E o cursor fica no início do período
    Quando informo um início em ano diferente do ano da entrega do pedido
    Então vejo "* Ano da entrega difere do ano do pedido *"
    E nada é gravado

  Cenário: Início em sábado, domingo ou feriado
    Quando informo um início que cai em sábado, domingo ou feriado da secretaria
    Então vejo "* Inicio da entrega nao deve ser um sabado *",
      "* Inicio da entrega nao deve ser um domingo *" ou
      "* Inicio da entrega nao deve ser um feriado *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: Data final impossível, anterior ao início, ou em dia não útil
    Quando informo uma data final impossível
    Então vejo "* Data final da entrega invalida *"
    E o cursor fica no limite do período
    Quando informo uma data final anterior ao início
    Então vejo "* Data final menor que a data inicial *"
    E o cursor volta ao início do período
    Quando informo um limite que cai em sábado, domingo ou feriado da secretaria
    Então vejo "* Final da entrega nao deve ser um sabado *",
      "* Final da entrega nao deve ser um domingo *" ou
      "* Final da entrega nao deve ser um feriado *"
    E o cursor fica no limite do período
    E nada é gravado

  Cenário: Período com mais de cinco dias úteis
    Quando informo um período que exige mais de cinco dias úteis
    Então vejo "* Periodo de entrega nao pode ultrapassar 5 dias *"
    E o cursor fica no início do período
    E nada é gravado

  Cenário: Semana fora de A, B, C, D e E
    Quando informo uma semana diferente de A, B, C, D e E e confirmo
    Então vejo "* Informe semana com A / B / C / D / E *"
    E o cursor fica no campo da semana
    E nada é gravado

  Cenário: Já existe outro pedido do mesmo fornecedor na mesma data de início
    Dado que existe outro pedido do mesmo órgão, do mesmo fornecedor e da mesma data de
      início, não excluído
    Quando confirmo a alteração
    Então vejo "* <- Dados cadastrados neste pedido *" com o número e o ano do outro
      pedido
    E o cursor vai para o campo da operação
    E nada é gravado

  Cenário: O outro pedido já aprovado
    Dado que o outro pedido do mesmo fornecedor e da mesma data de início está aprovado
    Quando confirmo a alteração
    Então vejo "* <- Pedido aprovado - em aberto *" ou
      "* <- Pedido aprovado - fechado *" com o número e o ano do outro pedido
    E nada é gravado

  Cenário: Pedido encostando no período informado
    Dado que existe um pedido do mesmo fornecedor começando no dia anterior ao início
      informado e ainda em entrega
    Quando confirmo a alteração
    Então vejo "* Ja existe pedido neste intervalo de entrega *" com o número e o ano
      desse pedido
    E o cursor fica no início do período
    E nada é gravado

  Cenário: Tirar um dia de entrega que já tem quantidade lançada
    Dado que um gênero do pedido já tem quantidade lançada em um dia que o período novo
      deixa de usar
    Quando confirmo a alteração
    Então vejo "* Nao diminua dias entrega. Ja existem quant.cad.*"
    E o cursor fica no limite do período
    E nada é gravado

  Cenário: A alteração apaga os pedidos já excluídos do mesmo fornecedor e data
    Dado que existe um pedido do mesmo órgão, do mesmo fornecedor e da mesma data de
      início, marcado como excluído, com gêneros
    Quando confirmo a alteração de outro pedido
    Então os gêneros desse pedido excluído são apagados do cadastro
    E o pedido excluído também é apagado do cadastro
    E cada um deles deixa registro de auditoria
    E o pedido alterado continua no cadastro

  Cenário: Sem autorização para a tela ou para a operação
    Dado que esta tela não está no cadastro de telas
    Quando abro a tela E041T
    Então vejo "* Tela nao cadastrada *"
    E nada é gravado
    Dado que o meu código de acesso não tem esta tela
    Quando abro a tela E041T
    Então vejo "* Acesso negado para esta matricula *"
    E o acesso termina ali
    Dado que o meu código de acesso não tem a operação de alteração liberada nesta tela
    Quando confirmo a alteração
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado e a tela é abandonada

  Cenário: A recusa não grava nem apaga nada
    Dado que a minha alteração foi recusada por alguma conferência
    Quando a tela termina a passagem
    Então nenhum gênero e nenhum pedido foram alterados por causa dela
    E nenhum registro de auditoria foi gerado
```
