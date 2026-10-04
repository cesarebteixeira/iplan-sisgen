# US — E059T — Alteração do fornecedor e do tipo de contrato dos pedidos

## Estória

Como **servidor de CRE**, quero **passar os pedidos de um período, de uma classe e de
um gênero do fornecedor e do tipo de contrato atuais para os novos**, para que **a
substituição do contrato não obrigue ninguém a relançar pedido por pedido**.

O pedido de fornecimento é atendido pelo fornecedor e pelo tipo de contrato que estão
nele. Quando o contrato é substituído, ou o fornecimento de um item passa para outra
empresa, os pedidos já lançados continuam apontando para o par antigo — e é por ele que
seriam atendidos. Esta tela faz a virada em conjunto: escolhe os pedidos ainda não
atendidos do fornecedor atual, de uma coordenadoria regional escolar, de um período e de
uma classe e gênero, e os passa para o fornecedor e o contrato novos. Sem ela, cada
pedido teria de ser corrigido um a um, ou ficaria preso ao contrato velho.

A tela não troca nada no momento em que o servidor confirma: ela confere o que foi
informado, mostra o que vai ser trocado, pede confirmação e deixa a atualização agendada
para o processamento, avisando que os pedidos estão sendo atualizados.

## Contexto

Jornada S000M → E000M → E010M → E059T.

Ator: servidor de CRE — informa a coordenadoria regional escolar, o início e o limite do
período, a classe e o gênero, o fornecedor e o tipo de contrato atuais e os novos, e
confirma a troca.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A tela é aberta por menu, e não encadeada por outra tela que lhe passe o registro e a
operação. O que ela usa do caminho é o que a sessão já carrega: a matrícula, o privilégio,
o tipo de órgão, a coordenadoria regional escolar, a estação e a data do sistema. As
regras abaixo são só as desta tela.

## Regras de negócio

### RN-01 — A tela só sabe alterar o fornecedor e o tipo de contrato dos pedidos

A tela se apresenta com a operação de alteração já preenchida, e é a única operação que
ela executa: não consulta, não inclui e não exclui pedido. Qualquer outra operação
informada é recusada com * Opcao nao disponivel. Use ALT *, com o cursor de volta ao
campo da operação, antes de qualquer leitura de cadastro.

[?] Quem preenche a operação ao abrir é a própria tela, e o acervo não mostra se o
servidor consegue digitar outra ali: a recusa existe, mas pode ser inalcançável por esse
caminho. E o que a mensagem quer dizer com "ALT" — se é uma tecla, se abre outra forma de
operar — também não está no acervo lido. Pergunta ao site.

### RN-02 — A tela abre sem procurar pedido

Ao ser aberta, a tela não procura pedido nenhum: mostra a data do sistema, a descrição do
tipo de órgão da sessão e a impressora que já está guardada para a matrícula, e fica
esperando. A procura de pedidos só acontece depois que o servidor informa a coordenadoria,
o período, a classe e o gênero.

[?] A data do sistema e a descrição do tipo de órgão são preenchidas na abertura e
limpas a cada digitação, sem que a tela as reponha: depois da primeira confirmação elas
podem sumir da tela. Se o quadro comum as repõe por fora, o acervo lido não mostra.
Pergunta ao site.

### RN-03 — A impressora é obrigatória e fica guardada para o servidor

Sem impressora informada, a recusa é * Informe a impressora *, com o cursor no campo da
impressora. Passando essa conferência, a impressora informada passa a ser a preferida
daquela matrícula — substituindo a anterior ou sendo guardada pela primeira vez — e isso
acontece logo no início, antes das demais conferências: a preferência fica guardada mesmo
que a operação venha a ser recusada depois, ou que a confirmação não venha.

### RN-04 — A coordenadoria é obrigatória, e quem tem coordenadoria na sessão só opera a dela

Sem coordenadoria informada, a recusa é * Informe o grupo *, com o cursor no campo da
coordenadoria. Se a sessão do servidor já está vinculada a uma coordenadoria regional
escolar, a informada tem de ser essa mesma coordenadoria; sendo outra, a recusa é
* Usuario sem acesso a este grupo *, também com o cursor no campo da coordenadoria. Se a
sessão não está vinculada a nenhuma coordenadoria, a informada tem de existir no cadastro
de coordenadorias; não existindo, a recusa é * Grupo nao cadastrado *.

[?] Quando a sessão não tem coordenadoria nenhuma, qualquer coordenadoria cadastrada é
aceita, e a que o servidor usou na operação anterior passa sem conferência de cadastro.
Se a intenção era que todo servidor só operasse a própria coordenadoria, o caminho não
garante isso. Pergunta ao site.

### RN-05 — Os campos numéricos passam por edição antes das conferências

Treze campos da tela são tratados como número: a coordenadoria, as três partes do início
do período, as três partes da data-limite, a subclasse, o gênero, o fornecedor e o tipo de
contrato atuais e os novos. Campo em branco vira zero, e o que não for número é recusado,
com o cursor devolvido ao primeiro campo recusado.

[?] Só dez desses treze campos têm posição de cursor definida — os três da data-limite
não têm. Se a digitação de uma das três partes da data-limite for recusada, o cursor não é
levado até ela. E a rotina que faz a edição não faz parte do acervo lido: o que o servidor
vê na recusa não pôde ser determinado. Pergunta ao site.

### RN-06 — A tela escolhe os pedidos do fornecedor e do contrato atuais, na classe e no gênero informados

A procura é pelos pedidos da coordenadoria informada, do fornecedor atual, ainda ativos,
que tenham itens do tipo de contrato atual, ativos, da classe e do gênero informados — ou
de qualquer classe e gênero, quando a subclasse é **99** e o gênero é **99999** — e que
não tenham nada recebido nem estornado. Não achando nenhum pedido assim, a recusa é
* Nao existem pedidos p/ forn/tc/gen nesta data *, com o cursor no dia do início do
período: a tela não agenda troca quando não há o que trocar.

[?] Se o mês e o dia informados restringem a procura. O programa leva as três partes do
período à leitura, mas do registro lido confere apenas a situação do pedido e o
fornecedor: em nenhuma linha o mês e o dia do pedido são comparados com o que foi
digitado. O que a leitura do cadastro faz com essas duas partes da chave não está
explicado no acervo: se ela não restringir, pedidos de outros meses e dias do mesmo ano
entram na troca. Pergunta ao site.

### RN-07 — A data-limite que vale é a do pedido, não a digitada

O campo da data-limite aceita digitação e passa pela edição numérica, mas, assim que a
tela encontra o primeiro pedido que serve, a data-limite é substituída pela do próprio
pedido, e é essa que vale para a conferência da permissão e para o agendamento. Na
prática, o que o servidor digitar ali não é usado por conferência nenhuma.

### RN-08 — A permissão de fornecimento tem de existir para os dois pares de fornecedor e contrato

A troca só passa quando existe permissão de fornecimento cadastrada para a coordenadoria,
na data-limite do pedido, tanto para o fornecedor e o tipo de contrato atuais quanto para
os novos, e o início do período informado é igual ou posterior ao início da vigência da
permissão. Faltando a permissão do par atual, a recusa é
* Permissao nao cadastrada para este forn/tc *, com o cursor no fornecedor atual; faltando
a do par novo, a mesma mensagem, com o cursor no fornecedor novo.

[?] A única comparação de datas que a tela faz é entre o início do período informado e o
início da vigência da permissão. O fim da vigência e o período do próprio pedido não são
conferidos pelo programa. Se a intenção era recusar o pedido fora do período da permissão,
o caminho não o faz. Pergunta ao site.

### RN-09 — O tipo de contrato novo tem de ser diferente do atual

Informando o mesmo tipo de contrato nos dois lados, a recusa é
* Informe novo tipo contrato *, com o cursor no tipo de contrato novo: a tela só troca
para um contrato diferente.

### RN-10 — A tela mostra os nomes do que vai ser trocado

Antes de pedir a confirmação, a tela mostra a razão social do fornecedor atual e a do
novo, as descrições dos dois tipos de contrato e a descrição da classe e do gênero — que
sai como **Todos** quando a subclasse informada é **99**, e continua **Todos** quando a
combinação de classe e gênero não está no cadastro.

[?] A tela mostra **Todos** sempre que a subclasse é 99, com qualquer gênero, mas só
trata a combinação como "todos" na escolha dos itens quando a subclasse é 99 **e** o
gênero é 99999: ou a exibição ou a escolha dos itens está errada para a subclasse 99 com
outro gênero. E a descrição **Todos** também aparece quando a combinação não está
cadastrada, sem que a tela avise. Pergunta ao site.

[?] A tela também não exige que o fornecedor ou o tipo de contrato estejam nos seus
cadastros: quando não estão, o nome sai em branco e a operação continua — quem decide é a
permissão de fornecimento. Se a intenção era recusar fornecedor ou contrato inexistente, o
caminho não recusa. Pergunta ao site.

### RN-11 — A tela pede confirmação, e sem "S" nada é agendado

Passando as conferências, a tela pergunta
* Confirma alteracao do fornecedor / TC <S/N> ? *, com o cursor no campo da resposta.
Nada é agendado enquanto o servidor não responder "S": resposta diferente de "S", inclusive
em branco, devolve a tela com a mesma pergunta, porque a tela confere tudo de novo. E se
entre a pergunta e a resposta o servidor mudar a coordenadoria, o período, a classe, o
gênero ou um dos dois pares de fornecedor e tipo de contrato, a confirmação é desfeita — a
tela confere tudo de novo e pergunta outra vez. Informar os dados e ver os nomes, por si
só, não agenda nada.

[?] A tela marca a pergunta de modo que o agendamento não aconteça na mesma digitação;
quem desfaz essa marca entre uma digitação e outra não está no acervo lido, e sem isso a
tela ficaria presa na pergunta. Pergunta ao site.

### RN-12 — Com uma atualização em andamento para a coordenadoria, a tela recusa

Depois da confirmação, e antes de agendar, a tela verifica se já existe uma requisição de
atualização pendente para a mesma coordenadoria. Existindo, a recusa é
* Relatorio em processamento. Aguarde. *, com o cursor no campo da resposta, e nada é
agendado. Como a conferência é posterior à pergunta, o servidor informa tudo, confirma e só
então é avisado de que há uma atualização em andamento.

[?] A conferência recusa exatamente a requisição que o próprio agendamento cria: mesma
coordenadoria, mesmo tipo de órgão, mesmo código de atualização. Se nada apagar essa
requisição quando o processamento termina, a tela agenda uma vez para cada coordenadoria e
depois fica recusando. Quem apaga a requisição — ou se ela nunca é apagada — não está nesta
jornada; a única limpeza de requisições que aparece no caminho é a da entrada, e ela só
apaga as anteriores à data inválida do sistema. Pergunta ao site.

### RN-13 — Confirmando, a tela agenda a atualização e avisa

Respondendo "S" e não havendo atualização em andamento, a tela grava uma requisição de
atualização para a coordenadoria — com o tipo de órgão, a data, a matrícula, a estação e o
código da atualização — e dispara o processamento, que é quem troca o fornecedor e o tipo
de contrato dos pedidos e dos itens. A tela então avisa * Pedidos sendo atualizados * e
volta pronta para uma nova operação. Os parâmetros da operação — o período, a classe, o
gênero, os dois pares, a impressora e o correio eletrônico do servidor — vão no pedido de
execução que a tela envia ao processamento, e não no registro da requisição.

[?] O que o processamento faz, quanto tempo leva, se apaga a requisição ao terminar e o
que o servidor vê se ele falhar não estão nesta jornada. Se o processamento depender só do
registro da requisição, ele não carrega o que foi pedido: o registro vai sem impressora e
sem os parâmetros variáveis. Pergunta ao site.

### RN-14 — A tela não altera pedido, item, fornecedor, contrato nem coordenadoria

A tela enxerga onze cadastros, e grava em dois: a impressora do servidor e a requisição do
processamento. Pedido, item de pedido, fornecedor, tipo de contrato e coordenadoria são
apenas lidos — nenhum é incluído, alterado ou excluído por ela — e a tela não apaga nada.

### RN-15 — Sem autorização para a tela ou para a operação, nada acontece

A tela só abre para o código de acesso que a tem autorizada no cadastro de telas por
código de acesso; não tendo, a recusa é * Acesso negado para esta matricula *, a tela é
abandonada e o servidor volta ao menu principal. E, antes de qualquer leitura de cadastro,
a operação de alteração tem de estar liberada para aquele código de acesso naquela tela;
não estando, a recusa é * Acesso negado para esta operacao *, e a operação é abandonada.

### RN-16 — A tela não muda conforme quem a chamou — e volta para quem a chamou

A tela não compara a tela de origem com código nenhum: ela abre sempre em alteração,
venha de onde vier, e reabre a si mesma depois da confirmação e depois de agendar. O que
ela faz com a origem é repassá-la à conferência de rota: quando a tela chega com a origem
preenchida, a rota devolve o servidor àquela tela e a operação é abandonada, sem agendar
nada. Nada é entregue a uma tela seguinte: a tela não encadeia em outra.

[?] Quem preenche a tela de origem não está no acervo lido — a tela só a repassa. Se ela
chega em branco, a rota segue e a operação acontece; se chega preenchida, a operação é
abandonada. Pergunta ao site.

### RN-17 — Falha de banco interrompe a operação

Erro de banco durante a leitura ou a gravação interrompe a operação: a tela avisa e não
completa a gravação — a requisição não é agendada e a preferência de impressora não é
gravada.

## Cenários BDD

```gherkin
Funcionalidade: Alteração do fornecedor e do tipo de contrato dos pedidos

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E059T

  Cenário: Trocar o fornecedor e o tipo de contrato dos pedidos de um período
    Dado que existem pedidos ativos do fornecedor atual, com itens do contrato atual,
      da classe e do gênero informados, sem nada recebido nem estornado
    E existe permissão de fornecimento para o par atual e para o par novo,
      na minha coordenadoria
    Quando informo a coordenadoria, o início e o limite do período, a classe, o gênero,
      o fornecedor e o contrato atuais e os novos
    Então a tela mostra as razões sociais, as descrições dos dois contratos
      e a descrição da classe e do gênero
    E me pergunta se confirmo a alteração
    Quando respondo "S"
    Então a atualização é agendada
    E vejo a mensagem "* Pedidos sendo atualizados *"

  Cenário: A tela não troca nada: ela agenda a troca
    Dado que a operação passou por todas as conferências e eu confirmei
    Então nenhum pedido e nenhum item é alterado pela tela
    E fica gravada uma requisição de atualização da minha coordenadoria,
      com o tipo de órgão, a data, a matrícula e a estação

  Cenário: A tela não grava pedido, item nem cadastro
    Dado que estou na E059T
    Quando informo os dados e peço a alteração
    Então nenhum pedido, item, fornecedor, tipo de contrato ou coordenadoria
      é incluído, alterado ou excluído
    E nada é apagado

  Cenário: Informar os dados e ver os nomes não agenda nada
    Dado que a tela já me mostrou os nomes e a pergunta de confirmação
    Então nada foi agendado: nenhuma requisição foi gravada
    E nenhum pedido mudou de fornecedor ou de tipo de contrato

  Cenário: Desistir na confirmação
    Dado que a tela já me pediu a confirmação
    Quando respondo "N", ou deixo a resposta em branco
    Então a atualização não é agendada
    E a tela confere tudo de novo e me pergunta outra vez

  Cenário: Mudar um dado depois da pergunta
    Dado que a tela já me pediu a confirmação
    Quando mudo a coordenadoria, o período, a classe, o gênero ou um dos pares
      e respondo "S"
    Então a tela confere tudo de novo
    E, estando os dados corretos, me pergunta outra vez
    E nada é agendado enquanto eu não confirmar de novo

  Cenário: Operação fora da alteração
    Quando informo uma opção diferente da alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo da operação
    E nada é lido nem agendado

  Cenário: A tela abre sem procurar pedido
    Quando abro a E059T
    Então a tela mostra a data do sistema, a descrição do tipo de órgão e a minha
      impressora preferida
    E não procura pedido nenhum enquanto eu não informar a coordenadoria e o período

  Cenário: A impressora fica guardada mesmo quando a operação é recusada
    Dado que informo uma impressora diferente da que está guardada para mim
    Quando a tela recusa a operação por qualquer outro motivo
    Então a impressora informada fica guardada como a minha preferida

  Cenário: Impressora não informada
    Dado que deixo a impressora em branco
    Quando peço a alteração
    Então vejo a mensagem "* Informe a impressora *"
    E o cursor volta ao campo da impressora
    E nada é agendado

  Cenário: Coordenadoria não informada
    Quando peço a alteração sem informar a coordenadoria
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo da coordenadoria

  Cenário: Coordenadoria diferente da minha
    Dado que a minha sessão está vinculada a uma coordenadoria regional escolar
    Quando informo outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenadoria

  Cenário: Coordenadoria que não existe no cadastro, para quem não tem coordenadoria na sessão
    Dado que a minha sessão não está vinculada a nenhuma coordenadoria regional escolar
    Quando informo uma coordenadoria que não existe no cadastro
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo da coordenadoria

  Cenário: Digitação que não é número
    Quando digito letras em um dos campos numéricos
    Então a digitação é recusada, sem chegar ao cadastro
    E o cursor volta ao campo recusado, quando a tela tem posição definida para ele

  Cenário: Sem pedidos para o fornecedor, o contrato, a classe e o gênero
    Dado que não há pedido ativo do fornecedor atual, com itens do contrato atual,
      da classe e do gênero informados, sem nada recebido nem estornado
    Quando peço a alteração
    Então vejo a mensagem "* Nao existem pedidos p/ forn/tc/gen nesta data *"
    E o cursor volta ao campo do dia do início do período
    E nada é agendado

  Cenário: A data-limite é a do pedido
    Dado que existe um pedido para a coordenadoria no período informado
    Quando informo uma data-limite diferente da do pedido
    Então a tela me mostra de volta a data-limite do pedido
    E é essa que vale para a conferência da permissão e para o agendamento

  Cenário: Permissão não cadastrada para o par atual
    Dado que não existe permissão de fornecimento para o fornecedor e o contrato atuais,
      na minha coordenadoria
    Quando peço a alteração
    Então vejo a mensagem "* Permissao nao cadastrada para este forn/tc *"
    E o cursor volta ao campo do fornecedor atual

  Cenário: Permissão não cadastrada para o par novo
    Dado que não existe permissão de fornecimento para o fornecedor ou o contrato novos
    Quando peço a alteração
    Então vejo a mesma mensagem "* Permissao nao cadastrada para este forn/tc *"
    E o cursor volta ao campo do fornecedor novo

  Cenário: Tipo de contrato novo igual ao atual
    Quando informo o mesmo tipo de contrato nos dois lados
    Então vejo a mensagem "* Informe novo tipo contrato *"
    E o cursor volta ao campo do tipo de contrato novo

  Cenário: A descrição da classe e do gênero
    Dado que a subclasse informada é 99
    Quando a tela mostra o que vai ser trocado
    Então a descrição da classe e do gênero sai como "Todos"

  Cenário: Já existe uma atualização em andamento para a coordenadoria
    Dado que já existe uma requisição de atualização pendente para a minha coordenadoria
    Quando confirmo a alteração
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da resposta
    E nada é agendado

  Cenário: Tela não autorizada para o meu código de acesso
    Dado que o meu código de acesso não tem a tela E059T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E volto ao menu principal

  Cenário: Operação não autorizada para o meu código de acesso
    Dado que o meu código de acesso não tem a alteração liberada nessa tela
    Quando tento alterar o fornecedor e o contrato dos pedidos
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é lido nem agendado

  Cenário: Com a tela de origem preenchida, a operação é abandonada
    Dado que a tela chega com a tela de origem preenchida
    Quando peço a alteração
    Então a operação é abandonada
    E o sistema me devolve à tela de origem
    E nada é agendado

  Cenário: Falha de banco interrompe a operação
    Dado que o banco falha durante a leitura ou a gravação
    Quando confirmo a alteração
    Então a tela avisa da falha
    E a requisição não é agendada
```
