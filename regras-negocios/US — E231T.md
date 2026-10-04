# US — E231T — Ajuste do pedido acumulado calculado

## Estória

Como **servidor de CRE**, quero **ajustar, gênero a gênero, a quantidade do pedido de
alimentação escolar acumulado calculado da minha coordenadoria regional escolar, excluir o
gênero que não deve mais constar e abrir o gênero que eu quiser conferir**, para que **o
total que a secretaria se compromete a comprar fique coerente com o que os órgãos da
coordenadoria vão receber, dentro do que a permissão de fornecimento do contrato permite**.

O pedido acumulado calculado é a soma, por gênero e por fornecedor, dos pedidos dos vários
órgãos de uma coordenadoria regional escolar — e é dele que sai a quantidade que a
secretaria se compromete a comprar. É esta tela que mostra os gêneros desse acumulado com o
que foi pedido, o que já chegou e o que ainda falta receber, confere cada ajuste contra a
permissão de fornecimento do contrato e mantém o pedido auxiliar que acompanha cada gênero.
Sem ela o total do acumulado ficaria sem quem o ajustasse e sem quem o conferisse: nada
falharia, mas o pedido sairia acima ou abaixo do que a permissão do contrato permite — e o
que os órgãos da coordenadoria vão receber deixaria de bater com o que a secretaria
comprou.

## Contexto

Jornada S000M → E000M → E010M → E040T → E231T.
Ator: servidor de CRE — confere o pedido acumulado calculado que a tela anterior abriu,
ajusta a quantidade de cada gênero, exclui o gênero que não deve mais constar e abre o
gênero que quer conferir.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Esta tela não se alcança por menu. Quem a abre é a tela do pedido (`E040T`): quando o
pedido que o servidor marcou na grade é o acumulado calculado, ela chama esta tela e leva
junto a operação de consultar e a identificação do pedido. A tela do pedido do ano
(`E230T`) também a abre, do mesmo modo e também em consulta, quando o servidor consulta um
pedido que já existe. Da sessão esta tela usa a matrícula, o código de acesso, o
privilégio, a estação, a secretaria (o tipo de órgão), a coordenadoria regional escolar e o
órgão filho do vínculo, além da descrição da secretaria e da data do sistema. E ela não
termina em si mesma: abre a tela do gênero — a `E232T` —, e o que entrega a essa tela é
regra desta estória.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela abre no acumulado que a tela anterior entregou, e a operação vem com ele

Esta tela não procura pedido ao abrir. Ela recebe pronta a identificação do acumulado — o
órgão filho, a coordenadoria regional escolar, o número do pedido e o ano da entrega — e,
com ela, repõe o cabeçalho: a data do sistema, a descrição da secretaria, o órgão com a sua
descrição, o fornecedor com a razão social, o operador com o nome, o período de entrega, o
código do cardápio, o tipo de contrato e a situação do pedido. Só depois disso ela monta a
lista dos gêneros daquele acumulado.

A operação também vem com a chamada: a tela assume a operação que a tela anterior deixou.
Quando não vem operação nenhuma, ela abre em **consulta** — e é assim que ela abre nas duas
origens desta jornada.

[?] A situação do pedido que o cabeçalho mostra **não** é lida do cadastro do pedido: ela
vem da área de trabalho da sessão. Pelo caminho desta jornada, quem abre esta tela não
escreve ali a situação do pedido — o que ela deixa nessa posição é outra coisa —, de modo
que um acumulado fechado pode aparecer no cabeçalho como **Aprovado**. A situação gravada
só é conferida quando o servidor confirma a alteração, e aí a recusa é
**\* Pedido fechado \*** (RN-10). Se a tela que chama deveria entregar a situação, o acervo
lido não mostra. Pergunta ao site.

### RN-02 — A tela só altera e consulta

O campo da operação aceita duas coisas: **alterar** e **consultar**. Qualquer outra —
inclusive o campo em branco — é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta ao campo da operação,
antes de qualquer leitura de pedido. A recusa não mostra nem grava nada além da mensagem.

[?] A mensagem manda usar "ALT" ou "CON", e a tela compara o campo com dois códigos internos
de três letras — os mesmos que ela e as telas vizinhas escrevem no campo. Quem traduziria o
que o servidor digita nesses códigos não está no acervo lido. Pergunta ao site.

### RN-03 — A tela não age quando a chamada já pede a tela seguinte ou já vem marcada por uma recusa

Quando a chamada traz preenchido o campo em que a tela anterior pede a tela seguinte, esta
tela não processa a passagem do servidor: ela não lê o pedido, não grava e não apaga nada,
qualquer que seja o conteúdo daquele campo.

A tela também marca a passagem quando recusa uma linha, e essa marca interrompe a
conferência das linhas seguintes da mesma passagem: a primeira recusa vale para as demais,
que não chegam a ser tratadas.

[?] Nenhuma tela do caminho desta jornada preenche o campo da tela seguinte antes de chamar
esta; se algum caminho do acervo o preenche, a tela fica inerte, e o acervo lido não mostra
quem o preencheria. Pergunta ao site.

### RN-04 — Os campos numéricos passam por edição antes das conferências

**Dezesseis** campos da tela são tratados como número antes de qualquer conferência de
negócio: o órgão filho, a coordenadoria regional escolar, o número do pedido, o ano da
entrega, o código do fornecedor, o tipo de contrato, o operador, o dia, o mês e o ano do
início do período, o dia, o mês e o ano do limite, o código da subclasse, o código do gênero
e a quantidade a ser pedida. O campo em branco é tratado como zero e o que não for número é
recusado ali mesmo, antes das conferências de pedido. A operação, o campo da tela seguinte e
a coluna de ação da linha **não** passam por essa edição.

A tela devolve o cursor a **quatro** desses dezesseis campos — o órgão filho, o número do
pedido, o ano da entrega e a quantidade —, e também ao campo da operação e à coluna de ação
da linha, que não são numéricos. A coordenadoria regional escolar, o código do fornecedor, o
tipo de contrato, o operador, as três partes do início, as três do limite e os códigos de
subclasse e de gênero ficam sem posição de erro: quando a edição os recusa, o cursor não vai
até eles.

[?] A rotina que faz a edição é externa ao programa, e o acervo lido só declara o seu nome,
não o corpo. Não se conclui do acervo se a edição interrompe o processamento ou apenas
corrige o valor e segue. Pergunta ao site.

### RN-05 — A lista mostra, dez por vez, os gêneros do acumulado

A lista tem **dez linhas**, e cada linha traz a subclasse, o gênero, a descrição do gênero,
a quantidade pedida no acumulado, a quantidade recebida, a quantidade a receber — o que
sobra da quantidade pedida depois de descontada a recebida — e a coluna de ação da linha. A
tela percorre os gêneros do pedido acumulado e mostra os que lá estão; um gênero que não
esteja no acumulado não aparece.

Quando o acumulado não tem nenhum gênero, a recusa é
**\* Pedido sem generos cadastrados \***, e a lista não é montada.

### RN-06 — O pedido tem de ser um acumulado calculado que exista no cadastro

O número do pedido e o ano da entrega juntos formam os dez dígitos que identificam o
pedido. Para consultar, o servidor informa o órgão filho, o número e o ano; e a tela recusa,
sem gravar nem apagar nada:

- **\* Informe o numero do pedido \*** — quando o número (com o ano) não foi informado, com
  o cursor no campo do pedido;
- **\* Pedido nao cadastrado \*** — quando o pedido não existe para a coordenadoria regional
  escolar que a tela está usando, com o cursor no campo do pedido;
- **\* Pedido nao acumulado \*** — quando o pedido existe mas não é um acumulado;
- **\* Pedido acumulado digitado \*** — quando o pedido é o acumulado digitado, que é o de
  outra tela deste sistema;
- **\* Pedido auxiliar do acumulado calculado \*** — quando o pedido é o auxiliar calculado
  de outro acumulado.

Passando por isso, o cabeçalho é reposto com o órgão do pedido, o fornecedor e a razão
social, o operador e o nome, o período, o código do cardápio e o tipo de contrato que estão
no pedido encontrado.

[?] O indicador de acumulação tem quatro valores no acervo: o campo em branco, um valor que
identifica o acumulado **digitado**, um que identifica o acumulado **calculado** e um que
identifica o **auxiliar do calculado**. Esta tela recusa o campo em branco, o acumulado
digitado e o auxiliar do calculado; trata o acumulado calculado — que é o que a tela do
pedido manda para cá. O que separa, no negócio, o acumulado digitado do calculado, o acervo
lido não diz. Pergunta ao site.

### RN-07 — O órgão filho tem de existir, ser da secretaria e estar no alcance do servidor

O órgão filho informado é procurado no cadastro de órgãos — os órgãos marcados como
excluídos são pulados — e a tela recusa, com o cursor de volta ao campo do órgão e sem
gravar nem apagar nada:

- **\* Informe o orgao \*** — quando o órgão não foi informado;
- **\* Orgao nao cadastrado \*** — quando o código não existe no cadastro de órgãos;
- **\* Orgao nao pertence a esta secretaria \*** — quando o tipo de órgão do cadastro não é
  o da secretaria da sessão;
- **\* Usuario sem acesso ao grupo deste orgao \*** — quando o vínculo do servidor traz uma
  coordenadoria regional escolar e o órgão é de outra.

Estas são as conferências da **consulta**, que é a operação com que esta tela se abre nesta
jornada. Na alteração a tela não as repete: ela exige apenas que o órgão e o pedido
continuem sendo os que a tela anterior entregou (RN-09).

### RN-08 — O pedido de outro órgão é recusado

Quando o vínculo do servidor traz um órgão filho e o pedido encontrado é de outro órgão, a
recusa é **\* Pedido de outro orgao \***, com o cursor de volta ao campo do órgão, e nada é
gravado nem apagado.

### RN-09 — Alterar exige o mesmo órgão e o mesmo pedido que a tela anterior entregou

Na alteração, o órgão filho e o pedido que estão na tela têm de ser os mesmos que a tela
anterior entregou; mudando um deles, a recusa é **\* Consulte antes de atualizar \***, com o
cursor de volta ao campo da operação — o servidor tem de reabrir o pedido pela tela do
pedido antes de alterá-lo.

Nesse caminho a tela deixa de repetir as conferências da consulta: ela confia no pedido que
a tela anterior entregou e confere só o que o servidor está mudando.

### RN-10 — O pedido fechado não se altera

Quando a situação gravada do pedido é **Fechado**, a tela recusa a alteração com
**\* Pedido fechado \***, com o cursor de volta ao campo da operação, e não grava nem apaga
nada. A consulta de um acumulado fechado, ao contrário, é permitida: é só a alteração que a
tela recusa.

### RN-11 — O gênero fechado no pedido não se altera nem se exclui

Quando o gênero marcado está fechado no acumulado, a recusa é
**\* Item fechado neste pedido \***, com o cursor de volta à coluna de ação da linha marcada
— tanto na alteração quanto na exclusão —, e nada é gravado nem apagado.

### RN-12 — A quantidade nova é conferida

Na alteração, a quantidade a ser pedida da linha passa por quatro conferências, todas com o
cursor de volta à quantidade da linha e sem gravar nada:

- **\* Informe quantidade a ser pedida \*** — quando ela não foi informada;
- **\* Informe nova quantidade a ser pedida \*** — quando ela é igual à que o gênero já tem
  no acumulado;
- **\* Quantidade deve ser < 100000 \*** — quando ela alcança 100.000;
- **\* Quant. fracionada invalida para este genero \*** — quando ela não é um múltiplo exato
  da fração em que o gênero é fornecido.

### RN-13 — A quantidade nova não pode ser menor que a recebida

A quantidade nova não pode ficar abaixo da quantidade já recebida daquele gênero no
acumulado; ficando, a recusa é **\* Quantidade pedida < quantidade recebida \***, com o
cursor de volta à quantidade da linha, e nada é gravado.

### RN-14 — A permissão de fornecimento limita o aumento

Quando a quantidade nova é **maior** que a que o gênero já tinha no acumulado, a tela
procura a permissão de fornecimento cadastrada para o conjunto (secretaria, tipo de
contrato, fornecedor, coordenadoria regional escolar, subclasse e gênero) cujo período cubra
o do pedido. A recusa é **\* Permiss nao cadastrada ou fora do intervalo \*** quando a
permissão não existe, quando o período do pedido começa antes do período permitido ou quando
o limite do pedido passa do limite permitido.

Na primeira recusa o cursor volta à coluna de ação da linha marcada; na segunda, à
quantidade dela.

Achada a permissão, a tela soma os **três** saldos iniciais que ela registra e confere o que
a permissão passa a ter pedido: o que ela já tem pedido, menos a quantidade antiga do
gênero, mais a quantidade nova. Passando dos saldos somados, a recusa é
**\* Quantidade insuficiente na permissao \***. Nas duas recusas nada é gravado.

Quando a quantidade nova é menor que a antiga, nenhuma dessas conferências é feita: a tela
apenas devolve o saldo.

### RN-15 — O que a alteração grava

Passando as conferências, a alteração do gênero marcado, no acumulado:

- regrava o gênero no acumulado com a quantidade nova e com a situação em aberto — fechado,
  quando a quantidade nova alcança o que já foi recebido daquele gênero;
- baixa a quantidade nova no saldo da permissão de fornecimento do contrato, devolvendo a
  quantidade antiga;
- recalcula o pedido auxiliar que acompanha o gênero: ele passa a valer a diferença que
  resta, e é **apagado** quando essa diferença chega a zero;
- ao terminar a passagem, repõe a situação do pedido acumulado: **Fechado** quando todos os
  gêneros do acumulado estão fechados, e aberto em qualquer outro caso.

Cada regravação e cada apagamento deixa um registro de auditoria com a operação, a
secretaria, a coordenadoria, o órgão, o operador, a data e a hora da sessão e o conteúdo
anterior e o posterior do registro.

[?] O que o pedido auxiliar representa no negócio, e qual das quantidades entra na diferença
que a tela repõe nele, o acervo lido não permite concluir: a soma percorre os itens do
acumulado e deixa um deles de fora, e nada no acervo diz o que esse item é. Pergunta ao
site.

### RN-16 — A exclusão recusa o gênero com recebimento e apaga os pedidos daquele gênero

A exclusão do gênero marcado recusa, com o cursor de volta à coluna de ação da linha e sem
apagar nada:

- **\* Item fechado neste pedido \*** — quando o gênero está fechado no acumulado (RN-11);
- **\* Ja existe quantidade recebida \*** — quando já há quantidade recebida daquele
  gênero.

Passando, a exclusão apaga do cadastro os pedidos que aquele gênero tem no acumulado e os
itens correspondentes, devolve ao saldo da permissão de fornecimento a quantidade do
acumulado daquele gênero, apaga o item do próprio acumulado e registra cada apagamento na
auditoria — o registro leva a operação, o órgão, a coordenadoria, o operador, a data e a
hora e o conteúdo apagado.

[?] A conferência da quantidade recebida olha só o item do próprio acumulado, e o apagamento
percorre os itens daquele gênero no acumulado — inclusive os dos pedidos dos órgãos, que não
passaram por essa conferência. Se um pedido de órgão com quantidade recebida deveria barrar
a exclusão, o acervo lido não diz. Pergunta ao site.

[?] O caminho de exclusão apaga **um** item por passagem, e o acervo lido não permite dizer
quantos e quais registros caem quando o gênero tem mais de um item no acumulado. Pergunta ao
site.

### RN-17 — Consultar o gênero abre a tela do gênero em consulta

Marcada a linha com a consulta, a tela entrega à tela do gênero — a `E232T` — o pedido e o
gênero marcados (a subclasse e o gênero) com a operação de **consultar**, e a abre. A tela
do gênero abre em consulta e não deixa gravar: é esta tela que decide isso, não um campo da
tela nova.

[?] O que a tela seguinte recebe, campo a campo, não se conclui daqui: a identificação que
esta tela monta só coincide com o que a tela do gênero declara esperar até a subclasse e o
gênero; da quantidade da linha em diante o conteúdo cai em posições que a tela seguinte lê
como número e ano do pedido auxiliar e como o começo da própria grade. O que se conclui é a
operação, a subclasse e o gênero. Pergunta ao site.

### RN-18 — A passagem de consulta não grava nada

Abrir a tela, percorrer a lista, repor o cabeçalho e abrir um gênero na tela seguinte: nada
disso inclui, altera ou apaga cadastro nenhum, e nada disso gera registro de auditoria. As
gravações desta tela existem só nos caminhos de **alteração** e de **exclusão** de um
gênero (RN-15 e RN-16).

### RN-19 — Sem autorização para a tela ou para a operação, nada acontece

Na abertura a tela confere que a estação é a mesma em que a sessão foi aberta — não sendo, o
acesso é encerrado —, que a tela está registrada para o código de acesso do servidor (senão
**\* Tela nao disponivel \***) e que o código de acesso alcança a tela (senão
**\* Acesso negado para esta matricula \***). Na passagem do servidor ela confere, antes de
ler pedido, que a tela continua registrada e não excluída (senão
**\* Tela nao cadastrada \***) e que a operação que está executando é liberada para aquele
código de acesso naquela tela (senão **\* Acesso negado para esta operacao \***). Nenhuma
dessas conferências grava ou apaga nada.

---

## Cenários BDD

```gherkin
Funcionalidade: Ajuste e conferência do pedido acumulado calculado da coordenadoria regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E231T

  Cenário: RN-01 — abrir a tela no acumulado que a tela anterior entregou
    Dado que abri pela tela E040T o pedido acumulado calculado da minha coordenadoria
    Quando abro a tela E231T
    Então vejo no cabeçalho a data do sistema, a descrição da secretaria, o órgão com a
      descrição, o fornecedor com a razão social, o operador com o nome, o período de
      entrega, o código do cardápio e o tipo de contrato do pedido
    E vejo a lista dos gêneros daquele acumulado
    E nada foi gravado nem apagado por causa da abertura

  Cenário: RN-01 — sem operação deixada, a tela abre em consulta
    Dado que a chamada não deixou operação nenhuma
    Quando abro a tela E231T
    Então a operação da tela é a consulta

  Cenário: RN-02 — operação diferente de alterar e consultar
    Quando informo uma operação que não é alterar nem consultar
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nenhum pedido é lido, gravado ou apagado

  Cenário: RN-03 — a chamada já pede a tela seguinte
    Dado que a chamada traz preenchido o campo da tela seguinte
    Quando confirmo
    Então a tela não lê o pedido
    E nada é gravado nem apagado

  Cenário: RN-03 — a primeira recusa interrompe a conferência das linhas seguintes
    Dado que marco duas linhas e a primeira é recusada por alguma conferência
    Quando confirmo
    Então a segunda linha não é conferida nem tratada
    E nada é gravado nem apagado

  Cenário: RN-04 — a edição numérica dos campos
    Dado que estou na tela E231T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências
    E a digitação que não é número é barrada antes das conferências do pedido

  Cenário: RN-05 — ver a lista dos gêneros do acumulado
    Dado que o acumulado tem gêneros cadastrados
    Quando abro a tela E231T
    Então vejo até dez linhas, cada uma com a subclasse, o gênero, a descrição do
      gênero, a quantidade pedida, a quantidade recebida, a quantidade a receber e a
      coluna de ação

  Cenário: RN-05 — acumulado sem gêneros
    Dado que o acumulado não tem nenhum gênero
    Quando abro a tela E231T
    Então vejo "* Pedido sem generos cadastrados *"
    E a lista não é montada

  Cenário: RN-06 — número do pedido em branco
    Dado que estou na tela E231T em consulta
    Quando confirmo sem informar o número do pedido
    Então vejo "* Informe o numero do pedido *"
    E o cursor fica no campo do pedido
    E nada é gravado

  Cenário: RN-06 — pedido não cadastrado
    Quando informo um número e um ano que não existem para a minha coordenadoria
    Então vejo "* Pedido nao cadastrado *"
    E o cursor fica no campo do pedido
    E nada é gravado

  Cenário: RN-06 — pedido que não é acumulado
    Quando informo um pedido que não está registrado como acumulado
    Então vejo "* Pedido nao acumulado *"
    E nada é gravado

  Cenário: RN-06 — pedido acumulado digitado
    Quando informo um pedido registrado como acumulado digitado
    Então vejo "* Pedido acumulado digitado *"
    E nada é gravado

  Cenário: RN-06 — pedido auxiliar do acumulado calculado
    Quando informo o pedido auxiliar calculado de um acumulado
    Então vejo "* Pedido auxiliar do acumulado calculado *"
    E nada é gravado

  Cenário: RN-07 — órgão em branco
    Quando confirmo sem informar o órgão filho
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: RN-07 — órgão não cadastrado
    Quando informo um órgão filho que não está no cadastro de órgãos
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: RN-07 — órgão de outra secretaria
    Quando informo um órgão cujo tipo de órgão não é o da minha secretaria
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: RN-07 — órgão de outra coordenadoria
    Dado que o meu vínculo carrega uma coordenadoria regional escolar
    Quando informo um órgão de outra coordenadoria
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: RN-08 — pedido de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando abro um pedido que é de outro órgão
    Então vejo "* Pedido de outro orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: RN-09 — alterar sem reabrir o pedido que a tela anterior entregou
    Dado que estou na tela E231T com o acumulado aberto em consulta
    Quando troco o número do pedido e peço a alteração
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: RN-10 — pedido fechado
    Dado que o acumulado informado está fechado
    Quando peço a alteração
    Então vejo "* Pedido fechado *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: RN-11 — gênero fechado no pedido
    Dado que o gênero marcado está fechado no acumulado
    Quando peço a alteração dessa linha
    Então vejo "* Item fechado neste pedido *"
    E o cursor fica na coluna de ação da linha
    E nada é gravado nem apagado

  Cenário: RN-12 — quantidade não informada
    Dado que marco uma linha com a alteração
    Quando deixo a quantidade em branco e confirmo
    Então vejo "* Informe quantidade a ser pedida *"
    E o cursor fica na quantidade da linha
    E nada é gravado

  Cenário: RN-12 — quantidade igual à que o gênero já tem
    Dado que marco uma linha com a alteração
    Quando informo a mesma quantidade que o gênero já tem no acumulado
    Então vejo "* Informe nova quantidade a ser pedida *"
    E o cursor fica na quantidade da linha
    E nada é gravado

  Cenário: RN-12 — quantidade que alcança 100.000
    Dado que marco uma linha com a alteração
    Quando informo uma quantidade de 100.000 ou mais
    Então vejo "* Quantidade deve ser < 100000 *"
    E o cursor fica na quantidade da linha
    E nada é gravado

  Cenário: RN-12 — quantidade fora da fração do gênero
    Dado que marco uma linha com a alteração
    Quando informo uma quantidade que não é múltipla da fração do gênero
    Então vejo "* Quant. fracionada invalida para este genero *"
    E o cursor fica na quantidade da linha
    E nada é gravado

  Cenário: RN-13 — quantidade menor que a recebida
    Dado que o gênero já tem quantidade recebida no acumulado
    Quando informo uma quantidade menor que essa
    Então vejo "* Quantidade pedida < quantidade recebida *"
    E o cursor fica na quantidade da linha
    E nada é gravado

  Cenário: RN-14 — permissão não cadastrada ou fora do intervalo
    Dado que marco uma linha com a alteração e aumento a quantidade
    E que não há permissão de fornecimento que cubra o período do pedido
    Quando confirmo
    Então vejo "* Permiss nao cadastrada ou fora do intervalo *"
    E o cursor fica na coluna de ação da linha
    E nada é gravado

  Cenário: RN-14 — saldo insuficiente na permissão
    Dado que marco uma linha com a alteração e aumento a quantidade
    E que a permissão de fornecimento do contrato não tem saldo para o aumento
    Quando confirmo
    Então vejo "* Quantidade insuficiente na permissao *"
    E o cursor fica na quantidade da linha
    E nada é gravado

  Cenário: RN-15 — alterar a quantidade de um gênero do acumulado
    Dado que marco uma linha com a alteração e informo uma quantidade nova válida
    Quando confirmo
    Então o gênero passa a ter a quantidade nova no acumulado
    E o saldo da permissão de fornecimento do contrato é baixado pela quantidade nova
    E o pedido auxiliar que acompanha o gênero é regravado com o que resta
    E a alteração deixa registro de auditoria
    E a situação do acumulado é reposta conforme os gêneros estejam ou não todos
      fechados

  Cenário: RN-15 — o pedido auxiliar é apagado quando não resta diferença
    Dado que a quantidade nova do gênero faz zerar a diferença que o pedido auxiliar
      representa
    Quando confirmo a alteração
    Então o pedido auxiliar daquele gênero é apagado do cadastro
    E o apagamento deixa registro de auditoria

  Cenário: RN-16 — excluir um gênero que já tem quantidade recebida
    Dado que o gênero marcado já tem quantidade recebida no acumulado
    Quando marco a linha com a exclusão
    Então vejo "* Ja existe quantidade recebida *"
    E o cursor fica na coluna de ação da linha
    E nada é apagado

  Cenário: RN-16 — excluir um gênero do acumulado
    Dado que marco uma linha com a exclusão
    E que não há quantidade recebida daquele gênero
    Quando confirmo
    Então os pedidos daquele gênero no acumulado são apagados do cadastro
    E o saldo da permissão de fornecimento é devolvido pela quantidade do acumulado
    E a exclusão deixa registro de auditoria em cada apagamento

  Cenário: RN-17 — consultar o gênero abre a tela do gênero
    Dado que marco uma linha com a consulta
    Quando confirmo
    Então a tela abre a E232T com o pedido e o gênero marcados
    E a E232T abre em consulta
    E nada foi gravado nem apagado

  Cenário: RN-18 — a consulta não grava nada
    Dado que abri a tela, percorri a lista e não marquei alteração nem exclusão
    Quando a tela termina a passagem
    Então nenhum cadastro foi incluído, alterado ou apagado por isso
    E nenhum registro de auditoria foi gerado

  Cenário: RN-19 — sem autorização para a tela
    Dado que o meu código de acesso não alcança esta tela
    Quando abro a tela E231T
    Então vejo "* Acesso negado para esta matricula *"
    E nada é mostrado nem gravado

  Cenário: RN-19 — sem autorização para a operação
    Dado que a alteração não está liberada para o meu código de acesso nesta tela
    Quando peço a alteração
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado nem apagado
```
