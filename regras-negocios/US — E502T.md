# US — E502T — Registrar a sobremesa do segmento da merenda

## Estória

Como **servidor de CRE**, quero **registrar, para cada refeição de um segmento do
cálculo da merenda, o cardápio de sobremesa e a quantidade de comensais que a
recebem em cada um dos sete dias do período — e, quando o segmento for o último do
cálculo, mandar calcular o pedido**, para que **a sobremesa entre no pedido dia a
dia, com o cardápio e a quantidade certos, e o pedido do fornecedor saia do que foi
planejado**.

O cálculo da merenda é montado segmento a segmento, e um segmento só fica completo
quando cada dia de cada refeição sabe o que será servido e para quantos. A sobremesa
é a última parte, e não é um campo do cardápio comum: ela tem cadastro próprio,
cardápio próprio e um limite de quantas vezes pode ser servida no mês. É esta tela
que fecha essa parte e, no último segmento, é ela que dispara o cálculo do pedido.
Sem ela o pedido sairia sem sobremesa; com a quantidade errada, sairia sobremesa a
mais ou a menos — e o que o fornecedor entrega a mais não volta, e o que falta deixa
o dia sem.

## Contexto

Jornada S000M → E000M → E500M → E500T → E501T → E502T.
Ator: servidor de CRE — informa, por refeição e por dia do período, o cardápio de
sobremesa e quantos comensais o recebem, confere as recusas do sistema antes de
gravar e, no último segmento do cálculo, responde se o pedido deve ser calculado.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Das telas antes desta, `E000M` e `E500M` são menus e não deixam estado nenhum. A
`E500T`, tela do cálculo, e a `E501T`, tela do segmento, **não são menus**: elas
encadeiam tela em tela, sem passar por menu. A `E501T` entrega a esta tela o
cálculo, o órgão, a coordenadoria, o segmento, o período e a operação, já com a
refeição zerada. É por isso que a operação desta tela é **regra dela** (RN-04) e não
um contexto: uma tela que abrisse sempre incluindo não falharia — só não deixaria
alterar nem consultar. E, como é a tela anterior que é dona do planejamento do
segmento, é lá que a sobremesa é apagada (RN-05). Ao terminar, esta tela entrega o
mesmo cálculo de volta à `E501T`, no segmento anterior ou no seguinte (RN-18); ou,
respondida a pergunta do cálculo do pedido, entrega à tela do pedido um cálculo já
fechado (RN-26).

As regras abaixo são só as desta tela. O que já está na entrada não se repete aqui.

---

## Regras de negócio

### RN-01 — Esta tela é a da sobremesa do segmento, e só trabalha na transação do cálculo

A tela pertence ao cálculo da merenda e só monta a sobremesa do segmento quando a
transação é a que a tela do cálculo abriu. Vindo de outra origem, ela não monta
nada: o servidor é levado ao menu `E500M`.

### RN-02 — As datas do cálculo e do período, e as sete letras de semana, têm de vir completas

A tela exige, antes de tudo: a data de início do cálculo, o limite do cálculo, o
início do período e o limite do período, todos preenchidos; nenhum limite anterior
ao seu início; as **sete** letras de semana do período e as **sete** descrições de
dia preenchidas; e a marca de creche do segmento preenchida. Faltando qualquer um,
ou estando um limite antes do seu início, a tela não segue: a operação volta a ser a
inclusão e o servidor retorna à tela do cálculo.

### RN-03 — O cálculo tem de ser do órgão do servidor

O cálculo só é atendido se o órgão dele for o órgão do vínculo do servidor.
Divergindo, a tela não segue: a operação volta a ser a inclusão e o servidor retorna
à tela do cálculo. Na confirmação o vínculo é lido de novo e, quando ele não existe
ou carrega um órgão diferente do cálculo, o servidor é levado ao menu `E500M` e nada
é gravado.

### RN-04 — A operação vem decidida pela tela anterior: esta tela inclui, altera e consulta

Inclusão, alteração e consulta chegam decididas pela tela do segmento, e esta tela
as adota como chegaram — é o que faz a alteração e a consulta abrirem no modo certo.
Chegando qualquer outra operação, a tela recusa com
**\* Opcao nao disponivel. Use INC, ALT ou CON \***, com o cursor no campo da
operação e sem gravar nem apagar nada.

### RN-05 — A exclusão da sobremesa é feita na tela anterior

Esta tela não apaga sobremesa. Chegando a exclusão, ela só serve para andar entre os
segmentos: acompanhada do pedido de segmento anterior ou seguinte, a tela navega
(RN-18); sem esse pedido, a recusa é **\* Exclua na tela anterior de refeicoes \***,
com o cursor no campo do segmento anterior, e nada é apagado.

### RN-06 — O cálculo já processado só aceita consulta

Inclusão e alteração de um cálculo cuja requisição já foi processada são recusadas
com **\* Nao atualize. Calculo ja processado \***, com o cursor no campo da operação
e sem gravar nem apagar nada. A consulta segue.

### RN-07 — O segmento tem de estar cadastrado para o órgão

Antes de tratar a sobremesa, a tela confere que o segmento informado está cadastrado
para o órgão. Não estando, mas havendo planejamento no segmento, a tela passa a
operar em **exclusão** e devolve o servidor à tela do segmento; não estando e não
havendo planejamento nenhum no segmento, a tela encerra sem tratar nada.

### RN-08 — A tela abre na primeira refeição do órgão que tem sobremesa, e mostra o que ela tem

A abertura percorre as refeições cadastradas para o órgão e para na primeira que
tenha sobremesa planejada no segmento ou, para inclusão e alteração, cujo cadastro
de máximo de comensais esteja ativo; refeição que o cadastro não marca como refeição
com sobremesa é pulada. A tela mostra então a descrição da refeição, os rótulos
**Cod.Sob:** e **Comens :** e, com eles, o código de sobremesa e a quantidade de
cada um dos sete dias. A linha de situação do segmento mostra
**\* REQUISICAO PROCESSADA \*** quando a requisição do período já foi processada, e
um traço quando não; a marca de creche do segmento aparece como **Sim** ou **Nao**.
Sem nenhuma refeição com sobremesa, o aviso é
**\* Segmento sem comensais cadastr. para refeicao \*** e a tela não segue.

[?] A tela tem lugar para seis blocos de refeição, mas a varredura que percorre as
refeições do órgão só troca o campo da refeição no ramo que sai do laço. Não se
conclui do fonte como a varredura anda de uma refeição para a seguinte, nem se as
seis chegam a ser mostradas.

### RN-09 — A quantidade de sobremesa e os comensais andam juntos

Para cada um dos sete dias, a quantidade de sobremesa e os comensais da refeição têm
de andar juntos: se a refeição não tem planejamento no segmento e alguma quantidade
de sobremesa foi informada, ou se um dia que **tem** comensais ficou **sem**
quantidade de sobremesa, a recusa é
**\* Informe primeiro comensais para a refeicao \***, com o cursor no campo do
segmento anterior, e nada é gravado.

### RN-10 — Os códigos de sobremesa informados de uma vez preenchem os dias que ainda não têm sobremesa

Antes dos blocos de refeição há sete campos em que o servidor pode informar, de uma
vez, o código de sobremesa de cada um dos sete dias do período. O código informado
passa a ser o da sobremesa daquele dia quando o dia ainda não tem código, ou quando
o dia não tem quantidade; e cada um deles tem de ser um cardápio de sobremesa
cadastrado, valendo desde o início do cálculo e registrado no segmento — não sendo,
a recusa é **\* Cardapio nao cadastrado \***,
**\* Cardapio nao cadastrado como sobremesa \*** ou
**\* Cardapio nao cadastrado neste segmento \***, com o cursor no campo daquele dia,
e nada é gravado.

[?] Os códigos informados nesses sete campos são gravados no planejamento da
refeição **seguinte** à que está na tela, e não na refeição mostrada. Não se conclui
do fonte se a intenção era essa.

### RN-11 — O código de sobremesa do dia tem de estar cadastrado como sobremesa, valer na data do dia e estar no segmento

O código de sobremesa de cada dia tem de constar do cadastro de cardápios, marcado
como sobremesa, com a validade começando até a data daquele dia, e constar do
cadastro de cardápios do segmento. Não constando, ou valendo só a partir de uma data
posterior à do dia, a recusa é **\* Cardapio nao cadastrado \***; não estando marcado
como sobremesa, **\* Cardapio nao cadastrado como sobremesa \***; não estando no
segmento, **\* Cardapio nao cadastrado neste segmento \*** — com o cursor no código
daquele dia e nada é gravado.

### RN-12 — Quantidade de sobremesa sem código é recusada

Um dia com quantidade de sobremesa informada e sem o código do cardápio é recusado
com **\* Informe o codigo do cardapio da sobremesa \***, com o cursor no código
daquele dia, e nada é gravado.

### RN-13 — O segmento que não recebe refeição em sábado e domingo não aceita sobremesa nesses dias

Quando o segmento está configurado para **não** receber refeição em sábados e
domingos, um dia do período que caia em sábado ou domingo **e tenha sobremesa
informada** é recusado com
**\* Segmento nao recebe refeic. sabados e domingos \***, com o cursor na quantidade
daquele dia, e nada é gravado. Dias sem sobremesa informada não são recusados.

### RN-14 — A quantidade de sobremesa do dia não pode passar do máximo cadastrado

Informada uma quantidade de sobremesa maior que a quantidade de pessoas do cadastro
do máximo de comensais da refeição no segmento, a recusa é
**<-Quant. comensais maior que o maximo permitido \***, com o máximo já no começo do
aviso, com o cursor na quantidade daquele dia e nada é gravado.

[?] O cadastro do máximo de comensais guarda **duas** quantidades — a quantidade de
pessoas e a quantidade máxima de pessoas —, e a tela confere só a primeira; nenhum
programa do acervo lê a segunda. Para que serve a segunda é pergunta ao site.

### RN-15 — A sobremesa tem um limite de vezes por mês

O cadastro de frequência da sobremesa guarda, para o órgão, a coordenadoria, o
segmento e a refeição, quantas vezes cada cardápio pode ser servido em **cada mês do
ano**, dentro de uma validade. Não havendo esse cadastro para o cardápio do dia, ou
sendo **zero** o limite do mês em que o dia cai, a recusa é
**\* Sobremesa nao pode ser solicitado neste mes \***; e, somando as vezes que
aquele cardápio já foi servido no mês — fora os dias deste período — com as
quantidades já informadas nos dias deste período que servem o mesmo cardápio,
passando do limite, a recusa é **<- Ultrapassada maxima frequencia do mes \***. Nos
dois casos o cursor fica na quantidade daquele dia e nada é gravado.

### RN-16 — Passando pelas conferências, a sobremesa dos sete dias é gravada no planejamento

Passando pelas conferências dos sete dias, a tela grava no planejamento do segmento,
para a refeição da tela, os **sete** códigos de sobremesa e as **sete** quantidades,
para o órgão, a coordenadoria, o cálculo, o segmento e a refeição. A gravação deixa
registro de auditoria com a operação, o cadastro atingido, o processo, a matrícula,
a estação, a secretaria, a coordenadoria e a data e a hora da sessão, com o conteúdo
antes e depois. Se nada mudou, nada é gravado.

### RN-17 — O cardápio extra de cada dia é reescrito, e apagado no dia que ficou sem sobremesa

Terminada a passagem, a tela reescreve o **cardápio extra** de cada um dos sete dias
do segmento e da refeição: o dia que ficou com sobremesa tem o extra gravado ou
corrigido com o código daquela sobremesa, com registro de auditoria; o dia que
ficou **sem quantidade** de sobremesa tem o extra daquele dia apagado. O dia cujo
cardápio não tem cadastro de frequência não é gravado.

[?] O extra do dia é apagado já na passagem de conferência, um dia por vez, e não
depois de todas passarem — e os códigos informados de uma vez (RN-10) também são
gravados nessa passagem. Se um dia posterior for recusado, o que já foi apagado ou
gravado fica, e a tela termina mesmo assim com a recusa. Ou a intenção era escrever
só depois da confirmação, ou a ordem é deliberada. Pergunta ao site.

### RN-18 — Andar para o segmento anterior ou seguinte devolve o servidor à tela do segmento

A tela move o servidor entre os segmentos do mesmo cálculo, devolvendo-o à tela do
segmento: pedido o segmento anterior, ela vai para o segmento imediatamente anterior
— cadastrado ou apenas com planejamento; pedido o segmento seguinte, ela vai para o
seguinte, e a tela do segmento abre em **inclusão**. Cálculo que não tem nem um nem
outro simplesmente não navega.

### RN-19 — A saída é cancelada quando um dia fica com sobremesa e sem quantidade

Antes de sair, a tela confere o planejamento do segmento inteiro: se algum dia de
alguma refeição ficou com **código de sobremesa e sem quantidade**, o pedido de
andar para o segmento anterior ou seguinte é cancelado e a resposta sobre calcular o
pedido é descartada. A tela só deixa sair de um segmento em que todo dia com código
de sobremesa tem quantidade.

### RN-20 — A pergunta do cálculo do pedido só vale no último segmento do cálculo

A tela só oferece a pergunta **Calcula Pedido <S/N>:** — e só respeita a resposta —
quando a tela anterior marcou o segmento como o **último** do cálculo. Fora disso o
campo não aparece e a resposta é descartada. O cálculo do pedido também só se faz
com as datas do período e as letras de semana válidas; não estando, o servidor volta
à tela do cálculo.

### RN-21 — Para calcular o pedido, a requisição do período tem de existir e não estar calculada

Respondida a pergunta com **S**, a tela confere que o início do período é a primeira
data de entrega do pedido — não sendo, o servidor volta à tela do cálculo —, que a
requisição do período está cadastrada e que ela ainda não foi calculada. Não estando
cadastrada, a recusa é **\* Requisicao nao cadastrada \***; já estando calculada,
**\* Requisicao ja calculada \*** — nos dois casos com o cursor no campo da pergunta
e nada é gravado.

### RN-22 — Para calcular, o cálculo tem de ter segmentos e nenhum pode ter sobremesa sem código

Ainda antes de calcular, a tela percorre os segmentos do cálculo: se algum dia de
algum segmento tem quantidade de sobremesa informada e **nenhum** código, a recusa é
**<- Segmento com comensais sem cod. sobremesa \***, começando pelo número do
segmento, com o cursor no campo da pergunta; e, não havendo nenhum segmento
cadastrado para o cálculo, a recusa é
**\* Nao existem segmentos cadastr. para calculo \***, no mesmo cursor. Em qualquer
das duas recusas nada é gravado.

### RN-23 — Respondendo sim, a tela reserva as quantidades por gênero, apagando o cálculo anterior

Respondido **S**, a tela apaga o cálculo anterior do período — as quantidades por
gênero que ele tinha reservadas — e o percorre de novo: para cada segmento, cada
refeição e cada um dos sete dias, converte os comensais da refeição na quantidade de
cada gênero que compõe o cardápio daquele dia e soma à reserva do cálculo; e faz o
mesmo para a sobremesa, com os comensais que a recebem. Cada reserva deixa registro
de auditoria.

### RN-24 — O cálculo grava a quantidade calculada de cada dia e acumula a quantidade na requisição

O cálculo grava, por gênero e por dia do período, a quantidade calculada; e acumula
na requisição a quantidade que já estava solicitada, respeitando o que o cadastro
define para o gênero — a conversão e o fracionamento da unidade —, para que a
requisição fique com o que foi pedido e com o que já foi recebido. As gravações e as
acumulações deixam registro de auditoria.

### RN-25 — O cálculo gera o pedido do fornecedor, com as parcelas de entrega, e marca a requisição como calculada

O cálculo numera e cria o pedido do fornecedor do período e, para cada gênero que
entrou no cálculo, o item do pedido com as **cinco** datas de entrega do cálculo, a
quantidade pedida e a quantidade a receber; liga cada reserva do cálculo ao número
do pedido; atualiza a quantidade do pedido auxiliar; e, antes de gerar o novo, apaga
o pedido do período que estava marcado para exclusão, com os seus itens. Terminado,
marca a requisição do período como **calculada**. Tudo com registro de auditoria.

[?] A tela tem uma recusa para pedido que já exista no intervalo de entrega
(**\* Ja existe pedido neste intervalo de entrega \***), mas as duas únicas vezes em
que o aviso é montado ficam em caminhos que comparam campos de data que o próprio
caminho acabou de zerar, e nada mais no programa escreve neles. Por esse caminho a
recusa é inalcançável: ou a comparação era com outra data, ou os campos deveriam
chegar preenchidos. Pergunta ao site.

### RN-26 — Terminado o cálculo, o servidor vai para a tela do pedido

Terminado o cálculo, a tela entrega o pedido à tela do pedido (`E507T`), com a
operação em **alteração** e com o cálculo, o órgão, a coordenadoria, o segmento, o
período e a refeição, limpando as marcas de gênero, de subclasse e da tela de
origem, para que a tela do pedido comece do zero.

### RN-27 — A consulta não grava nem apaga

A consulta de um segmento passa pela abertura e pelas conferências, mas não grava a
sobremesa do planejamento, não reescreve nem apaga o cardápio extra e não deixa
registro de auditoria: ela apenas devolve o servidor à tela do segmento (RN-18) e
serve para ver o que está planejado.

### RN-28 — Nada é gravado sem a conferência de tela, de rota, de acesso e de operação

Na abertura, a tela confere que ela está registrada para a transação e que o código
de acesso do servidor alcança a tela; na passagem de confirmação, confere a rota, a
segurança da tela e a operação. Sem passar por tudo, nada é gravado e nada é
apagado.

### RN-29 — A recusa não grava a sobremesa nem gera o pedido

Cada recusa encerra a passagem antes da gravação da sobremesa do planejamento e
antes de qualquer passo do cálculo do pedido: a sobremesa não é gravada, o cálculo
do período não é apagado e nenhum pedido é gerado nem alterado. A simples abertura
da tela também não escreve nada.

---

## Cenários BDD

```gherkin
Funcionalidade: Registrar a sobremesa dos dias do segmento do cálculo da merenda e calcular o pedido

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E502T

  Cenário: Registrar a sobremesa dos sete dias de uma refeição
    Dado que vim da tela do segmento, com o cálculo do meu órgão e um segmento
      cadastrado
    E que a refeição mostrada tem planejamento no segmento
    E que os sete dias têm cardápio de sobremesa cadastrado e registrado no segmento
    E que nenhum dia passa do máximo de comensais nem do limite de vezes no mês
    Quando informo o código de sobremesa e a quantidade de cada dia e confirmo
    Então a sobremesa dos sete dias é gravada no planejamento do segmento
    E a gravação deixa registro de auditoria
    E o cardápio extra de cada dia com sobremesa é reescrito

  Cenário: A tela não trabalha quando quem a chamou não é a tela do cálculo
    Dado que a transação não é a que a tela do cálculo abriu
    Quando a tela E502T abre
    Então ela não monta a sobremesa do segmento
    E sou levado ao menu E500M
    E nada é gravado nem apagado

  Cenário: Faltam as datas ou as letras de semana do período
    Dado que a transação chega sem uma das datas do cálculo ou do período, ou sem
      uma das sete letras de semana, ou sem uma das sete descrições de dia, ou sem a
      marca de creche, ou com um limite anterior ao seu início
    Quando abro a tela E502T
    Então a tela não segue
    E a operação volta a ser a inclusão
    E sou levado de volta à tela do cálculo

  Cenário: O cálculo não é do órgão do servidor
    Dado que o órgão do cálculo é diferente do órgão do meu vínculo
    Quando abro a tela E502T
    Então a tela não segue
    E a operação volta a ser a inclusão
    E sou levado de volta à tela do cálculo

  Cenário: O vínculo não alcança o órgão do cálculo
    Dado que o órgão do cálculo é diferente do órgão do meu vínculo
    Quando confirmo a passagem
    Então sou levado ao menu E500M
    E nada é gravado nem apagado

  Cenário: A operação vem decidida pela tela do segmento
    Dado que vim da tela do segmento com a operação de alteração
    Quando a tela E502T abre
    Então ela opera em alteração
    E não troca a operação por inclusão

  Cenário: Operação não disponível
    Dado que a transação chega com uma operação que não é inclusão, alteração nem
      consulta, e sem pedido de andar para outro segmento
    Quando confirmo
    Então vejo "* Opcao nao disponivel. Use INC, ALT ou CON *"
    E o cursor fica no campo da operação
    E nada é gravado nem apagado

  Cenário: A exclusão da sobremesa não é desta tela
    Dado que a transação chega com a operação de exclusão e sem pedido de andar para
      outro segmento
    Quando confirmo
    Então vejo "* Exclua na tela anterior de refeicoes *"
    E o cursor fica no campo do segmento anterior
    E nada é apagado

  Cenário: Cálculo já processado não aceita inclusão nem alteração
    Dado que a requisição do cálculo já foi processada
    Quando confirmo com a operação de inclusão ou de alteração
    Então vejo "* Nao atualize. Calculo ja processado *"
    E o cursor fica no campo da operação
    E nada é gravado nem apagado

  Cenário: O segmento não está cadastrado, mas o cálculo tem planejamento nele
    Dado que o segmento informado não está cadastrado para o órgão
    E que o cálculo tem planejamento no segmento
    Quando confirmo
    Então a tela passa a operar em exclusão
    E sou levado à tela do segmento
    E nada é gravado

  Cenário: O segmento não está cadastrado e o cálculo não tem planejamento nele
    Dado que o segmento informado não está cadastrado para o órgão
    E que o cálculo não tem planejamento nenhum no segmento
    Quando confirmo
    Então a tela encerra sem tratar nada
    E nada é gravado nem apagado

  Cenário: A tela abre na refeição que tem sobremesa e mostra o que ela tem
    Dado que o órgão tem uma refeição com sobremesa planejada no segmento
    Quando abro a tela E502T
    Então vejo a descrição da refeição
    E vejo os rótulos "Cod.Sob:" e "Comens :" com o código e a quantidade dos sete
      dias
    E vejo na linha de situação o traço, porque a requisição não está processada

  Cenário: A linha de situação mostra a requisição processada
    Dado que a requisição do período já foi processada
    Quando abro a tela E502T
    Então vejo "* REQUISICAO PROCESSADA *" na linha de situação do segmento

  Cenário: Segmento sem nenhuma refeição com sobremesa
    Dado que nenhuma refeição do órgão tem sobremesa planejada no segmento
    E que nenhuma tem cadastro de máximo de comensais ativo
    Quando abro a tela E502T
    Então vejo "* Segmento sem comensais cadastr. para refeicao *"
    E a tela não segue

  Cenário: Sobremesa informada onde a refeição não tem planejamento
    Dado que a refeição mostrada não tem planejamento no segmento
    Quando informo quantidade de sobremesa num dia e confirmo
    Então vejo "* Informe primeiro comensais para a refeicao *"
    E o cursor fica no campo do segmento anterior
    E nada é gravado nem apagado

  Cenário: Dia com comensais e sem quantidade de sobremesa
    Dado que a refeição mostrada tem planejamento no segmento
    E que um dos sete dias tem comensais
    Quando deixo a quantidade de sobremesa daquele dia zerada e confirmo
    Então vejo "* Informe primeiro comensais para a refeicao *"
    E o cursor fica no campo do segmento anterior
    E nada é gravado nem apagado

  Cenário: Os códigos informados de uma vez preenchem os dias que ainda não têm sobremesa
    Dado que dois dias do período ainda não têm código de sobremesa
    Quando informo nos campos do alto da tela o código de sobremesa desses dias e
      confirmo
    Então aqueles dias passam a ter esse código de sobremesa
    E a tela segue com eles

  Cenário: Código informado de uma vez não cadastrado
    Dado que informo num dos campos do alto da tela um código que não está
      cadastrado
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor fica no campo daquele dia
    E nada é gravado nem apagado

  Cenário: Código informado de uma vez que não é sobremesa
    Dado que informo num dos campos do alto da tela um código que existe, mas não
      está marcado como sobremesa
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado como sobremesa *"
    E o cursor fica no campo daquele dia
    E nada é gravado nem apagado

  Cenário: Código informado de uma vez que não está no segmento
    Dado que informo num dos campos do alto da tela um código de sobremesa que não
      está registrado no segmento
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado neste segmento *"
    E o cursor fica no campo daquele dia
    E nada é gravado nem apagado

  Cenário: Código de sobremesa do dia não cadastrado
    Dado que o código de sobremesa de um dos dias não existe no cadastro de
      cardápios
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor fica no código daquele dia
    E nada é gravado nem apagado

  Cenário: Código de sobremesa do dia não vale na data do dia
    Dado que o código de sobremesa de um dos dias só passa a valer depois daquele
      dia
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor fica no código daquele dia
    E nada é gravado nem apagado

  Cenário: Código de sobremesa do dia que não é sobremesa
    Dado que o código de um dos dias existe, mas não está marcado como sobremesa
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado como sobremesa *"
    E o cursor fica no código daquele dia
    E nada é gravado nem apagado

  Cenário: Código de sobremesa do dia que não está no segmento
    Dado que o código de um dos dias não está registrado no segmento
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado neste segmento *"
    E o cursor fica no código daquele dia
    E nada é gravado nem apagado

  Cenário: Quantidade de sobremesa sem código
    Dado que informo a quantidade de sobremesa de um dia e deixo o código vazio
    Quando confirmo
    Então vejo "* Informe o codigo do cardapio da sobremesa *"
    E o cursor fica no código daquele dia
    E nada é gravado nem apagado

  Cenário: Sobremesa em sábado ou domingo num segmento que não recebe refeição nesses dias
    Dado que o segmento está configurado para não receber refeição em sábados e
      domingos
    Quando informo sobremesa num dia do período que cai em sábado ou domingo e
      confirmo
    Então vejo "* Segmento nao recebe refeic. sabados e domingos *"
    E o cursor fica na quantidade daquele dia
    E nada é gravado nem apagado

  Cenário: Dia sem sobremesa em sábado ou domingo é aceito
    Dado que o segmento está configurado para não receber refeição em sábados e
      domingos
    Quando deixo sem sobremesa o dia do período que cai em sábado ou domingo
    Então a tela não recusa esse dia

  Cenário: Quantidade de sobremesa acima do máximo de comensais cadastrado
    Dado que informo, num dos dias, uma quantidade maior que a do cadastro do
      máximo de comensais da refeição no segmento
    Quando confirmo
    Então vejo "<-Quant. comensais maior que o maximo permitido *", com o máximo no
      aviso
    E o cursor fica na quantidade daquele dia
    E nada é gravado nem apagado

  Cenário: Cardápio de sobremesa sem cadastro de frequência para o mês
    Dado que o cardápio de sobremesa de um dos dias não tem cadastro de frequência
      para o segmento e a refeição
    Quando confirmo
    Então vejo "* Sobremesa nao pode ser solicitado neste mes *"
    E o cursor fica na quantidade daquele dia
    E nada é gravado nem apagado

  Cenário: Limite do mês zerado para o cardápio de sobremesa
    Dado que o cadastro de frequência do cardápio daquele dia tem zero para o mês em
      que o dia cai
    Quando confirmo
    Então vejo "* Sobremesa nao pode ser solicitado neste mes *"
    E o cursor fica na quantidade daquele dia
    E nada é gravado nem apagado

  Cenário: Frequência do mês ultrapassada
    Dado que o cardápio de sobremesa de um dos dias já foi servido no mês, fora este
      período, até o limite do cadastro
    Quando informo sobremesa nesse dia e confirmo
    Então vejo "<- Ultrapassada maxima frequencia do mes *"
    E o cursor fica na quantidade daquele dia
    E nada é gravado nem apagado

  Cenário: Nada mudou e nada é gravado
    Dado que a sobremesa dos sete dias está exatamente como já estava planejada
    Quando confirmo sem alterar nada
    Então nada é gravado
    E nenhum registro de auditoria é incluído

  Cenário: O cardápio extra do dia é reescrito, e o do dia sem sobremesa é apagado
    Dado que um dia do período ficou com sobremesa e outro ficou sem
    Quando confirmo
    Então o extra do dia com sobremesa é gravado com aquele código de sobremesa
    E o extra do dia sem sobremesa é apagado
    E as duas coisas deixam registro de auditoria

  Cenário: Andar para o segmento anterior
    Dado que o cálculo tem um segmento anterior ao que estou vendo
    Quando peço o segmento anterior
    Então sou levado à tela do segmento, no segmento imediatamente anterior

  Cenário: Andar para o segmento seguinte
    Dado que o cálculo tem um segmento seguinte ao que estou vendo
    Quando peço o segmento seguinte
    Então sou levado à tela do segmento, no segmento seguinte
    E a tela do segmento abre em inclusão

  Cenário: A saída é cancelada por um dia com código de sobremesa e sem quantidade
    Dado que um dia de uma refeição do segmento ficou com código de sobremesa e sem
      quantidade
    Quando peço o segmento anterior ou o seguinte
    Então a tela não navega
    E a resposta sobre calcular o pedido é descartada

  Cenário: A pergunta do cálculo do pedido no último segmento
    Dado que a tela anterior marcou o segmento como o último do cálculo
    Quando abro a tela E502T
    Então vejo a pergunta "Calcula Pedido <S/N>:"

  Cenário: A pergunta do cálculo do pedido fora do último segmento
    Dado que a tela anterior não marcou o segmento como o último do cálculo
    Quando abro a tela E502T
    Então não vejo a pergunta "Calcula Pedido <S/N>:"
    E a resposta é descartada

  Cenário: Calcular o pedido sem requisição cadastrada
    Dado que não há requisição cadastrada para o período
    Quando respondo "S" à pergunta do cálculo do pedido
    Então vejo "* Requisicao nao cadastrada *"
    E o cursor fica no campo da pergunta
    E nada é gravado nem apagado

  Cenário: Calcular o pedido de uma requisição já calculada
    Dado que a requisição do período já está marcada como calculada
    Quando respondo "S" à pergunta do cálculo do pedido
    Então vejo "* Requisicao ja calculada *"
    E o cursor fica no campo da pergunta
    E nada é gravado nem apagado

  Cenário: Calcular o pedido com o período começando fora da primeira data de entrega
    Dado que o início do período é diferente da primeira data de entrega do pedido
    Quando respondo "S" à pergunta do cálculo do pedido
    Então o cálculo não é feito
    E sou levado de volta à tela do cálculo
    E nada é gravado nem apagado

  Cenário: Calcular o pedido com um segmento que tem sobremesa sem código
    Dado que algum segmento do cálculo tem quantidade de sobremesa sem código
    Quando respondo "S" à pergunta do cálculo do pedido
    Então vejo "<- Segmento com comensais sem cod. sobremesa *", com o número do
      segmento no aviso
    E o cursor fica no campo da pergunta
    E nada é gravado nem apagado

  Cenário: Calcular o pedido de um cálculo sem segmento
    Dado que o cálculo não tem nenhum segmento cadastrado
    Quando respondo "S" à pergunta do cálculo do pedido
    Então vejo "* Nao existem segmentos cadastr. para calculo *"
    E o cursor fica no campo da pergunta
    E nada é gravado nem apagado

  Cenário: Respondendo sim, o cálculo do período é refeito e as quantidades são reservadas
    Dado que respondi "S" à pergunta do cálculo do pedido e passei pelas conferências
    Quando o cálculo é executado
    Então o cálculo anterior do período é apagado
    E para cada segmento, refeição e dia, os comensais são convertidos na quantidade
      de cada gênero do cardápio daquele dia e somados à reserva do cálculo
    E o mesmo é feito para a sobremesa
    E cada reserva deixa registro de auditoria

  Cenário: Respondendo sim, a quantidade calculada e a requisição são atualizadas
    Dado que o cálculo do pedido foi executado
    Então a quantidade calculada de cada gênero e de cada dia do período é gravada
    E a quantidade solicitada na requisição é acumulada com o que já havia
    E as gravações deixam registro de auditoria

  Cenário: Respondendo sim, o pedido é gerado e a requisição fica calculada
    Dado que o cálculo do pedido foi executado
    Então o pedido do fornecedor do período é numerado e criado
    E cada gênero que entrou no cálculo vira um item do pedido, com as cinco datas
      de entrega do cálculo, a quantidade pedida e a quantidade a receber
    E cada reserva do cálculo fica ligada ao número do pedido
    E o pedido do período marcado para exclusão é apagado com os seus itens
    E a requisição do período fica marcada como calculada
    E tudo deixa registro de auditoria

  Cenário: Terminado o cálculo, o servidor vai para a tela do pedido
    Dado que o cálculo do pedido terminou
    Quando a tela termina
    Então sou levado à tela do pedido E507T, em alteração
    E a tela do pedido recebe o cálculo, o órgão, a coordenadoria, o segmento, o
      período e a refeição
    E as marcas de gênero, de subclasse e da tela de origem são limpas

  Cenário: A consulta não grava nem apaga
    Dado que estou na tela E502T, na consulta
    Quando confirmo a consulta de um segmento
    Então a tela faz as mesmas conferências
    E nada é gravado nem apagado
    E nenhum registro de auditoria é incluído
    E a tela me devolve à tela do segmento

  Cenário: Nada é gravado sem a conferência de tela, de rota, de acesso e de operação
    Dado que estou na tela E502T
    Quando a conferência do registro da tela, da rota, do código de acesso ou da
      operação não passa
    Então a tela não segue
    E nada é gravado e nada é apagado

  Cenário: A recusa não grava a sobremesa nem gera o pedido
    Dado que estou na tela E502T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então nenhuma sobremesa foi gravada no planejamento do segmento
    E o cálculo do período não foi apagado
    E nenhum pedido foi gerado ou alterado
    E nenhum registro de auditoria foi incluído

  Cenário: A abertura da tela não grava nada
    Dado que estou na tela E502T
    Quando abro a tela
    Então vejo a refeição com sobremesa no segmento e os sete dias do período
    E nenhuma sobremesa, extra ou pedido é gravado
    E nenhuma auditoria é gravada
```
