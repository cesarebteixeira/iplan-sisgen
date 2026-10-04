# US — N214T — Informar a devolução de gênero da nota fiscal

## Estória

Como **servidor de CRE**, quero **informar a devolução dos gêneros de uma nota fiscal
e mandar de volta ao fornecedor o que veio em desacordo**, para que **o que voltou
deixe de contar na nota fiscal, no contrato do fornecedor e no pedido, sem que os
totais e os saldos tenham de ser acertados à mão**.

A devolução é o outro lado da entrega. Esta tela é onde ela é levantada: o servidor
identifica a devolução e a nota fiscal, confere o que a nota registrou para aquele
fornecedor e marca, gênero por gênero, o que volta e em que quantidade. Sem ela, o
que voltou continuaria contando como entrega recebida — a nota, o contrato e o
pedido seguiriam comprometidos com material que não está mais lá, e a despesa não
fecharia.

A tela não conclui a devolução: quem confirma e grava é a tela seguinte. O que ela
faz é levantar o item, conferi-lo e entregar a sessão à confirmação, e recebê-la de
volta para marcar o próximo gênero.

## Contexto

Jornada S000M → N000M → N050M → N210M → N214T (5 passos).
Ator: servidor de CRE — identifica a devolução e a nota fiscal, confere o que a nota
tem e marca os gêneros que voltam ao fornecedor.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os três passos que antecedem a tela nesta jornada são menus: não gravam nada e não
deixam regra própria. O que a N214T aproveita do caminho é o que a entrada deixou na
sessão — a matrícula do servidor, o órgão, o tipo de órgão e a coordenadoria regional
de ensino (CRE), que é o grupo a que a nota fiscal tem de pertencer.

A tela é uma etapa do encadeamento, não um fim: marcado o gênero, ela entrega a
sessão à tela de confirmação da devolução (`N224T`), que é quem grava; ao voltar, a
tela reabre já em alteração, para o gênero seguinte. Os valores que ela deixa na
sessão são o contrato de passagem entre as duas telas.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela abre em consulta e só aceita consulta e alteração

A operação da tela não é escolha livre. Quando a área de trabalho da sessão não traz
operação nenhuma — como na abertura pela opção do menu desta jornada, que não informa
nenhuma —, a tela abre em **consulta**. Das operações do sistema, a tela aceita duas:
a consulta e a alteração. Qualquer outra é recusada com
**\* Opcao nao disponivel. ALT ou CON \***, o cursor volta ao campo da operação e nada
é gravado. Em alteração, o cursor já vem posicionado na subclasse do gênero da linha
corrente.

O modo vem de quem abriu a tela, não de uma escolha na tela: a consulta que a
antecede (`N214C`) a abre em consulta, e a tela de confirmação a devolve em alteração.
Uma devolução já identificada não se reabre em branco para alterar.

### RN-02 — A consulta começa pela identificação da devolução e da nota fiscal

Para carregar a nota, o servidor informa o número da nota de devolução e o número da
nota fiscal; e a nota fiscal ainda precisa da data de emissão e do código do
fornecedor. Faltando, o sistema recusa, devolve o cursor ao campo e não segue:

| o que falta | o que o servidor vê |
| --- | --- |
| o número da nota de devolução | **\* Informe o numero da nota devolucao \*** |
| o número da nota fiscal | **\* Informe o numero da nota fiscal \*** |
| a data de emissão da nota fiscal (ano em branco) | **\* Informe a data nota fiscal \*** |
| o código do fornecedor | **\* Informe o fornecedor \*** |

Quando a devolução já existe e é encontrada pelo número informado, os dados vêm
dela — a data, o fornecedor, o contrato — e a conferência da nota fiscal fica para o
momento em que a devolução é nova.

[?] Quem cria o número da nota de devolução que o servidor informa. A consulta exige o
número, e o documento da devolução é criado com ele; nenhuma rotina desta jornada o
gera, e a tela de consulta que a antecede também o recebe digitado. Pergunta ao site.

### RN-03 — A nota fiscal tem de existir e ser da coordenadoria do servidor

A nota fiscal é procurada pelo órgão, pelo fornecedor, pelo número e pelo ano da
data de emissão. Não existindo, o sistema recusa com **\* Nota nao cadastrada \*** e
o cursor volta ao número da nota fiscal. Existindo, ela tem de pertencer à mesma
coordenadoria regional de ensino do servidor: sendo de outra, a recusa é
**\* <- Nota cadastrada em outro grupo \***, com o número da coordenadoria na
mensagem e o cursor de volta ao campo.

O mesmo vale para o documento da devolução: achado pelo número e pertencendo a outra
coordenadoria, a recusa é a mesma, com o cursor no número da devolução.

### RN-04 — A nota fiscal não pode estar presa a um processo

A nota fiscal não pode constar de um processo da secretaria. Consta: o sistema recusa
com **\* <- Antes, retire a nota deste processo \***, mostrando o número do processo,
e devolve o cursor ao número da nota fiscal. Enquanto a nota não for retirada do
processo, a devolução não começa.

### RN-05 — O pedido da nota tem de existir e estar fora do acumulado

A tela sobe do item da nota até o pedido e recusa em quatro desfechos:

- a nota não tem nenhum item com pedido — **\* Pedido nao cadastrado \***;
- o pedido não existe no cadastro de pedidos — **\* Pedido nao cadastrado \***;
- o pedido está no acumulado — **\* <- Pedido acumulado \***, com o número do pedido
  na mensagem;
- o item do pedido está cadastrado no acumulado —
  **\* <- Pedido cadastrado no acumulado \***, com o número do pedido acumulado.

Nas quatro, o cursor volta ao número da nota fiscal e nada é gravado. Uma devolução
não é levantada sobre pedido que ainda está no acumulado — o pedido precisa estar
fora dele.

[?] O que é o acumulado, e por que um pedido que está nele não pode ser devolvido. O
programa confere a marca de acumulado no pedido e no item do pedido e recusa; o que a
marca significa no negócio não está no corpus desta jornada. Pergunta ao site.

### RN-06 — As datas da nota e da devolução são conferidas

A data de emissão da nota fiscal e a data da devolução são conferidas contra o
calendário e entre si:

- data que não existe, ou com ano fora da faixa aceita (de 1994 a 2099) —
  **\* Data invalida \***;
- data da devolução posterior ao dia de hoje — **\* Data > que a data atual \***;
- data da devolução anterior à data de emissão da nota fiscal —
  **\* Data devolucao < data da nota \***.

Nas três, o cursor volta à data da devolução e nada é gravado. A data da devolução,
quando muda em relação à que o documento da devolução já tem, é a que o sistema
grava nele.

### RN-07 — Alterar exige ter consultado a mesma devolução

Em alteração, o número da nota de devolução e o número da nota fiscal informados têm
de ser os mesmos que a sessão já tinha da consulta anterior. Sendo outros, o sistema
recusa com **\* Consulte antes de atualizar \***, devolve o cursor ao campo da
operação e não grava: para alterar, o servidor consulta primeiro, e a alteração
trabalha sobre o que foi consultado.

### RN-08 — A tela lista os gêneros já devolvidos e recusa a devolução sem nenhum

Ao ser montada com a devolução identificada, a tela relê os gêneros daquela devolução
e os dispõe na grade, que tem **11 linhas**. Cada linha traz o código da subclasse e o
do gênero com a sua descrição resumida, a quantidade devolvida, o valor devolvido, o
preço unitário do item na nota e o campo de situação, onde o servidor escreve a letra
que diz o que quer fazer com a linha.

Quando a devolução não tem nenhum gênero cadastrado, a tela avisa
**\* Nota devolucao sem generos cadastrados \*** e abandona, sem processar nada.

### RN-09 — Marcar um gênero para devolver: o que a tela confere

Marcada a linha com a letra **I** (inclusão), e havendo subclasse e gênero, o sistema
confere, nesta ordem, e recusa na primeira que falhar — sempre devolvendo o cursor ao
campo da linha e sem gravar:

- o gênero já consta daquela devolução — **\* Genero ja cadastrado na devolucao \***;
- o gênero não consta da nota fiscal — **\* Genero nao cadastrado na nota fiscal \***;
- a quantidade devolvida está em branco ou zerada —
  **\* Informe quantidade de devolucao \***;
- a quantidade devolvida passa da quantidade daquele gênero na nota —
  **\* <- Quantidade > que a da nota \***, com a quantidade da nota na mensagem.

Passando as quatro, o valor a devolver é calculado pelo sistema e não informado: se a
quantidade devolvida é a quantidade inteira daquele gênero na nota, o valor é o valor
total do item; se é parcial, é o preço unitário multiplicado pela quantidade
devolvida.

### RN-10 — Levantado o item, a tela entrega a sessão à confirmação

Passadas as conferências, a tela não grava: ela marca a operação como inclusão, deixa
na sessão o item completo — a subclasse e o gênero com a sua descrição, a quantidade e
o valor a devolver, o preço unitário, a quantidade e o valor daquele gênero na nota —
junto com a identificação da devolução e da nota, e entrega o controle à tela de
confirmação (`N224T`), que é quem grava. A tela também deixa registrado que foi ela a
origem, e é por isso que a confirmação não abre por outro caminho.

Enquanto a confirmação não responde, nada foi gravado.

### RN-11 — Marcar um gênero para excluir: o gênero tem de constar da devolução

Marcada a linha com a letra **E** (exclusão), e havendo subclasse e gênero, o sistema
procura o gênero naquela devolução. Não constando, recusa com
**\* Genero nao cadastrado na devolucao \*** e devolve o cursor ao campo da linha.
Constando, a conferência termina e a exclusão é executada na passagem de gravação.

### RN-12 — A exclusão devolve o item à nota e recompõe o contrato e o pedido

Executada a exclusão de um gênero, o sistema desfaz, na mesma passada, o que a
devolução daquele item tinha feito:

- o item daquele gênero volta à nota fiscal: se ele ainda existe, recebe de volta a
  quantidade e o valor que a devolução tinha tirado; se a devolução o havia esgotado e
  ele foi excluído da nota, o item é recriado com a quantidade e o valor devolvidos;
- o item daquele gênero é excluído da devolução;
- os saldos do contrato do fornecedor voltam a subir — a quantidade e o valor
  temporariamente comprometidos e a quantidade do pedido —, mas só quando a data de
  emissão da nota não é anterior ao início da vigência daquele contrato; antes disso,
  o contrato fica como está;
- o saldo em estoque é reduzido e o saldo a receber do pedido é aumentado na
  quantidade devolvida, quando o cadastro do pedido e estoque daquele gênero existir.

Nada disso é opcional e nada é confirmado de novo: a exclusão é uma operação só, e
cada alteração fica registrada.

[?] O que são, no negócio, os saldos que a exclusão recompõe. O acervo nomeia os do
contrato apenas como a quantidade e o valor temporariamente comprometidos e a
quantidade do pedido, e os do pedido apenas como saldo em estoque e saldo a receber,
sem defini-los em palavras; a exclusão aumenta os do contrato e o saldo a receber e
reduz o saldo em estoque, sem conferir se o saldo a receber comporta o aumento.
Pergunta ao site.

### RN-13 — O documento da devolução é criado, atualizado ou excluído pelo total

Depois de acertado o item, o sistema soma de novo tudo o que a devolução tem e grava
esse total no documento da devolução, identificado pelo órgão, pelo número da
devolução e pelo número da nota fiscal:

- o documento não existe e o total não é zero — é criado com os dados da devolução;
- o documento existe — o total é atualizado;
- o documento existe e o total chegou a zero — o documento é excluído.

Pela tela de confirmação o total só cresce; é pela exclusão de gêneros desta tela que
a devolução pode ficar sem nenhum valor devolvido e o documento ser excluído.

### RN-14 — O total da nota é refeito e o índice do contrato é reaplicado por item

Em seguida o sistema soma de novo os itens da nota fiscal e compara com o total que a
nota registra:

- total igual — a nota não é regravada e o rateio não é refeito;
- total diferente — a nota recebe o novo total; sobre ele o sistema aplica o índice
  cadastrado no contrato daquele tipo de contrato (dividido por cem) e distribui o
  resultado entre os itens da nota, proporcionalmente ao valor de cada um e com
  arredondamento;
- como a soma dos rateios não fecha exatamente com o total calculado, a diferença é
  lançada no item de maior valor retido;
- índice zero — a nota é regravada com o total e sem rateio.

[?] O que o índice do contrato significa no negócio — se é retenção, desconto ou
outra coisa — o acervo não diz: o cadastro do contrato o exibe com o próprio nome do
campo e não há mensagem que o explique nesta jornada. O programa o usa como
percentual do total da nota. Pergunta ao site.

### RN-15 — A consulta não grava nada

Em consulta a tela carrega, mostra a grade e para: nenhum cadastro é gravado, nenhum
item é incluído ou excluído, nenhum total é refeito e nenhum registro de auditoria é
deixado. É o que o servidor usa para conferir a nota antes de alterar.

### RN-16 — Cada alteração fica registrada, e a tela devolve o controle à sessão

Antes de gravar cada alteração, o sistema monta o registro de auditoria com a operação
(inclusão, alteração ou exclusão), o cadastro alterado, a tela de origem, o órgão, o
número do processo, a matrícula do servidor, o terminal, a data e a hora da sessão e a
imagem do registro antes e depois da alteração — para o item da nota fiscal, para o
item da devolução, para o documento da devolução, para os saldos do contrato, para o
estoque e o pedido e para o total da nota fiscal. São **nove pontos de gravação de
auditoria** no programa; numa exclusão completa chegam a ser **seis** numa passagem
só.

Três gravações escapam da auditoria, e todas são valores recalculados: a data da
devolução regravada no documento da devolução e as duas gravações do valor retido dos
itens da nota no rateio do índice.

Terminada a passagem, o sistema devolve a área de trabalho à sessão, e o servidor
segue na própria tela — para marcar o próximo gênero, ou para que a confirmação
conclua o que ficou levantado.

## Cenários BDD

```gherkin
Funcionalidade: Informar a devolução de gênero da nota fiscal

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N214T

  Cenário: Abertura pela opção do menu
    Dado que chego à N214T pela opção do menu, sem operação informada
    Quando a tela é montada
    Então ela abre em consulta
    E nada é gravado

  Cenário: Operação diferente de consulta e de alteração
    Dado que estou na N214T
    Quando informo uma operação que não é consulta nem alteração e confirmo
    Então vejo a mensagem "* Opcao nao disponivel. ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: O modo de alteração vem da confirmação da devolução
    Dado que confirmei um item na tela de confirmação
    Quando a N214T é remontada
    Então ela reabre em alteração
    E o cursor fica na subclasse do gênero da linha corrente

  Cenário: Consulta sem o número da nota de devolução
    Dado que estou na N214T em consulta
    Quando deixo o número da nota de devolução em branco e confirmo
    Então vejo a mensagem "* Informe o numero da nota devolucao *"
    E o cursor volta ao número da nota de devolução
    E nada é gravado

  Cenário: Consulta sem o número da nota fiscal
    Dado que informei o número da nota de devolução
    Quando deixo o número da nota fiscal em branco e confirmo
    Então vejo a mensagem "* Informe o numero da nota fiscal *"
    E o cursor volta ao número da nota fiscal
    E nada é gravado

  Cenário: Consulta sem a data de emissão da nota fiscal
    Dado que informei os números da devolução e da nota fiscal
    Quando deixo o ano da data de emissão da nota fiscal em branco e confirmo
    Então vejo a mensagem "* Informe a data nota fiscal *"
    E o cursor volta à data de emissão da nota fiscal
    E nada é gravado

  Cenário: Consulta sem o fornecedor
    Dado que informei os números e a data de emissão da nota fiscal
    Quando deixo o código do fornecedor em branco e confirmo
    Então vejo a mensagem "* Informe o fornecedor *"
    E o cursor volta ao código do fornecedor
    E nada é gravado

  Cenário: Nota fiscal não cadastrada
    Dado que informei uma nota fiscal que não existe para aquele fornecedor
    Quando confirmo a consulta
    Então vejo a mensagem "* Nota nao cadastrada *"
    E o cursor volta ao número da nota fiscal
    E nada é gravado

  Cenário: Nota fiscal de outra coordenadoria
    Dado que a nota fiscal informada pertence a outra coordenadoria regional de ensino
    Quando confirmo a consulta
    Então vejo a mensagem "* <- Nota cadastrada em outro grupo *"
    E a mensagem mostra o código da coordenadoria da nota
    E o cursor volta ao número da nota fiscal
    E nada é gravado

  Cenário: Documento da devolução de outra coordenadoria
    Dado que a devolução informada já existe e pertence a outra coordenadoria
    Quando confirmo a consulta
    Então vejo a mensagem "* <- Nota cadastrada em outro grupo *"
    E o cursor volta ao número da nota de devolução
    E nada é gravado

  Cenário: Nota fiscal presa a um processo
    Dado que a nota fiscal informada consta de um processo
    Quando confirmo a consulta
    Então vejo a mensagem "* <- Antes, retire a nota deste processo *"
    E a mensagem mostra o número do processo
    E o cursor volta ao número da nota fiscal
    E nada é gravado

  Cenário: Pedido da nota não cadastrado
    Dado que nenhum item da nota fiscal informada tem pedido cadastrado
    Quando confirmo a consulta
    Então vejo a mensagem "* Pedido nao cadastrado *"
    E o cursor volta ao número da nota fiscal
    E nada é gravado

  Cenário: Pedido acumulado
    Dado que o pedido da nota fiscal está no acumulado
    Quando confirmo a consulta
    Então vejo a mensagem "* <- Pedido acumulado *"
    E a mensagem mostra o número do pedido
    E o cursor volta ao número da nota fiscal
    E nada é gravado

  Cenário: Item do pedido cadastrado no acumulado
    Dado que o item do pedido está cadastrado no acumulado
    Quando confirmo a consulta
    Então vejo a mensagem "* <- Pedido cadastrado no acumulado *"
    E o cursor volta ao número da nota fiscal
    E nada é gravado

  Cenário: Data da devolução que não existe
    Dado que informei uma data de devolução que não existe no calendário
    Quando confirmo a consulta
    Então vejo a mensagem "* Data invalida *"
    E o cursor volta à data da devolução
    E nada é gravado

  Cenário: Data da devolução no futuro
    Dado que informei uma data de devolução posterior ao dia de hoje
    Quando confirmo a consulta
    Então vejo a mensagem "* Data > que a data atual *"
    E o cursor volta à data da devolução
    E nada é gravado

  Cenário: Data da devolução anterior à da nota fiscal
    Dado que informei uma data de devolução anterior à data de emissão da nota
    Quando confirmo a consulta
    Então vejo a mensagem "* Data devolucao < data da nota *"
    E o cursor volta à data da devolução
    E nada é gravado

  Cenário: Alteração sem consulta prévia
    Dado que abro a N214T já em alteração, sem ter consultado aquela devolução
    Quando confirmo
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: A consulta carrega a nota e o que já foi devolvido
    Dado que informei a devolução e a nota fiscal de um fornecedor da minha
      coordenadoria
    Quando confirmo a consulta
    Então vejo a coordenadoria regional de ensino, o número do pedido com o ano da
      entrega, o tipo de contrato, o fornecedor com a sua razão social e o órgão filho
    E vejo, na grade de 11 linhas, os gêneros já devolvidos com a sua descrição, a
      quantidade e o valor devolvidos e o preço unitário
    E nada foi gravado

  Cenário: Devolução sem gêneros cadastrados
    Dado que a devolução informada não tem nenhum gênero cadastrado
    Quando a tela é montada
    Então vejo a mensagem "* Nota devolucao sem generos cadastrados *"
    E a tela é abandonada sem processar nada

  Cenário: Inclusão de um gênero na devolução
    Dado que estou na N214T com a nota carregada
    Quando marco uma linha com a letra I, informo a subclasse e o gênero e a
      quantidade devolvida e confirmo
    Então o sistema confere o gênero, a quantidade e o valor calculado
    E me leva à tela de confirmação para concluir a devolução
    E nada foi gravado ainda

  Cenário: Gênero já cadastrado naquela devolução
    Dado que marco com a letra I um gênero que já consta da devolução
    Quando confirmo
    Então vejo a mensagem "* Genero ja cadastrado na devolucao *"
    E o cursor volta ao campo da subclasse da linha
    E nada é gravado

  Cenário: Gênero que não está na nota fiscal
    Dado que marco com a letra I um gênero que não consta da nota fiscal
    Quando confirmo
    Então vejo a mensagem "* Genero nao cadastrado na nota fiscal *"
    E o cursor volta ao campo da subclasse da linha
    E nada é gravado

  Cenário: Quantidade de devolução não informada
    Dado que marco com a letra I um gênero da nota
    Quando deixo a quantidade devolvida em branco e confirmo
    Então vejo a mensagem "* Informe quantidade de devolucao *"
    E o cursor volta ao campo da quantidade devolvida da linha
    E nada é gravado

  Cenário: Quantidade maior que a da nota
    Dado que marco com a letra I um gênero da nota
    Quando informo uma quantidade devolvida maior que a daquele gênero na nota
    Então vejo a mensagem "* <- Quantidade > que a da nota *"
    E a mensagem mostra a quantidade da nota
    E o cursor volta ao campo da quantidade devolvida da linha
    E nada é gravado

  Cenário: Exclusão de um gênero que não está na devolução
    Dado que marco uma linha com a letra E para um gênero que não consta da devolução
    Quando confirmo
    Então vejo a mensagem "* Genero nao cadastrado na devolucao *"
    E o cursor volta ao campo da subclasse da linha
    E nada é gravado

  Cenário: Exclusão de um gênero devolve o item à nota e recompõe o resto
    Dado que a devolução tem um gênero que voltou a ser entregue
    Quando marco essa linha com a letra E e confirmo
    Então o item daquele gênero volta à nota fiscal com a quantidade e o valor
      devolvidos, ou é recriado, se a devolução o havia esgotado
    E o gênero é excluído da devolução
    E os saldos do contrato do fornecedor voltam a subir, quando a nota não é
      anterior ao início da vigência
    E o saldo em estoque cai e o saldo a receber do pedido sobe, quando o cadastro
      existe
    E cada alteração fica registrada na auditoria

  Cenário: A devolução fica sem valor devolvido
    Dado que excluí o último gênero da devolução
    Quando a exclusão é executada
    Então o total devolvido da devolução é refeito e fica em zero
    E o documento da devolução é excluído

  Cenário: O total da nota muda
    Dado que a exclusão mudou o que a nota fiscal soma
    Quando a passagem de gravação termina
    Então o total da nota fiscal é refeito e gravado
    E o índice do contrato é reaplicado sobre o novo total e rateado entre os itens
      da nota
    E a diferença de arredondamento é lançada no item de maior valor retido

  Cenário: A consulta não grava nada
    Dado que estou na N214T em consulta, com a nota carregada
    Quando confirmo a consulta
    Então a tela mostra a nota e os gêneros já devolvidos
    E nenhum cadastro é gravado
    E nenhum total é refeito
    E nenhum registro de auditoria é deixado
```
