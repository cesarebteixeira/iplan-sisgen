# US — C802C — Consultar gêneros e abrir a ficha

## Estória

Como **servidor da CRE que consulta o cadastro de gêneros da sua secretaria**, quero **procurar os
gêneros registrados pela subclasse e pelo código e abrir a ficha do gênero escolhido**, para que
**eu confira o que está cadastrado — a descrição, a unidade de medida e o resto da ficha — sem ter
de decorar o código do gênero**.

O gênero só existe dentro de uma subclasse, e o código dele não diz nada a quem não o decorou: quem
reconhece o gênero é a descrição. Esta tela é o índice do cadastro — ela lista os gêneros
registrados, cada um com a subclasse, o código, a descrição resumida e a unidade de medida, e deixa
escolher um deles para abrir a ficha. Sem essa lista, a conferência do cadastro vira tentativa por
código, e quem não decora o número não chega ao gênero. Nada aqui é gravado: quem mantém o gênero é
a tela que esta abre.

## Contexto

Jornada S000M → C000M → C800M → C802C.

Ator: servidor de CRE — folheia a lista dos gêneros registrados e escolhe um deles para ver a ficha
em consulta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio. Os dois menus do caminho (`C000M`, na opção 9, e `C800M`, na opção 5) não gravam
nada: só encaminham.

A tela recebe da sessão o **tipo de órgão (a secretaria)**, a **coordenação regional escolar**, a
**matrícula**, o **privilégio** e a **estação**; o **órgão filho do servidor** não limita esta tela
— o alcance aqui é o cadastro de gêneros, que não pertence a órgão. A **data do sistema** e o
**nome do órgão** que ela exibe também vêm da sessão. Essa carga é regra da entrada e está no
anexo, em **Regras que se revelaram da entrada**.

O que esta tela faz é uma passagem: escolhido um gênero na lista, ela **passa o registro e a
operação para a tela do gênero (`C802T`)**, que é quem mostra a ficha (RN-11). É por isso que a
jornada termina aqui — a tela desta jornada é o índice, e a ficha é da seguinte.

## Regras de negócio

### RN-01 — A tela consulta o cadastro de gêneros e lista o que está registrado

Esta é uma tela de **consulta**. Ela lê o cadastro de gêneros e mostra, **de cada gênero**, quatro
dados: o **código da subclasse**, o **código do gênero**, a **descrição resumida do gênero** e a
**unidade de medida**. No alto ela mostra o **nome do órgão** da sessão e a **data do sistema**.

Nada nesta tela é gravado: nem cadastro, nem travamento de registro, nem linha de auditoria. A tela
não inclui, não altera e não exclui gênero nenhum.

### RN-02 — A lista cabe em quinze posições e segue a ordem da subclasse e do gênero

A lista é lida na ordem do **código da subclasse** e, dentro dela, do **código do gênero** — a
ordem da chave do cadastro, que não admite dois gêneros com a mesma subclasse e o mesmo código.

A tela trabalha com **quinze posições** de gênero: ela lê uma posição de cada vez e avança na ordem
até a última posição da página. A capacidade declarada do cadastro é de **cem mil** gêneros —
parâmetro de dimensionamento, não o volume existente.

### RN-03 — A lista continua de onde a consulta anterior parou, e volta ao começo no fim do cadastro

A leitura não começa sempre no primeiro gênero: o **ponto de partida** é a subclasse e o gênero da
**última posição lida**, guardados na sessão. Sem leitura anterior, o ponto de partida é o começo
do cadastro.

Quando a página termina porque o cadastro acabou — a leitura não achou a posição seguinte —, o
ponto de partida é **apagado**, e a consulta seguinte recomeça do primeiro gênero.

Não há campo de ponto de partida nem comando de página: quem continua a leitura é a própria sessão.

[?] A tela não oferece busca por código: o que se vê é a página de quinze gêneros a partir de onde a
leitura parou. O material lido não mostra como o servidor pede a continuação — não há campo nem
mensagem para isso —, nem o que acontece quando o gênero procurado está depois da décima quinta
posição. Pergunta ao site.

### RN-04 — Sem gênero cadastrado, a tela avisa

Quando a **primeira posição** da página não traz nenhum gênero, a tela avisa
**\* Nao existem generos cadastrados \*** e não lista nada. O aviso é o da primeira posição da
página: ele não se repete a cada posição vazia.

Quando o aviso sai, o ponto de partida é apagado e o conteúdo exibido é limpo.

### RN-05 — Os códigos da linha passam pela conferência de número antes de qualquer uso

O código da subclasse e o código do gênero da linha percorrida passam por uma conferência de número
**antes** de qualquer uso: o que não for número é recusado no próprio campo, e nada é procurado por
causa disso. O código em branco é tratado como zero.

### RN-06 — Marcada a linha, a ficha daquele gênero é procurada e passa para a tela seguinte

Marcada a linha e informado o código da subclasse, a tela procura o gênero no cadastro pela
**subclasse e pelo gênero daquela linha** e passa o registro adiante.

A passagem leva o **registro do gênero escolhido** — a classe, o gênero, a subclasse, a descrição
resumida, a unidade de medida, o padrão de conversão, a menor quantidade a fracionar, a quantidade
do gênero e a unidade de conversão —, a **operação de consulta** e a **origem** (esta tela). Nada é
gravado nesta passagem.

[?] A linha marcada cujo gênero **não** está no cadastro não é recusada aqui: a tela pede a tela
seguinte do mesmo jeito e leva o registro que estiver na área de leitura. Ou a recusa é da tela
seguinte — que tem a mensagem * Genero nao cadastrado * —, ou o servidor vê ali dados de outro
gênero. O material lido não fecha. Pergunta ao site.

### RN-07 — Linha marcada sem o código da subclasse é recusada

Marcada a linha e **não** informado o código da subclasse (zero), a tela não procura nada: ela avisa
**\* Consulte genero cadastrado \***, devolve o cursor para o campo de marcação da linha e não abre
tela nenhuma. O ponto de partida da leitura fica como estava: a recusa não desloca a lista.

### RN-08 — A tela age numa linha só por passada

Marcadas duas linhas da mesma página, a tela abre a ficha de **uma** — a primeira na ordem da
página. Consumada a passagem para a tela seguinte, as demais posições são ignoradas, mesmo que
também estejam marcadas.

### RN-09 — A consulta exige a tela cadastrada e a autorização da operação

A tela é cadastrada: o cadastro de telas guarda o nome dela e a autorização de cada código de
acesso. Sem esse registro a tela não opera — a conferência responde **\* Tela nao cadastrada \***.

Além disso, a operação é submetida à conferência de permissão do código de acesso do servidor. Sem
o registro de autorização daquela tela para aquele código de acesso, a recusa é
**\* Acesso negado para esta operacao \***.

A conferência de sessão também confere a **estação**: a tela aberta em outra estação que não a da
sessão encerra o acesso.

[?] A operação submetida é a que vem no registro da tela, e o material lido não fecha qual é. A
conferência comum **pula** a conferência por operação quando a operação está preenchida e exige a
permissão de **alteração** quando ela está em branco; a permissão de consulta existe no cadastro de
telas e não é lida em nenhum ponto dessa conferência. Ou a consulta exige a permissão de alteração,
ou não é conferida. Pergunta ao site.

### RN-10 — A falha na leitura do cadastro interrompe a consulta e avisa

Toda leitura desta tela testa o erro do banco. Erro de leitura que não seja "não achado" interrompe
a consulta com a **mensagem de erro do sistema**, e a página não é completada.

### RN-11 — O que a tela entrega à seguinte depende de quem a chamou

A tela registra a **própria origem** na área de trabalho da sessão, junto com o registro escolhido,
e pede a tela do gênero (`C802T`). A tela do gênero **lê esse campo de origem**: é por ele que ela
reconhece que veio desta lista.

A tela também respeita a **tela seguinte** que quem a chamou tiver deixado no registro: se houver
uma indicada, o controle vai para ela e esta tela não faz mais nada.

[?] Em que modo a tela do gênero abre por causa desta passagem — em consulta sobre o gênero
escolhido, ou em inclusão com os campos preenchidos — o material lido não fecha. A tela desta
jornada grava a operação de consulta na área de trabalho da sessão, e a tela do gênero **não lê**
essa área; no registro, a consulta só é gravada na montagem da última posição da página. O trecho da
tela do gênero que reconhece esta origem copia o registro e, logo depois, repõe a operação de
inclusão e valores padrão de subclasse e de classe por cima do que veio. Pergunta ao site.

### RN-12 — A tela não grava, não altera, não exclui e não trava registro

Nenhuma das operações de gravação, de exclusão ou de travamento que o programa carrega é executada
por esta tela. As declarações existem para todos os cadastros que ela enxerga — é assim que o
gerador monta o programa —, mas a tela não as aciona: o travamento de registro aparece apenas
dentro dos caminhos de exclusão, que a tela não percorre. A tela também não deixa linha de
auditoria.

## Cenários BDD

```gherkin
Funcionalidade: Consultar os gêneros cadastrados e abrir a ficha do gênero escolhido

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C802C

  Cenário: RN-01 — consultar os gêneros cadastrados
    Quando confirmo a consulta
    Então vejo o nome do órgão e a data do sistema
    E vejo, de cada gênero, o código da subclasse, o código do gênero, a descrição resumida e a unidade de medida
    E nada é gravado

  Cenário: RN-01 — a consulta não deixa rastro
    Dado que faço uma consulta
    Quando a consulta termina
    Então nenhum registro é travado
    E nenhuma linha nova aparece na trilha de auditoria

  Cenário: RN-02 — a lista segue a ordem da subclasse e do gênero
    Dado que existem gêneros em mais de uma subclasse
    Quando confirmo a consulta
    Então os gêneros aparecem na ordem da subclasse e, dentro dela, do código do gênero
    E a página traz no máximo quinze gêneros

  Cenário: RN-03 — continuar a lista de onde a consulta anterior parou
    Dado que a consulta anterior terminou em uma página cheia
    Quando confirmo a consulta de novo
    Então a lista começa no gênero seguinte ao último lido

  Cenário: RN-03 — chegar ao fim do cadastro volta ao começo
    Dado que a leitura alcançou o fim do cadastro de gêneros
    Quando confirmo a consulta de novo
    Então a lista recomeça do primeiro gênero

  Cenário: RN-04 — nenhum gênero cadastrado
    Quando confirmo a consulta e não há gênero cadastrado
    Então vejo "* Nao existem generos cadastrados *"
    E nenhum gênero é listado

  Cenário: RN-05 — código com texto
    Quando informo texto no código da subclasse ou no código do gênero
    Então o campo é recusado antes de qualquer uso
    E nada é procurado por causa disso

  Cenário: RN-06 — marcar um gênero e abrir a ficha dele
    Dado que a lista mostra os gêneros cadastrados
    E marco a linha de um gênero
    Quando confirmo
    Então o gênero daquela linha é procurado no cadastro
    E a ficha daquele gênero se abre na tela C802T
    E nada é gravado por esta tela

  Cenário: RN-06 — gênero da linha marcada fora do cadastro
    Dado que marco a linha de um gênero que não está no cadastro
    Quando confirmo
    Então esta tela não recusa
    E a tela seguinte é pedida do mesmo jeito

  Cenário: RN-07 — linha marcada sem o código da subclasse
    Dado que marco uma linha sem informar o código da subclasse
    Quando confirmo
    Então vejo "* Consulte genero cadastrado *"
    E o cursor volta para o campo de marcação
    E nenhuma ficha se abre

  Cenário: RN-08 — duas linhas marcadas
    Dado que marco duas linhas da mesma página
    Quando confirmo
    Então a ficha de uma única linha se abre
    E é a da primeira linha marcada na ordem da página

  Cenário: RN-09 — tela não cadastrada
    Dado que o cadastro de telas não reconhece esta tela
    Quando confirmo a consulta
    Então vejo "* Tela nao cadastrada *"
    E a tela não opera

  Cenário: RN-09 — sem autorização para a operação
    Dado que não tenho o registro de autorização desta tela para o meu código de acesso
    Quando confirmo a consulta
    Então vejo "* Acesso negado para esta operacao *"
    E nada é listado

  Cenário: RN-09 — sessão em outra estação
    Dado que a minha sessão não está aberta na estação em que estou
    Quando confirmo a consulta
    Então o acesso é encerrado

  Cenário: RN-10 — falha do banco durante a consulta
    Dado que a leitura do cadastro de gêneros falha no banco
    Quando confirmo a consulta
    Então a operação é interrompida com a mensagem de erro do sistema
    E a página não é completada

  Cenário: RN-11 — a ficha aberta a partir da lista
    Dado que escolho um gênero na lista
    Quando confirmo
    Então a tela do gênero recebe o registro do gênero escolhido
    E reconhece que veio desta lista

  Cenário: RN-12 — a consulta não grava, não exclui e não trava
    Dado que faço uma consulta
    Quando a consulta termina
    Então nenhum gênero é incluído, alterado ou excluído
    E nenhum registro fica travado
```
