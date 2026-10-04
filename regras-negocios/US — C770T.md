# US — C770T — Montar o planejamento de cardápios de um grupo, semana, segmento e período

## Estória

Como **servidor de CRE**, quero **montar e manter o planejamento de cardápios de um
grupo, numa semana, para um segmento de atendimento e dentro de um período**, dizendo,
para cada refeição, o cardápio de cada dia da semana, para que **o que cada grupo serve
em cada dia esteja decidido antes de o período começar e a merenda do dia não dependa de
decisão de última hora**.

O planejamento de cardápios é o que diz o que cada grupo serve em cada dia; ele fica
guardado por grupo, semana, segmento de atendimento, período e refeição. Esta é a tela
que monta essa composição, refeição por refeição e dia por dia: as telas irmãs do mesmo
menu apenas copiam o planejamento para outro grupo ou período e o excluem em lote, e
nenhuma delas monta a composição. Sem esta tela o planejamento não nasce, e as telas de
cópia e de exclusão não têm o que copiar nem o que excluir.

## Contexto

Jornada S000M → C000M → C070M → C770M → C770T.

Ator: servidor de CRE — monta e mantém o planejamento de cardápios do grupo, por semana,
segmento de atendimento e período, refeição por refeição.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A tela é aberta por um menu, e não encadeada por outra tela que lhe passe o registro e a
operação: o `C000M`, o `C070M` e o `C770M` são menus, não gravam nada e não escolhem nada
por esta tela. Quem chega é que informa a operação e sobre qual refeição ela é; não há
nesta jornada comparação da tela que chamou com um código de tela. O contexto de que a
tela se serve — a matrícula, o código de acesso, o privilégio, o tipo de órgão e a
coordenação regional da sessão — é o que a entrada deixou na sessão; a tela não o
recalcula.

A jornada termina nesta tela: as telas irmãs ficam no mesmo menu, mas esta não encaminha
para nenhuma delas.

## Regras de negócio

### RN-01 — A tela monta o planejamento de cardápios de um grupo, semana, segmento e período

A tela identifica o planejamento pelo **grupo** (a coordenação regional escolar), pela
**semana**, pelo **segmento de atendimento** e pelo **período** — este pelas datas de
início e limite — e o guarda **refeição por refeição**. Ela mostra **13 linhas**, e cada
linha é uma refeição: o seu código e a sua descrição curta, o cardápio de cada um dos
**sete dias da semana**, de segunda a domingo, e a indicação do que fazer com aquela
refeição. É a combinação de grupo, semana, segmento de atendimento, refeição e período que
identifica cada planejamento guardado. O cadastro do planejamento tem **18 campos** e
declara capacidade para **160 mil** registros — capacidade é o máximo esperado, não o que
existe.

### RN-02 — A tela só executa com a opção de alteração ou de consulta

A tela aceita duas operações: **alteração (ALT)** e **consulta (CON)**. Qualquer outra é
recusada com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta na
opção, e nada é lido nem gravado. Em branco, a tela adota a **consulta**.

### RN-03 — Só a alteração grava; a consulta não grava nada

Na consulta a tela mostra o que está planejado e para: nenhum planejamento é incluído,
alterado ou excluído, nenhum registro é travado e nenhum lançamento de auditoria é gerado.
Inclusão, alteração e exclusão só acontecem na alteração.

### RN-04 — A alteração exige a combinação que a consulta deixou

Em alteração, a combinação informada — grupo, semana, segmento de atendimento e a
data-limite do período — tem de ser a mesma que a sessão guardou da última consulta.
Diferindo em qualquer um dos quatro, a operação é recusada com
**\* Consulte o planejamento antes da atualizacao \***, com o cursor de volta na operação,
e nada é gravado.

[?] A recusa é uma instrução, e não um beco sem saída: ao recusar, o sistema descarta a
semana que tinha guardado, de modo que a alteração só volta a passar depois de nova
consulta da mesma combinação. Se a intenção é obrigar a consulta a cada alteração, o
acervo não confirma. Pergunta ao site.

### RN-05 — Cada linha opera pela refeição e pela indicação I, A ou E

Em cada linha, o servidor indica o que fazer com a refeição: **I** inclui, **A** altera e
**E** exclui. Linha sem refeição informada, ou com indicação diferente de I, A e E, não
gera operação nenhuma. A indicação é convertida na operação correspondente antes de o
perfil ser conferido.

[?] A linha sem refeição é dispensada das conferências, mas a gravação acontece numa
passagem posterior que não repete essa dispensa: só o que a conferência marcou como erro é
que barra a gravação. Se uma linha com a refeição em branco e a indicação I chega a ser
gravada, o acervo não fecha. Pergunta ao site.

### RN-06 — A semana só aceita A, B, C ou D

A semana informada tem de ser **A**, **B**, **C** ou **D**; qualquer outra coisa é
recusada com **\* Informe semana com A, B, C ou D \***, com o cursor de volta na semana. A
conferência é da consulta: quem altera aproveita a consulta que já fez.

[?] A tela irmã que copia planejamento aceita também a semana **T**, com outro sentido. Se
o T vale para esta tela, o acervo não diz. Pergunta ao site.

### RN-07 — O grupo e o segmento de atendimento têm de estar cadastrados

O grupo informado é procurado no cadastro dos grupos daquele tipo de órgão; não constando,
a recusa é **\* Grupo nao cadastrado \***, com o cursor de volta nele. Em seguida o
segmento de atendimento é procurado no cadastro dos segmentos; não constando, a recusa é
**\* Segmento nao cadastrado \***, com o cursor de volta nele. O grupo é conferido antes
do segmento, e as duas conferências são da consulta.

[?] O grupo é conferido no cadastro, mas a conferência de acesso recebe a coordenação
regional da sessão, e não o grupo informado. Se um servidor de uma coordenação pode montar
planejamento para outra, o acervo desta jornada não mostra. Pergunta ao site.

### RN-08 — A data-limite do período é obrigatória, e o período tem de ter cardápio cadastrado

O período é informado pela **data-limite**: em branco, a recusa é
**\* Informe a data limite de validade \***, com o cursor nela. Informada, o sistema
procura um cardápio cadastrado naquele período; não havendo nenhum, a recusa é
**\* Nao existem cardapios neste periodo \***, com o cursor de volta na data-limite. A
**data de início** que a tela exibe vem do cardápio encontrado: a data de início digitada
não é conferida contra nada.

### RN-09 — Sem planejamento e sem a refeição atendida pelo segmento, a combinação é recusada

A procura percorre as refeições cadastradas do órgão: a primeira que já tenha planejamento
naquela combinação — ou que o segmento de atendimento atenda — é a que a tela mostra. Não
havendo nenhuma, a recusa é **\* Grupo/Semana/Segmento sem planejamento cadastrad \***. É
essa conferência que impede montar planejamento para uma refeição que o segmento não
atende.

### RN-10 — A inclusão de refeição já planejada é recusada

Para incluir, o sistema procura o planejamento daquela combinação com aquela refeição.
Existindo, a inclusão é recusada com **\* Refeicao ja cadastrada neste grupo/sem/seg.\* **,
e nada é gravado: há um planejamento só por refeição, grupo, semana, segmento de
atendimento e período.

### RN-11 — A alteração e a exclusão exigem a refeição já planejada

Para alterar ou para excluir, o planejamento daquela combinação com aquela refeição tem de
existir; não existindo, a recusa é
**\* Refeicao nao cadastrada neste grupo/sem/seg \***, com o cursor de volta na indicação
da linha, e nada é gravado.

### RN-12 — Cada dia informado tem de ter cardápio cadastrado e válido naquele contexto

Informado o cardápio de um dia, o sistema confere-o em cinco pontos, e cada um tem a sua
recusa: o cardápio tem de estar cadastrado no período e em vigor nele
(**\* Cardapio nao cadastrado \***); não pode ser um cardápio de sobremesa
(**\* Cardapio cadastrado como sobremesa \***); tem de estar cadastrado para aquele
segmento de atendimento (**\* Cardapio nao cadastrado neste segmento \***); tem de estar
marcado para a semana informada (**\* Cardapio nao cadastrado nesta semana \***); e tem de
estar cadastrado para aquela refeição (**\* Cardapio nao cadastrado nesta refeicao \***).
Dia deixado em branco não é conferido. As cinco conferências valem para a inclusão e para
a alteração.

[?] A primeira dessas recusas não fecha com a conferência que a dispara: ela é dada quando
o cardápio **foi encontrado** e a data de início dele é **igual ou anterior** à data de
início do período, e **não** é dada quando o cardápio não foi encontrado — que é justamente
o caso que a mensagem descreve. Ou a conferência invertida é o defeito, ou a mensagem é que
está trocada; o acervo não deixa escolher um dos dois. Pergunta ao site.

### RN-13 — Pelo menos um dia da semana tem de ser informado

A linha sem nenhum cardápio nos sete dias não é aceita: a inclusão e a alteração recusam
com **\* Informe cardapios para os dias \***, com o cursor de volta no primeiro dia, e nada
é gravado.

### RN-14 — Na alteração, os sete dias são regravados e o que identifica o planejamento não muda

A alteração regrava a composição dos sete dias do planejamento encontrado, depois de
travá-lo. O que identifica o planejamento — grupo, semana, segmento de atendimento,
refeição e período — não muda, e a data de início do período, que a tela exibe do cardápio
cadastrado, não é regravada na alteração: quem a grava é a inclusão.

### RN-15 — Toda operação deixa duas trilhas

Inclusão, alteração e exclusão gravam, além do planejamento, **dois** lançamentos de
auditoria: o lançamento comum do sistema, com a operação, quem operou, a estação, a sessão
(dia, mês, ano e hora), o tipo de órgão e o **conteúdo anterior e o posterior** do
planejamento; e um lançamento próprio do planejamento, que identifica a tela e o cadastro
alterado, o grupo, a semana, o segmento de atendimento, o período e o campo alterado. Na
inclusão o conteúdo anterior vai em branco e o posterior é o planejamento
gravado; na exclusão o posterior vai em branco. Na alteração, o lançamento próprio só é
gravado quando a composição dos sete dias muda — o lançamento comum é gravado sempre. O
cadastro da trilha comum tem **15 campos** e declara capacidade para **60 milhões** de
registros; o da trilha própria do planejamento tem **19 campos** e declara capacidade para
**1 milhão**.

### RN-16 — A operação só acontece com o perfil autorizado, e a abertura da tela é conferida

Cada linha, antes de gravar, passa pela conferência de acesso: o sistema procura, para o
código de acesso e a tela, a permissão da operação pretendida — inclusão, alteração ou
exclusão. Não estando liberada, a operação é recusada com mensagem e a tela é abandonada
sem gravar. A transação também passa pela conferência de rota, que recebe a tela pedida, a
matrícula, o código de acesso, o privilégio, o tipo de órgão e a coordenação regional da
sessão. A abertura da própria tela é conferida no cadastro de telas, e sem essa conferência
a tela não segue.

### RN-17 — Os códigos e as datas da tela passam pela edição numérica

Os **dezesseis** campos numéricos da tela — o grupo, o segmento de atendimento, as três
partes das duas datas, a refeição e os cardápios dos sete dias — são tratados como número:
o campo em branco vale zero, os zeros à esquerda são descartados e o que não for número é
recusado, com o cursor de volta no campo.

[?] O texto que o servidor vê nessa recusa não está nesta jornada: a edição é uma rotina
comum, a mesma que a entrada usa nos seus próprios campos. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Montar o planejamento de cardápios de um grupo, semana, segmento e período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C770T

  Cenário: A consulta mostra o planejamento e não grava nada
    Dado que existe planejamento para o grupo, a semana, o segmento e o período que vou informar
    Quando abro a C770T em modo de consulta e informo a combinação
    Então vejo, em cada linha, a refeição e os cardápios dos sete dias já planejados
    E nada é gravado, nada é travado e nenhum lançamento de auditoria é gerado

  Cenário: Operação diferente de alteração e de consulta
    Quando informo uma operação diferente de ALT e de CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo da operação
    E nada é lido nem gravado

  Cenário: Alteração sem consultar antes a mesma combinação
    Dado que a sessão não tem guardada a combinação que vou informar
    Quando indico ALT e informo a combinação
    Então vejo a mensagem "* Consulte o planejamento antes da atualizacao *"
    E o cursor volta para o campo da operação
    E nada é gravado

  Cenário: Linha sem refeição ou com indicação desconhecida é ignorada
    Dado que preenchi uma linha sem a refeição, ou com uma indicação diferente de I, A e E
    Quando a tela processa as linhas
    Então aquela linha não gera operação nenhuma

  Cenário: Semana fora de A, B, C e D
    Dado que consultei a combinação e informei uma semana diferente de A, B, C e D
    Quando envio a tela
    Então vejo a mensagem "* Informe semana com A, B, C ou D *"
    E o cursor volta para o campo da semana
    E nada é gravado

  Cenário: Grupo não cadastrado
    Dado que informei um grupo que não consta do cadastro daquele tipo de órgão
    Quando envio a consulta
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta para o campo do grupo
    E nada é gravado

  Cenário: Segmento de atendimento não cadastrado
    Dado que informei um segmento que não consta do cadastro daquele tipo de órgão
    Quando envio a consulta
    Então vejo a mensagem "* Segmento nao cadastrado *"
    E o cursor volta para o campo do segmento
    E nada é gravado

  Cenário: Data-limite do período em branco
    Dado que a combinação passou nas conferências de grupo e de segmento
    Quando envio a consulta sem informar a data-limite
    Então vejo a mensagem "* Informe a data limite de validade *"
    E o cursor volta para a data-limite
    E nada é gravado

  Cenário: Período sem cardápio cadastrado
    Dado que não existe cardápio cadastrado para a data-limite informada
    Quando envio a consulta
    Então vejo a mensagem "* Nao existem cardapios neste periodo *"
    E o cursor volta para a data-limite
    E nada é gravado

  Cenário: A data de início exibida é a do cardápio cadastrado
    Dado que digitei uma data de início diferente da do cardápio cadastrado
    Quando o sistema encontra o cardápio do período
    Então a data de início em tela passa a ser a do cardápio cadastrado

  Cenário: Combinação sem planejamento e sem refeição atendida pelo segmento
    Dado que nenhuma refeição tem planejamento naquela combinação
    E o segmento informado não atende a nenhuma delas
    Quando envio a consulta
    Então vejo a mensagem "* Grupo/Semana/Segmento sem planejamento cadastrad *"
    E nada é gravado

  Cenário: Inclusão de uma refeição nova no planejamento
    Dado que consultei a combinação e ela passou nas conferências
    E a refeição indicada ainda não está planejada naquela combinação
    Quando indico I na linha e informo o cardápio de cada dia
    Então o sistema grava o planejamento daquela refeição
    E registra a operação nas duas trilhas de auditoria, com a composição nova como conteúdo posterior

  Cenário: Inclusão de refeição já planejada é recusada
    Dado que a refeição indicada já está planejada naquela combinação
    Quando indico I na linha
    Então vejo a mensagem "* Refeicao ja cadastrada neste grupo/sem/seg.*"
    E o cursor volta para a indicação da linha
    E nada é gravado

  Cenário: Alteração dos cardápios dos dias de uma refeição planejada
    Dado que a refeição já está planejada naquela combinação
    Quando indico A na linha e troco o cardápio de um ou mais dias
    Então o sistema regrava a composição dos sete dias
    E registra a operação nas duas trilhas de auditoria, com a composição anterior e a nova

  Cenário: Alteração que não muda nenhum dia ainda registra a operação
    Dado que a refeição já está planejada e os sete dias informados são os mesmos que estavam guardados
    Quando indico A na linha
    Então o sistema regrava a composição dos sete dias
    E registra a auditoria comum, sem o lançamento próprio do planejamento

  Cenário: Exclusão do planejamento de uma refeição
    Dado que a refeição está planejada naquela combinação
    Quando indico E na linha
    Então o sistema exclui o planejamento daquela refeição
    E registra a operação nas duas trilhas de auditoria, com o conteúdo posterior em branco

  Cenário: Operação sobre refeição não planejada é recusada
    Dado que a refeição indicada não está planejada naquela combinação
    Quando indico A ou E na linha
    Então vejo a mensagem "* Refeicao nao cadastrada neste grupo/sem/seg *"
    E o cursor volta para a indicação da linha
    E nada é gravado

  Cenário: Cardápio do dia não cadastrado no período
    Dado que informei num dia um cardápio que não está cadastrado no período
    Quando indico I ou A na linha
    Então vejo a mensagem "* Cardapio nao cadastrado *"
    E nada é gravado

  Cenário: Cardápio de sobremesa não pode ser planejado como refeição
    Dado que informei num dia um cardápio cadastrado como sobremesa
    Quando indico I ou A na linha
    Então vejo a mensagem "* Cardapio cadastrado como sobremesa *"
    E nada é gravado

  Cenário: Cardápio não cadastrado para o segmento de atendimento
    Dado que o cardápio informado não está cadastrado para aquele segmento
    Quando indico I ou A na linha
    Então vejo a mensagem "* Cardapio nao cadastrado neste segmento *"
    E nada é gravado

  Cenário: Cardápio sem a semana informada
    Dado que o cardápio informado não está marcado para a semana da combinação
    Quando indico I ou A na linha
    Então vejo a mensagem "* Cardapio nao cadastrado nesta semana *"
    E nada é gravado

  Cenário: Cardápio não cadastrado para a refeição
    Dado que o cardápio informado não está cadastrado para aquela refeição
    Quando indico I ou A na linha
    Então vejo a mensagem "* Cardapio nao cadastrado nesta refeicao *"
    E nada é gravado

  Cenário: Linha sem nenhum dia informado
    Dado que deixei os sete dias da linha em branco
    Quando indico I ou A naquela linha
    Então vejo a mensagem "* Informe cardapios para os dias *"
    E o cursor volta para o primeiro dia da linha
    E nada é gravado

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não tem liberada a operação pretendida para a tela
    Quando indico I, A ou E em uma linha
    Então a operação é recusada com mensagem
    E a tela é abandonada sem gravar

  Cenário: Código ou data não numérica
    Dado que informei, num campo numérico da tela, algo que não é número
    Quando a tela edita os campos
    Então a entrada é recusada
    E o cursor volta para o campo
```
