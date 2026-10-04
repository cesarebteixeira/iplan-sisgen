# US — C697T — Prorrogação do saldo das permissões de contrato da coordenação regional escolar

## Estória

Como **servidor da coordenação regional escolar**, quero **conferir e ajustar, item por
item, o saldo prorrogado da permissão de contrato da minha regional**, para que **a
prorrogação registrada corresponda ao que o fornecedor de fato vai entregar e o saldo
que as escolas ainda podem pedir não fique acima do que o contrato sustenta**.

A permissão de contrato é o que autoriza um fornecedor, dentro de um período e de um
grupo de licitação, a fornecer cada item de compra — uma subclasse e um gênero de
produto. A prorrogação fica registrada ao lado da permissão, item por item, e é dela
que sai o saldo que as escolas ainda podem pedir. Quando a prorrogação de um item não
se sustenta — o item não vai ser fornecido, ou vai ser fornecido em quantidade menor —,
alguém precisa refazer esse saldo antes que ele vire pedido, e é nesta tela que ele é
conferido e ajustado. Sem ela, o contrato segue autorizando quantidade e valor que não
vão ser entregues, e a regional não tem por onde corrigir.

## Contexto

Jornada S000M → C000M → C050M → C664M → C697T.
Ator: servidor de CRE — informa o que identifica a permissão, confere o saldo prorrogado
de cada item, ajusta o que for preciso e confirma.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — a opção 5
do `C000M` abre o menu `C050M`, a opção 6 dele abre o `C664M` e a opção 7 dele chega a
esta tela — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os três menus do caminho não gravam nada: só
encaminham.

Esta tela é a última opção do `C664M`, o mesmo menu das telas que prorrogam o período,
consultam, cancelam e excluem a prorrogação da permissão de contrato. A jornada termina
nela: ela não abre nenhuma outra tela — ela se reapresenta.

O que ela usa do que veio antes é o **tipo de órgão**, a **coordenação regional**, o
**acesso**, a **matrícula**, a **data do sistema** e a **descrição do tipo de órgão** da
sessão, além da **liberação da tela** conferida na abertura; são regras da entrada, e
estão no anexo de evidências, em **Regras que se revelaram da entrada**.

## Regras de negócio

### RN-01 — O que identifica a permissão e o que a tela mostra

A permissão de contrato é identificada pela **coordenação regional escolar**, pelo
**tipo de contrato**, pelo **grupo de licitação**, pelo **fornecedor** e pelo **dia, o
mês e o ano do limite do período**. O **tipo de órgão** não se digita: vem da sessão.

O cabeçalho mostra a **razão social do fornecedor**, buscada no cadastro de fornecedores
pelo código informado, o **início do período**, os **valores adjudicado, aditivo e de
prorrogação** da permissão, a **descrição do tipo de órgão** e a **data do sistema**.
Cada item prorrogado ocupa uma linha e traz a **subclasse**, o **gênero com a sua
descrição**, o **desconto com a marca de sinal** — marca negativa, marca positiva ou
nenhuma marca quando o desconto é zero —, a **quantidade e o valor já prorrogados** e a
**nova quantidade e o novo valor**, que é o que o servidor informa.

A descrição do gênero é buscada no cadastro de gêneros na **versão vigente na data
limite do período**: a tela procura pela subclasse, pelo gênero e por essa data e, não
achando, repete a procura uma vez antes de seguir.

### RN-02 — Os campos com rótulo passam pela conferência numérica antes de qualquer leitura

Os **vinte** campos da tela com rótulo próprio — coordenação regional, tipo de contrato,
fornecedor, grupo de licitação, as três partes do início do período, as três partes do
limite do período, os três valores da permissão, a subclasse, o gênero, o desconto, as
duas quantidades e os dois valores de cada item — são conferidos como número e como data
antes de qualquer consulta ao cadastro. O que não passar é recusado no próprio campo,
com o cursor de volta nele, e nenhuma leitura chega a acontecer. Os valores são tratados
com **duas casas decimais** e as quantidades com **três**.

[?] A mensagem que o servidor vê em cada recusa de campo é montada pela rotina comum de
edição numérica, que não está no acervo desta jornada: o que se pode afirmar é que a
conferência acontece antes das leituras e que o cursor volta ao campo. Pergunta ao site.

### RN-03 — A tela abre em consulta, com a prorrogação que a consulta anterior deixou

Ao ser apresentada, a tela monta o cabeçalho e a grade com o que a sua área de trabalho
guardou e, não havendo operação informada, assume a **consulta**: ela abre lendo, não
gravando. A grade lista em até **doze** linhas os itens da prorrogação registrada para
aquela permissão.

[?] A grade é montada na passagem que apresenta a tela, e essa passagem só lista quando
a área de trabalho já tem a operação da consulta anterior — na primeira abertura não há
o que listar. O que essa área guarda de uma tela para outra, e portanto se a grade
aparece logo depois de consultar ou só na abertura seguinte, não está no material.
Pergunta ao site.

### RN-04 — Sem nenhum item de prorrogação, a tela avisa

Reapresentada com uma permissão que não tem nenhum item de prorrogação registrado, e não
sendo a operação de exclusão, a tela avisa **\* Nao existem registros para atualizacao \***
e não processa mais nada.

### RN-05 — Só a alteração, a exclusão e a consulta são aceitas

Se chegar qualquer operação diferente da **alteração**, da **exclusão** e da
**consulta**, o sistema recusa com **\* Opcao nao disponivel. Use ALT, EXC ou CON \***,
devolve o cursor ao campo da operação e não segue.

[?] A recusa manda usar as teclas de ALT, EXC e CON, mas a conferência compara o que
chegou com os códigos internos dessas operações. Ou o terminal traduz a tecla antes de
enviar, ou a mensagem está desalinhada da conferência. Pergunta ao site.

### RN-06 — A coordenação regional informada tem de ser a da sessão

Quando a sessão tem uma coordenação regional, a coordenação informada tem de ser a
mesma; informando outra, a recusa é **\* Usuario sem acesso a este grupo \*** — a
mensagem chama a coordenação regional de **grupo** —, o cursor volta ao campo e nada é
lido. Quando a sessão não tem coordenação regional, a tela não impõe essa restrição.

[?] Nenhum programa desta jornada atribui a coordenação regional da sessão que a
conferência usa: ela é zerada na abertura da sessão e só telas de contrato fora desta
jornada aparecem preenchendo-a. Se ela chegar vazia, a tela recusa qualquer coordenação
regional informada. Pergunta ao site.

### RN-07 — Alterar e excluir exigem que a permissão já tenha sido consultada

Na alteração, se o limite do período, a coordenação regional, o tipo de contrato e o
grupo de licitação informados não forem exatamente os que estão carregados, a recusa é
**\* Consulte antes de atualizar \***; na exclusão, com a mesma condição, a recusa é
**\* Consulte antes de excluir \***. Em qualquer das duas o cursor volta ao campo da
operação, e nada é lido nem gravado.

### RN-08 — A alteração exige a prorrogação registrada, a permissão cadastrada e o período prorrogado

Antes de alterar, o sistema confere três coisas, nesta ordem: não havendo **item de
prorrogação registrado** para aquela permissão, a recusa é
**\* Registros para atualizacao nao cadastrados \***; não estando a **permissão
cadastrada**, **\* Permissao nao cadastrada \***; e não estando o **período prorrogado**
correspondente, **\* Data limite nao e de prorrogacao \***. Nas três, o cursor volta ao
campo da operação e nada é gravado.

### RN-09 — A consulta confere a permissão e o período prorrogado, mostra o cabeçalho e não grava nada

Consultando, o sistema procura a permissão com o que foi informado; não a achando, a
recusa é **\* Permissao nao cadastrada \***, com o cursor de volta na coordenação
regional. Achando, procura o período prorrogado da permissão; não o achando, a recusa é
**\* Prorrogacao nao cadastrada \***, com o cursor de volta ao limite do período.
Passando pelas duas, a tela carrega o fornecedor, o início do período e os três valores
da permissão, e os exibe.

A consulta **não altera a permissão nem o período prorrogado**: não há gravação,
alteração nem exclusão de nenhum dos dois nessa operação.

[?] Há, no caminho da consulta, um trecho que grava a prorrogação do item quando não
encontra nenhuma para a permissão: ele lê o período prorrogado e a permissão e registra
a prorrogação daquele item com a quantidade e o valor do período. Se esse trecho chega a
rodar depende de a procura pela prorrogação devolver vazio, e a procura deixa a classe,
a subclasse e o gênero em branco — o que o sistema faz com esses componentes em branco
não está documentado no material. Pergunta ao site.

### RN-10 — A exclusão exige a prorrogação registrada

Antes de excluir, o sistema procura a prorrogação da permissão; não a achando, a recusa
é **\* Prorrogacao nao cadastrada \***, com o cursor de volta ao campo da operação, e
nada é apagado.

### RN-11 — A nova quantidade de um item não pode passar da quantidade prorrogada

Em cada item, a nova quantidade informada só é considerada se for **diferente** da
quantidade já prorrogada; sendo **maior** que ela, a recusa é
**\* Nova quantidade deve ser < que prorrogada \***, com o cursor de volta à nova
quantidade daquela linha, e nada é gravado. Item cuja subclasse esteja em branco é
simplesmente ignorado.

### RN-12 — O novo saldo do item não pode ficar abaixo da quantidade comprometida

Recalculado o total do item — o que a permissão daquele item já tem de inicial e de
aditivo, mais a quantidade prorrogada, trocando-se a prorrogação antiga pela nova —, se
esse total ficar **menor** que a quantidade já comprometida com pedidos, a recusa é
**\* Qt ini+adi+prorrog < quant comprometida \***, com o cursor de volta à nova
quantidade daquela linha, e nada é gravado.

### RN-13 — A alteração regrava o item: nova quantidade e novo valor; zero zera o saldo prorrogado

Confirmada a alteração, para cada item em que a nova quantidade difere da prorrogada o
sistema procura o item pela chave completa — com a classe vinda do cadastro de gêneros —
e grava a **nova quantidade prorrogada** e o **novo valor prorrogado**, calculado a
partir do **preço unitário** e do **desconto** registrados. Se a nova quantidade for
**zero**, o saldo prorrogado do item — quantidade e valor — é **zerado**.

Item que não for encontrado, e item cuja permissão não for encontrada na conferência do
total, são **descartados em silêncio**: nada é gravado e a tela não avisa.

[?] O significado de negócio do desconto da prorrogação e a conta do preço unitário
(dividir o desconto por cem, somar um e multiplicar pelo preço unitário) não estão no
corpus; do jeito que está, a conta só muda o preço unitário quando o desconto chega a
cem. Pergunta ao site.

### RN-14 — A exclusão apaga os itens da prorrogação e devolve a tela em consulta

Confirmada a exclusão, o sistema percorre os itens da prorrogação daquela permissão —
relendo a cada volta até não achar mais —, **apaga cada um** e devolve a área de trabalho
em **consulta**, com o aviso **Cadastro Excluido**.

[?] A procura que alimenta a exclusão é montada com a coordenação regional, o tipo de
contrato, o grupo de licitação, o fornecedor e o período da permissão, mas deixa a
classe, a subclasse e o gênero do item em branco. Se essa procura alcança todos os itens
da permissão ou apenas os que têm esses três componentes em branco — e, portanto, se a
exclusão apaga tudo ou quase nada —, o material não documenta. Pergunta ao site.

### RN-15 — O saldo ajustado fica só na prorrogação do item

O ajuste que o servidor faz na tela é gravado na **prorrogação daquele item**, e é só
ali que ele aparece. O trecho que levaria o saldo ajustado para a **permissão** e para o
**período prorrogado** — apagando as prorrogações já aplicadas e deixando o registro na
**trilha de auditoria** e no histórico da operação — depende de o **indicador de sucesso
da tela** chegar marcado do formulário, e nada no programa o marca. A prorrogação que
esta tela mantém **não é lida por nenhuma outra tela** do sistema.

[?] Ou o indicador de sucesso vem marcado do formulário, ou o trecho que consolida o
ajuste ficou inalcançável — e, nesse caso, o que a tela avisa ao servidor não corresponde
ao que ficou gravado para o resto do sistema, e o saldo ajustado aqui não vale para os
pedidos das escolas. O material não permite decidir entre os dois. Pergunta ao site.

### RN-16 — Só quem tem a tela e a operação liberadas passa

Ao apresentar a tela, o sistema confere na autorização do usuário o **acesso à tela**:
sem a tela cadastrada a recusa é **\* Tela nao disponivel \***, e sem o perfil de acesso,
**\* Acesso negado para esta matricula \***. Na conferência do que foi informado, passa
ainda pela **rota** do sistema e pela **liberação da operação**: a alteração exige, no
perfil, a liberação de alteração, e a exclusão, a de exclusão — não estando, a recusa é
**\* Acesso negado para esta operacao \***. A consulta não tem liberação própria: quem
tem a tela autorizada consulta.

[?] As rotinas de segurança avisam a recusa e mesmo assim devolvem "OK" a quem as chamou;
o que de fato interrompe a transação não está no acervo desta jornada. Pergunta ao site.

### RN-17 — A tela só opera quando é ela a tela atendida, e não encaminha para outra

A tela não abre nenhuma outra: ela se **reapresenta**, linha a linha da grade, até a
última. E ela só processa o que foi informado quando **é ela a tela atendida**: se o
pedido chegar marcado com a **tela de origem**, ela não lê nem grava nada — a rotina de
rota devolve o comando à tela de origem. É por isso que, vinda pelo menu, ela processa
normalmente: o menu a chama sem tela de origem.

Nenhuma outra tela do sistema chama esta: a única que a abre é o menu `C664M`.

## Cenários BDD

```gherkin
Funcionalidade: Prorrogação do saldo das permissões de contrato da coordenação regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C697T

  Cenário: RN-01 e RN-09 — consultar a permissão de contrato
    Dado que a permissão está cadastrada e tem período prorrogado
    Quando informo a coordenação regional, o tipo de contrato, o grupo de licitação, o fornecedor e o dia, o mês e o ano do limite do período
    E confirmo a consulta
    Então vejo a razão social do fornecedor, o início do período e os valores adjudicado, aditivo e de prorrogação
    E vejo a descrição do tipo de órgão e a data do sistema
    E a permissão e o período prorrogado continuam como estavam

  Cenário: RN-01 e RN-03 — a grade dos itens prorrogados
    Dado que a permissão tem itens de prorrogação registrados
    Quando a tela se reapresenta
    Então vejo em até doze linhas cada item com a subclasse, o gênero e a sua descrição
    E vejo o desconto com a marca de sinal e a quantidade e o valor já prorrogados
    E vejo a nova quantidade e o novo valor de cada item

  Cenário: RN-02 — campo com rótulo que não é número
    Dado que estou na tela C697T
    Quando informo letra onde o campo espera número ou data
    Então a tela recusa o campo e devolve o cursor a ele
    E nenhuma leitura de cadastro é feita

  Cenário: RN-03 — a tela abre em consulta
    Dado que não informei nenhuma operação
    Quando a tela C697T se apresenta
    Então ela abre em consulta
    E nada é gravado

  Cenário: RN-04 — permissão sem nenhum item de prorrogação
    Dado que a permissão carregada não tem item de prorrogação registrado
    Quando a tela se reapresenta
    Então vejo a mensagem "* Nao existem registros para atualizacao *"
    E nada mais é processado

  Cenário: RN-05 — operação diferente de ALT, EXC e CON
    Dado que estou na tela C697T
    Quando informo uma operação diferente de ALT, EXC e CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT, EXC ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: RN-06 — coordenação regional fora da minha sessão
    Dado que a minha sessão está presa a uma coordenação regional
    Quando informo outra coordenação regional
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenação regional
    E nada é lido

  Cenário: RN-07 — alterar sem consultar antes
    Dado que o que identifica a permissão é diferente do que está carregado
    Quando tento alterar
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E nada é lido nem gravado

  Cenário: RN-07 — excluir sem consultar antes
    Dado que o que identifica a permissão é diferente do que está carregado
    Quando tento excluir
    Então vejo a mensagem "* Consulte antes de excluir *"
    E nada é lido nem apagado

  Cenário: RN-08 — alterar uma permissão sem item de prorrogação registrado
    Dado que consultei a permissão e ela não tem item de prorrogação registrado
    Quando tento alterar
    Então vejo a mensagem "* Registros para atualizacao nao cadastrados *"
    E nada é gravado

  Cenário: RN-08 — alterar uma permissão não cadastrada
    Dado que a permissão informada não está cadastrada
    Quando tento alterar
    Então vejo a mensagem "* Permissao nao cadastrada *"
    E nada é gravado

  Cenário: RN-08 — alterar uma permissão cujo período não é de prorrogação
    Dado que a permissão não tem o período prorrogado correspondente
    Quando tento alterar
    Então vejo a mensagem "* Data limite nao e de prorrogacao *"
    E nada é gravado

  Cenário: RN-09 — consultar uma permissão não cadastrada
    Quando informo uma coordenação regional, um tipo de contrato, um grupo de licitação, um fornecedor e um período que não têm permissão
    Então vejo a mensagem "* Permissao nao cadastrada *"
    E o cursor volta ao campo da coordenação regional
    E nada é gravado

  Cenário: RN-09 — consultar uma permissão sem período prorrogado
    Dado que a permissão está cadastrada e não tem o período prorrogado
    Quando confirmo a consulta
    Então vejo a mensagem "* Prorrogacao nao cadastrada *"
    E o cursor volta ao limite do período
    E nada é gravado

  Cenário: RN-10 — excluir uma permissão sem prorrogação registrada
    Dado que consultei a permissão e ela não tem prorrogação registrada
    Quando tento excluir
    Então vejo a mensagem "* Prorrogacao nao cadastrada *"
    E nada é apagado

  Cenário: RN-11 — nova quantidade maior que a prorrogada
    Dado que informo, num item, uma nova quantidade maior que a quantidade prorrogada
    Quando confirmo a alteração
    Então vejo a mensagem "* Nova quantidade deve ser < que prorrogada *"
    E o cursor volta à nova quantidade daquela linha
    E nada é gravado

  Cenário: RN-12 — novo saldo abaixo da quantidade comprometida
    Dado que o total do item, com a nova quantidade, fica abaixo da quantidade comprometida com pedidos
    Quando confirmo a alteração
    Então vejo a mensagem "* Qt ini+adi+prorrog < quant comprometida *"
    E o cursor volta à nova quantidade daquela linha
    E nada é gravado

  Cenário: RN-13 — alteração que ajusta o saldo prorrogado de um item
    Dado que o item tem prorrogação registrada e informo uma nova quantidade menor que a prorrogada
    E que o total do item não fica abaixo da quantidade comprometida
    Quando confirmo a alteração
    Então o item passa a ter a nova quantidade prorrogada
    E o novo valor prorrogado é calculado a partir do preço unitário e do desconto registrados

  Cenário: RN-13 — nova quantidade zero zera o saldo prorrogado do item
    Dado que informo zero como nova quantidade de um item prorrogado
    Quando confirmo a alteração
    Então a quantidade e o valor prorrogados daquele item ficam zerados
    E o item continua registrado

  Cenário: RN-13 — item sem prorrogação registrada é descartado em silêncio
    Dado que informo uma nova quantidade para um item que não tem prorrogação registrada
    Quando confirmo a alteração
    Então nada é gravado naquele item
    E não vejo nenhuma mensagem

  Cenário: RN-14 — exclusão dos itens da prorrogação
    Dado que a permissão tem itens de prorrogação registrados
    Quando confirmo a exclusão
    Então os itens daquela prorrogação são apagados
    E a tela volta em consulta com o aviso "Cadastro Excluido"

  Cenário: RN-15 — o saldo ajustado não chega à permissão nem ao período prorrogado
    Dado que ajustei o saldo prorrogado de um item
    Quando consulto a mesma permissão em outra tela do menu C664M
    Então a quantidade e o valor prorrogados da permissão e do período continuam iguais aos de antes do ajuste
    E nenhum registro daquela alteração aparece na trilha de auditoria

  Cenário: RN-16 — tela não cadastrada para o meu perfil
    Dado que a tela C697T não está entre as minhas telas autorizadas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E nada é lido nem gravado

  Cenário: RN-16 — operação não liberada para o meu perfil
    Dado que o meu perfil não tem a liberação de alteração nem a de exclusão
    Quando tento alterar ou excluir
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é lido nem gravado

  Cenário: RN-17 — a tela se reapresenta e não encaminha para outra
    Dado que estou na tela C697T
    Quando confirmo a operação
    Então a tela se reapresenta a mim
    E nenhuma outra tela é aberta

  Cenário: RN-17 — tela atendida por outra tela dentro da mesma transação
    Dado que o pedido chega marcado com a tela de origem
    Quando a tela C697T é processada
    Então ela não lê nem grava nada
    E o comando volta à tela de origem
```
