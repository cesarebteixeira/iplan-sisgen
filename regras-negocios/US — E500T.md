# US — E500T — Manter cálculo da merenda de órgão filho

## Estória

Como **servidor de CRE**, quero **abrir o cálculo da merenda de um órgão filho,
dizendo o período de preparo e quando a entrega começa, para que a requisição do
período fique registrada com o seu primeiro segmento e as datas de entrega já
calculadas**, e depois alterar ou excluir esse cálculo enquanto ele ainda não
estiver sendo preparado.

A merenda de uma escola não é pedida solta: ela é pedida por um cálculo, que
existe por órgão, por coordenadoria regional escolar e por um período de preparo.
É esse cálculo que as telas seguintes percorrem para montar a requisição, e é
contra ele que a entrega de cada gênero é comparada depois. Sem ele, não há
requisição para receber, não há o que o fornecedor entregue e não há como conferir
permissão de fornecimento nenhuma. Esta tela é a porta de entrada desse cálculo:
ela confere o órgão, o período e o dia em que a entrega começa, calcula o limite
de entrega e deixa a requisição pronta, com o seu primeiro segmento.

## Contexto

Jornada S000M → E000M → E500M → E500T.

Ator: servidor de CRE — informa o órgão filho, a coordenadoria regional escolar e
as datas do preparo e da entrega, confere as datas de entrega que o sistema
calculou e confirma a inclusão, a alteração ou a exclusão do cálculo.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Da sessão a tela usa o tipo de órgão (a secretaria), a coordenadoria regional
escolar e o órgão filho do vínculo, além da descrição do órgão e da data do
sistema para o cabeçalho; a matrícula, o código de acesso, a estação e o privilégio
são o que as conferências de acesso leem. Pelas duas telas antes desta — `E000M` e
`E500M` — a tela não recebe nada: as duas são menus, e nenhuma delas deixa estado
no contexto da sessão. Esta tela, porém, pode reabrir a si mesma e entrega o
cálculo à `E501T`, que continua a montagem (RN-19 e RN-20).

As regras abaixo são só as da tela desta jornada. O que já está na entrada não se
repete aqui.

---

## Regras de negócio

### RN-01 — A tela abre incluindo; o servidor pode trocar isso pela alteração, pela exclusão ou pela consulta

Chegando de um menu, a tela abre pronta para **incluir** um cálculo, e cabe ao
servidor trocar a operação para alteração, exclusão ou consulta. Quando a tela
reabre a si mesma, ela já volta na inclusão. Qualquer outra operação é recusada
com **\* Operacao nao disponivel \***, com o cursor no campo da operação e sem
gravar nada.

### RN-02 — Quando a tela anterior é uma das telas do próprio cálculo, quem manda na operação, nas datas e no órgão é ela

Esta tela não abre só de menu: ela também abre de volta da tela de segmentos
(`E501T`), da alteração do cálculo (`E505T`) e da consulta do cálculo (`E508T`).
Nesse caso, a operação, o órgão filho, a coordenadoria regional escolar e as seis
datas que vêm da tela anterior são adotados como estão, e o campo da operação
passa a valer o que veio — a tela não troca por inclusão. É isso que faz a
alteração, a exclusão e a consulta abrirem já no modo certo; uma tela que abrisse
sempre em inclusão não falharia: só não deixaria alterar, excluir nem consultar.

### RN-03 — Três retornos de tela anterior viram aviso, e o cursor vai para o órgão

Quando a tela de onde se vem é a de segmentos, a de alteração do cálculo ou a de
consulta do cálculo, a tela mostra, no mesmo ponto, um dos três avisos —
**\* Orgao sem segmentos cadastrados \***, **\* Calculo cancelado \*** ou
**\* Consulta preparo \*** — deixa o cursor no órgão filho e espera que o servidor
informe tudo de novo.

### RN-04 — Sem órgão no vínculo, o órgão vem em branco; com órgão no vínculo, já vem preenchido e não se aceita outro

Quando o vínculo do servidor não carrega órgão filho, a tela **não** propõe órgão
nenhum: o campo fica em branco e o cursor vai para ele. Quando o vínculo carrega um
órgão filho, a tela já o traz preenchido, junto com a coordenadoria regional
escolar do vínculo, e passa a usar essa coordenadoria; nesse caso, informar outro
órgão é recusado com **\* Usuario sem acesso a outro orgao \***, nomeando o órgão
do vínculo, com o cursor no órgão e sem gravar nada.

### RN-05 — O órgão filho é obrigatório, tem de estar cadastrado e tem de ser aceito pelas conferências do órgão

O órgão filho tem de vir informado: em branco, a recusa é **\* Informe o orgao \***,
com o cursor no órgão. Informado, ele tem de estar cadastrado — senão
**\* Orgao nao cadastrado \*** — e passar por cinco conferências: não pode estar
cadastrado como **inativo** (**\* Orgao cadastrado como inativo \***), não pode
estar marcado como órgão de **pedido acumulado**
(**\* Orgao cadastrado para pedido acumulado \***), os dados de cadastro têm de
estar completos — bairro, órgão pai, nome do órgão, endereço, quantidade de
matrículas e quantidade de pessoas preenchidos
(**\* Orgao cadastrado com dados incompletos \***) —, o órgão tem de pertencer à
secretaria da sessão (**\* Orgao nao pertence a esta secretaria \***) e, quando o
vínculo carrega uma coordenadoria regional escolar, a coordenadoria **do órgão
cadastrado** tem de ser a mesma
(**<- Usuario sem acesso ao grupo deste orgao \***). Em todas essas recusas o
cursor volta ao órgão e nada é gravado.

### RN-06 — A conferência da coordenadoria é feita sobre o cadastro do órgão, e a coordenadoria do órgão passa a valer

A coordenadoria informada não decide nada: a tela lê a coordenadoria que está no
cadastro do órgão e passa a usá-la em todas as leituras e em todas as gravações —
inclusive na procura da requisição e da permissão de fornecimento. Depois disso, a
coordenadoria da tela é a do órgão.

[?] A coordenadoria é pedida ao servidor, passa pela edição numérica e depois é
descartada em favor da do órgão: a comparação de grupo é feita com a coordenadoria
do cadastro, nunca com a que foi digitada. Ou o campo é de enfeite, ou a
conferência deveria comparar o que foi digitado. Pergunta ao site.

### RN-07 — Antes de qualquer conferência, os quinze campos numéricos passam por edição numérica

Antes de qualquer conferência, os **quinze** campos numéricos da tela — o órgão
filho, a coordenadoria, o dia, o mês e o ano do início do cálculo, o dia, o mês e
o ano do limite do cálculo, o dia, o mês e o ano do início do período, o dia, o mês
e o ano do limite do período e a quantidade de dias de entrega — passam por edição
numérica, e o campo em branco é tratado como zero. A operação, a próxima tela e a
resposta da confirmação não passam por essa edição.

[?] O que o servidor vê quando digita algo que não é número não se conclui desta
tela: a rotina que faz a edição não está no acervo. E a tela só sabe devolver o
cursor a oito dos quinze campos — o órgão, as três partes do início do cálculo, o
dia, o mês e o ano do início do período e a quantidade de dias; um erro de
digitação na coordenadoria, no limite do cálculo ou no limite do período não tem
para onde devolver o cursor. Pergunta ao site.

### RN-08 — O cálculo é procurado pelo órgão, pela coordenadoria do órgão e pela data de início do cálculo

A tela procura o cálculo pela secretaria da sessão, pelo órgão filho informado,
pela coordenadoria **do órgão cadastrado** e pela data de início do cálculo,
formada pelo dia, pelo mês e pelo ano. Não achando, a recusa é
**\* Calculo nao cadastrado \***, com o cursor no dia do início do cálculo, e nada
é gravado. Achando, a tela adota a coordenadoria do órgão, a descrição do órgão e o
registro interno do órgão.

### RN-09 — O cálculo já calculado não aceita alteração: só consulta, alteração ou exclusão de quem ainda não foi calculado

Achado o cálculo, se a situação dele indicar **já calculado**, a tela recusa
qualquer operação que não seja a consulta, com
**\* Nao atualize. Requisicao ja calculada \***, com o cursor no campo da operação
e sem gravar nada. As operações de alteração, exclusão e consulta seguem, e a tela
continua a usar o cálculo encontrado.

### RN-10 — Alterar e excluir exigem que o cálculo exista

Para alterar ou excluir, o cálculo tem de existir na data informada: não existindo,
a recusa é **\* Requisicao nao cadastrada \***, com o cursor no campo da operação.

### RN-11 — A inclusão é recusada quando já existe cálculo no mesmo intervalo

Na inclusão, depois de lida a data de início do cálculo, a tela confere se há
cálculo já calculado com a mesma data de término do preparo. Havendo, a recusa é
**<- Ja existe requisicao neste intervalo \***, com a data do intervalo no aviso,
o cursor no dia do início do cálculo e nada é gravado.

### RN-12 — O órgão tem de ter segmento, e o segmento escolhido tem de cobrir o período

O órgão filho tem de ter segmentos cadastrados: sem nenhum, a recusa é
**\* Orgao sem segmentos cadastrados \***, com o cursor no órgão. Havendo, a tela
percorre os segmentos do órgão e escolhe o primeiro cujo período de validade
contém **todo** o intervalo pedido — o início do período e o limite do período têm
de caber dentro dele. O código e a descrição do segmento escolhido passam a ser os
da tela.

### RN-13 — As permissões de fornecimento do órgão e do segmento têm de existir

A tela confere que há permissão de fornecimento para o órgão, para a coordenadoria
e para o segmento escolhido, e que o segmento está cadastrado. Sem segmento
cadastrado, a recusa é **\* Orgao sem segmentos cadastrados \***, com o cursor no
órgão.

### RN-14 — O preparo só começa em dia com letra de semana cadastrada, e só depois da data do sistema

Quando se inclui um cálculo, a data de início do cálculo tem de ser **posterior à
data do sistema** — igual ou anterior é recusada com
**\* Data de inicio de calculo invalida \***, com o cursor no dia do início do
cálculo. Além disso, o dia da semana dessa data tem de ter **letra de semana
cadastrada** para o órgão e a coordenadoria: senão a recusa é
**\* Letra da semana nao cadastrada \***, no mesmo campo.

### RN-15 — O dia do preparo pode ter de bater com o dia da semana configurado para o órgão

Havendo, para o órgão, um dia da semana configurado, o dia da semana da data de
início do cálculo tem de ser exatamente esse. Divergindo, a recusa nomeia o dia
esperado — **\* Inicio de preparo deve ser <dia da semana> \*** —, com o cursor no
dia do início do cálculo e nada é gravado.

### RN-16 — A inclusão percorre as sete letras de semana do preparo e exige todas

Na inclusão, a tela percorre o intervalo do preparo — a data de início do cálculo
até seis dias depois — dia a dia e recolhe a letra da semana de cada um dos sete
dias, gravando também as datas. Se algum dos sete dias não tiver letra de semana
cadastrada, a recusa é **\* Letra da semana nao cadastrada \***, com o cursor no
dia do início do cálculo.

### RN-17 — A entrega só começa em dia útil que não seja feriado, e cabe na permissão de fornecimento

Na inclusão, a data de início da entrega é conferida contra o calendário e contra a
permissão de fornecimento:

- o dia da semana não pode ser sábado — **\* Inicio da entrega nao deve ser um
  sabado \*** — nem domingo — **\* Inicio da entrega nao deve ser um domingo \***,
  com o cursor no dia do início da entrega;
- o dia não pode ser feriado cadastrado para o órgão —
  **\* Inicio da entrega nao deve ser um feriado \***;
- o período de entrega tem de caber na validade de alguma permissão de fornecimento
  da coordenadoria do órgão, com o mesmo limite: senão a recusa é
  **\* Data de entrega fora do limite da permissao \***, com o cursor no dia do
  início da entrega.

Em todas essas recusas nada é gravado.

### RN-18 — A data de início da entrega também não pode ser anterior à data do cálculo nem ficar mais de sete dias depois dela

Na inclusão, o início da entrega tem de ser **posterior à data de início do
cálculo**: igual ou anterior é recusado com
**\* Data de entrega maior que data da requisicao \***, com o cursor no dia do
início da entrega. E a diferença entre o início do cálculo e o início da entrega
não pode passar de sete dias: passando, a recusa é
**\* Difer.entre preparo e entrega maior que 7 dias \***, no mesmo campo.

### RN-19 — Sem limite de entrega informado, a tela calcula o limite em dias úteis, no máximo cinco

Quando o limite da entrega não veio preenchido, a tela calcula-o: a quantidade de
dias de entrega é obrigatória — em branco, **\* Informe a quantidade de dias de
entrega \*** — e não pode passar de cinco —
**\* Quantidade maxima de dias de entrega = 5 \*** —, com o cursor na quantidade
nos dois casos. Aceita, a tela conta os dias de entrega a partir do início da
entrega, **pulando sábados, domingos e feriados**, e o último dia contado vira o
limite da entrega, que volta para a tela.

[?] A tela só confere o limite da entrega (RN-20) quando ele **já veio
preenchido**; quando ela mesma o calcula, a conferência contra a permissão de
fornecimento acontece na conta do início da entrega e não é refeita para o limite
apurado. Se o site espera que o limite calculado também seja conferido, é pergunta
ao site.

### RN-20 — O limite de entrega já informado tem de caber no mapa de merenda já atualizado

Quando o limite da entrega já veio preenchido, a tela verifica se ele está coberto
por algum mapa de merenda do órgão. Não estando, a recusa é
**<- Antes, atualize os mapas ate a data inf. \***, com a data faltante no aviso, o
cursor no campo da próxima tela e nada é gravado.

### RN-21 — A tela calcula a data de entrega de cada dia da semana do período

A tela monta o período de entrega — do início da entrega até seis dias corridos
depois — e recolhe, para cada um dos sete dias, a data e a letra de semana. Quando
o dia cai em sábado, domingo ou feriado, ele é pulado e a contagem avança, de modo
que as sete datas recolhidas são as dos sete primeiros dias úteis a partir do
início da entrega. Depois disso a tela mostra o limite da entrega calculado.

### RN-22 — Depois das conferências, a tela calcula e mostra o limite do cálculo

Passadas as conferências, a tela calcula o limite do cálculo somando seis dias ao
início do cálculo e o mostra na tela, junto com o limite da entrega.

### RN-23 — A inclusão, a alteração e a exclusão são confirmadas antes de acontecer

Passando por todas as conferências, a tela ainda não grava: ela mostra
**\* Confirma inclusao do calculo <S/N> ? \***, **\* Confirma alteracao do calculo
<S/N> ? \*** ou **\* Confirma exclusao do calculo <S/N> ? \***, conforme a
operação, com o cursor na resposta. Só a resposta afirmativa, com a operação, o
órgão e as datas ainda as mesmas que foram conferidas, leva à gravação.

[?] A resposta negativa não devolve o servidor ao começo nem encerra a tela: ela
descarta a pendência, e a tela confere tudo de novo e volta à mesma pergunta. Se a
intenção era poder desistir com a resposta negativa, o caminho não faz isso — quem
responde "N" só sai encerrando a tela. Pergunta ao site.

### RN-24 — Confirmada a inclusão ou a alteração, a requisição do cálculo e o primeiro segmento são gravados

Confirmada a inclusão ou a alteração, a tela grava a requisição do cálculo com o
início do período, o limite do período, o limite do cálculo, a situação e a data de
início do cálculo, e grava o primeiro segmento do período com o código e a
descrição do segmento, a letra de semana e as datas de entrega. Para cada uma das
duas gravações a tela deixa um registro de auditoria com a operação, o cadastro
atingido, o processo, a matrícula, a estação, a secretaria, a coordenadoria e a
data e a hora da sessão, com o conteúdo do registro antes e depois.

### RN-25 — Confirmada a exclusão, a requisição do cálculo, os segmentos e o que o cálculo deixou são apagados

Confirmada a exclusão, a tela apaga, um a um, todos os segmentos do período
encontrados para o cálculo, apaga o que a tela de geração deixou para aquele
cálculo e, por fim, apaga a própria requisição do cálculo. Cada uma dessas
exclusões deixa registro de auditoria, e na tela fica a mensagem
**Requisicao Excluida**.

### RN-26 — Terminada a gravação, a tela passa o cálculo para a tela de segmentos; a consulta vai para a tela de consulta do preparo

Terminada a inclusão ou a alteração, a tela passa o cálculo para a tela de
segmentos, para que o restante do período seja montado lá, e a consulta vai para a
tela de consulta do preparo. É a tela de segmentos que continua a montagem: ela
recebe o cálculo com a operação, o órgão, a coordenadoria e as datas, e volta para
esta tela quando precisa de novo cálculo.

### RN-27 — Nada é incluído, alterado ou apagado sem a conferência de sessão, de tela, de acesso e de operação

Na abertura, a tela confere que o servidor está na **estação em que a sessão foi
aberta** (em outra, o acesso é encerrado e a sessão volta à entrada), que a tela
está registrada (senão **\* Tela nao disponivel \***), que ela pertence ao módulo
da sessão e que o código de acesso do servidor alcança a tela e a operação
(senão **\* Acesso negado para esta matricula \*** ou
**\* Acesso negado para esta operacao \***). Também é recusada a requisição da
segunda página da tela (**\* Acesso a pagina 2 negado \***). Sem passar por tudo,
nada é gravado e nada é apagado.

### RN-28 — A consulta não grava nada, e a recusa também não

A operação de consulta percorre as mesmas conferências e não grava nem apaga: ela
leva à tela de consulta do preparo. E cada recusa encerra a passagem **antes** das
gravações e das exclusões, de modo que nenhuma delas grava a requisição do cálculo
ou o segmento, nem apaga segmento, requisição ou registro de geração, nem deixa
auditoria. A simples abertura da tela também não escreve nada.

---

## Cenários BDD

```gherkin
Funcionalidade: Abrir, alterar e excluir o cálculo da merenda de um órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria e, quando o meu vínculo tiver, a
      coordenadoria regional escolar e o órgão filho
    E tenho acesso à tela E500T

  Cenário: Incluir o cálculo de um órgão filho
    Dado que o órgão filho está cadastrado, ativo, completo, sem pedido acumulado e
      tem segmentos cadastrados
    E que o dia do início do cálculo tem letra de semana cadastrada e o intervalo
      do preparo tem as sete letras de semana
    E que o início da entrega é um dia útil não feriado, posterior ao início do
      cálculo em até sete dias, e cabe na permissão de fornecimento
    E que existe mapa de merenda do órgão até o limite da entrega
    Quando informo o órgão, a coordenadoria, o início do cálculo, o início da
      entrega e a quantidade de dias de entrega, e confirmo a inclusão
    Então a requisição do cálculo é gravada com o início e o limite do período, o
      limite do cálculo e a situação
    E o primeiro segmento do período é gravado com o código e a descrição do
      segmento e as sete datas de entrega
    E cada uma dessas gravações deixa registro de auditoria
    E a tela passa o cálculo para a tela de segmentos

  Cenário: A tela abre incluindo, e a operação pode ser trocada
    Dado que cheguei à tela E500T por um menu
    Quando abro a tela
    Então o campo da operação mostra a inclusão
    E posso trocá-la para alteração, exclusão ou consulta

  Cenário: Operação não disponível
    Dado que estou na tela E500T
    Quando a transação chega com uma operação que não é inclusão, alteração,
      exclusão nem consulta
    Então vejo "* Operacao nao disponivel *"
    E o cursor fica no campo da operação
    E nada é gravado nem apagado

  Cenário: A tela anterior decide a operação e as datas
    Dado que venho da tela de segmentos, da alteração do cálculo ou da consulta do
      cálculo
    Quando a tela E500T abre
    Então a operação, o órgão e as datas que a tela anterior deixou são adotados
      como estão
    E a tela não troca a operação por inclusão

  Cenário: Avisos de retorno das telas do cálculo
    Dado que venho da tela de segmentos, da alteração do cálculo ou da consulta do
      cálculo
    Quando a tela E500T abre
    Então vejo "* Orgao sem segmentos cadastrados *", "* Calculo cancelado *" ou
      "* Consulta preparo *", conforme a tela de onde vim
    E o cursor fica no campo do órgão filho
    E nada é gravado nem apagado

  Cenário: Sem órgão no vínculo, o órgão vem em branco
    Dado que o meu vínculo não carrega órgão filho
    Quando abro a tela E500T
    Então o campo do órgão filho está em branco
    E o cursor fica no campo do órgão filho

  Cenário: Com órgão no vínculo, o órgão já vem preenchido
    Dado que o meu vínculo carrega um órgão filho
    Quando abro a tela E500T
    Então o campo do órgão filho já vem com o órgão do meu vínculo
    E o campo da coordenadoria regional escolar já vem com o do meu vínculo

  Cenário: O servidor não usa cálculo de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo outro órgão e confirmo
    Então vejo "* Usuario sem acesso a outro orgao *", com o órgão do meu vínculo
      nomeado
    E o cursor fica no campo do órgão filho
    E nada é gravado nem apagado

  Cenário: O órgão é obrigatório
    Dado que estou na tela E500T
    Quando confirmo sem informar o órgão filho
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão filho
    E nada é gravado nem apagado

  Cenário: Órgão não cadastrado
    Dado que estou na tela E500T
    Quando informo um órgão filho que não está cadastrado e confirmo
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão filho
    E nada é gravado nem apagado

  Cenário: Órgão inativo
    Dado que o órgão informado está cadastrado como inativo
    Quando confirmo
    Então vejo "* Orgao cadastrado como inativo *"
    E o cursor fica no campo do órgão filho
    E nada é gravado nem apagado

  Cenário: Órgão de pedido acumulado
    Dado que o órgão informado está marcado para pedido acumulado
    Quando confirmo
    Então vejo "* Orgao cadastrado para pedido acumulado *"
    E o cursor fica no campo do órgão filho
    E nada é gravado nem apagado

  Cenário: Órgão com dados de cadastro incompletos
    Dado que falta ao órgão informado o bairro, o órgão pai, o nome, o endereço,
      a quantidade de matrículas ou a quantidade de pessoas
    Quando confirmo
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E o cursor fica no campo do órgão filho
    E nada é gravado nem apagado

  Cenário: Órgão de outra secretaria
    Dado que o órgão informado pertence a outra secretaria
    Quando confirmo
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor fica no campo do órgão filho
    E nada é gravado nem apagado

  Cenário: Órgão de outro grupo
    Dado que o meu vínculo carrega uma coordenadoria regional escolar
    Quando informo um órgão cadastrado em outra coordenadoria e confirmo
    Então vejo "<- Usuario sem acesso ao grupo deste orgao *", com a coordenadoria
      do órgão nomeada
    E o cursor fica no campo do órgão filho
    E nada é gravado nem apagado

  Cenário: A coordenadoria usada é a do órgão cadastrado
    Dado que informo o órgão e uma coordenadoria diferente da do órgão
    Quando confirmo
    Então a tela procura o cálculo pela coordenadoria do órgão cadastrado
    E a coordenadoria que eu digitei não é usada

  Cenário: Os campos numéricos passam por edição numérica antes das conferências
    Dado que estou na tela E500T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências
    E a digitação que não é número é barrada antes das conferências

  Cenário: Cálculo não cadastrado
    Dado que estou na tela E500T, na alteração ou na exclusão
    Quando informo um órgão, uma coordenadoria e uma data de início de cálculo que
      não correspondem a nenhum cálculo e confirmo
    Então vejo "* Calculo nao cadastrado *"
    E o cursor fica no dia do início do cálculo
    E nada é gravado nem apagado

  Cenário: Cálculo já calculado não aceita alteração
    Dado que o cálculo encontrado já está calculado
    Quando confirmo com uma operação que não é a consulta
    Então vejo "* Nao atualize. Requisicao ja calculada *"
    E o cursor fica no campo da operação
    E nada é gravado nem apagado

  Cenário: Já existe cálculo no mesmo intervalo
    Dado que já existe um cálculo calculado com a mesma data de término do preparo
    Quando incluo um cálculo naquele intervalo e confirmo
    Então vejo "<- Ja existe requisicao neste intervalo *", com a data do intervalo
      no aviso
    E o cursor fica no dia do início do cálculo
    E nada é gravado nem apagado

  Cenário: Órgão sem segmentos cadastrados
    Dado que o órgão informado não tem nenhum segmento cadastrado
    Quando confirmo
    Então vejo "* Orgao sem segmentos cadastrados *"
    E o cursor fica no campo do órgão filho
    E nada é gravado nem apagado

  Cenário: O segmento escolhido cobre todo o período pedido
    Dado que o órgão tem segmentos cadastrados
    Quando informo o período e confirmo
    Então o segmento escolhido é o primeiro cujo período de validade contém o
      início e o limite do período
    E o código e a descrição desse segmento passam a ser os da tela

  Cenário: Data de início de cálculo inválida
    Dado que a data de início do cálculo que informei é igual ou anterior à data do
      sistema
    Quando confirmo a inclusão
    Então vejo "* Data de inicio de calculo invalida *"
    E o cursor fica no dia do início do cálculo
    E nada é gravado nem apagado

  Cenário: Letra da semana não cadastrada
    Dado que um dos dias do início do cálculo ou dos sete dias do preparo não tem
      letra de semana cadastrada para o órgão e a coordenadoria
    Quando confirmo a inclusão
    Então vejo "* Letra da semana nao cadastrada *"
    E o cursor fica no dia do início do cálculo
    E nada é gravado nem apagado

  Cenário: O preparo tem de começar no dia da semana configurado
    Dado que o órgão tem um dia da semana configurado para o início do preparo
    Quando informo um início de cálculo que cai em outro dia da semana e confirmo
    Então vejo "* Inicio de preparo deve ser <dia da semana> *"
    E o cursor fica no dia do início do cálculo
    E nada é gravado nem apagado

  Cenário: O preparo percorre as sete letras de semana
    Dado que informo o início do cálculo
    Quando confirmo a inclusão
    Então a tela recolhe a letra da semana e a data dos sete dias do preparo
    E faltando a letra de semana de algum deles, vejo
      "* Letra da semana nao cadastrada *"

  Cenário: Início da entrega em sábado
    Dado que o início da entrega que informei cai em um sábado
    Quando confirmo a inclusão
    Então vejo "* Inicio da entrega nao deve ser um sabado *"
    E o cursor fica no dia do início da entrega
    E nada é gravado nem apagado

  Cenário: Início da entrega em domingo
    Dado que o início da entrega que informei cai em um domingo
    Quando confirmo a inclusão
    Então vejo "* Inicio da entrega nao deve ser um domingo *"
    E o cursor fica no dia do início da entrega
    E nada é gravado nem apagado

  Cenário: Início da entrega em feriado
    Dado que o início da entrega que informei é feriado cadastrado para o órgão
    Quando confirmo a inclusão
    Então vejo "* Inicio da entrega nao deve ser um feriado *"
    E o cursor fica no dia do início da entrega
    E nada é gravado nem apagado

  Cenário: Entrega fora do limite da permissão de fornecimento
    Dado que não há permissão de fornecimento da coordenadoria do órgão cobrindo o
      período de entrega informado
    Quando confirmo a inclusão
    Então vejo "* Data de entrega fora do limite da permissao *"
    E o cursor fica no dia do início da entrega
    E nada é gravado nem apagado

  Cenário: Início da entrega igual ou anterior ao início do cálculo
    Dado que o início da entrega que informei é igual ou anterior ao início do
      cálculo
    Quando confirmo a inclusão
    Então vejo "* Data de entrega maior que data da requisicao *"
    E o cursor fica no dia do início da entrega
    E nada é gravado nem apagado

  Cenário: Mais de sete dias entre o preparo e a entrega
    Dado que a diferença entre o início do cálculo e o início da entrega passa de
      sete dias
    Quando confirmo a inclusão
    Então vejo "* Difer.entre preparo e entrega maior que 7 dias *"
    E o cursor fica no dia do início da entrega
    E nada é gravado nem apagado

  Cenário: A quantidade de dias de entrega é obrigatória
    Dado que não informei o limite da entrega
    Quando confirmo a inclusão com a quantidade de dias de entrega em branco
    Então vejo "* Informe a quantidade de dias de entrega *"
    E o cursor fica no campo da quantidade de dias
    E nada é gravado nem apagado

  Cenário: A quantidade de dias de entrega é no máximo cinco
    Dado que não informei o limite da entrega
    Quando confirmo a inclusão com a quantidade de dias de entrega maior que cinco
    Então vejo "* Quantidade maxima de dias de entrega = 5 *"
    E o cursor fica no campo da quantidade de dias
    E nada é gravado nem apagado

  Cenário: O limite da entrega é calculado em dias úteis
    Dado que não informei o limite da entrega
    E que informei uma quantidade de dias de entrega de um a cinco
    Quando confirmo a inclusão
    Então a tela conta os dias de entrega a partir do início da entrega, pulando
      sábados, domingos e feriados
    E o último dia contado passa a ser o limite da entrega mostrado na tela

  Cenário: O limite da entrega informado não está coberto pelo mapa de merenda
    Dado que o limite da entrega veio preenchido
    E que não há mapa de merenda do órgão até essa data
    Quando confirmo
    Então vejo "<- Antes, atualize os mapas ate a data inf. *", com a data
      faltante no aviso
    E o cursor fica no campo da próxima tela
    E nada é gravado nem apagado

  Cenário: A tela calcula a data de entrega de cada dia da semana
    Dado que o período de entrega vai do início da entrega até seis dias corridos
      depois
    Quando confirmo a inclusão
    Então cada um dos sete dias recebe a sua data e a sua letra de semana
    E os dias que caem em sábado, domingo ou feriado são pulados e a contagem
      avança, de modo que as sete datas são as dos sete primeiros dias úteis
    E vejo o limite da entrega calculado

  Cenário: A tela calcula e mostra o limite do cálculo
    Dado que passei pelas conferências
    Quando confirmo a inclusão ou a alteração
    Então o limite do cálculo é mostrado como seis dias depois do início do cálculo
    E o limite da entrega é mostrado na tela

  Cenário: A gravação é pedida com confirmação
    Dado que o cálculo passou por todas as conferências
    Quando confirmo a inclusão, a alteração ou a exclusão
    Então vejo "* Confirma inclusao do calculo <S/N> ? *",
      "* Confirma alteracao do calculo <S/N> ? *" ou
      "* Confirma exclusao do calculo <S/N> ? *", conforme a operação
    E o cursor fica na resposta
    E nada foi gravado nem apagado ainda

  Cenário: A resposta negativa não grava
    Dado que a tela me pediu a confirmação
    Quando respondo algo diferente de "S"
    Então a gravação não acontece
    E a tela confere o cálculo de novo e volta a pedir a confirmação

  Cenário: Confirmada a inclusão ou a alteração, a requisição e o primeiro segmento são gravados
    Dado que confirmei a inclusão ou a alteração
    Quando a gravação é executada
    Então a requisição do cálculo é gravada com o início e o limite do período, o
      limite do cálculo, a situação e a data de início do cálculo
    E o primeiro segmento do período é gravado com o código e a descrição do
      segmento, a letra de semana e as sete datas de entrega
    E cada gravação deixa registro de auditoria com a operação, o cadastro
      atingido, o processo, a minha matrícula, a estação, a secretaria, a
      coordenadoria e a data e a hora da sessão, com o conteúdo antes e depois

  Cenário: Confirmada a exclusão, o cálculo e o que ele deixou são apagados
    Dado que confirmei a exclusão
    Quando a exclusão é executada
    Então todos os segmentos do período do cálculo são apagados
    E o que a tela de geração deixou para aquele cálculo é apagado
    E a requisição do cálculo é apagada
    E cada exclusão deixa registro de auditoria
    E vejo "Requisicao Excluida"

  Cenário: Terminada a gravação, a tela passa o cálculo adiante
    Dado que a inclusão ou a alteração foi gravada
    Quando a tela termina
    Então o cálculo é passado para a tela de segmentos, com a operação, o órgão, a
      coordenadoria e as datas
    E a tela de segmentos continua a montagem, e volta para esta tela quando
      precisa de novo cálculo

  Cenário: A consulta não grava nada
    Dado que estou na tela E500T, na consulta
    Quando confirmo a consulta de um cálculo
    Então a tela faz as mesmas conferências
    E nada é gravado nem apagado
    E a tela passa para a tela de consulta do preparo

  Cenário: Nada é gravado sem a conferência de sessão, de tela, de acesso e de operação
    Dado que estou na tela E500T
    Quando a conferência da estação, do registro da tela, do código de acesso ou da
      operação não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *",
      "* Acesso negado para esta operacao *" ou "* Acesso a pagina 2 negado *"
    E nada é gravado e nada é apagado
    E, se a estação não for a da minha sessão, o acesso é encerrado

  Cenário: A recusa não grava nem apaga nada
    Dado que estou na tela E500T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então a requisição do cálculo e o primeiro segmento não foram gravados
    E nenhum segmento, requisição ou registro de geração foi apagado
    E nenhum registro de auditoria foi incluído

  Cenário: A abertura da tela não grava nada
    Dado que estou na tela E500T
    Quando abro a tela
    Então vejo a descrição do órgão e a data do sistema no cabeçalho
    E o campo da operação mostra a inclusão
    E nenhuma requisição, segmento ou registro de geração é gravado
    E nenhuma auditoria é gravada
```
