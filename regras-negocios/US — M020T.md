# US — M020T — Manter as alterações da merenda de uma unidade no mês de referência

## Estória

Como **servidor da CRE**, quero **lançar e excluir as alterações da merenda de um
órgão filho da minha coordenadoria em cada mês de referência**, para que a
secretaria saiba qual cardápio (e quais gêneros, semana e justificativa) vale em
cada unidade naquele mês.

O cardápio e a merenda já existem no sistema — o que não existe é o registro do
que muda, unidade por unidade e mês a mês. Sem esse registro, o que foi combinado
com a unidade não tem onde ficar: não há como dizer que naquele mês, naquela
unidade, a merenda daquele dia mudou, nem por qual motivo. É esse registro que
alimenta quem entrega e quem fiscaliza a alimentação escolar.

## Contexto

Jornada S000M → M000M → M020T.
Ator: servidor de CRE — lança e exclui as alterações da merenda das unidades da
sua coordenadoria, mês a mês.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

O menu `M000M`, passo anterior da jornada, é um menu puro: ele só diz qual tela
abrir, não passa registro nem operação e não escreve em cadastro nenhum. A
`M020T` abre, portanto, sem nada recebido do menu — com os próprios campos de
entrada e de exibição e com o que a sessão já trazia: o tipo de órgão, a
coordenação regional escolar e o órgão filho do servidor, deixados pela entrada.

A tela não encadeia para outra: a jornada termina nela, e o que ela grava são as
alterações da merenda e a trilha de auditoria das operações. Não há comparação
com a tela de origem que mude o comportamento dela.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela inclui, exclui e consulta as alterações da merenda do mês

A tela mantém as alterações da merenda de uma unidade num mês de referência. Ela
aceita **três operações**: inclusão, exclusão e consulta. Qualquer outra coisa na
opção de manutenção é recusada com **\* Operacao nao disponivel. Use INC, EXC ou
CON \***, e nada é gravado ou apagado. A alteração não se faz por esta tela: não
há caminho que a execute.

A alteração da merenda é montada numa **grade de 12 linhas** — o mesmo limite que
o sistema fixa nas três passagens da tela. Na abertura, a tela começa pela
inclusão quando nada chegou de outra tela.

### RN-02 — A tela identifica a unidade e a coordenadoria regional escolar

A tela trabalha com o **órgão filho (SDI)**, com 8 dígitos, e a **coordenação
regional escolar (CRE)**, com 2 dígitos. Os dois passam pela conferência numérica
do sistema antes de qualquer consulta: campo em branco vira zero, os zeros à
esquerda são descartados e o que não for número é recusado — e o que não passa por
essa conferência não chega ao cadastro.

Quando a sessão do servidor já traz a unidade e a coordenadoria, é esse vínculo
que a tela adota; se o servidor não tem unidade presa, ele informa a unidade, e
informar é obrigatório: em branco, a recusa é **\* Informe o orgao \***, com o
cursor de volta no campo do órgão.

[?] A tela recusa informar outra unidade que não a do vínculo do servidor, com
**\* Usuario sem acesso a outro orgao \***. Nada no lote, porém, preenche esse
vínculo de unidade: o campo é apenas zerado na rotina comum de sessão, e o valor
que a entrada deixa é guardado em outra área. Ou a guarda nunca dispara, ou o
valor chega por um caminho que o lote não mostra. Pergunta ao site.

### RN-03 — A unidade informada tem de estar cadastrada, com os dados completos, do tipo da secretaria e do grupo do servidor

A unidade digitada é lida no cadastro do órgão filho e passa por quatro peneiras,
nesta ordem:

| peneira | recusa |
| --- | --- |
| 1. existe e não está excluída | **\* Orgao nao cadastrado \*** |
| 2. tem bairro, órgão pai, nome, endereço, número de matrículas e número de pessoas | **\* Orgao cadastrado com dados incompletos \*** |
| 3. é do tipo de órgão da secretaria da sessão | **\* Orgao nao pertence a esta secretaria \*** |
| 4. é da mesma coordenação regional escolar do servidor | **\* Usuario sem acesso ao grupo deste orgao \*** |

Passando pelas quatro, a tela mostra o **nome da unidade**, a **coordenação
regional escolar** e a **data de atualização** que o sistema informa.

### RN-04 — O mês e o ano de referência são obrigatórios e têm de ser um mês válido

Ao incluir, o **mês e o ano de referência** são obrigatórios: em branco, a recusa
é **\* Informe o Mes/Ano \***. Informados, o mês tem de estar entre 01 e 12 e o
ano entre 1994 e 2099; fora disso a recusa é **\* Mes/Ano invalidos \***.

O mês de referência tem de constar da **tabela de períodos do mapa** daquela
unidade, com o seu período de vigência: não constando, a recusa é **\* Mes/Ano
nao cadastr.na tab.de periodos do mapa \***.

### RN-05 — Incluir exige o mapa do mês aberto

Havendo mapa do mês para a unidade, a inclusão só passa se ele estiver
**aberto**. Fechado, a recusa é **\* Alteracoes fechadas. Reabra antes da
inclusao \***, e o cursor volta ao mês de referência.

### RN-06 — Cada alteração é de um dia da merenda, e o dia tem de caber no período

Cada alteração vale para **um dia da merenda**: o dia e o mês são obrigatórios ao
incluir. Com o dia e o mês informados, o sistema confere se formam uma **data
válida** — não formando, a recusa é **\* Dia/Mes invalidos \*** — e se a data cai
dentro do período de vigência do **cardápio** da unidade; fora dele, a recusa é
**\* Dia/Mes fora do intervalo do periodo \***.

[?] A comparação do período do cardápio usa o **primeiro** dia de vigência lido,
e o teste é "o início do período é depois do dia informado". O lote mostra as
duas pontas do período (início e limite), mas só a de início é usada nesse teste:
informar um dia depois do fim do período não é recusado por ele. Ou o teste vale
para outra coisa, ou falta a outra ponta. Pergunta ao site.

### RN-07 — A inclusão começa pelo dia, e o dia já lançado não é registrado de novo

A inclusão começa pelo **dia e mês da merenda**. Se já existir alteração da
merenda lançada para aquele dia e mês, a passagem termina sem mensagem e sem
gravar: o dia não é registrado de novo, e o servidor volta a ver o que já estava.

### RN-08 — A semana da merenda é A, B, C ou D

A alteração leva a **semana da merenda**, com uma letra: **A, B, C ou D**.
Qualquer outro valor é recusado com **\* Informe semana com A / B / C / D \***.

### RN-09 — O cardápio é obrigatório e tem de ser um cardápio da unidade

A alteração leva o **código do cardápio**, com 5 dígitos. O código tem de
corresponder a um cardápio cadastrado para aquela unidade; não correspondendo, a
recusa é **\* Cardapio nao cadastrado \***.

### RN-10 — A alteração leva ao menos um gênero, e o primeiro tem de constar do cardápio

A alteração leva **até dois pares de subclasse e gênero** — dois gêneros, cada um
com a sua subclasse. Pelo menos um gênero tem de estar informado; sem nenhum, a
recusa é **\* Informe genero a excluir ou incluir \***.

O **primeiro** par é conferido duas vezes: o gênero tem de existir, com a
subclasse dele, e estar **ativo** no cadastro de gêneros — senão a recusa é
**\* Sub/Genero nao cadastrado \*** — e o par tem de constar dos gêneros daquele
**cardápio**, para o período da merenda — senão a recusa é **\* Genero nao
cadastrado neste cardapio \***.

[?] O **segundo** par não passa pela conferência de cardápio: a tela verifica se
ele existe e está ativo no cadastro de gêneros, mas não confere se consta daquele
cardápio. Ou a conferência foi esquecida nesse ramo, ou o segundo gênero não
precisa constar do cardápio. Pergunta ao site.

### RN-11 — A justificativa é obrigatória e tem de existir para o tipo de órgão

A alteração leva o **código da justificativa**, com 2 dígitos, e ele é
obrigatório: em branco, a recusa é **\* Informe o codigo da justificativa \***.
Informado, tem de constar do cadastro de justificativas do tipo de órgão da
sessão; não constando, a recusa é **\* Justificativa nao cadastrada \***.

### RN-12 — Excluir exige ter consultado a mesma unidade, ano e mês, e a alteração tem de existir

A exclusão não se faz às cegas: a unidade, o ano e o mês informados têm de ser os
mesmos que a última consulta da sessão deixou carregados. Diferindo, a recusa é
**\* Consulte antes de excluir \***, com o cursor de volta na opção de manutenção.

Passando por essa amarração, o sistema procura a alteração do dia e do mês
informados, com o mesmo cardápio; não achando, a recusa é **\* Alteracao nao
cadastrada para este Mes/Ano \***.

### RN-13 — A guarda da exclusão contradiz o ramo que apaga

Antes de apagar, uma guarda olha o mapa do mês da unidade: se estiver **fechado**,
a exclusão é recusada com **\* Alteracoes fechadas para este Mes/Ano \*** e nada é
apagado. A leitura que essa guarda usa é a do **registro do mês** (sem o dia),
enquanto o ramo que apaga procura a alteração **pelo dia** — e a alteração de um
dia pode perfeitamente existir num mês cujo mapa está aberto.

[?] A guarda exige o mês **fechado** para deixar apagar, e recusa justamente
quando ele está fechado — os dois lados não fecham. Somando a isso, logo adiante a
tela recusa apagar quando não acha o registro do mês com o dia informado, o que só
acontece se o dia estiver preenchido. Ou a guarda vale para outro caso, ou o
caminho da exclusão ficou inalcançável para a alteração que o ramo exclui. Pergunta
ao site.

### RN-14 — A exclusão marca a alteração como excluída em vez de apagá-la

A exclusão não remove o registro: o sistema o regrava **marcado como excluído**,
com quem excluiu, de onde e quando, e a marcação é o que faz a alteração sair das
consultas do mês. O registro continua no cadastro, e é ele que permite auditar o
que foi lançado e depois retirado.

### RN-15 — Toda inclusão e toda exclusão deixam rastro

Toda inclusão e toda exclusão gravam na **trilha de auditoria (A010T)**: a tela de
origem, a operação (inclusão ou exclusão), o tipo de órgão, a unidade, a
coordenação regional escolar, a matrícula funcional, a estação, a sessão, a data e
a hora, e os valores **antes e depois**. A inclusão e a exclusão também registram
na própria alteração da merenda quem lançou (matrícula funcional), de onde
(estação) e quando (data e hora).

### RN-16 — Consultar não grava nada

Na consulta a tela apenas mostra: lê a unidade, o mapa do mês, o período, a
semana, o cardápio e os gêneros, e exibe o que está registrado. Nenhuma gravação é
executada, e nenhuma trilha é deixada. Quando não há alteração nenhuma para a
unidade no mês e ano informados, o aviso é **\* Nao existem alteracoes
cadastr.neste Mes/Ano \*** — e nada é gravado.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter as alterações da merenda de uma unidade no mês de referência

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M020T

  Cenário: RN-02, RN-03 e RN-16 — consultar as alterações do mês de uma unidade
    Dado que estou na tela M020T com a opção CON
    E informo uma unidade da minha coordenadoria, com um mês e um ano de referência já cadastrados
    Quando confirmo a consulta
    Então vejo o nome da unidade, a coordenação regional escolar, a data de atualização e o indicador de disponibilidade
    E vejo o período de vigência do mês, com dia, mês e ano de início e de limite
    E vejo as alterações já lançadas
    E nada é gravado

  Cenário: RN-16 — unidade sem alteração no mês e ano
    Dado que consultei uma unidade que não tem alteração lançada naquele mês e ano
    Então vejo "* Nao existem alteracoes cadastr.neste Mes/Ano *"
    E nada é gravado

  Cenário: RN-01 — operação não disponível
    Dado que estou na tela M020T
    Quando informo uma opção de manutenção diferente de INC, EXC e CON
    Então vejo "* Operacao nao disponivel. Use INC, EXC ou CON *"
    E nada é gravado

  Cenário: RN-02 — unidade em branco
    Dado que o meu usuário não tem unidade presa
    Quando confirmo sem informar a unidade
    Então vejo "* Informe o orgao *"
    E nada é gravado

  Cenário: RN-02 — unidade fora do vínculo da sessão
    Dado que a sessão traz uma unidade presa ao meu usuário
    Quando informo outra unidade
    Então vejo "* Usuario sem acesso a outro orgao *"
    E nada é gravado

  Cenário: RN-02 — campo não numérico
    Quando informo no órgão filho ou na coordenação regional escolar algo que não é número
    Então o campo é recusado antes de qualquer consulta
    E o cadastro não é lido

  Cenário: RN-03 — unidade não cadastrada
    Quando informo uma unidade que não existe no cadastro
    Então vejo "* Orgao nao cadastrado *"
    E nada é gravado

  Cenário: RN-03 — unidade com dados incompletos
    Quando informo uma unidade sem bairro, sem órgão pai, sem nome, sem endereço, sem número de matrículas ou sem número de pessoas
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E nada é gravado

  Cenário: RN-03 — unidade de outra secretaria
    Quando informo uma unidade do tipo de órgão de outra secretaria
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E nada é gravado

  Cenário: RN-03 — unidade de outra coordenação
    Dado que o meu usuário tem coordenação regional escolar
    Quando informo uma unidade de outra coordenação
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E nada é gravado

  Cenário: RN-04 — mês e ano de referência em branco
    Dado que estou na tela M020T com a opção INC
    Quando confirmo sem informar o mês e o ano de referência
    Então vejo "* Informe o Mes/Ano *"
    E nada é gravado

  Cenário: RN-04 — mês e ano de referência inválidos
    Quando informo um mês fora de 01 a 12 ou um ano fora de 1994 a 2099
    Então vejo "* Mes/Ano invalidos *"
    E nada é gravado

  Cenário: RN-04 — mês de referência fora da tabela de períodos
    Quando informo um mês e ano que não constam da tabela de períodos do mapa da unidade
    Então vejo "* Mes/Ano nao cadastr.na tab.de periodos do mapa *"
    E nada é gravado

  Cenário: RN-05 — incluir num mês fechado
    Dado que a unidade já tem o mapa do mês com as alterações fechadas
    Quando confirmo a inclusão
    Então vejo "* Alteracoes fechadas. Reabra antes da inclusao *"
    E nada é gravado

  Cenário: RN-06 — dia e mês da merenda inválidos
    Dado que estou na tela M020T com a opção INC
    Quando informo um dia e um mês que não formam uma data válida
    Então vejo "* Dia/Mes invalidos *"
    E nada é gravado

  Cenário: RN-06 — dia fora do período do cardápio
    Dado que o cardápio da unidade tem um período de vigência
    Quando informo um dia e um mês fora desse período
    Então vejo "* Dia/Mes fora do intervalo do periodo *"
    E nada é gravado

  Cenário: RN-07 — incluir um dia que já está lançado
    Dado que a unidade já tem alteração lançada para aquele dia e mês
    Quando confirmo a inclusão do mesmo dia
    Então nada é gravado e nenhuma mensagem é mostrada
    E a alteração que já existia continua como estava

  Cenário: RN-08 — semana da merenda diferente de A, B, C e D
    Quando informo a semana da merenda com qualquer valor diferente de A, B, C e D
    Então vejo "* Informe semana com A / B / C / D *"
    E nada é gravado

  Cenário: RN-09 — cardápio não cadastrado para a unidade
    Quando informo um código de cardápio que não é daquela unidade
    Então vejo "* Cardapio nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — alteração sem nenhum gênero
    Quando confirmo a inclusão sem informar nenhuma subclasse e nenhum gênero
    Então vejo "* Informe genero a excluir ou incluir *"
    E nada é gravado

  Cenário: RN-10 — gênero não cadastrado ou inativo
    Quando informo uma subclasse e um gênero que não existem, ou que não estão ativos
    Então vejo "* Sub/Genero nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — primeiro gênero fora do cardápio da unidade
    Quando informo no primeiro par uma subclasse e um gênero que não constam daquele cardápio
    Então vejo "* Genero nao cadastrado neste cardapio *"
    E nada é gravado

  Cenário: RN-11 — justificativa em branco
    Quando confirmo a inclusão sem informar o código da justificativa
    Então vejo "* Informe o codigo da justificativa *"
    E nada é gravado

  Cenário: RN-11 — justificativa não cadastrada para o tipo de órgão
    Quando informo um código de justificativa que não existe para o tipo de órgão da sessão
    Então vejo "* Justificativa nao cadastrada *"
    E nada é gravado

  Cenário: RN-04, RN-06, RN-08, RN-09, RN-10, RN-11 e RN-15 — incluir uma alteração completa
    Dado que a unidade tem o mapa do mês aberto e o cardápio está vigente no dia informado
    E a subclasse e o gênero existem, estão ativos e constam do cardápio
    E a justificativa existe para o tipo de órgão
    Quando preencho o dia e o mês, a semana, o cardápio, o gênero e a justificativa, e confirmo
    Então a alteração da merenda é gravada para aquela unidade naquele mês
    E a gravação registra a matrícula funcional, a estação, a data e a hora
    E um registro de auditoria é deixado para a operação

  Cenário: RN-12 — excluir sem ter consultado antes
    Dado que estou na tela M020T com a opção EXC
    E informo uma unidade, um ano ou um mês diferente do que consultei
    Quando confirmo
    Então vejo "* Consulte antes de excluir *"
    E nada é apagado

  Cenário: RN-12 — excluir uma alteração que não existe
    Dado que consultei a unidade e não há alteração lançada para aquele dia e mês
    Quando confirmo a exclusão do dia e mês
    Então vejo "* Alteracao nao cadastrada para este Mes/Ano *"
    E nada é apagado

  Cenário: RN-13 — excluir num mês fechado
    Dado que consultei a unidade e o mapa daquele mês está fechado
    Quando confirmo a exclusão da alteração lançada
    Então vejo "* Alteracoes fechadas para este Mes/Ano *"
    E nada é apagado

  Cenário: RN-12, RN-14 e RN-15 — excluir uma alteração lançada
    Dado que consultei a unidade e a alteração do dia e mês está lançada
    Quando confirmo a exclusão daquele dia e mês, com o mesmo cardápio
    Então a alteração da merenda passa a constar como excluída e sai das consultas do mês
    E a exclusão registra a matrícula funcional, a estação, a data e a hora
    E um registro de auditoria é deixado para a operação
```
