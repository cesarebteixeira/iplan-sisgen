# US — C772T — Pedir a cópia dos cardápios de um período para outro

## Estória

Como **servidor de CRE**, quero **pedir que os cardápios já cadastrados num período sejam repetidos em outro período, com o segmento que eu indicar em cada ponta**, para que **o período novo já conte com o mesmo cardápio do período anterior, sem que eu tenha de remontá-lo segmento por segmento**.

O cardápio de um período é guardado por segmento de atendimento: o mesmo período tem uma composição para cada segmento. Quando o período que vem repete o anterior, essa composição poderia ser reaproveitada, mas a tela do cadastro não copia nada — cada período é montado de novo, segmento por segmento. Esta tela existe para recolher de qual período se copia, para qual período e com quais segmentos, pedir a confirmação e entregar o pedido ao processamento do sistema, que é quem faz a cópia. Ela não é tela de cadastro: não inclui, não altera e não exclui cardápio nenhum.

## Contexto

Jornada S000M → C000M → C070M → C772T.

Ator: servidor de CRE — pede a cópia dos cardápios de um período já cadastrado para um período novo, escolhendo o segmento de cada ponta.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de negócio, e por isso não aparece entre as regras abaixo.

Os dois passos anteriores desta jornada são **menus** — o C000M e o C070M — e nenhum deles passa registro nem operação para esta tela: eles apenas chamam a tela pelo nome. Esta tela abre sozinha no modo de atualização, e o contexto que ela usa — matrícula, código de acesso, privilégio, tipo de órgão, coordenação regional e estação — é o que a entrada deixou na sessão. Ela também não encadeia em outra: terminado o pedido, ela reabre a si mesma.

As regras abaixo são só as da **tela desta jornada**. As regras da entrada estão no documento dela; a que se revelou pertencer à entrada está registrada no **anexo de evidências**, na seção própria.

## Regras de negócio

### RN-01 — A tela pede a cópia dos cardápios de um período para outro

O servidor informa o **período de origem** e o **período de destino**, cada um com o seu segmento, e a tela confere tudo e pede a confirmação antes de registrar coisa alguma. Confirmado o pedido, ela registra a **solicitação de processamento** e avisa **\* Cadastro sendo atualizado \***; o pedido é entregue ao processamento do sistema com o tipo de órgão da sessão, as duas datas de cada período e os dois segmentos. A tela não espera pelo resultado nem mostra o que foi copiado — o desfecho do pedido não volta para ela.

[?] O acervo desta jornada mostra o que a tela entrega ao processamento e onde o pedido é registrado, mas não o processamento em si: se ele copia mesmo o cardápio do período de origem para o de destino, o que faz quando a origem não tem composição para o segmento pedido e o que faz com o que já existe no destino é pergunta ao site.

### RN-02 — A tela não copia cardápio nenhum: registra o pedido e a auditoria

Esta tela não inclui, não altera e não exclui cardápio, segmento nem composição de cardápio: os cadastros que ela consulta são **só lidos**. O que ela grava é a **solicitação de processamento**, com o número seguinte da fila de pedidos, e o **registro de auditoria** da operação. As rotinas de gravação, de exclusão e de travamento existem declaradas para os oito cadastros que a tela enxerga, mas **só duas gravações são executadas** — a da solicitação e a da auditoria —, e nenhuma exclusão e nenhum travamento. Declarar não é executar.

### RN-03 — O período de origem é o que tem cardápio na data final informada

O período de origem não é escolhido por um código: ele é identificado pela **data final** que o servidor informa, dentro do tipo de órgão da sessão. A tela procura um cardápio com essa data final; não havendo, recusa com **\* Nao existem cardapios para esta data - DE \*** e devolve o cursor a esse campo. Havendo, a **data inicial** do período de origem que a tela exibe — e que manda ao processamento — deixa de ser a digitada e passa a ser a data inicial do cardápio encontrado.

[?] A data inicial de origem é pedida e editada, mas é descartada assim que o cardápio é encontrado; os três campos dela, além disso, não têm posição de cursor. Se ela deveria servir para identificar o cardápio de origem — ou para conferir o que foi lido —, o caminho não a usa. Pergunta ao site.

[?] A data inicial de origem nunca é conferida como data, nem contra a data final de origem: do período de origem a tela só confere a existência do cardápio na data final. Se ela deveria ser validada, o caminho não valida. Pergunta ao site.

### RN-04 — As datas do período de destino são conferidas, e a data final tem de cair num dia da semana

As datas de início e de fim do período de destino são conferidas como data — ano entre 1994 e 2099, dia e mês válidos — e a de início não pode ser maior que a final. Cada recusa tem a sua mensagem — **\* Data inicial do cardapio invalida - PARA \***, **\* Data final do cardapio invalida - PARA \***, **\* Data inicial maior que data final - PARA \*** — e o cursor volta ao campo recusado. Além disso, a data final tem de cair no **dia da semana anterior** ao dia que o cadastro de dias associa ao tipo de órgão da sessão; não caindo, a recusa é **\* <- Data final deve ser este dia da semana \***, com o dia exigido mostrado junto. Quando o cadastro não tem dia para o tipo de órgão — ou o dia está em branco —, essa exigência não se aplica.

[?] O acervo mostra o dia associado ao tipo de órgão, mas não diz o que ele significa em negócio (o dia em que não há cardápio? o dia em que o período recomeça?) nem por que a data final tem de ser o dia imediatamente anterior a ele. Pergunta ao site.

### RN-05 — O segmento é obrigatório nas duas pontas, tem de existir, e "todos" de um lado obriga "todos" do outro

Cada período tem o seu segmento, e nenhum dos dois pode ficar em branco: sem o segmento de destino, a recusa é **\* Informe segmento. Todos = 99 - PARA \***; sem o de origem, **\* Informe segmento. Todos = 99 - DE \***. O valor **99 significa todos os segmentos** e dispensa a conferência; qualquer outro tem de constar do cadastro de segmentos, senão a recusa é **\* Segmento invalido - PARA \*** ou **\* Segmento invalido - DE \***, com o cursor no campo. A descrição mostrada de cada segmento vem do cadastro. Quando o segmento de origem é "todos", a tela força o segmento de destino também para "todos": não se copia de todos os segmentos para um só.

### RN-06 — O intervalo de destino tem de estar livre

A tela procura cardápios do mesmo tipo de órgão a partir das duas datas do destino — a inicial e a final — e, se o que encontra cobrir o intervalo pedido, recusa com **\* <- Cardapios ja cadastrados neste intervalo \***, mostrando junto a data final do cardápio que já existe, e devolve o cursor à data inicial do destino. Quando o segmento de destino não é "todos", o cardápio só conta como ocupando o intervalo se existir também a composição daquele segmento para ele.

[?] A procura leva a data como chave, mas a conferência seguinte não compara a data limite lida de volta — compara só o tipo de órgão. O efeito exato da leitura pela chave, se ela exige a data exata ou apenas se posiciona no primeiro cardápio a partir dela, não está no acervo; é ele que decide se a tela recusa sempre que existe cardápio com aquela data limite, ou se compara mesmo os intervalos. Os dois comportamentos são compatíveis com o que o fonte mostra. Pergunta ao site.

### RN-07 — Quando as duas datas iniciais informadas são iguais, a conferência do destino não roda

Se a data inicial informada para o destino for igual à data inicial informada para a origem, a tela **não procura cardápios no intervalo de destino**: ela repõe a data inicial do destino com a data inicial do cardápio de origem e vai direto ao pedido de confirmação. Só quando as duas datas diferem é que a conferência do intervalo de destino (RN-06) roda.

[?] As duas datas iniciais coincidirem é justamente o caso em que o período de destino mais se parece com o de origem — e é o caso em que a tela deixa de conferir se ele já está ocupado. Ou a igualdade tem outro sentido (a data inicial digitada identifica o cardápio de origem, e não o período de destino), ou a conferência tem um buraco. Pergunta ao site; não concluo qual dos dois.

### RN-08 — A cópia só é pedida depois de confirmada, e um pedido pendente impede outro

Passadas todas as conferências, a tela mostra **\* Confirma copia dos cardapios <S/N> ? \*** e espera a resposta; só a resposta **S** leva ao registro. Junto com a resposta, os dois períodos e os dois segmentos informados têm de continuar iguais ao que a tela guardou; mudando qualquer um deles, a confirmação volta a ser pedida. Antes de registrar, a tela confere se já existe **solicitação de processamento pendente** para este mesmo processamento; existindo, recusa com **\* Relatorio em processamento. Aguarde. \*** e não registra nada.

[?] Responder **N** não cancela: a tela limpa a resposta, repõe o que já estava em tela e **volta a pedir a mesma confirmação**. Não há, no caminho lido, um desfecho que encerre a operação com a resposta negativa. Se o esperado é que N cancele, o caminho não cancela. Pergunta ao site.

[?] A tela registra a solicitação **sem marca de atendimento** e procura a pendente justamente pelas solicitações sem marca de atendimento; quem atende a solicitação — e a marca como atendida ou a remove — não está nos fontes desta jornada. Se ninguém a atender, o pedido de cópia só pode ser feito uma vez. O acervo não permite concluir qual dos dois. Pergunta ao site.

### RN-09 — O pedido recebe o número seguinte da fila e guarda quem pediu, quando e de onde

A solicitação é registrada na fila de processamento com o **número seguinte** ao último já usado, o código do processamento pedido, o tipo de órgão da sessão, a matrícula, a estação e o dia, o mês e o ano da sessão, e sem marca de atendimento. É esse número que identifica o pedido na fila.

### RN-10 — O processamento recebe os dois períodos e os dois segmentos

Junto com o pedido, a tela entrega ao processamento o tipo de órgão, as duas datas de cada período, os dois segmentos, a estação, a matrícula e o **e-mail** lido do cadastro do funcionário. É por essa entrega que o processamento sabe o que copiar e para onde.

[?] A entrega ao processamento depende de condições do ambiente — o produto em execução e o retorno da gravação — que o acervo desta jornada não explica; quando ela não acontece, o pedido fica registrado mas não é entregue. Pergunta ao site.

### RN-11 — Toda cópia pedida deixa rastro na auditoria

Cada pedido registra um lançamento na auditoria com o tipo de órgão, os dois períodos e os dois segmentos pedidos como valor anterior, o valor posterior em branco, a operação, a tela de origem, a matrícula, a estação e a data e a hora da sessão. O lançamento guarda **o que foi pedido**, não o que foi copiado.

### RN-12 — Só a atualização: qualquer outra opção é recusada

A tela abre no modo de atualização e exige esse modo. Se a opção que chega for outra, o sistema recusa com **\* Operacao nao disponivel. Use ALT \*** e devolve o cursor ao campo da opção, antes de ler qualquer cadastro; nesse caminho nada é lido e nada é registrado.

[?] A mensagem manda usar "ALT", mas a opção que a tela aceita é o código interno de alteração do sistema; nenhum valor "ALT" existe no acervo lido. Ou o formulário traduz o que o servidor digita para esse código, ou quem seguir a mensagem é recusado. Pergunta ao site.

[?] A recusa só é alcançável se a máscara oferecer ao servidor um campo de opção, e a abertura da tela repõe a atualização sozinha; a ficha da tela não lista campo de opção entre os rótulos. Se a máscara não tem esse campo, a recusa é trecho sem uso. Pergunta ao site.

### RN-13 — A digitação dos catorze campos numéricos é editada, e o cursor volta ao campo recusado

Os **catorze campos numéricos informados** — as quatro datas, em três partes cada, e os dois segmentos — passam por edição numérica antes de qualquer leitura: campo em branco é tratado como zero, o que não for número é recusado e o pedido não segue. O cursor volta ao campo recusado para **onze** deles; os três campos da data inicial de origem não têm posição de cursor.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não está nos fontes desta jornada: a rotina que faz a edição numérica não faz parte do acervo lido. Pergunta ao site.

### RN-14 — Ao reenviar, a tela apaga o resultado da apresentação anterior

Antes de conferir a digitação e de ler qualquer cadastro, a tela apaga os **cinco campos de resultado** da apresentação anterior — a descrição do tipo de órgão, a data do sistema, as descrições dos dois segmentos e a mensagem —, de modo que uma conferência recusada não deixa em tela o resultado da anterior. O cabeçalho recebe a data do sistema e a descrição do tipo de órgão; as descrições dos segmentos vêm do cadastro.

[?] Nem a data do sistema nem a descrição do tipo de órgão são preenchidas por nenhum caminho desta tela: ela copia as duas de áreas de trabalho que o acervo não declara, e a entrada guarda a descrição do tipo de órgão numa área com outro nome. Se o ambiente transporta o valor de uma área para a outra — e de onde vem a data do sistema —, o acervo não diz; se não transportar, os dois campos saem em branco. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Pedir a cópia dos cardápios de um período para outro

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C772T

  Cenário: Pedido de cópia dos cardápios de um período para outro
    Dado que informei o período de origem com uma data final que tem cardápio cadastrado
    E informei o período de destino e os dois segmentos
    Quando respondo S à confirmação
    Então vejo a mensagem "* Cadastro sendo atualizado *"
    E a solicitação de processamento é registrada
    E a operação fica registrada na auditoria

  Cenário: A tela não copia cardápio nenhum
    Dado que confirmo a cópia
    Então nenhum cardápio, segmento ou composição de cardápio é incluído, alterado ou excluído por esta tela
    E o que fica registrado é a solicitação de processamento e a auditoria

  Cenário: O pedido recebe o número seguinte da fila
    Dado que confirmo a cópia
    Então a solicitação é registrada com o número seguinte ao último já usado
    E fica sem marca de atendimento

  Cenário: O processamento recebe os dois períodos e os dois segmentos
    Dado que confirmo a cópia
    Então o processamento é entregue com o meu tipo de órgão, as duas datas de cada período, os dois segmentos, a estação, a matrícula e o meu e-mail

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

  Cenário: Data do período de destino inválida
    Quando informo uma data de início ou de fim do período de destino que não é uma data válida
    Então vejo "* Data inicial do cardapio invalida - PARA *" ou "* Data final do cardapio invalida - PARA *"
    E nada é registrado

  Cenário: Data inicial do destino maior que a final
    Quando informo a data inicial do destino maior que a data final
    Então vejo "* Data inicial maior que data final - PARA *"
    E nada é registrado

  Cenário: Data final do destino em dia da semana não permitido
    Dado que o cadastro de dias associa um dia ao meu tipo de órgão
    Quando informo uma data final de destino que não cai no dia anterior a esse dia
    Então vejo "* <- Data final deve ser este dia da semana *" com o dia exigido
    E nada é registrado

  Cenário: Sem dia associado ao meu tipo de órgão, a data final não é restringida
    Dado que o cadastro de dias não tem dia para o meu tipo de órgão
    Quando informo qualquer data final válida para o destino
    Então a tela aceita a data
    E segue para a conferência do intervalo de destino

  Cenário: Segmento de destino não informado
    Quando deixo o segmento de destino em branco
    Então vejo "* Informe segmento. Todos = 99 - PARA *"
    E o cursor volta ao campo do segmento de destino
    E nada é registrado

  Cenário: Segmento de origem não informado
    Quando deixo o segmento de origem em branco
    Então vejo "* Informe segmento. Todos = 99 - DE *"
    E o cursor volta ao campo do segmento de origem
    E nada é registrado

  Cenário: Segmento não cadastrado
    Quando informo um segmento que não consta do cadastro de segmentos
    Então vejo "* Segmento invalido - PARA *" ou "* Segmento invalido - DE *"
    E nada é registrado

  Cenário: "Todos" na origem força "todos" no destino
    Dado que informo 99 no segmento de origem
    Quando envio a tela
    Então o segmento de destino passa a ser 99, com a descrição "Todos"

  Cenário: Já existe cardápio com a data inicial do destino como data limite
    Dado que existe cardápio que cobre o intervalo de destino
    Quando envio a tela
    Então vejo "* <- Cardapios ja cadastrados neste intervalo *"
    E o cursor volta à data inicial do destino
    E nada é registrado

  Cenário: Já existe cardápio com a data final do destino como data limite
    Dado que existe cardápio que cobre o intervalo de destino, com a data final informada como data limite
    Quando envio a tela
    Então vejo "* <- Cardapios ja cadastrados neste intervalo *"
    E nada é registrado

  Cenário: Cardápio sem a composição do segmento pedido não bloqueia o pedido
    Dado que existe cardápio no intervalo de destino, mas sem composição para o segmento de destino informado
    Quando envio a tela
    Então a tela não recusa o intervalo por causa desse cardápio

  Cenário: As duas datas iniciais iguais dispensam a conferência do intervalo de destino
    Dado que informo a mesma data inicial para a origem e para o destino
    E já existe cardápio que cobre o intervalo de destino
    Quando envio a tela
    Então a tela segue para o pedido de confirmação, sem a recusa de intervalo ocupado

  Cenário: A confirmação vem antes de qualquer registro
    Dado que todas as conferências passaram
    Quando envio o pedido
    Então vejo "* Confirma copia dos cardapios <S/N> ? *"
    E nenhuma solicitação foi registrada ainda

  Cenário: A resposta negativa não cancela e não registra nada
    Dado que a tela pediu a confirmação
    Quando respondo N
    Então a tela volta a pedir a confirmação
    E nenhuma solicitação é registrada

  Cenário: Mudar um campo depois da confirmação faz a confirmação voltar
    Dado que a tela pediu a confirmação
    Quando mudo a data final do destino e respondo S
    Então a tela volta a conferir o pedido
    E volta a pedir a confirmação, sem registrar nada

  Cenário: Já existe pedido de cópia pendente
    Dado que existe solicitação de processamento pendente para este processamento
    Quando respondo S à confirmação
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E uma segunda solicitação não é registrada
    E o pedido pendente continua sendo o único

  Cenário: Opção diferente da atualização
    Dado que a opção informada não é a atualização
    Quando envio a tela
    Então vejo "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo da opção
    E nenhum cadastro é lido

  Cenário: Digitação não numérica nos campos informados
    Dado que digitei algo que não é número em um dos campos numéricos
    Quando envio a tela
    Então o sistema recusa a digitação antes de ler qualquer cadastro
    E o cursor volta ao campo recusado

  Cenário: O resultado da apresentação anterior é apagado
    Dado que a apresentação anterior mostrou as descrições e a mensagem
    Quando envio uma conferência que é recusada
    Então as descrições e a mensagem anteriores não ficam em tela

  Cenário: O cabeçalho mostra a data do sistema e o tipo de órgão da sessão
    Dado que entrei no sistema
    Quando abro a tela C772T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão
```
