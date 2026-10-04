# US — C022T — Manter os segmentos de atendimento do órgão filho

## Estória

Como **servidor da CRE**, quero **manter os segmentos de atendimento de cada órgão
filho e a marcação de atendimento em sábado e domingo de cada um**, para que o
órgão fique classificado por segmento de atendimento e o sistema saiba o que
aquele órgão atende.

Sem esse vínculo o órgão não diz o que atende: é ele que liga o órgão ao segmento
de atendimento, e é dele que saem os grupos de atendimento previstos para aquele
segmento. A tela é a única da jornada que grava — o que ela inclui, altera ou
exclui vale também para o que depende do par órgão e segmento.

## Contexto

Jornada S000M → C000M → C200M → C022T.

Ator: servidor de CRE — mantém os segmentos de atendimento de cada órgão filho da
sua coordenadoria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio.

As duas telas do meio do caminho são menus: elas não deixam nada de próprio para
a tela de destino, apenas dizem qual tela abrir. O que a C022T usa da sessão — o
tipo de órgão, a coordenação regional escolar e o órgão filho do servidor — foi
deixado pela entrada.

A tela não encadeia para nenhuma outra: ela não passa registro nem operação
adiante, e a jornada termina nela. Também não há comparação com a tela de origem
que mude o comportamento dela; o que varia na abertura vem do que a própria
sessão já trazia — o órgão preso ao servidor, o modo deixado pela sessão e a
última consulta.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela identifica o órgão filho, a coordenação regional escolar e o código do segmento

A tela trabalha com **três dados digitados**: o **órgão filho (SDI)**, com 8
dígitos; a **coordenação regional escolar (CRE)**, com 2 dígitos; e o **código do
segmento de atendimento**, com 2 dígitos. Os três passam pela conferência
numérica do sistema antes de qualquer consulta: campo em branco vira zero, os
zeros à esquerda são descartados e o que não for número é recusado — e o que não
passa por essa conferência não chega ao cadastro.

### RN-02 — A grade tem 12 linhas, e cada linha tem segmento, sábado/domingo e ação

A tela mostra os segmentos do órgão em uma grade de **12 linhas** — o sistema fixa
esse mesmo limite nas três passagens da tela (a de abertura, a de conferência e a
de gravação). Cada linha tem **três dados**: o **código do segmento** (2 dígitos),
o **indicador de atendimento em sábado e domingo** (1 caractere) e a **ação**
(1 caractere). O nome do segmento e o indicador de sábado e domingo por extenso
são preenchidos pelo sistema a partir dos cadastros — não se digita.

### RN-03 — A tela só opera em ALT (alterar) ou CON (consultar)

A opção de manutenção aceita apenas **alteração** e **consulta**; inclusão e
exclusão não se fazem por esta tela. Qualquer outra opção é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta no campo da
opção, e nada é gravado.

### RN-04 — Alterar exige ter consultado antes

Ao alterar, o órgão informado tem de ser o mesmo que a última consulta da sessão
deixou carregado. É essa amarração que faz as conferências do órgão (RN-06)
rodarem apenas no caminho da consulta: quem altera já passou por elas quando
consultou. Tentar alterar outro órgão é recusado com **\* Consulte antes de
atualizar \***, com o cursor no campo do órgão.

### RN-05 — O servidor preso a um órgão só alcança o próprio órgão, e o órgão é obrigatório

Se a entrada deixou um órgão filho preso ao servidor, a tela só aceita esse
órgão: informar outro é recusado com **\* Usuario sem acesso a outro orgao \***.
Se o servidor não tem órgão preso, ele pode informar qualquer órgão — mas
informar é obrigatório: em branco, a recusa é **\* Informe o orgao \***.

### RN-06 — O órgão informado tem de existir, estar ativo, estar completo, ser do tipo da secretaria e do grupo do servidor

Na consulta, o órgão digitado é lido no cadastro do órgão filho e passa por cinco
peneiras, nesta ordem:

| peneira | recusa |
| --- | --- |
| o órgão está cadastrado | \* Orgao nao cadastrado \* |
| o órgão não está inativo | \* Orgao cadastrado como inativo \* |
| o órgão tem bairro, órgão pai, nome, endereço, número de matrículas e número de pessoas preenchidos — **6 dados** | \* Orgao cadastrado com dados incompletos \* |
| o órgão é do tipo de órgão da secretaria do servidor | \* Orgao nao pertence a esta secretaria \* |
| quando o servidor tem coordenação regional escolar, o órgão é da mesma coordenação dele | \* <- Usuario sem acesso ao grupo deste orgao \* |

Cada recusa devolve o cursor ao campo do órgão e não grava nada.

### RN-07 — O nome do órgão, a coordenação regional escolar e o indicador de creche vêm do cadastro

O sistema não aceita esses valores do que foi digitado: encontrado o órgão, copia
para a tela o **nome**, a **coordenação regional escolar** e o **indicador de
creche** do cadastro, mostrando creche por extenso (Sim/Não). É essa
coordenação — a do cadastro do órgão — que segue para o vínculo gravado, e não a
digitada.

[?] A coordenação regional escolar é um campo digitável na tela e é conferida
como número, mas depois é sempre substituída pela coordenação do cadastro do
órgão. Ou o campo serve para o servidor conferir o que digitou, ou o programa
ignora o que ele digita. Pergunta ao site.

### RN-08 — A tela abre já apontada para o órgão do servidor e no modo que a sessão tiver deixado

Ao abrir, a tela adota o **modo de manutenção que a sessão tiver deixado**; não
havendo nada deixado, abre em **consulta**. E, se o servidor tem um órgão preso, a
tela já abre com esse órgão carregado — nome, coordenação regional escolar e
creche preenchidos; se não tem, posiciona o cursor no campo do órgão para que ele
informe. O órgão e o modo carregados a cada consulta ficam guardados na sessão, e
é esse órgão guardado que a alteração usa depois (RN-04).

Nesta jornada os dois menus do caminho não deixam modo nenhum: eles apenas dizem
qual tela abrir. A alteração, portanto, começa pelo servidor digitando ALT e
consultando o órgão.

[?] O modo deixado na sessão vem de uma área de trabalho compartilhada entre os
programas; o desenho dessa área não está no lote, e não é possível dizer de qual
tela — além da própria C022T — esse modo poderia vir. Se em algum caminho a tela
abrir em consulta onde deveria abrir em alteração, a causa está nessa área.
Pergunta ao site.

### RN-09 — Sábado/domingo: só "S" vale como Sim; qualquer outra coisa é "N"

O indicador de atendimento em sábado e domingo guarda um caractere. O sistema
preserva apenas o **"S"**; tudo o mais — branco inclusive — é normalizado para
**"N"** antes de gravar, e a tela mostra o indicador por extenso (Sim/Não).

### RN-10 — Cada linha traz a sua ação: I inclui, A altera, E exclui; linha vazia ou ação desconhecida é ignorada

A ação é da linha, não da tela — cada linha da grade pode pedir uma operação
diferente. O sistema traduz a ação para a operação correspondente (inclusão,
alteração ou exclusão) antes de pedir autorização. Linha sem código de segmento
não opera, e ação fora de I, A e E também não — sem mensagem nenhuma.

### RN-11 — Incluir exige que o vínculo ainda não exista e que o segmento esteja cadastrado

Na inclusão o sistema procura o vínculo do órgão com aquele segmento: se já
existe, recusa com **\* Orgao ja cadastrado neste segmento \***. Em seguida
procura o segmento no cadastro dos segmentos de atendimento: se não existe,
recusa com **\* Segmento nao cadastrado \***. O órgão considerado é sempre o da
última consulta.

### RN-12 — Incluir o segmento propaga o vínculo para os grupos de atendimento do segmento

A inclusão não grava apenas o vínculo do órgão com o segmento: o sistema percorre
os **grupos de atendimento previstos para aquele segmento** e cria, para cada
grupo que ainda não tenha registro, um vínculo do mesmo órgão com o mesmo
segmento na granularidade do grupo. É a materialização do vínculo também por
grupo de atendimento.

[?] O que é, em negócio, o "grupo de atendimento"? O cadastro prevê os grupos de
cada segmento e a tela propaga o vínculo até eles, mas o corpus não define o
conceito. Pergunta ao site.

### RN-13 — Alterar mexe só na marcação de sábado e domingo

A alteração exige que o vínculo exista; não existindo, a recusa é **\* Orgao nao
cadastrado neste segmento \***. Existindo, o sistema compara a marcação gravada
com a digitada: se forem iguais, nada acontece; se diferirem, trava o registro,
substitui a marcação de sábado e domingo e grava — os demais dados do vínculo
ficam como estavam.

### RN-14 — A exclusão apaga o vínculo, o que depende dele e os grupos de atendimento

A exclusão exige que o vínculo exista; não existindo, a recusa é a mesma da
alteração. Existindo, o sistema apaga, nesta ordem: o **vínculo do órgão com o
segmento**; depois **cada referência** ligada ao par órgão e segmento, uma a uma;
e por fim **cada grupo de atendimento** do par, um a um. Cada passo deixa o seu
registro de auditoria próprio.

[?] O que é, em negócio, a referência ligada ao par órgão e segmento que a
exclusão apaga em cascata e que não aparece em nenhuma tela desta jornada?
Pergunta ao site.

### RN-15 — A guarda dos grupos de atendimento recusa a exclusão

Antes de deixar a exclusão passar, o sistema procura qualquer grupo de
atendimento do par órgão e segmento; achando, recusa com **\* Nao exclua. Grupos
de atend.cadastrados \*** e não apaga nada.

[?] A guarda recusa excluir quando há grupo de atendimento cadastrado para o par,
mas o próprio caminho de exclusão apaga esses grupos — ele tem o laço que
percorre e apaga os grupos do mesmo par. Ou a guarda vale para outro caso, ou
aquele trecho de exclusão ficou inalcançável: sempre que ele teria o que apagar,
a guarda já barrou antes. Pergunta ao site.

### RN-16 — Consultar não grava nada

Na consulta a tela apenas exibe: lê o órgão, lê o vínculo e o nome do segmento e
monta a grade. A passagem que grava é desviada de propósito quando a opção é
consulta — nenhuma operação de banco é executada. O único efeito é interno à
sessão: o órgão e o modo consultados ficam guardados para a alteração seguinte
(RN-04).

### RN-17 — A tela mostra o que o órgão já tem e avisa quando ele não tem segmento nenhum

Ao carregar o órgão, a tela lista os vínculos que ele já tem, preenchendo cada
linha com o código do segmento, o nome do segmento e a marcação de sábado e
domingo por extenso. Quando o órgão não tem nenhum segmento vinculado, o aviso é
**\* Orgao sem segmentos cadastrados \***.

### RN-18 — Cada operação só grava depois de autorizada

Antes de tocar em qualquer cadastro, o sistema confere a autorização do servidor
para aquela tela e para **aquela operação** — inclusão, alteração e exclusão têm
permissões separadas. Sem a permissão da operação, monta a mensagem de recusa e a
linha não é gravada. A mesma conferência roda na abertura da tela; e sem acesso à
tela a sessão é devolvida à entrada.

### RN-19 — Toda gravação deixa rastro na auditoria

Cada operação grava um registro na **trilha de auditoria (A010T)** junto da
gravação: o cadastro que a originou (o vínculo, a referência ou o grupo), a
operação (inclusão, alteração ou exclusão), o tipo de órgão, o órgão filho, a
coordenação regional escolar, a matrícula funcional, a estação, a sessão, a data
e a hora, e os valores **antes e depois**. Na inclusão, o "antes" fica vazio e o
"depois" é o registro novo; na alteração, os dois são o registro alterado; na
exclusão, o "antes" é o registro apagado e o "depois" fica vazio.

### RN-20 — Falha de banco interrompe a operação e avisa

Todo acesso a dados testa o erro do banco. A falha de leitura e a de exclusão
viram o aviso de erro de leitura, e a de gravação vira o aviso de erro de
gravação — os dois despachados pela rotina de comunicação do sistema — e a
transação para ali, sem completar o resto.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os segmentos de atendimento do órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C022T

  Cenário: RN-01, RN-02, RN-16 e RN-17 — consultar os segmentos de um órgão filho
    Dado que estou na tela C022T com a opção CON
    E informo um órgão filho do meu escopo, que já tem segmentos
    Quando confirmo a consulta
    Então vejo o nome do órgão, a coordenação regional escolar e o indicador de creche
    E vejo, nas 12 linhas da grade, o código do segmento, o nome do segmento e a marcação de sábado e domingo por extenso
    E nada é gravado

  Cenário: RN-17 — órgão sem nenhum segmento
    Dado que consultei um órgão filho que não tem segmento vinculado
    Então vejo "* Orgao sem segmentos cadastrados *"
    E nada é gravado

  Cenário: RN-01 — campo não numérico
    Quando informo no órgão filho, na coordenação regional escolar ou no código do segmento algo que não é número
    Então o campo é recusado antes de qualquer consulta
    E o cadastro não é lido

  Cenário: RN-03 — opção de manutenção não disponível
    Dado que estou na tela C022T
    Quando informo uma opção de manutenção diferente de ALT e CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E nada é gravado

  Cenário: RN-04 — alterar sem ter consultado antes
    Dado que estou na tela C022T com a opção ALT
    E informo um órgão diferente do que consultei
    Quando confirmo
    Então vejo "* Consulte antes de atualizar *"
    E nada é gravado

  Cenário: RN-05 — órgão em branco
    Dado que o meu usuário não tem órgão preso
    Quando confirmo a consulta sem informar o órgão
    Então vejo "* Informe o orgao *"

  Cenário: RN-05 — órgão fora do meu escopo
    Dado que o meu usuário está preso a um órgão filho
    Quando informo outro órgão
    Então vejo "* Usuario sem acesso a outro orgao *"

  Cenário: RN-06 — órgão não cadastrado
    Quando informo um órgão filho que não existe no cadastro
    Então vejo "* Orgao nao cadastrado *"

  Cenário: RN-06 — órgão inativo
    Quando informo um órgão filho cadastrado como inativo
    Então vejo "* Orgao cadastrado como inativo *"

  Cenário: RN-06 — órgão com dados incompletos
    Quando informo um órgão filho sem bairro, sem órgão pai, sem nome, sem endereço, sem número de matrículas ou sem número de pessoas
    Então vejo "* Orgao cadastrado com dados incompletos *"

  Cenário: RN-06 — órgão de outra secretaria
    Quando informo um órgão filho do tipo de órgão de outra secretaria
    Então vejo "* Orgao nao pertence a esta secretaria *"

  Cenário: RN-06 — órgão de outro grupo
    Dado que o meu usuário tem coordenação regional escolar
    Quando informo um órgão filho de outra coordenação
    Então vejo "* <- Usuario sem acesso ao grupo deste orgao *"

  Cenário: RN-10, RN-11, RN-12 e RN-19 — incluir um segmento no órgão filho
    Dado que consultei o órgão e ele ainda não tem esse segmento
    E o segmento está cadastrado
    Quando preencho a linha com a ação I e confirmo
    Então o vínculo do órgão com o segmento é gravado
    E é criado um vínculo para cada grupo de atendimento previsto para o segmento
    E cada gravação fica registrada na auditoria

  Cenário: RN-11 — incluir um segmento que o órgão já tem
    Dado que consultei o órgão e ele já tem esse segmento
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Orgao ja cadastrado neste segmento *"
    E nada é gravado

  Cenário: RN-11 — incluir um segmento que não está cadastrado
    Dado que consultei o órgão
    Quando incluo um código de segmento que não existe
    Então vejo "* Segmento nao cadastrado *"
    E nada é gravado

  Cenário: RN-09 e RN-13 — alterar a marcação de sábado e domingo
    Dado que o órgão já tem o segmento com a marcação N
    Quando mudo a marcação da linha para S com a ação A e confirmo
    Então a marcação do vínculo passa a valer Sim
    E os demais dados do vínculo não mudam
    E a operação fica registrada na auditoria

  Cenário: RN-09 — marcação de sábado e domingo diferente de S
    Quando preencho a marcação da linha com qualquer valor diferente de S
    Então a marcação é gravada como Não

  Cenário: RN-13 — alterar um vínculo que não existe
    Dado que o órgão não tem esse segmento
    Quando preencho a linha com a ação A e confirmo
    Então vejo "* Orgao nao cadastrado neste segmento *"
    E nada é gravado

  Cenário: RN-14 e RN-19 — excluir um vínculo sem grupos de atendimento
    Dado que o órgão tem o segmento e não há grupo de atendimento para o par
    Quando preencho a linha com a ação E e confirmo
    Então o vínculo do órgão com o segmento é apagado
    E cada referência do par é apagada
    E cada gravação fica registrada na auditoria

  Cenário: RN-15 — excluir um vínculo que tem grupos de atendimento
    Dado que existe grupo de atendimento para o par órgão e segmento
    Quando preencho a linha com a ação E e confirmo
    Então vejo "* Nao exclua. Grupos de atend.cadastrados *"
    E nada é apagado

  Cenário: RN-10 — linha sem segmento ou com ação desconhecida
    Dado que preencho uma linha sem o código do segmento, ou com uma ação diferente de I, A e E
    Quando confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada

  Cenário: RN-18 — operação sem autorização
    Dado que não tenho permissão para a operação pedida na linha
    Quando confirmo
    Então vejo a mensagem de recusa da segurança
    E nada é gravado

  Cenário: RN-20 — falha de banco na gravação
    Dado que a gravação do vínculo falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com o aviso de erro do sistema
    E o vínculo não é considerado gravado
```
