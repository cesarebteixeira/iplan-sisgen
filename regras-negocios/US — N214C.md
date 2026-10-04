# US — N214C — Consultar notas fiscais e devoluções por fornecedor e ano

## Estória

Como **servidor da CRE**, quero **consultar, pelo meu grupo, as notas fiscais de um
fornecedor num ano de emissão, com as devoluções e os valores de cada uma**, para
que **eu veja numa tela só o que aquele fornecedor faturou e o que voltou contra
cada nota, e possa abrir a nota para conferir o detalhe**.

A nota fiscal diz o que o fornecedor entregou; a nota de devolução, o que voltou
contra ela. Quem confere a despesa do grupo precisa ver as duas juntas — as datas e
os valores lado a lado — para saber o que ainda está em aberto e o que já foi
abatido. Sem esta consulta, a conferência se faz pela lista das devoluções do ano,
sem o valor da nota correspondente. Esta tela só mostra: quem lança e mantém as
notas e as devoluções são as telas de manutenção.

## Contexto

Jornada S000M → N000M → N050M → N210M → N214C.
Ator: servidor de CRE — consulta as notas fiscais de um fornecedor do seu grupo,
num ano, e as devoluções lançadas contra cada uma.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os três passos antes desta tela — o `N000M`, o `N050M` e o `N210M` — são menus: só
encaminham e não deixam dado de negócio para ela. O contexto que a `N214C` usa — o
tipo de órgão, o grupo (a coordenação regional escolar) e a data do sistema — é o
que a entrada deixou na sessão; esta tela não o recalcula.

A tela não é folha solta: marcada uma linha da lista, ela encaminha à tela da nota
fiscal (`N214T`) sem passar por menu, e é essa passagem (RN-09) que dá sentido à
lista.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela é de consulta: só a consulta é aceita

Esta tela não inclui, não altera e não exclui: ela só mostra. Ao se apresentar, ela
mesma fixa a operação como **consulta**. Chegando uma mensagem com a operação em
branco, a tela recusa com **\* Operacao nao disponivel. Use CON \***, devolve o
cursor ao campo da operação e não lê cadastro nenhum. Uma operação de inclusão,
alteração ou exclusão não chega a essa recusa: a conferência de rota do sistema
recusa antes, com **\* Operacao nao disponivel \***, porque a tela se declara como
não sendo de manutenção.

[?] A recusa própria da tela só vale se a máscara oferecer o campo da operação em
branco — e a própria tela repõe a consulta antes de exibir. O desenho da tela está
na máscara, que não faz parte do lote; se o campo não existir, a recusa é trecho sem
uso. Pergunta ao site.

### RN-02 — A procura é pelo grupo, pelo fornecedor e pelo ano, no tipo de órgão da sessão

A consulta usa três dados informados — a **coordenação regional escolar** (o grupo),
o **código do fornecedor** e o **ano de emissão da nota fiscal** — e, além deles, o
**tipo de órgão** que vem da sessão: a tela não procura nota de outro tipo de órgão.
O grupo, o fornecedor e o ano são os campos que o servidor informa; os demais
valores que a tela mostra (os números das notas, as datas, os valores e a razão
social) voltam do cadastro e são escritos por ela.

Os campos numéricos da tela passam pela edição numérica antes de qualquer leitura —
são **7** (contados um a um pelos rótulos de edição) — e o que chega em branco vira
zero. Quando a combinação informada é exatamente a mesma da consulta anterior, a
tela aceita sem reler o cadastro.

[?] Quatro dos sete campos editados não têm rótulo de negócio: são os quatro números
da lista (o número da nota fiscal, o número da nota de devolução e os dois números
que a tela guarda para continuar a lista a partir da última linha lida), e a edição
os identifica pelo nome interno do campo. Quem os rotula é a máscara, que não faz
parte do lote. Pergunta ao site.

[?] O tipo de órgão vem da área da sessão, e a árvore expandida só o inicializa em
branco: quem o transporta são as rotinas comuns. Se o transporte não chegar antes
da tela, a procura sai pelo tipo de órgão zero e não acha nota nenhuma. O acervo não
mostra o momento do transporte. Pergunta ao site.

### RN-03 — O fornecedor e o ano são obrigatórios

Sem o fornecedor, a recusa é **\* Informe o fornecedor \***; com o fornecedor e sem
o ano, **\* Informe o ano \***. Cada recusa devolve o cursor ao campo que falta e
interrompe a consulta antes de qualquer leitura. O grupo não tem recusa própria de
preenchimento: quando ele não é informado, quem decide é a conferência de grupo da
RN-04 — e, se o servidor não tem grupo na sessão, o grupo em branco passa.

### RN-04 — O grupo informado tem de ser o do servidor

Quando o servidor tem coordenação regional escolar (o grupo) na sessão, o grupo
informado tem de ser o mesmo; sendo outro, a recusa é
**\* Usuario sem acesso a este grupo \*** e o cursor volta ao campo do grupo. Quem
não tem grupo na sessão passa sem essa conferência.

[?] O grupo conferido vem da área da sessão, não do cadastro da nota — é a mesma
dúvida da RN-02. Se o valor chegar zerado, a conferência não recusa nada e a tela
aceita o grupo de qualquer coordenação. Pergunta ao site.

### RN-05 — O fornecedor informado tem de estar cadastrado e não pode estar excluído

O código do fornecedor é procurado no cadastro de fornecedores (`C030T`). Não
existindo, a consulta é interrompida pela recusa de cadastro do próprio sistema, que
aponta o campo do fornecedor. Existindo, mas com a ficha marcada como **excluída**
ou com a marca do **apagamento definitivo**, a consulta também é recusada, e a lista
não é montada.

[?] O texto dessas duas recusas não está no acervo: a da ficha não cadastrada é montada
pela rotina comum do sistema e a da ficha excluída sai da tabela de mensagens — a
tabela, que é de onde saem os dois textos, não veio no lote. O que o servidor lê em
cada uma é pergunta ao site.

### RN-06 — O ano informado tem de ter nota de devolução lançada para aquele fornecedor

Antes de montar a lista, a tela procura, para o tipo de órgão da sessão e para o
grupo, o fornecedor e o ano informados, a primeira nota de devolução lançada. Não
achando nenhuma, a recusa é **\* Devolucoes nao cadastradas para este ano \***, com
o cursor de volta ao campo do ano, e a lista não é apresentada.

### RN-07 — A tela mostra até 12 notas fiscais de devolução, com as datas e os valores

A lista sai do cadastro que liga a nota fiscal à nota de devolução do fornecedor
(`N213T`), na ordem do número da nota, e a tela mostra **12 linhas** por vez. De
cada linha o servidor vê o **número da nota fiscal**, a **data de emissão** (dia,
mês e ano), o **valor total da nota fiscal**, o **número da nota de devolução**, a
**data da devolução** e o **valor da devolução**; a outra coluna é a marca da linha,
da RN-09.

O valor total da nota fiscal não fica no cadastro da ligação: a tela o busca na nota
fiscal do fornecedor e, quando lá não o acha (ou o acha zerado), no cadastro das
notas fiscais sem processo. O valor da devolução vem do próprio cadastro da ligação.
As datas são montadas no formato dia/mês/ano a partir dos campos separados de dia,
mês e ano — a tela não mostra a data como ela está guardada.

A capacidade declarada dos cadastros desta consulta é: **10.000** para a ligação
entre a nota e a devolução, **29.000.000** para as notas fiscais, **150.000** para
as notas fiscais sem processo, **50.000** para os itens da devolução por gênero e
**12.000** para os órgãos. Capacidade é o **máximo esperado** — parâmetro de
dimensionamento —, **não** o volume cadastrado.

[?] Como a lista é preenchida linha a linha — qual nota cai em qual linha, e o que a
tela faz quando o fornecedor e o ano têm mais de 12 notas — depende do mecanismo de
repetição do gerador, que o acervo não explica. A tela monta 12 cópias e para; se há
uma forma de ver a décima terceira nota, ela não foi determinada. Pergunta ao site.

[?] O que distingue, no negócio, o cadastro das notas fiscais do cadastro das notas
fiscais sem processo não está em nenhum texto do acervo: a tela lê o valor nas duas,
na mesma ordem, e troca de cadastro só quando o valor não vem da primeira. Pergunta
ao site.

### RN-08 — Quando não há nada para listar, a tela avisa

Quando a lista não tem nenhuma linha — o ano tem nota de devolução lançada, mas a
leitura da lista não devolve linha nenhuma —, o aviso é
**\* Notas de devolucao nao cadastradas \*** e a lista sai vazia.

[?] A recusa da RN-06 e este aviso dizem quase a mesma coisa por dois caminhos
diferentes: um confere o ano contra a primeira nota de devolução do fornecedor,
antes de montar a lista; o outro é a própria montagem da lista, quando a leitura da
primeira linha não acha nada. Pelo caminho normal da digitação o primeiro já barrou,
de modo que não se sabe em que situação o servidor vê o segundo. Pergunta ao site.

### RN-09 — Marcar a linha entrega a nota à tela seguinte, que abre em consulta

A coluna de marca de cada linha é uma escolha: marcada a linha com **X** e tendo ela
um número de nota fiscal, a tela **não** segue com operação própria — ela entrega à
tela da nota fiscal (`N214T`) o **registro daquela linha** (a coordenação, o
fornecedor com a razão social, o ano, o número da nota fiscal e o da nota de
devolução, as duas datas, o órgão, o tipo de contrato, o número do pedido com o ano
da entrega e os dois valores) e a **operação de consulta**, e sinaliza a chamada.
Não há menu entre as duas.

A tela seguinte abre, por isso, já sobre aquela nota e **em consulta**: é a operação
recebida que decide o modo dela, e é a mesma passagem que a dispensa de exigir a
consulta prévia quando o servidor quiser alterar. Linha marcada e sem número de nota
não abre nada: a tela simplesmente segue para a linha seguinte.

[?] Não está no acervo o que faz a marca valer "X" para uma linha da lista; a tela
apenas a testa e a limpa. Sem saber quem a preenche, não se sabe se a passagem para a
nota é alcançável pelo usuário. Pergunta ao site.

[?] Para achar o item da devolução, a tela procura a nota de devolução com a
subclasse e o gênero **zerados**. Se a leitura procurar a **chave exata**, nenhum
item é encontrado; se procurar a **primeira chave igual ou maior**, ela acha o
primeiro item. **A passagem para a nota depende disso.** O recurso de leitura é
importado de fora do lote. Pergunta ao site.

[?] Quando o item da devolução não é achado, a tela **não** recusa: ela segue para a
nota com o número do pedido que estiver na área de trabalho, que pode ser o da
devolução anterior. O acervo não mostra se esse é o pedido certo. Pergunta ao site.

### RN-10 — Cada mensagem começa com os campos de resultado em branco

Antes de conferir a digitação e de ler o cadastro, a resposta apaga **7** campos de
resultado: a descrição do órgão, a data do sistema, a razão social do fornecedor, a
data de emissão e o valor total da nota fiscal e a data e o valor da devolução. Uma
consulta recusada não deixa na tela o resultado da anterior; quem os repõe é a
apresentação da tela.

[?] A resposta apaga também a data do sistema e a descrição do órgão, e só a
apresentação da tela as repõe — recebendo-as da área da sessão, que a árvore
expandida inicializa em branco (ver RN-02). Se o ambiente não reexecutar a
apresentação depois da mensagem, o operador responde e vê esses campos vazios. A
ordem de chamadas do ambiente não está no acervo. Pergunta ao site.

### RN-11 — A consulta não grava nada e não deixa rastro de auditoria

A tela e as rotinas comuns que ela chama só leem: nenhum registro é incluído,
alterado ou excluído e nenhum registro de auditoria é gerado. Das **7** bases de
dados que o programa enxerga, **7** são lidas, e as rotinas de gravação, de exclusão
e de travamento existem declaradas para todas as 7 — **sem que nenhuma delas seja
executada em nenhum caminho**. Declarar não é executar.

### RN-12 — Antes de consultar, o sistema confere o acesso e a permissão da tela

Toda apresentação da tela passa pela conferência de que a tela está no cadastro de
telas e relatórios e de que a matrícula tem acesso a ela: não estando, as recusas
são as da entrada (**\* Acesso negado para esta matricula \*** e
**\* Tela nao disponivel \***). A mensagem passa ainda pela lógica de rota, que
recusa a tela retirada do cadastro (**\* Tela nao cadastrada \***) e a operação que
ela não reconhece (**\* Operacao nao disponivel \***), e pela conferência de
permissão por operação — que, na consulta, aprova sem exigir autorização específica
de operação.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar as notas fiscais e as devoluções de um fornecedor, por grupo e ano

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N214C

  Cenário: RN-02 e RN-07 — consultar um fornecedor num ano e ver as notas e as devoluções
    Dado que estou na tela N214C com a opção de consulta
    E informo a coordenação regional escolar, o código de um fornecedor cadastrado e um ano de emissão que tenha devolução lançada
    Quando confirmo a consulta
    Então vejo até 12 linhas, cada uma com o número da nota fiscal, a data de emissão, o valor total da nota, o número da nota de devolução, a data da devolução e o valor da devolução
    E vejo a razão social do fornecedor e a data do sistema
    E nada é gravado

  Cenário: RN-02 — a procura é dentro do tipo de órgão da minha sessão
    Dado que o fornecedor e o ano informados só têm nota de devolução em outro tipo de órgão
    Quando consulto
    Então a tela não considera essas notas
    E vejo a mensagem "* Devolucoes nao cadastradas para este ano *"

  Cenário: RN-02 — repetir a mesma chave não relê o cadastro
    Dado que consultei um fornecedor e a consulta foi aceita
    Quando envio a mensagem outra vez com o mesmo grupo, o mesmo fornecedor e o mesmo ano
    Então a tela aceita sem reler o cadastro

  Cenário: RN-03 — sem o fornecedor
    Quando envio a mensagem sem o código do fornecedor
    Então vejo a mensagem "* Informe o fornecedor *"
    E o cursor volta ao campo do fornecedor

  Cenário: RN-03 — sem o ano
    Dado que informei um fornecedor
    Quando envio a mensagem sem o ano de emissão
    Então vejo a mensagem "* Informe o ano *"
    E o cursor volta ao campo do ano

  Cenário: RN-04 — grupo de outra coordenação
    Dado que a sessão tem uma coordenação regional escolar
    Quando informo a coordenação regional escolar de outro grupo
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo do grupo

  Cenário: RN-04 — servidor sem grupo na sessão
    Dado que a sessão não tem coordenação regional escolar
    Quando informo qualquer coordenação regional escolar com fornecedor e ano válidos
    Então a tela aceita o grupo informado
    E a lista é apresentada

  Cenário: RN-05 — fornecedor não cadastrado
    Quando informo um código de fornecedor que não existe no cadastro de fornecedores
    Então a consulta é recusada pela recusa de cadastro do sistema, apontando o campo do fornecedor
    E a lista não é apresentada

  Cenário: RN-05 — fornecedor excluído
    Dado que o código informado é de um fornecedor marcado como excluído
    Quando consulto
    Então a consulta é recusada com a mensagem de fornecedor fora de uso
    E a lista não é apresentada

  Cenário: RN-06 — ano sem nota de devolução para o fornecedor
    Dado que informo um fornecedor cadastrado e um ano sem devolução lançada para ele
    Quando consulto
    Então vejo a mensagem "* Devolucoes nao cadastradas para este ano *"
    E o cursor volta ao campo do ano
    E a lista não é apresentada

  Cenário: RN-08 — a lista sai vazia
    Dado que a leitura da lista não devolve linha nenhuma
    Quando a tela monta a lista
    Então vejo a mensagem "* Notas de devolucao nao cadastradas *"
    E nenhuma linha é apresentada

  Cenário: RN-09 — de uma linha da lista para a nota fiscal
    Dado que a lista mostra as notas de devolução de um fornecedor
    Quando marco com "X" a linha de uma nota
    Então o sistema abre a tela da nota fiscal N214T sobre aquela nota
    E essa tela abre em consulta
    E leva junto a coordenação, o fornecedor com a razão social, o ano, o número da nota e o da devolução, as datas, o órgão, o tipo de contrato, o número do pedido com o ano da entrega e os dois valores

  Cenário: RN-09 — linha marcada sem número de nota
    Dado que marco com "X" uma linha sem número de nota fiscal
    Quando confirmo a mensagem
    Então nenhuma tela é aberta
    E a tela segue para a linha seguinte

  Cenário: RN-01 — a tela abre em consulta
    Dado que abro a tela N214C sem informar a operação
    Então a tela assume a consulta

  Cenário: RN-01 — operação em branco é recusada
    Dado que estou na tela N214C e a mensagem chega com a operação em branco
    Quando confirmo a mensagem
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nenhum cadastro é lido nesse caminho

  Cenário: RN-01 — operação de manutenção é recusada antes pela rota
    Dado que a mensagem chega com uma operação de inclusão, alteração ou exclusão
    Quando confirmo a mensagem
    Então a conferência de rota recusa com "* Operacao nao disponivel *"
    E nada é lido nem gravado

  Cenário: RN-10 — cada mensagem começa com os campos de resultado em branco
    Dado que a tela mostrou a razão social, a data do sistema, a descrição do órgão, as datas e os valores
    Quando respondo a mensagem
    Então esses campos voltam em branco antes da conferência da digitação

  Cenário: RN-11 — a consulta não grava nada
    Dado que abro a tela N214C
    Quando a lista e as devoluções são mostradas
    Então nenhum registro é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: RN-12 — tela não cadastrada
    Dado que a tela N214C não está no cadastro de telas e relatórios
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo consultar

  Cenário: RN-12 — sem autorização para a tela
    Dado que a minha matrícula não tem a tela N214C no seu código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo consultar
```
