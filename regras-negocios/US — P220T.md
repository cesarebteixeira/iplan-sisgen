# US — P220T — Consultar os processos de um empenho

## Estória

Como **servidor de CRE**, quero **consultar, pelo grupo da minha regional, pelo
número do empenho e pelo ano de referência, os processos lançados nesse empenho,
com os valores, os totais e o fornecedor**, para que **eu confira o que está
empenhado, quanto já foi processado e para quem, sem abrir processo por processo
nem pedir o extrato a outro setor**.

O empenho é a autorização de gasto; os processos são os lançamentos feitos contra
ele, cada um com o seu número, o seu contrato, as suas ordens e os seus valores.
Esta é a tela em que a regional vê, num só lugar, todos os processos daquele
empenho e a soma do que eles valem — é o que permite responder a uma escola, a
uma secretaria ou a um órgão de controle sem depender da memória de quem digitou.

A tela é só de leitura: não inclui, não altera e não exclui processo, empenho nem
fornecedor — quem os mantém são outras telas. E ela recusa, em vez de responder
pela metade: quando falta o grupo, o número do empenho ou o ano; quando o grupo
informado não é o do servidor; e quando o empenho não tem processo nenhum.

## Contexto

Jornada S000M → P000M → P220T.

Ator: servidor de CRE — informa o grupo, o número do empenho e o ano de referência
e vê os processos daquele empenho, com os valores, os totais e o fornecedor.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio.

Das telas anteriores esta tela usa o que a entrada deixou na sessão: o tipo de
órgão e o grupo do servidor. O menu do módulo `P000M` só encaminha: não tem regra
de negócio nesta jornada. A `P220T` não encadeia para outra tela — ela lê, mostra
e para; não passa registro nem operação adiante.

---

## Regras de negócio

### RN-01 — A tela é de consulta: qualquer outra operação é recusada

A tela serve para consultar, e só. Ao abrir, ela mesma repõe a consulta no campo
da operação. Se o operador informar outra operação e confirmar, o sistema recusa
com **\* Operacao nao disponivel. Use CON \***, devolve o cursor ao campo da
operação e não lê nem grava nada.

A conferência de segurança vem antes dessa recusa: quando a operação informada é
daquelas que o acesso do servidor não libera, a recusa que aparece primeiro é
**\* Acesso negado para esta operacao \***.

[?] A recusa manda usar CON, mas o código que a tela reconhece como consulta é o
mesmo que ela repõe sozinha no campo quando abre. Se o campo aceita CON e o
sistema o traduz, ou se é a mensagem que ficou desatualizada, não se conclui pelos
fontes desta jornada. Pergunta ao site.

### RN-02 — Ao abrir, a tela propõe o grupo do servidor e o ano corrente

Ao ser aberta, a tela propõe no campo do grupo o **grupo do vínculo da sessão** e
no campo do ano o **ano corrente do sistema**. Ela mostra também o **tipo de
órgão** da sessão e a **data do sistema**. Quando o vínculo não tem grupo, o campo
do grupo fica em branco para o servidor informar.

O **número do empenho** não é proposto: o campo abre em branco, para o servidor
digitá-lo ou para recebê-lo preenchido da tela de onde veio.

### RN-03 — A consulta é pelo tipo de órgão, pelo grupo, pelo número do empenho e pelo ano

O servidor informa o **grupo** (2 dígitos), o **número do empenho** (6 dígitos) e o
**ano de referência** (4 dígitos). A procura é feita dentro do **tipo de órgão da
sessão**: vale o processo do tipo de órgão, do grupo, do número e do ano
informados. Empenho de outro tipo de órgão não é encontrado por esta tela.

Processo marcado como **excluído** no cadastro não entra na consulta: ele não
aparece na lista e os seus valores não entram nos totais.

[?] O número do empenho não é proposto na abertura: ou o operador o digita, ou a
tela o recebe já preenchido. O menu que abre esta tela não transporta esse dado
pelo programa, e a tela o lê de uma área de trabalho da sessão; como essa área é
preenchida, e por quem, não está nos fontes desta jornada. Pergunta ao site.

### RN-04 — A tela lista os processos do empenho, até 14 por consulta

Achado o empenho, a tela mostra os seus processos numa lista de **14 posições**.
Cada posição traz o **número do processo**, o **tipo de contrato**, a **ordem de
pré-empenho**, a **ordem de pagamento**, as **três colunas de valor do processo** e
a **situação do processo**.

Fora da lista, uma vez por consulta, a tela mostra o **código da fonte**, o
**código do órgão** e a **razão social do fornecedor** do empenho.

[?] Os rótulos dessas colunas de valor e do fornecedor não estão nos fontes desta
jornada: as colunas foram reconhecidas pelo que o cadastro guarda em cada uma, e
não pelo texto que a tela escreve sobre elas. Se o site usa outros nomes na tela,
é pergunta ao site.

### RN-05 — O número do processo exibido segue o tipo do processo

O número que a lista mostra não é o número cru: a tela o monta a partir do número
que o processo tem, com pontuação própria de cada tipo de processo — um dos dois
tipos previstos recebe os separadores numa posição, o outro em outra. Processo de
um terceiro tipo aparece **sem número**.

### RN-06 — A tela totaliza os valores de todos os processos do empenho

A tela soma, em três totais, os valores de **todos** os processos do empenho —
inclusive os que não couberem nas 14 posições da lista. Cada total corresponde à
sua coluna de valor.

[?] A tela não avisa quando o empenho tem mais processos do que as posições da
lista: a lista para e os totais continuam somando. Se o operador precisa saber que
há mais processos, é pergunta ao site.

### RN-07 — O fornecedor, a fonte e o órgão que a tela mostra são os do empenho

O código da fonte, o código do órgão e a razão social do fornecedor vêm do
**primeiro processo** achado para o empenho. O campo do código do fornecedor
aceita digitação e passa pela edição numérica como os outros, mas não participa de
nenhuma leitura: o que o operador digitar nele **não** muda o resultado da
consulta.

[?] O campo aceita digitação e não é usado em leitura nenhuma; ao remontar a tela,
o seu conteúdo é substituído pelo fornecedor do empenho. Se o campo deveria servir
de filtro — consultar só os processos de um fornecedor — ou se é apenas um campo
de saída que a máscara deixa digitar, é pergunta ao site.

### RN-08 — A consulta é limitada ao grupo do servidor

Quando o vínculo da sessão tem grupo, a tela só consulta se o grupo informado for
esse mesmo; informando outro, recusa com **\* Usuario sem acesso a outro grupo \***
e devolve o cursor ao campo do grupo. Quando o vínculo não tem grupo, qualquer
grupo informado passa.

[?] Um servidor cujo vínculo não tem grupo consulta o empenho de qualquer grupo.
Se isso é intencional, ou se deveria haver outro recorte, é pergunta ao site.

### RN-09 — Sem grupo, sem número de empenho ou sem ano a consulta não é feita

A conferência é nesta ordem, e em nenhum dos três casos a tela chega a consultar:

- grupo em branco — **\* Informe o grupo \***, com o cursor de volta no campo do
  grupo;
- número do empenho em branco — **\* Informe o numero do empenho \***, com o
  cursor de volta no campo do número do empenho;
- ano de referência em branco — **\* Informe o ano do exercicio \***, com o cursor
  de volta no campo do ano.

### RN-10 — Empenho sem processos é recusado

Se o empenho informado não tiver nenhum processo no grupo e no ano informados, a
tela recusa com **\* Nao existem processos para este empenho \*** e devolve o
cursor ao campo do número do empenho.

[?] A tela tem uma segunda mensagem de mesmo sentido — **\* Nao existem processos
cadastrados \*** —, usada ao remontar a lista. Qual das duas o operador vê em cada
situação, e se a segunda pode aparecer no lugar de outra mensagem, não se conclui
pelos fontes desta jornada. Pergunta ao site.

### RN-11 — Cada consulta começa com os campos de resultado limpos

Antes de conferir qualquer coisa, a tela apaga o que a consulta anterior havia
mostrado: o tipo de órgão, a data do sistema, o código da fonte, o código do
órgão, a razão social do fornecedor, o número do processo, o tipo de contrato, as
ordens, as três colunas de valor, a situação do processo e os três totais. Uma
consulta recusada, portanto, não deixa na tela o resultado da consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se
existe um caminho de entrada em que os campos não são limpos, é pergunta ao site.

### RN-12 — Os campos digitáveis passam por edição numérica antes da consulta

Os quatro campos digitáveis — grupo, número do empenho, ano de referência e código
do fornecedor — passam por edição numérica antes da consulta. Campo em branco vira
zero; o que não for número é recusado, a consulta não é feita e o cursor volta ao
primeiro campo recusado.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual —
não está nos fontes desta jornada: a rotina que faz a edição não faz parte do
acervo lido. Pergunta ao site.

[?] O campo do código do fornecedor não tem posição de cursor declarada na tela;
recusada a digitação nele, o cursor pode voltar à posição padrão da máscara, que é
a do campo do grupo. Se é isso que o site espera, é pergunta ao site.

### RN-13 — Antes de consultar, o sistema confere a tela e o acesso

A tela lê o próprio código no **cadastro de telas**, para saber que ela existe e
qual é o seu nome, e depois passa pela conferência de segurança da tela, com a
matrícula, o privilégio, o tipo de órgão e o grupo da sessão. Não passando, a
transação é abandonada sem ler nem gravar nada, e a recusa vem da conferência:
**\* Tela nao disponivel \*** quando a tela não está no cadastro de telas, e
**\* Acesso negado para esta matricula \*** quando o código de acesso da matrícula
não tem esta tela autorizada. Se a estação da sessão não for a mesma da entrada, o
acesso termina e o sistema volta à tela de entrada.

[?] O grupo que a conferência de segurança recebe é o **da sessão**, não o grupo
informado na tela: o grupo digitado é conferido depois, pela própria tela (RN-08).
Se a intenção era a conferência de segurança recusar o grupo digitado, o caminho
não o faz. Pergunta ao site.

[?] A máscara tem um campo de "próxima tela": vindo preenchido, a tela abandona em
silêncio e a transação é desviada para a tela informada. Quem preenche esse campo
para esta tela não está nos fontes desta jornada. Pergunta ao site.

### RN-14 — A consulta não grava nada

A tela lê três cadastros — o de telas, o de processos do empenho e o de
fornecedores — e para por aí: nenhum registro é incluído, alterado ou excluído,
nenhum registro é reservado para alteração e nada é gerado para auditoria.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar os processos de um empenho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela P220T

  Cenário: Consulta de um empenho com processos
    Dado que o empenho informado tem processos no meu grupo e no ano informado
    Quando informo o grupo, o número do empenho e o ano e confirmo a consulta
    Então vejo os processos do empenho, um por posição da lista
    E cada posição traz o número do processo, o tipo de contrato, as ordens, as três colunas de valor e a situação
    E vejo o código da fonte, o código do órgão e a razão social do fornecedor
    E vejo o total de cada coluna de valor

  Cenário: A abertura da tela
    Dado que o meu vínculo tem grupo
    Quando abro a tela P220T
    Então o campo do grupo vem preenchido com o grupo do meu vínculo
    E o campo do ano vem preenchido com o ano corrente do sistema
    E o campo do número do empenho vem em branco
    E vejo o tipo de órgão da minha sessão e a data do sistema

  Cenário: Processo excluído não aparece na lista
    Dado que um dos processos do empenho está marcado como excluído
    Quando consulto o empenho
    Então esse processo não aparece na lista
    E os valores dele não entram nos totais

  Cenário: Os totais somam todos os processos do empenho
    Dado que o empenho tem mais processos do que as posições da lista
    Quando consulto o empenho
    Então a lista mostra os processos que couberem nas suas posições
    E o total de cada coluna soma todos os processos do empenho

  Cenário: O número do processo exibido segue o tipo do processo
    Dado que o empenho tem um processo de cada tipo previsto
    Quando consulto o empenho
    Então cada posição mostra o número do processo com a pontuação do tipo dele
    E o processo de um tipo não previsto aparece sem número

  Cenário: O código do fornecedor digitado não muda o resultado
    Dado que o empenho tem um fornecedor
    Quando digito outro código de fornecedor e confirmo a consulta
    Então vejo o fornecedor do empenho
    E não o que digitei

  Cenário: Operação diferente de consulta
    Dado que estou na tela P220T
    Quando informo uma operação diferente da consulta e confirmo
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nada é consultado nem gravado

  Cenário: Operação não liberada para o meu acesso
    Dado que a minha autorização não libera a operação informada
    Quando confirmo a operação
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é consultado nem gravado

  Cenário: Grupo diferente do meu
    Dado que o meu vínculo tem um grupo
    Quando informo o grupo de outra regional e confirmo a consulta
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo do grupo
    E nada é consultado

  Cenário: Grupo em branco
    Dado que o meu vínculo não tem grupo
    Quando deixo o grupo em branco e confirmo a consulta
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nada é consultado

  Cenário: Número do empenho em branco
    Dado que informei o grupo e deixei o número do empenho em branco
    Quando confirmo a consulta
    Então vejo a mensagem "* Informe o numero do empenho *"
    E o cursor volta ao campo do número do empenho
    E nada é consultado

  Cenário: Ano em branco
    Dado que informei o grupo e o número do empenho e deixei o ano em branco
    Quando confirmo a consulta
    Então vejo a mensagem "* Informe o ano do exercicio *"
    E o cursor volta ao campo do ano
    E nada é consultado

  Cenário: Empenho sem processos
    Dado que o empenho informado não tem processo no meu grupo e no ano informado
    Quando confirmo a consulta
    Então vejo a mensagem "* Nao existem processos para este empenho *"
    E o cursor volta ao campo do número do empenho

  Cenário: A consulta começa com os campos de resultado limpos
    Dado que já mostrei o resultado de uma consulta anterior
    Quando peço uma nova consulta
    Então os resultados da consulta anterior não ficam na tela
    E só aparecem os resultados da consulta que passou pelas conferências

  Cenário: Código digitado que não é número
    Dado que digito no grupo, no número do empenho, no ano ou no código do fornecedor algo que não é número
    Quando confirmo a consulta
    Então o cursor volta ao primeiro campo recusado
    E a consulta não é feita

  Cenário: A consulta não grava nada
    Dado que existe o empenho informado e ele tem processos
    Quando consulto o empenho
    Então nenhum cadastro é incluído, alterado ou excluído
    E nenhum registro é reservado para alteração
    E nada é gerado para auditoria

  Cenário: Tela não cadastrada
    Dado que a tela P220T não está no cadastro de telas
    Quando tento consultar
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo consultar

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela P220T autorizada
    Quando tento consultar
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo consultar

  Cenário: Estação diferente da da entrada
    Dado que a minha estação não é a mesma do início da sessão
    Quando tento consultar
    Então o acesso termina e o sistema volta à tela de entrada
```
