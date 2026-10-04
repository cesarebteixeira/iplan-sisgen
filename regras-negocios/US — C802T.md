# US — C802T — Manter os gêneros da alimentação escolar

## Estória

Como **servidor de CRE**, quero **manter o cadastro dos gêneros da alimentação
escolar — a classe e a subclasse do item, a descrição resumida, a unidade de compra e
as quantidades de conversão e de fracionamento**, para que **as telas que montam o
cardápio e estimam a compra da alimentação trabalhem com o item certo e na medida
certa**.

O gênero é o item da alimentação escolar: é ele que diz de que produto se trata, em
que subclasse e classe ele se encaixa, em que unidade ele é comprado, quanto contém e
em que medida pode ser fracionado. As outras telas do módulo — a montagem do cardápio
e as estimativas por período e por coordenação — leem este cadastro, e esta é a única
tela que o mantém. Sem o gênero cadastrado, ou com a unidade de compra ou a conversão
erradas, a quantidade e o preço que saem dessas telas saem errados.

## Contexto

Jornada S000M → C000M → C800M → C802T.

Ator: servidor de CRE — mantém o cadastro dos gêneros da alimentação escolar, um
gênero por vez, identificado pela subclasse e pelo código do gênero.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O contexto que a tela usa — matrícula,
código de acesso, privilégio, tipo de órgão, coordenação regional escolar e a data do
sistema — é o que a entrada deixou na sessão.

As regras abaixo são só as da tela desta jornada. O mesmo cadastro também é alcançado
pela tela de consulta `C802C`, e a regra RN-03 trata desse caminho.

---

## Regras de negócio

### RN-01 — A tela mantém o cadastro dos gêneros, um gênero por vez

A tela mantém o cadastro dos gêneros da alimentação escolar. Cada gênero é
identificado pelo **código da subclasse** (2 dígitos) e pelo **código do gênero**
(5 dígitos) e guarda, além da chave, **7 informações**: a **classe do gênero**
(4 dígitos), a **descrição resumida** (15 caracteres), a **unidade de compra**
(5 caracteres), o **padrão de conversão** (2 caracteres) e três quantidades — a
**quantidade do gênero** (até 5 inteiros e 3 decimais), a **unidade de conversão**
(até 5 inteiros e 3 decimais) e a **menor quantidade a fracionar** (até 3 inteiros e
2 decimais). No dicionário de dados, só a unidade de compra é de preenchimento
obrigatório.

A tela trabalha com **um gênero por vez**: não é lista e não tem paginação.

[?] O dicionário de dados não descreve as três quantidades. O que a "quantidade do
gênero" representa — quanto o item contém na unidade de compra? — e como ela se
relaciona com a "unidade de conversão" e com a "menor quantidade a fracionar" é
pergunta ao site. O que o acervo sustenta é que as duas últimas não podem ser zero na
inclusão nem na alteração, e que o padrão de conversão só aceita **g** ou **ml**.

### RN-02 — Ao abrir, a tela já está no modo de inclusão, com a subclasse e a classe nos valores máximos

Abrindo a tela pelo menu, o próprio sistema repõe o modo de **inclusão** e devolve a
mensagem ao estado vazio, de modo que a operação mostrada é sempre a inclusão. Os
campos da subclasse e da classe do gênero não vêm em branco: a subclasse vem com
**99** e a classe com **9999** — os valores máximos de cada campo.

[?] O que esses dois valores querem dizer — se são apenas o preenchimento máximo
usado para deixar o campo sem valor, ou se apontam para a última subclasse e a última
classe — não está no acervo. Como o gênero é identificado pela subclasse, isso muda o
que o operador vê ao abrir a tela. Pergunta ao site.

### RN-03 — Chegando pela consulta, a tela aproveita o gênero escolhido, mas volta à inclusão e descarta a subclasse e a classe

O mesmo cadastro é alcançado pela tela de consulta `C802C`, do mesmo menu. Quando a
sessão chega à `C802T` marcada com essa consulta, o sistema copia para os campos da
tela os valores do gênero que foi escolhido lá — a subclasse, o código do gênero, a
classe, a descrição resumida, a unidade de compra e as quantidades. Logo em seguida,
porém, a tela repõe o modo de **inclusão** e devolve a subclasse a **99** e a classe a
**9999**, apagando os dois valores que acabou de copiar e mantendo os demais.

[?] A cópia e a reposição estão no mesmo trecho, uma imediatamente depois da outra: a
subclasse faz parte da identificação do gênero, de modo que o gênero escolhido na
consulta não chega identificado à tela e o caminho consulta → manutenção parece não
fechar. Se a intenção era abrir a alteração com o gênero consultado, ou se a tela
deve mesmo voltar à inclusão, é pergunta ao site — não escolhi um dos dois lados.

### RN-04 — A tela executa inclusão, alteração, exclusão e consulta; opção desconhecida não faz nada

A tela reconhece quatro operações: **inclusão**, **alteração**, **exclusão** e
**consulta**. Cada uma segue por um caminho próprio: a inclusão confere os dados e
atribui o código; a alteração e a exclusão exigem que o gênero exista; a consulta
mostra o gênero e encerra. Informando uma opção diferente dessas quatro, a tela
**não executa operação nenhuma** e também não avisa nada: passa pelas conferências e
termina sem ler, sem gravar e sem mensagem.

[?] A tela não valida a opção informada contra uma lista: opção desconhecida cai fora
de todos os caminhos, em silêncio. Se a máscara já limita o que o operador pode
digitar, o caso não acontece; se não limita, o operador não recebe resposta. Pergunta
ao site.

### RN-05 — A inclusão confere os dados e o código do gênero é atribuído pelo sistema

Para incluir, o sistema exige a **descrição resumida** e confere: a **unidade de
compra** tem de existir no cadastro de unidades de compra; o **padrão de conversão**
tem de ser **g** ou **ml**; a **unidade de conversão** e a **menor quantidade a
fracionar** têm de ser diferentes de zero. A **quantidade do gênero** e a **classe**
não são exigidas nem conferidas contra cadastro nenhum: a classe é um número
informado livremente.

O **código do gênero não é digitado**: o sistema procura o último gênero cadastrado
naquela subclasse e atribui o **código seguinte**; não havendo nenhum, começa em
**1**. Passando nas conferências, o gênero é gravado e a tela confirma com
**\* Genero cadastrado com sucesso \***.

[?] A busca do "último gênero da subclasse" é feita com o código do gênero no valor
máximo do campo e depende de como a leitura trata esse valor: se ela procura a chave
exata, não acha nada e o código sai sempre **1** — e a segunda inclusão na mesma
subclasse tentaria gravar o gênero 1 outra vez. Não escolhi um dos dois lados;
pergunta ao site.

[?] A conferência da unidade de compra não olha a situação do cadastro dela: uma
unidade marcada como excluída ainda seria aceita. Pergunta ao site.

### RN-06 — A alteração exige o gênero cadastrado, confere os mesmos dados e não muda a classe

Para alterar, o gênero tem de existir — senão o sistema recusa com
**\* Genero nao cadastrado \***. Existindo, valem as mesmas conferências da inclusão:
descrição preenchida, unidade de compra cadastrada, padrão de conversão **g** ou
**ml**, unidade de conversão e menor quantidade a fracionar diferentes de zero. A
alteração grava a descrição resumida, a unidade de compra, o padrão de conversão e as
três quantidades — a **subclasse**, o **código do gênero** e a **classe do gênero**
não são alterados, ainda que a classe apareça na tela e aceite digitação.

A alteração **não tem mensagem de confirmação**: a única confirmação da tela é a da
inclusão.

[?] A classe aparece na tela e passa por edição, mas o que for digitado nela não é
gravado: quem define a classe do gênero é a inclusão. Se a alteração deveria mudá-la
— e como se corrige a classe de um gênero já cadastrado — é pergunta ao site.

[?] Se a tela deveria confirmar a alteração como confirma a inclusão, ou se a
ausência da mensagem é a regra, é pergunta ao site.

### RN-07 — A exclusão exige o gênero cadastrado e não confere se ele está em uso

Para excluir, o gênero tem de existir — senão o sistema recusa com
**\* Genero nao cadastrado \***. Existindo, o gênero é excluído. A tela **não consulta
nenhum outro cadastro** antes de excluir: não confere se o gênero está sendo usado por
cardápio, estimativa ou qualquer outra tabela do módulo. A exclusão também não tem
mensagem de confirmação e não pergunta "confirma?" ao operador.

[?] O gênero é lido por outras telas do módulo, e a exclusão não verifica nenhum uso.
Se o banco impede a exclusão de um gênero em uso, ou se isso é aceito e as telas que o
leem passam a não achá-lo, é pergunta ao site.

### RN-08 — A consulta mostra o gênero cadastrado e não grava nada

Informando a consulta com a subclasse e o código do gênero, o sistema mostra os dados
do gênero — a classe, a descrição resumida, a unidade de compra, o padrão de conversão
e as três quantidades — e encerra a transação ali. Se o gênero não existir, a recusa é
**\* Genero nao cadastrado \***.

A consulta **não grava nada**: nenhum gênero é incluído, alterado ou excluído e
nenhuma trilha de auditoria é gerada por ela.

### RN-09 — Os campos numéricos passam por edição antes de qualquer conferência

Antes de conferir regra nenhuma, os campos numéricos da tela passam por edição:
**subclasse** (2 dígitos), **código do gênero** (5 dígitos), **classe** (4 dígitos),
**quantidade do gênero** e **unidade de conversão** (até 5 inteiros e 3 decimais) e
**menor quantidade a fracionar** (até 3 inteiros e 2 decimais). Campo em branco vira
**zero**; o que não for número é recusado e a transação não segue.

[?] Quando a digitação de um desses campos é recusada, o sistema posiciona o cursor de
volta no campo recusado apenas para alguns deles — a subclasse e a classe não têm
posição de cursor definida. Se o operador deveria ser levado de volta a esses dois
campos, é pergunta ao site.

### RN-10 — Antes de processar, o sistema confere o acesso à tela e a autorização da operação

Toda transação passa por duas conferências, com o contexto da sessão. Primeiro, o
acesso à tela: a tela tem de estar cadastrada no cadastro de telas — não estando, a
recusa é **\* Tela nao disponivel \*** — e a matrícula tem de ter a tela autorizada no
seu código de acesso — não tendo, a recusa é
**\* Acesso negado para esta matricula \***. Depois, a operação pretendida: a inclusão
exige a permissão de inclusão, a alteração a de alteração e a exclusão a de exclusão;
faltando, a recusa é **\* Acesso negado para esta operacao \*** e nada é gravado.

[?] A conferência da operação não procura a permissão de consulta: quem tem a tela
autorizada consulta sem precisar dela. Se a intenção era exigir a permissão de
consulta por tela, o caminho não a exige. Pergunta ao site.

### RN-11 — Toda inclusão, alteração e exclusão deixa trilha de auditoria

Além do gênero, cada inclusão, alteração e exclusão grava um registro de auditoria com
a tela de origem, o cadastro auditado, a operação (inclusão, alteração ou exclusão), o
**conteúdo anterior** e o **conteúdo posterior** do gênero, a matrícula do funcionário,
a estação, o número do processo (o código do gênero), a data e a hora da sessão, o tipo
de órgão e a coordenação regional escolar. Na inclusão o conteúdo anterior é vazio; na
exclusão, o conteúdo posterior é vazio.

[?] O registro de auditoria guarda a operação — inclusão, alteração ou exclusão — e,
além dela, um código de manutenção que sai com o mesmo valor nas três. Qual dos dois
campos diz a operação para quem lê a trilha é pergunta ao site; pelo que o acervo
mostra, o código de manutenção não distingue as três.

### RN-12 — Depois da operação a tela continua na própria tela

Depois de incluir, alterar, excluir ou consultar, a tela permanece na `C802T` e é
apresentada de novo ao operador — ela não abre outra tela. O que o operador pode
informar é o código de uma próxima tela, que a lógica de rota da sessão avalia; a tela
em si não encaminha para nenhuma outra.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os gêneros da alimentação escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C802T

  Cenário: Abertura da tela
    Quando abro a C802T pelo menu da alimentação escolar
    Então a tela já está no modo de inclusão
    E a mensagem da tela vem vazia
    E o código de subclasse vem com 99 e a classe do gênero com 9999

  Cenário: Chegando pela tela de consulta
    Dado que escolhi um gênero na tela de consulta C802C
    Quando chego à C802T
    Então vejo a descrição, a unidade de compra e as quantidades daquele gênero
    E a tela volta ao modo de inclusão
    E o código de subclasse volta a 99 e a classe a 9999, e não os do gênero consultado

  Cenário: Inclusão de um gênero novo
    Dado que a unidade de compra informada está cadastrada
    E o padrão de conversão é "g" ou "ml"
    E a unidade de conversão e a menor quantidade a fracionar são diferentes de zero
    Quando informo a subclasse, a classe, a descrição e os demais dados, em modo de inclusão
    Então o sistema atribui ao gênero o código seguinte ao último cadastrado naquela subclasse
    E grava o gênero
    E vejo a mensagem "* Genero cadastrado com sucesso *"
    E a operação fica registrada na auditoria

  Cenário: Primeiro gênero de uma subclasse
    Dado que não existe nenhum gênero cadastrado na subclasse informada
    Quando incluo o gênero
    Então o código atribuído é 1

  Cenário: Inclusão sem a descrição resumida
    Quando tento incluir um gênero sem preencher a descrição resumida
    Então vejo a mensagem "* Informe descricao resumida do genero *"
    E nada é gravado

  Cenário: Inclusão com unidade de compra não cadastrada
    Quando tento incluir um gênero com uma unidade de compra que não existe
    Então vejo a mensagem "* Unidade de compra nao cadastrada *"
    E nada é gravado

  Cenário: Inclusão com padrão de conversão diferente de g e de ml
    Quando tento incluir um gênero com outro padrão de conversão
    Então vejo a mensagem "* Informe padrao de conversao com g ou ml *"
    E nada é gravado

  Cenário: Inclusão com a unidade de conversão zerada
    Quando tento incluir um gênero com a unidade de conversão em zero
    Então vejo a mensagem "* Informe a unidade de conversao *"
    E nada é gravado

  Cenário: Inclusão com a menor quantidade a fracionar zerada
    Quando tento incluir um gênero com a menor quantidade a fracionar em zero
    Então vejo a mensagem "* Informe a menor quantidade a fracionar *"
    E nada é gravado

  Cenário: Alteração de um gênero cadastrado
    Dado que o gênero informado existe
    E a unidade de compra informada está cadastrada
    E o padrão de conversão é "g" ou "ml"
    E a unidade de conversão e a menor quantidade a fracionar são diferentes de zero
    Quando altero a descrição, a unidade de compra e as quantidades
    Então o sistema grava os novos valores
    E a operação fica registrada na auditoria

  Cenário: A classe do gênero não muda na alteração
    Dado que o gênero informado existe
    Quando informo outra classe do gênero e confirmo a alteração
    Então a classe gravada continua sendo a que o gênero tinha
    E o restante dos dados é gravado

  Cenário: Operação sobre gênero não cadastrado
    Dado que o par de subclasse e código de gênero informado não existe
    Quando tento alterar ou excluir
    Então vejo a mensagem "* Genero nao cadastrado *"
    E nada é gravado

  Cenário: Exclusão de um gênero cadastrado
    Dado que o gênero informado existe
    Quando informo a exclusão
    Então o sistema exclui o gênero
    E a operação fica registrada na auditoria, com o conteúdo que o gênero tinha

  Cenário: A exclusão não confere se o gênero está em uso
    Dado que o gênero é lido por outras telas do módulo
    Quando informo a exclusão
    Então o sistema exclui o gênero sem consultar nenhum outro cadastro
    E não me pede confirmação

  Cenário: Consulta de um gênero cadastrado
    Dado que o gênero informado existe
    Quando informo a consulta
    Então vejo a classe, a descrição resumida, a unidade de compra, o padrão de conversão e as quantidades
    E continuo na C802T

  Cenário: Consulta de gênero não cadastrado
    Dado que o par de subclasse e código de gênero informado não existe
    Quando informo a consulta
    Então vejo a mensagem "* Genero nao cadastrado *"

  Cenário: A consulta não grava nada
    Dado que o gênero informado existe
    Quando informo a consulta
    Então nenhum gênero é incluído, alterado ou excluído
    E nenhuma trilha de auditoria é gerada

  Cenário: Opção de manutenção desconhecida
    Quando informo uma opção que não é inclusão, alteração, exclusão nem consulta
    Então nenhuma operação é executada
    E nenhuma mensagem me é mostrada
    E nada é gravado

  Cenário: Digitação não numérica
    Dado que digito letras em um dos campos numéricos
    Quando confirmo a transação
    Então a transação não segue
    E nada é gravado

  Cenário: Tela não cadastrada
    Dado que a tela C802T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela C802T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Operação não autorizada
    Dado que o meu perfil não tem a permissão da operação pretendida
    Quando tento incluir, alterar ou excluir
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: A consulta não exige a permissão de consulta
    Dado que a minha matrícula tem a tela C802T autorizada
    E não tem a permissão de consulta registrada
    Quando informo a consulta de um gênero cadastrado
    Então o sistema mostra o gênero mesmo assim

  Cenário: Depois da operação a tela continua na tela
    Dado que acabei de incluir, alterar, excluir ou consultar
    Então continuo na C802T
    E nenhuma outra tela é aberta
```
