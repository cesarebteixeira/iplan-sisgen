# US — M040C — Consultar a situação diária do mapa de um órgão filho da coordenadoria

## Estória

Como **servidor de CRE**, quero **consultar, a partir de uma data, a situação do
mapa de cada dia de um órgão filho da minha coordenadoria**, para que **eu veja de
uma vez quais dias já têm o mapa digitado, quais já foram fechados e quais ainda
faltam, sem abrir o mapa dia por dia**.

O mapa é o registro diário que a unidade preenche, e é por ele que a coordenação
regional acompanha o que já foi lançado e o que ficou para trás. Sem esta lista, a
conferência de um período teria só o acumulado, e achar o dia que faltou exigiria
abrir o mapa da unidade. A tela é de leitura: mostra os dias e a situação de cada
um, e não inclui, não altera e não exclui mapa nenhum.

## Contexto

Jornada S000M → M000M → M020M → M040C.
Ator: servidor de CRE — acompanha, para um órgão filho da sua coordenadoria e uma
data de partida, a situação do mapa de cada dia.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O `M000M` e o `M020M` são menus: não gravam nada, apenas encaminham, e a `M040C`
encerra a jornada — nenhum caminho desta jornada a encadeia para outra tela. A
`M020M` chega à `M040C` por transferência e **não deixa operação marcada**: o modo
de consulta é decisão da própria tela de destino. O que a tela usa da sessão — o
tipo de órgão, a coordenadoria e o órgão filho do vínculo do servidor — é o que a
entrada deixou.

---

## Regras de negócio

### RN-01 — A tela só consulta; qualquer outra operação é recusada

A tela abre em modo de consulta e, ao montar a lista, repõe esse modo, de sorte que
a operação volte a ser sempre a consulta. Se chegar outra operação, o sistema
recusa com **\* Operacao nao disponivel. Use CON \*** e devolve o cursor ao campo
da opção. A recusa vem depois das conferências de rota e de permissão da sessão e
**antes de ler qualquer cadastro**: nesse caminho o sistema não chega a ler órgão
nem mapa.

[?] A tela repõe a consulta sozinha, e o envio só recusa quando chega outra
operação. Se a máscara não oferece ao servidor o campo da operação, a recusa é um
trecho que nunca é alcançado. O texto da máscara não está no material lido.

[?] A mensagem manda usar **CON**, e o valor que a tela aceita como consulta é o
código de consulta do sistema. O que a máscara mostra nesse campo não está no
material lido.

[?] O que acontece depois da recusa. A expansão do programa descartou a instrução
que encerra a passagem — o descarte é da premissa de perfil do expansor, não do
acervo — e o programa que li segue adiante em vez de sair. Se o perfil de compilação
real mantém essa instrução, a recusa encerra como as outras telas do sistema.

### RN-02 — Sem o código do órgão filho a consulta não começa

A tela exige o código do órgão filho. Em branco, o sistema recusa com
**\* Informe o orgao \*** e devolve o cursor ao campo do órgão. A exigência só é
conferida para o servidor **cujo vínculo não traz órgão filho**: para quem tem um
órgão no vínculo, o campo em branco cai antes na recusa da RN-03.

### RN-03 — Quem tem órgão no vínculo só consulta esse órgão

Quando o vínculo do servidor traz um órgão filho, o código informado tem de ser o
dele. Sendo outro — inclusive em branco —, o sistema recusa com
**\* Usuario sem acesso a outro orgao \***, devolve o cursor ao campo do órgão e não
monta lista nenhuma. O alcance da consulta é o vínculo, não o que se digita.

[?] Para o servidor cujo vínculo **não** traz órgão, esta conferência não roda: ele
consulta qualquer órgão cadastrado. O acervo não diz se isso é intenção — servidor
de âmbito geral — ou resíduo do gerador. Pergunta ao site.

[?] O órgão informado igual ao do vínculo passa adiante sem ser conferido contra o
cadastro: as cinco recusas da RN-04 à RN-08 não valem para esse servidor, nem
quando o cadastro do órgão está incompleto, inativo ou em outra secretaria. Se a
intenção era conferir sempre o cadastro, o caminho não o confere.

### RN-04 — O órgão informado tem de estar cadastrado

O código informado tem de existir no cadastro de órgãos, e o registro não pode
estar marcado como excluído. Não existindo — ou existindo apenas excluído —, a tela
recusa com **\* Orgao nao cadastrado \***, devolve o cursor ao campo do órgão e não
monta lista nenhuma. O cadastro de órgãos tem **27 campos** e capacidade declarada
para **12.000** órgãos. A chave procurada pela tela é só o código do órgão.
Capacidade é o máximo esperado, parâmetro de dimensionamento — não o que está
cadastrado.

[?] O cadastro admite mais de um registro com o mesmo código de órgão, e a tela
julga pelo **primeiro** registro não excluído que a leitura devolver. Se o mesmo
código estiver em duas secretarias ou em duas coordenadorias, é o registro que vier
que decide a resposta. Qual deles é o certo é pergunta ao site.

[?] A leitura que pula o registro excluído é uma leitura importada da biblioteca de
execução, sem fonte no acervo. Se ela não avançar, o registro excluído devolve a
mesma resposta e o caminho não termina. Pergunta ao site.

### RN-05 — O órgão não pode estar cadastrado como inativo

O órgão informado tem de estar ativo no cadastro. Marcado como inativo, a tela
recusa com **\* Orgao cadastrado como inativo \***, devolve o cursor ao campo do
órgão e não monta lista nenhuma.

### RN-06 — O órgão tem de estar com os dados completos

O cadastro do órgão informado tem de ter preenchidos **seis** dados: o bairro, o
órgão pai, o nome, o endereço, a quantidade de matriculados e a quantidade de
pessoas. Faltando qualquer um deles, a tela recusa com
**\* Orgao cadastrado com dados incompletos \***, devolve o cursor ao campo do
órgão e não monta lista nenhuma.

### RN-07 — O órgão tem de ser da secretaria do servidor

O órgão informado tem de ser do mesmo tipo de órgão da sessão — a secretaria por
onde o servidor entrou. Sendo de outro, a tela recusa com
**\* Orgao nao pertence a esta secretaria \***, devolve o cursor ao campo do órgão
e não monta lista nenhuma.

### RN-08 — O órgão tem de ser da coordenadoria do servidor

O órgão informado tem de ser da coordenadoria do servidor. Sendo de outra, a tela
recusa com **\* Usuario sem acesso ao grupo deste orgao \***, devolve o cursor ao
campo do órgão e não monta lista nenhuma. O servidor **sem** coordenadoria na
sessão não passa por esta conferência: para ele, quem passa a definir a
coordenadoria em vigor é o cadastro do órgão consultado.

### RN-09 — A data informada é conferida antes de ler mapa nenhum

O dia, o mês e o ano do mapa passam pela edição numérica junto com o órgão e a
coordenadoria: o que não for número é recusado antes de qualquer conferência de
negócio. Informada a data, ela ainda tem de existir no calendário, com o ano entre
**1994** e **2099**: não existindo, a recusa é **\* Data invalida \*** e o cursor
volta ao campo do dia. A data em branco não é recusada: sem data, a tela escolhe
sozinha a data de partida (RN-11). Nenhuma leitura de mapa acontece antes desta
conferência.

[?] A coordenadoria digitada passa pela mesma edição, mas **não** tem desvio de
cursor: o que não for número é recusado sem que o cursor volte a campo nenhum, ao
contrário do órgão e dos três campos da data. Se há mensagem, ela não está nos
fontes lidos: a rotina de edição é importada e não tem fonte no acervo.

[?] Se a data em branco deveria ser recusada. A conferência de calendário só roda
quando o ano informado é maior que zero; em branco, a tela segue e escolhe sozinha a
data de partida (RN-11). Se a intenção era exigir a data, o caminho não a exige.

### RN-10 — A lista tem 12 linhas, uma por dia, e para na data do sistema

A lista é uma grade de **12 linhas**. Cada linha traz a **data do dia**, o **dia da
semana**, a **semana** a que o dia pertence e a **situação do mapa** daquele dia. A
primeira linha é a data de partida e cada linha seguinte é o dia imediatamente
posterior: a lista anda **um dia por linha**. A caminhada para quando o dia passa
da **data do sistema**: não havendo mais dia a mostrar, as linhas restantes ficam
em branco, e uma data de partida posterior a hoje não preenche linha nenhuma, sem
aviso — os campos do dia, do mês e do ano voltam em branco.

### RN-11 — Sem data informada, a lista começa no primeiro dia do mês do último mapa

Quando o servidor não informa a data, a tela procura o mapa do órgão: primeiro o do
**dia de hoje** e, não havendo, o **último mapa registrado** do órgão. Do mapa
encontrado ela aproveita o mês e o ano e adota o **dia 1** como data de partida. O
dia do mapa encontrado é descartado: quem volta à tela vê a lista começar no dia 1,
e não no dia do último mapa.

[?] Não há, no fonte, nenhum motivo para o dia do mapa encontrado virar dia 1. Se a
lista deveria começar no dia do último mapa — ou no dia de hoje —, o caminho não o
faz. Pergunta ao site.

### RN-12 — De agosto de 2008 em diante, a situação do dia vem do mapa daquele dia

Para mês e ano de **agosto de 2008** em diante, a situação de cada linha é a do
mapa registrado para aquela data: **ABERTO** quando o mapa existe e não está
marcado como fechado, **FECHADO** quando está marcado como fechado. A semana
mostrada na linha vem do próprio mapa. O mapa do dia guarda **12 campos** e a
capacidade declarada é de **20.000.000** registros — capacidade é dimensionamento,
não volume.

[?] A data que separa as duas formas de procurar o mapa é uma constante da própria
tela, fixa em agosto de 2008, e não algo que venha do cadastro. O que exatamente
ela separa — qual geração de mapa — não está no corpus nem no manual. Pergunta ao
site.

### RN-13 — Antes de agosto de 2008 a situação vem do mapa do período, e a creche tem mapa próprio

Para mês e ano **anteriores** a agosto de 2008, a situação de cada dia vem do
**mapa do período** daquele dia: a tela consulta o **calendário dos períodos** do
mês de referência e, quando o dia mostrado é anterior ao início do período do mês,
recua um mês — e um ano, quando o mês é janeiro. A **creche** tem mapa próprio: a
unidade cadastrada como creche consulta o mapa de creche, e as demais o mapa comum.
O mapa comum tem **64 campos** e capacidade para **3.000.000** registros; o mapa de
creche, **130 campos** e **300.000**; o calendário de períodos, **6 campos** e
**50.000**.

[?] O que a tela deve mostrar num dia que está dentro de um período mas não é o seu
primeiro dia. Como a procura usa o dia mostrado como início do período, esse dia
aparece sem mapa — "não digitado" (RN-14) — mesmo com o período digitado. Se o
desenho previa encontrar o período que contém o dia, o caminho não o encontra.

[?] O motivo do recuo de um mês. Quando o dia mostrado é anterior ao início do
período do mês, a tela recua um mês — e um ano, quando o mês vira janeiro — e relê o
calendário. O acervo não diz se é o período que atravessa a virada do mês ou outro
caso. Pergunta ao site.

[?] O indicador de creche e o caminho do mapa leem o mesmo atributo em sentidos
opostos: o indicador mostra **Nao** para tudo que não é a marca de creche, e o
caminho do mapa manda para o mapa de creche tudo que não é a marca de não-creche.
Um órgão com o atributo em branco — que é o valor inicial do cadastro — aparece
como "Nao" na lista e é consultado no mapa de creche. Os dois desfechos não podem
ser ambos pretendidos; o site precisa dizer qual vale.

### RN-14 — Sem mapa no dia, a linha diz que não foi digitado

Não havendo mapa para o dia da linha, a linha não mostra "ABERTO" nem "FECHADO":
mostra **\* Nao digitado \***, e a semana daquela linha fica em branco. O dia
continua na lista — o que não foi digitado é justamente o que o servidor precisa
ver.

### RN-15 — O órgão sem nenhum mapa avisa

Não havendo mapa nenhum para o órgão — nem o do dia de hoje nem um período
registrado —, a lista não começa e a tela avisa
**\* Orgao sem mapas cadastrados \***, sem preencher nenhuma linha. O aviso é
decidido **uma única vez, na última linha da lista**, e não a cada dia.

[?] O aviso também sai quando não há órgão nenhum a consultar — o vínculo não traz
órgão e o campo está em branco —, porque a decisão do aviso não distingue "órgão
sem mapa" de "nenhum órgão informado". Se o desenho previa apenas a recusa
"Informe o orgao", o caminho também avisa.

### RN-16 — A lista identifica o órgão, a unidade e o contexto da sessão

Fora das linhas, a tela mostra o **nome do órgão**, a **coordenadoria em vigor**, o
indicador de **creche** (aparece como **Sim** ou **Nao**), a **descrição do tipo de
órgão** da sessão e a **data do sistema**. A coordenadoria digitada não comanda a
consulta: a tela reescreve o campo com a coordenadoria em vigor, e quem recorta a
consulta é o grupo do órgão, não o que foi digitado.

[?] Nem a descrição do tipo de órgão nem a data do sistema são calculadas pela
tela: ela as copia da área de trabalho da sessão, e as duas únicas linhas do acervo
expandido que as escrevem são as que as deixam em branco na inicialização. Se não
vierem do ambiente de execução, os dois campos saem em branco. De onde vêm é
pergunta ao site.

[?] Se o campo da coordenadoria deveria servir de filtro — consultar um órgão pela
sua coordenadoria — ou se é apenas um campo de saída que a máscara deixa digitar, é
pergunta ao site.

[?] O dia da semana de cada linha não é o dia da semana daquela data: a montagem da
linha copia o dia da semana do dia corrente, o mesmo para as 12 linhas. Se a coluna
deveria descrever o dia de cada linha, o caminho não o faz.

[?] O rótulo que o servidor lê em cima de cada coluna da lista e em cima dos três
campos da data não está no acervo: a ficha da tela registra só os rótulos dos campos
que ela valida.

### RN-17 — A consulta não grava nada

A tela e as rotinas comuns que ela chama **só leem**. Nenhum registro é incluído,
alterado ou excluído, e nenhum registro de auditoria é gerado. A tela faz **22
chamadas de leitura** de cadastro — onze pontos de leitura, cada um nas duas formas
de posicionamento — e **nenhuma de gravação**. As operações de inclusão, de exclusão
e de travamento existem declaradas para os **6 cadastros** que a tela enxerga, mas
não são executadas em nenhum caminho: declarar não é executar.

### RN-18 — A próxima tela preenchida desvia a transação

A tela leva o seu campo de **próxima tela** para a conferência de rota, que vem
antes das conferências desta jornada. Se ele estiver preenchido, a transação é
encaminhada para a tela indicada e a consulta não é feita.

[?] Nenhum programa desta jornada preenche esse campo; quem o preenche, se alguém o
preenche, não está no acervo lido. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar a situação diária do mapa de um órgão filho da coordenadoria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M040C

  Cenário: A lista dos dias com a situação do mapa
    Dado que o órgão filho está cadastrado no meu grupo
    E que há mapa registrado para os dias a partir da data de partida
    Quando abro a tela M040C e informo o código do órgão filho e a data de partida
    Então vejo uma linha por dia, com a data, o dia da semana, a semana e a
      situação do mapa daquele dia

  Cenário: A lista mostra no máximo 12 dias
    Dado que informo uma data de partida de mais de doze dias atrás
    Quando a lista é montada
    Então a lista mostra 12 linhas

  Cenário: A lista para na data do sistema
    Dado que informo uma data de partida de mais de doze dias atrás
    Quando a lista é montada
    Então a lista mostra só os dias até a data de hoje
    E as linhas restantes ficam em branco

  Cenário: O dia com mapa aberto e o dia com mapa fechado
    Dado que o mapa de um dia da lista não está fechado
    E que o mapa de outro dia da lista está fechado
    Quando a lista é montada
    Então a linha do primeiro dia mostra "ABERTO"
    E a linha do segundo dia mostra "FECHADO"

  Cenário: A semana da linha vem do mapa
    Dado que o mapa de um dia da lista está registrado
    Quando a lista é montada
    Então a linha desse dia mostra a semana que está no mapa

  Cenário: O dia sem mapa digitado
    Dado que não há mapa registrado para um dos dias da lista
    Quando a lista é montada
    Então a linha desse dia mostra "* Nao digitado *"
    E a semana dessa linha fica em branco

  Cenário: Data de partida no futuro
    Dado que informo uma data de partida posterior à data de hoje
    Quando envio a tela
    Então nenhuma linha da lista é preenchida
    E nenhum aviso é mostrado
    E os campos do dia, do mês e do ano voltam em branco

  Cenário: Sem data informada, a lista começa no primeiro dia do mês do último mapa
    Dado que o órgão filho tem mapa registrado
    Quando envio a tela sem informar a data de partida
    Então as datas da lista começam no primeiro dia do mês do último mapa registrado

  Cenário: De agosto de 2008 em diante, a situação vem do mapa do dia
    Dado que informo uma data de partida de agosto de 2008 em diante
    Quando a lista é montada
    Então a situação de cada linha é a do mapa registrado para aquela data

  Cenário: Antes de agosto de 2008, a situação vem do mapa do período
    Dado que informo uma data de partida anterior a agosto de 2008
    Quando a lista é montada
    Então a situação de cada dia vem do mapa do período daquele dia

  Cenário: A unidade cadastrada como creche
    Dado que o órgão filho está cadastrado como creche
    E que informo uma data de partida anterior a agosto de 2008
    Quando a lista é montada
    Então a situação vem do mapa de creche
    E o indicador de creche mostra "Sim"

  Cenário: A unidade que não é creche
    Dado que o órgão filho não está cadastrado como creche
    Quando a lista é montada
    Então o indicador de creche mostra "Nao"

  Cenário: O órgão sem nenhum mapa
    Dado que o órgão filho está cadastrado no meu grupo
    E que não há mapa registrado para ele
    Quando abro a tela M040C
    Então vejo a mensagem "* Orgao sem mapas cadastrados *"
    E nenhuma linha da lista é preenchida

  Cenário: A identificação do órgão e o contexto da sessão
    Dado que o órgão filho está cadastrado no meu grupo
    Quando abro a tela M040C
    Então vejo o nome do órgão e a coordenadoria em vigor
    E vejo a descrição do tipo de órgão da minha sessão
    E vejo a data do sistema

  Cenário: Operação diferente da consulta
    Dado que estou na tela M040C
    Quando informo uma operação diferente da consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E a consulta não segue a partir daí

  Cenário: Sem o código do órgão filho
    Dado que o meu vínculo não traz órgão filho
    Quando envio a tela sem informar o código do órgão
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor volta ao campo do órgão

  Cenário: Órgão filho diferente do meu vínculo
    Dado que o meu vínculo traz um órgão filho
    Quando informo o código de outro órgão filho
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E o cursor volta ao campo do órgão
    E nenhuma lista é montada para esse órgão

  Cenário: O órgão do meu vínculo
    Dado que o meu vínculo traz um órgão filho
    Quando envio a tela com o código desse órgão
    Então a lista é montada para esse órgão

  Cenário: Órgão filho não cadastrado
    Dado que o meu vínculo não traz órgão filho
    Quando informo um código de órgão que não está no cadastro de órgãos
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão
    E nenhuma lista é montada para esse órgão

  Cenário: Órgão filho excluído do cadastro
    Dado que o código informado só tem registro marcado como excluído
    Quando envio a tela
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E nenhuma lista é montada para esse órgão

  Cenário: Órgão filho cadastrado como inativo
    Dado que o órgão informado está marcado como inativo no cadastro
    Quando envio a tela
    Então vejo a mensagem "* Orgao cadastrado como inativo *"
    E o cursor volta ao campo do órgão
    E nenhuma lista é montada para esse órgão

  Cenário: Órgão filho com dados incompletos
    Dado que falta um dos seis dados exigidos no cadastro do órgão informado
    Quando envio a tela
    Então vejo a mensagem "* Orgao cadastrado com dados incompletos *"
    E o cursor volta ao campo do órgão
    E nenhuma lista é montada para esse órgão

  Cenário: Órgão filho de outra secretaria
    Dado que o órgão informado é de outro tipo de órgão
    Quando envio a tela
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E o cursor volta ao campo do órgão
    E nenhuma lista é montada para esse órgão

  Cenário: Órgão filho de outra coordenadoria
    Dado que a minha sessão tem uma coordenadoria
    E que o órgão informado é de outra coordenadoria
    Quando envio a tela
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor volta ao campo do órgão
    E nenhuma lista é montada para esse órgão

  Cenário: Servidor sem coordenadoria na sessão
    Dado que a minha sessão não tem coordenadoria
    Quando informo o código de um órgão cadastrado em qualquer coordenadoria
    Então a lista é montada para esse órgão

  Cenário: Data que não existe no calendário
    Dado que informo uma data de partida que não existe no calendário
    Quando envio a tela
    Então vejo a mensagem "* Data invalida *"
    E o cursor volta ao campo do dia
    E nenhum mapa é lido antes dessa recusa

  Cenário: Ano da data fora do intervalo aceito
    Dado que informo uma data de partida com o ano anterior a 1994 ou posterior a 2099
    Quando envio a tela
    Então vejo a mensagem "* Data invalida *"
    E o cursor volta ao campo do dia

  Cenário: Dia, mês ou ano do mapa que não é número
    Dado que digito algo que não é número no dia, no mês ou no ano do mapa
    Quando envio a tela
    Então o sistema recusa a digitação antes de qualquer conferência de negócio

  Cenário: A coordenadoria digitada não comanda a consulta
    Dado que informo um código de órgão filho do meu grupo
    E informo uma coordenadoria diferente da dele
    Quando envio a tela
    Então a coordenadoria mostrada é a que está em vigor
    E a lista mostrada é a do órgão informado

  Cenário: A consulta não grava nada
    Dado que a lista dos dias foi mostrada
    Quando a tela é apresentada
    Então nenhum órgão e nenhum mapa é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Próxima tela preenchida
    Dado que a tela chega com uma próxima tela indicada
    Quando envio a tela
    Então a transação é encaminhada para a tela indicada
    E a consulta desta tela não é feita
```
