# US — C870T — Copiar os cardápios oficiais para a estimativa de um período

## Estória

Como **servidor de CRE**, quero **pedir que os cardápios oficiais de um período sejam
aproveitados na estimativa de outro período**, para que a estimativa do período novo não
precise ser montada de novo, cardápio por cardápio.

A alimentação escolar é planejada por cardápio: há o **cardápio oficial**, já cadastrado
para um período, e há a **estimativa**, que a secretaria projeta para outro período.
Quando o período novo repete o que já está cadastrado, o trabalho é o mesmo — e sem esta
tela cada cardápio teria de ser remontado à mão. O pedido não é a cópia: a tela recolhe o
período da estimativa e o período do cardápio oficial, confere os dois, pede a
confirmação e é o processamento do sistema que copia.

## Contexto

Jornada S000M → C000M → C800M → C811M → C870T.

Ator: servidor de CRE — pede que os cardápios oficiais de um período sejam aproveitados
na estimativa de outro, informando o período da estimativa e o período do cardápio
oficial.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As três telas do meio do caminho são **menus** — o `C000M`, o `C800M` e a `C811M` —, e
nenhuma delas passa registro nem operação para esta: elas apenas chamam a tela pelo
nome. A `C870T` abre sozinha, **sempre no modo de alteração**, e o que ela usa da sessão
— a matrícula, o privilégio, a secretaria e a CRE — foi deixado pela entrada. A tela
recebe o código da tela que a chamou e o entrega à lógica de rota da entrada, mas não o
compara com nada: o comportamento dela **não muda conforme quem a chamou**.

A tela também não encadeia em outra: terminado o pedido ela **reabre a si mesma**,
primeiro para mostrar a pergunta de confirmação e depois para avisar que o cadastro está
sendo atualizado. O que ela entrega não vai para uma tela seguinte, e sim para o
processamento do sistema: a secretaria, o período da estimativa e o período do cardápio.

As regras abaixo são só as da tela desta jornada. As da entrada estão no documento dela;
as que se revelaram pertencer à entrada estão registradas no **anexo de evidências**, na
seção própria.

---

## Regras de negócio

### RN-01 — A tela pede a cópia dos cardápios oficiais para a estimativa de um período

A tela trabalha com **dois períodos**. O da **estimativa** tem a **data inicial** e a
**data final**; o do **cardápio** tem a **data inicial** e a **data limite**. A tela
confere os dois, pergunta a confirmação e, só com a resposta afirmativa, registra o
pedido e o entrega ao processamento do sistema.

Quem copia não é a tela: ela não inclui, não altera e não exclui cardápio nenhum (RN-13).
Ela recolhe o pedido, confirma e dispara; o resultado não volta para ela — o servidor vê
**\* Cadastro sendo atualizado \*** e acompanha depois.

[?] Os fontes desta jornada mostram o que a tela entrega ao processamento e onde o
pedido é registrado, mas não o processamento em si: se ele copia mesmo os cardápios
oficiais para a estimativa, o que faz com o que já existe no destino e como o período
novo é preenchido são perguntas ao site.

### RN-02 — A tela é da secretaria da sessão, e a secretaria não é digitável

Ao abrir, a tela mostra a **data do sistema** e a **descrição da secretaria da sessão**;
não há campo de secretaria — todas as consultas da tela são da secretaria do servidor.

### RN-03 — A tela só opera em modo de alteração

A tela se apresenta sempre no modo de alteração. Acionada em qualquer outro modo de
manutenção, a operação é recusada com **\* Opcao nao disponivel. Use ALT \***, o cursor
volta ao campo do modo e nada é gravado.

[?] A recusa manda usar ALT e a conferência aceita apenas o código de alteração; o
acervo não traz a correspondência entre a tecla e o código. Ou o terminal traduz a tecla
antes de enviar, ou a mensagem está desalinhada da conferência. Pergunta ao site.

[?] O programa recebe o código da tela que chamou esta e o entrega à lógica de rota da
entrada, mas não o compara com nada: nesta tela o comportamento não muda conforme a
origem. Se a rota da entrada decide alguma coisa com esse código, isso não está nos
fontes desta jornada. Pergunta ao site.

### RN-04 — São quatro datas, em dia, mês e ano

As quatro datas são informadas em dia, mês e ano — **doze** partes numéricas. As doze
passam pela conferência numérica do sistema antes de qualquer consulta: campo em branco
vira zero e o que não for número é recusado antes de o cadastro ser lido; nada é gravado.

[?] Das doze partes conferidas como número, **nove** têm posição de cursor. Quando o
servidor digita algo que não é número em uma das três partes da **data inicial do
cardápio**, a tela recusa o campo mas não sabe onde pôr o cursor. Pergunta ao site.

### RN-05 — As duas datas da estimativa têm de ser datas válidas

As datas inicial e final da **estimativa** passam pelo calendário do sistema: o dia tem
de existir no mês. O ano tem de estar entre **1994 e 2099**. Quando a data inicial não
passa, a recusa é **\* Data inicial da estimativa invalida \***, com o cursor no dia
inicial; quando é a data final, **\* Data final da estimativa invalida \***, com o cursor
no dia final. Em qualquer dos casos nada é gravado.

### RN-06 — A data inicial da estimativa não pode ser posterior à data final

Se a data inicial da estimativa for maior que a data final, a recusa é
**\* Data inicial maior que data final \***, com o cursor no dia inicial, e nada é
gravado.

[?] A conferência de ordem existe só para o par da estimativa. As duas datas do
**cardápio** não são comparadas entre si e também não passam pelo calendário nem pela
faixa de ano: daquele par, só a data limite é conferida, e apenas contra o cadastro de
cardápios oficiais (RN-07). Se isso é intencional, o fonte não diz. Pergunta ao site.

### RN-07 — O período do cardápio tem de ter cardápio oficial cadastrado, e é dele que vem a data inicial do cardápio

Para a **data limite do cardápio** informada, a tela procura no cadastro de cardápios
oficiais o cardápio da secretaria da sessão que termina naquela data. Não achando, a
recusa é **\* Nao existem cardapios oficiais para esta data \***, com o cursor no dia
limite do cardápio, e nada é gravado. Achando, a **data inicial do cardápio** que a tela
mostra deixa de ser a digitada e passa a ser a data inicial daquele cardápio oficial;
essa é a data que a tela repõe no lugar da digitada e a que segue no pedido.

[?] A procura leva o código do cardápio zerado e, do que ela acha, a tela só reconfere a
secretaria e as três partes da data limite — o código do cardápio não é reconferido. O
que os modificadores da leitura fazem não está no corpus nem no manual: se a leitura for
a de uma chave exata, só o cardápio de código zero serve; se ela apenas se posicionar,
serve qualquer cardápio daquela secretaria que termine na data limite. Não escolho entre
os dois desfechos. Pergunta ao site.

### RN-08 — Já havendo cardápio de estimativa no intervalo, a cópia é recusada

Antes de pedir a confirmação, o sistema procura cardápio de estimativa já cadastrado
cujo período termine na **data inicial** ou na **data final** informada para a
estimativa. Achando qualquer um dos dois, a recusa é
**<- Cardapios ja cadastrados neste intervalo \***, com o cursor no dia inicial da
estimativa, e nada é gravado.

[?] Do que a procura acha, a tela compara só a secretaria — não reconfere a data limite
com a informada, ao contrário da procura do cardápio oficial (RN-07). E a conferência de
sobreposição que vem depois exige uma condição que o resultado dessa procura já
satisfaz: achando o registro, a recusa sai. Se a leitura for a de uma chave exata, o
efeito é "achou, recusa"; se ela apenas se posicionar, o efeito depende de qual registro
ela devolve. Não escolho entre os dois desfechos. Pergunta ao site.

### RN-09 — A cópia é confirmada pelo usuário, e os dados não podem mudar

Passadas as conferências, a tela repõe as quatro datas na tela — com a data inicial do
cardápio vinda do cardápio oficial (RN-07) — e pergunta
**\* Confirma copia dos cardapios <S/N> ? \***, com o cursor no campo da resposta. Só a
resposta afirmativa segue para o registro.

Junto com a resposta, os dados informados têm de continuar iguais aos que a tela guardou:
a data inicial e a data final da estimativa e a data limite do cardápio. Alterado
qualquer um deles, a tela não aproveita a resposta: refaz as conferências e pergunta de
novo.

[?] Responder N — ou deixar a resposta em branco — não cancela o pedido: a tela limpa a
resposta e volta às conferências, que pedem a mesma confirmação outra vez. Não há, no
caminho lido, um desfecho que encerre a operação com a resposta negativa. Pergunta ao
site.

[?] A comparação dos "dados inalterados" olha **nove** das doze partes de data e não olha
as **três** da data inicial do cardápio. Como a tela usa essa data no pedido e no
registro de auditoria, trocá-la entre a pergunta e a resposta não faz a tela refazer as
conferências, e o pedido segue com o que estiver em tela. O fonte não diz se é
proposital. Pergunta ao site.

### RN-10 — Um pedido de cópia em andamento impede outro

Antes de registrar, o sistema procura uma **solicitação de processamento pendente** deste
mesmo serviço; existindo, a recusa é **\* Relatorio em processamento. Aguarde. \***, a
confirmação é desfeita e nada é registrado. O pedido só pode ser feito quando não há
outro em andamento.

[?] A procura olha só o código do serviço, sem examinar a secretaria nem a situação do
pedido: um pedido de outra secretaria, ou um já atendido e ainda não retirado, também
bloqueia. E a própria tela registra o pedido **sem marcar a situação** — quem o marca
como atendido, ou o remove, não está nos fontes desta jornada. Se ninguém o retirar, a
cópia só pode ser pedida uma vez. Pergunta ao site.

### RN-11 — A tela não copia: registra o pedido e dispara o processamento

Confirmada a operação, a tela grava a **solicitação de processamento** com o número
seguinte da fila, o código do serviço, a secretaria da sessão, a data, a matrícula e a
estação, e entrega o serviço ao processamento com os parâmetros do pedido — a secretaria,
as duas datas da estimativa e as duas datas do cardápio —, **uma cópia** e o e-mail
cadastrado do servidor. A tela não pede impressora: o destino da impressão vai em branco.
Em seguida avisa **\* Cadastro sendo atualizado \***. A tela não espera pelo resultado.

[?] A entrega do serviço depende de indicadores do ambiente — o produto em execução e o
retorno da gravação — cujo valor e origem não estão nos fontes desta jornada: quando ela
não acontece, o pedido fica registrado mas o serviço não é entregue. Pergunta ao site.

[?] O número do pedido é o seguinte ao último já usado na fila; a tela não escolhe o
número sozinha, ela o lê da fila e incrementa. Se duas sessões pedirem ao mesmo tempo, o
fonte desta jornada não permite dizer o que acontece. Pergunta ao site.

### RN-12 — A cópia confirmada fica registrada na auditoria

Antes do pedido, a tela grava o **registro de auditoria** da operação: a tela, a operação
de inclusão, a data e a hora da sessão, a secretaria, a CRE, a matrícula e a estação, com
os **parâmetros do pedido** — a secretaria e as quatro datas — guardados como valor
anterior e o valor posterior vazio.

[?] O número do processo da auditoria recebe o **dia** da data inicial da estimativa; o
fonte não explica a escolha. Pergunta ao site.

### RN-13 — A tela não inclui, não altera e não exclui cardápio nenhum

A tela apenas **lê** os cadastros de que precisa — o de telas, o de cardápios oficiais, o
de cardápios de estimativa, o do funcionário e o de requisições. As rotinas de gravação,
de exclusão e de travamento existem declaradas para os **seis** cadastros que a tela
enxerga, mas **só duas gravações são executadas**: a do registro de auditoria e a da
solicitação de processamento. Não há nenhuma exclusão e nenhum travamento. Declarar não é
executar.

---

## Cenários BDD

```gherkin
Funcionalidade: Copiar os cardápios oficiais para a estimativa de um período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C870T

  Cenário: RN-01, RN-04, RN-05, RN-07, RN-09, RN-11 e RN-12 — copiar os cardápios oficiais para a estimativa de um período
    Dado que estou na tela C870T, na minha secretaria
    E existe cardápio oficial cadastrado terminando na data limite do cardápio que vou informar
    E não existe cardápio de estimativa cadastrado terminando nas duas datas da estimativa que vou informar
    Quando informo a data inicial e a data final da estimativa e a data limite do cardápio, e envio os dados
    Então vejo "* Confirma copia dos cardapios <S/N> ? *"
    E a data inicial do cardápio passa a ser a data inicial do cardápio oficial cadastrado
    Quando respondo S
    Então vejo "* Cadastro sendo atualizado *"
    E a solicitação de processamento fica registrada com a minha secretaria e com as quatro datas
    E a operação fica registrada na auditoria
    E nenhum cardápio é incluído, alterado ou excluído por esta tela

  Cenário: RN-02 — a tela abre na minha secretaria e com a data do sistema
    Dado que entrei com um usuário de uma secretaria
    Quando a tela C870T abre
    Então vejo a data do sistema e a minha secretaria
    E não há campo de secretaria

  Cenário: RN-03 — modo de manutenção diferente de alteração
    Dado que estou na tela C870T
    Quando aciono a tela em um modo de manutenção diferente de ALT
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo do modo de manutenção
    E nada é gravado

  Cenário: RN-04 — campo não numérico
    Dado que estou na tela C870T
    Quando informo, numa das doze partes das quatro datas, algo que não é número
    Então o campo é recusado pela conferência numérica antes de qualquer consulta
    E nada é gravado

  Cenário: RN-05 — data inicial da estimativa inválida
    Dado que estou na tela C870T
    Quando informo, na data inicial da estimativa, um dia que não existe no mês ou um ano fora de 1994 a 2099
    Então vejo "* Data inicial da estimativa invalida *"
    E o cursor volta ao dia inicial da estimativa
    E nada é gravado

  Cenário: RN-05 — data final da estimativa inválida
    Dado que estou na tela C870T e informei uma data inicial da estimativa válida
    Quando informo, na data final da estimativa, um dia que não existe no mês ou um ano fora de 1994 a 2099
    Então vejo "* Data final da estimativa invalida *"
    E o cursor volta ao dia final da estimativa
    E nada é gravado

  Cenário: RN-06 — data inicial maior que a data final
    Dado que estou na tela C870T
    Quando informo uma data inicial da estimativa posterior à data final
    Então vejo "* Data inicial maior que data final *"
    E o cursor volta ao dia inicial da estimativa
    E nada é gravado

  Cenário: RN-07 — não há cardápio oficial na data limite informada
    Dado que estou na tela C870T e informei as duas datas da estimativa
    Quando informo, na data limite do cardápio, uma data que não é o fim de um cardápio oficial cadastrado na minha secretaria
    Então vejo "* Nao existem cardapios oficiais para esta data *"
    E o cursor volta ao dia limite do cardápio
    E nada é gravado

  Cenário: RN-07 — a data inicial do cardápio vem do cardápio oficial achado
    Dado que existe cardápio oficial cadastrado terminando na data limite que vou informar
    Quando envio os dados
    Então a data inicial do cardápio deixa de ser a que digitei
    E passa a ser a data inicial daquele cardápio oficial

  Cenário: RN-08 — já existe cardápio de estimativa na data inicial da estimativa
    Dado que estou na tela C870T e existe cardápio oficial na data limite do cardápio que vou informar
    E existe cardápio de estimativa cadastrado terminando na data inicial da estimativa que vou informar
    Quando envio os dados
    Então vejo "<- Cardapios ja cadastrados neste intervalo *"
    E o cursor volta ao dia inicial da estimativa
    E nada é gravado

  Cenário: RN-08 — já existe cardápio de estimativa na data final da estimativa
    Dado que estou na tela C870T e existe cardápio oficial na data limite do cardápio que vou informar
    E não existe cardápio de estimativa na data inicial da estimativa, mas existe na data final
    Quando envio os dados
    Então vejo "<- Cardapios ja cadastrados neste intervalo *"
    E o cursor volta ao dia inicial da estimativa
    E nada é gravado

  Cenário: RN-09 — os dados mudam entre a pergunta e a resposta
    Dado que já vi a pergunta de confirmação
    Quando altero uma das datas guardadas e respondo S
    Então a tela não aproveita a resposta
    E refaz as conferências e pergunta de novo "* Confirma copia dos cardapios <S/N> ? *"
    E nada é registrado antes de eu responder S

  Cenário: RN-09 — resposta diferente de S
    Dado que já vi a pergunta de confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a tela refaz as conferências e pede a mesma confirmação outra vez
    E nada é registrado

  Cenário: RN-10 — já existe um pedido em processamento
    Dado que existe uma solicitação de cópia de cardápios já registrada
    Quando confirmo a operação com a resposta S
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E a confirmação é desfeita e nenhuma solicitação nova é registrada
    E nada é gravado

  Cenário: RN-13 — a tela não toca nos cadastros
    Dado que confirmei a operação com a resposta S
    Quando a operação termina
    Então os cadastros de cardápios oficiais e de cardápios de estimativa continuam como estavam
    E o que passa a existir é a solicitação de processamento e o registro de auditoria
```
