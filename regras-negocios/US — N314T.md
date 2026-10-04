# US — N314T — Registrar a nota fiscal da entrega do pedido

## Estória

Como **servidor de CRE**, quero **registrar os dados da nota fiscal que o fornecedor
entregou contra um pedido**, para que **a entrega fique amarrada ao pedido, ao contrato
e ao grupo da CRE, e o que veio possa ser conferido e pago pelo saldo certo**.

A nota fiscal é o documento com que o fornecedor comprova a entrega; sem ela registrada
contra um pedido, não há como conferir o que chegou nem liberar o pagamento. É este
registro que identifica a nota — número, as suas duas datas, a chave de acesso, o
modelo, o fornecedor e o operador logístico — e o amarra a um pedido, a um contrato e
ao grupo da CRE. Registrada a identificação, é ela que abre a tela em que os gêneros e
as quantidades cobertos pela nota são informados; sem esse registro, a nota não existe
para o sistema e a entrega fica sem conferência.

## Contexto

Jornada S000M → N000M → N050M → N300M → N314T.

Ator: servidor de CRE — identifica a nota fiscal recebida do fornecedor contra um
pedido e a encaminha ao lançamento dos gêneros.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
dado de navegação, não regra de negócio.

Esta tela entrega o cabeçalho à tela seguinte: confirmada a inclusão ou a alteração,
ela deixa na sessão o que foi informado — número, as duas datas, a chave de acesso, o
modelo, o fornecedor, o pedido, o ano da entrega, o contrato, o grupo, o órgão e o
operador logístico — marcado com a sua origem, e leva o servidor à tela dos gêneros da
nota (a N324T), que é quem cria a nota e recebe os gêneros. Em consulta, ela também
encaminha o servidor àquela tela, em modo de consulta.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela abre em inclusão; só a tela dos gêneros a abre preenchida

Aberta pelo menu — ou por qualquer tela que não seja a dos gêneros da nota —, a tela se
monta para uma nota nova: os campos vêm em branco, a operação já vem posta como
inclusão, o modelo da nota vem preenchido com o código 55, o número da nota e a chave
de acesso vêm zerados e o grupo da CRE vem preenchido com o grupo da sessão, quando o
servidor tem um.

Aberta pela tela dos gêneros, a tela se monta preenchida com o que aquela tela deixou na
sessão — o modelo, as duas datas, o fornecedor e a sua razão social, o operador
logístico e o seu nome, o grupo, o tipo de contrato, o número do pedido, o ano da
entrega e o órgão — e com a operação que ela definiu. Em qualquer das origens o número
da nota chega em branco: é campo que o servidor digita.

[?] O modelo vem preenchido com o código 55, mas a descrição dos modelos mora no
cadastro de modelos de nota fiscal, cujo conteúdo não está no lote. O que o código 55
significa não se sabe. Pergunta ao site.

### RN-02 — A tela atende a quatro operações, e a operação é escolhida nela

A tela atende a quatro operações: incluir, alterar, excluir e consultar. A operação é um
campo da própria tela, e vem com inclusão quando a tela é aberta pelo menu. Incluir,
alterar e excluir só passam quando a tela está em condição de manutenção; consultar
passa sempre. Com uma operação que não seja nenhuma dessas quatro, a tela é recusada
com **\* Operacao nao disponivel \*** e nada é processado.

[?] O rótulo do campo da operação e os valores que a tela aceita não estão no lote (a
máscara da tela não vem nos fontes). O que o servidor vê e digita nesse campo é
conclusão, não fonte. Pergunta ao site.

### RN-03 — O grupo da nota é o grupo do usuário

O grupo (coordenadoria regional de ensino) informado tem de ser o grupo da sessão. Quem
não tem grupo na sessão pode informar qualquer grupo, mas não pode deixar o campo em
branco: sem grupo na sessão e sem grupo no campo, a recusa é **\* Informe o grupo \***.
Com grupo na sessão e grupo diferente no campo, a recusa é
**\* Usuario sem acesso a outro grupo \***. A mesma conferência vale para a nota já
cadastrada: a nota de outro grupo é recusada.

### RN-04 — O modelo da nota fiscal é obrigatório e tem de estar cadastrado

O modelo é obrigatório: em branco, a operação é recusada com
**\* Informe o modelo da nota fiscal \***. Informado, ele é procurado no cadastro de
modelos e, não existindo, a recusa é **\* Modelo de nota fiscal nao cadastrado \***. Na
inclusão o modelo é sempre conferido; na alteração, a conferência de existência só
acontece quando o modelo foi trocado. Achado o modelo, a sua descrição é trazida para a
tela.

### RN-05 — Para alterar, excluir ou consultar, a nota é identificada por três dados

A alteração, a exclusão e a consulta não procuram a nota pelo que está na tela: exigem
que o servidor informe o número da nota, o ano da entrega e o código do operador
logístico. Faltando o número, a recusa é **\* Informe o numero da nota fiscal \***;
faltando o ano, **\* Informe o ano de entrega da nota \***; faltando o operador,
**\* Informe o codigo do oper.logistico \***. Com os três informados, a nota é
procurada no cadastro de notas fiscais pelo órgão, pelo operador, pelo número e pelo
ano; não sendo encontrada, a recusa é **\* Nota fiscal nao cadastrada \***.

### RN-06 — A chave de acesso é conferida

A chave de acesso tem 44 caracteres e é conferida em três pontos. Primeiro, o número da
nota que está dentro da chave tem de ser o número informado. Segundo, o CNPJ que está
dentro da chave tem de ser o do fornecedor cadastrado para aquele operador logístico.
Terceiro, o último caractere da chave é um dígito de conferência, que o sistema
recalcula a partir dos outros 43, com pesos que vão de 2 a 9 e o resto da divisão por
11. Falhando qualquer um dos três, a recusa é **\* Chave de acesso invalida \*** e o
cursor volta ao campo da chave. Na inclusão a chave é sempre conferida; na alteração,
só quando ela foi trocada.

[?] A conferência do CNPJ compara com o cadastro do fornecedor apenas os oito primeiros
dígitos, embora a chave carregue catorze. Se a intenção era conferir os catorze,
pergunta ao site.

### RN-07 — A data de entrega da nota fiscal

A data de entrega — os três campos que a tela rotula como emissão N.F. — tem de ser uma
data de calendário válida, com o ano entre 1994 e 2099; não pode ser posterior à data
atual; e não pode ser anterior ao início do pedido. As recusas são
**\* Data de entrega invalida \***, **\* Data de entrega > que a data atual \*** e
**\* Data de entrega menor que data do pedido \***. Na alteração, só é conferida quando
foi trocada.

[?] Os campos que a tela rotula como emissão N.F. são tratados pelo sistema como a data
de entrega, e os rotulados apenas como emissão são tratados como a data de emissão; os
próprios avisos do sistema chamam a primeira de "data de entrega" e a segunda de "data
de emissão". Qual dos dois sentidos é o de negócio, o acervo não diz. Pergunta ao site.

### RN-08 — A data de emissão da nota fiscal

A data de emissão também tem de ser uma data de calendário válida, com o ano entre 1994
e 2099; não pode ser posterior à data de entrega, e não pode ser anterior ao início do
pedido em mais de 20 dias. As recusas são **\* Data de emissao invalida \*** (data
inválida), **\* Data da emissao invalida \*** (anterior demais ao pedido) e
**\* Data de emissao > data da entrega \***. Na alteração, a data de emissão é
conferida sempre.

### RN-09 — O lançamento exige um pedido em situação de recebimento

O número do pedido é obrigatório: em branco, a recusa é
**\* Informe o numero do pedido \***. O pedido é procurado pelo órgão, pelo grupo e pelo
número; não existindo, a recusa é **\* Pedido nao cadastrado \***. Do pedido saem o
fornecedor, o operador logístico e o órgão, e dos cadastros deles vêm a razão social do
fornecedor e os nomes do operador e do órgão; o tipo de contrato vem do item do pedido.
Achado o pedido, ele ainda é recusado quando está excluído
(**\* Pedido excluido \***), quando não tem operador logístico
(**\* Pedido nao e de oper.logistico \***), quando está aprovado e fechado
(**\* Pedido aprovado - fechado \***), quando está pendente de distribuição
(**\* Pedido pendente de distribuicao \***) e quando está pendente de aprovação
(**\* Pedido pendente de aprovacao \***). A data de entrega também não pode ser anterior
ao início do pedido.

[?] As situações do pedido são lidas como letras — uma para aprovado e fechado, uma para
pendente de distribuição e o vazio para pendente de aprovação —, e a exclusão da nota
regrava o pedido fechado numa quarta situação. O significado das letras não está no
dicionário nem em mensagem do programa. Pergunta ao site.

### RN-10 — O órgão e o contrato têm de ser do grupo e de operação logística

O órgão que veio do pedido é lido no cadastro de órgãos e tem de pertencer ao grupo
informado: não pertencendo, a recusa é **\* Orgao nao pertence a este grupo \***. O
contrato do tipo que veio do item do pedido é lido no cadastro de contratos e tem de ser
de operação logística: não sendo, a recusa é
**\* Contrato nao e de Oper.Logistico \***. Nenhuma das duas recusas grava coisa alguma.

### RN-11 — A nota não pode estar já cadastrada nem ter entrega confirmada

Na inclusão, o sistema procura a nota pelo órgão, pelo operador, pelo número e pelo ano:
achando-a já cadastrada, recusa com **\* Nota ja cadastrada. Use ALT. \***; achando
entrega já confirmada para aquela nota, recusa com
**\* Nota fiscal com entrega confirmada \***. Na alteração, na exclusão e na consulta, a
entrega confirmada também recusa com **\* Nota fiscal com entrega confirmada \***, e a
nota que não está cadastrada recusa com **\* Nota fiscal nao cadastrada \***. Em
qualquer desses caminhos, a nota cujo grupo não é o grupo do servidor é recusada com
**\* Usuario sem acesso ao grupo desta nota \***.

### RN-12 — O sistema pede confirmação antes de gravar

Antes de gravar, o sistema pergunta e espera resposta em um campo de um caractere:
**\* Confirma inclusao da nota <S/N> ? \***, **\* Confirma alteracao da nota fiscal
<S/N> ? \*** ou **\* Confirma exclusao da nota fiscal <S/N> ? \***, conforme a operação.
Só a resposta "S" leva à gravação; qualquer outra resposta desfaz a confirmação. E,
mesmo com "S", a gravação só acontece se os dados que identificam a operação continuarem
iguais aos que foram guardados quando a pergunta foi feita: a própria operação, o número
da nota, as três partes da data de entrega, o grupo, o número do pedido, o ano da
entrega, o operador logístico e a chave de acesso — dez campos. Mudando qualquer um
deles, a confirmação é desfeita e a pergunta volta.

[?] O rótulo do campo onde se digita a resposta não está no lote; o programa compara o
conteúdo com "S", mas se outro caractere é aceito como recusa explícita, ou se qualquer
coisa diferente de "S" apenas cancela, o acervo não diz. Pergunta ao site.

### RN-13 — A inclusão não grava a nota: ela entrega o cabeçalho à tela dos gêneros

Confirmada a inclusão, esta tela não grava a nota fiscal. Ela deixa na sessão tudo o que
foi informado, marcado com a sua origem e com a operação de alteração, e encaminha o
servidor à tela dos gêneros da nota (a N324T) — que é quem cria a nota, com a data de
entrada do dia do sistema —, para que os gêneros e as quantidades sejam informados. A
nota só existe depois disso: sem passar por aquela tela, não há nota cadastrada.

### RN-14 — A alteração regrava o que mudou na nota

Confirmada a alteração, o sistema relê a nota e regrava o que mudou: o modelo, quando o
modelo foi trocado; a chave de acesso, quando a chave foi trocada; e as três partes da
data de emissão, quando a data de emissão foi trocada. Cada uma dessas gravações deixa
um registro de auditoria com o cadastro tocado, a operação, o conteúdo anterior e o
posterior, a matrícula do funcionário, a estação, o número do processo (o pedido), a
data e a hora da sessão e o tipo de órgão. Terminada a alteração, o servidor é
encaminhado à tela dos gêneros, em alteração.

[?] A alteração só regrava o modelo, a chave e a data de emissão: trocar na alteração a
data de entrega, o pedido, o operador logístico ou o fornecedor é aceito pelas
conferências e não é gravado — a nota continua com o que tinha. Se essas trocas deveriam
ser recusadas ou gravadas, o acervo não diz. Pergunta ao site.

### RN-15 — A exclusão apaga a nota, apaga os gêneros e estorna os saldos

Confirmada a exclusão, o sistema percorre os gêneros da nota e, para cada um, estorna a
quantidade: diminui o saldo do contrato e a quantidade recebida do item do pedido,
devolvendo-os ao estado anterior ao lançamento; se o pedido estava aprovado e fechado,
devolve-o à situação de recebimento; apaga a linha do gênero; e deixa um registro de
auditoria de cada gravação. Percorridos todos os gêneros, apaga a nota fiscal. A
exclusão não encaminha o servidor a outra tela.

[?] A exclusão é a única das três operações que não encaminha o servidor a outra tela: a
inclusão e a alteração o levam à tela dos gêneros e a exclusão termina sem destino
marcado. Se a exclusão deveria voltar ao menu ou à tela de origem, o acervo não diz.
Pergunta ao site.

### RN-16 — A consulta não grava nada

Em consulta, a tela procura a nota pela identificação informada, traz para a tela o
cabeçalho da nota e os nomes que vêm dos cadastros, e encaminha o servidor à tela dos
gêneros, em consulta. Nessa operação nada é gravado, alterado ou apagado, e nenhum
registro de auditoria sai desta tela.

[?] A consulta usa a mesma identificação da alteração e da exclusão — órgão, operador,
número e ano — e não há, nesta tela, consulta por pedido, por fornecedor ou pela chave
de acesso. Se é assim mesmo, pergunta ao site.

### RN-17 — A operação depende da autorização do usuário

Na montagem, o sistema confere a permissão do usuário para a tela; na confirmação,
confere a rota e a autorização da operação pedida, com o contexto da sessão (matrícula,
código de acesso, privilégio, tipo de órgão e grupo). Sem autorização, a tela não é
montada ou a operação é abandonada sem gravar, com a mensagem de acesso negado.

### RN-18 — A conferência dos campos antes de processar

Ao confirmar, o sistema percorre um a um 14 campos da tela — número da nota; as três
partes de cada uma das duas datas; grupo; número do pedido; ano da entrega; tipo de
contrato; fornecedor; órgão; e operador logístico — tratando cada um como número: campo
em branco vira zero, zeros à esquerda são descartados e o conteúdo não numérico é
recusado. Recusado o conteúdo, o campo é marcado e o cursor volta para ele, na posição
definida para onze desses campos. A descrição do tipo de órgão e a data do sistema são
limpas a cada entrada.

[?] O texto da mensagem mostrada quando um desses campos não é numérico vem de uma
rotina da biblioteca comum do gerador, que o lote não traz implementada; o que o
servidor lê nesse caso não se sabe. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Registrar a nota fiscal da entrega do pedido

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N314T

  Cenário: A tela abre em inclusão vinda do menu
    Dado que escolhi a N314T no menu N300M
    Quando a tela abre
    Então os campos vêm em branco, com a operação de inclusão já posta
    E o modelo da nota vem preenchido com o código 55
    E o número da nota e a chave de acesso vêm zerados
    E o grupo vem preenchido com o grupo da minha sessão, quando eu tenho um

  Cenário: A tela volta preenchida vinda da tela dos gêneros
    Dado que a tela dos gêneros da nota me encaminhou de volta à N314T
    Quando a tela abre
    Então vejo o modelo, as duas datas, o fornecedor com a sua razão social, o
      operador logístico com o seu nome, o grupo, o tipo de contrato, o número do
      pedido, o ano da entrega e o órgão que aquela tela deixou
    E o número da nota vem em branco, para eu digitar

  Cenário: Inclusão de uma nota fiscal
    Dado que informei o número da nota, as duas datas, a chave de acesso, o modelo,
      o grupo, o número do pedido, o ano da entrega e o operador logístico
    E o pedido está em situação de recebimento, o órgão é do meu grupo e o contrato
      é de operação logística
    Quando confirmo a inclusão com "S"
    Então o sistema deixa o cabeçalho na sessão, marcado com a origem desta tela e
      com a operação de alteração
    E sou encaminhado à tela dos gêneros da nota
    E a nota é criada lá, com a data de entrada do dia do sistema

  Cenário: A confirmação não é aceita
    Dado que preenchi a nota e o sistema pediu a confirmação
    Quando respondo qualquer coisa diferente de "S"
    Então a confirmação é desfeita
    E nada é gravado

  Cenário: A confirmação é desfeita quando os dados mudam
    Dado que o sistema pediu a confirmação da inclusão
    Quando altero o número da nota, a data de entrega, o grupo, o pedido, o ano da
      entrega, o operador ou a chave antes de responder
    Então a confirmação é desfeita e a pergunta volta
    E nada é gravado

  Cenário: Grupo diferente do grupo do usuário
    Dado que tenho grupo na sessão e informei outro grupo
    Quando confirmo
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo do grupo
    E nada é gravado

  Cenário: Grupo não informado
    Dado que não tenho grupo na sessão e deixei o grupo em branco
    Quando confirmo
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nada é gravado

  Cenário: Modelo da nota em branco
    Dado que deixei o modelo da nota fiscal em branco
    Quando confirmo
    Então vejo a mensagem "* Informe o modelo da nota fiscal *"
    E o cursor volta ao campo do modelo
    E nada é gravado

  Cenário: Modelo da nota não cadastrado
    Dado que informei um modelo que não existe no cadastro de modelos
    Quando confirmo
    Então vejo a mensagem "* Modelo de nota fiscal nao cadastrado *"
    E o cursor volta ao campo do modelo
    E nada é gravado

  Cenário: Chave de acesso inválida
    Dado que a chave de acesso não confere com o número da nota, com o CNPJ do
      fornecedor ou com o dígito de conferência
    Quando confirmo
    Então vejo a mensagem "* Chave de acesso invalida *"
    E o cursor volta ao campo da chave
    E nada é gravado

  Cenário: Data de entrega inválida
    Dado que informei uma data de entrega que não existe no calendário ou com o ano
      fora de 1994 a 2099
    Quando confirmo
    Então vejo a mensagem "* Data de entrega invalida *"
    E o cursor volta ao campo da data de entrega
    E nada é gravado

  Cenário: Data de entrega posterior à data atual
    Dado que informei uma data de entrega no futuro
    Quando confirmo
    Então vejo a mensagem "* Data de entrega > que a data atual *"
    E o cursor volta ao campo da data de entrega
    E nada é gravado

  Cenário: Data de entrega anterior ao pedido
    Dado que informei uma data de entrega anterior ao início do pedido
    Quando confirmo
    Então vejo a mensagem "* Data de entrega menor que data do pedido *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: Data de emissão inválida
    Dado que informei uma data de emissão que não existe no calendário ou com o ano
      fora de 1994 a 2099
    Quando confirmo
    Então vejo a mensagem "* Data de emissao invalida *"
    E o cursor volta ao campo da data de emissão
    E nada é gravado

  Cenário: Data de emissão anterior demais ao pedido
    Dado que informei uma data de emissão mais de 20 dias anterior ao início do
      pedido
    Quando confirmo
    Então vejo a mensagem "* Data da emissao invalida *"
    E nada é gravado

  Cenário: Data de emissão posterior à data de entrega
    Dado que informei a data de emissão depois da data de entrega
    Quando confirmo
    Então vejo a mensagem "* Data de emissao > data da entrega *"
    E o cursor volta ao campo da data de emissão
    E nada é gravado

  Cenário: Número do pedido não informado
    Dado que deixei o número do pedido em branco
    Quando confirmo
    Então vejo a mensagem "* Informe o numero do pedido *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: Pedido não cadastrado
    Dado que informei um pedido que não existe para o meu órgão e o meu grupo
    Quando confirmo
    Então vejo a mensagem "* Pedido nao cadastrado *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: Pedido excluído
    Dado que o pedido informado está excluído
    Quando confirmo
    Então vejo a mensagem "* Pedido excluido *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: Pedido sem operador logístico
    Dado que o pedido informado não tem operador logístico
    Quando confirmo
    Então vejo a mensagem "* Pedido nao e de oper.logistico *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: Pedido aprovado e fechado
    Dado que o pedido informado está aprovado e fechado
    Quando confirmo
    Então vejo a mensagem "* Pedido aprovado - fechado *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: Pedido pendente de distribuição
    Dado que o pedido informado está pendente de distribuição
    Quando confirmo
    Então vejo a mensagem "* Pedido pendente de distribuicao *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: Pedido pendente de aprovação
    Dado que o pedido informado está pendente de aprovação
    Quando confirmo
    Então vejo a mensagem "* Pedido pendente de aprovacao *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: Órgão que não pertence ao grupo
    Dado que o órgão do pedido não pertence ao grupo informado
    Quando confirmo
    Então vejo a mensagem "* Orgao nao pertence a este grupo *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: Contrato que não é de operação logística
    Dado que o contrato do tipo do item do pedido não é de operação logística
    Quando confirmo
    Então vejo a mensagem "* Contrato nao e de Oper.Logistico *"
    E o cursor volta ao campo do pedido
    E nada é gravado

  Cenário: Nota fiscal já cadastrada
    Dado que já existe nota cadastrada com o mesmo órgão, operador, número e ano
    Quando tento incluir
    Então vejo a mensagem "* Nota ja cadastrada. Use ALT. *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Nota fiscal com entrega confirmada
    Dado que a nota informada tem entrega confirmada
    Quando tento incluir, alterar ou excluir
    Então vejo a mensagem "* Nota fiscal com entrega confirmada *"
    E nada é gravado

  Cenário: Nota fiscal de outro grupo
    Dado que a nota cadastrada pertence a outro grupo
    Quando tento incluir, alterar, excluir ou consultar
    Então vejo a mensagem "* Usuario sem acesso ao grupo desta nota *"
    E nada é gravado

  Cenário: Alteração de uma nota fiscal
    Dado que informei o número da nota, o ano da entrega e o operador logístico de
      uma nota cadastrada
    E troquei o modelo, a chave de acesso ou a data de emissão
    Quando confirmo a alteração com "S"
    Então o sistema regrava o que foi trocado
    E deixa um registro de auditoria de cada gravação
    E sou encaminhado à tela dos gêneros da nota, em alteração

  Cenário: Número da nota não informado na alteração, na exclusão ou na consulta
    Dado que escolhi alterar, excluir ou consultar sem informar o número da nota
    Quando confirmo
    Então vejo a mensagem "* Informe o numero da nota fiscal *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: Ano da entrega não informado na alteração, na exclusão ou na consulta
    Dado que escolhi alterar, excluir ou consultar sem informar o ano da entrega
    Quando confirmo
    Então vejo a mensagem "* Informe o ano de entrega da nota *"
    E o cursor volta ao campo do ano da entrega
    E nada é gravado

  Cenário: Operador logístico não informado na alteração, na exclusão ou na consulta
    Dado que escolhi alterar, excluir ou consultar sem informar o operador logístico
    Quando confirmo
    Então vejo a mensagem "* Informe o codigo do oper.logistico *"
    E o cursor volta ao campo do operador logístico
    E nada é gravado

  Cenário: Alteração, exclusão ou consulta de nota não cadastrada
    Dado que informei número, ano e operador de uma nota que não está cadastrada
    Quando confirmo
    Então vejo a mensagem "* Nota fiscal nao cadastrada *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: Exclusão de uma nota fiscal
    Dado que informei a identificação de uma nota cadastrada, sem entrega confirmada
    Quando confirmo a exclusão com "S"
    Então o sistema percorre os gêneros da nota e estorna a quantidade de cada um no
      saldo do contrato e no item do pedido
    E devolve o pedido fechado à situação de recebimento
    E apaga cada gênero, com registro de auditoria
    E apaga a nota fiscal
    E não me encaminha a outra tela

  Cenário: A consulta não grava nada
    Dado que informei a identificação de uma nota cadastrada e escolhi consultar
    Quando confirmo
    Então a tela traz o cabeçalho da nota e os nomes dos cadastros
    E sou encaminhado à tela dos gêneros, em consulta
    E nada é gravado, alterado ou apagado, e nenhum registro de auditoria é gerado

  Cenário: Operação desconhecida é recusada
    Dado que informei no campo da operação um valor que não é incluir, alterar,
      excluir nem consultar
    Quando confirmo
    Então vejo a mensagem "* Operacao nao disponivel *"
    E nada é processado

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não autoriza esta operação nesta tela
    Quando confirmo
    Então o sistema abandona a operação com a mensagem de acesso negado
    E nada é gravado

  Cenário: Campo não numérico é recusado antes de processar
    Dado que digitei letras em um dos campos numéricos da nota
    Quando confirmo
    Então o campo é marcado e o cursor volta para ele
    E nada é processado
```
