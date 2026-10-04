# US — C141T — Manter os tipos de contrato da secretaria

## Estória

Como **servidor de CRE**, quero **manter os tipos de contrato da minha secretaria — com o
tipo de licitação que autoriza cada um, a prioridade, a tabela quinzena, a unidade
orçamentária, o número com sinal e o tipo de permissão —, em consulta, alteração e
exclusão**, para que **o contrato, o período e o pedido de cada tipo sejam classificados,
autorizados e calculados com o que aquele tipo realmente é**.

O tipo de contrato é a classificação que amarra o contrato à licitação que o autoriza, à
tabela de preços da quinzena, à unidade orçamentária e à permissão concedida. Quem registra
contrato, período ou pedido depende desta lista para saber o que cada tipo permite; sem ela
cadastrada, não há como classificar nada. E, como o tipo de licitação e a prioridade se
espalham pelas permissões já concedidas, corrigir um tipo sem acertar o que dele depende
deixaria a autorização do contrato desalinhada do que ele é.

## Contexto

Jornada S000M → C000M → C020M → C141T.
Ator: servidor de CRE — mantém os tipos de contrato da secretaria em que atua: consulta a
lista, altera os dados do tipo e exclui o tipo que não tem permissão presa a ele.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. O `C000M` e o `C020M` são menus: só encaminham e não
gravam nada. A tela anterior não deixa no contexto nada que a `C141T` leia: a lista de
opções do menu não é passada adiante, e o estado da `C141T` (a última opção de manutenção
usada e a posição da lista) é guardado pela própria tela, no seu espaço de trabalho.

O que a tela usa do contexto é a sessão carregada na entrada; a procedência dela está no
anexo de evidências, em **A jornada e o que ela usa do contexto**.

---

## Regras de negócio

### RN-01 — O cadastro é o dos tipos de contrato, com oito dados de classificação

Cada tipo de contrato tem um **código de 3 dígitos**, uma **descrição de até 30 caracteres**,
um **tipo de licitação** (código de 2 dígitos, com a descrição vinda de cadastro próprio),
uma **prioridade de 2 dígitos**, uma **tabela quinzena** (N = Normal ou E = Especial), um
**número com sinal e duas casas decimais**, a **unidade orçamentária** (8 dígitos) e o **tipo
de permissão** (N, C ou O, exibidos na tela como Nor, Coo ou Ope). Só esses oito dados vêm da
tela: o cadastro do tipo de contrato carrega ainda outros dois que ela não pede e que trata
nas regras da alteração e da inclusão.

Os campos numéricos passam pela edição do sistema: o que não for número é recusado e o
cursor volta ao campo. A tela mostra os dados do sistema no cabeçalho — a data do dia e a
descrição do tipo de órgão da sessão.

[?] O acervo não diz, em negócio, o que é o número com sinal e duas casas decimais que o tipo
de contrato carrega, nem o que ele altera depois: a tela só o confere como número, o exibe e
o grava. Pergunta ao site.

[?] O que significam, em negócio, os três tipos de permissão (N, C e O, exibidos como Nor,
Coo e Ope) e a prioridade de dois dígitos? O corpus dá as letras e as faixas de valor, não o
significado. Pergunta ao site.

### RN-02 — Todo tipo de contrato é da secretaria do servidor, e ele não escolhe outra

O que a tela lista, altera ou exclui pertence sempre ao tipo de órgão que veio da sessão do
servidor. Um tipo de contrato de outro tipo de órgão é tratado como inexistente: não aparece
na lista, não pode ser alterado nem excluído, e o código gravado é sempre o da sessão — nunca
outro. As permissões, as permissões auxiliares e os períodos procurados por esta tela também
são os daquele tipo de órgão.

### RN-03 — A tela abre em consulta e só aceita alteração (ALT) ou consulta (CON)

A opção de manutenção aceita apenas **alteração** e **consulta**; inclusão e exclusão não se
escolhem por ali — elas são ações de linha (RN-05, RN-06 e RN-07). A tela abre em consulta e,
nas passagens seguintes, reaproveita a última opção aceita. Qualquer outra opção é recusada
com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta ao campo da opção,
e a transação para sem conferir nem gravar nenhuma linha.

[?] A guarda interna compara a opção com os códigos de alteração e de consulta, mas a
mensagem manda usar "ALT" e "CON". Ou o terminal traduz o mnemônico antes de enviar, ou a
mensagem está desalinhada da guarda. Pergunta ao site; não concluo qual dos dois.

### RN-04 — Em consulta a tela não grava nada

Na consulta a tela apenas lista: a passagem de conferência é desviada antes de olhar qualquer
linha e a passagem de gravação também. Nenhuma gravação é feita — nem a auditoria é montada.

### RN-05 — A inclusão não se completa: a conferência recusa o mesmo código que a gravação exige

A inclusão se faz digitando o código novo na linha, com a ação de inclusão. Ela **não se
completa por esse caminho**, e as duas guardas se contradizem:

- a conferência procura o código no cadastro da secretaria e, **não achando**, recusa com
  **\* Tipo de contrato nao cadastrado \*** — a mesma mensagem da alteração e da exclusão —
  antes de olhar a descrição ou qualquer outro campo;
- a passagem que gravaria o tipo de contrato é protegida pela condição **contrária**: só
  grava o tipo que **já existe** no cadastro.

Ou seja: com o código já cadastrado, a inclusão recusaria com
**\* Tipo de contrato ja cadastrado \***; com o código livre, recusa com
**\* Tipo de contrato nao cadastrado \***. Os dois desfechos são recusa, e não escolho um dos
dois lados.

[?] A guarda da inclusão recusa o tipo de contrato que ainda não existe e o ramo que grava
exige que ele exista; o mesmo acontece com o aviso de lista vazia (RN-08). Ou essas guardas
deveriam olhar o contrário, ou a inclusão ficou inalcançável por este caminho. Pergunta ao
site — enquanto isso não se decide, não afirmo que incluir funciona.

### RN-06 — A alteração exige o tipo de contrato, a descrição e os oito dados de classificação

A alteração procura o código no cadastro da secretaria e, se não existe, recusa com
**\* Tipo de contrato nao cadastrado \***. Existindo, exige a **descrição** — sem ela, recusa
com **\* Informe a descricao \*** — e confere, com mensagem própria e o cursor no campo:

| o que a tela exige | mensagem |
| --- | --- |
| tipo de licitação informado | **\* Informe o tipo de licitacao \*** |
| tipo de licitação existente no cadastro próprio | **\* Tipo de licitacao nao cadastrado \*** |
| tabela quinzena marcada com N ou E | **\* Inf. tab.quinzena com N=Normal ou E=Especial \*** |
| unidade orçamentária existente, quando informada | **\* Unidade orcamentaria nao cadastrada \*** |
| tipo de permissão entre N, C e O | **\* Inf.tipo permiss com N, C ou O \*** |

A unidade orçamentária em branco é aceita (a conferência de cadastro só acontece quando ela é
informada).

### RN-07 — A alteração não deixa trocar o tipo de permissão, e mudar o tipo de licitação com permissão concedida é recusado

A alteração recusa a troca do **tipo de permissão**, comparando o valor da tela com o do
registro: **\* Nao altere tipo permiss \*** — o tipo de permissão do contrato é o que é, e
quem o muda é outra tela. E se o **tipo de licitação** informado é diferente do que o tipo de
contrato tem, a tela procura uma permissão daquele tipo de contrato; achando, recusa com
**\* Nao altere. Ja existe permissao \***. Sem permissão, a mudança é aceita.

[?] A procura da permissão decide com o ano-limite de **outro** registro, que aquela leitura
não carrega — e a tela irmã, que faz a mesma conferência, não tem essa condição. É a única
comparação desse tipo em todo o acervo. Ou a condição deveria olhar o registro lido, ou ela é
resto de geração: enquanto isso não se decide, não afirmo que a recusa acontece. Pergunta ao
site.

### RN-08 — Quando não há tipo de contrato cadastrado, a tela avisa

Se a primeira linha da página não encontra nenhum tipo de contrato, a tela mostra
**\* Nao existem tipos de contrato cadastrados \*** e o cursor volta ao código; a mesma coisa
acontece quando a página pedida passa do fim da lista. A conferência que produz o aviso é a
mesma guarda contraditória da inclusão (RN-05): ela testa a existência pelo lado oposto ao do
ramo que grava, e é no ramo de lista vazia que a tela avisa.

[?] Quem pede a página seguinte depois do fim da lista não recebe a página recomeçada do
começo: recebe o mesmo aviso de lista vazia (RN-08). O aviso e a posição da lista vivem na
mesma guarda. Pergunta ao site.

### RN-09 — A exclusão é recusada quando há permissão ou permissão auxiliar do tipo de contrato

A exclusão procura o código no cadastro da secretaria: se não existe, recusa com
**\* Tipo de contrato nao cadastrado \***. Existindo, procura primeiro uma **permissão** do
tipo de contrato e, achando, recusa com **\* Nao exclua.Permissao neste tipo contrato \***;
depois procura uma **permissão auxiliar** e, achando, recusa com
**\* Nao exclua.Perm.aux neste tipo contrato \***. Só sem nenhuma das duas o tipo de contrato
é apagado — e a exclusão apaga **só** o tipo de contrato: não apaga permissão nem permissão
auxiliar.

[?] O acervo não define, em negócio, o que são as permissões auxiliares presas a um tipo de
contrato: a tela só as procura para não deixar excluir. Pergunta ao site.

### RN-10 — A lista traz 6 tipos de contrato por vez, cada linha com a sua ação, e continua de onde parou

A tela mostra **6 linhas por vez**, com o código, a descrição, o tipo de licitação, a
prioridade, a tabela quinzena, o número com sinal, a unidade orçamentária, o tipo de
permissão e a ação da linha. A lista sai na ordem do cadastro (tipo de órgão e código do tipo
de contrato) e a página seguinte continua a partir do último tipo mostrado. A posição da
lista é guardada no espaço de trabalho da própria tela, inicializado uma única vez.

A **ação é por linha**, não pela tela: **I** inclui, **A** altera e **E** exclui. A linha sem
código é ignorada, e a ação fora de I, A e E também — silenciosamente, sem mensagem.

### RN-11 — Cada operação de linha só é executada com a permissão correspondente do servidor

A abertura da tela passa pela conferência de segurança do sistema, e a primeira linha passa
ainda pela lógica de rota e pela permissão da tela. Antes de cada operação de linha, com a
operação já identificada pela ação da linha, a tela confere a permissão do servidor para
inclusão, alteração ou exclusão. Sem a permissão, a transação é encerrada sem gravar.

### RN-12 — A alteração acerta as permissões e as permissões auxiliares; toda gravação deixa rastro na auditoria

Quando a alteração muda o **tipo de licitação**, a tela acerta o novo tipo de licitação nas
permissões auxiliares e nos períodos daquele tipo de contrato. Quando muda a **prioridade**,
acerta a nova prioridade nas permissões concedidas daquele tipo de contrato. O que não mudou
não é tocado. Cada acerto é precedido do registro de auditoria e da trava do registro
alterado.

Toda operação de escrita monta um registro na trilha de auditoria com o tipo de órgão, a
matrícula, a secretaria, a sessão, a tela de origem, a operação (inclusão, alteração ou
exclusão), a estação, a data e a hora, e os valores antes e depois: na alteração os dois
lados são preenchidos; na exclusão o "depois" vai vazio. O acerto das permissões também deixa
o seu próprio rastro, com os cadastros de origem próprios.

[?] Na alteração, o "entra no cálculo de pedidos" é derivado do tipo de permissão do registro
— tipo de permissão N grava **Não**; C ou O gravam **Sim** —, e o indicador de contrato do
operador logístico é regravado sempre como **Não**, sem que a tela os peça. Se um tipo de
contrato marcado como operador logístico for alterado por esta tela, a marcação se perde sem
aviso. Pergunta ao site.

[?] O número de processo que a auditoria guarda não é montado por esta tela nas operações
sobre o tipo de contrato: ele é apenas lido da área comum. Só o acerto da prioridade das
permissões o monta. Se ninguém preencher a área comum, o rastro das outras operações fica sem
esse identificador. Pergunta ao site.

### RN-13 — Falha de banco interrompe a operação e avisa

Todo acesso a dados testa o erro do banco; erro de leitura e erro de gravação são despachados
pela rotina de comunicação, que interrompe a transação com a mensagem do sistema e não deixa
a operação pela metade. A gravação não é considerada feita.

### RN-14 — A tela confere a página inteira antes de gravar, e o cadastro tem chave sem duplicatas

A exibição, a conferência e a gravação são passagens separadas de propósito: a exibição só lê
e mostra; a conferência só produz mensagens, linha a linha; e a gravação só acontece depois
de a página inteira ter passado pela conferência, também linha a linha. E o que a tela não
pegar, a chave sem duplicatas do cadastro barra — a gravação trata o registro duplicado como
falha.

## Cenários BDD

```gherkin
Funcionalidade: Manter os tipos de contrato da secretaria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C141T

  Cenário: RN-01, RN-02, RN-04, RN-10 — consultar os tipos de contrato da minha secretaria
    Dado que estou na tela C141T em consulta
    Quando confirmo
    Então vejo até 6 tipos de contrato da minha secretaria, em ordem de código, cada um com a descrição, o tipo de licitação, a prioridade, a tabela quinzena, o número com sinal, a unidade orçamentária e o tipo de permissão
    E nada é gravado

  Cenário: RN-02 — tipo de contrato de outra secretaria
    Dado que existe um tipo de contrato cadastrado para outro tipo de órgão
    Quando procuro esse código
    Então a tela o trata como inexistente

  Cenário: RN-10 — a lista continua na página seguinte
    Dado que a minha secretaria tem mais de 6 tipos de contrato
    Quando confirmo a tela sem alterar nada
    Então a lista seguinte continua a partir do último tipo mostrado

  Cenário: RN-08 — nenhum tipo de contrato cadastrado
    Dado que a minha secretaria não tem nenhum tipo de contrato cadastrado
    Quando confirmo a consulta
    Então vejo "* Nao existem tipos de contrato cadastrados *"

  Cenário: RN-03 — opção de manutenção não disponível
    Quando informo uma opção de manutenção diferente de ALT e CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E nada é gravado

  Cenário: RN-05 — incluir um tipo de contrato novo
    Dado que estou na tela C141T com a opção ALT
    Quando preencho uma linha com a ação I, um código que ainda não existe, a descrição, um tipo de licitação cadastrado, a prioridade, a tabela quinzena com N ou E, a unidade orçamentária e o tipo de permissão
    E confirmo
    Então vejo "* Tipo de contrato nao cadastrado *"
    E nada é gravado

  Cenário: RN-05 — incluir um código que já existe
    Dado que o código informado já está cadastrado
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Tipo de contrato ja cadastrado *"
    E nada é gravado

  Cenário: RN-06 — alterar sem a descrição
    Dado que o tipo de contrato está cadastrado
    Quando preencho a linha com a ação A e deixo a descrição em branco
    Então vejo "* Informe a descricao *"
    E nada é gravado

  Cenário: RN-06 — alterar sem o tipo de licitação
    Dado que o tipo de contrato está cadastrado
    Quando preencho a linha com a ação A e deixo o tipo de licitação zerado
    Então vejo "* Informe o tipo de licitacao *"
    E nada é gravado

  Cenário: RN-06 — tipo de licitação não cadastrado
    Dado que o tipo de contrato está cadastrado
    Quando preencho a linha com a ação A e um tipo de licitação que não existe
    Então vejo "* Tipo de licitacao nao cadastrado *"
    E nada é gravado

  Cenário: RN-06 — tabela quinzena fora de N e E
    Dado que o tipo de contrato está cadastrado
    Quando preencho a linha com a ação A e outra marcação de tabela quinzena
    Então vejo "* Inf. tab.quinzena com N=Normal ou E=Especial *"
    E nada é gravado

  Cenário: RN-06 — unidade orçamentária não cadastrada
    Dado que o tipo de contrato está cadastrado
    Quando preencho a linha com a ação A e uma unidade orçamentária que não existe
    Então vejo "* Unidade orcamentaria nao cadastrada *"
    E nada é gravado

  Cenário: RN-06 — tipo de permissão fora de N, C e O
    Dado que o tipo de contrato está cadastrado
    Quando preencho a linha com a ação A e outro tipo de permissão
    Então vejo "* Inf.tipo permiss com N, C ou O *"
    E nada é gravado

  Cenário: RN-06 e RN-10 — alterar um tipo de contrato existente
    Dado que o tipo de contrato está cadastrado
    Quando altero a descrição, a prioridade, a tabela quinzena, o número com sinal e a unidade orçamentária com a ação A
    E confirmo
    Então o tipo de contrato fica com os novos valores
    E o código e a secretaria do tipo de contrato não mudam
    E a alteração fica registrada na auditoria

  Cenário: RN-06 — alterar um tipo de contrato que não existe
    Quando preencho a linha com a ação A e um código não cadastrado
    Então vejo "* Tipo de contrato nao cadastrado *"
    E nada é gravado

  Cenário: RN-07 — trocar o tipo de permissão na alteração
    Dado que o tipo de contrato está cadastrado com um tipo de permissão
    Quando altero o tipo de permissão com a ação A
    Então vejo "* Nao altere tipo permiss *"
    E nada é gravado

  Cenário: RN-07 — mudar o tipo de licitação com permissão já concedida
    Dado que o tipo de contrato tem uma permissão concedida
    Quando altero o tipo de licitação com a ação A
    Então vejo "* Nao altere. Ja existe permissao *"
    E nada é gravado

  Cenário: RN-12 — alterar a prioridade acerta as permissões concedidas
    Dado que o tipo de contrato está cadastrado e tem permissões concedidas
    Quando altero a prioridade com a ação A e confirmo
    Então as permissões daquele tipo de contrato ficam com a nova prioridade
    E cada acerto fica registrado na auditoria

  Cenário: RN-09 e RN-10 — excluir um tipo de contrato sem permissão
    Dado que o tipo de contrato está cadastrado
    E não há permissão nem permissão auxiliar para ele
    Quando preencho a linha com a ação E e confirmo
    Então o tipo de contrato é apagado
    E a exclusão fica registrada na auditoria

  Cenário: RN-09 — excluir um tipo de contrato com permissão
    Dado que existe permissão para o tipo de contrato
    Quando preencho a linha com a ação E e confirmo
    Então vejo "* Nao exclua.Permissao neste tipo contrato *"
    E nada é apagado

  Cenário: RN-09 — excluir um tipo de contrato com permissão auxiliar
    Dado que existe permissão auxiliar para o tipo de contrato e não há permissão
    Quando preencho a linha com a ação E e confirmo
    Então vejo "* Nao exclua.Perm.aux neste tipo contrato *"
    E nada é apagado

  Cenário: RN-10 — linha sem código ou com ação desconhecida
    Dado que preencho uma linha sem o código do tipo de contrato, ou com uma ação diferente de I, A e E
    Quando confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada

  Cenário: RN-11 — servidor sem permissão para a operação
    Dado que não tenho permissão para a operação que a linha pede
    Quando confirmo
    Então a transação é encerrada
    E nada é gravado

  Cenário: RN-13 — falha de banco durante a gravação
    Dado que a gravação do tipo de contrato falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E a gravação não é considerada feita

  Cenário: RN-14 — a página inteira é conferida antes de gravar
    Dado que preenchi várias linhas da página com ações
    Quando confirmo
    Então a tela confere todas as linhas antes de gravar qualquer uma
    E a gravação só acontece se a conferência da página não acusar erro
```
