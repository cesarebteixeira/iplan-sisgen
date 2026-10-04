# US — E501T — Manter cardápio e comensais do segmento da merenda

## Estória

Como **servidor de CRE**, quero **registrar, para cada refeição de um segmento do
cálculo da merenda, o cardápio e a quantidade de comensais de cada um dos sete dias
do período — e apagar o que não vai ser servido —**, para que o período fique pedido
dia a dia, com o que será servido e para quantas pessoas, e para que a exclusão de
um segmento não deixe para trás o que ele tinha.

O cálculo da merenda é aberto por período e recebe o seu primeiro segmento na tela
anterior; mas um segmento sozinho não diz nada. O que a merenda precisa saber é,
para cada dia do período e para cada refeição, **qual é o cardápio** e **quantos
comensais** serão atendidos. É este registro que a tela desta jornada mantém, e é
ele que o período leva adiante. Sem ele, o segmento existe e não há o que pedir nem
o que conferir na entrega; com ele errado, o pedido sai com o cardápio ou com a
quantidade de outro dia.

## Contexto

Jornada S000M → E000M → E500M → E500T → E501T.
Ator: servidor de CRE — informa, por refeição e por dia do período, o cardápio e a
quantidade de comensais do segmento, e confere as recusas do sistema antes de
gravar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Das duas telas antes desta, `E000M` e `E500M` são menus e não deixam estado nenhum.
A `E500T`, que é a tela do cálculo, **não é menu**: ela encadeia tela em tela, sem
passar por menu, e é dela que chegam a operação, o órgão, a coordenadoria, o
segmento e o período que esta tela usa. É por isso que a operação desta tela é
**regra dela** (RN-02) e não um contexto: uma tela que abrisse sempre incluindo não
falharia — só não deixaria alterar, excluir nem consultar. Ao terminar, esta tela
entrega o mesmo cálculo à `E502T`, que continua o período no segmento seguinte
(RN-23); e pode devolver o servidor à própria `E500T` (RN-21) ou ao menu `E500M`
(RN-01, RN-03).

As regras abaixo são só as desta tela. O que já está na entrada não se repete aqui.

---

## Regras de negócio

### RN-01 — Esta tela é a do segmento do cálculo, e só trabalha quando quem a chamou foi a tela do cálculo

A tela pertence ao cálculo: ela monta o segmento e segue adiante **somente** quando
a tela que a chamou é a `E500T`. Vindo de qualquer outra origem, ela não monta o
segmento e não grava: o servidor é levado ao menu `E500M`. É isso que impede que o
registro de cardápio e comensais seja aberto por fora da requisição a que pertence.

### RN-02 — A operação vem da tela anterior, e só quatro são aceitas

Inclusão, alteração, exclusão e consulta chegam decididas pela tela do cálculo, e
esta tela as adota como chegaram — é o que faz a alteração, a exclusão e a consulta
abrirem no modo certo. Chegando qualquer outra coisa, a tela não monta o segmento e,
na confirmação, recusa com **\* Opcao nao disponivel. Use INC, ALT, EXC ou CON \***,
com o cursor no campo da operação e sem gravar nem apagar nada.

### RN-03 — O cálculo tem de ser do órgão do servidor

O cálculo só é atendido se o órgão dele for o órgão do vínculo do servidor.
Divergindo, a tela não segue: a operação volta a ser a inclusão e o servidor retorna
à tela do cálculo. Na confirmação o vínculo é lido de novo e, quando ele não existe
ou carrega um órgão diferente do cálculo, o servidor é levado ao menu `E500M` e nada
é gravado.

### RN-04 — As datas do cálculo e do período, e as sete letras de semana, têm de vir completas

A tela exige, antes de tudo: a data de início do cálculo, o limite do cálculo, o
início do período e o limite do período, todos preenchidos; nenhum limite anterior
ao seu início; as **sete** letras de semana do período e as **sete** descrições de
dia preenchidas; e a marca de creche do segmento preenchida. Faltando qualquer um,
ou estando um limite antes do início, a tela não segue: a operação volta a ser a
inclusão e o servidor retorna à tela do cálculo.

### RN-05 — O cálculo já processado só aceita consulta

Inclusão, alteração e exclusão de um cálculo cuja requisição já foi processada são
recusadas com **\* Nao atualize. Calculo ja processado \***, com o cursor no campo
da operação e sem gravar nem apagar nada. A consulta segue.

### RN-06 — O segmento tem de existir no cálculo, e o órgão tem de pertencer a ele

Antes de qualquer gravação, a tela confere que o segmento informado existe para o
órgão. Não existindo, a recusa é **\* Orgao nao pertence a este segmento \*** — ou,
quando o cálculo já tem planejamento no segmento,
**\* Orgao nao pertence a este segmento. Use EXC \*** —, com o cursor no campo da
operação e nada é gravado.

### RN-07 — A tela percorre as refeições do órgão e mostra as que têm planejamento no segmento

A abertura percorre as refeições registradas para o órgão e, para cada uma, procura
o planejamento do segmento. A tela mostra a descrição da refeição e os rótulos
**Cod.Car:** e **Comens :**, que antecedem o cardápio e a quantidade de cada dia.
Sem nenhuma refeição com planejamento no segmento, o aviso é
**\* Segmento sem comensais cadastr. para refeicao \*** e a tela não segue. A linha
de situação do segmento mostra **\* REQUISICAO PROCESSADA \*** quando a requisição
do período já foi processada, e um traço quando não.

[?] A tela tem lugar para seis blocos de refeição — cada bloco com o código da
refeição, os sete cardápios e as sete quantidades —, mas a leitura que percorre as
refeições do órgão usa a mesma refeição a cada volta: a refeição só é trocada no
ramo que sai do laço. Não se conclui do fonte como a varredura anda de uma refeição
para a seguinte, nem se as seis chegam a ser mostradas.

[?] O aviso **\* Planejamento nao cadastrado \*** está escrito num caminho que só é
seguido quando a procura do planejamento termina com um terceiro valor, que nenhum
ponto deste programa escreve — este programa só escreve "sim" e "não" naquele
resultado. Ou o aviso é de outro caso, ou o caminho ficou inalcançável por aqui.
Pergunta ao site.

### RN-08 — Excluir exige que haja o que excluir

A exclusão de um segmento sem nenhum planejamento e sem segmento vizinho — nem
anterior, nem seguinte — é recusada com **\* Segmento sem comensais cadastrados \***,
com o cursor no campo da operação e sem apagar nada. Havendo planejamento, ou
havendo segmento vizinho, a exclusão segue.

### RN-09 — O cardápio de cada dia é o informado; em branco, a tela propõe o do cadastro por letra de semana

Para cada um dos **sete** dias do período, o cardápio é o que veio informado na
tela. Não tendo vindo, a tela propõe o cardápio que o cadastro de cardápios guarda
para a letra de semana daquele dia, para o segmento e para a refeição. Só depois
disso a tela confere o cardápio do dia.

### RN-10 — O cardápio do dia tem de estar cadastrado para o segmento

O cardápio do dia tem de constar do cadastro de cardápios do segmento, com a
validade cobrindo a data de início do cálculo: não constando, ou valendo só a partir
de uma data posterior à do cálculo, a recusa é
**\* Cardapio nao cadastrado neste segmento \***, com o cursor no cardápio daquele
dia e nada é gravado.

### RN-11 — O cardápio do dia tem de estar cadastrado para a refeição

Além de existir para o segmento, o cardápio do dia tem de constar do cadastro de
cardápios da refeição: não constando, a recusa é
**\* Cardapio nao cadastrado nesta refeicao \***, com o cursor no cardápio daquele
dia e nada é gravado.

### RN-12 — O segmento que não recebe refeição em sábado e domingo não aceita comensais nesses dias

Quando o segmento está configurado para **não** receber refeição em sábados e
domingos, um dia do período que caia em sábado ou domingo **e tenha comensais
informados** é recusado com
**\* Segmento nao recebe refeic. sabados e domingos \***, com o cursor no cardápio
daquele dia e nada é gravado. Dias sem comensais informados não são recusados.

### RN-13 — Dia feriado do órgão não recebe comensais

Um dia do período que seja feriado cadastrado para o órgão **e tenha comensais
informados** é recusado com **\* Feriado - nao informe comensais \***, com o cursor
no cardápio daquele dia e nada é gravado. Dias sem comensais informados não são
recusados.

### RN-14 — O máximo de comensais da refeição tem de estar cadastrado e ativo

Para incluir ou alterar, a tela exige o cadastro do máximo de comensais da refeição
para o órgão, a coordenadoria e o segmento. Não existindo, a recusa é
**\* Maximo comensais nao cad. para esta refeicao \***; existindo e estando marcado
como inativo, a recusa é **\* Maximo de comensais inativo \***. Nos dois casos o
cursor vai para a quantidade de comensais do **primeiro** dia com quantidade
informada, e nada é gravado.

[?] O cadastro do máximo de comensais guarda **duas** quantidades — a quantidade de
pessoas e a quantidade máxima de pessoas —, e a tela confere só a primeira; nenhum
programa do acervo lê a segunda. Para que serve a segunda é pergunta ao site.

[?] A tela lê o registro de comensais já processados do segmento e da refeição, com
as sete quantidades e os sete cardápios de sobremesa, e descarta o resultado antes de
seguir. Não se conclui do fonte se a intenção era conferir o que já ficou gravado
contra o que veio na tela.

### RN-15 — A quantidade de comensais do dia não pode passar do máximo cadastrado

Informada uma quantidade de comensais maior que a quantidade de pessoas do cadastro
do máximo da refeição, a recusa é
**<-Quant. comensais maior que o maximo permitido \***, com o máximo já no começo do
aviso, com o cursor na quantidade daquele dia e nada é gravado.

### RN-16 — Cada recusa devolve o cursor ao dia que a causou

As conferências do dia valem para os sete dias, um a um, na ordem do período. A tela
devolve o cursor ao campo do dia que causou a recusa: o cardápio do dia nas recusas
de cardápio não informado, de cardápio não cadastrado para o segmento, de cardápio
não cadastrado para a refeição, de sábado e domingo e de feriado; e a quantidade do
dia na recusa de quantidade acima do máximo.

### RN-17 — Passando pelas conferências, o planejamento do segmento é gravado com registro de auditoria

Passando pelas conferências dos sete dias, a tela grava o planejamento do segmento
para a refeição: a refeição, os **sete** cardápios, os **sete** cardápios de
sobremesa e as **sete** quantidades, para o órgão, a coordenadoria, o mês e o ano do
início do cálculo, o segmento e o período. A gravação deixa registro de auditoria
com a operação, o cadastro atingido, o processo, a matrícula, a estação, a
secretaria, a coordenadoria e a data e a hora da sessão, com o conteúdo antes e
depois.

### RN-18 — Sem comensal em nenhum dos sete dias, o planejamento do segmento é apagado

Quando o planejamento do segmento já existe e nenhum dos sete dias fica com
quantidade de comensais informada, a tela apaga o planejamento do segmento para
aquela refeição, com registro de auditoria da exclusão, em vez de gravá-lo.

### RN-19 — O cardápio extra dos sete dias é apagado antes de a tela terminar

Terminada a passagem pelo planejamento, a tela apaga o cardápio extra de cada um dos
sete dias do segmento e da refeição. Quem recria o extra é a tela seguinte, a partir
do que ficou no planejamento — por isso a passagem por esta tela não deixa o extra
antigo para trás.

### RN-20 — Confirmada a exclusão, o planejamento, os extras e a requisição do cálculo são apagados

Confirmada a exclusão, a tela apaga, um a um, todos os planejamentos do cálculo no
segmento e todos os cardápios extras do segmento; e, quando não restar nenhum
planejamento para o cálculo, apaga também a requisição do período. Cada exclusão
deixa registro de auditoria.

### RN-21 — Excluído o último segmento do cálculo, o servidor volta à tela do cálculo em consulta

Quando, depois da exclusão, não resta segmento nenhum para o cálculo, a tela devolve
o servidor à `E500T` em **consulta**, com a marca que faz aquela tela avisar
**\* Orgao sem segmentos cadastrados \*** e esperar que o cálculo seja informado de
novo. Havendo ainda segmento, o servidor segue para o segmento anterior (RN-22).

### RN-22 — A tela anda entre os segmentos do cálculo, para trás e para diante

A tela move o servidor entre os segmentos do mesmo cálculo. Pedido o segmento
anterior, ela vai para o segmento imediatamente anterior; não existindo nenhum
anterior — nem segmento cadastrado, nem planejamento —, a recusa é
**\* Nao existem segmentos anteriores \***, com o cursor no campo do segmento
anterior. Pedido o segmento seguinte, ela vai para o seguinte. Depois de uma
exclusão, a tela passa a operar em **inclusão** no segmento para onde vai.

### RN-23 — Terminada a passagem, a tela entrega o cálculo à tela do segmento seguinte

Terminada a passagem — gravada, apagada ou apenas conferida —, a tela entrega o
cálculo à `E502T`, com a operação, o órgão, a coordenadoria, o segmento e o período,
para que o período continue a ser montado no segmento seguinte. É a `E502T` que
recria o cardápio extra dos dias (RN-19) e que pode devolver o cálculo a esta tela.

### RN-24 — A consulta percorre as mesmas conferências e não grava nem apaga

A consulta de um segmento passa pela mesma abertura e pelas mesmas conferências,
mas não grava planejamento, não apaga planejamento, cardápio extra nem requisição, e
não deixa registro de auditoria: ela segue para a tela do segmento seguinte.

### RN-25 — Nada é gravado sem a conferência de tela, de rota, de acesso e de operação

Na abertura, a tela confere que ela está registrada para a transação e que o código
de acesso do servidor alcança a tela; na passagem de confirmação, confere a rota, a
segurança da tela e a operação. Sem passar por tudo, nada é gravado e nada é
apagado.

[?] A tela só segue quando o campo que diz **para que tela a transação deve ir**
chega em branco; a transação que já traz esse campo preenchido passa pela tela sem
que ela faça nada. Não se conclui do fonte quem preenche esse campo nem o que a
tela deveria fazer nesse caso. Pergunta ao site.

### RN-26 — A recusa não grava nem apaga

Cada recusa encerra a passagem **antes** das gravações e das exclusões, de modo que
nenhuma delas grava o planejamento, apaga planejamento, cardápio extra ou requisição,
nem deixa auditoria. A simples abertura da tela também não escreve nada.

---

## Cenários BDD

```gherkin
Funcionalidade: Registrar o cardápio e os comensais de cada dia do segmento do cálculo da merenda

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E501T

  Cenário: Registrar o cardápio e os comensais dos sete dias de uma refeição
    Dado que vim da tela do cálculo, com o cálculo do meu órgão e um segmento
      cadastrado
    E que os sete dias do período têm cardápio cadastrado para o segmento e para a
      refeição informada
    E que o cadastro do máximo de comensais da refeição existe, está ativo e nenhum
      dia passa desse máximo
    E que nenhum dos dias com comensais é sábado, domingo ou feriado do órgão
    Quando informo o cardápio e a quantidade de comensais de cada dia e confirmo
    Então o planejamento do segmento é gravado para a refeição, com os sete
      cardápios, os sete cardápios de sobremesa e as sete quantidades
    E a gravação deixa registro de auditoria
    E a tela passa o cálculo para a tela do segmento seguinte

  Cenário: A tela não trabalha quando quem a chamou não é a tela do cálculo
    Dado que a tela que me trouxe a E501T não é a tela do cálculo
    Quando a tela E501T abre
    Então ela não monta o segmento
    E sou levado ao menu E500M
    E nada é gravado nem apagado

  Cenário: A operação vem decidida pela tela do cálculo
    Dado que vim da tela do cálculo com a operação de alteração
    Quando a tela E501T abre
    Então ela opera em alteração
    E não troca a operação por inclusão

  Cenário: Operação não disponível
    Dado que a transação chega com uma operação que não é inclusão, alteração,
      exclusão nem consulta
    Quando confirmo
    Então vejo "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E o cursor fica no campo da operação
    E nada é gravado nem apagado

  Cenário: O cálculo não é do órgão do servidor
    Dado que o órgão do cálculo é diferente do órgão do meu vínculo
    Quando abro a tela E501T
    Então a tela não segue
    E a operação volta a ser a inclusão
    E sou levado de volta à tela do cálculo

  Cenário: O vínculo não alcança o órgão do cálculo
    Dado que o órgão do cálculo é diferente do órgão do meu vínculo
    Quando confirmo a passagem
    Então sou levado ao menu E500M
    E nada é gravado nem apagado

  Cenário: Faltam as datas ou as letras de semana do período
    Dado que a transação chega sem uma das datas do cálculo ou do período, ou sem
      uma das sete letras de semana, ou com um limite anterior ao seu início
    Quando abro a tela E501T
    Então a tela não segue
    E a operação volta a ser a inclusão
    E sou levado de volta à tela do cálculo

  Cenário: Cálculo já processado não aceita inclusão, alteração nem exclusão
    Dado que a requisição do cálculo já foi processada
    Quando confirmo com uma operação que não é a consulta
    Então vejo "* Nao atualize. Calculo ja processado *"
    E o cursor fica no campo da operação
    E nada é gravado nem apagado

  Cenário: O segmento não existe no cálculo
    Dado que o segmento informado não está cadastrado para o órgão
    Quando confirmo
    Então vejo "* Orgao nao pertence a este segmento *"
    E o cursor fica no campo da operação
    E nada é gravado nem apagado

  Cenário: O segmento não existe, mas o cálculo já tem planejamento
    Dado que o segmento informado não está cadastrado para o órgão
    E que o cálculo já tem planejamento no segmento
    Quando confirmo
    Então vejo "* Orgao nao pertence a este segmento. Use EXC *"
    E o cursor fica no campo da operação
    E nada é gravado nem apagado

  Cenário: A tela mostra as refeições com planejamento no segmento
    Dado que o segmento tem planejamento para uma refeição
    Quando abro a tela E501T
    Então vejo a descrição da refeição
    E vejo os rótulos "Cod.Car:" e "Comens :" antes do cardápio e da quantidade de
      cada dia

  Cenário: Segmento sem nenhuma refeição com planejamento
    Dado que nenhuma refeição do órgão tem planejamento no segmento
    Quando abro a tela E501T
    Então vejo "* Segmento sem comensais cadastr. para refeicao *"
    E a tela não segue

  Cenário: A linha de situação mostra a requisição processada
    Dado que a requisição do período já foi processada
    Quando abro a tela E501T
    Então vejo "* REQUISICAO PROCESSADA *" na linha de situação do segmento

  Cenário: Excluir um segmento sem planejamento e sem vizinho
    Dado que o segmento não tem planejamento nem segmento anterior nem seguinte
    Quando confirmo a exclusão
    Então vejo "* Segmento sem comensais cadastrados *"
    E o cursor fica no campo da operação
    E nada é apagado

  Cenário: O cardápio em branco é proposto pelo cadastro por letra de semana
    Dado que deixo o cardápio de um dia em branco
    E que existe cardápio cadastrado para a letra de semana daquele dia, no segmento
      e na refeição
    Quando confirmo
    Então o cardápio daquele dia passa a ser o do cadastro por letra de semana
    E a tela segue com esse cardápio

  Cenário: Cardápio do dia não informado e sem cadastro por letra de semana
    Dado que deixo o cardápio de um dia em branco
    E que não há cardápio cadastrado para a letra de semana daquele dia
    Quando confirmo
    Então vejo "* Informe cardapio para a refeicao *"
    E o cursor fica no cardápio daquele dia
    E nada é gravado nem apagado

  Cenário: Cardápio do dia não cadastrado para o segmento
    Dado que o cardápio de um dos dias não está cadastrado para o segmento
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado neste segmento *"
    E o cursor fica no cardápio daquele dia
    E nada é gravado nem apagado

  Cenário: Cardápio do dia não cadastrado para a refeição
    Dado que o cardápio de um dos dias está cadastrado para o segmento mas não para
      a refeição
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado nesta refeicao *"
    E o cursor fica no cardápio daquele dia
    E nada é gravado nem apagado

  Cenário: Comensais em sábado ou domingo num segmento que não recebe refeição nesses dias
    Dado que o segmento está configurado para não receber refeição em sábados e
      domingos
    Quando informo comensais num dia do período que cai em sábado ou domingo e
      confirmo
    Então vejo "* Segmento nao recebe refeic. sabados e domingos *"
    E o cursor fica no cardápio daquele dia
    E nada é gravado nem apagado

  Cenário: Dia sem comensais em sábado ou domingo é aceito
    Dado que o segmento está configurado para não receber refeição em sábados e
      domingos
    Quando deixo sem comensais o dia do período que cai em sábado ou domingo
    Então a tela não recusa esse dia

  Cenário: Comensais em dia feriado do órgão
    Dado que um dia do período com comensais informados é feriado cadastrado para o
      órgão
    Quando confirmo
    Então vejo "* Feriado - nao informe comensais *"
    E o cursor fica no cardápio daquele dia
    E nada é gravado nem apagado

  Cenário: O máximo de comensais da refeição não está cadastrado
    Dado que não existe cadastro do máximo de comensais da refeição
    Quando confirmo a inclusão
    Então vejo "* Maximo comensais nao cad. para esta refeicao *"
    E o cursor fica na quantidade de comensais do primeiro dia com quantidade
      informada
    E nada é gravado nem apagado

  Cenário: O máximo de comensais da refeição está inativo
    Dado que o cadastro do máximo de comensais da refeição está marcado como inativo
    Quando confirmo a inclusão
    Então vejo "* Maximo de comensais inativo *"
    E o cursor fica na quantidade de comensais do primeiro dia com quantidade
      informada
    E nada é gravado nem apagado

  Cenário: Quantidade de comensais acima do máximo permitido
    Dado que informo, num dos dias, uma quantidade maior que a do cadastro do máximo
      da refeição
    Quando confirmo
    Então vejo "<-Quant. comensais maior que o maximo permitido *", com o máximo no
      aviso
    E o cursor fica na quantidade daquele dia
    E nada é gravado nem apagado

  Cenário: Cada recusa leva o cursor ao dia que a causou
    Dado que dois dias do período têm problemas diferentes
    Quando confirmo
    Então a recusa é a do primeiro dia na ordem do período
    E o cursor fica no campo daquele dia — o cardápio nas recusas de cardápio,
      sábado, domingo e feriado; a quantidade na recusa de quantidade acima do
      máximo

  Cenário: Nenhum comensal nos sete dias apaga o planejamento do segmento
    Dado que o planejamento do segmento já existe para a refeição
    Quando deixo os sete dias sem quantidade de comensais e confirmo
    Então o planejamento do segmento é apagado para aquela refeição
    E a exclusão deixa registro de auditoria

  Cenário: O cardápio extra dos dias é apagado
    Dado que os sete dias do segmento têm cardápio extra
    Quando a tela termina a passagem
    Então o cardápio extra de cada um dos sete dias é apagado
    E a tela seguinte os recria a partir do que ficou no planejamento

  Cenário: Confirmada a exclusão, o planejamento, os extras e a requisição são apagados
    Dado que confirmei a exclusão do segmento
    Quando a exclusão é executada
    Então os planejamentos do cálculo naquele segmento são apagados, um a um
    E os cardápios extras do segmento são apagados
    E, não restando planejamento para o cálculo, a requisição do período é apagada
    E cada exclusão deixa registro de auditoria

  Cenário: Excluído o último segmento, o servidor volta ao cálculo em consulta
    Dado que excluí o segmento e não resta segmento nenhum para o cálculo
    Quando a tela termina
    Então sou levado à tela do cálculo, em consulta
    E lá vejo "* Orgao sem segmentos cadastrados *"

  Cenário: Andar para o segmento anterior
    Dado que o cálculo tem um segmento anterior ao que estou vendo
    Quando peço o segmento anterior
    Então a tela passa a mostrar o segmento imediatamente anterior

  Cenário: Não existe segmento anterior
    Dado que não há segmento anterior — nem cadastrado, nem com planejamento
    Quando peço o segmento anterior
    Então vejo "* Nao existem segmentos anteriores *"
    E o cursor fica no campo do segmento anterior
    E nada é gravado nem apagado

  Cenário: Andar para o segmento seguinte
    Dado que o cálculo tem um segmento seguinte ao que estou vendo
    Quando peço o segmento seguinte
    Então a tela passa a mostrar o segmento seguinte

  Cenário: Depois de excluir, a tela opera em inclusão no segmento para onde vai
    Dado que confirmei a exclusão do segmento
    Quando a tela me leva para o segmento anterior
    Então a operação passa a ser a inclusão

  Cenário: Terminada a passagem, o cálculo é entregue à tela do segmento seguinte
    Dado que a gravação, a exclusão ou a consulta terminou
    Quando a tela termina
    Então o cálculo é entregue à tela do segmento seguinte, com a operação, o órgão,
      a coordenadoria, o segmento e o período
    E é a tela seguinte que recria o cardápio extra dos dias

  Cenário: A consulta não grava nem apaga
    Dado que estou na tela E501T, na consulta
    Quando confirmo a consulta de um segmento
    Então a tela faz as mesmas conferências
    E nada é gravado nem apagado
    E nenhum registro de auditoria é incluído
    E a tela passa para a tela do segmento seguinte

  Cenário: A transação que já traz a tela de destino preenchida não passa
    Dado que a transação chega com o campo da tela de destino já preenchido
    Quando a tela E501T abre
    Então ela não faz nada
    E nada é gravado nem apagado

  Cenário: Nada é gravado sem a conferência de tela, de rota, de acesso e de operação
    Dado que estou na tela E501T
    Quando a conferência do registro da tela, da rota, do código de acesso ou da
      operação não passa
    Então a tela não segue
    E nada é gravado e nada é apagado

  Cenário: A recusa não grava nem apaga nada
    Dado que estou na tela E501T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então nenhum planejamento foi gravado
    E nenhum planejamento, cardápio extra ou requisição foi apagado
    E nenhum registro de auditoria foi incluído

  Cenário: A abertura da tela não grava nada
    Dado que estou na tela E501T
    Quando abro a tela
    Então vejo as refeições com planejamento no segmento e os sete dias do período
    E nenhum planejamento, cardápio extra ou requisição é gravado
    E nenhuma auditoria é gravada
```
