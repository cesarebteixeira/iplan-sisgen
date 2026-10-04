# US — F042T — Trocar a fonte de recurso e a conta bancária de um pagamento

## Estória

Como **servidor de CRE**, quero **trocar a fonte de recurso de um pagamento já lançado — e,
se for preciso, a conta bancária em que ele foi pago**, para que **o pagamento passe a
apontar para a fonte certa sem ter de ser lançado de novo, e as notas fiscais do processo
acompanhem a correção**.

O pagamento nasce amarrado a uma fonte de recurso e a uma conta. Quando a fonte sai errada,
corrigi-la é uma manutenção do pagamento: esta tela é a que a faz, depois de o pagamento ser
localizado pelo processo, pelo empenho e pelo ano a que se refere. Sem ela, o lançamento
teria de ser refeito, e as notas fiscais do processo continuariam contando a fonte antiga.

A tela também decide o alcance da correção: mudar a fonte do pagamento de um processo que
veio da `P211T` obriga a mudar a mesma fonte nas notas fiscais daquele processo, para que o
pagamento e as notas não se contradigam.

## Contexto

Jornada S000M → F000M → F042T.

Ator: servidor de CRE — localiza um pagamento pelo processo, pelo empenho e pelo ano de
referência, confere o que ele tem hoje e troca a fonte de recurso (e a conta) dele.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. A `F000M` não deixa dado de negócio para a
`F042T`: o contexto que a tela usa — matrícula, código de acesso, privilégio, tipo de órgão e
CRE — é o que a entrada deixou na sessão, e a `F042T` apenas o repassa às conferências de
acesso do sistema. O que a tela retoma de um uso para o outro é dela mesma (RN-04).

## Regras de negócio

### RN-01 — A tela localiza o pagamento pelo processo, pelo empenho, pelo ano e pela origem do registro

Um pagamento é identificado por quatro dados: o **número do processo** (14 dígitos), o
**número do empenho** (6 dígitos), o **ano de referência** (4 dígitos) e a **origem do
registro** — o código de seis caracteres da tela que lançou o pagamento (por exemplo, o da
`P211T`). A consulta só encontra o pagamento com os quatro informados.

### RN-02 — O número do processo é digitado em quatro caixas, e a segunda pode ficar em branco

O número do processo é digitado em quatro caixas, na ordem em que aparecem na tela: **2
dígitos**, **2 dígitos**, **6 dígitos** e **4 dígitos**. Quando a **segunda caixa** fica em
branco — ou zerada —, a tela monta o número com as duas primeiras posições zeradas e os dois
dígitos da primeira caixa passando a ocupar a **segunda dupla** do número; as outras caixas
entram nas posições seguintes. Quando a segunda caixa tem conteúdo, o número é montado na
ordem natural das quatro caixas. É o mesmo número do processo nos dois casos, e é ele que
identifica o pagamento.

### RN-03 — A tela mostra o pagamento, o fornecedor e o que a sessão traz

Localizado o pagamento, a tela mostra o que ele tem hoje: o **fornecedor** (o código e a
razão social, alcançados pelo CNPJ/CPF gravado no pagamento), o **banco**, a **agência**, a
**conta**, o **dia**, o **mês** e o **ano do pagamento**, o **valor acumulado** e a **fonte
de recurso atual**. Mostra ainda a **descrição do tipo de órgão** e a **data do sistema**,
que vêm da sessão. O cadastro dos pagamentos tem capacidade para **1.000.000** de registros
— capacidade (máximo esperado, parâmetro de dimensionamento), não volume cadastrado.

### RN-04 — A tela abre em consulta, e a abertura vem preenchida

Ao abrir, a tela assume sozinha a **consulta**, e a **primeira caixa do número do processo**
vem preenchida com um código de duas posições tirado do cadastro do **tipo de órgão da
sessão**. Se a tela já foi usada, ela retoma o **último pagamento consultado**; se não foi,
abre sem pagamento nenhum.

[?] O que a tela guarda de um uso para o outro — e de quem é o que ela guarda: do terminal,
do servidor ou só da tela — o acervo não documenta, e é isso que faz a tela reabrir no
pagamento anterior. O cadastro do tipo de órgão guarda ainda cinco outros códigos de
secretaria municipal, numerados; o que cada um representa, e por que o código que preenche a
primeira caixa é esse e não outro, também não está no acervo lido. Pergunta ao site.

### RN-05 — A tela só aceita alteração e consulta

A tela faz duas coisas: **alteração** e **consulta**. Qualquer outra opção é recusada com
**\* Operacao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da opção, e nada
é lido nem gravado — a recusa vem depois das conferências de acesso e antes de qualquer
leitura do pagamento.

[?] A mensagem nomeia as opções como **ALT** e **CON**, mas a tela confere a opção contra os
códigos internos de alteração e de consulta do sistema. Os códigos estão no acervo, e o
acervo também mostra os rótulos ALT e CON usados para essas mesmas situações num relatório de
acessos — mas nenhum fonte do lote mostra quem traduz o que o operador digita no código
conferido. Se não houver tradução, a guarda recusa toda opção, inclusive a que a mensagem
pede, e a **alteração fica inalcançável**. Pergunta ao site.

### RN-06 — A consulta exige a origem do registro

Além do processo, do empenho e do ano, a consulta exige a **origem do registro**. Sem ela, a
tela recusa e devolve o cursor ao campo da origem — a mensagem que ela mostra é a literal
**\* Informe CDISPEC \*** — e não lê o pagamento.

### RN-07 — A consulta é que habilita a alteração

A consulta lê o pagamento pela chave informada e, quando o encontra, **guarda essa chave na
tela**. É a chave guardada que a alteração exige: se a origem, o processo, o empenho ou o ano
informados na alteração forem diferentes dos que a consulta carregou, a tela recusa com
**\* Consulte antes de atualizar \***, devolve o cursor ao campo da opção e não grava nada.

### RN-08 — Pagamento que não existe manda para a N032T

Consultar um pagamento que não existe não deixa a tela vazia: a tela avisa
**\* Atualize a fonte na tela N032T \***, devolve o cursor ao campo do processo e **esquece a
chave guardada** — a alteração seguinte volta a exigir consulta.

[?] A tela manda atualizar a fonte na `N032T` quando o pagamento não existe, mas a `N032T`
grava as notas fiscais do processo, e não o pagamento. O que a tela espera que o servidor
faça lá — lançar a nota fiscal que dará origem ao pagamento, ou outra coisa — o acervo lido
não diz. Pergunta ao site.

### RN-09 — A alteração sempre troca a fonte, e a nova fonte tem de ser diferente da atual

A alteração **exige uma nova fonte**: em branco — ou zerada —, a tela recusa com
**\* Informe a fonte correta \***; e exige que ela seja **diferente da atual**: igual, a tela
recusa com **\* Altere a fonte \***. Nas duas recusas o cursor volta ao campo da nova fonte e
nada é gravado.

### RN-10 — A nova fonte tem de estar cadastrada para o tipo de órgão

A nova fonte tem de existir no cadastro de fontes do **tipo de órgão da sessão**. Se não
existir, a tela recusa com **\* Fonte nao cadastrada \***, devolve o cursor ao campo da nova
fonte e não grava nada.

### RN-11 — A troca da conta é opcional, e a nova conta tem de estar cadastrada

Sem uma nova conta informada, a tela **mantém a conta atual** do pagamento e segue sem
conferi-la no cadastro. Com uma nova conta informada, ela tem de existir no cadastro de
contas do **tipo de órgão da sessão**; se não existir, a tela recusa com
**\* Conta nao cadastrada \***, devolve o cursor ao campo da nova conta e não grava nada. A
conta que a tela lê no pagamento está na **faixa dos dígitos finais do número do processo**
— ver a dúvida da RN-03 no anexo de evidências.

### RN-12 — A alteração reescreve a fonte e a conta do pagamento, e nada mais

Passadas as conferências, a alteração reescreve no pagamento **a fonte** e **a conta** —
nada mais: o banco, a agência, a data de pagamento e o valor acumulado que a tela mostra
ficam como estavam, e o pagamento não é criado nem apagado. A tela não cria nem apaga
registro em nenhum outro cadastro.

[?] O pagamento é localizado pelo processo, pelo empenho e pelo ano: a chave não inclui o
tipo de órgão, embora o pagamento tenha esse dado, e o cadastro admite mais de um registro
com a mesma trinca. Se houver dois pagamentos do mesmo processo, empenho e ano em tipos de
órgão diferentes, a tela lê um só e não percorre os outros — e a correção fica pela metade.
Pergunta ao site.

[?] A leitura que a tela faz do pagamento não exclui os registros cuja última manutenção foi
uma exclusão, embora o mesmo cadastro tenha outra leitura que os exclui. Se um pagamento
excluído ainda puder ser alcançado por essa chave, esta tela o altera. Pergunta ao site.

### RN-13 — Cada mudança deixa rastro na auditoria

Cada alteração gera um registro no cadastro de auditoria (**A010T**) com a operação, o
cadastro de origem, o ano e o mês de referência, a data e a hora, a CRE, a matrícula, a
estação, o tipo de órgão, o número do processo e o **conteúdo anterior e o novo** do
registro. No pagamento, o conteúdo anterior e o novo diferem exatamente na fonte e na conta.

### RN-14 — Quando a origem é a P211T, a nova fonte alcança as notas fiscais do processo

Se a origem informada é a **P211T**, a nova fonte não fica só no pagamento: a tela percorre
as **notas fiscais do processo** e grava nelas a mesma fonte, e faz o mesmo em **cada item de
cada nota**. Cada nota e cada item alterados geram o seu próprio registro de auditoria. Ficam
de fora as notas fiscais e os itens cuja última manutenção foi uma exclusão. Para qualquer
outra origem, a alteração termina no pagamento.

[?] Só os registros da `P211T` recebem a propagação. Por que só ela — e o que aconteceria com
as notas fiscais de um pagamento lançado por outra tela — o acervo lido não diz. Pergunta ao
site.

[?] A leitura que percorre as notas fiscais do processo é posicionada pelo tipo de órgão,
pelo processo e pelo número da nota fiscal **zerado**, e o laço só para quando o registro
lido deixa de ser daquele processo. Se essa leitura devolve só as notas daquele processo ou
se continua para as seguintes depende da semântica de posicionamento do banco de dados, que
não está no corpus: se continuar, esta tela troca a fonte em notas fiscais de outro processo.
Pergunta ao site.

[?] O laço dos itens de cada nota fiscal não confere a que nota o item pertence — ele só para
quando não há mais registros. Se ele passar da nota corrente, altera itens de outra nota.
Pergunta ao site.

### RN-15 — Antes de cada operação o sistema confere o acesso

Toda operação passa por três conferências: a tela tem de estar cadastrada no cadastro de
telas — senão **\* Tela nao disponivel \***; o código de acesso da matrícula tem de ter a
tela autorizada — senão **\* Acesso negado para esta matricula \***; e a operação pretendida
tem de constar do perfil — senão **\* Acesso negado para esta operacao \***. A alteração
exige o direito de alteração; a consulta não exige direito nenhum.

[?] O perfil da tela guarda quatro permissões — inclusão, alteração, exclusão e consulta —,
mas a conferência só olha as três primeiras. Quem tem a tela autorizada consulta sem a
permissão de consulta. Se a intenção era exigir essa permissão por tela, o caminho não a
exige. Pergunta ao site.

### RN-16 — Os campos numéricos da página passam por edição numérica

Os **17 campos numéricos** da página passam por edição: campo em branco vira zero, o que não
for número é recusado, e o cursor volta ao primeiro campo recusado. São eles: as quatro
caixas do processo, o empenho, o ano de referência, o código do fornecedor, o banco, a
agência, a conta, o dia, o mês e o ano do pagamento, o valor acumulado, a fonte atual, a nova
fonte e a nova conta. Contagem: são os dezessete campos de conteúdo numérico declarados no
registro da tela, um a um; a descrição do tipo de órgão, a data do sistema, a razão social e
o espaço da mensagem não entram na conta porque não são numéricos.

[?] Dez desses 17 campos não têm posição de cursor declarada na tela: quando a edição recusa
um deles, não se sabe para onde o cursor volta. O que o operador vê na recusa também não está
nos fontes desta jornada — a rotina que faz a edição não faz parte do acervo lido. Pergunta ao
site.

### RN-17 — Cada mensagem começa com os campos de resultado limpos

Antes de conferir qualquer coisa, cada operação começa apagando o que a anterior tinha
mostrado fora do pagamento: a **descrição do tipo de órgão**, a **data do sistema** e a
**razão social do fornecedor**.

### RN-18 — Dos 17 campos, 7 têm posição de cursor declarada

Quando a edição numérica recusa um campo, a tela sabe para onde voltar em **7** dos 17
campos: as quatro caixas do processo (a primeira delas só é alcançada por omissão), o
empenho, o ano de referência, o código do fornecedor, a nova fonte e a nova conta. Nos
demais, o cursor não é reposicionado. Contagem: são as sete entradas de reposicionamento
declaradas na tela, uma a uma.

## Cenários BDD

```gherkin
Funcionalidade: Trocar a fonte de recurso e a conta bancária de um pagamento

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F042T

  Cenário: Consulta de um pagamento existente
    Dado que existe pagamento para o processo, o empenho e o ano informados
    Quando informo a origem do registro e peço a consulta
    Então a tela mostra o fornecedor, o banco, a agência, a conta, a data de pagamento
    E mostra o valor acumulado e a fonte de recurso atual daquele pagamento

  Cenário: A consulta não grava nada
    Dado que localizei um pagamento pela consulta
    Quando repito a consulta
    Então nenhum pagamento é criado, alterado ou apagado
    E nenhum registro de auditoria é gerado

  Cenário: Consulta sem a origem do registro
    Dado que deixo a origem do registro em branco
    Quando peço a consulta
    Então vejo a mensagem "* Informe CDISPEC *"
    E o cursor volta ao campo da origem
    E o pagamento não é lido

  Cenário: Consulta de um pagamento que não existe
    Dado que não existe pagamento para o processo, o empenho e o ano informados
    Quando peço a consulta
    Então vejo a mensagem "* Atualize a fonte na tela N032T *"
    E o cursor volta ao campo do processo
    E a tela esquece a chave que tinha guardado

  Cenário: Alteração da fonte e da conta de um pagamento
    Dado que consultei o pagamento
    Quando informo uma nova fonte e uma nova conta, ambas cadastradas para o meu tipo de órgão
    E peço a alteração
    Então o pagamento passa a ter a nova fonte e a nova conta
    E o banco, a agência, a data de pagamento e o valor acumulado continuam como estavam
    E a auditoria registra a operação com o conteúdo anterior e o novo

  Cenário: Alteração de um pagamento que não foi consultado
    Dado que não consultei o pagamento informado
    Quando peço a alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: Alteração sem a nova fonte
    Dado que consultei o pagamento
    E deixo a nova fonte em branco
    Quando peço a alteração
    Então vejo a mensagem "* Informe a fonte correta *"
    E o cursor volta ao campo da nova fonte
    E nada é gravado

  Cenário: Alteração com a mesma fonte que o pagamento já tem
    Dado que consultei o pagamento
    Quando informo, como nova fonte, a fonte que o pagamento já tem
    Então vejo a mensagem "* Altere a fonte *"
    E o cursor volta ao campo da nova fonte
    E nada é gravado

  Cenário: Nova fonte que não existe para o tipo de órgão
    Dado que consultei o pagamento
    Quando informo uma nova fonte que não está cadastrada para o meu tipo de órgão
    Então vejo a mensagem "* Fonte nao cadastrada *"
    E o cursor volta ao campo da nova fonte
    E nada é gravado

  Cenário: Nova conta que não existe para o tipo de órgão
    Dado que consultei o pagamento
    Quando informo uma nova conta que não está cadastrada para o meu tipo de órgão
    Então vejo a mensagem "* Conta nao cadastrada *"
    E o cursor volta ao campo da nova conta
    E nada é gravado

  Cenário: Alteração sem nova conta
    Dado que consultei o pagamento
    Quando informo só a nova fonte e peço a alteração
    Então o pagamento fica com a nova fonte
    E a conta do pagamento continua a mesma

  Cenário: Operação diferente de alteração e de consulta
    Quando informo uma opção diferente de ALT e de CON
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é lido nem gravado no pagamento

  Cenário: A nova fonte alcança as notas fiscais do processo
    Dado que consultei um pagamento cuja origem é a P211T
    Quando altero a fonte do pagamento
    Então as notas fiscais daquele processo ficam com a mesma fonte nova
    E cada item dessas notas também fica com a nova fonte
    E cada nota e cada item alterados deixam o seu registro de auditoria

  Cenário: Nota fiscal excluída fica de fora da propagação
    Dado que o processo tem uma nota fiscal cuja última manutenção foi uma exclusão
    Quando altero a fonte do pagamento
    Então aquela nota fiscal e os itens dela não são alterados

  Cenário: Pagamento de outra origem não propaga
    Dado que consultei um pagamento cuja origem não é a P211T
    Quando altero a fonte do pagamento
    Então o pagamento fica com a nova fonte
    E nenhuma nota fiscal é alterada

  Cenário: Número do processo com a segunda caixa em branco
    Dado que preencho a primeira caixa do processo com dois dígitos
    E deixo a segunda caixa em branco
    Quando a tela monta o número do processo
    Então esses dois dígitos passam a valer como a segunda dupla do número
    E as duas primeiras posições do número ficam zeradas

  Cenário: Número do processo com as quatro caixas preenchidas
    Dado que preencho as quatro caixas do processo
    Quando a tela monta o número do processo
    Então o número é montado na ordem das quatro caixas, sem nenhuma posição zerada

  Cenário: Abertura da tela
    Quando abro a tela
    Então ela abre em consulta
    E a primeira caixa do processo vem preenchida com o código do tipo de órgão da minha sessão
    E nada é gravado

  Cenário: A tela retoma o último pagamento consultado
    Dado que consultei um pagamento nesta sessão
    Quando abro a tela de novo
    Então ela mostra o último pagamento que consultei

  Cenário: Sem pagamento guardado, a tela abre sem pagamento
    Dado que ainda não consultei nenhum pagamento nesta sessão
    Quando abro a tela
    Então ela abre sem os dados de um pagamento

  Cenário: Tela não cadastrada
    Dado que a tela F042T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que o código de acesso da minha matrícula não tem a tela F042T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não dá o direito da operação pretendida
    Quando peço a alteração
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Digitação que não é número
    Dado que digito, num dos campos numéricos da página, algo que não é número
    Quando peço a operação
    Então o cursor volta ao primeiro campo recusado
    E a operação não é feita

  Cenário: Campo numérico em branco
    Dado que deixo um dos campos numéricos da página em branco
    Quando peço a operação
    Então a tela trata o campo como zero

  Cenário: Recusa em campo sem posição de cursor
    Dado que digito algo que não é número num campo numérico sem posição de cursor declarada
    Quando peço a operação
    Então a operação não é feita
    E o cursor não é reposicionado pela tela

  Cenário: Cada mensagem começa com os campos de resultado limpos
    Dado que a tela já mostrou a descrição do tipo de órgão, a data do sistema e o fornecedor
    Quando envio uma nova operação
    Então a descrição do tipo de órgão, a data do sistema e a razão social do fornecedor não ficam na tela
```
