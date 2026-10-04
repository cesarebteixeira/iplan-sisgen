# US — C681T — Calcular e aplicar o aditivo do contrato

## Estória

Como **servidor de CRE que responde pela execução do contrato**, quero **apurar o aditivo dos
itens do contrato e aplicá-lo às permissões**, para que **o acréscimo negociado passe a valer no
contrato, dentro do teto de 25% da quantidade inicial de cada item, depois de conferido em
relatório**.

A permissão é o registro que autoriza um fornecedor, dentro de um contrato de uma coordenação
regional escolar, de um grupamento e de um período, a entregar um item — uma classe, uma
subclasse e um gênero — por uma quantidade e um valor. O acréscimo é negociado item a item e
depois apurado para o conjunto do contrato: a tela reúne os itens com o percentual ou a
quantidade que se pretende acrescer, apura o valor correspondente, emite o relatório do cálculo
para a conferência da secretaria e, só depois de conferido, soma o acréscimo às permissões. Sem
esse passo, o aditivo ficaria só na combinação de quem o negociou: ninguém veria o conjunto do
contrato, o teto de 25% não seria conferido contra o que já foi aditivado e não haveria registro
de que o acréscimo valeu.

## Contexto

Jornada S000M → C000M → C050M → C068M → C681T.
Ator: servidor de CRE — apura o aditivo dos itens do contrato da sua coordenação regional
escolar, confere o cálculo pelo relatório e o aplica às permissões, dentro da secretaria em que
entrou.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**,
não regra de negócio.

O que esta tela usa do que veio antes é o **tipo de órgão da secretaria** escolhida no LOGON —
ele entra na identificação de tudo o que a tela lê e a tela não deixa digitá-lo —, além da
**matrícula**, do **acesso**, da **coordenação regional** e da **data e hora do sistema** da
sessão. Essas são regras da entrada e estão no anexo de evidências, em **Regras que se revelaram
da entrada**.

A tela anterior da jornada é um menu, e esta tela não recebe dela nem o registro nem a operação:
o modo de operação vem no próprio registro da transação e, em branco, é assumido pela própria
tela (RN-02). A jornada termina aqui: a única tela a que a C681T leva é ela mesma, reapresentada
com o resultado do cálculo.

---

## Regras de negócio

### RN-01 — A tela apura o aditivo do contrato e o aplica às permissões

A tela trata do aditivo do **conjunto do contrato**, e não de um item isolado. Em um primeiro
momento ela **calcula**: monta a lista dos itens da permissão com o percentual ou a quantidade
que se pretende acrescer, apura o valor correspondente e confere o teto. Emitido o relatório do
cálculo (RN-14), ela **aplica**: soma o aditivo às permissões e marca o cálculo como atualizado.

A tela enxerga **nove cadastros**. **Oito** deles ela lê — o de telas, o do tipo de órgão, o da
permissão, o de gêneros, o do cálculo do aditivo, o do servidor, o da impressora do servidor e o
das requisições de relatório — e **quatro** ela grava: o do cálculo do aditivo, o da permissão e
o da impressora do servidor, que também lê, e a **trilha de auditoria**, que ela só grava. Do
cadastro do cálculo do aditivo ela também **apaga**.

A permissão comporta até **1.000.000** de registros; o cálculo do aditivo, **50.000**; as
requisições de relatório, **90.000**; o cadastro do servidor, **20.000**; o da impressora do
servidor, **10.000**; o de gêneros, **150.000**; o do tipo de órgão, **200**; o de telas,
**2.000**; e a trilha de auditoria, **60.000.000**.

A conferência de acesso do sistema vem antes das leituras da permissão, do gênero e do cálculo;
sem ela, a tela não segue.

[?] Os números acima são **capacidade** — o máximo esperado, parâmetro de dimensionamento —, e
não volume cadastrado: o acervo não diz quantos registros existem de fato em cada cadastro.
Pergunta ao site.

[?] O nome de negócio desta tela não vem do acervo: a ficha estrutural do programa está truncada
e a máscara da tela não está no lote. O nome usado nesta estória — "calcular e aplicar o aditivo
do contrato" — é leitura de negócio apoiada nas mensagens da própria tela, no cabeçalho dos dois
relatórios que ela emite e na comparação com as telas vizinhas do mesmo menu, das quais uma
trata do aditivo de quantidade de **um item** e outra do aditivo de **valor**. Pergunta ao site
se o nome deve ser esse na web.

### RN-02 — Os três modos são consulta, alteração e exclusão, e a consulta não grava

A tela tem um modo de operação que só admite três valores: os que a recusa nomeia como **ALT**,
**EXC** e **CON**. Qualquer outro valor é recusado com
**\* Opcao nao disponivel. Use ALT, EXC ou CON \***, com o cursor no campo do modo, e a transação
não segue. Quando a tela abre sem modo informado, ela assume sozinha o modo **consulta**.

No modo **consulta** nada é gravado: a consulta termina por si mesma, antes de qualquer passagem
que gravaria, e os campos de comando do cálculo e da atualização são zerados. No modo
**alteração** a tela calcula e registra o aditivo de uma linha ou de todo o contrato (RN-11,
RN-12), atualiza as permissões (RN-13) e emite os relatórios (RN-14); no modo **exclusão** ela
apaga o cálculo do contrato (RN-15).

[?] A recusa manda usar **ALT**, **EXC** e **CON**, mas as guardas comparam códigos internos do
sistema, e a varredura do acervo não encontra nenhum lugar em que o texto que o servidor lê seja
convertido no código que o programa compara. A correspondência é conclusão tirada da mensagem,
não verificada na fonte. Pergunta ao site.

[?] A tela também encerra a lógica sem processar nada quando vem preenchido, no registro da
transação, o campo de **prefixo de tela** — um código de cinco posições que o programa apenas
repõe e exibe, e que nenhum programa do acervo escreve. O que ele é em negócio e quem o
preenche não estão no corpus. Pergunta ao site.

### RN-03 — O aditivo é identificado pelo órgão da sessão, pela coordenação regional, pelo tipo de contrato, pelo período, pelo grupamento e pelo item

A tela localiza a permissão pelo **tipo de órgão da secretaria da sessão**, que não se digita,
pela **coordenação regional escolar**, pelo **tipo de contrato**, pela **data limite do período**
— dia, mês e ano —, pelo **grupamento** (o grupo de licitação) e pelo **item** — classe,
subclasse e gênero. A **data de início do período** e as datas-base não identificam a permissão:
elas vêm do cadastro e são apenas mostradas.

O **gênero** é conferido no cadastro de gêneros pela classe, subclasse, gênero e data de início
do período, e a tela mostra a descrição resumida que o cadastro traz; não achando a descrição,
ela mostra uma sequência de asteriscos.

O cadastro do cálculo do aditivo é lido pela mesma coordenação regional, tipo de contrato e data
limite, mais o grupamento e o item; é por essa chave que a tela percorre as linhas de um cálculo.
A tela traz ainda uma **segunda identificação** — coordenação regional, tipo de contrato e data
limite —, que ela nunca preenche a partir de nenhum cadastro: é o servidor que a digita, para
recarregar um cálculo já existente (RN-12).

[?] O que distingue, em negócio, essa segunda identificação da primeira — se é o mesmo contrato
com outra grafia de chave ou um cálculo de outro contrato e outro período — não está na fonte: a
máscara da tela não está no acervo e os rótulos que o programa traz para esses campos são os
nomes que eles têm no programa, não rótulos de negócio. A segunda identificação alimenta uma
leitura do cadastro do cálculo com fontes de dados diferentes da primeira. Pergunta ao site.

[?] Os nomes de negócio dos dois cadastros que esta tela move — "a permissão" e "o cálculo do
aditivo" — não são transcrição do acervo: vêm das mensagens da própria tela, do uso que as telas
vizinhas fazem dos mesmos cadastros e do cabeçalho do relatório. Pergunta ao site se devem ser
esses os nomes na web.

### RN-04 — A coordenação regional informada tem de ser a do acesso do servidor

Informada uma coordenação regional, ela tem de ser a mesma que o sistema determina para o acesso
do servidor. Não sendo, a recusa é **\* Usuario sem acesso a este grupo \***, com o cursor de
volta ao campo da coordenação regional escolar, e nada é lido nem gravado. Quando a sessão não
carrega coordenação regional alguma, a tela não faz essa conferência.

[?] A conferência compara o que foi digitado com uma referência que a própria tela não alimenta:
quem deveria preenchê-la é a rotina de roteamento do sistema, que é declarada no programa e não
tem corpo em nenhum arquivo do acervo. Na prática essa referência é a área de trabalho que as
telas anteriores deixam na sessão — outras telas do sistema a escrevem com a coordenação regional
dos seus próprios registros —, e nada garante que ela seja a do acesso do servidor quando esta
tela abre. Se ela estiver zerada, a tela não confere; se estiver preenchida com outra coordenação,
recusa qualquer coordenação regional informada. Pergunta ao site qual é a intenção.

### RN-05 — Antes de alterar ou excluir, é preciso ter consultado

Na alteração, se a coordenação regional, o tipo de contrato ou a data limite informados forem
diferentes dos que a tela mostrou, a recusa é **\* Consulte antes de atualizar \***, com o
cursor no campo do modo. Na exclusão vale o mesmo, com **\* Consulte antes de excluir \***.
Consultar é o que preenche a tela com a permissão e o cálculo do contrato: sem isso, a tela não
sabe o que vai alterar nem o que vai apagar.

Na consulta, mudados os campos de identificação, a tela procura de novo a permissão daquele
contrato e mostra o primeiro item que encontrar.

### RN-06 — Sem a permissão, sem o cálculo ou sem o cálculo pendente, a operação é recusada

- procurada a permissão pela combinação informada e não existindo, a recusa é
  **\* Permissao nao cadastrada \***, com o cursor de volta ao campo da coordenação regional
  escolar, e nada é mostrado nem calculado. A exclusão não é recusada por esse motivo;
- na exclusão, não havendo nenhuma linha de cálculo para o contrato, a recusa é
  **\* Nao existem aditivos para exclusao \***, com o cursor no campo do modo;
- pedido o relatório do cálculo, não havendo nenhuma linha de cálculo com quantidade aditivada, a
  recusa é **\* Nao existem aditivos para calculo \***, com o cursor na marca do cálculo;
- pedida a atualização, não havendo nenhuma linha com cálculo pendente, a recusa é
  **\* Nao existe calculo do aditivo \***, com o cursor na marca da atualização.

Na atualização, a linha do cálculo cujo item não tem mais permissão é apagada em vez de recusar a
operação.

### RN-07 — O aditivo exige uma das duas formas — a quantidade ou o percentual —, e o percentual não passa de 25

A alteração do aditivo de uma linha se faz pelo **percentual** ou pela **quantidade**. Informados
os **dois**, a recusa é **\* Informe quantidade ou percentual \***, com o cursor no campo da
quantidade. O percentual da linha e o do cabeçalho — este comanda o cálculo de todos os itens do
contrato (RN-11) — não podem passar de **25**: acima disso a recusa é
**\* Maior percentual = 25 \***.

[?] A recusa **\* Informe quantidade ou percentual \*** é dada quando a quantidade **e** o
percentual vêm informados — o contrário do que a mensagem sugere e do que fazem as telas irmãs do
mesmo menu, onde a mesma recusa é dada quando **nenhum** dos dois vem. A gravação, depois da
conferência, aceita os dois e faz prevalecer o percentual. Ou a guarda está invertida, ou a
intenção é mesmo não aceitar as duas formas juntas. Não se escolheu um dos dois lados. Pergunta
ao site.

### RN-08 — O aditivo não passa de 25% da quantidade inicial, somado o que já foi aditivado

O teto do aditivo é **25% da quantidade inicial do item** e o valor correspondente a esse teto,
apurado com o preço do item ajustado pelo percentual com sinal e duas casas decimais registrado
na permissão. O aditivo informado é conferido contra esse teto: se a quantidade passar, a recusa
é **<- Quantidade maxima \***, com o valor do teto mostrado ao lado e o cursor no campo da
quantidade; se o valor passar, a recusa é **<- Valor maximo \***, do mesmo modo.

O que a tela **registra** é o que ainda cabe. Ela soma o aditivo ao que o item já tem aditivado
e, passando do teto, reduz o aditivo à diferença entre o teto e o que já foi aditivado — em
quantidade e em valor. Na recarga de um cálculo já existente (RN-12), a linha cujo aditivo não
couber no teto não é regravada.

[?] A conferência compara o aditivo **novo** com o teto, sem somar o que já foi aditivado; a
gravação soma o acumulado e reduz o aditivo ao que cabe. Um aditivo que passa na conferência
pode, portanto, ser gravado menor do que o informado, e o servidor não vê recusa nenhuma. Se a
intenção era recusar, ou se a redução substitui a recusa, a fonte não diz. Pergunta ao site.

### RN-09 — A tela lista os itens do cálculo com o inicial, o aditivo e o novo aditivo

A tela mostra no cabeçalho a descrição do tipo de órgão da sessão e a data do sistema e, para a
permissão, a descrição resumida do gênero. Cada linha da lista traz o **grupamento**, a
**classe**, a **subclasse** e o **gênero**, o **percentual**, a **quantidade** e o **valor do
aditivo**, a **marca da linha**, a **quantidade e o valor iniciais** e a **quantidade e o valor
já aditivados** do item.

A lista comporta até **400 itens** e até **50 grupamentos de licitação**, e a tela a apresenta em
blocos de **seis linhas** por vez.

[?] As quantidades de 400 itens e 50 grupamentos são o dimensionamento das tabelas internas do
programa e o limite dos laços que as percorrem; a máscara da tela não está no acervo, e por isso
não se sabe se correspondem ao que a tela permite cadastrar. Pergunta ao site.

### RN-10 — A alteração só age sobre a linha marcada, e o cálculo e a atualização têm cada um a sua marca

A alteração do aditivo de uma linha só acontece se a linha vier **marcada**. Não vindo, a tela
não faz nada com ela. Vindo marcada e sem quantidade e sem percentual, a linha do cálculo daquele
item é **apagada**; vindo marcada com quantidade ou percentual, a linha é calculada e gravada.
Sem o grupamento informado na linha, a recusa é **\* Atualize linha preenchida \***, com o cursor
no fim da linha.

O relatório do cálculo e a atualização das permissões têm, cada um, a sua **marca de comando** na
tela. A tela escreve as três marcas **desligadas** quando se apresenta, e o acervo não tem nenhum
programa de tela que as ligue.

[?] As três marcas — a da linha, a do cálculo e a da atualização — são campos da tela que o
acervo só escreve desligados, e a máscara da tela, que diria quem pode ligá-las e como, não está
no acervo. Se elas não puderem ser ligadas pelo terminal, a alteração de linha, o relatório e a
atualização nunca acontecem e a tela fica só de consulta. Pergunta ao site.

### RN-11 — Informado o percentual, a tela calcula o aditivo do contrato e regrava o cálculo

Informado o **percentual do cabeçalho**, a tela lê a permissão do contrato, aplica o percentual
sobre a quantidade inicial, apura a quantidade e o valor do aditivo, reduz o que passar do teto
ao que ainda cabe (RN-08) e regrava a linha do cálculo, criando-a quando não existe. Cada
regravação deixa rastro na auditoria (RN-16).

O **valor do aditivo** não é o preço de tabela: é a quantidade aditivada multiplicada pelo preço
do item ajustado pelo percentual com sinal e duas casas decimais registrado na permissão — o
preço multiplicado por um mais esse percentual dividido por cem.

[?] O que é, em negócio, esse percentual com sinal e duas casas decimais guardado na permissão
não está nomeado em nenhuma mensagem do acervo: a leitura "desconto" vem do nome que o campo tem
no programa, não de uma fonte de negócio — e um desconto que **aumenta** o valor unitário é
contraditório. Pergunta ao site.

### RN-12 — Identificado um cálculo, a tela o recarrega com os dados atuais da permissão

Informada a segunda identificação (a coordenação regional, o tipo de contrato e a data limite do
cálculo), a tela lê as linhas daquele cálculo e, para cada uma, lê a permissão do item
correspondente, refaz o cálculo pelo percentual ou pela quantidade que a linha já trazia, confere
o teto e regrava a linha com os valores atuais da permissão. A linha cujo aditivo não couber no
teto **não é regravada** — o cálculo daquele item é descartado.

### RN-13 — A atualização soma o cálculo às permissões e totaliza o valor aditivado por grupamento

Marcada a atualização, a tela percorre as linhas do cálculo do contrato e:

- apaga a linha que **não** está com o cálculo pendente;
- apaga a linha de quantidade aditivada zero;
- apaga a linha cujo item não tem mais permissão;
- nas demais, soma a quantidade e o valor do aditivo à quantidade e ao valor **já aditivados** da
  permissão daquele item — é isso que faz o aditivo passar a valer — e marca a linha como
  **atualizada**.

Em seguida, para cada **grupamento de licitação** envolvido, a tela soma o valor já aditivado de
todos os itens daquele grupamento e regrava esse total como o **valor do aditivo** da permissão
de cada item do grupamento. Ao final, a tela emite o relatório do aditivo aplicado (RN-14), mostra
**\* Cadastro Atualizado \*** e volta ao modo consulta.

Nada mais da permissão é tocado: fornecedor, tipo de licitação, datas, preços e quantidades
iniciais permanecem como estavam.

[?] A atualização só conserva as linhas cuja marca diz **cálculo pendente**, e quem escreve essa
marca é o programa do relatório do cálculo, que não é uma tela e é chamado pela requisição de
relatório (RN-14). Se o relatório não for emitido entre o cálculo e a atualização, a atualização
apaga todas as linhas do contrato sem somar nada às permissões e ainda assim mostra
**\* Cadastro Atualizado \***. Pergunta ao site se esse é o comportamento pretendido.

### RN-14 — O cálculo do aditivo sai em relatório antes de valer

Marcada a marca do cálculo, a tela emite o **relatório do cálculo do aditivo** — o que lista, por
grupamento, o inicial, o aditivo e o novo aditivo de cada item, com os totais do grupamento e o
total do aditivo — e é ele que confere o conjunto do contrato antes de o acréscimo valer. A
segunda marca emite o **relatório do aditivo aplicado**, que lista, por grupamento, o inicial e o
novo aditivo das linhas já aplicadas.

Antes de emitir, a tela exige três coisas:

- que **não haja relatório do mesmo tipo em processamento** para a mesma coordenação regional:
  havendo, a recusa é **\* Relatorio em processamento. Aguarde. \***, com o cursor na marca;
- que a **impressora** esteja informada: sem ela, a recusa é **\* Informe a impressora \***, com o
  cursor no campo da impressora;
- que o **servidor tenha correio eletrônico** cadastrado: sem ele, a recusa é
  **\* Usuario sem e-mail cadastrado \***, com o cursor no campo da coordenação regional escolar.

A impressora informada fica **guardada no cadastro do servidor**, como sua preferência: a tela só
a regrava quando ela muda. O relatório é pedido para a impressora informada, em uma cópia, e para
o correio eletrônico do servidor.

[?] O programa que imprime os relatórios não está no acervo das telas: o que a tela sabe é o nome
com que o pede e os dois códigos de relatório. O conteúdo de cada um foi lido no próprio programa
de impressão, que não é uma fonte de negócio, e não se sabe se os dois devem continuar existindo
na web ou se viram um só. Pergunta ao site.

### RN-15 — O cálculo atualizado tem de ser excluído antes de um novo aditivo

Existindo, para o contrato, alguma linha de cálculo já **atualizada**, a alteração é recusada com
**\* Cad.atualizado. Exclua para novo aditivo \***, com o cursor no campo do modo: o aditivo já
aplicado não se refaz por cima. Para calcular um novo aditivo do mesmo contrato, o servidor exclui
o cálculo — no modo exclusão — e recomeça.

A exclusão percorre as linhas do cálculo do contrato, registra na auditoria a imagem de cada uma
antes de apagá-la e **apaga** todas. Ao final, a tela volta ao modo consulta.

### RN-16 — Toda operação deixa rastro na trilha de auditoria

Cada gravação e cada exclusão desta tela deixa um registro na **trilha de auditoria**, com o dado
auditado, a operação (inclusão, alteração ou exclusão), a imagem do registro **antes** e a de
**depois**, e o contexto da sessão: tipo de órgão, coordenação regional, matrícula, terminal,
data e hora. O que se apaga fica registrado com a imagem de antes e a de depois vazia.

O número de processo que vai para a auditoria é montado pela própria tela, com o tipo de
contrato, a data limite do período e o grupamento.

[?] O cadastro da trilha de auditoria não traz nome de negócio nem comentário no acervo: a leitura
desta estória vem do uso que todas as telas fazem dele e dos campos que a própria tela preenche.
Pergunta ao site.

### RN-17 — Todos os campos passam pela edição numérica antes das conferências

Nenhum campo desta tela é texto livre. São **29** os campos com rótulo que passam pela edição
numérica antes de qualquer conferência de cadastro: os códigos de identificação (coordenação
regional, tipo de contrato, grupamento, classe, subclasse e gênero), as doze partes das quatro
datas (início do período, limite e a data limite do cálculo), os dois percentuais, as quantidades
e os valores do aditivo e os iniciais, e os quatro códigos do item lido. O que não for número é
recusado no próprio campo, com o cursor devolvido a ele quando ele tem posição mapeada, e não
chega a ser conferido.

[?] A rotina que faz essa conferência não está no acervo e o texto da mensagem que o servidor vê
ao digitar letra num campo não pôde ser conferido. Só **17** dos 29 campos têm posição de cursor
mapeada; os outros 12 não têm, e a fonte não diz se é intencional. Pergunta ao site.

### RN-18 — A leitura que falha interrompe a transação

Toda leitura desta tela testa o retorno do banco. O "registro não encontrado" é tratado como
ausência e vira a recusa correspondente; qualquer outro erro é levado à rotina de comunicação do
sistema, e a transação para ali, sem completar o resto. Uma leitura que falhou não segue para o
passo seguinte.

[?] O que essa rotina de comunicação faz com a transação não pôde ser conferido — ela não está no
acervo, e é dela que depende se a leitura que falhou realmente barra o que vem depois. Pergunta
ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Calcular e aplicar o aditivo do contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a matrícula, o acesso, a coordenação regional e a data do sistema
    E tenho acesso à tela C681T

  Cenário: RN-02 — modo diferente de ALT, EXC e CON
    Dado que estou na tela C681T
    Quando informo um modo diferente de alteração, de exclusão e de consulta
    Então vejo "* Opcao nao disponivel. Use ALT, EXC ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-02 — a tela abre sem modo informado
    Dado que abro a tela C681T sem informar o modo
    Então a tela está no modo consulta
    E nada é gravado

  Cenário: RN-02 — a consulta não grava nada
    Dado que estou na tela C681T no modo consulta e a permissão do contrato existe
    Quando confirmo a consulta
    Então a tela apenas apresenta a permissão e o cálculo do aditivo do contrato
    E a permissão e o cálculo continuam como estavam

  Cenário: RN-03 — o que a consulta mostra
    Dado que a permissão do contrato existe e tem linhas de cálculo
    Quando confirmo a consulta
    Então vejo a descrição do tipo de órgão, a data do sistema e a descrição resumida do gênero
    E cada linha mostra o grupamento, a classe, a subclasse, o gênero, o percentual, a quantidade e o valor do aditivo, a quantidade e o valor iniciais e o que já foi aditivado

  Cenário: RN-04 — coordenação regional que não é a do meu acesso
    Dado que a minha sessão carrega a coordenação regional do meu acesso
    Quando informo uma coordenação regional diferente
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo da coordenação regional escolar
    E nada é lido

  Cenário: RN-05 — alterar sem consultar antes
    Dado que estou na tela C681T no modo alteração
    Quando a coordenação regional, o tipo de contrato ou a data limite informados não são os que a tela mostrou
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-05 — excluir sem consultar antes
    Dado que estou na tela C681T no modo exclusão
    Quando a coordenação regional, o tipo de contrato ou a data limite informados não são os que a tela mostrou
    Então vejo "* Consulte antes de excluir *"
    E o cursor fica no campo do modo
    E nada é apagado

  Cenário: RN-06 — permissão não cadastrada
    Dado que estou na tela C681T
    Quando a coordenação regional, o tipo de contrato e a data limite informados não têm permissão cadastrada
    Então vejo "* Permissao nao cadastrada *"
    E o cursor fica no campo da coordenação regional escolar
    E nada é mostrado

  Cenário: RN-06 — não existem aditivos para exclusão
    Dado que estou na tela C681T no modo exclusão e a permissão existe
    Quando o contrato não tem nenhuma linha de cálculo do aditivo
    Então vejo "* Nao existem aditivos para exclusao *"
    E o cursor fica no campo do modo
    E nada é apagado

  Cenário: RN-06 — não existem aditivos para cálculo
    Dado que estou na tela C681T no modo alteração, com a permissão do contrato
    Quando marco o cálculo sem que nenhuma linha tenha quantidade aditivada
    Então vejo "* Nao existem aditivos para calculo *"
    E o cursor fica na marca do cálculo
    E nada é gravado

  Cenário: RN-06 — não existe cálculo do aditivo
    Dado que estou na tela C681T no modo alteração, com a permissão do contrato
    Quando marco a atualização sem que nenhuma linha esteja com o cálculo pendente
    Então vejo "* Nao existe calculo do aditivo *"
    E o cursor fica na marca da atualização
    E nada é gravado

  Cenário: RN-07 — quantidade e percentual informados juntos
    Dado que estou na tela C681T no modo alteração e a permissão do contrato existe
    Quando informo a quantidade e o percentual do aditivo da mesma linha
    Então vejo "* Informe quantidade ou percentual *"
    E o cursor fica no campo da quantidade
    E nada é gravado

  Cenário: RN-07 — percentual da linha acima de 25
    Dado que estou na tela C681T no modo alteração e a permissão do contrato existe
    Quando informo o percentual do aditivo de uma linha acima de 25
    Então vejo "* Maior percentual = 25 *"
    E o cursor fica no fim da linha
    E nada é gravado

  Cenário: RN-07 — percentual do cabeçalho acima de 25
    Dado que estou na tela C681T no modo alteração e a permissão do contrato existe
    Quando informo o percentual do contrato acima de 25
    Então vejo "* Maior percentual = 25 *"
    E o cursor fica no campo do percentual
    E nada é gravado

  Cenário: RN-08 — o aditivo passa da quantidade máxima
    Dado que a permissão do item tem quantidade inicial
    Quando a quantidade do aditivo passa de 25% da quantidade inicial, somado o que já foi aditivado
    Então vejo "<- Quantidade maxima *" com o valor do teto
    E o cursor fica no campo da quantidade
    E nada é gravado

  Cenário: RN-08 — o aditivo passa do valor máximo
    Dado que a permissão do item tem quantidade inicial e preço
    Quando o valor do aditivo passa do valor correspondente a 25% da quantidade inicial
    Então vejo "<- Valor maximo *" com o valor do teto
    E o cursor fica no campo da quantidade
    E nada é gravado

  Cenário: RN-08 — o aditivo é reduzido ao que ainda cabe
    Dado que a permissão do item já tem parte dos 25% aditivada
    Quando a tela aplica um aditivo que, somado ao já aditivado, passa do teto
    Então a tela registra apenas a diferença entre o teto e o que já foi aditivado
    E a quantidade aditivada da permissão não passa de 25% da quantidade inicial

  Cenário: RN-10 — a linha marcada sem o grupamento
    Dado que estou na tela C681T no modo alteração
    Quando marco a linha sem informar o grupamento
    Então vejo "* Atualize linha preenchida *"
    E o cursor fica no fim da linha
    E nada é gravado

  Cenário: RN-10 — a alteração sem a linha marcada não faz nada
    Dado que estou na tela C681T no modo alteração, com a permissão do contrato
    Quando informo o percentual de uma linha que não veio marcada
    Então a linha do cálculo daquele item não é calculada nem gravada

  Cenário: RN-10 — a linha marcada sem quantidade e sem percentual é apagada
    Dado que estou na tela C681T no modo alteração e o cálculo tem uma linha para o item
    Quando marco a linha e não informo a quantidade nem o percentual
    Então a linha do cálculo daquele item é apagada
    E a exclusão fica registrada na auditoria

  Cenário: RN-11 — o cálculo pelo percentual do cabeçalho
    Dado que estou na tela C681T no modo alteração, com a permissão do contrato
    Quando informo o percentual do cabeçalho e confirmo
    Então a tela calcula o aditivo do contrato pelo percentual, reduz o que passar do teto ao que ainda cabe
    E regrava a linha do cálculo, criando-a quando não existe
    E cada regravação fica registrada na auditoria

  Cenário: RN-12 — a recarga de um cálculo identificado
    Dado que estou na tela C681T no modo alteração e existe um cálculo para a segunda identificação informada
    Quando informo a segunda identificação e confirmo
    Então a tela refaz o cálculo de cada linha com os dados atuais da permissão
    E as linhas cujo aditivo não cabe no teto não são regravadas

  Cenário: RN-13 — a atualização soma o aditivo às permissões
    Dado que o cálculo do contrato tem linhas com o cálculo pendente
    Quando marco a atualização e confirmo
    Então a quantidade e o valor do aditivo são somados à quantidade e ao valor já aditivados de cada permissão
    E as linhas do cálculo passam a estar marcadas como atualizadas
    E vejo "* Cadastro Atualizado *"

  Cenário: RN-13 — a atualização apaga o que não é o cálculo
    Dado que o cálculo do contrato tem linhas sem o cálculo pendente, linhas de quantidade zero e linhas de itens sem permissão
    Quando marco a atualização e confirmo
    Então essas linhas são apagadas com o registro na auditoria
    E elas não alteram nenhuma permissão

  Cenário: RN-13 — o valor do aditivo do grupamento é totalizado
    Dado que a atualização somou o aditivo aos itens de um grupamento
    Quando a atualização termina
    Então o total já aditivado do grupamento é regravado como valor do aditivo na permissão de cada item do grupamento

  Cenário: RN-14 — relatório em processamento
    Dado que já há um relatório deste tipo em processamento para a minha coordenação regional
    Quando marco o cálculo e confirmo
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor fica na marca do cálculo
    E nada é gravado

  Cenário: RN-14 — informe a impressora
    Dado que estou na tela C681T no modo alteração e há linhas de cálculo com quantidade aditivada
    Quando marco o cálculo sem informar a impressora
    Então vejo "* Informe a impressora *"
    E o cursor fica no campo da impressora
    E o relatório não é emitido

  Cenário: RN-14 — usuário sem e-mail cadastrado
    Dado que o meu cadastro de servidor não tem correio eletrônico
    Quando marco o cálculo e confirmo
    Então vejo "* Usuario sem e-mail cadastrado *"
    E o cursor fica no campo da coordenação regional escolar
    E o relatório não é emitido

  Cenário: RN-14 — o relatório do cálculo é emitido
    Dado que estou na tela C681T no modo alteração, com o cálculo do contrato montado
    E que não há relatório em processamento, a impressora está informada e tenho correio eletrônico
    Quando marco o cálculo e confirmo
    Então o relatório do cálculo do aditivo é pedido para a impressora informada, em uma cópia, e para o meu correio eletrônico
    E a impressora informada fica guardada no meu cadastro
    E a tela volta ao modo consulta

  Cenário: RN-15 — cálculo já atualizado
    Dado que o contrato já tem uma linha de cálculo marcada como atualizada
    Quando tento alterar o aditivo do contrato
    Então vejo "* Cad.atualizado. Exclua para novo aditivo *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-15 — a exclusão libera o contrato para um novo aditivo
    Dado que o contrato tem um cálculo atualizado
    Quando informo o modo exclusão, consulto e confirmo
    Então todas as linhas do cálculo daquele contrato são apagadas com o registro na auditoria
    E a tela volta ao modo consulta
    E o contrato pode receber um novo aditivo

  Cenário: RN-16 — a auditoria registra antes e depois
    Dado que alterei o aditivo de um item, apliquei o cálculo ou apaguei uma linha
    Quando a operação termina
    Então a trilha de auditoria tem o dado auditado, a operação, a imagem de antes e a de depois
    E tem o tipo de órgão, a coordenação regional, a matrícula, o terminal e a data e a hora da sessão

  Cenário: RN-17 — campo não numérico
    Quando preencho um dos campos da tela com letra
    Então a tela recusa o campo antes de qualquer conferência de cadastro
    E o cursor volta ao campo, quando ele tem posição mapeada
    E nada é lido

  Cenário: RN-18 — falha no banco durante a leitura
    Dado que a leitura de um dos cadastros falha
    Quando confirmo
    Então a transação é interrompida com o tratamento de erro do sistema
    E a operação não é completada
```
