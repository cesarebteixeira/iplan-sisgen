# US — C850T — Atualizar os cardápios oficiais de um período a partir da estimativa

## Estória

Como **servidor de CRE**, quero **aplicar aos cardápios oficiais de um período o cardápio que
a estimativa daquele período já fechou**, para que **a escola receba, no período informado, os
gêneros e as quantidades que a estimativa aprovou — e a secretaria consiga ver que a atualização
foi pedida, por quem e para que período**.

A estimativa é o cardápio que a regional planejou e fechou para um período; o cardápio oficial é
o que vale para a merenda. Enquanto o que a estimativa aprovou não passa para o lado oficial, a
escola continua com o cardápio antigo, e é esta atualização que faz a estimativa virar cardápio
em vigor. Como são muitos itens e mais de um cardápio por período, o trabalho não é feito na
hora: o servidor informa os períodos e os cardápios, confere e o sistema registra o pedido, que é
processado depois, fora do atendimento.

## Contexto

Jornada S000M → C000M → C800M → C840M → C850T.

Ator: servidor de CRE — informa o período do cardápio, o período da estimativa e os códigos de
cardápio, confere as recusas e confirma o pedido de atualização.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**,
não regra de negócio.

O contexto de que a C850T se serve — a matrícula, o código de acesso, o privilégio, o tipo de
órgão, a estação e a data do sistema — é o que a entrada deixou na sessão; a tela não recalcula
nada disso: usa para conferir o acesso, montar o cabeçalho, identificar quem pede e compor a
auditoria. Essas conferências de sessão e de perfil são as mesmas de todas as telas e não estão
repetidas aqui: estão no anexo, na seção das regras que se revelaram da entrada.

Os três passos anteriores — o `C000M`, o `C800M` e o `C840M` — são menus e não gravam nada:
nenhum deles deixa registro ou modo de operação para a C850T. A tela monta os próprios campos a
partir do formulário e é ela mesma que marca a operação como alteração; não há no fonte
comparação com o código da tela que a chamou, de modo que o comportamento dela **não muda**
conforme quem a abriu.

A jornada termina aqui. A C850T não encaminha para outra tela: ela reabre a si mesma para pedir a
confirmação e, depois de confirmada, para mostrar o aviso. O que ela entrega ao sistema não é uma
passagem para outra tela, e sim **o pedido de atualização** e o registro de auditoria — e a tela
**não altera cardápio nenhum**: quem altera é o processamento pedido.

---

## Regras de negócio

### RN-01 — A tela é o pedido de atualização dos cardápios do período

A atualização dos cardápios é feita por um processamento que roda fora do atendimento. Esta tela
é o pedido: nela o servidor informa o período do cardápio, o período da estimativa e os códigos
de cardápio, e o sistema confere tudo antes de registrar. Confirmado, o pedido passa a valer, com
o órgão, os dois períodos, os dois códigos e a identificação de quem pediu. A tela, sozinha, não
altera nenhum cardápio: ela registra o pedido de quem altera, e os cardápios só mudam quando o
processamento rodar.

### RN-02 — A tela só opera em alteração

A tela não abre para consulta nem para exclusão: a única operação aceita é a alteração. Ao ser
aberta, ela própria marca a operação como alteração e os campos do período chegam em branco. Se o
servidor trocar a operação por outra coisa, o sistema recusa com
**\* Opcao nao disponivel. Use ALT \***, com o cursor no campo da opção, antes de ler qualquer
estimativa ou cardápio, e nada é registrado.

[?] A recusa manda usar "ALT", mas o sistema reconhece a alteração por um código interno que o
acervo escreve como "CHG", e nenhum valor literal "ALT" existe nos programas: ou o formulário
traduz o que o servidor digita para esse código, ou quem seguir a mensagem é recusado. O texto da
máscara não está no material lido. Pergunta ao site.

### RN-03 — Antes de conferir, os campos de data e de código passam por edição numérica

Ainda antes de qualquer conferência de período, as três partes da data de início e as três da
data limite dos dois períodos e os dois códigos de cardápio — catorze campos — passam por edição
numérica: campo em branco vira zero e o que não for número faz a transação não seguir, sem que
nada seja registrado. A edição corre antes das conferências de período, de estimativa e de
cardápio.

### RN-04 — O período do cardápio tem de ser um período válido

As três partes da data de início e as três da data limite do período do cardápio são conferidas
uma a uma: cada uma tem de ser uma data que existe no calendário e o ano tem de estar na faixa
que o sistema reconhece — de 1994 a 2099. Se a data de início não fecha, o sistema recusa com
**\* Data de inicio invalida \***, com o cursor no dia da data de início; se é a data limite que
não fecha, recusa com **\* Data limite invalida \***, com o cursor no dia da data limite.
Conferidas as duas, a data de início não pode ser posterior à data limite: se for, o sistema
recusa com **\* Data de inicio maior que data limite \***. Em qualquer dessas recusas nada é
registrado.

As datas do período da **estimativa** não passam por conferência de data nenhuma: elas só servem
para localizar a estimativa de que os cardápios serão tirados.

### RN-05 — A estimativa do período tem de existir e estar fechada

Para o período da estimativa informado tem de existir estimativa cadastrada para o órgão da
sessão. Se não existir nenhuma, o sistema recusa com
**\* Registros de estimativa nao cadastrados \***, com o cursor no dia da data limite da
estimativa. Existindo, a estimativa daquele período tem de estar **fechada**: se ainda não
estiver, o sistema recusa com **\* Cadastro nao fechado para este periodo \***, com o cursor no
mesmo campo, e nada é registrado.

A data de início da estimativa que a tela mostra é a do cadastro da estimativa do período, não a
que o servidor digita: encontrado o registro, a tela substitui o que está em tela pelo que está
cadastrado.

[?] As leituras usam o recurso de posicionamento do dicionário de dados, cujo efeito exato não
está no acervo nem no manual: se ele exige a chave exata, a tela só acha a estimativa de quem
sabe o período inteiro e o código; se posiciona no primeiro registro igual ou posterior, o que foi
informado é apenas o ponto de partida da lista. O site precisa dizer qual é o esperado.

[?] A data de início da estimativa digitada pelo servidor é descartada e trocada pela do
cadastro. Se era para o servidor escolher outra data de início, ou se o campo era para ser apenas
de exibição, o acervo não diz. Pergunta ao site.

### RN-06 — O código do cardápio da estimativa escolhe o alcance: todos os cardápios ou um só

O servidor escolhe o alcance pelo código do cardápio da estimativa. Informando **99999** — que no
acervo significa "todos" —, a atualização alcança todos os cardápios da estimativa daquele
período, e o código do cardápio oficial em tela é substituído por esse mesmo 99999, sem que o
servidor precise informá-lo. Informando qualquer outro código, a tela entra no caminho do
cardápio específico, tratado nas duas regras seguintes.

### RN-07 — No caminho de todos os cardápios, o período do cardápio tem de estar livre

Com o código **99999** no cardápio da estimativa, a tela procura cardápios oficiais já
cadastrados para o órgão da sessão — um com o início do período informado e outro com a data
limite informada. Se algum deles existir e o período dele cruzar o período informado — isto é, se
a data limite informada não for anterior ao início do cardápio existente e a data de início
informada não for posterior à limite dele —, o sistema recusa com
**<- Cardapios ja cadastrados neste intervalo \***, mostrando junto a data limite do cardápio que
já existe, com o cursor no dia da data de início do cardápio, e nada é registrado. É essa guarda
que impede pedir de novo a atualização de um intervalo que já tem cardápios.

### RN-08 — No cardápio específico, os dois códigos são obrigatórios e o oficial tem de ser novo no período

Quando o código do cardápio da estimativa não é o 99999, os dois códigos passam a ser exigidos. Se
o código do cardápio da estimativa estiver em branco, o sistema recusa com
**\* Informe codigo do cardapio da estimativa \***; se o código do cardápio oficial estiver em
branco, recusa com **\* Informe codigo do cardapio oficial \***. O código do cardápio oficial
informado tem de ser um código de cardápio, e não o "todos": informando **99999** nesse campo, a
tela recusa com **\* Codigo do cardapio oficial invalido \***.

Com os dois códigos informados, a tela procura, entre as estimativas do período, a que tem o
código do cardápio da estimativa informado. Se não achar, recusa com
**\* Cardapio nao cadastrado nesta estimativa  \***, com o cursor no código do cardápio da
estimativa. Achando, a estimativa daquele cardápio também tem de estar fechada: se não estiver,
recusa com **\* Cadastro nao fechado para este periodo \***. Em seguida procura, entre os
cardápios oficiais do período do cardápio, algum com o código oficial informado. Se o período não
tiver nenhum cardápio oficial, recusa com
**\* Nao existem card. oficiais para este periodo \***, com o cursor no dia da data de início; se
o código oficial informado já estiver cadastrado no período, recusa com
**\* Cardapio ja cadastrado para este periodo \***, com o cursor no código do cardápio oficial.
Nenhuma dessas recusas registra nada.

[?] Na procura pelos cardápios oficiais do período, a tela percorre os registros encontrados e, a
cada um, troca a data de início do período informado pela data de início daquele cardápio
oficial. Se isso é para alinhar o pedido ao período do cardápio oficial, ou se é efeito do
gerador, o acervo não diz. Pergunta ao site.

[?] A procura pelos registros do período — tanto na estimativa quanto nos cardápios oficiais —
usa o mesmo recurso de posicionamento da RN-05, e o acervo não mostra se o laço percorre todos os
registros do período ou se para no primeiro. Se parar no primeiro, as recusas "cardápio não
cadastrado" e "não existem cardápios oficiais" podem aparecer para um período que tem registros
mais adiante. Pergunta ao site.

### RN-09 — A atualização só é registrada depois da confirmação, e a confirmação cai se algum dado mudar

Passada a conferência sem recusa, o sistema ainda não registra nada: ele guarda o que foi
informado — as três partes das duas datas do período do cardápio, as três partes da data limite
da estimativa e os dois códigos, onze valores —, volta à tela com o pedido
**\* Confirma atualizacao dos cardapios <S/N> ? \*** e o cursor na resposta. Só a resposta **S**
segue; qualquer outra resposta limpa a pergunta, devolve a tela à conferência e ela pergunta de
novo, sem registrar nada. E, se algum dos onze valores guardados mudar depois de a confirmação ser
pedida, a resposta é descartada e a conferência recomeça, também sem registrar nada.

### RN-10 — Um pedido por vez para o mesmo processamento

Confirmada a atualização, o sistema verifica se já existe um pedido do mesmo processamento ainda
sem andamento. Se existir, recusa com **\* Relatorio em processamento. Aguarde. \***, com o
cursor na resposta, e nada é registrado: é esse o que impede dois pedidos iguais de ficarem na
fila.

### RN-11 — Confirmado, ficam registrados o pedido e a auditoria, e a tela avisa que o cadastro está sendo atualizado

Com a resposta **S** e nenhum pedido em andamento, o sistema registra o pedido do processamento —
com o órgão, os dois períodos, os dois códigos, o número de requisição seguinte, a matrícula, a
estação e a data da sessão —, registra também a auditoria da tela, com os valores anteriores e os
novos, e lança o processamento na fila. Feito isso, a tela reabre com o aviso
**\* Cadastro sendo atualizado \***. Os cardápios, porém, ainda não mudaram: quem os altera é o
processamento, quando rodar.

## Cenários BDD

```gherkin
Funcionalidade: Atualizar os cardápios oficiais de um período a partir da estimativa

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C850T

  Cenário: A tela abre em alteração e com os campos em branco
    Dado que abri a tela C850T pela opção 10 do menu C840M
    Então a operação já está marcada como alteração
    E as datas e os códigos chegam em branco

  Cenário: Operação diferente de alteração
    Dado que estou na tela C850T
    Quando informo uma operação diferente de alteração
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor fica no campo da opção
    E nenhuma estimativa ou cardápio é lido
    E nada é registrado

  Cenário: Digitação que não é número
    Dado que estou na tela C850T em alteração
    Quando informo letras em um dos códigos de cardápio ou em uma das partes das datas
    Então a transação não segue
    E nada é registrado

  Cenário: Data de início do cardápio inválida
    Dado que estou na tela C850T em alteração
    Quando informo uma data de início que não existe no calendário
    Então vejo "* Data de inicio invalida *"
    E o cursor fica no dia da data de início
    E nada é registrado

  Cenário: Data limite do cardápio inválida
    Dado que estou na tela C850T em alteração
    Quando informo uma data limite que não existe no calendário
    Então vejo "* Data limite invalida *"
    E o cursor fica no dia da data limite
    E nada é registrado

  Cenário: Ano do período do cardápio fora da faixa
    Dado que estou na tela C850T em alteração
    Quando informo um ano anterior a 1994 ou posterior a 2099
    Então vejo a mensagem de data inválida daquele campo
    E nada é registrado

  Cenário: Data de início maior que a data limite
    Dado que estou na tela C850T em alteração
    Quando informo uma data de início posterior à data limite
    Então vejo "* Data de inicio maior que data limite *"
    E o cursor fica no dia da data de início
    E nada é registrado

  Cenário: O período da estimativa não passa por conferência de data
    Dado que estou na tela C850T em alteração
    Quando informo no período da estimativa datas que não formam um período válido
    Então a tela não recusa por isso
    E procura a estimativa daquele período

  Cenário: Sem estimativa cadastrada para o período
    Dado que estou na tela C850T em alteração
    Quando informo um período de estimativa que não tem estimativa cadastrada
    Então vejo "* Registros de estimativa nao cadastrados *"
    E o cursor fica no dia da data limite da estimativa
    E nada é registrado

  Cenário: Estimativa do período ainda não fechada
    Dado que estou na tela C850T em alteração
    E que a estimativa do período informado não está fechada
    Quando envio o pedido
    Então vejo "* Cadastro nao fechado para este periodo *"
    E o cursor fica no dia da data limite da estimativa
    E nada é registrado

  Cenário: A data de início da estimativa vem do cadastro
    Dado que estou na tela C850T em alteração
    E que informei uma data de início da estimativa diferente da do cadastro
    Quando envio o pedido
    Então a data de início da estimativa em tela passa a ser a do cadastro da estimativa

  Cenário: A conferência do período não registra nada
    Dado que estou na tela C850T em alteração
    Quando informo os períodos e os códigos e envio
    Então o sistema confere o que foi informado
    E ainda não registra nada

  Cenário: Atualização de todos os cardápios da estimativa
    Dado que estou na tela C850T em alteração
    E que a estimativa do período está cadastrada e fechada
    E que o período do cardápio não cruza cardápio oficial cadastrado
    Quando informo 99999 no código do cardápio da estimativa e envio
    Então o código do cardápio oficial é preenchido com 99999
    E vejo "* Confirma atualizacao dos cardapios <S/N> ? *"

  Cenário: O período já tem cardápio oficial
    Dado que estou na tela C850T em alteração
    E que informo 99999 no código do cardápio da estimativa
    E que já existe cardápio oficial cadastrado que cruza o período informado
    Quando envio o pedido
    Então vejo "<- Cardapios ja cadastrados neste intervalo *" com a data limite do cardápio existente
    E o cursor fica no dia da data de início do cardápio
    E nada é registrado

  Cenário: Cardápio específico sem o código do cardápio da estimativa
    Dado que estou na tela C850T em alteração
    Quando informo o código do cardápio oficial e deixo o da estimativa em branco
    Então vejo "* Informe codigo do cardapio da estimativa *"
    E nada é registrado

  Cenário: Cardápio específico sem o código do cardápio oficial
    Dado que estou na tela C850T em alteração
    Quando informo um código de cardápio da estimativa e deixo o oficial em branco
    Então vejo "* Informe codigo do cardapio oficial *"
    E o cursor fica no código do cardápio oficial
    E nada é registrado

  Cenário: "Todos" não vale como código do cardápio oficial
    Dado que estou na tela C850T em alteração
    Quando informo um código de cardápio da estimativa e 99999 no código do cardápio oficial
    Então vejo "* Codigo do cardapio oficial invalido *"
    E o cursor fica no código do cardápio oficial
    E nada é registrado

  Cenário: Cardápio da estimativa que não está na estimativa do período
    Dado que estou na tela C850T em alteração
    E que a estimativa do período tem outros cardápios
    Quando informo um código de cardápio da estimativa que não está entre eles
    Então vejo "* Cardapio nao cadastrado nesta estimativa  *"
    E o cursor fica no código do cardápio da estimativa
    E nada é registrado

  Cenário: Período sem nenhum cardápio oficial
    Dado que estou na tela C850T em alteração
    E que o período do cardápio não tem nenhum cardápio oficial cadastrado
    Quando informo um cardápio específico e envio
    Então vejo "* Nao existem card. oficiais para este periodo *"
    E o cursor fica no dia da data de início
    E nada é registrado

  Cenário: Cardápio oficial informado já cadastrado no período
    Dado que estou na tela C850T em alteração
    E que o código do cardápio oficial informado já está cadastrado no período
    Quando envio o pedido
    Então vejo "* Cardapio ja cadastrado para este periodo *"
    E o cursor fica no código do cardápio oficial
    E nada é registrado

  Cenário: A confirmação vem antes de qualquer registro
    Dado que estou na tela C850T em alteração com os períodos e os códigos conferidos
    Quando envio o pedido
    Então vejo "* Confirma atualizacao dos cardapios <S/N> ? *"
    E o cursor fica na resposta
    E nada foi registrado ainda

  Cenário: Algum dado mudou depois da confirmação
    Dado que a tela pediu a confirmação da atualização
    Quando troco uma das datas ou um dos códigos e respondo que sim
    Então a confirmação cai e o sistema confere tudo outra vez
    E nada é registrado

  Cenário: Resposta diferente de S
    Dado que a tela pediu a confirmação da atualização
    Quando respondo N
    Então a tela volta à conferência e pede a confirmação de novo
    E nada é registrado

  Cenário: Já existe um pedido do mesmo processamento aguardando
    Dado que estou na tela C850T em alteração e confirmei a atualização
    E que já existe um pedido do mesmo processamento ainda sem andamento
    Quando envio a resposta S
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor fica na resposta
    E nada é registrado

  Cenário: O que fica registrado quando confirmo
    Dado que estou na tela C850T em alteração com os períodos e os códigos conferidos
    Quando respondo S à confirmação e não há pedido em andamento
    Então fica registrado o pedido do processamento, com o órgão, os períodos, os códigos e quem pediu
    E fica registrada a auditoria da tela, com os valores anteriores e os novos
    E o processamento é lançado na fila
    E a tela reabre com "* Cadastro sendo atualizado *"
    E os cardápios só mudam quando o processamento rodar
```
