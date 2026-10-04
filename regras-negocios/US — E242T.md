# US — E242T — Distribuição das quantidades do gênero entre os órgãos

## Estória

Como **servidor da CRE que responde pelos pedidos da alimentação escolar da sua
coordenadoria**, quero **distribuir, entre os órgãos da minha coordenadoria, as
quantidades de cada gênero do contrato com as suas datas de entrega, e pedir a
geração dos pedidos**, para que **cada órgão receba exatamente o que vai consumir
no período, nos dias certos, e a geração só saia quando todas as quantidades do
cadastro estiverem fechadas**.

Os pedidos não nascem na tela do gênero: ela só diz *quais* gêneros o cadastro
entrega. Quem diz *quanto* cada órgão recebe, e em que dias, é esta tela — e é ela
que pede a geração. Sem ela, o contrato fica com gêneros autorizados e nenhum
pedido; com as quantidades informadas pela metade, a geração é recusada e os
pedidos daquele cadastro não saem.

Ela não é aberta por menu nenhum: chega-se a ela pela manutenção dos gêneros, que
entrega o cadastro do período já escolhido e diz em que modo a tela abre.

## Contexto

Jornada S000M → E000M → E240M → E240C → E241T → E242T.

Ator: servidor de CRE — distribui as quantidades de um gênero do contrato entre os
órgãos da sua coordenadoria e pede a geração dos pedidos.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O que esta tela usa da sessão é a **secretaria (o tipo de órgão)**, a
**coordenadoria regional escolar do servidor** (o grupo), a **matrícula**, o
**código de acesso**, o **privilégio** e a **data do sistema**; a carga disso é
regra da entrada e está no anexo de evidências, em **Regras que se revelaram da
entrada**. O **órgão filho** do servidor, que a entrada também carrega, não limita
esta tela: o alcance aqui são os órgãos da coordenadoria.

Esta tela **não é alcançada por menu**: só a manutenção dos gêneros (`E241T`)
encadeia nela, e é ela que decide o que a tela trata e em que modo (RN-02 e RN-03).
Na volta, esta tela **entrega a manutenção do período** (`E240T`), em consulta,
depois de pedir a geração (RN-15), e **devolve o cadastro à manutenção dos gêneros**
(`E241T`), também em consulta, quando recebe a marca de voltar (RN-16). Chegando de
qualquer outra origem, ela devolve o servidor ao menu `E240M` (RN-02).

## Regras de negócio

### RN-01 — A tela inclui, altera e consulta; qualquer outra operação é recusada

Esta é a tela da distribuição das quantidades do gênero entre os órgãos da
coordenadoria. Ela aceita **incluir**, **alterar** e **consultar**, e recusa
qualquer outra operação com **\* Opcao nao disponivel. Use INC, ALT ou CON \***,
com o cursor de volta ao campo da operação, e **nada é lido nem gravado** nesse
caminho. Os três valores aceitos não são palavras escritas no programa: vêm da
**tabela de mensagens do ambiente**, a mesma que dá o texto da recusa — é por isso
que a mensagem manda usar "INC", "ALT" e "CON" enquanto a tela compara os códigos
internos que essa tabela carrega.

A operação que aparece quando a tela abre não é escolhida por ela: é a que a tela
anterior deixou (RN-03).

[?] A recusa só é alcançável se a máscara oferecer ao operador o campo da operação.
Como a abertura repõe a operação que veio de quem chamou, essa recusa só pode
aparecer numa mensagem seguinte do operador; se a máscara não tem esse campo, a
recusa é trecho sem uso. Pergunta ao site.

### RN-02 — A origem manda: só a manutenção dos gêneros processa; outra origem devolve ao menu

A tela só processa o cadastro quando ele vem da **manutenção dos gêneros**
(`E241T`), que é a única tela que encadeia nela. Chegando de qualquer outra origem,
ela não processa nada e devolve o servidor ao menu `E240M` — e o menu, ao receber
essa volta, avisa **\* Acesso deve ser feito pela tela E240T \***, encaminhando o
servidor para a tela de manutenção do período.

### RN-03 — O modo vem de quem chamou; a consulta não grava nada

A tela não escolhe o modo em que abre: ela recebe da manutenção dos gêneros a
operação, o período, o cadastro e o gênero. Aberta para **incluir** ou **alterar**,
ela grava o que a distribuição produzir; aberta para **consultar**, ela mostra o
cabeçalho, a lista dos órgãos e as quantidades já informadas, **não confere**
fracionamento, tipo de contrato nem datas, e **não grava nada**: nenhum pedido é
incluído, alterado ou apagado e nenhuma linha de auditoria é gerada.

Por isso, uma tela que abre em consulta onde deveria abrir em alteração não falha:
ela simplesmente não deixa gravar.

### RN-04 — O que a manutenção dos gêneros entrega à tela

A tela abre com os dados do período já preenchidos — o **grupo** (a coordenadoria),
o **tipo de contrato**, o **fornecedor** com a sua razão social, o **início** e o
**limite do período** —, com a **identificação do cadastro**, com a **subclasse** e
o **gênero** e a sua descrição, e com as **datas de entrega** calculadas para
aquele gênero no período, até **cinco**. Recebe também a marca que diz se o
registro do período já foi requisitado (RN-05).

O alto da tela mostra ainda a **descrição do tipo de órgão da sessão** (a
secretaria) e a **data do sistema**.

[?] A descrição do tipo de órgão e a data do sistema são copiadas da sessão, e
nenhum programa deste caminho as preenche — a área comum só as apaga na
inicialização. Se o ambiente não as fornecer, o cabeçalho sai em branco. Pergunta
ao site.

### RN-05 — O total já pedido do gênero e a faixa de situação do cadastro

No alto da tela aparece o **total já pedido** daquele gênero no cadastro: a soma
das quantidades pedidas em **todos** os órgãos da coordenadoria, não só o da linha.
É o que diz ao servidor quanto daquele gênero já está comprometido antes de ele
informar mais.

Ao lado, uma **faixa de situação** mostra **"----- CADASTRO GERADO ----"** quando o
registro do período está marcado como já requisitado; nos demais cadastros a faixa
sai só de traços.

[?] Os rótulos da faixa e do total não estão no lote, e o material lido não diz o
que a faixa significa para quem lê a tela: o programa só a escreve. Pergunta ao
site.

### RN-06 — A lista dos órgãos da coordenadoria, em onze linhas

A tela percorre os órgãos da coordenadoria e mostra **uma linha por órgão ativo**,
com o **código** e o **nome** do órgão; de cada linha saem as **quantidades
informadas em cada uma das cinco datas de entrega**. A lista tem **onze linhas**;
quando os órgãos acabam, as linhas que sobram ficam em branco. Não havendo nenhum
órgão ativo, a tela avisa **\* Nao existem registros cadastrados \*** e não lista
nada — o aviso sai uma vez, na primeira linha, e não se repete.

[?] A tela não confere se o órgão de uma linha é um dos órgãos da coordenadoria
nem se ele está ativo: ela grava a quantidade para o código que estiver na linha
(RN-12). Se a máscara não proteger esse campo, um código fora da lista entra no
pedido. A máscara da tela não está no lote. Pergunta ao site.

### RN-07 — Só o gênero recebido é distribuído

A distribuição vale para o **gênero que a manutenção dos gêneros entregou**. Se o
servidor informar **outro gênero que exista naquele cadastro**, a tela não
distribui por ele: o tratamento termina sem conferir quantidade e sem gravar. Se
informar um **gênero que não existe naquele cadastro**, ela recusa com
**\* Genero nao cadastrado nesta requisicao \***, com o cursor de volta ao campo da
subclasse, e não procura nem grava nada.

### RN-08 — Cadastro com os pedidos já gerados só se consulta

Quando o **registro do período** está marcado como já requisitado, a tela recusa
**incluir** ou **alterar** com **\* Pedidos ja gerados. Use CON \***, com o cursor
de volta ao campo da operação, e nada é gravado. A **consulta** continua
funcionando: é o modo que a mensagem indica.

[?] Quem marca o registro do período como já requisitado está **fora do acervo
lido**: nenhum programa do lote escreve essa marca — a tela só a lê e a tela do
gênero a grava em branco quando cria o registro. Se o processo que a marca deixou
de existir, a recusa é trecho sem uso. Pergunta ao site.

### RN-09 — O tipo de contrato decide em que linha a quantidade pode ser informada

O cadastro de tipos de contrato diz se o contrato é de **cooperativa**. Num
contrato de cooperativa, **só a linha do órgão que acumula** a quantidade da
coordenadoria (o SICI da CRE, na linguagem das mensagens) aceita quantidade:
informada quantidade em qualquer outra linha, a tela para com
**<- Use SICI CRE. Contrato Cooperativa \***, com o cursor de volta à quantidade
daquela linha, e nada é gravado. Num contrato que **não** é de cooperativa vale o
contrário: a linha do órgão que acumula é recusada, com
**\* Nao use SICI CRE. Contrato nao Cooperativa \***, no mesmo campo.

A conferência só é feita na linha que tem quantidade informada; linha em branco não
é conferida nem gravada.

[?] A tela procura, entre os órgãos da coordenadoria, o órgão marcado como o que
acumula. Não achando nenhum, **todo contrato de cooperativa fica sem linha que
aceite quantidade** — nenhuma distribuição passa por esse caminho. Se a
coordenadoria pode existir sem esse órgão, a operação é inalcançável. Pergunta ao
site.

[?] Não achando o registro do tipo de contrato, a tela não avisa: ela decide pela
marca que estiver na área do cadastro, que pode ser a de uma leitura anterior.
Pergunta ao site.

### RN-10 — Cada quantidade tem de respeitar o fracionamento do gênero

A quantidade informada em cada data tem de ser **múltiplo exato da quantidade de
fracionamento** cadastrada para o gênero. Não sendo, a tela para com
**\* Qt fracionada invalida para este genero \***, com o cursor de volta à
quantidade daquela data, e nada é gravado.

[?] A conferência divide a quantidade informada pela quantidade de fracionamento.
Se essa quantidade de fracionamento estiver zerada, o material lido não diz o que
a operação faz: o programa desvia pelo erro de tamanho da divisão e segue como se o
resto fosse zero. Pergunta ao site.

### RN-11 — Só se informa quantidade nas datas de entrega calculadas

A tela só aceita quantidade nas datas de entrega que a manutenção dos gêneros
calculou para o gênero. Informada quantidade numa **data que a entrega não tem**,
ela para com **\* Dia inexistente para a requisicao \***, com o cursor de volta à
quantidade daquela data, e nada é gravado. A **primeira** data não passa por essa
conferência: ela é sempre a data de início do período.

### RN-12 — A distribuição cria, altera e apaga o pedido do órgão

Fechadas as conferências, cada linha com quantidade trata o **pedido daquele
órgão** para o gênero do cadastro, com as quantidades por data, o total e as datas
de entrega:

- não existindo pedido para o órgão e havendo quantidade informada, o pedido é
  **criado**;
- existindo pedido e sendo informado **o mesmo total**, nada é gravado;
- existindo pedido e sendo informado **total diferente**, o pedido é **alterado**;
- existindo pedido e sendo o total informado **zero**, o pedido daquele órgão é
  **apagado**.

Linha sem quantidade informada não é tratada. O pedido pertence ao período, ao
cadastro, ao gênero e ao órgão — é essa combinação que o identifica.

[?] O número do pedido nasce em branco e não faz parte da identificação do pedido;
quem numera os pedidos, o material lido não diz. Pergunta ao site.

### RN-13 — A requisição da geração exige a impressora

Marcada a **requisição da geração**, a tela exige a **impressora**: sem ela, para
com **\* Informe a impressora \***, com o cursor de volta ao campo da impressora, e
não segue. Informada, ela guarda a impressora como a **preferida do servidor** —
alterando a que estava guardada, se for outra, e criando o registro se não houver.

### RN-14 — Não se pede a geração com relatório em processamento nem com gênero sem quantidade

Marcada a requisição, a tela faz duas conferências antes de aceitá-la:

- havendo um **pedido de relatório da geração ainda na fila** para a coordenadoria,
  ela para com **\* Relatorio em processamento. Aguarde. \***, com o cursor de volta
  ao campo da requisição;
- percorrendo os **gêneros do cadastro**, se **algum** estiver **sem quantidade
  informada**, ela para com **<- Genero sem quantidades cadastradas \***, apontando
  o gênero que falta, no mesmo campo.

Nos dois casos nada é gravado.

### RN-15 — A requisição cria o pedido da geração, dispara o processo e devolve à manutenção do período

Passando as conferências, a tela **numera e cria o pedido do relatório da geração**
(relatório E24201) para a coordenadoria, com a impressora, a estação, a matrícula, o
ano e a data, e **dispara o processo de geração dos pedidos**, entregando-lhe os
parâmetros do período e do cadastro. Depois disso devolve o servidor à
**manutenção do período** (`E240T`), entregando-lhe o período e a operação de
consulta: a manutenção abre com o período já carregado e com a faixa
**"CADASTRO SENDO ATUALIZADO"** no alto, sem partir para a inclusão de um período
novo.

[?] A marca que dispara a requisição é um campo de tela que **nenhum programa do
acervo lido escreve** — a própria tela o limpa quando monta a tela — e a máscara
não está no lote. Se a máscara não oferecer o campo, a requisição, a recusa do
relatório em processamento e a volta à `E240T` são trecho sem uso. Pergunta ao
site.

### RN-16 — As marcas de saída: voltar à manutenção dos gêneros e avançar para o gênero seguinte

A tela tem duas marcas que decidem o que ela faz quando termina o tratamento do
último órgão da lista:

- a marca de **voltar** devolve o cadastro à **manutenção dos gêneros** (`E241T`),
  que abre em **consulta**, com o gênero em branco;
- a marca de **avançar** passa a tratar o **gênero seguinte** do cadastro — o
  próximo gênero cadastrado depois do atual e, não havendo seguinte, o primeiro do
  cadastro — e a tela se mostra com ele.

[?] Nenhuma das duas marcas é escrita por programa nenhum do acervo lido: a tela
só as limpa quando monta a tela, e a máscara não está no lote. Pergunta ao site.

### RN-17 — A digitação passa pela edição numérica antes de qualquer conferência

**Dezenove campos** da tela são tratados como número: o grupo, o tipo de contrato, o
fornecedor, as três partes do início do período, as três partes do limite, a
identificação do cadastro, o código da subclasse, o código do gênero, o código do
órgão de cada linha, as cinco quantidades da linha e o código do órgão que acumula.
O que estiver em branco vira zero, os zeros à esquerda caem e o que não for número
é recusado **antes** de qualquer conferência de negócio e de qualquer leitura do
cadastro. Na recusa, apenas **oito** desses campos devolvem o cursor: o código da
subclasse, o código do gênero, as cinco quantidades da linha e o código do órgão
que acumula.

[?] O texto da recusa da edição numérica não está nos fontes desta jornada: quem
edita é uma rotina comum, importada, sem corpo no acervo. E como só oito dos
dezenove campos devolvem o cursor, o servidor pode ser recusado sem saber em qual
campo errou. Pergunta ao site.

### RN-18 — Toda gravação de pedido deixa linha na trilha de auditoria

Cada pedido **criado**, **alterado** ou **apagado** deixa uma linha na **trilha de
auditoria**, com a tela, o cadastro afetado, a operação, o órgão, a matrícula, a
estação, a data e a hora, o número do processo e o conteúdo anterior e posterior do
registro. A trilha é gravada **depois** da criação e **antes** da alteração e da
exclusão.

As declarações de gravação, de exclusão e de travamento existem para **onze
cadastros** — é assim que o programa é montado —, mas a tela executa apenas as
gravações desta jornada: os pedidos, o pedido do relatório da geração, a impressora
preferida do servidor e a própria trilha. O pedido do relatório e a impressora são
gravados **sem** linha de auditoria.

[?] Nas exclusões a trilha é gravada **antes** da exclusão; se a exclusão falhar,
fica na trilha uma operação que não chegou a acontecer. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Distribuir as quantidades dos pedidos de um gênero entre os órgãos da coordenadoria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E242T

  Cenário: RN-01 — distribuir as quantidades de um gênero entre os órgãos
    Dado que a manutenção dos gêneros me entrega um gênero do cadastro de um período
    E o registro do período não está marcado como já requisitado
    Quando informo a quantidade de cada órgão nas datas de entrega e confirmo
    Então o pedido de cada órgão com quantidade fica gravado para aquele gênero
    E o total já pedido do gênero passa a somar o que foi informado

  Cenário: RN-01 — operação diferente de incluir, alterar e consultar
    Dado que estou na tela E242T
    Quando informo uma operação diferente de incluir, alterar e consultar
    Então vejo a mensagem "* Opcao nao disponivel. Use INC, ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado nesse caminho

  Cenário: RN-02 — abrir a tela pela manutenção dos gêneros
    Dado que confirmo a geração na manutenção dos gêneros
    Quando a tela E242T recebe o cadastro do período
    Então ela distribui as quantidades daquele gênero entre os órgãos da coordenadoria

  Cenário: RN-02 — registro vindo de outra origem
    Dado que o cadastro do período chega à tela E242T sem vir da manutenção dos gêneros
    Quando a tela recebe o registro
    Então ela não processa o cadastro
    E o servidor volta ao menu E240M
    E o menu avisa "* Acesso deve ser feito pela tela E240T *"

  Cenário: RN-03 — a operação é a que veio de quem chamou
    Dado que a manutenção dos gêneros me entrega o cadastro para consultar
    Quando abro a tela E242T
    Então o campo da operação mostra a consulta
    E nenhum pedido é incluído, alterado ou apagado

  Cenário: RN-03 — a consulta não grava nada
    Dado que abro a tela E242T em consulta
    Quando a lista dos órgãos é mostrada
    Então nenhum pedido é incluído, alterado ou apagado
    E nenhuma linha de auditoria é gerada
    E nenhuma conferência de fracionamento, de tipo de contrato ou de data é feita

  Cenário: RN-04 — os dados do período e do gênero já vêm preenchidos
    Dado que a manutenção dos gêneros me entrega o cadastro de um período
    Quando abro a tela E242T
    Então vejo o grupo, o tipo de contrato, o fornecedor e a razão social do período
    E vejo o início e o limite do período e a identificação do cadastro
    E vejo a subclasse e o gênero com a sua descrição
    E vejo as datas de entrega calculadas para aquele gênero, até cinco

  Cenário: RN-04 — o cabeçalho da sessão
    Dado que entrei no sistema
    Quando abro a tela E242T
    Então vejo a descrição do tipo de órgão da minha sessão
    E vejo a data do sistema

  Cenário: RN-05 — o total já pedido do gênero
    Dado que o gênero tem quantidades pedidas em mais de um órgão
    Quando abro a tela E242T
    Então o total mostrado no alto é a soma das quantidades pedidas em todos os órgãos

  Cenário: RN-05 — a faixa de situação do cadastro
    Dado que o registro do período está marcado como já requisitado
    Quando abro a tela E242T
    Então vejo a faixa "----- CADASTRO GERADO ----" no alto da tela
    E nos demais cadastros a faixa sai só de traços

  Cenário: RN-06 — a lista dos órgãos da coordenadoria
    Dado que a coordenadoria tem órgãos ativos
    Quando abro a tela E242T
    Então vejo uma linha por órgão, com o código e o nome do órgão
    E de cada linha vejo as quantidades já informadas em cada data de entrega
    E a lista mostra no máximo onze órgãos
    E as linhas que sobram ficam em branco

  Cenário: RN-06 — coordenadoria sem órgão ativo
    Dado que a coordenadoria não tem nenhum órgão ativo
    Quando a lista é montada
    Então vejo a mensagem "* Nao existem registros cadastrados *"
    E nenhuma linha é preenchida

  Cenário: RN-07 — gênero diferente do recebido
    Dado que estou na tela E242T com o gênero que a manutenção dos gêneros entregou
    Quando informo outro gênero daquele cadastro e confirmo
    Então nenhuma quantidade é distribuída por esse gênero
    E nada é gravado

  Cenário: RN-07 — gênero que não existe no cadastro
    Dado que informo um gênero que não faz parte do cadastro
    Quando confirmo
    Então vejo a mensagem "* Genero nao cadastrado nesta requisicao *"
    E o cursor volta ao campo da subclasse
    E nada é gravado

  Cenário: RN-08 — incluir ou alterar um cadastro já requisitado
    Dado que o registro do período está marcado como já requisitado
    Quando peço para incluir ou alterar
    Então vejo a mensagem "* Pedidos ja gerados. Use CON *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: RN-08 — consultar um cadastro já requisitado
    Dado que o registro do período está marcado como já requisitado
    Quando consulto o cadastro
    Então a tela mostra o gênero, os órgãos e as quantidades
    E nenhum pedido é gravado

  Cenário: RN-09 — contrato de cooperativa na linha do órgão que acumula
    Dado que o contrato do período é de cooperativa
    Quando informo quantidade na linha do órgão que acumula e confirmo
    Então a quantidade é gravada para aquele órgão

  Cenário: RN-09 — contrato de cooperativa fora da linha do órgão que acumula
    Dado que o contrato do período é de cooperativa
    Quando informo quantidade numa linha que não é a do órgão que acumula
    Então vejo a mensagem "<- Use SICI CRE. Contrato Cooperativa *"
    E o cursor volta à quantidade daquela linha
    E nada é gravado

  Cenário: RN-09 — contrato que não é de cooperativa na linha do órgão que acumula
    Dado que o contrato do período não é de cooperativa
    Quando informo quantidade na linha do órgão que acumula
    Então vejo a mensagem "* Nao use SICI CRE. Contrato nao Cooperativa *"
    E o cursor volta à quantidade daquela linha
    E nada é gravado

  Cenário: RN-10 — quantidade que não respeita o fracionamento do gênero
    Dado que o gênero tem uma quantidade de fracionamento cadastrada
    Quando informo, numa data, uma quantidade que não é múltiplo dela
    Então vejo a mensagem "* Qt fracionada invalida para este genero *"
    E o cursor volta à quantidade daquela data
    E nada é gravado

  Cenário: RN-11 — quantidade numa data que a entrega não tem
    Dado que a entrega daquele gênero só tem a primeira data calculada
    Quando informo quantidade na segunda data
    Então vejo a mensagem "* Dia inexistente para a requisicao *"
    E o cursor volta à quantidade daquela data
    E nada é gravado

  Cenário: RN-12 — criar o pedido de um órgão
    Dado que o órgão ainda não tem pedido para aquele gênero
    Quando informo a quantidade dele nas datas de entrega e confirmo
    Então o pedido daquele órgão é criado para o gênero do cadastro
    E fica com as quantidades por data, o total e as datas de entrega

  Cenário: RN-12 — alterar a quantidade de um órgão
    Dado que o órgão já tem pedido para aquele gênero
    Quando informo um total diferente do que estava gravado e confirmo
    Então o pedido daquele órgão é alterado para o novo total

  Cenário: RN-12 — repetir o mesmo total
    Dado que o órgão já tem pedido para aquele gênero
    Quando confirmo sem mudar o total informado
    Então nada é gravado para aquele órgão

  Cenário: RN-12 — zerar a quantidade de um órgão
    Dado que o órgão já tem pedido para aquele gênero
    Quando deixo o total daquele órgão em zero e confirmo
    Então o pedido daquele órgão é apagado

  Cenário: RN-13 — pedir a geração sem a impressora
    Dado que marco a requisição da geração
    Quando o campo da impressora está em branco
    Então vejo a mensagem "* Informe a impressora *"
    E o cursor volta ao campo da impressora
    E a geração não é pedida

  Cenário: RN-13 — pedir a geração com a impressora informada
    Dado que marco a requisição da geração
    E informo a impressora
    Quando confirmo
    Então a impressora informada passa a ser a preferida do servidor

  Cenário: RN-14 — já há um relatório da geração na fila
    Dado que existe um pedido de relatório da geração ainda na fila para a coordenadoria
    Quando marco a requisição da geração
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da requisição
    E nada é gravado

  Cenário: RN-14 — gênero do cadastro sem quantidade informada
    Dado que um gênero do cadastro não tem quantidade nenhuma informada
    Quando marco a requisição da geração
    Então vejo a mensagem "<- Genero sem quantidades cadastradas *" com o gênero que falta
    E o cursor volta ao campo da requisição
    E nada é gravado

  Cenário: RN-15 — pedir a geração dos pedidos
    Dado que todos os gêneros do cadastro têm quantidade informada
    E não há relatório da geração na fila
    Quando marco a requisição da geração e confirmo
    Então o pedido do relatório da geração é criado para a coordenadoria
    E o processo de geração dos pedidos é disparado
    E o servidor volta à manutenção do período (E240T), com o período carregado
          e a faixa "CADASTRO SENDO ATUALIZADO"

  Cenário: RN-16 — voltar à manutenção dos gêneros
    Dado que estou na tela E242T com um cadastro do período
    Quando a tela recebe a marca de voltar
    Então ela devolve o cadastro à manutenção dos gêneros (E241T)
    E a manutenção dos gêneros abre em consulta, com o gênero em branco

  Cenário: RN-16 — passar para o gênero seguinte do cadastro
    Dado que o cadastro tem mais de um gênero
    Quando a tela recebe a marca de avançar
    Então ela passa a tratar o gênero seguinte do cadastro
    E mostra o novo gênero e a sua descrição

  Cenário: RN-17 — digitação que não é número
    Quando digito num campo numérico algo que não é número
    Então o sistema recusa a digitação antes de qualquer conferência de negócio
    E o cursor volta ao campo recusado quando é a subclasse, o gênero,
          uma das quantidades da linha ou o código do órgão que acumula

  Cenário: RN-18 — a trilha das gravações
    Dado que crio, altero ou apago o pedido de um órgão
    Quando a gravação termina
    Então uma linha de auditoria é gravada com a tela, o órgão, a operação,
          a matrícula, a data e a hora
    E as gravações da tela são as dos pedidos, a do pedido do relatório da geração
          e a da impressora preferida do servidor
```
