# US — C050T — Manter os gêneros de compra e o início de vigência de cada versão

## Estória

Como **servidor da CRE que mantém o catálogo de gêneros de compra**, quero **incluir,
alterar, excluir e consultar os gêneros de compra e a data de início de cada versão
deles**, para que **as rotinas de compra do sistema encontrem o gênero certo, com a
descrição, a unidade e as quantidades de conversão que valem na data certa**.

O gênero é a categoria de compra a que os itens e as quantidades se referem, e é este
cadastro que **93 programas de tela do sistema leem** para saber o que estão comprando.
Por isso a tela não sobrescreve o que está gravado: cada mudança entra como uma **versão
nova**, com data de início, e o que existia continua na base. É também aqui, e só aqui,
que o gênero é marcado como **orgânico** — a marca que cria o relacionamento que a tela
C054T mantém. Sem esta tela o catálogo não evolui; com ela errada, o erro aparece em tudo
o que consulta o gênero depois.

## Contexto

Jornada S000M → C000M → C055M → C050T.
Ator: servidor de CRE — mantém, para a sua secretaria, os gêneros de compra e a data de
início de cada versão deles.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US — 00
Entrada (LOGON, S000M).md`. O caminho até a tela — a opção 6 do `C000M` abre o menu
`C055M`, e a opção 2 dele abre esta tela — está em `Documents/jornadas/00 Navegação e
menus.md`: é **dado de navegação**, não regra de negócio.

Os dois menus do caminho não gravam nada: só encaminham. O que esta tela usa do que veio
antes é o **vínculo da matrícula com a secretaria** — que fixa a CRE e o tipo de órgão da
sessão — e a **data do sistema**; essas são regras da entrada e estão no anexo de
evidências, em **Regras que se revelaram da entrada**.

Esta tela também é alcançada pela consulta `C240C`, que passa para ela o gênero que
estava sendo consultado; por isso o que a tela abre conforme quem a chamou é regra
própria (RN-16). A jornada termina nesta tela: ela não encaminha para outra do cadastro —
ela **reabre a si mesma** (RN-17).

## Regras de negócio

### RN-01 — O que a tela mantém, e o que ela grava

A tela mantém o **gênero de compra**, identificado pela **classe**, pela **subclasse**,
pelo **código do gênero** e pela **data de início de cada versão** — dia, mês e ano —,
junto com as **quatro linhas da descrição**, a **descrição resumida**, o **grupo de
licitação**, a **unidade de compra**, o **padrão de conversão**, a **unidade de
conversão**, a **quantidade do gênero**, as **duas quantidades mínimas a fracionar** (a
de pedidos e a de nota fiscal), a marca de **orgânico** e a marca de **ativo**. São
**22 campos** informados, fora as seis datas de início das versões e as descrições de
orgânico e ativo que a tela devolve — a contagem está no anexo.

A tela grava no **cadastro de gêneros** e no **cadastro do relacionamento dos gêneros
orgânicos**, e deixa rastro na **trilha de auditoria** (RN-18). **Nada é apagado**: a
exclusão deixa a versão na base, marcada como excluída e inativa (RN-15). A versão
**incluída nasce ativa**, independentemente do que estiver no indicador de ativo na tela.

### RN-02 — A tela abre em consulta, e a operação informada decide o resto

Ao abrir — pelo menu ou pela consulta `C240C` —, a tela vem com o campo de operação
preenchido com a **consulta**: ela abre lendo, não gravando. Quem decide o que acontece
é a operação que o servidor informa: **INC** inclui, **ALT** altera, **EXC** exclui e
**CON** consulta. Operação diferente dessas quatro é recusada com **\* Opcao nao
disponivel. Use INC, ALT, EXC ou CON \***, com o cursor de volta no campo, e nada é
gravado.

A operação informada ainda passa pela permissão do servidor (RN-19): sem a marca daquela
operação no cadastro de acesso, a recusa é **\* Acesso negado para esta operacao \***.

[?] A recusa fala em INC, ALT, EXC e CON, mas o que o programa compara são os códigos
internos de inclusão, alteração, exclusão e consulta. Ou o terminal traduz o que o
servidor digita, ou a mensagem está desalinhada da comparação. Pergunta ao site.

### RN-03 — A consulta não grava nada

Em **consulta**, a tela procura a versão do gênero pela **subclasse**, pelo **código do
gênero** e pela **data de início** informada. Achando, mostra os dados daquela versão —
classe, grupo de licitação, descrição e descrição resumida, unidade de compra, padrão e
unidade de conversão, quantidade do gênero, quantidades mínimas a fracionar, orgânico e
ativo — e reabre a si mesma com eles. Não achando, avisa **\* Genero nao cadastrado \***,
com o cursor de volta no campo.

Não informada a data (dia, mês ou ano em branco), a consulta não busca uma versão: ela
lista o gênero pela subclasse e pelo código do gênero e mostra **até seis datas de
início** das versões daquele gênero; não existindo nenhuma, avisa **\* Genero nao
cadastrado \***. Em qualquer dos casos, a consulta **não grava nada**, não trava registro
e não deixa rastro na auditoria.

[?] A tela recolhe até seis datas de início para mostrar as versões do gênero. Qual
versão tem os dados que a consulta exibe quando o gênero tem mais de uma, e o que
acontece quando ele tem mais de seis versões, não se lê no acervo: o efeito dos
posicionamentos de leitura não está documentado nele. Pergunta ao site.

### RN-04 — Os três códigos são obrigatórios, e a classe começa por 89

Na inclusão, os três códigos que identificam o gênero têm de ser informados: faltando a
**classe**, a recusa é **\* Informe a Classe \***; faltando a **subclasse**, **\* Informe
a SubClasse \***; faltando o **código do gênero**, **\* Informe o Genero \***.

E a **classe** tem de começar pelos dígitos **89** — o prefixo com que o sistema
identifica um gênero —, senão a recusa é **\* Informe inicio 89 na CLASSE para generos
\***. As três conferências e a do prefixo têm o cursor de volta no campo recusado, e nada
é gravado.

### RN-05 — A inclusão busca o gênero no SIGMA e só grava na confirmação

Informada a inclusão, a tela **não grava direto**: ela vai ao **SIGMA** — o cadastro
corporativo de onde saem a descrição, a descrição resumida e a unidade de compra do
gênero —, traz de lá esses dados e **reabre a si mesma** com eles preenchidos, para o
servidor conferir e completar o resto. **Só a confirmação grava**: a primeira passagem
nunca grava.

Falhando a ida ao SIGMA, a inclusão para e avisa: sem acesso à base, **\* Banco SIGMA sem
acesso \***; com problema no acesso, **\* Problemas no acesso ao SIGMA \***; código que
não existe lá, **\* Genero nao cadastrado \***; código desativado lá, **\* Codigo de
genero desativado \***.

### RN-06 — A inclusão recusa a versão já cadastrada e o gênero que já tem versão ativa

Antes de ir ao SIGMA, a inclusão confere o cadastro. Existindo versão daquele gênero com
**a mesma data de início** informada, a recusa é **\* Genero ja cadastrado \***. E
existindo versão **ativa** daquele gênero, a inclusão é recusada com **\* <- Codigo ja
ativo nesta data \***, com o cursor de volta no campo da operação.

[?] A segunda conferência compara a data informada com a data da versão ativa, mas a
comparação usa um valor que só é preenchido depois, na passagem seguinte — a do SIGMA.
Na passagem em que ela decide, esse valor está vazio, de modo que a recusa acontece
qualquer que seja a data informada: um gênero que já tem versão ativa não aceita versão
nova por este caminho. Ou a conferência vale para outro caso, ou o caminho ficou
inalcançável. Pergunta ao site.

### RN-07 — Depois de incluir, a tela inativa as versões anteriores do gênero

Gravada a versão incluída, o mesmo caminho relê as versões daquele gênero — começando
pela data de um dia antes da data informada — e marca cada uma que encontra como
**inativa**, para que o gênero fique com **uma única versão ativa**.

[?] A releitura é feita em laço, e o acervo não permite concluir quais versões ele
alcança, nem se a versão recém-incluída pode ser atingida por ele — o que a deixaria
inativa logo depois de gravada. O efeito dos posicionamentos de leitura não está
documentado no acervo. Pergunta ao site.

### RN-08 — A data de início tem de ser uma data válida

A data de início da versão passa pela conferência de data do sistema e tem de ter **ano
entre 1994 e 2099**. Data que não existe no calendário, ou ano fora dessa faixa, é
recusada com **\* Data de inicio invalida \***, com o cursor de volta no campo, e nada é
gravado.

### RN-09 — O grupo de licitação é obrigatório e tem de ter vigência

O **grupo de licitação** tem de ser informado — senão **\* Informe grupo da licitacao
\*** — e tem de estar cadastrado, no cadastro dos grupamentos, com **vigência para a data
de início informada**; não estando, a recusa é **\* Grupo de licitacao nao cadastrado \***.
Nada é gravado.

### RN-10 — As descrições do gênero são obrigatórias

A **descrição resumida do gênero** — a que vem do SIGMA — tem de estar preenchida, senão
**\* Informe descricao resumida do genero \***; e a **primeira linha da descrição do
gênero** também, senão **\* Informe a descricao do genero \***. As outras três linhas da
descrição não são conferidas. Nada é gravado.

### RN-11 — A unidade de compra e a conversão de quantidades

A **unidade de compra** tem de estar cadastrada no cadastro das unidades de compra,
senão **\* Unidade de compra nao cadastrada \***. O **padrão de conversão** só admite
**g** ou **ml**, senão **\* Informe padrao de conversao com g ou ml \***. A **unidade de
conversão** tem de ser diferente de zero, senão **\* Informe a unidade de conversao \***.
E as duas **quantidades mínimas a fracionar** também: a de pedidos, senão **\* Informe
menor qt a fracionar - pedidos \***; a de nota fiscal, senão **\* Informe menor qt a
fracionar - NF \***. Nada é gravado.

### RN-12 — A marca de orgânico cria ou retira o relacionamento do gênero

O indicador de **orgânico** só admite **S** ou **N**; qualquer outra coisa é recusada com
**\* Informe se organico com S ou N \***. Marcar um gênero como orgânico **cria** o
registro do relacionamento dele — o que a tela C054T passa a manter —, tanto na inclusão
quanto na alteração; desmarcar, na alteração, **retira** esse registro. É essa marca que
decide se a exclusão do gênero depende do relacionamento (RN-14).

### RN-13 — A alteração exige consulta antes, mantém o grupo e confere o ativo

Para alterar, o servidor tem de ter **consultado antes** nesta tela, e a tela tem de
estar com a **mesma classe, subclasse, código do gênero e data de início** que a consulta
deixou; fora disso, a recusa é **\* Consulte o genero antes de alterar \***. A data
informada ainda tem de ser a da versão que a tela relê para aquele gênero: sendo outra, a
recusa é **\* Genero desativado para esta data \***. E o **grupo de licitação não pode ser
trocado** na alteração — trocado, **\* Nao altere grupo da licitacao \***.

A alteração refaz, uma a uma, as mesmas conferências da inclusão — descrição resumida,
primeira linha da descrição, unidade de compra, padrão de conversão, unidade de conversão,
as duas quantidades mínimas a fracionar e o orgânico — com as mesmas mensagens de recusa
(RN-10, RN-11 e RN-12). Acrescenta a conferência do indicador de **ativo**, que só admite
**S** ou **N**: **\* Informe ativo com S ou N \***. Nenhuma dessas recusas grava.

[?] A tela relê a versão posicionando a leitura pelo maior valor da subclasse e do código
do gênero. Se isso devolve a última versão ou a primeira não está no acervo, e é disso
que depende poder alterar uma versão que não seja a mais recente. Pergunta ao site.

### RN-14 — A exclusão exige consulta antes, e o relacionamento a barra

Para excluir vale a mesma exigência da alteração: tem de haver **consulta antes** e a
chave na tela tem de ser a mesma que ela deixou — senão **\* Consulte o genero antes de
excluir \***. E um gênero **orgânico que já tem relacionamento com outro gênero** não pode
ser excluído: a recusa manda excluir antes o relacionamento do gênero. Nada é gravado.

### RN-15 — A exclusão não apaga a versão: marca como excluída e inativa

A exclusão confirmada **não apaga** o registro: grava a versão com a marca de **excluída**
e com o indicador de ativo em **N**. A versão sai das consultas — o cadastro deixa de
mostrá-la — e continua na base. Se o gênero era orgânico e tinha o relacionamento
registrado, a exclusão **retira** esse relacionamento, com rastro próprio na auditoria.

[?] Como a versão excluída sai do conjunto que a tela consulta, a conferência de "gênero
já cadastrado" (RN-06) deixa de enxergá-la. Não está no acervo se dá para incluir de novo
uma versão com a mesma data de início, nem se a chave da data continua ocupada. Pergunta
ao site.

### RN-16 — A tela abre diferente conforme quem a chamou

Esta tela é aberta pela opção 2 do menu `C055M` e pela consulta `C240C`. Vindo do
**menu**, ela abre **em branco**, em consulta, e o servidor informa tudo. Vindo da
**consulta `C240C`**, ela toma do chamador a operação, a subclasse e o código do gênero e
**abre já posicionada naquele gênero**: existindo versão, carrega os dados dela e até seis
datas de início das versões, sem que o servidor precise informá-los.

A carga acontece **só na abertura**: assim que a tela se apresenta, ela esquece a tela de
origem, de modo que a volta da tela não recarrega nada. E nos dois casos a operação com
que ela abre é a **consulta** (RN-02): o que a origem muda é o que vem preenchido, não o
modo de abrir.

[?] A consulta `C240C` deixa o gênero na área de trabalho que a sessão passa de uma tela
para a outra, mas a área que ela grava tem, antes da classe, o grupamento de licitação e a
descrição dele, enquanto esta tela lê a subclasse e o código do gênero logo depois da
operação. O acervo não diz se o sistema reposiciona esses valores na passagem: se não
reposicionar, o que esta tela recebe no lugar do gênero vem do grupamento. Pergunta ao
site.

### RN-17 — O que a tela entrega à seguinte: ela reabre a si mesma

A tela **não encaminha para outra do cadastro**: ela reabre a si mesma, e é reabrindo que
entrega o que apurou — a **classe, a subclasse, o código do gênero e a data de início** e
a **operação**, além da **marca de que a passagem é a segunda**. É essa marca que separa a
passagem que confere da passagem que grava: a inclusão **só grava na segunda passagem**
(RN-05). A reabertura acontece depois de buscar o gênero no SIGMA, depois de uma consulta
que achou o gênero e depois de montar a lista de datas.

A tela também carrega o campo da **próxima tela**: se ele vier preenchido, a rotina comum
de encaminhamento leva a ele em vez de manter esta tela aberta.

[?] O acervo não diz quem preenche o campo da próxima tela — se o servidor, se o
encaminhamento que trouxe a tela até aqui. Só diz que, preenchido, ele desvia. Pergunta ao
site.

### RN-18 — Toda gravação deixa registro na trilha de auditoria

Inclusão, alteração e exclusão — e também a criação e a retirada do relacionamento do
gênero orgânico — deixam, cada uma, um registro na **trilha de auditoria**: a tela de
origem, o cadastro alterado, a operação, o gênero, a matrícula, a estação, o tipo de órgão,
a data e a hora da sessão, e as imagens **anterior** e **posterior** do registro. A trilha
é gravada **antes** do cadastro.

[?] Como a trilha é gravada antes do cadastro, uma falha na gravação do cadastro deixa na
trilha uma operação que não chegou a acontecer. Pergunta ao site.

### RN-19 — Antes de operar, a tela confere o perfil, a rota e a permissão da operação

Antes de deixar operar, a tela chama as rotinas comuns de **perfil da tela**, **rota** e
**permissão por operação**. A permissão é lida do **cadastro de acesso** por código de
acesso, tela e tipo, e o cadastro guarda uma marca por operação — incluir, alterar,
excluir e consultar. A tela exige a marca da operação informada; a **consulta** é a única
que ela não exige, embora exija o registro de acesso da tela. Sem o registro de acesso
para aquela tela, a recusa é **\* Acesso negado para esta matricula \***; com o registro,
mas sem a marca da operação informada, a recusa é **\* Acesso negado para esta operacao
\***. Sem matrícula na sessão, a tela devolve ao `LOGON`. Retorno diferente de OK limpa o
status e a tela não opera.

### RN-20 — Falha no banco é avisada pela rotina do sistema

Erro de leitura do cadastro e erro de gravação são despachados para a rotina de
comunicação do sistema, com o código do erro correspondente. Quem decide o que o servidor
vê, e se a transação continua, é essa rotina.

[?] A rotina de comunicação do sistema não está no acervo: as telas apenas a chamam,
passando o código do erro. O que ela faz com o erro — avisa, interrompe ou deixa seguir —
não está no corpus. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manter os gêneros de compra e o início de vigência de cada versão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C050T

  Cenário: RN-01, RN-03 e RN-18 — consultar um gênero cadastrado
    Dado que o gênero está cadastrado
    Quando informo CON com a subclasse, o código do gênero e a data de início
    Então vejo a classe, o grupo de licitação, a descrição, a descrição resumida, a unidade de compra, a conversão e as quantidades
    E vejo o indicador de orgânico e o de ativo
    E nada é gravado e nenhum rastro de auditoria é deixado

  Cenário: RN-03 — consultar um gênero sem informar a data
    Dado que o gênero tem versões cadastradas
    Quando informo CON com a subclasse e o código do gênero e deixo a data em branco
    Então vejo as versões daquele gênero por até seis datas de início
    E nada é gravado

  Cenário: RN-03 — gênero não cadastrado na consulta
    Dado que não existe versão para a subclasse e o código do gênero informados
    Quando informo CON
    Então vejo "* Genero nao cadastrado *"
    E o cursor volta para o campo da subclasse
    E nada é gravado

  Cenário: RN-02 — operação diferente de INC, ALT, EXC e CON
    Dado que estou na tela C050T
    Quando informo uma operação diferente dessas quatro
    Então vejo "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E o cursor volta para o campo da operação
    E nada é gravado

  Cenário: RN-04 — a classe não foi informada
    Dado que estou na tela C050T e informo INC
    Quando deixo a classe em branco
    Então vejo "* Informe a Classe *"
    E o cursor volta para o campo da classe
    E nada é gravado

  Cenário: RN-04 — a subclasse não foi informada
    Dado que estou na tela C050T e informo INC com a classe preenchida
    Quando deixo a subclasse em branco
    Então vejo "* Informe a SubClasse *"
    E nada é gravado

  Cenário: RN-04 — o código do gênero não foi informado
    Dado que estou na tela C050T e informo INC com a classe e a subclasse preenchidas
    Quando deixo o código do gênero em branco
    Então vejo "* Informe o Genero *"
    E nada é gravado

  Cenário: RN-04 — a classe não começa por 89
    Dado que estou na tela C050T e informo INC
    Quando informo uma classe que não começa por 89
    Então vejo "* Informe inicio 89 na CLASSE para generos *"
    E nada é gravado

  Cenário: RN-05, RN-17 e RN-18 — incluir um gênero cadastrado no SIGMA
    Dado que o código existe no SIGMA e está ativo lá
    Quando informo INC com a classe começando por 89, a subclasse e o código do gênero
    Então a tela reabre já com a descrição, a descrição resumida e a unidade de compra vindas do SIGMA
    E ainda nada foi gravado
    Quando completo o grupo de licitação, a conversão, as quantidades e o orgânico e confirmo
    Então a versão fica gravada no cadastro de gêneros, ativa
    E a operação fica registrada na trilha de auditoria

  Cenário: RN-05 — o SIGMA está sem acesso
    Dado que a base do SIGMA está inacessível
    Quando informo INC com a classe, a subclasse e o código do gênero
    Então vejo "* Banco SIGMA sem acesso *"
    E nada é gravado

  Cenário: RN-05 — problemas no acesso ao SIGMA
    Dado que o acesso ao SIGMA responde com problema
    Quando informo INC com a classe, a subclasse e o código do gênero
    Então vejo "* Problemas no acesso ao SIGMA *"
    E nada é gravado

  Cenário: RN-05 — gênero não cadastrado no SIGMA
    Dado que o código do gênero não existe no SIGMA
    Quando informo INC com a classe, a subclasse e o código do gênero
    Então vejo "* Genero nao cadastrado *"
    E nada é gravado

  Cenário: RN-05 — código de gênero desativado no SIGMA
    Dado que o código do gênero existe no SIGMA e está desativado lá
    Quando informo INC com a classe, a subclasse e o código do gênero
    Então vejo "* Codigo de genero desativado *"
    E nada é gravado

  Cenário: RN-06 — versão com a mesma data de início já cadastrada
    Dado que já existe versão daquele gênero com a data de início informada
    Quando informo INC com a classe, a subclasse, o código do gênero e essa data
    Então vejo "* Genero ja cadastrado *"
    E nada é gravado

  Cenário: RN-06 — gênero que já tem versão ativa
    Dado que o gênero tem uma versão ativa
    Quando informo INC com a classe, a subclasse, o código do gênero e uma data de início
    Então vejo "* <- Codigo ja ativo nesta data *"
    E nada é gravado

  Cenário: RN-07 — incluir uma versão nova de um gênero que já tinha versão
    Dado que o gênero já tinha uma versão ativa
    Quando confirmo a inclusão de uma versão com data posterior
    Então a versão nova fica gravada e ativa
    E as versões anteriores daquele gênero ficam inativas

  Cenário: RN-08 — data de início inválida
    Dado que estou na tela C050T e informo INC
    Quando informo uma data de início que não existe no calendário, ou um ano fora de 1994 a 2099
    Então vejo "* Data de inicio invalida *"
    E o cursor volta para o campo da data
    E nada é gravado

  Cenário: RN-09 — o grupo de licitação não foi informado
    Dado que a tela já trouxe o gênero do SIGMA
    Quando deixo o grupo de licitação em branco e confirmo
    Então vejo "* Informe grupo da licitacao *"
    E nada é gravado

  Cenário: RN-09 — grupo de licitação sem vigência na data informada
    Dado que o grupo de licitação não tem vigência cadastrada para a data de início informada
    Quando confirmo a inclusão com esse grupo
    Então vejo "* Grupo de licitacao nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — descrição resumida do gênero não informada
    Dado que a descrição resumida do gênero está em branco
    Quando confirmo a inclusão
    Então vejo "* Informe descricao resumida do genero *"
    E nada é gravado

  Cenário: RN-10 — primeira linha da descrição do gênero não informada
    Dado que a primeira linha da descrição do gênero está em branco
    Quando confirmo a inclusão
    Então vejo "* Informe a descricao do genero *"
    E nada é gravado

  Cenário: RN-11 — unidade de compra não cadastrada
    Dado que a unidade de compra informada não está no cadastro das unidades
    Quando confirmo a inclusão
    Então vejo "* Unidade de compra nao cadastrada *"
    E nada é gravado

  Cenário: RN-11 — padrão de conversão diferente de g e de ml
    Dado que estou completando a inclusão
    Quando informo um padrão de conversão diferente de g e de ml
    Então vejo "* Informe padrao de conversao com g ou ml *"
    E nada é gravado

  Cenário: RN-11 — unidade de conversão não informada
    Dado que estou completando a inclusão
    Quando deixo a unidade de conversão zerada
    Então vejo "* Informe a unidade de conversao *"
    E nada é gravado

  Cenário: RN-11 — quantidade mínima a fracionar de pedidos não informada
    Dado que estou completando a inclusão
    Quando deixo zerada a quantidade mínima a fracionar de pedidos
    Então vejo "* Informe menor qt a fracionar - pedidos *"
    E nada é gravado

  Cenário: RN-11 — quantidade mínima a fracionar de nota fiscal não informada
    Dado que estou completando a inclusão
    Quando deixo zerada a quantidade mínima a fracionar de nota fiscal
    Então vejo "* Informe menor qt a fracionar - NF *"
    E nada é gravado

  Cenário: RN-12 — o indicador de orgânico não é S nem N
    Dado que estou completando a inclusão
    Quando informo no indicador de orgânico algo diferente de S e de N
    Então vejo "* Informe se organico com S ou N *"
    E nada é gravado

  Cenário: RN-12 e RN-18 — marcar o gênero como orgânico cria o relacionamento
    Dado que o gênero está cadastrado e não é orgânico
    Quando o altero informando S no indicador de orgânico
    Então o registro do relacionamento daquele gênero é criado
    E fica disponível para a tela C054T manter
    E a criação fica registrada na trilha de auditoria

  Cenário: RN-12 e RN-18 — incluir um gênero já marcado como orgânico
    Dado que o código existe no SIGMA e o gênero não está cadastrado
    Quando o incluo com S no indicador de orgânico
    Então a versão fica gravada no cadastro de gêneros
    E o registro do relacionamento daquele gênero é criado
    E a criação fica registrada na trilha de auditoria

  Cenário: RN-12 — desmarcar o orgânico retira o relacionamento
    Dado que o gênero está cadastrado como orgânico e o relacionamento não aponta para outro gênero
    Quando o altero informando N no indicador de orgânico
    Então o registro do relacionamento daquele gênero é retirado
    E a retirada fica registrada na trilha de auditoria

  Cenário: RN-13 — alterar sem consultar antes
    Dado que não consultei o gênero nesta tela
    Quando informo ALT com a classe, a subclasse, o código do gênero e a data
    Então vejo "* Consulte o genero antes de alterar *"
    E nada é gravado

  Cenário: RN-13 — alterar com uma data que não é a da versão
    Dado que consultei o gênero
    Quando informo ALT trocando a data de início por outra
    Então vejo "* Genero desativado para esta data *"
    E nada é gravado

  Cenário: RN-13 — tentar trocar o grupo de licitação na alteração
    Dado que consultei o gênero e estou alterando
    Quando troco o grupo de licitação
    Então vejo "* Nao altere grupo da licitacao *"
    E nada é gravado

  Cenário: RN-13 — o indicador de ativo não é S nem N
    Dado que consultei o gênero e estou alterando
    Quando informo no indicador de ativo algo diferente de S e de N
    Então vejo "* Informe ativo com S ou N *"
    E nada é gravado

  Cenário: RN-01, RN-13 e RN-18 — alterar uma versão consultada
    Dado que consultei o gênero e a versão que quero alterar
    Quando informo ALT trocando a descrição, a unidade de compra ou as quantidades
    E confirmo
    Então a versão passa a ter os novos dados
    E a operação fica registrada na trilha de auditoria

  Cenário: RN-14 — excluir sem consultar antes
    Dado que não consultei o gênero nesta tela
    Quando informo EXC com a classe, a subclasse, o código do gênero e a data
    Então vejo "* Consulte o genero antes de excluir *"
    E nada é gravado

  Cenário: RN-14 — excluir um gênero orgânico que tem relacionamento
    Dado que consultei um gênero orgânico cujo relacionamento aponta para outro gênero
    Quando informo EXC
    Então vejo uma recusa mandando excluir antes o relacionamento do gênero
    E nada é gravado

  Cenário: RN-15 e RN-18 — excluir uma versão consultada
    Dado que consultei o gênero e a versão que quero excluir
    Quando informo EXC e confirmo
    Então a versão fica marcada como excluída e com o ativo em N
    E deixa de aparecer nas consultas
    E continua na base
    E a operação fica registrada na trilha de auditoria

  Cenário: RN-16 — abrir a tela pelo menu
    Dado que venho do menu C055M
    Quando a tela C050T abre
    Então ela abre em consulta e em branco

  Cenário: RN-16 — abrir a tela pela consulta C240C
    Dado que estou na consulta C240C com uma subclasse e um código de gênero
    Quando a C240C passa para a tela C050T
    Então a tela abre em consulta
    E já com a subclasse e o código do gênero informados
    E, existindo versão daquele gênero, com os dados dela carregados

  Cenário: RN-16 — a carga da origem não se repete
    Dado que a tela abriu vinda da consulta C240C e já carregou o gênero
    Quando a tela volta a se apresentar
    Então ela não recarrega o gênero daquela origem
    E o que está na tela é o que o servidor informou

  Cenário: RN-17 — a tela não encaminha para outra do cadastro
    Dado que informei uma consulta que achou o gênero
    Quando a tela entrega o resultado
    Então ela reabre a si mesma com o gênero e a operação
    E não passa para outra tela do cadastro

  Cenário: RN-19 — sem permissão para a operação
    Dado que o meu acesso não tem a marca da operação informada nesta tela
    Quando confirmo a operação
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-19 — sem registro de acesso para a tela
    Dado que o meu código de acesso não tem registro para esta tela
    Quando a tela tenta operar
    Então vejo "* Acesso negado para esta matricula *"
    E nada é gravado

  Cenário: RN-20 — falha do banco durante a gravação
    Dado que a gravação no cadastro de gêneros falha
    Quando confirmo a operação
    Então a falha é avisada pela rotina de comunicação do sistema
    E a operação não é considerada gravada
```
