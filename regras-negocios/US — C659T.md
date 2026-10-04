# US — C659T — Permissão de períodos de estimativa do contrato

## Estória

Como **servidor de CRE**, quero **registrar ou retirar a permissão de uso dos
períodos do cálculo de estimativa de um contrato**, para que **o contrato fique
ligado apenas aos períodos de estimativa que a secretaria liberou, e não a
períodos que ninguém autorizou**.

O cálculo de estimativa é organizado por classe, subclasse e gênero e por
período, e não por contrato: o que liga um contrato — de um tipo de contrato e de
um fornecedor — a esses períodos é a permissão que esta tela controla. É por isso
que ela só aceita períodos que já existem no cadastro do órgão. E é por isso que
ela não grava a permissão na hora: confirmada a operação, ela apaga as permissões
de período do contrato, registra o pedido e avisa que o cadastro está sendo
atualizado, porque quem monta a permissão é o processamento.

## Contexto

Jornada S000M → C000M → C050M → C060M → C659T.

Ator: servidor de CRE — informa o tipo de contrato, o fornecedor, o período do
contrato, a vigência da tabela de referência e até três períodos de estimativa, e
registra ou retira a permissão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

O C000M, o C050M e o C060M são menus e não gravam nada. O contexto que a C659T
usa — matrícula, privilégio, tipo de órgão e coordenadoria regional — é o que a
entrada deixou na sessão; a tela não recalcula nada disso e nenhum dos menus lhe
deixa registro de negócio. O C060M, porém, encaminha também a operação que ele
mesmo tem em tela — e **esta tela a descarta**: ela se monta sempre com a opção de
inclusão (RN-01). Não há, no fonte, comparação com o código da tela que a chamou,
de modo que o comportamento desta tela **não muda conforme a origem**.

A jornada termina nesta tela. O que ela entrega de volta é ela mesma: concluída a
operação, ela se reabre em inclusão, já com o aviso do resultado (RN-16).

---

## Regras de negócio

### RN-01 — A tela abre em inclusão e só atende inclusão e exclusão

Ao ser montada, a tela repõe a opção de manutenção como **inclusão**, seja qual
for a tela que a chamou. A guarda da opção deixa passar dois caminhos — inclusão e
exclusão — e recusa os demais com
**\* Opcao nao disponivel. Use INC ou EXC \***, devolvendo o cursor ao campo da
opção, antes de ler cadastro nenhum. Não há modo de consulta nem de alteração
nesta tela.

[?] A recusa manda usar "INC" e "EXC", mas o sistema reconhece as operações por
códigos internos que o acervo escreve como "ADD" e "DEL"; nenhum valor "INC" ou
"EXC" existe no corpus lido como valor de operação. Ou o formulário traduz o que o
servidor digita, ou quem seguir a mensagem é recusado. Pergunta ao site.

[?] A tela é sempre montada com a inclusão, e a máscara do formulário não está no
acervo lido: como o operador chega à exclusão — se o campo da opção é digitável,
ou se a exclusão só se alcança por outro caminho — não está nos fontes desta
jornada. Se o campo não for digitável, todo o caminho da exclusão é inalcançável.
Pergunta ao site.

### RN-02 — O que o operador informa e o que a tela completa

O operador informa o **tipo de contrato**, o **código do fornecedor**, o **início
e o limite do período do contrato** — dia, mês e ano, em campos separados —, o
**limite da vigência da tabela de referência** e **até três períodos de
estimativa**, cada um com início e limite. O sistema completa com o que os
cadastros sabem: a **razão social do fornecedor**, o **início da vigência da
tabela de referência** e o **início de cada período de estimativa**.

Antes de qualquer leitura, **trinta e dois** campos passam pela edição numérica:
campo em branco vira zero, os zeros à esquerda são descartados e o que não for
número é recusado, sem que a conferência siga. Desses trinta e dois, **vinte** têm
posição de cursor definida para a devolução; os **doze** restantes — as três
partes do início da vigência da tabela e as nove do início dos três períodos de
estimativa — não têm.

[?] Os rótulos dos campos de fornecedor, de tabela de referência e de período de
estimativa não estão no acervo lido: a ficha da tela só registra os rótulos do
tipo de contrato e das duas datas do contrato. Como o formulário nomeia esses
campos é pergunta ao site.

[?] O que a rotina de edição recusa, além do não numérico — e se ela valida mês e
dia —, não está no acervo lido: ela é importada, não vem no lote. Pergunta ao
site.

### RN-03 — O tipo de contrato precisa estar cadastrado

Para incluir e para excluir, o tipo de contrato informado precisa existir no
cadastro dos tipos de contrato do órgão. Não existindo — ou existindo para outro
órgão —, o sistema recusa com **\* Tipo contrato nao cadastrado \*** e devolve o
cursor ao campo do tipo de contrato.

### RN-04 — A inclusão é recusada quando já há permissão vigente para o tipo de contrato

Antes das demais conferências da inclusão, o sistema percorre os registros daquele
tipo de contrato no órgão e, achando algum cujo limite seja **igual ou posterior**
ao início de período informado, recusa com
**\* Ja existe permissao para este tipo contrato \***. Os registros marcados como
excluídos ficam fora dessa leitura. Registro cujo limite seja anterior ao início
informado não recusa: a varredura segue para o registro seguinte.

[?] A varredura é feita com parte da chave de leitura zerada. Se zerar significa
"qualquer valor" — como sugerem as conferências seguintes, que só comparam os
campos que interessam —, a varredura alcança todas as coordenadorias e
fornecedores; se significar "exatamente zero", quase nenhuma dessas guardas
dispara e a RN-04, a RN-10 e a RN-11 mudam de sentido. Essa semântica é do
dialeto e não está explicada no acervo nem no manual. Pergunta ao site.

### RN-05 — O período inicial precisa ser uma data válida, de 1994 a 2099

O dia, o mês e o ano do início do período do contrato são conferidos como data:
data que não existe, ou ano fora da faixa de **1994 a 2099**, é recusado com
**\* Periodo inicial invalido \***, com o cursor de volta ao dia do início.

### RN-06 — O período limite precisa ser uma data válida e não anterior ao início

O limite do período é conferido como data; sendo inválido, a recusa é
**\* Periodo final invalido \***. Sendo válido e **anterior** ao início do
período, a recusa é **\* Data final menor que data inicial \***, com o cursor de
volta ao início. Data limite igual ao início é aceita.

### RN-07 — O fornecedor precisa estar cadastrado, e a razão social é mostrada

O código do fornecedor informado é procurado no cadastro de fornecedores; não
existindo, a recusa é **\* Fornecedor nao cadastrado \*** e o cursor volta ao
campo. Existindo, a razão social do fornecedor vem para a tela. O cadastro de
fornecedores não é por órgão: a chave dessa procura é só o código do fornecedor.

### RN-08 — A tabela de referência precisa existir para o período informado

O tipo de contrato informado traz um indicador que aponta **uma entre duas**
tabelas de referência. O sistema procura, na tabela indicada, o registro do
período informado — as três partes do limite da vigência, com a classificação em
branco — e confere as três partes do limite lido. Não achando, ou não havendo
indicação de tabela nenhuma, a recusa é
**\* Tabela de referencia nao cadastrada \***, com o cursor de volta ao limite da
vigência. Achando, o início da vigência que a tela mostra é o do registro
encontrado.

[?] O indicador do tipo de contrato tem dois valores possíveis e o acervo não diz
o que cada um significa; também não diz o que distingue as duas tabelas de
referência, que guardam os mesmos valores, a mesma chave e só mudam de capacidade.
Qual tabela vale para cada caso é pergunta ao site.

### RN-09 — É preciso informar ao menos um período de estimativa

Se os **anos** dos três períodos de estimativa vierem zerados, a inclusão é
recusada com **\* Informe periodos de estimativa \***, com o cursor no primeiro
período. A marca de "período informado" é o ano: informar só o dia ou só o mês,
sem o ano, não conta.

### RN-10 — Cada período informado precisa existir no cálculo de estimativa do órgão

Para cada período cujo ano tenha sido informado, o sistema percorre as
coordenadorias regionais do órgão procurando, no cadastro do cálculo de
estimativa, o registro daquele mesmo período limite, com a classificação em
branco. Não achando em nenhuma coordenadoria, recusa com
**\* Periodo de estimativa nao cadastrado \***, apontando o período recusado.
Achando, adota o **início do período que está no cadastro** e o mostra na tela: o
início que o operador tiver digitado nesse campo é descartado. A procura usa a
mesma chave com parte dos campos zerada e esbarra na mesma dúvida da RN-04.

### RN-11 — A inclusão é recusada quando já há permissão cadastrada para o contrato

O sistema percorre as coordenadorias regionais do órgão: se **qualquer uma**
tiver permissão cadastrada para o tipo de contrato informado, a inclusão é
recusada com **\* Permissao ja cadastrada para este contrato \*** e o cursor volta
ao tipo de contrato. A permissão é do órgão, não de uma coordenadoria específica:
basta uma.

### RN-12 — A operação só segue depois de confirmada, e com os mesmos dados

Passando por todas as conferências, o sistema guarda o que apurou e pergunta
**\* Confirma inclusao da permissao <S/N> ? \*** — na exclusão,
**\* Confirma exclusao da permissao <S/N> ? \***. Só a resposta **S** leva a
operação adiante; resposta diferente de S limpa a pergunta e refaz a conferência
desde o começo, sem gravar nada. Se, depois da pergunta, algum dos dados
informados for alterado, a confirmação é descartada e tudo é conferido outra vez.

[?] Respondendo N, o sistema volta à primeira conferência e pergunta de novo, e a
tela não tem saída própria para a operação: como o operador abandona a operação
sem confirmar é pergunta ao site.

[?] O início da vigência da tabela e o início de cada período de estimativa não
entram nessa comparação: redigitá-los depois da pergunta não descarta a
confirmação — e, de todo modo, o valor digitado é substituído pelo do cadastro
antes de a tela registrar o pedido. Ou esses campos deveriam ser só de exibição,
ou a guarda deveria incluí-los. Pergunta ao site.

### RN-13 — Um processamento já pedido para o órgão bloqueia nova confirmação

Na passagem da confirmação, o sistema procura na fila de pedidos de processamento
um pedido em andamento dessa mesma rotina para o órgão. Achando, recusa com
**\* Relatorio em processamento. Aguarde. \*** e devolve o cursor ao campo da
resposta.

[?] A recusa só emite a mensagem: quem marca o erro geral da transação é a rotina
de mensagem do ambiente, que é importada e não tem fonte no lote. Se essa rotina
não marcar, a passagem seguinte ainda registra a auditoria e o pedido. Se a recusa
interrompe a operação antes da gravação, o acervo lido não permite concluir.
Pergunta ao site.

### RN-14 — A exclusão exige permissão cadastrada e é recusada quando há registro do tipo de contrato

Para excluir, além de o tipo de contrato estar cadastrado (RN-03), duas
conferências precisam passar: o sistema **não** pode achar registro daquele tipo
de contrato no órgão — achando, recusa com
**\* Ja existe permissao para este tipo contrato \*** — e precisa achar permissão
cadastrada para aquele contrato em alguma coordenadoria regional do órgão — não
achando em nenhuma, recusa com
**\* Permissao nao cadastrada para este contrato \***, com o cursor de volta ao
tipo de contrato. Achando, o sistema adota o período da permissão encontrada e
pergunta a confirmação (RN-12).

[?] As duas conferências pedem coisas opostas: uma recusa quando o registro
daquele tipo de contrato **existe**, e a outra recusa quando a permissão do
contrato **não existe**. Se os dois registros andam juntos para o mesmo contrato,
a exclusão não tem caminho; se o primeiro é de outra natureza e pode faltar
enquanto o segundo existe, a exclusão passa. O acervo lido não diz o que
distingue os dois cadastros nem se eles andam juntos. Ou a primeira conferência
vale para outro caso, ou a exclusão está inalcançável por este caminho. Pergunta
ao site.

### RN-15 — Confirmada a operação, a tela apaga as permissões de período e registra o pedido

Confirmada a operação com **S**, na **inclusão** o sistema percorre as
coordenadorias regionais do órgão e apaga as permissões de período já registradas
para aquele tipo de contrato; na **exclusão** essa varredura não acontece. Em
seguida, nas duas operações, o sistema grava a **auditoria (A010T)** — com a tela,
o operador, a estação, a sessão, a data e a hora, o órgão, a coordenadoria
regional, a operação e o conteúdo anterior da permissão — e registra na **fila de
pedidos (S040T)** um pedido novo, com o número seguinte da fila, o código da
rotina, o tipo de órgão, a coordenadoria, o tipo de contrato, o fornecedor, o
período do contrato, a vigência da tabela e os três períodos de estimativa. O
pedido é então entregue ao processamento, e a tela mostra
**\* Cadastro sendo atualizado \***.

[?] O conteúdo posterior da auditoria vai em branco: o lançamento guarda os dados
informados como conteúdo anterior e não guarda o resultado da operação. Se quem
lê a trilha espera o antes e o depois, o caminho não produz o depois. Pergunta ao
site.

[?] A entrega do pedido à fila de processamento está sob um estado interno que o
acervo não atribui em ponto nenhum e sob o produto em execução não ser o LINC; o
que a tela faz no caso contrário, e se existe caminho em que o pedido é registrado
sem o processamento ser entregue, não está nos fontes desta jornada. Pergunta ao
site.

### RN-16 — A tela não grava a permissão, e reabre a si mesma

A tela **não cria nem altera** o cadastro da permissão nem o do cálculo de
estimativa: o que ela executa são **duas gravações** — a auditoria e o pedido de
processamento — e **uma exclusão** — as permissões de período do contrato, e só
na inclusão. A permissão em si, o contrato ligado aos períodos, é montada depois,
pelo processamento que o pedido dispara. Concluída a operação, a tela reabre a si
mesma, já em inclusão (RN-01) e com o aviso **\* Cadastro sendo atualizado \*** —
é essa reabertura que devolve o resultado ao operador.

[?] O acervo não tem o programa que atende esse pedido: o código de processamento
que a tela registra não aparece em nenhum outro fonte do lote, e o processamento
que ela entrega é o mesmo nome usado por dezenas de outras telas. O que o
processamento faz com os dados — e se ele de fato grava a permissão — não está
sustentado nesta jornada. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Permissão de períodos de estimativa do contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C659T

  Cenário: RN-01 — a tela abre em inclusão
    Dado que abro a tela C659T
    Então a opção de manutenção vem marcada como inclusão
    E eu não escolho a operação

  Cenário: RN-01 — opção diferente de inclusão e de exclusão
    Dado que estou na tela C659T
    Quando envio com uma opção diferente de inclusão e de exclusão
    Então vejo "* Opcao nao disponivel. Use INC ou EXC *"
    E o cursor volta ao campo da opção
    E nenhum cadastro é lido nesse caminho
    E nada é gravado

  Cenário: RN-02 — o que o operador informa e o que a tela completa
    Dado que estou na tela C659T
    E informo um tipo de contrato cadastrado, um fornecedor cadastrado, o início e o limite do período do contrato, a vigência da tabela de referência e um período de estimativa existente no cadastro do órgão
    Quando envio
    Então a tela me mostra a razão social do fornecedor, o início da vigência da tabela e o início do período de estimativa
    E me pergunta a confirmação

  Cenário: RN-02 — campo numérico inválido
    Dado que estou na tela C659T
    Quando informo, num campo de data, código ou período, algo que não é número
    Então a edição recusa o campo antes de qualquer leitura
    E o cursor volta ao campo quando a tela tem posição definida para ele

  Cenário: RN-03 — tipo de contrato não cadastrado
    Dado que estou na tela C659T
    Quando informo um tipo de contrato que não existe no cadastro do órgão
    Então vejo "* Tipo contrato nao cadastrado *"
    E o cursor volta ao tipo de contrato
    E nada é gravado

  Cenário: RN-04 — inclusão recusada porque já há permissão vigente para o tipo de contrato
    Dado que existe registro daquele tipo de contrato com limite igual ou posterior ao início de período informado
    Quando tento incluir
    Então vejo "* Ja existe permissao para este tipo contrato *"
    E nada é gravado

  Cenário: RN-05 — período inicial inválido
    Dado que informei uma data de início que não existe ou um ano fora de 1994 a 2099
    Quando tento incluir
    Então vejo "* Periodo inicial invalido *"
    E o cursor volta ao dia do início
    E nada é gravado

  Cenário: RN-06 — período limite inválido
    Dado que informei uma data limite que não existe
    Quando tento incluir
    Então vejo "* Periodo final invalido *"
    E nada é gravado

  Cenário: RN-06 — data limite anterior ao início do período
    Dado que a data limite informada é anterior ao início do período
    Quando tento incluir
    Então vejo "* Data final menor que data inicial *"
    E o cursor volta ao início do período
    E nada é gravado

  Cenário: RN-07 — fornecedor não cadastrado
    Dado que informei um código de fornecedor que não existe
    Quando tento incluir
    Então vejo "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo do fornecedor
    E nada é gravado

  Cenário: RN-08 — tabela de referência não cadastrada para o período
    Dado que o tipo de contrato não indica nenhuma tabela de referência, ou que não há tabela para o limite de vigência informado
    Quando tento incluir
    Então vejo "* Tabela de referencia nao cadastrada *"
    E o cursor volta ao limite da vigência
    E nada é gravado

  Cenário: RN-09 — nenhum período de estimativa informado
    Dado que não informei o ano de nenhum dos três períodos de estimativa
    Quando tento incluir
    Então vejo "* Informe periodos de estimativa *"
    E o cursor vai para o primeiro período
    E nada é gravado

  Cenário: RN-10 — período de estimativa não cadastrado
    Dado que informei um período de estimativa que não existe em nenhuma coordenadoria regional do órgão
    Quando tento incluir
    Então vejo "* Periodo de estimativa nao cadastrado *"
    E o cursor vai para o período recusado
    E nada é gravado

  Cenário: RN-10 — o início do período vem do cadastro
    Dado que informei o limite de um período de estimativa existente no cadastro do órgão
    E que digitei também um início para esse período
    Quando tento incluir
    Então a tela mostra como início do período o que está no cadastro
    E o início que digitei é descartado

  Cenário: RN-11 — permissão já cadastrada para o contrato
    Dado que alguma coordenadoria regional do órgão já tem permissão cadastrada para aquele tipo de contrato
    Quando tento incluir
    Então vejo "* Permissao ja cadastrada para este contrato *"
    E o cursor volta ao tipo de contrato
    E nada é gravado

  Cenário: RN-12 — o operador não confirma a inclusão
    Dado que o sistema pediu a confirmação da inclusão
    Quando respondo algo diferente de S
    Então a pergunta é limpa e a conferência recomeça
    E nada é gravado

  Cenário: RN-12 — o operador altera os dados depois da confirmação
    Dado que o sistema pediu a confirmação da operação
    Quando altero algum dos dados informados e envio
    Então a confirmação é descartada
    E os dados são conferidos outra vez
    E nada é gravado

  Cenário: RN-13 — já existe processamento em andamento para o órgão
    Dado que o órgão já tem um pedido de processamento em andamento para esta mesma rotina
    Quando confirmo a operação
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor fica no campo da resposta

  Cenário: RN-14 — exclusão recusada porque há registro do tipo de contrato
    Dado que existe registro daquele tipo de contrato no órgão
    Quando tento excluir
    Então vejo "* Ja existe permissao para este tipo contrato *"
    E nada é gravado

  Cenário: RN-14 — exclusão de permissão não cadastrada
    Dado que nenhuma coordenadoria regional do órgão tem permissão cadastrada para aquele contrato
    Quando tento excluir
    Então vejo "* Permissao nao cadastrada para este contrato *"
    E o cursor volta ao tipo de contrato
    E nada é gravado

  Cenário: RN-12 e RN-15 — inclusão confirmada
    Dado que informei um tipo de contrato cadastrado, um fornecedor cadastrado, um período de contrato válido, a vigência da tabela de referência e um período de estimativa existente
    Quando confirmo a inclusão com S
    Então as permissões de período anteriores daquele contrato são apagadas em todas as coordenadorias regionais do órgão
    E a operação fica registrada na auditoria
    E o pedido de processamento é registrado na fila com os dados informados
    E o processamento é entregue
    E vejo a mensagem "* Cadastro sendo atualizado *"

  Cenário: RN-15 — exclusão confirmada
    Dado que existe permissão cadastrada para o contrato em alguma coordenadoria regional e não existe registro daquele tipo de contrato
    Quando confirmo a exclusão com S
    Então as permissões de período do contrato não são apagadas por esta operação
    E a operação fica registrada na auditoria
    E o pedido de processamento é registrado na fila
    E vejo a mensagem "* Cadastro sendo atualizado *"

  Cenário: RN-16 — a tela reabre a si mesma depois da operação
    Dado que confirmei uma operação
    Quando a tela devolve o resultado
    Então ela se reabre na mesma tela, em inclusão
    E eu vejo o aviso "* Cadastro sendo atualizado *"

  Cenário: RN-16 — a tela não grava a permissão
    Dado que confirmo uma inclusão
    Então o cadastro da permissão e o do cálculo de estimativa não são criados nem alterados por esta tela
    E o que a tela grava é a auditoria e o pedido de processamento
    E a permissão fica por conta do processamento entregue
```
