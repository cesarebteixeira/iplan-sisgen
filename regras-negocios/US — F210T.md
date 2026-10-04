# US — F210T — Manter os agricultores vinculados ao fornecedor

## Estória

Como **servidor de CRE**, quero **registrar, corrigir e retirar os agricultores
vinculados a um fornecedor, informando o CPF, o nome e a inscrição da DAP de cada
um**, para que **a secretaria saiba de quem são as notas fiscais emitidas contra os
fornecedores e o cadastro do agricultor esteja certo para quem opera a nota**.

A nota fiscal é lançada contra o fornecedor e alcança o agricultor pelo CPF dele. É
esta tela que diz quais agricultores pertencem a cada fornecedor, com o nome e a
inscrição da DAP de cada um; sem ela, esse vínculo ficaria fora do sistema, e a nota
do fornecedor não teria a quem ser atribuída.

A tela consulta e mantém o vínculo: inclui o agricultor novo, corrige o nome e a
inscrição da DAP do que já está vinculado e retira o que não pertence mais àquele
fornecedor, deixando um registro de auditoria para cada operação. A consulta sozinha
não altera nada, e a retirada de um agricultor que já tem nota fiscal registrada é
recusada.

## Contexto

Jornada S000M → F000M → F200M → F210T.

Ator: servidor de CRE — informa o código do fornecedor, consulta a relação dos
agricultores vinculados a ele e inclui, corrige ou retira uma linha dessa relação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os dois menus da jornada só encaminham: nem o `F000M` nem o `F200M` deixam dado de
negócio nenhum para a `F210T`. O contexto de que a tela se serve — matrícula, código
de acesso, privilégio, tipo de órgão, CRE e estação da sessão — é o que a entrada
deixou na sessão, e a tela apenas o repassa às conferências de acesso; essas
conferências são da entrada e estão no anexo de evidências, não aqui. A tela também
não encadeia para nenhuma outra: ela é o fim da jornada, e não entrega registro nem
operação a tela seguinte. As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — Cada mensagem começa com os campos de resultado limpos

Antes de conferir o que o operador digitou, a tela apaga a razão social do
fornecedor, a descrição do órgão e a data do sistema que a mensagem anterior havia
mostrado. Uma mensagem recusada, portanto, não deixa na tela o resultado da mensagem
anterior.

### RN-02 — A tela só aceita alteração e consulta

A tela aceita duas operações: a **consulta**, que só lê, e a **alteração**, que é a
única por onde se inclui, se corrige e se retira um agricultor. Se a operação chegar
diferente, o sistema recusa com **\* Opcao nao disponivel. Use ALT ou CON \***,
devolve o cursor ao campo da operação e abandona a mensagem: nada é lido nos
cadastros de negócio e nada é gravado.

Ao ser aberta, a tela repõe como consulta a operação guardada na sessão; se a última
operação usada na sessão foi a alteração, é ela que reaparece no campo.

### RN-03 — Os códigos digitados passam pela edição numérica

Os três códigos que o operador digita — o do fornecedor, o CPF da linha e o código de
continuação da listagem — passam pela edição numérica: o que estiver em branco vira
zero e o que não for número é recusado, com o cursor devolvido ao campo recusado.

[?] O que o operador vê quando a digitação é recusada não está nos fontes desta
jornada: a rotina que faz essa edição não faz parte do acervo lido. Pergunta ao site.

### RN-04 — O fornecedor é obrigatório e tem de estar cadastrado

O operador informa o código do fornecedor. Em branco — ou zerado — o sistema recusa
com **\* Informe o fornecedor \*** e devolve o cursor ao campo. Informado um código
que não está no cadastro de fornecedores, a recusa é
**\* Fornecedor nao cadastrado \***, no mesmo campo. Nas duas recusas nada é lido do
cadastro de agricultores e nada é gravado. Achado o fornecedor, a tela mostra a razão
social dele.

[?] A tela não confere a situação do fornecedor no cadastro: qualquer registro
encontrado pelo código serve, qualquer que seja a situação em que ele esteja. Se a
intenção era recusar o fornecedor fora de uso, essa conferência não existe neste
fonte. Pergunta ao site.

### RN-05 — A alteração exige ter consultado antes o mesmo fornecedor

Escolhida a alteração, o fornecedor informado tem de ser o mesmo que a tela processou
na mensagem anterior da sessão. Não sendo, o sistema recusa com
**\* Consulte antes de atualizar \***, devolve o cursor ao campo do fornecedor e não
grava nada — nem a inclusão, nem a correção, nem a retirada daquela mensagem. A
consulta é aceita para qualquer fornecedor, e é ela que deixa o fornecedor pronto
para a alteração seguinte.

[?] A área em que a tela guarda o fornecedor da última mensagem não tem, no acervo,
indicação de ser da sessão do servidor ou compartilhada entre terminais. Se for
compartilhada, a consulta de um operador pode liberar a alteração de outro. Pergunta
ao site.

### RN-06 — A consulta mostra os agricultores do fornecedor, de 11 em 11

Informado um fornecedor cadastrado e escolhida a consulta, a tela mostra a razão
social dele, a descrição do órgão da sessão, a data do sistema e a relação dos
agricultores: em cada linha, o CPF, o nome do agricultor e a inscrição da DAP. A
relação enche até 11 linhas por mensagem, e a tela guarda o código de continuação da
listagem para que a mensagem seguinte retome a relação de onde ela parou. Quando não
há nenhum agricultor vinculado ao fornecedor, a tela avisa
**\* Nao existem agricultores cadastrados \***.

[?] O campo de continuação da listagem aparece na tela e passa pela edição numérica,
mas o acervo não traz o rótulo dele nem diz se o operador pode digitá-lo; e não dá
para decidir, só pelo fonte, se a retomada relê a última linha mostrada ou começa na
seguinte. Se a listagem puder repetir ou pular um agricultor, é pergunta ao site.

### RN-07 — Cada linha da relação recebe a operação de incluir, alterar ou excluir

Na alteração, cada linha da relação recebe um código de operação: **I** para incluir,
**A** para alterar e **E** para excluir. Uma linha cujo CPF esteja em branco é
ignorada, e uma linha cujo código de operação não seja nenhum dos três também é
ignorada — nos dois casos sem aviso nenhum, e nenhuma delas é gravada.

[?] A tela não avisa quando a linha tem o nome do agricultor e a inscrição da DAP
preenchidos mas o CPF em branco: a linha simplesmente não é processada. Se a intenção
era chamar a atenção do operador para o que ele deixou de informar, o aviso não existe
neste fonte. Pergunta ao site.

[?] Depois de cada mensagem, o campo da operação de cada linha é reposto com um valor
que o acervo lido não define; se esse valor não for o branco, o código da operação
anterior pode reaparecer na linha. Pergunta ao site.

### RN-08 — Incluir recusa agricultor já vinculado e exige nome e inscrição da DAP

Para incluir, a linha é conferida nesta ordem: o agricultor não pode estar vinculado
àquele fornecedor — estando, a recusa é **\* Agricultor ja cadastrado \***, com o
cursor no campo da operação daquela linha —, o nome do agricultor é obrigatório
(**\* Informe o nome do agricultor \***) e a inscrição da DAP também
(**\* Informe a inscricao DAP \***), cada recusa devolvendo o cursor ao campo que
falta naquela linha.

### RN-09 — Alterar exige o agricultor vinculado e os mesmos dados obrigatórios

Para alterar, o agricultor tem de estar vinculado àquele fornecedor: não estando, a
recusa é **\* Agricultor nao cadastrado \***, com o cursor no campo da operação
daquela linha. Vinculado, o nome do agricultor e a inscrição da DAP continuam
obrigatórios, com as mesmas duas mensagens da inclusão.

### RN-10 — Excluir exige o agricultor vinculado e recusa quem já tem nota fiscal

Para excluir, o agricultor tem de estar vinculado àquele fornecedor: não estando, a
recusa é **\* Agricultor nao cadastrado \***. Vinculado, a tela procura as notas
fiscais registradas para o CPF naquele fornecedor e, havendo alguma, recusa com
**\<- Ja existem notas cadastradas com este CPF \***. A retirada é recusada por
qualquer nota registrada para aquele CPF naquele fornecedor, no tipo de órgão da
sessão: a tela não distingue as notas por nenhum outro dado.

### RN-11 — Uma linha recusada cancela a mensagem inteira

Todas as linhas da relação são conferidas antes de a primeira ser gravada. Se
qualquer linha for recusada, o sistema não grava nenhuma das outras linhas aprovadas
daquela mesma mensagem: o operador corrige e envia tudo de novo.

### RN-12 — A alteração grava o vínculo do agricultor com o fornecedor

Passando pelas conferências, a alteração grava: inclui o vínculo do agricultor novo,
corrige o nome e a inscrição da DAP do agricultor que já estava vinculado, ou retira
o vínculo do agricultor excluído. Fora o registro de auditoria da regra seguinte,
nenhum outro cadastro é gravado por esta tela.

[?] Depois de gravar, a tela não emite aviso nenhum de que a operação foi feita. Se o
operador deveria receber uma confirmação, ela não existe neste fonte. Pergunta ao
site.

### RN-13 — Cada operação gravada deixa um registro de auditoria

Para cada linha que a tela grava, ela grava também um registro de auditoria com o
cadastro auditado, a operação realizada, o conteúdo do registro antes e depois, a
matrícula, a estação, o tipo de órgão e a data e a hora da sessão.

[?] Na inclusão a auditoria é gravada depois do vínculo do agricultor; na correção e
na retirada, antes. Se a gravação do cadastro falhar depois de a auditoria ter sido
gravada, o acervo não diz se o registro de auditoria é desfeito. Pergunta ao site.

### RN-14 — A consulta não grava nada e não deixa auditoria

A consulta lê o cadastro de fornecedores e o cadastro de agricultores do fornecedor,
e para aí: nenhum vínculo é incluído, corrigido ou retirado, nenhum registro de
auditoria é gerado e as notas fiscais do agricultor não chegam a ser procuradas.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os agricultores vinculados ao fornecedor

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F210T

  Cenário: Consulta de um fornecedor com agricultores vinculados
    Dado que o código do fornecedor informado está no cadastro de fornecedores
    E esse fornecedor tem agricultores vinculados
    Quando escolho a operação CON e envio a mensagem
    Então vejo a razão social do fornecedor, a descrição do meu órgão e a data do sistema
    E vejo, em cada linha, o CPF, o nome do agricultor e a inscrição da DAP
    E vejo até 11 agricultores
    E a tela guarda o código de continuação da listagem

  Cenário: Fornecedor sem agricultores vinculados
    Dado que o código do fornecedor informado está no cadastro de fornecedores
    E esse fornecedor não tem agricultores vinculados
    Quando escolho a operação CON e envio a mensagem
    Então vejo a mensagem "* Nao existem agricultores cadastrados *"

  Cenário: A consulta não grava nada
    Dado que o código do fornecedor informado está no cadastro de fornecedores
    Quando escolho a operação CON e envio a mensagem
    Então nenhum agricultor é vinculado, corrigido ou retirado
    E nenhum registro de auditoria é gerado

  Cenário: Incluir um agricultor novo
    Dado que consultei o fornecedor informado
    E o CPF informado na linha ainda não está vinculado a esse fornecedor
    E preencho o nome do agricultor e a inscrição da DAP
    Quando escolho a operação ALT e envio a linha com o código de operação I
    Então o vínculo do agricultor com o fornecedor é gravado
    E fica um registro de auditoria da inclusão

  Cenário: Incluir um agricultor já vinculado
    Dado que consultei o fornecedor informado
    E o CPF informado na linha já está vinculado a esse fornecedor
    Quando escolho a operação ALT e envio a linha com o código de operação I
    Então vejo a mensagem "* Agricultor ja cadastrado *"
    E o cursor volta ao campo da operação daquela linha
    E nada é gravado

  Cenário: Incluir ou alterar sem o nome do agricultor
    Dado que consultei o fornecedor informado
    Quando escolho a operação ALT e envio uma linha com o código de operação I ou A
      e deixo o nome do agricultor em branco
    Então vejo a mensagem "* Informe o nome do agricultor *"
    E o cursor volta ao campo do nome naquela linha
    E nada é gravado

  Cenário: Incluir ou alterar sem a inscrição da DAP
    Dado que consultei o fornecedor informado
    Quando escolho a operação ALT e envio uma linha com o código de operação I ou A
      e deixo a inscrição da DAP em branco
    Então vejo a mensagem "* Informe a inscricao DAP *"
    E o cursor volta ao campo da inscrição naquela linha
    E nada é gravado

  Cenário: Alterar o nome e a inscrição da DAP de um agricultor vinculado
    Dado que consultei o fornecedor informado
    E o CPF informado na linha está vinculado a esse fornecedor
    Quando escolho a operação ALT e envio a linha com o código de operação A
      e os dados corrigidos
    Então o vínculo do agricultor fica com o nome e a inscrição da DAP informados
    E fica um registro de auditoria da correção, com o conteúdo anterior e o novo

  Cenário: Alterar um agricultor não vinculado
    Dado que consultei o fornecedor informado
    Quando escolho a operação ALT e envio a linha com o código de operação A
      e um CPF que não está vinculado a esse fornecedor
    Então vejo a mensagem "* Agricultor nao cadastrado *"
    E o cursor volta ao campo da operação daquela linha
    E nada é gravado

  Cenário: Excluir um agricultor vinculado e sem nota fiscal
    Dado que consultei o fornecedor informado
    E o CPF informado na linha está vinculado a esse fornecedor
    E não há nota fiscal registrada para esse CPF naquele fornecedor
    Quando escolho a operação ALT e envio a linha com o código de operação E
    Então o vínculo do agricultor com o fornecedor é retirado
    E fica um registro de auditoria da exclusão, com o conteúdo anterior

  Cenário: Excluir um agricultor com nota fiscal registrada
    Dado que consultei o fornecedor informado
    E o CPF informado na linha está vinculado a esse fornecedor
    E há nota fiscal registrada para esse CPF naquele fornecedor
    Quando escolho a operação ALT e envio a linha com o código de operação E
    Então vejo a mensagem "<- Ja existem notas cadastradas com este CPF *"
    E o vínculo do agricultor não é retirado

  Cenário: Linha sem CPF ou sem código de operação é ignorada
    Dado que consultei o fornecedor informado
    Quando escolho a operação ALT e envio uma linha sem o CPF, ou com um código
      de operação que não é I, A nem E
    Então nenhuma mensagem é mostrada
    E nenhum vínculo é gravado para aquela linha

  Cenário: Uma linha recusada cancela a mensagem inteira
    Dado que consultei o fornecedor informado
    E envio uma linha válida junto com outra linha recusada
    Quando escolho a operação ALT e envio a mensagem
    Então a linha recusada é mostrada com a sua mensagem
    E nenhuma das linhas daquela mensagem é gravada

  Cenário: Alteração sem ter consultado antes o mesmo fornecedor
    Dado que o fornecedor processado na mensagem anterior é outro
    Quando escolho a operação ALT e envio o código do fornecedor
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo do fornecedor
    E nada é gravado

  Cenário: Operação diferente de ALT e de CON
    Dado que estou na tela F210T
    Quando informo uma operação que não é ALT nem CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: Fornecedor em branco
    Dado que deixo o código do fornecedor em branco
    Quando envio a mensagem
    Então vejo a mensagem "* Informe o fornecedor *"
    E o cursor volta ao campo do fornecedor
    E nada é lido nem gravado

  Cenário: Fornecedor não cadastrado
    Dado que informo um código de fornecedor que não está no cadastro de fornecedores
    Quando envio a mensagem
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo do fornecedor
    E nada é lido nem gravado

  Cenário: Código digitado que não é número
    Dado que digito um código de fornecedor, um CPF ou um código de continuação
      que não é número
    Quando envio a mensagem
    Então o cursor volta ao primeiro campo recusado
    E a mensagem não é processada

  Cenário: A mensagem começa com os campos de resultado limpos
    Dado que a mensagem anterior mostrou a razão social de um fornecedor
    Quando envio uma mensagem que é recusada
    Então a razão social da mensagem anterior não fica na tela
```
