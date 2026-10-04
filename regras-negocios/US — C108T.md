# US — C108T — Manter as refeições e a sobremesa do grupo de atendimento

## Estória

Como **servidor de CRE**, quero **definir quais refeições cada grupo de atendimento serve e em quais
delas há sobremesa**, para que **a oferta de alimentação daquele grupo fique montada e o mapa mensal
de atendimento tenha o que conferir**.

O grupo de atendimento é o recorte pelo qual a alimentação é oferecida: é sobre ele que se declara,
refeição por refeição, o que é servido. Enquanto a refeição não estiver ligada ao grupo, o grupo não
tem aquele item na oferta — e a marca de sobremesa só pode ser ligada onde a própria refeição já
prevê sobremesa. Sem essa ligação e essa marca, o mapa do mês não tem o que conferir: a quantidade de
refeições fica sem lastro e a de sobremesas é recusada.

## Contexto

Jornada S000M → C000M → C028M → C108T.

Ator: servidor de CRE — informa o grupo de atendimento, confere a oferta que ele já tem e liga,
desliga e marca a sobremesa de cada refeição.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu
a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio.

As duas telas antes desta — o `C000M` e o `C028M` — são menus, e a tela é aberta pela opção 6 do
`C028M`; não há encadeamento de tela de transação nesta jornada. O que a tela recebe delas é o
contexto da sessão: a matrícula, o acesso, a CRE e o tipo de órgão da secretaria escolhida no
`LOGON`. A opção de manutenção não é decidida pela tela anterior: a própria tela a guarda e a repõe,
e, sem nenhuma guardada, ela abre em consulta. Esta é a última tela da jornada: ela não entrega a
transação a nenhuma tela seguinte.

As regras abaixo são só as da **tela desta jornada**; as da entrada não se repetem aqui.

## Regras de negócio

### RN-01 — A tela mantém a oferta de refeições do grupo de atendimento

Para o tipo de órgão da secretaria, cada grupo de atendimento tem uma oferta: quais refeições ele
serve e, em cada uma delas, se há sobremesa. A tela é onde essa oferta se monta — ligar diz que o
grupo passou a servir aquela refeição; desligar, que deixou de servir —, e a marca de sobremesa é da
ligação, não da refeição: a mesma refeição pode ter sobremesa em um grupo e não em outro. O tipo de
órgão não se digita: é o da sessão, e é a chave de tudo o que a tela lê e grava.

### RN-02 — O cabeçalho identifica o grupo de atendimento e o segmento dele

Ao abrir, a tela mostra um grupo de atendimento do tipo de órgão da sessão — o primeiro — com a sua
descrição, e o segmento a que esse grupo pertence, também com a descrição. Mostra ainda a descrição
do tipo de órgão e a data do sistema. O segmento não se escolhe: o campo aceita o que for digitado e
passa pela conferência de número, mas é reescrito com o segmento do grupo de atendimento informado, e
é esse — não o digitado — que a tela usa em tudo o que lê e grava. Quando o tipo de órgão não tem
nenhum grupo de atendimento, não há oferta para mostrar.

### RN-03 — A grade mostra as refeições do tipo de órgão, doze por vez

A grade tem doze linhas. Cada linha traz o código e a descrição de uma refeição do tipo de órgão, a
marca de que aquele grupo a serve e a marca de sobremesa, cada uma delas por extenso, como Sim ou
Não. As refeições entram na ordem do código; a linha de uma refeição que o grupo já serve aparece
marcada, com a sobremesa que estiver gravada, e a das demais fica em branco.

[?] A lista é retomada a partir do código da última refeição mostrada; não dá para concluir, pela
fonte, se a página seguinte repete essa refeição ou passa direto para a próxima. Pergunta ao site.

### RN-04 — Sem refeição para mostrar, a tela avisa

Quando não encontra refeição nenhuma para mostrar, a tela avisa
"* Grupo sem refeicoes cadastradas *" e a operação termina ali.

[?] O aviso fala do grupo, mas a leitura que o produz é a das refeições do tipo de órgão: não dá para
concluir, pela fonte, se ele aparece quando o tipo de órgão não tem refeição nenhuma ou quando o
grupo não tem nenhuma refeição ligada. Pergunta ao site.

### RN-05 — A tela abre em consulta

A opção de manutenção é a que a própria tela guardou do uso anterior na mesma sessão; sem nenhuma
guardada, ela abre em consulta — e a opção informada é conservada para a mensagem seguinte.

### RN-06 — A opção de manutenção só aceita alteração e consulta

Qualquer opção diferente de alteração e de consulta é recusada com "* Operacao nao disponivel *", e o
cursor volta para o campo da opção.

[?] A recusa é dada na conferência, mas quem interromperia a gravação é a rotina comum do sistema,
que marca a falha — e o trecho que emite a recusa não a marca. Não é possível concluir, pela fonte,
se depois de uma recusa a gravação ainda acontece; a dúvida vale para todas as recusas desta tela: a
opção, o grupo e a sobremesa. Pergunta ao site.

### RN-07 — Para alterar, o grupo de atendimento tem de ser o que está em tela

A alteração vale só para o grupo que a tela já está mostrando — o que a consulta anterior trouxe.
Informando outro grupo, a tela recusa com "* Consulte antes de atualizar *", e o cursor volta para o
campo do grupo. Alterar é, portanto, um segundo passo: primeiro se consulta o grupo, depois se
altera.

### RN-08 — Para consultar, o grupo de atendimento tem de ser informado e existir

Na consulta o grupo tem de vir preenchido; em branco, a tela avisa
"* Informe o grupo de atendimento *", com o cursor no campo. Informado, ele tem de existir entre os
grupos daquele tipo de órgão; não existindo, "* Grupo de atendimento nao cadastrado *". Existindo, a
tela passa a mostrar aquele grupo, com o segmento dele e as refeições que ele já serve.

### RN-09 — A marca de situação é por linha, e só Sim e Não valem

A marca de que o grupo serve a refeição é da linha, não da tela: Sim liga a refeição ao grupo e Não
desliga. Linha sem código de refeição é ignorada, e marca diferente de Sim e de Não também — em
silêncio, sem mensagem.

### RN-10 — Ligar uma refeição nova ao grupo

A refeição marcada com Sim e ainda não ligada àquele grupo passa a fazer parte da oferta dele. Nessa
ligação, a sobremesa só é gravada como Sim se a linha a pedir; qualquer outra coisa é gravada como
Não.

### RN-11 — Marcar a refeição que o grupo já serve só acerta a sobremesa

Marcar Sim em uma refeição que o grupo já serve não duplica nada: a tela compara a sobremesa pedida
com a gravada e só grava quando ela muda; sendo a mesma, nada acontece.

### RN-12 — Só se marca sobremesa em refeição que a tem

A sobremesa de uma linha só pode ser Sim se a própria refeição estiver cadastrada como refeição com
sobremesa. Não estando, a tela recusa com "* Refeicao nao cadastrada para sobremesa *" e deixa o
cursor na marca de sobremesa da linha. A conferência só olha as linhas marcadas para servir.

### RN-13 — Desligar uma refeição do grupo

A refeição marcada com Não e ligada àquele grupo sai da oferta dele. Se não estava ligada, nada
acontece: a desligação não pede sobremesa e não avisa.

### RN-14 — A consulta não grava, e pedir o grupo seguinte também não

Na consulta a tela só lê e exibe: a passagem que grava sai antes de tocar na oferta. O campo que pede
o grupo seguinte também não grava: com ele preenchido, nenhuma linha da mensagem é executada e a tela
passa a trabalhar com o grupo seguinte ao informado — ou com o primeiro, quando não há seguinte.

### RN-15 — Toda gravação deixa rastro na auditoria

Cada ligação, cada troca de sobremesa e cada desligação monta antes o registro da trilha de auditoria
(A010T), com o tipo de órgão, a matrícula, a CRE, a estação, a data e a hora, o cadastro de origem, a
operação e os valores antes e depois — e só então executa a gravação. A ligação leva o "antes" em
branco; a desligação, o "depois" em branco; a troca de sobremesa leva os dois.

[?] Na ligação, a montagem desse rastro está condicionada a um estado do banco de dados que o acervo
não define. A rotina de gravação limpa esse estado imediatamente antes de gravar, de modo que, pela
fonte, o rastro é montado; mas, se o banco o devolver, a ligação fica sem rastro, ainda que a troca
de sobremesa e a desligação deixem. Pergunta ao site.

### RN-16 — A tela grava em dois cadastros e lê quatro

A tela liga, desliga e troca a sobremesa somente no cadastro da ligação entre grupo de atendimento,
segmento e refeição (C109T), e grava também a trilha de auditoria (A010T). Os outros cadastros que
ela enxerga — o das telas do sistema (S030T), o dos grupos de atendimento (C103T), o dos segmentos
(C160T) e o das refeições (C100T) — são apenas lidos. Para cada cadastro que enxerga, o sistema traz
prontas as operações de gravar, apagar e travar; trazer pronto não é usar: das operações que a tela
executa, ela grava em dois cadastros.

### RN-17 — A operação passa pela conferência de acesso

Antes de conferir a mensagem, a operação pretendida é conferida contra o perfil de acesso do usuário
àquela tela: consultar exige apenas o acesso à tela; alterar exige, além dele, a autorização de
alteração no código de acesso. Sem a permissão, a operação para ali, e nada é conferido nem gravado.

### RN-18 — O campo que pede outra tela encerra a conferência sem nenhuma recusa

O primeiro teste da conferência da mensagem é o campo que pede outra tela. Chegando vazio, a tela
confere tudo o que está descrito acima; chegando preenchido, ela sai da conferência sem produzir
nenhuma recusa — nem a da opção, nem a do grupo, nem a da sobremesa. Quem lê esse campo antes é a
rotina de encaminhamento do sistema, que passa a mensagem para a tela pedida e marca a falha; e é a
falha marcada que impede a gravação. Esta tela não pede nenhuma tela seguinte por conta própria:
nesta jornada ela é a última.

[?] A guarda da própria tela fica depois da rotina de encaminhamento e, pela fonte, não decide nada:
com o campo preenchido já não se chega a ela, e, sem ele, ela deixa passar. Se a falha marcada pela
rotina de encaminhamento for desmarcada adiante — a rotina que a atende não tem fonte neste acervo —,
a gravação acontece sem nenhuma das conferências. Pergunta ao site.

### RN-19 — Falha no banco interrompe a operação

Todo acesso ao banco testa o erro: o erro de leitura e o de gravação são levados à rotina de
comunicação do sistema, e a operação para ali, sem completar o resto.

### RN-20 — Os códigos informados são numéricos

O código do grupo de atendimento, o do segmento e o da refeição passam pela edição numérica antes de
qualquer conferência de negócio: o que não for número é recusado no próprio campo, com o cursor
deslocado para ele, e não chega a ser conferido.

## Cenários BDD

```gherkin
Funcionalidade: Manter as refeições e a sobremesa do grupo de atendimento

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C108T

  Cenário: RN-01, RN-02, RN-03 e RN-05 — abrir a tela em consulta
    Dado que abro a tela C108T sem informar a opção de manutenção
    Então vejo, no cabeçalho, a descrição do tipo de órgão da minha secretaria, a data do sistema, o grupo de atendimento com a sua descrição e o segmento do grupo com a sua descrição
    E vejo, em cada uma das doze linhas, o código e a descrição da refeição, a marca de sobremesa e a marca de que o grupo serve a refeição, cada uma por extenso, como Sim ou Não
    E as refeições que o grupo já serve aparecem marcadas, e as demais em branco
    E nada é gravado

  Cenário: RN-02 — o segmento do cabeçalho vem do grupo de atendimento
    Dado que estou na tela C108T mostrando um grupo de atendimento
    Quando digito outro código de segmento no cabeçalho e confirmo
    Então o segmento mostrado continua sendo o do grupo de atendimento
    E a oferta mostrada continua sendo a do mesmo grupo

  Cenário: RN-04 — sem refeição para mostrar
    Dado que não há refeição nenhuma para a tela listar
    Quando abro a tela C108T
    Então vejo "* Grupo sem refeicoes cadastradas *"

  Cenário: RN-06 — opção de manutenção não disponível
    Dado que estou na tela C108T
    Quando informo uma opção de manutenção diferente de alteração e de consulta
    Então vejo "* Operacao nao disponivel *"
    E o cursor volta para o campo da opção

  Cenário: RN-07 — alterar um grupo que não está em tela
    Dado que estou na tela C108T com a opção de alteração
    Quando informo um grupo de atendimento diferente do que está em tela e confirmo
    Então vejo "* Consulte antes de atualizar *"
    E o cursor volta para o campo do grupo

  Cenário: RN-08 — consultar sem informar o grupo
    Dado que estou na tela C108T com a opção de consulta
    Quando apago o grupo de atendimento e confirmo
    Então vejo "* Informe o grupo de atendimento *"
    E o cursor fica no campo do grupo

  Cenário: RN-08 — consultar um grupo que não existe
    Dado que estou na tela C108T com a opção de consulta
    Quando informo um grupo de atendimento que o tipo de órgão não tem
    Então vejo "* Grupo de atendimento nao cadastrado *"
    E nada é gravado

  Cenário: RN-08 — consultar outro grupo existente
    Dado que estou na tela C108T com a opção de consulta
    Quando informo um grupo de atendimento que existe no tipo de órgão e confirmo
    Então a tela passa a mostrar esse grupo, o segmento dele e as refeições que ele serve
    E nada é gravado

  Cenário: RN-09 — linha sem código de refeição ou com marca desconhecida
    Dado que preencho uma linha sem o código da refeição, ou com uma marca diferente de Sim e de Não
    Quando confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada

  Cenário: RN-10, RN-15 e RN-16 — ligar uma refeição nova ao grupo
    Dado que estou na tela C108T com a opção de alteração
    E a refeição ainda não está ligada a esse grupo
    Quando marco a linha com Sim e confirmo
    Então a refeição passa a fazer parte da oferta do grupo
    E a operação fica registrada na auditoria

  Cenário: RN-10 — ligar uma refeição sem pedir sobremesa
    Dado que estou na tela C108T com a opção de alteração
    Quando marco a linha com Sim e deixo a marca de sobremesa em branco, e confirmo
    Então a refeição fica ligada ao grupo, sem sobremesa

  Cenário: RN-11 — marcar Sim em uma refeição que o grupo já serve, com a mesma sobremesa
    Dado que a refeição já está ligada ao grupo
    Quando marco a linha com Sim e mantenho a mesma marca de sobremesa, e confirmo
    Então nada muda e nada é gravado

  Cenário: RN-11 e RN-15 — trocar a sobremesa de uma refeição já ligada
    Dado que a refeição já está ligada ao grupo
    Quando marco a linha com Sim e troco a marca de sobremesa, e confirmo
    Então a nova marca passa a valer para essa ligação
    E a operação fica registrada na auditoria

  Cenário: RN-12 — marcar sobremesa em refeição que não a tem
    Dado que estou na tela C108T com a opção de alteração
    E a refeição não está cadastrada como refeição com sobremesa
    Quando marco a linha com Sim e a sobremesa com Sim, e confirmo
    Então vejo "* Refeicao nao cadastrada para sobremesa *"
    E o cursor fica na marca de sobremesa da linha

  Cenário: RN-13 e RN-15 — desligar uma refeição do grupo
    Dado que a refeição está ligada ao grupo
    Quando marco a linha com Não e confirmo
    Então a refeição sai da oferta do grupo
    E a operação fica registrada na auditoria

  Cenário: RN-13 — desligar uma refeição que não estava ligada
    Dado que a refeição não está ligada ao grupo
    Quando marco a linha com Não e confirmo
    Então nada é apagado e nenhuma mensagem é mostrada

  Cenário: RN-14 — a consulta não grava nada
    Dado que estou na tela C108T com a opção de consulta
    E preencho linhas com Sim e com Não
    Quando confirmo
    Então nada é gravado

  Cenário: RN-14 — pedir o grupo seguinte não grava nada
    Dado que estou na tela C108T e o grupo em tela não é o último do tipo de órgão
    Quando preencho o campo que pede o grupo seguinte e confirmo
    Então a tela passa a mostrar o grupo seguinte, com as refeições que ele serve
    E nada é gravado

  Cenário: RN-17 — operação de alteração sem autorização
    Dado que o meu perfil de acesso não tem a autorização de alteração nesta tela
    Quando confirmo com a opção de alteração
    Então a operação não é executada
    E nada é gravado

  Cenário: RN-19 — falha no banco durante a gravação
    Dado que a gravação da oferta falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E a ligação não é considerada gravada

  Cenário: RN-20 — código não numérico
    Quando preencho o grupo, o segmento ou a refeição com letra
    Então a tela recusa o campo antes de qualquer conferência
    E nada é gravado
```
