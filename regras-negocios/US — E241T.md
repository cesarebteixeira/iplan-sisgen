# US — E241T — Manter gêneros do período de contrato

## Estória

Como **servidor da CRE que responde pelos contratos de fornecimento da alimentação
escolar da sua coordenadoria**, quero **manter os gêneros de alimentos do cadastro de um
período de contrato — ver o que já está lá, incluir um gênero novo e tirar o que não vale
mais —**, para que **o período só entregue os gêneros autorizados para aquele fornecedor e
o registro do período exista enquanto houver gênero nele**.

O período de contrato não tem número: ele é identificado pelo grupo, pela data de início,
pelo tipo de contrato e pelo fornecedor — e se repete em vários cadastros, cada um com a
sua identificação. É esta tela que diz quais gêneros cada cadastro entrega e que confere se
o gênero é permitido àquele fornecedor pelo contrato. Sem ela o registro do período não
nasceria — é o primeiro gênero incluído que o cria —, e um gênero incluído sem aquela
conferência sairia para um fornecedor que não tem permissão para fornecê-lo.

As duas telas que antecedem esta na jornada não são menus: a lista de períodos (`E240C`) e
a manutenção do período (`E240T`) encadeiam nela sem passar por menu, e é o que elas deixam
na sessão que decide em que modo a tela abre.

## Contexto

Jornada S000M → E000M → E240M → E240C → E241T.

Ator: servidor de CRE — chega pela lista dos períodos do seu grupo e mantém, no cadastro do
período escolhido, os gêneros de alimentos que aquele contrato entrega.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O que esta tela usa da sessão é a **secretaria (o tipo de órgão)**, a **coordenadoria
regional escolar do servidor** (o grupo), a **matrícula**, o **código de acesso**, o
**privilégio** e a **data do sistema**; a carga disso é regra da entrada e está no anexo de
evidências, em **Regras que se revelaram da entrada**. O **órgão filho** do servidor, que a
entrada também carrega, não limita esta tela: o alcance aqui é o cadastro do período do
grupo.

Esta tela **não é alcançada só pelo menu**: a lista de períodos (`E240C`), a manutenção do
período (`E240T`) e a tela dos pedidos (`E242T`) encadeiam nela sem passar por menu. Nesta
jornada quem a antecede é a `E240C`, que entrega o **período escolhido e a operação de
consulta** — a tela abre consultando (RN-02). Na volta, é esta tela que **entrega o cadastro
à tela dos pedidos** (`E242T`), com o gênero e as datas de entrega (RN-13).

## Regras de negócio

### RN-01 — A tela inclui, altera e consulta; qualquer outra operação é recusada

Esta é a tela de manutenção dos gêneros do cadastro de um período de contrato. Ela aceita
**incluir**, **alterar** e **consultar**, e recusa qualquer outra operação com
**\* Opcao nao disponivel. Use INC, ALT ou CON \***, com o cursor de volta ao campo da
operação, e **nada é procurado** nesse caminho: a recusa vem antes de o registro do período
ser lido.

Os três valores aceitos não são palavras escritas no programa: eles vêm da **tabela de
mensagens do ambiente**, a mesma que dá o texto da recusa — é por isso que a mensagem manda
usar "INC", "ALT" e "CON" enquanto a tela compara os códigos internos que essa tabela
carrega.

A operação que aparece quando a tela abre não é escolhida por ela: é a que a tela anterior
deixou (RN-02).

[?] A recusa só é alcançável se a máscara oferecer ao operador um campo de operação. Como a
abertura repõe a operação que veio de quem chamou, essa recusa só pode aparecer numa
mensagem seguinte do operador; se a máscara não tem esse campo, a recusa é trecho sem uso.
Pergunta ao site.

### RN-02 — A origem decide em que modo a tela abre

A tela só processa o cadastro quando ele vem de uma das três telas da família do contrato: a
**lista de períodos** (`E240C`), a **manutenção do período** (`E240T`) e a **tela dos
pedidos** (`E242T`). Vindo de qualquer outra origem, ela não processa nada e devolve o
servidor ao menu `E240M`.

O que cada origem entrega:

- a **lista de períodos** (`E240C`) e a **tela dos pedidos** (`E242T`) entregam o período
  escolhido e a **operação de consulta** — a tela abre consultando;
- a **manutenção do período** (`E240T`) entrega o período e a **operação de inclusão**, com
  a **identificação de cadastro seguinte** à última usada naquele período — a tela abre para
  incluir, e é essa abertura que cria o cadastro de um período novo.

A tela também reescreve a própria identidade quando entrega o cadastro à tela dos pedidos, e
é por essa marca que a tela seguinte aceita processá-lo.

### RN-03 — A lista: os gêneros do cadastro, em dez linhas

A tela lê os gêneros do cadastro — o do tipo de órgão da sessão, do grupo, do período e da
identificação de cadastro — e mostra, de cada um, **uma linha** com o **código da
subclasse**, o **código do gênero**, a **descrição**, a **situação da linha** e um
**indicador de pedidos**. A lista tem **dez linhas**; quando os gêneros do cadastro acabam,
as linhas que sobram ficam em branco. No alto a tela mostra a **descrição do tipo de órgão
da sessão** (a secretaria) e a **data do sistema**.

O indicador de pedidos sai marcado com um asterisco quando o gênero **não** tem pedido
registrado e em branco quando tem — é a única informação da lista que diz ao servidor se
aquele gênero já virou pedido.

A situação é o campo em que o servidor escreve o que quer fazer com a linha, na alteração
(RN-10); na consulta ela não decide nada.

[?] A descrição do tipo de órgão e a data do sistema são copiadas da sessão, e nenhum
programa deste caminho as preenche — a área comum só as apaga na inicialização. Se o
ambiente não as fornecer, o cabeçalho sai em branco. Pergunta ao site.

[?] Os rótulos das colunas da lista não estão no lote, e o material lido não diz o que o
asterisco significa para quem lê a tela: o programa só o escreve. Pergunta ao site.

### RN-04 — A identificação do cadastro manda: só o cadastro mostrado se altera

Um mesmo período pode ter mais de um cadastro — cada inclusão confirmada gera uma
identificação nova para o mesmo período —, e é a **identificação de cadastro** que diz qual
deles a tela está tratando. Numa **inclusão** ou **alteração**, se a identificação informada
for diferente da que a tela recebeu, a operação para com
**\* Consulte antes de atualizar nova requisicao \***, com o cursor de volta ao campo da
operação, e nada é gravado: para mexer num cadastro, o servidor tem de consultá-lo primeiro.

Na **consulta** é o contrário: a identificação informada é a que a tela procura, e é ela que
passa a ser o cadastro tratado.

### RN-05 — A tela prepara a identificação do cadastro novo

Quando a tela recebe a marca de **cadastro novo**, ela não mexe nos gêneros: toma a
**identificação seguinte** à do cadastro que está tratando, verifica se ela já existe e passa
a mostrar o período **em consulta**, com os limites e a identificação do período — os do
cadastro seguinte, se ele já existir; não existindo, os do primeiro cadastro daquele
período. Nada é gravado nesse caminho.

[?] A marca que dispara esse caminho é um campo de tela que **nenhum programa do acervo
lido escreve** — os programas só o apagam — e a máscara da tela não está no lote. Se a
máscara não oferecer esse campo, o caminho é trecho sem uso. Pergunta ao site.

### RN-06 — A consulta exige um cadastro que exista

Na consulta, a tela procura o registro do período com a identificação informada. Não
achando, avisa **\* Requisicao nao cadastrada \***, com o cursor de volta ao campo da
identificação do cadastro, e não segue: os gêneros não são procurados nesse caminho.
Achando, a identificação informada passa a ser a do cadastro tratado, e é ele que a tela
mostra.

### RN-07 — Cadastro com os pedidos já gerados só se consulta

Quando o registro do período está marcado como **já requisitado** — os pedidos daquele
cadastro já foram gerados —, a tela recusa **incluir** ou **alterar** com
**\* Pedidos ja gerados. Use CON \***, com o cursor de volta ao campo da operação, e nada é
gravado. A situação do cadastro aparece no alto da tela como uma faixa de traços, que vira
**"----- CADASTRO GERADO ----"** quando ele está nessa condição.

[?] Quem marca o registro do período como já requisitado está **fora do acervo lido**:
nenhum dos programas do lote escreve essa marca — esta tela só a grava em branco quando cria
o registro. Se o processo que a marca deixou de existir, a recusa é trecho sem uso. Pergunta
ao site.

### RN-08 — Sem gênero cadastrado, a tela avisa

Não achando nenhum gênero para o cadastro, a tela avisa
**\* Nao existem generos cadastrados \*** e não lista nada. O aviso é montado na primeira
posição da lista: ele sai uma vez, e não se repete a cada linha vazia.

### RN-09 — A inclusão de um gênero exige a permissão do fornecedor

Um gênero só entra no cadastro se houver, para ele, uma **permissão de contrato** cadastrada
para o **fornecedor** do período e para o **tipo de contrato** dele, com validade que
**cubra todo o período**: o início do período não pode ser anterior ao início da permissão,
nem o limite do período posterior ao limite dela. Não havendo permissão que sirva, a inclusão
para com **\* Genero sem permissao para este fornecedor \***, com o cursor de volta ao campo
da subclasse, e nada é gravado.

A conferência só é feita quando há **subclasse informada** na linha: a linha sem subclasse
não inclui nada e não é conferida.

[?] A procura da permissão informa a **data de início do período** no lugar do limite da
permissão, e o efeito exato desse posicionamento não está no acervo nem no manual: se ele
exige a chave exata, uma permissão com outro limite não é achada; se posiciona na primeira
igual ou posterior, é dela que a conferência parte. O site precisa dizer qual é o esperado.

### RN-10 — A alteração age pela situação de cada linha

Na alteração, cada linha leva uma **situação** escrita pelo servidor: **I** inclui no
cadastro o gênero daquela linha, e **E** exclui do cadastro o gênero dela. Para incluir, o
gênero **não pode já estar** no cadastro: se estiver, a alteração para com
**\* Genero ja cadastrado \***, com o cursor de volta ao campo da situação daquela linha, e
nada é gravado. Para excluir, o gênero **tem de estar** no cadastro: se não estiver, a
alteração para com **\* Genero nao cadastrado \***, no mesmo campo. Situação em branco — ou
diferente de I e de E — não faz nada com aquela linha.

[?] O que a máscara mostra no campo da situação, e se ele é digitável, não está no lote: o
programa só conhece as letras I e E. Pergunta ao site.

### RN-11 — O registro do período nasce com o primeiro gênero e morre com o último

O gênero é gravado com a identificação do cadastro do período, e é a existência de pelo menos
um gênero que sustenta o **registro do período**: incluído o **primeiro** gênero de uma
identificação de cadastro que ainda não tem registro, a tela **cria o registro do período**;
excluído o **último** gênero daquele cadastro, a tela **apaga o registro do período** junto.
O registro criado assim nasce sem a marca de requisição (é ela que diz, depois, que os
pedidos já foram gerados) e com as datas de início e limite do período.

### RN-12 — Excluir um gênero apaga os pedidos dele

Excluindo um gênero do cadastro, a tela percorre e **apaga todos os pedidos daquele gênero**
antes de apagar o gênero. É o que impede o pedido de ficar pendurado num gênero que não
existe mais.

[?] A exclusão de um gênero **com pedidos** só é alcançável se o cadastro **não** estiver
marcado como já requisitado — e é a geração dos pedidos que deveria marcar o cadastro
(RN-07). Como nenhum programa do lote escreve essa marca, o material lido não permite
concluir se o ramo que apaga os pedidos é alcançável na prática, e as duas linhas ficam no
anexo. Ou a marca significa outro estado — e não o de ter pedidos —, ou o caminho ficou
inalcançável. Pergunta ao site.

### RN-13 — A tela entrega o cadastro à geração dos pedidos

Quando a tela recebe a **marca de geração dos pedidos**, ela não grava pedido nenhum:
calcula as **datas de entrega** do gênero no período e entrega o cadastro, o gênero e essas
datas à tela dos pedidos (`E242T`), que é quem os trata. As datas são até **cinco**: a
**data de início do período** e, dia a dia, os **dias úteis** seguintes — sábados, domingos
e os **feriados do órgão** não contam —, e a última delas é a **data limite do período**, que
entra mesmo caindo em dia não útil. Quando o início e o limite coincidem, só a primeira data
é preenchida.

Se o registro do período não existir para a identificação tratada, a tela não entrega nada:
apenas devolve o cadastro à sessão. Antes de entregar, ela escreve a própria identidade na
sessão, e é por essa marca que a tela dos pedidos aceita processar o cadastro.

[?] A marca que dispara a geração é um campo de tela que **nenhum programa do acervo lido
escreve** — os programas só o apagam — e a máscara não está no lote: se ela não oferecer o
campo, a saída para a tela dos pedidos nunca acontece. Pergunta ao site.

### RN-14 — A consulta não grava nada; a inclusão e a alteração gravam e deixam trilha

A **consulta** não grava nada: nenhum gênero, pedido ou registro de período é incluído,
alterado ou excluído nesse modo.

A **inclusão** grava o gênero e, com ele, pode criar o registro do período (RN-11). A
**alteração** com a situação E exclui o gênero, apaga os pedidos dele (RN-12) e pode apagar
o registro do período (RN-11). Cada uma dessas gravações deixa uma **linha na trilha de
auditoria**, com a tela, o cadastro afetado, a operação, o órgão, a matrícula, a estação, a
data e a hora, o número do processo do período e o conteúdo anterior e posterior do registro.

As declarações de gravação, de exclusão e de travamento existem para todos os cadastros que
a tela enxerga — é assim que o programa é montado —, mas a tela só executa as gravações
acima: nenhuma outra é acionada por este caminho.

[?] Nas exclusões a trilha é gravada **antes** da exclusão; se a exclusão falhar, fica na
trilha uma operação que não chegou a acontecer. Pergunta ao site.

### RN-15 — A digitação passa pela edição numérica antes de qualquer conferência

**Doze campos** da tela são tratados como número: o grupo, o tipo de contrato, o fornecedor,
as três partes do início do período, as três partes da data limite, a identificação do
cadastro, o código da subclasse e o código do gênero. O que estiver em branco vira zero, os
zeros à esquerda caem e o que não for número é recusado **antes** de qualquer conferência de
negócio e de qualquer leitura do cadastro. Na recusa, apenas **três** deles devolvem o
cursor: a identificação do cadastro, o código da subclasse e o código do gênero.

[?] O texto da recusa da edição numérica não está nos fontes desta jornada: quem edita é uma
rotina comum, importada, sem corpo no acervo. E como o cursor só volta a três dos doze
campos, o servidor pode ser recusado sem saber em qual campo errou. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manter os gêneros do cadastro de um período de contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E241T

  Cenário: RN-01 — incluir um gênero no cadastro do período
    Dado que abro a tela E241T para incluir e o período tem uma identificação de cadastro livre
    Quando informo a subclasse e o gênero de uma linha
    E confirmo
    Então o gênero passa a fazer parte do cadastro daquele período

  Cenário: RN-01 — operação diferente de incluir, alterar e consultar
    Dado que estou na tela E241T
    Quando informo uma operação diferente de incluir, alterar e consultar
    Então vejo a mensagem "* Opcao nao disponivel. Use INC, ALT ou CON *"
    E o cursor volta ao campo da operação
    E nenhum registro do período é procurado nesse caminho

  Cenário: RN-02 — abrir o cadastro pela lista de períodos
    Dado que escolhi um período na lista de períodos
    Quando a tela E241T recebe o período e a operação de consulta
    Então ela abre consultando o cadastro daquele período
    E não mexe em nenhum gênero

  Cenário: RN-02 — abrir o cadastro pela manutenção do período
    Dado que confirmei a inclusão de um período na manutenção do período
    Quando a tela E241T recebe o período e a operação de inclusão
    Então ela abre para incluir, com a identificação de cadastro seguinte à última usada
    E o cadastro daquele período passa a existir quando eu incluo o primeiro gênero

  Cenário: RN-02 — período vindo de outra origem
    Dado que o período chega à tela E241T sem vir da lista, da manutenção ou dos pedidos
    Quando a tela recebe o registro
    Então ela não processa o período
    E o servidor volta ao menu E240M

  Cenário: RN-03 — os dados de cada gênero na lista
    Dado que o cadastro do período tem gêneros
    Quando abro a tela E241T
    Então de cada gênero vejo o código da subclasse, o código do gênero, a descrição,
          a situação da linha e o indicador de pedidos
    E a lista mostra no máximo dez gêneros
    E as linhas que sobram ficam em branco

  Cenário: RN-03 — o cabeçalho da lista
    Dado que entrei no sistema
    Quando abro a tela E241T
    Então vejo a descrição do tipo de órgão da minha sessão
    E vejo a data do sistema

  Cenário: RN-03 — o indicador de pedidos
    Dado que um gênero do cadastro tem pedido registrado
    Quando vejo a linha desse gênero
    Então o indicador de pedidos dela sai em branco
    E nos gêneros sem pedido o indicador sai marcado

  Cenário: RN-04 — alterar um cadastro que não é o mostrado
    Dado que estou na tela E241T com um cadastro do período
    Quando informo outra identificação de cadastro e peço para incluir ou alterar
    Então vejo a mensagem "* Consulte antes de atualizar nova requisicao *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: RN-04 — consultar pela identificação informada
    Dado que o período tem mais de um cadastro
    Quando informo a identificação de outro cadastro do período e consulto
    Então a tela passa a tratar aquele cadastro
    E mostra os gêneros dele

  Cenário: RN-05 — a tela prepara a identificação do cadastro novo
    Dado que a tela recebe a marca de cadastro novo para o período
    Quando a marca é processada
    Então a tela mostra o período em consulta, com a identificação seguinte à do cadastro atual
    E mostra os limites do período
    E nada é gravado

  Cenário: RN-06 — consultar um cadastro do período que não existe
    Dado que o período não tem cadastro com a identificação que informei
    Quando consulto
    Então vejo a mensagem "* Requisicao nao cadastrada *"
    E o cursor volta ao campo da identificação do cadastro
    E os gêneros não são procurados nesse caminho

  Cenário: RN-07 — cadastro com os pedidos já gerados
    Dado que os pedidos do cadastro do período já foram gerados
    Quando peço para incluir ou alterar
    Então vejo a mensagem "* Pedidos ja gerados. Use CON *"
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: RN-07 — a faixa de situação do cadastro
    Dado que os pedidos do cadastro do período já foram gerados
    Quando abro a tela E241T
    Então vejo a faixa "----- CADASTRO GERADO ----" no alto da tela
    E nos demais cadastros a faixa sai com traços

  Cenário: RN-08 — cadastro do período sem gênero
    Dado que o cadastro do período não tem nenhum gênero
    Quando a lista é montada
    Então vejo a mensagem "* Nao existem generos cadastrados *"
    E nenhuma linha é preenchida

  Cenário: RN-09 — incluir um gênero permitido ao fornecedor
    Dado que existe uma permissão de contrato do gênero para o fornecedor do período
    E a validade da permissão cobre todo o período
    Quando informo a subclasse e o gênero da linha e confirmo
    Então o gênero é gravado no cadastro do período

  Cenário: RN-09 — incluir um gênero sem permissão para o fornecedor
    Dado que não existe permissão de contrato do gênero para o fornecedor do período
    Quando informo a subclasse e o gênero da linha e confirmo
    Então vejo a mensagem "* Genero sem permissao para este fornecedor *"
    E o cursor volta ao campo da subclasse
    E nada é gravado

  Cenário: RN-09 — a permissão cobre só parte do período
    Dado que a permissão do gênero começa depois do início do período
    Quando confirmo a inclusão do gênero
    Então vejo a mensagem "* Genero sem permissao para este fornecedor *"
    E nada é gravado

  Cenário: RN-10 — situação de inclusão num gênero que já está no cadastro
    Dado que o gênero da linha já faz parte do cadastro do período
    Quando escrevo I na situação daquela linha e confirmo
    Então vejo a mensagem "* Genero ja cadastrado *"
    E o cursor volta ao campo da situação daquela linha
    E nada é gravado

  Cenário: RN-10 — situação de exclusão num gênero que não está no cadastro
    Dado que o gênero da linha não faz parte do cadastro do período
    Quando escrevo E na situação daquela linha e confirmo
    Então vejo a mensagem "* Genero nao cadastrado *"
    E o cursor volta ao campo da situação daquela linha
    E nada é gravado

  Cenário: RN-10 — excluir um gênero do cadastro
    Dado que o gênero da linha faz parte do cadastro do período
    Quando escrevo E na situação daquela linha e confirmo
    Então o gênero sai do cadastro do período

  Cenário: RN-10 — situação em branco
    Dado que a linha não tem situação escrita
    Quando confirmo a alteração
    Então aquela linha não é incluída nem excluída

  Cenário: RN-11 — o primeiro gênero cria o registro do período
    Dado que a identificação de cadastro do período ainda não tem registro
    Quando incluo o primeiro gênero daquele cadastro
    Então o registro do período é criado, sem a marca de requisição
    E fica com as datas de início e limite do período

  Cenário: RN-11 — o último gênero excluído apaga o registro do período
    Dado que o cadastro do período tem um único gênero
    Quando excluo esse gênero
    Então o gênero sai do cadastro
    E o registro do período é apagado junto

  Cenário: RN-12 — excluir um gênero apaga os pedidos dele
    Dado que o gênero do cadastro tem pedidos registrados
    Quando excluo esse gênero
    Então todos os pedidos daquele gênero são apagados
    E o gênero sai do cadastro

  Cenário: RN-13 — entregar o cadastro para a geração dos pedidos
    Dado que a tela recebe a marca de geração dos pedidos para o cadastro tratado
    E o registro do período existe
    Quando a marca é processada
    Então a tela calcula as datas de entrega do gênero
    E entrega o cadastro, o gênero e as datas à tela E242T
    E não grava pedido nenhum

  Cenário: RN-13 — as datas de entrega pulam os dias não úteis
    Dado que o período começa num sábado e tem uma data limite
    Quando a tela calcula as datas de entrega
    Então a primeira data é a data de início do período
    E as seguintes são dias úteis, sem sábados, domingos e feriados do órgão
    E a última data é a data limite do período

  Cenário: RN-13 — sem registro do período, nada é entregue
    Dado que a tela recebe a marca de geração dos pedidos
    E o registro do período não existe para a identificação tratada
    Quando a marca é processada
    Então a tela não entrega nada à tela seguinte
    E só devolve o cadastro à sessão

  Cenário: RN-14 — a consulta não grava nada
    Dado que abro a tela E241T e consulto o cadastro de um período
    Quando a lista é mostrada
    Então nenhum gênero, nenhum pedido e nenhum registro de período é incluído, alterado ou excluído
    E nenhuma linha de auditoria é gerada

  Cenário: RN-14 — a inclusão grava o gênero, o registro do período e a trilha
    Dado que incluo um gênero num cadastro do período
    Quando a gravação termina
    Então o gênero fica no cadastro
    E o registro do período é criado, se ainda não existia
    E uma linha de auditoria é gravada para o gênero

  Cenário: RN-15 — digitação que não é número
    Quando digito num campo numérico algo que não é número
    Então o sistema recusa a digitação antes de qualquer conferência de negócio
    E o cursor volta ao campo recusado quando é a identificação do cadastro,
          o código da subclasse ou o código do gênero
```
