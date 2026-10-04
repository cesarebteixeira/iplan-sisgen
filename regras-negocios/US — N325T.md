# US — N325T — Encaminhamento à nota fiscal informada

## Estória

Como **servidor de CRE**, quero **informar o número da nota fiscal e o operador
logístico e ser encaminhado à tela que detalha aquela nota**, para que **eu chegue ao
detalhe certo — a consulta da nota e dos gêneros entregues, ou a tela em que os
gêneros da nota são tratados — sem precisar saber de antemão em que ponto da vida da
nota ela está**.

Uma nota fiscal, no sistema, vive em dois registros: o das notas cuja entrega já foi
confirmada e o das notas apenas registradas. Cada registro tem a sua tela de detalhe, e
é esta tela que decide qual delas abre, a partir do número da nota e do operador
logístico. Sem ela, quem sabe o número da nota não tem por onde chegar ao detalhe sem
passar antes pela consulta por contrato — e a nota cuja entrega já está confirmada não
admite mais mexer nos gêneros, só consulta.

## Contexto

Jornada S000M → N000M → N050M → N300M → N325T.

Ator: servidor de CRE — informa o número da nota fiscal e o operador logístico e é
encaminhado à tela que detalha aquela nota.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As três telas anteriores do caminho — `N000M`, `N050M` e `N300M` — são menus, e nenhuma
delas encadeia na tela desta jornada: a `N325T` é aberta pela opção correspondente do
menu `N300M`. O que a `N325T` usa da sessão — o tipo de órgão, a coordenadoria regional
de ensino, o órgão filho, a matrícula e o privilégio — é o que a entrada deixou.

A `N325T` **não é folha**: ela encadeia, sem passar por menu, na consulta da nota e dos
gêneros (`N326T`) ou na tela dos gêneros da nota (`N324T`), conforme o registro em que a
nota é encontrada. O que ela entrega à tela seguinte está na RN-10.

A tela só é alcançada pelo menu: nenhuma outra tela do acervo a chama, e o único campo
de origem que o programa examina é o de próxima tela, que o próprio servidor informa
(RN-01).

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela abre em consulta, e consulta é a única operação que ela aceita

A tela recebe a operação já posta como consulta. Confirmando com qualquer outra
operação, o sistema recusa com **\* Operacao nao disponivel. Use CON \***, deixa o
cursor no campo da operação e não processa nada: não lê cadastro nenhum e não encaminha
o servidor a tela alguma. Indicando o servidor o código de outra tela no campo de
próxima tela, a confirmação também é abandonada sem processar nada, e o encaminhamento
passa a ser o que ele pediu.

[?] O aviso manda usar **CON**, mas o valor que o programa aceita como consulta é o
código interno dela, que o gerador exibe como a letra **I**; não há, no acervo, conversão
de um no outro. O que o servidor precisa digitar para ser aceito fica sem resposta.
Pergunta ao site.

### RN-02 — O que a tela mostra

Ao abrir, a tela trabalha sobre a nota que a sessão já carrega e mostra, dela, o número
da nota fiscal, o número do processo, a data de entrega, a coordenadoria regional de
ensino, o código e o nome do órgão, o tipo de contrato, o número do pedido e o ano da
entrega. Fora da lista aparecem o código e o nome do operador logístico, a descrição do
tipo de órgão e a data do sistema.

O nome do órgão e o pedido com o ano da entrega não vêm da nota: são buscados nos
cadastros de órgãos e de itens da nota. A data de entrega é montada a partir do dia, do
mês e do ano da nota fiscal. O número do processo é exibido já separado por barras a
partir do número do processo que a nota carrega. A coluna da situação de cada linha
existe na tela e é copiada para o registro da transação, mas o programa nunca a lê nem
a escreve.

[?] A tela comporta **12 linhas** e o programa percorre as 12 passadas, mas não há, no
que esta tela executa, contador de passada em uso: o campo de passada é zerado e nunca
lido. O que a tela faz quando a nota tem mais de 12 linhas fica sem resposta. Pergunta
ao site.

### RN-03 — A nota que a sessão carrega e não existe é avisada na abertura

Ao abrir com uma nota na sessão, o sistema projeta essa nota no registro das notas com
entrega confirmada. Não achando, avisa **\* Nota fiscal nao cadastrada \*** e não monta
os dados da nota.

### RN-04 — Sem nota na sessão, a tela abre sem nota e sem aviso

Se a sessão não carrega número de nota nenhum, a tela abre sem procurar cadastro e sem
avisar nada: o servidor digita o número da nota e o operador logístico e confirma.

### RN-05 — A conferência dos campos antes de processar

Ao confirmar, o sistema confere **três** campos, tratando cada um como número e exigindo
que caiba no tamanho dele: o número da nota fiscal (9 dígitos), o código do operador
logístico (4) e a coordenadoria regional de ensino (2). Campo em branco vira zero e os
zeros à esquerda são descartados. O conteúdo não numérico é recusado e o cursor volta ao
campo — para o número da nota e para o operador logístico; para a coordenadoria o
programa não define posição de cursor.

Os **oito** campos que a tela preenche a partir dos cadastros são limpos a cada entrada:
a descrição do tipo de órgão, a data do sistema, o número do processo, o órgão filho, o
nome do órgão, o tipo de contrato, o pedido e o ano do pedido.

[?] A coordenadoria regional de ensino é conferida a cada passada e nunca é usada: a nota
é procurada apenas pelo tipo de órgão da sessão, pelo operador logístico e pelo número.
Se a coordenadoria digitada deveria limitar a procura, o acervo não diz. Pergunta ao
site.

### RN-06 — O número da nota é obrigatório

Com o número da nota em branco na confirmação, a recusa é
**\* Informe o numero da nota fiscal \***, com o cursor de volta ao campo do número, e
nada mais é lido.

### RN-07 — O operador logístico tem de estar cadastrado

O operador informado é procurado no cadastro de operadores logísticos. Não existindo —
inclusive em branco —, a recusa é **\* Oper.logistico nao cadastrado \***, com o cursor
de volta ao campo do operador, e nada mais é lido.

### RN-08 — A nota encontrada decide a tela seguinte

Passadas as conferências, o sistema procura a nota pelo tipo de órgão da sessão, pelo
operador logístico informado e pelo número informado. Achando a nota no registro das
notas com **entrega confirmada**, o servidor é levado à tela de consulta da nota e dos
gêneros entregues (a `N326T`). Não achando ali, o sistema procura a nota no registro das
notas fiscais e, achando, leva o servidor à tela dos gêneros da nota (a `N324T`), onde os
gêneros e as quantidades da nota são tratados.

Nos dois desfechos a tela seguinte abre em **consulta**.

### RN-09 — Nota que não está em nenhum dos dois registros

Não achando a nota em nenhum dos dois registros, a confirmação termina sem aviso nenhum:
nada é gravado, nenhuma tela é aberta e o servidor continua na tela, com o que digitou.

[?] A abertura avisa **\* Nota fiscal nao cadastrada \*** quando não acha a nota que a
sessão carrega, mas a confirmação, na mesma situação, não avisa nada. Se a confirmação
deveria dar o mesmo aviso, o acervo não diz. Pergunta ao site.

### RN-10 — O que a tela entrega à tela seguinte

Antes de encaminhar, a tela deixa na sessão os dados da nota que encontrou e a marcação
de origem que a tela seguinte exige. Da nota saem o número, o número da nota de
modificação e a sua descrição, o ano da nota, o dia e o mês da nota, o fornecedor, a
razão social do fornecedor, a coordenadoria regional de ensino, o tipo de contrato, o
órgão filho e o seu nome, o operador logístico e o seu nome, a chave de acesso da nota e
as três partes da data de emissão; do item da nota saem o número do pedido e o ano da
entrega. A operação vai marcada como consulta, e a tela seguinte fica sabendo de qual
das duas telas irmãs ela é a continuação.

[?] A marcação de origem que esta tela deixa é o código `N314T` — o mesmo que a consulta
de notas fiscais e o cadastro da nota deixam — e não o dela própria. A tela seguinte
confere essa marcação ao abrir, mas apaga o mesmo campo ao inicializar: se a marcação
sobrevive até a conferência, o acervo não decide. Pergunta ao site.

### RN-11 — A consulta não grava nada

A tela não inclui, não altera e não exclui: as únicas operações que executa sobre os nove
cadastros que enxerga são leituras. Os caminhos de gravação e de exclusão que o programa
declara para esses cadastros não são executados em nenhum ponto do fluxo, e nenhum
registro de auditoria sai desta tela.

### RN-12 — A operação depende da autorização do usuário

Na abertura, o sistema confere a permissão do usuário para a tela; na confirmação,
confere a rota e a autorização da operação, com o contexto da sessão — matrícula, código
de acesso, privilégio, tipo de órgão e coordenadoria. Não estando autorizado, a tela não
é montada ou a operação é abandonada sem processar nada.

---

## Cenários BDD

```gherkin
Funcionalidade: Informar a nota fiscal e o operador logístico e ser levado à tela que detalha a nota

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N325T

  Cenário: A tela abre com a nota que a sessão carrega
    Dado que a sessão já carrega uma nota fiscal
    Quando a tela N325T abre
    Então vejo o número da nota, o número do processo, a data de entrega, a
      coordenadoria regional de ensino, o órgão e o seu nome, o tipo de contrato, o
      pedido e o ano da entrega
    E vejo o código e o nome do operador logístico, a descrição do tipo de órgão e a
      data do sistema

  Cenário: A tela abre sem nota quando a sessão não carrega nenhuma
    Dado que a sessão não carrega nota fiscal nenhuma
    Quando a tela N325T abre
    Então a tela abre sem procurar cadastro e sem me avisar nada
    E eu digito o número da nota e o operador logístico

  Cenário: A nota que a sessão carrega não está cadastrada
    Dado que a sessão carrega uma nota que não existe no registro das notas com
      entrega confirmada
    Quando a tela N325T abre
    Então vejo a mensagem "* Nota fiscal nao cadastrada *"
    E os dados da nota não são montados

  Cenário: A nota com entrega confirmada é levada à consulta da nota
    Dado que a nota informada está no registro das notas com entrega confirmada
    Quando confirmo a consulta
    Então sou levado à tela N326T
    E ela abre em consulta, com os dados da nota que esta tela deixou na sessão

  Cenário: A nota apenas registrada é levada à tela dos gêneros
    Dado que a nota informada não está no registro das notas com entrega confirmada
    E está no registro das notas fiscais
    Quando confirmo a consulta
    Então sou levado à tela N324T
    E ela abre em consulta, com os dados da nota que esta tela deixou na sessão

  Cenário: A nota não está em nenhum dos dois registros
    Dado que a nota informada não existe em nenhum dos dois registros de nota
    Quando confirmo a consulta
    Então nada é gravado, nenhuma tela é aberta e não vejo aviso nenhum
    E continuo na tela, com o que digitei

  Cenário: Nada é gravado na consulta
    Dado que estou na N325T
    Quando confirmo a consulta
    Então nenhum cadastro é gravado, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Operação diferente da consulta é recusada
    Dado que estou na N325T
    Quando confirmo com uma operação diferente da de consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nada é lido e nada é gravado

  Cenário: O número da nota não foi informado
    Dado que deixei o número da nota fiscal em branco
    Quando confirmo a consulta
    Então vejo a mensagem "* Informe o numero da nota fiscal *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: O operador logístico não está cadastrado
    Dado que informei um operador logístico que não existe no cadastro
    Quando confirmo a consulta
    Então vejo a mensagem "* Oper.logistico nao cadastrado *"
    E o cursor volta ao campo do operador logístico
    E nada é gravado

  Cenário: Informando outra tela no campo de próxima tela
    Dado que informei o código de outra tela no campo de próxima tela
    Quando confirmo
    Então a confirmação é abandonada sem processar nada
    E o encaminhamento é o que eu pedi

  Cenário: Campo não numérico é recusado na confirmação
    Dado que digitei letras no número da nota, no operador logístico ou na
      coordenadoria regional de ensino
    Quando confirmo
    Então o campo é marcado e o cursor volta para ele, quando há posição definida
    E nada é processado

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não autoriza esta operação
    Quando confirmo
    Então o sistema abandona a operação sem processar nada
    E nada é gravado
```
