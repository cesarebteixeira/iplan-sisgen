# US — E057T — Consulta do preparo semanal e pedidos de saída

## Estória

Como **servidor de CRE**, quero **consultar o preparo de uma semana de um órgão filho
SDI da minha coordenadoria regional e, a partir dele, pedir a listagem, pedir o arquivo
por correio eletrônico ou mandar o preparo para distribuição**, para que **a secretaria
veja, antes de a merenda sair, o que a semana tem calculado de cada gênero em cada dia —
e possa levar esse número para o papel, para a planilha ou para a distribuição sem
redigitar nada**.

O preparo da alimentação escolar de uma semana já chega a esta tela calculado: as
quantidades de cada gênero, dia a dia, estão na base, e o que falta é alguém olhar o
conjunto e decidir o que fazer com ele. É esta tela que mostra o conjunto — o órgão, o
período e o que está reservado em cada dia — e é ela que pede as três saídas que dependem
desse número: a listagem, o arquivo que sai pelo correio eletrônico de quem pediu e o
encaminhamento para a distribuição. Sem ela, o preparo continua existindo na base e
ninguém o vê junto; e não haveria por onde pedir, a partir do órgão, nem a listagem nem o
arquivo.

## Contexto

Jornada S000M → E000M → E050M → E057T.
Ator: servidor de CRE — informa o órgão filho SDI, a coordenação regional escolar e a data
de início do preparo, confere o que a semana tem calculado e, a partir daí, pede a
listagem, pede o arquivo ou manda o preparo para distribuição.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. O `E000M` e o `E050M` são menus e não gravam nada: eles
apenas encaminham.

Da sessão a tela usa o tipo de órgão, a matrícula, o código de acesso e o vínculo do
servidor — o órgão filho e a coordenação que ele alcança. No cabeçalho ela mostra a
descrição do tipo de órgão e a data do sistema, que vêm do ambiente da sessão.

Esta tela **não muda de comportamento conforme quem a chamou**. Ela tem porta própria no
menu desta jornada, é também alcançada por encadeamento a partir de outra tela do acervo
(fora desta jornada) e, nos dois casos, abre do mesmo jeito: em consulta, com a operação
que a tela que a chamou tenha deixado na passagem descartada (RN-02). O que muda o que a
tela mostra é o que a passagem traz carregado: chegando com um preparo já carregado, ela o
apresenta e o submete à conferência de preparo completo (RN-13).

Esta tela **encadeia para fora** em dois casos, e as duas passagens — para a E050T e para
a E055T — estão nas regras abaixo (RN-13 e RN-16), porque é delas que sai o comportamento
das telas seguintes. Fora disso, a tela termina nela mesma.

## Regras de negócio

### RN-01 — A tela mostra o preparo de uma semana, dia a dia e gênero a gênero

Informados o órgão filho SDI, a coordenação regional escolar e a data de início do
preparo, a tela mostra o preparo daquela semana:

- **no alto**, a descrição do tipo de órgão, a data do sistema, o nome do órgão, a
  coordenação regional escolar, a marca de creche do órgão (mostrada como **Sim** ou
  **Nao**), a data de início e a data limite do preparo e o início e o limite do período;
- os **sete** dias do preparo, cada um com o **dia do mês e o dia da semana** e com a
  **letra da semana do cardápio** que cobre aquele dia;
- **até treze** linhas de gênero, cada uma com o **código da subclasse e do gênero**
  (subclasse, ponto, gênero), a **descrição do gênero** e **sete quantidades**, uma para
  cada um dos sete dias mostrados.

A quantidade zerada aparece em branco. Acabando os gêneros do preparo, as linhas restantes
ficam em branco. Ao pé da tela há os campos de subclasse e de gênero que **posicionam a
lista**: preenchidos, a lista começa naquele par.

[?] Enchendo a lista as treze linhas, a posição fica guardada de uma passagem para a
seguinte — é assim que ela continua na página seguinte — e essa posição **não** é zerada
quando o servidor troca de órgão ou de data: a consulta nova pode abrir no meio do preparo,
em vez de no primeiro gênero. E, como a leitura seguinte parte da subclasse e do gênero
guardados, não se sabe, só pelo fonte, se a nova lista repete a última linha da anterior ou
continua depois dela — a semântica dos sinalizadores dessa leitura não está no corpus nem no
manual. Pergunta ao site.

### RN-02 — A tela só aceita consultar, e é isso que ela força

A tela serve para **consultar** o preparo: ela não inclui, não altera e não exclui. A
operação é conferida antes das demais conferências, e qualquer coisa diferente de
consultar é recusada com **\* Opcao nao disponivel. Use CON \***, com o cursor de volta ao
campo da operação e nada pedido. Ao reabrir o preparo, a própria tela repõe a operação
como consultar.

[?] A tela é também chamada por outra tela do acervo que lhe passa a passagem marcada como
**alteração**; como ela repõe a operação como consulta, quem a chama pedindo alteração
recebe consulta. Se existe caso em que esta tela deva abrir em alteração, o acervo lido não
mostra. Pergunta ao site.

### RN-03 — O acesso à tela e a permissão da consulta são conferidos antes de tudo

Antes de qualquer conferência de dados, a abertura confere a estação da sessão com a
estação do cadastro do servidor e procura a tela no cadastro de telas do seu código de
acesso. Não achando a tela no cadastro, a recusa é **\* Tela nao disponivel \***; achando a
tela mas sem ela liberada para aquele código de acesso, a recusa é
**\* Acesso negado para esta matricula \***. Depois, a operação é conferida contra a
liberação daquele código naquela tela: sem a consulta liberada, a recusa é
**\* Acesso negado para esta operacao \***. Em qualquer dos casos a passagem termina sem
nada mostrar e sem nada gravar.

### RN-04 — O órgão filho SDI é obrigatório

O código do órgão tem de ser informado. Em branco, a recusa é **\* Informe o orgao \***,
com o cursor de volta ao campo do órgão e nada pedido. A tela abre com o órgão do vínculo
do servidor já preenchido, quando ele tem um.

### RN-05 — A data de início do preparo é obrigatória

A data de início do preparo tem de ser informada. Em branco, a recusa é
**\* Informe a data de inicio do preparo \***, com o cursor de volta ao campo do dia e nada
pedido.

### RN-06 — Quem tem órgão no vínculo não consulta o preparo de outro

O órgão informado tem de ser o do vínculo do servidor. Quem tem um órgão no vínculo e
informa outro é recusado com **\* Usuario sem acesso a outro orgao \*** — a mensagem traz o
código do órgão do vínculo —, com o cursor de volta ao campo do órgão e nada pedido. Quem
não tem órgão no vínculo consulta o que informar. Quando o órgão informado é o mesmo que já
está carregado, a conferência não roda.

### RN-07 — O órgão informado tem de estar cadastrado

Do cadastro de órgãos vêm o nome do órgão, a coordenação regional escolar dele e a marca de
creche que a tela mostra. Órgão não cadastrado é recusado com **\* Orgao nao cadastrado \***,
com o cursor de volta ao campo do órgão e nada pedido.

### RN-08 — O órgão tem de ser de uma coordenação do servidor

Quando a sessão traz uma coordenação regional escolar, o órgão informado tem de ser de uma
coordenação igual à dela. Sendo de outra, a recusa é
**<- Usuario sem acesso ao grupo deste orgao \*** — a mensagem traz o código da coordenação
do órgão —, com o cursor de volta ao campo do órgão e nada pedido. Quando a sessão não traz
coordenação, esta conferência não é feita.

### RN-09 — O preparo tem de existir para o órgão e a data

Com o órgão cadastrado e da coordenação do servidor, a tela procura o preparo daquele órgão
na data informada. Não achando, a recusa é **\* Requisicao nao cadastrada \***, com o
cursor de volta ao campo do dia da data de início do preparo, e nada pedido.

[?] A procura é feita com a subclasse e o gênero zerados. Se ela exige um registro exato —
e então o preparo tem um registro próprio, sem subclasse nem gênero —, ou se basta
posicionar no primeiro gênero do conjunto, não se sabe: a semântica dos sinalizadores dessa
leitura não está no corpus nem no manual. A diferença é visível para quem usa a tela: com o
registro exato, um preparo sem nenhum gênero é recusado como não cadastrado; com o
posicionamento, ele é aceito e a lista sai vazia. Pergunta ao site.

### RN-10 — A coordenação informada não escolhe o preparo

O campo da coordenação regional escolar é mostrado e pode ser preenchido, mas não é ele que
a tela usa para procurar o preparo: a procura é feita pela coordenação que está no cadastro
do órgão informado, e é essa que a tela repõe no campo. Uma coordenação diferente da do
órgão não muda o resultado da consulta nem gera recusa — ela é apenas substituída pela do
órgão.

[?] A coordenação vem do cadastro do órgão e a conferência de acesso compara a coordenação
do órgão com a da sessão; a que o servidor digita não entra em nenhuma das duas. Se o campo
existe para o servidor escolher alguma coisa, essa escolha não é atendida. Pergunta ao
site.

### RN-11 — Os sete dias do preparo e a letra da semana do cardápio

A partir da data de início do preparo, a tela monta os **sete** dias do preparo — a data
informada e os seis dias seguintes. Para cada dia ela mostra o dia do mês e o dia da semana
e busca, no cadastro de períodos semanais do cardápio do órgão e da sua coordenação, a
**letra da semana** que cobre aquele dia.

[?] Quando não há período de cardápio cadastrado para um dos dias, a leitura não acha o
registro e a letra mostrada é a que ficou da leitura anterior; o que o cadastro devolve
numa leitura não achada não está no corpus. O preparo sem alguma das sete letras é tratado
como preparo incompleto (RN-13), de modo que, se a leitura repetir a letra do dia anterior,
essa conferência não o percebe. Pergunta ao site.

### RN-12 — A descrição do gênero vem do cadastro vigente no início do período

Cada linha traz o código da subclasse e do gênero e a **descrição do gênero**, lida do
cadastro de gêneros vigente na data de início do período — os gêneros excluídos ficam fora.
Sem o gênero no cadastro, a linha aparece com o código e a descrição em branco, e a tela
não recusa por isso.

[?] A linha sem descrição não é conferida nem avisada. Se a intenção era recusar o preparo
que tem gênero fora do cadastro, a conferência não existe nesta tela. Pergunta ao site.

### RN-13 — O preparo incompleto volta para a inclusão da requisição

Carregado o preparo, a tela confere se ele está completo. Se o preparo é de um órgão
diferente do que está no vínculo do servidor, ou se alguma das quatro datas — início e
limite do preparo, início e limite do período — está zerada, ou se o limite é anterior ao
início, ou se falta a letra de algum dos sete dias, ou falta o dia de algum dos sete dias,
ou se a marca de creche do órgão está em branco — a tela não mostra o preparo e **devolve o fluxo à E050T com a operação de
inclusão**, passando-lhe o órgão, a coordenação, a data de início do preparo e os demais
dados que estão na passagem, e termina.

A conferência do órgão alheio é a segunda vez que a tela barra o órgão de outro vínculo: a
primeira é a RN-06, quando o servidor o informa. Esta roda sobre o preparo que já chegou
carregado pela passagem, e o desfecho não é a recusa, e sim a inclusão.

[?] Um preparo que existe, mas está incompleto, leva o servidor a abrir uma **inclusão**, e
não a ver o que há nem a corrigir o que falta. Se a intenção era recusar e mostrar a
pendência, o desfecho não é esse. Pergunta ao site.

[?] A marca de creche do órgão em branco seria mostrada como **Sim** e, ao mesmo tempo, é
tratada como preparo incompleto: a mesma leitura dá dois desfechos e não se sabe qual o
site quer. Pergunta ao site.

### RN-14 — Com o código de impressão, a tela pede a listagem do preparo

Preenchido o **código de impressão** — e passadas as conferências — a tela registra **um
pedido** na fila de requisições e o entrega ao processamento em lote, que monta a listagem
do preparo daquele órgão e daquela semana. Antes de pedir, ela confere se já existe um
pedido daquela listagem para o mesmo órgão esperando processamento: havendo, a recusa é
**\* Relatorio em processamento. Aguarde. \***, com o cursor de volta ao campo e nada
pedido. Em branco, nada é pedido.

[?] O código de impressão é o único dado da tela que não passa por edição nem por
conferência: qualquer valor de até dez caracteres é aceito e vai para o pedido. Se ele
deveria apontar para um destino de impressão cadastrado, esta tela não o confere. Pergunta
ao site.

[?] Antes de pedir a listagem, a tela repete a conferência de que existem registros para
aquele preparo — **\* Nao existem registros para este preparo \*** —, e o caminho que chega
ali já exigiu o mesmo registro, pela mesma chave. Pela leitura do fonte, essa recusa só
teria como aparecer se o preparo fosse apagado entre a leitura que o carregou e esta. Ou a
conferência serve a outro caminho, ou ficou sem como ser alcançada. Pergunta ao site.

### RN-15 — Com o indicador de arquivo, a tela pede o arquivo por correio eletrônico

Marcado o **indicador de arquivo**, a tela faz o mesmo para o **arquivo** do preparo:
registra o pedido na fila e o entrega ao processamento em lote. O arquivo sai pelo
**correio eletrônico do servidor**, lido do cadastro de funcionários no momento do pedido;
sem endereço de correio cadastrado para a matrícula, a recusa é
**<- Usuario sem e-mail cadastrado \***, com o cursor de volta ao campo, e nada é pedido.
Já havendo um pedido de arquivo do mesmo órgão esperando processamento, a recusa é
**\* Arquivo em processamento. Aguarde. \***, também sem pedir nada.

O arquivo tem **precedência sobre a listagem**: pedindo os dois na mesma passagem, a tela
registra o arquivo e descarta o código de impressão — o relatório não chega a ser pedido, e
o servidor não é avisado disso.

[?] O descarte silencioso do código de impressão é o único desfecho em que um dado
preenchido pelo servidor é jogado fora sem mensagem. Se os dois pedidos deveriam conviver,
ou se pedir os dois deveria ser recusado em vez de atendido pela metade, o acervo lido não
diz. Pergunta ao site.

[?] A recusa do arquivo já em processamento devolve o cursor ao campo do **código de
impressão**, e não ao campo do indicador de arquivo; a recusa por falta de correio
eletrônico usa o campo do indicador. Se o cursor no campo do código de impressão é erro de
tela, é pergunta ao site.

### RN-16 — O indicador de distribuição encaminha o preparo para a distribuição

Marcado o **indicador de distribuição** — e não tendo sido pedido nem o arquivo nem a
listagem — a tela não pede nada: ela passa para a **E055T** o órgão, a coordenação, a marca
de creche, a data de início e o limite do preparo, o início e o limite do período e os sete
dias que tem na passagem, com a operação marcada como **alteração** e a posição da lista
zerada, e termina. É essa operação de alteração que a E055T recebe para abrir a
distribuição.

### RN-17 — O que a tela registra na fila de requisições

Cada pedido — o do arquivo e o da listagem — é um registro novo na **fila de requisições**,
que tem capacidade para **90.000** pedidos (capacidade é o máximo esperado, parâmetro de
dimensionamento, não o que está na fila). O pedido leva:

- o **número seguinte** ao do último pedido da fila;
- o **código do relatório**: um para a listagem, outro para o arquivo;
- o **código de impressão**, quando é a listagem;
- o **endereço de correio** do servidor, quando é o arquivo;
- a **matrícula** de quem pediu, a **estação** e o **dia e o mês** do pedido;
- o **tipo de órgão**, o **órgão filho SDI** e a **coordenação regional**;
- a **tela que pediu** e os **parâmetros** do pedido: as datas do preparo e do período, o
  órgão e a marca de creche (no arquivo, também a matrícula e uma via);
- a operação marcada como **inclusão**; a situação do pedido fica em branco.

Gravado o pedido, a tela dispara o **processamento em lote** que monta o arquivo ou a
listagem. Enquanto o pedido está na fila, um novo pedido do mesmo relatório para o mesmo
órgão é recusado (RN-14 e RN-15).

### RN-18 — A consulta sem pedido não grava nada

Sem o código de impressão e sem os indicadores de arquivo e de distribuição, a passagem
termina sem gravar nada: a tela só mostra o preparo. É a consulta pura, e é o desfecho em
que nada é registrado na fila nem em lugar nenhum.

## Cenários BDD

```gherkin
Funcionalidade: Consultar o preparo de uma semana do órgão filho SDI e pedir o impresso, o arquivo ou a distribuição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E057T

  Cenário: A consulta mostra o preparo da semana do órgão
    Dado que o órgão filho SDI é da minha coordenação e está cadastrado
    E existe preparo para a data de início do preparo informada
    Quando peço a consulta
    Então vejo o nome do órgão, a coordenação, a marca de creche e as datas do preparo e do período
    E vejo os sete dias do preparo, cada um com o dia, o dia da semana e a letra da semana do cardápio
    E vejo as linhas de subclasse e gênero com a descrição e as sete quantidades
    E nada é gravado

  Cenário: Quantidade zerada aparece em branco
    Dado um preparo com um gênero sem quantidade em um dos dias
    Quando a linha é mostrada
    Então a quantidade daquele dia aparece em branco

  Cenário: Acabando os gêneros, as linhas restantes ficam em branco
    Dado um preparo com menos gêneros do que as linhas da tela
    Quando a lista é montada
    Então as linhas que sobram aparecem em branco

  Cenário: A lista começa na subclasse e no gênero informados
    Dado que preencho a subclasse e o gênero no pé da tela
    Quando a lista é montada
    Então ela começa naquele par de subclasse e gênero

  Cenário: Operação diferente de consultar é recusada
    Dado que informei uma operação diferente de consultar
    Quando a tela confere a operação
    Então vejo "* Opcao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nada é pedido

  Cenário: A operação deixada pela tela que me chamou é descartada
    Dado que cheguei à tela por encaminhamento de outra tela, com a passagem marcada como alteração
    Quando a tela reabre o preparo
    Então a operação volta a ser consulta
    E nada é gravado

  Cenário: Acesso à tela sem autorização
    Dado que o meu código de acesso não tem a tela E057T no seu cadastro
    Quando a tela tenta abrir
    Então vejo "* Tela nao disponivel *"
    E nada é gravado

  Cenário: Consulta não liberada para o meu código de acesso
    Dado que o meu código de acesso não tem a tela E057T liberada
    Quando a tela confere o acesso
    Então vejo "* Acesso negado para esta matricula *"
    E nada é gravado

  Cenário: Operação não liberada para o meu código de acesso
    Dado que o meu código de acesso não tem a consulta liberada nesta tela
    Quando a tela confere a operação
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Órgão filho em branco é recusado
    Dado que deixei o órgão filho SDI em branco
    Quando a tela confere os dados
    Então vejo "* Informe o orgao *"
    E o cursor volta ao campo do órgão
    E nada é pedido

  Cenário: Data de início do preparo em branco é recusada
    Dado que deixei a data de início do preparo em branco
    Quando a tela confere os dados
    Então vejo "* Informe a data de inicio do preparo *"
    E o cursor volta ao campo do dia
    E nada é pedido

  Cenário: Órgão de outro vínculo é recusado
    Dado que o meu vínculo tem um órgão filho SDI
    Quando informo outro órgão
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor volta ao campo do órgão
    E nada é pedido

  Cenário: Órgão não cadastrado é recusado
    Dado um órgão filho SDI que não existe no cadastro de órgãos
    Quando a tela procura o órgão
    Então vejo "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão
    E nada é pedido

  Cenário: Órgão de outra coordenação é recusado
    Dado que a minha sessão traz uma coordenação regional escolar
    Quando informo um órgão de outra coordenação
    Então vejo "<- Usuario sem acesso ao grupo deste orgao *"
    E o cursor volta ao campo do órgão
    E nada é pedido

  Cenário: Preparo não cadastrado para o órgão e a data é recusado
    Dado que não existe preparo para o órgão e a data informados
    Quando a tela procura o preparo
    Então vejo "* Requisicao nao cadastrada *"
    E o cursor volta ao campo do dia da data de início do preparo
    E nada é pedido

  Cenário: A coordenação informada não muda a consulta
    Dado que informo uma coordenação diferente da que está no cadastro do órgão
    Quando a tela procura o preparo
    Então ela procura pela coordenação do cadastro do órgão
    E mostra a coordenação do órgão

  Cenário: A marca de creche do órgão é mostrada como Sim ou Nao
    Dado um órgão cadastrado como creche
    Quando a consulta mostra o cabeçalho
    Então a marca aparece como "Sim"
    E, não sendo creche, aparece como "Nao"

  Cenário: Sem a descrição do gênero, a linha sai com a descrição em branco
    Dado um gênero do preparo que não está no cadastro de gêneros do período
    Quando a linha é mostrada
    Então o código aparece e a descrição fica em branco
    E a tela não recusa por isso

  Cenário: Preparo incompleto é devolvido à inclusão da requisição
    Dado um preparo já carregado ao qual falta a letra de um dos sete dias
    Quando a tela confere o preparo
    Então ela não mostra o preparo
    E devolve o fluxo à tela E050T com a operação de inclusão
    E passa o órgão, a coordenação e a data de início do preparo

  Cenário: Preparo de outro órgão é devolvido à inclusão da requisição
    Dado um preparo já carregado de um órgão diferente do meu vínculo
    Quando a tela confere o preparo
    Então ela não mostra o preparo
    E devolve o fluxo à tela E050T com a operação de inclusão

  Cenário: Com o código de impressão, a listagem do preparo é pedida
    Dado um preparo completo e carregado
    E que não existe pedido daquela listagem para o mesmo órgão esperando processamento
    Quando preencho o código de impressão e confirmo
    Então um pedido de listagem é registrado na fila de requisições
    E o processamento em lote é disparado
    E o pedido leva o número seguinte da fila e os dados da consulta

  Cenário: Listagem já em processamento é recusada
    Dado que já existe um pedido daquela listagem para o mesmo órgão esperando processamento
    Quando preencho o código de impressão e confirmo
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E nada é pedido

  Cenário: Com o indicador de arquivo, o arquivo é pedido e sai por correio eletrônico
    Dado um preparo completo e carregado
    E que tenho endereço de correio cadastrado
    Quando marco o indicador de arquivo e confirmo
    Então um pedido de arquivo é registrado na fila de requisições
    E o pedido leva o meu endereço de correio
    E o processamento em lote é disparado

  Cenário: Arquivo já em processamento é recusado
    Dado que já existe um pedido de arquivo para o mesmo órgão esperando processamento
    Quando marco o indicador de arquivo e confirmo
    Então vejo "* Arquivo em processamento. Aguarde. *"
    E nada é pedido

  Cenário: Sem endereço de correio cadastrado, o arquivo não é pedido
    Dado que o meu cadastro de funcionário não tem endereço de correio
    Quando marco o indicador de arquivo e confirmo
    Então vejo "<- Usuario sem e-mail cadastrado *"
    E o cursor volta ao campo do indicador de arquivo
    E nada é pedido

  Cenário: Pedindo o arquivo e a listagem, só o arquivo é pedido
    Dado um preparo completo e carregado
    Quando marco o indicador de arquivo e preencho o código de impressão
    Então um pedido de arquivo é registrado
    E o pedido de listagem não é feito
    E não sou avisado de que a listagem ficou de fora

  Cenário: Com o indicador de distribuição, o preparo vai para a distribuição
    Dado um preparo completo e carregado
    E que não pedi nem o arquivo nem a listagem
    Quando marco o indicador de distribuição e confirmo
    Então a tela passa para a E055T o órgão, a coordenação, as datas e os sete dias
    E a passagem vai marcada como alteração
    E a posição da lista vai zerada

  Cenário: A consulta sem pedido não grava nada
    Dado um preparo completo e carregado
    Quando confirmo sem preencher o código de impressão nem marcar os indicadores
    Então a tela só mostra o preparo
    E nada é registrado na fila de requisições
```
