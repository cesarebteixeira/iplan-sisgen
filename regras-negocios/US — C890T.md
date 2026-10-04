# US — C890T — Excluir o planejamento de estimativa de um período

## Estória

Como **servidor de CRE**, quero **pedir a exclusão do planejamento de estimativa de um
período encerrado do meu órgão, dizendo se a exclusão leva junto o planejamento sazonal
e os máximos de comensais**, para que **o período que já não vale saia do sistema, em
vez de continuar respondendo às conferências das outras telas e aos relatórios**.

A estimativa da alimentação escolar é montada por período, por coordenação regional
escolar e por cardápio, e é dela que as outras telas e os relatórios se servem. Quando o
período acaba, o que ficou registrado para ele passa a atrapalhar: a estimativa velha
continua respondendo como se ainda valesse. Esta é a tela que tira o período do cadastro.

Só que ela não apaga na hora: ela **pede** a exclusão ao processamento que roda fora da
transação, e é esse processamento que apaga. O servidor recebe o aviso e o período só
some depois que o processamento termina.

## Contexto

Jornada S000M → C000M → C800M → C811M → C890T.

Ator: servidor de CRE — encerra o período informando o grupo, as duas datas e as duas
respostas, e confirma o pedido de exclusão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os três menus do caminho (C000M, C800M e C811M) são
menus e **não gravam nada**: apenas encaminham. O C811M entrega à tela desta jornada os
campos do próprio formulário, que chegam na primeira apresentação; o contexto que ela
usa — matrícula, código de acesso, privilégio, tipo de órgão, coordenação regional
escolar, a estação e a data do sistema — é o que a entrada deixou na sessão.

Esta tela é de transação e **não encadeia em outra**: ela reabre a si mesma. As regras
abaixo são só as da tela desta jornada; as que se revelaram da entrada estão no anexo de
evidências. A tela não é a última palavra sobre a exclusão: quem apaga é o processamento
que ela enfileira.

---

## Regras de negócio

### RN-01 — A tela serve à exclusão, e a operação da tela é reposta em alteração

A tela não tem modo de consulta e não abre em inclusão: **a cada apresentação ela repõe a
própria operação em alteração**, que é a única com que ela trabalha. A tela também
determina sozinha a operação que examina, sem depender do que o formulário trouxe, e é
por isso que ela **não chega a conferir se a operação informada é alteração** antes de
seguir.

[?] Existe na tela a recusa **\* Opcao nao disponivel. Use ALT \***, com o cursor no
campo da resposta da confirmação — mas ela depende de a operação chegar diferente de
alteração, e o trecho que a executa acaba de repor essa operação. Não dá para afirmar,
pelo acervo lido, qual das duas coisas acontece primeiro, nem se a recusa é alcançável.
Pergunta ao site.

### RN-02 — O que a tela pede: o grupo, o período e as duas respostas

Para pedir a exclusão, o servidor informa o **grupo** — a coordenação regional escolar,
com dois dígitos — e o **período**, em duas datas: o dia, o mês e o ano do **início** e o
dia, o mês e o ano do **limite**. Responde também, com S ou N, a duas perguntas: se a
exclusão leva junto o **planejamento sazonal** e se leva junto os **máximos de
comensais**. São ao todo sete campos numéricos e duas respostas de um caractere, e a
tela ainda mostra a descrição do órgão e a data do sistema, que não se digitam. Só o
grupo e as duas respostas aparecem como campo na tela; as seis posições das duas datas
não são apresentadas, e a tela as repõe do que guardou depois de achar o período.

### RN-03 — Os campos numéricos são editados antes de qualquer leitura, e o cursor volta ao campo recusado

Antes de ler qualquer cadastro, os sete campos numéricos passam pela edição de número: o
dia e o mês são de dois dígitos e o ano, de quatro. O campo em branco vale zero. Quando a
edição recusa a digitação, a tela devolve o cursor ao campo recusado — o grupo, o dia
limite, o mês limite ou o ano limite — e nada é lido nem gravado.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não está
nos fontes lidos: a rotina que faz a edição numérica pertence a uma biblioteca que não
faz parte do acervo desta jornada. E, entre os sete campos, só o grupo e a data limite
têm posição de cursor na conferência: recusada a data inicial, o cursor não se move. Se é
intencional, o acervo não diz. Pergunta ao site.

### RN-04 — Sem grupo informado, a tela avisa e não procura nada

O grupo em branco vale zero, e zero não é grupo nenhum: a tela recusa com
**\* Informe o grupo \***, com o cursor no campo do grupo, e não lê nenhum cadastro do
planejamento. Nada é gravado e nenhum pedido é criado.

### RN-05 — O período tem de estar cadastrado para a data limite informada

Com um grupo diferente de 99 informado, a tela procura o planejamento do órgão do
servidor cujo período **termina** no ano, no mês e no dia do limite informados, e
confere se a coordenação do registro achado é a do grupo informado. Não achando —
inclusive quando o registro achado é de outra coordenação —, avisa
**\* Nao existe planejamento para esta data \***, com o cursor no campo do grupo, e nada
é gravado. Achando, a **data inicial** que a tela repõe é a que está registrada no
cadastro do período — o servidor não precisa digitá-la, e, se digitou outra, vale a do
cadastro —, e a tela guarda o estado do cadastro para conferir em seguida.

### RN-06 — O grupo 99 vale por todas as coordenações do órgão, e só ele

O valor **99** no grupo é o único que a tela não compara com a coordenação do registro:
com 99 ela aceita o primeiro planejamento do órgão que termine no limite informado, de
qualquer coordenação. E é também o único valor que o processamento da exclusão
enfileirado sabe abrir por inteiro: recebendo 99, ele percorre as coordenações
cadastradas do órgão, uma a uma; recebendo outro grupo, ele age só sobre aquele.

[?] A tela procura o período com a coordenação em branco e 99 é justamente o valor que
dispensa a comparação; mas o acervo lido não diz o que a leitura faz com essa
coordenação em branco. Se ela exigir um registro de coordenação zerada, a tela pode
recusar com **\* Nao existe planejamento para esta data \*** um período que o
processamento apagaria. Pergunta ao site.

### RN-07 — O cadastro fechado não pode ser excluído

Achado o período e batendo a coordenação, a tela confere o estado do cadastro da
estimativa: se ele estiver marcado como **fechado**, a exclusão não segue e o sistema
avisa **\* Cadastro fechado para este periodo \***, com o cursor no dia limite. Nada é
gravado.

[?] O estado é um campo de um caractere, e esta tela só reconhece o valor que trata como
fechado; o que os outros valores significam — aberto, em digitação, cancelado — não vem
do material lido. Pergunta ao site.

### RN-08 — As duas respostas são obrigatórias, e cada uma só aceita S ou N

Com o período achado e o cadastro não fechado, a tela exige as duas respostas. Cada uma
só aceita **S** ou **N**: em branco ou qualquer outro valor, o sistema avisa
**\* Inf se exclui planejamento sazonal com S ou N \***, com o cursor na resposta do
sazonal, ou **\* Informe se exclui maximos comensais com S ou N \***, com o cursor na
resposta dos máximos, e nada é gravado. O sazonal é conferido antes dos máximos.

### RN-09 — A exclusão só segue depois da confirmação, e só a resposta S a confirma

Passadas as conferências, a tela guarda o grupo e o período, pergunta
**\* Confirma exclusao do planejamento <S/N> ? \*** na linha de mensagem e espera a
resposta na mensagem seguinte, com o cursor no campo da resposta. Só a resposta **S**
segue. Qualquer outra — N, em branco ou outro caractere — desfaz a guarda e o registro
do período que já havia sido achado, e devolve a tela às conferências; como a guarda se
perdeu, a tela volta a exigir o período e a mesma pergunta. Enquanto o servidor não
responder S, a exclusão não é pedida e nada é gravado. Se, na mensagem da resposta, o
grupo ou a data limite mudarem, a confirmação também é desfeita, mesmo que a resposta
seja S. O que a tela grava depois é o grupo e o período que ela guardou na pergunta, não
o que estiver digitado.

[?] Não há caminho de desistência pela resposta: o N volta à conferência e à mesma
pergunta, e só sair da tela interrompe. Se o N deveria cancelar a exclusão, o acervo não
mostra. Pergunta ao site.

### RN-10 — Só um pedido de exclusão por vez, em todo o sistema

Antes de gravar, a tela confere a fila de requisições de relatório pelo código do
relatório desta exclusão e recusa se houver **qualquer** requisição daquele relatório —
de qualquer órgão e em qualquer situação. A recusa é
**\* Relatorio em processamento. Aguarde. \***, com o cursor no campo da resposta, e ela
desfaz a confirmação: o servidor volta a ter de confirmar. Nada é gravado. A requisição
sai da fila quando o processamento termina de apagar.

[?] A conferência não olha o órgão nem a situação da requisição: uma requisição que
tenha sobrado de um processamento que falhou bloqueia o relatório inteiro, para todos os
órgãos, e o acervo não mostra o que limpa uma requisição que falhou. Pergunta ao site.

### RN-11 — A confirmação deixa registro na trilha de auditoria

Confirmada a exclusão, a tela grava na trilha de auditoria um registro com o código da
tela, a matrícula do servidor, a estação, o órgão, a coordenação, a data e a hora da
sessão e o conteúdo do pedido que será criado. A operação é registrada como **inclusão**,
e o número do processo do registro recebe o dia da data inicial, não o número da
requisição criada.

[?] A auditoria registra esta operação como inclusão, e o número do processo do registro
recebe o dia da data inicial. Ou a auditoria registra o pedido que entrou na fila, ou o
rótulo da operação está trocado; em qualquer dos dois casos o registro fica sem um número
de processo próprio. Pergunta ao site.

### RN-12 — A tela registra o pedido e o entrega ao processamento fora da transação

Confirmada a exclusão, a tela cria a requisição do relatório de exclusão: o número
seguinte ao da última requisição registrada, o órgão do servidor, a matrícula, a estação,
a data do pedido e a situação em branco. O grupo, o período e as duas respostas não ficam
como campo da requisição: eles vão no bloco de parâmetros que acompanha o
encaminhamento, junto com o correio eletrônico cadastrado do servidor. O pedido é então
entregue ao processamento que roda fora da transação, e a tela se reapresenta com
**\* Cadastro sendo excluido \***. O servidor recebe o aviso e vai embora sem ver o
resultado.

[?] Se o encaminhamento não ocorrer, a requisição fica na fila e, pela RN-10, bloqueia o
relatório inteiro para todos os órgãos; o acervo não mostra quem a limpa. A camada que
recebe o encaminhamento não tem fonte nos fontes desta jornada, e o correio eletrônico
do servidor vai no bloco mas não fica na requisição: quem o consome não tem fonte aqui.
Pergunta ao site.

### RN-13 — A tela não apaga nada

Dos seis cadastros que a tela enxerga, as rotinas de exclusão e de trava estão todas
declaradas e **nenhuma é executada**: o único cadastro do planejamento que ela toca é o
período, e só para ler. As duas únicas gravações que a transação faz são a trilha de
auditoria (RN-11) e a requisição (RN-12), e as duas são inclusões. Quem apaga é o
processamento da RN-14.

### RN-14 — O processamento apaga o planejamento do período e libera a fila

O processamento enfileirado percorre as coordenações do órgão que o pedido alcança — só
o grupo informado, ou todas as coordenações cadastradas quando o grupo é 99 —, e para
cada uma apaga o planejamento de estimativa do período; se a resposta do sazonal foi S,
apaga também o planejamento sazonal; e se a resposta dos máximos foi S, apaga também os
máximos de comensais. O apagamento se repete até não restar registro do período. Ao
terminar, apaga a própria requisição e libera a fila — é isso que permite pedir a
exclusão de outro período. De vez em quando o processamento faz uma pausa, que é também
o ponto em que ele atende a um pedido de encerramento.

### RN-15 — A tela exibe a descrição do órgão e a data do sistema

Além dos campos informados e da linha de mensagem, a tela mostra a **descrição do órgão**
do servidor e a **data do sistema**. Nenhuma das duas é digitada: as duas vêm da sessão.

### RN-16 — Falha de banco interrompe a transação

Toda leitura e toda gravação conferem o erro do banco, e a transação para ali, sem
completar o resto — a trilha de auditoria e a requisição não chegam a ser gravadas.

---

## Cenários BDD

```gherkin
Funcionalidade: Excluir o planejamento de estimativa de um período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C890T

  Cenário: RN-01 — a tela repõe a operação de alteração a cada apresentação
    Dado que chego à tela C890T
    Então a tela se apresenta com a operação de alteração
    E não me oferece modo de consulta nem de inclusão

  Cenário: RN-02 — o que a tela pede
    Dado que estou na tela C890T
    Então informo o grupo e o período, em duas datas de dia, mês e ano
    E respondo com S ou N se a exclusão leva o planejamento sazonal
    E respondo com S ou N se a exclusão leva os máximos de comensais
    E vejo a descrição do meu órgão e a data do sistema, sem digitá-las

  Cenário: RN-03 — os campos numéricos são editados como número
    Dado que estou na tela C890T
    Quando informo o grupo e as duas datas, deixando um campo numérico em branco
    Então o campo em branco é editado como zero
    E, se a digitação for recusada, o cursor volta ao campo recusado
    E nada é lido nem gravado

  Cenário: RN-04 — grupo não informado
    Dado que estou na tela C890T
    Quando informo o período e deixo o grupo em branco
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo do grupo
    E nenhum cadastro do planejamento é lido
    E nenhum pedido de exclusão é criado

  Cenário: RN-05 — o período não está cadastrado para a data limite
    Dado que nenhum planejamento do meu órgão termina na data limite informada
    Quando informo o grupo e o período
    Então vejo "* Nao existe planejamento para esta data *"
    E o cursor fica no campo do grupo
    E nenhum pedido de exclusão é criado

  Cenário: RN-05 — o período está cadastrado
    Dado que existe um planejamento do meu órgão terminando na data limite informada
    E a coordenação do registro é a do grupo que informei
    Quando informo o grupo e a data limite
    Então a tela repõe a data inicial registrada no cadastro do período
    E guarda o estado do cadastro para conferir em seguida

  Cenário: RN-06 — o grupo informado é o do órgão inteiro
    Dado que informo o grupo 99
    Quando informo a data limite
    Então a tela aceita o planejamento de qualquer coordenação do meu órgão que termine naquela data
    E o processamento do pedido vai percorrer as coordenações cadastradas do órgão

  Cenário: RN-07 — o cadastro do período está fechado
    Dado que o planejamento achado está marcado como fechado
    Quando informo o grupo e o período
    Então vejo "* Cadastro fechado para este periodo *"
    E o cursor fica no dia limite
    E nenhum pedido de exclusão é criado

  Cenário: RN-08 — falta responder sobre o planejamento sazonal
    Dado que o planejamento do período foi achado e não está fechado
    Quando deixo a resposta do sazonal em branco ou informo outra coisa que não S ou N
    Então vejo "* Inf se exclui planejamento sazonal com S ou N *"
    E o cursor fica no campo dessa resposta
    E nenhum pedido de exclusão é criado

  Cenário: RN-08 — falta responder sobre os máximos de comensais
    Dado que já respondi sobre o planejamento sazonal
    Quando deixo a resposta dos máximos em branco ou informo outra coisa que não S ou N
    Então vejo "* Informe se exclui maximos comensais com S ou N *"
    E o cursor fica no campo dessa resposta
    E nenhum pedido de exclusão é criado

  Cenário: RN-09 — a pergunta de confirmação
    Dado que o grupo, o período e as duas respostas passaram pelas conferências
    Quando a tela me pergunta "* Confirma exclusao do planejamento <S/N> ? *"
    Então o cursor fica no campo da resposta
    E a tela espera a minha resposta na mensagem seguinte

  Cenário: RN-09 — a resposta que não confirma
    Dado que a tela está esperando a resposta da confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a confirmação e o período achado são desfeitos
    E a tela volta a conferir e a me perguntar
    E nada é gravado

  Cenário: RN-09 — muda o grupo ou a data limite depois da pergunta
    Dado que a tela está esperando a resposta da confirmação
    Quando respondo S mudando o grupo ou a data limite
    Então a confirmação é desfeita
    E a tela volta a conferir e a me perguntar
    E nada é gravado

  Cenário: RN-10 — já existe um pedido de exclusão em andamento
    Dado que existe uma requisição do relatório desta exclusão na fila, de qualquer órgão
    Quando respondo S à pergunta de confirmação
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor fica no campo da resposta
    E a confirmação é desfeita e preciso confirmar de novo
    E nada é gravado

  Cenário: RN-11, RN-12 e RN-13 — confirmar a exclusão de um período
    Dado que o período está cadastrado, não está fechado e não há requisição em andamento
    Quando respondo S à pergunta de confirmação
    Então o sistema grava o registro na trilha de auditoria
    E cria a requisição do relatório de exclusão com o órgão, a minha matrícula, a estação e a data
    E entrega ao processamento o grupo, o período e as duas respostas
    E vejo "* Cadastro sendo excluido *"
    E nenhum cadastro do planejamento é apagado nesta transação

  Cenário: RN-14 — o processamento apaga o planejamento do período
    Dado que o pedido de exclusão foi criado para um órgão e uma data limite
    Quando o processamento assume o pedido
    Então o planejamento de estimativa daquela data limite é apagado
    E o planejamento sazonal é apagado se a resposta foi S
    E os máximos de comensais são apagados se a resposta foi S
    E o próprio pedido é apagado ao fim, liberando a fila

  Cenário: RN-14 — o pedido do órgão inteiro percorre as coordenações
    Dado que o pedido foi feito com o grupo 99
    Quando o processamento assume o pedido
    Então ele apaga o planejamento do período em cada coordenação cadastrada do órgão

  Cenário: RN-15 — a descrição do órgão e a data do sistema
    Dado que abri a tela C890T
    Então vejo a descrição do meu órgão e a data do sistema, sem digitá-las

  Cenário: RN-16 — falha de banco na confirmação
    Dado que a gravação falha no banco
    Quando respondo S à pergunta de confirmação
    Então a transação é interrompida com a mensagem de erro do sistema
    E o pedido de exclusão não é considerado criado
```
