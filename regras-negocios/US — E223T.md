# US — E223T — Registrar as notas fiscais das entregas do pedido acumulado

## Estória

Como **servidor de CRE**, quero **registrar a nota fiscal e a quantidade recebida de
cada pedido que compõe um pedido acumulado e pedir a relação das entregas na
impressora**, para que **cada entrega fique comprovada no sistema e a CRE saiba o que
já foi entregue do que foi pedido**.

O pedido acumulado reúne num só documento vários pedidos do mesmo gênero, feitos a um
fornecedor para entrega dentro de um período. Quem recebe a mercadoria precisa lançar,
pedido a pedido, a nota fiscal que a acompanhou e a quantidade que efetivamente
chegou; sem esse lançamento o acumulado fica marcado como não entregue, a CRE não
consegue comprovar o que já entrou nem cobrar do fornecedor o que faltou, e o
acumulado não fecha. É também por aqui que a CRE tira a relação das entregas do
acumulado, com o que foi pedido e o que foi recebido, para conferência em papel.

## Contexto

Jornada S000M → E000M → E200M → E220M → E223T.

Ator: servidor de CRE — informa o órgão filho, a coordenadoria regional escolar, o
pedido acumulado (número do pedido e ano da entrega) e o gênero, lança a nota fiscal
e a quantidade recebida de cada pedido do acumulado e, quando quer o papel, informa a
impressora.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Das telas anteriores a tela usa o que a entrada deixou na sessão: a matrícula, o
código de acesso, o privilégio, o tipo de órgão, a coordenadoria regional escolar e o
órgão filho do vínculo. Ela não abre outra tela: termina nela mesma.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela lança a nota fiscal das entregas do acumulado e emite a relação das entregas

A tela serve a duas coisas. A primeira é lançar a entrega: para cada pedido que
compõe o pedido acumulado, a nota fiscal que a acompanhou, a data de emissão dessa
nota e a quantidade recebida, com a operação pretendida naquela linha — incluir,
alterar ou excluir a nota. A segunda é pedir a impressão da relação das entregas
daquele acumulado, com a quantidade pedida e a recebida de cada pedido e os totais.

As duas coisas não acontecem na mesma passagem. Com a impressora informada a tela
emite a relação e **não** grava nota nenhuma; sem impressora ela grava a nota e
**não** emite. A tela não avisa o operador de que a gravação foi deixada de lado por
causa da impressora, e também não deixa trilha de auditoria da emissão.

[?] A impressora é o que decide entre emitir e gravar, mas esse campo não tem rótulo
de negócio no programa nem é conferido por ele, e a máscara da tela não veio no lote:
não se conclui daqui como o operador informa a impressora, nem se a exclusividade
entre emitir e gravar é o que o site espera — do jeito que está, quem pede o papel na
mesma passagem em que lançou as notas não grava nenhuma delas, sem aviso. Pergunta ao
site.

### RN-02 — A tela não mantém o pedido: consulta dez cadastros e grava em três

Para montar a tela e conferir a transação ela consulta **dez** cadastros: o das telas,
o dos servidores (para o correio eletrônico), o dos órgãos, o dos fornecedores, o dos
operadores logísticos, o dos gêneros, o dos pedidos, o dos itens de pedido, o das
entregas com nota fiscal e a fila de requisições de impressão. Grava em **três**: a
entrega com a nota fiscal, a trilha de auditoria e a fila de requisições de impressão.
Nenhum outro cadastro é incluído, alterado ou excluído — em particular, a tela **não**
altera o pedido acumulado nem os seus itens: a composição do acumulado vem de fora.

### RN-03 — Ao abrir, a tela entra em consulta e não mostra pedido nenhum até que o acumulado seja consultado

Na primeira abertura a tela se coloca sozinha em modo de consulta e termina a passagem
sem exibir pedido algum, porque ainda não há um acumulado em contexto. O acumulado
entra em contexto quando o operador informa a chave e consulta: é a consulta que
guarda o órgão, a coordenadoria, o pedido, o gênero e o período, e é dela que a
exibição seguinte se serve. Abrir a tela não grava nem emite nada.

### RN-04 — A consulta exige órgão filho, pedido com ano de entrega, subclasse e gênero, e confere cada um deles

Para consultar, são obrigatórios o órgão filho, o número do pedido com o ano da
entrega, a subclasse e o gênero. O órgão filho tem de estar cadastrado e não excluído,
tem de pertencer ao tipo de órgão da sessão e, quando o vínculo do servidor carrega uma
coordenadoria regional escolar, tem de estar na coordenadoria dele. O pedido tem de
estar cadastrado, tem de ser um pedido acumulado — **não** serve um acumulado calculado
nem um pedido auxiliar de acumulado calculado — e tem de ser do órgão filho do vínculo,
quando o vínculo tem um. A coordenadoria informada tem de ser a do órgão: o pedido é
procurado com ela e, na alteração, ela é comparada com a do órgão. O gênero tem de
estar cadastrado no sistema e tem de existir naquele pedido acumulado.

Cada conferência tem a sua recusa, com o cursor no campo culpado: **\* Informe o orgao
\***, **\* Orgao nao cadastrado \***, **\* Orgao nao pertence a esta secretaria \***,
**\* Usuario sem acesso ao grupo deste orgao \***, **\* Informe o numero do pedido \***,
**\* Pedido nao cadastrado \***, **\* Pedido nao acumulado \***, **\* Pedido acumulado
calculado \***, **\* Pedido auxiliar do acumulado calculado \***, **\* Pedido de outro
orgao \***, **\* Informe o genero \***, **\* Genero nao cadastrado \*** e **\* Genero
nao cadastrado neste pedido \***. Quando o acumulado está cadastrado mas não tem
pedido nenhum, a recusa é **\* Nao existem pedidos cadastrados \***.

### RN-05 — A tela só aceita as operações de alteração e de consulta

A transação só é aceita como consulta (CON) ou como alteração (ALT). Qualquer outra
operação — inclusive inclusão e exclusão do documento — é recusada com **\* Opcao nao
disponivel. Use ALT ou CON \***, com o cursor no campo do código de manutenção. O que
se inclui, se altera ou se exclui é a nota fiscal de cada linha, não o pedido.

[?] O código de manutenção chega pronto na transação e quem o monta é a máscara da
tela, que não veio no lote; o programa só o repõe para consulta na primeira abertura.
Se a máscara manda inclusão ou exclusão, a tela nunca deixa passar — e não se conclui
daqui o que o site espera. Pergunta ao site.

### RN-06 — A alteração exige a consulta prévia do mesmo acumulado, do mesmo gênero e da mesma coordenadoria

A alteração só passa quando a coordenadoria, o pedido acumulado, a subclasse e o
gênero informados são exatamente os que a consulta anterior deixou em contexto. Se
qualquer um deles for diferente, a alteração é recusada com **\* Consulte antes de
atualizar \***, com o cursor no código de manutenção, e nada é gravado.

### RN-07 — Cada linha do acumulado traz a operação da sua nota fiscal

A tela lista os pedidos que compõem o acumulado, um por linha, com o número do pedido
e o ano da entrega, o número e a data de emissão da nota fiscal, a quantidade recebida
e a operação pretendida na linha: incluir, alterar ou excluir a nota fiscal. A
quantidade pedida daquele pedido também aparece, ao lado da recebida, e a tela fecha
com o total pedido e o total recebido do acumulado. Cada página mostra até onze
linhas. Linha em branco ou sem número de pedido é ignorada em silêncio: nem recusa nem
grava.

[?] O significado das letras que marcam a operação da linha não está tabelado no
acervo; a leitura vem das próprias recusas (a inclusão recusa nota **já** cadastrada,
a alteração e a exclusão recusam nota **não** cadastrada) e dos caminhos que gravam. Se
o site usa outras letras na máscara, não se conclui daqui. Pergunta ao site.

### RN-08 — Incluir a nota fiscal de um pedido do acumulado

Para incluir a nota de um pedido, a nota fiscal é obrigatória — em branco, a recusa é
**\* Informe nota fiscal \*** —, o pedido tem de ser um dos que compõem aquele
acumulado (senão **\* Pedido nao cadastrado neste acumulado \***) e a nota **não** pode
já estar lançada para aquele pedido (senão **\* Nota fiscal ja cadastrada \***). A
soma das demais notas daquele item não pode já cobrir o total pedido (senão
**\* Quantidade total entregue \***). A data de emissão da nota não pode ser anterior
à data do pedido (senão **\* Data da nota < data do pedido \***). A quantidade
recebida é obrigatória (senão **\* Informe a quantidade recebida \***) e a soma do que
já foi recebido com ela não pode ultrapassar a quantidade pedida (senão
**\* Quantidade recebida > pedida \***). Passando por tudo, a nota é gravada no
registro de entrega daquele pedido.

### RN-09 — Alterar a nota fiscal de um pedido do acumulado

Para alterar, a nota tem de existir no registro de entrega daquele pedido do
acumulado: nota em branco recusa com **\* Informe nota fiscal \***, pedido fora do
acumulado recusa com **\* Pedido nao cadastrado neste acumulado \*** e nota não
lançada recusa com **\* Nota fiscal nao cadastrada \***. As mesmas conferências de
data, de quantidade recebida obrigatória e de não ultrapassar a quantidade pedida são
feitas contra as **outras** notas daquele item, e a nota e a quantidade informadas
substituem as anteriores.

### RN-10 — Excluir a nota fiscal de um pedido do acumulado

Para excluir, a nota tem de existir naquele pedido do acumulado: as recusas são
**\* Informe nota fiscal \***, **\* Pedido nao cadastrado neste acumulado \*** e
**\* Nota fiscal nao cadastrada \***. Apagada a nota, o destino do registro de entrega
depende do que sobra: se aquele item tem **outras** notas lançadas, o registro daquele
pedido é apagado; se era a **única** nota do item, o registro permanece e fica sem
nota, sem data e sem quantidade.

[?] O que um registro de entrega sem nota representa depois disso não está no acervo —
e é justamente o estado que a inclusão aproveita para receber uma nota nova. Se a
intenção era tirar a entrega de vez, o registro não sai. Pergunta ao site.

### RN-11 — A relação das entregas sai pela impressora informada, uma cópia, e não pode haver pedido pendente do mesmo relatório

Quando a impressora é informada, a tela pede a impressão da relação das entregas
daquele acumulado e daquele gênero, em **uma cópia**, para a impressora indicada, e
entrega o trabalho ao processamento em lote. A emissão exige que o servidor tenha
correio eletrônico cadastrado (senão **\* Usuario sem e-mail cadastrado \***) e que não
haja pedido de impressão pendente daquele relatório para o mesmo órgão e a mesma
coordenadoria (senão **\* Relatorio ja esta em processamento. Aguarde. \***, com o
cursor no número do pedido). A requisição fica na fila de requisições de impressão, com
o próximo número da fila, a matrícula, o terminal e o tipo de órgão da sessão.

[?] Quem executa o trabalho entregue à impressão não está no acervo com o nome que a
tela usa: o programa de lote da relação das entregas existe, recebe exatamente o
acumulado e o gênero como parâmetro e é o candidato, mas a ligação entre o nome do
trabalho e esse programa não está no lote. Também não se conclui daqui o que acontece
fora do ambiente previsto: nesse caso a requisição fica na fila e o trabalho não é
entregue. Pergunta ao site.

### RN-12 — Toda gravação de nota fiscal deixa trilha de auditoria; a emissão não deixa

Cada nota incluída, alterada ou excluída gera um registro de auditoria com a operação
(foi incluída, foi alterada, foi excluída), a imagem anterior e a posterior, a tela, a
coordenadoria, o número de processo (o acumulado), a matrícula, o terminal e a data e a
hora da sessão. A emissão da relação das entregas **não** deixa registro de auditoria.

### RN-13 — A abertura, a consulta e qualquer recusa não gravam nada

A abertura da tela e a consulta só leem. Toda recusa termina a passagem antes das
gravações: nenhuma nota, nenhuma auditoria e nenhuma requisição de impressão é gravada
quando a transação é recusada — inclusive quando a recusa é a de relatório já em
processamento.

### RN-14 — A transação passa pela conferência de sessão, de tela, de rota e de operação

Antes de exibir ou de gravar, a tela lê o cadastro de telas pela tela e pelo terminal e
submete a transação à conferência de sessão e tela, e, na confirmação, à conferência de
rota e à de operação, repassando a matrícula, o código de acesso, o privilégio, o tipo
de órgão e a coordenadoria da sessão. Nenhuma dessas conferências deixa a transação
seguir quando não está liberada, e a tela se declara tela de manutenção, de modo que a
permissão de operação do código de acesso é exigida.

## Cenários BDD

```gherkin
Funcionalidade: Registrar as notas fiscais das entregas do pedido acumulado

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E223T

  Cenário: Consultar um pedido acumulado e ver os pedidos que o compõem
    Dado que o acumulado 123456/2024 do órgão filho 00000123 existe e tem dois pedidos
    Quando informo a coordenadoria do órgão, o número do pedido, o ano da entrega e o gênero e confirmo a consulta
    Então a tela mostra os pedidos do acumulado, com a quantidade pedida e a recebida de cada um
    E mostra o total pedido e o total recebido
    E não grava nada

  Cenário: A primeira abertura não mostra pedido nenhum
    Dado que acabei de abrir a tela e ainda não consultei acumulado nenhum
    Então a tela fica em modo de consulta e não exibe pedido algum
    E não grava nada

  Cenário: A consulta exige o órgão filho
    Quando confirmo a consulta sem informar o órgão filho
    Então a tela recusa com "* Informe o orgao *"
    E o cursor volta ao campo do órgão filho

  Cenário: A consulta exige o número do pedido
    Quando informo o órgão filho e confirmo a consulta sem o número do pedido
    Então a tela recusa com "* Informe o numero do pedido *"

  Cenário: A consulta exige o gênero
    Quando informo o órgão filho, o pedido e o ano da entrega e confirmo sem a subclasse
    Então a tela recusa com "* Informe o genero *"

  Cenário: Órgão filho fora do cadastro, de outra secretaria ou de outra coordenadoria
    Quando informo um órgão filho que não está cadastrado
    Então a tela recusa com "* Orgao nao cadastrado *"
    Quando informo um órgão filho de outra secretaria
    Então a tela recusa com "* Orgao nao pertence a esta secretaria *"
    Quando informo um órgão filho de coordenadoria diferente da minha
    Então a tela recusa com "* Usuario sem acesso ao grupo deste orgao *"

  Cenário: Pedido que não serve para esta tela
    Quando informo um pedido que não existe
    Então a tela recusa com "* Pedido nao cadastrado *"
    Quando informo um pedido que não é acumulado
    Então a tela recusa com "* Pedido nao acumulado *"
    Quando informo um acumulado calculado
    Então a tela recusa com "* Pedido acumulado calculado *"
    Quando informo um pedido auxiliar de acumulado calculado
    Então a tela recusa com "* Pedido auxiliar do acumulado calculado *"
    Quando informo um pedido de outro órgão
    Então a tela recusa com "* Pedido de outro orgao *"

  Cenário: Gênero fora do cadastro ou fora do pedido
    Quando informo um gênero que não está cadastrado
    Então a tela recusa com "* Genero nao cadastrado *"
    Quando informo um gênero que não está naquele pedido acumulado
    Então a tela recusa com "* Genero nao cadastrado neste pedido *"

  Cenário: Acumulado sem pedidos
    Quando consulto um acumulado que não tem pedido nenhum
    Então a tela recusa com "* Nao existem pedidos cadastrados *"

  Cenário: Operação diferente de alteração e de consulta
    Quando chego à tela com a operação de inclusão
    Então a tela recusa com "* Opcao nao disponivel. Use ALT ou CON *"

  Cenário: Alterar sem consultar antes
    Dado que consultei o acumulado 123456/2024
    Quando altero o gênero informado e confirmo a alteração
    Então a tela recusa com "* Consulte antes de atualizar *"
    E não grava nada

  Cenário: Incluir a nota fiscal de um pedido do acumulado
    Dado que consultei o acumulado 123456/2024, do gênero 00001/00002, com um pedido
    E que esse pedido ainda não tem nota lançada
    Quando informo na linha a nota fiscal 987654, a data de emissão e a quantidade recebida e confirmo a alteração
    Então a tela grava a nota no registro de entrega daquele pedido
    E deixa o registro de auditoria da inclusão

  Cenário: Inclusão sem nota fiscal
    Quando confirmo a alteração de uma linha marcada para incluir sem informar a nota
    Então a tela recusa com "* Informe nota fiscal *"
    E não grava nada

  Cenário: Inclusão de nota já lançada ou de item já entregue
    Quando informo na linha uma nota que já está lançada para aquele pedido
    Então a tela recusa com "* Nota fiscal ja cadastrada *"
    Quando as demais notas daquele item já cobrem a quantidade pedida
    Então a tela recusa com "* Quantidade total entregue *"
    E não grava nada

  Cenário: Inclusão com data anterior ao pedido, sem quantidade ou acima do pedido
    Quando informo a data de emissão da nota anterior à data do pedido
    Então a tela recusa com "* Data da nota < data do pedido *"
    Quando confirmo a inclusão sem a quantidade recebida
    Então a tela recusa com "* Informe a quantidade recebida *"
    Quando a quantidade recebida faz a soma passar da quantidade pedida
    Então a tela recusa com "* Quantidade recebida > pedida *"
    E não grava nada

  Cenário: Alterar a nota fiscal lançada
    Dado que consultei o acumulado 123456/2024, do gênero 00001/00002
    E que o pedido tem a nota 987654 lançada
    Quando informo na linha a mesma nota com outra quantidade recebida e confirmo a alteração
    Então a tela substitui a nota e a quantidade daquele pedido
    E deixa o registro de auditoria da alteração

  Cenário: Alterar nota que não está lançada
    Dado que consultei o acumulado 123456/2024, do gênero 00001/00002
    Quando informo na linha uma nota que não está lançada naquele pedido e confirmo a alteração
    Então a tela recusa com "* Nota fiscal nao cadastrada *"
    E não grava nada

  Cenário: Excluir a única nota do item
    Dado que consultei o acumulado 123456/2024, do gênero 00001/00002
    E que o pedido tem uma única nota lançada
    Quando marco a linha para excluir e confirmo a alteração
    Então a tela apaga a nota, a data e a quantidade daquele registro
    E o registro de entrega daquele pedido permanece
    E deixa o registro de auditoria da alteração

  Cenário: Excluir a nota quando há outras no mesmo item
    Dado que consultei o acumulado 123456/2024, do gênero 00001/00002
    E que o item tem notas lançadas em mais de um pedido
    Quando marco para excluir a nota de um deles e confirmo a alteração
    Então a tela apaga o registro de entrega daquele pedido
    E deixa o registro de auditoria da exclusão

  Cenário: Excluir nota que não está lançada
    Dado que consultei o acumulado 123456/2024, do gênero 00001/00002
    Quando marco a linha para excluir com uma nota que não está lançada e confirmo a alteração
    Então a tela recusa com "* Nota fiscal nao cadastrada *"
    E não grava nada

  Cenário: Linha em branco não faz nada
    Dado que consultei o acumulado 123456/2024, do gênero 00001/00002
    Quando confirmo a alteração sem preencher nenhuma linha
    Então a tela não grava nada e não recusa nada

  Cenário: Pedir a relação das entregas na impressora
    Dado que consultei o acumulado 123456/2024, do gênero 00001/00002
    E que tenho correio eletrônico cadastrado
    E que não há pedido de impressão pendente dessa relação para o meu órgão e a minha coordenadoria
    Quando informo a impressora e confirmo
    Então a tela registra o pedido de impressão na fila de requisições de impressão
    E entrega o trabalho de impressão da relação das entregas
    E não grava nota fiscal nenhuma nessa passagem

  Cenário: Pedir a relação sem correio eletrônico
    Quando confirmo com a impressora informada e sem correio eletrônico cadastrado
    Então a tela recusa com "* Usuario sem e-mail cadastrado *"
    E não emite e não grava

  Cenário: Pedir a relação que já está em processamento
    Dado que já existe um pedido de impressão pendente dessa relação para o meu órgão e a minha coordenadoria
    Quando confirmo com a impressora informada
    Então a tela recusa com "* Relatorio ja esta em processamento. Aguarde. *"
    E não emite e não grava

  Cenário: A recusa não grava nada
    Dado que consultei o acumulado 123456/2024, do gênero 00001/00002
    Quando qualquer linha é recusada
    Então nenhuma nota, nenhuma auditoria e nenhuma requisição de impressão é gravada

  Cenário: A transação passa pela conferência de sessão, de rota e de operação
    Dado que a minha sessão ou a minha tela não está liberada, ou que não tenho a operação
    Quando confirmo a alteração
    Então a tela não exibe e não grava, e a transação é encerrada pela conferência
```
