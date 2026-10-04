# US — F020T — Manter o vínculo do gênero com o gênero FAE

## Estória

Como **servidor de CRE**, quero **manter, pelo código do gênero FAE, quais gêneros
ficam vinculados a ele, com que unidade de medida e com que unidade de conversão**,
para que **cada item seja classificado e medido pelo código e pela conversão que o
cadastro determina, sem depender de quem digitou**.

O vínculo entre o gênero e o gênero FAE é o que diz em que código o item é tratado,
em que unidade ele é medido e quanto vale a conversão entre a unidade do gênero e a
unidade do código. É esta tela que cria, altera e apaga esse vínculo: a consulta do
mesmo vínculo (a `F022T`) só mostra o que aqui foi mantido, e a tela dos códigos de
gênero FAE (a `F010T`) só lê os vínculos, sem gravar nenhum. Sem esta tela o vínculo
não existe, e o item fica sem código e sem conversão para ser medido e classificado.

A tela é de manutenção: as operações que passam pelas conferências gravam e deixam
rastro no cadastro de auditoria. A consulta é a única que não grava nada.

## Contexto

Jornada S000M → F000M → F020T.

Ator: servidor de CRE — mantém, por código de gênero FAE, os gêneros vinculados a
ele, com a unidade de medida do código e a conversão de cada gênero.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. As duas telas do caminho são menus e só
encaminham: a `F000M` não deixa operação nem código para a tela seguinte, e as
regras da entrada não se repetem aqui.

As regras abaixo são só as da tela desta jornada. O que a tela usa do que veio antes
é o contexto da sessão — a **matrícula**, o **código de acesso**, o **privilégio**,
o **tipo de órgão**, a **CRE** e a **data do sistema**; isso pertence ao documento
da entrada e está no anexo de evidências, em **Regras que se revelaram da entrada**.

Esta tela não muda de comportamento conforme quem a chamou: ela abre em consulta, e
é ela que decide o que fazer com o que o servidor informa (RN-15). Ela também não
passa nada adiante — é o fim da jornada, e o que ela deixa gravado é o que as outras
telas leem.

## Regras de negócio

### RN-01 — A tela mantém o vínculo do gênero com o código de gênero FAE

Informado o **código do gênero FAE**, a tela mostra os **gêneros vinculados** a ele.
Cada linha da lista traz o **código de subclasse**, o **código de gênero**, a
**descrição resumida do gênero**, a **unidade de medida do gênero**, a **unidade de
conversão** entre a unidade do gênero e a do código, e a **situação da linha** — o
que se quer fazer com ela. A lista mostra **doze linhas por vez**.

Não havendo nenhum vínculo para o código que estava na tela, ela avisa
**\* Nao existem relacionamentos cadastrados \*** e deixa a lista vazia.

Os cadastros que a tela lê são o das telas, o dos códigos de gênero FAE, o dos
gêneros, o das unidades de medida, o das unidades de medida de cada código FAE e o
do próprio vínculo. O único cadastro que ela grava é o do vínculo — e, a cada
gravação nele, o da auditoria.

### RN-02 — A tela abre em consulta, e incluir, alterar e consultar são as opções aceitas

A tela tem um campo de opção. Quando quem a abre não deixa opção nenhuma, ela abre
em **consulta**.

Informada uma opção que não seja incluir, alterar ou consultar — inclusive a de
excluir —, o sistema recusa com **\* Opcao nao disponivel. Use INC, ALT ou CON \***,
devolve o cursor ao campo da opção e não lê nem grava nada.

A **exclusão não é uma opção da tela**: ela se pede pela situação de uma linha, e só
quando a tela está em alteração (RN-09).

[?] Os valores que a tela aceita não são literais no programa: eles vêm da tabela de
mensagens do ambiente, carregada em tempo de execução. É por isso que a recusa manda
usar "INC", "ALT" e "CON" enquanto a tela compara os códigos internos dessa tabela.
Se o que o servidor digita é exatamente "INC", "ALT" e "CON", o acervo lido não
permite confirmar.

### RN-03 — O código do gênero FAE e a unidade de medida dele são obrigatórios, e o código tem de estar cadastrado na inclusão

O **código do gênero FAE** é o assunto da tela e tem de ser informado: em branco, a
recusa é **\* Informe o codigo FNDE \***, com o cursor de volta ao campo do código, e
nada é conferido nem gravado.

Na **inclusão**, o código ainda tem de existir no cadastro dos códigos de gênero
FAE: não existindo, a recusa é **\* Codigo FNDE nao cadastrado \***, também com o
cursor no campo do código.

Na **inclusão** e na **alteração**, a **unidade de medida do código** tem de ser
informada — em branco, a recusa é **\* Informe a unidade de medida do codigo FNDE
\*** — e tem de estar vinculada àquele código — não estando, a recusa é
**\* Unid.medida nao cadastrada para este cod.FNDE \***. Nas duas recusas o cursor
volta ao campo da unidade de medida, e nada é gravado.

[?] A tela e as mensagens falam em **código FNDE**, e o rótulo do campo fala em
**gênero FAE**. Se FNDE e FAE são o mesmo ente, é pergunta ao site.

### RN-04 — A consulta carrega o código e a lista dele, e não grava nada

Na **consulta** a tela usa o código informado para trazer os vínculos dele e mostrar
a lista. Não havendo vínculo para o código, a recusa é
**\* Relacionamentos nao cadastrados \***, com o cursor de volta ao campo do código,
e a lista fica vazia.

A consulta **não grava**: nenhum vínculo é criado, alterado ou apagado, o código não
é mexido e nenhuma linha de auditoria é gerada. O que ela deixa é a ficha do código
na sessão, e é ela que habilita a alteração da mensagem seguinte (RN-05).

Na consulta o cadastro dos códigos de gênero FAE não é conferido: um código que não
existe nesse cadastro recebe a mesma resposta que um código cadastrado e sem vínculo.

### RN-05 — A alteração exige que o código tenha sido consultado antes

Para **alterar** — e, com ela, para incluir, alterar ou excluir uma linha (RN-06 a
RN-09) —, o código informado tem de ser o mesmo que a **consulta** anterior deixou na
sessão: sendo outro, a recusa é **\* Consulte antes de atualizar \***, com o cursor de
volta ao campo do código, e nada é gravado. É a consulta que carrega a ficha do
código; a alteração só segue sobre a ficha já carregada.

### RN-06 — Na inclusão de uma linha, o gênero tem de existir e ainda não estar vinculado

Na **inclusão**, cada linha com gênero é conferida nesta ordem:

- o **gênero** — o par formado pelo código de subclasse e pelo código de gênero —
  tem de existir no cadastro dos gêneros: não existindo, a recusa é
  **\* Genero nao cadastrado \***;
- o **vínculo** entre aquele gênero e aquele código de gênero FAE não pode existir:
  existindo, a recusa é **\* Genero ja cadastrado neste relacionamento \***;
- aquele gênero **não pode estar vinculado a outro código de gênero FAE**: estando,
  a recusa é **<- Genero ja relacionado a outro codigo \***, e a mensagem traz o
  código em que ele já está;
- a **unidade de conversão** tem de estar informada: zerada, a recusa é
  **\* Informe a unidade de conversao \***.

Todas as recusas apontam a linha em que aconteceram, e nada é gravado em nenhuma
delas.

### RN-07 — Na alteração de uma linha, o vínculo tem de existir e a unidade de conversão é obrigatória

Na **alteração**, a linha marcada como alterar exige que o **vínculo** entre o código
de gênero FAE, o código de subclasse e o código de gênero já exista: não existindo, a
recusa é **\* Genero nao cadastrado neste relacionamento \***, com o cursor na linha.
A **unidade de conversão** também tem de estar informada: zerada, a recusa é
**\* Informe a unidade de conversao \***, com o cursor no campo da unidade de
conversão da linha. Nada é gravado nas duas recusas.

### RN-08 — A exclusão de uma linha apaga o vínculo, e exige que ele exista

Na **alteração**, a linha marcada como excluir **apaga o vínculo** entre aquele
gênero e aquele código de gênero FAE. Exige que o vínculo exista: não existindo, a
recusa é **\* Genero nao cadastrado neste relacionamento \***, com o cursor na linha,
e nada é apagado.

A tela **não apaga o gênero nem o código de gênero FAE**: apaga só o vínculo entre os
dois. E a exclusão **não pede a unidade de conversão** — ela não pede valor nenhum,
só a linha marcada.

### RN-09 — A situação da linha decide a operação; linha em branco e situação desconhecida são ignoradas

Cada linha da lista tem uma **situação**, e é ela que diz o que fazer com a linha:
**incluir**, para vincular o gênero ao código; **alterar**, para trocar a unidade de
conversão daquele vínculo; e **excluir**, para desfazer o vínculo.

A situação de incluir vale tanto na inclusão quanto na alteração. Já a **alteração**
e a **exclusão** de uma linha só acontecem quando a tela está em **alteração**: com a
tela em inclusão, todas as linhas com gênero são tratadas como incluir, seja qual for
a situação que trouxerem.

São ignoradas, sem recusa nenhuma e sem gravar nada: a linha **sem código de
subclasse** e a linha cuja situação **não é** incluir, alterar nem excluir.

A tela percorre todas as linhas da mensagem, uma a uma. Uma **recusa interrompe a
mensagem**: as linhas seguintes não chegam às conferências.

[?] Depois de uma recusa, o que impede a gravação é o estado que a rotina comum de
mensagem deixa. Essa rotina não faz parte do acervo lido; se ela não marcar esse
estado, uma linha recusada ainda poderia ser gravada. Pergunta ao site.

### RN-10 — O que a inclusão grava

Passando as conferências, a inclusão **cria o vínculo** com o **código de gênero FAE**
informado, o **código de subclasse** e o **código de gênero** da linha, a **unidade de
medida** informada para o código, a **unidade de conversão** da linha, o **ano**, o
**dia** e o **mês** da sessão, a **matrícula** de quem incluiu e a **marca que diz que
o vínculo está vigente**. Nada mais é gravado nesse registro.

### RN-11 — O que a alteração grava

A **alteração** tem dois efeitos. O primeiro é sobre o código: a **unidade de medida**
informada para o código é regravada nos **vínculos daquele código**, um a um. O
segundo é sobre a linha marcada como alterar: ela troca só a **unidade de conversão**
daquele vínculo.

Nenhum dos dois efeitos repõe a **data de atualização** nem a **matrícula** do
vínculo: elas voltam com o valor que foi lido.

[?] O primeiro efeito percorre os vínculos do código em sequência, e o acervo não
define o efeito das leituras que se posicionam na chave do cadastro — se a leitura
seguinte volta ao mesmo registro ou avança para o próximo. Pela mesma razão, não se
pode afirmar que o percurso termina. Pergunta ao site.

### RN-12 — Toda gravação deixa rastro na auditoria

Cada **inclusão**, cada **alteração** — a do código e a da linha — e cada **exclusão**
grava uma linha no cadastro de auditoria com o **conteúdo anterior** e o **posterior**
do vínculo, a **operação**, a **matrícula** do servidor, a **data e a hora** da
sessão, a **estação**, o **órgão**, a **CRE**, o **cadastro de origem** (o do vínculo)
e o **código de gênero FAE** como número do processo. Na **inclusão** o conteúdo
anterior vai em branco; na **exclusão**, o posterior vai em branco.

A **consulta** não deixa rastro nenhum.

[?] A linha da **exclusão** fica marcada como **alteração**, e não como exclusão: é a
única das quatro gravações desta tela que não usa a operação correspondente ao que
aconteceu. Se era para ficar marcada como exclusão, o acervo lido não diz.

[?] A montagem da auditoria da **inclusão** está sob uma condição de estado que o
acervo não explica; se existe um caminho em que a inclusão passa sem deixar rastro, é
pergunta ao site.

### RN-13 — A permissão de cada operação é conferida antes de gravar

A **inclusão** exige a autorização de inclusão do código de acesso; a **alteração** e
a **exclusão** de uma linha exigem, cada uma, a autorização correspondente. Sem a
autorização, a operação não segue e nada é gravado.

A **consulta** não é comparada com autorização nenhuma: o cadastro de autorizações
guarda também a marca da consulta, e nenhuma passagem desta tela a lê.

[?] Se a consulta deveria exigir a autorização de consulta, o caminho não a exige: a
marca existe no cadastro e não é lida por esta tela.

### RN-14 — A tela não segue quando o controle da tela anterior está preenchido

Quando o **controle da tela anterior** chega preenchido, a tela **não segue**: ela não
confere nada, não mostra a lista e não grava. É a guarda que impede esta tela de
operar por cima de outra que ainda está no meio de uma operação.

[?] A guarda é anterior a todas as conferências desta tela, e o acervo não diz o que
preenche o controle da tela anterior nem o que o servidor vê quando isso acontece. Ou
ele é uma tela em fim de operação, ou é um caminho que não deveria existir. Pergunta
ao site.

### RN-15 — A tela não muda conforme quem a chamou, e não passa nada adiante

O menu que a abre não deixa operação nem código: a tela abre em **consulta**, sem
ficha carregada, e é ela que decide o que fazer com o que o servidor informa. Ela não
consulta de que tela veio.

A tela também **não encaminha** nada: em nenhum caminho ela passa registro ou operação
para outra tela. É o fim da jornada, e o que ela deixa gravado é o que as outras telas
leem.

### RN-16 — Os quatro campos passam pela edição numérica antes de qualquer conferência de negócio

O **código do gênero FAE**, o **código de subclasse**, o **código de gênero** e a
**unidade de conversão** passam por uma conferência numérica **antes** das conferências
de negócio desta tela. O que não for número é recusado no próprio campo, com o cursor
nele, e nada é lido nem gravado por causa disso. O campo em branco chega às
conferências valendo zero, e cada mensagem começa com os campos de resultado da
anterior apagados.

[?] A rotina que faz essa conferência é importada, sem corpo no acervo lido: a
mensagem que o servidor vê na digitação recusada não pôde ser conferida.

## Cenários BDD

```gherkin
Funcionalidade: Manter o vínculo do gênero com o gênero FAE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F020T

  Cenário: RN-01, RN-10 — incluir um vínculo novo
    Dado que a tela está em inclusão
    E informo um código de gênero FAE cadastrado e a unidade de medida dele
    E marco uma linha com um gênero cadastrado que ainda não tem vínculo, com a unidade de conversão
    Quando confirmo
    Então o vínculo entre aquele gênero e aquele código é criado
    E fica com a unidade de medida do código e com a unidade de conversão que informei
    E fica com a minha matrícula e com o ano, o mês e o dia da sessão
    E fica com a marca de vínculo vigente
    E a inclusão deixa uma linha no rastro de auditoria

  Cenário: RN-01 — o código ficou sem nenhum vínculo
    Dado que o código que estava na tela ficou sem nenhum vínculo
    Quando a tela se apresenta de novo
    Então vejo "* Nao existem relacionamentos cadastrados *"
    E a lista fica vazia

  Cenário: RN-02 — a tela abre em consulta
    Dado que chego a esta tela pela opção do menu que a abre
    Então ela abre em consulta
    E não há ficha de código carregada

  Cenário: RN-02 — operação diferente de incluir, alterar e consultar
    Quando informo uma operação que não é incluir, alterar nem consultar
    Então vejo "* Opcao nao disponivel. Use INC, ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é lido nem gravado

  Cenário: RN-03 — código do gênero FAE em branco
    Quando confirmo sem informar o código do gênero FAE
    Então vejo "* Informe o codigo FNDE *"
    E o cursor volta ao campo do código
    E nada é conferido nem gravado

  Cenário: RN-03 — código não cadastrado, na inclusão
    Dado que a tela está em inclusão
    Quando informo um código que não existe no cadastro dos códigos de gênero FAE
    Então vejo "* Codigo FNDE nao cadastrado *"
    E o cursor volta ao campo do código
    E nada é gravado

  Cenário: RN-03 — unidade de medida do código em branco
    Quando confirmo sem informar a unidade de medida do código
    Então vejo "* Informe a unidade de medida do codigo FNDE *"
    E o cursor volta ao campo da unidade de medida
    E nada é gravado

  Cenário: RN-03 — unidade de medida não vinculada ao código
    Quando informo uma unidade de medida que não está vinculada àquele código
    Então vejo "* Unid.medida nao cadastrada para este cod.FNDE *"
    E o cursor volta ao campo da unidade de medida
    E nada é gravado

  Cenário: RN-04 — consultar um código com vínculos
    Dado que informo um código de gênero FAE que tem vínculos
    Quando confirmo a consulta
    Então vejo a lista dos gêneros vinculados, com a unidade de medida de cada gênero e a unidade de conversão
    E nenhum vínculo é criado, alterado ou apagado
    E nenhuma linha nova aparece no rastro de auditoria

  Cenário: RN-04 — código sem vínculo, na consulta
    Quando consulto um código que não tem nenhum vínculo
    Então vejo "* Relacionamentos nao cadastrados *"
    E o cursor volta ao campo do código
    E a lista fica vazia

  Cenário: RN-05 — alterar sem ter consultado antes
    Dado que a tela está em alteração
    Quando informo um código que não foi o consultado na mensagem anterior
    Então vejo "* Consulte antes de atualizar *"
    E o cursor volta ao campo do código
    E nada é gravado

  Cenário: RN-06 — incluir um gênero que não existe no cadastro
    Dado que a tela está em inclusão
    Quando marco uma linha com um gênero que não existe no cadastro dos gêneros
    Então vejo "* Genero nao cadastrado *"
    E o cursor volta à linha
    E nada é gravado

  Cenário: RN-06 — incluir um vínculo que já existe
    Quando marco uma linha com um gênero que já está vinculado àquele código de gênero FAE
    Então vejo "* Genero ja cadastrado neste relacionamento *"
    E o cursor volta à linha
    E nada é gravado

  Cenário: RN-06 — gênero já vinculado a outro código
    Quando marco uma linha com um gênero que já está vinculado a outro código de gênero FAE
    Então vejo "<- Genero ja relacionado a outro codigo *"
    E a mensagem traz o código em que ele já está
    E nada é gravado

  Cenário: RN-06 — incluir sem a unidade de conversão
    Quando marco uma linha com o gênero e deixo a unidade de conversão zerada
    Então vejo "* Informe a unidade de conversao *"
    E o cursor volta ao campo da unidade de conversão da linha
    E nada é gravado

  Cenário: RN-07, RN-11 — alterar a unidade de conversão de uma linha
    Dado que consultei um código e a tela está em alteração
    E marco uma linha com um vínculo existente e uma unidade de conversão nova
    Quando confirmo
    Então a unidade de conversão daquele vínculo é trocada
    E a unidade de medida informada para o código é regravada nos vínculos daquele código
    E a alteração deixa linhas no rastro de auditoria

  Cenário: RN-07 — alterar uma linha cujo gênero não está vinculado
    Quando marco como alterar uma linha cujo gênero não está vinculado àquele código
    Então vejo "* Genero nao cadastrado neste relacionamento *"
    E o cursor volta à linha
    E nada é gravado

  Cenário: RN-07 — alterar uma linha sem a unidade de conversão
    Quando marco como alterar uma linha com vínculo e deixo a unidade de conversão zerada
    Então vejo "* Informe a unidade de conversao *"
    E nada é gravado

  Cenário: RN-08 — excluir um vínculo
    Dado que consultei um código e a tela está em alteração
    Quando marco uma linha com um vínculo existente como excluir
    Então o vínculo entre aquele gênero e aquele código é apagado
    E o gênero e o código de gênero FAE continuam cadastrados
    E a exclusão deixa uma linha no rastro de auditoria

  Cenário: RN-08 — excluir uma linha cujo gênero não está vinculado
    Quando marco como excluir uma linha cujo gênero não está vinculado àquele código
    Então vejo "* Genero nao cadastrado neste relacionamento *"
    E o cursor volta à linha
    E nada é apagado

  Cenário: RN-08 — excluir não pede a unidade de conversão
    Dado que consultei um código e a tela está em alteração
    Quando marco como excluir uma linha com vínculo e deixo a unidade de conversão zerada
    Então o vínculo é apagado

  Cenário: RN-09 — linha sem gênero é ignorada
    Quando confirmo com uma linha sem o código de subclasse
    Então a linha é ignorada, sem mensagem
    E nada é gravado por causa dela

  Cenário: RN-09 — situação desconhecida é ignorada
    Quando marco uma linha com um gênero e uma situação que não é incluir, alterar nem excluir
    Então a linha é ignorada, sem mensagem
    E nada é gravado por causa dela

  Cenário: RN-09 — com a tela em inclusão, a situação não muda a operação
    Dado que a tela está em inclusão
    Quando marco uma linha com um gênero novo e qualquer situação
    Então a linha é tratada como incluir

  Cenário: RN-09 — uma recusa interrompe a mensagem
    Dado que marco duas linhas, a primeira com um dado que a tela recusa
    Quando confirmo
    Então vejo a mensagem da primeira linha
    E as linhas seguintes não chegam às conferências

  Cenário: RN-11 — a alteração não repõe a data nem a matrícula
    Dado que altero a unidade de conversão de um vínculo
    Quando a alteração se conclui
    Então a data de atualização e a matrícula daquele vínculo continuam as que foram lidas

  Cenário: RN-12 — a exclusão fica marcada como alteração no rastro
    Dado que excluo um vínculo
    Quando a exclusão se conclui
    Então a linha do rastro de auditoria fica marcada com a operação de alteração
    E o conteúdo posterior daquela linha vai em branco

  Cenário: RN-12 — a consulta não deixa rastro
    Dado que consulto um código
    Quando a consulta se conclui
    Então nenhuma linha nova aparece no rastro de auditoria

  Cenário: RN-13 — sem a autorização da operação
    Dado que o meu código de acesso não tem a autorização de alteração
    Quando confirmo uma alteração
    Então a operação não segue
    E nada é gravado

  Cenário: RN-14 — controle da tela anterior preenchido
    Dado que o controle da tela anterior está preenchido
    Quando confirmo
    Então a tela não segue
    E nada é conferido, mostrado ou gravado

  Cenário: RN-15 — a tela não encaminha nada
    Dado que concluo uma operação nesta tela
    Então nenhum registro nem operação é passado a outra tela

  Cenário: RN-16 — campo com texto
    Quando informo texto no código do gênero FAE, no código de subclasse, no código de gênero ou na unidade de conversão
    Então o campo é recusado antes de qualquer conferência de negócio
    E o cursor fica no campo recusado
    E nada é lido nem gravado por causa dele
```
