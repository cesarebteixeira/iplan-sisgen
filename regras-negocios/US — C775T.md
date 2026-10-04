# US — C775T — Pedir a cópia dos cardápios e dos planejamentos de um período para outro

## Estória

Como **servidor de CRE**, quero **pedir que os cardápios e os planejamentos já
cadastrados num período sejam repetidos em outro, indicando o tipo de órgão, o grupo e
o segmento de cada ponta**, para que **o período novo já conte com a mesma composição do
período anterior, sem que eu tenha de remontá-la grupo por grupo e segmento por
segmento**.

O cardápio de um período é guardado por grupo e por segmento de atendimento, e o
planejamento segue essa mesma composição. Quando o período seguinte repete o anterior,
essa composição poderia ser reaproveitada, mas não há como copiá-la pela tela do
cadastro — cada período é montado do zero. Esta tela existe para recolher de qual
período se copia, para qual período e com que tipo de órgão, grupo e segmento em cada
ponta, pedir a confirmação e entregar o pedido ao processamento do sistema. Ela não é
tela de cadastro: quem copia é o processamento, e a tela só registra o pedido.

## Contexto

Jornada S000M → C000M → C070M → C775T.

Ator: servidor de CRE — pede a cópia dos cardápios e dos planejamentos de um período
para outro, informando o tipo de órgão, o grupo e o segmento de cada ponta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O `C000M` e o `C070M` são menus e não
gravam nada; o contexto que esta tela usa — matrícula, código de acesso, privilégio,
tipo de órgão e coordenação regional — é o que a entrada deixou na sessão.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela pede a cópia dos cardápios e dos planejamentos de um período para outro

O servidor informa o **período de origem** e o **período de destino** — cada um com o
seu tipo de órgão, o seu grupo, as suas datas de início e fim e o seu segmento — e a
tela pede a confirmação antes de registrar coisa alguma. Confirmado, ela registra a
**solicitação de processamento** e o **lançamento de auditoria**, e avisa
**\* Cadastro sendo atualizado \***. A tela não espera pelo resultado e não mostra o
que foi copiado: o desfecho do pedido acontece no processamento, e não volta para ela.

[?] O acervo desta jornada mostra o que a tela entrega ao processamento e onde o pedido
é registrado, mas não o processamento em si: se ele copia mesmo o cardápio e o
planejamento de origem para o destino, o que faz quando a origem não tem composição
para o segmento pedido e o que ele faz com o que já existir no destino é pergunta ao
site.

### RN-02 — A tela não copia cadastro nenhum: registra o pedido e a auditoria

Esta tela não inclui, não altera e não exclui cardápio, planejamento, grupo, segmento
nem tipo de órgão: o que ela grava é a **solicitação de processamento**, com o número
seguinte da fila de pedidos, e o **lançamento de auditoria** da operação. As rotinas de
gravação, de exclusão e de travamento existem declaradas para os **dez** cadastros e
registros que a tela enxerga, mas **só duas gravações são executadas** — a da
solicitação e a da auditoria —, e nenhuma exclusão e nenhum travamento. Declarar não é
executar: os outros oito são só lidos.

### RN-03 — O período de origem é o que tem cardápio na data final informada

O período de origem não é escolhido por um código: ele é identificado pela **data
final** que o servidor informa, dentro do tipo de órgão de origem. A tela procura um
cardápio com essa data final; não havendo, recusa com
**\* Nao existem cardapios para esta data - DE \*** e devolve o cursor a esse campo. A
**data inicial** do período de origem que a tela exibe — e que entrega ao processamento
— não é a que o servidor digitou: ela é reposta com a data inicial do cardápio
encontrado.

[?] A data inicial de origem é pedida e editada, mas é descartada assim que o cardápio é
encontrado; os três campos dela, além disso, não têm posição de cursor. Se ela deveria
identificar o cardápio de origem — ou conferir o que foi lido —, o caminho não a usa.
Pergunta ao site.

[?] A data inicial de origem nunca é conferida como data, nem contra a data final de
origem; a data final de origem também não é conferida como data — do período de origem
a tela só confere a existência do cardápio naquela data. Se as duas deveriam ser
validadas, o caminho não valida. Pergunta ao site.

### RN-04 — O tipo de órgão e o grupo das duas pontas têm de existir no cadastro

Cada ponta informa o seu **tipo de órgão** e o seu **grupo** — a coordenação regional. O
tipo de órgão tem de constar do cadastro de secretarias, e o grupo, do cadastro de
grupos daquele tipo de órgão. Faltando o tipo de órgão, a recusa é
**\* Secretaria nao cadastrada - PARA \*** ou **\* Secretaria nao cadastrada - DE \***;
faltando o grupo, **\* Grupo nao cadastrado - PARA \*** ou **\* Grupo nao cadastrado -
DE \***, sempre com o cursor no campo recusado. É do cadastro que sai a descrição do
tipo de órgão que a tela mostra em cada ponta; a descrição do grupo não é mostrada — o
grupo aparece só pelo código.

[?] O grupo é informado e conferido nas duas pontas, mas não participa de nenhuma
procura que a tela faz: as procuras de cardápio e de composição são só pelo tipo de
órgão. Se o grupo deveria restringir o que se copia, o caminho não o usa. Pergunta ao
site.

### RN-05 — As datas do período de destino são conferidas, e a data final tem de cair num dia da semana

As datas de início e fim do período de destino são conferidas como data — ano entre 1994
e 2099, dia e mês válidos — e a de início não pode ser maior que a final. Cada recusa
tem a sua mensagem — **\* Data inicial do cardapio invalida - PARA \***,
**\* Data final do cardapio invalida - PARA \***,
**\* Data inicial maior que data final - PARA \*** — e o cursor volta ao campo recusado.
Além disso, a data final tem de cair no **dia da semana anterior** ao dia que o cadastro
de dias associa ao tipo de órgão do destino; não caindo, a recusa é
**\* <- Data final deve ser este dia da semana \***, com o dia exigido mostrado junto.
Quando o cadastro não tem dia para aquele tipo de órgão — ou o dia está em branco —
essa exigência não se aplica.

[?] O acervo mostra o dia associado ao tipo de órgão, mas não diz o que ele significa em
negócio (o dia em que não há cardápio? o dia em que o período recomeça?) nem por que a
data final tem de ser o dia imediatamente anterior a ele. Pergunta ao site.

### RN-06 — O segmento das duas pontas tem de existir para o respectivo tipo de órgão

Cada ponta informa o seu **segmento**, e o segmento tem de constar do cadastro de
segmentos daquele tipo de órgão: não constando, a recusa é
**\* Segmento invalido - PARA \*** ou **\* Segmento invalido - DE \***, com o cursor no
campo. A descrição mostrada de cada segmento vem do cadastro.

[?] Na tela C772T, que pede só a cópia dos cardápios, o segmento **99** significa
"todos" e dispensa a conferência; nesta tela não há esse tratamento, de modo que o 99 só
passa se constar do cadastro daquele tipo de órgão. Se "todos" deveria valer aqui — e
por que ele dispensa a conferência lá e não aqui —, o caminho não diz. Pergunta ao site.

### RN-07 — O intervalo do período de destino tem de estar livre

A tela procura cardápios do tipo de órgão do destino a partir das duas datas do destino
— a inicial e a final — e, se o que encontra cobrir o intervalo pedido, recusa com
**\* <- Cardapios ja cadastrados neste intervalo \***, mostrando junto a data limite do
cardápio que já existe, e devolve o cursor à data inicial do destino. Um cardápio só
conta como ocupando o intervalo se existir também a **composição daquele segmento** para
ele: é o segmento do destino que decide.

[?] A procura leva as datas como chave, mas a conferência que vem depois compara o
intervalo lido do cadastro; o efeito exato da leitura — se ela exige a data exata ou
apenas se posiciona no primeiro cardápio a partir dela — decide se a tela recusa sempre
que existe cardápio com aquela data limite, ou se compara mesmo os intervalos. Os dois
comportamentos são compatíveis com o que o fonte mostra, e o significado dos indicadores
da leitura comum não está no acervo. Pergunta ao site.

[?] A procura da composição do segmento fixa a subclasse e o gênero em zero e não confere
esses dois valores de volta: se um cardápio tem composição para o segmento em outra
subclasse ou outro gênero, o acervo não permite dizer se ele conta como ocupando o
intervalo. Pergunta ao site.

### RN-08 — A cópia só é pedida depois de confirmada, e mudar um campo refaz a conferência

Passadas todas as conferências, a tela mostra
**\* Confirma copia cardap/planejamentos <S/N> ? \*** e espera a resposta; só a resposta
**S** registra o pedido. Junto com a resposta, os dois tipos de órgão, os dois grupos, os
dois segmentos, as duas datas do período de destino e a data final do período de origem
têm de continuar iguais ao que a tela guardou; mudando qualquer um deles, as conferências
recomeçam e a confirmação volta a ser pedida.

[?] Responder **N** não cancela: a tela limpa a resposta, repõe o que já estava em tela e
**volta a pedir a mesma confirmação**. Não há, no caminho lido, um desfecho que encerre a
operação com a resposta negativa. Se o esperado é que N cancele, o caminho não cancela.
Pergunta ao site.

### RN-09 — Um pedido do mesmo processamento já registrado impede outro

Antes de registrar, a tela confere se já existe **solicitação de processamento
registrada** para este mesmo processamento; existindo, recusa com
**\* Relatorio em processamento. Aguarde. \***, com o cursor na resposta, e não registra
nada.

[?] A conferência procura as solicitações com a marca de atendimento em branco e o número
do pedido zerado, mas, do registro que encontra, só confere de volta o código do
processamento: se uma solicitação já atendida também bloqueia, o acervo não permite
concluir. Quem atende a solicitação — e a marca como atendida ou a remove — não está nos
fontes desta jornada: se ninguém a atender, o pedido de cópia só pode ser feito uma vez.
Pergunta ao site.

### RN-10 — O pedido recebe o número seguinte da fila e guarda quem pediu, quando e de onde

A solicitação é registrada na fila de processamento com o **número seguinte** ao último
já usado, o código do processamento pedido, o tipo de órgão de origem, a matrícula, a
estação e o dia, o mês e o ano da sessão, e **sem marca de atendimento**. É esse número
que identifica o pedido na fila.

### RN-11 — O processamento recebe os dois períodos, os dois órgãos, os dois grupos e os dois segmentos

O pedido entregue ao processamento leva o tipo de órgão, o grupo, as duas datas e o
segmento de cada ponta, além da estação, da matrícula e o **e-mail** lido do cadastro do
funcionário. É por essa entrega que o processamento sabe o que copiar e para onde; o
resultado não volta para a tela.

[?] A entrega à fila de processamento é feita pela chamada comum de submissão do
ambiente, que não tem corpo no acervo lido: o que a rotina faz com o pedido — e o que o
processamento faz com ele — não está nos fontes desta jornada. Pergunta ao site.

### RN-12 — Todo pedido deixa rastro na auditoria

Cada pedido registra um lançamento na auditoria com os dois tipos de órgão, os dois
grupos, as duas datas e os dois segmentos pedidos, a operação, a tela de origem, a
matrícula, a estação e a data e a hora da sessão, e com o **tipo de órgão e o grupo da
sessão** — não os informados em tela —; o valor posterior fica em branco. O lançamento
guarda **o que foi pedido**, não o que foi copiado.

[?] O lançamento identifica o pedido pelo **dia da data inicial do destino** no campo do
número do processo, e nunca recebe um número de processo de verdade: o acervo não diz se
isso é intencional nem o efeito disso na chave da auditoria. Pergunta ao site.

### RN-13 — Só a atualização: qualquer outro modo é recusado

A tela abre no modo de atualização e exige esse modo. Se o modo que chega for outro, o
sistema recusa com **\* Operacao nao disponivel. Use ALT \*** e devolve o cursor ao campo
do modo, antes de ler qualquer cadastro; nesse caminho nada é lido e nada é registrado.

[?] A mensagem manda usar "ALT", mas o modo que a tela aceita é o código de alteração do
sistema, e nenhum valor "ALT" existe no acervo lido: ou o formulário traduz o que o
servidor digita para esse código, ou quem seguir a mensagem é recusado. Pergunta ao site.

### RN-14 — A digitação dos dezoito campos numéricos é editada, e o cursor volta ao campo recusado

Os **dezoito campos informados** — os dois tipos de órgão, os dois grupos, as duas datas
de cada período, em três partes cada, e os dois segmentos — passam por edição numérica
antes de qualquer leitura: campo em branco é tratado como zero, e o que não for número é
recusado. O cursor volta ao campo recusado para **quinze** deles; os três campos da data
inicial de origem não têm posição de cursor.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não está
nos fontes desta jornada: a rotina que faz a edição numérica é declarada no programa de
runtime e não tem corpo no acervo lido. Pergunta ao site.

### RN-15 — Ao abrir, a tela apaga o resultado anterior e mostra o cabeçalho

Antes de conferir a digitação e de ler qualquer cadastro, a tela apaga os **sete campos
de resultado** da apresentação anterior — a descrição do tipo de órgão da sessão, a data
do sistema, as descrições dos dois tipos de órgão informados, as descrições dos dois
segmentos e a mensagem —, de modo que uma conferência recusada não deixa em tela o
resultado da anterior. O cabeçalho recebe, na abertura, a data do sistema e a descrição
do tipo de órgão da sessão; as descrições dos dois tipos de órgão informados e as dos
dois segmentos vêm dos cadastros.

[?] A data do sistema e a descrição do tipo de órgão da sessão são copiadas de duas áreas
de trabalho que nenhum caminho do acervo preenche — a única atribuição que existe para
elas é a inicialização em branco no programa de runtime. Se o ambiente as preenche em
outro lugar, o acervo não diz; se não preencher, os dois campos saem em branco. Pergunta
ao site.

### RN-16 — A recusa de destino inválido não é alcançável pela tela

O ramo que trata a **distribuição automática** do lançamento entre destinos — e a recusa
de destino inválido que vem com ela — só roda se o modo de distribuição automática
estiver preenchido; a tela limpa esse campo imediatamente antes dos dois únicos pontos em
que ele poderia disparar. Pela tela, portanto, a recusa de destino inválido **não** é
apresentada.

[?] A limpeza é feita nos dois pontos e o ramo fica sem caminho: se a distribuição
automática deveria valer para esta tela, o caminho não a alcança. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Cópia dos cardápios e dos planejamentos de um período para outro

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C775T

  Cenário: O pedido de cópia dos cardápios e dos planejamentos de um período para outro
    Dado que informei o período de origem com uma data final que tem cardápio cadastrado
    E informei o período de destino, com o tipo de órgão, o grupo, as datas e o segmento das duas pontas
    Quando respondo S à confirmação
    Então vejo a mensagem "* Cadastro sendo atualizado *"
    E a solicitação de processamento é registrada
    E a operação fica registrada na auditoria

  Cenário: A tela não copia cadastro nenhum
    Dado que confirmo a cópia
    Então nenhum cardápio, planejamento, grupo, segmento ou tipo de órgão é incluído, alterado ou excluído por esta tela
    E o que fica registrado é a solicitação de processamento e a auditoria

  Cenário: O processamento recebe os dois períodos, os dois órgãos, os dois grupos e os dois segmentos
    Dado que confirmo a cópia
    Então o processamento é entregue com o tipo de órgão, o grupo, as duas datas e o segmento de cada ponta
    E com a estação, a matrícula e o meu e-mail lido do cadastro do funcionário

  Cenário: O pedido recebe o número seguinte da fila
    Dado que confirmo a cópia
    Então a solicitação é registrada com o número seguinte ao último já usado
    E fica sem marca de atendimento

  Cenário: Todo pedido deixa rastro na auditoria
    Dado que confirmei o pedido de cópia
    Quando o registro termina
    Então existe um lançamento de auditoria com os dois períodos, os dois órgãos, os dois grupos e os dois segmentos pedidos
    E com a operação, a tela de origem, a matrícula, a estação e a data e a hora da sessão
    E com o valor posterior em branco

  Cenário: Período de origem sem cardápio na data final
    Quando informo uma data final de origem que não tem cardápio cadastrado
    Então vejo "* Nao existem cardapios para esta data - DE *"
    E o cursor volta ao campo da data final de origem
    E nada é registrado

  Cenário: A data inicial de origem vem do cardápio cadastrado
    Dado que digitei uma data inicial de origem diferente da do cardápio cadastrado
    Quando envio a tela
    Então a data inicial de origem em tela passa a ser a do cardápio cadastrado
    E é essa data que vai para o processamento

  Cenário: Tipo de órgão não cadastrado
    Quando informo um tipo de órgão que não consta do cadastro
    Então vejo "* Secretaria nao cadastrada - PARA *" ou "* Secretaria nao cadastrada - DE *"
    E o cursor volta ao campo do tipo de órgão recusado
    E nada é registrado

  Cenário: Grupo não cadastrado
    Quando informo um grupo que não consta do cadastro daquele tipo de órgão
    Então vejo "* Grupo nao cadastrado - PARA *" ou "* Grupo nao cadastrado - DE *"
    E o cursor volta ao campo do grupo recusado
    E nada é registrado

  Cenário: Data do período de destino inválida
    Quando informo uma data de início ou de fim do período de destino que não é uma data válida
    Então vejo "* Data inicial do cardapio invalida - PARA *" ou "* Data final do cardapio invalida - PARA *"
    E o cursor volta ao campo recusado
    E nada é registrado

  Cenário: Data inicial do destino maior que a final
    Quando informo a data inicial do destino maior que a data final
    Então vejo "* Data inicial maior que data final - PARA *"
    E nada é registrado

  Cenário: Data final do destino em dia da semana não permitido
    Dado que o cadastro de dias associa um dia ao tipo de órgão do destino
    Quando informo uma data final de destino que não cai no dia anterior a esse dia
    Então vejo "* <- Data final deve ser este dia da semana *" com o dia exigido
    E nada é registrado

  Cenário: Sem dia associado ao tipo de órgão, a data final não é restringida
    Dado que o cadastro de dias não tem dia para o tipo de órgão do destino
    Quando informo qualquer data final válida para o destino
    Então a tela aceita a data
    E segue para a conferência do intervalo de destino

  Cenário: Segmento não cadastrado para o tipo de órgão
    Quando informo um segmento que não consta do cadastro daquele tipo de órgão
    Então vejo "* Segmento invalido - PARA *" ou "* Segmento invalido - DE *"
    E o cursor volta ao campo do segmento recusado
    E nada é registrado

  Cenário: Já existe cardápio cobrindo o intervalo de destino
    Dado que existe cardápio que cobre o intervalo pedido para o destino
    E esse cardápio tem composição para o segmento do destino
    Quando envio a tela
    Então vejo "* <- Cardapios ja cadastrados neste intervalo *" com a data limite do cardápio existente
    E o cursor volta à data inicial do destino
    E nada é registrado

  Cenário: Cardápio sem a composição do segmento não ocupa o intervalo
    Dado que o único cardápio que cobre o intervalo de destino não tem composição para o segmento do destino
    Quando envio a tela
    Então a tela segue para o pedido de confirmação, sem a recusa de intervalo ocupado

  Cenário: A confirmação vem antes de qualquer registro
    Dado que todas as conferências passaram
    Quando envio o pedido
    Então vejo "* Confirma copia cardap/planejamentos <S/N> ? *"
    E nenhuma solicitação foi registrada ainda

  Cenário: A resposta negativa não cancela e não grava nada
    Dado que a tela pediu a confirmação
    Quando respondo N
    Então a tela volta a pedir a confirmação
    E nenhuma solicitação é registrada

  Cenário: Mudar um campo depois da confirmação faz a confirmação voltar
    Dado que a tela pediu a confirmação
    Quando mudo a data final do destino e respondo S
    Então a tela volta a conferir o pedido
    E volta a pedir a confirmação, sem registrar nada

  Cenário: Já existe pedido deste processamento
    Dado que existe solicitação de processamento registrada para este processamento
    Quando respondo S à confirmação
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E uma segunda solicitação não é registrada

  Cenário: Modo diferente da atualização
    Dado que o modo informado não é a atualização
    Quando envio a tela
    Então vejo "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo do modo
    E nenhum cadastro é lido

  Cenário: Digitação não numérica nos campos informados
    Dado que digitei algo que não é número em um dos dezoito campos informados
    Quando envio a tela
    Então o sistema recusa a digitação antes de ler qualquer cadastro
    E o cursor volta ao campo recusado

  Cenário: O resultado da apresentação anterior é apagado
    Dado que a apresentação anterior mostrou as descrições e a mensagem
    Quando envio uma conferência que é recusada
    Então as descrições e a mensagem anteriores não ficam em tela

  Cenário: O cabeçalho mostra a data do sistema e o tipo de órgão da sessão
    Dado que entrei no sistema
    Quando abro a tela C775T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: A tela não apresenta a recusa de destino inválido
    Dado que estou na tela C775T e confirmei o pedido de cópia
    Quando a gravação é preparada
    Então a tela limpa o modo de distribuição automática
    E a recusa de destino inválido não é apresentada
```
