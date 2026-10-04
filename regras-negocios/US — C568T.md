# US — C568T — Alterar as datas de vigência do período de contrato da coordenadoria regional

## Estória

Como **servidor de CRE**, quero **alterar as datas de início e de fim da vigência de um
período de contrato da minha coordenadoria regional**, para que **a vigência passe a
valer com as novas datas, sem precisar recadastrar o período nem os registros que o
referenciam**.

O período é a faixa de vigência do contrato — o dia, o mês e o ano em que começa e em que
termina —, e é pela data limite que o sistema reconhece cada período. Quando o contrato é
prorrogado ou tem a vigência ajustada, é essa faixa que precisa mudar, e é por isso que a
alteração é pedida aqui, e não no cadastro do contrato. A alteração não sai na hora: ela
vira um pedido de processamento, e enquanto esse processamento não termina o mesmo
relatório não aceita pedido novo. Sem esse pedido, os registros que apontam para o
período continuariam com as datas velhas e a vigência do contrato ficaria contraditória
no sistema.

## Contexto

Jornada S000M → C000M → C050M → C060M → C568T.

Ator: servidor de CRE — informa a coordenadoria regional, o tipo de contrato e a data
limite do período, confere o período que o sistema mostra, informa as novas datas de
início e de fim, confirma e acompanha o processamento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O menu principal e os três menus seguintes da jornada (`C000M`, `C050M` e `C060M`) só
encaminham: não gravam nada e não passam registro nenhum adiante, apenas abrem a tela
escolhida. O contexto que esta tela usa — a matrícula funcional, o código de acesso, o
privilégio, o tipo de órgão, a coordenadoria regional do vínculo e a descrição do tipo de
órgão — é o que a entrada deixou na sessão; esta tela não o recalcula nem o recebe dos
menus.

A tela não encadeia em outra: ela reabre a si mesma para pedir a confirmação e para
mostrar o desfecho. O que ela entrega adiante é um **pedido de processamento** (RN-10),
não uma tela. A operação com que ela abre também não vem de quem a chamou: é a própria
tela que preenche a alteração (RN-01).

---

## Regras de negócio

### RN-01 — Esta tela só altera: qualquer outra opção é recusada

A tela abre com a **alteração** já preenchida no campo de opção. Se a opção enviada não
for a de alteração, o sistema recusa com **\* Opcao nao disponivel. Use ALT \***, devolve
o cursor ao campo da opção e encerra a passagem **antes de ler qualquer cadastro**. Nesta
tela não há inclusão nem exclusão de período: o único caminho que segue é o da alteração,
que ainda passa pela conferência de rota e pela conferência de acesso antes de chegar às
leituras.

[?] O valor que o campo de opção carrega não é o código da operação: é o texto da operação
no idioma do usuário, carregado de uma tabela de mensagens que não está no material lido;
o código interno da alteração é "CHG" e a recusa manda usar "ALT". Não dá para conferir,
pelo fonte, se "ALT" é o texto dessa tabela para a alteração ou outra coisa. Pergunta ao
site.

[?] A tela informa à conferência de rota e à de acesso qual foi a tela de origem. No
acervo, a conferência de rota devolve o servidor à tela de origem quando ela vem
preenchida — a única exceção é a tela C213C — e, sem origem, confere no cadastro de telas
se aquela operação é permitida; nenhuma das duas compara a origem com um código de tela
para decidir o modo desta tela. Se a abertura pelo menu deixa a origem preenchida, e o que
isso muda, o material lido não mostra. Pergunta ao site.

### RN-02 — Só quem tem a coordenadoria regional altera, e ela tem de existir

O período só pode ser alterado pelo servidor cuja coordenadoria regional de vínculo é a
informada. Quando o vínculo não aponta coordenadoria alguma, qualquer uma é aceita; quando
aponta, a informada tem de ser a dele, senão a recusa é
**\* Usuario sem acesso a este grupo \***, com o cursor de volta ao campo. Aceita a
coordenadoria, o sistema confere se ela está cadastrada: não estando, a recusa é
**\* Grupo nao cadastrado \***, também com o cursor no campo. O cadastro das
coordenadorias tem **5 campos** e capacidade para **1.000** registros — capacidade é o
máximo esperado, parâmetro de dimensionamento, não o que está cadastrado.

### RN-03 — O período tem de estar cadastrado para a coordenadoria e o contrato informados

O sistema procura o período pela coordenadoria regional, pelo tipo de contrato e pelo dia,
o mês e o ano limite informados, dentro do tipo de órgão da sessão. Não encontrando a
combinação — ou encontrando um registro cujas chaves não conferem com o que foi informado
—, a recusa é **\* Periodo nao cadastrado \***, com o cursor de volta ao dia do campo
limite. O cadastro dos períodos tem **16 campos** e capacidade para **10.000** registros.

[?] A procura ancora a classe de licitação em zero e o teste que encerra a procura não
compara esse campo. O fonte, portanto, não permite decidir se períodos cadastrados com
outra classe de licitação são alcançados por esta tela — que, além disso, não pede nem
mostra essa classe. Se é intencional, o acervo não diz. Pergunta ao site.

### RN-04 — Não pode haver permissão oficial registrada para aquele período

Antes de pedir as datas novas, o sistema confere se já existe **permissão oficial**
registrada para aquele período: mesma coordenadoria regional, mesmo tipo de contrato e
mesma data limite, com classe de licitação, classe, subclasse e gênero zerados. Existindo,
a recusa é **\* Ja existe permissao oficial \***, com o cursor de volta ao campo da opção,
e nada é pedido nem gravado. As permissões marcadas como excluídas não contam para essa
conferência. O cadastro das permissões tem **52 campos** e capacidade para **1.000.000** de
registros.

[?] A conferência recusa quando a permissão existe; já o processamento que a tela dispara
reajusta as datas do período e de **outro** cadastro do mesmo período, e não o da permissão
conferida aqui. Qual das duas relações o acervo chama de "oficial", e por que só uma delas
é conferida, não está no material lido. Pergunta ao site.

### RN-05 — As duas datas novas são obrigatórias

O operador tem de informar o dia da nova data inicial **e** o dia da nova data final;
faltando qualquer um dos dois, a recusa é
**\* Informe nova data da permissao \*** e o cursor volta ao dia da nova data inicial. A
conferência olha só o dia informado: mês e ano em branco só são recusados adiante, na
validação da data (RN-07).

### RN-06 — A nova vigência tem de ser diferente da vigente

Se a nova data inicial for igual à data de início **e** a nova data final for igual à data
limite que o operador informou como vigentes, o sistema recusa com
**\* Data para atualizacao igual a atual \***, com o cursor de volta ao campo da
coordenadoria regional: não há alteração a fazer.

[?] A comparação usa as datas que o operador digitou como vigentes, e não as que estão
registradas no período; e a procura do período (RN-03) usa apenas a data limite, nunca a
data de início. Uma data de início digitada diferente da cadastrada muda o resultado dessa
recusa sem que a tela avise. Se isso é o pretendido, o acervo não diz. Pergunta ao site.

### RN-07 — As datas novas têm de ser datas válidas, com o ano entre 1994 e 2099

Cada uma das duas datas novas passa pela validação de data do sistema e tem de ter o ano
entre **1994** e **2099**. Recusada a inicial, a mensagem é
**\* Nova data inicial invalida \***, com o cursor no dia da nova data inicial; recusada a
final, é **\* Nova data final invalida \***, com o cursor no dia da nova data final. A
alteração não segue.

### RN-08 — A nova data inicial não pode ser posterior à nova data final

Se a nova data inicial for posterior à nova data final, a recusa é
**\* Novo periodo invalido \***, com o cursor de volta ao dia da nova data inicial.

### RN-09 — O sistema pede confirmação, e só o "S" manda alterar

Passando por todas as conferências, o sistema pede confirmação com
**\* Confirma alteracao do periodo <S/N> ? \***. Só a resposta **"S"** leva a alteração
adiante; qualquer outra resposta não grava nada, e a tela volta a pedir a confirmação
depois de repetir as conferências — não há um desfecho de "alteração cancelada". Se, ao
responder, a coordenadoria regional, o tipo de contrato ou a data limite tiverem mudado, a
confirmação é descartada e tudo é conferido de novo.

[?] As datas novas que chegam junto com a resposta "S" não são as que valem: a alteração é
gravada com as datas informadas e conferidas na passagem anterior. Quem corrigir uma nova
data no momento de confirmar tem a correção ignorada, e a tela não avisa. Pergunta ao
site.

### RN-10 — A alteração não é aplicada na hora: ela entra para processamento

A tela **não altera** o cadastro do período. Ela registra a alteração na auditoria (RN-12)
e cria um **pedido de processamento** com os parâmetros da mudança — a coordenadoria
regional, o tipo de contrato, a data limite vigente, as duas datas novas, a matrícula
funcional, a estação e o tipo de órgão —, e mostra a mensagem
**\* Cadastro sendo atualizado \***. É o processamento do relatório que a tela aciona que
reajusta as datas do período e do segundo cadastro do mesmo período, registra na auditoria
o valor anterior e o novo e apaga o pedido quando termina; se o período ainda não estiver
cadastrado quando ele rodar, ele espera e repete a procura. A tela não executa nenhuma
gravação no cadastro do período: as operações de gravar e de excluir existem declaradas no
programa para todos os cadastros que ele enxerga, mas só as da auditoria e do pedido são
executadas — declarar não é executar.

[?] Como o pedido chega ao processamento não está inteiro no material lido: o acionamento
passa por uma rotina de sistema que não tem fonte no acervo, embora o bloco de parâmetros
gravado pela tela e o bloco lido pelo programa do relatório sejam o mesmo, campo a campo.
Pergunta ao site.

### RN-11 — Um pedido por vez: enquanto o anterior não termina, a tela recusa

Ao receber a confirmação, o sistema percorre os pedidos de processamento já existentes
para este relatório. Havendo algum, a recusa é
**\* Relatorio em processamento. Aguarde. \***, com o cursor de volta ao campo da
confirmação, e nada é gravado — nem a auditoria, nem um pedido novo.

### RN-12 — A alteração fica registrada na auditoria

Antes de criar o pedido, a tela grava um registro de auditoria com a data e a hora da
sessão, o mês de competência, a matrícula funcional, a estação, o tipo de órgão, a
coordenadoria regional, o tipo de contrato, o número do processo, a operação e o valor do
período. O cadastro de auditoria tem **15 campos** e capacidade para **60.000.000** de
registros. O processamento grava o seu próprio registro de auditoria, esse sim com o
período como estava e como ficou.

[?] O registro da tela sai com a operação gravada como **inclusão**, e não como alteração,
e o valor que ele põe no campo do valor anterior é o valor **proposto**, com o campo do
valor novo em branco. Por que a tela não o registra como alteração, o acervo não diz.
Pergunta ao site.

### RN-13 — A tela mostra o período, a licitação e o fornecedor

Além das datas novas que o operador digitou, o que a tela devolve é: a **data do sistema**
e a **descrição do tipo de órgão** da sessão; o dia, o mês e o ano de início e o dia, o
mês e o ano limite do período; o **tipo de licitação** com a sua descrição, lida do
cadastro dos tipos de licitação — não achada, a descrição sai em branco e nenhuma recusa é
apresentada; a descrição do período; e o **código do operador** com a **razão social**,
lida do cadastro dos fornecedores. Quando o período não tem operador, o código e a razão
social saem em branco. Os campos de resultado são apagados no começo de cada passagem, de
modo que uma recusa não deixa na tela o resultado da passagem anterior.

[?] A data do sistema e a descrição do tipo de órgão só são preenchidas na abertura da
tela: a cada envio os dois são apagados e nenhum caminho do fonte os repreenche. Se o
ambiente os conserva entre um envio e outro, o acervo não diz. Pergunta ao site.

[?] O tipo de licitação e o código do operador têm campo na tela e passam pela edição, mas
o valor digitado nunca é usado: o que aparece vem sempre do período cadastrado. Se a
máscara os protege da digitação, o material lido não mostra. Pergunta ao site.

### RN-14 — A digitação dos campos é editada, e o cursor volta ao campo recusado

Os **dezesseis** campos informados passam, um a um, pela edição numérica antes de qualquer
leitura de cadastro: campo em branco é tratado como zero e o que não for número é recusado.
Para **onze** deles — a coordenadoria regional, o tipo de contrato, as três partes da data
limite e as seis datas novas — a tela tem posição de cursor definida e devolve o cursor ao
campo recusado; para o tipo de licitação, as três partes da data de início e o código do
operador a tela não define posição.

[?] Os seis campos de data nova não têm rótulo de negócio: o rótulo que a conferência
carrega é o nome técnico do próprio campo, e é isso que a mensagem de recusa mostraria.
Como a máscara da tela não faz parte do material lido, não se sabe se ela mostra outro
texto. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Alterar as datas de vigência do período de contrato da coordenadoria regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C568T

  Cenário: Alteração do período confirmada
    Dado que informei a coordenadoria regional, o tipo de contrato e a data limite de um período cadastrado
    E informei uma nova data inicial e uma nova data final diferentes das vigentes
    Quando confirmo a alteração com "S"
    Então vejo a mensagem "* Cadastro sendo atualizado *"

  Cenário: A alteração entra para processamento, não sai na hora
    Dado que confirmei a alteração do período
    Quando volto à tela antes de o processamento terminar
    Então o período ainda aparece com as datas anteriores
    E existe um pedido de processamento pendente para este relatório

  Cenário: A alteração fica registrada na auditoria
    Dado que confirmei a alteração do período
    Quando a alteração é registrada
    Então ficam registrados a data e a hora, a minha matrícula, a minha estação, o tipo de órgão, a coordenadoria regional e o valor do período

  Cenário: Abertura da tela mostra o período
    Dado que existe período cadastrado para a coordenadoria regional, o tipo de contrato e a data limite que informei
    Quando abro a tela C568T
    Então vejo as datas de início e de limite do período
    E vejo o tipo de licitação com a sua descrição
    E vejo a razão social do fornecedor do período

  Cenário: Opção diferente da alteração
    Dado que estou na tela C568T
    Quando informo uma opção diferente da alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo da opção
    E nenhum cadastro é lido nesse caminho

  Cenário: Coordenadoria regional fora do meu acesso
    Dado que o meu vínculo é restrito a uma coordenadoria regional
    Quando informo outra coordenadoria regional
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenadoria regional

  Cenário: Coordenadoria regional não cadastrada
    Dado que informo uma coordenadoria regional que não está cadastrada
    Quando envio a alteração
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo da coordenadoria regional

  Cenário: Período não cadastrado
    Dado que não existe período para a coordenadoria regional, o tipo de contrato e a data limite que informei
    Quando envio a alteração
    Então vejo a mensagem "* Periodo nao cadastrado *"
    E o cursor volta ao dia do campo limite

  Cenário: Período com permissão oficial registrada
    Dado que existe permissão oficial registrada para o período que informei
    Quando envio a alteração
    Então vejo a mensagem "* Ja existe permissao oficial *"
    E o cursor volta ao campo da opção
    E nenhuma data nova me é pedida

  Cenário: Datas novas não informadas
    Dado que informei o período a alterar
    Quando envio sem informar o dia da nova data inicial ou o dia da nova data final
    Então vejo a mensagem "* Informe nova data da permissao *"
    E o cursor volta ao dia da nova data inicial

  Cenário: Nova vigência igual à vigente
    Dado que informei o período a alterar
    Quando informo como novas datas exatamente as datas vigentes que informei
    Então vejo a mensagem "* Data para atualizacao igual a atual *"
    E o cursor volta ao campo da coordenadoria regional

  Cenário: Nova data inicial inválida
    Dado que informei o período a alterar
    Quando a nova data inicial não é uma data válida ou tem o ano fora de 1994 a 2099
    Então vejo a mensagem "* Nova data inicial invalida *"
    E o cursor volta ao dia da nova data inicial

  Cenário: Nova data final inválida
    Dado que informei o período a alterar
    Quando a nova data final não é uma data válida ou tem o ano fora de 1994 a 2099
    Então vejo a mensagem "* Nova data final invalida *"
    E o cursor volta ao dia da nova data final

  Cenário: Nova data inicial posterior à nova data final
    Dado que informei o período a alterar
    Quando a nova data inicial é posterior à nova data final
    Então vejo a mensagem "* Novo periodo invalido *"
    E o cursor volta ao dia da nova data inicial

  Cenário: Resposta diferente de "S" na confirmação
    Dado que a tela pediu a confirmação da alteração
    Quando respondo "N"
    Então nenhuma data do período é alterada
    E a tela volta a pedir a confirmação, depois de repetir as conferências

  Cenário: Mudança da identificação do período no momento de confirmar
    Dado que a tela pediu a confirmação da alteração
    Quando respondo "S" tendo mudado a coordenadoria regional, o tipo de contrato ou a data limite
    Então a confirmação é descartada
    E as conferências são feitas de novo

  Cenário: Pedido de processamento pendente
    Dado que existe um pedido de processamento pendente para este relatório
    Quando confirmo a alteração
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E nada é gravado

  Cenário: A passagem de conferência não grava nada
    Dado que informei o período e as novas datas
    Quando envio a alteração pela primeira vez
    Então vejo o pedido de confirmação
    E nenhuma data do período é alterada
    E nenhum pedido de processamento é criado
    E nenhum registro de auditoria é gravado

  Cenário: A tela não altera o cadastro do período
    Dado que confirmei a alteração do período
    Quando a tela termina o seu processamento
    Então nenhuma data do cadastro do período foi alterada pela tela
    E ficaram gravados a auditoria e o pedido de processamento

  Cenário: Digitação não numérica
    Dado que informei letras em um dos campos numéricos
    Quando envio a alteração
    Então o sistema recusa a digitação antes de ler qualquer cadastro
    E o cursor volta ao campo recusado

  Cenário: O resultado da passagem anterior não fica na tela
    Dado que a tela já mostrou um período
    Quando envio uma alteração que é recusada
    Então as datas, o tipo de licitação e a razão social da passagem anterior não ficam na tela
```
