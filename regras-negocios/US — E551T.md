# US — E551T — Planejamento de comensais e cardápios do calendário

## Estória

Como **servidor da coordenação regional escolar**, quero **registrar, para cada
segmento de atendimento e cada refeição de um órgão filho, o cardápio e a
quantidade de comensais de cada dia do calendário escolar**, para que **a
secretaria saiba quantas refeições preparar e distribuir em cada dia, e com qual
cardápio**.

O planejamento é o que transforma o atendimento do órgão em número: o segmento
diz qual público aquele órgão cobre, a refeição diz qual refeição é, e cada dia do
calendário recebe o cardápio e o número de comensais. Sem esse registro não há
como dimensionar a produção nem a distribuição da merenda, porque é o número de
comensais por dia que vira quantidade a preparar. E o planejamento só existe
dentro do calendário do órgão: fora dele não há onde registrar, e o dia que está
marcado como feriado, ou que ainda não tem cardápio cadastrado, não aceita
comensais.

## Contexto

Jornada S000M → E000M → E550M → E550T → E551T.
Ator: servidor de CRE — planeja, por segmento de atendimento e por refeição de um
órgão filho, o cardápio e o número de comensais de cada dia do calendário escolar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A E551T não se abre por menu: quem a abre é a **E550T**, a tela do calendário do
órgão. É a E550T que decide em que modo a E551T abre — consulta ou manutenção — e é
ela que deixa pronto o que a E551T usa: o órgão filho, a coordenação regional
escolar, o indicador de creche, as datas de início e de fim do calendário, o
segmento de atendimento e os **sete primeiros dias** do calendário, cada um com a
sua data, o seu dia da semana e o tipo de cardápio vigente. Quando o calendário não
está completo, é para a E550T que se volta.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A grade tem 6 refeições e 7 dias, e cada célula tem cardápio e quantidade

A tela apresenta **6 linhas**, uma por refeição, e **7 colunas de dias** — os sete
primeiros dias do calendário, contados a partir da data de início. São **42
células** e, em cada uma, **2 campos**: o cardápio (5 dígitos) e a quantidade de
comensais (5 dígitos), o que dá **84 campos dentro da grade**. Fora da grade, o
cabeçalho identifica o órgão filho (8 dígitos), a coordenação regional escolar (2),
as duas datas do calendário (dia, mês e ano de cada uma), o código do segmento (2),
a opção de manutenção e dois campos de passagem — o segmento anterior e o segmento
seguinte.

### RN-02 — A tela só abre vinda da E550T; de outra origem, volta para o menu E550M

A E551T não é aberta por menu. Se a origem registrada na sessão não for a E550T, a
tela não trabalha: devolve o servidor ao menu **E550M**, sem gravar nada. É a E550T
quem escolhe o modo em que a tela abre — em consulta, quando o calendário foi
consultado lá, ou em manutenção, quando a inclusão ou a alteração do cálculo foi
confirmada lá.

### RN-03 — A tela trabalha sobre o que a E550T deixou

O órgão filho, a coordenação regional escolar, o indicador de creche, as datas de
início e de fim do calendário, o segmento e os sete dias — cada um com a data, o
dia da semana e o tipo de cardápio — não são digitados aqui: vêm da E550T, que os
monta a partir do cadastro do calendário e do cadastro do segmento. A E551T apenas
os mostra e os usa para localizar o planejamento.

[?] O tipo de cardápio aparece como **uma letra, de A a D**, e o cadastro que o
mantém apenas lista as quatro letras, sem dizer o que cada uma significa em
negócio. Pergunta ao site.

### RN-04 — Calendário incompleto (ou órgão preso diferente) devolve para a E550T, já em inclusão

Antes de deixar trabalhar, a tela confere o que recebeu da E550T. Devolve o
servidor para a **E550T com a opção de inclusão já marcada** quando qualquer uma
destas cinco condições ocorre: a data de início do calendário está zerada; a data
de fim está zerada; a data de fim é anterior à de início; falta o tipo de cardápio
ou o dia da semana em algum dos sete dias; ou o indicador de creche está em branco.
A mesma devolução acontece quando a sessão tem um **órgão filho preso** ao servidor
e esse órgão não é o órgão do calendário.

[?] O órgão preso do servidor é zerado na reinicialização da sessão no corpus, e a
única carga do órgão filho está no vínculo do LOGON com a secretaria; a passagem
desse valor para o nível que esta tela lê não aparece na árvore expandida. Se a
carga não vier do runtime, a conferência do órgão preso nunca dispara. Pergunta ao
site.

### RN-05 — O acesso é conferido por tela e o vínculo do servidor com o órgão é exigido

Ao abrir, o sistema confere se o servidor tem acesso à tela; ao confirmar, confere
de novo o acesso e a autorização da operação — consultar, incluir, alterar ou
excluir, conforme o caso. Sem autorização, a operação para antes de qualquer
gravação. Passando por aí, a tela exige o **vínculo da matrícula com o órgão do
calendário**: se a matrícula não tem esse vínculo, ou se o vínculo dela carrega um
órgão filho diferente do órgão do calendário, a tela limpa a opção e devolve o
servidor ao menu **E550M**, sem gravar.

[?] A devolução ao E550M, nesses dois casos, sai sem mensagem própria: o programa
não escreve nenhum aviso antes de mandar de volta. Não dá para concluir do fonte se
o servidor recebe alguma explicação na tela de destino. Pergunta ao site.

### RN-06 — A opção de manutenção aceita INC, ALT, EXC e CON; nada mais

A tela é comandada por uma opção digitada. Só quatro valores são aceitos —
**INC** (incluir), **ALT** (alterar), **EXC** (excluir) e **CON** (consultar).
Qualquer outra coisa é recusada com **\* Opcao nao disponivel. Use INC, ALT, EXC ou
CON \***, com o cursor de volta na opção, e nada é gravado.

[?] A guarda do programa compara a opção digitada com códigos internos de operação
que não são as siglas que a mensagem manda usar. Ou o terminal traduz a sigla antes
de enviar, ou a mensagem está desalinhada da guarda. Não concluo qual dos dois.
Pergunta ao site.

### RN-07 — A primeira linha vem preenchida do cadastro; as demais são digitadas; linha sem refeição é ignorada

Ao abrir, a tela carrega a **primeira refeição cadastrada para o órgão** na primeira
linha e, com ela, o que já estiver planejado para aquele segmento. As outras cinco
linhas ficam para o servidor digitar a refeição e as quantidades. Linha sem código
de refeição é ignorada em silêncio, inclusive na gravação.

### RN-08 — Consultar mostra o que está planejado e não grava nada

Na consulta a tela apenas exibe: mostra os cardápios e as quantidades já
registrados para cada refeição do segmento e não propõe cardápios nem grava nada.
A passagem de gravação é desviada de propósito quando a opção é a de consulta.

### RN-09 — Sem planejamento, a tela propõe os cardápios do tipo de cardápio vigente

Quando ainda não existe planejamento para aquela refeição no segmento, a tela não
deixa a grade vazia: ela lê o **máximo de comensais da refeição** no segmento e, se
esse cadastro existe e está ativo, busca os cardápios registrados para o **tipo de
cardápio vigente no primeiro dia do calendário** e preenche com eles as sete
posições de cardápio. A proposta só vale se o conjunto de cardápios do tipo já
estiver em vigor na data de início do calendário; caso contrário a grade fica como
estava. As quantidades continuam em branco e são o que o servidor vai digitar.

[?] A ordem em que a proposta preenche os dias não é a ordem segunda-a-domingo: a
primeira posição recebe o cardápio cadastrado para **terça-feira** e a sétima vem
de outro conjunto, pela segunda-feira seguinte. Isso só fecha se o calendário
sempre começar numa terça, o que o corpus não afirma. Ou a convenção do calendário
é essa, ou a proposta troca o cardápio de lugar. Pergunta ao site.

### RN-10 — Sem comensais cadastrados para a refeição, a tela recusa ao carregar

Se, para a refeição que a tela está carregando, o segmento não tem o máximo de
comensais cadastrado e ativo **e** também não há cardápio de tipo vigente para
propor, não há o que planejar: a tela recusa com **\* Segmento sem comensais
cadastr. para refeicao \*** e devolve o servidor sem gravar.

[?] Existe no programa uma segunda recusa, **\* Planejamento nao cadastrado \***,
que dispara quando um certo estado da sessão está marcado como "C" — mas nenhum
programa desta jornada produz esse estado, e o próprio programa o reinicia antes de
testá-lo. Ou a recusa é inalcançável, ou o estado vem de outra tela da sessão.
Pergunta ao site.

### RN-11 — O segmento informado tem que pertencer ao órgão

O código do segmento digitado é conferido contra o vínculo do órgão com os seus
segmentos. Se o órgão não tem aquele segmento, a tela recusa: com **\* Orgao nao
pertence a este segmento. Use EXC \*** quando já existe planejamento registrado
para esse segmento — nesse caso, o servidor só pode excluir —, e com **\* Orgao nao
pertence a este segmento \*** quando não existe. Nada é gravado.

### RN-12 — O máximo de comensais da refeição é exigido e tem que estar ativo

Para gravar, o segmento precisa ter o **máximo de comensais** cadastrado para
aquela refeição. Faltando, a tela recusa com **\* Maximo comensais nao cad. para
esta refeicao \***. Se o cadastro existe mas está marcado como inativo, a recusa é
**\* Maximo de comensais inativo \***. Nas duas, o cursor volta para as quantidades
da linha e nada é gravado.

### RN-13 — Em cada dia, a quantidade não pode passar do máximo e o cardápio tem que ser informado

Para os dias em que o servidor informou quantidade, a tela confere duas coisas. A
quantidade não pode ser maior que o máximo de comensais do segmento para aquela
refeição: passando, recusa com **\<-Quant. comensais maior que o maximo permitido
\*** e devolve o cursor à quantidade do dia. E o cardápio do dia não pode ficar em
branco: recusa com **\* Informe cardapio para a refeicao \***. Dia sem quantidade
informada é pulado, e nada é gravado enquanto houver recusa.

### RN-14 — O cardápio do dia tem que estar cadastrado no segmento e previsto para a refeição

O cardápio informado para um dia é procurado no cadastro de cardápios do segmento.
Se não está cadastrado para aquele segmento — ou se a vigência dele começa depois
da data de início do calendário —, a recusa é **\* Cardapio nao cadastrado neste
segmento \***. Se está cadastrado no segmento mas não está previsto para aquela
refeição, a recusa é **\* Cardapio nao cadastrado nesta refeicao \***.

[?] A conferência de vigência do cardápio usa sempre a **data de início do
calendário**, mesmo quando o dia que está sendo validado é o terceiro, o quinto ou
o sétimo. Não dá para concluir do fonte se isso é intencional — a vigência ser
semanal — ou se o cardápio dos últimos dias deveria ser conferido contra a data do
próprio dia. Pergunta ao site.

### RN-15 — Sábado e domingo só quando o segmento recebe refeição nesses dias

Se o dia que está sendo validado cai em sábado ou domingo, a tela olha a marcação
de sábado/domingo do vínculo do órgão com o segmento. Quando o vínculo não recebe
refeição nesses dias, a recusa é **\* Segmento nao recebe refeic. sabados e
domingos \*** e aquele dia não é gravado.

### RN-16 — Feriado não recebe comensais

Se o dia do calendário está cadastrado como feriado para o órgão, a tela recusa com
**\* Feriado - nao informe comensais \***. O feriado é procurado pela data completa
do dia — dia, mês e ano contados a partir do início do calendário.

### RN-17 — Alterar só grava se algo mudou

Na alteração, a tela compara o que está na grade com o que está gravado, cardápio a
cardápio e quantidade a quantidade. Se nada mudou, a tela não executa gravação
nenhuma: a operação termina em silêncio, sem mensagem.

### RN-18 — Zerar as sete quantidades apaga o planejamento daquela refeição

Se a refeição já tem planejamento e o servidor deixa as **sete quantidades** em
branco (zero), o sistema entende que a refeição saiu do planejamento e apaga o
registro daquela refeição no segmento.

### RN-19 — Excluir tira o segmento inteiro do planejamento, e exige que ele exista

A exclusão não é por refeição: ela apaga **todo o planejamento daquele segmento**,
em todas as refeições. E exige que exista: se o segmento não tem planejamento
registrado — e o servidor não está passando de um segmento para outro pelos campos
de passagem —, a recusa é **\* Segmento sem comensais cadastrados \*** e nada é
apagado.

### RN-20 — A sobremesa do dia acompanha o cardápio informado

Quando a refeição tem sobremesa, o servidor não precisa informá-la: para cada dia
com quantidade, o sistema pega no cadastro do cardápio a sobremesa prevista para
aquele cardápio e grava, junto com o cardápio e a quantidade de comensais, o
cardápio de sobremesa do dia e a quantidade correspondente. Nos dias sem
quantidade, a sobremesa também fica zerada. Se a refeição não tem sobremesa, nada
disso é gravado.

### RN-21 — A requisição do cálculo nasce com o primeiro planejamento e sai com o último

Enquanto existir qualquer planejamento no calendário do órgão, tem que existir a
**requisição do cálculo** daquele calendário. Ela é criada junto com a primeira
gravação, se ainda não existir; e, quando o último planejamento do calendário é
excluído, ela é apagada também. É o que mantém o cálculo do órgão coerente com o
que foi planejado: requisição sem planejamento nenhum não fica de pé.

### RN-22 — A tela anda entre os segmentos; não havendo segmento anterior, avisa

Pelos campos de passagem, o servidor anda para o segmento anterior ou para o
seguinte sem sair da tela: o sistema procura esse segmento nos cadastros do órgão e
reposiciona a tela nele. Se não existir nem o segmento nem planejamento para ele na
direção pedida, a recusa é **\* Nao existem segmentos anteriores \*** e a tela fica
onde está. Depois de uma exclusão, a tela se reposiciona no segmento vizinho já em
modo de inclusão; e se o órgão ficar sem nenhum segmento, ela devolve o servidor à
E550T em consulta.

[?] Os dois campos de passagem são de um caractere e não têm rótulo de negócio que
diga o que marcar. E a saída desta tela para a **E552T** depende de um campo de
requisição estar marcado como "C" — valor que nenhum programa desta jornada
escreve; o único destino que o programa atribui a esse campo é vazio. Ou a saída
registrada no grafo é inalcançável por aqui, ou o valor chega de fora desta árvore.
Pergunta ao site.

### RN-23 — A tela só escreve em dois cadastros; os outros onze são leitura

O gerador declara, para cada cadastro que a tela enxerga, as rotinas de gravar,
apagar e travar. Declaração não é uso: a E551T enxerga **13 cadastros**, e só
grava — e apaga — em **2**: o planejamento de comensais e a requisição do cálculo.
Os outros **11** ela apenas lê, para conferir órgão, refeição, segmento, cardápio,
feriado, máximo de comensais, acesso e vínculo do servidor.

### RN-24 — Falha de banco interrompe a gravação e avisa

Todo acesso a dados testa o erro do banco: erro de leitura vira a ação 53 e erro de
gravação ou de exclusão vira a ação 55, ambas despachadas pela rotina de
comunicação. A transação para ali, sem completar o resto — o que não foi gravado
não é considerado gravado.

---

## Cenários BDD

```gherkin
Funcionalidade: Planejar os comensais e os cardápios de cada dia do calendário de um órgão filho, por segmento de atendimento e refeição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E551T

  Cenário: RN-01 e RN-03 — o que a tela mostra
    Dado que o calendário do órgão está completo na E550T
    Quando abro a E551T
    Então vejo o órgão filho, a coordenação regional escolar, as datas de início e de fim do calendário e o segmento
    E vejo 6 linhas de refeição e, em cada uma, 7 colunas de dias com o cardápio e a quantidade de comensais

  Cenário: RN-02 — a tela foi aberta por outro caminho
    Dado que a tela não foi aberta pela E550T
    Quando confirmo
    Então volto ao menu E550M
    E nada é gravado

  Cenário: RN-04 — calendário com o fim antes do início
    Dado que a data de fim do calendário é anterior à de início
    Quando abro a E551T
    Então volto à E550T com a opção de inclusão já marcada
    E nada é gravado

  Cenário: RN-04 — falta o tipo de cardápio em um dos dias
    Dado que um dos sete dias do calendário não tem tipo de cardápio
    Quando abro a E551T
    Então volto à E550T com a opção de inclusão já marcada

  Cenário: RN-05 — sem vínculo com o órgão do calendário
    Dado que a minha matrícula não tem vínculo com o órgão do calendário
    Quando confirmo
    Então a opção é limpa e volto ao menu E550M
    E nada é gravado

  Cenário: RN-06 — opção de manutenção não disponível
    Quando confirmo com uma opção diferente de INC, ALT, EXC e CON
    Então vejo "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E nada é gravado

  Cenário: RN-07 — a primeira linha e as demais
    Dado que o órgão tem refeições cadastradas
    Quando abro a E551T
    Então a primeira linha vem com a primeira refeição cadastrada do órgão
    E as outras linhas ficam em branco para eu digitar

  Cenário: RN-07 — linha sem refeição
    Dado que deixo uma linha sem código de refeição
    Quando confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada

  Cenário: RN-08 — consultar o planejamento do segmento
    Dado que estou na tela E551T com a opção CON
    E o segmento já tem planejamento para a refeição
    Quando confirmo
    Então vejo os cardápios e as quantidades de comensais já registrados para cada dia
    E nada é gravado

  Cenário: RN-09 — a tela propõe os cardápios do tipo vigente
    Dado que o segmento não tem planejamento para a refeição
    E existe máximo de comensais ativo para a refeição no segmento
    E os cardápios do tipo vigente já valem na data de início do calendário
    Quando abro a E551T
    Então as sete posições de cardápio vêm preenchidas com os cardápios daquele tipo
    E as quantidades continuam em branco

  Cenário: RN-10 — segmento sem comensais cadastrados para a refeição
    Dado que o segmento não tem máximo de comensais cadastrado para a refeição
    E não há cardápio de tipo vigente para propor
    Quando abro a E551T
    Então vejo "* Segmento sem comensais cadastr. para refeicao *"
    E nada é gravado

  Cenário: RN-11 — segmento que não pertence ao órgão, sem planejamento
    Dado que o órgão não tem o segmento informado
    Quando confirmo a inclusão
    Então vejo "* Orgao nao pertence a este segmento *"
    E nada é gravado

  Cenário: RN-11 — segmento que não pertence ao órgão, mas com planejamento
    Dado que já existe planejamento registrado para o segmento informado
    E o órgão não tem mais esse segmento
    Quando confirmo a inclusão
    Então vejo "* Orgao nao pertence a este segmento. Use EXC *"
    E nada é gravado

  Cenário: RN-12 — máximo de comensais não cadastrado para a refeição
    Dado que o segmento não tem máximo de comensais para a refeição
    Quando confirmo a inclusão
    Então vejo "* Maximo comensais nao cad. para esta refeicao *"
    E nada é gravado

  Cenário: RN-12 — máximo de comensais inativo
    Dado que o máximo de comensais do segmento está marcado como inativo
    Quando confirmo a inclusão
    Então vejo "* Maximo de comensais inativo *"
    E nada é gravado

  Cenário: RN-13 — quantidade acima do máximo permitido
    Dado que informo, em um dia, quantidade maior que o máximo de comensais do segmento
    Quando confirmo
    Então vejo "<-Quant. comensais maior que o maximo permitido *"
    E o cursor volta para a quantidade daquele dia
    E nada é gravado

  Cenário: RN-13 — dia com quantidade e sem cardápio
    Dado que informo quantidade em um dia e deixo o cardápio dele em branco
    Quando confirmo
    Então vejo "* Informe cardapio para a refeicao *"
    E nada é gravado

  Cenário: RN-14 — cardápio não cadastrado no segmento
    Dado que informo um cardápio que não está cadastrado para o segmento
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado neste segmento *"
    E nada é gravado

  Cenário: RN-14 — cardápio não previsto para a refeição
    Dado que informo um cardápio cadastrado no segmento, mas não previsto para aquela refeição
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado nesta refeicao *"
    E nada é gravado

  Cenário: RN-15 — sábado e domingo não atendidos pelo segmento
    Dado que um dos dias do calendário cai em sábado ou domingo
    E o vínculo do órgão com o segmento não recebe refeição nesses dias
    Quando informo quantidade nesse dia e confirmo
    Então vejo "* Segmento nao recebe refeic. sabados e domingos *"
    E nada é gravado

  Cenário: RN-16 — dia de feriado
    Dado que um dos dias do calendário está cadastrado como feriado para o órgão
    Quando informo quantidade nesse dia e confirmo
    Então vejo "* Feriado - nao informe comensais *"
    E nada é gravado

  Cenário: RN-19 e RN-23 — incluir o planejamento de uma refeição
    Dado que estou na tela E551T com a opção INC
    E o segmento tem máximo de comensais ativo para a refeição
    E informo o cardápio e a quantidade de comensais em cada dia que tem atendimento
    Quando confirmo
    Então o planejamento daquela refeição no segmento é gravado
    E nada mais é escrito além do planejamento e da requisição do cálculo

  Cenário: RN-20 — a sobremesa acompanha o cardápio
    Dado que a refeição tem sobremesa
    E informo cardápio e quantidade em um dia
    Quando confirmo
    Então o planejamento do dia é gravado com o cardápio informado, a quantidade de comensais, o cardápio de sobremesa previsto para aquele cardápio e a quantidade correspondente

  Cenário: RN-17 — alterar sem mudar nada
    Dado que o segmento já tem o planejamento da refeição
    Quando confirmo a alteração sem mudar nenhum cardápio e nenhuma quantidade
    Então nenhuma gravação é executada
    E nenhuma mensagem é mostrada

  Cenário: RN-17 — alterar um dia e gravar
    Dado que o segmento já tem o planejamento da refeição
    Quando mudo a quantidade de um dia e confirmo a alteração
    Então o planejamento daquela refeição passa a ter a nova quantidade naquele dia
    E os demais dias ficam como estavam

  Cenário: RN-18 — zerar todas as quantidades
    Dado que o segmento já tem o planejamento da refeição
    Quando deixo as sete quantidades em branco e confirmo
    Então o planejamento daquela refeição no segmento é apagado

  Cenário: RN-19 — excluir o planejamento de um segmento
    Dado que o segmento tem planejamento registrado
    Quando confirmo a exclusão
    Então todo o planejamento daquele segmento, em todas as refeições, é apagado

  Cenário: RN-19 — excluir um segmento sem planejamento
    Dado que o segmento não tem planejamento registrado
    Quando confirmo a exclusão
    Então vejo "* Segmento sem comensais cadastrados *"
    E nada é apagado

  Cenário: RN-21 — a requisição nasce com o primeiro planejamento
    Dado que o calendário do órgão ainda não tem planejamento nenhum
    E a requisição do cálculo ainda não existe
    Quando gravo o primeiro planejamento
    Então a requisição do cálculo daquele calendário é criada

  Cenário: RN-21 — a requisição sai com o último planejamento
    Dado que o segmento tem o último planejamento daquele calendário
    Quando confirmo a exclusão
    Então o planejamento é apagado
    E a requisição do cálculo daquele calendário também é apagada

  Cenário: RN-22 — não existem segmentos anteriores
    Dado que estou no primeiro segmento do órgão
    Quando peço o segmento anterior
    Então vejo "* Nao existem segmentos anteriores *"
    E a tela continua no segmento em que eu estava

  Cenário: RN-24 — falha de banco durante a gravação
    Dado que a gravação do planejamento falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E o planejamento não é considerado gravado
```
