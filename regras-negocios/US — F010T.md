# US — F010T — Manter o cadastro de códigos de gênero FAE

## Estória

Como **servidor de CRE**, quero **manter o cadastro dos códigos de gênero FAE —
incluindo um código novo com a sua descrição, corrigindo a descrição de um código
existente e apagando o código que não serve mais — e mandar um código já
cadastrado para a tela que trata as unidades de medida dele**, para que **o código
que classifica o item no FNDE exista uma única vez, com uma descrição acordada, e
possa ser detalhado sem que ninguém precise redigitar o código**.

O código de gênero FAE é a chave pela qual o item é tratado no FNDE: é ele que
amarra gênero, subclasse e unidade de medida. Sem este cadastro, a classificação
do item fica sem código, e o vínculo com o gênero não tem a quem se referir. Esta
é a tela que cria, corrige e apaga esse código; e é por ela que se chega à tela
que detalha as unidades de medida do código — que só recebe o que aqui existe.

A tela é de manutenção, e não só de leitura: passando pelas conferências,
incluir, alterar e apagar gravam, e cada gravação deixa registro no rastro de
auditoria. A consulta é a única operação que não grava nada.

## Contexto

Jornada S000M → F000M → F010T.

Ator: servidor de CRE — mantém o cadastro dos códigos de gênero FAE e manda um
código já cadastrado para a tela das unidades de medida.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

As regras abaixo são só as da tela desta jornada. A tela anterior só encaminha: a
`F000M` não deixa dado de negócio para a `F010T`, apenas a escolha da opção que
abre a tela; o contexto que a `F010T` usa — matrícula, código de acesso,
privilégio, tipo de órgão e CRE — é o que a entrada deixou na sessão, e a `F010T`
apenas o repassa às rotinas de segurança. A única coisa que a origem da chamada
muda nesta tela é o modo em que ela abre (RN-02).

---

## Regras de negócio

### RN-01 — Esta é a tela que mantém o cadastro de códigos de gênero FAE

Esta é a tela de manutenção do cadastro de códigos de gênero FAE: ela **inclui**,
**altera** e **apaga** o código e o texto que o descreve. Passando pelas
conferências, cada uma dessas operações grava no cadastro e deixa um registro no
rastro de auditoria.

É o único cadastro que esta tela grava, além do rastro: os cadastros que ela
apenas consulta — o das telas, o dos vínculos do código com gênero e subclasse —
são só lidos. O vínculo com gênero é mantido em outra tela; aqui ele só é
consultado, para não deixar apagar um código que ainda está em uso.

O código é a chave do cadastro: não há dois códigos iguais, e a tela trata o
código como texto de sete dígitos, com a descrição de setenta e seis caracteres
como conteúdo obrigatório. Os códigos que o código guarda de quem o criou e de
quando o criou acompanham a ficha.

[?] A ficha do código tem dois textos: a descrição e uma segunda descrição, mais
curta. A tela lê a curta e a entrega adiante, mas nenhum programa do acervo lido
a grava. Se ela deveria ser informada nesta tela, o campo não existe aqui.
Pergunta ao site.

[?] Depois de uma recusa, o que impede a gravação é o estado que a rotina comum
de mensagem deixa. Essa rotina não faz parte do acervo lido. Se ela não marcar
esse estado, uma operação recusada ainda seria gravada. Pergunta ao site.

### RN-02 — A tela abre em consulta, e só a opção de alteração grava

A tela tem um campo de opção. Quando quem a abre não deixa opção nenhuma, ela
abre em **consulta**, e com o código de partida zerado — é assim que ela abre
pelo menu. Quem chama a tela pode deixar a opção de **alteração** no lugar; no
acervo lido, nenhuma chamada faz isso.

Informada uma opção diferente de alteração e de consulta — ou em branco —, o
sistema recusa com **\* Opcao nao disponivel. Use ALT ou CON \***, devolve o
cursor ao campo da opção e não lê nem grava nada.

Na **consulta**, a tela não confere a operação e não grava: ela mostra a lista e
sai antes das verificações. Só a opção de **alteração** chega às operações que
gravam — incluir, alterar e apagar.

[?] A recusa nomeia as opções ALT e CON, mas a tela compara a opção informada com
outros dois valores. Se a máscara da tela não traduzir o que o operador digita
para esses valores, a opção legítima seria recusada. O acervo lido não traz a
máscara. Pergunta ao site.

[?] A conferência da operação só corre quando a mensagem chega sem uma tela
seguinte indicada; a passagem que grava não repete essa condição. Se esse campo
chegar preenchido de quem chamou a tela, a operação é gravada sem passar por
conferência alguma; se ele só se preenche na saída, a condição não barra nada. O
acervo lido não diz quem o preenche. Pergunta ao site.

### RN-03 — A lista mostra quatro códigos por vez, a partir do código inicial

A tela trabalha com uma lista de **até quatro códigos por vez**. Em cada linha
aparecem o **código do gênero FAE**, a **descrição**, a **situação da linha** (a
operação que se quer: incluir, alterar ou apagar) e a **marca de consulta**. Fora
da lista, a tela mostra o **órgão** da sessão, a **data do sistema** e o campo do
**código inicial**, com a descrição dele.

A lista começa no código informado no campo do **código inicial**; em branco, ela
começa no primeiro código cadastrado. Quando a lista termina, o campo recebe o
último código mostrado e a descrição dele — é por ali que se continua a leitura; e
quando não há mais códigos, o campo volta a zero.

### RN-04 — Sem nenhum código cadastrado, a tela avisa

Não havendo nenhum código cadastrado — ou não havendo código a partir do ponto
informado —, a tela avisa **\* Nao existem codigos cadastrados \*** e zera o
campo do código inicial e a descrição dele.

### RN-05 — A inclusão exige código novo e descrição informada

Para incluir, o código informado **não pode estar cadastrado**: estando, a recusa
é **\* Codigo FNDE ja cadastrado \***, com o cursor de volta ao campo da situação
da linha. A **descrição** também é obrigatória: em branco, a recusa é
**\* Informe a descricao \***, com o cursor no campo da descrição.

Passando as duas conferências, o código é gravado com a descrição informada, a
**matrícula** de quem incluiu e a **data** da sessão como data de atualização, e
o rastro de auditoria guarda o conteúdo posterior — na inclusão, o conteúdo
anterior vai em branco.

### RN-06 — A alteração exige código cadastrado e descrição informada

Para alterar, o código informado **tem de estar cadastrado**: não estando, a
recusa é **\* Codigo FNDE nao cadastrado \***, com o cursor de volta ao campo da
situação da linha. A **descrição** também é obrigatória, com a mesma recusa da
inclusão — **\* Informe a descricao \***.

Passando, a alteração grava a nova descrição e a **matrícula** de quem alterou, e
o rastro de auditoria guarda o conteúdo anterior e o posterior.

[?] A alteração troca a matrícula pela de quem alterou, mas não refaz a data de
atualização: a ficha continua mostrando a data em que o código foi criado ou
alterado pela última vez antes desta alteração. Se a data deveria acompanhar a
matrícula, é pergunta ao site.

### RN-07 — A exclusão exige código cadastrado e nenhuma relação com gênero

Para apagar, o código informado **tem de estar cadastrado**: não estando, a
recusa é **\* Codigo FNDE nao cadastrado \***. O código também **não pode estar
relacionado com gênero e subclasse**: estando, a recusa é
**\* Codigo FNDE ja relacionado com codigo genero \***, com o cursor de volta ao
campo da situação da linha. Esta tela não apaga relação nenhuma — ela só se
recusa a apagar o código enquanto a relação existir.

Passando, o código é apagado e o rastro de auditoria guarda o conteúdo anterior;
na exclusão, o conteúdo posterior vai em branco.

[?] A consulta que sustenta essa recusa procura a relação com o código de
subclasse e o código de gênero zerados. Se ela for feita pela chave inteira, um
código relacionado apenas a subclasses e gêneros reais não é encontrado — e o
código é apagado deixando a relação órfã; se for feita pelo começo da chave, a
recusa funciona. O acervo não diz qual das duas leituras vale. Pergunta ao site.

### RN-08 — O código marcado para consulta é entregue à tela das unidades de medida

O operador marca a **marca de consulta** de uma linha (a letra **X**) para levar
aquela linha à tela que trata as unidades de medida do código. A linha precisa
ter código: em branco, a recusa é **\* Linha nao preenchida \***, com o cursor na
marca. O código também tem de estar cadastrado: não estando, a recusa é
**\* Codigo FNDE nao cadastrado \***, com o cursor na marca.

Passando, a tela **entrega à tela seguinte**: o **código do gênero FAE**, a
**descrição** e a **descrição curta** lidos do cadastro, a informação de que o
modo é **consulta** e a tela de origem. A tela das unidades de medida abre então
**em consulta, já posicionada nesse código**, e não refaz o próprio
posicionamento. Esta tela, nesse caminho, não grava nada: só entrega e sai.

O caminho funciona tanto na consulta quanto na alteração; ele vem antes das
conferências das operações que gravam. A tela lembra por qual tela foi chamada:
quando o pedido de encaminhamento tem por destino a própria tela que a chamou, o
sistema apenas devolve o controle, sem refazer a apresentação da lista.

[?] A entrega é feita por uma área de trabalho comum às duas telas. No fonte, a
área de trabalho das duas tem uma diferença: antes dela, a tela de destino guarda
um bloco de campos que esta não tem. O acervo não diz se os valores são
encontrados pelo nome dos campos ou pela posição; se for pela posição, os valores
não chegam alinhados e a tela seguinte abre no código errado. Pergunta ao site.

### RN-09 — O código e o código inicial passam por edição numérica

Dois campos passam por edição numérica antes de qualquer leitura: o **código do
gênero FAE** (sete dígitos) e o **código inicial** (sete dígitos). Em branco, o
campo vira zero. O que não for número é recusado, o cursor volta ao primeiro
campo recusado — o código ou o código inicial — e a operação não é feita.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual —
não está nos fontes desta jornada: a rotina que faz a edição não faz parte do
acervo lido. Pergunta ao site.

### RN-10 — Cada mensagem começa com os resultados anteriores limpos

Antes de conferir qualquer coisa, a tela apaga o órgão, a data do sistema e a
descrição do código inicial que a operação anterior havia mostrado. Uma operação
recusada, portanto, não deixa na tela o resultado anterior.

### RN-11 — Antes de operar, a tela confere o acesso e a operação autorizada

Toda mensagem passa por três conferências, com o contexto da sessão — matrícula,
código de acesso, privilégio, tipo de órgão e CRE. Primeiro, a tela precisa estar
cadastrada no cadastro de telas: não estando, o acesso é recusado com
**\* Tela nao disponivel \***. Depois, a matrícula precisa ter a tela autorizada
no seu código de acesso: não tendo, a recusa é
**\* Acesso negado para esta matricula \***. Por fim, alterar e apagar exigem,
cada uma, a autorização correspondente no código de acesso, e sem ela a recusa é
**\* Acesso negado para esta operacao \***.

[?] A inclusão não exige a autorização de inclusão: ela é conferida como
consulta, e quem tem a tela autorizada inclui. Se a intenção era exigir essa
autorização, o caminho não a exige. Pergunta ao site.

### RN-12 — Toda operação que grava deixa rastro de auditoria

Cada inclusão, alteração e exclusão grava um registro no cadastro de auditoria com
o **conteúdo anterior** e o **conteúdo posterior** do código, a **matrícula** do
servidor, a **data e a hora** da sessão, a **estação**, o **órgão**, a **CRE** e o
cadastro de origem. Na inclusão o conteúdo anterior sai em branco; na exclusão, o
posterior sai em branco. A operação registrada é a que foi executada — inclusão,
alteração ou exclusão.

[?] A inclusão só grava o rastro quando o estado da operação não é um certo valor
técnico que o acervo não explica; se existe um caminho em que a inclusão passa
sem deixar rastro, é pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter o cadastro de códigos de gênero FAE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F010T

  Cenário: Consulta da lista de códigos
    Dado que existem códigos de gênero FAE cadastrados
    Quando informo a opção de consulta
    Então vejo, em cada linha, o código do gênero FAE, a descrição e a situação da linha
    E vejo o órgão da minha sessão, a data do sistema e o campo do código inicial
    E não vejo mais de quatro linhas por vez

  Cenário: A lista começa no código inicial informado
    Dado que existem códigos cadastrados
    Quando informo o código inicial e peço a consulta
    Então a lista começa no código informado
    E ao terminar a lista o campo do código inicial mostra o último código mostrado e a descrição dele

  Cenário: A consulta não grava nada
    Dado que existem códigos cadastrados
    Quando informo a opção de consulta
    Então nenhum código é incluído, alterado ou apagado
    E nenhum registro de auditoria é gerado

  Cenário: Não há nenhum código cadastrado
    Dado que não existe nenhum código de gênero FAE cadastrado
    Quando peço a consulta
    Então vejo a mensagem "* Nao existem codigos cadastrados *"
    E o campo do código inicial e a descrição dele ficam zerados

  Cenário: Opção diferente de alteração e de consulta
    Dado que estou na tela F010T
    Quando informo uma opção diferente de alteração e de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é lido nem gravado

  Cenário: Inclusão de um código novo
    Dado que o código informado não está cadastrado
    E informo a descrição do código
    Quando peço a inclusão
    Então o código é gravado com a descrição informada
    E a ficha do código fica com a minha matrícula e com a data de hoje

  Cenário: Inclusão de um código já cadastrado
    Dado que o código informado já está cadastrado
    Quando peço a inclusão
    Então vejo a mensagem "* Codigo FNDE ja cadastrado *"
    E o cursor volta ao campo da situação da linha
    E o código não é incluído de novo

  Cenário: Descrição não informada na inclusão
    Dado que o código informado não está cadastrado
    E deixo a descrição em branco
    Quando peço a inclusão
    Então vejo a mensagem "* Informe a descricao *"
    E o cursor volta ao campo da descrição
    E o código não é criado

  Cenário: Alteração bem-sucedida
    Dado que o código informado está cadastrado
    Quando informo a nova descrição
    E peço a alteração
    Então a descrição do código é gravada
    E a ficha do código fica com a minha matrícula

  Cenário: Alteração de um código não cadastrado
    Dado que o código informado não está cadastrado
    Quando peço a alteração
    Então vejo a mensagem "* Codigo FNDE nao cadastrado *"
    E o cursor volta ao campo da situação da linha
    E nada é gravado

  Cenário: Descrição não informada na alteração
    Dado que o código informado está cadastrado
    E deixo a descrição em branco
    Quando peço a alteração
    Então vejo a mensagem "* Informe a descricao *"
    E o cursor volta ao campo da descrição
    E nada é gravado

  Cenário: Exclusão de um código
    Dado que o código informado está cadastrado
    E não está relacionado com nenhum gênero
    Quando peço a exclusão
    Então o código é apagado
    E a exclusão deixa registro no rastro de auditoria

  Cenário: Exclusão de um código não cadastrado
    Dado que o código informado não está cadastrado
    Quando peço a exclusão
    Então vejo a mensagem "* Codigo FNDE nao cadastrado *"
    E o cursor volta ao campo da situação da linha
    E nada é apagado

  Cenário: Exclusão de um código já relacionado com gênero
    Dado que o código informado está cadastrado
    E está relacionado com gênero e subclasse
    Quando peço a exclusão
    Então vejo a mensagem "* Codigo FNDE ja relacionado com codigo genero *"
    E o cursor volta ao campo da situação da linha
    E o código não é apagado

  Cenário: Marca de consulta sem a linha preenchida
    Dado que marco a consulta de uma linha que está sem código
    Quando peço a operação
    Então vejo a mensagem "* Linha nao preenchida *"
    E o cursor volta à marca de consulta
    E nada é encaminhado

  Cenário: Marca de consulta de um código não cadastrado
    Dado que marco a consulta de uma linha com um código que não está cadastrado
    Quando peço a operação
    Então vejo a mensagem "* Codigo FNDE nao cadastrado *"
    E o cursor volta à marca de consulta
    E nada é encaminhado

  Cenário: O código marcado é entregue à tela das unidades de medida, em consulta
    Dado que marco a consulta de uma linha com um código cadastrado
    Quando peço a operação
    Então a tela das unidades de medida abre em consulta
    E ela já abre posicionada no código que marquei
    E esta tela não grava nada ao encaminhar

  Cenário: Código digitado que não é número
    Dado que digito um código do gênero FAE ou um código inicial que não é número
    Quando peço a operação
    Então o cursor volta ao primeiro campo recusado
    E a operação não é feita

  Cenário: O resultado da operação anterior não fica na tela
    Dado que já mostrei uma lista de códigos
    Quando peço uma nova consulta
    Então o órgão, a data do sistema e a descrição do código inicial que apareciam não ficam na tela
    E só aparecem os resultados da consulta que passou nas conferências

  Cenário: Toda operação de gravação deixa rastro de auditoria
    Dado que incluo, altero ou apago um código
    Quando a operação é gravada
    Então o rastro guarda o conteúdo anterior e o posterior do código
    E guarda a minha matrícula, a data e a hora, a estação, o órgão, a CRE e o cadastro de origem
    E registra a operação que foi executada

  Cenário: Tela não cadastrada
    Dado que a tela F010T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela F010T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Sem autorização para a operação
    Dado que a minha matrícula tem a tela F010T autorizada, mas não a operação de apagar
    Quando peço a exclusão
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E o código não é apagado
```
