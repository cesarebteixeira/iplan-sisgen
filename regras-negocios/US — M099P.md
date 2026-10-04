# US — M099P — Solicitar o processamento dos relatórios da merenda escolar

## Estória

Como **servidor da coordenação regional escolar que responde pela merenda**, quero
**completar os dados do relatório que já escolhi e pedir que ele seja processado**,
para que **o relatório saia na impressora ou no e-mail certos, com o recorte de
grupo, de órgão e de período que eu preciso, sem ter de repetir o que já informei
no passo anterior**.

O relatório da merenda não existe enquanto ninguém o pede: é nesta tela que o
pedido é montado. Ela recebe do passo anterior qual relatório foi escolhido e em
que impressora ele deve sair, cobra apenas os dados daquele relatório e registra a
solicitação, que o processamento busca depois. Sem esse registro o relatório não é
produzido — e é a solicitação registrada que aparece para quem acompanha o que
está na fila. Um pedido repetido do mesmo relatório, para o mesmo recorte, é
recusado enquanto o anterior não sai da fila: é assim que se evita imprimir duas
vezes a mesma coisa.

## Contexto

Jornada S000M → M000M → M010M → M099P.

Ator: servidor de CRE — nesta tela, completa os dados do relatório já escolhido e
confirma o pedido de processamento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O `M000M` é um menu e não grava nada. O `M010M` também é menu, mas é ele que decide
o que esta tela vai fazer: recolhe a impressora, guarda-a no cadastro do próprio
servidor e **encadeia** nesta tela, passando o relatório escolhido — sem passar por
outro menu. Por isso o relatório e a impressora são regra desta estória, e não
contexto. O que a jornada deixa pronto além disso é o vínculo do servidor com a
secretaria: dele saem o tipo de órgão, a coordenação regional escolar (o grupo) e,
quando houver, o órgão a que o servidor está preso — os limites de alcance que
valem aqui.

Esta tela não é exclusiva desta jornada: ela é a tela de parâmetros dos relatórios
da merenda e é chamada por cinco menus de relatórios do módulo. Dos **quarenta e
um** relatórios que ela sabe montar, esta jornada alcança **catorze**.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O relatório e a impressora chegam escolhidos do passo anterior

Esta tela não pergunta qual relatório processar nem em que impressora: as duas
decisões vêm do menu de relatórios. Aquele menu não deixa seguir sem impressora
informada, avisando **\* Informe a impressora \***; a impressora informada ali fica
guardada no cadastro do servidor, para ser lembrada nas próximas vezes, e é ela que
segue com a solicitação feita aqui, ao lado da estação de onde o pedido saiu.

[?] Dos quarenta e um relatórios que esta tela atende, vinte e sete não são
alcançáveis por esta jornada: vinte e seis chegam por outros menus de relatórios do
módulo, fora desta jornada, e um — o do envio de atualização por e-mail — não tem, no
acervo lido, nenhum menu que o escolha: ou é acionado por fora do acervo, ou é resto
de uma versão anterior. Pergunta ao site.

### RN-02 — A tela se molda ao relatório escolhido

A mesma tela serve a vários relatórios. Ao abrir, ela assinala os campos que o
relatório escolhido exige, deixa o cursor no primeiro deles e escreve, ao lado dos
campos que aceitam um código de "todos", o código que significa todos — **99** para
o grupo e **99999** para o cardápio. Nos **catorze** relatórios desta jornada os
dados pedidos se agrupam em oito conjuntos:

| o que o relatório pede | quantos |
| --- | --- |
| referência (mês e ano), grupo, indicação de creche e, num deles, a refeição | 4 |
| referência, grupo e intervalo de órgãos (inicial e final) | 3 |
| referência, grupo, intervalo de órgãos e indicação de creche | 1 |
| referência, grupo, intervalo de órgãos, indicação de creche, marca de imprimir e projeto | 1 |
| referência e indicação de creche | 2 |
| referência e grupo | 1 |
| período (data inicial e data limite), grupo, indicação de creche e marca de imprimir | 1 |
| referência inicial e final, grupo, indicação de creche, códigos de refeição, cardápio e marca de imprimir | 1 |

Dos catorze, dois não pedem grupo e nenhum deles pede órgão: são os de referência
com indicação de creche, que abrangem toda a secretaria.

[?] Quatro posições da tela nunca são exigidas por relatório nenhum — o código de
segmento, o código de fornecedor, o dia útil e o grupo de atendimento. As quatro
são exibidas, apagadas e conferidas como número, e não entram em pedido nenhum; se
servem a outro uso, que não passa por aqui, o acervo lido não diz. E o nome de
negócio de cada relatório também não está no acervo: o que existe é o código com
que o menu o escolhe, sem título. Por isso esta estória fala dos relatórios pelos
dados que eles pedem. Pergunta ao site.

### RN-03 — O grupo é o limite de alcance do servidor

O grupo que o servidor tem no vínculo com a secretaria limita o que ele pode pedir.
Se ele tem grupo, só o dele passa; informar outro é recusa com
**\* Usuario sem acesso a outro grupo \***. Se ele não tem grupo, essa conferência
não recusa nada. Onde o relatório exige o grupo, deixá-lo em branco recusa com
**\* Informe o grupo \*** — e, nos **dois** relatórios em que a tela anuncia que o
grupo admite todas as coordenações, com
**\* Informe o grupo ou 99 para todos \***.

### RN-04 — O grupo informado tem de estar cadastrado

Nos **cinco** relatórios desta jornada em que a tela confere o grupo no cadastro, o
grupo informado é procurado no cadastro de grupos do órgão, pelo tipo de órgão de
quem opera e pelo código do grupo. Não achando, a recusa é
**\* Grupo nao cadastrado \*** e nada é gravado.

### RN-05 — Quem está preso a um órgão só alcança esse órgão

Quando o vínculo do servidor fixa um órgão, **três** dos relatórios desta jornada
aceitam apenas esse órgão: qualquer outro é recusado com
**\* Usuario sem acesso a outro orgao \***, e, sendo o órgão dele, o intervalo se
fecha nesse único órgão.

[?] A trava pelo órgão do servidor existe em três dos **cinco** relatórios desta
jornada que trabalham por órgão; nos outros dois, qualquer órgão da secretaria
passa desde que o grupo confira. Se a diferença é intencional, o acervo não diz.
Pergunta ao site.

### RN-06 — Pedido repetido do mesmo relatório é recusado

Antes de registrar, a tela procura solicitação já gravada do mesmo relatório e,
conforme o relatório, do mesmo grupo ou do mesmo órgão — sempre para o tipo de
órgão de quem opera. Achando, recusa com
**\* Relatorio em processamento. Aguarde. \*** e nada é gravado. Nos relatórios que
não informam grupo no pedido, a procura é feita com o grupo zerado, de modo que uma
única solicitação daquele relatório já barra as demais, seja qual for o grupo.

[?] A procura não olha a situação da solicitação: o cadastro distingue o que está
solicitado, em processamento e terminado, e a recusa fala só de "em processamento".
Ou quem processa apaga a solicitação ao terminar — e a recusa vale apenas enquanto
há pedido pendente —, ou a segunda emissão do mesmo relatório para o mesmo recorte
nunca passa. O acervo desta jornada não permite escolher entre os dois. Pergunta ao
site.

### RN-07 — A referência é obrigatória e tem de ser uma data real

Nos relatórios de referência, o mês e o ano são obrigatórios: em branco, a recusa é
**\* Informe mes/ano de referencia \***. Os dois têm de formar uma data que exista,
com o ano entre **1994 e 2099**; fora disso a recusa é
**\* Mes/Ano de referencia invalido \***. Ao recusar, o cursor volta ao campo da
referência.

[?] A conferência de calendário é feita por rotina do ambiente, fora dos fontes
lidos; o que exatamente ela aceita — por exemplo, se o dia 29 de fevereiro de um
ano não bissexto passa — não está no acervo. Pergunta ao site.

### RN-08 — Quando o relatório pede duas referências, as duas têm de fechar

**Um** dos relatórios desta jornada pede a referência inicial e a final. A tela
exige as duas — **\* Informe mes/ano inicial de referencia \*** e
**\* Informe mes/ano final de referencia \*** —, confere cada uma como data real
(**\* Mes/Ano de referencia inicial invalido \*** e
**\* Mes/Ano de referencia final invalido \***), recusa quando as duas não são do
mesmo ano (**\* Registros devem ser do mesmo ano \***) e recusa quando a final é
anterior à inicial (**\* Periodo de referencia invalido \***).

### RN-09 — A indicação de creche é obrigatória e só aceita sim ou não

**Dez** dos catorze relatórios desta jornada separam creche de não creche e exigem
que o servidor diga qual dos dois quer. Qualquer valor diferente de sim ou de não é
recusado com **\* Inf. se relatorio de Creche com S ou N \***, com o cursor de
volta ao campo.

### RN-10 — O intervalo de órgãos tem de existir e ser coerente com o cadastro

Nos relatórios que trabalham por órgão, o órgão inicial e o final são conferidos no
cadastro de órgãos: cada um tem de existir (**\* Orgao inicial nao cadastrado \*** e
**\* Orgao final nao cadastrado \***), ser da secretaria de quem opera
(**\* Orgao nao pertence a esta secretaria \***) e — quando o servidor tem grupo —
ser de um órgão do grupo dele (**\* <- Usuario sem acesso ao grupo deste orgao \***).
O órgão inicial não pode ser maior que o final
(**\* Orgao inicial > que orgao final \***), e em **três** desses relatórios o órgão
final é obrigatório, com **99999999** significando até o último órgão
(**\* Informe orgao final ou 99999999 \***). Num dos relatórios por órgão, responder
não à pergunta "imprime detalhe" troca o recorte: o pedido passa a valer para todos
os órgãos, sem conferir nenhum.

### RN-11 — O órgão tem de combinar com a indicação de creche

Onde o relatório pede a indicação de creche, o órgão informado tem de combinar com
ela: órgão que não é creche não entra em relatório de creche
(**\* Orgao nao cadastrado como creche \***) e órgão que é creche não entra em
relatório que não é de creche (**\* Orgao cadastrado como creche \***). A conferência
vale para o órgão inicial e para o final.

[?] A recusa por creche só dispara quando a marca de creche do cadastro do órgão é
exatamente "não" (para quem pediu creche) ou exatamente "sim" (para quem pediu não
creche). Com a marca em branco — que o cadastro admite, porque o campo não é
obrigatório — nenhuma das duas recusas acontece e o órgão passa dos dois lados. Ou
todo órgão tem essa marca preenchida, e o caso não ocorre, ou a conferência está
incompleta. Pergunta ao site.

### RN-12 — No relatório por projeto, o órgão tem de estar no projeto

**Um** dos relatórios desta jornada recorta também por projeto, e o projeto só é
conferido quando informado com um código diferente do que significa todos. Num
intervalo de um único órgão, o par órgão e projeto tem de existir no cadastro do
projeto, senão a recusa é **\* Orgao nao cadastrado neste projeto \***. Num
intervalo que percorre vários órgãos, a tela procura o projeto no cadastro e, não
achando nenhum órgão nele, recusa com **\* Projeto sem Orgaos cadastrados \***.

### RN-13 — Os relatórios de mapa exigem o mapa ou os registros do período

Os relatórios que trabalham sobre o mapa do período procuram o mapa do órgão, do
grupo e da referência pedidos — **cinco** dos catorze fazem essa conferência. Num
intervalo de um único órgão a recusa é **\* Mapa nao cadastrado para este orgao \***;
nos que percorrem o mapa aberto e, não o achando, o mapa fechado, a recusa é
**\* Noa existem registros para esta data \*** — a mensagem sai assim mesmo, com o
erro de grafia. Nos relatórios que percorrem os registros do grupo no período, a
mesma ideia aparece como **\* Nao existem registros para este grupo \***.

### RN-14 — Os relatórios de período exigem um período válido, de até um ano

**Um** dos relatórios desta jornada recebe um período. A data inicial e a data
limite são obrigatórias (**\* Informe data inicial do periodo \*** e
**\* Informe data final do periodo \***), cada uma tem de ser uma data real
(**\* Data inicial do periodo invalida \*** e
**\* Data final do periodo invalida \***), a inicial não pode ser posterior à
limite (**\* Data inicial maior que data finaL \***) e o período não pode passar de
um ano (**\* Periodo > 1 ano \***).

### RN-15 — Os relatórios de consumo exigem a refeição, o cardápio e a marca de imprimir

Nos **dois** relatórios de consumo, o código da refeição é obrigatório
(**\* Informe os codigos das refeicoes \***); num deles o cardápio também é, com
**99999** significando todos (**\* Informe o cardapio ou 99999 para todos \***), e a
marca de imprimir tem de ser respondida com sim ou não
(**\* Inf. se imprime relatorio com S ou N \***). No outro, o código da refeição
informado ainda é conferido no cadastro de refeições e, não existindo, a recusa é
**\* Refeicao nao cadastrada \***. A pergunta "imprime detalhe" aparece também num
relatório por órgão, onde a resposta diferente de sim ou não é recusada com
**\* Informe se imprime detalhe com S ou N \***.

[?] No relatório de período, a tela assinala a marca de imprimir como exigida, mas
nunca a cobra nem a leva no pedido: responder sim, não ou deixar em branco dá no
mesmo. Ou a conferência se perdeu, ou a pergunta ficou sem uso. Pergunta ao site.

### RN-16 — Há relatórios que só atendem registros a partir de 08/2008

**Nove** dos catorze relatórios desta jornada só atendem registros posteriores a
07/2008. Informada uma referência anterior a agosto de 2008, a recusa é
**\* Relatorio para registros posteriores a 07/2008 \***; no relatório de período, a
mesma marca vale para a data inicial. Os outros cinco não têm esse corte.

### RN-17 — Três relatórios só passam com e-mail cadastrado

**Três** dos catorze relatórios desta jornada são entregues por e-mail e exigem
e-mail no cadastro do servidor: sem ele, a recusa é
**\* Usuario sem e-mail cadastrado \*** e nada é gravado. São exatamente os três
entregues por e-mail; os outros onze são entregues para impressão.

### RN-18 — O que a tela grava é a solicitação, e o relatório vai para o processamento

Passando as conferências, a tela registra a solicitação no cadastro de solicitações
de relatório (`S040T`): o relatório, o tipo de órgão, o grupo e o órgão quando o
relatório os tem, a impressora quando o relatório imprime, a matrícula e a estação
de quem pediu, a data do pedido e os dados informados. O número da solicitação é
atribuído pelo sistema — o seguinte ao da última já registrada. A situação da
solicitação fica em branco, a cargo de quem processa.

Em seguida a tela monta o pedido de execução do relatório e o entrega ao serviço de
processamento do ambiente, no mesmo passo da gravação. Esta tela não encadeia em
nenhuma outra: o que sai dela é a solicitação e o pedido de execução.

[?] O número sai de uma leitura do último registro do cadastro feita sem travar, com
uma marca de leitura cujo significado não está no acervo lido; dois pedidos
simultâneos podem receber o mesmo número, e o acervo não diz o que acontece nesse
caso. E o cadastro tem hora de início da solicitação, mas esta tela não a preenche:
a hora fica zerada. Se quem processa a preenche, o acervo lido não mostra. Pergunta
ao site.

[?] A tela não mostra mensagem de confirmação depois de registrar a solicitação, e o
que o serviço de processamento faz com o pedido — se imprime, se guarda, se devolve
erro — não está no acervo lido. Pergunta ao site.

### RN-19 — Abrir a tela não grava nada

A primeira passagem da tela serve apenas para apresentá-la: ela liga os campos do
relatório escolhido, monta os campos de exibição e termina, sem passar por
conferência nem por gravação. Só a confirmação do servidor percorre o caminho que
grava. Fora a solicitação, nada mais é gravado: embora o programa declare rotinas de
gravação, de exclusão e de bloqueio para cada um dos **dezoito** cadastros que
enxerga, no caminho desta tela apenas a gravação da solicitação é executada — os
cadastros consultados (grupo, órgão, projeto, refeição, mapa, usuário) são só lidos,
e nenhuma solicitação é alterada ou apagada.

### RN-20 — A tela confere o que é numérico e devolve o cursor ao campo recusado

Todos os campos de código, número e data da tela passam pela conferência numérica
antes de qualquer consulta: campo em branco conta como zero, e o que não for número
não chega ao cadastro. Recusado um campo, o cursor volta para a posição daquele
campo na tela.

[?] A mensagem que o servidor lê nessa recusa vem de rotina comum do ambiente, que
não está no acervo lido. O que ele lê exatamente é pergunta ao site.

### RN-21 — Falha de banco interrompe a solicitação

Toda consulta e toda gravação testam o retorno do banco. Havendo erro, a transação
é interrompida com o aviso do sistema e o resto do caminho não é percorrido: a
solicitação não é considerada registrada.

---

## Cenários BDD

```gherkin
Funcionalidade: Solicitar o processamento dos relatórios da merenda escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M099P
    E vim do menu de relatórios com um relatório e uma impressora escolhidos

  Cenário: RN-02 e RN-19 — abrir a tela não grava nada
    Dado que vim do menu de relatórios com um relatório escolhido
    Quando a tela M099P é apresentada
    Então vejo assinalados apenas os campos que aquele relatório exige
    E o cursor fica no primeiro campo a preencher
    E nada é gravado

  Cenário: RN-01 — o relatório e a impressora vêm do menu de relatórios
    Dado que escolhi o relatório e a impressora no menu de relatórios
    Quando confirmo a solicitação
    Então a solicitação é registrada com essa impressora e com a estação de onde pedi
    E o relatório é entregue ao processamento

  Cenário: RN-01 — sem impressora o pedido não chega a esta tela
    Dado que não informei a impressora no menu de relatórios
    Quando tento confirmar naquele menu
    Então vejo "* Informe a impressora *"
    E não chego à tela M099P

  Cenário: RN-02 — o grupo que admite todos vem com a dica na tela
    Dado que o relatório escolhido admite o código de todas as coordenações
    Quando a tela abre
    Então vejo ao lado do campo do grupo o código que significa todos
    E, no relatório do cardápio, vejo também o código que significa todos os cardápios

  Cenário: RN-02 — o relatório de referência, grupo e creche
    Dado que o relatório escolhido pede referência, grupo e indicação de creche
    Quando informo um grupo existente, uma referência válida e a indicação de creche
    Então a solicitação é registrada com esses dados
    E o relatório é entregue ao processamento

  Cenário: RN-02 — o relatório de referência, grupo e intervalo de órgãos
    Dado que o relatório escolhido pede referência, grupo e órgãos inicial e final
    Quando informo grupo, referência e um intervalo de órgãos válido
    Então a solicitação é registrada com esses dados

  Cenário: RN-02 — o relatório de período
    Dado que o relatório escolhido pede período, grupo e indicação de creche
    Quando informo um período válido de até um ano, grupo e indicação de creche
    Então a solicitação é registrada com esses dados
    E o relatório é entregue por e-mail

  Cenário: RN-02 e RN-08 — o relatório de referências, refeições e cardápio
    Dado que o relatório escolhido pede referência inicial e final, refeições e cardápio
    Quando informo as duas referências do mesmo ano, a refeição, o cardápio e a marca de imprimir
    Então a solicitação é registrada com esses dados
    E o relatório é entregue por e-mail

  Cenário: RN-03 — grupo em branco
    Dado que o meu vínculo não me dá grupo
    Quando confirmo sem informar o grupo
    Então vejo "* Informe o grupo *"
    E nada é gravado

  Cenário: RN-03 — grupo fora do meu alcance
    Dado que o meu vínculo me dá um grupo
    Quando informo outro grupo
    Então vejo "* Usuario sem acesso a outro grupo *"
    E nada é gravado

  Cenário: RN-03 — grupo em branco no relatório que aceita todos
    Dado que o relatório escolhido aceita o código de todas as coordenações
    Quando deixo o grupo em branco
    Então vejo "* Informe o grupo ou 99 para todos *"
    E nada é gravado

  Cenário: RN-04 — grupo não cadastrado
    Dado que informo um grupo que não existe no cadastro de grupos
    Quando confirmo
    Então vejo "* Grupo nao cadastrado *"
    E nada é gravado

  Cenário: RN-05 — órgão fora do meu alcance
    Dado que o meu vínculo me prende a um órgão
    E o relatório escolhido é um dos que respeitam essa prisão
    Quando informo outro órgão
    Então vejo "* Usuario sem acesso a outro orgao *"
    E nada é gravado

  Cenário: RN-05 — o órgão do meu vínculo fecha o intervalo
    Dado que o meu vínculo me prende a um órgão
    Quando informo esse mesmo órgão como inicial e deixo o final em branco
    Então o pedido vale só para esse órgão
    E a solicitação é registrada

  Cenário: RN-06 — pedido repetido para o mesmo grupo
    Dado que já existe solicitação do mesmo relatório para o mesmo grupo
    Quando confirmo outro pedido
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E nada é gravado

  Cenário: RN-06 — pedido repetido no relatório que não informa grupo
    Dado que já existe solicitação do mesmo relatório
    E o relatório escolhido não informa grupo no pedido
    Quando confirmo outro pedido, com qualquer grupo
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E nada é gravado

  Cenário: RN-07 — referência em branco
    Dado que o relatório escolhido é de referência
    Quando confirmo sem informar o mês e o ano
    Então vejo "* Informe mes/ano de referencia *"
    E o cursor volta ao campo da referência
    E nada é gravado

  Cenário: RN-07 — referência que não é data real
    Dado que informo um mês e um ano que não formam uma data válida
    Quando confirmo
    Então vejo "* Mes/Ano de referencia invalido *"
    E nada é gravado

  Cenário: RN-07 — ano fora da faixa aceita
    Quando informo o ano 1993 ou 2100 na referência
    Então vejo "* Mes/Ano de referencia invalido *"
    E nada é gravado

  Cenário: RN-08 — referência final em branco
    Dado que o relatório escolhido pede duas referências
    Quando confirmo sem informar a final
    Então vejo "* Informe mes/ano final de referencia *"
    E nada é gravado

  Cenário: RN-08 — referências que não fecham
    Dado que o relatório escolhido pede duas referências
    Quando as duas não são do mesmo ano
    Então vejo "* Registros devem ser do mesmo ano *"
    E quando a final é anterior à inicial vejo "* Periodo de referencia invalido *"
    E nada é gravado

  Cenário: RN-08 — referências que não são datas reais
    Dado que o relatório escolhido pede duas referências
    Quando a inicial não forma uma data real
    Então vejo "* Mes/Ano de referencia inicial invalido *"
    E quando é a final que não forma data real vejo "* Mes/Ano de referencia final invalido *"
    E nada é gravado

  Cenário: RN-09 — indicação de creche fora de sim e não
    Dado que o relatório escolhido separa creche de não creche
    Quando informo uma indicação diferente de sim e de não
    Então vejo "* Inf. se relatorio de Creche com S ou N *"
    E o cursor volta ao campo
    E nada é gravado

  Cenário: RN-10 — órgão inicial não cadastrado
    Dado que o relatório escolhido trabalha por órgão
    Quando informo um órgão inicial que não existe no cadastro
    Então vejo "* Orgao inicial nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — órgão de outra secretaria
    Quando informo um órgão que não é da minha secretaria
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E nada é gravado

  Cenário: RN-10 — órgão de outro grupo
    Dado que o órgão informado pertence a um grupo que não é o meu
    Quando confirmo
    Então vejo "* <- Usuario sem acesso ao grupo deste orgao *"
    E nada é gravado

  Cenário: RN-10 — órgão final não cadastrado
    Quando informo um órgão final que não existe no cadastro
    Então vejo "* Orgao final nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — órgão inicial maior que o final
    Quando informo o órgão inicial maior que o órgão final
    Então vejo "* Orgao inicial > que orgao final *"
    E nada é gravado

  Cenário: RN-10 — órgão final em branco no relatório que o exige
    Dado que o relatório escolhido exige o órgão final
    Quando confirmo sem informá-lo
    Então vejo "* Informe orgao final ou 99999999 *"
    E quando informo 99999999 o pedido alcança até o último órgão

  Cenário: RN-10 — imprimir sem detalhe passa a valer para todos os órgãos
    Dado que o relatório escolhido pergunta se imprime o detalhe
    Quando respondo que não
    Então o pedido passa a valer para todos os órgãos, sem conferir nenhum

  Cenário: RN-11 — órgão que não é creche num relatório de creche
    Dado que o órgão informado não é cadastrado como creche
    Quando peço o relatório com a indicação de creche
    Então vejo "* Orgao nao cadastrado como creche *"
    E nada é gravado

  Cenário: RN-11 — órgão que é creche num relatório que não é de creche
    Dado que o órgão informado é cadastrado como creche
    Quando peço o relatório sem a indicação de creche
    Então vejo "* Orgao cadastrado como creche *"
    E nada é gravado

  Cenário: RN-12 — órgão fora do projeto
    Dado que o relatório escolhido recorta por projeto e informei o projeto
    Quando o órgão informado não está nesse projeto
    Então vejo "* Orgao nao cadastrado neste projeto *"
    E nada é gravado

  Cenário: RN-12 — projeto sem órgãos
    Dado que o relatório escolhido recorta por projeto e informei o projeto
    E o intervalo percorre vários órgãos
    Quando o projeto não tem nenhum órgão cadastrado
    Então vejo "* Projeto sem Orgaos cadastrados *"
    E nada é gravado

  Cenário: RN-13 — mapa inexistente para a referência
    Dado que o relatório escolhido trabalha sobre o mapa do período
    E não existe mapa do órgão, do grupo e da referência pedidos
    Quando confirmo
    Então vejo "* Mapa nao cadastrado para este orgao *" ou "* Noa existem registros para esta data *"
    E nada é gravado

  Cenário: RN-13 — grupo sem registros no período
    Dado que o relatório escolhido percorre os registros do grupo no período
    E não existem registros do grupo na referência pedida
    Quando confirmo
    Então vejo "* Nao existem registros para este grupo *"
    E nada é gravado

  Cenário: RN-14 — período sem a data inicial
    Dado que o relatório escolhido recebe um período
    Quando confirmo sem informar a data inicial
    Então vejo "* Informe data inicial do periodo *"
    E nada é gravado

  Cenário: RN-14 — período com data que não existe
    Quando informo uma data inicial que não é data real
    Então vejo "* Data inicial do periodo invalida *"
    E quando informo uma data limite que não é data real vejo "* Data final do periodo invalida *"
    E nada é gravado

  Cenário: RN-14 — período com a data inicial posterior à limite
    Quando informo a data inicial depois da data limite
    Então vejo "* Data inicial maior que data finaL *"
    E nada é gravado

  Cenário: RN-14 — período maior que um ano
    Quando informo um período de mais de um ano
    Então vejo "* Periodo > 1 ano *"
    E nada é gravado

  Cenário: RN-15 — relatório de consumo sem a refeição
    Dado que o relatório escolhido é de consumo
    Quando confirmo sem informar o código da refeição
    Então vejo "* Informe os codigos das refeicoes *"
    E nada é gravado

  Cenário: RN-15 — relatório de consumo sem o cardápio
    Dado que o relatório escolhido pede o cardápio
    Quando informo a refeição e deixo o cardápio em branco
    Então vejo "* Informe o cardapio ou 99999 para todos *"
    E nada é gravado

  Cenário: RN-15 — refeição não cadastrada
    Dado que o relatório escolhido confere a refeição no cadastro de refeições
    Quando informo um código de refeição que não existe
    Então vejo "* Refeicao nao cadastrada *"
    E nada é gravado

  Cenário: RN-15 — marca de imprimir o relatório não respondida
    Dado que o relatório escolhido pergunta se imprime o relatório
    Quando confirmo sem responder
    Então vejo "* Inf. se imprime relatorio com S ou N *"
    E nada é gravado

  Cenário: RN-15 — marca de imprimir o detalhe não respondida
    Dado que o relatório escolhido pergunta se imprime o detalhe
    Quando respondo algo diferente de sim e de não
    Então vejo "* Informe se imprime detalhe com S ou N *"
    E nada é gravado

  Cenário: RN-16 — referência anterior ao corte de 08/2008
    Dado que o relatório escolhido só atende registros posteriores a 07/2008
    Quando informo uma referência anterior a agosto de 2008
    Então vejo "* Relatorio para registros posteriores a 07/2008 *"
    E nada é gravado

  Cenário: RN-16 — data inicial do período anterior ao corte
    Dado que o relatório de período só atende registros posteriores a 07/2008
    Quando informo uma data inicial anterior a agosto de 2008
    Então vejo "* Relatorio para registros posteriores a 07/2008 *"
    E nada é gravado

  Cenário: RN-17 — relatório por e-mail sem e-mail cadastrado
    Dado que o relatório escolhido é entregue por e-mail
    E o meu cadastro não tem e-mail
    Quando confirmo
    Então vejo "* Usuario sem e-mail cadastrado *"
    E nada é gravado

  Cenário: RN-18 — pedido aceito vira solicitação e vai para o processamento
    Dado que informei os dados válidos do relatório escolhido
    E não existe solicitação do mesmo relatório para o mesmo recorte
    Quando confirmo
    Então fica gravada uma solicitação com o número seguinte ao da última
    E ela guarda o relatório, o tipo de órgão, o grupo, o órgão e a impressora do pedido
    E a estação, a matrícula e a data do pedido
    E a situação da solicitação fica em branco
    E o relatório é entregue ao processamento
    E nenhum cadastro consultado é alterado

  Cenário: RN-19 — recusa não registra nada e não altera cadastro
    Dado que confirmo um pedido com um dado em falta ou com um cadastro que não existe
    Quando a tela recusa
    Então nenhuma solicitação é registrada
    E nenhum dos cadastros consultados é alterado
    E nenhuma solicitação já registrada é alterada ou apagada

  Cenário: RN-20 — valor não numérico num campo de código
    Dado que informo letras num campo de código, número ou data
    Quando confirmo
    Então a tela recusa o valor e devolve o cursor para esse campo
    E nada é gravado

  Cenário: RN-21 — falha de banco durante a solicitação
    Dado que a leitura ou a gravação falha no banco
    Quando confirmo
    Então a transação é interrompida com o aviso do sistema
    E a solicitação não é considerada registrada
```
