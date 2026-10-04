# US — E061T — Renumeração do pedido de requisição

## Estória

Como **servidor de CRE**, quero **trocar o número de um pedido já cadastrado por outro
número, menor e ainda livre na minha coordenadoria**, para que **o pedido fique com um
número válido sem perder nada do que já foi lançado nele**.

O pedido é encontrado pelo número, e é o número que o identifica junto com o ano da entrega
e com a coordenadoria a que pertence. Quando ele sai errado — repetido, fora de sequência
ou trocado com outro —, corrigi-lo refazendo o pedido significaria relançar tudo o que já
estava nele, item por item. Esta rotina existe para essa correção: numa operação só, ela
troca o número no pedido e em todos os itens dele e deixa o rastro da troca para auditoria.
Sem ela, o pedido errado fica como está, ou vira um pedido novo — e o que já estava lançado
se perde.

A rotina faz uma coisa só: renumerar. Ela não inclui, não exclui e não serve para
consultar; a leitura do pedido acontece no caminho da renumeração, e a gravação só acontece
depois de uma confirmação.

## Contexto

Jornada S000M → E000M → E010M → E061T.
Ator: servidor de CRE — informa a sua coordenadoria regional escolar, o pedido atual
(número e ano da entrega) e o número novo, confere o que a tela mostra, confirma e renomeia
o pedido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O menu que abre esta tela não deixa nenhum dado do pedido com ela: quem chega encontra a
tela já na alteração e nenhum pedido carregado. O que a tela usa do caminho — a matrícula, o
privilégio, o tipo de órgão, a coordenadoria regional escolar (o grupo) e a descrição da
secretaria — é o que a entrada deixou na sessão; a tela não recalcula nada disso. E a tela
não encadeia para outra: ao terminar, ela reabre a si mesma.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela tem uma única operação: renumerar o pedido

Esta tela só sabe alterar o número de um pedido. Ao ser aberta, ela já se apresenta com a
operação de alteração preenchida, e qualquer outra operação que o operador digitar é
recusada com a mensagem **\* Opcao nao disponivel. Use ALT \***, com o cursor de volta ao
campo da opção, antes de qualquer leitura de pedido.

[?] O que a mensagem quer dizer com "ALT" — se é uma tecla, se abre outra forma de operar —
não está no acervo lido. E o campo da operação é preenchido pela própria tela: não há fonte
que diga se o operador pode escolher outra operação por ali. Pergunta ao site.

### RN-02 — A tela abre sem buscar pedido

Ao ser aberta, a tela não procura pedido nenhum: ela mostra a data do sistema e a descrição
da secretaria da sessão e fica esperando o grupo e o número. A leitura do pedido só acontece
depois que o operador informa o grupo, o número e o ano da entrega.

[?] A data do sistema e a descrição da secretaria são preenchidas na abertura e limpas a
cada digitação, sem que a tela as reponha; se o ambiente as repõe por fora, o acervo lido
não mostra. Pergunta ao site.

### RN-03 — O pedido é identificado pelo grupo, pelo número e pelo ano da entrega

Dentro de uma coordenadoria regional escolar (o grupo), um pedido é identificado pelo número
(seis dígitos) junto com o ano da entrega (quatro dígitos). O número sozinho não identifica
nada: o mesmo número pode existir em anos de entrega diferentes e em coordenadorias
diferentes. O ano da entrega informado é o que entra nessa identificação.

### RN-04 — Os campos numéricos passam por edição antes das conferências

Treze campos da tela são tratados como número: o grupo, o número do pedido, o ano da
entrega, o número novo, o ano novo, o órgão filho, o fornecedor e as seis partes do período
de entrega. Campo em branco vira zero, e o que não for número é recusado, com o cursor
devolvido ao primeiro campo recusado.

[?] Só quatro desses treze campos têm posição de cursor definida — o grupo, o número do
pedido, o ano da entrega e o número novo. Se a digitação de um dos outros for recusada, o
cursor não é levado até ele. E a rotina que faz a edição não faz parte do acervo lido: o que
o operador vê na recusa não pôde ser determinado. Pergunta ao site.

### RN-05 — O grupo é obrigatório e, para quem tem grupo na sessão, só o da sessão serve

Sem grupo informado, a recusa é **\* Informe o grupo \***, com o cursor no campo do grupo.
Se a sessão do operador já está vinculada a uma coordenadoria regional escolar, o grupo
informado tem de ser essa mesma coordenadoria; sendo outra, a recusa é
**\* Usuario sem acesso a este grupo \***, com o cursor no campo do grupo. Se a sessão não
está vinculada a nenhuma coordenadoria, o grupo informado tem de existir no cadastro de
grupos; não existindo, a recusa é **\* Grupo nao cadastrado \***, com o cursor no campo do
grupo.

[?] Quando a sessão já tem coordenadoria, o grupo informado não é conferido contra o
cadastro de grupos — só contra o da sessão. E, quando a sessão não tem coordenadoria
nenhuma, qualquer grupo cadastrado é aceito: a tela não restringe o operador à sua
coordenadoria porque ele não tem uma. Se a intenção era que todo operador só operasse a
própria coordenadoria, o caminho não garante isso. Pergunta ao site.

### RN-06 — O pedido atual tem de existir no grupo informado

Procurando o pedido pelo grupo, pelo número e pelo ano da entrega informados, se ele não
estiver cadastrado a recusa é **\* Pedido DE - nao cadastrado \***, com o cursor no campo do
número do pedido.

### RN-07 — Um pedido que já recebeu quantidade não pode ser renumerado

Achado o pedido, a tela percorre os itens dele: se algum item tem quantidade já recebida, a
renumeração é recusada com **\* Pedido DE - com quantidade recebida \***, com o cursor no
campo do número do pedido. O pedido só pode ser renumerado enquanto nada dele tiver sido
recebido.

[?] A conferência percorre os itens do pedido a partir da primeira combinação de
classificação e gênero; se essa caminhada não alcançar todos os itens, um pedido já recebido
pode passar pela conferência. O acervo lido não permite afirmar que ela alcança todos.
Pergunta ao site.

### RN-08 — O número novo tem de ser menor que o número atual

O número novo informado tem de ser menor que o número atual do pedido. Igual ou maior, a
recusa é **\* Pedido PARA - deve ser < que Pedido DE \***, com o cursor no campo do número
novo.

### RN-09 — O número novo tem de estar livre no grupo

O número novo não pode estar em uso: se já existe um pedido com o número novo, no mesmo
grupo e no mesmo ano de entrega, a recusa é **\* Pedido PARA - ja cadastrado \***, com o
cursor no campo do número novo. Essa conferência é feita no momento em que os dados são
conferidos, e não se repete na hora de gravar.

### RN-10 — O ano da entrega do pedido renumerado é o mesmo do pedido atual

A renumeração não muda o ano da entrega. O ano que o operador digitar para o pedido novo é
descartado e substituído pelo ano do pedido atual, e é esse que a tela mostra de volta e usa
para identificar o pedido novo: na prática, o campo do ano novo é apenas informativo.

[?] Se a intenção era permitir mudar o ano da entrega junto com o número, o caminho não
permite: o valor digitado é substituído antes de qualquer leitura. Pergunta ao site.

### RN-11 — A tela mostra o pedido e pede confirmação; sem "S" não grava nada

Passando as conferências, a tela lê o pedido e mostra o que ele tem: o órgão filho e o seu
nome, o fornecedor e a razão social, o período de entrega e o cardápio. Em seguida pergunta
**\* Confirma alteracao do numero do pedido <S/N> ? \***, com o cursor no campo da resposta.

Nada é gravado enquanto o operador não responder "S": resposta diferente de "S", inclusive
em branco, apenas devolve a tela. E, se entre a pergunta e a resposta o operador mudar o
grupo ou algum dos números, a confirmação é desfeita — a tela confere tudo de novo e
pergunta outra vez. Informar os dados e ver o pedido, por si só, não grava nada.

[?] A tela marca a pergunta para que a gravação não aconteça na mesma passagem; quem desfaz
essa marca entre uma digitação e outra não está no acervo lido, e sem isso a tela ficaria
presa na pergunta. Pergunta ao site.

### RN-12 — Confirmando, o número novo é gravado no pedido e em todos os itens dele

Respondendo "S", a tela regrava o pedido e todos os itens dele com o número novo, um a um, e
avisa **\* Pedido atualizado \***. O ano da entrega fica como estava. Nenhum registro é
criado e nenhum é apagado: o mesmo pedido e os mesmos itens passam a ter outro número.

[?] Os itens são regravados antes do pedido. Se a gravação do pedido falhar, os itens já
foram renumerados e o pedido fica apontando para um número que não existe; o acervo lido não
diz o que o operador vê nesse caso nem se há desfazimento. Pergunta ao site.

[?] Como a conferência do número novo aconteceu na digitação anterior, um pedido criado por
outra pessoa nesse meio-tempo só é percebido na hora de gravar. O acervo lido não diz o que
a tela mostra então. Pergunta ao site.

[?] Os itens são regravados um a um, e não foi possível determinar, pelo acervo, se essa
caminhada alcança todos os itens do pedido. Se algum ficar de fora, ele continua apontando
para o número antigo. Pergunta ao site.

### RN-13 — Toda renumeração fica registrada na auditoria

Cada renumeração grava registros de auditoria com a tela e o cadastro de origem, a operação,
os valores antes e depois, a matrícula, a estação, o grupo, o número do pedido e a data e a
hora da sessão. É gravado um registro para o pedido e um para cada item renumerado.
Informar os dados, ver o pedido e responder "N" não geram registro.

[?] Além da operação de alteração, cada registro de auditoria leva uma marca de manutenção
fixa, e o pedido em si não tem a sua marca de manutenção atualizada por esta tela. O que
essa marca significa não está no acervo lido. Pergunta ao site.

### RN-14 — Sem autorização para a tela ou para a operação, nada acontece

A tela só abre para o código de acesso que a tem autorizada no cadastro de telas por código
de acesso; não tendo, a recusa é **\* Acesso negado para esta matricula \***, a tela é
abandonada e o servidor volta ao menu principal. E, antes de qualquer leitura de pedido, a
operação de alteração tem de estar liberada para aquele código de acesso naquela tela; não
estando, a recusa é **\* Acesso negado para esta operacao \***, a operação é abandonada e o
servidor volta ao menu principal.

---

## Cenários BDD

```gherkin
Funcionalidade: Renumeração do pedido de requisição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E061T

  Cenário: Tela aberta pelo menu, sem buscar pedido
    Dado que chego à tela pelo menu de requisições
    Então encontro a tela já na operação de alteração
    E nenhum pedido foi lido: a tela espera o grupo, o número e o ano da entrega

  Cenário: Renumerar um pedido que ainda não teve quantidade recebida
    Dado que existe um pedido no meu grupo, sem nenhuma quantidade recebida
    E o número novo é menor que o número atual e não está em uso no meu grupo
    Quando informo o grupo, o número atual, o ano da entrega e o número novo
    Então a tela mostra os dados do pedido e pergunta se confirmo a alteração
    Quando respondo "S"
    Então o pedido e todos os seus itens passam a ter o número novo
    E o ano da entrega continua o mesmo
    E vejo a mensagem "* Pedido atualizado *"

  Cenário: Informar os dados e ver o pedido não grava nada
    Dado que existe um pedido no meu grupo, sem nenhuma quantidade recebida
    Quando informo o grupo, o número atual, o ano da entrega e um número novo válido
    Então vejo os dados do pedido e a pergunta de confirmação
    E nada foi gravado: nem o pedido nem os itens mudaram de número

  Cenário: Desistir na confirmação
    Dado que a tela já me pediu a confirmação
    Quando respondo "N", ou deixo a resposta em branco
    Então a renumeração não acontece
    E nenhum registro de auditoria é gerado

  Cenário: Mudar o grupo ou os números depois da pergunta
    Dado que a tela já me pediu a confirmação
    Quando mudo o grupo ou um dos números e respondo "S"
    Então a tela confere tudo de novo
    E, estando os dados corretos, me pergunta outra vez

  Cenário: Operação fora da alteração
    Quando informo uma opção diferente da alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo da opção

  Cenário: Grupo não informado
    Quando peço a renumeração sem informar o grupo
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo do grupo

  Cenário: Grupo diferente do da minha sessão
    Dado que a minha sessão está vinculada a uma coordenadoria regional escolar
    Quando informo outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo do grupo

  Cenário: Grupo que não existe no cadastro, para quem não tem coordenadoria na sessão
    Dado que a minha sessão não está vinculada a nenhuma coordenadoria regional escolar
    Quando informo um grupo que não existe no cadastro de grupos
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo do grupo

  Cenário: Pedido atual não cadastrado
    Quando peço a renumeração de um pedido que não existe no grupo informado
    Então vejo a mensagem "* Pedido DE - nao cadastrado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido com quantidade recebida
    Dado que o pedido tem pelo menos um item com quantidade recebida
    Quando peço a renumeração
    Então vejo a mensagem "* Pedido DE - com quantidade recebida *"
    E o cursor volta ao campo do número do pedido
    E nada é gravado

  Cenário: Número novo igual ou maior que o atual
    Quando informo um número novo igual ou maior que o número atual
    Então vejo a mensagem "* Pedido PARA - deve ser < que Pedido DE *"
    E o cursor volta ao campo do número novo

  Cenário: Número novo já em uso
    Dado que já existe um pedido com o número novo, no mesmo grupo e no mesmo ano de entrega
    Quando peço a renumeração
    Então vejo a mensagem "* Pedido PARA - ja cadastrado *"
    E o cursor volta ao campo do número novo

  Cenário: Ano da entrega digitado para o pedido novo
    Quando informo um ano de entrega novo diferente do ano do pedido atual
    Então a tela me mostra de volta o ano do pedido atual
    E a renumeração mantém esse ano

  Cenário: Toda renumeração fica na auditoria
    Dado que a renumeração foi confirmada
    Quando o pedido e os seus itens passam a ter o número novo
    Então fica registrado, para o pedido e para cada item, a tela e o cadastro de origem,
      a operação, os valores antes e depois, a matrícula, a estação, o grupo,
      o número do pedido e a data e a hora da sessão

  Cenário: Digitação que não é número
    Quando digito letras em um dos campos numéricos
    Então a digitação é recusada
    E o cursor volta ao campo recusado, quando a tela tem posição definida para ele

  Cenário: Tela não autorizada para o meu código de acesso
    Dado que o meu código de acesso não tem a tela E061T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E volto ao menu principal

  Cenário: Operação não autorizada para o meu código de acesso
    Dado que o meu código de acesso não tem a alteração liberada nessa tela
    Quando tento renumerar o pedido
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é lido nem gravado
```
