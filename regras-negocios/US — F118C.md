# US — F118C — Consultar instituições beneficentes da mantenedora

## Estória

Como **servidor de CRE que responde pelas instituições beneficentes de uma mantenedora**, quero
**consultar a relação das instituições beneficentes de uma mantenedora e abrir, a partir dela, o
registro da instituição que eu marcar**, para que **eu chegue ao registro certo pelo código INEP,
sem depender de saber de cor o código de cada instituição**.

O registro de uma instituição beneficente é grande — nome, endereço, bairro, número, CNPJ e a
coordenadoria regional escolar a que ela pertence — e não se procura por ele pelo nome. Quem
conhece a instituição conhece a **mantenedora** a que ela pertence e o **código INEP** dela. É
esta tela que liga as duas coisas: ela mostra as instituições beneficentes de uma mantenedora e
leva ao registro da que for escolhida. Sem ela, chegar a uma instituição depende de já saber de
cor o código dela, e a conferência do dia a dia da coordenadoria fica sem caminho.

Nada nesta tela é gravado: ela consulta e encaminha.

## Contexto

Jornada S000M → F000M → F100M → F118C.

Ator: servidor de CRE — consulta a relação das instituições beneficentes de uma mantenedora e
escolhe uma delas para abrir o registro dela em consulta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

Os dois menus do caminho — a `F000M` e a `F100M` — não leem cadastro de negócio nenhum e não
deixam dado de negócio para esta tela. Do que a sessão carrega, esta tela usa a **matrícula**, o
**código de acesso**, o **tipo de órgão** e a **data do sistema**, e mostra a **descrição do tipo
de órgão**; a **mantenedora da relação** é a que a sessão já tiver guardado de uma passagem
anterior (RN-02), e a **coordenadoria regional escolar do servidor não limita** o que a tela
relaciona (RN-01).

Esta tela é uma passagem: ela mostra a relação e, marcada uma instituição, **passa o registro
escolhido e a operação de consulta** para a tela da instituição beneficente (`F120T`), que abre
naquele registro e em consulta (RN-06). A jornada termina aqui porque esta tela é o índice —
quem mostra a instituição é a tela seguinte.

## Regras de negócio

### RN-01 — A tela consulta a relação das instituições beneficentes de uma mantenedora

Esta é uma tela de **consulta**. Ela mostra a relação das **instituições beneficentes de uma
mantenedora**, **doze por página**, em ordem crescente de **código INEP**. De cada instituição a
relação mostra o **código INEP**, o **nome da instituição**, a **coordenadoria regional escolar**
a que ela pertence, o **CNPJ do órgão** e o campo que marca a linha escolhida.

Acima da relação a tela mostra a **mantenedora** — o CNPJ e o nome dela —, o **código INEP por
onde a relação começa**, a **data do sistema** e a **descrição do tipo de órgão** da sessão.

O cadastro que a relação lê tem capacidade para **1.000** instituições beneficentes —
capacidade (máximo esperado, parâmetro de dimensionamento), não volume cadastrado.

A relação **não é recortada pela coordenadoria do servidor**: aparecem todas as instituições
beneficentes da mantenedora, de qualquer coordenadoria regional escolar.

[?] A chave por que a relação é lida admite repetição — o mesmo código INEP pode constar duas
vezes para a mesma mantenedora. Se a repetição é permitida de propósito, e o que a relação deve
mostrar quando ela acontece, pergunta ao site.

### RN-02 — A relação é de uma mantenedora, e a mantenedora precisa existir

A relação pertence a **uma mantenedora**, identificada pelo CNPJ. O servidor informa a
mantenedora na tela. Quando o CNPJ informado é o mesmo que a relação já está usando, a tela segue
sem conferir nada de novo; quando é **outro**, ele passa a ser a mantenedora da relação — com o
nome do cadastro dele — e a relação **recomeça da primeira instituição**.

A mantenedora informada é procurada no cadastro de mantenedoras:

- **em branco** — a tela recusa com **\* Informe a mantenedora \***, com o cursor de volta ao
  campo da mantenedora;
- **não encontrada** — a tela recusa com **\* Mantenedora nao cadastrada \***, também com o
  cursor de volta ao campo.

Nas duas recusas nada mais é feito naquela passagem.

[?] A relação é lida no caminho de apresentação da tela, e o caminho em que o servidor devolve a
tela preenchida só confere a mantenedora e guarda o CNPJ dela. O material lido não permite dizer
se a relação aparece na mesma passagem em que o servidor informa a mantenedora ou só na passagem
seguinte. Pergunta ao site.

### RN-03 — Sem mantenedora na sessão, a tela abre sem relação e sem aviso

Quando a sessão não tem nenhuma mantenedora guardada, a tela **não lê a relação**: não relaciona
instituição nenhuma e **não avisa nada**. O servidor vê a tela com os campos a preencher e
nenhuma linha preenchida — informar a mantenedora é o que começa a relação.

[?] O que a área da sessão guarda quando a tela é aberta direto do menu depende de quem passou
por ela antes e de uma comparação de CNPJ com zero, que é semântica de dialeto e não está no
material lido. Se a intenção era avisar que falta informar a mantenedora, por esse caminho o
aviso não sai. Pergunta ao site.

### RN-04 — A relação continua de onde parou

A tela aceita um **ponto de partida**: o **código INEP por onde a relação começa**. É por ele que
a leitura começa, e é ele que a tela guarda quando a página enche — o código INEP da última
instituição mostrada fica na linha do fim da página e na memória da sessão, de modo que a
abertura seguinte **continua a relação a partir dali**, em vez de voltar ao primeiro.

Quando a relação **acaba antes de a página encher**, o ponto de partida é esquecido e a abertura
seguinte **recomeça da primeira instituição**.

[?] O que os sinalizadores da leitura do cadastro fazem (posicionar, avançar) não está no corpus
nem no manual, e é isso que decide se a instituição do ponto de partida aparece de novo na
página seguinte ou se a leitura começa depois dela. Não afirmo qual dos dois. Pergunta ao site.

### RN-05 — Sem instituição beneficente para a mantenedora, a tela avisa

Quando a primeira linha da página **não encontra** instituição beneficente para a mantenedora, a
tela avisa **\* Nao existem inst.beneficentes cadastradas \***, esquece o ponto de partida e não
preenche a relação. As demais linhas da página ficam em branco, sem repetir o aviso.

### RN-06 — Marcada uma instituição, o registro dela se abre em consulta

Marcada uma linha da relação, a tela **não** segue com uma operação própria: ela passa o
**registro da instituição escolhida** — o código INEP da linha, com o CNPJ do órgão — e a
**operação de consulta** para a tela da instituição beneficente (`F120T`), que abre **naquele
registro** e **em consulta**. É essa passagem que dá sentido à tela: a relação é o índice, o
registro é o conteúdo, e é por ela que a jornada termina na tela seguinte.

A passagem só acontece nessa combinação: **instituição preenchida na linha** e **campo de
seleção da linha marcado**. Sem o código INEP na linha, a tela apenas segue mostrando a relação;
com o código INEP preenchido e o campo de seleção em branco, a tela também apenas segue, sem
abrir nada.

[?] O campo que marca a linha escolhida é lido e exibido, mas o material lido não traz o rótulo
que o servidor vê nem o valor que ele digita: a tela não tem conferência de valor para esse
campo, não tem mensagem própria para ele, e só mostra o literal que dispara a passagem. Pergunta
ao site.

### RN-07 — A tela não grava nada

Esta é uma tela de **consulta**: nada é gravado por ela. Nenhuma instituição beneficente,
nenhuma mantenedora e nenhum cadastro de tela é incluído, alterado ou apagado; nenhum registro é
travado; e nenhuma linha de auditoria é gerada. O único acesso que a tela faz aos cadastros é de
leitura.

### RN-08 — A tela não segue quando há uma tela anterior por terminar

Quando o **controle da tela anterior** está preenchido, a tela **não** segue com a consulta: ela
devolve o controle, e nada é relacionado nem aberto. O mesmo vale quando a passagem anterior
deixou um **erro marcado**: a tela para ali, sem continuar.

[?] A guarda é uma das primeiras do caminho, não tem mensagem própria, e o material lido não diz
o que preenche esse controle nem o que o servidor vê quando a guarda dispara. Ou é uma tela em
fim de operação, ou é um caminho que não deveria existir. Pergunta ao site.

### RN-09 — Os três códigos passam pela conferência de número antes da consulta

Os três códigos que o servidor informa nesta tela — o **código INEP da linha marcada**, a
**coordenadoria regional escolar** e o **código INEP por onde a relação começa** — passam por uma
conferência de número **antes** de qualquer consulta ao cadastro: o que não for número é
recusado no próprio campo, com o cursor de volta nele, e nada é consultado por causa disso. O
código deixado em branco é tratado como zero — e uma relação que começa em zero começa na
primeira instituição.

[?] O texto da recusa que o servidor vê quando um desses códigos não é número vem da rotina
comum de edição do sistema, que não está entre os fontes lidos; o que a tela faz é apontar em
qual campo o cursor volta. Pergunta ao site.

### RN-10 — A consulta exige que a tela esteja cadastrada e autorizada para o código de acesso

Toda passagem desta tela passa pelas conferências comuns do sistema: a tela tem de estar
**cadastrada** — senão **\* Tela nao disponivel \*** — e o **código de acesso** da matrícula tem
de ter a tela autorizada — senão **\* Acesso negado para esta matricula \***. Sem isso, a relação
não é lida.

A tela também monta a **operação de consulta** e a submete à conferência de permissão do código
de acesso.

[?] O cadastro de permissões guarda as quatro operações separadas — inclusão, alteração, exclusão
e consulta —, mas a rotina comum de conferência só tem ramos para inclusão, alteração e
exclusão: não há ramo para a consulta, e o caminho termina sem exigir a permissão de consulta. Se
o campo da operação chegar em branco, o ramo que sobra exige a permissão de **alteração**. Qual
das duas coisas acontece depende de o campo da operação voltar preenchido do terminal, o que o
fonte desta tela não fecha. Se a intenção era exigir a permissão de consulta, o caminho não a
exige. Pergunta ao site.

### RN-11 — Falha de leitura do cadastro interrompe a consulta e avisa

Toda leitura desta tela testa o erro do banco de dados. Um erro de leitura vira a ação de erro de
acesso do sistema, com a mensagem de erro do sistema, e a operação para ali, sem completar a
relação.

### RN-12 — A data do sistema, o tipo de órgão e o nome da mantenedora aparecem e não são digitáveis

A tela mostra a **data do sistema** e a **descrição do tipo de órgão** da sessão, e o **nome da
mantenedora** da relação. Os três são informação de saída — o servidor os vê, mas o terminal não
os devolve ao programa —, e cada passagem da tela começa apagando os três, para que não fique na
tela o que a passagem anterior mostrou.

## Cenários BDD

```gherkin
Funcionalidade: Consultar as instituições beneficentes de uma mantenedora e abrir o registro da escolhida

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F118C

  Cenário: Abrir a tela e listar as instituições beneficentes da mantenedora
    Dado que a mantenedora da relação é a mantenedora de instituições beneficentes cadastradas
    Quando abro a tela
    Então vejo, em até doze linhas, o código INEP, o nome, a coordenadoria regional escolar e o CNPJ de cada instituição
    E vejo a mantenedora, a data do sistema e a descrição do tipo de órgão da minha sessão
    E nada é gravado

  Cenário: A relação não é recortada pela minha coordenadoria
    Dado que a mantenedora tem instituições beneficentes de mais de uma coordenadoria regional escolar
    Quando abro a tela
    Então vejo as instituições de todas as coordenadorias daquela mantenedora
    E não apenas as da minha

  Cenário: Informar a mantenedora que a relação deve mostrar
    Dado que informo o CNPJ de uma mantenedora cadastrada
    Quando confirmo
    Então a relação passa a ser a das instituições beneficentes daquela mantenedora
    E o nome mostrado é o nome dela

  Cenário: Trocar a mantenedora reinicia a relação
    Dado que a relação já está sendo mostrada para uma mantenedora
    Quando informo o CNPJ de outra mantenedora cadastrada
    Então a relação recomeça da primeira instituição beneficente dela

  Cenário: Informar uma mantenedora que não está cadastrada
    Dado que informo o CNPJ de uma mantenedora que não existe
    Quando confirmo
    Então vejo a mensagem "* Mantenedora nao cadastrada *"
    E o cursor volta para o campo da mantenedora
    E nada mais é feito nessa passagem

  Cenário: Não informar a mantenedora
    Dado que deixo o campo da mantenedora em branco
    Quando confirmo
    Então vejo a mensagem "* Informe a mantenedora *"
    E o cursor volta para o campo da mantenedora

  Cenário: Abrir a tela sem mantenedora na sessão
    Dado que a sessão não tem nenhuma mantenedora guardada
    Quando abro a tela
    Então não vejo nenhuma instituição beneficente relacionada
    E não vejo nenhuma mensagem de aviso

  Cenário: A relação continua de onde parou
    Dado que a relação mostrou uma página cheia de instituições beneficentes
    Quando abro a tela de novo
    Então a relação continua a partir do último código INEP que tinha sido mostrado

  Cenário: A relação acaba antes de a página encher
    Dado que a mantenedora tem menos instituições beneficentes do que cabem na página
    Quando abro a tela de novo
    Então a relação recomeça da primeira instituição beneficente da mantenedora

  Cenário: A mantenedora não tem instituição beneficente
    Dado que a mantenedora não tem nenhuma instituição beneficente cadastrada
    Quando abro a tela
    Então vejo a mensagem "* Nao existem inst.beneficentes cadastradas *"
    E nenhuma linha da relação é preenchida

  Cenário: Marcar uma instituição e abrir o registro dela
    Dado que a relação mostra as instituições beneficentes da mantenedora
    E marco uma linha com o código INEP preenchido e o campo de seleção marcado
    Quando confirmo
    Então o registro daquela instituição beneficente se abre em consulta
    E nada é gravado por esta tela

  Cenário: Marcar o campo de seleção sem a instituição na linha
    Dado que a linha está com o campo de seleção marcado
    E o código INEP da linha está em branco
    Quando confirmo
    Então nenhum registro se abre
    E a tela segue mostrando a relação

  Cenário: Linha preenchida sem o campo de seleção marcado
    Dado que a linha está com o código INEP preenchido
    E o campo de seleção da linha está em branco
    Quando confirmo
    Então nenhum registro se abre
    E a tela segue mostrando a relação

  Cenário: A consulta não grava nada
    Dado que localizei uma instituição beneficente pela relação
    E que marco uma linha da relação
    Quando confirmo
    Então nenhuma instituição beneficente, mantenedora ou cadastro de tela é incluído, alterado ou apagado
    E nenhum registro é travado
    E nenhuma linha de auditoria é gerada

  Cenário: Há uma tela anterior por terminar
    Dado que o controle da tela anterior está preenchido
    Quando confirmo
    Então a tela devolve o controle
    E nada é relacionado nem aberto

  Cenário: Código que não é número
    Quando informo, em um dos códigos da tela, algo que não é número
    Então a tela recusa o código antes de consultar o cadastro
    E o cursor volta para o campo do código

  Cenário: Código em branco vale zero
    Dado que deixo o código INEP inicial da relação em branco
    Quando confirmo
    Então a relação começa na primeira instituição beneficente da mantenedora

  Cenário: Tela não cadastrada
    Dado que a tela F118C não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo consultar

  Cenário: Sem autorização para a tela
    Dado que o código de acesso da minha matrícula não tem a tela F118C autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo consultar

  Cenário: Falha na leitura do cadastro
    Dado que a leitura do cadastro falha
    Quando abro a tela
    Então vejo a mensagem de erro do sistema
    E a relação não é completada

  Cenário: Os dados de saída da tela
    Quando abro a tela
    Então vejo a data do sistema, a descrição do tipo de órgão da minha sessão e o nome da mantenedora
    E esses três dados não são digitáveis
```
