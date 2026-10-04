# US — E920C — Consulta dos contratos de fornecimento da unidade

## Estória

Como **servidor da CRE**, quero **consultar, para cada unidade da minha
coordenadoria, o contrato de fornecimento com o período de início e o período
limite**, para que eu saiba até quando aquela unidade está coberta pelo contrato e
por qual fornecedor.

O período do contrato é o que define a janela em que a unidade pode ser atendida: o
início e o limite. Sem essa consulta, a coordenação não tem como conferir se a
unidade está coberta, nem abrir o contrato certo para ver o que está vigendo. A
consulta também é a porta de entrada do detalhamento do contrato: é escolhendo uma
linha da lista que o servidor chega à tela do contrato.

## Contexto

Jornada S000M → E000M → E900M → E920C.
Ator: servidor de CRE — consulta os contratos de fornecimento de uma unidade da sua
coordenadoria e escolhe o contrato que quer detalhar.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O
caminho até a tela — qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio.

O `E900M` desta jornada não é menu: é tela de consulta que já lista os contratos da
unidade e encaminha para esta tela quando o servidor escolhe uma das linhas. Por
isso esta tela abre já na operação de **consultar** — o que ela recebe de quem a
chamou é regra dela, e está na RN-01. E esta tela também encadeia: escolhida uma
linha, ela passa o contrato para a tela de detalhamento, sem passar por menu
nenhum (RN-09). As três telas do caminho não gravam nada.

## Regras de negócio

### RN-01 — A tela abre na operação de consultar, e é a consulta que ela faz

A tela é de consulta: ela mostra os contratos já cadastrados para uma unidade e o
período de cada um, e não inclui, não altera e não exclui contrato. A operação da
tela é a de consultar, e ela é fixada pela própria tela no primeiro momento em que
aparece — por isso a consulta não depende de o servidor digitar a operação, e não há
outro campo de operação a preencher: a tela só abre do jeito que quem a chamou a
abriu.

[?] A tela traz uma recusa para a hipótese de a operação não ser a de consultar —
com a mensagem "* Opcao nao disponivel. Use CON *" e o cursor de volta na operação
—, mas, no mesmo caminho, a operação é sobrescrita pelo código de consultar antes de
ser conferida. Do jeito que está, a recusa nunca acontece: a operação não pode ser
outra coisa senão consultar. Ou a guarda vale para outro caso, ou esse ramo ficou
inalcançável. Pergunta ao site.

### RN-02 — A consulta é a da unidade que veio da tela anterior

A lista de contratos é lida para a **unidade** que a sessão trouxe da tela anterior
(o órgão filho e o tipo de órgão da sessão), combinada com o **ano do contrato** e o
**número do contrato**. A tela não pede a unidade de novo: o servidor não digita de
qual unidade quer ver os contratos.

### RN-03 — A tela mostra catorze contratos por vez, e o ano e o número em cada linha

A lista de contratos da unidade é apresentada de **catorze em catorze** — é a
capacidade do quadro de linhas da tela —, e a tela avança sozinha para a leitura
seguinte, até acabar. Cada linha traz o **número do contrato**, o **ano do
contrato**, o **fornecedor** (o código e o nome), o **dia, o mês e o ano do início**
e o **dia, o mês e o ano do limite** do período, além da **situação** da linha.

### RN-04 — A lista sai do cadastro dos contratos de fornecimento, que tem limite de mil registros

A origem da lista é o cadastro de **contratos de fornecimento** por unidade, cuja
capacidade declarada é de **mil registros** — capacidade é o máximo esperado, não o
volume existente. A leitura da lista é feita pela chave que combina **tipo de
órgão, ano do contrato e número do contrato**, o que significa que os contratos são
identificados pelo ano e pelo número, dentro de uma unidade.

### RN-05 — Quando não há contrato cadastrado, a tela avisa e não deixa seguir

Se a unidade não tem nenhum contrato cadastrado, a tela avisa **\* Nao existem
contratos cadastrados \***, **zera** o ano e o número do contrato do contexto e não
preenche linha nenhuma. Nesse estado não há o que escolher, e a tela não encaminha
para o detalhamento.

### RN-06 — As seis datas são numéricas, e o campo em branco vale zero

Os seis campos de data — **dia, mês e ano do início** e **dia, mês e ano do
limite** — passam pela edição numérica, na ordem em que aparecem: o que estiver em
branco vira zero, os zeros à esquerda são descartados, e o que não for número é
recusado e zerado. São **6** campos: contei os seis rótulos que a tela valida, dois
dígitos para o dia, dois para o mês e quatro para o ano de cada ponta do período.

### RN-07 — A tela não confere calendário nem a ordem do período

A tela confere que as seis datas são números; **não** confere se o dia e o mês
existem no calendário — o dia aceita até 99 e o mês até 99 — e **não** confere se a
data limite é posterior à data de início. Um limite anterior ao início, ou um dia 31
de fevereiro, passam pela tela.

### RN-08 — A linha escolhida é a que manda, e uma linha só

A escolha do contrato é feita pelo **número do contrato** informado na linha em que
o servidor marcou a opção de linha. É um contrato por vez: escolhida uma linha, a
tela continua a operação com aquele ano, aquele número, aquele período e aquela
situação. Se o servidor marcar a opção de linha e **não** informar o número do
contrato, a tela recusa com **\* Consulte linha preenchida \*** e devolve o cursor à
opção da linha.

### RN-09 — Escolhido um contrato, a tela abre o detalhamento dele em consulta

Escolhido o contrato, a tela passa o **ano do contrato, o número do contrato e a
unidade** para a tela de detalhamento do contrato, que é aberta **em consulta** —
porque foi esta tela que a chamou. O servidor não sai por menu nenhum: a passagem é
direta, e é ela que explica por que o detalhamento abre sem permissão de alterar.
Quem chega ao detalhamento por outro caminho o abre em inclusão; chegando por
aqui, não.

### RN-10 — A consulta não grava nada, nem antes nem depois da escolha

Esta tela apenas lê. Exibir a lista, informar as datas e escolher uma linha **não**
gravam contrato, não alteram o período e não excluem nada: a tela não executa
nenhuma gravação. Quem grava o contrato é o detalhamento, quando aberto para
inclusão ou alteração.

### RN-11 — O período mostrado na linha é o período do contrato, e a situação vem do contrato

O que a tela mostra como início e limite é o **período do contrato** lido do cadastro
dos contratos de fornecimento, e a **situação** mostrada na linha também vem do
contrato; a tela não os recalcula nem os altera.

### RN-12 — O nome do fornecedor é buscado no cadastro de fornecedores

O nome do fornecedor que aparece junto ao código do contrato é lido do **cadastro de
fornecedores**, pelo código do fornecedor que o contrato guarda. Por isso a tela
encontra o nome mesmo quando a linha do contrato só traz o código.

### RN-13 — O que a tela mostra fora da lista

Fora das catorze linhas, a tela mostra o **nome da unidade** sobre a qual se está
consultando e a **data do sistema** — e mais nada de identificação. É essa
identificação que diz ao servidor a qual unidade pertencem os contratos listados.

[?] A tela tem um campo rotulado **CDPEDAUX** na sua máscara, mas o programa não o
lê, não o valida e não o usa em nenhum ponto: ou o rótulo é sobra de máscara, ou o
campo serve a uma função que não está nesta versão do programa. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consulta dos contratos de fornecimento de uma unidade e do período de cada um

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E920C

  Cenário: Consultar os contratos da unidade e ver o período de cada um
    Dado que cheguei à tela pela consulta da unidade que quero conferir
    Quando a tela mostra os contratos daquela unidade
    Então vejo até catorze linhas, cada uma com o número e o ano do contrato, o fornecedor e o dia, o mês e o ano do início e do limite
    E vejo o nome da unidade e a data do sistema sobre a lista

  Cenário: A unidade não tem contrato cadastrado
    Dado que cheguei à tela pela consulta de uma unidade sem contrato cadastrado
    Quando a tela procura os contratos daquela unidade
    Então vejo a mensagem "* Nao existem contratos cadastrados *"
    E o ano e o número do contrato ficam zerados
    E nenhuma linha é preenchida e não sou levado ao detalhamento

  Cenário: Escolher um contrato e abrir o detalhamento em consulta
    Dado que a tela está mostrando os contratos da unidade
    Quando marco a opção de linha e informo o número de um contrato preenchido
    Então a tela abre o detalhamento daquele contrato
    E o detalhamento abre em consulta, sem permissão de alterar

  Cenário: A opção de linha está marcada sem o número do contrato
    Dado que a tela está mostrando os contratos da unidade
    Quando marco a opção de linha e deixo o número do contrato em branco
    Então vejo a mensagem "* Consulte linha preenchida *"
    E o cursor volta para a opção da linha

  Cenário: A data informada não é número
    Dado que a tela está mostrando um contrato da unidade
    Quando informo letras em um dos seis campos de data do período
    Então o campo é recusado e fica zerado
    E a tela não grava nada e não segue com o período informado

  Cenário: Consultar não grava
    Dado que a tela está mostrando os contratos da unidade
    Quando apenas exibo a lista e informo as datas do período
    Então nenhum contrato é incluído, alterado ou excluído
```
