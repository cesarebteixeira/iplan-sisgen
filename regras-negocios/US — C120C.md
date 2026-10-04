# US — C120C — Consulta das secretarias cadastradas

## Estória

Como **servidor de CRE**, quero **consultar a relação das secretarias cadastradas, com os códigos
que cada uma tem no município, e abrir a ficha da secretaria que eu marcar**, para que **eu confira
como cada secretaria está identificada no município e chegue à manutenção dela sem decorar o
código**.

A identificação da secretaria no município é o que liga o cadastro da secretaria aos registros do
município: cada secretaria tem um código no município, pode ter até cinco outros, e informa os
códigos de processo RIO que usa. Esta relação existe para que essa identificação seja conferida de
uma vez, secretaria por secretaria, em vez de uma consulta por código. Sem ela, um código errado só
aparece quando alguém abre a ficha daquela secretaria, uma a uma — e quem não decora os códigos não
chega à ficha.

## Contexto

Jornada S000M → C000M → C015M → C120C (4 passos).

Ator: servidor de CRE — consulta a relação das secretarias cadastradas e escolhe uma delas para
abrir a ficha em consulta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio. Os menus do caminho não gravam nada: só encaminham.

A `C120C` é uma tela de consulta, não um menu: ela mostra uma página de **quinze secretarias por
vez** e **não tem campo para escolher a secretaria da relação** — a relação começa na posição que
ficou guardada da exibição anterior (RN-03). Da sessão ela usa a **secretaria do vínculo**, para
dizer no alto de quem é a sessão, e a **data do sistema**; essa carga é regra da entrada e está no
anexo, em **Regras que se revelaram da entrada**.

A tela encadeia com a `C120T`, que mantém o cadastro das secretarias, nos dois sentidos: marcada uma
secretaria, ela entrega a sessão à `C120T` com a secretaria escolhida e a operação de consulta
(RN-04); e a `C120T` devolve a sessão a esta tela. É por isso que a jornada termina aqui — quem
mostra e mantém a ficha é a tela seguinte, e esta tela é o índice dela.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela consulta as secretarias cadastradas

Esta é uma tela de **consulta**. Ela mostra a relação das secretarias do cadastro e, de cada uma, o
**código**, a **sigla**, o **código no município**, **até cinco outros códigos no município**, os
**dois códigos de processo RIO**, a marca de **se o número de processo usa o grupo** e a marca de
**se a secretaria está ativa** — as duas marcas saem **Sim** ou **Nao**. No alto a tela mostra a
**sigla da secretaria do vínculo** e a **data do sistema**.

O código no município e os cinco outros são a identificação da secretaria no município: eles só
aparecem quando existem — o que estiver zerado sai em branco, e cada código adicional sai precedido
de um traço. As duas marcas saem **Nao** somente quando o cadastro traz exatamente "N"; qualquer
outro conteúdo, inclusive em branco, sai **Sim**.

Nada nesta tela é gravado: nem cadastro, nem travamento de registro, nem linha de auditoria — o
cadastro de auditoria não está entre os cadastros que a tela enxerga.

[?] A relação não filtra a marca que o cadastro da secretaria guarda da última operação: ela mostra
todas as secretarias registradas, inclusive as que estiverem marcadas como excluídas, e a tela não
consulta essa marca em ponto nenhum. Se a relação deveria omitir as excluídas — como fazem outras
relações deste sistema —, a fonte não diz. Pergunta ao site.

### RN-02 — A relação traz quinze secretarias por página, na ordem do código

A página comporta **quinze secretarias**. Cada linha exibida ocupa **80 posições** e traz os dados
daquela secretaria; a parte editável de cada linha tem **três posições** — o **código** (dois
dígitos) e a **marca da linha** (uma posição), que é como se escolhe a secretaria (RN-04). Dos
campos que a cópia do cadastro da secretaria carrega, a tela usa **doze** e ignora **três**: o nome
da secretaria, a marca da última operação e um número de processo.

A relação é lida na **ordem do código da secretaria** — a ordem da chave do cadastro —, e cada linha
avança para a secretaria seguinte nessa ordem: não há busca por nome nem por sigla, e a tela também
não oferece página anterior.

[?] O dicionário da base declara **catorze** campos para o cadastro da secretaria e a cópia que as
telas carregam traz **quinze**: o campo a mais é um número de processo, que o cadastro de secretarias
informa e que esta relação não mostra. Ou o dicionário está desatualizado, ou o campo pertence a
outro cadastro. Pergunta ao site.

### RN-03 — A relação começa na secretaria que ficou guardada da exibição anterior

A tela não tem campo para escolher por onde a relação começa: ela começa na **posição guardada na
sessão**. Ao montar a página, a posição passa a ser a **última secretaria mostrada**; quando a
relação chega ao fim, a posição é **limpa**, e a exibição seguinte começa do começo. Quando esta
tela entrega a sessão à `C120T`, a posição passa a ser a **secretaria escolhida** — e é por isso que,
voltando da `C120T`, a relação reabre na secretaria que se abriu.

[?] Na primeira abertura de uma sessão não está no material quem deixa a posição: os menus do
caminho não deixam nenhuma secretaria escolhida na sessão — só o código da tela que abrem. Se a
posição chegar vazia, a tela pode avisar que não existem secretarias cadastradas mesmo com o
cadastro cheio (RN-05). O que o sistema faz nesse caso, e quem deveria preencher a posição inicial,
não está nos fontes lidos. Pergunta ao site.

[?] Ao virar a página, a relação parte da última secretaria mostrada, e o material lido não decide
se essa leitura **repete** aquela secretaria na primeira linha da página seguinte ou já começa na
seguinte: a leitura da primeira posição é feita pela chave, e a das demais é uma continuação na
ordem. Se repetir, a mesma secretaria aparece em duas páginas seguidas. Pergunta ao site.

### RN-04 — Marcada uma secretaria, a ficha dela se abre em consulta

A escolha é a **marca da linha**: marcada uma linha com a marca que a dispara, e estando o **código**
daquela linha preenchido, a tela **não** segue com operação própria — ela entrega a sessão à `C120T`,
a tela que mantém o cadastro das secretarias, com a **secretaria escolhida** e a **operação de
consulta**, e registra a própria tela como **origem** da passagem. É por causa dessa origem que a
`C120T` abre em **consulta** sobre a secretaria escolhida, e não pedindo cadastro.

Sem a marca na linha, ou com o código em zero, a tela apenas segue mostrando a relação e não abre
ficha nenhuma. A tela **não confere** se a secretaria marcada existe antes de passar adiante: ela
entrega o código como está, e nada é gravado por esta tela nessa passagem.

[?] O rótulo que o servidor vê na marca da linha e o valor que ele digita não estão no corpus: o
fonte fixa o literal que dispara a passagem e o fato de a marca ser exibida, mas o formato da tela
não veio no lote. A mesma dúvida vale para os rótulos das colunas da relação. Pergunta ao site.

### RN-05 — Sem nenhuma secretaria na posição de partida, a tela avisa e não relaciona nada

Quando a relação **não encontra nenhuma secretaria na sua posição de partida**, a tela avisa
**\* Nao existem secretarias cadastradas \*** e não relaciona nada. O aviso é o do topo da relação:
ele só é montado na primeira posição da página, e não se repete a cada posição vazia. Quando o aviso
sai, a posição guardada é limpa.

### RN-06 — O código da linha é conferido como número, e o zero não abre ficha

O código informado em cada linha passa por uma **conferência de número** antes de qualquer uso, e o
que estiver **em branco é tratado como zero**. Como a passagem exige o código diferente de zero
(RN-04), uma linha marcada sem código não abre ficha nenhuma: a tela segue mostrando a relação.

### RN-07 — A tela não grava, não exclui e não trava registro

O programa carrega as declarações de gravação, de exclusão e de travamento para os dois cadastros que
enxerga — o cadastro de telas e o das secretarias —, mas **nenhuma delas é executada**: as únicas
operações que a tela aciona são as leituras, as rotinas comuns da sessão e o aviso ao usuário. O
travamento de registro só aparece dentro dos caminhos de exclusão, que a tela não percorre.

### RN-08 — A consulta exige acesso à tela e permissão da operação

Na abertura, a tela confere se ela própria consta do **cadastro de telas** — não constando, o aviso é
**\* Tela nao disponivel \*** — e se o **código de acesso** de quem opera tem a tela — não tendo, a
recusa é **\* Acesso negado para esta matricula \***. A abertura confere ainda a **estação** contra a
da sessão: estando a sessão aberta em outra estação, o acesso é encerrado e a tela não abre.

Na confirmação, a tela confere a **rota** — tendo a tela sido retirada do cadastro de telas, o aviso
é **\* Tela nao cadastrada \*** — e, para a operação que ela monta, a autorização daquela operação no
mesmo código de acesso — não tendo, a recusa é **\* Acesso negado para esta operacao \***. Nas
recusas nada é mostrado nem passado adiante.

[?] O cadastro de telas guarda um indicador por operação — consulta, inclusão, alteração e exclusão —
, e a operação de consulta atravessa a conferência de permissão sem que o indicador da consulta seja
lido em nenhum ponto: só a inclusão, a alteração e a exclusão são conferidas. Ou a consulta é
liberada a quem tem o registro da tela, ou a conferência está deixando de ler a permissão de
consulta. Pergunta ao site.

### RN-09 — Falha na leitura do cadastro interrompe a consulta e avisa

Toda leitura desta tela testa a falha do banco. Falha que não seja "não achado" vira a **ação de erro
de acesso**, com a mensagem de erro do sistema, e a operação para ali, sem completar a relação.

### RN-10 — A tela não muda conforme quem a chamou; o que muda é a posição da relação

A tela não compara o código da tela de origem com nada e assume a **consulta** em qualquer entrada —
pelo menu do caminho, pela devolução da `C120T` ou na primeira abertura da sessão. O que muda
conforme quem a chamou é apenas a **posição guardada da relação** (RN-03). Quem muda de comportamento
por causa da origem é a tela **seguinte**: a `C120T` abre em consulta quando a origem é esta tela
(RN-04).

[?] A operação que a tela carrega faz parte do leiaute dela e é levada para a exibição, e a tela não
confere o valor desse campo em ponto nenhum: qualquer valor informado segue para a conferência de
permissão como se fosse a operação pedida, e a tela não tem mensagem própria de operação
indisponível. Se o servidor pode trocar o valor, e o que acontece quando troca, não está no material.
Pergunta ao site.

[?] O leiaute da tela carrega ainda um campo com o código de uma tela de destino, e a rota do sistema
abandona esta tela quando ele vem preenchido, antes de qualquer conferência. Nenhum fonte desta
jornada o preenche, e não está no material quem o preenche nem o que o servidor vê nesse caso.
Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar as secretarias cadastradas e abrir a ficha da secretaria escolhida

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C120C

  Cenário: RN-01 e RN-02 — abrir a tela mostra a relação das secretarias
    Quando abro a tela C120C
    Então vejo a sigla da minha secretaria e a data do sistema
    E vejo até quinze secretarias, cada uma com o código, a sigla, o código no município, os outros códigos no município, os códigos de processo RIO e as marcas de processo e de ativo
    E os códigos no município que não existem saem em branco
    E as marcas de processo e de ativo saem Sim ou Nao
    E nada é gravado

  Cenário: RN-02 — a relação continua na página seguinte
    Dado que o cadastro tem mais de quinze secretarias
    Quando a primeira página da relação é mostrada
    Então vejo as quinze primeiras na ordem do código
    E a exibição seguinte parte da última secretaria mostrada

  Cenário: RN-01 — a consulta não deixa rastro
    Dado que faço uma consulta
    Quando a consulta termina
    Então nenhum registro é travado
    E nenhuma linha nova aparece na trilha de auditoria

  Cenário: RN-03 — a relação retoma de onde parou
    Dado que a exibição anterior mostrou a relação até uma secretaria
    Quando a tela é exibida de novo na mesma sessão
    Então a relação começa naquela secretaria

  Cenário: RN-03 — esgotada a relação, a exibição seguinte começa do começo
    Dado que a relação chegou ao fim do cadastro
    Quando a tela é exibida de novo na mesma sessão
    Então a posição guardada é limpa
    E a relação começa do começo do cadastro

  Cenário: RN-04 — marcar uma secretaria e abrir a ficha dela
    Dado que a relação mostra as secretarias
    E marco a linha de uma secretaria, com o código dela preenchido
    Quando confirmo
    Então a ficha daquela secretaria se abre em consulta, sem passar por menu
    E a tela fica registrada como a origem dessa passagem
    E nada é gravado por esta tela

  Cenário: RN-04 — a linha sem marca não abre ficha
    Dado que a relação mostra as secretarias
    Quando confirmo sem marcar nenhuma linha
    Então a tela segue mostrando a relação
    E nenhuma ficha se abre

  Cenário: RN-06 — a linha marcada sem código não abre ficha
    Dado que marco uma linha cujo código está em branco
    Quando confirmo
    Então nenhuma ficha se abre
    E a relação segue como estava

  Cenário: RN-05 — nenhuma secretaria na posição de partida
    Quando confirmo a consulta e a relação não encontra secretaria nenhuma
    Então vejo a mensagem "* Nao existem secretarias cadastradas *"
    E nenhuma secretaria é relacionada
    E a posição guardada da relação é limpa

  Cenário: RN-08 — sem acesso à tela
    Dado que o meu código de acesso não tem a tela C120C
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: RN-08 — tela fora do cadastro de telas
    Dado que a tela C120C não consta do cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: RN-08 — tela retirada do cadastro de telas
    Dado que a tela C120C foi retirada do cadastro de telas
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é passado adiante

  Cenário: RN-08 — sem permissão para a operação
    Dado que o meu código de acesso tem a tela C120C sem aquela operação liberada
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é passado adiante

  Cenário: RN-08 — a sessão está aberta em outra estação
    Dado que a minha sessão está aberta em outra estação
    Quando tento abrir a tela
    Então o acesso é encerrado e a tela não abre

  Cenário: RN-09 — falha do banco durante a consulta
    Dado que a leitura do cadastro falha no banco
    Quando confirmo a consulta
    Então a operação é interrompida com a mensagem de erro do sistema
    E a relação não é completada

  Cenário: RN-10 — a tela abre em consulta venha de onde vier
    Dado que chego à tela C120C pelo menu do caminho ou pela volta da C120T
    Quando a tela é exibida
    Então ela abre em consulta, na posição guardada da relação
    E não abre pedindo cadastro

  Cenário: RN-07 — a consulta não grava nada
    Dado que abri a tela e percorri a relação
    Quando confirmo a mensagem
    Então nenhum cadastro é gravado, alterado ou apagado
    E nenhum registro é travado
    E nenhuma trilha de auditoria é gerada
```
