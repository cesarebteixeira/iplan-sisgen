# US — F400T — Pedir a geração das relações SME e INSBE

## Estória

Como **servidor de CRE**, quero **pedir a geração das relações SME e INSBE para o
meu órgão**, para que **o processamento dessas relações seja executado sem eu
depender de quem opera o processamento em lote**.

O trabalho não é feito na tela: ele roda em processamento de lote. O que a tela faz
é registrar o pedido e entregá-lo ao serviço que executa o trabalho, avisando que a
geração entrou em processamento. Sem o pedido registrado, o lote não tem o que
executar; e pedir o mesmo trabalho duas vezes só ocuparia a fila — por isso o
pedido repetido é recusado enquanto o primeiro não sai dela.

A tela não altera nem exclui nada do que já está cadastrado: ela só acrescenta
pedidos, e não deixa registro de auditoria.

## Contexto

Jornada S000M → F000M → F400T.
Ator: servidor de CRE — marca a opção da relação que quer pedir e recebe o aviso de
que a geração entrou em processamento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada são menus, e nenhuma delas deixa dado de
negócio para esta tela: o contexto de que ela se serve — a matrícula funcional, o
código de acesso, o privilégio, o tipo de órgão, a CRE e a estação da sessão — é o
que a entrada deixou na sessão. As regras abaixo são só as desta tela.

---

## Regras de negócio

### RN-01 — A tela é de geração e só aceita a operação de alteração

A tela abre com a operação fixada em **alteração**. Confirmada com a operação
diferente de alteração, o sistema recusa com
**\* Opcao nao disponivel. Use ALT \***, devolve o cursor ao campo da operação e
abandona a transação: nenhum pedido é procurado na fila, nada é registrado e nenhum
processamento é disparado.

Antes dessa recusa, a confirmação já passou pela conferência de encaminhamento e
pela autorização da operação; por isso uma operação de retorno ou de menu pode ser
resolvida antes, com outra mensagem (ver RN-08 e RN-09).

[?] A tela exige a autorização de **alteração** no código de acesso do servidor,
mas o que ela faz é **incluir** um pedido novo. Se a intenção era exigir a
autorização de inclusão, este caminho não a exige. E, como a própria abertura da
tela repõe a alteração, esta recusa só é alcançável se a máscara deixar o operador
mudar o campo da operação. Pergunta ao site.

### RN-02 — Duas opções de geração, uma por relação

A tela tem duas opções. A primeira pede a relação **SME**; a segunda, a **INSBE**.
Cada uma tem o seu próprio trabalho de processamento, entregue em separado, e o
servidor pode marcar uma delas ou as duas. Concluída a confirmação, a opção marcada
é limpa na tela.

[?] O que as relações **SME** e **INSBE** nomeiam, em termos de negócio, não está
nos fontes lidos: os dois códigos só aparecem nas telas desta família e nos
programas de lote que se declaram dessas relações, e nenhum deles diz o que a
relação significa. Pergunta ao site.

### RN-03 — O pedido repetido é recusado enquanto o anterior está na fila

Antes de registrar, a tela procura, no cadastro de requisições, um pedido **daquela
relação para o órgão da sessão**. Havendo, o sistema recusa com
**\* Geracao em processamento. Aguarde. \***, devolve o cursor à opção marcada,
reapresenta a tela e abandona a transação: nenhum pedido novo é registrado e nenhum
processamento é disparado.

A procura não filtra a situação do pedido: enquanto o registro estiver na fila, a
mesma relação não pode ser pedida de novo para aquele órgão. Quem tira o pedido da
fila é o próprio processamento, que exclui o registro que consome.

[?] Para a relação INSBE há quem exclua o pedido — o programa de lote dessa relação
procura a requisição pela mesma chave e a apaga ao processá-la. Para a relação SME
não encontrei esse consumidor entre os programas de lote lidos. Se o pedido do SME
não sai da fila, a opção fica recusada por tempo indeterminado, a não ser pela
limpeza de requisições vencidas que a entrada faz. Pergunta ao site.

### RN-04 — O pedido recebe o próximo número e leva quem pediu, quando e para qual órgão

O pedido é numerado pelo sistema: o número é o do último pedido registrado no
cadastro mais um. No registro ficam o ano, o mês e o dia do sistema; a matrícula
funcional de quem pediu; a estação; o órgão da sessão; a relação pedida; a CRE; a
operação marcada como **inclusão**; e, em branco, a situação do pedido, o número do
processo e os demais campos de controle.

[?] A CRE que compõe a chave do pedido é gravada sempre **zerada**, qualquer que
seja a CRE da sessão: a procura e o registro usam o mesmo zero. Se a intenção era
separar os pedidos por CRE, este caminho não separa. Pergunta ao site.

[?] A contagem parte do número que estiver na área do registro depois da leitura; se
o cadastro estiver vazio, esse número não é reposto antes da soma, e não foi
possível determinar com o que ele sai nesse caso. Pergunta ao site.

### RN-05 — Registrado o pedido, o processamento é disparado e a tela avisa

A tela registra a requisição e, em seguida, monta e entrega ao serviço de
processamento o pedido de execução do trabalho daquela relação — cada relação tem o
seu próprio trabalho. A opção marcada é limpa e a tela volta com o aviso
**Geracao em processamento**.

[?] A entrega é condicionada a um estado da transação que a tela nunca preenche —
ela só o limpa — e que nenhum programa desta jornada atribui. Nos desfechos
observados a entrega acontece sempre, inclusive quando o registro é recusado por
número repetido. O que esse estado significa é pergunta ao site.

[?] A rotina que recebe o pedido de execução não tem fonte neste lote; o que ela faz
com o pedido — e se o trabalho roda na hora ou apenas entra na fila — não foi
possível conferir. Pergunta ao site.

### RN-06 — Com as duas opções marcadas, o segundo pedido não é registrado, mas o segundo processamento é disparado

A tela trata as duas opções em ordem. Ao concluir a primeira, ela encerra a
transação marcando-a como falha — é assim que volta com o aviso. O caminho que
criaria e registraria o segundo pedido só age se a transação ainda não estiver
marcada como falha, e ela está: **a segunda requisição não é registrada**. A
entrega do segundo processamento, porém, não consulta essa marca e acontece — e o
servidor vê o mesmo aviso, sem sinal de que o registro faltou.

[?] Ou a máscara não permite marcar as duas opções ao mesmo tempo — e aí este
trecho não é alcançável —, ou marcar as duas deixa o segundo processamento rodando
sem o pedido que o registra. Não foi possível decidir qual dos dois; pergunta ao
site.

### RN-07 — Sem nenhuma opção marcada, a tela não pede nada

Se o servidor confirma sem marcar nenhuma das duas opções, a tela termina: nenhum
pedido é procurado no cadastro de requisições, nenhuma requisição é registrada e
nenhum processamento é disparado.

[?] Ainda nesse caso, a confirmação passa por uma conferência do mês da transação:
ela roda depois do ponto em que um pedido já teria sido gravado — e, quando há
pedido, a tela já saiu antes — e o texto da recusa é carregado em tempo de
execução, fora dos fontes lidos. Pergunta ao site.

### RN-08 — Antes de processar, o sistema confere a tela, o acesso e a operação

Na abertura, a tela é procurada no cadastro de telas e a matrícula funcional é
procurada no seu código de acesso:

- tela não cadastrada — recusa com **\* Tela nao disponivel \***;
- matrícula sem essa tela no código de acesso — recusa com
  **\* Acesso negado para esta matricula \***.

Na confirmação, antes de tratar as opções, o sistema confere o encaminhamento e a
autorização da operação no código de acesso:

- operação não autorizada — recusa com **\* Acesso negado para esta operacao \***;
- tela não cadastrada no encaminhamento — recusa com **\* Tela nao cadastrada \***.

Em qualquer desses casos nada é registrado e nenhum processamento é disparado.

[?] A releitura do cadastro de telas feita na confirmação só marca a tela como não
cadastrada no caminho de registro ausente quando a tela ainda não passou pela
abertura; como a abertura já passou, não foi possível determinar se a recusa
**\* Tela nao cadastrada \*** ainda é alcançável numa confirmação. Pergunta ao
site.

### RN-09 — A tela devolve o controle à tela de origem quando ela vem identificada

Toda confirmação desta tela carrega junto a identificação de uma tela de origem. Se
essa identificação vier preenchida, o sistema devolve o controle àquela tela e
abandona a transação, sem tratar as opções. Vindo em branco — como acontece quando
a tela é aberta pela opção do menu desta jornada —, o processamento segue.

A mesma conferência trata as operações de **retorno** e de **menu**: com a operação
de retorno o sistema devolve o controle à tela anterior cadastrada para esta tela;
com a de menu, à tela de menu cadastrada. Não havendo essa tela cadastrada, a
recusa é **\* Operacao nao disponivel \***.

[?] Se a máscara expõe ao operador o campo da tela de origem, e o que o preenche,
não está nos fontes lidos — o texto da máscara não veio no lote. Pergunta ao site.

### RN-10 — A tela só inclui: não altera, não exclui e não deixa auditoria

A tela lê o cadastro de telas, o código de acesso e o cadastro de requisições;
escreve **só** no cadastro de requisições, e só incluindo. Nenhum registro
existente é alterado ou excluído, e nenhum registro de auditoria é gerado.

### RN-11 — Cada confirmação começa com os campos de resultado limpos

Antes de conferir a digitação, a tela apaga a descrição do tipo de órgão, a data do
sistema e o aviso que a abertura havia mostrado. Quem confirma a tela, portanto,
não continua vendo a data e o tipo de órgão que a abertura apresentou — vê o
resultado da confirmação.

[?] A data do sistema e a descrição do tipo de órgão que a abertura apresenta vêm
de áreas que, nos fontes lidos, só são **limpas**: nenhum programa do lote as
preenche. Se o ambiente não as preencher, o cabeçalho fica em branco. Pergunta ao
site.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedir a geração das relações SME e INSBE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F400T

  Cenário: Pedido da geração da relação SME
    Dado que o cadastro de requisições não tem pedido da relação SME para o meu órgão
    Quando marco a opção da relação SME e confirmo a tela
    Então o sistema registra a requisição com o meu órgão, a minha matrícula e a data do dia
    E entrega ao processamento o trabalho da relação SME
    E vejo o aviso "Geracao em processamento"
    E a opção marcada fica limpa na tela

  Cenário: Pedido da geração da relação INSBE
    Dado que o cadastro de requisições não tem pedido da relação INSBE para o meu órgão
    Quando marco a opção da relação INSBE e confirmo a tela
    Então o sistema registra a requisição da relação INSBE
    E entrega ao processamento o trabalho da relação INSBE
    E vejo o aviso "Geracao em processamento"
    E a opção marcada fica limpa na tela

  Cenário: Pedido repetido da relação SME enquanto o primeiro está na fila
    Dado que já existe um pedido de geração da relação SME para o meu órgão
    Quando marco a opção da relação SME e confirmo a tela
    Então vejo a mensagem "* Geracao em processamento. Aguarde. *"
    E o cursor volta ao campo da opção marcada
    E nenhum pedido novo é registrado

  Cenário: Pedido repetido da relação INSBE enquanto o primeiro está na fila
    Dado que já existe um pedido de geração da relação INSBE para o meu órgão
    Quando marco a opção da relação INSBE e confirmo a tela
    Então vejo a mensagem "* Geracao em processamento. Aguarde. *"
    E o cursor volta ao campo da opção marcada
    E nenhum pedido novo é registrado

  Cenário: Nenhuma opção marcada
    Dado que não marco nenhuma das duas opções
    Quando confirmo a tela
    Então nenhum pedido é registrado
    E nenhum processamento é disparado

  Cenário: As duas opções marcadas
    Dado que nenhuma das duas relações tem pedido na fila para o meu órgão
    Quando marco as duas opções e confirmo a tela
    Então o processamento das duas relações é disparado
    E só a requisição da primeira relação fica registrada
    E o aviso que vejo é o mesmo dos outros pedidos

  Cenário: Operação diferente de alteração
    Dado que estou na tela F400T
    Quando confirmo com a operação diferente de alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo da operação
    E nada é registrado

  Cenário: Tela não cadastrada
    Dado que a tela F400T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo pedir geração nenhuma

  Cenário: Matrícula sem acesso à tela
    Dado que a minha matrícula não tem a tela F400T no seu código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo pedir geração nenhuma

  Cenário: Sem autorização para a operação
    Dado que a minha matrícula tem a tela F400T, mas não a autorização de alteração
    Quando confirmo a tela
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é registrado

  Cenário: A tela devolve o controle à tela de origem
    Dado que a tela recebe a identificação de uma tela de origem
    Quando confirmo a tela
    Então o sistema devolve o controle àquela tela
    E nenhum pedido é registrado

  Cenário: Sem a tela cadastrada para o retorno
    Dado que confirmo com a operação de retorno
    E não há tela anterior cadastrada para esta tela
    Então vejo a mensagem "* Operacao nao disponivel *"
    E nenhum pedido é registrado

  Cenário: A tela não altera, não exclui e não deixa auditoria
    Dado que registro um pedido de geração
    Então nenhum registro existente é alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Cada confirmação limpa os campos de resultado
    Dado que a abertura da tela mostrou a data do sistema e a descrição do tipo de órgão
    Quando confirmo a tela
    Então esses campos não continuam na tela
    E vejo o resultado da confirmação
```
