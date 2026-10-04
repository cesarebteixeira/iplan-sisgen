# US — E030T — Cópia de pedidos escolares para o novo período

## Estória

Como **servidor de CRE**, quero **pedir a cópia dos pedidos de um fornecedor, de um tipo de
contrato e de uma semana, para um novo período de entrega**, para que **as cópias desses pedidos
sejam impressas já com as datas de entrega do novo período, sem ter de redigitar pedido por
pedido**.

A tela é o pedido da cópia, não a cópia: ela procura os pedidos já cadastrados que casam com o
que foi informado, calcula as datas de entrega do período novo, registra um pedido de impressão
e dispara o processamento da relação que gera e imprime as cópias. Sem ela, a cópia de um
período teria de ser montada fora do sistema, pedido a pedido — e o que já está cadastrado
deixaria de servir de base para o que vem.

## Contexto

Jornada S000M → E000M → E010M → E030T.

Ator: servidor de CRE — informa de quais pedidos quer a cópia (o fornecedor, o tipo de contrato e
a semana), o início do período de entrega, o contrato e a semana para os quais a cópia é emitida
e a impressora; confere e confirma.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

A tela é aberta por uma opção de menu, e não encadeada por outra tela que lhe passe o registro e
a operação: quem chega informa na própria tela o que quer copiar, e ela abre sempre na mesma
operação, a de inclusão. A identificação da tela de origem que chega na transação não é
comparada com nenhum código de tela — ela só alimenta a conferência de rota da sessão. A única
saída que a tela mesma decide é reabrir-se para a pergunta de confirmação; passada a confirmação,
o que ela deixa é a impressora do servidor acertada, um pedido de impressão na fila e o disparo
do processamento da relação de cópia.

Da sessão a tela usa a matrícula, o código de acesso, o privilégio, a estação, o tipo de órgão
(a secretaria), a coordenadoria regional escolar e a data do sistema; o tipo de órgão e a
coordenadoria são o recorte com que ela procura os pedidos.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela só opera na inclusão

Ao ser aberta, a tela repõe no campo da operação a **inclusão**, e só deixa seguir quando a
transação volta com essa operação. Qualquer outra é recusada com
**\* Opcao nao disponivel. Use INC \***, com o cursor de volta ao campo da operação, e nada é
registrado. É coerente com o resto: o que se registra aqui é o pedido de uma cópia nova — a tela
não consulta, não altera e não exclui nada.

[?] A tela nunca põe outra operação nesse campo: o único ponto do programa que o preenche põe a
inclusão, e o que volta da confirmação é a própria inclusão guardada. A recusa existe, mas não
achei caminho em que o servidor a veja. Se é defesa contra transação adulterada ou sobra do
gerador, o site confirma.

### RN-02 — A tela não mantém cadastro: lê oito cadastros e escreve em dois

Para pedir a cópia, a tela consulta **oito cadastros**: o registro das telas, o cadastro das
impressoras por servidor, o cadastro dos pedidos, o cadastro dos gêneros do pedido, o cadastro
dos fornecedores, o cadastro dos feriados, o cadastro dos servidores (para o e-mail de quem
pede) e a fila de requisições de impressão. Escreve em **dois**: acerta a impressora do servidor
(criando o registro quando ele não existe) e inclui **um** registro na fila de impressões.
Nenhum pedido, gênero, fornecedor ou feriado é incluído, alterado ou excluído por esta tela — e
abrir a tela não escreve nada: só lê.

Os cadastros são dimensionados para: pedidos **10 milhões**; gêneros do pedido **200 milhões**;
fornecedores **10 mil**; feriados **10 mil**; impressoras por servidor **10 mil**; telas **2
mil**; servidores **20 mil**; fila de requisições de impressão **90 mil**. São capacidades (o
máximo esperado no dimensionamento), não volumes cadastrados.

[?] A tela não deixa rastro próprio: ela não alcança o cadastro de auditoria e nenhum dos oito
caminhos de gravação que ela declara chega a ser executado. Se o pedido do servidor devia ficar
registrado na auditoria, o fonte não o mostra. Pergunta ao site.

### RN-03 — Ao abrir, a tela propõe a coordenadoria, lembra a impressora e mostra o cabeçalho

Ao ser aberta, a tela preenche a **coordenadoria regional escolar** com a do vínculo do servidor
e, quando ele já tem impressora registrada, traz o código dela; quando não tem, o campo da
impressora fica em branco, para o servidor informar. O cabeçalho mostra a descrição do tipo de
órgão da sessão e a data do sistema. O cursor fica no dia do início do período quando o vínculo
tem coordenadoria; quando não tem, fica no campo da coordenadoria, que é o que falta informar.
Abrir a tela só lê: não acerta a impressora e não registra pedido nenhum.

### RN-04 — O servidor só pede cópia para o seu grupo

A coordenadoria informada é comparada com a do vínculo: diferente, a recusa é
**\* Usuario sem acesso a outro grupo \***, com o cursor de volta ao campo, e nada é pedido.
Quando o vínculo não tem coordenadoria, essa conferência não é feita. A coordenadoria
confirmada é a que viaja no pedido de impressão: é ela que identifica o grupo da cópia.

### RN-05 — Sete campos são obrigatórios

Antes de procurar qualquer pedido, a tela exige, um a um, devolvendo o cursor ao campo recusado:

| campo | sem ele, a recusa é |
| --- | --- |
| a impressora | **\* Informe a impressora \*** |
| o fornecedor — com **9999** valendo por todos | **\* Informe o fornecedor ou 9999 para todos \*** |
| o tipo de contrato dos pedidos | **\* Informe o tipo contrato \*** |
| o **dia** do início do período | **\* Informe data inicial do periodo \*** |
| a semana dos pedidos, de A a E | **\* Informe semana com A / B / C / D / E \*** |
| o tipo de contrato para o qual a cópia é emitida | **\* Informe o tipo contrato - PARA \*** |
| a semana para a qual a cópia é emitida, de A a E | **\* Informe semana com A / B / C / D / E \*** |

Em qualquer dessas recusas nada é pedido. A obrigatoriedade do início do período recai **só no
dia**: o mês e o ano não têm conferência própria — em branco, viram zero e é com zero que eles
entram na procura dos pedidos.

### RN-06 — Dezesseis campos passam por edição numérica antes das conferências

Antes de qualquer conferência de negócio, **dezesseis campos numéricos** passam por edição
numérica, e o campo em branco é tratado como zero: a coordenadoria, o fornecedor, o tipo de
contrato dos pedidos, o dia, o mês e o ano do início do período, o dia, o mês e o ano do limite
do período, o dia, o mês e o ano de início da entrega, o dia, o mês e o ano do limite da entrega
e o tipo de contrato de destino. A operação, a impressora, as duas semanas, a identificação da
tela de origem e a resposta da confirmação não passam por essa edição.

[?] O que o servidor vê quando digita algo que não é número não se conclui desta tela: a rotina
que faz a edição não está no acervo lido. E a tela só sabe devolver o cursor a **dez** campos:
os três limites do período e os três limites da entrega não têm posição de cursor definida,
apesar de serem editados. Há ainda uma posição de cursor preparada para um rótulo de campo que
nenhum ponto do programa chega a preencher. Pergunta ao site.

### RN-07 — Quais pedidos entram na cópia

A tela percorre os pedidos **do tipo de órgão da sessão**, **da coordenadoria informada** e
**cujo início do período é exatamente a data informada**; entre eles, só os **do fornecedor
informado** (com 9999, todos) e os **da semana informada**. Um pedido só conta se tiver **pelo
menos um gênero com o tipo de contrato informado**. Não havendo nenhum, a recusa é
**\* Pedidos nao cad. para os dados informados \***, com o cursor de volta ao campo do
fornecedor, e nada é pedido. Achando, a tela mostra a razão social do fornecedor — ou **TODOS**,
quando o fornecedor informado é 9999.

O recorte é sempre sobre o **primeiro** que casa: a data limite do período e o número de
entregas saem do primeiro pedido (e do primeiro gênero dele) que atende às condições; os demais
pedidos e gêneros que também atendem não somam nada.

[?] A tela nunca lê a marca de exclusão dos pedidos, dos gêneros nem dos fornecedores: essa
marca existe na declaração desses registros e nenhuma linha da lógica a consulta, ainda que o
dicionário tenha versões de acesso que saltam os excluídos. Assim, um pedido já marcado como
excluído continua contando para a conferência de "existem pedidos para estes dados" e continua
entrando na cópia, e um fornecedor excluído continua dando a razão social. Se a cópia devia
saltar os excluídos, este caminho não salta. Pergunta ao site.

### RN-08 — A data de início da entrega é conferida

A data de início da entrega tem de ser uma **data válida**, com o **ano entre 1994 e 2099**
(senão **\* Data de inicio da entrega invalida \***), e não pode cair em **sábado**
(**\* Inicio da entrega nao deve ser um sabado \***), em **domingo**
(**\* Inicio da entrega nao deve ser um domingo \***) nem em um **feriado do tipo de órgão da
sessão** (**\* Inicio da entrega nao deve ser um feriado \***). Nas quatro recusas o cursor
volta ao dia da entrega e nada é pedido. O feriado é procurado pela data e pelo tipo de órgão da
sessão no cadastro de feriados.

### RN-09 — A tela mostra o período e calcula as datas de entrega do novo período

Do pedido encontrado a tela traz a **data limite do período** que está gravada nele e **quantas
entregas** o período tem: o número de datas de entrega preenchidas no primeiro gênero que casa
com o contrato informado, de uma a cinco. A partir da **data de início da entrega informada**,
ela calcula as demais datas, avançando **dia a dia** e saltando sábados, domingos e os feriados
do tipo de órgão da sessão: a primeira data de entrega é a informada, e as seguintes são os dias
úteis consecutivos. A última data calculada é o **limite da entrega** que a tela mostra — as
duas triplas de datas, a do período e a da entrega, aparecem na tela —, e as cinco datas vão no
pedido de impressão.

[?] A tela conta quantas entregas o gênero tem, mas **não** usa as datas gravadas nele: calcula
datas novas por dias úteis consecutivos a partir da data informada. Se o período do site entrega
em dias alternados ou em uma data por semana, a cópia sai com datas diferentes das que estão
gravadas no pedido. E a rotina que soma os dias à data não faz parte do acervo lido, de modo que
o efeito exato do avanço não foi conferido no fonte. Pergunta ao site.

[?] Os três campos do limite do período são mandados editar, mas depois o programa os repõe com
o que está gravado no pedido: o que o servidor digitar ali é descartado sem aviso. Se a máscara
deixa esses campos na tela como informação, ou se o servidor devia poder informá-los, o fonte
não decide. Pergunta ao site.

### RN-10 — A impressora do servidor é acertada antes das conferências

A tela acerta a impressora do servidor **antes** de conferir o fornecedor, o contrato e as
datas: se ele já tem impressora registrada e ela é diferente da informada, o registro é
alterado; se não tem, o registro é criado. Isso acontece na passagem de conferência, de modo que
uma cópia recusada depois — ou nem confirmada — já deixou a impressora do servidor trocada. A
recusa, em si, não registra o pedido de cópia.

[?] Acertar a impressora antes de conferir significa que uma transação abandonada por recusa (ou
por uma resposta diferente de "S") muda o cadastro do servidor. Se a intenção era não mexer em
nada quando a cópia não sai, o caminho não a cumpre. Pergunta ao site.

[?] A pergunta de confirmação repõe os campos conferidos, mas **não** a impressora: quem trocá-la
na tela da confirmação e responder "S" faz a cópia sair na impressora nova sem que o registro do
servidor seja atualizado. Se isso é permitido de propósito, o site confirma.

### RN-11 — A cópia é confirmada antes de ser pedida

Passando por todas as conferências, a tela ainda não pede nada: ela reabre a si mesma com a
pergunta **\* Confirma copia de pedidos <S/N> ? \***, o cursor na resposta, e guarda o que foi
conferido. Só a resposta afirmativa leva adiante; qualquer outra descarta a confirmação e a tela
refaz todas as conferências, voltando à mesma pergunta. E se algum dos **doze campos**
conferidos — a operação, o fornecedor, o tipo de contrato e a semana dos pedidos, o dia, o mês e
o ano do início do período, o tipo de contrato e a semana de destino e o dia, o mês e o ano de
início da entrega — chegar diferente do que foi guardado, a confirmação também é descartada e a
conferência recomeça. A passagem da confirmação não grava nada.

### RN-12 — Confirmada, o pedido de impressão é registrado e a relação é disparada

Confirmada a cópia, a tela registra **um pedido de impressão** na fila: ele leva o tipo de órgão
da sessão, a coordenadoria, o código do fornecedor, o tipo de contrato e a semana dos pedidos
copiados, a data de início do período, o tipo de contrato e a semana de destino, as cinco datas
de entrega calculadas, a matrícula do servidor, a impressora, a estação, o dia, o mês e o ano do
sistema, a operação de inclusão e o número seguinte da fila; a solicitação é de **uma cópia**.
Em seguida a tela dispara o processamento da relação de cópia, entregando-lhe os parâmetros da
cópia — o órgão, a coordenadoria, o fornecedor, o contrato e a semana dos pedidos, o início do
período, o contrato e a semana de destino, as cinco datas de entrega e a matrícula de quem pediu
— em uma cadeia de **73 posições**. É a relação que gera e imprime as cópias; ela está fora
desta jornada.

[?] A tela não dá nenhuma mensagem de sucesso: depois da confirmação ela não escreve texto
nenhum para o servidor. E o disparo do processamento só acontece quando a instalação é a
esperada pela relação; não sendo, o pedido fica registrado na fila e o processamento não é
disparado. O que o servidor vê nesse desfecho não se conclui do fonte. Pergunta ao site.

[?] A tela não confere se a mesma cópia já foi pedida: não há nenhuma leitura da fila procurando
um pedido igual, e a única leitura que ela faz da fila é para pegar o número seguinte. Se o
servidor confirmar duas vezes, o processamento é disparado duas vezes — e o que a relação faz com
o segundo pedido está fora desta jornada. Pergunta ao site.

[?] No pedido de impressão, o campo que guarda o número de processo recebe a **coordenadoria**
confirmada, e não um número de processo. Se é esse o uso do campo na relação, ou se ele foi
usado por conveniência, não se conclui desta jornada. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Cópia de pedidos escolares para o novo período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E030T

  Cenário: Pedir a cópia dos pedidos de um fornecedor no novo período
    Dado que existem pedidos da minha secretaria e da minha coordenadoria, iniciados na
      data informada, do fornecedor, do tipo de contrato e da semana informados, com
      pelo menos um gênero do tipo de contrato informado
    E que a data de início da entrega é um dia útil que não é feriado
    Quando informo a impressora, o tipo de contrato e a semana de destino e confirmo a
      cópia
    Então um pedido de impressão é registrado na fila, com as cinco datas de entrega
      calculadas e uma cópia
    E o processamento da relação de cópia é disparado

  Cenário: O fornecedor 9999 copia os pedidos de todos os fornecedores
    Dado que informo 9999 no código do fornecedor
    Quando confirmo a cópia
    Então a tela considera os pedidos de todos os fornecedores da semana e do contrato
      informados
    E a razão social mostrada é TODOS

  Cenário: A tela só opera na inclusão
    Dado que estou na tela E030T
    Quando a transação chega com uma operação que não é a de inclusão
    Então vejo "* Opcao nao disponivel. Use INC *"
    E o cursor fica no campo da operação
    E nada é registrado

  Cenário: A abertura propõe a coordenadoria, lembra a impressora e mostra o cabeçalho
    Dado que o meu vínculo tem coordenadoria e eu já tenho impressora registrada
    Quando abro a tela E030T
    Então o campo da coordenadoria vem preenchido com a do meu vínculo
    E o campo da impressora vem preenchido com a impressora registrada para a minha
      matrícula
    E o cursor fica no dia do início do período
    E vejo a descrição do tipo de órgão da minha sessão e a data do sistema
    E nada é registrado e nenhuma impressora é acertada

  Cenário: A abertura sem coordenadoria no vínculo
    Dado que o meu vínculo não tem coordenadoria regional escolar
    Quando abro a tela E030T
    Então o cursor fica no campo da coordenadoria, que é o que falta informar
    E a impressora registrada, se houver, continua vindo preenchida
    E nada é registrado

  Cenário: O servidor não pede cópia para outro grupo
    Dado que o meu vínculo carrega uma coordenadoria regional escolar
    Quando informo outra coordenadoria e confirmo
    Então vejo "* Usuario sem acesso a outro grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é pedido

  Cenário: A impressora é obrigatória
    Dado que estou na tela E030T
    Quando confirmo com o campo da impressora em branco
    Então vejo "* Informe a impressora *"
    E o cursor fica no campo da impressora
    E nada é pedido

  Cenário: O fornecedor é obrigatório
    Dado que estou na tela E030T
    Quando confirmo com o código do fornecedor zerado
    Então vejo "* Informe o fornecedor ou 9999 para todos *"
    E o cursor fica no campo do fornecedor
    E nada é pedido

  Cenário: O tipo de contrato dos pedidos é obrigatório
    Dado que estou na tela E030T
    Quando confirmo sem o tipo de contrato dos pedidos
    Então vejo "* Informe o tipo contrato *"
    E o cursor fica no campo do tipo de contrato
    E nada é pedido

  Cenário: O dia do início do período é obrigatório
    Dado que estou na tela E030T
    Quando confirmo com o dia do início do período zerado
    Então vejo "* Informe data inicial do periodo *"
    E o cursor fica no dia do início do período
    E nada é pedido

  Cenário: A semana dos pedidos é obrigatória
    Dado que estou na tela E030T
    Quando confirmo com uma semana dos pedidos que não está entre A e E
    Então vejo "* Informe semana com A / B / C / D / E *"
    E o cursor fica no campo da semana
    E nada é pedido

  Cenário: O tipo de contrato de destino é obrigatório
    Dado que estou na tela E030T
    Quando confirmo sem o tipo de contrato para o qual a cópia é emitida
    Então vejo "* Informe o tipo contrato - PARA *"
    E o cursor fica naquele campo
    E nada é pedido

  Cenário: A semana de destino é obrigatória
    Dado que estou na tela E030T
    Quando confirmo com uma semana de destino que não está entre A e E
    Então vejo "* Informe semana com A / B / C / D / E *"
    E o cursor fica no campo da semana de destino
    E nada é pedido

  Cenário: Não há pedidos para os dados informados
    Dado que não existe pedido da minha secretaria e da minha coordenadoria, iniciado na
      data informada, do fornecedor e da semana informados
    Quando confirmo
    Então vejo "* Pedidos nao cad. para os dados informados *"
    E o cursor fica no campo do fornecedor
    E nada é pedido

  Cenário: Pedido sem gênero do contrato informado não conta
    Dado que o único pedido do período e do fornecedor não tem nenhum gênero do tipo de
      contrato informado
    Quando confirmo
    Então vejo "* Pedidos nao cad. para os dados informados *"
    E nada é pedido

  Cenário: Os campos numéricos em branco contam como zero
    Dado que estou na tela E030T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências
    E a digitação que não é número é barrada antes das conferências dos pedidos

  Cenário: A data de início da entrega inválida é recusada
    Dado que estou na tela E030T
    Quando informo uma data de início da entrega que não existe
    Então vejo "* Data de inicio da entrega invalida *"
    E o cursor fica no dia da entrega
    E nada é pedido

  Cenário: O início da entrega não pode ser um sábado
    Dado que estou na tela E030T
    Quando informo um sábado como início da entrega
    Então vejo "* Inicio da entrega nao deve ser um sabado *"
    E o cursor fica no dia da entrega
    E nada é pedido

  Cenário: O início da entrega não pode ser um domingo
    Dado que estou na tela E030T
    Quando informo um domingo como início da entrega
    Então vejo "* Inicio da entrega nao deve ser um domingo *"
    E o cursor fica no dia da entrega
    E nada é pedido

  Cenário: O início da entrega não pode ser feriado
    Dado que a data informada é um feriado do meu tipo de órgão
    Quando confirmo
    Então vejo "* Inicio da entrega nao deve ser um feriado *"
    E o cursor fica no dia da entrega
    E nada é pedido

  Cenário: A tela mostra o período e calcula as datas de entrega
    Dado que o pedido encontrado tem data limite do período e três datas de entrega
      preenchidas no gênero de contrato informado
    Quando confirmo
    Então vejo a data limite do período que está gravada no pedido
    E a primeira data de entrega é a data que informei
    E as datas seguintes são os dias úteis consecutivos, saltando sábados, domingos e os
      feriados do meu tipo de órgão
    E as quatro datas de entrega vão no pedido de impressão
    E vejo o limite da entrega, que é a última data calculada

  Cenário: A cópia é pedida com confirmação
    Dado que os pedidos passaram por todas as conferências
    Quando confirmo
    Então vejo "* Confirma copia de pedidos <S/N> ? *"
    E o cursor fica na resposta
    E nada foi pedido ainda

  Cenário: A resposta negativa não pede a cópia
    Dado que a tela me pediu a confirmação da cópia
    Quando respondo algo diferente de "S"
    Então o pedido de impressão não é registrado
    E a tela confere tudo de novo e volta a pedir a confirmação

  Cenário: A confirmação é descartada se um campo mudou
    Dado que a tela me pediu a confirmação da cópia
    Quando respondo "S" depois de trocar o fornecedor ou a semana
    Então a confirmação é descartada
    E a tela confere tudo de novo e volta a pedir a confirmação

  Cenário: Confirmada a cópia, o pedido é registrado e a relação é disparada
    Dado que confirmei a cópia e não mudei nenhum campo
    Quando a confirmação é aceita
    Então é registrado um pedido de impressão com o tipo de órgão da sessão, a
      coordenadoria, o fornecedor, o contrato e a semana dos pedidos copiados, a data de
      início do período, o contrato e a semana de destino, as cinco datas de entrega, a
      minha matrícula, a impressora, a estação e a data do sistema
    E a solicitação é de uma cópia
    E o processamento da relação de cópia é disparado

  Cenário: A impressora do servidor é acertada mesmo quando a cópia é recusada
    Dado que o meu vínculo tem coordenadoria e eu ainda não tenho impressora registrada
    Quando confirmo com uma impressora e um fornecedor em branco
    Então vejo "* Informe o fornecedor ou 9999 para todos *"
    E a impressora informada já ficou registrada para a minha matrícula
    E nenhum pedido de impressão foi registrado

  Cenário: Abrir a tela não grava nada
    Dado que tenho impressora registrada e o meu vínculo tem coordenadoria
    Quando abro a tela E030T e não confirmo nada
    Então nenhum pedido de impressão é registrado
    E o cadastro da minha impressora fica como estava

  Cenário: A tela não altera pedido, gênero nem fornecedor
    Dado que pedi uma cópia de um período
    Quando o pedido de impressão é registrado
    Então nenhum pedido, gênero ou fornecedor existente foi incluído, alterado ou excluído
    E o que a tela deixou foi a impressora do servidor e o pedido de impressão na fila
```
