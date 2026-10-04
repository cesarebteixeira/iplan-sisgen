# US — S070T — Exclusão das requisições de impressão de um relatório

## Estória

Como **servidor de CRE com a tela S070T autorizada**, quero **apagar as requisições
de impressão de um relatório**, para que **os pedidos que não devem mais ser
atendidos saiam da fila, sem ter de ser cancelados um a um**.

A requisição de impressão é o pedido de relatório que fica na fila esperando ser
processado. É esta tela que tira da fila os pedidos de um relatório inteiro, de uma
vez, e só os pedidos da área de quem está operando — os das outras áreas continuam
onde estão. Sem ela, um pedido que não deve mais ser atendido seria processado
depois, ou teria de ser cancelado requisição por requisição.

## Contexto

Jornada S000M → S001M → S004M → S070T.

Ator: servidor de CRE — informa o código de um relatório e apaga as requisições de
impressão dele que são da área da sua sessão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas entre o menu principal e esta — `S001M` e `S004M` — são menus: elas só
apontam a tela seguinte e não deixam registro nem operação para esta tela. Por isso
nada nesta tela muda conforme quem a chamou, e a operação que ela confere é a do seu
próprio campo, não a da tela de origem. Esta tela também não encadeia para outra: a
jornada termina nela. O contexto de negócio que ela usa — a matrícula, o privilégio,
o tipo de órgão, a CRE e o código de acesso — é o que a entrada deixou na sessão.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela só apaga requisição de impressão

Desta tela só saem exclusões: nada na fila de requisições de impressão é incluído e
nada é alterado. Ela também não mostra requisição nenhuma ao operador — quem cria o
pedido e quem o acompanha são outras telas. A exclusão é a única operação do
cadastro que ela chega a executar.

### RN-02 — Abrir a tela não apaga nada

Enquanto a tela é apenas aberta, nada é apagado: a abertura lê o cadastro de telas e
relatórios para confirmar que a tela existe e confere o acesso da matrícula, e
termina sem passar pela varredura das requisições. A exclusão só acontece numa
mensagem respondida pelo operador.

### RN-03 — A exclusão é pelo código do relatório, na mesma mensagem

Para apagar, o operador informa o código do relatório. É o único dado de negócio que
a exclusão usa: não há escolha de requisição, de período nem de área. A exclusão
acontece na mesma mensagem em que o código é informado — não há etapa de
confirmação — e a tela não devolve a lista nem a quantidade das requisições
apagadas.

### RN-04 — A exclusão alcança as requisições do relatório que são do tipo de órgão da sessão

Ao apagar, a tela varre as requisições do relatório informado e apaga cada uma que
seja do tipo de órgão da sessão. O tipo de órgão vem do vínculo que a entrada deixou
na sessão, não de um campo da tela.

[?] A varredura é pelo código do relatório, e a fila guarda também a CRE e o órgão
filho de cada requisição. Duas CREs com o mesmo tipo de órgão caem na mesma
exclusão. Se a exclusão deveria ser restrita à CRE de quem opera, o caminho não a
restringe. Pergunta ao site.

[?] A varredura posiciona a leitura pela chave (relatório, situação da requisição,
número da requisição) com a situação em branco e o número zerado, e o acervo não
documenta o que a leitura faz com uma chave assim: se ela posiciona no começo das
requisições daquele relatório — e a varredura as alcança — ou se procura a
requisição de número zero, e nada é apagado. O mesmo vale para a leitura da
requisição seguinte, feita logo depois de apagar a atual, sem reposicionar a chave.
Disso depende a exclusão existir de fato. Pergunta ao site.

### RN-05 — A exclusão alcança também as requisições sem tipo de órgão

Requisições do relatório que estão **sem tipo de órgão** também são apagadas: elas
não pertencem a nenhuma área e caem na mesma varredura.

### RN-06 — Requisição do relatório de outro tipo de órgão fica de fora

Requisição do mesmo relatório que seja de um tipo de órgão diferente do da sessão
não é apagada: a tela passa por ela e continua varrendo as demais.

### RN-07 — O código do relatório não é conferido contra o cadastro de telas e relatórios

O código informado vai direto para a varredura das requisições: a tela não procura o
relatório no cadastro de telas e relatórios. Um código que não existe não é recusado
como relatório não cadastrado — ele simplesmente não encontra requisição nenhuma.

### RN-08 — Sem requisição para o relatório, nada é apagado

Se o relatório informado não tem requisição nenhuma, a varredura termina sem apagar
e o sistema fica marcado como não tendo encontrado o registro.

[?] O que o operador vê nesse caso — se há mensagem e qual é o texto — depende de um
aviso do ambiente que não está nos fontes desta jornada. Pergunta ao site.

### RN-09 — A operação informada não comanda a exclusão

A operação informada serve à conferência de acesso, não à exclusão: o caminho que
apaga não consulta a operação. Com a operação de consulta, a conferência de acesso
não exige a autorização de exclusão — e a tela apaga as requisições do relatório do
mesmo jeito.

[?] A máscara desta tela não está no acervo: só se conhecem os campos que o programa
transporta. Não se sabe se a máscara oferece ao operador o campo da operação — e é
disso que depende esta regra. Se o campo não existir na máscara, o trecho fica sem
uso. Pergunta ao site.

[?] Quando a operação informada não é reconhecida, o sistema avisa
**\* Operacao nao disponivel \*** e a exclusão segue acontecendo: esse aviso, no
próprio trecho que o emite, não marca a falha que interromperia a mensagem (ao
contrário dos avisos de segurança, que a marcam). Ou a recusa deveria interromper a
mensagem, ou o caminho da exclusão deveria conferir a operação. Pergunta ao site.

### RN-10 — Antes de apagar, o sistema confere o acesso

A mensagem passa por quatro conferências, com o contexto da sessão. A tela `S070T`
precisa estar no cadastro de telas e relatórios — não estando, a recusa é
**\* Tela nao disponivel \***. A matrícula precisa ter a tela liberada no cadastro
de liberações do seu nível de acesso — não tendo, a recusa é
**\* Acesso negado para esta matricula \***. Sendo a operação a de exclusão, esse
mesmo cadastro precisa ter a exclusão liberada para esta tela — não tendo, a recusa
é **\* Acesso negado para esta operacao \***. Por fim, a operação passa pela
conferência de rota, que recusa a operação que a tela não reconhece
(**\* Operacao nao disponivel \***) e a tela que foi retirada do cadastro
(**\* Tela nao cadastrada \***).

[?] A autorização de exclusão só é exigida quando a operação informada é a de
exclusão (ou a de retorno): qualquer outra operação passa sem conferir liberação
nenhuma. Se a intenção era exigir a autorização de exclusão sempre que houver
exclusão, o caminho não a exige. Pergunta ao site.

### RN-11 — A exclusão não deixa rastro de auditoria

Ao apagar, a tela não grava registro de auditoria nem passa por nenhum outro
cadastro: a única alteração é a própria exclusão das requisições.

### RN-12 — Cada mensagem começa com os campos de contexto limpos

A cada mensagem respondida, a descrição do tipo de órgão e a data do sistema são
apagadas antes de qualquer conferência e não são repostas: a resposta sai com esses
dois campos em branco, mesmo que a tela os tivesse mostrado ao abrir.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se
existe um caminho de entrada em que os campos não são limpos, não foi possível
determinar. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Exclusão das requisições de impressão de um relatório

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S070T

  Cenário: RN-01 — A tela só apaga: não inclui, não altera e não mostra requisição
    Dado que existem requisições de impressão do relatório informado
    Quando informo o código do relatório e confirmo
    Então as requisições são apagadas
    E nenhuma requisição é incluída ou alterada
    E não vejo a lista das requisições

  Cenário: RN-02 — Abrir a tela não apaga nada
    Dado que abro a tela S070T
    Então nenhuma requisição é apagada
    E a tela apenas confere se ela está cadastrada e se a minha matrícula tem acesso

  Cenário: RN-03 — Exclusão das requisições do relatório informado
    Dado que existem requisições de impressão do relatório informado
    Quando informo o código do relatório
    Então as requisições daquele relatório saem da fila

  Cenário: RN-03 — A exclusão não pede confirmação e não devolve o que apagou
    Dado que existem requisições do relatório informado
    Quando informo o código do relatório
    Então a exclusão acontece na mesma mensagem
    E não vejo a lista nem a quantidade das requisições apagadas

  Cenário: RN-04 — A exclusão alcança as requisições do meu tipo de órgão
    Dado que existem requisições do relatório informado do tipo de órgão da minha sessão
    Quando informo o código do relatório
    Então essas requisições saem da fila

  Cenário: RN-05 — A exclusão alcança as requisições sem tipo de órgão
    Dado que existem requisições do relatório informado sem tipo de órgão
    Quando informo o código do relatório
    Então essas requisições também saem da fila

  Cenário: RN-06 — Requisição do relatório de outro tipo de órgão permanece
    Dado que existem requisições do relatório informado de outro tipo de órgão
    Quando informo o código do relatório
    Então essas requisições continuam na fila

  Cenário: RN-07 — Código de relatório que não existe
    Dado que informo um código que não existe no cadastro de telas e relatórios
    Quando confirmo a mensagem
    Então nada é apagado
    E não recebo recusa de relatório não cadastrado

  Cenário: RN-08 — Relatório sem requisição
    Dado que não existe requisição para o relatório informado
    Quando informo o código do relatório
    Então nada é apagado
    E o sistema fica marcado como não tendo encontrado o registro

  Cenário: RN-09 — A operação de consulta também apaga
    Dado que existem requisições do relatório informado do meu tipo de órgão
    Quando informo a operação de consulta junto com o código do relatório
    Então as requisições são apagadas do mesmo jeito
    E nenhuma autorização de exclusão me é exigida

  Cenário: RN-09 — Operação não reconhecida
    Dado que informo uma operação que a tela não reconhece
    Quando confirmo a mensagem
    Então vejo a mensagem "* Operacao nao disponivel *"

  Cenário: RN-10 — Tela não cadastrada
    Dado que a tela S070T não está no cadastro de telas e relatórios
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: RN-10 — Sem autorização para a tela
    Dado que a minha matrícula não tem a tela S070T no seu código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: RN-10 — Sem autorização de exclusão
    Dado que o meu código de acesso tem a tela S070T sem a exclusão liberada
    Quando informo a operação de exclusão com o código de um relatório
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E as requisições não são apagadas

  Cenário: RN-10 — Tela retirada do cadastro
    Dado que a tela S070T foi retirada do cadastro de telas e relatórios
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"

  Cenário: RN-11 — A exclusão não deixa rastro de auditoria
    Dado que existem requisições do relatório informado do meu tipo de órgão
    Quando informo o código do relatório
    Então as requisições são apagadas
    E nenhum registro de auditoria é gravado

  Cenário: RN-12 — A cada mensagem os campos de contexto ficam em branco
    Dado que a tela abriu mostrando a descrição do tipo de órgão e a data do sistema
    Quando respondo uma mensagem
    Então a resposta vem com esses dois campos em branco
```
