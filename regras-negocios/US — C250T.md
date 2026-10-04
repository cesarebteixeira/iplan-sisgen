# US — C250T — Manter códigos de justificativa do tipo de órgão

## Estória

Como **servidor da Coordenação Regional Escolar (CRE)**, quero **manter a lista dos códigos de
justificativa do meu tipo de órgão — incluir, alterar, excluir e consultar cada código com a sua
descrição**, para que **quem lança uma ocorrência tenha o motivo certo para escolher**.

A justificativa é o motivo com que o sistema registra uma ocorrência, e cada tipo de órgão tem a sua
própria lista: um código de dois dígitos e a descrição que aparece para quem lança. Sem o código
cadastrado, quem lança não tem o que escolher; com a descrição errada, o registro passa a dizer
outro motivo. É esta tela que mantém esse vocabulário — e é a única que escreve nele.

## Contexto

Jornada S000M → C000M → C028M → C029M → C250T.
Ator: servidor de CRE — mantém os códigos de justificativa do tipo de órgão da sua sessão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

A `C250T` é uma tela de transação, não um menu: mantém **uma justificativa por vez**. As telas do
caminho (`C028M` e `C029M`) são menus e só encaminham — não gravam nada. Da sessão esta tela usa o
**tipo de órgão do vínculo** de quem opera, a **descrição desse tipo de órgão**, a **data do
sistema**, a **matrícula**, o **código de acesso**, o **privilégio**, a **CRE** e a **estação**;
essa carga é regra da entrada e está no anexo, em **Regras que se revelaram da entrada**.

Esta tela sai para a **relação das justificativas (`C250C`)** — a tela de consulta que lista os
códigos do tipo de órgão da sessão — e reabre em cima de um registro pelos cinco comandos de leitura
(RN-12). O que ela entrega à relação, e a saída pelo campo da tela informada, estão na RN-13.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — O cadastro que esta tela mantém

Esta tela mantém o **cadastro das justificativas de um tipo de órgão**. Cada registro tem **quatro
campos**: o **código da justificativa** (dois dígitos), a **descrição** (40 caracteres, de
preenchimento obrigatório), o **tipo de órgão** (dois dígitos) e a **marca da última operação** feita
nele.

O código **não se repete dentro do mesmo tipo de órgão**: a chave do cadastro é o par tipo de órgão
+ código, e é única. O cadastro é dimensionado para **100 registros** — capacidade (máximo esperado,
parâmetro de dimensionamento), não volume cadastrado.

O código da justificativa é o que as telas do mapa de atendimento usam para indicar o motivo de uma
ocorrência. Dos programas do lote, **11 leem** este cadastro — a relação das justificativas e dez
telas de mapa — e **só esta tela o escreve**.

### RN-02 — O tipo de órgão vem da sessão, e não se digita

O tipo de órgão é o do **vínculo da minha matrícula** escolhido na entrada, e é ele que identifica o
acervo de justificativas que eu vejo e onde o registro é gravado. Não há campo para informá-lo: a
tela o toma da sessão na passagem de validação, a cada transmissão. Sem tipo de órgão na sessão, a
chave do registro fica pela metade e a tela trabalha com zeros.

### RN-03 — A descrição do tipo de órgão e a data do sistema no cabeçalho

O cabeçalho mostra a **descrição do tipo de órgão da sessão** e a **data do sistema**, e o código do
tipo de órgão não aparece na tela — só a sua descrição. A descrição e a data — junto com o próprio
tipo de órgão — são **apagadas a cada resposta** e repostas com os valores da sessão na passagem de
gravação; nas respostas de recusa e nos comandos que trazem um registro, elas voltam em branco.

### RN-04 — O campo da operação: incluir, alterar, excluir, consultar e purgar

O campo da operação é o único campo de escolha da tela. Ele aceita as cinco operações que o sistema
conhece — **incluir**, **alterar**, **excluir**, **consultar** e **purgar** —, escritas como o
sistema as nomeia, e o que for digitado em minúsculas é convertido para maiúsculas antes da
conferência.

Um valor que o sistema não conhece é recusado pela conferência padrão dele, que nomeia o conjunto
aceito, e nada é gravado. A operação em branco é recusada pela conferência própria da tela, com o
rótulo do campo e a mensagem do catálogo do sistema.

[?] A operação é comparada com os códigos do catálogo de mensagens do sistema, que são carregados no
idioma da sessão por uma biblioteca do ambiente: o que se lê no acervo são os valores iniciais do
fonte. Se o que o servidor digita chega à conferência como digitado ou já traduzido, pergunta ao
site.

### RN-05 — Incluir e alterar exigem o código e a descrição

Na **inclusão** e na **alteração**, a tela exige, nesta ordem, sempre com o cursor de volta ao campo
recusado:

- o **código da justificativa** — **\* Informe o codigo da justificativa \***;
- a **descrição** — **\* Informe a descricao \***.

A **exclusão**, a **consulta** e a **purga** não conferem nenhum dos dois. Além dessas, a conferência
final da tela recusa a inclusão com o código zerado e o tipo de órgão zerado, com aviso do catálogo
do sistema.

[?] A exigência do código aparece **duas vezes** no caminho: na conferência de campo, que recusa e
encerra a transação, e na conferência final, que só seria alcançada se a primeira não tivesse
recusado. Não se lê no acervo se a segunda chega a ser executada — ou ela é um resto, ou a primeira
não encerra a transação. Pergunta ao site.

### RN-06 — O código da justificativa passa pela conferência numérica

O código da justificativa é conferido como **número** antes de qualquer uso, em toda resposta e
também nos comandos que trazem um registro — **exceto** nos dois de ponta (o primeiro e o último,
RN-12). O campo em branco é tratado como zero e os zeros à esquerda são descartados; o que não for
número é recusado no próprio campo, com o cursor de volta nele, e nada é gravado.

### RN-07 — Incluir recusa código já cadastrado; as outras operações exigem que ele exista

Antes de gravar, a tela lê o registro pela chave — o **tipo de órgão da sessão** e o **código
informado**.

- **Na inclusão**, achando um registro com aquela chave, a gravação é recusada:
  **\* ITEM ALREADY EXISTS \***. Não achando, a inclusão segue.
- **Na alteração, na exclusão e na consulta**, não achando o registro, a operação é recusada:
  **\* ITEM NOT FOUND \***.

Nas duas recusas o cursor volta ao campo do código, e nada é gravado.

### RN-08 — O tipo de órgão é conferido no cadastro das secretarias

Antes de gravar, a tela lê o **tipo de órgão** no cadastro das secretarias. Achando-o marcado como
excluído, a operação é avisada com **"Key deleted"** e o cursor volta.

[?] Não achando o tipo de órgão, a recusa só está escrita para a alteração, a exclusão e a consulta
(RN-07); para a **inclusão** o acervo não mostra recusa nenhuma — o registro da justificativa segue
com o tipo de órgão da sessão, mesmo que ele não esteja no cadastro das secretarias. Se é
intencional, pergunta ao site.

### RN-09 — Um registro marcado como excluído é avisado

Excluir **não apaga** a justificativa: o sistema regrava o registro com a **marca da última
operação** de exclusão, e o registro continua no cadastro — é essa marca, e não a ausência do
registro, que diz que ele está excluído.

Trazendo de novo para a tela um registro já marcado como excluído, o aviso é **"Key deleted"**:

- **na consulta**, o aviso sai e **não** impede a exibição da ficha;
- **na exclusão**, o aviso sai e nada é regravado;
- **na alteração**, o aviso **não** sai: é a alteração que devolve a justificativa ao uso;
- **na inclusão**, o registro marcado é tratado como já existente (RN-07).

[?] O que separa o aviso da gravação é a marca de falha que a rotina de mensagem do ambiente deixa, e
essa rotina não está no lote. Se ela não marcar, o que foi avisado ainda assim é gravado. Pergunta
ao site — a mesma dúvida vale para todas as recusas desta tela.

### RN-10 — A consulta mostra a ficha e não grava nada

Na **consulta**, a tela reabre em cima do registro lido, com o código e a descrição dele no
formulário: nenhuma justificativa é incluída, alterada ou apagada e **nenhuma linha de auditoria é
gerada**. A consulta também não confere o código e a descrição exigidos pela inclusão (RN-05).

[?] A rotina de gravação tem uma recusa própria para a consulta ("not available with this format "),
mas o caminho da consulta encerra a transação antes de chamá-la: pelo acervo, o servidor não vê esse
aviso — ele vê a ficha. Se a recusa vale para outro caminho, pergunta ao site.

### RN-11 — A exclusão marca; a exclusão definitiva não é alcançada

A **exclusão** regrava o registro com a marca da exclusão (RN-09) e deixa na auditoria o conteúdo
anterior, com o posterior em branco.

A **purga** tem, no caminho, uma guarda que a recusa — **"PUR not allowed"** — e, depois dela, o
único ramo do programa que **apaga fisicamente** o registro. A guarda recusaria exatamente a operação
de que o ramo que apaga depende.

[?] A guarda e o ramo não fecham, e **por este caminho a exclusão definitiva é inalcançável**: se a
guarda encerra a transação, o ramo que apaga nunca roda; se não encerra, o aviso é dado e o registro
é apagado assim mesmo. Não se escolhe um dos dois lados. Pergunta ao site.

### RN-12 — Os cinco comandos que trazem um registro para a tela

O campo da operação aceita, além das cinco operações, **cinco comandos que trazem um registro** para
a tela, e ela **reabre em cima dele**, sem passar por menu: o registro do **código informado**, o
**seguinte**, o **anterior**, o **primeiro** e o **último**. O que for digitado em minúsculas é
convertido para maiúsculas antes da conferência.

Nos dois comandos de ponta — o primeiro e o último — o código não é conferido como número; nos
outros três, é (RN-06). Trazendo um registro marcado como excluído, o aviso é **"Key deleted"**
(RN-09). Nenhum dos cinco comandos grava: eles só leem e reapresentam, e a tela volta com o campo de
indicação limpo.

### RN-13 — As duas saídas: a relação das justificativas e a tela informada

A tela tem duas saídas.

A primeira é a **relação das justificativas (`C250C`)** — a tela de consulta que lista os códigos do
tipo de órgão da sessão. Preenchido o **campo de indicação** com algo diferente de branco e de
**N**, a tela não segue com a manutenção: ela entrega a sessão à relação, que abre na **consulta**
sobre os códigos do tipo de órgão da sessão. Nessa passagem não vai nenhum dado do formulário e nada
é gravado.

A segunda é o **campo com o código de uma tela**: preenchido, a transação é desviada para aquela tela
**antes de qualquer conferência** — nem os dados da justificativa nem a permissão da operação são
conferidos nesse caso.

[?] O rótulo do campo de indicação e o do campo da tela não estão no acervo: a máscara da tela é
carregada em tempo de execução e não veio no lote. O que o servidor vê nesses dois campos, e quem os
preenche, pergunta ao site.

### RN-14 — A tela abre para incluir, e não muda conforme quem a chamou

Ao se apresentar, a tela **escreve a operação como inclusão** e mostra o formulário em branco, com a
descrição do tipo de órgão e a data vindas da sessão.

Esta tela **não compara a tela de origem com código nenhum**: ela abre sempre na inclusão, venha do
menu ou de onde vier. O código da tela que a chamou, quando chega preenchido, não escolhe o modo —
ele desvia a transação para aquela tela (RN-13).

### RN-15 — A operação só segue com a permissão da tela e da operação

Na abertura, o sistema confere se a tela consta do **cadastro de telas** — não constando, o aviso é
**\* Tela nao disponivel \*** — e confere a **estação** contra a da sessão: estando a sessão aberta
em outra estação, o acesso é encerrado e a tela não abre.

A cada transmissão, o sistema confere a **rota** — a operação pedida tem de estar entre as que a
tela admite, senão o aviso é **\* Operacao nao disponivel \*** — e, para a operação pedida, a
**autorização daquela operação** no código de acesso da sessão:

- sem o registro da tela para aquele código de acesso, a recusa é
  **\* Acesso negado para esta matricula \***;
- com o registro, mas sem aquela operação liberada, a recusa é
  **\* Acesso negado para esta operacao \***.

Nas recusas nada é lido nem gravado.

### RN-16 — Toda manutenção deixa rastro na auditoria

A **inclusão**, a **alteração** e a **exclusão** gravam, no cadastro de auditoria, **uma linha por
operação**, com a operação, o cadastro tocado, a tela `C250T`, a matrícula de quem operou, a estação,
a CRE, o tipo de órgão, o número do processo e a data e a hora da sessão, mais o **conteúdo anterior
e o posterior** do registro — o tipo de órgão, o código e a descrição, em 47 bytes de um campo de
300.

Na **inclusão** a tela preenche só o conteúdo novo; na **alteração** preenche o anterior — o que
estava gravado — e o novo; na **exclusão** preenche o anterior e deixa o novo em branco. A
**consulta** e os cinco comandos que trazem registro **não** geram auditoria.

[?] O conteúdo auditado começa por um campo de três posições que a tela **nunca** preenche — só o
limpa quando a sessão abre. O que deveria ir nessas três posições, e o que o auditor lê nelas, o
acervo não mostra. Pergunta ao site.

### RN-17 — A recusa de destino inválido não é alcançável pela C250T

O ramo que produz a recusa de **destino inválido** (a distribuição automática entre destinos) só roda
quando o modo de distribuição automática está preenchido; a C250T limpa esse campo imediatamente
antes dos **três** únicos pontos em que ele poderia disparar. Pela C250T, portanto, essa recusa
**não** é apresentada.

---

## Cenários BDD

```gherkin
Funcionalidade: Manutenção dos códigos de justificativa do tipo de órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C250T

  Cenário: RN-01 — a inclusão grava a justificativa
    Dado que a tela abriu na inclusão, com o formulário em branco
    Quando informo o código 7 e a descrição "Feriado municipal" e confirmo
    Então a justificativa passa a constar do cadastro do meu tipo de órgão
    E nenhuma outra justificativa é alterada

  Cenário: RN-01 — o código não se repete dentro do tipo de órgão
    Dado que a justificativa 7 já existe para o meu tipo de órgão
    Quando consulto a lista do meu tipo de órgão
    Então o código 7 aparece uma única vez

  Cenário: RN-02 — o tipo de órgão do registro é o da minha sessão
    Dado que estou na tela com o vínculo da minha matrícula
    Quando gravo uma justificativa
    Então ela vale para o acervo do tipo de órgão da minha sessão
    E não há campo na tela para eu informar outro tipo de órgão

  Cenário: RN-03 — o cabeçalho mostra a descrição do tipo de órgão e a data do sistema
    Dado que abri a tela C250T
    Então o cabeçalho mostra a descrição do tipo de órgão da minha sessão
    E mostra a data do sistema
    E não mostra o código do tipo de órgão

  Cenário: RN-04 — operação que o sistema não conhece
    Quando informo no campo da operação um valor que o sistema não conhece
    Então o sistema recusa a operação, nomeando o conjunto que ele aceita
    E nada é gravado

  Cenário: RN-04 — operação em branco
    Quando deixo o campo da operação em branco e confirmo
    Então vejo o aviso do catálogo do sistema para o campo da operação
    E nada é gravado

  Cenário: RN-05 — inclusão sem o código da justificativa
    Dado que a operação é a de inclusão
    Quando confirmo sem informar o código
    Então vejo "* Informe o codigo da justificativa *"
    E o cursor volta ao campo do código
    E nada é gravado

  Cenário: RN-05 — inclusão sem a descrição
    Dado que a operação é a de inclusão
    E informei o código
    Quando confirmo sem a descrição
    Então vejo "* Informe a descricao *"
    E o cursor volta ao campo da descrição
    E nada é gravado

  Cenário: RN-06 — código da justificativa com texto
    Quando informo texto no campo do código
    Então o campo é recusado antes de qualquer uso
    E o cursor volta ao campo
    E nada é gravado

  Cenário: RN-07 — inclusão de código já cadastrado
    Dado que já existe uma justificativa com o código informado para o meu tipo de órgão
    Quando confirmo a inclusão
    Então vejo "* ITEM ALREADY EXISTS *"
    E o cursor volta ao campo do código
    E a justificativa existente não é alterada

  Cenário: RN-07 — alteração, exclusão ou consulta de código não cadastrado
    Quando confirmo a alteração, a exclusão ou a consulta de um código que não existe
    Então vejo "* ITEM NOT FOUND *"
    E o cursor volta ao campo do código
    E nada é gravado

  Cenário: RN-08 — o tipo de órgão da sessão está excluído
    Dado que o tipo de órgão da minha sessão está marcado como excluído
    Quando confirmo a operação
    Então vejo o aviso "Key deleted"
    E o cursor volta
    E nada é gravado

  Cenário: RN-09 — a exclusão marca o registro
    Dado que a justificativa está cadastrada e sem uso
    E a operação é a de exclusão
    Quando confirmo a exclusão
    Então a justificativa fica marcada como excluída
    E continua no cadastro

  Cenário: RN-09 — trazer de novo uma justificativa excluída
    Dado que a justificativa informada está marcada como excluída
    Quando confirmo a consulta
    Então vejo o aviso "Key deleted"
    E a ficha é mostrada mesmo assim

  Cenário: RN-09 — a alteração devolve ao uso uma justificativa excluída
    Dado que a justificativa informada está marcada como excluída
    E corrijo a descrição e confirmo a alteração
    Então a justificativa volta a constar como em uso
    E nenhum aviso de exclusão é apresentado

  Cenário: RN-10 — a consulta mostra a ficha e não grava nada
    Dado que a justificativa informada está cadastrada e em uso
    Quando confirmo a consulta
    Então a tela reabre mostrando o código e a descrição daquela justificativa
    E nenhuma justificativa é incluída, alterada ou apagada
    E nenhuma linha de auditoria é gerada

  Cenário: RN-11 — a exclusão confirmada marca a justificativa
    Dado que a justificativa está cadastrada
    E a operação é a de exclusão
    Quando confirmo a exclusão
    Então a justificativa fica marcada como excluída
    E a auditoria registra a exclusão
    E o registro continua no cadastro

  Cenário: RN-11 — a exclusão definitiva é recusada
    Dado que a operação é a de purga
    Quando confirmo a purga
    Então vejo o aviso "PUR not allowed"
    E nada é apagado
    E o ramo que apaga o registro não é alcançado

  Cenário: RN-12 — trazer um registro para a tela
    Dado que a operação é um dos comandos que trazem registro
    Quando confirmo o comando informando o código
    Então a tela reabre em cima daquele registro
    E o campo de indicação volta limpo
    E nada é gravado

  Cenário: RN-12 — o primeiro e o último registro do cadastro
    Dado que informo o comando que traz o primeiro registro ou o que traz o último
    Quando confirmo o comando
    Então a tela reabre no primeiro ou no último registro do meu tipo de órgão
    E o código informado não é conferido como número
    E nada é gravado

  Cenário: RN-12 — trazer um registro marcado como excluído
    Dado que a justificativa do código informado está marcada como excluída
    Quando confirmo um dos comandos que trazem registro
    Então vejo o aviso "Key deleted"
    E nada é gravado

  Cenário: RN-13 — a tela passa a sessão para a relação das justificativas
    Dado que preenchi o campo de indicação com algo diferente de branco e de N
    Quando confirmo
    Então a relação das justificativas se abre, listando os códigos do meu tipo de órgão
    E nada é gravado por essa passagem

  Cenário: RN-13 — o campo da tela de destino desvia a transação
    Dado que preenchi o campo com o código de uma tela de destino
    Quando confirmo
    Então sou levado àquela tela
    E os dados da justificativa e a permissão da operação não são conferidos
    E nada é gravado

  Cenário: RN-14 — abrir a tela prepara a inclusão
    Quando abro a tela C250T pela opção do menu
    Então a operação é a de inclusão
    E o formulário está em branco
    E nada é gravado

  Cenário: RN-14 — a tela não muda conforme quem a chamou
    Dado que cheguei à C250T por qualquer caminho
    Quando a tela se apresenta
    Então ela abre na inclusão, e não em consulta
    E o código da tela que me chamou não escolhe o modo — ele desvia a transação

  Cenário: RN-15 — sem permissão para a operação
    Dado que o meu código de acesso tem a tela C250T sem aquela operação liberada
    Quando transmito a operação
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-15 — sem o registro da tela no meu código de acesso
    Dado que o meu código de acesso não tem a tela C250T
    Quando tento operar
    Então vejo "* Acesso negado para esta matricula *"
    E nada é gravado

  Cenário: RN-15 — a tela fora do cadastro de telas
    Dado que a tela C250T não consta do cadastro de telas
    Quando tento abrir a tela
    Então vejo "* Tela nao disponivel *"
    E não consigo operar

  Cenário: RN-15 — a operação não admitida pela tela
    Dado que a operação informada não está entre as que a tela admite
    Quando transmito
    Então vejo "* Operacao nao disponivel *"
    E nada é gravado

  Cenário: RN-15 — a sessão está aberta em outra estação
    Dado que a sessão da minha matrícula está registrada em outra estação
    Quando abro a tela C250T
    Então o acesso é encerrado
    E a tela não abre

  Cenário: RN-16 — toda manutenção deixa rastro na auditoria
    Dado que confirmei uma inclusão, uma alteração ou uma exclusão na C250T
    Quando a gravação termina
    Então existe uma linha de auditoria da justificativa
    E com a operação, o cadastro tocado, a tela C250T e o conteúdo anterior e o posterior
    E com a matrícula, a CRE, o tipo de órgão, a estação, o processo e a data e a hora

  Cenário: RN-16 — a consulta e os comandos não geram auditoria
    Dado que confirmei uma consulta ou um dos comandos que trazem registro
    Então nenhuma linha de auditoria é criada

  Cenário: RN-17 — a tela não apresenta a recusa de destino inválido
    Dado que confirmei uma inclusão na C250T
    Quando a gravação é preparada
    Então a tela limpa o modo de distribuição automática
    E a recusa de destino inválido não é apresentada
```
