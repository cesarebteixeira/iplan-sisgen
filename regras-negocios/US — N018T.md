# US — N018T — Número próprio e relatório da entrega

## Estória

Como **servidor da Coordenadoria Regional de Ensino que responde pela prestação de
contas**, quero **separar, por fornecedor, o que já está pronto para ser prestado e
entregar adiante o que ainda precisa de número, imprimindo o relatório do que vai ser
entregue**, para que **cada fornecedor da minha coordenadoria receba a sua remessa com
o número próprio e com o papel que acompanha a entrega, e nada seja entregue sem essa
identificação**.

O fornecedor entrega a nota fiscal; a nota é lançada num processo, e um processo reúne
as notas de um fornecedor. Esta tela é o posto onde o servidor vê o que já está fechado
para o fornecedor escolhido e decide o destino daquela remessa: entregá-la adiante para
receber o número próprio, ou imprimir o documento que a acompanha. Sem isso, os
processos fechados ficariam parados sem número e sem o papel que a entrega exige, e a
prestação de contas não avançaria.

## Contexto

Jornada S000M → N000M → N060M → N018T.
Ator: servidor de CRE — escolhe a coordenadoria, o fornecedor e o lote, e decide, para
cada processo que o sistema lista, se ele segue adiante para receber o número próprio
ou se o relatório da entrega é impresso.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US — 00
Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu a abre —
está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

Esta tela não é o fim da jornada: o desfecho dela entrega o processo adiante (RN-10).
O que ela entrega — e por que o caminho de volta fica fechado por causa disso — é
regra desta tela, e não contexto.

## Regras de negócio

### RN-01 — Quem entra precisa ter permissão para esta tela

Antes de abrir, a tela se apresenta ao catálogo de telas do sistema — ela precisa estar
cadastrada e vigente ali — e confere se o servidor tem autorização de acesso para ela.
Faltando qualquer uma das duas coisas, a tela não abre e a sessão segue o rumo que o
próprio cadastro de telas mandar.

### RN-02 — A coordenadoria é a do servidor: quem é de outra não trabalha aqui

A coordenadoria regional escolar informada na tela tem de ser a mesma da sessão do
servidor. Sendo outra, o sistema recusa com **\<- Ususario sem acesso a outro grupo \***,
devolve o cursor ao campo da coordenadoria e não segue: nada é listado, nada é entregue
e nada é impresso. A tela reapresenta, então, a coordenadoria da sessão.

[?] A conferência só acontece quando a sessão traz uma coordenadoria diferente de zero.
Se a sessão vier sem coordenadoria, a conferência não roda e a tela aceita a
coordenadoria informada sem comparar. Se isso é intencional — por exemplo, para o
servidor que responde por mais de uma coordenadoria — ou é furo da conferência,
pergunta ao site.

### RN-03 — O fornecedor é obrigatório e tem de estar cadastrado

Sem fornecedor informado, o sistema recusa com **\* Informe o fornecedor \*** e devolve o
cursor ao campo do fornecedor. Informado, ele tem de existir no cadastro de
fornecedores; não existindo, a recusa é **\* Fornecedor nao cadastrado \***. Nas duas, a
tela não segue: nada é listado, nada é entregue e nada é impresso.

### RN-04 — O que a tela lista: os processos fechados do fornecedor, com o que cada um reúne

Escolhidos a coordenadoria e o fornecedor, a tela percorre os lançamentos daquele
fornecedor e mostra, em **12 linhas**, cada processo que tenha lançamento — o número do
processo no formato da tela, o tipo de contrato, o tipo do processo e a sua descrição e
o **valor total do processo**. O valor total de cada processo é a **soma dos valores
totais dos seus itens**: a tela percorre os itens do processo e soma; os itens marcados
como excluídos ficam de fora da soma.

[?] A lista não é escolhida só pelo fornecedor. A tela lê os lançamentos pela
coordenadoria, pelo fornecedor e por um número de processo, e devolve a esse número o
último processo mostrado — de modo que a tela seguinte de uma mesma consulta começa
depois dele. É esse número, que o servidor vê no campo do lote, que faz a consulta
avançar de página. Se é isso que o servidor espera ao reenviar a tela, ou se ele espera
ver a lista recomeçar do primeiro processo, pergunta ao site.

### RN-05 — Não havendo o que listar, a tela avisa e para

Quando a leitura dos processos fechados do fornecedor não encontra o que listar, a tela
avisa **\* Nao existem processos fechados \***, encerra a listagem e devolve o controle
ao começo da tela, para o servidor recomeçar a escolha.

[?] O aviso é dado pela mesma marca que indica "não encontrei" para cada leitura de
processo, e não por um contador do que a tela já listou. Se um dia a leitura de um dos
processos da lista falhar no meio, o aviso "não existem processos fechados" aparece —
embora existam. Se o aviso deveria considerar só a lista vazia, pergunta ao site.

### RN-06 — A tela só opera em consulta

Esta tela não inclui, não altera e não exclui nada dos cadastros do processo. A operação
com que ela trabalha é a **consulta**: qualquer outra operação é recusada com
**\* Operacao nao disponivel. Use CON \***, com o cursor de volta no campo da operação,
e nada é listado, entregue ou impresso.

[?] A recusa da operação diferente de consulta não fecha com o resto do fonte: na
passagem que faz a conferência, a própria tela já havia reposto a operação como
consulta, de modo que a comparação que dispara a recusa encontra sempre o valor
esperado. Ou a recusa vale para um caminho que esta jornada não percorre, ou o caminho
ficou inalcançável. Pergunta ao site.

### RN-07 — O que a tela entrega: o número próprio do processo, ou o relatório da entrega

O que a tela faz com cada processo depende da **situação** que o processo traz, na
lista:

- **processo que ainda não tem número próprio e não foi entregue para impressão** — ele
  segue adiante para receber o número próprio (RN-08);
- **processo entregue para impressão** — o sistema registra a impressão do relatório da
  entrega (RN-09).

Processo em qualquer outra situação não gera nem número nem impressão: a tela passa
adiante sem fazer nada com ele. Um processo que tenha ido para o número próprio sai
daqui marcado como fechado e com o número já atribuído, e é a tela seguinte que
continua o trabalho.

[?] Os valores gravados pela situação de "sem número próprio" e de "entregue para
impressão" — **X** e **I** — são os únicos que a tela conhece, e de onde eles vêm (do
processo ou de uma escolha do servidor) não está nos fontes desta jornada. É pergunta ao
site.

### RN-08 — Verificado que há o que entregar, a tela dá o número próprio ao processo

Antes de entregar o processo adiante, a tela confere que o fornecedor tem processo
fechado a entregar; não tendo, avisa **\* Nao existem proc.fechados para este fornecedor \***,
devolve o cursor ao campo do fornecedor e para. Havendo, ela atribui ao processo o
**número próprio seguinte** e o devolve à tela seguinte marcado como fechado, com a
quantidade de notas e os totais apurados. A gravação do número é a operação que trava o
registro e o regrava com o número novo.

### RN-09 — Para imprimir, a tela exige impressora, e-mail e que não haja pedido em andamento

Para registrar a impressão do relatório da entrega, a tela exige três coisas, nesta
ordem, e recusa nas três com o cursor de volta ao campo da impressora:

- **impressora** — sem impressora informada, **\* Informe a impressora \***;
- **nenhum pedido em andamento** — já existindo pedido de relatório daquela
  coordenadoria que ainda não terminou, **\* Relatorio em processamento. Aguarde. \***;
- **e-mail cadastrado** — o relatório é enviado, e o servidor sem e-mail cadastrado
  recebe **\* Usuario sem e-mail cadastrado \***.

Passando pelas três, a tela **registra o pedido de impressão**: o relatório, a
impressora, **uma cópia**, o e-mail do servidor, a matrícula, o órgão, a coordenadoria,
o processo, a estação e a data. O pedido entra na fila e não altera o processo nem as
notas dele — quem imprime é o processamento, fora desta tela.

[?] O aviso pede a impressora, mas este fonte não mostra a tela recebendo impressora
digitada: o campo da impressora é preenchido com a impressora padrão do cadastro do
servidor. Se o servidor pode trocar a impressora nesta tela, e de onde o campo viria, é
pergunta ao site.

### RN-10 — O que a tela entrega à tela seguinte, e por que o caminho de volta fica fechado

Entregue o processo adiante (RN-08), a tela da jornada que recebe o processo **só se
deixa abrir por quatro telas** — esta entre elas — e manda de volta ao menu de
processos qualquer outra origem, marcando a sessão como vinda da família da tela do
processo. O menu, ao ver essa marca, bloqueia a opção que leva ao processo e avisa
**\* Acesso deve ser feito pela tela N016T \***.

Por isso a passagem daqui tem de levar tudo o que a tela seguinte precisa para trabalhar
sozinha: **qual processo**, **a operação** e o que mais ela mostra do processo. Sem
isso, quem lê esta estória isolada não reproduz a passagem — e o processo entregue por
aqui não voltaria a ser aberto por nenhum caminho.

## Cenários BDD

```gherkin
Funcionalidade: Processos fechados do fornecedor — dar o número próprio e imprimir o relatório da entrega

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N018T

  Cenário: RN-02 — a coordenadoria é a da minha sessão
    Dado que estou na tela com a coordenadoria da minha sessão
    Quando informo o fornecedor e envio
    Então a tela segue e lista os processos do fornecedor

  Cenário: RN-02 — coordenadoria de outro grupo é recusada
    Dado que informo uma coordenadoria diferente da minha
    Quando envio a tela
    Então vejo a mensagem "<- Ususario sem acesso a outro grupo *"
    E o cursor volta ao campo da coordenadoria
    E nada é listado, entregue ou impresso

  Cenário: RN-03 — fornecedor não cadastrado é recusado
    Dado que informo um fornecedor que não existe no cadastro
    Quando envio a tela
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo do fornecedor
    E nada é listado, entregue ou impresso

  Cenário: RN-04 — a tela lista os processos fechados com o que cada um reúne
    Dado que informei a minha coordenadoria e um fornecedor cadastrado
    Quando envio a tela
    Então vejo até 12 linhas, uma por processo, com o número do processo, o tipo de contrato, o tipo do processo e o valor total
    E o valor total de cada processo é a soma dos itens dele, sem os itens excluídos
    E nada é gravado por causa da consulta

  Cenário: RN-05 — não havendo o que listar, a tela avisa e para
    Dado que o fornecedor informado não tem processo fechado a listar
    Quando envio a tela
    Então vejo a mensagem "* Nao existem processos fechados *"
    E a listagem não continua

  Cenário: RN-06 — operação diferente de consulta é recusada
    Dado que enviei a tela com uma operação que não é a consulta
    Quando a tela confere a operação
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nada é listado, entregue ou impresso

  Cenário: RN-08 — sem processo fechado a entregar, a tela recusa
    Dado que o fornecedor informado não tem processo fechado para entregar
    Quando envio a tela
    Então vejo a mensagem "* Nao existem proc.fechados para este fornecedor *"
    E o cursor volta ao campo do fornecedor
    E nada é gravado

  Cenário: RN-08 — o processo sem número próprio recebe o número seguinte
    Dado que o fornecedor tem processo fechado a entregar
    Quando envio a tela
    Então o processo recebe o número próprio seguinte
    E o processo é entregue à tela seguinte marcado como fechado, com a quantidade de notas e os totais
    E fica registrado o número atribuído

  Cenário: RN-09 — recusa imprimir sem impressora informada
    Dado que o processo está entregue para impressão
    E não há impressora informada
    Quando envio a tela
    Então vejo a mensagem "* Informe a impressora *"
    E o cursor volta ao campo da impressora
    E nada é impresso

  Cenário: RN-09 — recusa imprimir enquanto há pedido em andamento
    Dado que já existe pedido de relatório da minha coordenadoria em processamento
    Quando peço a impressão do relatório da entrega
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da impressora
    E nada é impresso

  Cenário: RN-09 — recusa imprimir sem e-mail cadastrado
    Dado que o meu cadastro de servidor não tem e-mail
    Quando peço a impressão do relatório da entrega
    Então vejo a mensagem "* Usuario sem e-mail cadastrado *"
    E o cursor volta ao campo da impressora
    E nada é impresso

  Cenário: RN-09 — o pedido de impressão entra na fila
    Dado que tenho impressora e e-mail cadastrado
    E não há pedido de relatório em andamento
    Quando peço a impressão do relatório da entrega
    Então o pedido de impressão fica registrado, com uma cópia
    E o processo e as notas dele não são alterados

  Cenário: RN-07 — processo em situação que a tela não trata passa sem operação
    Dado que o processo listado tem uma situação diferente das duas que a tela trata
    Quando envio a tela
    Então nada é entregue para número próprio
    E nada é impresso
```
