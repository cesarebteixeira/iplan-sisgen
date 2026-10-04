# US — C066T — Lançamento do apostilamento por item das permissões da CRE

## Estória

Como **servidor de CRE**, quero **lançar, item a item, o apostilamento das permissões da minha
coordenação regional escolar**, para que **o valor apostilado de cada item e o total apostilado da
permissão passem a refletir o que foi calculado e efetivamente apostilado, e o contrato siga com o
valor certo**.

O apostilamento é o registro posterior que atualiza o valor de uma permissão da coordenação
regional escolar, e ele é lançado gênero a gênero. O que se lança aqui não é um valor solto: o
lançamento consome o cálculo que já foi feito para aquela permissão e aquele gênero, soma o valor
informado ao valor apostilado da permissão e guarda o item apostilado com a data e com quem o
lançou. Sem esse lançamento, o cálculo fica parado e o valor apostilado da permissão não anda; e é
justamente o item lançado que a tela de estorno depois desfaz e a tela de consulta depois mostra.

## Contexto

Jornada S000M → C000M → C050M → C066M → C066T.
Ator: servidor de CRE — lança, item a item, o apostilamento das permissões da sua coordenação
regional escolar, por tipo de contrato, período e grupo de licitação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

Esta é uma das telas do mesmo menu que tratam do mesmo registro: a `C062T` calcula o apostilamento
por gênero, esta o lança item a item, a `C065T` passa para esta ao terminar, a `C067T` o consulta e
a `C064T` o estorna. O que esta tela grava é o efeito do lançamento — o valor apostilado do item e
o total apostilado da permissão — e o que ela apaga é o cálculo daquele gênero, já consumido.

As regras abaixo são só as da **tela desta jornada**. O que esta tela recebe da entrada — a
secretaria, o órgão e a matrícula da sessão — está no anexo de evidências, na seção das regras que
se revelaram da entrada.

---

## Regras de negócio

### RN-01 — Esta tela lança o apostilamento por item: é ela que grava e que apaga

Esta é a porta de entrada do apostilamento por item: é uma tela de gravação, não de consulta. Ela
enxerga dez cadastros — o de telas do sistema, o do tipo de órgão, o de gêneros, o do cálculo do
apostilamento, o da permissão da coordenação regional escolar, o do tipo de licitação, o da
liberação desta tela por tipo de licitação, o do item de apostilamento, a trilha de auditoria e o
registro de alterações — e, para cada um deles, o sistema traz prontas uma operação de gravar e uma
de apagar. Aqui só cinco dessas operações são executadas: a permissão é regravada com o valor
apostilado do item e com o total apostilado, o item de apostilamento é criado, a trilha de auditoria
e o registro de alterações recebem o rastro da gravação, e o cálculo daquele gênero é apagado.
Nenhum outro cadastro é gravado nem apagado por esta tela.

Os números de capacidade são de dimensionamento, não volume cadastrado: a permissão, o cálculo do
apostilamento e o item de apostilamento comportam 1.000.000 de registros cada um, o gênero 150.000,
o cadastro de telas 2.000, o tipo de licitação e a liberação da tela 1.000 cada um, o tipo de órgão
200, o registro de alterações 200.000 e a trilha de auditoria 60.000.000.

### RN-02 — O que identifica a permissão e o item

A permissão é identificada pela coordenação regional escolar, pelo tipo de contrato e pela data
limite do período — dia, mês e ano —, sempre dentro do órgão da sessão. O item, dentro dela, pelo
grupo de licitação, pela classe, pela subclasse e pelo gênero. A data de início do período aparece
na tela, mas não identifica nada: é a que o cálculo registrou para aquele item. A tela trabalha com
até treze itens por vez, uma linha para cada.

O que se digita são quatorze campos com rótulo: a coordenação regional escolar, o tipo de contrato,
as três partes do início do período, as três partes da data limite, o tipo de licitação, o grupo de
licitação, a classe, a subclasse, o gênero e o valor a apostilar por item; além deles há, em cada
linha, uma marca de situação.

[?] Quando um desses campos é recusado por não ser numérico, o cursor volta sozinho apenas para
cinco deles — a coordenação regional, o tipo de contrato e as três partes da data limite. Para os
outros nove, a fonte não diz onde o cursor fica. Pergunta ao site se é intencional.

### RN-03 — O tipo de órgão é o da secretaria da sessão, e não se digita

O tipo de órgão não se digita nesta tela: é o da secretaria que o vínculo da matrícula escolheu no
LOGON e que ficou na sessão, e ele entra na identificação de tudo o que a tela lê e grava. O
cabeçalho apenas mostra a descrição desse tipo de órgão, junto com a data do sistema; o servidor não
tem como lançar apostilamento no acervo de outro órgão.

### RN-04 — A permissão informada tem de estar cadastrada

Informados a coordenação regional, o tipo de contrato e a data limite, o sistema procura a permissão
correspondente. Não existindo, o lançamento é recusado com **\* Permissao nao cadastrada \***, com o
cursor de volta no campo da coordenação regional escolar, e a transação não segue.

[?] A fonte não fecha o que acontece depois de uma recusa: as recusas desta tela anunciam a
mensagem mas não marcam, no que está no acervo desta jornada, o erro que barra a gravação — quem
poderia marcá-lo é a rotina de comunicação, que não está no acervo. A dúvida vale para todas as
recusas desta tela (RN-04 a RN-07): não concluo se uma transação recusada ainda assim grava.
Pergunta ao site.

### RN-05 — A tela tem de estar liberada para o tipo de licitação da permissão

A permissão tem um tipo de licitação. O sistema procura, para esse tipo de licitação, a liberação de
uso desta tela. Não estando a tela liberada, o lançamento é recusado com
**\* Tela nao disponivel para esta licitacao \***, com o cursor de volta no campo da coordenação
regional escolar, e nada é gravado. Passando a conferência, o tipo de licitação da permissão e a sua
descrição são mostrados no cabeçalho.

### RN-06 — A permissão tem de ter o apostilamento calculado

A permissão precisa ter o apostilamento calculado, gênero a gênero. Se não houver nenhum cálculo
para ela, o lançamento é recusado com **\* Permissao sem generos a apostilar \***; se houver
cálculos, mas nenhum deles com valor calculado, a recusa é
**\* Apostilamento ainda nao calculado \***. Nos dois casos o cursor volta ao campo da coordenação
regional escolar e nada é gravado.

Ao se reapresentar a última permissão usada na sessão, o caso de ela já não ter cálculo nenhum
aparece como **\* Permissao sem registros calculados \***, com a lista em branco.

[?] A descrição do gênero de cada linha só é lida dos gêneros que não estão marcados com D no
cadastro; o que essa marca significa não está no acervo desta jornada: não concluo se é exclusão
lógica do cadastro ou outra coisa. Pergunta ao site.

### RN-07 — O item marcado na linha tem de ter cálculo

Para o item que o servidor marca na linha, o sistema exige o cálculo correspondente. Não havendo
cálculo para aquela classe, subclasse e gênero, o lançamento é recusado com
**\* Genero sem calculo para este apostilamento \***, com o cursor de volta à marca da linha, e nada
é gravado.

### RN-08 — A tela só executa a alteração

A tela é de alteração e não aceita outra operação. Um valor que não seja um código de operação
conhecido é recusado pelo próprio roteamento do sistema, com **\* Operacao nao disponivel \***, e a
transação não segue. Um código de inclusão, de exclusão ou de consulta é aceito pelo roteamento e
recusado por esta tela, com **\* Operacao nao disponivel. Use ALT \***, com o cursor de volta no
campo da opção, e nada é gravado. Ao se apresentar, é a própria tela que marca a operação como
alteração.

[?] A recusa por operação manda usar ALT, mas a conferência da tela compara o valor com o código
interno de alteração, que é outro. Ou o terminal traduz o mnemônico antes de enviar, ou as mensagens
estão desalinhadas das conferências. Pergunta ao site; não concluo qual dos dois.

### RN-09 — Sem nenhuma linha marcada, a tela não grava nada

A gravação só acontece para a linha que o servidor marcou: a marca de situação, de um caractere, é a
única coisa que autoriza o lançamento, e a tela nunca a escreve — quem a digita é o servidor. Sem
nenhuma linha marcada, a transação apenas confere e reapresenta: a tela serve também para ver os
itens calculados da permissão sem apostilar nada.

[?] A marca não tem rótulo validado como os demais campos, e a fonte não diz o que ela significa: o
material só mostra que **S** é o valor que dispara o lançamento. Pergunta ao site.

[?] A gravação é executada uma vez por transação, com os dados de uma única linha. Se o servidor
marcar mais de uma linha na mesma tela, a fonte não diz se todas são lançadas ou apenas uma: quem
decide isso é a rotina de comunicação, que não está no acervo desta jornada. Pergunta ao site.

### RN-10 — O servidor informa o valor a apostilar, item a item

Para o item que marcou, o servidor informa o valor a apostilar, com duas casas. A linha mostra o
gênero com a sua descrição e o valor que o cálculo lhe atribuiu; é o valor informado que entra na
permissão.

[?] A tela preenche o valor da linha com o valor calculado e depois o apaga quando o terminal é de
um certo tipo; o material não diz o que esse tipo é. Não concluo se o servidor digita o valor ou se
confirma o valor calculado. Pergunta ao site.

### RN-11 — O que a confirmação grava

Confirmada a linha marcada, o sistema lança o valor informado na permissão: o valor apostilado
daquele item passa a ser o anterior mais o valor informado, e o total apostilado da permissão recebe
o mesmo acréscimo em todos os registros daquela permissão, de modo que ele continue igual em todos
os itens dela. Em seguida cria o item de apostilamento, com o órgão, a coordenação regional, o tipo
de contrato, a data limite, o grupo de licitação, a classe, a subclasse e o gênero, o valor lançado,
a data do dia, a data-base e a data do cálculo que o originou, a matrícula de quem calculou e a
matrícula de quem lançou.

Por fim apaga o cálculo daquele gênero e deixa o rastro: a trilha de auditoria guarda o registro da
permissão como estava e como ficou, com a operação, a matrícula, o terminal, a data e a hora; o
registro de alterações guarda a mesma gravação, identificando se foi o item apostilado ou um dos
demais registros daquela permissão.

[?] A trilha de auditoria recebe, como registro anterior e como registro resultante, a mesma área de
trabalho, lida antes e depois da regravação. O acervo não define a semântica dessa área no dialeto;
não concluo se as duas imagens saem diferentes na trilha. Pergunta ao site.

### RN-12 — O gênero apostilado sai do cálculo: o mesmo item não se lança duas vezes

O lançamento consome o cálculo: o registro de cálculo daquele gênero é apagado na mesma transação em
que o item de apostilamento é criado. Por isso um segundo lançamento do mesmo gênero é recusado, com
**\* Genero sem calculo para este apostilamento \*** — é a tela de cálculo do mesmo menu, a `C062T`,
que produz o cálculo de novo quando ele deve existir.

### RN-13 — A tela reapresenta a última permissão informada na sessão

Ao ser usada de novo na mesma sessão, a tela volta à última permissão informada — a mesma
coordenação regional, o tipo de contrato e a data limite — e remonta a lista dos itens calculados a
partir dela. Enquanto não houver nenhuma permissão informada na sessão, ela abre sem nada preenchido
e sem lista. Quando quem a chamou foi a `C065T`, os códigos de item chegam limpos.

[?] A tela limpa os códigos de item quando o registro da área de trabalho diz que a tela anterior
foi a `C065T`, e é a própria `C065T` que os deixa marcados ao passar para esta. O que a `C065T`
deixa na área de trabalho, e por que isso obriga a limpar os códigos, não pôde ser conferido nesta
jornada. Pergunta ao site.

### RN-14 — Só quem tem a tela liberada e permissão de alteração chega a gravar

O lançamento é feito dentro da secretaria e do órgão da sessão. O sistema confere, no cadastro de
acesso, se o perfil da matrícula tem esta tela e, para a alteração, se o perfil permite alterar.
Faltando a tela no perfil, a transação é recusada com **\* Acesso negado para esta matricula \***;
faltando a permissão de alteração, com **\* Acesso negado para esta operacao \***; e, se a tela não
estiver registrada ou não estiver disponível para o perfil, com **\* Tela nao disponivel \***. Em
qualquer um dos casos, nada é lido e nada é gravado.

### RN-15 — Quando outra tela chama esta marcando um próximo destino, ela não confere nem grava

Esta tela pode chegar já com um próximo destino marcado por quem a chamou, dentro da mesma
transação. Nesse caso o roteamento do sistema assume e devolve o controle à tela marcada, e esta
tela não faz nenhuma das conferências de cadastro desta jornada e não grava. Esta é a última tela da
jornada: ela não entrega registro nem operação a uma tela seguinte.

[?] O próximo destino não está definido no acervo desta jornada: a fonte só mostra que, preenchido,
ele desvia o roteamento e pula as conferências. Não concluo quem o preenche nem se esse caminho é
alcançável pelo terminal. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Lançar o apostilamento por item das permissões da CRE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C066T

  Cenário: RN-02, RN-03 e RN-10 — lançar o apostilamento de um item
    Dado que existe permissão para a minha coordenação regional escolar, com o tipo de contrato e a data limite que informei
    E ela tem o apostilamento calculado por gênero
    E o gênero que informei tem cálculo
    Quando informo o valor a apostilar naquela linha e a marco com S
    Então o valor apostilado daquele item passa a ser o anterior mais o valor que informei
    E o total apostilado da permissão é acrescido do mesmo valor
    E vejo no cabeçalho a descrição do meu tipo de órgão, a data do sistema e o tipo de licitação com a sua descrição

  Cenário: RN-02 — a lista acaba antes das treze linhas
    Dado que a permissão tem menos itens calculados do que linhas
    Quando confirmo o lançamento
    Então as linhas que sobram ficam em branco
    E nenhuma mensagem é mostrada

  Cenário: RN-02 — campo não numérico
    Quando preencho a coordenação regional, o tipo de contrato, uma das datas, o tipo de licitação, o grupo de licitação ou um código de item com letra
    Então a tela recusa o campo antes de qualquer conferência de cadastro
    E nada é gravado

  Cenário: RN-11 — o item de apostilamento criado
    Dado que lancei o apostilamento de um item
    Então é criado um item de apostilamento com o órgão, a minha coordenação regional, o tipo de contrato, a data limite, o grupo de licitação, a classe, a subclasse e o gênero
    E ele guarda o valor lançado, a data do dia, a data-base e a data do cálculo de origem
    E guarda a matrícula de quem calculou e a minha matrícula

  Cenário: RN-11 — o rastro de cada gravação
    Dado que lancei o apostilamento de um item
    Então a trilha de auditoria guarda o registro da permissão como estava e como ficou, com a operação, a minha matrícula, o terminal, a data e a hora
    E o registro de alterações guarda a mesma gravação, identificando se foi o item apostilado ou um dos demais registros daquela permissão

  Cenário: RN-12 — o cálculo é consumido
    Dado que lancei o apostilamento de um gênero
    Quando tento lançar de novo o mesmo gênero da mesma permissão
    Então vejo "* Genero sem calculo para este apostilamento *"
    E o cursor volta à marca da linha
    E nada é gravado

  Cenário: RN-09 — sem linha marcada nada é gravado
    Dado que consultei uma permissão e vi os itens calculados
    Quando confirmo a alteração sem marcar nenhuma linha
    Então os valores da permissão continuam os mesmos
    E nenhum item de apostilamento é criado
    E nenhum cálculo é apagado

  Cenário: RN-04 — permissão não cadastrada
    Dado que não existe permissão para a coordenação regional, o tipo de contrato e a data limite que informei
    Quando confirmo o lançamento
    Então vejo "* Permissao nao cadastrada *"
    E o cursor volta ao campo da coordenação regional escolar
    E nada é gravado

  Cenário: RN-05 — a tela não está liberada para o tipo de licitação
    Dado que a permissão existe, mas esta tela não está liberada para o tipo de licitação dela
    Quando confirmo o lançamento
    Então vejo "* Tela nao disponivel para esta licitacao *"
    E o cursor volta ao campo da coordenação regional escolar
    E nada é gravado

  Cenário: RN-06 — permissão sem gêneros a apostilar
    Dado que a permissão existe, mas não tem nenhum cálculo de apostilamento
    Quando confirmo o lançamento
    Então vejo "* Permissao sem generos a apostilar *"
    E o cursor volta ao campo da coordenação regional escolar
    E nada é gravado

  Cenário: RN-06 — cálculo sem valor
    Dado que a permissão existe e tem cálculos, mas nenhum deles com valor calculado
    Quando confirmo o lançamento
    Então vejo "* Apostilamento ainda nao calculado *"
    E o cursor volta ao campo da coordenação regional escolar
    E nada é gravado

  Cenário: RN-06 — a última permissão da sessão perdeu os cálculos
    Dado que já usei uma permissão nesta sessão
    E aquela permissão não tem mais nenhum cálculo
    Quando abro a tela C066T de novo
    Então vejo "* Permissao sem registros calculados *"
    E a lista fica em branco

  Cenário: RN-07 — o gênero informado não tem cálculo
    Dado que a permissão tem itens calculados, mas o gênero que marquei não está entre eles
    Quando confirmo o lançamento
    Então vejo "* Genero sem calculo para este apostilamento *"
    E o cursor volta à marca da linha
    E nada é gravado

  Cenário: RN-13 — a tela reapresenta a última permissão informada
    Dado que já informei uma permissão nesta sessão
    Quando abro a tela C066T de novo
    Então os campos da permissão já estão preenchidos
    E a lista dos itens calculados é remontada a partir dela

  Cenário: RN-13 — sem permissão informada na sessão
    Dado que ainda não informei nenhuma permissão nesta sessão
    Quando abro a tela C066T
    Então os campos estão em branco
    E a lista está vazia

  Cenário: RN-13 — a tela é aberta pela C065T
    Dado que a tela C065T passou para esta ao terminar
    Quando a tela C066T se apresenta
    Então os códigos de item chegam limpos
    E a lista dos itens calculados é remontada para a permissão informada

  Cenário: RN-08 — operação desconhecida
    Quando informo no campo da opção um valor que não é código de operação conhecido
    Então vejo "* Operacao nao disponivel *"
    E a transação não segue

  Cenário: RN-08 — inclusão, exclusão ou consulta
    Quando informo no campo da opção um código de inclusão, de exclusão ou de consulta
    Então vejo "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: RN-14 — sem perfil de acesso à tela
    Dado que a minha matrícula não tem perfil de acesso a esta tela
    Quando confirmo o lançamento
    Então vejo "* Acesso negado para esta matricula *"
    E nada é lido e nada é gravado

  Cenário: RN-14 — sem permissão para alterar
    Dado que o meu perfil de acesso tem esta tela, mas não permite alterar
    Quando confirmo o lançamento
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-14 — tela indisponível para o meu perfil ou para o meu órgão
    Dado que esta tela não está registrada ou não está disponível para o meu perfil
    Quando confirmo o lançamento
    Então vejo "* Tela nao disponivel *"
    E nada é lido e nada é gravado

  Cenário: RN-15 — a tela chega com um próximo destino marcado
    Dado que outra tela chama esta dentro da mesma transação, deixando um próximo destino marcado
    Quando a transação chega a esta tela
    Então nenhuma das conferências de cadastro desta tela é feita
    E nada é gravado
    E o controle volta para a tela marcada como próximo destino
```
