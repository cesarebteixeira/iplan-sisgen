# US — C341T — Prioridade dos contratos de um gênero na coordenação regional escolar

## Estória

Como **servidor da coordenação regional escolar**, quero **ver, para um gênero, as permissões
de contrato que a minha regional tem para ele e ajustar a prioridade de cada uma**, para que
**a ordem que a regional definiu fique registrada nessas permissões, e não só a que veio do
cadastro**.

A prioridade acompanha a permissão de contrato, e é ela que a regional ajusta quando a ordem
cadastrada não serve. Esta tela é o único lugar que reúne, de uma vez, as permissões de um
gênero na regional: sem ela, a prioridade só se veria abrindo as permissões uma a uma, e não
haveria como comparar a ordem entre os contratos do mesmo gênero. Ela não inclui nem exclui
permissão: monta a lista do gênero, deixa ajustar a prioridade linha a linha e grava o que
mudou.

## Contexto

Jornada S000M → C000M → C050M → C060M → C341T.

Ator: servidor da coordenação regional escolar — informa a coordenação regional, a subclasse e
o gênero, e ajusta a prioridade dos contratos que a regional tem para aquele gênero.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Os três passos anteriores (o `C000M`, o `C050M` e o `C060M`) são menus: só encaminham, não
gravam nada e não deixam na sessão nada além do que a entrada deixou. A tela trabalha com o que
a entrada registrou — o tipo de órgão, a matrícula, o código de acesso, o privilégio, a
coordenação regional e a estação — e não pergunta nada disso ao servidor.

As regras abaixo são só as desta tela; as da entrada não se repetem aqui.

## Regras de negócio

### RN-01 — A tela reúne as permissões de contrato de um gênero na coordenação regional

Para uma **coordenação regional escolar**, uma **subclasse** e um **gênero**, a tela mostra as
**permissões de contrato** que a regional tem para aquele gênero, uma por linha. A página tem
**4 linhas**, e cada linha carrega **9 campos**: o tipo de contrato, a vigência (a data limite),
a tabela quinzena, a prioridade do contrato, a prioridade, a ação da linha, o código do
fornecedor, o número com sinal e o sinal. A linha mostra ainda a descrição do contrato e a
razão social do fornecedor, que vêm dos cadastros.

A permissão de contrato é identificada, dentro do órgão, da subclasse e do gênero, pela
**vigência** e pelo **tipo de contrato**; essa identificação não distingue o grupo de licitação
nem a classe, de modo que mais de uma permissão cabe na mesma identificação.

A tela enxerga **sete** bases: as permissões de contrato (52 campos; capacidade de 1.000.000 de
registros), os contratos (12 campos; 1.000), os fornecedores (19 campos; 10.000), os gêneros (25
campos; 150.000), a lista de prioridades de cada servidor (9 campos; 100.000), a auditoria (15
campos; 60.000.000) e o cadastro das telas (7 campos; 2.000). Capacidade é o máximo esperado,
parâmetro de dimensionamento — não é o que está cadastrado.

[?] O que a prioridade de dois dígitos ordena no negócio — o atendimento de um pedido, a ordem
de compra, outra coisa — o acervo lido não diz: a tela só a mostra e a altera. Pergunta ao
site.

[?] O que é, em negócio, o número com sinal e duas casas decimais que a permissão carrega e que
a linha exibe, o acervo lido também não diz; nenhuma mensagem do sistema o nomeia. Pergunta ao
site.

### RN-02 — A tela abre em consulta e só aceita a alteração e a consulta

A opção de manutenção da tela aceita **alteração** e **consulta**; inclusão e exclusão não se
escolhem por ali — a tela não inclui nem exclui permissão. A tela **abre em consulta** e,
reapresentada dentro da mesma sessão, volta na opção usada da última vez. Qualquer outra opção é
recusada com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta ao campo da
opção.

[?] A recusa manda usar "ALT" e "CON", mas a conferência reconhece a alteração e a consulta por
códigos internos que o acervo escreve de outra forma, e nenhum texto "ALT" ou "CON" isolado
existe nos 506 programas do acervo lido. Ou o terminal traduz o que o servidor digita antes de
enviar, ou a mensagem indica valores que a tela recusa. Pergunta ao site.

[?] A recusa da opção **não** marca por si a transação como perdida, e o caminho que grava a
prioridade da linha aceita qualquer opção diferente da consulta. Quem interrompe a transação é
a rotina de mensagem do sistema, cujo corpo não está no acervo lido: se ela não interromper, a
mesma resposta que mostrou a recusa pode gravar a prioridade. Não se escolhe um dos dois.
Pergunta ao site.

### RN-03 — A tela só abre e só altera para quem tem autorização

A abertura passa pela conferência da sessão: a matrícula tem de estar cadastrada, a estação em
que se está tem de ser a do cadastro do servidor, e a tela tem de estar liberada para a
matrícula. Barrada aí, a tela avisa **\* Tela nao disponivel \*** (quando a tela não consta do
cadastro das telas) ou **\* Acesso negado para esta matricula \*** (quando a matrícula não a tem
no seu acesso); estando a estação fora do cadastro, a sessão é encerrada. Em qualquer desses
casos nada é processado.

Na passagem da resposta, além da rota, o sistema confere o **acesso do servidor a esta tela por
operação**: a **alteração** só passa quando o acesso tem a alteração liberada; sem ela, a
recusa é **\* Acesso negado para esta operacao \*** e a resposta não é processada. A
**consulta** não passa por essa conferência de operação — ela responde a qualquer acesso que
tenha a tela.

[?] A liberação da alteração é conferida uma vez, na passagem da resposta, e o caminho que grava
a prioridade da linha não a reconfere; como a recusa também não marca por si a transação como
perdida, não se conclui se a prioridade chega a ser gravada quando o acesso não libera a
alteração. O corpo da rotina de mensagem do sistema não está no acervo lido. Pergunta ao site;
não se escolhe um dos dois.

### RN-04 — A coordenação regional informada tem de ser a do próprio servidor

Na consulta, a coordenação informada é conferida: informando uma coordenação à qual o servidor
não pertence, a recusa é **\* Usuario sem acesso a este grupo \***, com o cursor devolvido ao
campo. Se a sessão não carrega coordenação nenhuma, a conferência é dispensada e qualquer
coordenação informada passa. Essa conferência é feita só na consulta; na alteração, o que se
exige é que a coordenação seja a mesma do gênero já consultado (RN-10).

[?] A conferência compara a coordenação informada com uma área de trabalho que esta tela não
preenche em nenhum caminho, enquanto a coordenação da sessão é lida de outra área; nos 506
programas do acervo lido, aquela área só recebe valor em telas de outro módulo. Quem a preenche
nesta jornada, e se ela carrega a coordenação da sessão, o acervo não mostra: se não carregar, a
recusa alcança qualquer coordenação informada por quem tem uma na sessão. Pergunta ao site.

[?] As mensagens da tela chamam de "grupo" o campo que a máscara rotula de coordenação regional
escolar. Se grupo e coordenação são a mesma coisa, ou se o grupo é uma subdivisão dela, o
acervo lido não diz. Pergunta ao site.

### RN-05 — O gênero tem de ser informado e estar cadastrado

Na consulta, a subclasse e o gênero são exigidos: vindo a subclasse zerada, a recusa é
**\* Informe o genero \***, com o cursor no campo. Informados, o gênero é procurado no cadastro
de gêneros pela subclasse e pelo gênero, com a vigência informada na posição de leitura, e o que
estiver marcado como excluído não conta. Não estando no cadastro, a recusa é
**\* Genero nao cadastrado \***, com o cursor de volta ao campo do gênero.

[?] A procura leva a data de hoje nas partes da vigência e usa o recurso de posicionamento do
dicionário de dados, cujo efeito não está no corpus nem no manual: se ele exigir a coincidência
exata, só o gênero que começa exatamente hoje seria encontrado, e todo o resto seria recusado
como não cadastrado; se ele apenas posicionar, a procura começa na primeira vigência a partir
de hoje. Os dois comportamentos são compatíveis com o que o fonte mostra e não se escolhe um
deles. Pergunta ao site.

### RN-06 — A coordenação precisa ter permissão de contrato para o gênero

Confirmado o gênero, o sistema procura uma permissão de contrato daquela coordenação para aquele
gênero, na vigência de hoje; não havendo nenhuma, a recusa é
**\* Gen. sem permissoes cad. para este grupo \***, com o cursor no campo do gênero. Nada é
gravado nessa recusa.

### RN-07 — A consulta remonta a lista de prioridades do servidor, e não é só leitura

Passando pelas conferências, a tela **apaga as linhas da lista de prioridades daquele servidor**
e a **remonta** a partir das permissões do gênero naquela coordenação: entra uma linha por
vigência e tipo de contrato, com a prioridade que a permissão tem hoje. Ficam de fora as
permissões cuja vigência já venceu e as dos contratos cuja permissão está marcada com o tipo
**C**. Cada linha incluída deixa um registro na auditoria — de modo que a consulta **não** é uma
operação de leitura: ela escreve na lista e na trilha de auditoria.

A lista é remontada só quando a coordenação, a subclasse e o gênero informados diferem dos do
gênero já em curso; reenviar a mesma consulta não a refaz.

[?] As varreduras que apagam as linhas antigas e a que inclui as novas usam o posicionamento do
dicionário de dados, cujo efeito não está no corpus nem no manual: o alcance exato de cada uma —
se a lista do gênero anterior some por inteiro ou se sobra linha de outro gênero — não se
conclui. Pergunta ao site.

[?] A lista é guardada **por servidor** (a matrícula da sessão faz parte da identificação dela),
e nenhum outro programa do acervo lido a lê ou a grava. Por que a ordem montada pela consulta é
de cada servidor, e não da coordenação, e o que ela guarda entre sessões, o acervo não diz.
Pergunta ao site.

[?] O que significa, em negócio, o tipo de permissão **C** — que a tela irmã dos tipos de
contrato exibe como *Coo* — e por que os contratos com esse tipo ficam de fora da lista, o
acervo lido não diz. Pergunta ao site.

### RN-08 — A página é montada a partir da lista guardada, e a tela avisa quando ela está vazia

A página é montada a partir da lista guardada para o gênero, e de cada linha o sistema vai
buscar o contrato, a permissão e o fornecedor correspondentes; o que já não existir nesses
cadastros deixa a linha sem esses dados. Se a lista do gênero estiver vazia, a tela mostra
**\* Genero sem prioridades cadastradas \*** e não preenche nenhuma linha.

[?] A página é montada na passagem de exibição e a lista é remontada na passagem da resposta; o
acervo não mostra se a lista nova já aparece na resposta da própria consulta ou só na abertura
seguinte da tela. Pergunta ao site.

[?] A lista é mostrada de 4 em 4 e a varredura continua a partir da prioridade da última linha
mostrada; chegando ao fim, o sistema repõe o cursor na prioridade 99 com a data de hoje. O que
acontece com a página seguinte — se ela recomeça do começo ou fica vazia — o acervo lido não
permite concluir. Pergunta ao site.

### RN-09 — Abrir a tela sem um gênero em curso apaga a lista do servidor

Ao ser aberta sem um gênero em curso — o caso do primeiro uso na sessão —, a tela **apaga as
linhas da lista de prioridades daquele servidor** e apresenta a página vazia. A lista só volta a
existir quando o servidor consulta um gênero; e, a partir daí, ela é de um gênero só.

[?] Não está no acervo por que abrir a tela apaga a lista de trabalho do servidor em vez de
apenas deixá-la de lado. Se isso é o pretendido ou resíduo do gerador, é pergunta ao site.

### RN-10 — Só se altera o gênero que já foi consultado

Com a opção de alteração, o sistema exige que a coordenação, a subclasse e o gênero informados
sejam os mesmos do último gênero consultado nesta sessão. Não sendo, a recusa é
**\* Consulte antes de atualizar \***, com o cursor de volta ao campo do gênero. Consultar é,
portanto, condição da alteração.

[?] Essa recusa também não marca por si a transação como perdida, e o caminho que grava a
prioridade da linha não volta a conferir se a consulta foi feita: se a rotina de mensagem do
sistema não interromper, a gravação pode acontecer na mesma resposta em que a recusa foi
mostrada. Pergunta ao site; não se escolhe um dos dois.

### RN-11 — A linha só é processada com a ação de alteração

Uma linha só é processada quando carrega a ação **A** (alterar). Qualquer outra ação — e também
a linha em branco — passa em silêncio: não gera recusa, não gera mensagem e não grava nada. A
tela não oferece ação de inclusão nem de exclusão de linha: as linhas nascem e se refazem pela
consulta (RN-07).

### RN-12 — A alteração grava a prioridade nova na permissão e na linha da lista

Com a linha carregando a ação de alteração, o sistema desmembra a vigência da linha nas suas
três partes e procura a permissão daquele contrato, naquela coordenação, naquele gênero e
naquela vigência. Achando, compara a prioridade informada com a registrada: sendo **igual**,
nada é gravado; sendo **diferente**, deixa o rastro na auditoria e grava a prioridade nova na
permissão e na linha da lista do servidor.

### RN-13 — A prioridade nova alcança mais de uma permissão do mesmo contrato

A identificação da permissão não distingue o grupo de licitação nem a classe: as permissões que
casam com o contrato, a subclasse, o gênero, a coordenação e a vigência recebem todas a
prioridade informada, cada uma com o seu próprio registro de auditoria; a linha correspondente
da lista do servidor também.

[?] A leitura que faz a procura da permissão usa o posicionamento do dicionário de dados, e
depois de ler o sistema reconfere a coordenação, a subclasse e o gênero — mas não a vigência nem
o tipo de contrato. Se o posicionamento procurar só por esses três, a prioridade nova alcança
**todas** as permissões do gênero na coordenação, e não apenas as da vigência e do tipo da
linha. Os dois comportamentos são compatíveis com o que o fonte mostra e não se escolhe um
deles. Pergunta ao site.

### RN-14 — A tela exibe o que os cadastros dizem, e não o que foi digitado

O tipo de contrato, a descrição do contrato, a tabela quinzena, a prioridade do contrato, o
código do fornecedor, a razão social e o número com sinal são preenchidos pelo sistema a partir
dos cadastros lidos — contrato, permissão e fornecedor — e são reescritos a cada exibição: o que
for digitado neles não altera a gravação. A **prioridade** e a **ação** da linha são os valores
que a tela aproveita do que foi informado.

Fora da lista, o cabeçalho mostra a **data do sistema**, a **descrição do tipo de órgão** da
sessão e a descrição resumida do gênero em curso.

[?] De onde vêm a data do sistema e a descrição do tipo de órgão não está no lote: as duas áreas
de onde a tela as copia não recebem valor de nenhum dos 506 programas do acervo lido — só
aparecem como destino, para serem apagadas —, e a entrada guarda a descrição do tipo de órgão em
outra área. Se o ambiente transporta os valores de uma área para a outra, e de onde vem a data
do sistema, o acervo não diz; se não transportar, os dois campos saem em branco. Pergunta ao
site.

### RN-15 — A digitação é conferida antes de qualquer leitura, e o resultado anterior é apagado

Os **oito campos** informados — a coordenação regional, a subclasse, o gênero, o tipo de
contrato, a prioridade do contrato, a prioridade, o código do fornecedor e o número com sinal —
passam pela edição numérica antes de qualquer leitura: o que está em branco vale zero, os zeros
à esquerda caem e o que não for número é recusado. Antes disso, a tela apaga os **cinco campos
de resultado** da consulta anterior — a descrição do tipo de órgão, a data do sistema, a
descrição resumida do gênero, a descrição do contrato e a razão social —, de modo que uma
consulta recusada não deixa na tela o resultado da anterior. O mapa de cursor, porém, tem
posição definida para apenas **quatro** dos oito campos: a coordenação regional, a subclasse, o
gênero e a prioridade.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não está nos
fontes desta jornada: a rotina que faz a edição numérica é importada, sem corpo no acervo lido,
e a tela só reposiciona o cursor. Pergunta ao site.

[?] Os quatro campos de retorno (o tipo de contrato, a prioridade do contrato, o código do
fornecedor e o número com sinal) podem ser recusados pela edição sem que a tela tenha onde
posicionar o cursor. Se isso é pretendido — por serem campos que o sistema reescreve — ou
resíduo do gerador, é pergunta ao site.

### RN-16 — Toda gravação deixa rastro na auditoria

Cada linha incluída na consulta e cada prioridade alterada monta um registro na trilha de
auditoria com o **tipo de órgão**, a **matrícula**, a **coordenação regional**, a **tela de
origem**, a **estação**, a **data e a hora** da sessão, a **operação** (inclusão ou alteração),
o **objeto acertado** (a lista ou a permissão) e os **valores antes e depois**.

[?] O número de processo que a auditoria guarda não é montado por esta tela: ela leva para lá o
tipo de contrato da linha em foco. Se é isso o pretendido, ou se o rastro fica sem o
identificador do processo, é pergunta ao site.

### RN-17 — A tela grava em três bases e só lê as outras quatro

Das **sete** bases que a tela enxerga, ela escreve em **três**: a lista de prioridades do
servidor (inclusão, alteração e exclusão de linhas), o cadastro das permissões de contrato
(alteração da prioridade) e a trilha de auditoria. As outras quatro — o cadastro das telas, os
contratos, os fornecedores e os gêneros — ela apenas lê. As operações de gravação, de exclusão e
de travamento existem declaradas para as sete bases, mas **declarar não é executar**: nenhum
caminho inclui ou exclui permissão de contrato, e a única exclusão que a tela faz é a de linhas
da própria lista.

### RN-18 — A tela não encadeia em outra e não muda de comportamento conforme quem a chamou

A tela não passa registro nem operação para nenhuma tela seguinte: não tem saída. O campo que
carregaria a tela de destino existe e, quando ele chega preenchido, a passagem da resposta não
confere nada — mas o caminho que grava a prioridade da linha não volta a conferir essa condição.

A tela **não** decide o modo pelo código da tela que a chamou: ela não compara a origem com
código de tela nenhum. Ela abre em consulta porque a opção da sessão está em branco no primeiro
uso, e reabre na opção da última vez (RN-02).

[?] Quando a tela de destino já vem definida, a tela deixa de conferir a resposta, mas o caminho
que grava a prioridade continua a existir sem reconferir essa condição; como a recusa não marca
por si a transação como perdida e o corpo da rotina de mensagem do sistema não está no acervo
lido, não se conclui se a prioridade é gravada nesse caso. Pergunta ao site; não se escolhe um
dos dois.

[?] A ficha da tela no grafo diz que ela "alcança 1 tela em 0 saídas", mas o programa não leva
nenhuma tela de destino: o campo que guardaria a tela seguinte aparece uma única vez, como
leitura, na conferência da rota. A contagem da ficha parece vir do que o gerador compartilha com
as outras telas. Pergunta a quem mantém o grafo.

## Cenários BDD

```gherkin
Funcionalidade: Prioridade dos contratos de um gênero na coordenação regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C341T

  Cenário: A tela abre em consulta
    Dado que abro a tela C341T pela primeira vez na sessão
    Quando a tela é apresentada
    Então a opção de manutenção vem como consulta

  Cenário: A tela reabre na opção usada da última vez
    Dado que já usei a alteração nesta sessão
    Quando a tela é reapresentada
    Então a opção de manutenção volta como alteração

  Cenário: Opção de manutenção fora da alteração e da consulta
    Dado que estou na tela C341T
    Quando informo uma opção diferente da alteração e da consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção

  Cenário: Matrícula sem esta tela no seu acesso
    Dado que a minha matrícula não tem a tela C341T liberada
    Quando abro a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E nada é processado

  Cenário: Tela fora do cadastro das telas
    Dado que a tela C341T não consta do cadastro das telas
    Quando abro a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E nada é processado

  Cenário: Estação diferente da do meu cadastro
    Dado que estou em uma estação diferente da do meu cadastro
    Quando abro a tela C341T
    Então a minha sessão é encerrada
    E nada é processado

  Cenário: Acesso sem a alteração liberada
    Dado que o meu acesso a esta tela não tem a alteração liberada
    Quando envio uma alteração de prioridade
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E a resposta não é processada

  Cenário: Consulta em coordenação regional à qual não tenho acesso
    Dado que informo uma coordenação regional diferente da minha
    Quando envio a consulta
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenação regional

  Cenário: Gênero não informado
    Dado que deixo a subclasse e o gênero em branco
    Quando envio a consulta
    Então vejo a mensagem "* Informe o genero *"
    E o cursor volta ao campo do gênero

  Cenário: Gênero não cadastrado
    Dado que informo uma subclasse e um gênero que não existem no cadastro de gêneros
    Quando envio a consulta
    Então vejo a mensagem "* Genero nao cadastrado *"
    E o cursor volta ao campo do gênero

  Cenário: Sem permissão de contrato para o gênero na coordenação
    Dado que a minha coordenação regional não tem permissão de contrato para o gênero informado
    Quando envio a consulta
    Então vejo a mensagem "* Gen. sem permissoes cad. para este grupo *"
    E o cursor volta ao campo do gênero
    E nada é gravado

  Cenário: A consulta monta a lista do gênero na coordenação
    Dado que a minha coordenação regional tem permissões de contrato para o gênero informado
    Quando envio a consulta
    Então a lista daquele gênero é montada a partir dessas permissões
    E cada linha traz a vigência, o tipo de contrato e a prioridade da permissão
    E a lista fica guardada para o servidor que consultou

  Cenário: A página mostra no máximo 4 linhas
    Dado que o gênero tem mais de 4 permissões na minha coordenação
    Quando envio a consulta
    Então a página mostra no máximo 4 linhas
    E as linhas restantes ficam em branco

  Cenário: A consulta descarta as permissões vencidas e as do tipo C
    Dado que o gênero tem permissões com vigência vencida e permissões de contrato do tipo C
    Quando envio a consulta
    Então essas permissões não entram na lista

  Cenário: A consulta não é só leitura: ela deixa rastro na auditoria
    Dado que envio uma consulta que monta a lista
    Quando a consulta termina
    Então cada linha incluída na lista deixa um registro na auditoria
    E o registro traz a operação de inclusão, o objeto acertado e o contexto da sessão

  Cenário: Reenviar a mesma consulta não remonta a lista
    Dado que acabei de consultar uma coordenação, uma subclasse e um gênero
    Quando envio de novo exatamente os mesmos valores
    Então a lista não é remontada

  Cenário: Gênero sem prioridades na lista
    Dado que a lista daquele gênero está vazia
    Quando a página do gênero é apresentada
    Então vejo a mensagem "* Genero sem prioridades cadastradas *"
    E nenhuma linha é preenchida

  Cenário: Abrir a tela sem um gênero em curso
    Dado que eu tinha uma lista de prioridades de um gênero
    Quando abro a tela sem ter um gênero em curso
    Então a minha lista de prioridades é apagada
    E a página aparece vazia

  Cenário: Alteração sem ter consultado antes
    Dado que a coordenação, a subclasse e o gênero informados não são os do último gênero consultado
    Quando envio a alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo do gênero

  Cenário: A alteração grava a prioridade nova
    Dado que consultei o gênero e a lista está na tela
    Quando informo uma prioridade nova na linha de um contrato com a ação de alteração
    Então a prioridade fica gravada na permissão daquele contrato
    E a linha da minha lista fica com a prioridade nova
    E a alteração deixa registro na auditoria

  Cenário: Prioridade igual à registrada não grava nada
    Dado que consultei o gênero e a lista está na tela
    Quando confirmo a ação de alteração sem mudar a prioridade da linha
    Então nada é gravado para aquele contrato

  Cenário: A prioridade nova alcança todas as permissões daquele contrato e vigência
    Dado que o mesmo contrato e a mesma vigência têm mais de uma permissão para o gênero
    Quando confirmo a ação de alteração com uma prioridade nova
    Então todas essas permissões ficam com a prioridade nova
    E cada uma deixa o seu registro na auditoria

  Cenário: Linha sem a ação de alteração não é processada
    Dado que a lista está na tela
    Quando deixo a ação de uma linha em branco, ou com outra letra
    Então aquela linha não é processada
    E nada é gravado para ela

  Cenário: As colunas de retorno vêm dos cadastros
    Dado que a lista está na tela
    Quando altero o tipo de contrato, a prioridade do contrato, o fornecedor ou o número com sinal
    E confirmo
    Então esses valores voltam como estão nos cadastros
    E não como eu digitei

  Cenário: O cabeçalho mostra a data do sistema e o tipo de órgão da sessão
    Dado que entrei pelo LOGON
    Quando abro a tela C341T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: Digitação não numérica
    Dado que digito algo que não é número em um dos campos informados
    Quando envio a resposta
    Então o sistema recusa a digitação antes de ler qualquer cadastro

  Cenário: O resultado da consulta anterior não fica na tela
    Dado que já consultei um gênero e a tela mostrou o resultado
    Quando envio uma consulta nova
    Então as descrições e a data da consulta anterior não ficam na tela

  Cenário: Toda gravação deixa rastro na auditoria
    Dado que consultei um gênero e alterei a prioridade de uma linha
    Quando as gravações terminam
    Então existe um registro na auditoria para cada linha incluída na lista
    E existe um registro para a permissão alterada
    E cada registro traz o tipo de órgão, a matrícula, a coordenação regional, a tela de origem, a estação, a operação e os valores antes e depois

  Cenário: A tela não inclui nem exclui permissão
    Dado que estou na tela C341T
    Quando consulto o gênero e altero prioridades
    Então nenhuma permissão de contrato é incluída ou excluída
    E os cadastros de contratos, de fornecedores e de gêneros são apenas lidos

  Cenário: A tela não encadeia em outra
    Dado que alterei a prioridade de uma linha
    Quando a resposta é processada
    Então nenhum registro e nenhuma operação são passados para outra tela
    E a tela continua sendo a última da jornada
```
