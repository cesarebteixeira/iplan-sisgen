# US — N027T — Exclusão do lote de notas fiscais

## Estória

Como **servidor da CRE**, quero **consultar as notas fiscais de um lote e excluir o lote lançado por engano**,
para que **as quantidades e os valores daquele lote voltem ao contrato e ao pedido e a execução fique só com o que
foi entregue de fato**.

Um lote reúne as notas fiscais de um mesmo processo, de um fornecedor. Esta é a tela que desfaz o lote inteiro — as
notas, os itens das notas, o contrato e o pedido — e é também a que mostra o que o lote tem antes de desfazer. Sem
ela, um lote lançado por engano continua consumindo o contrato para sempre. Toda exclusão confirmada fica registrada
para auditoria; a consulta, não.

## Contexto

Jornada S000M → N000M → N050M → N027T.

Ator: servidor de CRE — informa o número do processo do lote, confere as notas fiscais que o lote tem e, quando o
lote está errado, pede a exclusão e responde à confirmação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu a abre —
está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de negócio.

As telas anteriores da jornada só encaminham: o que a N027T usa — a matrícula, o código de acesso, o privilégio, o
tipo de órgão e a coordenadoria regional escolar — é o que a entrada deixou na sessão, e a tela o aplica nas
conferências e nas chaves de todas as leituras. As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela trabalha em consulta ou em exclusão, e mais nada

A tela é aberta em um de dois modos: consulta ou exclusão. Qualquer outro modo é recusado com
* Operacao nao disponivel * e o cursor volta ao campo do modo; a conferência é feita uma vez por página. Quando o
modo chega em branco, a tela assume consulta — é sempre em consulta que ela se apresenta pela primeira vez. Voltar
de exclusão para consulta cancela a exclusão que estivesse pedida.

### RN-02 — A tela não é de consulta: ela apaga o lote e desfaz o que ele consumiu

A tela enxerga dez cadastros — o registro das telas, o das notas fiscais, o dos órgãos, o dos fornecedores, o das
notas fiscais no processo, o dos itens das notas, o dos contratos, o da auditoria, o dos itens dos pedidos e o dos
pedidos. Escreve em seis deles: apaga as notas do lote, apaga os itens dessas notas, atualiza o contrato, o item do
pedido e o pedido, e cria o rastro de auditoria. Os cadastros de negócio não recebem registro novo: as gravações são
atualizações de registros que já existiam e as duas exclusões são apagamentos — a única criação é o registro de
auditoria. O que ela escreve depende do modo (RN-01) e da confirmação (RN-09); em consulta, nada é escrito (RN-15).

### RN-03 — O número do lote é obrigatório

O lote é identificado pelo número do processo, informado em quatro partes que compõem quatorze dígitos. Sem ele, a
recusa é * Informe o numero do lote *, com o cursor no primeiro campo do número. Um lote diferente do último
consultado reinicia a leitura: a tela volta a mostrar as notas desde a primeira.

### RN-04 — O lote tem de estar cadastrado, e o fornecedor dele é o que a tela mostra

Informado o número, a tela procura as notas daquele lote. Não encontrando nenhuma, recusa com
* Lote nao cadastrado *, no campo do número. Encontrando, ela toma do lote o fornecedor, o tipo de contrato e o nome
do fornecedor e os apresenta no cabeçalho — o fornecedor não é digitado, vem do próprio lote.

[?] O fornecedor do lote não precisa estar no cadastro de fornecedores para a exclusão acontecer: se o cadastro não
for encontrado, ou estiver marcado como excluído, a tela segue sem avisar, apenas sem mostrar o nome. Pergunta ao
site se é intencional.

### RN-05 — O acesso ao lote é conferido pela coordenadoria do operador

O lote é liberado quando a coordenadoria regional escolar da sessão é a mesma da primeira nota do lote; quando a
sessão não carrega coordenadoria, a tela não restringe. Fora disso, a recusa é
* Usuario sem acesso aos grupos deste lote *, com o cursor no número do lote.

[?] A conferência olha só a primeira nota do lote (a primeira na ordem do sistema), e a exclusão apaga todas as notas daquele
fornecedor no lote sem reconferir a coordenadoria de cada uma — e a própria mensagem fala em "grupos deste lote",
no plural. Se um lote pode reunir notas de mais de uma coordenadoria, o operador de uma delas apaga as notas das
outras. Pergunta ao site.

### RN-06 — Lote sem notas é avisado

Quando a leitura que monta a lista não encontra nota nenhuma, a tela não monta lista e avisa
* Lote sem notas cadastradas *.

[?] A tela tem duas recusas muito próximas — * Lote nao cadastrado * e * Lote sem notas cadastradas * — e o fonte
não deixa claro o que separa uma da outra: as duas dependem de a leitura do lote não encontrar registro, e a
diferença está em qual passo da transação faz a leitura. Confirmar com o site qual das duas o operador deve ver em
cada situação.

### RN-07 — A tela lista as notas do lote em treze linhas

A lista tem treze linhas, e cada linha traz o número da nota fiscal, a data da nota, a coordenadoria, o órgão e o
seu nome e o valor da nota. No cabeçalho ficam o modo de operação, o tipo de órgão, a data do sistema, as quatro
partes do número do lote, o tipo de contrato, o código e o nome do fornecedor, a linha de mensagem e o campo da
resposta da confirmação.

[?] As treze linhas são lidas uma a uma, e a leitura guarda o número da última nota lida na área de trabalho da
tela. Um lote com mais de treze notas não cabe numa apresentação, e o fonte não mostra como o operador percorre as
demais — se a apresentação seguinte continua de onde parou ou volta ao começo depende de estado que a tela não
expõe. Pergunta ao site.

### RN-08 — A exclusão exige a consulta anterior do lote

Para excluir, o lote tem de ter sido consultado na tela: pedida a exclusão de um lote que não passou pela consulta na
apresentação anterior, a recusa é * Consulte antes de excluir *, com o cursor no campo do modo, e nada é apagado.

### RN-09 — A exclusão é pedida e confirmada antes de acontecer

Pedida a exclusão, a tela não apaga: ela apresenta * Confirma exclusao do lote <S/N> ? * e espera a resposta. Só a
resposta afirmativa segue; qualquer outra resposta desfaz o pedido e nada é apagado. A pergunta é feita uma vez por
pedido, e a exclusão só acontece depois da resposta.

### RN-10 — A exclusão apaga o lote inteiro, não só as linhas da lista

Confirmada, a exclusão percorre o lote desde a primeira nota e não para nas treze que estavam na tela: cada nota é
apagada junto com os seus itens, até o lote acabar.

### RN-11 — A exclusão devolve ao contrato a quantidade e o valor dos itens

Para cada item da nota, a tela procura o contrato daquele material — mesmo tipo de contrato, fornecedor,
coordenadoria, subclasse e gênero, com o limite de vigência na data da nota — e devolve ao contrato a quantidade e o
valor do item. A devolução só acontece quando o contrato é encontrado e a nota não é anterior ao início da vigência
dele.

[?] A exclusão segue e apaga a nota mesmo quando o contrato não é encontrado ou quando a nota é anterior ao início
da vigência; nesse caso a quantidade e o valor ficam consumidos no contrato e ninguém avisa o operador. Confirmar se
é intencional.

[?] O saldo de pedido do contrato recebe de volta a quantidade do item só quando o item **não** tem pedido; quando o
item tem pedido, esse saldo não é tocado. A condição está invertida em relação ao resto da devolução: confirmar se é
assim mesmo.

### RN-12 — A exclusão atualiza o item do pedido e o pedido

Para cada item da nota preso a um pedido, a tela reduz a quantidade recebida daquele item no pedido, marca a
situação do item como "A" e guarda quem estornou e a data do estorno; e, quando a situação do pedido era "F", passa
a do pedido para "A" também. Se o item da nota não tem pedido, nada disso é feito.

[?] O que as situações "A" e "F" do pedido e do item significam não está no acervo: o fonte testa "F" e grava "A", e
nenhuma mensagem ou rótulo do lote traduz essas letras. Pergunta ao site.

### RN-13 — O contrato das notas antigas é procurado pelo tipo de contrato convertido

Antes de procurar o contrato, a tela converte o tipo de contrato das notas anteriores a 2004: no tipo de órgão 01,
o tipo de contrato 15 passa a 2; no tipo de órgão 02, o tipo 2 passa a 1. Para as notas de 2004 em diante, o tipo é
usado como está.

### RN-14 — A exclusão deixa rastro de auditoria, menos na atualização do pedido

Cada operação confirmada grava um registro de auditoria com o objeto auditado, o tipo de operação, o conteúdo do
cadastro antes e depois da mudança, a matrícula, a data e a hora da sessão, o terminal e o processo. Uma nota com
itens deixa: um registro para o contrato (quando o contrato é atualizado), um para o item do pedido (quando o item é
encontrado), um para cada item da nota apagado e um para a nota apagada. A atualização do pedido é o único passo que
não deixa registro.

[?] O processo e a coordenadoria que vão no rastro de auditoria saem do primeiro item lido no lote e ficam guardados
desde então; nas notas seguintes do mesmo lote a auditoria continua registrada com a coordenadoria e o processo
daquela primeira nota. Confirmar se era essa a intenção.

### RN-15 — A consulta não grava nada

Em consulta a tela lê e mostra, e não escreve em cadastro nenhum: nenhum registro é incluído, alterado ou excluído,
e nenhum registro de auditoria é criado.

### RN-16 — Nada é apagado sem a conferência de sessão, de tela, de rota e de permissão

Ao trabalhar, a tela confere: o servidor tem de estar no terminal em que a sessão foi aberta — em outro, o acesso é
encerrado; a tela tem de estar registrada, senão * Tela nao disponivel *; o código de acesso do servidor tem de
alcançar a tela, senão * Acesso negado para esta matricula *; e a operação pedida tem de estar liberada para esse
código, senão * Acesso negado para esta operacao *. A rota ainda confere a tela: uma tela fora do registro é
recusada com * Tela nao cadastrada *. Sem passar por tudo, nada é apagado e nada é atualizado.

### RN-17 — A tela não apresenta a recusa de destino inválido

A recusa de **destino inválido** existe no trecho que a tela executa para gravar a auditoria, e a ficha estrutural
da tela a lista entre as suas mensagens. Esse caminho só roda com o modo de distribuição automática preenchido, e a
própria tela limpa esse campo imediatamente antes de executar o trecho. Pela N027T, portanto, essa mensagem não é
apresentada.

### RN-18 — Prefixo de tela preenchido abandona a exclusão

Se a transação chega com o prefixo de tela preenchido, a preparação para antes de qualquer conferência de modo ou de
lote: nada é apagado e nada é gravado.

[?] O que preenche o prefixo de tela não está no acervo: não se sabe quem manda prefixo para a N027T.

---

## Cenários BDD

```gherkin
Funcionalidade: Exclusão do lote de notas fiscais

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o código de acesso, o privilégio, o tipo de órgão e a coordenadoria regional escolar
    E tenho acesso à tela N027T

  Cenário: A tela só aceita consulta e exclusão
    Dado que estou na tela N027T
    Quando peço um modo de operação que não é consulta nem exclusão
    Então vejo "* Operacao nao disponivel *"
    E o cursor fica no campo do modo
    E nada é apagado

  Cenário: A tela abre em consulta
    Dado que abro a tela N027T sem informar o modo de operação
    Então a tela me apresenta em consulta

  Cenário: Voltar para consulta cancela a exclusão pedida
    Dado que pedi a exclusão de um lote na tela N027T
    Quando volto o modo para consulta
    Então a exclusão deixa de estar pedida
    E a confirmação não me é apresentada
    E nada é apagado

  Cenário: A consulta mostra as notas do lote e o valor de cada uma
    Dado que estou na tela N027T em consulta
    Quando informo o número do lote
    Então vejo as notas do lote em até treze linhas, cada uma com o número da nota,
      a data, a coordenadoria, o órgão e o seu nome e o valor
    E vejo no cabeçalho o tipo de contrato e o código e o nome do fornecedor do lote

  Cenário: A consulta não grava nada
    Dado que consultei um lote na tela N027T
    Quando a consulta termina
    Então nenhum cadastro é incluído, alterado ou excluído
    E nenhum registro de auditoria é criado

  Cenário: O número do lote é obrigatório
    Dado que estou na tela N027T
    Quando confirmo sem informar o número do lote
    Então vejo "* Informe o numero do lote *"
    E o cursor fica no primeiro campo do número do lote
    E nada é apagado

  Cenário: Lote não cadastrado é recusado
    Dado que estou na tela N027T
    Quando informo um número de lote que não existe
    Então vejo "* Lote nao cadastrado *"
    E o cursor fica no número do lote
    E nada é apagado

  Cenário: Lote sem notas é avisado
    Dado que estou na tela N027T
    Quando o lote informado não tem nota nenhuma para mostrar
    Então vejo "* Lote sem notas cadastradas *"
    E nenhuma lista de notas é montada
    E nada é apagado

  Cenário: O acesso ao lote é conferido pela coordenadoria da sessão
    Dado que a minha sessão carrega uma coordenadoria regional escolar
    Quando consulto um lote cuja primeira nota é de outra coordenadoria
    Então vejo "* Usuario sem acesso aos grupos deste lote *"
    E o cursor fica no número do lote
    E nada é apagado

  Cenário: Sem coordenadoria na sessão, a tela não restringe o lote
    Dado que a minha sessão não carrega coordenadoria regional escolar
    Quando consulto um lote de qualquer coordenadoria
    Então as notas do lote me são apresentadas

  Cenário: A exclusão exige a consulta anterior do lote
    Dado que estou na tela N027T e peço a exclusão de um lote que não consultei antes
    Quando confirmo a exclusão
    Então vejo "* Consulte antes de excluir *"
    E o cursor fica no campo do modo
    E nada é apagado

  Cenário: A exclusão é confirmada antes de acontecer
    Dado que consultei o lote e peço a sua exclusão
    Quando confirmo
    Então vejo "* Confirma exclusao do lote <S/N> ? *"
    E a exclusão só acontece depois da minha resposta afirmativa

  Cenário: A exclusão é desfeita quando a resposta não é afirmativa
    Dado que vejo a pergunta de confirmação da exclusão do lote
    Quando respondo que não
    Então o pedido de exclusão é desfeito
    E nada é apagado

  Cenário: A exclusão apaga o lote inteiro, e não só o que está na tela
    Dado que consultei um lote com mais notas do que as que a lista mostra
    E peço a sua exclusão e confirmo
    Quando a exclusão acontece
    Então todas as notas daquele lote são apagadas, com os seus itens
    E não apenas as notas que estavam na lista

  Cenário: A exclusão devolve ao contrato a quantidade e o valor dos itens
    Dado que o lote excluído tem itens de um contrato vigente na data da nota
    Quando a exclusão acontece
    Então a quantidade do item volta ao contrato
    E o valor do item volta ao contrato

  Cenário: O contrato fora da vigência não é tocado e a nota é apagada assim mesmo
    Dado que o contrato do item não é encontrado, ou que a nota é anterior ao início da vigência dele
    Quando a exclusão acontece
    Então o contrato não é atualizado
    E a nota e os seus itens são apagados do mesmo jeito

  Cenário: A exclusão atualiza o item do pedido e o pedido
    Dado que a nota excluída tem item preso a um pedido
    Quando a exclusão acontece
    Então a quantidade recebida daquele item no pedido é reduzida
    E a situação do item do pedido passa a "A", com quem estornou e a data do estorno
    E, se a situação do pedido era "F", ela passa a "A"

  Cenário: O contrato das notas antigas é procurado pelo tipo convertido
    Dado que a nota é de antes de 2004
    Quando a exclusão procura o contrato do item
    Então o tipo de contrato usado é o convertido para o tipo de órgão da sessão

  Cenário: A atualização do pedido não deixa auditoria
    Dado que confirmei a exclusão de um lote com item de pedido
    Quando a tela atualiza o pedido
    Então nenhum registro de auditoria é gravado para essa atualização
    E as demais operações da exclusão deixam o seu registro

  Cenário: Nada é apagado sem a conferência de sessão, de tela, de rota e de permissão
    Dado que estou na tela N027T e pedi a exclusão de um lote
    Quando a conferência do terminal, do registro da tela, do código de acesso,
      da permissão de excluir ou do registro da rota não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *",
      "* Acesso negado para esta operacao *" ou "* Tela nao cadastrada *"
    E nada é apagado e nada é atualizado
    E, se o terminal não for o da sessão, o acesso é encerrado

  Cenário: A recusa de destino inválido não é apresentada
    Dado que estou na tela N027T e excluí um lote
    Quando a tela grava o registro de auditoria
    Então a tela limpa o modo de distribuição automática
    E a recusa de destino inválido não é apresentada

  Cenário: Prefixo de tela preenchido abandona a exclusão
    Dado que a transação chega à N027T com prefixo de tela preenchido
    Quando a preparação começaria
    Então nenhuma conferência de modo ou de lote é feita
    E nada é apagado e nada é gravado
```
