# US — C662T — Troca de gramatura do item da permissão de fornecimento

## Estória

Como **servidor de CRE**, quero **registrar a troca do gênero — a gramatura — de um item já
autorizado em uma permissão de fornecimento da minha coordenação regional escolar**, para que
**o item passe a ser medido, entregue e pago na especificação que passou a valer, sem perder a
quantidade e o valor que já estavam autorizados**.

A permissão autoriza um fornecedor, dentro de um contrato de uma coordenação regional escolar, com
um grupo de licitação, um período e um item — classe, subclasse e gênero. A gramatura é o registro
da troca: é ela que leva a quantidade e o valor do gênero em uso para o gênero novo e que guarda o
preço de cada um, as datas das tabelas de preço e a situação da troca. Sem esse registro, o item
continuaria apontando para um gênero que já não se fornece, a conferência de preço do gênero novo
não teria onde acontecer e não haveria como saber, depois, que a especificação do item mudou.

## Contexto

Jornada S000M → C000M → C050M → C662T.

Ator: servidor de CRE — registra a troca de gramatura do item de uma permissão da sua coordenação
regional escolar, dentro da secretaria em que entrou.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

As duas telas antes do destino são menus, e nenhuma delas é tela de transação encadeada: a `C050M`
apenas nomeia a `C662T`, sem passar registro nem operação adiante. O que a `C662T` usa do que veio
antes é o **tipo de órgão** da secretaria escolhida no `LOGON` — ele entra na identificação de tudo
o que a tela lê e grava, e a tela não deixa digitá-lo —, além da **coordenação regional**, da
**matrícula**, do **código de acesso**, do **privilégio**, da **descrição do tipo de órgão** e da
**data do sistema** da sessão. Essas são regras da entrada e estão no anexo de evidências, em
**Regras que se revelaram da entrada**.

A jornada termina nesta tela: ela não encaminha para nenhuma outra — o que ela faz é se
reapresentar, com o resultado da consulta ou da alteração, na operação que estava em uso.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela registra a troca de gramatura do item da permissão

A tela trata de **um item de uma permissão de fornecimento**: o gênero que está autorizado e o
gênero pelo qual o item deve passar a ser fornecido. O registro da troca — a **gramatura** — guarda,
ao lado do gênero em uso, o **gênero novo**, as quantidades e os valores de cada um, o preço
unitário de cada gênero, as datas das tabelas de preço e uma marca de situação.

A tela enxerga **14 cadastros** e **lê 11** deles: o das telas do sistema, o do tipo de órgão, o da
gramatura do item, o dos gêneros, o do contrato, as **duas tabelas de preço**, o da permissão, o da
liberação da tela por tipo de licitação, o dos fornecedores e o do tipo de licitação. Os outros
três — a trilha de auditoria e os dois registros de acompanhamento da alteração — ela **não lê**:
só sabe criá-los. Para cada um dos 14 o gerador publica uma operação de gravar, uma de apagar e uma
de travar (14 de cada), mas **declarar não é executar**: por caminho alcançável a tela grava, apaga
e trava um único cadastro — o da gramatura do item. A permissão, os acompanhamentos da alteração e
a trilha de auditoria só são gravados pelo caminho que depende da confirmação (RN-13).

Os números de capacidade são de dimensionamento, não volume cadastrado: a permissão e a gramatura
do item comportam **1.000.000** de registros cada uma; os gêneros e uma das tabelas de preço,
**150.000**; os dois acompanhamentos da alteração, **200.000** e **100.000**; a auditoria,
**60.000.000**; os fornecedores e a outra tabela de preço, **10.000** cada; as telas do sistema,
**2.000**; o contrato, o tipo de licitação e a liberação da tela, **1.000** cada; o tipo de órgão,
**200**.

### RN-02 — O que identifica a permissão e o item

A permissão é identificada pela **coordenação regional escolar**, pelo **tipo de contrato** e pela
**data limite do período** — dia, mês e ano —, sempre dentro do **tipo de órgão** da sessão. O
**item**, dentro dela, pelo **grupo de licitação**, pela **classe**, pela **subclasse** e pelo
**gênero**. É por esses mesmos dados que se identifica a gramatura.

O tipo de órgão **não se digita**: é o da secretaria que o vínculo da matrícula escolheu na entrada
e ficou na sessão, e ele entra na identificação de tudo o que a tela lê e grava. O fornecedor, o
tipo de licitação, a data de início do período e as datas das tabelas de preço aparecem na tela e
podem ser informados, mas **não identificam** a gramatura: não fazem parte da sua identificação nem
das conferências que comparam o que está na tela com o registro consultado.

### RN-03 — Todo campo passa pela conferência numérica; o cursor volta para quinze deles

Antes de qualquer leitura, os **56 campos** da tela passam por uma conferência numérica: o que não
for número é recusado, e o campo não chega ao cadastro. **Vinte e um** deles têm rótulo de tela — a
coordenação regional escolar, o tipo de contrato, o código do fornecedor, o grupo de licitação, as
três partes do início do período, as três da data limite, o valor homologado, o valor adjudicado, o
apostilado por item, a classe, a subclasse, o gênero, a quantidade inicial da permissão, o valor
inicial do item, a quantidade inicial do aditivo, o valor inicial do aditivo e o valor comprado do
item; os outros **35** levam o próprio nome do campo como rótulo, o que faz crer que não aparecem
na máscara.

Quando a recusa é de um dos **quinze** campos com posição marcada — a coordenação regional, o tipo
de contrato, o grupo de licitação, as três partes da data limite, as três datas de vigência das
tabelas, a classe, a subclasse, o gênero e os três códigos do gênero novo —, o cursor volta ao
campo. Nos outros quarenta e um, a fonte não diz onde o cursor fica.

[?] A recusa de um campo que não é número é feita por uma rotina de edição do sistema, cujo texto de
mensagem não está no acervo desta jornada; e o retorno do cursor só é montado para quinze dos
cinquenta e seis campos, de modo que o servidor pode ser recusado sem que a tela aponte o campo. Não
concluo se os outros quarenta e um são recusáveis na prática ou se a volta do cursor ficou
incompleta. Pergunta ao site.

### RN-04 — A tela abre em consulta e depois na operação da última vez; só aceita ALT, DEL e CON

A tela só opera em **alteração**, **exclusão** e **consulta** — os mnemônicos que a mensagem nomeia
como **ALT**, **DEL** e **CON**. Na primeira vez na sessão ela abre em **consulta**; depois disso já
vem com a **operação da última vez**, guardada na sessão. Qualquer outra operação é recusada com
**\* Opcao nao disponivel. Use ALT, DEL ou CON \***, com o cursor de volta ao campo da operação, e
nada é lido nem gravado.

Um código de operação que o sistema não conhece é recusado **antes** disso, pelo roteamento, com
**\* Operacao nao disponivel \***.

[?] A correspondência entre os mnemônicos que a mensagem manda usar (ALT, DEL, CON) e as operações
internas que a tela compara é conclusão tirada do próprio texto da mensagem: o acervo desta jornada
não traz a máscara nem a rotina que traduz o que o terminal envia. Pergunta ao site.

### RN-05 — A consulta mostra o item, o gênero em uso e o gênero novo

Na consulta a tela apresenta o cabeçalho, o item e a gramatura. Do tipo de órgão da sessão vêm a
descrição e a data do sistema; do item da permissão vêm o fornecedor com a razão social, o tipo de
licitação com a sua descrição, as datas do período, as datas das tabelas, o valor homologado, o
valor adjudicado, o apostilado por item e o valor comprado; do cadastro de gêneros vêm a descrição
resumida e a quantidade de conversão do gênero em uso e do gênero novo. As quantidades e os valores
de cada gênero e os totais vêm do próprio registro da gramatura — e, quando ele está marcado como
**consolidado**, vêm do item da permissão, e a tela escreve no campo de situação
**Cad.Atualizado**.

Consulta que encontra a gramatura já registrada **não grava nada**.

### RN-06 — A consulta cria a gramatura do item quando ela ainda não existe

Se o item da permissão ainda **não tem** registro de gramatura, a consulta o **cria**: o preço
unitário sai do próprio item — o valor inicial dividido pela quantidade inicial — e o registro nasce
com as quantidades e os valores iniciais do item, sem gênero novo. Consultar, portanto, pode
gravar — mas só esse registro: a permissão não é alterada e a trilha de auditoria não recebe nada.

### RN-07 — A consulta exige a permissão e a liberação da tela para o tipo de licitação

Enquanto o registro da gramatura não existe, a consulta exige que a **permissão** daquele item
exista — senão recusa com **\* Permissao nao cadastrada \***, com o cursor de volta à coordenação
regional — e que a **tela esteja liberada para o tipo de licitação** daquela permissão — senão
recusa com **\* Tela nao disponivel para esta licitacao \***, com o cursor no mesmo campo. Quando o
registro da gramatura já existe, nenhuma das duas conferências é feita.

### RN-08 — Alteração e exclusão só andam no registro que a consulta deixou

A tela guarda na sessão o registro que a consulta mostrou. A alteração e a exclusão só seguem se a
**coordenação regional**, o **tipo de contrato**, o **grupo de licitação**, a **data limite do
período** e os **três códigos do item** forem exatamente os mesmos. Mudando qualquer um deles, a
operação é recusada — **\* Consulte antes para alterar a gramatura \***, na alteração, e
**\* Consulte antes para excluir o registro \***, na exclusão — com o cursor de volta ao campo da
operação, e nada é gravado. Quem atualiza o registro guardado é a consulta: a alteração e a exclusão
não o atualizam.

### RN-09 — A exclusão apaga a gramatura marcada como consolidada, e não deixa rastro

Para excluir, o registro da gramatura precisa **existir** — senão **\* Registro nao cadastrado \*** —
e estar marcado como **consolidado** — senão **\* Gramatura ja atualizada \***. Passando nas duas
conferências, a exclusão apaga o registro da gramatura: nada mais é apagado e nada é gravado na
trilha de auditoria — não fica registrado quem excluiu, quando, nem o que foi excluído.

[?] A recusa diz **\* Gramatura ja atualizada \*** justamente quando a gramatura **não** está marcada
como consolidada, e deixa passar a que está. Só o ramo que depende da confirmação (RN-13) escreve
essa marca, e a consulta cria a gramatura sem ela. Ou a marca vem de fora — a máscara da tela não
está no acervo —, ou a exclusão fica **inalcançável por este caminho**, porque o registro que a
própria consulta cria nunca passa na conferência. Não concluo qual dos dois. Pergunta ao site.

### RN-10 — A alteração exige um gênero novo válido

Para alterar, o registro da gramatura precisa existir — senão **\* Registro nao cadastrado \*** — e
estar marcado como consolidado — senão **\* Gramatura ja atualizada \***; os três códigos do
**gênero novo** têm de estar informados — senão **\* Informe o codigo do novo genero \***; e, se o
registro já aponta um gênero novo, ele não pode ser trocado por outro — senão **\* Codigo do novo
genero nao pode ser alterado \***.

O gênero novo tem ainda de existir e estar ativo no cadastro de gêneros (**\* Genero nao cadastrado
\***), ser do mesmo grupo de licitação do item (**\* Genero nao cadastrado neste grupamento \***),
ainda não estar na permissão (**\* Genero ja cadastrado nesta permissao \***) e ter preço cadastrado
(RN-11, **\* Genero sem preco cadastrado \***). Nenhuma dessas conferências grava.

### RN-11 — O preço do gênero novo sai da tabela que a configuração do contrato indica

A tela lê a **configuração do contrato** pelo tipo de órgão e pelo tipo de contrato; é essa
configuração que diz de qual das **duas tabelas de preço** sai o preço do gênero novo. A procura é
pelo gênero novo e por uma data: a **data de vigência da tabela**, quando ela está informada na
tela, e a **data-base da tabela**, quando não está.

Não achando preço — inclusive quando a configuração não indica nenhuma das duas tabelas —, a
alteração é recusada com **\* Genero sem preco cadastrado \***, com o cursor de volta aos códigos do
gênero novo, e nada é gravado.

### RN-12 — A troca converte a quantidade e o valor do gênero em uso para o gênero novo

A troca não é só a troca do código do gênero: as quantidades e os valores que estavam no gênero em
uso são levados para o gênero novo, **parcela a parcela** — a permissão inicial, o aditivo e a
prorrogação. A quantidade nova é a quantidade da parcela multiplicada pela quantidade de conversão
do gênero em uso e dividida pela quantidade de conversão do gênero novo; o valor novo é essa
quantidade multiplicada pelo preço do gênero novo. Quando esse valor fica **menor** do que o valor
que a parcela já tinha, a tela refaz a conta ao contrário: recalcula a quantidade dividindo o valor
antigo pelo preço do gênero novo, de modo que o item não perca valor na troca. Antes disso, o preço
do gênero novo é ajustado por um percentual que vem da permissão daquele item. Os totais e o valor
máximo que a tela mostra são as somas das três parcelas.

[?] O percentual que ajusta o preço do gênero novo vem da permissão do item (o preço entra
multiplicado pelo percentual dividido por cem, mais um), e o acervo desta jornada não diz de que
desconto ou acréscimo esse percentual trata. Pergunta ao site.

### RN-13 — A alteração que regrava a permissão depende de uma confirmação que a tela não escreve

A alteração que também **regrava a permissão** — reduzindo a quantidade e o valor do gênero em uso,
criando a linha do gênero novo na permissão, redistribuindo o valor pelas demais linhas do grupo,
gravando o acompanhamento do item e deixando o rastro na trilha de auditoria — depende de uma
**confirmação**. Sem ela, a tela confere tudo (RN-10 e RN-11) e, sendo o caminho alcançável, grava
apenas o **registro da gramatura** — o gênero novo, as quantidades e os valores convertidos e as
datas das tabelas — e **não** toca na permissão, no acompanhamento nem na auditoria.

Com a confirmação, a alteração exige ainda que o registro da gramatura **já traga** o gênero novo
(**\* Informe codigo do genero da nova gramatura \***) e uma quantidade do gênero novo
(**\* Informe quantidade do novo genero \***), e marca a gramatura como **consolidada**.

[?] A confirmação não é escrita em nenhum ponto deste programa — as duas únicas escritas nesse campo
são **N** e vazio —, e a própria tela repõe o campo em branco quando reapresenta o registro. Ou a
confirmação vem da máscara (que não está no acervo) e o ramo que regrava a permissão e deixa o
rastro é alcançável, ou esse ramo é **inalcançável por este caminho** e a alteração só grava a
gramatura. Não concluo qual dos dois. Pergunta ao site.

### RN-14 — Nada é lido nem gravado sem a conferência de acesso e de rota

Antes de qualquer leitura, a tela consulta o cadastro das telas do sistema e chama a conferência de
acesso à tela. Antes de validar e de gravar, passa pela **rota** e pela **conferência da operação**,
que recebem o contexto da sessão — matrícula, código de acesso, privilégio, tipo de órgão e
coordenação regional — e a operação informada. Recusando qualquer uma dessas conferências, a tela
termina sem ler nem gravar.

[?] A mensagem que o servidor vê quando a rota ou a conferência da operação recusam não é despachada
por esta tela; o texto que aparece na rota é **\* Operacao nao disponivel \***, mas quem o apresenta
é a rotina de comunicação, que não está no acervo desta jornada. Pergunta ao site.

### RN-15 — Chegando com a tela de retorno preenchida, a manutenção é abandonada

Se a transação chegar com a indicação de **tela de retorno** preenchida — o dado que a rota usa para
devolver o servidor a outra tela —, a manutenção é abandonada: nada é validado, nada é gravado e o
servidor é levado à tela indicada.

[?] Nada nesta jornada preenche essa indicação, e o acervo desta jornada não diz quem a preenche nem
para onde ela levaria. Pergunta ao site.

### RN-16 — Terminada a operação, a tela se reapresenta com o resultado

Terminada a consulta ou a alteração, a tela **se reapresenta**: na consulta, com o item e a
gramatura; na alteração, com a gramatura já trazendo o gênero novo e os valores convertidos. Ela
guarda na sessão a operação usada e os dados do registro, e é isso que faz a transação seguinte já
vir neles (RN-08). A **exclusão** é a única operação que não reapresenta a tela.

Esta tela não encaminha para nenhuma outra: a jornada termina nela.

---

## Cenários BDD

```gherkin
Funcionalidade: Troca de gramatura do item da permissão de fornecimento

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenação regional, a matrícula,
      o acesso e o privilégio
    E tenho acesso à tela C662T

  Cenário: A tela abre em consulta
    Dado que ainda não usei a tela C662T nesta sessão
    Quando a tela é apresentada
    Então ela abre em consulta

  Cenário: Operação diferente de ALT, DEL e CON é recusada
    Dado que estou na tela C662T
    Quando informo uma operação diferente de alteração, exclusão e consulta
    Então vejo "* Opcao nao disponivel. Use ALT, DEL ou CON *"
    E o cursor fica no campo da operação
    E nada é lido nem gravado

  Cenário: A tela reabre na operação da última vez
    Dado que usei a tela C662T em alteração nesta sessão
    Quando volto a abri-la
    Então ela vem com a operação de alteração

  Cenário: Consulta de um item que já tem gramatura não grava nada
    Dado que o item da permissão já tem gramatura registrada
    Quando informo a coordenação regional, o tipo de contrato, o grupo de licitação,
      a data limite do período e os três códigos do item, e consulto
    Então vejo o item da permissão, o gênero em uso, o gênero novo, os preços,
      as quantidades, os valores e os totais
    E vejo a descrição resumida de cada gênero e a sua quantidade de conversão
    E nada é gravado

  Cenário: A gramatura consolidada traz a situação Cad.Atualizado
    Dado que a gramatura do item está marcada como consolidada
    Quando consulto o item
    Então as quantidades e os valores mostrados são os do item da permissão
    E o campo de situação da gramatura mostra "Cad.Atualizado"

  Cenário: Consulta de um item que ainda não tem gramatura cria o registro
    Dado que o item da permissão não tem gramatura registrada
    Quando consulto o item
    Então o sistema cria a gramatura daquele item
    E o preço unitário sai do valor inicial dividido pela quantidade inicial do item
    E a gramatura nasce sem gênero novo
    E a permissão não é alterada e a auditoria não recebe nada

  Cenário: Consulta de item sem gramatura e sem permissão é recusada
    Dado que o item não tem gramatura registrada e não tem permissão
    Quando consulto
    Então vejo "* Permissao nao cadastrada *"
    E o cursor fica na coordenação regional
    E nada é gravado

  Cenário: Consulta recusada porque a tela não está liberada para o tipo de licitação
    Dado que o item ainda não tem gramatura registrada
    E a tela C662T não está liberada para o tipo de licitação daquela permissão
    Quando consulto
    Então vejo "* Tela nao disponivel para esta licitacao *"
    E o cursor fica na coordenação regional
    E nada é gravado

  Cenário: Alteração fora do registro que a consulta deixou é recusada
    Dado que informo uma coordenação regional, um contrato, um grupo, uma data limite
      ou códigos de item diferentes dos da última consulta
    Quando tento alterar
    Então vejo "* Consulte antes para alterar a gramatura *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: Exclusão fora do registro que a consulta deixou é recusada
    Dado que informo um registro diferente do da última consulta
    Quando tento excluir
    Então vejo "* Consulte antes para excluir o registro *"
    E o cursor fica no campo da operação
    E nada é apagado

  Cenário: Operação sobre gramatura não cadastrada é recusada
    Dado que os dados em tela são os da última consulta
    E a gramatura daquele item já não existe
    Quando tento alterar ou excluir
    Então vejo "* Registro nao cadastrado *"
    E nada é gravado

  Cenário: Alteração de gramatura não consolidada é recusada
    Dado que a gramatura do item existe e não está marcada como consolidada
    Quando tento alterar
    Então vejo "* Gramatura ja atualizada *"
    E nada é gravado

  Cenário: Exclusão de gramatura não consolidada é recusada
    Dado que a gramatura do item existe e não está marcada como consolidada
    Quando tento excluir
    Então vejo "* Gramatura ja atualizada *"
    E a gramatura continua registrada

  Cenário: Exclusão de gramatura consolidada apaga o registro e não deixa rastro
    Dado que a gramatura do item está consolidada
    E o registro é o da última consulta
    Quando excluo
    Então a gramatura daquele item é apagada
    E o item da permissão continua como estava
    E nada é gravado na auditoria

  Cenário: Alteração sem o gênero novo informado é recusada
    Dado que a gramatura do item existe e está consolidada
    Quando confirmo a alteração sem informar os códigos do gênero novo
    Então vejo "* Informe o codigo do novo genero *"
    E o cursor fica nos códigos do gênero novo
    E nada é gravado

  Cenário: Troca do gênero novo já definido é recusada
    Dado que a gramatura do item já aponta um gênero novo
    Quando informo um gênero novo diferente daquele
    Então vejo "* Codigo do novo genero nao pode ser alterado *"
    E nada é gravado

  Cenário: Gênero novo inexistente ou inativo é recusado
    Dado que o gênero novo informado não existe no cadastro de gêneros, ou não está ativo
    Quando tento alterar
    Então vejo "* Genero nao cadastrado *"
    E nada é gravado

  Cenário: Gênero novo de outro grupamento é recusado
    Dado que o gênero novo informado pertence a outro grupo de licitação
    Quando tento alterar
    Então vejo "* Genero nao cadastrado neste grupamento *"
    E nada é gravado

  Cenário: Gênero novo que já está na permissão é recusado
    Dado que o gênero novo informado já está autorizado naquela permissão
    Quando tento alterar
    Então vejo "* Genero ja cadastrado nesta permissao *"
    E nada é gravado

  Cenário: Gênero novo sem preço cadastrado é recusado
    Dado que a configuração do contrato indica uma das tabelas de preço
    E o gênero novo não tem preço cadastrado naquela tabela
    Quando tento alterar
    Então vejo "* Genero sem preco cadastrado *"
    E nada é gravado

  Cenário: A alteração leva a quantidade e o valor do gênero em uso para o gênero novo
    Dado que a gramatura do item está consolidada
    E o gênero novo tem preço cadastrado e ainda não está na permissão
    Quando informo os códigos do gênero novo e confirmo a alteração
    Então a quantidade do gênero novo é a do gênero em uso convertida entre as gramaturas
    E o valor do gênero novo sai dessa quantidade pelo preço do gênero novo
    E o item não perde valor na troca
    E o gênero novo, as quantidades e os valores ficam gravados na gramatura
    E a permissão não é regravada por este caminho

  Cenário: A operação não autorizada pelo perfil não lê nem grava
    Dado que o meu perfil não tem a operação pretendida na tela C662T
    Quando tento consultar, alterar ou excluir
    Então o sistema recusa a operação
    E nada é lido nem gravado

  Cenário: A tela de retorno preenchida abandona a manutenção
    Dado que a transação chega à C662T com a indicação de tela de retorno preenchida
    Quando a manutenção começaria
    Então o processamento é abandonado e nada é gravado
    E o servidor é levado à tela indicada

  Cenário: Campo que não é número é recusado com o cursor de volta
    Dado que estou na tela C662T
    Quando informo, na coordenação regional ou nos códigos do item, algo que não é número
    Então o sistema recusa o campo antes de qualquer leitura
    E o cursor volta ao campo
```
