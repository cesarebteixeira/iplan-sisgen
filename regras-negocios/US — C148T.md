# US — C148T — Manter as telas de uso de cada tipo de licitação

## Estória

Como **servidor de CRE**, quero **declarar quais telas cada tipo de licitação pode
usar**, para que uma licitação daquele tipo só aceite as telas que estiverem
declaradas para ele.

O tipo de licitação classifica a licitação, e cada tipo tem o seu conjunto de telas.
É esse conjunto que libera a tela em uso dentro de uma licitação: quando o servidor
abre, numa licitação, uma tela que não foi declarada para o tipo dela, o sistema
recusa com **\* Tela nao disponivel para esta licitacao \*** e ele não trabalha.
Sem a declaração, o tipo fica sem tela nenhuma liberada e o processo daquele tipo
não anda. A tela serve às duas pontas — declarar e conferir —, e é na conferência
que nada é gravado.

## Contexto

Jornada S000M → C000M → C015M → C148T.

Ator: servidor de CRE — declara, por tipo de licitação, as telas que aquele tipo usa.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada — `C000M` e `C015M` — são menus: nenhuma delas
deixa para a `C148T` um registro ou uma operação. A opção que a tela obedece é a do
seu próprio campo, e a tela abre no estado que a sessão guardou (RN-06). Ela é o
**fim** do caminho: não entrega registro nem operação adiante, e o único
encadeamento que ela conhece é o campo que indica qual tela deve ser aberta em
seguida — que nada nesta jornada preenche (RN-18). Do que a sessão guarda — a
matrícula, o código de acesso, a CRE e o órgão deixados pela entrada — a tela usa o
contexto para conferir permissão e para registrar a auditoria, e não para recortar a
lista.

As regras abaixo são só as da tela desta jornada; as da entrada não se repetem aqui.

## Regras de negócio

### RN-01 — A tela trabalha sobre um tipo de licitação

Um tipo de licitação por vez, identificado pelo código que o servidor informa. O
cabeçalho identifica o tipo (código e descrição), o órgão da sessão e a data do
sistema. Tudo o que a lista mostra e tudo o que a tela grava pertence a esse tipo. A
descrição do tipo não vem do terminal: ela é recarregada do cadastro a cada
consulta, e o que o terminal devolver nesse campo é descartado.

[?] De onde vem a data do sistema que o cabeçalho exibe não está nas telas desta
jornada: nenhuma delas a preenche. Pergunta ao site.

### RN-02 — O que a tela mantém é o vínculo entre o tipo de licitação e a tela

O que a tela inclui e exclui é o par **tipo de licitação × tela**. O cadastro do tipo
de licitação e o cadastro de telas servem só para conferir: a tela não cria, não
altera e não exclui nenhum dos dois. Também não é por esta tela que se autoriza o
servidor: quem pode incluir e excluir é conferido à parte, pelo cadastro de acesso
por tela.

### RN-03 — O vínculo não é por secretaria: vale para todo o sistema

O vínculo guarda apenas o tipo de licitação e a tela — não guarda secretaria, CRE
nem órgão. A secretaria, a CRE, a matrícula e o órgão do servidor entram na
conferência de permissão e no registro de auditoria, mas não recortam a lista: o que
um servidor de uma CRE declara para um tipo de licitação vale para as demais.

### RN-04 — A lista mostra as telas já vinculadas, com o nome que vem do cadastro de telas

A lista traz os vínculos que já existem para o tipo em foco, um por linha: o código
da tela e o nome dela, este buscado no cadastro de telas a cada exibição. O que o
terminal devolver no campo do nome é descartado.

### RN-05 — A página tem 14 linhas, uma por tela

São **14 linhas** por página. Cada linha tem o código da tela (é ele que identifica
o vínculo) e a ação da linha. A página é preenchida com os vínculos do tipo em foco,
na ordem do cadastro; quando a lista acaba, as linhas restantes ficam vazias.

### RN-06 — A tela abre no estado que a sessão guardou; sem nenhum, em consulta

Ao ser aberta, a tela assume a opção e o tipo de licitação que a sessão tem em foco
— os da última vez em que a tela foi usada. Na primeira abertura da sessão não há
nem um nem outro: não havendo opção, a tela está em **consulta**; não havendo tipo
em foco, a lista vem vazia. A consulta é o que põe o tipo em foco.

### RN-07 — A opção só admite alterar e consultar

A opção da página aceita **alterar** e **consultar**: incluir e excluir não se
escolhem no campo da opção, e sim linha a linha. Qualquer outra opção é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta no campo da
opção, e nada é gravado.

[?] A recusa manda usar ALT e CON, mas a conferência da opção compara códigos
internos de alteração e de consulta. Ou o terminal converte a tecla nesse código
antes de enviar, ou a mensagem manda o servidor informar algo que a tela recusa.
Pergunta ao site; não escolho um dos dois.

### RN-08 — Alterar exige ter consultado antes o mesmo tipo

Para alterar, o tipo informado tem de ser o mesmo que a última consulta deixou em
foco. Sendo outro, a recusa é **\* Consulte antes de atualizar \***, com o cursor de
volta no campo do tipo. A alteração não relê o cadastro do tipo: quem confere o tipo
no cadastro é a consulta, e é dela que a alteração se aproveita.

### RN-09 — Consultar exige informar um tipo cadastrado

Na consulta o tipo é obrigatório: em branco, a recusa é
**\* Informe o tipo de licitacao \***; informado mas não encontrado no cadastro do
tipo de licitação, a recusa é **\* Tipo de Licitacao nao cadastrado \***. Passando
pelas duas, a tela adota o tipo — código e descrição — e reinicia a lista desde a
primeira tela.

### RN-10 — Tipo sem tela vinculada é avisado, com a lista vazia

Quando não há nenhum vínculo para o tipo em foco, a lista fica vazia e a tela avisa
**\* Nao existem telas cadastradas \*** na primeira linha.

[?] O aviso depende da marca de "não encontrado" que a leitura da lista deixa.
Quando não há tipo em foco, essa leitura não acontece e a marca não é reiniciada —
o aviso não sai, e o servidor vê uma lista vazia sem explicação. Se o aviso deveria
sair também nesse caso, falta uma guarda. Pergunta ao site.

### RN-11 — Incluir uma tela exige que ela não esteja vinculada e que exista no cadastro de telas

A ação de incluir numa linha tem duas conferências: se a tela já está vinculada ao
tipo, a recusa é **\* Tela ja cadastrada \***, com o cursor na coluna da ação; se
não está vinculada mas não existe no cadastro de telas, a recusa é
**\* Tela nao cadastrada \***. Passando pelas duas, o vínculo é gravado.

[?] A conferência do cadastro de telas não olha o indicador de exclusão desse
cadastro: uma tela marcada como excluída no cadastro de telas ainda pode ser
vinculada. Ou o indicador não vale para esta conferência, ou falta a guarda.
Pergunta ao site.

[?] A leitura que decide "já cadastrada" e a que decide "tela não cadastrada" usam
marcas de leitura próprias do banco, cuja semântica não está no material
disponível. Tratei as duas como leitura pela chave exata (tipo + tela), que é o que
o par de campos informados permite; se a leitura for posicional, o desfecho muda.

[?] A documentação extraída do acervo lista, para esta tela, uma recusa por destino
inválido na gravação, mas o caminho que a produz é desligado antes de qualquer
inclusão — pela tela, essa recusa não acontece. Divergência entre a documentação e o
comportamento, a confirmar com o site.

### RN-12 — Excluir uma tela exige que ela esteja vinculada

A ação de excluir numa linha exige que o vínculo exista: sem ele, a recusa é
**\* Tela nao cadastrada \***, com o cursor na coluna da ação. Havendo, o vínculo é
apagado do cadastro.

### RN-13 — Linha sem código, sem ação ou com ação desconhecida não faz nada

Linha com o código da tela em branco é ignorada. Linha com código preenchido e ação
em branco, ou com ação diferente de incluir e de excluir, também não faz nada: não
gera recusa e não grava. Só as duas ações, com o código preenchido, são tratadas.

### RN-14 — A consulta não grava nada

Com a opção de consulta, a tela não valida linha nenhuma e não chega à gravação:
nada é incluído, nada é excluído e nenhum registro de auditoria é criado. A consulta
serve para ler a lista e para pôr o tipo em foco.

### RN-15 — Uma linha recusada recusa a página inteira

A recusa de uma linha interrompe a validação das demais, e a página não chega à
gravação: nenhum vínculo é incluído nem excluído enquanto houver uma linha recusada.
Não existe gravação parcial da página.

[?] O abandono da página depende da marca de erro que a recusa deixa na operação — e
o que produz essa marca não está no material desta jornada, que só traz o texto de
cada mensagem. Se a marca não for deixada, a página gravaria as linhas já validadas.
Pergunta ao site; não concluo.

### RN-16 — Toda gravação deixa rastro na auditoria

Cada vínculo incluído ou excluído gera um registro na auditoria (`A010T`), com o
cadastro auditado (o próprio vínculo tipo × tela), a operação (inclusão ou
exclusão), o valor anterior, o valor novo e o contexto da sessão — matrícula, CRE,
órgão, terminal, data, hora e o número do processo. Na inclusão, o valor novo é o
vínculo gravado e o valor anterior fica vazio; na exclusão, o valor anterior é o
vínculo apagado e o valor novo fica vazio.

### RN-17 — Nada é exibido nem gravado sem a segurança de tela e a permissão da operação

Antes de exibir, a tela confere a autorização da tela para o código de acesso do
servidor e o estado da sessão; sem isso não exibe, e as recusas são as da rotina de
segurança — **\* Tela nao disponivel \*** ou
**\* Acesso negado para esta matricula \***. Antes de manter, confere a rota e a
permissão da operação: **incluir exige a inclusão liberada, alterar exige a
alteração liberada e excluir exige a exclusão liberada** para esta tela — sem a
liberação, a recusa é **\* Acesso negado para esta operacao \*** —, e a consulta
segue sem exigir permissão de operação. Se qualquer conferência não retorna OK, a
tela limpa o status e sai: nada é validado, nada é gravado e nada é auditado.

[?] A permissão é conferida na passagem de validação e não se repete na passagem que
grava: se ela mudasse entre as duas, a gravação não a reconferiria. Pergunta ao site
se isso é aceitável.

### RN-18 — Código de outra tela no campo de encadeamento: a tela não processa a transação

Se a transação chega com o **código de uma tela** no campo de encadeamento, a `C148T`
não valida nem grava nada: pela lógica de rota, a transação é encaminhada à tela ali
indicada, antes de qualquer teste de linha. O campo serve para dizer qual tela deve
ser aberta em seguida.

[?] O programa só lê esse campo; nenhum programa da árvore expandida o preenche — só
o limpa. Ou o terminal o preenche, ou o encaminhamento é inalcançável. Pergunta ao
site.

## Cenários BDD

```gherkin
Funcionalidade: Manter as telas de uso de cada tipo de licitação

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C148T

  Cenário: RN-01 — o cabeçalho identifica o tipo de licitação e o órgão da sessão
    Dado que estou na tela C148T com um tipo de licitação em foco
    Então o cabeçalho mostra o código e a descrição do tipo
    E mostra o órgão da minha sessão
    E a data exibida é a do sistema

  Cenário: RN-02 — a tela mantém o vínculo e não mexe nos cadastros
    Dado que estou na tela C148T no modo de alteração
    Quando confirmo uma inclusão e uma exclusão de tela
    Então o vínculo entre o tipo de licitação e a tela é gravado ou apagado
    E o cadastro do tipo de licitação e o cadastro de telas continuam como estavam

  Cenário: RN-03 — o vínculo vale para todo o sistema
    Dado que declarei uma tela para um tipo de licitação
    Quando outro servidor, de outra secretaria, consulta o mesmo tipo
    Então ele vê a mesma lista de telas

  Cenário: RN-04 — a lista mostra as telas vinculadas com o nome do cadastro
    Dado que consultei um tipo de licitação que tem telas vinculadas
    Então vejo uma linha por tela, com o código da tela
    E o nome exibido é o do cadastro de telas, não o que o terminal enviar

  Cenário: RN-05 — a página tem 14 linhas
    Dado que abro a tela C148T
    Então a lista tem até 14 linhas
    E cada linha tem o código da tela e a ação da linha

  Cenário: RN-06 — primeira abertura da sessão: a tela está em consulta
    Dado que abro a tela C148T pela primeira vez na sessão
    Então a tela está em consulta
    E a lista do tipo em foco é exibida
    E nada é gravado

  Cenário: RN-07 — opção não disponível
    Dado que estou na tela C148T
    Quando informo uma opção diferente de alterar e de consultar
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: RN-08 — alterar um tipo que não foi consultado
    Dado que estou na tela C148T com a opção de alteração
    E informo um tipo de licitação diferente do que consultei
    Quando confirmo
    Então vejo "* Consulte antes de atualizar *"
    E o cursor volta ao campo do tipo
    E nada é gravado

  Cenário: RN-09 — consultar sem informar o tipo
    Dado que estou na tela C148T com a opção de consulta
    E deixo o tipo de licitação em branco
    Quando confirmo
    Então vejo "* Informe o tipo de licitacao *"
    E nada é gravado

  Cenário: RN-09 — consultar um tipo não cadastrado
    Dado que estou na tela C148T com a opção de consulta
    E informo um tipo de licitação que não está no cadastro
    Quando confirmo
    Então vejo "* Tipo de Licitacao nao cadastrado *"
    E nada é gravado

  Cenário: RN-09 — a consulta de um tipo cadastrado carrega o tipo
    Dado que estou na tela C148T com a opção de consulta
    E informo um tipo de licitação cadastrado
    Quando confirmo
    Então a tela adota esse tipo, com a descrição do cadastro
    E a lista volta a começar da primeira tela
    E nada é gravado

  Cenário: RN-10 — tipo sem tela vinculada
    Dado que o tipo de licitação em foco não tem nenhuma tela vinculada
    Quando a tela C148T exibe a lista
    Então a lista fica vazia
    E vejo "* Nao existem telas cadastradas *"

  Cenário: RN-11 — incluir uma tela ainda não vinculada
    Dado que estou na tela C148T no modo de alteração
    E que a tela informada existe no cadastro de telas e não está vinculada ao tipo
    Quando marco a ação de incluir na linha e confirmo
    Então o vínculo entre o tipo de licitação e a tela é gravado

  Cenário: RN-11 — incluir uma tela já vinculada
    Dado que estou na tela C148T no modo de alteração
    Quando marco a ação de incluir numa tela que já está vinculada ao tipo
    Então vejo "* Tela ja cadastrada *"
    E o cursor fica na coluna da ação
    E nada é gravado

  Cenário: RN-11 — incluir uma tela que não existe no cadastro de telas
    Dado que estou na tela C148T no modo de alteração
    Quando marco a ação de incluir numa tela que não existe no cadastro de telas
    Então vejo "* Tela nao cadastrada *"
    E nada é gravado

  Cenário: RN-12 — excluir uma tela vinculada
    Dado que estou na tela C148T no modo de alteração
    E que a tela está vinculada ao tipo em foco
    Quando marco a ação de excluir na linha e confirmo
    Então o vínculo entre o tipo de licitação e a tela é apagado

  Cenário: RN-12 — excluir uma tela que não está vinculada
    Dado que estou na tela C148T no modo de alteração
    Quando marco a ação de excluir numa tela que não está vinculada ao tipo
    Então vejo "* Tela nao cadastrada *"
    E o cursor fica na coluna da ação
    E nada é gravado

  Cenário: RN-13 — linha sem código ou sem ação não faz nada
    Dado que estou na tela C148T no modo de alteração
    Quando deixo o código da tela em branco, ou deixo a ação em branco, ou escrevo uma ação diferente de incluir e de excluir
    Então a linha não é validada, não recebo recusa e nada é gravado para ela

  Cenário: RN-14 — a consulta não grava nada
    Dado que estou na tela C148T no modo de consulta
    Quando confirmo a tela
    Então nenhum vínculo é gravado ou apagado
    E nenhum registro de auditoria é criado

  Cenário: RN-15 — uma linha recusada recusa a página inteira
    Dado que estou na tela C148T no modo de alteração
    E que uma das linhas da página é recusada
    Quando confirmo a tela
    Então nenhuma das outras linhas é gravada
    E a página não grava nada

  Cenário: RN-16 — toda gravação deixa rastro na auditoria
    Dado que incluí o vínculo de uma tela com o tipo de licitação
    Então fica registrada a inclusão, com o valor novo do vínculo
    E com a minha matrícula, a CRE, o órgão, o terminal, a data e a hora
    E, ao excluir um vínculo, fica registrada a exclusão com o valor anterior

  Cenário: RN-17 — sem autorização para a tela
    Dado que o meu código de acesso não tem a tela C148T liberada
    Quando abro a tela C148T
    Então a lista não é exibida
    E recebo a mensagem da rotina de segurança

  Cenário: RN-17 — sem permissão para a operação
    Dado que o meu código de acesso não tem a inclusão liberada para a tela C148T
    Quando confirmo uma inclusão na tela C148T
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado
    E nenhum registro de auditoria é criado

  Cenário: RN-18 — a transação traz o código de outra tela
    Dado que a transação chega à tela C148T com o código de outra tela no campo de encadeamento
    Quando a validação da manutenção começaria
    Então nenhuma linha é validada
    E nada é gravado
    E a transação é encaminhada à tela indicada
```
