# US — N016C — Consulta de processo e notas fiscais

## Estória

Como **servidor de CRE que responde pelos processos de despesa da sua coordenadoria regional
escolar**, quero **consultar um processo pelo seu número, pelo número do processo SEI ou pelo
número do processo RIO e ver, numa só tela, a sua situação, os seus totais e as notas fiscais que
o formam**, para que **eu confira o que o sistema registrou, peça o relatório do processo e chegue
à tela que mantém as notas — tudo sem decorar número de processo**.

O processo é por onde a despesa da secretaria caminha, e é o conjunto das notas fiscais dele —
quantas são, quanto valem, de que fornecedor e de que fonte — que a coordenação acompanha. Esta
tela é a porta de entrada dessa conferência: é ela que acha o processo, que mostra os seus totais
e a sua relação de notas e que pede o impresso por correio eletrônico. Sem ela, quem tem a nota na
mão não teria por onde chegar ao processo pelo processo SEI, que é o número que circula no dia a
dia, e a conferência dependeria de quem digita a nota.

## Contexto

Jornada S000M → N000M → N060M → N016C.

Ator: servidor de CRE — consulta um processo da sua coordenadoria pelos seus identificadores,
confere os seus totais e a sua relação de notas fiscais e, marcando o indicador de consulta, abre
a tela de manutenção das notas sobre o mesmo processo.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

Os dois menus do caminho (**N000M** e **N060M**) são menus de verdade: não gravam nada e não
deixam nada para esta tela — não passam processo e não passam operação. A tela abre, portanto, em
branco, com o que a sessão já tinha. O contexto que ela usa da sessão — a **secretaria (o tipo de
órgão)**, a **coordenadoria regional escolar**, a **matrícula**, o **código de acesso**, o
**privilégio** e a **data do sistema** — é o que a entrada deixou; a regra é da entrada e está no
anexo de evidências, em **Regras que se revelaram da entrada**.

Esta tela **não muda conforme quem a chamou**: ela não compara a tela de origem com nenhum código
de tela. Quem muda conforme a origem é a tela seguinte — e é por isso que o que esta tela entrega
adiante é regra dela (RN-13).

## Regras de negócio

### RN-01 — A tela consulta um processo e a relação das suas notas fiscais

Esta é uma tela de **consulta**. Do processo, ela mostra a **situação**, a **quantidade de notas
fiscais**, o **valor total das notas**, o **valor total do imposto retido** e o **valor total a
pagar**. Do fornecedor, a **razão social**; da fonte do recurso, a **descrição**; do tipo do
processo, a **descrição**; do órgão da nota, o **nome**; e, no cabeçalho, o **nome da secretaria**
e a **data do sistema**.

A relação das notas fiscais é uma página de **nove** linhas. De cada nota, a linha traz o
**número de ordem da nota dentro do processo**, o **número da nota fiscal**, o **código do órgão**
e a **data da nota**; o nome do órgão e os valores da nota são preenchidos pelo sistema na mesma
linha.

A tela **não tem operação de manutenção**: nenhuma nota fiscal é incluída, alterada ou excluída
por ela e nenhum registro de auditoria é criado. Isso não quer dizer que ela não escreva: ela
numera notas (RN-08) e cria a requisição do relatório (RN-12).

[?] O número de ordem da nota dentro do processo e as partes do processo SEI e do processo RIO são
rotulados na tela apenas pelo nome interno do campo — ao contrário dos vizinhos, que trazem rótulo
de negócio ("COD. SECRETARIA", "COD LOTE", "CORD.REG.ESCOLAR", "TIPO DE CONTRATO"). O que o
servidor lê nesses campos é pergunta ao site.

### RN-02 — A tela só aceita a operação de consulta

Ao montar a página, a tela repõe a opção de consulta, de modo que o campo da opção volta a ser
sempre a consulta. Informada outra operação, ela recusa com **\* Opcao nao disponivel. Use CON \***,
com o cursor de volta ao campo da opção, e nada é lido.

A recusa vem **depois** das conferências de acesso, de rota e de permissão, e **antes** de o
sistema montar o número do processo: quem informou uma operação que não tem permissão é recusado
pela conferência de permissão, e não por esta mensagem.

### RN-03 — O processo é um número de 14 dígitos em quatro partes

O número do processo tem 14 dígitos e é informado na tela em quatro partes, que o sistema junta
antes de consultar. Na montagem principal, as duas primeiras posições são o **COD. SECRETARIA**,
as duas seguintes são uma parte sem rótulo na tela, da quinta à décima está o **COD LOTE** e as
quatro últimas são a outra parte sem rótulo.

Quando as duas primeiras posições do número guardado estão zeradas, o sistema desloca tudo em duas
posições: a secretaria passa para as posições 3 e 4 e as duas primeiras ficam em zero.

O **COD. SECRETARIA** não precisa ser digitado: o sistema repõe o campo com o código que o cadastro
de órgãos guarda para o tipo de órgão da sessão, de modo que o que o servidor tiver digitado ali é
substituído. E quando o cadastro daquele órgão estiver marcado como órgão do tipo "S", o sistema
também repõe a segunda parte do número com a **coordenadoria regional escolar da sessão**.

[?] O acervo não explica o deslocamento de duas posições nem o que distingue os dois formatos do
número — a mesma dúvida já registrada na estória da **N011C**, que consulta a mesma família de
processos. Nenhuma linha do acervo nomeia o prefixo que some no deslocamento. Pergunta ao site.

### RN-04 — O processo também é achado pelo processo SEI e pelo processo RIO

O servidor pode informar, em vez do número do processo, o **número do processo SEI** ou o **número
do processo RIO**, cada um em quatro partes. Informado o SEI, o sistema procura o processo por ele;
informado o RIO, procura por ele. Achando o registro, o sistema **adota o número do processo que
aquele registro trouxer** e segue a consulta por esse número — é assim que se chega ao processo
pelo número que circula no dia a dia.

Duas das partes do processo RIO e a terceira parte do SEI não são digitadas: as duas primeiras
partes do RIO vêm do cadastro do órgão da sessão e o ano, nas terceiras partes do SEI e do RIO, vem
da data do sistema.

### RN-05 — A consulta se limita aos processos da coordenadoria do servidor

Quando o servidor **tem** coordenadoria regional escolar na sessão e o processo consultado é de
**outra** coordenadoria, a tela recusa com **\* Usuario sem acesso ao grupo deste processo \***, com
o cursor de volta ao **COD LOTE**, e nada é mostrado. Quando o servidor **não tem** coordenadoria
na sessão, a tela não recusa por isto.

A conferência é feita sobre o processo já achado no cadastro — a coordenadoria vem do próprio
registro do processo, não do que o servidor digitou.

### RN-06 — O processo tem de estar cadastrado, por qualquer das três vias

Nenhuma das três procuras — pelo número do processo, pelo processo SEI e pelo processo RIO —
encontrando registro, a tela recusa, e cada via tem a sua mensagem:

- pelo número do processo e pelo **COD LOTE**: **\* Processo nao cadastrado \***, com o cursor de
  volta ao **COD LOTE**;
- pelo **processo SEI**: **\* SEI nao cadastrado \***, com o cursor de volta ao campo do SEI;
- pelo **processo RIO**: **\* PROCESSO RIO nao cadastrado \***, com o cursor de volta ao campo do
  RIO.

Nas três, nada é mostrado e a consulta para ali.

### RN-07 — O processo tem de ter nota fiscal cadastrada

Não havendo nota fiscal para o processo, a tela avisa **\* Processo sem notas cadastradas \***,
sem posicionar o cursor, e não mostra a relação nem os totais.

### RN-08 — A tela numera as notas fiscais que ainda não têm número de ordem

Ao percorrer as notas do processo para contá-las e somá-las, o sistema encontra cada nota que
**ainda não tem número de ordem dentro do processo**. Essas notas não ficam só sendo contadas: o
sistema trava o registro, grava nele o próximo número de ordem — começando em um, na ordem em que
as notas aparecem — e segue.

É a única gravação que a tela faz no cadastro das notas, e ela acontece em consulta: **consultar
um processo que tenha nota sem número de ordem muda o cadastro**.

[?] A numeração começa sempre em um a cada consulta e só avança sobre as notas que estão sem
número; se o processo tiver notas já numeradas e uma sem número, o número atribuído pode repetir um
que já existe. O acervo não diz se essa é a intenção nem o que acontece com a repetição. Pergunta
ao site.

### RN-09 — A situação do processo vem do empenho

A situação mostrada para o processo é **FECHADO** quando a nota fiscal não está marcada com a
situação que libera a busca; estando marcada, o sistema lê o empenho do processo e mostra
**PRE LIQUIDADO**, **LIQUIDADO** ou **PAGO**, conforme a situação do empenho.

[?] O acervo não traz o catálogo dos valores da situação da nota fiscal: sabe-se apenas que um
deles — "P" — é o que libera a busca do empenho. E, quando o empenho do processo não é achado, o
programa não testa a ausência antes de ler a situação: ele segue para a leitura do campo de
situação mesmo assim, de modo que o que o servidor vê nesse caso não se decide pelo fonte. Qual
rótulo de negócio corresponde a "P" e o que aparece quando falta o empenho são perguntas ao site.

### RN-10 — A tela conta as notas fiscais do processo e soma os seus valores

Ao carregar um processo, o sistema percorre todas as notas fiscais dele: conta quantas são e soma
o **valor total das notas**, o **valor total do imposto retido** e o **valor total a pagar**. A
quantidade aparece no campo próprio e os valores, nos campos de total. Não havendo valor, os
campos aparecem em branco em vez de zero.

Os totais são do processo inteiro, não da página: a relação mostra nove notas por vez, mas a
contagem e a soma alcançam todas as notas do processo.

### RN-11 — Fornecedor, fonte, tipo do processo e órgão aparecem por extenso

A tela não mostra só códigos. Ela lê o cadastro de **fornecedores** para trazer a **razão social**,
o cadastro de **fontes** para a **descrição da fonte**, o cadastro de **processos** para o **tipo
do processo** e o cadastro dos **tipos de processo** para a **descrição desse tipo**. O cadastro de
fornecedores é único para todo o sistema — a razão social é achada só pelo código do fornecedor —,
enquanto a fonte e o tipo do processo são por secretaria.

O cadastro de fornecedores tem **19 campos** e capacidade para **10.000** fornecedores; o de
fontes, **5 campos** e **1.000** fontes; o de processos, **3 campos** e **40.000** processos; o dos
tipos de processo, **3 campos** e **1.000** tipos.

### RN-12 — O código de impressão pede o relatório do processo por correio eletrônico

Preenchido o **código de impressão** e confirmada a consulta, a tela pede o **relatório do
processo** — o relatório **N11005** —, endereçado ao **correio eletrônico cadastrado para a
matrícula do servidor**, e leva junto o processo, a matrícula, o fornecedor e os parâmetros da
requisição. A requisição é criada com o número seguinte ao último já emitido.

O pedido tem três guardas, cada uma com a sua recusa e todas com o cursor de volta ao campo do
código de impressão:

- sem o processo SEI ou o processo RIO associado ao processo: **\* SEI ainda nao associado ao
  processo \***;
- já havendo requisição do mesmo relatório pendente para aquela secretaria e aquela coordenadoria:
  **\* Relatorio em processamento. Aguarde. \***;
- sem correio eletrônico cadastrado para a matrícula: **\* Usuario sem e-mail cadastrado \***.

Não preenchido o código de impressão, a tela não pede relatório nenhum.

[?] O campo que dispara o pedido é rotulado na tela apenas pelo nome interno do campo de código de
impressão, e o acervo não traz o catálogo de códigos de impressão nem o que o servidor digita nele
— e o cadastro de requisições exige esse código. O que o servidor lê no campo é pergunta ao site.

### RN-13 — Marcado o indicador de consulta, o processo é entregue à tela das notas fiscais

Marcado o **indicador de consulta**, a tela **não** segue com uma operação própria: ela refaz a
contagem e a soma das notas do processo e **entrega o processo à tela de manutenção das notas
fiscais (N017T)**, junto com os totais apurados e com a sua própria identificação como origem.

A tela seguinte reconhece essa origem — a N016C está entre as origens que ela trata de modo
próprio — e segue **direto ao processo entregue**, sem desviar para o menu de processos. A operação
vai junto na área de trabalho, e é a **consulta**: esta tela não tem outra operação para repassar
(RN-02). É essa passagem que dá sentido à tela: ela é o índice, a tela seguinte é o conteúdo.

Ao chegar ao fim da página, esta tela também limpa o código de impressão e o indicador, para não
os repassar adiante.

[?] O indicador de consulta é rotulado na tela apenas pelo nome interno do campo, e o acervo não
diz o que o servidor lê nele. Nas telas irmãs do acervo o mesmo campo é usado para **pedir a
consulta** e levar à tela de leitura par; aqui ele leva à tela de manutenção. Se o rótulo diz
"consultar" ou "abrir as notas", o acervo não diz. Pergunta ao site.

### RN-14 — Os campos informados são conferidos como números

Os **dezoito** campos informados na tela — as quatro partes do número do processo, a coordenadoria
regional escolar, o tipo de contrato, as quatro partes do processo SEI, as duas partes digitáveis
do processo RIO, o código do fornecedor, o código da fonte, o tipo do processo, o número de ordem,
o número da nota fiscal e o código do órgão — são conferidos como números, cada um com o seu
número de dígitos. Campo em branco é tratado como zero e os separadores de milhar são removidos
antes da conferência. Achado conteúdo que não seja número, a linha é recusada.

[?] O corpo da rotina que faz a conferência numérica não está no acervo — ela é importada do
ambiente de execução —, e o programa só devolve o
cursor para **onze** dos dezoito campos conferidos (as quatro partes do número do processo, as
quatro do processo SEI, as duas digitáveis do processo RIO e o número de ordem); nos outros sete a
linha é recusada sem que o cursor indique onde. O que o servidor vê nesse caso é pergunta ao site.

### RN-15 — Cada consulta começa com os campos de resultado limpos

Antes de conferir a digitação, os **doze** campos de resultado — nome da secretaria, data do
sistema, razão social do fornecedor, descrição da fonte, valor total do processo, descrição do tipo
do processo, valor total do imposto retido do processo, quantidade de notas, valor total a pagar,
nome do órgão, valor total da nota e valor total do imposto retido da nota — são apagados. Uma
consulta recusada, portanto, não deixa na tela o resultado da consulta anterior.

### RN-16 — A consulta só é montada com o acesso, a rota e a permissão confirmados

Antes de ler qualquer cadastro, a tela confere o **acesso** do servidor à tela e, na passagem de
confirmação, a **rota** e a **permissão por operação**, levando a matrícula, o código de acesso, o
privilégio, a secretaria e a coordenadoria da sessão. Qualquer uma dessas conferências que não
devolva "OK" limpa o estado e encerra: nada é lido e nada é mostrado.

A tela também lê o seu próprio título no cadastro de telas, pela identificação da tela; não
achando, marca o estado com o sinal de falha.

### RN-17 — Prefixo de tela preenchido desvia a transação

A tela leva o seu campo de próxima tela para a rota; preenchido, a transação é encaminhada e a
tela encerra antes de montar o número do processo.

[?] Nenhum programa desta jornada atribui valor a esse campo, e o acervo não mostra quem o
preenche. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consultar um processo, os seus totais e a relação das suas notas fiscais

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, o acesso e a coordenadoria
    E tenho acesso à tela N016C

  Cenário: RN-01 — consultar um processo e a relação das suas notas fiscais
    Dado que estou na tela N016C
    Quando consulto um processo que tem notas fiscais
    Então vejo a situação, a quantidade de notas e os valores do processo
    E vejo o fornecedor, a fonte do recurso, o tipo do processo e o órgão por extenso
    E vejo o nome da secretaria e a data do sistema no cabeçalho
    E vejo até nove notas fiscais, cada uma com o número de ordem, o número, o órgão e a data

  Cenário: RN-01 — a tela não inclui, não altera e não exclui nota fiscal
    Dado que estou na tela N016C
    Quando consulto um processo
    Então nenhuma nota fiscal é incluída, alterada ou excluída por esta tela
    E nenhum registro de auditoria é criado

  Cenário: RN-02 — operação diferente da consulta
    Dado que estou na tela N016C
    Quando a opção de manutenção da página não é a consulta
    Então vejo "* Opcao nao disponivel. Use CON *"
    E o cursor fica no campo da opção
    E nada é consultado

  Cenário: RN-03 — o número do processo em quatro partes
    Dado que estou na tela N016C
    Quando a tela é montada
    Então o COD. SECRETARIA está preenchido com a secretaria da minha sessão
    E o COD LOTE e as outras duas partes compõem o número de 14 dígitos que será consultado

  Cenário: RN-04 — achar o processo pelo processo SEI
    Dado que estou na tela N016C
    E que informo o número do processo SEI em vez do número do processo
    Quando confirmo a consulta
    Então o sistema adota o número do processo que o registro do SEI trouxer
    E vejo esse processo com os seus totais e as suas notas

  Cenário: RN-04 — achar o processo pelo processo RIO
    Dado que estou na tela N016C
    E que informo o número do processo RIO em vez do número do processo
    Quando confirmo a consulta
    Então o sistema adota o número do processo que o registro do RIO trouxer
    E vejo esse processo com os seus totais e as suas notas

  Cenário: RN-05 — processo de outra coordenadoria
    Dado que tenho coordenadoria regional escolar na sessão
    Quando consulto um processo de outra coordenadoria
    Então vejo "* Usuario sem acesso ao grupo deste processo *"
    E o cursor volta ao COD LOTE
    E nada é mostrado

  Cenário: RN-06 — número de processo não cadastrado
    Dado que estou na tela N016C
    Quando informo um número de processo que não existe
    Então vejo "* Processo nao cadastrado *"
    E o cursor volta ao COD LOTE
    E nada é mostrado

  Cenário: RN-06 — processo SEI não cadastrado
    Dado que estou na tela N016C
    Quando informo um processo SEI que não existe
    Então vejo "* SEI nao cadastrado *"
    E o cursor volta ao campo do SEI
    E nada é consultado

  Cenário: RN-06 — processo RIO não cadastrado
    Dado que estou na tela N016C
    Quando informo um processo RIO que não existe
    Então vejo "* PROCESSO RIO nao cadastrado *"
    E o cursor volta ao campo do RIO
    E nada é consultado

  Cenário: RN-07 — processo sem notas fiscais
    Dado que estou na tela N016C
    Quando consulto um processo cadastrado que não tem nota fiscal
    Então vejo "* Processo sem notas cadastradas *"
    E nenhuma nota é relacionada
    E nenhum total é mostrado

  Cenário: RN-08 — a tela numera a nota que ainda não tem número de ordem
    Dado que estou na tela N016C
    E que o processo consultado tem uma nota sem número de ordem dentro do processo
    Quando confirmo a consulta
    Então o sistema grava nessa nota o próximo número de ordem
    E a nota passa a aparecer numerada

  Cenário: RN-09 — a situação do processo vem do empenho
    Dado que estou na tela N016C
    Quando consulto um processo cuja nota está marcada com a situação que libera a busca
    Então vejo a situação do empenho: pré-liquidado, liquidado ou pago
    E quando a nota não está marcada assim, vejo o processo como fechado

  Cenário: RN-10 — a tela conta as notas do processo e soma os seus valores
    Dado que estou na tela N016C
    Quando consulto um processo com várias notas fiscais
    Então vejo quantas notas ele tem
    E vejo o valor total das notas, o do imposto retido e o total a pagar
    E quando não há valor, os campos aparecem em branco

  Cenário: RN-11 — fornecedor, fonte, processo e tipo do processo por extenso
    Dado que estou na tela N016C
    Quando consulto um processo cujo fornecedor, fonte e tipo estão cadastrados
    Então vejo a razão social do fornecedor e a descrição da fonte
    E vejo a descrição do tipo do processo
    E vejo o nome do órgão de cada nota

  Cenário: RN-12 — preencher o código de impressão pede o relatório do processo
    Dado que estou na tela N016C
    E que informo um código de impressão
    E que o processo tem o processo SEI associado
    E que não há relatório pendente para a minha secretaria e a minha coordenadoria
    E que a minha matrícula tem correio eletrônico cadastrado
    Quando confirmo a consulta
    Então a requisição do relatório do processo é criada
    E ela é endereçada ao meu correio eletrônico

  Cenário: RN-12 — processo sem o processo SEI associado
    Dado que estou na tela N016C
    E que informo um código de impressão
    Quando o processo consultado não tem o processo SEI nem o processo RIO associado
    Então vejo "* SEI ainda nao associado ao processo *"
    E o cursor volta ao campo do código de impressão
    E nenhuma requisição é criada

  Cenário: RN-12 — relatório já pendente
    Dado que estou na tela N016C
    E que informo um código de impressão
    E que já existe requisição pendente do mesmo relatório para a minha secretaria e a minha coordenadoria
    Quando confirmo a consulta
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo do código de impressão
    E nenhuma requisição é criada

  Cenário: RN-12 — matrícula sem correio eletrônico
    Dado que estou na tela N016C
    E que informo um código de impressão
    E que a minha matrícula não tem correio eletrônico cadastrado
    Quando confirmo a consulta
    Então vejo "* Usuario sem e-mail cadastrado *"
    E o cursor volta ao campo do código de impressão
    E nenhuma requisição é criada

  Cenário: RN-13 — marcado o indicador, a tela das notas abre sobre o processo
    Dado que estou na tela N016C
    E que consultei um processo
    Quando marco o indicador de consulta e confirmo
    Então a tela de manutenção das notas fiscais abre sobre o processo consultado
    E ela abre em consulta
    E ela reconhece que veio desta tela e não desvia para o menu de processos

  Cenário: RN-14 — campo com texto
    Dado que estou na tela N016C
    Quando informo, em qualquer dos dezoito campos conferidos, algo que não é número
    Então a linha é recusada
    E nada é consultado com essa digitação

  Cenário: RN-15 — cada consulta começa com os campos de resultado limpos
    Dado que estou na tela N016C
    E que a consulta anterior mostrou um processo
    Quando faço uma consulta que é recusada
    Então o resultado da consulta anterior não fica na tela

  Cenário: RN-16 — a consulta só é montada com o acesso, a rota e a permissão confirmados
    Dado que estou na tela N016C
    Quando a conferência de acesso, de rota ou de permissão não devolve "OK"
    Então a tela encerra sem ler nada
    E nada é mostrado

  Cenário: RN-17 — prefixo de tela preenchido
    Dado que a transação chega à N016C com o campo de próxima tela preenchido
    Quando a tela seria montada
    Então a transação é encaminhada
    E nada é consultado
```
