# US — C076T — Manter as refeições, as semanas e a sobremesa do cardápio de um período

## Estória

Como **servidor de CRE**, quero **dizer quais refeições o cardápio de um período
oferece, em quais semanas do período ele está em vigor e qual é o cardápio de
sobremesa que o acompanha**, para que **o período sirva exatamente o que a minha
coordenação definiu, sem que a montagem da alimentação tenha de adivinhar pelo nome
do cardápio o que ele serve**.

Um cardápio não vale pelo nome: vale pela lista das refeições que ele oferece, pelas
semanas em que está em vigor e pela sobremesa que o acompanha. É essa lista que a
distribuição da alimentação consome — um cardápio registrado e sem refeição ligada
não serve nada. E depois que o cardápio já entrou no planejamento semanal de uma
semana ou de uma refeição, a tela não deixa mais desfazer o que já foi planejado.

## Contexto

Jornada S000M → C000M → C070M → C076T.

Ator: servidor de CRE — liga e desliga, no cardápio de um período, as refeições que
ele oferece, as semanas em que ele vale e o cardápio de sobremesa que o acompanha,
no âmbito do tipo de órgão da sua sessão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O `C000M` e o `C070M` são menus e não gravam nada; o contexto que esta tela usa —
matrícula, código de acesso, privilégio, tipo de órgão e coordenação regional — é o
que a entrada deixou na sessão. Quem mantém o cadastro dos cardápios é a **C070T** e
o cadastro das refeições é a **C100T**; esta tela não é nenhuma das duas: ela lê os
dois e liga um ao outro. A C070T também **encadeia** nesta tela, e o que ela deixa
registrado na sessão muda o modo com que a C076T abre (RN-04). A jornada termina
aqui: a C076T não passa registro nem operação para nenhuma tela seguinte.

---

## Regras de negócio

### RN-01 — O que a tela mantém: a ligação do cardápio com cada refeição do período

O cardápio é um registro do cadastro de cardápios (C072T) e é identificado pelo
**código do cardápio**, pelo **tipo de órgão** a que pertence e pela **data limite do
período**. O que esta tela mantém é a **ligação entre esse cardápio e cada refeição
servida no período**: um registro do cadastro de refeições do cardápio (C077T), de
**nove campos** — o tipo de órgão, o código do cardápio, o código da refeição, o dia,
o mês e o ano de início e o dia, o mês e o ano limite do período.

O cadastro das ligações é dimensionado para **100.000** registros e o dos cardápios
para **1.000.000** (capacidade é o máximo esperado, parâmetro de dimensionamento, não
o que está cadastrado). A ligação é lida pela combinação do tipo de órgão, do código
do cardápio, da data limite e do código da refeição; essa combinação **admite
repetição** no cadastro — quem garante que o mesmo par cardápio e refeição não esteja
ligado duas vezes no período é a própria tela, ao recusar a inclusão do que já existe
(RN-08).

### RN-02 — A consulta é pelo código do cardápio e pela data limite do período

O servidor informa o **código do cardápio** e o **dia, o mês e o ano limite** do
período. A tela procura o cardápio no cadastro, dentro do **tipo de órgão da sessão**,
pela combinação do código com a data limite; não achando, avisa
**\* Cardapio nao cadastrado neste periodo \*** e devolve o cursor ao campo do código
do cardápio — nesse caminho nada é listado. Achando, aquele passa a ser o cardápio em
tela e a lista das refeições é montada a partir dele.

[?] O dia, o mês e o ano de **início** do período são digitados, mostrados e
guardados, mas não entram em nenhuma das **24 leituras** que a tela faz (contagem por
chamada de leitura, no texto juntado: 8 no cadastro de cardápios, 6 nas ligações, 4 no
cadastro de refeições, 4 no planejamento semanal e 2 no cadastro de telas). O período é
identificado só pela data limite; se o início deveria distinguir duas versões do mesmo
cardápio com o mesmo limite, ou servir para conferir o que foi digitado, o acervo desta
jornada não diz. Pergunta ao site.

### RN-03 — A lista das refeições do cardápio, até 10 linhas por vez

A tela mostra as refeições ligadas ao cardápio no período, cada uma em uma linha, com
o **código da refeição**, a **descrição da refeição** e a **situação** da linha
(RN-07), **até 10 linhas por vez**. Terminadas as ligações, a lista para e as linhas
restantes ficam em branco.

Não havendo nenhuma refeição ligada ao cardápio, a tela avisa
**\* Cardapio sem refeicoes cadastradas \*** e devolve o cursor ao campo do código do
cardápio, sem preencher nenhuma linha. O aviso é decidido na montagem da **primeira**
linha da lista.

### RN-04 — Quem abre a tela decide o modo com que ela abre

A operação de manutenção com que a tela abre **não é digitada**: ela vem de quem
chamou a tela, pelo que ficou registrado na sessão.

- Aberta pela **C070T** — que encadeia nesta tela para completar o cardápio —, a
  C076T abre em **alteração**, já com o **cardápio, o período, as semanas e a
  sobremesa** daquele cardápio preenchidos. É a C070T que deixa esses valores na
  sessão antes de passar o controle, e é por isso que a alteração aqui já chega com o
  cardápio "consultado".
- Aberta pelo **menu C070M**, não há operação registrada e a tela assume a
  **consulta**, em branco — é esse o caminho da jornada.

[?] A C070T só encadeia quando um campo dela está marcado em tela (o do registro novo
de refeição), e a máscara das telas não está no lote lido: o rótulo desse campo — o
que o servidor marca, na C070T, para chegar aqui — não se sabe. Pergunta ao site.

### RN-05 — A tela só aceita consulta e alteração

Informada uma operação diferente de **consulta** e de **alteração** — inclusão,
exclusão ou qualquer outro valor —, a tela recusa com
**\* Opcao nao disponivel. Use ALT ou CON \*** e devolve o cursor ao campo da
operação; nesse caminho nada é lido nem mostrado. É por isso que esta tela **não
cria** e **não exclui** cardápio: ela só lê e altera o que já existe.

[?] A mensagem manda usar `ALT` e `CON`, grafias que não existem nos fontes desta
jornada — as operações que a tela compara são os códigos internos de consulta e de
alteração. Ou o formulário traduz o que o servidor digita para esses códigos, ou quem
seguir a mensagem é recusado. Pergunta ao site.

### RN-06 — A alteração exige que o cardápio já esteja em tela

A alteração só segue quando o **código do cardápio** e as **três partes da data
limite** informados são exatamente os do cardápio que já está em tela, isto é, o que
foi consultado. Sendo outros, a tela recusa com **\* Consulte antes de alterar \*** e
devolve o cursor ao campo da operação; nada é gravado. Na consulta, informar outro
cardápio apenas refaz a procura e troca o cardápio em tela.

### RN-07 — A situação de cada linha decide a operação, e a linha marcada exige a refeição

Cada linha tem uma **situação**: **I** inclui a ligação e **E** exclui a ligação.
Linha com situação em branco ou com outra letra é **ignorada** — não gera operação
nenhuma. Numa linha marcada para incluir ou para excluir, o **código da refeição é
obrigatório**: sem ele, a tela recusa com **\* Atualize linha preenchida \*** e
devolve o cursor ao campo da situação daquela linha. A operação de cada linha ainda
passa pela conferência de permissão correspondente — inclusão ou exclusão — antes de
qualquer leitura.

### RN-08 — A inclusão exige refeição cadastrada e ligação que ainda não exista

Para incluir, o sistema procura a ligação entre o cardápio em tela e a refeição
informada, no período. Já existindo, a inclusão é recusada com
**\* Cardapio ja cadastrado nesta refeicao \*** e o cursor volta ao campo da refeição
daquela linha. Não existindo, o sistema procura a refeição no cadastro de refeições
(C100T), dentro do tipo de órgão da sessão; não achando, recusa com
**\* Refeicao nao cadastrada \***, com o cursor no campo da refeição. Passando nas
duas conferências, a ligação é gravada.

[?] O cadastro de refeições guarda, em cada registro, a última operação que ele sofreu,
e a manutenção daquele cadastro recusa mexer no registro marcado como excluído; esta
tela não confere essa marca — só confere que a refeição existe. Se uma refeição marcada
como excluída pode continuar sendo ligada a um cardápio, o acervo desta jornada não diz.
Pergunta ao site.

### RN-09 — A exclusão exige a ligação e recusa o que já está no planejamento daquela refeição

Para excluir, a ligação entre o cardápio em tela e a refeição informada precisa
existir; não existindo, a tela recusa com
**\* Cardapio nao cadastrado nesta refeicao \***. Existindo, o sistema varre o
**planejamento semanal** do período (o cadastro C771T) — todas as semanas, todas as
coordenações e todos os segmentos do tipo de órgão da sessão — e, achando naquela
refeição algum dia planejado com este cardápio, recusa com
**\* Cardapio no planejamento desta refeicao \*** e devolve o cursor ao campo da
situação daquela linha. Não achando, a ligação é excluída.

### RN-10 — O cardápio de sobremesa do período

Na alteração, o servidor pode apontar o **cardápio de sobremesa** do período. O código
informado precisa ser o de um cardápio registrado **no mesmo período** — senão a tela
recusa com **\* Cardapio nao cadastrado neste periodo \***, com o cursor no campo do
código de sobremesa — e esse cardápio precisa estar marcado como **de sobremesa**; não
estando, a recusa é **\* Cardapio nao cadastrado como sobremesa \***. E o cardápio que
está sendo mantido **não pode ser ele próprio** um cardápio de sobremesa: sendo, a
tela recusa com **\* Cardapio cadastrado como sobremesa \*** e devolve o cursor ao
campo do código do cardápio. Deixando o campo em branco, o período fica sem
apontamento de sobremesa.

[?] O cadastro de refeições marca, em cada registro, se a refeição é básica e se é de
sobremesa, e esta tela lê esse cadastro sem conferir nenhuma das duas marcas — a
sobremesa do período é conferida no cadastro de cardápios, não no de refeições. Se a
refeição ligada a um cardápio de sobremesa deveria ser ela própria uma refeição de
sobremesa, o acervo desta jornada não diz. Pergunta ao site.

### RN-11 — As semanas do cardápio e o que já está no planejamento semanal

Dentro do período, o cardápio cobre um conjunto de semanas identificadas pelas letras
**A, B, C e D**. A tela traz as **quatro marcas** e a alteração grava no cardápio
exatamente as semanas que estiverem marcadas em tela — marca em branco deixa a semana
de fora. Antes de gravar, para cada semana que o cardápio cobre e que **não** está
marcada em tela, a tela confere o planejamento semanal do período: se o cardápio já
estiver no planejamento daquela semana, recusa com
**\* Cardapio no planejamento desta semana \*** e devolve o cursor à marca daquela
semana; nesse caminho nada é gravado.

[?] A conferência das semanas compara as marcas do **último cardápio lido**, e não
necessariamente as do cardápio que está em tela: quando o servidor informa uma
sobremesa, é a leitura que confere o cardápio de sobremesa que fica valendo como
última, e é dela que saem as marcas comparadas. Se as marcas deviam ser as do cardápio
mantido, a conferência olha o registro errado. Pergunta ao site.

[?] A conferência só tem efeito se o servidor puder apagar em tela a marca de uma
semana que o cardápio cobre. Como a máscara apresenta essas quatro marcas — se são
campo de digitação ou só de leitura — não está no lote lido; se forem só de leitura, a
recusa fica inalcançável e a semana nunca sai do cardápio. Pergunta ao site.

### RN-12 — O que a alteração grava, o que fica na auditoria e o que a tela não faz

Cada linha confirmada grava a sua ligação — inclusão ou exclusão. A alteração grava
também **o próprio cardápio**: as quatro marcas de semana e o código do cardápio de
sobremesa, uma vez por confirmação.

Cada operação gera **dois registros de auditoria**: um na **auditoria das operações**
(A010T), com a origem, a operação, o registro antes e o registro depois, a matrícula, a
estação, o tipo de órgão, a coordenação regional e a sessão (dia, mês, ano e hora); e
outro na **auditoria de campos** (C782T), com o campo alterado — a semana, ou a
refeição identificada — e as duas imagens. A alteração do cardápio entra na auditoria
das operações mesmo que só as refeições tenham mudado; a auditoria de campos recebe a
semana apenas quando alguma marca muda.

A **consulta não grava nada**: nenhuma ligação, nenhum cardápio e nenhum registro de
auditoria. A tela **não cria** cardápio — se ele não existe, a consulta o recusa — e
**não exclui** cardápio nenhum. As rotinas de gravar, de excluir e de travar existem
declaradas para os **sete cadastros** que a tela enxerga, mas o que se executa é a
gravação do cardápio, a gravação e a exclusão da ligação, a gravação das duas
auditorias e o travamento do cardápio e da ligação — declarar não é executar.

[?] A auditoria de campos identifica como origem da alteração a tela do cardápio
(**C070T**), mesmo quando a alteração foi feita aqui na C076T; a auditoria das
operações identifica a C076T. Se a divergência é intencional, o acervo desta jornada
não diz. Pergunta ao site.

### RN-13 — A digitação dos nove campos numéricos é editada

O código do cardápio, o dia, o mês e o ano de início, o dia, o mês e o ano limite, o
código do cardápio de sobremesa e o código da refeição — **nove campos** — passam por
edição numérica antes de qualquer leitura: campo em branco é tratado como zero e o que
não for número é recusado.

[?] A rotina que devolve o cursor ao campo recusado trata **seis** desses campos — o
código do cardápio, o dia, o mês e o ano limite, o código de sobremesa e o código da
refeição — e não trata o dia, o mês e o ano de início, embora os três passem pela
mesma edição: se a digitação de um deles for recusada, o cursor não é devolvido a ele.
Pergunta ao site.

[?] A rotina que faz a edição numérica não está entre os fontes desta jornada, então
não se sabe que mensagem o servidor vê quando a digitação é recusada. E o rótulo que a
tela entrega para o campo do código de sobremesa é o **nome interno do campo**, não um
rótulo de tela como o dos outros oito; se a mensagem usa esse rótulo, é o nome interno
que aparece. Pergunta ao site.

### RN-14 — A cada envio, o que a tela mostra é remontado

Antes de conferir a digitação e de ler qualquer cardápio, a tela apaga a descrição do
tipo de órgão, a data do sistema e as descrições do cardápio, do cardápio de sobremesa
e da refeição que a apresentação anterior havia mostrado. Uma consulta recusada não
deixa em tela o resultado da anterior.

Fora da lista, a tela exibe a **data do sistema** e a **descrição do tipo de órgão** da
sessão; as duas são copiadas da área de trabalho do módulo.

[?] O acervo desta jornada não mostra quem preenche a data do sistema e a descrição do
tipo de órgão na área de trabalho do módulo antes da primeira apresentação da tela — a
tela só as copia de lá. Se ninguém preencher, os dois campos saem em branco. Pergunta
ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter as refeições, as semanas e a sobremesa do cardápio de um período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C076T

  Cenário: A tela aberta pelo menu abre em consulta
    Dado que venho do menu C070M
    Quando abro a tela C076T
    Então a operação em tela é a consulta
    E não há cardápio nem período em tela

  Cenário: A tela encadeada pela C070T abre em alteração com o cardápio preenchido
    Dado que venho da tela do cardápio C070T, que me passou o controle
    Quando abro a tela C076T
    Então a operação em tela é a alteração
    E o cardápio, o período, as semanas e a sobremesa daquele cardápio já vêm preenchidos

  Cenário: Consulta das refeições do cardápio do período
    Dado que existe cardápio com o código e a data limite que vou informar
    Quando envio a consulta com o código do cardápio e a data limite do período
    Então vejo as refeições ligadas a esse cardápio, uma por linha, com o código e a descrição da refeição
    E nada é gravado

  Cenário: A lista mostra até 10 refeições por vez
    Dado que o cardápio tem mais de 10 refeições ligadas
    Quando envio a consulta
    Então a lista mostra no máximo 10 linhas
    E as linhas restantes ficam em branco

  Cenário: Consulta de cardápio que não existe no período
    Dado que não existe cardápio com o código e a data limite que informei
    Quando envio a consulta
    Então vejo a mensagem "* Cardapio nao cadastrado neste periodo *"
    E o cursor volta ao campo do código do cardápio
    E nenhuma linha é listada

  Cenário: Cardápio sem refeições ligadas
    Dado que o cardápio informado existe no período, mas não tem refeição ligada
    Quando envio a consulta
    Então vejo a mensagem "* Cardapio sem refeicoes cadastradas *"
    E o cursor volta ao campo do código do cardápio
    E nenhuma linha é preenchida

  Cenário: Operação diferente de consulta e de alteração
    Quando informo uma operação de manutenção que não é consulta nem alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido nem mostrado

  Cenário: Alteração sem consultar antes
    Dado que o cardápio informado não é o que está em tela
    Quando envio a alteração
    Então vejo a mensagem "* Consulte antes de alterar *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Inclusão de uma refeição no cardápio
    Dado que o cardápio está em tela e a refeição informada está cadastrada
    E que essa refeição ainda não está ligada a esse cardápio no período
    Quando informo a situação I na linha e confirmo a alteração
    Então a refeição passa a estar ligada ao cardápio no período
    E a operação é registrada nas duas auditorias

  Cenário: Inclusão de refeição que já está ligada ao cardápio
    Dado que a refeição informada já está ligada a esse cardápio no período
    Quando informo a situação I e envio a alteração
    Então vejo a mensagem "* Cardapio ja cadastrado nesta refeicao *"
    E o cursor volta ao campo da refeição daquela linha
    E nada é gravado

  Cenário: Inclusão de refeição não cadastrada
    Dado que o código de refeição informado não consta do cadastro de refeições
    Quando informo a situação I e envio a alteração
    Então vejo a mensagem "* Refeicao nao cadastrada *"
    E o cursor volta ao campo da refeição daquela linha
    E nada é gravado

  Cenário: Linha marcada para operação sem o código da refeição
    Dado que informei a situação I ou E numa linha e deixei o código da refeição em branco
    Quando envio a alteração
    Então vejo a mensagem "* Atualize linha preenchida *"
    E o cursor volta ao campo da situação daquela linha
    E nada é gravado

  Cenário: Linha sem situação ou com situação desconhecida é ignorada
    Dado que deixei a situação de uma linha em branco, ou informei outra letra
    Quando envio a alteração
    Então aquela linha não gera operação nenhuma

  Cenário: Exclusão de uma refeição do cardápio
    Dado que a refeição informada está ligada ao cardápio em tela
    E que o cardápio não está no planejamento semanal daquela refeição
    Quando informo a situação E na linha e confirmo a alteração
    Então a refeição deixa de estar ligada ao cardápio no período
    E a operação é registrada nas duas auditorias

  Cenário: Exclusão de ligação que não existe
    Dado que a refeição informada não está ligada ao cardápio em tela
    Quando informo a situação E e envio a alteração
    Então vejo a mensagem "* Cardapio nao cadastrado nesta refeicao *"
    E o cursor volta ao campo da refeição daquela linha
    E nada é gravado

  Cenário: Exclusão recusada porque o cardápio está no planejamento da refeição
    Dado que o cardápio em tela está no planejamento semanal do período, naquela refeição
    Quando informo a situação E e envio a alteração
    Então vejo a mensagem "* Cardapio no planejamento desta refeicao *"
    E o cursor volta ao campo da situação daquela linha
    E a refeição continua ligada ao cardápio

  Cenário: Semana do cardápio que o planejamento já usa não pode sair
    Dado que o cardápio cobre uma semana cuja marca está em branco em tela
    E que esse cardápio já está no planejamento daquela semana
    Quando confirmo a alteração
    Então vejo a mensagem "* Cardapio no planejamento desta semana *"
    E o cursor volta à marca daquela semana
    E nada é gravado

  Cenário: A alteração grava as semanas e a sobremesa no cardápio
    Dado que o cardápio está em tela e a alteração é confirmada
    Então o cardápio passa a ter as marcas de semana que estão em tela
    E o cardápio passa a apontar o cardápio de sobremesa informado

  Cenário: Cardápio de sobremesa apontado para o período
    Dado que o cardápio em tela não é um cardápio de sobremesa
    E que o código informado é de um cardápio do mesmo período, marcado como de sobremesa
    Quando confirmo a alteração
    Então o período passa a apontar esse cardápio de sobremesa

  Cenário: Código de sobremesa que não é cardápio do período
    Dado que o código informado não corresponde a nenhum cardápio do período
    Quando confirmo a alteração
    Então vejo a mensagem "* Cardapio nao cadastrado neste periodo *"
    E o cursor volta ao campo do código de sobremesa
    E nada é gravado

  Cenário: Código de sobremesa que não é cardápio de sobremesa
    Dado que o código informado é de um cardápio do período que não está marcado como de sobremesa
    Quando confirmo a alteração
    Então vejo a mensagem "* Cardapio nao cadastrado como sobremesa *"
    E o cursor volta ao campo do código de sobremesa
    E nada é gravado

  Cenário: Cardápio que já é de sobremesa não recebe sobremesa
    Dado que o cardápio em tela é ele próprio um cardápio de sobremesa
    E que informei um código de sobremesa
    Quando confirmo a alteração
    Então vejo a mensagem "* Cardapio cadastrado como sobremesa *"
    E o cursor volta ao campo do código do cardápio
    E nada é gravado

  Cenário: Cada operação da alteração fica nas duas auditorias
    Dado que confirmo uma alteração que liga ou desliga uma refeição do cardápio
    Então a auditoria das operações guarda a origem, a operação e os registros anterior e posterior
    E a auditoria de campos guarda o campo alterado e os registros anterior e posterior

  Cenário: A consulta não grava nada
    Dado que estou em modo de consulta
    Quando envio a consulta
    Então nenhuma refeição é ligada ou desligada do cardápio
    E o cardápio não é alterado
    E nenhum registro de auditoria é gerado

  Cenário: A tela não cria cardápio
    Dado que não existe cardápio com o código e a data limite informados
    Quando envio a alteração
    Então vejo a mensagem "* Consulte antes de alterar *"
    E nenhum cardápio é criado

  Cenário: A tela não exclui cardápio
    Dado que o cardápio está em tela
    Quando informo uma operação de exclusão
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cardápio continua cadastrado

  Cenário: Digitação não numérica é recusada
    Dado que digitei uma letra num campo numérico
    Quando envio a tela
    Então a tela recusa a digitação
    E a consulta não segue

  Cenário: O resultado anterior é apagado antes da conferência
    Dado que a apresentação anterior mostrou um cardápio e as suas refeições
    Quando envio uma consulta que é recusada
    Então as descrições do cardápio, da sobremesa e da refeição não ficam em tela

  Cenário: A data do sistema e o tipo de órgão da sessão
    Dado que entrei no sistema
    Quando abro a tela C076T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão
```
