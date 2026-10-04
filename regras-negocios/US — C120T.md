# US — C120T — Manter o cadastro das secretarias

## Estória

Como **servidor de CRE com a tela de manutenção das secretarias autorizada**, quero **manter o
cadastro das secretarias — incluir uma secretaria nova, corrigir os dados de uma que já existe e
tirar de circulação a que não tem mais órgão**, para que **cada secretaria fique identificada no
sistema com o seu código, a sua sigla, o seu código no município e os seus processos, e o resto do
sistema encontre a secretaria certa**.

A secretaria é a dona dos outros cadastros: é por ela que os órgãos, os materiais, as licitações e a
sessão de cada servidor são separados. Os dados que esta manutenção guarda — o código no município e
os códigos de processo — são o que liga a secretaria aos registros do município; errados, quem
consulta a secretaria trabalha com a identificação de outra. E uma secretaria que sai de circulação
sem que o cadastro saiba disso deixa os órgãos e os vínculos dos servidores apontando para uma
secretaria que não deveria mais existir. É esta manutenção que mantém esse cadastro em dia.

## Contexto

Jornada S000M → C000M → C015M → C120T.
Ator: servidor de CRE — mantém o cadastro das secretarias que o resto do sistema usa.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio. Os menus do caminho não gravam nada: só encaminham.

A `C120T` é uma tela de transação, não um menu: ela mantém **uma secretaria por vez**, e termina
nela mesma ou na tela seguinte. Ela encadeia com a **relação das secretarias (`C120C`)** nos dois
sentidos e sem passar por menu: marcada uma secretaria na relação, a relação entrega a sessão a esta
tela com a secretaria escolhida e a operação de consulta (RN-02); e esta tela devolve a sessão à
relação quando o campo de indicação é preenchido (RN-15). Da sessão ela usa o **tipo de órgão do
vínculo** de quem opera, a sua **sigla**, a **data do sistema** e, na transmissão, a **matrícula**, o
**código de acesso**, o **privilégio** e a **CRE** — essa carga é regra da entrada e está no anexo,
em **Regras que se revelaram da entrada**.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O cadastro das secretarias e quem escreve nele

O cadastro das secretarias é a lista das secretarias do município tal como o sistema as conhece.
Cada secretaria tem um **código de duas posições** — que a identifica e não se repete —, uma
**sigla**, um **nome**, um **código no município**, **até cinco outros códigos no município**, os
**dois pedaços do código do processo RIO**, **um número de processo**, a marca de **se o número de
processo usa o grupo**, a marca de **se ela está ativa** e a marca da **última operação** feita nela.
No dicionário da base são **catorze** campos, e a **sigla é o único de preenchimento obrigatório**;
a cópia que as telas carregam traz **quinze**. O cadastro é dimensionado para **200 secretarias**, e
a chave é o código.

Esta tela é a única que escreve nesse cadastro: dos programas do lote, **83** contêm leitura dele e
**nenhum outro** contém a gravação.

[?] O dicionário da base declara **catorze** campos e a cópia que as telas carregam traz **quinze**:
o campo a mais é um número de processo de seis dígitos, que esta tela confere como número e grava, e
que não existe no dicionário. Ou o dicionário está defasado, ou o campo pertence a outro cadastro.
Pergunta ao site.

### RN-02 — A tela abre para incluir pelo menu e para consultar quando vem da relação

Chegando **pela opção do menu**, a tela abre na **inclusão**, com o formulário em branco e o
**código da secretaria já preenchido com o tipo de órgão da sessão** — a secretaria do vínculo de
quem está operando.

Chegando **da relação das secretarias**, com uma secretaria marcada, a tela abre na **consulta**
sobre ela: os campos vêm preenchidos com a ficha guardada daquela secretaria.

Quem decide é a **tela de origem**, deixada na área de trabalho da sessão pelo programa que chamou:
esta tela compara essa origem com o código da relação e, sendo ela, troca a operação por consulta e
carrega a ficha do registro escolhido; a marca da origem é consumida em seguida, para não valer na
abertura seguinte. Sem essa marca, a operação fica a de inclusão.

### RN-03 — A tela só trabalha em incluir, alterar, excluir ou consultar

O campo da operação é o único campo de escolha da tela, e aceita as quatro operações que a própria
tela anuncia quando recusa: **INC** (incluir), **ALT** (alterar), **EXC** (excluir) e **CON**
(consultar). O que for digitado em minúsculas é convertido para maiúsculas antes da conferência.
Qualquer outro valor é recusado com
**\* Opcao nao disponivel. Use INC, ALT, EXC ou CON \***, com o cursor de volta no campo da operação,
e nada é gravado. A operação em branco é recusada pela conferência própria da tela, com o rótulo do
campo e a mensagem do catálogo do sistema.

[?] A tela compara a operação com os quatro códigos de operação do catálogo de mensagens do sistema
— carregados no idioma da sessão —, e a mensagem que ela escreve nomeia as mesmas quatro
abreviaturas. O catálogo não veio no lote: o que se pode ler é a mensagem da tela. Se o que o
servidor digita chega à conferência como digitado ou já traduzido pelo formulário, pergunta ao site.

[?] Toda recusa desta tela sai por um aviso ao usuário e a transação para ali; o que separa o aviso
da gravação é a marca de falha que a rotina de mensagem do ambiente deixa, e essa rotina não está no
lote. Se ela não marcar, o que foi recusado ainda assim é gravado. Pergunta ao site — a mesma dúvida
vale para as recusas de campo (RN-05) e para as do cadastro (RN-07).

### RN-04 — Os campos de número passam pela conferência numérica antes de qualquer uso

**Oito campos** são conferidos como número antes de qualquer uso: o **código da secretaria**, o
**código no município**, os **cinco códigos alternativos no município** e o **número de processo de
seis dígitos**. O que não for número é recusado no próprio campo, com o cursor de volta nele, e a
operação não segue. O campo em branco é tratado como zero, e os zeros à esquerda são descartados.

### RN-05 — A inclusão e a alteração exigem os dados da secretaria

Na **inclusão** e na **alteração**, a tela exige, nesta ordem, sempre com o cursor de volta no campo
recusado:

- o **código da secretaria** — **\* Informe o codigo da Secretaria \***;
- a **sigla** — **\* Informe a sigla da Secretaria \***;
- o **código no município** — **\* Informe o codigo no municipio \***;
- o **nome** — **\* Informe o nome da Secretaria \***;
- a marca de **se o número de processo usa o grupo**, com **S** ou **N** —
  **\* Inf. se o nr.processo usa o grupo com S o N \***;
- os **dois pedaços do código do processo RIO**, preenchidos —
  **\* Inf. codigo do PROCESSO RIO \***;
- a marca de **ativa ou não**, com **S** ou **N** —
  **\* Informe se ativo ou nao com S ou N \***.

A **exclusão** e a **consulta** não conferem nenhum desses campos. Além dessas recusas, a
conferência final da tela recusa a inclusão com o código da secretaria zerado, com o aviso do
catálogo do sistema.

### RN-06 — O código no município não pode repetir um dos códigos alternativos

Informado o **código no município** e estando ele igual a **qualquer um dos cinco códigos
alternativos** da mesma secretaria, a inclusão ou a alteração é recusada com
**\* Codigo no municipio ja cadastrado \***, com o cursor de volta no campo do código no município,
e nada é gravado.

[?] A conferência compara só o código principal com os cinco alternativos, e só dentro da mesma
secretaria: os alternativos não são comparados entre si nem com os de outras secretarias, e nada
impede que duas secretarias tenham o mesmo código no município. Se o código no município é a
identificação da secretaria no município (RN-01), a unicidade não é garantida. Pergunta ao site.

### RN-07 — Incluir exige que a secretaria ainda não exista; alterar e excluir, que exista

Antes de gravar, a tela lê o cadastro pelo código informado. **Na inclusão**, achando uma secretaria
com aquele código, a gravação é recusada; **na alteração e na exclusão**, não achando, a gravação é
recusada. As duas recusas são do sistema — o aviso é montado pelo caminho de mensagem do ambiente —,
com o cursor de volta no campo do código. A alteração e a exclusão leem o registro guardado antes de
regravá-lo; a inclusão tenta criar o registro novo.

[?] Se essas recusas interrompem a gravação: o aviso sai pelo caminho do ambiente e o que o separa
da gravação é a marca de falha que a rotina de mensagem deixa — a mesma dúvida de RN-03. Pergunta ao
site.

### RN-08 — A consulta mostra a ficha e não grava nada

Na consulta, a tela lê a secretaria pelo código informado e traz a ficha para o formulário; não
achando, avisa **\* Secretaria nao cadastrada \***, com o cursor de volta no campo da operação, e não
grava. Achando, ela **reabre em cima daquele registro** e o único efeito é a exibição: nenhuma
secretaria é incluída, alterada ou apagada, nenhum vínculo de servidor é criado e nenhuma linha de
auditoria é gerada. A consulta também não confere os campos exigidos pela inclusão (RN-05).

[?] Quando a consulta chega pela relação das secretarias com um código que não existe no cadastro, a
tela não tem mensagem própria: ela monta o formulário vazio e marca o estado de registro não
encontrado. O que o servidor vê nesse caso não está no acervo. Pergunta ao site.

### RN-09 — A exclusão é recusada quando a secretaria tem órgãos cadastrados

Antes de excluir, a tela percorre o cadastro de órgãos pela secretaria informada; achando **qualquer
órgão** daquela secretaria, a exclusão é recusada com
**\* Nao exclua. Orgaos cad. nesta secretaria \***, com o cursor de volta no campo da operação, e
nada é apagado nem marcado. Como a chave do cadastro de órgãos começa pela secretaria, a conferência
vai direto aos órgãos dela — não é uma varredura de todos os órgãos.

### RN-10 — Excluir não apaga o registro, e um registro excluído é avisado

Excluir **não apaga** a secretaria: o sistema regrava o registro com a marca da **última operação**
de exclusão, e a secretaria continua no cadastro — é essa marca, e não a ausência do registro, que
diz que ela está excluída (a relação das secretarias, por exemplo, não a esconde).

Um registro já marcado como excluído que seja trazido de novo para a tela **avisa "Key deleted"**,
texto do catálogo de mensagens do sistema. Na **consulta** o aviso sai e **não** impede a exibição
da ficha; na **exclusão** a regravação é recusada; e a **alteração** é o único caminho que devolve a
secretaria ao uso — ela não recebe esse aviso e regrava o registro.

### RN-11 — A exclusão definitiva não é oferecida

A tela não oferece apagar a secretaria de vez: informada a operação de expurgo, ela é recusada como
opção indisponível, junto com as demais operações que a tela não aceita (RN-03). O programa tem,
além disso, uma guarda que recusa o expurgo com **"PUR not allowed"**, do catálogo de mensagens, e um
caminho que apaga fisicamente o registro.

[?] A guarda e o ramo não fecham, e **por este caminho a exclusão definitiva é inalcançável**: a
tela recusa o expurgo antes de qualquer conferência — o campo da operação só admite as quatro
operações — e a guarda de "PUR not allowed" recusaria exatamente a operação de que o ramo que apaga
depende. Ou o ramo é morto, ou o expurgo entra por outro caminho que o acervo não mostra. Pergunta
ao site — não se escolhe um dos dois lados.

### RN-12 — Incluir uma secretaria cria os vínculos de acesso dela

Ao incluir, além do registro da secretaria, o sistema cria o **vínculo de cada servidor do código de
acesso fixo 99 com a nova secretaria**, na tabela que liga o servidor à secretaria (o código de
acesso, a matrícula e a nova secretaria; a CRE e o órgão filho vão zerados). São criados **até 100
vínculos** numa inclusão, e cada vínculo criado rende uma linha de auditoria própria (RN-13). A
alteração e a exclusão não mexem nesses vínculos.

[?] O que o **código de acesso 99** significa no negócio. Ele não é escolhido por quem opera: está
gravado no programa e é o mesmo em toda inclusão. O dicionário de dados não o documenta. Pergunta ao
site.

### RN-13 — Toda manutenção deixa rastro na auditoria

A inclusão, a alteração e a exclusão gravam, no cadastro de auditoria (`A010T`), **uma linha por
operação**, com a operação, o cadastro tocado, a tela `C120T`, a matrícula de quem operou, a estação,
a CRE, o tipo de órgão, o número do processo da sessão, a data e a hora, e o **conteúdo anterior e o
posterior** do registro. Na **inclusão** a tela preenche só o conteúdo novo; na **alteração**
preenche o anterior — o que estava gravado — e o novo; na **exclusão** preenche o anterior e deixa o
novo em branco. A inclusão grava ainda uma linha de auditoria para **cada vínculo** criado (RN-12).
A consulta não gera auditoria.

### RN-14 — Os cinco comandos que trazem um registro para a tela

O campo da operação aceita cinco comandos que **trazem um registro** para a tela, e a tela **reabre
em cima dele**, sem passar por menu: **REC** (o registro do código informado), **NEX** (o seguinte),
**BAC** (o anterior), **FIR** (o primeiro) e **LAS** (o último). O que for digitado em minúsculas é
convertido para maiúsculas antes da conferência. Nos dois comandos de ponta — o primeiro e o último —
o código da tela não é conferido como número; nos outros três, sim. Trazendo um registro marcado
como excluído, o aviso é **"Key deleted"** (RN-10). Nenhum dos cinco comandos grava: eles só leem e
reapresentam.

### RN-15 — As saídas da tela: a relação e a tela de destino

A tela tem duas saídas. A primeira é a **relação das secretarias (`C120C`)**: preenchido o campo de
indicação com algo diferente de branco e de **N**, a tela não segue com a manutenção — ela entrega a
sessão à relação, que abre na **consulta** e na posição que ficou guardada da exibição anterior, e
essa passagem não grava nada. A segunda é o **campo com o código de uma tela de destino**:
preenchido, a transação é desviada para aquela tela **antes de qualquer conferência** — nem os dados
da secretaria nem a permissão da operação são conferidos nesse caso.

[?] O rótulo do campo de indicação e o do campo da tela de destino não estão no acervo: a máscara é
carregada em tempo de execução e não veio no lote. O que o servidor vê nesses dois campos, e quem os
preenche, pergunta ao site.

### RN-16 — A operação só segue com a permissão da tela e da operação

Na abertura, o sistema confere se a tela consta do **cadastro de telas** — não constando, o aviso é
**\* Tela nao disponivel \*** — e se o **código de acesso** de quem opera tem a tela — não tendo, a
recusa é **\* Acesso negado para esta matricula \***; confere ainda a **estação** contra a da sessão,
e estando a sessão aberta em outra estação o acesso é encerrado e a tela não abre.

A cada transmissão, o sistema confere a **rota** — tendo a tela sido retirada do cadastro de telas, o
aviso é **\* Tela nao cadastrada \*** — e, para a operação pedida, a **autorização daquela operação**
no mesmo código de acesso — não tendo, a recusa é **\* Acesso negado para esta operacao \***. Nas
recusas nada é gravado.

### RN-17 — Os campos de contexto somem a cada mensagem

A **descrição do tipo de órgão da sessão**, a **data do sistema** e a **marca de ativa ou não**, que
a abertura mostra, são apagadas a cada mensagem respondida e não são repostas: a resposta sai com os
três campos em branco.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe um caminho de
entrada em que os campos não são limpos, não foi possível determinar. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter o cadastro das secretarias

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C120T

  Cenário: RN-01 — a ficha mostra os dados que o cadastro guarda
    Dado que a secretaria informada está cadastrada
    Quando abro a sua ficha
    Então vejo o código, a sigla, o nome, o código no município e os códigos alternativos, os dois pedaços do código de processo RIO, o número de processo e as marcas de uso do grupo e de ativa
    E nada é gravado

  Cenário: RN-02 — abrir pelo menu prepara a inclusão com o código da sessão
    Quando abro a tela C120T pela opção do menu
    Então a operação é a de inclusão
    E o formulário está em branco, com o código preenchido com o tipo de órgão da minha sessão
    E nada é gravado

  Cenário: RN-02 — abrir pela relação das secretarias mostra a ficha em consulta
    Dado que marquei uma secretaria na relação das secretarias
    Quando a tela C120T se abre
    Então a operação é a de consulta
    E vejo os dados daquela secretaria
    E nada é gravado

  Cenário: RN-03 — operação que a tela não aceita
    Quando informo uma operação diferente de incluir, alterar, excluir e consultar
    Então vejo a mensagem "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: RN-04 — campo de número com texto
    Quando informo texto em um dos campos de número
    Então o campo é recusado antes de qualquer uso
    E o cursor volta ao campo
    E nada é gravado

  Cenário: RN-05 — inclusão de uma secretaria
    Dado que a operação é a de inclusão
    E informo o código, a sigla, o código no município, o nome, a marca de uso do grupo no processo, os dois códigos de processo RIO e a marca de ativa
    Quando transmito a inclusão
    Então a secretaria passa a constar do cadastro
    E a auditoria registra a inclusão

  Cenário: RN-05 — inclusão sem o código da secretaria
    Quando transmito a inclusão sem o código
    Então vejo a mensagem "* Informe o codigo da Secretaria *"
    E o cursor volta ao campo do código
    E nada é gravado

  Cenário: RN-05 — inclusão sem a sigla
    Quando transmito a inclusão sem a sigla
    Então vejo a mensagem "* Informe a sigla da Secretaria *"
    E o cursor volta ao campo da sigla
    E nada é gravado

  Cenário: RN-05 — inclusão sem o código no município
    Quando transmito a inclusão sem o código no município
    Então vejo a mensagem "* Informe o codigo no municipio *"
    E o cursor volta ao campo do código no município
    E nada é gravado

  Cenário: RN-05 — inclusão sem o nome
    Quando transmito a inclusão sem o nome da secretaria
    Então vejo a mensagem "* Informe o nome da Secretaria *"
    E o cursor volta ao campo do nome
    E nada é gravado

  Cenário: RN-05 — marca de uso do grupo no processo diferente de S e de N
    Quando transmito a inclusão com essa marca diferente de S e de N
    Então vejo a mensagem "* Inf. se o nr.processo usa o grupo com S o N *"
    E o cursor volta ao campo da marca
    E nada é gravado

  Cenário: RN-05 — código do processo RIO incompleto
    Quando transmito a inclusão sem um dos dois pedaços do código do processo RIO
    Então vejo a mensagem "* Inf. codigo do PROCESSO RIO *"
    E o cursor volta ao campo do processo
    E nada é gravado

  Cenário: RN-05 — marca de ativa diferente de S e de N
    Quando transmito a inclusão com a marca de ativa diferente de S e de N
    Então vejo a mensagem "* Informe se ativo ou nao com S ou N *"
    E o cursor volta ao campo da marca
    E nada é gravado

  Cenário: RN-06 — código no município repetido entre os alternativos
    Dado que a secretaria tem um código alternativo no município
    Quando transmito a inclusão informando esse mesmo código como o principal
    Então vejo a mensagem "* Codigo no municipio ja cadastrado *"
    E o cursor volta ao campo do código no município
    E nada é gravado

  Cenário: RN-07 — inclusão de secretaria que já está cadastrada
    Dado que já existe uma secretaria com o código informado
    Quando transmito a inclusão
    Então o sistema recusa a gravação, avisando que o registro já existe
    E o cursor volta ao campo do código
    E nada é gravado

  Cenário: RN-07 — alteração ou exclusão de secretaria que não está cadastrada
    Quando transmito a alteração ou a exclusão de um código que não está cadastrado
    Então o sistema recusa a gravação, avisando que o registro não foi encontrado
    E o cursor volta ao campo do código
    E nada é gravado

  Cenário: RN-08 — a consulta mostra a ficha e não grava nada
    Dado que a secretaria informada está cadastrada
    Quando transmito a consulta
    Então a tela reabre mostrando os dados daquela secretaria
    E nenhuma secretaria é incluída, alterada ou apagada
    E nenhum vínculo de servidor é criado
    E nenhuma linha de auditoria é gerada

  Cenário: RN-08 — consulta de secretaria que não está cadastrada
    Quando transmito a consulta de um código que não está cadastrado
    Então vejo a mensagem "* Secretaria nao cadastrada *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: RN-09 — exclusão de uma secretaria sem órgãos
    Dado que a secretaria informada não tem nenhum órgão cadastrado
    E a operação é a de exclusão
    Quando transmito a exclusão
    Então a secretaria fica marcada como excluída
    E a auditoria registra a exclusão

  Cenário: RN-09 — exclusão recusada porque a secretaria tem órgãos
    Dado que a secretaria informada tem órgão cadastrado
    E a operação é a de exclusão
    Quando transmito a exclusão
    Então vejo a mensagem "* Nao exclua. Orgaos cad. nesta secretaria *"
    E o cursor volta ao campo da operação
    E a secretaria continua cadastrada e não marcada

  Cenário: RN-10 — trazer uma secretaria já excluída
    Dado que a secretaria informada está marcada como excluída
    Quando transmito a consulta ou a exclusão
    Então vejo o aviso "Key deleted"
    E, na consulta, a ficha é mostrada mesmo assim
    E, na exclusão, nada é gravado

  Cenário: RN-10 — a alteração devolve ao uso uma secretaria excluída
    Dado que a secretaria informada está marcada como excluída
    E corrijo os seus dados e transmito a alteração
    Então a secretaria volta a constar como em uso
    E a auditoria registra a alteração

  Cenário: RN-11 — a exclusão definitiva não é oferecida
    Quando informo a operação de expurgo
    Então vejo a mensagem "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E o cursor volta ao campo da operação
    E nada é gravado nem apagado

  Cenário: RN-12 — inclusão cria os vínculos de acesso
    Dado que existem servidores com o código de acesso 99
    Quando transmito a inclusão de uma secretaria
    Então cada um desses servidores fica vinculado à nova secretaria
    E cada vínculo criado é registrado na auditoria

  Cenário: RN-14 — trazer um registro para a tela
    Dado que a operação é um dos comandos que trazem registro
    Quando transmito o comando informando o código
    Então a tela reabre em cima daquele registro
    E nada é gravado

  Cenário: RN-14 — o primeiro e o último registro do cadastro
    Dado que informo o comando que traz o primeiro registro ou o que traz o último
    Quando transmito o comando
    Então a tela reabre no primeiro ou no último registro do cadastro
    E o código informado não é conferido como número
    E nada é gravado

  Cenário: RN-15 — a tela passa a sessão para a relação das secretarias
    Dado que preenchi o campo de indicação com algo diferente de branco e de N
    Quando transmito
    Então a relação das secretarias se abre
    E nada é gravado por essa passagem

  Cenário: RN-15 — o campo da tela de destino desvia a transação
    Dado que preenchi o campo com o código de uma tela de destino
    Quando transmito
    Então sou levado àquela tela
    E os dados da secretaria e a permissão da operação não são conferidos
    E nada é gravado

  Cenário: RN-16 — sem permissão para a operação
    Dado que o meu código de acesso tem a tela C120T sem aquela operação liberada
    Quando transmito a operação
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-16 — sem permissão para a tela
    Dado que o meu código de acesso não tem a tela C120T
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: RN-16 — tela fora do cadastro de telas
    Dado que a tela C120T não consta do cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: RN-16 — tela retirada do cadastro de telas
    Dado que a tela C120T foi retirada do cadastro de telas
    Quando transmito uma operação
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é gravado

  Cenário: RN-17 — a resposta volta com os campos de contexto em branco
    Dado que a tela abriu mostrando a descrição do tipo de órgão da sessão, a data do sistema e a marca de ativa
    Quando respondo uma mensagem
    Então a resposta vem com esses três campos em branco
```
