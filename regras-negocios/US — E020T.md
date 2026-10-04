# US — E020T — Registro do pedido de alimentação escolar

## Estória

Como **servidor de CRE**, quero **registrar o pedido de alimentação escolar de um
fornecedor para um órgão da secretaria, com o período, a semana e os dias de
entrega**, para que **o fornecedor saiba quando entregar e a secretaria possa
distribuir os gêneros por dia, aprovar o pedido e conferir o que chega**.

O pedido de alimentação escolar começa aqui: é esta tela que diz de qual órgão é o
pedido, qual fornecedor o atende, em que período e em que dias a entrega deve
acontecer — e é ela que dá ao pedido o seu número. Sem isso não há como distribuir
gênero nenhum por dia de entrega, nem aprovar o pedido, nem conferir a entrega
contra o que a escola recebeu. É também aqui que o pedido se corrige e se desfaz:
enquanto não está aprovado ele pode ser alterado e excluído; depois disso, não.

## Contexto

Jornada S000M → E000M → E010M → E020T.
Ator: servidor de CRE — abre o pedido de alimentação escolar do órgão, informa o
fornecedor, o período, a semana e os dias de entrega, inclui, altera, exclui ou
consulta o pedido e segue para a tela que distribui os gêneros pelos dias.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Da sessão a tela usa o vínculo do servidor — a matrícula, o tipo de órgão, a
coordenadoria regional escolar, o órgão filho e o código de acesso —, e é dele que
sai o alcance do que ela deixa consultar e gravar. No cabeçalho ela mostra a
descrição do tipo de órgão e a data do sistema.

A tela não termina em si: ela reabre a si mesma para pedir a confirmação e, ao fim
da passagem, abre a tela `E021T`, que distribui as quantidades de cada gênero pelos
dias de entrega. Para lá ela passa o pedido, o órgão, a coordenadoria, o
fornecedor, o período, a semana, a quantidade e os cinco dias de entrega, e a
operação — e é essa operação que decide se a `E021T` abre em consulta ou em
alteração. A `E021T` também reabre esta tela, quando o servidor pede, lá, um pedido
novo.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela só aceita incluir, alterar, excluir e consultar

O campo da operação aceita quatro coisas: **incluir**, **alterar**, **excluir** e
**consultar**. Sem nenhuma delas — campo em branco, valor estranho ou qualquer
outra coisa — a tela recusa com **\* Opcao nao disponivel. Use INC, ALT, EXC ou
CON \***, com o cursor de volta no campo da operação, e não grava nada.

[?] A tela compara a operação com quatro códigos internos de três letras —
inclusão, alteração, exclusão e consulta —, e não com as siglas que a mensagem
manda usar; e o valor que ela mesma escreve no campo, ao abri-lo para um pedido
novo, é o código interno da inclusão. Não se conclui do acervo se o terminal
entrega a sigla já traduzida ou se o campo é preenchido por outra via. Pergunta ao
site.

### RN-02 — Os campos numéricos passam por edição numérica antes das conferências

Antes de qualquer conferência de negócio, **dezessete campos** passam por edição
numérica: o órgão filho, a coordenadoria regional escolar, o número do pedido, o
ano da entrega, o código do fornecedor, o dia, o mês e o ano do início do período,
o dia, o mês e o ano do limite, a quantidade de dias de entrega, o número e o ano
do pedido a copiar e os três dias de cópia. O campo em branco é tratado como zero,
e o que não for número é recusado antes das conferências. A operação, a próxima
tela, a semana e a resposta da confirmação **não** passam por essa edição.

[?] A tela só sabe devolver o cursor a treze desses dezessete campos: um erro de
digitação na coordenadoria regional escolar ou em qualquer uma das três datas do
limite não tem posição de cursor definida, e o que o servidor vê nesse caso não se
conclui desta tela. Pergunta ao site.

### RN-03 — A tela abre de dois jeitos, conforme a tela que a chamou

Aberta pelo menu (`E010M`), a tela começa um pedido novo: a operação é a inclusão e
o órgão filho e a coordenadoria vêm do vínculo do servidor na sessão; não vindo o
órgão do vínculo, o cursor já fica no campo do órgão, para o servidor informá-lo.
Reaberta pela tela que ela mesma abre (`E021T`), ela repõe o cabeçalho que aquela
tela devolveu — o órgão com a descrição, a coordenadoria, o fornecedor, o período e
a semana — e continua a partir dali, também para incluir. Nas duas entradas o
número do pedido e o ano da entrega começam vazios e a quantidade de dias de
entrega já vem preenchida com **5**.

### RN-04 — O órgão filho tem de ser informado e estar no alcance do servidor

Para incluir, o servidor informa o órgão filho (o SDI, de 8 dígitos). A tela recusa,
com o cursor de volta no campo do órgão e sem gravar nada:

- **\* Informe o orgao \*** — quando o órgão não foi informado;
- **\* Usuario sem acesso a outro orgao \*** — quando o servidor tem um órgão no
  vínculo da sessão e informa outro;
- **\* Orgao nao cadastrado \*** — quando o código não existe no cadastro de
  órgãos;
- **\* Orgao cadastrado como inativo \*** — quando o cadastro está marcado como
  inativo;
- **\* Orgao cadastrado com dados incompletos \*** — quando faltam, no cadastro, o
  bairro, o órgão pai, o nome, o endereço, a quantidade de matrículas ou a de
  pessoas;
- **\* Orgao nao pertence a esta secretaria \*** — quando o tipo de órgão do
  cadastro não é o da secretaria da sessão;
- **<- Usuario sem acesso ao grupo deste orgao \*** — quando a coordenadoria do
  servidor não é a coordenadoria do órgão.

Passando por isso, a descrição do órgão aparece no cabeçalho e a coordenadoria do
órgão passa a ser a do pedido.

### RN-05 — O fornecedor tem de estar cadastrado

O código do fornecedor (4 dígitos) é procurado no cadastro de fornecedores. Não
existindo — ou estando marcado como excluído, que a tela não aceita — ela recusa com
**\* Fornecedor nao cadastrado \***, com o cursor no campo, e não grava nada.
Achado, a razão social do fornecedor aparece no cabeçalho.

[?] Quando o fornecedor informado está marcado como excluído, a tela volta a
procurá-lo pelo mesmo código, em laço; a única saída do laço é a releitura deixar de
devolver o registro. Das duas leituras, uma posiciona pelo código e a outra relê, e
nada no acervo diz se a releitura avança para o fornecedor seguinte. Se não avançar,
a tela fica presa nesse caso. Pergunta ao site.

### RN-06 — O início da entrega tem de ser uma data válida e um dia de entrega

O dia, o mês e o ano do início do período formam a data de início da entrega. Ela é
recusada, com o cursor no campo do dia do início e sem gravar nada:

- **\* Data de inicio da entrega invalida \*** — quando não é uma data que existe
  no calendário; o ano tem de ficar entre 1994 e 2099;
- **\* Inicio da entrega nao deve ser um sabado \*** e **\* Inicio da entrega nao
  deve ser um domingo \*** — quando a data cai no fim de semana;
- **\* Inicio da entrega nao deve ser um feriado \*** — quando a data está entre os
  feriados cadastrados para o tipo de órgão.

### RN-07 — Os mapas do órgão têm de estar atualizados até o limite que o perfil implica

Quando o cadastro do órgão **não** está marcado como acumulado, a tela toma o
número de dias do perfil do tipo de órgão e recua o início da entrega nesse tanto,
chegando a uma data de referência. Ela então procura, para o órgão e a
coordenadoria, o mapa dessa data; não o encontrando, recusa com **<- Antes,
atualize os mapas ate a data inf. \*** — a data mostrada é o limite que falta
cobrir —, com o cursor no campo da próxima tela, e não grava nada. Para o órgão
marcado como **acumulado**, essa conferência e o recuo pelo perfil do tipo de órgão
não são feitos.

[?] A busca do mapa anda pelo calendário a partir da data de referência, com um
limite de nove passos e comparando a data com uma data fixa do ano de 2008. O que a
tela considera "mapa atualizado" para aceitar a inclusão não se conclui do acervo
com precisão — só a mensagem e a data que ela mostra. Pergunta ao site.

### RN-08 — A quantidade de dias de entrega vai de 1 a 5

O servidor informa quantos dias de entrega o pedido tem, de **1 a 5**. Zero é
recusado com **\* Informe a quantidade de dias de entrega \*** e acima de 5 com
**\* Quantidade maxima de dias de entrega = 5 \***, com o cursor no campo e sem
gravar nada.

### RN-09 — Os dias de entrega saem do início, pulando fins de semana e feriados

A tela monta os dias de entrega a partir do início: o primeiro é o próprio início
da entrega e cada seguinte é o próximo dia que não seja sábado, domingo nem feriado
do tipo de órgão, até completar a quantidade informada. O limite do período de
entrega é o último desses dias. São esses dias que a tela entrega à tela seguinte,
que distribui por eles as quantidades de cada gênero.

### RN-10 — A semana da entrega tem de ser A, B, C, D ou E

O campo da semana da entrega (o cartão) aceita de **A** a **E**. Qualquer outro
valor — inclusive em branco — é recusado com **\* Informe semana com A / B / C / D
/ E \***, com o cursor no campo, e nada é gravado.

### RN-11 — Copiar de outro pedido

Para não redigitar, o servidor pode informar o número e o ano de um pedido já
cadastrado e até três dias de entrega dele; a tela então copia desse pedido os
gêneros, com as quantidades daqueles dias. Antes de copiar ela recusa, sem gravar
nada:

- **\* Pedido para copia nao cadastrado \*** — quando o pedido de origem não
  existe, com o cursor no número do pedido de origem;
- **\* Pedido para copia de outro orgao \*** — quando o pedido de origem é de outro
  órgão que não o do pedido novo (conferido quando o servidor tem órgão no vínculo
  da sessão), com o cursor no número do pedido de origem;
- **\* Dias de copia sem quant.cadastradas \*** — quando os dias informados não têm
  quantidade cadastrada no pedido de origem, com o cursor no primeiro dia de cópia;
- **\* Nao repita dia de copia \*** — quando o mesmo dia é informado duas vezes, com
  o cursor no dia repetido;
- **\* Dias de copia > dias entrega \*** — quando são informados mais dias de cópia
  do que dias de entrega do pedido novo, com o cursor no primeiro dia de cópia;
- **\* Dia nao cadastrado no pedido para copia \*** — quando um dia informado não é
  um dos dias de entrega do pedido novo, com o cursor naquele dia.

[?] A quantidade que a tela usa para conferir o terceiro dia de cópia é procurada
com o **primeiro** dia informado, e não com o terceiro: o terceiro dia acaba
conferido contra a quantidade do primeiro. Não se conclui do acervo se é isso que o
site espera. Pergunta ao site.

### RN-12 — O pedido se identifica pelo número e pelo ano, e é do órgão e da coordenadoria do servidor

Nas operações de alterar, excluir e consultar, e também na requisição de impressão,
o servidor informa o número do pedido e o ano da entrega — juntos, os dez dígitos
que identificam o pedido — e a tela procura o pedido daquela coordenadoria. Ela
recusa, sem gravar nada:

- **\* Informe o numero do pedido \*** — quando o número não foi informado, com o
  cursor no campo;
- **\* Orgao nao cadastrado \*** — quando o órgão filho informado não existe no
  cadastro de órgãos, com o cursor no órgão;
- **\* Pedido nao cadastrado \*** — quando o pedido não existe, com o cursor no
  número do pedido;
- **\* Pedido de outro orgao \*** — quando o pedido é de outro órgão filho, com o
  cursor no número do pedido;
- **<- Usuario sem acesso ao grupo deste pedido \*** — quando o pedido é de outra
  coordenadoria que não a do servidor, com o cursor no número do pedido.

Passando por isso, a tela repõe no cabeçalho o órgão com a descrição, a
coordenadoria, o fornecedor, o período e a semana que estão no pedido procurado.

### RN-13 — O que a situação do pedido recusa em cada operação

Conforme o estado do pedido procurado, a tela recusa, sem gravar nada, e com o
cursor no campo que a mensagem indica:

- **\* Pedido acumulado \*** — pedido de órgão cujo cadastro o marca como
  acumulado, em qualquer dessas operações;
- **\* Pedido pendente de distribuicao \*** — pedido que ainda não teve os gêneros
  distribuídos pelos dias de entrega, em qualquer dessas operações;
- **\* Pedido excluido \*** — na consulta e na impressão, quando o pedido está
  marcado como excluído;
- **\* Pedido aprovado nao pode ser alterado \*** e **\* Pedido fechado nao pode ser
  alterado \*** — na alteração, conforme a situação do pedido;
- **\* Pedido com tipo contrato nao pode ser alterado \*** — na alteração, quando
  algum gênero do pedido tem tipo de contrato;
- **\* Pedido aprovado nao pode ser excluido \***, **\* Pedido fechado nao pode ser
  excluido \*** e **\* Pedido nao pode ser excluido \*** — na exclusão, os dois
  primeiros pela situação do pedido e o terceiro quando algum gênero do pedido tem
  tipo de contrato.

[?] A tela prevê seis outras recusas dessa mesma família — o pedido acumulado na
inclusão, os dados já cadastrados neste pedido (use alteração), o pedido já aprovado
e o já fechado (não use inclusão), o pedido pendente de distribuição e os dados
excluídos (use alteração para reativar) —, mas o campo que decide qual delas mostrar
é reiniciado imediatamente antes dessas conferências, de modo que todas as seis são
inalcançáveis e o servidor nunca as vê por este caminho. Ou a reinicialização é o
defeito, ou as conferências ficaram para trás. Pergunta ao site.

### RN-14 — O intervalo de entrega não pode bater com o de outro pedido do mesmo fornecedor

Na alteração, a tela procura outros pedidos do mesmo fornecedor e recusa com
**\* Ja existe pedido neste intervalo de entrega \*** — mostrando, junto, o número
do pedido que já ocupa o intervalo — quando o intervalo de entrega do pedido novo
se sobrepõe ao de um pedido já cadastrado. Também recusa **\* Data final de entrega
menor que a data inicial \*** quando o limite é anterior ao início, com o cursor no
dia do início.

[?] A busca de outro pedido no mesmo intervalo usa como chave o dia **anterior** e
o dia **seguinte** ao início informado, e não o início informado: a tela só compara
o intervalo com pedidos do mesmo fornecedor que começam exatamente um dia antes ou
um dia depois. Não se conclui do acervo se a intenção era varrer o intervalo
inteiro. Pergunta ao site.

### RN-15 — A tela pede confirmação antes de gravar

Antes de incluir, alterar ou excluir, a tela reabre a si mesma com a pergunta no
campo de resposta: **\* Confirma inclusao do pedido <S/N> ? \***, **\* Confirma
alteracao do pedido <S/N> ? \*** ou **\* Confirma exclusao do pedido <S/N> ? \***.
Só com a resposta afirmativa a operação segue e grava; entre a pergunta e a
resposta a tela confere que nada mudou nos dados — se mudou, a confirmação é
descartada e a tela volta a conferir tudo antes de perguntar de novo. A consulta
não pede confirmação.

[?] Quando a resposta é negativa, a tela descarta a confirmação e volta a conferir
tudo; no caminho da inclusão ela chega outra vez à pergunta, porque a passagem que
pede a confirmação é a mesma que confere os dados. Não se conclui do acervo se o
servidor consegue desistir da inclusão respondendo "não". Pergunta ao site.

### RN-16 — O que a inclusão grava

Confirmada a inclusão, a tela dá o número ao pedido e o deixa pronto para a tela
seguinte:

- o número sai de um contador por tipo de órgão, coordenadoria regional escolar e
  ano: ela soma 1 ao último número do ano e, quando ainda não há pedido no ano,
  começa em **1** e cria o contador;
- o número do pedido é montado com dez dígitos — os seis do número e os quatro do
  ano da entrega — e fica na área de trabalho para a tela seguinte;
- o contador deixa um registro de auditoria, de inclusão quando nasceu agora e de
  alteração quando apenas avançou;
- **havendo pedido de origem para cópia**, a tela grava no pedido novo os gêneros
  copiados, com as quantidades dos dias informados, e grava o próprio pedido com o
  cabeçalho informado; **sem cópia**, a tela não grava nem o pedido nem os gêneros:
  isso é feito pela tela seguinte (`E021T`), que ela abre na inclusão.

[?] O contador do número do pedido é chaveado pelo **ano do início do período**, e o
número do pedido carrega o **ano da entrega**. Se os dois divergirem, não se conclui
do acervo se o número continua único por ano de entrega. Pergunta ao site.

### RN-17 — O que a exclusão grava

Confirmada a exclusão, a tela apaga cada gênero do pedido e, em seguida, o próprio
pedido, deixando um registro de auditoria para cada registro apagado — com a
operação, o cadastro atingido, o número do pedido, a coordenadoria, a secretaria, a
matrícula do servidor, a estação, a data e a hora da sessão e o conteúdo do registro
antes da exclusão. O contador do número do pedido **não** é tocado.

### RN-18 — A consulta e as recusas não gravam nada

A consulta termina antes de qualquer gravação: não cria pedido, gênero nem
contador, e não deixa registro de auditoria. Cada recusa também encerra a passagem
antes das gravações, de modo que o pedido continua exatamente como estava.

### RN-19 — O que a tela entrega à tela seguinte

Terminada a passagem, a tela abre a `E021T` e deixa na área de trabalho, para ela, o
órgão filho com a descrição, a coordenadoria regional escolar, o número do pedido,
o fornecedor com a razão social, o período, a semana, a quantidade e os cinco dias
de entrega, e a operação:

- **consultar**, quando o servidor consultou;
- **alterar**, quando o servidor alterou;
- **incluir**, quando o servidor incluiu **sem** cópia de outro pedido — porque
  nesse caso o pedido e os gêneros ainda não existem e quem os cria é a `E021T`;
- **alterar**, quando o servidor incluiu **com** cópia de outro pedido — porque
  nesse caso o pedido e os gêneros já foram gravados aqui.

A `E021T` decide por essa operação se abre em consulta ou em alteração. A exclusão
não segue para a `E021T`: ela termina nesta tela.

### RN-20 — A requisição de impressão do pedido

Quando o servidor preenche o código de impressão, a operação passa a ser a de
consulta, seja qual for a que ele havia marcado, e a tela procura o pedido como na
consulta (RN-12 e RN-13). Achado, ela monta a requisição de impressão do relatório
do pedido com o número do pedido, a secretaria (o tipo de órgão), a coordenadoria, a
matrícula do servidor, a estação, **uma** cópia e o endereço de correio eletrônico
do cadastro do servidor, e a entrega ao serviço de requisições do sistema. Nenhum
outro cadastro é tocado.

### RN-21 — Nada é gravado sem a conferência de sessão, de tela, de acesso e da operação

Na abertura, a tela confere que o servidor está na **estação em que a sessão foi
aberta**, que a tela está registrada (senão **\* Tela nao disponivel \***) e que o
código de acesso do servidor alcança a tela (senão **\* Acesso negado para esta
matricula \***). Em toda passagem de mensagem ela repõe, do vínculo da sessão, a
matrícula, o tipo de órgão, a coordenadoria, o órgão filho, o acesso e o privilégio,
e confere a rota e a **permissão da operação** que está executando (senão **\*
Acesso negado para esta operacao \***). Nenhuma dessas conferências grava.

---

## Cenários BDD

```gherkin
Funcionalidade: Registro do pedido de alimentação escolar de um fornecedor para um órgão da secretaria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenadoria regional escolar,
      o órgão filho e o código de acesso
    E tenho acesso à tela E020T

  Cenário: Incluir um pedido
    Dado que vim do menu E010M e o órgão filho é do meu alcance, está cadastrado,
      ativo, com os dados completos, é da minha secretaria e da minha coordenadoria
    E que o fornecedor está cadastrado e os mapas do órgão estão atualizados até o
      limite do perfil do tipo de órgão
    E que o início da entrega é uma data válida, em dia útil, que não é feriado
    E que informei 5 dias de entrega e a semana A
    Quando confirmo a inclusão
    Então o pedido recebe um número novo, com o ano da entrega
    E sou levado à tela E021T para distribuir os gêneros pelos dias de entrega

  Cenário: Incluir um pedido copiando outro
    Dado que estou na tela E020T para incluir
    E que informei o número e o ano de um pedido já cadastrado do meu órgão e até
      três dias de entrega dele, com quantidade cadastrada
    Quando confirmo a inclusão
    Então os gêneros daquele pedido são copiados para o pedido novo, com as
      quantidades daqueles dias
    E o pedido novo é gravado com o cabeçalho que informei
    E sou levado à tela E021T para continuar a distribuição

  Cenário: Alterar um pedido
    Dado que o pedido está cadastrado, é do meu órgão e da minha coordenadoria,
      não é acumulado, não está pendente de distribuição, não está aprovado nem
      fechado e nenhum gênero dele tem tipo de contrato
    Quando informo a operação de alterar, confirmo e a alteração é aceita
    Então sou levado à tela E021T, que abre em alteração

  Cenário: Excluir um pedido
    Dado que o pedido está cadastrado, é do meu órgão e da minha coordenadoria,
      não é acumulado, não está pendente de distribuição, não está aprovado nem
      fechado e nenhum gênero dele tem tipo de contrato
    Quando informo a operação de excluir e confirmo a exclusão
    Então os gêneros do pedido são apagados
    E o pedido é apagado
    E fica um registro de auditoria para cada registro apagado

  Cenário: Consultar um pedido
    Dado que existe um pedido do meu órgão e da minha coordenadoria, não acumulado
      e não pendente de distribuição
    Quando informo a operação de consultar
    Então vejo no cabeçalho o órgão, a coordenadoria, o fornecedor, o período e a
      semana do pedido
    E sou levado à tela E021T, que abre em consulta
    E nada é gravado

  Cenário: A tela reaberta pela tela seguinte começa um pedido novo
    Dado que a tela E021T me devolveu o cabeçalho de um pedido
    Quando a tela E020T é reaberta
    Então ela repõe o órgão, a coordenadoria, o fornecedor, o período e a semana
      que a tela E021T devolveu
    E o número do pedido e o ano da entrega vêm vazios
    E a quantidade de dias de entrega já vem preenchida com 5

  Cenário: A operação não é nenhuma das quatro
    Dado que estou na tela E020T
    Quando confirmo com uma operação que não é incluir, alterar, excluir nem
      consultar
    Então vejo "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: Campo numérico em branco antes das conferências
    Dado que estou na tela E020T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências do pedido

  Cenário: Órgão filho não informado
    Dado que estou na tela E020T para incluir
    Quando confirmo sem informar o órgão filho
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho fora do meu alcance
    Dado que o meu vínculo na sessão tem um órgão filho
    Quando confirmo um órgão filho diferente
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho não cadastrado
    Dado que estou na tela E020T para incluir
    Quando confirmo um órgão filho que não existe no cadastro de órgãos
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho inativo
    Dado que o cadastro do órgão filho está marcado como inativo
    Quando confirmo a inclusão
    Então vejo "* Orgao cadastrado como inativo *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho com dados incompletos
    Dado que falta um dos dados do cadastro do órgão filho — bairro, órgão pai,
      nome, endereço, quantidade de matrículas ou de pessoas
    Quando confirmo a inclusão
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho de outra secretaria
    Dado que o tipo de órgão do cadastro do órgão filho não é o da minha secretaria
    Quando confirmo a inclusão
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho de outra coordenadoria
    Dado que a coordenadoria do órgão filho não é a minha
    Quando confirmo a inclusão
    Então vejo "<- Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Fornecedor não cadastrado
    Dado que estou na tela E020T para incluir, com um órgão filho válido
    Quando confirmo um código de fornecedor que não existe no cadastro de
      fornecedores
    Então vejo "* Fornecedor nao cadastrado *"
    E o cursor fica no campo do fornecedor
    E nada é gravado

  Cenário: Início da entrega não é uma data válida
    Dado que estou na tela E020T para incluir
    Quando informo um dia, um mês ou um ano que não formam uma data do calendário
    Então vejo "* Data de inicio da entrega invalida *"
    E o cursor fica no campo do dia do início
    E nada é gravado

  Cenário: Início da entrega em um sábado
    Dado que estou na tela E020T para incluir
    Quando a data de início da entrega cai em um sábado
    Então vejo "* Inicio da entrega nao deve ser um sabado *"
    E o cursor fica no campo do dia do início
    E nada é gravado

  Cenário: Início da entrega em um domingo
    Dado que estou na tela E020T para incluir
    Quando a data de início da entrega cai em um domingo
    Então vejo "* Inicio da entrega nao deve ser um domingo *"
    E o cursor fica no campo do dia do início
    E nada é gravado

  Cenário: Início da entrega em um feriado do órgão
    Dado que a data de início da entrega está entre os feriados cadastrados para o
      tipo de órgão
    Quando confirmo a inclusão
    Então vejo "* Inicio da entrega nao deve ser um feriado *"
    E o cursor fica no campo do dia do início
    E nada é gravado

  Cenário: Os mapas do órgão não estão atualizados
    Dado que o órgão não está marcado como acumulado
    E que não há mapa do órgão e da coordenadoria até o limite que o perfil do tipo
      de órgão implica
    Quando confirmo a inclusão
    Então vejo "<- Antes, atualize os mapas ate a data inf. *" com o limite que
      falta cobrir
    E a inclusão não é feita
    E nada é gravado

  Cenário: Órgão marcado como acumulado não passa pela conferência dos mapas
    Dado que o cadastro do órgão está marcado como acumulado
    Quando confirmo a inclusão
    Então a conferência dos mapas não é feita
    E a inclusão segue para as demais conferências

  Cenário: Quantidade de dias de entrega não informada
    Dado que estou na tela E020T para incluir
    Quando confirmo com a quantidade de dias de entrega zerada
    Então vejo "* Informe a quantidade de dias de entrega *"
    E o cursor fica no campo da quantidade
    E nada é gravado

  Cenário: Quantidade de dias de entrega acima do máximo
    Dado que estou na tela E020T para incluir
    Quando confirmo com mais de 5 dias de entrega
    Então vejo "* Quantidade maxima de dias de entrega = 5 *"
    E o cursor fica no campo da quantidade
    E nada é gravado

  Cenário: Os dias de entrega pulam fins de semana e feriados
    Dado que informei 5 dias de entrega começando em uma sexta-feira
    Quando a tela monta os dias de entrega
    Então o primeiro dia é a própria data de início
    E os demais são os próximos dias que não são sábado, domingo nem feriado do
      tipo de órgão
    E o limite do período de entrega é o último desses dias

  Cenário: Semana da entrega inválida
    Dado que estou na tela E020T para incluir
    Quando confirmo com uma semana que não é A, B, C, D nem E
    Então vejo "* Informe semana com A / B / C / D / E *"
    E o cursor fica no campo da semana
    E nada é gravado

  Cenário: Pedido para cópia não cadastrado
    Dado que estou incluindo um pedido
    Quando informo, para cópia, o número e o ano de um pedido que não existe
    Então vejo "* Pedido para copia nao cadastrado *"
    E o cursor fica no número do pedido de origem
    E nada é gravado

  Cenário: Pedido para cópia de outro órgão
    Dado que o meu vínculo na sessão tem um órgão filho
    E que o pedido de origem para cópia é de outro órgão
    Quando confirmo a inclusão
    Então vejo " * Pedido para copia de outro orgao *"
    E o cursor fica no número do pedido de origem
    E nada é gravado

  Cenário: Dias de cópia sem quantidade cadastrada
    Dado que informei dias de cópia que não têm quantidade cadastrada no pedido de
      origem
    Quando confirmo a inclusão
    Então vejo "* Dias de copia sem quant.cadastradas *"
    E o cursor fica no primeiro dia de cópia
    E nada é gravado

  Cenário: Dia de cópia repetido
    Dado que informei o mesmo dia de cópia duas vezes
    Quando confirmo a inclusão
    Então vejo "* Nao repita dia de copia *"
    E o cursor fica no dia repetido
    E nada é gravado

  Cenário: Mais dias de cópia do que dias de entrega
    Dado que informei mais dias de cópia do que os dias de entrega do pedido novo
    Quando confirmo a inclusão
    Então vejo "* Dias de copia > dias entrega *"
    E o cursor fica no primeiro dia de cópia
    E nada é gravado

  Cenário: Dia de cópia que não está no pedido novo
    Dado que informei um dia de cópia que não é um dos dias de entrega do pedido
      novo
    Quando confirmo a inclusão
    Então vejo "* Dia nao cadastrado no pedido para copia *"
    E o cursor fica naquele dia
    E nada é gravado

  Cenário: Número do pedido não informado
    Dado que estou na tela E020T para alterar, excluir ou consultar
    Quando confirmo sem informar o número do pedido
    Então vejo "* Informe o numero do pedido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido não cadastrado
    Dado que estou na tela E020T para alterar, excluir ou consultar
    Quando confirmo um número e um ano que não existem para o meu órgão
    Então vejo "* Pedido nao cadastrado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido de outro órgão
    Dado que estou na tela E020T para alterar, excluir ou consultar
    Quando confirmo um pedido que é de outro órgão filho
    Então vejo "* Pedido de outro orgao *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido de outra coordenadoria
    Dado que o pedido é de uma coordenadoria que não é a minha
    Quando confirmo a alteração, a exclusão ou a consulta
    Então vejo "<- Usuario sem acesso ao grupo deste pedido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido de órgão acumulado
    Dado que o órgão do pedido está marcado como acumulado
    Quando confirmo a alteração, a exclusão ou a consulta
    Então vejo "* Pedido acumulado *"
    E nada é gravado

  Cenário: Pedido pendente de distribuição
    Dado que o pedido ainda não teve os gêneros distribuídos pelos dias de entrega
    Quando confirmo a alteração, a exclusão ou a consulta
    Então vejo "* Pedido pendente de distribuicao *"
    E nada é gravado

  Cenário: Pedido já aprovado
    Dado que a situação do pedido já é aprovado
    Quando confirmo a alteração
    Então vejo "* Pedido aprovado nao pode ser alterado *"
    E a alteração não é feita
    E nada é gravado

  Cenário: Pedido já fechado
    Dado que a situação do pedido já é fechado
    Quando confirmo a alteração
    Então vejo "* Pedido fechado nao pode ser alterado *"
    E a alteração não é feita
    E nada é gravado

  Cenário: Pedido com gênero de tipo de contrato
    Dado que ao menos um gênero do pedido tem tipo de contrato
    Quando confirmo a alteração
    Então vejo "* Pedido com tipo contrato nao pode ser alterado *"
    E nada é gravado

  Cenário: Pedido já excluído
    Dado que o pedido está marcado como excluído
    Quando confirmo a consulta
    Então vejo "* Pedido excluido *"
    E nada é gravado

  Cenário: Pedido aprovado não pode ser excluído
    Dado que a situação do pedido já é aprovado
    Quando confirmo a exclusão
    Então vejo "* Pedido aprovado nao pode ser excluido *"
    E nada é gravado

  Cenário: Pedido fechado não pode ser excluído
    Dado que a situação do pedido já é fechado
    Quando confirmo a exclusão
    Então vejo "* Pedido fechado nao pode ser excluido *"
    E nada é gravado

  Cenário: Pedido com gênero de tipo de contrato não pode ser excluído
    Dado que ao menos um gênero do pedido tem tipo de contrato
    Quando confirmo a exclusão
    Então vejo "* Pedido nao pode ser excluido *"
    E nada é gravado

  Cenário: Data final de entrega menor que a data inicial
    Dado que estou alterando ou consultando um pedido
    Quando o limite do período de entrega é anterior ao início
    Então vejo "* Data final de entrega menor que a data inicial *"
    E o cursor fica no campo do dia do início
    E nada é gravado

  Cenário: Já existe pedido no intervalo de entrega
    Dado que estou alterando um pedido do mesmo fornecedor
    E que o intervalo de entrega informado se sobrepõe ao de outro pedido do mesmo
      fornecedor
    Quando confirmo a alteração
    Então vejo "* Ja existe pedido neste intervalo de entrega *" com o número do
      pedido que já ocupa o intervalo
    E nada é gravado

  Cenário: A confirmação é pedida antes de gravar
    Dado que informei uma inclusão, uma alteração ou uma exclusão e ela passou por
      todas as conferências
    Quando a tela pede a confirmação
    Então vejo "* Confirma inclusao do pedido <S/N> ? *",
      "* Confirma alteracao do pedido <S/N> ? *" ou
      "* Confirma exclusao do pedido <S/N> ? *" conforme a operação
    E a operação só segue com a resposta afirmativa
    E, se os dados tiverem mudado entre a pergunta e a resposta, a confirmação é
      descartada e a tela confere tudo de novo

  Cenário: A consulta não pede confirmação
    Dado que pedi a consulta de um pedido
    Quando a tela o encontra
    Então ela não pede confirmação
    E abre a tela E021T em consulta
    E nada é gravado

  Cenário: A inclusão dá o número ao pedido e abre a tela seguinte
    Dado que confirmei a inclusão sem cópia de outro pedido
    Quando a tela termina a passagem
    Então o contador do ano avança e o pedido recebe o número seguinte
    E fica um registro de auditoria do contador
    E a tela E021T é aberta com a operação de incluir
    E o pedido e os gêneros ainda não existem: quem os grava é a tela E021T

  Cenário: O número do pedido começa em 1 quando não há pedido no ano
    Dado que ainda não há pedido no ano, para o meu tipo de órgão e a minha
      coordenadoria
    Quando confirmo a inclusão
    Então o pedido recebe o número 1
    E o contador do ano é criado

  Cenário: A exclusão apaga os gêneros e o pedido, com auditoria
    Dado que confirmei a exclusão de um pedido
    Quando a tela termina a passagem
    Então cada gênero do pedido é apagado
    E o pedido é apagado
    E fica um registro de auditoria para cada registro apagado
    E o contador do número do pedido não é tocado

  Cenário: A recusa não grava nada
    Dado que estou na tela E020T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então o pedido continua como estava
    E nenhum gênero foi incluído, alterado ou apagado
    E nenhum registro de auditoria foi incluído
    E nenhum contador foi tocado

  Cenário: O que a tela entrega à tela seguinte
    Dado que terminei uma inclusão, uma alteração ou uma consulta
    Quando a tela abre a E021T
    Então ela deixa para a tela seguinte o órgão com a descrição, a coordenadoria,
      o número do pedido, o fornecedor com a razão social, o período, a semana, a
      quantidade e os cinco dias de entrega
    E deixa a operação: consultar, se consultei; alterar, se alterei; incluir, se
      incluí sem cópia; e alterar, se incluí com cópia de outro pedido

  Cenário: A requisição de impressão do pedido
    Dado que preenchi o código de impressão
    Quando confirmo
    Então a operação passa a ser a de consulta
    E a tela procura o pedido como na consulta
    E monta a requisição de impressão do relatório do pedido com o número do
      pedido, a secretaria, a coordenadoria, a minha matrícula, a estação, uma
      cópia e o meu correio eletrônico
    E nenhum outro cadastro é tocado

  Cenário: Nada é gravado sem a conferência de sessão, de tela, de acesso e da operação
    Dado que estou na tela E020T
    Quando a conferência da estação, do registro da tela, do código de acesso, da
      rota ou da permissão da operação não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *"
      ou "* Acesso negado para esta operacao *"
    E nada é gravado
    E, se a estação não for a da minha sessão, o acesso é encerrado
```
