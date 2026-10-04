# US — C672C — Solicitar a impressão das alterações de período de licitação

## Estória

Como **servidor da CRE**, quero **pedir a impressão das alterações de período de
licitação já cadastradas para o tipo de órgão da minha secretaria**, para que **o
relatório saia com o período, o tipo de contrato e o número do ofício sem redigitação, e
cada alteração fique com o papel que instrui o processo**.

O período de uma licitação é a faixa de vigência: o dia, o mês e o ano em que ela começa
e o dia, o mês e o ano em que termina. Quando a data limite muda, o sistema guarda a
alteração com o número do ofício que a autorizou, a data limite anterior e a nova — e é
esta tela que transforma essa alteração em papel. O que depende dela é o relatório que
acompanha o processo: sem o pedido, a alteração existe no sistema e ninguém a lê no
papel.

## Contexto

Jornada S000M → C000M → C050M → C672C.

Ator: servidor de CRE — escolhe, entre as alterações de período já cadastradas do seu
tipo de órgão, a linha cujo relatório deve ser impresso, e informa a impressora.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas antes do destino, `C000M` e `C050M`, são menus: a tela é aberta por opção
de menu, não por encadeamento de tela. O tipo de órgão, a matrícula, o privilégio, a CRE
e a descrição do tipo de órgão com que ela trabalha chegam pela sessão, deixados pela
entrada; esta tela não os recalcula. O modo de operação também não vem de quem a chama:
não há, no fonte desta tela, nenhuma comparação com a tela de origem, e ela abre sempre
em consulta.

A tela grava, mas não no cadastro que mostra: o que ela deixa é o pedido de impressão do
relatório, na fila de impressão do sistema, e a entrega do relatório para processamento.
Ela não inclui, não altera e não exclui nenhuma alteração de período, e é o fim da
jornada: não encadeia outra tela.

---

## Regras de negócio

### RN-01 — A tela pede a impressão do que já está cadastrado; ela não mantém o cadastro

A tela existe para uma coisa: escolher, entre as alterações de período já cadastradas do
tipo de órgão, a que deve ser impressa, e pedir o relatório. Do que ela mostra, nada é
mantido aqui — não há inclusão, alteração nem exclusão de alteração de período. O que ela
deixa é o pedido: um registro na fila de impressão, com o relatório, o tipo de órgão, a
matrícula de quem pediu, a estação e o dia, o mês e o ano do pedido, e a entrega do
relatório para processamento. O cadastro que alimenta a lista não aparece nesta jornada.

[?] O nome de negócio desta tela e o do relatório não vêm do lote: o título que ela
exibe é lido de um cadastro de títulos que não faz parte do material, e o relatório é
referenciado por um código e por um caminho de execução. O nome usado nesta estória é
leitura de negócio, não transcrição. Pergunta ao site.

[?] Nenhum programa da árvore expandida grava as alterações de período que esta tela
lista: ela é o único programa do lote que enxerga esse cadastro, e nenhuma inclusão,
alteração ou exclusão dele é executada. De onde elas vêm — de outro sistema ou de rotina
fora do lote — é pergunta ao site.

### RN-02 — A lista mostra treze alterações por passagem, cada uma com o período, o contrato e o ofício

A tela apresenta até treze alterações por passagem, na ordem do próprio cadastro — tipo
de órgão, data limite, tipo de contrato, número do ofício, CRE e classe de licitação — e
continua na passagem seguinte quando a anterior enche. De cada alteração, a linha mostra
o período como uma faixa: o dia, o mês e o ano de início, a letra "a" e o dia, o mês e o
ano limite; e informa ainda o tipo de contrato e o número do ofício. Fora da lista, o
cabeçalho traz a descrição do meu tipo de órgão e a data do sistema. A capacidade
declarada do cadastro é de 10.000 alterações — capacidade, não volume cadastrado.

[?] A listagem avança por cima das alterações cujo tipo de contrato e número de ofício
repetem os da linha já aceita. Se isso é para não repetir a mesma alteração, ou efeito
colateral, e quantas alterações ficam escondidas, não está no material. Pergunta ao site.

[?] A retomada da lista entre uma passagem e outra usa recursos de posicionamento do
banco que não estão explicados no material lido: não dá para afirmar que a passagem
seguinte começa na alteração seguinte, sem repetir nem pular. Pergunta ao site.

### RN-03 — As três datas e o tipo de contrato são números; o número do ofício é texto

O dia, o mês e o ano — de início e de limite — e o tipo de contrato de cada linha passam
pela edição numérica com o rótulo que o operador vê, antes de qualquer conferência de
negócio; o campo deixado em branco é lido como zero. O número do ofício, esse, é texto e
não passa por essa edição.

[?] O que a tela faz com um valor que não é número — se recusa no campo, se zera, com que
mensagem — não está no material lido: a rotina de edição numérica é do ambiente de
execução e não tem corpo nos fontes. Pergunta ao site.

### RN-04 — Só a linha marcada é pedida; a linha sem marca não faz nada

A linha só conta quando leva a marca de seleção: sem ela, a linha atravessa a tela em
silêncio — nenhuma mensagem, nenhum pedido. A marca é digitada pelo operador; a tela não
a preenche sozinha nem a devolve preenchida.

[?] O rótulo que o usuário lê nesse campo está na máscara da tela, que não faz parte do
material. Pergunta ao site.

### RN-05 — Sem alterações cadastradas, a tela avisa e não pede nada

Se o tipo de órgão não tem nenhuma alteração de período cadastrada, a tela avisa
* Nao existem alteracoes cadastradas * e deixa o cursor na marca da primeira linha; nada
é pedido.

### RN-06 — A tela abre em consulta e só a consulta passa

Entrando sem informar a opção, a tela repõe a consulta a cada apresentação. Se o operador
informar outra opção, o sistema recusa com
* Operacao nao disponivel. Use ALT * e devolve o cursor ao campo da opção. Não há nesta
tela inclusão, alteração nem exclusão de alteração de período. O modo não muda conforme a
tela que a chamou: esta tela não compara a origem com código de tela nenhum.

[?] A opção é comparada com a palavra da consulta que o ambiente carrega da tabela de
mensagens do idioma, não com um texto fixo do programa — e a tabela não faz parte do
material. A mensagem da recusa manda usar ALT: se ALT é a palavra que o ambiente carrega,
a guarda e a mensagem combinam; se não é, ALT é recusado. Qual palavra o operador tem de
digitar é pergunta ao site.

### RN-07 — O mesmo relatório não pode ter dois pedidos na fila

Para cada linha marcada, a tela confere se já existe um pedido desse relatório esperando
na fila de impressão. Existindo, recusa com
* Relatorio em processamento. Aguarde. * e o cursor volta à marca da linha; nenhum pedido
novo é registrado.

[?] A conferência olha só o código do relatório: não compara quem pediu, para qual tipo
de órgão, nem o estado do pedido. Se um pedido de outra origem com o mesmo relatório
travar o pedido desta tela, é pergunta ao site.

[?] A conferência só passa pela linha que tem o dia limite preenchido e a marca; a
passagem que registra o pedido olha apenas a marca e o ano de início do período. Uma
linha marcada com o dia limite zerado atravessa as recusas desta regra e da impressora e
ainda gera pedido — ou a guarda do dia limite vale para outro caso, ou o caminho ficou
alcançável demais. Pergunta ao site.

### RN-08 — A impressora é obrigatória

A linha marcada só é conferida quando a impressora está informada; sem ela, a tela recusa
com * Informe a impressora * e devolve o cursor ao campo da impressora.

[?] A impressora é exigida na conferência, mas o registro do pedido é gravado com ela em
branco: a impressora informada segue apenas no bloco de parâmetros entregue ao
processamento do relatório. Se o pedido for reprocessado pela fila, a impressora pode
faltar. Pergunta ao site.

### RN-09 — A linha marcada gera o pedido de impressão do relatório

Com a linha marcada e o ano de início do período preenchido, a tela relê a alteração no
cadastro, numera o pedido como o seguinte ao último pedido registrado e o grava na fila
de impressão, com o relatório, o tipo de órgão, a matrícula de quem pediu, a estação e o
dia, o mês e o ano do pedido; em seguida entrega o processamento do relatório, levando no
bloco de parâmetros o tipo de órgão, a CRE, a classe de licitação, as três datas do
período, o tipo de contrato e o número do ofício. É esse pedido que fica como rastro da
operação: esta tela não grava a trilha de auditoria do sistema.

[?] A releitura que antecede o pedido confere a alteração pela chave inteira do cadastro
— tipo de órgão, data limite, tipo de contrato e número do ofício —, mas quando não
encontra o registro a operação segue adiante do mesmo jeito: o pedido é montado com o que
estiver na área de trabalho. Uma linha marcada cuja alteração não esteja mais no cadastro
ainda pode gerar pedido. Pergunta ao site.

[?] A CRE e a classe de licitação que vão ao relatório são lidas numa segunda procura ao
cadastro que **não** usa esses dois campos na chave — ela procura pelo tipo de órgão,
pelas datas, pelo tipo de contrato e pelo número do ofício. Havendo mais de um registro
com essa combinação, o pedido pode sair com a CRE e a classe de outro registro. Pergunta
ao site.

[?] Parte do código gerado desta tela foi omitida na expansão do acervo — entre os
trechos omitidos está a rotina chamada entre a conferência e o registro do pedido. O que
ela faz não pode ser lido. Pergunta ao site.

[?] Quem lê a fila de impressão e imprime o relatório não está nesta jornada: nenhum dos
programas dela imprime o relatório nem marca o pedido como processado. Pergunta ao site.

### RN-10 — Depois do pedido, a tela para: um pedido por passagem

Registrado o pedido, a tela marca a operação como já feita e não pede mais nada nesta
passagem: a segunda linha marcada é conferida de novo, encontra na fila o pedido que
acabou de ser registrado e recebe
* Relatorio em processamento. Aguarde. * — nenhum segundo pedido sai.

[?] Não está no material se a mensagem de recusa encerra a transação: a rotina que a
exibe é do ambiente de execução e não tem corpo nos fontes. Se ela não encerrar, o
caminho que grava pode registrar o pedido depois da recusa. Pergunta ao site.

### RN-11 — A tela só opera para quem está cadastrado nela

A abertura e a operação passam pela segurança do sistema: a tela tem de estar cadastrada
e o código de acesso do usuário tem de ter registro para ela, com a matrícula, o
privilégio, o tipo de órgão e a CRE vindo da sessão. Sem o registro da tela, a recusa é
* Tela nao disponivel *; sem o registro do acesso, é
* Acesso negado para esta matricula * — e a transação é abandonada sem ler nem registrar
nada.

[?] O cadastro de acessos tem um campo próprio para liberar ou negar a consulta, e a
conferência desta tela não o testa: só a inclusão, a alteração e a exclusão têm flag
conferido. Se negar a consulta pelo cadastro é para valer, é pergunta ao site.

### RN-12 — A tela pode servir de passagem para outra, e aí não faz nada aqui

Se a transação chega com o campo que indica a próxima tela preenchido, a operação é
entregue a essa tela e esta não confere nem pede nada. Chegando vazio esse campo, a
conferência corre normalmente. A tela não encadeia tela por conta própria: o que ela
entrega adiante, além da passagem, é o pedido de impressão e o processamento do
relatório.

[?] Não dá para concluir, pela fonte, se esse campo pode chegar preenchido pelo terminal:
nada nesta tela o limpa, e a segunda conferência do mesmo campo — a que desviaria em
silêncio — está depois do desvio que entrega a operação à outra tela, de modo que ela é
inalcançável por esse caminho. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Solicitar a impressão das alterações de período de licitação

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C672C

  Cenário: RN-01 e RN-02 — a lista mostra as alterações de período do meu tipo de órgão
    Dado que existem alterações de período cadastradas para o meu tipo de órgão
    Quando abro a tela C672C
    Então vejo o cabeçalho com a descrição do meu tipo de órgão e a data do sistema
    E vejo até treze linhas, cada uma com o período (de início a limite), o tipo de contrato e o número do ofício
    E nada é gravado

  Cenário: RN-01 e RN-04 — consultar sem marcar nenhuma linha não pede nada
    Dado que estou na tela C672C com a opção de consulta
    Quando confirmo sem marcar nenhuma linha
    Então nenhum pedido de impressão é registrado
    E nenhuma mensagem é mostrada

  Cenário: RN-05 — o tipo de órgão não tem alterações cadastradas
    Dado que não há alteração de período cadastrada para o meu tipo de órgão
    Quando abro a tela C672C
    Então vejo "* Nao existem alteracoes cadastradas *"
    E o cursor fica na marca da primeira linha
    E nada é registrado

  Cenário: RN-03 — a data deixada em branco vale zero
    Dado que estou na tela C672C
    Quando deixo o mês de uma data em branco
    Então a tela conta aquele mês como zero

  Cenário: RN-06 — opção diferente da consulta é recusada
    Dado que estou na tela C672C
    Quando informo uma opção diferente da consulta
    Então vejo "* Operacao nao disponivel. Use ALT *"
    E o cursor volta para o campo da opção
    E nenhum pedido é registrado

  Cenário: RN-07 — o relatório já tem um pedido na fila
    Dado que já existe um pedido desse relatório na fila de impressão
    Quando marco uma linha e confirmo
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor volta para a marca da linha
    E nenhum pedido novo é registrado

  Cenário: RN-08 — sem a impressora a tela recusa
    Dado que estou na tela C672C com uma linha marcada, o dia limite preenchido e nenhum pedido desse relatório na fila
    Quando confirmo sem informar a impressora
    Então vejo "* Informe a impressora *"
    E o cursor volta para o campo da impressora
    E nenhum pedido é registrado

  Cenário: RN-09 — a linha marcada gera o pedido de impressão do relatório
    Dado que a alteração de período está cadastrada, a linha está marcada, o ano de início está preenchido e a impressora está informada
    Quando confirmo o pedido
    Então o sistema registra o pedido de impressão do relatório na fila
    E o pedido recebe o número seguinte ao último pedido registrado
    E o processamento do relatório é entregue para execução
    E o pedido leva o tipo de órgão, a CRE, a classe de licitação, as três datas do período, o tipo de contrato e o número do ofício

  Cenário: RN-03 e RN-09 — sem o ano de início a linha marcada não gera pedido
    Dado que estou na tela C672C com uma linha marcada e o ano de início do período zerado
    Quando confirmo
    Então nenhum pedido é registrado para aquela linha

  Cenário: RN-10 — depois do pedido, a segunda linha marcada é recusada
    Dado que acabei de registrar o pedido de impressão de uma linha nesta passagem
    Quando a conferência chega a uma segunda linha marcada
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E nenhum segundo pedido é registrado

  Cenário: RN-11 — acesso não cadastrado para a tela
    Dado que o meu código de acesso não tem registro para esta tela
    Quando tento abrir a tela C672C
    Então vejo "* Acesso negado para esta matricula *"
    E a transação é abandonada
    E nada é lido nem registrado

  Cenário: RN-12 — a tela é usada como passagem para outra
    Dado que a transação chega à C672C com o campo que indica a próxima tela preenchido
    Quando confirmo
    Então a operação é entregue à tela indicada
    E nada é pedido nesta tela
```
