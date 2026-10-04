# US — C666T — Consultar a permissão e as prorrogações por gênero

## Estória

Como **servidor da CRE que acompanha as permissões de fornecimento**, quero **consultar
uma permissão e ver as prorrogações concedidas a cada gênero**, para que **eu saiba, sem
sair da tela, qual é o período, quanto já foi adjudicado, aditado e prorrogado e quais
gêneros tiveram o período estendido — inclusive os que passaram de cinco anos**.

A permissão é o que autoriza um fornecedor a entregar, dentro de um período e para um
grupo de licitação, na área de uma CRE. Quem responde por essa área precisa ver o quadro
reunido: o período, os valores, o fornecedor, o tipo de licitação e as prorrogações uma a
uma, por gênero. É essa conferência que sustenta a decisão de prorrogar, de cobrar ou de
responder a uma consulta do órgão. Sem esta tela, a situação da permissão só aparece
espalhada pelas telas que a mantêm, e o aviso de que um período passou de cinco anos não
chega a quem precisa vê-lo. Esta tela não altera nada: ela só lê.

## Contexto

Jornada S000M → C000M → C050M → C664M → C666T (5 passos).
Ator: servidor de CRE — consulta a permissão de um fornecedor e as prorrogações por
gênero.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — a opção 5
do `C000M` abre o menu `C050M`, a opção 6 dele abre o menu `C664M` e a opção 3 dele abre
esta tela — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**,
não regra de negócio. Os três passos do meio são menus: não gravam nada e não deixam nada
de próprio para esta tela, apenas dizem qual tela abrir.

Nenhum deles encadeia a tela de destino: ela não recebe registro nem operação de outra
tela, e quem chega escolhe na própria `C666T` o que quer consultar. Da sessão ela usa o
que ficou da entrada — a matrícula, o acesso, o privilégio, o tipo de órgão e a CRE, mais
a descrição do órgão e a data do sistema que ela mostra no cabeçalho. Essas são regras da
entrada e estão no anexo de evidências, em **Regras que se revelaram da entrada**.

A jornada termina nesta tela: ela não encaminha para nenhuma outra.

As regras abaixo são só as desta tela.

## Regras de negócio

### RN-01 — A tela consulta a permissão e mostra o seu quadro

A tela é a **consulta da permissão** de um fornecedor. Ela identifica a permissão pela
**CRE** (o campo que a tela rotula `CORD.REG.ESCOLAR`), pelo **tipo de contrato**, pelo
**grupo de licitação** e pela **data limite** do período; o **órgão** é o da sessão e não
se informa. Os mesmos campos que o servidor informa voltam preenchidos, e é por eles que a
tela procura a permissão.

Achando a permissão, a tela mostra:

- o **período** — o dia, o mês e o ano de início e o dia, o mês e o ano limite;
- o **valor adjudicado**, o **valor aditivo** e o **valor de prorrogação**;
- o **código do fornecedor** e a **razão social** dele;
- o **tipo de licitação** e a **descrição** dele;
- o **início** e o **limite** de um segundo par de datas da permissão, além do período;
- e, para cada gênero, uma linha da lista (RN-08).

Ao reexibir a tela, os campos informáveis e os dados voltam com o que a área de trabalho
da sessão guardou da consulta anterior: a tela não os recalcula.

[?] O segundo par de datas — o início e o limite que a tela mostra além do período — não
tem nome no acervo desta jornada: as mensagens do sistema falam em tabela de preços, mas
nenhuma tela da jornada diz se é essa a tabela a que as duas datas se referem. Pergunta ao
site.

### RN-02 — A tela abre em consulta, e só aceita consulta

Ao abrir, a tela põe a **consulta** no campo de operação, seja qual for a origem. Se a
operação informada não for a consulta, a recusa é **\* Operacao nao disponivel. Use CON \***
e o cursor volta para o campo da operação; nada é procurado e nada é mostrado.

Antes de qualquer procura, a tela também se cala quando o pedido de outra tela chega
preenchido: nesse caso ela não recalcula nada.

[?] A recusa manda usar CON, mas o que a tela compara é o mnemônico interno da consulta.
Ou o terminal traduz o que o servidor digita, ou a mensagem está desalinhada da
comparação. Pergunta ao site.

[?] A tela recusa toda operação que não seja a consulta, mas guarda um ramo que só muda de
comportamento quando a operação informada é a **exclusão**: por ele, a segunda recusa de
prorrogação (RN-07) deixa de ser dada. Como a tela não grava e não apaga nada, não está no
acervo se esse ramo é alcançável por outro caminho ou se é herança do gerador. Pergunta ao
site.

### RN-03 — A consulta não grava nada

A consulta **não grava, não apaga, não trava registro e não deixa rastro de auditoria**.
As operações de gravação e de exclusão existem declaradas para todos os cadastros que a
tela enxerga — **oito cadastros, dezesseis operações de escrita** — e **nenhuma delas é
executada**: o que a tela executa são **vinte leituras**, sobre os mesmos oito cadastros.
A conferência dos cinco anos (RN-09) e a montagem das linhas (RN-08) também só leem.

### RN-04 — A permissão só se abre para a CRE do servidor

Se a sessão traz uma **CRE** — e o vínculo da entrada pode não trazer —, a CRE informada
tem de ser a do servidor. Informando a CRE de outro grupo, a recusa é **\* Usuario sem
acesso a este grupo \***, com o cursor de volta no campo da CRE, e a consulta não segue.
Sem CRE na sessão, a tela não restringe: qualquer CRE pode ser consultada.

[?] A conferência decide se há restrição por uma área de trabalho e compara a CRE
informada com a CRE do servidor guardada em outra. A entrada carrega a CRE do vínculo no
registro de trabalho da sessão, e o acervo não deixa ver como — nem se — ela chega a essas
duas áreas. Divergindo as duas, ou chegando vazias, não está no corpus qual delas manda.
Pergunta ao site.

### RN-05 — A permissão tem de estar cadastrada

Passando pela conferência da CRE, a tela procura a permissão pelo **órgão da sessão**,
pela **CRE**, pelo **tipo de contrato**, pelo **grupo de licitação** e pela **data limite**
informados. Não achando, a recusa é **\* Permissao nao cadastrada \***, com o cursor de
volta no campo da CRE, e a tela para.

[?] Na procura da permissão, a **classe**, a **subclasse** e o **gênero** do cadastro
entram zerados, e os três fazem parte da chave da permissão no dicionário de dados. O
acervo não diz se zero ali significa "qualquer um" ou se a tela só encontra a permissão
cujos três estejam zerados. Pergunta ao site.

### RN-06 — A tela tem de estar liberada para o tipo de licitação

A permissão achada traz o seu **tipo de licitação**, e a tela confere, no cadastro que diz
para quais tipos de licitação cada tela está liberada, se ela mesma está liberada para
aquele tipo. Não estando, a recusa é **\* Tela nao disponivel para esta licitacao \***,
com o cursor no campo do tipo de contrato, e a tela para.

### RN-07 — A permissão tem de ter prorrogações cadastradas

Ainda antes de mostrar, a tela percorre as **prorrogações** daquela permissão — pelo
órgão, pelo **início do período** que a permissão registra, pela CRE, pelo tipo de
contrato e pelo grupo de licitação. Não achando nenhuma, a recusa é **\* Nao existem reg
de prorrogacao cadastrados \***, com o cursor no campo da CRE, e a tela para.

Não achando prorrogação para a **primeira linha** da lista, a recusa é **\* Nao existem
prorrogacoes para esta permissao \***.

[?] As duas recusas acima cobrem a mesma ausência por dois caminhos: uma na conferência
que antecede a exibição, outra na montagem da primeira linha. Se a segunda é alcançável
depois de a primeira passar, o acervo não deixa concluir. Pergunta ao site.

### RN-08 — Uma linha por gênero, até dez, e a marcação do traço

Cada prorrogação da permissão ocupa **uma linha** da lista, e cada linha traz o **código
do gênero** (a subclasse e o gênero escritos juntos), a **descrição resumida** do gênero,
o **início** e o **limite** daquela prorrogação, a **quantidade** e o **valor inicial**
registrados nela. Prorrogações seguidas do mesmo gênero não fazem a tela procurar a
descrição de novo.

A lista mostra **dez linhas**. Havendo mais prorrogações do que isso, as que passam da
décima não aparecem.

Quando a prorrogação daquele gênero está marcada com o **traço**, a **marcação da
quantidade** e a **do valor inicial** daquela linha recebem um traço.

[?] O acervo não diz o que a marca do traço significa para quem opera — nem o que a
marcação da quantidade e do valor passa a querer dizer quando ela aparece. Pergunta ao
site.

[?] A descrição do gênero é procurada usando a **data limite da permissão** como data de
início da versão do gênero. Não está no acervo se é essa a versão que a tela deve mostrar,
nem se o que se queria era a versão vigente na data da prorrogação. Pergunta ao site.

### RN-09 — O aviso de que o período passou de cinco anos

A tela percorre as prorrogações da permissão e, se **alguma** delas está marcada como
**período maior que cinco anos**, mostra no cabeçalho o aviso **Ultrapassou 5 anos**.
Nenhuma marcada assim, o aviso não aparece.

[?] Nenhum programa do acervo calcula essa marca a partir das datas: a tela que mantém as
prorrogações só copia o indicador quando ele já vem preenchido. Ou a marca vem de carga,
ou o aviso nunca aparece. Pergunta ao site.

### RN-10 — De onde vêm os nomes e as descrições que a tela mostra

Além do que a permissão e as prorrogações guardam, a tela busca três coisas em outros
cadastros: a **razão social do fornecedor**, pelo código do fornecedor que a permissão
registra; a **descrição do tipo de licitação**, pelo tipo de licitação; e a **descrição
resumida do gênero**, no cadastro de gêneros, a cada linha. Não achando a descrição
resumida daquele gênero, a tela deixa no lugar dela um aviso de quatro asteriscos.

[?] O tipo de licitação que a tela mostra vem da permissão, e a descrição que ela mostra
ao lado vem do tipo de licitação registrado nas prorrogações. Divergindo os dois, a tela
mostraria um par incoerente, e o acervo não diz qual dos dois é o correto. Pergunta ao
site.

### RN-11 — Falha na leitura do banco é avisada pela rotina do sistema

Erro de leitura dos cadastros — e a leitura que não acha o registro — é despachado para a
rotina de comunicação do sistema, com o código do erro. Quem decide o que o servidor vê, e
se a consulta continua, é essa rotina.

[?] A rotina de comunicação do sistema não está no acervo: as telas apenas a chamam,
passando o código do erro. O que ela faz com o erro — avisa, interrompe ou deixa seguir —
não está no corpus. Pergunta ao site.

### RN-12 — A tela não encaminha para outra: a jornada termina nela

Esta tela não passa registro nem operação para nenhuma outra: não há tela seguinte. A
consulta começa e termina nela, e é por isso que esta jornada termina neste passo e não
tem saída.

## Cenários BDD

```gherkin
Funcionalidade: Consultar a permissão e as prorrogações por gênero

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C666T

  Cenário: RN-01, RN-03, RN-10 e RN-12 — consultar uma permissão cadastrada
    Dado que existe permissão para a CRE, o tipo de contrato, o grupo de licitação e a data limite que vou informar
    E essa permissão tem prorrogações cadastradas
    Quando informo CON com a CRE, o tipo de contrato, o grupo de licitação e a data limite
    Então vejo o período, o valor adjudicado, o valor aditivo e o valor de prorrogação
    E vejo o código e a razão social do fornecedor e a descrição do tipo de licitação
    E vejo o início e o limite do segundo par de datas da permissão
    E vejo uma linha por gênero, com o código do gênero, a descrição resumida, as datas, a quantidade e o valor inicial
    E nada é gravado, nada é apagado e nenhum rastro de auditoria é deixado

  Cenário: RN-01 — a tela reexibe o que ficou da consulta anterior
    Dado que consultei uma permissão nesta sessão
    Quando a tela se reexibe
    Então os campos informáveis e os dados voltam com o que a consulta anterior deixou
    E não é preciso informá-los de novo

  Cenário: RN-02 — a tela abre em consulta
    Dado que venho do menu C664M
    Quando a tela C666T abre
    Então ela abre com a consulta no campo de operação
    E o cabeçalho traz a descrição do órgão e a data do sistema
    E nada é gravado

  Cenário: RN-02 — operação diferente da consulta
    Dado que estou na tela C666T
    Quando informo uma operação diferente de CON
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor volta para o campo da operação
    E nada é mostrado e nada é gravado

  Cenário: RN-03 — a consulta não grava nada
    Dado que a permissão está cadastrada e tem prorrogações
    Quando informo CON
    Então nenhum cadastro é gravado ou apagado
    E nenhum registro é travado
    E nenhum rastro de auditoria é deixado

  Cenário: RN-04 — a CRE informada não é a do servidor
    Dado que a minha sessão tem uma CRE
    Quando informo CON com a CRE de outro grupo
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor volta para o campo da CRE
    E nada é consultado

  Cenário: RN-04 — servidor sem CRE na sessão
    Dado que a minha sessão não tem CRE
    Quando informo CON com a CRE de qualquer grupo
    Então a consulta segue pela permissão daquela CRE
    E nada é gravado

  Cenário: RN-05 — permissão não cadastrada
    Dado que não existe permissão para a CRE, o tipo de contrato, o grupo de licitação e a data limite informados
    Quando informo CON
    Então vejo "* Permissao nao cadastrada *"
    E o cursor volta para o campo da CRE
    E nada é gravado

  Cenário: RN-06 — a tela não está liberada para o tipo de licitação
    Dado que a permissão está cadastrada e o tipo de licitação dela não libera esta tela
    Quando informo CON
    Então vejo "* Tela nao disponivel para esta licitacao *"
    E o cursor vai para o campo do tipo de contrato
    E nada é mostrado

  Cenário: RN-07 — a permissão não tem prorrogações cadastradas
    Dado que a permissão está cadastrada e não tem prorrogação para os gêneros dela
    Quando informo CON
    Então vejo "* Nao existem reg de prorrogacao cadastrados *"
    E o cursor vai para o campo da CRE
    E nada é gravado

  Cenário: RN-07 — a lista não encontra prorrogação para a primeira linha
    Dado que a permissão está cadastrada
    Quando a tela monta a primeira linha da lista e não encontra prorrogação para aquele gênero
    Então vejo "* Nao existem prorrogacoes para esta permissao *"
    E nada é gravado

  Cenário: RN-08 — uma linha por gênero
    Dado que a permissão tem três gêneros com prorrogação
    Quando informo CON
    Então vejo três linhas, uma para cada gênero
    E cada linha traz o código do gênero, a descrição resumida, o início e o limite da prorrogação, a quantidade e o valor inicial

  Cenário: RN-08 — prorrogação marcada com o traço
    Dado que a prorrogação de um gênero está marcada com o traço
    Quando informo CON
    Então a marcação da quantidade e a do valor inicial daquela linha recebem um traço
    E as outras linhas ficam sem a marcação

  Cenário: RN-08 — mais prorrogações do que a tela mostra
    Dado que a permissão tem mais de dez prorrogações
    Quando informo CON
    Então vejo dez linhas
    E as prorrogações que passam da décima não aparecem

  Cenário: RN-09 — o período passou de cinco anos
    Dado que uma das prorrogações da permissão está marcada como período maior que cinco anos
    Quando informo CON
    Então vejo o aviso "Ultrapassou 5 anos" no cabeçalho

  Cenário: RN-09 — nenhuma prorrogação passou de cinco anos
    Dado que nenhuma prorrogação da permissão está marcada como período maior que cinco anos
    Quando informo CON
    Então o aviso "Ultrapassou 5 anos" não aparece

  Cenário: RN-10 — a descrição resumida do gênero não é encontrada
    Dado que a prorrogação de um gênero não tem versão no cadastro de gêneros para a data limite da permissão
    Quando informo CON
    Então no lugar da descrição resumida daquela linha aparece " **** "
    E a linha aparece assim mesmo

  Cenário: RN-11 — falha na leitura do banco
    Dado que a leitura dos cadastros falha
    Quando informo CON
    Então a falha é avisada pela rotina de comunicação do sistema
    E a consulta não é concluída
    E nada é gravado

  Cenário: RN-12 — a jornada termina na tela
    Dado que consultei a permissão
    Quando a tela termina a consulta
    Então ela não abre outra tela
    E não passa registro nem operação adiante
```
