# US — C866T — Copiar os cardápios de uma origem para a estimativa de outro período

## Estória

Como **servidor de CRE**, quero **pedir que os cardápios já cadastrados de uma
secretaria e de um segmento sejam aproveitados na estimativa de um período novo,
em outra secretaria ou em outro segmento**, para que a estimativa não precise ser
remontada cardápio por cardápio, segmento por segmento.

A estimativa de um período é o que sustenta o serviço e a compra da alimentação
escolar: é nela que fica a composição de cada cardápio por classe, gênero e
subclasse. Quando o período que vem repete o desenho do anterior, esse trabalho é
o mesmo — e sem esta tela cada secretaria e cada segmento teriam de ser montados
de novo, à mão. O pedido não é a cópia: a tela recolhe a origem, o destino e a
confirmação, e é o processamento do sistema que copia.

## Contexto

Jornada S000M → C000M → C800M → C811M → C866T.

Ator: servidor de CRE — pede a cópia dos cardápios já cadastrados de um período
para a estimativa de outro, escolhendo a secretaria e o segmento de cada ponta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio.

As três telas do meio do caminho são **menus** — o `C000M`, o `C800M` e a
`C811M` —, e nenhuma delas passa registro nem operação para esta: elas apenas
chamam a tela pelo nome. A `C866T` abre sozinha, **sempre no modo de alteração**, e
o que ela usa da sessão — a matrícula, o privilégio, a coordenação regional
escolar, a secretaria e a data do sistema — foi deixado pela entrada. Não há, no
fonte, comparação com a tela de origem: o comportamento da `C866T` não muda
conforme quem a chamou.

A tela também não encadeia em outra: terminado o pedido ela **reabre a si mesma**,
primeiro para mostrar a pergunta de confirmação e depois para avisar que o cadastro
está sendo atualizado. O que ela entrega não vai para uma tela seguinte, e sim para
o processamento do sistema: o pedido com as duas secretarias, os dois segmentos e
os dois períodos.

As regras abaixo são só as da tela desta jornada. As da entrada estão no documento
dela; a que se revelou pertencer à entrada está registrada no **anexo de
evidências**, na seção própria.

---

## Regras de negócio

### RN-01 — A tela pede a cópia dos cardápios para a estimativa de outro período

A tela trabalha com **dois lados**. No lado **de origem** ficam a **secretaria**, o
**segmento** e o **período dos cardápios** que serão aproveitados. No lado **de
destino** ficam a **secretaria**, o **segmento** e o **período da estimativa** que
vai ser criada. A tela confere os dois lados, pergunta a confirmação e, só com a
resposta afirmativa, registra o pedido e o entrega ao processamento do sistema.

Quem copia não é a tela: ela não inclui, não altera e não exclui cardápio nenhum
(RN-14). Ela recolhe o pedido, confirma e dispara; o resultado não volta para ela —
o servidor vê **\* Cadastro sendo atualizado \*** e acompanha depois.

[?] Os fontes desta jornada mostram o que a tela entrega ao processamento e onde o
pedido é registrado, mas não o processamento em si: se ele copia mesmo os cardápios
da origem para a estimativa de destino, o que faz com o que já existe no destino e
como o período novo é preenchido são perguntas ao site.

### RN-02 — A tela abre na secretaria do usuário e com a data do sistema; a secretaria de destino é obrigatória e tem de existir

Ao abrir, a tela mostra a **data do sistema** e a **descrição da secretaria do
usuário**, e preenche os dois lados com essa mesma secretaria. Os nomes de
secretaria mostrados vêm do cadastro de secretarias, não do que foi digitado.

A **secretaria de destino** é de preenchimento obrigatório: em branco, a recusa é
**\* Informe a Secretaria - PARA \***; informada, tem de constar do cadastro, senão
a recusa é **\* Secretaria nao cadastrada - PARA \***. Nas duas o cursor volta ao
campo da secretaria de destino e nada é gravado.

[?] A secretaria de origem não tem recusa própria: não há "informe a secretaria de
origem" nem "secretaria de origem não cadastrada". Ela vem preenchida com a do
usuário e, quando não consta do cadastro, a tela segue sem mensagem própria — o que
o servidor vê nesse caso depende das conferências seguintes, e o fonte não permite
concluir qual é. Também não se pode concluir do fonte se o servidor tem de manter a
secretaria de origem na dele ou se pode trocá-la. Pergunta ao site.

[?] Se o que foi digitado na secretaria de origem não for número, a conferência
recusa o campo mas não sabe onde pôr o cursor: das **dezesseis** posições que a
tela confere antes das consultas, **quatro** não têm posição de cursor — a
secretaria de origem e as três do início do período dos cardápios. Pergunta ao
site.

### RN-03 — A tela só opera em modo de alteração

A tela se apresenta sempre no modo de alteração. Acionada em qualquer outro modo de
manutenção, a operação é recusada com **\* Opcao nao disponivel. Use ALT \***, o
cursor volta ao campo do modo e nada é gravado.

[?] A recusa manda usar ALT e a conferência aceita apenas o código de alteração; o
acervo não traz a correspondência entre a tecla e o código. Ou o terminal traduz a
tecla antes de enviar, ou a mensagem está desalinhada da conferência. Pergunta ao
site.

### RN-04 — Os dois segmentos; o código 99 só vale na origem, e obriga o destino

Cada lado tem o seu segmento. Os dois são obrigatórios: sem o segmento de origem a
recusa é **\* Informe o segmento - DE \***; sem o de destino, **\* Informe o
segmento - PARA \***.

O código **99** só é aceito no segmento de origem. Informado lá, o segmento de
destino assume 99 sozinho; informado apenas no destino, a recusa é **\* Nao use 99
para esta opcao - PARA \***. Com 99 a tela não procura a composição por segmento —
procura o cardápio do período (RN-08); com qualquer outro código, a composição
daquele segmento tem de existir nos dois lados.

[?] O que o código 99 significa em negócio — "todos os segmentos" ou outro
conjunto — não está no corpus desta jornada nem no dicionário de dados. O que se
pode afirmar é só o que a tela faz com ele: dispensa a composição por segmento e
obriga o outro lado a também ser 99. Pergunta ao site.

### RN-05 — São quatro datas; a data final identifica o cardápio de origem, e a inicial de origem é substituída

São **quatro datas**, digitadas como dia, mês e ano — **doze números** ao todo: o
início e o fim do período da estimativa e o início e o fim do período dos
cardápios. Todas passam pela conferência numérica do sistema antes de qualquer
consulta: campo em branco vira zero e o que não for número é recusado antes de o
cadastro ser lido.

Quem define o período que a cópia vai gerar são as duas datas da **estimativa**. Do
lado dos cardápios quem decide é a **data final**: é ela que localiza o cardápio já
cadastrado que será aproveitado (RN-08). A **data inicial** do período dos
cardápios é digitada e conferida como número, e o sistema a substitui pela data
inicial do cardápio que encontrar.

[?] A data inicial do período dos cardápios não é conferida como data — não passa
pelo calendário nem pela faixa de anos — nem é comparada com a data final, e as
três posições dela (dia, mês, ano) não têm posição de cursor na conferência
numérica. Se ela deveria identificar ou conferir o período de origem, o caminho não
a usa para isso. Pergunta ao site.

### RN-06 — As duas datas da estimativa têm de ser datas válidas

As datas da estimativa passam pelo calendário do sistema e ainda têm de ter **ano
entre 1994 e 2099**. Quando a data inicial não passa, a recusa é **\* Data inicial
da estimativa invalida \***; quando é a final, **\* Data final da estimativa
invalida \***. Em qualquer dos casos o cursor volta à data recusada e nada é
gravado.

[?] Só as datas da estimativa passam por essa conferência; as do período dos
cardápios são conferidas apenas como número. O fonte não diz se isso é intencional.
Pergunta ao site.

### RN-07 — A data inicial da estimativa não pode ser posterior à data final

Se a data inicial da estimativa for maior que a data final, a recusa é **\* Data
inicial maior que data final \***, com o cursor na data inicial, e nada é gravado.

[?] Essa conferência de ordem existe só para o par da estimativa: o par do período
dos cardápios não tem conferência equivalente. Pergunta ao site.

### RN-08 — O período dos cardápios tem de ter cardápio cadastrado na secretaria e no segmento de origem

A **data final** informada para o período dos cardápios é procurada como o fim de
um cardápio já cadastrado da secretaria de origem. Quando o segmento de origem não
é 99, exige-se ainda a composição daquele segmento para o cardápio encontrado. Não
havendo, a recusa é **\* Nao existem card.estimativa para esta data \***, com o
cursor na data final do período dos cardápios, e nada é gravado. Havendo, a data
inicial do cardápio encontrado substitui a que foi digitada (RN-05).

### RN-09 — O período da estimativa tem de estar livre

Antes de pedir a confirmação, o sistema procura cardápio já cadastrado para a
**secretaria de destino** cuja data final caia na **data inicial** ou na **data
final** informadas para a estimativa; quando o segmento de destino não é 99, só
conta o cardápio que também tenha a composição daquele segmento. Achando, a recusa
é **<- Cardapios ja cadastrados neste intervalo \***, mostrando junto a data final
do cardápio que já existe, com o cursor na data inicial da estimativa; nada é
gravado.

[?] A procura leva a data como chave, mas a conferência seguinte não compara a data
lida de volta — compara só a secretaria. O efeito exato da leitura pela chave não
está no acervo: se ela exigir a data exata, a recusa é incondicional quando o
cardápio existe, e o trecho que continuaria a operação fica **inalcançável por esse
caminho**; se ela apenas se posicionar no primeiro cardápio a partir da data
informada, a conferência compara mesmo os períodos. Os dois comportamentos são
compatíveis com o que o fonte mostra, e não escolho entre eles. Pergunta ao site.

### RN-10 — A cópia só segue depois de confirmada, e com os dados inalterados

Passadas as conferências, a tela pergunta **\* Confirma copia dos cardapios <S/N> ?
\*** e espera a resposta. Só a resposta afirmativa segue para o registro.

Junto com a resposta, os dados informados têm de continuar iguais aos que a tela
guardou — a secretaria e o segmento de destino, as duas datas da estimativa, o
segmento de origem e as duas datas finais dos períodos. Alterado qualquer um deles,
a tela não aproveita a resposta: refaz as conferências e pergunta de novo.

[?] Responder N — ou deixar a resposta em branco — não cancela o pedido: a tela
limpa a resposta e volta às conferências, que pedem a mesma confirmação outra vez.
Não há, no caminho lido, um desfecho que encerre a operação com a resposta negativa.
Pergunta ao site.

[?] A comparação dos "dados inalterados" não olha a **secretaria de origem** nem a
**data inicial** do período dos cardápios: mudá-las entre a pergunta e a resposta
não faz a tela refazer as conferências. O fonte não diz se é proposital. Pergunta
ao site.

### RN-11 — Um pedido de cópia pendente impede outro

Antes de registrar, o sistema procura uma **solicitação de processamento pendente**
para este mesmo serviço; existindo, a recusa é **\* Relatorio em processamento.
Aguarde. \*** e nada é registrado. O pedido só pode ser feito quando não há outro
em andamento.

[?] A procura olha só o código do serviço, sem examinar a secretaria nem a situação
do pedido: um pedido de outra secretaria, ou um já atendido e ainda não retirado,
também bloqueia. E a própria tela registra o pedido **sem marcar a situação** —
quem o marca como atendido, ou o remove, não está nos fontes desta jornada. Se
ninguém o retirar, a cópia só pode ser pedida uma vez. O acervo não permite
concluir qual dos dois. Pergunta ao site.

### RN-12 — A tela registra o pedido e entrega o serviço ao processamento

Confirmada a operação, a tela grava a **solicitação de processamento** com o
**número seguinte** da fila, o código do serviço, a **secretaria de origem**, a
data, a matrícula e a estação da sessão, e entrega o serviço ao processamento com
os parâmetros do pedido — as duas secretarias, os dois segmentos e as quatro datas.
Em seguida avisa **\* Cadastro sendo atualizado \***. A tela não espera pelo
resultado.

[?] A entrega do serviço depende de indicadores do ambiente — o produto em execução
e o retorno da gravação — cujo valor e origem não estão nos fontes desta jornada:
quando ela não acontece, o pedido fica registrado mas o serviço não é entregue.
Pergunta ao site.

[?] O número do pedido é o seguinte ao último já usado na fila; a tela não escolhe
o número sozinha, ela o lê da fila e incrementa. Se duas sessões pedirem ao mesmo
tempo, o fonte desta jornada não permite dizer o que acontece. Pergunta ao site.

### RN-13 — Toda cópia confirmada deixa rastro na auditoria

Antes do pedido, a tela grava o **registro de auditoria** da operação: a tela, a
operação de inclusão, a data e a hora da sessão, a secretaria, a matrícula e a
estação, com os **parâmetros do pedido** guardados como valor anterior e o valor
posterior vazio.

[?] O número do processo da auditoria recebe o **dia** da data inicial da
estimativa; o fonte não explica a escolha. Pergunta ao site.

### RN-14 — A tela não inclui, não altera e não exclui cadastro nenhum

A tela apenas **lê** os cadastros de que precisa — o de secretarias, o de cardápios
e a composição dos cardápios por segmento. As rotinas de gravação, de exclusão e de
travamento existem declaradas para os **sete** cadastros que a tela enxerga, mas
**só duas gravações são executadas**: a da solicitação de processamento e a da
auditoria. Não há nenhuma exclusão e nenhum travamento. Declarar não é executar.

---

## Cenários BDD

```gherkin
Funcionalidade: Copiar os cardápios de uma origem para a estimativa de outro período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C866T

  Cenário: RN-01, RN-08, RN-10, RN-12 e RN-13 — copiar os cardápios para a estimativa de outro período
    Dado que estou na tela C866T, na minha secretaria
    E a secretaria e o segmento de origem têm um cardápio cadastrado que termina na data final que vou informar
    E o período da estimativa que vou informar está livre na secretaria de destino
    Quando informo as duas secretarias, os dois segmentos e as quatro datas
    E confirmo a operação
    Então vejo "* Confirma copia dos cardapios <S/N> ? *"
    Quando respondo S
    Então vejo "* Cadastro sendo atualizado *"
    E a solicitação de processamento fica registrada com as duas secretarias, os dois segmentos, as quatro datas, a minha matrícula e a data da sessão
    E a operação fica registrada na auditoria
    E nenhum cardápio é incluído, alterado ou excluído por esta tela

  Cenário: RN-02 — a tela abre na minha secretaria e com a data do sistema
    Dado que entrei com um usuário de uma secretaria
    Quando a tela C866T abre
    Então vejo a data do sistema
    E os dois lados vêm preenchidos com a minha secretaria e com o nome dela

  Cenário: RN-02 — secretaria de destino em branco
    Dado que estou na tela C866T
    Quando deixo a secretaria de destino em branco
    Então vejo "* Informe a Secretaria - PARA *"
    E o cursor volta ao campo da secretaria de destino
    E nada é gravado

  Cenário: RN-02 — secretaria de destino não cadastrada
    Dado que estou na tela C866T
    Quando informo uma secretaria de destino que não existe no cadastro
    Então vejo "* Secretaria nao cadastrada - PARA *"
    E o cursor volta ao campo da secretaria de destino
    E nada é gravado

  Cenário: RN-03 — modo de manutenção diferente de alteração
    Dado que estou na tela C866T
    Quando aciono a tela em um modo de manutenção diferente de ALT
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo do modo de manutenção
    E nada é gravado

  Cenário: RN-04 — segmento de origem em branco
    Dado que estou na tela C866T
    Quando deixo o segmento de origem em branco
    Então vejo "* Informe o segmento - DE *"
    E o cursor volta ao campo do segmento de origem
    E nada é gravado

  Cenário: RN-04 — segmento de destino em branco
    Dado que estou na tela C866T
    E informei o segmento de origem
    Quando deixo o segmento de destino em branco
    Então vejo "* Informe o segmento - PARA *"
    E o cursor volta ao campo do segmento de destino
    E nada é gravado

  Cenário: RN-04 — o código 99 informado só no destino
    Dado que estou na tela C866T
    E informei no segmento de origem um código diferente de 99
    Quando informo 99 no segmento de destino
    Então vejo "* Nao use 99 para esta opcao - PARA *"
    E o cursor volta ao campo do segmento de destino
    E nada é gravado

  Cenário: RN-04 — o código 99 na origem obriga o destino
    Dado que estou na tela C866T
    Quando informo 99 no segmento de origem
    Então o segmento de destino assume 99 sozinho
    E a operação segue com o código 99 nos dois lados

  Cenário: RN-05 — campo não numérico
    Dado que estou na tela C866T
    Quando informo, numa das quatro datas ou num dos códigos dos dois segmentos ou das duas secretarias, algo que não é número
    Então o campo é recusado pela conferência numérica antes de qualquer consulta
    E nada é gravado

  Cenário: RN-05 e RN-08 — a data inicial de origem vem do cardápio encontrado
    Dado que a secretaria e o segmento de origem têm um cardápio cadastrado que termina na data final que informei
    Quando confirmo a operação
    Então a data inicial do período dos cardápios deixa de ser a que digitei
    E passa a ser a data inicial daquele cardápio

  Cenário: RN-06 — data inicial da estimativa inválida
    Dado que estou na tela C866T
    Quando informo uma data inicial da estimativa que não existe no calendário
    Então vejo "* Data inicial da estimativa invalida *"
    E o cursor volta à data inicial da estimativa
    E nada é gravado

  Cenário: RN-06 — data final da estimativa inválida
    Dado que estou na tela C866T
    Quando informo uma data final da estimativa que não existe no calendário
    Então vejo "* Data final da estimativa invalida *"
    E o cursor volta à data final da estimativa
    E nada é gravado

  Cenário: RN-06 — ano da estimativa fora da faixa aceita
    Dado que estou na tela C866T
    Quando informo uma data da estimativa com ano anterior a 1994 ou posterior a 2099
    Então vejo a mensagem de data da estimativa inválida
    E nada é gravado

  Cenário: RN-07 — data inicial da estimativa depois da data final
    Dado que estou na tela C866T
    Quando informo a data inicial da estimativa maior que a data final
    Então vejo "* Data inicial maior que data final *"
    E o cursor volta à data inicial da estimativa
    E nada é gravado

  Cenário: RN-08 — não há cardápio na data final informada
    Dado que estou na tela C866T
    Quando informo uma data final de cardápio que não é o fim de um cardápio cadastrado na secretaria de origem
    Então vejo "* Nao existem card.estimativa para esta data *"
    E o cursor volta à data final do período dos cardápios
    E nada é gravado

  Cenário: RN-08 — não há composição para o segmento de origem
    Dado que informei um segmento de origem diferente de 99
    E o cardápio do período não tem composição para aquele segmento
    Quando confirmo a operação
    Então vejo "* Nao existem card.estimativa para esta data *"
    E nada é gravado

  Cenário: RN-09 — o período da estimativa já está ocupado
    Dado que a secretaria de destino tem um cardápio cadastrado que termina na data inicial ou na data final da estimativa que informei
    Quando confirmo a operação
    Então vejo "<- Cardapios ja cadastrados neste intervalo *"
    E o cursor volta à data inicial da estimativa
    E nada é gravado

  Cenário: RN-10 — os dados mudam entre a pergunta e a resposta
    Dado que já vi a pergunta de confirmação
    Quando altero um dos dados informados e respondo S
    Então a tela não aproveita a resposta
    E refaz as conferências e pergunta de novo "* Confirma copia dos cardapios <S/N> ? *"
    E nada é registrado antes de eu responder S

  Cenário: RN-10 — resposta diferente de S
    Dado que já vi a pergunta de confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a tela refaz as conferências e pede a mesma confirmação outra vez
    E nada é registrado

  Cenário: RN-11 — já existe um pedido de cópia pendente
    Dado que existe uma solicitação de cópia de cardápios já registrada
    Quando confirmo a operação com a resposta S
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E nenhuma solicitação nova é registrada
    E nada é gravado

  Cenário: RN-14 — a tela não toca nos cadastros
    Dado que confirmei a operação com a resposta S
    Quando a operação termina
    Então os cadastros de secretarias, de cardápios e de composição dos cardápios continuam como estavam
    E o que passa a existir é a solicitação de processamento e o registro de auditoria
```
