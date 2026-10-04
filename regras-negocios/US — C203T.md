# US — C203T — Referência mensal de matriculados e comensais do órgão filho

## Estória

Como **servidor da CRE**, quero **declarar e manter, mês a mês, quantos alunos cada
órgão filho tem matriculados e quantos comensais ele atende**, para que a Secretaria
dimensione a alimentação escolar pelo volume real de cada órgão.

A referência mensal é a declaração que vem antes do pedido: é dela que sai o volume
de matrículas e de refeições com que cada mês de cada órgão é planejado, e é ela que
alimenta o total do próprio órgão. Sem a declaração o mês não tem com que ser
planejado; e depois que os pedidos daquele mês já existem, a declaração não pode mais
ser apagada. A tela também é a consulta do que já foi declarado — e abri-la não grava
nada.

## Contexto

Jornada S000M → C000M → C200M → C203T.

Ator: servidor da CRE — declara e consulta a referência mensal de matriculados e de
comensais dos órgãos filho da sua coordenadoria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas do meio do caminho são menus e não são telas de transação encadeadas: a
`C203T` é aberta pela opção 6 do `C200M`, e nada de negócio é passado de uma para a
outra. O que a `C203T` usa da sessão — o tipo de órgão, a coordenadoria, a matrícula e
o código de acesso do servidor — foi deixado pela entrada, e a tela apenas o repassa
às rotinas comuns de segurança e de rota. A tela não encadeia para nenhuma outra: não
passa registro nem operação adiante, e a jornada termina nela.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela identifica o órgão filho, a coordenadoria e o mês/ano da referência

A tela trabalha com **quatro dados digitados**: o **órgão filho (SDI)**, com 8 dígitos;
a **coordenação regional escolar (CRE)**, com 2 dígitos; o **mês de referência**, com
2 dígitos; e o **ano de referência**, com 4 dígitos. É esse conjunto — mais a
secretaria do acesso, que vem da sessão — que identifica a referência mensal de cada
órgão.

A tela mostra ainda, sem que se digite: o **nome do órgão**, o **indicador de creche**
por extenso (Sim/Não), a **secretaria do acesso**, a **data do sistema** e o **tipo de
órgão** do servidor. Esses valores saem do cadastro de órgãos e da sessão.

### RN-02 — Todo campo digitado é conferido como número antes de ser usado

Os campos digitados — órgão, coordenadoria, mês, ano, matriculados e comensais — passam
pela conferência numérica do sistema antes de qualquer consulta: campo em branco vira
zero, os zeros à esquerda são descartados e o que não for número é recusado. A recusa
devolve o cursor ao campo recusado, e o que não passa por essa conferência não chega ao
cadastro.

### RN-03 — O modo da página só admite alteração (ALT) ou consulta (CON)

O modo da página admite dois valores: **ALT** (alteração) e **CON** (consulta). Qualquer
outro valor é recusado com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor
de volta no campo do modo, e nada é processado. O campo do modo é de cabeçalho — vale
para a página inteira, não é coluna de linha — e a conferência é feita no processamento
da primeira linha: as linhas seguintes da página já não a repetem.

### RN-04 — Em consulta, o órgão é obrigatório

No modo consulta, o servidor informa o **código do órgão filho**. Em branco, a recusa é
**\* Informe o orgao \***, com o cursor no campo do órgão, e nada é lido.

### RN-05 — O órgão informado tem de existir e não estar excluído

O órgão informado é procurado no **cadastro de órgãos filho**. Não existindo — ou
estando marcado como excluído — a recusa é **\* Orgao nao cadastrado \***, com o cursor
no campo do órgão, e nenhuma referência é mostrada. Órgãos marcados como excluídos são
saltados na procura; se não sobrar nenhum, a recusa é a mesma.

Aceito o órgão, o **nome**, a **coordenadoria** e o **indicador de creche** que a tela
mostra passam a ser os do cadastro, não os digitados.

[?] O cadastro de órgãos é procurado apenas pelo código do órgão, sem conferir a
secretaria da sessão, e a leitura aceita o mesmo código em mais de uma secretaria. A
tela pode estar mostrando o órgão de outra secretaria, e o acervo não permite decidir
se a conferência da secretaria era esperada. Pergunta ao site.

### RN-06 — Cada servidor só alcança os órgãos da sua coordenadoria

Encontrado o órgão, a tela compara a **coordenadoria do órgão** com a coordenadoria que
a sessão traz. Diferentes, a recusa é **\* <- Usuario sem acesso a este grupo \***, com
o cursor no campo do órgão, e o órgão não fica selecionado; nada é lido nem gravado.

[?] A conferência só acontece quando a sessão traz uma coordenadoria: se o vínculo do
servidor não tem coordenadoria, a tela não confere nada e qualquer órgão cadastrado
passa. Se isso é intencional — servidor sem coordenadoria vê todos os órgãos — ou é
buraco de alcance, o acervo não diz. Pergunta ao site.

### RN-07 — A página mostra 13 linhas, cada uma com mês, ano, matriculados, comensais e ação

A tela apresenta **13 linhas** por página. Cada linha traz o **mês de referência**, o
**ano de referência**, a **quantidade de matriculados**, a **quantidade de comensais** e
a **ação**. O sistema fixa esse mesmo limite de 13 nas passagens de validação e de
gravação, e é ele que decide se ainda há linhas a percorrer.

### RN-08 — Sem referência declarada para o órgão, a tela avisa

Quando a leitura da página não encontra nenhuma referência declarada para o órgão, o
processamento da página para e a tela avisa **\* Orgao sem registros cadastrados \***,
sem mostrar linha alguma.

[?] O mesmo aviso é disparado tanto quando o órgão não tem nenhuma referência quanto
quando as referências acabam no meio da página: a leitura começa pela referência mais
antiga do órgão e avança linha a linha até a mais nova, e o aviso é dado na linha em
que a leitura não encontra mais nada — mesmo já tendo mostrado as anteriores. Ou o aviso
é de "órgão sem registro", ou é de "fim dos registros", e o acervo não decide qual.
Pergunta ao site.

### RN-09 — Linha sem mês/ano ou com ação desconhecida é ignorada

Uma linha só é processada se o **mês/ano** estiver preenchido **e** a ação for inclusão
(**I**), alteração (**A**) ou exclusão (**E**). Mês/ano zerado, ação em branco ou ação
que não seja uma dessas três passa batido: não gera recusa, não gera gravação e não
interrompe as demais linhas da página.

### RN-10 — A ação da linha traduz a operação: I declara, A altera, E exclui

A ação é da linha, não da página: cada linha pode pedir uma operação diferente. O
sistema traduz a ação para a operação correspondente — inclusão, alteração ou exclusão —
e é essa operação que ele submete à conferência de acesso do servidor, antes de gravar
qualquer coisa. A tela permite declarar, alterar e excluir; não há ação de consulta por
linha (a consulta é o modo CON da página, RN-03).

### RN-11 — A consulta não grava nada

Com o modo da página igual a consulta, o processamento de cada linha é abandonado antes
de qualquer conferência de ação — tanto na passagem de validação quanto na de gravação.
A consulta apenas lê o órgão e lista as referências declaradas, da mais antiga para a
mais nova; nenhuma referência é criada, alterada ou apagada e nenhuma auditoria é
gerada. O único efeito é interno à sessão: o órgão consultado e o modo ficam guardados
para as operações seguintes (RN-15).

### RN-12 — A declaração (I) recusa mês/ano que já está declarado

Na ação **I** o sistema procura a referência daquele órgão naquele mês e ano: se ela já
existe, recusa com **\* Mes/Ano ja cadastrado \***, com o cursor na coluna da ação, e
nada é gravado.

### RN-13 — A alteração (A) e a exclusão (E) exigem a referência declarada

Nas ações **A** e **E** o sistema exige que a referência daquele mês e ano exista para o
órgão. Não existindo, a recusa é **\* Mes/Ano nao cadastrado \***, com o cursor na
coluna da ação, e nada é gravado nem apagado. A ação **I** não faz essa conferência —
declarar é justamente criar a referência.

### RN-14 — As quantidades são obrigatórias e os comensais não podem superar os matriculados

Na **declaração** e na **alteração**, a quantidade de matriculados em branco ou zero é
recusada com **\* Quantidade de matriculados invalida \***; a de comensais, em branco ou
zero, com **\* Quantidade de comensais invalida \***; e comensais maior que matriculados,
com **\* Comensais > que matriculados \***. Em cada caso o cursor volta à coluna da
quantidade recusada e nada é gravado. A **exclusão** não confere quantidade.

### RN-15 — Alterar exige ter consultado antes o mesmo órgão

No modo ALT, o órgão informado tem de ser o mesmo que a última consulta deixou
carregado. Sendo outro, a recusa é **\* Consulte antes de alterar \***, com o cursor no
campo do órgão, e nada é gravado: para alterar ou declarar por esta tela, o servidor
consulta o órgão primeiro.

### RN-16 — O mês e o ano têm de ser um mês real, de 1994 a 2099

O mês/ano informado é conferido como data: o mês tem de ser de 1 a 12 e o ano, de 1994
a 2099. Fora disso a recusa é **\* Mes/Ano invalidos \***, com o cursor no campo do mês,
e nada é gravado.

### RN-17 — A declaração grava a referência do mês

Passadas as guardas, a declaração cria a referência com o **órgão filho**, a
**coordenadoria**, a **secretaria do acesso**, o **mês**, o **ano** e as duas
quantidades, e a grava no **cadastro de referências mensais**. A gravação é precedida
de trava do registro e cada operação deixa o seu registro na **auditoria**.

### RN-18 — A alteração repõe as quantidades e guarda as anteriores

A alteração traz a referência declarada, substitui as duas quantidades pelas informadas
e grava; o órgão, a coordenadoria, a secretaria, o mês e o ano da referência não mudam.
A auditoria guarda o conteúdo anterior e o novo.

### RN-19 — Os totais do órgão só são repostos quando a referência é a mais nova

A declaração e a alteração também repõem os **totais do órgão** no **cadastro de órgãos
filho**: a quantidade de matriculados e a de comensais do órgão passam a ser as da
referência informada. A reposição só acontece quando essa referência é a **mais nova do
órgão** — declarar ou alterar um mês anterior aos já declarados não mexe nos totais do
órgão. E ela **não** acontece quando já existe **mapa de atendimento** para o órgão e a
coordenadoria: nesse caso os totais do órgão não são repostos por esta tela.

[?] O acervo mostra que o mapa de atendimento manda mais que a declaração, mas não
explica o que é esse mapa em negócio nem por que ele impede a reposição: o mapa
consolida o mês e passa a ser a fonte dos totais do órgão, ou o mapa apenas trava a
declaração? Pergunta ao site.

### RN-20 — A exclusão apaga a referência e repõe os totais pela remanescente mais nova

Passadas as guardas, a exclusão traz a referência e a apaga do cadastro; a auditoria
guarda o conteúdo apagado. Em seguida, se ainda sobrar referência para o órgão, os
totais do órgão são repostos com as quantidades da **remanescente mais nova** — e essa
reposição também não acontece quando já existe mapa de atendimento para o órgão e a
coordenadoria.

[?] Se a referência apagada era a última do órgão, os totais do órgão não são mexidos e
ficam com as quantidades de um mês que já não existe no cadastro. Se isso é intencional
— o órgão mantém o último volume conhecido — ou é esquecimento, o acervo não diz.
Pergunta ao site.

### RN-21 — A exclusão é recusada quando já existem pedidos para o mês/ano

Antes de apagar, o sistema procura **pedido** daquele órgão, daquela coordenadoria, mês
e ano no **cadastro de pedidos**. Havendo, a recusa é **\* Ja existem pedidos para este
Mes/Ano \***, com o cursor na coluna da ação, e a referência continua declarada.

### RN-22 — Nada é gravado sem as conferências de acesso da operação

Antes de listar e de gravar cada linha, a tela repassa o contexto da sessão às rotinas
comuns de segurança e de rota. Sem a tela autorizada no perfil, a operação não segue; e
se a operação pretendida — inclusão, alteração ou exclusão — não constar do perfil de
acesso do servidor, a linha não é validada e nada é gravado nem auditado.

[?] A conferência da operação distingue inclusão, alteração e exclusão, mas não a
consulta: quem tem a tela autorizada consulta sem o perfil de consulta — e a consulta
acaba conferida contra o indicador de exclusão, porque a tela não liga o indicador geral
que desvia dessa conferência. Se isso é intencional ou defeito, o acervo não diz.
Pergunta ao site.

### RN-23 — Falha de banco interrompe a operação e avisa

Toda leitura e toda gravação testam o erro do banco. A falha de leitura e a de exclusão
viram o aviso de erro de leitura, e a de gravação vira o aviso de erro de gravação — os
dois despachados pela rotina de comunicação do sistema — e a transação para ali, sem
completar o resto.

---

## Cenários BDD

```gherkin
Funcionalidade: Referência mensal de matriculados e comensais do órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C203T

  Cenário: RN-01, RN-07 e RN-11 — consultar as referências declaradas de um órgão
    Dado que estou na tela C203T no modo CON
    E informo um órgão filho do meu escopo, que já tem referências declaradas
    Quando confirmo a consulta
    Então vejo o nome do órgão, a coordenadoria e o indicador de creche do cadastro
    E vejo, nas 13 linhas da página, o mês, o ano, os matriculados, os comensais e a ação de cada referência
    E nada é gravado

  Cenário: RN-02 — campo digitado que não é número
    Quando informo no órgão, na coordenadoria, no mês, no ano ou nas quantidades algo que não é número
    Então o campo recusado recebe de volta o cursor
    E o cadastro não é lido

  Cenário: RN-03 — modo da página diferente de ALT e de CON
    Dado que estou na tela C203T
    Quando informo um modo de página diferente de ALT e de CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-04 — consulta sem órgão informado
    Dado que estou na tela C203T no modo CON
    Quando confirmo sem informar o órgão filho
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão

  Cenário: RN-05 — órgão não cadastrado
    Quando informo um órgão filho que não existe no cadastro
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nenhuma referência é mostrada

  Cenário: RN-06 — órgão de outra coordenadoria
    Dado que o meu vínculo tem coordenadoria regional escolar
    Quando informo um órgão filho de outra coordenadoria
    Então vejo "* <- Usuario sem acesso a este grupo *"
    E o cursor fica no campo do órgão
    E o órgão não fica selecionado

  Cenário: RN-08 — órgão sem referência declarada
    Dado que consultei um órgão filho que não tem nenhuma referência
    Então não vejo linha alguma
    E vejo "* Orgao sem registros cadastrados *"
    E nada é gravado

  Cenário: RN-09 — linha sem mês/ano ou com ação desconhecida
    Dado que estou na tela C203T no modo ALT
    Quando deixo uma linha com o mês/ano zerado, ou com a ação em branco, ou com uma ação diferente de I, A e E
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada
    E nenhuma gravação acontece

  Cenário: RN-10, RN-17 e RN-19 — declarar um mês/ano novo
    Dado que consultei o órgão e ele ainda não tem o mês/ano informado
    E a referência informada é a mais nova do órgão
    E informo as quantidades de matriculados e de comensais
    Quando marco a ação I e confirmo
    Então a referência fica declarada com o órgão, a coordenadoria, a minha secretaria, o mês, o ano e as quantidades
    E os totais do órgão passam a ser os da referência declarada
    E cada gravação fica registrada na auditoria

  Cenário: RN-19 — declarar um mês/ano anterior aos já declarados
    Dado que consultei o órgão e já existem referências de meses mais novos
    Quando declaro um mês/ano anterior, com as quantidades, na ação I
    Então a referência fica declarada
    E os totais do órgão não são mexidos

  Cenário: RN-19 — órgão com mapa de atendimento
    Dado que existe mapa de atendimento para o órgão e a coordenadoria
    Quando declaro ou altero uma referência na ação I ou A
    Então a referência é gravada
    E os totais do órgão não são repostos por esta tela

  Cenário: RN-12 — declarar um mês/ano que já está declarado
    Dado que consultei o órgão e ele já tem o mês/ano informado
    Quando marco a ação I e confirmo
    Então vejo "* Mes/Ano ja cadastrado *"
    E o cursor fica na coluna da ação
    E nada é gravado

  Cenário: RN-13 — alterar um mês/ano que não está declarado
    Dado que consultei o órgão e ele não tem o mês/ano informado
    Quando marco a ação A e confirmo
    Então vejo "* Mes/Ano nao cadastrado *"
    E o cursor fica na coluna da ação
    E nada é gravado

  Cenário: RN-13 — excluir um mês/ano que não está declarado
    Dado que consultei o órgão e ele não tem o mês/ano informado
    Quando marco a ação E e confirmo
    Então vejo "* Mes/Ano nao cadastrado *"
    E o cursor fica na coluna da ação
    E nada é apagado

  Cenário: RN-14 — quantidade de matriculados em branco ou zero
    Dado que consultei o órgão e o mês/ano está declarado ou é novo
    Quando confirmo a linha com a quantidade de matriculados em branco ou zero
    Então vejo "* Quantidade de matriculados invalida *"
    E o cursor fica na coluna da quantidade
    E nada é gravado

  Cenário: RN-14 — quantidade de comensais em branco ou zero
    Quando confirmo a linha com a quantidade de comensais em branco ou zero
    Então vejo "* Quantidade de comensais invalida *"
    E o cursor fica na coluna da quantidade
    E nada é gravado

  Cenário: RN-14 — comensais maior que matriculados
    Quando confirmo a linha com mais comensais do que matriculados
    Então vejo "* Comensais > que matriculados *"
    E o cursor fica na coluna da quantidade
    E nada é gravado

  Cenário: RN-15 — alterar sem ter consultado o mesmo órgão
    Dado que estou na tela C203T no modo ALT
    E o órgão informado não é o que a última consulta deixou carregado
    Quando confirmo
    Então vejo "* Consulte antes de alterar *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: RN-16 — mês ou ano fora da faixa válida
    Quando informo um mês diferente de 1 a 12, ou um ano anterior a 1994 ou posterior a 2099
    Então vejo "* Mes/Ano invalidos *"
    E o cursor fica no campo do mês
    E nada é gravado

  Cenário: RN-10, RN-18 e RN-19 — alterar as quantidades de um mês declarado
    Dado que consultei o órgão e ele tem o mês/ano declarado
    E a referência é a mais nova do órgão
    Quando mudo as quantidades, marco a ação A e confirmo
    Então as quantidades da referência passam a ser as informadas, e o mês, o ano, o órgão e a secretaria não mudam
    E os totais do órgão passam a ser as quantidades novas
    E a auditoria guarda o conteúdo anterior e o novo

  Cenário: RN-10 e RN-20 — excluir uma referência declarada
    Dado que consultei o órgão e ele tem o mês/ano declarado
    E não há pedido para esse mês/ano
    Quando marco a ação E e confirmo
    Então a referência é apagada do cadastro
    E os totais do órgão passam a ser os da referência remanescente mais nova
    E a auditoria guarda o conteúdo apagado

  Cenário: RN-21 — excluir quando já existem pedidos para o mês/ano
    Dado que consultei o órgão e ele tem o mês/ano declarado
    E já existe pedido para esse órgão, essa coordenadoria, esse mês e esse ano
    Quando marco a ação E e confirmo
    Então vejo "* Ja existem pedidos para este Mes/Ano *"
    E o cursor fica na coluna da ação
    E a referência continua declarada

  Cenário: RN-22 — operação sem autorização
    Dado que o meu perfil de acesso não tem a operação pedida na linha
    Quando confirmo
    Então vejo a mensagem de recusa da segurança
    E nada é gravado nem auditado

  Cenário: RN-23 — falha de banco na gravação
    Dado que a gravação da referência falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com o aviso de erro do sistema
    E a referência não é considerada gravada
```

