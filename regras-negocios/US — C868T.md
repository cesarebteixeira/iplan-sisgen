# US — C868T — Copiar os planejamentos de uma origem para a estimativa de outro período

## Estória

Como **servidor de CRE**, quero **pedir que o planejamento já cadastrado de um
período, de um grupo, de uma semana e de um segmento seja aproveitado na estimativa
de outro período**, para que a estimativa do período novo não precise ser remontada
dia a dia, semana a semana, segmento a segmento e grupo a grupo.

A alimentação escolar é planejada por período: para cada semana e cada dia há um
cardápio previsto, e há também as quantidades de cada mês. Quando o período que vem
repete o desenho do anterior, esse trabalho é o mesmo — e sem esta tela cada grupo,
cada semana e cada segmento teriam de ser refeitos à mão. O pedido não é a cópia: a
tela recolhe a origem, o destino, o que copiar e a confirmação, e é o processamento
do sistema que copia.

## Contexto

Jornada S000M → C000M → C800M → C811M → C868T.

Ator: servidor de CRE — pede que o planejamento já cadastrado de um período seja
aproveitado na estimativa de outro, escolhendo a secretaria, o grupo, a semana e o
segmento de cada lado.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As três telas do meio do caminho são **menus** — o `C000M`, o `C800M` e a `C811M` —,
e nenhuma delas passa registro nem operação para esta: elas apenas chamam a tela pelo
nome. A `C868T` abre sozinha, **sempre no modo de alteração**, e o que ela usa da
sessão — a matrícula, o código de acesso, o privilégio, a secretaria, o grupo do
usuário e a data do sistema — foi deixado pela entrada. No fonte da tela não há
comparação com a tela de origem: o comportamento dela não muda conforme quem a chamou.

A tela também não encadeia em outra: terminado o pedido ela **reabre a si mesma**,
primeiro para mostrar a pergunta de confirmação e depois para avisar que o cadastro
está sendo atualizado. O que ela entrega não vai para uma tela seguinte, e sim para o
processamento do sistema: o pedido com as duas secretarias, os dois grupos, as duas
semanas, os dois segmentos, as quatro datas, a indicação do que copiar e a impressora.

As regras abaixo são só as da tela desta jornada. As da entrada estão no documento
dela; a que se revelou pertencer à entrada está registrada no **anexo de evidências**,
na seção própria.

---

## Regras de negócio

### RN-01 — A tela pede a cópia dos planejamentos para a estimativa de outro período

A tela trabalha com **dois lados**. No lado **de origem** ficam a **secretaria**, o
**grupo**, a **semana**, o **segmento** e o **período** do planejamento que será
aproveitado. No lado **de destino** ficam a **secretaria**, o **grupo**, a **semana**,
o **segmento** e o **período** da estimativa que vai recebê-lo. A tela confere os dois
lados, pergunta a confirmação e, só com a resposta afirmativa, registra o pedido e o
entrega ao processamento do sistema.

Quem copia não é a tela: ela não inclui, não altera e não exclui planejamento nem
cardápio nenhum (RN-15). Ela recolhe o pedido, confirma e dispara; o resultado não
volta para ela — o servidor vê **\* Cadastro sendo atualizado \*** e acompanha depois.

[?] Os fontes desta jornada mostram o que a tela entrega ao processamento e onde o
pedido é registrado, mas não o processamento em si: se ele copia mesmo o planejamento
da origem para a estimativa de destino, o que faz com o que já existe no destino e
como o período novo é preenchido são perguntas ao site.

### RN-02 — A tela abre na secretaria do usuário e com a data do sistema; a secretaria de destino é obrigatória e tem de existir

Ao abrir, a tela mostra a **data do sistema** e a **descrição da secretaria do
usuário**, e preenche os dois lados com essa mesma secretaria; os dois marcadores do
que copiar já vêm desmarcados. Os nomes de secretaria mostrados vêm do cadastro de
secretarias, não do que foi digitado.

A **secretaria de destino** é de preenchimento obrigatório: em branco, a recusa é
**\* Informe a Secretaria - PARA \***; informada, tem de constar do cadastro, senão a
recusa é **\* Secretaria nao cadastrada - PARA \***. Nas duas o cursor volta ao campo
da secretaria de destino e nada é gravado.

[?] A secretaria de origem não tem recusa própria: não há "informe a secretaria de
origem" nem "secretaria de origem não cadastrada". Ela vem preenchida com a do usuário
e, quando não consta do cadastro, a tela segue sem mensagem própria — o que o servidor
vê nesse caso depende das conferências seguintes, e o fonte não permite concluir qual
é. Também não se pode concluir do fonte se o servidor tem de manter a secretaria de
origem na dele ou se pode trocá-la. Pergunta ao site.

### RN-03 — A tela só opera em modo de alteração

A tela se apresenta sempre no modo de alteração. Acionada em qualquer outro modo de
manutenção, a operação é recusada com **\* Opcao nao disponivel. Use ALT \***, o cursor
volta ao campo do modo e nada é gravado.

[?] A recusa manda usar ALT e a conferência aceita apenas o código de alteração; o
acervo não traz a correspondência entre a tecla e o código. Ou o terminal traduz a
tecla antes de enviar, ou a mensagem está desalinhada da conferência. Pergunta ao
site.

### RN-04 — Os dois grupos; o código 99 só vale na origem

Cada lado tem o seu **grupo** — a coordenação regional escolar, em dois dígitos. Os
dois são obrigatórios: sem o grupo de origem a recusa é **\* Informe o grupo - DE \***;
sem o de destino, **\* Informe o grupo - PARA \***. E os dois têm de constar do
cadastro de grupos: senão, **\* Grupo nao cadastrado - DE \*** ou
**\* Grupo nao cadastrado - PARA \***. Em qualquer das recusas o cursor volta ao grupo
recusado e nada é gravado.

O código **99** só é aceito no grupo de origem: informado lá, o grupo de destino
assume 99 sozinho; informado apenas no destino, a recusa é
**\* Nao use 99 para esta opcao - PARA \***. Com 99 a tela não procura o planejamento
daquele grupo — procura o do período inteiro (RN-09).

[?] O que o código 99 significa em negócio — "todos os grupos" ou outro conjunto — não
está no corpus desta jornada nem no dicionário de dados. O que se pode afirmar é só o
que a tela faz com ele: dispensa a procura pelo grupo e obriga o outro lado a também
ser 99. Pergunta ao site.

[?] No grupo de origem, o caminho do 99 dispensa a consulta ao cadastro, mas deixa a
decisão de seguir para uma marca que este caminho não prepara antes de consultá-la: se
a sessão a deixou posta, o 99 passa e o destino assume 99; se não, a tela recusa como
grupo não cadastrado. O fonte não permite escolher entre os dois desfechos. Pergunta
ao site.

### RN-05 — As duas semanas; a letra T só vale na origem

Cada lado tem a sua **semana** — a letra do cardápio semanal. O valor aceito é uma das
letras **A, B, C ou D**; qualquer outra coisa é recusada com
**\* Informe a semana A / B / C / D - DE \*** ou
**\* Informe a semana A / B / C / D - PARA \***, com o cursor na semana recusada e
nada gravado.

A letra **T** só é aceita na semana de origem: informada lá, a semana de destino
assume T sozinha; informada apenas no destino, a recusa é
**\* Nao use T para esta opcao - PARA \***.

[?] O que a letra T abrange — todas as semanas do período ou uma semana a mais do
conjunto — não está no corpus nem no dicionário de dados. Pergunta ao site.

[?] A semana informada não participa de procura nenhuma da tela: ela é conferida e
enviada no pedido, e quem a usa é o processamento. O fonte não diz se ela deveria
restringir o planejamento copiado. Pergunta ao site.

### RN-06 — Os dois segmentos; o código 99 só vale na origem

Cada lado tem o seu **segmento** — o segmento de atendimento da alimentação escolar.
Os dois são obrigatórios e têm de constar do cadastro de segmentos da secretaria: sem
o de origem a recusa é **\* Informe o segmento - DE \***; sem o de destino,
**\* Informe o segmento - PARA \***; não constando, **\* Segmento nao cadastrado - DE
\*** ou **\* Segmento nao cadastrado - PARA \***. O código **99** só é aceito no
segmento de origem: informado lá, o segmento de destino assume 99 sozinho; informado
apenas no destino, a recusa é **\* Nao use 99 para esta opcao - PARA \***. Em qualquer
das recusas o cursor volta ao campo recusado e nada é gravado.

[?] O que o 99 abrange no segmento — todos os segmentos da secretaria ou só os que têm
planejamento — não está no corpus. Pergunta ao site.

[?] Como a semana, o segmento informado não participa de procura nenhuma desta tela: é
conferido contra o cadastro e enviado no pedido. O fonte não diz se ele deveria
restringir o planejamento copiado. Pergunta ao site.

### RN-07 — Cada período é informado pela sua data limite; as datas de início vêm dos cardápios

Cada um dos dois períodos é informado pela sua **data limite**, em dia, mês e ano. As
**datas de início** que a tela mostra não são as digitadas: a do período de origem é a
data de início do cardápio achado para aquele período, e a do período de destino é a
do cardápio achado para o período novo (RN-08). O que o servidor houver digitado nelas
é substituído antes de a tela pedir a confirmação.

As doze partes numéricas das quatro datas passam pela conferência numérica do sistema
antes de qualquer consulta: campo em branco vira zero e o que não for número é
recusado antes de o cadastro ser lido. Nenhuma das quatro datas passa pelo calendário:
a tela não confere se o dia existe no mês nem faixa de ano — o que ela aceita é só o
número.

[?] Das dezoito posições que a tela confere como número, sete não têm posição de
cursor: a secretaria de origem e as duas datas de início — dia, mês e ano de cada uma.
Quando o servidor digita nelas algo que não é número, a tela recusa o campo mas não
sabe onde pôr o cursor. Também não há, para as datas de início, conferência de
calendário nem comparação com a data limite: se isso é intencional, o fonte não diz.
Pergunta ao site.

### RN-08 — Cada período precisa de um cardápio de estimativa cadastrado na sua data limite

Para cada lado, a tela procura no cadastro de cardápios de estimativa o cardápio
daquela secretaria que termina na **data limite** informada. Não achando no período de
origem, a recusa é **\* Cardapios nao cadastrados para esta data - DE \***, com o
cursor no dia limite desse período; não achando no período de destino, a recusa é
**\* Cardapios nao cad. para esta data - PARA \***, com o cursor no dia limite do
período novo. Em qualquer dos casos nada é gravado. Achando, a data de início daquele
cardápio é a que a tela passa a mostrar e a que vai no pedido.

[?] A procura do cardápio é feita com o código do cardápio zerado, e do que ela acha a
tela só compara a secretaria e as três partes da data limite — o código do cardápio
não é reconferido. O que os modificadores da leitura fazem não está no corpus nem no
manual: se a leitura for a de uma chave exata, só o cardápio de código zero serve; se
ela apenas se posicionar, serve qualquer cardápio daquela secretaria que termine na
data limite. Não escolho entre os dois desfechos. Pergunta ao site.

### RN-09 — O que copiar: o planejamento por dia da semana e o planejamento sazonal

A tela pede ao servidor que diga **o que copiar**: o planejamento por dia da semana, o
planejamento sazonal (as quantidades por mês), ou os dois. Sem nenhum dos dois
marcado, a recusa é **\* Informe planejamento a copiar \***, com o cursor no campo do
planejamento, e nada é gravado.

Para cada um que estiver marcado, o sistema confere se ele existe no **período de
origem**, na data limite e no grupo informados. Não achando o planejamento por dia da
semana, a recusa é **\* Planejamentos nao cadastrados - DE \***; não achando o
sazonal, **\* Planejamentos sazonais nao cad. - DE \***. Nas duas o cursor volta ao
dia limite do período de origem e nada é gravado. A conferência do **sazonal**,
porém, só é feita quando a do planejamento por dia da semana **não** foi pedida: com
os dois marcados, o caminho que achou o primeiro segue direto para a conferência da
impressora.

[?] O fonte não diz se essa dispensa é intencional: ou o sazonal não precisa existir
para ser copiado, ou a conferência ficou inalcançável nesse caso. Pergunta ao site.

[?] As duas procuras olham a secretaria, a data limite e — fora o 99 — o grupo. A
semana e o segmento informados não entram nelas, e a refeição não é informada na tela:
pode haver planejamento para o grupo e não para a semana ou o segmento pedidos, e a
recusa é mais grossa do que a mensagem sugere. O que os modificadores da leitura fazem
não está no corpus. Pergunta ao site.

### RN-10 — A impressora é obrigatória

A cópia sai impressa, e o destino da impressão é informado na tela. Sem a impressora,
a recusa é **\* Informe a impressora \***, com o cursor no campo da impressora, e nada
é gravado.

### RN-11 — A cópia só segue depois de confirmada, e com os dados inalterados

Passadas as conferências, a tela repõe os dois lados na tela e pergunta
**\* Confirma copia dos planejamentos <S/N> ? \***, com o cursor no campo da resposta.
Só a resposta afirmativa segue para o registro.

Junto com a resposta, os dados informados têm de continuar iguais aos que a tela
guardou — a secretaria, o grupo, a semana, o segmento e a data limite do período de
destino, e o grupo, a semana, o segmento e a data limite do período de origem.
Alterado qualquer um deles, a tela não aproveita a resposta: refaz as conferências e
pergunta de novo.

[?] Responder N — ou deixar a resposta em branco — não cancela o pedido: a tela limpa
a resposta e volta às conferências, que pedem a mesma confirmação outra vez. Não há,
no caminho lido, um desfecho que encerre a operação com a resposta negativa. Pergunta
ao site.

[?] A comparação dos "dados inalterados" olha **treze** dados e não olha **dez**:
ficam de fora a secretaria de origem, as duas datas de início (seis partes) e os três
campos que dizem o que copiar e para onde imprimir. Trocá-los entre a pergunta e a
resposta não faz a tela refazer as conferências, e o pedido segue com o que estiver em
tela. O fonte não diz se é proposital. Pergunta ao site.

### RN-12 — Um pedido pendente deste relatório impede outro

Antes de registrar, o sistema procura uma **solicitação de processamento pendente**
deste mesmo serviço; existindo, a recusa é **\* Relatorio em processamento. Aguarde.
\***, a confirmação é desfeita e nada é registrado. O pedido só pode ser feito quando
não há outro em andamento.

[?] A procura olha só o código do serviço, sem examinar a secretaria nem a situação do
pedido: um pedido de outra secretaria, ou um já atendido e ainda não retirado, também
bloqueia. E a própria tela registra o pedido **sem marcar a situação** — quem o marca
como atendido, ou o remove, não está nos fontes desta jornada. Se ninguém o retirar, a
cópia só pode ser pedida uma vez. Pergunta ao site.

### RN-13 — A tela registra o pedido e entrega o serviço ao processamento

Confirmada a operação, a tela grava a **solicitação de processamento** com o número
seguinte da fila, o código do serviço, a **secretaria de origem**, a data, a matrícula
e a estação da sessão, e entrega o serviço ao processamento com os parâmetros do
pedido — as duas secretarias, os dois grupos, as duas semanas, os dois segmentos, as
quatro datas, a indicação do que copiar, a impressora, uma cópia e o e-mail cadastrado
do servidor. Em seguida avisa **\* Cadastro sendo atualizado \***. A tela não espera
pelo resultado.

[?] A entrega do serviço depende de indicadores do ambiente — o produto em execução e
o retorno da gravação — cujo valor e origem não estão nos fontes desta jornada: quando
ela não acontece, o pedido fica registrado mas o serviço não é entregue. Pergunta ao
site.

[?] O número do pedido é o seguinte ao último já usado na fila; a tela não escolhe o
número sozinha, ela o lê da fila e incrementa. Se duas sessões pedirem ao mesmo tempo,
o fonte desta jornada não permite dizer o que acontece. Pergunta ao site.

### RN-14 — Toda cópia confirmada deixa rastro na auditoria

Antes do pedido, a tela grava o **registro de auditoria** da operação: a tela, a
operação de inclusão, a data e a hora da sessão, a secretaria, o grupo e o acesso da
sessão, a matrícula e a estação, com os **parâmetros do pedido** guardados como valor
anterior e o valor posterior vazio.

[?] O número do processo da auditoria recebe o **dia** da data de início do período de
destino; o fonte não explica a escolha. Pergunta ao site.

### RN-15 — A tela não inclui, não altera e não exclui cadastro nenhum

A tela apenas **lê** os cadastros de que precisa — o de secretarias, o de grupos, o de
segmentos, o de cardápios de estimativa e os dois de planejamento. As rotinas de
gravação, de exclusão e de travamento existem declaradas para os **dez** cadastros que
a tela enxerga, mas **só duas gravações são executadas**: a da solicitação de
processamento e a da auditoria. Não há nenhuma exclusão e nenhum travamento. Declarar
não é executar.

---

## Cenários BDD

```gherkin
Funcionalidade: Copiar os planejamentos de uma origem para a estimativa de outro período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C868T

  Cenário: RN-01, RN-02, RN-07, RN-08, RN-09, RN-11, RN-13 e RN-14 — copiar o planejamento por dia da semana para a estimativa de outro período
    Dado que estou na tela C868T, na minha secretaria
    E os dois períodos que vou informar têm cardápio de estimativa cadastrado terminando na data limite que vou informar
    E existe planejamento por dia da semana para o grupo e o período de origem
    Quando informo as duas secretarias, os dois grupos, as duas semanas, os dois segmentos, as duas datas limite e a impressora, e marco a cópia do planejamento por dia da semana
    E envio os dados
    Então vejo "* Confirma copia dos planejamentos <S/N> ? *"
    Quando respondo S
    Então vejo "* Cadastro sendo atualizado *"
    E a solicitação de processamento fica registrada com as duas secretarias, os dois grupos, as duas semanas, os dois segmentos, as quatro datas, a impressora e o que copiar
    E a operação fica registrada na auditoria
    E nenhum planejamento é incluído, alterado ou excluído por esta tela

  Cenário: RN-09 e RN-13 — copiar o planejamento sazonal
    Dado que estou na tela C868T e os dois períodos têm cardápio de estimativa na data limite que vou informar
    E existe planejamento sazonal para o grupo e o período de origem
    E não marco a cópia do planejamento por dia da semana
    Quando informo os dois lados com o grupo, a semana, o segmento e as datas limite, marco a cópia do planejamento sazonal e informo a impressora
    E envio os dados
    Então vejo "* Confirma copia dos planejamentos <S/N> ? *"
    Quando respondo S
    Então vejo "* Cadastro sendo atualizado *"
    E o pedido registrado pede a cópia do planejamento sazonal

  Cenário: RN-02 — a tela abre na minha secretaria e com a data do sistema
    Dado que entrei com um usuário de uma secretaria
    Quando a tela C868T abre
    Então vejo a data do sistema
    E os dois lados vêm preenchidos com a minha secretaria e com o nome dela
    E os dois marcadores do que copiar vêm desmarcados

  Cenário: RN-02 — secretaria de destino em branco
    Dado que estou na tela C868T
    Quando deixo a secretaria de destino em branco
    Então vejo "* Informe a Secretaria - PARA *"
    E o cursor volta ao campo da secretaria de destino
    E nada é gravado

  Cenário: RN-02 — secretaria de destino não cadastrada
    Dado que estou na tela C868T
    Quando informo uma secretaria de destino que não existe no cadastro
    Então vejo "* Secretaria nao cadastrada - PARA *"
    E o cursor volta ao campo da secretaria de destino
    E nada é gravado

  Cenário: RN-03 — modo de manutenção diferente de alteração
    Dado que estou na tela C868T
    Quando aciono a tela em um modo de manutenção diferente de ALT
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo do modo de manutenção
    E nada é gravado

  Cenário: RN-04 — grupo de origem em branco
    Dado que estou na tela C868T
    Quando deixo o grupo de origem em branco
    Então vejo "* Informe o grupo - DE *"
    E o cursor volta ao campo do grupo de origem
    E nada é gravado

  Cenário: RN-04 — grupo de destino em branco
    Dado que estou na tela C868T
    E informei o grupo de origem
    Quando deixo o grupo de destino em branco
    Então vejo "* Informe o grupo - PARA *"
    E o cursor volta ao campo do grupo de destino
    E nada é gravado

  Cenário: RN-04 — grupo de origem não cadastrado
    Dado que estou na tela C868T
    Quando informo, no grupo de origem, um código que não existe no cadastro de grupos da secretaria de origem
    Então vejo "* Grupo nao cadastrado - DE *"
    E o cursor volta ao campo do grupo de origem
    E nada é gravado

  Cenário: RN-04 — grupo de destino não cadastrado
    Dado que estou na tela C868T e informei um grupo de origem cadastrado
    Quando informo, no grupo de destino, um código que não existe no cadastro de grupos da secretaria de destino
    Então vejo "* Grupo nao cadastrado - PARA *"
    E o cursor volta ao campo do grupo de destino
    E nada é gravado

  Cenário: RN-04 — o código 99 informado só no destino, no grupo
    Dado que estou na tela C868T
    E informei no grupo de origem um código diferente de 99
    Quando informo 99 no grupo de destino
    Então vejo "* Nao use 99 para esta opcao - PARA *"
    E o cursor volta ao campo do grupo de destino
    E nada é gravado

  Cenário: RN-05 — semana de origem inválida
    Dado que estou na tela C868T
    Quando informo, na semana de origem, algo que não é A, B, C, D nem T
    Então vejo "* Informe a semana A / B / C / D - DE *"
    E o cursor volta ao campo da semana de origem
    E nada é gravado

  Cenário: RN-05 — semana de destino inválida
    Dado que estou na tela C868T e informei a semana de origem
    Quando informo, na semana de destino, algo que não é A, B, C, D nem T
    Então vejo "* Informe a semana A / B / C / D - PARA *"
    E o cursor volta ao campo da semana de destino
    E nada é gravado

  Cenário: RN-05 — a letra T informada só no destino
    Dado que estou na tela C868T
    E informei, na semana de origem, uma letra entre A, B, C e D
    Quando informo T na semana de destino
    Então vejo "* Nao use T para esta opcao - PARA *"
    E o cursor volta ao campo da semana de destino
    E nada é gravado

  Cenário: RN-06 — segmento de origem em branco
    Dado que estou na tela C868T
    Quando deixo o segmento de origem em branco
    Então vejo "* Informe o segmento - DE *"
    E o cursor volta ao campo do segmento de origem
    E nada é gravado

  Cenário: RN-06 — segmento de destino em branco
    Dado que estou na tela C868T
    E informei o segmento de origem
    Quando deixo o segmento de destino em branco
    Então vejo "* Informe o segmento - PARA *"
    E o cursor volta ao campo do segmento de destino
    E nada é gravado

  Cenário: RN-06 — segmento de origem não cadastrado
    Dado que estou na tela C868T
    Quando informo, no segmento de origem, um código que não existe no cadastro de segmentos da secretaria de origem
    Então vejo "* Segmento nao cadastrado - DE *"
    E o cursor volta ao campo do segmento de origem
    E nada é gravado

  Cenário: RN-06 — segmento de destino não cadastrado
    Dado que estou na tela C868T e informei um segmento de origem cadastrado
    Quando informo, no segmento de destino, um código que não existe no cadastro de segmentos da secretaria de destino
    Então vejo "* Segmento nao cadastrado - PARA *"
    E o cursor volta ao campo do segmento de destino
    E nada é gravado

  Cenário: RN-06 — o código 99 informado só no destino, no segmento
    Dado que estou na tela C868T
    E informei no segmento de origem um código diferente de 99
    Quando informo 99 no segmento de destino
    Então vejo "* Nao use 99 para esta opcao - PARA *"
    E o cursor volta ao campo do segmento de destino
    E nada é gravado

  Cenário: RN-05 — a letra T na semana de origem vale para o destino
    Dado que estou na tela C868T e informei um grupo de origem cadastrado
    Quando informo T na semana de origem
    Então a semana de destino assume T sozinha
    E a operação segue com T nos dois lados

  Cenário: RN-06 — o código 99 no segmento de origem vale para o destino
    Dado que estou na tela C868T e informei um grupo de origem cadastrado
    Quando informo 99 no segmento de origem
    Então o segmento de destino assume 99 sozinho
    E a operação segue com o código 99 nos dois lados

  Cenário: RN-07 — campo não numérico
    Dado que estou na tela C868T
    Quando informo, numa das quatro datas ou num dos códigos de secretaria, grupo ou segmento, algo que não é número
    Então o campo é recusado pela conferência numérica antes de qualquer consulta
    E nada é gravado

  Cenário: RN-07 e RN-08 — as datas de início vêm dos cardápios achados
    Dado que os dois períodos têm cardápio de estimativa cadastrado terminando na data limite que informei
    Quando envio os dados e confirmo a operação
    Então as duas datas de início deixam de ser as que digitei
    E passam a ser as datas de início dos cardápios daqueles períodos

  Cenário: RN-08 — não há cardápio na data limite do período de origem
    Dado que estou na tela C868T
    Quando informo, para o período de origem, uma data limite que não é o fim de um cardápio cadastrado naquela secretaria
    Então vejo "* Cardapios nao cadastrados para esta data - DE *"
    E o cursor volta ao dia limite do período de origem
    E nada é gravado

  Cenário: RN-08 — não há cardápio na data limite do período de destino
    Dado que estou na tela C868T e o período de origem tem cardápio cadastrado na data limite que informei
    Quando informo, para o período de destino, uma data limite que não é o fim de um cardápio cadastrado na secretaria de destino
    Então vejo "* Cardapios nao cad. para esta data - PARA *"
    E o cursor volta ao dia limite do período de destino
    E nada é gravado

  Cenário: RN-09 — nenhum dos dois marcado
    Dado que estou na tela C868T e os dois períodos têm cardápio cadastrado nas datas limite que informei
    Quando não marco nem o planejamento por dia da semana nem o sazonal
    Então vejo "* Informe planejamento a copiar *"
    E o cursor volta ao campo do planejamento
    E nada é gravado

  Cenário: RN-09 — não há planejamento por dia da semana no período de origem
    Dado que estou na tela C868T e os dois períodos têm cardápio cadastrado nas datas limite que informei
    E marco a cópia do planejamento por dia da semana
    E o grupo e o período de origem não têm planejamento por dia da semana cadastrado
    Quando envio os dados
    Então vejo "* Planejamentos nao cadastrados - DE *"
    E o cursor volta ao dia limite do período de origem
    E nada é gravado

  Cenário: RN-09 — não há planejamento sazonal no período de origem
    Dado que estou na tela C868T e os dois períodos têm cardápio cadastrado nas datas limite que informei
    E não marco a cópia do planejamento por dia da semana
    E marco a cópia do planejamento sazonal
    E o grupo e o período de origem não têm planejamento sazonal cadastrado
    Quando envio os dados
    Então vejo "* Planejamentos sazonais nao cad. - DE *"
    E o cursor volta ao dia limite do período de origem
    E nada é gravado

  Cenário: RN-09 — os dois marcados e o sazonal não cadastrado
    Dado que estou na tela C868T e os dois períodos têm cardápio cadastrado nas datas limite que informei
    E existe planejamento por dia da semana para o grupo e o período de origem
    E não existe planejamento sazonal para aquele grupo e período
    Quando marco as duas cópias, informo a impressora e envio os dados
    Então a tela não recusa por falta do sazonal
    E vejo "* Confirma copia dos planejamentos <S/N> ? *"

  Cenário: RN-10 — impressora em branco
    Dado que estou na tela C868T e passaram as conferências dos dois lados
    Quando deixo a impressora em branco
    Então vejo "* Informe a impressora *"
    E o cursor volta ao campo da impressora
    E nada é gravado

  Cenário: RN-11 — os dados mudam entre a pergunta e a resposta
    Dado que já vi a pergunta de confirmação
    Quando altero um dos dados guardados e respondo S
    Então a tela não aproveita a resposta
    E refaz as conferências e pergunta de novo "* Confirma copia dos planejamentos <S/N> ? *"
    E nada é registrado antes de eu responder S

  Cenário: RN-11 — resposta diferente de S
    Dado que já vi a pergunta de confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a tela refaz as conferências e pede a mesma confirmação outra vez
    E nada é registrado

  Cenário: RN-12 — já existe um pedido pendente
    Dado que existe uma solicitação de cópia de planejamentos já registrada
    Quando confirmo a operação com a resposta S
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E a confirmação é desfeita e nenhuma solicitação nova é registrada
    E nada é gravado

  Cenário: RN-15 — a tela não toca nos cadastros
    Dado que confirmei a operação com a resposta S
    Quando a operação termina
    Então os cadastros de secretarias, de grupos, de segmentos, de cardápios e os dois de planejamento continuam como estavam
    E o que passa a existir é a solicitação de processamento e o registro de auditoria
```
