# US — C847T — Ajuste da quantidade estimada de gênero

## Estória

Como **servidor da Coordenação Regional Escolar (CRE)**, quero **ajustar a quantidade estimada
de um gênero de alimento em um período, dizendo o quanto e por quê**, para que **a estimativa da
alimentação escolar do meu grupo passe a refletir o que de fato vai ser servido, sem reescrever
a estimativa e sem perder o registro de quem mexeu nela**.

A estimativa da alimentação escolar é montada por grupo, subclasse e gênero e é detalhada por
refeição e por segmento de atendimento dentro de um período. Quando a quantidade prevista de um
gênero muda, o sistema não reescreve a previsão: lança um **ajuste** — quantos e por quê —, e é
esse ajuste que abate o saldo estimado do gênero e faz crescer a quantidade já ajustada. Esta
tela é onde o ajuste é lançado, alterado e desfeito. Sem ela, a correção da estimativa só
existiria por fora do sistema: sem motivo registrado e sem rastro de quem a fez.

## Contexto

Jornada S000M → C000M → C800M → C840M → C847T (5 passos).
Ator: servidor de CRE — informa o grupo, a subclasse, o gênero e o período, confere o preço e o
saldo estimados do gênero e lança, altera ou desfaz o ajuste de quantidade, com o motivo.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**,
não regra de negócio. Os menus do caminho — `C000M`, `C800M` e `C840M` — só encaminham e não
gravam nada.

A tela é alcançada de duas maneiras. Pela **opção 7 do menu `C840M`**, que apenas encaminha; e
por **encadeamento**, quando o servidor marca uma linha da estimativa na tela de consulta
`C846T` — que entrega a esta tela o grupo, a subclasse, o gênero, o período, a refeição e o
segmento daquela linha e marca a operação como alteração. No sentido contrário, esta tela, quando
o servidor pede a consulta, entrega o gênero à `C846T` (RN-14).

O modo com que a tela abre **não depende de quem a chamou**: o fonte não compara a tela de origem
com código de tela nenhum, e é a própria tela que repõe a alteração quando não encontra operação
guardada na sessão (RN-02). O contexto que ela consome — a matrícula, o privilégio, o tipo de
órgão e o grupo da sessão, e a data e a hora do sistema — é o que a entrada deixou; o **tipo de
órgão da sessão** entra na chave de tudo o que ela procura e grava, e é ele que limita o que a
tela alcança.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela mantém os ajustes da estimativa do gênero; ela lê dez cadastros e grava em quatro

A tela mantém os **ajustes** da estimativa de um gênero de alimento. Cada ajuste diz quanto se
ajustou, quanto isso vale pelo preço estimado do gênero e o motivo; lançá-lo **abate** o saldo
estimado do gênero e faz crescer a quantidade já ajustada, e desfazê-lo devolve o saldo. A tela
enxerga **dez** cadastros — o de telas, o dos ajustes, o da estimativa, o do detalhe da
estimativa, o dos gêneros, o dos gêneros da subclasse 99, o das refeições, o dos segmentos, o
dos grupos e o da auditoria —, mas só **grava em quatro**: no ajuste, no detalhe da estimativa,
na estimativa e na auditoria. Nos outros **seis** ela só lê, ainda que o sistema traga pronta,
para cada cadastro que a tela enxerga, uma rotina de gravar e uma de apagar: declarar não é
executar.

Os números de capacidade são de **dimensionamento** — o máximo esperado declarado no dicionário
de dados —, não volume cadastrado: a auditoria comporta 60.000.000 de registros; o detalhe da
estimativa, 500.000; o gênero, 150.000; o segmento, 200.000; a estimativa, o ajuste, o gênero da
subclasse 99 e o cadastro de telas, 100.000 cada um; a refeição, 1.200; o grupo, 1.000.

[?] Além do saldo, a tela mostra um segundo par de quantidade e valor, que só cresce quando um
ajuste é lançado e que os ajustes devolvem quando são desfeitos; descrevi-o como "já ajustado"
pela conta que a tela faz, mas a máscara não lhe dá rótulo e o material não define o que ele
significa em negócio. Pergunta ao site.

### RN-02 — A tela abre em alteração

Ao abrir, a tela procura na sessão a operação guardada para ela. Não achando — que é o que
acontece na primeira vez —, adota a **alteração** e passa a guardá-la; achando, é a operação
guardada que vale. Quem repõe o modo é a própria tela: não há comparação da tela de origem com
código de tela nenhum, de modo que o comportamento não muda conforme a tela que a chamou.

### RN-03 — Só alteração e consulta passam

A operação da tela aceita apenas **alteração** e **consulta**. Qualquer outra é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta ao campo da operação,
**antes de qualquer leitura de cadastro**.

[?] A recusa manda usar **ALT** e **CON**, mas o que a guarda aceita é o código interno da
alteração e o da consulta; nenhum documento do material lido diz que o terminal traduz o
mnemônico antes de enviar. Ou o formulário traduz, ou quem seguir a mensagem é recusado — e a
ficha da tela não lista rótulo para o campo da operação, de modo que a recusa pode ser trecho sem
uso. Pergunta ao site.

### RN-04 — Alterar exige ter consultado o gênero antes

Para alterar, o grupo, a subclasse, o gênero, o período, a refeição e o segmento informados têm
de ser exatamente os que a **sessão já guardou** da última consulta do gênero; qualquer diferença
é recusada com **\* Consulte o genero antes da atualizacao \***, com o cursor de volta ao campo
da operação. É isso que amarra a alteração à leitura que validou o gênero: só depois de consultá-lo
o ajuste pode ser lançado.

[?] A tela abre em alteração e o único caminho que grava a chave consultada na sessão é o da
consulta; como a tela não se coloca em consulta por conta própria, ou a chave tem de vir de fora,
ou a alteração fica inalcançável por este caminho. O material não diz quem coloca esta tela em
consulta. Pergunta ao site.

### RN-05 — A estimativa do gênero tem de estar aberta

Ao alterar, a tela procura a estimativa do gênero no período informado. Achando-a marcada como
**fechada**, recusa com **\* Cadastro fechado para este periodo \***, com o cursor de volta ao
campo COORD.REG.ESCOLA, e não deixa alterar. Não achar a estimativa não é recusa: nesse caso a
tela segue, e a falta aparece depois, na conferência do ajuste.

### RN-06 — O ajuste se identifica por grupo, subclasse, gênero, período, refeição e segmento

O que se informa para chegar a um ajuste é o **grupo** — a coordenação regional escolar, com
rótulo de negócio **COORD.REG.ESCOLA** —, a **subclasse**, o **gênero** e o **período** (dia, mês
e ano de início e dia, mês e ano limite) e, na linha, a **refeição** e o **segmento**. O **preço
2001** e a quantidade estimada são mostrados, mas não identificam: o preço é o do gênero no
período e a quantidade é o saldo. O tipo de órgão da sessão completa a identificação de tudo o
que a tela procura e grava. O ajuste acrescenta ainda à própria identificação a **data e a hora**
com que foi lançado: o mesmo gênero, no mesmo período, na mesma refeição e no mesmo segmento pode
ter mais de um ajuste, um por data e hora.

### RN-07 — Incluir um ajuste: quantidade e motivo, dentro do saldo

Com a ação da linha marcada como **inclusão**, o servidor informa a **quantidade a ser ajustada**
e o **motivo**. A quantidade é obrigatória — sem ela, a recusa é **\* Informe quantidade a ser
ajustada \***, com o cursor no campo da quantidade — e não pode passar do saldo estimado do
gênero naquela refeição e segmento: excedendo, a recusa é **\* Quantidade ajustada invalida \***,
com o cursor no mesmo campo. O motivo também é obrigatório: em branco, a recusa é **\* Informe
motivo, sem acentuacao \***, com o cursor no campo do motivo.

Passando pelas três conferências, a tela calcula o valor do ajuste multiplicando a quantidade
pelo preço, abate a quantidade e o valor do saldo do gênero na refeição e no segmento, soma-os à
quantidade e ao valor já ajustados e grava o ajuste com a **data e a hora do sistema** — se já
existir um ajuste gravado naquela mesma hora e data, a hora gravada é deslocada para não colidir
com ele.

### RN-08 — Alterar um ajuste: a linha já tem de estar preenchida

Com a ação da linha marcada como **alteração**, a linha tem de trazer a **data e a hora do
ajuste** que se quer alterar; sem ela — linha em branco —, a recusa é **\* Atualize motivo de
linha preenchida \***, com o cursor no campo do motivo. Com a linha preenchida, o servidor
informa a nova quantidade e o motivo: o motivo é obrigatório, com a mesma recusa **\* Informe
motivo, sem acentuacao \***; a quantidade pode ser zero (RN-09) e, quando informada, não pode
passar do saldo devolvido — isto é, do saldo do momento somado ao que aquele ajuste já havia
abatido, e excedendo vale a mesma recusa **\* Quantidade ajustada invalida \***.

Passando, a tela devolve ao saldo o que o ajuste antigo abatia, abate o novo, e regrava o ajuste
com a nova quantidade, o novo valor e o novo motivo, **mantendo a data e a hora originais**.

### RN-09 — Zerar a quantidade desfaz o ajuste

Na alteração, informar a quantidade **zero** não grava um ajuste de quantidade zero: a tela
devolve ao saldo o que aquele ajuste abatia e **apaga** o ajuste.

### RN-10 — Fechada a alteração, a estimativa do gênero é recalculada do detalhe

Terminada uma alteração, a tela reúne o detalhe da estimativa do gênero no período — todas as
refeições e todos os segmentos — e **regrava** o registro da estimativa com os totais
recalculados de quantidade e de valor, os já ajustados inclusive. Quando o saldo do gênero chega
a **zero**, o registro da estimativa é **apagado** em vez de regravado. O preço, a situação de
fechamento e a classe do gênero não são tocados.

### RN-11 — O grupo tem de estar cadastrado

Na consulta, o grupo informado é procurado no cadastro de grupos, dentro do tipo de órgão da
sessão. Não achando, a recusa é **\* Grupo nao cadastrado \***, com o cursor de volta ao campo
COORD.REG.ESCOLA.

### RN-12 — A subclasse e o gênero têm de estar cadastrados, e o gênero ativo

Na consulta, o par subclasse e gênero é procurado no cadastro de gêneros, tomando a data limite
do período como data de início da vigência. Não achando — ou achando o gênero **inativo** —, a
recusa é **\* Genero nao cadastrado \***, com o cursor no campo COD.SUB.CLASSE. Para a
**subclasse 99** a procura sai de outro cadastro de gêneros, pelo mesmo par, e o gênero aparece
marcado com um asterisco.

[?] O que a subclasse 99 identifica, por que ela usa outro cadastro de gêneros e o que a marca de
asterisco quer dizer em negócio não estão no material lido nem no manual. Pergunta ao site.

[?] A data limite do período entra na procura do gênero como data de início da vigência; o
material não diz se isso significa "o gênero vigente no período" nem o que acontece quando a
vigência do gênero não começa naquele dia. Pergunta ao site.

### RN-13 — O gênero tem de ter ajuste registrado

Na consulta, depois de o grupo e o gênero passarem, a tela procura um ajuste do gênero para a
refeição e o segmento informados. Não achando nenhum, a recusa é **\* Genero sem registros de
ajuste cadastrados \***, com o cursor no campo COD.SUB.CLASSE.

### RN-14 — Pedir a consulta entrega o gênero à C846T

Preenchido o **campo de consulta** com **S**, a tela zera o saldo e o valor que estavam em tela,
posiciona a leitura na estimativa do gênero e entrega à tela de consulta **C846T** o grupo, a
subclasse, o gênero e o período informados — **sem** a refeição e **sem** o segmento — e a abre
em consulta. A `C846T` é a tela que mostra a estimativa detalhada por refeição e segmento.

[?] O campo de consulta tem uma posição e nenhum rótulo no material lido, e o corpus não diz o
que a letra **S** significa em negócio, nem quem a preenche. Pergunta ao site.

### RN-15 — Consultar não grava nada

Em consulta, a passagem que grava é desviada de propósito: nada é incluído, alterado ou excluído
e nenhum registro de auditoria é gerado. As rotinas de gravar e de apagar que o sistema declara
para cada cadastro que a tela enxerga não são executadas nesse caminho.

### RN-16 — Toda gravação deixa rastro na auditoria

Cada gravação — o ajuste incluído, alterado ou apagado, o detalhe da estimativa, a estimativa
regravada ou apagada — vem acompanhada da montagem de um registro na **auditoria**, com a operação
(inclusão, alteração ou exclusão), o cadastro que a originou, o grupo, a data limite do período, a
matrícula, a estação, a sessão, a data e a hora e a imagem do registro gravado. São **sete**
pontos de auditoria no caminho vivo da tela: dois na inclusão, três na alteração — um deles só
quando a alteração apaga o ajuste — e dois no recálculo final, um para a estimativa regravada e
outro para a estimativa apagada.

[?] O registro de auditoria recebe sempre a mesma marca de manutenção — qualquer que seja a
operação —, e a operação propriamente dita vai em outro campo; o material não diz o que aquela
marca significa ali. Pergunta ao site.

### RN-17 — A digitação passa pela edição numérica, e o cursor volta ao campo recusado

**Treze campos** passam pela edição numérica antes de qualquer leitura: o grupo, o preço, a
subclasse, o gênero, as três partes do início do período, as três partes do limite, a refeição, o
segmento e a quantidade a ser ajustada. Campo em branco vale zero; o que não for número é
recusado, a passagem não segue e o cursor volta ao campo recusado. O motivo, a ação da linha, a
data do ajuste e o campo de consulta não são numéricos e não passam por essa edição.

[?] O que quem opera vê quando a digitação é recusada — se há mensagem, e qual — não está nos
fontes desta jornada: a rotina que faz a edição numérica é importada e não faz parte do acervo
lido. Pergunta ao site.

### RN-18 — Falha de banco interrompe a passagem e avisa

Todo acesso a dados testa o erro do banco; o erro de leitura e o de gravação viram avisos
despachados pela rotina de comunicação — a passagem para ali, sem completar o resto.

---

## Cenários BDD

```gherkin
Funcionalidade: Ajustar a quantidade estimada de um gênero da alimentação escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C847T

  Cenário: Incluir um ajuste de quantidade
    Dado que o grupo, a subclasse e o gênero estão cadastrados
    E existe estimativa aberta do gênero no período, com saldo de 500 unidades
    Quando marco a linha com a ação de inclusão
    E informo a quantidade a ser ajustada de 120 e o motivo "merenda suspensa"
    Então o saldo do gênero cai para 380 unidades
    E a quantidade e o valor já ajustados sobem pelo que foi ajustado
    E o ajuste fica gravado com a data, a hora, a quantidade e o motivo
    E o total da estimativa do gênero é recalculado

  Cenário: Alterar a quantidade de um ajuste já lançado
    Dado que existe um ajuste do gênero com data e hora registradas
    Quando marco a linha com a ação de alteração e informo outra quantidade e outro motivo
    Então o que o ajuste antigo abatia volta ao saldo
    E o novo valor é abatido do saldo
    E o ajuste passa a valer com a nova quantidade e o novo motivo, na mesma data e hora

  Cenário: Zerar a quantidade desfaz o ajuste
    Dado que existe um ajuste do gênero com data e hora registradas
    Quando marco a linha com a ação de alteração e informo a quantidade zero
    Então o ajuste é apagado
    E o saldo do gênero volta a ser o que era antes dele

  Cenário: O saldo do gênero chega a zero
    Dado que o ajuste a lançar consome todo o saldo estimado do gênero no período
    Quando confirmo a alteração
    Então o total da estimativa do gênero fica zerado
    E o registro da estimativa daquele gênero no período é apagado

  Cenário: Operação diferente de alteração e de consulta
    Dado que estou na tela C847T
    Quando informo uma operação que não é a alteração nem a consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nenhum cadastro é lido nesse caminho

  Cenário: Alterar sem ter consultado o gênero
    Dado que a sessão não guarda o gênero na combinação que informei
    Quando confirmo a alteração
    Então vejo a mensagem "* Consulte o genero antes da atualizacao *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: Estimativa fechada para o período
    Dado que a estimativa do gênero no período está fechada
    Quando confirmo a alteração
    Então vejo a mensagem "* Cadastro fechado para este periodo *"
    E o cursor volta ao campo COORD.REG.ESCOLA
    E nada é gravado

  Cenário: Grupo não cadastrado
    Dado que informo um grupo que não existe no cadastro de grupos do meu tipo de órgão
    Quando peço a consulta do gênero
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo COORD.REG.ESCOLA

  Cenário: Gênero não cadastrado ou inativo
    Dado que informo uma subclasse e um gênero que não estão no cadastro de gêneros, ou um gênero inativo
    Quando peço a consulta do gênero
    Então vejo a mensagem "* Genero nao cadastrado *"
    E o cursor volta ao campo COD.SUB.CLASSE
    E nada é preenchido

  Cenário: Gênero da subclasse 99
    Dado que informo a subclasse 99 e um gênero do outro cadastro de gêneros
    Quando peço a consulta do gênero
    Então o gênero aparece marcado com um asterisco

  Cenário: Gênero sem ajuste registrado
    Dado que o gênero está cadastrado mas não tem nenhum ajuste na refeição e no segmento informados
    Quando peço a consulta do gênero
    Então vejo a mensagem "* Genero sem registros de ajuste cadastrados *"
    E o cursor volta ao campo COD.SUB.CLASSE

  Cenário: Incluir sem informar a quantidade
    Dado que marco a linha com a ação de inclusão
    Quando deixo a quantidade a ser ajustada em branco
    Então vejo a mensagem "* Informe quantidade a ser ajustada *"
    E o cursor volta ao campo da quantidade

  Cenário: Quantidade acima do saldo do gênero
    Dado que marco a linha com a ação de inclusão
    Quando informo uma quantidade maior que o saldo estimado do gênero
    Então vejo a mensagem "* Quantidade ajustada invalida *"
    E o cursor volta ao campo da quantidade
    E nada é gravado

  Cenário: Motivo em branco
    Dado que marco a linha com a ação de inclusão e informo a quantidade
    Quando deixo o motivo em branco
    Então vejo a mensagem "* Informe motivo, sem acentuacao *"
    E o cursor volta ao campo do motivo
    E nada é gravado

  Cenário: Alterar uma linha em branco
    Dado que marco a linha com a ação de alteração
    Quando a linha não traz a data e a hora de um ajuste
    Então vejo a mensagem "* Atualize motivo de linha preenchida *"
    E o cursor volta ao campo do motivo
    E nada é gravado

  Cenário: Pedir a consulta encaminha para a C846T
    Dado que informei o grupo, a subclasse, o gênero e o período
    Quando preencho o campo de consulta com S
    Então a tela C847T entrega o grupo, a subclasse, o gênero e o período à tela C846T
    E a C846T abre em consulta
    E a refeição e o segmento não são levados

  Cenário: Consultar não grava nada
    Dado que estou na tela C847T em consulta
    Quando confirmo a passagem
    Então nenhum ajuste, nenhum detalhe de estimativa e nenhuma estimativa são gravados ou apagados
    E nenhum registro de auditoria é gerado

  Cenário: Digitação não numérica
    Dado que digito no grupo, no preço, na subclasse, no gênero, em uma das partes das datas, na refeição, no segmento ou na quantidade algo que não é número
    Quando confirmo a passagem
    Então a passagem não segue antes de ler qualquer cadastro
    E o cursor volta ao campo recusado

  Cenário: Falha de banco durante a leitura
    Dado que o banco falha na leitura de um dos cadastros da tela
    Quando confirmo a passagem
    Então a passagem para e um aviso é despachado pela rotina de comunicação
```
