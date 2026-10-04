# US — E052T — Sobremesa por refeição do segmento

## Estória

Como **servidor de CRE**, quero **registrar a sobremesa de cada refeição do segmento e
mandar calcular o pedido da alimentação escolar do período**, para que **o pedido saia
com a sobremesa certa em cada dia de entrega, sem que a secretaria tenha de refazer a
conta à mão nem descobrir depois que um dia ficou sem sobremesa ou que a quantidade
passou do que a permissão de entrega permite**.

O pedido da alimentação escolar de um órgão nasce de uma corrente: o período de entrega
da coordenadoria, os segmentos do órgão, os comensais de cada refeição e, por fim, a
sobremesa. Esta é a última volta dessa corrente — é aqui que a sobremesa de cada dia da
semana é amarrada à refeição, que os comensais da sobremesa viram quantidade de item do
pedido e que o item é conferido contra as permissões de entrega da coordenadoria. Uma
volta errada aqui não falha na hora: nasce um pedido com sobremesa a menos, com
quantidade acima do que a permissão comporta, ou com um dia sem sobremesa. E o acerto só
existe enquanto a requisição daquele período ainda não foi dada por calculada.

## Contexto

Jornada S000M → E000M → E050M → E050T → E051T → E052T.

Ator: servidor de CRE — informa a operação, a sobremesa de cada dia e os comensais da
sobremesa de cada refeição do segmento e manda calcular o pedido do período.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Esta tela não é aberta por menu: ela é a continuação da tela das refeições e dos
comensais, que é a continuação da tela do período de entrega do órgão. Do encadeamento
ela recebe o órgão filho SDI, a coordenadoria regional escolar, o segmento, o período de
cálculo, o período de entrega, os sete dias da semana e o que já está cadastrado naquele
segmento; da sessão, a secretaria, a matrícula, o código de acesso e a estação. Do que
ela faz, o que sobra é o pedido do órgão gravado e a requisição do período marcada como
calculada.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O que esta tela mantém

Para cada órgão filho SDI, cada coordenadoria regional escolar, cada segmento e cada
período de cálculo, a tela mantém, refeição por refeição, a sobremesa de cada um dos sete
dias da semana e os comensais da sobremesa daquele dia. Desse par sai o item do pedido.

A tela só trata as refeições que o cadastro de refeições da secretaria marca como
refeição com sobremesa; as demais não aparecem e não são mantidas. No alto ela mostra o
órgão filho, a coordenadoria, o segmento, o período de cálculo, o período de entrega, se
o órgão é creche, os sete dias da semana com os seus nomes e, quando a requisição do
período já foi calculada, o aviso **\* REQUISICAO PROCESSADA \***.

Os campos de sobremesa e de comensais vêm em branco quando a tela é apresentada, com o
que está gravado à mostra ao lado: para alterar, eu redigito.

[?] A tela mostra uma refeição por página e, sob o código da sobremesa de cada dia, os
comensais daquela sobremesa. O que eu digito nessas colunas é tratado, num trecho, como
sendo da refeição **anterior** à que está à mostra e, noutro, da refeição **seguinte**.
O acervo lido não permite dizer com segurança a que refeição cada linha digitada
pertence quando há mais de uma página. Pergunta ao site.

[?] A tela apaga, a cada digitação, as descrições que ela mesma mostrou — o nome do
órgão, o do segmento, os nomes dos dias e os rótulos das colunas — e nenhuma passagem
posterior as repõe. Se o ambiente comum as repõe antes de mostrar a tela, o acervo lido
não mostra. Pergunta ao site.

### RN-02 — A tela só opera dentro do percurso da tela do período

Esta tela não tem como ser aberta por menu: ela confere, na abertura, se a passagem veio
pelo encadeamento da tela do período de entrega. Não vindo, ela não processa nada: no
fim da passagem manda o operador de volta ao menu da alimentação escolar, que avisa
**\* Acesso deve ser feito pela tela E050T \***.

Do mesmo modo, se o que a tela anterior deixou está incompleto ou incoerente — data de
início ou data limite do período de cálculo em branco, limite anterior ao início, algum
dos sete dias da semana sem código ou sem nome, ou o órgão filho do meu vínculo
diferente do que a passagem carrega — a tela não abre: devolve a passagem para a tela do
período de entrega, para que o período seja refeito.

[?] O acervo lido não mostra por que caminho uma passagem poderia chegar a esta tela sem
o marcador do percurso — se por alguma reentrada depois de outra tela. Como nesse caso a
tela não processa nada, não é possível dizer se isso já aconteceu em produção. Pergunta
ao site.

### RN-03 — A requisição já calculada fecha a tela

Quando a requisição daquele órgão, naquele período de cálculo, já foi dada por
calculada, a tela recusa qualquer operação que não seja a consulta, com
**\* Nao atualize. Calculo ja processado \***, e o cursor volta ao campo da operação.
Nada é gravado. A consulta continua funcionando: ela mostra a sobremesa e os comensais
do segmento e mais nada.

### RN-04 — As operações

A operação é uma só para a tela: incluir, alterar, consultar ou excluir. Qualquer outra
é recusada com **\* Operacao nao disponivel. Use INC, ALT ou CON \***, com o cursor de
volta ao campo da operação, e nada é gravado.

A recusa vem depois das conferências da passagem — o vínculo do servidor com o órgão e o
segmento cadastrado para o órgão —, e não antes delas.

### RN-05 — A consulta

Na consulta a tela termina antes das conferências da sobremesa e antes do trecho que
grava a sobremesa e os comensais do segmento: ela só lê e mostra, e a requisição do
período não é tocada.

[?] Duas coisas no acervo lido contrariam isso. Primeira: a tela pergunta
**Calcula Pedido \<S/N\>:** também na consulta, e o trecho que calcula o pedido não
confere a operação — de modo que uma consulta respondida com "S" calcula e grava o
pedido do período. Segunda: o trecho em que a passagem da consulta termina ainda grava
as sobremesas que eu tiver digitado nos dias que estiverem sem sobremesa na refeição
vizinha, e o campo onde a sobremesa é digitada não é limpo quando a tela é apresentada.
Ou a consulta não deveria chegar a esses trechos, ou eles não deveriam gravar na
consulta. Pergunta ao site.

### RN-06 — Acesso à tela, à operação e o vínculo com o órgão

A tela só abre para o código de acesso que a tem no cadastro de telas, com a estação da
sessão; a operação escolhida também é conferida contra a liberação daquele código de
acesso naquela tela. Sem a liberação, a recusa é **\* Acesso negado para esta operacao \***
e nada é gravado; sem a tela no cadastro, é **\* Tela nao disponivel \***.

O servidor tem de estar vinculado àquele órgão filho na secretaria da sessão: se o
vínculo não existe, ou se o vínculo aponta para outro órgão filho, a tela não processa —
ela devolve a passagem ao menu da alimentação escolar.

### RN-07 — O segmento tem de estar cadastrado para o órgão

O segmento que a passagem carrega tem de estar cadastrado para aquele órgão filho.
Não estando, a tela não grava nada: ela leva a operação de exclusão para a tela das
refeições e dos comensais, para que o segmento seja tratado lá.

### RN-08 — O código de sobremesa digitado tem de ser um cardápio de sobremesa vigente no segmento

Cada código que eu digitar num dia da semana tem de ser um cardápio cadastrado, marcado
como sobremesa e válido para aquele segmento, dentro da vigência do cardápio. Cada uma
das três faltas tem a sua recusa, com o cursor de volta à coluna daquele dia:

- cardápio que não existe: **\* Cardapio nao cadastrado \***;
- cardápio que existe, mas não está marcado como sobremesa:
  **\* Cardapio nao cadastrado como sobremesa \***;
- sobremesa que existe, mas não está cadastrada naquele segmento:
  **\* Cardapio nao cadastrado neste segmento \***.

### RN-09 — A sobremesa do dia tem de ser a do cardápio do dia

A sobremesa não é escolhida livremente aqui: cada cardápio do dia já traz a sua
sobremesa, e o código que eu digitar naquele dia tem de ser exatamente essa. Diferindo,
a recusa é **\<- Nao altere codigo da sobremesa \***, com o cursor de volta à coluna
daquele dia. Quando o cardápio do dia não traz sobremesa, esta conferência não é feita.

### RN-10 — A sobremesa só se sustenta sobre os comensais da refeição

A sobremesa de um dia só existe se a refeição já tiver comensais naquele dia e se eu
informar os comensais da sobremesa. Não havendo, a recusa é
**\* Informe primeiro comensais para a refeicao \***, com o cursor na coluna dos
comensais daquele dia — o que manda registrar antes os comensais da refeição, na tela
anterior.

Inversamente, informados os comensais da sobremesa, o código da sobremesa daquele dia é
obrigatório: sem ele, a recusa é **\* Informe o codigo do cardapio da sobremesa \***,
com o cursor na coluna do código daquele dia.

E o contrário também vale na abertura: escolhida uma refeição que não tem comensais
naquele segmento, a tela avisa
**\* Segmento sem comensais cadastr. para refeicao \***.

### RN-11 — Sábado e domingo só onde o segmento os atende

Se o dia da semana for sábado ou domingo e o segmento estiver cadastrado como segmento
que não recebe refeição nesses dias, a sobremesa daquele dia é recusada com
**\* Segmento nao recebe refeic. sabados e domingos \***, com o cursor na coluna do dia.

### RN-12 — Os comensais da sobremesa não podem passar das pessoas do segmento

Os comensais informados para a sobremesa de um dia não podem passar do número de pessoas
cadastrado para aquele segmento naquela refeição. Passando, a recusa é
**\<-Quant. comensais maior que o maximo permitido \***, com o cursor na coluna dos
comensais daquele dia.

### RN-13 — A frequência mensal da sobremesa

Cada sobremesa só pode ser pedida, num segmento e numa refeição, dentro de um limite
mensal e dentro de uma vigência, os dois no cadastro. Fora da vigência, ou sem cota para
o mês da data pedida, a recusa é
**\* Sobremesa nao pode ser solicitada neste mes \***.

Somando as datas da semana que está sendo pedida às sobremesas daquele mês já
solicitadas para o mesmo segmento e a mesma refeição, o total não pode passar da cota do
mês. Passando, a recusa é **\<- Ultrapassada maxima frequencia do mes \***, com o cursor
na coluna dos comensais daquele dia.

### RN-14 — A exclusão não é feita nesta tela

Escolhida a operação de excluir, esta tela não apaga nada: ou ela recusa com
**\* Exclua na tela anterior de refeicoes \***, com o cursor no campo da operação, ou
encerra a passagem em silêncio. Quem apaga a sobremesa e os comensais da refeição é a
tela anterior, a das refeições e dos comensais.

### RN-15 — As permissões de entrega da coordenadoria

Cada item calculado é conferido contra as permissões de entrega vigentes da
coordenadoria: serve a permissão que contém o período de entrega do item, da mesma
classe, que atende à quantidade mínima exigida e que seja do órgão — e, entre as que
servem, vale a de maior prioridade. O consumo acumulado da permissão, somado a esta
requisição, não pode passar do limite da permissão; passando, aquela permissão não
serve.

Não havendo nenhuma permissão que sirva, o item é descartado do pedido, **sem nenhuma
mensagem** ao operador: o pedido segue sem aquele item.

Quando o consumo passa de setenta por cento do limite da permissão, a tela apura o
percentual atingido e o registra no item do pedido — ou registra o código três, quando a
requisição consome o limite inteiro. A permissão usada passa a ter a quantidade
requisitada atualizada.

[?] O acervo lido não diz o que os setenta por cento e o registro do percentual (ou do
código três) significam para a secretaria, nem quem lê esse registro depois. Pergunta ao
site.

[?] Uma das conferências desta escolha de permissão lê o tipo do contrato de um cadastro
que **este programa nunca lê**: o valor lido é o que tiver ficado na área comum de outra
tela, e não o do contrato. Dependendo desse resto, a permissão é descartada e o item pode
sair do pedido sem nunca ter sido conferido de verdade. Ou a leitura do contrato se
perdeu, ou a conferência deveria usar outro campo. Pergunta ao site.

### RN-16 — O cálculo do pedido

Ao fim do segmento, quando é o último segmento e eu respondo **S** a
**Calcula Pedido \<S/N\>:**, a tela calcula o pedido do período. Se eu responder **N**, ou
se não for o último segmento, ela apenas grava a sobremesa e os comensais do segmento.

Antes de calcular, a tela exige, nesta ordem, e recusa com a mensagem respectiva:

- que a requisição daquele órgão exista naquele período de cálculo:
  **\* Requisicao nao cadastrada \***;
- que ela ainda não tenha sido dada por calculada: **\* Requisicao ja calculada \***;
- que nenhuma refeição do período tenha comensais de sobremesa sem o código da
  sobremesa: **\<- Segmento com comensais sem cod. sobremesa \*** (mostrando o segmento
  em falta);
- que exista pelo menos um segmento cadastrado para o cálculo:
  **\* Nao existem segmentos cadastr. para calculo \***.

O cálculo, por refeição e por dia da semana: a quantidade de comensais da sobremesa é
multiplicada pelo fator por comensal daquele cardápio naquele segmento e o resultado é
somado ao item do pedido e à quantidade calculada do período para aquela subclasse e
aquele gênero. A quantidade assim obtida é convertida nas frações de entrega do item —
o cadastro da fração mínima da secretaria e o da fração da subclasse e do gênero —
arredondando para a fração de cima quando sobra mais que a fração mínima, e ficando em
uma fração quando não cabe nenhuma. O acumulado da requisição do órgão é atualizado
respeitando o mínimo da permissão. É tomado o número do pedido daquele ano na
coordenadoria e o pedido do órgão é criado com os seus itens, já conferidos contra as
permissões. Por fim, a requisição do período é marcada como calculada.

Uma sobremesa cuja quantidade de comensais eu deixar em branco é apagada daquele dia;
onde a quantidade muda, a sobremesa e os comensais daquele dia são regravados; e quando
nada muda em relação ao que já está gravado, a tela não regrava nada.

[?] A tela prevê recusar o cálculo quando já existe pedido no intervalo de entrega e
traz essa mensagem duas vezes. Mas as duas conferências comparam a data do período com
campos que são zerados na linha imediatamente anterior e que nenhum outro trecho do
programa preenche: **as duas recusas nunca acontecem**. Ou a conferência perdeu o
cálculo desses campos, ou ela deveria usar outros. Pergunta ao site.

[?] Não havendo permissão que sirva, o item sai do pedido em silêncio — sem recusa e sem
aviso. Se isso é o esperado, ou se o operador deveria ser avisado de que um item ficou de
fora, o acervo lido não diz. Pergunta ao site.

### RN-17 — O que fica registrado e o que a tela entrega a seguir

Cada gravação da tela deixa um registro de auditoria com a tela de origem, o cadastro
atingido, a operação, a coordenadoria, o meu número de processo, a minha matrícula, a
estação, a secretaria, a data e a hora da sessão e os valores de antes e de depois.

Ao terminar o cálculo, a tela entrega a passagem à tela do pedido, já com a operação de
alteração e sem o marcador do percurso; e ela não pergunta confirmação antes de gravar
nem avisa depois que gravou. Nas recusas, ela devolve a passagem ao menu da alimentação
escolar, à tela do período de entrega ou à tela das refeições e dos comensais, conforme
o que faltou.

---

## Cenários BDD

```gherkin
Funcionalidade: Sobremesa por refeição do segmento e cálculo do pedido da alimentação escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E052T
    E que cheguei a ela pelo encadeamento da tela do período de entrega, com órgão
      filho, coordenadoria, segmento, período de cálculo e período de entrega
    E que a minha sessão carrega a secretaria, a matrícula, o código de acesso e a
      estação

  Cenário: Calcular o pedido do período
    Dado que existe requisição do órgão naquele período de cálculo
    E que ela ainda não foi dada por calculada
    E que é o último segmento do órgão
    E que todas as refeições que têm comensais de sobremesa têm o código da sobremesa
    Quando informo, em cada dia, a sobremesa e os comensais da sobremesa
    E escolho a operação de alterar
    E respondo S a "Calcula Pedido <S/N>:"
    Então o pedido do órgão é criado, com os seus itens e o número do pedido do ano
    E a quantidade requisitada acumulada do órgão é atualizada
    E a permissão de entrega usada tem a quantidade requisitada atualizada
    E a requisição do período fica marcada como calculada
    E a passagem segue para a tela do pedido

  Cenário: Gravar a sobremesa e os comensais sem calcular
    Dado que existe requisição do órgão naquele período de cálculo
    E que ela ainda não foi dada por calculada
    E que não é o último segmento, ou que respondo N a "Calcula Pedido <S/N>:"
    Quando informo, em cada dia, a sobremesa e os comensais da sobremesa
    E escolho a operação de alterar
    Então a sobremesa e os comensais daquele segmento são gravados
    E nenhum pedido é calculado

  Cenário: A sobremesa em branco apaga a sobremesa daquele dia
    Dado que existe sobremesa gravada para um dia da refeição
    Quando escolho a operação de alterar e deixo os comensais daquele dia em branco
    Então a sobremesa daquele dia é apagada

  Cenário: Nada mudou, nada é regravado
    Dado que a sobremesa e os comensais que informei são iguais aos que estão gravados
    Quando escolho a operação de alterar
    Então a tela não regrava a sobremesa daquela refeição

  Cenário: Refeição sem comensais cadastrados no segmento
    Dado que a refeição escolhida não tem comensais naquele segmento
    Quando abro a tela E052T
    Então vejo "* Segmento sem comensais cadastr. para refeicao *"

  Cenário: Comensais da sobremesa sem o código da sobremesa
    Dado que existe comensais de sobremesa informados para um dia
    Quando deixo o código da sobremesa daquele dia em branco
    Então vejo "* Informe o codigo do cardapio da sobremesa *"
    E o cursor fica na coluna do código daquele dia
    E nada é gravado

  Cenário: Sobremesa sem comensais na refeição
    Dado que a refeição não tem comensais naquele dia
    E que informei a sobremesa daquele dia
    Então vejo "* Informe primeiro comensais para a refeicao *"
    E o cursor fica na coluna dos comensais daquele dia
    E nada é gravado

  Cenário: Consultar não grava
    Dado que existe sobremesa gravada para o segmento
    Quando escolho a operação de consultar
    E deixo em branco a pergunta do cálculo
    Então a tela mostra a sobremesa e os comensais do segmento
    E nenhuma sobremesa é criada, alterada ou apagada
    E nenhum pedido é calculado

  Cenário: Operação fora das previstas
    Quando informo uma operação diferente de incluir, alterar, consultar e excluir
    Então vejo "* Operacao nao disponivel. Use INC, ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Requisição já calculada e operação de alterar
    Dado que a requisição do órgão naquele período já foi dada por calculada
    Quando escolho a operação de alterar
    Então vejo "* Nao atualize. Calculo ja processado *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Requisição já calculada e consulta
    Dado que a requisição do órgão naquele período já foi dada por calculada
    Quando escolho a operação de consultar
    Então a tela mostra a sobremesa e os comensais do segmento
    E vejo o aviso "* REQUISICAO PROCESSADA *"
    E nada é gravado

  Cenário: A tela aberta fora do percurso da tela do período
    Dado que a passagem não traz o marcador do percurso da tela do período de entrega
    Quando mando processar a tela
    Então nada é processado
    E sou levado ao menu da alimentação escolar, que avisa
      "* Acesso deve ser feito pela tela E050T *"

  Cenário: O período deixado pela tela anterior está incoerente
    Dado que a passagem traz, por exemplo, a data limite anterior à data de início
    Quando abro a tela E052T
    Então a tela não abre
    E sou levado de volta à tela do período de entrega

  Cenário: Segmento não cadastrado para o órgão
    Dado que o segmento da passagem não está cadastrado para aquele órgão filho
    Quando mando processar a tela
    Então nada é gravado
    E a operação de exclusão é levada para a tela das refeições e dos comensais

  Cenário: Servidor sem vínculo com o órgão filho
    Dado que o meu vínculo na secretaria aponta para outro órgão filho, ou não existe
    Quando mando processar a tela
    Então nada é gravado
    E sou levado ao menu da alimentação escolar

  Cenário: Sem autorização para a operação
    Dado que o meu código de acesso não tem a operação escolhida liberada nesta tela
    Quando escolho a operação de alterar
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Código de sobremesa não cadastrado
    Quando informo, num dia, um código de cardápio que não existe
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor fica na coluna daquele dia
    E nada é gravado

  Cenário: Código que não é sobremesa
    Quando informo, num dia, um cardápio que não está marcado como sobremesa
    Então vejo "* Cardapio nao cadastrado como sobremesa *"
    E o cursor fica na coluna daquele dia
    E nada é gravado

  Cenário: Sobremesa não cadastrada no segmento
    Quando informo, num dia, uma sobremesa que não vale para aquele segmento
    Então vejo "* Cardapio nao cadastrado neste segmento *"
    E o cursor fica na coluna daquele dia
    E nada é gravado

  Cenário: Sobremesa diferente da do cardápio do dia
    Dado que o cardápio daquele dia traz outra sobremesa
    Quando informo uma sobremesa diferente da dele
    Então vejo "<- Nao altere codigo da sobremesa *"
    E o cursor fica na coluna daquele dia
    E nada é gravado

  Cenário: Sábado ou domingo em segmento que não os atende
    Dado que o segmento está cadastrado como segmento que não recebe refeição no fim
      de semana
    Quando informo a sobremesa de um sábado ou de um domingo
    Então vejo "* Segmento nao recebe refeic. sabados e domingos *"
    E o cursor fica na coluna daquele dia
    E nada é gravado

  Cenário: Comensais da sobremesa acima das pessoas do segmento
    Quando informo, num dia, mais comensais de sobremesa do que as pessoas
      cadastradas para aquele segmento naquela refeição
    Então vejo "<-Quant. comensais maior que o maximo permitido *"
    E o cursor fica na coluna dos comensais daquele dia
    E nada é gravado

  Cenário: Sobremesa fora da vigência ou sem cota no mês
    Dado que a sobremesa informada não vale para o mês daquela data, ou está fora da
      sua vigência no segmento e na refeição
    Quando informo a sobremesa daquele dia
    Então vejo "* Sobremesa nao pode ser solicitada neste mes *"
    E o cursor fica na coluna daquele dia
    E nada é gravado

  Cenário: Frequência do mês ultrapassada
    Dado que a soma das datas pedidas naquela semana com as já solicitadas no mês
      passa da cota mensal daquela sobremesa
    Quando informo a sobremesa daquele dia
    Então vejo "<- Ultrapassada maxima frequencia do mes *"
    E o cursor fica na coluna dos comensais daquele dia
    E nada é gravado

  Cenário: Excluir nesta tela
    Quando escolho a operação de excluir
    Então vejo "* Exclua na tela anterior de refeicoes *"
    E o cursor volta ao campo da operação
    E nada é apagado aqui

  Cenário: Requisição não cadastrada no período
    Dado que não existe requisição daquele órgão naquele período de cálculo
    Quando respondo S a "Calcula Pedido <S/N>:"
    Então vejo "* Requisicao nao cadastrada *"
    E nada é calculado

  Cenário: Requisição já calculada no momento do cálculo
    Dado que a requisição daquele órgão naquele período já foi dada por calculada
    Quando respondo S a "Calcula Pedido <S/N>:"
    Então vejo "* Requisicao ja calculada *"
    E nada é calculado de novo

  Cenário: Segmento com comensais de sobremesa sem o código da sobremesa
    Dado que alguma refeição do período tem comensais de sobremesa sem o código
    Quando respondo S a "Calcula Pedido <S/N>:"
    Então vejo "<- Segmento com comensais sem cod. sobremesa *", com o segmento
    E nada é calculado

  Cenário: Não existem segmentos cadastrados para o cálculo
    Dado que não existe nenhum segmento cadastrado para aquele período de cálculo
    Quando respondo S a "Calcula Pedido <S/N>:"
    Então vejo "* Nao existem segmentos cadastr. para calculo *"
    E nada é calculado

  Cenário: Item sem permissão de entrega que o comporte
    Dado que nenhuma permissão de entrega vigente da coordenadoria serve para o item
    Quando respondo S a "Calcula Pedido <S/N>:"
    Então o item é descartado do pedido, sem nenhuma mensagem
    E o pedido segue com os demais itens

  Cenário: Consumo acima de setenta por cento do limite da permissão
    Dado que a requisição faz o consumo de uma permissão passar de setenta por cento
      do seu limite
    Quando respondo S a "Calcula Pedido <S/N>:"
    Então o percentual atingido é registrado no item do pedido
    E a permissão usada tem a quantidade requisitada atualizada

  Cenário: Cálculo com pedido já existente no intervalo de entrega
    Dado que já existe pedido no intervalo de entrega do período
    Quando respondo S a "Calcula Pedido <S/N>:"
    Então o cálculo acontece assim mesmo
    E nenhuma recusa por pedido já existente é mostrada

  Cenário: A exclusão de uma refeição é feita na tela anterior
    Dado que existe sobremesa gravada para a refeição
    Quando escolho a operação de excluir na tela das refeições e dos comensais
    Então a sobremesa e os comensais daquela refeição são apagados
    E esta tela não é tocada

  Cenário: A recusa não grava nada
    Dado que a minha passagem foi recusada por alguma conferência
    Quando a tela termina a passagem
    Então nenhuma sobremesa foi criada, alterada ou apagada
    E nenhum pedido foi calculado
    E nenhum registro de auditoria foi gerado

  Cenário: Cada gravação deixa auditoria
    Dado que a passagem passou por todas as conferências
    Quando a tela grava a sobremesa e os comensais, ou calcula o pedido
    Então fica um registro de auditoria com a tela de origem, o cadastro atingido, a
      operação, a coordenadoria, o meu número de processo, a minha matrícula, a
      estação, a secretaria, a data e a hora da sessão e os valores de antes e depois
```
