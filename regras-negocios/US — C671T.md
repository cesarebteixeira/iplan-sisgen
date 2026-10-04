# US — C671T — Correção do período do contrato

## Estória

Como **servidor da Coordenação Regional Escolar (CRE)**, quero **corrigir as datas de
início e de limite do período de um contrato já cadastrado para a minha coordenação
regional**, para que **a vigência errada deixe de valer em todo o sistema, sem precisar
excluir e recadastrar o contrato**.

O período — as datas de início e de limite — é a vigência que o contrato, a coordenação
regional, o fornecedor e o órgão filho compartilham: as mesmas datas valem em quatro
cadastros, e tudo o que foi lançado dentro do período se apoia nelas. Quando a vigência é
cadastrada errada, o que depende dela fica errado junto. Esta tela existe para mover o
período já registrado, no lugar de obrigar a refazer o cadastro — e só enquanto não houver
pedido dentro do período: depois do primeiro pedido, a vigência deixa de ser corrigível por
aqui.

## Contexto

Jornada S000M → C000M → C050M → C671T.

Ator: servidor de CRE — corrige, para a sua coordenação regional e para um tipo de
contrato, as datas de um período que foi cadastrado errado.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A tela anterior da jornada abre esta por chamada direta, sem passar registro nem operação:
esta tela monta sozinha a sua chave, com o que a sessão já carrega — o tipo de órgão, a
coordenação regional, a matrícula, o código de acesso, o privilégio e a data do sistema — e
com o que o operador digita. O que ela consome da sessão pertence ao arquivo da entrada, e
está no anexo, em "Regras que se revelaram da entrada".

Esta é a última tela da jornada: ela não entrega registro nem operação a nenhuma tela
seguinte — quando o operador confirma, ela reabre a si mesma.

---

## Regras de negócio

### RN-01 — A tela corrige um período já cadastrado; não inclui e não exclui cadastro

Esta tela tem uma única operação: reescrever as datas de um período que já está
registrado. Ela não cria cadastro novo e não apaga cadastro nenhum — o período anterior
deixa de existir porque é sobrescrito, não porque foi removido. A conferência que antecede
a gravação, sozinha, não altera nada: enquanto o operador não confirmar, nenhum cadastro é
tocado e nenhum registro de auditoria é criado. O que a confirmação deixa é a vigência nova
nos cadastros de período e um registro na auditoria do sistema.

[?] O nome de negócio desta tela não vem do material: o título que ela exibe é lido do
cadastro de títulos do sistema, que não faz parte do lote. "Correção do período do
contrato" é leitura de negócio, não transcrição. Pergunta ao site.

### RN-02 — O mesmo período vale em quatro cadastros, e a correção vale para os quatro

A vigência do contrato é guardada em quatro cadastros, cada um do seu ponto de vista: o das
permissões de contrato, que é onde a vigência é conferida e reescrita, com capacidade para
**1.000.000** de registros; o do período por coordenação regional, que guarda também a
descrição do período, com **10.000**; o do período por fornecedor, subclasse e gênero, que
guarda o saldo inicial do período, com **100**; e o do período por fornecedor, gênero e
órgão filho, também com **100**. Capacidade é o máximo esperado — parâmetro de
dimensionamento —, não o que está cadastrado. A correção vale para os quatro: as mesmas
datas são reescritas em todos.

[?] O nome de negócio do código de órgão do cadastro por órgão filho não está na tela desta
jornada: a máscara, que traz os rótulos que o usuário lê, não faz parte do material. "Órgão
filho" é o nome que o mesmo código tem em outra tela do sistema. Pergunta ao site.

### RN-03 — A correção é identificada pela coordenação regional, pelo tipo de contrato e pela data limite do período atual

Para corrigir, o operador informa a coordenação regional, o tipo de contrato e a data limite
do período que está errado — dia, mês e ano. É por essa combinação, mais o tipo de órgão da
sessão, que a tela procura a permissão de contrato. A data de início do período atual não é
digitada: a tela traz do cadastro o início registrado e descarta o que o operador tenha
escrito nela. No cabeçalho, a tela mostra a descrição do tipo de órgão da sessão, a data do
sistema e a descrição do contrato, esta última buscada pelo tipo de órgão e pelo tipo de
contrato informado — não achando a descrição, a tela segue sem reclamar.

### RN-04 — Só o modo de alteração passa

O modo de manutenção que a tela aceita é o de **alteração**. Chegando com qualquer outro
modo, a tela recusa com * Opcao nao disponivel. Use ALT *, devolve o cursor ao campo do
modo e não confere nem grava nada; não há nesta tela modo de consulta. Ao se apresentar, a
própria tela já se coloca no modo de alteração, de modo que a recusa só aparece quando a
transação chega de outro modo.

[?] A palavra que o operador precisa informar no campo do modo é carregada da tabela de
mensagens do idioma, que não faz parte do material, e a mensagem da recusa nomeia ALT. Se
ALT é a palavra que o sistema carrega para a alteração, a guarda e a mensagem combinam; se
não é, a tela recusa justamente o que a mensagem manda usar. Pergunta ao site.

### RN-05 — A coordenação regional, o tipo de contrato e a data limite do período atual são obrigatórios

Deixando em branco a coordenação regional, o tipo de contrato ou o dia da data limite do
período atual, a tela recusa e devolve o cursor ao campo: * Informe o grupo * para a
coordenação regional — a mensagem chama esse campo de **grupo** —, * Informe o tipo
contrato * para o tipo de contrato e * Informe a data limite do periodo atual * para a data
limite. Em qualquer dos três casos nada é conferido dali para a frente e nada é gravado.

### RN-06 — Sem a permissão de contrato para a coordenação e a data limite informadas, a correção é recusada

A vigência tem de estar registrada no cadastro das permissões de contrato para o tipo de
órgão da sessão, a coordenação regional, o tipo de contrato e a data limite informados. Não
estando, a recusa é * Permissao nao cadastrada *, com o cursor na data limite, e nada mais
é conferido nem gravado.

[?] A conferência procura a permissão pela coordenação, pela data limite e pelo tipo de
contrato e também pela classe, pela subclasse e pelo gênero — estes últimos em branco,
porque a tela não os informa —, mas depois só compara os quatro primeiros. Se a procura
exige a combinação inteira, a tela não acha as permissões que têm classe, subclasse ou
gênero preenchidos; se ela apenas se posiciona no registro igual ou posterior, a correção
pode alcançar mais de uma permissão da mesma coordenação e do mesmo tipo de contrato,
porque a gravação não filtra por essas classificações. O material lido não diz qual dos dois
comportamentos vale. Pergunta ao site.

### RN-07 — Havendo pedido dentro do período atual, a correção é recusada

Antes de conferir as datas novas, a tela procura os pedidos da subclasse e do gênero do
período — os mesmos da permissão de contrato que acabou de ler — e recusa quando encontra um
pedido com data igual ou anterior à data limite do período atual e do tipo de contrato
informado: * Ja existem pedidos cadastrados *, com o cursor na data limite. É a garantia de
que uma vigência já usada por pedidos não é movida por baixo deles.

[?] A conferência olha uma única data do pedido — a primeira das cinco que o registro
guarda — e só até a data limite do período; um pedido datado depois do limite, ou lançado
nas outras quatro datas do registro, não é visto por ela. Se isso cobre todos os pedidos do
período, o material lido não responde. Pergunta ao site.

### RN-08 — As datas do novo período têm de ser datas válidas

As duas datas informadas — início e limite do novo período — passam pela conferência de
calendário: data que não existe no calendário é recusada, e o ano tem de estar entre 1994 e
2099. A recusa da data inicial é * Nova data inicial invalida * e a da final é * Nova data
final invalida *, cada uma com o cursor na sua data.

[?] A conferência do calendário é feita por rotina do ambiente de execução, que não tem
corpo no material: o que ela devolve para uma data recusada não está documentado, e é esse
retorno que dispara a mensagem. A leitura feita aqui é a que o resto do acervo sustenta —
recusa quando a rotina aponta problema —, mas a convenção do retorno não está no lote.
Pergunta ao site.

### RN-09 — O novo período não pode ter as duas datas iguais, nem a data inicial depois da data final

Com as duas datas válidas, a tela ainda exige que o novo período tenha começo e fim
distintos — datas iguais recusam com * Data do novo periodo invalida * — e que a data
inicial não seja posterior à final: * Data inicial maior que data final *. As duas recusas
apontam o cursor para a data inicial do novo período.

### RN-10 — A correção só é aplicada depois de confirmada

Passadas as conferências, a tela não grava: ela mostra * Confirma correcao do periodo
<S/N> ? *, com o cursor no campo da resposta, e reabre a si mesma esperando a resposta. Só
a resposta **S** aplica a correção; qualquer outra resposta, inclusive em branco, volta à
conferência sem gravar nada. Se o operador alterar qualquer um dos dados informados antes de
responder, a tela descarta a confirmação e refaz a conferência inteira. Nada muda, portanto,
enquanto a resposta não for S.

### RN-11 — Confirmada, a correção reescreve as datas nos quatro cadastros

Respondida a confirmação com S, a tela reescreve as datas do período nos quatro cadastros
que guardam a vigência. No cadastro das permissões de contrato e no do período por
coordenação regional, além do início e do limite, o limite inicial do período também passa a
ser o novo limite.

O alcance não é o mesmo nos quatro. No cadastro das permissões de contrato e no do período
por coordenação regional, a varredura percorre **todos** os registros daquela coordenação
regional e daquele tipo de contrato — qualquer fornecedor, classe, subclasse, gênero e data
de limite —, e não apenas o período informado. Já no cadastro por fornecedor, subclasse e
gênero e no do órgão filho, a varredura se limita aos registros cujo limite é o período
atual informado, mas alcança todas as subclasses, gêneros, fornecedores e órgãos filhos.
Em nenhum dos quatro a varredura toca registros de outra coordenação regional. Terminada a
gravação, a tela avisa * Cadastro sendo atualizado * e reabre a si mesma.

[?] As datas do período fazem parte da chave dos cadastros que a correção reescreve, e só um
deles está declarado como preparado para gravar com a chave alterada. Se o sistema exigir
essa preparação também nos outros três, a reescrita pode não se efetivar neles. Pergunta ao
site.

[?] O cadastro do período por coordenação regional guarda uma descrição do período, que esta
tela não lê nem reescreve: se a descrição registra as datas, ela fica desatualizada depois
da correção. Pergunta ao site.

[?] No cadastro das permissões de contrato e no do período por coordenação regional a
varredura vai além do período que o operador informou e identificou: a correção reescreve
todos os períodos daquela coordenação regional e daquele tipo de contrato. Se eras
anteriores ou posteriores do mesmo contrato devem andar junto, ou se a correção deveria
alcançar só o período informado, o material lido não decide. Pergunta ao site.

### RN-12 — A correção fica registrada na auditoria como uma inclusão do período

Antes de reescrever os cadastros, a gravação deixa um registro na auditoria: o objeto
auditado é a própria tela, a operação é registrada com a palavra de **inclusão** do sistema,
e o valor anterior recebe um bloco de **39 posições** com o tipo de órgão, o período atual
(início e limite), o período novo (início e limite), o tipo de contrato e a coordenação
regional informada; o valor posterior fica em branco. O registro leva ainda a matrícula, a
coordenação regional da sessão, o tipo de órgão, o terminal, a data e a hora da sessão, e um
número de processo montado com a coordenação regional informada, o tipo de contrato e a data
limite nova — 13 dígitos em um campo de 14. A capacidade do cadastro de auditoria é de
**60.000.000** de registros. Antes de gravar a auditoria, a tela desliga a distribuição
automática entre destinos, de modo que a recusa de destino inválido não acontece por aqui.

[?] A correção é registrada com a palavra de inclusão, e não com a de alteração, e o valor
posterior fica em branco: o período novo só se recupera pelo bloco do valor anterior e pelo
número do processo. Se essa é a trilha pretendida para uma correção, o material lido não
diz. Pergunta ao site.

[?] A palavra que rotula a operação na auditoria vem da tabela de mensagens do idioma, que
não faz parte do material: o que o auditor lê no registro é essa palavra, não um texto fixo
do programa. Pergunta ao site.

[?] A coordenação regional gravada no campo próprio da auditoria é a da sessão, e a
coordenação corrigida vai no número do processo e no bloco do período: corrigindo uma
coordenação diferente da da sessão, o registro aponta as duas. Se é o pretendido, o material
não diz. Pergunta ao site.

### RN-13 — Nada é conferido nem gravado sem a autorização de perfil, de rota e de operação

Antes de conferir e antes de gravar, a tela passa pelas rotinas de segurança do sistema: a
de perfil, a de rota e a de permissão por operação, levando o tipo de órgão, a coordenação
regional, a matrícula, o código de acesso e o privilégio da sessão. Não voltando "OK" de
qualquer uma delas, a transação é abandonada: nada é conferido, nada é gravado e nenhum
registro de auditoria é criado. A data e a hora que vão para a auditoria também passam por
rotina do ambiente, e a falha dela interrompe a gravação.

[?] As rotinas de segurança e a de rota só aparecem declaradas, sem corpo no material: a
regra efetiva de quem pode corrigir um período não pode ser lida nesta jornada. Pergunta ao
site.

[?] O prefixo da tela de origem é repassado à lógica de rota como contexto, mas — diferente
de outras telas do acervo — nada nesta tela interrompe a conferência por causa dele, e o que
preenche esse prefixo também não está no material. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Correção do período do contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a matrícula, a coordenação regional, o código de acesso, o privilégio e a data do sistema
    E tenho acesso à tela C671T

  Cenário: RN-01 — a correção reescreve o período e não exclui cadastro
    Dado que o período está registrado para a minha coordenação regional e o tipo de contrato informados
    Quando confirmo a correção
    Então as datas do período são reescritas nos cadastros de período
    E nenhum registro é excluído
    E o período anterior deixa de existir porque foi sobrescrito

  Cenário: RN-02 — o mesmo período vale nos quatro cadastros
    Dado que corrigi o período de um contrato da minha coordenação regional
    Quando consulto o período do contrato, o da coordenação regional, o do fornecedor e o do órgão filho
    Então os quatro mostram as datas novas

  Cenário: RN-03 — a correção é identificada pela coordenação, pelo contrato e pela data limite
    Dado que estou na tela C671T
    Quando informo a coordenação regional, o tipo de contrato e a data limite do período atual
    Então vejo a descrição do tipo de órgão, a data do sistema e a descrição do contrato
    E a tela me devolve a data de início registrada no cadastro

  Cenário: RN-03 — o que eu digitar na data de início do período atual é descartado
    Dado que estou na tela C671T
    Quando informo um valor qualquer na data de início do período atual
    Então a tela mostra a data de início que está registrada no cadastro
    E o valor que digitei não é levado em conta

  Cenário: RN-04 — modo diferente de alteração é recusado
    Dado que estou na tela C671T
    Quando a transação chega com um modo de manutenção diferente do de alteração
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-05 — a coordenação regional é obrigatória
    Dado que estou na tela C671T
    Quando deixo a coordenação regional em branco
    Então vejo "* Informe o grupo *"
    E o cursor fica nesse campo
    E nada é gravado

  Cenário: RN-05 — o tipo de contrato é obrigatório
    Dado que estou na tela C671T
    Quando deixo o tipo de contrato em branco
    Então vejo "* Informe o tipo contrato *"
    E o cursor fica nesse campo
    E nada é gravado

  Cenário: RN-05 — a data limite do período atual é obrigatória
    Dado que estou na tela C671T
    Quando deixo o dia da data limite do período atual em branco
    Então vejo "* Informe a data limite do periodo atual *"
    E o cursor fica nessa data
    E nada é gravado

  Cenário: RN-06 — sem permissão de contrato para a coordenação e a data limite
    Dado que estou na tela C671T
    Quando informo uma coordenação regional e uma data limite que não têm permissão de contrato cadastrada
    Então vejo "* Permissao nao cadastrada *"
    E o cursor fica na data limite
    E nada é gravado

  Cenário: RN-07 — há pedido dentro do período atual
    Dado que a permissão de contrato existe
    E que há um pedido do mesmo tipo de contrato com data dentro do período atual
    Quando informo datas novas válidas
    Então vejo "* Ja existem pedidos cadastrados *"
    E o cursor fica na data limite
    E nada é gravado

  Cenário: RN-08 — a data inicial do novo período não é válida
    Dado que a permissão de contrato existe e não há pedido dentro do período
    Quando informo uma data de início que não existe no calendário
    Então vejo "* Nova data inicial invalida *"
    E o cursor fica nessa data
    E nada é gravado

  Cenário: RN-08 — a data final do novo período não é válida
    Dado que a permissão de contrato existe e não há pedido dentro do período
    Quando informo uma data limite que não existe no calendário
    Então vejo "* Nova data final invalida *"
    E o cursor fica nessa data
    E nada é gravado

  Cenário: RN-09 — as duas datas do novo período são iguais
    Dado que a permissão de contrato existe e não há pedido dentro do período
    Quando informo a mesma data para o início e para o limite do novo período
    Então vejo "* Data do novo periodo invalida *"
    E o cursor fica na data inicial
    E nada é gravado

  Cenário: RN-09 — a data inicial é posterior à final
    Dado que a permissão de contrato existe e não há pedido dentro do período
    Quando informo uma data de início posterior à data limite
    Então vejo "* Data inicial maior que data final *"
    E o cursor fica na data inicial
    E nada é gravado

  Cenário: RN-10 — a tela pede confirmação antes de gravar
    Dado que a permissão de contrato existe, não há pedido dentro do período e as datas novas são válidas
    Quando envio os dados da correção
    Então vejo "* Confirma correcao do periodo <S/N> ? *"
    E o cursor fica no campo da resposta
    E a correção ainda não foi aplicada

  Cenário: RN-01 e RN-10 — a conferência não grava nada
    Dado que estou na tela C671T com os dados de uma correção possível
    Quando a tela confere as datas e me pede a confirmação
    Então nenhum cadastro de período foi alterado
    E nenhum registro de auditoria foi criado

  Cenário: RN-10 — resposta diferente de S não grava
    Dado que a tela me pediu a confirmação da correção
    Quando respondo N, ou deixo a resposta em branco
    Então a correção não é aplicada
    E nenhum cadastro é alterado

  Cenário: RN-10 — alterar os dados antes de responder refaz a conferência
    Dado que a tela me pediu a confirmação da correção
    Quando altero uma das datas e envio a resposta S
    Então a tela descarta a confirmação
    E confere tudo de novo antes de gravar
    E nada foi gravado

  Cenário: RN-11 — resposta S aplica a correção
    Dado que a permissão de contrato existe, não há pedido dentro do período e as datas novas são válidas
    Quando respondo S à confirmação
    Então as datas do período são reescritas nos quatro cadastros
    E vejo "* Cadastro sendo atualizado *"

  Cenário: RN-11 — o limite inicial do período passa a ser o novo limite
    Dado que confirmei a correção de um período
    Quando consulto o cadastro das permissões de contrato e o do período por coordenação regional
    Então o início e o limite do período são as datas novas
    E o limite inicial do período também é o novo limite

  Cenário: RN-11 — a correção não alcança as outras coordenações regionais
    Dado que o mesmo tipo de contrato tem períodos em outra coordenação regional
    Quando confirmo a correção da minha coordenação regional
    Então só os registros da minha coordenação regional são reescritos
    E os das outras coordenações regionais ficam como estão

  Cenário: RN-12 — a correção deixa o período anterior na auditoria
    Dado que confirmei a correção de um período
    Quando a gravação termina
    Então existe um registro de auditoria do objeto C671T
    E o valor anterior leva o tipo de órgão, o período atual, o período novo, o tipo de contrato e a coordenação regional
    E leva a matrícula, a coordenação regional da sessão, o tipo de órgão, o terminal, a data e a hora
    E leva um número de processo com a coordenação regional, o tipo de contrato e a data limite nova
    E o valor posterior fica em branco

  Cenário: RN-13 — sem autorização nada é conferido nem gravado
    Dado que estou na tela C671T
    Quando a checagem de perfil, de rota ou de permissão por operação não retorna OK
    Então a transação é abandonada
    E nada é conferido, nada é gravado e nenhum registro de auditoria é criado
```
