# US — C677T — Saldo mínimo da permissão de contrato por gênero

## Estória

Como **servidor da CRE**, quero **definir o saldo mínimo de cada classe, subclasse
e gênero da permissão de contrato da minha coordenadoria regional**, para que **o
piso de cada gênero do contrato fique registrado no período, sem precisar refazer a
permissão**.

A permissão de contrato é o registro que fixa, para uma secretaria e uma
coordenadoria regional, num período e num grupo de licitação, o que cada classe,
subclasse e gênero do contrato carrega: o fornecedor, os valores, o tipo de
licitação, a quantidade inicial e o saldo mínimo. O saldo mínimo é o piso do gênero
no período, e é esta tela que o define: as demais operações apenas devolvem o valor
que recebem, e é esse piso que o processamento dos pedidos lê e compara com a
quantidade pedida. Sem ele registrado, o pedido passa a ser medido por uma
referência que não existe.

## Contexto

Jornada S000M → C000M → C050M → C677T.

Ator: servidor de CRE — informa e ajusta o saldo mínimo de cada classe, subclasse e
gênero da permissão de contrato da sua coordenadoria regional.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O tipo de órgão, a coordenação regional, a matrícula, o código de acesso, o
privilégio, a data do sistema e a descrição do tipo de órgão chegam pela sessão,
deixados pela entrada; esta tela não os recalcula. As duas telas que antecedem o
destino são menus e nenhuma delas passa registro ou operação adiante: a tela abre
por si, em consulta. A jornada termina aqui — esta tela não abre outra.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela reescreve o saldo mínimo da permissão de contrato; ela não inclui nem exclui cadastro

A tela mantém um único dado da permissão de contrato: o saldo mínimo da linha. A
alteração reescreve esse valor no cadastro das permissões de contrato (C061T), que
tem capacidade para **1.000.000** de registros, e cria um registro na auditoria do
sistema (A010T), com capacidade para **60.000.000**. Capacidade é o máximo esperado
— parâmetro de dimensionamento —, não o que está cadastrado. Nenhuma permissão é
criada e nenhuma é apagada por esta tela, ainda que ela traga declaradas as rotinas
de inclusão e de exclusão dos nove cadastros que enxerga: o que ela executa é a
reescrita, e só ela. A conferência que antecede a gravação, por si só, não altera
nada.

[?] O nome de negócio desta tela não vem do material: o título que ela exibe é lido
do cadastro que registra as telas do sistema (S030T), que não faz parte do lote. O
nome usado nesta estória é leitura de negócio, não transcrição. Pergunta ao site.

### RN-02 — A permissão é identificada pela coordenação regional, pelo tipo de contrato, pelo grupo de licitação e pela data limite do período

Para chegar à permissão, o operador informa a coordenação regional, o tipo de
contrato, o grupo de licitação e o dia, o mês e o ano da data limite do período; o
tipo de órgão vem da sessão. Dessa combinação, mais a classe, a subclasse e o
gênero da linha, sai a permissão de contrato. A data de início do período e as
demais datas e valores não são digitados: a tela os traz do cadastro. O fornecedor
mostrado é o da permissão, buscado no cadastro de fornecedores (C030T) pelo seu
código, com o nome; a descrição do tipo de licitação vem do cadastro próprio
(C143T) e o nome do operador, do cadastro de operadores (C331T), quando a permissão
tem um operador. No alto, a tela mostra a descrição do tipo de órgão da sessão, a
data do sistema e o título lido do cadastro das telas. Os cadastros que ela consulta
para compor a tela têm capacidade para **10.000** fornecedores, **1.000** tipos de
licitação, **100** operadores, **2.000** títulos e **200** tipos de órgão.

[?] Duas das datas que a tela mostra e reexibe, além das duas do período, não têm
rótulo nem significado no material: a máscara que traz os nomes que o operador lê
não faz parte do lote, e o dicionário só as declara como datas. Elas não entram em
nenhuma conferência desta tela. Pergunta ao site.

### RN-03 — A grade mostra até nove linhas, uma por classe, subclasse e gênero

A grade tem até nove linhas, e cada linha é uma permissão de contrato do mesmo tipo
de órgão, coordenação regional, período, tipo de contrato e grupo de licitação; o
que as distingue é a classe, a subclasse e o gênero. Cada linha mostra a classe, a
subclasse, o gênero, a descrição resumida do gênero — buscada no cadastro de
gêneros (C051T) pela classe, subclasse, gênero e data de início do período —, a
quantidade inicial que a permissão registra, o saldo mínimo e a coluna de ação. O
cadastro de gêneros tem capacidade para **150.000** registros. As demais datas e
valores da permissão ficam no cabeçalho da tela: o período, os valores homologado e
adjudicado, mais duas datas que a tela apenas reexibe, o tipo de licitação com a
descrição e o operador com o nome.

### RN-04 — Só os modos de alteração e de consulta passam

A tela aceita dois modos de manutenção: **alteração** e **consulta**. Chegando com
qualquer outro modo, ela recusa com * Opcao nao disponivel. Use ALT ou CON *,
devolve o cursor ao campo do modo e não confere nem grava nada. Chegando sem modo
informado, a tela assume a consulta. A conferência que ela faz ao se exibir também
só reconhece esses dois modos: com qualquer outro, ela não chega a ler a permissão.

[?] As palavras que o operador informa no campo do modo não são texto fixo da tela:
elas vêm da tabela de mensagens do idioma, que não faz parte do material, e a
mensagem da recusa nomeia ALT e CON. Se ALT e CON forem as palavras que o sistema
carrega, a guarda e a mensagem combinam; se não forem, a tela recusa justamente o
que a mensagem manda usar. Pergunta ao site.

### RN-05 — A alteração exige que os dados tenham sido consultados antes

No modo de alteração a tela não confere a permissão do zero: ela aproveita a
consulta já feita. Por isso a coordenação regional, o tipo de contrato, o grupo de
licitação e a data limite informados têm de ser exatamente os da última consulta;
mudando qualquer um deles, a recusa é * Consulte antes de atualizar *, com o cursor
de volta no campo do modo, e nada é gravado.

### RN-06 — A tela só trabalha na coordenação regional da sessão

Informada uma coordenação regional diferente daquela em que o servidor entrou, a
recusa é * Usuario sem acesso a este grupo * — a mensagem chama a coordenação
regional de **grupo** —, com o cursor de volta nesse campo, e nada é conferido nem
gravado. Quando a sessão não tem coordenação regional definida, a tela não impõe
essa restrição.

### RN-07 — Sem permissão de contrato cadastrada, a consulta é recusada

Não estando a permissão registrada para o tipo de órgão da sessão, a coordenação
regional, o período, o tipo de contrato e o grupo de licitação informados, a recusa
é * Permissao nao cadastrada *, com o cursor de volta na coordenação regional, e
nada mais é conferido nem gravado. A mesma recusa acontece quando a tela se abre
sem que a permissão exista.

[?] A busca da permissão é montada com todos os componentes da chave, mas deixa a
classe, a subclasse e o gênero em zero, e depois confere só parte deles: as
permissões que têm classe, subclasse ou gênero preenchidos — que são justamente as
que a tela mostra — podem não ser achadas por essa busca. O que o posicionamento da
leitura faz com os componentes zerados não está documentado no material. Pergunta
ao site.

### RN-08 — A tela só está disponível para o tipo de licitação do contrato

Esta tela é liberada por tipo de licitação: o cadastro que diz quais telas valem
para cada tipo de licitação (C149T), com capacidade para **1.000** registros, tem
de ter o par formado pelo tipo de licitação da permissão e esta tela. Não tendo, a
recusa é * Tela nao disponivel para esta licitacao *, com o cursor no tipo de
contrato, e nada é gravado. A conferência só acontece no caminho da consulta; no da
alteração ela é dispensada, porque a alteração já exige a consulta antes (RN-05).

### RN-09 — Só a linha marcada para alteração é atualizada

A alteração só alcança as linhas que o operador marcou, na coluna de ação, como
linhas de alteração. As demais são ignoradas — mesmo que tragam um saldo digitado —
, e o saldo delas é descartado sem aviso. Linha sem classe, subclasse ou gênero
também é ignorada, e a quantidade que ela traga não chega a ser conferida. A coluna
de ação desta tela só admite a marcação de alteração: não há marcação de inclusão
nem de exclusão, porque esta tela não cria nem apaga permissão. A coluna volta em
branco a cada exibição, de modo que a marca é sempre do operador.

[?] A coluna de ação não tem rótulo no material (a máscara não faz parte do lote),
e a tela nunca escreve nela a marca que a guarda exige — a marca aceita é a letra
A. Se o operador a digita, a alteração acontece; se o valor tiver de vir de um
campo oculto da máscara, o material não diz. Sem a marca, o saldo digitado não é
gravado e o operador não recebe aviso algum. Pergunta ao site.

### RN-10 — O saldo mínimo informado tem de ser múltiplo da fração do gênero

A tela lê a fração registrada para o gênero — no cadastro de gêneros, pela
subclasse, pelo gênero e pela data de início do período — e divide por ela o saldo
mínimo informado; sobrando resto, a recusa é * Quant. fracionada invalida para este
genero *, com o cursor de volta no saldo mínimo, e nada é gravado. A conferência só
acontece quando o saldo informado não é zero: saldo zero passa sem ela.

[?] Quando o gênero não tem registro no cadastro de gêneros, ou quando a leitura
não se efetiva, a tela divide o saldo pelo que estiver na área do registro —
inclusive zero, o que é erro de tamanho e deixa o resto com o valor anterior. A
área que guarda esse resto é limpa uma única vez, na primeira passagem pelo
programa, e não a cada transação. Se a linha passa ou é recusada nesse caso, o
material não responde. Pergunta ao site.

### RN-11 — Nada é conferido nem gravado sem a autorização de perfil, de rota e de operação

Antes de conferir e antes de gravar, a tela passa pelas rotinas de segurança do
sistema: a do perfil da sessão, na exibição, e as de rota e de permissão por
operação, no tratamento da entrada, levando o tipo de órgão, a coordenação
regional, a matrícula, o código de acesso e o privilégio da sessão, além do modo e
do prefixo de tela. Não voltando "OK" de qualquer uma delas, a transação é
abandonada: nada é conferido, nada é gravado e nenhum registro de auditoria é
criado. Antes de montar a auditoria, a tela ainda pede a data e a hora da sessão à
rotina própria do sistema e abandona tudo se ela não responder.

[?] As rotinas de segurança e a de rota só aparecem declaradas, sem corpo no
material: a regra efetiva de quem pode alterar o saldo mínimo não pode ser lida
nesta jornada. Pergunta ao site.

[?] Toda a conferência está atrás do prefixo de tela: chegando preenchido, a tela
abandona a transação em silêncio, sem mensagem nenhuma; chegando vazio, ela
confere. Nada nesta tela escreve nesse campo e o material não diz quem o preenche —
se a máscara, se a tela que a chamou —, nem se o abandono silencioso é o pretendido.
Pergunta ao site.

[?] O texto da recusa por falta de autorização também não está no fonte da tela, que
apenas testa o retorno das rotinas; o que o operador vê nesse caso não vem do
material. Pergunta ao site.

### RN-12 — Confirmada, a alteração reescreve o saldo mínimo e deixa o registro na auditoria

Passadas as conferências, a tela trava a permissão, reescreve o saldo mínimo da
linha com o que foi informado e cria o registro na auditoria (A010T). Nada mais da
permissão muda: os valores, as datas, o fornecedor, o operador e as demais
quantidades ficam como estavam. O registro da auditoria leva o objeto auditado (o
cadastro das permissões de contrato), a tela, a operação de alteração do sistema, a
matrícula, a coordenação regional, o tipo de órgão, o terminal, a data, o mês e a
hora da sessão, um número de processo montado com o tipo de órgão, a coordenação
regional, a subclasse e o gênero, e as imagens do registro antes e depois da
alteração. Cada linha marcada gera a sua própria reescrita e o seu próprio registro
de auditoria: até nove no mesmo envio. Antes de gravar a auditoria, a tela desliga a
distribuição automática entre destinos, de modo que a recusa de destino inválido
não acontece por aqui. Se a permissão não for achada na releitura que antecede a
gravação, a linha é abandonada em silêncio, sem mensagem e sem gravação.

[?] As duas imagens do registro — antes e depois — são montadas do mesmo retrato da
permissão, e as duas antes de o saldo novo ser escrito: o registro de auditoria
guarda o mesmo conteúdo nos dois lados e não guarda o saldo mínimo novo. Se é essa a
trilha pretendida para uma alteração, o material não diz. Pergunta ao site.

[?] A palavra que rotula a operação na auditoria vem da tabela de mensagens do
idioma, que não faz parte do material: o que o auditor lê no registro é essa
palavra, não um texto fixo do programa. Pergunta ao site.

### RN-13 — A consulta não grava nada

No modo de consulta a tela não grava: ela lê a permissão e os cadastros que a
compõem, exibe a grade e para. Nenhuma reescrita e nenhum registro de auditoria são
criados. A gravação só pode acontecer no modo de alteração, e ainda assim depois de
todas as conferências do mesmo envio. A tela não pede confirmação ao operador.

## Cenários BDD

```gherkin
Funcionalidade: Saldo mínimo da permissão de contrato por gênero

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenação regional e a data do sistema
    E tenho acesso à tela C677T

  Cenário: RN-01 — a alteração reescreve o saldo mínimo e não inclui nem exclui permissão
    Dado que a permissão de contrato existe para a minha coordenação regional
    Quando marco uma linha, informo o saldo mínimo e confirmo a alteração
    Então o saldo mínimo daquela linha é reescrito no cadastro das permissões de contrato
    E nenhuma permissão é criada ou apagada por esta tela
    E a alteração deixa um registro na auditoria

  Cenário: RN-02 — a permissão é identificada pela coordenação, pelo contrato, pelo grupo e pela data limite
    Dado que estou na tela C677T
    Quando informo a coordenação regional, o tipo de contrato, o grupo de licitação e a data limite do período
    Então a tela me devolve a data de início, o fornecedor e o seu nome, o tipo de licitação com a descrição e o operador com o nome
    E mostra a descrição do tipo de órgão da sessão e a data do sistema
    E o que eu tenha digitado na data de início é descartado

  Cenário: RN-03 — a grade mostra até nove linhas, uma por classe, subclasse e gênero
    Dado que a permissão existe e tem linhas registradas
    Quando consulto
    Então cada linha mostra a classe, a subclasse, o gênero, a descrição do gênero, a quantidade inicial e o saldo mínimo
    E a tela mostra no máximo nove linhas

  Cenário: RN-04 — modo diferente de consulta e de alteração é recusado
    Dado que estou na tela C677T
    Quando a transação chega com um modo de manutenção diferente de ALT e de CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-04 — sem modo informado, a tela consulta
    Dado que estou na tela C677T
    Quando chego sem informar o modo de manutenção
    Então a tela se comporta como consulta
    E nada é gravado

  Cenário: RN-05 — a alteração exige a mesma identificação da consulta
    Dado que consultei uma permissão
    Quando informo o modo de alteração e mudo a coordenação regional, o tipo de contrato, o grupo de licitação ou a data limite
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-06 — coordenação regional diferente da da sessão é recusada
    Dado que estou na tela C677T
    Quando informo uma coordenação regional diferente da da minha sessão
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica nesse campo
    E nada é gravado

  Cenário: RN-07 — permissão não cadastrada
    Dado que estou na tela C677T
    Quando informo uma coordenação regional, um período, um tipo de contrato e um grupo de licitação sem permissão registrada
    Então vejo "* Permissao nao cadastrada *"
    E o cursor fica na coordenação regional
    E nada é gravado

  Cenário: RN-08 — a tela não está liberada para o tipo de licitação do contrato
    Dado que a permissão existe
    E que o tipo de licitação dela não tem esta tela liberada
    Quando consulto
    Então vejo "* Tela nao disponivel para esta licitacao *"
    E o cursor fica no tipo de contrato
    E nada é gravado

  Cenário: RN-09 — o saldo digitado em linha não marcada não é gravado
    Dado que a permissão existe e eu informo o modo de alteração
    Quando digito o saldo mínimo de uma linha sem marcar a coluna de ação
    Então o saldo daquela linha não é gravado
    E nenhuma mensagem me avisa disso

  Cenário: RN-09 — a linha marcada para alteração é gravada
    Dado que a permissão existe e eu informo o modo de alteração
    Quando marco a coluna de ação da linha e informo o saldo mínimo
    Então o saldo daquela linha é reescrito no cadastro da permissão
    E a alteração fica registrada na auditoria

  Cenário: RN-10 — o saldo mínimo não é múltiplo da fração do gênero
    Dado que a permissão existe e a linha tem gênero
    Quando marco a linha e informo um saldo mínimo que não é múltiplo da fração do gênero
    Então vejo "* Quant. fracionada invalida para este genero *"
    E o cursor fica no saldo mínimo
    E nada é gravado

  Cenário: RN-10 — o saldo mínimo zero passa sem a conferência da fração
    Dado que a permissão existe e a linha está marcada para alteração
    Quando informo zero como saldo mínimo
    Então o saldo é gravado sem a conferência da fração do gênero

  Cenário: RN-11 — sem autorização, nada é conferido nem gravado
    Dado que estou na tela C677T
    Quando a checagem de perfil, de rota ou de permissão por operação não retorna OK
    Então a transação é abandonada
    E nada é conferido, nada é gravado e nenhum registro de auditoria é criado

  Cenário: RN-12 — a auditoria da alteração
    Dado que alterei o saldo mínimo de uma linha marcada
    Quando a gravação termina
    Então existe um registro de auditoria do cadastro das permissões de contrato
    E o registro leva a matrícula de quem alterou, a coordenação regional, o tipo de órgão, o terminal e a data e a hora da sessão
    E leva um número de processo com o tipo de órgão, a coordenação regional, a subclasse e o gênero
    E cada linha marcada gera o seu próprio registro de auditoria

  Cenário: RN-12 — permissão desaparecida na releitura que antecede a gravação
    Dado que marquei a linha e informei o saldo mínimo
    Quando a permissão não é encontrada na releitura que antecede a gravação
    Então aquela linha é abandonada sem mensagem
    E nada é gravado para ela

  Cenário: RN-13 — a consulta não grava nada
    Dado que estou na tela C677T no modo de consulta
    Quando consulto uma permissão
    Então nenhuma permissão de contrato é alterada
    E nenhum registro de auditoria é criado
```
