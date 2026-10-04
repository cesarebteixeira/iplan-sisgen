# US — C064T — Estorno do apostilamento por item das permissões da CRE

## Estória

Como **servidor da Coordenação Regional de Ensino**, quero **desfazer uma rodada de apostilamento
das permissões da minha coordenação regional**, para que o valor apostilado volte ao valor da
permissão e o contrato pare de contabilizar um apostilamento que não vale mais.

O apostilamento é o registro posterior que atualiza o valor de uma permissão de fornecimento, e é
lançado item a item — por classe, por subclasse e por gênero do objeto. Desfazer uma rodada não é
só deixá-la de lado: enquanto os itens existirem, o valor deles continua somado ao valor apostilado
da permissão e ao total apostilado do contrato. Esta tela mostra os itens apostilados de um
contrato numa data, apaga-os e devolve o valor à permissão, recalculando o total. Sem ela, um
apostilamento lançado por engano só sairia por intervenção direta na base.

## Contexto

Jornada S000M → C000M → C050M → C066M → C064T.
Ator: servidor de CRE — consulta e desfaz o apostilamento por item das permissões da sua
coordenação regional, por contrato e por data.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

A tela é aberta por uma opção de menu e não recebe registro nem operação de tela anterior: sem
operação informada, ela abre em consulta. O tipo de órgão e a coordenação regional vêm do vínculo
escolhido na entrada, e é isso que esta tela consome da jornada. Esta é a terceira tela do mesmo
menu a tratar do mesmo cadastro: uma lança o apostilamento por item, outra o consulta e esta o
estorna.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — Esta tela estorna o apostilamento por item; ela não lança nem altera apostilamento

A tela não cria nem altera item de apostilamento: o que ela faz é apagar os itens de uma rodada e
devolver o valor deles à permissão. Ela enxerga oito cadastros — fornecedores, títulos de tela,
tipo de órgão, apostilamento por item, gênero, permissão de contrato, tipo de licitação e a trilha
de auditoria —, e grava em apenas dois: apaga no apostilamento por item e regrava, na permissão de
contrato, o valor apostilado e o total apostilado; cada operação deixa também o seu registro na
trilha de auditoria. Para cada cadastro que enxerga, o sistema traz prontas uma operação de gravar
e uma de apagar; aqui só as duas acima são executadas.

Os números de capacidade são de dimensionamento, não volume cadastrado: a permissão de contrato e
o apostilamento por item comportam um milhão de registros cada um; o gênero, cento e cinquenta
mil; o fornecedor, dez mil; o título, dois mil; o tipo de licitação, mil; o tipo de órgão,
duzentos; e a trilha de auditoria, sessenta milhões.

[?] O campo de situação desta tela tem um caractere só, não tem rótulo validado como os demais
campos e o sistema nunca o escreve: a marca **S** — a única que dispara a exclusão — é digitação do
servidor, e o material não diz se ela significa "sim", "excluir" ou outra coisa.

### RN-02 — O contrato e a rodada são identificados pela coordenação regional, pelo tipo de contrato, pelo grupo de licitação, pelo período e pela data de atualização

O que se informa para chegar a um contrato é a coordenação regional, o tipo de contrato, o grupo de
licitação e a data limite do período — dia, mês e ano. O tipo de órgão não se digita: é o da
secretaria escolhida no vínculo da matrícula, na entrada, e entra na identificação de tudo o que a
tela lê e apaga. O fornecedor e o tipo de licitação aparecem no cabeçalho, mas não identificam
nada: não fazem parte da identificação do apostilamento nem das conferências da tela. O item de
apostilamento é identificado, além dos dados acima, pela data de atualização e pelos três códigos
do item — classe, subclasse e gênero.

[?] A tela procura o apostilamento com os três códigos do item e a data de atualização zerados e
depois confere de volta só as sete partes do contrato, sem os códigos nem a data. Se a procura
exigir o item exato, um contrato com os códigos preenchidos não seria achado; se ela se posicionar
no item igual ou seguinte, a tela pode estar respondendo por mais de um. Pergunta ao site.

### RN-03 — A data de atualização diz qual rodada de apostilamento está em tela

Cada item de apostilamento tem uma data de atualização, e é ela que separa uma rodada de outra: a
tela mostra, e depois apaga, só os itens cuja data de atualização é a informada. Sem essa data, a
tela não sabe de qual rodada se trata. A data é informada em três partes — dia, mês e ano — e o
sistema a monta como ano, mês e dia. A data-base mostrada em cada linha é outro dado, do próprio
item, e não se digita.

### RN-04 — A lista tem nove linhas, uma por item de apostilamento

A lista da tela tem nove linhas. Cada linha é um item de apostilamento: os códigos de classe, de
subclasse e de gênero, a descrição resumida do gênero, a data-base e o valor apostilado. A
descrição resumida é a do gênero vigente na data de início do período e vem do cadastro de
gêneros; não achando, a linha fica sem ela. Fora da lista existe **um único** campo de situação,
para a tela inteira — não há marca por linha.

### RN-05 — O cabeçalho mostra o órgão, o contrato, o fornecedor, o tipo de licitação e o total apostilado

No cabeçalho a tela mostra a descrição do tipo de órgão da sessão e a data do sistema; a
coordenação regional, o tipo de contrato, o grupo de licitação e as três partes da data limite
informados; o fornecedor — o código e o nome — e o tipo de licitação — o código e a descrição —
que constam do apostilamento; e o total apostilado do contrato. A data de início do período não se
digita: achada a permissão, ela é reposta do cadastro. O total apostilado é o do contrato inteiro,
não a soma das linhas mostradas.

### RN-06 — A tela abre em consulta e só aceita consulta e alteração

Aberta sem nada guardado na sessão, a tela assume a **consulta**. Se a operação informada não for a
de alteração nem a de consulta, o sistema recusa com **\* Opcao nao disponivel. User ALT ou CON \***
e devolve o cursor ao campo da opção. Uma operação que o sistema não conhece é recusada antes
disso, pelo roteamento, com **\* Operacao nao disponivel \***, e a transação não segue.

[?] A recusa nomeia as operações como ALT e CON, e a conferência da tela compara o que foi digitado
com o nome da alteração e o da consulta que o sistema carrega da tabela de textos do idioma — a
mesma tabela de onde pode sair o próprio texto da mensagem. Os textos dessa tabela não fazem parte
do lote, de modo que não pude ler o nome literal: se a tabela não trouxer ALT e CON, a mensagem e a
conferência discordam. Pergunta ao site.

### RN-07 — O acesso passa pela segurança, e a alteração depende do perfil de alteração

Antes de ler qualquer cadastro, a tela pede ao sistema de segurança que confira a matrícula do
servidor, a estação, a tela e o código de acesso do vínculo. Sem a tela cadastrada, a operação é
recusada com **\* Tela nao disponivel \***; sem o acesso cadastrado, com **\* Acesso negado para
esta matricula \***. Na conferência do que foi informado, o sistema confere a operação e exige o
flag próprio de cada uma: a alteração exige o flag de alteração, e sem ele a recusa é **\* Acesso
negado para esta operacao \***. A segurança recebe o contexto da sessão: o tipo de órgão, a
matrícula, o código de acesso, o privilégio, a coordenação regional e a operação.

[?] A conferência da operação só examina inclusão, alteração e exclusão: a consulta não passa por
nenhum desses flags. Como esta tela só grava na alteração, a consequência é pequena — mas o
material não diz se a consulta é livre por desenho ou se a conferência ficou incompleta.

### RN-08 — A coordenação regional da sessão limita o que pode ser estornado

Quando a sessão tem coordenação regional, a coordenação regional informada tem de ser a mesma da
sessão; sendo outra, a operação é recusada com **\* Usuario sem acesso a este grupo \*** e o cursor
volta ao campo. Quando a sessão não tem coordenação regional, essa conferência não é feita.

[?] A conferência compara o que foi informado com um segundo contexto de sessão, paralelo ao que
traz a coordenação regional do usuário, e nenhuma tela desta jornada escreve nele: se ele chega
zerado ou com valor deixado por outra tela, a conferência recusa o que deveria aceitar. É a mesma
conferência, na mesma forma, em outras telas do acervo; o material não diz quem preenche esse
segundo contexto.

### RN-09 — Na consulta, a permissão e o apostilamento da data precisam existir

Confirmada a consulta, o sistema procura a permissão do contrato informado. Não existindo, a
consulta é recusada com **\* Permissao nao cadastrada \***, com o cursor de volta ao campo da
coordenação regional, e nada é mostrado. Existindo, o sistema procura o apostilamento daquela data
de atualização; não existindo, recusa com **\* Apostilamento nao cad. para esta data \***.

[?] Repetindo exatamente a mesma consulta, a tela não refaz essas duas conferências: aproveita o
que ficou guardado da vez anterior. Se um cadastro mudou entre as duas vezes, a repetição não
percebe.

### RN-10 — Não havendo item para a data, a lista fica vazia e o sistema avisa

Quando não há item de apostilamento para a data em tela, as nove linhas ficam vazias e o sistema
avisa **\* Permiss. sem apostilamento para esta data \***.

### RN-11 — Na alteração só se estorna o que foi consultado

A alteração não trabalha sobre um contrato desconhecido: ela só segue se as nove partes informadas
— a coordenação regional, o tipo de contrato, o grupo de licitação, as três da data limite e as
três da data de atualização — forem exatamente as da última consulta. Mudando qualquer uma delas,
a operação é recusada com **\* Consulte antes da atualizacao \***, com o cursor de volta ao campo da
coordenação regional, e nada é apagado.

### RN-12 — O estorno apaga os itens da data e devolve o valor à permissão

A alteração só age quando o campo de situação está marcado com **S**; com qualquer outro valor, a
tela termina sem apagar nada. Marcado, o sistema percorre o apostilamento **do contrato inteiro
naquela data de atualização** — não as linhas marcadas, porque não há marca por linha — e, para
cada item: apaga o item e subtrai o valor dele do valor apostilado da permissão daquele item,
regravando a permissão. No fim, recalcula o total apostilado do contrato como a soma dos valores
apostilados das permissões do contrato e regrava esse total em cada uma delas — mesmo quando não
havia item nenhum para apagar naquela data. A conta usa o valor que está no cadastro: a tela não
pede nem aceita valor.

[?] No modo de alteração a tela não confere se a permissão do item existe — essa conferência só é
feita na consulta. Há no fonte um caminho que manda apagar o item sem baixar o valor quando a
permissão não é achada; se ele for alcançável pelo terminal, o item sai e o valor fica. Pergunta ao
site.

[?] O recálculo do total acontece também quando não havia item nenhum para apagar, alcançando
todas as permissões do contrato. Se a intenção era recalcular só o que mudou, o material não diz.

### RN-13 — A consulta não grava nada

Na consulta, o sistema lê e para: nenhum item é apagado e nenhum valor é regravado, mesmo que o
campo de situação esteja marcado.

### RN-14 — Cada exclusão e cada regravação ficam registradas na auditoria

Cada item apagado e cada permissão regravada — o valor apostilado e o total apostilado — deixam um
registro na trilha de auditoria, com o cadastro de origem, a operação, o conteúdo anterior e o
conteúdo posterior, a matrícula do funcionário, a estação, o número do processo, o dia, o mês e a
hora da sessão, o tipo de órgão e a coordenação regional. As regravações do total, que alcançam
todas as permissões do contrato, também geram um registro cada uma.

[?] O registro de auditoria declara sempre a mesma situação de manutenção, qualquer que tenha sido
a operação registrada. Se esse campo é a operação ou outra coisa, o material não diz.

### RN-15 — O que se digita é conferido: os campos são numéricos e o fornecedor informado precisa estar cadastrado

Nenhum campo desta tela é texto livre: a coordenação regional, o tipo de contrato, o fornecedor, o
grupo de licitação, as três partes do início do período, as três partes da data limite, as três
partes da data de atualização, o tipo de licitação e os três códigos de item de cada linha passam
pela edição numérica antes de qualquer leitura — são **dezessete** os campos com rótulo que passam
por essa edição; o que não for número é recusado no próprio campo, com o cursor de volta a ele.
Além disso, o código de fornecedor informado é procurado no cadastro de fornecedores: não achado —
ou achado em situação que a tela não aceita —, a operação é recusada com a mensagem de cadastro do
sistema e nada é lido.

[?] O texto dessa recusa não está no material: a mensagem sai da tabela de textos do idioma, que
não faz parte do lote. Também não pude conferir **o que** o usuário vê quando a edição numérica
recusa o campo: o que a tela chama está fora do acervo desta jornada.

[?] O material desta tela é uma expansão com opções de compilação assumidas e cinquenta e duas
linhas descartadas na geração. Se houver regra de negócio em algum desses trechos, ela não está
nesta jornada.

---

## Cenários BDD

```gherkin
Funcionalidade: Estorno do apostilamento por item das permissões da CRE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenação regional, a matrícula, o código de acesso, o privilégio e a data do sistema
    E tenho acesso à tela C064T

  Cenário: RN-02, RN-03, RN-04, RN-05 e RN-13 — consultar o apostilamento de uma data
    Dado que existe permissão de contrato da minha coordenação regional, para o tipo de contrato, o grupo de licitação e a data limite que informei
    E que há apostilamento para a data de atualização que informei
    Quando confirmo a consulta
    Então vejo no cabeçalho a descrição do meu tipo de órgão, a data do sistema, o fornecedor, o tipo de licitação e o total apostilado do contrato
    E vejo até nove linhas, cada uma com a classe, a subclasse, o gênero, a descrição resumida do gênero, a data-base e o valor apostilado daquele item
    E nada é apagado e nenhum valor é regravado

  Cenário: RN-13 — a consulta não grava nada
    Dado que os itens estão em tela
    Quando confirmo a consulta quantas vezes quiser, mesmo com o campo de situação marcado
    Então os itens continuam os mesmos
    E o valor apostilado da permissão e o total apostilado do contrato não mudam

  Cenário: RN-06 — operação que o sistema não conhece
    Quando a transação chega com uma operação que o sistema não conhece
    Então vejo "* Operacao nao disponivel *"
    E a transação não segue

  Cenário: RN-06 — operação diferente de consulta e de alteração
    Quando informo no campo da opção uma operação que não é a de alteração nem a de consulta
    Então vejo "* Opcao nao disponivel. User ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é apagado

  Cenário: RN-07 — sem o perfil da alteração
    Dado que o meu perfil não tem o flag da alteração desta tela
    Quando confirmo a alteração
    Então vejo "* Acesso negado para esta operacao *"
    E nada é apagado

  Cenário: RN-08 — coordenação regional diferente da da sessão
    Dado que a minha sessão tem coordenação regional
    Quando informo uma coordenação regional diferente
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenação regional
    E nada é apagado

  Cenário: RN-09 — permissão de contrato não cadastrada
    Dado que não existe permissão de contrato para a coordenação regional, o tipo de contrato, a data limite e o grupo de licitação que informei
    Quando confirmo a consulta
    Então vejo "* Permissao nao cadastrada *"
    E o cursor volta ao campo da coordenação regional
    E nada é mostrado

  Cenário: RN-09 — não há apostilamento para a data
    Dado que a permissão existe, mas não há item de apostilamento para a data de atualização que informei
    Quando confirmo a consulta
    Então vejo "* Apostilamento nao cad. para esta data *"
    E o cursor volta ao campo da coordenação regional

  Cenário: RN-10 — a lista sai vazia
    Dado que a data de atualização em tela não tem item de apostilamento
    Quando a tela é apresentada
    Então as nove linhas ficam vazias
    E vejo "* Permiss. sem apostilamento para esta data *"

  Cenário: RN-11 — alterar sem consultar antes, ou mudando os dados da consulta
    Dado que a minha última consulta foi de outro contrato, ou que mudei a coordenação regional, o tipo de contrato, o grupo de licitação, a data limite ou a data de atualização
    Quando informo a operação de alteração e confirmo
    Então vejo "* Consulte antes da atualizacao *"
    E o cursor volta ao campo da coordenação regional
    E nada é apagado

  Cenário: RN-12 — estornar o apostilamento de uma data
    Dado que consultei o contrato e ele tem itens de apostilamento naquela data
    Quando marco a situação com S e confirmo a alteração
    Então o sistema apaga os itens daquele contrato naquela data de atualização
    E subtrai de cada permissão o valor do item apagado
    E recalcula o total apostilado do contrato e o regrava nas permissões
    E cada exclusão e cada regravação fica registrada na auditoria

  Cenário: RN-12 — a situação não marcada não apaga nada
    Dado que consultei o contrato e ele tem itens naquela data
    Quando confirmo a alteração sem marcar a situação
    Então os itens continuam lá
    E nenhum valor é regravado

  Cenário: RN-12 — a marca é da tela inteira, não da linha
    Dado que o contrato tem itens de apostilamento naquela data
    Quando marco a situação com S
    Então todos os itens daquele contrato naquela data são apagados
    E não há como escolher uma linha para apagar sozinha

  Cenário: RN-15 — campo não numérico
    Quando preencho com letra a coordenação regional, o tipo de contrato, o fornecedor, o grupo de licitação, uma das datas, o tipo de licitação ou um código de item
    Então a tela recusa o campo antes de qualquer leitura
    E o cursor volta ao campo recusado
    E nada é apagado

  Cenário: RN-15 — fornecedor não cadastrado
    Dado que o código de fornecedor informado não está no cadastro de fornecedores
    Quando confirmo a operação
    Então a operação é recusada com a mensagem de cadastro do sistema
    E nada é lido e nada é apagado
```
