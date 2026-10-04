# US — M100T — Manter o perfil mensal de atendimento do órgão filho

## Estória

Como **servidor da CRE**, quero **registrar e conferir, para um órgão filho e um mês de
referência, o perfil mensal de atendimento — as quantidades de matriculados de cada faixa,
as refeições e os residentes —**, para que **o mês daquele órgão tenha os números com que a
secretaria dimensiona e presta contas do atendimento e da merenda**.

O perfil do mês é a base numérica do mapa daquele mês: sem ele a unidade não tem quantos
são os parciais e os integrais de cada faixa, nem quantos almoços e jantares servir, e a
conferência do mês fica sem referência. É dele que sai também a quantidade de matriculados
que fica no cadastro do órgão. A tela inclui, altera, exclui e consulta esse perfil — mas
só serve meses de referência **anteriores a agosto de 2008**: de agosto de 2008 em diante o
sistema devolve o servidor à tela de onde ele veio, sem gravar nada. E ela abre de dois
modos: em **consulta**, quando quem a chama é a tela que abre o mês, e em **inclusão**, por
qualquer outro caminho — quem decide isso é a tela de origem, não o servidor.

## Contexto

Jornada S000M → M000M → M010T → M100T.

Ator: servidor de CRE — informa e confere o perfil mensal de atendimento de um órgão filho
da sua coordenadoria regional escolar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O M000M é um menu e não grava nada: apenas encaminha. O M010T, que abre o mês de
referência, **não é um menu** para esta tela: numa **consulta** de um mês anterior a agosto
de 2008 ela passa o controle direto para a M100T, deixando o órgão, a coordenadoria e o mês
que o servidor consultou e a marca de que foi ela a origem. É por isso que a M100T abre em
consulta — o modo de abertura é decidido por quem a chamou (RN-05). O corte de agosto de
2008 é do M010T e está na RN-02; o perfil que a M100T mantém é o do mapa antigo, e o que
ela entrega de volta à M010T está na RN-20.

As regras abaixo são só as da tela desta jornada. O contexto que a M100T usa — o **órgão
filho**, a **coordenadoria regional**, o **tipo de órgão** e a **matrícula** do servidor — é
o que a entrada deixou na sessão. As conferências de tela, de estação, de rota e de
permissão que a M100T executa antes de aceitar a operação são as mesmas de todas as telas e
já estão no documento da entrada: ficam no anexo de evidências, em **Regras que se
revelaram da entrada**. A jornada termina nesta tela.

---

## Regras de negócio

### RN-01 — A tela mantém o perfil do mês; não é só de consulta

A M100T inclui, altera, exclui e consulta o perfil mensal de atendimento de um órgão filho.
A **inclusão** cria o perfil e o total do mês; a **alteração** regrava o perfil com os novos
números e repõe a quantidade de matriculados no cadastro do órgão; a **exclusão** não apaga
o registro — marca-o como excluído, e o perfil sai das leituras; a **consulta** não grava
nada. Cada inclusão, alteração e exclusão deixa rastro na auditoria, com a operação, o valor
anterior e o valor novo; a consulta não deixa. Dos cadastros que a tela enxerga, dois ela
não mantém: o cadastro de segmentos, em que ela só cria e apaga os vínculos do órgão (RN-18),
e o cadastro de mapas do mês, que ela apenas procura (RN-14).

[?] A inclusão grava o total do mês do órgão, mas não repõe a quantidade de matriculados do
cadastro do órgão; a alteração faz o contrário — repõe o cadastro do órgão e não toca no
total do mês. Se as duas coisas deveriam andar juntas nas duas operações, pergunta ao site.

[?] Se a recusa encerra a operação sem gravar. As recusas interrompem a passagem de
conferência, e o que decide se a passagem de gravação ainda roda é uma marca de erro que a
rotina que mostra a mensagem deveria deixar; essa rotina não está no material lido, e a linha
que fecha a passagem de conferência foi uma das descartadas na expansão. Sem isso não se
decide se a recusa termina sem gravar ou se a gravação ainda acontece. Vale para todas as
recusas desta tela. Pergunta ao site.

### RN-02 — A tela só serve meses de referência anteriores a agosto de 2008

Informado um mês de referência de **agosto de 2008 em diante**, a tela não processa a
operação: devolve o servidor à tela que abriu o mês e encerra, sem gravar nada e sem mostrar
recusa. O perfil que ela mantém é o do **mapa antigo**, e é a tela que abre o mês que só a
aciona para os meses até **julho de 2008**.

[?] O corte de agosto de 2008 está fixo nos dois programas e separa o mapa antigo do novo,
mas o corpus não diz de onde vem essa data. Pergunta ao site.

### RN-03 — O que a tela chama de perfil do mês

O perfil do mês são **33 quantidades** informadas e **13 totais** que a tela calcula e mostra
sem guardar. As quantidades são: para cada uma das **sete faixas** de atendimento — Educação
Infantil, Progressão, Ensino Especial, Ciclo, 3ª/4ª séries, 5ª/8ª séries e PEJA —, os
matriculados **parciais** e os **integrais** e, em todas elas menos a Progressão, os
**almoços** e os **jantares**; fora das faixas, os **matriculados** do mês e o almoço e o
jantar lançados à parte delas; e, ainda, os quatro números de **residentes**: pais solteiros,
filhos solteiros, filhos "BI" e desassistidos. Os totais são o de cada faixa, o de parciais,
o de integrais, o geral, o de almoços, o de jantares e o de residentes.

Os títulos que a tela põe sobre quatro dessas faixas mudam com o mês de referência: até
**dezembro de 2006** são "Progressao", "Ciclo", "3a/4a Series" e "5a/8a Series"; de **janeiro
de 2007** em diante, "1o. Ciclo", "2o. Ciclo" e "3o. Ciclo".

O cabeçalho da tela traz a descrição do tipo de órgão e a data do sistema.

[?] O que significam o "BI" dos filhos residentes e a abreviação do almoço e do jantar
lançados fora das faixas: o corpus traz os rótulos abreviados e os nomes dos campos, e não a
explicação. Pergunta ao site.

[?] Por que os títulos das faixas mudam em janeiro de 2007: o corpus traz a data de corte e
não a razão. Pergunta ao site.

[?] De onde vêm a descrição do tipo de órgão e a data do sistema que o cabeçalho mostra: a
tela só as repassa do ambiente, e a única linha que lhes dá valor no corpus é a
inicialização em branco. Pergunta ao site.

### RN-04 — A situação do perfil: aberto ou fechado

A tela mostra a situação do perfil do mês — **ABERTO** ou **FECHADO** —, e é essa situação
que decide se a alteração e a exclusão passam (RN-11). O perfil que esta tela cria nasce
**fechado**, e toda alteração o grava **fechado** outra vez.

[?] Quem reabre o perfil do mês não é esta tela: no acervo, quem o reabre é a tela de
reabertura do mapa (M060T) e quem o fecha é a de fechamento (M050T), ambas fora desta
jornada. Se era para o perfil nascer aberto — ou para a alteração mantê-lo aberto —, o
caminho não o faz. Pergunta ao site.

### RN-05 — Como a tela abre depende de quem a chamou

Na abertura, a tela compara a **tela de origem** deixada na área de trabalho da sessão com a
**M010T**, a tela que abre o mês de referência, e o comportamento muda conforme a resposta:

- vinda da **M010T** numa consulta (RN-02), ela abre em **consulta**, já carregada com o
  órgão, a coordenadoria e o mês que aquela tela consultou, e mostra o perfil do mês. Se,
  ainda assim, a M010T não tiver deixado órgão nenhum, esta tela **encerra sem mostrar
  nada** — não abre em consulta nem em inclusão, não avisa o servidor e não grava;
- vinda de **qualquer outra origem** — o menu, ou qualquer tela que não seja a M010T —, ela
  abre em **inclusão**, em branco, com o **órgão** e a **coordenadoria** da sessão já
  preenchidos e com o nome do órgão (ou "não cadastrado", quando não o encontrar). Sem órgão
  na sessão, o cursor fica no campo do órgão.

Na abertura vinda da M010T, não havendo perfil para aquele órgão e mês, a tela avisa
**\* Perfil nao cadastrado para este Mes/Ano \***, passa sozinha para a **inclusão** e devolve
o cursor ao campo do órgão. Nas outras origens **nenhuma conferência é feita na abertura**:
a tela abre em inclusão, em branco, e só confere o que o servidor informar quando ele pedir a
operação. Isto não aparece em campo nenhum da tela — o modo de abertura não é escolhido pelo
servidor, e é a regra mais fácil de se perder, porque uma tela aberta em consulta onde
deveria abrir em inclusão não falha: só não deixa gravar.

[?] O que o servidor digita no campo da operação. A tela confere os códigos de inclusão,
alteração, exclusão e consulta, e nenhuma mensagem dela diz que sigla usar; o texto da
máscara não está no material lido. Pergunta ao site.

[?] Quando a tela chega a encerrar sem mostrar nada. Ela encerra na abertura vinda da tela
do mês quando aquela tela não deixa órgão nenhum, mas o material lido não mostra se ela pode
deixá-lo em branco: o caminho que a aciona já leu o cadastro do órgão antes de passar o
controle. Se a guarda vale para outro caso, ou se a passagem é inalcançável, pergunta ao
site.

### RN-06 — Só se trabalha no órgão do próprio vínculo

Quando a sessão define o **órgão filho** do servidor, informar outro é recusado com
**\* Usuario sem acesso a outro orgao \***. Quando a sessão tem **coordenadoria regional**, o
órgão é obrigatório — sem ele, **\* Informe o orgao \*** — e o órgão informado tem de ser
daquela coordenadoria, senão **\* Usuario sem acesso ao grupo deste orgao \***. Em qualquer
desses casos o cursor volta ao campo do órgão e nada é gravado.

### RN-07 — O órgão tem de estar cadastrado, ativo, não ser creche e ter os dados completos

A tela lê o cadastro do órgão pelo código informado. Não encontrado — ou marcado como
excluído —, a recusa é **\* Orgao nao cadastrado \***. O órgão tem ainda de estar **ativo**
(senão **\* Orgao cadastrado como inativo \***), **não pode ser creche** (senão
**\* Orgao cadastrado como Creche \***) e tem de ter os **seis** dados que o identificam — o
bairro, o órgão a que pertence, o nome, o endereço, o número de matriculados e o número de
pessoas; faltando qualquer um deles, **\* Orgao cadastrado com dados incompletos \***. E o
órgão tem de ser do mesmo tipo de órgão da sessão, isto é, da mesma secretaria: senão,
**\* Orgao nao pertence a esta secretaria \***. Em todas essas recusas o cursor volta ao
campo do órgão e nada é gravado.

### RN-08 — O mês e o ano de referência

O mês e o ano identificam o perfil do mês. Com os dois em branco, a recusa é
**\* Informe o Mes/Ano \***, com o cursor no campo do mês. O par tem de formar uma **data
válida**, tomada no dia 1, com o ano entre **1994** e **2099**: fora disso,
**\* Mes/Ano invalidos \***, com o cursor no mês. E o par tem de constar da **tabela de
períodos do mapa**: não constando,
**\* Mes/Ano nao cadastr.na tab.de periodos do mapa \***, também com o cursor no mês. É
dessa tabela que a tela tira o início e o limite do período que mostra.

[?] A primeira recusa olha os dois campos juntos — basta um deles preenchido para passar — e
as duas seguintes já barram o par incompleto; a mensagem e o cursor falam do mês nos três
casos. Se cada campo deveria ter a sua própria recusa, pergunta ao site.

### RN-09 — A inclusão recusa um perfil que já existe

Ao incluir, a tela procura o perfil do órgão naquele mês, **aberto ou fechado**; achando,
recusa com **\* Orgao com perfil ja cadastrado \***, com o cursor no campo do órgão, e nada é
gravado.

### RN-10 — O horário único de distribuição do almoço

A tela pede se há **horário único de distribuição do almoço**. A resposta tem de ser **S** ou
**N**; qualquer outra é recusada com
**\* Inf.horario unico distr de almoco com S ou N \***, com o cursor nesse campo, e nada é
gravado.

### RN-11 — A alteração e a exclusão exigem o perfil aberto

Alterar ou excluir um perfil **fechado** é recusado: **\* Perfil fechado. Reabra antes da
alteracao \*** na alteração, **\* Perfil fechado. Reabra antes da exclusao \*** na exclusão.
É preciso reabrir o mapa do mês antes, e quem o reabre é outra tela, fora desta jornada.

[?] O perfil que esta tela inclui já nasce fechado e toda alteração o grava fechado outra
vez, de modo que corrigir um número depois de incluir depende de outra tela reabrir o mapa.
Se era para o perfil nascer aberto, ou para a alteração mantê-lo aberto, o caminho não o faz.
Pergunta ao site.

### RN-12 — A alteração e a exclusão exigem ter consultado antes

Alterar ou excluir só vale para o **órgão** e o **mês** que a tela guardou da última
consulta. Informado outro órgão, ou outro mês, a recusa é **\* Consulte antes de alterar \***
ou **\* Consulte antes de excluir \***, com o cursor no campo da operação, e nada é gravado.
Trocar o órgão informado descarta o mês e o ano guardados, e depois de uma alteração o mês e
o ano guardados também são descartados: nos dois casos é preciso consultar de novo.

### RN-13 — Consultar um órgão sem perfil no mês é recusado

Consultar, alterar ou excluir um órgão num mês para o qual não existe perfil é recusado com
**\* Orgao sem perfil cadastrado para o Mes/Ano \***, com o cursor no campo do mês, e nada é
gravado.

### RN-14 — A exclusão é recusada quando o mês já tem mapas cadastrados

Antes de excluir, a tela procura os mapas do órgão naquele mês; achando algum, recusa com
**\* Ja existem mapas diarios cadastrados \***, com o cursor no campo da operação, e o
perfil não é excluído.

[?] O que a tela considera "mapas diários cadastrados": ela procura o mapa do mês pelo
órgão, pela coordenadoria e pelo mês com o **início do período zerado**, e quem cria esse
registro não é esta tela. Se a intenção era olhar os mapas diários do mês — que têm início de
período preenchido —, a chave usada é outra. Pergunta ao site.

### RN-15 — A exclusão marca o perfil como excluído

A exclusão **não apaga** o registro: marca-o como excluído, com quem excluiu, de onde e
quando, e o perfil deixa de ser encontrado nas leituras do mês. A rotina que apagaria o
registro de fato existe declarada no programa e nunca é executada em nenhum caminho.

### RN-16 — As quantidades de refeição têm de fechar com as do parcial

Informada uma faixa com parcial e sem almoço nem jantar, a recusa é
**\* Informe almoco ou jantar parcial \***; com almoço e jantar que não somam o parcial da
faixa, **\* Soma almoco e jantar difere de parcial \***; e com almoço ou jantar numa faixa
sem parcial, **\* Nao informe almoco ou jantar parcial \***. Nesses casos o cursor volta ao
almoço da faixa. Quando nenhuma quantidade do mês é informada, a recusa é
**\* Informe matriculados do mes para o perfil \***, com o cursor no parcial da Educação
Infantil.

Quando o mês tem parciais e nenhum integral — ou integrais e nenhum parcial —, a tela não
chega a conferir nada disso: ela **zera todos os almoços e jantares informados** e segue.

[?] Os dois caminhos não fecham: a tela manda informar almoço ou jantar para a faixa que tem
parcial e, ao mesmo tempo, zera esses mesmos almoços e jantares e pula as conferências de
refeição quando o mês não tem nenhum integral. Ou a limpeza vale para outro caso, ou a
exigência fica inalcançável nesse caso. Pergunta ao site.

### RN-17 — A consulta não grava nada

A consulta mostra o perfil do mês e os seus totais e **não grava nada**: nenhum cadastro é
gravado e nenhum rastro de auditoria é deixado. É ela que repõe o órgão e o mês guardados
para a alteração e a exclusão seguintes.

### RN-18 — Os vínculos do órgão com os segmentos acompanham as quantidades

Ao incluir ou alterar o perfil, a tela acerta os **vínculos do órgão com os segmentos de
atendimento**: para cada um dos quatro segmentos que ela controla, havendo números no grupo
correspondente, o vínculo é criado — marcado como **sem atendimento em sábado e domingo** —,
e não havendo, o vínculo é apagado. A criação e o apagamento deixam rastro na auditoria.

[?] O que são, em negócio, os quatro segmentos que a tela acerta: o corpus traz os códigos
01, 02, 09 e 10 e o cadastro de segmentos, mas não o conteúdo que diz o que cada código
significa. Pergunta ao site.

### RN-19 — Toda gravação deixa rastro na auditoria

Cada inclusão, alteração e exclusão do perfil, cada criação e cada apagamento de vínculo de
segmento e cada reposição do cadastro do órgão deixam um registro na auditoria, com o tipo de
órgão, o órgão, a tela, a operação, a matrícula, a estação, a data e a hora da sessão e o
valor anterior e o novo.

### RN-20 — O que a tela entrega à tela seguinte

Ao informar um mês de referência de **agosto de 2008 em diante**, esta tela não processa nada
e **entrega o mês à M010T**, a tela que abre o mês de referência (e é por isso que ela é
devolvida à tela de onde veio, como diz a RN-02):

- deixa no contexto o **órgão**, o nome dele, a **coordenadoria**, o **mês** e o **ano** e o
  **início e o limite do período**;
- deixa a operação em **consulta** quando o perfil do mapa novo já existe para aquele órgão e
  mês, e em **inclusão** quando não existe — e é com essa operação que a M010T abre, no órgão
  e no mês que esta tela deixou, em vez de voltar ao órgão da sessão;
- marca que a tela de origem é ela mesma, para que a M010T saiba preservar a operação.

Terminada uma **consulta** de um mês anterior ao corte, ela guarda o órgão, o ano e o mês
consultados e **reabre a si mesma**, já carregada com eles — é assim que a alteração e a
exclusão seguintes têm o órgão e o mês que elas exigem (RN-12).

---

## Cenários BDD

```gherkin
Funcionalidade: Manter o perfil mensal de atendimento do órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenadoria regional e o órgão filho do meu vínculo
    E tenho acesso à tela M100T

  Cenário: A tela abre em consulta quando vem da tela que abre o mês
    Dado que a tela que abre o mês me passou o controle numa consulta de um mês anterior a agosto de 2008
    E ela deixou o órgão, a coordenadoria e o mês que consultei
    Quando abro a tela M100T
    Então a tela abre em consulta, com o órgão, a coordenadoria e o mês que aquela tela deixou
    E vejo o perfil do mês, os seus totais e a situação dele

  Cenário: A tela abre em inclusão quando vem de qualquer outra origem
    Dado que chego à tela M100T por um caminho que não é a tela que abre o mês
    Quando abro a tela M100T
    Então a tela abre em inclusão, em branco
    E o órgão e a coordenadoria da minha sessão já vêm preenchidos
    E nenhuma conferência me é apresentada

  Cenário: A tela do mês não deixou órgão
    Dado que a tela que abre o mês me passou o controle sem deixar órgão nenhum
    Quando abro a tela M100T
    Então a tela encerra sem mostrar nada
    E nada é gravado

  Cenário: O mês não tem perfil e a tela passa a inclusão
    Dado que o órgão e o mês de referência não têm perfil cadastrado
    Quando abro a tela M100T pela tela que abriu o mês
    Então vejo "* Perfil nao cadastrado para este Mes/Ano *"
    E a operação fica em inclusão
    E o cursor fica no campo do órgão

  Cenário: O perfil do mês é consultado
    Dado que o órgão e o mês de referência têm perfil cadastrado
    Quando abro a tela M100T pela tela que abriu o mês
    Então vejo as 33 quantidades do perfil, os 13 totais calculados e a situação do perfil
    E a operação fica em consulta
    E nada é gravado e nenhum rastro de auditoria é deixado

  Cenário: O perfil do mês é incluído
    Dado que o órgão e o mês de referência não têm perfil cadastrado
    E o mês consta da tabela de períodos do mapa
    Quando informo as quantidades e o horário único de distribuição do almoço
    Então o perfil do mês é gravado, fechado
    E o total do mês do órgão é gravado
    E os vínculos do órgão com os segmentos são acertados conforme as quantidades
    E a inclusão deixa rastro na auditoria

  Cenário: O perfil do mês é alterado
    Dado que consultei o órgão e o mês de referência
    E o perfil está aberto
    Quando altero uma quantidade e peço a alteração
    Então o perfil é regravado com os novos números, fechado
    E a quantidade de matriculados do cadastro do órgão é reposta com o total do mês
    E a alteração deixa rastro na auditoria

  Cenário: O perfil do mês é excluído, sem apagar o registro
    Dado que consultei o órgão e o mês de referência
    E o perfil está aberto
    E o mês não tem mapas cadastrados
    Quando peço a exclusão
    Então o perfil passa a excluído e deixa de ser encontrado nas leituras do mês
    E a exclusão deixa rastro na auditoria

  Cenário: A tela só serve meses anteriores a agosto de 2008
    Dado que estou na tela M100T com o órgão consultado
    Quando informo um mês de referência de agosto de 2008 em diante
    Então a tela me devolve à tela que abriu o mês
    E nada é gravado

  Cenário: O mês de agosto de 2008 em diante é entregue à tela que abre o mês
    Dado que estou na tela M100T com o órgão consultado
    Quando informo um mês de referência de agosto de 2008 em diante
    Então a tela entrega à tela que abre o mês o órgão, o mês, o ano e o período do mês
    E a operação entregue é consulta quando o perfil do mapa novo já existe para aquele órgão e mês
    E a operação entregue é inclusão quando ele não existe
    E ela abre naquele órgão e naquele mês, e não no órgão da minha sessão

  Cenário: Depois de consultar, a tela se reabre com o que foi consultado
    Dado que consultei um mês de referência anterior a agosto de 2008
    Quando a consulta termina
    Então a tela se reabre com o órgão, o ano e o mês que consultei

  Cenário: A situação do perfil do mês
    Dado que o órgão e o mês têm perfil cadastrado e aberto
    Quando abro a tela M100T
    Então a situação mostrada é ABERTO
    E um perfil incluído por esta tela é gravado FECHADO

  Cenário: A inclusão de um perfil que já existe
    Dado que o órgão e o mês já têm perfil cadastrado, aberto ou fechado
    Quando tento incluir o perfil
    Então vejo "* Orgao com perfil ja cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Alterar um perfil fechado
    Dado que consultei o órgão e o mês de referência
    E o perfil está fechado
    Quando peço a alteração
    Então vejo "* Perfil fechado. Reabra antes da alteracao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Excluir um perfil fechado
    Dado que consultei o órgão e o mês de referência
    E o perfil está fechado
    Quando peço a exclusão
    Então vejo "* Perfil fechado. Reabra antes da exclusao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Alterar sem ter consultado
    Dado que o órgão ou o mês informados não são os da última consulta
    Quando peço a alteração
    Então vejo "* Consulte antes de alterar *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: Excluir sem ter consultado
    Dado que o órgão ou o mês informados não são os da última consulta
    Quando peço a exclusão
    Então vejo "* Consulte antes de excluir *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: Excluir com mapas cadastrados no mês
    Dado que consultei o órgão e o mês de referência
    E o perfil está aberto
    E o mês já tem mapa cadastrado
    Quando peço a exclusão
    Então vejo "* Ja existem mapas diarios cadastrados *"
    E o cursor fica no campo da operação
    E o perfil não é excluído

  Cenário: Consultar um órgão sem perfil no mês
    Dado que o órgão e o mês de referência não têm perfil cadastrado
    Quando peço a consulta
    Então vejo "* Orgao sem perfil cadastrado para o Mes/Ano *"
    E o cursor fica no campo do mês
    E nada é gravado

  Cenário: O órgão não é o do meu vínculo
    Dado que a minha sessão define o órgão filho do meu vínculo
    Quando informo outro órgão
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O órgão não é da minha coordenadoria
    Dado que a minha sessão tem uma coordenadoria regional
    Quando informo um órgão de outra coordenadoria
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Sem o órgão
    Dado que a minha sessão tem coordenadoria regional
    Quando deixo o órgão em branco
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão não cadastrado
    Dado que o órgão informado não existe no cadastro do órgão
    Quando tento trabalhar no perfil
    Então vejo "* Orgao nao cadastrado *"
    E nada é gravado

  Cenário: Órgão inativo
    Dado que o cadastro do órgão está marcado como inativo
    Quando tento trabalhar no perfil
    Então vejo "* Orgao cadastrado como inativo *"
    E nada é gravado

  Cenário: Órgão que é creche
    Dado que o cadastro do órgão está marcado como creche
    Quando tento trabalhar no perfil
    Então vejo "* Orgao cadastrado como Creche *"
    E nada é gravado

  Cenário: Órgão com dados incompletos
    Dado que o cadastro do órgão está sem o bairro, o órgão a que pertence, o nome, o endereço, os matriculados ou as pessoas
    Quando tento trabalhar no perfil
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E nada é gravado

  Cenário: Órgão de outra secretaria
    Dado que o órgão informado é de outro tipo de órgão
    Quando tento trabalhar no perfil
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E nada é gravado

  Cenário: Sem o mês e o ano de referência
    Dado que estou na tela M100T
    Quando deixo o mês e o ano em branco
    Então vejo "* Informe o Mes/Ano *"
    E o cursor fica no campo do mês
    E nada é gravado

  Cenário: Mês e ano que não formam uma data válida
    Dado que estou na tela M100T
    Quando informo um mês ou um ano inválido, ou um ano fora de 1994 a 2099
    Então vejo "* Mes/Ano invalidos *"
    E o cursor fica no campo do mês
    E nada é gravado

  Cenário: Mês fora da tabela de períodos do mapa
    Dado que o mês informado não consta da tabela de períodos do mapa
    Quando tento trabalhar no perfil
    Então vejo "* Mes/Ano nao cadastr.na tab.de periodos do mapa *"
    E o cursor fica no campo do mês
    E nada é gravado

  Cenário: Horário único de distribuição do almoço fora de S ou N
    Dado que estou informando o perfil do mês
    Quando informo nesse campo algo diferente de S ou N
    Então vejo "* Inf.horario unico distr de almoco com S ou N *"
    E o cursor fica nesse campo
    E nada é gravado

  Cenário: Faixa com parcial e sem almoço nem jantar
    Dado que o mês tem parciais e integrais informados
    E uma faixa tem parcial
    Quando deixo o almoço e o jantar dessa faixa em branco
    Então vejo "* Informe almoco ou jantar parcial *"
    E o cursor fica no almoço da faixa
    E nada é gravado

  Cenário: Almoço e jantar que não somam o parcial da faixa
    Dado que o mês tem parciais e integrais informados
    Quando o almoço mais o jantar de uma faixa não dá o parcial dela
    Então vejo "* Soma almoco e jantar difere de parcial *"
    E o cursor fica no almoço da faixa
    E nada é gravado

  Cenário: Almoço ou jantar numa faixa sem parcial
    Dado que o mês tem parciais e integrais informados
    Quando informo almoço ou jantar numa faixa que não tem parcial
    Então vejo "* Nao informe almoco ou jantar parcial *"
    E o cursor fica no almoço da faixa
    E nada é gravado

  Cenário: Nenhuma quantidade informada
    Dado que estou informando o perfil do mês
    Quando não informo nenhuma quantidade
    Então vejo "* Informe matriculados do mes para o perfil *"
    E o cursor fica no parcial da Educação Infantil
    E nada é gravado

  Cenário: Só parciais informados
    Dado que informo parciais e nenhum integral
    Quando peço a inclusão
    Então os almoços e jantares que informei são zerados
    E o perfil é gravado sem refeição
    E nenhuma conferência de refeição me é apresentada

  Cenário: Os vínculos do órgão com os segmentos acompanham as quantidades
    Dado que o órgão tem números numa faixa e nenhum em outra
    Quando peço a inclusão ou a alteração do perfil
    Então o vínculo do órgão com o segmento da faixa com números é criado, sem sábado e domingo
    E o vínculo do segmento da faixa sem números é apagado
    E as duas coisas deixam rastro na auditoria
```
