# US — E235T — Inclusão de pedido a partir do saldo da nota fiscal

## Estória

Como **servidor de CRE**, quero **abrir o pedido de entrega de uma unidade aproveitando o
que uma nota fiscal já recebeu de um pedido acumulado, informando o fornecedor, a nota, o
gênero, o órgão que vai receber, o início da entrega e a quantidade**, para que **o que
chegou pela nota deixe de valer só no acumulado e passe a valer como pedido da unidade que
vai receber, no período combinado**.

O pedido acumulado junta num só número o que várias unidades pediram ao mesmo fornecedor,
e a nota fiscal que o fornecedor emite é lançada contra ele, gênero a gênero. Quando a
mercadoria é destinada a uma unidade determinada, a parte que a nota já recebeu precisa
sair do acumulado e virar pedido próprio dessa unidade — com o gênero, a quantidade e o
dia em que a entrega começa —, porque é o pedido individual, e não o acumulado, que a
unidade e a secretaria acompanham depois. Sem esta tela, o que chegou continua valendo só
no acumulado e a unidade que recebeu fica sem pedido que a identifique: nada falha, mas o
que ela recebeu não aparece em nome dela.

## Contexto

Jornada S000M → E000M → E200M → E230M → E235T.

Ator: servidor de CRE — informa o fornecedor, o número e o ano da nota fiscal, a subclasse
e o gênero, o órgão filho que vai receber, o dia, o mês e o ano de início da entrega e a
quantidade a ser pedida, vê o que a tela apurou sobre a nota e o órgão, e confirma a
inclusão do pedido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Os três passos do meio — `E000M`, `E200M` e `E230M` — são menus: não gravam nada, não
passam registro nem operação a esta tela e apenas apontam para onde ir. Por isso esta tela
não herda modo de ninguém: ela abre por decisão própria, já em inclusão, e nada do que o
operador informou nos passos anteriores é aproveitado — tudo o que ela mostra vem dos
cadastros. Da sessão ela usa a matrícula, o código de acesso, o tipo de órgão, a
coordenadoria regional escolar, a estação e a data e a hora do sistema, e as regras disso
estão no documento da entrada.

Esta é a última tela da jornada: ela não abre outra. Pedida a confirmação, ou confirmada a
inclusão, ela reabre a si mesma, pronta para o próximo pedido.

---

## Regras de negócio

### RN-01 — A tela só inclui, e a abertura já propõe a inclusão

A tela trabalha com uma única operação: **incluir pedido**. Ao ser aberta, ela mesma põe
essa operação no campo, mostra no campo da coordenadoria regional escolar a coordenadoria
do vínculo do servidor e marca o cartão do pedido; no cabeçalho ela mostra a descrição do
tipo de órgão da sessão e a data do sistema, e o cursor começa no **órgão filho**, que é o
primeiro dado a informar. Se a mensagem chegar com qualquer operação que não seja a de
inclusão, o sistema recusa com **\* Opcao invalida. Use INC \***, devolve o cursor ao campo
da operação e encerra a passagem: nada da nota, do fornecedor, do gênero ou do órgão é
lido, e nada é gravado. A recusa vem depois das conferências comuns de sessão, de tela e
de liberação, e antes de qualquer leitura de cadastro.

O órgão filho de destino **não** vem proposto: quem escolhe a unidade que vai receber é o
servidor, a cada inclusão. Sem coordenadoria no vínculo, o campo da coordenadoria fica com
o que já estava.

[?] A recusa manda usar INC, mas o código da inclusão com que a tela compara o campo tem,
na declaração do ambiente, o texto **ADD** — e é de uma tabela de mensagens que o ambiente
carrega, e que não veio no lote, que esse código é lido em tempo de execução. Os dois nomes
não coincidem: ou o servidor digita o que a mensagem manda e é recusado, ou o código do
ambiente não é o texto que a declaração sugere e a mensagem é que está errada. Pergunta ao
site.

### RN-02 — A tela lê de dezesseis cadastros, grava em seis e apaga de três

A tela enxerga **dezesseis** cadastros: o registro das telas, o cadastro dos fornecedores,
o cadastro dos gêneros, o cadastro das notas fiscais, o cadastro dos itens da nota, o
cadastro dos pedidos, o cadastro dos gêneros do pedido, um segundo par de cadastro de nota
fiscal e de itens da nota, o cadastro dos órgãos, o cadastro dos operadores, o cadastro das
quantidades recebidas da nota, o cadastro dos feriados, a numeração dos pedidos, a
auditoria e o vínculo entre a nota, o gênero e o pedido.

Ela **grava em seis**: a numeração dos pedidos, o cadastro dos pedidos, o cadastro dos
gêneros do pedido, o vínculo entre a nota, o gênero e o pedido, o cadastro das quantidades
recebidas da nota e a auditoria. E **apaga de três**: o gênero do pedido de origem, o
pedido de origem e o vínculo da nota com ele. Todos os demais são só de leitura.

[?] Do acervo não se conclui o que distingue os dois pares de cadastro de nota fiscal e de
itens da nota: o segundo par só é procurado quando o primeiro não existe, e a tela trata os
dois do mesmo modo, aceitando de ambos o mesmo gênero. Se um é a nota do fornecedor e o
outro a nota de entrada, ou se são duas origens diferentes, é pergunta ao site.

### RN-03 — Os campos numéricos passam por edição antes das conferências

Antes de qualquer conferência de cadastro, os **vinte e um** campos numéricos da tela
passam por edição numérica e o campo deixado em branco é tratado como zero: o órgão filho,
o dia, o mês e o ano do início, o dia, o mês e o ano do limite, a subclasse, o gênero, a
quantidade a ser pedida, o número da nota, o dia, o mês e o ano de emissão da nota, a
coordenadoria, o número e o ano do pedido acumulado, o tipo de contrato, o fornecedor, o
operador e o órgão da nota. A quantidade aceita **vírgula** como separador decimal, e o
separador de milhar do que for informado é retirado. O cartão, a operação e a resposta da
confirmação não passam por essa edição.

Para **dez** desses campos a tela escreve o destino do cursor quando a edição acusa erro: o
órgão filho, o dia, o mês e o ano do início, a subclasse, o gênero, a quantidade a ser
pedida, o número da nota, o ano da nota e o fornecedor.

[?] A mensagem da edição numérica vem da rotina comum do ambiente, não desta tela, e o
texto dela não está no lote. Para os campos sem destino escrito — o dia, o mês e o ano
limite, a coordenadoria, o número e o ano do pedido acumulado, o tipo de contrato, o
operador e o órgão da nota — quem calcula a posição do cursor é essa rotina, e do acervo
não se conclui onde o cursor fica. Pergunta ao site.

### RN-04 — A nota fiscal é identificada pelo fornecedor, pelo número e pelo ano, e a data da nota vem do dia e do mês de emissão

A nota fiscal é identificada pelo **tipo de órgão da sessão**, pelo **código do
fornecedor**, pelo **número de nove dígitos** e pelo **ano**. O número é obrigatório — sem
ele a recusa é **\* Informe o numero da nota fiscal \***, com o cursor no número — e o ano
também, senão **\* Informe o ano de entrega da nota fiscal \***, com o cursor no ano. O dia
e o mês de emissão não são exigidos: junto com o ano eles formam a **data da nota**, e é
essa data que a tela compara com o início da entrega (RN-12).

[?] O mesmo campo aparece como **ano de emissão** no seu rótulo e como **ano de entrega**
na mensagem de recusa. Se são a mesma coisa no site, um dos dois nomes está errado; se não
são, a nota está sendo procurada pelo ano errado. Pergunta ao site.

[?] O dia e o mês de emissão não são exigidos nem entram na identificação da nota — a
procura usa só o tipo de órgão, o fornecedor, o número e o ano —, mas são a única data da
nota que a tela conhece: em branco, a data da nota fica reduzida ao primeiro dia do ano
informado, e é contra essa data que o início da entrega é comparado. Pergunta ao site.

### RN-05 — O fornecedor tem de estar cadastrado

O fornecedor informado tem de estar no cadastro de fornecedores; o registro marcado como
excluído é saltado. Não achando, a recusa é **\* Fornecedor nao cadastrado \***, com o
cursor no código do fornecedor, e nada é gravado. Não há recusa própria para o código em
branco: em branco, o fornecedor simplesmente não é encontrado e a mensagem é a mesma.

### RN-06 — A subclasse e o gênero têm de estar cadastrados no ano da nota

O código da subclasse é obrigatório: em branco, a recusa é **\* Informe o genero \***, com
o cursor na **subclasse**. O par subclasse e gênero tem de estar no cadastro de gêneros, no
ano da nota — e o gênero marcado como excluído não é achado. Não achando, a recusa é
**\* Genero nao cadastrado \***, com o cursor na subclasse. Do cadastro do gênero a tela
traz a descrição resumida, a classe e a quantidade de fracionamento, que usa para conferir
a quantidade pedida (RN-13).

[?] A obrigatoriedade é cobrada no campo da subclasse e o cursor volta para lá, embora a
mensagem fale do gênero; o gênero em si não passa por conferência de obrigatoriedade e vai
direto para a conferência de cadastro. Se a intenção era exigir os dois, o caminho não
exige. Pergunta ao site.

[?] O gênero é procurado pela vigência do ano informado no campo da nota, e o cadastro de
gêneros tem vigência por ano; o acervo não diz o que a tela deveria fazer quando o gênero
vigora num ano e a nota é de outro. Pergunta ao site.

### RN-07 — A nota tem de existir, ter o gênero e estar amarrada a um pedido acumulado

A nota fiscal do fornecedor, no ano informado, tem de estar cadastrada: não achando, a
recusa é **\* Nota fiscal nao cadastrada \***, com o cursor no número da nota. Entre os
itens da nota tem de estar a subclasse e o gênero informados; não estando, a recusa é
**\* Genero nao cadastrado nesta nota \***, com o cursor na subclasse. E o pedido a que a
nota está amarrada tem de ser um **pedido acumulado**; não sendo, a recusa é
**\* Nota nao e de pedido acumulado \***, com o cursor no número da nota. Em todas elas
nada é gravado.

A tela procura a nota em **dois cadastros**: primeiro naquele em que a nota vem amarrada a
um processo, e só quando não acha ali é que procura no outro, o das notas sem processo.
Achando, ela guarda o número do processo, o operador, a coordenadoria, o tipo de contrato,
o órgão da nota e o pedido acumulado que acompanha a nota — e é esse pedido acumulado que a
tela consulta depois para achar o saldo (RN-11). No cabeçalho, o pedido acumulado aparece
rotulado como **Processo** quando a nota tem processo e como **Lote** quando não tem.

[?] A tela não confere se o pedido amarrado à nota foi encontrado antes de perguntar se ele
é acumulado: quando ele não existe, o que a conferência lê é o resto da última leitura, e
não se conclui do acervo qual dos dois desfechos o operador vê. Pergunta ao site.

### RN-08 — A nota e o órgão de destino têm de ser da coordenadoria e da secretaria do servidor

Quando o vínculo do servidor tem coordenadoria regional escolar, a nota fiscal tem de ser
dessa mesma coordenadoria: sendo de outra, a recusa é **\* Usuario sem acesso a outro grupo
\***, com o cursor no número da nota. O órgão filho de destino também tem de ser da
coordenadoria do vínculo, senão **\* Usuario sem acesso ao grupo deste orgao \***, com o
cursor no órgão; e ele tem de pertencer ao **tipo de órgão da sessão**, senão **\* Orgao
nao pertence a esta secretaria \***. Nas três, nada é gravado.

[?] Sem coordenadoria no vínculo, nenhuma das duas conferências de grupo se aplica e o
servidor abre pedido a partir de nota e de órgão de qualquer coordenadoria. Se isso é
intencional ou é buraco de autorização, é pergunta ao site.

### RN-09 — O órgão filho de destino tem de existir, estar ativo e não ser órgão de pedido acumulado

O órgão filho que vai receber é obrigatório: em branco, a recusa é **\* Informe o orgao
\***, com o cursor no órgão. Ele tem de estar cadastrado — o registro marcado como excluído
é saltado, e o que sobra é **\* Orgao nao cadastrado \***, com o cursor no órgão —, não
pode estar marcado como **inativo** (**\* Orgao cadastrado como inativo \***) nem como
órgão de **pedido acumulado** (**\* Orgao cadastrado para pedido acumulado \***). Em todas,
o cursor volta ao órgão e nada é gravado.

### RN-10 — O cadastro do órgão de destino tem de estar completo

Achado o órgão, **seis** dados do seu cadastro têm de estar preenchidos: o bairro, o órgão
pai, o nome, o endereço, o número de matrículas e o número de pessoas. Faltando qualquer um
deles, a recusa é **\* Orgao cadastrado com dados incompletos \***, com o cursor no órgão,
e nada é gravado.

### RN-11 — O saldo da nota limita a quantidade pedida

A quantidade pedida não pode passar do que a nota ainda tem para distribuir naquele gênero.
A tela procura o saldo da nota pelo pedido acumulado, pela coordenadoria, pela subclasse,
pelo gênero e pelo número da nota, e o saldo é a diferença entre as duas quantidades que
esse registro guarda — a **quantidade recebida** e a **quantidade recebida acumulada**.
Quando as duas são iguais, não há saldo e a recusa é **\* Nao existe saldo disponivel para
esta nota \***; quando a quantidade pedida passa da diferença, a recusa é **\* Saldo da
nota insuficiente para o pedido \***. Nas duas, o cursor fica na quantidade e nada é
gravado.

[?] A conferência lê o saldo como a quantidade recebida menos a recebida acumulada, mas a
gravação soma a quantidade pedida à quantidade recebida — a mesma que a conferência leu
como o total — e não toca na recebida acumulada. Lido assim, o saldo cresce a cada inclusão
em vez de ser consumido, e a mesma nota poderia render pedidos sucessivos. Além disso, a
conferência do saldo escolhe o registro por chaves diferentes das da gravação, de modo que
podem não ser o mesmo registro. Pergunta ao site; não escolho um dos dois lados.

[?] Na passagem que grava, a tela refaz a conferência do saldo antes de escrever qualquer
coisa e, quando essa segunda conferência recusa, o caminho cai direto na mensagem de pedido
cadastrado: a tela anuncia o pedido como cadastrado sem ter gravado nada. Se isso só é
alcançável quando outra sessão mexe na nota entre a pergunta e a resposta, é pergunta ao
site.

### RN-12 — O início da entrega tem de ser dia útil e não anterior à data da nota

O dia, o mês e o ano do início formam a data de início da entrega, e ela tem de cair num
**dia útil**: **sábado** é recusado com **\* Inicio da entrega nao deve ser um sabado \***,
**domingo** com **\* Inicio da entrega nao deve ser um domingo \***, e **feriado** do tipo
de órgão da sessão com **\* Inicio da entrega nao deve ser um feriado \***. A data também
não pode ser anterior à **data da nota fiscal**, senão **\* Inicio da entrega < data da
nota \***. Em todas as recusas o cursor fica no dia do início e nada é gravado.

[?] A tela não exige a data de início nem confere o resultado da conversão que faz para
descobrir o dia da semana e o feriado: com os três campos em branco a data vira zero, e um
dia ou um mês que não existe não tem recusa própria. Se o site espera um aviso de data
inválida, é pergunta ao site.

### RN-13 — A quantidade pedida é obrigatória e tem de respeitar o fracionamento do gênero

A quantidade a ser pedida é obrigatória: zerada, a recusa é **\* Informe quantidade a ser
pedida \***, com o cursor na quantidade. Ela tem de ser um **múltiplo inteiro** da
quantidade de fracionamento do gênero; sobrando resto, a recusa é **\* Quant. fracionada
invalida para este genero \***, com o cursor na quantidade, e nada é gravado.

[?] A conferência divide a quantidade pedida pelo fracionamento do gênero e decide pelo
resto; quando o fracionamento cadastrado é zero a divisão não tem resultado e o resto não é
recalculado, de modo que a conferência decide por um valor que não veio dessa conta. O que
a tela conclui nesse caso não se sabe do acervo. Pergunta ao site.

### RN-14 — A inclusão é confirmada antes de gravar

Passadas todas as conferências, a tela mostra **\* Confirma inclusao do pedido <S/N> ? \***
no campo da resposta, com o cursor nele, e **não grava nada nessa passagem**: ela só
reapresenta o que apurou — o órgão escolhido, o fornecedor, o gênero, a quantidade e a data
de início. Só a resposta **S** grava, e ainda assim apenas se nenhum dos **dez** dados
conferidos tiver mudado entre a pergunta e a resposta: o fornecedor, o número e o ano da
nota, a subclasse, o gênero, o órgão filho, o dia, o mês e o ano do início e a quantidade.
Qualquer outra resposta, ou qualquer mudança em um desses dados, descarta a confirmação e
devolve a tela ao começo das conferências, que pergunta de novo.

[?] Quando a resposta não é afirmativa, a tela descarta a confirmação e volta a conferir
tudo; no caminho da inclusão ela chega outra vez à pergunta, porque a passagem que pergunta
é a mesma que confere os dados. Não se conclui do acervo se o servidor consegue desistir
respondendo "não". Pergunta ao site.

### RN-15 — Confirmada a inclusão, o que fica gravado

Confirmada a inclusão, a tela **numera o pedido**: no cadastro da numeração, por secretaria,
coordenadoria e ano de entrega, ela soma um ao contador do ano quando ele já existe e o abre
em um quando não existe, e o número do pedido é esse contador com o ano de entrega ao lado,
formando o código de dez dígitos.

Com esse número ela abre um **pedido novo** com o fornecedor, o órgão filho de destino, a
coordenadoria da nota, o tipo de contrato, o operador, o cartão do pedido, as matrículas de
quem aprovou e de quem digitou, a data de aprovação e de digitação e a situação de
**fechado** — o pedido novo já nasce fechado. No **gênero do pedido** ela grava o item com
a quantidade pedida, a recebida e a acumulada iguais à quantidade informada, a situação de
item fechado, a marca de que o item vem de um acumulado e o início da entrega na primeira
data de entrega do período.

Do lado do **pedido acumulado de origem** ela desconta a quantidade pedida no gênero,
apagando esse gênero quando a quantidade chega a zero, e apaga o pedido de origem quando
não sobra nenhum gênero dele. No **vínculo entre a nota, o gênero e o pedido** ela também
desconta a quantidade e apaga o vínculo quando ele chega a zero. Depois refaz a **situação
do pedido acumulado**: ele fica **fechado** quando todos os gêneros dele estão fechados e
continua **aprovado** enquanto algum não está. Cada registro tocado deixa uma linha na
**auditoria** com a operação, o cadastro atingido, o número do pedido, a coordenadoria, a
secretaria, a matrícula do servidor, a estação, a data e a hora da sessão e o conteúdo do
registro antes e depois da alteração.

Por fim a tela mostra **\* Pedido cadastrado \*** com o número do pedido e a data, e reabre
a si mesma para o próximo.

[?] O gênero do pedido novo é gravado com a marca de acumulado e o cabeçalho do pedido novo
é gravado **sem** marca de acumulado. As telas que tratam o acumulado comparam essa marca
no cabeçalho do pedido, e não no gênero; do acervo não se conclui o que a marca no gênero
significa nem se o acumulado reconhece esse pedido como parte dele. Pergunta ao site.

### RN-16 — O limite do período informado não chega ao pedido

A tela mostra o **dia**, o **mês** e o **ano limite** do período de entrega e passa os três
por edição numérica, mas não os usa: antes de confirmar ela reescreve o limite com a própria
data de início, e é esse limite que vai para o pedido. O que o servidor digitar nesses três
campos não chega ao pedido, e o período gravado é sempre de um único dia.

[?] Os três campos de limite estão na tela e são conferidos como número, mas nada no acervo
diz se deveriam servir para o servidor escolher o fim do período. Se o site espera um
período de vários dias, o caminho não tem. Pergunta ao site.

### RN-17 — A recusa, a pergunta e a abertura não gravam nada

Cada recusa encerra a passagem **antes** de qualquer gravação: um pedido recusado não cria
pedido, não desconta nada do acumulado, não mexe no vínculo da nota e não deixa linha na
auditoria. A passagem que pede a confirmação também não grava, e a simples abertura da tela
não escreve nem apaga nada.

---

## Cenários BDD

```gherkin
Funcionalidade: Inclusão de pedido a partir do saldo da nota fiscal

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão e a coordenadoria regional escolar
    E tenho acesso à tela E235T

  Cenário: Inclusão do pedido de uma unidade a partir do saldo da nota
    Dado que existe um pedido acumulado da minha coordenadoria com uma nota fiscal lançada
    E que o saldo da nota para o gênero informado cobre a quantidade pedida
    E que o órgão filho de destino está cadastrado, ativo e com os dados completos
    E que o início da entrega é um dia útil, não é feriado e não é anterior à data da nota
    Quando informo o fornecedor, o número e o ano da nota, a subclasse, o gênero, o órgão
      filho, o dia, o mês e o ano do início da entrega e a quantidade
    E confirmo a inclusão
    Então o sistema abre um pedido novo, com o contador do ano somado de um e o ano de
      entrega ao lado
    E o pedido fica com o fornecedor, o órgão filho, a coordenadoria da nota, o tipo de
      contrato, o operador, o cartão e a situação de fechado
    E o gênero do pedido fica com a quantidade pedida, a recebida e a acumulada iguais à
      quantidade informada, com a situação de item fechado e o início da entrega
    E o período do pedido fica com o início e o limite iguais à data informada
    E o gênero do pedido acumulado de origem fica com a quantidade descontada
    E o vínculo entre a nota, o gênero e o pedido fica com a quantidade descontada
    E cada registro tocado deixa uma linha na auditoria
    E vejo a mensagem de pedido cadastrado com o número do pedido e a data

  Cenário: A abertura propõe a inclusão, a coordenadoria do vínculo e o cartão
    Dado que o meu vínculo tem coordenadoria regional escolar
    Quando abro a tela E235T
    Então o campo da operação vem com a inclusão
    E o campo da coordenadoria vem com a coordenadoria do meu vínculo
    E o cartão do pedido vem marcado pela tela
    E no cabeçalho vejo a descrição do tipo de órgão e a data do sistema
    E o cursor começa no órgão filho
    E nada é gravado nem apagado

  Cenário: A tela só inclui
    Dado que estou na tela E235T
    Quando a mensagem chega com uma operação que não é a de inclusão
    Então vejo "* Opcao invalida. Use INC *"
    E o cursor volta ao campo da operação
    E nenhuma nota, fornecedor, gênero ou órgão é lido
    E nada é gravado

  Cenário: A inclusão escreve em seis cadastros e apaga de três
    Dado que passei por todas as conferências e confirmei a inclusão
    Quando a inclusão é gravada
    Então são escritos a numeração dos pedidos, o cadastro dos pedidos, o cadastro dos
      gêneros do pedido, o vínculo entre a nota, o gênero e o pedido, o cadastro das
      quantidades recebidas da nota e a auditoria
    E o gênero e o pedido de origem e o vínculo da nota são apagados quando ficam vazios
    E nenhum outro cadastro é escrito ou apagado

  Cenário: Campo numérico inválido
    Dado que estou na tela E235T
    Quando informo texto onde se espera um código, uma data ou uma quantidade
    Então a tela recusa antes de conferir cadastro nenhum
    E o cursor volta ao campo culpado, quando a tela tem esse destino escrito

  Cenário: O número da nota fiscal é obrigatório
    Dado que estou na tela E235T
    Quando confirmo com o número da nota em branco
    Então vejo "* Informe o numero da nota fiscal *"
    E o cursor volta ao número da nota
    E nada é gravado

  Cenário: O ano da nota fiscal é obrigatório
    Dado que estou na tela E235T
    Quando informo o número da nota e deixo o ano em branco
    Então vejo "* Informe o ano de entrega da nota fiscal *"
    E o cursor volta ao ano da nota
    E nada é gravado

  Cenário: A data da nota é montada com o dia e o mês de emissão
    Dado que informo o ano, o mês e o dia de emissão da nota
    Quando a tela compara o início da entrega com a nota
    Então a data da nota é formada pelo ano, pelo mês e pelo dia de emissão informados

  Cenário: Fornecedor não cadastrado
    Dado que estou na tela E235T
    Quando informo um fornecedor que não está cadastrado ou que está marcado como excluído
    Então vejo "* Fornecedor nao cadastrado *"
    E o cursor volta ao código do fornecedor
    E nada é gravado

  Cenário: A subclasse é obrigatória
    Dado que estou na tela E235T
    Quando confirmo com a subclasse em branco
    Então vejo "* Informe o genero *"
    E o cursor volta à subclasse
    E nada é gravado

  Cenário: Gênero não cadastrado
    Dado que estou na tela E235T
    Quando informo uma subclasse e um gênero que não estão cadastrados no ano da nota
    Então vejo "* Genero nao cadastrado *"
    E o cursor volta à subclasse
    E nada é gravado

  Cenário: Nota fiscal não cadastrada
    Dado que estou na tela E235T
    Quando informo uma nota que não existe para aquele fornecedor e aquele ano
    Então vejo "* Nota fiscal nao cadastrada *"
    E o cursor volta ao número da nota
    E nada é gravado

  Cenário: Gênero que não consta da nota
    Dado que a nota existe, mas entre os itens dela não está o gênero informado
    Quando confirmo a inclusão
    Então vejo "* Genero nao cadastrado nesta nota *"
    E o cursor volta à subclasse
    E nada é gravado

  Cenário: A nota não é de pedido acumulado
    Dado que o pedido a que a nota está amarrada não é um pedido acumulado
    Quando confirmo a inclusão
    Então vejo "* Nota nao e de pedido acumulado *"
    E o cursor volta ao número da nota
    E nada é gravado

  Cenário: O pedido acumulado da nota aparece como processo ou como lote
    Dado que a nota está amarrada a um processo
    Quando a tela mostra o pedido acumulado da nota
    Então o pedido aparece rotulado como "Processo"
    E uma nota sem processo aparece rotulada como "Lote"

  Cenário: Nota fiscal de outra coordenadoria
    Dado que a minha sessão carrega uma coordenadoria regional escolar
    Quando informo uma nota de outra coordenadoria e confirmo
    Então vejo "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao número da nota
    E nada é gravado

  Cenário: Órgão de outra coordenadoria
    Dado que a minha sessão carrega uma coordenadoria regional escolar
    Quando informo um órgão filho de outra coordenadoria e confirmo
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor volta ao órgão filho
    E nada é gravado

  Cenário: Órgão de outra secretaria
    Dado que estou na tela E235T
    Quando informo um órgão filho que não pertence ao tipo de órgão da minha sessão
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor volta ao órgão filho
    E nada é gravado

  Cenário: O órgão filho é obrigatório
    Dado que estou na tela E235T
    Quando confirmo com o órgão filho em branco
    Então vejo "* Informe o orgao *"
    E o cursor volta ao órgão filho
    E nada é gravado

  Cenário: Órgão filho não cadastrado
    Dado que estou na tela E235T
    Quando informo um órgão filho que não está cadastrado e confirmo
    Então vejo "* Orgao nao cadastrado *"
    E o cursor volta ao órgão filho
    E nada é gravado

  Cenário: Órgão filho inativo
    Dado que o órgão filho está marcado como inativo
    Quando confirmo a inclusão
    Então vejo "* Orgao cadastrado como inativo *"
    E o cursor volta ao órgão filho
    E nada é gravado

  Cenário: Órgão filho de pedido acumulado
    Dado que o órgão filho está marcado como órgão de pedido acumulado
    Quando confirmo a inclusão
    Então vejo "* Orgao cadastrado para pedido acumulado *"
    E o cursor volta ao órgão filho
    E nada é gravado

  Cenário: Órgão filho com dados incompletos
    Dado que falta, no cadastro do órgão filho, o bairro, o órgão pai, o nome, o endereço,
      o número de matrículas ou o número de pessoas
    Quando confirmo a inclusão
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E o cursor volta ao órgão filho
    E nada é gravado

  Cenário: A nota não tem saldo disponível
    Dado que a quantidade recebida da nota para o gênero já está toda na quantidade
      recebida acumulada
    Quando confirmo a inclusão
    Então vejo "* Nao existe saldo disponivel para esta nota *"
    E o cursor volta à quantidade
    E nada é gravado

  Cenário: Saldo da nota insuficiente
    Dado que a quantidade pedida passa do saldo disponível da nota
    Quando confirmo a inclusão
    Então vejo "* Saldo da nota insuficiente para o pedido *"
    E o cursor volta à quantidade
    E nada é gravado

  Cenário: O início da entrega não pode ser um sábado
    Dado que estou na tela E235T
    Quando informo como início da entrega uma data que cai em sábado
    Então vejo "* Inicio da entrega nao deve ser um sabado *"
    E o cursor volta ao dia do início
    E nada é gravado

  Cenário: O início da entrega não pode ser um domingo
    Dado que estou na tela E235T
    Quando informo como início da entrega uma data que cai em domingo
    Então vejo "* Inicio da entrega nao deve ser um domingo *"
    E o cursor volta ao dia do início
    E nada é gravado

  Cenário: O início da entrega não pode ser um feriado
    Dado que a data informada é um feriado do tipo de órgão da minha sessão
    Quando confirmo a inclusão
    Então vejo "* Inicio da entrega nao deve ser um feriado *"
    E o cursor volta ao dia do início
    E nada é gravado

  Cenário: O início da entrega não pode ser anterior à nota
    Dado que estou na tela E235T
    Quando informo como início da entrega uma data anterior à data da nota fiscal
    Então vejo "* Inicio da entrega < data da nota *"
    E o cursor volta ao dia do início
    E nada é gravado

  Cenário: A quantidade é obrigatória
    Dado que estou na tela E235T
    Quando confirmo com a quantidade a ser pedida zerada
    Então vejo "* Informe quantidade a ser pedida *"
    E o cursor volta à quantidade
    E nada é gravado

  Cenário: Quantidade fracionada inválida
    Dado que a quantidade informada não é um múltiplo inteiro do fracionamento do gênero
    Quando confirmo a inclusão
    Então vejo "* Quant. fracionada invalida para este genero *"
    E o cursor volta à quantidade
    E nada é gravado

  Cenário: A inclusão é confirmada antes de gravar
    Dado que passei por todas as conferências
    Quando envio a tela
    Então vejo "* Confirma inclusao do pedido <S/N> ? *" no campo da resposta
    E a tela me reapresenta o órgão, o fornecedor, o gênero, a quantidade e a data de início
    E nada é gravado nessa passagem

  Cenário: A inclusão sem a resposta S
    Dado que a tela me perguntou se confirma a inclusão
    Quando respondo qualquer coisa que não seja S
    Então a tela volta ao começo das conferências e me pergunta de novo
    E nada é gravado

  Cenário: A inclusão com um dado mudado depois da pergunta
    Dado que a tela me perguntou se confirma a inclusão
    Quando mudo a quantidade e respondo S
    Então a tela volta ao começo das conferências e me pergunta de novo
    E nada é gravado

  Cenário: O pedido acumulado fecha quando todos os gêneros fecham
    Dado que, depois do desconto, o pedido acumulado de origem fica sem nenhum gênero
      em aberto
    Quando confirmo a inclusão
    Então a situação do pedido acumulado passa a fechado
    E um registro de auditoria do pedido acumulado é incluído

  Cenário: O pedido acumulado continua aprovado enquanto sobra gênero
    Dado que, depois do desconto, ainda sobra gênero em aberto no pedido acumulado
    Quando confirmo a inclusão
    Então a situação do pedido acumulado continua aprovado

  Cenário: O limite do período informado não é usado
    Dado que informo um dia, um mês e um ano limite diferentes do início
    Quando confirmo a inclusão
    Então o período do pedido novo fica com o início e o limite iguais à data de início
    E o limite que eu digitei não vai para o pedido

  Cenário: A recusa não grava nada
    Dado que estou na tela E235T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então nenhum pedido novo foi criado
    E o gênero do pedido acumulado continua com a mesma quantidade
    E o vínculo entre a nota, o gênero e o pedido continua como estava
    E nenhum registro de auditoria foi incluído

  Cenário: A abertura da tela não grava nada
    Dado que o meu vínculo tem coordenadoria regional escolar
    Quando abro a tela E235T
    Então nenhum pedido é criado ou apagado
    E nenhum gênero do pedido é alterado
    E nenhuma auditoria é gravada
```
