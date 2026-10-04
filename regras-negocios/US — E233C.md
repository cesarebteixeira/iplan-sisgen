# US — E233C — Consultar os pedidos pendentes de fechamento de um pedido acumulado

## Estória

Como **servidor de CRE**, quero **consultar quais pedidos ainda estão pendentes de
fechamento dentro de um pedido acumulado, com o órgão de cada um, a nota fiscal, a
data de início e a quantidade pedida**, para que **eu saiba o que compõe o acumulado
e quanto ainda falta antes de fechá-lo**.

Um pedido acumulado reúne, sob um único número, vários pedidos do mesmo gênero, com o
seu próprio período de início e limite — e é esse conjunto que se fecha. Sem esta
consulta, quem fecha o acumulado não vê, antes de fechar, quais
pedidos continuam pendentes, de que órgão é cada um, qual nota fiscal os acompanha e
qual é o total pedido; o fechamento vira conferência às cegas, e um pedido esquecido
dentro do acumulado só aparece depois de fechado. A tela não altera o que mostra: ela
só apresenta o que o cadastro do acumulado já registra.

## Contexto

Jornada S000M → E000M → E200M → E230M → E233C.

Ator: servidor de CRE — informa o órgão filho, o número do pedido com o ano da
entrega, a subclasse e o gênero do acumulado, e lê a lista dos pedidos pendentes de
fechamento e o total do acumulado; não inclui, não altera e não exclui nada.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os três passos do meio — E000M, E200M e E230M — são menus: não gravam nada e não
deixam dado nenhum para esta tela; a opção que a abre apenas aponta o destino. Por
isso a tela abre sem acumulado em contexto (o que também decide a sua operação
inicial). O que ela usa da sessão — o tipo de órgão, a coordenadoria regional de
ensino e o órgão filho do servidor — vem do vínculo da matrícula, e as regras disso
estão no documento da entrada.

Esta é a última tela da jornada: ela não encadeia em nenhuma outra.

---

## Regras de negócio

### RN-01 — A tela é de consulta: a operação vem de quem a abre e qualquer outra é recusada

Na abertura, se nenhuma operação veio no contexto, a tela se coloca sozinha em
consulta e passa a mostrar essa operação; a operação que ela exibe é a que quem a
abriu deixou. Chegando à conferência da operação — depois das conferências comuns de
rota e de liberação da operação, e antes de qualquer leitura do pedido —, o que não
for a consulta é recusado com **\* Opcao nao disponivel. Use CON \*** e o cursor
volta ao campo da operação. Nesse caminho nada do pedido é lido nem mostrado.

[?] O valor que vale como consulta não é escrito pelo programa: ele é lido, no
ambiente, de uma tabela de mensagens que não veio no lote, e é o texto da própria
recusa (*Use CON*) que o nomeia. Como a abertura repõe a consulta, a recusa só é
alcançável numa mensagem seguinte do operador — e nada garante que a máscara da tela
ofereça esse campo. Pergunta ao site.

[?] A operação que encerra a sessão não chega a essa conferência: quem a trata é a
rotina comum de rota, antes dela. Das operações que chegam, só a consulta passa; se o
site espera que alguma outra funcione nesta tela, o caminho não deixa. Pergunta ao
site.

### RN-02 — Os campos numéricos são editados antes das conferências de cadastro

Antes de conferir cadastro nenhum, a tela edita como número os **vinte e um** campos
que o operador pode informar — do órgão filho às quantidades da lista. O campo
deixado em branco vira zero, e o separador de milhar do que for informado é retirado.
Quando a edição acusa erro, a transação para antes de qualquer conferência de cadastro
e a tela devolve o cursor ao campo culpado: para sete deles o destino do cursor está
escrito na própria tela — o órgão filho, o número do pedido, o ano da entrega, a
subclasse, o gênero e o par formado pelo pedido auxiliar e o seu ano. É essa edição
que explica por que a tela não aceita texto onde se espera código, data ou quantidade.

[?] A mensagem da recusa da edição vem da rotina comum de edição numérica do
ambiente, não desta tela, e o texto dela não está no lote. Para os demais campos, quem
calcula a posição do cursor é essa rotina. Pergunta ao site.

### RN-03 — O acumulado é identificado por cinco dados, e o número do pedido com o ano da entrega formam o seu código

O acumulado é procurado pelo **órgão filho** informado, pelo **número do pedido** com
o **ano da entrega**, pela **subclasse** e pelo **gênero**. O número do pedido e o ano
da entrega formam juntos o código de dez dígitos do acumulado: os seis primeiros são o
número do pedido e os quatro últimos, o ano da entrega. A tela cobra o órgão —
**\* Informe o orgao \*** — e o código do pedido — **\* Informe o numero do pedido
\*** —, e em cada recusa o cursor volta ao campo que falta. O órgão não vem preenchido
do vínculo do servidor: quem o informa é o operador.

[?] A obrigatoriedade do gênero é cobrada no campo da subclasse: a recusa diz
**\* Informe o genero \***, mas o cursor vai para o campo da subclasse, e o gênero não
passa por nenhuma conferência de obrigatoriedade — vai direto para a conferência de
cadastro. Se a intenção era exigir o gênero, o caminho não exige. Pergunta ao site.

### RN-04 — O órgão informado tem de existir, ser da secretaria do servidor e da sua coordenadoria

O órgão informado é procurado no cadastro de órgãos, e o registro marcado como
excluído é saltado. Não achado, a recusa é **\* Orgao nao cadastrado \***; se o órgão
é de um tipo de órgão diferente do que está na sessão do servidor, a recusa é
**\* Orgao nao pertence a esta secretaria \***; e se é de uma coordenadoria regional
de ensino diferente da do servidor, a recusa é **\* Usuario sem acesso ao grupo deste
orgao \***. Em todas elas o cursor volta ao campo do órgão e nada do pedido é lido.

[?] Quando o vínculo do servidor não tem coordenadoria, a conferência de grupo não se
aplica e o servidor passa com um órgão de qualquer coordenadoria. Se isso é
intencional ou é buraco de autorização, é pergunta ao site.

### RN-05 — O pedido tem de pertencer ao órgão filho do próprio servidor

O pedido só é aceito se pertencer ao **órgão filho do vínculo do servidor**; sendo de
outro órgão, a recusa é **\* Pedido de outro orgao \*** e o cursor volta ao campo do
órgão. Quem define o órgão do pedido é o cadastro do pedido, não o que o operador
digitou.

[?] Sem órgão filho no vínculo, a conferência é saltada e qualquer pedido passa —
mesma dúvida de autorização da regra anterior. Pergunta ao site.

### RN-06 — O pedido é procurado pela secretaria do servidor, pela coordenadoria do órgão e pelo código do acumulado

Não existindo pedido para o tipo de órgão da sessão, para a coordenadoria do órgão
encontrado e para o código do acumulado informado, a tela recusa com **\* Pedido nao
cadastrado \*** e devolve o cursor ao campo do número do pedido.

[?] A coordenadoria regional escolar que o operador informa não participa de leitura
nenhuma: o órgão é procurado só pelo código, e o pedido, pela coordenadoria que o
próprio cadastro do órgão traz. Informar outra coordenadoria não muda o que a consulta
acha — o campo só é comparado com o da consulta anterior, para decidir se a lista
continua de onde parou. Se a intenção era usar a coordenadoria informada como
critério, o caminho não usa. Pergunta ao site.

### RN-07 — Só se consulta o acumulado que o próprio sistema calculou

O pedido encontrado passa por três recusas em sequência sobre a marca de acumulação,
cada uma com o cursor de volta ao campo do número do pedido: **\* Pedido nao acumulado
\***, quando não é um pedido acumulado; **\* Pedido acumulado digitado \***, quando o
acumulado foi lançado à mão; e **\* Pedido auxiliar do acumulado calculado \***,
quando o que veio é o pedido auxiliar que o sistema calculou para o acumulado. A tela
serve, portanto, ao acumulado que o próprio sistema calculou.

[?] A tela recusa esses três casos e não nomeia o valor aceito: passa qualquer outra
marca. Fora desta jornada, é o fechamento do acumulado que grava ali a marca do
acumulado calculado, e é a tela do pedido auxiliar que grava a outra. Se a base tiver
outras marcas, elas passam. Pergunta ao site.

### RN-08 — A subclasse e o gênero têm de estar cadastrados e constar do pedido

A subclasse e o gênero informados são procurados no cadastro de gêneros. Não achados,
a recusa é **\* Genero nao cadastrado \*** e o cursor volta ao campo da subclasse.
Depois, o gênero tem de constar do pedido: não constando, a recusa é **\* Genero nao
cadastrado neste pedido \*** e o cursor volta ao campo do número do pedido. Achados, a
tela mostra a **descrição resumida do gênero**, de quinze posições, vinda do cadastro
de gêneros.

[?] A descrição é procurada pela vigência do pedido — ano, mês e dia de início —, mas
a conferência do que voltou compara apenas a subclasse e o gênero, não a vigência: se
o pedido for de outra vigência do mesmo gênero, a descrição mostrada pode ser a de
outra. Pergunta ao site.

### RN-09 — O fornecedor e o operador mostrados são os do pedido

O código do fornecedor e a sua razão social, e o código do operador com o seu nome, são
os do **pedido encontrado**, buscados nos cadastros de fornecedores e de operadores. O
que o operador porventura digitar nesses campos não escolhe a consulta nem substitui o
mostrado. Sem código de operador no pedido, a busca não é feita e o nome fica em
branco.

[?] Se o fornecedor ou o operador do pedido não estiver no cadastro, a tela não avisa:
o nome sai em branco e a consulta segue normalmente. Se o esperado é um aviso, é
pergunta ao site.

### RN-10 — A situação do pedido é mostrada como Aprovado ou Fechado

A tela mostra a situação do pedido em texto: **Fechado** quando o pedido está fechado,
e **Aprovado** em qualquer outra situação.

[?] A descrição é decidida pela tela, não vem do cadastro, e só tem esses dois textos:
pedidos em outras situações — excluído, pendente de distribuição, por exemplo, que
outras telas do sistema distinguem — aparecem aqui como Aprovado. Se a intenção era
distinguir mais situações, o caminho não distingue. Pergunta ao site.

### RN-11 — A lista traz até 11 pedidos do acumulado, com oito dados cada

A lista dos pedidos pendentes de fechamento tem **11 linhas**, e cada linha traz
**oito dados** de um pedido: o número do pedido, o ano da entrega, o código e o nome
do órgão, o número da nota fiscal, o dia e o mês de início, um código de uma posição e
a quantidade pedida. Cada linha vem de um registro do acumulado — no mesmo órgão, na
mesma subclasse e no mesmo gênero —, e o nome do órgão é buscado no cadastro de órgãos
pelo órgão daquele registro, saltando o registro marcado como excluído.

[?] As definições de máscara da tela não vieram no lote: não se sabe quais desses
campos o operador pode digitar, nem o que exatamente ele vê em cada coluna. Pergunta
ao site.

[?] A lista começa pelo pedido auxiliar que a consulta anterior deixou em contexto, e
o recurso de posicionamento da leitura — o que diz à base se deve posicionar por um
pedido ou seguir para o próximo registro — não está explicado no acervo nem no manual.
Se ele posicionar sempre no mesmo pedido, a lista repete a mesma linha; se seguir, a
lista percorre os pendentes. Os dois comportamentos são compatíveis com o que o fonte
mostra. Pergunta ao site.

### RN-12 — O total é o de todos os pedidos do acumulado

Fora da lista, a tela mostra o **total do acumulado**: a soma das quantidades pedidas
de **todos** os registros do acumulado naquele órgão, naquela subclasse e naquele
gênero — e não apenas das linhas mostradas.

[?] Sendo a lista fixa em 11 linhas e o total a soma de todos os registros, um
acumulado com mais de onze pedidos mostra um total maior do que a soma do que está em
tela, e o fonte não diz como o operador vê o restante. Se a intenção era a lista cobrir
o acumulado inteiro, o caminho não cobre. Pergunta ao site.

### RN-13 — Não havendo pedido pendente, a tela avisa e não mostra linha

Não existindo pedido pendente de fechamento para o acumulado, a tela avisa
**\* Nao existem pedidos pendentes de fechamento \*** e nenhuma linha é preenchida. O
aviso sai quando a primeira linha da lista não acha registro, e é só ali: uma vez
começada a lista, o fim dela não gera aviso.

### RN-14 — As quantidades e as datas saem formatadas

As quantidades — a pedida de cada linha e o total do acumulado — aparecem com três
casas decimais e vírgula. A data de início de cada linha aparece só como dia e mês; o
período do acumulado aparece em dia, mês e ano, em campos separados.

[?] A quantidade igual a zero passa por uma rotina comum de formatação que não tem
fonte no lote: não se sabe se o zero sai em branco ou como zero. Pergunta ao site.

### RN-15 — A consulta não grava nada

A tela e as rotinas comuns que ela chama só leem cadastros: telas, registros do
acumulado, órgãos, pedidos, fornecedores, itens do pedido, operadores e gêneros.
Nenhum registro é incluído, alterado ou excluído, e nenhum registro de auditoria é
gerado. As operações de gravação, de exclusão e de travamento existem declaradas para
os oito cadastros que a tela enxerga, mas **não são executadas em nenhum caminho**:
declarar não é executar.

[?] A única gravação a que a passagem pode dar origem é a da rotina comum de rota,
quando a operação encerra a sessão — e essa gravação é da sessão, não desta tela, e não
tem fonte no lote quanto ao que ela registra. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar os pedidos pendentes de fechamento de um pedido acumulado

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E233C

  Cenário: Consulta dos pedidos pendentes de fechamento
    Dado que existe um pedido acumulado calculado pelo sistema no meu órgão filho
    E que esse acumulado tem pedidos pendentes de fechamento
    Quando informo o órgão filho, o número do pedido com o ano da entrega, a subclasse e o gênero
    Então vejo a lista dos pedidos pendentes de fechamento
    E vejo o total do acumulado

  Cenário: O número do pedido e o ano da entrega formam o código do acumulado
    Dado que o acumulado é identificado por um código de dez dígitos
    Quando informo o número do pedido e o ano da entrega
    Então os seis primeiros dígitos do código são o número do pedido
    E os quatro últimos são o ano da entrega

  Cenário: A lista mostra no máximo 11 pedidos
    Dado que o acumulado tem pedidos pendentes de fechamento
    Quando envio a consulta
    Então a lista mostra uma linha por pedido, até 11 linhas
    E cada linha traz oito dados daquele pedido

  Cenário: Cada linha identifica o pedido componente
    Dado que um dos pedidos pendentes tem órgão, nota fiscal e data de início
    Quando vejo a linha desse pedido
    Então vejo o número do pedido e o ano da entrega
    E vejo o código e o nome do órgão
    E vejo o número da nota fiscal, o dia e o mês de início, o código de uma posição e a quantidade pedida

  Cenário: O total é o de todos os pedidos do acumulado
    Dado que o acumulado tem pedidos pendentes de fechamento
    Quando a lista é mostrada
    Então o total é a soma das quantidades pedidas de todos os registros do acumulado
    E o total não se limita às linhas mostradas

  Cenário: A descrição do gênero vem do cadastro de gêneros
    Dado que a subclasse e o gênero informados estão cadastrados
    Quando a consulta encontra o pedido
    Então vejo ao lado do código do gênero a descrição resumida do cadastro

  Cenário: O fornecedor e o operador mostrados são os do pedido
    Dado que existe um pedido para a combinação que vou informar
    E que o pedido tem fornecedor e operador cadastrados
    Quando informo um código de fornecedor diferente do dele
    Então o código e a razão social mostrados são os do pedido encontrado
    E ao lado do código do operador vejo o nome cadastrado

  Cenário: A situação do pedido aparece em texto
    Dado que o pedido consultado está fechado
    Quando vejo o pedido
    Então a situação aparece como "Fechado"
    E um pedido em qualquer outra situação aparece como "Aprovado"

  Cenário: As quantidades e as datas saem formatadas
    Dado que uma linha tem quantidade pedida com casas decimais
    Quando vejo a linha
    Então a quantidade aparece com três casas decimais e vírgula
    E a data de início da linha aparece como dia e mês
    E o período do acumulado aparece em dia, mês e ano

  Cenário: Não existem pedidos pendentes de fechamento
    Dado que o acumulado não tem pedido pendente de fechamento
    Quando envio a consulta
    Então vejo a mensagem "* Nao existem pedidos pendentes de fechamento *"
    E nenhuma linha é preenchida

  Cenário: Operação diferente de consulta
    Dado que estou na tela E233C
    Quando chego à conferência da operação com uma operação diferente da consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nenhum pedido é lido nesse caminho

  Cenário: Órgão não informado
    Quando deixo o órgão filho em branco
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor volta ao campo do órgão filho

  Cenário: Número do pedido não informado
    Quando deixo o número do pedido e o ano da entrega em branco
    Então vejo a mensagem "* Informe o numero do pedido *"
    E o cursor volta ao campo do número do pedido

  Cenário: Gênero não informado
    Quando deixo a subclasse em branco
    Então vejo a mensagem "* Informe o genero *"
    E o cursor volta ao campo da subclasse

  Cenário: Órgão não cadastrado
    Quando informo um órgão filho que não existe no cadastro de órgãos
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão filho
    E nenhum pedido é lido

  Cenário: Órgão de outra secretaria
    Quando informo um órgão de tipo de órgão diferente do da minha sessão
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E o cursor volta ao campo do órgão filho

  Cenário: Órgão de outra coordenadoria
    Dado que a minha sessão tem uma coordenadoria
    Quando informo um órgão de outra coordenadoria regional de ensino
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor volta ao campo do órgão filho

  Cenário: Pedido não cadastrado
    Dado que o órgão informado é da minha coordenadoria
    Quando informo um número de pedido que não existe
    Então vejo a mensagem "* Pedido nao cadastrado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido que não é acumulado
    Quando informo um pedido que não é pedido acumulado
    Então vejo a mensagem "* Pedido nao acumulado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido acumulado digitado à mão
    Quando informo um acumulado lançado à mão
    Então vejo a mensagem "* Pedido acumulado digitado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido auxiliar do acumulado
    Quando informo o pedido auxiliar que o sistema calculou para o acumulado
    Então vejo a mensagem "* Pedido auxiliar do acumulado calculado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido de outro órgão
    Dado que a minha sessão tem um órgão filho
    Quando informo um pedido que pertence a outro órgão filho
    Então vejo a mensagem "* Pedido de outro orgao *"
    E o cursor volta ao campo do órgão filho

  Cenário: Gênero não cadastrado
    Quando informo uma subclasse e um gênero que não estão no cadastro de gêneros
    Então vejo a mensagem "* Genero nao cadastrado *"
    E o cursor volta ao campo da subclasse

  Cenário: Gênero que não está no pedido
    Dado que a subclasse e o gênero estão cadastrados
    Quando informo um gênero que não consta daquele pedido
    Então vejo a mensagem "* Genero nao cadastrado neste pedido *"
    E o cursor volta ao campo do número do pedido

  Cenário: Campo numérico inválido
    Quando informo texto onde se espera um código, uma data ou uma quantidade
    Então a tela recusa antes de conferir cadastro nenhum
    E o cursor volta ao campo culpado

  Cenário: A consulta não grava nada
    Dado que abro a tela E233C e consulto um pedido acumulado
    Quando a lista e o total são mostrados
    Então nenhum pedido, item, órgão, fornecedor, operador ou gênero é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: A transação passa pela conferência de sessão, de rota e de operação
    Dado que a minha sessão ou a minha tela não está liberada, ou que não tenho a operação
    Quando confirmo a consulta
    Então a tela não lê, não mostra e não grava, e a transação é encerrada pela conferência
```
