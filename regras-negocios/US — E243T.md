# US — E243T — Exclusão dos pedidos extras do período

## Estória

Como **servidor da CRE que responde pelos pedidos da alimentação escolar da sua
coordenadoria**, quero **identificar um período de contrato que já teve os pedidos
gerados e pedir a exclusão dos pedidos extras dele**, para que **o que foi gerado a
mais seja desfeito e o período volte a valer apenas pelo que deveria ter sido
pedido**.

Os pedidos do período não nascem na tela: eles saem de um processamento que roda
fora dela, a partir das quantidades que a distribuição entre os órgãos informou.
Quando esse processamento gera pedidos a mais — em órgãos ou em quantidades que não
deveriam existir —, não há como corrigi-los um a um: é preciso desfazer o que foi
gerado. Esta é a porta desse desfazer: ela identifica o período, confirma com quem
opera e deixa o pedido na fila do processamento.

E ela **não apaga nada**. O que ela faz é registrar a requisição da exclusão; quem
apaga é o processo que atende à requisição. Sem esta tela, o período ficaria com os
pedidos errados e sem caminho de volta.

## Contexto

Jornada S000M → E000M → E240M → E243T.

Ator: servidor de CRE — informa o grupo, o tipo de contrato, o fornecedor, o início
do período e a identificação do cadastro, confirma a exclusão dos pedidos extras e
é devolvido à manutenção do período.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. Os dois menus do caminho, `E000M` e
`E240M`, só encaminham: não gravam nada e não deixam nada para esta tela.

O que esta tela usa da sessão é a **secretaria (o tipo de órgão)**, a
**coordenadoria regional escolar do servidor** (o grupo), a **matrícula**, o
**código de acesso**, o **privilégio**, a **estação** e a **data e a hora do
sistema**; a carga disso é regra da entrada e está no anexo de evidências, em
**Regras que se revelaram da entrada**. O **órgão filho** do servidor, que a entrada
também carrega, não é usado aqui.

Esta tela é uma passagem, e tem duas saídas: ela **reabre a si mesma** para pedir a
confirmação da exclusão e, confirmada, **entrega o período à manutenção do período
(`E240T`) em consulta** (RN-11). Ao contrário da sua tela irmã, a distribuição das
quantidades (`E242T`), esta **não recebe de ninguém o modo em que abre**: quem a
alcança é o menu, e ela repõe a exclusão a cada abertura (RN-01 e RN-03).

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela só exclui: qualquer outra operação é recusada

Esta tela trabalha com uma única operação: **excluir**. Ao abrir, ela repõe a
exclusão no campo da operação; e se a mensagem chegar com qualquer outra operação, o
sistema recusa com **\* Opcao nao disponivel. Use EXC \***, devolve o cursor ao
campo da operação e **nada é lido nem gravado**. A recusa vem depois das
conferências de sessão, de tela e de acesso e antes de qualquer leitura do período.

A operação não é escolhida por quem chama: nada aqui compara a tela de origem, e a
única porta de entrada do acervo é o menu. Mesmo que a tela anterior estivesse
tratando outra coisa, esta abre para excluir.

[?] A recusa manda usar "EXC", mas a tela compara o campo com um código que vem da
tabela de mensagens do ambiente, carregada em execução: não se conclui do acervo
como a tecla do terminal chega escrita nesse campo. Se ela chegar como "EXC", a
exclusão seria recusada. Pergunta ao site.

### RN-02 — A tela lê seis cadastros e grava em dois; ela não apaga nenhum

A tela enxerga **seis** cadastros: o **registro das telas**, o cadastro das
**impressoras preferidas**, o **registro do período**, o cadastro dos
**fornecedores**, o cadastro dos **servidores** e a **fila de requisições**. Ela
**grava em dois** — a impressora preferida do servidor e a requisição que pede a
exclusão — e **não apaga registro nenhum**: as declarações de exclusão existem para
os seis, porque é assim que o programa é montado, mas esta tela não aciona nenhuma
delas, nem a do período.

São **dezesseis consultas de leitura**, em **oito pontos** do cadastro: os pontos em
laço consultam duas vezes, uma para posicionar e outra para seguir. As conferências
de acesso leem ainda o cadastro dos servidores e o das autorizações do código de
acesso.

Os cadastros são dimensionados para: registro das telas **2 mil**; impressoras
preferidas **10 mil**; registro do período **100 mil**; fornecedores **10 mil**;
servidores **20 mil**; fila de requisições **90 mil**. São capacidades (o máximo
esperado no dimensionamento), não volumes cadastrados.

### RN-03 — Ao abrir, a tela propõe a exclusão, o grupo do servidor e a impressora já guardada

Ao ser aberta, a tela põe a **exclusão** no campo da operação, propõe no campo do
**grupo** a **coordenadoria do vínculo** do servidor e preenche a **impressora** com
a que ficou guardada para ele. No cabeçalho ela mostra a **descrição do tipo de
órgão** da sessão e a **data do sistema**.

O cursor começa no **tipo de contrato** quando o grupo já vem proposto e no **grupo**
quando o vínculo do servidor não tem coordenadoria. Abrir a tela não escreve nem
apaga nada.

### RN-04 — O grupo é obrigatório e o servidor só age no grupo dele

O **grupo** — a coordenadoria regional escolar — é o primeiro dado exigido. Em
branco, a tela para com **\* Informe o grupo \***, com o cursor de volta ao campo, e
**nada é procurado**.

Informado um grupo **diferente do da sessão**, a recusa é
**\* Usuario sem acesso a outro grupo \***, com o cursor de volta ao campo e **nada
lido**. A conferência é dispensada quando o vínculo do servidor não tem
coordenadoria: nesse caso, qualquer grupo informado passa.

### RN-05 — O período tem de existir e estar com os pedidos gerados

O período é identificado pelo **tipo de órgão da sessão**, pelo **grupo**, pelo
**início do período** (dia, mês e ano), pelo **tipo de contrato**, pelo **código do
fornecedor** e pela **identificação do cadastro**. Não existindo esse período, ou
existindo **sem a marca de que os pedidos já foram gerados**, a tela para com
**\* Pedidos nao gerados \***, com o cursor de volta ao campo da operação, e não
segue.

[?] O que são exatamente os "pedidos extras" e o que a exclusão apaga, o material
lido não diz: o processo que atende à requisição não está neste lote, e a tela só
conhece a marca de que os pedidos foram gerados. Quem grava essa marca também não
está no lote. Pergunta ao site.

### RN-06 — A impressora é obrigatória e passa a ser a preferida do servidor

A **impressora** é exigida. Em branco, a tela para com **\* Informe a impressora \***,
com o cursor de volta ao campo, e nada é gravado.

Informada, a tela **guarda a impressora como a preferida daquele servidor** —
alterando a que estava guardada, se for outra, ou criando o registro se não houver
nenhum. É essa preferência que a abertura da tela propõe na vez seguinte (RN-03).

### RN-07 — Não se pede a exclusão com um pedido do mesmo período já na fila

Havendo **uma requisição do mesmo relatório ainda na fila** para o mesmo **tipo de
órgão e grupo**, a tela para com **\* Relatorio em processamento. Aguarde. \***, com
o cursor de volta ao campo da confirmação, e não segue.

[?] O que tira a requisição da fila não está no material lido: a entrada apaga as
requisições vencidas, e o processo que atende ao pedido não está neste lote. Se ele
não existir, a recusa bloqueia para sempre o pedido daquele grupo. Pergunta ao site.

### RN-08 — O fornecedor é procurado só para nomear a confirmação

O **código do fornecedor** informado é procurado no cadastro de fornecedores, e o
que se aproveita dele é a **razão social**, que aparece na tela. **Não achado, a
tela não recusa**: segue com o nome em branco, e a exclusão pode ser pedida para um
código de fornecedor que não existe no cadastro.

[?] A tela tem uma posição de cursor reservada para o cadastro de fornecedores, mas
nenhuma recusa desta jornada a usa. Se a exclusão deveria ser barrada quando o
fornecedor não está cadastrado, é pergunta ao site.

### RN-09 — A exclusão só sai depois da confirmação, e a confirmação é amarrada ao período identificado

Passadas as conferências, a tela **reabre a si mesma** com a pergunta
**\* Confirma exclusao de pedidos extras <S/N> ? \***, com o cursor no campo da
resposta, e **não grava nada** nessa passagem. Só depois da resposta é que o pedido
sai:

- respondendo **"S"**, e continuando o período identificado com os **mesmos** grupo,
  tipo de contrato, fornecedor, início do período e identificação do cadastro, a
  exclusão é pedida;
- respondendo **qualquer outra coisa**, a tela volta ao começo do tratamento, refaz
  as conferências e pergunta de novo;
- **mudando qualquer um desses dados** entre a pergunta e a resposta, a confirmação
  é descartada e a tela volta ao começo.

### RN-10 — Confirmada, a tela registra a requisição e manda processá-la; quem apaga não é a tela

Confirmada, a tela **numera e cria a requisição** do relatório de exclusão para o
tipo de órgão e o grupo, com a impressora, a estação, a matrícula, o ano, o mês, o
dia e a identificação do cadastro, e deixa nela, junto com os dados do período, a
**marca da operação de exclusão** — é essa marca que distingue este pedido do pedido
de geração que a tela irmã faz com o mesmo relatório. Quando o ambiente é o do
processamento em lote, a tela **dispara o processo**, entregando-lhe os dados do
período.

**Nada é apagado pela tela**: o que a exclusão apaga, o material lido não diz,
porque o processo que a executa não está neste lote.

[?] O número da requisição é o seguinte ao último registro da fila. Duas telas
pedindo ao mesmo tempo podem pedir o mesmo número; o que a base faz com isso o
material lido não diz. Pergunta ao site.

### RN-11 — Depois de registrar, a tela entrega o período à manutenção do período, em consulta

Registrada a requisição, a tela **não fica nela**: entrega o **período** — grupo,
tipo de contrato, fornecedor com a razão social, início, limite e identificação do
cadastro — à **manutenção do período (`E240T`)**, com a operação de **consulta** e
com a sua própria identidade como origem. É por causa dessa entrega que a manutenção
abre com o período já carregado e com a faixa **"CADASTRO SENDO ATUALIZADO"** no
alto, em vez de propor a inclusão de um período novo.

### RN-12 — A recusa não grava nada; a impressora, porém, já ficou guardada

Nas recusas anteriores à conferência da impressora — grupo, acesso ao grupo, período
e a própria impressora — **nada é gravado**. A partir dessa conferência, porém, a
**impressora preferida já foi guardada**, e nem a recusa seguinte — o pedido do
mesmo período já na fila — nem o cancelamento da confirmação a desfazem: a
preferência do servidor fica atualizada mesmo quando a exclusão não chega a ser
pedida.

### RN-13 — A digitação passa pela edição numérica antes de qualquer conferência

**Dez campos** da tela são tratados como número: o grupo, o tipo de contrato, o
fornecedor, as três partes do início do período, as três partes do limite e a
identificação do cadastro. O que estiver em branco vira zero, os zeros à esquerda
caem e o que não for número é recusado **antes** de qualquer conferência de negócio
e de qualquer leitura do cadastro.

Na recusa, **oito** posições de cursor estão declaradas para esses dez campos — as
do grupo, do tipo de contrato, do fornecedor, das três partes do início e da
identificação do cadastro; as três partes do **limite** não têm nenhuma —, e uma
delas é a do cadastro de fornecedores, que nenhuma recusa desta tela aciona.

## Cenários BDD

```gherkin
Funcionalidade: Pedir a exclusão dos pedidos extras de um período de contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E243T

  Cenário: RN-01 — operação diferente de excluir
    Dado que estou na tela E243T
    Quando a mensagem chega com uma operação que não é a de excluir
    Então vejo a mensagem "* Opcao nao disponivel. Use EXC *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado nesse caminho

  Cenário: RN-02 — o que a tela grava e o que ela não apaga
    Dado que confirmo a exclusão dos pedidos extras de um período
    Quando o tratamento termina
    Então a impressora preferida do servidor fica guardada
    E a requisição da exclusão fica criada na fila
    E nenhum registro do período foi apagado pela tela

  Cenário: RN-03 — a abertura da tela
    Dado que o meu vínculo tem coordenadoria
    E a minha impressora preferida está guardada
    Quando abro a tela E243T
    Então a operação mostrada é a exclusão
    E o campo do grupo vem com a coordenadoria do meu vínculo
    E o campo da impressora vem com a minha impressora preferida
    E vejo a descrição do tipo de órgão da minha sessão e a data do sistema

  Cenário: RN-03 — vínculo sem coordenadoria
    Dado que o meu vínculo não tem coordenadoria
    Quando abro a tela E243T
    Então o campo do grupo vem em branco
    E o cursor começa nele

  Cenário: RN-04 — grupo em branco
    Quando deixo o grupo em branco e confirmo
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nada é procurado

  Cenário: RN-04 — grupo de outra coordenadoria
    Dado que o meu vínculo tem coordenadoria
    Quando informo um grupo diferente do meu e confirmo
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo do grupo
    E nada é lido

  Cenário: RN-05 — período sem os pedidos gerados
    Dado que informo um período que não tem a marca de pedidos gerados
    Quando confirmo
    Então vejo a mensagem "* Pedidos nao gerados *"
    E o cursor volta ao campo da operação
    E a exclusão não é pedida

  Cenário: RN-06 — impressora em branco
    Dado que o período existe e tem os pedidos gerados
    Quando deixo a impressora em branco e confirmo
    Então vejo a mensagem "* Informe a impressora *"
    E o cursor volta ao campo da impressora
    E nada é gravado

  Cenário: RN-06 — a impressora passa a ser a preferida do servidor
    Dado que informo uma impressora diferente da que estava guardada
    Quando confirmo o período
    Então a impressora informada fica guardada como a minha preferida

  Cenário: RN-07 — pedido do mesmo período já na fila
    Dado que já existe uma requisição do mesmo relatório para o meu grupo
    Quando confirmo o período
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da confirmação
    E a exclusão não é pedida

  Cenário: RN-08 — fornecedor que não está cadastrado
    Dado que informo um código de fornecedor que não existe no cadastro
    Quando confirmo o período
    Então a tela não recusa
    E a razão social aparece em branco
    E a exclusão pode ser pedida para esse código

  Cenário: RN-09 — confirmação respondida com S
    Dado que a tela me perguntou se confirma a exclusão dos pedidos extras
    Quando respondo S sem mudar nenhum dado do período
    Então a exclusão é pedida

  Cenário: RN-09 — confirmação não respondida com S
    Dado que a tela me perguntou se confirma a exclusão dos pedidos extras
    Quando respondo qualquer coisa que não seja S
    Então a tela volta ao começo do tratamento
    E me pergunta de novo
    E nada é gravado

  Cenário: RN-09 — período trocado entre a pergunta e a resposta
    Dado que a tela me perguntou se confirma a exclusão dos pedidos extras
    Quando mudo o grupo, o tipo de contrato, o fornecedor, o início do período ou
      a identificação do cadastro e respondo S
    Então a confirmação é descartada
    E a tela volta ao começo do tratamento
    E nada é gravado

  Cenário: RN-10 — o pedido da exclusão
    Dado que respondi S à confirmação, sem mudar o período
    Quando a tela termina a passagem
    Então a requisição da exclusão é criada para o meu tipo de órgão e o meu grupo
    E ela fica com a impressora, a estação, a matrícula, a data e a identificação
      do cadastro
    E a marca da operação de exclusão vai junto com os dados do período
    E o processo é disparado
    E nenhum registro do período é apagado pela tela

  Cenário: RN-11 — a volta à manutenção do período
    Dado que a requisição da exclusão foi criada
    Quando a tela encaminha
    Então chego à manutenção do período (E240T) em consulta
    E ela abre com o período carregado e com a faixa "CADASTRO SENDO ATUALIZADO"

  Cenário: RN-12 — a recusa antes da impressora não grava nada
    Dado que a minha confirmação foi recusada antes da conferência da impressora
    Quando a tela termina a passagem
    Então nada foi gravado

  Cenário: RN-12 — a recusa depois da impressora
    Dado que a impressora já foi conferida e guardada
    Quando a tela recusa por já haver um pedido do mesmo período na fila
    Então a impressora preferida continua guardada
    E a exclusão não é pedida

  Cenário: RN-13 — digitação que não é número
    Quando digito num campo numérico algo que não é número
    Então o sistema recusa a digitação antes de qualquer conferência de negócio
    E o cursor volta ao campo recusado quando é o grupo, o tipo de contrato, o
      fornecedor, uma das partes do início ou a identificação do cadastro
```
