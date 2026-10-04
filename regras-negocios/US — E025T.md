# US — E025T — Registrar o recebimento e o cancelamento dos itens do pedido

## Estória

Como **servidor da CRE**, quero **confirmar o recebimento dos itens de um pedido de
merenda escolar e cancelar quantidades já recebidas**, para que o pedido fique com
o que foi entregue, o que ainda falta e o que foi cancelado na medida certa.

É esta tela que fecha o pedido: ela decide se cada item está recebido por completo
ou ainda acumulado, aprova o pedido que já chegou e fecha o que já foi recebido e
cancelado. Sem ela o pedido fica parado em "pendente de distribuição" e as
quantidades da distribuição nunca voltam a bater com o que chegou na escola.

## Contexto

Jornada S000M → E000M → E010M → E025T.

Ator: servidor de CRE — acompanha os pedidos de merenda da sua coordenadoria:
confere o que já foi distribuído, recebe os itens e registra o cancelamento das
quantidades recebidas.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio.

A E010M é o painel de pedidos da jornada: ela consulta os pedidos por período de
entrega, tipo e situação, e é dela que sai a opção que abre esta tela. Ela deixa na
sessão o último pedido consultado — ano de início, número do pedido e os itens — e
é esse pedido que esta tela carrega ao abrir.

Esta tela **não é um menu**: ela não encadeia para outra tela e a jornada termina
nela. Quem a abre por outro caminho é a tela de manutenção do pedido, que passa o
registro do pedido adiante sem passar por menu; por isso o **modo de operação
desta tela não é escolhido nela** — vem de quem a chamou (RN-03).

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela identifica o pedido pelo órgão, pela coordenadoria, pelo número, pelo ano e pelo fornecedor

O pedido é localizado por cinco dados: o **órgão filho (SDI)**, com 8 dígitos; a
**coordenação regional escolar (CRE)**, com 2 dígitos; o **número do pedido**, com
6 dígitos; o **ano da entrega**, com 4 dígitos; e o **código do fornecedor**, com 4
dígitos. Todos passam pela conferência numérica do sistema antes de qualquer
consulta: campo em branco vira zero, os zeros à esquerda são descartados e o que
não for número é recusado — e o que não passa por essa conferência não chega ao
cadastro.

Há ainda o **código do operador**, com 4 dígitos, que não se digita: é o operador
do pedido, buscado no cadastro e mostrado com o nome.

### RN-02 — A grade tem 9 linhas, e cada linha tem subclasse, gênero, quantidades e ação

Os itens do pedido aparecem em uma grade de **9 linhas**, e o sistema fixa esse
mesmo limite nas passagens da tela (a de abertura, a de conferência e a de
gravação). Cada linha tem **cinco dados operáveis**: a **subclasse** (2 dígitos),
o **código do gênero** (5 dígitos), a **quantidade** (10 posições, com 3 casas
decimais) e uma **ação** de 1 caractere. O sistema preenche, além desses, o nome
resumido do gênero, o tipo de contrato, a situação do item e as quantidades de
pendente e de recebido — nove valores que a tela mostra e o usuário não digita.

### RN-03 — A tela só opera em ALT (alterar) ou CON (consultar), e quem escolhe a operação é a tela que a chamou

A operação aceita apenas **alteração** e **consulta**; qualquer outra é recusada
com **\* Operacao nao disponivel. Use ALT ou CON \***, com o cursor de volta no
campo da operação, e nada é gravado. Em branco também é recusada: a tela exige que
a operação chegue preenchida.

A operação não é escolhida nesta tela. Ela chega pela área de trabalho da sessão,
que é o que as telas encadeadas usam para passar o registro e a operação adiante —
e o programa **não escreve** "ALT" nem "CON" nesse campo em nenhum ponto: só
confere e usa o que chegou. Quem abre a tela pela opção do painel de pedidos chega
com a última consulta na área de trabalho; quem a abre pela tela de manutenção do
pedido chega com a consulta do pedido selecionado. Só com "alt" a tela grava
(RN-04 e RN-05).

[?] A operação vem da área de trabalho da sessão, mas nenhuma das três telas deste
lote que abrem esta tela escreve "alt" nesse campo — as duas telas de manutenção
escrevem a consulta do pedido consultado. Não é possível dizer, pelos fontes do
lote, por qual caminho a tela abriria em alteração para gravar. Se em algum caminho
ela abrir em consulta onde deveria abrir em alteração, a tela não falha: apenas não
deixa gravar. Pergunta ao site.

### RN-04 — A tela confere a autorização do servidor na abertura e antes de gravar

Ao abrir, o sistema confere a autorização do servidor para esta tela e para a
operação que chegou; sem o registro de acesso, a sessão é devolvida à entrada. Na
passagem que grava, a conferência é refeita com a operação da tela. A autorização é
por tela e por operação: há uma marca separada para incluir, alterar, excluir e
consultar.

### RN-05 — O caminho que grava exige a alteração; a consulta não grava nada

A passagem que grava começa desviando de propósito quando a operação não é
alteração: em consulta, a tela apenas lê e mostra, nenhuma gravação acontece, e o
único efeito é interno à sessão — o pedido consultado fica na área de trabalho para
a alteração seguinte. É por isso que alterar exige ter consultado antes: a tela só
atualiza o pedido que a última consulta deixou carregado.

### RN-06 — O número do pedido é obrigatório, e sem ele não se chega ao cadastro

Sem número do pedido — e sem o pedido da última consulta — a recusa é
**\* Informe o numero do pedido \***, com o cursor no campo, e nada é lido. Se a
consulta já tinha deixado um pedido, a tela usa esse número, dispensando a
digitação. O número digitado tem 6 dígitos e é acrescido do ano da entrega para
formar a chave do pedido.

### RN-07 — O órgão e a coordenadoria são obrigatórios, e o servidor só alcança o próprio órgão e o próprio grupo

Informar o órgão filho é obrigatório: em branco, e sem um pedido já consultado, a
recusa é **\* Informe o orgao \***. Se a entrada deixou um órgão preso ao servidor,
a tela só aceita esse órgão: informar outro é recusado com
**\* Usuario sem acesso a outro orgao \***. A mesma amarração vale para a
coordenação regional escolar: se o servidor tem coordenação, o pedido tem de ser
dela, senão a recusa é **\* <- Usuario sem acesso ao grupo deste pedido \***.

### RN-08 — O pedido tem de existir, não pode estar excluído, acumulado, pendente ou fechado

Lido o cabeçalho do pedido, ele passa por cinco peneiras, nesta ordem:

| peneira | recusa |
| --- | --- |
| o pedido está cadastrado para o órgão, a coordenadoria e o ano informados | \* Pedido nao cadastrado \* |
| o pedido não está excluído | \* Pedido excluido \* |
| o pedido não é acumulado | \* Pedido acumulado \* |
| o pedido não está pendente de distribuição | \* Pedido pendente de distribuicao \* |
| o pedido não está pendente de aprovação | \* Pedido pendente de aprovacao \* |

O pedido **fechado** não é recusado por esta sequência — ele segue para o
carregamento e, adiante, quem recusa é a regra do cancelamento (RN-13). Cada
recusa devolve o cursor ao campo do número do pedido e nada é gravado.

### RN-09 — Alguns dados do pedido não se digitam: vêm dos cadastros

Encontrado o pedido, o sistema copia para a tela o **nome do órgão**, o **nome do
fornecedor**, o **nome do operador**, o **indicador de cartão**, os **períodos de
início e de limite** do pedido, a **situação** do pedido e as **quantidades de
pendente e recebido** de cada item. A situação do pedido é mostrada por extenso —
**APROVADO** para o pedido aprovado e **FECHADO** para o pedido fechado. Quem
decide o que aparece na grade é o pedido e os cadastros, não o que foi digitado.

### RN-10 — O cancelamento é linha a linha: só a linha da página com a ação de cancelar é cancelada

O cancelamento não é o pedido inteiro: é **uma linha** — o item que está na página
corrente — e exige que a linha esteja marcada com a **ação de cancelar**. O sistema
grava o cancelamento no item daquela linha e o seu efeito de volta no pedido.

### RN-11 — Cancelar pergunta a quantidade a cancelar, e ela não pode ser zero

Na linha marcada para cancelar, o sistema lê a **quantidade a cancelar**. Se ela for
zero, a recusa é **\* Estorne quantidade de linha preenchida \***, com o cursor na
quantidade da linha, e nada é gravado. Depois disso o item é lido no cadastro do
pedido por subclasse e gênero; não existindo, a recusa é **\* Genero acumulado
neste pedido \*** e nada é gravado.

### RN-12 — A quantidade a cancelar passa por quatro conferências, nesta ordem

| conferência | recusa |
| --- | --- |
| a quantidade não é a que já foi cancelada no item | \* Quantidade ja estornada neste pedido \* |
| o recebido somado ao que será cancelado não passa do pedido | \* Recebida + estornada maior que pedida \* |
| a quantidade é múltiplo inteiro da fração permitida para o gênero | \* Quant. fracionada invalida para este genero \* |
| o pedido ainda tem saldo dentro da permissão do contrato, da coordenadoria, do fornecedor e do período | \* Quantidade insuficiente na permissao \* |

Cada recusa devolve o cursor à quantidade da linha e nada é gravado. A terceira
conferência precisa do cadastro do gênero: o sistema lê a fração permitida pelo
gênero; não achando o gênero no cadastro, ele segue sem a conferência da fração.

### RN-13 — Pedido com o recebido igual ao pedido não tem o que cancelar

Se o pedido está fechado e a linha pede cancelamento, a recusa é
**\* Nao existem quantidades a estornar \***, com o cursor na ação da linha, e nada
é gravado.

### RN-14 — O cancelamento grava no item e devolve o saldo à permissão do contrato

Passando as conferências, o cancelamento grava: no item do pedido, o **recebido
igual ao que foi cancelado**, o **tipo de contrato** de onde a quantidade saiu, a
**data do cancelamento** e a **situação** que resultar (RN-15); e, na permissão do
contrato, o saldo pendente volta a valer. Cada gravação deixa o seu registro na
auditoria.

### RN-15 — O cancelamento fecha o item ou o deixa acumulado, e o pedido acompanha

Depois do cancelamento o sistema compara o recebido com o pedido: **igual fecha o
item**, diferente deixa o item **acumulado**, à espera do resto. Terminada a
gravação, se todos os itens ficaram fechados o pedido também é fechado; se algum
ficou acumulado, o pedido continua aberto.

### RN-16 — A aprovação decide o pedido pelo que foi distribuído, e não pelo que está sendo cancelado

Quando o pedido está sem item acumulado, a tela decide se ele já pode ser aprovado:
o sistema recorre aos itens do pedido e compara, item a item, o recebido com o
pedido.

- Se **todo** item já está recebido, o pedido é **aprovado** e passa a aguardar
  distribuição — a tela avisa com a situação **APROVADO**.
- Se algum item ainda não foi recebido, o pedido continua **acumulado**, à espera.
- Se havia item com o recebido igual ao pedido (o caso de adiantar o recebimento),
  a tela apenas confere a situação e **não** toca no status do pedido.

Essa decisão acontece antes do cancelamento da linha e não depende dele.

### RN-17 — O cancelamento pode fechar o pedido por inteiro

Voltando a percorrer os itens depois dos cancelamentos, o sistema procura algum
item acumulado: não achando nenhum, e se a tela estiver em alteração, o pedido é
**fechado** — a situação passa a **FECHADO**. A decisão depende dos itens, não do
que foi cancelado na página.

### RN-18 — Toda gravação deixa rastro na auditoria

Cada item gravado e cada mudança de status do pedido gera um registro na **trilha
de auditoria**: o cadastro que a originou (o item do pedido, a permissão do
contrato ou o cabeçalho do pedido), a operação, o tipo de órgão, o órgão filho, a
coordenação regional escolar, a matrícula funcional, a estação, a sessão, a data e
a hora, e os valores **antes e depois**.

### RN-19 — Falha de banco interrompe a operação e avisa

Todo acesso a dados testa o erro do banco. A falha de leitura e a de gravação
viram o aviso de erro correspondente — os dois despachados pela rotina de
comunicação do sistema — e a transação para ali, sem completar o resto.

---

## Cenários BDD

```gherkin
Funcionalidade: Registrar o recebimento e o cancelamento dos itens do pedido

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E025T

  Cenário: RN-01, RN-02, RN-05, RN-08 e RN-09 — consultar um pedido
    Dado que estou na tela E025T com a operação CON
    E informo o órgão filho, a coordenação regional escolar, o número do pedido, o ano da entrega e o fornecedor de um pedido do meu escopo
    Quando confirmo a consulta
    Então vejo o nome do órgão, o nome do fornecedor, o nome do operador, a situação do pedido e os períodos de início e de limite
    E vejo, nas 9 linhas da grade, a subclasse, o gênero, o tipo de contrato, o pendente, o recebido e a quantidade a cancelar
    E nada é gravado

  Cenário: RN-01 — campo não numérico
    Quando informo no órgão filho, na coordenadoria, no número do pedido, no ano da entrega ou no fornecedor algo que não é número
    Então o campo é recusado antes de qualquer consulta
    E o cadastro não é lido

  Cenário: RN-03 — operação não disponível
    Dado que estou na tela E025T
    Quando a operação não é ALT nem CON
    Então vejo "* Operacao nao disponivel. Use ALT ou CON *"
    E nada é gravado

  Cenário: RN-05 — alterar sem ter consultado antes
    Dado que estou na tela E025T com a operação ALT
    Quando confirmo com um pedido diferente do que a última consulta deixou carregado
    Então nada é gravado

  Cenário: RN-06 — pedido não informado
    Dado que a última consulta não deixou nenhum pedido carregado
    Quando confirmo sem informar o número do pedido
    Então vejo "* Informe o numero do pedido *"
    E nada é lido

  Cenário: RN-07 — órgão não informado
    Dado que a última consulta não deixou nenhum pedido carregado
    Quando confirmo sem informar o órgão filho
    Então vejo "* Informe o orgao *"
    E nada é lido

  Cenário: RN-07 — órgão fora do meu escopo
    Dado que o meu usuário está preso a um órgão filho
    Quando informo outro órgão filho
    Então vejo "* Usuario sem acesso a outro orgao *"
    E nada é lido

  Cenário: RN-07 — pedido de outro grupo
    Dado que o meu usuário tem coordenação regional escolar
    Quando informo um pedido de outra coordenadoria
    Então vejo "* <- Usuario sem acesso ao grupo deste pedido *"
    E nada é lido

  Cenário: RN-08 — pedido não cadastrado
    Quando informo um pedido que não existe para o órgão, a coordenadoria e o ano informados
    Então vejo "* Pedido nao cadastrado *"
    E nada é gravado

  Cenário: RN-08 — pedido excluído
    Quando informo um pedido cadastrado como excluído
    Então vejo "* Pedido excluido *"
    E nada é gravado

  Cenário: RN-08 — pedido acumulado
    Quando informo um pedido acumulado
    Então vejo "* Pedido acumulado *"
    E nada é gravado

  Cenário: RN-08 — pedido pendente de distribuição
    Quando informo um pedido pendente de distribuição
    Então vejo "* Pedido pendente de distribuicao *"
    E nada é gravado

  Cenário: RN-08 — pedido pendente de aprovação
    Quando informo um pedido pendente de aprovação
    Então vejo "* Pedido pendente de aprovacao *"
    E nada é gravado

  Cenário: RN-10, RN-14, RN-15 e RN-18 — cancelar a quantidade de uma linha
    Dado que consultei um pedido com operação ALT
    E a linha do item está marcada com a ação de cancelar
    E o saldo a cancelar é múltiplo da fração permitida para o gênero e cabe na permissão do contrato
    Quando confirmo
    Então o recebido do item passa a ser o que foi cancelado, com a data e o tipo de contrato de origem
    E o saldo da permissão do contrato é devolvido
    E cada gravação fica registrada na auditoria

  Cenário: RN-11 — cancelar sem informar a quantidade
    Dado que consultei um pedido com operação ALT
    E a linha está marcada com a ação de cancelar e sem quantidade
    Quando confirmo
    Então vejo "* Estorne quantidade de linha preenchida *"
    E nada é gravado

  Cenário: RN-11 — item que não está no pedido
    Dado que consultei um pedido com operação ALT
    E a linha está marcada com a ação de cancelar e com um item que não está no pedido
    Quando confirmo
    Então vejo "* Genero acumulado neste pedido *"
    E nada é gravado

  Cenário: RN-12 — quantidade já cancelada
    Dado que consultei um pedido com operação ALT
    Quando a quantidade a cancelar é a que já foi cancelada naquele item
    Então vejo "* Quantidade ja estornada neste pedido *"
    E nada é gravado

  Cenário: RN-12 — recebido mais cancelado maior que o pedido
    Dado que consultei um pedido com operação ALT
    Quando o recebido somado ao que será cancelado passa da quantidade pedida
    Então vejo "* Recebida + estornada maior que pedida *"
    E nada é gravado

  Cenário: RN-12 — quantidade fracionada inválida
    Dado que consultei um pedido com operação ALT
    Quando a quantidade a cancelar não é múltiplo da fração permitida para o gênero
    Então vejo "* Quant. fracionada invalida para este genero *"
    E nada é gravado

  Cenário: RN-12 — quantidade insuficiente na permissão
    Dado que consultei um pedido com operação ALT
    Quando a quantidade a cancelar passa do saldo da permissão do contrato
    Então vejo "* Quantidade insuficiente na permissao *"
    E nada é gravado

  Cenário: RN-13 — pedido sem quantidade a cancelar
    Dado que consultei um pedido com operação ALT
    E o recebido do pedido é igual ao pedido
    Quando a linha pede cancelamento
    Então vejo "* Nao existem quantidades a estornar *"
    E nada é gravado

  Cenário: RN-15 e RN-17 — o cancelamento fecha o pedido
    Dado que consultei um pedido com operação ALT
    E o cancelamento da última linha completa o que faltava
    Quando confirmo
    Então o item fica fechado
    E o pedido é fechado
    E a situação mostrada passa a FECHADO

  Cenário: RN-15 — o cancelamento deixa o item acumulado
    Dado que consultei um pedido com operação ALT
    E o cancelamento não completa o que faltava
    Quando confirmo
    Então o item fica acumulado, à espera do resto
    E o pedido continua aberto

  Cenário: RN-16 — aprovar o pedido que já chegou por inteiro
    Dado que consultei um pedido sem item acumulado
    E todos os itens estão recebidos
    Quando confirmo
    Então o pedido é aprovado e passa a aguardar distribuição
    E a situação mostrada passa a APROVADO

  Cenário: RN-16 — o pedido que ainda não chegou por inteiro
    Dado que consultei um pedido sem item acumulado
    E algum item ainda não está recebido
    Quando confirmo
    Então o pedido continua acumulado, à espera

  Cenário: RN-04 — operação sem autorização
    Dado que não tenho permissão para esta tela ou para a operação que chegou
    Quando confirmo
    Então vejo a mensagem de recusa da segurança
    E nada é gravado

  Cenário: RN-19 — falha de banco na gravação
    Dado que a gravação do item falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com o aviso de erro do sistema
    E o item não é considerado gravado
```
