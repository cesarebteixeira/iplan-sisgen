# US — C240C — Consultar gêneros do grupo de licitação

## Estória

Como **servidor de CRE que responde pela classificação de licitação da secretaria**, quero
**consultar os gêneros que compõem um grupo de licitação e abrir, da linha que eu marcar, a ficha
do gênero em consulta**, para que **eu saiba o que está classificado naquele grupo e chegue ao
gênero certo sem ter de digitar a classe, a subclasse e o gênero**.

O grupo de licitação é a classificação que agrupa os itens comprados: cada item aponta para um
gênero, e cada gênero pertence a um grupo. Quem confere a classificação não decora código de
subclasse e de gênero — sem uma relação do que está dentro do grupo, a única saída seria abrir a
manutenção dos gêneros e tentar combinações até acertar. Esta tela é o índice do grupo, e não grava
nada: quem inclui, altera e exclui gênero é a tela que ela abre.

## Contexto

Jornada S000M → C000M → C055M → C240C.

Ator: servidor de CRE — vê quais gêneros compõem um grupo de licitação e escolhe um deles para
abrir a ficha em consulta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — a opção 6 do `C000M`
abre o menu `C055M`, e a opção 4 dele abre esta tela — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de negócio. O
`C000M` e o `C055M` são **menus**: só encaminham, não gravam nada e não deixam grupamento escolhido
nem operação para esta tela.

Do contexto da sessão, esta tela usa a **matrícula**, o **código de acesso**, o **privilégio**, o
**tipo de órgão**, a **coordenação regional escolar** e a **estação**, que entrega às conferências de
acesso, e exibe a **data do sistema** e a **descrição do tipo de órgão**. Essa carga é regra da
entrada e está no anexo, em **Regras que se revelaram da entrada**.

Esta tela encadeia: marcada uma linha, ela passa o **gênero escolhido** e a **operação de consulta**
para a tela de manutenção dos gêneros (`C050T`), que abre em consulta sobre ele (RN-14). É essa
passagem que dá sentido à tela: a relação de gêneros é o índice, a ficha do gênero é o conteúdo. A
jornada termina aqui.

## Regras de negócio

### RN-01 — A tela consulta os gêneros de um grupo de licitação, e não grava nada

Esta é uma tela de **consulta**. Ela mostra, para um **grupo de licitação** — o grupamento —, os
**gêneros** que o compõem. De cada gênero, a linha traz o **código da subclasse de classificação**,
o **código do gênero**, a **descrição resumida do gênero**, a **unidade de medida** do gênero e a
**data de início da vigência** daquela versão, mais uma coluna para marcar a linha (RN-10). No alto
a tela mostra o **código do grupo** e a **descrição dele**, a **descrição do tipo de órgão** da
sessão, a **data do sistema** e a linha de mensagem.

Nada aqui é gravado: não há inclusão, alteração nem exclusão, nenhum registro é travado e nenhuma
linha de auditoria é gerada. A tela confere ainda, ao se apresentar, se ela própria está cadastrada
no **cadastro de telas** — é de lá que vem o título que ela mostra.

O grupo de licitação que esta tela consulta é o do cadastro dos grupamentos de classificação de
licitação, que a tela `C240T` mantém: cada versão do grupo tem um código e uma descrição com data de
vigência. O grupamento que esta tela mostra ao lado do código é a descrição da versão que a leitura
alcança.

[?] Qual versão do grupamento a tela alcança para mostrar a descrição — a mais recente ou a mais
antiga — não se decide pelo material lido (ver RN-03). Pergunta ao site.

### RN-02 — Como a tela se apresenta: ela repõe a consulta e retoma o grupamento guardado

Quando a tela é aberta, ela se apresenta com a **operação de consulta** já preenchida e sem
grupamento. Se a **área de trabalho que a sessão guarda entre as telas** já traz uma operação e um
grupamento, a tela **retoma os dois** — e com eles a descrição do grupamento —, e é dali que a
relação é montada. É essa mesma área que a tela regrava ao terminar cada passagem, de modo que é ela
que carrega o grupo e o ponto de parada da relação de uma exibição para a outra.

[?] A montagem da relação só começa quando a área de trabalho já traz uma operação guardada, e quem
a grava é a própria tela na passagem em que a área chega em branco: nessa passagem ela se limita a
fixar a consulta e a encerrar a montagem, com o indicador de fim de lista ainda em branco. Ou a
primeira exibição sai sem nenhuma linha e a relação aparece na passagem seguinte, ou o ambiente
reapresenta a tela sem intervenção do servidor. O acervo não define a vida da área de trabalho
comum, e os dois menus do caminho não escrevem nela. Pergunta ao site.

### RN-03 — O grupo de licitação tem de estar cadastrado, e a tela mostra a descrição dele

O **grupo informado tem de existir** no cadastro dos grupamentos de classificação de licitação. Não
existindo — inclusive quando o campo chega em branco, porque a tela procura o código zero —, a tela
recusa com **\* Grupamento nao cadastrado \***, devolve o cursor ao campo do grupo e não lê gênero
nenhum. Existindo, a tela passa a mostrar a **descrição daquele grupamento** ao lado do código.

A conferência é dispensada quando o código do grupo não foi trocado desde a exibição anterior: nesse
caso a tela segue direto para a linha marcada.

[?] A leitura que procura o grupamento se posiciona pela maior data de vigência possível, e o efeito
exato desse posicionamento não está no acervo nem no manual: o texto não traz o verbo de
posicionamento do dialeto por trás da leitura. Se ela devolve a versão mais recente do grupo, a
descrição mostrada é a da versão que vale hoje; se devolve outra, a descrição pode ser a de uma
versão antiga — e, no limite, o grupo pode ser dado como não cadastrado. Pergunta ao site.

### RN-04 — Cada gênero aparece uma vez, e só o ativo; a página tem doze linhas

A relação é montada no **cadastro dos gêneros**, no recorte do grupo informado, e **percorre o
cadastro na ordem do próprio cadastro**: grupo, subclasse, gênero e data de início da vigência. Cada
gênero — cada par de subclasse e gênero — aparece em **uma única linha**, na versão que a leitura
alcança primeiro; as demais versões do mesmo gênero são **saltadas em silêncio**, e a leitura segue.
O gênero que **não estiver marcado como ativo** também é saltado, sem aviso, e a leitura segue para
o próximo.

A página tem **doze linhas**. Quando a relação termina antes de a página encher, as linhas que
sobram ficam em branco. A tela regrava na área de trabalho o ponto em que a relação parou: quando a
página enche, o ponto fica na última linha mostrada; quando a relação termina, o ponto volta a zero.

A capacidade declarada do cadastro dos gêneros é de **150 mil** registros — capacidade é o máximo
esperado, um parâmetro de dimensionamento, não o que está cadastrado.

[?] A direção da leitura não se decide pelo material lido: o índice que a tela usa declara a data de
início da vigência em ordem **decrescente**, mas o texto da tela não traz o verbo de posicionamento
do dialeto, só os parâmetros de chave de cada leitura. Por isso não se sabe se a linha de cada
gênero mostra a **vigência mais recente** ou a **mais antiga**, nem se a relação começa no primeiro
ou no último gênero do grupo. É o mesmo defeito de leitura já registrado na `C050T` e na `C240T`.
Pergunta ao site.

### RN-05 — As colunas de código passam pela conferência de número antes de qualquer leitura

O **código do grupo** e os **códigos de subclasse e de gênero** da linha em conferência passam por
uma **conferência de número antes de qualquer leitura** do cadastro: o que não for número é recusado
no próprio campo e a leitura não segue. Campo em branco é tratado como zero — é por isso que o grupo
em branco é procurado como código zero (RN-03).

[?] O texto que o servidor lê quando um valor não numérico é recusado não está no acervo: a
conferência é chamada de uma rotina de biblioteca cujo corpo não veio no lote, e ela recebe apenas o
rótulo do campo. A volta do cursor só está declarada para o **campo do grupo**; para as colunas de
subclasse e de gênero a tela marca o erro sem dizer onde o cursor volta. Pergunta ao site.

### RN-06 — A tela apaga o resultado da consulta anterior antes de conferir

A cada envio, **antes** de qualquer conferência, a tela apaga a **descrição do tipo de órgão**, a
**data do sistema**, a **descrição do grupamento**, a **descrição resumida do gênero** e a **data de
vigência** que havia mostrado. Uma consulta recusada, portanto, não deixa o resultado da consulta
anterior na tela.

[?] Os dois campos do cabeçalho — a descrição do tipo de órgão e a data do sistema — só são
preenchidos na **primeira** apresentação da tela: quem os preenche é o caminho que monta a página, e
ele não roda de novo a cada envio. Se o ambiente não repuser o cabeçalho por conta própria — e o
acervo lido não mostra quem o faria —, os dois aparecem em branco depois do primeiro envio.
Pergunta ao site.

### RN-07 — Sem gênero ativo, a tela avisa que não existem gêneros para o grupamento

Quando o grupo existe e **nenhum gênero ativo** é encontrado para ele, a tela não preenche linha
alguma, limpa o que havia mostrado e avisa **\* Nao existem generos para este grupamento \***. O
aviso é decidido na montagem da **primeira linha** da página e não se repete nas demais.

### RN-08 — A tela só trabalha em consulta

A tela se apresenta repondo a **operação de consulta** no campo da opção. Se a confirmação chegar
com **outra operação**, a tela recusa com **\* Operacao nao disponivel. Use CON \***, devolve o
cursor ao campo da opção e não lê grupo nem gênero. A conferência vale para a **primeira linha** da
página.

[?] A recusa manda usar "CON", mas o sistema reconhece a consulta por um código interno que o acervo
escreve como "INQ"; nenhum valor "CON" existe no corpus lido. Ou o formulário traduz o que o
servidor digita para esse código, ou quem seguir a mensagem é recusado. É a mesma dúvida já
registrada nas telas irmãs. Pergunta ao site.

[?] A recusa só existe se a máscara oferecer ao operador um campo de opção, e é o mesmo campo que a
tela preenche ao se apresentar: se ele não voltar preenchido, a tela não deixa passar consulta
nenhuma. A ficha da tela lista os rótulos dos campos e não diz qual deles é o da operação. Pergunta
ao site.

### RN-09 — O código da próxima tela preenchido abandona a conferência

Se a mensagem chegar com o **código da próxima tela** preenchido, a conferência da consulta é
abandonada — nada de grupo, de linha marcada nem de encaminhamento — e a sessão é encaminhada para a
tela indicada.

[?] O que preenche esse código nesta tela não está no acervo: não se sabe quem manda próxima tela
para a `C240C`. Pergunta ao site.

### RN-10 — Marcada a linha com código, o gênero abre em consulta na tela de manutenção

**Marcada** uma linha da relação em que o **código da subclasse está preenchido**, a tela **não**
segue com uma operação própria: ela passa o **código da subclasse** e o **código do gênero** daquela
linha e a **operação de consulta** para a tela de manutenção dos gêneros, que abre **em consulta**
sobre aquele gênero. A conferência percorre as linhas da página uma a uma; é a linha marcada que
decide o gênero da passagem.

**Marcada** uma linha em que o código da subclasse está **zerado** — a linha vazia da página —, a
tela recusa com **\* Informe consulta para linha preenchida \*** e devolve o cursor à **coluna de
marcação daquela linha**. **Sem nenhuma linha marcada**, a tela apenas segue mostrando a relação,
não abre nada e não grava nada. A conferência olha só o código da subclasse: o código do gênero
pode ir zerado para a tela seguinte.

[?] O rótulo que o servidor vê na coluna de marcação e o valor que ele digita não estão no acervo
lido: o programa reconhece a marcação por a coluna estar **preenchida**, sem conferir o que foi
digitado, e não há literal de marcação no texto. A máscara da tela é carregada em tempo de execução
e não veio no lote. Pergunta ao site.

### RN-11 — A tela confere a sessão, a tela, a rota e a permissão antes de operar

Ao **se apresentar**, a tela chama a conferência de sessão: ela confere a **estação** da sessão
contra a estação do cadastro do servidor e confere se a **tela está cadastrada** no cadastro de
telas e se o **código de acesso** do servidor tem aquela tela autorizada.

Ao **confirmar**, e antes de qualquer leitura, a tela pede a **rota** — que examina o cadastro da
tela e decide se aquela operação é alcançável a partir dali — e a **permissão do código de acesso
para a operação**. Retorno diferente de aprovado em qualquer das duas limpa o status e interrompe a
tela: ela não lê nada. Vindo esta tela do menu, a operação entregue à conferência é a de consulta.

[?] A permissão de **consulta** não é lida em nenhum ponto da conferência por operação: o cadastro
de telas guarda as quatro permissões separadas, e a rotina só compara as de inclusão, alteração e
exclusão. Para a consulta, ela passa sem examinar permissão nenhuma. Ou uma tela de consulta não
exige mesmo permissão de operação, ou a conferência está lendo o ramo errado. A mesma dúvida está
registrada na `C240T`. Pergunta ao site.

### RN-12 — Falha do banco interrompe a leitura e avisa

Toda leitura desta tela testa o erro do banco. Erro que **não** seja "registro não encontrado" vira
a ação de erro de acesso, com a mensagem de erro do sistema, e a operação para ali, sem completar a
relação.

### RN-13 — A tela não grava, não trava e não apaga nada

A tela enxerga **três cadastros**: o cadastro de telas, o cadastro dos gêneros e o cadastro dos
grupamentos. Para cada um deles o programa carrega as rotinas de **gravar**, de **apagar** e de
**travar** registro — é assim que o gerador monta o programa —, mas **nenhuma delas é executada**:
as declarações existem para todo cadastro que a tela enxerga, e a tela não as aciona. As seis
rotinas de gravação e de exclusão e as três de travamento ficam declaradas e sem uso. Não há,
portanto, gravação, travamento nem exclusão por esta tela, e nenhuma linha de auditoria é gerada.

### RN-14 — O que a tela entrega à seguinte, e como a seguinte muda conforme a origem

A tela de manutenção dos gêneros, **aberta a partir daqui**, abre **em consulta sobre o gênero
escolhido**: o que a decide é a **operação de consulta** e os **códigos de subclasse e de gênero**
que esta tela deixa na área de trabalho da sessão, junto com a **marca de que a origem é esta tela**.
Essa marca é lida pela tela seguinte, e é ela que faz a tela seguinte repor a operação e o gênero.

Aberta pela **opção do menu `C055M`**, sem passar por aqui, a mesma tela de manutenção não recebe
gênero escolhido nem esta marca — o menu limpa a área de trabalho que esta tela usa — e por isso não
abre sobre um gênero.

Esta tela, ao contrário, **não muda conforme quem a chamou**: ela não compara a tela de origem com
código nenhum. A operação que ela apresenta vem da área de trabalho da sessão (RN-02), e a única
tela que a chama é o menu `C055M`.

## Cenários BDD

```gherkin
Funcionalidade: Consultar os gêneros de um grupo de licitação e abrir o gênero escolhido em consulta

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C240C

  Cenário: RN-01 — consultar os gêneros de um grupo de licitação
    Dado que o grupo de licitação tem gêneros ativos
    Quando informo o grupo e confirmo
    Então vejo a descrição do grupo, a data do sistema e a descrição do tipo de órgão da minha sessão
    E vejo, em cada linha, o código da subclasse, o código do gênero, a descrição resumida, a unidade de medida e a data de início da vigência

  Cenário: RN-01 e RN-13 — a consulta não deixa rastro
    Dado que abro a tela C240C
    Quando a relação é mostrada
    Então nenhum registro é travado
    E nenhuma linha nova aparece na trilha de auditoria
    E nenhum cadastro recebe gravação por esta tela

  Cenário: RN-02 — a tela abre repondo a consulta
    Dado que abro a tela C240C sem operação guardada na área de trabalho da sessão
    Quando a tela é exibida
    Então a operação que ela mostra é a consulta
    E o campo do grupo vem em branco

  Cenário: RN-02 — a tela retoma o grupamento guardado
    Dado que a área de trabalho da sessão traz a operação de consulta e um grupamento
    Quando abro a tela C240C
    Então o campo do grupo vem preenchido com aquele grupamento
    E vejo a descrição daquele grupamento

  Cenário: RN-03 — grupo de licitação não cadastrado
    Dado que informo um grupo que não existe no cadastro dos grupamentos
    Quando confirmo
    Então vejo a mensagem "* Grupamento nao cadastrado *"
    E o cursor volta ao campo do grupo
    E nenhum gênero é lido

  Cenário: RN-03 — o grupo em branco não passa
    Dado que deixo o campo do grupo em branco
    Quando confirmo
    Então vejo a mensagem "* Grupamento nao cadastrado *"
    E nenhum gênero é lido

  Cenário: RN-03 — a descrição do grupo aparece com o código
    Dado que o grupo informado existe
    Quando confirmo
    Então vejo a descrição daquele grupo ao lado do código

  Cenário: RN-04 — gênero com mais de uma versão aparece uma vez
    Dado que um gênero do grupo tem versões registradas em datas diferentes
    Quando vejo a relação
    Então aquele gênero aparece em uma única linha
    E as demais versões dele não aparecem

  Cenário: RN-04 — gênero inativo não aparece
    Dado que existe um gênero do grupo que não está marcado como ativo
    Quando vejo a relação
    Então esse gênero não aparece
    E os gêneros ativos do grupo continuam sendo mostrados

  Cenário: RN-04 — a página tem doze linhas
    Dado que o grupo tem mais de doze gêneros ativos
    Quando vejo a relação
    Então a página mostra no máximo doze linhas
    E as linhas que sobram ficam em branco quando a relação termina antes de a página encher

  Cenário: RN-05 — digitação não numérica
    Dado que digito algo que não é número no campo do grupo ou nos códigos de uma linha
    Quando envio a consulta
    Então a consulta não segue
    E nenhum gênero é lido do cadastro

  Cenário: RN-06 — o resultado da consulta anterior não fica na tela
    Dado que a tela mostrou o grupo, a descrição dele e as linhas da relação
    Quando reenvio a consulta
    Então o que a tela havia mostrado foi apagado antes da conferência

  Cenário: RN-07 — nenhum gênero ativo no grupo
    Dado que o grupo existe e não tem nenhum gênero ativo
    Quando informo o grupo e confirmo
    Então vejo a mensagem "* Nao existem generos para este grupamento *"
    E nenhuma linha é preenchida

  Cenário: RN-08 — operação diferente da consulta
    Dado que estou na tela C240C
    Quando a tela recebe uma operação diferente da consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nenhum grupo e nenhum gênero são lidos

  Cenário: RN-09 — código da próxima tela preenchido
    Dado que a mensagem chega à C240C com o código da próxima tela preenchido
    Quando eu confirmar
    Então o grupo, a linha marcada e o encaminhamento não são conferidos
    E a sessão é encaminhada para a tela indicada

  Cenário: RN-10 — marcar a linha e abrir o gênero em consulta
    Dado que a relação mostra os gêneros ativos do grupo
    E marco a linha de um gênero
    Quando confirmo
    Então a tela de manutenção dos gêneros abre em consulta sobre aquele gênero
    E nada é gravado por esta tela

  Cenário: RN-10 — marcar uma linha sem código
    Dado que marco a coluna de ação de uma linha em que o código da subclasse está em branco
    Quando confirmo
    Então vejo a mensagem "* Informe consulta para linha preenchida *"
    E o cursor volta à coluna de marcação daquela linha
    E nenhuma tela se abre

  Cenário: RN-10 — confirmar sem marcar nenhuma linha
    Dado que a relação mostra os gêneros ativos do grupo
    Quando confirmo sem marcar nenhuma linha
    Então a tela segue mostrando a relação
    E nenhuma tela se abre
    E nada é gravado

  Cenário: RN-11 — sem a tela autorizada no código de acesso
    Dado que o meu código de acesso não tem esta tela autorizada ou a tela não está cadastrada
    Quando abro a tela C240C
    Então a tela não opera
    E nenhum grupo e nenhum gênero são lidos

  Cenário: RN-12 — falha do banco durante a consulta
    Dado que a leitura do cadastro dos gêneros falha no banco
    Quando confirmo a consulta
    Então a operação é interrompida com a mensagem de erro do sistema
    E a relação não é completada

  Cenário: RN-14 — a tela de manutenção aberta a partir desta lista
    Dado que escolho um gênero na relação desta tela
    Quando confirmo
    Então a tela de manutenção dos gêneros abre em consulta sobre aquele gênero
    E ela abre sabendo que veio desta tela

  Cenário: RN-14 — a tela de manutenção aberta pelo menu
    Dado que abro a tela de manutenção dos gêneros pelo menu C055M, sem passar por esta lista
    Quando a tela é exibida
    Então ela não abre sobre um gênero escolhido nesta lista
    E não recebe a marca de origem desta tela
```
