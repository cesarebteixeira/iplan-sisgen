# US — C648T — Reduzir a quantidade e o valor da permissão de contrato

## Estória

Como **servidor de CRE**, quero **reduzir a quantidade e o valor de uma permissão de
contrato da minha coordenadoria**, para que **o saldo autorizado volte a refletir o que de
fato será fornecido e os totais do contrato fiquem corretos**.

A permissão é o que autoriza um fornecedor, dentro de um contrato de uma coordenadoria, a
entregar uma quantidade de um item num período por um valor. Quando a demanda cai, esse
saldo precisa ser reduzido; sem isso o contrato continua autorizando uma compra que não
vai acontecer, e os totais adjudicado e homologado do contrato ficam acima do real. A
redução nunca passa do que ainda está livre — o que já foi pedido ou comprado não se
retira — e a tela não apaga permissão nenhuma: ela só abaixa o saldo, depois de a
permissão ter sido consultada e de o servidor ter acesso àquela coordenadoria.

## Contexto

Jornada S000M → C000M → C050M → C648T.
Ator: servidor de CRE — reduz o saldo de uma permissão de contrato da sua coordenadoria,
consultando-a antes na própria tela.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Duas coisas que a tela usa vêm de antes dela e **não são regra desta estória**: a
**coordenadoria da sessão** e o **órgão do servidor**, que a entrada deixa na sessão, e a
**tela de origem**, pela qual a conferência de rota é feita. Elas estão no anexo de
evidências, em **Regras que se revelaram da entrada**. A jornada termina nesta tela: ela
não encaminha para nenhuma outra.

## Regras de negócio

### RN-01 — A tela reduz o saldo da permissão de contrato

A permissão de contrato é o registro que autoriza um fornecedor, dentro de um contrato de
uma coordenadoria, de um grupo de licitação e de um período, a fornecer um item — uma
classe, uma subclasse e um gênero de produto — por uma quantidade e um valor. O cadastro
dessas permissões tem **52 campos** e comporta até **1.000.000** de registros —
**capacidade** declarada (máximo esperado, parâmetro de dimensionamento), não volume.

O que o servidor informa nesta tela é **a quantidade a reduzir**; o valor a reduzir a tela
calcula. Os demais dados da permissão — fornecedor, período, saldos, totais — a tela
apresenta e não deixa alterar. A tela **grava**: a redução confirmada trava e regrava a
permissão e deixa o rastro na auditoria. **Nada é apagado** — a rotina de exclusão existe
declarada no programa e não é executada por caminho nenhum desta tela.

[?] A chave que a tela usa para gravar admite mais de um registro para a mesma combinação
de contrato, período e item, mas a tela trata a permissão como única: ao gravar, ela grava
no primeiro registro que encontra. Se duas permissões iguais podem existir, a segunda
ficaria com o saldo antigo — pergunta ao site.

### RN-02 — A permissão é identificada pela coordenadoria, pelo contrato, pelo período e pelo item

A tela localiza a permissão pela **coordenadoria**, pelo **tipo de contrato**, pelo
**código do fornecedor**, pelo **grupo de licitação** e pelo **período** — dia, mês e ano
de início e dia, mês e ano limite —, dentro da secretaria e do órgão da sessão. A
**classe do item não se digita**: o sistema a deduz da subclasse e do gênero vigentes no
ano limite do período. O nome do fornecedor a tela busca no cadastro de fornecedores e
apresenta; o preço do item vem do contrato.

[?] Quando a subclasse e o gênero não existem para o período informado, a tela segue sem a
classe deduzida e procura a permissão com o que tiver ficado na área de leitura do
programa; o acervo não permite dizer se esse resto é o que o servidor informou ou o que
sobrou da leitura anterior. A recusa, nesse caso, é sempre a mesma: permissão não
cadastrada. Pergunta ao site.

### RN-03 — A tela apresenta os dados da permissão e dos cadastros vizinhos

Apresentada a permissão, a tela mostra, além dos dados que identificam o registro, os
**saldos e valores** do item e do contrato — quantidade inicial, acrescida por aditivo e
por prorrogação, quantidade pedida, quantidade e valor máximos, valor inicial, do
aditivo, da prorrogação e do apostilamento, valores comprados e o preço do item — e o
**nome e a descrição** do fornecedor, da classe, da subclasse e do gênero.

**6 dados** ela apresenta mas não deixa digitar: a **situação** do registro, o **órgão**, a
**data do sistema**, a **situação atualizada**, a **descrição do item** e o **sinal** do
desconto ou acréscimo. A tela escreve a situação como não confirmada quando se apresenta
e a limpa quando termina a operação. Os **29 dados** que restam da permissão a tela aceita
do servidor, submetendo cada um à edição numérica — e é sobre eles que ela diz, quando
algum não passa, em qual campo o cursor deve voltar (são **10** posições de cursor).

### RN-04 — O modo da tela é alteração ou consulta, e a consulta não grava

A tela tem um modo de manutenção que só admite dois valores: **alteração** e **consulta**
— os que a recusa nomeia como **ALT** e **CON**. Qualquer outro valor é recusado com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no campo do modo. Quando a
tela abre sem modo informado, ela assume sozinha o modo **consulta**.

No modo consulta **nada é gravado**: a passagem de gravação é abandonada antes de qualquer
teste de valor — a tela apenas lê, calcula e apresenta a permissão.

[?] A recusa nomeia as opções como ALT e CON, mas o que a tela compara para decidir o modo
são os códigos internos de alteração e de consulta. O acervo desta jornada não mostra quem
traduz o texto que aparece na recusa para esse código, nem onde ele é informado. Se o
texto da recusa é o que o servidor digita, pergunta ao site.

### RN-05 — A tela só trabalha a coordenadoria a que o servidor tem acesso

Se a sessão do servidor tem uma coordenadoria e ele informa outra, a tela recusa com
**\* Usuario sem acesso a este grupo \*** e devolve o cursor ao campo da coordenadoria. A
coordenadoria informada também precisa existir para o órgão da sessão: não existindo, a
recusa é **\* Grupo nao pertence a esta secretaria \***, com o cursor no mesmo campo.

[?] Quando a sessão não tem coordenadoria, a tela não confere a coordenadoria informada
contra nenhuma outra: segue direto para a leitura. Se isso é intencional — o servidor sem
coordenadoria podendo alcançar qualquer grupo —, pergunta ao site.

### RN-06 — A permissão não cadastrada é recusada

Não havendo permissão para a combinação informada, a tela não apresenta valor algum e
recusa com **\* Permissao nao cadastrada \***, com o cursor na coordenadoria. A permissão
marcada como excluída no cadastro não é encontrada por nenhuma das leituras da tela.

### RN-07 — A alteração exige que a permissão tenha sido consultada

A alteração só é aceita para a permissão que a tela acabou de apresentar. Informados
coordenadoria, subclasse ou gênero diferentes dos da consulta anterior, a recusa é
**\* Consulte antes de atualizar \***, com o cursor na subclasse. Confirmada a alteração
com uma quantidade diferente da que a tela calculou, a recusa é a mesma mensagem, agora
com o cursor na quantidade.

[?] A quantidade calculada e a quantidade informada são a mesma referência de memória: a
tela calcula sobre o que o próprio servidor digitou. Se a confirmação for enviada com
outra quantidade, a comparação não reconhece o que foi calculado e recusa — e a alteração
fica inalcançável por esse caminho. Se existe outra passagem que preserve a quantidade
calculada entre o cálculo e a confirmação, o site confirma.

### RN-08 — A redução exige a quantidade a reduzir

Sem a quantidade a reduzir informada, a tela recusa com
**\* Informe a quantidade a reduzir \***, com o cursor no campo da quantidade, e não
grava.

### RN-09 — O valor a reduzir é a quantidade pelo preço, e nada passa do teto

O valor a reduzir é calculado pela tela: a quantidade informada multiplicada pelo preço do
item. A quantidade não pode passar do **teto de quantidade** da permissão; passando, a
recusa é **\* <- Maior quantidade a reduzir \***, com o teto apresentado ao lado. O valor
não pode passar do **teto de valor**; passando, a recusa é
**\* <- Maior valor a reduzir \***, também com o teto apresentado. As duas recusas apontam
o cursor para a quantidade.

### RN-10 — O teto é o saldo livre: o que foi pedido e comprado sai, o que foi acrescentado entra

O **teto de quantidade** é a quantidade inicial **mais** a acrescida por aditivo e a
prorrogada, **menos** a quantidade já pedida contra a permissão, descontada a menor
unidade do saldo. O **teto de valor** é o valor inicial **mais** o do aditivo, o da
prorrogação e o do apostilamento, **mais** os valores dos demais itens do mesmo contrato —
os que não são o próprio item nem os que diferem por subclasse e gênero —, **menos** o
valor comprado, também descontada a menor unidade. Em uma frase: **só se reduz o que ainda
está livre**.

[?] O teto de valor é limitado uma segunda vez, ao valor inicial com aditivo, prorrogação
e apostilamento, e essa segunda conta **não** desconta o comprado. Os dois limites
discordam entre si quando o comprado é maior que os valores dos demais itens. Qual dos
dois o site considera o teto, pergunta ao site.

### RN-11 — A redução abate primeiro o aditivo, depois a prorrogação e, por último, o que é inicial

A quantidade a reduzir é abatida nesta ordem: primeiro a quantidade acrescida por aditivo;
o que não bastar passa para a prorrogada; e o resto, para a quantidade inicial. O valor
segue a mesma ideia, com o apostilamento antes do valor inicial: primeiro o valor do
aditivo, depois o da prorrogação, depois o do apostilamento e, por último, o valor inicial
do item. Cada parcela só é abatida até zerar; o que sobra desce para a seguinte.

### RN-12 — A tela aplica a redução, trava e regrava só o que mudou

Aplicada a redução, a tela trava a permissão e regrava cada saldo que mudou: a quantidade
inicial, a do aditivo, a da prorrogação, os respectivos valores e o valor do
apostilamento. Só o que mudou é regravado. **Nada é apagado** nesta tela — a exclusão
existe declarada no programa e não é executada por caminho nenhum.

### RN-13 — Depois da redução os totais do contrato são refeitos em todos os itens

Terminada a redução, a tela percorre **todos os itens do mesmo contrato** — mesma
coordenadoria, mesmo órgão, mesmo período, mesmo tipo de contrato e mesmo grupo de
licitação — e regrava em cada um os totais do contrato: o **valor adjudicado** passa a ser
a soma dos valores iniciais dos itens, o **valor homologado** recebe o adjudicado, e o
**valor do aditivo**, o **da prorrogação** e o **total de apostilamento** passam a ser as
somas das respectivas parcelas.

[?] O valor homologado recebe a soma dos valores iniciais, que é a soma **anterior** à
redução registrada na área de trabalho. Depois de uma redução, o homologado pode ficar
acima dos valores iniciais que a mesma passagem regravou nos itens. Se é o esperado, o
site confirma.

### RN-14 — Toda redução deixa rastro na auditoria

Cada redução gravada deixa um registro de auditoria: o objeto auditado (a permissão do
contrato), a operação de alteração, a imagem do registro anterior e a do posterior, e o
contexto da sessão — matrícula, secretaria, coordenadoria, órgão, terminal, data e hora e
número do processo. O cadastro de auditoria tem **15 campos** e comporta **60.000.000** de
registros (capacidade).

[?] O rastro cobre só a permissão reduzida: o cadastro de auditoria não recebe o valor
anterior nem o posterior dos demais itens do contrato regravados junto. Se essa alteração
em cascata fica sem imagem, é pergunta ao site.

### RN-15 — Depois da gravação a tela volta à consulta

Terminada a gravação, a tela passa sozinha ao modo consulta, reapresenta a permissão já com
os saldos regravados e escreve no campo de situação **## ATUALIZADO \*\***.

### RN-16 — Nada é feito sem a autorização de perfil, de rota e de operação

Antes de apresentar, antes de gravar e antes de escrever a auditoria, a tela chama as
rotinas do sistema que conferem o **perfil** do servidor, a **rota** da transação e a
**permissão por operação**. Se qualquer uma delas não responder "OK", a tela volta sem
gravar e sem auditar. A conferência recebe o contexto da sessão — matrícula, código de
acesso, privilégio, órgão, coordenadoria — e, na conferência da rota, a **tela de origem**
que a chamou.

[?] A regra efetiva de permissão por perfil e por rota não está no acervo: as rotinas são
declaradas em comum, sem corpo no lote. A tela só confere o retorno.

[?] A tela de origem que a conferência de rota recebe é lida do registro da transação e não
é escrita em ponto nenhum desta tela: chega o que a tela que a chamou deixou. De que tela
de origem a C648T espera a rota, e o que acontece quando ela chega em branco, o site
confirma.

### RN-17 — A operação depende do modo e dos dados que o registro da transação traz

A tela decide o que fazer pelo modo de manutenção que chega no registro da transação: com
o código de alteração ela segue a passagem de alteração; com o código de consulta,
abandona a gravação. Os dados que identificam a permissão também chegam por esse registro
— é por ele que a tela recebe a coordenadoria quando aberta por outra tela.

[?] Se o registro da transação chega sem modo, a tela assume consulta, e não há, nesta
jornada, caminho que a faça gravar por outro modo que não o de alteração. Se isso deixa a
redução alcançável apenas quando outra tela informa o modo, ou se a estação de trabalho o
informa, pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Reduzir a quantidade e o valor da permissão de contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, o órgão e a coordenadoria
    E tenho acesso à tela C648T

  Cenário: A tela apresenta a permissão de contrato
    Dado que estou na tela C648T
    Quando informo a coordenadoria, o tipo de contrato, o código do fornecedor,
      o grupo de licitação, o período e o item
    Então vejo o nome do fornecedor e a descrição da classe, da subclasse e do gênero
    E vejo os saldos e valores do item e os totais do contrato
    E a classe do item me aparece deduzida da subclasse e do gênero

  Cenário: A consulta não grava nada
    Dado que estou na tela C648T no modo consulta
    Quando percorro a permissão e informo uma quantidade a reduzir
    Então a tela apenas calcula e apresenta os saldos
    E a permissão continua com a quantidade e o valor anteriores
    E nenhum registro de auditoria é criado

  Cenário: O modo da tela só admite ALT ou CON
    Dado que estou na tela C648T
    Quando informo um modo diferente de ALT e de CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: A tela recusa coordenadoria fora do meu acesso
    Dado que a minha sessão tem uma coordenadoria
    Quando informo outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: A tela recusa coordenadoria que não pertence à secretaria
    Dado que estou na tela C648T
    Quando informo uma coordenadoria que não existe para o órgão da minha sessão
    Então vejo a mensagem "* Grupo nao pertence a esta secretaria *"
    E o cursor fica no campo da coordenadoria
    E nada é gravado

  Cenário: A permissão não cadastrada é recusada
    Dado que estou na tela C648T
    Quando a combinação informada não tem permissão cadastrada
    Então vejo a mensagem "* Permissao nao cadastrada *"
    E o cursor fica no campo da coordenadoria
    E nenhum valor é apresentado

  Cenário: A alteração sem consulta prévia é recusada
    Dado que estou na tela C648T e informei coordenadoria, subclasse ou gênero
      diferentes dos da consulta anterior
    Quando informo o modo de alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor fica no campo da subclasse
    E nada é gravado

  Cenário: A confirmação com quantidade diferente da calculada é recusada
    Dado que a tela calculou uma redução e reapresentou os saldos
    Quando confirmo a alteração com uma quantidade diferente da calculada
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor fica no campo da quantidade
    E nada é gravado

  Cenário: A redução sem quantidade é recusada
    Dado que estou na tela C648T no modo de alteração e a permissão está cadastrada
    Quando deixo a quantidade a reduzir em branco
    Então vejo a mensagem "* Informe a quantidade a reduzir *"
    E o cursor fica no campo da quantidade
    E nada é gravado

  Cenário: A quantidade acima do teto é recusada
    Dado que estou na tela C648T no modo de alteração e a permissão está cadastrada
    Quando informo uma quantidade maior que o teto de quantidade
    Então vejo a mensagem "* <- Maior quantidade a reduzir *", com o teto apresentado
    E nada é gravado

  Cenário: O valor acima do teto é recusado
    Dado que estou na tela C648T no modo de alteração e a permissão está cadastrada
    Quando a quantidade informada produz um valor maior que o teto de valor
    Então vejo a mensagem "* <- Maior valor a reduzir *", com o teto apresentado
    E nada é gravado

  Cenário: O teto é o saldo livre da permissão
    Dado que a permissão tem quantidade já pedida e valor já comprado
    Quando a tela calcula os tetos de quantidade e de valor
    Então o que já foi pedido e comprado é descontado
    E o que foi acrescido por aditivo, prorrogação e apostilamento é somado
    E cada teto desconta a menor unidade do saldo

  Cenário: A redução abate o aditivo antes do saldo inicial
    Dado que a permissão tem quantidade e valor iniciais, de aditivo e de prorrogação
    Quando a tela aplica a quantidade a reduzir
    Então a quantidade sai primeiro do aditivo e depois da prorrogação
    E o valor sai primeiro do aditivo, depois da prorrogação, depois do apostilamento
      e por último do valor inicial
    E cada parcela só é abatida até zerar

  Cenário: A redução é gravada e só o que mudou é regravado
    Dado que a tela calculou a redução de uma permissão cadastrada
    Quando a redução é confirmada
    Então a permissão é travada e regravada com os saldos reduzidos
    E a permissão continua no cadastro, sem nenhum registro apagado

  Cenário: Depois da redução os totais do contrato são refeitos em todos os itens
    Dado que confirmei a redução de um item do contrato
    Quando a gravação termina
    Então todos os itens do mesmo contrato são percorridos
    E o valor adjudicado passa a ser a soma dos valores iniciais dos itens
    E o valor homologado recebe o adjudicado
    E o valor do aditivo, o da prorrogação e o total de apostilamento são regravados
      em cada item

  Cenário: A tela volta à consulta depois de gravar
    Dado que a redução foi gravada
    Quando a tela se reapresenta
    Então ela está em modo consulta
    E a situação mostra "## ATUALIZADO **"
    E os saldos apresentados são os regravados

  Cenário: Toda redução deixa rastro na auditoria
    Dado que confirmei uma redução na C648T
    Quando a gravação termina
    Então existe um registro de auditoria da permissão do contrato
    E com a operação de alteração, a imagem anterior e a posterior
    E com a matrícula, a secretaria, a coordenadoria, o órgão, o terminal,
      a data e a hora e o número do processo

  Cenário: Nada é gravado sem a autorização de perfil, de rota e de operação
    Dado que estou na tela C648T
    Quando a conferência de perfil, de rota ou de permissão por operação não retorna OK
    Então a tela volta sem gravar nada
    E nenhum registro de auditoria é criado

  Cenário: Modo de manutenção não informado
    Dado que a tela abre pelo caminho desta jornada
    Quando o registro da transação chega sem modo de manutenção
    Então a tela assume o modo consulta
    E nada é gravado
```
