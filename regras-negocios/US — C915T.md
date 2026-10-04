# US — C915T — Consultar refeições de um cardápio

## Estória

Como **servidor de CRE**, quero **consultar quais refeições um cardápio atende dentro do
período de validade dele**, para que **eu confira, antes de seguir para a composição daquele
cardápio, se as refeições do período já estão previstas — e não tome um cardápio sem refeição
por um cardápio pronto**.

O que diz quais refeições um cardápio atende não é o cardápio: é a ligação dele com cada
refeição, dentro da validade. Sem essa lista, o código do cardápio e as datas não dizem o que
será servido, e um cardápio cadastrado e sem refeição nenhuma fica indistinguível de um
cardápio completo. É também por esta lista que o servidor chega à composição do cardápio:
quando a passagem está pedida, esta tela entrega à tela dos gêneros o cardápio que está em tela.

## Contexto

Jornada S000M → C000M → C800M → C900M → C915T.
Ator: servidor de CRE — consulta as refeições previstas para um cardápio na validade dele e,
quando é o caso, segue para a composição daquele cardápio.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O caminho até aqui é todo por menu: o C000M, o C800M e o C900M não gravam nada e só
encaminham. O contexto que esta tela usa — o tipo de órgão, a matrícula, o código de acesso, o
privilégio, a coordenação regional escolar e a data do sistema — é o que a entrada deixou na
sessão; isso é regra da entrada e está no anexo de evidências, em **Regras que se revelaram da
entrada**.

Esta tela é só de consulta (RN-02 e RN-03): não inclui, não altera e não exclui nada. O que
ela tem de próprio é a passagem para a composição do cardápio, a `C910T` (RN-08); e o modo em
que ela mesma abre depende de quem a chamou — vinda daquela tela, ela abre com o cardápio já
carregado e a lista começando na primeira refeição (RN-04).

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela consulta as refeições de um cardápio dentro da validade dele

Para um **código de cardápio** e um **período de validade** — dia, mês e ano de início e dia,
mês e ano limite —, esta tela mostra **quais refeições aquele cardápio atende**, uma a uma, com
a descrição de cada uma, mais o código e a descrição do cardápio e o código e a descrição do
cardápio de sobremesa daquela validade. O tipo de órgão não se digita: é o da sessão, e ele
entra na identificação de tudo o que a tela lê.

A ligação do cardápio com a refeição é guardada **refeição a refeição** — cada refeição
atendida é um registro do cadastro, identificado pelo tipo de órgão, pelo cardápio, pelo
período e pela refeição —, e esse cadastro tem **nove campos** e capacidade para **100.000
registros**. A capacidade é o máximo esperado que o dicionário de dados declara, parâmetro de
dimensionamento, não o volume cadastrado.

A tela enxerga **quatro** cadastros e não grava nenhum: o título das telas (2.000), o cardápio
do período (100.000), as refeições do cardápio (100.000) e o cadastro das refeições (1.200).

### RN-02 — A consulta não grava nada e não deixa rastro

Em **consulta**, a tela apenas mostra: o código e a descrição do cardápio, o início e o limite
da validade, o código e a descrição do cardápio de sobremesa e a lista das refeições com a
descrição de cada uma. Nenhum registro é incluído, alterado, excluído ou travado, e nenhum
registro de auditoria é gerado. As operações de gravação, de exclusão e de travamento existem
**declaradas** para os quatro cadastros que a tela enxerga, mas não são executadas em caminho
nenhum: declarar não é executar. A passagem de gravação da transação existe e não faz outra
coisa senão devolver a área de trabalho da sessão.

### RN-03 — A tela só trabalha em consulta

A tela reconhece **uma** operação no campo da operação: a **consulta**. Qualquer outra coisa
informada nesse campo é recusada com **\* Opcao nao disponivel. Use CON \***, com o cursor de
volta ao campo, e nada é lido nem gravado.

[?] A recusa manda usar CON e o que a tela compara é o código interno da consulta; é a mesma
dúvida já registrada nas outras telas desta jornada. Ou o terminal traduz o que o servidor
digita antes de enviar, ou quem seguir a mensagem é recusado. Pergunta ao site.

[?] A recusa só é alcançada por uma mensagem do servidor: abrindo a tela sem operação na área
da sessão, a própria tela repõe a consulta, de modo que é preciso ter outra operação no campo
para vê-la. Se a máscara não oferecer ao servidor o campo da operação, a recusa é trecho sem
uso. Pergunta ao site.

### RN-04 — A abertura depende de quem chamou a tela, e a tela lê esse código

A operação e o cardápio desta tela não são escolhidos só por quem a abre: eles vêm da área de
trabalho da sessão, que a tela anterior preenche — e esta tela **lê o código da tela que a
chamou** para decidir o que fazer com o que recebeu.

- Aberta **pela opção do menu** (`C900M`), a área chega sem operação: a tela assume a
  **consulta**, abre em branco, sem cardápio carregado e sem ler cadastro nenhum.
- Aberta **pela tela da composição do cardápio** (`C910T`), a área chega com a operação de
  **consulta** — não com alteração — e com o cardápio, a descrição dele, as duas datas do
  período, o segmento, as marcas e o código do cardápio de sobremesa. A tela abre em consulta
  com esse cardápio carregado e monta a lista **desde a primeira refeição**: reconhecendo que
  veio da `C910T`, ela apaga a refeição de partida que a área tiver trazido. Vinda de qualquer
  outra origem, essa refeição de partida é mantida, e a lista começa nela.

[?] A área de trabalho é a mesma para todas as telas da sessão e o menu que abre esta tela só
limpa nela o campo da tela de origem, de seis caracteres; se o resto — a operação, o cardápio,
as datas — chega em branco depende do ambiente, que o acervo não descreve. Se não chegar, a
tela abre na operação e no cardápio que outra tela deixou, e a alteração é recusada por esta
tela. Pergunta ao site.

### RN-05 — A consulta é pelo código do cardápio e pela data limite do período

O servidor informa **o código do cardápio** e o **dia, o mês e o ano limite** do período; a
procura é sempre dentro do **tipo de órgão da sessão**. Reenviar exatamente o que já está em
tela não provoca nova procura: os valores informados são aceitos como estão.

Havendo mudança na chave, o cardápio tem de existir naquele período — não existindo, a recusa
é **\* Cardapio nao cadastrado neste periodo \***, com o cursor no campo do código do
cardápio, e nada é gravado. Existindo, a tela traz do cadastro a descrição do cardápio, a
**data de início** do período, as marcas, o código do cardápio de sobremesa e a situação de
estimativa; o **limite** continua o que o servidor informou, e a lista de refeições recomeça
da primeira.

A data de início passa pela conferência de número como as outras e é exibida, mas **não entra
na identificação**: quem identifica são o código do cardápio e a data limite.

[?] A procura usa o recurso de posicionamento do dicionário de dados e, diferente das outras
leituras desta tela e das leituras da tela da composição, **não confere a chave lida de
volta**. Se a leitura apenas posiciona no registro igual ou seguinte, um registro vizinho
passa como se fosse o cardápio informado, sem recusa. Pergunta ao site.

### RN-06 — A lista tem dez linhas, uma por refeição do cardápio

A lista é uma página de **dez** linhas, uma por refeição que aquele cardápio atende naquele
período. Cada linha traz o **código da refeição** e a **descrição** dela, buscada no cadastro
das refeições pelo tipo de órgão e pela refeição. A lista percorre o cadastro das refeições do
cardápio uma leitura por linha, a partir da refeição de partida, e só aceita o registro que
for daquele órgão, daquele cardápio e daquele período.

Uma refeição ligada ao cardápio que não estiver no cadastro de refeições aparece na linha só
com o código, **sem descrição**.

Não havendo refeição nenhuma ligada àquele cardápio naquele período, a tela avisa
**\* Cardapio sem refeicoes cadastradas \*** e não monta linha nenhuma; o aviso é decidido na
montagem da primeira linha e não se repete nas demais.

[?] O que a leitura faz com a refeição de partida não vem do material: o COBOL expandido não
traz o verbo do dialeto (primeiro, último, anterior, seguinte), só os parâmetros de posição de
cada leitura. Se ela exige a chave exata, a lista só encontra a refeição que já estiver na
sessão; se apenas posiciona, começa na refeição igual ou seguinte. Pergunta ao site.

### RN-07 — Fora da lista: o tipo de órgão, a data do sistema, a sobremesa e as quatro marcas

Fora da lista, a tela exibe a **descrição do tipo de órgão** da sessão, a **data do sistema**,
o **código do cardápio de sobremesa** com a descrição dele — buscada no cadastro do cardápio,
no mesmo período, quando o código vier preenchido — e **quatro marcas** de um caractere, que a
tela acende como **X** quando o cadastro do cardápio as traz preenchidas e deixa em branco
quando não traz.

[?] O significado de negócio das quatro marcas não vem do material lido; é a mesma dúvida já
registrada na estória da tela análoga do outro menu. Pergunta ao site.

[?] Não achando no cadastro o cardápio de sobremesa informado, a descrição fica em branco e a
tela não avisa o servidor. Se era para avisar, o caminho não avisa. Pergunta ao site.

### RN-08 — Com a marca de passagem posta, a tela entrega o cardápio à tela da composição

Quando a **marca de passagem** está posta, esta tela **não faz a consulta**: ela confere que o
cardápio existe naquele período — não existindo, recusa com **\* Cardapio nao cadastrado \***
e o cursor no código do cardápio — e entrega a transação à tela da composição do cardápio
(`C910T`).

O que ela entrega: a operação de **consulta**, o código e a descrição do cardápio, o início e
o limite do período, o segmento que estiver na sessão, as marcas de sobremesa, fruta e
estimativa, as quatro marcas do cardápio e o código do cardápio de sobremesa. A identificação
da tela de origem é apagada antes da entrega. É assim que a tela da composição abre por causa
desta: em consulta, com o cardápio carregado.

[?] A marca de passagem é um campo de um caractere que esta tela só escreve como **N**, na
montagem da última linha da lista, e nunca como **S**; nenhum rótulo da ficha da tela
corresponde a ele. Quem a preenche com **S** — o formulário, um comando ou outra tela — o
material não diz. Pergunta ao site.

### RN-09 — O que se digita é conferido como número antes de qualquer leitura

Nenhum dos campos com rótulo é texto livre. Passam pela edição numérica, antes de qualquer
leitura de cadastro — em branco valendo zero —, **nove** campos: o código do cardápio, as três
partes do início do período, as três partes do limite do período, o código do cardápio de
sobremesa e o código da refeição da linha. O que não for número é recusado no próprio campo.
Não passam por essa edição: a operação, o campo da próxima tela, as quatro marcas e a marca de
passagem.

[?] O cursor de volta ao campo recusado só está definido para **quatro** desses campos — o
código do cardápio, o dia, o mês e o ano do limite. Nos outros cinco a tela não redireciona o
cursor, e ele fica onde estava. Se era para voltar ao campo recusado em todos, o caminho não
faz. Pergunta ao site.

[?] O texto dessa recusa não está no material: a edição é uma rotina de biblioteca, cujo corpo
não faz parte do lote, e o texto sai da tabela de mensagens do idioma, que também não está no
lote. Pergunta ao site.

### RN-10 — O acesso, a rota e a permissão são conferidos antes de qualquer leitura

Na abertura, o sistema confere a permissão de segurança do perfil para esta tela; a cada
mensagem do servidor ele confere o contexto da sessão e a rota; e, quando a conferência não
devolve a marca de conformidade, a transação é interrompida e a tela sai sem mostrar nada.
Sem essas conferências, a tela não lê cadastro nenhum e não grava nada.

[?] O texto das recusas de acesso não está no material: as conferências são rotinas de
biblioteca, sem corpo no lote, e o texto sai da tabela de mensagens do sistema, que também não
está no lote. Pergunta ao site.

### RN-11 — Falha no banco interrompe a operação e avisa

Cada leitura de cadastro é seguida da conferência de erro do banco: havendo erro, a rotina
comum de comunicação despacha a ação de erro de leitura e a operação é interrompida, sem
seguir para a próxima leitura.

### RN-12 — O cadastro das refeições do cardápio não tem tela de manutenção no acervo lido

O cadastro das refeições do cardápio, que esta tela lista, não é gravado por nenhuma tela do
acervo lido: nenhuma inclui, altera, exclui ou trava registro nele. Entre os programas de
tela, ele é lido só por esta; os outros programas que o mencionam são programas de trabalho em
lote dos relatórios do módulo — um deles apaga registros dele.

[?] Quem alimenta o cadastro das refeições do cardápio no dia a dia — e por qual caminho — não
se conclui das telas do acervo lido. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: As refeições que um cardápio atende na validade dele

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C915T

  Cenário: RN-01 — consultar as refeições de um cardápio
    Dado que existe um cardápio com refeições ligadas a ele naquele período
    Quando informo o código do cardápio e o dia, o mês e o ano limite do período
    Então vejo o código e a descrição do cardápio, o início e o limite do período
    E vejo até dez linhas, uma por refeição daquele cardápio, com a descrição de cada uma
    E nada é gravado

  Cenário: RN-02 — a consulta não grava nada e não deixa rastro
    Dado que consulto as refeições de um cardápio
    Quando a consulta se conclui
    Então nenhum registro é incluído, alterado, excluído ou travado
    E nenhuma linha nova aparece na trilha de auditoria por causa desta tela

  Cenário: RN-03 — operação que a tela não reconhece
    Quando informo no campo da operação uma operação que não é a consulta
    Então vejo "* Opcao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nenhum cadastro é lido

  Cenário: RN-04 — abrir a tela pelo menu
    Dado que nenhuma tela desta sessão deixou operação na área de trabalho
    Quando abro a tela C915T pela opção do menu
    Então ela abre em consulta, em branco
    E nenhum cadastro é lido

  Cenário: RN-04 — abrir a tela pela composição do cardápio
    Dado que a tela da composição do cardápio entrega a transação a esta tela
    Quando a tela é apresentada
    Então ela abre em consulta, com o cardápio, as duas datas, o segmento e as marcas que recebeu
    E a lista das refeições é montada desde a primeira refeição

  Cenário: RN-05 — reenviar a mesma chave não procura de novo
    Dado que um cardápio está carregado em tela
    Quando confirmo outra vez, sem mudar o código do cardápio nem a data limite
    Então os valores informados são aceitos como estão
    E nada é gravado

  Cenário: RN-05 — cardápio que não existe naquele período
    Dado que informo um código de cardápio que não existe naquela data limite
    Quando confirmo a consulta
    Então vejo "* Cardapio nao cadastrado neste periodo *"
    E o cursor volta ao campo do código do cardápio
    E nada é gravado

  Cenário: RN-06 — cardápio sem refeições ligadas
    Dado que o cardápio existe naquele período e não tem nenhuma refeição ligada a ele
    Quando a tela é apresentada
    Então vejo "* Cardapio sem refeicoes cadastradas *"
    E nenhuma linha da lista é montada

  Cenário: RN-06 — refeição ligada que não está no cadastro de refeições
    Dado que uma refeição ligada ao cardápio não existe no cadastro de refeições
    Quando a tela monta aquela linha
    Então a linha aparece com o código da refeição
    E aparece sem descrição

  Cenário: RN-07 — o que a tela mostra fora da lista
    Dado que há um cardápio carregado, com o código do cardápio de sobremesa preenchido
    Quando a tela é apresentada
    Então vejo a descrição do tipo de órgão e a data do sistema
    E vejo o código do cardápio de sobremesa com a descrição dele
    E as quatro marcas do cardápio aparecem como "X" quando estão preenchidas, e em branco quando não estão

  Cenário: RN-08 — a passagem para a tela da composição
    Dado que a marca de passagem está posta e o cardápio existe naquele período
    Quando confirmo
    Então a transação passa para a tela C910T
    E ela abre em consulta, com o cardápio, o segmento, as duas datas e as marcas que esta tela entregou
    E nenhuma consulta é feita nesta confirmação

  Cenário: RN-08 — passagem com cardápio que não existe
    Dado que a marca de passagem está posta e o cardápio não existe naquele período
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor volta ao campo do código do cardápio
    E nada é gravado

  Cenário: RN-09 — campo não numérico
    Quando preencho o código do cardápio, uma das partes das datas, o código do cardápio de sobremesa ou o código da refeição com letra
    Então a tela recusa o campo antes de qualquer leitura de cadastro
    E nada é consultado por causa dele

  Cenário: RN-10 — sem a permissão de acesso
    Dado que o meu perfil não tem esta tela, ou eu não tenho a permissão da operação
    Quando entro na tela ou confirmo a consulta
    Então vejo a recusa de acesso do sistema
    E nenhum cadastro é lido e nada é gravado

  Cenário: RN-11 — falha do banco durante a leitura
    Dado que a leitura de um dos cadastros falha no banco
    Quando confirmo a consulta
    Então a transação é interrompida com a mensagem de erro do sistema
    E nenhuma linha nova é montada
```
