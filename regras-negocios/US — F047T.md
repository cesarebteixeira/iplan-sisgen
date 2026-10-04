# US — F047T — Manter o documento de pagamento das datas do ano

## Estória

Como **servidor de CRE**, quero **registrar e manter, para cada data de pagamento de um
ano, o número do documento e o valor acumulado que a ela correspondem**, para que **os
pagamentos da secretaria fiquem amarrados ao documento certo e possam ser conferidos
pela data em que foram pagos**.

O pagamento é lançado pela secretaria por data e por tipo de órgão, e é o documento que
dá à data o número pelo qual ela é conhecida. Sem esse número, os pagamentos de um dia
ficam sem documento, e a conferência do que foi pago em cada data não tem por onde
começar.

A tela também confere o valor: não deixa gravar um valor acumulado diferente da soma dos
pagamentos daquela data e recusa incluir uma data para a qual não exista pagamento
lançado. E toda mudança fica registrada na auditoria, com o que havia antes e o que
passou a valer.

## Contexto

Jornada S000M → F000M → F047T.

Ator: servidor de CRE — registra e mantém, por data de pagamento, o documento e o valor
acumulado do ano, conferindo-os contra os pagamentos lançados.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A `F000M` é um menu: ela abre a `F047T` e não lhe passa registro nem operação. O que a
`F047T` usa é o contexto que a **entrada** deixou na sessão — a matrícula, o código de
acesso, o privilégio, a CRE e o tipo de órgão —, e ela não recalcula nada disso. Não há
nesta tela nenhuma decisão que dependa da tela de origem: o comportamento da `F047T` não
muda conforme quem a chamou.

A `F047T` é o fim da jornada e não leva a outra tela por si. A máscara tem um campo de
**próxima tela** que, se vier preenchido de fora, desvia a sessão antes de qualquer
leitura de documento — isso é navegação, e não regra de negócio.

## Regras de negócio

### RN-01 — O que a tela mantém por data de pagamento

Dentro de um **ano de pagamento** (4 dígitos), cada **data de pagamento** — **dia** (2
dígitos) e **mês** (2 dígitos) — tem um **número de documento** (18 dígitos) e um
**valor acumulado** (até 10 inteiros e 2 decimais, com vírgula). Fora do corpo da
página, a tela mostra o **total do ano**, a **data do sistema** e a **descrição do tipo
de órgão** da sessão. O cadastro dos documentos tem capacidade para **10.000** registros
— capacidade (máximo esperado, parâmetro de dimensionamento), não volume cadastrado.

[?] Ao abrir depois de já ter sido usada, a tela mostra o ano que ela mesma carregou no
uso anterior; só no primeiro uso o ano é o anterior ao do sistema. O que a tela guarda
de um uso para o outro — se é por servidor, por estação ou só pela própria tela — o
acervo não diz. Pergunta ao site.

### RN-02 — A página tem 11 datas e o total do ano

A página comporta até **11 datas**. O **total do ano** aparece uma vez e é refeito,
somando os documentos do ano, depois de cada operação — inclusive na consulta. Quando o
ano que a tela carregou não tem documento nenhum, ela avisa
**\* Nao existem documentos cadastrados \***.

[?] A soma percorre os documentos a partir do ano carregado, mas não confere o ano de
cada documento antes de somar; se a leitura atravessar a virada do ano, o total deixa de
ser o do ano. A semântica da leitura do cadastro não está no acervo lido. Pergunta ao
site.

### RN-03 — A situação da linha decide a operação

Cada data da página tem uma **situação**, de um caractere: **I** inclui, **A** altera e
**E** exclui a data daquela linha. Linha sem dia, ou com situação diferente de I, A e E,
é ignorada: não gera operação nem mensagem.

### RN-04 — A tela abre em consulta e só aceita alteração e consulta

Ao abrir, a tela assume sozinha a **consulta**. Se a opção de manutenção informada for
diferente de **alteração** e de **consulta**, o sistema recusa com
**\* Opcao nao disponivel. Use ALT ou CON \*** e devolve o cursor ao campo da opção. A
recusa vem depois das conferências de acesso e antes de qualquer leitura do documento ou
dos pagamentos.

[?] A mensagem nomeia as opções como **ALT** e **CON**, mas a tela confere a opção contra
códigos internos de manutenção que o acervo não traduz para os rótulos da máscara. Se o
que o operador digita e o que a tela confere não forem o mesmo vocabulário, a recusa
alcança toda opção e a manutenção fica inalcançável. Pergunta ao site.

### RN-05 — A consulta não grava nada

Em consulta, nada é incluído, alterado ou excluído — nem o documento, nem os pagamentos
— e nenhum registro de auditoria é gerado, seja qual for a situação marcada nas linhas.
A tela apenas relê os documentos do ano para refazer o total.

### RN-06 — A alteração exige o ano informado

Com o ano de pagamento em branco — ou zerado —, a alteração é recusada com
**\* Informe o ano dos pagamentos \***, o cursor volta ao campo do ano e nada é gravado.
O campo em branco é tratado como zero antes da conferência.

### RN-07 — A alteração só vale para o ano já consultado

A alteração só vale para o ano que a tela já carregou. Se o ano informado for outro, a
tela recusa com **\* Consulte o ano antes de atualizar \***, devolve o cursor ao campo do
ano e não grava nada. É a consulta que guarda o ano na tela: consultar o ano passa a ser
o que habilita alterá-lo.

### RN-08 — Data já cadastrada não pode ser incluída

Ao incluir uma data que já tem documento, a tela recusa com **\* Dia ja cadastrado \***
e devolve o cursor ao campo da situação. Nada é gravado.

### RN-09 — Data sem pagamento não pode ser incluída

Ao incluir uma data que não tem nenhum pagamento lançado, a tela recusa com
**\* Nao existe pagamento para esta data \*** e devolve o cursor ao campo do dia. Nada é
gravado.

### RN-10 — Sem o número do documento não há inclusão nem alteração

Inclusão e alteração exigem o número do documento. Sem ele, a tela recusa com
**\* Informe o numero do documento \*** e devolve o cursor ao campo do número. Nada é
gravado.

### RN-11 — O valor acumulado tem de bater com a soma dos pagamentos da data

Na inclusão, a tela soma os pagamentos do **tipo de órgão da sessão**, do ano e do mês
da linha, cujo **dia de pagamento** é o da linha, e só os da conta **78999**. O valor
acumulado informado tem de ser igual a essa soma; sendo diferente, a tela recusa com
**<- Valor do documento incorreto \*** e devolve o cursor ao campo do valor. Nada é
gravado.

[?] A busca dos pagamentos posiciona pela chave do tipo de órgão, do ano e do mês, com
dois componentes da chave zerados (a fonte e o processo), e depois percorre comparando só
os três primeiros. Se a leitura exigir a chave inteira, só entrariam os pagamentos com
fonte e processo zerados, e não todos os do órgão, ano e mês. A semântica da leitura não
está no acervo lido. Pergunta ao site.

### RN-12 — Data não cadastrada não pode ser alterada nem excluída

Alterar ou excluir uma data que não tem documento é recusado com
**\* Dia nao cadastrado \***, com o cursor de volta ao campo da situação. Nada é
gravado.

### RN-13 — A inclusão grava o documento e leva o número aos pagamentos

Passadas as conferências, a inclusão cria o documento daquela data com o número e o
valor informados e grava esse mesmo número em todos os pagamentos daquela data. A
operação é registrada na auditoria.

[?] A tela trata cada data da página como uma operação; o acervo lido não permite
afirmar quantas datas de uma mesma página são gravadas numa única confirmação. Pergunta
ao site.

### RN-14 — A alteração troca o número do documento e o leva aos pagamentos

A alteração reescreve apenas o número do documento daquela data — o dia, o mês e o valor
acumulado permanecem os do cadastro — e passa o número novo aos pagamentos daquela data.
A operação é registrada na auditoria, com o conteúdo anterior e o novo.

### RN-15 — A exclusão apaga o documento e tira o número dos pagamentos

A exclusão apaga o documento daquela data e deixa os pagamentos daquela data sem número
de documento. A operação é registrada na auditoria, com o conteúdo que foi apagado.

### RN-16 — Só os pagamentos da conta 78999 contam

Dos pagamentos da data, apenas os da conta **78999** somam para o valor acumulado e
apenas eles recebem o número do documento; os das outras contas são ignorados — na
inclusão, na alteração e na exclusão.

[?] O número **78999** está fixo no programa e não aparece em nenhum outro ponto do
acervo lido: o que essa conta representa — a conta em que a secretaria paga, ou um
marcador — não está documentado. Como a conta tem 14 dígitos e o número comparado tem 5,
também não se sabe se a comparação vale para a conta inteira ou para um pedaço dela.
Pergunta ao site.

### RN-17 — Cada mudança deixa rastro na auditoria

Cada inclusão, alteração ou exclusão gera um registro no cadastro de auditoria
(**A010T**) com a operação, a tela de origem, o ano e o mês de referência, a data e a
hora, a CRE, a matrícula, a estação, o tipo de órgão, e o conteúdo anterior e o novo do
documento.

[?] Na inclusão, o rastro só é gravado se um status interno da operação não for um valor
que o acervo chama de **DATA**; o que esse status significa não está no corpus, e se ele
ocorrer o documento é gravado sem o rastro. A alteração e a exclusão não fazem esse
teste. Pergunta ao site.

[?] O rastro guarda o **dia de pagamento** da data no campo que o sistema usa como
**número de processo** da operação; se é essa mesmo a intenção, ou se o campo foi
trocado, não foi possível determinar. Pergunta ao site.

### RN-18 — Tela, matrícula e operação são conferidas antes de operar

Toda operação passa por três conferências: a tela precisa estar cadastrada no cadastro de
telas — senão **\* Tela nao disponivel \***; a matrícula precisa ter a tela autorizada no
seu código de acesso — senão **\* Acesso negado para esta matricula \***; e a operação
pretendida precisa constar do perfil — senão **\* Acesso negado para esta operacao \***.
As conferências valem para a abertura e para cada data da página.

[?] A conferência da operação distingue inclusão, alteração e exclusão, mas não a
consulta: quem tem a tela autorizada consulta sem precisar do flag de consulta. Se a
intenção era exigir esse flag por tela, o caminho não o exige. Pergunta ao site.

### RN-19 — Os campos digitados passam por edição numérica

Os campos digitáveis — ano, dia, mês, número do documento, valor acumulado e total do
ano — passam por edição numérica. Campo em branco vira zero; o que não for número é
recusado, o cursor vai para o primeiro campo recusado e a operação não é feita.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não
está nos fontes desta jornada: a rotina que faz a edição não faz parte do acervo lido, e
o tratamento visível é só o cursor. Pergunta ao site.

### RN-20 — Cada operação começa com os campos de resultado limpos

Antes de conferir qualquer coisa, a tela apaga a data do sistema e a descrição do tipo de
órgão que havia mostrado, para que uma operação recusada não deixe na tela o resultado da
anterior.

## Cenários BDD

```gherkin
Funcionalidade: Manter o documento de pagamento das datas do ano

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F047T

  Cenário: O que a tela guarda de cada data de pagamento
    Dado que existe documento para uma data do ano
    Quando abro a tela no ano carregado
    Então vejo, para aquela data, o dia, o mês, o número do documento e o valor acumulado
    E vejo o total do ano, a data do sistema e a descrição do tipo de órgão

  Cenário: O total do ano
    Dado que o ano tem documentos cadastrados
    Quando a página é montada
    Então o total do ano mostrado é a soma dos valores acumulados desses documentos
    E o total é refeito depois de cada operação

  Cenário: Abertura de um ano sem documentos
    Dado que o ano que a tela carregou não tem documento nenhum
    Quando abro a tela
    Então vejo a mensagem "* Nao existem documentos cadastrados *"

  Cenário: Linha sem dia ou com situação desconhecida
    Dado que preenchi uma linha sem dia, ou com situação diferente de I, A e E
    Quando a tela processa a página
    Então aquela linha não gera operação nenhuma
    E nenhuma mensagem é mostrada por causa dela

  Cenário: Operação de manutenção diferente de alteração e de consulta
    Quando informo uma opção de manutenção diferente de ALT e de CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é lido nem gravado no documento e nos pagamentos

  Cenário: A consulta não grava nada
    Dado que a página tem datas com as situações I, A e E marcadas
    Quando peço a consulta
    Então nenhum documento é incluído, alterado ou excluído
    E nenhum pagamento é reescrito
    E nenhum registro de auditoria é gerado

  Cenário: Inclusão do documento de uma data
    Dado que existe pagamento para a data informada e ela ainda não tem documento
    E a soma dos pagamentos da data é um valor conhecido
    Quando informo o ano, o dia, o mês, o número do documento e o valor acumulado
    E marco a situação I
    Então o documento da data fica registrado com esse número e esse valor
    E os pagamentos daquela data ficam com esse número de documento
    E a operação fica registrada na auditoria

  Cenário: Alteração do número do documento de uma data
    Dado que a data informada já tem documento
    Quando informo outro número de documento e marco a situação A
    Então o documento passa a ter o número novo
    E os pagamentos daquela data passam a ter o número novo
    E o valor acumulado da data não muda
    E a operação fica registrada na auditoria, com o conteúdo anterior e o novo

  Cenário: Exclusão do documento de uma data
    Dado que a data informada já tem documento
    Quando marco a situação E
    Então o documento da data é apagado
    E os pagamentos daquela data ficam sem número de documento
    E a operação fica registrada na auditoria

  Cenário: Ano em branco na alteração
    Dado que deixo o ano de pagamento em branco
    Quando peço a alteração
    Então vejo a mensagem "* Informe o ano dos pagamentos *"
    E o cursor volta ao campo do ano
    E nada é gravado

  Cenário: Alteração de um ano que não foi consultado
    Dado que a tela está posicionada em um ano
    Quando informo outro ano e peço a alteração
    Então vejo a mensagem "* Consulte o ano antes de atualizar *"
    E o cursor volta ao campo do ano
    E nada é gravado

  Cenário: Inclusão de uma data que já tem documento
    Dado que a data informada já tem documento
    Quando marco a situação I
    Então vejo a mensagem "* Dia ja cadastrado *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: Inclusão de uma data sem pagamento
    Dado que a data informada não tem nenhum pagamento lançado
    Quando marco a situação I
    Então vejo a mensagem "* Nao existe pagamento para esta data *"
    E o cursor volta ao campo do dia
    E nada é gravado

  Cenário: Inclusão ou alteração sem o número do documento
    Dado que deixo o número do documento em branco
    Quando marco a situação I ou a situação A
    Então vejo a mensagem "* Informe o numero do documento *"
    E o cursor volta ao campo do número do documento
    E nada é gravado

  Cenário: Valor acumulado diferente da soma dos pagamentos
    Dado que a soma dos pagamentos da data é um valor conhecido
    Quando informo, na inclusão, um valor acumulado diferente
    Então vejo a mensagem "<- Valor do documento incorreto *"
    E o cursor volta ao campo do valor acumulado
    E nada é gravado

  Cenário: Alteração ou exclusão de uma data sem documento
    Dado que a data informada não tem documento
    Quando marco a situação A ou a situação E
    Então vejo a mensagem "* Dia nao cadastrado *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: Só os pagamentos da conta 78999 contam para a data
    Dado que a data tem pagamentos lançados na conta 78999 e em outras contas
    Quando incluo o documento da data
    Então o valor acumulado conferido é a soma dos pagamentos da conta 78999
    E só os pagamentos dessa conta recebem o número do documento

  Cenário: Cada mudança deixa rastro de auditoria
    Dado que incluo, altero ou excluo um documento
    Quando a operação é concluída
    Então a auditoria registra a operação, a tela de origem, a CRE, a minha matrícula, a minha estação e a data e a hora
    E registra o conteúdo anterior e o conteúdo novo do documento

  Cenário: Tela não cadastrada
    Dado que a tela F047T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela F047T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não tem o flag da operação pretendida
    Quando tento incluir, alterar ou excluir
    Então o sistema recusa a operação com "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Campo digitado que não é número
    Dado que digito, no ano, no dia, no mês, no número do documento ou em um valor, algo que não é número
    Quando peço a operação
    Então o cursor volta ao primeiro campo recusado
    E a operação não é feita

  Cenário: Cada operação começa com os campos de resultado limpos
    Dado que a tela já mostrou a data do sistema e o tipo de órgão
    Quando peço uma nova operação
    Então a data do sistema e a descrição do tipo de órgão da operação anterior não ficam na tela
```
