# US — C054T — Manter o relacionamento dos gêneros orgânicos e o acréscimo sobre o preço

## Estória

Como **servidor da CRE que mantém o cadastro de gêneros**, quero **registrar, alterar
ou retirar, para cada gênero orgânico já cadastrado, o gênero com que ele se relaciona
e o percentual de acréscimo sobre o preço**, para que **o cadastro dos gêneros
orgânicos fique com o relacionamento e o acréscimo vigentes de cada um**.

O gênero orgânico é o gênero que o cadastro de gêneros marca como orgânico; o
relacionamento com um segundo gênero e o percentual de acréscimo sobre o preço são
dados desse gênero, e é esta tela que os mantém. Sem eles, o gênero orgânico fica sem
o relacionamento vigente e o acréscimo praticado não tem onde ser registrado. Esta
tela não cria nem tira o gênero orgânico do cadastro — quem faz isso é o cadastro de
gêneros — e retirar o relacionamento aqui **não** apaga o gênero: deixa-o sem
relacionamento.

## Contexto

Jornada S000M → C000M → C055M → C054T.

Ator: servidor de CRE — mantém o relacionamento e o acréscimo dos gêneros orgânicos
da sua secretaria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas do meio são menus — têm opções e só encaminham; nenhuma delas grava
nada. Esta tela também não encaminha nada adiante: a jornada termina nela, e ela não
muda de comportamento conforme a tela que a chamou, porque não lê o código da tela de
origem. O que ela aproveita da sessão é o **vínculo do servidor com a secretaria** —
matrícula, acesso, privilégio, tipo de órgão e CRE —, que é regra da entrada e está no
anexo de evidências.

A lista que esta tela mantém é a dos gêneros orgânicos já reconhecidos pelo cadastro
de gêneros; quem cria e quem apaga esse reconhecimento é o cadastro de gêneros (a
tela C050T do mesmo menu), não esta tela.

## Regras de negócio

### RN-01 — A tela mantém o relacionamento do gênero orgânico e o acréscimo sobre o preço

A tela registra, para um gênero orgânico já cadastrado, o **gênero com que ele se
relaciona** e o **percentual de acréscimo sobre o preço**; altera o que já está
gravado; e exclui — o que, aqui, quer dizer **deixar o relacionamento em branco**.
Excluir não apaga o gênero orgânico e não tira o reconhecimento dele do cadastro: o
registro continua, sem relacionamento.

### RN-02 — A tela não cria o gênero orgânico; sem o reconhecimento dele, nada é gravado e nada é avisado

A tela só grava sobre o gênero orgânico que o cadastro de gêneros já reconheceu. A
gravação relê o reconhecimento daquele gênero e, não o encontrando, termina sem gravar
e **sem mensagem**.

[?] O reconhecimento do gênero orgânico é criado pelo cadastro de gêneros quando o
gênero passa a orgânico, e apagado quando ele deixa de ser; o estado "gênero orgânico
sem reconhecimento" só deveria existir por dado antigo ou por falha. O que a tela faz
nesse caso, além do silêncio do caminho de gravação, o acervo não diz. Pergunta ao
site.

### RN-03 — A tela lista os gêneros orgânicos, sete por vez, na ordem do código

A lista é montada a partir do **reconhecimento dos gêneros orgânicos**, na ordem do
código — classe, subclasse e gênero —, **sete linhas por vez**; a tela preenche as
linhas uma a uma, sem que o servidor peça cada uma, e guarda a **posição em que a
leitura parou**, que ela mostra fora da lista. Terminada a lista, a posição é zerada. A
mesma medida de sete linhas vale para a conferência.

### RN-04 — Quando não há nenhum gênero orgânico, a tela avisa

Abrindo sobre um cadastro sem nenhum gênero orgânico, a tela avisa
**\* Nao existem generos organicos cadastrados \*** e nenhuma linha é preenchida.

### RN-05 — O que a tela mostra em cada linha, e a posição da leitura

Cada linha traz o **código de classe, a subclasse e o gênero** do gênero orgânico e o
**nome do gênero**; o **relacionamento** — classe, subclasse e gênero — e o **nome do
gênero relacionado**; o **percentual de acréscimo**, com duas casas; e a **ação** da
linha. Fora da lista, a tela mostra a **data do sistema**, o **tipo de órgão da
sessão** e a **posição em que a leitura parou**: classe, subclasse e gênero.

[?] O rótulo **NMFUNCINI** aparece sobre o campo que guarda a **subclasse da posição
de leitura**, e no mesmo acervo esse rótulo aparece em outras telas sobre outros
campos, inclusive um nome de servidor. O que ele nomeia aqui, em negócio, não está no
acervo. Pergunta ao site.

[?] A posição da leitura é editável como os demais campos, mas a tela relê a lista
pela posição que ela mesma guardou, não pela que foi digitada. Se o que o servidor
digita ali muda a leitura — e como —, o acervo não diz. Pergunta ao site.

### RN-06 — A tela só trabalha em alteração ou consulta

A opção de manutenção aceita **alteração** e **consulta**; sem opção informada, a tela
assume **consulta**. Qualquer outra opção é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta no campo da
opção, e a tela não segue.

[?] A recusa fala em ALT e CON e a comparação é com os mnemônicos internos de
alteração e de consulta; a correspondência entre o texto e os mnemônicos vem da
própria mensagem e não se confirma no acervo desta jornada. Pergunta ao site.

[?] A opção informada fica guardada na área de trabalho da tela, que o acervo
inicializa uma única vez por instância do programa; se essa área não sobrevive entre
transações, a opção guardada e a posição da leitura voltam ao início a cada chamada. O
acervo não define a vida da área comum. Pergunta ao site.

### RN-07 — A consulta não grava nada

Em **consulta**, a tela apenas monta e exibe a lista: não passa pelas conferências de
linha, não grava o relacionamento, não trava registro nenhum e não deixa rastro na
auditoria.

### RN-08 — A ação é de cada linha: incluir, alterar e excluir

A operação se decide **linha a linha**, pela letra que o servidor informa na ação:
**I** inclui o relacionamento, **A** altera o que já está gravado e **E** exclui
(limpa). Linha **sem o gênero relacionado** é ignorada, e ação **diferente de I, A e
E** também — silenciosamente, sem mensagem. A tela percorre as sete linhas conferindo
e só depois volta a elas para gravar, linha a linha.

[?] A recusa mostra a mensagem e manda a tela para o fim da sua lógica; o que impede a
gravação depois disso é o marcador de erro do sistema, que a rotina de mensagem
preenche — e essa rotina não está no acervo. Se a recusa de uma linha impede mesmo a
gravação dela, pergunta ao site.

### RN-09 — Incluir exige que o gênero orgânico ainda não tenha relacionamento

Na inclusão, a tela relê o gênero orgânico da linha e **recusa se ele já tem
relacionamento**: **\* Relacionamento ja cadastrado \***. A tela considera que não há
relacionamento quando o código de **subclasse** do relacionamento está em branco — que
é o estado em que o cadastro de gêneros deixa o gênero orgânico novo.

[?] A conferência olha só a subclasse do relacionamento; um relacionamento gravado com
a subclasse zerada passaria como "sem relacionamento" e seria aceito de novo. O
cadastro de gêneros cria o reconhecimento com os quatro dados do relacionamento
zerados, mas o acervo não diz se o estado parcial — só a subclasse em branco — existe.
Pergunta ao site.

### RN-10 — O gênero relacionado tem de estar cadastrado, ativo e não ser orgânico

O gênero informado como relacionamento é procurado no **cadastro de gêneros** pelo par
**subclasse e gênero**, e passa por três peneiras: tem de **existir** — senão
**\* Genero do relacionamento nao cadastrado \***; estar **ativo** — senão
**\* Genero do relacionamento inativo \***; e **não ser orgânico** — senão
**\* Genero do relacionamento cad como organico \***. A alteração repete as três
conferências.

### RN-11 — O acréscimo sobre o preço é obrigatório e não passa de 30%

O **percentual de acréscimo sobre o preço** tem de ser informado — em branco, a recusa
é **\* Informe o % de acrescimo para o preco \*** — e **não pode passar de 30%** —
passando, **\* Acrescimo maior que 30% \***. Vale para incluir e para alterar; a
exclusão não confere percentual, porque ela o deixa em branco.

[?] O acréscimo é gravado por esta tela e não é lido por nenhum outro programa do
acervo: fora da trilha de auditoria, o percentual não reaparece em lugar nenhum. O que
ele altera no preço, e quem o aplica, não está no acervo. Pergunta ao site.

### RN-12 — A classe do relacionamento vem do cadastro do gênero relacionado

A classe do relacionamento **não é a que se digita na linha**: a tela usa a **classe do
gênero relacionado**, lida do cadastro de gêneros. É essa classe que vai para o
relacionamento gravado.

[?] A classe do relacionamento aparece na linha e passa pela edição numérica, como se
fosse digitável, mas a tela sempre a substitui pela do cadastro. Ou o campo serve de
conferência, ou o que o servidor digita é ignorado. Pergunta ao site.

### RN-13 — Toda operação fica na trilha, como alteração do cadastro do gênero

Incluir, alterar e excluir deixam, cada um, um registro na **trilha de auditoria**: o
cadastro de origem (o reconhecimento do gênero orgânico), a **operação** — as três
entram como **alteração** —, o código do gênero, a matrícula, a estação, o tipo de
órgão, a sessão (dia, mês, ano e hora) e as imagens **anterior** e **posterior** do
relacionamento. A trilha é gravada **antes** do relacionamento.

[?] Como a trilha é gravada antes do cadastro, uma falha na gravação do relacionamento
deixa na trilha uma operação que não chegou a acontecer. Pergunta ao site.

### RN-14 — A tela grava no reconhecimento do gênero orgânico e na trilha; não apaga registro nenhum

A tela declara, para cada cadastro que enxerga, as rotinas de incluir, de apagar e de
travar — declaração, não uso. Dos **quatro** cadastros que ela enxerga, **dois** são
só de leitura (o cadastro de telas e o cadastro de gêneros) e **dois recebem
gravação**: o reconhecimento dos gêneros orgânicos e a trilha. **Nenhuma** rotina de
apagar é executada por caminho nenhum.

### RN-15 — Antes de operar, a tela confere o perfil, a rota e a permissão da operação

A tela chama as rotinas comuns de segurança: a de **perfil**, na exibição, e as de
**rota** e de **permissão por operação**, na conferência. A conferência recebe o
vínculo da sessão (matrícula, acesso, privilégio, tipo de órgão e CRE) e o código da
tela de destino que a sessão carrega. Retorno diferente de OK limpa o status e
interrompe a tela.

[?] A regra efetiva de permissão por perfil e por operação não está no acervo: as
rotinas aparecem só declaradas e a tela apenas testa o retorno. O mesmo vale para o
código da tela de destino: com ele preenchido, a conferência é encerrada sem conferir
as linhas, e o acervo não diz em que situação a sessão o preenche. Pergunta ao site.

### RN-16 — Falha no banco interrompe a operação e avisa

Erro de banco na leitura ou na gravação interrompe a operação e a tela avisa; o
relacionamento não é considerado gravado.

## Cenários BDD

```gherkin
Funcionalidade: Manter o relacionamento dos gêneros orgânicos e o acréscimo sobre o preço

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C054T

  Cenário: RN-03 — a lista dos gêneros orgânicos, sete por vez
    Dado que existem gêneros orgânicos cadastrados
    Quando abro a tela C054T
    Então vejo até sete gêneros orgânicos, na ordem do código
    E a tela mostra a posição em que a leitura parou

  Cenário: RN-05 — o que a tela mostra em cada linha
    Dado que a lista tem gêneros orgânicos
    Quando a tela exibe a lista
    Então cada linha traz a classe, a subclasse, o gênero e o nome do gênero
    E traz a classe, a subclasse, o gênero e o nome do gênero relacionado
    E traz o percentual de acréscimo com duas casas e a ação da linha
    E a tela mostra a data do sistema e o tipo de órgão da sessão

  Cenário: RN-04 — não há nenhum gênero orgânico cadastrado
    Dado que não há nenhum gênero orgânico cadastrado
    Quando abro a tela C054T
    Então vejo "* Nao existem generos organicos cadastrados *"
    E nenhuma linha é preenchida

  Cenário: RN-07 — a consulta não grava nada
    Dado que estou na tela C054T em consulta
    Quando confirmo
    Então vejo a lista dos gêneros orgânicos com o relacionamento de cada um
    E nada é gravado, nenhum registro é travado e nenhuma trilha é deixada

  Cenário: RN-06 — opção de manutenção não disponível
    Dado que estou na tela C054T
    Quando informo uma opção de manutenção diferente de alteração e de consulta
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo da opção

  Cenário: RN-08, RN-09, RN-10, RN-11 e RN-13 — incluir o relacionamento de um gênero orgânico
    Dado que o gênero orgânico ainda não tem relacionamento
    E o gênero relacionado está cadastrado, está ativo e não é orgânico
    Quando informo a ação I na linha, com o gênero relacionado e o acréscimo
    E confirmo
    Então o relacionamento e o acréscimo ficam gravados para aquele gênero orgânico
    E a operação fica na trilha, como alteração do cadastro do gênero

  Cenário: RN-08, RN-12 e RN-13 — alterar o relacionamento de um gênero orgânico
    Dado que o gênero orgânico já tem relacionamento
    Quando informo a ação A na linha, troco o gênero relacionado e o acréscimo
    E confirmo
    Então o relacionamento gravado passa a ser o novo
    E a classe do relacionamento é a que está no cadastro do gênero relacionado
    E a operação fica na trilha, como alteração do cadastro do gênero

  Cenário: RN-01, RN-08 e RN-13 — excluir o relacionamento de um gênero orgânico
    Dado que o gênero orgânico tem relacionamento
    Quando informo a ação E na linha
    E confirmo
    Então o relacionamento e o acréscimo daquele gênero ficam em branco
    E o gênero orgânico continua no cadastro e na lista, sem relacionamento
    E a operação fica na trilha, como alteração do cadastro do gênero

  Cenário: RN-08 — linha sem o gênero relacionado ou com ação desconhecida
    Dado que deixo a linha sem o gênero relacionado ou informo uma ação diferente de I, A e E
    Quando confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada

  Cenário: RN-09 — incluir num gênero orgânico que já tem relacionamento
    Dado que o gênero orgânico da linha já tem relacionamento
    Quando informo a ação I na linha e confirmo
    Então vejo "* Relacionamento ja cadastrado *"
    E o cursor volta para o campo do relacionamento

  Cenário: RN-10 — gênero relacionado não cadastrado
    Dado que o gênero informado como relacionamento não está no cadastro de gêneros
    Quando informo a ação I ou A na linha e confirmo
    Então vejo "* Genero do relacionamento nao cadastrado *"

  Cenário: RN-10 — gênero relacionado inativo
    Dado que o gênero informado como relacionamento está cadastrado como inativo
    Quando informo a ação I ou A na linha e confirmo
    Então vejo "* Genero do relacionamento inativo *"

  Cenário: RN-10 — gênero relacionado cadastrado como orgânico
    Dado que o gênero informado como relacionamento é um gênero orgânico
    Quando informo a ação I ou A na linha e confirmo
    Então vejo "* Genero do relacionamento cad como organico *"

  Cenário: RN-11 — acréscimo não informado
    Dado que deixo o percentual de acréscimo em branco
    Quando informo a ação I ou A na linha e confirmo
    Então vejo "* Informe o % de acrescimo para o preco *"

  Cenário: RN-11 — acréscimo maior que 30%
    Dado que informo um percentual de acréscimo maior que 30%
    Quando informo a ação I ou A na linha e confirmo
    Então vejo "* Acrescimo maior que 30% *"

  Cenário: RN-02 — gênero orgânico sem reconhecimento no cadastro
    Dado que o gênero da linha não tem reconhecimento no cadastro de gêneros
    Quando informo a ação I ou A na linha e confirmo
    Então nada é gravado para aquele gênero
    E nenhuma mensagem é mostrada

  Cenário: RN-14 — o que a tela grava
    Dado que faço uma inclusão, uma alteração e uma exclusão
    Quando o sistema processa cada operação
    Então só o reconhecimento dos gêneros orgânicos e a trilha recebem gravação
    E nenhum registro é apagado

  Cenário: RN-15 — sem permissão para a operação
    Dado que não tenho permissão para esta operação nesta tela
    Quando confirmo
    Então a tela não opera
    E nada é gravado

  Cenário: RN-16 — falha do banco durante a gravação
    Dado que a gravação do relacionamento falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com o aviso de erro do sistema
    E o relacionamento não é considerado gravado
```
