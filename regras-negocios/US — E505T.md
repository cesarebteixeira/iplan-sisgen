# US — E505T — Distribuição e aprovação do pedido de merenda

## Estória

Como **servidor de CRE**, quero **distribuir, gênero a gênero, a quantidade
calculada do pedido da merenda do órgão entre os dias de entrega e responder pela
aprovação do pedido**, para que **a entrega saia dia a dia dentro do que foi
calculado e do que a permissão de fornecimento do fornecedor permite, sem que a
secretaria descubra depois que um dia ficou sem quantidade ou que o total passou do
permitido**.

O pedido da merenda de um órgão nasce de uma corrente: o período de entrega da
coordenadoria, os segmentos do órgão, os comensais de cada refeição, a sobremesa e,
por fim, a quantidade calculada de cada gênero. Esta é a última volta dessa
corrente antes de o pedido virar requisição: é aqui que a quantidade calculada de
cada par de subclasse e gênero é repartida entre os dias de entrega e que a
repartição é conferida contra as permissões de fornecimento da coordenadoria. Uma
repartição errada não falha na hora: nasce um pedido com dia sem quantidade, com
quantidade acima da permissão, ou com um item acumulado sem a quantidade recebida
na nota.

## Contexto

Jornada S000M → E000M → E500M → E505T.

Ator: servidor de CRE — informa, para cada subclasse e gênero do cálculo, a
quantidade que vai em cada dia de entrega e responde pela aprovação do pedido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas antes desta na jornada são menus e não deixam nada na passagem. Da
sessão a tela usa o tipo de órgão (a secretaria), a coordenadoria regional escolar
e o órgão filho do vínculo, a descrição do tipo de órgão e a data do sistema para o
cabeçalho; a matrícula, o código de acesso, a estação e o privilégio são o que as
conferências de acesso leem. A mesma tela também é alcançada pela tela de
distribuição do preparo (`E507T`), fora desta jornada, e essa tela limpa a passagem
antes de entregá-la. Quando o cálculo carregado é de um órgão diferente do órgão do
meu vínculo, esta tela devolve a passagem à `E500T` já com a operação de inclusão;
fora desse caso, termina em si mesma (RN-21).

As regras abaixo são só as da tela desta jornada. O que já está na entrada não se
repete aqui.

---

## Regras de negócio

### RN-01 — O que esta tela mantém

Para cada órgão filho, cada coordenadoria regional escolar e cada pedido, a tela
mantém a distribuição da quantidade calculada de cada par de subclasse e gênero
pelos dias de entrega: eu informo quanto daquele gênero sai em cada um dos dias e a
tela guarda essa repartição.

No alto ela mostra o órgão filho e o seu nome, a coordenadoria, o número do pedido,
o ano da entrega, o fornecedor e a sua razão social, o operador e o seu nome, o dia,
o mês e o ano do início do período, o dia, o mês e o ano limite, o tipo de contrato
e o cartão, além das datas dos cinco dias de entrega. Cada linha traz **9 campos** —
a subclasse, o gênero, a quantidade calculada, as **5** quantidades (uma por dia de
entrega) e a situação da linha — e a tela mostra **12 linhas** por vez. A quantidade
calculada é a que veio do cálculo do pedido e, quando as cinco quantidades da linha
estão zeradas, aparece um asterisco ao lado dela.

### RN-02 — A tela abre sempre em alteração, com o cálculo do órgão à mostra

Esta tela não tem operação de consulta nem é aberta para escolher uma operação: ela
abre sempre em alteração, e o que a passagem deixou é o que ela mostra. Se a
passagem chega com o campo da tela seguinte preenchido, ou já marcada por uma recusa
anterior, a tela encerra sem processar nada.

Existindo cálculo para o órgão, a tela o apresenta e mostra o aviso para teclar
enter para o pedido — com o número do pedido no aviso —; e quando o pedido já tem
alguma quantidade distribuída, ela pergunta, ao pé da última linha,
**Aprova Pedido <S/N>:**, com o cursor na resposta.

Chegando pela tela de distribuição do preparo (`E507T`), a passagem vem limpa: a
tela começa a distribuição do pedido do começo, sem retomar o que estava em
andamento.

[?] O campo da tela seguinte não é atribuído em nenhum ponto do programa; se é a
máscara ou o ambiente que o deixa em branco, é pergunta ao site.

[?] Como não há consulta, o pedido já distribuído só pode ser revisto pela
alteração — e é nessa mesma passagem que a pergunta da aprovação aparece. Se quem só
veio corrigir a distribuição deve ser obrigado a responder à pergunta, é pergunta
ao site.

### RN-03 — A tela e a operação só abrem para quem tem acesso

Antes de qualquer coisa, a abertura confere a estação da sessão com a estação do meu
cadastro e procura a tela no cadastro de telas do meu código de acesso; não achando,
o acesso é recusado — com **\* Tela nao disponivel \*** ou
**\* Acesso negado para esta matricula \***. Depois, a operação pretendida é
conferida contra a liberação daquele código de acesso naquela tela: sem a liberação
da alteração, a recusa é **\* Acesso negado para esta operacao \***. Em qualquer dos
casos nada é gravado.

### RN-04 — O órgão do cálculo e o meu vínculo

O órgão é obrigatório: sem ele, a tela recusa com **\* Informe o orgao \*** e devolve
o cursor ao campo do órgão, sem gravar nada. E quem tem um órgão no vínculo da
sessão não pode trabalhar em outro: informando um órgão diferente, a recusa é
**\* Usuario sem acesso a outro orgao \***, com o órgão do vínculo nomeado no aviso
e o cursor de volta ao campo. Quem não tem nenhum órgão no vínculo é posicionado no
campo do órgão, para informá-lo.

### RN-05 — O grupo do cálculo tem de ser o meu

O cálculo que a tela carrega tem de ser da minha coordenadoria. Se o que a passagem
encontrou para o órgão é de outro grupo, a recusa é
**\* Usuario sem acesso ao grupo deste orgao \***, com a coordenadoria nomeada no
aviso e o cursor no campo do órgão, e nada é processado.

Ao carregar o cálculo do órgão, a tela ainda varre o que existe para aquele órgão e
apaga o que não é da minha coordenadoria — e faz a mesma varredura quando eu aponto
para outro órgão. A limpeza não deixa registro de auditoria.

[?] A varredura que apaga é feita com a coordenadoria zerada, e apaga tudo o que não
bate com a coordenadoria da minha sessão. Se essa varredura alcança mesmo o cálculo
de outro grupo, abrir a tela apaga o pedido calculado alheio; e, quando o meu vínculo
não carrega coordenadoria nenhuma, a comparação é com zero e a limpeza leva todas as
reservas do órgão, de qualquer grupo. Ou a limpeza só deveria rodar com coordenadoria
no vínculo, ou a comparação deveria ser outra. Pergunta ao site.

### RN-06 — A tela só aceita a alteração

A única operação aceita é a alteração. Qualquer outra é recusada com
**\* Opcao nao disponivel. Use ALT \***, sem que nada seja gravado.

[?] A operação já vem marcada como alteração pela própria abertura da tela, e a
recusa é conferida antes das demais. Se a máscara permite escolher outra operação,
essa escolha é recusada sem chegar a ser usada; se existe caso em que a tela deva
abrir em outra operação, é pergunta ao site.

### RN-07 — Sem gêneros calculados, não há o que distribuir

Quando não há nenhum gênero calculado para o órgão — nem para o pedido que a
passagem carrega — a tela avisa **\* Nao existem generos a distribuir \***,
posiciona o cursor no campo do órgão e encerra sem gravar. Havendo pedido para o
órgão, mas ainda sem gênero calculado, o aviso é o outro: a tela aponta o pedido e
manda teclar enter para buscá-lo.

### RN-08 — Antes de qualquer conferência, os vinte e três campos numéricos passam por edição numérica

Antes de qualquer conferência, os **vinte e três** campos numéricos da tela — o
órgão filho, a coordenadoria regional escolar, o número do pedido, o ano da entrega,
o código do fornecedor, o código do operador, o dia, o mês e o ano do início do
período, o dia, o mês e o ano limite, o tipo de contrato, o código da subclasse, o
código do gênero, a quantidade calculada, as cinco quantidades dos dias de entrega e
dois campos de controle da linha em foco — passam por edição numérica. Em **vinte e
dois** deles o campo em branco é tratado como zero; nas **seis** quantidades a tela
trata também o separador decimal. A operação, a próxima tela e a resposta da
aprovação não passam por essa edição.

[?] O que o servidor vê quando digita algo que não é número não se conclui desta
tela: a rotina que faz a conferência é apenas declarada no acervo, e o corpo dela não
está nele. E a tela só sabe devolver o cursor a **oito** dos vinte e três campos — o
órgão, as cinco quantidades e os dois campos de controle —; um erro de digitação no
número do pedido, no ano da entrega, no fornecedor, no operador, nas datas do
período ou do limite, no tipo de contrato, na subclasse ou no gênero não tem para
onde devolver o cursor. Pergunta ao site.

### RN-09 — A quantidade distribuída não pode passar da calculada

Somando as cinco quantidades que eu informo em uma linha, o total não pode passar da
quantidade calculada daquele gênero. Passando, a recusa é
**\* Quantidade distribuida maior que calculada \***, com o cursor de volta à coluna
da quantidade, e nada é gravado.

### RN-10 — Item acumulado exige quantidade informada

Nos itens que acumulam, a linha não pode ficar sem quantidade: somando zero nas
cinco quantidades, a recusa é **\* Informe quantidade a ser distribuida \***, com o
cursor de volta à coluna da quantidade, e nada é gravado.

### RN-11 — Cada quantidade vai para um dia de entrega válido

Não se informa quantidade para um dia que não é dia de entrega daquele pedido: em
cada uma das cinco quantidades, quando eu informo um valor e o dia correspondente não
tem data de entrega, a recusa é
**\* Inf. quantidade para dias de entrega validos \***, com o cursor de volta à
coluna daquele dia, e nada é gravado.

### RN-12 — A quantidade tem de respeitar a fração do gênero

Cada quantidade informada tem de ser múltipla da fração de entrega daquele gênero.
Não sendo, a recusa é **\* Quant. fracionada invalida para este genero \***, com o
cursor de volta à coluna daquele dia, e nada é gravado.

### RN-13 — O gênero precisa de permissão de fornecimento vigente no contrato

A distribuição só pode ser feita sobre uma permissão de fornecimento: o sistema
procura, para o órgão, o tipo de contrato, o fornecedor, a minha coordenadoria, a
subclasse, o gênero e a data limite do item, uma permissão não excluída cujo início
seja igual ou anterior ao início do período. Não achando, a recusa é
**\* Genero sem permissao \***, com o cursor de volta à coluna da situação, e nada é
gravado. A conferência é feita em toda linha carregada, mesmo na que eu não mudei.

### RN-14 — A quantidade não pode estourar o saldo inicial da permissão

Na permissão achada, o sistema parte do que já está pedido naquela permissão, devolve
o que aquele item do pedido já tinha distribuído, soma o que eu estou distribuindo
agora e compara o resultado com o saldo inicial da permissão — as três parcelas que
ela guarda, somadas. Se o resultado passar do saldo inicial, a recusa é
**\* Quantidade insuficiente na permissao \***, com o cursor de volta à coluna da
situação, e nada é gravado.

[?] A tela calcula 70% do saldo inicial da permissão em toda conferência e não usa
esse valor em nenhuma comparação: se a intenção era limitar a distribuição a 70% da
permissão, isso não acontece. Pergunta ao site.

### RN-15 — Item acumulado exige a quantidade recebida na nota

Nos itens que acumulam, a tela procura a quantidade recebida daquele item — órgão,
coordenadoria, item acumulado, subclasse, gênero e número da nota fiscal. Não
achando, a recusa é **\* Nao existe quantidade recebida \***, com o cursor de volta à
coluna da quantidade, e nada é gravado.

### RN-16 — A linha marcada é excluída, e a exclusão desfaz o que o cálculo gerou para aquele gênero

Quando a coluna da situação de uma linha chega marcada, a linha não passa por
nenhuma conferência de quantidade — só é excluída. Nesse caso, a tela:

- registra a requisição daquele gênero já como excluída, com a data, a hora e a
  matrícula de quem excluiu;
- devolve à permissão de fornecimento a quantidade que aquele item do pedido tinha;
- apaga o item do pedido daquele gênero;
- apaga o pedido inteiro, quando não sobrou nenhum item dele;
- apaga o cálculo daquele gênero.

Cada uma dessas operações, menos o registro da requisição e a exclusão do
cálculo, deixa registro de auditoria.

Nas linhas de item acumulado a exclusão é outra: registra a requisição excluída,
desconta da quantidade recebida o que estava distribuído e apaga o cálculo daquele
gênero; não devolve nada à permissão de fornecimento nem toca no item do pedido.

[?] A coluna que recebe a marca é lida em quatro pontos do programa e não é
atribuída em nenhum: o acervo não diz como ela se chama na máscara nem se a marca é
um X digitado. Pergunta ao site.

[?] Na linha comum, excluir devolve a quantidade à permissão de fornecimento; na
linha de item acumulado, não devolve nada à permissão. Ou as duas exclusões deveriam
devolver, ou só uma delas deveria mexer na permissão. Pergunta ao site.

### RN-17 — A aprovação exige todos os gêneros com quantidade e prontos

Respondendo **S** à pergunta da aprovação, a tela só aprova se **todos** os gêneros
calculados do pedido tiverem quantidade distribuída e se os itens do pedido estiverem
na situação que a aprovação aceita. Achando qualquer gênero sem quantidade, ou um
item na situação que ela não aceita aprovar, a recusa é
**\* Generos sem quantidade distribuida \***, com o cursor de volta ao campo da
resposta, e nada é gravado.

[?] A situação do item do pedido é comparada com um código de uma letra que a tela
não explica; o que a letra significa — e por que ela barra a aprovação — é pergunta
ao site.

### RN-18 — O que a aprovação gera

Passando nas conferências, a aprovação:

- cria a requisição de cada gênero do pedido, com a situação de requisição
  processada, a data, a hora e a matrícula de quem aprovou;
- marca o pedido como aprovado, com a data da aprovação;
- apaga os cálculos que viraram requisição;
- nos itens que acumulam, baixa da quantidade recebida o que estava distribuído,
  apaga o item do pedido quando ele zera e refaz a distribuição por gênero do item
  acumulado, fechando os itens que ficaram completos e regravando a situação do
  pedido acumulado.

### RN-19 — Recusar a aprovação não grava nada

Respondendo qualquer coisa diferente de **S** à pergunta da aprovação, nada é
gravado: a tela apenas reexamina o pedido e termina. Como o pedido continua com
quantidade distribuída, a pergunta volta a ser feita na próxima passagem.

### RN-20 — O que fica gravado e a auditoria

Cada gravação no item do pedido, na permissão de fornecimento, no pedido, na
quantidade recebida e na distribuição por gênero deixa um registro na auditoria
**A010T** com a tela, a operação, o cadastro atingido, o órgão, a coordenadoria, o
meu número de processo, a minha matrícula, a estação, a secretaria, a data e a hora
da sessão e os valores de antes e depois. O cálculo, o registro da requisição e as
exclusões do cálculo não deixam auditoria.

Além da auditoria, a tela grava: a quantidade de cada dia no cálculo — e só os dias
cuja quantidade eu mudei; a quantidade distribuída do item do pedido e a quantidade
pedida da permissão de fornecimento — as duas só quando aquele item do pedido já
existe; e, na aprovação, a requisição. A criação do item do pedido acontece só no
caminho do pedido acumulado, quando a aprovação refaz as quantidades do item
acumulado. A limpeza das reservas de outra coordenadoria e a exclusão do cálculo não
deixam auditoria.

[?] Quando o item do pedido daquele gênero ainda não existe, a distribuição atualiza
a quantidade do cálculo, mas não grava a quantidade distribuída em item nenhum nem
toca a permissão. Ou o item deveria nascer também neste caminho, ou o caminho não
deveria existir — pergunta ao site.

### RN-21 — O que a tela entrega à tela seguinte

Quando o cálculo que chegou na passagem é de um órgão diferente do órgão do meu
vínculo, a tela não processa nada: ela devolve a passagem à `E500T` já com a operação
de inclusão. Fora desse caso, a tela termina em si mesma.

[?] A jornada registra esta tela como quem "passa para E500T", e a única passagem à
`E500T` no fonte é essa, que exige um cálculo carregado para outro órgão que não o do
vínculo. Se existem outros caminhos de saída, é pergunta ao site. Há ainda o caminho
inverso: a mesma tela também é alcançada a partir da tela de distribuição do preparo
(`E507T`), fora desta jornada.

---

## Cenários BDD

```gherkin
Funcionalidade: Distribuir a quantidade calculada do pedido pelos dias de entrega e aprovar o pedido

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria e, quando o meu vínculo tiver, a
      coordenadoria regional escolar e o órgão filho
    E tenho acesso à tela E505T

  Cenário: A abertura mostra o cálculo do órgão
    Dado que existe cálculo para o órgão da minha passagem
    Quando a tela abre
    Então vejo o órgão, a coordenadoria, o número do pedido, o período e as datas dos
      cinco dias de entrega
    E vejo até 12 linhas, com subclasse, gênero, quantidade calculada e os cinco dias
    E, quando as cinco quantidades de uma linha estão zeradas, aparece um asterisco
    E nada é gravado

  Cenário: Distribuição de um gênero pelos dias de entrega
    Dado que a linha tem uma quantidade calculada e há dias de entrega válidos
    Quando informo as quantidades de cada dia, dentro do calculado e da fração do
      gênero
    Então a tela grava a quantidade de cada dia no cálculo
    E grava a quantidade distribuída no item do pedido e a quantidade pedida na
      permissão de fornecimento
    E registra a operação na auditoria A010T

  Cenário: Aprovação do pedido
    Dado que todos os gêneros calculados do pedido têm quantidade distribuída
    E que os itens do pedido estão na situação que a aprovação aceita
    Quando respondo S à pergunta "Aprova Pedido <S/N>:"
    Então o sistema cria a requisição de cada gênero do pedido
    E marca o pedido como aprovado, com a data da aprovação
    E apaga os cálculos que viraram requisição
    E registra a operação na auditoria A010T

  Cenário: Aprovação de pedido com item acumulado
    Dado que o item é acumulado e tem quantidade recebida na nota
    Quando respondo S à pergunta da aprovação
    Então a quantidade recebida é baixada pelo que estava distribuído
    E a distribuição por gênero do item acumulado é refeita
    E os itens que ficaram completos são fechados
    E a situação do pedido acumulado é regravada

  Cenário: Recusa da aprovação não grava nada
    Dado que o pedido tem quantidade distribuída
    Quando respondo algo diferente de S à pergunta "Aprova Pedido <S/N>:"
    Então nada é gravado
    E a pergunta volta a ser feita na próxima passagem

  Cenário: Aprovação recusada porque há gênero sem quantidade distribuída
    Dado que algum gênero calculado do pedido está sem quantidade
    Quando respondo S à pergunta da aprovação
    Então vejo a mensagem "* Generos sem quantidade distribuida *"
    E o cursor volta ao campo da resposta
    E nada é gravado

  Cenário: Exclusão de uma linha da distribuição
    Dado que marco a coluna da situação de uma linha
    Quando confirmo
    Então a linha não passa por nenhuma conferência de quantidade
    E a requisição daquele gênero fica registrada como excluída, com a data, a hora e
      a minha matrícula
    E a quantidade daquele item volta para a permissão de fornecimento
    E o item do pedido daquele gênero é apagado
    E o cálculo daquele gênero é apagado
    E a devolução à permissão, a exclusão do item e a do pedido deixam auditoria

  Cenário: Exclusão de uma linha e o pedido sem itens
    Dado que marco a coluna da situação da última linha de um pedido
    Quando confirmo
    Então o item do pedido daquele gênero é apagado
    E o pedido inteiro é apagado, porque não sobrou nenhum item dele
    E a requisição daquele gênero fica registrada como excluída

  Cenário: Exclusão de uma linha de item acumulado
    Dado que marco a coluna da situação de uma linha de item acumulado
    Quando confirmo
    Então a requisição daquele gênero fica registrada como excluída
    E a quantidade recebida é descontada do que estava distribuído
    E o cálculo daquele gênero é apagado
    E a permissão de fornecimento não é tocada

  Cenário: Aviso de pedido sem gêneros para distribuir
    Dado que o pedido do órgão ainda não tem gênero calculado
    Quando a tela abre
    Então vejo o aviso para teclar enter para o pedido, com o número do pedido no
      aviso
    E nada é gravado

  Cenário: Acesso à tela sem autorização
    Dado que o meu código de acesso não tem a tela E505T no seu cadastro
    Quando a tela tenta abrir
    Então vejo a mensagem "* Tela nao disponivel *"
    E nada é gravado

  Cenário: Operação não liberada para o meu código de acesso
    Dado que o meu código de acesso não tem a alteração liberada nesta tela
    Quando confirmo a passagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Operação diferente de alteração é recusada
    Quando a passagem chega com uma operação diferente de ALT
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E nada é gravado

  Cenário: Órgão não informado
    Dado que a passagem chega sem órgão
    Quando confirmo a passagem
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor volta ao campo do órgão
    E nada é gravado

  Cenário: Órgão de outro vínculo é recusado
    Dado que eu tenho um órgão no vínculo da sessão
    Quando informo um órgão diferente
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *", com o órgão do meu
      vínculo nomeado
    E o cursor volta ao campo do órgão
    E nada é gravado

  Cenário: Cálculo de outro grupo é recusado
    Dado que o cálculo carregado é de outra coordenadoria regional escolar
    Quando a tela carrega o pedido
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste orgao *", com a
      coordenadoria nomeada
    E o cursor fica no campo do órgão
    E nada é processado

  Cenário: Ao carregar o órgão, as reservas de outra coordenadoria são apagadas
    Dado que existe reserva de outra coordenadoria para o órgão
    Quando a tela carrega o cálculo do órgão
    Então o que não é da minha coordenadoria é apagado
    E essa limpeza não deixa auditoria

  Cenário: Não há gêneros calculados para distribuir
    Dado que não existe gênero calculado para o órgão
    Quando a tela abre
    Então vejo a mensagem "* Nao existem generos a distribuir *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Os campos numéricos passam por edição numérica antes das conferências
    Dado que estou na tela E505T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências
    E a digitação que não é número é barrada antes das conferências

  Cenário: Quantidade acima da calculada é recusada
    Dado que somo nas cinco quantidades da linha mais do que a quantidade calculada
    Quando confirmo a linha
    Então vejo a mensagem "* Quantidade distribuida maior que calculada *"
    E o cursor volta à coluna da quantidade
    E nada é gravado

  Cenário: Item acumulado sem quantidade é recusado
    Dado que a linha é de um item acumulado
    Quando deixo as cinco quantidades zeradas
    Então vejo a mensagem "* Informe quantidade a ser distribuida *"
    E o cursor volta à coluna da quantidade
    E nada é gravado

  Cenário: Quantidade em dia sem data de entrega é recusada
    Dado que informo quantidade em um dia que não é dia de entrega do pedido
    Quando confirmo a linha
    Então vejo a mensagem "* Inf. quantidade para dias de entrega validos *"
    E o cursor volta à coluna daquele dia
    E nada é gravado

  Cenário: Quantidade fora da fração do gênero é recusada
    Dado que informo uma quantidade que não é múltipla da fração do gênero
    Quando confirmo a linha
    Então vejo a mensagem "* Quant. fracionada invalida para este genero *"
    E o cursor volta à coluna daquele dia
    E nada é gravado

  Cenário: Gênero sem permissão de fornecimento é recusado
    Dado que não há permissão de fornecimento vigente para o gênero no contrato
    Quando confirmo a linha
    Então vejo a mensagem "* Genero sem permissao *"
    E o cursor volta à coluna da situação
    E nada é gravado

  Cenário: Quantidade acima do saldo inicial da permissão é recusada
    Dado que o que eu distribuo passa do saldo inicial da permissão, descontado o que
      o item já tinha
    Quando confirmo a linha
    Então vejo a mensagem "* Quantidade insuficiente na permissao *"
    E o cursor volta à coluna da situação
    E nada é gravado

  Cenário: Item acumulado sem quantidade recebida na nota é recusado
    Dado que a linha é de um item acumulado
    E não existe quantidade recebida para ele na nota procurada
    Quando confirmo a linha
    Então vejo a mensagem "* Nao existe quantidade recebida *"
    E o cursor volta à coluna da quantidade
    E nada é gravado

  Cenário: A recusa não grava nada
    Dado que a passagem foi recusada por alguma conferência
    Quando a tela termina a passagem
    Então nenhuma quantidade de dia foi gravada
    E nenhum item do pedido, pedido ou permissão foi tocado
    E nenhum registro de auditoria foi gerado

  Cenário: Passagem devolvida por causa do vínculo
    Dado que o cálculo carregado é de um órgão diferente do meu vínculo
    Quando a tela recebe a passagem
    Então ela não processa nada
    E devolve a passagem à tela E500T com a operação de inclusão

  Cenário: Chegando da tela de distribuição do preparo, a distribuição começa do começo
    Dado que venho da tela E507T com o pedido marcado para distribuição
    Quando a tela E505T abre
    Então ela começa a distribuição do pedido do começo
    E não retoma a distribuição que estava em andamento

  Cenário: Cada gravação deixa auditoria
    Dado que a passagem passou por todas as conferências
    Quando a tela grava a distribuição, exclui uma linha, ou aprova o pedido
    Então fica um registro de auditoria com a tela, a operação, o cadastro atingido,
      o órgão, a coordenadoria, o meu número de processo, a minha matrícula, a
      estação, a secretaria, a data e a hora da sessão e os valores de antes e depois
```
