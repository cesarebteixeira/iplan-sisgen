# US — C700T — Prorrogar o período do cardápio

## Estória

Como **servidor de CRE**, quero **prorrogar o período de vigência dos cardápios do meu
tipo de órgão**, para que **o cardápio continue valendo depois da data-limite, sem
recadastrar cardápio por cardápio**.

O cardápio é cadastrado por período, e o período é reconhecido pelo dia em que ele se
encerra. Quando esse dia chega, alguém precisa abrir o período seguinte levando junto os
cardápios que já existem: é isso que esta tela faz — ela confere o período novo contra os
cardápios cadastrados e registra o pedido de prorrogação, que um processamento aplica
depois. Sem esse pedido, o período vence e o cardápio da semana deixa de valer. O que a
tela **não** faz é recadastrar cardápio: ela registra o pedido.

## Contexto

Jornada S000M → C000M → C070M → C700T.

Ator: servidor de CRE — prorroga o período dos cardápios do tipo de órgão da sua sessão e
acompanha os cardápios do período em tela.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. O C000M e o C070M são menus e não gravam nada: o
contexto que a C700T usa — a matrícula, a estação, o nível de acesso e o tipo de órgão —
é o que a entrada deixou na sessão. A tela não encadeia em nenhuma outra: ela encerra a
jornada.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela trabalha com o tipo de órgão do servidor e mostra a data do sistema

A tela não pergunta o tipo de órgão: ele é o da sessão. Sobre esse tipo de órgão a tela lê
o cadastro correspondente e mostra a sua descrição, junto com a data do sistema. É o mesmo
recorte que governa todo o resto da tela — os cardápios que ela lista, o período que ela
confere e o dia da semana que ela exige para a data-limite nova.

### RN-02 — A tela lista os cardápios do período, até treze linhas

A tela monta uma lista de até **treze** cardápios, uma linha por cardápio, com a data de
início do período, o código e a descrição do cardápio. A lista é a dos cardápios do tipo
de órgão da sessão, no período que está em tela; sem período em tela, a lista não é
montada.

### RN-03 — A tela abre em consulta e só aceita consultar ou alterar

Sem operação em tela, a tela abre em **consulta**. Ela aceita duas operações — consultar e
alterar — e recusa qualquer outra com `* Opcao nao disponivel. Use ALT ou CON *`,
devolvendo o cursor ao campo da operação, sem registrar nada. Não há caminho de inclusão
nem de exclusão nesta tela.

### RN-04 — A consulta parte da data-limite e exige cardápio cadastrado no período

Na consulta o servidor informa o período — dia, mês e ano de início e dia, mês e ano de
limite. Se a data-limite informada é diferente da que já está em tela, a tela procura,
para o tipo de órgão da sessão, um cardápio cujo período se encerre no ano e no mês
informados e cujo dia de encerramento seja o dia informado. Não achando, avisa
`* Nao existem cardapios para esta data *`, com o cursor no dia-limite, e não monta a
lista. Achando, toma a data de início desse cardápio como a data de início do período,
guarda a data-limite informada e mostra os cardápios do período. A consulta não grava
nada.

[?] A busca é feita pelo ano e pelo mês da data-limite e o dia é conferido depois, no
registro encontrado; o acervo lido não traz a semântica da leitura posicionada, de modo
que não se conclui o que acontece quando há mais de um cardápio no mesmo mês — se a
conferência alcança os demais ou só o primeiro deles. Pergunta ao site.

### RN-05 — O período que ficou sem cardápios é avisado e limpo

Quando a tela reapresenta um período que não tem cardápio nenhum cadastrado, ela avisa
`* Cardapios nao cadastrados *`, apaga o período que estava em tela e encerra.

### RN-06 — A alteração exige que o período tenha sido consultado antes

Na alteração, a data-limite informada tem de ser igual à que a consulta guardou. Não
sendo, a tela avisa `* Consulte antes de atualizar *`, com o cursor no campo da operação,
e não segue. Como só a consulta que acha cardápio guarda a data-limite, um período sem
cardápio cadastrado não chega a ser prorrogável.

### RN-07 — A alteração exige as duas datas novas; em branco, não acontece nada e não há aviso

Na alteração o servidor informa o período novo: dia, mês e ano de início e dia, mês e ano
de limite. Se os três campos do início novo estiverem zerados — ou os três do limite novo
—, a tela apaga o período novo e encerra **sem mensagem nenhuma**; a alteração já validada
termina sem gravar. Só com as seis datas preenchidas a tela segue adiante.

[?] Nesse encerramento sem mensagem a tela grava na área de trabalho um código de três
letras — o da consulta — num campo de um dígito, e é esse valor que interrompe as linhas
seguintes da apresentação. O acervo lido não diz como o ambiente lê esse valor; pelo
programa, a guarda seguinte só interromperia com o número 1. Pergunta ao site.

### RN-08 — As doze datas informadas passam por edição numérica

A tela tem **doze** campos de data — seis do período em vigor (dia, mês e ano de início e
de limite) e seis do período novo — e cada um deles passa por edição numérica. Campo em
branco vale zero. Quando a edição recusa um campo, o cursor volta ao campo recusado; a
tela sabe reposicionar o cursor em **nove** dos doze — os três campos do início do período
em vigor não têm posição de cursor na tela.

[?] A rotina de edição numérica é importada de biblioteca e não está no lote lido: se ela
emite mensagem própria na recusa, não se sabe qual — a tela só devolve o cursor ao campo.
Pergunta ao site.

[?] Os seis campos do período novo aparecem no acervo com o próprio nome como rótulo; a
ficha extraída do programa registra só os seis rótulos do período em vigor. Se a tela
mostra esses campos ao servidor com outro texto, o acervo não diz. Pergunta ao site.

### RN-09 — As datas novas têm de ser datas válidas, com ano entre 1994 e 2099, e a de início não pode passar da de limite

As datas novas passam por três conferências, nesta ordem: a data de início nova tem de ser
uma data de calendário válida, com o ano entre 1994 e 2099, senão a tela avisa
`* Nova data de inicio invalida *`, com o cursor no dia de início novo; a data-limite nova
passa pela mesma conferência, senão o aviso é `* Nova data limite invalida *`, com o
cursor no dia-limite novo; e a data de início nova não pode ser posterior à data-limite
nova, senão o aviso é `* Data inicial maior que data final *`, com o cursor no dia de
início novo. As datas do período em vigor não passam por essas conferências: elas só
passam pela edição numérica.

### RN-10 — A data-limite nova tem de cair no dia da semana exigido para o tipo de órgão

A tela lê o dia da semana configurado para o tipo de órgão da sessão e exige que a
data-limite nova caia no dia **anterior** a esse: segunda-feira exige domingo, terça-feira
exige segunda, quarta exige terça, quinta exige quarta, sexta exige quinta, sábado exige
sexta, e um dia não reconhecido exige sábado. Não caindo, a tela avisa
`<- Data final deve ser este dia da semana *`, com o dia esperado no próprio aviso e o
cursor no dia-limite novo. Se o tipo de órgão não tem dia da semana configurado, a
conferência não é feita — e a data-limite nova passa sem essa exigência.

[?] O que o dia configurado significa no negócio — se é o dia em que o período se encerra,
o dia da entrega ou o dia da virada — o acervo desta jornada não diz; o mesmo cadastro
guarda outros parâmetros do cardápio (dias, faixa e pessoas). Pergunta ao site.

[?] A conferência compara o dia devolvido pela conversão de data com o nome do dia em
português, e a rotina de conversão é importada de biblioteca: não se sabe pelo lote lido
se ela responde em português ou em inglês — se responder em inglês, nenhuma data-limite
nova passaria. Pergunta ao site.

### RN-11 — A prorrogação não pode invadir o período de cardápio já cadastrado

A tela faz duas conferências da mesma forma: uma procura cardápios encerrando no ano e no
mês da **data de início nova**; a outra, no ano e no mês da **data-limite nova**. Achando
um cardápio, ela compara o período novo com o período do cardápio achado e, se os dois se
sobrepõem, avisa `<- Cardapios ja cadastrados neste intervalo *`, com a data-limite do
cardápio achado no aviso e o cursor no dia de início novo. A conferência é dispensada
quando a data-limite em vigor é exatamente a data-limite do cardápio achado.

[?] A mensagem fala de "intervalo", mas a procura é por um cardápio cuja data-limite cai
no ano e no mês da data nova, e é esse cardápio que é comparado — não uma varredura de
todos os cardápios do intervalo. O acervo lido não permite concluir se a conferência
alcança os demais cardápios do mês. Pergunta ao site.

### RN-12 — A prorrogação só é registrada quando o campo de solicitação está marcado

O pedido de prorrogação só é registrado se um campo de um caractere da própria tela
estiver marcado com `S`. Sem a marca, a alteração já validada termina sem mensagem e sem
registrar nada, e a conferência de pedido em processamento também não é feita. A cada
apresentação da tela esse campo é reposto em `N`.

[?] O rótulo desse campo não está no lote lido: a ficha extraída do programa registra só
os rótulos das seis datas do período, e o programa não usa rótulo de negócio para ele.
Pergunta ao site.

### RN-13 — Marcada a solicitação, a tela registra o pedido e adota o período novo

Com a marca, a tela lê o cadastro do servidor pela matrícula da sessão — de onde tira o
e-mail do solicitante, que entra nos parâmetros do processamento —, toma o número seguinte
ao último número de requisição já usado e registra uma requisição do relatório que aplica a
prorrogação, levando o tipo de órgão, a matrícula e a estação do solicitante e as duas
datas-limite: a do período em vigor e a do período novo. Registrada a requisição, a tela
adota o período novo como o período em vigor, apaga as datas novas e mostra **Cadastro
sendo Atualizado**. A requisição nasce sem a marca de atendida.

[?] O que o processamento faz com o pedido — se ele grava a prorrogação e altera o cadastro
de cardápios — não se verifica no lote lido: nenhum dos programas desta jornada grava o
cadastro de cardápios. Pergunta ao site.

[?] O passo que registra o pedido volta a exigir só a operação de alteração, as seis datas
novas e a marca de solicitação; ele não relê as recusas do passo anterior, e quem encerra
a transação depois de uma recusa é a rotina comum de mensagens, importada de biblioteca e
sem corpo no acervo lido. Se ela não interromper, o pedido pode ser registrado depois do
aviso de recusa. Pergunta ao site.

### RN-14 — Um pedido em processamento impede outro pedido do mesmo relatório

Antes de registrar, e só quando o campo de solicitação está marcado, a tela procura um
pedido do mesmo relatório que ainda esteja em processamento. Achando, avisa
`* Relatorio em processamento. Aguarde. *`, com o cursor no campo de solicitação, e
encerra sem registrar nada.

[?] O acervo lido não mostra o que tira uma requisição da condição de pendente. O pedido
que a própria tela cria nasce sem a marca de atendida e com um número, e é por essa
condição que a conferência procura; se a procura alcança o pedido já numerado, a segunda
prorrogação fica bloqueada até que o processamento marque a requisição. Pergunta ao site.

### RN-15 — A tela não altera o cadastro de cardápios: a única gravação é o pedido

A tela enxerga **seis** cadastros — o cadastro de telas, o do tipo de órgão, o de
cardápios, o do dia da semana do cardápio, o do funcionário e o das requisições — e não
está entre eles o cadastro de auditoria. A única gravação que a tela executa é a
requisição do relatório: não há, no fluxo, nenhuma gravação do cadastro de cardápios, e a
consulta não grava nada em cadastro nenhum. A prorrogação do cardápio não acontece nesta
tela.

### RN-16 — A tela é desviada quando a transação chega endereçada a outra tela

Se a transação chega com o prefixo de tela preenchido, o encaminhamento assume: o sistema
troca a tela de destino pela tela do prefixo, sinaliza a falha e a C700T encerra sem
operar nem gravar. É o caminho pelo qual o terminal reencaminha uma transação já
endereçada.

## Cenários BDD

```gherkin
Funcionalidade: Prorrogar o período do cardápio

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C700T

  Cenário: A data do sistema e a descrição do tipo de órgão
    Dado que entrei no sistema como servidor de CRE
    Quando abro a tela C700T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: A lista dos cardápios do período
    Dado que o meu tipo de órgão tem cardápios cadastrados no período em tela
    Quando a tela se apresenta com esse período
    Então vejo até treze linhas de cardápio
    E cada linha traz a data de início, o código e a descrição do cardápio

  Cenário: A tela abre em consulta
    Dado que abro a tela C700T pelo menu
    Então a operação em tela vem preenchida com a consulta

  Cenário: Consulta dos cardápios de um período
    Dado que o meu tipo de órgão tem cardápio encerrando em 31/05/2025
    E ainda não consultei esse período
    Quando informo a data-limite 31/05/2025 e consulto
    Então vejo os cardápios do período
    E a data de início do período passa a ser a do cardápio encontrado

  Cenário: Consulta de uma data-limite sem cardápio
    Dado que o meu tipo de órgão não tem cardápio encerrando na data-limite informada
    Quando informo essa data-limite e consulto
    Então a tela avisa que não existem cardápios para esta data
    E o cursor fica no dia-limite
    E nada é gravado

  Cenário: Período em tela que ficou sem cardápios
    Dado que a tela voltou a mostrar um período
    Quando esse período não tem cardápio cadastrado
    Então a tela avisa que os cardápios não estão cadastrados
    E o período que estava em tela é apagado

  Cenário: Operação não disponível
    Dado que a tela está aberta
    Quando envio a tela com uma operação que não é consultar nem alterar
    Então a tela recusa com a mensagem que manda usar ALT ou CON
    E o cursor fica no campo da operação
    E nada é registrado

  Cenário: Prorrogação pedida
    Dado que consultei o período com a data-limite 31/05/2025 e havia cardápios
    E o meu tipo de órgão tem o dia da semana configurado como domingo
    E não há pedido do mesmo relatório em processamento
    Quando informo o período novo de 01/06/2025 a 28/06/2025 e marco a solicitação
    Então a tela registra o pedido de prorrogação
    E o período novo passa a ser o período em vigor
    E a tela mostra "Cadastro sendo Atualizado"

  Cenário: Prorrogar sem ter consultado o período
    Dado que não consultei o período com a data-limite que vou informar
    Quando altero com essa data-limite e com as datas novas preenchidas
    Então a tela avisa que é preciso consultar antes de atualizar
    E o cursor fica no campo da operação
    E nenhum pedido é registrado

  Cenário: Prorrogação sem as datas novas
    Dado que consultei o período e a data-limite informada é a mesma
    Quando altero com os seis campos do período novo zerados
    Então a alteração termina sem mensagem
    E o período novo não fica em tela
    E nenhum pedido é registrado

  Cenário: Digitação não numérica numa data
    Dado que a tela está aberta para alteração
    Quando digito letras em um dos campos de data
    Então a edição recusa a digitação
    E o cursor volta ao campo recusado

  Cenário: Data de início nova inválida
    Dado que consultei o período e a data-limite informada é a mesma
    Quando informo a data de início nova fora do calendário ou com ano fora de 1994 a 2099
    Então a tela avisa que a nova data de início é inválida
    E o cursor fica no dia de início novo
    E nenhum pedido é registrado

  Cenário: Data-limite nova inválida
    Dado que consultei o período e a data-limite informada é a mesma
    Quando informo a data-limite nova fora do calendário ou com ano fora de 1994 a 2099
    Então a tela avisa que a nova data limite é inválida
    E o cursor fica no dia-limite novo
    E nenhum pedido é registrado

  Cenário: Data de início nova posterior à data-limite nova
    Dado que consultei o período e a data-limite informada é a mesma
    Quando informo a data de início nova depois da data-limite nova
    Então a tela avisa que a data inicial é maior que a data final
    E o cursor fica no dia de início novo
    E nenhum pedido é registrado

  Cenário: Data-limite nova fora do dia da semana do cardápio
    Dado que consultei o período e o meu tipo de órgão tem o dia configurado como domingo
    Quando informo a data-limite nova em 30/06/2025, que é segunda-feira
    Então a tela avisa que a data final deve ser o dia da semana esperado
    E o aviso mostra o dia esperado, sábado
    E o cursor fica no dia-limite novo
    E nenhum pedido é registrado

  Cenário: Prorrogação que invade um período já cadastrado
    Dado que consultei o período e há cardápio cadastrado encerrando no mês da data nova
    Quando o período novo se sobrepõe ao período desse cardápio
    Então a tela avisa que já há cardápios cadastrados neste intervalo
    E o aviso mostra a data-limite do cardápio encontrado
    E o cursor fica no dia de início novo
    E nenhum pedido é registrado

  Cenário: Prorrogação sem a marca de solicitação
    Dado que consultei o período e as datas novas estão válidas
    Quando altero sem marcar o campo de solicitação
    Então a alteração termina sem mensagem
    E nenhum pedido é registrado

  Cenário: Pedido do relatório já em processamento
    Dado que consultei o período e marco a solicitação
    E já há um pedido do mesmo relatório em processamento
    Quando altero com as datas novas válidas
    Então a tela avisa que o relatório está em processamento e pede para aguardar
    E o cursor fica no campo de solicitação
    E nenhum pedido novo é registrado

  Cenário: A prorrogação não altera o cadastro de cardápios
    Dado que consultei o período e o pedido de prorrogação foi registrado
    Quando confiro o cadastro de cardápios do meu tipo de órgão
    Então nenhum cardápio foi incluído, alterado ou excluído
    E a única gravação feita foi a requisição do relatório

  Cenário: A consulta não grava nada
    Dado que consulto o período com a data-limite informada
    Quando a consulta termina
    Então nada foi gravado em cadastro nenhum

  Cenário: A transação chega endereçada a outra tela
    Dado que a transação chega com o prefixo de tela preenchido
    Quando envio a tela C700T
    Então o sistema desvia para a tela do prefixo
    E a C700T encerra sem operar e sem gravar
```
