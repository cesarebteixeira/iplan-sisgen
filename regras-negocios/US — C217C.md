# US — C217C — Consultar tabelas de preços

## Estória

Como **servidor de CRE**, quero **consultar as tabelas de preços por data de
referência já cadastradas e abrir o detalhe de uma delas**, para que **eu encontre
a tabela de uma data sem ter de adivinhá-la e veja o que ela contém**.

A tabela de preços de gêneros de material é mantida por data de referência, e quem
precisa do preço de um gênero numa data precisa primeiro saber qual data procurar.
Esta tela existe para isso: mostra as tabelas que existem, na ordem das datas, com
a descrição de cada uma, e leva ao detalhe da tabela escolhida. Sem ela, chegar a
uma tabela seria tentativa e erro sobre a data — e uma data sem tabela não é
recusada pela tela de manutenção: ela abre vazia, como se a tabela fosse nova.

## Contexto

Jornada S000M → C000M → C020M → C217C.
Ator: servidor de CRE — percorre a lista das tabelas de preços cadastradas e
escolhe uma para ver o detalhe.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O `C000M` e o `C020M` são menus: só encaminham e não deixam dado de negócio para
esta tela. O contexto de que a C217C se serve — a matrícula, o tipo de órgão, a CRE,
a estação e a data do sistema — é o que a entrada deixou na sessão; a tela não o
recalcula.

Esta é a tela **de consulta** do cadastro cuja manutenção é a C217T. A C217C lista
as tabelas de preços uma a uma, pela data de referência; a C217T mantém as linhas de
uma tabela, um preço por gênero. Quando o servidor pede o detalhe de uma linha da
lista, a C217C entrega a tabela escolhida à C217T, que abre nela em consulta.

O cadastro consultado é o mesmo que a C217T mantém: uma tabela por data de
referência, com uma descrição, e uma linha por gênero de material, com o preço. A
base comporta **1.500 linhas** — capacidade declarada, não volume cadastrado. A
descrição da tabela é uma só, repetida em cada linha dela; as linhas criadas pela
carga por arquivo podem entrar sem descrição.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — O que a consulta mostra

A tela lista as **tabelas de preços já cadastradas**, na ordem das datas de
referência, mostrando em cada linha a **data de referência** (dia, mês e ano) e a
**descrição da tabela**, e uma coluna de ação. O preço e a classificação do gênero —
classe, subclasse e gênero — **não** aparecem nesta lista: são o detalhe, que a tela
seguinte mostra. A lista também não enxerga os registros que o cadastro marca como
excluídos. No cabeçalho a tela tem dois campos: a **descrição do tipo de órgão** do
servidor e a **data do sistema**.

[?] Os dois campos do cabeçalho são copiados de uma área de trabalho que nenhum
programa do lote preenche: os únicos destinos desses dois campos, nos 506 programas
da árvore expandida, são as duas linhas que os apagam na abertura do sistema. Se o
ambiente não os transportar de fora para dentro, os dois saem em branco. Pergunta ao
site.

[?] A área de trabalho da tela carrega uma **classificação auxiliar** — classe,
subclasse e gênero auxiliares —, além da classe, da subclasse, do gênero e do preço;
ao abrir, a tela zera os nove campos e nenhuma outra linha do programa os lê. O
título provisório desta estória veio dessa classificação auxiliar, e o acervo não diz
para que ela serviria aqui. Pergunta ao site.

[?] A marca de manutenção que a lista desconsidera só é gravada, em todo o lote, com
o valor que significa registro novo; o valor que a leitura descarta não tem quem o
escreva em nenhum programa lido. Ou ele vem de fora do lote, ou a filtragem nunca
tem efeito. Pergunta ao site.

### RN-02 — A consulta não grava nada

Esta tela **não grava**. As rotinas de gravar e de apagar dos cadastros que ela
enxerga estão declaradas no programa e nenhuma delas é executada; a tela enxerga dois
cadastros — o cadastro das telas do sistema e a tabela de preços — e não enxerga a
trilha de auditoria. Consultar aqui não altera preço, descrição nem marca nenhuma, e
não deixa rastro; para mexer na tabela o servidor precisa da tela de manutenção
(C217T).

### RN-03 — A tela só atende em consulta

A tela é de consulta e de mais nada: ao abrir, ela sempre se apresenta em consulta,
venha de onde vier. Se a mensagem chegar com outra operação, a tela recusa com
**\* Operacao nao disponivel. Use CON \***, devolve o cursor ao campo da operação e
não lê nem grava nada.

[?] A recusa manda usar **CON** e a conferência compara o campo com o código interno
de consulta do sistema; nenhum fonte do lote mostra quem traduz o que o operador
digita. A mesma dúvida está registrada nas telas irmãs. Pergunta ao site.

### RN-04 — Sem tabela nenhuma, a consulta avisa

Não havendo tabela nenhuma a partir da posição em que a lista começa, a tela não
mostra linha e avisa **\* Nao existem tabelas cadastradas \***; o aviso aparece uma
vez, na primeira linha da página, e nada mais é feito.

[?] A mesma marca de "não encontrei" serve aos dois casos — não há tabela nenhuma e a
lista começou depois da última —, e por isso não se sabe se o aviso distingue os
dois. Pergunta ao site.

### RN-05 — A página: treze tabelas, uma por data de referência

A lista é montada de **treze em treze**. A tela percorre o cadastro na ordem da data
de referência e mostra **uma linha por data**: as várias linhas de uma mesma tabela —
uma por gênero — produzem uma só linha na lista, e é a primeira delas que dá a
descrição. Ao fim da página, a data da última tabela mostrada fica guardada como o
ponto de onde a lista continua.

[?] O que a lista faz na página seguinte depende de como a leitura se reposiciona
quando a tela volta a ser preenchida, e o efeito dos sinalizadores de leitura não
está no acervo nem no manual. Se a leitura volta à mesma tabela, a página seguinte
repete a anterior; se avança, segue; se não acha, a lista termina. Os três
comportamentos são compatíveis com o que o fonte mostra. Pergunta ao site.

### RN-06 — Onde a lista começa

Informada a **data de início** (dia, mês e ano), é dela que a lista parte. Em branco,
a lista começa na **primeira tabela do ano do sistema** e, não havendo nenhuma desse
ano em diante, na primeira tabela cadastrada.

[?] O ano da data de início é descartado: antes de procurar, a tela repõe o ano do
sistema e adota o ano da primeira tabela que encontrar, de modo que só o mês e o dia
da data de início posicionam a lista. Se o esperado é que a data de início inteira
posicione, o caminho não a usa. Pergunta ao site.

### RN-07 — A marca na linha preenchida abre o detalhe

A coluna de ação de cada linha aceita a marca **X**: marcando uma linha **que tem
tabela**, o servidor pede o detalhe daquela tabela — a consulta relê a tabela daquela
data e entrega a sessão à tela de manutenção (C217T). Ação em branco ou diferente de
**X** passa sem aviso: a linha não é tratada e nada acontece.

### RN-08 — A marca na linha vazia é recusada

Marcando **X** numa linha que **não tem tabela** — a data em branco —, a recusa é
**\* Consulte detalhes de linha preenchida \***, com o cursor de volta na coluna de
ação da própria linha; nada é entregue à tela seguinte.

### RN-09 — O que a consulta entrega à tela seguinte

Ao abrir o detalhe, a consulta entrega à tela de manutenção (C217T) três coisas: a
**data de referência** da tabela escolhida, a **descrição** dela e a **operação
consulta**. A tela seguinte abre por causa disso já naquela tabela e **em consulta**,
e não em alteração; é assim que esta consulta decide o modo da seguinte. Nada é
gravado nesta passagem.

### RN-10 — Os campos informados passam pela conferência de numérico

**Seis** campos passam pela conferência de numérico antes de a leitura que os usa
acontecer: o dia, o mês e o ano da **data de referência** das linhas e o dia, o mês e
o ano da **data de início**. O campo recusado interrompe a mensagem antes de qualquer
leitura, e nada é gravado.

[?] A conferência recusa os seis, mas só os três campos da data de início têm posição
de cursor mapeada: recusado o dia, o mês ou o ano da data de referência de uma linha,
o cursor não é devolvido ao campo. Se era para devolver, o caminho não devolve.
Pergunta ao site.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não
está no programa: a conferência é chamada de uma rotina de biblioteca cujo corpo não
veio no lote. Pergunta ao site.

### RN-11 — A próxima tela preenchida abandona a consulta

Se a mensagem chega com o **código da próxima tela** preenchido, a consulta é
abandonada antes de a linha ser tratada, nada é gravado e a sessão é encaminhada para
a tela indicada.

[?] O que preenche o código da próxima tela nesta tela não está no acervo: nenhuma
linha do programa o atribui. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consultar as tabelas de preços por data de referência

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C217C

  Cenário: RN-01 — a lista das tabelas cadastradas
    Dado que existem tabelas de preços cadastradas
    Quando a tela C217C é apresentada
    Então vejo uma linha por tabela, com a data de referência e a descrição
    E não vejo o preço nem a classificação do gênero
    E nada é gravado

  Cenário: RN-02 — a consulta não grava nada
    Dado que estou na tela C217C
    Quando percorro a lista das tabelas
    Então nenhum preço, descrição ou marca é alterado
    E nenhum registro é incluído ou apagado
    E nenhum rastro de auditoria é deixado

  Cenário: RN-03 — operação diferente de consulta
    Dado que estou na tela C217C
    Quando confirmo a mensagem com uma operação que não é a consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor fica no campo da operação
    E nada é lido e nada é gravado

  Cenário: RN-04 — nenhuma tabela na posição em que a lista começa
    Dado que não há tabela nenhuma a partir da posição em que a lista começa
    Quando a página é apresentada
    Então vejo a mensagem "* Nao existem tabelas cadastradas *"
    E a página não mostra linha alguma

  Cenário: RN-05 — treze tabelas por página, uma por data
    Dado que existem mais de treze tabelas cadastradas
    Quando a página é apresentada
    Então vejo no máximo treze linhas
    E cada linha corresponde a uma data de referência distinta
    E a lista continua a partir da data da última tabela mostrada

  Cenário: RN-06 — a lista começa no ano do sistema
    Dado que a data de início está em branco
    Quando a tela C217C é apresentada
    Então a lista começa na primeira tabela do ano do sistema
    E, não havendo nenhuma desse ano em diante, começa na primeira tabela cadastrada

  Cenário: RN-07 — pedir o detalhe de uma tabela
    Dado que estou na tela C217C
    E a linha de uma tabela está preenchida
    Quando marco a coluna de ação dessa linha
    Então a tabela daquela data de referência é aberta em consulta na tela C217T
    E nada é gravado

  Cenário: RN-07 — linha com ação em branco ou desconhecida
    Dado que estou na tela C217C
    Quando deixo a coluna de ação em branco ou uso uma marca diferente de X
    Então aquela linha não é tratada
    E nenhuma mensagem é mostrada

  Cenário: RN-08 — marcar uma linha sem tabela
    Dado que estou na tela C217C
    E a linha está sem data de referência
    Quando marco a coluna de ação dessa linha
    Então vejo a mensagem "* Consulte detalhes de linha preenchida *"
    E o cursor volta à coluna de ação da linha
    E nada é entregue à tela seguinte

  Cenário: RN-09 — o que a consulta entrega à tela seguinte
    Dado que pedi o detalhe de uma tabela da lista
    Quando a tela C217T abre
    Então ela mostra a tabela daquela data de referência, com a descrição
    E abre em consulta, e não em alteração

  Cenário: RN-10 — valor não numérico em um campo informado
    Dado que estou na tela C217C
    Quando informo um valor não numérico em um dos campos da data
    Então a mensagem é recusada antes de qualquer leitura
    E nada é gravado

  Cenário: RN-11 — a próxima tela preenchida abandona a consulta
    Dado que a mensagem chega à tela C217C com o código da próxima tela preenchido
    Quando a consulta começaria
    Então a linha não é tratada e nada é gravado
    E a sessão é encaminhada para a tela indicada
```
