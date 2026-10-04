# US — C942T — Cópia dos cadastros do cardápio para a estimativa de um novo período

## Estória

Como **servidor de CRE**, quero **copiar os cadastros do cardápio de um período já
fechado para a estimativa de um período novo**, para que **a estimativa do período novo
já nasça montada a partir do que estava valendo, sem redigitar cadastro por cadastro**.

A estimativa é o planejamento de um período: o que cada segmento e cada refeição vão
consumir, mês a mês, e as médias por segmento. O cardápio é o que passou a valer de fato.
Montar a estimativa de um período novo sem esta cópia é refazer à mão, cadastro por
cadastro, um conjunto que já existe — e quem digita de novo erra. Esta tela é a que dispara
a cópia; e ela não copia na hora: registra o pedido e o entrega ao processamento que roda
fora da transação.

## Contexto

Jornada S000M → C000M → C800M → C900M → C942T.

Ator: servidor de CRE — informa o período do cardápio, que é a origem da cópia, e o período
novo da estimativa, que é o destino, e dispara a cópia.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — a opção 9 do
`C000M`, a opção 9 do `C800M` e a opção 7 do `C900M` — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio. As três telas do caminho são menus e não gravam nada: só encaminham. Esta tela não
encadeia em outra tela: ela reabre a si mesma e entrega o trabalho ao processamento.

As regras abaixo são só as da tela desta jornada. Cada dúvida fica ao fim da regra a que
pertence; o lastro de tudo o que aqui se afirma está no anexo de evidências.

## Regras de negócio

### RN-01 — A tela não tem consulta: a opção de manutenção é sempre alteração

Esta tela só serve para copiar: não há modo de consulta. A cada apresentação, ela mesma
repõe a opção de manutenção em **alteração**. Quando a resposta do terminal chega, antes de
ler qualquer um dos cadastros dos dois períodos, a tela exige alteração: qualquer outra
opção é recusada com **\* Opcao nao disponivel. Use ALT \***, com o cursor no campo da
opção, e a transação termina ali — nada é lido e nada é copiado. O modo não vem de quem
chamou a tela: quem a abre pelo menu não escolhe consulta nem inclusão.

[?] A mensagem manda usar **ALT**, mas a conferência não aceita uma "opção ALT": ela exige
a opção de alteração. Ou a mensagem está desalinhada da conferência, ou o que o terminal
envia é traduzido antes de chegar à tela. Pergunta ao site.

### RN-02 — Os dois períodos são informados em doze campos numéricos

A tela pede dois períodos, cada um com data de início e data limite, e cada data em dia,
mês e ano: **doze campos** — o período do cardápio, origem da cópia, e o período novo da
estimativa, destino. O dia e o mês têm dois dígitos e o ano tem quatro. O que estiver em
branco vale zero; o que não for número é recusado no próprio campo, antes de qualquer
consulta aos cadastros.

[?] A tela posiciona o cursor em nove dos doze campos: os três campos do início do período
do cardápio não têm posição definida — a recusa é acusada, mas o cursor não vai até o campo
errado. Pergunta ao site.

[?] As duas datas do período do cardápio não passam pela conferência de calendário que as
datas do período novo passam (RN-06): a data limite do cardápio só precisa achar um período
cadastrado, e a data de início, quando informada, segue como foi digitada. O acervo não diz
se é omissão. Pergunta ao site.

### RN-03 — O período do cardápio tem de estar cadastrado, e a procura é pela data limite

Com o tipo de órgão do servidor, a tela percorre as coordenações regionais escolares
cadastradas para esse tipo e, em cada uma, procura o período do cardápio cuja data limite
seja a informada. Não achando em nenhuma, a cópia não é aceita: **\* Salva nao cadastrada
\***, com o cursor na data limite do período do cardápio, e a transação para ali — nada é
pedido e nada é copiado.

[?] A recusa fala em "salva nao cadastrada", e "salva" não é o nome que o resto do acervo
dá a esse período: os rótulos que a própria tela mostra para as datas dele — o início e o
limite — são os de cardápio. Ou "salva" é o nome de negócio do cadastro do período, ou é de
uma versão dele, ou a mensagem perdeu o sentido. Pergunta ao site.

[?] Nenhum programa deste acervo grava o cadastro que esta conferência procura — a conta
está no fim do anexo. Ou ele é alimentado por processo de fora do acervo, ou esta
conferência nunca passa e a cópia nunca chega a ser pedida. Pergunta ao site.

[?] A procura passa por todas as coordenações do tipo de órgão: a primeira que tiver o
período satisfaz a conferência, mas quem vai para a auditoria é a coordenação da sessão —
não a que foi achada —, e o pedido segue sem coordenação. Se um tipo de órgão tiver mais de
uma coordenação, o período conferido pode não ser o da coordenação do servidor. Pergunta ao
site.

### RN-04 — A data de início do período do cardápio em branco é completada pelo cadastro

O servidor pode informar só a data limite do período do cardápio: achado o período, se o
ano do início veio em branco, a tela o preenche com o dia, o mês e o ano do início daquele
mesmo período cadastrado.

### RN-05 — O período novo da estimativa não pode já estar registrado

Antes de pedir qualquer coisa, a tela procura, para o tipo de órgão do servidor e as
coordenações dele, um período da estimativa já registrado cuja data limite seja a informada
para o período novo. Havendo, recusa com **\* Estimativa ja cadastrada nesta data \***, com
o cursor na data limite do período novo, e nada é copiado.

[?] A leitura que faz essa procura vem do gerador com sinalizadores de chave que não
correspondem um a um às partes da chave, e a semântica deles não está no acervo: não se
conclui se a procura exige a data limite inteira ou só parte dela (o tipo de órgão, a
coordenação e o ano). Se fixar menos do que a data, a recusa dispara para qualquer período
da coordenação e a recusa por sobreposição (RN-08) fica sem alcance. Pergunta ao site.

### RN-06 — As datas do período novo têm de ser datas de calendário

As duas datas do período novo são conferidas como datas: dia e mês que não existem, ou ano
fora da faixa admitida — de 1994 a 2099 —, são recusados com **\* Data inicial da
estimativa invalida \***, com o cursor na data de início, ou **\* Data final da estimativa
invalida \***, com o cursor na data limite.

### RN-07 — A data de início do período novo não pode ser maior que a data limite

Se a data de início do período novo for maior que a data limite dele, a cópia é recusada com
**\* Data inicial maior que data final \***, com o cursor na data de início.

### RN-08 — O período novo não pode se sobrepor a um período da estimativa já registrado

Ainda antes de perguntar, a tela confere a sobreposição: procura, em cada coordenação do
tipo de órgão, um período da estimativa cuja data limite seja a data de **início**
informada e, achando, compara o intervalo desse período com o intervalo informado; havendo
sobreposição, recusa com **\* <- Estimativa ja cadastrada neste intervalo \***, com o cursor
na data de início.

[?] A tela faz essa conferência de sobreposição duas vezes: uma procurando pela data de
início e a outra pela data limite. A segunda repete exatamente a procura que a recusa por
data já cadastrada (RN-05) já fez — e, se o período existisse, a transação já teria parado
antes. A recusa por sobreposição, por esse caminho, nunca aparece; só a procura pela data de
início pode produzi-la. Ou a repetição é inofensiva, ou uma das duas conferências foi
trocada. Pergunta ao site.

### RN-09 — A cópia só segue com a confirmação S

Passadas as conferências, a tela guarda os doze campos informados, pede **\* Confirma copia
dos cadastros <S/N> ? \*** e se reapresenta. Só a resposta **S** leva adiante. Resposta
diferente de S desfaz a confirmação e nada é copiado. Trocar a data limite do período do
cardápio, ou qualquer das datas do período novo, entre a pergunta e a resposta, também
desfaz a confirmação: o que a tela guardou na pergunta é o que volta para ela e o que vale.

[?] A conferência entre a pergunta e a resposta não inclui os três campos do início do
período do cardápio: trocar só essa data não desfaz a confirmação, e o valor guardado — o
da pergunta — é o que volta para a tela. Pergunta ao site.

### RN-10 — Só um pedido desta cópia por vez, em todo o sistema

Na resposta da confirmação, antes de registrar o pedido, a tela lê a fila de pedidos pelo
código desta operação, **sem separar por órgão**: achando qualquer pedido desta cópia em
andamento, recusa com **\* Relatorio em processamento. Aguarde. \***, com o cursor no campo
da resposta, e desfaz a confirmação — o servidor precisa informar os dois períodos de novo.
O pedido sai da fila quando o processamento que copia termina.

[?] A conferência da fila não é feita quando a tela pergunta, e sim quando recebe a
resposta: a pergunta é apresentada mesmo havendo um pedido em andamento, e a recusa só vem
depois de o servidor responder S.

### RN-11 — A cópia não acontece na tela

Dos sete cadastros que a tela enxerga, os dois únicos que a transação grava são a
**auditoria** e o **pedido de processamento**. As rotinas que gravariam, apagariam ou
travaram o período do cardápio e o período da estimativa estão todas declaradas e
**nenhuma delas é executada**: os dois períodos são apenas lidos. Quem copia é o
processamento da RN-14.

### RN-12 — Toda confirmação deixa rastro na auditoria

Confirmada a cópia, fica um registro na trilha de auditoria com o tipo de órgão, os dois
períodos informados (as doze datas) como valor anterior, o valor posterior em branco, a
coordenação regional escolar da sessão, a matrícula, a estação, a data e a hora, e o número
do processo — montado com o tipo de órgão e a data limite do período novo. O cadastro que
originou a operação é a própria tela e a operação fica registrada como **inclusão**.

### RN-13 — A tela registra o pedido e o entrega ao processamento

O pedido recebe o número seguinte ao do último pedido da fila, o tipo de órgão, a matrícula,
a estação, o dia, o mês e o ano, e o código desta operação. A tela monta ainda a área de
parâmetros que acompanha o pedido, com o código do relatório, a estação, a matrícula, o
correio eletrônico do funcionário e o bloco do tipo de órgão com as doze datas, e o entrega
ao processamento fora da transação — o programa que efetivamente copia. A tela então se
reapresenta com **\* Cadastro sendo atualizado \***: nada foi copiado na transação e o
servidor não vê o resultado.

[?] A entrega ao processamento só acontece quando o ambiente é o produto LINC; fora dele o
pedido fica na fila sem ser executado, e o acervo não diz o que faria com ele. Pergunta ao
site.

### RN-14 — O processamento copia os cadastros do cardápio para a estimativa do período novo

O processamento enfileirado lê os parâmetros do pedido e trabalha em duas varreduras. Na
primeira, percorre os cardápios do período de origem: para cada um, se já existe o cardápio
correspondente no período novo, salta; senão copia a composição do cardápio, as referências
e o próprio cardápio, todos carimbados com as datas do período novo. Na segunda, percorre as
coordenações do tipo de órgão e copia, por coordenação, o cardápio de cada dia da semana, as
quantidades mês a mês e as médias por segmento, também carimbados com as datas do período
novo. Ao terminar, apaga os pedidos desta cópia e libera a fila.

### RN-15 — Falha de banco interrompe a transação

Todo acesso ao banco é conferido: o erro de leitura e o de gravação são despachados pela
rotina de comunicação, e a transação para ali, sem completar o resto — a entrega ao
processamento não chega a acontecer.

[?] A auditoria é gravada antes do pedido: se a gravação do pedido falhar, o acervo não diz
se a auditoria já gravada volta atrás. Pergunta ao site.

### RN-16 — A tela mostra a descrição do tipo de órgão e a data do sistema

Além dos dois períodos, a tela exibe a **descrição do tipo de órgão** do servidor e a **data
do sistema**, as duas vindas da sessão — não são digitadas, e ao receber a entrada a tela as
descarta. Exibe também a sua linha de mensagem.

[?] O código da próxima tela, que o registro carrega de quem chamou esta tela, é repassado à
rotina de rota antes das conferências; essa rotina não está nos fontes desta jornada, e não
se conclui se a tela de origem muda algum outro comportamento desta tela. Pergunta ao site.

### RN-17 — A tela não apresenta a recusa de destino inválido

A tela desliga o modo de distribuição automática imediatamente antes das duas únicas
gravações que faz. O ramo que produziria a recusa por **destino inválido** depende desse
modo ligado; por esta tela, portanto, ele não é alcançado.

## Cenários BDD

```gherkin
Funcionalidade: Cópia dos cadastros do cardápio para a estimativa de um novo período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão e a coordenação regional escolar
    E tenho acesso à tela C942T

  Cenário: RN-01 — a tela não tem consulta
    Dado que estou na tela C942T
    Quando a opção de manutenção chega diferente de alteração
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor fica no campo da opção
    E nada é lido e nada é copiado

  Cenário: RN-02 — letra em um campo de data
    Quando preencho com uma letra o dia, o mês ou o ano de uma das quatro datas
    Então o campo é recusado antes de qualquer consulta
    E nada é copiado

  Cenário: RN-03, RN-04 e RN-16 — informar um período do cardápio cadastrado
    Dado que existe um período do cardápio cadastrado com a data limite que vou informar
    Quando informo a data limite do cardápio, deixando o ano do início em branco
    Então a tela mostra a descrição do meu tipo de órgão e a data do sistema
    E completa o início do período do cardápio com o do período cadastrado

  Cenário: RN-16 — abrir a tela não grava nada
    Dado que abro a tela C942T
    Então vejo a descrição do meu tipo de órgão e a data do sistema
    E nenhum cadastro é gravado

  Cenário: RN-03 — período do cardápio não cadastrado
    Quando informo uma data limite de cardápio que não corresponde a nenhum período cadastrado para o meu tipo de órgão
    Então vejo "* Salva nao cadastrada *"
    E o cursor fica na data limite do período do cardápio
    E nada é pedido e nada é copiado

  Cenário: RN-05 — período novo já registrado
    Dado que o período novo que vou informar já está registrado na estimativa
    Quando informo os dois períodos
    Então vejo "* Estimativa ja cadastrada nesta data *"
    E o cursor fica na data limite do período novo
    E nada é pedido e nada é copiado

  Cenário: RN-06 — data de início do período novo inválida
    Quando informo uma data de início do período novo que não existe no calendário
    Então vejo "* Data inicial da estimativa invalida *"
    E o cursor fica na data de início do período novo
    E nada é copiado

  Cenário: RN-06 — data limite do período novo fora da faixa
    Quando informo a data limite do período novo com o ano fora de 1994 a 2099
    Então vejo "* Data final da estimativa invalida *"
    E o cursor fica na data limite do período novo
    E nada é copiado

  Cenário: RN-07 — início do período novo maior que o limite
    Quando informo a data de início do período novo maior que a data limite dele
    Então vejo "* Data inicial maior que data final *"
    E o cursor fica na data de início do período novo
    E nada é copiado

  Cenário: RN-08 — período novo que se sobrepõe a um período registrado
    Dado que existe um período da estimativa registrado cuja data limite é a data de início que vou informar
    Quando informo os dois períodos
    Então vejo "* <- Estimativa ja cadastrada neste intervalo *"
    E o cursor fica na data de início do período novo
    E nada é copiado

  Cenário: RN-09 — a pergunta de confirmação
    Dado que os dois períodos informados passam pelas conferências
    Quando confirmo os períodos informados
    Então vejo "* Confirma copia dos cadastros <S/N> ? *"
    E nada foi copiado nem pedido ainda

  Cenário: RN-09 — resposta diferente de S
    Dado que estou vendo a pergunta de confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a confirmação é desfeita
    E nada é pedido e nada é copiado

  Cenário: RN-09 — troca das datas entre a pergunta e a resposta
    Dado que estou vendo a pergunta de confirmação
    Quando troco a data limite do cardápio ou uma data do período novo e respondo S
    Então a confirmação é desfeita
    E a tela volta a pedir os dois períodos
    E nada é copiado

  Cenário: RN-10 — já existe um pedido desta cópia em andamento
    Dado que existe um pedido desta cópia em andamento, de qualquer órgão
    Quando respondo S à pergunta de confirmação
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E a confirmação é desfeita
    E nada é copiado

  Cenário: RN-11, RN-12 e RN-13 — confirmar a cópia
    Dado que os dois períodos passam pelas conferências e não há pedido em andamento
    Quando respondo S à pergunta de confirmação
    Então o sistema grava o registro na trilha de auditoria
    E registra o pedido de processamento com os dois períodos, a minha matrícula, a estação e a data
    E entrega o pedido ao processamento que roda fora da transação
    E vejo "* Cadastro sendo atualizado *"
    E nenhum cadastro do cardápio ou da estimativa é gravado nesta transação

  Cenário: RN-14 — o processamento copia os cadastros do cardápio
    Dado que o pedido foi criado para um tipo de órgão e dois períodos
    Quando o processamento assume o pedido
    Então cada cardápio do período de origem é copiado para o período novo, com a composição, as referências e o próprio cardápio
    E cada coordenação do tipo de órgão é percorrida, copiando o cardápio de cada dia da semana, as quantidades mês a mês e as médias por segmento
    E o cardápio que já existe no período novo é saltado
    E os pedidos desta cópia são apagados ao fim, liberando a fila

  Cenário: RN-15 — falha de banco durante a confirmação
    Dado que a gravação falha no banco
    Quando respondo S à pergunta de confirmação
    Então a transação é interrompida com a mensagem de erro do sistema
    E a entrega ao processamento não acontece

  Cenário: RN-17 — a recusa de destino inválido não é apresentada
    Dado que confirmei uma cópia
    Quando as duas gravações são preparadas
    Então a tela desliga o modo de distribuição automática
    E a recusa de destino inválido não é apresentada
```
