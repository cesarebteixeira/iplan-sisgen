# US — C102T — Manter os grupos de atendimento de cada segmento do órgão

## Estória

Como **servidor da CRE**, quero **manter os grupos de atendimento de cada segmento
de atendimento do meu órgão**, para que os atendimentos do órgão possam ser
classificados por grupo — o integral, o parcial e o de 24 horas — sobre grupos que
existam de fato no segmento.

O grupo de atendimento é a peça mais fina dessa classificação: é apontando para um
grupo que o cadastro de atendimentos do órgão diz qual é o seu grupo integral, qual
é o parcial e qual é o de 24 horas. Sem grupo cadastrado o atendimento não se
classifica; e enquanto um atendimento apontar para o grupo, o grupo não pode sair.
Esta é a única porta de entrada e de saída dos grupos de atendimento do órgão.

## Contexto

Jornada S000M → C000M → C028M → C102T.

Ator: servidor de CRE — mantém os grupos de atendimento dos segmentos do órgão da
sua secretaria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A tela trabalha sobre o órgão da secretaria do usuário, nunca sobre um órgão digitado

O órgão não se digita nesta tela: é o tipo de órgão que o vínculo da matrícula com a
secretaria escolhida no LOGON deixou na sessão. O cabeçalho apenas mostra a descrição
desse órgão e a data do sistema. Tudo o que a tela exibe, confere e grava pertence a
esse órgão, e o usuário não tem como operar outro.

### RN-02 — A grade tem 15 linhas, e cada linha informa cinco dados

São 15 linhas por vez. Cada linha informa cinco dados: o código do segmento (2
dígitos), o código do grupo de atendimento (2), a descrição do grupo (20 caracteres),
a descrição resumida do grupo (5) e a ação (1). A tela mostra ainda, por linha, a
descrição resumida do segmento a que aquele grupo pertence — essa vem do cadastro de
segmentos e não se digita. Fora da grade, o cabeçalho tem sete campos vindos do
terminal (a tela, a origem, o número da transação, a data de entrada, o mês de
referência, a opção de manutenção e o prefixo de tela), mais o órgão, a data do
sistema e a linha de mensagem.

### RN-03 — Os dois códigos da linha têm de ser numéricos

O código do segmento e o código do grupo digitados na linha passam pela edição
numérica antes de qualquer conferência de negócio: o que não for número é recusado no
próprio campo e não chega a ser conferido.

### RN-04 — A tela só trabalha em ALT (alterar) ou CON (consultar); sem opção informada, ela abre em consulta

A opção de manutenção aceita apenas alteração e consulta. Qualquer outra é recusada
com "* Opcao nao disponivel. Use ALT ou CON *". Quando o campo chega em branco, a
tela adota a consulta e zera o grupo da linha — de modo que abrir a tela e confirmar
sem digitar nada não altera nada.

[?] A guarda interna compara a opção com os códigos de alteração e de consulta,
enquanto a mensagem manda usar "ALT" e "CON". Ou o terminal traduz o mnemônico antes
de enviar, ou a mensagem está desalinhada da guarda. Pergunta ao site; não concluo
qual dos dois.

### RN-05 — Consultar lista os grupos de atendimento do órgão, um por linha, com o segmento de cada um

Na consulta a tela percorre os grupos de atendimento cadastrados para o órgão e
mostra um por linha, até 15, na ordem do segmento e, dentro dele, do código do grupo.
Cada linha traz também a descrição resumida do segmento a que aquele grupo pertence,
lida do cadastro de segmentos. Quando o órgão não tem nenhum grupo, a tela avisa
"* Nao existem grupos atendimento cadastrados *".

[?] A lista continua a partir da chave do último grupo exibido; não dá para concluir,
pela fonte, se a retomada de uma página para a seguinte repete ou pula um grupo.
Pergunta ao site.

### RN-06 — A ação é por linha: I inclui, A altera, E exclui; o resto não faz nada

A ação é da linha, não da tela: I inclui, A altera e E exclui, e a tela traduz a letra
para a operação correspondente antes de pedir autorização. Linha sem código de grupo é
ignorada, e ação fora de I, A e E também — silenciosamente, sem mensagem.

### RN-07 — Cada linha executável passa antes pela conferência de acesso do usuário

Antes de tocar no cadastro, a operação da linha é conferida contra o perfil de acesso
do usuário àquela tela: sem a permissão da operação pretendida — incluir, alterar ou
excluir —, a tela mostra "* Acesso negado para esta operacao *" e nada é executado. A
própria opção de manutenção da tela passa pela mesma conferência.

### RN-08 — Incluir exige que o grupo não exista no órgão: nem o par segmento×grupo, nem o código em outro segmento

Ao incluir, a tela procura primeiro o par segmento×grupo: existindo, recusa com
"* Grupo de atendimento ja cadastrado *". Em seguida procura o código do grupo em
qualquer segmento do mesmo órgão: existindo — isto é, já usado em outro segmento —,
recusa com a mesma mensagem. O código do grupo é, portanto, único dentro do órgão, e
não se repete em dois segmentos.

### RN-09 — Incluir exige o segmento informado e cadastrado

Na inclusão o segmento é obrigatório: em branco, a tela recusa com
"* Informe o segmento *". Informado, ele tem de existir no cadastro de segmentos do
órgão; não existindo, "* Segmento nao cadastrado *".

### RN-10 — Incluir e alterar exigem as duas descrições do grupo

Para incluir ou alterar, a descrição do grupo e a sua descrição resumida têm de vir
preenchidas: em branco, a tela recusa com "* Informe a descricao *" e, na falta da
outra, com "* Informe a descricao resumida *". A exclusão não pede descrição nenhuma.

### RN-11 — Alterar exige que o grupo exista, e troca só as duas descrições

Ao alterar, o grupo (segmento e código) tem de existir: se não existir,
"* Grupo de atendimento nao cadastrado *". Existindo, a alteração substitui apenas a
descrição e a descrição resumida — o segmento e o código do grupo permanecem os que
estavam gravados.

### RN-12 — Excluir exige que o grupo exista e que nenhum atendimento o use

Ao excluir, o grupo tem de existir; se não existir,
"* Grupo de atendimento nao cadastrado *". Existindo, a tela percorre os atendimentos
cadastrados para o órgão e recusa a exclusão se algum deles apontar para esse grupo
como o seu grupo integral, parcial ou de 24 horas —
"* Grupos cadastrados neste atendimento *". Sem nenhum uso, a exclusão é executada.

[?] O que é, em negócio, um "atendimento" e o que distinguem os papéis integral,
parcial e 24 horas não está definido no corpus desta jornada; o que se vê é que são
três referências ao mesmo cadastro de grupos e que qualquer uma delas trava a
exclusão. Pergunta ao site.

### RN-13 — Consultar não grava nada

Na consulta a tela só lê e exibe: a passagem que grava é desviada de propósito quando
a opção não é alteração, e nenhuma gravação é feita.

### RN-14 — A tela grava em dois cadastros e lê outros três

A tela inclui, altera e exclui somente no cadastro de grupos de atendimento (C103T), e
grava também a trilha de auditoria (A010T). Os outros três cadastros que ela enxerga —
o de títulos de tela (S030T), o de segmentos de atendimento (C160T) e o de atendimentos
(C105T) — são apenas lidos. Para cada cadastro que enxerga, o sistema traz prontas as
operações de gravar e de apagar; mas trazer pronto não é usar: das cinco, a tela grava
em duas.

### RN-15 — Toda gravação deixa rastro na auditoria

Cada inclusão, alteração e exclusão monta um registro na trilha de auditoria (A010T)
com o tipo de órgão, a matrícula, a estação, a data e a hora, o cadastro que originou
a operação, a operação (inclusão, alteração ou exclusão) e os valores antes e depois —
e só então grava o grupo. Na inclusão os valores anteriores vão em branco; na
exclusão, os posteriores.

### RN-16 — A conferência vem toda antes da gravação

A tela percorre as linhas duas vezes: numa primeira passagem só confere e produz as
recusas; é a última passagem que grava. A conferência e a gravação são separadas de
propósito.

### RN-17 — Falha no banco interrompe a operação

Todo acesso ao banco testa o erro: o erro de leitura e o de gravação são levados à
rotina de comunicação do sistema, e a transação para ali, sem completar o resto.

### RN-18 — A conferência inteira fica atrás do prefixo de tela

Toda a conferência das linhas — grupo já cadastrado, segmento informado e cadastrado,
descrições obrigatórias e atendimento usando o grupo — está pendurada em um único
campo do cabeçalho, o prefixo de tela: chegando vazio, a tela confere; chegando
preenchido, ela pula a conferência inteira, em silêncio.

[?] Não dá para concluir, pela fonte, se esse caminho é alcançável pelo terminal: o
campo é informado à tela e nada nesta jornada o limpa. Se for alcançável, incluir,
alterar e excluir passam sem nenhuma das conferências; se não for, a guarda não
protege nada. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manter os grupos de atendimento de cada segmento do órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C102T

  Cenário: RN-01, RN-02, RN-05 e RN-13 — consultar os grupos de atendimento do órgão
    Dado que estou na tela C102T com a opção CON
    Quando confirmo a consulta
    Então vejo, no cabeçalho, a descrição do órgão da minha secretaria e a data do sistema
    E vejo, em cada uma das 15 linhas, o segmento, a descrição resumida do segmento, o grupo, a descrição do grupo, a descrição resumida e a ação
    E nada é gravado

  Cenário: RN-04 — sem opção informada a tela abre em consulta
    Dado que abro a tela C102T sem informar a opção de manutenção
    Quando confirmo sem digitar nenhuma linha
    Então a tela se comporta como consulta
    E nada é gravado

  Cenário: RN-04 — opção de manutenção não disponível
    Dado que estou na tela C102T
    Quando informo uma opção de manutenção diferente de ALT e CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"

  Cenário: RN-05 — órgão sem grupos de atendimento
    Dado que o órgão da minha secretaria não tem nenhum grupo de atendimento
    Quando confirmo a consulta
    Então vejo "* Nao existem grupos atendimento cadastrados *"

  Cenário: RN-03 — código de segmento ou de grupo não numérico
    Quando preencho o segmento ou o grupo de uma linha com letra
    Então a tela recusa o campo antes de qualquer conferência
    E nada é gravado

  Cenário: RN-06 — linha em branco ou com ação desconhecida
    Dado que preencho uma linha sem o código do grupo, ou com uma ação diferente de I, A e E
    Quando confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada

  Cenário: RN-07 — acesso negado para a operação da linha
    Dado que o meu perfil de acesso não permite incluir, alterar ou excluir nesta tela
    Quando confirmo a linha com a ação correspondente
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-08, RN-09, RN-10 e RN-14 — incluir um grupo de atendimento novo
    Dado que estou na tela C102T com a opção ALT
    E o segmento está cadastrado e o código do grupo ainda não existe no órgão
    Quando preencho a linha com a ação I, a descrição e a descrição resumida, e confirmo
    Então o grupo fica gravado no segmento informado
    E a operação fica registrada na auditoria

  Cenário: RN-08 — incluir um grupo que já existe no segmento
    Dado que o segmento já tem esse código de grupo
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Grupo de atendimento ja cadastrado *"
    E nada é gravado

  Cenário: RN-08 — incluir um código de grupo que já existe em outro segmento do órgão
    Dado que o código do grupo já existe em outro segmento do mesmo órgão
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Grupo de atendimento ja cadastrado *"
    E nada é gravado

  Cenário: RN-09 — incluir sem informar o segmento
    Quando preencho a linha com a ação I e deixo o segmento em branco
    Então vejo "* Informe o segmento *"
    E nada é gravado

  Cenário: RN-09 — incluir em um segmento que não está cadastrado
    Quando incluo um grupo em um segmento que o órgão não tem cadastrado
    Então vejo "* Segmento nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — incluir sem a descrição do grupo
    Quando preencho a linha com a ação I e deixo a descrição do grupo em branco
    Então vejo "* Informe a descricao *"
    E nada é gravado

  Cenário: RN-10 — incluir sem a descrição resumida do grupo
    Quando preencho a descrição do grupo e deixo a descrição resumida em branco
    Então vejo "* Informe a descricao resumida *"
    E nada é gravado

  Cenário: RN-11 — alterar as descrições de um grupo existente
    Dado que o grupo existe no segmento
    Quando preencho a linha com a ação A e as novas descrições, e confirmo
    Então as duas descrições do grupo passam a ser as novas
    E o segmento e o código do grupo não mudam
    E a operação fica registrada na auditoria

  Cenário: RN-11 — alterar um grupo que não existe
    Quando preencho a linha com a ação A em um segmento e um grupo que não existem
    Então vejo "* Grupo de atendimento nao cadastrado *"
    E nada é gravado

  Cenário: RN-12 — excluir um grupo que nenhum atendimento usa
    Dado que o grupo existe e nenhum atendimento do órgão aponta para ele
    Quando preencho a linha com a ação E e confirmo
    Então o grupo é apagado
    E a operação fica registrada na auditoria

  Cenário: RN-12 — excluir um grupo que um atendimento usa
    Dado que um atendimento do órgão aponta para esse grupo como o seu grupo integral, parcial ou de 24 horas
    Quando preencho a linha com a ação E e confirmo
    Então vejo "* Grupos cadastrados neste atendimento *"
    E nada é apagado

  Cenário: RN-17 — falha no banco durante a gravação
    Dado que a gravação do grupo falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E o grupo não é considerado gravado
```
