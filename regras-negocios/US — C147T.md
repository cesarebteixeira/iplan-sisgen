# US — C147T — Classificar as contas do órgão por fonte de recursos e creche

## Estória

Como **servidor de CRE que mantém os cadastros da secretaria**, quero **classificar as contas
do órgão pela fonte de recursos a que cada uma pertence e marcar quais delas são de creche**,
para que **a despesa saia na fonte certa e as contas de creche sejam reconhecidas nos
lançamentos**.

A conta do órgão precisa estar neste cadastro para ser aceita nos lançamentos: outras telas
procuram a conta aqui e recusam com **\* Conta nao cadastrada \*** quando ela não está. É esta
classificação que liga a conta à fonte de recursos; sem ela, o gasto da secretaria fica sem
origem e não há como acompanhar o dinheiro por fonte. A tela serve às duas coisas — mantém a
classificação (inclui, altera e exclui) e mostra o que já está classificado —, e é na mostra
que nada é gravado.

## Contexto

Jornada S000M → C000M → C020M → C147T.

Ator: servidor de CRE — mantém, para as contas do órgão da sua sessão, a fonte de recursos e a
marca de creche, incluindo, alterando e excluindo a classificação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A C147T é o último passo da jornada: ela não encaminha para outra tela. No passo anterior,
quando a sessão traz o módulo do cadastro de contas, a opção do menu que abriria esta tela
aparece bloqueada com **\* Acesso deve ser feito pela tela C147T \*** e a sessão é encaminhada
para cá; a tela abre, então, como transação própria, sem receber registro nem operação de quem
a chamou.

A tela **grava**: é ela que inclui, altera e exclui a classificação da conta (a fonte e a
marca de creche) e registra a auditoria de cada operação. Ela **não** cria, não altera e não
exclui o cadastro das fontes de recursos nem o cadastro de telas — os dois são apenas lidos —,
e não é por ela que se cadastra o servidor nem se libera o acesso.

As regras abaixo são só as da tela desta jornada; as da entrada não se repetem aqui.

## Regras de negócio

### RN-01 — O que a tela mantém e como a página se apresenta

A tela mantém, para cada conta do órgão da sessão, a **fonte de recursos** a que ela pertence e
a **marca de creche**. A conta é a identidade do registro: no mesmo órgão a conta aparece uma
vez só, e é isso que garante que ela pertença a uma única fonte.

A classificação se apresenta em uma página de até **15 linhas**, com quatro colunas — a
**conta**, a **fonte**, a **marca de creche** e a **ação** —, e o cabeçalho traz a identificação
da tela, a opção de manutenção e o prefixo de tela. Ao lado da página, a tela mostra a
identificação do órgão da sessão e a data do sistema. A coluna da fonte mostra o **código**
gravado na conta — é a coluna que a ficha da tela chama de **CODIGO DA FONTE** —, e não a
descrição do cadastro de fontes. O cadastro comporta **1.000 registros** no total —
**capacidade** declarada (o máximo esperado, parâmetro de dimensionamento), não volume
cadastrado.

A lista é montada percorrendo as contas do órgão na ordem da conta e para no primeiro registro
de outro órgão: nada de outro órgão aparece, e nada é escolhido pelo servidor — é o órgão da
sessão que decide o que a tela vê e onde ela grava.

[?] A identificação do órgão e a data do sistema que a tela mostra vêm da área da sessão, e os
programas lidos só as inicializam em branco: quem as preenche não está no material lido.
Pergunta ao site.

[?] O rótulo que a tela exibe sobre a coluna da conta não está no material desta jornada — a
máscara da tela não faz parte do acervo. A coluna é descrita aqui pela posição e pelo
significado. Pergunta ao site.

### RN-02 — A página só admite alteração e consulta

A opção de manutenção da página aceita **dois valores**: alteração e consulta — os mesmos que a
mensagem de recusa nomeia como **ALT** e **CON**. Qualquer outro valor é recusado com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no campo da opção, e nada é
conferido nem gravado. A conferência da opção é feita uma vez por página, na primeira linha.

Quando a página é montada e a sessão não traz opção nenhuma, a própria tela a preenche com
**consulta** — é assim que a tela abre para ver o que já está classificado.

[?] A mensagem manda usar ALT e CON, mas a tela confere os códigos de alteração e de consulta
do sistema, de três caracteres, e não os mnemônicos que ela própria escreve. Ou a máscara
traduz o mnemônico antes de enviar, ou a mensagem está desalinhada da guarda. A máscara não
está no material lido. Pergunta ao site.

[?] Se a opção chega em branco, a conferência da entrada recusa com a mesma mensagem, ainda que
a página tenha sido montada com consulta: só se a máscara devolver o valor que exibiu é que a
consulta sem opção informada passa. Pergunta ao site.

### RN-03 — As ações da linha incluem, alteram e excluem

Cada linha da página tem uma ação de uma posição: **I** inclui a conta no cadastro, **A**
altera a classificação da conta e **E** exclui a conta do cadastro. As ações só têm efeito no
modo de alteração: no modo de consulta a página inteira é abandonada antes de qualquer ação.

Linha com a **conta zerada**, ou com ação **diferente dessas três** (inclusive em branco),
passa em claro: não é conferida, não grava nada e não gera aviso ao servidor.

[?] Recusada uma linha, a conferência das linhas seguintes é interrompida, mas o caminho de
gravação não reconfere esse indicador — ele só volta a olhar a opção da página e a ação da
linha. Ou a página inteira para na primeira recusa, ou as linhas seguintes gravam sem ter sido
conferidas. Pergunta ao site.

### RN-04 — Na inclusão, a conta não pode já estar classificada com aquela fonte

Para incluir, a conta informada é procurada no cadastro do órgão da sessão. Se já houver
classificação **com aquela mesma fonte**, a inclusão é recusada com
**\* Conta ja cadastrada \***, com o cursor na coluna da conta, e nada é gravado.

[?] A recusa só olha o par conta + fonte, mas o cadastro não aceita a mesma conta duas vezes no
mesmo órgão: incluir uma conta que já existe apontando **outra** fonte passa pela recusa e é
barrada pelo próprio cadastro, sem mensagem desta tela. Ou a recusa deveria olhar só a conta,
ou o cadastro deveria aceitar mais de uma fonte por conta. Pergunta ao site.

### RN-05 — Na alteração e na exclusão, a conta tem de estar classificada

Para alterar ou excluir, a conta informada tem de estar classificada — e a conferência só a
reconhece quando a **fonte informada é a mesma** que está registrada na conta. Não sendo, a
operação é recusada com **\* Conta nao cadastrada \***, com o cursor na coluna da conta, e nada
é gravado.

[?] A alteração grava a fonte informada na conta lida, mas a conferência que a deixa passar
exige que a fonte informada já seja a registrada: trocar a fonte de uma conta é recusado como
se a conta não estivesse cadastrada, e o ramo que grava a fonte nova fica inalcançável por este
caminho. A tela C146T, que mantém esse mesmo cadastro um registro por vez, aceita a troca.
Pergunta ao site.

### RN-06 — A fonte informada é obrigatória e tem de existir no cadastro de fontes

Nas duas operações que classificam — incluir e alterar —, a fonte é conferida duas vezes. Em
branco, a operação é recusada com **\* Informe a fonte \***, com o cursor na coluna da fonte.
Informada, ela tem de existir no cadastro de fontes do órgão da sessão: não existindo, a recusa
é **\* Fonte nao cadastrada \***, no mesmo cursor.

A **exclusão** não confere a fonte: ela só precisa da conta.

### RN-07 — A marca de creche só aceita S ou N

Nas duas operações que classificam — incluir e alterar —, a marca de creche só aceita **S** ou
**N**. Qualquer outro valor, inclusive em branco, é recusado com
**\* Informe S ou N para creche \***, com o cursor na coluna da creche. A **exclusão** não
confere a marca.

### RN-08 — A inclusão cria a conta no cadastro do órgão da sessão

A ação **I** cria o registro da conta no cadastro do órgão, com a **conta** e a **fonte**
informadas e a **marca de creche**. O órgão não é digitado na tela: é o da sessão, e é ele que
decide a que órgão a conta nova passa a pertencer.

### RN-09 — A alteração regrava a classificação da conta lida

A ação **A** relê a conta classificada, guarda o valor anterior, **trava o registro**, substitui
a fonte e a marca de creche pelas informadas na linha e grava. A **conta** é a identidade do
registro: a alteração não a troca.

### RN-10 — A exclusão apaga a conta do cadastro

A ação **E** apaga do cadastro a conta do órgão. A fonte e a marca de creche que ela tinha vão
embora com ela, e é esse conteúdo que fica guardado na auditoria.

### RN-11 — Toda gravação deixa rastro na auditoria

Cada inclusão, cada alteração e cada exclusão grava também um registro na trilha de auditoria:
o cadastro de origem, a operação, o **valor anterior** e o **posterior** e o contexto da sessão
— matrícula, secretaria, CRE, terminal, data e hora e o número do processo, além do órgão. Na
alteração, o valor anterior é o registro como estava e o posterior é o registro já com a fonte
e a creche novas; na inclusão, o valor anterior vai em branco; na exclusão, o posterior vai em
branco.

[?] O rastro da inclusão é escrito depois de a conta ser criada, e o estado que a criação
devolve não chega a barrá-lo: a tela só desvia quando a operação é abortada. O que esse estado
significa não está no material lido — se a criação não se completar sem abortar, a auditoria
registra uma inclusão que não houve. Pergunta ao site.

### RN-12 — No modo de consulta nada é gravado

Com a opção de manutenção em **consulta**, o processamento das linhas é abandonado antes de
qualquer conferência de ação e antes de qualquer gravação — tanto na passagem de conferência
quanto na de gravação. A consulta é somente leitura: percorrer a página não inclui, não altera,
não exclui e não deixa rastro de auditoria.

### RN-13 — Órgão sem conta classificada é avisado

Quando a página é montada e o órgão da sessão não tem nenhuma conta classificada, a tela não
mostra linha alguma e avisa **\* Nao existem contas cadastradas \***, com o cursor na coluna da
conta. É o mesmo caminho de uma tela que abre sem nada a listar.

### RN-14 — Nada é exibido nem gravado sem as conferências de tela, de rota e de permissão

Ao apresentar a página, a tela confere se o cadastro do servidor é encontrado pela matrícula,
se o **terminal** da sessão é o do cadastro — não sendo, a sessão é encerrada —, se a **tela**
está no cadastro de telas e se ela está liberada para o **acesso** do servidor. Faltando a tela
no cadastro, a recusa é **\* Tela nao disponivel \***; faltando a liberação para o acesso, a
recusa é **\* Acesso negado para esta matricula \***, e a sessão volta ao menu principal (ou à
entrada, quando não há matrícula).

Ao conferir a entrada, a tela publica o contexto da sessão (tela, prefixo de tela, matrícula,
privilégio, órgão e CRE) e passa pela **lógica de rota** e pela **segurança de perfil**. Depois,
linha a linha, passa pela **permissão da operação** pretendida: incluir, alterar e excluir são
liberados um a um pelo cadastro de acesso × tela, e a operação não liberada é recusada com
**\* Acesso negado para esta operacao \***. **Consultar** passa sem essa conferência de
operação.

Se qualquer uma dessas conferências não aprovar, a tela sai sem conferir as linhas e sem
gravar, e nada é auditado.

### RN-15 — Prefixo de tela preenchido abandona a manutenção

Se a transação chega com o **prefixo de tela** preenchido, a manutenção é abandonada antes de
qualquer conferência de opção ou de ação, e a sessão é encaminhada para a tela indicada no
prefixo. O campo é exibido na página.

[?] Não se sabe quem preenche o prefixo de tela nesta tela: o passo anterior da jornada abre a
C147T sem passar registro nem operação, e nenhum programa da jornada atribui valor a esse campo.
Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Classificar as contas do órgão por fonte de recursos e creche

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o órgão da secretaria
    E tenho acesso à tela C147T

  Cenário: A página lista as contas do meu órgão
    Dado que estou na tela C147T
    Quando a página é apresentada
    Então vejo até 15 linhas, cada uma com a conta, a fonte, a marca de creche e a ação
    E vejo a identificação do meu órgão e a data do sistema
    E a fonte mostrada é o código gravado na conta, não a descrição do cadastro de fontes
    E o cadastro comporta até 1.000 contas classificadas

  Cenário: Órgão sem conta classificada é avisado
    Dado que estou na tela C147T e o meu órgão não tem conta classificada
    Quando a página é apresentada
    Então não vejo linha alguma
    E vejo "* Nao existem contas cadastradas *"
    E o cursor fica na coluna da conta

  Cenário: A tela abre em consulta e a consulta não grava nada
    Dado que estou na tela C147T sem informar a opção de manutenção
    Quando percorro e confirmo as linhas da página
    Então a tela assume a consulta
    E nenhuma conta é incluída, alterada ou excluída
    E nenhum registro de auditoria é criado

  Cenário: Opção de manutenção diferente de ALT e de CON é recusada
    Dado que estou na tela C147T
    Quando informo uma opção de manutenção diferente de ALT e de CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo da opção
    E nada é conferido nem gravado

  Cenário: Linha sem conta ou com ação desconhecida é ignorada
    Dado que estou na tela C147T no modo ALT
    Quando deixo a conta em branco, ou informo uma ação que não é I, A nem E
    Então a linha não é conferida, não grava nada e não gera aviso

  Cenário: Inclusão de uma conta
    Dado que estou na tela C147T no modo ALT
    E que a conta ainda não está classificada com aquela fonte
    E que a fonte existe no cadastro de fontes do meu órgão
    Quando informo a conta, a fonte, a marca de creche e a ação I
    Então a conta passa a estar classificada no cadastro do meu órgão
    E a inclusão fica registrada na auditoria

  Cenário: Inclusão recusa conta já classificada com aquela fonte
    Dado que estou na tela C147T no modo ALT
    E que a conta já está classificada com aquela fonte
    Quando informo a ação I
    Então vejo "* Conta ja cadastrada *"
    E o cursor fica na coluna da conta
    E nada é gravado

  Cenário: Alteração regrava a classificação e guarda o valor anterior
    Dado que estou na tela C147T no modo ALT
    E que a conta está classificada
    Quando informo a ação A com a fonte registrada e uma nova marca de creche
    Então a classificação da conta é regravada
    E a classificação anterior fica registrada na auditoria

  Cenário: Alteração e exclusão recusam conta não cadastrada
    Dado que estou na tela C147T no modo ALT
    Quando informo a ação A ou a ação E para uma conta que não está classificada com aquela fonte
    Então vejo "* Conta nao cadastrada *"
    E o cursor fica na coluna da conta
    E nada é gravado

  Cenário: Exclusão apaga a conta do cadastro
    Dado que estou na tela C147T no modo ALT
    E que a conta está classificada
    Quando informo a ação E com a conta e a fonte registradas
    Então a conta deixa o cadastro do meu órgão
    E a exclusão fica registrada na auditoria com o valor anterior

  Cenário: A fonte informada é obrigatória
    Dado que estou na tela C147T no modo ALT
    Quando tento incluir ou alterar uma conta sem informar a fonte
    Então vejo "* Informe a fonte *"
    E o cursor fica na coluna da fonte
    E nada é gravado

  Cenário: A fonte informada tem de existir no cadastro de fontes
    Dado que estou na tela C147T no modo ALT
    Quando informo uma fonte que não está cadastrada no meu órgão
    Então vejo "* Fonte nao cadastrada *"
    E o cursor fica na coluna da fonte
    E nada é gravado

  Cenário: A marca de creche só aceita S ou N
    Dado que estou na tela C147T no modo ALT
    Quando tento incluir ou alterar uma conta com a marca de creche diferente de S e de N
    Então vejo "* Informe S ou N para creche *"
    E o cursor fica na coluna da creche
    E nada é gravado

  Cenário: Toda gravação deixa rastro na auditoria
    Dado que confirmei uma inclusão, uma alteração ou uma exclusão na C147T
    Quando a gravação termina
    Então existe um registro de auditoria do cadastro de contas
    E com a operação, o valor anterior e o valor posterior
    E com a matrícula, a secretaria, a CRE, o terminal e a data e hora

  Cenário: A tela não abre sem estar liberada para o meu acesso
    Dado que a tela C147T não está liberada para o meu código de acesso
    Quando tento abrir a tela
    Então a lista não é exibida
    E vejo "* Tela nao disponivel *" ou "* Acesso negado para esta matricula *"
    E a sessão volta ao menu principal
    E nada é gravado

  Cenário: Sem permissão para a operação
    Dado que o meu código de acesso não libera a inclusão na tela C147T
    Quando confirmo a inclusão de uma conta
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado
    E nenhum registro de auditoria é criado

  Cenário: A consulta não exige permissão de operação
    Dado que estou na tela C147T no modo de consulta
    Quando a minha permissão não libera incluir, alterar nem excluir nesta tela
    Então a página é apresentada normalmente
    E nada é gravado

  Cenário: Prefixo de tela preenchido abandona a manutenção
    Dado que a transação chega à C147T com o prefixo de tela preenchido
    Quando a conferência das linhas começaria
    Então as linhas não são conferidas
    E a sessão é encaminhada para a tela indicada no prefixo
    E nada é gravado
```
