# US — C810C — Consultar os cardápios do órgão pela validade e pedir a relação

## Estória

Como **servidor de CRE**, quero **informar o dia, o mês e o ano limite de uma validade
e ver quais cardápios do meu órgão valem nessa data, pedindo a relação deles**, para
que **eu confira o que está valendo no período e leve a relação dos cardápios daquela
validade para quem precisa**.

O cardápio reúne os gêneros da alimentação escolar, e cada um tem um período de
validade: uma data de início e uma data limite. Vários cardápios podem terminar na
mesma data, e é a data limite que diz o que valia naquele momento. Esta tela é a porta
da relação dos cardápios de um órgão numa data limite: ela só lê o cadastro dos
cardápios — quem cadastra e altera é outra tela —, mas é dela que sai o pedido da
relação, e é por isso que ela também confere, recusa e registra.

## Contexto

Jornada S000M → C000M → C800M → C811M → C810C.

Ator: servidor de CRE — consulta os cardápios do seu órgão pela data limite e pede a
relação deles.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O C000M, o C800M e o C811M são menus
e não gravam nada: eles apenas encaminham. O contexto que a C810C usa — matrícula,
órgão, código de acesso, privilégio, CRE, a estação e a data do sistema — é o que a
entrada deixou na sessão.

---

## Regras de negócio

### RN-01 — A única operação da tela é a consulta, e é ela que pede a relação

A tela abre em modo de consulta e repõe esse modo a cada abertura, de modo que a
operação mostrada volta a ser sempre a consulta. Se chegar outra operação, o sistema
recusa com **\* Operacao nao disponivel. Use CON \*** e devolve o cursor ao campo da
operação. A recusa vem depois das conferências de acesso e de rota e antes de ler
qualquer cardápio. É dentro da consulta — e não de uma operação de manutenção — que o
pedido da relação é registrado: na prática, esta tela só tem a consulta e o pedido.

[?] A recusa só existe se o formulário oferecer ao servidor o campo de operação. Como
a abertura repõe a consulta sozinha, essa recusa só pode ser alcançada numa mensagem
seguinte do servidor; se o formulário não tem esse campo, a recusa é trecho sem uso.
Pergunta ao site.

[?] A mensagem manda usar "CON", mas a tela aceita apenas o código interno de consulta
que o sistema reconhece; nenhum valor "CON" existe no acervo lido. Ou o formulário
traduz o que o servidor digita para esse código, ou quem seguir a mensagem é recusado.
Pergunta ao site.

### RN-02 — O assunto é o cardápio do órgão do servidor

A tela trata do cadastro dos cardápios. Cada cardápio pertence a um tipo de órgão, tem
código, descrição, uma data de início e uma data limite de validade; o conjunto pelo
qual a tela lê está ordenado pelo tipo de órgão, pela data limite e pelo código do
cardápio, e não admite dois cardápios com a mesma data limite e o mesmo código no
mesmo tipo de órgão. O tipo de órgão é o da sessão do servidor: ele não é digitado
nesta tela, e é ele que limita tudo o que a tela vê. A descrição tem até 60 caracteres
no cadastro, e a tela mostra 50.

[?] O cadastro tem 17 campos e esta tela usa 9. Ficam de fora seis marcas de um
caractere, uma marca de estimativa e um segundo código de cardápio; o que elas
significam no negócio não vem do material lido. Pergunta ao site.

### RN-03 — A lista mostra até 13 cardápios, com o início e o limite da validade, o código e a descrição

A lista é uma página de 13 linhas de 80 posições; cada linha traz a data de início, a
data limite, o código do cardápio e a descrição, com as duas datas montadas no formato
dia/mês/ano. Fora da lista, a tela mostra a descrição do tipo de órgão e a data do
sistema.

### RN-04 — A lista parte da posição que a tela guarda na sessão

A posição de leitura — o ano limite, o mês limite, o dia limite e o código do cardápio
— fica na área de trabalho da sessão, e é dela que a abertura tira o ponto de partida
da lista. A cada linha achada, os valores do cardápio lido passam a ser a posição da
linha seguinte: é assim que a página percorre o cadastro do tipo de órgão, uma linha
por vez, na ordem do ano limite, depois o mês, depois o dia e depois o código do
cardápio. Ao encher a última linha da página, os valores do 13º cardápio listado
voltam para os quatro campos do cabeçalho; quando o cadastro do tipo de órgão termina
antes da última linha, esses quatro campos saem zerados.

[?] Na primeira abertura da tela na sessão, a área de trabalho não traz posição
guardada e o fonte desta tela não repõe nenhuma — ao contrário das telas irmãs do
mesmo módulo, que partem da data do sistema. Se a lista abre no começo do cadastro do
tipo de órgão, ou se ela sai com o aviso de cardápio não cadastrado, não se conclui do
acervo: depende do que a área de trabalho da sessão traz. Pergunta ao site.

### RN-05 — O dia, o mês, o ano limite e o cardápio informados são números, e o cursor volta ao campo recusado

Os quatro campos informados são editados como número antes de qualquer leitura — em
branco vale zero — e, quando a edição acusa erro, o cursor volta ao campo recusado: o
dia limite, depois o mês limite, depois o ano limite e depois o cardápio.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não
está nos fontes desta jornada: a rotina que faz a edição numérica não faz parte do
acervo lido. Pergunta ao site.

### RN-06 — O acesso é conferido antes de a tela mostrar a lista, e de novo na mensagem do servidor

Na abertura a tela confere a segurança do perfil antes de ler qualquer cardápio; na
mensagem do servidor ela monta o contexto da sessão, confere a rota e, depois, a
permissão da operação. Tela fora do quadro de telas liberadas sai
**\* Tela nao disponivel \***; tela não cadastrada sai **\* Tela nao cadastrada \***;
par de código de acesso e tela não autorizado sai
**\* Acesso negado para esta matricula \***; operação não permitida ao código de acesso
sai **\* Acesso negado para esta operacao \***. A estação gravada no cadastro do
funcionário tem de bater com a da sessão.

[?] A permissão conferida por operação só conhece inclusão, alteração e exclusão: não
há uma permissão de consulta. Como esta tela opera sempre em consulta, quem tem a tela
liberada consulta sem nenhuma permissão de operação. Se a intenção era exigir uma
permissão de consulta por tela, o caminho não a exige. Pergunta ao site.

### RN-07 — Sem cardápio a partir da posição, a tela avisa

Não achando nenhum cardápio do tipo de órgão a partir da posição de leitura, a tela
avisa **\* Cardapio nao cadastrado \***, zera a posição que traria e não monta a
lista. O aviso sai só na montagem da primeira linha da página e não devolve o cursor a
um campo.

[?] O aviso é decidido uma única vez, na primeira linha, e a conferência que o decide
olha só o tipo de órgão — não distingue "não há cardápio nenhum no tipo de órgão" de
"não há cardápio a partir da posição". Se a lista pode começar vazia em outro caso, o
acervo não mostra. Pergunta ao site.

### RN-08 — Informar outra posição reposiciona a lista; não achando, os quatro campos voltam a zero

Se os quatro valores informados forem diferentes dos que a tela já tinha, ela larga a
posição anterior e procura de novo pelo tipo de órgão e pelos quatro valores
informados. Não achando, os quatro campos voltam a zero, sem mensagem; achando, os
valores informados passam a ser a posição da lista.

[?] A conferência que autoriza o pedido da relação procura o cardápio na data
informada levando o código do cardápio zerado e confere, além do tipo de órgão, só o
dia, o mês e o ano; a procura do reposicionamento leva o código informado e confere só
o tipo de órgão. A semântica dos sinalizadores que dizem de que partes da chave a
leitura usa não está no acervo lido, e é ela que decide o desfecho: se a leitura usar o
código do cardápio, existindo cardápio na data informada e não com o código informado,
o pedido passa por essa conferência, os quatro campos são zerados em silêncio e a
requisição é registrada com a data zerada, porque nada entre o zeramento e a gravação
reconfere a posição. Ou a conferência do pedido devia exigir a posição inteira, ou o
zeramento devia interromper o pedido; o acervo não diz qual dos dois. Pergunta ao
site.

### RN-09 — Com o código de impressão preenchido, a tela registra o pedido da relação e o encaminha

Preenchido o código de impressão, a tela registra uma requisição no cadastro de
requisições de relatório para o relatório C81007 — a relação dos cardápios —, com o
tipo de órgão do servidor, a matrícula, a estação, o código do relatório e a data do
pedido, numerada a partir da última requisição registrada mais um. Registrada a
requisição, o pedido é encaminhado para processamento com a data limite informada, o
código de impressão e uma via. Sem o código de impressão, nada é registrado.

[?] O código de impressão vai no encaminhamento, mas não fica na requisição, e o
programa do relatório só declara como parâmetros o tipo de órgão e a data limite. Quem
consome o código de impressão — formulário, destino ou fila de impressão — não está no
lote. Pergunta ao site.

[?] O encaminhamento depende de o produto estar identificado como LINC e usa um
identificador de trabalho que o acervo não documenta. O que acontece com o pedido
quando esse encaminhamento não ocorre — a requisição fica registrada e não processada?
— não está no lote. Pergunta ao site.

### RN-10 — O pedido é recusado enquanto houver requisição do mesmo relatório para o tipo de órgão

Havendo qualquer requisição do relatório C81007 para o tipo de órgão do servidor, o
pedido é recusado com **\* Relatorio ja esta em processamento. Aguarde. \***, com o
cursor no dia limite. A requisição sai do cadastro quando o relatório é processado: o
próprio relatório a apaga no fim.

[?] A recusa não olha a situação da requisição: qualquer registro do mesmo relatório e
tipo de órgão barra o pedido. Se o processamento falhar e a requisição sobrar, o tipo
de órgão fica sem poder pedir de novo. O acervo não mostra o que limpa uma requisição
que falhou. Pergunta ao site.

### RN-11 — O pedido exige e-mail cadastrado para o servidor

O pedido lê o cadastro do funcionário pela matrícula da sessão e exige e-mail
preenchido; sem e-mail, recusa com **\* Usuario sem e-mail cadastrado \*** e não
registra nada.

[?] O e-mail é exigido e segue no encaminhamento, mas o programa do relatório não o
declara entre os seus parâmetros, e a requisição registra o campo de e-mail em branco.
Se a relação é impressa na estação, enviada por e-mail ou as duas coisas, o lote lido
não diz. Pergunta ao site.

### RN-12 — O pedido é recusado se não houver cardápio na data limite informada

O pedido procura o cardápio do tipo de órgão na data limite informada — dia, mês e ano
exatos — e, não achando, recusa com **\* Nao existem cardapios para esta data \***,
com o cursor no dia limite, sem registrar nada.

### RN-13 — A tela não altera o cadastro dos cardápios

A tela não inclui, não altera e não exclui cardápio nenhum; a única gravação que ela
alcança é a requisição do relatório. Quem mantém o cadastro dos cardápios são as telas
de manutenção, e esta aqui não deixa rastro de auditoria.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar os cardápios do órgão pela validade e pedir a relação

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C810C

  Cenário: Abrir a tela e ver os cardápios do meu órgão
    Quando abro a tela C810C
    Então vejo a lista dos cardápios do meu órgão, com a data de início, a data limite, o código e a descrição
    E vejo no máximo 13 cardápios por vez
    E nada é gravado

  Cenário: Consultar outra posição de validade
    Dado que informo o dia, o mês, o ano limite e o código de um cardápio do meu órgão
    Quando confirmo a consulta
    Então os valores informados passam a ser a posição da lista
    E os cardápios listados passam a sair a partir daquela posição

  Cenário: Consultar uma posição que não existe no cadastro
    Dado que informo um dia, um mês, um ano limite e um código de cardápio que não formam uma posição cadastrada
    Quando confirmo a consulta
    Então os quatro campos informados voltam a zero
    E nenhuma mensagem de recusa é mostrada

  Cenário: Órgão sem cardápio a partir da posição
    Dado que o meu órgão não tem cardápio a partir da posição de leitura
    Quando abro a tela
    Então o sistema avisa "* Cardapio nao cadastrado *"
    E a lista não é montada

  Cenário: Órgão com menos de 13 cardápios
    Dado que o meu órgão tem menos de 13 cardápios
    Quando abro a tela
    Então a lista termina antes da última linha
    E os quatro campos da posição aparecem zerados

  Cenário: Recusa de operação diferente da consulta
    Dado que o formulário me oferece o campo de operação
    E informo uma operação de manutenção
    Quando confirmo
    Então o sistema recusa com "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação

  Cenário: Recusa de dia, mês, ano ou cardápio não numérico
    Dado que informo letras no mês limite
    Quando confirmo
    Então o sistema recusa o mês
    E o cursor volta ao campo do mês limite

  Cenário: Recusa de acesso, quando a tela não está liberada
    Dado que a tela C810C não está liberada para o meu código de acesso
    Quando abro a tela
    Então o sistema recusa com "* Acesso negado para esta matricula *"

  Cenário: Pedir a relação de uma data limite
    Dado que informo o dia, o mês e o ano limite de um cardápio do meu órgão
    E preencho o código de impressão
    E tenho e-mail cadastrado
    E não há requisição desse relatório em processamento para o meu órgão
    Quando confirmo
    Então o sistema registra a requisição do relatório C81007 para o meu órgão
    E encaminha o pedido com a data limite informada e o código de impressão

  Cenário: Consulta sem código de impressão não registra nada
    Dado que informo o dia, o mês e o ano limite de um cardápio do meu órgão
    E deixo o código de impressão em branco
    Quando confirmo
    Então nenhuma requisição é registrada
    E nenhum cardápio é incluído, alterado ou excluído

  Cenário: Recusa por requisição do mesmo relatório em processamento
    Dado que já existe uma requisição do relatório C81007 para o meu órgão
    E preencho o código de impressão
    Quando confirmo
    Então o sistema recusa com "* Relatorio ja esta em processamento. Aguarde. *"
    E o cursor volta ao dia limite
    E nenhuma requisição nova é registrada

  Cenário: Recusa por falta de e-mail
    Dado que a minha matrícula não tem e-mail cadastrado
    E preencho o código de impressão
    Quando confirmo
    Então o sistema recusa com "* Usuario sem e-mail cadastrado *"
    E nenhuma requisição é registrada

  Cenário: Recusa por não haver cardápio na data informada
    Dado que informo uma data limite sem cardápio no meu órgão
    E preencho o código de impressão
    Quando confirmo
    Então o sistema recusa com "* Nao existem cardapios para esta data *"
    E o cursor volta ao dia limite
    E nenhuma requisição é registrada
```
