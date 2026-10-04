# US — S065T — Liberação de telas e relatórios por nível de acesso

## Estória

Como **servidor de CRE responsável pela segurança do acesso**, quero **definir,
para cada nível de acesso, o que ele pode consultar, incluir, alterar e excluir
numa tela ou num relatório**, para que **cada nível alcance exatamente o que a
secretaria decidiu, e nada além disso**.

O nível de acesso é o que abre as telas do sistema para cada servidor, e é esta
tela que escreve o que cada nível pode fazer em cada tela ou relatório. Sem ela, a
liberação não acompanha o sistema: mudar o alcance de um nível deixa de ser
possível sem mexer no programa, e um nível continua fazendo o que não deveria ou
deixa de fazer o que precisa.

## Contexto

Jornada S000M → S001M → S004M → S065T.

Ator: servidor de CRE — escolhe uma tela ou um relatório e mantém, para cada nível
de acesso, as quatro liberações de operação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

As duas telas entre o menu principal e esta — `S001M` e `S004M` — são menus: elas
só apontam a tela seguinte e não deixam registro nem operação para esta tela. Por
isso esta tela abre sempre em consulta, e o modo de operação é decidido nela
mesma, não por quem a abriu. Esta tela também não encadeia para outra: a jornada
termina nela.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela mantém as liberações de cada nível de acesso para uma tela ou um relatório

Para uma tela (tipo **T**) ou um relatório (tipo **R**), identificado pelo seu
código, esta tela mantém o que cada nível de acesso pode fazer: **consultar**,
**incluir**, **alterar** e **excluir**. Cada linha mostra o código e a descrição do
nível de acesso e as quatro liberações daquele nível para a tela ou o relatório
escolhido. A lista comporta 13 níveis de uma vez.

[?] A lista fixa 13 linhas e o cadastro de níveis é dimensionado para 100. O fonte
não traz paginação para esta tela: se houver mais de 13 níveis cadastrados, não se
conclui do fonte se os demais são alcançáveis por aqui. Pergunta ao site.

### RN-02 — A tela só opera em consulta ou em alteração, e quem a chama não decide o modo

Esta tela não inclui nem exclui tela ou relatório: ela só **consulta** e
**altera** liberações. Com qualquer outra operação, o sistema recusa com
**\* Opcao nao disponivel. Use ALT ou CON \***. A tela abre sempre em consulta, e o
menu que a abre não passa operação nenhuma: o modo é decidido nela, e não pela tela
de origem.

[?] A recusa compara a operação com os códigos de consulta e de alteração, mas o
aviso manda o servidor usar as teclas **ALT** e **CON**. Ou o terminal traduz a
tecla antes de enviar, ou o aviso está desalinhado da conferência — o fonte não
decide qual dos dois. Pergunta ao site.

[?] A máscara desta tela não está no acervo: só se conhecem os campos que o
programa transporta. O que o servidor vê na tela — títulos, colunas e o campo em
que a operação é informada — não se confirma no fonte. Pergunta ao site.

### RN-03 — A tela ou o relatório é identificado pelo tipo e pelo código

Para consultar, o servidor informa o **tipo** — T para tela, R para relatório — e o
**código** da tela ou do relatório. Faltando o tipo, ou informado um valor fora de
T e R, a recusa é **\* Informe T para tela ou R para relatorio \***; faltando o
código, **\* Informe o codigo da tela ou relatorio \***. O nome da tela ou do
relatório e o nome do módulo — que sai da primeira letra do código — são mostrados
junto com a lista.

### RN-04 — A tela ou o relatório tem de estar cadastrado

O par tipo e código é procurado no cadastro de telas e relatórios. Não achando o
par — ou achando um registro retirado do cadastro —, a recusa é
**\* Tela / relatorio nao cadastrado \***. Desse cadastro vêm também o nome da tela
ou do relatório e a marca de que ela permite ou não atualização.

### RN-05 — O servidor só consulta o que ele próprio alcança

O nível de acesso do servidor precisa ter liberação para a tela ou o relatório
informado: procurado o par tipo e código no cadastro de liberações do nível do
servidor, a falta recusa com **\* Usuario sem acesso a esta tela/relatorio \***.
É o mesmo cadastro que a entrada consulta para deixar ou não abrir uma tela.

### RN-06 — A alteração exige que o mesmo par tenha sido consultado antes

A consulta guarda o tipo e o código consultados. Ao alterar, o sistema compara o
que está na tela com o que ficou guardado: sendo outro par, recusa com
**\* Consulte antes de alterar \***. Por isso a manutenção das liberações de uma
tela começa, sempre, por uma consulta a essa mesma tela.

### RN-07 — O servidor mantém os níveis abaixo do seu; o seu próprio, só com privilégio

O nível do servidor é o mais alto entre os vínculos da sua matrícula. A manutenção
de um nível de acesso só passa quando o nível da linha é **menor** que o do
servidor; ou é **igual** ao do servidor e ele tem a marca de **privilégio**. Nível
acima do seu é sempre recusado, e o próprio nível sem privilégio também — nos dois
casos com **\* Seu nivel de acesso nao permite esta operacao \***.

[?] O nível do servidor sai de uma varredura dos vínculos da matrícula com o tipo
de órgão zerado, e fica o maior valor encontrado. Se essa leitura alcança todos os
vínculos — como a entrada faz para contar as secretarias —, o servidor fica com o
maior nível entre eles; se ela procura exatamente o tipo de órgão zero, fica com
zero e nenhum servidor sem privilégio passa na conferência. O que a leitura faz com
a chave zerada não está no acervo. Pergunta ao site.

### RN-08 — A ação da linha exige a operação liberada para o próprio servidor nesta tela

Antes de aplicar a ação de uma linha, o sistema confere, no cadastro de liberações
do nível do servidor, se ele pode fazer aquela operação **nesta tela de
liberações**: incluir uma liberação exige a inclusão liberada aqui, alterar exige a
alteração, excluir exige a exclusão. Faltando, a recusa é
**\* Acesso negado para esta operacao \*** e nada é gravado.

### RN-09 — Cada linha traz a sua ação; linha sem nível ou sem ação conhecida é ignorada

Cada linha tem o nível de acesso, as quatro liberações e a ação pretendida:
**I** inclui a liberação daquele nível para a tela ou o relatório, **A** altera a
liberação existente, **E** exclui. Linha sem o nível preenchido, ou com ação
diferente de I, A e E, é ignorada em silêncio — sem aviso e sem gravação.

### RN-10 — Inclusão: a liberação não pode existir e a consulta tem de ser informada

Para incluir a liberação de um nível, o sistema procura o par nível + tela ou
relatório no cadastro de liberações. Achando, recusa com
**\* Codigo ja cadastrado neste nivel de acesso \***. Não achando, exige que pelo
menos a liberação de **consulta** esteja marcada: sem nenhuma autorização, recusa
com **\* Informe autorizacoes para o codigo \***.

### RN-11 — Alteração e exclusão: a liberação tem de existir

Para alterar ou excluir, o sistema faz a mesma procura pelo par nível + tela ou
relatório; não achando, recusa com
**\* Codigo nao cadastrado neste nivel de acesso \***.

### RN-12 — Numa tela sem opção de atualização, e num relatório, só se libera a consulta

Se a tela está cadastrada como **sem opção de atualização** e o servidor marcou
alguma liberação de atualização — incluir, alterar ou excluir —, o sistema recusa
com **\* Tela sem opcao de atualizacao \***; marcar só a consulta é aceito. Num
**relatório**, as três liberações de atualização são descartadas: só a consulta
fica gravada.

### RN-13 — Liberar uma atualização libera a consulta junto

Marcar incluir, alterar ou excluir faz a liberação de **consulta** ser marcada
junto: não existe liberação de atualização sem consulta. Qualquer marca informada
numa dessas quatro colunas vale como liberação.

### RN-14 — Alterar uma linha deixando-a sem nenhuma liberação apaga a liberação

Na alteração, se a linha ficar sem a liberação de consulta — e, portanto, sem
nenhuma das quatro —, o sistema não grava a linha vazia: **exclui** a liberação
daquele nível para a tela ou o relatório.

[?] A inclusão exige a liberação de consulta e a alteração não tem conferência
equivalente. Apagar a linha quando a alteração a deixa sem nada pode ser
proposital — linha sem consulta não serve para nada — ou efeito colateral da falta
daquela exigência. Pergunta ao site.

### RN-15 — A consulta não grava nada

A consulta confere tipo, código, cadastro, acesso e nível e termina **sem gravar**:
nenhuma liberação e nenhum registro de auditoria. É a consulta que prepara a
alteração, e só ela.

### RN-16 — Sem nível de acesso para mostrar, a tela avisa

Se a varredura do cadastro de níveis não encontra nenhum nível, a tela mostra
**\* Tela/Relatorio sem niveis cadastrados \*** na primeira linha e termina. O
aviso é da varredura dos níveis, não do cadastro de telas e relatórios.

[?] A primeira leitura da lista usa o nível zerado como chave, e o acervo não
documenta o que a leitura faz com uma chave zerada: se ela posiciona no começo do
conjunto, a lista aparece; se procura o nível zero, a tela cai neste aviso. Pelo
mesmo motivo, o aviso pode significar “não há nível de acesso cadastrado” ou “esta
tela ou relatório não tem nível”. O fonte não decide entre os dois. Pergunta ao
site.

### RN-17 — A requisição inteira é abandonada quando uma linha é recusada

As linhas são conferidas na mesma requisição que grava. A recusa de qualquer linha
faz a requisição terminar com o aviso correspondente e **sem gravar nada** —
inclusive o que estava correto nas outras linhas.

[?] Quando uma leitura ou uma gravação do banco falha, a tela pede o aviso a uma
rotina de mensagens que não está no acervo: o que o servidor vê nesse caso não se
conclui do fonte. Pergunta ao site.

### RN-18 — Toda liberação gravada fica registrada no histórico

As três operações — incluir, alterar e excluir a liberação — gravam um registro de
auditoria com a operação, o valor anterior e o posterior da liberação, a matrícula
do servidor, a secretaria, o tipo de órgão, a estação, a data, a hora e o número
do processo.

[?] O registro de auditoria leva sempre o mesmo código de manutenção, e é o código
da operação que distingue incluir, alterar e excluir. O que esse código de
manutenção distingue não está no acervo. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Liberação de telas e relatórios por nível de acesso

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S065T

  Cenário: RN-01 — Consulta de uma tela mostra as liberações de cada nível de acesso
    Dado que informo o tipo tela e o código de uma tela cadastrada, à qual tenho acesso
    Quando confirmo a consulta
    Então vejo o nome da tela, o módulo e, em cada linha, o nível de acesso
      e o que ele pode consultar, incluir, alterar e excluir

  Cenário: RN-01 — Consulta de um relatório mostra as liberações de cada nível de acesso
    Dado que informo o tipo relatório e o código de um relatório cadastrado, ao qual tenho acesso
    Quando confirmo a consulta
    Então vejo as liberações de cada nível de acesso para aquele relatório

  Cenário: RN-02 — Operação diferente de consulta e de alteração
    Dado que estou na tela S065T
    Quando escolho uma operação que não é consulta nem alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E nada é gravado

  Cenário: RN-02 — A tela abre em consulta
    Dado que cheguei à tela S065T pelo menu S004M
    Quando a tela é aberta
    Então ela está em consulta, sem nenhuma alteração pendente

  Cenário: RN-03 — Tipo não informado ou fora de T e R
    Quando informo o código e deixo o tipo em branco, ou informo um tipo diferente de T e R
    Então vejo a mensagem "* Informe T para tela ou R para relatorio *"

  Cenário: RN-03 — Código em branco
    Quando informo o tipo e deixo o código em branco
    Então vejo a mensagem "* Informe o codigo da tela ou relatorio *"

  Cenário: RN-04 — Tela ou relatório não cadastrado
    Quando consulto um par tipo e código que não está no cadastro de telas e relatórios
    Então vejo a mensagem "* Tela / relatorio nao cadastrado *"
    E nada é gravado

  Cenário: RN-05 — Tela à qual não tenho acesso
    Dado que o meu nível de acesso não tem liberação para a tela informada
    Quando confirmo a consulta
    Então vejo a mensagem "* Usuario sem acesso a esta tela/relatorio *"
    E nada é gravado

  Cenário: RN-06 — Alteração sem consulta prévia
    Dado que não consultei esta tela nesta sessão
    Quando marco uma linha com a ação A e confirmo
    Então vejo a mensagem "* Consulte antes de alterar *"
    E nada é gravado

  Cenário: RN-07 — Nível acima do meu
    Dado que consultei a tela e marco uma linha cujo nível de acesso é maior que o meu
    Quando confirmo
    Então vejo a mensagem "* Seu nivel de acesso nao permite esta operacao *"
    E nada é gravado

  Cenário: RN-07 — Meu próprio nível sem privilégio
    Dado que consultei a tela e marco uma linha cujo nível de acesso é o meu
    E não tenho a marca de privilégio
    Quando confirmo
    Então vejo a mensagem "* Seu nivel de acesso nao permite esta operacao *"
    E nada é gravado

  Cenário: RN-07 — Meu próprio nível com privilégio
    Dado que consultei a tela e marco uma linha cujo nível de acesso é o meu
    E tenho a marca de privilégio
    Quando confirmo a alteração
    Então a liberação daquela linha é gravada

  Cenário: RN-08 — Operação não liberada para mim nesta tela
    Dado que o meu nível de acesso não tem a inclusão liberada nesta tela de liberações
    Quando marco uma linha com a ação I e confirmo
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-09 — Linha sem nível ou com ação desconhecida é ignorada
    Dado que deixo uma linha sem o nível de acesso, ou marco nela uma ação diferente de I, A e E
    Quando confirmo
    Então aquela linha é ignorada, sem aviso e sem gravação

  Cenário: RN-10 — Inclusão da liberação de um nível que ainda não a tem
    Dado que consultei uma tela cadastrada e escolhi um nível de acesso abaixo do meu
    Quando marco a linha com a ação I e confirmo
    Então a liberação daquele nível para aquela tela passa a existir
    E a inclusão fica registrada no histórico

  Cenário: RN-10 — Incluir código que já existe naquele nível
    Dado que a liberação daquele nível para aquela tela já existe
    Quando marco a linha com a ação I e confirmo
    Então vejo a mensagem "* Codigo ja cadastrado neste nivel de acesso *"
    E nada é gravado

  Cenário: RN-10 — Incluir sem nenhuma autorização
    Dado que marco a linha com a ação I e não deixo nenhuma liberação marcada
    Quando confirmo
    Então vejo a mensagem "* Informe autorizacoes para o codigo *"
    E nada é gravado

  Cenário: RN-11 — Alteração das liberações de um nível
    Dado que consultei a tela e a liberação daquele nível já existe
    Quando marco a linha com a ação A, mudo as liberações e confirmo
    Então o que ficou marcado passa a valer para aquele nível
    E os valores anterior e posterior ficam no histórico

  Cenário: RN-11 — Alterar ou excluir código que não existe naquele nível
    Dado que a liberação daquele nível para aquela tela não existe
    Quando marco a linha com a ação A, ou com a ação E, e confirmo
    Então vejo a mensagem "* Codigo nao cadastrado neste nivel de acesso *"
    E nada é gravado

  Cenário: RN-11 — Exclusão da liberação de um nível
    Dado que consultei a tela e a liberação daquele nível existe
    Quando marco a linha com a ação E e confirmo
    Então a liberação daquele nível para aquela tela deixa de existir
    E a exclusão fica registrada no histórico

  Cenário: RN-12 — Tela sem opção de atualização
    Dado que a tela está cadastrada como sem opção de atualização
    Quando marco na linha uma liberação de inclusão, de alteração ou de exclusão
    Então vejo a mensagem "* Tela sem opcao de atualizacao *"
    E nada é gravado

  Cenário: RN-12 — Relatório só aceita consulta
    Dado que consultei um relatório cadastrado
    Quando marco a linha com a ação A e libero inclusão, alteração e exclusão
    Então só a liberação de consulta fica gravada para aquele nível

  Cenário: RN-13 — Liberar uma atualização libera a consulta
    Dado que consultei uma tela cadastrada
    Quando marco na linha a liberação de inclusão, ou a de alteração, ou a de exclusão
    Então a liberação de consulta daquela linha fica marcada junto

  Cenário: RN-14 — Alterar uma linha deixando-a sem nenhuma liberação
    Dado que consultei a tela e a liberação daquele nível existe
    Quando marco a linha com a ação A e deixo as quatro liberações em branco
    Então a liberação daquele nível para aquela tela é apagada

  Cenário: RN-15 — A consulta não grava nada
    Dado que informo um tipo e um código válidos e tenho acesso à tela
    Quando confirmo a consulta
    Então vejo as liberações daquele nível
    E nenhuma liberação e nenhum registro de auditoria são gravados

  Cenário: RN-16 — Sem níveis de acesso cadastrados
    Dado que o cadastro de níveis não tem nenhum nível
    Quando consulto uma tela cadastrada à qual tenho acesso
    Então vejo a mensagem "* Tela/Relatorio sem niveis cadastrados *"
    E nada é gravado

  Cenário: RN-17 — Uma linha recusada impede a gravação da requisição
    Dado que marco duas linhas, uma correta e outra que será recusada
    Quando confirmo
    Então vejo o aviso da linha recusada
    E nenhuma das duas é gravada

  Cenário: RN-18 — Toda liberação gravada fica no histórico
    Dado que incluo, altero ou excluo a liberação de um nível
    Quando a gravação se completa
    Então fica um registro de auditoria com a operação, os valores anterior e
      posterior, o servidor, a secretaria, o tipo de órgão, a estação e a data e hora
```
