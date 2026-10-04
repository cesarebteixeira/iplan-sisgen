# US — C112T — Manter os grupos de atendimento de cada refeição

## Estória

Como **servidor de CRE**, quero **declarar, para cada refeição do tipo de órgão da
minha secretaria, em quais grupos de atendimento ela é oferecida**, para que **a
oferta de alimentação fique registrada no nível do grupo de atendimento, e não só
do segmento inteiro**.

A refeição e o segmento de atendimento são mantidos em outros cadastros; o grupo de
atendimento também. O que não existe em lugar nenhum é a **ligação** entre os três,
e é essa ligação que esta tela registra e desfaz. Sem ela, a oferta da refeição
fica declarada para o segmento todo — não há como dizer quais grupos, dentro do
segmento, recebem aquela refeição.

## Contexto

Jornada S000M → C000M → C028M → C029M → C112T.
Ator: servidor de CRE — declara, para a refeição do tipo de órgão da sua secretaria,
os grupos de atendimento que a recebem.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da **tela desta jornada**. O que ela consome da entrada
(o tipo de órgão, o acesso e a CRE da sessão) está no anexo de evidências, na seção
*Regras que se revelaram da entrada*.

Esta é a última tela da jornada: ela **não encadeia** em outra tela sem menu — o que
ela deixa é a ligação gravada e o seu rastro de auditoria.

---

## Regras de negócio

### RN-01 — A tela identifica-se por dois códigos: o da refeição e o do segmento de atendimento

A tela nomeia dois códigos: a **refeição** e o **segmento de atendimento**, ambos
numéricos de dois dígitos. O que não for número é recusado antes de qualquer
consulta, e a recusa aponta o campo. Cada linha da grade traz ainda um terceiro
código, o do **grupo de atendimento**, também de dois dígitos.

[?] O grupo de atendimento é o único dos três códigos sem rótulo de negócio no
programa. O que o servidor lê nessa coluna não pôde ser demonstrado pela fonte.
Pergunta ao site.

### RN-02 — A grade tem 13 linhas, e cada linha traz o segmento, o grupo de atendimento e a ação

Cada linha tem **3 campos**: o código do segmento de atendimento (2 dígitos), o
código do grupo de atendimento (2 dígitos) e a **ação** (1 caractere). O segmento e
o grupo aparecem com as suas descrições. A grade mostra **13 linhas** por vez. Fora
da grade, o cabeçalho tem **9 itens**: a tela, a origem, o número da transação, a
data de entrada, o mês de referência, a opção de manutenção, a tela anterior, a
refeição e o indicador de passagem — contei item a item o leiaute de entrada: 9 no
cabeçalho e 3 em cada uma das 13 linhas.

### RN-03 — O tipo de órgão da sessão é o escopo de tudo o que a tela lê e grava

O tipo de órgão — o da secretaria escolhida na entrada — não se digita aqui: ele
entra na tela pela conferência de sessão e é a primeira parte da chave de tudo o
que a tela lê e grava — a refeição, a ligação, o catálogo de grupos de atendimento
e o cadastro de segmentos. O cabeçalho mostra a descrição do tipo de órgão e a data
do sistema, ambas vindas da sessão.

### RN-04 — A refeição é de outro cadastro; esta tela não a cria nem a altera

A refeição, com a sua descrição, é mantida para o tipo de órgão inteiro na tela
**C101T**. Esta tela só **lê** o cadastro de refeições: daqui não sai inclusão,
alteração nem exclusão de refeição. Sem refeição cadastrada no tipo de órgão não há
onde pendurar os grupos de atendimento.

### RN-05 — Abrindo, a tela mostra a primeira refeição do tipo de órgão, em consulta

Sem opção de manutenção na sessão, a tela abre em **consulta**. Sem refeição em
foco, ela se posiciona na **primeira refeição** do tipo de órgão e passa a
mostrá-la. Se o tipo de órgão não tem refeição nenhuma, a tela abre vazia e **sem
mensagem**: não há aviso de que falta refeição.

### RN-06 — Só se altera ou se consulta

A opção de manutenção aceita apenas **alteração** e **consulta**; inclusão e
exclusão da ligação não se fazem por aqui. Qualquer outra opção é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no campo da opção.

[?] A tela recusa a opção comparando-a com o mnemônico da língua instalada do
sistema, e a mensagem manda usar `ALT` e `CON`. Se o mnemônico da língua instalada
não for esse, a recusa e a mensagem não combinam — a tabela da língua instalada não
está no acervo. Pergunta ao site.

### RN-07 — Alterar exige que a refeição seja a que a tela está mostrando

Para alterar, a refeição informada tem de ser a mesma que a tela já estava
mostrando — a que veio da consulta. Informar outra é recusa: **\* Consulte antes de
atualizar \***. É essa amarração que dispensa a alteração de reconferir o cadastro
da refeição. Na prática, para mexer em outra refeição é preciso consultá-la antes.

### RN-08 — Consultar exige a refeição informada, e ela tem de existir

Na consulta a refeição é obrigatória: em branco, a recusa é **\* Informe a refeicao
\***. Se a refeição informada não é a que a tela já mostrava, ela é procurada no
cadastro do tipo de órgão: não existindo, a recusa é **\* Refeicao nao cadastrada
\***; existindo, a tela passa a mostrar a lista daquela refeição. Sendo a mesma que
já estava em tela, o cadastro não é relido.

### RN-09 — A lista traz os grupos de atendimento já ligados à refeição, com as descrições dos cadastros

A lista percorre as ligações da refeição em foco, uma por linha, na ordem da chave
— segmento de atendimento e, dentro dele, grupo de atendimento —, e completa cada
linha com a descrição do grupo (do catálogo do tipo de órgão) e a descrição do
segmento (do cadastro de segmentos). Quando a refeição não tem **nenhuma** ligação,
a tela avisa **\* Refeicao sem grupos de atend.cadastrados \***.

### RN-10 — A ação é por linha: I inclui, E exclui; o resto não faz nada

A ação é da linha, não da tela: `I` inclui a ligação e `E` exclui a ligação — não há
ação de alteração nesta tela. Linha sem grupo de atendimento é ignorada, e ação
diferente de `I` e de `E` também, silenciosamente: nenhuma mensagem e nenhuma
gravação.

### RN-11 — Incluir exige o grupo de atendimento cadastrado, e o segmento vem do cadastro do grupo

Na inclusão, o grupo de atendimento da linha é procurado no catálogo de grupos do
tipo de órgão. Não achando, a recusa é **\* Grupo de atendimento nao cadastrado \***.
Achando, o **segmento de atendimento da linha é substituído pelo segmento daquele
grupo**: o que o servidor digita na coluna do segmento não manda na inclusão. O
catálogo não admite o mesmo código de grupo duas vezes no tipo de órgão, de modo que
cada grupo pertence a um único segmento.

[?] Na inclusão o segmento digitado é substituído pelo do grupo, mas na exclusão é o
digitado que vale. Se a coluna do segmento é só informativa na inclusão, ou se o
servidor deveria poder apontar outro segmento, a fonte não diz. Pergunta ao site.

### RN-12 — Incluir não pode repetir uma ligação que já existe

Antes de incluir, e já com o segmento resolvido pelo catálogo, a tela procura a
ligação da refeição com aquele segmento e aquele grupo. Existindo, a recusa é
**\* Grupo de atendimento ja cadastrado \***.

[?] A recusa é mostrada e o processamento da linha para ali, mas a fonte não
demonstra que essa parada impeça a gravação: o trecho que grava não consulta a marca
de recusa que a linha deixou, e a rotina que despacha a mensagem não está no acervo.
Se ela não marcar a transação como falha, uma linha recusada pode ainda ser gravada.
Pergunta ao site.

### RN-13 — Excluir exige a ligação existente, com o segmento informado na linha

Na exclusão, a tela procura a ligação com a refeição, o segmento **informado na
linha** e o grupo. Não achando — inclusive quando o segmento digitado não é o do
grupo —, a recusa é **\* Grupo de atendimento nao cadastrado \***. Aqui o catálogo de
grupos não é consultado.

### RN-14 — Consultar não grava nada

Na consulta a tela apenas exibe: a passagem que grava é desviada de propósito quando
a opção não é alteração. Nenhuma ligação é incluída ou excluída.

### RN-15 — A tela grava a ligação e o rastro de auditoria, e só

Das **6 tabelas** que a tela enxerga, o gerador declara **12 rotinas** de gravação e
exclusão; a tela executa **3**: inclui a ligação, exclui a ligação e grava o rastro
de auditoria. As demais — o cadastro de refeições, o catálogo de grupos, o cadastro
de segmentos e o cadastro das telas — são apenas lidas, e as rotinas de exclusão da
auditoria e as demais rotinas declaradas nunca são chamadas. Declarar não é executar.

[?] O dicionário da base marca o indicador de creche da ligação como obrigatório, e
esta tela nunca o informa. O que o banco grava nesse campo, e o que ele significa
para o atendimento em creche, não está no acervo. Pergunta ao site.

### RN-16 — Toda gravação deixa rastro na auditoria

Cada inclusão e cada exclusão monta um registro na trilha de auditoria **A010T**, com
o cadastro que originou a operação, a operação (inclusão ou exclusão), a refeição
como número de processo, a matrícula, a estação, a data e a hora do sistema e os
valores antes e depois. Na inclusão o valor anterior vai em branco e o novo é a
ligação gravada; na exclusão o valor anterior é a ligação lida e o novo vai em
branco. A auditoria da exclusão é montada **antes** da exclusão; a da inclusão,
**depois** da gravação.

### RN-17 — O indicador de passagem leva à refeição seguinte e, nessa passagem, nada é mantido

Com o indicador de passagem preenchido, a tela lê a refeição seguinte à informada e,
não achando, volta à primeira do tipo de órgão; nessa passagem a lista não é mantida
— não se inclui nem se exclui ligação nenhuma. O programa só lê esse indicador; ele
nunca o escreve.

[?] O indicador de passagem é lido em três pontos da tela e nunca é escrito por ela.
Se ninguém o preencher — o terminal ou a lógica global —, a passagem para a refeição
seguinte é inalcançável. Pergunta ao site.

### RN-18 — A tela devolve o controle à tela de origem, e o modo não depende de quem a chamou

Quando o campo da tela anterior vem preenchido, a tela é encaminhada de volta àquela
tela e não faz mais nada — nem conferência, nem gravação. O modo de operação
(consultar ou alterar) **não** vem de quem chamou a tela: vem da opção de manutenção
da sessão, que a tela assume; sem opção, a tela abre em consulta.

[?] O programa desta tela nunca preenche o campo da tela anterior, e a fonte não
mostra quem o preenche. Se ele chegar preenchido pelo terminal no caminho desta
jornada, a tela não faz nada. Pergunta ao site.

### RN-19 — Nada é exibido nem gravado sem a conferência de sessão, de rota e de permissão por operação

A exibição chama a conferência de sessão e de acesso à tela; a manutenção chama a
rota e a permissão por operação. A permissão é conferida **de novo por linha**, com
a operação da linha: a inclusão exige a permissão de inclusão e a exclusão, a de
exclusão; a consulta não exige permissão de operação. Qualquer resultado diferente
do esperado encerra a tela, e a falta de permissão aparece como acesso negado para a
operação.

### RN-20 — Falha de banco interrompe a operação e avisa

Todo acesso a dados testa o retorno do banco: o erro de leitura vira uma ação de erro
e o de gravação, outra, ambas despachadas pela rotina de comunicação — a transação
para ali, sem completar o resto. Não encontrar registro não é erro: é desfecho de
conferência.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os grupos de atendimento de cada refeição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C112T

  Cenário: RN-01, RN-02, RN-05 e RN-14 — abrir a tela e consultar a refeição que ela já mostra
    Dado que o tipo de órgão do meu vínculo tem refeições cadastradas
    Quando abro a tela C112T
    Então ela abre em consulta, na primeira refeição do tipo de órgão
    E em cada uma das 13 linhas vejo o segmento de atendimento, o grupo de atendimento e as suas descrições
    E vejo os grupos de atendimento já ligados àquela refeição
    E nada é gravado

  Cenário: RN-03 — o escopo do tipo de órgão da minha secretaria
    Dado que entrei com a secretaria em que atuo
    Quando consulto uma refeição na tela C112T
    Então só vejo refeições, grupos de atendimento e segmentos do tipo de órgão daquela secretaria
    E o cabeçalho mostra a descrição do tipo de órgão e a data do sistema

  Cenário: RN-04 — a refeição não se cria nem se altera por esta tela
    Dado que estou na tela C112T
    Quando procuro uma operação de inclusão de refeição
    Então não a encontro: a refeição é mantida na tela C101T
    E sem refeição cadastrada no tipo de órgão não há o que ligar a grupo de atendimento

  Cenário: RN-05 — tipo de órgão sem refeição cadastrada
    Dado que o tipo de órgão do meu vínculo não tem refeição cadastrada
    Quando abro a tela C112T
    Então a tela abre vazia, sem nenhuma mensagem

  Cenário: RN-06 — opção de manutenção não disponível
    Dado que estou na tela C112T
    Quando informo uma opção de manutenção diferente de ALT e de CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"

  Cenário: RN-07 — alterar uma refeição que não é a que a tela está mostrando
    Dado que estou na tela C112T com a opção ALT
    Quando informo uma refeição diferente da que a tela está mostrando
    Então vejo "* Consulte antes de atualizar *"
    E nada é gravado

  Cenário: RN-08 — consultar sem informar a refeição
    Dado que estou na tela C112T com a opção CON
    Quando confirmo sem informar a refeição
    Então vejo "* Informe a refeicao *"
    E nada é gravado

  Cenário: RN-08 — consultar uma refeição que não existe
    Dado que estou na tela C112T com a opção CON
    Quando informo uma refeição que não está cadastrada no meu tipo de órgão
    Então vejo "* Refeicao nao cadastrada *"
    E nada é gravado

  Cenário: RN-08 — consultar outra refeição cadastrada
    Dado que estou na tela C112T com a opção CON
    Quando informo outra refeição cadastrada no meu tipo de órgão
    Então a lista passa a mostrar os grupos de atendimento ligados a essa refeição
    E nada é gravado

  Cenário: RN-09 — refeição sem nenhum grupo de atendimento ligado
    Dado que a refeição em tela não tem nenhuma ligação com grupo de atendimento
    Quando consulto essa refeição
    Então vejo "* Refeicao sem grupos de atend.cadastrados *"

  Cenário: RN-10 — linha sem grupo de atendimento ou com ação desconhecida
    Dado que estou na tela C112T com a opção ALT
    E preencho uma linha sem o código do grupo de atendimento, ou com uma ação diferente de I e de E
    Quando confirmo a alteração
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada
    E nada é gravado

  Cenário: RN-11, RN-12, RN-15 e RN-16 — incluir um grupo de atendimento na refeição
    Dado que a refeição em tela não tem ligação com esse grupo de atendimento
    E o grupo está no catálogo do meu tipo de órgão
    Quando preencho a linha com a ação I e confirmo
    Então a ligação da refeição com aquele grupo, no segmento do grupo, é gravada
    E o segmento gravado é o do grupo no catálogo, e não o que digitei na coluna
    E a operação fica registrada na auditoria, com a ligação gravada como valor novo
    E nenhuma outra tabela é gravada

  Cenário: RN-11 — incluir um grupo de atendimento que não está no catálogo
    Dado que o grupo informado não está no catálogo do meu tipo de órgão
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Grupo de atendimento nao cadastrado *"
    E nada é gravado

  Cenário: RN-12 — incluir um grupo de atendimento que a refeição já tem
    Dado que a refeição em tela já tem ligação com esse grupo de atendimento
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Grupo de atendimento ja cadastrado *"
    E nada é gravado

  Cenário: RN-13, RN-15 e RN-16 — excluir uma ligação existente
    Dado que a refeição em tela tem ligação com o segmento e o grupo informados na linha
    E estou na tela C112T com a opção ALT
    Quando preencho a linha com a ação E e confirmo
    Então a ligação da refeição com aquele segmento e aquele grupo é apagada
    E a operação fica registrada na auditoria, com a ligação apagada como valor anterior
    E nenhuma outra tabela é apagada

  Cenário: RN-13 — excluir uma ligação que não existe
    Dado que a refeição em tela não tem ligação com o segmento e o grupo informados na linha
    Quando preencho a linha com a ação E e confirmo
    Então vejo "* Grupo de atendimento nao cadastrado *"
    E nada é apagado

  Cenário: RN-17 — passagem para a refeição seguinte
    Dado que a tela está mostrando uma refeição do tipo de órgão
    Quando peço a passagem para a refeição seguinte
    Então a tela passa a mostrar a refeição seguinte do tipo de órgão
    E, se não houver seguinte, volta à primeira
    E nenhuma ligação é incluída ou excluída nessa passagem

  Cenário: RN-18 — a tela anterior preenchida devolve o controle à tela de origem
    Dado que estou na tela C112T
    Quando o campo da tela anterior chega preenchido
    Então a tela devolve o controle à tela de origem
    E nada é conferido nem gravado

  Cenário: RN-19 — sem permissão para a operação
    Dado que o meu acesso à tela não tem liberada a operação de inclusão ou de exclusão
    Quando confirmo uma inclusão ou uma exclusão
    Então vejo a mensagem de acesso negado para a operação
    E nada é gravado

  Cenário: RN-20 — falha de banco durante a gravação
    Dado que a gravação da ligação falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E a ligação não é considerada gravada
```
