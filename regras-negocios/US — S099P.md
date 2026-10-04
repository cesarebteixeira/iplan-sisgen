# US — S099P — Requisitar o processamento do relatório com os parâmetros informados

## Estória

Como **servidor de CRE**, quero **informar os parâmetros do pedido que escolhi e
requisitar o seu processamento**, para que **o relatório saia na impressora que
indiquei, sem eu depender de quem opera o processamento em lote**.

O relatório não é montado nesta tela: ele roda em lote, depois. O que a tela faz é
conferir se o pedido pode ser feito — se o nível de acesso e a coordenação regional
informados existem, se a listagem pedida tem o que listar para a data que eu digitei,
se já não há um pedido do mesmo tipo esperando na fila — e, passando, **registrar o
pedido e disparar o processamento**. Sem o pedido registrado, o processamento não tem
trabalho a executar; e pedir duas vezes o mesmo trabalho só ocuparia a fila — por isso
o pedido repetido é recusado enquanto o primeiro não é consumido.

A tela não altera nem exclui nada do que já está cadastrado, e não deixa registro de
auditoria: o único cadastro que ela escreve é o da própria fila de pedidos, e só
incluindo.

## Contexto

Jornada S000M → S001M → S006M → S099P.
Ator: servidor de CRE — informa os parâmetros do relatório escolhido no passo anterior
e confirma o pedido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Esta tela **não é aberta por menu**: quem a chama é a tela de impressão `S006M`, que
passa adiante, sem menu nenhum, o **tipo de pedido** que o operador escolheu e a
**impressora** que ele informou. O tipo de pedido decide qual dos quatro conjuntos de
parâmetros a tela trabalha — e é por isso que a regra do tipo de pedido está aqui, e
não na tela anterior. A sessão traz ainda a matrícula, o tipo de órgão e a coordenação
regional de quem opera, que a tela usa nas conferências.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela registra o pedido e dispara o processamento

Confirmado e passando pelas conferências, o sistema registra um **pedido novo na fila**
— com a data do sistema, a matrícula de quem pediu, o tipo de órgão, a coordenação
regional (no tipo que se resolve por ela), a estação, a impressora da sessão e o bloco
de parâmetros do tipo de pedido — e em seguida **submete o processamento**
correspondente. São dois processamentos em lote, e qual deles é submetido depende do
tipo de pedido: um para o primeiro e o terceiro tipos, outro para o segundo e o quarto.

Essa é a única escrita da tela, e é sempre uma inclusão. A fila é a mesma para todas as
telas do sistema, e quem retira dela o pedido é o processamento que o consome.

[?] O disparo só acontece se um estado interno, limpo pela própria tela antes de
gravar, voltar com um valor que **nenhum** programa do lote atribui — só a rotina de
gravação, que é do ambiente e não tem fonte no lote, poderia atribuí-lo. Não voltando
esse valor, o pedido fica registrado na fila e o processamento não é submetido.
Pergunta ao site.

### RN-02 — O pedido recebe o próximo número da fila

O número do pedido **não é digitado**: o sistema procura o último pedido já registrado
na fila e toma o seguinte. É esse número que identifica o pedido daí em diante.

[?] Com a fila vazia, o número sai do que estiver na área do registro lido — que, não
achando nada, não é reposta. Se ela guardar valor de uma leitura anterior, dois pedidos
podem acabar com o mesmo número. Pergunta ao site.

### RN-03 — São quatro tipos de pedido, e o tipo vem decidido pela tela anterior

O **tipo de pedido** chega escolhido no passo anterior e a tela reconhece quatro:

- o **primeiro**, que se resolve pelo **nível de acesso**;
- o **segundo**, que se resolve pela **coordenação regional** e pelo **nível de
  acesso** — e cuja abertura já repõe no campo a coordenação regional da sessão;
- o **terceiro**, que se resolve pelo **módulo**;
- o **quarto**, que se resolve pela **data inicial** e pela **listagem** pedida.

Na abertura, para cada tipo, a tela assinala com um asterisco **os campos que aquele
tipo usa** e deixa o cursor no primeiro deles. No primeiro tipo, o nível de acesso. No
segundo, a coordenação regional e o nível de acesso. No terceiro, o módulo. No quarto, a
data inicial, a matrícula, dois códigos de tela, a coordenação regional, a subclasse e o
gênero, o número do pedido e o ano da entrega, a listagem e o arquivo, e as quatro
partes do número do processo. Os campos dos outros tipos não são assinalados.

Um tipo de pedido que a tela não reconhece — isto é, o passo anterior não tendo deixado
nenhum dos quatro — **abre a tela e não faz mais nada**: não assinala campo, não
confere, não registra e não avisa quem opera.

[?] O que o asterisco faz na máscara — se apenas aponta o campo, se o exige ou se o
impede de ser digitado — não está no acervo; o mesmo vale para os rótulos que a máscara
dá aos campos que não passam pela edição numérica, entre eles os dois códigos de tela do
quarto tipo. Pergunta ao site.

[?] Os quatro tipos são identificados por códigos de relação, e o nome de negócio de
cada um está na máscara da tela anterior, que não veio no lote: nesta estória eles só
podem ser descritos pelos parâmetros que pedem. Pergunta ao site.

### RN-04 — Antes de registrar, a tela passa pelas conferências de acesso

Ao **abrir**, a tela confere que ela própria está cadastrada e que o código de acesso de
quem opera a tem, e — na sequência das conferências comuns de acesso — confere se **a
relação escolhida no passo anterior está autorizada** para aquele código de acesso. Não
estando a tela cadastrada, a recusa é **\* Tela nao disponivel \***; não tendo a
matrícula a tela no seu código de acesso, **\* Acesso negado para esta matricula \***.

Ao **confirmar**, as conferências comuns de acesso conferem o encaminhamento e a
autorização da operação: não estando a tela cadastrada, **\* Tela nao cadastrada \***;
operação que o sistema não reconhece, **\* Operacao nao disponivel \***; e, sem o
liberador daquela operação no código de acesso, **\* Acesso negado para esta operacao
\***. Em qualquer desses casos nada é registrado e nenhum processamento é disparado.

[?] A **relação escolhida que não está cadastrada passa sem recusa**: a rotina que a
procura marca um estado de recusa, mas a rotina de mensagens não tem texto para esse
estado, e o resultado volta como aprovado. Se a intenção era recusar a relação não
cadastrada, esse caminho não recusa. Pergunta ao site.

[?] A **operação que a tela envia vem da máscara** e a tela não a repõe em momento
nenhum: mandando a máscara a operação em branco, a conferência da operação aprova;
mandando inclusão, exige o liberador de inclusão. Qual valor a máscara manda não está no
lote. Pergunta ao site.

### RN-05 — Um pedido de cada vez, por tipo e por órgão

Antes de registrar, cada tipo procura na fila um pedido **do mesmo tipo, para o mesmo
órgão** — no segundo tipo, para a coordenação regional informada; nos outros três, sem
distinguir a coordenação. Havendo, recusa com **\* Programa em processamento. Aguarde.
\*** e abandona: nenhum pedido novo é registrado e nenhum processamento é disparado.

A procura não olha a situação do pedido nem a data: é qualquer pedido daquele tipo para
aquele órgão. É o próprio pedido registrado por esta tela que satisfaz a procura
seguinte — é assim que o mesmo trabalho fica bloqueado enquanto não sai da fila. O
cursor volta ao campo da coordenação regional no primeiro e no segundo tipos, e ao campo
do dia inicial no terceiro e no quarto.

[?] Quem tira o pedido da fila é o processamento que o consome, e a entrada também apaga
pedidos antigos na abertura do `LOGON` — nem o prazo nem a condição exata dessa limpeza
pertencem a esta jornada. Pergunta ao site.

[?] A fila comporta **90 mil pedidos**: esse número é a capacidade declarada — o máximo
esperado, parâmetro de dimensionamento —, e não o volume de pedidos existentes, que o
acervo não informa.

### RN-06 — O nível de acesso informado tem de estar cadastrado

No primeiro e no segundo tipos, o **nível de acesso** informado é procurado no cadastro
de níveis de acesso. Não estando cadastrado, a recusa é **\* Nivel de acesso nao
cadastrado \***, com o cursor de volta ao campo do nível de acesso, e nada é registrado.

### RN-07 — No tipo por coordenação regional, a coordenação, o e-mail e os servidores do nível

No segundo tipo, além do nível de acesso, a tela exige três coisas:

- a **coordenação regional** informada tem de ser a **da sessão** — se a sessão tem
  coordenação e o campo traz outra, a recusa é **\* Usuario sem acesso a outro grupo
  \***, com o cursor de volta à coordenação;
- o **servidor que pede** tem de ter e-mail cadastrado — não tendo, a recusa é
  **\* Usuario sem e-mail cadastrado \***, também com o cursor de volta à coordenação;
- tem de existir **pelo menos um servidor ativo** com vínculo naquela coordenação e
  naquele nível de acesso — não havendo, a recusa é **\* Usuarios nao cad neste nivel de
  acesso \***, com o cursor de volta ao campo do nível de acesso.

[?] A conferência da coordenação regional contra a da sessão só existe **neste** tipo de
pedido: nos outros três a coordenação informada não é comparada com a da sessão. E, como
a abertura repõe a coordenação da sessão no campo, essa recusa só é alcançável se o
operador trocar a coordenação na confirmação. Se a intenção era restringir a coordenação
em todos os tipos, os outros caminhos não restringem. Pergunta ao site.

### RN-08 — No tipo por módulo, o módulo tem de ser um dos válidos

No terceiro tipo, o **módulo** informado tem de ser um dos sete aceitos. Não sendo, a
recusa é **\* Informe modulo com C/E/F/M/N/P/S \***, com o cursor de volta ao campo do
módulo, e nada é registrado.

### RN-09 — No tipo por data, o dia inicial é obrigatório

No quarto tipo, o **dia inicial** tem de estar informado: em branco, a recusa é
**\* Informe a data \***, com o cursor de volta ao campo do dia. O mês e o ano não
passam por essa conferência — só o dia é exigido.

### RN-10 — No tipo por data, a listagem pedida tem de ter o que listar

Ainda no quarto tipo, antes de registrar, a tela confere a **listagem pedida** contra o
que existe para a data informada. A conferência depende da listagem:

- **sem listagem informada**, a tela procura a **auditoria** do órgão naquele dia, mês
  e ano — não havendo, a recusa é **\* Nao existe auditoria para esta data \***, com o
  cursor de volta ao dia;
- pedindo a **listagem de pagamentos**, a tela procura os **pagamentos do órgão naquele
  mês e ano** — não havendo, a recusa é **\* Nao existe registros para esta data \***,
  com o cursor de volta ao dia;
- pedindo a **listagem de um processo**, a tela monta o **número do processo** com as
  partes informadas e procura o processo **pendente** — cadastrado e ainda não
  processado —; não havendo, a recusa é **\* Processo nao cadastrado \***, com o cursor
  de volta ao campo do número do processo;
- pedindo a **listagem a partir de arquivo**, a tela exige que o **nome do arquivo**
  esteja informado — não estando, a recusa é **\* Informe arquivo \***, com o cursor de
  volta ao campo do arquivo.

Informando qualquer outra listagem, nenhuma dessas conferências é feita e o pedido
segue.

[?] O que cada listagem nomeia, em termos de negócio, não está no acervo: os valores que
a tela reconhece são códigos, um deles nem é nome de tela, e o rótulo da máscara para
esse campo não veio no lote. Pergunta ao site.

### RN-11 — No tipo por data, a matrícula informada tem de existir e o servidor ter e-mail

Ainda no quarto tipo: se a **matrícula** for informada, ela tem de estar cadastrada —
não estando, a recusa é **\* Matricula nao cadastrada \***, com o cursor de volta ao
campo da matrícula; e o **servidor que pede** tem de ter e-mail cadastrado — não tendo,
a recusa é **<- Usuario sem e-mail cadastrado \*** (a mensagem sai assim mesmo), com o
cursor de volta ao campo do dia.

### RN-12 — A digitação dos campos numéricos é editada, e o cursor volta ao campo recusado

Na confirmação, e **antes** de qualquer conferência de cadastro, os **14 campos
numéricos** da tela passam por edição: o dia e o mês com dois dígitos, o ano com quatro,
a matrícula com nove, a coordenação regional e o nível de acesso com dois, a subclasse
com dois, o gênero com cinco, o número do pedido com seis, o ano da entrega com quatro,
e as quatro partes do número do processo com dois, dois, seis e quatro. Campo em branco
é tratado como zero, e o que não for número é recusado, com o cursor devolvido ao campo.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não
está no acervo: a rotina que faz a edição numérica é importada do ambiente e não tem
fonte no lote. A estória registra só o cursor de volta ao campo. Pergunta ao site.

### RN-13 — A tela só inclui na fila; não altera, não exclui e não deixa auditoria

A tela lê o cadastro de telas, o cadastro de funcionários, os vínculos do servidor com o
órgão, os níveis de acesso, os pagamentos, a auditoria e a própria fila de pedidos —
**sete** cadastros. Ela **escreve só na fila**, e só incluindo: nenhum registro
existente é alterado ou excluído e nenhum registro de auditoria é gerado. As operações
de gravação, de exclusão e de travamento existem **declaradas** para os cadastros que a
tela enxerga, mas **não são executadas em caminho nenhum** — declarar não é executar.

---

## Cenários BDD

```gherkin
Funcionalidade: Requisitar o processamento do relatório com os parâmetros informados

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S099P
    E escolhi o tipo de pedido e a impressora no passo anterior

  Cenário: A abertura assinala os campos do tipo de pedido
    Dado que escolhi um dos quatro tipos de pedido
    Quando abro a tela
    Então os campos que aquele tipo usa aparecem assinalados com um asterisco
    E o cursor fica no primeiro deles
    E, no tipo por coordenação regional, a coordenação já vem preenchida com a da minha sessão

  Cenário: A abertura não registra nada
    Dado que abri a tela e ainda não confirmei
    Então nenhum pedido foi registrado
    E nenhum processamento foi disparado

  Cenário: Tipo de pedido que a tela não atende
    Dado que o passo anterior não deixou nenhum dos quatro tipos de pedido
    Quando confirmo a tela
    Então nenhum campo aparece assinalado
    E nenhuma conferência é feita
    E nenhum pedido é registrado
    E nenhuma mensagem aparece

  Cenário: Pedido do primeiro tipo
    Dado que escolhi o tipo que se resolve pelo nível de acesso
    E informei um nível de acesso cadastrado
    E não há pedido desse tipo na fila para o meu órgão
    Quando confirmo a tela
    Então um pedido novo é registrado na fila, com o próximo número
    E o processamento correspondente é disparado

  Cenário: Pedido do segundo tipo
    Dado que escolhi o tipo que se resolve pela coordenação regional
    E o meu cadastro tem e-mail
    E existe servidor ativo naquela coordenação e naquele nível de acesso
    Quando confirmo a tela
    Então um pedido novo é registrado na fila, com a coordenação da minha sessão
    E o processamento correspondente é disparado

  Cenário: Pedido do terceiro tipo
    Dado que escolhi o tipo que se resolve pelo módulo
    E informei um dos sete módulos aceitos
    Quando confirmo a tela
    Então um pedido novo é registrado na fila
    E o processamento correspondente é disparado

  Cenário: Pedido do quarto tipo
    Dado que escolhi o tipo que se resolve pela data inicial
    E informei o dia, o mês e o ano iniciais
    E a listagem pedida tem o que listar para aquela data
    E o meu cadastro tem e-mail
    Quando confirmo a tela
    Então um pedido novo é registrado na fila
    E o processamento correspondente é disparado

  Cenário: Pedido repetido enquanto o anterior está na fila
    Dado que já existe um pedido do mesmo tipo para o meu órgão
    Quando confirmo a tela
    Então vejo a mensagem "* Programa em processamento. Aguarde. *"
    E nenhum pedido novo é registrado
    E nenhum processamento é disparado

  Cenário: Nível de acesso não cadastrado
    Dado que informei um nível de acesso que não está cadastrado
    Quando confirmo a tela
    Então vejo a mensagem "* Nivel de acesso nao cadastrado *"
    E o cursor volta ao campo do nível de acesso
    E nada é registrado

  Cenário: Coordenação regional de outro grupo
    Dado que escolhi o tipo que se resolve pela coordenação regional
    E tenho coordenação regional na minha sessão
    E informei uma coordenação diferente da minha
    Quando confirmo a tela
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo da coordenação
    E nada é registrado

  Cenário: Servidor sem e-mail cadastrado, no tipo por coordenação regional
    Dado que escolhi o tipo que se resolve pela coordenação regional
    E o meu cadastro não tem e-mail
    Quando confirmo a tela
    Então vejo a mensagem "* Usuario sem e-mail cadastrado *"
    E o cursor volta ao campo da coordenação
    E nada é registrado

  Cenário: Nenhum servidor no nível de acesso
    Dado que escolhi o tipo que se resolve pela coordenação regional
    E não existe servidor ativo naquela coordenação e naquele nível de acesso
    Quando confirmo a tela
    Então vejo a mensagem "* Usuarios nao cad neste nivel de acesso *"
    E o cursor volta ao campo do nível de acesso
    E nada é registrado

  Cenário: Módulo inválido
    Dado que escolhi o tipo que se resolve pelo módulo
    E informei um módulo fora dos sete aceitos
    Quando confirmo a tela
    Então vejo a mensagem "* Informe modulo com C/E/F/M/N/P/S *"
    E o cursor volta ao campo do módulo
    E nada é registrado

  Cenário: Dia inicial em branco
    Dado que escolhi o tipo que se resolve pela data inicial
    E deixei o dia inicial em branco
    Quando confirmo a tela
    Então vejo a mensagem "* Informe a data *"
    E o cursor volta ao campo do dia
    E nada é registrado

  Cenário: Sem auditoria para a data informada
    Dado que escolhi o tipo que se resolve pela data inicial
    E não informei a listagem
    E não há auditoria do meu órgão para aquela data
    Quando confirmo a tela
    Então vejo a mensagem "* Nao existe auditoria para esta data *"
    E o cursor volta ao campo do dia
    E nada é registrado

  Cenário: Sem pagamentos no mês e no ano informados
    Dado que pedi a listagem de pagamentos
    E não há pagamento do meu órgão naquele mês e ano
    Quando confirmo a tela
    Então vejo a mensagem "* Nao existe registros para esta data *"
    E o cursor volta ao campo do dia
    E nada é registrado

  Cenário: Processo não cadastrado
    Dado que pedi a listagem de um processo
    E não há processo pendente com o número que informei
    Quando confirmo a tela
    Então vejo a mensagem "* Processo nao cadastrado *"
    E o cursor volta ao campo do número do processo
    E nada é registrado

  Cenário: Listagem a partir de arquivo sem o nome do arquivo
    Dado que pedi a listagem a partir de arquivo
    E não informei o nome do arquivo
    Quando confirmo a tela
    Então vejo a mensagem "* Informe arquivo *"
    E o cursor volta ao campo do arquivo
    E nada é registrado

  Cenário: Matrícula não cadastrada
    Dado que escolhi o tipo que se resolve pela data inicial
    E informei uma matrícula que não está cadastrada
    Quando confirmo a tela
    Então vejo a mensagem "* Matricula nao cadastrada *"
    E o cursor volta ao campo da matrícula
    E nada é registrado

  Cenário: Servidor sem e-mail cadastrado, no tipo por data inicial
    Dado que escolhi o tipo que se resolve pela data inicial
    E o meu cadastro não tem e-mail
    Quando confirmo a tela
    Então vejo a mensagem "<- Usuario sem e-mail cadastrado *"
    E o cursor volta ao campo do dia
    E nada é registrado

  Cenário: Digitação não numérica
    Dado que digitei, em um dos campos numéricos, algo que não é número
    Quando confirmo a tela
    Então o sistema recusa a digitação antes de conferir qualquer cadastro
    E o cursor volta ao campo recusado
    E nada é registrado

  Cenário: Tela fora do cadastro, ao abrir
    Dado que a tela S099P não está no cadastro de telas
    Quando tento abri-la
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo pedir processamento nenhum

  Cenário: Matrícula sem a tela no código de acesso
    Dado que o meu código de acesso não tem a tela S099P
    Quando tento abri-la
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo pedir processamento nenhum

  Cenário: Tela fora do cadastro, ao confirmar
    Dado que a tela S099P não está no cadastro de telas
    Quando confirmo a tela
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é registrado

  Cenário: Operação não disponível
    Dado que a operação que a tela envia não é reconhecida
    Quando confirmo a tela
    Então vejo a mensagem "* Operacao nao disponivel *"
    E nada é registrado

  Cenário: Sem o liberador da operação
    Dado que a minha matrícula tem a tela S099P, mas não o liberador da operação enviada
    Quando confirmo a tela
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é registrado

  Cenário: A tela não altera nem exclui nada e não deixa auditoria
    Dado que registro um pedido
    Então nenhum registro existente é alterado ou excluído
    E nenhum registro de auditoria é gerado
    E o único registro escrito é o do pedido, na fila
```
