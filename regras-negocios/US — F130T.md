# US — F130T — Manter o cadastro de fornecedores por CNPJ ou CPF

## Estória

Como **servidor da CRE que lança e confere as despesas da secretaria**, quero
**consultar, incluir, corrigir e excluir os fornecedores pelo CNPJ ou pelo CPF**,
para que **toda nota fiscal lançada no sistema fique ligada a um fornecedor
cadastrado e com o número de identificação conferido**.

O fornecedor é a contraparte de cada nota fiscal: quem lança a nota escolhe o
fornecedor na lista, e é a razão social dele que sai no documento e na prestação
de contas. A lista é uma só para toda a secretaria — não é por órgão —, e por
isso não basta digitá-la: o número de identificação precisa ter os dígitos
verificadores conferidos, e um fornecedor que já tem nota lançada não pode
simplesmente desaparecer da lista. Quando falta o fornecedor certo, quem lança a
nota não tem o que escolher; quando a lista tem número errado ou fornecedor
apagado, o vínculo da nota com quem a emitiu se perde e a prestação de contas não
fecha.

## Contexto

Jornada S000M → F000M → F100M → F130T.
Ator: servidor de CRE — mantém a lista de fornecedores que o lançamento de nota
fiscal usa.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e
menus.md`: é **dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada são menus: a `F130T` é aberta por opção de
menu, e não encadeada por uma tela que lhe passe o registro e a operação. Quem
chega escolhe na própria `F130T` o que fazer e sobre qual fornecedor, e a tela
termina nela mesma — não chama outra tela. É este cadastro que as telas de nota
fiscal leem depois.

Da sessão a tela usa o tipo de órgão, a CRE, a matrícula, o código de acesso e o
privilégio de quem opera, além da estação, da data e da hora.

As regras abaixo são só as da **tela desta jornada**; o que a tela anterior faz
com o próprio menu não é regra desta estória.

## Regras de negócio

### RN-01 — O cadastro de fornecedores e o que a tela mostra

O cadastro de fornecedores (`F131T`) é a lista de quem emite nota fiscal para a
secretaria. Cada fornecedor tem **três dados**: a **razão social**, de até 40
caracteres e de preenchimento obrigatório; o **número de identificação**, de até
14 caracteres, que pode ser CNPJ ou CPF; e a **marca do tipo** — se aquele número
é CNPJ ou CPF. Só a razão social é obrigatória; o número não é.

A tela mostra **7 fornecedores por vez**, e cada linha traz o número, a marca de
CNPJ ou de CPF, a razão social e a **situação** — o que se quer fazer com aquela
linha. O cadastro tem dois índices, um pelo número e outro pela razão social
seguida do número, e **nenhum dos dois proíbe repetição**. Quem impede dois
fornecedores com o mesmo número é a própria tela, na inclusão. A capacidade
dimensionada do cadastro é de **1.000 fornecedores** — máximo esperado, não o
volume cadastrado.

[?] O cadastro não tem órgão, secretaria nem CRE: se a lista é única para toda a
secretaria, nada no cadastro impede duas razões sociais iguais — basta o número
diferir. Se a regra de negócio exige razão social única, ela não está no cadastro
nem nesta tela. Pergunta ao site.

[?] O que a tela escreve como rótulo de cada campo, e o próprio nome por que ela
é conhecida, não estão no acervo: a definição da tela não veio no lote, e o nome
da tela é buscado num cadastro de telas cujo conteúdo também não veio. Os nomes
usados aqui — número de identificação, razão social, situação, opção — vêm do
cadastro de dados e das mensagens da tela, não da tela. Pergunta ao site.

### RN-02 — A tela abre na consulta e só aceita alteração e consulta

Chegando à tela sem opção de manutenção informada, ela assume a **consulta**. A
opção informada só pode ser a de **alteração** ou a de **consulta**; qualquer
outra é recusada com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor
de volta ao campo da opção, e nada é processado.

[?] A mensagem nomeia as opções pelas abreviaturas **ALT** e **CON**, e a
conferência compara o que foi informado com as siglas internas de alteração e de
consulta. Nenhum fonte do lote mostra quem traduz o que o operador digita na
sigla conferida — o mesmo desenho aparece nas outras telas de manutenção deste
sistema. Se não houver tradução, a conferência recusa toda opção, inclusive as
duas que a própria mensagem pede, e **a tela fica só de consulta**: incluir,
corrigir e excluir nunca acontecem. Pergunta ao site.

[?] A recusa da opção é conferida na abertura e não é refeita no caminho que
grava: o que separa uma recusa da gravação é a marca de falha que a rotina de
mensagem do ambiente deixa — rotina que não está no lote. Se ela não marcar, uma
linha com a opção recusada ainda assim é gravada. Pergunta ao site.

### RN-03 — A situação de cada linha diz o que fazer com ela

Em cada linha, a **situação** decide a operação: **I** inclui, **A** altera e
**E** exclui, e a operação assim decidida é a que vai para a conferência de
acesso de quem opera. Situação diferente de I, A e E não gera operação nenhuma.
A linha cujo número está todo em zeros é descartada antes das conferências.

[?] A situação E só produz exclusão no modo de alteração: no modo de consulta o
fluxo termina antes de qualquer conferência ou gravação. Se a tela deixa digitar
E em consulta, o que o operador espera ver é pergunta ao site.

[?] O número de identificação é um campo de texto, e a conferência que descarta a
linha o compara com zeros: uma linha com o número em branco pode não ser
descartada por ela. O que acontece com uma linha sem número marcada com situação
I é pergunta ao site.

### RN-04 — Ao abrir, a tela lista os fornecedores já cadastrados

Na abertura, a tela percorre o cadastro de fornecedores e preenche as 7 linhas
visíveis, marcando em cada uma se a identificação é por CNPJ ou por CPF. Quando
não há nenhum fornecedor cadastrado, ela avisa
**\* Nao existem fornecedores cadastrados \*** e posiciona o cursor na primeira
linha.

[?] A ordem da lista é conclusão provável — a leitura é pelo índice que começa
pela razão social — e não foi verificada: os sinalizadores de posicionamento da
leitura são do dialeto e não estão explicados no corpus. Pergunta ao site.

### RN-05 — A inclusão de fornecedor que já existe é recusada

Para incluir, a tela procura o número informado no cadastro de fornecedores.
Já existindo fornecedor com aquele número, a inclusão é recusada com
**\* Fornecedor ja cadastrado \***, com o cursor no campo da situação da linha, e
nada é gravado.

[?] Como nenhum dos dois índices do cadastro proíbe repetição, a unicidade do
número é convenção da tela e não do cadastro: se um registro repetido entrar por
outro caminho, a conferência acha o primeiro e recusa a inclusão de novo. Se a
unicidade precisa ser garantida na base, pergunta ao site.

### RN-06 — O número informado é conferido pelos dígitos verificadores

O número informado é conferido pelo cálculo dos dígitos verificadores: **CPF**,
de 11 dígitos, ou **CNPJ**, de 14 caracteres — e no CNPJ as letras são aceitas,
entrando na conta com os valores de 17 a 42 (A a Z). Não fechando a conta, a
recusa é **\* CNPJ invalido \*** quando a linha está marcada como CNPJ e
**\* CPF invalido \*** quando não está, com o cursor no campo da situação da
linha, e nada é gravado.

A marca que decide qual das duas conferências roda é a **de CNPJ**: sem ela, o
sistema trata o que foi digitado como CPF. Esta conferência só existe na
inclusão; a alteração não a repete.

[?] A coluna de CPF da linha não é lida em nenhum ponto do programa — quem decide
é a marca de CNPJ. Se a tela deixa marcar CPF sem marcar CNPJ, essa marca não
muda nada. Pergunta ao site.

### RN-07 — A razão social é obrigatória

Informado um número novo (na inclusão) ou um fornecedor existente (na alteração),
a razão social não pode ir em branco: sem ela a recusa é
**\* Informe a razao social \***, com o cursor no campo da razão social, e nada é
gravado. No cadastro a razão social é de preenchimento obrigatório; a tela avisa
antes disso.

### RN-08 — A alteração exige fornecedor cadastrado e regrava só a razão social

Para alterar, o fornecedor tem de existir — não existindo, a recusa é
**\* Fornecedor nao cadastrado \***, com o cursor no campo da situação da linha,
e nada é gravado. Passando a conferência, o sistema trava o registro e regrava
**apenas a razão social**: o número de identificação e a marca de CNPJ ou CPF
permanecem como estavam.

### RN-09 — A exclusão é recusada quando há nota fiscal lançada

Para excluir, o fornecedor tem de existir — não existindo, a recusa é
**\* Fornecedor nao cadastrado \*** — e não pode ter nota fiscal lançada: a tela
procura no cadastro de notas fiscais (`F155T`) alguma nota daquele fornecedor e,
achando, recusa com **\* Ja existem notas cadastradas \***, com o cursor no campo
do número, e o fornecedor continua cadastrado. Passando nas duas conferências, o
registro é travado e apagado.

A procura pelas notas é feita **no tipo de órgão da sessão**, que é a primeira
parte do índice de notas fiscais.

[?] O cadastro de fornecedores não é por órgão, mas a conferência das notas é: um
fornecedor com notas lançadas em outro tipo de órgão passa pela recusa e pode ser
apagado, deixando aquelas notas apontando para um fornecedor que não existe mais.
Se a conferência deveria alcançar todos os órgãos, pergunta ao site.

### RN-10 — A consulta não grava nada

Na consulta a tela só lê e mostra: ela lista os fornecedores, não confere as
linhas e desvia do caminho que grava. Nenhum fornecedor é incluído, alterado ou
apagado, e nenhum registro de auditoria é gerado.

### RN-11 — A operação só acontece se o perfil autorizar

Na abertura, a tela passa pela conferência de acesso — o cadastro de telas tem de
ter a tela, e o código de acesso de quem opera tem de ter a tela — e, por linha,
confere no mesmo código de acesso a autorização da operação que a situação pediu
(inclusão, alteração ou exclusão). Não estando liberada, a operação é recusada com
aviso e a tela é abandonada sem gravar. A conferência recebe o contexto da sessão:
matrícula, código de acesso, privilégio, CRE e tipo de órgão.

[?] Quem preenche a área da sessão de onde as telas desta jornada copiam a
matrícula, o código de acesso, o privilégio, a CRE e o tipo de órgão não está no
lote — o programa apenas copia o que já estava lá, e a entrada não cita nenhum
desses campos. Pergunta ao site.

### RN-12 — Cada operação grava no cadastro e deixa rastro na auditoria

Cada operação grava no cadastro de fornecedores — a inclusão cria o registro, a
alteração regrava a razão social e a exclusão apaga o registro — e grava, no
cadastro de auditoria (`A010T`), um registro por operação, com a operação
(inclusão, alteração ou exclusão), o cadastro tocado (`F131T`), a tela `F130T`, o
número do fornecedor, a matrícula de quem operou, a estação, a CRE, o tipo de
órgão, o dia e a hora da sessão e o conteúdo anterior e o posterior do registro;
na exclusão, o conteúdo posterior vai em branco. A tela só **lê** o cadastro de
telas e o cadastro das notas fiscais, e não grava em nenhum dos dois.

### RN-13 — Esta é a única tela do sistema que grava o cadastro de fornecedores

O mesmo cadastro é citado por outras cinco telas — as de nota fiscal `F150T`,
`F152T`, `F158T`, `F145C` e `F150C` —, mas todas elas apenas o leem: as rotinas de
gravar e de apagar o fornecedor estão escritas em cada uma e **nunca são
executadas**. Incluir, corrigir e excluir fornecedor só acontece por esta tela.

### RN-14 — A resposta volta com o nome do órgão e a data do sistema em branco

A descrição do tipo de órgão da sessão e a data do sistema, que a abertura mostra,
são apagadas a cada mensagem respondida e não são repostas: a resposta sai com os
dois campos em branco.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se
existe um caminho de entrada em que os campos não são limpos, não foi possível
determinar. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manter o cadastro de fornecedores por CNPJ ou CPF

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F130T

  Cenário: Abrir a tela mostra os fornecedores cadastrados
    Dado que o cadastro tem fornecedores
    Quando abro a tela F130T
    Então vejo os fornecedores, até 7 por vez, com o número, a marca de CNPJ ou CPF e a razão social
    E a tela abre na opção de consulta
    E nada é gravado

  Cenário: Cadastro sem nenhum fornecedor
    Dado que não existe nenhum fornecedor cadastrado
    Quando abro a tela F130T
    Então vejo a mensagem "* Nao existem fornecedores cadastrados *"
    E o cursor fica na primeira linha

  Cenário: A consulta não grava nada
    Dado que abri a tela e estou na opção de consulta
    Quando confirmo a mensagem
    Então o cadastro é apenas lido
    E nenhum fornecedor é incluído, alterado ou apagado
    E nenhum registro de auditoria é gerado

  Cenário: Opção diferente de alteração e de consulta
    Quando informo uma opção que não é a de alteração nem a de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: Inclusão de um fornecedor
    Dado que a opção é a de alteração
    E informo, numa linha, um número que ainda não está cadastrado, a razão social e a marca de CNPJ
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então o fornecedor passa a constar do cadastro
    E a auditoria registra a inclusão

  Cenário: Inclusão de fornecedor que já está cadastrado
    Dado que a opção é a de alteração
    E informo, numa linha, um número já cadastrado
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Fornecedor ja cadastrado *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: CNPJ com dígito verificador errado
    Dado que a opção é a de alteração
    E informo, numa linha, um CNPJ cujos dígitos verificadores não fecham
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* CNPJ invalido *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: CPF com dígito verificador errado
    Dado que a opção é a de alteração
    E informo, numa linha, um CPF cujos dígitos verificadores não fecham
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* CPF invalido *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: Inclusão sem a razão social
    Dado que a opção é a de alteração
    E informo, numa linha, um número que não está cadastrado, sem a razão social
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Informe a razao social *"
    E o cursor volta ao campo da razão social
    E nada é gravado

  Cenário: Alteração da razão social de um fornecedor
    Dado que a opção é a de alteração
    E o número informado está cadastrado
    E informo a nova razão social
    E assinalo nessa linha a situação A
    Quando confirmo a mensagem
    Então o cadastro passa a mostrar a nova razão social
    E o número de identificação continua o mesmo
    E a auditoria registra a alteração

  Cenário: Alteração sem a razão social
    Dado que a opção é a de alteração
    E o número informado está cadastrado e a razão social está em branco
    E assinalo nessa linha a situação A
    Quando confirmo a mensagem
    Então vejo a mensagem "* Informe a razao social *"
    E o cursor volta ao campo da razão social
    E nada é gravado

  Cenário: Alteração de fornecedor não cadastrado
    Dado que a opção é a de alteração
    E informo, numa linha, um número que não está cadastrado
    E assinalo nessa linha a situação A
    Quando confirmo a mensagem
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: Exclusão de fornecedor não cadastrado
    Dado que a opção é a de alteração
    E informo, numa linha, um número que não está cadastrado
    E assinalo nessa linha a situação E
    Quando confirmo a mensagem
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: Exclusão de um fornecedor sem nota fiscal lançada
    Dado que a opção é a de alteração
    E o número informado está cadastrado
    E não há nota fiscal daquele fornecedor no tipo de órgão da sessão
    E assinalo nessa linha a situação E
    Quando confirmo a mensagem
    Então o fornecedor sai do cadastro
    E a auditoria registra a exclusão, com o conteúdo posterior em branco

  Cenário: Exclusão recusada porque há nota fiscal lançada
    Dado que a opção é a de alteração
    E o número informado está cadastrado
    E existe nota fiscal daquele fornecedor no tipo de órgão da sessão
    E assinalo nessa linha a situação E
    Quando confirmo a mensagem
    Então vejo a mensagem "* Ja existem notas cadastradas *"
    E o cursor volta ao campo do número
    E o fornecedor continua cadastrado

  Cenário: Linha com situação desconhecida é ignorada
    Dado que a opção é a de alteração
    E preenchi uma linha com uma situação diferente de I, A e E
    Quando confirmo a mensagem
    Então aquela linha não gera operação nenhuma
    E nada é gravado

  Cenário: Sem autorização para a operação
    Dado que o meu código de acesso tem a tela F130T sem aquela operação liberada
    E informo a opção de alteração com uma linha preenchida
    Quando confirmo a mensagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela F130T
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Tela fora do cadastro de telas
    Dado que a tela F130T não consta do cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: A resposta volta com os dois campos de contexto em branco
    Dado que a tela abriu mostrando a descrição do tipo de órgão da sessão e a data do sistema
    Quando respondo uma mensagem
    Então a resposta vem com esses dois campos em branco
```
