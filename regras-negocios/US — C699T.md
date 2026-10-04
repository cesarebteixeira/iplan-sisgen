# US — C699T — Transferir a permissão para outro fornecedor e outro tipo de contrato

## Estória

Como **servidor de CRE**, quero **transferir a permissão de licitação de um fornecedor e de um
tipo de contrato para outro fornecedor e outro tipo de contrato**, para que **a permissão
acompanhe o fornecimento quando a empresa ou o tipo de contrato muda**.

A permissão é o registro que prende as quantidades e os valores de um grupamento de licitação a
um fornecedor, a um tipo de contrato e a um período. Quando o fornecimento passa para outra
empresa, ou quando o contrato muda de tipo, a permissão tem de acompanhar — e é essa troca que a
tela faz: ela reescreve o fornecedor e o tipo de contrato das permissões que já existem e deixa
todo o resto como estava. A tela não cria permissão e não apaga permissão: só transfere. Sem
isso, as telas que operam sobre a permissão continuariam lendo o fornecedor antigo.

## Contexto

Jornada S000M → C000M → C050M → C060M → C699T.
Ator: servidor de CRE — transfere a permissão de licitação do seu tipo de órgão para outro
fornecedor e outro tipo de contrato.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**,
não regra de negócio.

Os três menus antes da tela apenas encaminham: não gravam nada e não passam registro nem
operação adiante. O que a tela usa da sessão — o tipo de órgão, a descrição do tipo de órgão, a
data do sistema, a matrícula, o código de acesso, o privilégio e a CRE — é o que a entrada
deixou. A tela não é encadeada por outra: quem chega decide o que fazer na própria `C699T`, e ao
terminar ela reabre a si mesma — não há tela seguinte. O comportamento dela também não muda
conforme a tela que a chamou: ela não compara a tela de origem com nenhum código de tela e abre
sempre com a opção de alteração já preenchida. Da tela anterior guarda apenas a identificação de
origem, que é enviada às conferências de perfil e de rota e vai registrada na auditoria.

As regras abaixo são só as da **tela desta jornada**.

## Regras de negócio

### RN-01 — Esta tela transfere a permissão; ela não inclui e não apaga permissão

A tela troca, nas permissões que já existem, o fornecedor e o tipo de contrato. Cada permissão
do grupo e do grupamento de licitação, no período limite informado, que hoje está no fornecedor
de origem e no tipo de contrato de origem passa a ficar no fornecedor de destino e no tipo de
contrato de destino; as quantidades, os valores, o período, a classificação dos itens, o operador
e o tipo de licitação permanecem como estavam. A tela não inclui permissão e não apaga permissão:
quem inclui e quem apaga é outra tela do menu.

### RN-02 — O que a tela pede e o que ela devolve

Para achar a permissão, a tela pede o grupo, o grupamento de licitação, o limite do período e o
par de origem — tipo de contrato e fornecedor; para onde a permissão vai, ela pede o par de
destino — tipo de contrato e fornecedor. São **oito dados em doze campos**, porque cada uma das
duas datas é pedida em dia, mês e ano. Ao todo a tela tem **vinte campos de edição**: os doze dos
oito dados, a opção de manutenção, a identificação da tela de origem, o campo da resposta de
confirmação e os cinco do cabeçalho. Fora da edição, ela mostra a descrição do tipo de órgão, a
data do sistema, a razão social de cada fornecedor informado e o campo onde faz a pergunta de
confirmação.

### RN-03 — A tela só faz alteração, e a opção já vem preenchida

Ao abrir, a tela já traz a opção de manutenção preenchida com a alteração. Se essa opção chegar
diferente, a tela recusa com * Operacao nao disponivel. Use ALT * e para ali: não há, nesta tela,
caminho de consulta, de inclusão nem de exclusão.

[?] A conferência compara a opção recebida com o código interno de alteração do sistema e a
mensagem manda usar "ALT". Ou o formulário traduz o rótulo antes de enviar, ou a mensagem está
desalinhada da conferência — o mesmo desencontro já registrado em outras telas deste acervo.
Pergunta ao site; não concluo qual dos dois.

### RN-04 — O acesso, a rota e a autorização são conferidos antes de ler e de gravar

A abertura da tela confere a estação da sessão contra o cadastro de sessão do usuário; quando os
dados chegam, a alteração é conferida contra a autorização de alterar que o usuário tem naquela
tela, e a operação só segue se ele tiver essa autorização. As conferências
recebem o contexto da sessão — a tela de origem, a matrícula, o código de acesso, o privilégio, o
tipo de órgão e a CRE — e acontecem antes de qualquer leitura do tipo de contrato, do fornecedor,
da permissão ou do período, e antes de qualquer gravação. Não sendo a rota esperada, ou não
estando a operação liberada, a transação é abandonada sem ler e sem gravar.

### RN-05 — Todo dado informado passa por conferência de número

Os doze campos dos oito dados de negócio passam por conferência de número antes de qualquer
consulta: o que não for número é recusado, o cursor volta ao campo recusado e nada é lido nem
gravado. Campo deixado em branco passa por essa conferência como zero; é a exigência de cada dado
(RN-06) que decide se o branco pode seguir.

[?] O texto do aviso da conferência de número e o mapa de retorno do cursor vivem em rotinas
chamadas por nome, que não fazem parte do acervo lido; o próprio programa não escreve essa
mensagem. Não sei, portanto, que frase o usuário vê quando digita uma letra. Pergunta ao site.

### RN-06 — Sete dados são exigidos, cada um com o seu aviso

A tela exige, nesta ordem, o grupo, o grupamento de licitação, o limite do período, o tipo de
contrato de origem, o fornecedor de origem, o tipo de contrato de destino e o fornecedor de
destino — **sete dados**, cada um com o seu aviso e com o cursor no campo que falta. O início do
período não é exigido: quando não é informado, a tela o preenche com o início que a permissão já
tem (RN-13).

### RN-07 — Os dois tipos de contrato têm de estar cadastrados e ser do mesmo tipo de permissão

O tipo de contrato de origem é lido no cadastro de tipos de contrato do tipo de órgão do usuário;
não estando lá, a tela recusa com * Tipo contrato nao cadastrado - DE *. O tipo de contrato de
destino passa pela mesma leitura, com o seu próprio aviso; além disso, os dois têm de apontar para
o mesmo tipo de permissão no cadastro — apontando para tipos de permissão diferentes, a tela
recusa com * TC PARA diferente de TC DE *. É essa igualdade que impede que a troca mude a natureza
da permissão.

[?] O cadastro do tipo de contrato guarda um tipo de permissão de um único caractere e o corpus
não define o que ele significa em negócio; o que a tela faz é exigir que origem e destino tenham o
mesmo valor. Pergunta ao site.

### RN-08 — Os dois fornecedores têm de estar cadastrados, e a tela mostra a razão social de cada um

O fornecedor de origem e o de destino são lidos no cadastro de fornecedores; não estando lá, a
tela recusa com o aviso de cada lado — * Fornecedor nao cadastrado - DE * e * Fornecedor nao
cadastrado - PARA *. Achado o cadastro, a tela mostra a razão social do fornecedor ao lado do
código informado.

### RN-09 — O fornecedor de origem não pode estar excluído nem purgado

Antes de gravar, a tela relê o cadastro do fornecedor de origem e recusa a transação quando o
registro está marcado com a situação de excluído ou com a de purgado; a recusa interrompe a
operação antes da gravação.

[?] O texto dessa recusa é pedido por número a uma rotina de comunicação que não faz parte do
acervo lido, e o corpus não traz o cadastro de mensagens: não sei que frase o usuário vê. O
corpus também não diz se o mesmo impedimento vale para o fornecedor de destino — a releitura só é
feita para o de origem. Pergunta ao site.

### RN-10 — A permissão de origem tem de existir e não pode ter quantidade comprometida

A tela procura a permissão pelo tipo de órgão do usuário, pelo grupo, pelo grupamento de licitação,
pelo limite do período e pelo par de origem. Não achando, recusa com * Permissao nao cadastrada
neste grupamento *. Achando, confere a quantidade comprometida de cada permissão que casa: se
alguma estiver com a quantidade pedida ou com a temporária diferente de zero, recusa com *
Permissao com quant.comprometidas - DE * — a troca não é permitida sobre permissão com compromisso.

[?] O corpus dá os nomes das duas quantidades comprometidas — a pedida e a temporária — e a
mensagem fala em "quant. comprometidas", mas não define o que cada uma é em negócio. Pergunta ao
site.

[?] A tela não confere o grupo informado contra a CRE da sessão, embora trate os dois como o mesmo
código ao registrar a auditoria. Se o servidor pode operar o grupo de outra CRE, o site confirma.

### RN-11 — O tipo de contrato de destino não pode já ter permissão em outro período no mesmo grupo

A tela percorre as permissões do tipo de contrato de destino naquele grupo e recusa se encontrar
alguma com um limite de período diferente do informado: * TC ja cadastrado para outro periodo -
PARA *. Se as que existirem tiverem o mesmo limite, a operação segue — a troca mantém o período.

### RN-12 — A permissão de destino não pode já existir

Com o fornecedor de destino, o tipo de contrato de destino e o limite informado, a tela procura a
permissão naquele grupo e grupamento; se ela já existir, recusa com * Permissao ja cadastrada -
PARA * e nada é gravado. É o espelho da exigência da permissão de origem (RN-10): o destino tem de
estar livre.

### RN-13 — O início do período vem da permissão, não do formulário

Os três campos do início do período passam pela conferência de número, mas não entram em nenhuma
procura e não são gravados na permissão. Achada a permissão de origem, a tela copia o início que
está na própria permissão; é esse início que ela devolve ao formulário no lugar do que foi
digitado, e é ele que vai para o período do tipo de contrato de destino. Quem informa um início
diferente vê o campo voltar com o valor do cadastro.

[?] Ou os três campos do início são, na prática, de leitura — e a máscara os apresenta como
digitáveis porque a conferência de número os aceita —, ou a tela deveria usá-los e ignora o que o
operador informa. Pergunta ao site; não concluo qual dos dois.

### RN-14 — A tela não enxerga permissão excluída nem permissão sem grupamento

As procuras de permissão desta tela não alcançam os registros marcados como excluídos nem os que
estão sem grupamento de licitação: esses registros ficam fora do que a tela lê e grava.

### RN-15 — A troca é em dois tempos: a tela pergunta e só grava com "S"

No primeiro envio não há gravação: a tela confere tudo, guarda os dados de identificação e pergunta
"Altera fornecedor da permissao <S/N>?" no campo de mensagem, com o cursor na resposta. A gravação
só acontece quando a resposta é "S" e quando os **nove dados de identificação** guardados — o
grupo, o grupamento, o limite do período, os dois tipos de contrato e os dois fornecedores —
continuam iguais aos da pergunta; se algum deles mudou, a tela descarta a pergunta e recomeça a
conferência desde o princípio. Resposta diferente de "S" cancela: a tela não grava.

### RN-16 — Confirmada, a troca reescreve o fornecedor e o tipo de contrato de cada permissão de origem

Confirmada a troca, a tela percorre as permissões do par de origem e, em cada uma, substitui o
tipo de contrato e o fornecedor pelos de destino, preservando todos os demais dados — e grava. Ao
terminar, mostra * Cadastro atualizado *. A troca alcança as permissões daquela combinação de
grupo, grupamento, limite do período, tipo de contrato e fornecedor de origem.

[?] A procura da permissão fixa em zero a classe, a subclasse e o gênero dos itens, mas a
conferência que confirma o registro encontrado não compara esses três dados. Não se conclui do
corpus se a troca alcança a permissão cujo item tem classe, subclasse ou gênero diferente de zero,
nem quantas permissões a repetição alcança quando a combinação tem mais de uma. Pergunta ao site.

[?] O tipo de contrato faz parte das chaves de acesso da permissão, e o conjunto de dados que a
tela usa para gravar não declara que a chave pode mudar — o que outros conjuntos do mesmo cadastro
declaram. Se o banco aceita a gravação que troca o tipo de contrato, ou se ela é recusada, não se
conclui do corpus. Pergunta ao site.

### RN-17 — O período do tipo de contrato de destino passa a existir

Depois da troca, a tela verifica se já existe o período do tipo de contrato de destino para aquele
grupo, aquele grupamento de licitação e aquele limite. Não existindo, ela cria o período com o
início que estava na permissão, o limite informado, o tipo de licitação e o operador que estavam
na permissão, e com a descrição do período marcada como atualização feita por esta tela. Existindo,
ela não mexe nele.

[?] O corpus não define, em negócio, o que é o período guardado por esse cadastro — a tela que o
mantém é outra, do mesmo menu, e nenhuma das duas explica para que ele serve. Pergunta ao site.

### RN-18 — Toda gravação deixa rastro na auditoria

Cada permissão trocada deixa um registro na auditoria com o tipo de órgão, o grupo, o cadastro que
originou a operação, a operação de alteração, a matrícula, a estação, a data e a hora, e o
conteúdo da permissão antes e depois da troca. A criação do período de destino também deixa o seu
registro, com a operação de inclusão e o período do lado do depois. A leitura, a conferência e as
recusas não deixam rastro.

### RN-19 — Abrir a tela e cancelar a confirmação não gravam nada

Abrir a tela não procura permissão nem período e não grava: apenas monta o formulário com a opção
de alteração preenchida e lê o cadastro da tela e a descrição do tipo de órgão. Nenhuma recusa das
conferências grava, e responder à pergunta de confirmação com qualquer coisa diferente de "S"
também não — a transação termina sem tocar no banco.

### RN-20 — Falha de banco interrompe a transação

Toda leitura e toda gravação testam o erro do banco; quando ele acontece, a transação é despachada
para o tratamento de erro do sistema e a gravação que falhou não é considerada feita.

[?] O que a rotina de comunicação do sistema faz com a transação não está no acervo lido; se ela
não interromper, o aviso é dado e o processamento pode seguir para a próxima permissão da
combinação. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Transferir a permissão para outro fornecedor e outro tipo de contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C699T

  Cenário: Abrir a tela não procura permissão e não grava nada
    Quando abro a tela C699T
    Então vejo o formulário com a opção de manutenção já preenchida com a alteração
    E vejo a descrição do tipo de órgão e a data do sistema
    E nenhuma permissão é procurada e nada é gravado

  Cenário: Opção de manutenção diferente da alteração é recusada
    Dado que a opção de manutenção chega diferente da alteração
    Quando a tela confere a opção
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT *"
    E o cursor volta para o campo da opção
    E nada é lido e nada é gravado

  Cenário: Dado informado que não é número é recusado
    Dado que informo em um dos dados algo que não é número
    Quando a tela confere os dados
    Então o dado é recusado
    E o cursor volta ao campo recusado
    E nada é lido e nada é gravado

  Cenário: O grupo não informado é cobrado
    Dado que deixo o grupo em branco
    Quando confirmo os dados
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor fica no campo do grupo
    E nada é gravado

  Cenário: O grupamento de licitação não informado é cobrado
    Dado que deixo o grupamento de licitação em branco
    Quando confirmo os dados
    Então vejo a mensagem "* Informe o grupamento *"
    E o cursor fica no campo do grupamento
    E nada é gravado

  Cenário: O limite do período não informado é cobrado
    Dado que deixo o dia do limite do período em branco
    Quando confirmo os dados
    Então vejo a mensagem "* Informe data limite da permissao *"
    E o cursor fica no campo do dia do limite
    E nada é gravado

  Cenário: O tipo de contrato de origem não informado é cobrado
    Dado que deixo o tipo de contrato de origem em branco
    Quando confirmo os dados
    Então vejo a mensagem "* Informe o tipo contrato - DE *"
    E nada é gravado

  Cenário: O tipo de contrato de destino não informado é cobrado
    Dado que deixo o tipo de contrato de destino em branco
    Quando confirmo os dados
    Então vejo a mensagem "* Informe o tipo contrato - PARA *"
    E nada é gravado

  Cenário: O fornecedor de origem não informado é cobrado
    Dado que deixo o fornecedor de origem em branco
    Quando confirmo os dados
    Então vejo a mensagem "* Informe o fornecedor - DE *"
    E nada é gravado

  Cenário: O fornecedor de destino não informado é cobrado
    Dado que deixo o fornecedor de destino em branco
    Quando confirmo os dados
    Então vejo a mensagem "* Informe o fornecedor - PARA *"
    E nada é gravado

  Cenário: Tipo de contrato de origem não cadastrado
    Dado que o tipo de contrato de origem informado não está no cadastro do meu tipo de órgão
    Quando confirmo os dados
    Então vejo a mensagem "* Tipo contrato nao cadastrado - DE *"
    E o cursor volta ao tipo de contrato de origem
    E nada é gravado

  Cenário: Tipo de contrato de destino não cadastrado
    Dado que o tipo de contrato de destino informado não está no cadastro do meu tipo de órgão
    Quando confirmo os dados
    Então vejo a mensagem "* Tipo contrato nao cadastrado - PARA *"
    E o cursor volta ao tipo de contrato de destino
    E nada é gravado

  Cenário: Tipos de contrato de naturezas diferentes são recusados
    Dado que o tipo de contrato de origem e o de destino não apontam para o mesmo tipo de permissão
    Quando confirmo os dados
    Então vejo a mensagem "* TC PARA diferente de TC DE *"
    E nada é gravado

  Cenário: Fornecedor de origem não cadastrado
    Dado que o fornecedor de origem informado não está no cadastro de fornecedores
    Quando confirmo os dados
    Então vejo a mensagem "* Fornecedor nao cadastrado - DE *"
    E o cursor volta ao fornecedor de origem
    E nada é gravado

  Cenário: Fornecedor de destino não cadastrado
    Dado que o fornecedor de destino informado não está no cadastro de fornecedores
    Quando confirmo os dados
    Então vejo a mensagem "* Fornecedor nao cadastrado - PARA *"
    E o cursor volta ao fornecedor de destino
    E nada é gravado

  Cenário: A tela mostra a razão social dos fornecedores informados
    Dado que informo um fornecedor de origem e um de destino cadastrados
    Quando confirmo os dados
    Então vejo a razão social ao lado de cada código informado

  Cenário: Fornecedor de origem excluído ou purgado é recusado
    Dado que o fornecedor de origem está marcado como excluído ou como purgado
    Quando confirmo os dados
    Então a operação é recusada
    E nada é gravado

  Cenário: Permissão de origem não cadastrada no grupamento
    Dado que não existe permissão para o grupo, o grupamento, o período e o par de origem informados
    Quando confirmo os dados
    Então vejo a mensagem "* Permissao nao cadastrada neste grupamento *"
    E nada é gravado

  Cenário: Permissão de origem com quantidade comprometida
    Dado que a permissão de origem existe e tem quantidade pedida ou temporária
    Quando confirmo os dados
    Então vejo a mensagem "* Permissao com quant.comprometidas - DE *"
    E nada é gravado

  Cenário: O tipo de contrato de destino já tem permissão em outro período
    Dado que o tipo de contrato de destino já tem permissão naquele grupo em um limite de período diferente
    Quando confirmo os dados
    Então vejo a mensagem "* TC ja cadastrado para outro periodo - PARA *"
    E nada é gravado

  Cenário: A permissão de destino já existe
    Dado que já existe permissão do fornecedor e do tipo de contrato de destino, naquele período
    Quando confirmo os dados
    Então vejo a mensagem "* Permissao ja cadastrada - PARA *"
    E nada é gravado

  Cenário: O início do período volta com o valor da permissão
    Dado que a permissão de origem existe e informo um início de período diferente do dela
    Quando a tela encontra a permissão
    Então os campos do início do período voltam com o início que está na permissão
    E é esse início que vai para o período do tipo de contrato de destino

  Cenário: A troca é pedida antes de ser gravada
    Dado que a permissão de origem existe, sem quantidade comprometida, e o destino está livre
    Quando confirmo os dados
    Então vejo a pergunta "Altera fornecedor da permissao <S/N>?" no campo de mensagem
    E o cursor fica na resposta
    E nada foi gravado ainda

  Cenário: Responder "S" grava a troca e confirma
    Dado que a tela já pediu a confirmação e os dados de identificação não mudaram
    Quando respondo "S"
    Então cada permissão daquela combinação passa para o fornecedor e o tipo de contrato de destino
    E os demais dados de cada permissão não mudam
    E nenhuma permissão é criada e nenhuma é apagada
    E vejo a mensagem "* Cadastro atualizado *"

  Cenário: Responder diferente de "S" cancela e não grava
    Dado que a tela já pediu a confirmação
    Quando respondo qualquer coisa diferente de "S"
    Então a transação termina sem gravar
    E nada é tocado no cadastro de permissões

  Cenário: Mudar um dado de identificação depois da pergunta recomeça a conferência
    Dado que a tela já pediu a confirmação
    Quando mudo o grupo, o grupamento, o limite do período, um tipo de contrato ou um fornecedor
    Então a pergunta é descartada
    E a tela refaz a conferência desde o princípio
    E nada é gravado

  Cenário: O período do tipo de contrato de destino passa a existir
    Dado que a permissão foi transferida para o fornecedor e o tipo de contrato de destino
    E que o período daquele tipo de contrato ainda não existe para o grupo, o grupamento e o limite informados
    Quando a tela conclui a troca
    Então o período é criado com o início que estava na permissão, o limite informado, o tipo de licitação e o operador da permissão
    E o período fica com a marca de que foi atualizado por esta tela

  Cenário: O período do tipo de contrato de destino já existente não é alterado
    Dado que o período daquele tipo de contrato já existe para o grupo, o grupamento e o limite informados
    Quando a tela conclui a troca
    Então o período existente não é alterado

  Cenário: Toda gravação deixa rastro na auditoria
    Dado que a troca foi confirmada e gravada
    Então cada permissão trocada deixa um registro na auditoria com a operação de alteração, a matrícula, a estação, a data, a hora e o conteúdo de antes e de depois
    E a criação do período de destino também deixa o seu registro na auditoria

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não tem a autorização de alterar nesta tela
    Quando confirmo os dados
    Então a operação é recusada
    E a transação é abandonada sem ler e sem gravar

  Cenário: Rota não esperada para a tela de origem
    Dado que cheguei à C699T por uma tela de origem diferente da esperada
    Quando a tela confere a rota
    Então a transação é abandonada
    E nada é lido e nada é gravado

  Cenário: Falha de banco interrompe a transação
    Dado que a leitura ou a gravação falha no banco
    Quando confirmo a troca
    Então a transação é despachada para o tratamento de erro do sistema
    E a gravação que falhou não é considerada feita
```
