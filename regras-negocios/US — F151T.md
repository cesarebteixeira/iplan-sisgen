# US — F151T — Manter itens de nota fiscal

## Estória

Como **servidor da CRE que lança e confere os itens de uma nota fiscal**, quero
**registrar, corrigir e apagar, item por item, o que a nota recebeu — código de
gênero, unidade, quantidade e valor — e ver o que ainda sobra do valor da nota**,
para que **a nota fique fechada contra os seus itens e o pagamento não saia nem a
mais nem a menos do que foi efetivamente recebido**.

A nota fiscal chega com um valor, e cada item consumido tem o seu próprio valor; é
o conjunto dos itens que explica o total da nota. Esta tela é onde esse conjunto é
mantido: é ela que cadastra o item, corrige a quantidade e o valor, apaga o item
que entrou errado e mostra, a cada resposta, quanto do valor da nota já foi
consumido e quanto ainda resta. Sem ela, a nota existe com um valor que ninguém
consegue abrir — não há por onde dizer o que ela recebeu, nem por onde corrigir um
item lançado a maior, e o valor retido ou deduzido da nota fica sem base para ser
conferido. Quando o último item da nota é apagado, a própria nota deixa de fazer
sentido e é desfeita junto.

## Contexto

Jornada S000M → F000M → F100M → F150C → F151T.
Ator: servidor de CRE — mantém os itens que compõem uma nota fiscal já lançada
(código de gênero, unidade de medida, quantidade e valor do item) e acompanha
quanto do valor da nota já foi consumido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é dado de navegação, não regra de negócio.

A `F151T` **não é um menu**: é a tela de itens de uma nota fiscal, mostra **7 itens
por vez** e grava em três cadastros. Ela recebe de trás o grupo, a instituição
beneficente, o fornecedor, o ano de competência, o número da nota e os valores de
nota, retenção e dedução já escolhidos, e trabalha em cima desse recorte — o
usuário digita o item, não a nota.

Quem a chama decide o que ela pode fazer: ela abre em **consulta** quando vem da
tela de consulta de gêneros por nota, e abre em **inclusão** quando vem da tela de
nota fiscal. É a mesma tela, com o mesmo desenho; muda o que ela deixa gravar.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — Há um caminho até esta tela e ele não é o que a trilha sugere

A tela é alcançada a partir da **tela de consulta de gêneros por nota fiscal**,
que a abre em consulta, e da **tela de nota fiscal**, que a abre em inclusão. A
tela de consulta de notas fiscais por grupo e competência — o passo anterior da
trilha — também tem, no seu programa, o encaminhamento para esta tela, mas o
caminho é **inalcançável**: ele depende de uma marca de situação na linha que
aquela tela nunca preenche na tela de transação, e por isso o encaminhamento nunca
acontece por ali. Quem chega a esta tela chega pela consulta de gêneros ou pela
tela de nota fiscal.

[?] A tela de consulta de notas fiscais por grupo e competência nunca escreve a
marca de situação que o seu próprio encaminhamento exige, de modo que o trecho que
leva desta tela para a F151T não roda. Ou a marca deveria ser preenchida, e o
encaminhamento funciona no site, ou o trecho é resíduo de uma versão anterior.
Como as duas leituras são possíveis com o que o acervo mostra, não se escolheu
nenhuma. Pergunta ao site.

### RN-02 — O modo de gravação vem de quem chamou a tela, não de quem a usa

Ao abrir, a tela assume o modo que a chamadora deixou no seu contexto. Da consulta
de gêneros por nota ela abre em **consulta**; da tela de nota fiscal ela abre em
**inclusão**. A partir da abertura, o que o usuário escreve no campo de opção manda:
ele pode pedir **inclusão**, **alteração** ou **consulta**. Qualquer outro valor no
campo de opção é recusado com **\* Opcao nao disponivel. Use INC, ALT ou CON \***,
com o cursor no próprio campo de opção, e nada é gravado.

[?] O programa da tela de consulta de gêneros por nota fiscal encaminha a nota
para esta tela em inclusão, mesmo quando o usuário estava apenas alterando ou
apagando a nota. Não se conseguiu determinar, pelo acervo, se a intenção é que a
alteração e a exclusão da nota também recomecem a lista de itens por aqui, ou se
o encaminhamento deveria preservar a operação que o usuário pediu. Pergunta ao
site.

### RN-03 — A tela só abre com a nota e a instituição no contexto

Ao abrir, a tela exige que o órgão e o grupo de coordenação regional tenham vindo
preenchidos no contexto de quem a chamou. Faltando qualquer um dos dois, a tela é
abandonada e o usuário é devolvido à **tela de consulta de gêneros por nota
fiscal**, com aviso, sem que nada seja mostrado e sem que nada seja gravado. É
essa também a saída de quem apaga a nota inteira: apagado o último item, a tela
recua para a consulta de onde veio.

### RN-04 — Sem a tela no cadastro de telas e sem o código de acesso, não há tela

Na abertura, a tela consulta o cadastro de telas pela sua própria identificação e
passa pela conferência de acesso; não achando a tela no cadastro, ou não tendo o
código de acesso de quem opera a tela liberada, a tela é abandonada com aviso e
nada é mostrado. A cada resposta a conferência de acesso se repete, sempre com a
descrição da tela e o código de acesso da sessão.

[?] O texto dos avisos de acesso negado e a identificação por que a tela é
conhecida no cadastro de telas não estão no acervo: a tela copia o que leu do
cadastro, e o conteúdo do cadastro de telas não veio no lote. Pergunta ao site.

### RN-05 — O código de gênero tem de existir no cadastro de gêneros

O item é identificado pelo **código de gênero** (o código FNDE). Informado um
código que não existe no cadastro de gêneros, a tela recusa com
**\* Cod.FNDE nao cadastrado \***, com o cursor no campo do código, e o item não
entra. O mesmo acontece na alteração: o item apagado ou alterado tem de existir no
cadastro de gêneros antes de qualquer outra conferência.

### RN-06 — A unidade de medida tem de ser a do código de gênero

A unidade de medida do item tem de estar cadastrada para aquele código de gênero.
Não estando, a recusa é **\* Unid.medida nao cad. para este cod.FNDE \***, com o
cursor no campo da unidade, e o item não entra.

### RN-07 — Quantidade e valor total do item são obrigatórios, e o preço não pode zerar

O item traz **quantidade** e **valor total do item na nota**. Faltando a
quantidade, a recusa é **\* Informe a quantidade \***, com o cursor no campo da
quantidade. Faltando o valor total, a recusa é
**\* Informe o valor total do item na nota \***, com o cursor no campo do valor.
A partir da quantidade e do valor total, a tela calcula o **preço unitário**
dividindo o valor total pela quantidade; se esse preço sair zerado — porque a
quantidade informada é maior do que o valor total —, a recusa é
**\* Preco unitario zerado \***, com o cursor no campo do valor total do item.

### RN-08 — A soma dos itens não pode passar do que sobra na nota

A tela calcula o **disponível da nota** como o valor da nota, mais o valor
deduzido, menos o valor retido, e compara com o que a nota já tem lançado em
itens. Somando os itens da nota um valor maior do que o disponível, a recusa é
**\* Rec.proprios + vl.itens - desc. > vl.nota \***, com o cursor no campo do valor
total do item, e o item não entra nem é alterado.

[?] O aviso fala em "recursos próprios", "valor dos itens" e "desconto", mas os
únicos valores que a tela lê para essa conta são o valor da nota, o valor retido e
o valor deduzido. Não se conseguiu determinar, pelo acervo, se "recursos próprios"
e "desconto" são sinônimos do retido e do deduzido, ou se a conta deveria usar
outros valores que esta tela não lê. Pergunta ao site.

### RN-09 — Um código de gênero não se repete na mesma nota

A nota não aceita o mesmo código de gênero duas vezes. Ao incluir um código que a
nota já tem, a tela soma a quantidade e o valor à linha existente, em lugar de
criar uma segunda linha; e, terminado o lançamento, a linha repetida é desfeita.
Ou seja: o item entra, mas a nota continua com uma linha por código de gênero.

[?] Nesse caso, em que o código de gênero já está na nota, a tela recusa com a
mensagem **\* Cod.FNDE nao cadastrado nesta nota \*** — o texto diz o contrário do
que aconteceu, porque o item foi encontrado. A mesma frase é usada quando o item
realmente não existe na nota. Perguntou-se ao site qual das duas situações a
mensagem deveria descrever; a tela usa a mesma nas duas.

### RN-10 — Alterar e apagar só valem para item que a nota já tem

Para **alterar** ou **apagar**, o item informado tem de existir na nota. Não
existindo, a recusa é **\* Cod.FNDE nao cadastrado nesta nota \***, com o cursor
no campo do código, e nada é alterado nem apagado. A conferência é a mesma nos
dois casos, e é feita antes de qualquer leitura de cadastro.

### RN-11 — A nota sem item nenhum é avisada

Abrindo com o recorte de uma nota que não tem item nenhum cadastrado, a tela
avisa **\* Nota fiscal sem generos cadastrados \*** e não mostra linha alguma. O
aviso é dado na abertura; ele não impede o lançamento do primeiro item.

### RN-12 — A tela mostra 7 itens por vez

A tela preenche **7 linhas** de item por vez — o mesmo número, em todas as
páginas — e a leitura percorre os itens do recorte do começo ao fim. Cada linha
mostra o código de gênero, a descrição do gênero, a unidade de medida, a
quantidade, o preço unitário, o valor total do item e a situação da linha.

A descrição do gênero, que aparece junto do código, vem do cadastro de gêneros,
pelo próprio código da linha.

[?] A tela não mostra em lugar nenhum quantos itens a nota tem ao todo, nem marca
em que página está; e a linha de situação, que ela exibe, não é preenchida por ela.
Se o usuário espera ver o total de itens ou em que página está, essa informação não
está nesta tela. Pergunta ao site.

### RN-13 — Apagado o último item, a nota é desfeita

Quando o **último** item da nota é apagado, a tela apaga também o resumo de
retenção e dedução que a nota tinha, e a própria nota fiscal. Se ainda restar item,
a exclusão derruba apenas aquele item e a tela recomeça a leitura para mostrar a
nota sem ele. Não sobrando item nenhum, a tela deixa de exibir a nota e devolve o
usuário à consulta de gêneros por nota fiscal.

### RN-14 — O que a tela entrega para a tela seguinte

Respondida em **inclusão** ou **alteração**, a tela não é um fim: ela encaminha
para a **tela de nota fiscal** levando consigo o grupo, a instituição beneficente,
o fornecedor, o ano de competência, o número da nota, as datas de emissão e de
entrega da nota, o valor da nota, o valor retido, o valor deduzido e **o total dos
itens da nota já com o item que acabou de ser lançado**. É esse total que a tela
de nota fiscal passa a usar como valor dos itens da nota. Como não há menu no meio,
a tela de nota fiscal abre já em **inclusão**, com os valores recebidos; ela não
reapresenta a escolha de operação.

### RN-15 — Cada item gravado deixa trilha de auditoria

Cada inclusão, alteração ou exclusão de item registra um lançamento de auditoria,
com a tela de origem, a tela que disparou o registro, a matrícula funcional de
quem operou, o órgão, o grupo, o terminal, a data e a hora, o número do processo
(aqui, o número da nota fiscal) e o conteúdo do registro antes e depois da
operação — separadamente para o item e para o resumo de retenção e dedução.
Falhando o registro de auditoria, a gravação é interrompida e nada é gravado.

### RN-16 — A tela confere a data e a competência da nota antes de gravar

A tela lê a competência e a data do sistema antes de gravar e recusa a operação
quando a competência não é um mês válido ou está fora da faixa de competências
aceita, e quando a data do sistema não pode ser lida. Em qualquer desses casos a
gravação é interrompida e um aviso é dado; nada é gravado.

[?] O texto dos avisos de competência e de data do sistema é montado por rotinas
comuns que não estão neste programa nem no lote; o que se conseguiu verificar foi
só a existência da conferência e o efeito dela, que é interromper a gravação.
Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os itens que compõem uma nota fiscal

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F151T

  Cenário: Abrir pela tela de nota fiscal e incluir um item
    Dado que a tela de nota fiscal me encaminhou esta nota, em inclusão
    E o código de gênero informado existe no cadastro de gêneros
    E a unidade de medida é a do código de gênero
    E informei a quantidade e o valor total do item
    Quando confirmo a inclusão
    Então o item fica lançado na nota
    E o total dos itens da nota passa a incluir esse item

  Cenário: Abrir pela consulta de gêneros por nota fiscal
    Dado que a consulta de gêneros por nota fiscal me encaminhou esta nota
    Quando a tela F151T abre
    Então ela abre em consulta
    E ela não grava nada, por mais que eu responda

  Cenário: Opção diferente de inclusão, alteração e consulta
    Dado que abri a tela F151T
    Quando informo no campo de opção algo que não é inclusão, alteração nem consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use INC, ALT ou CON *"
    E o cursor volta ao campo de opção
    E nada é gravado

  Cenário: A nota ou a instituição não vieram no contexto
    Dado que fui encaminhado à tela F151T sem o órgão ou sem o grupo de coordenação regional
    Quando a tela F151T abre
    Então sou devolvido à consulta de gêneros por nota fiscal
    E nada é mostrado
    E nada é gravado

  Cenário: A tela não consta do cadastro de telas
    Dado que a tela F151T não consta do cadastro de telas
    Quando abro a tela F151T
    Então sou avisado de que a tela não está disponível
    E não consigo ver nem lançar itens da nota

  Cenário: Meu código de acesso não tem a tela
    Dado que o meu código de acesso não tem a tela F151T liberada
    Quando abro a tela F151T
    Então sou avisado de que o acesso à tela foi negado
    E não consigo ver nem lançar itens da nota

  Cenário: Incluir item com código de gênero inexistente
    Dado que abri a tela F151T em inclusão
    Quando informo um código de gênero que não existe no cadastro de gêneros
    Então vejo a mensagem "* Cod.FNDE nao cadastrado *"
    E o cursor volta ao campo do código de gênero
    E o item não é lançado

  Cenário: Incluir item com unidade de medida que não é a do gênero
    Dado que abri a tela F151T em inclusão
    E o código de gênero existe no cadastro de gêneros
    Quando informo uma unidade de medida que não está cadastrada para esse código
    Então vejo a mensagem "* Unid.medida nao cad. para este cod.FNDE *"
    E o cursor volta ao campo da unidade de medida
    E o item não é lançado

  Cenário: Incluir item sem quantidade
    Dado que abri a tela F151T em inclusão
    E o código de gênero e a unidade de medida são válidos
    Quando deixo a quantidade em branco
    Então vejo a mensagem "* Informe a quantidade *"
    E o cursor volta ao campo da quantidade
    E o item não é lançado

  Cenário: Incluir item sem valor total
    Dado que abri a tela F151T em inclusão
    E o código de gênero, a unidade de medida e a quantidade são válidos
    Quando deixo o valor total do item em branco
    Então vejo a mensagem "* Informe o valor total do item na nota *"
    E o cursor volta ao campo do valor total do item
    E o item não é lançado

  Cenário: Incluir item cujo preço unitário sai zerado
    Dado que abri a tela F151T em inclusão
    E informei uma quantidade maior do que o valor total do item
    Quando confirmo a inclusão
    Então vejo a mensagem "* Preco unitario zerado *"
    E o cursor volta ao campo do valor total do item
    E o item não é lançado

  Cenário: Item que faz a soma passar do disponível da nota
    Dado que abri a tela F151T em inclusão
    E o valor dos itens da nota somado a este item passa do disponível da nota
    Quando confirmo a inclusão
    Então vejo a mensagem "* Rec.proprios + vl.itens - desc. > vl.nota *"
    E o cursor volta ao campo do valor total do item
    E o item não é lançado

  Cenário: Código de gênero que a nota já tem
    Dado que abri a tela F151T em inclusão
    E a nota já tem um item lançado com aquele código de gênero
    Quando confirmo a inclusão do mesmo código
    Então a quantidade e o valor são somados à linha que a nota já tinha
    E a nota continua com uma única linha para aquele código de gênero
    E vejo a mensagem "* Cod.FNDE nao cadastrado nesta nota *"

  Cenário: Alterar um item que a nota tem
    Dado que abri a tela F151T em alteração
    E a nota tem o item que informei
    Quando informo a nova quantidade e o novo valor total do item
    Então o item é alterado na nota
    E o total dos itens da nota é refeito

  Cenário: Alterar ou apagar item que a nota não tem
    Dado que abri a tela F151T em alteração ou em exclusão
    Quando informo o código de gênero de um item que a nota não tem
    Então vejo a mensagem "* Cod.FNDE nao cadastrado nesta nota *"
    E o cursor volta ao campo do código de gênero
    E nada é alterado nem apagado

  Cenário: Apagar um item, restando outros na nota
    Dado que abri a tela F151T em exclusão
    E a nota tem mais de um item lançado
    Quando confirmo a exclusão de um deles
    Então aquele item sai da nota
    E os demais itens continuam lançados
    E a tela recomeça a leitura mostrando a nota sem ele

  Cenário: Apagar o último item da nota
    Dado que abri a tela F151T em exclusão
    E a nota tem um único item lançado
    Quando confirmo a exclusão desse item
    Então o item sai da nota
    E o resumo de retenção e dedução da nota é apagado
    E a própria nota fiscal é apagada
    E sou devolvido à consulta de gêneros por nota fiscal

  Cenário: A nota não tem item nenhum
    Dado que abri a tela F151T para uma nota sem item cadastrado
    Então vejo a mensagem "* Nota fiscal sem generos cadastrados *"
    E nenhuma linha de item é mostrada

  Cenário: A tela mostra 7 itens por vez
    Dado que a nota tem mais de 7 itens lançados
    Quando abro a tela F151T
    Então vejo 7 itens por vez
    E cada linha mostra o código de gênero, a descrição do gênero, a unidade de medida, a quantidade, o preço unitário, o valor total do item e a situação da linha

  Cenário: A tela encaminha para a tela de nota fiscal
    Dado que abri a tela F151T em inclusão
    E lancei um item
    Quando respondo a tela
    Então sou encaminhado à tela de nota fiscal
    E ela abre em inclusão
    E ela recebe o grupo, a instituição beneficente, o fornecedor, o ano de competência, o número da nota, as datas de emissão e de entrega da nota, o valor da nota, o valor retido, o valor deduzido e o total dos itens já com o item lançado

  Cenário: Cada item gravado deixa trilha de auditoria
    Dado que abri a tela F151T e lancei, alterei ou apaguei um item
    Quando a gravação se completa
    Então fica registrado quem operou, em que tela, em que órgão, grupo e terminal, em que data e hora, com que número de nota, e o conteúdo do item e do resumo de retenção e dedução antes e depois

  Cenário: A competência ou a data do sistema não conferem
    Dado que abri a tela F151T em modo de gravação
    E a competência ou a data do sistema não passam na conferência
    Quando confirmo a operação
    Então vejo um aviso sobre a competência ou sobre a data do sistema
    E nada é gravado
```
