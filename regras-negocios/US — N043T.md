# US — N043T — Manutenção da data de entrega da nota fiscal

## Estória

Como **servidor da CRE**, quero **consultar a nota fiscal pelo seu número e ano e
manter a data de entrega das ordens que a compõem**, para que **a secretaria saiba
quando cada pedido de material foi efetivamente entregue**.

A nota fiscal só vira entrega quando a data de entrega de cada pedido é registrada:
é essa data que libera o acompanhamento do fornecimento e a conferência do que
ainda está pendente. Sem ela, o pedido fica em aberto indefinidamente, mesmo que a
mercadoria já tenha chegado. A tela também serve de consulta: mostra a nota, o
fornecedor, o órgão e a composição de pedidos da nota, e nessa consulta nada é
gravado.

## Contexto

Jornada S000M → N000M → N050M → N043T.

Ator: servidor de CRE — consulta a nota fiscal da sua secretaria pelo número e ano
e registra a data de entrega dos pedidos da nota.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O
caminho até a tela — qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio.

Os dois menus do caminho — o `N000M` e o `N050M` — só encaminham: não deixam nota
nem pedido na sessão e não gravam nada. O que a tela desta jornada usa da sessão — a
matrícula, o tipo de órgão e a coordenadoria regional de ensino — é o que a entrada
deixou.

As regras abaixo são só as da **tela desta jornada**. Nenhuma regra de tela anterior
se revelou aqui; a conferência da entrada está no anexo de evidências.

---

## Regras de negócio

### RN-01 — A tela é a agenda de entrega da nota fiscal

A tela guarda, por nota fiscal, a data de entrega das ordens que a compõem. A nota é
localizada pela combinação de **número da nota fiscal**, **dia, mês e ano de emissão**,
**coordenadoria regional de ensino**, **número do pedido auxiliar** e **ano da entrega
do pedido auxiliar**, **tipo de contrato**; a data de entrega pertence à ordem, cujo
registro é identificado pelo **ano da entrega** junto com o **número do pedido**.

A composição que a tela mantém tem capacidade de **100.000** registros — **capacidade**
(máximo esperado, parâmetro de dimensionamento), não volume cadastrado.

[?] O registro é chaveado também pelo **número e ano do pedido auxiliar**, mas o
caminho de consulta preenche esse par com zeros. O que significa "pedido auxiliar"
aqui — outro pedido da mesma nota, ou o pedido que originou o acumulado? O corpus não
diz.

### RN-02 — A consulta é somente leitura

Ao abrir a tela sem uma operação escolhida, ela entra em **consulta** e não grava nada:
mostra a nota, o fornecedor, o órgão e a composição de pedidos e termina aí. Percorrer
a tela, trocar de linha da composição e sair não altera registro nenhum.

### RN-03 — A tela só aceita consultar ou alterar

A operação da tela admite **consulta** ou **alteração** — as mesmas que a mensagem de
recusa nomeia como **CON** e **ALT**. Qualquer outra operação é recusada com
* Operacao nao disponivel. Use CON ou ALT *, com o cursor no campo de operação.

### RN-04 — O acesso é restrito à secretaria do usuário

A tela mostra e altera somente notas da **coordenadoria regional de ensino** do usuário.
Quando a nota pertence a outra coordenadoria, a operação é recusada com
* Usuario sem acesso a outro grupo * e nenhum dado da nota é apresentado.

### RN-05 — A nota é identificada pelo número e pelo ano de emissão

A tela exige o **número da nota fiscal** — sem ele, recusa com
* Informe o numero da nota fiscal * e põe o cursor nesse campo — e exige o **ano de
emissão da nota** — sem ele, recusa com * Informe o ano de entrega da nota fiscal * e
põe o cursor nesse campo.

[?] As duas recusas leem a mesma chave da nota (número e ano de emissão), mas a
segunda mensagem fala em "ano de entrega". O ano é um só, o de emissão da nota, como
mostra o registro da composição; se o ano de entrega é outro campo, a tela não o lê
nesse ponto.

### RN-06 — O fornecedor da nota tem de estar cadastrado

Se o código do fornecedor informado não estiver cadastrado, a tela recusa com
* Fornecedor nao cadastrado * e põe o cursor nesse campo.

### RN-07 — A subclasse de atividade tem de estar informada

Sem a **subclasse de atividade** informada, a tela recusa com * Informe o genero * e
não segue.

[?] A recusa é disparada pela falta da subclasse de atividade, mas a mensagem pede o
gênero. Ou a mensagem está no lugar trocado, ou a tela usa os dois códigos como se
fossem um só. Pergunta ao site.

### RN-08 — A subclasse de atividade e o gênero têm de estar cadastrados

Se o par **subclasse de atividade + gênero** não existir no cadastro de gênero de
material, a tela recusa com * Genero nao cadastrado * e não segue.

### RN-09 — A nota mostra a sua composição de pedidos

Localizada a nota, a tela apresenta a **composição de pedidos da nota** — até **10
linhas**, cada uma com **número do pedido**, **ano da entrega**, **órgão** e a **data
do órgão** (número, dia, mês e ano) e a **ação** da linha — junto do **fornecedor**
(razão social), do **operador** (nome), do **órgão filho** e da sua descrição, do
**tipo de contrato**, e, para pedido acumulado, do **processo** e da sua situação
(*Fechada*, *Pre Liq*, *Liquida* ou *Paga*).

[?] Quando a nota fiscal não tem nenhuma linha de composição, o programa acusa
* Nota fiscal sem composicao de pedidos * e volta à tela. Qual é o caminho que
preenche a composição a partir do pedido? Não foi possível segui-lo só pelo fonte da
tela desta jornada.

### RN-10 — Na composição, a linha já preenchida não se repete

Numa linha da composição que já tem **número do pedido**, a ação de linha não pode ser
*incluir*: a tela recusa com * Atualize linha preenchida * e põe o cursor na ação da
linha.

### RN-11 — A ordem acumulada não pode ser alterada pela ordem auxiliar

Quando o **órgão filho** da ordem acumulada da nota é diferente do **órgão filho** da
nota, a tela recusa com * Nao atualize. Pedido auxiliar do acumulado *, com o cursor na
ação da linha, e não grava.

### RN-12 — A ordem acumulada da nota tem de existir

Se a nota não tiver ordem acumulada registrada, a alteração não é aceita: a tela
recusa com * Nota fiscal nao cadastrada *, com o cursor no número da nota. A recusa
aparece tanto para a nota cujo pedido é acumulado quanto para a nota cujo pedido não é
acumulado.

### RN-13 — A data de entrega só é atualizada para pedido acumulado

A alteração da data de entrega exige a **data de entrega** preenchida — sem ela, a tela
recusa com * Informe data da entrega * e põe o cursor nessa data —, e exige que a nota
seja de **pedido acumulado**: se for nota de pedido não acumulado, a tela recusa com
* Nota nao e de pedido acumulado * e põe o cursor no número da nota.

### RN-14 — A data de entrega é conferida contra a nota e contra o pedido

A data de entrega informada tem de ser **data de calendário válida** — senão a tela
recusa com * Data da entrega invalida * —, tem de ter o **ano igual ao da emissão da
nota** — senão recusa com * Ano da entrega invalido * —, e não pode ser **anterior à
data da nota acumulada**: a tela recusa com
* Data da entrega < data da nota acumulada *, com o cursor na data da entrega.

[?] O ramo que ainda recusa a entrega anterior ao início do pedido
(* Data da entrega < data do pedido *) compara a data informada com uma data de início
lida do cadastro do pedido. A tela não mostra essa data de início em campo nenhum.
Não foi possível determinar de que pedido é a data com que a tela compara. Pergunta ao
site.

## Cenários BDD

```gherkin
Funcionalidade: Manutenção da data de entrega da nota fiscal

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N043T

  Cenário: Consultar uma nota fiscal da minha secretaria
    Dado que informei o número, o dia, o mês e o ano de emissão, a coordenadoria regional de ensino e o tipo de contrato da nota
    Quando confirmo a consulta
    Então a tela mostra a nota, o fornecedor, o operador, o órgão filho e a composição de pedidos da nota
    E nada é gravado

  Cenário: Abrir a tela sem operação escolhida abre em consulta
    Dado que abri a tela sem escolher operação
    Quando a tela termina de montar a consulta
    Então a tela abre em consulta
    E nada é gravado

  Cenário: Recusar operação que não seja consulta nem alteração
    Dado que escolhi uma operação diferente de consulta e de alteração
    Quando confirmo
    Então a tela recusa com * Operacao nao disponivel. Use CON ou ALT *
    E o cursor fica no campo de operação
    E nada é gravado

  Cenário: Recusar nota de outra coordenadoria regional de ensino
    Dado que informei a nota de uma coordenadoria regional de ensino diferente da minha
    Quando confirmo
    Então a tela recusa com * Usuario sem acesso a outro grupo *
    E nenhum dado da nota é apresentado
    E nada é gravado

  Cenário: Exigir o número da nota fiscal
    Dado que deixei o número da nota fiscal em branco
    Quando confirmo
    Então a tela recusa com * Informe o numero da nota fiscal *
    E o cursor fica no número da nota fiscal
    E nada é gravado

  Cenário: Exigir o ano de emissão da nota fiscal
    Dado que informei o número da nota fiscal e deixei o ano em branco
    Quando confirmo
    Então a tela recusa com * Informe o ano de entrega da nota fiscal *
    E o cursor fica no ano da nota fiscal
    E nada é gravado

  Cenário: Recusar fornecedor não cadastrado
    Dado que informei o número e o ano de emissão da nota e um código de fornecedor não cadastrado
    Quando confirmo
    Então a tela recusa com * Fornecedor nao cadastrado *
    E o cursor fica no código do fornecedor
    E nada é gravado

  Cenário: Exigir a subclasse de atividade
    Dado que deixei a subclasse de atividade em branco
    Quando confirmo
    Então a tela recusa com * Informe o genero *
    E nada é gravado

  Cenário: Recusar subclasse de atividade e gênero não cadastrados
    Dado que informei uma subclasse de atividade e um gênero que não existem no cadastro
    Quando confirmo
    Então a tela recusa com * Genero nao cadastrado *
    E nada é gravado

  Cenário: Mostrar a composição de pedidos da nota
    Dado que a nota fiscal existe e tem composição de pedidos
    Quando confirmo a consulta
    Então a tela mostra até 10 linhas de composição, cada uma com o número do pedido, o ano da entrega, o órgão, a data do órgão e a ação da linha
    E mostra a razão social do fornecedor e o nome do operador
    E nada é gravado

  Cenário: Recusar incluir linha já preenchida da composição
    Dado que a linha da composição já tem número do pedido
    Quando escolho incluir nessa linha
    Então a tela recusa com * Atualize linha preenchida *
    E o cursor fica na ação da linha
    E nada é gravado

  Cenário: Recusar alterar a ordem acumulada pela ordem auxiliar
    Dado que o órgão filho da ordem acumulada da nota é diferente do órgão filho da nota
    Quando confirmo a alteração
    Então a tela recusa com * Nao atualize. Pedido auxiliar do acumulado *
    E o cursor fica na ação da linha
    E nada é gravado

  Cenário: Recusar nota sem ordem acumulada registrada
    Dado que a nota fiscal informada não tem ordem acumulada registrada
    Quando confirmo
    Então a tela recusa com * Nota fiscal nao cadastrada *
    E o cursor fica no número da nota fiscal
    E nada é gravado

  Cenário: Exigir a data de entrega para atualizar
    Dado que a nota é de pedido acumulado e deixei a data de entrega em branco
    Quando confirmo a alteração
    Então a tela recusa com * Informe data da entrega *
    E o cursor fica na data de entrega
    E nada é gravado

  Cenário: Recusar atualizar nota de pedido não acumulado
    Dado que a nota informada é de pedido não acumulado
    Quando confirmo a alteração
    Então a tela recusa com * Nota nao e de pedido acumulado *
    E o cursor fica no número da nota fiscal
    E nada é gravado

  Cenário: Recusar data de entrega que não é data de calendário
    Dado que a nota é de pedido acumulado
    Quando informo uma data de entrega que não existe no calendário
    Então a tela recusa com * Data da entrega invalida *
    E o cursor fica na data de entrega
    E nada é gravado

  Cenário: Recusar ano da entrega diferente do ano da nota
    Dado que a nota é de pedido acumulado
    Quando informo uma data de entrega cujo ano é diferente do ano de emissão da nota
    Então a tela recusa com * Ano da entrega invalido *
    E o cursor fica no ano da data de entrega
    E nada é gravado

  Cenário: Recusar data de entrega anterior à data da nota acumulada
    Dado que a nota é de pedido acumulado
    Quando informo uma data de entrega anterior à data da nota acumulada
    Então a tela recusa com * Data da entrega < data da nota acumulada *
    E o cursor fica na data de entrega
    E nada é gravado

  Cenário: Atualizar a data de entrega de uma ordem da nota
    Dado que a nota é de pedido acumulado e a ordem não é a auxiliar do acumulado
    E que a linha da composição já tem o número do pedido
    Quando informo uma data de entrega de calendário válido, do ano da nota e não anterior à data da nota acumulada
    Então a tela grava a data de entrega na ordem da nota
    E a alteração fica registrada com o operador, a data e a hora
```
