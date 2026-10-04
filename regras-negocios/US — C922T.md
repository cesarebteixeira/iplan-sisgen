# US — C922T — Consultar o planejamento sazonal de cardápios de um grupo

## Estória

Como **servidor de CRE**, quero **consultar o planejamento sazonal de cardápios do meu
grupo — por segmento de atendimento, refeição e período —, vendo cada cardápio previsto
com as quantidades de cada mês**, para que **eu confira, antes de pedir os gêneros, o que
já está planejado para o período e em que meses cada cardápio entra**.

O planejamento sazonal de cardápios é o que diz quais cardápios estão previstos em cada
mês, por grupo, segmento de atendimento e refeição, e é dele que saem as quantidades
usadas nos pedidos de gêneros do período. Sem esta consulta, o servidor só vê o
planejamento abrindo o cadastro, ou descobre o que foi planejado depois que o pedido já
saiu. A tela é só de leitura: ela não inclui, não altera e não exclui planejamento
nenhum.

## Contexto

Jornada S000M → C000M → C800M → C900M → C922T (6 passos).

Ator: servidor de CRE — consulta o planejamento sazonal de cardápios do seu grupo pela
data limite de validade.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. Não repito as da entrada: o que
encontrei que pertence àquele arquivo está no **anexo de evidências**, na seção
`## Regras que se revelaram da entrada`.

As duas telas do meio do caminho — a C800M e o menu da C900M — apenas encaminham: não
gravam nada e não deixam modo nem registro preparado para esta tela. **Nenhuma tela
encadeia na C922T passando operação ou registro**: a C900M só manda abrir a C922T, e quem
decide em que modo ela abre é o próprio campo de operação dela. Também não há comparação
com a tela de origem que mude o comportamento dela; o que muda a abertura é o que a
sessão já trazia — o modo da última operação, o tipo de órgão, a coordenação regional
escolar e o grupo do servidor.

A C922T não encadeia para nenhuma outra: ela não passa registro nem operação adiante, e a
jornada termina nela. Ela enxerga **seis cadastros** — o dos grupos da coordenação, o dos
segmentos de atendimento, o das refeições, o dos cardápios, o do planejamento sazonal de
cardápios e o Título do próprio sistema — e **não grava nenhum deles**.

Todo recorte da consulta é o do **tipo de órgão da sessão**: o grupo, o segmento, a
refeição e o período são procurados dentro dele.

---

## Regras de negócio

### RN-01 — A tela é de consulta, e outra operação é recusada

A tela abre em consulta e repõe a consulta a cada apresentação, de modo que a opção
mostrada volta a ser sempre a consulta. Se o operador informar outra operação, o sistema
recusa com **\* Opcao nao disponivel. Use CON \***, devolve o cursor ao campo da opção e
**não lê** o cadastro do grupo, do segmento, da refeição nem o planejamento.

[?] A mensagem manda usar "CON", mas a conferência interna compara com o código de
consulta do sistema, e nenhum literal "CON" existe no acervo lido: ou o terminal traduz o
que o servidor digita antes de enviar, ou a mensagem indica um valor que a tela recusa.
Pergunta ao site.

[?] Como a apresentação repõe a consulta sozinha, a recusa só pode ser alcançada numa
mensagem seguinte do operador; se a máscara não oferecer o campo de opção, esse trecho não
se alcança. Pergunta ao site.

### RN-02 — A lista mostra até 11 cardápios, cada um com as quantidades de cada mês

A consulta apresenta, em **11 linhas**, o **código do cardápio**, a sua **descrição** e
as **quantidades previstas mês a mês**, de janeiro a dezembro. Fora da lista, a tela
mostra o grupo, o segmento e a sua descrição, a refeição e a sua descrição, as **datas de
início e limite** do período, a descrição do tipo de órgão da sessão e a data do sistema.
O limite de 11 linhas é fixado pelo próprio programa em todas as passagens da tela.

### RN-03 — O grupo, o segmento e a refeição precisam estar cadastrados

O grupo informado é procurado no cadastro dos grupos da coordenação; não estando lá, o
sistema avisa **\* Grupo nao cadastrado \*** e devolve o cursor ao campo do grupo. O
segmento é procurado no cadastro dos segmentos de atendimento; não estando, avisa
**\* Segmento nao cadastrado \*** e devolve o cursor ao campo do segmento. A refeição,
quando informada com código diferente de zero, é procurada no cadastro das refeições; não
estando, avisa **\* Refeicao nao cadastrada \*** e devolve o cursor ao campo da refeição.
Informar a refeição como zero dispensa essa conferência.

[?] O aviso do grupo chama de "grupo" um dado que o campo da tela rotula como coordenação
regional escolar, e o cadastro procurado guarda a descrição da coordenação. Se grupo e
coordenação são a mesma coisa, ou se o grupo é uma subdivisão dela, o acervo lido não diz.
Pergunta ao site.

### RN-04 — A data limite é obrigatória, e é ela que localiza o período

As três partes da data limite têm de estar preenchidas; faltando qualquer uma, o sistema
avisa **\* Informe a data limite de validade \*** e devolve o cursor ao campo do dia
limite. É a **data limite** — junto com o grupo, o segmento e a refeição — que localiza o
planejamento; a data de início não participa de nenhuma procura.

### RN-05 — A consulta exige cardápio no período e planejamento para o recorte

Achados o grupo, o segmento e a refeição, o sistema procura no cadastro dos cardápios
algum cardápio cuja validade termine na data limite informada; não havendo nenhum, avisa
**\* Nao existem cardapios neste periodo \*** e devolve o cursor ao campo do dia limite.
Em seguida procura o planejamento sazonal do tipo de órgão da sessão, da data limite, do
grupo, do segmento e da refeição informados; não havendo, avisa
**\* Cardapio sazonal nao cadastrado \*** e devolve o cursor ao campo do dia limite.

### RN-06 — Só a consulta trabalha a lista; é ela que carrega e mostra o planejamento

A montagem da lista só roda quando a operação é a consulta. Em qualquer outra operação a
tela sai antes de montar linha nenhuma. Na consulta, a tela lê o planejamento do recorte e
preenche cada linha com o código do cardápio, a descrição vinda do cadastro dos cardápios
e as doze quantidades mensais.

[?] Há ainda um terceiro aviso, **\* Segmento sem planejamento cadastrado \***, que sai da
montagem da lista quando a leitura do planejamento não acha nada para o que a conferência
já aceitou. Os dois trechos leem a mesma posição; se esse aviso é proteção contra o
planejamento mudar entre as duas passagens ou um trecho que já não se alcança, o acervo
não diz. Pergunta ao site.

### RN-07 — As linhas da lista saem zeradas e sem descrição na consulta

Na hora de apresentar, a tela **zera o código do cardápio e apaga a descrição de cada
linha** da lista, além de zerar as doze quantidades mensais de cada linha. É um passo
próprio da apresentação, que roda depois de o sistema ter carregado o planejamento.

[?] Ou a limpeza existe para a primeira apresentação, quando ainda não há planejamento
lido — e nesse caso o operador nunca vê os cardápios —, ou ela deveria poupar a consulta e
o acervo lido mostra o contrário. As duas leituras do mesmo trecho levam a resultados
diferentes; não escolho um dos dois. Pergunta ao site.

### RN-08 — Os campos informados são editados como número, e o cursor volta ao campo recusado

Os **vinte e dois campos digitáveis** — o grupo, o segmento, a refeição, as três partes da
data de início, as três partes da data limite, o código do cardápio e as doze quantidades
mensais — passam pela edição numérica **antes de qualquer leitura**: o que está em branco
vale zero, o que não for número é recusado e a consulta não segue. Recusada a digitação, o
cursor volta ao campo recusado — mas a tela só tem posição de cursor definida para o
grupo, o segmento, a refeição e as três partes da data limite; para os demais campos não
há onde posicionar.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não está
nos fontes desta jornada: a rotina que faz a edição numérica é importada e não tem corpo
no acervo lido. Pergunta ao site.

### RN-09 — A data de início mostrada é a do cardápio, não a digitada

Passando nas conferências, ficam valendo o grupo, o segmento, a refeição e a data limite
informados, mas a **data de início**, as descrições do segmento e da refeição e a marca de
estado vêm dos cadastros lidos. A data de início digitada é substituída pela do cardápio
encontrado. O próprio planejamento também guarda uma data de início, e ela não é usada: a
que aparece é a do cadastro dos cardápios.

[?] A data de início é digitada e editada, mas não é usada para procurar nem para
conferir. O acervo lido não mostra para que ela serve além de ser exibida. Pergunta ao
site.

### RN-10 — O código do cardápio digitado não entra na procura

O campo do código do cardápio é digitável e editado como número, mas **não é usado em
nenhuma leitura**: o código que aparece em cada linha da lista é o do planejamento lido.

[?] Ou o campo existe só para o operador se orientar, ou a digitação é ignorada; o acervo
lido mostra que ela não altera a lista, e não diz qual dos dois é o pretendido. Pergunta
ao site.

### RN-11 — Reenviar o que já está na tela não refaz a conferência

Se o operador reenviar exatamente o grupo, o segmento, a refeição e a data limite que já
foram aceitos, o sistema **não refaz** as conferências nem as procuras: a lista continua a
mesma.

### RN-12 — Cada consulta começa com os campos de resultado limpos

Antes de conferir a digitação e de ler qualquer cadastro, a tela apaga as descrições do
segmento, da refeição, do tipo de órgão e do cardápio, a marca de estado e a data do
sistema que a consulta anterior havia mostrado. Uma consulta recusada, portanto, não deixa
na tela o resultado da consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe um
caminho de entrada em que os campos não são limpos, é pergunta ao site.

### RN-13 — A tela mostra a data do sistema e a descrição do tipo de órgão da sessão

Fora da lista, a tela exibe a **descrição do tipo de órgão da sessão** e a **data do
sistema**.

[?] Nem a data do sistema nem a descrição do tipo de órgão são preenchidas por nenhum
caminho que o acervo mostre: as duas aparecem sempre como origem de cópia, nunca como
destino, e a entrada guarda a descrição do tipo de órgão em outra área da sessão. Se o
ambiente transporta o valor de uma área para a outra — e de onde vem a data do sistema —,
o acervo não diz; se não transportar, os dois campos saem em branco. Pergunta ao site.

### RN-14 — A consulta não grava nada e não deixa rastro de auditoria

A tela só lê. Nenhum registro é incluído, alterado, excluído ou travado, e nenhum registro
de auditoria é gerado: as operações de gravação, de exclusão e de travamento existem
declaradas para os seis cadastros que a tela enxerga, mas **nenhum caminho desta tela as
executa**.

[?] Quem alimenta o planejamento que esta tela mostra não é nenhuma tela do acervo lido: o
único ponto do acervo que grava esse cadastro é o processamento do relatório do período —
aquele que a tela C940T pede —, que o monta a partir do planejamento de estimativa, e quem
o apaga é o processamento do relatório de exclusão, que a tela C944T pede. Se esses
processamentos continuam rodando na operação, e o que exatamente eles copiam, não se
conclui das telas. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar o planejamento sazonal de cardápios de um grupo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C922T

  Cenário: Consulta do planejamento do grupo
    Dado que informo o grupo, o segmento, a refeição e a data limite de validade
    Quando envio a consulta
    Então vejo os cardápios previstos para o período, cada um com as quantidades de cada mês
    E vejo as descrições do grupo, do segmento, da refeição e do tipo de órgão da minha sessão

  Cenário: A lista mostra no máximo 11 cardápios
    Dado que há mais de 11 cardápios previstos para o recorte informado
    Quando envio a consulta
    Então a lista mostra no máximo 11 linhas
    E as linhas restantes ficam em branco

  Cenário: Cada linha traz as quantidades dos doze meses
    Dado que o planejamento tem quantidades previstas para o recorte informado
    Quando envio a consulta
    Então cada linha mostra as quantidades de janeiro a dezembro

  Cenário: A data de início mostrada não é a digitada
    Dado que o cardápio previsto tem data de início registrada
    Quando envio a consulta
    Então a data de início que vejo é a registrada no cadastro dos cardápios
    E não a que eu digitei

  Cenário: Código de cardápio informado não restringe a lista
    Dado que informo também um código de cardápio
    Quando envio a consulta
    Então a lista continua sendo a do planejamento do recorte informado

  Cenário: Refeição informada como zero dispensa a conferência
    Dado que deixo a refeição em branco
    Quando envio a consulta
    Então o sistema não confere se a refeição está cadastrada
    E segue procurando o planejamento do recorte

  Cenário: Reenviar o que já está na tela
    Dado que a tela já mostra o resultado de uma consulta
    Quando envio de novo exatamente os mesmos valores
    Então a conferência não é refeita
    E a lista continua a mesma

  Cenário: O resultado da consulta anterior não fica na tela
    Dado que já abri a tela e ela mostrou cardápios
    Quando volto a consultar
    Então as descrições, a marca de estado e as datas da consulta anterior não ficam na tela

  Cenário: Grupo não cadastrado
    Dado que informo um grupo que não existe
    Quando envio a consulta
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo do grupo

  Cenário: Segmento não cadastrado
    Dado que informo um segmento que não existe
    Quando envio a consulta
    Então vejo a mensagem "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento

  Cenário: Refeição não cadastrada
    Dado que informo uma refeição que não existe
    Quando envio a consulta
    Então vejo a mensagem "* Refeicao nao cadastrada *"
    E o cursor volta ao campo da refeição

  Cenário: Data limite incompleta
    Dado que deixo em branco o dia, o mês ou o ano da data limite
    Quando envio a consulta
    Então vejo a mensagem "* Informe a data limite de validade *"
    E o cursor volta ao campo do dia limite

  Cenário: Sem cardápio no período
    Dado que não há cardápio com validade terminando na data limite informada
    Quando envio a consulta
    Então vejo a mensagem "* Nao existem cardapios neste periodo *"
    E o cursor volta ao campo do dia limite

  Cenário: Sem planejamento sazonal para o recorte
    Dado que não há planejamento para o grupo, a data limite, o segmento e a refeição informados
    Quando envio a consulta
    Então vejo a mensagem "* Cardapio sazonal nao cadastrado *"
    E o cursor volta ao campo do dia limite

  Cenário: O planejamento desaparece entre a conferência e a lista
    Dado que a conferência aceitou o recorte e o planejamento dele deixa de existir
    Quando a tela monta a primeira linha da lista
    Então vejo a mensagem "* Segmento sem planejamento cadastrado *"
    E nenhuma linha da lista é preenchida

  Cenário: Operação diferente da consulta
    Dado que estou na tela C922T
    Quando informo uma operação diferente da consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nenhum cadastro é lido nesse caminho

  Cenário: Digitação não numérica
    Dado que digito algo que não é número em um dos campos informados
    Quando envio a consulta
    Então o sistema recusa a digitação antes de ler qualquer cadastro
    E o cursor volta ao campo recusado

  Cenário: A data do sistema e o tipo de órgão da sessão
    Dado que entrei no sistema
    Quando abro a tela C922T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: A consulta não grava nada
    Dado que abro a tela C922T
    Quando a lista é mostrada
    Então nenhum registro é incluído, alterado, excluído ou travado
    E nenhum registro de auditoria é gerado

  Cenário: As linhas da lista saem zeradas na consulta
    Dado que o planejamento do recorte existe e tem cardápios e quantidades
    Quando a tela apresenta a lista
    Então o código do cardápio e a descrição de cada linha saem em branco
    E as quantidades mensais de cada linha saem zeradas
```
