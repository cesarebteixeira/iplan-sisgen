# US — C880T — Alterar o período da estimativa do órgão

## Estória

Como **servidor de CRE**, quero **alterar o período da estimativa do meu órgão**,
para que **a estimativa já montada passe a valer nas datas novas, sem eu ter de
redigitar o cardápio, as quantidades e o planejamento**.

A estimativa do órgão é montada para um período: o cardápio previsto, a sua
composição, as refeições, o planejamento por dia da semana, as quantidades por mês
e as médias ficam amarrados às datas de início e de limite desse período. Quando as
datas do período mudam, refazer tudo à mão é caro e abre margem a erro; esta tela
pede a mudança de uma vez, para o órgão inteiro. Ela não altera nada na hora:
registra o pedido, e o processamento que roda fora da transação é quem move os
cadastros para as datas novas.

## Contexto

Jornada S000M → C000M → C800M → C811M → C880T.
Ator: servidor de CRE — informa o período em vigor e o período novo do seu órgão,
confirma a alteração e recebe o aviso de que o cadastro está sendo atualizado.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. Os menus do caminho (C000M, C800M e
C811M) não gravam nada: eles apenas encaminham.

Esta tela não é menu: é tela de transação, e ela **encadeia na própria tela**. A cada
passagem ela reabre a si mesma em alteração, passando adiante o modo de operação e o
código da tela anterior; o período não viaja por esse encadeamento, ele fica guardado
na área de trabalho da sessão. É a mesma tela, o mesmo modo e a mesma sessão que
recebem a resposta da confirmação.

As regras abaixo são só as desta jornada.

---

## Regras de negócio

### RN-01 — A alteração move o período da estimativa do órgão

A estimativa é cadastrada por período, e o período são duas datas: uma **data de
início** e uma **data de limite**. O conjunto da estimativa vale entre essas duas
datas, e é por elas que os cadastros do período são alcançados. Esta tela troca essas
datas: o servidor informa o **período em vigor** e o **período novo** do órgão dele, e
o sistema move a estimativa de um para o outro.

A tela mostra a **descrição do órgão** e a **data do sistema**, que vêm da sessão e
não são digitadas, e uma linha de mensagem. O cadastro da estimativa comporta até
**100.000** registros — a capacidade é o máximo esperado declarado no dicionário de
dados, parâmetro de dimensionamento, não o volume cadastrado.

### RN-02 — A tela só tem a alteração

Esta tela não tem modo de consulta nem de inclusão: a cada abertura ela repõe a opção
de manutenção em **alteração**. Qualquer outra opção é recusada com
**\* Opcao nao disponivel. Use ALT \***, com o cursor no campo da resposta, antes de
qualquer leitura do cadastro da estimativa.

[?] A conferência interna recusa a passagem quando o modo que a tela repõe não é o de
alteração, e a mensagem pede que se use outra opção. Ou o terminal traduz o que o
servidor digita antes de enviar, ou a mensagem está desalinhada da conferência. Não
concluo qual dos dois é; pergunta ao site.

### RN-03 — O período é informado por doze campos, e sem número a tela não lê nada

O que a tela pede são **quatro datas**, cada uma em três campos — dia, mês e ano, o
ano com quatro dígitos: a data de início e a data de limite do período **em vigor**, e
a data de início e a data de limite do período **novo**. São **doze campos**, todos
numéricos, e os doze passam pela conferência numérica **antes** de qualquer leitura de
cadastro. O que não for número é recusado. Ao abrir, o cursor está no **dia da data de
limite do período em vigor**.

[?] Os doze campos passam pela conferência numérica, mas só **nove** têm posição de
cursor mapeada — os três da data de início do período em vigor não têm. Ou o terminal
valida esses três antes de enviar, ou a recusa fica sem apontar o campo. Pergunta ao
site.

### RN-04 — O período em vigor tem de ter estimativa, e o início vem do cadastro

A procura é feita pelo **órgão da sessão** e pela **data de limite do período em
vigor**; a data de início não entra na procura. Se não houver estimativa daquele órgão
com aquele limite, a alteração não é aceita:
**\* Registros de estimativa nao cadastrados \***, com o cursor no dia do limite em
vigor, e a transação para ali — nada é pedido.

Achado o cadastro, a tela repõe o **dia, o mês e o ano do início do período em vigor**
com os do cadastro da estimativa: o que tiver sido digitado ali é descartado. É essa
data reposta que segue para a pergunta de confirmação, para a trilha de auditoria e
para o pedido.

[?] O mesmo órgão e o mesmo limite podem ter mais de um cadastro de estimativa — um por
código de cardápio —, e a tela lê o primeiro, o de menor código. Se esses cadastros
tiverem datas de início diferentes, a data mostrada e conferida é a do primeiro, e não
se sabe qual delas o processamento toma. Pergunta ao site.

### RN-05 — A estimativa fechada não se reprograma

Estimativa **fechada** não se altera por esta tela:
**\* Cadastro fechado para este periodo \***, com o cursor no dia do limite em vigor, e
a transação para ali. O fechamento é um **estado gravado no próprio cadastro da
estimativa**, que esta tela apenas lê: enquanto o período estiver fechado, ela não
altera as datas dele.

### RN-06 — As datas novas têm de ser datas válidas

Cada uma das duas datas novas é conferida. Se a **data inicial nova** não passar, a
recusa é **\* Nova data inicial invalida \***, com o cursor no dia dela; se for a
**data final nova**, a recusa é **\* Nova Data final invalida \***, também com o cursor
no dia dela. Em qualquer dos dois casos nada é pedido.

A tela só aceita ano entre **1994** e **2099**; fora disso a data é inválida.

[?] A conferência do ano limita-se a 1994–2099 e compara o **ano informado com o ano
de hoje**, não com o ano que o sistema monta a partir das três partes da data; o
trecho que examina a data montada, logo depois, alimenta-se de outra área, a mesma que
a rotina de data deixou em branco. Ou a conferência alcança menos do que o desenho
pretendia, ou a área examinada não é a que eu li. Pergunta ao site.

### RN-07 — A data inicial nova não pode ser maior que a data final nova

Informado um período novo que começa depois de terminar, a recusa é
**\* Data inicial maior que data final \***, com o cursor no dia da data inicial nova,
e nada é pedido.

### RN-08 — O período novo não pode cair sobre estimativa já cadastrada

A tela procura estimativa do órgão pela **data de limite** dos cadastros, em duas
buscas: uma pela data em que o período novo **começa**, outra pela data em que ele
**termina**. Achando o cadastro e havendo interseção entre o período novo e o intervalo
dele, a alteração é recusada com **<- Cardapios ja cadastrados neste intervalo \***,
com o cursor no dia da data inicial nova, e nada é pedido.

A conferência é dispensada em um caso: quando a data procurada — o início do período
novo, na primeira busca, ou o limite do período novo, na segunda — coincide com a data
de limite do período em vigor.

[?] As duas buscas conferem o resultado apenas pelo órgão, sem reconferir as três
partes da data procurada, embora a chave de leitura as inclua. Se a leitura por chave
puder devolver um cadastro de outra data, a conferência conclui sobre um cadastro que
não é o pedido. Pergunta ao site.

### RN-09 — A alteração só segue com a confirmação S

Passadas as conferências, a tela ainda não altera nada: ela guarda o período informado,
pergunta **\* Confirma alteracao do periodo <S/N> ? \***, põe o cursor no campo da
resposta e devolve a mesma tela com a pergunta. Só a resposta **S**, com as datas iguais
às que foram guardadas na pergunta, leva adiante. Qualquer outra resposta — ou a troca
de qualquer uma das datas guardadas entre a pergunta e a resposta — desfaz a
confirmação e a tela volta à primeira passagem, refazendo as conferências e perguntando
de novo. Confirmada a resposta, a tela avisa **\* Cadastro sendo atualizado \***.

### RN-10 — A tela reabre a si mesma, em alteração

A única saída desta tela é ela mesma: a cada passagem o sistema passa adiante o modo
**alteração**, o código da tela anterior e o registro; a próxima abertura é a mesma
tela, no mesmo modo. O período conferido e o andamento da confirmação não viajam por
esse encadeamento — ficam guardados na área de trabalho da sessão, que a tela só
inicializa na primeira abertura.

### RN-11 — Só um pedido de alteração por vez, em todo o sistema

Enquanto houver um pedido desta operação na fila — de **qualquer órgão**, não só do
órgão do servidor —, a tela recusa com
**\* Relatorio em processamento. Aguarde. \***, com o cursor no campo da resposta, e
desfaz a confirmação: o servidor precisa informar o período de novo. Quem tira o pedido
da fila é o processamento, ao terminar de mover os cadastros.

[?] A procura do pedido em andamento usa só o código do relatório e não filtra a
situação do pedido. Se um pedido antigo já processado continuar na fila, a tela fica
bloqueada; se o processamento o apaga ao terminar, o bloqueio dura só o processamento.
Qual dos dois é o caso, pergunta ao site.

### RN-12 — A confirmação deixa registro na trilha de auditoria

Confirmada a alteração, o sistema grava um registro na trilha de auditoria com o tipo
de órgão, o período em vigor, o período novo, o número do processo, a matrícula, a
estação, a data e a hora. A operação fica registrada como uma **inclusão**, o cadastro
de origem é esta tela, e os dois períodos vão para o campo do **valor anterior**, com o
campo do valor posterior em branco.

[?] O número do processo recebe apenas o **dia da data de início do período novo** — um
número de 1 a 31 —, e não o órgão com o período, que é o que outras telas da mesma
família montam. Como é o número do processo que distingue um registro do outro na
trilha, alterações do mesmo dia feitas pelo mesmo servidor caem na mesma identificação.
Ou o processo deste período é mesmo o dia, ou o campo ficou com o valor errado. Pergunta
ao site.

### RN-13 — A tela não altera o cadastro da estimativa

Dos **cinco** cadastros que a tela enxerga, as rotinas de gravação e as de exclusão
estão **todas declaradas** e só **duas** rotinas de gravação são executadas: a da
trilha de auditoria e a do pedido. **Nenhuma** rotina de exclusão é executada, e o
cadastro da estimativa é apenas **lido**, em três procuras de conferência. Quem altera
as datas é o processamento da RN-15.

### RN-14 — A alteração é pedida ao processamento que roda fora da transação

Na passagem da confirmação, a tela lê o funcionário pela matrícula (para o correio
eletrônico), toma o número seguinte ao do último pedido da fila e cria o **pedido de
processamento** com o código do relatório, o tipo de órgão, o período em vigor, o
período novo, a matrícula, a estação e a data, e o entrega ao serviço de processamento
fora de linha. A tela então se reapresenta com **\* Cadastro sendo atualizado \***. Nada
é alterado na transação: o servidor recebe o aviso e vai embora sem ver o resultado.

[?] O que o **relatório** desta operação é, fora do processamento que a tela enfileira,
não tem fonte no acervo: o despacho que a tela monta é o mesmo trabalho genérico usado
por dezenas de telas, e o que distingue este pedido é o código do relatório gravado
nele. Se existir, no ambiente, um relatório impresso com esse código — ou um catálogo
que o nomeie —, ele não está no corpus. Pergunta ao site.

### RN-15 — O processamento move o período e libera a fila

O processamento enfileirado lê as estimativas do órgão e do período em vigor e, para
cada uma, reescreve as datas da **composição**, das **refeições** e da **própria
estimativa** para as datas do período novo; em seguida reescreve também as datas do
**planejamento por dia da semana**, das **quantidades por mês** e das **médias** do
período; no fim apaga o pedido e libera a fila. São **seis** cadastros movidos, e
nenhum deles é apagado.

### RN-16 — Falha de banco interrompe a transação

Toda leitura e toda gravação conferem o erro do banco, e a transação para ali, sem
completar o resto — a trilha de auditoria e o pedido não chegam a ser gravados. Depois
de cada gravação a tela ainda confere o sinal de aborto e sai antes de montar o pedido.

---

## Cenários BDD

```gherkin
Funcionalidade: Alterar o período da estimativa do órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C880T

  Cenário: RN-01 — o que a alteração alcança
    Dado que existe estimativa para o período em vigor do meu órgão
    Quando informo o período em vigor e o período novo
    Então vejo a descrição do meu órgão e a data do sistema
    E a estimativa do órgão passa do período em vigor para o período novo
    E o cadastro da estimativa comporta até 100.000 registros

  Cenário: RN-02 — a tela não tem consulta nem inclusão
    Dado que estou na tela C880T
    Quando informo uma opção de manutenção diferente da alteração
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E nenhuma estimativa é consultada

  Cenário: RN-03 — campo de data sem número
    Quando preencho o dia, o mês ou o ano de uma das quatro datas com algo que não é número
    Então a tela recusa o campo antes de ler qualquer cadastro
    E nenhuma estimativa é consultada

  Cenário: RN-04 — período em vigor sem estimativa cadastrada
    Quando informo uma data de limite em vigor que não corresponde a nenhuma estimativa do meu órgão
    Então vejo "* Registros de estimativa nao cadastrados *"
    E a transação para ali
    E nada é pedido

  Cenário: RN-04 — a data de início do período em vigor vem do cadastro
    Dado que existe estimativa para o meu órgão com a data de limite que vou informar
    Quando informo o período em vigor com uma data de início diferente da do cadastro
    Então a tela repõe o início com o do cadastro da estimativa
    E é essa data reposta que segue para a confirmação

  Cenário: RN-05 — estimativa fechada
    Dado que a estimativa do período em vigor já foi fechada
    Quando confirmo o período em vigor
    Então vejo "* Cadastro fechado para este periodo *"
    E nada é pedido

  Cenário: RN-06 — data nova inválida
    Quando informo uma data inicial nova ou uma data final nova inválida
    Então vejo "* Nova data inicial invalida *" ou "* Nova Data final invalida *"
    E o cursor fica no dia da data recusada
    E nada é pedido

  Cenário: RN-06 — ano fora do intervalo aceito
    Quando informo o ano de uma das datas novas fora de 1994 a 2099
    Então a data nova é considerada inválida
    E nada é pedido

  Cenário: RN-07 — início novo depois do fim novo
    Quando informo a data de início nova maior que a data de limite nova
    Então vejo "* Data inicial maior que data final *"
    E nada é pedido

  Cenário: RN-08 — período novo sobre estimativa já cadastrada
    Dado que existe estimativa do meu órgão encerrando na data em que o novo período começa
    Quando informo o período novo
    Então vejo "<- Cardapios ja cadastrados neste intervalo *"
    E nada é pedido

  Cenário: RN-09 — resposta diferente de S
    Dado que estou vendo a pergunta de confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a confirmação é desfeita e a tela volta a conferir o período
    E nada é pedido

  Cenário: RN-09 — datas trocadas entre a pergunta e a resposta
    Dado que estou vendo a pergunta de confirmação
    Quando troco qualquer uma das datas e respondo S
    Então a confirmação é desfeita
    E nada é pedido

  Cenário: RN-10 — a tela reabre a si mesma em alteração
    Dado que estou na tela C880T
    Quando a tela passa adiante o modo de operação e o código da tela anterior
    Então a mesma tela C880T reabre em alteração
    E o período conferido continua guardado na área de trabalho da sessão

  Cenário: RN-11 — já existe um pedido de alteração em andamento
    Dado que existe um pedido desta operação na fila, de qualquer órgão
    Quando informo o período em vigor
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E a confirmação é desfeita: preciso informar o período de novo
    E nada é pedido

  Cenário: RN-12, RN-13 e RN-14 — confirmar a alteração do período
    Dado que existe estimativa aberta para o período em vigor e nenhum pedido em andamento
    Quando respondo S à pergunta de confirmação
    Então o sistema grava o registro na trilha de auditoria
    E cria o pedido de processamento com o órgão, o período em vigor e o período novo
    E vejo "* Cadastro sendo atualizado *"
    E nenhum cadastro de estimativa é alterado nesta transação

  Cenário: RN-15 — o processamento move o período
    Dado que o pedido foi criado para um órgão, um período em vigor e um período novo
    Quando o processamento assume o pedido
    Então a composição, as refeições e a própria estimativa do período em vigor passam às datas novas
    E o planejamento por dia da semana, as quantidades por mês e as médias do período também passam às datas novas
    E o pedido é apagado ao fim, liberando a fila

  Cenário: RN-16 — falha de banco durante a confirmação
    Dado que a gravação falha no banco
    Quando respondo S à pergunta de confirmação
    Então a transação é interrompida com a mensagem de erro do sistema
    E o pedido não é considerado criado

  Cenário: sair sem confirmar não grava nada
    Dado que estou na tela C880T com o período informado e conferido
    Quando saio sem responder S à pergunta de confirmação
    Então nada é gravado na trilha de auditoria
    E nenhum pedido de processamento é criado
```
