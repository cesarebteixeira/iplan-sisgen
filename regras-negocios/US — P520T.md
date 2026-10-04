# US — P520T — Consulta e exclusão dos processos da CRE, com pedido de impressão

## Estória

Como **servidor de CRE**, quero **conferir a relação dos processos do meu grupo e
tirar dela o processo que não deve seguir**, para que **só o que a CRE reconhece
como devido seja transmitido — e para que a relação possa ser impressa**.

Os processos do grupo passam por uma conferência em que se vê, processo a processo,
o número, o valor, o empenho, o ano de referência e o dia e a hora da última
atualização. É nessa conferência que se decide o que sai: o servidor da CRE assinala
o processo que não deve seguir, e ele é apagado do cadastro. Sem esta tela, um
processo que não deva seguir não teria por onde ser retirado da relação, e a CRE não
teria por onde pedir a impressão dela.

## Contexto

Jornada S000M → P000M → P500M → P520T.

Ator: servidor de CRE — nesta tela, confere os processos do seu grupo, exclui o
processo que não deve seguir e pede a impressão da relação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada, `P000M` e `P500M`, são menus: só encaminham e
não deixam dado de negócio para esta tela. O contexto que a `P520T` usa — a
matrícula, a CRE, a secretaria (o órgão da sessão), o código de acesso e a estação —
é o que a entrada deixou na sessão.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — Ao abrir, a tela mostra os processos do grupo

Abrir a tela não grava nada: ela lê os processos do grupo e mostra, uma linha por
processo, até sete processos por vez, com o número do processo, o valor, o número do
empenho, o ano de referência, o dia e a hora em que o processo foi atualizado e o
tipo de anulação. Não havendo nenhum processo no grupo, a tela avisa
**\* Nao existem processos a transmitir \*** e encerra a operação sem mostrar linha
nenhuma.

[?] A tela confere na entrada — e edita — o valor do processo, o número do empenho e
o ano de referência, mas nenhum dos três é usado em leitura ou em gravação: eles não
filtram a lista nem identificam o processo. Se a máscara espera que eles filtrem, ou
se são só informativos, não se lê no corpus. Pergunta ao site.

[?] O que a tela pede ao banco para começar a lista não está no corpus: o primeiro
pedido é feito com a data e a hora de atualização em zero, e o recurso de leitura que
a tela usa vem de fora do acervo. Se essa leitura, com data zero, é a leitura exata
de um registro, a tela não mostra processo nenhum; se é um posicionamento a partir do
começo, mostra os processos do grupo. Disso depende a tela ter conteúdo. Pergunta ao
site.

[?] Os nomes das colunas que o operador vê não estão no lote: o que se lê no fonte
são os quatro rótulos de conferência (**CORD.REG.ESCOLAR**, **VALOR PROCESSO**,
**NUM.EMPENHO** e **ANO REFERENCIA**), e a ficha da tela registra que a máscara pode
ter outros. Pergunta ao site.

### RN-02 — A tela só tem duas operações: consulta e exclusão

A tela não inclui processo nenhum e não altera dado nenhum de processo: das
operações que ela executa, a única que mexe no cadastro é a exclusão do processo
assinalado. Só passam a consulta e a alteração; qualquer outra opção é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, o cursor volta para o campo da opção
e nada é gravado.

[?] A recusa da opção, no próprio trecho que a emite, não marca a falha que
interromperia a mensagem — ao contrário dos avisos de acesso, que a marcam —, e o
trecho que executa a exclusão não confere a opção: ele trata como alteração tudo o
que não for consulta. Se o operador assinalar uma linha e informar uma opção
recusada, não foi possível determinar pelos fontes se a exclusão ainda acontece.
Pergunta ao site.

[?] A tela manda usar ALT ou CON, mas compara o que foi informado com os códigos de
operação do sistema (os mesmos das telas de manutenção), e a máscara, que poderia
traduzir um vocabulário no outro, não está no acervo. Se o operador digitar
exatamente o que a mensagem manda, a opção pode ser recusada na conferência e, ainda
assim, executada. Pergunta ao site.

### RN-03 — A consulta não exclui nem altera processo

Com a opção de consulta, a tela não exclui, não inclui e não altera processo nenhum,
ainda que alguma linha esteja assinalada. A consulta também não exige a liberação de
alteração no código de acesso de quem opera — basta o acesso à tela. O pedido de
impressão não depende da opção: vale para a consulta e para a alteração (RN-11).

### RN-04 — A exclusão é do processo assinalado, e só se ele estiver cadastrado

Para excluir, o operador assinala a linha do processo com a marca de exclusão e
confirma com a opção de alteração. A marca não vem preenchida: a tela chega em branco
e é o operador que a informa, linha a linha. O processo assinalado precisa existir no
cadastro do grupo: não existindo, a tela avisa **\* Registro nao cadastrado \***,
deixa o cursor na marca daquela linha e não apaga nada. Linha assinalada com outra
marca é ignorada.

[?] A conferência da linha exige o dia e a hora da atualização, e a exclusão exige o
número do processo: uma linha sem data passa sem conferência e, ainda assim, a
exclusão é tentada, com a data em zero. Se isso alcança um processo de data zerada,
não se lê no corpus. Pergunta ao site.

### RN-05 — A exclusão apaga o processo e deixa registro de auditoria

Achando o processo, a tela apaga o registro do cadastro do grupo e, antes de apagar,
grava na auditoria a operação de exclusão, o cadastro, o processo inteiro como estava
— número, valor, empenho, ano de referência, fornecedor, órgão, datas — e quem
operou, a CRE, a secretaria, o terminal e o dia e a hora da sessão. Como o processo
sai do cadastro, o registro de auditoria guarda o que havia antes e nada depois.

[?] A rotina da auditoria é abandonada quando a mensagem já está marcada como falha,
mas a exclusão que vem logo depois não consulta essa marca: se a leitura do processo
falhar e marcar a falha, o processo pode ser apagado sem o registro de auditoria.
Pergunta ao site.

[?] O cadastro admite mais de um processo com o mesmo número na mesma data, e a busca
para no primeiro que casa: havendo repetição, não se sabe qual dos dois é apagado.
Pergunta ao site.

### RN-06 — A exclusão exige autorização de alteração para esta tela

A exclusão exige que o código de acesso da matrícula tenha a alteração liberada para
esta tela; não tendo, a tela avisa **\* Acesso negado para esta operacao \*** e nada é
apagado. A conferência é feita antes de o processo ser lido e antes de ser apagado.

### RN-07 — A exclusão é do grupo que a tela já carregou

Para excluir, o grupo informado tem de ser o mesmo que a tela carregou: o grupo da
matrícula, ou o grupo que a tela já consultou nesta sessão. Informando um grupo
diferente, a recusa é **\* Consulte antes de atualizar \*** e nada é apagado — é
preciso consultar o grupo antes de atualizá-lo. Quem não tem grupo na matrícula, por
isso, consulta o grupo primeiro e só depois consegue excluir.

### RN-08 — O operador alcança o grupo dele, ou um grupo da sua secretaria

Na consulta, quem tem grupo na matrícula só alcança aquele grupo: informando outro, a
recusa é **\* Usuario sem acesso a este grupo \***. Quem não tem grupo na matrícula
alcança os grupos da sua secretaria, e o grupo informado tem de estar cadastrado para
a secretaria da sessão: não estando, a recusa é
**\* Grupo nao pertence a esta secretaria \***. O grupo aceito passa a ser o grupo da
tela para as operações seguintes da sessão.

### RN-09 — Nada acontece sem a tela e a matrícula habilitadas

Antes de qualquer operação, inclusive ao abrir a tela, o sistema confere, com o
contexto da sessão, se a tela está cadastrada e se a matrícula tem a tela no seu
código de acesso; não estando, a recusa é **\* Tela nao disponivel \*** ou
**\* Acesso negado para esta matricula \***, e a operação não segue. A tela passa
ainda pela lógica de rota, que confere a opção e recusa a tela retirada do cadastro
(**\* Tela nao cadastrada \***) e a operação que não é nenhuma das previstas
(**\* Operacao nao disponivel \***).

### RN-10 — A lista é de sete em sete e retoma de onde parou

Cada abertura mostra até sete processos. O último processo mostrado fica como ponto
de partida da abertura seguinte, e quando a lista alcança o fim do grupo a abertura
seguinte recomeça do começo. A opção informada também fica guardada: a tela chega em
consulta, mas reabre com a opção da última operação do operador.

[?] O ponto de partida da lista e a opção ficam guardados numa área comum do processo,
que é inicializada uma única vez; o acervo não diz quando essa área é reiniciada — se
a cada sessão, se a cada dia, ou só quando o processo é carregado. Isso decide se a
próxima abertura continua a lista de onde parou e se reabre com a opção anterior.
Pergunta ao site.

### RN-11 — Informando o código de impressão, a tela pede a impressão da relação

Além da consulta e da exclusão, a tela aceita um **código de impressão**. Informado,
ela confere se o grupo tem processos e se já não existe um pedido de impressão
daquela relação em processamento — havendo, avisa
**\* Relatorio em processamento. Aguarde. \*** e não pede outro; não havendo
processos, avisa **\* Registros nao cadastrados \***. Passando as duas conferências, a
tela cria o pedido de impressão da relação do grupo, com o relatório, o código de
impressão, a matrícula, a CRE, a secretaria, o terminal e o dia e a hora, e aciona a
execução do relatório na hora.

[?] A conferência do pedido já em processamento fica só na passagem de conferência da
mensagem; o trecho que cria o pedido não a repete. Depende da rotina comum de
mensagem, que não está no lote, saber se o pedido deixa de ser criado. Pergunta ao
site.

[?] A execução do relatório só deixa de ser acionada se a gravação do pedido
devolver um estado que nenhum trecho do lote atribui. Se existe um caminho em que o
pedido é gravado e o relatório não roda, não se lê no acervo. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consulta e exclusão dos processos da CRE, com pedido de impressão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela P520T

  Cenário: Abertura mostra os processos do grupo
    Dado que o meu grupo tem processos cadastrados
    Quando abro a tela P520T
    Então vejo os processos do grupo, um por linha, com o número do processo, o valor, o número do empenho, o ano de referência, o dia e a hora da atualização e o tipo de anulação
    E nada é gravado

  Cenário: O grupo não tem processos
    Dado que o meu grupo não tem nenhum processo cadastrado
    Quando abro a tela P520T
    Então vejo a mensagem "* Nao existem processos a transmitir *"
    E nenhuma linha é mostrada
    E nada é gravado

  Cenário: A consulta não exclui nem altera processo
    Dado que o meu grupo tem processos cadastrados
    E assinalo um processo com a marca de exclusão
    Quando confirmo a mensagem com a opção de consulta
    Então nenhum processo é excluído nem alterado
    E nenhum dado é gravado

  Cenário: Opção diferente de consulta e alteração é recusada
    Dado que o meu grupo tem processos cadastrados
    Quando informo uma opção que não é a de consulta nem a de alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo da opção
    E nada é gravado

  Cenário: Exclusão do processo assinalado
    Dado que o processo da linha assinalada está cadastrado no meu grupo
    Quando confirmo a mensagem com a opção de alteração
    Então o processo é apagado do cadastro do grupo
    E fica registrada na auditoria a exclusão, com o processo como estava e com quem operou, a CRE, a secretaria, o terminal e o dia e a hora da sessão

  Cenário: Mais de uma linha assinalada é excluída
    Dado que assinalo dois processos cadastrados do meu grupo
    Quando confirmo a mensagem com a opção de alteração
    Então os dois processos são apagados
    E cada exclusão fica registrada na auditoria

  Cenário: Exclusão de processo não cadastrado é recusada
    Dado que o processo da linha assinalada não está cadastrado no meu grupo
    Quando confirmo a mensagem com a opção de alteração
    Então vejo a mensagem "* Registro nao cadastrado *"
    E o cursor fica na marca daquela linha
    E nada é apagado

  Cenário: Linha assinalada com outra marca é ignorada
    Dado que assinalo uma linha com uma marca que não é a de exclusão
    Quando confirmo a mensagem com a opção de alteração
    Então nada é apagado

  Cenário: Sem autorização de alteração, a tela não exclui
    Dado que o meu código de acesso não tem a alteração liberada para a tela P520T
    E assinalo um processo cadastrado do meu grupo
    Quando confirmo a mensagem com a opção de alteração
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é apagado

  Cenário: Alteração de um grupo que a tela não carregou é recusada
    Dado que informo um grupo diferente do grupo que a tela carregou
    E assinalo um processo com a marca de exclusão
    Quando confirmo a mensagem com a opção de alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor fica no campo do grupo
    E nada é apagado

  Cenário: Consulta de um grupo fora do meu acesso
    Dado que a minha matrícula tem um grupo
    Quando informo outro grupo e confirmo a mensagem com a opção de consulta
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo do grupo

  Cenário: Consulta de um grupo de outra secretaria
    Dado que a minha matrícula não tem grupo
    Quando informo um grupo que não pertence à secretaria da sessão
    Então vejo a mensagem "* Grupo nao pertence a esta secretaria *"
    E o cursor fica no campo do grupo

  Cenário: Consulta de um grupo da minha secretaria
    Dado que a minha matrícula não tem grupo
    E o grupo informado pertence à secretaria da sessão
    Quando confirmo a mensagem com a opção de consulta
    Então vejo os processos daquele grupo
    E o grupo passa a ser o grupo da tela

  Cenário: Tela não cadastrada
    Dado que a tela P520T não está no cadastro de telas e relatórios
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela P520T no seu código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Tela retirada do cadastro
    Dado que a tela P520T foi retirada do cadastro de telas e relatórios
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"

  Cenário: A lista é de sete em sete e continua na abertura seguinte
    Dado que o meu grupo tem mais de sete processos cadastrados
    Quando abro a tela P520T e depois a abro de novo
    Então a primeira abertura mostra até sete processos
    E a abertura seguinte continua a partir do último processo mostrado
    E ao alcançar o fim do grupo a abertura seguinte recomeça do primeiro processo

  Cenário: Pedido de impressão da relação do grupo
    Dado que o meu grupo tem processos cadastrados
    E não existe pedido de impressão da relação em processamento
    Quando informo o código de impressão e confirmo a mensagem
    Então a tela cria o pedido de impressão da relação do grupo
    E a execução do relatório é acionada

  Cenário: Pedido de impressão com relatório já em processamento
    Dado que já existe um pedido de impressão da relação do meu grupo em processamento
    Quando informo o código de impressão e confirmo a mensagem
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E nenhum pedido novo é criado

  Cenário: Pedido de impressão sem processos no grupo
    Dado que o meu grupo não tem processos cadastrados
    Quando informo o código de impressão e confirmo a mensagem
    Então vejo a mensagem "* Registros nao cadastrados *"
    E nenhum pedido novo é criado
```
