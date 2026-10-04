# US — E055T — Distribuição e aprovação do pedido da alimentação escolar

## Estória

Como **servidor de CRE**, quero **distribuir, gênero a gênero, a quantidade calculada do
pedido da alimentação escolar entre os dias de entrega e responder pela aprovação do
pedido**, para que **a entrega saia dia a dia dentro do que foi calculado e do que a
permissão de entrega do fornecedor permite, sem que a secretaria descubra depois que um
dia ficou sem quantidade ou que o total passou do permitido**.

O pedido da alimentação escolar de um órgão nasce de uma corrente: o período de entrega da
coordenadoria, os segmentos do órgão, os comensais de cada refeição, a sobremesa e, por
fim, a quantidade calculada de cada gênero. Esta é a última volta dessa corrente antes de o
pedido virar requisição: é aqui que a quantidade calculada de cada subclasse e gênero é
repartida entre os dias de entrega e que a repartição é conferida contra as permissões de
entrega da coordenadoria. Uma repartição errada não falha na hora: nasce um pedido com dia
sem quantidade, com quantidade acima da permissão, ou com um item acumulado sem a
quantidade recebida na nota.

## Contexto

Jornada S000M → E000M → E050M → E055T.

Ator: servidor de CRE — informa, para cada subclasse e gênero, a quantidade calculada que
vai em cada dia de entrega e responde pela aprovação do pedido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Esta tela não é aberta por menu com uma operação escolhida por mim: ela é a última etapa do
encadeamento do pedido e recebe pronta a passagem da tela anterior — o órgão, a
coordenadoria, o fornecedor, o pedido e o período de entrega. Ela também é chamada pela
tela de preparo do pedido quando o preparo é mandado para distribuição, e a passagem que
essa tela deixa é a mesma. Do que ela faz, o que sobra é a distribuição por dia gravada no
item calculado, a quantidade distribuída do item do pedido, a permissão de entrega
atualizada e, quando eu aprovo, a requisição.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — O que esta tela mantém

Para cada órgão filho SDI, cada coordenadoria regional escolar e cada pedido, a tela mantém
a distribuição da quantidade calculada de cada par de subclasse e gênero pelos dias de
entrega: eu informo quanto daquele gênero sai em cada um dos dias e a tela guarda essa
repartição.

No alto ela mostra o órgão filho e o seu nome, a coordenadoria, o número do pedido, o ano
da entrega, o fornecedor e a sua razão social, o operador e o seu nome, o dia, o mês e o
ano do início do período, o dia, o mês e o ano limite, o tipo de contrato e o cartão, além
das datas dos dias de entrega. Cada linha traz **9 campos** — a subclasse, o gênero, a
quantidade calculada, as **5** quantidades (uma por dia de entrega) e a situação — e a tela
mostra **12 linhas** por vez. A quantidade calculada é a que veio do cálculo do pedido e,
quando as cinco quantidades da linha estão zeradas, aparece um asterisco ao lado dela.

[?] A situação de cada linha é um campo que a tela nunca preenche: ela só o lê. O que a
máscara coloca ali, e o que isso significa, é pergunta ao site.

### RN-02 — A tela abre pelo encadeamento, sempre em alteração, com o pedido do órgão à mostra

Esta tela não tem operação de consulta nem é aberta para escolher uma operação: ela abre
sempre em alteração, e o que a tela anterior deixou na passagem é o que ela mostra. Se a
passagem chega com o campo da tela seguinte preenchido, ou já marcada por uma recusa
anterior, a tela encerra sem processar nada.

Existindo um item calculado para o órgão, a tela o apresenta e mostra o aviso para teclar
enter para o pedido; e quando o pedido já tem alguma quantidade distribuída, ela pergunta,
ao pé da última linha, **Aprova Pedido <S/N>:**.

[?] O campo da tela seguinte não é atribuído em nenhum ponto do programa; se é a máscara ou
o ambiente que o deixa em branco, é pergunta ao site.

[?] Como não há consulta, o pedido já distribuído só pode ser revisto pela alteração — e é
nessa mesma passagem que a pergunta da aprovação aparece. Se quem só veio corrigir a
distribuição deve ser obrigado a responder à pergunta, é pergunta ao site.

[?] A tela anterior da jornada, quando não vem da tela E050T nem da tela do preparo,
avisa que o acesso deve ser feito pela tela E050T e marca a opção que abre a E049T. Como a
opção que leva a esta tela é outra, não é possível dizer, só pelo fonte, se o caminho de
menu desta jornada chega a abrir esta tela — ou se ela só se abre pelo encadeamento.
Pergunta ao site.

### RN-03 — A tela e a operação só abrem para quem tem acesso

Antes de qualquer coisa, a abertura confere a estação da sessão com a estação do meu
cadastro e procura a tela no cadastro de telas do meu código de acesso; não achando, o
acesso é recusado — com **\* Tela nao disponivel \*** ou
**\* Acesso negado para esta matricula \***. Depois, a operação pretendida é conferida
contra a liberação daquele código de acesso naquela tela: sem a liberação da alteração, a
recusa é **\* Acesso negado para esta operacao \***. Em qualquer dos casos nada é gravado.

### RN-04 — O órgão do pedido e o meu vínculo

O órgão é obrigatório: sem ele, a tela recusa com **\* Informe o orgao \*** e devolve o
cursor ao campo do órgão, sem gravar nada. E quem tem um órgão no vínculo da sessão não
pode trabalhar em outro: informando um órgão diferente, a recusa é
**\* Usuario sem acesso a outro orgao \***, também com o cursor de volta ao campo. Quem não
tem nenhum órgão no vínculo é posicionado no campo do órgão, para informá-lo.

### RN-05 — O grupo do pedido tem de ser o meu

O item calculado que a tela carrega tem de ser da minha coordenadoria. Se o que a passagem
encontrou para o órgão é de outro grupo, a recusa é
**<- Usuario sem acesso ao grupo deste orgao \***, com o cursor no campo do órgão, e nada é
processado.

[?] Ao carregar os itens calculados do órgão, a tela lê o cadastro com a coordenadoria
zerada e apaga os itens cuja coordenadoria não é a minha. Se essa leitura alcança mesmo os
itens de outro grupo, a tela apaga o pedido calculado alheio: pergunta ao site.

### RN-06 — A tela só aceita a alteração

A única operação aceita é a alteração. Qualquer outra é recusada com
**\* Opcao nao disponivel. Use ALT \***, sem que nada seja gravado.

[?] A operação já vem marcada como alteração pela própria abertura da tela, e a recusa é
conferida antes das demais. Se a máscara permite escolher outra operação, essa escolha é
recusada sem chegar a ser usada; se existe caso em que a tela deva abrir em outra operação,
é pergunta ao site.

### RN-07 — Sem gêneros calculados, não há o que distribuir

Quando não há nenhum item calculado para o órgão — nem para o pedido que a passagem
carrega — a tela avisa **\* Nao existem generos a distribuir \***, posiciona o cursor no
campo do órgão e encerra sem gravar.

### RN-08 — A quantidade distribuída não pode passar da calculada

Somando as cinco quantidades que eu informo em uma linha, o total não pode passar da
quantidade calculada daquele item. Passando, a recusa é
**\* Quantidade distribuida maior que calculada \***, com o cursor de volta à coluna da
quantidade, e nada é gravado.

### RN-09 — Item acumulado exige quantidade informada

Nos itens que acumulam, a linha não pode ficar sem quantidade: somando zero nas cinco
quantidades, a recusa é **\* Informe quantidade a ser distribuida \***, com o cursor de
volta à coluna da quantidade.

### RN-10 — Cada quantidade vai para um dia de entrega válido

Não se informa quantidade para um dia que não é dia de entrega daquele pedido: em cada uma
das cinco quantidades, quando eu informo um valor e o dia correspondente não tem data de
entrega, a recusa é **\* Inf. quantidade para dias de entrega validos \***, com o cursor de
volta à coluna daquele dia.

### RN-11 — A quantidade tem de respeitar a fração do gênero

Cada quantidade informada tem de ser múltipla da fração de entrega daquele gênero. Não
sendo, a recusa é **\* Quant. fracionada invalida para este genero \***, com o cursor de
volta à coluna daquele dia.

### RN-12 — O gênero precisa de permissão de entrega vigente no contrato

A distribuição só pode ser feita sobre uma permissão de entrega: o sistema procura, para o
órgão, o tipo de contrato, o fornecedor, a minha coordenadoria, a subclasse, o gênero e a
data limite do item, uma permissão não excluída cujo início seja igual ou anterior ao
início do item. Não achando, a recusa é **\* Genero sem permissao \***, com o cursor de
volta à coluna da situação, e nada é gravado.

### RN-13 — A quantidade não pode estourar o saldo inicial da permissão

Na permissão achada, o sistema parte do que já está distribuído naquela permissão, devolve o
que aquele item do pedido já tinha distribuído, soma o que eu estou distribuindo agora e
compara o resultado com o saldo inicial da permissão — as três parcelas que ela guarda,
somadas. Se o resultado passar do saldo inicial, a recusa é
**\* Quantidade insuficiente na permissao \***, com o cursor de volta à coluna da situação.

[?] A tela calcula 70% do saldo inicial da permissão em toda conferência e não usa esse
valor em nenhuma comparação: se a intenção era limitar a distribuição a 70% da permissão,
isso não acontece. Pergunta ao site.

### RN-14 — Item acumulado exige a quantidade recebida na nota

Nos itens que acumulam, a tela procura a quantidade recebida daquele item — órgão,
coordenadoria, item acumulado, subclasse, gênero e número da nota fiscal. Não achando, a
recusa é **\* Nao existe quantidade recebida \***, com o cursor de volta à coluna da
quantidade, e nada é gravado.

### RN-15 — A aprovação exige todos os itens com quantidade e prontos

Respondendo **S** à pergunta da aprovação, a tela só aprova se **todos** os itens
calculados do pedido tiverem quantidade distribuída e se os itens do pedido estiverem na
situação que a aprovação aceita. Achando qualquer item sem quantidade, ou um item na
situação que ela não aceita aprovar, a recusa é
**\* Generos sem quantidade distribuida \***, com o cursor de volta ao campo da resposta, e
nada é gravado.

[?] A situação do item do pedido é comparada com um código de uma letra que a tela não
explica; o que a letra significa — e por que ela barra a aprovação — é pergunta ao site.

### RN-16 — O que a aprovação gera

Passando nas conferências, a aprovação:

- cria a requisição do pedido, com a situação de requisição processada;
- marca o pedido como aprovado, com a data da aprovação;
- apaga o item calculado que virou requisição;
- nos itens que acumulam, baixa a quantidade distribuída da quantidade recebida, apaga o
  item do pedido quando ele zera e refaz a distribuição por gênero, fechando os itens que
  ficaram completos.

### RN-17 — Recusar a aprovação não grava nada

Respondendo qualquer coisa diferente de **S** à pergunta da aprovação, nada é gravado: a
tela apenas reexamina o pedido e termina. Como o pedido continua com quantidade
distribuída, a pergunta volta a ser feita na próxima passagem.

### RN-18 — O que fica gravado e a auditoria

Cada gravação deixa um registro na auditoria **A010T** com a tela, a operação, o cadastro
atingido, o órgão, a coordenadoria, o meu número de processo, a minha matrícula, a estação,
a secretaria, a data e a hora da sessão e os valores de antes e depois.

Além da auditoria, a tela grava: a quantidade de cada dia no item calculado — e só os dias
cuja quantidade eu mudei; a quantidade distribuída do item do pedido e a quantidade
distribuída da permissão de entrega — as duas só quando aquele item do pedido já existe; e,
na aprovação, a requisição. A criação do item do pedido acontece só no caminho do pedido
acumulado, quando a aprovação refaz as quantidades do pedido acumulado.

[?] Quando o item do pedido daquele gênero ainda não existe, a distribuição atualiza a
quantidade do item calculado, mas não grava a quantidade distribuída em item nenhum nem
toca a permissão. Ou o item deveria nascer também neste caminho, ou o caminho não deveria
existir — pergunta ao site.

### RN-19 — O que a tela entrega à tela seguinte

Quando o item calculado que chegou na passagem é de um órgão diferente do órgão do meu
vínculo, a tela não processa nada: ela devolve a passagem à tela E050T já com a operação de
inclusão. Fora desse caso, a tela termina em si mesma.

[?] A jornada registra esta tela como quem "passa para E050T", e a única passagem à E050T
no fonte é essa, que exige um pedido carregado para outro órgão que não o do vínculo. Se
existem outros caminhos de saída, é pergunta ao site. Há ainda o caminho inverso: a mesma
tela também é alcançada a partir da tela de preparo do pedido, fora desta jornada.

---

## Cenários BDD

```gherkin
Funcionalidade: Distribuir a quantidade calculada do pedido pelos dias de entrega e aprovar o pedido

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que o meu perfil tem acesso à tela E055T

  Cenário: A abertura mostra o pedido calculado do órgão
    Dado que existe item calculado para o órgão da minha passagem
    Quando a tela abre
    Então vejo o órgão, a coordenadoria, o número do pedido, o período e os dias de entrega
    E vejo até 12 linhas, com subclasse, gênero, quantidade calculada e os cinco dias
    E nada é gravado

  Cenário: Distribuição de um gênero pelos dias de entrega
    Dado que a linha tem uma quantidade calculada e há dias de entrega válidos
    Quando informo as quantidades de cada dia, dentro do calculado e da fração do gênero
    Então a tela grava a quantidade de cada dia no item calculado
    E grava a quantidade distribuída no item do pedido e na permissão de entrega
    E registra a operação na auditoria A010T

  Cenário: Aprovação do pedido
    Dado que todos os itens calculados do pedido têm quantidade distribuída
    E que os itens do pedido estão na situação que a aprovação aceita
    Quando respondo S à pergunta "Aprova Pedido <S/N>:"
    Então o sistema cria a requisição do pedido
    E marca o pedido como aprovado, com a data da aprovação
    E apaga o item calculado que virou requisição
    E registra a operação na auditoria A010T

  Cenário: Aprovação de pedido com item acumulado
    Dado que o item é acumulado e tem quantidade recebida na nota
    Quando respondo S à pergunta da aprovação
    Então a quantidade recebida é baixada pela quantidade distribuída
    E a distribuição por gênero é refeita
    E os itens que ficaram completos são fechados

  Cenário: Recusa da aprovação não grava nada
    Dado que o pedido tem quantidade distribuída
    Quando respondo algo diferente de S à pergunta "Aprova Pedido <S/N>:"
    Então nada é gravado
    E a pergunta volta a ser feita na próxima passagem

  Cenário: Aprovação recusada porque há gênero sem quantidade distribuída
    Dado que algum item calculado do pedido está sem quantidade
    Quando respondo S à pergunta da aprovação
    Então vejo a mensagem "* Generos sem quantidade distribuida *"
    E o cursor volta ao campo da resposta
    E nada é gravado

  Cenário: Acesso à tela sem autorização
    Dado que o meu código de acesso não tem a tela E055T no seu cadastro
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

  Cenário: Órgão de outro vínculo é recusado
    Dado que eu tenho um órgão no vínculo da sessão
    Quando informo um órgão diferente
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E o cursor volta ao campo do órgão

  Cenário: Pedido de outro grupo é recusado
    Dado que o item calculado carregado é de outra coordenadoria
    Quando a tela carrega o pedido
    Então vejo a mensagem "<- Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é processado

  Cenário: Não há gêneros calculados para distribuir
    Dado que não existe item calculado para o órgão
    Quando a tela abre
    Então vejo a mensagem "* Nao existem generos a distribuir *"
    E o cursor fica no campo do órgão
    E nada é gravado

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

  Cenário: Gênero sem permissão de entrega é recusado
    Dado que não há permissão de entrega vigente para o gênero no contrato
    Quando confirmo a linha
    Então vejo a mensagem "* Genero sem permissao *"
    E o cursor volta à coluna da situação
    E nada é gravado

  Cenário: Quantidade acima do saldo inicial da permissão é recusada
    Dado que o que eu distribuo passa do saldo inicial da permissão, descontado o que o item já tinha
    Quando confirmo a linha
    Então vejo a mensagem "* Quantidade insuficiente na permissao *"
    E nada é gravado

  Cenário: Item acumulado sem quantidade recebida na nota é recusado
    Dado que a linha é de um item acumulado
    E não existe quantidade recebida para ele na nota procurada
    Quando confirmo a linha
    Então vejo a mensagem "* Nao existe quantidade recebida *"
    E nada é gravado

  Cenário: A recusa não grava nada
    Dado que a passagem foi recusada por alguma conferência
    Quando a tela termina a passagem
    Então nenhuma quantidade de dia foi gravada
    E nenhum item do pedido nem permissão foi tocado
    E nenhum registro de auditoria foi gerado

  Cenário: Passagem devolvida por causa do vínculo
    Dado que o item calculado carregado é de um órgão diferente do meu vínculo
    Quando a tela recebe a passagem
    Então ela não processa nada
    E devolve a passagem à tela E050T com a operação de inclusão

  Cenário: Cada gravação deixa auditoria
    Dado que a passagem passou por todas as conferências
    Quando a tela grava a distribuição, ou aprova o pedido
    Então fica um registro de auditoria com a tela, a operação, o cadastro atingido, a coordenadoria,
      o meu número de processo, a minha matrícula, a estação, a secretaria, a data e a hora da sessão
      e os valores de antes e depois
```
