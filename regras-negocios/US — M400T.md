# US — M400T — Manter o mapa diário de atendimento do órgão filho

## Estória

Como **servidor da CRE**, quero **registrar e conferir o mapa diário de atendimento
de um órgão filho — o cardápio e as quantidades de refeições de um dia de um mês de
referência**, para que **aquele dia fique com os números do atendimento e da
merenda, que são a base da prestação de contas da secretaria**.

O mapa de cada dia é a peça que fecha o mês do órgão: é dele que saem as refeições
servidas dia a dia, e sem ele o mês não tem como ser conferido. Informar a
quantidade sem o cardápio correspondente — ou o cardápio sem quantidade — deixaria
o dia incompleto, e passar dos números previstos no perfil do mês faria a conta
estourar. Quando não houve atendimento, a ausência precisa ficar explicada por um
motivo e, em um dos casos, por uma justificativa cadastrada. Esta tela atende os
dias até julho de 2008 e os órgãos que não são creche; de agosto de 2008 em diante
o mapa do dia é o de outra tela, e é a tela anterior que faz a separação.

## Contexto

Jornada S000M → M000M → M040T → M400T.

Ator: servidor de CRE — registra e confere o mapa diário de atendimento de um órgão
filho da sua coordenadoria regional escolar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O `M000M` é um menu e não grava nada: só encaminha. O `M040T` não é menu: é a tela
que escolhe o dia do mapa e que encadeia, sem passar por menu nenhum, para esta
tela. O que ela deixa na sessão — o órgão filho, a coordenadoria regional, o mês e o
ano de referência e o dia escolhidos — é o que esta tela aproveita ao abrir (RN-01).
É também a `M040T` que separa a creche dos demais órgãos: a creche vai para a
`M420T`, os demais vêm para cá (RN-04). A jornada termina nesta tela.

Esta tela também encadeia de volta, sem menu, em dois momentos. Ao fim da
**consulta** ela reabre a si mesma, deixando o dia consultado na sessão. E devolve à
`M040T` — levando a operação, o dia, o início e o limite do período e a semana — nos
dois casos em que precisa que o dia seja escolhido de novo: quando o dia informado
é de 1º de agosto de 2008 em diante (RN-04) e quando a inclusão chega sem nenhum dia
informado. Não é um passo novo da jornada: é a retomada da escolha do dia.

As conferências de tela, de estação, de rota e de permissão que esta tela executa
antes de aceitar a operação são as mesmas de todas as telas e já estão no documento
da entrada: ficam no anexo de evidências, em **Regras que se revelaram da entrada**.

---

## Regras de negócio

### RN-01 — De onde a tela vem decide com que dia e em que operação ela abre

A tela é aberta pela tela que escolhe o dia do mapa. Vindo dela, a tela encontra na
sessão o órgão filho, a coordenadoria regional e o dia escolhidos, e abre assim: **em
consulta**, quando aquele dia já tem mapa — mostrando a situação e o que o dia tem
gravado; **em inclusão**, quando ainda não tem, com o dia em aberto. Vindo por
qualquer outro caminho, ela abre sempre **em inclusão**, com o órgão do vínculo do
servidor, e não aproveita nenhum dia escolhido antes.

[?] A tela pergunta quem a abriu para decidir se aproveita o dia deixado na sessão;
se a resposta for "não foi a tela que escolhe o dia", ela força a inclusão. Como a
jornada só a alcança por essa tela, não se sabe em que situação o outro caminho
acontece, nem se ele é alcançável na prática. Pergunta ao site.

### RN-02 — A tela inclui, altera, exclui e consulta o mapa do dia — e a exclusão não apaga

A tela faz quatro operações sobre o mapa do dia: **incluir** (cria o mapa do dia,
aberto), **alterar** (regrava cardápios e quantidades), **excluir** e **consultar**.
A exclusão **não apaga o registro**: marca-o como excluído, e daí em diante aquele
dia deixa de ser encontrado nas leituras; a consulta não grava nada (RN-16).
Inclusão, alteração e exclusão deixam rastro na auditoria (RN-17).

A tela enxerga treze cadastros, mas **só dois recebem gravação**: o mapa do dia e a
auditoria. A rotina de apagar existe para os treze e **não é chamada por caminho
nenhum**. Na exclusão a tela não confere cardápios, quantidades nem justificativa:
exige o órgão apto, o dia dentro do período, o mapa existente e aberto e que o dia
tenha sido consultado (RN-10, RN-11).

[?] A recusa mostra a mensagem e encerra a passagem, mas quem decide se a passagem de
gravação roda depois é um marcador de erro do sistema, e a rotina comum que mostra a
mensagem não está no acervo — ela é uma entrada de biblioteca, sem definição em
fonte algum. Nenhuma recusa desta tela marca esse erro; se a rotina comum não
marcar, a gravação acontece apesar da recusa. Pergunta ao site.

### RN-03 — O que o mapa do dia registra e como a tela o mostra

O mapa é de **um órgão, um mês de referência e um dia**. Para **sete refeições**, a
tela guarda o **código do cardápio** e as **quantidades**, separadas entre educação
infantil e outras séries, nas formas parcial e integral, e ainda residentes,
funcionários e uma quantidade que a tela rotula PEJA. Guarda também **quatro
cardápios extras**, com as sobremesas. Ao todo são **33 quantidades** e **11 códigos
de cardápio**, em **57 campos identificados por nome** na máscara — contei os 57
nomes de campo que o programa manda para a máscara. A tela mostra ainda se o mapa
está **aberto** ou **fechado**, o dia da semana e o início e o limite do período do
mês. Quando não houve atendimento, o mapa guarda também o motivo (RN-15).

[?] O significado de cada grupo e de cada rótulo — o PEJA, o que distingue os dois
lanches e o que são as letras das formas parcial e integral — não está no acervo: ele
traz o nome do campo, não o que ele significa em negócio. Pergunta ao site.

### RN-04 — A tela só serve dias até julho de 2008 e órgãos que não são creche

A tela só trabalha com dias **até 31 de julho de 2008**: informado um dia de 1º de
agosto de 2008 em diante, ela não processa — devolve o servidor à tela que escolhe o
dia e encerra, sem gravar nada, em qualquer das quatro operações. E o órgão **não
pode estar cadastrado como creche**: nesse caso a recusa é * Orgao cadastrado como
creche *. Quem separa os dois casos é a tela que escolhe o dia: ela manda a creche
para a `M420T` e os demais órgãos para esta tela.

[?] O corte é uma data gravada com o dia zero (20080800), o que na prática barra de
1º de agosto de 2008 em diante. Se a intenção era outro dia — por exemplo, 31 de
julho —, o número gravado não a expressa. Pergunta ao site.

### RN-05 — O órgão tem de ser o do servidor e estar apto

Antes de qualquer operação, a tela confere o órgão: se o órgão informado é o do
vínculo do servidor — senão * Usuario sem acesso a outro orgao *; se está cadastrado
— * Orgao nao cadastrado *; se está ativo — * Orgao cadastrado como inativo *; se
não é creche — * Orgao cadastrado como creche *; se tem os dados completos (bairro,
órgão pai, nome, endereço, matriculados e pessoas) — * Orgao cadastrado com dados
incompletos *; se é da secretaria da sessão — * Orgao nao pertence a esta secretaria
*; e se o servidor tem acesso à coordenadoria regional do órgão — * Usuario sem
acesso ao grupo deste orgao *. Sem órgão informado, a tela pede * Informe o orgao *.

### RN-06 — O mês de referência e o dia têm de estar no período do mapa

O mês e o ano de referência têm de estar informados e válidos, e o mês tem de constar
da **tabela de períodos do mapa**, que define o início e o limite do período. O dia
do mapa também: precisa ser uma data válida, **não pode ser posterior à data de
hoje** e tem de cair **dentro do intervalo do período**. Faltando o mês ou o ano, a
tela pede * Informe o Mes/Ano *; faltando o dia, * Informe o Dia/Mes *; data de mês
ou ano impossível, * Mes/Ano invalidos *; mês fora da tabela, * Mes/Ano nao
cadastr.na tab.de periodos do mapa *; dia impossível, * Dia/Mes invalidos *; data
futura, * Data do mapa maior que data atual *; fora do período, * Dia/Mes fora do
intervalo do periodo *.

### RN-07 — A semana do dia vem do calendário de semanas do órgão

A semana do mapa (A, B, C ou D) é a que o **calendário de semanas do órgão** define
para o dia escolhido. Se o operador não informar a semana, o sistema a preenche com a
do calendário; se informar outra, recusa com * <- Informe semana correta *.

### RN-08 — O mês tem de ter perfil cadastrado para o órgão

A inclusão e a alteração exigem que o **mês tenha perfil de atendimento cadastrado
para o órgão** — aberto ou fechado. Não havendo, a operação é recusada com * Nao
existe perfil cadastrado para o Orgao *. A exclusão não faz essa conferência.

### RN-09 — A inclusão recusa um dia que já tem mapa

A inclusão é recusada se **já existir mapa para aquele dia**: * Mapa ja cadastrado
para este Dia/Mes *. A conferência não enxerga os mapas já marcados como excluídos.

[?] A exclusão marca o mapa como excluído sem mexer nos campos que identificam o dia,
e a conferência da inclusão ignora os excluídos; além disso, o dicionário do acervo
não traz a chave primária do mapa, só os conjuntos de leitura. Não se sabe se a nova
inclusão cria um segundo registro com a mesma identificação do dia ou se substitui o
excluído. Pergunta ao site.

### RN-10 — Alterar e excluir exigem ter consultado aquele dia

Para **alterar** ou **excluir**, o servidor precisa ter **consultado antes aquele
mesmo dia** na sessão. Não tendo, a recusa é * Consulte antes de alterar * ou *
Consulte antes de excluir *, conforme a operação. E o dia informado precisa ter mapa:
não tendo, a recusa é * Mapa nao cadastrado para este Dia/Mes *.

### RN-11 — Só o mapa aberto aceita alteração e exclusão

Só se altera ou exclui **mapa aberto**. Estando o mapa fechado, a recusa é * Mapas
fechados para este Mes/Ano *.

[?] A recusa fala do mês e do ano, mas a conferência olha a situação do mapa daquele
dia; se o que se quer barrar é o mês fechado, o alvo é outro. Pergunta ao site.

### RN-12 — O cardápio tem de existir e valer para a data, a semana e a refeição

O cardápio informado tem de **estar cadastrado e valer na data do mapa** — senão *
Cardapio nao cadastrado *; tem de **estar cadastrado na semana** do dia — senão *
Cardapio nao cadastrado nesta semana *; e o **tipo de refeição** a que ele pertence
tem de estar cadastrado no serviço — senão * Refeicao nao cadastrada *, ou *
Cardapio nao cadastrado nesta refeicao * quando o cardápio não serve àquela refeição.
Há ainda duas recusas de tipo: * Cardapio cadastrado como sobremesa *, quando um
cardápio de sobremesa é informado numa refeição, e * Cardapio nao cadastrado como
sobremesa *, quando um cardápio de refeição é informado num dos cardápios extras.

### RN-13 — As quantidades não podem passar as do perfil mensal

As quantidades de cada refeição **não podem passar as do perfil mensal do órgão**. A
tela soma as faixas do perfil para chegar aos tetos com que compara — as parciais de
todas as faixas, as integrais de todas as faixas, os residentes, os funcionários e os
totais por tipo de aluno —, e cada quantidade tem o seu teto. Passando, a recusa é *
NRP maior que o informado no perfil *.

[?] O acervo chama as quantidades de NRP e não traz o que a sigla abre; e a
correspondência entre cada quantidade da tela e cada faixa do perfil — as faixas que
o perfil nomeia com dois dígitos e as siglas PR, EE, CI, 34 e 58 — é leitura do
código, não do dicionário. Pergunta ao site.

### RN-14 — Cada refeição com quantidade exige cardápio, e cada cardápio exige quantidade

Cada refeição **com quantidade tem de ter o cardápio**, e cada cardápio informado tem
de ter quantidade. Quantidade sem cardápio é recusada com * Nao informe o NRP para
esta refeicao * — e * Nao informe o NRP para a sobremesa * nos cardápios extras;
cardápio sem nenhuma quantidade é recusado com * Informe o NRP para este cardapio *.
Antes das conferências, o código do cardápio é zerado quando todas as quantidades
daquela refeição são zero, de modo que refeição sem cardápio e sem quantidade é
simplesmente ignorada: não gera conferência.

### RN-15 — Sem atendimento, o motivo e a justificativa

Quando **não houve atendimento** no dia — nenhuma refeição com cardápio válido —, a
tela exige que se informe o **motivo**, uma das quatro marcações da máscara: sem
nenhuma, a recusa é * Informe motivo do nao atendimento *. A marcação do motivo é
única: informada uma das três primeiras, as demais são limpas e o código da
justificativa é zerado; o código preenchido marca a quarta. A quarta marcação exige o
**código da justificativa**: sem o código, * Informe o codigo da justificativa *; e o
código tem de estar cadastrado para o órgão, senão * Justificativa nao cadastrada *.

[?] O acervo não diz o nome de cada um dos quatro motivos nem qual deles é o da
quarta marcação. Pergunta ao site.

### RN-16 — A consulta não grava nada

Na **consulta**, a tela lê o mapa do dia e o mostra — situação, cardápios e
quantidades. Não grava, não trava registro e não gera rastro de auditoria. Ao fim,
reabre a si mesma com o dia consultado.

### RN-17 — Toda gravação deixa rastro na auditoria

Toda inclusão, alteração e exclusão grava, além do mapa, um registro no cadastro de
auditoria (`A010T`) com a tela de origem, a operação, a matrícula do funcionário, a
estação, o número do processo, a sessão (dia, mês, ano e hora), o tipo de órgão e o
mapa resultante. A consulta não gera registro.

[?] A auditoria tem um campo para o conteúdo anterior e outro para o conteúdo
resultante; a tela deixa o anterior sempre em branco e grava o mapa no resultante. Se
o anterior deveria mostrar como o mapa estava antes da alteração e da exclusão, ele
não está sendo preenchido. Pergunta ao site.

### RN-18 — Ao incluir o mapa de um dia, os mapas abertos do mês anterior são fechados

Ao **incluir** o mapa de um dia, o sistema **fecha os mapas abertos do mês anterior**
do mesmo órgão e da mesma coordenadoria: percorre-os e grava cada um como fechado.
Depois disso, aquele mês anterior não aceita mais alteração nem exclusão por esta tela
(RN-11).

### RN-19 — Ao abrir para incluir um dia, a tela já sugere o cardápio de cada refeição

Quando a tela abre para **incluir** um dia, ela já preenche o **cardápio de cada
refeição** com o que o **calendário de cardápios do órgão** define para aquele dia da
semana: para cada refeição, o sistema procura o cardápio vigente na data do mapa e usa
a coluna do dia da semana. Refeição que o calendário não cobrir abre sem cardápio.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter o mapa diário de atendimento do órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M400T

  Cenário: A tela abre em consulta para o dia que já tem mapa
    Dado que a tela que escolhe o dia do mapa encaminhou um dia que já tem mapa
    Quando a tela abre
    Então ela já vem em consulta, com aquele dia, o órgão e a coordenadoria preenchidos
    E nada é gravado

  Cenário: A tela abre em inclusão para o dia que ainda não tem mapa
    Dado que a tela que escolhe o dia do mapa encaminhou um dia sem mapa
    Quando a tela abre
    Então ela já vem em inclusão, com o dia em aberto

  Cenário: Consulta mostra o mapa do dia e não grava nada
    Dado que o dia tem mapa
    Quando informo a operação de consulta
    Então vejo a situação do mapa, os cardápios e as quantidades do dia
    E nada é gravado

  Cenário: Inclusão do mapa de um dia
    Dado que o órgão do meu vínculo tem perfil cadastrado no mês de referência
    E que aquele dia ainda não tem mapa
    Quando informo a operação de inclusão, o dia, a semana e os cardápios com as quantidades
    Então o sistema cria o mapa do dia, aberto
    E registra a operação na auditoria

  Cenário: Alteração dos cardápios e das quantidades de um dia
    Dado que consultei aquele dia nesta sessão
    E o mapa do dia está aberto
    Quando informo a operação de alteração e regravo os cardápios e as quantidades
    Então o sistema grava o mapa com os novos dados
    E registra a operação na auditoria

  Cenário: Exclusão marca o mapa como excluído
    Dado que consultei aquele dia nesta sessão
    E o mapa do dia está aberto
    Quando informo a operação de exclusão
    Então o sistema marca o mapa como excluído
    E o dia sai das leituras
    E registra a operação na auditoria

  Cenário: Dia de 1º de agosto de 2008 em diante volta para a tela que escolhe o dia
    Dado que informo um dia de 1º de agosto de 2008 em diante
    Quando tento incluir, alterar, excluir ou consultar
    Então o sistema me devolve à tela que escolhe o dia, com a operação e o dia
    E nada é gravado

  Cenário: Órgão cadastrado como creche é recusado
    Dado que o órgão informado está cadastrado como creche
    Quando tento abrir o mapa do dia
    Então vejo a mensagem "* Orgao cadastrado como creche *"
    E nada é gravado

  Cenário: Órgão fora do vínculo do servidor
    Dado que informo um órgão que não é o do meu vínculo
    Quando tento abrir o mapa do dia
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"

  Cenário: Órgão não cadastrado ou não informado
    Dado que informo um órgão que não existe no cadastro
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E quando não informo o órgão vejo a mensagem "* Informe o orgao *"

  Cenário: Órgão inativo ou com dados incompletos
    Dado que o órgão está cadastrado como inativo
    Então vejo a mensagem "* Orgao cadastrado como inativo *"
    E quando o órgão está sem bairro, órgão pai, nome, endereço, matriculados ou pessoas vejo "* Orgao cadastrado com dados incompletos *"

  Cenário: Órgão de outra secretaria ou de coordenadoria sem acesso
    Dado que o órgão não é da secretaria da sessão
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E quando o órgão é de uma coordenadoria à qual não tenho acesso vejo "* Usuario sem acesso ao grupo deste orgao *"

  Cenário: Mês, ano e dia não informados
    Quando deixo o mês e o ano em branco
    Então vejo a mensagem "* Informe o Mes/Ano *"
    E quando deixo o dia em branco vejo a mensagem "* Informe o Dia/Mes *"

  Cenário: Mês, ano ou dia impossíveis
    Dado que informo um mês ou um ano que não existem
    Então vejo a mensagem "* Mes/Ano invalidos *"
    E quando informo um dia que não existe vejo a mensagem "* Dia/Mes invalidos *"

  Cenário: Mês fora da tabela de períodos do mapa
    Dado que informo um mês e um ano que não constam da tabela de períodos do mapa
    Quando tento abrir o mapa do dia
    Então vejo a mensagem "* Mes/Ano nao cadastr.na tab.de periodos do mapa *"

  Cenário: Data do mapa maior que a data atual
    Dado que informo um dia depois de hoje
    Quando tento abrir o mapa do dia
    Então vejo a mensagem "* Data do mapa maior que data atual *"

  Cenário: Dia fora do intervalo do período
    Dado que informo um dia fora do início e do limite do período do mês
    Então vejo a mensagem "* Dia/Mes fora do intervalo do periodo *"

  Cenário: Semana diferente da do calendário do órgão
    Dado que informo uma semana diferente da que o calendário define para o dia
    Então vejo a mensagem "<- Informe semana correta *"
    E quando não informo a semana, o sistema preenche com a do calendário

  Cenário: Mês sem perfil cadastrado para o órgão
    Dado que o mês não tem perfil de atendimento para o órgão
    Quando tento incluir ou alterar
    Então vejo a mensagem "* Nao existe perfil cadastrado para o Orgao *"
    E nada é gravado

  Cenário: Inclusão de um dia que já tem mapa
    Dado que o dia já tem mapa
    Quando tento incluir
    Então vejo a mensagem "* Mapa ja cadastrado para este Dia/Mes *"
    E nada é gravado

  Cenário: Alterar ou excluir sem ter consultado aquele dia
    Dado que não consultei aquele dia nesta sessão
    Quando tento alterar
    Então vejo a mensagem "* Consulte antes de alterar *"
    E quando tento excluir vejo a mensagem "* Consulte antes de excluir *"

  Cenário: Dia sem mapa cadastrado
    Dado que o dia não tem mapa
    Quando tento alterar, excluir ou consultar
    Então vejo a mensagem "* Mapa nao cadastrado para este Dia/Mes *"

  Cenário: Mapa fechado não aceita alteração nem exclusão
    Dado que o mapa do dia está fechado
    Quando tento alterar ou excluir
    Então vejo a mensagem "* Mapas fechados para este Mes/Ano *"
    E o mapa continua como está

  Cenário: Cardápio não cadastrado ou fora da semana
    Dado que informo um cardápio que não vale na data do mapa
    Então vejo a mensagem "* Cardapio nao cadastrado *"
    E quando informo um cardápio que não está cadastrado na semana do dia vejo "* Cardapio nao cadastrado nesta semana *"

  Cenário: Cardápio de sobremesa informado numa refeição
    Dado que informo, numa refeição, um cardápio cadastrado como sobremesa
    Então vejo a mensagem "* Cardapio cadastrado como sobremesa *"
    E quando informo um cardápio de refeição num dos cardápios extras vejo "* Cardapio nao cadastrado como sobremesa *"

  Cenário: Refeição ou cardápio não cadastrado no serviço
    Dado que o cardápio informado não pertence a nenhuma refeição cadastrada
    Então vejo a mensagem "* Refeicao nao cadastrada *"
    E quando o cardápio existe mas não serve àquela refeição vejo "* Cardapio nao cadastrado nesta refeicao *"
    E nada é gravado

  Cenário: Quantidade maior que a do perfil do mês
    Dado que informo uma quantidade acima da que o perfil do mês registra
    Então vejo a mensagem "* NRP maior que o informado no perfil *"
    E nada é gravado

  Cenário: Quantidade sem cardápio e cardápio sem quantidade
    Dado que informo quantidade numa refeição sem cardápio
    Então vejo a mensagem "* Nao informe o NRP para esta refeicao *"
    E quando informo quantidade num dos cardápios extras sem o cardápio vejo "* Nao informe o NRP para a sobremesa *"
    E quando informo um cardápio sem nenhuma quantidade vejo "* Informe o NRP para este cardapio *"

  Cenário: Refeição sem cardápio e sem quantidade é ignorada
    Dado que deixo uma refeição sem cardápio e sem nenhuma quantidade
    Quando a tela processa o dia
    Então aquela refeição não gera conferência nenhuma

  Cenário: Dia sem atendimento e sem motivo informado
    Dado que nenhuma refeição tem cardápio válido
    E não marco nenhum motivo
    Então vejo a mensagem "* Informe motivo do nao atendimento *"
    E nada é gravado

  Cenário: Motivo que exige justificativa
    Dado que marco o motivo que exige o código da justificativa
    E deixo o código em branco
    Então vejo a mensagem "* Informe o codigo da justificativa *"
    E quando informo um código que não está cadastrado vejo "* Justificativa nao cadastrada *"

  Cenário: Inclusão de um dia fecha os mapas abertos do mês anterior
    Dado que o mês anterior tem mapas abertos para o órgão e a coordenadoria
    Quando incluo o mapa de um dia do mês
    Então os mapas abertos do mês anterior ficam fechados
    E não aceitam mais alteração nem exclusão

  Cenário: A tela abre com os cardápios do dia sugeridos
    Dado que o calendário de cardápios do órgão tem cardápio para aquele dia da semana
    Quando abro a tela para incluir um dia
    Então cada refeição já vem com o cardápio daquele dia da semana

  Cenário: A gravação deixa rastro na auditoria
    Dado que incluo, altero ou excluo o mapa de um dia
    Então a auditoria guarda a operação, a matrícula, a estação e a sessão
    E quando só consulto, nenhum registro de auditoria é gerado
```
