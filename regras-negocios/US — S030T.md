# US — S030T — Cadastro das telas e relatórios do sistema

## Estória

Como **servidor de CRE que administra o catálogo do sistema**, quero **cadastrar e
manter as telas e os relatórios — o tipo, o código, a descrição, a situação e as telas
ligadas a cada um —**, para que **exista uma lista única do que o sistema tem, de onde
cada tela se abre e quem pode operar cada uma**.

Toda tela e todo relatório do sistema precisa existir neste cadastro: é dele que a
navegação tira o destino da tela seguinte e é ele que a segurança consulta para decidir
se a tela existe e se o meu nível de acesso pode incluir, alterar, retirar ou consultar
nela. Sem este cadastro, acrescentar uma tela ao sistema só seria possível por fora dele;
e o que estiver errado aqui aparece para quem opera — uma tela fora do cadastro não abre,
e uma descrição errada é o nome que se lê por aí.

## Contexto

Jornada S000M → S001M → S004M → S030T.
Ator: servidor de CRE — administra o catálogo das telas e relatórios do sistema e as
autorizações de acesso de cada um.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os três passos anteriores da jornada são **menus**: encaminham a transação e não gravam
nada — nem registro de negócio, nem autorização de acesso. O contexto que esta tela usa
(a matrícula de quem opera, o nível de acesso, o privilégio, o tipo de órgão, a CRE e a
estação) é o que a entrada deixou na sessão; esta tela apenas o repassa às conferências
de rota e de acesso.

O comportamento desta tela **não muda conforme a tela que a chamou**: o que se vai fazer
com o registro vem do campo da operação, informado por quem opera. O único dado de
origem que ela trata é o campo da próxima tela, que ela repassa à conferência de rota
(RN-16).

As regras abaixo são só as desta tela.

---

## Regras de negócio

### RN-01 — O cadastro que esta tela mantém

Esta tela mantém o cadastro das telas e relatórios do sistema. Cada registro guarda sete
dados: o tipo (tela ou relatório), o código, a descrição, a situação, o código da tela de
menu por onde se chega à tela cadastrada, o código da tela de retorno de onde se vem, e a
marca de estado que o sistema mantém sozinho, dizendo se o registro está em uso ou
retirado.

O código tem seis posições e, junto com o tipo, identifica o registro: não pode haver
dois registros com o mesmo par (tipo, código). O cadastro tem capacidade para **2.000**
registros, e o seu índice por esse mesmo par para **2.000** entradas — capacidade é o
máximo esperado, parâmetro de dimensionamento, não o que está cadastrado.

A tela mostra ainda, ao lado dos dois códigos de tela, a descrição de cada um já
resolvida, e mantém um campo de próxima tela, que é dado de navegação (RN-16).

[?] O que a marca de estado significa além de "em uso" e "retirado", e quais valores a
situação aceita. O dicionário de dados não documenta os valores possíveis de nenhum dos
dois; as letras que o sistema grava na marca saem do mapeamento da própria rotina de
manutenção. Pergunta ao site.

### RN-02 — A tela abre pronta para incluir

Ao ser aberta, a tela mostra a data do sistema e a descrição do tipo de órgão da sessão,
deixa a operação já apontada para **incluir** e a situação como **não**, e **não traz
nenhum registro do cadastro** para os campos: o que aparece ali é o que o servidor vai
informar. Antes de abrir, ela ainda confere a matrícula, a estação e o acesso (as regras
da entrada estão no anexo de evidências).

### RN-03 — O campo da operação: o que se faz e o que se traz

O campo da operação acumula duas funções. As manutenções são **incluir**, **alterar**,
**retirar**, **consultar** e **expurgar**; os comandos que trazem um registro para a tela
são cinco: **o do tipo e do código informados**, **o primeiro**, **o último**, **o
seguinte** e **o anterior**. O que se digita é convertido para maiúsculas antes de
qualquer conferência.

A operação em branco é recusada: o sistema acusa que o tipo de manutenção não pode ficar
sem valor. Qualquer outro valor que não seja uma manutenção nem um dos cinco comandos é
avisado como tipo de manutenção inválido.

[?] O texto dos dois avisos acima — operação obrigatória e tipo de manutenção inválido —
é do catálogo de mensagens do ambiente, carregado por idioma na hora da execução; o
acervo lido só traz o literal de um idioma e o número da mensagem. Pergunta ao site.

[?] Não se pode afirmar que o aviso de tipo de manutenção inválido impeça o registro de
ser gravado: o despacho da recusa é do ambiente, e a única coisa que o programa usa para
desistir de gravar é a marca de falha da transação, que ele mesmo só liga no ramo da
consulta. Pergunta ao site.

[?] Os próprios códigos das operações — as três letras de incluir, alterar, retirar,
consultar e expurgar, e as dos cinco comandos — são entradas do catálogo de mensagens,
carregadas por idioma: o que se digita no campo da operação pode mudar com o idioma da
sessão. Pergunta ao site.

### RN-04 — Os cinco comandos que trazem um registro para a tela

Qualquer um dos cinco comandos lê o cadastro e traz o registro para os campos: o tipo, o
código, a descrição, a situação e os dois códigos de tela ligados. A descrição do tipo de
órgão, a data do sistema, o campo da próxima tela e as duas descrições das telas ligadas
ficam **em branco**: elas só são repostas pela abertura e pela consulta. Se o registro
trazido estiver retirado, o sistema avisa **"Key deleted"** (texto do catálogo de
mensagens).

O comando encerra a transação ali, reabrindo a própria tela: ele **não grava nada**.

[?] O que "primeiro", "último", "seguinte" e "anterior" percorrem, e em que ordem. As
leituras usam marcadores de posicionamento do dicionário de dados cujo efeito não está no
corpus nem no manual, e a rotina de leitura é importada da biblioteca de execução, sem
fonte no acervo. Pergunta ao site.

### RN-05 — Incluir e alterar exigem tipo, código e descrição

Numa inclusão e numa alteração, o tipo tem de ser **tela** ou **relatório**: com qualquer
outro valor, a recusa é **\* Informe tipo com T=Tela ou R=Relatorio \*** e o cursor volta
ao campo do tipo. O código é obrigatório: em branco, a recusa é
**\* Informe codigo da tela ou relatorio \*** e o cursor volta ao campo do código. Sendo o
tipo **tela**, a **última posição do código tem de estar em branco** — preenchida, o
sistema entende que o código é de relatório e recusa com
**\* Codigo corresponde a relatorio \***, com o cursor no campo do código. A descrição é
obrigatória: em branco, a recusa é
**\* Informe descricao da tela ou relatorio \***, com o cursor no campo da descrição.

Na **inclusão** há ainda três conferências de campo obrigatório, com o cursor no campo e
o texto do catálogo de mensagens: com o tipo e o código os dois em branco, o sistema acusa
que falta o código; com o tipo em branco, acusa que o campo do tipo não pode ficar sem
valor; com o código em branco, acusa o mesmo para o código.

[?] Os textos das três conferências de obrigatoriedade são do catálogo de mensagens do
ambiente, carregado de uma biblioteca por idioma na hora da execução; os literais do fonte
são os de um idioma, e o que o servidor lê na tela pode estar em português. O acervo lido
não traz a biblioteca de idiomas. Pergunta ao site.

### RN-06 — Relatório não tem tela de menu nem tela de retorno

Quando o tipo é **relatório**, a situação é forçada para **não** e os dois códigos de tela
são apagados: relatório não se abre por menu nem guarda de onde se vem. Quando o tipo é
**tela**, a situação só se mantém se já estiver marcada como ativa; caso contrário passa a
**não**.

### RN-07 — Retirar e consultar não conferem os campos

**Retirar** e **consultar** não passam pelas conferências de tipo, código e descrição:
elas valem só para incluir e alterar. As três conferências de campo obrigatório valem
apenas para a inclusão.

### RN-08 — Toda manutenção fica na auditoria

Cada inclusão, cada alteração e cada retirada deixa item na auditoria do sistema. O item
guarda a tela que executou a operação, a operação, a matrícula de quem opera, a CRE, o
tipo de órgão, o terminal, o dia, o mês, o ano e a hora do momento, e o conteúdo do
registro antes e depois da operação.

São **nove** pontos de gravação de auditoria no programa: **três** para o registro do
cadastro (um por operação de manutenção) e **seis** para os vínculos de acesso mexidos no
mesmo passo — a criação na inclusão, a exclusão e a recriação quando o registro estava
retirado, a liberação e a retirada das autorizações quando a situação muda, e a exclusão
em cascata na retirada. A consulta **não gera item de auditoria**.

[?] O que o servidor vê quando uma leitura ou uma gravação do depósito de dados falha. A
tela entrega o tratamento ao ambiente, e o acervo lido não traz nem a rotina nem o
significado dos códigos de ação. Pergunta ao site.

### RN-09 — Incluir cria o vínculo de acesso da tela

Ao incluir uma tela, o sistema cria também o vínculo dela com o **nível de acesso fixo que
a própria tela usa nas inclusões**, na tabela que diz o que cada nível pode fazer em cada
tela: nesse vínculo a **consulta fica sempre liberada**, e **incluir, alterar e retirar
ficam liberados somente quando a situação do registro está marcada como ativa**; não
estando, o vínculo nasce só com a consulta. É por essa tabela que a conferência de acesso
decide, a cada mensagem, se o meu nível pode operar a tela. A tabela tem sete campos e
capacidade para **10.000** vínculos, e a chave é o trio (nível de acesso, tipo, código).

[?] Qual é o nível de acesso fixo — o **99** — e o que ele significa no negócio. Ele não
é escolhido por quem opera: está gravado no programa e é o mesmo nas inclusões e no ramo
de reativação. O dicionário de dados não o documenta. Pergunta ao site.

### RN-10 — A situação governa as autorizações do vínculo

A situação do registro decide o que os vínculos autorizam. Numa alteração em que a
situação **não muda**, o sistema não mexe em vínculo nenhum. Quando a tela **deixa** de
estar ativa, o sistema percorre **todos** os níveis de acesso e regrava cada vínculo
existente sem as autorizações de incluir, alterar e retirar, mantendo a de consultar.
Quando a tela **volta** a estar ativa, o sistema devolve essas autorizações **apenas ao
nível de acesso fixo**. Os demais níveis ficam, depois de uma ida e volta da situação, só
com a consulta.

[?] Se essa assimetria é intencional. A retirada das autorizações varre a lista de níveis
de acesso, e a devolução lê um único nível fixo; nada no acervo lido diz que os outros
níveis devessem ser refeitos por outra tela nem que devessem ficar sem as autorizações.
Pergunta ao site.

### RN-11 — Retirar não apaga o registro

Retirar uma tela **não apaga** o registro: o sistema apaga os vínculos de acesso dela em
**todos** os níveis de acesso e marca o registro do cadastro como **retirado**. O registro
continua no cadastro, continua sendo encontrado pelos cinco comandos e continua sendo lido
pelo sistema — mas retirado. É a marca de retirado, e não a ausência do registro, que tira
a tela do ar.

### RN-12 — Um registro retirado avisa, e só a alteração o devolve ao uso

Sobre um registro **retirado**, o sistema avisa **"Key deleted"** (texto do catálogo de
mensagens) — e não avisa na alteração nem no expurgo. A **consulta** é avisada mas
acontece, e mostra o registro. Sobre esse mesmo registro retirado, a **inclusão** e a
**retirada** do código avisam, e a retirada de um já retirado também.

A **alteração** de um registro retirado é aceita sem aviso e o devolve ao uso; ao fazê-lo,
o sistema apaga os vínculos de acesso desse registro em **todos** os níveis e recria
apenas o do nível de acesso fixo, com a consulta liberada e as autorizações conforme a
situação que a alteração deixou.

[?] Se o aviso de registro retirado interrompe a operação. Ele é despachado como aviso de
campo, e a única coisa que decide se o vínculo e o registro são gravados depois disso é a
marca de falha da transação, que neste programa só é ligada no ramo da consulta: quem a
liga nos avisos é a rotina de comunicação do ambiente, sem corpo no acervo lido. Se ela
não ligar, a operação sobre o registro retirado acontece apesar do aviso. Pergunta ao
site.

### RN-13 — A exclusão definitiva é recusada

A exclusão definitiva do registro **não é oferecida**: informando a operação de expurgo, o
sistema avisa **"PUR not allowed"** (texto do catálogo de mensagens) e **não deveria**
apagar o registro — o caminho normal de retirada marca o registro como retirado e o deixa
no cadastro.

[?] A guarda que recusa o expurgo e o ramo que apaga fisicamente o registro **não
fecham**: a guarda recusa exatamente a operação de que o ramo depende para apagar, e entre
a guarda e o ramo não há nenhuma conferência da marca de falha. Ou o ramo é inalcançável,
ou o registro é apagado de fato apesar do aviso. O acervo não mostra quem liga a marca de
falha. Pergunta ao site — não se escolhe um dos dois lados.

### RN-14 — A consulta mostra as telas ligadas e não grava nada

Na consulta, o sistema mostra o que está no cadastro para o tipo e o código informados —
inclusive a descrição guardada e a situação — e completa a tela com os nomes das telas
ligadas: lê o registro da **tela de menu** informada e o registro da **tela de retorno**
informada, e mostra a descrição de cada um no seu campo. O caminho usual é trazer o
registro para a tela e então consultar, porque a leitura do cadastro é feita pelo tipo e
pelo código que estiverem nos campos.

A consulta **não inclui, não altera, não retira e não gera item de auditoria**: no fim
dela o próprio programa marca a transação como falha, e as duas rotinas que gravam
desistem por causa dessa marca. O tratamento da consulta que existe escrito dentro da
rotina que grava o registro nunca é alcançado, pela mesma razão.

### RN-15 — Os comandos que levam à tela de menu e à tela de retorno

O campo da operação também aceita os comandos que levam a outra tela: ir para a **tela de
menu** cadastrada para a tela em que se está e voltar para a **tela de retorno** também
cadastrada. Se o cadastro da tela em que se está não tiver o código correspondente, o
aviso é **\* Operacao nao disponivel \*** e a tela continua onde está. Quando o comando
funciona, a transação é encaminhada para essa tela e a S030T encerra **sem operar o
cadastro**.

### RN-16 — A próxima tela preenchida desvia a transação

A tela leva o seu campo de **próxima tela** para a conferência de rota. Vindo preenchido,
a transação é encaminhada para a tela indicada e a S030T encerra sem operar o cadastro —
nem inclui, nem altera, nem retira, nem consulta.

[?] Nada no acervo lido preenche esse campo por esta tela; quem o preenche, se alguém o
preenche, não está no acervo. O leiaute da máscara, que diria se o campo é oferecido a
quem opera, também não está no acervo lido. Pergunta ao site.

### RN-17 — O cabeçalho só se mantém na abertura

Cada mensagem enviada à tela começa apagando a **data do sistema**, a **descrição do tipo
de órgão** da sessão e as duas descrições das telas ligadas. Só a abertura repõe a data do
sistema e a descrição do tipo de órgão; as duas descrições das telas ligadas são repostas
pela consulta. O resultado da operação anterior, portanto, não fica na tela.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe um
caminho de entrada em que os campos não são limpos, não foi possível determinar. Pergunta
ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Cadastro das telas e relatórios do sistema

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S030T

  Cenário: A tela abre pronta para incluir
    Dado que abro a tela S030T
    Então vejo a data do sistema e a descrição do tipo de órgão da minha sessão
    E o campo da operação já traz a inclusão
    E o campo da situação traz não
    E nenhum registro do cadastro aparece nos campos

  Cenário: Inclusão de uma tela
    Dado que o cadastro de telas e relatórios não tem a tela C900T
    Quando informo a inclusão, o tipo tela, o código C900T e a descrição da tela
    Então a tela é cadastrada
    E o vínculo de acesso dela libera a consulta
    E o vínculo não autoriza incluir, alterar nem retirar
    E a inclusão fica registrada na auditoria

  Cenário: Inclusão de uma tela já ativa
    Dado que o cadastro não tem a tela C901T
    Quando informo a inclusão, o tipo tela, o código C901T, a descrição e a situação ativa
    Então a tela é cadastrada
    E o vínculo de acesso dela autoriza consultar, incluir, alterar e retirar

  Cenário: Inclusão de um relatório
    Dado que o cadastro não tem o relatório N900R
    Quando informo a inclusão, o tipo relatório, o código N900R e a descrição do relatório
    Então o relatório é cadastrado
    E ele fica sem tela de menu e sem tela de retorno
    E a situação dele fica como não

  Cenário: Tipo diferente de tela e de relatório
    Dado que estou na tela S030T
    Quando informo a inclusão com um tipo que não é tela nem relatório
    Então vejo a mensagem "* Informe tipo com T=Tela ou R=Relatorio *"
    E o cursor volta ao campo do tipo

  Cenário: Inclusão sem código
    Dado que estou na tela S030T
    Quando informo a inclusão com o tipo tela e sem o código
    Então vejo a mensagem "* Informe codigo da tela ou relatorio *"
    E o cursor volta ao campo do código

  Cenário: Código de tela com a última posição preenchida
    Dado que estou na tela S030T
    Quando informo a inclusão, o tipo tela e um código com a última posição preenchida
    Então vejo a mensagem "* Codigo corresponde a relatorio *"
    E o cursor volta ao campo do código

  Cenário: Inclusão sem descrição
    Dado que estou na tela S030T
    Quando informo a inclusão, o tipo tela, o código e nenhuma descrição
    Então vejo a mensagem "* Informe descricao da tela ou relatorio *"
    E o cursor volta ao campo da descrição

  Cenário: Inclusão com o tipo e o código em branco
    Dado que estou na tela S030T
    Quando informo a inclusão sem o tipo e sem o código
    Então o sistema acusa que falta o código
    E o cursor fica no campo do código

  Cenário: Campo obrigatório em branco na inclusão
    Dado que estou na tela S030T
    Quando informo a inclusão com o tipo em branco
    Então o sistema acusa que o campo do tipo não pode ficar sem valor
    E o cursor fica no campo do tipo

  Cenário: Operação em branco
    Dado que estou na tela S030T
    Quando envio a tela sem informar a operação
    Então o sistema acusa que o tipo de manutenção não pode ficar sem valor
    E o cursor fica no campo da operação

  Cenário: Operação desconhecida
    Dado que estou na tela S030T
    Quando informo no campo da operação um valor que não é manutenção nem comando
    Então o sistema avisa que o tipo de manutenção é inválido

  Cenário: Alteração de uma tela
    Dado que o cadastro tem a tela C900T
    Quando trago a tela para os campos e altero a descrição
    Então a descrição nova fica no cadastro
    E a alteração fica registrada na auditoria

  Cenário: Inativar a tela retira as autorizações de todos os níveis de acesso
    Dado que o cadastro tem a tela C900T com a situação ativa
    E existem vínculos de acesso dessa tela em mais de um nível
    Quando trago a tela para os campos e altero a situação para não
    Então todos os vínculos deixam de autorizar incluir, alterar e retirar
    E todos continuam autorizando consultar

  Cenário: Reativar a tela devolve as autorizações só ao nível fixo
    Dado que a tela C900T está com a situação não e com os vínculos sem as autorizações
    Quando trago a tela para os campos e altero a situação para ativa
    Então o vínculo do nível fixo do cadastro volta a autorizar incluir, alterar e retirar
    E os vínculos dos demais níveis continuam só com a consulta

  Cenário: Retirar uma tela não a apaga
    Dado que o cadastro tem a tela C900T
    Quando trago a tela para os campos e informo a retirada
    Então os vínculos de acesso da tela são apagados em todos os níveis
    E o registro fica marcado como retirado
    E o registro continua no cadastro
    E a retirada fica registrada na auditoria

  Cenário: Inclusão de um registro retirado avisa
    Dado que a tela C900T está retirada
    Quando informo a inclusão do código C900T
    Então vejo o aviso "Key deleted"

  Cenário: Consultar um registro retirado
    Dado que a tela C900T está retirada
    Quando trago a tela para os campos e informo a consulta
    Então vejo o aviso "Key deleted"
    E vejo a descrição guardada da tela
    E nada é gravado

  Cenário: Alterar um registro retirado o devolve ao uso
    Dado que a tela C900T está retirada
    Quando trago a tela para os campos e informo a alteração
    Então o registro volta ao uso
    E os vínculos de acesso dos demais níveis são apagados
    E o vínculo do nível fixo do cadastro é recriado
    E a alteração fica registrada na auditoria

  Cenário: Exclusão definitiva
    Dado que o cadastro tem a tela C900T
    Quando informo a operação de expurgo
    Então vejo o aviso "PUR not allowed"
    E a tela continua com a retirada como a forma de tirar o registro do uso

  Cenário: Trazer um registro para a tela
    Dado que o cadastro tem a tela C900T
    Quando informo o comando de trazer o registro do tipo e do código informados
    Então vejo o tipo, o código e a descrição da tela nos campos
    E a data do sistema, a descrição do tipo de órgão e o campo da próxima tela ficam vazios
    E as duas descrições das telas ligadas ficam vazias
    E nada é gravado

  Cenário: Consulta mostra as telas ligadas
    Dado que o cadastro tem a tela C900T com tela de menu e tela de retorno informadas
    Quando trago a tela para os campos e informo a consulta
    Então vejo a descrição da tela de menu no seu campo
    E vejo a descrição da tela de retorno no seu campo
    E nada é incluído, alterado, retirado ou registrado na auditoria

  Cenário: Comando para a tela de menu
    Dado que o cadastro da tela em que estou tem uma tela de menu
    Quando informo o comando de ir para a tela de menu
    Então a transação é encaminhada para essa tela
    E o cadastro não é operado

  Cenário: Comando para a tela de menu sem tela cadastrada
    Dado que o cadastro da tela em que estou não tem tela de menu
    Quando informo o comando de ir para a tela de menu
    Então vejo a mensagem "* Operacao nao disponivel *"
    E continuo na tela S030T

  Cenário: Próxima tela preenchida
    Dado que a tela chega com uma próxima tela indicada
    Quando envio a tela
    Então a transação é encaminhada para a tela indicada
    E o cadastro não é operado

  Cenário: O cabeçalho só se mantém na abertura
    Dado que abri a tela e vi a data do sistema e a descrição do tipo de órgão
    Quando envio uma mensagem
    Então a data do sistema e a descrição do tipo de órgão não ficam na tela
```
