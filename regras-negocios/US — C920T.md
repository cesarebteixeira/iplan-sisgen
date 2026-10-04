# US — C920T — Conferir período e planejamento semanal

## Estória

Como **servidor de CRE**, quero **declarar o grupo, o segmento, a semana e o período
de validade com que quero trabalhar e ver o que já existe para essa combinação**,
para que **eu saiba, antes de mexer em cardápio, se o período tem cardápios
cadastrados e se o planejamento da semana já foi montado — e siga daí para a tela
que monta o planejamento**.

O planejamento da semana é o que liga cada refeição de cada dia a um cardápio: sem
ele, o período pode ter cardápios cadastrados e mesmo assim não haver o que servir.
Esta tela é a conferência que antecede essa montagem — o servidor escolhe a
coordenação regional escolar, o segmento, a semana (A, B, C ou D) e a data limite de
validade, e o sistema responde se o grupo existe, se o segmento existe, se a semana é
válida, se aquele período tem cardápios e se o planejamento já existe. Se o servidor
tivesse de descobrir isso abrindo o cadastro de cada peça, a montagem do planejamento
viraria tentativa e erro.

## Contexto

Jornada S000M → C000M → C800M → C900M → C920T.

Ator: servidor de CRE — escolhe o grupo, o segmento, a semana e o período de validade
com que vai trabalhar e confere o que já existe para essa combinação antes de seguir
para a tela que monta o planejamento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O contexto que a tela usa — o tipo
de órgão e a coordenação regional escolar da sessão — é o que a entrada deixou; a
tela não o recalcula. O que ela deixa para a tela seguinte está na última regra.

---

## Regras de negócio

### RN-01 — A tela abre em consulta e repõe a consulta a cada apresentação

A tela abre sempre em modo de consulta. Se o operador chegar com outra operação
anotada, o sistema não a executa: ele repõe a consulta e avisa **\* Opcao nao
disponivel. Use CON \***, deixando o cursor no campo da opção, antes de qualquer
leitura de cadastro. Ao fim da apresentação, a operação gravada volta a ser a
consulta, de modo que uma passagem seguinte nunca herde outra operação.

[?] A recusa existe como texto, mas a guarda que a protege pode torná-la
inalcançável. Para o aviso sair é preciso que a operação anotada seja diferente da
consulta; no caminho em que a operação anotada é lida para a tela, ela já foi
forçada à consulta pela própria abertura. Ou a recusa vale para um caso que o acervo
não mostra, ou o trecho ficou sem uso. Pergunta ao site.

### RN-02 — O cadastro desta tela é o planejamento semanal: uma semana por grupo, segmento, refeição e período

O cadastro consultado tem **um registro por semana, por grupo, por segmento, por
refeição e por período de validade**: o tipo de órgão, a coordenação regional escolar,
a semana, o segmento, a refeição e o dia, o mês e o ano limite formam a chave, com
repetição admitida no fim, e o registro guarda **os sete cardápios da semana** — um
para cada dia, de segunda a domingo. A capacidade declarada do cadastro é de
**100.000 registros** (capacidade é o máximo esperado, parâmetro de dimensionamento,
não o que está cadastrado).

[?] O cadastro traz ainda **duas marcas de uma posição e um código de cinco dígitos**
cujo significado não está no acervo lido nem no manual: a marca de estimativa e o
código de cardápio que não é o código do planejamento. A tela lê os dois e não os
exibe. Pergunta ao site.

### RN-03 — A tela lê também a coordenação, o segmento, a refeição e os cardápios do período

Para responder, a tela lê mais quatro cadastros, todos **dentro do tipo de órgão da
sessão**: a **coordenação regional escolar** (que traz a descrição do grupo e o
vínculo desse grupo com a refeição), o **segmento** (que traz a descrição do
segmento), a **refeição** (que traz a descrição da refeição) e os **cardápios** (que
trazem o período e a marca de estimativa de cada cardápio). Nenhum deles é alterado:
esta tela só lê.

### RN-04 — A tela confere a coordenação regional escolar informada

A coordenação regional escolar informada é procurada no cadastro de coordenações,
dentro do tipo de órgão da sessão. Não achando, o sistema avisa **\* Grupo nao
cadastrado \***, devolve o cursor ao campo da coordenação e não segue: o segmento, a
semana e o período informados não são conferidos nem listados.

### RN-05 — A semana tem de ser A, B, C ou D

A semana informada tem de ser **A, B, C ou D**. Campo em branco ou qualquer outra
letra é recusado com **\* Informe semana com A, B, C ou D \***, com o cursor de volta
ao campo da semana, e nada é listado.

### RN-06 — A tela confere o segmento informado

O segmento informado é procurado no cadastro de segmentos, dentro do tipo de órgão da
sessão. Não achando, o sistema avisa **\* Segmento nao cadastrado \***, devolve o
cursor ao campo do segmento e não segue.

### RN-07 — A data limite de validade tem de estar completa

O dia, o mês e o ano limite do período têm de estar preenchidos: faltando qualquer um
dos três, o sistema avisa **\* Informe a data limite de validade \*** e devolve o
cursor ao campo do dia limite. Sem a data limite completa não se procura período.

### RN-08 — O período começa no cardápio que tem aquela data limite de validade

Preenchida a data limite, a tela procura, no cadastro de cardápios, o período
registrado para aquela data limite e para o tipo de órgão da sessão. **O operador não
informa a data de início**: o dia, o mês e o ano de início do período vêm do cardápio
encontrado. Não havendo cardápio com aquela data limite, o sistema avisa **\* Nao
existem cardapios neste periodo \***, devolve o cursor ao campo do dia limite e não
lista nada.

[?] A procura leva também, como parte da chave, um **código de cardápio sempre
zerado**, e o acervo não mostra nenhum caminho que preencha esse código — nem nesta
tela, nem nas telas irmãs. Se todo cardápio fica com o código zerado, a procura acha
qualquer um que sirva pela data; se algum caminho não lido preenche esse código, a
procura pela data deixa de achar. Pergunta ao site.

### RN-09 — Achado o período, a tela diz se o planejamento da semana existe

Achado o período, a tela procura o **planejamento daquela semana** — mesmo grupo,
mesmo segmento, mesma semana A a D, mesmo período e mesma refeição, dentro do tipo de
órgão da sessão. Achando, mostra o que ele tem para cada dia; não achando, avisa
**\* Grupo/Semana/Segmento sem planejamento cadastr \*** e não lista os cardápios dos
dias. **Esse aviso é decidido na montagem da primeira posição da lista e não é
repetido nas demais.**

[?] O aviso de planejamento ausente está no mesmo caminho que confere se existem
cardápios no período, e é a primeira condição a ser testada depois das conferências
de grupo, semana, segmento e data limite: quando não há planejamento, a conferência
de cardápios do período não chega a acontecer. Se a falta de planejamento deve
esconder também a falta de cardápios, ou se o aviso devia sair depois dessa
conferência, o acervo não diz. Pergunta ao site.

### RN-10 — A lista tem treze posições, uma por refeição, com os cardápios dos sete dias

A lista da tela tem **treze posições**, e cada posição tem **oito informações**: o
**código da refeição** e os **sete cardápios** dos dias de segunda a domingo. O que a
tela procura e mostra é o planejamento da semana por refeição; a descrição do
segmento encontrado e a marca de estimativa lida do cardápio acompanham a
apresentação.

[?] Quantas posições a tela chega a preencher de uma vez não se conclui do acervo. A
montagem percorre as treze posições, mas o percurso está amarrado a uma marca de
segunda passagem cujo estado inicial o acervo não mostra. Se as treze posições da
lista aparecem preenchidas de uma vez, ou só a primeira até o operador pedir a
seguinte, é pergunta ao site.

### RN-11 — A tela indica se a refeição é de creche, e a marca sempre sai "Nao"

A tela mostra se a refeição vale para creche, escrevendo **Sim** ou **Nao** conforme
uma marca da refeição. A marca é reinicializada em branco toda vez que a sessão
começa a usar esta tela, e **nenhum caminho da tela a põe em "sim"**: na prática o
campo sai sempre "Nao".

[?] A marca que decide o "Sim"/"Nao" é carregada de uma área da sessão que a tela
reinicializa e nunca preenche; se alguma tela anterior ou posterior pode preenchê-la —
e quando o campo deveria mostrar "Sim" —, o acervo não mostra. Pergunta ao site.

### RN-12 — A tela não grava nada

Esta tela só lê e mostra. Nenhum registro é incluído, alterado ou excluído em nenhum
cadastro, e nenhum registro de auditoria é gerado. As operações de gravação, de
exclusão e de travamento de registro existem **declaradas** para os sete cadastros
que a tela enxerga, mas **nenhum caminho da tela as executa**: declarar não é
executar. Em particular, o cadastro do planejamento semanal é lido por esta tela e não
é gravado por ela.

### RN-13 — Terminada a conferência, a tela passa o serviço adiante

Quando o período tem cardápios e o planejamento da semana **não** existe, a tela
encaminha para a tela seguinte, que é a que monta o planejamento da semana, e deixa
o modo de consulta ligado ao sair. A jornada da tela seguinte tem a sua própria
estória.

[?] A passagem para a tela seguinte está condicionada a uma marca de "planejamento
novo" que **não é conferida em lugar nenhum**: ela é lida da mensagem que chegou, não
tem valor inicial no acervo e nenhum caminho a escreve. Se a passagem depende da
máscara oferecer essa marca ao operador, e o que a tela seguinte aproveita do que
esta deixa, o acervo não responde. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Conferir o período e o planejamento da semana antes de montá-lo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C920T

  Cenário: Período com cardápios e planejamento já montado
    Dado que informo uma coordenação regional escolar cadastrada
    E informo um segmento cadastrado
    E informo a semana A, B, C ou D
    E informo o dia, o mês e o ano limite de um período que tem cardápios
    Quando envio a conferência
    Então vejo o período, o segmento e as refeições com os cardápios dos sete dias

  Cenário: Operação diferente da consulta
    Dado que estou na tela C920T
    Quando chego com uma operação diferente da consulta
    Então a tela repõe a consulta
    E vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor fica no campo da operação

  Cenário: Coordenação regional escolar não cadastrada
    Dado que informo uma coordenação regional escolar que não existe
    Quando envio a conferência
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo da coordenação
    E a semana e o período informados não são conferidos

  Cenário: Semana fora de A, B, C ou D
    Dado que informo a semana em branco ou com uma letra diferente de A, B, C e D
    Quando envio a conferência
    Então vejo a mensagem "* Informe semana com A, B, C ou D *"
    E o cursor volta ao campo da semana
    E nada é listado

  Cenário: Segmento não cadastrado
    Dado que informo um segmento que não existe
    Quando envio a conferência
    Então vejo a mensagem "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento

  Cenário: Data limite de validade incompleta
    Dado que deixo em branco o dia, o mês ou o ano limite
    Quando envio a conferência
    Então vejo a mensagem "* Informe a data limite de validade *"
    E o cursor volta ao campo do dia limite
    E nenhum período é procurado

  Cenário: Nenhum cardápio com aquela data limite
    Dado que informo uma data limite para a qual não há cardápio cadastrado
    Quando envio a conferência
    Então vejo a mensagem "* Nao existem cardapios neste periodo *"
    E o cursor volta ao campo do dia limite
    E nenhuma refeição é listada

  Cenário: Planejamento da semana não montado
    Dado que o período tem cardápios
    E não há planejamento para aquela semana, segmento e período
    Quando envio a conferência
    Então vejo a mensagem "* Grupo/Semana/Segmento sem planejamento cadastr *"
    E a tela passa o serviço para a tela de montagem do planejamento

  Cenário: O início do período vem do cardápio, não do operador
    Dado que informo o dia, o mês e o ano limite
    Quando a conferência encontra o cardápio daquela data limite
    Então o dia, o mês e o ano de início que vejo são os do cardápio encontrado

  Cenário: A lista tem treze posições
    Dado que o período e o planejamento foram encontrados
    Quando a lista é mostrada
    Então cada posição traz o código de uma refeição e os cardápios dos sete dias
    E a lista para na décima terceira posição

  Cenário: A tela não grava nada
    Dado que abro a tela C920T
    Quando a lista é mostrada
    Então nenhum registro é incluído, alterado ou excluído em nenhum cadastro
    E nenhum registro de auditoria é gerado

  Cenário: Toda apresentação recomeça em consulta
    Dado que já conferi um período nesta tela
    Quando a tela é apresentada de novo
    Então a operação mostrada é outra vez a consulta
```
