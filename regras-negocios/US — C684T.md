# US — C684T — Exclusão da prorrogação da permissão de contrato por grupo de licitação e coordenação regional

## Estória

Como **servidor da CRE**, quero **pedir a exclusão da prorrogação registrada nos grupos de
licitação das coordenações regionais que eu indicar**, para que **a permissão de contrato pare de
carregar um prazo prorrogado que não se sustenta**.

A prorrogação é o que estende o prazo de uma permissão de contrato já cadastrada, grupo de licitação
por grupo de licitação de cada coordenação regional: ela é lançada à parte e fica somada ao que a
permissão autoriza. Quando o que foi prorrogado não vale mais, alguém precisa tirá-la do cadastro, e
é isso que esta tela faz — escolhidos o contrato, o período e as coordenações, ela confere grupo por
grupo, pede a confirmação e entrega o pedido de exclusão para processamento. Sem ela, a exclusão só
sairia por intervenção direta na base, e a permissão continuaria autorizando um prazo que não vai ser
cumprido.

## Contexto

Jornada S000M → C000M → C050M → C664M → C684T.
Ator: servidor de CRE — informa o contrato, o período e as coordenações regionais cuja prorrogação
deve ser excluída, confere o que a tela encontrou e confirma o pedido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

Esta tela é a quarta opção do menu `C664M`, o mesmo menu das telas irmãs que cadastram e cancelam a
prorrogação. O menu entrega a tela **sem passar registro e sem passar operação**: quem abre não
escolhe o modo, e a própria tela se apresenta em alteração. Ela não encadeia em outra — ao terminar,
reabre a si mesma — e o que deixa para trás é o **pedido do relatório**, na fila de impressão.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — Esta tela pede a exclusão; quem exclui é o processamento do relatório

A tela não apaga a prorrogação: ela confere o que foi informado, pergunta e registra o **pedido** do
relatório na fila de impressão. O período da coordenação e a prorrogação são lidos e nunca escritos
por ela, e a única gravação que ela dispara é a do pedido — nenhum outro registro é criado por esta
tela. Enquanto o processamento do relatório não roda, a prorrogação continua registrada e a permissão
continua como estava.

[?] O nome de negócio desta tela não vem do material: o texto que ela exibe é o do próprio pedido —
`Atualiza cadastro da permissao <S/N>?` — e os rótulos da máscara, que trariam o nome que o operador
lê, não fazem parte do lote. O nome usado nesta estória é leitura de negócio, não transcrição.
Pergunta ao site.

### RN-02 — O que se informa para dizer de qual prorrogação se trata

O operador informa o **tipo de contrato**, o **grupo de licitação** — com **9999** valendo por todos
os grupos da coordenação —, as duas datas do período (o **início** e a **data limite**, cada uma em
dia, mês e ano) e as **coordenações regionais**, que são **doze** campos de dois dígitos: só as
preenchidas são conferidas. A **secretaria** não se digita: é a do vínculo da matrícula, que ficou na
sessão desde a entrada, e é ela que entra na chave de tudo o que a tela lê.

[?] A tela não confere as coordenações informadas contra a coordenação do vínculo: as doze são
percorridas sem comparação com a da sessão, e a rotina de segurança que a tela chama recebe a
coordenação do vínculo apenas como contexto, não como limite das informadas. Se um servidor de uma
coordenação pode pedir a exclusão da prorrogação de outra, o material não diz. Pergunta ao site.

### RN-03 — O contrato, o grupo, o dia da data limite e ao menos uma coordenação são obrigatórios

Antes de ler qualquer cadastro, a tela exige, nesta ordem: o tipo de contrato, o grupo de licitação,
o **dia** da data limite do período — o mês e o ano não são conferidos — e ao menos uma coordenação
preenchida. Sem o tipo de contrato a recusa é **\* Informe o tipo de contrato \***; sem o grupo,
**\* Informe o grupamento \***; sem a data limite, **\* Informe data limite da permissao \***; e sem
nenhuma coordenação, **\* Informe grupos para exclusao da prorrogacao \***. Em cada recusa o cursor
volta ao campo que faltou e nada é lido nem registrado.

### RN-04 — Só as coordenações preenchidas são conferidas

As doze coordenações regionais são percorridas uma a uma, e só as que foram preenchidas: a que está
vazia é saltada, sem mensagem e sem leitura. Um pedido com uma só coordenação vale; com as doze,
também.

### RN-05 — Cada coordenação precisa ter o grupo no período

Para cada coordenação informada, a tela percorre os grupos registrados no **período** daquela
coordenação, para a secretaria, o tipo de contrato e a data limite informados. O grupo informado
limita o alcance — só ele é conferido —, e o grupo **9999** dispensa o filtro e alcança todos os
grupos do período. Não achando grupo, a exclusão é recusada com **\* Grupo nao cadastrado nesta
permissao \***, com o cursor de volta à coordenação em conferência, e as coordenações seguintes não
são conferidas. Os grupos achados são guardados para conferência um a um: cabem **cinquenta** por
coordenação.

[?] A leitura do período pergunta ao sistema por sete componentes da chave, com o grupo zerado quando
o informado é 9999, e depois não compara o grupo lido — só corta pelo limite superior. O que os
modificadores de leitura do sistema fazem não está no corpus: se a leitura exigisse a chave exata, o
grupo 9999 não acharia nada. Pergunta ao site.

[?] São cinquenta os grupos guardados por coordenação, e a área é a mesma para todas as coordenações
do pedido: passando de cinquenta grupos no período, os excedentes não entram na conferência e a tela
segue como se não existissem. O material não diz qual é o volume real de grupos por período.
Pergunta ao site.

### RN-06 — Cada grupo achado precisa ter a prorrogação registrada

Para cada grupo achado no período, a tela procura a prorrogação daquele grupo — a mesma coordenação,
a mesma secretaria, o mesmo tipo de contrato, a mesma data limite e o mesmo grupo. Não achando, a
exclusão é recusada com **\* Grupo nao cadastrado nesta prorrogacao \***, com o cursor de volta à
coordenação em conferência: não há o que excluir onde a prorrogação não foi registrada.

[?] A procura da prorrogação ignora a classe, a subclasse, o gênero e a data de atualização, que
também identificam o registro: a tela zera esses componentes e, achado o primeiro registro da classe,
não compara nenhum deles. Se o que ela encontra é sempre o lançamento inicial do período ou pode ser
uma prorrogação lançada depois, o material não diz. Pergunta ao site.

### RN-07 — Prorrogação que ainda tem quantidade não é excluída

Achada a prorrogação, a tela examina o que ela acrescentou. Se ainda há **quantidade prorrogada** no
registro, a exclusão é recusada com **\* Existem quantidades prorrogadas \*** e o cursor volta à
coordenação em conferência. Só a prorrogação sem quantidade segue para a conferência seguinte.

[?] A conferência olha a quantidade e não o valor prorrogado, que o cadastro também guarda: uma
prorrogação lançada só com valor, sem quantidade, passaria por aqui. Se é para ser assim, o material
não diz. Pergunta ao site.

### RN-08 — Pedido em curso na janela da prorrogação impede a exclusão

Ainda na conferência de cada grupo, a tela procura, na mesma coordenação, um **pedido** cuja data
limite termine depois do início da prorrogação; a procura começa **sete dias** antes desse início.
Achando um, a exclusão é recusada com **\* Existem pedidos nesta prorrogacao \***, com o cursor de
volta à coordenação em conferência: prorrogação com pedido em curso não sai por aqui.

[?] De onde vêm os sete dias subtraídos do início — prazo de antecedência, janela de segurança ou
regra do contrato — o material não diz, e a unidade do decréscimo é leitura de negócio a partir da
construção da tela, não declaração do corpus. Pergunta ao site.

[?] A data de referência dessa procura é montada do cadastro da prorrogação, e só quando o operador
deixa os campos de início em branco; se ele os preencher, a referência fica zerada e a janela perde o
sentido. Se esses campos são para o operador informar, o material não diz o que a tela faz com o que
ele informa. Pergunta ao site.

### RN-09 — O que o operador deixar em branco é reposto do cadastro

O início do período é digitável, mas não precisa ser informado: achado o período da coordenação, a
tela repõe nele o início registrado. O início da prorrogação é reposto do mesmo modo, do registro da
prorrogação, quando o operador o deixa em branco. O que o operador digitar nesses campos, quando
digitar, é o que segue no pedido.

[?] Os dois pares de datas da prorrogação — o início e o limite — não têm rótulo de negócio como os
oito primeiros campos: a conferência numérica os chama pelos próprios nomes internos. O material não
diz se eles existem para o operador conferir o que está vigente ou para informar o novo período; o
que se pode afirmar é que o sistema os repõe do cadastro quando vêm em branco e os entrega ao
processamento. Pergunta ao site.

### RN-10 — A exclusão só vira pedido depois da confirmação

Passando todas as conferências, a tela guarda o que foi informado e pergunta **Atualiza cadastro da
permissao <S/N>?**, com o cursor no campo da resposta. Só a resposta **S** leva o pedido adiante.
Resposta diferente de S — ou a mudança do tipo de contrato, do grupo, da data limite (dia, mês e ano)
ou de qualquer uma das doze coordenações depois da pergunta — descarta a confirmação e a conferência
inteira recomeça: nada é registrado. Mudar as datas de início depois da pergunta não descarta a
confirmação, porque a conferência as repõe.

[?] A resposta diferente de S não encerra a operação: ela limpa a resposta, volta o contador da
passagem e a conferência recomeça, terminando na mesma pergunta, enquanto os campos conferidos
estiverem preenchidos. Se a intenção era permitir desistir, o material não diz como. Pergunta ao
site.

### RN-11 — Um pedido do mesmo relatório já na fila bloqueia o pedido novo

Antes de aceitar a confirmação, a tela procura na fila de relatórios um pedido do mesmo relatório.
Havendo, recusa com **\* Relatorio em processamento. Aguarde. \***, com o cursor de volta ao campo da
resposta, e nenhum pedido novo é registrado. Enquanto o pedido anterior não for processado e sair da
fila, esta tela não aceita outro.

[?] A procura olha só o código do relatório: um pedido na fila de qualquer origem, coordenação ou
contrato bloqueia o pedido desta tela — e são **41** os programas do acervo que leem a mesma fila por
essa chave. Se é para ser assim, o material não diz. Pergunta ao site.

### RN-12 — O que a tela grava e o que entrega ao processamento

Confirmada a exclusão, a tela grava **o pedido do relatório** na fila de impressão e, em seguida,
entrega o relatório ao processamento, avisando **\* Cadastro sendo atualizado \*** e reabrindo a
própria tela. O pedido é numerado como o **seguinte ao último pedido da fila** e leva o relatório, a
secretaria, a matrícula de quem pediu, a estação, o dia, o mês e o ano da sessão e, no bloco de
parâmetros, o tipo de contrato, o grupo de licitação, as datas do período, o início da prorrogação,
as doze coordenações e a matrícula. A fila comporta **90.000** pedidos.

[?] O pedido não leva impressora, saída, tipo de impressão nem e-mail: a tela deixa esses campos em
branco e a gravação só leva o que não está em branco, de modo que eles ficam com o que estava no
último pedido lido da fila; e o dicionário marca a impressora como campo obrigatório do pedido. O
e-mail lido do cadastro do servidor segue apenas no bloco de parâmetros. Se é para ser assim, o
material não diz. Pergunta ao site.

[?] O programa que processa o relatório pedido não está entre os fontes desta jornada: o que a tela
entrega está sustentado, o que o processamento faz com o pedido e com os cadastros não. Pergunta ao
site.

### RN-13 — A tela só opera em alteração, e quem a abre não escolhe o modo

A tela se apresenta já em **alteração**: a operação vem preenchida com a alteração a cada exibição.
Qualquer outra operação é recusada com **\* Operacao nao disponivel. Use ALT \***, com o cursor de
volta ao campo da operação. O menu que a abre entrega apenas a tela — sem registro e sem operação —,
de modo que o modo não vem de quem chamou.

[?] A recusa compara a operação com a palavra da alteração que o ambiente carrega — o mnemônico é
"CHG" —, enquanto a mensagem manda usar "ALT": ou o terminal traduz o que o operador digita antes de
enviar, ou a mensagem está desalinhada da conferência. Pergunta ao site; não concluo qual dos dois.

### RN-14 — Nenhum campo desta tela é texto livre

Os **vinte e seis** campos abertos à digitação — o tipo de contrato, o grupo de licitação, as três
partes do início do período, as três da data limite, as três do início e as três do limite da
prorrogação e as doze coordenações regionais — passam pela edição numérica antes de qualquer leitura;
o que não for número é recusado no próprio campo, com o cursor de volta a ele. A operação e a
resposta à confirmação não passam por essa edição.

[?] Nos doze campos de coordenação a edição numérica usa o próprio nome interno do campo como rótulo
da mensagem, e não um rótulo de negócio como nos outros catorze: o que o operador lê quando erra um
desses campos não está no material. Pergunta ao site.

### RN-15 — A operação só acontece com o acesso autorizado

Antes de ler qualquer cadastro, a tela pede ao sistema de segurança que confira a matrícula, a tela e
o código de acesso do vínculo; na conferência do que foi informado, pede a conferência da operação,
depois de passar pelo roteamento da tela, e essa conferência é contra o que o código de acesso do
vínculo permite para aquela tela. A segurança recebe o contexto da sessão — a secretaria, a
matrícula, o código de acesso, o privilégio e a coordenação regional. Sem liberação, a transação é
abandonada sem ler nem registrar nada.

[?] O texto da recusa por falta de autorização é montado pela rotina de mensagens de segurança, que a
tela não chama diretamente: o fonte da tela só testa a liberação. Pergunta ao site.

### RN-16 — A falha de acesso ao banco interrompe a operação

Toda leitura e toda gravação são conferidas: o erro interrompe a transação com o tratamento de erro
do sistema — leitura e gravação com códigos distintos —, sem completar o que vinha depois. Uma falha
ao gravar o pedido interrompe a transação antes de o processamento ser entregue.

## Cenários BDD

```gherkin
Funcionalidade: Exclusão da prorrogação da permissão de contrato por grupo de licitação e coordenação regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a matrícula, o código de acesso, o privilégio e a coordenação regional do vínculo
    E tenho acesso à tela C684T

  Cenário: RN-02 e RN-03 — informar o contrato, o período e as coordenações
    Dado que informo o tipo de contrato, o grupo de licitação, o início do período e a data limite
    E informo uma coordenação regional que tem grupos nesse período
    Quando confirmo
    Então a tela confere o período da coordenação pela secretaria da minha sessão
    E o início do período que eu não informei é reposto do cadastro
    E nada foi registrado ainda

  Cenário: RN-04 — a coordenação em branco não é conferida
    Dado que preencho apenas duas das doze coordenações
    Quando confirmo
    Então a tela confere somente as duas coordenações preenchidas
    E as demais não são lidas nem exigidas

  Cenário: RN-05 — o grupo 9999 alcança todos os grupos do período
    Dado que informo o grupo de licitação 9999 e uma coordenação que tem grupos no período
    Quando confirmo
    Então todos os grupos daquele período são conferidos
    E nenhum grupo é recusado por não ser o informado

  Cenário: RN-03 — tipo de contrato não informado
    Quando confirmo sem informar o tipo de contrato
    Então vejo "* Informe o tipo de contrato *"
    E o cursor volta ao campo do tipo de contrato
    E nada é lido nem registrado

  Cenário: RN-03 — grupo de licitação não informado
    Dado que informei o tipo de contrato
    Quando confirmo sem informar o grupo de licitação
    Então vejo "* Informe o grupamento *"
    E o cursor volta ao campo do grupo

  Cenário: RN-03 — data limite não informada
    Dado que informei o tipo de contrato e o grupo de licitação
    Quando confirmo sem informar a data limite do período
    Então vejo "* Informe data limite da permissao *"
    E o cursor volta ao campo da data limite

  Cenário: RN-03 — nenhuma coordenação informada
    Dado que informei o tipo de contrato, o grupo de licitação e a data limite
    Quando confirmo sem informar nenhuma coordenação regional
    Então vejo "* Informe grupos para exclusao da prorrogacao *"
    E o cursor volta ao primeiro campo de coordenação

  Cenário: RN-05 — a coordenação não tem o grupo no período
    Dado que informo uma coordenação que não tem grupo registrado no período informado
    Quando confirmo
    Então vejo "* Grupo nao cadastrado nesta permissao *"
    E o cursor volta ao campo daquela coordenação
    E as coordenações seguintes não são conferidas
    E nada é registrado

  Cenário: RN-06 — o grupo não tem prorrogação registrada
    Dado que o período da coordenação tem o grupo, mas não há prorrogação registrada para ele
    Quando confirmo
    Então vejo "* Grupo nao cadastrado nesta prorrogacao *"
    E o cursor volta ao campo daquela coordenação
    E nada é registrado

  Cenário: RN-07 — a prorrogação ainda tem quantidade
    Dado que a prorrogação do grupo tem quantidade acrescentada
    Quando confirmo
    Então vejo "* Existem quantidades prorrogadas *"
    E o cursor volta ao campo daquela coordenação
    E a prorrogação continua registrada

  Cenário: RN-08 — há pedido em curso na janela da prorrogação
    Dado que existe um pedido daquela coordenação cuja data limite termina depois do início da prorrogação
    Quando confirmo
    Então vejo "* Existem pedidos nesta prorrogacao *"
    E o cursor volta ao campo daquela coordenação
    E nada é registrado

  Cenário: RN-09 — as datas em branco são repostas do cadastro
    Dado que deixo o início do período em branco e o período da coordenação está registrado
    Quando confirmo
    Então a tela repõe o início do período que está no cadastro
    E o início da prorrogação também é reposto do cadastro quando eu o deixo em branco

  Cenário: RN-10 — a pergunta de confirmação vem antes de qualquer gravação
    Dado que todas as conferências passaram
    Quando confirmo
    Então vejo "Atualiza cadastro da permissao <S/N>?"
    E o cursor fica no campo da resposta
    E nada foi registrado ainda

  Cenário: RN-10 — resposta diferente de S descarta a exclusão
    Dado que vejo a pergunta de confirmação
    Quando respondo N
    Então nenhum pedido é registrado
    E a tela volta a conferir a exclusão
    E a prorrogação continua registrada

  Cenário: RN-10 — mudar um campo conferido depois da pergunta descarta a confirmação
    Dado que vejo a pergunta de confirmação
    Quando troco o grupo de licitação, a data limite ou uma das coordenações e respondo S
    Então a confirmação é descartada
    E a tela volta a conferir a exclusão
    E nenhum pedido é registrado

  Cenário: RN-11 — já há pedido do mesmo relatório na fila
    Dado que há um pedido do mesmo relatório ainda não processado
    Quando respondo S à pergunta de confirmação
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da resposta
    E nenhum pedido novo é registrado

  Cenário: RN-12 — a exclusão confirmada gera o pedido, não a exclusão
    Dado que todas as conferências passaram e já respondi que confirmo
    Quando a tela registra a exclusão
    Então o pedido do relatório é gravado na fila com a secretaria, a matrícula, a estação e a data da sessão
    E o pedido recebe o número seguinte ao do último pedido da fila
    E o pedido leva o contrato, o grupo, as datas do período, o início da prorrogação e as coordenações
    E vejo "* Cadastro sendo atualizado *"
    E a prorrogação continua registrada até o processamento do relatório rodar

  Cenário: RN-13 — operação diferente da alteração
    Dado que estou na tela C684T
    Quando informo uma operação diferente da alteração
    Então vejo "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo da operação
    E nada é registrado

  Cenário: RN-13 — quem abre a tela não escolhe o modo
    Dado que abro a tela pela opção do menu C664M
    Quando a tela se apresenta
    Então ela vem em alteração, sem que o menu tenha passado registro ou operação
    E nenhum dado de outra tela vem preenchido

  Cenário: RN-14 — campo não numérico
    Quando preencho com letra o tipo de contrato, o grupo de licitação, uma das datas ou uma das coordenações
    Então a tela recusa o campo antes de qualquer leitura
    E o cursor volta ao campo recusado
    E nada é registrado

  Cenário: RN-15 — acesso não autorizado
    Dado que o meu código de acesso não permite esta tela ou esta operação
    Quando tento abrir a tela C684T
    Então a transação é abandonada
    E nada é lido nem registrado

  Cenário: RN-16 — falha de banco durante a gravação
    Dado que a gravação do pedido falha no banco
    Quando confirmo a exclusão
    Então a transação é interrompida com o tratamento de erro do sistema
    E a exclusão não é considerada registrada
```
