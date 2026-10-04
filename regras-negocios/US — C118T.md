# US — C118T — Declarar justificativas por refeição

## Estória

Como **servidor de CRE**, quero **declarar quais justificativas estão previstas para cada
refeição do tipo de órgão da minha secretaria**, para que **o motivo registrado para quem não
recebe a refeição seja um dos que aquela refeição admite**.

A refeição nasce no cadastro do tipo de órgão e é distribuída, depois, por segmento e por grupo
de atendimento. Esta tela acrescenta o motivo: liga a refeição, uma a uma, às justificativas que
podem ser usadas com ela. É essa ligação que declara a justificativa para a refeição; sem ela, a
justificativa existe no catálogo do tipo de órgão, mas não vale para aquela refeição.

## Contexto

Jornada S000M → C000M → C028M → C029M → C118T (5 passos).

Ator: servidor de CRE — declara, para o tipo de órgão da sua secretaria, quais justificativas
estão previstas para cada refeição.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

A `C118T` é uma tela de transação, não um menu: ela trabalha sobre **uma refeição por vez** e
mostra as justificativas dela em **13 linhas de grade**. Do contexto da sessão ela usa o tipo de
órgão do vínculo do servidor — **não há campo para escolhê-lo**. Ela encadeia com a `C114T` nos
dois sentidos: a `C114T`, que trata as refeições de cada grupo de atendimento, entrega a sessão a
esta tela com a refeição e o modo de consulta já escolhidos; e esta tela devolve a sessão à
`C114T`, em consulta, quando o indicador de consulta vem preenchido.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A ligação que esta tela mantém

O cadastro que esta tela mantém é a ligação entre uma **refeição** e uma **justificativa**,
dentro do **tipo de órgão**. Cada registro tem **4 campos** — contei entre o cabeçalho e o
fechamento do cadastro no dicionário da base — e se identifica por três códigos: o tipo de órgão,
a refeição e a justificativa. Essa combinação **não se repete**: a chave do cadastro não admite
duplicidade. O quarto campo é um **indicador de atendimento em creche**, que o dicionário marca
como obrigatório. O cadastro é dimensionado para **1.200 registros** — capacidade, o máximo
esperado, e não o volume cadastrado.

Esta tela é a única que escreve nesse cadastro, e nenhum outro programa do acervo o lê.

[?] O indicador de atendimento em creche existe na ligação e esta tela **nunca** o informa: nem
na inclusão, nem na exclusão. O que fica gravado nesse campo, e o que ele significa nesta
ligação, não está no acervo. Pergunta ao site.

[?] Nenhum outro programa do acervo lê esta ligação: a tela é a única que a escreve e não há
quem a consulte. O que o sistema faz com a declaração, e quem a consome adiante, não está no
lote. Pergunta ao site.

### RN-02 — A grade tem 13 linhas, e cada linha traz a justificativa, a situação e a descrição

A grade comporta **13 linhas**, e cada linha tem **3 posições** — a justificativa (2 dígitos) e a
situação (uma letra) —, o que dá **39 posições de grade**. Fora da grade, o cabeçalho tem **9
itens**: a tela, a origem, o número da transação, a data de entrada, o mês de referência, a opção
de manutenção, a tela de destino, a refeição e o indicador de consulta. Contei item a item o
leiaute de entrada do programa: 9 no cabeçalho e 3 posições em cada uma das 13 linhas.

Na exibição, cada linha ocupa **80 posições** e mostra, além do código da justificativa e da
situação, a **descrição da justificativa**, com 40 posições, que vem do catálogo de justificativas
do tipo de órgão. Fora da grade, o cabeçalho mostra a descrição do tipo de órgão da sessão, a data
do sistema e a descrição da refeição em trabalho.

[?] A tela nomeia **um único** campo: a refeição (**COD.REFEICAO**). A coluna da justificativa
entra na conferência numérica com o próprio nome técnico do campo como rótulo, e o que o usuário
lê no cabeçalho da grade e na coluna da situação não está na fonte. Pergunta ao site.

### RN-03 — O tipo de órgão do vínculo do servidor é o escopo de tudo

Tudo o que a tela lê e grava é do **tipo de órgão do vínculo** do servidor — o mesmo que a
entrada deixou na sessão: a ligação entre refeição e justificativa, o catálogo de justificativas,
o cadastro de refeições e a declaração das refeições por grupo de atendimento. Não há campo para
escolher outro tipo de órgão; a descrição dele e a data do sistema abrem o cabeçalho.

### RN-04 — Abrindo, a tela mostra as justificativas da refeição que estiver na sessão, em consulta

Aberta, a tela procura a **refeição que estiver na sessão da tela** — a que a listagem estava
mostrando. Não havendo refeição na sessão, **nada é listado e nenhuma mensagem aparece**. Havendo,
a tela assume a **consulta** — salvo se a sessão já trouxer outra opção — e percorre as
justificativas declaradas para aquela refeição na ordem da chave do cadastro, mostrando **13 por
vez**, cada uma com o código e a descrição vindos do catálogo. Quando a refeição não tem
**nenhuma** justificativa declarada, a tela avisa **\* Registros nao cadastrados \***. Esgotada a
lista, a posição volta ao começo na exibição seguinte. A listagem não grava nada.

### RN-05 — A tela só altera ou consulta, e a opção fica guardada na sessão

A opção de manutenção aceita apenas **alterar** e **consultar**: incluir e excluir se fazem pelas
linhas, com a alteração. Qualquer outra opção é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta no campo da opção, e nada é
gravado. Passando a conferência, a opção fica guardada na sessão da tela: é nela que a tela reabre
na exibição seguinte.

[?] A mensagem manda usar **ALT** e **CON**, e a conferência compara o que foi informado com os
códigos internos de alteração e de consulta. Nenhum fonte do lote mostra quem traduz o que o
servidor digita no código conferido — a mesma forma aparece nas outras telas de manutenção deste
sistema. Se não houver tradução, a conferência recusa toda opção, inclusive as duas que a própria
mensagem pede, e nenhuma justificativa é declarada por esta tela. Pergunta ao site.

[?] A recusa da opção não é reconferida no caminho que grava: ele descarta apenas a consulta, e o
que separa uma recusa da gravação é a marca de falha que a rotina de mensagem do ambiente deixa —
rotina que não está no lote. Se ela não marcar, uma linha com a opção recusada ainda assim é
gravada. Pergunta ao site.

### RN-06 — Alterar exige que a refeição já tenha sido consultada

Com a opção de alteração, a **refeição informada tem de ser a que está na sessão da tela**. Sendo
outra, a alteração é recusada com **\* Consulte antes de atualizar \***, com o cursor de volta no
campo da refeição, e nada é gravado: o caminho é consultar a refeição primeiro e só depois
alterá-la.

### RN-07 — Informar a refeição em consulta a carrega, e ela tem de existir e estar no cálculo da média

Com a opção de consulta, informar a refeição **carrega-a para a sessão da tela**: a listagem passa
a ser a das justificativas dela, e o cabeçalho, a mostrar a descrição dela. Antes de carregar, a
tela confere três coisas, nesta ordem:

- a refeição tem de estar informada — em branco, a recusa é **\* Informe codigo da refeicao \***;
- a refeição tem de estar **cadastrada** no tipo de órgão — não estando, a recusa é
  **\* Refeicao nao cadastrada \***;
- a refeição tem de estar **declarada no cálculo da média**, isto é, ter pelo menos uma ligação
  com grupo de atendimento — não tendo, a recusa é
  **\* Refeicao nao cadastrada no calculo da media \***.

As três recusas devolvem o cursor ao campo da refeição, nada é gravado, e a refeição em trabalho
continua a que estava.

[?] A refeição carrega, no próprio cadastro, a marca de que tem justificativa — a que a tela do
cadastro de refeições mostra como **Sim** ou **Nao** —, e esta tela **não a consulta**: ela deixa
declarar justificativa para qualquer refeição cadastrada e declarada no cálculo da média. Se a
marca deveria limitar esta tela, a fonte não diz. Pergunta ao site.

### RN-08 — A situação da linha decide o que fazer com ela

Em cada linha, a **situação** decide a operação: **I** inclui e **E** exclui. Linha cuja situação
não é I nem E não gera operação nenhuma — a tela passa adiante sem avisar. Linha sem
**justificativa** informada é descartada antes das conferências. Antes de manter, a tela confere
se o perfil de quem opera autoriza a operação daquela linha; não autorizando, nada é gravado.

### RN-09 — Incluir exige a justificativa cadastrada e ainda não declarada para a refeição

Para incluir, a tela confere dois cadastros. A **justificativa** informada tem de estar no
**catálogo de justificativas** do tipo de órgão; não estando, a recusa é
**\* Justificativa nao cadastrada \***, com o cursor de volta no campo da justificativa, e nada é
gravado. Estando, a tela procura a **ligação** daquela justificativa com a refeição em trabalho; já
existindo, a inclusão é recusada com **\* Justificativa ja cadastrada nesta refeicao \***, com o
cursor no mesmo campo, e nada é gravado. A chave do cadastro não admite a combinação repetida.

### RN-10 — Excluir exige a justificativa cadastrada, e não confere se ela está declarada

Para excluir, a tela confere apenas o **catálogo de justificativas**: a justificativa informada tem
de estar cadastrada no tipo de órgão; não estando, a recusa é **\* Justificativa nao cadastrada \***,
com o cursor de volta no campo da justificativa, e nada é gravado. Nesse caminho a tela **não**
confere se a justificativa está declarada para a refeição.

[?] A exclusão segue para a gravação mesmo quando a declaração **não existe**: a tela monta a
trilha de auditoria com o conteúdo anterior lido de dados que essa passagem não leu e manda apagar.
Ou o caminho apaga uma declaração que já não havia, e a auditoria registra uma exclusão que não
aconteceu, ou a conferência da exclusão está no cadastro errado — ela exige o catálogo e deveria
exigir a declaração. A fonte não fecha. Pergunta ao site.

### RN-11 — Incluir cria a ligação; excluir apaga a ligação

A **inclusão** grava a ligação com o **tipo de órgão da sessão**, a **refeição em trabalho na
sessão** e a **justificativa da linha** — a refeição gravada é a da sessão, e não a que estiver no
campo. A **exclusão** apaga a ligação inteira. Nenhuma das duas toca o catálogo de justificativas,
o cadastro de refeições nem a declaração das refeições por grupo de atendimento: esses são apenas
lidos.

### RN-12 — Cada operação deixa rastro na auditoria

Cada inclusão e cada exclusão grava também um registro no **cadastro de auditoria** (`A010T`), com
a operação (inclusão ou exclusão), o cadastro tocado, a tela `C118T`, a matrícula de quem operou, a
estação, o tipo de órgão, a data e a hora, o número do processo — que recebe o **código da
refeição** — e o conteúdo anterior e o posterior da ligação: na inclusão o anterior vai em branco
e o posterior é a ligação criada; na exclusão o anterior é a ligação apagada e o posterior vai em
branco.

[?] A auditoria grava a **CRE zerada**: o programa zera esse campo antes de montar o registro, nas
duas operações. Se isso é intencional, e como se confere a auditoria sem a CRE de quem operou, não
está no acervo. Pergunta ao site.

[?] Na inclusão, a trilha de auditoria só é montada se um **estado** deixado pela rotina de
gravação não for um valor determinado; na exclusão não há condição nenhuma. Nenhum programa do
lote escreve esse valor, e o que ele significa na gravação de uma ligação não está no acervo — se
ele aparecer, a inclusão passa sem deixar rastro. Pergunta ao site.

### RN-13 — O indicador de consulta devolve a sessão à tela C114T, em consulta e sem refeição

Quando o **indicador de consulta** vem preenchido com um valor que não é o de "não" nem branco, a
tela não mantém nada: ela **devolve a sessão à tela `C114T`** — a das refeições de cada grupo de
atendimento —, **em consulta e sem refeição escolhida**, para que a lista comece do começo. Essa
devolução tem precedência sobre a manutenção das linhas: acontece antes de qualquer conferência de
linha e interrompe o processamento.

Quem ler esta estória isolada precisa saber que a passagem se faz **sem menu**: esta tela entrega à
`C114T` o modo de consulta e a ausência de refeição, e é por isso que a `C114T` abre em consulta,
listando desde o início.

[?] Quem preenche o indicador de consulta, e com que valor, não está em nenhum programa do lote:
as telas irmãs deste sistema desviam para a **sua própria** tela de consulta quando o indicador vem
preenchido, e esta desvia para a `C114T` — não existe, no acervo, tela de consulta desta. Se a
devolução para a `C114T` é a intenção, ou se o alvo está trocado, a fonte não diz. Pergunta ao
site.

### RN-14 — O modo e a refeição vêm de quem chamou a tela

A tela é alcançada pelo menu, mas também é **encadeada** pela tela `C114T`, que lhe entrega, pela
área da sessão, a refeição e o modo de consulta. Se a sessão já trouxer uma **opção de manutenção**,
a tela usa essa opção em vez de assumir a consulta; e se a sessão já trouxer uma **refeição**, a
tela abre mostrando as justificativas dela. Chegando pelo menu, a sessão vem vazia, a tela assume a
consulta e a refeição é a que o servidor informar.

É a **mesma área de sessão** das duas telas, com o mesmo conteúdo: o que a `C114T` deixa lá é o que
esta tela lê, e é por isso que o comportamento dela muda conforme quem a chamou — sem nenhum campo
da própria tela que o diga.

### RN-15 — Nada é exibido nem gravado sem a segurança de sessão, de rota e de permissão

Na abertura, a tela confere se ela própria existe no cadastro de telas — não existindo, o aviso é
**\* Tela nao disponivel \*** — e se o código de acesso de quem opera tem a tela — não tendo, a
recusa é **\* Acesso negado para esta matricula \***. Na passagem que mantém, ela confere a rota —
tendo a tela sido retirada do cadastro de telas, o aviso é **\* Tela nao cadastrada \*** — e, para
a operação que a linha pede, a autorização daquela operação no mesmo código de acesso — não tendo,
a recusa é **\* Acesso negado para esta operacao \***. Nas recusas nada é gravado.

[?] A permissão da operação é conferida na passagem de validação e **não** se repete na passagem
que grava: se ela mudasse entre as duas, a gravação não a reconferiria. Pergunta ao site.

[?] De onde vêm os dados da sessão que a conferência recebe não está em nenhum programa desta
jornada: nem o `LOGON` nem o `S000M` os preenchem, e quem os preenche não veio no acervo. Pergunta
ao site.

### RN-16 — A consulta não grava nada

Na consulta a tela só mostra: ela lista as justificativas da refeição, não confere as linhas e
desvia do caminho que grava. Nenhuma ligação é incluída ou apagada, e nenhuma trilha de auditoria é
gerada.

---

## Cenários BDD

```gherkin
Funcionalidade: Declarar as justificativas de cada refeição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C118T

  Cenário: RN-01, RN-02, RN-03 e RN-04 — abrir a tela mostra as justificativas da refeição da sessão
    Dado que a refeição em trabalho na sessão tem justificativas declaradas
    Quando abro a tela C118T
    Então ela abre em consulta
    E vejo até 13 linhas, cada uma com a justificativa e a situação
    E cada linha traz a descrição da justificativa
    E o cabeçalho identifica o tipo de órgão do meu vínculo, a data do sistema e a refeição em trabalho
    E não há campo para escolher outro tipo de órgão
    E nada é gravado

  Cenário: RN-04 — refeição sem nenhuma justificativa declarada
    Dado que a refeição em trabalho na sessão não tem nenhuma justificativa declarada
    Quando abro a tela C118T
    Então vejo a mensagem "* Registros nao cadastrados *"
    E nenhuma linha é preenchida

  Cenário: RN-04 — abrir a tela sem refeição na sessão
    Dado que a sessão da tela não tem refeição escolhida
    Quando abro a tela C118T
    Então nenhuma linha é preenchida
    E nenhuma mensagem é mostrada

  Cenário: RN-05 — opção de manutenção não disponível
    Dado que estou na tela C118T
    Quando informo uma opção diferente de alterar e de consultar
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: RN-05 — a tela reabre na opção da última vez
    Dado que usei a tela C118T com a opção de alteração
    Quando a tela é exibida de novo na mesma sessão
    Então ela reabre na opção de alteração

  Cenário: RN-06 — alterar sem ter consultado a refeição
    Dado que estou na tela C118T com a opção de alteração
    E a refeição em trabalho na sessão é outra
    Quando informo uma refeição diferente da que está na sessão
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo da refeição
    E nada é gravado

  Cenário: RN-07 — informar a refeição em branco
    Dado que estou na tela C118T com a opção de consulta
    Quando deixo o campo da refeição em branco
    Então vejo a mensagem "* Informe codigo da refeicao *"
    E o cursor volta ao campo da refeição

  Cenário: RN-07 — consultar uma refeição que não está cadastrada
    Dado que estou na tela C118T com a opção de consulta
    Quando informo uma refeição que não existe no meu tipo de órgão
    Então vejo a mensagem "* Refeicao nao cadastrada *"
    E o cursor volta ao campo da refeição
    E nada é gravado

  Cenário: RN-07 — consultar uma refeição que não está no cálculo da média
    Dado que estou na tela C118T com a opção de consulta
    Quando informo uma refeição cadastrada que não tem nenhuma ligação com grupo de atendimento
    Então vejo a mensagem "* Refeicao nao cadastrada no calculo da media *"
    E o cursor volta ao campo da refeição
    E nada é gravado

  Cenário: RN-07 — consultar a refeição carrega a listagem dela
    Dado que estou na tela C118T com a opção de consulta
    E a refeição informada está cadastrada e declarada no cálculo da média
    Quando informo essa refeição
    Então ela passa a ser a refeição em trabalho na sessão
    E a listagem passa a mostrar as justificativas declaradas para ela, até 13 por vez
    E o cabeçalho passa a mostrar a descrição daquela refeição
    E nada é gravado

  Cenário: RN-08 — linha com situação desconhecida é ignorada
    Dado que estou na tela C118T com a opção de alteração
    E preenchi uma linha com uma situação diferente de I e de E
    Quando confirmo a mensagem
    Então aquela linha não gera operação nenhuma
    E nenhuma mensagem é mostrada
    E nada é gravado

  Cenário: RN-09 — incluir uma justificativa que não está no catálogo
    Dado que estou na tela C118T com a opção de alteração
    E informo, numa linha, uma justificativa que não está no catálogo do meu tipo de órgão
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Justificativa nao cadastrada *"
    E o cursor volta ao campo da justificativa
    E nada é gravado

  Cenário: RN-09 — incluir uma justificativa que já está declarada para a refeição
    Dado que estou na tela C118T com a opção de alteração
    E a justificativa informada já está declarada para a refeição em trabalho
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Justificativa ja cadastrada nesta refeicao *"
    E o cursor volta ao campo da justificativa
    E nada é gravado

  Cenário: RN-09 e RN-11 — incluir uma justificativa nova
    Dado que estou na tela C118T com a opção de alteração
    E informo, numa linha, uma justificativa do catálogo que ainda não está declarada para a refeição
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então a justificativa passa a constar como declarada para aquela refeição
    E a declaração fica com o tipo de órgão e a refeição em trabalho na sessão
    E a auditoria registra a inclusão

  Cenário: RN-10 — excluir uma justificativa que não está no catálogo
    Dado que estou na tela C118T com a opção de alteração
    E informo, numa linha, uma justificativa que não está no catálogo do meu tipo de órgão
    E assinalo nessa linha a situação E
    Quando confirmo a mensagem
    Então vejo a mensagem "* Justificativa nao cadastrada *"
    E o cursor volta ao campo da justificativa
    E nada é gravado

  Cenário: RN-11 — excluir uma justificativa declarada
    Dado que estou na tela C118T com a opção de alteração
    E a justificativa informada está declarada para a refeição em trabalho
    E assinalo nessa linha a situação E
    Quando confirmo a mensagem
    Então a declaração daquela justificativa sai do cadastro
    E a auditoria registra a exclusão com o valor anterior

  Cenário: RN-12 — toda gravação deixa rastro na auditoria
    Dado que incluí ou excluí uma declaração
    Então a auditoria registra a operação, o cadastro tocado e a tela C118T
    E registra a minha matrícula, a estação, o tipo de órgão, a data e a hora
    E registra o número do processo com o código da refeição
    E registra o conteúdo anterior e o posterior da declaração

  Cenário: RN-13 — o indicador de consulta devolve a tela C114T, em consulta
    Dado que o indicador de consulta vem preenchido com um valor que não é o de "não"
    Quando confirmo a mensagem
    Então a tela não mantém nenhuma linha
    E entrega a sessão à C114T, sem passar por menu
    E a C114T abre em consulta, sem refeição escolhida, listando desde o início
    E nada é gravado

  Cenário: RN-14 — a tela aberta a partir da C114T já vem com a refeição e o modo
    Dado que a tela C114T entregou a sessão a esta tela com uma refeição e o modo de consulta
    Quando a tela C118T é exibida
    Então ela abre em consulta, na refeição que a C114T deixou
    E mostra as justificativas declaradas para aquela refeição

  Cenário: RN-15 — sem permissão para a operação
    Dado que o meu código de acesso tem a tela C118T sem aquela operação liberada
    E informo a opção de alteração com uma linha preenchida
    Quando confirmo a mensagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-15 — sem acesso à tela
    Dado que o meu código de acesso não tem a tela C118T
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: RN-15 — tela fora do cadastro de telas
    Dado que a tela C118T não consta do cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: RN-15 — tela retirada do cadastro de telas
    Dado que a tela C118T foi retirada do cadastro de telas
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é gravado

  Cenário: RN-16 — a consulta não grava nada
    Dado que abri a tela e estou na opção de consulta
    Quando confirmo a mensagem
    Então o cadastro é apenas lido
    E nenhuma justificativa é declarada ou apagada
    E nenhuma trilha de auditoria é gerada
```
