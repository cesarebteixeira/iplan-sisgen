# US — C071C — Consultar os cardápios de uma data limite e pedir a listagem

## Estória

Como **servidor de CRE**, quero **informar o dia, o mês e o ano limite de um cardápio e
ver os cardápios do meu órgão que terminam nessa data, pedindo a listagem deles**, para
que **eu confira o que estava valendo no período e leve a relação dos cardápios daquela
validade para quem precisa dela**.

O cardápio reúne os gêneros da alimentação escolar e cada versão dele vale por um
período, com uma data de início e uma data limite. É a data limite que diz a que momento
o cardápio pertence, e mais de um cardápio pode terminar no mesmo dia. Esta tela é a
porta dessa relação: ela não inclui, não altera e não exclui cardápio nenhum — isso é
das telas de manutenção —, mas é dela que sai o pedido da listagem, e é por isso que ela
também confere, recusa e registra.

## Contexto

Jornada S000M → C000M → C070M → C071C.
Ator: servidor de CRE — consulta os cardápios do seu órgão pela data limite e pede a
listagem deles.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. Os dois menus do caminho não gravam nada:
só encaminham.

O que esta tela usa do que veio antes vem do vínculo da matrícula com a secretaria
escolhida no `LOGON`: o **tipo de órgão**, que decide de que órgão são os cardápios
mostrados, e a **matrícula**, o **código de acesso** e o **privilégio**; usa também a
**data do sistema**. Essas são regras da entrada e estão no anexo de evidências, em
**Regras que se revelaram da entrada**.

A jornada termina nesta tela: ela não encaminha para nenhuma outra e não recebe cadastro
de tela nenhuma. O modo de operação dela não vem de quem a chamou (RN-06).

## Regras de negócio

### RN-01 — A tela consulta os cardápios do órgão, e é daqui que sai o pedido da listagem

Esta é uma tela de **consulta**, e o assunto dela é o **cardápio**. Ela mostra os
cardápios do **tipo de órgão** que o meu vínculo com a secretaria deixou na sessão —
nunca de um órgão digitado, que não se digita aqui. No cabeçalho ela mostra a
**descrição do tipo de órgão** e a **data do sistema**.

A tela **não inclui, não altera e não exclui cardápio nenhum**, e não deixa registro de
auditoria: quem mantém o cadastro dos cardápios são as telas de manutenção. A única
gravação que ela alcança é a **requisição da listagem** (RN-11), e só quando o servidor a
pede. Sem o pedido, consultar não grava nada.

### RN-02 — O cardápio, e como a tela o procura

Cada cardápio pertence a um **tipo de órgão**, tem um **código**, uma **descrição**, uma
**data de início** e uma **data limite**. O conjunto pelo qual a tela lê está ordenado
pelo tipo de órgão e pela data limite e não admite o **mesmo código de cardápio repetido
na mesma data limite** do mesmo órgão — cardápios de códigos diferentes podem terminar
no mesmo dia.

A tela informa o tipo de órgão da sessão e a data limite, e é por esse par que ela
procura. O **código do cardápio** também entra na procura, porém **zerado**, e a
conferência que vem depois não o olha.

[?] Se o código zerado participa da procura, a tela procuraria um cardápio de código
zero e não acharia nenhum; se não participa, ela se posiciona pelo órgão e pela data
limite. O que os sinalizadores da leitura fazem não está no acervo: a leitura é de uma
rotina de biblioteca, sem corpo no lote. Pergunta ao site.

### RN-03 — A relação tem até 13 linhas, e cada linha informa quatro dados

São **13 linhas** por vez. Cada linha traz a **data de início**, a **data limite**, o
**código do cardápio** e a **descrição** dele, com as datas montadas no formato
**dia/mês/ano**. Fora da relação, a tela traz a descrição do tipo de órgão e a data do
sistema.

A relação começa na posição em que a abertura a deixou (RN-04) e segue a ordem do
cadastro: o tipo de órgão e, dentro dele, a data limite.

### RN-04 — A abertura posiciona a relação pela data do sistema

Ao abrir, a tela procura o cardápio do meu órgão cuja **data limite é a data do
sistema** — o dia, o mês e o ano de hoje — e leva para os campos de limite o **ano** e o
**mês** desse cardápio. O **dia não é trazido**: o campo do dia aparece zerado, e quem
for pedir a listagem precisa informá-lo.

[?] Na última linha da relação a tela copia para os campos de limite a data completa do
último cardápio lido. Se a relação chega às 13 linhas, o dia deixa de aparecer zerado;
se não chega, ele fica zero. Qual dos dois o servidor deve ver, o acervo não diz.
Pergunta ao site.

### RN-05 — O dia, o mês e o ano informados são números, e o cursor volta ao campo recusado

Os três campos — **dia limite**, **mês limite** e **ano limite** — são editados como
número antes de qualquer leitura, e em branco valem zero. A edição trata o dia e o mês
com dois dígitos e o ano com quatro. Quando ela acusa erro, o cursor volta ao campo
recusado: o dia, depois o mês, depois o ano.

### RN-06 — A tela é de consulta: só a consulta é aceita, e ela é adotada sempre

O campo de operação aceita **apenas a consulta**. A própria tela o preenche com a
consulta quando abre, e ao confirmar uma operação de inclusão, de alteração ou de
exclusão ela recusa com **\* Operacao nao disponivel. Use CON \***, devolve o cursor ao
campo da operação e não lê nem pede mais nada. Uma operação em branco, ou um valor que
não seja nenhuma das operações que o sistema conhece, é recusada antes disso, na
conferência de rota, com **\* Operacao nao disponivel \***.

O modo da tela **não depende de quem a chamou**: venha do menu ou de outra tela, ela
adota a consulta. Não há nesta tela nenhuma comparação com a tela de origem.

[?] A recusa manda usar "CON", mas o que a tela compara é o código interno de consulta, e
nenhum valor "CON" aparece no fonte lido. Ou a máscara traduz o que o servidor digita, ou
quem seguir a mensagem é recusado. A máscara da tela não veio no lote, então também não
dá para afirmar que o campo da operação aparece nela. Pergunta ao site.

### RN-07 — A tela só opera com a tela e o código de acesso autorizados

Antes de mostrar a relação, a abertura confere se a **tela** está no cadastro de telas e
se o meu **código de acesso** tem registro para ela. Faltando a tela, o aviso é
**\* Tela nao disponivel \***; faltando o registro do código de acesso, o aviso é
**\* Acesso negado para esta matricula \***. Nos dois casos a sessão volta ao menu
principal e nada é consultado nem pedido.

Na mensagem do servidor a tela passa ainda pela conferência de **rota** e pela de
**permissão da operação**. A tela marcada como excluída no cadastro de telas é recusada
com **\* Tela nao cadastrada \***. Como a única operação aceita é a consulta, a
conferência de permissão não chega a exigir permissão de inclusão, de alteração ou de
exclusão.

### RN-08 — O código da próxima tela leva a transação para aquela tela

Se a mensagem chegar com o **código da próxima tela** preenchido, a transação segue para
a tela informada e mais nada desta tela é processado: a relação não é remontada, nenhuma
conferência do pedido é feita e nada é registrado. Em branco, a tela segue o seu curso
normal.

[?] Nenhuma linha deste programa preenche esse campo, e a máscara não veio no lote: o que
o servidor digita para disparar a passagem, e se o campo aparece na tela, o acervo não
mostra. Pergunta ao site.

### RN-09 — Órgão sem cardápio a partir da posição de abertura a tela avisa

Quando a primeira leitura da relação não encontra cardápio do órgão a partir da posição
de abertura, a tela avisa **\* Cardapio nao cadastrado \***, zera os limites que traria
e não monta a relação. O aviso é dado uma vez, na montagem da primeira linha.

[?] A conferência que decide o aviso olha só o tipo de órgão: ela não distingue "o órgão
não tem cardápio nenhum" de "não há cardápio a partir da posição de abertura". Se o
aviso pode sair no segundo caso, o acervo não mostra. Pergunta ao site.

### RN-10 — Informar outra data limite reposiciona a leitura; não achando, os campos voltam a zero

Se a data informada for diferente da que a tela já trazia, a tela larga a posição
anterior e procura de novo o cardápio do órgão com a data informada. **Não achando, os
três campos voltam a zero, sem mensagem**; achando, a data informada passa a ser a da
tela.

Essa procura da consulta confere só o tipo de órgão; a mesma procura, no caminho do
pedido, confere também o ano, o mês e o dia (RN-14). É o que faz o mesmo "não achou" ser
silencioso na consulta e virar recusa no pedido.

[?] A relação de linhas é montada quando a tela abre, e a releitura feita quando a data
muda não a remonta: se as linhas passam a mostrar os cardápios da data nova ou continuam
as da abertura, o fonte não fecha. Pergunta ao site.

### RN-11 — Com o código de impressão preenchido, a tela registra a requisição da listagem e a encaminha

Preenchido o **código de impressão**, a tela registra uma **requisição** no cadastro de
requisições de relatório: o **relatório C71001** — a relação dos cardápios —, o **tipo de
órgão** do servidor, a **matrícula**, a **estação**, a **data do sistema** como data do
pedido, a situação em branco e o **número da requisição**, que é o da **última
requisição registrada mais um** (se esse número já existir, a tela volta a buscar a
última e refaz). A requisição nasce como **inclusão**.

Registrada a requisição, o pedido é **encaminhado para processamento** quando o ambiente
é o do produto LINC, levando a estação, a matrícula, o **e-mail do servidor**, o
**código de impressão**, **uma via** e os parâmetros do relatório: o **tipo de órgão** e
a **data limite informada**. A listagem que sai daí traz a **validade do cardápio** —
início e limite — e uma linha por cardápio, com o **código** e a **descrição**.

**Sem o código de impressão, nada é registrado**: a consulta termina sem gravação. E nem
o código de impressão nem o e-mail ficam guardados na requisição — os dois seguem no
encaminhamento.

[?] Quem consome o código de impressão e o e-mail — formulário, destino ou fila de
impressão — não está no lote: o programa do relatório recebe como parâmetros só o órgão
e a data limite. Pergunta ao site.

[?] O encaminhamento só acontece no ambiente do produto LINC. O que sobra do pedido
quando ele não acontece — a requisição registrada e não processada — o acervo não mostra.
Pergunta ao site.

### RN-12 — O pedido é recusado enquanto houver requisição do mesmo relatório para o órgão

Havendo **qualquer requisição do relatório C71001 para o meu tipo de órgão**, o pedido é
recusado com **\* Relatorio ja esta em processamento. Aguarde. \***, com o cursor de volta
no dia limite, e nada é registrado. A requisição não fica presa: é o próprio relatório
que a apaga quando termina.

[?] A recusa não olha a situação da requisição: qualquer registro do mesmo relatório e
órgão barra o pedido, e só o relatório o retira. Se o processamento não chegar a rodar e
a requisição sobrar, o órgão fica sem poder pedir de novo — a entrada apaga as
requisições vencidas, mas isso é regra dela. Pergunta ao site.

### RN-13 — O pedido exige e-mail cadastrado para o servidor

O pedido lê o cadastro do funcionário pela **matrícula da sessão** e exige **e-mail
preenchido**; sem e-mail, recusa com **\* Usuario sem e-mail cadastrado \*** e não
registra nada.

### RN-14 — O pedido é recusado se não houver cardápio na data informada

O pedido procura o cardápio do órgão com a **data limite informada — dia, mês e ano
exatos** — e, não achando, recusa com **\* Nao existem cardapios para esta data \***, com
o cursor no dia limite, e não registra nada.

### RN-15 — Falha no banco é avisada pela rotina do sistema e impede a gravação

Toda leitura desta tela testa o erro do banco: o erro é despachado para a rotina de
comunicação do sistema com a ação de erro de acesso, que avisa o usuário e marca a falha
que impede a requisição de ser gravada. A gravação da requisição, quando falha, é
despachada como erro de gravação.

## Cenários BDD

```gherkin
Funcionalidade: Consultar os cardápios de uma data limite e pedir a listagem

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C071C

  Cenário: RN-01 e RN-03 — consultar os cardápios do meu órgão
    Dado que estou na tela C071C
    Quando confirmo a consulta
    Então vejo, no cabeçalho, a descrição do tipo de órgão da minha sessão e a data do sistema
    E vejo, em cada linha, a data de início, a data limite, o código do cardápio e a descrição dele
    E nada é gravado

  Cenário: RN-03 — a relação mostra 13 linhas e segue a ordem do cadastro
    Dado que o meu órgão tem mais de 13 cardápios a partir da posição de abertura
    Quando confirmo a consulta
    Então vejo 13 cardápios na relação
    E a relação segue a ordem do cadastro: o tipo de órgão e, dentro dele, a data limite

  Cenário: RN-04 — a abertura posiciona a relação pela data do sistema
    Dado que existe cardápio do meu órgão com a data limite de hoje
    Quando abro a tela C071C
    Então o ano e o mês limite aparecem preenchidos com os do cardápio da data de hoje
    E o dia limite aparece zerado

  Cenário: RN-05 — mês limite não numérico
    Dado que estou na tela C071C
    Quando informo letras no mês limite e confirmo
    Então o sistema recusa o mês
    E o cursor volta ao campo do mês limite

  Cenário: RN-05 — ano limite não numérico
    Dado que estou na tela C071C
    Quando informo letras no ano limite e confirmo
    Então o sistema recusa o ano
    E o cursor volta ao campo do ano limite

  Cenário: RN-06 — a tela abre em consulta venha de onde vier
    Dado que a opção 4 do menu C070M me encaminhou para a tela C071C
    Quando a tela abre
    Então o campo de operação vem preenchido com a consulta
    E não há nesta tela nenhuma conferência da tela de origem

  Cenário: RN-06 — operação diferente da consulta
    Dado que estou na tela C071C
    Quando informo uma operação de manutenção e confirmo
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nada é lido e nada é registrado

  Cenário: RN-06 — operação em branco
    Dado que estou na tela C071C
    Quando deixo o campo da operação em branco e confirmo
    Então vejo "* Operacao nao disponivel *"
    E nada é lido e nada é registrado

  Cenário: RN-07 — o meu código de acesso não tem registro para esta tela
    Dado que o meu código de acesso não tem registro para a tela C071C
    Quando a tela abre
    Então vejo "* Acesso negado para esta matricula *"
    E volto ao menu principal

  Cenário: RN-07 — a tela não está no cadastro de telas
    Dado que o cadastro de telas não tem a tela C071C
    Quando a tela abre
    Então vejo "* Tela nao disponivel *"
    E volto ao menu principal

  Cenário: RN-08 — o código da próxima tela informado
    Dado que estou na tela C071C
    Quando informo o código de outra tela e confirmo
    Então a transação segue para a tela informada
    E nada mais desta tela é processado

  Cenário: RN-09 — órgão sem cardápio a partir da data do sistema
    Dado que o meu órgão não tem cardápio a partir da data do sistema
    Quando abro a tela C071C
    Então vejo "* Cardapio nao cadastrado *"
    E a relação não é montada

  Cenário: RN-10 — informar outra data limite que tem cardápio
    Dado que estou na tela C071C
    Quando informo o dia, o mês e o ano limite de um cardápio do meu órgão
    Então a tela passa a guardar a data que informei
    E nada é gravado

  Cenário: RN-10 — informar outra data limite que não tem cardápio
    Dado que estou na tela C071C
    Quando informo uma data limite sem cardápio no meu órgão
    Então os três campos de limite voltam a zero
    E nenhuma mensagem de recusa é mostrada

  Cenário: RN-11 — pedir a listagem de uma data limite
    Dado que informo o dia, o mês e o ano limite de um cardápio do meu órgão
    E preencho o código de impressão
    E tenho e-mail cadastrado
    E não há requisição do relatório C71001 para o meu órgão
    Quando confirmo
    Então o sistema registra a requisição do relatório C71001 para o meu tipo de órgão
    E o pedido é encaminhado com a data limite que informei e com uma via
    E a listagem traz a validade do cardápio e uma linha por cardápio, com o código e a descrição

  Cenário: RN-11 — consulta sem o código de impressão não registra nada
    Dado que informo o dia, o mês e o ano limite de um cardápio do meu órgão
    E deixo o código de impressão em branco
    Quando confirmo
    Então nenhuma requisição é registrada
    E nenhum cardápio é incluído, alterado ou excluído

  Cenário: RN-12 — já existe requisição do mesmo relatório para o órgão
    Dado que já existe uma requisição do relatório C71001 para o meu tipo de órgão
    E preencho o código de impressão
    Quando confirmo
    Então vejo "* Relatorio ja esta em processamento. Aguarde. *"
    E o cursor volta ao dia limite
    E nenhuma requisição nova é registrada

  Cenário: RN-12 — o relatório apaga a requisição ao terminar
    Dado que existe uma requisição do relatório C71001 para o meu tipo de órgão
    Quando o relatório é processado até o fim
    Então a requisição é apagada
    E um novo pedido da mesma listagem volta a ser aceito

  Cenário: RN-13 — matrícula sem e-mail cadastrado
    Dado que a minha matrícula não tem e-mail cadastrado
    E preencho o código de impressão
    Quando confirmo
    Então vejo "* Usuario sem e-mail cadastrado *"
    E nenhuma requisição é registrada

  Cenário: RN-14 — não há cardápio na data informada
    Dado que informo uma data limite sem cardápio no meu órgão
    E preencho o código de impressão
    Quando confirmo
    Então vejo "* Nao existem cardapios para esta data *"
    E o cursor volta ao dia limite
    E nenhuma requisição é registrada

  Cenário: RN-15 — falha do banco durante a consulta
    Dado que a leitura do cadastro dos cardápios falha no banco
    Quando confirmo a consulta
    Então vejo a mensagem de erro do sistema
    E a requisição da listagem não é gravada
```
