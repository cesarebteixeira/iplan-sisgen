# US — P230T — Pré-liquidação, liquidação e pagamento do processo de despesa

## Estória

Como **servidor de CRE**, quero **registrar e desfazer a pré-liquidação, a
liquidação e o pagamento de um processo de despesa**, para que **o processo
avance até o pagamento com as notas fiscais conferidas, o valor líquido apurado e
o contrato do fornecedor atualizado**.

O processo de despesa nasce preso a um empenho e a um ano, e só anda quando a
secretaria confere as notas fiscais e registra a etapa correspondente. É desse
registro que dependem o pagamento e o saldo do contrato; sem ele o processo fica
parado, e uma etapa lançada por engano só se corrige por aqui.

## Contexto

Jornada S000M → P000M → P230T.

Ator: servidor de CRE — informa a secretaria, as partes do número do processo, o
número do empenho e o ano de referência, marca a etapa que quer registrar ou
desfazer, confere o que a tela mostra e transmite de novo para confirmar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — a
opção 5 do menu do módulo `P000M` — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio. O `P000M` é um menu de seis opções: não procura processo nenhum, não
deixa dado de negócio na sessão e não escolhe operação.

O que esta tela usa das anteriores é o que a entrada deixou na sessão: o **tipo de
órgão**, a **coordenadoria regional escolar do vínculo**, a **matrícula**, o
**código de acesso**, a **estação** e a **data e a hora do sistema**. A secretaria
do processo ela tira do **cadastro de tipos de órgão**, relendo-o para o tipo de
órgão da sessão; a procedência disso está no anexo de evidências.

A `P230T` não encadeia para outra tela: terminada a operação, ela se reapresenta a
si mesma. Ao voltar dela para o menu `P000M`, o menu chega com a opção 5 já
marcada — é o `P000M` que faz isso, não esta tela.

---

## Regras de negócio

### RN-01 — A tela registra e desfaz as três etapas do mesmo processo

A tela serve para registrar e para desfazer três etapas de um processo de despesa:
a **pré-liquidação**, a **liquidação** e o **pagamento**. As três são situações do
mesmo processo, não lançamentos separados: é pela situação registrada que as telas
seguintes sabem em que ponto o processo está.

Registrar a pré-liquidação libera as notas fiscais do processo, acumula no contrato
do fornecedor a quantidade e o valor dos itens e põe o processo como
pré-liquidado. Registrar a liquidação e o pagamento muda a situação desse mesmo
registro. Desfazer apaga a etapa: na pré-liquidação o registro do processo é
excluído e, conforme a resposta do operador, as notas fiscais e o contrato também
são devolvidos; na liquidação e no pagamento o processo volta à situação anterior.

A tela não inclui processo, empenho nem fornecedor: quem os mantém são outras
telas.

### RN-02 — O processo é identificado por cinco dados, e o número tem 14 dígitos

O processo é localizado pelo **tipo de órgão**, pela **secretaria**, pelas **partes
do número do processo**, pelo **número do empenho** e pelo **ano de referência**.

O número do processo não é digitado inteiro: o sistema o monta a partir de quatro
partes — a **secretaria**, a **coordenadoria regional escolar** e as duas que o
operador informa, uma de 6 e outra de 4 dígitos — e forma um número único de **14
dígitos**, que é o que identifica o processo em tudo o que a tela lê e grava. O
tipo de órgão, a secretaria e a coordenadoria vêm da sessão; as duas partes
restantes, não.

[?] Quando a coordenadoria do vínculo não vem preenchida, o sistema monta o número
com zeros na posição dela e desloca a secretaria para essa posição, de modo que o
número fica com a secretaria fora do lugar de sempre. Se é o caso legítimo do
processo sem coordenadoria ou um resíduo do programa, é pergunta ao site.

[?] O que representam as duas partes informadas, de 6 e de 4 dígitos, não está dito
no acervo desta jornada. Pergunta ao site.

### RN-03 — Ao abrir, a tela vem na alteração e propõe o órgão, a secretaria e a coordenadoria da sessão

Ao ser aberta, a tela entra no **modo de alteração** — todas as suas operações
mudam cadastro — e preenche o **tipo de órgão** com o da sessão, a **secretaria do
processo** com a que o cadastro de tipos de órgão guarda para esse tipo de órgão e a
**coordenadoria** com a do vínculo do servidor. Mostra também a **descrição do tipo
de órgão** e a **data do sistema**, limpa a linha de mensagem e começa a contagem
das transmissões.

### RN-04 — Sem as conferências de tela, de acesso e de rota nada é lido nem gravado

Ao abrir, a tela confere: a sessão tem de estar na **estação** em que foi aberta —
em outra, o acesso termina e o sistema volta à tela de entrada; o **registro da
tela** tem de existir, senão a recusa é **\* Tela nao disponivel \***; e o **código
de acesso** do servidor tem de alcançar a tela, senão a recusa é
**\* Acesso negado para esta matricula \***. Uma requisição marcada como **página
2** é recusada com **\* Acesso a pagina 2 negado \***.

Na transmissão, a tela passa pela conferência de **rota** — tela fora do registro é
recusada com **\* Tela nao cadastrada \***, e operação que ela não prevê, com
**\* Operacao nao disponivel \*** — e pela **permissão da operação**: como toda
operação desta tela é de alteração, o código de acesso precisa ter a alteração
liberada para ela, senão a recusa é **\* Acesso negado para esta operacao \***. Se
a transação chegar com o **prefixo de próxima tela** preenchido, esta tela não faz
nada: o prefixo leva o servidor à tela nele indicada.

### RN-05 — A tela só trabalha na alteração

Se o campo da operação chegar com valor diferente da alteração, o sistema recusa
com **\* Opcao nao disponivel. Use ALT \***, devolve o cursor ao campo da operação
e não lê nem grava nada.

[?] A tela tem duas recusas para a mesma situação: a da conferência de rota
(**\* Operacao nao disponivel \***) e a da própria tela
(**\* Opcao nao disponivel. Use ALT \***). Nos fontes desta jornada a conferência
de rota emite a mensagem sem desviar o fluxo, e a tela emite a sua logo depois; não
se conclui se o operador vê as duas, nem qual delas barra a operação. Pergunta ao
site.

### RN-06 — O que o sistema exige antes de qualquer operação

Antes de executar qualquer etapa, nesta ordem:

- a **secretaria do processo** tem de vir preenchida — em branco, a recusa é
  **\* Informe o numero do processo \***, com o cursor de volta no campo do número
  do processo;
- a secretaria informada tem de ser uma das cadastradas para o **tipo de órgão da
  sessão** — não sendo, a recusa é **\* Numero do processo invalido \***, com o
  cursor no mesmo campo;
- as partes do número informadas pelo operador não podem vir todas zeradas — se
  vierem, a recusa é **\* Informe o numero do processo \***;
- o **número do empenho** é exigido — **\* Informe o numero do empenho \***, com o
  cursor no campo do empenho;
- o **ano de referência** é exigido — **\* Informe o ano do exercicio \***, com o
  cursor no campo do ano.

Em nenhum desses casos a tela lê ou grava cadastro de negócio.

[?] A recusa pede o "ano do exercício", e o rótulo da tela é ANO REFERENCIA; se são
o mesmo dado ou dois campos que a máscara separa, o acervo desta jornada não mostra.
Pergunta ao site.

[?] O cadastro do tipo de órgão guarda, além da secretaria principal, até cinco
códigos alternativos que a tela aceita na primeira parte do número do processo. O
que distingue cada um não está no acervo desta jornada. Pergunta ao site.

### RN-07 — As seis marcas: só uma operação acontece, e é a primeira na ordem da tela

A tela oferece seis marcas: **incluir** e **anular** a pré-liquidação, **incluir** e
**anular** a liquidação, **incluir** e **anular** o pagamento. O operador marca o
que quer fazer e transmite; a operação só se efetiva na transmissão seguinte, a de
confirmação.

Quando as seis marcas chegam preenchidas, o sistema recusa com
**\* Escolha apenas uma opcao de atualizacao \*** e devolve o cursor à primeira
delas.

[?] A recusa só acontece quando as **seis** marcas estão preenchidas. Com duas a
cinco marcadas o sistema não avisa: executa a **primeira na ordem da tela** —
incluir a pré-liquidação, anular a pré-liquidação, incluir a liquidação, anular a
liquidação, incluir o pagamento, anular o pagamento — e ignora as demais em
silêncio. Ou a máscara impede mais de uma marca, ou a guarda é mais fraca do que a
mensagem. Pergunta ao site.

[?] As marcas não têm rótulo de validação no acervo desta jornada e a máscara da
tela não está nele: o que o operador digita em cada marca, e se a máscara aceita
mais de uma, não se conclui daqui. Pergunta ao site.

[?] Marca nenhuma: a transmissão termina sem executar operação e sem avisar nada ao
operador. Se é assim que deve ser, é pergunta ao site.

### RN-08 — Inclusão da pré-liquidação: o que a tela confere

Para incluir a pré-liquidação, o processo tem de ter **notas fiscais cadastradas** —
sem nenhuma, a recusa é **\* Processo nao cadastrado \***, com o cursor no número do
processo — e nenhuma delas pode já estar **liberada**. Havendo etapa registrada
para o processo, a recusa depende da situação encontrada:
**\* Processo ja esta pre-liquidado \***, **\* Processo ja esta pago \*** ou
**\* Processo ja esta liquidado \***.

O **contrato do fornecedor** é conferido contra o **FINCON**: o sistema procura o
contrato pela coordenadoria, pelo tipo de contrato e pela data da nota fiscal e,
achando-o, exige que o **número** e o **ano** do contrato informados sejam os mesmos
de lá — senão a recusa é **\* Contrato no FINCON difere do cadastro \*** ou
**\* Ano do contrato no FINCON difere do cadastro \***. O ano do contrato não pode
ser maior que o ano corrente (**\* Ano contrato maior que ano corrente \***) nem
faltar (**\* Informe o ano do contrato no FINCON \***), e o número do contrato
também não pode faltar (**\* Informe o numero do contrato no FINCON \***). Quando o
contrato está no FINCON mas sem número cadastrado, a recusa manda cadastrá-lo em
outra tela: **\* Cadastrar contrato no FINCON na tela C690T \***.

A **data da pré-liquidação** e a **ordem de pré-liquidação** também são exigidas:
**\* Informe a data da pre-liquidacao \***, **\* Data da pre-liquidacao invalida \***
(data que não existe ou cujo ano não cai entre 1994 e 2099) e
**\* Informe a ordem de pre-liquidacao \***.

[?] A recusa que manda cadastrar o contrato no FINCON só aparece quando o contrato
**é encontrado** e o número dele lá está zerado. Quando o contrato **não é
encontrado**, o caminho passa ao largo dessa recusa e apenas exige que o operador
tenha informado número e ano, sem comparar com o FINCON. Ou o desvio está
invertido, ou a conferência do FINCON vale só para o contrato ausente. Não escolhi
um dos lados. Pergunta ao site.

### RN-09 — Inclusão da pré-liquidação: o que a confirmação grava

Confirmada a inclusão, o sistema percorre as **notas fiscais** do processo, soma o
**valor total** e o **valor retido** e apura o **líquido** (o total menos o retido);
mostra o fornecedor, os três valores e a fonte na própria tela e, confirmando o
operador, grava:

- cada nota fiscal do processo fica **liberada**, com a data do dia no lugar da
  data anterior;
- o **contrato do fornecedor** recebe, agrupado por classificação de item, a
  **quantidade** e o **valor** dos itens do processo;
- o processo fica registrado como **pré-liquidado**, com a data e a ordem da
  pré-liquidação, o fornecedor, a fonte, o órgão e os valores apurados.

No fim, a tela avisa **\* PROCESSO PRE-LIQUIDADO \*** e se reapresenta.

[?] Na inclusão, o sistema lê o contrato toda vez que o grupo de itens muda, mas o
trecho que grava o acúmulo só é alcançado quando a lista de itens termina: com
itens em mais de um grupo, só o **último** grupo chega ao contrato. Na anulação,
todos os grupos são subtraídos. Ou o caminho intermediário ficou inalcançável, ou a
anulação subtrai mais do que a inclusão somou — o contrato pode ficar abaixo do que
deveria, até negativo. Não escolhi um dos lados. Pergunta ao site.

[?] A anulação procura os itens do processo marcados como **excluídos**, enquanto a
inclusão só considera os **não excluídos**: os dois lados leem o mesmo cadastro com
o filtro oposto. Ou a marcação tem outro sentido, ou um dos dois lados está
invertido. Pergunta ao site.

[?] A data gravada em cada nota fiscal é a **do dia do processamento**, e não a data
de pré-liquidação que o operador informou; se as duas devem coincidir, é pergunta
ao site.

### RN-10 — Anulação da pré-liquidação: com ou sem devolução

Para anular a pré-liquidação o processo tem de estar **pré-liquidado** — não
estando, a recusa é **\* Processo nao esta pre-liquidado \***; liquidado,
**\* Processo ja esta liquidado \***; pago, **\* Processo ja esta pago \***.

A tela exige que o operador diga se a operação é **somente exclusão**, com S ou N —
sem resposta, a recusa é **\* Informe se somente exclusao com S ou N \***.

Respondendo **S**, o sistema apaga apenas o registro do processo. Respondendo
**N**, além de apagá-lo, devolve cada nota fiscal ao estado anterior, sem a data de
liberação, e subtrai do contrato do fornecedor a quantidade e o valor dos itens. No
fim, a tela avisa **\* PRE-LIQUIDACAO ANULADA \*** e se reapresenta.

### RN-11 — Inclusão da liquidação

Para liquidar, o processo tem de estar **pré-liquidado** — não estando, inclusive
quando não existe para a identificação informada, a recusa é
**\* Processo nao esta pre-liquidado \***; já liquidado,
**\* Processo ja esta liquidado \***; pago, **\* Processo ja esta pago \***.

A tela exige a **data da liquidação** (**\* Informe a data da liquidacao \***,
**\* Data da liquidacao invalida \***) e a **ordem de liquidação**
(**\* Informe a ordem de liquidacao \***). Confirmada a operação, o processo passa a
**liquidado**, com a ordem e a data gravadas, e a tela avisa
**\* PROCESSO LIQUIDADO \***.

### RN-12 — Anulação da liquidação

Para anular a liquidação o processo tem de estar **liquidado** — não estando,
inclusive quando não existe para a identificação informada, a recusa é
**\* Processo nao esta liquidado \***; pré-liquidado,
**\* Processo ja esta pre-liquidado \***; pago, **\* Processo ja esta pago \***.

Confirmada a operação, o processo volta a **pré-liquidado**, com a ordem e a data da
liquidação apagadas, e a tela avisa **\* LIQUIDACAO ANULADA \***.

### RN-13 — Inclusão do pagamento

Para pagar, o processo tem de estar **liquidado**; pré-liquidado, a recusa é
**\* Processo ja esta pre-liquidado \***, e já pago,
**\* Processo ja esta pago \***.

A tela exige a **data do pagamento** (**\* Informe a data de pagamento \***,
**\* Data de pagamento invalida \***) e a **ordem de pagamento**
(**\* Informe a ordem de pagamento \***). Confirmada a operação, o processo passa a
**pago**, com a ordem e a data do pagamento, e a tela avisa **\* PROCESSO PAGO \***.

[?] Quando não existe processo com a identificação informada, a recusa é
**\* Processo nao esta pago \*** — o nome de uma situação, e não o aviso de que o
processo não existe. Se a intenção era outra, é pergunta ao site.

### RN-14 — Anulação do pagamento

Para anular o pagamento o processo tem de estar **pago** — não estando, inclusive
quando não existe para a identificação informada, a recusa é
**\* Processo nao esta pago \***; pré-liquidado,
**\* Processo ja esta pre-liquidado \***; liquidado,
**\* Processo ja esta liquidado \***.

Confirmada a operação, o sistema apaga a ordem e a data do pagamento **e também a
data da liquidação**, devolvendo o processo à situação de **pré-liquidado**, e avisa
**\* PAGAMENTO ANULADO \***.

[?] Anular o pagamento devolve o processo a pré-liquidado, e não a liquidado, e
apaga a data da liquidação — isto é, desfaz duas etapas de uma vez. Se a intenção
era voltar apenas à etapa imediatamente anterior, é pergunta ao site.

### RN-15 — A primeira transmissão não grava: ela confere e pede a confirmação

A primeira transmissão de uma operação **não grava nada**: o sistema faz as
conferências, busca nos cadastros o fornecedor, a fonte, os valores e as datas do
processo e os mostra na própria tela, com a frase **\* Transmita para ... \*** —
incluir ou anular a pré-liquidação, incluir ou anular a liquidação, incluir ou
anular o pagamento. A gravação só acontece na transmissão seguinte, com os mesmos
dados.

Se, entre a conferência e a confirmação, o **número do processo**, o **empenho**, o
**ano** ou as **marcas** mudarem, o sistema volta a conferir em vez de gravar. Por
isso uma etapa marcada e transmitida uma única vez não produz efeito nenhum nos
cadastros.

[?] A confirmação só exige que a identificação e as marcas não tenham mudado: a
**data** e a **ordem** informadas para a etapa podem ser trocadas entre a
conferência e a confirmação e vão para o cadastro sem passar de novo pela
conferência de data. Se a conferência deveria cobrir esses campos, é pergunta ao
site.

### RN-16 — Antes de gravar, o sistema reconfere o fornecedor, a secretaria e a fonte de recurso

Entre a conferência e a gravação, o sistema relê os cadastros do **fornecedor** do
processo, da **secretaria** do tipo de órgão e da **fonte de recurso** do órgão com
a secretaria. Registro que não exista, ou que esteja **excluído** ou **purgado**, é
recusado antes da gravação.

[?] As mensagens dessa reconferência não estão no acervo desta jornada — só o
número delas. E, nos fontes lidos, a reconferência emite a mensagem sem desviar o
fluxo: não se conclui se é a mensagem que impede a gravação ou se a gravação segue
assim mesmo. Pergunta ao site.

### RN-17 — O que fica registrado na auditoria

Cada mudança no registro do processo — criação, alteração de situação e exclusão —
deixa um registro de auditoria com a tela de origem, o cadastro alterado, a
operação, o conteúdo anterior e o posterior, o tipo de órgão, o número do processo,
a coordenadoria, a matrícula do servidor, o terminal e a data e a hora da sessão. Na
anulação da pré-liquidação com devolução, a volta de cada nota fiscal e a subtração
no contrato também deixam o seu registro.

[?] Na inclusão da pré-liquidação, a liberação das notas fiscais e o acúmulo no
contrato não geram registro de auditoria próprio: a inclusão só registra a criação
do processo. Se a intenção era auditar toda gravação, falta trilha nesse caminho — e
a anulação da mesma operação é auditada. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Pré-liquidação, liquidação e pagamento do processo de despesa

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que o meu perfil tem acesso à tela P230T

  Cenário: A abertura da tela
    Dado que o meu vínculo tem tipo de órgão e coordenadoria regional escolar
    Quando abro a tela P230T
    Então ela abre no modo de alteração
    E o tipo de órgão e a coordenadoria já vêm preenchidos com os do meu vínculo
    E a secretaria do processo já vem preenchida com a do tipo de órgão da sessão
    E vejo a descrição do tipo de órgão e a data do sistema

  Cenário: Operação diferente da alteração
    Dado que estou na tela P230T
    Quando informo uma operação diferente da alteração e transmito
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não alcança a tela P230T
    Quando abro a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E nada é lido nem gravado

  Cenário: Tela fora do registro
    Dado que a tela P230T não está no registro de telas
    Quando transmito
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é lido nem gravado

  Cenário: Alteração não liberada para o meu acesso
    Dado que o meu código de acesso não tem a alteração liberada para a tela P230T
    Quando transmito uma etapa
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é lido nem gravado

  Cenário: Estação diferente da da entrada
    Dado que a minha estação não é a mesma do início da sessão
    Quando transmito uma etapa
    Então o acesso termina e o sistema volta à tela de entrada

  Cenário: Secretaria do processo em branco
    Dado que deixei em branco a secretaria do processo
    Quando transmito uma etapa
    Então vejo a mensagem "* Informe o numero do processo *"
    E o cursor volta ao campo do número do processo
    E nada é lido nem gravado

  Cenário: Secretaria que não pertence ao tipo de órgão
    Dado que informei, na secretaria do processo, um código que não é dos cadastrados
      para o tipo de órgão da minha sessão
    Quando transmito uma etapa
    Então vejo a mensagem "* Numero do processo invalido *"
    E o cursor volta ao campo do número do processo
    E nada é lido nem gravado

  Cenário: Número do processo sem as partes do operador
    Dado que deixei zeradas as duas partes do número do processo que eu informo
    Quando transmito uma etapa
    Então vejo a mensagem "* Informe o numero do processo *"
    E nada é lido nem gravado

  Cenário: Número do empenho em branco
    Dado que informei o processo e deixei o número do empenho em branco
    Quando transmito uma etapa
    Então vejo a mensagem "* Informe o numero do empenho *"
    E o cursor volta ao campo do empenho
    E nada é lido nem gravado

  Cenário: Ano de referência em branco
    Dado que informei o processo e o empenho e deixei o ano em branco
    Quando transmito uma etapa
    Então vejo a mensagem "* Informe o ano do exercicio *"
    E o cursor volta ao campo do ano
    E nada é lido nem gravado

  Cenário: As seis marcas preenchidas
    Dado que marquei as seis etapas ao mesmo tempo
    Quando transmito
    Então vejo a mensagem "* Escolha apenas uma opcao de atualizacao *"
    E o cursor volta à primeira marca
    E nada é gravado

  Cenário: Duas marcas preenchidas
    Dado que marquei ao mesmo tempo a inclusão da pré-liquidação e a inclusão do
      pagamento
    Quando transmito
    Então o sistema segue com a primeira na ordem da tela, a inclusão da
      pré-liquidação
    E a outra marca é ignorada

  Cenário: Nenhuma marca preenchida
    Dado que não marquei etapa nenhuma
    Quando transmito
    Então a transmissão termina sem executar operação e sem avisar nada
    E nada é gravado

  Cenário: Pré-liquidação de processo sem notas fiscais
    Dado que o processo informado não tem nenhuma nota fiscal cadastrada
    Quando marco a inclusão da pré-liquidação e transmito
    Então vejo a mensagem "* Processo nao cadastrado *"
    E o cursor volta ao campo do número do processo
    E nada é gravado

  Cenário: Pré-liquidação de processo com etapa já registrada
    Dado que o processo já tem registro de pré-liquidação, de liquidação ou de
      pagamento
    Quando marco a inclusão da pré-liquidação e transmito
    Então vejo a mensagem "* Processo ja esta pre-liquidado *",
      "* Processo ja esta pago *" ou "* Processo ja esta liquidado *"
    E o processo continua na situação em que estava

  Cenário: Contrato ou ano do contrato divergente do FINCON
    Dado que o contrato do fornecedor está no FINCON
    E que informei número ou ano de contrato diferentes dos que lá estão
    Quando marco a inclusão da pré-liquidação e transmito
    Então vejo a mensagem "* Contrato no FINCON difere do cadastro *" ou
      "* Ano do contrato no FINCON difere do cadastro *"
    E nada é gravado

  Cenário: Contrato sem número cadastrado no FINCON
    Dado que o contrato do fornecedor está no FINCON sem número de contrato
    Quando marco a inclusão da pré-liquidação e transmito
    Então vejo a mensagem "* Cadastrar contrato no FINCON na tela C690T *"
    E o cursor volta ao campo do número do contrato
    E nada é gravado

  Cenário: Ano do contrato ausente ou maior que o ano corrente
    Dado que deixei o ano do contrato em branco ou informei um ano futuro
    Quando marco a inclusão da pré-liquidação e transmito
    Então vejo a mensagem "* Informe o ano do contrato no FINCON *" ou
      "* Ano contrato maior que ano corrente *"
    E nada é gravado

  Cenário: Número do contrato em branco
    Dado que deixei o número do contrato em branco
    Quando marco a inclusão da pré-liquidação e transmito
    Então vejo a mensagem "* Informe o numero do contrato no FINCON *"
    E nada é gravado

  Cenário: Data ou ordem da pré-liquidação faltando ou inválida
    Dado que não informei a data ou a ordem da pré-liquidação, ou que informei uma
      data que não existe
    Quando marco a inclusão da pré-liquidação e transmito
    Então vejo a mensagem "* Informe a data da pre-liquidacao *",
      "* Data da pre-liquidacao invalida *" ou
      "* Informe a ordem de pre-liquidacao *"
    E nada é gravado

  Cenário: A conferência da pré-liquidação mostra os valores e pede a transmissão
    Dado que o processo pode ser pré-liquidado e que os dados do contrato conferem
    Quando marco a inclusão da pré-liquidação e transmito
    Então vejo o fornecedor, a fonte, o valor total das notas, o valor retido e o
      líquido apurado
    E vejo a mensagem "* Transmita para incluir a pre-liquidacao *"
    E nada é gravado ainda

  Cenário: A confirmação grava a pré-liquidação
    Dado que conferi os valores da pré-liquidação e não mudei nada
    Quando transmito de novo
    Então cada nota fiscal do processo fica liberada com a data do dia
    E o contrato do fornecedor recebe a quantidade e o valor dos itens
    E o processo fica pré-liquidado, com a data e a ordem da pré-liquidação
    E vejo a mensagem "* PROCESSO PRE-LIQUIDADO *"

  Cenário: Anulação da pré-liquidação com devolução das notas e do contrato
    Dado que o processo está pré-liquidado
    Quando marco a anulação da pré-liquidação, respondo N e confirmo
    Então o registro do processo é apagado
    E cada nota fiscal volta ao estado anterior, sem a data de liberação
    E o contrato do fornecedor é subtraído da quantidade e do valor dos itens
    E vejo a mensagem "* PRE-LIQUIDACAO ANULADA *"

  Cenário: Anulação da pré-liquidação somente com a exclusão do registro
    Dado que o processo está pré-liquidado
    Quando marco a anulação da pré-liquidação, respondo S e confirmo
    Então somente o registro do processo é apagado
    E as notas fiscais e o contrato ficam como estavam
    E vejo a mensagem "* PRE-LIQUIDACAO ANULADA *"

  Cenário: Anulação da pré-liquidação sem a resposta S ou N
    Dado que o processo está pré-liquidado
    Quando marco a anulação da pré-liquidação sem responder se é somente exclusão
    Então vejo a mensagem "* Informe se somente exclusao com S ou N *"
    E nada é gravado

  Cenário: Anulação da pré-liquidação de processo sem a etapa
    Dado que o processo não está pré-liquidado
    Quando marco a anulação da pré-liquidação e transmito
    Então vejo a mensagem "* Processo nao esta pre-liquidado *"
    E nada é gravado

  Cenário: Liquidação registrada
    Dado que o processo está pré-liquidado
    E que informei a data e a ordem da liquidação
    Quando marco a inclusão da liquidação, confiro e confirmo
    Então o processo fica liquidado, com a ordem e a data gravadas
    E vejo a mensagem "* PROCESSO LIQUIDADO *"

  Cenário: Liquidação recusada pela situação do processo
    Dado que o processo não está pré-liquidado, ou já está liquidado, ou já está pago
    Quando marco a inclusão da liquidação e transmito
    Então vejo a mensagem "* Processo nao esta pre-liquidado *",
      "* Processo ja esta liquidado *" ou "* Processo ja esta pago *"
    E nada é gravado

  Cenário: Anulação da liquidação devolve o processo à pré-liquidação
    Dado que o processo está liquidado
    Quando marco a anulação da liquidação, confiro e confirmo
    Então o processo volta a pré-liquidado
    E a ordem e a data da liquidação são apagadas
    E vejo a mensagem "* LIQUIDACAO ANULADA *"

  Cenário: Anulação da liquidação de processo sem a etapa
    Dado que o processo não está liquidado
    Quando marco a anulação da liquidação e transmito
    Então vejo a mensagem "* Processo nao esta liquidado *"
    E nada é gravado

  Cenário: Pagamento registrado
    Dado que o processo está liquidado
    E que informei a data e a ordem do pagamento
    Quando marco a inclusão do pagamento, confiro e confirmo
    Então o processo fica pago, com a ordem e a data do pagamento
    E vejo a mensagem "* PROCESSO PAGO *"

  Cenário: Pagamento de processo que não existe
    Dado que não existe processo com a identificação informada
    Quando marco a inclusão do pagamento e transmito
    Então vejo a mensagem "* Processo nao esta pago *"
    E nada é gravado

  Cenário: Pagamento recusado pela situação do processo
    Dado que o processo está pré-liquidado ou já está pago
    Quando marco a inclusão do pagamento e transmito
    Então vejo a mensagem "* Processo ja esta pre-liquidado *" ou
      "* Processo ja esta pago *"
    E nada é gravado

  Cenário: Anulação do pagamento devolve o processo à pré-liquidação
    Dado que o processo está pago
    Quando marco a anulação do pagamento, confiro e confirmo
    Então o processo volta a pré-liquidado
    E a ordem e a data do pagamento são apagadas, assim como a data da liquidação
    E vejo a mensagem "* PAGAMENTO ANULADO *"

  Cenário: Anulação do pagamento de processo sem a etapa
    Dado que o processo não está pago
    Quando marco a anulação do pagamento e transmito
    Então vejo a mensagem "* Processo nao esta pago *"
    E nada é gravado

  Cenário: Dado trocado entre a conferência e a confirmação
    Dado que conferi uma etapa e recebi o pedido de transmissão
    Quando mudo o número do processo, o empenho, o ano ou a marca antes de transmitir
    Então o sistema volta a conferir, em vez de gravar a etapa
    E nada é gravado

  Cenário: Uma etapa transmitida uma única vez não grava
    Dado que marquei e transmiti uma etapa
    Quando a transmissão termina com o pedido de confirmação
    Então nenhum cadastro foi incluído, alterado ou excluído

  Cenário: A reconferência do fornecedor, da secretaria e da fonte antes de gravar
    Dado que confirmei uma etapa
    E que o fornecedor do processo está excluído ou purgado, ou que a secretaria ou
      a fonte de recurso já não valem
    Quando a gravação é tentada
    Então o sistema recusa antes de gravar

  Cenário: A mudança do processo fica registrada na auditoria
    Dado que confirmei uma etapa que muda o registro do processo
    Quando a gravação termina
    Então ficam registrados o conteúdo anterior e o posterior, a tela de origem, o
      cadastro alterado, a operação, o tipo de órgão, o processo, a coordenadoria,
      a matrícula, o terminal e a data e a hora da sessão
```
