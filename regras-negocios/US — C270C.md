# US — C270C — Consulta dos segmentos com percentual registrado

## Estória

Como **servidor de CRE**, quero **consultar quais segmentos de atendimento da minha
secretaria já têm percentual registrado e escolher um deles**, para que **eu chegue à
manutenção do percentual daquele segmento conferindo antes a descrição de cada segmento
que a secretaria tem, sem ter de saber de cor o código dele**.

O percentual de atendimento de um segmento é o que a atualização do cadastro aplica para
repartir o total apurado entre os segmentos da secretaria, e a manutenção dele é feita
segmento por segmento: o código do segmento é o que a tela de manutenção pede. Sem esta
consulta, quem vai manter o percentual teria de saber de cor esse código, sem nada que
lhe mostre os segmentos já registrados para a sua secretaria. Esta tela é só de leitura:
ela não inclui, não altera e não exclui registro nenhum.

## Contexto

Jornada S000M → C000M → C028M → C270C.

Ator: servidor de CRE — confere os segmentos de atendimento que a sua secretaria já tem
com percentual registrado, escolhe um e segue para a manutenção do percentual dele.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O C000M e o C028M são menus: eles não
gravam nada e apenas encaminham.

Esta tela **encadeia** com a C270T, a tela de manutenção do percentual de atendimento por
segmento e tipo de refeição. O operador não volta ao menu para chegar lá: é esta tela que
a abre.

O que ela usa da sessão — o tipo de órgão (a secretaria), a descrição dele e a data do
sistema — é o que a entrada e as telas anteriores deixaram. A tela não pergunta a
secretaria: ela só enxerga a da sessão.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela é de consulta: ela não grava nada

A tela abre em modo de consulta e assim permanece em todo caminho de quem a usa. Nenhuma
inclusão, alteração ou exclusão é executada, e nenhum registro de auditoria é gerado. As
operações de gravação, de exclusão e de travamento existem declaradas para os três
cadastros que a tela enxerga, mas **não são executadas em nenhum caminho** — declarar não
é executar.

### RN-02 — A lista é dos segmentos que já têm percentual registrado, e só da secretaria da sessão

O que a tela lista são os **segmentos de atendimento com percentual registrado** para a
**secretaria da sessão**. A lista não é montada a partir do cadastro de segmentos, e sim
do cadastro do percentual por segmento e tipo de refeição — o mesmo que a C270T mantém.
Por isso a tela não pergunta de qual secretaria se trata: todas as leituras são do tipo
de órgão que a sessão deixou. O cabeçalho mostra a **descrição do tipo de órgão** e a
**data do sistema**.

[?] A lista parte do cadastro do percentual, e não do cadastro de segmentos: um segmento
da secretaria que não tenha nenhum percentual registrado não aparece na lista, e por esta
tela não há como chegar à manutenção dele — que é justamente onde o percentual seria
criado. Ou a leitura deveria ser do cadastro de segmentos, ou o segmento sem percentual
tem outro caminho, que o acervo lido não mostra. Pergunta ao site.

### RN-03 — Cada linha traz o código do segmento, a descrição e a situação; a lista comporta treze linhas

Cada uma das linhas traz **três informações**: o **código do segmento**, a **descrição do
segmento** e a **situação da linha**. A tela mostra **treze linhas** por página; as que
não tiverem registro ficam em branco. O código é apresentado com dois dígitos, com zeros
à esquerda, e a descrição ocupa trinta posições.

### RN-04 — O mesmo segmento aparece uma só vez, ainda que tenha vários tipos de refeição

O percentual é registrado por segmento **e** por tipo de refeição, de modo que o mesmo
segmento tem um registro para cada refeição que atende. A lista mostra **uma linha por
segmento**: os registros seguintes do mesmo segmento são saltados, e o que se vê é o
segmento, não cada refeição dele.

### RN-05 — A descrição da linha é a do cadastro de segmentos da secretaria

A descrição que a linha mostra é a **descrição do segmento registrada no cadastro de
segmentos**, lida a partir do código do segmento que está sendo listado e do tipo de
órgão da sessão. A tela não pergunta a descrição: ela vem do cadastro.

### RN-06 — O campo de posição reinicia a lista pelo segmento informado

A tela tem um **campo de posição**, que mostra o código do segmento por onde a leitura da
lista começa, junto com a descrição dele. Informando ali o código de um segmento
cadastrado, a leitura da lista recomeça por ele; informando um código que não está no
cadastro de segmentos, a leitura recomeça pelo **primeiro segmento cadastrado** para a
secretaria. Quando a página se completa, a própria tela reescreve o campo de posição com
o **último segmento listado** e a descrição dele, de modo que a leitura continue de onde
parou.

[?] O rótulo **NMFUNCINI** está sobre o campo que guarda um código de segmento de dois
dígitos, e o mesmo rótulo aparece, no mesmo acervo, sobre campos de posição inicial de
outras telas. Ou o rótulo é sobra da máscara, ou nomeia outra coisa que o acervo lido não
mostra. Pergunta ao site.

### RN-07 — Sem escolha, a tela só volta a se mostrar

A tela não abre outra tela por conta própria. Se a linha não estiver marcada — sem código
de segmento informado, ou sem a marcação própria de escolha —, a tela apenas volta a se
mostrar, em consulta, e nada é entregue à tela seguinte.

### RN-08 — Escolhendo um segmento marcado, a tela abre a manutenção do percentual em consulta

Escolhendo a linha de um segmento — com o **código do segmento** informado e a linha
**marcada** com o código de situação que a tela exige —, o sistema entrega à **C270T** o
**segmento escolhido** e a **descrição dele**, com o **tipo de refeição zerado**, e abre
aquela tela em **consulta**. O operador não volta ao menu: é esta tela que abre a
manutenção, e ela abre em consulta — alterar depende de outra origem.

[?] A escolha só é considerada quando a linha está marcada com o código de situação
**X**, e **nenhum caminho do programa escreve esse código**: a situação é exibida e
testada, mas nunca atribuída, e a própria passagem que monta a lista a apaga. Ou o
formulário a transporta — uma marca que o servidor digita na linha —, ou esse desfecho é
inalcançável pelo caminho lido. Não escolhi um dos dois lados. Pergunta ao site.

### RN-09 — O código do segmento e o campo de posição passam pela edição numérica

Os dois campos informados — o **código do segmento** e o **campo de posição** — passam por
edição numérica antes de qualquer leitura: campo em branco é tratado como zero, o que não
for número é recusado no campo e a consulta não segue. Na recusa do campo de posição, o
cursor volta a ele; na recusa do código do segmento, não há devolução do cursor.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não está
nos fontes desta jornada: a rotina que faz a edição numérica é externa ao programa desta
tela. Pergunta ao site.

### RN-10 — Sem segmento com percentual para a secretaria, a tela avisa e encerra a listagem

Quando a secretaria não tem **nenhum segmento com percentual registrado**, a tela avisa
**\* Maximos comensais nao cadastrados \***, zera o campo de posição e encerra a
listagem.

[?] O aviso fala de "máximos comensais", e a condição que o dispara é a secretaria não ter
nenhum segmento com percentual registrado: nada no acervo lido liga as duas coisas. Ou o
texto é de outro caso, ou o aviso está no lugar errado. Pergunta ao site.

[?] O aviso está guardado também por uma condição de página — só a primeira linha da
página o dispara. O acervo mostra dois caminhos de entrada no programa, e a passagem que
monta a página é a de um deles; se a abertura vinda do menu percorre o outro, o aviso não
aparece. Pergunta ao site.

### RN-11 — Nada acontece sem a segurança do perfil, da rota e da operação

Antes de montar a lista, a tela leva a sessão à **segurança do perfil**: o cadastro de
telas e o cadastro que libera, por código de acesso e por tela, cada operação. Não estando
a tela cadastrada, a recusa é **\* Tela nao disponivel \***; não estando ela liberada para
o código de acesso da sessão, a recusa é **\* Acesso negado para esta matricula \***. Nas
duas, a lista não é montada e a sessão volta ao menu principal.

Na confirmação, a tela leva o contexto da sessão à **segurança da rota** e à **da
operação**. A rota recusa a operação informada quando ela não é permitida naquele ponto,
com **\* Operacao nao disponivel \***; e o cadastro de acesso recusa a operação informada
quando ele não a libera para aquela tela, com **\* Acesso negado para esta operacao \***.
Em qualquer recusa, nada é lido e nada é entregue à tela seguinte.

A operação desta tela é a **consulta**: é ela que a tela apresenta e é ela que segue para
as conferências de segurança.

[?] A tela carrega dois campos que a conferência de rota usa para desviar para outra tela
— um código de próxima tela e o campo da operação —, e o acervo lido não mostra quem os
preenche na máscara desta tela. Se a máscara os traz preenchidos, o servidor pode ser
levado a outra tela em vez de consultar; se não, esses desvios nunca acontecem. Pergunta
ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta dos segmentos de atendimento com percentual registrado

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C270C

  Cenário: A lista dos segmentos com percentual registrado
    Dado que a minha secretaria tem segmentos com percentual registrado
    Quando abro a tela C270C
    Então vejo a lista daqueles segmentos

  Cenário: A secretaria da lista é a da sessão
    Dado que a minha sessão tem uma secretaria
    Quando abro a tela C270C
    Então a lista é a daquela secretaria
    E a tela não me pergunta de qual secretaria se trata

  Cenário: O cabeçalho traz a secretaria e a data do sistema
    Quando abro a tela C270C
    Então vejo a descrição do tipo de órgão da minha sessão
    E vejo a data do sistema

  Cenário: A lista mostra até treze linhas
    Dado que a minha secretaria tem mais segmentos do que cabem na página
    Quando abro a tela C270C
    Então a lista mostra no máximo treze linhas
    E as linhas restantes ficam em branco

  Cenário: Cada linha traz o código, a descrição e a situação
    Dado que existe um segmento com percentual registrado
    Quando abro a tela C270C
    Então a linha daquele segmento traz o código, a descrição e a situação

  Cenário: Vários tipos de refeição no mesmo segmento
    Dado que o segmento tem percentual registrado para mais de um tipo de refeição
    Quando abro a tela C270C
    Então aquele segmento aparece em uma só linha

  Cenário: A descrição vem do cadastro de segmentos
    Dado que o segmento listado está cadastrado com uma descrição
    Quando abro a tela C270C
    Então a linha mostra a descrição registrada no cadastro daquele segmento

  Cenário: Informar um segmento reposiciona a lista
    Dado que a minha secretaria tem vários segmentos com percentual registrado
    Quando informo no campo de posição um segmento cadastrado e confirmo
    Então a leitura da lista recomeça por aquele segmento

  Cenário: Informar um segmento que não está cadastrado
    Quando informo no campo de posição um segmento que não está no cadastro e confirmo
    Então a leitura da lista recomeça pelo primeiro segmento cadastrado da secretaria

  Cenário: Sem escolha, a tela só volta a se mostrar
    Dado que estou na tela C270C
    Quando confirmo sem escolher um segmento
    Então a tela continua em consulta
    E nenhuma outra tela é aberta

  Cenário: Escolher um segmento abre a manutenção do percentual
    Dado que a linha de um segmento está marcada
    Quando confirmo com o código daquele segmento
    Então a tela C270T abre em consulta, com aquele segmento escolhido

  Cenário: Digitação não numérica no código do segmento ou na posição
    Dado que digito no código do segmento ou no campo de posição algo que não é número
    Quando confirmo
    Então o sistema recusa a digitação antes de listar qualquer registro

  Cenário: Secretaria sem segmento com percentual registrado
    Dado que a minha secretaria não tem nenhum segmento com percentual registrado
    Quando abro a tela C270C
    Então vejo a mensagem "* Maximos comensais nao cadastrados *"
    E a listagem termina

  Cenário: A tela não cadastrada
    Dado que a tela não está cadastrada no cadastro de telas
    Quando abro a tela C270C
    Então vejo a mensagem "* Tela nao disponivel *"
    E a lista não é montada

  Cenário: A tela não liberada para o meu código de acesso
    Dado que a tela não está liberada para o código de acesso da minha sessão
    Quando abro a tela C270C
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E a lista não é montada

  Cenário: Operação não permitida pela rota
    Dado que estou na tela C270C
    Quando confirmo com uma operação que a rota não permite naquele ponto
    Então vejo a mensagem "* Operacao nao disponivel *"
    E nada é lido nem entregue à tela seguinte

  Cenário: Operação não liberada para o meu código de acesso
    Dado que estou na tela C270C
    Quando confirmo com uma operação que o meu cadastro de acesso não libera
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é lido nem entregue à tela seguinte

  Cenário: A consulta não grava nada
    Dado que abro a tela C270C
    Quando a lista é mostrada e escolho um segmento
    Então nenhum registro é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado
```
