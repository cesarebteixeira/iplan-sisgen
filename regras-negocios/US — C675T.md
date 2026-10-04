# US — C675T — Identificar permissões de contrato por órgão

## Estória

Como **servidor de CRE que responde pelas permissões de contrato da sua
coordenadoria regional escolar**, quero **identificar, órgão por órgão, quais
unidades da minha coordenadoria estão autorizadas a contratar por um tipo de
contrato, dentro de um período, para uma subclasse e um gênero — apontando os
órgãos um a um, trazendo-os de outra permissão ou marcando todos de uma vez**,
para que **a autorização deixe de valer para a coordenadoria inteira e passe a
valer para os órgãos certos, e quem contrata saiba até onde aquela permissão
alcança**.

A permissão de tipo de contrato nasce valendo para a coordenadoria: o registro do
período guarda o tipo de contrato, o período, a subclasse, o gênero e a quantidade
inicial, sem dizer a que unidade aquilo se aplica. É esta tela que faz a passagem
do "vale para o grupo" ao "vale para estes órgãos": cada órgão identificado ganha
o seu próprio registro, e é o conjunto deles que diz o alcance da permissão.
Enquanto a identificação não é feita, a permissão continua valendo para toda a
coordenadoria — e, sem ela, quem contrata não sabe se a sua unidade está coberta.

## Contexto

Jornada S000M → C000M → C050M → C670M → C675T.

Ator: servidor de CRE — consulta uma permissão de tipo de contrato da sua
coordenadoria e identifica, órgão por órgão, quais unidades ela alcança.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e
menus.md`: é **dado de navegação**, não regra de negócio.

Os três passos anteriores da jornada — o `C000M`, o `C050M` e o `C670M` — são
menus e **não gravam nada**: só encaminham. O contexto que a tela usa — o tipo de
órgão, a coordenadoria da sessão, a matrícula, o privilégio e a data do sistema —
é o que a entrada deixou, e a tela não o recalcula. A tela, porém, também é
alcançada pela **passagem** da tela que consulta o período (`C674C`), que a
entrega já consultada; o comportamento da tela muda conforme essa origem, e isso
é regra dela (RN-10). A tela ainda entrega o registro às telas `C674C` e `C675C`,
também sem passar por menu (RN-10).

A autorização da tela e da operação, e as demais conferências de acesso, são
regras da **entrada**: estão no anexo de evidências, na seção **Regras que se
revelaram da entrada**.

## Regras de negócio

### RN-01 — A tela abre em consulta e só aceita consulta e alteração

A tela trabalha com uma operação, e só duas são aceitas: **consulta** e
**alteração**. Quando a operação chega em branco, a tela adota a consulta.
Qualquer outra operação é recusada com
**\* Operacao nao disponivel. Use ALT ou CON \***, com o cursor de volta ao campo
da operação — e a recusa acontece antes de qualquer leitura: nesse caminho nenhuma
permissão é lida nem mostrada.

[?] O texto da recusa manda usar "ALT" ou "CON", mas as operações que a tela
compara são as da tabela do sistema — a de alteração e a de consulta —, e não
essas abreviaturas. Qual valor o operador digita no campo, e se a máscara oferece
esse campo, não está no lote lido. Pergunta ao site.

[?] A operação com que a tela abre pode vir de quem a chamou, pelo registro da
transação: a tela que consulta o período a entrega com a operação de consulta, e o
menu não tem operação de manutenção. Antes desta guarda, a lógica de rota já
recusa as operações que não reconhece, com uma mensagem parecida
(**\* Operacao nao disponivel \***), e ela roda primeiro. Qual das duas mensagens o
operador vê em cada caso, e se a segunda é alcançável, depende de valores do
formulário que não estão no acervo. Pergunta ao site.

### RN-02 — A permissão é do grupo, para um tipo de contrato, e vale por órgão

O cadastro por trás da tela guarda **uma permissão por órgão**: o tipo de órgão, a
coordenadoria (o grupo), a **data limite**, a subclasse, o gênero, o **órgão** e o
**tipo de contrato**. São **13 campos** no registro — entre eles o início do
período, a data limite, o fornecedor, o órgão e o tipo de contrato — e a capacidade
do cadastro é de **100 registros** (capacidade é o máximo esperado, parâmetro de
dimensionamento, não o que está gravado). O **início do período não faz parte da
identidade** da permissão: quem distingue uma permissão da outra é a data limite,
junto com o órgão e o tipo de contrato. Há também um índice que agrupa essas
permissões pelo grupo e pelo órgão.

Enquanto existe o **registro do grupo** — o que **não** aponta para um órgão —, a
permissão vale para a coordenadoria inteira. A identificação (RN-06, RN-07 e RN-08)
é o que substitui esse registro por um registro por órgão.

[?] O que a subclasse e o gênero classificam, e o que a **descrição resumida do
gênero** — que a tela mostra — representa, não está no acervo lido nem no manual.
Pergunta ao site.

[?] O registro do grupo é lido e apagado posicionando a leitura no **órgão zero**,
dentro do grupo e da combinação consultada. Se o que a tela chama de "registro do
grupo" é sempre um único registro, ou se a leitura apenas começa por ali e alcança
outros, depende do efeito exato do posicionamento no dicionário de dados, que o
acervo não descreve. Pergunta ao site.

### RN-03 — O grupo é obrigatório, tem de existir e é o do próprio servidor

O grupo (a coordenadoria) é a chave de entrada da tela. Vindo em branco, a tela
recusa com **\* Informe o grupo \***, com o cursor no campo. Informado, ele é
procurado no cadastro das coordenadorias **dentro do tipo de órgão da sessão**:
não existindo, a recusa é **\* Grupo nao cadastrado \***. E quando a sessão tem uma
coordenadoria, o servidor só identifica **a própria**: informar outra dá
**\* Usuario sem acesso a este grupo \***.

Estas três conferências acontecem na consulta. Em alteração, a tela não as repete:
quem passou por elas foi a consulta anterior, e é a conferência dos dados iguais
(RN-05) que amarra as duas.

[?] Se a sessão não tem coordenadoria (o vínculo do servidor não fixou nenhuma), o
fonte deixa passar qualquer grupo cadastrado. Se essa é a intenção — ou se o
vínculo deveria sempre trazer uma coordenadoria —, o acervo não responde. Pergunta
ao site.

### RN-04 — A consulta é pela combinação do grupo, do tipo de contrato, da data limite, da subclasse e do gênero

Confirmado o grupo, o operador informa o **tipo de contrato**, a **data limite**
(dia, mês e ano), a **subclasse** e o **gênero**; a tela procura a permissão
registrada para essa combinação, dentro do tipo de órgão da sessão. **O início do
período não é procurado: ele vem do registro** — é o que a tela mostra depois de
achar, junto com a **descrição resumida do gênero**, o **código do fornecedor**, a
**razão social** e a **quantidade inicial** (a que a tela rotula como quantidade
de permissão inicial). Não achando a permissão para a combinação, a recusa é
**\* Permissao nao cadastrada para identificacao \***, com o cursor na data limite.

Reenviar os mesmos valores que já estão na tela não provoca nova leitura.

[?] A leitura usa o recurso de posicionamento do dicionário de dados, cujo efeito
exato não está no acervo nem no manual: se ela exige a **data limite exata** de uma
permissão registrada, o operador só consulta quem sabe a data; se apenas
**posiciona** na primeira permissão igual ou posterior, a data informada é o ponto
de partida. O site precisa dizer qual é o esperado.

### RN-05 — A alteração exige que os dados sejam os mesmos da consulta

Em alteração, a tela confere **sete valores** — o grupo, o tipo de contrato, as
três partes da data limite, a subclasse e o gênero — contra os que ela guardou da
consulta. Se algum estiver diferente, a alteração é recusada com
**\* Consulte antes de atualizar \***, com o cursor no campo da operação: primeiro
se consulta, depois se altera.

[?] A conferência **não inclui o início do período**: quando ele é informado e não
bate com o registrado, a tela não recusa — ela o substitui pelo que está no
registro. Se o início do período deveria ser conferido, o caminho não o confere.
Pergunta ao site.

[?] A recusa convive com o caminho que grava: ela acontece num passo que não marca
erro fatal, e a mesma remessa segue para o passo que identifica os órgãos, que
**não repete a conferência**. Ou a recusa deveria interromper a identificação, ou o
caminho de gravação ficou sem guarda. O acervo não traz o corpo da rotina do
sistema que emite as mensagens, e é ela que decidiria. Pergunta ao site.

### RN-06 — A identificação grava a permissão de cada órgão marcado na lista

Cada linha da lista — um órgão — tem um campo de marcação. Em alteração, a linha
marcada para **inclusão** tem a permissão daquele órgão **gravada**: a tela monta o
registro com o grupo, o tipo de contrato, o período, a subclasse, o gênero, o
fornecedor e o órgão da linha, e grava. Linha sem marcação não grava nada; e em
**consulta** nenhuma linha grava.

Depois de gravada a permissão, a tela grava o **rastro de auditoria** da inclusão
(RN-13); se a gravação do rastro aborta, o caminho é abandonado. O órgão incluído
deixa de aparecer na lista, que mostra só os que ainda não estão identificados
(RN-09).

[?] O campo de marcação não é preenchido por nenhum caminho do programa: ele só é
lido da máscara e devolvido a ela. Se a máscara não oferecer esse campo por linha,
a inclusão por linha fica inalcançável. Pergunta ao site.

### RN-07 — A cópia traz os órgãos de outra permissão e apaga o registro do grupo

O operador pode informar os dados de **outra permissão** — a subclasse, o gênero, o
dia, o mês e o ano limite e o tipo de contrato de origem — para trazer de lá os
órgãos já identificados. Nesse caminho, a tela apaga o **registro do grupo** (o que
não aponta para um órgão) da permissão consultada, do mesmo tipo de contrato, e
grava, para **cada órgão identificado na permissão de origem**, a permissão
correspondente na combinação que está na tela. A permissão deixa, então, de valer
para a coordenadoria inteira e passa a valer para os órgãos trazidos.

Se a permissão de origem não tem nenhum órgão identificado para aquele tipo de
contrato, a recusa é **\* Nao existem registros para copia \***, com o cursor no
campo da subclasse de origem, e nada é gravado nem apagado.

[?] A tela apaga o registro do grupo antes de gravar os órgãos trazidos, e o faz
registro a registro; o acervo lido não mostra nenhum tratamento para o meio-caminho
— se a remessa inteira desfaz o que já gravou quando uma das gravações aborta, ou
se a coordenadoria pode ficar sem permissão para todos e com os órgãos pela
metade. Pergunta ao site.

### RN-08 — O flag de total grava a permissão para todos os órgãos do grupo

Há ainda um campo de total. Marcado, a tela percorre os órgãos da coordenadoria e,
para cada órgão que ainda **não** tem a permissão identificada, grava o registro
correspondente, com o rastro de auditoria depois de cada gravação (RN-13). Órgão
que já tem a permissão é pulado. Em consulta, o flag não grava nada.

[?] Como o campo da linha, o flag de total só é lido da máscara e devolvido a ela:
o programa nunca o preenche. Se a máscara não o oferecer, esse caminho de
identificação fica inalcançável. Pergunta ao site.

[?] O cadastro de órgãos marca a situação de cada um, e este caminho só identifica
os que estão com a situação ativa; o acervo lido não define o que a marca
significa, nem o que acontece com a permissão do grupo quando um órgão está
inativo. Pergunta ao site.

### RN-09 — A lista traz até 8 órgãos, só os que ainda não estão identificados

A lista da tela tem **8 linhas**. Para cada linha, a tela caminha pelos órgãos da
coordenadoria, a partir do **órgão inicial** informado, e mostra o primeiro órgão
que **ainda não tem** a permissão identificada — com o código e o nome do órgão.
Órgão que já tem a permissão não aparece: a tela passa para o próximo. Havendo mais
órgãos sem permissão do que linhas, a lista continua a partir do último órgão
mostrado.

Quando a caminhada não encontra nenhum órgão sem permissão — todos os órgãos da
coordenadoria já estão identificados —, a tela avisa
**\* Orgaos ja identificados \*** e limpa o campo do órgão inicial, sem preencher
nenhuma linha.

[?] A continuação da lista depende de uma marca de continuidade que os próprios
caminhos da tela reescrevem, e o efeito exato da leitura posicionada não está no
manual. Se a página seguinte pode repetir ou pular órgãos, o acervo não responde.
Pergunta ao site.

### RN-10 — A tela muda conforme quem a chamou, e entrega o registro às telas seguintes

A tela traz duas marcas de encaminhamento. Marcado o campo que pede a tela do
**período**, a tela entrega o registro à `C674C` — que abre em **consulta** — e o
servidor é levado para lá; marcado o campo que pede a tela de **exclusão**, a
entrega é para a `C675C`, também em consulta.

Quando a permissão **chegou** da consulta do período, a tela reconhece essa origem
pela marca correspondente e **não deixa alterar**: toda remessa devolve o servidor
à `C674C`, em consulta. É por isso que quem chega a esta tela pela consulta do
período não identifica nada — e quem chega pelo menu, sim: sem a marca, a alteração
segue, depois da consulta que a RN-05 exige.

A tela também respeita o campo genérico de "próxima tela" da máscara: informado um
código de tela, o encaminhamento é para ele, e a lógica da própria tela termina
ali.

[?] As duas marcas não são escritas por nenhum caminho desta tela nem das telas que
a chamam: elas chegam pelo registro da transação, e o lote não traz a máscara, que
é carregada em tempo de execução — é a máscara que as poderia trazer. A leitura
também não encontrou, na tela do período, o preenchimento que a estória dela
registra ("a tela seguinte fica sabendo que veio desta"). Enquanto a marca não for
localizada, os dois encaminhamentos e a devolução da alteração podem estar
inalcançáveis. Pergunta ao site.

### RN-11 — A digitação dos vinte campos é editada, e o cursor volta ao campo recusado

**Vinte campos** passam pela edição numérica antes de qualquer leitura: o grupo, o
tipo de contrato, o dia, o mês e o ano do início do período, o dia, o mês e o ano
limite, o fornecedor, a subclasse, o gênero, a quantidade inicial, os seis campos
da permissão de origem (subclasse, gênero, o dia, o mês e o ano limite e o tipo de
contrato), o órgão da linha e o órgão inicial. Campo em branco é tratado como zero,
e o que não for número é recusado, sem chegar a consultar o cadastro. Quando o
campo recusado tem posição na tela — **quatorze dos vinte** —, o cursor volta para
ele; os outros seis a tela apenas recusa.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual —
não está nos fontes desta jornada: a rotina que faz a edição numérica não faz parte
do acervo lido. A tela também não confere faixa: mês fora de 1 a 12 e dia fora do
mês não são recusados aqui. Pergunta ao site.

### RN-12 — A consulta não grava nada

Em consulta, a tela lê e mostra: nenhuma permissão é incluída, alterada ou apagada,
e nenhum rastro de auditoria é gerado. O caminho que grava e o que apaga são
alcançados só **fora** da consulta.

### RN-13 — Toda identificação deixa rastro de auditoria

Antes de apagar, a tela grava um **rastro** no cadastro de auditoria — a tela de
origem, o cadastro auditado (o das permissões), a operação de exclusão, a matrícula
funcional, a estação, a data e a hora da sessão, o valor anterior e o valor
resultante — e só depois apaga. Nas inclusões, a permissão é gravada primeiro e o
rastro da inclusão vem logo depois; em qualquer dos casos, se a gravação do rastro
aborta, o caminho é abandonado antes de a operação valer.

[?] A inclusão só grava o rastro quando a gravação da permissão devolve um
resultado diferente de "DATA"; o acervo lido não diz o que esse resultado
significa, nem em que desfecho o rastro deixa de ser gravado. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Identificar, órgão por órgão, as permissões de tipo de contrato de uma coordenadoria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C675T

  Cenário: A tela abre em consulta
    Dado que abro a tela C675T pelo menu
    Quando a tela é apresentada
    Então o campo da operação mostra a consulta
    E nenhuma permissão foi gravada

  Cenário: Operação diferente de consulta e de alteração
    Quando informo uma operação que não é consulta nem alteração
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo da operação
    E nenhuma permissão é lida ou mostrada

  Cenário: A permissão é identificada órgão por órgão
    Dado que consultei uma permissão que ainda vale para toda a coordenadoria
    Quando identifico três órgãos
    Então cada um dos três órgãos tem a sua própria permissão
    E a permissão deixa de valer para a coordenadoria inteira

  Cenário: O grupo é obrigatório
    Dado que estou consultando
    Quando deixo a coordenadoria em branco
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta para o campo da coordenadoria
    E nenhuma permissão é lida

  Cenário: Coordenadoria de outro servidor
    Dado que a minha sessão tem uma coordenadoria
    Quando informo outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"

  Cenário: Coordenadoria não cadastrada
    Quando informo uma coordenadoria que não existe na minha secretaria
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta para o campo da coordenadoria

  Cenário: Consultar uma permissão cadastrada
    Dado que informo a coordenadoria, o tipo de contrato, a data limite, a subclasse e o gênero de uma permissão cadastrada
    Quando envio a consulta
    Então vejo o início do período, a descrição resumida do gênero, o fornecedor, a razão social e a quantidade inicial
    E vejo nas linhas os órgãos que ainda não foram identificados

  Cenário: A combinação informada não tem permissão
    Dado que informo um tipo de contrato, uma data limite, uma subclasse e um gênero sem permissão registrada
    Quando envio a consulta
    Então vejo a mensagem "* Permissao nao cadastrada para identificacao *"
    E o cursor volta para o campo da data limite

  Cenário: Alteração sem consultar antes
    Dado que estou alterando e mexi num dos dados de identificação da permissão
    Quando envio a alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta para o campo da operação

  Cenário: A linha marcada para inclusão grava a permissão daquele órgão
    Dado que estou alterando e há uma permissão consultada
    Quando marco uma linha para inclusão e envio
    Então a permissão daquele órgão é gravada
    E o rastro de auditoria da inclusão é gravado depois
    E o órgão deixa de aparecer na lista

  Cenário: A linha sem marcação não grava nada
    Dado que estou alterando
    Quando envio sem marcar nenhuma linha e sem marcar o total
    Então nenhuma permissão é gravada

  Cenário: A cópia traz os órgãos de outra permissão
    Dado que outra permissão da minha coordenadoria tem órgãos identificados
    Quando informo os dados dessa permissão para copiar e envio a alteração
    Então cada órgão identificado na origem ganha a permissão na combinação informada
    E o registro da coordenadoria inteira é apagado

  Cenário: A permissão de origem não tem órgãos
    Dado que informo, para copiar, uma permissão sem órgãos identificados
    Quando envio a alteração
    Então vejo a mensagem "* Nao existem registros para copia *"
    E o cursor volta para o campo da subclasse de origem
    E nada é gravado ou apagado

  Cenário: O flag de total grava para todos os órgãos da coordenadoria
    Dado que estou alterando e há órgãos ativos sem a permissão identificada
    Quando marco o flag de total e envio
    Então cada órgão ativo sem a permissão ganha o seu registro
    E os órgãos que já tinham a permissão continuam como estavam

  Cenário: A lista mostra os órgãos que ainda não estão identificados
    Dado que a coordenadoria tem órgãos com e sem a permissão identificada
    Quando a lista é montada
    Então ela mostra os órgãos sem a permissão, em até 8 linhas
    E a lista continua a partir do último órgão mostrado

  Cenário: Todos os órgãos já identificados
    Dado que todos os órgãos da coordenadoria já têm a permissão identificada
    Quando a tela é apresentada
    Então vejo a mensagem "* Orgaos ja identificados *"
    E o campo do órgão inicial é limpo
    E nenhuma linha é preenchida

  Cenário: Vim da consulta do período e tento alterar
    Dado que cheguei à tela C675T pela consulta do período, na tela C674C
    Quando tento alterar
    Então sou devolvido à tela C674C, em consulta
    E nada é gravado aqui

  Cenário: Pelo menu, a alteração acontece
    Dado que cheguei à tela C675T pelo menu e consultei a permissão
    Quando altero e envio
    Então a identificação é gravada

  Cenário: O encaminhamento para a tela de exclusão
    Dado que marco o campo que pede a tela de exclusão
    Quando envio
    Então chego à tela C675C, em consulta

  Cenário: A próxima tela informada na máscara
    Dado que a máscara traz um código de tela no campo de próxima tela
    Quando envio
    Então sou encaminhado para a tela informada
    E a lógica da C675T termina ali

  Cenário: Digitação não numérica é recusada
    Quando informo um valor não numérico num dos campos de código ou de data
    Então a tela recusa antes de ler a permissão
    E o cursor volta ao campo recusado quando ele tem posição na tela

  Cenário: A consulta não grava nada
    Dado que estou consultando uma permissão
    Quando envio a consulta
    Então nenhuma permissão é gravada, alterada ou apagada
    E nenhum rastro de auditoria é gerado
```
