# US — C685T — Itens iniciais da permissão de contrato, por classe, subclasse e gênero

## Estória

Como **servidor da Coordenação Regional Escolar (CRE)**, quero **trazer de outro tipo de
contrato os itens iniciais da permissão de contrato da minha coordenação — e poder apagá-los de
uma vez quando o lançamento não serve**, para que **cada classe, subclasse e gênero da permissão
fique com a quantidade e o valor iniciais registrados, sem digitação item a item**.

A permissão de contrato é detalhada item a item — por classe, subclasse e gênero —, e é nesse
detalhe que ficam a quantidade inicial e o valor inicial de cada item. Esta é a tela que povoa
esse detalhe: em vez de pedir a digitação item a item, ela traz os itens de outro tipo de
contrato e reprecifica cada um pelo valor unitário do próprio contrato; é também ela que apaga o
detalhe inteiro, quando o lançamento precisa ser refeito. Sem esse detalhe a permissão fica sem
quantidade e sem valor inicial por item, porque aqui não se digita item: só se copia o que já
existe em outro contrato.

## Contexto

Jornada S000M → C000M → C050M → C664M → C685T.

Ator: servidor de CRE — consulta, copia de outro tipo de contrato e exclui os itens iniciais da
permissão de contrato da sua coordenação regional.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O tipo de órgão, a coordenação regional, a matrícula, o código de acesso, o privilégio, a data
do sistema e a descrição do tipo de órgão chegam pela sessão, deixados pela entrada; esta tela
não os recalcula. A tela **não** entrega a transação a nenhuma outra: a jornada termina nela.
As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — Esta tela cria e apaga os itens da permissão de contrato; ela não altera a permissão

A permissão de contrato tem dois registros: a **permissão** — o que o contrato carrega para a
secretaria, a coordenação regional, o período e o grupo de licitação — e o **detalhe dos itens**,
um registro por classe, subclasse e gênero, com a quantidade e o valor iniciais. Esta tela
mantém o detalhe dos itens, e só ele: a alteração apaga o detalhe que existe e o recria a partir
de outro contrato, e a exclusão apaga o detalhe inteiro. A permissão não é gravada nem apagada
por aqui, e nenhum outro cadastro o é: a tela lê o cadastro de títulos das telas, o dos tipos de
órgão, o dos gêneros, o das permissões de contrato e o dos fornecedores, e grava e apaga apenas
no detalhe dos itens. Esse detalhe tem capacidade para **100.000** registros — capacidade é o
máximo esperado, parâmetro de dimensionamento, não o que está cadastrado.

[?] As telas vizinhas da permissão registram as suas alterações na auditoria do sistema; esta
não monta nem grava esse registro. Se a intenção era que a cópia e a exclusão dos itens
deixassem rastro, o caminho não deixa. Pergunta ao site.

[?] O nome de negócio desta tela não vem do material: o título que ela exibe é lido do cadastro
de títulos do sistema, cujo conteúdo não faz parte do lote. O nome usado nesta estória é leitura
de negócio, não transcrição. Pergunta ao site.

### RN-02 — A permissão se identifica pela coordenação regional, pelo tipo de contrato, pelo grupo de licitação e pelo período; o tipo de órgão vem da sessão

A identificação da permissão é a coordenação regional, o tipo de contrato, o grupo de licitação
e as três partes da data limite do período; o tipo de órgão não se digita — é o da secretaria
escolhida na entrada e ficou na sessão, e entra na identificação de tudo o que a tela lê e
grava. Dessa combinação, mais a classe, a subclasse e o gênero, sai o item.

Achada a permissão, três coisas do cabeçalho deixam de ser digitação e passam a ser as do
cadastro: a data de início do período, o código do fornecedor — com o nome buscado no cadastro
de fornecedores por esse código — e os valores homologado e adjudicado. Nenhuma delas identifica
a permissão nem entra nas conferências de alteração e de exclusão; e o código do fornecedor não
é gravado por esta tela. No alto a tela mostra a descrição do tipo de órgão da sessão e a data
do sistema.

Para a alteração existe, além disso, o **tipo de contrato cópia** com as três partes da data
limite dele: é de lá que os itens são trazidos (RN-09), e por isso ele é um segundo jogo de
identificação, separado da permissão que está em tela.

[?] A alteração aceita trocar o código do fornecedor — ele não entra na conferência do
"consulte antes" — mas a tela não grava fornecedor em lugar nenhum, e o registro que ela grava
não tem esse campo. Se o fornecedor deveria ser gravado na permissão e a gravação ficou de
fora, ou se ele é só conferência na tela, o material não diz. Pergunta ao site.

### RN-03 — A grade tem doze linhas, uma por classe, subclasse e gênero

A grade tem **doze linhas**, e cada linha é um item da permissão: a classe, a subclasse, o
gênero, a descrição resumida do gênero — buscada no cadastro de gêneros pela classe, pela
subclasse, pelo gênero e pela data de início do período — e três números: a quantidade inicial,
o valor inicial do item e uma segunda quantidade. Não achando o gênero, a linha sai sem a
descrição, e os demais dados dela aparecem normalmente. Os itens de uma mesma permissão são
distinguidos pela classe, pela subclasse e pelo gênero.

[?] O que é a segunda quantidade da linha — e o segundo valor que o detalhe guarda ao lado dos
dois primeiros — não vem do material: os dois pares têm o mesmo nome de negócio e significados
diferentes que o acervo não declara. O mesmo já foi registrado na jornada da E121T. Pergunta ao
site.

### RN-04 — A tela abre em consulta e só aceita consultar, alterar e excluir

A tela aceita três modos de manutenção: **alteração**, **exclusão** e **consulta**. Chegando com
qualquer outro — incluir, entre eles —, ela recusa com **\* Opcao nao disponivel. Use ALT, EXC
ou CON \***, devolve o cursor ao campo do modo e não confere nem grava nada. Chegando sem modo
informado, a tela assume a consulta. A conferência que ela faz ao se exibir também só reconhece
os modos de consulta e de alteração: com o de exclusão, ela não chega a ler os itens. O
roteamento, chamado antes, recusa um código de operação que o sistema não conhece com **\*
Operacao nao disponivel \***, e a transação não segue.

[?] As palavras que o operador precisa informar no campo do modo não são texto fixo da tela:
elas vêm da tabela de mensagens do idioma, que não faz parte do material, e a mensagem da recusa
nomeia ALT, EXC e CON. Se essas forem as palavras que o sistema carrega, a guarda e a mensagem
combinam; se não forem, a tela recusa justamente o que a mensagem manda usar. Pergunta ao site.

### RN-05 — A tela só trabalha na coordenação regional da sessão

Informada uma coordenação regional diferente daquela em que o servidor entrou, a recusa é **\*
Usuario sem acesso a este grupo \*** — a mensagem chama a coordenação regional de **grupo** —,
com o cursor de volta nesse campo, e nada é conferido nem gravado. Quando a sessão não tem
coordenação regional definida, esta tela não impõe a restrição.

[?] A recusa lê dois valores de sessão diferentes: um para saber se o servidor tem grupo e outro
para comparar com o grupo informado. Nenhum dos dois é preenchido pelo programa desta tela —
vêm da sessão montada na entrada. Se os dois carregam sempre o mesmo grupo, o material não diz.
Pergunta ao site.

### RN-06 — A consulta exige a permissão de contrato cadastrada

Não estando a permissão registrada para o tipo de órgão da sessão, a coordenação regional, o
período, o tipo de contrato e o grupo de licitação informados, a recusa é **\* Permissao nao
cadastrada \***, com o cursor de volta na coordenação regional, e nada é mostrado nem gravado.
Existindo, o início do período, o código do fornecedor e os valores homologado e adjudicado
passam a ser os do cadastro: o que tiver sido digitado neles é substituído.

### RN-07 — Não havendo item para mostrar, a tela avisa e não preenche linha nenhuma

Não havendo item para a permissão consultada, a tela avisa **\*Qt inicial nao cadastrada \*** e
nenhuma linha da grade é preenchida. O aviso é decidido na montagem da primeira linha e não se
repete nas outras; e ele não sai quando o modo é o de exclusão, porque excluir o detalhe de uma
permissão que ainda não tem detalhe é legítimo. Quando a tela é aberta sem nenhuma consulta
anterior na sessão, a grade sai vazia e sem aviso.

[?] A procura do item começa com a linha em branco e vai sendo repetida linha a linha; o que as
marcas da rotina de leitura fazem quando parte da identificação vai zerada não está no corpus
nem no manual. Isso decide se a tela pagina os itens ou repete o mesmo; e, como a linha sem item
cadastrado é recusada, decide também se uma permissão com menos itens do que a página é
recusada. Pergunta ao site.

### RN-08 — Alterar e excluir exigem os dados da consulta anterior

Na alteração e na exclusão, a coordenação regional, o tipo de contrato, o grupo de licitação e
as três partes da data limite informados têm de ser exatamente os da consulta anterior. Na
alteração, qualquer diferença é recusada com **\* Consulte antes de atualizar \***; na exclusão,
com **\* Consulte antes de excluir \*** — nos dois casos com o cursor de volta na coordenação
regional, e nada é gravado. O início do período, o fornecedor e os valores não entram nessa
conferência: eles são do cadastro.

A consulta, ao contrário, pode ser feita com dados novos: ela lê a permissão e recomeça. Mas a
consulta repetida com os **mesmos** dados não relê nada — achando os dados iguais aos guardados,
a tela pula a procura da permissão e a do fornecedor.

[?] Como a consulta repetida pula a procura, uma permissão apagada entre duas consultas iguais
não é percebida. Se é intencional, o material não diz.

### RN-09 — A alteração traz os itens de outro tipo de contrato, e o tipo copiado tem de ser diferente e estar cadastrado

A alteração desta tela não digita item: ela **copia** o detalhe de itens de outro tipo de
contrato. O operador informa o tipo de contrato cópia e as três partes da data limite desse
contrato copiado; o tipo de órgão, a coordenação regional e o grupo de licitação são os mesmos
da permissão em tela. O tipo copiado tem de ser diferente do contrato em tela — sendo igual, a
recusa é **\* Tipo contrato copia igual da permissao  \*** — e tem de ter permissão cadastrada —
não tendo, a recusa é **\* Permissao copia nao cadastrada \***, nos dois casos com o cursor de
volta no tipo de contrato cópia. Informado o tipo cópia, a tela apaga o detalhe atual da
permissão e o recria a partir dos itens do contrato copiado.

[?] Com o campo do tipo de contrato cópia em branco, a alteração é aceita e termina sem mensagem
e sem gravar nada. Se a intenção era avisar que não há o que copiar, o caminho não avisa.
Pergunta ao site.

### RN-10 — Cada item copiado é reprecificado pelo valor unitário do contrato

A cópia não traz o valor do contrato copiado: ela traz a quantidade e os códigos do item —
classe, subclasse e gênero — e calcula o valor. Para isso, o sistema divide o valor inicial pela
quantidade inicial de cada item da permissão do próprio contrato, chegando ao valor unitário, e
multiplica esse valor unitário pela quantidade que veio do contrato copiado. Quando o item
copiado não tem, na permissão do contrato, um item com a mesma subclasse e o mesmo gênero, o
item é criado assim mesmo, com valor zerado e sem nenhum aviso.

[?] A quantidade vem de um contrato e o valor unitário vem do outro, e os dois são permissões
com os mesmos dois números gravados. O material não diz por que a quantidade não sai do mesmo
lado que o valor — se era para copiar a quantidade e reprecificar, ou para copiar o valor e
recontar. Pergunta ao site.

[?] A procura do valor unitário usa a subclasse e o gênero e ignora a classe; havendo a mesma
subclasse e o mesmo gênero em mais de uma classe do mesmo contrato, vale o primeiro que
aparecer. A fonte não permite dizer qual dos registros a cópia alcança. Pergunta ao site.

### RN-11 — A alteração apaga os itens antigos antes de criar os novos, no mesmo envio

A alteração percorre e apaga **todos** os itens do contrato e, só depois, cria os itens novos,
um a um, a partir dos itens do contrato copiado. Não há conferência intermediária nem volta
atrás: apagado o detalhe antigo, o detalhe novo é criado no mesmo envio, sem confirmação do
operador, e um item cuja criação não se efetive é abandonado em silêncio enquanto os outros
seguem. Se a cópia parar no meio, a permissão fica com o detalhe incompleto — o que já foi
apagado não volta. A exclusão e a criação rodam uma única vez por envio, na primeira página da
grade.

### RN-12 — A exclusão apaga todos os itens do contrato

A exclusão percorre os itens da permissão e apaga cada um, até não achar mais. Não há linha a
informar: a exclusão vale para a permissão inteira, e não depende do tipo de contrato cópia.
Nenhum item é criado no lugar, e a permissão continua como estava.

### RN-13 — A consulta não grava nada

Na consulta a tela só lê: a permissão de contrato, o detalhe dos itens, o cadastro dos gêneros
(para a descrição da linha), o do fornecedor, o dos tipos de órgão e o dos títulos. Nenhum item
é criado, nenhum é apagado e a permissão não é alterada. A exclusão e a alteração só acontecem
nos modos correspondentes, e a tela não pede confirmação.

### RN-14 — Nada é conferido nem gravado sem a autorização de perfil, de rota e de operação

Antes de conferir, a tela passa pela rotina de segurança do perfil da sessão, que confere a
matrícula e o cadastro da tela. No tratamento do que foi digitado, passa ainda pelas rotinas de
rota e de permissão por operação, levando o tipo de órgão, a coordenação regional, a matrícula,
o código de acesso e o privilégio da sessão, além do modo informado. Sem a tela no perfil de
acesso, a mensagem é **\* Acesso negado para esta matricula \***; sem a tela cadastrada, **\*
Tela nao disponivel \***; faltando o flag da operação no perfil, **\* Acesso negado para esta
operacao \***; e a tela não cadastrada no roteamento, **\* Tela nao cadastrada \***. Em todos
esses casos a transação é devolvida ao menu principal (ou à entrada, quando não há matrícula) e
nada é conferido, gravado ou apagado.

[?] As rotinas de segurança e a de rota só aparecem declaradas, sem corpo no material: a regra
efetiva de quem pode copiar e apagar os itens não pode ser lida nesta jornada. Pergunta ao site.

[?] Toda a conferência está atrás do prefixo de tela: chegando preenchido, a tela abandona a
conferência em silêncio, sem mensagem nenhuma; e a via que grava não testa esse prefixo de novo.
Nada nesta tela escreve nesse campo e o material não diz quem o preenche — se a máscara, se a
tela que a chamou —, nem se o abandono silencioso é o pretendido. Pergunta ao site.

[?] A conferência da operação só examina inclusão, alteração e exclusão: a consulta passa sem
flag nenhum. Se a consulta é livre por desenho ou se a conferência ficou incompleta, o material
não diz. Pergunta ao site.

### RN-15 — A digitação é numérica, e os números da linha vêm do cadastro

Os **vinte e dois** campos com rótulo na tela passam pela edição numérica antes de qualquer
leitura: os dez rótulos de negócio do cabeçalho (coordenação regional, tipo de contrato, código
do fornecedor, grupo de licitação, as três partes da data de início e as três da data limite),
os dois valores, o tipo de contrato cópia com as três partes do limite dele e, na linha em
conferência, a classe, a subclasse, o gênero, a quantidade inicial, o valor inicial do item e a
segunda quantidade. Campo em branco vira zero, e o que não for número é recusado. O cursor volta
ao campo recusado em **dez** deles (a coordenação regional, o tipo de contrato, o grupo de
licitação, as três partes da data limite, o tipo de contrato cópia com as três partes do limite
dele); nos outros doze, a recusa deixa o cursor onde estava.

Mesmo passando pela edição, os números das linhas não se digitam: a quantidade inicial, o valor
inicial do item e a segunda quantidade são trazidos do detalhe a cada exibição, e o que o
operador escrever neles é descartado.

[?] Os três números da linha são apresentados e conferidos como se fossem digitáveis, e o que se
digita neles nunca é usado: a tela os substitui pelo que leu do cadastro. Ou as colunas são de
leitura, ou a tela ignora o que foi informado. O mesmo já foi registrado na jornada da C658T.
Pergunta ao site.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não está nos
fontes desta jornada: a rotina que faz a edição numérica não faz parte do acervo lido. Pergunta
ao site.

[?] Esta estória foi escrita a partir da árvore expandida do sistema, e **52 linhas** do
programa desta tela ficaram de fora dessa versão (o perfil de compilação foi assumido, não
lido): o que estava nelas não faz parte desta jornada, e nada aqui afirma o contrário. Se alguma
regra de negócio estava entre elas, ela não está nesta estória. Pergunta ao site.

[?] Entre um envio e outro a tela guarda, na sessão, um conjunto de dados da permissão que ela
nunca chega a ler nem a gravar — o tipo de licitação com a descrição, o operador com o nome, o
status da permissão, o número e o ano do contrato e duas datas-base, cada uma com as suas três
partes. A máscara do material não os exibe: o material não diz se eram campos da tela ou sobra
do gerador. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Itens iniciais da permissão de contrato, por classe, subclasse e gênero

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a matrícula, o código de acesso, o privilégio, a coordenação regional e a data do sistema
    E tenho acesso à tela C685T

  Cenário: RN-02, RN-03, RN-06 e RN-13 — consultar os itens de uma permissão
    Dado que existe permissão de contrato da minha coordenação regional, para o tipo de contrato, o grupo de licitação e a data limite que informei
    E que a permissão tem itens cadastrados
    Quando confirmo a consulta
    Então vejo, em cada linha, a classe, a subclasse, o gênero, a descrição do gênero, a quantidade inicial, o valor inicial do item e a segunda quantidade
    E vejo o início do período, o fornecedor com o nome e os valores homologado e adjudicado vindos do cadastro
    E a tela mostra no máximo doze linhas
    E nada é gravado

  Cenário: RN-13 — a consulta não grava nada
    Dado que os itens da permissão estão em tela
    Quando envio a consulta quantas vezes quiser
    Então os itens continuam os mesmos
    E nenhum item é criado ou apagado e a permissão não muda

  Cenário: RN-08 — a consulta repetida com os mesmos dados não relê
    Dado que consultei esta permissão
    Quando confirmo de novo a consulta sem mudar nenhum dado
    Então a tela não procura de novo a permissão nem o fornecedor
    E nada é gravado

  Cenário: RN-03 — o gênero do item não está cadastrado
    Dado que o gênero de um item não está cadastrado para a data de início do período
    Quando confirmo a consulta
    Então a linha daquele item fica sem a descrição do gênero
    E a quantidade e o valor do item aparecem normalmente

  Cenário: RN-04 — a tela abre em consulta
    Dado que abro a tela C685T sem nada informado
    Então o campo do modo está no modo de consulta
    E a grade sai vazia, sem aviso

  Cenário: RN-04 — modo diferente de consulta, alteração e exclusão é recusado
    Dado que estou na tela C685T
    Quando a transação chega com o modo de inclusão
    Então vejo "* Opcao nao disponivel. Use ALT, EXC ou CON *"
    E o cursor fica no campo do modo
    E nada é lido e nada é gravado

  Cenário: RN-04 — operação que o sistema não conhece
    Quando a transação chega com um código de operação que o sistema não conhece
    Então vejo "* Operacao nao disponivel *"
    E a transação não segue

  Cenário: RN-05 — coordenação regional diferente da da sessão é recusada
    Dado que a minha sessão tem coordenação regional
    Quando informo uma coordenação regional diferente
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica nesse campo
    E nada é gravado

  Cenário: RN-06 — permissão de contrato não cadastrada
    Dado que não existe permissão de contrato para a coordenação regional, o tipo de contrato, o grupo de licitação e a data limite que informei
    Quando confirmo a consulta
    Então vejo "* Permissao nao cadastrada *"
    E o cursor fica na coordenação regional
    E nenhuma linha é preenchida

  Cenário: RN-07 — a permissão não tem item para mostrar
    Dado que a permissão existe e não tem nenhum item cadastrado
    Quando confirmo a consulta
    Então vejo "*Qt inicial nao cadastrada *"
    E nenhuma linha da grade é preenchida
    E nada é gravado

  Cenário: RN-07 — excluir o detalhe de uma permissão que ainda não tem detalhe
    Dado que a permissão existe e não tem nenhum item cadastrado
    Quando informo o modo de exclusão e confirmo
    Então a tela não me avisa de nada
    E nada é apagado

  Cenário: RN-08 — alterar sem consultar antes, ou mudando os dados da consulta
    Dado que a minha última consulta foi de outra permissão, ou que mudei a coordenação regional, o tipo de contrato, o grupo de licitação ou a data limite
    Quando informo o modo de alteração e confirmo
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica na coordenação regional
    E nada é gravado

  Cenário: RN-08 — excluir sem consultar antes, ou mudando os dados da consulta
    Dado que a minha última consulta foi de outra permissão, ou que mudei um dos dados que identificam a permissão
    Quando informo o modo de exclusão e confirmo
    Então vejo "* Consulte antes de excluir *"
    E o cursor fica na coordenação regional
    E nada é gravado

  Cenário: RN-09 — o tipo de contrato cópia é o mesmo do contrato
    Dado que consultei a permissão
    Quando informo, no tipo de contrato cópia, o mesmo tipo de contrato da permissão em tela
    Então vejo "* Tipo contrato copia igual da permissao  *"
    E o cursor fica no tipo de contrato cópia
    E nada é gravado

  Cenário: RN-09 — o contrato copiado não tem permissão cadastrada
    Dado que consultei a permissão
    Quando informo o tipo de contrato cópia e a data limite de um contrato sem permissão cadastrada
    Então vejo "* Permissao copia nao cadastrada *"
    E o cursor fica no tipo de contrato cópia
    E nada é gravado

  Cenário: RN-09 — a alteração com o tipo de contrato cópia em branco
    Dado que consultei a permissão e informo o modo de alteração
    Quando confirmo sem informar o tipo de contrato cópia
    Então nada é apagado e nada é criado
    E nenhuma mensagem me avisa disso

  Cenário: RN-09, RN-10 e RN-11 — copiar os itens de outro tipo de contrato
    Dado que consultei a permissão e ela tem itens
    E que o contrato copiado tem permissão cadastrada e itens próprios
    Quando informo o modo de alteração, o tipo de contrato cópia e a data limite dele, e confirmo
    Então os itens antigos da permissão são apagados
    E os itens do contrato copiado passam a ser os itens da permissão, com a classe, a subclasse e o gênero de lá
    E a quantidade de cada item é a quantidade do contrato copiado
    E o valor de cada item é a quantidade multiplicada pelo valor unitário do próprio contrato
    E a permissão não muda

  Cenário: RN-10 — o item copiado não tem valor unitário correspondente no contrato
    Dado que o contrato copiado tem um item cuja subclasse e gênero não existem na permissão do contrato
    Quando confirmo a alteração
    Então o item é criado assim mesmo, com valor zerado
    E nenhuma mensagem me avisa disso

  Cenário: RN-12 — excluir os itens da permissão
    Dado que consultei a permissão e ela tem itens
    Quando informo o modo de exclusão e confirmo
    Então todos os itens da permissão são apagados
    E nenhum item é criado no lugar
    E a permissão continua como estava

  Cenário: RN-14 — sem a tela no perfil de acesso
    Dado que o meu perfil não tem esta tela
    Quando entro na tela
    Então vejo "* Acesso negado para esta matricula *"
    E a transação é devolvida ao menu principal
    E nada é lido e nada é gravado

  Cenário: RN-14 — sem o flag da operação no perfil
    Dado que o meu perfil não tem o flag de alteração desta tela
    Quando confirmo a alteração
    Então vejo "* Acesso negado para esta operacao *"
    E a transação é devolvida ao menu principal
    E nada é gravado

  Cenário: RN-14 — a tela não está cadastrada
    Dado que a tela não está cadastrada para o sistema
    Quando entro na tela
    Então vejo "* Tela nao disponivel *" ou "* Tela nao cadastrada *"
    E nada é lido e nada é gravado

  Cenário: RN-14 — a volta para a tela anterior
    Dado que a transação traz o código da tela anterior
    Quando confirmo
    Então volto à tela de onde vim
    E nenhuma conferência é feita e nada é gravado

  Cenário: RN-15 — campo não numérico
    Quando preencho com letra a coordenação regional, o tipo de contrato, o fornecedor, o grupo de licitação, uma das datas ou um dos números da linha
    Então a tela recusa o campo antes de qualquer leitura
    E o cursor volta ao campo recusado, quando ele tem posição de retorno
    E nada é lido e nada é gravado

  Cenário: RN-15 — o que se digita nos números da linha é descartado
    Dado que os itens da permissão estão em tela
    Quando digito outra quantidade ou outro valor em uma linha e confirmo a consulta
    Então a linha continua mostrando a quantidade e o valor que estão no cadastro
```
