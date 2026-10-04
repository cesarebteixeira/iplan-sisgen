# US — N324T — Manter os gêneros e as quantidades da nota fiscal

## Estória

Como **servidor de CRE**, quero **informar, na nota fiscal que acabei de cadastrar,
quais gêneros ela cobre e em que quantidade**, para que a entrega do fornecedor
fique amarrada ao pedido e ao contrato e o pagamento saia pelo saldo certo.

A nota fiscal, sozinha, não diz o que veio: quem a identifica para a conferência e
para o pagamento são os gêneros e as quantidades que ela traz. É nesta tela que
esse conteúdo é montado — e é ele que consome o saldo do contrato e do item do
pedido. Com a nota cadastrada e sem os gêneros informados, o item do pedido
continua em aberto e a CRE não tem como conferir a entrega do fornecedor.

## Contexto

Jornada S000M → N000M → N050M → N300M → N314T → N324T.

Ator: servidor de CRE — depois de cadastrar o cabeçalho da nota fiscal na N314T,
informa os gêneros que ela cobre e as quantidades de cada um.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e
menus.md`: é **dado de navegação**, não regra de negócio.

A N314T entrega a esta tela o cabeçalho já cadastrado — número da nota fiscal, as
duas datas de emissão, a chave de acesso, o fornecedor, o número do pedido, o ano
da entrega, o tipo de contrato, a coordenadoria regional de ensino, o órgão e o
operador — e a opção de manutenção escolhida. O que esta tela acrescenta são as
linhas de gênero.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela só abre vinda do cadastro da nota fiscal

A tela não se abre pelo menu. Ela só é montada quando a sessão chega marcada com a
tela do cadastro da nota fiscal (N314T); vinda de outra origem, não é montada: o
sistema marca a operação como falha e devolve o servidor ao menu N300M. Quem passa
o controle é a N314T, deixando antes na sessão a marcação de origem e a opção de
manutenção.

[?] A marcação de origem que a N314T deixa é o código `N314T`, e não o da própria
tela que a recebe; a tela irmã, de consulta, usa a mesma marcação. Se `N314T` é o
código da tela de cadastro da nota fiscal ou apenas o rótulo da família da nota,
o acervo não diz. Pergunta ao site.

### RN-02 — O que a tela apresenta

A tela é o detalhe da nota fiscal escolhida. Em cima, o cabeçalho que veio do
cadastro: número da nota, data da nota fiscal (dia, mês e ano), segunda data de
emissão (dia, mês e ano), chave de acesso, código e razão social do fornecedor,
número do pedido, ano da entrega, tipo de contrato, código e nome do operador,
código e nome do órgão, coordenadoria regional de ensino, número e descrição da
nota de modificação, descrição do tipo de órgão e a data do sistema. Embaixo,
**até 8 linhas**, cada uma com o código da subclasse (2 dígitos), o código do
gênero (5), a quantidade (5 inteiros e 3 decimais), a descrição do gênero e a
situação da linha. A descrição é preenchida pelo sistema a partir do cadastro de
gêneros; a coluna da unidade de medida existe na tela e é limpa a cada entrada.

[?] A coluna da unidade de medida nunca é preenchida: nenhuma das leituras que a
tela executa traz a unidade para a linha, embora ela exista no cadastro de
gêneros. A quantidade aparece sem unidade. Pergunta ao site.

[?] O cadastro de gêneros é procurado pela subclasse e pelo gênero, com a data da
nota fiscal carregada como início de vigência, mas a conferência do que volta
compara apenas a subclasse e o gênero. Se a descrição mostrada é a vigente na
data da nota ou a primeira do par subclasse/gênero, não se sabe. Pergunta ao site.

### RN-03 — A situação de cada linha diz o que fazer com ela

Em cada linha, a situação decide a operação: **I** inclui o gênero na nota, **A**
altera a quantidade já registrada e **E** exclui a linha. Linha sem gênero
informado, ou com situação diferente de I, A e E, é ignorada: não gera operação
nenhuma e não produz mensagem.

### RN-04 — A tela trabalha em alteração ou em consulta

A opção de manutenção vem do cadastro da nota. Para a tela ser montada, ela tem de
ser **alteração** ou **consulta**; na confirmação, qualquer outra é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da opção e
nada é processado. Indicando o servidor outra tela no campo de próxima tela, a
confirmação desta tela também é abandonada sem processar as linhas.

[?] A correspondência entre os rótulos da máscara (ALT e CON) e as opções internas
de alteração e de consulta é conclusão tirada do texto da mensagem, não verificada
no fonte.

### RN-05 — Ao entrar, a tela lista os gêneros da nota

A tela percorre os gêneros já registrados na nota e preenche as 8 linhas visíveis,
trazendo do cadastro a descrição de cada gênero. Se a nota não tiver nenhum
gênero, o sistema avisa **\* Nota fiscal sem generos cadastrados \*** e não mostra
linha nenhuma.

[?] Se a nota tem mais de 8 gêneros, não há, no que esta tela executa, contador de
página em uso. O que acontece com os gêneros além do oitavo fica sem resposta.
Pergunta ao site.

### RN-06 — A conferência dos campos

Ao confirmar, o sistema confere **um a um 17 campos** da nota e das linhas,
exigindo que sejam numéricos e que caibam no tamanho de cada um: número da nota
fiscal (9), dia, mês e ano da nota (2, 2 e 4), dia, mês e ano de emissão (2, 2 e
4), coordenadoria regional de ensino (2), número do pedido (6), ano da entrega
(4), tipo de contrato (3), código do fornecedor (4), órgão (8), operador (4),
código da subclasse (2), código do gênero (5) e quantidade do gênero (5 inteiros e
3 decimais). Campo em branco vira zero e os zeros à esquerda são descartados. O
conteúdo recusado é marcado e o cursor volta ao campo — na linha certa, quando o
campo é de uma linha de gênero. Os campos que a tela preenche a partir dos
cadastros — a descrição do gênero, a unidade de medida, a razão social do
fornecedor, os nomes do órgão e do operador, a descrição da nota de modificação, a
descrição do tipo de órgão e a data do sistema — são limpos a cada entrada.

### RN-07 — Inclusão de gênero que já está na nota é recusada

Para incluir, o sistema procura o par subclasse/gênero digitado entre os gêneros
já registrados na nota. Já existindo, a inclusão é recusada com **\* Genero ja
cadastrado nesta nota \*** e nada é gravado.

### RN-08 — Inclusão exige gênero do pedido

O gênero informado tem de constar do pedido da nota: o sistema procura o item do
pedido pelo pedido, pela coordenadoria, pela subclasse e pelo gênero. Não achando,
recusa com **\* Genero nao cadastrado neste pedido \***.

### RN-09 — Inclusão exige permissão de compra no contrato

Além de constar do pedido, o gênero precisa ter permissão de compra: o sistema
procura, no contrato daquele fornecedor com aquela coordenadoria e aquele tipo de
contrato, a linha do gênero cuja data-limite seja exatamente a data da nota fiscal
e que não esteja excluída, e exige que ela comece antes da data da nota. Não
achando, recusa com **\* Genero sem permissao de compra \***.

[?] A procura toma a data-limite do contrato como exatamente o dia, o mês e o ano
da nota fiscal. Um contrato de vigência mais ampla, com outra data-limite, não é
encontrado e a inclusão é recusada. Se é assim mesmo, pergunta ao site.

### RN-10 — A quantidade é obrigatória e não pode passar o saldo do pedido

Na inclusão e na alteração, a quantidade é obrigatória: zero é recusado com
**\* Informe a quantidade \***. A quantidade informada é somada ao que o item do
pedido já tem recebido e ao que está em trânsito; passando do total solicitado no
pedido, a operação é recusada com **\* Quantidade excede a solicitada no pedido \***.
Na inclusão, o item do pedido também não pode estar fechado: estando, a recusa é
**\* Pedido fechado \***.

[?] A conferência do pedido fechado existe no caminho de inclusão e não no de
alteração. Se a alteração de quantidade num item fechado deve ser aceita, pergunta
ao site.

### RN-11 — A quantidade tem de fechar a fração do gênero

O cadastro de gêneros guarda, para cada gênero, uma fração. A quantidade informada
é dividida por essa fração e, se sobrar resto, a operação é recusada com
**\* Quant. fracionada invalida para este genero \***.

[?] O que a fração representa — embalagem, lote, múltiplo de venda — não está no
corpus. Pergunta ao site.

### RN-12 — Alteração exige gênero na nota e quantidade diferente da atual

Para alterar, o par subclasse/gênero tem de estar registrado na nota — não estando,
a recusa é **\* Genero nao cadastrado nesta nota \***. A quantidade nova tem de
ser diferente da que já está registrada: repetindo-a, o sistema recusa com
**\* Informe uma nova quantidade \***. Passando nas duas conferências, a quantidade
é regravada.

### RN-13 — Exclusão exige gênero na nota

Para excluir, o par subclasse/gênero tem de estar registrado na nota; não estando,
a recusa é **\* Genero nao cadastrado nesta nota \***. Na exclusão, a quantidade
informada na linha é a que sai da nota, do contrato e do item do pedido.

### RN-14 — O que cada operação grava

Incluir grava a linha do gênero na nota, soma a quantidade ao saldo do contrato e à
quantidade recebida do item do pedido. Alterar regrava a linha e acerta o contrato
e o item do pedido pela diferença entre a quantidade nova e a antiga. Excluir apaga
a linha da nota e subtrai a quantidade do contrato e do item do pedido. Cada uma
dessas gravações deixa um registro de auditoria com o cadastro tocado, a operação
(inclusão, alteração ou exclusão), o conteúdo anterior e o posterior, a matrícula do
funcionário, a estação, o número do processo (o pedido), a data e a hora da sessão
e o tipo de órgão. Ao mexer na quantidade do item do pedido, a tela também regrava
a situação desse item.

### RN-15 — No fim, o sistema acerta o cabeçalho da nota e a situação do pedido

Processadas as linhas, o sistema reexamina a nota: se sobrou pelo menos um gênero e
o cabeçalho da nota não existe, ele é criado, com a situação de nota nova e a data
de entrada do dia do sistema; se não sobrou nenhum gênero e o cabeçalho existe, ele
é apagado. Em seguida a situação do pedido é reescrita: o sistema percorre os itens
do pedido e deixa na situação do pedido a marca de item aberto se algum item
estiver aberto; não havendo nenhum, fica a situação do último item percorrido.

[?] O critério de "último item percorrido" e o significado das letras de situação
(a de aberto e a de fechado) não estão no dicionário desta base nem em mensagem do
programa. Pergunta ao site.

### RN-16 — A consulta não inclui, altera nem exclui linhas

Em consulta, as linhas informadas não geram operação nenhuma: o sistema não grava,
não altera e não exclui gênero, e nenhuma trilha de auditoria de gênero é gerada.

[?] O fecho da tela não é guardado pela opção. Depois de processar as 8 linhas, o
sistema executa o acerto do cabeçalho da nota e a reescrita da situação do pedido
(RN-15) também em consulta, porque o desvio da consulta salta as operações de linha
mas não alcança o fim da rotina. Ou a consulta de fato regrava o cabeçalho da nota
e o pedido, ou o desvio deveria chegar ao fim da rotina. Não se escolhe um dos dois
lados: pergunta ao site.

### RN-17 — A operação depende da autorização do usuário

Na montagem, o sistema confere a permissão do usuário para a tela; na confirmação,
confere a rota e a autorização da operação, com o contexto da sessão (matrícula,
código de acesso, privilégio, tipo de órgão e coordenadoria). Não estando
autorizado, a tela não é montada ou a operação é abandonada sem gravar.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os gêneros e as quantidades da nota fiscal

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N324T

  Cenário: A tela só abre vinda do cadastro da nota fiscal
    Dado que chego à N324T sem a marcação de origem do cadastro da nota fiscal
    Quando a tela é chamada
    Então o sistema não monta a tela
    E sou devolvido ao menu N300M

  Cenário: A nota e os seus gêneros são apresentados
    Dado que cadastrei o cabeçalho da nota fiscal na N314T
    Quando a tela N324T abre
    Então vejo o número e as datas da nota, a chave, o fornecedor, o pedido, o
      ano da entrega, o contrato, a coordenadoria, o órgão e o operador
    E vejo os gêneros já registrados, com a descrição de cada um, até 8 linhas

  Cenário: Nota fiscal sem gêneros registrados
    Dado que a nota escolhida não tem nenhum gênero registrado
    Quando a tela N324T abre
    Então vejo a mensagem "* Nota fiscal sem generos cadastrados *"
    E nenhuma linha de gênero é mostrada

  Cenário: Inclusão de um gênero na nota
    Dado que o gênero consta do pedido, tem permissão de compra no contrato e a
      quantidade cabe no saldo do pedido
    Quando informo a situação I com a subclasse, o gênero e a quantidade
    Então o sistema grava a linha do gênero na nota
    E soma a quantidade ao saldo do contrato e à quantidade recebida do item do
      pedido
    E registra a operação na auditoria

  Cenário: Inclusão de gênero que já está na nota é recusada
    Dado que a nota já tem aquele par de subclasse e gênero
    Quando tento incluir o gênero
    Então vejo a mensagem "* Genero ja cadastrado nesta nota *"
    E nada é gravado

  Cenário: Inclusão de gênero que não consta do pedido é recusada
    Dado que o gênero não consta do pedido da nota
    Quando tento incluir o gênero
    Então vejo a mensagem "* Genero nao cadastrado neste pedido *"
    E nada é gravado

  Cenário: Inclusão de gênero sem permissão de compra é recusada
    Dado que o gênero não tem linha de contrato com a data-limite da nota
    Quando tento incluir o gênero
    Então vejo a mensagem "* Genero sem permissao de compra *"
    E nada é gravado

  Cenário: Inclusão sem quantidade é recusada
    Dado que estou na N324T em modo de alteração
    Quando informo a situação I com a subclasse e o gênero, sem quantidade
    Então vejo a mensagem "* Informe a quantidade *"
    E o cursor volta ao campo da quantidade

  Cenário: Inclusão acima do saldo do pedido é recusada
    Dado que a quantidade informada faz o item do pedido passar do total
      solicitado
    Quando tento incluir o gênero
    Então vejo a mensagem "* Quantidade excede a solicitada no pedido *"
    E nada é gravado

  Cenário: Inclusão em item de pedido fechado é recusada
    Dado que o item do pedido está fechado
    Quando tento incluir o gênero
    Então vejo a mensagem "* Pedido fechado *"
    E nada é gravado

  Cenário: Quantidade fora da fração do gênero é recusada
    Dado que a quantidade informada não é múltipla da fração do gênero
    Quando tento incluir ou alterar a quantidade
    Então vejo a mensagem "* Quant. fracionada invalida para este genero *"
    E nada é gravado

  Cenário: Alteração da quantidade de um gênero da nota
    Dado que o gênero já está registrado na nota
    E a quantidade nova cabe no saldo do pedido
    Quando informo a situação A com a nova quantidade
    Então o sistema regrava a linha
    E acerta o contrato e o item do pedido pela diferença entre a quantidade
      nova e a antiga
    E registra a operação na auditoria

  Cenário: Alteração de gênero que não está na nota é recusada
    Dado que aquele par de subclasse e gênero não está registrado na nota
    Quando tento alterar
    Então vejo a mensagem "* Genero nao cadastrado nesta nota *"
    E nada é gravado

  Cenário: Alteração repetindo a quantidade atual é recusada
    Dado que o gênero está registrado na nota
    Quando informo a situação A com a mesma quantidade já registrada
    Então vejo a mensagem "* Informe uma nova quantidade *"
    E nada é gravado

  Cenário: Exclusão de um gênero da nota
    Dado que o gênero está registrado na nota
    Quando informo a situação E com a quantidade que sai
    Então o sistema apaga a linha da nota
    E subtrai a quantidade do contrato e do item do pedido
    E registra a operação na auditoria

  Cenário: Exclusão de gênero que não está na nota é recusada
    Dado que aquele par de subclasse e gênero não está registrado na nota
    Quando tento excluir
    Então vejo a mensagem "* Genero nao cadastrado nesta nota *"
    E nada é gravado

  Cenário: A nota fica sem nenhum gênero
    Dado que excluí o último gênero da nota
    Quando a tela fecha as linhas
    Então o cabeçalho da nota é apagado
    E a situação do pedido é reescrita

  Cenário: A situação do pedido é reescrita
    Dado que alterei os gêneros da nota
    Quando a tela fecha as linhas
    Então o sistema percorre os itens do pedido
    E deixa na situação do pedido a marca de item aberto, se algum item estiver
      aberto

  Cenário: Consulta não inclui, não altera e não exclui linhas
    Dado que cheguei à N324T em modo de consulta
    Quando confirmo as linhas
    Então nenhum gênero é incluído, alterado ou excluído
    E nenhuma trilha de auditoria de gênero é gerada

  Cenário: Opção de manutenção indisponível
    Quando informo uma opção de manutenção diferente de ALT e de CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção

  Cenário: Linha sem gênero ou com situação desconhecida é ignorada
    Dado que preenchi uma linha sem o código do gênero, ou com situação diferente
      de I, A e E
    Quando a tela processa as linhas
    Então aquela linha não gera operação nenhuma e não produz mensagem

  Cenário: Campo não numérico é recusado na confirmação
    Dado que digitei letras em um dos campos da nota ou da linha
    Quando confirmo
    Então o campo é marcado e o cursor volta para ele
    E nada é gravado

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não autoriza esta operação
    Quando confirmo as linhas
    Então o sistema abandona a operação com mensagem
    E nada é gravado
```
