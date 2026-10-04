# US — N031T — Consulta e exclusão de notas fiscais de fornecedor

## Estória

Como **servidor da CRE**, quero **ver as notas fiscais de um fornecedor na minha coordenadoria e excluir a nota
lançada errada**, para que **a quantidade e o valor daquela nota saiam do contrato e o pedido volte a refletir o que
foi entregue de fato**.

A nota fiscal do fornecedor é registrada por outra tela; esta é a que desfaz o registro, item por item, devolvendo ao
contrato o que a nota havia consumido e reabrindo o pedido. É também a que mostra, para uma coordenadoria regional
escolar, tudo o que um fornecedor tem de nota, com o valor somado. Sem ela, um lançamento errado fica para sempre no
contrato, e a compra seguinte nasce sobre uma conta que não é real. Toda exclusão fica registrada para auditoria; a
consulta, não.

## Contexto

Jornada S000M → N000M → N050M → N031T.
Ator: servidor de CRE — informa a coordenadoria regional escolar e o fornecedor, vê as notas fiscais que esse
fornecedor tem no sistema e, quando precisa, marca a linha da nota que deve ser excluída.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu a abre — está
em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada são menus: elas não encadeiam a N031T, apenas a abrem. O que a N031T usa — a
matrícula, o código de acesso, o tipo de órgão e a coordenadoria regional escolar — é o que a entrada deixou na
sessão, e essas regras estão no documento da entrada. A N031T é o último passo da jornada: por este caminho ela não
encadeia outra tela e não entrega registro nem operação a ninguém. As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela trabalha em consulta ou em alteração, e só a alteração exclui

A tela é aberta em um de dois modos: consulta ou alteração. Qualquer outro modo é recusado com
* Opcao nao disponivel. Use ALT ou CON * e o cursor volta ao campo do modo. Na consulta a tela só mostra e soma; a
exclusão de uma nota exige as duas coisas juntas — o modo de alteração **e** a linha da nota marcada para exclusão.
O modo pedido é também a operação que a tela apresenta às conferências de rota e de permissão: quem não tem a
permissão de alterar não chega ao trecho que grava, e quem não tem a de excluir não exclui (RN-16).

### RN-02 — A tela lê nove cadastros e escreve em seis

A tela enxerga nove cadastros: o registro das telas, o dos órgãos, o dos fornecedores, o das notas fiscais, o dos
itens das notas, o dos pedidos, o dos itens dos pedidos, o dos contratos e o da auditoria. Escreve em seis deles:
apaga a nota fiscal e cada um dos seus itens, atualiza o contrato, o item do pedido e o pedido, e cria o registro de
auditoria. Nos cadastros de negócio não entra registro novo: as atualizações são de registros que já existiam e as
duas exclusões são apagamentos; a única criação é a do registro de auditoria. O que a tela escreve depende do modo e
da marca da linha (RN-01); em consulta, nada é escrito.

### RN-03 — A coordenadoria regional escolar é a da sessão

A coordenadoria regional escolar é a chave da consulta. Quando a sessão já carrega uma, a tela a traz preenchida e
não deixa o servidor trabalhar em outra: outra coordenadoria é recusada com * Usuario sem acesso a outro grupo *,
com o cursor no campo da coordenadoria. Quando a sessão não carrega nenhuma, a coordenadoria é exigida — sem ela a
recusa é * Informe o grupo *, no mesmo campo. Nas duas situações a recusa vale para consulta e para alteração.

[?] Esta tela não confere a coordenadoria contra o cadastro das coordenadorias regionais escolares: nenhuma leitura
desse cadastro aparece no programa, ao contrário do que outras telas do mesmo módulo fazem. Se uma coordenadoria
informada à mão pode não existir, pergunta ao site.

### RN-04 — O fornecedor é obrigatório e tem de estar cadastrado

Na consulta, o fornecedor é exigido: sem ele a recusa é * Informe o codigo do fornecedor *, com o cursor no campo do
fornecedor. Informado, a tela procura o cadastro do fornecedor e, não encontrando — ou encontrando o registro
marcado como excluído —, recusa com * Fornecedor nao cadastrado *, no mesmo campo. Encontrado, o nome do fornecedor
passa a ser mostrado no cabeçalho da tela. Na alteração quem responde por um fornecedor ausente é outra conferência,
a da consulta anterior (RN-07).

### RN-05 — O fornecedor tem de ter nota fiscal

Se o fornecedor existe mas não tem nenhuma nota fiscal registrada naquela coordenadoria, a tela recusa com
* Fornecedor sem notas cadastradas * e não monta lista nenhuma. A recusa vale na abertura da tela e na confirmação.

### RN-06 — A tela lista as notas fiscais do fornecedor e o valor somado

A tela mostra as notas fiscais do fornecedor em até 12 linhas. Cada linha traz a data de emissão, o número da nota,
o órgão e o seu nome, o valor da nota, o número do processo, o tipo de contrato e a marca de operação daquela linha.
No cabeçalho ficam o modo de operação, o tipo de órgão, a data do sistema, a coordenadoria, o fornecedor com o seu
nome e a data e o número a partir dos quais a lista é posicionada; no pé, o valor somado de todas as notas do
fornecedor naquela coordenadoria — as 12 linhas e as demais.

[?] O nome do órgão de cada linha sai do órgão da nota; não achando, a tela procura o nome no cadastro dos órgãos
pelo código do órgão, mas só quando um campo de data é anterior a 08/10/2003 — e esse campo, na abertura da tela,
carrega o valor deixado pela última exclusão da sessão, não a data da nota que está sendo mostrada. Se a intenção
era olhar a data da nota exibida, o teste está lendo outra coisa. Pergunta ao site.

### RN-07 — A alteração exige a consulta anterior do mesmo fornecedor

Em alteração, a tela só age sobre um fornecedor que já tenha sido consultado antes: se a coordenadoria e o
fornecedor informados não forem os mesmos da consulta anterior, a recusa é * Consulte antes de atualizar *, com o
cursor no campo do modo. É a consulta que registra sobre qual fornecedor a alteração vai trabalhar.

### RN-08 — A exclusão é marcada linha a linha e exige o número da nota na linha

A exclusão não é um botão da tela: ela é pedida na própria linha. O servidor marca a linha da nota com a operação de
exclusão e confirma. Se a linha marcada não tiver o número da nota, a recusa é * Exclua nota de linha preenchida *,
com o cursor na marca de operação da linha. Antes disso a tela já conferiu se o código de acesso do servidor tem a
permissão de exclusão (RN-16).

[?] A marca de operação da linha só entende a letra da exclusão ("E"); qualquer outro valor é ignorado em silêncio —
não recusa e não avisa, e a exclusão simplesmente não acontece. Em tela irmã do mesmo acervo, um valor inválido nessa
mesma marca é recusado com uma mensagem que ensina os dois valores possíveis, inclusão e exclusão
("* Informe I=INC ou E=EXC *"), e essa mensagem não existe aqui. Se a máscara desta tela deixa digitar outra coisa
nessa coluna, o servidor fica sem saber por que nada foi excluído. Pergunta ao site.

### RN-09 — A exclusão procura a nota pelo fornecedor, número e ano; não a encontrando, não faz nada e não avisa

A nota a excluir é procurada pelo fornecedor, pelo número marcado na linha e pelo ano que consta da data daquela
linha. Não encontrando, a tela não apaga nada, não avisa nada e segue para a linha seguinte — o servidor fica sem
saber que a exclusão não aconteceu.

### RN-10 — A exclusão é recusada quando a nota tem pedido acumulado

Se a nota tiver item preso a um pedido marcado como acumulado, a exclusão não é feita: a recusa é
* Nota de pedido acumulado *, com o cursor na marca de operação da linha, e nada é apagado.

[?] A conferência guarda o resultado do último item com pedido que leu, e não o de todos: pelo que está no fonte, um
item preso a pedido acumulado que não seja o último lido não provoca a recusa. Confirmar com o site se a intenção era
recusar a nota inteira.

### RN-11 — A exclusão apaga a nota fiscal e os seus itens

Passando as conferências, a tela apaga cada item da nota e, em seguida, a própria nota fiscal. O apagamento é
definitivo — não é marca de inativo —, e o que a nota tinha fica preservado apenas no rastro de auditoria (RN-14).

### RN-12 — A exclusão devolve ao contrato a quantidade e o valor do item

Para cada item da nota, a tela procura o contrato daquele material — mesmo tipo de contrato, fornecedor,
coordenadoria, subclasse e gênero —, tomando por limite a data da nota, e devolve ao contrato a quantidade e o valor
do item, reduzindo o que a nota havia consumido. O tipo de contrato com que procura é ajustado conforme o tipo de
órgão da sessão: nas notas de 2004 em diante o tipo gravado é usado como está; nas anteriores, o órgão 01 troca o
tipo 15 por 02, e o órgão 02 troca o tipo 02 por 01. A devolução só acontece quando a nota não é anterior ao início
da vigência do contrato.

[?] A exclusão segue e apaga a nota mesmo quando o contrato não é encontrado ou quando a nota é anterior ao início da
vigência dele; nesse caso a quantidade e o valor do item não voltam ao contrato e ninguém avisa o servidor. Confirmar
se é intencional.

### RN-13 — A exclusão atualiza o item do pedido e o pedido

Para cada item da nota preso a um pedido, a tela reduz a quantidade recebida daquele item no pedido, marca a situação
do item como "A" e registra a matrícula e a data da baixa; e, quando a situação do pedido era "F", passa a do pedido
para "A" também, limpando a marca de manutenção. Se o item da nota não tem pedido, nada disso é feito.

[?] O que as situações "A" e "F" do pedido e do item significam não está no acervo: o fonte testa "F" e grava "A", e
nenhum rótulo, mensagem ou comentário desta jornada traduz essas letras. Pergunta ao site.

### RN-14 — A exclusão deixa rastro de auditoria, menos na atualização do pedido

Cada passo da exclusão grava um registro de auditoria com o conteúdo do cadastro antes e depois da mudança, a tela de
origem, o tipo de operação, a matrícula, a data e a hora da sessão, o terminal e o processo. Para uma nota com itens,
a tela grava: um registro para o contrato (quando o contrato é atualizado), um para o item do pedido (quando ele é
encontrado), um para cada item da nota apagado e um para a nota apagada. A atualização do pedido é o único passo que
não deixa registro.

### RN-15 — A consulta não grava nada

Em consulta a tela lê e soma, e não escreve em cadastro nenhum: nenhum registro é incluído, alterado ou excluído e
nenhum registro de auditoria é criado. É a alteração que escreve, e só com a linha marcada para exclusão.

### RN-16 — Nada acontece sem a conferência de sessão, de tela, de acesso e de operação

Ao abrir e ao confirmar, a tela passa pelas conferências de sessão, de tela, de acesso e de operação: o servidor tem
de estar no terminal em que a sessão foi
aberta — em outro, o acesso é encerrado; a tela tem de estar registrada, senão * Tela nao disponivel *; o código de
acesso do servidor tem de alcançar a tela, senão * Acesso negado para esta matricula *; e cada operação pedida —
alterar e excluir — tem de estar liberada para esse código, senão * Acesso negado para esta operacao *. A rota ainda
confere a tela: uma tela fora do registro é recusada com * Tela nao cadastrada *. Sem passar por tudo, nada é apagado
e nada é atualizado.

[?] A recusa * Operacao nao disponivel * não é alcançada por esta tela: ela se declara de manutenção e só pede
consulta ou alteração, que são as operações que a rota aceita. Pergunta ao site.

### RN-17 — A tela não apresenta a recusa de destino inválido

A recusa de **destino inválido** existe no trecho que a tela executa para gravar a auditoria, e a ficha estrutural da
tela a lista entre as suas mensagens. Esse caminho só roda com o modo de distribuição automática preenchido, e a
própria tela limpa esse campo imediatamente antes de executar o trecho. Pela N031T, portanto, essa mensagem não é
apresentada.

[?] Divergência entre a ficha e o comportamento, a confirmar com quem mantém o grafo.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta e exclusão de notas fiscais de fornecedor

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a coordenadoria regional escolar e o tipo de órgão
    E tenho acesso à tela N031T

  Cenário: A consulta mostra as notas fiscais do fornecedor e o valor somado
    Dado que estou na tela N031T em consulta
    Quando informo a coordenadoria e o fornecedor
    Então vejo as notas fiscais do fornecedor linha a linha, com a data de emissão,
      o número, o órgão e o seu nome, o valor, o processo e o tipo de contrato
    E vejo o nome do fornecedor no cabeçalho
    E vejo o valor somado de todas as notas daquele fornecedor na coordenadoria

  Cenário: A consulta não grava nada
    Dado que consultei as notas fiscais de um fornecedor
    Quando a consulta termina
    Então nenhum cadastro é incluído, alterado ou excluído
    E nenhum registro de auditoria é criado

  Cenário: A tela só aceita consulta e alteração
    Dado que estou na tela N031T
    Quando peço um modo de operação que não é consulta nem alteração
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é apagado e nada é atualizado

  Cenário: A coordenadoria é a da sessão
    Dado que a minha sessão carrega uma coordenadoria regional escolar
    Quando informo outra coordenadoria
    Então vejo "* Usuario sem acesso a outro grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é apagado

  Cenário: A coordenadoria é obrigatória quando a sessão não carrega uma
    Dado que a minha sessão não carrega coordenadoria regional escolar
    Quando confirmo sem informar a coordenadoria
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é apagado

  Cenário: O fornecedor é obrigatório
    Dado que estou na tela N031T em consulta
    Quando confirmo sem informar o fornecedor
    Então vejo "* Informe o codigo do fornecedor *"
    E o cursor fica no campo do fornecedor
    E nada é apagado

  Cenário: Fornecedor não cadastrado é recusado
    Dado que estou na tela N031T em consulta
    Quando informo um fornecedor que não está cadastrado
    Então vejo "* Fornecedor nao cadastrado *"
    E o cursor fica no campo do fornecedor
    E nada é apagado

  Cenário: Fornecedor sem notas é recusado
    Dado que o fornecedor não tem nenhuma nota fiscal registrada na coordenadoria
    Quando confirmo a consulta
    Então vejo "* Fornecedor sem notas cadastradas *"
    E nenhuma lista de notas é montada

  Cenário: A alteração exige a consulta anterior do mesmo fornecedor
    Dado que estou na tela N031T em alteração
    E que não consultei esse fornecedor antes
    Quando confirmo
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo do modo
    E nada é apagado

  Cenário: A linha marcada tem de ter o número da nota
    Dado que estou na tela N031T em alteração e já consultei o fornecedor
    Quando marco a exclusão numa linha sem o número da nota e confirmo
    Então vejo "* Exclua nota de linha preenchida *"
    E o cursor fica na marca de operação da linha
    E nada é apagado

  Cenário: A marca que não é a da exclusão é ignorada em silêncio
    Dado que estou na tela N031T em alteração e já consultei o fornecedor
    Quando marco uma linha com outra operação que não é a letra da exclusão
    Então nenhuma nota é apagada
    E nenhuma mensagem me é apresentada

  Cenário: A nota que não é encontrada não é excluída e nada é avisado
    Dado que estou na tela N031T em alteração e já consultei o fornecedor
    Quando marco a exclusão numa linha cuja nota o sistema não encontra
      pelo fornecedor, número e ano
    Então nenhuma nota é apagada
    E nenhuma mensagem me é apresentada

  Cenário: A nota com pedido acumulado não é excluída
    Dado que estou na tela N031T em alteração e já consultei o fornecedor
    E que a nota marcada tem item preso a um pedido acumulado
    Quando confirmo a exclusão
    Então vejo "* Nota de pedido acumulado *"
    E o cursor fica na marca de operação da linha
    E nada é apagado

  Cenário: A exclusão apaga a nota fiscal e os seus itens
    Dado que estou na tela N031T em alteração e já consultei o fornecedor
    Quando marco a exclusão na linha da nota e confirmo
    Então cada item daquela nota é apagado
    E a própria nota fiscal é apagada em definitivo

  Cenário: A exclusão devolve quantidade e valor ao contrato
    Dado que estou na tela N031T em alteração e já consultei o fornecedor
    E que a nota marcada tem item de um contrato vigente na data dela
    Quando confirmo a exclusão
    Então a quantidade do item volta ao contrato
    E o valor do item volta ao contrato

  Cenário: O contrato fora da vigência não é tocado e a nota é apagada mesmo assim
    Dado que estou na tela N031T em alteração e já consultei o fornecedor
    E que o contrato do item não é encontrado ou a nota é anterior ao início dele
    Quando confirmo a exclusão
    Então o contrato não é atualizado
    E a nota e os seus itens são apagados do mesmo jeito
    E o servidor não é avisado de que o contrato não foi creditado

  Cenário: A exclusão atualiza o item do pedido e o pedido
    Dado que estou na tela N031T em alteração e já consultei o fornecedor
    E que o item da nota está preso a um pedido
    Quando confirmo a exclusão
    Então a quantidade recebida daquele item no pedido é reduzida
    E a situação do item do pedido passa a "A", com a matrícula e a data da baixa
    E, se a situação do pedido era "F", ela passa a "A"

  Cenário: Nada é excluído sem a conferência de sessão, de tela, de acesso e de operação
    Dado que estou na tela N031T
    Quando a conferência do terminal, do registro da tela, do código de acesso,
      da permissão de alterar, da permissão de excluir ou do registro da rota não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *",
      "* Acesso negado para esta operacao *" ou "* Tela nao cadastrada *"
    E nada é apagado e nada é atualizado
    E, se o terminal não for o da sessão, o acesso é encerrado

  Cenário: A exclusão deixa rastro de auditoria nos seus passos
    Dado que confirmei a exclusão de uma nota com itens
    Quando a tela atualiza o contrato, o item do pedido, cada item da nota e a nota
    Então cada um desses passos deixa um registro de auditoria com o conteúdo
      do cadastro antes e depois, a tela de origem, a operação, a matrícula,
      a data e a hora da sessão, o terminal e o processo

  Cenário: A atualização do pedido não deixa auditoria
    Dado que confirmei a exclusão de uma nota com item de pedido
    Quando a tela atualiza o pedido
    Então nenhum registro de auditoria é gravado para essa atualização
    E os demais passos da exclusão deixam o seu registro

  Cenário: A recusa de destino inválido não é apresentada
    Dado que estou na tela N031T em alteração e excluí uma nota
    Quando a tela grava o registro de auditoria
    Então a tela limpa o modo de distribuição automática
    E a recusa de destino inválido não é apresentada
```
