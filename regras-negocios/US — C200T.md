# US — C200T — Comensais por refeição e segmento da unidade escolar

## Estória

Como **servidor da CRE que responde pelo acompanhamento da alimentação das unidades da sua
coordenadoria**, quero **informar, refeição por refeição e segmento por segmento, quantos
comensais cada unidade (o órgão filho SDI) vai atender**, para que **a quantidade de refeições a
produzir fique registrada por unidade e presa ao que o mapa de comensais daquela unidade previu,
sem estourar o perfil**.

A quantidade de comensais é o número com que a secretaria dimensiona a alimentação de cada
unidade: é por ele que se sabe quantas refeições de cada tipo aquela unidade e aquele segmento
esperam por mês. Sem esse número registrado, a unidade fica sem previsão de refeições por segmento
e por tipo de refeição, e o que o mapa de comensais planejou para o mês não chega ao cadastro da
unidade. É esta tela que grava o número — um por refeição —, e é ela que recusa a quantidade que
passa do que o perfil da unidade autoriza. A mesma tela serve para conferir o que já está previsto.

## Contexto

Jornada S000M → C000M → C028M → C200T.

Ator: servidor de CRE — informa e confere, para as unidades da sua coordenadoria, quantos
comensais cada refeição atende em cada segmento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

Os dois menus do caminho (`C000M` e `C028M`) não são telas de dados: não gravam nada, não deixam
registro e não deixam origem na sessão — apenas dizem qual tela abrir. O que a C200T usa da sessão
— a secretaria, a coordenação regional escolar, a matrícula, o código de acesso, o privilégio, o
órgão do servidor e a data do sistema — foi deixado pela entrada, e está no anexo de evidências,
em **Regras que se revelaram da entrada**.

A jornada termina nesta tela: a C200T não encadeia para nenhuma outra e não passa registro nem
operação adiante. O contexto que ela deixa na sessão é o dela mesma — a última unidade, o último
segmento e o último modo usados —, e é por causa disso que ela reabre onde parou (RN-17). Nada do
caminho de menus preenche esse contexto: a primeira abertura é uma consulta com o formulário vazio
(RN-16), porque não há unidade carregada.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O que a tela mantém: os comensais de cada refeição em cada segmento da unidade

A tela registra, para uma unidade (o órgão filho SDI), **quantos comensais ela atende em cada
refeição de cada segmento**. Cada registro é o par **refeição + quantidade de comensais**, preso à
secretaria, à unidade, à coordenação regional escolar e ao segmento; não existem dois registros
para o mesmo par. Junto da quantidade ficam a **situação** do registro (ativo ou inativo), a
**matrícula e a data de quem o criou** e a **matrícula e a data da última atualização**. O cadastro
comporta **20.000** registros; capacidade declarada é o máximo esperado — parâmetro de
dimensionamento —, e não o volume já cadastrado.

### RN-02 — A página tem 13 linhas e lista as refeições da unidade naquele segmento

A página mostra **até 13 linhas**. Cada linha traz uma **refeição** — o código e a descrição — e a
**quantidade de comensais** já registrada para ela, mais o aviso de inatividade quando o registro
está inativo. O rol de refeições é da secretaria (o mesmo para todas as unidades) e **a linha só
aparece** para a refeição do rol que já tenha comensais registrados para aquela unidade e aquele
segmento **ou** que esteja prevista para o segmento; as demais refeições do rol não ocupam linha.

[?] A tela carrega um campo de código de referência, que ela mesma preenche com a última refeição
que exibiu e que o servidor não precisa informar; o corpus não traz o rótulo desse campo nem o que
ele faz. Pergunta ao site.

### RN-03 — O modo da tela só admite ALT ou CON, e a operação é autorizada

A tela tem um campo próprio de modo, e ele aceita **alteração** e **consulta** — os mesmos que a
mensagem de recusa nomeia como **ALT** e **CON**. Qualquer outro valor é recusado com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta no campo do modo, e nada é
gravado. Antes de seguir, a operação informada é conferida contra a **autorização do servidor para
esta tela**: sem a marca daquela operação, a tela volta e nada é conferido nem gravado.

[?] A mensagem manda usar ALT ou CON, mas o teste da tela é feito contra os códigos internos de
alteração e de consulta: se o campo recebe exatamente o que a mensagem manda digitar, a alteração
seria recusada. O corpus mostra o teste, não a tradução que a camada de apresentação faria.
Pergunta ao site.

### RN-04 — A unidade é obrigatória

O código da unidade (o órgão filho SDI) tem de ser informado. Em branco, a recusa é
**\* Informe o orgao \***, com o cursor de volta no campo da unidade, e nada é conferido nem
gravado.

### RN-05 — A unidade tem de estar cadastrada, ativa e com o cadastro completo

Informado o código, o sistema busca a unidade no cadastro. Não achando, a recusa é
**\* Orgao nao cadastrado \***. Achando, recusa com **\* Orgao cadastrado como inativo \*** quando
a unidade está marcada como inativa, e com **\* Orgao cadastrado com dados incompletos \*** quando
falta algum destes seis dados: o bairro, o órgão pai, o nome, o endereço, o número de matriculados
ou o número de comensais. Em qualquer dos três casos o cursor volta ao campo da unidade e nada é
gravado.

### RN-06 — A unidade tem de ser da secretaria do servidor e da coordenação dele

A unidade tem de pertencer ao mesmo tipo de órgão da secretaria da sessão; sendo de outra, a
recusa é **\* Orgao nao pertence a esta secretaria \***, com o cursor de volta no campo da unidade.
E a coordenação regional escolar da unidade tem de ser a do servidor: quando a sessão traz uma
coordenação e a unidade está em outra, a recusa é
**\* Usuario sem acesso ao grupo deste orgao \***, com o número da coordenação da unidade na
mensagem, o cursor de volta no campo da unidade e nada gravado. Quem **não** tem coordenação na
sessão não passa por essa última restrição.

[?] O campo de coordenação regional escolar informado na tela não participa da busca nem dessa
autorização: a unidade é encontrada só pelo código, e a coordenação que vale é a que está no
cadastro dela. O corpus não diz se o campo é para o servidor digitar ou para o sistema apenas
exibir. Pergunta ao site.

### RN-07 — Consultar a unidade de outro órgão é restrito

Na **consulta**, quando o servidor tem um órgão próprio na sessão e informa outra unidade, a recusa
é **\* Usuario sem acesso a outro orgao \***, com o número do órgão do servidor na mensagem, com o
cursor de volta no campo da unidade, e nada é carregado. Quem não tem órgão na sessão consulta
qualquer unidade. Na **alteração** essa restrição não existe: o que vale lá é a exigência de
consultar antes (RN-09).

### RN-08 — A unidade tem de ter o segmento informado; em branco, o primeiro segmento dela

O segmento é informado junto com a unidade. **Em branco**, o sistema assume o **primeiro segmento
cadastrado** da unidade. Informado um segmento que a unidade não tem, a recusa é
**\* Orgao nao cadastrado neste segmento \***, com o cursor de volta no campo do segmento, e nada é
carregado.

### RN-09 — Alterar exige ter consultado antes, o mesmo par unidade e segmento

Na alteração, o sistema exige que a unidade e o segmento informados sejam exatamente os que a
**última consulta** deixou carregados na sessão. Divergindo qualquer um dos dois, a recusa é
**\* Consulte antes de atualizar \***, com o cursor de volta no campo da unidade, e nada é gravado.
É assim que a alteração só alcança o que o servidor acabou de ver.

### RN-10 — Novo segmento: exige a unidade já carregada e leva ao segmento seguinte

A tela aceita o pedido de **outro segmento da mesma unidade**, por um campo próprio que recebe a
marca de novo segmento. O pedido exige que a unidade informada seja a que já está carregada na
sessão: não sendo, a recusa é **\* Consulte antes de solicitar novo seg \***, com o cursor de volta
no campo da unidade, e nada é gravado. Aceito o pedido, o sistema passa para o **segmento seguinte
da unidade** — ou, não havendo seguinte, para o primeiro — e recarrega o que a unidade tem naquele
segmento. O pedido, por si só, não grava quantidade nenhuma.

[?] Quando não há segmento seguinte, o sistema relê o cadastro de segmentos da unidade desde o
começo e fica com o primeiro que encontra; o corpus não documenta o posicionamento dessa leitura,
e não dá para afirmar se ela alcança o primeiro segmento da unidade ou apenas o primeiro da faixa
em que a leitura parou. Pergunta ao site.

### RN-11 — O segmento tem de estar no mapa de comensais do mês da unidade

Havendo quantidade a gravar, o sistema procura o **mapa de comensais do mês de referência** da
unidade e, dentro dele, o segmento informado. Não achando o segmento no mapa, a recusa é
**\* Segmento nao cadastrado no perfil \***, com o cursor de volta no campo da quantidade, e nada é
gravado. A procura usa a **referência mais recente** que a unidade tem no mapa, qualquer que seja o
mês em que o servidor esteja.

### RN-12 — A quantidade não pode passar do limite do perfil

A quantidade de comensais de uma linha não pode passar do que o perfil autoriza para aquela
refeição naquele segmento. O limite é a **quantidade prevista no mapa de comensais do segmento** —
a soma do que o mapa previu para os atendimentos de 24 horas, integral e parcial — reduzida por um
**percentual cadastrado para a unidade**: o sistema procura esse percentual, nesta ordem, para a
unidade com o segmento e a refeição, para o segmento com a refeição, para a refeição e, por último,
para a secretaria, e usa o primeiro que encontrar; não achando nenhum, o percentual é de **100%**.
Em unidade de creche o sistema soma à parte as quantidades dos segmentos de creche e usa essa soma
quando o segmento informado é um deles; nos demais, usa a soma dos outros. Passando do limite, a
recusa é **<- Quantidade maxima de comensais \***, com o cursor de volta no campo da quantidade, com
o limite calculado na mensagem, e nada é gravado. A conferência só roda para a linha que vai mudar:
linha com a quantidade já registrada passa em silêncio. E quando o mapa não prevê quantidade
nenhuma para o segmento, o limite não é aplicado.

[?] O cadastro do perfil tem dois números com nome de quantidade e de perfil; o programa aplica,
dividido por cem, o campo de quantidade de pessoas, o que o faz valer como percentual. Qual dos
dois é o percentual esperado, o corpus não diz. Pergunta ao site.

[?] Quando a unidade não tem mapa de comensais do mês, a conferência do limite é abandonada sem
recusa — e a quantidade informada é gravada assim mesmo, sem limite nenhum. Ou a falta de mapa
deveria impedir a gravação, ou esse caminho é inalcançável por outro motivo. Pergunta ao site.

### RN-13 — O que a alteração grava em cada linha

Confirmada a alteração, cada linha é tratada pelo que ela pede:

- **linha com a quantidade zerada** e registro existente: o registro é **apagado**;
- **linha com quantidade diferente** da registrada: o registro é **atualizado** com a nova
  quantidade, volta a ficar **ativo** e recebe a matrícula e a data da atualização — ou é
  **criado**, se ainda não existia, já com a situação ativo e a matrícula e a data do cadastro;
- **linha com a quantidade igual** à registrada: a quantidade **não é regravada**; o sistema só
  ajusta a situação — mantém ativo o registro do segmento que tem perfil no mapa e **desativa** o
  que não tem;
- **linha sem quantidade e sem registro**: nada é gravado.

O limite calculado não é gravado em lugar nenhum: ele só serve para a recusa.

### RN-14 — Toda gravação deixa rastro na auditoria

Cada inclusão, alteração e exclusão confirmadas deixam uma linha na **trilha de auditoria**, com o
objeto auditado (os comensais da unidade), a **operação**, o **conteúdo anterior** e o **novo** e o
contexto da sessão — matrícula, secretaria, coordenação, estação, data e hora da sessão e número do
processo, que esta tela preenche com o código da unidade. Na inclusão o conteúdo anterior vai
vazio; na exclusão, o novo.

### RN-15 — A consulta carrega e confere; não altera quantidade

Na consulta, o sistema carrega a unidade e o segmento pelo cadastro, confere as autorizações
(RN-05 a RN-08) e mostra as refeições com as quantidades já registradas. **As quantidades digitadas
na consulta são ignoradas**: nenhuma inclusão, alteração ou exclusão de linha acontece por causa
delas.

[?] O caminho de gravação, porém, não fica inerte na consulta: ele percorre os registros de
comensais da unidade e **apaga** os que estão em branco — sem segmento, sem refeição ou sem
quantidade —, e não deixa rastro na auditoria. Ou essa limpeza pertence a outro fluxo, ou a
consulta não é somente leitura. O corpus não decide. Pergunta ao site.

### RN-16 — A abertura sem unidade carregada é uma consulta com o formulário vazio

A primeira abertura da tela na sessão — sem unidade nenhuma carregada — é uma **consulta com o
formulário vazio**: nenhuma refeição é listada, e o servidor precisa informar a unidade (e o
segmento) e confirmar para que a tela carregue o que existe. A tela não abre listando o cadastro
inteiro nem uma unidade por conta própria.

### RN-17 — A tela reabre no modo e no par unidade e segmento da última passagem

O modo usado, a última unidade e o último segmento carregados ficam guardados na área de trabalho
da sessão. Reabrindo a tela, ela volta no **mesmo modo** — alteração, se foi o último — e apontada
para a **mesma unidade e o mesmo segmento**, com o que eles têm naquele segmento.

### RN-18 — A tela não muda conforme quem a chamou

A tela não consulta de onde veio: não há, nela, comparação com a tela de origem, e os menus do
caminho também não deixam origem na sessão. Ela abre sempre do mesmo jeito — em consulta quando não
há unidade carregada (RN-16) e no modo que a sessão guardou quando há (RN-17). O que muda o
comportamento dela é o modo informado e o contexto da sessão, não quem a chamou.

### RN-19 — Chegando com a tela de destino preenchida, a manutenção é abandonada

Se a tela chegar com a indicação de **tela de destino** preenchida — o dado que a rota usa para
devolver o servidor a outra tela —, a manutenção é abandonada: nada é validado, nada é gravado e o
servidor é levado à tela indicada.

[?] Nada nesta jornada preenche essa indicação, e o corpus não traz o rótulo do campo nem diz para
onde ele levaria. Pergunta ao site.

### RN-20 — Os códigos e a quantidade passam por conferência numérica antes das regras

O código da unidade, a coordenação regional escolar, o código do segmento, o código da refeição, a
quantidade de comensais e o código de referência passam por uma conferência numérica **antes** das
regras de negócio desta tela: texto informado em qualquer deles é recusado no próprio campo, com o
cursor nele, e nada é consultado por causa disso.

[?] O texto exato da recusa não está no lote: a conferência é feita por rotina padrão de edição
numérica, e a mensagem que o terminal mostra sai da rotina de comunicação, fora dos fontes
fornecidos. Pergunta ao site.

### RN-21 — O aviso quando o segmento não tem nenhuma refeição com comensais

Carregadas a unidade e o segmento, se **nenhuma** refeição puder ser listada — nem por já ter
comensais registrados, nem por estar prevista para o segmento —, o sistema avisa
**\* Orgao sem comensais cadastrados neste seg \*** e não deixa seguir. É o aviso de que aquele
segmento da unidade ainda não tem previsão de refeições.

---

## Cenários BDD

```gherkin
Funcionalidade: Comensais por refeição e segmento da unidade escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenação, a matrícula, o órgão e a data do sistema
    E tenho acesso à tela C200T

  Cenário: RN-01 — os comensais ficam guardados por unidade, segmento e refeição
    Dado que estou na tela C200T em alteração, com uma unidade e um segmento carregados
    Quando informo a quantidade de comensais de uma refeição e confirmo
    Então fica gravado um registro daquela refeição com aquela quantidade
    E o registro fica preso à secretaria, à unidade, à coordenação e ao segmento
    E não existe um segundo registro para a mesma refeição naquele segmento
    E o registro fica com a minha matrícula e a data do dia

  Cenário: RN-02 — a página mostra as refeições da unidade naquele segmento
    Dado que estou na tela C200T com uma unidade e um segmento carregados
    Quando a página é apresentada
    Então vejo até 13 linhas, cada uma com a refeição e a quantidade de comensais
    E a linha só aparece para a refeição que tem comensais registrados ou que está prevista para o segmento
    E a linha do registro inativo traz o aviso de inatividade

  Cenário: RN-03 — modo diferente de ALT e de CON
    Dado que estou na tela C200T
    Quando informo um modo diferente de alteração e de consulta
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo do modo
    E nada é gravado

  Cenário: RN-03 — sem a autorização da operação informada
    Dado que a minha autorização não libera a operação informada nesta tela
    Quando confirmo
    Então a operação não segue
    E nada é conferido nem gravado

  Cenário: RN-04 — unidade em branco
    Dado que estou na tela C200T com o campo da unidade em branco
    Quando confirmo
    Então vejo "* Informe o orgao *"
    E o cursor volta para o campo da unidade
    E nada é gravado

  Cenário: RN-05 — unidade que não está cadastrada
    Quando informo o código de uma unidade que não existe no cadastro
    Então vejo "* Orgao nao cadastrado *"
    E o cursor volta para o campo da unidade
    E nada é gravado

  Cenário: RN-05 — unidade cadastrada como inativa
    Quando informo o código de uma unidade marcada como inativa
    Então vejo "* Orgao cadastrado como inativo *"
    E o cursor volta para o campo da unidade
    E nada é gravado

  Cenário: RN-05 — unidade com o cadastro incompleto
    Quando informo o código de uma unidade à qual falta bairro, órgão pai, nome, endereço,
      matriculados ou comensais
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E o cursor volta para o campo da unidade
    E nada é gravado

  Cenário: RN-06 — unidade de outra secretaria
    Quando informo o código de uma unidade de outro tipo de órgão
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor volta para o campo da unidade
    E nada é gravado

  Cenário: RN-06 — unidade de outra coordenação regional escolar
    Dado que a minha sessão traz a minha coordenação regional escolar
    Quando informo o código de uma unidade de outra coordenação
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E a mensagem traz a coordenação da unidade
    E o cursor volta para o campo da unidade
    E nada é gravado

  Cenário: RN-06 — servidor sem coordenação na sessão
    Dado que a minha sessão não traz coordenação regional escolar
    Quando informo uma unidade de qualquer coordenação já cadastrada
    Então a tela carrega a unidade, sem passar por essa restrição

  Cenário: RN-07 — consulta a unidade de outro órgão
    Dado que estou na tela C200T em consulta
    E que a minha sessão traz o meu órgão
    Quando informo uma unidade de outro órgão
    Então vejo "* Usuario sem acesso a outro orgao *"
    E a mensagem traz o meu órgão
    E nada é carregado

  Cenário: RN-08 — segmento que a unidade não tem
    Dado que estou na tela C200T consultando uma unidade
    Quando informo um segmento que aquela unidade não tem
    Então vejo "* Orgao nao cadastrado neste segmento *"
    E o cursor volta para o campo do segmento
    E nada é carregado

  Cenário: RN-08 — segmento em branco assume o primeiro da unidade
    Dado que estou na tela C200T consultando uma unidade
    Quando deixo o segmento em branco e confirmo
    Então a tela carrega o primeiro segmento cadastrado da unidade
    E mostra as refeições e as quantidades daquele segmento

  Cenário: RN-09 — alterar sem ter consultado o mesmo par
    Dado que estou na tela C200T em alteração
    E que a última consulta deixou outra unidade ou outro segmento carregado
    Quando confirmo com a unidade e o segmento informados
    Então vejo "* Consulte antes de atualizar *"
    E o cursor volta para o campo da unidade
    E nada é gravado

  Cenário: RN-10 — novo segmento sem a unidade carregada
    Dado que estou na tela C200T com a marca de novo segmento
    E que a unidade informada não é a que está carregada na sessão
    Quando confirmo
    Então vejo "* Consulte antes de solicitar novo seg *"
    E o cursor volta para o campo da unidade
    E nada é gravado

  Cenário: RN-10 — novo segmento leva ao segmento seguinte e não grava
    Dado que estou na tela C200T com a unidade carregada
    Quando informo a marca de novo segmento e confirmo
    Então a tela passa para o segmento seguinte da unidade
    E recarrega o que a unidade tem naquele segmento
    E nenhuma quantidade é gravada por causa do pedido

  Cenário: RN-11 — segmento fora do mapa de comensais do mês
    Dado que estou na tela C200T em alteração
    E que o mapa de comensais da unidade não tem o segmento informado
    Quando confirmo uma quantidade naquela linha
    Então vejo "* Segmento nao cadastrado no perfil *"
    E o cursor volta para o campo da quantidade
    E nada é gravado

  Cenário: RN-12 — quantidade acima do limite do perfil
    Dado que estou na tela C200T em alteração
    E que o segmento tem previsão no mapa de comensais do mês
    Quando informo uma quantidade maior do que o limite calculado para a refeição
    Então vejo "<- Quantidade maxima de comensais *"
    E a mensagem traz o limite calculado
    E o cursor volta para o campo da quantidade
    E nada é gravado

  Cenário: RN-12 — linha com a quantidade já registrada não passa pela conferência
    Dado que estou na tela C200T em alteração
    Quando confirmo sem mudar a quantidade que já estava registrada na linha
    Então nenhuma recusa é apresentada
    E a quantidade permanece a que já estava gravada

  Cenário: RN-13 — quantidade zerada apaga o registro
    Dado que estou na tela C200T em alteração, sobre uma linha que tem quantidade registrada
    Quando zero a quantidade da linha e confirmo
    Então o registro daquela refeição é apagado
    E a exclusão fica registrada na auditoria

  Cenário: RN-13 — quantidade nova cria ou atualiza o registro
    Dado que estou na tela C200T em alteração, sobre um segmento com previsão no mapa
    Quando informo uma quantidade diferente da registrada em uma linha e confirmo
    Então o registro daquela refeição passa a ter a quantidade informada
    E fica ativo, com a minha matrícula e a data do dia
    E a gravação fica registrada na auditoria

  Cenário: RN-13 — quantidade igual à registrada não regrava a quantidade
    Dado que estou na tela C200T em alteração, sobre uma linha que tem quantidade registrada
    Quando confirmo a mesma quantidade da linha
    Então a quantidade não é regravada
    E o segmento que tem perfil no mapa continua ativo
    E o segmento que não tem perfil no mapa fica inativo

  Cenário: RN-14 — a gravação deixa rastro na auditoria
    Dado que confirmei uma inclusão, uma alteração ou uma exclusão na C200T
    Quando a gravação termina
    Então existe um registro de auditoria dos comensais da unidade
    E com a operação, o conteúdo anterior e o novo
    E com a matrícula, a secretaria, a coordenação, a estação, a data e a hora da sessão
    E com o número do processo preenchido com o código da unidade

  Cenário: RN-15 — a consulta não altera quantidade
    Dado que estou na tela C200T em consulta
    Quando informo quantidades nas linhas e confirmo
    Então nenhuma quantidade é incluída, alterada ou apagada por causa do que digitei
    E as quantidades registradas continuam as mesmas

  Cenário: RN-16 — a abertura sem unidade carregada
    Dado que estou abrindo a tela C200T pela primeira vez na sessão
    Quando a tela é apresentada
    Então ela abre em consulta, com o formulário vazio
    E nenhuma refeição é listada

  Cenário: RN-17 — a tela reabre no modo e no par unidade e segmento da última passagem
    Dado que passei pela tela C200T em alteração, sobre uma unidade e um segmento
    Quando volto a abrir a tela
    Então ela reabre em alteração
    E apontada para a mesma unidade e o mesmo segmento, com o que eles têm

  Cenário: RN-18 — a tela abre do mesmo jeito por qualquer caminho
    Dado que chego a esta tela pela opção do menu C028M
    Quando a tela é apresentada
    Então ela abre no modo que a sessão guardou
    E não muda de comportamento por causa de quem a chamou

  Cenário: RN-19 — a tela de destino preenchida abandona a manutenção
    Dado que a transação chega à C200T com a indicação de tela de destino preenchida
    Quando a manutenção começaria
    Então nada é validado e nada é gravado
    E o servidor é levado à tela indicada

  Cenário: RN-20 — texto onde se espera número
    Quando informo texto no código da unidade, na coordenação, no segmento, na refeição ou
      na quantidade
    Então o campo é recusado antes de qualquer regra de negócio
    E o cursor fica no campo recusado
    E nada é consultado por causa dele

  Cenário: RN-21 — o segmento não tem nenhuma refeição com comensais
    Dado que estou na tela C200T consultando uma unidade
    E que naquele segmento não há comensais registrados nem refeição prevista
    Quando confirmo
    Então vejo "* Orgao sem comensais cadastrados neste seg *"
    E a tela não segue
```
