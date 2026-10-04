# US — N028T — Ajuste do preço dos gêneros da nota fiscal

## Estória

Como **servidor da Coordenação Regional Escolar (CRE)**, quero **ajustar o preço de um
gênero de uma nota fiscal já lançada e conferir o que a nota passou a valer depois
disso**, para que **o valor da nota acompanhe o preço corrigido sem que a nota precise
ser apagada e lançada de novo**.

A nota fiscal é lançada em outra tela: é lá que o fornecedor, os gêneros, as quantidades
e os preços entram. Quando o preço de um gênero sai errado, não é a nota inteira que se
refaz — é esta tela que corrige o preço unitário de um gênero, e é ela que refaz, a
partir daí, o total do item, o total da nota e a retenção do imposto de renda que a nota
carrega. **Sem esse ajuste, o total da nota e a retenção ficam presos ao preço errado** —
e é esse valor que a secretaria paga e contabiliza. A correção é pequena de propósito: o
preço ajustado não pode cair abaixo do preço que a nota registra, nem passar dele por
mais de cinco centavos.

## Contexto

Jornada S000M → N000M → N050M → N028T (4 passos).
Ator: servidor de CRE — abre a nota pelo fornecedor, pelo número e pelo ano, confere os
gêneros e corrige o preço do gênero que estiver marcado na linha.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Os dois passos anteriores desta jornada são menus, e nada chega junto com a abertura
além do que a entrada deixou na sessão — o tipo de órgão e a coordenação regional do
vínculo. Não há encadeamento de tela a tela na chegada: é por isso que a tela abre no
modo de consulta, e é o próprio servidor que muda o modo depois de ver a nota (RN-03 e
RN-05). Na saída, porém, a tela **encadeia**: ao desfazer um ajuste ela entrega a nota
aberta à tela de lançamento da nota (`N024T`), em modo de alteração (RN-15).

As regras abaixo são só as da **tela desta jornada**. As regras que se revelaram ser da
entrada estão no anexo de evidências.

---

## Regras de negócio

### RN-01 — Esta tela corrige o preço dos gêneros de uma nota já lançada, e é isso que ela altera

Esta tela não lança nota, não inclui gênero e não exclui gênero avulso: ela **abre uma
nota fiscal que já existe**, mostra os seus gêneros e ajusta o **preço unitário** do
gênero marcado. O ajuste não é livre — parte do preço que a nota registra e só sobe até
cinco centavos.

Por baixo do ajuste, ela refaz o **total do item**, o **total da nota** e a **retenção do
imposto de renda** da nota e dos seus gêneros. É a única operação desta tela que muda
valor.

Ela enxerga onze cadastros — as telas do sistema, os gêneros da nota, o cadastro de
gêneros, a nota fiscal, os modelos de nota, os fornecedores, os operadores, os órgãos, os
pedidos, os contratos e a trilha de auditoria — e, para cada um deles, o gerador deixa
prontas uma operação de gravar, uma de apagar e uma de travar. Dessas trinta e três
operações prontas, **só três são executadas**: a gravação dos gêneros da nota, a gravação
da nota e a exclusão da nota (esta última só no caso da RN-19). Toda gravação executada é
precedida de uma linha na trilha de auditoria, com a tela, a operação, a matrícula, a
coordenação regional, a estação, a data e a hora, e com o valor de antes e o de depois —
com as exceções apontadas na RN-18.

Os números de capacidade são de dimensionamento, não volume cadastrado: as notas fiscais
comportam 150.000 registros; os gêneros da nota, 1.000.000; os modelos de nota, 100; o
cadastro de gêneros, 150.000; os fornecedores, 10.000; os operadores, 100; os órgãos,
12.000; os pedidos, 10.000.000; os contratos, 1.000; as telas do sistema, 2.000; e a
trilha de auditoria, 60.000.000.

### RN-02 — O órgão é o da sessão, e a nota se identifica por fornecedor, número e ano

A nota é procurada no **tipo de órgão que a sessão carrega**, escolhido no vínculo da
matrícula na entrada; **não há campo na tela para informar outro órgão**. A nota fiscal se
identifica por três dados: o **código do fornecedor**, o **número da nota** e o **ano da
nota**. Cada gênero da nota é identificado por esses três mais a **subclasse** e o
**gênero**.

A tela não recalcula a sessão: usa a matrícula, o código de acesso, o privilégio, o tipo
de órgão e a coordenação regional que a entrada deixou.

### RN-03 — A tela abre em consulta, e só aceita ALT e CON

Ao se apresentar, sem nada vindo de outra tela, a tela adota a **consulta** como modo: é
esse o código que aparece no campo de operação. Qualquer modo que não seja **alteração
(ALT)** ou **consulta (CON)** é recusado com **\* Opcao nao disponivel. Use ALT ou CON \***;
o cursor volta ao campo da operação e **nada é lido e nada é gravado**.

### RN-04 — Chegando com o código de tela anterior preenchido, a tela não confere nada

Toda a conferência da operação — os campos obrigatórios, a existência da nota, o acesso ao
grupo regional e os limites de preço — fica **depois** de uma guarda que olha o **código
da tela anterior**. Se esse código vier preenchido, a conferência é **abandonada ali** e a
tela não segue para nenhuma regra de negócio. O código é levado à conferência de rota e de
permissão.

[?] O que preenche o código de tela anterior não está no corpus: nesta jornada a tela é
aberta por menu, e o menu não o preenche. Se é o encadeamento de outra tela que o
preenche, o corpus não diz qual — e é isso que decide se essa guarda é caminho normal ou
excepcional.

### RN-05 — Para alterar, é preciso ter consultado antes a mesma nota

Em alteração, a tela compara a nota que está na tela com a última nota que ela abriu:
**fornecedor, número e ano têm de ser os mesmos**. Trocando a nota e confirmando direto em
alteração, a recusa é **\* Consulte antes de atualizar \***, com o cursor de volta ao campo
da operação, e nada é gravado. Em consulta, trocar a nota apenas dispara nova leitura.

### RN-06 — A consulta exige o número, o ano e o fornecedor

Em consulta, quando a nota pedida é diferente da que estava aberta, os três dados passam a
ser obrigatórios, nesta ordem:

| o que falta | o que o servidor vê |
| --- | --- |
| o número da nota | **\* Informe o numero da nota fiscal \*** |
| o ano da nota | **\* Informe o ano de entrega da nota \*** |
| o código do fornecedor | **\* Informe o codigo do fornecedor \*** |

Em qualquer dos três casos o cursor volta ao campo do número da nota.

[?] A recusa do ano fala em "ano de entrega da nota", mas o campo que ela cobra é o ano
que a tela rotula como "ANO EMISSAO N.F."; o campo rotulado "ANO DA ENTREGA" é outro, e
fica ao lado. A mensagem e o campo conferido não coincidem — pergunta ao site qual dos
dois a mensagem queria dizer.

### RN-07 — A nota tem de estar cadastrada

Não sendo encontrada nota do órgão da sessão com aquele fornecedor, aquele número e aquele
ano, a recusa é **\* Nota fiscal nao cadastrada \***, com o cursor de volta ao campo do
número da nota, e nada é gravado.

### RN-08 — A nota tem de ser do meu grupo regional

A nota carrega a sua coordenação regional escolar. Se o servidor tem coordenação no
vínculo e ela **difere** da coordenação da nota, a recusa é
**\* Usuario sem acesso ao grupo desta nota \***, com o cursor de volta ao número da nota,
e a nota não é aberta. O servidor **sem coordenação no vínculo** não passa por essa
conferência: ele alcança a nota de qualquer grupo.

### RN-09 — A nota tem de ter gêneros

Se a nota existe mas não tem nenhum gênero cadastrado, a tela avisa
**\* Nota fiscal sem generos cadastrados \*** e não mostra a nota. O aviso é dado uma única
vez, já na primeira linha da lista de gêneros.

### RN-10 — O que a tela mostra

A tela mostra o cabeçalho da nota — a descrição do tipo de órgão e a data do sistema, o
número da nota, o dia e o mês da emissão (que vêm da própria nota; o ano é o que o
servidor informou), o ano, o mês e o dia da emissão, a coordenação regional escolar, o
número do pedido com o seu ano de entrega, o tipo de contrato, o código do fornecedor com
a razão social, o código do operador com o nome, o órgão filho com a sua descrição, a
descrição do modelo da nota, o número do processo, a chave da nota, o total da nota e a
retenção do imposto de renda.

Abaixo do cabeçalho vêm **até oito linhas de gênero** da nota. Cada linha traz a
subclasse, o gênero, a **descrição resumida do gênero vigente na data da nota**, a
quantidade, o preço unitário, o valor da linha, o total do item e a marca de ajuste da
linha. A descrição do gênero não vem do cadastro do gênero pelo código apenas: ela é
procurada com a data da nota, de modo que a linha mostra a descrição que valia naquela
data.

### RN-11 — A consulta não altera valor

A consulta não muda preço, quantidade, total nem retenção: ela só mostra. A **única
gravação** que a consulta faz é registrar, em cada gênero da nota **que ainda não tem**,
o **preço da nota** — o preço unitário que aquele gênero tem hoje, guardado como a
referência da nota. É essa referência que a alteração usa depois para limitar o ajuste
(RN-13); o gênero que já tem a referência não é tocado.

[?] O cadastro de gêneros tem 22 campos declarados no dicionário de dados, mas o programa
trabalha com 23: o campo onde o preço da nota fica guardado não consta do dicionário.
Entre os onze cadastros desta tela é o único em que o dicionário e o programa não batem.
Se o dicionário está atrás do programa, pergunta ao site.

### RN-12 — O ajuste é de um gênero marcado da nota

O ajuste só acontece quando a linha traz a **subclasse** e o **gênero** de um gênero
daquela nota e a **marca de ajuste** está na linha. Sem a marca, nada é ajustado.

[?] A conferência do preço exige subclasse **e** gênero preenchidos, mas a gravação do
ajuste aceita que um dos dois esteja zerado. Nessa combinação o ajuste é tentado **sem** as
conferências de preço da RN-13 — e, como a leitura do gênero é feita com esse zero na
chave, ele só encontra um gênero cujo código seja zero. Se é intencional, pergunta ao
site.

### RN-13 — O preço ajustado fica entre o preço da nota e cinco centavos acima dele

O preço informado passa por três conferências, nesta ordem:

| o que acontece | o que o servidor vê |
| --- | --- |
| o preço está em branco (zero) | **\* Informe o valor \*** |
| o preço é **menor** que o preço da nota | **\* Preco ajuste < preco nota. Use N024T \*** |
| o preço passa do preço da nota por **mais de cinco centavos** | **\* Preco ajuste > que 0,05 em relacao Preco nota \*** |

A recusa da diferença manda usar a tela de lançamento da nota (`N024T`): quando o preço
novo é muito diferente do preço da nota, o caminho não é o ajuste, é o lançamento. Em
todos os casos o cursor volta ao preço unitário da linha, e nada é gravado.

[?] A conferência do valor está escrita duas vezes, idêntica e em sequência; a segunda
nunca é alcançada, porque a primeira só deixa chegar lá com o valor preenchido. Se a
segunda deveria conferir outro campo — o valor da linha ou o total do item —, o corpus não
diz.

### RN-14 — Gravar o ajuste grava o preço unitário e o total do item, e isso fica registrado

Passando pelas conferências, o gênero da nota recebe o preço informado como **preço
unitário**, e o **total do item** passa a ser a quantidade vezes esse preço. Antes da
gravação, a tela deixa a linha de auditoria do gênero, com o valor de antes e o de depois.

[?] A gravação regrava o preço unitário e o total do item, mas **não** a quantidade — e o
total é calculado com a quantidade que está na tela, que pode ser digitada. Corrigindo a
quantidade antes de confirmar, o total gravado deixa de corresponder à quantidade guardada
no gênero. Se a intenção era regravar a quantidade também, o corpus não diz.

### RN-15 — O desfazer devolve os gêneros ao preço da nota e entrega a nota à tela de lançamento

Quando a linha traz a **marca de desfazer**, a tela percorre os gêneros da nota e, em cada
um, devolve o **preço unitário** ao **preço da nota**, refaz o total do item com a
quantidade guardada e **limpa o preço da nota**. Cada devolução deixa a sua linha de
auditoria.

Encerrado o percurso, a tela **não volta ao menu**: entrega a transação à tela de
lançamento da nota (`N024T`), com a nota que estava aberta — fornecedor, número, ano,
coordenação regional e pedido —, em **modo de alteração**, e marcando a origem como a tela
do cabeçalho da nota (`N014T`). Do outro lado, a tela de lançamento só segue por esse
caminho se o modo recebido for consulta ou alteração; fora dele, devolve o controle ao menu
da nota fiscal (`N050M`).

[?] A tela lê o pedido da nota para saber se ele é acumulado e guarda essa marca, mas não
a mostra em campo nenhum; ela só segue na área de trabalho para a tela seguinte. E o campo
que manda desfazer não tem rótulo no fonte nem passa pela conferência numérica, de modo que
o texto que o servidor lê nesse campo não está no corpus.

### RN-16 — Ao gravar a alteração, o total da nota é refeito pela soma dos gêneros

Antes de encerrar uma alteração, a tela soma os totais dos gêneros da nota e compara com o
total gravado: soma **diferente** → a nota é regravada com a soma dos gêneros; soma
**igual** → a nota não é tocada.

### RN-17 — A retenção do imposto de renda é recalculada pela alíquota do tipo de contrato

A retenção da nota passa a ser o **total da nota multiplicado pela alíquota do tipo de
contrato**, guardada no cadastro de contratos por órgão e tipo de contrato e com duas
casas decimais. Alíquota zerada — ou contrato não cadastrado — deixa a retenção zerada.

A conta só vale para **notas emitidas depois de 18/10/2021**: a nota emitida até essa data
fica com a retenção zerada na regravação.

[?] A tela regrava a retenção das notas antigas como **zero**, em vez de deixar o valor que
já estava gravado. Se a intenção era "não recalcular", o fonte faz coisa diferente —
pergunta ao site.

### RN-18 — A retenção item a item é redistribuída, e a sobra do arredondamento vai para o item de maior retenção

Quando a retenção da nota muda, cada gênero da nota recebe a sua parte: o **total do item
multiplicado pela alíquota**. Se a soma das partes ficar diferente da retenção gravada na
nota, a diferença é lançada no gênero de **maior retenção**, para que a soma das partes
feche com a nota. A tela só faz esse acerto quando a alíquota é diferente de zero.

[?] As duas gravações deste acerto — a de cada gênero e a da diferença no maior — são as
**únicas gravações desta tela que não deixam linha na trilha de auditoria**; as outras
cinco deixam. Se o acerto deveria ser auditado como as demais, pergunta ao site.

### RN-19 — A nota cuja soma dos gêneros fica zero é apagada

Se a soma dos totais dos gêneros da nota der **zero**, a alteração não regrava a nota: ela
**apaga** a nota fiscal, com a sua linha de auditoria. É a única exclusão que esta tela
executa.

### RN-20 — Os campos passam pela conferência numérica antes de qualquer regra de negócio

**Vinte campos** da tela passam pela conferência numérica, com o rótulo que a tela mostra:
o número da nota; as três partes da emissão da nota; as três partes da emissão; a
coordenação regional escolar; o número do pedido; o ano da entrega; o tipo de contrato; o
código do fornecedor; o órgão filho; o código do operador; a subclasse; o gênero; a
quantidade do gênero; o preço unitário do item; o valor da linha; e o total do item.

O que não for número é recusado ali, **antes de qualquer consulta de cadastro** — a
conferência numérica roda antes das conferências de negócio de todas as regras acima.

[?] Dos vinte campos, só quatro têm o cursor devolvido quando a recusa é por não ser
número: o número da nota, o ano da nota, o código do fornecedor e o preço unitário do
item. Nos demais a mensagem de recusa não move o cursor.

---

## Cenários BDD

```gherkin
Funcionalidade: Ajuste do preço dos gêneros de uma nota fiscal já lançada

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N028T

  Cenário: RN-03 — a tela abre em consulta
    Dado que cheguei à tela pelo menu, sem nada vindo de outra tela
    Quando a tela se apresenta
    Então o campo da operação mostra a consulta
    E nenhum valor é lido nem gravado

  Cenário: RN-03 — operação que não é ALT nem CON
    Dado que a nota está aberta
    Quando informo no campo da operação um código de inclusão ou de exclusão
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido e nada é gravado

  Cenário: RN-02 — o órgão da nota é o da minha sessão
    Dado que estou na tela com o vínculo da minha matrícula
    Quando procuro a nota
    Então ela é procurada no tipo de órgão da minha sessão
    E não há campo na tela para eu informar outro órgão

  Cenário: RN-06 — falta o número da nota
    Quando deixo o número da nota em branco e confirmo a consulta
    Então vejo "* Informe o numero da nota fiscal *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: RN-06 — falta o ano da nota
    Dado que informei o número da nota
    Quando deixo o ano em branco e confirmo a consulta
    Então vejo "* Informe o ano de entrega da nota *"
    E o cursor volta ao campo do número da nota

  Cenário: RN-06 — falta o fornecedor
    Dado que informei o número e o ano da nota
    Quando deixo o código do fornecedor em branco e confirmo a consulta
    Então vejo "* Informe o codigo do fornecedor *"
    E o cursor volta ao campo do número da nota

  Cenário: RN-20 — campo não numérico
    Quando preencho o número da nota, uma data, o fornecedor ou um valor com letra
    Então a tela recusa o campo antes de qualquer consulta de cadastro
    E nada é gravado

  Cenário: RN-07 — nota não cadastrada
    Dado que informei fornecedor, número e ano que não existem no cadastro
    Quando confirmo a consulta
    Então vejo "* Nota fiscal nao cadastrada *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: RN-08 — nota de outro grupo regional
    Dado que tenho coordenação regional no meu vínculo
    E a nota que procuro é de outra coordenação
    Quando confirmo a consulta
    Então vejo "* Usuario sem acesso ao grupo desta nota *"
    E o cursor volta ao campo do número da nota
    E a nota não é aberta

  Cenário: RN-08 — servidor sem coordenação alcança qualquer grupo
    Dado que o meu vínculo não traz coordenação regional
    Quando procuro uma nota de qualquer grupo
    Então a nota é aberta normalmente

  Cenário: RN-09 — nota sem gêneros
    Dado que a nota existe e não tem nenhum gênero cadastrado
    Quando confirmo a consulta
    Então vejo "* Nota fiscal sem generos cadastrados *"
    E a nota não é mostrada

  Cenário: RN-10 e RN-11 — a consulta mostra a nota e não altera valor
    Dado que a nota existe, é do meu grupo e tem gêneros
    Quando confirmo a consulta
    Então vejo a nota com o fornecedor, o operador, o órgão filho, o modelo, o pedido,
      o processo, o total e a retenção
    E vejo até oito linhas de gênero, cada uma com a descrição vigente na data da nota,
      a quantidade, o preço unitário, o valor e o total do item
    E nenhum preço, quantidade, total ou retenção da nota é alterado

  Cenário: RN-11 — a consulta registra o preço da nota no gênero que ainda não tem
    Dado que os gêneros da nota ainda não têm o preço da nota registrado
    Quando confirmo a consulta
    Então cada gênero recebe, como preço da nota, o preço unitário que ele tem hoje
    E o gênero que já tinha o preço da nota não é tocado

  Cenário: RN-05 — alterar sem ter consultado antes
    Dado que a nota em tela é diferente da última que abri
    Quando informo o modo de alteração e confirmo
    Então vejo "* Consulte antes de atualizar *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: RN-12 — ajuste sem a marca de ajuste na linha
    Dado que abri a nota em consulta
    E informei a subclasse e o gênero de um dos seus gêneros
    Quando confirmo em alteração sem marcar a linha
    Então nenhum preço é ajustado

  Cenário: RN-13 — ajuste sem valor
    Dado que marquei a linha de um gênero da nota
    Quando deixo o preço em branco e confirmo
    Então vejo "* Informe o valor *"
    E o cursor volta ao preço unitário da linha

  Cenário: RN-13 — preço abaixo do preço da nota
    Dado que marquei a linha de um gênero da nota
    Quando informo um preço menor que o preço da nota
    Então vejo "* Preco ajuste < preco nota. Use N024T *"
    E o cursor volta ao preço unitário da linha
    E nada é gravado

  Cenário: RN-13 — preço mais de cinco centavos acima do preço da nota
    Dado que marquei a linha de um gênero da nota
    Quando informo um preço que passa do preço da nota por mais de cinco centavos
    Então vejo "* Preco ajuste > que 0,05 em relacao Preco nota *"
    E o cursor volta ao preço unitário da linha
    E nada é gravado

  Cenário: RN-14 — o ajuste é gravado
    Dado que marquei a linha de um gênero da nota
    E informei um preço entre o preço da nota e cinco centavos acima dele
    Quando confirmo a alteração
    Então o gênero da nota fica com esse preço unitário
    E o total do item passa a ser a quantidade vezes esse preço
    E a gravação deixa a sua linha na trilha de auditoria

  Cenário: RN-16 e RN-17 — o total da nota e a retenção depois do ajuste
    Dado que ajustei o preço de um gênero da nota
    Quando a alteração é gravada
    Então o total da nota é refeito pela soma dos totais dos seus gêneros
    E a retenção da nota passa a ser o total da nota vezes a alíquota do tipo de contrato
    E a nota é regravada com o total e a retenção novos

  Cenário: RN-16 — total igual ao gravado
    Dado que a soma dos gêneros da nota é igual ao total que a nota já tem
    Quando confirmo a alteração
    Então a nota não é regravada

  Cenário: RN-17 — nota antiga tem a retenção zerada
    Dado que a nota foi emitida até 18/10/2021
    Quando confirmo uma alteração que muda o total da nota
    Então a retenção da nota é regravada como zero

  Cenário: RN-18 — o acerto da retenção item a item
    Dado que a retenção da nota mudou e a alíquota do contrato não é zero
    Quando a alteração é gravada
    Então cada gênero da nota recebe o seu total multiplicado pela alíquota
    E, se a soma das partes não fechar com a nota, a diferença vai para o gênero de maior
      retenção
    E as duas gravações desse acerto não deixam linha na trilha de auditoria

  Cenário: RN-19 — a nota que ficou sem valor é apagada
    Dado que a soma dos totais dos gêneros da nota é zero
    Quando confirmo a alteração
    Então a nota fiscal é apagada
    E a exclusão deixa a sua linha na trilha de auditoria

  Cenário: RN-15 — o desfazer devolve os gêneros ao preço da nota
    Dado que a nota está aberta em alteração e tem gêneros ajustados
    Quando informo a marca de desfazer e confirmo
    Então cada gênero volta a ter como preço unitário o preço da nota
    E o total de cada item é refeito com a quantidade guardada
    E o preço da nota de cada gênero é limpo

  Cenário: RN-15 — o desfazer entrega a transação à N024T
    Dado que percorri todos os gêneros da nota com a marca de desfazer
    Quando o percurso termina
    Então a tela de lançamento da nota N024T é aberta
    E ela recebe a nota que estava aberta, em modo de alteração
    E a origem é marcada como a tela do cabeçalho da nota

  Cenário: RN-04 — a tela aberta com o código de tela anterior preenchido
    Dado que a transação chega a esta tela com o código de tela anterior preenchido
    Quando a conferência da operação começaria
    Então nenhuma conferência de negócio é feita
    E nada é gravado por essa passagem

  Cenário: RN-01 — nenhum outro cadastro é alterado pela tela
    Dado que ajustei o preço, refiz o total e recalculei a retenção
    Quando a alteração termina
    Então só os gêneros da nota, a nota e a trilha de auditoria foram gravados
    E os cadastros de fornecedores, operadores, órgãos, pedidos, contratos, modelos de
      nota e gêneros não são alterados
```
