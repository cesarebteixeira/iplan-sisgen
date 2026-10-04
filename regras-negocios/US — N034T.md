# US — N034T — Consulta de notas fiscais e saldos de um pedido

## Estória

Como **servidor da CRE**, quero **conferir as notas fiscais e os saldos de um pedido
da minha coordenação**, para que **eu veja, gênero a gênero, o que já tem nota lançada
e como estão os saldos daquele pedido**.

Esta é a conferência do pedido: pelo número e pelo ano da entrega, o servidor vê as
notas fiscais lançadas e os saldos por subclasse e gênero. A tela não altera nada — só
lê —, e só responde ao pedido que já saiu da espera, isto é, que não está aguardando
aprovação nem aguardando distribuição, e que tem tipo de contrato e nota lançada. Sem
essas condições não há o que conferir, e a tela recusa.

## Contexto

Jornada S000M → N000M → N060M → N034T.

Ator: servidor de CRE — informa o pedido e confere, sem alterar nada, as notas fiscais
e os saldos que ele tem.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada — `N000M` e `N060M` — são **menus**: a tela é
aberta por opção de menu, e não por encadeamento de transação. Nenhuma delas deixa
pedido, operação ou registro para esta tela; o que a N034T usa da sessão — a
coordenação, o órgão, a matrícula, o código de acesso e o privilégio — é o que a
entrada deixou, e a tela apenas o repassa às conferências. A tela **não muda de
comportamento conforme quem a chamou**: ela mesma fixa a consulta, e a consulta é a
única operação que ela atende.

A tela mostra a descrição do órgão da sessão e a data do sistema, o código e a razão
social do fornecedor do pedido, a marca de acúmulo e uma grade de 15 linhas com a
subclasse, o gênero, o número da nota fiscal, a descrição do gênero e os saldos. Ela é
o último passo desta jornada e **não encaminha o servidor a lugar nenhum**.

---

## Regras de negócio

### RN-01 — A tela consulta as notas fiscais e os saldos de um pedido

A tela responde por **um pedido**: informados a coordenação regional, o número do
pedido e o ano da entrega, ela mostra o que o pedido tem de **nota fiscal lançada** e
como estão os **saldos por subclasse e gênero**.

A grade tem **15 linhas**. Cada linha traz a subclasse, o código do gênero, o número da
nota fiscal e a descrição do gênero; e, **uma vez por par subclasse/gênero**, a
quantidade do gênero e os saldos daquela classificação. Acima da grade a tela mostra a
**descrição do órgão da sessão**, a **data do sistema**, o **código do fornecedor** do
pedido com a sua **razão social** e, quando o pedido está marcado como acumulado, a
**marca de acúmulo**.

[?] A tela mostra três saldos por classificação, além da quantidade do gênero. O
dicionário de dados os nomeia como saldo do pedido, saldo recebido e um terceiro cujo
sentido não se conclui do nome nem de texto de tela — a máscara da tela não está no
material lido. Pergunta ao site.

### RN-02 — A tela não grava nada

A tela só lê. Ela enxerga **oito** cadastros — o de telas, o de pedidos, o de
classificações do pedido, o de gêneros, o de notas fiscais, o de notas fiscais por
processo, o de tipos de contrato e o de fornecedores —, e traz, para cada um deles, as
rotinas de gravar, excluir e travar; **nenhuma delas é executada**. Quem consulta não
altera pedido, nota, contrato nem fornecedor.

### RN-03 — A consulta é a única operação aceita

A tela atende **uma** operação: a consulta. Chegando com qualquer outra, ela recusa com
**\* Operacao nao disponivel. Use CON \***, deixa o cursor no campo da operação e não
lê nem grava nada. Não há, nesta tela, caminho de inclusão, alteração ou exclusão.

A tela não muda de comportamento conforme quem a abriu: é ela mesma que fixa a
consulta.

[?] O campo da operação não é preenchido por ninguém nesta jornada: quem o traz é a
requisição, e a tela escreve nele o código da consulta antes de trabalhar. Se a recusa
por outra operação chega a aparecer para um servidor na tela, ou se ela só protege
contra requisição de outro programa, o material lido não decide — a máscara, que
mostraria o campo, não está no lote. Pergunta ao site.

### RN-04 — A coordenação regional é obrigatória

A consulta é sempre de uma **coordenação regional**. Sem ela informada, a recusa é
**\* Informe o grupo \***, com o cursor de volta ao campo.

[?] Essa recusa só é alcançável quando a sessão **não** traz coordenação nenhuma. Com
coordenação na sessão — o caso do servidor de CRE —, o campo em branco é barrado
**antes**, pela conferência que compara a coordenação informada com a da sessão: o
branco vale zero, a comparação falha e a mensagem que o servidor vê é
**\* Usuario sem acesso a outro grupo \***, e não a de campo obrigatório. Ou a ordem
das duas conferências está invertida, ou "Informe o grupo" serve a um caso que este
caminho não alcança. Não se escolhe um dos lados. Pergunta ao site.

### RN-05 — Cada servidor só consulta a coordenação do seu vínculo

Quando o vínculo da sessão traz uma coordenação, o pedido só é consultado se a
coordenação informada for essa mesma; sendo outra — ou vindo o campo em branco —, a
recusa é **\* Usuario sem acesso a outro grupo \***, com o cursor de volta ao campo. A
conferência não é só de leitura: no passo seguinte a coordenação informada é
**substituída** pela da sessão. Sem coordenação na sessão, essa conferência não é
feita.

### RN-06 — O pedido é identificado pelo número e pelo ano da entrega

O número do pedido é digitado com **6 dígitos**, mas o pedido é identificado por
**10**: o sistema junta o número nas seis primeiras posições e o **ano da entrega**
(4 dígitos) nas quatro últimas. É essa chave de dez posições, junto do órgão e da
coordenação, que procura o pedido. O mesmo número com outro ano da entrega é **outro**
pedido.

### RN-07 — O pedido tem de existir e não estar excluído

Não achando o pedido, a recusa é **\* Pedido nao cadastrado \***, com o cursor no
número do pedido. Achando-o marcado como **excluído**, a recusa é
**\* Pedido excluido \***, no mesmo campo. Quando o pedido informado é o mesmo da
consulta anterior, a tela não o procura de novo: aproveita o que já conferiu.

### RN-08 — O pedido tem de estar liberado, não pendente

Pedido com a situação **em branco** é recusado com
**\* Pedido pendente de aprovacao \***; pedido com a situação **"P"** é recusado com
**\* Pedido pendente de distribuicao \***. Qualquer outra situação registrada passa: a
tela só barra esses dois estados de espera.

[?] O dicionário de dados não traz domínio para a situação do pedido: o material lido
mostra apenas que o branco e o "P" recusam e que **qualquer outro** valor segue. Quais
valores existem, e qual deles significa aprovado ou distribuído, pergunta ao site.

### RN-09 — O tipo de contrato do pedido é conferido no cadastro

Passada a existência do pedido, a tela procura o **tipo de contrato** dele. Pedido sem
tipo de contrato é recusado com **\* Pedido sem tipo contrato \***; tipo informado que
não existe no cadastro é recusado com **\* Tipo contrato nao cadastrado \***. Nos dois
casos o cursor volta ao número do pedido.

### RN-10 — Pedido de operação logística é de outra tela

Quando o tipo de contrato do pedido está marcado como de **operação logística**, a
recusa é **\* Pedido de oper.logistico. Use N334T \***, com o cursor no número do
pedido: esse pedido é acompanhado pela tela N334T.

### RN-11 — O fornecedor do pedido é mostrado pela razão social

O fornecedor vem do próprio pedido; a tela usa o código dele para buscar a **razão
social** no cadastro de fornecedores e mostra as duas coisas juntas.

### RN-12 — A forma da consulta é obrigatória

A tela exige que o servidor diga **se a consulta é com número de processo ou não**: a
resposta é "sim" ou "não", e qualquer outro preenchimento é recusado com
**\* Inf consulta com numero de processo ou nao \***, com o cursor de volta ao campo. A
resposta escolhe de qual conjunto de notas fiscais a tela lê depois.

[?] Quando a área de trabalho da tela chega em branco, ela mesma escreve "sim" no
campo; mas a conferência é feita sobre o que veio informado, e não sobre o que ela
escreveu. Se o campo em branco é mesmo recusado, ou se o valor que a tela sugere chega
antes da conferência, o material lido não decide. Pergunta ao site.

### RN-13 — O pedido tem de ter notas fiscais no conjunto indicado

Confirmado o pedido, a tela percorre as notas fiscais dele no conjunto correspondente à
resposta — com número de processo ou sem — e exige **pelo menos uma nota viva**: nota
marcada como excluída não conta. Não achando nenhuma, a recusa é
**\* Pedido sem notas cadastradas \***, com o cursor no número do pedido. A mesma
recusa aparece quando o pedido não tem nenhuma classificação registrada.

[?] O material lido mostra dois conjuntos distintos de notas fiscais — um para a
consulta com número de processo e outro para a consulta sem ele —, mas não diz como os
dois se distinguem, nem o que cada um guarda de diferente. Pergunta ao site.

### RN-14 — Cada linha mostra o gênero buscado pela data da nota

A descrição do gênero mostrada em cada linha é buscada no cadastro de gêneros pela
subclasse, pelo código do gênero e pelo **ano, mês e dia de emissão da nota fiscal**;
os gêneros marcados como excluídos não entram na busca.

[?] Não se conclui do material lido se a data de emissão da nota participa mesmo da
busca — e portanto se a descrição mostrada é a vigente naquela data — ou se a leitura
pega o primeiro gênero da classificação e ignora a data. Os sinalizadores da leitura
são dialeto do banco e não estão explicados no corpus. Pergunta ao site.

### RN-15 — Pedido acumulado mostra os saldos acumulados

Quando o pedido está marcado como **acumulado**, a tela mostra os saldos acumulados da
classificação; quando não está, mostra os saldos correntes. A marca aparece na tela
como um **asterisco**. Os valores aparecem **uma vez por par subclasse/gênero**: a
segunda linha do mesmo par não os repete.

### RN-16 — Os três códigos de cada linha não selecionam nada

Cada uma das 15 linhas tem três códigos — a subclasse, o código do gênero e o número da
nota fiscal —, e todos passam pela conferência de número. Mas eles **não escolhem** o
que a tela lê: a tela percorre todas as notas do pedido e devolve as linhas já
preenchidas com o que leu, sobrepondo-se ao que o servidor digitou.

[?] Se os três códigos deveriam filtrar a consulta, e o que a tela deveria fazer quando
eles não correspondem a nenhuma nota do pedido, o material lido não diz: fora da
conferência de número, nenhuma comparação é feita com eles. Pergunta ao site.

### RN-17 — Os campos de número passam por edição

Os **seis** campos de número da tela — a coordenação (2 dígitos), o número do pedido
(6), o ano da entrega (4) e os três códigos da linha: subclasse (2), gênero (5) e
número da nota fiscal (9) — passam por edição antes de qualquer leitura de cadastro: o
que estiver em branco vira zero, os zeros à esquerda caem e o que não for número é
recusado, com o cursor de volta ao campo recusado. O que não passa por essa edição não
chega a ser procurado.

[?] Dos seis campos, só os **três** primeiros têm posição de cursor declarada; quando a
edição recusa um dos três códigos da linha, não se sabe para onde o cursor volta.
Pergunta ao site.

### RN-18 — A tela é terminal e não encaminha o servidor

A tela não manda o servidor para nenhuma outra: é o fim da jornada. E se a requisição
chega já com uma **tela de destino** indicada, ela não faz nada — não confere, não lê e
não mostra mensagem.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta de notas fiscais e saldos de um pedido

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a coordenação regional e o órgão do meu vínculo
    E tenho acesso à tela N034T

  Cenário: Consulta de um pedido com notas fiscais
    Dado que existe um pedido liberado e com notas fiscais lançadas na minha coordenação
    Quando informo a coordenação, o número do pedido e o ano da entrega
    E indico que a consulta é com número de processo
    Então vejo as notas fiscais do pedido nas linhas da grade
    E cada linha traz a subclasse, o gênero e a descrição do gênero
    E, uma vez por par subclasse/gênero, vejo a quantidade do gênero e os saldos
    E vejo o código e a razão social do fornecedor do pedido
    E nada é gravado

  Cenário: O pedido é identificado pelo número com o ano da entrega
    Dado que existe um pedido com o número informado no ano da entrega indicado
    Quando informo o número do pedido com outro ano da entrega
    Então vejo "* Pedido nao cadastrado *"

  Cenário: Operação diferente da consulta
    Dado que estou na tela N034T
    Quando a requisição chega com uma operação que não é a consulta
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor fica no campo da operação
    E nada é lido nem gravado

  Cenário: Consulta sem a coordenação regional
    Dado que a minha sessão não carrega coordenação nenhuma
    Quando peço a consulta sem informar a coordenação
    Então vejo "* Informe o grupo *"
    E o cursor volta ao campo da coordenação

  Cenário: Coordenação de outro grupo
    Dado que a minha sessão carrega a coordenação do meu vínculo
    Quando informo uma coordenação diferente da minha
    Então vejo "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo da coordenação
    E nada é consultado

  Cenário: Pedido não cadastrado
    Dado que o pedido informado não existe no órgão da minha sessão
    Quando peço a consulta
    Então vejo "* Pedido nao cadastrado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido excluído
    Dado que o pedido informado está marcado como excluído
    Quando peço a consulta
    Então vejo "* Pedido excluido *"
    E o cursor volta ao campo do número do pedido

  Esquema do Cenário: Pedido que ainda está na espera
    Dado que o pedido informado está com a situação <situação>
    Quando peço a consulta
    Então vejo "<mensagem>"
    E o cursor volta ao campo do número do pedido

    Exemplos:
      | situação   | mensagem                            |
      | em branco  | * Pedido pendente de aprovacao *    |
      | P          | * Pedido pendente de distribuicao * |

  Cenário: Pedido sem tipo de contrato
    Dado que o pedido informado não tem tipo de contrato
    Quando peço a consulta
    Então vejo "* Pedido sem tipo contrato *"
    E o cursor volta ao campo do número do pedido

  Cenário: Tipo de contrato não cadastrado
    Dado que o pedido informado aponta um tipo de contrato que não existe no cadastro
    Quando peço a consulta
    Então vejo "* Tipo contrato nao cadastrado *"
    E o cursor volta ao campo do número do pedido

  Cenário: Pedido de operação logística
    Dado que o tipo de contrato do pedido é de operação logística
    Quando peço a consulta
    Então vejo "* Pedido de oper.logistico. Use N334T *"
    E o cursor volta ao campo do número do pedido

  Cenário: Razão social do fornecedor do pedido
    Dado que o fornecedor do pedido informado está cadastrado
    Quando peço a consulta
    Então vejo o código do fornecedor do pedido e a razão social dele

  Cenário: Forma da consulta não indicada
    Dado que estou na tela N034T
    Quando peço a consulta sem dizer se ela é com número de processo
    Então vejo "* Inf consulta com numero de processo ou nao *"
    E o cursor volta ao campo da forma da consulta

  Cenário: A consulta com número de processo lê o conjunto daquele processo
    Dado que o pedido informado só tem notas no conjunto da consulta com número de
      processo
    Quando indico que a consulta é com número de processo
    Então vejo as notas fiscais do pedido nas linhas da grade

  Cenário: A consulta sem número de processo lê o outro conjunto
    Dado que o pedido informado só tem notas no conjunto da consulta com número de
      processo
    Quando indico que a consulta é sem número de processo
    Então vejo "* Pedido sem notas cadastradas *"
    E o cursor volta ao campo do número do pedido

  Cenário: Nota excluída não conta como nota do pedido
    Dado que todas as notas do pedido informado estão marcadas como excluídas
    Quando peço a consulta
    Então vejo "* Pedido sem notas cadastradas *"
    E o cursor volta ao campo do número do pedido

  Cenário: A descrição do gênero de cada linha
    Dado que o gênero da nota tem descrição no cadastro
    Quando peço a consulta
    Então cada linha da grade traz a descrição do gênero buscada pela subclasse, pelo
      código do gênero e pela data de emissão da nota

  Esquema do Cenário: Os saldos que a linha mostra
    Dado que o pedido informado <acúmulo>
    Quando peço a consulta
    Então a linha mostra <saldos>

    Exemplos:
      | acúmulo           | saldos               |
      | está marcado      | os saldos acumulados |
      | não está marcado  | os saldos correntes  |

  Cenário: A marca de acúmulo aparece na tela
    Dado que o pedido informado está marcado como acumulado
    Quando peço a consulta
    Então vejo o asterisco que marca o acúmulo na tela

  Cenário: Os valores aparecem uma vez por par subclasse/gênero
    Dado que o pedido tem duas notas do mesmo par subclasse/gênero
    Quando peço a consulta
    Então a quantidade e os saldos aparecem só na primeira linha do par
    E a segunda linha do par traz o número da outra nota, sem repetir os valores

  Cenário: Os três códigos digitados na linha não filtram
    Dado que estou na tela N034T com um pedido consultado
    Quando troco a subclasse e o gênero de uma linha e confirmo
    Então a tela devolve as linhas com o que leu do pedido
    E os códigos que digitei não mudam o que é mostrado

  Cenário: Campo de número que não é número
    Dado que estou na tela N034T
    Quando digito algo que não é número em um dos campos de número
    Então a tela recusa o campo antes de procurar no cadastro
    E o cursor volta ao campo recusado
    E nada é consultado

  Cenário: A tela não encaminha o servidor
    Dado que chego à tela N034T com uma tela de destino já indicada
    Quando a requisição é processada
    Então a tela não confere, não lê e não mostra mensagem
    E não me leva a outra tela

  Cenário: A consulta não grava nada
    Dado que consultei um pedido
    Quando a consulta termina
    Então nenhum pedido, nota fiscal, tipo de contrato ou fornecedor é incluído,
      alterado ou excluído
    E nada fica gravado
```
