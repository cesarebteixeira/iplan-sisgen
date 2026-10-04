# US — E058T — Consulta dos preparos da merenda do órgão

## Estória

Como **servidor de CRE**, quero **ver os preparos da merenda que o órgão filho SDI da minha
coordenadoria regional escolar tem, escolher um deles e abrir o preparo escolhido em
consulta**, para que **eu ache o preparo certo sem ter de saber de cor a data em que o
cálculo dele começa — e chegue à tela onde o preparo se consulta já com o órgão e a data
carregados**.

O preparo da merenda de uma escola é feito por órgão e por período, e cada preparo tem uma
data de início de cálculo que só existe na base. Quem atende o órgão não guarda essa data de
cabeça: o que existe é a lista dos preparos daquele órgão, com a situação de cada um. Esta
tela é essa lista — ela mostra, de uma vez, os preparos do órgão do servidor com a data de
início do cálculo, o limite do cálculo, o período de entrega e a situação de cada linha, e
entrega o escolhido à tela de preparo. Sem ela, o servidor teria de adivinhar a data exata
para chegar ao preparo, e não teria como ver, antes de abrir, quais preparos aquele órgão já
tem calculados.

## Contexto

Jornada S000M → E000M → E050M → E058T.
Ator: servidor de CRE — confere o órgão filho SDI e a coordenadoria regional escolar, vê a
lista dos preparos daquele órgão e marca a linha do preparo que quer consultar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Da sessão a tela usa o **tipo de órgão**, a **coordenadoria regional escolar** e o **órgão
filho** do vínculo do servidor — é o vínculo que limita o que ela deixa consultar —, e ainda
a **matrícula**, o **código de acesso**, a **estação** e o **privilégio**, que é o que as
conferências de acesso leem. No cabeçalho ela mostra a **descrição do tipo de órgão** e a
**data do sistema**.

Esta tela **não decide nada pelo código da tela que a chamou**: no acervo, a única porta
medida para ela é a opção do menu desta jornada, e o que ela confere é o que está na sessão e
o que o servidor informa. O que ela **entrega à seguinte** está na RN-13: ela encadeia para a
tela de preparo, sem passar por menu, e é o modo que ela deixa nessa passagem que decide como
a tela seguinte abre.

As regras abaixo são só as da tela desta jornada. O `E000M` e o `E050M` são menus: não gravam
nada e apenas encaminham. O que já está na entrada não se repete aqui; o que se revelou dela
ao ler estes fontes está no anexo de evidências.

---

## Regras de negócio

### RN-01 — A tela só consulta, e é isso que ela exige

A tela serve para consultar: ela não inclui, não altera e não exclui. Ao ser apresentada, ela
mesma põe **consultar** no campo da operação, e a operação que a tela que a chamou tenha
deixado na passagem é descartada antes de ser olhada. Se a transação voltar com outra
operação, a recusa é **\* Operacao nao disponivel. Use CON \***, com o cursor de volta ao
campo da operação, e nada mais é conferido, mostrado ou encaminhado.

[?] A recusa manda usar a tecla **CON**, mas o que a tela põe no campo é o mnemônico interno
da consulta, que não é o mesmo texto. Se o terminal traduz a tecla para esse mnemônico antes
de enviar, a regra é uma só; se não traduz, ou a mensagem engana quem opera, ou a guarda
recusa exatamente o que ela manda fazer. O corpus não traz essa tradução. Pergunta ao site.

### RN-02 — A tela não grava nada

A tela não inclui, não altera e não exclui registro nenhum: as **três** bases que ela usa —
o cadastro de telas, o cadastro de órgãos e os preparos — são só lidas, e não há caminho
nenhum que escreva. A abertura, a recusa e a consulta terminam sem escrita. O único desfecho
que muda o que o servidor vê é o encaminhamento para a tela seguinte (RN-13), que também não
grava nada.

As bases são dimensionadas para: cadastro de telas **2.000**; cadastro de órgãos **12.000**;
preparos **500.000**. São capacidades — o máximo esperado no dimensionamento —, não volumes
cadastrados.

### RN-03 — Ao abrir, a tela mostra o cabeçalho e os preparos do órgão, onze por vez

Ao ser aberta, a tela traz no cabeçalho a **descrição do tipo de órgão** da sessão e a **data
do sistema**; no campo do órgão, o órgão do vínculo do servidor, com o **nome do órgão** lido
do cadastro; e, abaixo, a lista dos **preparos** daquele órgão — **onze linhas** por vez,
cada uma com a **data de início do cálculo**, o **limite do cálculo**, o **início do período
de entrega** e o **limite do período**, cada data escrita como dia/mês/ano, mais a
**situação** do preparo e a **marca da linha**. Acabando os preparos do órgão, as linhas que
sobram ficam em branco. A lista é lida na ordem das datas de início do cálculo.

[?] A descrição do tipo de órgão e a data do sistema não têm, no acervo, nenhum caminho que
as preencha: as duas aparecem só como origem de cópia, e os dois únicos destinos que o acervo
registra para elas as apagam. A entrada guarda as duas numa área da sessão e esta tela as lê
de outra. Se o ambiente transporta o valor de uma área para a outra, o acervo não diz — e, se
não transportar, os dois campos do cabeçalho saem em branco. Pergunta ao site.

[?] Entre as datas a tela devolve duas marcas separadoras com o valor **A**, e o corpus não
traz o que essa marca significa: a máscara da tela não está no acervo, e o único outro
programa que grava o mesmo valor é uma tela irmã do mesmo gerador. Se a marca é só de
exibição, é pergunta ao site.

### RN-04 — O preparo já calculado é mostrado como "Calculada"

A situação de cada linha vem do próprio preparo: quando ele já foi calculado, a linha mostra
**Calculada**; quando não, a situação sai em branco. O acervo só registra dois estados para o
preparo — a marca de calculado, que a tela de cálculo grava, e a marca em branco, que a tela
de cancelamento grava.

### RN-05 — O órgão sem preparos cadastrados é avisado, e as datas saem em branco

Quando não existe preparo para o órgão e a data que a tela está usando, ela não mostra linha
nenhuma: avisa **\* Orgao sem preparos cadastrados \***, deixa as datas em branco e encerra a
passagem. O aviso sai uma vez só, na primeira linha da lista.

### RN-06 — Quando o vínculo não traz órgão, a tela abre esperando que o servidor o informe

Se o vínculo do servidor não carrega um órgão filho, a tela abre sem órgão, com o cursor no
campo do órgão, e não mostra preparo nenhum até que ele seja informado. Quem tem órgão no
vínculo já o encontra preenchido, com o nome lido do cadastro.

### RN-07 — O órgão é obrigatório

O órgão filho SDI tem de vir informado. Em branco, a recusa é **\* Informe o orgao \***, com
o cursor de volta ao campo do órgão, e nada é mostrado nem encaminhado.

### RN-08 — Quem tem órgão no vínculo não consulta preparo de outro órgão

O órgão informado tem de ser o do vínculo do servidor. Quem tem um órgão no vínculo e informa
outro é recusado com **\* Usuario sem acesso a outro orgao \*** — a mensagem traz o código do
órgão do vínculo —, com o cursor de volta ao campo do órgão e nada mostrado. Quem não tem
órgão no vínculo consulta o que informar.

### RN-09 — O órgão informado tem de estar cadastrado

Do cadastro de órgãos vêm o nome do órgão e a coordenadoria regional escolar dele. Órgão não
cadastrado é recusado com **\* Orgao nao cadastrado \***, com o cursor de volta ao campo do
órgão e nada mostrado.

[?] A recusa por órgão não cadastrado não é disparada só pela falta do cadastro: o sinal que
a decide é o de **outra** leitura — a do preparo do órgão na data do sistema. Lendo o
caminho, o órgão ausente do cadastro **e** sem preparo naquela data é recusado; o órgão
ausente do cadastro **com** preparo naquela data passa e segue adiante com o nome que ficou
da leitura anterior e sem trocar a coordenadoria. Ou a guarda queria testar a leitura do
cadastro, ou o sinal está trocado. Não escolho um dos dois lados: pergunta ao site.

### RN-10 — O órgão tem de ser de uma coordenadoria do servidor

Quando a sessão traz uma coordenadoria regional escolar, o órgão informado tem de ser de uma
coordenadoria igual à dela. Sendo de outra, a recusa é
**<- Usuario sem acesso ao grupo deste orgao \*** — a mensagem traz o código da coordenadoria
—, com o cursor de volta ao campo do órgão e nada mostrado. Quando a sessão não traz
coordenadoria, esta conferência não é feita.

### RN-11 — A coordenadoria informada cede lugar à do órgão cadastrado

O campo da coordenadoria regional escolar é mostrado e pode ser preenchido, mas não é ele que
decide o acesso em todos os casos: quando **não** existe preparo para o órgão e a
coordenadoria informados na data do sistema, a tela troca a coordenadoria digitada pela que
está no cadastro do órgão, e é essa que ela confere e usa dali em diante. Quando existe
preparo para o par informado, é a coordenadoria digitada que a tela confere.

[?] O mesmo campo tem dois destinos: se o par órgão e coordenadoria digitado tem preparo na
data do sistema, vale o que o servidor digitou; se não tem, vale a coordenadoria do cadastro
do órgão e a digitada é descartada em silêncio. Quem digita a coordenadoria errada é recusado
num caso e aceito no outro, sem que a tela avise. Se o campo existe para o servidor escolher
alguma coisa, essa escolha não é atendida. Pergunta ao site.

### RN-12 — Só a linha marcada é levada adiante

A tela não faz nada com a linha que não esteja marcada: sem nenhuma marca, a passagem termina
e a tela continua onde está. Marcada a linha e **vazia** a data dela — o caso das linhas que
sobram depois do último preparo do órgão —, a recusa é **\* A linha deve estar preenchida \***,
com o cursor de volta à marca da linha, e nada é encaminhado.

### RN-13 — A linha marcada abre a tela de preparo, em consulta

Com a linha marcada e preenchida, a tela não mostra mais nada: ela passa a transação para a
tela de preparo levando o **órgão**, a **coordenadoria regional escolar** e a **data de
início do cálculo** daquela linha, com a operação marcada como **consulta** e com a marca de
que a consulta vem desta tela. A tela de preparo abre, então, com esses três dados já
preenchidos, em consulta, e avisa **\* Consulta preparo \***, com o cursor no campo do órgão.
É a única saída desta tela.

### RN-14 — Os campos numéricos passam por edição numérica antes das conferências

Antes de qualquer conferência, **cinco** campos passam pela edição numérica — o órgão filho
SDI, a coordenadoria regional escolar e o dia, o mês e o ano da data —, e o campo em branco é
tratado como zero. O campo da operação e o da próxima tela não passam por essa edição.

[?] O dia, o mês e o ano isolados não decidem nada: a data que a tela encaminha à tela
seguinte é montada a partir da data mostrada na linha marcada, e não do que foi digitado
nesses três campos, que só voltam à tela como exibição. Se eles são de digitação ou de
exibição, o acervo não diz — a máscara da tela não está nele. Pergunta ao site.

### RN-15 — Nada é mostrado nem encaminhado sem a conferência de sessão, de tela, de acesso e de operação

Na abertura, a tela confere que o servidor está na **estação em que a sessão foi aberta** —
em outra, o acesso é encerrado e a sessão volta à entrada —, que a tela está registrada
(senão **\* Tela nao disponivel \***) e que o código de acesso do servidor alcança a tela
(senão **\* Acesso negado para esta matricula \***) e a operação de consulta (senão
**\* Acesso negado para esta operacao \***). Ao enviar a transação, a lógica de rota confere
a tela de novo (**\* Tela nao cadastrada \***) e exige a operação. A requisição da segunda
página da tela é recusada com **\* Acesso a pagina 2 negado \***. Sem passar por tudo, nada é
mostrado e nada é encaminhado.

[?] A transação é roteada por um campo de "próxima tela" que chega preenchido de fora da
tela: vindo preenchido, a tela encaminha a transação para essa outra tela e a passagem
termina sem mostrar nada nem encaminhar a linha marcada. Em todo o acervo nenhum caminho
escreve nesse campo, e não se conclui quem o preenche nem se ele pode levar a transação para
outra tela. Pergunta ao site.

[?] A mesma falta — a tela não registrada — tem duas mensagens diferentes, porque duas
rotinas comuns a conferem em momentos distintos: a da abertura e a da rota, que roda quando a
transação é enviada. Qual das duas o servidor vê depende do momento em que a falta é
percebida, e o acervo não diz qual é a pretendida. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar os preparos da merenda do órgão filho SDI da coordenadoria regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E058T

  Cenário: A tela mostra os preparos do órgão do meu vínculo
    Dado que o órgão do meu vínculo tem preparos cadastrados
    Quando abro a tela E058T
    Então vejo a descrição do tipo de órgão e a data do sistema no cabeçalho
    E vejo o órgão do meu vínculo já preenchido, com o nome dele
    E vejo as linhas dos preparos, cada uma com a data de início do cálculo, o limite do
      cálculo, o início e o limite do período de entrega e a situação
    E nenhum preparo, órgão ou registro de tela é gravado ou apagado

  Cenário: O preparo já calculado aparece como "Calculada"
    Dado um preparo que já foi calculado
    Quando a linha dele é mostrada
    Então a situação da linha mostra "Calculada"

  Cenário: O preparo ainda não calculado aparece sem situação
    Dado um preparo que ainda não foi calculado
    Quando a linha dele é mostrada
    Então a situação da linha sai em branco

  Cenário: Órgão sem preparos cadastrados
    Dado que o órgão em uso não tem nenhum preparo
    Quando abro a tela E058T
    Então vejo "* Orgao sem preparos cadastrados *"
    E as datas saem em branco
    E nada é gravado

  Cenário: O vínculo sem órgão abre a tela esperando o órgão
    Dado que o meu vínculo não carrega um órgão filho
    Quando abro a tela E058T
    Então a tela abre sem órgão e com o cursor no campo do órgão
    E não vejo preparo nenhum até informar o órgão

  Cenário: Operação diferente de consultar é recusada
    Dado que a transação chega com uma operação que não é a de consulta
    Quando a tela confere a operação
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor fica no campo da operação
    E nada é mostrado nem encaminhado

  Cenário: O órgão é obrigatório
    Dado que estou na tela E058T
    Quando confirmo sem informar o órgão
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é mostrado nem encaminhado

  Cenário: O servidor não consulta preparo de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo outro órgão e confirmo
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão
    E nada é mostrado nem encaminhado

  Cenário: Órgão não cadastrado
    Dado que estou na tela E058T
    Quando informo um órgão que não está no cadastro e confirmo
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é mostrado nem encaminhado

  Cenário: Órgão de outra coordenadoria
    Dado que a minha sessão carrega uma coordenadoria regional escolar
    Quando informo um órgão de outra coordenadoria e confirmo
    Então vejo "<- Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é mostrado nem encaminhado

  Cenário: A coordenadoria informada sem preparo na data do sistema é trocada
    Dado que informo um órgão e uma coordenadoria que não têm preparo na data do sistema
    Quando confirmo
    Então a tela passa a usar a coordenadoria que está no cadastro do órgão
    E a coordenadoria que eu digitei não é usada

  Cenário: Nenhuma linha marcada não faz nada
    Dado que estou na tela E058T com a lista dos preparos
    Quando confirmo sem marcar nenhuma linha
    Então a tela continua onde está
    E nada é encaminhado

  Cenário: Linha marcada e vazia é recusada
    Dado que marco uma linha que está em branco, depois do último preparo do órgão
    Quando confirmo
    Então vejo "* A linha deve estar preenchida *"
    E o cursor fica na marca da linha
    E nada é encaminhado

  Cenário: A linha marcada abre o preparo em consulta
    Dado que marco a linha de um preparo e a data dela está preenchida
    Quando confirmo
    Então a tela encaminha a transação para a tela de preparo
    E a tela de preparo abre com o órgão, a coordenadoria e a data de início do cálculo
      já preenchidos
    E ela abre em consulta e avisa "* Consulta preparo *", com o cursor no campo do órgão

  Cenário: Os campos numéricos passam por edição numérica antes das conferências
    Dado que deixo um dos campos numéricos em branco
    Quando confirmo
    Então o campo em branco é tratado como zero antes das conferências
    E a digitação que não é número é barrada antes das conferências do órgão

  Cenário: Nada é mostrado sem a conferência de sessão, de tela, de acesso e de operação
    Dado que estou na tela E058T
    Quando a conferência da estação, do registro da tela, do código de acesso ou da operação
      não passa
    Então vejo "* Tela nao disponivel *", "* Tela nao cadastrada *",
      "* Acesso negado para esta matricula *", "* Acesso negado para esta operacao *" ou
      "* Acesso a pagina 2 negado *"
    E nada é mostrado e nada é encaminhado
    E, se a estação não for a da minha sessão, o acesso é encerrado

  Cenário: A consulta não grava nada
    Dado que consultei os preparos do órgão sem marcar nenhuma linha
    Quando a passagem termina
    Então nenhum preparo, órgão ou registro de tela foi incluído, alterado ou excluído
    E nenhum registro de auditoria foi gravado
```
