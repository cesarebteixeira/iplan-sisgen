# US — F099P — Parâmetros e pedido de processamento do relatório

## Estória

Como **servidor de CRE**, quero **informar os parâmetros do relatório que escolhi e pedir o seu
processamento**, para que **o relatório saia com o recorte certo — o período, o grupo, a fonte, a
creche ou escola, o fornecedor, a nota fiscal ou o ano de competência — e não fique pedido duas
vezes na mesma fila**.

Esta é a última etapa de todo pedido de relatório do módulo. Quem escolhe o relatório é a tela
anterior; aqui ele ganha os parâmetros e entra no processamento. Sem esta etapa o relatório não
teria com que recorte rodar — rodaria vazio, ou com o recorte que outra consulta tivesse deixado na
tela.

A tela é de pedido, não de consulta: passando pelas conferências, ela grava o pedido na fila de
requisições e o encaminha ao processamento. Nenhum dos cadastros que ela lê para conferir os
parâmetros é incluído, alterado ou apagado por ela.

## Contexto

Jornada S000M → F000M → F010M → F099P.

Ator: servidor de CRE — informa os parâmetros do relatório escolhido e pede o seu processamento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

O `F000M` só encaminha: a opção dele abre o menu de relatórios `F010M`. Do `F010M` vêm as duas
coisas que esta tela usa e não pergunta de novo: **qual relatório** foi escolhido e **qual
impressora** foi informada. O resto do contexto — matrícula, código de acesso, privilégio, tipo de
órgão e CRE — é o que a entrada deixou na sessão, e a `F099P` apenas o repassa às rotinas de
segurança.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela pede o relatório: ela grava o pedido e o encaminha

A tela não consulta e não mantém cadastro: ela recebe os parâmetros do relatório e **registra o
pedido**. Passando pelas conferências, o pedido é gravado na fila de requisições do relatório —
para os relatórios que usam esse registro — e, em seguida, encaminhado ao processamento. A gravação
é uma inclusão: a requisição nasce nova, com o número seguinte ao último já usado.

Dos dez cadastros que a tela enxerga, **um só** é gravado: a fila de requisições. Os outros nove —
telas, funcionários, acumulados, pagamentos, notas fiscais, valores convertidos, escolas, processos
e grupos — são apenas lidos para conferir os parâmetros.

Seis dos relatórios que a tela atende não passam por essa gravação: o pedido deles vai direto ao
processamento, sem registro na fila.

[?] Está declarado, para os dez cadastros, o caminho de inclusão, de exclusão e de trava, mas só o
da fila de requisições é executado. Se algum deles deveria ser usado — por exemplo, apagar uma
requisição antiga do mesmo relatório —, o acervo não diz.

### RN-02 — O relatório vem escolhido da etapa anterior e define o que a tela pede

Quem escolhe o relatório é a etapa anterior, que também deixa a impressora já informada: a tela não
pergunta nenhuma das duas coisas. Ao abrir, a tela libera apenas os campos do conjunto de
parâmetros daquele relatório, marca os que ele exige, protege os demais e deixa o cursor no
primeiro campo do conjunto.

São onze conjuntos de parâmetros: a referência inicial, a referência limite, a fonte, a
creche/escola, o grupo, o início do período, o limite do período, o fornecedor, a escola, a nota
fiscal e a competência. Nenhum relatório pede os onze.

Nesta jornada o relatório chega escolhido pela tela de relatórios do módulo (a `F010M`), que passa
o registro e a operação sem passar por menu. Os relatórios que pedem grupo, escola e competência
chegam escolhidos por outra tela do mesmo módulo.

[?] Se o relatório escolhido não for um dos que a tela conhece, ela não libera parâmetro nenhum,
não grava e **não avisa**: a tela fica sem ação, sem mensagem. O acervo não diz se esse caminho
acontece na prática nem se a intenção era avisar.

[?] Quais conjuntos cada relatório libera é o que o programa faz; os rótulos e a ordem em que os
campos aparecem ao operador estão na máscara da tela, que não faz parte do lote lido.

### RN-03 — O período de referência: os dois campos, o mesmo ano e o limite não anterior

Nos relatórios que usam o mês e o ano de referência, os dois têm de estar informados: em branco, a
recusa é **\* Informe mes/ano de referencia \***, com o cursor de volta ao campo do mês.

Nos relatórios que também pedem o mês e o ano de referência limite, o **ano limite tem de ser o
mesmo ano do inicial** — ano diferente é recusado com
**\* Utilize o mesmo ano para o periodo \***, com o cursor no campo do ano limite — e o **mês limite
não pode ser anterior ao mês inicial**, senão a recusa é **\* Periodo invalido \***, com o cursor no
campo do mês limite. Deixando o ano limite em branco, a tela assume o mês e o ano iniciais e segue.

[?] No relatório cujos parâmetros são só o ano de competência das notas fiscais, a tela também
preenche a referência limite quando ela vem em branco — e não a usa em nada depois. Se esse
preenchimento deveria valer para alguma conferência, o acervo não diz.

### RN-04 — O período em datas: duas datas válidas, de 1994 a 2099, e o limite não anterior

No relatório cujos parâmetros são o período em datas (dia, mês e ano de início e limite), as duas
datas passam por conversão antes de qualquer leitura. Data de início que não fecha é recusada com
**\* Dt inicio invalida \*** e data limite que não fecha, com **\* Dt limite invalida \***, o
cursor voltando ao campo do dia correspondente. Só o ano de **1994 a 2099** é aceito: fora dessa
faixa a mesma recusa aparece.

As duas datas também são comparadas: data limite **anterior** à data de início é recusada com
**\* Dt limite < Dt inicio \***, com o cursor de volta ao campo do dia de início.

[?] A tela calcula o ano corrente a partir da data do dia e não o compara com a data informada em
nenhum ponto: a única faixa aplicada ao ano é a de 1994 a 2099. Se a intenção era recusar data
futura, o caminho não confere.

### RN-05 — A fonte escolhe os acumulados e a creche/escola tem de ser C ou E

No relatório cujo recorte é o acumulado da fonte, é esse código que seleciona os valores acumulados
lidos na conferência: a tela procura os acumulados da fonte informada dentro do período de referência
pedido. O código da fonte não é conferido contra um cadastro de fontes — o que existe para conferir
é o acumulado; nos outros relatórios que pedem a fonte, ela é apenas levada ao pedido. Se o acumulado
encontrado tiver referência posterior ao limite pedido, a recusa é
**\* Nao existem registros para os dados informados \***.

O campo de creche/escola aceita **"C"** (creche) ou **"E"** (escola). Qualquer outro conteúdo é
recusado com **\* Informe creche/escola com C ou E \***, com o cursor no campo.

### RN-06 — O grupo tem de ser informado, cadastrado e o do próprio servidor

Nos relatórios que pedem o grupo, ele é obrigatório: em branco, a recusa é **\* Informe o grupo \***
e o cursor volta ao campo. Nos relatórios em que a tela também confere o cadastro de grupos, o grupo
informado tem de existir — não existindo, a recusa é **\* Grupo nao cadastrado \***.

O servidor que **tem grupo na sessão** — isto é, o vínculo dele com a secretaria define uma
coordenação — só pode pedir o próprio grupo: informando outro, a recusa é
**\* Usuario sem acesso a outro grupo \***, com o cursor no campo do grupo. O servidor que não tem
grupo na sessão pode pedir qualquer grupo.

[?] Um dos relatórios que pedem grupo não confere o cadastro de grupos: o grupo informado só é
confrontado com a escola. Se ali o grupo deveria ser conferido como nos outros, o caminho não
existe. Pergunta ao site.

[?] Para um dos relatórios, o valor **99** significa "todos os grupos": nesse caso a tela dispensa a
conferência do cadastro e mostra "Todos=99" ao lado do campo. Os outros relatórios que pedem grupo
não têm esse atalho, e a tela não avisa o operador de que ali o 99 não vale. Se a intenção era
aceitar "todos os grupos" em todos, o caminho não existe.

### RN-07 — A escola tem de ser informada, cadastrada e do grupo informado

No relatório que pede a escola pelo código da escola, o código é obrigatório: em branco, a recusa é
**\* Informe o INEP \***. O código tem de existir no cadastro de escolas — não existindo, a recusa é
**\* INEP nao cadastrado \*** — e a escola cadastrada tem de pertencer ao **grupo informado**;
sendo de outro grupo, a recusa é **\* INEP nao pertence a este grupo \***.

### RN-08 — A nota fiscal: uma nota específica ou todas as notas do período

A nota fiscal pode ser pedida de duas formas.

**Por uma nota específica:** o número tem de estar cadastrado para o fornecedor e o ano inicial
informados; não estando, a recusa é **\* Nota Fiscal nao cadastrada \***, com o cursor no campo da
nota. Nesse caminho o **CNPJ do fornecedor** e o **ano inicial do período** passam a ser
obrigatórios: sem o CNPJ, a recusa é **\* Informe o CNPJ do fornecedor \***; sem o ano, é
**\* Informe ano inicial do periodo \***.

**Por todas as notas:** informando o valor especial que significa "todas" no campo da nota, a tela
procura as notas lançadas para o grupo dentro do período informado e aceita a nota do fornecedor
informado **ou** a da escola informada; não achando nenhuma, a recusa é
**\* Nao existem registros para este periodo \***.

Ao lado dos campos que representam "todos", a tela escreve o texto que diz qual valor significa
isso.

[?] O CNPJ do fornecedor é alfanumérico e **não** passa pela edição numérica; a guarda que exige o
CNPJ o compara com zeros. Deixando o campo em branco, a mensagem **\* Informe o CNPJ do
fornecedor \*** pode não aparecer e a tela segue até recusar por nota não cadastrada. Se o campo em
branco deveria ser recusado como "não informado", é pergunta ao site.

[?] O valor especial que significa "todas" aparece ao lado do campo como texto — a tela não o
escreve no campo. Se a máscara não o trouxer preenchido, o operador que não digitar o valor especial
pede, sem querer, a nota de número zero. Pergunta ao site.

### RN-09 — O ano de competência tem de ser informado

Nos relatórios que pedem o ano de competência, ele é obrigatório: em branco, a recusa é
**\* Informe ano de competencia \***, com o cursor de volta ao campo.

### RN-10 — Só há pedido se houver dado para o recorte, e cada conjunto tem a sua recusa

Antes de gravar, a tela confere se existe dado para o recorte informado. A conferência e a recusa
mudam com o conjunto de parâmetros do relatório:

| o que o pedido usa | o que a tela confere | a recusa |
| --- | --- | --- |
| só o mês e o ano de referência | nada | — |
| mês e ano de referência, no relatório de pagamentos | há pagamento lançado no mês e ano de referência, quando o tipo de órgão da sessão é 01; nos outros tipos de órgão, há processo lançado no mês e ano | **\* Nao existem pagamentos para este mes \*** |
| ano e mês de referência, fonte e creche/escola | há acumulado da fonte informada com referência até o limite pedido | **\* Nao existem registros para os dados informados \*** |
| referência inicial e limite | há pagamento lançado no **mês e ano iniciais** do período | **\* Nao existem registros para este periodo \*** |
| ano de referência, fonte e creche/escola | há pagamento lançado no ano informado | **\* Nao existem registros para o ano informado \*** |
| grupo, período em datas, fornecedor, escola e nota | a nota fiscal, conforme a RN-08 | as da RN-08 |
| grupo e ano de competência | há valor convertido lançado para o grupo no ano | **\* Nao existem registros para este ano compet.\*** |
| grupo, escola e ano de competência | há nota fiscal do grupo e da escola no ano | **\* Nao existem registros para este ano compet.\*** |
| só o ano de competência (notas fiscais) | há nota fiscal lançada no ano | **\* Nao existem registros para este ano compet.\*** |
| só o ano de competência (pagamentos) | há pagamento lançado no ano | **\* Nao existem registros para este ano \*** |

[?] As conferências procuram os lançamentos completando parte da chave com zeros — a fonte e o
número do processo, nos pagamentos; o grupo, a escola e o fornecedor, em outros casos. Se a procura
for pela chave inteira, esses zeros teriam de existir no lançamento gravado e **nenhum** destes
pedidos passaria; se for pelo começo da chave, a tela acha os lançamentos do recorte informado. Como
as duas leituras levam a resultados opostos, o acervo não decide. Pergunta ao site.

[?] No relatório cuja conferência é de pagamento no mês inicial do período, a recusa fala do
"período", mas a conferência só olha o **mês e o ano iniciais** — o mês limite não participa. Se a
intenção era exigir dado em todo o período, o caminho não confere o limite. Pergunta ao site.

### RN-11 — Um pedido por relatório: a fila recusa o pedido repetido

Antes de gravar, a tela confere se já existe pedido do mesmo relatório na fila. Existindo, a recusa
é **\* Relatorio ja esta em processamento. Aguarde. \*** e nada é gravado.

Nos relatórios cujo pedido é identificado também pelo grupo, a conferência é pelo **relatório e
grupo**, e a recusa é **\* Relatorio em processamento. Aguarde. \***, com o cursor no campo do grupo.

[?] Em quatro relatórios a procura do pedido na fila é feita com o número da requisição **zerado**,
enquanto o pedido gravado tem um número real; e um deles confere a fila pelo relatório e o grupo,
mas nunca grava requisição — a conferência dele nunca encontra nada. Se a procura for pela chave
completa, a recusa por pedido repetido nunca acontece nesses casos; se for pelo começo da chave, ela
funciona. Como as duas leituras levam a resultados diferentes, o acervo não decide. Pergunta ao
site.

### RN-12 — O pedido registrado guarda o relatório, os parâmetros e quem pediu

O pedido gravado na fila guarda: o **relatório**, a **impressora** informada na etapa anterior, a
**estação**, a **matrícula** do servidor, o **dia, o mês e o ano da sessão**, o **tipo de órgão**, o
**grupo** — o informado, nos relatórios que o pedem; nos que não pedem grupo, o valor que o próprio
programa fixa —, o **número da requisição**, que é o seguinte ao último já usado, e a **cadeia de
parâmetros** do relatório. A requisição nasce marcada como **inclusão**.

Além do registro na fila, o pedido é encaminhado ao processamento levando o relatório, a impressora,
a estação, a matrícula, o e-mail do servidor (lido do cadastro do funcionário) e **uma cópia** — a
tela não pergunta o número de cópias: ele é fixo em uma.

[?] O registro da fila não leva o e-mail do servidor, e a tela não confere se o relatório tem e-mail
cadastrado. Se algum relatório depende de ser avisado por e-mail, esse dado só existe no
encaminhamento. Pergunta ao site.

### RN-13 — Os quinze campos numéricos passam por edição antes de qualquer conferência

Quinze campos passam pela edição numérica antes de qualquer conferência: o mês e o ano de referência
inicial, o mês e o ano de referência limite, o código da fonte, o grupo, o dia, o mês e o ano do
início do período, o dia, o mês e o ano do limite, o código da escola, o número da nota fiscal e o
ano de competência. Em treze deles a tela trata o campo em branco como **zero** antes de editá-lo;
nos dois anos do período em datas — o ano de início e o ano limite — esse tratamento não aparece. O
que não for número é recusado e a operação não é feita, com o cursor de volta ao **primeiro** campo
recusado.

Ficam de fora dessa edição o CNPJ do fornecedor (alfanumérico) e o campo de creche/escola (uma
letra).

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não está nos
fontes desta jornada: a rotina que faz a edição não faz parte do lote lido. Pergunta ao site.

[?] Nos dois campos de ano em que a tela não trata o branco como zero, e também no CNPJ do
fornecedor (que não passa por edição), a guarda que exige o campo o compara com zeros: um campo em
branco não é zeros. Se a rotina de edição converter o branco em zeros, o aviso sai; se o deixar em
branco, a tela segue e recusa adiante. O acervo não diz o que a rotina faz. Pergunta ao site.

### RN-14 — Antes de processar, a tela confere a tela, a matrícula, o relatório, a estação e a rota

Toda mensagem passa por conferências com o contexto da sessão — matrícula, código de acesso,
privilégio, tipo de órgão e CRE. Na abertura e no momento do pedido:

- a tela `F099P` tem de estar cadastrada: não estando, a recusa é **\* Tela nao disponivel \*** e a
  tela não abre;
- a matrícula tem de ter a tela `F099P` autorizada no seu código de acesso: não tendo, a recusa é
  **\* Acesso negado para esta matricula \***;
- o relatório escolhido também tem de estar cadastrado e autorizado no código de acesso da
  matrícula: não estando cadastrado, a tela **encerra sem avisar nada**; não estando autorizado, a
  recusa é **\* Acesso negado para esta matricula \***;
- a sessão tem de estar na mesma estação em que foi aberta: não estando, a sessão é encerrada, sem
  mensagem;
- a tela passa ainda pela lógica de rota, que decide entre seguir, voltar para a tela de origem e
  encerrar a sessão.

[?] A recusa "operação não disponível" existe na rotina de rota, mas depende de um campo que a
máscara preenche — e o programa desta tela não o preenche. Como a máscara não faz parte do lote
lido, não dá para dizer qual operação o operador tem autorizada aqui, nem se esta tela abre em
consulta ou em inclusão.

[?] A rotina de rota volta para a tela de origem quando o campo que a identifica vem preenchido, e
essa volta acontece antes de o pedido ser processado. Se a máscara desta tela traz a tela de origem
preenchida, o pedido nunca é gravado; o lote lido não mostra a máscara. Pergunta ao site.

### RN-15 — O que a tela mostra sem perguntar

Fora dos campos de parâmetro, a tela mostra o **tipo de órgão** e a **data do sistema** da sessão, e
escreve ao lado dos campos que representam "todos" o texto que diz o que aquele valor significa.
Esses dados da sessão são apenas apresentados: a tela não os recalcula.

[?] A tela tem campos de descrição ao lado do grupo, do fornecedor, da escola e da nota fiscal, mas
não os preenche: só os limpa a cada digitação. Se a máscara os preenche por outro caminho, o lote
lido não mostra. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Parâmetros e pedido de processamento do relatório

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F099P

  Cenário: A tela pede só os parâmetros do relatório escolhido
    Dado que o relatório escolhido na etapa anterior usa o mês e o ano de referência
    Quando abro a tela F099P
    Então os campos de referência inicial ficam disponíveis e marcados como obrigatórios
    E os demais parâmetros ficam protegidos
    E o cursor fica no primeiro campo do conjunto
    E nada é gravado na abertura da tela

  Cenário: Tipo de órgão e data do sistema são mostrados na abertura
    Quando abro a tela F099P
    Então vejo o tipo de órgão e a data do sistema que a minha sessão tem
    E a tela não os recalcula

  Cenário: Pedido registrado para um relatório de período de referência
    Dado que o relatório escolhido pede referência inicial e limite, fonte e creche/escola
    E existe acumulado da fonte informada com referência dentro do período
    E informo a creche "C"
    Quando informo o mês e o ano de referência inicial e limite, o código da fonte e peço o relatório
    Então o pedido é encaminhado ao processamento
    E nenhuma requisição é gravada na fila

  Cenário: Pedido registrado para um relatório de pagamentos por ano de referência
    Dado que o relatório escolhido usa o ano de referência, a fonte e a creche/escola
    E existe pagamento lançado no ano informado
    Quando informo a referência inicial, o código da fonte, a creche "E" e peço o relatório
    Então o pedido é encaminhado ao processamento

  Cenário: Pedido registrado para um relatório de referência e limite
    Dado que o relatório escolhido usa a referência inicial e limite
    E existe pagamento lançado no mês e ano iniciais do período
    Quando informo o período e peço o relatório
    Então o pedido é gravado na fila de requisições
    E o número da requisição é o seguinte ao último já usado
    E a requisição nasce marcada como inclusão
    E o pedido é encaminhado ao processamento

  Cenário: Pedido registrado para um relatório de grupo e competência
    Dado que o relatório escolhido usa o grupo e o ano de competência
    E existe valor convertido lançado para o grupo no ano informado
    Quando informo o grupo, o ano de competência e peço o relatório
    Então o pedido é gravado na fila de requisições
    E a requisição leva o relatório, a impressora da etapa anterior, a estação, a minha matrícula,
      a data da sessão, o tipo de órgão, o grupo e a cadeia de parâmetros
    E o pedido é encaminhado ao processamento levando uma cópia e o meu e-mail

  Cenário: Pedido registrado para um relatório de grupo, escola e competência
    Dado que o relatório escolhido usa o grupo, a escola e o ano de competência
    E existe nota fiscal do grupo e da escola no ano informado
    Quando informo o grupo, o código da escola, o ano de competência e peço o relatório
    Então o pedido é gravado na fila de requisições
    E o pedido é encaminhado ao processamento

  Cenário: Pedido registrado para um relatório de competência dos pagamentos
    Dado que o relatório escolhido usa só o ano de competência dos pagamentos
    E existe pagamento lançado no ano informado
    Quando informo o ano de competência e peço o relatório
    Então o pedido é gravado na fila de requisições
    E o pedido é encaminhado ao processamento

  Cenário: Pedido recusado não grava nada
    Dado que os parâmetros informados não encontram dado na conferência
    Quando peço o relatório
    Então vejo a mensagem de recusa do conjunto de parâmetros
    E nenhuma requisição é gravada
    E nenhum dos cadastros que a tela lê é incluído, alterado ou apagado

  Cenário: Relatório que só encaminha ao processamento
    Dado que o relatório escolhido é um dos que não registram requisição na fila
    Quando informo os parâmetros e peço o relatório
    Então o pedido é encaminhado ao processamento
    E nenhuma requisição é gravada na fila

  Cenário: Referência em branco
    Dado que deixo o mês e o ano de referência em branco
    Quando peço o relatório
    Então vejo a mensagem "* Informe mes/ano de referencia *"
    E o cursor volta ao campo do mês de referência
    E nada é gravado

  Cenário: Ano limite diferente do ano inicial
    Dado que o relatório pede a referência inicial e limite
    E informo um ano limite diferente do ano inicial
    Quando peço o relatório
    Então vejo a mensagem "* Utilize o mesmo ano para o periodo *"
    E o cursor volta ao campo do ano limite
    E nada é gravado

  Cenário: Mês limite anterior ao mês inicial
    Dado que o relatório pede a referência inicial e limite
    E informo o mês limite anterior ao mês inicial, no mesmo ano
    Quando peço o relatório
    Então vejo a mensagem "* Periodo invalido *"
    E o cursor volta ao campo do mês limite
    E nada é gravado

  Cenário: Ano limite em branco assume a referência inicial
    Dado que o relatório pede a referência inicial e limite
    E deixo o ano limite em branco
    Quando informo a referência inicial e peço o relatório
    Então a tela assume o mês e o ano iniciais como limite
    E segue com a conferência do período

  Cenário: Data de início que não existe
    Dado que o relatório pede o período em datas
    E informo uma data de início que não fecha
    Quando peço o relatório
    Então vejo a mensagem "* Dt inicio invalida *"
    E o cursor volta ao campo do dia de início
    E nada é gravado

  Cenário: Data limite que não existe
    Dado que o relatório pede o período em datas
    E informo uma data limite que não fecha
    Quando peço o relatório
    Então vejo a mensagem "* Dt limite invalida *"
    E o cursor volta ao campo do dia limite
    E nada é gravado

  Cenário: Data limite anterior à data de início
    Dado que o relatório pede o período em datas
    E informo uma data limite anterior à data de início
    Quando peço o relatório
    Então vejo a mensagem "* Dt limite < Dt inicio *"
    E o cursor volta ao campo do dia de início
    E nada é gravado

  Cenário: Ano fora da faixa aceita
    Dado que o relatório pede o período em datas
    E informo um ano anterior a 1994 ou posterior a 2099
    Quando peço o relatório
    Então vejo a mensagem de data inválida do campo
    E nada é gravado

  Cenário: Sem acumulado da fonte no período informado
    Dado que não existe acumulado da fonte informada com referência dentro do período
    Quando peço o relatório de referência, fonte e creche
    Então vejo a mensagem "* Nao existem registros para os dados informados *"
    E nada é gravado

  Cenário: Creche/escola fora de C e E
    Dado que informo no campo de creche/escola algo diferente de "C" e de "E"
    Quando peço o relatório
    Então vejo a mensagem "* Informe creche/escola com C ou E *"
    E o cursor volta ao campo de creche/escola
    E nada é gravado

  Cenário: Grupo em branco
    Dado que o relatório pede o grupo e deixo o campo em branco
    Quando peço o relatório
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nada é gravado

  Cenário: Grupo não cadastrado
    Dado que informo um grupo que não existe no cadastro de grupos
    Quando peço o relatório
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo do grupo
    E nada é gravado

  Cenário: Servidor com grupo próprio informa outro grupo
    Dado que o meu vínculo define um grupo
    E informo um grupo diferente do meu
    Quando peço o relatório
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo do grupo
    E nada é gravado

  Cenário: O valor 99 dispensa a conferência do grupo
    Dado que o relatório admite "todos os grupos" no valor 99
    Quando informo o grupo 99
    Então a tela dispensa a conferência do cadastro de grupos
    E mostra "Todos=99" ao lado do campo

  Cenário: Escola em branco
    Dado que o relatório pede a escola e deixo o código em branco
    Quando peço o relatório
    Então vejo a mensagem "* Informe o INEP *"
    E o cursor volta ao campo da escola
    E nada é gravado

  Cenário: Escola não cadastrada
    Dado que informo um código de escola que não existe
    Quando peço o relatório
    Então vejo a mensagem "* INEP nao cadastrado *"
    E o cursor volta ao campo da escola
    E nada é gravado

  Cenário: Escola de outro grupo
    Dado que informo uma escola cadastrada em outro grupo
    Quando peço o relatório
    Então vejo a mensagem "* INEP nao pertence a este grupo *"
    E o cursor volta ao campo da escola
    E nada é gravado

  Cenário: Nota fiscal específica sem o CNPJ do fornecedor
    Dado que informo o número de uma nota fiscal específica
    E o CNPJ do fornecedor está zerado
    Quando peço o relatório
    Então vejo a mensagem "* Informe o CNPJ do fornecedor *"
    E o cursor volta ao campo do fornecedor
    E nada é gravado

  Cenário: Nota fiscal específica sem o ano inicial do período
    Dado que informo o número de uma nota fiscal e o CNPJ do fornecedor
    E o ano inicial do período está zerado
    Quando peço o relatório
    Então vejo a mensagem "* Informe ano inicial do periodo *"
    E o cursor volta ao campo do ano de início
    E nada é gravado

  Cenário: Nota fiscal específica não cadastrada
    Dado que informo uma nota fiscal que não está cadastrada para o fornecedor e o ano informados
    Quando peço o relatório
    Então vejo a mensagem "* Nota Fiscal nao cadastrada *"
    E o cursor volta ao campo da nota fiscal
    E nada é gravado

  Cenário: Todas as notas sem nenhuma nota no período
    Dado que informo o valor especial que significa todas as notas
    E não existe nota fiscal do grupo lançada dentro do período informado
    Quando peço o relatório
    Então vejo a mensagem "* Nao existem registros para este periodo *"
    E nada é gravado

  Cenário: Ano de competência em branco
    Dado que o relatório pede o ano de competência e deixo o campo em branco
    Quando peço o relatório
    Então vejo a mensagem "* Informe ano de competencia *"
    E o cursor volta ao campo do ano de competência
    E nada é gravado

  Cenário: Sem pagamento no mês e ano de referência
    Dado que o relatório confere pagamento no mês e ano de referência
    E o tipo de órgão da minha sessão é 01
    E não existe pagamento lançado nesse mês e ano
    Quando peço o relatório
    Então vejo a mensagem "* Nao existem pagamentos para este mes *"
    E o cursor volta ao campo do mês de referência
    E nada é gravado

  Cenário: Sem processo no mês e ano de referência, fora do tipo de órgão 01
    Dado que o relatório confere pagamento no mês e ano de referência
    E o tipo de órgão da minha sessão não é 01
    E não existe processo lançado nesse mês e ano
    Quando peço o relatório
    Então vejo a mensagem "* Nao existem pagamentos para este mes *"
    E nada é gravado

  Cenário: Sem pagamento no ano de referência
    Dado que o relatório confere pagamento no ano de referência
    E não existe pagamento lançado nesse ano
    Quando peço o relatório
    Então vejo a mensagem "* Nao existem registros para o ano informado *"
    E nada é gravado

  Cenário: Sem pagamento no mês inicial do período
    Dado que o relatório confere pagamento no mês e ano iniciais do período
    E não existe pagamento lançado nesse mês e ano
    Quando peço o relatório
    Então vejo a mensagem "* Nao existem registros para este periodo *"
    E nada é gravado

  Cenário: Sem valor convertido para o grupo no ano de competência
    Dado que não existe valor convertido lançado para o grupo no ano de competência informado
    Quando peço o relatório de grupo e ano de competência
    Então vejo a mensagem "* Nao existem registros para este ano compet.*"
    E o cursor volta ao campo do ano de competência
    E nada é gravado

  Cenário: Sem nota fiscal para o grupo e a escola no ano de competência
    Dado que não existe nota fiscal do grupo e da escola no ano de competência informado
    Quando peço o relatório de grupo, escola e ano de competência
    Então vejo a mensagem "* Nao existem registros para este ano compet.*"
    E nada é gravado

  Cenário: Sem nota fiscal no ano de competência
    Dado que não existe nota fiscal lançada no ano de competência informado
    Quando peço o relatório de ano de competência das notas fiscais
    Então vejo a mensagem "* Nao existem registros para este ano compet.*"
    E o cursor volta ao campo do ano de competência
    E nada é gravado

  Cenário: Sem pagamento no ano de competência
    Dado que não existe pagamento lançado no ano de competência informado
    Quando peço o relatório de ano de competência dos pagamentos
    Então vejo a mensagem "* Nao existem registros para este ano *"
    E o cursor volta ao campo do ano de competência
    E nada é gravado

  Cenário: Pedido repetido do mesmo relatório
    Dado que já existe um pedido do mesmo relatório na fila
    Quando peço o relatório
    Então vejo a mensagem "* Relatorio ja esta em processamento. Aguarde. *"
    E nenhuma requisição nova é gravada

  Cenário: Pedido repetido do mesmo relatório e grupo
    Dado que o relatório tem o pedido identificado pelo grupo
    E já existe um pedido desse relatório para o grupo informado
    Quando peço o relatório
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo do grupo
    E nenhuma requisição nova é gravada

  Cenário: Campo numérico recusado
    Dado que digito letras em um dos campos numéricos
    Quando peço o relatório
    Então a operação não é feita
    E o cursor volta ao primeiro campo recusado
    E nada é gravado

  Cenário: Tela não cadastrada
    Dado que a tela F099P não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo pedir o relatório

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela F099P autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo pedir o relatório

  Cenário: Sem autorização para o relatório escolhido
    Dado que a minha matrícula tem a tela F099P autorizada
    E não tem o relatório escolhido autorizado no seu código de acesso
    Quando abro a tela F099P
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo pedir o relatório

  Cenário: Relatório escolhido não cadastrado
    Dado que o relatório escolhido não está no cadastro de telas
    Quando abro a tela F099P
    Então a tela encerra sem me avisar nada
    E não consigo pedir o relatório

  Cenário: Sessão aberta em outra estação
    Dado que a minha sessão foi aberta em outra estação
    Quando abro a tela F099P
    Então a sessão é encerrada
    E não consigo pedir o relatório
```
