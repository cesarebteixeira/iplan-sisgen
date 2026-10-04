# US — E760T — Cardápios registrados por dia de um órgão filho

## Estória

Como **servidor de CRE**, quero **consultar, excluir e restabelecer os cardápios
registrados para cada dia de um mês, num órgão filho, num segmento de atendimento e numa
refeição**, para que **o registro diário daquela unidade fique fiel ao que foi previsto — e
uma exclusão feita por engano possa ser desfeita sem depender de outro setor**.

O registro de cada dia é o que amarra o cardápio à unidade que o serve: é ele que a tela
irmã `E760C` percorre e conta por cardápio, para comparar o que já está registrado com o que
foi planejado para o mês. Sem esta tela, um dia registrado por
engano só se corrigiria fora do sistema; e sem o estorno, a correção seria irreversível — o
dia sairia do registro e não teria como voltar.

## Contexto

Jornada S000M → E000M → E050M → E760T.
Ator: servidor de CRE — consulta, exclui e restabelece o cardápio registrado em cada dia de
um mês, para um órgão filho, um segmento de atendimento e uma refeição.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As regras abaixo são só as da **tela desta jornada**.

## Regras de negócio

### RN-01 — A tela mostra, dia a dia, o cardápio registrado num mês — e corrige esse registro

A tela opera sobre cinco coisas: o **órgão filho (SDI)**, de 8 dígitos; a **coordenação
regional escolar**, de 2; o **segmento de atendimento**, de 2; a **refeição**, de 2; e o
**mês e o ano**. Com elas ela lista os dias daquele mês que têm cardápio registrado para
aquela unidade, segmento e refeição, mostra a descrição do cardápio de cada dia e permite
**excluir** o cardápio de um dia e **restabelecer** um dia já excluído. A tela não inclui
cardápio novo por escolha do usuário nem troca o cardápio de um dia já registrado: ela só
tira e devolve o dia.

Cada linha da lista é um **dia**, com o dia, o código do cardápio, uma marca de cardápio
extra (um asterisco) e a descrição do cardápio. A lista traz **treze linhas** por vez, e a
tela reexibe, ao abrir, o último período trabalhado na sessão; na primeira abertura da
sessão, nenhum período.

### RN-02 — A digitação é numérica, e o campo em branco vira zero

**Oito** campos numéricos passam pela edição numérica antes de qualquer leitura: o órgão
filho (8 dígitos), a coordenação regional escolar (2), o segmento de atendimento (2), a
refeição (2), o mês (2), o ano (4), o dia informado no cabeçalho (2) e o dia a estornar (2).
Cada um é conferido com o seu próprio rótulo, e o valor em branco entra como zero.

[?] A rotina de edição numérica é do sistema, sem corpo no material: o que ela recusa, e com
que mensagem, não se lê nesta jornada. O que se lê é que a recusa devolve o cursor ao campo
recusado.

### RN-03 — A lista percorre o mês dia a dia, até treze dias, e mostra a descrição do cardápio de cada data

Preenchidos o órgão, o segmento, a refeição, o mês e o ano, a tela percorre os registros
daquele mês e preenche as linhas, uma por registro. O percurso para quando o registro lido
deixa de pertencer àquele órgão, segmento, refeição, mês e ano — e o dia é justamente o que
muda de uma linha para a outra. Para cada dia, a descrição mostrada é a do cardápio daquele
código **vigente naquela data**: o cadastro de cardápios é procurado pelo código e pela data
do próprio dia.

A linha cujo registro está marcado como cardápio extra aparece com um **asterisco**; a linha
cujo cardápio não é encontrado no cadastro fica com a marca de não encontrado no lugar da
descrição.

[?] Que fato do negócio marca um cardápio como "extra", e quem o marca, não está no material
desta jornada: a tela apenas mostra o asterisco.

[?] Que a leitura avance dia a dia é conclusão do desenho do laço (a comparação da chave
ignora o dia, e a tela guarda o dia lido para a linha seguinte); a rotina de leitura é do
sistema e não tem corpo no material.

### RN-04 — Mês sem sobremesa cadastrada é avisado

Não havendo nenhum registro no mês para aquele órgão, segmento e refeição, a tela avisa
**\* Mes sem sobremesas cadastradas \*** e não mostra linhas.

### RN-05 — A tela só trabalha em alteração e em consulta, e abre em consulta

A opção de manutenção aceita apenas **alteração** e **consulta**; qualquer outra é recusada
com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no campo da opção, e nada é
lido nem gravado. Entrando sem informar a opção, a tela assume **consulta**.

[?] A recusa manda usar "ALT" e "CON", mas a guarda interna compara o campo com outros dois
códigos. Ou o terminal traduz o que o usuário digita antes de enviar, ou a mensagem está
desalinhada da guarda. Pergunta ao site; não concluo qual dos dois.

### RN-06 — Para excluir ou estornar, é preciso ter consultado a mesma combinação

Em alteração, a tela confere se o órgão, o segmento, a refeição e o mês e ano informados são
os mesmos da consulta anterior; não sendo, recusa com
**\* Consulte periodo antes de atualizar \***, com o cursor no campo da opção, e não grava
nada. Em consulta, a mesma recusa aparece quando o período difere do consultado **e** há um
dia a estornar informado.

### RN-07 — O órgão filho e a coordenação da sessão limitam a tela

Se o vínculo do usuário com a secretaria deixa um órgão filho para a sessão, a tela força
esse órgão — tanto ao exibir quanto ao conferir — e a coordenação regional escolar da sessão
é adotada. Tentar trabalhar em outro órgão é recusa:
**\* Usuario sem acesso a outro orgao \***, com o cursor no campo do órgão. Sem órgão
informado, a recusa é **\* Informe o orgao \***.

### RN-08 — O órgão informado tem que existir, ser da secretaria e do grupo do usuário

O órgão é lido no cadastro de órgãos e passa por três peneiras, nesta ordem: tem que existir
(**\* Orgao nao cadastrado \***); tem que ser do tipo de órgão da secretaria do usuário
(**\* Orgao nao pertence a esta secretaria \***); e, quando o usuário tem coordenação
regional, o órgão tem que ser do grupo dele
(**\* <- Usuario sem acesso ao grupo deste orgao \***). Em cada recusa o cursor volta ao
campo do órgão e nada é gravado.

### RN-09 — O segmento e a refeição têm que estar cadastrados, e a coordenação exibida vem do cadastro do órgão

O segmento informado é procurado no cadastro de segmentos daquele tipo de órgão — senão
**\* Segmento nao cadastrado \*** — e a refeição, no cadastro de refeições — senão
**\* Refeicao nao cadastrada \***. As descrições dos dois são mostradas na tela. A
coordenação regional escolar exibida não é a digitada: o programa a substitui pela do
cadastro do órgão.

[?] A coordenação regional escolar é digitável na tela e passa pela edição numérica, mas
sempre é substituída pela do cadastro do órgão. Ou o campo de entrada serve para conferência,
ou o que o usuário digita é ignorado. Pergunta ao site.

### RN-10 — O mês e o ano são obrigatórios, e o mês tem que ter registro

Sem mês e ano informados, a recusa é **\* Informe mes/ano \***, com o cursor no campo do mês.
Informados, a tela confere que existe registro daquele órgão, segmento e refeição no mês e
ano — senão **\* Nao existem registros para este mes/ano \*** — e só então segue.

### RN-11 — A exclusão tira o cardápio do dia do registro diário e o guarda no cadastro de exclusões

Em cada linha, a situação **E** exclui o cardápio daquele dia. A linha tem que ter um dia
informado (a linha sem dia é recusada com **\* Exclua cardapio de linha preenchida \***) e
esse dia tem que ter cardápio registrado — senão
**\* Cardapio nao cadastrado para este dia \***. A exclusão passa ainda pela autorização de
exclusão do perfil da sessão. Passando, o registro daquele dia sai do cadastro diário e fica
guardado no cadastro de exclusões, e a operação é lançada na auditoria (`A010T`) com a tela
de origem, o cadastro diário identificado como o cadastro alterado, a operação de exclusão, o
conteúdo anterior do dia e o número do processo montado com o órgão, o segmento, a refeição,
o ano e o mês.

[?] A recusa da linha sem dia fala de "linha preenchida": a guarda recusa quando a linha
**não** tem dia, e a mensagem manda excluir o cardápio de uma linha preenchida. Ou a mensagem
está desalinhada da guarda, ou a guarda vale para outro caso. Pergunta ao site.

### RN-12 — O estorno devolve ao registro diário o dia que foi excluído

Informando o dia a estornar e deixando vazia a situação abaixo da lista, a tela confere que
existe, no cadastro de exclusões, o registro daquele dia — senão
**\* Dia sem cardapio a estornar \***, com o cursor no campo do dia. Existindo, a tela tira o
dia do registro diário (se ainda estiver lá) e o devolve a partir do registro guardado no
cadastro de exclusões, apagando esse registro. O estorno não gera lançamento na auditoria.

O estorno e a exclusão por linha não convivem: informado o dia a estornar, as situações das
linhas não são processadas.

[?] O estorno não deixa lançamento na auditoria, ao contrário da exclusão que ele desfaz. Se
a volta do dia deve ou não ficar registrada, é pergunta ao site.

[?] A remoção do registro do cadastro de exclusões depende de um retorno do sistema que não
tem corpo no material; não dá para concluir, pela fonte, se o registro de exclusões sempre
sai quando o dia volta.

### RN-13 — A tela passa para a E760C quando a situação abaixo da lista é preenchida

Preenchendo o campo de situação abaixo das linhas, a tela entrega a navegação para a
**E760C** — a tela irmã, do mesmo mês e do mesmo órgão, que confronta o que está registrado
com o que foi planejado. A passagem não ensina operação nenhuma: a `E760C` abre pelo que ela
mesma tem. A conferência do período (RN-06) acontece antes dessa passagem, de modo que o dia
a estornar informado perde para ela.

[?] O que viaja nessa passagem — se os campos da tela de origem, se nada além do destino —
não está no fonte desta tela, que só troca o destino e não ensina operação. Pergunta ao site.

### RN-14 — Em consulta, nada é gravado

Em consulta, a passagem que grava é abandonada antes de qualquer leitura de dia: nenhum
cardápio é excluído, nenhum estorno acontece e nenhum lançamento de auditoria é gerado.

### RN-15 — Sem a autorização de perfil e de rota, nada é conferido nem gravado

Ao abrir, a tela passa pela autorização de acesso à tela. Antes de conferir os campos, passa
pela autorização de rota (levando o prefixo de tela, a matrícula, o acesso, o privilégio, o
tipo de órgão, a coordenação da sessão e a opção informada) e pela autorização da operação
pretendida. Não voltando "OK" de qualquer uma delas, a transação é abandonada em silêncio. A
exclusão de cada linha ainda consulta, por conta própria, a autorização de exclusão.

[?] As rotinas de segurança e de rota só aparecem declaradas, sem corpo no material: quem
pode excluir ou estornar não se lê nesta jornada.

### RN-16 — Prefixo de tela preenchido abandona a conferência, e a passagem que grava não o testa

Chegando com o prefixo de tela preenchido, a passagem de conferência da tela é abandonada em
silêncio — sem mensagem e sem marcar erro —, e a passagem seguinte, que é a que grava, não
testa esse prefixo de novo. Nada nesta tela escreve nesse campo.

[?] Com o prefixo preenchido, a exclusão e o estorno correm sem as conferências de órgão,
segmento, refeição, mês e dia — inclusive o estorno sem haver exclusão a desfazer, que nesse
caminho apaga o dia do registro diário sem devolvê-lo. Ou a guarda vale para outro caso, ou
esse caminho é inalcançável pelo terminal. Não se sabe, também, quem preenche o prefixo.
Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Cardápios registrados por dia de um órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E760T

  Cenário: Consulta mostra o mês dia a dia
    Dado que estou na E760T em modo de consulta
    Quando informo o órgão filho, a coordenação regional escolar, o segmento, a refeição, o mês e o ano
    Então vejo até treze dias daquele mês, cada linha com o dia, o código e a descrição do cardápio
    E nada é gravado

  Cenário: Dia com cardápio extra aparece marcado
    Dado que um dos dias do mês está registrado como cardápio extra
    Quando consulto o mês
    Então a linha daquele dia aparece com um asterisco

  Cenário: Mês sem sobremesa cadastrada
    Dado que não há cardápio registrado no mês informado para aquele órgão, segmento e refeição
    Quando consulto
    Então vejo a mensagem "* Mes sem sobremesas cadastradas *"
    E nenhuma linha é mostrada

  Cenário: Campo com valor que não é número
    Quando preencho um dos campos numéricos com valor que não é número
    Então o sistema recusa o campo e o cursor volta para ele

  Cenário: Opção de manutenção indisponível
    Quando informo uma opção diferente de alteração e de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E nada é gravado

  Cenário: Excluir sem ter consultado antes
    Dado que estou em alteração e mudo o órgão, o segmento, a refeição, o mês ou o ano
    Quando confirmo a exclusão de uma linha
    Então vejo a mensagem "* Consulte periodo antes de atualizar *"
    E nada é gravado

  Cenário: Estornar em consulta com período diferente do consultado
    Dado que estou em consulta e o período informado difere do último consultado
    Quando informo o dia a estornar
    Então vejo a mensagem "* Consulte periodo antes de atualizar *"
    E nada é gravado

  Cenário: Órgão fora do alcance do meu vínculo
    Dado que o meu vínculo deixou um órgão filho para a sessão
    Quando informo outro órgão filho
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E nada é gravado

  Cenário: Órgão não informado
    Quando deixo o órgão filho em branco
    Então vejo a mensagem "* Informe o orgao *"
    E nada é gravado

  Cenário: Órgão não cadastrado
    Quando informo um órgão filho que não existe no cadastro de órgãos
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E nada é gravado

  Cenário: Órgão de outra secretaria
    Quando informo um órgão filho que não é do tipo de órgão da minha secretaria
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E nada é gravado

  Cenário: Órgão de outro grupo
    Dado que tenho coordenação regional na sessão
    Quando informo um órgão filho que não é do meu grupo
    Então vejo a mensagem "* <- Usuario sem acesso ao grupo deste orgao *"
    E nada é gravado

  Cenário: Segmento de atendimento não cadastrado
    Quando informo um segmento que não está cadastrado para aquele tipo de órgão
    Então vejo a mensagem "* Segmento nao cadastrado *"
    E nada é gravado

  Cenário: Refeição não cadastrada
    Quando informo uma refeição que não está cadastrada
    Então vejo a mensagem "* Refeicao nao cadastrada *"
    E nada é gravado

  Cenário: Mês e ano não informados
    Quando deixo o mês e o ano em branco
    Então vejo a mensagem "* Informe mes/ano *"
    E nada é gravado

  Cenário: Mês sem registros
    Dado que não há registro para aquele órgão, segmento e refeição no mês informado
    Quando confirmo
    Então vejo a mensagem "* Nao existem registros para este mes/ano *"
    E nada é gravado

  Cenário: Exclusão do cardápio de um dia
    Dado que consultei o órgão, o segmento, a refeição e o mês
    Quando marco a situação E na linha de um dia que tem cardápio registrado
    Então o cardápio daquele dia sai do registro diário e fica guardado no cadastro de exclusões
    E a operação fica registrada na auditoria

  Cenário: Linha marcada para exclusão sem dia
    Dado que estou em alteração
    Quando marco a situação E numa linha que não tem dia
    Então vejo a mensagem "* Exclua cardapio de linha preenchida *"
    E nada é gravado

  Cenário: Dia marcado para exclusão sem cardápio registrado
    Dado que estou em alteração
    Quando marco a situação E na linha de um dia que não tem cardápio registrado
    Então vejo a mensagem "* Cardapio nao cadastrado para este dia *"
    E nada é gravado

  Cenário: Estorno de um dia excluído
    Dado que consultei o órgão, o segmento, a refeição e o mês
    E existe uma exclusão registrada para um dia daquele mês
    Quando informo aquele dia no campo do dia a estornar
    Então o cardápio daquele dia volta ao registro diário
    E o registro de exclusão é apagado

  Cenário: Estornar um dia sem exclusão a desfazer
    Dado que não existe exclusão registrada para o dia informado
    Quando informo aquele dia no campo do dia a estornar
    Então vejo a mensagem "* Dia sem cardapio a estornar *"
    E nada é gravado

  Cenário: Estorno e linhas marcadas no mesmo envio
    Dado que informo o dia a estornar
    E marco a situação E em uma linha
    Quando confirmo
    Então só o estorno é processado
    E a linha marcada não gera exclusão

  Cenário: Consulta não grava nada
    Dado que estou na E760T em modo de consulta
    Quando a tela mostra o mês e eu saio
    Então nenhum cardápio é excluído e nenhum estorno acontece
    E nenhum lançamento de auditoria é gerado

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não tem a autorização da operação pretendida para esta tela
    Quando tento excluir ou estornar
    Então a transação é abandonada sem gravar

  Cenário: Passagem para a E760C
    Dado que consultei o órgão, o segmento, a refeição e o mês
    Quando preencho o campo de situação abaixo da lista
    Então a tela passa para a E760C
    E nenhuma exclusão nem estorno da E760T é processado

  Cenário: Chegada com o prefixo de tela preenchido
    Dado que a transação chega à E760T com o prefixo de tela preenchido
    Quando confirmo
    Então nenhuma conferência é feita e nada é mostrado
    E a passagem que grava segue sem testar o prefixo
```
