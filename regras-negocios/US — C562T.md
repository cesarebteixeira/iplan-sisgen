# US — C562T — Transferir quantidade e valor do gênero em uso para o gênero novo da permissão de fornecimento

## Estória

Como **servidor de CRE que responde pela execução da permissão de fornecimento**, quero
**passar para o gênero novo a quantidade e o valor que ainda cabem no gênero em uso**, para
que **o item autorizado possa ser entregue e pago na especificação nova sem perder o saldo que
já estava autorizado, e a permissão deixe de autorizar o que saiu**.

A permissão de fornecimento é o que autoriza um fornecedor, dentro de um contrato de uma
coordenação regional escolar, de um grupo de licitação e de um período, a entregar uma
quantidade de um item — uma classe, uma subclasse e um gênero — por um valor. Quando a
especificação do item em uso muda, o saldo que ainda resta naquele gênero tem de mudar de mãos:
o gênero em uso cede, o gênero novo recebe, e a permissão passa a medir o item pela
especificação nova. Sem isso, o saldo ficaria preso a um gênero que já não se fornece, e o
gênero novo não teria permissão para ser pedido.

A troca não sai de uma vez. Consultar apura o que ainda pode ser transferido e registra esse
apurado no registro da troca daquele item; confirmar regrava o registro com a quantidade
informada; e só a confirmação seguinte, com a estação mandando a marca de confirmação, aplica
a troca à permissão — que então apaga o registro da troca. A tela atende apenas às permissões
de agricultura familiar, e a operação passa pela conferência do perfil de quem opera.

## Contexto

Jornada S000M → C000M → C050M → C060M → C562T.

Ator: servidor de CRE — transfere o saldo do gênero em uso para o gênero novo do item de uma
permissão da sua coordenação regional escolar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Esta tela é aberta por um menu, e não encadeada por outra tela que lhe passe registro e
operação: o menu apenas a abre. Nada nela compara a tela de origem, e é a própria tela que
decide o modo com que trabalha (RN-08). O que ela usa do que veio antes é o **tipo de órgão da
secretaria** escolhida no LOGON — ele entra na identificação de tudo o que a tela lê e grava, e
a tela não deixa digitá-lo —, além da **matrícula**, do **código de acesso**, do **privilégio**,
da **coordenação regional** e da **data do sistema** da sessão. Essas são regras da entrada e
estão no anexo de evidências, em **Regras que se revelaram da entrada**.

A jornada termina nesta tela: ela não encaminha para nenhuma outra — o que ela faz, ao fim da
consulta e da alteração, é se reapresentar com o resultado.

---

## Regras de negócio

### RN-01 — A tela transfere quantidade e valor do gênero em uso para o gênero novo do item

A tela trata de **um item** de uma permissão por vez, e mostra os dois gêneros que o compõem: o
gênero que está autorizado — o **gênero em uso** — e aquele pelo qual o item deve passar a ser
fornecido — o **gênero novo**. A operação é uma cessão dentro do mesmo item: a quantidade sai
do gênero em uso e entra no gênero novo.

O que se cede é a **quantidade** informada pelo servidor; o valor correspondente a tela calcula,
multiplicando essa quantidade pelo preço unitário do gênero novo. Do lado do gênero em uso, o
valor cedido é descontado e a quantidade que resta é recalculada pelo preço unitário dele —
faixa por faixa: a inicial, a do aditivo e a da prorrogação. A tela não é uma grade: ela mostra
um item contra o outro, em um único conjunto de campos.

### RN-02 — A permissão e os dois gêneros são identificados pela coordenação regional, pelo contrato, pelo grupo de licitação, pelo período limite e pelos códigos dos gêneros

Para chegar ao item, o servidor informa a **coordenação regional escolar**, o **tipo de
contrato**, o **grupo de licitação**, o dia, o mês e o ano do **período limite** e os **três
códigos do gênero em uso** — classe, subclasse e gênero —, e mais os **três códigos do gênero
novo**. É essa combinação que localiza o registro da troca daquele item e a permissão do gênero
em uso; a permissão do gênero novo é procurada com os códigos dele no lugar dos do gênero em
uso.

O **tipo de órgão** não se digita: é o da secretaria que o vínculo da matrícula escolheu na
entrada e ficou na sessão. O fornecedor, a razão social, o tipo de licitação, o início do
período, as datas-base, o valor homologado e o valor adjudicado aparecem na tela, mas **não
identificam** nada: não fazem parte da conferência de "o mesmo registro" (RN-09).

### RN-03 — A consulta apura o máximo transferível e registra o apurado no registro da troca

Consultar não é só olhar. A consulta apura, faixa por faixa — a inicial, a do aditivo e a da
prorrogação —, a **quantidade máxima que ainda pode ser transferida** para o gênero novo: parte
do valor já comprado e dos valores da permissão do gênero em uso e converte o que apura em
quantidade pelo **preço unitário do gênero novo**.

Esse apurado é **gravado no registro da troca daquele item** — criando-o se ainda não existir,
já com o gênero novo informado e com o saldo que resta do gênero em uso —, e a gravação deixa
rastro na auditoria. Consultar de novo o mesmo registro, sem mudar nada, não repete o cálculo
nem a gravação: a tela só reapresenta o registro.

[?] A apuração subtrai o valor inicial do valor já comprado — e não o contrário. Se essa
subtração conservar o sinal, o máximo transferível sai negativo justamente quando ainda há saldo
para transferir, e toda quantidade informada seria recusada como acima do máximo disponível; se
o resultado negativo for gravado sem sinal, o que sai é o saldo livre e a regra é a que está
escrita. O que o acervo diz é apenas a ordem da operação, não o que acontece com o resultado
negativo. Pergunta ao site.

### RN-04 — Consultar um registro diferente do último consultado refaz o registro da troca daquele item

Quando o que foi informado não é o mesmo registro que a última consulta deixou guardado, a
consulta, antes de gravar, percorre os registros da troca daquele item e **apaga aqueles que têm
o gênero novo informado**; a gravação seguinte cria o registro de novo, com o apurado da
consulta. O que estava registrado para **outro** gênero novo permanece.

É a consulta que guarda o registro que a alteração vai aplicar (RN-12). Consultar de novo o
mesmo registro, sem mudar nada, não apaga nem grava.

### RN-05 — A permissão precisa existir, ser de agricultura familiar e ter a tela liberada para o tipo de licitação dela

Antes de qualquer coisa, a tela procura a **permissão** do gênero em uso. Não achando, recusa
com **\* Permissao nao cadastrada \*** e devolve o cursor à coordenação regional. Achando, exige
que a licitação daquela permissão seja a de **agricultura familiar** — senão recusa com
**\* Permissao nao e de agricultura familiar \*** — e que a **tela esteja liberada para o tipo
de licitação** daquela permissão — senão recusa com
**\* Tela nao disponivel para esta licitacao \***, também com o cursor na coordenação regional.

### RN-06 — Os dois gêneros precisam existir, ser do mesmo grupamento e ter preço

O gênero em uso, quando a **classe** dele não é informada, é recusado com
**\* Informe o genero - DE \***. O gênero novo, quando a **classe** dele não é informada, é
recusado com **\* Informe o genero - PARA \*** — as duas mensagens falam em gênero, mas a
conferência olha a classe.

O gênero novo é procurado no cadastro de gêneros: não existindo, a recusa é
**\* Genero nao cadastrado - PARA \***; existindo mas pertencendo a **outro grupamento** que o
da permissão, a recusa é **\<- Genero de outro grupamento - PARA \***. E o gênero novo ainda
precisa ter **preço**: a tela procura o preço na tabela quinzenal do tipo de contrato — a normal
ou a especial, conforme a configuração do contrato — e, não achando, recusa com
**\* Genero sem preco na tabela - PARA \***. Todas essas recusas devolvem o cursor ao gênero
novo, e nada é gravado.

[?] O gênero novo não tem nome de negócio no material: os três campos dele aparecem na tela
pelos nomes internos dos campos. Se o "PARA" é o gênero novo, o gênero de destino ou outra
coisa, o acervo não diz. Pergunta ao site.

### RN-07 — A quantidade do gênero em uso precisa ter saldo

A tela soma a quantidade permitida do gênero em uso — a inicial, a do aditivo e a da
prorrogação — e compara com o que **já foi pedido** daquele item. Se o que já foi pedido alcança
tudo o que a permissão permite, a recusa é **\* Quantidade nao disponivel - DE \***, com o
cursor no gênero em uso.

[?] O que a comparação trata como "já pedido" vem do nome do campo; nenhum rótulo de negócio
diz se ele conta o que foi pedido, o que foi entregue ou o que foi comprado. Pergunta ao site.

### RN-08 — A tela só atende alteração, exclusão e consulta, e abre na operação da última vez

Aberta pela primeira vez desde que o programa foi carregado, a tela assume a **consulta**.
Depois disso, ela abre na operação da última vez em que foi usada naquela estação — alteração,
exclusão ou consulta. Qualquer outra operação é recusada com
**\* Opcao nao disponivel. Use ALT, DEL ou CON \***, e o cursor volta ao campo da operação.

[?] A correspondência entre os rótulos que o servidor lê (ALT, DEL, CON) e as operações que o
programa reconhece é conclusão tirada do texto da mensagem, não verificada no material.
Pergunta ao site.

### RN-09 — Alterar e excluir exigem que a consulta tenha deixado o mesmo registro

Alteração e exclusão só seguem quando a **coordenação regional**, o **tipo de contrato**, o
**grupo de licitação**, o **período limite**, a **subclasse** e o **gênero do item em uso** e a
**subclasse** e o **gênero do gênero novo** são exatamente os que a consulta deixou guardados;
mudando qualquer um deles, a recusa é **\* Consulte antes para atualizar \***, com o cursor no
campo da operação. As duas operações exigem ainda que o registro da troca daquele item exista
(RN-11).

[?] A conferência de "o mesmo registro" **não inclui a classe**, nem a do gênero em uso nem a do
gênero novo, embora a classe faça parte da identificação da permissão e do registro da troca.
Trocar só a classe não obriga a consultar de novo — e, nesse caso, a tela segue pelo atalho do
registro já consultado. Se isso é proposital ou falta, pergunta ao site.

### RN-10 — A alteração confere a quantidade informada para o gênero novo

Na alteração, a quantidade do gênero novo é obrigatória: se as três quantidades do gênero novo
— inicial, aditivo e prorrogação — vierem zeradas, a recusa é
**\* Informe a quantidade - PARA \***, com o cursor na quantidade inicial. Informada, cada uma
delas é comparada com o **máximo transferível** daquela faixa, apurado pela consulta; se passar,
a recusa é **\* Quantidade inicial > maximo disponivel - PARA \***,
**\* Quantidade aditivo > maximo disponivel - PARA \*** ou
**\* Quantidade prorrog > maximo disponivel - PARA \***, conforme a faixa, com o cursor na
quantidade correspondente. Nada é gravado em nenhuma dessas recusas.

### RN-11 — A alteração e a exclusão exigem que a troca já esteja registrada

Se, para aquele item, não houver o **registro da troca** com o gênero novo informado, a
alteração e a exclusão são recusadas com **\* Registro nao cadastrado \***, com o cursor no
campo da operação. É a consulta que cria esse registro (RN-03); sem consultar, não há o que
alterar nem o que excluir.

### RN-12 — A alteração grava a quantidade informada e, confirmada de novo, aplica a troca à permissão

Confirmada a alteração com as quantidades informadas, a tela regrava o registro da troca daquele
item com elas — e com o saldo que resta do gênero em uso, recalculado (RN-01) —, sem tocar na
permissão.

A **aplicação** à permissão só acontece numa confirmação seguinte, quando as quantidades
informadas são iguais às que ficaram registradas e a estação manda a **marca de confirmação**.
Então a tela soma o cedido à permissão do gênero novo (RN-14), desconta da permissão do gênero
em uso (RN-13), recalcula os totais da permissão (RN-16), regrava o acumulado do item (RN-15) e
**apaga o registro da troca daquele item**. Os registros são travados antes de serem regravados.

[?] A quantidade e a aplicação não cabem na mesma confirmação: o trecho que registra a
quantidade apaga a marca de confirmação e o trecho que aplica a troca exige essa marca — e a
consulta registra as quantidades do gênero novo zeradas, de modo que a primeira confirmação cai
sempre no ramo da quantidade. A marca de confirmação não é escrita em nenhum ponto deste
programa nem de nenhum outro do acervo: ela só é lida e apagada aqui, e a tela que a enviaria (a
máscara) não está no lote. Sem ela a troca nunca chega à permissão; com ela, chega. Se esse é o
desenho, ou se a aplicação é inalcançável pela tela, pergunta ao site.

### RN-13 — Quando o gênero em uso fica sem quantidade, a permissão dele é excluída

Se, depois da cessão, as três quantidades do gênero em uso no registro da troca ficarem
zeradas, a tela não regrava a permissão dele com quantidade zero: **exclui** o registro daquele
item da permissão, com a operação registrada na auditoria como exclusão. Nos demais casos, a
permissão do gênero em uso é regravada com o saldo que sobrou.

### RN-14 — O gênero novo ganha permissão própria quando ainda não tem, com o preço da tabela quinzenal do contrato

Se a permissão já tem o gênero novo, a tela **soma** o que foi cedido ao que ele já tinha. Se
não tem, a tela **cria** a permissão daquele item: leva o fornecedor, o grupo de licitação, o
período e as datas-base da permissão de origem, o gênero novo nos códigos do item, a quantidade
e o valor cedidos, e o **preço unitário tirado da tabela quinzenal** do tipo de contrato — a
normal ou a especial, conforme a configuração do contrato. A criação da permissão também deixa
rastro na auditoria.

### RN-15 — O acumulado do item é regravado com a quantidade convertida entre as gramaturas

O item também tem um **acumulado**, identificado pelo gênero novo e pelo mesmo contrato e
período. Ao aplicar a troca, a tela converte a quantidade cedida de uma gramatura para a outra
— usando a conversão do gênero em uso e a do gênero novo —, limita o resultado pelo valor
cedido e divide pelo preço do gênero novo, e regrava esse acumulado.

[?] O acumulado só é regravado quando o gênero novo **ainda não tinha** permissão própria; no
caminho em que ele já tinha, a tela soma o que recebeu à permissão dele e não toca no acumulado.
Se o acumulado deveria acompanhar os dois casos, pergunta ao site.

### RN-16 — Os totais da permissão são recalculados como a soma dos itens

Aplicada a troca, a tela recalcula os totais da permissão daquele grupo e período — o valor
adjudicado, o valor do aditivo, o valor da prorrogação e o valor homologado — somando os valores
iniciais dos itens da permissão, e regrava os registros da permissão com esses totais.

[?] A soma começa com os códigos do item zerados e a conferência do laço não compara o item, de
modo que a varredura toma todos os itens da permissão. Se a permissão tem um registro de resumo,
com o item zerado, que seria o único a receber os totais — ou se são todos os itens que os
recebem — o acervo não diz. Pergunta ao site.

### RN-17 — A exclusão apaga o registro da troca e nada mais

Excluir, nesta tela, é **desfazer a troca preparada**: a tela apaga o registro da troca daquele
item e deixa a permissão como estava. Nada mais é apagado, e a permissão do gênero em uso e a do
gênero novo não são tocadas.

### RN-18 — Toda gravação deixa rastro na auditoria

Cada gravação — a criação ou a mudança do registro da troca, a criação, a alteração ou a
exclusão da permissão, e a regravação do acumulado do item — deixa um registro de auditoria com
o cadastro de origem da operação, a operação (inclusão, alteração ou exclusão), o conteúdo
anterior e o posterior, o número do processo — formado pelo tipo de órgão, pela coordenação
regional, pela subclasse e pelo gênero do item —, a matrícula do funcionário, a estação, o ano,
o dia, o mês e a hora da sessão e o tipo de órgão.

### RN-19 — A operação só acontece se o perfil do usuário autorizar

Antes de ler e de gravar, a tela passa pela conferência de acesso à tela e, na passagem da
operação, pela conferência da rota e da operação do perfil: o sistema procura a autorização do
código de acesso para aquela tela e verifica se a operação pretendida está liberada. Não estando,
a operação é abandonada sem gravar. A conferência recebe o contexto da sessão: a matrícula, o
código de acesso, o privilégio, o tipo de órgão e a coordenação regional.

[?] A regra efetiva de permissão por perfil e por operação não está no material: as rotinas são
declaradas em comum e não têm corpo no lote; a tela só confere o retorno. Pergunta ao site.

### RN-20 — O que o gerador declara não é o que a tela executa

A tela enxerga **doze cadastros** e, para cada um deles, o gerador deixa prontas uma operação de
gravar e uma de apagar. Por caminho alcançável, ela **grava quatro**: o registro da troca, a
permissão, o acumulado do item e a auditoria. Os outros oito — as telas, o tipo de órgão, os
gêneros, o tipo de contrato, as duas tabelas de preço, a liberação da tela por tipo de licitação
e os fornecedores — são **só de leitura**: a tela os consulta para montar a tela e para conferir,
e não os altera.

Os números de capacidade do dicionário são de dimensionamento, não volume cadastrado: a
permissão e o registro da troca comportam **1.000.000** de registros cada um; os gêneros e a
tabela normal, **150.000**; o acumulado do item, **100.000**; a auditoria, **60.000.000**; a
tabela especial e os fornecedores, **10.000**; as telas, **2.000**; o tipo de contrato e a
liberação da tela, **1.000** cada; o tipo de órgão, **200**.

---

## Cenários BDD

```gherkin
Funcionalidade: Transferir quantidade e valor do gênero em uso para o gênero novo da permissão de fornecimento

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C562T

  Cenário: Consulta de um item ainda não consultado apura e registra o que pode ser transferido
    Dado que a permissão do item existe e é de agricultura familiar
    E a tela está liberada para o tipo de licitação daquela permissão
    E o gênero novo existe, é do mesmo grupamento e tem preço na tabela quinzenal do contrato
    Quando consulto o item informando o gênero em uso e o gênero novo
    Então vejo o gênero em uso, o gênero novo, o valor já comprado e os totais
    E o máximo que pode ser transferido fica registrado naquele item, faixa por faixa
    E a tela se reapresenta com o resultado
    E a gravação deixa rastro na auditoria

  Cenário: Consultar de novo o mesmo registro não grava nada
    Dado que aquele registro já foi consultado
    Quando consulto outra vez o mesmo registro, sem mudar nada
    Então a tela reapresenta o registro da troca
    E nada é gravado

  Cenário: Consultar um registro diferente refaz o registro da troca daquele item
    Dado que aquele item tem registro da troca com o gênero novo que vou informar
    Quando consulto o item mudando a coordenação regional, o contrato, o grupo, o período ou os códigos dos gêneros
    Então o registro da troca daquele item é apagado
    E o registro é gravado de novo com o apurado da consulta
    E o que estava registrado para outro gênero novo permanece

  Cenário: Permissão não cadastrada
    Dado que não existe permissão para o item informado
    Quando consulto o item
    Então vejo a mensagem "* Permissao nao cadastrada *"
    E o cursor volta para a coordenação regional
    E nada é gravado

  Cenário: Permissão que não é de agricultura familiar
    Dado que a permissão do item não é de agricultura familiar
    Quando consulto o item
    Então vejo a mensagem "* Permissao nao e de agricultura familiar *"
    E o cursor volta para a coordenação regional
    E nada é gravado

  Cenário: Tela não liberada para o tipo de licitação
    Dado que a tela não está liberada para o tipo de licitação daquela permissão
    Quando consulto o item
    Então vejo a mensagem "* Tela nao disponivel para esta licitacao *"
    E o cursor volta para a coordenação regional
    E nada é gravado

  Cenário: Gênero em uso não informado
    Quando consulto o item sem informar a classe do gênero em uso
    Então vejo a mensagem "* Informe o genero - DE *"
    E o cursor fica no gênero em uso
    E nada é gravado

  Cenário: Gênero novo não informado
    Quando informo o gênero em uso e deixo a classe do gênero novo em branco
    Então vejo a mensagem "* Informe o genero - PARA *"
    E o cursor fica no gênero novo
    E nada é gravado

  Cenário: Gênero novo não cadastrado
    Dado que o gênero novo informado não existe no cadastro de gêneros
    Quando consulto o item
    Então vejo a mensagem "* Genero nao cadastrado - PARA *"
    E o cursor fica no gênero novo
    E nada é gravado

  Cenário: Gênero novo de outro grupamento
    Dado que o gênero novo informado pertence a outro grupamento que o da permissão
    Quando consulto o item
    Então vejo a mensagem "<- Genero de outro grupamento - PARA *"
    E o cursor fica no gênero novo
    E nada é gravado

  Cenário: Gênero novo sem preço na tabela quinzenal
    Dado que o gênero novo não tem preço na tabela quinzenal do tipo de contrato
    Quando consulto o item
    Então vejo a mensagem "* Genero sem preco na tabela - PARA *"
    E o cursor fica no gênero novo
    E nada é gravado

  Cenário: Quantidade do gênero em uso sem saldo
    Dado que o que já foi pedido daquele item alcança tudo o que a permissão permite
    Quando consulto o item
    Então vejo a mensagem "* Quantidade nao disponivel - DE *"
    E o cursor fica no gênero em uso
    E nada é gravado

  Cenário: Operação não disponível
    Quando envio uma operação diferente de ALT, DEL e CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT, DEL ou CON *"
    E o cursor volta para o campo da operação
    E nada é lido

  Cenário: A tela abre sem operação informada
    Dado que ainda não usei a tela nesta estação
    Quando a tela abre
    Então ela abre em consulta

  Cenário: Alterar sem ter consultado o mesmo registro
    Dado que os códigos na tela não são os que a consulta deixou guardados
    Quando tento alterar
    Então vejo a mensagem "* Consulte antes para atualizar *"
    E o cursor volta para o campo da operação
    E nada é gravado

  Cenário: Excluir sem ter consultado o mesmo registro
    Dado que os códigos na tela não são os que a consulta deixou guardados
    Quando tento excluir
    Então vejo a mensagem "* Consulte antes para atualizar *"
    E o cursor volta para o campo da operação
    E nada é apagado

  Cenário: Alteração sem a quantidade do gênero novo
    Dado que consultei o item
    Quando deixo as três quantidades do gênero novo zeradas e confirmo a alteração
    Então vejo a mensagem "* Informe a quantidade - PARA *"
    E o cursor fica na quantidade inicial do gênero novo
    E nada é gravado

  Cenário: Quantidade inicial acima do máximo disponível
    Dado que consultei o item
    Quando informo, para o gênero novo, quantidade inicial maior que o máximo transferível
    Então vejo a mensagem "* Quantidade inicial > maximo disponivel - PARA *"
    E o cursor fica na quantidade inicial do gênero novo
    E nada é gravado

  Cenário: Quantidade do aditivo acima do máximo disponível
    Dado que consultei o item
    Quando informo, para o gênero novo, quantidade de aditivo maior que o máximo transferível
    Então vejo a mensagem "* Quantidade aditivo > maximo disponivel - PARA *"
    E o cursor fica na quantidade do aditivo
    E nada é gravado

  Cenário: Quantidade da prorrogação acima do máximo disponível
    Dado que consultei o item
    Quando informo, para o gênero novo, quantidade de prorrogação maior que o máximo transferível
    Então vejo a mensagem "* Quantidade prorrog > maximo disponivel - PARA *"
    E o cursor fica na quantidade da prorrogação
    E nada é gravado

  Cenário: Troca não registrada
    Dado que aquele item não tem registro de troca com o gênero novo informado
    Quando tento alterar ou excluir
    Então vejo a mensagem "* Registro nao cadastrado *"
    E o cursor volta para o campo da operação
    E nada é gravado

  Cenário: A primeira confirmação da alteração registra a quantidade informada
    Dado que consultei o item e o registro da troca tem as quantidades do gênero novo zeradas
    Quando confirmo a alteração com a quantidade que quero transferir
    Então o registro da troca fica com essa quantidade e com o saldo que resta do gênero em uso
    E a permissão do gênero em uso e a do gênero novo não são tocadas
    E a gravação deixa rastro na auditoria

  Cenário: A confirmação seguinte aplica a troca à permissão
    Dado que o registro da troca já tem a quantidade que a alteração registrou
    E a estação manda a marca de confirmação
    Quando confirmo a alteração
    Então o gênero novo fica com o que já tinha mais o que recebeu
    E o gênero em uso fica com o saldo que sobrou
    E o registro da troca daquele item é apagado
    E as gravações deixam rastro na auditoria

  Cenário: O gênero em uso fica sem quantidade
    Dado que a cessão zera as três quantidades do gênero em uso
    Quando confirmo a alteração com a marca de confirmação
    Então a permissão daquele item do gênero em uso é excluída
    E a exclusão fica registrada na auditoria

  Cenário: O gênero novo ganha permissão própria
    Dado que a permissão não tem o gênero novo
    Quando confirmo a alteração com a marca de confirmação
    Então o sistema cria a permissão daquele item, com o preço da tabela quinzenal do contrato
    E regrava o acumulado do item com a quantidade convertida entre as gramaturas
    E a criação fica registrada na auditoria

  Cenário: Os totais da permissão são recalculados
    Dado que confirmei a alteração com a marca de confirmação
    Então os totais da permissão passam a ser a soma dos valores iniciais dos itens
    E os registros da permissão são regravados com esses totais

  Cenário: Exclusão apaga a troca preparada
    Dado que existe o registro da troca daquele item
    Quando confirmo a exclusão
    Então o registro da troca é apagado
    E a permissão do gênero em uso e a do gênero novo ficam como estavam
    E a exclusão deixa rastro na auditoria

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não tem a operação pretendida liberada para a tela
    Quando tento alterar ou excluir
    Então o sistema recusa a operação com mensagem
    E a tela é abandonada sem gravar

  Cenário: Os cadastros que a tela só lê não são alterados
    Dado que consultei o item
    Quando a tela termina
    Então os cadastros de telas, tipo de órgão, gêneros, tipo de contrato,
      as duas tabelas de preço, a liberação da tela e os fornecedores
      continuam como estavam
```
