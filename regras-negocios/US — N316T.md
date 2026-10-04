# US — N316T — Pedidos e notas fiscais do operador logístico por tipo de contrato

## Estória

Como **servidor de CRE**, quero **consultar, por tipo de contrato, os pedidos de um
operador logístico com as notas fiscais de cada pedido**, para que **eu enxergue a
carteira daquele operador — o que ele tem para entregar, para qual órgão e com que
notas — sem juntar isso à mão**.

A lista de pedidos que a tela mostra não é digitada por ninguém: ela é montada a
partir dos pedidos que o sistema já tem, e é montada **somente aqui** — nenhum outro
programa do acervo mantém essa lista. Isso tem consequência de negócio: a lista é um
retrato, tirado no momento em que o servidor consulta uma combinação nova; se os
pedidos mudarem depois, o retrato continua o antigo até que alguém consulte outra
combinação. É por isso que esta tela, embora só atenda em consulta, também escreve.

## Contexto

Jornada S000M → N000M → N050M → N300M → N316T.

Ator: servidor de CRE — informa a coordenadoria regional escolar, o tipo de contrato
e o operador logístico, consulta os pedidos daquele operador com as notas fiscais de
cada pedido e, ao consultar uma combinação nova, remonta a lista.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Esta tela não encaminha o servidor a outra tela: a jornada termina nela. Da sessão ela
usa a matrícula funcional, o tipo de órgão e a coordenadoria regional escolar que a
entrada deixou. As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A lista é mantida somente por esta tela, e é de cada servidor

A tela não é um cadastro. Ela consulta dez registros do sistema — o registro de telas,
as coordenadorias regionais escolares, os tipos de contrato, os operadores
logísticos, os órgãos, os fornecedores, as notas fiscais, os pedidos, os itens dos
pedidos e a própria lista — e escreve em **um único**: a **lista de pedidos do
operador logístico**. Nenhum cadastro de negócio é incluído, alterado ou excluído por
ela, e a lista é o único registro que ela escreve, sem deixar rastro de auditoria.

A lista é **de cada servidor**: ela é guardada pela matrícula funcional de quem
consultou, e a lista de um não é a do outro. Como nenhum outro programa do acervo a
escreve nem a lê, é aqui que ela nasce e é aqui que ela é refeita.

[?] Nenhum outro programa do acervo lê ou escreve essa lista, e ela é guardada por
servidor: se ela é a carteira de trabalho do servidor ou apenas uma memória da tela,
o acervo não diz. Pergunta ao site.

### RN-02 — Sete campos são conferidos como número antes de qualquer consulta

A tela trata como número sete campos: a **coordenadoria regional escolar**, o **tipo
de contrato**, o **operador logístico**, o **número do pedido**, o **ano da entrega**
e os **dois campos do par auxiliar** — o número do pedido e o ano da entrega por onde
a leitura continua. O campo em branco vira zero, os zeros à esquerda são descartados,
e o que não for número é recusado **antes** de a tela procurar qualquer cadastro, com
o cursor de volta ao campo.

[?] O rótulo que o servidor lê no campo do operador logístico não está no acervo — o
programa carrega, como rótulo desse campo, o próprio nome técnico dele, e é o único
dos sete sem nome de negócio. Pergunta ao site.

### RN-03 — O que a tela mostra

A lista é apresentada em blocos de até **5 pedidos**. De cada pedido a tela mostra o
**número do pedido**, o **ano da entrega**, a **situação do pedido**, o **órgão**
(código e descrição), o **fornecedor** (código e descrição) e até **7 notas fiscais**.

Fora do bloco ficam os campos que o servidor informa — a **coordenadoria regional
escolar**, o **tipo de contrato**, o **operador logístico** (que aparece pelo nome) e o
**par auxiliar**, com o número do pedido e o ano da entrega por onde a leitura
continua.

[?] O texto exato da máscara — rótulos das colunas, posição e tamanho de cada campo
— não está no acervo. O que se sabe dos rótulos é o que a própria rotina de
conferência carrega, e a ordem dos campos vem do layout do registro. Pergunta ao site.

### RN-04 — A coordenadoria regional escolar é obrigatória e é a da sessão

Ao confirmar, a tela exige a coordenadoria. Quando a sessão carrega uma coordenadoria,
o servidor só pode consultar essa: informar outra é recusado com
**\* Usuario sem acesso a este grupo \***. Quando a sessão não carrega nenhuma,
qualquer coordenadoria informada é aceita — menos em branco, que é recusada com
**\* Informe o grupo \***. Em qualquer dos casos, a coordenadoria informada tem de
existir para o tipo de órgão da sessão: não existindo, a recusa é
**\* Grupo nao cadastrado \***. Nas três recusas o cursor volta ao campo da
coordenadoria, e nada é gravado.

### RN-05 — O tipo de contrato tem de existir para o meu tipo de órgão e ser de operador logístico

O tipo de contrato é obrigatório. Ele tem de estar cadastrado para o tipo de órgão da
sessão — senão **\* Tipo de contrato nao cadastrado \*** — e tem de ser um tipo
marcado como de **operador logístico** — senão **\* TC nao e de operador logistico
\***. As duas recusas devolvem o cursor ao campo do tipo de contrato e não gravam
nada. Em branco, o tipo de contrato vira zero e é procurado como qualquer outro: não
achando o cadastro, a recusa é a mesma.

### RN-06 — O operador logístico tem de estar cadastrado

O operador informado é procurado no cadastro de operadores logísticos; não existindo,
a recusa é **\* Ope.logisitico nao cadastrado \***, com o cursor de volta ao campo do
operador e sem gravar nada. Em branco, o operador vira zero e cai na mesma procura.
Achado o operador, é a **razão social** dele que a tela mostra como nome.

### RN-07 — A tela só atende em consulta

Se a transação chegar em um modo que não seja o de **consulta**, a tela recusa com
**\* Opcao nao disponivel. Use CON \***, com o cursor no campo do modo, e não faz mais
nada. Ao abrir, a própria tela força o modo de consulta: a lista que o servidor vê é
sempre a de uma consulta, e não há caminho nesta tela que inclua, altere ou exclua
cadastro de negócio.

[?] O rótulo do campo do modo e se ele é digitável não estão no acervo — a máscara da
tela não veio no lote. A tela relê o modo do registro de entrada na confirmação, o
que sugere que ele chega preenchido; se existe outra forma de chegar com um modo
diferente, o acervo não diz. Pergunta ao site.

### RN-08 — Confirmar a mesma combinação não revalida nem remonta: só reposiciona a leitura

Se a coordenadoria, o tipo de contrato e o operador forem os mesmos da última
consulta confirmada, a tela **não grava nada e nem reconfere os cadastros**: ela
apenas reposiciona a leitura, começando pelo pedido indicado no par auxiliar (RN-11).
É por aí que o servidor anda dentro da lista sem refazê-la — e é também por isso que
consultar duas vezes a mesma combinação não traz pedido novo para a lista.

### RN-09 — Consultar uma combinação nova apaga a lista daquele servidor e a remonta

Quando algum dos três campos difere do que ficou da última consulta, a tela apaga, um
a um, os pedidos da lista **daquele servidor** e remonta a lista a partir dos **itens
dos pedidos** daquele tipo de contrato, no tipo de órgão e na coordenadoria da sessão.
A ordem é essa — primeiro apaga, depois remonta — e a tela não exige que haja pedido
para remontar: uma combinação sem pedidos deixa a lista do servidor vazia.

Cada pedido que entra na lista leva a **situação do pedido**, o **fornecedor**, o
**órgão** e o **ano de início**. As **notas fiscais não são copiadas** para a lista: a
tela as busca no cadastro de notas fiscais na hora de mostrar.

[?] O trecho que inclui cada pedido na lista traz uma recusa de "destino inválido" que
só dispara com o modo de distribuição automática preenchido — e o próprio trecho que
monta o registro limpa esse campo imediatamente antes de executá-lo. Por esta tela,
portanto, essa recusa não acontece. Se era para acontecer, pergunta ao site.

[?] O cadastro da lista não está no dicionário de dados que veio no lote: sem a
declaração, não se sabe qual é a chave da lista nem se ela admite repetição. O que o
programa mostra é que a leitura e o apagamento percorrem, um a um, os registros
daquele servidor, até não haver mais nenhum. Pergunta ao site.

### RN-10 — Só o pedido que tem ficha entra na lista

A remontagem percorre os itens dos pedidos e, para cada pedido, procura a **ficha do
pedido**. Só quando a ficha existe é que o pedido entra na lista; o pedido cujo item
existe mas cuja ficha não aparece **fica de fora, sem aviso nenhum**.

### RN-11 — O par auxiliar diz por onde a leitura continua

O número do pedido que a tela mostra tem **seis dígitos** e o ano da entrega tem
**quatro**; juntos, os dois formam o código de **dez dígitos** do pedido. É esse
código que o servidor informa no par auxiliar para posicionar a leitura: informando os
dois, a lista passa a começar por aquele pedido; deixando os dois em branco, a
próxima leitura começa do começo da lista. Um só dos dois — ou um pedido que não está
na lista — não posiciona nada.

### RN-12 — Sem pedidos na lista, a tela avisa

Ao abrir, a tela procura na lista um pedido daquela combinação. Não achando nenhum,
ela avisa **\* TC sem pedidos cadastrados \*** e não mostra pedido nenhum — o desfecho
natural de uma combinação que nunca foi remontada ou cuja remontagem não achou pedido.

## Cenários BDD

```gherkin
Funcionalidade: Pedidos e notas fiscais do operador logístico por tipo de contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão e a coordenadoria regional escolar
    E tenho acesso à tela N316T

  Cenário: A tela abre na consulta, com a coordenadoria da sessão e a última combinação
    Dado que escolhi a N316T no menu N300M
    Quando a tela abre
    Então o campo da coordenadoria já vem com a coordenadoria da minha sessão
    E o tipo de contrato e o operador logístico já vêm com os da última consulta
    E o modo já vem como consulta
    E essa abertura não grava nada

  Cenário: A lista é apresentada em blocos de até cinco pedidos, com as notas de cada um
    Dado que existe lista montada para a combinação informada
    Quando a tela abre
    Então vejo até 5 pedidos
    E de cada pedido vejo o número, o ano da entrega, a situação, o órgão, o
      fornecedor e até 7 notas fiscais

  Cenário: O único registro que a tela escreve é a lista, e sem rastro de auditoria
    Dado que consultei uma combinação na tela N316T
    Quando a consulta termina
    Então nenhum cadastro de negócio foi incluído, alterado ou excluído
    E o único registro escrito é a lista de pedidos daquele servidor
    E nenhum registro de auditoria saiu desta tela

  Cenário: A lista é de cada servidor
    Dado que dois servidores consultam a mesma combinação
    Quando cada um abre a tela N316T
    Então cada um vê a lista que a sua própria consulta montou

  Cenário: Campo não numérico é recusado antes de qualquer consulta
    Dado que digitei letras em um dos campos numéricos da tela
    Quando confirmo
    Então a tela recusa o campo antes de procurar qualquer cadastro
    E o cursor volta para o campo

  Cenário: Coordenadoria não informada
    Dado que a minha sessão não carrega coordenadoria
    Quando confirmo sem informar a coordenadoria
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Coordenadoria de outro grupo
    Dado que a minha sessão carrega uma coordenadoria
    Quando informo outra coordenadoria
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Coordenadoria não cadastrada
    Dado que informei uma coordenadoria que não existe para o tipo de órgão da minha sessão
    Quando confirmo
    Então vejo "* Grupo nao cadastrado *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Tipo de contrato não cadastrado
    Dado que informei um tipo de contrato que não existe para o tipo de órgão da minha sessão
    Quando confirmo
    Então vejo "* Tipo de contrato nao cadastrado *"
    E o cursor fica no campo do tipo de contrato
    E nada é gravado

  Cenário: Tipo de contrato que não é de operador logístico
    Dado que informei um tipo de contrato não marcado como de operador logístico
    Quando confirmo
    Então vejo "* TC nao e de operador logistico *"
    E o cursor fica no campo do tipo de contrato
    E nada é gravado

  Cenário: Operador logístico não cadastrado
    Dado que informei um operador logístico que não está cadastrado
    Quando confirmo
    Então vejo "* Ope.logisitico nao cadastrado *"
    E o cursor fica no campo do operador
    E nada é gravado

  Cenário: Modo diferente de consulta
    Dado que a transação chega à N316T em modo de inclusão, alteração ou exclusão
    Quando confirmo
    Então vejo "* Opcao nao disponivel. Use CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: Confirmar a mesma combinação não revalida nem remonta
    Dado que a coordenadoria, o tipo de contrato e o operador são os mesmos da última consulta
    Quando confirmo
    Então nenhum pedido é apagado e nenhum é remontado
    E nem os cadastros são reconferidos
    E a leitura apenas se reposiciona

  Cenário: Consultar uma combinação nova apaga a lista do servidor e a remonta
    Dado que a lista daquele servidor tem pedidos de uma consulta anterior
    Quando informo uma coordenadoria, um tipo de contrato e um operador diferentes dos últimos
    Então os pedidos da lista daquele servidor são apagados
    E a lista é remontada a partir dos itens dos pedidos daquele tipo de contrato

  Cenário: Consultar uma combinação nova sem pedidos deixa a lista vazia
    Dado que a lista daquele servidor tem pedidos de uma consulta anterior
    Quando confirmo uma combinação nova que não tem pedido nenhum
    Então a lista daquele servidor é apagada
    E nada é remontado

  Cenário: Pedido sem ficha fica de fora da lista
    Dado que existe um item de pedido daquele tipo de contrato
    E que a ficha daquele pedido não existe
    Quando a lista é remontada
    Então aquele pedido não entra na lista
    E nenhum aviso é dado

  Cenário: As notas fiscais não entram na lista
    Dado que um pedido entrou na lista
    Quando a lista é remontada
    Então as notas fiscais daquele pedido não são copiadas para a lista
    E elas são buscadas no cadastro de notas fiscais quando a lista é mostrada

  Cenário: O par auxiliar posiciona a leitura
    Dado que informei no par auxiliar o número do pedido e o ano da entrega de um pedido da lista
    Quando confirmo
    Então a próxima leitura começa por aquele pedido

  Cenário: O par auxiliar em branco faz a lista voltar ao começo
    Dado que deixei o par auxiliar em branco
    Quando confirmo
    Então a próxima leitura começa do começo da lista

  Cenário: Sem pedidos na lista, a tela avisa
    Dado que a lista daquela combinação está vazia
    Quando a tela abre
    Então vejo "* TC sem pedidos cadastrados *"
    E nenhum pedido é mostrado
    E nada é gravado
```
