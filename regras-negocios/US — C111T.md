# US — C111T — Manter as unidades de medida

## Estória

Como **servidor da CRE com a tela C111T autorizada**, quero **manter o cadastro das
unidades de medida — incluir uma unidade nova, corrigir a descrição de uma que já existe
e tirar a que ninguém usa**, para que **cada gênero de material seja cadastrado e medido
na unidade certa, sem que cada um invente a sua**.

A unidade de medida é a grandeza em que o gênero de material é medido, e é ela que o
gênero guarda no seu cadastro. Enquanto faltar a unidade certa na lista, quem cadastra
gênero não tem o que escolher; e uma unidade que já está em uso por algum gênero não pode
sair da lista, senão o gênero fica apontando para uma unidade que não existe mais. É esta
tela que faz as duas coisas: completa a lista e recusa retirar dela a unidade que está em
uso.

## Contexto

Jornada S000M → C000M → C015M → C111T.
Ator: servidor de CRE — mantém o cadastro das unidades de medida que os gêneros de
material usam.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A `C111T` é uma tela de transação, não um menu: ela mostra o cadastro das unidades de
medida **15 unidades por vez**, cada linha com o código, a descrição e a situação da
linha, e termina nela mesma. O mesmo cadastro é mantido também pela tela `C110T`, que
trata uma unidade por vez. O que a `C111T` usa da sessão — a matrícula de quem opera, o
código de acesso e o privilégio dela, a CRE, o tipo de órgão e o terminal — é o que a
entrada deixou. Quem chega a ela vem encadeado pela tela anterior, que não informa
operação nenhuma; por isso a tela abre na consulta, e a alteração só acontece se quem
opera a informar (RN-02).

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — O cadastro das unidades de medida e quem mais escreve nele

O cadastro das unidades de medida é a lista das grandezas que o cadastro dos gêneros de
material pode usar. Cada unidade tem um **código de até 5 caracteres** — que a identifica
e não se repete — e uma **descrição de até 15 caracteres**. No dicionário da base, só o
código é de preenchimento obrigatório; a descrição é exigida pela tela. A tela mostra
**15 unidades por vez** e o código não é atribuído pelo sistema: é o que estiver na linha.
Este mesmo cadastro é mantido também pela tela `C110T`.

[?] O que a tela escreve como rótulo de cada campo não está no acervo: a definição da tela
não veio no lote, e o programa desta tela não declara nem o título dela. Os nomes usados
aqui — código, descrição, situação, opção — vêm do cadastro de dados e das mensagens da
própria tela, não da tela. Pergunta ao site.

### RN-02 — A tela abre na consulta e só aceita alteração e consulta

Chegando à tela sem opção informada, ela assume a **consulta**. A opção informada só pode
ser **alteração** ou **consulta**; qualquer outra é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no campo da opção. A recusa
vale para a conferência das linhas, e não para o caminho que grava: esse caminho descarta
apenas a consulta.

[?] A mensagem nomeia as opções pelas abreviaturas **ALT** e **CON**, e a conferência
compara o que foi informado com as siglas internas de alteração e de consulta. Nenhum
fonte do lote mostra quem traduz o que o operador digita na sigla conferida — o mesmo
desenho aparece nas outras telas de manutenção deste sistema. Se não houver tradução, a
conferência recusa toda opção, inclusive as duas que a própria mensagem pede, e nenhuma
unidade é mantida por esta tela. Pergunta ao site.

[?] A recusa da opção não é conferida de novo no caminho que grava: ele descarta apenas a
consulta, e o que separa uma recusa da gravação é a marca de falha que a rotina de
mensagem do ambiente deixa — rotina que não está no lote. Se ela não marcar, uma linha com
a opção recusada ainda assim é gravada. Pergunta ao site.

### RN-03 — A situação de cada linha diz o que fazer com ela

Em cada linha, a **situação** decide a operação: **I** inclui, **A** altera, **E** exclui.
Linha com situação diferente de I, A e E não gera operação nenhuma — a tela passa adiante
sem avisar. Antes de qualquer gravação, a tela confere se o perfil de quem opera autoriza
a operação daquela linha.

[?] A linha cujo código é zero é descartada antes das conferências. O código, porém, é
alfanumérico e a conferência o compara com zeros: uma linha com o código em branco não é
descartada por ela. O que acontece com uma linha em branco com situação de inclusão é
pergunta ao site.

### RN-04 — Ao abrir, a tela lista as unidades cadastradas

Na abertura, a tela percorre o cadastro das unidades de medida e preenche as 15 linhas
visíveis, na ordem do código. Quando não há nenhuma unidade cadastrada, ela avisa
**\* Nao existem unidades de medidas cadastradas \*** e posiciona o cursor na primeira
linha.

[?] A ordem da lista é conclusão provável — a leitura é pela chave do cadastro, que é o
código — e não foi verificada: os sinalizadores de posicionamento da leitura são do
dialeto e não estão explicados no corpus.

### RN-05 — Inclusão de unidade que já existe é recusada

Para incluir, a tela procura o código informado no cadastro das unidades de medida. Já
existindo uma unidade com aquele código, a inclusão é recusada com
**\* Unidade de medida ja cadastrada \***, com o cursor no campo da situação da linha, e
nada é gravado.

### RN-06 — A inclusão exige a descrição

Informado um código que ainda não existe, a inclusão exige a descrição: sem ela, a recusa
é **\* Informe a descricao \***, com o cursor no campo da descrição, e nada é gravado.

### RN-07 — A alteração e a exclusão exigem unidade cadastrada

Para alterar ou excluir, o código informado tem de estar cadastrado; não estando, a recusa
é **\* Unidade de medida nao cadastrada \***, com o cursor no campo da situação da linha, e
nada é gravado. A alteração também exige a descrição — sem ela, a recusa é a mesma da
inclusão, **\* Informe a descricao \*** — e muda só a descrição: o código da unidade não é
alterado por esta tela.

### RN-08 — A exclusão é recusada quando algum gênero de material usa a unidade

Antes de excluir, a tela percorre o cadastro dos gêneros de material à procura de algum que
declare aquela unidade de medida. Achando, a recusa é
**\* Nao exclua. Generos com esta unidade \***, com o cursor no campo do código, e nada é
apagado. Como a unidade não faz parte da chave daquele cadastro, a conferência é registro a
registro — não há índice que responda direto.

[?] A conferência olha um único campo de unidade de medida do gênero, e o cadastro do
gênero tem dois. Se o outro também guarda a unidade usada, a recusa é parcial e a exclusão
passa por um gênero que continua apontando para a unidade apagada. O que o segundo campo
carrega é pergunta ao site.

[?] A varredura é completa: o cadastro dos gêneros de material é dimensionado para 150.000
registros, e cada tentativa de exclusão pode percorrer todos. Se essa varredura é
aceitável, pergunta ao site.

### RN-09 — A consulta não grava nada

Na consulta a tela só mostra: ela lista as unidades, não confere as linhas e desvia do
caminho que grava. Nenhuma unidade é incluída, alterada ou apagada, e nenhuma trilha de
auditoria é gerada.

### RN-10 — A operação só acontece se o perfil autorizar

Na abertura, a tela confere se ela própria existe no cadastro de telas — não existindo, o
aviso é **\* Tela nao disponivel \*** — e se o código de acesso de quem opera tem a tela —
não tendo, a recusa é **\* Acesso negado para esta matricula \***. A cada mensagem ela
confere de novo o cadastro de telas — tendo a tela sido retirada dele, o aviso é
**\* Tela nao cadastrada \*** — e, para a operação que a linha pede, a autorização daquela
operação no mesmo código de acesso — não tendo, a recusa é
**\* Acesso negado para esta operacao \***. Nas recusas nada é gravado. A conferência
recebe o contexto da sessão: a matrícula, o código de acesso, o privilégio, a CRE e o tipo
de órgão.

[?] De onde vêm esses dados da sessão não está em nenhum programa desta jornada: os
programas da entrada não os preenchem, e quem os preenche não veio no acervo. Pergunta ao
site.

### RN-11 — Cada operação grava no cadastro e deixa rastro na auditoria

A tela grava no cadastro das unidades de medida — a inclusão cria o registro, a alteração
regrava a descrição e a exclusão apaga o registro — e grava, no cadastro de auditoria
(`A010T`), um registro por operação, com a operação (inclusão, alteração ou exclusão), o
cadastro tocado, a tela `C111T`, a matrícula de quem operou, a estação, a CRE, o tipo de
órgão, o número do processo da sessão, a data e a hora, e o conteúdo anterior e o posterior
do registro. O rastro nomeia as duas telas: a que estava em uso, `C111T`, e a dona do
cadastro, `C110T`. A tela só lê o cadastro de telas e o dos gêneros de material, e não
grava em nenhum dos dois.

[?] Na alteração, o conteúdo anterior e o posterior são copiados da mesma área, sem que ela
seja remontada entre as duas cópias: as duas colunas da auditoria podem sair iguais, e quem
auditar não verá qual era a descrição antiga. A área não está declarada em nenhum arquivo
do lote. Pergunta ao site.

### RN-12 — Cada mensagem volta com os dois campos de contexto em branco

A descrição do tipo de órgão da sessão e a data do sistema, que a abertura mostra, são
apagadas a cada mensagem respondida e não são repostas: a resposta sai com os dois campos
em branco.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe um
caminho de entrada em que os campos não são limpos, não foi possível determinar. Pergunta
ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manter as unidades de medida

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C111T

  Cenário: Abrir a tela mostra as unidades cadastradas e não grava nada
    Dado que o cadastro tem unidades de medida cadastradas
    Quando abro a tela C111T
    Então vejo as unidades cadastradas, até 15 por vez, com código e descrição
    E a tela abre na opção de consulta
    E nada é gravado

  Cenário: Cadastro sem nenhuma unidade de medida
    Dado que não existe nenhuma unidade de medida cadastrada
    Quando abro a tela C111T
    Então vejo a mensagem "* Nao existem unidades de medidas cadastradas *"
    E o cursor fica na primeira linha

  Cenário: A consulta não grava nada
    Dado que abri a tela e estou na opção de consulta
    Quando confirmo a mensagem
    Então o cadastro é apenas lido
    E nenhuma unidade é incluída, alterada ou apagada
    E nenhuma trilha de auditoria é gerada

  Cenário: Opção diferente de alteração e de consulta
    Quando informo uma opção que não é a de alteração nem a de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: Inclusão de uma unidade de medida
    Dado que a opção é a de alteração
    E informo, numa linha, um código que ainda não está cadastrado e a sua descrição
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então a unidade passa a constar do cadastro
    E a auditoria registra a inclusão

  Cenário: Inclusão de unidade que já está cadastrada
    Dado que a opção é a de alteração
    E informo, numa linha, um código já cadastrado
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Unidade de medida ja cadastrada *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: Inclusão sem a descrição
    Dado que a opção é a de alteração
    E informo, numa linha, um código que não está cadastrado, sem descrição
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Informe a descricao *"
    E o cursor volta ao campo da descrição
    E nada é gravado

  Cenário: Alteração da descrição de uma unidade de medida
    Dado que a opção é a de alteração
    E o código informado está cadastrado
    E informo a nova descrição
    E assinalo nessa linha a situação A
    Quando confirmo a mensagem
    Então o cadastro passa a mostrar a nova descrição
    E o código da unidade continua o mesmo
    E a auditoria registra a alteração

  Cenário: Alteração ou exclusão de unidade não cadastrada
    Dado que a opção é a de alteração
    E informo, numa linha, um código que não está cadastrado
    E assinalo nessa linha a situação A ou a situação E
    Quando confirmo a mensagem
    Então vejo a mensagem "* Unidade de medida nao cadastrada *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: Alteração sem a descrição
    Dado que a opção é a de alteração
    E o código informado está cadastrado e a descrição está em branco
    E assinalo nessa linha a situação A
    Quando confirmo a mensagem
    Então vejo a mensagem "* Informe a descricao *"
    E nada é gravado

  Cenário: Exclusão de uma unidade de medida que nenhum gênero usa
    Dado que a opção é a de alteração
    E o código informado está cadastrado
    E nenhum gênero de material declara aquela unidade
    E assinalo nessa linha a situação E
    Quando confirmo a mensagem
    Então a unidade sai do cadastro
    E a auditoria registra a exclusão

  Cenário: Exclusão recusada porque um gênero de material usa a unidade
    Dado que a opção é a de alteração
    E o código informado está cadastrado
    E algum gênero de material declara aquela unidade
    E assinalo nessa linha a situação E
    Quando confirmo a mensagem
    Então vejo a mensagem "* Nao exclua. Generos com esta unidade *"
    E o cursor volta ao campo do código
    E a unidade continua cadastrada

  Cenário: Linha com situação desconhecida é ignorada
    Dado que a opção é a de alteração
    E preenchi uma linha com uma situação diferente de I, A e E
    Quando confirmo a mensagem
    Então aquela linha não gera operação nenhuma
    E nada é gravado

  Cenário: Sem autorização para a operação
    Dado que o meu código de acesso tem a tela C111T sem aquela operação liberada
    E informo a opção de alteração com uma linha preenchida
    Quando confirmo a mensagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela C111T
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Tela fora do cadastro de telas
    Dado que a tela C111T não consta do cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Tela retirada do cadastro de telas
    Dado que a tela C111T foi retirada do cadastro de telas
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é gravado

  Cenário: A resposta volta com os dois campos de contexto em branco
    Dado que a tela abriu mostrando a descrição do tipo de órgão da sessão e a data do sistema
    Quando respondo uma mensagem
    Então a resposta vem com esses dois campos em branco
```
