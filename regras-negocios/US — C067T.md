# US — C067T — Consultar o apostilamento por item das permissões da CRE

## Estória

Como **servidor de CRE**, quero **consultar, item a item, o apostilamento das permissões da minha
coordenação regional escolar**, para que **eu acompanhe como o valor apostilado de cada item e o
total apostilado da permissão evoluíram, sem risco de mexer no que já foi lançado**.

O apostilamento é o registro posterior que atualiza o valor de uma permissão da coordenação
regional escolar, e ele é lançado gênero a gênero pela tela vizinha do mesmo menu. Esta tela é a
leitura desse lançamento: mostra o item apostilado, com a data-base, a data de atualização e o valor
de cada registro, além do total apostilado da permissão inteira. Sem ela, quem confere uma permissão
só vê o total e não consegue dizer qual item puxou a diferença — e quem depende disso é a própria
coordenação, que precisa conferir o que foi apostilado antes de qualquer novo lançamento.

## Contexto

Jornada S000M → C000M → C050M → C066M → C067T.
Ator: servidor de CRE — consulta, item a item, o apostilamento das permissões da sua coordenação
regional escolar, por tipo de contrato, período e grupo de licitação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

Esta é a tela de consulta do grupo que trata do mesmo registro: a `C062T` calcula o apostilamento por
gênero, a `C065T` e a `C066T` lançam o item, esta o consulta e a `C064T` o estorna. Das telas
anteriores da jornada, a `C050M` e a `C066M` não entregam nada de negócio a esta: a `C066M` é menu e
só aponta a tela de destino, sem passar registro nem operação. O que esta tela usa da sessão é o
**tipo de órgão**, a **coordenação regional** e a **descrição do tipo de órgão** que o vínculo da
matrícula deixou na entrada (LOGON); a **data do sistema** vem do relógio da sessão. Esta é a última
tela da jornada: ela **não entrega registro nem operação** a uma tela seguinte, e não há tela depois
dela.

As regras abaixo são só as da **tela desta jornada**. O que esta tela consome da entrada está no
anexo de evidências, na seção das regras que se revelaram da entrada.

---

## Regras de negócio

### RN-01 — Esta tela só consulta: não grava, não altera e não exclui nada

A tela é de consulta. Ela lê a permissão, o item de apostilamento dela e os cadastros que servem para
descrever o que é mostrado, e não executa nenhuma gravação nem exclusão em cadastro nenhum. Para
cada cadastro que ela enxerga o sistema traz prontas uma operação de gravar e uma de apagar; aqui
essas operações estão declaradas e **nenhuma delas é executada**. Nada nesta tela muda o valor
apostilado, o total da permissão ou o cadastro de permissão. Os cadastros que ela lê são o de telas
do sistema, o do tipo de órgão, o do item de apostilamento, o de gêneros, o da permissão da
coordenação regional escolar, o do tipo de licitação e o da liberação desta tela por tipo de
licitação.

### RN-02 — O que identifica a permissão

O que identifica a permissão consultada é a coordenação regional escolar, o tipo de contrato, a data
limite do período — dia, mês e ano — e o grupo de licitação, sempre dentro do tipo de órgão da
sessão. Isso se informa em **seis campos com rótulo** — a coordenação regional, o tipo de contrato, o
dia, o mês e o ano da data limite, e o grupo de licitação —, e os seis passam pela edição numérica
antes de qualquer conferência de cadastro. A data de início do período não se digita: ela vem do
cadastro da permissão e é mostrada na tela.

[?] A fonte mostra que os seis campos da permissão e os três códigos de item da linha passam pela
edição numérica, mas não mostra **qual mensagem** o servidor vê quando digita letra num deles: a
rotina que faz essa edição não está no acervo desta jornada. Pergunta ao site.

### RN-03 — O tipo de órgão é o da secretaria da sessão, e não se digita

O tipo de órgão não se digita nesta tela: é o da secretaria que o vínculo da matrícula escolheu no
LOGON e que ficou na sessão, e ele entra na identificação de tudo o que a tela lê. O cabeçalho
apenas mostra a descrição desse tipo de órgão; o servidor não tem como consultar o acervo de outro
órgão.

### RN-04 — A tela só aceita a consulta

A tela é de consulta e não tem outra operação. Um valor que não seja um código de operação conhecido
é recusado pelo próprio roteamento do sistema, com **\* Operacao nao disponivel \***, e a transação
não segue. Um código de inclusão, alteração ou exclusão é aceito pelo roteamento e recusado por esta
tela, com **\* Operacao nao disponivel. Use CON \***, com o cursor de volta no campo da opção — e
nada é lido.

[?] A recusa manda usar CON, mas as duas conferências — a do roteamento e a da própria tela —
comparam o que foi digitado com o código interno da consulta, que é o mesmo valor que a tela escreve
nesse campo. Ou o terminal traduz o mnemônico antes de enviar, ou as mensagens estão desalinhadas
das conferências. Pergunta ao site; não concluo qual dos dois.

### RN-05 — O acesso é conferido pelo sistema de segurança antes das leituras

Antes de ler qualquer cadastro, a tela pede ao sistema de segurança que confira o acesso: na
montagem da tela são conferidos a matrícula e a tela; na conferência do que foi informado, é
conferida a operação. Sem perfil de acesso à tela, a consulta não é feita e a recusa é
**\* Acesso negado para esta matricula \***; a mesma conferência pode recusar com
**\* Tela nao disponivel \*** quando o cadastro da tela não corresponde, e com
**\* Acesso a pagina 2 negado \*** quando a requisição vem marcada como página 2. Sem permissão para
a operação, a recusa é **\* Acesso negado para esta operacao \*** — e essa recusa só pode aparecer
quando o que foi informado no campo da opção é um código de inclusão, de alteração ou de exclusão,
porque é o que foi digitado que a conferência da operação examina.

[?] A conferência de operação só distingue incluir, alterar e excluir. O código da consulta não é
nenhum dos três e passa sem nenhum teste de permissão: ou a consulta é livre por desenho, ou a
conferência ficou incompleta. Como esta tela não grava, a consequência é pequena — mas a fonte não
diz qual dos dois é. Pergunta ao site.

### RN-06 — A permissão informada tem de estar cadastrada

Informados a coordenação regional, o tipo de contrato, a data limite e o grupo de licitação, o
sistema procura a permissão correspondente. Não existindo, a consulta é recusada com
**\* Permissao nao cadastrada \***, com o cursor de volta no campo da coordenação regional, e nada é
mostrado.

### RN-07 — A tela tem de estar liberada para o tipo de licitação da permissão

A permissão tem um tipo de licitação. O sistema procura, para esse tipo de licitação, a liberação de
uso desta tela. Não estando a tela liberada, a consulta é recusada com
**\* Tela nao disponivel para esta licitacao \***, com o cursor de volta no campo da coordenação
regional, e nada é mostrado. Passando a conferência, o tipo de licitação da permissão e a sua
descrição são mostrados no cabeçalho.

### RN-08 — A permissão tem de ter histórico de apostilamento

Antes de montar a lista, o sistema confere se existe item de apostilamento para a permissão. Não
existindo, a consulta é recusada com **\* Permissao sem historico de apostilamento \***, com o
cursor de volta no campo da coordenação regional.

### RN-09 — Os campos da consulta e das linhas passam pela edição numérica

Nenhum campo desta tela é texto livre. A coordenação regional, o tipo de contrato, as três partes da
data de início, as três partes da data limite, o grupo de licitação e os três códigos de item da
linha — classe, subclasse e gênero — passam pela edição numérica antes de qualquer conferência de
cadastro. O que não for número é recusado no próprio campo, **sem chegar a ser conferido**: a
coordenação regional, o tipo de contrato, as três partes da data limite, o grupo de licitação e os
três códigos de item da linha devolvem o cursor ao próprio campo (os códigos de item, à linha
correspondente). São treze campos no total: os doze com rótulo na tela que passam por essa edição,
mais o tipo de licitação, que a tela mesma preenche do cadastro.

[?] Para as três partes da data de início, a fonte não diz onde o cursor fica quando o campo é
recusado: o retorno do cursor alcança nove dos treze campos, e as três partes da data de início
ficam de fora. Pergunta ao site se é intencional.

### RN-10 — A lista tem doze linhas, e cada linha é um item de apostilamento

São doze linhas por consulta, e cada linha mostra um item de apostilamento: os códigos de classe,
subclasse e gênero do item, a descrição resumida do gênero, a data-base, a data de atualização e o
valor apostilado daquele item. São sete dados por linha. A descrição resumida do gênero é a vigente
na data de início do item e vem do cadastro de gêneros; não achando, a linha fica sem ela. A lista
percorre os itens na ordem do cadastro — grupo de licitação, classe, subclasse, gênero e data de
atualização —, de modo que o mesmo item pode ocupar mais de uma linha, uma por atualização. Quando
os itens acabam, as linhas que sobram ficam em branco e nada é avisado.

[?] A descrição do gênero ignora os registros marcados como excluídos, mas o que essa marca
significa — se é exclusão lógica do cadastro ou outra coisa — não está no corpus desta jornada.
Pergunta ao site.

### RN-11 — O cabeçalho identifica o órgão, a permissão e o tipo de licitação, e mostra o total apostilado

Fora da lista, o cabeçalho traz dez dados: a coordenação regional, o tipo de contrato, o período (a
data de início, que vem do cadastro, e a data limite, que foi informada), o grupo de licitação, o
tipo de licitação da permissão com a sua descrição, a descrição do tipo de órgão da sessão, a data
do sistema e o total apostilado da permissão. O total apostilado é o da permissão inteira, e não a
soma das linhas mostradas. A linha de mensagem fica no rodapé da tela.

### RN-12 — A tela reapresenta a consulta em que a sessão parou

Ao ser usada de novo na mesma sessão, a tela volta à consulta anterior — a mesma coordenação
regional, o mesmo tipo de contrato, o mesmo período e o mesmo grupo de licitação — e recarrega a
lista a partir dela; ao voltar, a operação já vem fixada na consulta. Enquanto não houver nenhuma
consulta guardada na sessão, ela abre sem nada preenchido, fixa a consulta e não lê nada.

### RN-13 — Os códigos de item de cada linha são os do item lido, e a procura avança sozinha

A lista não é digitada: os códigos de classe, subclasse e gênero de cada linha são os do item lido,
e a tela os repõe na linha ao apresentá-la. A leitura começa pelo grupo de licitação, sem classe,
subclasse nem gênero informados, e avança item a item na ordem do cadastro até as doze linhas; depois
de cada linha lida, o sistema guarda os três códigos e a data de atualização dela para continuar de
onde parou. A descrição resumida do gênero é a do gênero da linha, na data de início do item.

### RN-14 — Quando a tela chega com um próximo destino marcado, ela não confere nada e não mostra nada

A tela pode chegar já com um próximo destino marcado por quem a chamou, dentro da mesma transação.
Nesse caso o roteamento do sistema assume e devolve o controle à tela marcada, e esta tela não faz
nenhuma das conferências de cadastro da jornada e não monta lista nenhuma.

[?] O campo do próximo destino não é preenchido em nenhum ponto do acervo desta jornada: a fonte só
mostra que, preenchido, ele desvia o roteamento e pula as conferências. A tela anterior da jornada,
que é menu, não o preenche. Não concluo quem o preenche nem se esse caminho é alcançável pelo
terminal. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar o apostilamento por item das permissões da CRE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C067T

  Cenário: RN-02, RN-03, RN-10 e RN-11 — consultar os itens apostilados de uma permissão
    Dado que existe permissão para a minha coordenação regional escolar, com o tipo de contrato, a data limite e o grupo de licitação que informei
    E ela tem itens de apostilamento
    Quando confirmo a consulta
    Então vejo no cabeçalho a descrição do meu tipo de órgão, a data do sistema, o tipo de licitação com a sua descrição e o total apostilado da permissão
    E vejo a data de início do período, que veio do cadastro
    E vejo até doze linhas, cada uma com a classe, a subclasse, o gênero, a descrição resumida do gênero, a data-base, a data de atualização e o valor apostilado daquele item

  Cenário: RN-01 — esta tela não grava nada
    Dado que estou na tela C067T com uma permissão consultada
    Quando confirmo a consulta quantas vezes quiser
    Então o valor apostilado de cada item e o total apostilado da permissão continuam os mesmos
    E nenhum cadastro é gravado, alterado ou excluído por esta tela

  Cenário: RN-10 — o mesmo item com mais de uma atualização
    Dado que o item consultado tem mais de um registro de apostilamento
    Quando confirmo a consulta
    Então o item aparece em mais de uma linha, uma por atualização
    E a lista segue a ordem do cadastro: grupo de licitação, classe, subclasse, gênero e data de atualização

  Cenário: RN-10 — a lista acaba antes das doze linhas
    Dado que a permissão tem menos itens de apostilamento do que linhas
    Quando confirmo a consulta
    Então as linhas que sobram ficam em branco
    E nenhuma mensagem é mostrada

  Cenário: RN-13 — a linha vem do item lido, não do que eu digitei
    Dado que consultei uma permissão com itens de apostilamento
    Quando a lista é apresentada
    Então os códigos de classe, subclasse e gênero de cada linha são os do item lido
    E a leitura continua item a item na ordem do cadastro, a partir do grupo de licitação, até as doze linhas

  Cenário: RN-04 — a primeira operação com o campo em branco vale consulta
    Dado que é a primeira vez que a tela é usada nesta sessão
    E deixo o campo da opção em branco
    Quando a tela é apresentada
    Então a operação fica fixada na consulta
    E os campos da permissão continuam em branco, à espera do que eu informar

  Cenário: RN-04 — operação desconhecida
    Quando informo no campo da opção um valor que não é código de operação conhecido
    Então vejo "* Operacao nao disponivel *"
    E a transação não segue

  Cenário: RN-04 — operação de inclusão, de alteração ou de exclusão
    Quando informo no campo da opção um código de inclusão, de alteração ou de exclusão
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nada é lido

  Cenário: RN-09 — campo não numérico
    Quando preencho a coordenação regional, o tipo de contrato, uma das datas, o grupo de licitação ou um código de item com letra
    Então a tela recusa o campo antes de qualquer conferência de cadastro
    E o cursor volta ao campo, ou à linha do código de item
    E nada é lido

  Cenário: RN-12 — a tela reapresenta a consulta em que a sessão parou
    Dado que já consultei uma permissão nesta sessão
    Quando abro a tela C067T de novo
    Então os dados da consulta anterior já estão preenchidos
    E a lista é recarregada a partir deles

  Cenário: RN-12 — sem consulta anterior na sessão
    Dado que ainda não consultei nada nesta sessão
    Quando abro a tela C067T
    Então os campos da consulta estão em branco
    E a lista está vazia

  Cenário: RN-06 — permissão não cadastrada
    Dado que não existe permissão para a coordenação regional, o tipo de contrato, a data limite e o grupo de licitação que informei
    Quando confirmo a consulta
    Então vejo "* Permissao nao cadastrada *"
    E o cursor volta ao campo da coordenação regional escolar
    E nada é mostrado

  Cenário: RN-07 — a tela não está liberada para o tipo de licitação
    Dado que a permissão existe, mas esta tela não está liberada para o tipo de licitação dela
    Quando confirmo a consulta
    Então vejo "* Tela nao disponivel para esta licitacao *"
    E o cursor volta ao campo da coordenação regional escolar
    E nada é mostrado

  Cenário: RN-08 — permissão sem histórico de apostilamento
    Dado que a permissão existe, mas não tem nenhum item de apostilamento
    Quando confirmo a consulta
    Então vejo "* Permissao sem historico de apostilamento *"
    E o cursor volta ao campo da coordenação regional escolar

  Cenário: RN-08 — a lista sai vazia
    Dado que a consulta foi aceita e não há nenhum item para mostrar
    Quando a tela é apresentada
    Então vejo "* Permissao sem historico de apostilamento *"
    E as doze linhas ficam em branco

  Cenário: RN-05 — sem perfil de acesso à tela
    Dado que a minha matrícula não tem perfil de acesso a esta tela
    Quando confirmo a consulta
    Então vejo "* Acesso negado para esta matricula *"
    E nada é lido

  Cenário: RN-05 — sem permissão para a operação
    Dado que informo no campo da opção um código de inclusão, de alteração ou de exclusão
    E o meu perfil de acesso não permite aquela operação
    Quando confirmo a consulta
    Então vejo "* Acesso negado para esta operacao *"
    E nada é lido

  Cenário: RN-14 — a tela chega com um próximo destino marcado
    Dado que outra tela chama esta dentro da mesma transação, deixando um próximo destino marcado
    Quando a transação chega a esta tela
    Então nenhuma das conferências de cadastro desta tela é feita
    E nenhuma lista é montada
    E o controle volta para a tela marcada como próximo destino
```
