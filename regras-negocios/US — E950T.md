# US — E950T — Transferir o cartão do aluno entre órgãos

## Estória

Como **servidor da CRE**, quero **transferir o cartão do aluno do órgão em que ele
está para outro órgão do mesmo contrato**, para que **o cartão acompanhe a mudança de
unidade do aluno e a contagem de cartões de cada órgão continue certa**.

O cartão de referência fica registrado dentro de um órgão e de um contrato: quando o
aluno muda de unidade, ele precisa ser reacomodado sob o órgão novo, e a contagem de
cartões do contrato — entregues, pendentes e cancelados — precisa sair de um órgão e
entrar no outro no mesmo movimento. Sem essa transferência, o cartão continua contado
na unidade errada: um órgão fica com cartões a mais e o outro com cartões a menos, e a
conferência de entrega do contrato deixa de bater com o que foi entregue aos alunos.

## Contexto

Jornada S000M → E000M → E900M → E950T.
Ator: servidor de CRE — reacomoda o cartão do aluno no órgão em que ele passou a
estudar e acerta a contagem do contrato nos dois órgãos.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A tela não é encadeada: o menu `E900M` a abre pela própria opção e não lhe passa
registro nem operação. O único contexto que a `E950T` herda é o da sessão — o órgão
filho, a coordenadoria e o tipo de órgão do vínculo do servidor —, e é ela mesma que
decide o modo em que abre: **alteração**. O comportamento da tela não muda conforme
quem a chamou. Ao concluir, ela também não encadeia em outra: reabre a si mesma com o
aviso de sucesso.

## Regras de negócio

### RN-01 — A tela transfere o cartão do aluno de um órgão para outro

Identificada pelos rótulos ORGAO FILHO SDI e COORD.REG.ESCOLA, a tela recebe o órgão de
origem, a coordenadoria, o contrato (ano e número), a matrícula do aluno e o órgão de
destino, e transfere o cartão do aluno de um órgão para o outro. O cartão é o registro
que liga um aluno a um contrato dentro de um órgão: ele guarda o próprio código, o
código do subcartão, a matrícula do aluno, o contrato, a situação de entrega e o
vínculo com a justificativa dessa situação. A transferência **não reemite o cartão** —
ele conserva o código e os demais dados; o que muda é o órgão a que pertence, e a
coordenadoria passa a ser a do órgão de destino. Para conferência, a tela mostra o nome
do órgão de origem, a data do sistema, o período de validade do contrato, a razão social
do fornecedor, o nome do órgão de destino e a mensagem do sistema.

### RN-02 — A tela abre em modo de alteração, com o órgão e a coordenadoria do vínculo

Na primeira apresentação a tela já vem em modo de **alteração**, e o órgão de origem e a
coordenadoria são preenchidos com os do vínculo do servidor. Quando o órgão informado não
é o que a tela guardou, o sistema lê o cadastro daquele órgão e traz dele o nome e **a
coordenadoria, que substitui a que estava no campo** — é a coordenadoria do cadastro do
órgão, e não a digitada, que segue para a operação. Se o vínculo não tiver órgão, o campo
abre em branco e o cursor é posicionado nele.

[?] O órgão filho e a coordenadoria do vínculo são procurados numa área da sessão que, em
todo o acervo, só aparece sendo zerada: nenhum programa grava ali o órgão filho. Ou o
valor vem do ambiente, fora dos fontes, ou a tela abre sempre sem órgão e sem
coordenadoria — e aí vale o caminho do cadastro do órgão, descrito acima. Não escolho um
dos dois lados; pergunta ao site.

[?] Se o campo COORD.REG.ESCOLA for digitável, o que o operador digita nele é descartado
sem aviso quando a tela lê o cadastro do órgão; se for só de exibição, o rótulo não indica
isso. O que define a editabilidade está na máscara da tela, que não está no lote. Pergunta
ao site.

### RN-03 — Fora do modo de alteração a operação é recusada

A tela só executa quando o modo informado é o de alteração. Em qualquer outro modo — a
consulta, por exemplo —, a operação é recusada com
**\* Operacao nao disponivel. Use ALT \***, o cursor volta para o campo do modo e nada é
gravado. No momento da gravação o modo é conferido de novo: não sendo o de alteração, o
caminho termina sem gravar.

[?] O próprio programa preenche o campo do modo com o código da alteração a cada exibição
da tela. Se o campo não for sobrescrevível pelo operador, a recusa por modo indisponível
nunca acontece. Pergunta ao site.

### RN-04 — A origem é o órgão do próprio servidor

O órgão de origem só pode ser o órgão do servidor: o sistema compara o órgão informado com
o do vínculo e, sendo outro — inclusive em branco —, recusa com
**\* Usuario sem acesso a outro orgao \***, com o cursor de volta ao campo. Quando o
vínculo não tem órgão, não há com o que comparar: aí a tela exige o preenchimento e recusa
o vazio com **\* Informe o Orgao \***.

### RN-05 — O órgão informado precisa existir e ser da coordenadoria do servidor

O órgão informado é procurado no cadastro de órgãos. Não existindo, a operação é recusada
com **\* Orgao nao cadastrado \*** e o cursor volta ao campo. E a coordenadoria do órgão
tem de ser a coordenadoria do vínculo: sendo outra, a recusa é
**\* Usuario sem acesso ao grupo deste Orgao \***, também com o cursor de volta ao órgão.

[?] A recusa por órgão não cadastrado depende de uma marca que esse caminho de leitura não
prepara — ao contrário das leituras do contrato, da matrícula e do órgão de destino, que a
preparam antes de ler. Com a marca deixada por uma leitura anterior, a recusa não dispara e
o sistema segue com o nome e a coordenadoria que estiverem na área do cadastro. Se o site
confirma que a marca é sempre reiniciada por fora, a recusa vale. Pergunta ao site.

### RN-06 — O contrato é obrigatório, precisa existir e estar aberto

O contrato é identificado pelo ano e pelo número informados, dentro do órgão. Sem o número
do contrato a operação para em **\* Informe o Contrato \***, com o cursor de volta ao
contrato; o ano em branco não gera aviso próprio. O contrato é procurado no cadastro de
contratos pelo tipo de órgão da sessão, pelo ano e pelo número: não existindo, a recusa é
**\* Contrato nao cadastrado \***. E ele precisa estar aberto: o contrato marcado como
fechado é recusado com **\* Contrato fechado \***, com o cursor de volta ao contrato.

### RN-07 — A matrícula é obrigatória e precisa ter cartão no contrato e no órgão

Sem a matrícula do aluno a operação para em **\* Informe a Matricula do Aluno \***. Com a
matrícula informada, o sistema percorre os cartões daquele aluno naquele contrato e órgão e
recusa com **\* Matricula nao cadastrada \*** quando não acha nenhum. Cartão cancelado ou
bloqueado **conta** para essa existência e também é transferido: a situação de entrega só
decide qual número de cartão a tela publica no campo — o do primeiro cartão que não esteja
cancelado nem bloqueado; não havendo nenhum assim, fica ali o último cartão encontrado.

[?] A tela move todos os cartões da matrícula naquele contrato e órgão, mas publica um
número só, sem dizer quantos serão movidos. Se o operador precisa saber o que exatamente vai
sair da unidade, esse campo não responde. Pergunta ao site.

### RN-08 — O novo órgão é obrigatório, diferente do atual e cadastrado

Sem o novo órgão a operação para em **\* Informe o novo Orgao \***. Sendo igual ao órgão de
origem, a recusa é **\* Informe outro Orgao para a Matricula \***. E o novo órgão é
procurado no cadastro de órgãos: não existindo, a recusa é **\* Orgao nao cadastrado \***,
com o cursor no campo do novo órgão. Do cadastro do destino saem o nome e a coordenadoria
que a tela mostra e que o cartão novo recebe. A coordenadoria do destino **não** é
comparada com a do servidor.

### RN-09 — A conferência não grava: a tela mostra os dados e pede confirmação

Informados os dados e enviada a tela, o sistema confere tudo e **não grava nada**: mostra o
fornecedor, a validade do contrato, o nome do órgão de destino e a coordenadoria dele, e
pergunta **"Confirma alteracao do Orgao <S/N> ?"**, com o cursor no campo da confirmação. Só
com a resposta **S** a transferência é executada, na mesma requisição. Qualquer outra
resposta deixa a tela como estava. E se algum dos dados que identificam a operação — órgão
de origem, ano ou número do contrato, matrícula ou novo órgão — mudar junto com a resposta,
a confirmação é descartada e o operador recomeça. Toda recusa desta tela devolve a transmissão
à primeira passagem: o dado recusado barra a gravação naquela transmissão e nada é gravado.

[?] A execução exige sete dados preenchidos, entre eles a coordenadoria do órgão de destino
e a do órgão de origem. Faltando algum, a tela volta sem gravar e **sem avisar nada**: se a
coordenadoria do órgão de destino vier zerada do cadastro, o operador confirma e não vê a
mudança nem uma explicação. Pergunta ao site.

### RN-10 — Confirmada, a transferência recria cada cartão no órgão de destino

Confirmada a operação, o sistema percorre os cartões da matrícula naquele contrato e órgão
de origem, um a um; para cada um, guarda em memória o código do cartão, o código do
subcartão, a situação de entrega e o vínculo com a justificativa, e apaga o cartão daquele
órgão. Terminada a varredura, recria os cartões sob o novo órgão, com os mesmos dados e com
a coordenadoria do destino. A transferência leva **todos** os cartões da matrícula naquele
contrato e órgão — inclusive os cancelados e os bloqueados.

[?] A transferência guarda os cartões a levar numa área de **50 posições**. Se a matrícula
tiver mais de 50 cartões no órgão de origem, o sistema exclui os excedentes da origem, registra
a exclusão na auditoria e **não os recria no destino**, e a contagem do destino não os soma
— sem aviso ao operador. O cadastro de cartões não limita quantos cartões uma matrícula pode
ter no mesmo contrato e órgão. Confirmar com o site qual é o máximo real e o que se deve
fazer com o excedente.

### RN-11 — A contagem de cartões do contrato é acertada nos dois órgãos

Na origem, para cada cartão transferido o sistema subtrai um do total do contrato e um do
contador da situação do cartão — pendentes, entregues ou cancelados, sendo que cancelado e
bloqueado caem no mesmo contador —, e **apaga a contagem** daquele contrato no órgão quando
o total chega a zero. No destino, soma um ao contador da situação e um ao total, e **cria a
contagem** daquele contrato no órgão quando ela não existe, com o cartão transferido.

[?] Quando não existe contagem do contrato no órgão de origem, os cartões são excluídos e
nenhuma contagem é subtraída; ao fim, o operador ainda vê **\* Orgao atualizado \***. A
consulta do contrato passa a mostrar número que não bate com os cartões. Pergunta ao site.

[?] A contagem criada no destino recebe só a quantidade da situação daquele cartão e o total;
o movimento para o registro novo só atribui o que não é zero. Não se conclui do programa se o
registro novo nasce zerado ou com sobras da leitura anterior. Pergunta ao site.

### RN-12 — Cada cartão movimentado fica registrado na auditoria

Cada cartão apagado do órgão de origem e cada cartão recriado no destino geram um registro na
trilha de auditoria: o cadastro auditado (o cartão), a tela de origem, a operação (exclusão de
um lado, inclusão do outro), o conteúdo anterior e o posterior do cartão, a matrícula do
servidor, o terminal, o dia, o mês, o ano e a hora da sessão, o número do processo — que aqui é
a matrícula do aluno —, o tipo de órgão e a coordenadoria. As atualizações de quantidade e o
apagamento da contagem da origem **não** geram registro próprio.

### RN-13 — Concluída a gravação, a tela reabre a si mesma com o aviso de sucesso

Terminada a transferência, a tela é reaberta com o aviso **\* Orgao atualizado \***, a
confirmação é limpa e a operação volta ao estado inicial, pronta para outra transferência. A
mesma reabertura da própria tela é usada para apresentar a pergunta de confirmação. A tela não
encadeia em outra e não entrega registro nenhum a uma tela seguinte.

### RN-14 — Os campos de código passam pela edição numérica

Os **nove** campos de código da tela — órgão de origem, coordenadoria, ano e número do
contrato, fornecedor, matrícula, cartão, novo órgão e grupo — são tratados como número: o
campo em branco vale zero, os zeros à esquerda são descartados e a formatação com sinal é
removida. O que não for número é recusado, com o cursor de volta ao campo, sem chegar aos
cadastros.

### RN-15 — A operação depende do perfil e da rota, não da tela de origem

A abertura da tela passa pela conferência de segurança, que lê o cadastro da própria tela. Cada
transmissão repassa o contexto da sessão — matrícula funcional, código de acesso, privilégio,
tipo de órgão e coordenadoria — e pede a autorização da operação: não liberada, a operação é
recusada — **\* Acesso negado para esta operacao \*** ou **\* Acesso negado para esta matricula
\*** — e o servidor é devolvido ao menu principal, sem gravar. A mesma passagem confere a rota e
o cadastro da tela: tela em manutenção ou não cadastrada é abandonada com
**\* Tela nao cadastrada \***, e a tela só responde quando o modo é o de alteração. Nada disso
depende de qual tela chamou a `E950T`: o fonte desta tela não compara a tela de origem com
código nenhum.

[?] A conferência de rota é uma rotina comum do acervo, fora dos fontes desta jornada: o que
ela decide a partir da tela informada como próxima não se conclui daqui. Pergunta ao site.

### RN-16 — Falha de banco interrompe a operação

Erro de banco durante a leitura ou a gravação interrompe a operação: a tela avisa da falha e a
gravação não é completada. A falta de registro é tratada como situação normal — órgão não
cadastrado, contrato não cadastrado, matrícula sem cartão —, e não como erro.

## Cenários BDD

```gherkin
Funcionalidade: Transferir o cartão do aluno entre órgãos

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E950T

  Cenário: A tela abre pronta para alterar, com o órgão e a coordenadoria do vínculo
    Dado que o meu vínculo tem órgão e coordenadoria
    Quando a tela E950T é aberta
    Então ela abre em modo de alteração
    E o órgão de origem e a coordenadoria já vêm preenchidos com os da minha sessão

  Cenário: Transferência de um cartão confirmada
    Dado que informo o contrato, a matrícula de um aluno com cartão no meu órgão e um novo órgão cadastrado e diferente
    Quando envio a tela
    Então vejo o fornecedor do contrato, a validade, o nome do órgão de destino e a coordenadoria dele
    E vejo a pergunta "Confirma alteracao do Orgao <S/N> ?"
    Quando respondo S
    Então o cartão passa a pertencer ao novo órgão
    E a contagem de cartões do contrato é acertada nos dois órgãos
    E vejo o aviso "* Orgao atualizado *"

  Cenário: A conferência não grava nada
    Dado que informo dados válidos
    Quando envio a tela e ela pede a confirmação
    Então nenhum cartão foi excluído ou gravado
    E nenhuma contagem de cartões foi alterada

  Cenário: Resposta diferente de S não transfere
    Dado que a tela me pediu a confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a tela volta ao estado anterior
    E nada é gravado

  Cenário: Alterar um dado junto com a confirmação cancela a operação
    Dado que a tela me pediu a confirmação
    Quando troco o novo órgão e respondo S
    Então a confirmação é descartada
    E a tela confere os dados de novo, sem gravar nada

  Cenário: A tela não está em modo de alteração
    Dado que o modo da tela não é o de alteração
    Quando envio a operação
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT *"
    E o cursor volta para o campo do modo
    E nada é gravado

  Cenário: Órgão de origem de outro servidor
    Dado que o meu vínculo tem órgão
    Quando troco o órgão de origem por outro órgão cadastrado
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E o cursor volta ao órgão de origem
    E nada é gravado

  Cenário: Órgão de origem não informado em vínculo sem órgão
    Dado que o meu vínculo não tem órgão
    Quando deixo o órgão de origem em branco e envio a operação
    Então vejo a mensagem "* Informe o Orgao *"
    E o cursor fica no órgão de origem

  Cenário: Órgão não cadastrado
    Dado que informo um órgão que não existe no cadastro
    Quando envio a operação
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão

  Cenário: Órgão de outra coordenadoria
    Dado que informo um órgão cadastrado de coordenadoria diferente da minha
    Quando envio a operação
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste Orgao *"
    E nada é gravado

  Cenário: A coordenadoria passa a ser a do cadastro do órgão
    Dado que informo um órgão de origem diferente do que a tela guardou
    Quando o sistema lê o cadastro daquele órgão
    Então a coordenadoria usada na operação é a que está no cadastro do órgão
    E a coordenadoria que eu digitei não é a que vale

  Cenário: Contrato não informado
    Dado que deixo o número do contrato em branco
    Quando envio a operação
    Então vejo a mensagem "* Informe o Contrato *"
    E o cursor fica no contrato
    E nada é gravado

  Cenário: Contrato não cadastrado
    Dado que informo ano e número de contrato que não existem para o meu tipo de órgão
    Quando envio a operação
    Então vejo a mensagem "* Contrato nao cadastrado *"
    E nada é gravado

  Cenário: Contrato fechado
    Dado que o contrato informado está marcado como fechado
    Quando envio a operação
    Então vejo a mensagem "* Contrato fechado *"
    E nada é gravado

  Cenário: Matrícula do aluno não informada
    Dado que deixo a matrícula do aluno em branco
    Quando envio a operação
    Então vejo a mensagem "* Informe a Matricula do Aluno *"
    E o cursor fica na matrícula
    E nada é gravado

  Cenário: Matrícula sem cartão no contrato e no órgão
    Dado que a matrícula informada não tem cartão naquele contrato e órgão
    Quando envio a operação
    Então vejo a mensagem "* Matricula nao cadastrada *"
    E o cursor volta à matrícula
    E nada é transferido

  Cenário: Cartões cancelados e bloqueados também são transferidos
    Dado que a matrícula só tem cartões cancelados e bloqueados naquele contrato e órgão
    Quando confirmo a transferência
    Então os cartões passam para o novo órgão com a situação em que estavam

  Cenário: Novo órgão não informado
    Dado que deixo o novo órgão em branco
    Quando envio a operação
    Então vejo a mensagem "* Informe o novo Orgao *"
    E o cursor fica no novo órgão
    E nada é gravado

  Cenário: Novo órgão igual ao de origem
    Dado que informo como novo órgão o mesmo órgão de origem
    Quando envio a operação
    Então vejo a mensagem "* Informe outro Orgao para a Matricula *"
    E nada é gravado

  Cenário: Novo órgão não cadastrado
    Dado que informo como novo órgão um órgão que não existe no cadastro
    Quando envio a operação
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor fica no novo órgão
    E nada é gravado

  Cenário: A transferência leva todos os cartões da matrícula
    Dado um aluno com mais de um cartão no contrato dentro do órgão de origem
    Quando confirmo a transferência
    Então todos os cartões daquele aluno no contrato são excluídos do órgão de origem
    E todos são recriados sob o novo órgão, com o mesmo código e a mesma situação de entrega
    E a coordenadoria dos cartões passa a ser a do novo órgão

  Cenário: O último cartão sai e a contagem da origem é apagada
    Dado que o contrato tem um único cartão naquele órgão de origem
    Quando confirmo a transferência
    Então o total do contrato naquele órgão chega a zero
    E a contagem daquele contrato no órgão de origem deixa de existir

  Cenário: A contagem do destino é criada quando não existe
    Dado que o contrato não tem contagem no órgão de destino
    Quando confirmo a transferência
    Então a contagem do contrato naquele órgão é criada com o cartão transferido

  Cenário: A movimentação fica registrada na auditoria
    Quando confirmo a transferência
    Então a exclusão do cartão na origem fica registrada, com o conteúdo anterior
    E a inclusão do cartão no destino fica registrada, com o conteúdo posterior
    E o ajuste das contagens não gera registro próprio

  Cenário: Campos de código em branco ou não numéricos
    Dado que um dos campos de código está em branco ou contém algo que não é número
    Quando envio a operação
    Então o campo em branco é tratado como zero
    E o que não for número é recusado, com o cursor de volta ao campo, sem chegar aos cadastros

  Cenário: Operação não autorizada pelo perfil
    Dado que a minha sessão não tem a operação liberada para esta tela
    Quando envio a operação
    Então a operação é recusada
    E volto ao menu principal sem nada gravado

  Cenário: Tela fora de operação
    Dado que a tela não está cadastrada ou está em manutenção
    Quando envio a operação
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é gravado

  Cenário: Falha de banco interrompe a operação
    Dado que o banco falha durante a leitura ou a gravação
    Quando envio a operação
    Então a tela avisa da falha
    E a gravação não é completada

  Cenário: Ao concluir, a tela reabre a si mesma
    Quando a transferência termina
    Então a tela é reaberta com o aviso "* Orgao atualizado *"
    E nenhum registro é passado a outra tela
```
