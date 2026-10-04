# US — F115T — Manter o cadastro de mantenedoras das instituições beneficentes

## Estória

Como **servidor de CRE**, quero **manter o cadastro das mantenedoras — incluir, alterar e
excluir a razão social e o CNPJ de cada uma**, para que **as instituições beneficentes da
secretaria tenham a entidade mantenedora registrada com o nome e o CNPJ corretos**.

A mantenedora é a entidade a que a instituição beneficente pertence: é por ela que o
restante do sistema encontra quem responde pela instituição. O nome que o cadastro das
instituições beneficentes mostra como nome da mantenedora é este, e é aqui que ele é
corrigido; a mantenedora também pode nascer no próprio cadastro da instituição beneficente,
quando lá o nome dela ainda não existe. É aqui, ainda, que uma mantenedora sem instituição
beneficente ligada a ela deixa de existir. Sem esta manutenção, o nome da mantenedora fica
como veio do cadastro da instituição, e a mantenedora que perdeu a última instituição
beneficente não sai do sistema.

Esta tela **grava**: inclui, altera e exclui mantenedoras e deixa o rastro de cada operação
na auditoria. Só não grava no modo de consulta.

## Contexto

Jornada S000M → F000M → F100M → F115T.

Ator: servidor de CRE — mantém o cadastro das mantenedoras: lista as que existem, inclui as
novas, corrige a razão social das que já existem e exclui as que não têm instituição
beneficente ligada a elas.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. A `F000M` e a `F100M` são menus: não leem
cadastro de negócio nenhum e não deixam dado de negócio para a `F115T`. O contexto que a
tela usa — matrícula, código de acesso, privilégio, tipo de órgão, CRE e a data do sistema —
é o que a entrada deixou na sessão, e a `F115T` apenas o repassa às conferências de acesso.

O cadastro que esta tela mantém é o mesmo que a tela que registra as instituições
beneficentes consulta e chega a alimentar quando a mantenedora ainda não existe. Por isso as
duas telas compartilham as mesmas recusas de CNPJ, descritas em RN-05 e RN-08.

Esta tela **não muda de comportamento conforme a tela que a chamou** — o modo de operação
sai do próprio campo de opção, não de quem a abriu — e **não encadeia em outra**: é o fim da
jornada. Quando ela é acionada com o código de uma próxima tela já preenchido, ela não
confere nem grava nada (RN-03).

## Regras de negócio

### RN-01 — O cadastro de mantenedoras: razão social obrigatória e CNPJ, sete por vez

A tela é a manutenção do cadastro de mantenedoras (o cadastro `F116T`). Cada mantenedora tem
**dois dados**: a **razão social**, de preenchimento obrigatório, e o **CNPJ**, de 14
posições. A tela mostra **sete mantenedoras por vez**, uma por linha, e cada linha tem o
CNPJ, a razão social e a **situação** da linha. O cadastro tem capacidade para **1.000**
registros — capacidade (máximo esperado, parâmetro de dimensionamento), não volume
cadastrado.

O registro da mantenedora não guarda secretaria, CRE nem tipo de órgão, e a lista não é
filtrada por nenhum deles.

[?] Como o cadastro não distingue a CRE nem o tipo de órgão, a mantenedora cadastrada por
uma CRE é a mesma que as outras veem. Se a mantenedora é única para toda a secretaria — e se
duas CREs podem cadastrar a mesma entidade com razões sociais diferentes —, pergunta ao
site.

### RN-02 — A situação de cada linha diz o que fazer com ela

Em cada linha, a **situação** decide a operação: **I** inclui, **A** altera, **E** exclui. A
situação é convertida na operação correspondente antes da conferência de permissão.

A linha **sem CNPJ** não gera operação nenhuma. A linha com situação **diferente de I, A e
E** também é ignorada — e **em silêncio**: a tela não avisa nada, apenas não faz nada com
ela.

[?] A conferência que reconhece a linha sem CNPJ compara o campo do CNPJ com zero, e o CNPJ
é um campo que aceita letras; comparar a zero um campo que pode ter letras é semântica que o
acervo não fixa. Na prática a linha em branco também não tem situação e sai pelo mesmo
caminho — mas isso fecha o caminho pela situação, não pela comparação. Pergunta ao site.

### RN-03 — A tela abre em consulta, e a operação só acontece no modo de alteração

Sem opção informada, a tela assume sozinha a **consulta**. Ela só admite duas opções —
**alteração (ALT)** e **consulta (CON)**; qualquer outra é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da opção, e nada é
conferido nem gravado.

**Só a opção de alteração executa**: no modo de consulta, mesmo que a linha esteja marcada
com I, A ou E, a tela lista e termina — a linha não é conferida nem gravada. O modo escolhido
fica guardado, e é ele que reaparece quando a tela é aberta de novo.

Quando a tela já vem com o **código de uma próxima tela** preenchido, ela também não confere
nem grava nada — nesse caso, nem a opção é conferida.

[?] A mensagem nomeia as opções como **ALT** e **CON**, mas a conferência compara o que foi
digitado com os códigos internos de alteração e de consulta do sistema. O acervo mostra os
códigos, e mostra os rótulos ALT e CON usados para essas mesmas duas situações num relatório
de acessos — mas nenhum fonte do lote mostra quem traduz o que o operador digita no código
conferido. Se não houver tradução, a guarda recusa **toda** opção, inclusive a que a própria
mensagem pede, e a manutenção da tela fica **inalcançável**. Pergunta ao site.

### RN-04 — A tela lista as mantenedoras cadastradas e retoma a lista de onde parou

Ao abrir, a tela preenche as **sete linhas** com as mantenedoras já cadastradas, lidas em
ordem de razão social, e guarda o nome do último registro mostrado. É esse nome que a
leitura seguinte usa como ponto de partida: a página seguinte — e a próxima abertura da tela
— continua a lista a partir dele, em vez de voltar ao começo.

Quando a **primeira linha da página** não encontra registro, a tela avisa
**\* Nao existem mantenedoras cadastradas \*** e esquece o ponto de partida. Quando a página
termina de ser preenchida — o fim da lista foi alcançado —, a tela também esquece o ponto de
partida, e a próxima abertura começa do começo.

[?] O aviso * Nao existem mantenedoras cadastradas * sai quando a primeira linha da página
não encontra registro **a partir do ponto guardado**, e não só quando o cadastro está vazio.
Se, com o cadastro cheio, uma abertura da tela cai depois do último nome, o usuário vê o
mesmo aviso. Se o aviso deveria distinguir um caso do outro, pergunta ao site.

[?] O ponto de partida e o modo escolhido ficam guardados na área da sessão, que sobrevive
de uma operação para a outra e só é zerada no primeiro uso do programa. De quem é essa
memória — do terminal, do servidor ou só da tela — o acervo não diz. E a leitura do cadastro
é feita por uma chave parcial (o começo da razão social), cujo posicionamento depende de
sinalizadores do banco de dados que não estão no corpus lido. Pergunta ao site.

### RN-05 — A inclusão exige CNPJ inédito, CNPJ válido, razão social informada e CNPJ que não seja de instituição beneficente

Incluir uma mantenedora (situação I) passa por quatro conferências, nesta ordem:

1. o **CNPJ** não pode pertencer a uma mantenedora já cadastrada — senão
   **\* Mantenedora ja cadastrada \***;
2. o **CNPJ** tem de ter os dígitos verificadores válidos — senão **\* CNPJ invalido \***;
3. a **razão social** tem de estar informada — senão **\* Informe a razao social \***;
4. o **CNPJ** não pode ser o de uma instituição beneficente já registrada — senão
   **<- CNPJ de Instituicao Beneficente \***.

Nas recusas o cursor volta à linha recusada — à coluna da situação, e à coluna da razão
social no caso da razão social em branco — e nada é gravado.

A conferência do CNPJ **aceita letras**: cada letra vale de 17 a 42, e os dígitos verificadores
são calculados sobre esses valores (o CNPJ alfanumérico).

### RN-06 — A inclusão grava a mantenedora e deixa o rastro na auditoria

Passadas as conferências, a inclusão cria o registro no cadastro de mantenedoras com o
**CNPJ** e a **razão social** informados e, em seguida, grava na auditoria (`A010T`) um
registro com a operação de inclusão, o cadastro de origem, a sessão, a CRE, a matrícula, a
estação de trabalho, a data e a hora, o tipo de órgão e as imagens anterior (**vazia**) e
nova (**a mantenedora criada**).

[?] O rastro da inclusão só é gravado se a gravação da mantenedora não tiver deixado um
estado específico no sistema — e nenhum dos programas do acervo lido produz esse estado. Se
ele aparecer, a inclusão grava a mantenedora e **não** grava a auditoria. De onde vem esse
estado, e se a intenção era auditar toda inclusão, pergunta ao site.

[?] O número do processo da auditoria recebe o CNPJ da mantenedora, mas o campo do processo é
numérico e o CNPJ pode ter letras; a rotina da auditoria zera o que não for número. O que
fica gravado no processo quando o CNPJ tem letras não se lê no corpus. Pergunta ao site.

### RN-07 — A alteração exige mantenedora existente e razão social informada, e regrava só a razão social

Alterar (situação A) exige que a mantenedora do CNPJ informado **exista** — senão
**\* Mantenedora nao cadastrada \*** — e que a **razão social** esteja informada — senão
**\* Informe a razao social \***. Passando nas duas conferências, a tela trava o registro e
o regrava com a **nova razão social**, e deixa o rastro na auditoria com as imagens anterior
e nova diferindo apenas na razão social.

O **CNPJ é o que identifica a mantenedora**: a alteração procura pelo CNPJ informado na
linha e não o reescreve. Se o CNPJ da linha for trocado, a alteração passa a valer sobre a
mantenedora daquele CNPJ, e não sobre a que estava na linha antes.

[?] A alteração não confere se a nova razão social já é de outra mantenedora, e o cadastro
admite mais de um registro começando pela mesma razão social. Se duas mantenedoras podem ter
a mesma razão social — e o que isso faz com a lista e com o vínculo das instituições
beneficentes —, pergunta ao site.

### RN-08 — A exclusão exige mantenedora existente e nenhuma instituição beneficente ligada a ela

Excluir (situação E) exige que a mantenedora **exista** — senão
**\* Mantenedora nao cadastrada \*** — e que **não haja instituição beneficente registrada
para ela** — senão **\* Ja existem inst.beneficentes cadastradas \***. Passando nas duas
conferências, a tela trava o registro, grava na auditoria a operação de exclusão com a
imagem anterior preenchida e a nova vazia, e apaga a mantenedora.

A conferência que procura instituição beneficente da mantenedora não lê a chave inteira do
cadastro dessas instituições: ela posiciona a leitura pelo CNPJ da mantenedora com o número
do cadastro da instituição zerado, e só então compara o CNPJ do registro lido com o CNPJ
pedido.

[?] O posicionamento da leitura por chave parcial depende de sinalizadores do banco de dados
que não estão no corpus lido. Se a leitura exigir a chave inteira, nenhuma instituição
beneficente é encontrada com o número zerado e a recusa * Ja existem inst.beneficentes
cadastradas * fica **inalcançável**, de modo que a tela exclui a mantenedora mesmo com
instituição beneficente ligada a ela. Pergunta ao site.

[?] A conferência da inclusão procura o CNPJ da instituição beneficente pela chave inteira e
não compara o registro lido; a da exclusão procura por chave parcial e compara. Se as duas
leituras têm o mesmo alcance, a diferença é de estilo; se não têm, uma das duas decide pelo
registro errado. Pergunta ao site.

### RN-09 — A consulta lista e não grava nada

No modo de consulta a tela lista as mantenedoras e para: nenhuma linha é incluída, alterada
ou excluída, e nenhum registro de auditoria é gerado — mesmo que a linha esteja marcada com
I, A ou E.

### RN-10 — Nenhuma operação acontece sem a conferência de acesso e de permissão

A abertura e cada operação passam pelas conferências comuns do sistema: a tela tem de estar
cadastrada no cadastro de telas — senão **\* Tela nao disponivel \***; o código de acesso da
matrícula tem de ter a tela autorizada — senão **\* Acesso negado para esta matricula \***; e
a operação pretendida tem de constar do perfil da tela — senão
**\* Acesso negado para esta operacao \***.

A conferência de permissão é feita **duas vezes**: uma com a opção digitada (alteração ou
consulta) e outra com a operação da linha (inclusão, alteração ou exclusão). Como só a opção
de alteração executa, **incluir e excluir exigem, além da permissão da própria operação, a
permissão de alteração**: quem tem a permissão de inclusão mas não a de alteração não inclui
por esta tela. A consulta, por sua vez, não exige permissão de consulta — basta a tela estar
autorizada para a matrícula.

[?] O perfil da tela guarda quatro permissões — inclusão, alteração, exclusão e consulta —,
mas a conferência da consulta não lê a de consulta. Quem tem a tela autorizada consulta sem
essa permissão. Se a intenção era exigi-la por tela, o caminho não a exige. Pergunta ao
site.

[?] Se a operação da linha deveria exigir também a permissão de alteração. Como a opção
digitada só pode ser alteração ou consulta, e é ela que a primeira conferência usa, incluir
e excluir passam por duas conferências seguidas. Se quem tem só a permissão de inclusão
deveria poder incluir por esta tela, a guarda da opção o impede. Pergunta ao site.

### RN-11 — A tela mostra a data do sistema e a descrição do tipo de órgão, e as limpa a cada operação

A tela exibe a **data do sistema** e a **descrição do tipo de órgão** da sessão. As duas são
informação de saída — o usuário as vê, mas o terminal não as devolve ao programa —, e cada
operação começa apagando as duas, para que não sobre na tela o que a operação anterior
mostrou.

## Cenários BDD

```gherkin
Funcionalidade: Manter o cadastro de mantenedoras das instituições beneficentes

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F115T

  Cenário: A tela abre em consulta e lista as mantenedoras
    Quando abro a tela
    Então o modo é o de consulta
    E vejo, em até sete linhas, o CNPJ e a razão social das mantenedoras cadastradas

  Cenário: A lista continua de onde parou
    Dado que a tela já mostrou uma página da lista
    Quando abro a tela de novo
    Então a lista continua a partir do último nome que tinha sido mostrado

  Cenário: Não há mantenedora a mostrar
    Dado que a primeira linha da página não encontra mantenedora cadastrada
    Quando abro a tela
    Então vejo a mensagem "* Nao existem mantenedoras cadastradas *"
    E a tela esquece o ponto de partida da lista

  Cenário: Inclusão de uma mantenedora
    Dado que informo um CNPJ que não pertence a nenhuma mantenedora cadastrada
    E informo a razão social
    E marco a linha com a situação I
    Quando peço a alteração
    Então a mantenedora fica cadastrada com aquele CNPJ e aquela razão social
    E a auditoria registra a inclusão com a imagem nova da mantenedora

  Cenário: Inclusão de CNPJ que já é de uma mantenedora
    Dado que o CNPJ informado já pertence a uma mantenedora cadastrada
    Quando marco a linha com a situação I e peço a alteração
    Então vejo a mensagem "* Mantenedora ja cadastrada *"
    E o cursor volta à linha recusada
    E nada é gravado

  Cenário: Inclusão com CNPJ inválido
    Dado que informo um CNPJ cujos dígitos verificadores não fecham
    Quando marco a linha com a situação I e peço a alteração
    Então vejo a mensagem "* CNPJ invalido *"
    E o cursor volta à linha recusada
    E nada é gravado

  Cenário: Inclusão sem a razão social
    Dado que informo um CNPJ inédito e válido
    E deixo a razão social em branco
    Quando marco a linha com a situação I e peço a alteração
    Então vejo a mensagem "* Informe a razao social *"
    E o cursor volta à coluna da razão social da linha recusada
    E nada é gravado

  Cenário: Inclusão com o CNPJ de uma instituição beneficente
    Dado que o CNPJ informado é o de uma instituição beneficente já registrada
    Quando marco a linha com a situação I e peço a alteração
    Então vejo a mensagem "<- CNPJ de Instituicao Beneficente *"
    E o cursor volta à linha recusada
    E nada é gravado

  Cenário: CNPJ com letras
    Dado que informo um CNPJ com letras, com os dígitos verificadores válidos
    Quando marco a linha com a situação I e peço a alteração
    Então a mantenedora é incluída com aquele CNPJ

  Cenário: Alteração da razão social de uma mantenedora
    Dado que informo o CNPJ de uma mantenedora cadastrada
    E informo a nova razão social
    Quando marco a linha com a situação A e peço a alteração
    Então a mantenedora daquele CNPJ fica com a nova razão social
    E a auditoria registra a alteração com o conteúdo anterior e o novo

  Cenário: Alteração de mantenedora que não existe
    Dado que informo um CNPJ que não pertence a nenhuma mantenedora cadastrada
    Quando marco a linha com a situação A e peço a alteração
    Então vejo a mensagem "* Mantenedora nao cadastrada *"
    E o cursor volta à linha recusada
    E nada é gravado

  Cenário: Alteração sem a razão social
    Dado que informo o CNPJ de uma mantenedora cadastrada
    E deixo a razão social em branco
    Quando marco a linha com a situação A e peço a alteração
    Então vejo a mensagem "* Informe a razao social *"
    E o cursor volta à coluna da razão social da linha recusada
    E nada é gravado

  Cenário: Exclusão de uma mantenedora sem instituição beneficente
    Dado que a mantenedora do CNPJ informado não tem instituição beneficente registrada
    Quando marco a linha com a situação E e peço a alteração
    Então a mantenedora daquele CNPJ deixa de existir
    E a auditoria registra a exclusão com o conteúdo anterior da mantenedora

  Cenário: Exclusão de mantenedora que não existe
    Dado que informo um CNPJ que não pertence a nenhuma mantenedora cadastrada
    Quando marco a linha com a situação E e peço a alteração
    Então vejo a mensagem "* Mantenedora nao cadastrada *"
    E o cursor volta à linha recusada
    E nada é apagado

  Cenário: Exclusão de mantenedora com instituição beneficente ligada a ela
    Dado que a mantenedora do CNPJ informado tem instituição beneficente registrada
    Quando marco a linha com a situação E e peço a alteração
    Então vejo a mensagem "* Ja existem inst.beneficentes cadastradas *"
    E o cursor volta à linha recusada
    E a mantenedora continua cadastrada

  Cenário: Linha marcada com uma situação que não existe
    Dado que marco a linha com uma situação diferente de I, de A e de E
    Quando peço a alteração
    Então a tela não avisa nada
    E nada é gravado para aquela linha

  Cenário: Linha em branco
    Dado que deixo o CNPJ da linha em branco
    E não marco a linha com nenhuma situação
    Quando peço a alteração
    Então nada é gravado para aquela linha

  Cenário: A consulta não grava nada
    Dado que localizei mantenedoras pela consulta
    E que marco uma linha com a situação I, A ou E
    Quando peço a consulta
    Então nenhuma mantenedora é incluída, alterada ou apagada
    E nenhum registro de auditoria é gerado

  Cenário: Operação diferente de alteração e de consulta
    Quando informo uma opção diferente de ALT e de CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E a tela não confere nem grava nada

  Cenário: Tela não cadastrada
    Dado que a tela F115T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que o código de acesso da minha matrícula não tem a tela F115T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Operação não autorizada pelo perfil
    Dado que o perfil da tela não libera a operação da linha
    Quando marco a linha com I, A ou E e peço a alteração
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado nem auditado

  Cenário: Inclusão e exclusão exigem também a permissão de alteração
    Dado que o meu perfil libera a inclusão mas não a alteração
    Quando marco uma linha com a situação I e informo a opção ALT
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E a mantenedora não é incluída

  Cenário: A data do sistema e o tipo de órgão na tela
    Quando abro a tela
    Então vejo a data do sistema e a descrição do tipo de órgão da minha sessão
    E esses dois dados não são digitáveis
```
