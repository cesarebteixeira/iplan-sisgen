# US — C219C — Consultar períodos da tabela especial de preços

## Estória

Como **servidor de CRE**, quero **consultar os períodos da tabela especial de preços e abrir,
do período que eu marcar, a relação de gêneros e preços daquela quinzena**, para que **eu saiba
quais quinzenas já têm preço cadastrado e chegue aos preços da quinzena escolhida sem precisar
digitar a data de início**.

A tabela especial de preços é a que responde pelo preço do gênero quando a quinzena é do tipo
especial; cada preço é registrado por classe, subclasse e gênero, dentro de um período. Quem
confere o que já está cadastrado não tem como adivinhar as datas: sem uma relação dos períodos,
a única saída seria abrir a manutenção período por período, tentando datas até acertar. Esta tela
é o índice dessas quinzenas — e não grava nada: quem inclui, altera e exclui preço é a tela que
ela abre.

## Contexto

Jornada S000M → C000M → C015M → C219C.

Ator: servidor de CRE — vê quais períodos têm tabela de preços e escolhe um deles para abrir os
preços daquela quinzena.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio. O `C000M` e o `C015M` são **menus**: só encaminham, não gravam nada e não
deixam período escolhido nem operação para esta tela.

Do contexto da sessão, esta tela usa **a descrição do tipo de órgão** e **a data do sistema**,
que exibe no cabeçalho, e **a matrícula, o código de acesso, o privilégio, a estação e a
coordenação regional**, que entrega às conferências de acesso. A tabela de preços que ela
consulta, porém, **não é por secretaria**: ela não guarda o órgão, e a relação não é limitada por
ele.

Esta tela encadeia: marcado um período, ela passa o **período escolhido** e a **operação de
consulta** para a `C219T` — a tela de manutenção dos preços daquela tabela —, que abre em
consulta sobre o período. A jornada termina aqui; quem mostra os preços por gênero é a tela
seguinte.

## Regras de negócio

### RN-01 — A tela consulta os períodos da tabela especial de preços

Esta é uma tela de **consulta**. Ela mostra os **períodos** registrados na **tabela especial de
preços** e nada grava: não há inclusão, alteração nem exclusão, nenhum registro é travado e
nenhuma linha de auditoria é gerada.

O cabeçalho da tela traz a **descrição do tipo de órgão** da sessão e a **data do sistema**. A
tela também confere, ao se apresentar, se ela própria está cadastrada no **cadastro de telas** —
é de lá que vem o título que ela mostra.

Cada linha da relação traz o **dia, o mês e o ano do início do período** e o **dia, o mês e o ano
do limite** dele, mais um campo para marcar a linha (RN-10). Como a tabela de preços não guarda a
secretaria, a relação é a mesma para qualquer secretaria: a descrição do tipo de órgão aparece na
tela, mas **não filtra** o que é listado.

### RN-02 — Cada período aparece uma vez, na ordem do início

A relação é montada percorrendo os preços registrados na tabela e **guardando só o primeiro
registro de cada período**: os demais registros do mesmo período — que existem um por classe,
subclasse e gênero — são saltados, de modo que **cada período vira uma única linha**, com o
início e o limite daquele período. Os gêneros de um período, portanto, **não** aparecem aqui: eles
são o conteúdo da tela que esta abre.

A ordem é a do cadastro: **ano, mês e dia do início** e, dentro da mesma data, classe, subclasse
e gênero. Como a linha só se repete por período, o efeito é uma **relação de períodos em ordem
crescente de início**.

### RN-03 — A relação começa no ano do sistema

Ao se apresentar sem operação vinda da sessão, a tela posiciona a relação no **ano do sistema**,
com mês, dia, classe, subclasse e gênero zerados — isto é, começa no primeiro período registrado
**do ano corrente**, e não no começo da tabela.

[?] O posicionamento usa um recurso do dicionário de dados cujo efeito exato não está no acervo
nem no manual: se ele exige a chave exata — e mês e dia zerados não existem em período nenhum —,
a relação não acha nada e cai no aviso de RN-05; se ele posiciona no primeiro registro igual ou
posterior, a relação começa no primeiro período do ano. O site precisa dizer qual é o esperado.
Pergunta ao site.

[?] A tela só faz esse posicionamento quando a área de trabalho que a sessão guarda entre telas
chega **sem operação**; chegando com operação, ela pula a busca da data e da hora e começa do
período que já estiver guardado ali. Como os menus que encaminham para esta tela não escrevem
essa área, não há como saber pelo acervo lido se a tela abre sempre no ano do sistema. Pergunta
ao site.

### RN-04 — A página tem treze períodos, e a relação continua de onde parou

A página tem **treze linhas** — treze períodos — e três campos de posição (**dia, mês e ano
iniciais**), que dizem por onde a relação começa. Quando a página enche, esses três campos passam
a mostrar o início do período da **última linha**, de modo que reenviar a consulta nesse estado
continua a relação a partir dali. Quando a relação chega ao fim antes de a página encher, os três
campos voltam a zero.

[?] Não há no fonte nenhum avanço depois de a página encher — nem um dia a mais, nem o salto do
registro que já apareceu: se o posicionamento for o de "primeiro registro igual ou posterior", a
página seguinte começa repetindo o período que já era a última linha. O acervo não permite
decidir. Pergunta ao site.

### RN-05 — Sem período na posição, a tela avisa que não existem tabelas cadastradas

Não achando **nenhum** período na posição em que a relação começa, a tela não preenche linha
alguma e avisa **\* Nao existem tabelas cadastradas \***. O aviso é decidido na montagem da
**primeira linha** da página e não se repete nas demais.

### RN-06 — A tela apaga o resultado anterior antes de conferir

A cada envio, **antes** de qualquer conferência, a tela apaga **a descrição do tipo de órgão** e
**a data do sistema** que havia mostrado. Uma consulta recusada, portanto, não deixa o resultado
da consulta anterior no cabeçalho.

[?] Os dois campos só são preenchidos na **primeira** apresentação da tela: quem os preenche é o
caminho que monta a página, e ele não roda de novo a cada envio. Se o ambiente não repuser o
cabeçalho por conta própria — e o acervo lido não mostra quem o faria —, os dois aparecem em
branco depois do primeiro envio. Pergunta ao site.

### RN-07 — A conferência de número vem antes de qualquer leitura

**Nove** campos passam pela conferência de número antes de qualquer leitura do cadastro: o dia, o
mês e o ano do início, o dia, o mês e o ano do limite e os três campos de posição. O que não for
número é recusado no próprio campo e a consulta não segue. O dia, o mês e o ano de **posição** em
branco são tratados como zero.

[?] A posição do cursor só está declarada para **três** dos nove campos — os de posição —; para os
seis campos do período o programa não diz onde o cursor volta. E o texto que o operador lê quando
um valor não numérico é recusado não está no programa: a conferência é chamada de rotinas de
biblioteca cujo corpo não veio no lote. Pergunta ao site.

### RN-08 — A operação da tela é a consulta: qualquer outra é recusada

A tela se apresenta repondo a **operação de consulta** no campo da opção. Se o que chega ali for
outra operação, ela recusa com **\* Operacao nao disponivel. Use CON \***, devolve o cursor ao
campo da opção e não lê período nenhum. A conferência vale para a **primeira** linha da página.

[?] A recusa manda usar "CON", mas o sistema reconhece a consulta por um código interno que o
acervo escreve como "INQ"; nenhum valor "CON" existe no corpus lido. Ou o formulário traduz o que
o servidor digita para esse código, ou quem seguir a mensagem é recusado. A mesma dúvida está
registrada nas telas irmãs. Pergunta ao site.

[?] A recusa só existe se a máscara oferecer ao operador um campo de opção, e é o mesmo campo que
a tela preenche ao se apresentar: se ele não voltar preenchido, a tela não deixa passar consulta
nenhuma. A ficha da tela lista os rótulos dos campos e não diz qual deles é o da operação.
Pergunta ao site.

### RN-09 — Marcado um período, a tela de preços abre em consulta sobre ele

Marcada uma linha da relação **e** preenchido o início do período daquela linha, a tela **não**
segue com uma operação própria: ela passa o **período escolhido** — início e limite — e a
**operação de consulta** para a tela de manutenção dos preços, que abre **em consulta** sobre
aquele período. É essa passagem que dá sentido à tela: a relação é o índice, os preços são o
conteúdo.

Junto com o período e a operação, a tela marca de onde veio; a tela seguinte, porém, **não lê
essa marca**: o que decide o modo dela é a **operação** recebida, e ela só aceita a consulta e a
alteração. Vindo desta tela, o modo é sempre o de consulta.

### RN-10 — Marcar uma linha sem período é recusado

Marcada uma linha da página em que o início do período está em branco, a tela recusa com
**\* Consulte detalhes de linha preenchida \***, devolve o cursor ao campo de marcação daquela
linha e não abre nada. É a recusa de quem marca uma linha vazia da página.

[?] O rótulo que o servidor vê no campo de marcação e o valor que ele digita não estão no corpus:
o que o fonte fixa é o literal "X" e o fato de o campo ser exibido em cada linha. A máscara da
tela é carregada em tempo de execução e não veio no lote. Pergunta ao site.

### RN-11 — O código da próxima tela preenchido abandona a consulta

Se a mensagem chega com o **código da próxima tela** preenchido, a consulta é abandonada antes de
qualquer conferência de período e a sessão é encaminhada para a tela indicada.

[?] O que preenche esse código nesta tela não está no acervo: não se sabe quem manda próxima tela
para a C219C. Pergunta ao site.

### RN-12 — Nada é lido sem a conferência de sessão e de permissão

Antes de mostrar a relação, a tela confere a sessão — a estação, o cadastro da tela e o código de
acesso do servidor — e, por operação, a permissão do perfil para a tela, com a operação de
consulta que ela mesma montou. Faltando a autorização, a tela não opera e nada é lido.

[?] Na conferência de permissão, a operação de consulta cai no ramo que confere a permissão de
**alteração**, e não a de consulta — o cadastro de telas guarda as quatro permissões separadas.
Como a tela manda a operação de consulta junto com a marca de manutenção, este é exatamente o
caminho que ela percorre. Ou uma tela de consulta exige mesmo a permissão de alteração, ou a
conferência está lendo a permissão errada. A mesma dúvida está registrada nas telas irmãs.
Pergunta ao site.

### RN-13 — Falha do banco interrompe a consulta e avisa

Toda leitura desta tela testa o erro do banco. Erro de leitura vira a ação de erro de acesso, com
a mensagem de erro do sistema, e a operação para ali, sem completar a relação.

## Cenários BDD

```gherkin
Funcionalidade: Consultar os períodos da tabela especial de preços e abrir os preços da quinzena escolhida

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C219C

  Cenário: RN-01 — consultar os períodos da tabela especial de preços
    Dado que a tabela especial de preços tem períodos registrados
    Quando abro a tela C219C
    Então vejo a descrição do tipo de órgão da minha sessão e a data do sistema
    E vejo, em cada linha, o dia, o mês e o ano do início e do limite do período

  Cenário: RN-01 — a consulta não grava nada
    Dado que abro a tela C219C
    Quando a relação é mostrada
    Então nenhum registro é travado
    E nenhuma linha nova aparece na trilha de auditoria

  Cenário: RN-02 — um período com vários gêneros aparece uma vez
    Dado que um mesmo período tem preço registrado para mais de um gênero
    Quando vejo a relação
    Então aquele período aparece em uma única linha
    E os gêneros daquele período não aparecem nesta tela

  Cenário: RN-02 — os períodos aparecem em ordem de início
    Dado que a tabela tem mais de um período registrado
    Quando vejo a relação
    Então os períodos aparecem do mais antigo para o mais novo
    E cada linha traz o início e o limite de um período

  Cenário: RN-03 — a relação começa no ano do sistema
    Dado que a tabela tem períodos de anos anteriores e do ano corrente
    Quando abro a tela C219C
    Então a relação começa no primeiro período do ano corrente
    E os períodos dos anos anteriores não aparecem

  Cenário: RN-04 — a página tem treze períodos
    Dado que a tabela tem mais de treze períodos registrados
    Quando abro a tela C219C
    Então a página mostra no máximo treze linhas
    E os campos de posição passam a mostrar o início do período da última linha

  Cenário: RN-04 — continuar a relação a partir do período mostrado
    Dado que a página encheu as treze linhas
    Quando reenvio a consulta sem mudar os campos de posição
    Então a relação continua a partir do período indicado nos campos de posição

  Cenário: RN-05 — nenhum período na posição
    Dado que não há período registrado na posição em que a relação começa
    Quando abro a tela C219C
    Então vejo a mensagem "* Nao existem tabelas cadastradas *"
    E nenhuma linha é preenchida

  Cenário: RN-06 — o resultado da consulta anterior não fica no cabeçalho
    Dado que abri a tela e ela mostrou o tipo de órgão e a data do sistema
    Quando reenvio a consulta
    Então a descrição do tipo de órgão e a data do sistema foram apagadas antes da conferência

  Cenário: RN-07 — digitação não numérica
    Dado que digito algo que não é número em um dos campos do período ou de posição
    Quando envio a consulta
    Então a consulta não segue
    E nenhum período é lido do cadastro

  Cenário: RN-08 — operação diferente da consulta
    Dado que estou na tela C219C
    Quando a tela recebe uma operação diferente da consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nenhum período é lido

  Cenário: RN-09 — marcar um período e abrir os preços dele
    Dado que a relação mostra períodos registrados
    E marco a linha de um período
    Quando confirmo
    Então a tela de manutenção dos preços abre em consulta sobre aquele período
    E vejo o início e o limite daquele período
    E nada é gravado por esta tela

  Cenário: RN-09 — o período entregue é o da linha marcada
    Dado que marco a linha de um período da relação
    Quando a tela de preços abre
    Então ela abre no período marcado, com a operação de consulta
    E não no período que estava nos campos de posição

  Cenário: RN-10 — marcar uma linha sem período
    Dado que marco o campo de marcação de uma linha em que o período está em branco
    Quando confirmo
    Então vejo a mensagem "* Consulte detalhes de linha preenchida *"
    E o cursor volta ao campo de marcação daquela linha
    E nenhuma tela se abre

  Cenário: RN-11 — código da próxima tela preenchido
    Dado que a mensagem chega à C219C com o código da próxima tela preenchido
    Quando a consulta começaria
    Então o período não é conferido e nada é lido
    E a sessão é encaminhada para a tela indicada

  Cenário: RN-12 — sem autorização para a tela
    Dado que o meu código de acesso não tem esta tela autorizada no perfil
    Quando abro a tela C219C
    Então a tela não opera
    E nenhum período é lido

  Cenário: RN-13 — falha do banco durante a consulta
    Dado que a leitura do cadastro falha no banco
    Quando abro a tela C219C
    Então a operação é interrompida com a mensagem de erro do sistema
    E a relação não é completada
```
