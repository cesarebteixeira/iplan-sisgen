# US — C330T — Manter o cadastro dos operadores

## Estória

Como **servidor de CRE com a tela dos operadores autorizada**, quero **manter o cadastro dos
operadores do órgão — incluir um operador novo com o seu endereço e o seu contato, corrigir os dados
de um que já existe e tirar do cadastro o que não se usa mais**, para que **a ficha de cada operador
fique certa e o resto do sistema mostre o nome, o endereço e o contato corretos quando referir um
operador pelo código**.

O cadastro dos operadores é o que dá nome e endereço a quem o órgão refere pelo código: são outras
telas e rotinas que procuram o operador e mostram a razão social dele. Um operador sem ficha, ou com o
endereço e o contato errados, sai errado em tudo o que o cita. E é a ficha que guarda o CNPJ, que não
pode ser o mesmo em dois operadores — é por ele que o sistema impede que a mesma empresa entre duas
vezes no cadastro.

## Contexto

Jornada S000M → C000M → C015M → C330T.
Ator: servidor de CRE — mantém o cadastro dos operadores que o resto do sistema refere pelo código.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio. Os menus do caminho não gravam nada: só encaminham.

A `C330T` é uma tela de transação, não um menu: ela mantém **um operador por vez**, e termina nela
mesma ou em outra tela. Ela encadeia com a **relação de operadores (`C330C`)** nos dois sentidos e
sem passar por menu: marcado um operador na relação, a relação entrega a sessão a esta tela com o
operador escolhido e a operação de consulta (RN-02); e esta tela devolve a sessão à relação quando o
campo de indicação é preenchido (RN-16). Da sessão ela usa o **tipo de órgão** e a **data do
sistema** para o que exibe, e, na transmissão, a **matrícula**, o **código de acesso**, o
**privilégio** e a **CRE** — essa carga é regra da entrada e está no anexo, em **Regras que se
revelaram da entrada**.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O cadastro dos operadores e quem escreve nele

O cadastro dos operadores é a lista das empresas que o órgão mantém, com uma ficha por operador. Cada
ficha tem o **código** — que a identifica e não se repete —, a **razão social**, o **CNPJ**, o
**endereço**, o **complemento**, o **número do imóvel**, o **código do bairro**, o **nome do bairro**,
o **CEP**, a **cidade**, o **estado**, o **contato**, o **telefone**, o **ramal**, a **inscrição
estadual** e um **CPF/CGC** que esta tela não usa. No dicionário da base são **dezesseis** campos, e o
**código é a chave**; o cadastro é dimensionado para **100 operadores**.

Esta tela é a única que escreve nesse cadastro: dos **506** programas do lote, **50** leem o cadastro
de operadores e **um só** — esta tela — grava nele. **48** desses programas movem a **razão social**
do operador: é por ela que o sistema nomeia o operador ao referenciá-lo pelo código.

[?] O cadastro guarda um **CPF/CGC** do operador que esta tela não mostra e nunca preenche: na
inclusão ele sai zerado e na alteração fica com o que já estava gravado. Como esse dado entra no
cadastro não está nesta jornada. Pergunta ao site.

### RN-02 — A tela abre para incluir pelo menu e em consulta quando vem da relação de operadores

Chegando **pela opção do menu**, a tela abre na **inclusão**: o formulário vem em branco e a operação
é a de incluir.

Chegando da **relação de operadores (`C330C`)** com um operador marcado, a tela abre na **consulta**
sobre ele: os campos vêm preenchidos com a ficha guardada daquele operador.

Quem decide é a **tela de origem**, deixada na área de trabalho da sessão pelo programa que chamou:
esta tela compara essa origem com o código da relação e, sendo ela, troca a operação por consulta e
carrega a ficha do operador escolhido; a marca da origem é consumida em seguida, para não valer na
abertura seguinte. Sem essa marca, a operação fica a de inclusão.

### RN-03 — A operação da tela: incluir, alterar, excluir ou consultar

O campo da operação diz o que a tela vai fazer, e só valem quatro operações: **incluir**, **alterar**,
**excluir** e **consultar**. Qualquer outro valor — inclusive a operação em branco — é recusado
**antes de qualquer conferência da ficha**, com **\* Operacao nao disponivel \***, e nada é gravado.

[?] A tela compara o que foi informado com as siglas internas das quatro operações, e o catálogo de
mensagens que dá o texto dessas siglas — e o texto da própria recusa — não veio no lote. Se não
houver tradução do que o servidor digita para a sigla conferida, a recusa vale para toda operação,
inclusive as quatro. O mesmo desenho aparece nas outras telas de manutenção deste sistema. Pergunta
ao site.

### RN-04 — Os campos de número passam pela conferência numérica

**Sete campos** são conferidos como número antes de qualquer uso: o **código do operador**, o
**número do imóvel**, o **código do bairro**, o **CEP**, o **telefone**, o **ramal** e a **inscrição
estadual**. O que não for número é recusado no próprio campo, com o cursor de volta nele, e a operação
não segue; o campo em branco é tratado como zero. A conferência roda a cada mensagem, antes das
conferências da operação.

### RN-05 — A tela só abre e só opera com autorização

Na abertura, o sistema confere se a tela consta do **cadastro de telas** — não constando, o aviso é
**\* Tela nao disponivel \*** — e se o **código de acesso** de quem opera tem a tela — não tendo, a
recusa é **\* Acesso negado para esta matricula \***; confere ainda a **estação** contra a da sessão,
e estando a sessão aberta em outra estação o acesso é encerrado e a tela não abre.

A cada transmissão, o sistema confere a **rota** — tendo a tela sido retirada do cadastro de telas, o
aviso é **\* Tela nao cadastrada \*** — e, para a operação pedida, a **autorização daquela operação**
no mesmo código de acesso: incluir, alterar e excluir têm cada uma a sua marca, e não tendo a marca a
recusa é **\* Acesso negado para esta operacao \***. **A consulta não é conferida por operação**: ela
passa sem que a autorização de consulta seja olhada.

Nas recusas nada é gravado.

### RN-06 — A inclusão exige a razão social, o CNPJ e o endereço, e o CNPJ não pode repetir

Na **inclusão**, a tela exige, nesta ordem, sempre com o cursor de volta no campo recusado:

- a **razão social** — **\* Informe a razao social \***;
- o **CNPJ** — **\* Informe o CNPJ do Operador \***;
- que o **CNPJ** não pertença a nenhum operador já cadastrado — **\* <- CNPJ ja cadastrado neste
  codigo \***, depois de percorrer o cadastro inteiro comparando o CNPJ;
- o **endereço** — **\* Informe o endereco \***.

A **alteração** exige os mesmos quatro (RN-11). O complemento, o número do imóvel, o contato, o
telefone, o ramal e a inscrição estadual **não** são exigidos.

### RN-07 — O código do operador é do sistema, não de quem digita

Na inclusão o código do operador não é escolhido por quem opera: o que for digitado no campo é
substituído. A conferência calcula o **código seguinte ao maior já usado** no cadastro de operadores
e o coloca no campo; a **gravação**, porém, recalcula: procura o **CNPJ informado no cadastro de
fornecedores** e adota o **código que o fornecedor já tem lá**; não achando aquele CNPJ no cadastro de
fornecedores, começa em **1** e toma o **primeiro código ainda livre** do cadastro de operadores. A
ficha é gravada com o código que a gravação calculou.

[?] Os dois cálculos são diferentes e um só vale: quando o CNPJ do operador tem, no cadastro de
fornecedores, um código que não é o seguinte ao maior em uso, a tela mostra um código na conferência
e grava outro. Pergunta ao site qual dos dois é a regra.

[?] Chegando ao fim da faixa de códigos de quatro posições, a transação simplesmente termina — sem
aviso e sem gravar nada. Não há, no fonte, mensagem de cadastro esgotado. Pergunta ao site.

### RN-08 — No Rio de Janeiro o bairro vem do cadastro de bairros; nas outras cidades, é digitado

Com a **cidade do Rio de Janeiro**, o **código do bairro** é obrigatório — **\* Informe o codigo do
Bairro \*** — e tem de existir no **cadastro de bairros**: não existindo, a recusa é **\* Bairro nao
cadastrado \***. Achando, o **nome do bairro** que a ficha recebe é o que está no cadastro de
bairros, sobrepondo o que estiver digitado.

Com **qualquer outra cidade**, o **código do bairro é zerado** e o que se exige é o **nome do
bairro** — **\* Informe o Bairro \***; nesse caso o bairro não é conferido contra o cadastro de
bairros.

A comparação da cidade é pelo texto exato **RIO DE JANEIRO**.

### RN-09 — O CEP, a cidade e o estado são obrigatórios, e o estado tem de estar na lista

Depois do endereço e do bairro, a tela exige o **CEP** (**\* Informe o CEP \***), a **cidade**
(**\* Informe a Cidade \***) e o **estado** (**\* Inforne o Estado \*** na inclusão e **\* Informe o
Estado \*** na alteração — a diferença de grafia está na própria tela), sempre com o cursor de volta
no campo recusado.

O **estado** é conferido contra uma lista de siglas: fora dela, a recusa é **\* Estado invalido \***.
A lista tem **24 unidades da federação** escritas em **25 comparações** — **PA** aparece duas vezes —
e **não traz AP, DF nem PB**.

[?] Três unidades ficam de fora e uma se repete na lista: pelo fonte não é possível saber se a relação
é intencional ou se ficou incompleta. Pergunta ao site.

### RN-10 — Alterar, excluir e consultar exigem operador cadastrado

Informada a **alteração**, a **exclusão** ou a **consulta**, a tela procura o **código do operador**
no cadastro; não achando, recusa com **\* Operador nao cadastrado \***, com o cursor de volta no
campo, e nada é gravado.

A **inclusão** não faz essa conferência — o código ainda não existe; ela confere o CNPJ (RN-06).

### RN-11 — A alteração regrava a ficha do operador

Na alteração, existindo o operador (RN-10), a tela exige a **razão social**, o **CNPJ**, o
**endereço**, o **bairro**, o **CEP**, a **cidade** e o **estado**, com as mesmas mensagens da
inclusão. O CNPJ pode ser o do próprio operador; pertencendo a **outro** operador cadastrado, a
alteração é recusada com **\* <- CNPJ ja cadastrado neste codigo \***.

Passando as conferências, a tela reserva o registro e **regrava a ficha** com os dados informados.

### RN-12 — A exclusão apaga o registro do cadastro

Na exclusão, existindo o operador (RN-10), a tela **apaga o registro** do cadastro de operadores —
não é uma marca de excluído: o registro sai do conjunto, e a relação de operadores deixa de mostrá-lo.
O que havia na ficha vai para a auditoria (RN-13).

A exclusão não confere razão social, CNPJ, endereço, bairro, CEP, cidade nem estado.

### RN-13 — Toda manutenção deixa rastro na auditoria

A inclusão, a alteração e a exclusão gravam, no cadastro de auditoria (**A010T**), **uma linha por
operação**, com a operação, o cadastro tocado, a tela `C330T`, a **matrícula** de quem operou, a
estação, a **CRE**, o **tipo de órgão**, o número do processo, a **data e a hora** e o **conteúdo
anterior e o posterior** da ficha.

Na **inclusão** o conteúdo anterior vai em branco e o posterior leva a ficha nova; na **alteração**
vão os dois — o que estava gravado e o que passou a valer; na **exclusão** o anterior leva a ficha
apagada e o posterior vai em branco. A **consulta** não gera auditoria.

### RN-14 — A consulta mostra a ficha e não grava nada

Na consulta, a tela lê o operador pelo código e traz a ficha para o formulário; achando, **reabre em
cima daquele registro** e o único efeito é a exibição. Nenhum operador é incluído, alterado ou
apagado e nenhuma linha de auditoria é gerada. A consulta não confere razão social, CNPJ, endereço,
bairro, CEP, cidade nem estado — só exige que o operador exista (RN-10).

### RN-15 — Depois de incluir, a tela reabre em cima do operador gravado

Terminada a inclusão, a tela passa a operação para **consulta** e relê o registro que acabou de
gravar, **reabrindo em cima dele** com a ficha na tela.

[?] Pelo fonte não é possível determinar em que modo a tela reaberta fica: quem decide entre inclusão
e consulta é a marca da tela de origem, que já foi consumida na abertura e não é reposta na
reabertura. Se a reabertura depender dessa marca, a tela volta à inclusão sobre uma ficha já gravada.
Pergunta ao site.

[?] A reabertura só acontece quando o estado que a gravação deixa é diferente de um estado conhecido
do ambiente; nesse estado a tela nem troca a operação nem relê o registro. O que produz esse estado
não está no lote — quem o escreve é a rotina do ambiente. Pergunta ao site.

### RN-16 — As duas saídas da tela

A tela tem duas saídas, ambas sem passar por menu e sem gravar nada:

- a **relação de operadores (`C330C`)**: preenchido o **campo de indicação** com algo diferente de
  branco e de **N**, a tela não segue com a manutenção — entrega a sessão à relação;
- o **campo com o código de uma tela de destino**: preenchido, a transação é desviada para aquela
  tela **antes de qualquer conferência** — nem os dados da ficha, nem a operação, nem a permissão são
  conferidos nesse caso.

[?] O rótulo e o significado do campo de indicação e o do campo com o código de tela não estão no
acervo: a máscara da tela é carregada em tempo de execução e não veio no lote. O que o servidor vê
nesses dois campos, e quem os preenche, pergunta ao site.

### RN-17 — Os campos de contexto somem a cada mensagem

A **descrição do tipo de órgão da sessão** e a **data do sistema**, que a abertura mostra, são
apagadas a cada mensagem respondida e não são repostas: a resposta sai com os dois campos em branco.

[?] A limpeza está amarrada ao tipo de mensagem recebida; o acervo não explica o que separa esse tipo
das demais, nem se existe um caminho de entrada em que os campos não sejam limpos. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter o cadastro dos operadores

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C330T

  Cenário: RN-01 — a ficha mostra os dados que o cadastro guarda
    Dado que o operador informado está cadastrado
    Quando abro a sua ficha
    Então vejo o código, a razão social, o CNPJ, o endereço, o complemento, o número do imóvel, o código e o nome do bairro, o CEP, a cidade, o estado, o contato, o telefone, o ramal e a inscrição estadual
    E nada é gravado

  Cenário: RN-02 — abrir pelo menu prepara a inclusão
    Quando abro a tela C330T pela opção do menu
    Então a operação é a de inclusão
    E o formulário está em branco
    E nada é gravado

  Cenário: RN-02 — abrir pela relação de operadores mostra a ficha em consulta
    Dado que marquei um operador na relação de operadores
    Quando a tela C330T se abre
    Então a operação é a de consulta
    E vejo os dados daquele operador
    E nada é gravado

  Cenário: RN-03 — inclusão de um operador
    Dado que a operação é a de inclusão
    E informo a razão social, o CNPJ, o endereço, o bairro, o CEP, a cidade e o estado
    Quando transmito a inclusão
    Então o operador passa a constar do cadastro
    E a auditoria registra a inclusão

  Cenário: RN-03 — operação que a tela não aceita
    Quando informo uma operação diferente de incluir, alterar, excluir e consultar
    Então vejo a mensagem "* Operacao nao disponivel *"
    E nada é gravado

  Cenário: RN-03 — operação em branco
    Quando transmito sem informar a operação
    Então vejo a mensagem "* Operacao nao disponivel *"
    E nada é gravado

  Cenário: RN-04 — campo de número com texto
    Quando informo texto em um dos campos de número
    Então o campo é recusado antes de qualquer uso
    E o cursor volta ao campo
    E nada é gravado

  Cenário: RN-05 — sem autorização para a tela
    Dado que o meu código de acesso não tem a tela C330T
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: RN-05 — tela fora do cadastro de telas
    Dado que a tela C330T não consta do cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: RN-05 — tela retirada do cadastro de telas
    Dado que a tela C330T foi retirada do cadastro de telas
    Quando transmito uma operação
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é gravado

  Cenário: RN-05 — operação sem autorização
    Dado que o meu código de acesso tem a tela C330T sem aquela operação liberada
    Quando transmito a inclusão
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-06 — inclusão sem a razão social
    Dado que a operação é a de inclusão
    Quando transmito a inclusão sem a razão social
    Então vejo a mensagem "* Informe a razao social *"
    E o cursor volta ao campo da razão social
    E nada é gravado

  Cenário: RN-06 — inclusão sem o CNPJ
    Dado que a operação é a de inclusão e informei a razão social
    Quando transmito a inclusão sem o CNPJ
    Então vejo a mensagem "* Informe o CNPJ do Operador *"
    E o cursor volta ao campo do CNPJ
    E nada é gravado

  Cenário: RN-06 — inclusão sem o endereço
    Dado que a operação é a de inclusão e informei a razão social e o CNPJ
    Quando transmito a inclusão sem o endereço
    Então vejo a mensagem "* Informe o endereco *"
    E o cursor volta ao campo do endereço
    E nada é gravado

  Cenário: RN-06 — inclusão com o CNPJ de um operador já cadastrado
    Dado que o CNPJ informado já pertence a um operador cadastrado
    Quando transmito a inclusão
    Então vejo a mensagem "* <- CNPJ ja cadastrado neste codigo *"
    E o cursor volta ao campo do CNPJ
    E nada é gravado

  Cenário: RN-07 — o código do operador vem do sistema
    Dado que a operação é a de inclusão
    E informo um código qualquer no campo do código
    Quando transmito a inclusão
    Então o operador é gravado com o código que o sistema calculou, e não com o que eu informei
    E a auditoria registra a inclusão

  Cenário: RN-08 — inclusão no Rio de Janeiro sem o código do bairro
    Dado que a operação é a de inclusão e informo a cidade RIO DE JANEIRO
    Quando transmito a inclusão com o código do bairro em branco
    Então vejo a mensagem "* Informe o codigo do Bairro *"
    E o cursor volta ao campo do código do bairro
    E nada é gravado

  Cenário: RN-08 — inclusão no Rio de Janeiro com bairro não cadastrado
    Dado que a operação é a de inclusão e informo a cidade RIO DE JANEIRO
    Quando transmito a inclusão com o código de um bairro que não está no cadastro de bairros
    Então vejo a mensagem "* Bairro nao cadastrado *"
    E o cursor volta ao campo do código do bairro
    E nada é gravado

  Cenário: RN-08 — inclusão no Rio de Janeiro com bairro cadastrado
    Dado que a operação é a de inclusão e informo a cidade RIO DE JANEIRO
    E informo o código de um bairro cadastrado e um nome de bairro diferente do cadastrado
    Quando transmito a inclusão
    Então a ficha do operador fica com o nome do bairro que está no cadastro de bairros
    E o operador passa a constar do cadastro

  Cenário: RN-08 — inclusão em outra cidade sem o nome do bairro
    Dado que a operação é a de inclusão e informo uma cidade diferente de RIO DE JANEIRO
    Quando transmito a inclusão com o nome do bairro em branco
    Então vejo a mensagem "* Informe o Bairro *"
    E o código do bairro fica zerado
    E nada é gravado

  Cenário: RN-09 — inclusão sem o CEP
    Dado que a operação é a de inclusão e já informei razão social, CNPJ, endereço e bairro
    Quando transmito a inclusão sem o CEP
    Então vejo a mensagem "* Informe o CEP *"
    E o cursor volta ao campo do CEP
    E nada é gravado

  Cenário: RN-09 — inclusão sem a cidade
    Dado que a operação é a de inclusão e já informei razão social, CNPJ, endereço, bairro e CEP
    Quando transmito a inclusão sem a cidade
    Então vejo a mensagem "* Informe a Cidade *"
    E o cursor volta ao campo da cidade
    E nada é gravado

  Cenário: RN-09 — inclusão sem o estado
    Dado que a operação é a de inclusão e já informei razão social, CNPJ, endereço, bairro, CEP e cidade
    Quando transmito a inclusão sem o estado
    Então vejo a mensagem "* Inforne o Estado *"
    E o cursor volta ao campo do estado
    E nada é gravado

  Cenário: RN-09 — inclusão com uma sigla de estado fora da lista
    Dado que a operação é a de inclusão e informo todos os dados exigidos
    E informo no estado uma sigla que não está na lista da tela
    Quando transmito a inclusão
    Então vejo a mensagem "* Estado invalido *"
    E o cursor volta ao campo do estado
    E nada é gravado

  Cenário: RN-10 — alteração de operador não cadastrado
    Dado que informo a operação de alteração com um código que não existe no cadastro
    Quando transmito a alteração
    Então vejo a mensagem "* Operador nao cadastrado *"
    E o cursor volta ao campo do código
    E nada é gravado

  Cenário: RN-10 — exclusão de operador não cadastrado
    Dado que informo a operação de exclusão com um código que não existe no cadastro
    Quando transmito a exclusão
    Então vejo a mensagem "* Operador nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — consulta de operador não cadastrado
    Dado que informo a operação de consulta com um código que não existe no cadastro
    Quando transmito a consulta
    Então vejo a mensagem "* Operador nao cadastrado *"
    E nada é gravado

  Cenário: RN-11 — alteração de um operador cadastrado
    Dado que a operação é a de alteração e o operador está cadastrado
    E altero a razão social e o endereço mantendo os demais dados exigidos
    Quando transmito a alteração
    Então a ficha do operador passa a valer com os dados informados
    E a auditoria registra a alteração com o conteúdo anterior e o novo

  Cenário: RN-11 — alteração com o CNPJ de outro operador
    Dado que a operação é a de alteração e o operador está cadastrado
    E informo o CNPJ de um operador diferente
    Quando transmito a alteração
    Então vejo a mensagem "* <- CNPJ ja cadastrado neste codigo *"
    E nada é gravado

  Cenário: RN-12 — exclusão de um operador cadastrado
    Dado que a operação é a de exclusão e o operador está cadastrado
    Quando transmito a exclusão
    Então o operador sai do cadastro
    E a auditoria registra a exclusão com o conteúdo que existia

  Cenário: RN-13 — a auditoria guarda o antes e o depois
    Dado que alterei um operador cadastrado
    Quando a alteração é gravada
    Então a auditoria registra o conteúdo anterior e o novo, a matrícula, a CRE, o tipo de órgão, a data e a hora
    E a consulta não deixa linha de auditoria

  Cenário: RN-14 — a consulta não grava nada
    Dado que a operação é a de consulta e o operador está cadastrado
    Quando transmito a consulta
    Então vejo a ficha do operador
    E nenhum operador é incluído, alterado ou apagado
    E nenhuma linha de auditoria é gerada

  Cenário: RN-15 — depois de incluir, a tela reabre na ficha gravada
    Dado que incluí um operador
    Quando a inclusão é gravada
    Então a ficha que a tela mostra é a do operador que acabei de gravar
    E nada mais é gravado

  Cenário: RN-16 — a saída para a relação de operadores
    Dado que preencho o campo de indicação com algo diferente de branco e de N
    Quando transmito
    Então a sessão vai para a relação de operadores
    E nada é gravado

  Cenário: RN-16 — a saída pelo campo com o código de uma tela
    Dado que preencho o campo com o código de outra tela
    Quando transmito, mesmo com a ficha incompleta
    Então a sessão vai para aquela tela
    E nada é gravado

  Cenário: RN-17 — os campos de contexto voltam em branco
    Dado que a tela abriu mostrando a descrição do tipo de órgão da sessão e a data do sistema
    Quando respondo uma mensagem
    Então a resposta vem com esses dois campos em branco
```
