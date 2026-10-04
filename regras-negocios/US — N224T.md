# US — N224T — Confirmar a devolução de gênero da nota fiscal

## Estória

Como **servidor de CRE**, quero **confirmar a devolução de um gênero da nota fiscal
que o informe anterior deixou preparado**, para que **a quantidade devolvida saia do
que a nota fiscal e o contrato do fornecedor contavam, e o estoque e o pendente do
pedido fiquem certos**.

Nenhuma devolução vale enquanto não é confirmada: é esta tela que transforma o que
foi informado em movimento no sistema — o gênero passa a constar da devolução, o
item correspondente da nota fiscal é reduzido ou excluído, o total da nota e o
índice do contrato são refeitos e rateados, os saldos do contrato e do pedido são
acertados e cada alteração fica registrada para auditoria. Sem essa confirmação, o
informe anterior não passa de uma tela preenchida — e o que voltou continuaria
contando como entrega recebida.

## Contexto

Jornada S000M → N000M → N050M → N210M → N214T → N224T.

Ator: servidor de CRE — confere o item da devolução que o informe anterior levantou
e confirma a execução.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os passos N000M, N050M e N210M são menus: encaminham e não decidem nada do que esta
tela faz. O contexto que esta tela usa — o perfil de acesso, a secretaria, a
coordenadoria regional de ensino e o órgão do servidor — vem da entrada, e está
documentado lá.

Esta é a última tela da jornada e é a que **executa** a devolução. O passo anterior,
o informe da devolução (`N214T`), é uma tela de transação que **encadeia** nesta,
sem passar por menu: ele levanta o item, faz as primeiras conferências e passa o
registro e a operação adiante. Quem conclui a inclusão é esta tela, que confirma,
grava e, ao fim, devolve o controle ao informe — já marcando a operação como
alteração — para o próximo gênero.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela só é montada vindo do informe da devolução

A tela não abre pelo menu nem por acesso direto: para ela ser montada, a sessão
precisa trazer a marca de que o servidor veio do informe da devolução (`N214T`), que
registra essa marca antes de passar o controle. Fora desse caminho, o sistema não
monta a tela, avisa **\* Acesse esta tela pela N214T \*** e devolve o servidor ao que
ele estava fazendo. Antes disso, o sistema confere se o perfil do servidor tem acesso
à tela; sem a permissão, a tela também não é montada.

### RN-02 — A tela só faz inclusão

Das operações do sistema, esta tela aceita uma só: a inclusão do item na devolução.
Qualquer outra é recusada com **\* Opcao nao disponivel. Use INC, ALT ou EXC \***, o
cursor volta ao campo da opção e nada é gravado. No caminho desta jornada, o informe
anterior passa o controle já marcando a operação como inclusão.

### RN-03 — A tela traz o item que o informe levantou e pede a confirmação do item

Ao ser montada, a tela mostra o que o informe da devolução deixou na sessão — são
**29 dados**: a operação já marcada como inclusão, o número e a data da devolução, o
número e a data da nota fiscal, o código e a razão social do fornecedor, a
coordenadoria regional de ensino, o número do pedido e o ano da entrega, o tipo de
contrato, o órgão filho e o seu nome, o código da subclasse e o do gênero com a
descrição resumida, o preço unitário do item, a quantidade daquele gênero na nota e
o seu valor total, a quantidade e o valor a devolver e o que sobra depois da
devolução. A descrição do tipo de órgão do servidor e a data do sistema completam o
cabeçalho. Com isso, a tela pede a confirmação do item, com a mensagem
**\* Confirma inclusao do item da devolucao <S/N> ? \*** e o cursor no campo de
resposta. Nada foi gravado até aqui.

### RN-04 — O gênero não pode já constar da devolução

Antes de aceitar o item, o sistema verifica se aquele gênero já consta da devolução,
procurando pelo órgão, pelo número da nota fiscal, pelo número da devolução, pela
subclasse e pelo gênero. Consta: recusa com **\* Genero ja cadastrado na devolucao
\***, o cursor volta à quantidade e nada é gravado — o item não é duplicado.

### RN-05 — O gênero tem de constar da nota fiscal

O gênero devolvido tem de existir na nota fiscal informada, procurado pelo órgão,
pelo fornecedor, pelo número e pelo ano da nota, pela subclasse e pelo gênero. Não
existindo, o sistema recusa com **\* Genero nao cadastrado na nota fiscal \***, o
cursor volta à quantidade e nada é gravado.

### RN-06 — A quantidade devolvida é obrigatória e limitada à da nota

A quantidade a devolver tem de ser informada: em branco ou zero, o sistema recusa
com **\* Informe quantidade de devolucao \***. E ela não pode passar da quantidade
daquele gênero na nota fiscal: passando, recusa com **\* <- Quantidade > que a da
nota \***, e a mensagem mostra a quantidade da nota. Nos dois casos o cursor volta à
quantidade e nada é gravado.

### RN-07 — O valor da devolução é calculado; quando é parcial, admite 2 centavos

Há dois desfechos. Quando a quantidade devolvida é a quantidade inteira daquele item
na nota, o valor é o valor total do item e é o sistema que o determina — o valor
informado é descartado. Quando a devolução é parcial, o valor é conferido contra o
preço unitário multiplicado pela quantidade devolvida: abaixo disso, o sistema
recusa com **\* <- Valor < que o calculado para a quant \***; acima disso mais 2
centavos, recusa com **\* <- Valor > que o calculado para a quant \***. Nos dois
casos o cursor volta ao valor e nada é gravado. Valor em branco (zero) é preenchido
pelo próprio cálculo e segue aceito.

[?] Na conferência do valor, o programa ajusta 2 centavos em um valor que ele só zera
na inicialização e que ninguém lê depois: o ajuste não altera o limite aplicado, e a
tolerância acaba sendo sempre de 2 centavos para mais. Se o ajuste devia recair sobre
o valor informado — tirando a tolerância quando a devolução é do item inteiro — ou
sobre o total do item, o fonte não diz. Pergunta ao site.

### RN-08 — Passadas as conferências, a tela pede a confirmação da devolução

Se a resposta à confirmação do item não for afirmativa, o sistema refaz as
conferências do gênero, da quantidade e do valor e, passando todas, apresenta a
segunda pergunta — **\* Confirma inclusao da devolucao <S/N> ? \*** — com os números
já acertados (o que foi devolvido e o que sobra). Responder que sim à primeira
pergunta também leva à gravação, e nesse caso as conferências de quantidade e de
valor não são refeitas, porque os números vêm do informe anterior, que já as tinha
feito. Enquanto a resposta não for afirmativa, nada é gravado.

[?] A tela reage a um único valor em um campo de situação: quando ele vem preenchido
com a letra S, a operação é abandonada e o controle volta ao informe, sem gravar. O
programa não diz o que esse campo significa, e o acervo não traz o rótulo dele na
máscara. Se é um comando de saída que o servidor digita ou um campo que a tela não
deixa preencher, não se sabe. Pergunta ao site.

### RN-09 — A confirmação grava tudo o que depende da devolução, numa operação só

Confirmada a devolução, a tela executa o item e acerta, na mesma passada, tudo o que
depende dele: inclui o gênero devolvido na devolução do fornecedor, com a subclasse,
o gênero, a quantidade e os valores; ajusta o item correspondente da nota fiscal;
refaz o total e cria ou atualiza o documento da devolução; refaz o total da nota
fiscal e reaplica o índice do contrato, rateando-o por item; acerta os saldos do
contrato; e acerta o estoque e o pendente do pedido. São **seis cadastros de negócio
tocados numa única confirmação**, dos quais dois — o contrato e o estoque — dependem
de o cadastro existir para aquele gênero e aquele pedido. Cada uma dessas gravações
leva junto o seu registro de auditoria, e nenhuma delas pede confirmação de novo.

[?] Não há, no programa, desfazer das gravações já feitas quando uma etapa posterior
não conclui: o sistema apenas para e devolve o controle, e o que já foi gravado
permanece. Se a transação do ambiente desfaz o conjunto, o acervo não diz. Pergunta
ao site.

### RN-10 — O item da nota fiscal é reduzido ou excluído

Quando a quantidade devolvida é a quantidade inteira daquele item na nota, o item é
excluído da nota fiscal. Quando é parcial, o item permanece, com a quantidade e o
valor reduzidos na mesma medida. É assim que a nota deixa de contar o que foi
devolvido.

### RN-11 — O documento da devolução é criado ou atualizado

A cada item, o sistema soma de novo tudo o que aquela devolução tem e grava esse
total no documento da devolução, identificado pelo órgão, pelo número da devolução e
pelo número da nota fiscal: se o documento ainda não existe, é criado com os dados do
item; se existe, o total é atualizado. Quando a soma do que a devolução tem fica em
zero e o documento existe, o documento é excluído — mas esta tela só inclui, e
inclusão some, nunca subtrai: o total só chega a zero aqui quando o item incluído não
tem valor nenhum.

### RN-12 — O total da nota é refeito e o índice do contrato é rateado por item

Depois de ajustar o item, o sistema soma de novo os itens da nota fiscal e grava o
novo total na nota. Sobre esse total aplica o índice cadastrado no contrato do
fornecedor (dividido por cem) e distribui o resultado entre os itens da nota,
proporcionalmente ao valor de cada um e com arredondamento; como a soma dos rateios
não fecha exatamente com o total calculado, a diferença é lançada no item de maior
valor retido. Se o total recalculado for igual ao que a nota já tinha, a nota não é
regravada e o rateio não é refeito. Se o índice for zero, a nota é regravada com o
total e sem rateio.

[?] O que o índice significa no negócio — se é retenção, desconto ou outra coisa — o
acervo não diz: o cadastro do contrato o exibe com o próprio nome do campo, e não há
mensagem que o explique nesta jornada. O programa o usa como percentual do total da
nota. Pergunta ao site.

### RN-13 — Os saldos do contrato só são acertados se a nota não for anterior ao contrato

O contrato procurado é o do órgão, tipo de contrato, fornecedor, coordenadoria
regional de ensino, subclasse e gênero, com a data-limite igual à data de emissão da
nota fiscal; não existindo, não há o que acertar. Existindo, os saldos do contrato —
a quantidade e o valor temporariamente comprometidos e a quantidade do pedido — são
reduzidos pela devolução, mas só quando a data de emissão da nota não é anterior à
data de início do contrato daquele gênero. Antes disso, a devolução é registrada do
mesmo jeito (o item, a nota, o documento da devolução, o estoque e a auditoria); o
contrato fica como está.

[?] O acervo não define em palavras o que são os saldos temporariamente comprometidos
do contrato, nem por que a devolução os reduz e ainda reduz a quantidade do pedido.
Pergunta ao site.

### RN-14 — O estoque e o pendente do pedido são acertados quando o cadastro existe

A devolução soma a quantidade devolvida ao saldo em estoque do gênero e subtrai a
mesma quantidade do saldo a receber do pedido, no cadastro procurado pelo órgão, pela
coordenadoria regional de ensino, pelo número do pedido com o ano da entrega, pela
subclasse e pelo gênero. Se esse cadastro não existir para o gênero e o pedido, o
sistema segue sem acertá-lo: a devolução é gravada assim mesmo, o estoque fica como
estava e nenhum aviso é mostrado ao servidor.

[?] O acervo nomeia esses dois saldos apenas pelos nomes dos campos (saldo de estoque
e saldo a receber), sem defini-los em palavras, e o programa aumenta um e reduz o
outro pela mesma quantidade, sem conferir se o saldo a receber comporta a redução.
Qual é o efeito pretendido no negócio e o que deve acontecer quando a devolução é
maior que o saldo pendente, o corpus não diz. Pergunta ao site.

### RN-15 — Cada alteração é registrada para auditoria, e o controle volta ao informe

Antes de gravar cada alteração, o sistema monta o registro de auditoria com a
operação (inclusão, alteração ou exclusão), o cadastro alterado, a tela de origem, o
órgão, o número do processo, a matrícula do servidor, o terminal, a data e a hora da
sessão e a imagem do registro antes e depois da alteração — para o item da devolução,
para o item da nota fiscal, para o documento da devolução, para os saldos do
contrato, para o estoque e para o total da nota. O rateio do índice nos itens da
nota, porém, não passa pela auditoria: os itens têm o valor retido regravado sem
registro. Concluída a passagem, a tela devolve o controle ao informe da devolução, já
marcando a operação como alteração e com o gênero processado, para o próximo item.

---

## Cenários BDD

```gherkin
Funcionalidade: Confirmar a devolução de gênero da nota fiscal

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N224T

  Cenário: A tela não abre fora do caminho do informe da devolução
    Dado que chego à N224T sem a marca do informe da devolução
    Quando a tela é chamada
    Então o sistema não monta a tela
    E vejo a mensagem "* Acesse esta tela pela N214T *"
    E sou devolvido à tela em que estava

  Cenário: Operação diferente da inclusão é recusada
    Dado que o informe da devolução me passou o controle
    Quando informo uma operação diferente da inclusão e confirmo
    Então vejo a mensagem "* Opcao nao disponivel. Use INC, ALT ou EXC *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: O item informado aparece na tela para confirmação
    Dado que informei no N214T um gênero, uma quantidade devolvida e um valor
    Quando a N224T é montada
    Então vejo o número e a data da devolução, o número e a data da nota fiscal,
      o fornecedor e a sua razão social, a coordenadoria regional de ensino, o
      pedido e o ano da entrega, o tipo de contrato, o órgão filho, a subclasse e
      o gênero com a sua descrição, o preço unitário, a quantidade e o valor do
      item na nota, a quantidade e o valor a devolver e o que sobra
    E vejo a mensagem "* Confirma inclusao do item da devolucao <S/N> ? *"
    E nada foi gravado ainda

  Cenário: Gênero já incluído naquela devolução
    Dado que o gênero informado já consta daquela devolução
    Quando confirmo o item
    Então vejo a mensagem "* Genero ja cadastrado na devolucao *"
    E o cursor volta à quantidade
    E nada é gravado

  Cenário: Gênero que não está na nota fiscal
    Dado que o gênero informado não consta da nota fiscal escolhida
    Quando confirmo o item
    Então vejo a mensagem "* Genero nao cadastrado na nota fiscal *"
    E o cursor volta à quantidade
    E nada é gravado

  Cenário: Quantidade de devolução não informada
    Dado que estou na N224T com o item informado
    Quando deixo a quantidade devolvida em branco e confirmo o item
    Então vejo a mensagem "* Informe quantidade de devolucao *"
    E o cursor volta à quantidade
    E nada é gravado

  Cenário: Quantidade maior que a da nota fiscal
    Dado que estou na N224T com o item informado
    Quando informo uma quantidade devolvida maior que a daquele gênero na nota
    Então vejo a mensagem "* <- Quantidade > que a da nota *"
    E a mensagem mostra a quantidade da nota
    E o cursor volta à quantidade
    E nada é gravado

  Cenário: Valor devolvido menor que o calculado
    Dado que estou na N224T com uma devolução parcial
    Quando informo um valor menor que o preço unitário vezes a quantidade
    Então vejo a mensagem "* <- Valor < que o calculado para a quant *"
    E o cursor volta ao valor
    E nada é gravado

  Cenário: Valor devolvido acima do calculado com a tolerância
    Dado que estou na N224T com uma devolução parcial
    Quando informo um valor maior que o cálculo com os 2 centavos de tolerância
    Então vejo a mensagem "* <- Valor > que o calculado para a quant *"
    E o cursor volta ao valor
    E nada é gravado

  Cenário: Devolução da quantidade inteira do item
    Dado que a quantidade devolvida é a quantidade inteira daquele gênero na nota
    Quando confirmo a devolução
    Então o valor da devolução é o valor total do item na nota
    E o item é excluído da nota fiscal

  Cenário: Segunda confirmação da devolução
    Dado que respondi que não à confirmação do item
    Quando o item passa nas conferências de gênero, quantidade e valor
    Então vejo a segunda pergunta "* Confirma inclusao da devolucao <S/N> ? *"
    E os números devolvidos e o que sobra aparecem já acertados
    E nada foi gravado ainda

  Cenário: Resposta não afirmativa não grava nada
    Dado que estou na N224T com o item conferido
    Quando respondo que não à confirmação da devolução
    Então a tela volta a pedir a confirmação da devolução
    E nada é gravado

  Cenário: Confirmação da devolução grava o item e acerta o que depende dele
    Dado que estou na N224T com um item conferido
    Quando respondo que sim à confirmação
    Então o gênero passa a constar da devolução do fornecedor
    E o item da nota fiscal fica reduzido pela quantidade devolvida
    E o total do documento da devolução é refeito
    E o total da nota fiscal é refeito e o índice do contrato é rateado entre os
      itens da nota
    E os saldos do contrato são reduzidos
    E o saldo em estoque sobe e o saldo a receber do pedido cai
    E cada alteração fica registrada na auditoria
    E volto ao informe da devolução para o próximo gênero

  Cenário: Nota anterior ao início do contrato
    Dado que a data de emissão da nota é anterior ao início do contrato daquele
      gênero
    Quando confirmo a devolução
    Então o item, a nota, o documento da devolução, o estoque e a auditoria são
      gravados
    E os saldos do contrato ficam como estavam

  Cenário: Sem cadastro de estoque e pedido para o gênero e o pedido
    Dado que não existe cadastro de estoque e pedido para aquele gênero naquele
      pedido
    Quando confirmo a devolução
    Então a devolução é gravada
    E o saldo em estoque e o saldo a receber do pedido ficam como estavam
    E nenhum aviso sobre isso é mostrado
```
