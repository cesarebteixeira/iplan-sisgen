# US — C658T — Manter as quantidades e os valores dos itens da permissão auxiliar da CRE

## Estória

Como **servidor de CRE que responde pela permissão auxiliar de compras**, quero
**consultar a permissão de um tipo de contrato e ajustar as quantidades e os valores
das suas linhas de item**, para que **o que a CRE pode empenhar e comprar, item a item,
fique com a quantidade e o valor certos — sem que os dados da própria permissão sejam
mexidos**.

A permissão auxiliar é o que amarra uma coordenadoria regional escolar a um tipo de
contrato, a um fornecedor, a um grupo de licitação e a uma data limite; as linhas de
item dizem, item a item, quanto e por quanto. É esse detalhe que a compra e o empenho
leem depois. Sem esta tela o detalhe fica do jeito que foi criado — e o detalhe errado
não falha: ele compra errado, calado.

## Contexto

Jornada S000M → C000M → C050M → C658T.
Ator: servidor de CRE — consulta a permissão auxiliar da sua coordenadoria e ajusta as
quantidades e os valores dos itens dela.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — a opção 5
do `C000M` abre o `C050M`, e a opção 14 dele abre esta tela — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio.

As duas telas do caminho são **menus**: nenhuma delas deixa registro ou operação para
esta tela, e aqui não há encadeamento de tela em tela. O que esta tela usa do que veio
antes é o **vínculo da matrícula com a secretaria**, que fixa o tipo de órgão, o acesso
e a CRE da sessão; essa é regra da entrada e está no anexo de evidências, em **Regras
que se revelaram da entrada**.

Quem **cria** a permissão auxiliar é outra tela do mesmo menu; esta só acerta o que já
está cadastrado. A jornada termina aqui: esta tela não encaminha para nenhuma outra.

## Regras de negócio

### RN-01 — O que a tela mantém: a permissão auxiliar da CRE e as suas linhas de item

A tela trabalha sobre uma **permissão auxiliar**: o registro que amarra uma
**coordenadoria regional escolar** (a CRE, "CORD.REG.ESCOLAR" no rótulo da tela) a um
**tipo de contrato**, a um **fornecedor**, a um **grupo de licitação** e a uma **data
limite**. Junto com esses cinco identificadores, a permissão traz os dados que a tela
apenas mostra: o tipo de licitação e a sua descrição, o operador responsável e o seu
nome, o valor homologado, o valor adjudicado, as datas da tabela (início e limite) e o
período de início e limite.

O que a tela **grava** são as **linhas de item** dessa permissão: cada linha é
identificada pela subclasse e pelo gênero do item e carrega duas faixas de quantidade e
valor. Todos os outros dados da permissão são só mostrados — esta tela não os altera.

**A tela não cria nada**: não inclui permissão nem linha de item. Quem cadastra a
permissão auxiliar é outra tela do menu.

### RN-02 — A tela abre em consulta e só reconhece consultar, alterar e excluir

São três as operações: **consultar**, **alterar** e **excluir**. Quando a operação
chega em branco — é assim que ela chega quando a tela é aberta pelo menu —, a tela
assume **consulta**. Qualquer operação que não seja uma das três é recusada com
**\* Opcao nao disponivel. Use ALT, DEL ou CON \***, com o cursor de volta no campo da
opção, e nada é gravado.

**Incluir não existe nesta tela** — não há caminho que crie uma permissão nem uma linha
de item —, e a recusa não distingue incluir de qualquer outra opção fora das três.

[?] A recusa manda usar ALT, DEL e CON, mas a tela — e a rota do sistema, que roda
antes — comparam outros códigos de operação: das três, só DEL coincide. Ou o terminal
traduz o que o servidor digita antes de a tela ver, ou as duas conferências estão
desalinhadas da mensagem — e, nesse caso, ALT e CON seriam recusadas. É a mesma dúvida
já registrada nas outras telas desta jornada. Pergunta ao site.

[?] Há um caminho no texto que assume a **inclusão** quando a operação chega em branco,
mas ele fica depois do trecho que já trocou o branco por **consulta**, e a inclusão é
recusada logo adiante. Ou o tratamento do branco está no lugar errado, ou aquele
caminho é inalcançável. Pergunta ao site.

### RN-03 — A alteração e a exclusão exigem que a permissão tenha sido consultada antes

**Alterar** e **excluir** só passam se a permissão já estiver carregada na sessão: o
ano, o mês e o dia da **data limite**, a **CRE**, o **fornecedor**, o **tipo de
contrato** e o **grupo de licitação** informados têm de ser exatamente os da permissão
carregada. Divergindo qualquer um deles, a operação é recusada com **\* Consulte antes
de atualziar \*** (a grafia é a do sistema), com o cursor de volta no campo da opção, e
nada é gravado.

O período de início, os dois valores do cabeçalho, o tipo de licitação e o operador não
entram nessa conferência: eles são do cadastro, e a tela os repõe.

### RN-04 — O grupo informado tem de ser o grupo da sessão

A tela confere a CRE informada contra o **grupo guardado na área de trabalho da
sessão**. Quando a sessão não tem grupo nenhum, essa conferência não se aplica; quando
tem, a CRE informada tem de ser igual à guardada. Divergindo, a recusa é **\* Usuario
sem acesso a este grupo \***, com o cursor de volta no campo da CRE, e nada é lido nem
gravado.

[?] A área que esta tela consulta não é a mesma de que o resto da jornada tira o grupo
da sessão: os dois menus do caminho leem o grupo de uma área e esta tela compara com
outra, que nenhuma tela desta jornada preenche. Se aquela área estiver vazia, a
conferência recusa qualquer grupo diferente de zero para quem tem grupo no vínculo — e
a tela fica sem uso para esse servidor; a tela irmã, aberta pela opção seguinte do mesmo
menu, faz a mesma conferência contra a área que a jornada usa. Pergunta ao site.

### RN-05 — A consulta de uma permissão não cadastrada é recusada

Quando a consulta é de uma combinação **diferente** da que está carregada, a tela
procura a permissão; não existindo, a recusa é **\* Permissao nao cadastrada \***, com
o cursor de volta no campo da CRE, e nada é mostrado. Existindo, o início do período, o
valor homologado, o valor adjudicado, o tipo de licitação, a descrição do tipo de
licitação, o operador e a razão social do fornecedor passam a ser os do cadastro — o que
tiver sido digitado nesses campos é substituído.

Consultar de novo a mesma combinação já carregada não volta ao cadastro: apenas
reapresenta o que está na sessão.

### RN-06 — A permissão carregada sem registro no arquivo auxiliar é avisada

Quando a combinação que está na sessão não corresponde a nenhuma permissão registrada no
arquivo auxiliar, a tela avisa **\* Permissao sem registros no arquivo auxiliar \*** e
encerra o passo sem gravar. É esse o aviso que sai na **abertura** da tela, quando ainda
não há nada carregado, e ele é decidido na montagem da primeira linha, não se repetindo
nas outras.

[?] Na abertura a combinação está em branco, a procura não encontra registro e o aviso
aparece já na primeira exibição. Se a intenção era avisar só depois de o servidor
informar uma combinação, o aviso está adiantado. Pergunta ao site.

### RN-07 — A quantidade de incremento não pode passar do total

Na **alteração**, e só nas linhas que trazem uma **subclasse** informada, a tela confere
as duas quantidades da linha contra as que estão gravadas:

- aumentando a **quantidade de incremento** acima da total, a recusa é
  **\* Qt.Incremento > Qt.Total \***, com o cursor no campo dessa quantidade;
- reduzindo a **quantidade total** abaixo do incremento que já estava gravado — sem ter
  mexido no incremento —, a recusa é **\* Qt.Total < Qt.Incremento \***, com o cursor no
  campo da quantidade total.

Cada uma das duas conferências é dispensada quando a quantidade informada é igual à que
já está gravada naquela coluna. A linha sem subclasse informada não passa por nenhuma
delas. Em qualquer das duas recusas, nada é gravado.

### RN-08 — O valor gravado é recalculado a partir da quantidade

A alteração **não grava o valor que o servidor digita**: a tela recalcula o valor de
cada faixa a partir do valor unitário que já está no registro — o valor inicial dividido
pela quantidade inicial gravada — multiplicado pela quantidade informada. Se a
quantidade inicial gravada estiver zerada, a divisão não se completa e os dois valores
saem zerados.

[?] Os dois campos de valor são apresentados e validados como se fossem digitáveis, e o
que o servidor digita neles nunca é usado. Ou as colunas de valor são de leitura, ou a
tela ignora o que foi informado. Pergunta ao site.

### RN-09 — A alteração só grava a linha que mudou, e não grava quando nada mudou

Na alteração, cada linha é comparada com a que está gravada: **quando as duas
quantidades continuam iguais, nada é gravado e nada vai para a trilha**. Só as linhas em
que a quantidade mudou são gravadas — uma a uma, com a sua passagem pela trilha —, e a
linha sem subclasse informada é ignorada.

Informando a subclasse e o gênero de um item que a permissão não tem, nada é gravado e
nenhuma mensagem é mostrada: a tela não cria item.

### RN-10 — A exclusão não apaga: zera a quantidade total e o valor

A exclusão **não apaga registro nenhum**: ela grava a mesma permissão com a **quantidade
total** e o **valor correspondente zerados**, deixando a faixa do incremento como está.
É a retirada do segundo período, não a remoção da linha. Não há linha a informar — a
exclusão vale para a permissão inteira —, cada item tratado é travado, gravado e
registrado na trilha, e a tela volta sozinha para a consulta.

[?] A varredura da exclusão zera a faixa total em **todos** os registros que alcança, e
não só na linha que estava na tela — a alteração, ao contrário, confere se o registro é
a linha da vez. Onde essa varredura começa e onde termina não se decide pelo texto.
Pergunta ao site.

### RN-11 — A consulta não grava nada

Em **consulta** a tela apenas lê — a permissão auxiliar, o cadastro dos gêneros (para a
descrição da linha), o do fornecedor, o do operador, o do tipo de licitação e o do tipo
de órgão — e mostra o que encontrou: não grava, não apaga, não trava registro e não
deixa rastro na trilha de auditoria.

### RN-12 — Quem grava deixa trilha, e a trilha é gravada antes

A alteração e a exclusão deixam registro na **trilha de auditoria (A010T)**: a tela de
origem, o cadastro auditado, a operação, a CRE, a matrícula funcional, a estação, o tipo
de órgão, a sessão (dia, mês, ano e hora) e as imagens **anterior** e **posterior** do
registro. A trilha é gravada **antes** do cadastro da permissão.

[?] As duas imagens da trilha só saem certas na exclusão — a anterior com os valores
gravados e a posterior zerada. Na alteração, a imagem chamada de **anterior** já leva as
quantidades e os valores novos, porque a tela a monta depois de recalcular: a trilha da
alteração guarda duas vezes o estado posterior. Se a intenção era registrar o que mudou,
o caminho não registra. Pergunta ao site.

[?] A exclusão registra na trilha a operação como **alteração**, e não como exclusão.
Pergunta ao site.

### RN-13 — Os campos passam pela edição de número

Vinte e seis campos da tela passam pela edição de número — os do cabeçalho (a CRE, o
tipo de contrato, o fornecedor, o grupo de licitação, as três partes da data de início,
as três da data limite, o valor homologado, o valor adjudicado, as seis partes das duas
datas-base, o tipo de licitação e o operador) e os da linha de item (a subclasse, o
gênero, as duas quantidades e os dois valores): o que estiver em branco vira zero e o
que não for número é recusado **antes de qualquer consulta ao cadastro**. Quando a
recusa é de um campo, o cursor volta para ele: a tela tem **dez** posições de retorno
mapeadas, que cobrem nove campos — a CRE, o tipo de contrato, o código do fornecedor
(em duas situações), o grupo de licitação, o dia, o mês e o ano do limite e as duas
quantidades da linha. Nos outros campos recusados, o cursor fica onde estava.

[?] O que o servidor vê quando a digitação é recusada — o texto da mensagem — não está
nos fontes desta jornada: a edição de número aponta para uma mensagem numerada do
sistema, e a tabela dessas mensagens não faz parte do acervo lido. Pergunta ao site.

### RN-14 — A tela enxerga oito cadastros e grava em dois; não apaga nenhum

A tela declara, para os **oito** cadastros que enxerga, as rotinas de incluir, de apagar
e de travar — declaração, não uso. Desses oito, **dois recebem gravação**: o cadastro
das permissões auxiliares e a trilha de auditoria. Os outros seis são só de leitura — o
cadastro de telas por perfil, o de órgãos, o de tipos de licitação, o de operadores, o
de fornecedores e o de gêneros. E a tela **não apaga**: nenhuma das oito rotinas de
apagar é executada, nem na exclusão.

### RN-15 — A tela só abre para a sessão e para o perfil autorizados

Antes de mostrar qualquer coisa, a tela confere a sessão:

- a **estação** tem de ser a da matrícula; divergindo, a sessão é encerrada e desviada
  para a saída do sistema;
- a requisição não pode ser de **segunda página**: **\* Acesso a pagina 2 negado \***;
- a **tela** tem de estar cadastrada para o perfil do servidor:
  **\* Tela nao disponivel \***;
- o **código de acesso** do servidor tem de ter a tela:
  **\* Acesso negado para esta matricula \***.

Em qualquer recusa, a tela não é exibida e nada é gravado.

### RN-16 — A tela e a operação têm de estar liberadas para a sessão

Antes das conferências da permissão, o sistema passa a operação informada pela **rota** e
pela **permissão da operação**: a tela tem de estar cadastrada e ativa — uma tela
marcada como excluída no cadastro é tratada como não cadastrada, **\* Tela nao
cadastrada \*** —, a operação tem de ser uma das previstas — **\* Operacao nao
disponivel \*** — e o código de acesso tem de liberá-la — para **alterar**, para
**excluir** e para a manutenção em geral —, sob pena de **\* Acesso negado para esta
operacao \***. Recusado o acesso, nada é lido e nada é gravado.

[?] O cadastro de acesso guarda, por tela, a marca de **consulta** liberada, mas nenhuma
conferência a lê: **consultar passa sem nenhum teste de permissão**. Se a intenção era
exigir uma autorização própria para consultar, o caminho não a exige. Pergunta ao site.

### RN-17 — O campo da próxima tela desvia a sessão e a tela não processa nada

Se o campo da **próxima tela** chegar preenchido, a sessão é levada para a tela
informada e esta tela não confere nada nem grava nada. É o mesmo campo que as telas do
sistema usam para encadear uma na outra sem passar por menu.

[?] Nenhum programa do acervo preenche esse campo por esta tela: ele é lido da máscara e
republicado, e não há quem o informe. Ou quem o preenche está fora do acervo, ou o
desvio nunca acontece por aqui. Pergunta ao site.

### RN-18 — Cada permissão tem até oito linhas de item

A permissão tem **até oito linhas de item**; cada linha traz a subclasse, o gênero, a
descrição do gênero, as duas quantidades e os dois valores. A **classe** do item entra na
chave do cadastro, mas não é mostrada nem se digita aqui: o que identifica a linha é a
subclasse com o gênero. Quando o gênero não tem descrição para a data de início do
período — inclusive quando está marcado como excluído no cadastro —, a tela mostra
**\*\*\*\*** no lugar dela. É a consulta que carrega a permissão e as suas linhas para a
sessão.

[?] A leitura que monta as oito linhas é posicional: o texto não deixa explícito em que
registro ela começa nem para onde anda a cada linha, e não se decide, por ele, se a
ordem exibida é a ordem em que as linhas foram gravadas — nem se reenviar a mesma
consulta continua a lista de onde parou ou recomeça do primeiro item. A grade é fixa em
oito linhas, e o acervo não traz a máscara que diria ao servidor como ver os itens
seguintes de uma permissão maior. Pergunta ao site.

### RN-19 — Falha no banco interrompe a operação

Toda leitura e toda gravação desta tela testa o retorno do banco. O "registro não
encontrado" é tratado como ausência e vira a recusa correspondente; qualquer outro erro
é levado à rotina de comunicação do sistema, e a operação para ali — a linha não é
considerada gravada. Os avisos de recusa desta tela saem por essa mesma rotina.

## Cenários BDD

```gherkin
Funcionalidade: Manter as quantidades e os valores dos itens da permissão auxiliar da CRE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C658T

  Cenário: RN-01, RN-05, RN-11 e RN-18 — consultar os itens de uma permissão auxiliar
    Dado que existe permissão auxiliar da minha coordenadoria regional, para o tipo de contrato, a data limite, o fornecedor e o grupo de licitação que informei
    E ela tem itens cadastrados
    Quando confirmo a consulta
    Então vejo, em cada uma das oito linhas, a subclasse, o gênero, a descrição do gênero, a quantidade de incremento, o valor do incremento, a quantidade total e o valor total
    E vejo o início do período, o valor homologado, o valor adjudicado, o tipo de licitação e a razão social do fornecedor vindos do cadastro
    E nada é gravado e nenhuma trilha é deixada

  Cenário: RN-11 — a consulta não grava nada
    Dado que consultei uma permissão cadastrada
    Quando confirmo a consulta quantas vezes quiser
    Então a tela apenas mostra a permissão e as suas linhas
    E nada é gravado, nenhum registro é travado e nenhuma trilha é deixada

  Cenário: RN-18 — a descrição do gênero não é encontrada
    Dado que o gênero de um item não está cadastrado para a data de início do período, ou está marcado como excluído
    Quando confirmo a consulta
    Então a linha daquele item fica com o marcador no lugar da descrição do gênero
    E os demais dados da linha são mostrados normalmente

  Cenário: RN-02 — a tela abre em consulta
    Dado que chego à tela C658T pela opção 14 do menu C050M
    Quando a tela é exibida
    Então ela está em consulta

  Cenário: RN-02 — opção de manutenção não disponível
    Dado que estou na tela C658T
    Quando informo uma opção que não é consultar, alterar nem excluir
    Então vejo "* Opcao nao disponivel. Use ALT, DEL ou CON *"
    E o cursor volta para o campo da opção
    E nada é gravado

  Cenário: RN-02 — não existe inclusão nesta tela
    Dado que estou na tela C658T
    Quando tento incluir uma permissão ou uma linha de item
    Então a operação é recusada
    E nada é gravado

  Cenário: RN-15 — sessão sem a tela liberada
    Dado que a minha matrícula não tem esta tela pelo código de acesso, ou a tela não está cadastrada para o meu perfil
    Quando tento abrir a tela C658T
    Então vejo a recusa correspondente
    E a tela não é exibida e nada é gravado

  Cenário: RN-16 — operação não liberada
    Dado que o meu código de acesso não libera esta operação nesta tela
    Quando confirmo a operação
    Então vejo "* Acesso negado para esta operacao *"
    E nada é lido e nada é gravado

  Cenário: RN-04 — grupo diferente do grupo da sessão
    Dado que a minha sessão tem um grupo
    E o grupo que informo não é o da sessão
    Quando confirmo a operação
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor volta para o campo da CRE
    E nada é lido nem gravado

  Cenário: RN-05 — consulta de permissão não cadastrada
    Dado que não há permissão para a combinação que vou informar
    Quando consulto
    Então vejo "* Permissao nao cadastrada *"
    E o cursor volta para o campo da CRE
    E nada é mostrado

  Cenário: RN-06 — a combinação carregada não tem registro no arquivo auxiliar
    Dado que a combinação que está na sessão não corresponde a nenhuma permissão registrada
    Quando a tela exibe esse estado
    Então vejo "* Permissao sem registros no arquivo auxiliar *"
    E nenhuma linha é preenchida
    E nada é gravado

  Cenário: RN-06 — a tela é aberta sem consulta anterior na sessão
    Dado que ainda não consultei nenhuma permissão nesta sessão
    Quando abro a tela C658T
    Então vejo "* Permissao sem registros no arquivo auxiliar *"
    E nenhuma linha da grade é preenchida

  Cenário: RN-03 — alterar sem consultar antes, ou mudando os dados do cabeçalho
    Dado que a minha última consulta foi de outra permissão, ou que mudei a CRE, o contrato, a data limite, o fornecedor ou o grupo de licitação
    Quando informo a alteração e confirmo
    Então vejo "* Consulte antes de atualziar *"
    E o cursor volta para o campo da opção
    E nada é gravado

  Cenário: RN-03 — excluir sem consultar antes, ou mudando os dados do cabeçalho
    Dado que a minha última consulta foi de outra permissão, ou que mudei um dos dados que identificam a permissão
    Quando informo a exclusão e confirmo
    Então vejo "* Consulte antes de atualziar *"
    E nada é gravado

  Cenário: RN-07, RN-08, RN-09 e RN-12 — alterar o incremento e o total de um item
    Dado que consultei a permissão auxiliar e o item está na grade
    Quando preencho a linha com a subclasse e o gênero daquele item, informo a quantidade de incremento e a quantidade total e confirmo a alteração
    Então o item fica gravado com as duas quantidades informadas
    E o valor do incremento e o valor total são recalculados a partir do valor unitário do item
    E os outros itens da permissão não mudam
    E a operação fica registrada na trilha, antes do cadastro da permissão

  Cenário: RN-08 — o item não tem quantidade inicial gravada
    Dado que a quantidade inicial do item, no cadastro, está zerada
    Quando confirmo a alteração com as quantidades informadas
    Então as duas quantidades ficam gravadas
    E o valor do incremento e o valor total ficam zerados

  Cenário: RN-09 — o item informado não existe na permissão
    Dado que consultei a permissão auxiliar
    Quando informo a subclasse e o gênero de um item que ela não tem e confirmo a alteração
    Então nada é gravado
    E nenhuma mensagem é mostrada

  Cenário: RN-09 — as quantidades informadas são as que já estão gravadas
    Dado que consultei a permissão e o item está na grade
    Quando confirmo a alteração sem mudar nenhuma das duas quantidades
    Então nada é gravado
    E nenhuma trilha é deixada

  Cenário: RN-07 — o incremento maior que o total
    Dado que consultei a permissão e o item está na grade
    Quando informo uma quantidade de incremento maior que a quantidade total e confirmo a alteração
    Então vejo "* Qt.Incremento > Qt.Total *"
    E o cursor fica no campo da quantidade de incremento
    E nada é gravado

  Cenário: RN-07 — o total menor que o incremento que não mudou
    Dado que consultei a permissão, o item está na grade e a quantidade de incremento é a que já está gravada
    Quando abaixo a quantidade total para menos que o incremento e confirmo
    Então vejo "* Qt.Total < Qt.Incremento *"
    E o cursor fica no campo da quantidade total
    E nada é gravado

  Cenário: RN-10 e RN-12 — excluir a permissão auxiliar
    Dado que consultei a permissão auxiliar e ela tem itens cadastrados
    Quando informo a exclusão e confirmo
    Então a quantidade total e o valor total de cada item ficam zerados
    E a quantidade e o valor do incremento de cada item permanecem como estavam
    E cada item tratado fica registrado na trilha como alteração
    E a tela volta para a consulta

  Cenário: RN-10 e RN-14 — a exclusão não apaga registro
    Dado que excluí uma permissão
    Quando o sistema processa a operação
    Então nenhum registro é apagado do cadastro das permissões auxiliares
    E a permissão continua consultável, com a faixa do total zerada

  Cenário: RN-13 — campo não numérico
    Dado que estou na tela C658T
    Quando informo uma letra na CRE, no tipo de contrato, no fornecedor, no grupo de licitação, em uma das datas ou em uma das quantidades da linha
    Então a tela recusa o campo antes de qualquer consulta ao cadastro
    E o cursor volta ao campo, quando a tela tem a posição dele mapeada
    E nada é lido e nada é gravado

  Cenário: RN-17 — próxima tela preenchida
    Dado que o campo da próxima tela chega preenchido
    Quando confirmo
    Então a sessão é levada para a tela informada
    E esta tela não confere nem grava nada

  Cenário: RN-19 — falha no banco durante a gravação
    Dado que a gravação de um item falha no banco
    Quando confirmo a alteração
    Então a transação é interrompida com o tratamento de erro do sistema
    E o item não é considerado gravado
```
