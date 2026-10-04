# US — M049T — Pedir a geração do mapa do mês de referência da coordenadoria

## Estória

Como **servidor de CRE**, quero **pedir a geração do mapa do mês de referência das
unidades da minha coordenadoria, informando o período, a justificativa de cada tipo de
dia e a impressora**, para que **o mapa daquelas unidades já saia com os dias úteis, os
sábados, os domingos, os feriados e os recessos preenchidos de uma vez, sem que cada
unidade tenha de lançar o mês dia a dia**.

O mapa é o registro diário da unidade, e é por ele que a coordenação regional acompanha o
que já foi lançado e o que falta. Pedir o mapa de um mês é dizer ao sistema, de uma vez,
o que vale em cada tipo de dia do período — e é esse pedido que dispara o processamento
que preenche o mapa das unidades da coordenadoria. Como o pedido decide o mês inteiro
daquelas unidades, o sistema só o registra depois de mostrar o que entendeu e ouvir a
confirmação de quem pediu; e, enquanto houver um pedido de mapa da mesma coordenadoria que
ainda não terminou, recusa um segundo, para não processar o mesmo mês duas vezes.

## Contexto

Jornada S000M → M000M → M049T.

Ator: servidor de CRE — pede, para as unidades da sua coordenadoria, a geração do mapa do
mês de referência, informando o período das justificativas, a justificativa de cada tipo
de dia, a resposta sobre o perfil do mês anterior e a impressora.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O M000M é um menu e **não grava nada**: apenas encaminha para a M049T, sem passar modo nem
registro. O contexto que a M049T usa — a matrícula, o acesso, o tipo de órgão, a
coordenadoria e a estação do servidor — é o que a entrada deixou na sessão. Nada no fonte
desta tela compara a tela de origem com um código de tela: o comportamento da M049T **não
muda conforme quem a chamou**. A jornada termina nesta tela: ela não encaminha a outra, e
a única tela que ela alcança é ela mesma, ao se repetir para pedir a confirmação.

As regras abaixo são só as da tela desta jornada. Nenhuma regra da entrada foi repetida
aqui; o que a leitura da entrada revelou sobre esta tela está no anexo de evidências.

---

## Regras de negócio

### RN-01 — A tela não mantém cadastro: ela pede um processamento, e o que grava é o pedido

A M049T não é tela de consulta nem de manutenção do mapa. O que ela faz é **pedir** o
processamento do mapa: registra o pedido, dispara a execução e avisa. Para os sete
cadastros que ela enxerga, o programa traz escritas as rotinas de gravação e de exclusão,
mas só três gravações chegam a ser executadas — o **pedido**, no cadastro de requisições,
a **auditoria** do pedido e a **impressora do servidor**, que é criada ou alterada. Nenhuma
exclusão é executada, e o próprio mapa não é tocado por esta tela: quem preenche o mapa do
mês é o processamento que ela dispara.

### RN-02 — A tela só trabalha na inclusão

A opção de manutenção desta tela aceita um valor só, o de **inclusão**. Qualquer outro é
recusado com **\* Opcao nao disponivel. Use INC \***, com o cursor no campo da opção, e
nada é validado nem registrado. É a própria tela que repõe a inclusão ao abrir.

[?] A mensagem manda usar **INC**, mas o valor que a tela confere é o código de inclusão
do sistema. O que a máscara mostra nesse campo não está no material lido e, como a
abertura da tela repõe a opção sozinha, a recusa só é alcançada se o campo chegar com
outro valor. Pergunta ao site.

### RN-03 — A tela abre com o contexto já preenchido

Ao abrir, a tela traz preenchidos: a **coordenadoria do servidor**; os **códigos das
justificativas de sábado, domingo, feriado e recesso** que o tipo de órgão tem cadastrados,
cada um com a sua descrição; e a **impressora guardada para o servidor**. São digitados
apenas a justificativa dos dias úteis, o mês e o ano de referência, os dois dias do
período, a resposta sobre o perfil do mês anterior e a impressora, quando o servidor
quiser trocá-la.

### RN-04 — A coordenadoria é a do próprio servidor

A coordenadoria vem da sessão. Se a sessão não traz nenhuma, o campo abre em branco, o
cursor vai para ele e o pedido não anda sem que seja informada — **\* Informe o grupo \***.
Com coordenadoria na sessão, o campo volta sempre com ela, e uma coordenadoria diferente é
recusada com **\* Usuario sem acesso a outro grupo \***.

[?] A sessão sem coordenadoria é o único caso em que a tela aceita uma coordenadoria
digitada. O acervo não diz se isso é intenção — um servidor de âmbito geral — ou resíduo do
gerador. Pergunta ao site.

### RN-05 — O servidor precisa ter e-mail cadastrado

Antes de validar o pedido, o sistema lê o cadastro do funcionário pela matrícula da sessão.
Sem e-mail no cadastro, a recusa é **\* Usuario sem e-mail cadastrado \*** e nada é
registrado.

[?] A conferência compara o e-mail com zeros, e não com branco, ao contrário de outras
telas do mesmo sistema que usam a mesma mensagem. Com o e-mail em branco no cadastro, não
se sabe se a recusa aparece. Pergunta ao site.

### RN-06 — O servidor diz se o pedido é das creches ou das demais unidades

O campo de creche aceita **S** ou **N**; em branco, ou com outro valor, a recusa é
**\* Informe se creche ou nao com S ou N \***, com o cursor no campo. A resposta escolhe de
quais unidades da coordenadoria o processamento trata: as creches, com **S**, ou as
demais, com **N**.

### RN-07 — O mês e o ano de referência são obrigatórios, e o mês é de agosto de 2008 em diante

Os dois campos do mês de referência, ou nenhum: faltando um deles, a recusa é
**\* Informe Mes/Ano de referencia \***, com o cursor no mês. Informados os dois, o mês tem
de ser **agosto de 2008 ou posterior**; um mês anterior a esse é recusado com
**\* Mes/Ano de referencia invalido \***, também com o cursor no mês.

[?] A data que separa os meses aceitos dos recusados é uma constante da própria tela, fixa
em agosto de 2008, e não algo que venha de cadastro. É a mesma data que, nas telas de
consulta do mapa, separa as duas gerações de mapa; o que exatamente ela separa aqui não
está no corpus nem no manual. Pergunta ao site.

### RN-08 — O mês de referência tem de estar cadastrado na tabela de períodos do mapa

O mês e o ano informados têm de existir na **tabela de períodos do mapa**; não existindo, a
recusa é **\* Mes/Ano nao cadastr.na tab.de periodos do mapa \***, com o cursor no mês, e
nada é registrado. Existindo, a tela mostra o **início e o limite do período** daquele mês,
lidos dessa tabela.

[?] O período que a tabela traz é mostrado, mas não é conferido contra os dias informados
nem enviado ao processamento: o que segue no pedido é o mês de referência com os dois dias
digitados. Se a intenção era prender o período informado ao período da tabela, o caminho
não o prende. Pergunta ao site.

### RN-09 — O período das justificativas é informado só pelos dias

As duas datas do período pertencem ao mês de referência: o mês e o ano delas são repostos
com o mês e o ano informados, e o servidor digita apenas o **dia inicial** e o **dia
final**. Por isso os dois dias são conferidos como data do calendário daquele mês: um dia
que não existe no mês é recusado pela conferência de data, e não por uma conferência
própria.

### RN-10 — As datas do período: válidas, não futuras, e a final não anterior à inicial

Cada uma das duas datas tem de ser uma data válida do calendário, com o ano entre **1994** e
**2099**: fora disso, **\* Periodo inicial invalido \*** ou **\* Periodo final invalido \***,
com o cursor no dia correspondente. Nenhuma das duas pode estar no futuro — **\* Data
inicial maior que data atual \*** e **\* Data final maior que data atual \*** —, e a data
final não pode ser anterior à inicial: **\* Data final menor que data inicial \***.

### RN-11 — As cinco justificativas: cadastradas, e a dos dias úteis distinta das outras quatro

As cinco justificativas — dias úteis, sábado, domingo, feriado e recesso — são procuradas no
**cadastro de justificativas do tipo de órgão**; a que não estiver cadastrada é recusada com
**\* Justificativa nao cadastrada \***, com o cursor no campo dela. E a justificativa
informada para os **dias úteis** não pode ser a mesma de sábado, domingo, feriado ou
recesso: sendo, a recusa é **\* Justificativa invalida para dias uteis \***, com o cursor
nela.

### RN-12 — O servidor diz se o perfil do mês anterior deve ser repetido

A resposta é obrigatória e só aceita **S** ou **N**; em branco, ou com outro valor, a recusa
é **\* Inf.se repete perfil do mes ant. com S ou N \***, com o cursor no campo. A resposta
viaja no pedido.

[?] O que "perfil" significa nesta tela não é dela: é o processamento que decide de qual mês
vem o perfil da unidade conforme a resposta. O sentido do termo no negócio não está no
material lido. Pergunta ao site.

### RN-13 — A impressora é obrigatória, e a informada passa a ser a do servidor

A impressora não pode ficar em branco: sem ela o sistema recusa com
**\* Informe a impressora \***, devolve o cursor ao campo e não registra nada. Aceito o
pedido, a impressora informada é gravada como a **impressora do servidor** — é por isso que
ela volta preenchida na próxima abertura da tela.

### RN-14 — O pedido é confirmado antes de ser registrado, e a resposta vale para o que foi mostrado

Conferido tudo, a tela não registra: ela mostra
**\* Confirma justificativas no periodo <S/N> ? \*** e espera. É a resposta **S** que leva ao
registro. Se, ao responder, algum campo mostrado já não for o mesmo — a **impressora não
entra** nessa reconferência —, a resposta é descartada, o pedido é validado de novo e a
mesma pergunta volta. Qualquer resposta diferente de **S**, inclusive **N**, não registra
nada e a tela volta a perguntar.

[?] Responder **N** não cancela o pedido: a tela insiste e repete a pergunta. Se isso é o
desenho, ou se o ramo ficou sem caminho de saída, pergunta ao site — não há no fonte nenhum
rótulo de cancelamento.

[?] Apagar ou trocar a impressora entre a pergunta e a resposta não invalida a resposta: o
valor que entra no pedido é o que estiver na tela na hora do registro. Confirmar com o site
se é esse o desenho.

### RN-15 — Um pedido da mesma coordenadoria bloqueia o novo

Antes de registrar, o sistema procura no **cadastro de requisições** um pedido do **mesmo
relatório** e da **mesma coordenadoria**. Achando, recusa com
**\* Relatorio em processamento. Aguarde. \***, descarta a confirmação e não registra nada. O
pedido que esta tela cria é apagado quando o processamento termina — é o próprio
processamento que o remove — e, de todo modo, pela limpeza que a entrada faz nas requisições
vencidas.

[?] A procura é pela chave do pedido e **não** confere se ele ainda está pendente: qualquer
requisição daquela coordenadoria para aquele relatório barra, mesmo já processada. E, se o
processamento não chegar a rodar, o pedido fica e a tela recusa até a limpeza da entrada do
dia seguinte. Se é esse o desenho, pergunta ao site.

### RN-16 — O pedido registrado leva o mapa, quem pediu e o número seguinte ao último

Confirmada a resposta, o sistema grava o pedido no cadastro de requisições como
**inclusão**. O pedido leva:

- o **relatório do mapa**;
- a **coordenadoria** e o **tipo de órgão** da sessão;
- a **matrícula** de quem pediu e a **estação**;
- o **ano**, o **mês** e o **dia** do pedido, que são os do sistema;
- o **número da requisição**, que é o **seguinte** ao último já registrado.

Junto vai o **bloco de parâmetros do relatório**: o código do relatório, a impressora, **uma**
cópia, a estação, a matrícula, o **e-mail** de quem pediu e o registro do mapa —
coordenadoria, tipo de órgão, creche, o mês de referência com os dois dias informados, as
cinco justificativas e a resposta sobre o perfil.

[?] O cadastro de requisições marca a impressora como campo obrigatório, e o pedido é
gravado com a impressora **em branco** e com o estado de pendência em branco: a impressora
informada viaja dentro do bloco de parâmetros, e o estado não é preenchido por ninguém. Se o
obrigatório do cadastro barra essa gravação, não está no corpus lido. Pergunta ao site.

### RN-17 — O processamento é disparado, a tela avisa, e o pedido fica auditado

Registrado o pedido, o sistema submete a execução do processamento do mapa e a tela avisa
**\* Cadastro sendo atualizado \***. O estado de confirmação é descartado: um novo pedido
exige uma nova confirmação. O sistema grava também a **auditoria** do pedido, como inclusão,
com a coordenadoria no lugar do número de processo e o bloco de parâmetros como valor novo —
e sem valor anterior.

[?] O retorno da submissão da execução é guardado e não conferido: se a submissão falhar, o
operador vê a mesma mensagem de cadastro sendo atualizado. E, se a gravação do pedido
encontrar a chave já existente, o desfecho para o operador não está no material lido.
Pergunta ao site.

### RN-18 — Nada é registrado sem as conferências de tela, de estação, de rota e de permissão

Antes de validar, a tela confere o **cadastro de telas** e a sessão: se a estação da sessão
não for a registrada no cadastro do funcionário, o acesso é encerrado; e uma requisição
marcada como segunda página é recusada. Antes de registrar, confere a **rota** — a tela tem
de estar cadastrada e não excluída — e a **permissão**: o cadastro de acessos tem de liberar
a **inclusão** para esta tela. Se qualquer conferência não passar, a tela devolve o controle
sem validar e sem registrar nada, com uma destas mensagens:
**\* Tela nao disponivel \***, **\* Acesso negado para esta matricula \***,
**\* Acesso negado para esta operacao \***, **\* Acesso a pagina 2 negado \*** ou
**\* Tela nao cadastrada \***.

### RN-19 — Prefixo de tela preenchido desvia a transação

Se a transação chega com o campo de prefixo de tela preenchido, a conferência de rota desvia
a transação para a tela indicada ali e o processamento desta tela é abandonado: nada é
validado e nada é registrado.

[?] O que preenche esse campo não está no corpus lido: não se sabe quem manda prefixo de
tela para a M049T. Pergunta ao site.

### RN-20 — A recusa de destino inválido não é alcançada pela tela

A tela prevê a recusa de **destino inválido**, da distribuição automática entre destinos.
Para chegar lá, o campo de distribuição automática teria de estar preenchido, e a tela o
limpa imediatamente antes de preparar a gravação: por este caminho essa recusa não é
apresentada.

[?] A conferência de destino continua no caminho da gravação: se as chaves de origem e de
destino da transação forem diferentes, o pedido **não** é registrado e uma mensagem do
catálogo é apresentada no lugar. O que preenche essas chaves, e o que o operador vê nesse
caso, não está no corpus lido — e disso depende o pedido ser registrado ou não. Pergunta ao
site.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedir a geração do mapa do mês de referência da coordenadoria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a matrícula, o acesso, o tipo de órgão, a coordenadoria e a estação
    E tenho acesso à tela M049T
    E tenho permissão de inclusão nesta tela

  Cenário: O pedido é registrado e o processamento é disparado
    Dado que estou na tela M049T
    Quando informo o mês e o ano de referência, o dia inicial e o dia final, as cinco justificativas, a resposta sobre o perfil e a impressora, e respondo S à confirmação
    Então o pedido é gravado no cadastro de requisições como uma inclusão
    E o processamento do mapa é disparado
    E vejo "* Cadastro sendo atualizado *"

  Cenário: A tela não mantém o mapa: ela pede o processamento
    Dado que confirmei um pedido na tela M049T
    Quando o pedido é gravado
    Então o sistema grava o pedido, a auditoria e a minha impressora
    E nenhum registro do mapa é incluído, alterado ou excluído por esta tela
    E nenhuma exclusão de cadastro é executada

  Cenário: A tela abre com a coordenadoria, as justificativas dos tipos de dia e a impressora
    Dado que a minha sessão carrega a coordenadoria e o meu cadastro tem e-mail
    Quando abro a tela M049T
    Então a coordenadoria aparece preenchida com a da sessão
    E as justificativas de sábado, domingo, feriado e recesso aparecem com os códigos cadastrados para o meu tipo de órgão
    E a impressora aparece com a que está guardada para mim

  Cenário: Opção de manutenção diferente de inclusão é recusada
    Dado que estou na tela M049T
    Quando a tela chega com uma opção de manutenção diferente da inclusão
    Então vejo "* Opcao nao disponivel. Use INC *"
    E o cursor fica no campo da opção
    E nada é validado e nada é registrado

  Cenário: Sessão sem coordenadoria e campo em branco
    Dado que a minha sessão não carrega coordenadoria
    Quando tento pedir o mapa sem informar a coordenadoria
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Coordenadoria de outro grupo
    Dado que a minha sessão carrega uma coordenadoria
    Quando informo uma coordenadoria diferente da minha
    Então vejo "* Usuario sem acesso a outro grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: Sem e-mail cadastrado
    Dado que o meu cadastro de funcionário está sem e-mail
    Quando confirmo um pedido na tela M049T
    Então vejo "* Usuario sem e-mail cadastrado *"
    E nada é gravado

  Cenário: O campo de creche em branco
    Dado que estou na tela M049T
    Quando deixo o campo de creche em branco
    Então vejo "* Informe se creche ou nao com S ou N *"
    E o cursor fica no campo da creche
    E nada é gravado

  Cenário: Sem o mês ou sem o ano de referência
    Dado que estou na tela M049T
    Quando deixo o mês ou o ano de referência em branco
    Então vejo "* Informe Mes/Ano de referencia *"
    E o cursor fica no mês
    E nada é gravado

  Cenário: Mês de referência anterior a agosto de 2008
    Dado que estou na tela M049T
    Quando informo um mês de referência anterior a agosto de 2008
    Então vejo "* Mes/Ano de referencia invalido *"
    E o cursor fica no mês
    E nada é gravado

  Cenário: Mês de referência fora da tabela de períodos do mapa
    Dado que estou na tela M049T
    Quando informo um mês e um ano que a tabela de períodos do mapa não tem
    Então vejo "* Mes/Ano nao cadastr.na tab.de periodos do mapa *"
    E o cursor fica no mês
    E nada é gravado

  Cenário: O período da tabela é mostrado e os dias informados são os que valem
    Dado que informei um mês de referência que existe na tabela de períodos do mapa
    Quando a tela valida o mês
    Então ela mostra o início e o limite do período daquele mês
    E o período que segue no pedido é o mês de referência com os dois dias que eu digitei

  Cenário: Dia do período que não existe no mês
    Dado que estou na tela M049T
    Quando informo um dia que não existe no mês de referência
    Então vejo "* Periodo inicial invalido *" ou "* Periodo final invalido *"
    E o cursor fica no dia correspondente
    E nada é gravado

  Cenário: Data do período no futuro
    Dado que estou na tela M049T
    Quando informo um dia posterior à data de hoje
    Então vejo "* Data inicial maior que data atual *" ou "* Data final maior que data atual *"
    E o cursor fica no dia correspondente
    E nada é gravado

  Cenário: Data final anterior à inicial
    Dado que estou na tela M049T
    Quando informo um dia final anterior ao dia inicial
    Então vejo "* Data final menor que data inicial *"
    E o cursor fica no dia final
    E nada é gravado

  Cenário: Justificativa não cadastrada para o tipo de órgão
    Dado que estou na tela M049T
    Quando informo uma justificativa que o meu tipo de órgão não tem cadastrada
    Então vejo "* Justificativa nao cadastrada *"
    E o cursor fica no campo daquela justificativa
    E nada é gravado

  Cenário: Justificativa dos dias úteis igual à de outro tipo de dia
    Dado que estou na tela M049T
    Quando informo, para os dias úteis, a mesma justificativa de sábado, domingo, feriado ou recesso
    Então vejo "* Justificativa invalida para dias uteis *"
    E o cursor fica no campo da justificativa dos dias úteis
    E nada é gravado

  Cenário: Sem a resposta sobre o perfil do mês anterior
    Dado que estou na tela M049T
    Quando deixo em branco a resposta sobre repetir o perfil do mês anterior
    Então vejo "* Inf.se repete perfil do mes ant. com S ou N *"
    E o cursor fica nesse campo
    E nada é gravado

  Cenário: Sem impressora
    Dado que estou na tela M049T
    Quando deixo a impressora em branco
    Então vejo "* Informe a impressora *"
    E o cursor fica no campo da impressora
    E nada é gravado

  Cenário: A impressora informada passa a ser a do servidor
    Dado que confirmei um pedido na tela M049T com uma impressora diferente da minha
    Quando o pedido é gravado
    Então aquela impressora passa a ser a impressora guardada para mim
    E ela volta preenchida na próxima vez que eu abrir a tela

  Cenário: A tela pede confirmação antes de registrar
    Dado que informei o mês de referência, o período, as justificativas e a impressora
    Quando a validação termina
    Então vejo "* Confirma justificativas no periodo <S/N> ? *"
    E nada foi gravado ainda

  Cenário: A confirmação vale para o que foi mostrado
    Dado que a tela M049T pediu a confirmação de um período
    Quando troco o mês, o ano ou um dos dias e respondo
    Então a minha resposta é descartada
    E o sistema valida o que está na tela e pede a confirmação outra vez

  Cenário: Responder N não registra, e a tela volta a perguntar
    Dado que a tela M049T pediu a confirmação de um período
    Quando respondo N
    Então nada é gravado
    E vejo o mesmo pedido de confirmação outra vez

  Cenário: Um pedido da mesma coordenadoria bloqueia o novo
    Dado que já existe um pedido do mesmo relatório para a minha coordenadoria
    Quando confirmo um novo pedido na tela M049T
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E a confirmação é descartada
    E nada é gravado

  Cenário: O pedido leva o mapa, quem pediu e o número seguinte ao último
    Dado que confirmei um pedido na tela M049T
    Quando o pedido é gravado
    Então ele leva o relatório do mapa, a coordenadoria e o tipo de órgão da sessão
    E leva a matrícula de quem pediu, a estação e as datas do sistema
    E leva o bloco de parâmetros com a creche, o mês de referência, os dois dias, as cinco justificativas, a resposta sobre o perfil, a impressora, uma cópia e o e-mail de quem pediu
    E o número da requisição é o seguinte ao último registrado

  Cenário: A auditoria do pedido é gravada como inclusão
    Dado que confirmei um pedido na tela M049T
    Quando o pedido é gravado
    Então a auditoria do pedido é gravada como inclusão
    E a coordenadoria fica no lugar do número de processo
    E o bloco de parâmetros fica como valor novo, sem valor anterior

  Cenário: Depois do registro, o estado de confirmação é descartado
    Dado que confirmei um pedido na tela M049T
    Quando o pedido é gravado
    Então vejo "* Cadastro sendo atualizado *"
    E um novo pedido exige uma nova confirmação

  Cenário: Sem permissão de inclusão para esta tela
    Dado que o meu cadastro de acessos não libera a inclusão nesta tela
    Quando tento confirmar um pedido na tela M049T
    Então vejo "* Acesso negado para esta operacao *"
    E nada é validado e nada é registrado

  Cenário: Tela não disponível ou fora da rota
    Dado que a tela M049T não está no cadastro de telas, ou está excluída
    Quando ela é aberta
    Então vejo "* Tela nao disponivel *" ou "* Tela nao cadastrada *"
    E nada é validado e nada é registrado

  Cenário: Acesso negado para esta matrícula
    Dado que o meu cadastro não tem acesso a esta tela
    Quando ela é aberta
    Então vejo "* Acesso negado para esta matricula *"
    E nada é validado e nada é registrado

  Cenário: A sessão está em outra estação
    Dado que a estação da minha sessão não é a registrada no meu cadastro
    Quando a tela M049T é aberta
    Então o meu acesso é encerrado
    E nada é validado e nada é registrado

  Cenário: Requisição de segunda página é negada
    Dado que a minha requisição está marcada como página 2
    Quando a tela M049T é aberta
    Então vejo "* Acesso a pagina 2 negado *"
    E nada é validado e nada é registrado

  Cenário: Prefixo de tela preenchido desvia a transação
    Dado que a transação chega à M049T com o campo de prefixo de tela preenchido
    Quando a conferência de rota é feita
    Então a transação é desviada para a tela indicada no prefixo
    E o processamento desta tela é abandonado
    E nada é registrado

  Cenário: A recusa de destino inválido não é apresentada
    Dado que confirmei um pedido na tela M049T
    Quando a gravação é preparada
    Então a tela limpa o campo da distribuição automática
    E a recusa de destino inválido não aparece

  Cenário: Nada é registrado antes da confirmação
    Dado que estou na tela M049T
    Quando informo o mês de referência, o período, as justificativas e a impressora, mas não respondo S
    Então nenhuma requisição é criada
    E nenhum processamento é disparado
    E a minha impressora não é alterada
```
