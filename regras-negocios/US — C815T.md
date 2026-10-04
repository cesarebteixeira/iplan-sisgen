# US — C815T — Manter as refeições do cardápio

## Estória

Como **servidor de CRE que monta o cardápio do período**, quero **ligar e desligar as
refeições que servem um cardápio já cadastrado, dentro da validade dele, e dizer qual é o
cardápio de sobremesa e em quais semanas do rodízio esse cardápio atende**, para que
**cada refeição do período sirva o cardápio que foi cadastrado para ela, e o planejamento
da alimentação escolar encontre o cardápio onde ele de fato está**.

Um cardápio cadastrado sozinho não serve nada: é a ligação dele com a refeição que diz que
aquele cardápio vale para aquela refeição, naquela validade. As telas do planejamento não
aceitam, para uma refeição, um cardápio que não esteja ligado a ela — recusam dizendo que
o cardápio não está cadastrado naquela refeição —, e é por isso que esta tela existe: sem
ela, o que se cadastra no cardápio não chega ao planejamento. Do outro lado, desfazer uma
ligação que já está no planejamento derruba o que estava montado; por isso a tela recusa a
retirada enquanto o cardápio estiver no planejamento daquela refeição.

## Contexto

Jornada S000M → C000M → C800M → C811M → C815T.

Ator: servidor de CRE — monta, na validade de um cardápio, quais refeições o servem, qual
é o cardápio de sobremesa do período e em quais semanas do rodízio ele atende.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os três menus do caminho (o `C000M`, o `C800M` e o
`C811M`) não gravam nada e só encaminham; o `C811M` esvazia a área de trabalho da sessão
antes de encaminhar, e é por isso que esta tela abre em branco na consulta (§RN-11).

O que esta tela usa do que veio antes é o **contexto da sessão** — o tipo de órgão, a
matrícula, o código de acesso, o privilégio, a coordenação regional, a estação e a data do
sistema —, que é regra da entrada e está no anexo de evidências, em **Regras que se
revelaram da entrada**.

Esta tela **encadeia** na manutenção do cardápio, a `C810T`, quando a marca de novo
cardápio está posta (§RN-12): é a única saída dela para outra tela, e não há menu no
meio.

## Regras de negócio

### RN-01 — O que a tela mantém: as refeições do cardápio, a sobremesa e as semanas

Para um **cardápio já cadastrado** dentro da validade dele, esta tela mantém **quais
refeições o servem** — a ligação do cardápio com a refeição, uma a uma —, **qual é o
cardápio de sobremesa daquela validade** e **em quais semanas do rodízio** aquele cardápio
atende. A ligação guarda o órgão, o cardápio, o início e o limite da validade e a
refeição; a sobremesa e as marcas de semana ficam no próprio cardápio daquela validade.

A tela enxerga **sete** cadastros. **Quatro** ela só lê: o título das telas (2.000
registros de capacidade), o cadastro das refeições (1.200), o planejamento semanal da
refeição por dia da semana (200.000) e o planejamento mensal da refeição (100.000). Em
**três** ela grava: o cardápio da validade (100.000), a ligação do cardápio com as
refeições (100.000) e a auditoria (60.000.000). Os números são de **dimensionamento** — o
máximo esperado que o dicionário de dados declara, não o volume cadastrado.

O tipo de órgão não se digita: é o da sessão, e ele entra na identificação de tudo o que a
tela lê e grava.

### RN-02 — A consulta não grava nada

Em **consulta**, a tela apenas mostra: o código e a descrição do cardápio, o código e a
descrição do cardápio de sobremesa daquela validade, o início e o limite da validade, a
situação do período, as quatro marcas de semana e a lista das refeições que já servem
aquele cardápio naquela validade, com a descrição de cada uma. Não grava, não trava
registro e não deixa rastro na auditoria.

### RN-03 — A tela só trabalha em alterar e consultar

A tela reconhece **duas** operações no campo da operação: **alterar** e **consultar**.
Qualquer outra coisa informada nesse campo é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta ao campo, e nada é
lido nem gravado.

[?] A recusa manda usar ALT ou CON e o que a tela compara são os códigos internos das
duas operações — a alteração e a consulta —; é a mesma dúvida já registrada nas outras
telas desta jornada. Ou o terminal traduz o que o servidor digita antes de enviar, ou
quem seguir a mensagem é recusado. Pergunta ao site.

### RN-04 — A identificação: o código do cardápio e a data limite da validade

O cardápio é identificado pelo **código** e pela **data limite da validade** — dia, mês e
ano. Não havendo cardápio com aquele código naquela validade, a consulta é recusada com
**\* Cardapio nao cadastrado neste periodo \***, com o cursor no código do cardápio, e o
que se alterou na tela é descartado. Existindo, a tela traz do cadastro a descrição do
cardápio e a data de início da validade.

A data de início é exibida e passa pela conferência de número como as outras, mas **não
entra na identificação**: quem identifica são o código e a data limite.

Um cardápio que existe naquela validade e não tem nenhuma refeição ligada avisa
**\* Cardapio sem refeicoes cadastradas \*** e não monta linha nenhuma na lista.

### RN-05 — Alterar exige ter consultado antes

A alteração só passa com o **mesmo código de cardápio e a mesma data limite** que a
consulta deixou guardados na sessão. Divergindo, a recusa é
**\* Consulte antes de alterar \***, com o cursor de volta ao campo da operação, e nada é
lido nem gravado. A consulta não exige nada disso: é ela que deixa o cardápio guardado
para a alteração.

### RN-06 — A lista tem dez linhas, uma por refeição, e cada linha pede uma ação

A lista de refeições é uma página de **dez** linhas. Cada linha traz o código da refeição,
a descrição dela e o campo onde o servidor escreve o que fazer naquela linha: **I** para
ligar o cardápio àquela refeição, **E** para desligar. Linha deixada em branco não é
tocada. Outra coisa escrita na linha é recusada com **\* Informe I=INC ou E=EXC \***, com
o cursor na ação da linha. Uma ação escrita numa linha **sem refeição** é recusada com
**\* Atualize linha preenchida \***, com o cursor na ação da linha.

### RN-07 — Ligar uma refeição ao cardápio

Para ligar, duas conferências: o cardápio **não pode** já estar ligado àquela refeição
naquela validade — estando, a recusa é **\* Cardapio ja cadastrado nesta refeicao \***,
com o cursor no código da refeição da linha —, e a **refeição tem de estar cadastrada e
não pode estar excluída** — não estando, a recusa é **\* Refeicao nao cadastrada \***, no
mesmo cursor. Passando, a ligação é criada com o órgão, o cardápio, o início e o limite da
validade e a refeição.

### RN-08 — Desligar uma refeição do cardápio

Para desligar, duas conferências: a ligação **tem de existir** — não existindo, a recusa é
**\* Cardapio nao cadastrado nesta refeicao \***, com o cursor no código da refeição da
linha —, e o cardápio **não pode estar no planejamento daquela refeição** — estando,
qualquer que seja o dia da semana daquela validade, no planejamento semanal ou no
planejamento mensal, a recusa é **\* Cardapio no planejamento desta refeicao \***, com o
cursor na ação da linha. Passando, a ligação é apagada.

### RN-09 — O cardápio de sobremesa da validade

O servidor pode informar o **cardápio de sobremesa** daquela validade. Informando, três
conferências: o cardápio que está sendo alterado **não pode ser ele mesmo um cardápio de
sobremesa** — sendo, a recusa é **\* Cardapio cadastrado como sobremesa \***, com o cursor
no código do cardápio de sobremesa —; o cardápio informado **tem de existir naquela
validade** — não existindo, **\* Cardapio nao cadastrado neste periodo \***, no mesmo
cursor —; e ele **tem de estar marcado como cardápio de sobremesa** — não estando,
**\* Cardapio nao cadastrado como sobremesa \***, no mesmo cursor. Passando, o código
informado é gravado no cardápio daquela validade e a descrição do cardápio de sobremesa
passa a aparecer na tela.

### RN-10 — As quatro marcas de semana do rodízio

Fora da lista, o cardápio da validade tem **quatro marcas**, uma por semana do rodízio.
Marca deixada em branco significa que o cardápio não atende aquela semana do rodízio;
marca preenchida com qualquer coisa vira **S** e passa a significar que atende. Antes de
gravar, para **cada** marca que ficar posta, a tela procura aquele cardápio no
planejamento semanal daquela semana do rodízio, naquela validade: achando, a alteração
inteira é recusada com **\* Cardapio no planejamento desta semana \***, com o cursor na
marca recusada, e nada é gravado.

[?] A conferência roda também quando a marca não mudou: um cardápio que já está no
planejamento da semana não pode ser alterado — nem só para trocar o cardápio de sobremesa
— enquanto a marca daquela semana continuar posta; só apagando a marca a alteração passa,
e aí o cardápio sai daquela semana do rodízio. Se a intenção era só impedir a retirada, o
caminho faz mais do que isso. Pergunta ao site.

### RN-11 — A abertura depende de quem chamou a tela

A operação da tela não é escolhida por quem a abre: ela vem da área de trabalho da sessão,
e quem a preenche é a tela anterior.

- Aberta **pelo menu**, a área chega em branco — o menu a esvazia antes de encaminhar —, e
  a tela abre em **consulta**, com o cardápio e as datas em branco e sem ler cadastro
  nenhum.
- Aberta **pela manutenção do cardápio** (`C810T`), a área chega com a operação de
  **alteração** e com o cardápio, a validade e as marcas daquele cardápio, e a tela abre
  em **alteração** com esse cardápio carregado e a lista das refeições sendo montada desde
  o começo.
- Aberta **pelo planejamento semanal** (`C820T`), a área chega com a operação de
  **consulta** e sem cardápio, e a tela abre em consulta, com tudo em branco.

A validade vem com a situação do período: estando **fechado** para estimativa, a tela
mostra **FECHADO** no lugar da estimativa; não estando, mostra um traço.

[?] A vida da área de trabalho comum não vem do acervo: o menu desta jornada a esvazia
escrevendo nela um campo de seis caracteres, e a troca entre a área que o programa usa e a
área comum é do ambiente. Se o ambiente a limpa a cada transação, o material não diz.
Pergunta ao site.

### RN-12 — A tela entrega o cardápio à manutenção

Quando a **marca de novo cardápio** está posta, esta tela não faz manutenção: ela confere
que o cardápio existe naquela validade — não existindo, recusa com
**\* Cardapio nao cadastrado \*** e o cursor no código do cardápio — e entrega a transação
à manutenção do cardápio (`C810T`) com o código e a descrição do cardápio, o segmento, o
início e o limite da validade, as marcas de sobremesa e fruta, a situação do período e o
código do cardápio de sobremesa. A operação que ela entrega é a de **consulta**, e é assim
que a manutenção do cardápio abre por causa da entrega.

[?] A marca de novo cardápio é um campo de um caractere que esta tela só escreve como
**N**, na montagem da listagem, e nunca como **S**, e nenhum rótulo da ficha da tela
corresponde a ele. Quem a preenche com **S** — o formulário, um comando, ou outra tela —
o material não diz. Pergunta ao site.

### RN-13 — O período fechado barra a alteração

Alterando, o cardápio daquela validade tem de estar com o período **aberto**: estando
fechado para estimativa, a alteração é recusada com
**\* Cadastro fechado para este periodo \***, com o cursor no dia limite, e nada é
gravado. A consulta a um período fechado é permitida.

### RN-14 — Toda mudança deixa rastro na auditoria

Cada gravação é acompanhada de um registro de auditoria: a alteração do cardápio da
validade, a criação da ligação com a refeição e o apagamento dela. O registro leva o
órgão, o **cadastro que mudou** — o cardápio da validade ou a ligação com a refeição —, a
imagem do registro antes e a depois, a operação, a matrícula, o código de acesso, a
estação, a data e a hora, o número do processo e o código da tela que provocou a mudança.
A consulta não deixa registro.

### RN-15 — O acesso, a rota e a permissão são conferidos antes de qualquer leitura

Na abertura, o sistema confere a permissão de segurança do perfil para esta tela; a cada
mensagem do servidor ele confere o contexto da sessão e a rota; e, antes de ligar ou
desligar uma refeição, confere de novo a permissão, agora para a operação que a linha
pediu. Sem isso, a tela não lê nada e não grava nada.

[?] O texto das recusas de acesso não está no material: as conferências são rotinas de
biblioteca, sem corpo no lote, e o texto sai da tabela de mensagens do sistema, que também
não está no lote. Pergunta ao site.

### RN-16 — O que se digita é conferido antes de qualquer leitura

Nenhum dos campos com rótulo é texto livre. Passam pela edição numérica, antes de qualquer
leitura de cadastro — em branco valendo zero —, **nove** campos: o código do cardápio, as
três partes do início da validade, as três partes do limite da validade, o código do
cardápio de sobremesa e o código da refeição da linha. O que não for número é recusado no
próprio campo, com o cursor de volta a ele. Não passam por essa edição: o campo da
operação, a ação da linha, as quatro marcas de semana e a marca de novo cardápio.

[?] O texto dessa recusa não está no material: a edição é uma rotina de biblioteca, cujo
corpo não faz parte do lote, e o texto sai da tabela de mensagens do idioma, que também
não está no lote. Pergunta ao site.

### RN-17 — Falha no banco interrompe a operação e avisa

Erro de leitura vira a ação 53 e erro de gravação a ação 55, despachadas pela rotina comum
de comunicação; cada gravação é seguida do teste de aborto, que interrompe a transação
antes de seguir para a gravação seguinte.

## Cenários BDD

```gherkin
Funcionalidade: As refeições que servem cada cardápio, o cardápio de sobremesa e as semanas do rodízio

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C815T

  Cenário: RN-01 — o que a tela grava e o que ela só lê
    Dado que altero o cardápio de uma validade, ligo uma refeição a ele e desligo outra
    Quando confirmo cada operação
    Então só o cardápio da validade, a ligação do cardápio com as refeições e a auditoria recebem gravação
    E o título das telas, o cadastro das refeições e os dois planejamentos não são alterados

  Cenário: RN-02 — consultar o cardápio de uma validade
    Dado que informo o código de um cardápio e a data limite da validade dele
    Quando confirmo a consulta
    Então vejo o cardápio, a sua descrição, o cardápio de sobremesa, o início e o limite da validade
    E vejo a lista das refeições que já servem aquele cardápio naquela validade
    E nada é gravado e nenhum registro de auditoria é deixado

  Cenário: RN-03 — operação que a tela não reconhece
    Quando informo no campo da operação uma operação que não é alterar nem consultar
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: RN-04 — cardápio que não existe naquela validade
    Dado que informo o código de um cardápio que não existe naquela data limite
    Quando confirmo a consulta
    Então vejo "* Cardapio nao cadastrado neste periodo *"
    E o cursor volta ao campo do código do cardápio
    E nada é gravado

  Cenário: RN-04 — cardápio sem refeições ligadas
    Dado que o cardápio existe naquela validade e não tem nenhuma refeição ligada
    Quando a tela é apresentada
    Então vejo "* Cardapio sem refeicoes cadastradas *"
    E nenhuma linha da lista é montada

  Cenário: RN-05 — alterar sem ter consultado
    Dado que o cardápio e a data limite em tela não são os que a consulta deixou guardados
    Quando confirmo a alteração
    Então vejo "* Consulte antes de alterar *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: RN-06 — linha com ação que a tela não reconhece
    Dado que consultei o cardápio e escrevi numa linha uma ação que não é I nem E
    Quando confirmo
    Então vejo "* Informe I=INC ou E=EXC *"
    E o cursor volta à ação daquela linha
    E nada é gravado nela

  Cenário: RN-06 — ação numa linha sem refeição
    Dado que consultei o cardápio e escrevi uma ação numa linha que está sem refeição
    Quando confirmo
    Então vejo "* Atualize linha preenchida *"
    E o cursor volta à ação daquela linha
    E nada é gravado nela

  Cenário: RN-06 — linha sem ação
    Dado que consultei o cardápio e deixei a ação de todas as linhas em branco
    Quando confirmo
    Então nenhuma ligação é criada nem apagada
    E nada é gravado naquelas linhas

  Cenário: RN-07 — ligar uma refeição ao cardápio
    Dado que consultei o cardápio
    E a refeição informada existe, não está excluída e ainda não está ligada a ele
    Quando marco a linha com I e confirmo
    Então a ligação daquela refeição com o cardápio daquela validade passa a existir
    E a operação fica registrada na auditoria

  Cenário: RN-07 — refeição que já está ligada ao cardápio
    Dado que a refeição informada já está ligada àquele cardápio naquela validade
    Quando marco a linha com I e confirmo
    Então vejo "* Cardapio ja cadastrado nesta refeicao *"
    E o cursor volta ao código da refeição da linha
    E nada é gravado

  Cenário: RN-07 — refeição não cadastrada
    Dado que a refeição informada não existe no cadastro das refeições, ou está excluída
    Quando marco a linha com I e confirmo
    Então vejo "* Refeicao nao cadastrada *"
    E o cursor volta ao código da refeição da linha
    E nada é gravado

  Cenário: RN-08 — desligar uma refeição do cardápio
    Dado que consultei o cardápio e a refeição está ligada a ele
    E o cardápio não está no planejamento daquela refeição
    Quando marco a linha com E e confirmo
    Então a ligação daquela refeição com aquele cardápio deixa de existir
    E a operação fica registrada na auditoria

  Cenário: RN-08 — ligação que não existe
    Dado que a refeição informada não está ligada àquele cardápio naquela validade
    Quando marco a linha com E e confirmo
    Então vejo "* Cardapio nao cadastrado nesta refeicao *"
    E o cursor volta ao código da refeição da linha
    E nada é apagado

  Cenário: RN-08 — cardápio que está no planejamento da refeição
    Dado que consultei o cardápio e ele está no planejamento semanal ou no mensal daquela refeição
    Quando marco a linha com E e confirmo
    Então vejo "* Cardapio no planejamento desta refeicao *"
    E o cursor volta à ação da linha
    E a ligação continua existindo

  Cenário: RN-09 — gravar o cardápio de sobremesa da validade
    Dado que consultei o cardápio, que ele não é de sobremesa e que o período está aberto
    E o cardápio informado como sobremesa existe naquela validade e está marcado como de sobremesa
    Quando informo o código dele e confirmo a alteração
    Então o código do cardápio de sobremesa fica gravado no cardápio daquela validade
    E a descrição do cardápio de sobremesa aparece na tela

  Cenário: RN-09 — o próprio cardápio é um cardápio de sobremesa
    Dado que o cardápio em tela está marcado como cardápio de sobremesa
    Quando informo um código de cardápio de sobremesa e confirmo a alteração
    Então vejo "* Cardapio cadastrado como sobremesa *"
    E o cursor volta ao código do cardápio de sobremesa
    E nada é gravado

  Cenário: RN-09 — cardápio de sobremesa informado que não existe na validade
    Dado que o código informado como cardápio de sobremesa não existe naquela validade
    Quando confirmo a alteração
    Então vejo "* Cardapio nao cadastrado neste periodo *"
    E o cursor volta ao código do cardápio de sobremesa
    E nada é gravado

  Cenário: RN-09 — cardápio informado que não é de sobremesa
    Dado que o código informado existe naquela validade, mas não está marcado como cardápio de sobremesa
    Quando confirmo a alteração
    Então vejo "* Cardapio nao cadastrado como sobremesa *"
    E o cursor volta ao código do cardápio de sobremesa
    E nada é gravado

  Cenário: RN-10 — gravar as marcas de semana do rodízio
    Dado que consultei o cardápio, que o período está aberto
    E que aquele cardápio não está no planejamento semanal das semanas que vou marcar
    Quando preencho as marcas das semanas que ele atende e confirmo a alteração
    Então cada marca preenchida fica gravada como S
    E cada marca deixada em branco fica gravada em branco

  Cenário: RN-10 — marca de semana que já está no planejamento
    Dado que o cardápio está no planejamento semanal de uma das semanas marcadas
    Quando confirmo a alteração
    Então vejo "* Cardapio no planejamento desta semana *"
    E o cursor volta à marca daquela semana
    E nada é gravado

  Cenário: RN-11 — abrir a tela pelo menu
    Dado que abro a tela C815T pela opção do menu
    Quando a tela é apresentada
    Então ela abre na consulta
    E o cardápio, as datas e as marcas estão em branco
    E nenhum cadastro é lido

  Cenário: RN-11 — abrir a tela pela manutenção do cardápio
    Dado que a manutenção do cardápio entrega a transação a esta tela
    Quando a tela é apresentada
    Então ela abre na alteração
    E o cardápio, a validade e as marcas dele estão carregados
    E a lista das refeições é montada desde o começo

  Cenário: RN-11 — abrir a tela pelo planejamento semanal
    Dado que o planejamento semanal entrega a transação a esta tela
    Quando a tela é apresentada
    Então ela abre na consulta
    E o cardápio, as datas e as marcas estão em branco

  Cenário: RN-11 — a situação do período
    Dado que o cardápio em tela está com a validade fechada para estimativa
    Quando a tela é apresentada
    Então no lugar da estimativa aparece FECHADO
    E, não estando fechada, aparece um traço

  Cenário: RN-12 — a passagem para a manutenção do cardápio
    Dado que consulto um cardápio que existe naquela validade
    E a marca de novo cardápio está posta
    Quando confirmo
    Então a transação passa para a tela C810T
    E ela abre na consulta com o cardápio, o segmento, as duas datas e as marcas entregues
    E nenhuma manutenção é feita nesta confirmação

  Cenário: RN-12 — passagem com cardápio que não existe na validade
    Dado que a marca de novo cardápio está posta e o cardápio informado não existe naquela validade
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor volta ao campo do código do cardápio
    E nada é gravado

  Cenário: RN-13 — alterar um período fechado
    Dado que consultei o cardápio e a validade dele está fechada para estimativa
    Quando confirmo a alteração
    Então vejo "* Cadastro fechado para este periodo *"
    E o cursor volta ao campo do dia limite
    E nada é gravado

  Cenário: RN-14 — o rastro da gravação
    Dado que liguei uma refeição ao cardápio e desliguei outra, numa alteração
    Quando o sistema processa cada operação
    Então o sistema deixa um registro de auditoria por mudança, dizendo qual cadastro mudou
    E cada registro leva o órgão, o antes e o depois, a operação, a matrícula, o código de acesso, a estação, a data, a hora e a tela que provocou a mudança

  Cenário: RN-15 — sem a permissão de acesso
    Dado que o meu perfil não tem esta tela, ou eu não tenho a permissão da operação
    Quando entro na tela ou confirmo a operação
    Então vejo a recusa de acesso do sistema
    E nenhum cadastro é lido e nada é gravado

  Cenário: RN-16 — campo não numérico
    Quando preencho o código do cardápio, uma das partes das datas, o código do cardápio de sobremesa ou o código da refeição com letra
    Então a tela recusa o campo antes de qualquer leitura de cadastro
    E o cursor volta ao campo recusado
    E nada é gravado

  Cenário: RN-17 — falha do banco durante a gravação
    Dado que a gravação da ligação ou do cardápio falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E a gravação não é considerada feita
```
