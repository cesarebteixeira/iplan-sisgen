# US — S064C — Consulta de servidores por nível de acesso

## Estória

Como **servidor de CRE que responde pelos níveis de acesso da sua coordenadoria**,
quero **ver quem são os servidores vinculados a um nível de acesso e, daí, abrir a
ficha funcional de um deles**, para que **o nível de acesso deixe de ser um número
solto e passe a ter nome e matrícula — e eu possa conferir quem carrega aquele
nível e a quem ele foi dado**.

O nível de acesso do servidor é o que abre as telas do sistema e o que decide, em
cada uma, o que ele pode fazer. Quem carrega cada nível está no vínculo entre a
matrícula e a coordenadoria, e não em campo nenhum que se veja por aí. Esta tela é
onde esse vínculo se lê pelo lado do nível: ela lista os servidores de um nível e
entrega a matrícula escolhida à ficha funcional. Sem ela, um nível de acesso só se
confere por fora do sistema — e quem recebeu um nível indevido não tem por onde ser
encontrado.

## Contexto

Jornada S000M → S001M → S005M → S064C.
Ator: servidor de CRE — escolhe um nível de acesso, vê os servidores vinculados a
ele na sua coordenadoria e abre a ficha funcional de um deles.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores desta jornada são menus: elas só encaminham. O que a
`S064C` usa da sessão — o nível de acesso, a matrícula, a coordenadoria e o tipo de
órgão — é o que a entrada deixou ali, e a tela apenas o repassa às rotinas de rota
e de segurança. A tela **não** é menu: é consulta, e no fim ela entrega a matrícula
escolhida à ficha funcional, sem passar por menu nenhum (RN-11).

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela é só de consulta

Esta tela não grava, não altera e não apaga nada. Nenhum cadastro é modificado por
ela, em nenhuma das suas respostas; ela lê o cadastro de níveis de acesso, o dos
vínculos das matrículas e o dos funcionários, e mostra. A operação que ela aceita é
a consulta, e outra qualquer é recusada com
**\* Operacao nao disponivel. Use CON \***, com o cursor de volta ao campo da
operação — a mensagem manda usar a consulta. A recusa é conferida uma vez, na
primeira linha da lista; a partir da segunda a tela já não a examina.

### RN-02 — O nível de acesso tem de ser informado

Sem nível de acesso informado não há consulta: a tela recusa com
**\* Informe o nivel de acesso \*** e devolve o cursor ao campo. Não é a mesma coisa
que nível inexistente: aqui o campo ficou em branco, e a tela nem chega a procurar.

### RN-03 — O nível de acesso informado tem de estar cadastrado

O nível de acesso informado é procurado no cadastro de níveis de acesso. Não
estando lá, a tela recusa com **\* Nivel de acesso nao cadastrado \***, devolve o
cursor ao campo e não segue: sem nível válido não há lista nem passagem adiante.

### RN-04 — O nível informado é conferido contra o da sessão

A tela confere o nível de acesso informado contra o nível que veio na sessão do
servidor. Coincidindo, ela segue com o nível da sessão. Não coincidindo e estando o
nível informado no cadastro, ela **não recusa com mensagem**: passa a trabalhar com
o nível que foi digitado, e é ele que recorta a lista. Em qualquer dos casos a
consulta só olha um nível por vez.

[?] Um nível diferente do da sessão, existindo no cadastro, muda a lista: a tela
mostra os servidores daquele nível. Se isso é intencional — consultar o nível de
outro servidor — ou sobra de um desenho anterior, o material não diz. Pergunta ao
site.

### RN-05 — A lista traz matrícula, nome e coordenadoria, 11 por vez

Montada a consulta, a tela lista os servidores vinculados àquele nível de acesso,
cada linha com a **matrícula funcional**, o **nome** do servidor e a
**coordenadoria regional escolar** a que o vínculo pertence — a coordenadoria é o
rótulo do topo da tela, **COORD.REG.ESCOLA**, e é o único rótulo de validação que o
programa carrega. A lista traz **11 linhas** por vez, e as matrículas vêm em ordem
crescente de número.

[?] Quando o nível tem mais servidores do que as 11 linhas, a tela avança pela
lista e a consulta seguinte recomeça da maior matrícula que apareceu. Se o resto
aparece numa consulta seguinte, e se o operador recebe algum aviso de que ficou
gente de fora, o material não diz. Pergunta ao site.

### RN-06 — Servidor retirado do cadastro não aparece na lista

O vínculo leva à ficha do servidor, e a ficha marcada com a operação de exclusão
não entra na lista: a tela pula aquele vínculo e segue para o próximo, sem avisar e
sem deixar linha em branco. Quem foi retirado do cadastro some da relação.

### RN-07 — Nível sem ninguém cadastrado avisa e não segue

Se a varredura não encontrar nenhum servidor vinculado ao nível de acesso, a tela
avisa **\* Nao existem usuarios cadastrados \*** e para ali: não monta lista e não
passa nada adiante.

[?] O percurso da lista tem duas saídas que caem no mesmo aviso: acabaram os
vínculos daquele nível, ou o percurso retornou à última linha sem ter carregado
ninguém. Se os dois casos são o mesmo para quem opera — e se "não existem usuários
cadastrados" é a leitura certa também quando o nível tem gente fora do que a
consulta alcança —, o material não diz. Pergunta ao site.

### RN-08 — Marcar uma linha exige ter apontado o servidor

Quando o operador aponta o servidor, ele informa dois dados na linha: a
**matrícula** e a **operação** pretendida. Informando a operação sem a matrícula, a
tela recusa com **\* Informe consulta para linha preenchida \*** e devolve o cursor
ao campo da operação. Sem os dois, a tela não procura ninguém.

[?] A mensagem fala em "informar a consulta", mas o que a conferência examina é a
presença da matrícula; o conteúdo digitado no campo da operação a tela nunca
compara com código nenhum. O que o operador deve escrever ali — e se existe mais de
um código aceito —, o material não diz. Pergunta ao site.

### RN-09 — O servidor apontado tem de estar cadastrado

Apontado o servidor, a matrícula é procurada na ficha funcional. Não estando lá, a
tela recusa com **\* Usuario nao cadastrado \*** e devolve o cursor ao campo da
matrícula.

[?] A recusa é a mesma do LOGON para matrícula não cadastrada, mas aqui o texto que
o operador vê sai da tabela de mensagens do idioma, que não faz parte do lote; o que
se pode afirmar é a mensagem que o LOGON mostra com esse mesmo número, não a que
esta tela mostra. Pergunta ao site.

### RN-10 — O campo de tela anterior encerra a mensagem sem consultar

Há na tela um campo de **tela anterior**. Preenchido, ele encerra a mensagem em
silêncio: a tela não monta a lista, não procura o servidor apontado e não passa nada
adiante. Em branco — que é como ele chega da jornada, pelo menu `S005M` —, a tela
segue normalmente.

### RN-11 — A tela entrega a matrícula escolhida à ficha funcional

Confirmada a mensagem com a operação e o servidor apontado — e estando ele
cadastrado —, a tela abre a **ficha funcional (`S010T`)** já com a matrícula
daquele servidor e **em consulta**. É a única passagem adiante que esta tela faz, e
ela não passa por menu.

O que a matrícula é: a que estava apontada na linha. A tela move o bloco da linha
escolhida para a primeira posição antes de passar, de modo que a linha apontada
vira a primeira, e é essa matrícula que a ficha recebe.

### RN-12 — O modo em que a ficha funcional abre é decidido por quem a chama

A ficha funcional abre **em consulta** quando vem desta tela; quem a chama define
o modo, e não um campo da própria ficha. Esta tela entrega, junto com a matrícula,
a operação de consulta — e é isso que faz a ficha abrir para ver, e não para
alterar.

[?] A ficha funcional tem, no seu próprio código, uma conferência que só aproveita
os dados de quatro telas de origem, e o código desta tela está entre as quatro. O
que a conferência examina, porém, chega em branco nesta jornada, e por isso ela cai
no ramo que abre em consulta de qualquer maneira. Se o nome desta tela naquela
conferência é resto de um desenho anterior ou se há um caminho em que aquilo chega
preenchido e a ficha abre em alteração, o material não diz — e a diferença não é
cosmética: uma tela que abre em consulta onde deveria abrir em alteração não falha,
só não deixa gravar. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta dos servidores vinculados a um nível de acesso

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S064C

  Cenário: A consulta lista os servidores do nível de acesso
    Dado que o nível de acesso da minha sessão está cadastrado
    Quando confirmo a consulta
    Então vejo até 11 linhas, cada uma com a matrícula, o nome e a coordenadoria do servidor
    E as matrículas vêm em ordem crescente
    E nada é gravado

  Cenário: O nível escolhido é o que recorta a lista
    Dado que o nível de acesso 5 tem servidores vinculados na minha coordenadoria
    E o nível de acesso 7 tem outros servidores
    Quando confirmo a consulta com o nível 5
    Então a lista é a dos servidores do nível 5
    E os servidores do nível 7 não aparecem

  Cenário: Servidor retirado do cadastro não aparece
    Dado que um dos vínculos do nível aponta para um servidor retirado do cadastro
    Quando confirmo a consulta
    Então esse servidor não ocupa nenhuma linha da lista
    E os demais aparecem na posição que lhes cabe

  Cenário: Nível sem ninguém vinculado
    Dado que o nível informado não tem nenhum servidor vinculado
    Quando confirmo a consulta
    Então vejo a mensagem "* Nao existem usuarios cadastrados *"
    E a tela não segue adiante

  Cenário: Nível de acesso não informado
    Quando confirmo a consulta sem informar o nível de acesso
    Então vejo a mensagem "* Informe o nivel de acesso *"
    E o cursor volta ao campo do nível de acesso
    E nenhuma lista é montada

  Cenário: Nível de acesso não cadastrado
    Quando confirmo a consulta com um nível de acesso que não está no cadastro
    Então vejo a mensagem "* Nivel de acesso nao cadastrado *"
    E o cursor volta ao campo do nível de acesso
    E nada é consultado nem passado adiante

  Cenário: Nível diferente do meu não é recusado
    Dado que o meu nível de acesso é o 5
    E o nível de acesso 7 está cadastrado
    Quando confirmo a consulta com o nível 7
    Então não vejo mensagem de recusa
    E a lista que vejo é a dos servidores do nível 7

  Cenário: Operação diferente de consulta
    Quando confirmo a mensagem com uma operação que não é a consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nada é consultado nem passado adiante

  Cenário: Operação marcada sem servidor apontado
    Quando confirmo a mensagem marcando a operação de uma linha sem apontar a matrícula
    Então vejo a mensagem "* Informe consulta para linha preenchida *"
    E o cursor volta ao campo da operação
    E nada é passado adiante

  Cenário: Escolher um servidor da lista e abrir a ficha
    Dado que a lista do nível mostra os servidores vinculados
    E que o servidor apontado está cadastrado
    Quando confirmo a mensagem com a operação e a matrícula dele
    Então a ficha funcional S010T abre com a matrícula daquele servidor
    E abre em consulta
    E nenhum cadastro é gravado por esta tela

  Cenário: Servidor apontado não cadastrado
    Quando confirmo a mensagem com a operação e uma matrícula que não existe
    Então vejo a mensagem "* Usuario nao cadastrado *"
    E o cursor volta ao campo da matrícula
    E a ficha funcional não abre

  Cenário: Tela anterior preenchida encerra a mensagem
    Quando preencho o campo de tela anterior e confirmo
    Então a tela não monta a lista
    E não passa nada adiante

  Cenário: A consulta não grava nada
    Dado que fiz a consulta de um nível de acesso
    Quando nada mais informo e confirmo
    Então nenhum nivel de acesso, vínculo ou ficha funcional é gravado, alterado ou apagado
```
