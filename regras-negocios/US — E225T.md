# US — E225T — Registrar a quantidade da nota fiscal por gênero no pedido acumulado

## Estória

Como **servidor de CRE**, quero **registrar, gênero por gênero, quanto a nota fiscal de
um fornecedor cobre de um pedido acumulado da minha coordenação**, para que **a
secretaria saiba o que a nota entrega de cada produto e possa conferir a entrega contra
o que foi pedido**.

O pedido acumulado reúne num só documento o que várias unidades pediram a um mesmo
fornecedor, e a nota fiscal que o fornecedor emite precisa ser amarrada, produto por
produto, ao pedido que ela atende. É esta tela que faz a amarração: diz de que gênero a
nota trata e quanto dele está chegando, e a quantidade que ela aceita é limitada pelo que
o pedido previu, de modo que a nota não registre mais do que foi pedido. O lançamento só
sai depois de o servidor ter consultado o mesmo pedido e a mesma nota, o que evita lançar
a entrega contra o pedido errado. Sem esse vínculo a nota fica solta, a conferência da
entrega não fecha e a secretaria não consegue comprovar o que já entrou; a mesma tela
serve para consultar o que está lançado e, nesse caso, não grava nada.

## Contexto

Jornada S000M → E000M → E200M → E220M → E225T.

Ator: servidor de CRE — informa a coordenação regional escolar, o órgão filho, o pedido
acumulado (número do pedido e ano da entrega) e a nota fiscal de um fornecedor (número,
ano e data de emissão) e registra, gênero por gênero, quanto a nota cobre daquele
pedido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os três menus do caminho só encaminham: nenhum deles deixa pedido, nota ou valor para
esta tela, que busca tudo nos cadastros. Das telas anteriores a tela usa apenas o que a
entrada deixou na sessão: a matrícula, o código de acesso, o privilégio, o tipo de órgão
e a coordenação regional escolar. Também não há comportamento que mude conforme quem
chamou a tela: a operação chega com a própria transação (RN-08), e um encaminhamento para
outra tela registrado na transação faz esta abandonar a passagem sem gravar. A tela não
abre outra: a jornada termina nela.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela grava a quantidade da nota no vínculo entre a nota e o pedido

Confirmada a alteração, a tela substitui, no vínculo entre a nota fiscal e o pedido, a
**quantidade do gênero** e o **ano e a data de emissão da nota**; quando o vínculo ainda
não existe para aquela combinação de fornecedor, nota, ano, subclasse, gênero e pedido de
origem, ela o **cria** com a quantidade informada. Cada gravação deixa o seu **registro
de auditoria**. Nenhum outro cadastro é incluído ou alterado e **nada é excluído**, em
nenhum caminho. O cadastro em que ela grava é dimensionado para **100 mil** registros —
capacidade (máximo esperado no dimensionamento), não volume cadastrado.

[?] O ano de emissão da nota faz parte do próprio conjunto de dados que localiza o
vínculo, e o acervo não diz o que acontece quando o operador muda esse ano na tela.
Pergunta ao site.

[?] A tela confere e grava as linhas uma a uma, na ordem da grade; o fonte não permite
concluir se a recusa de uma linha impede a gravação das linhas anteriores, já processadas
na mesma mensagem. Pergunta ao site.

[?] Antes de gravar, a tela reserva o registro que vai alterar, e o acervo não diz o que
essa reserva significa nem por quanto tempo ela vale. Pergunta ao site.

### RN-02 — A consulta não grava e não emite nada

A tela só escreve quando a operação é a **alteração**. Confirmada a consulta, ela mostra
o que apurou e encerra a passagem **sem gravar e sem emitir nada**: não há trabalho de
impressão nem requisição de impressão, e a tela não abre outra. Qualquer recusa — de
campo, de cadastro ou de quantidade — marca a passagem de modo que nenhuma gravação
acontece.

[?] A tela carrega a área de parâmetros de um relatório, com o código de um relatório de
entregas, e a repõe a cada transação, mas não há neste programa nenhum disparo de
impressão. Se a intenção era que esta tela também emitisse um relatório, esse caminho não
existe aqui. Pergunta ao site.

### RN-03 — A grade tem nove linhas, e cada linha tem quatro campos

A grade é mostrada em até **nove linhas** por mensagem. Cada linha carrega **quatro
campos**: o **código da subclasse** (2 dígitos), o **código do gênero** (5), a
**quantidade** (8 inteiros e 3 decimais) e a **ação** da linha (1) — 20 posições por
linha. Fora da grade a tela traz o cabeçalho do pedido e da nota; no todo, **22 campos**
passam pela edição numérica — **13** do cabeçalho do pedido, **6** do pedido de origem e
da nota e **3** da linha.

### RN-04 — Só a linha marcada com a ação A é gravada

A ação é por linha, não pela tela. A tela só grava a linha marcada com a ação **A**:
linha sem ação, ou com ação diferente, é ignorada e não produz gravação nem mensagem. Uma
linha marcada com **A** e sem o código da subclasse é recusada com
**\* Atualize linha preenchida \***, com o cursor de volta ao campo da ação, e a passagem
não grava.

[?] O formulário da tela não está no acervo e não se conclui dele quais ações a grade
aceita; neste fonte, o único caminho de gravação é o da ação **A**, e a grade não oferece
caminho de inclusão nem de exclusão de linha. Se a intenção era que a grade também
incluísse e excluísse, como em outras telas do sistema, esse caminho não existe aqui.
Pergunta ao site.

### RN-05 — A quantidade informada tem de ser diferente da que está registrada

A tela compara a quantidade digitada na linha com a que já está registrada no vínculo
entre a nota e o pedido. Iguais, a recusa é **\* Altere a quantidade \***, com o cursor
de volta ao campo da quantidade, e nada é gravado — isto é, confirmar a linha sem mexer
na quantidade não passa.

[?] O nome de negócio do campo da quantidade não está no acervo: o rótulo que a tela usa
para ele é a própria sigla interna do programa, e o acervo não diz o que essa sigla abre.
O que aqui se chama "quantidade da nota" é a leitura desta jornada, pelo que o campo
recebe no vínculo e pelo que a tela limita contra a quantidade pedida. Pergunta ao site.

### RN-06 — A quantidade informada não pode passar da quantidade pedida

A quantidade lançada para o gênero não pode ser maior que a **quantidade pedida** daquele
gênero no pedido. Passando, a recusa é **\* Quantidade > quantidade pedida \***, com o
cursor de volta ao campo da quantidade, e nada é gravado.

[?] A tela lê o item do pedido para a subclasse e o gênero digitados, mas não recusa
quando esse item não existe: a leitura não tem desfecho de erro, e a passagem segue para
a conferência da quantidade usando a quantidade do item que estiver na área de trabalho.
Se a intenção era exigir que o gênero pertencesse ao pedido, essa conferência não existe
neste fonte. Pergunta ao site.

### RN-07 — A alteração exige ter consultado antes o mesmo pedido e a mesma nota

Para alterar, o pedido e a nota informados têm de ser **os mesmos da última consulta**: a
tela compara o órgão filho, a coordenação regional escolar, o número do pedido acumulado,
o pedido de origem e o número da nota com o que ela guardou. Não batendo, a recusa é
**\* Consulte antes de atualizar \***, com o cursor de volta ao campo da operação, e nada
é gravado. É por isso que a conferência do órgão, do pedido e da nota roda no caminho da
consulta: é ela que deixa em contexto o que a alteração vai exigir depois.

### RN-08 — A tela só atende consulta e alteração

A operação informada só pode ser **consulta** ou **alteração**. Qualquer outra é recusada
com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta ao campo da
operação, antes de qualquer leitura do pedido e da nota. Chegando à tela sem operação
informada, ela adota a consulta. Quando a transação chega com um encaminhamento para
outra tela, esta abandona a passagem sem gravar.

[?] A recusa manda usar **ALT** e **CON**, mas a guarda compara a operação com os códigos
internos de alteração e de consulta, que são outros. Ou o formulário da tela traduz o que
o servidor digita, ou a mensagem indica valores que a tela não aceita — e, neste segundo
caso, a alteração inteira fica inalcançável por este caminho. Pergunta ao site; não
concluo qual dos dois.

### RN-09 — Ao abrir, a tela repõe o que ficou da última consulta e limpa os campos de resultado

Enquanto a tela continuar em uso, ela guarda o pedido e a nota da última consulta e, ao
ser aberta de novo, os campos aparecem preenchidos com eles outra vez, junto com as
linhas do pedido — a subclasse, o gênero, a descrição resumida do gênero, a quantidade
pedida, a quantidade registrada na nota e a ação. Não havendo nada guardado, a tela abre
em branco, com a operação em consulta. Quando o pedido guardado não tem nenhum gênero, a
tela avisa **\* Nao existem generos cadastrados \*** e não mostra linha nenhuma. Antes de
conferir o que o operador digitou, a tela apaga **nove campos de resultado** — a descrição
do órgão da sessão, a data do sistema, a descrição do órgão filho, a razão social do
fornecedor, o nome do operador, o código e o nome do órgão do pedido, a descrição
resumida do gênero e a quantidade pedida —, de modo que uma mensagem recusada não deixa
na tela o resultado da mensagem anterior; em seguida repõe a descrição do órgão da sessão
e a data do sistema.

### RN-10 — Os campos numéricos passam pela edição numérica

Os **22 campos** numéricos do cabeçalho e da grade passam pela edição numérica antes de
qualquer conferência de negócio; o que chega em branco é tratado como zero. O campo da
quantidade é o único conferido como número com **três casas decimais**. A tela guarda as
posições de cursor dos campos que ela própria recusa: o órgão filho, o número do pedido
acumulado, o ano da entrega, o número e o ano do pedido de origem, o número, o dia, o mês
e o ano da nota, e a quantidade de cada linha.

[?] O que o operador vê quando a digitação é recusada não se conclui desta tela: a rotina
que faz a edição numérica não faz parte do acervo lido. Pergunta ao site.

### RN-11 — O órgão filho é obrigatório e passa por quatro conferências

O órgão filho é exigido: em branco, a recusa é **\* Informe o orgao \***, com o cursor no
campo. Informado, ele tem de estar **cadastrado** (senão **\* Orgao nao cadastrado \***),
não pode estar marcado como excluído — a tela segue procurando o próximo —, tem de ser do
**tipo de órgão da sessão** (senão **\* Orgao nao pertence a esta secretaria \***), e,
quando o vínculo da sessão tem coordenação regional escolar, o órgão tem de ser **daquela
coordenação** (senão **\* Usuario sem acesso ao grupo deste orgao \***). Por fim, o órgão
tem de estar habilitado a **pedido acumulado** (senão
**\* Orgao nao cadastrado para pedido acumulado \***). Em todas essas recusas o cursor
volta ao campo do órgão filho e nada é lido adiante.

### RN-12 — O pedido tem de estar cadastrado e ser um pedido acumulado ainda não calculado

O número do pedido acumulado é exigido — em branco, a recusa é
**\* Informe o numero do pedido \***, com o cursor no campo do número. Informado, o
pedido tem de estar **cadastrado** (senão **\* Pedido nao cadastrado \***) e tem de estar
marcado como **acumulado** (senão **\* Pedido nao acumulado \***). O acumulado já
**calculado** é recusado com **\* Pedido acumulado calculado \***, e o auxiliar do
acumulado já calculado com **\* Pedido auxiliar do acumulado calculado \***. Nas cinco
recusas o cursor volta ao número do pedido e nada é lido adiante.

### RN-13 — O pedido informado tem de constar do acumulado e ser do órgão informado

O **pedido de origem** — o número e o ano do pedido a que a nota é lançada — é exigido:
em branco, a recusa é **\* Informe o numero do pedido \***, com o cursor nesse número. O
órgão do pedido acumulado tem de ser o **órgão filho informado** (senão
**<- Pedido de outro orgao \***) e o pedido de origem tem de **constar entre os pedidos
do acumulado** (senão **\* Pedido nao cad. no pedido acumulado \***); a tela percorre os
pedidos do acumulado até achar o informado.

[?] A mesma mensagem — **\* Informe o numero do pedido \*** — serve a dois campos
diferentes: o número do pedido acumulado e o número do pedido de origem, que a tela
distingue. Se cada campo deveria ter o seu aviso, o texto não os distingue. Pergunta ao
site.

[?] A tela não rotula os dois campos do pedido de origem: os rótulos que ela usa para eles
são as próprias siglas internas do programa, e o acervo não diz como o formulário os
apresenta ao servidor. Pergunta ao site.

### RN-14 — A nota fiscal tem de estar lançada contra esse pedido

O número da nota fiscal é exigido: em branco, a recusa é **\* Informe nota fiscal \***,
com o cursor no campo. Informado, a tela procura a nota **daquele fornecedor e daquele
ano** e, encontrando registro da nota lançado em **outro pedido**, recusa com
**<- Nota cad em outro pedido \***, com o cursor de volta ao número da nota, e nada é
gravado.

[?] A procura da nota é feita com o fornecedor, o número e o ano informados, deixando em
branco a subclasse, o gênero e o pedido; o que essa procura alcança quando a chave vai
incompleta é semântica do banco de dados, e o acervo não a define. Se a intenção era
conferir a nota inteira, e não um registro dela, não se conclui daqui. Pergunta ao site.

### RN-15 — A data da nota é obrigatória, tem de ser válida e não anterior ao início do pedido

O ano de emissão da nota é exigido: em branco, a recusa é
**\* Informe data nota fiscal \***, com o cursor no dia da nota. Informada, a data tem de
ser uma data real e ter o **ano entre 1994 e 2099** (senão **\* Data da nota invalida \***)
e **não pode ser anterior ao início do período do pedido** (senão
**\* Data da nota < data pedido \***), sempre com o cursor de volta ao dia da nota.

[?] A tela busca a data de hoje e o ano corrente e não os usa na conferência: a recusa por
data inválida usa uma faixa fixa de anos. Se a intenção era limitar a data ao ano
corrente, a conferência não faz isso. Pergunta ao site.

### RN-16 — O fornecedor e o operador são mostrados, mas não recusam

O fornecedor informado é lido apenas para a tela mostrar a **razão social**; o operador
do pedido, para mostrar o **nome**, e o operador zerado nem é procurado. Nenhum dos dois
é exigido e nenhum dos dois recusa a passagem quando não é encontrado — o campo
simplesmente fica em branco. O tipo de contrato vem do pedido e é apenas mostrado.

---

## Cenários BDD

```gherkin
Funcionalidade: Registrar a quantidade da nota fiscal por gênero no pedido acumulado

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão e a coordenação regional escolar
    E tenho acesso à tela E225T

  Cenário: Consultar o que a nota já cobre do pedido acumulado
    Dado que existe um pedido acumulado do meu órgão filho, com gêneros pedidos
    Quando informo a coordenação, o pedido acumulado, o pedido de origem e a nota fiscal e confirmo a consulta
    Então a tela mostra o órgão, o fornecedor, o operador e o pedido
    E mostra as linhas do pedido com a subclasse, o gênero, a quantidade pedida e a quantidade registrada na nota
    E não grava e não emite nada

  Cenário: A tela registra a quantidade de um gênero da nota no pedido acumulado
    Dado que consultei o pedido acumulado e a nota fiscal de um fornecedor
    E que a linha traz a subclasse e o gênero com uma quantidade diferente da registrada
    Quando confirmo a alteração com a linha marcada com a ação A
    Então a quantidade daquele gênero passa a ser a informada no vínculo entre a nota e o pedido
    E a alteração deixa o seu registro de auditoria

  Cenário: O vínculo entre a nota e o pedido é criado quando ainda não existe
    Dado que consultei o pedido e a nota e não há registro daquele gênero para a nota
    Quando confirmo a alteração com a quantidade informada, marcada com a ação A
    Então o vínculo entre a nota e o pedido é criado com a quantidade informada
    E a inclusão deixa o seu registro de auditoria

  Cenário: A tela não exclui nada
    Dado que confirmei uma alteração na tela E225T
    Quando a gravação termina
    Então nenhum registro de negócio é excluído
    E nenhum outro cadastro além do vínculo entre a nota e o pedido é alterado

  Cenário: A confirmação recusada não grava nada
    Dado que a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então nenhum vínculo entre a nota e o pedido foi criado ou alterado
    E nenhum registro de auditoria foi gerado

  Cenário: A grade tem nove linhas
    Dado que abri a tela E225T com um pedido acumulado consultado
    Então vejo até nove linhas
    E cada linha tem o código da subclasse, o código do gênero, a quantidade e a ação

  Cenário: Linha sem a ação A não é gravada
    Dado que consultei o pedido e a nota
    Quando confirmo a alteração deixando uma linha sem ação, ou com ação diferente de A
    Então aquela linha não é gravada
    E nenhuma mensagem é mostrada por causa dela

  Cenário: Linha marcada com A e sem subclasse
    Dado que consultei o pedido e a nota
    Quando confirmo a alteração com uma linha marcada com A e sem o código da subclasse
    Então vejo a mensagem "* Atualize linha preenchida *"
    E o cursor volta ao campo da ação
    E nada é gravado

  Cenário: A quantidade tem de mudar
    Dado que consultei o pedido e a nota
    Quando confirmo a alteração com a mesma quantidade que já está registrada
    Então vejo a mensagem "* Altere a quantidade *"
    E o cursor volta ao campo da quantidade
    E nada é gravado

  Cenário: A quantidade não pode passar da pedida
    Dado que consultei o pedido e a nota
    Quando confirmo a alteração com uma quantidade maior que a pedida para aquele gênero
    Então vejo a mensagem "* Quantidade > quantidade pedida *"
    E o cursor volta ao campo da quantidade
    E nada é gravado

  Cenário: A alteração exige ter consultado antes
    Dado que não consultei aquele pedido e aquela nota
    Quando confirmo a alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Operação diferente de consulta e de alteração
    Dado que estou na tela E225T
    Quando chego à tela com uma operação que não é consulta nem alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido e nada é gravado

  Cenário: Encaminhamento para outra tela abandona a passagem
    Dado que a transação chega com um encaminhamento para outra tela
    Quando a tela E225T é aberta
    Então a tela abandona a passagem
    E nada é lido e nada é gravado

  Cenário: Abrir a tela repõe a última consulta
    Dado que consultei um pedido acumulado e uma nota
    Quando abro a tela E225T de novo
    Então os campos do pedido e da nota aparecem preenchidos com os que consultei
    E as linhas do pedido aparecem outra vez
    E nada é gravado

  Cenário: Abrir a tela sem nada guardado
    Dado que não há consulta guardada nesta sessão
    Quando abro a tela E225T
    Então os campos ficam em branco
    E a operação aparece como consulta
    E nada é gravado

  Cenário: Pedido guardado sem gênero
    Dado que o pedido da última consulta não tem nenhum gênero
    Quando abro a tela E225T
    Então vejo a mensagem "* Nao existem generos cadastrados *"
    E nenhuma linha é mostrada
    E nada é gravado

  Cenário: Os campos de resultado da mensagem anterior são apagados
    Dado que a mensagem anterior mostrou a razão social de um fornecedor
    Quando envio uma mensagem que é recusada
    Então a razão social da mensagem anterior não fica na tela
    E vejo a descrição do órgão da minha sessão e a data do sistema

  Cenário: A digitação passa pela edição numérica antes das conferências
    Dado que estou na tela E225T
    Quando envio a mensagem com os campos numéricos informados
    Então a edição numérica roda antes de qualquer conferência de negócio
    E o campo numérico deixado em branco é tratado como zero

  Cenário: Órgão filho em branco
    Dado que estou na tela E225T
    Quando confirmo sem informar o órgão filho
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor volta ao campo do órgão filho
    E nada é lido adiante

  Cenário: Órgão filho não cadastrado
    Dado que estou na tela E225T
    Quando informo um órgão filho que não está cadastrado
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão filho

  Cenário: Órgão filho marcado como excluído não é aceito
    Dado que estou na tela E225T
    Quando informo um órgão filho cujo único cadastro está marcado como excluído
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão filho

  Cenário: Órgão filho de outra secretaria
    Dado que estou na tela E225T
    Quando informo um órgão filho que não é do tipo de órgão da minha sessão
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E o cursor volta ao campo do órgão filho

  Cenário: Órgão filho de outra coordenação
    Dado que a minha sessão carrega uma coordenação regional escolar
    Quando informo um órgão filho de outra coordenação
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor volta ao campo do órgão filho

  Cenário: Órgão filho que não acumula pedido
    Dado que estou na tela E225T
    Quando informo um órgão filho que não está habilitado a pedido acumulado
    Então vejo a mensagem "* Orgao nao cadastrado para pedido acumulado *"
    E o cursor volta ao campo do órgão filho

  Cenário: Pedido acumulado em branco
    Dado que estou na tela E225T
    Quando confirmo sem informar o número do pedido acumulado
    Então vejo a mensagem "* Informe o numero do pedido *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido não cadastrado
    Dado que estou na tela E225T
    Quando informo um pedido que não está cadastrado
    Então vejo a mensagem "* Pedido nao cadastrado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido que não é acumulado
    Dado que estou na tela E225T
    Quando informo um pedido que não está marcado como acumulado
    Então vejo a mensagem "* Pedido nao acumulado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido acumulado já calculado
    Dado que estou na tela E225T
    Quando informo um pedido acumulado já calculado
    Então vejo a mensagem "* Pedido acumulado calculado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Auxiliar do acumulado já calculado
    Dado que estou na tela E225T
    Quando informo o auxiliar de um acumulado já calculado
    Então vejo a mensagem "* Pedido auxiliar do acumulado calculado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido de outro órgão
    Dado que estou na tela E225T
    Quando informo um pedido acumulado de outro órgão filho
    Então vejo a mensagem "<- Pedido de outro orgao *"
    E o cursor volta ao campo do órgão filho

  Cenário: Pedido de origem em branco
    Dado que consultei o pedido acumulado
    Quando confirmo sem informar o número do pedido de origem
    Então vejo a mensagem "* Informe o numero do pedido *"
    E o cursor volta ao campo do número do pedido de origem

  Cenário: Pedido de origem que não consta do acumulado
    Dado que consultei o pedido acumulado e a nota
    Quando informo um pedido de origem que não consta do acumulado
    Então vejo a mensagem "* Pedido nao cad. no pedido acumulado *"
    E o cursor volta ao campo do número do pedido de origem

  Cenário: Nota fiscal em branco
    Dado que consultei o pedido acumulado
    Quando confirmo sem informar o número da nota fiscal
    Então vejo a mensagem "* Informe nota fiscal *"
    E o cursor volta ao campo do número da nota

  Cenário: Nota lançada em outro pedido
    Dado que a nota fiscal informada está lançada em outro pedido
    Quando confirmo
    Então vejo a mensagem "<- Nota cad em outro pedido *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: Data da nota em branco
    Dado que consultei o pedido acumulado e a nota
    Quando confirmo sem informar o ano de emissão da nota
    Então vejo a mensagem "* Informe data nota fiscal *"
    E o cursor volta ao campo do dia da nota

  Cenário: Data da nota inválida
    Dado que consultei o pedido acumulado e a nota
    Quando informo uma data que não existe, ou um ano fora da faixa aceita
    Então vejo a mensagem "* Data da nota invalida *"
    E o cursor volta ao campo do dia da nota
    E nada é gravado

  Cenário: Data da nota anterior ao início do pedido
    Dado que consultei o pedido acumulado e a nota
    Quando informo uma data de emissão anterior ao início do período do pedido
    Então vejo a mensagem "* Data da nota < data pedido *"
    E o cursor volta ao campo do dia da nota
    E nada é gravado

  Cenário: Fornecedor ou operador não cadastrado não recusa a passagem
    Dado que consultei o pedido acumulado e a nota
    Quando o fornecedor ou o operador do pedido não está cadastrado
    Então a tela segue sem mostrar a razão social ou o nome
    E nenhuma mensagem de recusa é mostrada por causa disso
```
