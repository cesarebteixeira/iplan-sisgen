# US — C875T — Copiar o planejamento oficial de um grupo para o período da estimativa

## Estória

Como **servidor de CRE**, quero **pedir que o planejamento oficial de um grupo seja
aproveitado nos planejamentos do período da estimativa**, para que o período novo já
nasça planejado — o cardápio de cada dia da semana e as quantidades de cada mês —, sem
redigitar, dia a dia e mês a mês, um planejamento que já existe.

A alimentação escolar é planejada por cardápio: há o **planejamento oficial**, já
cadastrado para um período, e há os **planejamentos** que a secretaria mantém para o
período da estimativa — quais cardápios valem em cada dia da semana e quantos cardápios
cada mês leva. Quando o período novo repete o que já está oficialmente planejado, o
trabalho é o mesmo, e sem esta tela o período novo teria de ser remontado à mão. O pedido
não é a cópia: a tela recolhe o grupo, o período da estimativa e o período do planejamento
oficial, confere os três, pergunta a impressora, pede a confirmação e é o processamento
do sistema que copia e imprime. A cópia não acontece na hora: a tela registra o pedido e
o entrega ao processamento, que roda fora da transação — o servidor recebe o aviso, vai
embora sem ver o resultado, e o período novo só fica planejado depois que ele termina.

## Contexto

Jornada S000M → C000M → C800M → C811M → C875T.

Ator: servidor de CRE — pede que o planejamento oficial de um grupo, cadastrado para um
período, seja copiado para os planejamentos do período da estimativa, informando o grupo,
os dois períodos e a impressora.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As três telas do meio do caminho são **menus** — o `C000M`, o `C800M` e a `C811M` —, e
nenhuma delas passa registro nem operação para esta: elas apenas chamam a tela pelo nome,
e a `C875T` repõe por conta própria o modo de manutenção com que trabalha. A `C875T` abre
sozinha, **sempre no modo de alteração**, e o que ela usa da sessão — o tipo de órgão, a
matrícula, a coordenação regional escolar do servidor, a estação e a data e a hora da
sessão — foi deixado pela entrada. A tela recebe o código da tela que a chamou e o
entrega à lógica de rota da entrada, mas não o compara com nada: o comportamento dela
**não muda conforme quem a chamou**.

A tela também não encadeia em outra: terminado o pedido ela **reabre a si mesma**, primeiro
para mostrar a pergunta de confirmação e depois para avisar que o cadastro está sendo
atualizado. O que ela entrega não vai para uma tela seguinte, e sim para o processamento
do sistema: o grupo, os dois períodos e a impressora. É esse processamento — e não a tela
— que copia o planejamento oficial para os planejamentos do período da estimativa e que
imprime o relatório da cópia.

As regras abaixo são só as da tela desta jornada e do processamento que ela dispara. As da
entrada estão no documento dela; as que se revelaram pertencer à entrada estão registradas
no **anexo de evidências**, na seção própria.

---

## Regras de negócio

### RN-01 — A tela pede a cópia do planejamento oficial para os planejamentos do período da estimativa

A tela trabalha com **dois períodos** e um **grupo**. O período da **estimativa** tem a
**data inicial** e a **data limite**; o período do **planejamento** tem a **data inicial**
e a **data limite**. A tela confere os dois, pergunta a **impressora**, pede a confirmação
e, só com a resposta afirmativa, registra o pedido e o entrega ao processamento do
sistema.

Quem copia não é a tela (RN-13). Ela recolhe o pedido, confirma e dispara; o resultado não
volta para ela — o servidor vê **\* Cadastro sendo atualizado \*** e acompanha depois. O
que o processamento faz com o planejamento oficial que consumiu não é dito ao servidor:
ele não recebe aviso disso na tela.

### RN-02 — A tela é do órgão da sessão, e o órgão não é digitável

Ao abrir, a tela mostra a **data do sistema** e a **descrição do tipo de órgão da sessão**;
não há campo de órgão nem de secretaria — todas as consultas da tela são do órgão do
servidor. É esse tipo de órgão que limita o que a tela procura e o que o processamento
copia.

### RN-03 — A tela só opera em modo de alteração

A tela se apresenta sempre no modo de alteração. Acionada em qualquer outro modo de
manutenção, a operação é recusada com **\* Opcao nao disponivel. Use ALT \*** e nada é
gravado.

[?] A recusa manda usar ALT e a conferência aceita apenas o código da alteração; o acervo
não traz a correspondência entre a tecla e o código. Ou o terminal traduz a tecla antes de
enviar, ou a mensagem está desalinhada da conferência. Pergunta ao site.

[?] O programa recebe o código da tela que chamou esta e o entrega à lógica de rota da
entrada, mas não o compara com nada: nesta tela o comportamento não muda conforme a
origem. Se a rota da entrada decide alguma coisa com esse código, isso não está nos fontes
desta jornada. Pergunta ao site.

### RN-04 — O grupo é obrigatório, e o grupo 99 vale por todos

O **grupo** — o código da coordenação regional escolar a que o planejamento pertence —
tem de ser informado: em branco, a recusa é **\* Informe o grupo \***, com o cursor de
volta no campo, e nenhum cadastro é lido.

O grupo 99 não é um grupo: com ele, as conferências de planejamento são feitas **sem o
grupo** — isto é, valem para qualquer um —, e o processamento repete a cópia para cada
coordenação cadastrada do órgão.

[?] A tela aceita qualquer grupo de 1 a 99 e não confere o grupo informado com a
coordenação do servidor; se há restrição por perfil, o fonte desta jornada não mostra.
Pergunta ao site.

[?] Com o grupo 99 a procura leva a coordenação **zerada**: se isso alcança o planejamento
de qualquer coordenação ou só o de uma coordenação de valor zero depende do posicionamento
da leitura, que o acervo não explica — no segundo caso, a tela recusaria um período que o
processamento saberia copiar. Pergunta ao site.

### RN-05 — O grupo informado é a coordenação que vale para os planejamentos

A tela mostra um campo de coordenação regional escolar do período da estimativa, mas quem
vale é o **grupo**: antes das consultas, a tela repõe o grupo nesse campo, e é por ele que
os planejamentos do período da estimativa são procurados. O que o servidor digitar nesse
campo é descartado sem aviso.

### RN-06 — São quatorze valores numéricos, e nenhuma data passa pelo calendário

Os valores numéricos da tela — o **grupo**, a **coordenação da estimativa** e as **doze
partes** das quatro datas (dia, mês e ano da data inicial e da data limite de cada período)
— passam pela conferência numérica do sistema: campo em branco vira zero, os zeros à
esquerda são descartados e o que não for número é recusado antes de qualquer consulta.

Nenhuma das doze partes passa pelo calendário, e não há conferência de ordem entre a data
inicial e a data limite de nenhum dos dois períodos.

[?] Dos quatorze valores conferidos como número, **sete** têm posição de cursor. Quando o
servidor digita algo que não é número na coordenação da estimativa ou nas três partes da
data inicial de qualquer dos dois períodos, a tela recusa o campo mas não sabe onde pôr o
cursor. Pergunta ao site.

[?] Se a falta de conferência de calendário e de ordem é proposital, o fonte não diz: a
tela aceita, por exemplo, um dia que não existe naquele mês, e quem decide passa a ser a
conferência do cadastro (RN-07 e RN-09). Pergunta ao site.

### RN-07 — A data limite da estimativa tem de ter cardápio cadastrado, e é dela que sai a data inicial da estimativa

Para a **data limite da estimativa** informada, a tela procura, no órgão da sessão, o
**cardápio cadastrado** que termina naquela data. Não achando, a recusa é
**\* Cardapios nao cadastrados para esta data \***, com o cursor no dia limite da
estimativa, e nada é gravado. Achando, a **data inicial da estimativa** deixa de ser a
digitada e passa a ser a data inicial daquele cardápio; é essa data que a tela repõe no
lugar da digitada e a que segue no pedido.

[?] A procura leva o código do cardápio zerado e, do que ela acha, a tela só reconfere o
órgão e as três partes da data limite — o código do cardápio não é reconferido. O que os
modificadores da leitura fazem não está no corpus nem no manual: se a leitura for a de uma
chave exata, só o cardápio de código zero serve; se ela apenas se posicionar, serve
qualquer cardápio do órgão que termine naquela data. Não escolho entre os dois desfechos.
Pergunta ao site.

### RN-08 — Já havendo planejamento no período da estimativa, a cópia é recusada

Antes de pedir a confirmação, o sistema procura, no **período da estimativa** e no
**grupo** informado, os dois planejamentos do período: o **planejamento** — os cardápios
de cada dia da semana, por segmento e por refeição — e o **planejamento sazonal** — as
quantidades de cardápios de cada mês, por segmento e por refeição. Achando o primeiro, a
recusa é **\* Planejamentos ja cadastrados \***; achando o segundo, **\* Planejamentos
sazonais ja cadastrados \***; achando os dois, a recusa é a primeira. O cursor volta ao
dia limite da estimativa e nada é gravado.

A tela é quem garante que a cópia não vai somar-se a um planejamento já existente: a
cópia só é pedida para um período que ainda não tenha planejamento nenhum.

[?] A procura leva o órgão, as três partes da data limite e o grupo, mas, do que acha, a
tela reconfere só o órgão e as três partes da data limite — **não reconfere o grupo**. Se
a leitura for a de uma chave exata, o efeito é "achou, recusa"; se ela apenas se
posicionar, um planejamento de outro grupo também recusa a cópia. Não escolho entre os
dois desfechos. Pergunta ao site.

### RN-09 — O período do planejamento tem de ter planejamento oficial cadastrado, e é dele que sai a data inicial do planejamento

Para a **data limite do planejamento** informada, a tela procura o **planejamento
oficial** desse grupo — ou de qualquer grupo, quando o grupo é 99 (RN-04). Não achando, a
recusa é **\* Planejamento oficial nao cadastrado \***, com o cursor no dia limite do
planejamento, e nada é gravado. Achando, a **data inicial do planejamento** deixa de ser a
digitada e passa a ser a data inicial daquele planejamento oficial. É esse planejamento
oficial que a cópia leva para o período da estimativa.

[?] As duas datas iniciais nunca são conferidas — nem contra o calendário, nem contra a
data limite, nem entre si — e é a própria tela que as substitui pelas dos cadastros que
achou (RN-07 e esta regra). O que o servidor digita nelas é descartado sem aviso. Pergunta
ao site.

### RN-10 — A impressora é obrigatória

A cópia sai impressa, e o destino da impressão é informado na tela: deixando a impressora
em branco, a recusa é **\* Informe a impressora \***, com o cursor de volta no campo, e
nada é gravado.

### RN-11 — A cópia é confirmada pelo servidor, e os dados conferidos não podem mudar

Passadas as conferências, a tela repõe as quatro datas — com as duas datas iniciais vindas
dos cadastros (RN-07 e RN-09) — e pergunta
**\* Confirma copia dos planejamentos <S/N> ? \***, com o cursor na resposta. Só a
resposta afirmativa segue para o registro.

Junto com a resposta, os dados que a tela guardou têm de continuar iguais: o grupo e as
duas datas limite, a da estimativa e a do planejamento. Alterado qualquer um deles, a tela
não aproveita a resposta: refaz as conferências e pergunta de novo.

[?] Responder N — ou deixar a resposta em branco — não cancela o pedido: a tela limpa a
resposta e volta às conferências, que pedem a mesma confirmação outra vez. Não há, no
caminho lido, um desfecho que encerre a operação com a resposta negativa. Pergunta ao
site.

[?] A comparação dos "dados inalterados" olha o grupo e as duas datas limite e **não olha
as datas iniciais** dos dois períodos. Como é a tela que repõe essas datas a partir dos
cadastros, trocá-las entre a pergunta e a resposta não faz a tela refazer as conferências,
e o pedido segue com o que estiver em tela. O fonte não diz se é proposital. Pergunta ao
site.

[?] A pergunta e a resposta acontecem em duas passagens da mesma transação, e a passagem
que pergunta marca a transação como falha para obrigar a tela a se reapresentar — e a
passagem seguinte começa recusando rodar quando essa marca está posta. O acervo lido não
mostra quem limpa a marca entre uma passagem e a seguinte; se ninguém limpar, a resposta
S não chega ao trecho que grava. Pergunta ao site.

### RN-12 — Um pedido de cópia em andamento impede outro

Antes de registrar, o sistema procura uma **solicitação de processamento pendente** deste
mesmo serviço — a cópia dos planejamentos —, com a situação em branco e o número do pedido
zerado; existindo, a recusa é **\* Relatorio em processamento. Aguarde. \***, a confirmação
é desfeita e nada é registrado. O pedido só pode ser feito quando não há outro em
andamento.

[?] A procura não examina o órgão, o grupo, a data nem a situação do pedido: um pedido de
outro órgão, de outro grupo, ou um já atendido e ainda não retirado, também bloqueia. E a
própria tela registra o pedido **sem marcar a situação** — quem o marca como atendido não
está nos fontes desta jornada; quem o apaga é o processamento, ao terminar (RN-16).
Enquanto isso, a cópia não pode ser pedida outra vez. Pergunta ao site.

### RN-13 — A tela não copia: registra o pedido e dispara o processamento

Confirmada a operação, a tela grava a **solicitação de processamento** com o número
seguinte da fila, o código do serviço, o órgão da sessão, a data e o mês da sessão, a
matrícula, a estação e a impressora, com a situação em branco, e entrega o serviço ao
processamento com os parâmetros do pedido — o grupo, os dois períodos —, **uma cópia** e o
**e-mail cadastrado do servidor**. Em seguida avisa **\* Cadastro sendo atualizado \*** e
reabre a si mesma. A tela não espera pelo resultado.

[?] A entrega do serviço depende de indicadores do ambiente — o produto em execução e o
retorno da gravação — cujo valor e origem não estão nos fontes desta jornada: quando ela
não acontece, o pedido fica registrado mas o serviço não é entregue. Pergunta ao site.

[?] O número do pedido é o seguinte ao último já usado na fila; a tela não escolhe o número
sozinha, ela o lê da fila e incrementa. Se duas sessões pedirem ao mesmo tempo, o fonte
desta jornada não permite dizer o que acontece. Pergunta ao site.

[?] O e-mail do pedido vem do cadastro do funcionário pela matrícula da sessão; não
achando o cadastro, a tela segue com o e-mail em branco e o pedido é registrado assim
mesmo. O fonte não diz se é proposital. Pergunta ao site.

### RN-14 — O processamento copia o planejamento oficial, dia a dia, para o período da estimativa

O processamento enfileirado relê os parâmetros do pedido e percorre, para o tipo de órgão
do pedido, as coordenações regionais cadastradas — a do pedido, ou todas, quando o grupo é
99. Em cada coordenação, toma o **planejamento oficial** do período informado e, para
**cada um dos sete dias da semana**, confere o cardápio previsto contra o período da
estimativa: o cardápio tem de estar cadastrado nos cardápios daquele período, não pode
estar cadastrado como sobremesa, tem de ter composição para o segmento do planejamento
oficial e tem de ter refeição cadastrada. O que passa vira registro do **planejamento** do
período da estimativa, com a data inicial e a data limite daquele período; o que já
existir naquele período é deixado como está. A mesma passagem leva o **planejamento
sazonal** do período informado para o sazonal do período da estimativa — as quantidades de
cada mês —, conferindo antes se já existe. Terminada a cópia, o processamento imprime o
relatório.

[?] O avanço de uma coordenação para a seguinte não é incrementado no programa: depende do
posicionamento da leitura, que o acervo não explica. Pergunta ao site.

### RN-15 — O que não tem lastro no período da estimativa não é copiado e sai no relatório

Nada é copiado à força: cada dia da semana e cada cardápio do planejamento oficial que não
encontra lastro no período da estimativa não vira registro e sai **impresso**, com o
motivo na linha. São seis motivos para o planejamento e um para o sazonal:

| # | motivo impresso | o que faltou |
| --- | --- | --- |
| 1 | planejamento oficial não cadastrado | o período informado não tem planejamento oficial daquela coordenação |
| 2 | cardápio não cadastrado na estimativa | o cardápio do dia não está cadastrado no período da estimativa |
| 3 | cardápio cadastrado como sobremesa | o cardápio está marcado como sobremesa no período da estimativa |
| 4 | cardápio não cadastrado neste segmento | o cardápio não tem composição para o segmento do planejamento oficial |
| 5 | cardápio não cadastrado nesta semana | o planejamento oficial manda um código de semana sem cardápio no período da estimativa |
| 6 | cardápio não cadastrado nesta refeição | o cardápio não tem a refeição do planejamento oficial |
| 7 | planejamento sazonal não cadastrado | o período informado não tem o sazonal daquela coordenação |

É por esse relatório que o servidor descobre o que precisa cadastrar para completar a
cópia.

### RN-16 — O processamento consome o planejamento oficial e, no fim, libera a fila

Ao percorrer o período informado, o processamento **apaga** os registros do planejamento
oficial que não têm refeição e, no sazonal, os que tiverem coordenação, segmento ou
refeição zerados — sem copiá-los e sem imprimir aviso. Terminada a cópia, apaga os pedidos
deste serviço do órgão e libera a fila: é isso que permite pedir a cópia de outro período
(RN-12).

[?] Os registros do período informado que não têm refeição — e, no sazonal, os que têm
coordenação, segmento ou refeição zerados — são apagados em silêncio, e não copiados. O
acervo não diz o que esses registros são nem por que são consumidos pela cópia. Pergunta
ao site.

### RN-17 — A cópia confirmada fica registrada na auditoria

Antes do pedido, a tela grava o **registro de auditoria** da operação: a tela, a operação
de inclusão, a data e a hora da sessão, o órgão, a coordenação regional escolar do
servidor, a matrícula e a estação, com os **parâmetros do pedido** — o órgão, o grupo e as
quatro datas — guardados como valor anterior e o valor posterior vazio.

[?] O número do processo da auditoria recebe o **dia** da data inicial da estimativa, um
número de 1 a 31, e não o número do pedido criado; como é esse número que distingue um
registro do outro na trilha, cópias do mesmo dia feitas pelo mesmo servidor caem na mesma
identificação. Ou o processo desta cópia é mesmo o dia, ou o campo ficou com o valor
errado. Pergunta ao site.

### RN-18 — A tela não inclui, não altera e não exclui planejamento nenhum

A tela apenas **lê** os cadastros de que precisa — o de telas, o de cardápios, os dois de
planejamento, o de planejamento oficial, o do funcionário e o de requisições. As rotinas de
gravação, de exclusão e de travamento existem declaradas para os **oito** cadastros que a
tela enxerga, mas **só duas gravações são executadas** nesta transação: a do registro de
auditoria (RN-17) e a da solicitação de processamento (RN-13) — nenhuma delas é a cópia.
Não há nenhuma exclusão e nenhum travamento. Declarar não é executar.

### RN-19 — Falha de banco interrompe a transação

Todo acesso ao banco é conferido: o erro de leitura e o de gravação são despachados pela
rotina de comunicação do sistema, e a transação para ali, sem completar o resto — a
auditoria e o pedido não chegam a ser gravados.

### RN-20 — A tela exibe a descrição do órgão e a data do sistema

Além dos campos informados e da linha de mensagem, a tela mostra a **descrição do tipo de
órgão** do servidor e a **data do sistema**. Nenhuma das duas é digitada: as duas vêm da
sessão.

---

## Cenários BDD

```gherkin
Funcionalidade: Copiar o planejamento oficial de um grupo para o período da estimativa

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C875T

  Cenário: RN-01, RN-04 a RN-11, RN-13, RN-14 e RN-17 — copiar o planejamento oficial para os planejamentos do período da estimativa
    Dado que estou na tela C875T, no órgão da minha sessão
    E existe cardápio cadastrado terminando na data limite da estimativa que vou informar
    E não existe planejamento nem planejamento sazonal no período da estimativa que vou informar
    E existe planejamento oficial terminando na data limite do planejamento que vou informar
    Quando informo o grupo, as quatro datas e a impressora, e envio os dados
    Então vejo "* Confirma copia dos planejamentos <S/N> ? *"
    E a data inicial da estimativa passa a ser a data inicial do cardápio cadastrado
    E a data inicial do planejamento passa a ser a data inicial do planejamento oficial
    Quando respondo S
    Então vejo "* Cadastro sendo atualizado *"
    E a solicitação de processamento fica registrada com o órgão da minha sessão, a data da sessão, a minha matrícula, a estação, a impressora e a situação em branco
    E o serviço é entregue ao processamento com o grupo, os dois períodos, uma cópia e o meu e-mail
    E a operação fica registrada na auditoria
    E nenhum planejamento é incluído, alterado ou excluído por esta tela

  Cenário: RN-02 e RN-20 — a tela abre no órgão da sessão e com a data do sistema
    Dado que entrei com um usuário de um tipo de órgão
    Quando a tela C875T abre
    Então vejo a data do sistema e a descrição do meu tipo de órgão
    E não há campo de órgão nem de secretaria

  Cenário: RN-03 — modo de manutenção diferente de alteração
    Dado que estou na tela C875T
    Quando aciono a tela em um modo de manutenção diferente de ALT
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E nada é gravado

  Cenário: RN-04 — grupo não informado
    Dado que estou na tela C875T
    Quando deixo o grupo em branco e envio os dados
    Então vejo "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nenhum cadastro é consultado

  Cenário: RN-04 — grupo 99 confere os planejamentos de qualquer grupo e percorre as coordenações
    Dado que estou na tela C875T
    Quando informo o grupo 99 e envio os dados
    Então as conferências de planejamento são feitas sem o grupo
    E o serviço é entregue com o grupo 99
    E o processamento repete a cópia para cada coordenação cadastrada do órgão

  Cenário: RN-05 — o grupo informado é a coordenação que vale
    Dado que a tela mostra uma coordenação da estimativa diferente do grupo que vou informar
    Quando informo o grupo e envio os dados
    Então os planejamentos do período da estimativa são procurados por esse grupo
    E a coordenação da estimativa mostrada passa a ser o grupo informado

  Cenário: RN-06 — valor não numérico
    Dado que estou na tela C875T
    Quando informo, num dos valores numéricos, algo que não é número
    Então o campo é recusado pela conferência numérica antes de qualquer consulta
    E nada é gravado

  Cenário: RN-06 — data fora do calendário não é recusada por isso
    Dado que estou na tela C875T
    Quando informo, numa das quatro datas, um dia que não existe naquele mês
    Então a tela não recusa a data por isso
    E quem decide é a conferência do cadastro

  Cenário: RN-07 — não há cardápio cadastrado na data limite da estimativa
    Dado que estou na tela C875T e informei o grupo
    Quando informo, na data limite da estimativa, uma data que não é o fim de um cardápio cadastrado no meu órgão
    Então vejo "* Cardapios nao cadastrados para esta data *"
    E o cursor volta ao dia limite da estimativa
    E nada é gravado

  Cenário: RN-07 — a data inicial da estimativa vem do cardápio cadastrado
    Dado que existe cardápio cadastrado terminando na data limite da estimativa que vou informar
    Quando informo uma data inicial da estimativa que não é a daquele cardápio e envio os dados
    Então a data inicial da estimativa deixa de ser a que digitei
    E passa a ser a data inicial daquele cardápio

  Cenário: RN-08 — já existe planejamento no período da estimativa
    Dado que estou na tela C875T e informei o grupo
    E existe cardápio cadastrado na data limite da estimativa que vou informar
    E já existe planejamento cadastrado no período da estimativa, no meu grupo
    Quando envio os dados
    Então vejo "* Planejamentos ja cadastrados *"
    E o cursor volta ao dia limite da estimativa
    E nada é gravado

  Cenário: RN-08 — já existe planejamento sazonal no período da estimativa
    Dado que estou na tela C875T e informei o grupo
    E existe cardápio cadastrado na data limite da estimativa que vou informar
    E não existe planejamento, mas existe planejamento sazonal no período da estimativa
    Quando envio os dados
    Então vejo "* Planejamentos sazonais ja cadastrados *"
    E o cursor volta ao dia limite da estimativa
    E nada é gravado

  Cenário: RN-09 — não há planejamento oficial no período informado
    Dado que estou na tela C875T, informei o grupo e passei pelas conferências de cardápio e de planejamento
    Quando informo, na data limite do planejamento, uma data em que não há planejamento oficial do grupo
    Então vejo "* Planejamento oficial nao cadastrado *"
    E o cursor volta ao dia limite do planejamento
    E nada é gravado

  Cenário: RN-09 — a data inicial do planejamento vem do planejamento oficial
    Dado que existe planejamento oficial terminando na data limite do planejamento que vou informar
    Quando informo uma data inicial do planejamento que não é a daquele planejamento oficial e envio os dados
    Então a data inicial do planejamento deixa de ser a que digitei
    E passa a ser a data inicial daquele planejamento oficial

  Cenário: RN-10 — impressora não informada
    Dado que estou na tela C875T e passei por todas as conferências de cadastro
    Quando deixo a impressora em branco e envio os dados
    Então vejo "* Informe a impressora *"
    E o cursor volta ao campo da impressora
    E nada é gravado

  Cenário: RN-11 — os dados conferidos mudam entre a pergunta e a resposta
    Dado que já vi a pergunta de confirmação
    Quando altero o grupo, ou uma das duas datas limite, e respondo S
    Então a tela não aproveita a resposta
    E refaz as conferências e pergunta de novo "* Confirma copia dos planejamentos <S/N> ? *"
    E nada é registrado antes de eu responder S

  Cenário: RN-11 — resposta diferente de S
    Dado que já vi a pergunta de confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a tela refaz as conferências e pede a mesma confirmação outra vez
    E nada é registrado

  Cenário: RN-12 — já existe um pedido em processamento
    Dado que existe uma solicitação de cópia dos planejamentos já registrada, de qualquer órgão, sem situação marcada
    Quando confirmo a operação com a resposta S
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E a confirmação é desfeita e nenhuma solicitação nova é registrada
    E nada é gravado

  Cenário: RN-14 — o processamento copia os sete dias da semana
    Dado que a solicitação de cópia foi registrada para um órgão, um grupo e dois períodos
    Quando o processamento assume o pedido
    Então, para cada dia da semana, o cardápio do planejamento oficial do período informado vira registro do planejamento do período da estimativa
    E o registro fica com a data inicial e a data limite do período da estimativa
    E o planejamento que já existir no período da estimativa é deixado como está

  Cenário: RN-14 — a cópia do planejamento sazonal
    Dado que o período informado tem planejamento sazonal
    Quando o processamento assume o pedido
    Então as quantidades previstas para cada mês são levadas para o planejamento sazonal do período da estimativa
    E o sazonal que já existir no período da estimativa é deixado como está

  Cenário: RN-15 — o que não tem lastro sai no relatório
    Dado que o planejamento oficial manda um cardápio que não está cadastrado na estimativa do período novo
    Quando o processamento assume o pedido
    Então aquele dia da semana não é copiado
    E o relatório mostra a linha daquele cardápio com o motivo da recusa

  Cenário: RN-16 — os registros sem identificação e a liberação da fila
    Dado que o período informado tem registros de planejamento oficial sem refeição
    Quando o processamento assume o pedido
    Então esses registros são apagados do período informado, sem aviso no relatório
    E, ao terminar a cópia, os pedidos deste serviço do órgão são apagados e a fila é liberada

  Cenário: RN-17 — a confirmação deixa registro na auditoria
    Dado que confirmei a operação com a resposta S
    Quando a operação termina
    Então a trilha de auditoria tem um registro desta tela, com a operação marcada como inclusão
    E o registro traz a minha matrícula, a minha estação, o órgão, a coordenação do servidor e a data e a hora da sessão
    E os parâmetros do pedido ficam guardados como valor anterior
    E o valor posterior fica vazio

  Cenário: RN-18 — a abertura da tela não grava nada
    Dado que tenho acesso à tela C875T
    Quando a tela abre, sem que eu envie dados
    Então vejo a data do sistema e a descrição do meu tipo de órgão
    E nenhuma solicitação de processamento é registrada
    E nada é anotado na auditoria

  Cenário: RN-18 — a tela não toca nos cadastros de planejamento
    Dado que confirmei a operação com a resposta S
    Quando a operação termina
    Então os cadastros de cardápios, de planejamento, de planejamento sazonal e de planejamento oficial continuam como estavam
    E o que passa a existir é a solicitação de processamento e o registro de auditoria

  Cenário: RN-19 — falha de banco na confirmação
    Dado que a gravação falha no banco
    Quando respondo S à pergunta de confirmação
    Então a transação é interrompida com a mensagem de erro do sistema
    E o pedido da cópia não é considerado criado
```
