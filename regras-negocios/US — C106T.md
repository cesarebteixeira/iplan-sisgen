# US — C106T — Manter os grupos de atendimento do órgão filho

## Estória

Como **servidor da CRE**, quero **manter a lista dos grupos de atendimento que cada órgão filho da
minha secretaria pode usar**, para que **o atendimento prestado nesse órgão possa ser classificado
— o integral, o parcial e o de 24 horas — sobre grupos que aquele órgão realmente tem**.

O grupo de atendimento é a classificação mais fina do atendimento, e cada órgão filho só pode usar
os grupos dos segmentos de atendimento que ele tem cadastrados: é esta tela que diz quais são, e é
esta lista que as outras telas do sistema leem para classificar o que o órgão atende. Órgão sem
essa lista não se classifica; e um grupo que o órgão não oferece não pode ser apontado por ninguém
do órgão.

## Contexto

Jornada S000M → C000M → C028M → C106T.

Ator: servidor de CRE — mantém, para o órgão filho da sua secretaria, os grupos de atendimento que
aquele órgão pode usar em cada segmento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

As duas telas antes desta são menus, e a tela é alcançada pela opção 5 do `C028M` — não por
encadeamento de uma tela de transação. O que a `C106T` recebe delas é o contexto da sessão: a
matrícula, o perfil de acesso, o tipo de órgão da secretaria escolhida, a CRE e o órgão filho do
vínculo. A opção de manutenção não vem de fora: é a própria tela que a guarda e a repõe — e, quando
não há nenhuma guardada, ela abre em consulta. Esta é a última tela da jornada: ela não entrega a
transação a nenhuma tela seguinte.

As regras abaixo são só as da **tela desta jornada**.

## Regras de negócio

### RN-01 — A tela trabalha sobre o órgão filho; o tipo de órgão vem da sessão e não se digita

O cadastro que esta tela mantém pertence a um órgão filho — o mesmo órgão que o vínculo da
matrícula com a secretaria escolhida no LOGON deixou na sessão. Esse órgão é mostrado informado e
pode ser trocado; o **tipo de órgão** (o da secretaria da sessão) não se digita: ele é a chave de
tudo o que a tela lê e grava. O cabeçalho ainda mostra a descrição do tipo de órgão e a data do
sistema.

### RN-02 — A tela reapresenta a última opção e o último órgão da sessão

Ao abrir, a tela mostra a opção de manutenção que ficou guardada do uso anterior na mesma sessão —
e, quando não há nenhuma guardada, ela abre em consulta. O órgão filho que ela mostra é o do vínculo
da matrícula, quando existe; quando a matrícula não tem vínculo, ela reapresenta o último órgão que
a sessão trabalhou.

### RN-03 — Consultar exige o órgão informado, e quem tem órgão vinculado não consulta outro

Na consulta o órgão é obrigatório: em branco, a tela recusa com "* Informe o orgao *". Se a
matrícula tem órgão vinculado, a tela só aceita consultar esse órgão — informando outro, recusa com
"* Usuario sem acesso a outro orgao *". Sem vínculo, qualquer órgão pode ser informado, desde que
passe pelas conferências seguintes.

### RN-04 — O órgão informado tem de existir, ser da secretaria, ser do mesmo grupo e estar completo

O órgão informado tem de existir no cadastro de órgãos: não existindo, "* Orgao nao cadastrado *".
Existindo, a tela confere, nesta ordem, que o cadastro não está incompleto — o nome, o endereço, o
bairro, o órgão pai, a quantidade de matrículas e a quantidade de pessoas têm de estar preenchidos
—, senão "* Orgao cadastrado com dados incompletos *"; que o tipo de órgão do cadastro é o da
sessão, senão "* Orgao nao pertence a esta secretaria *"; e, quando a sessão tem um código de CRE,
que o do cadastro é o mesmo, senão "* Usuario sem acesso ao grupo deste orgao *". Passando, a tela
assume o órgão e mostra o nome, a CRE e se ele é creche ("Sim" ou "Nao"). O cadastro de órgãos
guarda versões do mesmo código, e a tela ignora as versões marcadas como excluídas.

### RN-05 — A grade tem 13 linhas, e cada linha informa três dados

São 13 linhas por vez. Cada linha informa três dados: o código do segmento (2 dígitos), o código do
grupo de atendimento (2) e a ação (1). A linha ainda mostra dois dados que não se digitam — a
descrição resumida do segmento e a descrição do grupo —, ambos lidos dos cadastros. Fora da grade, a
tela mostra a opção de manutenção, o prefixo de tela, o órgão, a CRE, a descrição do tipo de órgão,
a data do sistema, a indicação de creche e a linha de mensagem.

### RN-06 — Os códigos passam pela edição numérica antes de qualquer conferência

O órgão filho, a CRE, o segmento e o grupo de atendimento passam pela edição numérica antes de
qualquer conferência de negócio: o que não for número é recusado no próprio campo, com o cursor
deslocado para ele, e não chega a ser conferido.

### RN-07 — A opção de manutenção só aceita alteração e consulta; sem opção, a tela abre em consulta

A opção aceita apenas alteração e consulta. Qualquer outra é recusada com
"* Opcao nao disponivel. Use ALT ou CON *". Quando o campo chega em branco, a tela adota a consulta.

[?] A guarda interna compara a opção com os códigos de alteração e de consulta, enquanto a mensagem
manda usar "ALT" e "CON". Ou o terminal traduz o mnemônico antes de enviar, ou a mensagem está
desalinhada da guarda. Pergunta ao site; não concluo qual dos dois.

### RN-08 — Alterar exige que o órgão já tenha sido consultado

A alteração vale só para o órgão que a tela já está trabalhando — o do vínculo da matrícula ou o que
foi consultado antes. Informando outro órgão, a tela recusa com "* Consulte antes de atualizar *" e
não altera nada. Alterar é, portanto, um segundo passo: primeiro se consulta o órgão, depois se
altera.

### RN-09 — Consultar lista os grupos de atendimento do órgão, até 13 linhas

Na consulta a tela percorre os grupos de atendimento do órgão e mostra um por linha, até 13, na
ordem do segmento e, dentro dele, do código do grupo, com a descrição resumida do segmento e a
descrição do grupo. Quando o órgão não tem nenhum grupo, a tela avisa
"* Orgao sem grupos de atend.cadastrados *". As linhas informadas na consulta não são conferidas nem
gravadas pela conferência — a complementação automática da RN-19 é a única gravação que a consulta
alcança.

### RN-10 — A ação é por linha: I inclui, E exclui; o resto não faz nada

A ação é da linha, não da tela: I inclui e E exclui. Qualquer outra letra — inclusive A — não faz
nada, em silêncio, sem mensagem. Linha sem código de grupo é ignorada.

### RN-11 — Cada linha executável passa pela conferência de acesso do usuário

Antes de tocar no cadastro, a operação da linha (incluir ou excluir) é conferida contra o perfil de
acesso do usuário àquela tela: sem a permissão da operação, a tela mostra
"* Acesso negado para esta operacao *" e nada é executado. Sem o perfil de acesso à tela, a recusa é
"* Acesso negado para esta matricula *". A própria opção de manutenção passa pela mesma conferência.

### RN-12 — Incluir exige que o grupo exista no catálogo, e o segmento vem do próprio grupo

Ao incluir, o código do grupo informado tem de existir no catálogo de grupos de atendimento do tipo
de órgão: não existindo, "* Grupo de atendimento nao cadastrado *". Existindo, o segmento sai do
próprio cadastro do grupo — o que o usuário tenha digitado no campo do segmento é substituído por
ele.

### RN-13 — Incluir exige que o segmento esteja cadastrado para o órgão

O segmento do grupo tem de estar entre os segmentos cadastrados para aquele órgão filho: não
estando, "* Cadastrar o segmento para este Orgao *" e a inclusão não acontece.

### RN-14 — Incluir exige que o grupo ainda não esteja no órgão

A inclusão só passa se aquele grupo ainda não estiver registrado para o órgão no segmento: já
estando, "* Grupo de atendimento ja cadastrado *".

### RN-15 — Excluir exige que o grupo esteja no órgão

A exclusão só passa se aquele grupo estiver registrado para o órgão no segmento informado: não
estando, "* Grupo de atendimento nao cadastrado *". Estando, a associação é apagada.

### RN-16 — A conferência vem toda antes da gravação

A tela percorre as linhas duas vezes na mesma entrada: numa primeira passagem só confere e produz as
recusas; é a última passagem que grava. Nenhuma gravação é executada na exibição nem na conferência.

[?] Uma recusa tem de interromper a transação para que a gravação não aconteça, mas quem marca essa
interrupção depois de mostrar a mensagem é uma rotina do sistema que não está no acervo desta
jornada. Não dá para conferir, pela fonte, se toda recusa chega a interromper. Pergunta ao site.

### RN-17 — Toda inclusão e exclusão deixam rastro na auditoria

Cada inclusão e cada exclusão monta um registro na trilha de auditoria com o tipo de órgão, a
matrícula, a estação, a data e a hora, o cadastro de origem, a operação (inclusão ou exclusão) e os
valores antes e depois — na inclusão os valores anteriores vão em branco, na exclusão, os
posteriores. É esse registro que diz quem mexeu na lista.

### RN-18 — A tela grava em um cadastro e lê cinco; das operações prontas, executa três

A tela inclui e exclui somente no cadastro de grupos de atendimento do órgão (C107T), e grava também
a trilha de auditoria (A010T). Os outros cinco cadastros que ela enxerga — o de títulos de tela
(S030T), o de órgãos (C020T), o de grupos de atendimento do catálogo (C103T), o de segmentos de
atendimento (C160T) e o de segmentos do órgão (C024T) — são apenas lidos. Para cada cadastro que
enxerga, o sistema traz prontas uma operação de gravar e uma de apagar: das catorze, a tela executa
três.

### RN-19 — A tela completa sozinha a lista do órgão a partir do catálogo

Na última passagem a tela percorre os segmentos cadastrados para o órgão e, para cada segmento que
ainda não tem **nenhum** grupo registrado, registra todos os grupos que o catálogo tem para aquele
segmento, deixando a auditoria de cada um. É a única gravação que acontece sem que o usuário tenha
informado linha nenhuma.

[?] Essa complementação automática só é alcançada quando a opção é a de **consulta**; quando a opção
é a de alteração, a tela desvia dela. Ou a consulta grava — contrariando o que ela própria promete —,
ou a complementação foi feita para a alteração e ficou inalcançável nela. As duas leituras cabem na
fonte; pergunta ao site, não escolho um dos lados.

### RN-20 — Falha no banco interrompe a operação

Todo acesso ao banco testa o erro: o erro de leitura e o de gravação são levados à rotina de
comunicação do sistema, e a transação para ali, sem completar o resto.

### RN-21 — A conferência inteira fica atrás do prefixo de tela

Toda a conferência das linhas — a opção, o órgão, a existência do grupo no catálogo, o segmento do
órgão e o grupo já cadastrado — está pendurada em um único campo do cabeçalho, o prefixo de tela:
chegando vazio, a tela confere; chegando preenchido, ela pula a conferência inteira, em silêncio, e
a última passagem segue para a gravação.

[?] Não dá para concluir, pela fonte, se esse caminho é alcançável pelo terminal: o campo é
informado à tela e nada nesta jornada o limpa. Se for alcançável, incluir e excluir passam sem
nenhuma das conferências; se não for, a guarda não protege nada. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manter os grupos de atendimento do órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C106T

  Cenário: RN-01, RN-05 e RN-09 — consultar os grupos de atendimento do órgão
    Dado que abro a tela C106T
    Quando confirmo sem informar nada
    Então a tela abre em consulta, com o órgão filho do meu vínculo informado
    E vejo, no cabeçalho, a descrição do tipo de órgão, o nome do órgão, a CRE, a indicação de creche e a data do sistema
    E vejo, em cada uma das 13 linhas, o segmento, a descrição resumida do segmento, o grupo, a descrição do grupo e a ação
    E nenhuma das linhas informadas é conferida ou gravada

  Cenário: RN-02 — a tela reapresenta a última opção e o último órgão da sessão
    Dado que já usei a tela nesta sessão
    Quando abro a tela C106T de novo
    Então a opção de manutenção é a da última utilização
    E o órgão mostrado é o do meu vínculo — ou o último que a sessão trabalhou, se eu não tiver vínculo

  Cenário: RN-03 — consultar sem informar o órgão
    Dado que a minha matrícula não tem órgão vinculado
    Quando confirmo a consulta com o órgão em branco
    Então vejo "* Informe o orgao *"
    E nada é gravado

  Cenário: RN-03 — consultar um órgão diferente do meu vínculo
    Dado que a minha matrícula tem um órgão vinculado
    Quando informo outro órgão e confirmo a consulta
    Então vejo "* Usuario sem acesso a outro orgao *"
    E nada é gravado

  Cenário: RN-04 — consultar um órgão que o cadastro não tem
    Quando informo um órgão que não existe e confirmo a consulta
    Então vejo "* Orgao nao cadastrado *"
    E nada é gravado

  Cenário: RN-04 — consultar um órgão com o cadastro incompleto
    Dado que o órgão existe e está sem o nome, o endereço, o bairro, o órgão pai, a quantidade de matrículas ou a quantidade de pessoas
    Quando confirmo a consulta
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E nada é gravado

  Cenário: RN-04 — consultar um órgão de outra secretaria
    Dado que o órgão existe, mas é de um tipo de órgão diferente do da minha secretaria
    Quando confirmo a consulta
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E nada é gravado

  Cenário: RN-04 — consultar um órgão de outro grupo da mesma secretaria
    Dado que o órgão existe e é da minha secretaria, mas de outra CRE
    Quando confirmo a consulta
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E nada é gravado

  Cenário: RN-09 — órgão sem grupos de atendimento
    Dado que o órgão não tem nenhum grupo de atendimento registrado
    Quando confirmo a consulta
    Então vejo "* Orgao sem grupos de atend.cadastrados *"

  Cenário: RN-06 — código não numérico
    Quando preencho o órgão, a CRE, o segmento ou o grupo com letra
    Então a tela recusa o campo antes de qualquer conferência
    E nada é gravado

  Cenário: RN-07 — opção de manutenção não disponível
    Quando informo uma opção de manutenção diferente de ALT e CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E nada é gravado

  Cenário: RN-08 — alterar sem ter consultado o órgão
    Dado que a tela está trabalhando um órgão
    Quando informo outro órgão com a opção ALT e confirmo
    Então vejo "* Consulte antes de atualizar *"
    E nada é gravado

  Cenário: RN-10 — linha sem grupo ou com ação desconhecida
    Dado que preencho uma linha sem o código do grupo, ou com uma ação diferente de I e E
    Quando confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada

  Cenário: RN-11 — acesso negado para a operação da linha
    Dado que o meu perfil de acesso não permite incluir nem excluir nesta tela
    Quando confirmo a linha com a ação correspondente
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-12, RN-13, RN-17 e RN-18 — incluir um grupo de atendimento no órgão
    Dado que estou na tela C106T com a opção ALT e o órgão já consultado
    E o grupo existe no catálogo do meu tipo de órgão
    E o segmento desse grupo está cadastrado para o órgão
    E esse grupo ainda não está registrado para o órgão
    Quando preencho a linha com a ação I e o código do grupo, e confirmo
    Então o grupo fica registrado para o órgão no segmento do próprio grupo
    E a operação fica registrada na auditoria

  Cenário: RN-12 — incluir um grupo que o catálogo não tem
    Quando preencho a linha com a ação I e um código de grupo que o catálogo do meu tipo de órgão não tem
    Então vejo "* Grupo de atendimento nao cadastrado *"
    E nada é gravado

  Cenário: RN-13 — incluir um grupo cujo segmento o órgão não tem
    Dado que o grupo existe no catálogo, mas o segmento dele não está cadastrado para o órgão
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Cadastrar o segmento para este Orgao *"
    E nada é gravado

  Cenário: RN-14 — incluir um grupo que o órgão já tem
    Dado que o grupo já está registrado para o órgão no segmento
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Grupo de atendimento ja cadastrado *"
    E nada é gravado

  Cenário: RN-15 e RN-17 — excluir um grupo do órgão
    Dado que o grupo está registrado para o órgão no segmento informado
    Quando preencho a linha com a ação E e confirmo
    Então o grupo deixa de estar registrado para o órgão
    E a operação fica registrada na auditoria

  Cenário: RN-15 — excluir um grupo que o órgão não tem
    Quando preencho a linha com a ação E em um segmento e um grupo que o órgão não tem registrado
    Então vejo "* Grupo de atendimento nao cadastrado *"
    E nada é apagado

  Cenário: RN-19 — o órgão ganha sozinho os grupos que faltavam do catálogo
    Dado que o órgão tem um segmento cadastrado sem nenhum grupo de atendimento registrado
    E o catálogo tem grupos para esse segmento
    Quando confirmo a consulta
    Então a tela registra para o órgão os grupos daquele segmento
    E registra a auditoria de cada um

  Cenário: RN-20 — falha no banco durante a gravação
    Dado que a gravação falha no banco
    Quando confirmo a inclusão
    Então a transação é interrompida com a mensagem de erro do sistema
    E o grupo não é considerado incluído
```
