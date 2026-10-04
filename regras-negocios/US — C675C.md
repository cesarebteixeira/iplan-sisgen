# US — C675C — Manter permissões de tipo de contrato da CRE

## Estória

Como **servidor de CRE**, quero **consultar, órgão por órgão, as permissões de tipo
de contrato da minha coordenadoria regional — com o período, a subclasse e o gênero
de cada uma — e tirar as que não valem mais**, para que **a secretaria saiba quais
órgãos e fornecedores estão autorizados a contratar por aquele tipo de contrato, e
dentro de que período**.

A permissão de tipo de contrato é o que autoriza um órgão da rede a contratar por
uma modalidade, para um gênero e uma subclasse, dentro de um período. Quem confere
o que a rede pode contratar precisa ver isso órgão a órgão: a autorização é
registrada por órgão, e é o conjunto delas que diz o alcance da permissão. Esta
tela é a que mostra esse conjunto e a que tira dele o que não vale mais.

## Contexto

Jornada S000M → C000M → C050M → C670M → C675C.

Ator: servidor de CRE — consulta as permissões de tipo de contrato da sua
coordenadoria regional, órgão por órgão, e tira as que não valem mais.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os três passos anteriores — o `C000M`, o `C050M` e o `C670M` — são menus e **não
gravam nada**: só encaminham. O contexto que a C675C usa — o tipo de órgão, a
coordenadoria e a matrícula do servidor — é o que a entrada deixou na sessão, e a
tela não o recalcula.

A tela também **encadeia** para a tela de detalhe (`C675T`) sem passar por menu: o
que ela entrega nessa passagem é regra dela (RN-13).

As regras abaixo são só as da tela desta jornada. As regras da entrada que
apareceram nesta leitura estão no anexo de evidências, na seção **Regras que se
revelaram da entrada**.

---

## Regras de negócio

### RN-01 — A tela abre em consulta e só aceita consulta e alteração

A tela trabalha com uma operação, e só duas são aceitas: **consulta** e
**alteração**. Quando a operação chega em branco, a tela adota a consulta. Qualquer
outra operação é recusada com **\* Operacao nao disponivel. Use ALT ou CON \***, com
o cursor de volta ao campo da operação — e a recusa acontece **antes de qualquer
leitura**: nesse caminho nenhuma permissão é lida nem mostrada.

[?] A operação com que a tela abre vem de quem a chamou, e a C675C é aberta por um
menu, que não tem operação de manutenção. O acervo não mostra qual valor chega
nessa passagem; e a recusa só é alcançável se a máscara oferecer ao operador o
campo da operação — o texto da máscara não está no lote. Pergunta ao site.

[?] Antes dessa guarda, a lógica de rota já recusa as operações que não reconhece,
com uma mensagem parecida (**\* Operacao nao disponivel \***), e ela roda primeiro.
Qual das duas mensagens o operador vê em cada caso depende de valores do formulário
que não estão no acervo. Pergunta ao site.

### RN-02 — A permissão é do grupo, para um tipo de contrato, e vale por órgão

O cadastro por trás da tela guarda **uma permissão por combinação**: o tipo de
órgão, a coordenadoria (o grupo), a **data limite**, a subclasse, o gênero, o
**órgão** e o **tipo de contrato**. São **13 campos** no registro — entre eles o
início do período, a data limite, o fornecedor, o órgão e o tipo de contrato — e a
capacidade do cadastro é de **100 registros** (capacidade é o máximo esperado,
parâmetro de dimensionamento, não o que está gravado). O **início do período não
faz parte da identidade** da permissão: quem distingue uma permissão da outra é a
data limite. Toda leitura da tela é feita dentro do **tipo de órgão da sessão**.

A inclusão da permissão não é feita aqui: quem inclui é a tela de detalhe
(`C675T`). A C675C só apaga.

[?] O que a subclasse e o gênero classificam, e o que a **descrição resumida do
gênero** — que a tela mostra — representa, não está no acervo lido nem no manual.
Pergunta ao site.

### RN-03 — O grupo é obrigatório, tem de existir e é o do próprio servidor

O grupo (a coordenadoria) é a chave de entrada da tela. Vindo em branco, a tela
recusa com **\* Informe o grupo \***, com o cursor no campo. Informado, ele é
procurado no cadastro de grupos **dentro do tipo de órgão da sessão**: não
existindo — ou estando marcado como excluído —, a recusa é
**\* Grupo nao cadastrado \***. E quando a sessão tem um grupo, o servidor só
consulta **o próprio**: informar outro grupo dá
**\* Usuario sem acesso a este grupo \***.

[?] Se a sessão não tem grupo (o vínculo do servidor não fixou nenhum), o fonte
deixa passar qualquer grupo cadastrado. Se essa é a intenção — ou se o vínculo
deveria sempre trazer um grupo —, o acervo não responde. Pergunta ao site.

### RN-04 — A consulta é pela combinação do grupo com o tipo de contrato, a data limite, a subclasse e o gênero

Confirmado o grupo, o operador informa o **tipo de contrato**, a **data limite**
(dia, mês e ano), a **subclasse** e o **gênero**; a tela procura a permissão
registrada para essa combinação, dentro do tipo de órgão da sessão. **O início do
período não é procurado: ele vem do registro** — é o que a tela mostra depois de
achar, junto com a descrição resumida do gênero. Não achando nenhuma permissão para
a combinação, a recusa é **\* Permissao sem Orgaos identificados \***, com o cursor
na data limite; e se o grupo informado não tem **nenhuma** permissão registrada, o
aviso é **\* Orgaos nao identificados \***.

Reenviar os mesmos valores que já estão na tela não provoca nova leitura.

[?] A leitura usa o recurso de posicionamento do dicionário de dados, cujo efeito
exato não está no acervo nem no manual: se ela exige a **data limite exata** de uma
permissão registrada, o operador só consulta quem sabe a data; se apenas
**posiciona** na primeira permissão igual ou posterior, a data informada é o ponto
de partida da lista. O site precisa dizer qual é o esperado.

### RN-05 — A alteração exige que os dados sejam os mesmos da consulta

Em alteração, a tela confere **sete valores** — o grupo, o tipo de contrato, as
três partes da data limite, a subclasse e o gênero — contra os que ela guardou da
consulta. Se algum estiver diferente, a alteração é recusada com
**\* Consulte antes de atualizar \***, com o cursor no campo da operação: primeiro
se consulta, depois se altera.

[?] A conferência **não inclui o início do período**: quando ele é informado e não
bate com o registrado, a tela não recusa — ela o substitui pelo que está no
registro. Se o início do período deveria ser conferido, o caminho não o confere.
Pergunta ao site.

### RN-06 — Em alteração, a permissão do órgão marcado na linha é apagada

Cada linha da lista — um órgão — tem um campo de marcação. Estando a marcação com
**"E"**, o órgão daquela linha tem a **permissão apagada**: a tela lê a permissão
daquele órgão, monta o rastro de auditoria e exclui o registro. Em **consulta**, a
marcação não faz nada: nada é apagado.

[?] O campo de marcação não é preenchido por nenhum caminho do programa: ele só é
lido da máscara e devolvido a ela. Se a máscara não oferecer esse campo por linha,
a exclusão por linha fica inalcançável. Pergunta ao site.

### RN-07 — O flag de total apaga a permissão do grupo inteiro, e exige que ela exista

Há ainda um campo de total. Marcado, o alvo não é um órgão da lista, e sim a
permissão **do grupo** — a que não aponta para um órgão. Em alteração, a tela
primeiro verifica se essa permissão existe: não existindo, recusa com
**\* Nao existem registros para exclusao \***, com o cursor no campo do total;
existindo, apaga o registro do grupo, também depois de gravar o rastro.

[?] Como o campo da linha, o flag de total só é lido da máscara e devolvido a ela:
o programa nunca o preenche. Se a máscara não o oferecer, esse caminho de exclusão
fica inalcançável. Pergunta ao site.

[?] A recusa da operação de exclusão convive com um caminho que apaga: a mensagem
manda usar ALT ou CON, e é justamente **fora da consulta** que a exclusão acontece
— o caminho que apaga começa por "se a operação não é consulta", e a operação
recusada também não é consulta. Quem manda excluir e marca a linha com "E" (ou
marca o total) recebe a recusa e, ainda assim, a permissão é apagada. Ou a guarda
de operação vale para outro caso, ou o caminho de exclusão ficou sem guarda.
Pergunta ao site.

### RN-08 — Toda exclusão grava antes o rastro de auditoria

Antes de apagar, a tela grava um **rastro** no cadastro de auditoria: a tela de
origem, o cadastro auditado (o das permissões), a operação de exclusão, a matrícula
funcional, a estação, a data e a hora da sessão, o valor anterior do registro e o
valor resultante (em branco, porque o registro sai). Só depois de o rastro ser
gravado é que a permissão é apagada: se a gravação do rastro aborta, o caminho é
abandonado antes da exclusão.

[?] O número de processo do rastro recebe o código do órgão da permissão — um
código de 8 dígitos no campo que o cadastro destina a número de processo. O que
esse número significa ali não está no acervo lido. Pergunta ao site.

### RN-09 — A lista traz o órgão, o fornecedor e a razão social, em até 12 linhas

A lista da tela tem **12 linhas**, e cada linha traz o **órgão** (código e nome,
do cadastro de órgãos) e o **fornecedor** (código e razão social, do cadastro de
fornecedores) da permissão daquele órgão. Órgãos marcados como excluídos no
cadastro não aparecem: a tela passa para o próximo. Havendo mais permissões do que
linhas, a lista continua a partir do último órgão mostrado.

[?] O cadastro de órgãos marca a situação do registro num campo de manutenção, e o
fonte pula os marcados com "D". O que "D" significa (excluído? desativado?) e o que
o operador vê na linha de uma permissão cujo órgão foi pulado não está no acervo
nem no manual. Pergunta ao site.

[?] A continuação da lista depende de uma marca de continuidade que os próprios
caminhos da tela reescrevem, e o efeito exato da leitura posicionada não está no
manual. Se a página seguinte pode repetir ou pular órgãos, o acervo não responde.
Pergunta ao site.

### RN-10 — Antes de mostrar, o sistema confere o acesso

A abertura da tela passa pelas conferências de acesso, com o contexto da sessão —
matrícula, código de acesso, privilégio, tipo de órgão e coordenadoria. A tela
precisa estar cadastrada no cadastro de telas: não estando, a recusa é
**\* Tela nao disponivel \*** ou **\* Tela nao cadastrada \***. A matrícula precisa
ter a tela autorizada no seu código de acesso: não tendo, a recusa é
**\* Acesso negado para esta matricula \***. E a operação também é conferida contra
essa autorização: sem o flag correspondente, a recusa é
**\* Acesso negado para esta operacao \***. O contexto da sessão não é recalculado
aqui: é o que a entrada deixou.

[?] A conferência da operação procura os flags de inclusão, de alteração e de
exclusão, mas **não** o de consulta: quem tem a tela autorizada consulta sem
precisar do flag de consulta. E como a exclusão da permissão corre pela operação de
alteração, quem tem a alteração liberada apaga mesmo sem a exclusão liberada. Se a
intenção era exigir o flag de consulta e o de exclusão, os caminhos não os exigem.
Pergunta ao site.

### RN-11 — Cada apresentação começa com os campos de resultado limpos

Antes de conferir a digitação e de ler qualquer permissão, a tela apaga **sete
campos** de resultado: a descrição do tipo de órgão, a data do sistema, a descrição
resumida do gênero, o nome do órgão, o código do fornecedor, a razão social e o
órgão inicial. Uma consulta recusada, portanto, não deixa na tela o resultado da
consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se
existe um caminho de entrada em que os campos não são limpos, não foi possível
determinar. Pergunta ao site.

### RN-12 — A digitação de doze campos é editada, e o cursor volta ao campo recusado

**Doze campos** passam pela edição numérica antes de qualquer leitura: o grupo, o
tipo de contrato, o dia, o mês e o ano do início do período, o dia, o mês e o ano
limite, a subclasse, o gênero, o órgão da linha e o órgão inicial. Campo em branco
é tratado como zero, e o que não for número é recusado. Quando o campo recusado tem
posição na tela — **oito dos doze** —, o cursor volta para ele.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual —
não está nos fontes desta jornada: a rotina que faz a edição numérica não faz parte
do acervo lido. Pergunta ao site.

### RN-13 — A tela entrega à tela de detalhe o grupo e a operação de consulta

Marcado o campo que pede o detalhamento, a tela **encadeia** para a tela de detalhe
(`C675T`) sem passar por menu: ela se identifica como origem, deixa registrado que
a operação é **consulta** e leva o grupo consultado. Quem chega ao detalhamento por
esse caminho, portanto, não altera nada lá: a tela de detalhe abre em consulta. A
tela também respeita o campo genérico de "próxima tela" da máscara: informado um
código de tela, o encaminhamento é para ele, e a lógica da própria tela termina
ali.

[?] Os campos que decidem esse encadeamento — o que pede o detalhamento e o de
próxima tela — não são preenchidos por nenhum caminho do programa: vêm da máscara.
Quem os preenche, e o que exatamente o encadeamento transporta de uma tela para a
outra além do que esta tela prepara, não está no acervo lido. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar e excluir as permissões de tipo de contrato de uma coordenadoria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C675C

  Cenário: Consulta das permissões do grupo
    Dado que informo a minha coordenadoria, o tipo de contrato, a data limite, a subclasse e o gênero
    Quando envio a consulta
    Então vejo as permissões em linhas, cada uma com o órgão, o fornecedor e a razão social
    E vejo o período, a subclasse e o gênero da permissão consultada

  Cenário: A lista mostra no máximo 12 órgãos
    Dado que a permissão consultada alcança mais de 12 órgãos
    Quando a lista é montada
    Então ela mostra no máximo 12 linhas
    E a lista continua a partir do último órgão mostrado

  Cenário: Órgão excluído não aparece na lista
    Dado que uma permissão aponta para um órgão marcado como excluído no cadastro
    Quando a lista é montada
    Então a tela passa para o próximo órgão

  Cenário: Operação diferente de consulta e de alteração
    Quando informo uma operação que não é consulta nem alteração
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo da operação
    E nenhuma permissão é lida ou mostrada

  Cenário: O grupo é obrigatório
    Quando deixo a coordenadoria em branco
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta para o campo da coordenadoria

  Cenário: Coordenadoria não cadastrada
    Quando informo uma coordenadoria que não existe
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta para o campo da coordenadoria

  Cenário: Coordenadoria de outro servidor
    Dado que a minha sessão tem uma coordenadoria
    Quando informo outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"

  Cenário: A combinação informada não tem permissão
    Dado que informo um tipo de contrato, uma data limite, uma subclasse e um gênero sem permissão registrada
    Quando envio a consulta
    Então vejo a mensagem "* Permissao sem Orgaos identificados *"
    E o cursor volta para o campo da data limite

  Cenário: A coordenadoria não tem nenhuma permissão
    Dado que a coordenadoria informada não tem nenhuma permissão registrada
    Quando envio a consulta
    Então vejo a mensagem "* Orgaos nao identificados *"
    E nenhuma linha é preenchida

  Cenário: Alteração sem consultar antes
    Dado que estou alterando e mexi num dos dados de identificação da permissão
    Quando envio a alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta para o campo da operação

  Cenário: Marcar a linha com "E" apaga a permissão daquele órgão
    Dado que estou alterando e há uma permissão para o órgão da linha
    Quando marco a linha com "E" e envio
    Então a permissão daquele órgão é apagada
    E o rastro de auditoria da exclusão é gravado antes

  Cenário: Marcar a linha em consulta não apaga nada
    Dado que estou consultando
    Quando marco uma linha com "E" e envio
    Então nada é apagado
    E a linha continua na lista

  Cenário: O flag de total apaga a permissão do grupo
    Dado que estou alterando e existe a permissão do grupo para a combinação informada
    Quando marco o flag de total e envio
    Então a permissão do grupo é apagada
    E o rastro de auditoria da exclusão é gravado antes

  Cenário: Flag de total sem permissão do grupo
    Dado que estou alterando e não existe permissão do grupo para a combinação informada
    Quando marco o flag de total e envio
    Então vejo a mensagem "* Nao existem registros para exclusao *"
    E o cursor volta para o campo do total
    E nada é apagado

  Cenário: A consulta não grava nada
    Dado que estou consultando uma permissão
    Quando a lista é montada
    Então nenhuma permissão é incluída, alterada ou apagada
    E nenhum rastro de auditoria é gerado

  Cenário: Digitação não numérica é recusada
    Quando informo um valor não numérico num dos campos de código ou de data
    Então a tela recusa antes de ler a permissão
    E o cursor volta para o campo recusado

  Cenário: Os resultados da consulta anterior são limpos
    Dado que uma consulta anterior deixou nome de órgão e razão social na tela
    Quando a tela é apresentada de novo
    Então os campos de resultado são apagados antes da nova leitura

  Cenário: Acesso negado à tela
    Dado que a minha matrícula não tem a tela autorizada
    Quando abro a tela C675C
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E a tela não lê nenhuma permissão

  Cenário: Operação não liberada
    Dado que a minha matrícula tem a tela, mas não tem a alteração liberada
    Quando envio uma alteração
    Então vejo a mensagem "* Acesso negado para esta operacao *"

  Cenário: Do detalhamento para a tela de detalhe
    Dado que a permissão consultada está na tela
    Quando marco o campo que pede o detalhamento e envio
    Então chego à tela de detalhe C675T
    E ela abre em consulta, com a minha coordenadoria

  Cenário: A próxima tela informada na máscara
    Dado que a máscara traz um código de tela no campo de próxima tela
    Quando envio
    Então sou encaminhado para a tela informada
    E a lógica da C675C termina ali
```
