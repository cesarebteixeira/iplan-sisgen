# US — M010T — Lançar o perfil de atendimento do órgão filho por segmento e atendimento

## Estória

Como **servidor de CRE**, quero **lançar, alterar, excluir e consultar, para um órgão filho
e um mês de referência, o perfil de atendimento do mês — quantos parciais, integrais, 24
horas, almoços e jantares cada segmento e cada atendimento daquele órgão tem —**, para que
**o mês daquela unidade fique com os números com que a secretaria dimensiona a merenda e o
atendimento, e para que o mapa do mês possa ser aberto em cima deles**.

O perfil do mês é o que dá número ao mapa da unidade: sem ele não se sabe quantos parciais e
quantos integrais há em cada segmento, nem quantos almoços e jantares servir, e o mapa fica
sem de onde partir. É dele que saem o total de matriculados que fica no cadastro do órgão e
os números de pessoas por segmento e por tipo de refeição. É por isso que a tela só aceita
incluir o mês que ainda não tem perfil, e só aceita alterar e excluir enquanto o perfil
daquele mês está aberto.

## Contexto

Jornada S000M → M000M → M010T.

Ator: servidor de CRE — lança e confere o perfil de atendimento do mês de um órgão filho
(escola, creche ou outro órgão da rede) da sua coordenadoria regional escolar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O M000M é um menu e não grava nada: apenas
encaminha, e o mês que ele mostra não é passado a esta tela — quem informa o mês de
referência é o servidor, aqui. O que esta tela recebe de quem a abre está na RN-03 e na
RN-04; o que ela entrega à seguinte, na RN-23. As conferências de tela, de estação, de rota
e de permissão que a M010T executa antes de aceitar a operação são as mesmas de todas as
telas e já estão no documento da entrada: ficam no anexo de evidências, em **Regras que se
revelaram da entrada**.

---

## Regras de negócio

### RN-01 — A tela mantém o perfil de atendimento do mês; não é só de consulta

A M010T inclui, altera, exclui e consulta o perfil de atendimento de um órgão num mês de
referência. A **inclusão** cria o perfil do mês — o registro do mês e uma linha por
segmento e atendimento, com as quantidades — e, a partir dele, refaz os números derivados:
o total de matriculados do mês no cadastro do órgão, o número de pessoas por segmento e tipo
de refeição e os vínculos do órgão com os segmentos e com os grupos de atendimento. A
**alteração** regrava as linhas do mês e refaz os derivados. A **exclusão** apaga as linhas
do mês, o registro do mês e o guardado do mês anterior (RN-21). A **consulta** mostra o mês e
os seus números (RN-24).

[?] A tela não avisa o servidor quando grava: das mensagens que ela sabe mostrar, nenhuma é
de sucesso — todas são recusas. Confirmar com o site o que o operador deveria ver depois de
gravar, e o que aparece quando a gravação falha.

[?] A exclusão não confirma nada e apaga de fato: as linhas do mês e o registro do mês são
removidos, e não há marca de excluído a preservar como em outros cadastros. Se o perfil do
mês deveria ficar guardado para conferência depois de excluído, pergunta ao site.

### RN-02 — Só inclusão, alteração, exclusão e consulta são aceitas

A tela só trabalha em inclusão, alteração, exclusão ou consulta. Qualquer outro valor no
campo da operação é recusado com **\* Oper.nao disponivel. Use INC,ALT,EXC ou CON \***, com o
cursor de volta nesse campo, e nada é conferido nem gravado.

[?] A mensagem manda usar **INC**, **ALT**, **EXC** e **CON**, e o que a tela confere são os
códigos internos de inclusão, alteração, exclusão e consulta. O que a máscara mostra nesse
campo não está no material lido. Pergunta ao site.

### RN-03 — A tela abre com o órgão e a coordenadoria do servidor, e com o mês e a operação da última utilização

Ao abrir, a tela traz o **órgão filho** e a **coordenadoria regional** do servidor, tirados
da sessão, e repõe o **mês** e o **ano de referência** e a **operação** que ficaram guardados
da última utilização; chegando a operação em branco, ela repõe a **inclusão**. O cabeçalho
mostra o nome do órgão, a descrição do tipo de órgão da sessão, a data do sistema, o início e
o limite do período do mês, se o órgão é creche e a situação do perfil (**ABERTO** ou
**FECHADO**).

[?] Com que operação a tela reabre. A operação vem do que a última utilização deixou, e só é
reposta como inclusão quando chega em branco — de modo que a tela pode reabrir na consulta,
na alteração ou na exclusão anterior. Se era para abrir sempre em inclusão, pergunta ao site.

### RN-04 — Quem abre a tela decide como ela abre

Quando quem abre a M010T é a **tela do mapa do mês** (M040T), a M010T entra em **consulta**
do órgão e da coordenadoria que aquela tela deixou. Quando quem a abre é uma das telas do
perfil antigo (M100T ou M120T), a M010T descarta o último segmento e atendimento mostrados e
reabre com a operação e o órgão guardados. Aberta pelo menu, ela usa o órgão e a
coordenadoria da sessão e, não tendo a sessão órgão, pede o órgão ao servidor (RN-05).

### RN-05 — Só se mantém o perfil do órgão do próprio vínculo

Quando a sessão já define o **órgão filho** do servidor, informar outro é recusado com
**\* Usuario sem acesso a outro orgao \***. Faltando o órgão, a recusa é
**\* Informe o codigo do orgao \***. O órgão informado tem ainda de ser da **coordenadoria
regional** da sessão, senão **\* <- Usuario sem acesso ao grupo deste orgao \***, e, quando a
tela volta a ler o órgão para alterar, excluir ou consultar um mês que não é o que estava
guardado, a mesma conferência aparece como
**\* Usuario sem acesso ao grupo deste Orgao \***. Em qualquer desses casos o cursor volta ao
campo do órgão e nada é gravado.

### RN-06 — O órgão tem de estar cadastrado, ativo, completo e da mesma secretaria

O órgão informado é lido no cadastro do órgão. Não encontrado, a recusa é
**\* Orgao nao cadastrado \***. O órgão tem ainda de **não estar inativo**, senão
**\* Orgao cadastrado como inativo \***; tem de ter os **seis** dados que o identificam — o
bairro, o órgão a que pertence, o nome, o endereço, o número de matriculados e o número de
pessoas —, e faltando qualquer um deles a recusa é
**\* Orgao cadastrado com dados incompletos \***; e tem de ser do **mesmo tipo de órgão** da
sessão, isto é, da mesma secretaria, senão **\* Orgao nao pertence a esta secretaria \***.
Em todas essas recusas o cursor volta ao campo do órgão e nada é gravado.

[?] A tela lê o cadastro do órgão sem afastar o registro marcado como **excluído**: a marca
existe no cadastro do órgão e outras telas do acervo a conferem, e aqui ela só é copiada para
a auditoria. Se o órgão excluído deveria ser recusado, falta a conferência. Pergunta ao site.

### RN-07 — O mês e o ano de referência: obrigatórios, válidos, dentro do prazo e na tabela de períodos do mapa

Informar o mês e o ano de referência é obrigatório para incluir: sem eles, a recusa é
**\* Informe Mes/Ano \***, com o cursor no mês. O par tem de formar uma **data válida**,
tomada no dia 1, com o ano entre **1994** e **2099**: fora disso,
**\* Mes/Ano invalidos \***, com o cursor no mês. A inclusão só alcança o **mês corrente e o
mês seguinte**: um mês de referência depois disso é recusado com
**\* Mes do perfil indisponivel para inclusao \***, com o cursor no mês. E o par tem de
constar da **tabela de períodos do mapa**; não constando, a recusa é
**\* Mes/Ano nao cadastr.na tab.de periodos do mapa \***, também com o cursor no mês. É
dessa tabela que saem o início e o limite do período que a tela mostra.

[?] A conferência da tabela de períodos do mapa só acontece na inclusão de um mês que ainda
não é o que estava guardado: alterar, excluir e consultar não a refazem, e a inclusão do
mesmo mês da última utilização também a pula. Se a tabela deveria valer para toda operação,
pergunta ao site.

### RN-08 — A inclusão recusa o mês que já tem perfil

Ao incluir, a tela procura o perfil do órgão naquele mês, **aberto ou fechado**; achando,
recusa com **\* Perfil ja cadastrado para esta data \***, com o cursor no mês, e nada é
gravado.

[?] A procura só é feita quando o mês informado é diferente do mês que a última utilização
deixou guardado, e quando a primeira linha da grade traz um atendimento. Incluir outra vez o
mês que acabou de ser lido passa pela recusa e regrava o mês. Se era para recusar sempre,
pergunta ao site.

### RN-09 — Consultar, alterar e excluir exigem o perfil do mês cadastrado para o órgão

Consultar, alterar ou excluir um órgão num mês para o qual não existe perfil é recusado com
**\* Perfil nao cadastrado para este Orgao \***, com o cursor no campo do órgão, e nada é
gravado. Nesse caminho a tela também recusa o órgão que não é da coordenadoria da sessão
(RN-05).

### RN-10 — Alterar e excluir exigem ter consultado antes o mesmo órgão e mês

Alterar ou excluir só vale para o **órgão** e o **mês** que a tela guardou da última
consulta. Informado outro órgão, ou outro mês, a recusa é **\* Consulte antes de alterar \***
na alteração e **\* Consulte antes de excluir \*** na exclusão, com o cursor no campo do
órgão, e nada é gravado. Trocar a operação também descarta o que estava guardado.

### RN-11 — Alterar e excluir só valem com o perfil aberto

Alterar ou excluir um mês cujo perfil está **fechado** é recusado com
**\* Perfil fechado para este Mes/Ano \***, com o cursor no mês, e nada é gravado; a mesma
situação ainda é conferida mais adiante como **\* Perfil fechado para esta data \***.

[?] O perfil que esta tela cria nasce **fechado**, e toda gravação o deixa fechado outra
vez, de modo que corrigir um número depois de incluir depende de outra tela reabrir o mapa
do mês — que não é desta jornada. Se era para o perfil nascer aberto, ou para a alteração
mantê-lo aberto, o caminho não o faz. Pergunta ao site.

[?] A segunda recusa — "para esta data" — fica inalcançável por este caminho: quando a tela
chega nela, a primeira já garantiu que a situação lida não é a de fechado. Ou a segunda vale
para outro caso, ou é resíduo. Pergunta ao site.

### RN-12 — A exclusão é recusada quando o mapa do mês já está cadastrado

Antes de excluir, a tela procura o **mapa do mês** daquele órgão; achando, recusa com
**\* Nao exclua o perfil. Mapa ja cadastrado \***, com o cursor no mês, e o perfil não é
excluído. É preciso desfazer o mapa do mês noutra tela antes de excluir o perfil.

[?] A procura do mapa é feita pela data de **início do período** do mês, e quem cria os
mapas do mês é a tela do mapa (M040T), que os grava por dia. Se a leitura casa o registro
exato ou apenas se posiciona no começo da chave depende de sinalizadores de leitura que não
têm valor nos fontes; se ela só casa exatamente, a recusa alcança apenas o mapa lançado
justamente no primeiro dia do período. Pergunta ao site.

### RN-13 — O horário único de distribuição do almoço tem de ser S ou N

A tela pergunta se há **horário único de distribuição do almoço**. A resposta tem de ser
**S** ou **N**; qualquer outra é recusada com
**\* Inf.horario unico distr de almoco com S ou N \***, com o cursor nesse campo, e nada é
gravado.

### RN-14 — O perfil é lançado em linhas de segmento e atendimento, treze por página

O perfil do mês é lançado em linhas, e cada linha é um par de **segmento** e **atendimento**
do órgão, com as quantidades de **parciais**, **integrais**, **24 horas**, **almoços** e
**jantares**. A tela mostra **treze** linhas por vez e pede a página seguinte ao ambiente
quando o servidor avança. Cada linha mostra ainda a descrição do segmento, a descrição do
atendimento e o **total** da linha, que é a soma das três quantidades de refeição.

[?] A grade é montada a partir do catálogo de atendimentos do tipo de órgão: a tela mostra
os atendimentos **ativos** daquele tipo cujo segmento é um dos segmentos do órgão ou que já
têm perfil no mês, e para no primeiro atendimento ativo que não é do órgão nem tem perfil,
avisando **\* Perfil nao cadastrado para esta data \***. Se o aviso deveria falar do perfil
do órgão, e não interromper a grade, pergunta ao site.

### RN-15 — Cada tipo de refeição informado tem de ser admitido pelo atendimento

Informada uma quantidade de **parciais**, o atendimento daquela linha tem de admitir
horário parcial; senão a recusa é **\* Atendimento nao cadastrado - horario parcial \***.
O mesmo vale para **integrais**, com **\* Atendimento nao cadastrado - horario integral \***,
e para **24 horas**, com **\* Atendimento nao cadastrado - horario 24 H \***. O cursor volta
ao campo da quantidade recusada e nada é gravado.

[?] A tela lê o cadastro de atendimentos e segue adiante mesmo quando não o encontra: a
leitura vazia não tem recusa própria, e as três recusas acima saem do que a linha do
atendimento diz admitir. Se o atendimento inexistente deveria recusar por si, falta a
recusa. Pergunta ao site.

### RN-16 — As refeições têm de fechar com os parciais

Antes de conferir, a tela ajusta as refeições da linha: a linha **sem nenhum parcial** tem o
almoço e o jantar **zerados**; a linha que traz parciais, não traz integrais e não trouxe
almoço nem jantar tem **todo o parcial lançado no almoço**, com o jantar zerado. Depois
disso, uma linha com parciais e **nenhuma refeição** é recusada com
**\* Informe almoco ou jantar parcial \***, com o cursor no almoço; e uma linha cujo almoço e
jantar **não somam** os parciais é recusada com
**\* Soma almoco e jantar difere da parcial \***, também com o cursor no almoço.

[?] Quando o ajuste automático se aplica — parciais sem integrais e sem refeição informada —,
a linha nunca chega à recusa de "informe almoço ou jantar": o parcial vira almoço e a soma
fecha. A recusa alcança, então, sobretudo a linha que traz parciais e integrais juntos. Se
era para a recusa valer para toda linha com parcial e sem refeição, o ajuste a impede.
Pergunta ao site.

### RN-17 — A tela fecha o perfil do mês anterior ao incluir

Passando as conferências, uma inclusão procura o perfil do **mês anterior** daquele órgão e,
achando-o **aberto**, marca-o como **fechado**. Esse fechamento acontece antes da gravação
do mês novo.

[?] O fechamento procura o mês anterior apenas na situação **ABERTO**, e o perfil que esta
tela grava nasce **FECHADO** (RN-11): se a intenção era fechar o mês anterior sempre, o
caminho só o alcança quando outra tela o reabriu. Pergunta ao site.

### RN-18 — A tela repõe o total do mês no cadastro do órgão

Ao incluir ou alterar o perfil, a tela soma as quantidades de parciais, integrais e 24 horas
das linhas do mês. Esse total é reposto no **número de matriculados do cadastro do órgão** —
mas só quando o mês de referência é o **mês corrente** do sistema — e no número de
matriculados do cadastro do órgão por mês, que é atualizado quando existe e criado quando não
existe.

[?] O número de pessoas do cadastro do órgão por mês é montado com zero e o zero não chega a
ser gravado: a rotina de gravação só copia os campos que chegam com valor diferente de zero.
Se ele deveria ser gravado, o caminho não o faz. E se o número de matriculados do cadastro do
órgão deveria ser reposto também nos meses de referência que não são o mês corrente, pergunta
ao site.

### RN-19 — A tela acerta o número de pessoas por segmento e tipo de refeição

Para cada **segmento** que o órgão atende, a tela soma as quantidades do perfil daquele mês,
aplica sobre esse total a cota de refeições por pessoa do segmento e compara o resultado com
o número de pessoas já cadastrado para aquele segmento e tipo de refeição: **não superando**,
o vínculo daquele segmento e tipo de refeição é marcado como **inativo**, com a data e a
matrícula de quem o alterou; superando, é marcado como **ativo**. Num órgão que é **creche**,
os dois segmentos de funcionários entram nessa conta à parte.

[?] De onde vêm a **cota de refeições por pessoa** do segmento e o que o tipo de refeição do
vínculo representa: o corpus traz a cota em centésimos, dividida por cem, e os cadastros de
cota por segmento, órgão e faixa de pessoas, sem o significado de negócio. Pergunta ao site.

### RN-20 — A tela acerta os vínculos do órgão com os segmentos e os grupos de atendimento

Ao incluir ou alterar o perfil, a tela garante o **vínculo do órgão com cada segmento** que
tem números no perfil do mês, marcando-o como sem atendimento em sábado e domingo, e o
**vínculo do órgão com cada grupo de atendimento** que aparece no perfil. A criação de cada
vínculo deixa rastro na auditoria.

[?] Esta tela só cria vínculos: as rotinas que apagariam o vínculo do órgão com o segmento e
com o grupo de atendimento existem declaradas no programa e não são executadas em caminho
nenhum. Se o vínculo deveria ser apagado quando o segmento deixa de ter números, falta o
apagamento. Pergunta ao site.

### RN-21 — A tela guarda e apaga, para o mês anterior, o número de pessoas por segmento

Ao incluir, a tela apaga o que estava guardado, para o **mês anterior** daquele órgão, sobre
o número de pessoas por segmento, e regrava esse guardado a partir dos números do mês
anterior. A exclusão também apaga o guardado do mês anterior; a alteração não o toca.

[?] O que é, em negócio, esse guardado do mês anterior: o corpus mostra o cadastro, os
campos que ele leva (segmento, tipo de refeição, número de pessoas, data e matrícula de quem
atualizou) e as duas operações, mas não o seu nome nem a sua finalidade. Pergunta ao site.

[?] Por que a alteração não regrava o guardado, e por que a exclusão o apaga sem regravar
nada: se ele é o retrato do mês anterior, a exclusão do mês seguinte o deixa sem retrato.
Pergunta ao site.

### RN-22 — Cada gravação deixa rastro na auditoria

Cada gravação que a tela faz deixa um registro na **auditoria**: o tipo de órgão, a
coordenadoria, a tela, a operação, a matrícula, a estação, o dia, o mês e a hora da sessão, a
tela auditada e o **valor anterior** e o **valor novo**. São **vinte e duas** as passagens
que gravam auditoria no caminho da tela, e a consulta não é uma delas.

[?] A auditoria da exclusão de linha do perfil grava o valor anterior e o novo, e a da
criação de vínculo grava o valor novo; o que o operador vê quando a gravação de auditoria
falha não está nos fontes desta jornada. Pergunta ao site.

### RN-23 — A tela entrega o mês à tela do mapa, e passa à tela do perfil antigo na consulta de mês antigo

Terminada a operação, a M010T deixa no contexto o **órgão**, a **coordenadoria**, o **mês de
referência** e a operação em **inclusão**, com o **mapa do mês zerado**, e passa para a
**tela do mapa do mês** (M040T) — que abre, por isso, para incluir o mapa daquele órgão
naquele mês. É por essa passagem que a jornada continua.

Numa **consulta** de um mês de referência **anterior a agosto de 2008**, a M010T não processa
o mês: ela deixa no contexto o órgão, a coordenadoria e o mês, marca que veio da tela do
perfil antigo e passa para a **M100T**, que é a tela que mantém o perfil do mapa antigo. O
corte é **agosto de 2008**.

[?] A passagem para a tela do mapa depende de um campo de um caractere da própria tela, que
a tela **limpa** ao abrir e nunca preenche; a passagem alternativa, na passagem de
conferência, exige uma marca de erro que só é escrita nos caminhos que já encerraram a
operação. Por esses dois caminhos a tela do mapa não é aberta. Se era para ela ser aberta,
pergunta ao site.

[?] O corte de agosto de 2008 está fixo no programa e separa o mapa antigo do novo, mas o
corpus não diz de onde vem essa data. Pergunta ao site.

### RN-24 — A consulta mostra o mês e não grava nada

A consulta mostra a grade do mês — treze linhas por vez, com o segmento, o atendimento, as
quantidades e o total da linha — e o cabeçalho do mês; não grava nenhum cadastro e não deixa
rastro de auditoria. É ela que repõe o órgão, o mês e a operação que a alteração e a
exclusão seguintes exigem.

[?] A consulta não é inofensiva: ela termina no mesmo caminho que apaga as linhas do mês
cujas quantidades estejam todas zeradas — e, não sobrando linha nenhuma, o registro do mês.
Se a leitura que decide isso casa o registro exato ou apenas se posiciona no começo do mês
depende dos mesmos sinalizadores de leitura, que não têm valor nos fontes; se ela se
posiciona, uma consulta apaga. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Perfil de atendimento do mês de referência de um órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenadoria regional e o órgão filho do meu vínculo
    E tenho acesso à tela M010T

  Cenário: O perfil do mês é incluído
    Dado que o órgão e o mês de referência não têm perfil
    E o mês consta da tabela de períodos do mapa
    E o mês não passa do mês seguinte ao corrente
    Quando informo uma linha com o segmento, o atendimento, os parciais e as refeições e peço a inclusão
    Então o perfil do mês é gravado, com uma linha por segmento e atendimento
    E o total do mês é regravado no cadastro do órgão por mês
    E, sendo o mês de referência o mês corrente, o total do mês é reposto no número de matriculados do cadastro do órgão
    E os números de pessoas por segmento e tipo de refeição são acertados
    E os vínculos do órgão com os segmentos e os grupos de atendimento são criados
    E a inclusão deixa rastro na auditoria

  Cenário: O perfil do mês é alterado
    Dado que consultei o órgão e o mês de referência
    Quando altero uma quantidade e peço a alteração
    Então o perfil do mês é regravado com os novos números
    E o total do mês é regravado no cadastro do órgão por mês
    E, sendo o mês de referência o mês corrente, o total do mês é reposto no número de matriculados do cadastro do órgão
    E a alteração deixa rastro na auditoria

  Cenário: O perfil do mês é excluído
    Dado que consultei o órgão e o mês de referência
    E o perfil está aberto
    E o mapa daquele mês não está cadastrado
    Quando peço a exclusão
    Então as linhas do mês e o registro do mês são apagados
    E o guardado do mês anterior sobre o número de pessoas por segmento também é apagado
    E a exclusão deixa rastro na auditoria

  Cenário: A consulta mostra o perfil do mês e não grava nada
    Dado que o órgão e o mês de referência têm perfil cadastrado
    Quando consulto o mês
    Então vejo a grade do mês, com o segmento, o atendimento, as quantidades e o total de cada linha
    E vejo o nome do órgão, o período do mês e a situação do perfil
    E nada é gravado e nenhum rastro de auditoria é deixado

  Cenário: A consulta de um mês anterior a agosto de 2008 passa para a tela do perfil antigo
    Dado que o mês de referência é anterior a agosto de 2008
    Quando consulto o mês
    Então a tela do perfil antigo, a M100T, abre com o órgão, a coordenadoria e o mês
    E nada é gravado nesta tela

  Cenário: A tela entrega o mês à tela do mapa do mês
    Dado que a operação terminou, sem nenhuma recusa
    Quando a tela segue para a tela seguinte
    Então a tela do mapa, a M040T, abre com o órgão, a coordenadoria e o mês de referência
    E ela abre em inclusão, com o mapa do mês zerado

  Cenário: A tela fecha o perfil do mês anterior ao incluir
    Dado que o mês anterior daquele órgão está aberto
    Quando incluo o perfil do mês
    Então o perfil do mês anterior passa a fechado
    E isso acontece antes da gravação do mês novo

  Cenário: A tela regrava o número de pessoas por segmento do mês anterior
    Dado que o mês anterior daquele órgão tem números por segmento guardados
    Quando incluo o perfil do mês
    Então o que estava guardado para o mês anterior é apagado e regravado
    E o regravo leva o número de pessoas por segmento do mês anterior

  Cenário: Operação diferente de inclusão, alteração, exclusão e consulta é recusada
    Dado que estou na tela M010T
    Quando a tela chega com uma operação que não é inclusão, alteração, exclusão nem consulta
    Então vejo "* Oper.nao disponivel. Use INC,ALT,EXC ou CON *"
    E o cursor fica no campo da operação
    E nada é conferido e nada é gravado

  Cenário: O órgão informado não é o do meu vínculo
    Dado que a minha sessão define o órgão filho do meu vínculo
    Quando informo outro órgão
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Sem o órgão
    Dado que a minha sessão não define o órgão filho
    Quando deixo o órgão em branco
    Então vejo "* Informe o codigo do orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O órgão é de outra coordenadoria
    Dado que a minha sessão tem uma coordenadoria regional
    Quando informo um órgão que não é daquela coordenadoria
    Então vejo "* <- Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O órgão não é da coordenadoria da sessão, já com o mês informado
    Dado que informei um mês que não é o que estava guardado
    Quando o órgão informado é de outra coordenadoria
    Então vejo "* Usuario sem acesso ao grupo deste Orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O órgão não está cadastrado
    Dado que o órgão informado não existe no cadastro do órgão
    Quando tento incluir o perfil do mês
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O órgão está inativo
    Dado que o cadastro do órgão informado está marcado como inativo
    Quando tento incluir o perfil do mês
    Então vejo "* Orgao cadastrado como inativo *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O órgão está com os dados incompletos
    Dado que o cadastro do órgão está sem o bairro, o órgão pai, o nome, o endereço, os matriculados ou as pessoas
    Quando tento incluir o perfil do mês
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: O órgão é de outra secretaria
    Dado que o órgão informado é de outro tipo de órgão
    Quando tento incluir o perfil do mês
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Sem o mês e o ano de referência
    Dado que estou incluindo o perfil do mês
    Quando deixo o mês e o ano em branco
    Então vejo "* Informe Mes/Ano *"
    E o cursor fica no mês
    E nada é gravado

  Cenário: Mês e ano que não formam uma data válida
    Dado que estou incluindo o perfil do mês
    Quando informo um mês ou um ano inválido, ou um ano fora de 1994 a 2099
    Então vejo "* Mes/Ano invalidos *"
    E o cursor fica no mês
    E nada é gravado

  Cenário: Mês de referência depois do mês seguinte
    Dado que estou incluindo o perfil do mês
    Quando informo um mês de referência posterior ao mês seguinte ao corrente
    Então vejo "* Mes do perfil indisponivel para inclusao *"
    E o cursor fica no mês
    E nada é gravado

  Cenário: Mês fora da tabela de períodos do mapa
    Dado que o mês informado não existe na tabela de períodos do mapa
    Quando tento incluir o perfil do mês
    Então vejo "* Mes/Ano nao cadastr.na tab.de periodos do mapa *"
    E o cursor fica no mês
    E nada é gravado

  Cenário: Inclusão de um mês que já tem perfil
    Dado que o órgão já tem perfil naquele mês
    Quando tento incluir o perfil do mês
    Então vejo "* Perfil ja cadastrado para esta data *"
    E o cursor fica no mês
    E nada é gravado

  Cenário: O mês não tem perfil para o órgão
    Dado que o órgão não tem perfil naquele mês
    Quando consulto, altero ou excluo o mês
    Então vejo "* Perfil nao cadastrado para este Orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Alterar sem ter consultado antes
    Dado que o órgão ou o mês que estão na tela não são os da última consulta
    Quando tento alterar o perfil
    Então vejo "* Consulte antes de alterar *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Excluir sem ter consultado antes
    Dado que o órgão ou o mês que estão na tela não são os da última consulta
    Quando tento excluir o perfil
    Então vejo "* Consulte antes de excluir *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Alterar ou excluir um perfil fechado
    Dado que consultei o órgão e o mês de referência
    E o perfil daquele mês está fechado
    Quando tento alterar ou excluir o perfil
    Então vejo "* Perfil fechado para este Mes/Ano *"
    E o cursor fica no mês
    E nada é gravado

  Cenário: Excluir um mês que já tem mapa cadastrado
    Dado que consultei o órgão e o mês de referência
    E o perfil está aberto
    Quando tento excluir o perfil de um mês que já tem o mapa cadastrado
    Então vejo "* Nao exclua o perfil. Mapa ja cadastrado *"
    E o cursor fica no mês
    E o perfil não é excluído

  Cenário: Horário único de distribuição do almoço fora de S e N
    Dado que estou incluindo ou alterando o perfil do mês
    Quando informo no horário único de distribuição do almoço algo que não é S nem N
    Então vejo "* Inf.horario unico distr de almoco com S ou N *"
    E o cursor fica nesse campo
    E nada é gravado

  Cenário: A grade para num atendimento sem perfil para a data
    Dado que o tipo de órgão tem um atendimento ativo que não é de um segmento do órgão
    E esse atendimento não tem perfil no mês
    Quando abro a tela M010T
    Então vejo "* Perfil nao cadastrado para esta data *"
    E a grade para nesse atendimento

  Cenário: Parciais informados num atendimento que não admite horário parcial
    Dado que estou lançando uma linha do perfil
    Quando informo parciais num atendimento que não admite horário parcial
    Então vejo "* Atendimento nao cadastrado - horario parcial *"
    E o cursor fica no campo dos parciais
    E nada é gravado

  Cenário: Integrais informados num atendimento que não admite horário integral
    Dado que estou lançando uma linha do perfil
    Quando informo integrais num atendimento que não admite horário integral
    Então vejo "* Atendimento nao cadastrado - horario integral *"
    E o cursor fica no campo dos integrais
    E nada é gravado

  Cenário: 24 horas informadas num atendimento que não admite esse horário
    Dado que estou lançando uma linha do perfil
    Quando informo 24 horas num atendimento que não admite esse horário
    Então vejo "* Atendimento nao cadastrado - horario 24 H *"
    E o cursor fica no campo das 24 horas
    E nada é gravado

  Cenário: Parciais e integrais sem almoço nem jantar
    Dado que estou lançando uma linha do perfil
    Quando informo parciais e integrais e não informo nenhum almoço nem jantar
    Então vejo "* Informe almoco ou jantar parcial *"
    E o cursor fica no almoço
    E nada é gravado

  Cenário: Parciais sem integrais e sem refeição informada
    Dado que estou lançando uma linha do perfil
    Quando informo os parciais e não informo integrais, almoço nem jantar
    Então o total de parciais é lançado no almoço da linha
    E o jantar da linha fica zerado
    E a linha passa nas conferências de refeição

  Cenário: Almoço e jantar que não somam os parciais
    Dado que estou lançando uma linha do perfil
    Quando o almoço e o jantar somados não fecham com os parciais da linha
    Então vejo "* Soma almoco e jantar difere da parcial *"
    E o cursor fica no almoço
    E nada é gravado

  Cenário: Nada é gravado enquanto alguma conferência recusar
    Dado que estou lançando o perfil do mês
    Quando qualquer conferência da tela recusa o que informei
    Então nenhuma linha do perfil é gravada
    E nenhum número derivado é acertado
    E nenhum rastro de auditoria é deixado
```
