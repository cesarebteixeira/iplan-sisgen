# US — P099P — Pedido de emissão dos relatórios de empenhos e pagamentos

## Estória

Como **servidor de CRE que emite os relatórios de despesa da secretaria**, quero
**completar os parâmetros do relatório que já escolhi e pedir a sua emissão**, para
que **o relatório saia com o recorte que eu preciso — a coordenação, o período, o
processo, o empenho, o fornecedor, a fonte ou o dia da auditoria — sem depender de
pedido por fora do sistema**.

É nesta tela que o pedido do relatório vira registro: ela recebe o relatório e a
impressora já escolhidos, cobra só os parâmetros daquele relatório e grava a
solicitação com um número próprio, que é o que a emissão usa para produzir o
relatório. Um pedido do mesmo relatório, para a mesma coordenação e o mesmo órgão, é
recusado enquanto o anterior está na fila — é assim que se evita imprimir duas vezes
a mesma coisa. E é aqui que os parâmetros errados são barrados: data fora do
calendário, ano fora da faixa aceita, período invertido, coordenação, fornecedor ou
fonte que não existe e situação de processo inválida voltam com aviso, sem registrar
nada.

## Contexto

Jornada S000M → P000M → P010M → P099P.

Ator: servidor de CRE — nesta tela, completa os parâmetros do relatório já escolhido
e pede a sua emissão.

A P099P não é menu e não deixa escolher o relatório: o relatório chega escolhido do
passo anterior e a tela se molda a ele. A P010M também não é menu — ela encadeia para
a P099P levando o relatório e a impressora, sem passar por opção de menu; é por isso
que a jornada chega aqui sem que a tela anterior ofereça a escolha outra vez.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. A conferência de acesso à tela e as
marcas de sessão que ela usa são as da entrada e não se repetem aqui: a procedência
delas está no anexo.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O relatório chega escolhido e a tela se molda a ele

A tela não oferece escolha de relatório: ele chega decidido pelo passo anterior, e a
tela se ajusta a ele. Ao abrir, ela assinala os campos que aquele relatório exige e
deixa o cursor no primeiro deles; nos relatórios que aceitam um código de "todos",
escreve ao lado do campo o código que significa todos — **9999** para fornecedor,
**9999999** para fonte e **99** para coordenação. São **dez relatórios** que a tela
sabe montar, cada um com o seu conjunto de campos; a escolha que esta jornada
oferece alcança **sete** deles.

[?] Os outros **três** — o de número de processo, o de coordenação, período e ano de
referência e o de coordenação, empenho e fornecedor — continuam sendo atendidos pela
tela, mas nenhuma opção da tela de escolha vigente os seleciona: quem os selecionava
é uma versão anterior dela, que ainda está no acervo. Ou são resto de uma versão
antiga, ou são acionados por fora do que foi lido. Pergunta ao site.

### RN-02 — A coordenação regional escolar recorta o relatório

**Cinco** dos sete relatórios desta jornada exigem a coordenação regional escolar.
Faltando, a recusa é **\* Informe o grupo \***; no relatório que aceita o código de
todas as coordenações, **\* Informe o grupo ou 99 para todas \***, porque ali **99**
vale por todas. Em **dois** desses cinco, a coordenação informada é conferida contra
o cadastro de coordenações do meu órgão e, não existindo, a recusa é
**\* Grupo nao cadastrado \***; nos outros **três** o valor segue sem conferência.

Os **dois** relatórios restantes não pedem coordenação: um abrange todas as
coordenações por definição e o outro recebe só o dia da auditoria.

[?] Nos três relatórios em que a coordenação não é conferida, um código inexistente
segue como se existisse — inclusive o **99**, que só é "todas" no relatório que o
anuncia. Se o emissor recusa depois, essa recusa não está no acervo lido. Pergunta
ao site.

### RN-03 — O período é conferido antes de virar pedido

**Quatro** dos sete relatórios pedem o período do relatório, com dia, mês e ano
iniciais e finais. A tela confere se cada data existe no calendário — recusando com
**\* Data de inicio invalida \*** ou **\* Data final invalida \*** —, se o ano está
entre **1994** e **2099**, e se a data inicial não é posterior à final, recusando com
**\* Data inicial > que data final \***. Ao recusar, o cursor volta para o campo da
data.

[?] A conferência de calendário é feita por rotina do ambiente, fora dos fontes
lidos; o que exatamente ela aceita — por exemplo, se o dia 29 de fevereiro de um ano
não bissexto passa — não está no acervo. Pergunta ao site.

### RN-04 — O primeiro trecho do número do processo vem preenchido do meu órgão

Ao abrir, a tela preenche o primeiro trecho do número do processo com o código da
secretaria municipal do órgão a que o servidor está vinculado. Os outros três
trechos — de dois, seis e quatro dígitos — são informados por quem opera.

### RN-05 — O empenho e o ano de referência identificam a despesa

Em **dois** dos sete relatórios o recorte é o empenho: o número do empenho e o ano de
referência são obrigatórios e, faltando, a recusa é **\* Informe o numero do
empenho \*** ou **\* Informe o ano de referencia \***.

### RN-06 — O fornecedor precisa existir, ou vir com o código de todos

**Três** dos sete relatórios usam o fornecedor. O código **9999** significa todos os
fornecedores e dispensa a conferência. Fora esse caso, o fornecedor informado tem de
existir no cadastro de fornecedores, e a recusa não é a mesma nos três: no relatório
por fornecedor e notas fiscais, o campo em branco recusa com **\* Informe o fornecedor
ou 9999 para todos \*** e o código que não existe no cadastro recusa com
**\* Fornecedor nao cadastrado \***, que é a única recusa do relatório por empenho,
também para o campo em branco; e, no relatório por fornecedor e fonte, a falta e o
código inexistente recebem a mesma recusa — **\* Informe fornecedor ou 9999 para
todos \***.

[?] No relatório por empenho, quando o fornecedor existe mas está marcado como
excluído, a tela volta a ler o mesmo fornecedor, no mesmo ponto: ou a conferência
está errada, ou a leitura deveria trazer o fornecedor seguinte. Por esse caminho o
pedido não é registrado e a recusa por fornecedor não cadastrado não chega a
aparecer. Pergunta ao site.

### RN-07 — A fonte precisa existir, ou vir com o código de todas

**Um** dos sete relatórios usa a fonte. O código **9999999** significa todas as
fontes e dispensa a conferência; fora esse caso, a fonte informada tem de existir no
cadastro de fontes. Faltando ou não cadastrada, a recusa é **\* Informe fonte ou
9999999 para todas \***.

### RN-08 — A situação do processo filtra o relatório

**Dois** relatórios usam a situação do processo: **1 = Fechado**, **2 =
Pré-empenho**, **3 = Liquidação** e **4 = Pagamento**. Um deles aceita as quatro
situações e avisa quais são com **\* Status 1=Fechado/2=PRE/3=LIQ/4=PAG \*** quando o
que foi informado não é uma delas; o outro só aceita as situações de **2 a 4** — o
Fechado não entra — e a recusa é **\* Status 2=PRE/3=LIQ/4=PAG \***. É a mensagem que
informa as situações válidas; a tela não traz a lista.

### RN-09 — Notas fiscais e a classificação por fornecedor ou por fonte

Um dos relatórios pergunta se o pedido deve considerar as notas fiscais, e a resposta
tem de ser **S** ou **N** — outra coisa é recusada com **\* Informar notas fiscais ?
<S/N> \***. Outro pede a classificação do relatório: **1 = Fornecedor** ou **2 =
Fonte**, recusando o resto com **\* Classificacao 1=Fornecedor/2=Fonte \***.

### RN-10 — O período das notas fiscais é um segundo recorte

Um dos relatórios pede, além do período do relatório, o período das notas fiscais. As
mesmas três conferências valem para ele: data que não existe, ano fora da faixa de
**1994** a **2099** e data inicial posterior à final.

### RN-11 — O relatório de auditoria recebe um único dia e não vira pedido

**Um** dos sete relatórios não recebe coordenação nem período: recebe um único dia, o
dia da auditoria. Faltando, a recusa é **\* Informe a data da auditoria \***.
Informado, a tela confere se existem registros de auditoria daquele dia e, não
existindo, recusa com **\* Nao existem registros para este dia \***. Diferente dos
outros, esse relatório não passa pelo cadastro de pedidos: é entregue direto à
emissão.

[?] A auditoria conferida é sempre a da tela P211T, fixada no programa, e não a da
tela em uso. Por que essa tela — e se o relatório deveria ser o da P099P — é pergunta
ao site.

### RN-12 — Pedido repetido do mesmo relatório é recusado

Antes de qualquer outra conferência, a tela procura pedido do mesmo relatório, para a
mesma coordenação e o mesmo órgão. Achando, recusa com **\* Relatorio ja esta em
processamento. Aguarde. \*** e nada é gravado. Vale para **seis** dos sete
relatórios; o de auditoria, que não vira pedido, não passa por essa conferência. No
relatório que abrange todas as coordenações, a procura é feita sem coordenação.

[?] A conferência não olha a situação do pedido: se um pedido já atendido continuar
no cadastro, um novo pedido igual é recusado para sempre. Se o emissor apaga o pedido
ao terminar, a conferência vale só para o que está em andamento. Pergunta ao site.

### RN-13 — O pedido é registrado com número do sistema

Passando as conferências, a tela registra o pedido no cadastro de solicitações de
relatório, com o relatório, o órgão, a coordenação, o período e os demais parâmetros,
a matrícula e a estação de quem pediu e a impressora escolhida. O número do pedido é
atribuído pelo sistema: é o **seguinte ao último já registrado** e começa em **1**
quando não há nenhum. A tela só acrescenta pedido — não altera e não apaga
solicitação nenhuma.

### RN-14 — A tela entrega o pedido à emissão e encerra a jornada

Registrado o pedido, a tela entrega à emissão, no mesmo passo, o relatório, o número
do pedido, o órgão, a coordenação, os parâmetros, a estação, a impressora e a
identificação de quem pediu; nos relatórios por fornecedor e fonte e por fornecedor e
notas fiscais segue também o e-mail cadastrado do servidor. O relatório de auditoria é
entregue do mesmo modo, sem o registro do pedido. A P099P é o fim da jornada: não há
opção nem tela seguinte — o que ela deixa é o pedido na fila da emissão.

[?] Quando o conjunto de parâmetros não cabe no espaço reservado, o pedido já
registrado fica sem entrega: a emissão não é acionada. Se é para ser assim, é
pergunta ao site.

### RN-15 — Fora o pedido, nada é gravado

Para montar o pedido, a tela consulta o cadastro de processos, o de coordenações, o
de fornecedores, o de fontes, o rastro de auditoria, o cadastro de funcionários, o de
órgãos e a autorização de tela do servidor. Nenhum deles é alterado: a única gravação
que a tela faz é a da solicitação de relatório.

### RN-16 — Campo numérico recusado devolve o cursor ao campo

Os **24** campos de código, número e data passam por conferência numérica antes de
qualquer uso: campo em branco conta como zero, texto no lugar de número é recusado, e
o cursor volta para o campo recusado. Nenhuma conferência posterior acontece com o
campo recusado.

[?] A tela reposiciona o cursor, mas a mensagem que o operador vê nessa recusa vem de
rotina comum que não está no acervo lido. O que ele lê exatamente é pergunta ao site.

### RN-17 — Os números de ordem de pagamento não seguem com o pedido

A tela tem dois campos de número de ordem de pagamento, inicial e final. Eles são
conferidos e mostrados na tela, mas não entram em nenhum pedido: os parâmetros que
seguem com a solicitação não os contêm.

[?] O que eles deveriam fazer — servir a um relatório que não está nesta versão, ou
ser campo sem uso — é pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedido de emissão dos relatórios de empenhos e pagamentos

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela P099P

  Cenário: A tela se molda ao relatório que chegou escolhido
    Dado que chego à P099P com um relatório já escolhido no passo anterior
    Então vejo assinalados os campos que aquele relatório exige
    E o cursor fica no primeiro campo a preencher
    E, quando o relatório aceita um código de todos, vejo ao lado do campo o código que significa todos

  Cenário: Relatório por coordenação e período
    Dado que o relatório escolhido é o de coordenação e período
    Quando informo uma coordenação existente, um período válido, uma situação de 1 a 4 e a resposta sobre notas fiscais
    Então o pedido é registrado com a coordenação, o período, a situação e a resposta
    E o pedido recebe um número atribuído pelo sistema
    E o relatório é entregue à emissão

  Cenário: Relatório por coordenação e período, por fornecedor ou por fonte
    Dado que o relatório escolhido é o de coordenação e período por fornecedor ou por fonte
    Quando informo uma coordenação existente, um período válido, um fornecedor cadastrado, uma situação de 2 a 4 e a classificação fornecedor ou fonte
    Então o pedido é registrado com esses dados
    E o relatório é entregue à emissão

  Cenário: Relatório por fornecedor e período das notas fiscais
    Dado que o relatório escolhido é o de fornecedor e notas fiscais
    Quando informo uma coordenação existente, um período válido, um fornecedor cadastrado e o período das notas fiscais
    Então o pedido é registrado com os dois períodos e o fornecedor

  Cenário: Relatório por empenho
    Dado que o relatório escolhido é o de empenho
    Quando informo a coordenação, o número do empenho, o ano de referência e um fornecedor cadastrado
    Então o pedido é registrado com esses dados

  Cenário: Relatório por empenho de todas as coordenações
    Dado que o relatório escolhido é o de empenho de todas as coordenações
    Quando informo 99 na coordenação, o número do empenho e o ano de referência
    Então o pedido é registrado para todas as coordenações

  Cenário: Relatório por período, de todas as coordenações
    Dado que o relatório escolhido abrange todas as coordenações
    Quando informo um período válido e deixo a coordenação em branco
    Então o pedido é registrado sem coordenação
    E o relatório é entregue à emissão

  Cenário: Relatório de auditoria do dia
    Dado que o relatório escolhido é o de auditoria
    E que existem registros de auditoria para o dia informado
    Quando informo o dia
    Então o relatório é entregue à emissão
    E nenhum pedido é registrado

  Cenário: O primeiro trecho do número do processo já vem preenchido
    Dado que o órgão a que estou vinculado tem secretaria municipal cadastrada
    Quando abro a P099P
    Então o primeiro trecho do número do processo aparece preenchido com o código dessa secretaria
    E os outros três trechos ficam por minha conta

  Cenário: O primeiro pedido recebe o número 1
    Dado que não há nenhum pedido registrado
    Quando informo parâmetros válidos
    Então o pedido recebe o número 1

  Cenário: O número do pedido é o seguinte ao último registrado
    Dado que o último pedido registrado é o de número 41
    Quando informo parâmetros válidos
    Então o pedido recebe o número 42

  Cenário: Coordenação não informada
    Dado que o relatório escolhido exige coordenação
    Quando não informo a coordenação
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta para o campo da coordenação
    E nada é registrado

  Cenário: Coordenação não informada no relatório que aceita todas
    Dado que o relatório escolhido aceita o código de todas as coordenações
    Quando deixo a coordenação em branco
    Então vejo a mensagem "* Informe o grupo ou 99 para todas *"
    E nada é registrado

  Cenário: Coordenação inexistente
    Dado que a coordenação informada não existe para o meu órgão
    Quando peço o relatório
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E nada é registrado

  Cenário: Data que não existe no calendário
    Quando informo uma data impossível no período
    Então vejo a mensagem "* Data de inicio invalida *" ou "* Data final invalida *"
    E o cursor volta para o campo da data
    E nada é registrado

  Cenário: Ano fora da faixa aceita
    Quando informo o ano inicial 1993 ou 2100
    Então vejo a mensagem "* Data de inicio invalida *"
    E nada é registrado

  Cenário: Período invertido
    Dado que a data inicial é posterior à data final
    Quando peço o relatório
    Então vejo a mensagem "* Data inicial > que data final *"
    E o cursor volta para a data inicial
    E nada é registrado

  Cenário: Período das notas fiscais invertido
    Dado que o relatório escolhido pede o período das notas fiscais
    E que a data inicial das notas é posterior à final
    Quando peço o relatório
    Então vejo a mensagem "* Data inicial > que data final *"
    E nada é registrado

  Cenário: Empenho e ano de referência não informados
    Dado que o relatório escolhido é o de empenho
    Quando deixo o número do empenho em branco
    Então vejo a mensagem "* Informe o numero do empenho *"
    E quando deixo o ano de referência em branco vejo "* Informe o ano de referencia *"
    E nada é registrado

  Cenário: Fornecedor não informado
    Dado que o relatório escolhido é o de fornecedor e notas fiscais
    Quando deixo o fornecedor em branco
    Então vejo a mensagem "* Informe o fornecedor ou 9999 para todos *"
    E nada é registrado

  Cenário: Fornecedor não cadastrado
    Dado que o fornecedor informado não existe no cadastro
    Quando peço o relatório
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E nada é registrado

  Cenário: No relatório por fornecedor e fonte, a falta e o inexistente recebem a mesma recusa
    Dado que o relatório escolhido é o de fornecedor e fonte
    Quando deixo o fornecedor em branco ou informo um fornecedor não cadastrado
    Então vejo a mensagem "* Informe fornecedor ou 9999 para todos *"
    E nada é registrado

  Cenário: 9999 significa todos os fornecedores
    Dado que o relatório escolhido aceita o código de todos
    Quando informo 9999 no fornecedor
    Então o pedido é registrado sem que o fornecedor seja conferido

  Cenário: Fonte não informada e 9999999 significa todas as fontes
    Dado que o relatório escolhido pede a fonte
    Quando deixo a fonte em branco ou informo uma fonte não cadastrada
    Então vejo a mensagem "* Informe fonte ou 9999999 para todas *"
    E quando informo 9999999 o pedido é registrado sem conferir a fonte

  Cenário: Situação do processo fora das quatro
    Dado que o relatório escolhido aceita as quatro situações
    Quando informo uma situação diferente de 1, 2, 3 e 4
    Então vejo a mensagem "* Status 1=Fechado/2=PRE/3=LIQ/4=PAG *"
    E nada é registrado

  Cenário: A situação Fechado não entra no relatório por fornecedor e fonte
    Dado que o relatório escolhido é o de fornecedor e fonte
    Quando informo a situação 1
    Então vejo a mensagem "* Status 2=PRE/3=LIQ/4=PAG *"
    E nada é registrado

  Cenário: Resposta sobre notas fiscais fora de S e N
    Dado que o relatório pergunta se deve considerar as notas fiscais
    Quando respondo algo diferente de S ou N
    Então vejo a mensagem "* Informar notas fiscais ? <S/N> *"
    E nada é registrado

  Cenário: Classificação fora de fornecedor e fonte
    Dado que o relatório pede a classificação por fornecedor ou por fonte
    Quando informo uma classificação diferente de 1 e 2
    Então vejo a mensagem "* Classificacao 1=Fornecedor/2=Fonte *"
    E nada é registrado

  Cenário: Dia da auditoria não informado
    Dado que o relatório escolhido é o de auditoria
    Quando deixo o dia em branco
    Então vejo a mensagem "* Informe a data da auditoria *"
    E nada é registrado

  Cenário: Auditoria sem registros no dia informado
    Dado que não há registros de auditoria para o dia informado
    Quando peço o relatório de auditoria
    Então vejo a mensagem "* Nao existem registros para este dia *"
    E nada é emitido
    E nada é registrado

  Cenário: Pedido repetido do mesmo relatório é recusado
    Dado que já existe pedido do mesmo relatório para a mesma coordenação e o mesmo órgão
    Quando tento registrar outro igual
    Então vejo a mensagem "* Relatorio ja esta em processamento. Aguarde. *"
    E nada é registrado

  Cenário: Texto em campo numérico
    Quando digito texto em um campo de código, número ou data
    Então o cursor volta para aquele campo
    E nada é registrado

  Cenário: Nenhum cadastro é alterado e nenhum pedido é apagado
    Dado que peço um relatório com parâmetros válidos
    Quando o pedido é registrado
    Então nenhum dos cadastros consultados é alterado
    E nenhum pedido já registrado é alterado ou apagado

  Cenário: Os números de ordem de pagamento não seguem com o pedido
    Dado que preencho os números de ordem de pagamento inicial e final
    Quando o pedido é registrado
    Então esses números não fazem parte dos parâmetros do pedido

  Cenário: A tela não leva a nenhuma outra
    Dado que o pedido foi registrado e entregue à emissão
    Então continuo na P099P
    E não há opção de menu que abra outra tela
```
