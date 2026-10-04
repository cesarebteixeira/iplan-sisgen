# US — N033T — Registrar e consultar o número SEI do processo

## Estória

Como **servidor da CRE**, quero **registrar o número SEI de um processo
administrativo — ou consultar o que já está registrado —**, para que **o processo
fique identificado no sistema pelo mesmo número que ele tem no SEI e a despesa dele
possa seguir**.

O número SEI é o que liga o processo administrativo à despesa que ele originou: é por
ele que o processo é reconhecido e conferido no restante do sistema. Sem esse número
registrado, o processo fica sem a sua identificação eletrônica e o acompanhamento da
despesa se perde. A tela serve também para consultar o número que já está lá, sem
alterá-lo, e para ver em que pé está o processo.

## Contexto

Jornada S000M → N000M → N050M → N033T.

Ator: servidor de CRE — informa o número do processo e o número SEI que ele tem, ou
consulta o número já registrado.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio.

As duas telas anteriores da jornada são menus e só encaminham: não deixam processo,
número SEI nem operação para esta tela. O que a N033T usa da sessão — matrícula,
código de acesso, privilégio, tipo de órgão e CRE — é o que a entrada deixou, e a tela
apenas o repassa às conferências e o leva à auditoria. A tela **não muda de
comportamento conforme quem a chamou**: abre sempre em consulta, e quem decide entre
alterar e consultar é o servidor, no campo da operação.

A tela mostra o número do processo em quatro caixas, o número SEI em quatro caixas, a
descrição do tipo de órgão, a data do sistema, o número SEI já registrado sob um
rótulo e a linha de mensagem. Ela é o último passo desta jornada e **não encaminha o
servidor a outra tela**: nas recusas permanece nela mesma e, na recusa do serviço
externo de processos, reabre-se.

---

## Regras de negócio

### RN-01 — A tela altera ou consulta o número SEI; não inclui nem exclui

A tela faz duas coisas com o número SEI do processo: **alterar** — registrar o número
que o processo tem no SEI — e **consultar**. Ao abrir, ela se apresenta na consulta.
Qualquer outra operação é recusada com
**\* Operacao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da operação
e nada é lido nem gravado.

Inclusão e exclusão não existem nesta tela: o número SEI de um processo se informa
alterando o processo, não criando nem apagando processo.

[?] A recusa manda usar **ALT** e **CON**, mas essas duas palavras não são valor
nenhum aceito pelo sistema: o que a tela compara são os códigos internos de alteração
e de consulta, e é o código de consulta que ela mesma escreve no campo quando ele vem
em branco. Ou o formulário da tela traduz o que o servidor digita, ou a recusa indica
valores que o sistema não reconhece. Pergunta ao site.

### RN-02 — O processo é um número de catorze dígitos, informado em quatro caixas

O processo é identificado por um número de **catorze** dígitos. A tela o recebe em
quatro caixas — duas de **2 dígitos**, uma de **6** e uma de **4**. Se a **segunda
caixa** ficar em branco — ou zerada —, os dois dígitos da primeira passam a valer como
a **segunda dupla** do número, e as duas primeiras posições do número ficam zeradas. O
número que a tela procura é sempre o mesmo, seja ele digitado numa forma ou na outra.

[?] O número é montado de uma forma quando a segunda caixa vem preenchida e de outra
quando ela vem zerada, e o que cada posição do número significa por dentro não está no
acervo lido. Pergunta ao site.

### RN-03 — A tela abre em consulta, e as duas primeiras caixas vêm do cadastro do tipo de órgão

Ao abrir, a tela assume sozinha a **consulta**. A **primeira caixa** do número do
processo vem preenchida com um código de duas posições tirado do cadastro do **tipo de
órgão da sessão**; quando aquele cadastro traz ligado o indicador de numeração própria,
a **segunda caixa** vem preenchida com a **CRE do vínculo da sessão**. No número SEI, a
caixa de **quatro dígitos** vem preenchida com o **ano do sistema**. A tela mostra
ainda a **descrição do tipo de órgão** e a **data do sistema**.

Esse comportamento não depende de quem abriu a tela: o menu que a antecede só a invoca,
sem passar processo, número SEI ou operação.

[?] O indicador do cadastro do tipo de órgão só é comparado com "S" e com "N": o
dicionário de dados não traz domínio nem comentário para ele, e nenhuma tela desta
jornada o descreve em negócio. O que ele significa — e por que decide se a CRE entra no
número — pergunta ao site.

### RN-04 — A tela retoma o processo e o número SEI do uso anterior

Se a tela já foi usada, ela repõe o **processo** e o **número SEI** que ficaram em uso,
espalhados pelas caixas, e apresenta o número SEI reunido e formatado, sob um rótulo.
Se não foi, ela abre sem processo nenhum. O que a tela guarda sobrevive de uma operação
para a outra; a consulta recusada esquece o processo que estava em uso.

[?] De quem é o que a tela guarda — do terminal, do servidor ou só da tela — o acervo
lido não documenta. Pergunta ao site.

### RN-05 — As oito caixas de número passam por edição numérica

As **oito** caixas de número da tela — as quatro do processo e as quatro do número SEI
— passam por edição antes de qualquer leitura de cadastro: o que estiver em branco vira
zero, os zeros à esquerda caem e o que não for número é recusado, com o cursor de volta
ao primeiro campo recusado. O que não passa por essa edição não chega a ser procurado
no cadastro.

[?] A edição é feita por um serviço do ambiente, que não faz parte do acervo lido, e
**uma** das oito caixas — a primeira do processo — não tem posição de cursor declarada:
quando a edição a recusa, não se sabe para onde o cursor volta. Pergunta ao site.

### RN-06 — O número SEI é informado em quatro caixas, e a segunda é obrigatória

O número SEI do processo é informado em quatro caixas — **6, 6, 4 e 2 dígitos** —, que a
tela reúne num único número de **dezoito** dígitos e apresenta formatado. A **segunda
caixa** não pode ficar zerada: sem ela, a alteração é recusada com **\* Informe o SEI
\*** e o cursor volta a essa caixa.

[?] O número reunido tem dezoito dígitos e o cadastro reserva **dezessete** posições
para ele. O que acontece com a última posição gravada não se conclui do acervo. Pergunta
ao site.

### RN-07 — O número SEI já registrado em qualquer documento não pode ser informado de novo

Antes de gravar, a tela procura o número SEI informado nos documentos dos processos —
de **qualquer** processo. Achando, a alteração é recusada com **<- SEI ja cadastrado
\***, o cursor volta à segunda caixa do número SEI e nada é gravado. Um número SEI
pertence a um processo só.

### RN-08 — A alteração exige que o processo tenha sido consultado antes

Com a operação de alteração, o processo informado tem de ser exatamente o que a consulta
anterior deixou em uso. Sendo outro, a recusa é **\* Consulte antes de atualizar \***, o
cursor volta ao campo da operação e nada é gravado. É a consulta que escolhe o processo
a alterar.

[?] A consulta só deixa o processo em uso quando **não** o encontra no cadastro de
empenhos nem na relação de integração com o SIAFIC — e é justamente nesses dois casos
que ela recusa e esquece o processo. Lendo as duas guardas juntas, o processo que a
consulta recusa não tem por onde ser alterado, e o servidor que acabou de consultá-lo vê
"consulte antes de atualizar". Ou a limpeza do processo vale para outro caso, ou a
alteração desses processos ficou sem caminho. Não se escolhe um dos lados. Pergunta ao
site.

### RN-09 — O número SEI é conferido no serviço externo de processos

Antes de gravar, a tela entrega ao **serviço externo de processos** uma requisição com o
número SEI informado, em nome do processo, e só segue quando a resposta diz que o
processo existe. Quando a resposta diz que ele não existe, a alteração é recusada com a
mensagem que o próprio serviço devolveu, o cursor volta à segunda caixa do número SEI,
nada é gravado e a tela se reabre.

[?] O protocolo da consulta — o destino, o hospedeiro, o ambiente e um código de acesso
fixo gravado no programa — não está no corpus nem no manual, e o texto que o serviço
devolve não é verificável por aqui. Também não se sabe o que significa a resposta vir
sem dado, caso em que a tela chama outra rotina comum antes de decidir. Pergunta ao
site.

### RN-10 — A alteração grava o número SEI nos documentos, no processo e nos empenhos

Passadas as conferências, a alteração grava o número SEI informado — e a marca de que
ele é do tipo SEI — nos **documentos do processo** (todos os documentos daquele
processo), no **registro do processo** e nos **empenhos do processo** (todos os
lançamentos daquele processo). Quando o processo ainda não tem registro próprio, esse
registro é criado na mesma operação. Nenhum outro dado desses cadastros é tocado.

Ao terminar, a tela confirma: o número SEI passa a aparecer sob o rótulo **SEI
atualizado:** e, na abertura seguinte, a tela avisa **\*\* SEI atualizado \*\***.

### RN-11 — Cada registro alterado deixa rastro na auditoria

Para **cada** documento do processo alcançado pela alteração, a tela grava um registro
na **auditoria**, com o cadastro de origem, a operação de alteração, o número do
processo, o conteúdo **anterior** e o **novo** — que diferem no número SEI — e o
contexto da sessão: matrícula, estação, tipo de órgão, CRE, ano e mês, data e hora e o
número da transação. O registro do processo, alterado ou criado, também é levado à
auditoria.

[?] O trecho que leva a **criação** do registro do processo à auditoria está sob uma
condição de estado da operação anterior; se essa condição não se verificar, a criação
fica sem rastro. O acervo lido não permite decidir se ela sempre se verifica. Pergunta
ao site.

### RN-12 — A consulta exige o processo registrado

Consultando, a tela procura o processo pelos documentos dele. Não achando, a recusa é
**\* Processo nao cadastrado \***, com o cursor na segunda caixa do número do processo,
e a tela esquece o processo que estava em uso. O processo é dado por cadastrado quando
existe **pelo menos um** documento dele.

### RN-13 — A consulta mostra o andamento do processo

Achado o processo, a tela lê os lançamentos dele nos empenhos e, conforme a situação
registrada, avisa **\* Processo pre-liquidado \***, **\* Processo liquidado \*** ou
**\* Processo pago \*** — e a consulta termina aí, com o cursor de volta ao número do
processo e o processo esquecido.

[?] A recusa só apresenta mensagem para essas três situações: qualquer outra situação
registrada no lançamento encerra a consulta **em silêncio**, sem mensagem nenhuma. O
acervo lido não lista os valores possíveis da situação. Pergunta ao site.

[?] A leitura que procura o lançamento posiciona dois campos que fazem parte da chave do
cadastro — o empenho e o ano de referência — com zero. Os sinalizadores de posicionamento
da leitura são dialeto do banco e não estão explicados no corpus: se o zero impedir o
casamento, o andamento não é encontrado e a gravação nos empenhos também não acontece.
Pergunta ao site.

### RN-14 — Processo em integração com o SIAFIC é recusado

Não achando o processo nos empenhos, a tela varre a relação de processos em
**integração com o SIAFIC**; achando o processo ali, a recusa é
**\* Processo na integracao com SIAFIC \***, com o cursor de volta ao número do
processo, e a tela esquece o processo que estava em uso.

### RN-15 — O servidor só alcança processos do seu grupo regional

Quando o vínculo da sessão tem CRE, o processo — cuja CRE vem dos documentos dele —
precisa pertencer a essa mesma CRE; sendo de outra, a recusa é
**\* Usuario sem acesso ao grupo deste processo \***, com o cursor na segunda caixa do
número do processo, e nada é consultado. Sem CRE na sessão, essa conferência não é
feita.

[?] A conferência de grupo só é alcançada quando o processo não está nos empenhos nem na
relação de integração com o SIAFIC: nesses dois casos a consulta termina antes, sem a
conferência. Se a intenção era conferir sempre, o caminho não confere. Pergunta ao site.

### RN-16 — A consulta não grava nada

A consulta termina antes da etapa de gravação: nenhum documento, registro de processo ou
empenho é incluído, alterado ou excluído, e nenhum registro de auditoria é criado. O que
ela deixa é só o processo e o número SEI que ficam em uso — e, nas recusas, nem isso.

### RN-17 — A tela confere o acesso antes de operar

Antes de mostrar os dados, a tela passa pelas conferências de acesso: ela tem de estar
registrada no **cadastro de telas** — senão **\* Tela nao disponivel \***; o **código de
acesso** da sessão tem de alcançar esta tela — senão **\* Acesso negado para esta
matricula \***; e o servidor tem de estar na **estação** em que a sessão foi aberta — em
outra, o acesso é encerrado. Na confirmação a tela confere ainda a rota — tela fora do
registro é recusada com **\* Tela nao cadastrada \*** e operação não prevista para a
tela com **\* Operacao nao disponivel \*** — e a permissão da operação no perfil: sem a
alteração liberada, a recusa é **\* Acesso negado para esta operacao \***, nada é gravado
e a sessão volta ao menu principal. A consulta **não** é conferida por essa permissão.

[?] O perfil da tela guarda quatro permissões — inclusão, alteração, exclusão e consulta
—, mas a conferência só olha as três primeiras. Quem tem a tela autorizada consulta sem
a permissão de consulta. Se a intenção era exigir a permissão de consulta por tela, o
caminho não a exige. Pergunta ao site.

### RN-18 — As recusas interrompem a tela antes de qualquer gravação

Cada recusa acima é apresentada com a mensagem e o cursor de volta ao campo culpado, e o
processamento da tela termina ali: nada é gravado. Só depois de passar por todas as
conferências a tela entra na etapa de gravação.

[?] A interrupção depois da recusa não se prova só com o programa da tela: quem marca a
operação como falha é a rotina global de mensagem, que não faz parte do acervo lido, e
**apenas** a recusa do serviço externo marca a falha no próprio programa. Se aquela
rotina não marcar o erro nas demais recusas, uma alteração recusada ainda poderia chegar
à etapa de gravação — que tem uma guarda própria (o número SEI anterior em uso), mas ela
só barra os casos em que a sessão ainda não tem número SEI nenhum. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Registrar e consultar o número SEI do processo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão e a CRE do meu vínculo
    E tenho acesso à tela N033T

  Cenário: Abertura da tela
    Quando abro a tela N033T pela opção do menu, sem informar operação
    Então ela abre em consulta
    E a primeira caixa do número do processo vem preenchida com o código de
      secretaria do meu tipo de órgão
    E a caixa de quatro dígitos do número SEI vem preenchida com o ano do sistema
    E vejo a descrição do tipo de órgão e a data do sistema
    E nada é gravado

  Cenário: O processo é informado em quatro caixas
    Dado que estou na tela N033T
    Quando o processo é apresentado
    Então vejo quatro caixas — duas de 2 dígitos, uma de 6 e uma de 4 — que formam
      um número de catorze dígitos

  Cenário: Número do processo com a segunda caixa em branco
    Dado que preencho a primeira caixa do processo com dois dígitos
    E deixo a segunda caixa em branco
    Quando a tela monta o número do processo
    Então esses dois dígitos passam a valer como a segunda dupla do número
    E as duas primeiras posições do número ficam zeradas

  Cenário: A tela retoma o processo e o número SEI do uso anterior
    Dado que consultei um processo nesta sessão
    Quando abro a tela N033T de novo
    Então o processo e o número SEI já aparecem nas caixas

  Cenário: Caixa de número que não é número
    Dado que estou na tela N033T
    Quando digito algo que não é número em uma das caixas de número
    Então a tela recusa a caixa antes de procurar no cadastro
    E o cursor volta ao campo recusado
    E nada é gravado

  Cenário: Operação diferente de alteração e de consulta
    Dado que estou na tela N033T
    Quando informo uma operação que não é a de alteração nem a de consulta
    Então vejo "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo da operação
    E nada é lido nem gravado

  Cenário: Registro do número SEI de um processo
    Dado que consultei o processo
    E informo a operação de alteração com o número SEI que o processo tem
    Quando confirmo a alteração
    Então o número SEI fica gravado nos documentos do processo, no registro do
      processo e nos empenhos dele
    E, se o processo ainda não tinha registro próprio, ele passa a ter
    E o número SEI aparece sob o rótulo "SEI atualizado:"
    E nenhum outro dado desses cadastros é alterado

  Cenário: O aviso da alteração
    Dado que alterei o número SEI de um processo
    Quando abro a tela N033T de novo
    Então vejo o aviso "** SEI atualizado **"

  Cenário: Alteração de processo que não foi consultado antes
    Dado que informo a operação de alteração
    E o processo informado não é o que a consulta deixou em uso
    Quando confirmo a alteração
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: Alteração sem a segunda caixa do número SEI
    Dado que consultei o processo
    E informo a operação de alteração
    E deixo a segunda caixa do número SEI em branco
    Quando confirmo a alteração
    Então vejo "* Informe o SEI *"
    E o cursor volta à segunda caixa do número SEI
    E nada é gravado

  Cenário: Número SEI que já identifica outro documento
    Dado que consultei o processo
    E informo a operação de alteração
    E o número SEI informado já está registrado em um documento de qualquer processo
    Quando confirmo a alteração
    Então vejo "<- SEI ja cadastrado *"
    E o cursor volta à segunda caixa do número SEI
    E nada é gravado

  Cenário: Número SEI reconhecido pelo serviço externo de processos
    Dado que consultei o processo e informo um número SEI novo
    Quando confirmo a alteração
    E o serviço externo de processos responde que aquele processo existe
    Então a alteração é gravada

  Cenário: Número SEI que o serviço externo não reconhece
    Dado que consultei o processo e informo um número SEI novo
    Quando confirmo a alteração
    E o serviço externo de processos responde que aquele processo não existe
    Então vejo a mensagem que o serviço devolveu
    E o cursor volta à segunda caixa do número SEI
    E nada é gravado
    E a tela se reabre

  Cenário: Toda alteração deixa rastro na auditoria
    Dado que alterei o número SEI de um processo
    Quando a gravação termina
    Então existe um registro de auditoria para cada documento do processo alcançado
    E o registro traz o conteúdo anterior e o novo, que diferem no número SEI
    E traz a matrícula, a estação, o tipo de órgão, a CRE, o ano e o mês, a data e a hora

  Cenário: Consulta de um processo registrado
    Dado que existe pelo menos um documento para o número informado
    E que o processo não está nos empenhos nem na relação de integração com o SIAFIC
    Quando peço a consulta
    Então vejo o número SEI que o processo já tem
    E nada é gravado

  Cenário: Consulta de um processo não cadastrado
    Dado que o processo informado não tem nenhum documento
    Quando peço a consulta
    Então vejo "* Processo nao cadastrado *"
    E o cursor volta à segunda caixa do número do processo
    E a tela esquece o processo que estava em uso

  Esquema do Cenário: Consulta de processo com andamento registrado
    Dado que o processo informado tem lançamento nos empenhos com a situação <situação>
    Quando peço a consulta
    Então vejo "<mensagem>"
    E o cursor volta ao número do processo
    E a tela esquece o processo que estava em uso

    Exemplos:
      | situação      | mensagem                     |
      | pré-liquidado | * Processo pre-liquidado *   |
      | liquidado     | * Processo liquidado *       |
      | pago          | * Processo pago *            |

  Cenário: Processo na relação de integração com o SIAFIC
    Dado que o processo informado está na relação de integração com o SIAFIC
    Quando peço a consulta
    Então vejo "* Processo na integracao com SIAFIC *"
    E o cursor volta ao número do processo
    E a tela esquece o processo que estava em uso

  Cenário: Processo de outro grupo regional
    Dado que a minha sessão carrega uma CRE
    E o processo informado pertence a outra CRE
    Quando peço a consulta
    Então vejo "* Usuario sem acesso ao grupo deste processo *"
    E o cursor volta à segunda caixa do número do processo
    E nada é consultado

  Cenário: A consulta não grava nada
    Dado que consultei um processo
    Quando a consulta termina
    Então nenhum documento, registro de processo ou empenho é incluído, alterado ou
      excluído
    E nenhum registro de auditoria é criado
    E o que fica é só o processo e o número SEI em uso

  Cenário: Tela não cadastrada
    Dado que a tela N033T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Recusa da rota
    Dado que a tela N033T está fora do registro da rota, ou a operação não é
      prevista para ela
    Quando confirmo a operação
    Então vejo "* Tela nao cadastrada *" ou "* Operacao nao disponivel *"
    E nada é consultado nem gravado

  Cenário: Sem autorização para a tela
    Dado que o código de acesso da minha matrícula não tem a tela N033T autorizada
    Quando tento abrir a tela
    Então vejo "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Sessão aberta em outra estação
    Dado que a minha sessão foi aberta em outra estação
    Quando tento operar a tela N033T
    Então o meu acesso é encerrado
    E nada é consultado nem gravado

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não dá o direito de alteração nesta tela
    Quando peço a alteração
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: As recusas interrompem a tela antes de qualquer gravação
    Dado que informei uma alteração que a tela recusa
    Quando vejo a mensagem da recusa
    Então o processamento termina ali
    E nada é gravado
```
