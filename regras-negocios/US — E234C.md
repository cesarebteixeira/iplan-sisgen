# US — E234C — Consultar as quantidades recebidas de uma permissão

## Estória

Como **servidor da coordenadoria regional de ensino que acompanha o
recebimento**, quero **consultar o que já foi recebido de um fornecedor dentro de
uma permissão de fornecimento**, para que **eu confira o que já entrou, item por
item e nota por nota, sem depender de quem lançou cada recebimento**.

A permissão é o que autoriza o fornecedor a entregar dentro de um período, e é
identificada pela coordenadoria regional de ensino, pelo tipo de contrato, pelo
grupamento de licitação e pela data limite. O que a tela mostra é o que já foi
recebido contra essa permissão: item a item, pedido a pedido, nota a nota, com a
quantidade recebida e a acumulada. Sem esta consulta, saber o que já entrou
depende de quem lançou os recebimentos lembrar o que lançou — e é essa
conferência que sustenta a cobrança do que falta entregar.

## Contexto

Jornada S000M → E000M → E200M → E230M → E234C.

Ator: servidor da coordenadoria regional de ensino — consulta, sem incluir,
alterar ou excluir nada, o que já foi recebido dentro de uma permissão da sua
coordenadoria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

Os três passos do meio — `E000M`, `E200M` e `E230M` — são menus: não gravam nada,
não passam registro nem operação à tela seguinte e apenas apontam para onde ir.
Por isso esta tela não herda modo de ninguém: ela abre por decisão própria, já em
consulta, e é ela mesma que repõe esse modo a cada abertura. O que ela usa da
sessão — o tipo de órgão, a coordenadoria regional de ensino e o código de acesso
do servidor — foi deixado pela entrada, e as regras disso estão naquele
documento.

Esta é a última tela da jornada: ela não encadeia outra.

## Regras de negócio

### RN-01 — A tela é de consulta, e qualquer outra opção é recusada

Ao abrir, a tela já se apresenta na opção de consulta e repõe essa opção a cada
abertura, de modo que a opção mostrada volta a ser sempre a de consulta. Se o
operador informar outra opção e enviar a tela, o sistema recusa com
**\* Opcao nao disponivel. Use CON \*** e devolve o cursor ao campo da opção.
Essa recusa vem depois das conferências de acesso e antes das conferências de
obrigatoriedade e de qualquer leitura do cadastro: nesse caminho nada é lido e
nenhuma linha é mostrada.

[?] A recusa só é alcançável se a máscara oferecer ao operador um campo de opção
para digitar; as definições de tela não estão neste lote. Como a própria tela
repõe a consulta a cada abertura, a recusa só pode acontecer numa segunda
mensagem do operador. Se a máscara não tem esse campo, a recusa é trecho sem uso.
Pergunta ao site.

### RN-02 — O operador só consulta o grupo da sua própria coordenadoria

Informada uma coordenadoria regional de ensino diferente da que está na sessão do
servidor, a consulta é recusada com **\* Usuario sem acesso a este grupo \*** e o
cursor volta ao campo da coordenadoria. Essa conferência é uma das primeiras: vem
antes das conferências de obrigatoriedade e antes de qualquer leitura.

[?] Quando a sessão não tem coordenadoria — o vínculo do servidor não aponta
nenhuma —, a conferência não se aplica e o servidor consulta o grupo de qualquer
coordenadoria. Se isso é o desenho ou um buraco de autorização, é pergunta ao
site.

### RN-03 — A data limite, o tipo de contrato e o grupamento são obrigatórios

A permissão é procurada pela coordenadoria, pela data limite, pelo tipo de
contrato e pelo grupamento. Faltando a **data limite**, a recusa é
**\* Informe data limite da permissao \***; faltando o **tipo de contrato**, é
**\* Informe tipo de contrato \***; faltando o **grupamento**, é
**\* Informe o grupamento \***. Em cada uma delas o cursor volta ao campo que
falta e nada é lido do cadastro.

[?] Só o **dia** da data limite é exigido: o mês e o ano não passam por
conferência de obrigatoriedade, embora os três componham a identificação da
permissão. Com o mês e o ano em branco a permissão não é encontrada, e o que o
operador vê é o aviso de que não existem quantidades recebidas, não o de campo
faltando. Se a intenção era exigir a data inteira, o caminho não exige. Pergunta
ao site.

### RN-04 — A permissão procurada é a do órgão da sessão

O servidor não escolhe o órgão: a permissão procurada é sempre a do **tipo de
órgão da sessão**. Sobre ele o operador informa a **coordenadoria regional de
ensino**, a **data limite** (dia, mês e ano), o **tipo de contrato** e o
**grupamento**. Essa combinação identifica a permissão no cadastro de quantidades
recebidas. O **início do período** não é informado pelo operador: vem do próprio
registro encontrado, e é o que a tela passa a mostrar.

### RN-05 — A tela mostra o fornecedor da permissão encontrada

Encontrada a permissão, a tela mostra o **código do fornecedor** e a **razão
social** desse fornecedor, ambos vindos do cadastro de fornecedores. O código
mostrado é o da permissão, não um que porventura tenha sido digitado.

[?] Se o fornecedor da permissão não estiver no cadastro de fornecedores, a tela
não avisa: a razão social sai em branco e a consulta segue normalmente. Se o
esperado é um aviso, é pergunta ao site.

### RN-06 — As quantidades recebidas aparecem numa grade de 13 linhas

A lista tem **13 linhas**, e cada linha traz **8 dados** do registro: o código da
subclasse, o código do gênero, a descrição do gênero, o número do pedido, o ano
da entrega, o número da nota fiscal, a quantidade recebida acumulada e a
quantidade recebida. As quantidades saem com **três casas decimais** e vírgula
decimal; quantidade igual a zero sai em branco. A lista para quando não há mais
registro daquela permissão, e as linhas que sobram ficam em branco.

[?] O ponto de partida da lista fica guardado na sessão e só é zerado quando a
grade enche **e** a lista termina. Numa consulta seguinte, com outros dados, a
lista pode começar do meio; e, se o ponto de partida guardado não corresponder à
permissão procurada, a primeira linha pode não achar registro e a tela avisar que
não existem quantidades recebidas **logo depois** de ter encontrado a permissão.
Se isso é a paginação pretendida ou um efeito colateral, é pergunta ao site.

[?] O recurso de posicionamento da leitura — o que diz à base se deve posicionar
pela combinação informada ou seguir para o registro seguinte — não está
explicado no acervo nem no manual, e o programa o usa com dois jogos de
sinalizadores diferentes para a mesma leitura. Se ele posicionar sempre na
combinação informada, a lista mostra o mesmo registro repetido; se seguir, a
lista percorre a permissão. Os dois comportamentos são compatíveis com o que o
fonte mostra. Pergunta ao site.

### RN-07 — O pedido é um código de 10 dígitos: número do pedido e ano da entrega

O cadastro de quantidades recebidas guarda o pedido num único código de **10
dígitos**: os **6 primeiros** são o número do pedido e os **4 últimos**, o ano da
entrega. A tela separa os dois e mostra o número do pedido e o ano em campos
próprios de cada linha.

### RN-08 — A descrição do gênero vem do cadastro de gêneros

A descrição que acompanha o código do gênero é buscada no cadastro de gêneros,
pelo par subclasse + gênero e pela vigência do início do período. O cadastro
guarda quatro linhas de descrição completa, de 78 caracteres cada, e uma
**descrição resumida**, de 15; a tela mostra a resumida, em 11 caracteres.

[?] A busca da descrição usa o início do período do **primeiro** registro da
lista e confere apenas a subclasse e o gênero, não o período. Se os registros da
mesma permissão tiverem períodos diferentes, a descrição de uma linha pode ser a
de outra vigência do mesmo gênero. Pergunta ao site.

[?] Não achando a descrição no cadastro de gêneros, a linha sai sem descrição e
sem aviso. Se o esperado é um aviso, é pergunta ao site.

### RN-09 — Não havendo quantidade recebida, a tela avisa

Não existindo registro para a combinação informada, a tela avisa
**\* Nao existem quantidades recebidas \*** e devolve o cursor ao campo da
coordenadoria; nenhuma linha é preenchida.

### RN-10 — O cabeçalho mostra o órgão e a data que a sessão deixou

Fora da grade, a tela mostra a **descrição do tipo de órgão** da sessão e a
**data do sistema**.

[?] A descrição mostrada vem da sessão, não do cadastro de tipos de órgão: esse
cadastro chega a ser lido, mas a descrição que ele traz não vai para a tela —
serve apenas para não repetir a leitura. A data do sistema também só aparece como
origem de cópia, e nenhum programa desta jornada preenche os dois valores. Se o
ambiente não os fornecer, o cabeçalho sai em branco. Pergunta ao site.

[?] Os dois dados do cabeçalho são apagados pela limpeza que a tela faz antes de
tratar cada mensagem do operador, e nada os repõe nesse caminho: depois da
primeira resposta do operador, o cabeçalho reaparece em branco. Se a intenção era
mantê-los, o caminho não mantém. Pergunta ao site.

### RN-11 — Os campos de resultado não escolhem a consulta

O código do fornecedor, as datas de início do período, o código da subclasse, o
código do gênero, o número do pedido, o ano da entrega e o número da nota fiscal
são dados de **resultado**: quem os define é a permissão encontrada, não o
operador. Digitando qualquer um deles, a consulta continua sendo a da combinação
informada e o valor mostrado volta a ser o da permissão.

[?] Se a máscara deixa digitar esses campos, o valor digitado é ignorado — o
código do fornecedor exibido é o da permissão. Se a intenção era usá-los como
filtro — consultar um fornecedor, um gênero ou um pedido só —, o caminho não
filtra. Como a máscara não está neste lote, não se sabe quais desses campos o
operador pode digitar. Pergunta ao site.

### RN-12 — A digitação passa pela edição numérica antes de qualquer conferência

Os **15 campos numéricos** da tela — a coordenadoria, o tipo de contrato, o
fornecedor, o grupamento, as três partes da data de início, as três da data
limite, a subclasse, o gênero, o pedido, o ano da entrega e a nota fiscal — são
tratados como número: o que estiver em branco vira zero e o que não for número é
recusado antes de qualquer conferência de negócio e antes de qualquer leitura. A
recusa devolve o cursor a apenas **6** deles: a coordenadoria, o tipo de
contrato, o grupamento e as três partes da data limite. Nos outros nove o
tratamento é interrompido sem devolver o cursor ao campo.

[?] O texto da recusa da edição numérica não está nos fontes desta jornada: quem
edita é uma rotina comum, importada, sem fonte no acervo. Pergunta ao site.

[?] Como o cursor só volta a seis dos quinze campos, o operador pode ser recusado
sem saber em qual campo errou. Se a intenção era apontar o campo em todos, o
caminho só aponta em seis. Pergunta ao site.

### RN-13 — A consulta não grava nada

A tela e as rotinas comuns que ela chama só leem os cadastros desta jornada:
quantidades recebidas, fornecedores, gêneros, tipos de órgão e telas. Nenhum
registro é incluído, alterado ou excluído, e nenhum registro de auditoria é
gerado. As operações de gravação, de exclusão e de travamento existem declaradas
para os cinco cadastros que a tela enxerga, mas **não são executadas em nenhum
caminho**: declarar não é executar.

## Cenários BDD

```gherkin
Funcionalidade: Consultar as quantidades recebidas de uma permissão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E234C

  Cenário: Consulta das quantidades recebidas de uma permissão
    Dado que existe uma permissão da minha coordenadoria com data limite, tipo de contrato e grupamento
    Quando informo a coordenadoria, a data limite, o tipo de contrato e o grupamento
    Então vejo o fornecedor da permissão
    E vejo as quantidades recebidas, uma linha por subclasse, gênero, pedido e nota fiscal

  Cenário: A permissão consultada é a do órgão da minha sessão
    Dado que estou na tela E234C
    Quando informo os dados de uma permissão
    Então a permissão procurada é a do tipo de órgão da minha sessão
    E não preciso informar o órgão

  Cenário: A lista mostra no máximo 13 linhas
    Dado que a permissão tem quantidades recebidas
    Quando informo os dados da permissão e envio a consulta
    Então a lista mostra uma linha por registro, até 13 linhas
    E as linhas que sobram ficam em branco

  Cenário: Cada linha separa o número do pedido e o ano da entrega
    Dado que uma das quantidades recebidas é de um pedido entregue num ano
    Quando vejo a linha dessa quantidade
    Então o número do pedido e o ano da entrega aparecem em campos próprios

  Cenário: A descrição do gênero vem do cadastro de gêneros
    Dado que o gênero da linha está cadastrado no cadastro de gêneros
    Quando vejo a linha
    Então ao lado do código do gênero vejo a descrição resumida do cadastro

  Cenário: As quantidades aparecem com vírgula decimal e zero sai em branco
    Dado que uma linha tem quantidade recebida com casas decimais
    Quando vejo a linha
    Então a quantidade aparece com três casas decimais e vírgula
    E uma quantidade igual a zero aparece em branco

  Cenário: Não existem quantidades recebidas para a permissão informada
    Dado que não existe quantidade recebida para a combinação informada
    Quando envio a consulta
    Então vejo a mensagem "* Nao existem quantidades recebidas *"
    E o cursor volta ao campo da coordenadoria
    E nenhuma linha é preenchida

  Cenário: Opção diferente de consulta
    Dado que estou na tela E234C
    Quando informo uma opção diferente da consulta e envio a tela
    Então vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nenhuma quantidade recebida é lida nesse caminho

  Cenário: Coordenadoria diferente da minha
    Dado que a minha sessão tem uma coordenadoria
    Quando informo a coordenadoria de outro grupo
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenadoria

  Cenário: Data limite não informada
    Quando deixo o dia da data limite em branco
    Então vejo a mensagem "* Informe data limite da permissao *"
    E o cursor volta ao campo do dia da data limite

  Cenário: Tipo de contrato não informado
    Quando deixo o tipo de contrato em branco
    Então vejo a mensagem "* Informe tipo de contrato *"
    E o cursor volta ao campo do tipo de contrato

  Cenário: Grupamento não informado
    Quando deixo o grupamento em branco
    Então vejo a mensagem "* Informe o grupamento *"
    E o cursor volta ao campo do grupamento

  Cenário: O cabeçalho mostra o órgão da sessão e a data do sistema
    Dado que entrei no sistema
    Quando abro a tela E234C
    Então vejo a descrição do tipo de órgão da minha sessão
    E vejo a data do sistema

  Cenário: O fornecedor mostrado é o da permissão, não o digitado
    Dado que existe uma permissão para a combinação que vou informar
    Quando informo um código de fornecedor diferente do dela
    Então a consulta continua sendo a da permissão encontrada
    E o código e a razão social mostrados são os dela

  Cenário: Os campos de resultado não comandam a consulta
    Dado que informo também um gênero, um pedido ou uma nota fiscal
    Quando envio a consulta
    Então a lista continua sendo a das quantidades recebidas da permissão
    E o que digitei nesses campos não escolhe o que aparece

  Cenário: Digitação que não é número
    Dado que digito num campo numérico algo que não é número
    Quando envio a tela
    Então o sistema recusa a digitação antes de qualquer conferência de negócio
    E nada é lido do cadastro de quantidades recebidas nesse caminho

  Cenário: A consulta não grava nada
    Dado que abro a tela E234C e consulto uma permissão
    Quando a lista é mostrada
    Então nenhuma quantidade recebida, fornecedor, gênero ou tipo de órgão é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado
```
