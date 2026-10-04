# US — C667T — Prorrogação de quantidade e valor da permissão de contrato da coordenação regional escolar

## Estória

Como **servidor da CRE que responde pela permissão de contrato**, quero **informar item por item
a quantidade a prorrogar e aplicar a prorrogação à permissão de contrato da minha coordenação
regional escolar**, para que **o contrato passe a autorizar a quantidade e o valor acrescidos, com
o rastro do que foi aplicado, sem que ninguém tenha de refazer o cálculo item por item**.

A permissão de contrato fixa o que cada item — uma classe, uma subclasse e um gênero — autoriza a
um fornecedor, dentro de um grupamento de licitação, de um período e de uma coordenação regional
escolar. Acontece de o quantitativo ser remanejado e de o aditivo ser assinado depois da permissão:
o que o contrato autoriza precisa crescer, e esse crescimento não pode ficar só na conta de quem
acompanha o contrato. Esta tela é onde o acréscimo por item é decidido, conferido contra o que o
item já tem e aplicado de uma só vez, deixando registrado o que acrescentou e sobre qual permissão.

## Contexto

Jornada S000M → C000M → C050M → C664M → C667T.
Ator: servidor de CRE — informa a coordenação regional escolar, o tipo de contrato, o fornecedor, o
grupamento de licitação e o período da permissão, ajusta a quantidade a prorrogar de cada item e
aplica a prorrogação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio. O menu que a abre não lhe passa dado nenhum: ela abre em consulta, com o que
ficou da última consulta daquela estação. O tipo de órgão, a coordenação regional, a matrícula, o
código de acesso, o privilégio, a data do sistema e a descrição do tipo de órgão chegam pela
sessão, deixados pela entrada.

**Esta tela grava**, e grava em vários cadastros: ela acrescenta o que foi prorrogado à permissão
de contrato, cria o registro da prorrogação, mantém o registro da prorrogação em elaboração — que
a própria consulta monta e que a tela apaga depois de aplicado —, apaga os registros de
transferência de quantidade que o item tenha, e cria o rastro na auditoria e no acompanhamento do
aditivo. A permissão de contrato e o registro da prorrogação ela não apaga em momento nenhum.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela aplica a prorrogação: acrescenta à permissão, cria o registro da prorrogação, apaga o registro de trabalho e deixa o rastro

Confirmada a alteração, o sistema percorre a prorrogação em elaboração daquela identificação e, para
cada item: acrescenta à permissão de contrato a quantidade e o valor prorrogados, cria um registro de
prorrogação preso ao limite inicial do período, cria o rastro na auditoria e no acompanhamento do
aditivo e **apaga o registro da prorrogação em elaboração** daquele item. Ao final, regrava o total
de prorrogação do contrato em todos os itens e o servidor vê **Cadastro Atualizado**.

A tela enxerga **doze** cadastros e o sistema traz prontas, para cada um deles, uma rotina de
gravação, uma de exclusão e uma de travamento. Nesta tela são executadas a gravação da permissão de
contrato (**dois** pontos), a gravação — na forma de criação — do registro da prorrogação
(**três** pontos), a gravação e a exclusão do registro da prorrogação em elaboração, a exclusão dos
registros de transferência de quantidade (**três** pontos), e a criação do rastro (**cinco** pontos
de auditoria e **dois** de acompanhamento do aditivo). Os outros cadastros que ela enxerga não são
gravados nem apagados em caminho nenhum. As capacidades são de dimensionamento, não de volume
cadastrado: a permissão de contrato comporta 1.000.000 de registros, os registros de transferência
1.000.000, o acompanhamento do aditivo 200.000, o acumulado do item 100.000, a auditoria
60.000.000, a prorrogação 30.000, os gêneros 150.000, os fornecedores 10.000, os títulos de tela
2.000, a liberação por tipo de licitação 1.000 e os tipos de órgão 200 — e o registro da prorrogação
em elaboração, 1.000, o menor de todos.

### RN-02 — A tela só atende à consulta, à alteração e à exclusão, e abre em consulta

O modo de manutenção admite três valores: **consulta**, **alteração** e **exclusão**. Qualquer
outro valor é recusado com **\* Opcao nao disponivel. Use ALT, EXC ou CON \***, com o cursor no
campo do modo, e nada é lido nem gravado. Abrindo sem modo informado, a tela assume sozinha a
consulta e se apresenta com o que ficou da última consulta daquela estação.

[?] A recusa manda usar ALT, EXC e CON, e a conferência compara o que chegou com o código interno
de cada modo. Se as duas palavras não forem as mesmas depois de o terminal traduzir o mnemônico, a
tela recusa justamente os três modos que ela aceita. Pergunta ao site.

### RN-03 — Nada é lido nem gravado sem a autorização de perfil, de rota e de operação

Antes de exibir, a tela passa pela rotina de segurança do perfil da sessão; antes de conferir,
passa pela rota do sistema e pela autorização por operação, levando o tipo de órgão, a coordenação
regional, a matrícula, o código de acesso, o privilégio e o modo; antes de cada gravação, passa pela
rotina de data e hora. Não voltando "OK" de qualquer uma delas, a transação é abandonada: nada é
lido, nada é gravado e nenhum rastro é criado.

[?] As três rotinas de segurança e a de data e hora só aparecem declaradas, sem corpo no material:
a regra efetiva de quem pode prorrogar nesta tela não pôde ser lida nesta jornada. Pergunta ao site.

### RN-04 — A tela só atende à coordenação regional da sessão

Quando a sessão do servidor tem uma coordenação regional, a coordenação informada tem de ser a
mesma; informando outra, a recusa é **\* Usuario sem acesso a este grupo \*** — a mensagem chama a
coordenação regional de **grupo** —, o cursor volta ao campo e nada é lido nem gravado. Quando a
sessão não tem coordenação regional, a tela não impõe essa restrição.

[?] A tela decide se impõe a restrição por uma área de sessão e compara a coordenação informada com
uma segunda área, alimentada por outro grupo de telas. Nesta jornada nenhuma das duas é carregada, e
o material não diz quem as preenche. Se a área da comparação chegar vazia, a tela recusa qualquer
coordenação informada. Pergunta ao site.

### RN-05 — A permissão é identificada pela coordenação regional, pelo tipo de contrato, pelo fornecedor, pelo grupamento de licitação e pelo limite do período

Para chegar à permissão e à sua prorrogação, o servidor informa a **coordenação regional escolar**,
o **tipo de contrato**, o **código do fornecedor**, o **grupo de licitação** e o **dia, o mês e o
ano do limite do período**; o **tipo de órgão vem da sessão** e é a primeira parte da identificação.
São **oito** os componentes da identificação, dos quais sete o servidor digita e um vem da sessão. A
tela procura com todos eles e deixa a classe, a subclasse e o gênero em zero, conferindo em seguida
apenas os componentes que o servidor informou.

[?] A busca da prorrogação em elaboração é montada com a classe, a subclasse e o gênero zerados,
embora a consulta crie esses registros com a classe, a subclasse e o gênero de cada item da
permissão. O material não documenta o que a leitura faz com os componentes zerados; se ela exigir
os três iguais a zero, a alteração e a exclusão nunca acham o que a consulta criou. Pergunta ao
site.

### RN-06 — A tela só está disponível para o tipo de licitação que a libera

Esta tela é liberada por tipo de licitação: o cadastro que diz quais telas valem para cada tipo de
licitação tem de ter o par formado pelo tipo de licitação da permissão e esta tela. Não tendo, a
recusa é **\* Tela nao disponivel para esta licitacao \***, com o cursor de volta na coordenação
regional, e nada é exibido nem gravado.

### RN-07 — A consulta monta o que falta da prorrogação em elaboração — e por isso grava

Na consulta, para cada item da permissão de contrato que **não** tenha prorrogação em elaboração, o
sistema **cria** o registro da prorrogação daquele item, com a quantidade prorrogada e o valor
prorrogado zerados; o que o item tem de quantidade inicial e de valor inicial é tomado do acumulado
do item quando ele existe. É essa criação que a alteração e a exclusão exigem depois. Os registros
de transferência de quantidade que o item tenha também são consumidos aqui: o que estiver marcado é
somado e o restante é apagado. **A consulta, portanto, não é inofensiva**: ela grava.

[?] O cadastro do registro da prorrogação em elaboração não tem nome de negócio no material, nem
comentário no dicionário; o menor de todos os cadastros da tela, criado só por esta tela e apagado
por ela depois de aplicado, é o que a leitura desta estória chama de prorrogação em elaboração.
Pergunta ao site pelo nome que o órgão usa.

[?] A consulta verifica se o item já tem prorrogação em elaboração pela mesma chave com a classe, a
subclasse e o gênero zerados, e a criação usa a classe, a subclasse e o gênero do item. Se a leitura
não tolerar os componentes zerados, a consulta criará um registro novo a cada passagem. Pergunta ao
site.

### RN-08 — Sem prorrogação em elaboração, nem a alteração nem a exclusão passam

A alteração e a exclusão exigem que exista prorrogação em elaboração para a identificação informada.
Não existindo, a recusa é **\* Prorrogacao nao cadastrada \*** e nada é gravado — na alteração o
cursor volta ao campo do modo, na exclusão também. É o que obriga o servidor a consultar antes de
alterar: quem consulta antes monta o que faltava. A apresentação também escreve **\* Permissao sem
registros para prorrogacao \*** quando a tela reabre com a identificação da consulta anterior e não
encontra mais a prorrogação em elaboração daquele item.

### RN-09 — A alteração e a exclusão exigem a consulta anterior dos mesmos dados

A alteração só é aceita para a identificação que a tela acabou de apresentar: se a coordenação
regional, o tipo de contrato, o grupo de licitação ou as três partes do limite do período informados
não forem os da última consulta registrada naquela estação, a recusa é **\* Consulte antes de
atualizar \***, com o cursor no campo do modo. A exclusão tem a mesma exigência, com a recusa
**\* Consulte antes de excluir \***. Em nenhuma das duas nada é lido além da conferência nem
gravado.

### RN-10 — A quantidade a prorrogar não pode passar o que o item tem

A quantidade que o servidor informa em cada linha é a quantidade a prorrogar daquele item. Ela é
conferida contra o que o item tem de quantidade inicial somada ao aditivo, item por item, e também
contra o total que a tela monta a partir do período da permissão. Passando, a recusa é
**\* Quant prorrogada > inicial+aditivo \***, com o cursor de volta na quantidade da linha, e nada é
gravado.

[?] A mesma recusa aparece em dois pontos com o mesmo texto — um na linha da grade e outro no
cálculo do período — e o material não diz se um deles é resto de gerador. Pergunta ao site.

### RN-11 — O valor da prorrogação é calculado pela própria tela

O servidor informa a quantidade; o valor não. O sistema multiplica a quantidade a prorrogar pelo
preço do item e, quando o item traz um percentual próprio, corrige antes o preço por esse percentual;
o resultado é o valor prorrogado daquela linha, que a tela grava junto com a quantidade. O valor que
o servidor digitar é substituído por esse cálculo.

[?] O material diz que o percentual corrige o preço, mas não diz se ele o aumenta ou o diminui, nem
por que a correção zera o preço quando o percentual não cabe na conta. Pergunta ao site.

### RN-12 — A alteração depende do campo de confirmação e do indicador de quantidade

A alteração não é aplicada só por ter passado nas conferências: ela exige que o campo de confirmação
da atualização venha marcado e que o indicador de quantidade **não** venha marcado, e é executada na
última passagem da grade. Sem a confirmação, a passagem apenas confere: a permissão, a prorrogação e
a auditoria ficam como estavam. A tela repõe o campo de confirmação como não marcado quando se
apresenta e quando recusa alguma coisa, e **nenhum caminho do sistema o marca**.

[?] Quem marca a confirmação é a estação de trabalho — o campo faz parte do registro da transação e
nenhum programa do acervo escreve nele a marca afirmativa. O acervo não tem a máscara da tela, e por
isso não se sabe se o campo é digitável pelo servidor. Se ele não puder ser marcado, a alteração
nunca é gravada e a tela fica só de consulta. Pergunta ao site.

[?] O que o indicador de quantidade significa em negócio não está no material: marcado, ele faz a
tela recusar a aplicação e apenas recalcular a prorrogação em elaboração a partir do cadastro; não
marcado, a tela aplica as quantidades que o servidor digitou. Ou o indicador é um modo de
recalculo, ou é resto de gerador. Pergunta ao site.

### RN-13 — Aplicada a alteração, o acréscimo entra na permissão e vira registro de prorrogação

Para cada item da prorrogação em elaboração, o acréscimo é somado à quantidade prorrogada e ao valor
prorrogado que a permissão de contrato já tinha, e a permissão é regravada. O mesmo acréscimo vira
um registro de prorrogação preso ao **limite inicial do período** da permissão: aproveitando o
registro existente quando ele está **sem quantidade**, e criando um registro novo quando já existe
prorrogação **com quantidade** para aquele limite inicial. Em qualquer dos casos o registro da
prorrogação em elaboração daquele item é apagado depois de aplicado.

### RN-14 — O total de prorrogação do contrato é recalculado e regravado em todos os itens

Terminada a aplicação, o sistema percorre os itens da permissão daquele contrato, soma os valores
prorrogados de todos eles e **regrava esse total em cada item**, com o rastro de antes e depois. O
que a linha a linha acrescentou não fica só na linha: o total de prorrogação do contrato é recomposto
e redistribuído.

### RN-15 — A exclusão apaga a prorrogação em elaboração e não toca na permissão

A exclusão percorre as prorrogações em elaboração daquela identificação e **apaga todas elas**, sem
pedir confirmação, e o servidor vê **Cadastro Excluido**. A permissão de contrato e o registro da
prorrogação **não** são apagados nem alterados, e nada é acrescentado a eles: a exclusão desfaz o
que a consulta tinha montado, não o que já foi aplicado.

### RN-16 — Toda gravação deixa rastro na auditoria e no acompanhamento do aditivo

Cada gravação cria o seu rastro: na auditoria, um registro por permissão de contrato regravada, por
prorrogação criada ou aproveitada e por item na regravação do total, sempre com a operação de
alteração, a imagem do registro **antes** e a **depois**, o objeto auditado e a matrícula, o órgão, a
coordenação regional, o terminal, a data e a hora da sessão e o número do processo; e, no
acompanhamento do aditivo, um registro por item aplicado e um por item na regravação do total. O
rastro é criado, nunca alterado nem apagado.

[?] O número do processo que o rastro guarda é o tipo de contrato, e o acompanhamento do aditivo
distingue os dois momentos por um código interno — um para a aplicação e outro para a regravação do
total — cujo significado o material não traz. Pergunta ao site.

### RN-17 — Nenhum campo é texto livre: vinte campos são conferidos como número e sete devolvem o cursor

Os **vinte** campos com rótulo — a coordenação regional, o tipo de contrato, o código do
fornecedor, o grupo de licitação, as três partes do início do período, as três do limite, o valor
adjudicado, o valor aditivo, o valor de prorrogação, e a subclasse, o gênero, a quantidade inicial, a
quantidade prorrogada, a nova quantidade e o valor prorrogado de cada linha — passam pela conferência
numérica, cada um com o tamanho que o dicionário declara. O campo em branco vira zero. O que não for
número é recusado, e a tela devolve o cursor a **sete** deles: a coordenação regional, o tipo de
contrato, o grupo de licitação, as três partes do limite e a nova quantidade da linha. Os treze
restantes são recusados sem posicionar o cursor.

[?] O texto da recusa por campo não numérico não está no fonte da tela: ele vem da rotina de edição,
que só aparece declarada no material. O que o operador lê nesse caso não pôde ser conferido.
Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Prorrogação de quantidade e valor da permissão de contrato da coordenação regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C667T

  Cenário: RN-05, RN-07 e RN-13 — consultar a permissão e aplicar a prorrogação de um item
    Dado que a permissão de contrato está cadastrada para a coordenação regional, o tipo de contrato, o fornecedor, o grupo de licitação e o limite do período que informei
    E que a tela está liberada para o tipo de licitação da permissão
    Quando consulto a permissão e informo a quantidade a prorrogar de um item
    E marco a confirmação da atualização
    Então o valor prorrogado da linha é calculado pela tela
    E a quantidade e o valor prorrogados são acrescentados à permissão daquele item
    E a prorrogação passa a existir presa ao limite inicial do período da permissão
    E vejo "Cadastro Atualizado"

  Cenário: RN-01, RN-13, RN-14 e RN-16 — o que a aplicação grava
    Dado que apliquei uma prorrogação na tela C667T
    Quando a gravação termina
    Então a permissão de contrato do item foi regravada com a quantidade e o valor acrescidos
    E o registro da prorrogação em elaboração daquele item foi apagado
    E o total de prorrogação do contrato foi regravado em todos os itens da permissão
    E existe rastro de auditoria de cada gravação, com a imagem de antes e a de depois
    E nenhuma permissão de contrato e nenhuma prorrogação foram apagadas

  Cenário: RN-07 — a consulta monta a prorrogação em elaboração e grava
    Dado que a permissão tem itens ainda sem prorrogação em elaboração
    Quando consulto a permissão
    Então a tela cria, para cada um desses itens, a prorrogação em elaboração com as quantidades zeradas
    E o que o item tem de quantidade e valor iniciais vem do acumulado do item
    E nenhum valor é acrescentado à permissão

  Cenário: RN-07 — a consulta consome os registros de transferência de quantidade
    Dado que um item da permissão tem registro de transferência de quantidade
    Quando consulto a permissão
    Então o que está marcado é somado ao que a tela mostra
    E o restante dos registros de transferência é apagado

  Cenário: RN-02 — modo de manutenção diferente de ALT, EXC e CON
    Dado que estou na tela C667T
    Quando informo um modo diferente de ALT, EXC e CON
    Então vejo "* Opcao nao disponivel. Use ALT, EXC ou CON *"
    E o cursor fica no campo do modo
    E nada é lido nem gravado

  Cenário: RN-02 — a tela abre em consulta
    Dado que abro a tela C667T pela opção do menu
    Então ela abre no modo de consulta, com o que ficou da última consulta daquela estação
    E nenhum cadastro é lido

  Cenário: RN-03 — sem a autorização de perfil, de rota ou de operação
    Dado que estou na tela C667T
    Quando a conferência de perfil, de rota ou de operação não retorna OK
    Então a tela volta sem ler e sem gravar
    E nenhum registro de auditoria é criado

  Cenário: RN-04 — coordenação regional fora da minha sessão
    Dado que o meu usuário está preso a uma coordenação regional
    Quando informo outra coordenação regional
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo da coordenação regional
    E nada é lido nem gravado

  Cenário: RN-06 — tela não liberada para o tipo de licitação
    Dado que o tipo de licitação da permissão não libera esta tela
    Quando consulto a permissão
    Então vejo "* Tela nao disponivel para esta licitacao *"
    E nada é exibido nem gravado

  Cenário: RN-08 — sem prorrogação em elaboração
    Dado que não existe prorrogação em elaboração para a identificação que informei
    Quando peço a alteração ou a exclusão
    Então vejo "* Prorrogacao nao cadastrada *"
    E nada é gravado

  Cenário: RN-08 — a tela reabre e a prorrogação em elaboração não existe mais
    Dado que a tela reabre com a identificação da consulta anterior e o item não tem prorrogação em elaboração
    Quando a tela se apresenta
    Então vejo "* Permissao sem registros para prorrogacao *"
    E nada é gravado

  Cenário: RN-09 — alteração sem a consulta anterior dos mesmos dados
    Dado que estou na tela C667T e informo uma coordenação regional, um tipo de contrato, um grupo de licitação ou um limite de período diferentes dos da última consulta
    Quando peço a alteração
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-09 — exclusão sem a consulta anterior dos mesmos dados
    Dado que estou na tela C667T e informo dados diferentes dos da última consulta
    Quando peço a exclusão
    Então vejo "* Consulte antes de excluir *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-10 — quantidade a prorrogar maior do que o item tem
    Dado que consultei uma permissão cujo item tem quantidade inicial somada ao aditivo
    Quando informo uma quantidade a prorrogar maior do que essa
    Então vejo "* Quant prorrogada > inicial+aditivo *"
    E o cursor fica na quantidade da linha
    E nada é gravado

  Cenário: RN-11 — o valor prorrogado é calculado pela tela
    Dado que consultei uma permissão e informei a quantidade a prorrogar de uma linha
    Quando a tela calcula o valor da linha
    Então o valor é a quantidade multiplicada pelo preço do item
    E, quando o item tem percentual próprio, o preço é corrigido antes por esse percentual
    E o valor que eu tiver digitado é substituído pelo cálculo

  Cenário: RN-12 — alteração sem o campo de confirmação marcado
    Dado que consultei a permissão e informei as quantidades a prorrogar
    Quando não marco a confirmação da atualização
    Então a passagem apenas confere
    E a permissão, a prorrogação e a auditoria ficam como estavam

  Cenário: RN-12 — alteração com o indicador de quantidade marcado
    Dado que consultei a permissão e informei as quantidades a prorrogar
    Quando marco o indicador de quantidade e a confirmação da atualização
    Então a tela recalcula a prorrogação em elaboração a partir do cadastro
    E não aplica à permissão as quantidades que digitei

  Cenário: RN-13 — a prorrogação aproveita o registro sem quantidade
    Dado que já existe prorrogação registrada para o limite inicial do período, sem quantidade
    Quando confirmo a alteração
    Então esse registro recebe a quantidade e o valor prorrogados
    E o registro da prorrogação em elaboração é apagado

  Cenário: RN-13 — a prorrogação cria um registro novo
    Dado que já existe prorrogação com quantidade para o limite inicial do período
    Quando confirmo a alteração
    Então é criado um registro novo de prorrogação para aquele limite inicial
    E a permissão recebe o acréscimo
    E o registro da prorrogação em elaboração é apagado

  Cenário: RN-15 — excluir a prorrogação em elaboração
    Dado que consultei uma permissão que tem prorrogação em elaboração
    Quando peço a exclusão
    Então a prorrogação em elaboração daquela identificação é apagada
    E vejo "Cadastro Excluido"
    E a permissão de contrato e a prorrogação continuam como estavam

  Cenário: RN-16 — toda gravação deixa rastro
    Dado que apliquei uma prorrogação na tela C667T
    Quando a gravação termina
    Então existe rastro de auditoria da permissão de contrato, da prorrogação e de cada item do total
    E cada um com a operação de alteração, a imagem do registro antes e a depois
    E com a matrícula, o órgão, a coordenação regional, o terminal, a data e a hora
    E existe rastro no acompanhamento do aditivo

  Cenário: RN-17 — campo não numérico
    Dado que estou na tela C667T
    Quando informo letras no campo do ano do limite do período
    Então a tela recusa a digitação e devolve o cursor ao campo
    E nada é gravado

  Cenário: RN-17 — campo não numérico sem retorno do cursor
    Dado que estou na tela C667T
    Quando informo letras no campo do início do período
    Então a tela recusa a digitação sem posicionar o cursor
    E nada é gravado
```
