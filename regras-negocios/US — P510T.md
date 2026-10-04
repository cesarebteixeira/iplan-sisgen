# US — P510T — Consulta dos anos de arquivo e atualização do número do arquivo

## Estória

Como **servidor de CRE com a tela P510T autorizada**, quero **conferir quais anos de
arquivo estão cadastrados e atualizar o número do arquivo de um deles**, para que **o
número que identifica o arquivo de cada ano fique correto no cadastro, sem precisar
recadastrar o ano**.

Cada ano de arquivo guarda, no cadastro, o número do arquivo daquele ano e a
quantidade de registros que ele reúne, e é por esse cadastro que se sabe quais anos
já têm arquivo e com que número. Esta tela é onde o servidor de CRE vê a lista
desses anos e troca o número de um ano que estiver errado — e a troca não é
anônima: fica registrada com o número anterior e o novo. No acervo desta jornada é
a única tela que grava esse cadastro; sem ela, um número errado só se resolveria
fora do sistema.

## Contexto

Jornada S000M → P000M → P500M → P510T.

Ator: servidor de CRE — nesta tela, confere os anos de arquivo cadastrados e atualiza
o número do arquivo do ano que assinalar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada — `P000M` e `P500M` — são menus: elas só
encaminham e não deixam dado de negócio para esta tela. O contexto que a `P510T`
usa — a matrícula, a CRE, o órgão, o código de acesso e a estação — é o que a
entrada deixou na sessão; a tela não recebe da `P500M` nenhum ano nem nenhum
empenho.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — Ao abrir, a tela mostra os anos de arquivo cadastrados

Abrir a tela não grava nada: ela lê o cadastro de anos de arquivo e mostra, uma por
linha, até quinze anos por vez, com o número do arquivo e a quantidade de registros
de cada ano. Não havendo nenhum ano cadastrado, a tela avisa
**\* Nao existem anos cadastrados \***, deixa o cursor no campo do número do
arquivo e encerra a operação sem mostrar linha nenhuma.

[?] A quantidade de registros que aparece em cada linha não vem do cadastro de anos
de arquivo: a tela monta essa coluna a partir de um dado do cadastro de processos
(o identificador usado no arquivo do ano), que ela não chega a ler. Ou a coluna
aparece com sobra de outra operação, ou o número vem de um caminho que não está nos
fontes desta jornada. Pergunta ao site.

### RN-02 — A tela só tem duas operações: consulta e alteração

A tela não inclui e não exclui: ela não cria ano de arquivo nenhum e não apaga ano
nenhum — esta tela não é por onde os anos entram ou saem do cadastro. Das operações
que ela chega a executar só existem duas, a consulta e a alteração; qualquer outra
opção é recusada com **\* Opcao nao disponivel. Use ALT ou CON \***, o cursor volta
para o campo da opção e nada é gravado.

[?] A recusa da opção, no próprio trecho que a emite, não marca a falha que
interromperia a mensagem (ao contrário dos avisos de acesso, que a marcam), e o
caminho que grava não consulta a opção, só a marca de ação da linha. Se o operador
assinalar uma linha e informar uma opção recusada, não foi possível determinar
pelos fontes se a gravação ainda acontece. Pergunta ao site.

### RN-03 — A consulta não altera nada

Com a opção de consulta, a tela apenas confere o acesso e responde: não atualiza,
não inclui e não exclui nada, ainda que alguma linha esteja assinalada. A consulta
também não exige autorização própria no código de acesso de quem opera — basta o
acesso à tela.

### RN-04 — A alteração é do ano assinalado, e só se ele estiver cadastrado

Para alterar, o operador assinala a linha do ano com a marca de ação da linha, a
mesma usada nas telas de manutenção do sistema. Só as linhas assinaladas e com o
ano informado são tratadas; as demais passam em branco, sem aviso. O ano assinalado
precisa estar cadastrado: não estando, a tela avisa **\* Ano nao cadastrado \***,
deixa o cursor na marca de ação daquela linha e não grava nada para ela. Linha
assinalada com outra marca — a de exclusão, por exemplo — é simplesmente ignorada:
esta tela não apaga.

### RN-05 — A alteração troca o número do arquivo do ano

Estando o ano cadastrado, a tela troca o número do arquivo daquele ano pelo número
que estiver na linha assinalada, e é o único dado do ano que ela altera: o ano e a
quantidade de registros permanecem como estavam. Se mais de uma linha estiver
assinalada, cada uma é tratada com a sua própria conferência e a sua própria
gravação.

[?] O cadastro admite mais de um registro para o mesmo ano, e a tela lê o registro
apenas pelo ano, sem distinguir as repetições: havendo dois registros do mesmo ano,
não foi possível determinar qual deles é o atualizado. Pergunta ao site.

### RN-06 — A alteração deixa registro de auditoria com o número anterior e o novo

Toda alteração feita pela tela é registrada na auditoria: ficam gravados a operação,
o cadastro alterado, o ano com o número anterior e o ano com o novo número, além de
quem operou, a CRE, o órgão, o terminal e o dia e a hora da sessão. O registro do
ano é travado antes da gravação.

[?] O registro de auditoria é pulado quando a mensagem está marcada como falha, mas
a gravação do cadastro não consulta essa marca: se a leitura do ano falhar e marcar
a falha, a atualização pode acontecer sem o registro de auditoria. Depende da rotina
comum de mensagem, que não está no lote. Pergunta ao site.

### RN-07 — Sem autorização de alteração, a tela não altera

A alteração exige que o código de acesso da matrícula tenha a alteração liberada
para esta tela; não tendo, a tela avisa **\* Acesso negado para esta operacao \***
e nada é gravado — a conferência é feita antes de ler e antes de gravar o ano.

### RN-08 — Nada acontece sem a tela e a matrícula habilitadas

Antes de qualquer operação, inclusive ao abrir a tela, o sistema confere, com o
contexto da sessão, se a tela está cadastrada — não estando, a recusa é
**\* Tela nao disponivel \*** —, se a matrícula tem a tela no seu código de acesso
— não tendo, a recusa é **\* Acesso negado para esta matricula \*** — e passa a
operação pela lógica de rota, que recusa a opção que a tela não reconhece
(**\* Operacao nao disponivel \***) e a tela que foi retirada do cadastro
(**\* Tela nao cadastrada \***).

### RN-09 — A lista é de quinze em quinze e retoma de onde parou

Cada abertura mostra até quinze anos. O último ano mostrado fica como ponto de
partida da abertura seguinte, e quando a lista alcança o fim do cadastro a abertura
seguinte recomeça do primeiro ano.

[?] O significado dos sinalizadores da leitura posicionada deste dialeto não está no
corpus — o recurso vem de fora do acervo. A lista pode começar no primeiro ano
cadastrado, ou a leitura pode ser a exata do ano de partida, que é zero na primeira
abertura: disso depende a tela mostrar os anos ou não mostrar nenhum. Pergunta ao
site.

### RN-10 — A resposta à mensagem sai sem a data do sistema e sem a descrição do órgão

Ao abrir, a tela mostra a data do sistema e a descrição do órgão da sessão. A cada
mensagem respondida, esses dois campos são apagados antes de qualquer conferência e
não são repostos: a resposta sai com eles em branco.

[?] Essa limpeza está amarrada a um tipo de mensagem que o acervo não explica; se
existe um caminho de entrada em que os campos não são limpos, não foi possível
determinar. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consulta dos anos de arquivo e atualização do número do arquivo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela P510T

  Cenário: Abertura mostra os anos de arquivo cadastrados
    Dado que existem anos de arquivo cadastrados
    Quando abro a tela P510T
    Então vejo os anos cadastrados, um por linha, com o número do arquivo e a quantidade de registros de cada um
    E nada é gravado

  Cenário: Nenhum ano de arquivo cadastrado
    Dado que não existe ano de arquivo cadastrado
    Quando abro a tela P510T
    Então vejo a mensagem "* Nao existem anos cadastrados *"
    E o cursor fica no campo do número do arquivo
    E nada é gravado

  Cenário: A consulta não grava nada
    Dado que existem anos de arquivo cadastrados
    Quando informo a opção de consulta
    Então a tela confere o meu acesso e responde
    E nenhum ano é atualizado, incluído ou excluído

  Cenário: Opção diferente de consulta e alteração é recusada
    Dado que existem anos de arquivo cadastrados
    Quando informo uma opção que não é a de consulta nem a de alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo da opção
    E nada é gravado

  Cenário: Atualização do número do arquivo do ano assinalado
    Dado que existe o ano de arquivo informado
    E assinalo a linha desse ano com a marca de alteração
    Quando confirmo a mensagem com a opção de alteração
    Então o número do arquivo desse ano passa a ser o número mostrado na linha
    E o ano e a quantidade de registros ficam como estavam
    E a alteração fica registrada na auditoria com o número anterior e o novo

  Cenário: Mais de uma linha assinalada é atualizada
    Dado que existem dois anos de arquivo informados e cadastrados
    E assinalo as duas linhas com a marca de alteração
    Quando confirmo a mensagem com a opção de alteração
    Então o número do arquivo dos dois anos é atualizado
    E cada alteração fica registrada na auditoria

  Cenário: Alteração de ano não cadastrado é recusada
    Dado que o ano informado na linha assinalada não está cadastrado
    Quando confirmo a mensagem com a opção de alteração
    Então vejo a mensagem "* Ano nao cadastrado *"
    E o cursor fica na marca de ação dessa linha
    E nada é gravado para esse ano

  Cenário: Linhas não assinaladas não são alteradas
    Dado que existem anos cadastrados e só uma linha está assinalada
    Quando confirmo a mensagem com a opção de alteração
    Então só o número do arquivo do ano assinalado é atualizado
    E os demais anos ficam como estavam

  Cenário: Linha assinalada para exclusão é ignorada
    Dado que assinalo uma linha com a marca de exclusão
    Quando confirmo a mensagem com a opção de alteração
    Então o ano dessa linha não é excluído
    E nada é gravado para essa linha

  Cenário: Sem autorização de alteração
    Dado que o meu código de acesso tem a tela P510T sem a alteração liberada
    Quando confirmo a mensagem com a opção de alteração e uma linha assinalada
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E o número do arquivo não é atualizado

  Cenário: A lista é de quinze em quinze e retoma do último ano mostrado
    Dado que existem mais anos cadastrados do que cabem em uma tela
    Quando abro a tela P510T
    Então vejo os primeiros quinze anos
    E ao reabrir a tela a lista continua a partir do último ano mostrado
    E ao alcançar o fim do cadastro a próxima abertura recomeça do primeiro ano

  Cenário: A resposta à mensagem sai sem a data do sistema e sem a descrição do órgão
    Dado que a tela abriu mostrando a data do sistema e a descrição do órgão
    Quando respondo uma mensagem
    Então a resposta vem com esses dois campos em branco

  Cenário: Tela não cadastrada
    Dado que a tela P510T não está no cadastro de telas e relatórios
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela P510T no seu código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Opção não reconhecida
    Dado que informo uma opção que a tela não reconhece
    Quando confirmo a mensagem
    Então vejo a mensagem "* Operacao nao disponivel *"

  Cenário: Tela retirada do cadastro
    Dado que a tela P510T foi retirada do cadastro de telas e relatórios
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"
```
