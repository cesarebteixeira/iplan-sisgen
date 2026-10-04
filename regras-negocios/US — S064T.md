# US — S064T — Manter vínculos de acesso da matrícula

## Estória

Como **servidor de CRE**, quero **manter, para a matrícula de um servidor, a quais
secretarias, grupos regionais e órgãos filhos ela tem acesso — e com que nível de
acesso**, para que **o que cada servidor enxerga e opera no sistema fique preso a um
conjunto de vínculos que a própria CRE controla, sem que ninguém receba acesso que a
CRE não deu**.

O acesso de um servidor a uma secretaria não é um campo do cadastro dele: é um
vínculo separado, com o nível que ele tem naquela secretaria, no grupo daquela
secretaria e no órgão filho daquele grupo. É por esse vínculo que o sistema decide,
tela a tela, o que ele pode ver e fazer. Esta tela é o único lugar em que o conjunto
desses vínculos de uma matrícula é montado e desmontado de uma vez — e é por aqui,
também, que se corrige a origem do servidor, que é a descrição pela qual a secretaria
o localiza. Sem esta tela, conceder acesso seria abrir tela por tela para cada
servidor, e nenhum cadastro de unidade ficaria sabendo a quais matrículas ele atende.

## Contexto

Jornada S000M → S001M → S004M → S064T.
Ator: servidor de CRE — monta e desmonta, para uma matrícula, o conjunto de vínculos
de acesso às secretarias, aos grupos regionais e aos órgãos filhos, com o nível de
acesso de cada um.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada, `S001M` e `S004M`, são menus: só encaminham e
não deixam dado de negócio para esta tela. O que a `S064T` usa da sessão — a matrícula
de quem opera, o código de acesso dela, o privilégio que ela tem, a secretaria e o
tipo de órgão — é o que a entrada deixou, e as conferências de acesso da abertura são
as da entrada.

A `S064T` é uma tela de transação que, no fim, **encadeia noutra tela** sem passar por
menu: há uma passagem em que ela entrega o controle à tela que mantém o catálogo das
descrições de origem. Essa passagem depende de um pedido que quem chamou a `S064T`
deixa registrado, e não de campo nenhum da tela nova (RN-14).

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela mostra os vínculos de uma matrícula numa lista de dez linhas

Ao abrir, a tela mostra a descrição do tipo de órgão da sessão e a data do sistema, e
monta uma lista com os vínculos de acesso já cadastrados para a matrícula. A lista tem
**dez linhas**, e cada linha tem cinco colunas: a secretaria, o grupo regional
(coordenação regional de escola), o órgão filho, o nível de acesso e a **ação** — que
diz o que fazer com aquela linha. A matrícula de que a lista trata é a que estiver no
campo próprio do cabeçalho; o nome do servidor e a origem dele só aparecem depois que
essa matrícula é lida com sucesso (RN-06).

### RN-02 — A tela só altera e consulta, e a consulta é o ponto de partida

A opção informada só pode ser **alteração** ou **consulta**. Em branco, a tela assume
**consulta**. Qualquer outra — inclusive inclusão e exclusão — é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da opção, e
nada é lido nem gravado.

### RN-03 — Em alteração, a matrícula precisa ter sido consultada antes

No modo de alteração, a tela só aceita mexer numa matrícula que já apareceu na lista
por uma consulta anterior, na mesma sessão de tela. Informando uma matrícula que ainda
não foi lida, a alteração é recusada com **\* Consulte antes de atualizar \***, o
cursor volta ao campo da matrícula, e nada é gravado.

### RN-04 — A ação de cada linha decide a operação

Em cada linha, a **ação** decide o que fazer: **I** inclui o vínculo daquela linha e
**E** exclui o vínculo. Linha sem secretaria, ou com ação diferente de I e E, é
**ignorada**: não gera operação nenhuma e a tela passa à linha seguinte. A ação só é
olhada depois das conferências de autorização e de acesso da linha (RN-09 a RN-12), e
em consulta as linhas nem chegam a ser processadas (RN-13).

### RN-05 — A secretaria e o nível de acesso são exigidos em cada linha

Na linha, a **secretaria** e o **nível de acesso** são de preenchimento obrigatório.
Linha sem secretaria é ignorada (RN-04). Sem nível de acesso, a operação é recusada
com **\* Informe o nivel de acesso \***, o cursor volta ao campo do nível, e nada é
gravado.

### RN-06 — A matrícula é lida para trazer o nome e a origem do servidor

Informada — ou trocada — a matrícula, a tela procura o cadastro do servidor. Achando,
mostra o **nome** e a **origem** dele no cabeçalho e passa a trabalhar com os vínculos
daquela matrícula; é essa leitura que habilita a alteração (RN-03). Não achando, a
operação é recusada com **\* Matricula nao cadastrada \*** e o cursor volta ao campo da
matrícula. Matrícula em branco, quando exigida, é recusada com **\* Informe matricula
\***. A tela não deixa passar para nenhuma operação sem a leitura da matrícula.

[?] A tela avisa **\* Matricula sem secretarias cadastradas \*** quando o servidor não
tem nenhum vínculo, mas a verificação que dispara esse aviso depende de uma marca que
o próprio programa só sabe produzir quando não encontra o vínculo — e ela é apagada
logo no começo da leitura de cada linha. Se o aviso aparece na prática, e em que
momento do processamento, não dá para concluir do fonte. Pergunta ao site.

### RN-07 — O operador não mantém o próprio cadastro por esta tela

Se a matrícula informada for a do próprio operador, a alteração é recusada com
**\* Nao atualize seu proprio cadastro \***, o cursor volta ao campo da matrícula, e
nada é gravado. A tela faz isso para o operador não conceder a si mesmo acesso nem
reescrever o próprio vínculo.

### RN-08 — O nível de acesso concedido não pode ser maior que o do operador

O nível de acesso informado na linha é conferido contra o cadastro de níveis de acesso
do sistema e contra o **nível do próprio operador**. Nível maior que o do operador é
recusado com **\* Seu nivel de acesso nao permite esta operacao \***, o cursor volta ao
campo da opção, e nada é gravado. Nível igual ou menor passa. Quem opera com o
privilégio da sessão passa também com o nível igual, na mesma comparação.

[?] Nível não cadastrado no sistema é recusado com **\* Nivel de acesso nao cadastrado
\***. O que o código do nível significa em ordem — se o número maior é o nível mais
poderoso ou o menos — não está no corpus: a regra acima descreve a comparação, não a
hierarquia. Pergunta ao site.

### RN-09 — A secretaria, o grupo e o órgão informados precisam existir e ser do operador

Antes de a linha operar, a tela confere a **secretaria** informada: não existindo no
cadastro, a recusa é **\* Secretaria nao cadastrada \***. Depois confere se o operador
tem o **código de acesso** daquela secretaria: não tendo, a recusa é **\* Usuario sem
acesso a esta secretaria \***. Em seguida confere o **grupo regional**: não existindo
naquela secretaria, a recusa é **\* Grupo nao cadastrado nesta secretaria \***; não
sendo um grupo do operador, a recusa é **\* Usuario sem acesso a outro grupo \***. Por
fim confere o **órgão filho**, e essa conferência só vale quando há órgão informado:
não existindo, a recusa é **\* Orgao nao cadastrado \***; sendo de outra secretaria,
**\* Orgao nao pertence a esta secretaria \***; sendo de outro grupo, **\* Orgao nao
pertence ao grupo informado \***; e, estando o cadastro do órgão incompleto, **\* Orgao
cadastrado com dados incompletos \***. Em todas elas o cursor volta ao campo da linha
que falhou e nada é gravado. Linha sem órgão informado passa por essa última parte sem
conferência e concede o acesso à secretaria e ao grupo como um todo.

### RN-10 — Incluir um vínculo que já existe é recusado

Para incluir, a tela procura o par matrícula-e-secretaria no quadro de vínculos.
Existindo, a inclusão é recusada com **\* Matricula ja cadastrada nesta secretaria \***,
o cursor volta ao campo da secretaria, e nada é gravado. Um servidor tem **um** vínculo
por secretaria: incluir de novo é sempre recusa.

### RN-11 — A inclusão grava o vínculo e registra a operação

Passando por todas as conferências, a inclusão grava o vínculo com a secretaria, o
grupo regional, o órgão filho e o nível de acesso da linha, e registra a operação com
os dados de quem a fez: o sistema anota a data e a hora do sistema, a tela de onde a
operação partiu, a matrícula do operador, o tipo de órgão e a operação praticada,
guardando o vínculo como estava antes e como ficou depois.

### RN-12 — A exclusão tira o vínculo, e só se ele existir e for do operador

A ação **E** exclui o vínculo da linha. Antes de excluir, a tela confere duas coisas:
que o vínculo **existe** para aquela matrícula naquela secretaria — não existindo, a
recusa é **\* Matricula nao cadastrada nesta secretaria \*** — e que o vínculo é de uma
secretaria e de um grupo que o operador também tem — não sendo, a recusa é **\*
Usuario sem acesso a esta secretaria \*** ou **\* Usuario sem acesso a outro grupo \***
conforme a coluna que divergir. Passando, o vínculo é apagado e a exclusão é registrada
com os dados de quem a fez, como na inclusão (RN-11).

### RN-13 — A consulta não grava nada, e o que se corrige é a origem do servidor

Em consulta, a tela lê e mostra: as linhas não são processadas e nenhum vínculo é
incluído ou apagado. É também na alteração que a tela **corrige a origem do servidor**:
quando a origem mostrada no cabeçalho é diferente da que está gravada no cadastro do
servidor, a tela reescreve a origem do cadastro do servidor com a origem informada e
registra a operação, guardando o cadastro como estava antes e como ficou depois. Quando
a origem informada é igual à já gravada, nada é reescrito. Essa correção só acontece na
alteração e com a linha de ação de inclusão — a exclusão não mexe na origem.

[?] A exclusão do vínculo passa por uma conferência de existência e de autorização
diferente da que a inclusão usa — a exclusão confere o vínculo gravado, e a inclusão
confere o que foi digitado — de modo que **excluir um vínculo que o operador não tem**
é recusado mesmo quando o operador tem a secretaria. Qual das duas conferências é a
pretendida, e se a exclusão deveria ser mais permissiva que a inclusão, não dá para
concluir do fonte. Pergunta ao site.

### RN-14 — A tela entrega o controle ao catálogo de origens quando quem a chamou pede

Há uma passagem em que a `S064T` **encadeia na tela que mantém o catálogo das
descrições de origem**, sem passar por menu, e não grava nada por conta disso. Essa
passagem é decidida por um pedido que **quem chamou a `S064T`** deixa registrado — não
por campo nenhum da tela nova, e não pela linha da lista. Sem esse pedido, a `S064T`
segue o seu caminho normal e não encadeia.

[?] O aviso que acompanha essa passagem é o de consulta, e o campo que a decide não
aparece em nenhuma outra tela do lote lido: nada no acervo mostra quem o preenche nem
o que ele significa em português. Se a passagem é a "volta" de quem veio da tela de
origens ou um encaminhamento para ela, não dá para concluir do fonte. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manter os vínculos de acesso de uma matrícula às unidades da secretaria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S064T

  Cenário: Abrir a tela mostra os vínculos já cadastrados e não grava nada
    Dado que a matrícula de um servidor já tem vínculos de acesso cadastrados
    Quando abro a tela S064T
    Então vejo a lista dos vínculos daquela matrícula, com secretaria, grupo regional, órgão filho, nível de acesso e ação
    E vejo a descrição do tipo de órgão da sessão e a data do sistema
    E nenhum vínculo é incluído, apagado ou alterado

  Cenário: A tela trabalha por dez linhas
    Dado que a matrícula de um servidor tem vínculos cadastrados
    Quando abro a tela S064T
    Então vejo os vínculos distribuídos em dez linhas
    E em cada linha posso informar secretaria, grupo regional, órgão filho, nível de acesso e ação

  Cenário: Em branco, a tela assume a consulta
    Dado que abro a tela S064T
    Quando deixo a opção em branco
    Então a tela trata a operação como consulta
    E não grava nada

  Cenário: Opção diferente de alteração e consulta é recusada
    Dado que estou na tela S064T
    Quando informo uma opção que não é alteração nem consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é lido nem gravado

  Cenário: Alterar uma matrícula que não foi consultada antes é recusado
    Dado que estou na tela S064T em alteração
    Quando informo a matrícula de um servidor que ainda não apareceu na lista
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo da matrícula
    E nada é gravado

  Cenário: Linha sem secretaria é ignorada
    Dado que estou na tela S064T em alteração
    Quando deixo a secretaria de uma linha em branco e informo ação nela
    Então a tela ignora essa linha e passa à seguinte
    E nenhum vínculo é incluído ou apagado por causa dela

  Cenário: Linha com ação diferente de inclusão e exclusão é ignorada
    Dado que estou na tela S064T em alteração
    Quando informo a secretaria de uma linha e deixo a ação dela em branco
    Então a tela ignora essa linha e passa à seguinte
    E nenhum vínculo é incluído ou apagado por causa dela

  Cenário: Linha sem nível de acesso é recusada
    Dado que estou na tela S064T em alteração
    Quando informo a secretaria de uma linha e deixo o nível de acesso em branco
    Então vejo a mensagem "* Informe o nivel de acesso *"
    E o cursor volta ao campo do nível de acesso
    E nada é gravado

  Cenário: Matrícula não cadastrada é recusada
    Dado que estou na tela S064T em alteração
    Quando informo uma matrícula que não está no cadastro de servidores
    Então vejo a mensagem "* Matricula nao cadastrada *"
    E o cursor volta ao campo da matrícula
    E nada é gravado

  Cenário: Matrícula em branco é recusada
    Dado que estou na tela S064T em alteração
    Quando deixo a matrícula em branco
    Então vejo a mensagem "* Informe matricula *"
    E o cursor volta ao campo da matrícula
    E nada é gravado

  Cenário: Informar a matrícula mostra o nome e a origem do servidor
    Dado que estou na tela S064T em alteração
    Quando informo a matrícula de um servidor cadastrado
    Então vejo o nome e a origem dele no cabeçalho
    E a lista passa a ser a dos vínculos daquela matrícula

  Cenário: Trocar a matrícula troca a lista e o servidor mostrado
    Dado que já consultei os vínculos de uma matrícula
    Quando troco a matrícula pelo de outro servidor cadastrado
    Então vejo o nome e a origem do novo servidor
    E a lista passa a ser a dos vínculos da matrícula nova

  Cenário: Atualizar o próprio cadastro é recusado
    Dado que estou na tela S064T em alteração
    Quando informo a minha própria matrícula
    Então vejo a mensagem "* Nao atualize seu proprio cadastro *"
    E o cursor volta ao campo da matrícula
    E nada é gravado

  Cenário: Nível de acesso maior que o do operador é recusado
    Dado que estou na tela S064T em alteração e tenho um nível de acesso conhecido
    Quando informo numa linha um nível de acesso maior que o meu
    Então vejo a mensagem "* Seu nivel de acesso nao permite esta operacao *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: Secretaria não cadastrada é recusada
    Dado que estou na tela S064T em alteração
    Quando informo numa linha uma secretaria que não está no cadastro de secretarias
    Então vejo a mensagem "* Secretaria nao cadastrada *"
    E o cursor volta ao campo da secretaria
    E nada é gravado

  Cenário: Secretaria fora do acesso do operador é recusada
    Dado que estou na tela S064T em alteração
    Quando informo numa linha a secretaria do meu acesso e outra secretaria que não é minha
    Então vejo a mensagem "* Usuario sem acesso a esta secretaria *"
    E o cursor volta ao campo da secretaria
    E nada é gravado

  Cenário: Grupo regional e órgão filho são conferidos
    Dado que estou na tela S064T em alteração
    Quando informo numa linha um grupo regional que não existe naquela secretaria
    Então vejo a mensagem "* Grupo nao cadastrado nesta secretaria *"
    E o cursor volta ao campo do grupo regional
    E nada é gravado
    Quando informo numa linha um grupo regional que não é do meu acesso
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E nada é gravado
    Quando informo numa linha um órgão filho que não existe no cadastro de órgãos
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão filho
    E nada é gravado
    Quando informo numa linha um órgão filho de outra secretaria
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E nada é gravado
    Quando informo numa linha um órgão filho de outro grupo
    Então vejo a mensagem "* Orgao nao pertence ao grupo informado *"
    E nada é gravado

  Cenário: Linha sem órgão filho concede o acesso à secretaria e ao grupo
    Dado que estou na tela S064T em alteração e o operador tem a secretaria e o grupo informados
    Quando preencho uma linha com a secretaria do meu acesso, o grupo regional, um nível de acesso permitido, a ação de inclusão e deixo o órgão filho em branco
    Então o vínculo fica gravado para a secretaria e o grupo, sem órgão filho
    E nenhuma conferência de órgão filho é feita

  Cenário: Incluir um vínculo que já existe é recusado
    Dado que a matrícula consultada já tem vínculo com uma secretaria
    Quando informo numa linha essa mesma secretaria com ação de inclusão
    Então vejo a mensagem "* Matricula ja cadastrada nesta secretaria *"
    E o cursor volta ao campo da secretaria
    E nada é gravado

  Cenário: Incluir um vínculo novo grava o acesso e registra a operação
    Dado que consultei a matrícula de um servidor que não tem vínculo com uma secretaria
    Quando informo numa linha essa secretaria, o grupo regional, o órgão filho, um nível de acesso permitido e a ação de inclusão
    Então o vínculo fica gravado com a secretaria, o grupo, o órgão e o nível informados
    E o sistema registra a data e a hora, a tela de origem, a matrícula de quem operou e a operação praticada
    E o registro guarda como o vínculo estava antes e como ficou depois

  Cenário: Excluir um vínculo que não existe é recusado
    Dado que consultei a matrícula de um servidor
    Quando informo numa linha uma secretaria com a qual ele não tem vínculo e a ação de exclusão
    Então vejo a mensagem "* Matricula nao cadastrada nesta secretaria *"
    E o cursor volta ao campo da secretaria
    E nenhum vínculo é apagado

  Cenário: Excluir um vínculo que existe apaga o acesso e registra a operação
    Dado que consultei a matrícula de um servidor que tem vínculo com uma secretaria do meu acesso
    Quando informo numa linha essa secretaria com a ação de exclusão
    Então o vínculo é apagado
    E o sistema registra a data e a hora, a tela de origem, a matrícula de quem operou e a operação praticada
    E o registro guarda como o vínculo estava antes de ser apagado

  Cenário: Corrigir a origem do servidor reescreve o cadastro dele
    Dado que consultei a matrícula de um servidor cuja origem gravada é diferente da origem mostrada
    Quando confirmo a alteração com a linha de ação de inclusão
    Então a origem do cadastro do servidor passa a ser a origem informada
    E o sistema registra a operação com o cadastro como estava antes e como ficou depois

  Cenário: Consulta não grava nada
    Dado que estou na tela S064T em consulta
    Quando preencho uma ou mais linhas com ação de inclusão ou de exclusão
    Então a tela mostra os vínculos e não processa as linhas
    E nenhum vínculo é incluído ou apagado
    E a origem do servidor não é reescrita

  Cenário: Sem o pedido de quem chamou, a tela não encadeia
    Dado que cheguei à tela S064T pelo menu, sem pedido registrado de encadeamento
    Quando termino a operação
    Então a tela não entrega o controle ao catálogo das descrições de origem
    E nenhuma outra tela é aberta por causa disso
```
