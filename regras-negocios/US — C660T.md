# US — C660T — Lançamento dos grupamentos de licitação do tipo de contrato

## Estória

Como **servidor de CRE**, quero **lançar e manter o grupamento de licitação de um tipo
de contrato — o fornecedor, o grupo, o período, os valores e, linha a linha, os gêneros
com a quantidade e o preço — e confirmar a atualização desse cadastro**, para que **o
tipo de contrato ganhe a permissão, o contrato e o período com que a coordenadoria vai
licitar e comprar, já conferidos contra a tabela de preço da época**.

O grupamento é o passo que antecede a permissão de contrato: é ele que reúne, para um
tipo de contrato e um grupo de licitação, o fornecedor, o período e a lista de gêneros
com que a coordenadoria vai operar. Enquanto ele não é confirmado, a licitação não tem
fornecedor nem preço por gênero. Confirmado, ele **gera** a permissão de contrato, o
contrato e o período — e **apaga as suas próprias linhas**, porque deixaram de ser
necessárias.

Sem esta tela, o cadastro do período fica pela metade: ou existem gêneros sem grupo e
sem preço, ou existem permissões apontando para um contrato que nunca foi gerado.

## Contexto

Jornada S000M → C000M → C050M → C060M → C660T.
Ator: servidor de CRE — informa o grupamento de licitação de um tipo de contrato,
consulta o que já está lançado, mantém as linhas de gênero e confirma a atualização do
cadastro.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O C000M, o C050M e o C060M são menus e não gravam nada: eles apenas encaminham. O
contexto que a C660T usa — matrícula, código de acesso, privilégio, tipo de órgão e
coordenadoria regional — é o que a entrada deixou na sessão. A C660T é o **fim da
jornada**: ela não passa registro nem operação para nenhuma tela seguinte.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela lança o grupamento de licitação de um tipo de contrato

O grupamento de licitação é o cadastro que a tela mantém. No cabeçalho ele identifica a
**coordenadoria regional**, o **tipo de contrato**, o **fornecedor** (com a razão
social), o **grupo de licitação**, o **período inicial** e o **período limite**, o
**valor homologado**, o **valor adjudicado**, as **datas de início e de fim da tabela
de referência**, o **tipo de licitação** (com a sua descrição) e o **operador do
contrato**.

O grupo de linhas tem **8 linhas**. Cada linha traz a **subclasse**, o **gênero** (com
a sua descrição), o **sinal** do percentual, a **quantidade inicial**, o **valor
inicial**, o **preço fixo**, a **indicação de identificação dos órgãos** e a **situação
da linha**. O cabeçalho mostra ainda a descrição do tipo de órgão e a data do sistema.

A tela **completa** esses dados com os cadastros: a razão social vem do cadastro de
fornecedores; a descrição do tipo de licitação, do cadastro de tipos de licitação; o
período, do cadastro de períodos do tipo de contrato com o grupo; o nome do operador,
do cadastro de operadores; a descrição do gênero, do cadastro de gêneros; e, no
cabeçalho, o tipo de quinzena do contrato (**Quinzena Normal**, **Quinzena Especial** ou
**Valor Fixo**), do cadastro do tipo de contrato.

Uma **permissão de contrato** de mesma chave é o que se chama, aqui, de "cadastro já
atualizado": ela é o produto desta tela, não o que ela mantém. A tela mantém o
grupamento (`C661T`) e, na atualização, gera a permissão de contrato (`C061T`), o
contrato (`C691T`) e o período do contrato (`C138T`).

### RN-02 — A opção de manutenção: sem opção, inclusão; fora de INC, ALT e CON, recusa

A tela aceita **inclusão (INC)**, **alteração (ALT)** e **consulta (CON)**. Quando a
opção chega em branco, a apresentação da tela a assume como **inclusão**. Informando
qualquer outra opção, a tela recusa com
**\* Opcao nao disponivel. Use INC, ALT ou CON \*** e devolve o cursor ao campo da
opção, sem ler e sem gravar nada.

O tratamento da tela também prevê uma operação de exclusão da permissão, mas ela não
passa por esta conferência: pela tela, a exclusão da permissão inteira não acontece. O
que existe é a exclusão de **uma linha** do grupamento, pela situação da linha (RN-13).

[?] A inclusão assumida quando a opção chega em branco é feita **na apresentação** da
tela. Na apresentação transacional — a que o acervo descreve como tela de transação — o
programa não preenche a opção em branco e a mesma conferência que recusa as outras
opções recusaria a opção vazia. Ou o terminal sempre manda a opção preenchida, ou as
duas apresentações da mesma tela se comportam de modo diferente. Pergunta ao site.

[?] A recusa manda usar "INC", "ALT" e "CON", mas as opções que o programa reconhece
valem **ADD**, **CHG** e **INQ** — e existem ainda **DEL** e **PUR**, que esta tela não
aceita. Nenhum literal "INC", "ALT" ou "CON" existe no corpus lido. Ou o formulário
traduz o que o servidor digita, ou quem seguir a mensagem é recusado. Pergunta ao site.

### RN-03 — O servidor só opera na coordenadoria dele

Quando a sessão tem **coordenadoria regional** definida, o servidor só opera na
coordenadoria dele: informando outra, a tela recusa com
**\* Usuario sem acesso a este grupo \***, com o cursor no campo da coordenadoria, e
nada é lido nem gravado. Sem coordenadoria na sessão, a tela aceita qualquer uma.

[?] O valor com que a coordenadoria informada é comparada não é preenchido por nenhuma
tela desta jornada: ele só é preenchido por telas de outro módulo do sistema, fora desta
trilha. Se ele chega zerado, a guarda recusa **toda** coordenadoria informada para o
servidor cuja sessão tem coordenadoria, e o único valor aceito é o zero, que não é
coordenadoria cadastrada. Ou o valor vem preenchido de fora da jornada, ou a tela está
inutilizável para esse servidor. Pergunta ao site.

### RN-04 — A inclusão exige o grupo, o tipo de contrato, o período e a liberação da licitação

Para incluir, a tela confere, nesta ordem:

| o que tem de existir | a recusa |
| --- | --- |
| a **coordenadoria regional**, no cadastro de coordenadorias | **\* Grupo nao cadastrado \*** |
| o **tipo de contrato**, no cadastro de tipos de contrato | **\* Tipo de Contrato nao cadastrado \*** |
| o **período**, no cadastro de períodos daquele tipo de contrato com aquele grupo de licitação | **\* Periodo nao cad. para este TC/grupamento \*** |
| a **liberação desta tela para o tipo de licitação** do período | **\* Tela nao disponivel para esta licitacao \*** |

Cada recusa devolve o cursor ao campo culpado e interrompe a transação antes de
qualquer gravação. O **início do período** não é digitado: ele vem do cadastro do
período.

### RN-05 — A inclusão exige o fornecedor ativo, o grupo vigente e o cadastro ainda não atualizado

Ainda na inclusão: o **fornecedor** tem de estar cadastrado e não estar marcado como
excluído (**\* Fornecedor nao cadastrado \***); e o **grupo de licitação** tem de ter a
sua vigência cadastrada alcançando o período informado — sem vigência nenhuma, a recusa
é **\* Grupamento invalido \***; com a vigência do grupo começando depois do início do
período, **\* Grupamento invalido no periodo \***.

E o tipo de contrato **não pode já ter a permissão atualizada**: havendo permissão de
contrato para aquele grupamento e período, a inclusão é recusada com
**\* Cadastro ja atualizado. Utilize C060T \*** — que manda o servidor para a tela que
mantém a permissão de contrato (`C060T`), porque a partir daí o grupamento não é mais o
caminho.

### RN-06 — O grupo de licitação não pode estar lançado para outro fornecedor no mesmo período

Antes de incluir, a tela varre os grupamentos daquela coordenadoria, tipo de contrato e
período com o **mesmo grupo de licitação**: se encontrar um pertencente a **outro
fornecedor**, recusa com **\* <- Grupamento ja cad.para outro fornecedor \***. O mesmo
cuidado volta na atualização do cadastro, com outra mensagem (RN-15).

[?] A leitura que procura esse grupamento informa a chave **pela metade** — sem o
fornecedor e sem o grupo de licitação — e depois compara o que voltou. Se o
posicionamento da leitura exige a chave inteira, a varredura encontra qualquer
grupamento do período; se ele apenas posiciona no primeiro registro igual ou posterior,
ela varre a partir do primeiro. O acervo não define esse posicionamento, e é dele que
depende o alcance desta recusa. Pergunta ao site.

### RN-07 — Os valores e as datas da tabela têm de bater com o que está cadastrado

Havendo grupamento daquele mesmo fornecedor para o período, a tela **compara** o que foi
informado com o que está gravado, e cada divergência tem a sua recusa:

**\* Valor Homologado difere do cadastrado \***,
**\* Valor Adjudicado difere do cadastrado \***,
**\* Dt.Ini.Refer difere da cadastrada \*** e
**\* Dt.Fim.Refer difere da cadastrada \***.

O que veio em branco é completado com o que está cadastrado, e não é divergência.

### RN-08 — A inclusão exige os valores e o período da tabela antes do início do contrato

Na inclusão, o **valor homologado** e o **valor adjudicado** são de preenchimento
obrigatório: **\* Informe o valor homologado \*** e
**\* Informe o valor adjudicado \***. O **valor adjudicado** não pode ser maior que o
**valor homologado**: **\* Valor adjudicado maior que valor homologado \***.

E a **data de início da tabela de referência** não pode ser posterior ao **início do
período** do grupamento: **\* Tabela de referencia maior que data de inicio \***.

### RN-09 — A tabela de preço do período tem de existir

A tela escolhe a tabela de preço que vai conferir o preço de cada gênero:

- quando as datas de início e de fim da tabela informadas **coincidem**, a **tabela
  especial**;
- quando não coincidem, a **tabela de referência** do contrato; e
- quando a quinzena do tipo de contrato é a **especial**, também a **tabela especial**.

Não existindo a tabela escolhida, a recusa é
**\* Tabela de referencia nao cadastrada \*** ou **\* Tabela especial nao cadastrada \***.

### RN-10 — A inclusão de cada linha exige o gênero, o grupo e o preço

Cada linha preenchida passa por uma bateria própria. O **gênero** tem de estar
cadastrado e **ativo** (**\* Genero nao cadastrado \***); não pode estar **já no
grupamento** (**\* Genero ja cadastrado nesta permissao \***); e o grupo de licitação
a que o gênero pertence tem de ser o **grupo informado no cabeçalho**
(**\* Genero nao cadastrado neste grupamento \***).

O **preço** da linha vem da tabela do período (RN-09), procurando o gênero nas
vigências da tabela: sem preço cadastrado para aquele gênero, a recusa é
**\* Genero sem preco na tabela de referencia \*** ou
**\* Genero sem preco na tabela especial \***.

### RN-11 — A inclusão de cada linha exige quantidade, sinal e identificação dos órgãos

Ainda por linha: a **quantidade inicial** é obrigatória
(**\* Informe a quantidade \***); o **sinal** tem de dizer se o percentual é desconto ou
acréscimo, com `-` ou `+`
(**\* Informe se desconto ou acrescimo com - ou + \***); e o sinal não pode contrariar o
que o grupamento já usa — o grupamento inteiro é de desconto **ou** de acréscimo, e a
linha divergente é recusada com **\* Permissao com desconto \*** ou
**\* Permissao com acrescimo \***. A **indicação de identificação dos órgãos**, se
preenchida, só pode ser `I` (**\* Informe I para identificacao dos Orgaos \***); em
branco, ela é aceita.

Passando por tudo, a linha é gravada no grupamento com o **valor inicial** calculado a
partir da quantidade e do preço — já com o desconto ou o acréscimo — e a operação entra
na auditoria. A linha **não é gravada** quando o grupamento já tem aquele gênero: nesse
caso a conferência anterior já recusou.

### RN-12 — A alteração só depois da consulta, e não muda grupo nem período

A alteração exige que o servidor tenha **consultado antes** aquele mesmo grupamento,
com o mesmo cabeçalho (coordenadoria, tipo de contrato, período limite, fornecedor e
grupo de licitação): sem isso, a recusa é **\* Consulte antes de atualizar \***, com o
cursor no campo da opção. É a consulta que deixa na sessão a marca de qual grupamento
foi visto, e é essa marca que libera a alteração seguinte.

Na alteração também **não se muda** o **grupo de licitação**
(**\* Nao altere o grupamento \***) nem o **período limite**, que se muda na tela de
vigência (**\* Altere o periodo na tela de vigencia \***). O grupo, o tipo de contrato e
o fornecedor são reconferidos nos cadastros (**\* Grupo nao cadastrado \***,
**\* Tipo de Contrato nao cadastrado \***, **\* Fornecedor nao cadastrado \***), a
operação é recusada se já existir permissão com aqueles dados
(**\* Ja existe permissao com estes dados \***), e a tabela de referência continua tendo
de existir (**\* Tabela de referencia nao cadastrada \***).

### RN-13 — Na alteração, a situação da linha decide o que fazer com ela

Em cada linha, a **situação** decide a operação: **I** inclui o gênero, **A** altera e
**E** exclui. Na alteração, a linha que inclui passa pelas mesmas conferências da
inclusão (RN-10 e RN-11); a linha que altera ou exclui tem conferências próprias:

| a linha altera ou exclui | a recusa |
| --- | --- |
| sem a subclasse informada | **\* Atualize linha preenchida \*** |
| com gênero que não existe ou não está **ativo** | **\* Genero nao cadastrado \*** |
| com gênero que **não está** naquele grupamento | **\* Genero nao cadastrado nesta permissao \*** |

E a linha que **altera** tem ainda de trazer a quantidade
(**\* Informe a quantidade \***), o sinal de desconto ou acréscimo
(**\* Informe se desconto ou acrescimo com - ou + \***) e a identificação dos órgãos
reconferida (**\* Informe I para identificacao dos Orgaos \***); e o **sinal não pode
ser trocado** em relação ao que está gravado — trocá-lo de acréscimo para desconto
recusa com **\* Nao altere sinal do acrescimo \***, e no sentido contrário com
**\* Nao altere sinal do desconto \***.

A linha que **exclui** apaga aquele gênero do grupamento, com rastro na auditoria.

### RN-14 — A consulta lista o grupamento e não grava nada

Na consulta, a tela procura o grupamento pela **coordenadoria**, **tipo de contrato**,
**período limite** e **grupo de licitação** informados — o **fornecedor** é opcional: em
branco, ele vem do próprio grupamento. Achando, ela carrega o cabeçalho e as linhas na
sessão e marca que **aquele** grupamento foi consultado (é essa marca que libera a
alteração seguinte); se o tipo de licitação do grupamento não libera esta tela, recusa
com **\* Tela nao disponivel para esta licitacao \***.

Não achando grupamento para o cabeçalho, recusa com **\* Permissao nao cadastrada \***,
com o cursor na coordenadoria.

A consulta **não grava nada**: nenhuma linha é incluída, alterada ou excluída, e nenhuma
trilha de operação é gerada.

[?] Duas mensagens cobrem o caso de não haver grupamento para o cabeçalho: **\*
Permissao nao cadastrada \***, na conferência, e **\* Permissao sem registros no arquivo
auxiliar \***, na apresentação da tela. Como a apresentação que mostra a segunda só
roda depois de a conferência ter encerrado a transação, o acervo não deixa claro em qual
das duas o servidor esbarra. Pergunta ao site.

### RN-15 — A confirmação da atualização do cadastro

Há uma segunda operação nesta tela, disparada por uma **marca de atualização** que
chega junto com a tela: com a marca posta, a tela **não** valida linha a linha — ela
confirma a **atualização do cadastro** do tipo de contrato contra o que já está gravado.
As recusas dessa confirmação são:

| o que a confirmação recusa | a mensagem |
| --- | --- |
| não há grupamento lançado para o cabeçalho | **\* Permissao nao cadastrada \*** |
| já existe permissão de contrato para o grupamento e o período | **\* Permissao ja atualizada. Use outro TC \*** |
| a permissão já está nos mesmos limites do grupamento | **\* Permissao ja atualizada \*** |
| a permissão do intervalo é de **outro fornecedor** | **\* Grupamento cadastrado para outro fornecedor \*** |
| já existe permissão **no intervalo** do grupamento | **\* Ja existe permissao neste intervalo \*** |
| a soma dos valores iniciais dos gêneros não fecha com o valor adjudicado | **\* Nao atualize.Soma qt.ini generos difere vl.adj \*** |

Quando algum gênero do grupamento está **sem desconto**, a atualização pede uma
confirmação a mais — **\* Confirma genero sem desconto ? \*** — e só segue se a
confirmação vier marcada. Passando por tudo, a atualização segue para a RN-16.

[?] A marca de atualização é um dado da tela que o programa **nunca atribui**: ele só a
lê, a mostra e a limpa. Não está no material lido qual campo da máscara a preenche, nem
se é o servidor que a marca. Pergunta ao site.

### RN-16 — Confirmada, a tela gera a permissão, o contrato e o período, e consome o grupamento

A atualização percorre **as linhas do grupamento** e, para cada uma: regrava a
**permissão de contrato** com os dados do grupamento; registra dois movimentos (um com o
valor anterior e o posterior, outro com a quantidade); e, para o contrato daquela
coordenadoria, tipo de contrato, período e fornecedor, **gera o contrato** (se ainda não
existir) e **o período do contrato** (se ainda não existir). Quando o gênero está
marcado com a **indicação de identificação dos órgãos**, gera também o registro de
identificação. Feito isso, **apaga a linha do grupamento** que serviu de base, e ao fim
acerta, no contrato, a prioridade de dois dígitos do tipo de contrato. A tela fecha com
o aviso **Cadastro Atualizado**, e cada passo fica na auditoria.

Quando o **tipo de licitação do grupamento é o código 99**, a atualização vai além: ela
cria, a partir das permissões existentes, as linhas do grupamento do período anterior ao
início da permissão, com o mesmo preço e a mesma quantidade.

[?] A atualização só é processada na **primeira** das 8 linhas da tela: o tratamento
abandona as outras. Como quem escolhe a linha da transação é o terminal, não concluo se
o servidor consegue confirmar a partir de outra linha. Pergunta ao site.

[?] O período do grupamento criado no caso do código **99** vem de uma conversão de data
do dialeto, chamada com sinal de menos e incremento 1, e o resultado vira ano, mês e dia
do novo período. O corpus não define essa conversão: se o período novo é o anterior ao
da permissão, o mesmo, ou um dia antes dele, não concluo. O significado de negócio do
código 99 também não está no material lido. Pergunta ao site.

### RN-17 — Toda operação fica registrada na auditoria

Cada gravação de linha — inclusão, alteração ou exclusão — e cada passo da atualização
do cadastro deixam um registro de auditoria com a tela de origem, a operação, o valor
anterior, o valor posterior, a matrícula do funcionário, a estação, o número do
processo, a sessão (dia, mês, ano e hora) e o tipo de órgão.

---

## Cenários BDD

```gherkin
Funcionalidade: Lançamento dos grupamentos de licitação do tipo de contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C660T

  Cenário: RN-01 — abrir a tela com o grupamento já lançado
    Dado que existe grupamento lançado para a coordenadoria, tipo de contrato, período, fornecedor e grupo
    Quando abro a C660T
    Então vejo o cabeçalho com o grupo, o fornecedor, o período, os valores e as datas da tabela
    E vejo até 8 linhas, cada uma com subclasse, gênero, sinal, quantidade, valor inicial, preço fixo e situação
    E vejo a descrição do tipo de licitação, o operador e a quinzena do contrato
    E nada é gravado

  Cenário: RN-02 — sem opção informada, a tela assume a inclusão
    Dado que não informo a opção de manutenção
    Quando confirmo o cabeçalho
    Então a tela trata a operação como inclusão

  Cenário: RN-02 — opção de manutenção indisponível
    Quando informo uma opção de manutenção diferente de INC, ALT e CON
    Então vejo a mensagem "* Opcao nao disponivel. Use INC, ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: RN-03 — coordenadoria diferente da da minha sessão
    Dado que a minha sessão está presa a uma coordenadoria regional
    Quando informo outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E nada é gravado

  Cenário: RN-03 — coordenadoria igual à da minha sessão
    Dado que a minha sessão está presa a uma coordenadoria regional
    Quando informo a mesma coordenadoria
    Então a tela segue para as conferências seguintes

  Cenário: RN-04 — coordenadoria não cadastrada
    Quando informo uma coordenadoria que não existe
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E nada é gravado

  Cenário: RN-04 — tipo de contrato não cadastrado
    Quando informo um tipo de contrato que não existe
    Então vejo a mensagem "* Tipo de Contrato nao cadastrado *"
    E nada é gravado

  Cenário: RN-04 — período não cadastrado para o tipo de contrato e grupo
    Quando informo um período que não existe para aquele tipo de contrato e grupo
    Então vejo a mensagem "* Periodo nao cad. para este TC/grupamento *"
    E nada é gravado

  Cenário: RN-04 — tela não liberada para a licitação
    Dado que esta tela não está liberada para a licitação do período
    Quando tento incluir
    Então vejo a mensagem "* Tela nao disponivel para esta licitacao *"
    E nada é gravado

  Cenário: RN-05 — fornecedor não cadastrado ou excluído
    Quando informo um fornecedor que não existe, ou que está marcado como excluído
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E nada é gravado

  Cenário: RN-05 — grupo de licitação sem vigência
    Dado que o grupo de licitação não tem vigência cadastrada
    Quando tento incluir
    Então vejo a mensagem "* Grupamento invalido *"
    E nada é gravado

  Cenário: RN-05 — vigência do grupo posterior ao início do período
    Dado que a vigência do grupo começa depois do início do período informado
    Quando tento incluir
    Então vejo a mensagem "* Grupamento invalido no periodo *"
    E nada é gravado

  Cenário: RN-05 — cadastro já atualizado
    Dado que já existe permissão de contrato para aquele grupamento e período
    Quando tento incluir
    Então vejo a mensagem "* Cadastro ja atualizado. Utilize C060T *"
    E nada é gravado

  Cenário: RN-06 — grupamento do período já pertence a outro fornecedor
    Dado que o grupo de licitação daquele período já está lançado para outro fornecedor
    Quando tento incluir
    Então vejo a mensagem "<- Grupamento ja cad.para outro fornecedor *"
    E nada é gravado

  Cenário: RN-07 — valor homologado diferente do cadastrado
    Dado que já existe grupamento do mesmo fornecedor naquele período
    Quando informo um valor homologado diferente do cadastrado
    Então vejo a mensagem "* Valor Homologado difere do cadastrado *"
    E nada é gravado

  Cenário: RN-07 — valor adjudicado diferente do cadastrado
    Dado que já existe grupamento do mesmo fornecedor naquele período
    Quando informo um valor adjudicado diferente do cadastrado
    Então vejo a mensagem "* Valor Adjudicado difere do cadastrado *"
    E nada é gravado

  Cenário: RN-07 — datas da tabela diferentes das cadastradas
    Dado que já existe grupamento do mesmo fornecedor naquele período
    Quando informo datas da tabela de referência diferentes das cadastradas
    Então vejo a mensagem "* Dt.Ini.Refer difere da cadastrada *" ou "* Dt.Fim.Refer difere da cadastrada *"
    E nada é gravado

  Cenário: RN-07 — campo em branco é completado pelo cadastro
    Dado que já existe grupamento do mesmo fornecedor naquele período
    Quando deixo um valor ou uma data da tabela em branco
    Então a tela completa o campo com o que está cadastrado
    E segue sem recusar

  Cenário: RN-08 — valor homologado em branco
    Quando deixo o valor homologado em branco
    Então vejo a mensagem "* Informe o valor homologado *"
    E nada é gravado

  Cenário: RN-08 — valor adjudicado em branco
    Quando deixo o valor adjudicado em branco
    Então vejo a mensagem "* Informe o valor adjudicado *"
    E nada é gravado

  Cenário: RN-08 — valor adjudicado maior que o homologado
    Quando informo um valor adjudicado maior que o valor homologado
    Então vejo a mensagem "* Valor adjudicado maior que valor homologado *"
    E nada é gravado

  Cenário: RN-08 — início da tabela depois do início do período
    Quando informo a data de início da tabela de referência depois do início do período
    Então vejo a mensagem "* Tabela de referencia maior que data de inicio *"
    E nada é gravado

  Cenário: RN-09 — tabela de preço do período não cadastrada
    Dado que a tabela de preço escolhida para o período não está cadastrada
    Quando tento incluir
    Então vejo a mensagem "* Tabela de referencia nao cadastrada *" ou "* Tabela especial nao cadastrada *"
    E nada é gravado

  Cenário: RN-10 — gênero não cadastrado ou inativo
    Quando informo na linha um gênero que não existe, ou que não está ativo
    Então vejo a mensagem "* Genero nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — gênero já lançado no grupamento
    Dado que aquele gênero já está no grupamento
    Quando tento incluí-lo de novo
    Então vejo a mensagem "* Genero ja cadastrado nesta permissao *"
    E nada é gravado

  Cenário: RN-10 — gênero de outro grupo de licitação
    Dado que o gênero pertence a um grupo de licitação diferente do informado no cabeçalho
    Quando tento incluí-lo
    Então vejo a mensagem "* Genero nao cadastrado neste grupamento *"
    E nada é gravado

  Cenário: RN-10 — gênero sem preço na tabela do período
    Dado que o gênero não tem preço cadastrado na tabela do período
    Quando tento incluir a linha
    Então vejo a mensagem "* Genero sem preco na tabela de referencia *" ou "* Genero sem preco na tabela especial *"
    E nada é gravado

  Cenário: RN-11 — quantidade da linha em branco
    Quando deixo a quantidade da linha em branco
    Então vejo a mensagem "* Informe a quantidade *"
    E nada é gravado

  Cenário: RN-11 — sinal da linha em branco ou inválido
    Quando deixo o sinal em branco, ou informo algo diferente de - e +
    Então vejo a mensagem "* Informe se desconto ou acrescimo com - ou + *"
    E nada é gravado

  Cenário: RN-11 — sinal contrário ao do grupamento
    Dado que o grupamento é de desconto
    Quando informo uma linha de acréscimo
    Então vejo a mensagem "* Permissao com desconto *"
    E nada é gravado

  Cenário: RN-11 — linha de acréscimo num grupamento de desconto, no outro sentido
    Dado que o grupamento é de acréscimo
    Quando informo uma linha de desconto
    Então vejo a mensagem "* Permissao com acrescimo *"
    E nada é gravado

  Cenário: RN-11 — indicação de identificação dos órgãos inválida
    Quando preencho a indicação de identificação dos órgãos com algo diferente de I
    Então vejo a mensagem "* Informe I para identificacao dos Orgaos *"
    E nada é gravado

  Cenário: RN-11 — inclusão de uma linha do grupamento
    Dado que o gênero existe, está ativo, pertence ao grupo informado e tem preço na tabela
    Quando incluo a linha com a quantidade, o sinal e a identificação dos órgãos válidos
    Então a linha é gravada no grupamento com o valor inicial calculado
    E a operação fica registrada na auditoria

  Cenário: RN-12 — alteração sem consultar antes
    Dado que não consultei antes aquele grupamento
    Quando tento alterar
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E nada é gravado

  Cenário: RN-12 — alteração do grupo de licitação
    Dado que consultei o grupamento antes
    Quando tento mudar o grupo de licitação
    Então vejo a mensagem "* Nao altere o grupamento *"
    E nada é gravado

  Cenário: RN-12 — alteração do período limite
    Dado que consultei o grupamento antes
    Quando tento mudar o período limite
    Então vejo a mensagem "* Altere o periodo na tela de vigencia *"
    E nada é gravado

  Cenário: RN-12 — já existe permissão com aqueles dados
    Dado que já existe permissão com os dados informados
    Quando tento alterar
    Então vejo a mensagem "* Ja existe permissao com estes dados *"
    E nada é gravado

  Cenário: RN-12 — alterar uma linha do grupamento
    Dado que consultei o grupamento e o gênero existe nele
    Quando informo a situação A com a quantidade e o sinal já gravados
    Então a linha é regravada com o novo valor
    E a operação fica registrada na auditoria

  Cenário: RN-13 — linha de alteração ou exclusão sem subclasse
    Dado que a linha tem situação A ou E e nenhuma subclasse informada
    Quando tento alterar
    Então vejo a mensagem "* Atualize linha preenchida *"
    E nada é gravado

  Cenário: RN-13 — linha de alteração com gênero fora do grupamento
    Dado que a linha tem situação A e o gênero não está naquele grupamento
    Quando tento alterar
    Então vejo a mensagem "* Genero nao cadastrado nesta permissao *"
    E nada é gravado

  Cenário: RN-13 — troca do sinal da linha
    Dado que a linha já está gravada com um sinal
    Quando tento trocar o sinal
    Então vejo a mensagem "* Nao altere sinal do acrescimo *" ou "* Nao altere sinal do desconto *"
    E nada é gravado

  Cenário: RN-13 — inclusão de linha numa alteração
    Dado que consultei o grupamento
    Quando informo uma linha com a situação I e os dados válidos
    Então o gênero é incluído no grupamento
    E a operação fica registrada na auditoria

  Cenário: RN-13 — exclusão de uma linha do grupamento
    Dado que consultei o grupamento e o gênero existe nele
    Quando informo a situação E na linha
    Então a linha é apagada do grupamento
    E a operação fica registrada na auditoria

  Cenário: RN-14 — consulta lista o grupamento sem gravar
    Dado que existe grupamento lançado para o cabeçalho informado
    Quando abro a tela em consulta
    Então vejo as linhas do grupamento na tela
    E nada é incluído, alterado ou excluído
    E nenhuma trilha de operação é gerada

  Cenário: RN-14 — fornecedor em branco na consulta
    Dado que existe grupamento lançado para o cabeçalho, com fornecedor
    Quando deixo o fornecedor em branco e consulto
    Então a tela adota o fornecedor do próprio grupamento
    E mostra as linhas daquele grupamento

  Cenário: RN-14 — nada lançado para o cabeçalho informado
    Dado que não existe grupamento lançado para o cabeçalho informado
    Quando abro a tela em consulta
    Então vejo a mensagem "* Permissao nao cadastrada *"
    E o cursor volta ao campo da coordenadoria

  Cenário: RN-14 — depois de consultar, a alteração é liberada
    Dado que consultei aquele grupamento nesta sessão
    Quando troco a opção para ALT e confirmo o mesmo cabeçalho
    Então a tela aceita a alteração daquele grupamento

  Cenário: RN-15 — confirmação sem grupamento lançado
    Dado que não existe linha de grupamento para o cabeçalho
    Quando confirmo a atualização do cadastro
    Então vejo a mensagem "* Permissao nao cadastrada *"
    E nada é gravado

  Cenário: RN-15 — permissão já atualizada para aquele tipo de contrato
    Dado que já existe permissão de contrato para o grupamento e o período
    Quando confirmo a atualização do cadastro
    Então vejo a mensagem "* Permissao ja atualizada. Use outro TC *"
    E nada é gravado

  Cenário: RN-15 — permissão nos mesmos limites do grupamento
    Dado que a permissão já está nos mesmos limites do grupamento
    Quando confirmo a atualização do cadastro
    Então vejo a mensagem "* Permissao ja atualizada *"
    E nada é gravado

  Cenário: RN-15 — permissão do intervalo é de outro fornecedor
    Dado que a permissão do intervalo é de outro fornecedor
    Quando confirmo a atualização do cadastro
    Então vejo a mensagem "* Grupamento cadastrado para outro fornecedor *"
    E nada é gravado

  Cenário: RN-15 — sobreposição de intervalo com permissão existente
    Dado que já existe permissão no intervalo do grupamento
    Quando confirmo a atualização do cadastro
    Então vejo a mensagem "* Ja existe permissao neste intervalo *"
    E nada é gravado

  Cenário: RN-15 — soma dos valores iniciais não fecha com o adjudicado
    Dado que a soma dos valores iniciais dos gêneros difere do valor adjudicado
    Quando confirmo a atualização do cadastro
    Então vejo a mensagem "* Nao atualize.Soma qt.ini generos difere vl.adj *"
    E nada é gravado

  Cenário: RN-15 — gênero sem desconto pede confirmação
    Dado que há no grupamento um gênero sem desconto
    Quando confirmo a atualização do cadastro sem marcar a confirmação
    Então vejo a mensagem "* Confirma genero sem desconto ? *"
    E nada é gravado

  Cenário: RN-15 — gênero sem desconto, com a confirmação marcada
    Dado que há no grupamento um gênero sem desconto
    E que marco a confirmação
    Quando confirmo a atualização do cadastro
    Então a atualização segue

  Cenário: RN-16 — a atualização gera a permissão, o contrato e o período e apaga o grupamento
    Dado que as conferências da atualização passaram
    Quando confirmo a atualização do cadastro
    Então a permissão de contrato é gerada para cada linha do grupamento
    E o contrato e o período do contrato são gerados, se ainda não existirem
    E o registro de identificação dos órgãos é gerado para as linhas assim marcadas
    E as linhas do grupamento que serviram de base são apagadas
    E vejo o aviso "Cadastro Atualizado"
    E a operação fica registrada na auditoria

  Cenário: RN-16 — licitação 99 cria o grupamento do período anterior
    Dado que o grupamento está marcado com o tipo de licitação 99
    Quando confirmo a atualização do cadastro
    Então as linhas do grupamento do período anterior à permissão são criadas
    E vejo o aviso "Cadastro Atualizado"

  Cenário: RN-17 — toda gravação deixa rastro
    Dado que incluí, alterei ou excluí uma linha do grupamento
    Então existe um registro de auditoria com a tela de origem, a operação e o conteúdo anterior e posterior da linha
```
