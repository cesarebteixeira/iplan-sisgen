# US — E240T — Manter períodos de contrato

## Estória

Como **servidor da CRE que responde pelo contrato de fornecimento da alimentação
escolar da sua coordenadoria**, quero **informar o tipo de contrato, o fornecedor, o
dia em que a entrega começa e por quantos dias ela corre, e confirmar o período do
meu grupo — ou abrir um período já cadastrado**, para que **o período nasça com o
prazo e as datas de entrega certos, dentro do que a permissão do contrato autoriza, e
eu siga para o detalhe dele sem redigitar nada**.

O período de contrato não tem número: ele é identificado pelo grupo, pela data de
início, pelo tipo de contrato e pelo fornecedor. Esta é a tela em que essa combinação
é montada e conferida, e é a conferência dela que impede o período de nascer com data
de entrega fora do prazo permitido, em dia não útil ou para um fornecedor sem
permissão cadastrada. A inclusão não grava direto: ela pede uma confirmação, e quem
cria o registro do período e o cadastro de gêneros é a tela seguinte, que esta abre já
com a próxima identificação de cadastro livre. Sem essa passagem, o período ficaria
validado e não cadastrado.

## Contexto

Jornada S000M → E000M → E240M → E240T.

Ator: servidor de CRE — monta o período de contrato do seu grupo (tipo de contrato,
fornecedor, início e dias de entrega) e confirma a inclusão, ou abre um período já
cadastrado para seguir ao detalhe dele.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. Os dois menus do caminho — `E000M` e
`E240M` — não gravam nada: só encaminham.

Uma coisa da navegação, porém, é regra. Esta tela **não é alcançada só pelo menu**:
duas telas da mesma família, a `E242T` e a `E243T`, encadeiam nela sem passar por menu
e deixam o registro e a operação que estavam tratando. Por essa porta a tela abre em
consulta com o período já preenchido, e não na inclusão proposta (RN-09).

O que esta tela usa da sessão é a **secretaria (o tipo de órgão)**, a **coordenadoria
regional escolar do servidor** (o grupo), a **matrícula**, o **código de acesso**, o
**privilégio** e a **data do sistema**; a carga disso é regra da entrada e está no
anexo de evidências, em **Regras que se revelaram da entrada**. O **órgão filho** do
servidor, que a entrada também carrega, não limita esta tela: as leituras aqui são
delimitadas pelo tipo de órgão e pelo grupo.

Esta tela é uma passagem, e tem duas saídas. Ela **reabre a si mesma** para pedir a
confirmação da inclusão e para tratar o pedido de impressão do período, e **entrega o
período à tela `E241T`**, que é quem grava. É por isso que a jornada não termina aqui:
o que esta tela decide — o modo e o período — é o que a tela seguinte executa (RN-08 e
RN-13).

## Regras de negócio

### RN-01 — A tela inclui e consulta: qualquer outra operação é recusada

Esta é uma tela de **manutenção do período**: ela aceita **incluir** e **consultar**, e
recusa qualquer outra operação com **\* Opcao nao disponivel. Use INC ou CON \***, com
o cursor de volta ao campo da operação e **nada lido** do cadastro nesse caminho — a
recusa vem antes de o período ser procurado.

Os dois valores aceitos não são palavras escritas na tela: eles vêm da **tabela de
mensagens do ambiente**, a mesma que dá o texto da recusa. É por isso que a mensagem
manda usar "INC" e "CON" enquanto a tela compara os códigos que essa tabela carrega.

### RN-02 — A abertura pelo menu propõe a inclusão, para o grupo da sessão

Aberta pelo menu, a tela propõe **incluir**: a operação mostrada é a inclusão, o
**grupo** vem preenchido com a coordenadoria da sessão, a **quantidade de dias de
entrega** já vem com cinco e o **código de impressão** vem em branco. Não havendo
coordenadoria na sessão, o grupo abre em branco e o cursor fica nele. Nada é gravado
na abertura.

No alto a tela mostra a **descrição do tipo de órgão da sessão** (a secretaria) e a
**data do sistema**.

[?] A descrição do tipo de órgão e a data do sistema são copiadas da sessão, e nenhum
programa deste caminho as preenche — a área comum só as apaga na inicialização. Se o
ambiente não as fornecer, o cabeçalho sai em branco. Pergunta ao site.

### RN-03 — O grupo é obrigatório, e é o da própria coordenadoria

O grupo tem de ser informado: em branco, a recusa é **\* Informe o grupo \***, com o
cursor de volta ao campo e nada lido do cadastro. Informado um grupo diferente do que
a sessão carrega, a recusa é **\* Usuario sem acesso a outro grupo \***, também com o
cursor no campo e antes de qualquer leitura. Quando a sessão já traz o grupo, é ele que
a tela mostra no campo: o servidor não precisa informá-lo, e informar outro não é
aceito.

[?] Quando a sessão **não** tem grupo — o vínculo do servidor não aponta nenhuma
coordenadoria —, a conferência não se aplica e a tela aceita qualquer grupo. Se isso é
intencional ou é buraco de autorização, é pergunta ao site.

### RN-04 — A inclusão exige permissão cadastrada para o grupo, o contrato e o fornecedor, dentro do prazo

Na inclusão, o **tipo de contrato** tem de ser informado: em branco, a recusa é
**\* Informe tipo contrato \***, com o cursor no campo.

Informado, a tela percorre o **cadastro de permissões do contrato** do tipo de órgão da
sessão, procurando as permissões que casam o **grupo**, o **tipo de contrato** e o
**fornecedor** informados. A inclusão só passa quando existe uma permissão cujo
**prazo cobre todo o período pedido**: o início da entrega não pode ser anterior ao
início da permissão, nem a data limite pode passar do limite dela. Não achando, a
recusa é **\* Permissao nao cadastrada \***, com o cursor no campo do tipo de contrato,
e nada é gravado.

[?] A permissão também é cadastrada por recortes de classe, subclasse e gênero do
contrato, e a busca desta tela percorre esses recortes sem olhar para eles: basta que
um recorte cubra o período. Se a intenção era exigir um recorte específico, a
conferência não existe. Pergunta ao site.

### RN-05 — O início da entrega é conferido: data válida, ano plausível, no máximo trinta dias à frente e dia útil

A data de início da entrega é montada com o dia, o mês e o ano informados, e passa por
quatro conferências, nesta ordem:

- a data tem de **existir** — dia e mês que o calendário aceita — e o **ano** tem de
  estar entre **1994 e 2099**; senão, **\* Data de inicio da entrega invalida \***;
- a data **não pode cair em sábado** — **\* Inicio da entrega nao deve ser um sabado \***
  — **nem em domingo** — **\* Inicio da entrega nao deve ser um domingo \***;
- a data **não pode ser feriado** do tipo de órgão da sessão, procurado no **cadastro
  de feriados** da secretaria — **\* Inicio da entrega nao deve ser um feriado \***;
- a data **não pode passar de trinta dias** contados do dia do sistema; senão,
  **\* Inicio da entrega invalido \***.

Em todas, o cursor volta ao campo do dia do início e nada é lido do período. O **prazo de
trinta dias é a última conferência**, depois do dia da semana e do feriado: uma data fora
do prazo ainda é recusada antes por ser sábado, domingo ou feriado, quando for o caso.

[?] A conferência de sábado e domingo depende do **nome do dia** que a rotina de data
do ambiente devolve, e essa rotina é importada, sem corpo no acervo expandido; o que se
lê é que a tela compara o resultado da conversão da data com "SABADO"/"SATURDAY" e
"DOMINGO"/"SUNDAY", e que as telas irmãs fazem a mesma conferência logo depois da mesma
conversão. Se o ambiente devolver outro texto, a recusa não sai. Pergunta ao site.

### RN-06 — A quantidade de dias de entrega é de um a cinco, e a data limite é calculada a partir dela

A quantidade de dias de entrega tem de ser informada e ficar entre **um e cinco**: em
branco, a recusa é **\* Informe a quantidade de dias de entrega \***; acima de cinco,
**\* Quantidade maxima de dias de entrega = 5 \***; as duas com o cursor de volta ao
campo dos dias.

Informada, a tela calcula as datas de entrega do período. A primeira é o próprio início
da entrega, e as seguintes são os dias úteis que vêm depois, **pulando sábados,
domingos e feriados** do tipo de órgão da sessão. A **data limite** do período é a
última dessas datas: ela não é digitada — a tela a calcula e substitui o que estiver no
campo. São até cinco datas, uma por dia de entrega.

[?] Os três campos da data limite passam pela edição numérica, mas **nenhum deles
devolve o cursor** quando a digitação é recusada (só o grupo, o tipo de contrato, o
fornecedor, as três partes do início e os dias o fazem), e a tela os substitui pelas
datas que calculou. Se a máscara deixa o servidor digitar neles, o que ele escreve ali
não muda nada. Pergunta ao site.

### RN-07 — A inclusão é confirmada antes de seguir, e a resposta que não é "sim" não cancela a inclusão

Passando todas as conferências, a tela **não segue direto**: ela guarda o que foi
informado, reabre a si mesma com a pergunta
**\* Confirma inclusao de generos <S/N> ? \*** e deixa o cursor no campo da resposta.
Só a resposta **"S"** faz a tela seguir, e a resposta é conferida contra o que foi
guardado: se algum dado do período mudou entre a pergunta e a resposta, a tela volta ao
começo das conferências e pergunta de novo.

[?] A resposta diferente de "S" — inclusive "N" — **não abandona a inclusão**: a tela
limpa a resposta, volta ao começo das conferências e apresenta a mesma pergunta outra
vez. Não há, no material lido, caminho de cancelamento; para sair, é preciso trocar a
operação para consulta. Se "N" deveria cancelar, o caminho não existe. Pergunta ao site.

### RN-08 — Confirmada a inclusão, esta tela entrega o período à tela seguinte, com a próxima identificação de cadastro livre

Confirmada a inclusão, esta tela **não grava o período**. Ela procura, entre os
cadastros do mesmo período — grupo, tipo de contrato, fornecedor e data de início —, a
**maior identificação de cadastro já usada**, propõe a **seguinte** e entrega à tela
`E241T`: a operação de **inclusão**, a identificação do período, o fornecedor com a
razão social lida e as datas calculadas. A `E241T` abre em **inclusão** por causa disso
e é ela que cria o registro do período e o cadastro de gêneros.

Um mesmo período pode ter mais de um cadastro: cada inclusão confirmada gera uma
identificação nova para o mesmo período, e é essa identificação que diz se o cadastro
de gêneros já existe.

[?] Para achar a maior identificação, a leitura do período é posicionada com um valor
máximo no lugar da identificação, e o que os sinalizadores da leitura dizem à base não
se lê no material desta jornada (ver o anexo, **O que ficou sem fonte**). Se essa
leitura devolver o primeiro cadastro e não o último, a identificação proposta pode
repetir uma já usada. Pergunta ao site.

### RN-09 — A tela abre com o registro de quem a chamou quando vem da E242T ou da E243T

A tela tem duas aberturas. Pelo **menu** (`E240M`), ela abre como em RN-02: inclusão
proposta, grupo da sessão e cinco dias, com os campos do período em branco. Vinda
**encadeada da `E242T` ou da `E243T`** — telas que não passam por menu e deixam o
registro e a operação que estavam tratando —, ela abre mostrando o **período e a
operação que essas telas deixaram** (a consulta) e com o aviso
**CADASTRO SENDO ATUALIZADO** na linha de situação; nesse caso ela não propõe a
inclusão.

Esse é o único ponto em que o comportamento da tela depende de quem a chamou, e vale
só para a primeira abertura: assim que a tela passa a receber as mensagens do operador,
ela volta ao seu próprio caminho.

[?] A marca de origem que a tela consulta é a da última tela que passou por ela, e esta
tela apaga essa marca na própria abertura: a abertura por encadeamento não se repete
depois. Se o esperado era conservar a origem durante toda a sessão da tela, não é o que
o programa faz. Pergunta ao site.

### RN-10 — A consulta exige a requisição cadastrada

Na consulta, a tela procura o período pela combinação informada — **grupo, tipo de
contrato, fornecedor e data de início** —, conferindo o **tipo de órgão** da sessão em
todas as partes desse conjunto. Não achando, a recusa é
**\* Requisicao nao cadastrada \***, o cursor volta ao campo da operação e nada mais é
lido.

[?] A **identificação do cadastro** não faz parte do que o servidor informa nem da
conferência: havendo mais de um cadastro para o mesmo período, a tela mostra o que a
leitura devolver primeiro e não há como escolher entre eles. Se o esperado é abrir o
cadastro mais recente, a escolha não existe. Pergunta ao site.

[?] A recusa devolve o cursor ao campo da **operação**, e não aos campos que
identificam a requisição (grupo, contrato, fornecedor e data de início). Se a intenção
era apontar o dado que falta, o cursor está no lugar errado. Pergunta ao site.

### RN-11 — O código de impressão transforma a operação em consulta e exige o cadastro já gerado

Preenchido o **código de impressão**, a tela força a operação para **consulta**, mesmo
que a operação mostrada seja a inclusão. Nesse caminho, o período consultado tem de
estar marcado no cadastro de períodos como **já gerado**: não estando, a recusa é
**\* Cadastro nao gerado \***, com o cursor de volta ao campo do código de impressão.

[?] O código de impressão não é conferido contra nenhum cadastro nesta tela: ele entra
no pedido do relatório como parâmetro. Existe no dicionário um cadastro que associa
código de impressão e matrícula, e esta tela não o lê — se deveria conferir a
autorização de quem pede, a conferência não existe. Pergunta ao site.

### RN-12 — O pedido de impressão: o relatório em processamento e a requisição criada

Com o código de impressão preenchido e o cadastro já gerado, a tela procura no
**cadastro de requisições** se já existe um pedido de relatório daquele tipo para o
**tipo de órgão e o grupo** da sessão. Existindo, ela avisa
**\* Relatorio em processamento. Aguarde. \***, com o cursor no campo do código de
impressão, e não cria nada.

Não existindo, ela monta a **requisição do relatório** que trata os períodos de
contrato: toma o **número seguinte** ao maior número de requisição já usado, leva a
estação, a matrícula, a data e o **e-mail do servidor**, lido do cadastro de
funcionários, e o período como parâmetro — grupo, tipo de contrato, fornecedor, data de
início e identificação do cadastro —, e grava a requisição. O pedido é então enviado
para processamento fora da tela.

[?] A tela prepara o aviso **\* Relatorio em Processamento \*** e a rota para si mesma,
mas o trecho seguinte, sem desvio, reaponta a rota para a `E241T`: a tela não se reabre
e o aviso não chega a ser mostrado. Ou o aviso é trecho sem uso, ou falta um desvio.
Pergunta ao site.

### RN-13 — A consulta entrega o período à tela seguinte, que abre em consulta

Achando a requisição e **sem** código de impressão, a tela lê o fornecedor (a razão
social), guarda o período completo — grupo, tipo de contrato, fornecedor, tipo de
cartão, datas de início e limite, situação de requisição e identificação do cadastro —
e **entrega esse registro e a operação de consulta** à `E241T`, que abre o período
**em consulta** por causa disso. Nada é gravado por esta tela nessa passagem.

A `E241T` só processa o período quando ele vem da `E240T`, da `E240C` ou da `E242T`; de
qualquer outra origem ela não o processa e devolve o servidor ao menu `E240M`. Sem a
marca desta tela, portanto, o período escolhido não se abre.

### RN-14 — O que esta tela grava: só a requisição de relatório

Esta tela **não grava o período de contrato nem o cadastro de gêneros** — quem os cria é
a `E241T`. A única gravação que ela executa é a da **requisição de relatório** (RN-12).
As declarações de gravação, de exclusão e de travamento existem para todos os cadastros
que a tela enxerga — é assim que o programa é montado —, mas só a requisição é
acionada: nenhuma exclusão é executada, e o travamento de registro aparece apenas
dentro dos caminhos de exclusão, que esta tela não percorre. A tela também não gera
trilha de auditoria: o cadastro de auditoria não está entre os que ela enxerga — quem o
escreve é a `E241T`, junto com o período.

### RN-15 — A digitação passa pela edição numérica antes de qualquer conferência

**Dez campos** da tela são tratados como número: o grupo, o tipo de contrato, o
fornecedor, as três partes do início da entrega, as três partes da data limite e a
quantidade de dias. O que estiver em branco vira zero, os zeros à esquerda caem e o que
não for número é recusado **antes** de qualquer conferência de negócio e de qualquer
leitura do cadastro. Na recusa, **sete** deles devolvem o cursor: o grupo, o tipo de
contrato, o fornecedor, as três partes do início da entrega e a quantidade de dias. As
três partes da data limite não devolvem o cursor.

[?] O texto da recusa da edição numérica não está nos fontes desta jornada: quem edita é
uma rotina comum, importada, sem corpo no acervo. E como nem todos os campos devolvem o
cursor, o servidor pode ser recusado sem saber em qual campo errou. Pergunta ao site.

### RN-16 — A razão social vem do cadastro de fornecedores, e o fornecedor não é conferido

O código do fornecedor informado é procurado no **cadastro de fornecedores**, e é a
**razão social** de lá que a tela mostra — tanto na inclusão quanto na consulta. Não
achando o fornecedor, a tela **não avisa**: a razão social sai em branco e o caminho
segue.

[?] O fornecedor não é conferido contra o cadastro: a tela só lê o nome dele. Na
inclusão, o que barra um fornecedor sem direito é a permissão do contrato (RN-04), e não
o cadastro de fornecedores; na consulta, nada o confere. Se o fornecedor deveria estar
cadastrado para o período existir, a conferência não existe. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Incluir e consultar o período de contrato da alimentação escolar de um grupo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E240T

  Cenário: RN-01 — operação diferente de incluir e consultar
    Dado que estou na tela E240T
    Quando informo uma operação que não é incluir nem consultar
    Então vejo a mensagem "* Opcao nao disponivel. Use INC ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido do cadastro de períodos nesse caminho

  Cenário: RN-02 — a abertura pelo menu propõe a inclusão
    Dado que a minha sessão tem uma coordenadoria
    Quando abro a tela E240T pelo menu E240M
    Então a operação mostrada é a inclusão
    E o grupo mostrado é o da minha sessão
    E a quantidade de dias de entrega já vem preenchida com cinco

  Cenário: RN-02 — abertura sem coordenadoria na sessão
    Dado que a minha sessão não tem coordenadoria
    Quando abro a tela E240T
    Então o grupo abre em branco, com o cursor no campo

  Cenário: RN-03 — grupo não informado
    Quando deixo o grupo em branco
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nada é lido do cadastro

  Cenário: RN-03 — grupo de outra coordenadoria
    Dado que a minha sessão tem uma coordenadoria
    Quando informo o grupo de outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo do grupo
    E nada é lido do cadastro

  Cenário: RN-03 — sessão sem coordenadoria aceita qualquer grupo
    Dado que a minha sessão não tem coordenadoria
    Quando informo qualquer grupo
    Então a tela aceita o grupo informado

  Cenário: RN-04 — tipo de contrato não informado
    Quando deixo o tipo de contrato em branco
    Então vejo a mensagem "* Informe tipo contrato *"
    E o cursor volta ao campo do tipo de contrato

  Cenário: RN-04 — inclusão sem permissão para o contrato
    Dado que o meu grupo não tem permissão cadastrada para esse tipo de contrato
          e esse fornecedor
    Quando confirmo a inclusão
    Então vejo a mensagem "* Permissao nao cadastrada *"
    E o cursor volta ao campo do tipo de contrato
    E nada é gravado

  Cenário: RN-04 — inclusão com permissão que cobre o período
    Dado que existe uma permissão do meu grupo para esse contrato e fornecedor
    E o prazo dessa permissão cobre o início da entrega e a data limite do período
    Quando confirmo a inclusão
    Então a tela segue para a confirmação

  Cenário: RN-05 — data de início que não existe
    Quando informo um dia e um mês que não formam uma data
    Então vejo a mensagem "* Data de inicio da entrega invalida *"
    E o cursor volta ao campo do dia do início

  Cenário: RN-05 — início da entrega além de trinta dias
    Quando informo um início de entrega a mais de trinta dias do dia de hoje
    Então vejo a mensagem "* Inicio da entrega invalido *"
    E o cursor volta ao campo do dia do início

  Cenário: RN-05 — início da entrega em sábado
    Quando informo um início de entrega que cai em sábado
    Então vejo a mensagem "* Inicio da entrega nao deve ser um sabado *"
    E o cursor volta ao campo do dia do início

  Cenário: RN-05 — início da entrega em domingo
    Quando informo um início de entrega que cai em domingo
    Então vejo a mensagem "* Inicio da entrega nao deve ser um domingo *"
    E o cursor volta ao campo do dia do início

  Cenário: RN-05 — início da entrega em feriado da secretaria
    Dado que o dia informado é feriado do tipo de órgão da minha sessão
    Quando confirmo
    Então vejo a mensagem "* Inicio da entrega nao deve ser um feriado *"
    E o cursor volta ao campo do dia do início

  Cenário: RN-06 — quantidade de dias de entrega não informada
    Quando deixo a quantidade de dias de entrega em branco
    Então vejo a mensagem "* Informe a quantidade de dias de entrega *"
    E o cursor volta ao campo dos dias

  Cenário: RN-06 — quantidade de dias de entrega acima de cinco
    Quando informo mais de cinco dias de entrega
    Então vejo a mensagem "* Quantidade maxima de dias de entrega = 5 *"
    E o cursor volta ao campo dos dias

  Cenário: RN-06 — a data limite é calculada a partir dos dias
    Dado que informo cinco dias de entrega a partir de um início válido
    Quando a tela calcula o período
    Então a data limite passa a ser a data do último dia de entrega
    E os dias que caem em sábado, domingo ou feriado não contam como dia de entrega

  Cenário: RN-07 — a inclusão é confirmada antes de gravar
    Dado que o período passou por todas as conferências
    Quando a tela reabre
    Então vejo a pergunta "* Confirma inclusao de generos <S/N> ? *"
    E o cursor fica no campo da resposta
    E nada foi gravado ainda

  Cenário: RN-07 — resposta diferente de "S"
    Dado que estou na pergunta da confirmação
    Quando respondo "N"
    Então a tela volta ao começo das conferências
    E a mesma pergunta é apresentada de novo

  Cenário: RN-08 — confirmada a inclusão, a tela seguinte abre em inclusão
    Dado que confirmei a inclusão com "S" e não mudei nenhum dado do período
    Quando a tela entrega o período à tela E241T
    Então a E241T abre em inclusão
    E a identificação de cadastro proposta é a seguinte à maior já usada para o período
    E nenhum período de contrato foi gravado por esta tela

  Cenário: RN-09 — abertura encadeada da E242T ou da E243T
    Dado que cheguei à E240T encadeado da E242T
    Quando a tela abre
    Então vejo o período e a operação de consulta que a E242T deixou
    E a linha de situação mostra "CADASTRO SENDO ATUALIZADO"
    E a tela não propõe a inclusão

  Cenário: RN-09 — abertura pelo menu não traz registro
    Dado que cheguei à E240T pelo menu E240M
    Quando a tela abre
    Então os campos do período abrem em branco
    E a operação proposta é a inclusão

  Cenário: RN-10 — consulta de requisição não cadastrada
    Quando consulto uma combinação de grupo, contrato, fornecedor e data de início
          que não existe
    Então vejo a mensagem "* Requisicao nao cadastrada *"
    E o cursor volta ao campo da operação
    E nada mais é lido

  Cenário: RN-11 — pedido de impressão para cadastro não gerado
    Dado que informo um código de impressão
    E o período consultado ainda não foi gerado
    Quando confirmo
    Então vejo a mensagem "* Cadastro nao gerado *"
    E o cursor volta ao campo do código de impressão

  Cenário: RN-12 — relatório já em processamento para o grupo
    Dado que informo um código de impressão
    E o período está gerado
    E já existe uma requisição de relatório em processamento para o meu grupo
    Quando confirmo
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E nenhuma requisição nova é criada

  Cenário: RN-12 — a requisição de relatório é criada
    Dado que informo um código de impressão
    E o período está gerado
    E não existe relatório em processamento para o meu grupo
    Quando confirmo
    Então o sistema cria a requisição com o número seguinte ao maior já usado
    E leva a estação, a matrícula e o e-mail do servidor
    E o pedido é enviado para processamento

  Cenário: RN-13 — a consulta entrega o período à tela seguinte
    Dado que encontrei o período do meu grupo
    Quando confirmo a consulta sem informar código de impressão
    Então a tela E241T abre com o período em consulta
    E nada é gravado por esta tela

  Cenário: RN-14 — esta tela não grava o período
    Dado que percorri a inclusão e a consulta
    Quando a tela termina
    Então nenhum período de contrato e nenhum cadastro de gêneros foi gravado por esta tela
    E nenhum registro de auditoria foi gerado

  Cenário: RN-15 — digitação que não é número
    Quando digito num campo numérico algo que não é número
    Então o sistema recusa a digitação antes de qualquer conferência
    E o cursor volta ao campo quando é o grupo, o tipo de contrato, o fornecedor,
          o dia, o mês ou o ano do início, ou a quantidade de dias

  Cenário: RN-16 — a razão social vem do cadastro de fornecedores
    Dado que o fornecedor informado está no cadastro de fornecedores
    Quando a tela lê o fornecedor
    Então vejo a razão social do cadastro
    E quando o fornecedor não está cadastrado a razão social sai em branco e o caminho segue
```
