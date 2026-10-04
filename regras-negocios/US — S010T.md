# US — S010T — Cadastro dos usuários do sistema

## Estória

Como **servidor de CRE com a tela S010T autorizada**, quero **consultar e manter o
cadastro de quem pode entrar no sistema — a matrícula funcional, o nome, a origem, o
e-mail, o privilégio e a senha —**, para que **o acesso ao sistema fique sob controle e
quem deixa a secretaria deixe de entrar**.

O sistema só abre a porta para quem tem cadastro de usuário: é esse cadastro que diz o
nome de quem entra, de onde a pessoa vem, se ela tem o privilégio especial e qual é a
senha. Sem ele ninguém entra; e sem quem o mantenha não há como corrigir um nome, uma
origem ou um e-mail, nem tirar do sistema quem não trabalha mais ali. É esta tela que
mostra o cadastro e o mantém: inclui, altera, exclui e, quando o servidor só quer ver,
devolve o que está gravado sem tocar em nada.

## Contexto

Jornada S000M → S001M → S004M → S010T.
Ator: servidor de CRE — consulta e mantém, pela matrícula funcional, o cadastro de quem
pode entrar no sistema.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada são menus: elas só encaminham e não deixam dado de
negócio para esta tela. Em particular, o menu principal apaga o código da tela anterior
na área de passagem da sessão, e é por isso que esta tela, vinda da jornada, abre sem
saber de tela nenhuma — em consulta. O que a `S010T` usa da sessão — a matrícula de quem
opera, o acesso, o privilégio, o tipo de órgão, a CRE, a descrição do tipo de órgão e a
data do sistema — é o que a entrada deixou. A matrícula funcional que o operador informa
não é a dele: é o alvo da consulta ou da manutenção.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela é o cadastro de quem pode entrar no sistema

O cadastro de usuários guarda a matrícula funcional, o nome, a origem, o e-mail, o
privilégio, o registro da última utilização — dia, mês, ano, hora e estação —, a senha
de acesso com o histórico das anteriores e as datas de criação e de atualização. É esse
cadastro que esta tela mantém: consulta, inclui, altera e exclui.

De cada manutenção saem três coisas: o cadastro do usuário; os vínculos dele com os
órgãos, que a exclusão apaga; e um registro de auditoria com o que o cadastro era antes
e como ficou depois. Nenhum outro cadastro é tocado. A tela não mostra a senha nem o
histórico de senhas: nenhum desses campos é exibido.

### RN-02 — Abrir a tela não lê nem grava cadastro

Enquanto a tela é apenas aberta, nenhum cadastro de usuário é lido e nada é gravado
nele. A abertura mostra a descrição do tipo de órgão da sessão e a data do sistema,
procura a própria tela no cadastro de telas para confirmar que ela existe e passa a
conferência de acesso. O cadastro só é lido depois de uma mensagem do operador.

### RN-03 — Como a tela abre depende de qual tela a chamou

A tela decide o modo de abertura pelo código da tela que a chamou, deixado na área de
passagem da sessão:

- quando o encaminhamento vem da tela de inclusão de usuário com o cidadão ainda por
  registrar, a abertura **registra o cidadão e a origem** — criando a origem quando ela
  ainda não existe — e grava a auditoria dessa passagem antes de mostrar a tela, que
  abre para inclusão com os dados que a chamadora deixou;
- quando o encaminhamento traz o cidadão já registrado pela inclusão, ou vem de uma das
  telas de consulta de usuário ou de vínculo com os órgãos, a tela abre **já preenchida**
  com o que a chamadora deixou — matrícula, nome, origem, e-mail, privilégio e registro
  da última utilização — e com a **operação que a chamadora determinou**, que pode ser a
  de inclusão ou a de alteração;
- quando não há código nenhum — é o caso desta jornada, em que ela vem do menu —, ela
  abre **vazia, em consulta e com o privilégio marcado como não**.

[?] A área de passagem é da sessão e esta tela não a limpa ao abrir. Se uma transação
anterior deixar nela um daqueles códigos, esta tela abre encadeada — com dados de outra
pessoa e a operação que aquela determinou. Se isso é possível na prática, os fontes
desta jornada não dizem. Pergunta ao site.

### RN-04 — A matrícula funcional identifica o usuário: um cadastro por matrícula

A matrícula funcional é o que identifica o usuário no cadastro: cada matrícula tem um
único cadastro e a busca é feita por ela sozinha. Não existindo cadastro para a
matrícula informada, a mensagem termina sem gravar e o cursor volta ao campo da
matrícula. Na inclusão, ao contrário, não achar é o esperado: é assim que se sabe que a
matrícula ainda não tem cadastro.

[?] O que a tela mostra quando a matrícula não está cadastrada não se conclui dos
fontes desta jornada: o caminho da consulta continua depois de a busca não achar e
devolve os campos que estiverem na área do cadastro. Pergunta ao site.

### RN-05 — A matrícula, o dia, o mês, o ano e a hora de utilização são editados como número

Esses campos passam pela edição numérica antes de qualquer consulta: o que estiver em
branco vale zero, os separadores são repostos na exibição e o que não for número é
recusado antes da consulta ao cadastro, com o cursor devolvido ao próprio campo. A
matrícula é editada como número de nove dígitos; o dia e o mês da utilização, como
número de dois; o ano, como número de quatro; e a hora, o minuto e o segundo, como
número de dois cada um.

[?] O texto que o operador vê quando a digitação é recusada não está nos fontes desta
jornada: a conferência é chamada de uma rotina de biblioteca cujo corpo não veio no
lote. Pergunta ao site.

[?] A matrícula em branco vira zero e a consulta é feita com zero: fora da inclusão não
há guarda que recuse o campo vazio. Se existir cadastro com matrícula zero, é ele o
consultado. Pergunta ao site.

### RN-06 — A consulta só devolve o cadastro, e não grava nada

Com a operação de consulta, a tela lê o cadastro pela matrícula informada e devolve na
tela o nome, a origem, o e-mail, o privilégio, o estado da sessão, o dia, o mês, o ano e
a hora da última utilização e a estação — doze campos. Nada é gravado: nenhum cadastro
é incluído, alterado ou excluído e nenhum registro de auditoria é escrito. É também com
essa operação que a tela abre quando vem do menu.

### RN-07 — O cadastro pode ser percorrido sem digitar a matrícula

A tela reconhece operações próprias de percurso do cadastro: a primeira página, a
última, a seguinte, a anterior e a que relê o cadastro pela matrícula já informada. Com
elas a tela relê o cadastro e volta a mostrá-lo, sem gravar nada. As duas de página —
primeira e última — não exigem a matrícula preenchida; as outras três usam a matrícula
informada e, sem ela, a mensagem é recusada no próprio campo.

[?] Como o operador escolhe essas operações não se conclui dos fontes desta jornada: os
nomes delas são códigos do ambiente, e a ficha da tela não registra nenhuma opção
declarada. Pergunta ao site.

### RN-08 — A alteração grava o cadastro; o e-mail deixado em branco apaga o e-mail

Com a operação de alteração, a tela lê o cadastro pela matrícula, refaz o nome a partir
do cadastro do cidadão e o grava com os dados informados. Campo em branco não apaga o
que estava gravado: a matrícula, o nome, a origem, o e-mail, o privilégio, o estado da
sessão e o registro da última utilização só são gravados quando o campo correspondente
vem preenchido. A exceção é o e-mail — deixá-lo em branco numa alteração apaga o e-mail
que estava gravado.

[?] A origem informada não é conferida contra o cadastro de origens nesta operação: a
tela a grava como veio. Se origem não cadastrada deveria ser recusada, o fonte não diz.
Pergunta ao site.

### RN-09 — Só se inclui ou altera quem consta da Tabela Cidadão

A inclusão e a alteração exigem que a matrícula informada conste da Tabela Cidadão. Não
consta: a recusa é **\* Matricula nao cadastrada na Tabela Cidadao \***, com o cursor de
volta ao campo da matrícula, e nada é gravado. A consulta e a exclusão não fazem essa
exigência.

### RN-10 — A exclusão marca o cadastro como excluído e apaga os vínculos

A exclusão não apaga o cadastro do usuário: ela o **marca como excluído**, de modo que a
matrícula deixa de entrar no sistema e passa a ser avisada como cadastro excluído quando
alguém a procura. Junto com isso, a tela percorre os vínculos daquela matrícula com os
órgãos e apaga cada um deles, registrando a auditoria de cada apagamento. O cadastro do
cidadão e a origem não são tocados.

### RN-11 — A inclusão gera a senha e entrega o cadastro à tela de vínculo

Com a operação de inclusão, a tela toma a data e a hora do momento, marca a estação de
onde se inclui, gera a senha inicial do sistema — a mesma para todo usuário incluído —,
atualiza no cadastro do cidadão a data de atualização daquela matrícula, grava a
auditoria da inclusão e cria o cadastro do usuário com a marca de inclusão, a matrícula
de quem incluiu e as datas de criação e de atualização.

Feito isso, a mensagem **não termina na tela**: ela é encaminhada para a tela de vínculo
do usuário com os órgãos, levando a matrícula, o nome e a origem do usuário incluído e a
operação de **alteração**. É por causa disso que a tela de vínculo abre com o cadastro
do usuário já posicionado e em modo de alteração.

### RN-12 — Não se exclui o próprio cadastro

Quando a matrícula informada é a do próprio operador e a operação é a de exclusão, a
exclusão é recusada: a mensagem é **\* Nao exclua seu proprio cadastro \***, com o
cursor no campo da operação, e nada é gravado.

### RN-13 — O nível de acesso limita a exclusão

A exclusão também depende do nível de acesso. O sistema toma o maior nível registrado
para a matrícula de quem opera e o maior nível registrado para a matrícula informada, e
deixa passar quando o alvo tem nível **menor**. Quando os dois níveis são **iguais**, a
exclusão só passa se o operador tiver o privilégio especial da sessão; quando o nível do
alvo é **maior**, a recusa é **\* Seu nivel de acesso nao permite esta operacao \***,
com o cursor no campo da operação, e nada é gravado. A conferência de nível vale só para
a exclusão: a inclusão e a alteração não a fazem.

### RN-14 — Não se exclui usuário com a sessão aberta no dia

Antes de excluir, o sistema confere o registro da última utilização do alvo. Se o
cadastro está com a sessão **aberta** e o dia registrado é o de hoje, a exclusão é
recusada com **\* Usuario esta com sessao aberta \***, com o cursor no campo da
matrícula, e nada é gravado.

[?] O registro de utilização só barra a exclusão quando o dia é o de hoje; uma sessão
deixada aberta em dia anterior não barra — quem fecha essas sessões é outra tela. Se o
barramento deveria valer para qualquer sessão aberta, o fonte não diz. Pergunta ao site.

### RN-15 — Só quem tem nível 99 concede o privilégio especial

O privilégio do usuário só pode ser o especial ou o comum. Na inclusão e na alteração, o
privilégio informado tem de ser **S** ou **N**; não sendo, a recusa é
**\* Informe se usuario tem privilegio com S ou N \***, com o cursor no campo do
privilégio, e nada é gravado.

Conceder o privilégio especial a alguém é mais restrito: quando quem opera não tem o
privilégio especial na sessão e o privilégio informado para o usuário é **S**, o sistema
exige que o operador tenha nível **99** no próprio cadastro de acessos, para o tipo de
órgão dele. Sem isso, a recusa é **\* Nao cadastre usuario com privilegio \***, com o
cursor no campo do privilégio, e nada é gravado.

### RN-16 — O cadastro marcado como excluído é avisado

Antes de qualquer manutenção, o sistema procura a matrícula informada e confere se o
cadastro está marcado como excluído. Estando, o aviso **"Key deleted"** é emitido junto
ao campo da matrícula. O aviso interrompe a inclusão e a exclusão; a **consulta** é a
exceção — nela o aviso é emitido e a consulta continua, mostrando o cadastro. A
**alteração** é o contrário: não emite aviso nenhum e segue adiante.

[?] Os fontes desta jornada mostram a tela apagando, na consulta, a marca de falha que
interromperia a mensagem — o que só faz sentido se a rotina que emite o aviso a tiver
posto. Quem emite o aviso é uma rotina do ambiente, cujo corpo não está no lote; se ela
não marcar a falha, a alteração de um cadastro marcado como excluído grava sobre ele.
Pergunta ao site.

### RN-17 — Antes de gravar, o sistema confere a tela, a operação e o acesso

Toda mensagem passa pelas conferências comuns. A da rota exige que a tela esteja no
cadastro de telas — tendo sido retirada, a recusa é **\* Tela nao cadastrada \*** — e
reconhece como operação a inclusão, a alteração, a exclusão, a consulta, o retorno, o
menu e a saída; não reconhecendo, o aviso é **\* Operacao nao disponivel \***. A do
acesso exige a tela `S010T` no cadastro de telas por código de acesso da matrícula que
opera — não estando, a recusa é **\* Acesso negado para esta matricula \*** — e, para a
inclusão, a alteração e a exclusão, a liberação daquela operação no mesmo cadastro — não
tendo, a recusa é **\* Acesso negado para esta operacao \***. Ao abrir, a conferência
ainda exige que a tela exista no cadastro de telas — não existindo, o aviso é
**\* Tela nao disponivel \***.

[?] Os fontes desta jornada não permitem concluir se o aviso
**\* Operacao nao disponivel \*** interrompe a mensagem: o ramo que o emite não marca a
falha que a conferência da rota testa, e o caminho que grava volta a ler a operação sem
conferi-la. Se a marca não estiver posta, uma operação recusada na tela ainda é gravada
— e existe, no caminho que grava, um ramo que **apaga** o cadastro para a operação de
expurgo, sem guarda anterior que o impeça. Se esse ramo é alcançável, o fonte não diz.
Pergunta ao site.

### RN-18 — A descrição do tipo de órgão e a data do sistema voltam em branco

A descrição do tipo de órgão da sessão e a data do sistema, que a tela mostra ao abrir,
são apagadas a cada mensagem respondida e não são repostas: a resposta sai com os dois
campos em branco.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe um
caminho de entrada em que os campos não são limpos, não foi possível determinar.
Pergunta ao site.

### RN-19 — A próxima tela preenchida abandona a manutenção

Se a mensagem chegar com o campo da próxima tela preenchido, ela é desviada para a tela
indicada e a manutenção é abandonada: nada é lido do cadastro e nada é gravado.

[?] O que preenche o campo da próxima tela nesta tela não está no acervo: nenhuma linha
do programa o atribui a partir da área de passagem — a tela só o lê. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta e manutenção do cadastro de usuários do sistema

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S010T

  Cenário: Abrir a tela pelo menu abre em consulta e não lê cadastro nenhum
    Dado que abro a tela S010T vinda do menu
    Então o cadastro abre vazio e em consulta
    E o privilégio aparece marcado como não
    E nenhum cadastro de usuário foi lido ou gravado
    E vejo a descrição do tipo de órgão da sessão e a data do sistema
    E a tela apenas confere se ela está cadastrada e se a minha matrícula tem acesso

  Cenário: A tela chamada por uma tela encadeadora abre com os dados e a operação dela
    Dado que uma tela de consulta de usuário me encaminha para a S010T
    Quando a tela abre
    Então ela já mostra a matrícula, o nome, a origem, o e-mail, o privilégio e o registro da última utilização que a chamadora deixou
    E abre na operação que a chamadora determinou

  Cenário: A tela chamada pela inclusão de usuário registra o cidadão e a origem antes de abrir
    Dado que a tela de inclusão de usuário me encaminha para a S010T
    Quando a tela abre
    Então o cidadão e a origem foram registrados antes
    E a origem foi criada porque ainda não existia
    E o cadastro abre para inclusão com os dados que a chamadora deixou

  Cenário: Consulta de um usuário cadastrado
    Dado que a matrícula informada é de um usuário cadastrado
    Quando informo a matrícula funcional com a operação de consulta
    Então vejo o nome, a origem, o e-mail, o privilégio, o estado da sessão e o dia, o mês, o ano e a hora da última utilização
    E nada é gravado

  Cenário: Consulta de matrícula não cadastrada
    Dado que informo uma matrícula que não existe no cadastro de usuários
    Quando confirmo a mensagem com a operação de consulta
    Então o sistema marca que não achou o registro
    E o cursor volta para o campo da matrícula
    E nada é gravado

  Cenário: Matrícula não numérica
    Dado que informo uma matrícula que não é número
    Quando confirmo a mensagem
    Então o campo é recusado antes da consulta ao cadastro
    E o cursor volta para o campo da matrícula

  Cenário: Data e hora de utilização não numéricas
    Dado que informo um dia, um mês, um ano ou uma hora de utilização que não é número
    Quando confirmo a mensagem
    Então o campo é recusado antes de qualquer gravação
    E o cursor volta para o campo da utilização

  Cenário: Percorrer o cadastro sem digitar a matrícula
    Dado que peço a primeira ou a última página do cadastro
    Quando confirmo a mensagem
    Então vejo o cadastro de um usuário, sem precisar informar a matrícula
    E nada é gravado

  Cenário: Percorrer o cadastro a partir de uma matrícula
    Dado que informo a matrícula funcional e peço a página seguinte, a anterior ou a releitura
    Quando confirmo a mensagem
    Então vejo o cadastro seguinte, o anterior ou o da própria matrícula
    E nada é gravado

  Cenário: Percorrer o cadastro sem informar a matrícula
    Dado que peço a página seguinte sem informar a matrícula funcional
    Quando confirmo a mensagem
    Então o campo da matrícula é recusado
    E nada é gravado

  Cenário: Alteração de um usuário cadastrado
    Dado que a matrícula informada é de um usuário cadastrado na Tabela Cidadão
    Quando informo a operação de alteração com a origem, o e-mail e o privilégio
    Então o cadastro do usuário fica com os dados informados
    E o nome é refeito a partir do cadastro do cidadão
    E a alteração fica registrada na auditoria

  Cenário: Alteração deixando o e-mail em branco apaga o e-mail gravado
    Dado que o cadastro do usuário tem um e-mail gravado
    Quando informo a operação de alteração com o campo do e-mail em branco
    Então o e-mail gravado é apagado
    E os demais campos que deixei em branco continuam como estavam

  Cenário: Inclusão ou alteração de matrícula que não consta da Tabela Cidadão
    Dado que a matrícula informada não consta da Tabela Cidadão
    Quando confirmo a mensagem com a operação de inclusão ou de alteração
    Então vejo a mensagem "* Matricula nao cadastrada na Tabela Cidadao *"
    E o cursor volta para o campo da matrícula
    E nada é gravado

  Cenário: Inclusão de um usuário que consta da Tabela Cidadão
    Dado que a matrícula informada consta da Tabela Cidadão e ainda não tem cadastro de usuário
    Quando informo a operação de inclusão
    Então o cadastro do usuário passa a existir
    E ele fica com a senha inicial do sistema
    E a data de atualização da matrícula no cadastro do cidadão passa a ser a de hoje
    E a estação de onde incluí fica registrada
    E a inclusão fica registrada na auditoria

  Cenário: A inclusão entrega o cadastro à tela de vínculo
    Dado que incluí um usuário que consta da Tabela Cidadão
    Quando a inclusão termina
    Então a mensagem é encaminhada para a tela de vínculo do usuário com os órgãos
    E ela abre com a matrícula, o nome e a origem do usuário incluído
    E ela abre na operação de alteração

  Cenário: Exclusão de um usuário cadastrado
    Dado que a matrícula informada é de um usuário cadastrado
    E o nível de acesso dele é menor que o meu
    Quando informo a operação de exclusão
    Então o cadastro dele fica marcado como excluído
    E os vínculos dele com os órgãos são apagados
    E a exclusão fica registrada na auditoria

  Cenário: Exclusão da própria matrícula
    Dado que a matrícula informada é a minha
    Quando informo a operação de exclusão
    Então vejo a mensagem "* Nao exclua seu proprio cadastro *"
    E o cursor volta para o campo da operação
    E nada é gravado

  Cenário: Exclusão de quem tem nível de acesso maior
    Dado que a matrícula informada é de um usuário com nível de acesso maior que o meu
    Quando informo a operação de exclusão
    Então vejo a mensagem "* Seu nivel de acesso nao permite esta operacao *"
    E nada é gravado

  Cenário: Exclusão de quem tem nível de acesso igual ao meu, sem o privilégio especial
    Dado que a matrícula informada é de um usuário com o meu nível de acesso
    E não tenho o privilégio especial na sessão
    Quando informo a operação de exclusão
    Então vejo a mensagem "* Seu nivel de acesso nao permite esta operacao *"
    E nada é gravado

  Cenário: Exclusão de usuário com a sessão aberta hoje
    Dado que o cadastro do usuário está com a sessão aberta
    E o dia registrado da sessão é o de hoje
    Quando informo a operação de exclusão
    Então vejo a mensagem "* Usuario esta com sessao aberta *"
    E o cursor volta para o campo da matrícula
    E nada é gravado

  Cenário: Conceder o privilégio especial sem ter nível 99
    Dado que não tenho o privilégio especial na sessão
    E não tenho nível 99 no meu cadastro de acessos
    Quando informo o privilégio especial para o usuário e confirmo a mensagem
    Então vejo a mensagem "* Nao cadastre usuario com privilegio *"
    E o cursor volta para o campo do privilégio
    E nada é gravado

  Cenário: Privilégio diferente de especial ou comum
    Dado que informo um privilégio que não é o especial nem o comum
    Quando confirmo a mensagem
    Então vejo a mensagem "* Informe se usuario tem privilegio com S ou N *"
    E o cursor volta para o campo do privilégio
    E nada é gravado

  Cenário: Cadastro marcado como excluído
    Dado que o cadastro da matrícula informada está marcado como excluído
    Quando confirmo a mensagem com a operação de exclusão
    Então vejo o aviso "Key deleted" junto ao campo da matrícula
    E a exclusão não acontece

  Cenário: A consulta de um cadastro marcado como excluído continua
    Dado que o cadastro da matrícula informada está marcado como excluído
    Quando confirmo a mensagem com a operação de consulta
    Então vejo o aviso "Key deleted" junto ao campo da matrícula
    E a consulta continua e mostra o cadastro

  Cenário: A alteração de um cadastro marcado como excluído não é avisada
    Dado que o cadastro da matrícula informada está marcado como excluído
    Quando confirmo a mensagem com a operação de alteração
    Então não vejo aviso nenhum sobre o cadastro estar excluído

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela S010T
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Sem autorização para a operação
    Dado que o meu código de acesso tem a tela S010T sem a alteração liberada
    E informo a operação de alteração com a matrícula de um usuário cadastrado
    Quando confirmo a mensagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Tela não disponível
    Dado que a tela S010T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Tela retirada do cadastro
    Dado que a tela S010T foi retirada do cadastro de telas
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é gravado

  Cenário: Operação não reconhecida
    Dado que informo uma operação que a tela não reconhece
    Quando confirmo a mensagem
    Então vejo a mensagem "* Operacao nao disponivel *"

  Cenário: A próxima tela preenchida abandona a manutenção
    Dado que informo um código no campo da próxima tela
    Quando confirmo a mensagem
    Então a mensagem é desviada para a tela indicada
    E nada é lido do cadastro e nada é gravado

  Cenário: A resposta volta com dois campos em branco
    Dado que a tela abriu mostrando a descrição do tipo de órgão da sessão e a data do sistema
    Quando respondo uma mensagem
    Então a resposta vem com esses dois campos em branco
```
