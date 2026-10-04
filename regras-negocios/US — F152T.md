# US — F152T — Manter nota fiscal de desconto

## Estória

Como **servidor de CRE que lança a despesa da secretaria**, quero **registrar, alterar,
excluir e consultar a capa da nota fiscal de desconto — número, grupo, fornecedor,
unidade, convênio, datas e valores — e encaminhá-la ao lançamento dos gêneros**, para que
**a nota de desconto entre no sistema presa ao grupo, ao fornecedor, ao convênio e ao valor
certos, e possa receber os itens que a compõem**.

A nota de desconto é a despesa lançada pelo desconto abatido no convênio: é por ela que a
compra entra no sistema e é conferida contra o que foi pago, e é o desconto dela que
compõe o acumulado do convênio daquele fornecedor, que a secretaria usa na prestação de
contas. Sem esta tela a nota não existe: o valor lançado ficaria sem fornecedor e sem
convênio a que se prender, o acumulado do convênio não refletiria o que foi pago, e o
lançamento dos itens não teria por onde começar.

## Contexto

Jornada S000M → F000M → F100M → F152T.
Ator: servidor de CRE — registra e mantém a capa da nota fiscal de desconto e a encaminha
ao lançamento dos gêneros.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A `F152T` não é menu: é a tela da capa da nota fiscal de desconto. As duas telas antes
dela, `F000M` e `F100M`, são menus e **não deixam dado de negócio nenhum para esta tela**:
o contexto que ela usa — a secretaria (o tipo de órgão), o grupo de coordenação regional
(a CRE), a matrícula, o código de acesso e o privilégio — é o que a entrada deixou na
sessão, e a tela apenas o repassa às conferências de rota, de acesso e de permissão.

O cadastro da nota que esta tela mantém é o mesmo que as telas irmãs usam: não há nota
"desta tela". As telas irmãs do mesmo cadastro tratam das notas **sem** desconto e das que
têm desconto **com** recursos próprios; esta trata só das notas **de desconto**, e a
divisão está nas regras abaixo.

O que a tela também aproveita é o que o **lançamento dos gêneros** deixa quando o devolve
ao servidor para lançar outra nota — o grupo, o fornecedor, a unidade, as datas, o
convênio e os valores da nota anterior.

## Regras de negócio

### RN-01 — A tela é a manutenção da capa da nota fiscal de desconto

Esta tela mantém a **capa** da nota fiscal de desconto: o número e o grupo da nota, o
fornecedor, a unidade, as datas de emissão e de entrega, a competência, o convênio e a
instituição beneficiada, o modelo e os dois valores — o total da nota e o desconto. Ela
inclui, altera, exclui e consulta.

A nota é o registro do cadastro de notas fiscais (F155T), que guarda o fornecedor, o tipo
de órgão, o grupo, a unidade (pelo código INEP), o modelo, o convênio e a competência, as
duas datas e **quatro valores** — o total da nota, o total dos gêneros, os recursos
próprios e o desconto. São **20 campos**, e a nota é identificada pela **secretaria (o
tipo de órgão), pelo fornecedor, pelo ano de entrega e pelo número da nota**. Capacidade
de **100.000** notas.

Os **gêneros** da nota — os itens — estão no cadastro (F156T): **13 campos**, capacidade
de **100.000**. O **acumulado do convênio do fornecedor** está no cadastro (F157T), por
órgão, grupo, unidade, competência e fornecedor, com os totais dos gêneros, das notas, dos
descontos e dos recursos próprios: **9 campos**, capacidade de **100.000**. A tela ainda
lê o cadastro dos modelos de nota fiscal (2 campos, capacidade de 100 modelos), o dos
fornecedores (3 campos, 1.000), o das instituições beneficentes (9 campos, 1.000) e o dos
convênios (4 campos, 100.000). Toda operação confirmada de alteração ou exclusão deixa
rastro na auditoria (A010T).

As capacidades acima são **capacidade** — o máximo esperado, parâmetro de dimensionamento
—, não volume cadastrado.

Na tela o servidor vê e digita a operação, o número da nota, o grupo, as duas datas, o ano
de competência, o número e o ano do convênio, o modelo com a sua descrição, o fornecedor
com a razão social, a unidade com o nome do órgão e os dois valores. A **descrição do tipo
de órgão** da sessão e a **data do sistema** também aparecem, mas são informação de saída —
o usuário as vê, o terminal não as devolve — e são apagadas no começo de cada operação.

### RN-02 — A tela abre em inclusão, e a operação é a do campo da tela

Abrindo a tela, ela escreve **inclusão** no campo da operação — venha do menu de despesas,
venha de volta do lançamento dos gêneros. A tela admite **quatro operações**: **inclusão**,
**alteração**, **exclusão** e **consulta**. Uma operação que o sistema não reconheça é
recusada, antes de qualquer leitura, com **\* Operacao nao disponivel \***; com o campo da
operação em branco, a tela não avisa e não faz nada: ela volta a mostrar os mesmos dados —
a permissão conferida nesse caso é a de alteração.

O campo da operação é digitável, e é nele que o servidor escolhe o que vai fazer. A
operação informada no menu que abre a tela não é a que a tela usa: ao abrir, ela escreve
inclusão por cima.

[?] O menu de despesas só deixa passar a consulta: informando inclusão, alteração ou
exclusão nele, a própria conferência de rota do menu recusa com * Operacao nao disponivel *
e o servidor não chega à tela. Chegando pelo menu — que só aceita a consulta, ou o campo
em branco —, a tela abre em inclusão mesmo assim, e a alteração, a exclusão e a própria
consulta só são alcançadas digitando-as já dentro da tela. Se a operação informada no menu
era para valer na tela, pergunta ao site.

### RN-03 — O grupo (CORD.REG.ESCOLAR) é obrigatório, e só vale o do servidor

A nota pertence a um **grupo** de coordenação regional (a CRE): é por ele que a nota é
recortada e é por ele que o acumulado do convênio do fornecedor é somado. Sem grupo
informado, a recusa é **\* Informe o grupo \***; com grupo diferente daquele a que o
servidor está vinculado, **\* Usuario sem acesso a este grupo \***. Nas duas o cursor volta
ao campo do grupo e nada é lido nem gravado. O grupo da sessão é o que a tela escreve no
campo ao abrir.

[?] A conferência do grupo alheio é dispensada quando a sessão não tem grupo definido; e,
nesse caso, a tela aceita o grupo que o servidor digitar e soma o acumulado por ele. Se
quem entra sem grupo deveria operar só o próprio grupo — ou qualquer um —, pergunta ao
site.

### RN-04 — A nota é identificada pela secretaria, pelo fornecedor, pelo ano de entrega e pelo número

A tela procura a nota pela combinação **secretaria da sessão, CNPJ/CPF do fornecedor, ano
de entrega e número da nota** — o grupo não entra nessa identificação, ele é conferido
depois. A secretaria não é digitada: é a da sessão, e a sua descrição aparece na tela.

Na inclusão, o **número da nota fiscal**, o **ano de entrega** e o **CNPJ / CPF do
fornecedor** são obrigatórios: em branco — ou zero —, as recusas são **\* Informe o numero
da nota fiscal \***, **\* Informe o ano de entrega \*** e **\* Informe o CNPJ / CPF do
fornecedor \***, cada uma com o cursor de volta ao campo que falta. Na alteração, na
exclusão e na consulta valem as mesmas três exigências. Com os três informados, procurada
a nota e não estando ela cadastrada, a recusa é **\* Nota fiscal nao cadastrada \***, com
o cursor no número da nota. Em todas elas nada é gravado.

[?] O rótulo da segunda data, na tela, fala de **emissão** da nota fiscal, e as recusas
pedem o **ano de entrega** e a **data de entrega**. As telas irmãs do mesmo cadastro
tratam as duas datas como distintas — há uma de emissão e uma de entrega, e a de entrega
não pode ser anterior à de emissão. Se o rótulo está trocado, ou se as duas datas são a
mesma coisa, pergunta ao site.

### RN-05 — A nota tem de ser do grupo do servidor

Uma nota já cadastrada com a identificação informada só é aceita se for do **grupo do
servidor**. Sendo de outro grupo, a inclusão recusa com **\* Usuario sem acesso ao grupo
desta nota \***, e a alteração, a exclusão e a consulta recusam com **\* Nota ja cadastrada
em outro grupo \*** — nas duas, com o cursor no número da nota e sem gravar nada. Quando a
sessão não tem grupo definido, a conferência é dispensada.

### RN-06 — Esta tela só trata a nota de desconto

A nota que a tela altera, exclui ou consulta precisa ter **desconto** e **nenhuma parcela
de recursos próprios**. Sem desconto — desconto zero —, a recusa é **\* Nota fiscal nao e
de desconto \***; com desconto e com parcela de recursos próprios, é **\* Nota fiscal de
desconto e rec.proprios \***. Nas duas o cursor volta ao número da nota e nada é gravado.
As notas sem desconto e as que têm as duas parcelas não são tratadas aqui: quem as mantém
são as telas irmãs do mesmo cadastro.

### RN-07 — As duas datas são conferidas, uma contra a outra e contra hoje

A capa trabalha com duas datas: a de **emissão** e a de **entrega dos gêneros** (a data da
nota). Cada uma precisa ser uma data completa e válida — dia, mês e ano, com o ano entre
1994 e 2099 — e, além disso:

- a **data de emissão** não pode ser posterior ao dia de hoje;
- o **ano de entrega** tem de ser o mesmo ano da emissão;
- a **data de entrega** não pode ser anterior à data de emissão.

As recusas, na ordem em que o servidor as encontra, são **\* Data de emissao invalida \***,
**\* Data de emissao > que a data atual \***, **\* Data de entrega invalida \***, **\* Ano
de entrega diferente de ano emissao \*** e **\* Data de entrega < que data emissao \***,
cada uma com o cursor de volta a um dos campos de data. O "hoje" dessas conferências é a
data do sistema, a mesma que a tela mostra, e cada recusa deixa a nota parada: nada é
gravado.

### RN-08 — O convênio é obrigatório, e a instituição tem de ser do grupo e da secretaria

O convênio é o instrumento pelo qual a despesa corre, e vem com o seu ano. Em branco, a
recusa é **\* Informe numero do convenio \***, com o cursor no campo do convênio.

Informados o número e o ano, o sistema procura o convênio e, dentro dele, a instituição
beneficente:

- convênio que não existe naquele ano, ou que não tem nenhuma instituição vinculada ao
  **grupo informado**, é recusado com **\* Convenio nao cadastrado \***;
- a instituição vinculada ao convênio precisa estar cadastrada — não estando, a recusa é
  **\* Instituicao beneficente nao cadastrada \***;
- a instituição precisa pertencer à **mesma secretaria** do servidor — não pertencendo,
  **\* Inst.benef nao pertence a esta secretaria \***;
- e, quando o servidor tem grupo, a instituição precisa ser do **grupo dele** — não sendo,
  **\* Usuario sem acesso a outro grupo \***.

Todas devolvem o cursor ao campo do convênio, e nenhuma delas grava.

[?] A última recusa é lida duas vezes: o laço que procura o convênio já exige que a
instituição encontrada seja do grupo informado, e logo antes da recusa a mesma instituição
é lida outra vez, pela mesma chave. Se essa segunda leitura devolve o mesmo registro, a
recusa nunca dispara; se devolve o próximo da chave (a chave do cadastro admite repetição),
ela é alcançável. O que os sinalizadores de leitura do banco fazem não está no corpus lido
nem no manual. Pergunta ao site.

### RN-09 — O modelo da nota fiscal e o fornecedor precisam estar cadastrados

A tela trabalha com um modelo de nota fiscal fixo, que ela mesma assume ao abrir (o modelo
55), e confere se esse modelo está cadastrado: não estando, a recusa é **\* Modelo de nota
fiscal nao cadastrado \***. O fornecedor, identificado pelo CNPJ/CPF informado, também
precisa estar cadastrado: não estando, **\* Fornecedor nao cadastrado \***, com o cursor no
campo do fornecedor. Nada é gravado.

[?] O número do modelo é fixado pela própria tela e não vem de campo informado pelo
servidor; se esse é o modelo único da nota de desconto ou se depende do tipo de despesa,
pergunta ao site.

[?] As descrições que a tela mostra — a razão social do fornecedor, o nome da instituição e
a descrição do modelo — vêm de leituras que **não** recusam quando o registro não existe: o
que fica no campo, nesse caso, não se lê no corpus (o modelo da nota ainda é conferido na
alteração; o fornecedor, não). Pergunta ao site.

### RN-10 — A nota não pode repetir uma já cadastrada

Na inclusão, se já existir nota com a mesma secretaria, o mesmo fornecedor, o mesmo ano de
entrega e o mesmo número, e ela for do grupo do servidor — ou o servidor não tiver grupo —
a recusa é **\* Nota ja cadastrada \***, com o cursor no número da nota, e nada é gravado.

### RN-11 — O valor total da nota e o desconto

O **valor total da nota** é obrigatório — em branco ou zero, **\* Informe o valor total da
nota \*** — e o **desconto** também: desconto zero é tratado como não informado, e a recusa
é **\* Informe o valor do desconto \***. Os dois são valores em dinheiro, com duas casas
decimais, e a vírgula é o separador decimal.

O desconto tem de ser **menor que o valor total**: sendo igual ou maior, a recusa é
**\* Desconto deve ser < valor da nota \***, com o cursor no campo do desconto. E, na
alteração de uma nota que já tem gêneros, o total informado não pode ser menor que o
**total dos gêneros dela menos o desconto**: sendo, a recusa é **\* Vl.total < vl.itens -
desconto \***, com o cursor no valor total.

Todas as recusas desta regra param a operação: nada é gravado.

### RN-12 — A operação é confirmada antes de ser executada

Passando pelas conferências, a tela não executa: ela guarda o que conferiu, mostra a
confirmação — **\* Confirma inclusao da nota <S/N> ? \***, **\* Confirma alteracao da nota
fiscal <S/N> ? \*** ou **\* Confirma exclusao da nota fiscal <S/N> ? \*** —, posiciona o
cursor no campo de resposta e espera. Só a resposta **sim** executa.

Resposta diferente de sim **cancela**: a tela limpa o aviso e o que guardou e volta ao
mesmo ponto, refazendo as conferências e armando a confirmação outra vez. Na inclusão, se
algum dado conferido mudou entre a confirmação e a resposta, a confirmação é desarmada e as
conferências voltam. Na alteração, as conferências de data, de convênio e de valor rodam
**depois** do sim: falhando uma delas, a alteração não acontece e o servidor recomeça do
aviso.

A consulta **não** pede confirmação.

[?] Ao armar a confirmação da alteração, a tela recarrega do cadastro os dados da nota: o
que o servidor tiver digitado de novo nessa mesma resposta é substituído pelo que está
gravado, e a alteração exige uma segunda digitação — a resposta "sim" tem de vir junto com
os valores já corrigidos. Se era para a tela preservar o que foi digitado, pergunta ao
site.

### RN-13 — A inclusão não grava a nota: ela segue para o lançamento dos gêneros

Confirmada a inclusão, esta tela **não grava**: ela passa a nota — grupo, fornecedor,
unidade, modelo, convênio, datas e valores —, com a operação **inclusão**, para o
lançamento dos gêneros (F153T), que abre na mesma operação e é quem grava a nota e os
itens. Nenhuma resposta desta tela, no caminho da inclusão, grava, altera ou apaga cadastro
algum, e nenhum registro de auditoria é gerado por ela.

O lançamento dos gêneros só aceita ser chamado por esta tela: vindo de outro lugar, ele
devolve o servidor ao menu de despesas.

### RN-14 — A alteração grava a nota e refaz o acumulado do convênio do fornecedor

Confirmada, a alteração trava o registro da nota e o regrava com os valores informados, e
deixa na auditoria (A010T) um registro com a operação, o cadastro alterado, a sessão, o
grupo, a matrícula, a estação de trabalho, a data e a hora, o tipo de órgão e as imagens
anterior e nova do registro.

Quando o que mudou mexe no que o convênio acumula — o valor total, o desconto, a
competência ou a unidade —, a tela refaz o **acumulado do convênio do fornecedor**: soma,
de todas as notas do mesmo órgão, grupo, unidade, competência e fornecedor, o total dos
gêneros, o total das notas, o desconto e os recursos próprios, e regrava o acumulado com
essas somas. O acumulado do recorte antigo é refeito e, se a soma dele ficar zerada, é
apagado; o do recorte novo é criado se ainda não existir. Cada uma dessas gravações também
vai para a auditoria.

Se **nenhum** dado da nota mudou, a tela não grava, não audita e **não avisa nada**: a
alteração termina e o servidor segue para os gêneros.

[?] A soma das notas do fornecedor é lida com a chave do cadastro e com o número da nota
**zerado** — uma chave parcial. O que os sinalizadores de leitura do banco fazem
(posicionar, avançar, voltar) não está no corpus lido nem no manual. Se a leitura exigir a
chave inteira, nenhuma nota entra na soma e o acumulado é regravado só com zeros. Pergunta
ao site.

### RN-15 — A exclusão apaga a nota, os gêneros dela e mexe no acumulado do convênio

Confirmada, a exclusão percorre os **gêneros** da nota e apaga um a um, apaga a nota e
refaz o acumulado do convênio do fornecedor **descontando** os valores da nota; ficando o
acumulado zerado, ele é apagado. Cada apagamento e cada gravação deixa registro na
auditoria. Esta é a única operação que apaga alguma coisa nesta tela, e ela exige a mesma
identificação e as mesmas conferências da consulta.

### RN-16 — A consulta não grava nada e mostra os gêneros da nota

Na consulta — que não pede confirmação —, a tela mostra a nota e passa para o lançamento
dos gêneros, que abre em **consulta** e mostra os itens da nota. Nenhum cadastro é gravado,
alterado ou apagado e nenhum registro de auditoria é gerado, ainda que algum campo seja
mudado na tela.

### RN-17 — Sem a secretaria e o grupo da sessão a operação não acontece, e a tela não avisa

A operação confirmada só é executada quando a sessão tem **secretaria** (o tipo de órgão) e
**grupo**. Faltando um dos dois, a tela desarma a confirmação, limpa o aviso e volta, sem
gravar e **sem dizer nada**: o servidor vê a tela de volta, com os mesmos dados, e nada
aconteceu.

[?] A falta de grupo já é recusada antes, com * Informe o grupo *; a falta de secretaria
não tem aviso nenhum. Se a sessão pode chegar a esta tela sem secretaria — e o que o
servidor deveria ver nesse caso —, pergunta ao site.

### RN-18 — Toda operação passa pelas conferências de tela, de acesso e de permissão

A abertura e cada resposta passam pelas conferências comuns do sistema: a tela tem de estar
cadastrada no cadastro de telas — não constando, ou estando desativada, a operação é
abandonada com **\* Tela nao cadastrada \***, pela conferência de rota, ou **\* Tela nao
disponivel \***, pela conferência de acesso; o código de acesso da matrícula tem de ter a
tela autorizada — senão **\* Acesso negado para esta matricula \***; e a operação digitada
tem de constar do perfil da tela — senão **\* Acesso negado para esta operacao \***. É da
mesma conferência que vêm a data e a hora do sistema, que são as usadas nas comparações de
data. A conferência recebe o contexto da sessão: a matrícula, o código de acesso, o
privilégio, a secretaria e o grupo do servidor, além da operação e da tela.

[?] O perfil da tela guarda quatro permissões — inclusão, alteração, exclusão e consulta —,
mas a conferência da consulta não lê a permissão de consulta: quem tem a tela autorizada
consulta sem essa permissão. Se era para exigi-la, o caminho não a exige. Pergunta ao site.

### RN-19 — Os campos de número são editados a cada resposta

A cada resposta, antes de qualquer conferência, a tela edita os seus **14 campos de
número**: o número da nota fiscal, o grupo, o dia, o mês e o ano de emissão, o dia, o mês e
o ano da nota, o ano de competência, o número e o ano do convênio, o código da unidade e os
dois valores. Cada um é tratado como número — o que estiver em branco vira zero e os zeros
à esquerda caem — e reescrito; os dois valores usam a vírgula como separador decimal. No
primeiro campo que não passar pela edição, o cursor volta para ele e a tela não segue.

[?] Dois desses campos — o ano de competência e o código da unidade — são editados, mas não
têm posição de cursor na tabela da tela; recusados na edição, o cursor não é posicionado.
Se isso deixa o servidor sem saber qual campo corrigir, pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Registrar e manter a capa da nota fiscal de desconto

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F152T

  Cenário: A tela abre em inclusão, com o grupo da sessão e o modelo assumidos por ela
    Dado que chego à F152T pelo menu de despesas
    Quando a tela abre
    Então ela está em inclusão
    E o campo do grupo já vem preenchido com o grupo a que estou vinculado
    E o modelo de nota fiscal já vem assumido pela tela
    E nada é gravado

  Cenário: A tela reaberta pelo lançamento dos gêneros volta em inclusão com os dados da nota anterior
    Dado que o lançamento dos gêneros me devolve para lançar outra nota
    Quando a tela F152T abre
    Então ela está em inclusão
    E o grupo, o fornecedor, a unidade, as datas, o convênio e os valores vêm preenchidos com o que aquela tela deixou
    E o número da nota fiscal vem em branco

  Cenário: Inclusão de uma nota de desconto com todos os dados válidos
    Dado que preenchi número, datas, grupo, convênio, instituição, modelo, fornecedor e valores válidos de uma nota que ainda não existe
    E informei a operação de inclusão
    Quando respondo a tela
    Então vejo "* Confirma inclusao da nota <S/N> ? *"
    E respondendo que sim sou levado ao lançamento dos gêneros daquela nota, que abre em inclusão
    E nenhum cadastro foi gravado por esta tela

  Cenário: Alteração de uma nota já cadastrada
    Dado que informei a identificação de uma nota de desconto cadastrada
    E informei a operação de alteração
    Quando respondo a tela
    Então vejo a nota e a pergunta "* Confirma alteracao da nota fiscal <S/N> ? *"
    E respondendo que sim com os valores corrigidos a nota fica com os novos valores
    E o acumulado do convênio do fornecedor é refeito
    E a auditoria registra a alteração

  Cenário: Exclusão de uma nota já cadastrada
    Dado que informei a identificação de uma nota de desconto cadastrada
    E informei a operação de exclusão
    Quando respondo a tela
    Então vejo a pergunta "* Confirma exclusao da nota fiscal <S/N> ? *"
    E respondendo que sim os gêneros da nota são apagados, a nota é apagada e o acumulado do convênio é reduzido
    E a auditoria registra cada apagamento

  Cenário: Consulta de uma nota e dos seus gêneros
    Dado que informei a identificação de uma nota de desconto cadastrada
    E informei a operação de consulta
    Quando respondo a tela
    Então vejo a nota
    E sou levado ao lançamento dos gêneros, que abre em consulta e mostra os itens da nota
    E nada é gravado nem auditado

  Cenário: Operação não reconhecida
    Quando informo uma operação diferente de inclusão, alteração, exclusão e consulta
    Então vejo "* Operacao nao disponivel *"
    E nada é lido nem gravado

  Cenário: Operação em branco
    Quando deixo o campo da operação em branco
    Então a tela volta a mostrar os mesmos dados
    E não vejo aviso nenhum
    E nada é gravado

  Cenário: Grupo não informado
    Dado que deixei o grupo em branco
    Quando respondo a tela
    Então vejo "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nada é gravado

  Cenário: Grupo diferente do meu
    Dado que informei um grupo diferente daquele a que estou vinculado
    Quando respondo a tela
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo do grupo
    E nada é gravado

  Cenário: Número da nota fiscal não informado
    Dado que deixei o número da nota fiscal em branco
    Quando respondo a tela
    Então vejo "* Informe o numero da nota fiscal *"
    E o cursor volta ao campo do número
    E nada é gravado

  Cenário: Ano de entrega não informado
    Dado que informei o número da nota fiscal e deixei o ano de entrega em branco
    Quando respondo a tela
    Então vejo "* Informe o ano de entrega *"
    E o cursor volta ao campo do ano
    E nada é gravado

  Cenário: CNPJ / CPF do fornecedor não informado
    Dado que informei o número da nota e o ano de entrega, e deixei o fornecedor em branco
    Quando respondo a tela
    Então vejo "* Informe o CNPJ / CPF do fornecedor *"
    E o cursor volta ao campo do fornecedor
    E nada é gravado

  Cenário: Nota fiscal não cadastrada
    Dado que informei a identificação de uma nota que não existe para aquela secretaria, aquele fornecedor e aquele ano
    E informei a operação de alteração, de exclusão ou de consulta
    Quando respondo a tela
    Então vejo "* Nota fiscal nao cadastrada *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: Nota de outro grupo na alteração, na exclusão ou na consulta
    Dado que a nota informada pertence a outro grupo
    E informei a operação de alteração, de exclusão ou de consulta
    Quando respondo a tela
    Então vejo "* Nota ja cadastrada em outro grupo *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: Nota de outro grupo na inclusão
    Dado que já existe nota com a mesma secretaria, fornecedor, ano e número, em outro grupo
    E informei a operação de inclusão
    Quando respondo a tela
    Então vejo "* Usuario sem acesso ao grupo desta nota *"
    E nada é gravado

  Cenário: Nota sem desconto
    Dado que a nota informada está cadastrada sem desconto
    Quando respondo a tela
    Então vejo "* Nota fiscal nao e de desconto *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: Nota de desconto e de recursos próprios
    Dado que a nota informada está cadastrada com desconto e com parcela de recursos próprios
    Quando respondo a tela
    Então vejo "* Nota fiscal de desconto e rec.proprios *"
    E nada é gravado

  Cenário: Data de emissão inválida
    Dado que informei uma data de emissão que não existe, ou com o ano fora de 1994 a 2099
    Quando respondo a tela
    Então vejo "* Data de emissao invalida *"
    E o cursor volta ao campo da data de emissão
    E nada é gravado

  Cenário: Data de emissão posterior a hoje
    Dado que informei uma data de emissão depois do dia de hoje
    Quando respondo a tela
    Então vejo "* Data de emissao > que a data atual *"
    E o cursor volta ao campo da data de emissão
    E nada é gravado

  Cenário: Data de entrega inválida
    Dado que informei uma data de entrega que não existe, ou com o ano fora de 1994 a 2099
    Quando respondo a tela
    Então vejo "* Data de entrega invalida *"
    E o cursor volta ao campo da data de entrega
    E nada é gravado

  Cenário: Ano de entrega diferente do ano de emissão
    Dado que o ano da data de entrega é diferente do ano da data de emissão
    Quando respondo a tela
    Então vejo "* Ano de entrega diferente de ano emissao *"
    E nada é gravado

  Cenário: Data de entrega anterior à data de emissão
    Dado que informei a data de entrega antes da data de emissão
    Quando respondo a tela
    Então vejo "* Data de entrega < que data emissao *"
    E nada é gravado

  Cenário: Convênio não informado
    Dado que deixei o número do convênio em branco
    Quando respondo a tela
    Então vejo "* Informe numero do convenio *"
    E o cursor volta ao campo do convênio
    E nada é gravado

  Cenário: Convênio não cadastrado no ano informado, ou sem instituição no grupo
    Dado que informei um convênio que não existe naquele ano, ou que não tem instituição vinculada ao grupo informado
    Quando respondo a tela
    Então vejo "* Convenio nao cadastrado *"
    E o cursor volta ao campo do convênio
    E nada é gravado

  Cenário: Instituição beneficente não cadastrada
    Dado que a instituição vinculada ao convênio não está cadastrada
    Quando respondo a tela
    Então vejo "* Instituicao beneficente nao cadastrada *"
    E nada é gravado

  Cenário: Instituição beneficente de outra secretaria
    Dado que a instituição vinculada ao convênio pertence a outra secretaria
    Quando respondo a tela
    Então vejo "* Inst.benef nao pertence a esta secretaria *"
    E nada é gravado

  Cenário: Modelo de nota fiscal não cadastrado
    Dado que o modelo de nota fiscal que a tela assume não está cadastrado
    Quando respondo a tela
    Então vejo "* Modelo de nota fiscal nao cadastrado *"
    E nada é gravado

  Cenário: Fornecedor não cadastrado
    Dado que informei um CNPJ / CPF de fornecedor que não está cadastrado
    Quando respondo a tela
    Então vejo "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo do fornecedor
    E nada é gravado

  Cenário: Nota já cadastrada
    Dado que já existe uma nota com a mesma secretaria, fornecedor, ano de entrega e número, no meu grupo
    E informei a operação de inclusão
    Quando respondo a tela
    Então vejo "* Nota ja cadastrada *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: Valor total da nota não informado
    Dado que deixei o valor total da nota em branco
    Quando respondo a tela
    Então vejo "* Informe o valor total da nota *"
    E o cursor volta ao campo do valor
    E nada é gravado

  Cenário: Desconto não informado
    Dado que informei o valor total da nota e deixei o desconto em branco
    Quando respondo a tela
    Então vejo "* Informe o valor do desconto *"
    E o cursor volta ao campo do desconto
    E nada é gravado

  Cenário: Desconto igual ou maior que o valor da nota
    Dado que informei um desconto igual ou maior que o valor total da nota
    Quando respondo a tela
    Então vejo "* Desconto deve ser < valor da nota *"
    E o cursor volta ao campo do desconto
    E nada é gravado

  Cenário: Total menor que os gêneros menos o desconto
    Dado que a nota já tem gêneros
    E informei um valor total menor que o total dos gêneros dela menos o desconto
    Quando peço a alteração
    Então vejo "* Vl.total < vl.itens - desconto *"
    E o cursor volta ao campo do valor total
    E nada é gravado

  Cenário: Resposta negativa à confirmação
    Dado que a tela me pediu a confirmação de uma inclusão
    Quando respondo que não
    Então o aviso é limpo
    E a tela volta a conferir os mesmos dados
    E me pede a confirmação outra vez
    E nada é gravado

  Cenário: Alteração sem nenhum dado mudado
    Dado que consultei uma nota e peço a alteração sem mudar nada
    Quando confirmo
    Então a tela não mostra aviso nenhum
    E a nota continua como estava
    E o acumulado do convênio não é regravado
    E nenhum registro de auditoria é gerado

  Cenário: A consulta não grava nada
    Dado que consultei uma nota
    E mudo o desconto mostrado na tela
    Quando peço a consulta
    Então a nota continua com o desconto que estava gravado
    E nenhum gênero e nenhum acumulado de convênio é alterado
    E nenhum registro de auditoria é gerado

  Cenário: A operação sem a secretaria na sessão não acontece, e a tela não avisa
    Dado que a minha sessão não tem secretaria
    E confirmei uma inclusão de nota
    Quando respondo a tela
    Então a tela volta a mostrar os mesmos dados
    E não vejo aviso nenhum
    E nenhum cadastro foi gravado

  Cenário: Campo de número recusado na edição
    Dado que informei letras em um dos campos de número da tela
    Quando respondo a tela
    Então a edição recusa aquele campo
    E o cursor volta ao primeiro campo recusado
    E a tela não segue
    E nada é gravado

  Cenário: A tela não consta do cadastro de telas
    Dado que a tela F152T não consta do cadastro de telas, ou está desativada
    Quando abro a tela F152T
    Então sou avisado de que a tela não está disponível
    E não consigo operar

  Cenário: Meu código de acesso não tem a tela
    Dado que o meu código de acesso não tem a tela F152T liberada
    Quando abro a tela F152T
    Então vejo "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Sem permissão para a operação
    Dado que o perfil da tela não libera a operação que informei
    Quando respondo a tela
    Então vejo "* Acesso negado para esta operacao *"
    E nada é lido nem gravado
```
