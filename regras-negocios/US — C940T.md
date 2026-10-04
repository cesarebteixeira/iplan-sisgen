# US — C940T — Cópia dos cadastros da estimativa para o cardápio de um período

## Estória

Como **servidor de CRE**, quero **copiar para o cardápio de um período os cadastros que
já estavam planejados na estimativa de outro período**, para que **o cardápio do período
novo já nasça montado, sem redigitar cadastro por cadastro**.

A estimativa é o planejamento do período; o cardápio é o que passa a valer de fato.
Refazer à mão, cadastro por cadastro, aquilo que já foi planejado é onde o trabalho se
perde — e é esta a tela que dispara a cópia. Só que ela não copia na hora: registra o
pedido e o entrega ao processamento que roda fora da transação.

## Contexto

Jornada S000M → C000M → C800M → C900M → C940T.

Ator: servidor de CRE — informa o período de origem (a estimativa) e o período de destino
(o cardápio) e dispara a cópia.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. A C940T é aberta pela opção 6 do C900M, e os três
menus do caminho não gravam nada: apenas encaminham.

O que a tela usa da sessão — o órgão do servidor, a coordenação, a matrícula e o
privilégio — foi deixado pela entrada.

A tela não encadeia para nenhuma outra: ela reabre a si mesma nas duas passagens em que
muda de estado e não passa registro nem operação adiante. Também não há comparação com a
tela de origem que mude o comportamento dela: quem a chamou não decide em que modo ela
abre — ela abre sempre em alteração.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela não tem consulta: só alteração

A tela não abre em consulta. A cada apresentação ela repõe a operação em **alteração**;
se a operação que volta do terminal não for a de alteração, a tela recusa com
**\* Opcao nao disponivel. Use ALT \***, devolve o cursor ao campo da operação e para
ali — nada é conferido, nada é pedido e nada é copiado.

### RN-02 — Os dois períodos são informados em doze campos, todos numéricos

A tela pede dois períodos: o da **estimativa** (a origem) e o do **cardápio** (o
destino). Cada período tem data de início e data limite, e cada data é informada em três
campos — dia, mês e ano —, com o ano de quatro dígitos e o dia e o mês de dois. São
**doze campos**, todos numéricos: o que não for número é recusado no próprio campo,
antes de qualquer consulta ao cadastro, e a conferência para ali.

[?] Quando a recusa é em uma das três casas do início da estimativa, a tela não tem
posição de cursor definida para ela: o erro é acusado, mas o cursor não vai até o campo —
só nove dos doze campos têm posição. Pergunta ao site.

### RN-03 — O período da estimativa tem de estar cadastrado, e a tela o procura pela data limite

Com o órgão do servidor, a tela percorre as coordenações regionais escolares cadastradas
para esse órgão e, em cada uma, procura o período da estimativa cuja **data limite** seja
a informada como limite da estimativa. Não achando em nenhuma delas, a cópia não é
aceita: **\* Estimativa nao cadastrada \***, com o cursor na data limite da estimativa, e
a transação para ali — nada é pedido e nada é copiado. A data de início da estimativa não
é conferida como data de calendário: é a data limite que tem de corresponder a um período
cadastrado.

[?] A procura aceita o período achado em **qualquer** coordenação do órgão, e o pedido que
a tela registra não diz qual coordenação foi a que satisfez a conferência. Se a cópia vale
para todas as coordenações do órgão, o acervo não diz. Pergunta ao site.

### RN-04 — A data de início da estimativa em branco é completada pelo período cadastrado

O servidor pode informar só a data limite da estimativa: achado o período, se o ano do
início veio em branco, a tela o preenche com o dia, o mês e o ano do início daquele mesmo
período cadastrado.

### RN-05 — O período do cardápio não pode já estar registrado

Nas mesmas coordenações do órgão, a tela procura o período do cardápio cuja data limite
seja a informada para o cardápio. Havendo, a cópia é recusada com
**\* Salva ja cadastrada nesta data \***, com o cursor na data limite do cardápio, e nada
é pedido e nada é copiado.

[?] O cadastro desse período não é gravado por nenhuma tela do acervo: cinco programas o
enxergam, todos apenas declaram as rotinas de gravação e exclusão e nenhum as executa. Uma
tela irmã, que copia no sentido contrário, exige o oposto — recusa quando ele **não** está
registrado. Se nada o grava, um dos dois caminhos é inalcançável; o acervo não diz qual.
Pergunta ao site.

### RN-06 — As datas do cardápio têm de ser datas de calendário

As duas datas do cardápio são conferidas como datas de calendário: dia e mês que não
existem, ou ano fora da faixa admitida — de 1994 a 2099 —, são recusados. Se a recusa é na
data de início, a tela avisa **\* Data inicial da salva invalida \***, com o cursor na data
de início; se é na data limite, **\* Data final da salva invalida \***, com o cursor na
data limite. Em qualquer dos dois casos nada é pedido e nada é copiado.

### RN-07 — A data de início do cardápio não pode ser maior que a data limite

Se a data de início do cardápio for maior que a data limite do cardápio, a cópia é
recusada com **\* Data inicial maior que data final \***, com o cursor na data de início,
e nada é pedido.

### RN-08 — A cópia só segue com a confirmação S

Passadas as conferências, a tela guarda os dois períodos informados, pede
**\* Confirma copia dos cadastros <S/N> ? \*** e se reapresenta. Só a resposta **S** leva
adiante; qualquer outra resposta desfaz a confirmação e devolve a tela ao pedido dos
períodos. Trocar, entre a pergunta e a resposta, a data limite da estimativa ou qualquer
das datas do cardápio também desfaz a confirmação, e a tela volta a pedir os períodos:
nada é copiado.

[?] A conferência entre a pergunta e a resposta não inclui as três casas do início da
estimativa: trocar só essa data não desfaz a confirmação, e o valor guardado — o da
pergunta — é o que volta para a tela e o que vale. Pergunta ao site.

### RN-09 — Um pedido desta cópia por vez, em todo o sistema

Na resposta da confirmação, e antes de registrar qualquer coisa, a tela lê a fila de
pedidos pelo código desta cópia, **sem separar por órgão**: achando um pedido desta cópia
ainda em andamento, recusa com **\* Relatorio em processamento. Aguarde. \***, devolve o
cursor ao campo da resposta e desfaz a confirmação — o servidor precisa informar os
períodos de novo. O pedido sai da fila quando o processamento que copia o assume. A
conferência não é feita quando a tela pergunta, e sim quando recebe a resposta: a pergunta
é apresentada mesmo havendo um pedido em andamento.

[?] A procura é posicionada com o número do pedido zerado, e o pedido que a própria tela
registra leva um número calculado — o seguinte ao último da fila. Se a leitura exigir a
chave inteira, nenhum pedido pendente tem o número zerado e a recusa fica inalcançável; o
acervo não permite concluir qual das duas leituras o sistema faz. Pergunta ao site.

### RN-10 — A tela não copia: registra o pedido e o entrega ao processamento

Dos sete cadastros que a tela enxerga, esta transação grava **dois**: o lançamento na
trilha de auditoria e o pedido de processamento. As rotinas que gravariam ou apagariam o
período e os cadastros da cópia estão todas declaradas e **nenhuma é executada**. Quem
copia é o processamento que roda fora da transação — é para ele que a tela entrega o
pedido —, e o servidor não vê na tela o resultado da cópia.

### RN-11 — Toda cópia confirmada deixa rastro na auditoria

Confirmada a cópia, fica um registro na trilha de auditoria com o órgão, a coordenação, a
matrícula, a estação, a data e a hora da sessão, a tela que originou o pedido, o número do
processo — montado com o órgão e a data limite da estimativa — e o bloco dos dois períodos
informados como valor anterior; o valor posterior vai vazio. A operação fica registrada
como **inclusão**.

### RN-12 — O pedido de processamento e a mensagem de espera

O pedido recebe o número **seguinte ao do último pedido da fila**, o órgão, a matrícula, a
estação, o dia, o mês e o ano da sessão, sem coordenação; e no parâmetro que acompanha o
disparo vão os dois períodos informados, o correio eletrônico do servidor — tirado do
cadastro funcional —, a estação, a matrícula e uma cópia. Entregue o pedido ao
processamento fora da transação, a tela se reapresenta com
**\* Cadastro sendo atualizado \***: na transação nada do cardápio foi gravado, e o
servidor não acompanha o que o processamento faz.

[?] A entrega ao processamento está condicionada a uma configuração do ambiente: fora
dela o pedido fica na fila sem ser executado, e o acervo não diz o que se espera nesse
caso. Pergunta ao site.

### RN-13 — Nada é registrado sem a segurança de tela, de rota e de permissão

Na abertura, a tela lê o cadastro de títulos que a habilita e chama a segurança da tela;
depois, antes de conferir e de registrar, chama a rota e a permissão por operação, levando
a matrícula, o privilégio, o órgão e a coordenação da sessão. Qualquer resultado diferente
de aprovado limpa o status e encerra ali: nada é conferido, nada é gravado e nada é
auditado.

[?] As rotinas de segurança de tela, de rota e de permissão aparecem apenas declaradas
como comuns; o corpo delas não está nas fontes desta jornada, e a regra efetiva de
permissão não pode ser conferida por aqui. Pergunta ao site.

### RN-14 — A tela mostra a descrição do órgão e a data do sistema

Além dos dois períodos e da linha de mensagem, a tela exibe a descrição do órgão do
servidor e a data do sistema. As duas vêm da sessão — não são digitadas — e não mudam com
o que o servidor informa.

---

## Cenários BDD

```gherkin
Funcionalidade: Cópia dos cadastros da estimativa para o cardápio de um período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o órgão, a coordenação, a matrícula e o privilégio
    E tenho acesso à tela C940T

  Cenário: RN-01 — a tela não tem consulta
    Dado que estou na tela C940T
    Quando informo uma operação diferente de alteração
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor fica no campo da operação
    E nada é conferido, nada é pedido e nada é copiado

  Cenário: RN-02 — letra num campo de data
    Dado que estou na tela C940T
    Quando preencho com uma letra o dia, o mês ou o ano de uma das quatro datas
    Então o campo é recusado
    E a conferência para ali
    E nada é copiado

  Cenário: RN-03, RN-04 e RN-14 — informar um período de estimativa cadastrado
    Dado que existe um período da estimativa cadastrado com a data limite que vou informar
    Quando informo a data limite da estimativa deixando o ano do início em branco
    Então a tela mostra a descrição do meu órgão e a data do sistema
    E completa a data de início da estimativa com a do período cadastrado
    E me pede o período do cardápio

  Cenário: RN-03 — período da estimativa não cadastrado
    Dado que estou na tela C940T
    Quando informo uma data limite de estimativa que não corresponde a nenhum período cadastrado para o meu órgão
    Então vejo "* Estimativa nao cadastrada *"
    E o cursor fica na data limite da estimativa
    E a transação para ali
    E nada é pedido e nada é copiado

  Cenário: RN-05 — período do cardápio já registrado
    Dado que o período do cardápio que vou informar já está registrado
    Quando informo os dois períodos
    Então vejo "* Salva ja cadastrada nesta data *"
    E o cursor fica na data limite do cardápio
    E nada é pedido e nada é copiado

  Cenário: RN-06 — data de início do cardápio inválida
    Dado que estou na tela C940T
    Quando informo uma data de início do cardápio que não existe no calendário
    Então vejo "* Data inicial da salva invalida *"
    E o cursor fica na data de início do cardápio
    E nada é pedido e nada é copiado

  Cenário: RN-06 — data limite do cardápio inválida
    Dado que estou na tela C940T
    Quando informo uma data limite do cardápio fora da faixa admitida
    Então vejo "* Data final da salva invalida *"
    E o cursor fica na data limite do cardápio
    E nada é pedido e nada é copiado

  Cenário: RN-07 — início do cardápio maior que a data limite
    Dado que estou na tela C940T
    Quando informo a data de início do cardápio maior que a data limite do cardápio
    Então vejo "* Data inicial maior que data final *"
    E o cursor fica na data de início do cardápio
    E nada é pedido e nada é copiado

  Cenário: RN-08 — a pergunta de confirmação
    Dado que os dois períodos informados passam pelas conferências
    Quando envio os períodos
    Então vejo "* Confirma copia dos cadastros <S/N> ? *"
    E nada foi pedido e nada foi copiado ainda

  Cenário: RN-08 — resposta diferente de S
    Dado que estou vendo a pergunta de confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a confirmação é desfeita
    E a tela volta a pedir os períodos
    E nada é pedido e nada é copiado

  Cenário: RN-08 — troca das datas entre a pergunta e a resposta
    Dado que estou vendo a pergunta de confirmação
    Quando troco a data limite da estimativa ou uma data do cardápio e respondo S
    Então a confirmação é desfeita
    E a tela volta a pedir os períodos
    E nada é pedido e nada é copiado

  Cenário: RN-09 — já existe um pedido desta cópia em andamento
    Dado que existe um pedido desta cópia em andamento, de qualquer órgão
    Quando respondo S à pergunta de confirmação
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da resposta
    E a confirmação é desfeita
    E nada é pedido e nada é copiado

  Cenário: RN-10, RN-11 e RN-12 — confirmar a cópia
    Dado que os dois períodos passam pelas conferências e não há pedido em andamento
    Quando respondo S à pergunta de confirmação
    Então o sistema grava o registro na trilha de auditoria, com a operação como inclusão
    E registra o pedido de processamento com os dois períodos, a minha matrícula, a estação e a data
    E entrega o pedido ao processamento que roda fora da transação
    E vejo "* Cadastro sendo atualizado *"
    E nenhum cadastro do cardápio é gravado nesta transação

  Cenário: RN-13 — nada é registrado sem a segurança de tela, de rota e de permissão
    Dado que estou na tela C940T
    Quando a segurança da tela, a rota ou a permissão por operação não aprova
    Então a tela volta sem conferir nada
    E nada é gravado e nenhum registro de auditoria é criado

  Cenário: RN-14 — a tela mostra a descrição do órgão e a data do sistema
    Dado que estou na tela C940T
    Quando a tela se apresenta
    Então vejo a descrição do meu órgão e a data do sistema
    E nenhum dos dois é digitado por mim
```
