# US — N011C — Consulta das notas fiscais de um processo

## Estória

Como **servidor de CRE**, quero **consultar um processo da minha secretaria com as notas
fiscais que o compõem**, para que **eu confira, numa só tela, o fornecedor, a fonte do
recurso, o tipo e a situação do processo, quantas notas fiscais ele tem e quanto elas
somam**.

O processo é por onde a despesa da secretaria caminha, e é o conjunto das notas fiscais
dele — quantas são e quanto valem — que a coordenação acompanha. Sem esta consulta, o
servidor que tem a nota na mão não teria como conferi-la contra o que o sistema
registrou, e dependeria de quem mantém os cadastros para saber em que pé está o
processo. A tela é só de leitura: quem inclui, altera ou exclui nota fiscal é outra
tela, e esta não grava, não exclui e não deixa rastro de auditoria.

## Contexto

Jornada S000M → N000M → N060M → N011C.

Ator: servidor de CRE — consulta um processo da sua secretaria e as notas fiscais que o
formam.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. Os dois menus do caminho (N000M e
N060M) não gravam nada: apenas encaminham. Da sessão, a N011C usa a secretaria e a
coordenadoria do servidor e o cabeçalho que exibe — a descrição do órgão e a data do
sistema; essa carga é regra da entrada e está no anexo, em **Regras que se revelaram da
entrada**.

A N011C é a última tela da jornada: ela não encadeia em outra. E o modo dela não depende
de quem a chamou — não há comparação com a tela de origem em ponto nenhum do programa,
e é a própria tela que repõe a consulta antes de operar (RN-06).

## Regras de negócio

### RN-01 — A tela é de consulta: nada é gravado

A tela abre em modo de consulta e repõe esse modo ao montar a página, de modo que a opção
da transação volta a ser sempre a consulta. Nenhuma inclusão, alteração, exclusão ou
travamento de registro é executado, e nenhuma linha de auditoria é criada: a única
operação que a tela faz sobre os cadastros que enxerga é ler.

### RN-02 — A tela mostra um processo e as notas fiscais que o formam

A consulta devolve o processo e as suas notas fiscais. Do processo, a tela mostra a
situação, o tipo por extenso, a quantidade de notas e o valor somado; de cada nota
fiscal, o número, a data e o valor. Do fornecedor, a razão social; da fonte de recurso, a
descrição. No cabeçalho, a descrição do órgão e a data do sistema.

A lista é uma página de **treze notas fiscais**; cada linha traz o número da nota, a data
e o valor. O cadastro das notas fiscais tem **39 campos** e capacidade para
**29.000.000** registros — capacidade é o máximo esperado, parâmetro de dimensionamento,
não o que está cadastrado.

### RN-03 — O número do processo tem catorze dígitos em quatro partes, e a secretaria é a da sessão

O número do processo tem catorze dígitos e é informado na tela em quatro partes, que o
sistema junta antes de consultar. A primeira parte, de dois dígitos, é o **COD.
SECRETARIA**; a terceira, de seis, é o **COD LOTE**; a segunda e a quarta não têm rótulo
próprio na tela. O **COD. SECRETARIA** não precisa ser digitado: ao montar a página, o
sistema repõe o campo com o código da secretaria do servidor, lido no cadastro de órgãos
pela secretaria da sessão, de modo que o que o operador tiver digitado ali é substituído.

Ao remontar os campos a partir do número já guardado, o sistema reconhece **dois
arranjos** do mesmo número: no mais comum, a secretaria ocupa as duas primeiras posições
e as partes seguem na ordem; quando essas duas primeiras posições estão zeradas, a
secretaria é lida nas duas posições seguintes e o restante segue igual.

[?] O material lido não diz o que são a segunda e a quarta partes do número — as duas sem
rótulo na tela — nem o que distingue os dois arranjos: se são duas gerações do mesmo
número, um prefixo opcional, ou composições diferentes. Pergunta ao site.

### RN-04 — Sem o número do processo a consulta não começa

Montado o número, se ele ficar todo em zero o sistema recusa com
**\* Informe o numero do processo \*** e devolve o cursor ao número do processo. A recusa
vem depois das conferências de acesso e antes de qualquer leitura das notas fiscais.

[?] Como o COD. SECRETARIA é reposto pelo sistema com a secretaria do servidor, o número
só fica todo em zero se essa secretaria não tiver código no cadastro de órgãos, ou se os
quatro campos vierem todos em branco. O material lido não mostra em que circunstância
isso acontece. Pergunta ao site.

### RN-05 — O processo tem de ter nota fiscal cadastrada

Não havendo nota fiscal para o processo, a consulta não mostra nada e o sistema avisa.
São **duas** mensagens, conforme a passagem: **\* Processo nao cadastrado \***, com o
cursor de volta ao número do processo, e **\* Processo sem notas cadastradas \***, sem
posicionar o cursor.

[?] As duas mensagens vêm da mesma ausência — nenhuma nota fiscal para o processo —
apurada em duas passagens diferentes do programa. O material lido não diz qual delas o
operador vê numa consulta feita por esta jornada. Pergunta ao site.

### RN-06 — A tela só opera em consulta

A tela é de uso exclusivo da consulta, e é ela que repõe a consulta na opção antes de
entregá-la às conferências de rota e de permissão. Há uma recusa preparada para quando a
opção que chega não é a consulta: **\* Operacao nao disponivel. Use CON \***, com o
cursor no campo da opção e antes de qualquer leitura das notas fiscais.

Essa recusa só é alcançada por quem chega com um código de manutenção — inclusão,
alteração ou exclusão — e tem a permissão daquela operação. Com qualquer outro valor que
não seja a consulta, quem recusa primeiro é a conferência de rota, com a mensagem
**\* Operacao nao disponivel \***, que não diz ao operador qual valor serve.

[?] Há dois vocabulários para a mesma consulta: o texto que o operador lê manda usar
"CON" e o programa exige o código interno de consulta, que é outro. Se o operador digitar
"CON", quem recusa é a conferência de rota, com a mensagem sem "Use CON". O material lido
não mostra a camada que converte um vocabulário no outro nem a máscara da tela, que diria
se o campo da opção é apresentado ao operador. Pergunta ao site.

### RN-07 — Os campos informados são conferidos como números

Os **dez** campos informados na tela — as quatro partes do número do processo, a
coordenadoria regional escolar, o tipo de contrato, o fornecedor, a fonte do recurso, o
tipo de processo e o número da nota fiscal — são conferidos como números, cada um com a
sua quantidade de dígitos. Campo em branco é tratado como zero, e os separadores de
milhar são retirados antes da conferência. Achado conteúdo que não seja número, a linha é
recusada.

[?] A rotina que faz a conferência numérica não tem fonte no material lido, e o programa
só devolve o cursor para **três** dos dez campos conferidos — as duas partes do número do
processo que não têm rótulo e o código do lote. Nos outros sete a linha é recusada sem
que a tela indique onde está o erro. Pergunta ao site.

### RN-08 — Nota fiscal marcada como excluída não aparece

A leitura das notas fiscais descarta as que estão marcadas como logicamente excluídas no
cadastro: elas não entram na lista, não entram na contagem e não entram no valor somado
do processo. O corte é o mesmo na leitura que procura uma nota e na que percorre o
processo inteiro.

### RN-09 — Fornecedor, fonte e tipo do processo aparecem por extenso

A tela não mostra só códigos: do fornecedor ela traz a razão social, da fonte de recurso
a descrição, e do processo o tipo por extenso. Três dessas leituras são da secretaria da
sessão — a fonte, o processo e o tipo do processo —, enquanto a do fornecedor é do
cadastro único do sistema, que não pertence a órgão e por isso é achada só pelo código do
fornecedor. Os dados de fornecedor, fonte, tipo e situação vêm da **primeira nota fiscal
do processo**, a de menor número.

Os cadastros consultados têm estas capacidades: fornecedores, **10.000**; fontes de
recurso, **1.000**; processos, **40.000**; tipos de processo, **1.000**; órgãos da
secretaria, **200**; empenhos, **10.000.000**. E estes tamanhos: o cadastro de
fornecedores tem **19 campos**, o de fontes de recurso **5**, o de processos **3** e o
dos tipos de processo **3**.

### RN-10 — A situação do processo vem do empenho da primeira nota

A situação mostrada para o processo é **FECHADO** por padrão. Quando a primeira nota
fiscal do processo — a de menor número — está marcada com a situação que libera a busca,
o sistema lê o empenho do processo e mostra **PRE LIQUIDADO**, **LIQUIDADO** ou
**PAGO**, conforme a situação do empenho.

[?] O material lido não traz o catálogo dos valores da situação da nota fiscal: sabe-se
apenas que um deles — "P" — é o que libera a busca do empenho. Qual rótulo de negócio
corresponde a "P"? E o que significa, para o negócio, a situação de empenho que não é nem
"PRE" nem "LIQ", que a tela mostra como pago? Pergunta ao site.

### RN-11 — A tela conta as notas fiscais do processo e soma os seus valores

Ao carregar um processo, o sistema percorre todas as notas fiscais dele — as que não
estão excluídas —, conta quantas são e soma os seus valores. A quantidade aparece no
campo próprio e o valor somado, no valor total do processo; não havendo valor, os dois
campos aparecem em branco em vez de zero.

### RN-12 — A data da nota e os valores são apresentados no formato da tela

A data da nota fiscal é guardada no cadastro em três partes — ano, mês e dia —, e a tela
as junta e apresenta como dia-mês-ano, apoiada na rotina comum de conversão de data. Os
valores são apresentados com separador decimal.

### RN-13 — Os campos informados fora do número do processo não comandam a consulta

A coordenadoria regional escolar, o tipo de contrato, o fornecedor, a fonte do recurso e
o tipo de processo não entram em nenhuma chave de leitura: quem comanda a consulta é o
número do processo. Depois de ler, o sistema reescreve esses cinco campos com o que está
no processo e nas notas, de modo que o que o operador digitou neles é substituído pelos
valores do cadastro.

A leitura do processo começa sempre pela sua **primeira nota fiscal**, independentemente
do número de nota que esteja informado no campo próprio.

[?] O número da nota fiscal aparece na tela e passa pela conferência de número, mas não
posiciona a leitura. Se ele deveria servir de ponto de partida — o rótulo sugere isso —
ou se é apenas a nota da primeira linha exibida, o material lido não diz. Pergunta ao
site.

[?] Se a coordenadoria, o tipo de contrato, o fornecedor, a fonte e o tipo de processo
deveriam filtrar a consulta. Os cinco passam pela conferência numérica, mas não entram em
nenhuma chave e são substituídos depois da leitura. Ou são campos de saída que a máscara
deixou editáveis, ou o filtro ficou sem efeito. Pergunta ao site.

### RN-14 — Cada consulta começa com os campos de resultado limpos

Antes de conferir a digitação, os **oito** campos de resultado — descrição do órgão, data
do sistema, razão social do fornecedor, quantidade de notas, descrição da fonte, valor
total do processo, descrição do processo e valor total da nota — são apagados. Uma
consulta recusada, portanto, não deixa na tela o resultado da consulta anterior.

### RN-15 — O cabeçalho traz a descrição do órgão e a data do sistema

O cabeçalho da tela mostra a descrição do órgão e a data do sistema. A tela não os
calcula: ela copia os dois da área de trabalho da sessão.

[?] O material lido não mostra quem preenche a área que a tela lê. A entrada deixa a data
do sistema e a descrição do órgão na área da sessão; se a área que a tela lê não recebe
esses valores, os dois campos saem em branco. Pergunta ao site.

### RN-16 — A consulta só é montada com o acesso, a rota e a permissão confirmados

Antes de ler qualquer cadastro, a tela confere o acesso do servidor à própria tela e, na
passagem em que ele confirma, a rota e a permissão por operação, levando a matrícula, o
código de acesso, o privilégio, a secretaria e a coordenadoria da sessão. Qualquer uma
dessas conferências que não devolva tudo certo limpa o estado e encerra: nada é lido e
nada é mostrado.

[?] A permissão por operação não exige o indicador de consulta: a rotina comum confere
inclusão, alteração e exclusão, e no caminho da consulta não lê indicador algum. Se a
intenção era exigir a permissão de consulta por tela, o caminho não a exige. Pergunta ao
site.

### RN-17 — O campo de próxima tela preenchido desvia a transação

A tela leva o seu campo de próxima tela para a conferência de rota; preenchido, a
transação é encaminhada para a tela indicada e esta encerra antes de ler as notas
fiscais.

[?] Nenhum programa da jornada atribui valor a esse campo, e o material lido não mostra
quem o preenche. Pergunta ao site.

### RN-18 — Repetir a consulta do mesmo processo não percorre as notas de novo

A tela guarda, entre uma consulta e outra, o processo que já carregou. Informando o mesmo
processo outra vez, o sistema reaproveita o que já tem e não percorre as notas fiscais de
novo; a varredura só acontece quando o processo informado é diferente do que estava
carregado.

[?] Por quanto tempo a tela guarda o processo já carregado — até a consulta seguinte, até
o fim da sessão, ou mais — depende de quanto tempo vive a área livre da transação, e o
material lido não define isso. Pergunta ao site.

[?] Repetindo o mesmo processo, a quantidade de notas e o valor somado mostrados são os
da consulta anterior: se o cadastro mudou nesse meio-tempo, a tela mostra o número
antigo. O material lido não mostra nenhuma invalidação desse guardado. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consulta das notas fiscais de um processo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N011C

  Cenário: RN-01 — consultar não grava nada
    Dado que estou na tela N011C
    Quando consulto um processo e percorro as suas notas fiscais
    Então nenhuma nota fiscal é incluída, alterada ou excluída
    E nenhum registro é travado
    E nenhum rastro fica na auditoria

  Cenário: RN-02 — a tela mostra o processo e as notas fiscais que o formam
    Dado que estou na tela N011C
    Quando consulto um processo que tem notas fiscais
    Então vejo a situação, o tipo por extenso, a quantidade de notas e o valor somado do processo
    E vejo o fornecedor e a fonte do recurso por extenso
    E vejo até treze notas fiscais, cada uma com número, data e valor
    E vejo no cabeçalho a descrição do órgão e a data do sistema

  Cenário: RN-03 — o número do processo em quatro partes, com a secretaria da sessão
    Dado que estou na tela N011C
    Quando a tela é montada
    Então o COD. SECRETARIA está preenchido com a secretaria da minha sessão, mesmo que eu tenha digitado outra
    E o COD LOTE e as outras duas partes do número compõem o número de catorze dígitos que será consultado

  Cenário: RN-04 — sem o número do processo a consulta não começa
    Dado que estou na tela N011C
    Quando o número do processo fica todo em zero
    Então vejo "* Informe o numero do processo *"
    E o cursor volta ao número do processo
    E nenhuma nota fiscal é lida

  Cenário: RN-05 — o processo tem de ter nota fiscal cadastrada
    Dado que estou na tela N011C
    Quando o processo informado não tem nota fiscal
    Então vejo o aviso de que não há notas para o processo
    E nada é mostrado na lista

  Cenário: RN-06 — opção diferente da consulta
    Dado que estou na tela N011C
    Quando a opção da transação não é a consulta
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor fica no campo da opção
    E nenhuma nota fiscal é lida

  Cenário: RN-06 — a tela repõe a consulta
    Dado que abro a tela N011C pelo menu
    Quando a tela é montada
    Então a opção da transação é a consulta
    E a tela opera em consulta

  Cenário: RN-07 — campo com texto
    Dado que estou na tela N011C
    Quando informo texto em qualquer dos dez campos conferidos
    Então a linha é recusada
    E nada é lido com essa digitação

  Cenário: RN-08 — nota fiscal excluída não aparece
    Dado que estou na tela N011C
    E que uma das notas fiscais do processo está marcada como excluída
    Quando consulto o processo
    Então essa nota não aparece na lista
    E ela não entra na contagem nem no valor somado

  Cenário: RN-09 — fornecedor, fonte e tipo do processo por extenso
    Dado que estou na tela N011C
    Quando consulto um processo cujo fornecedor, fonte e tipo estão cadastrados
    Então vejo a razão social do fornecedor e a descrição da fonte do recurso
    E vejo a descrição do tipo do processo

  Cenário: RN-10 — a situação do processo vem do empenho
    Dado que estou na tela N011C
    Quando consulto um processo cuja primeira nota está marcada com a situação que libera a busca
    Então vejo a situação do empenho: pré-liquidado, liquidado ou pago
    E quando a nota não está marcada assim, vejo o processo como fechado

  Cenário: RN-11 — a tela conta as notas fiscais do processo e soma os seus valores
    Dado que estou na tela N011C
    Quando consulto um processo com várias notas fiscais
    Então vejo quantas notas ele tem
    E vejo o valor somado delas
    E quando não há valor, os dois campos aparecem em branco

  Cenário: RN-12 — a data da nota e os valores no formato da tela
    Dado que estou na tela N011C
    Quando consulto um processo que tem notas fiscais
    Então a data de cada nota aparece como dia-mês-ano
    E os valores aparecem com separador decimal

  Cenário: RN-13 — os campos informados não comandam a consulta
    Dado que estou na tela N011C
    Quando informo coordenadoria, tipo de contrato, fornecedor, fonte e tipo de processo diferentes dos do processo
    Então a consulta é feita pelo número do processo
    E esses cinco campos me são devolvidos com os valores do processo e das notas
    E a lista começa na primeira nota fiscal do processo

  Cenário: RN-14 — cada consulta começa com os campos de resultado limpos
    Dado que estou na tela N011C
    E que a consulta anterior mostrou um processo
    Quando faço uma consulta que é recusada
    Então o resultado da consulta anterior não fica na tela

  Cenário: RN-15 — o cabeçalho traz a descrição do órgão e a data do sistema
    Dado que estou na tela N011C
    Quando a tela é montada
    Então vejo a descrição do órgão e a data do sistema

  Cenário: RN-16 — a consulta só é montada com as conferências confirmadas
    Dado que estou na tela N011C
    Quando a conferência de acesso, de rota ou de permissão não devolve tudo certo
    Então a tela encerra sem ler nada
    E nada é mostrado

  Cenário: RN-17 — o campo de próxima tela preenchido desvia a transação
    Dado que a transação chega à N011C com o campo de próxima tela preenchido
    Quando a tela seria montada
    Então a transação é encaminhada para a tela indicada
    E nenhuma nota fiscal é lida

  Cenário: RN-18 — repetir a consulta do mesmo processo não percorre as notas de novo
    Dado que estou na tela N011C
    E que acabei de consultar um processo
    Quando consulto outra vez o mesmo processo
    Então o sistema reaproveita o que já carregou
    E não percorre as notas fiscais de novo
```
