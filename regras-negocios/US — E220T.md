# US — E220T — Abertura do pedido acumulado de alimentação escolar

## Estória

Como **servidor de CRE**, quero **abrir o pedido acumulado de alimentação escolar
de um órgão filho para um fornecedor, com o período, a semana, o tipo de contrato e
o gênero**, para que **o órgão que recebe por acumulado passe a ter o pedido do
período — numerado, alterável, consultável e imprimível — e a secretaria consiga
distribuir os gêneros e conferir o que já foi recebido**.

O órgão marcado como acumulado no cadastro não entra no pedido comum: o pedido dele
é **um só por período, fornecedor e semana**, e é esta tela que o abre. É aqui que o
número do pedido nasce, e é daqui que a tela seguinte o recebe para distribuir os
gêneros; sem isso o órgão fica sem pedido no período e não há o que distribuir,
entregar nem conferir. É também por aqui que esse pedido se corrige, se desfaz e se
consulta, enquanto não está fechado.

## Contexto

Jornada S000M → E000M → E200M → E220M → E220T.
Ator: servidor de CRE — abre o pedido acumulado do órgão filho, informa o
fornecedor, o período, a semana, o tipo de contrato e o gênero, inclui, altera,
exclui, consulta ou pede a impressão, e segue para a tela de consulta ou para a que
recebe os gêneros.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Da sessão a tela usa o vínculo do servidor — a matrícula, o tipo de órgão, a
coordenadoria regional escolar, o órgão filho e o código de acesso —, e é dele que
sai o alcance do que ela deixa informar e gravar.

A tela não termina em si: ela reabre a si mesma para pedir a confirmação e, ao fim
da passagem, abre a `E221T`, que consulta o pedido acumulado, ou a `E222T`, que
recebe os gêneros do pedido. Para lá ela passa o órgão filho, a coordenadoria, o
pedido acumulado, o fornecedor, o período, a semana, o tipo de contrato, a subclasse
e o gênero, e a operação — e é essa operação que decide se a `E221T` e a `E222T`
abrem em consulta ou em alteração.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela só aceita incluir, alterar, excluir e consultar

O campo da operação aceita quatro coisas: **incluir**, **alterar**, **excluir** e
**consultar**. Sem nenhuma delas — campo em branco, valor estranho ou qualquer outra
coisa — a tela recusa com **\* Opcao nao disponivel. Use INC, ALT, EXC ou CON \***,
com o cursor de volta no campo da operação, e não grava nada.

[?] A tela compara a operação com quatro códigos internos de três letras — inclusão,
alteração, exclusão e consulta —, e não com as siglas que a mensagem manda usar; e o
valor que ela mesma escreve no campo, ao abri-lo para um pedido novo, é o código
interno da inclusão. Não se conclui do acervo se o terminal entrega a sigla já
traduzida ou se o campo é preenchido por outra via. Pergunta ao site.

### RN-02 — Os campos numéricos passam por edição numérica antes das conferências

Antes de qualquer conferência de negócio, **quinze campos** passam por edição
numérica: o órgão filho, a coordenadoria regional escolar, o número do pedido, o ano
da entrega, o código do fornecedor, o tipo de contrato, o operador, o dia, o mês e o
ano do início do período, o dia, o mês e o ano do limite, a subclasse e o gênero. O
campo em branco é tratado como zero, e o que não for número é recusado antes das
conferências. A operação, a próxima tela, a semana e a resposta da confirmação
**não** passam por essa edição. A cada mensagem, antes da edição, a tela apaga do
cabeçalho a descrição da secretaria, a data do sistema, a descrição do órgão, a do
fornecedor, a do operador, a do gênero e a mensagem da passagem anterior.

[?] A tela só sabe devolver o cursor a **dez** desses quinze campos: um erro de
digitação na coordenadoria regional escolar, no operador ou em qualquer um dos três
campos do limite não tem posição de cursor definida, e o que o servidor vê nesse
caso não se conclui desta tela. Pergunta ao site.

### RN-03 — A tela abre em inclusão, com o órgão e a coordenadoria do vínculo

Toda abertura começa um pedido novo: a operação é a **inclusão**, e o número do
pedido, o ano da entrega e o código de impressão vêm vazios. Vindo do vínculo da
sessão um órgão filho, a tela já o informa, traz a coordenadoria do vínculo e mostra
a descrição do órgão; **não vindo órgão do vínculo**, ela deixa o cursor no campo do
órgão, para o servidor informá-lo.

A tela **não** muda de comportamento conforme a tela que a chamou: ela é alcançada
pelo menu `E220M` e por si mesma, na reabertura da confirmação, e nas duas entradas
o que decide o que acontece é a operação que o servidor informa e o estado do pedido
procurado — nunca a origem.

### RN-04 — O órgão filho tem de ser informado, ser do acumulado e estar no alcance do servidor

O órgão filho (o SDI, de 8 dígitos) é a chave da tela. A tela recusa, com o cursor
de volta no campo do órgão e sem gravar nada:

- **\* Informe o orgao \*** — quando o órgão não foi informado;
- **\* Usuario sem acesso a outro orgao \*** — quando o vínculo da sessão tem um
  órgão filho e o servidor informa outro;
- **\* Orgao nao cadastrado \*** — quando o órgão trazido do vínculo não existe no
  cadastro de órgãos;
- **\* Orgao nao cadastrado \*** — quando o código informado não existe no cadastro
  de órgãos;
- **\* Orgao cadastrado como inativo \*** — quando o cadastro está marcado como
  inativo;
- **\* Orgao nao cadastrado para pedido acumulado \*** — quando o cadastro do órgão
  **não** está marcado como acumulado, que é o único caso que esta tela atende;
- **\* Orgao cadastrado com dados incompletos \*** — quando faltam, no cadastro, o
  bairro, o órgão pai, o nome, o endereço, a quantidade de matrículas ou a de
  pessoas;
- **\* Orgao nao pertence a esta secretaria \*** — quando o tipo de órgão do
  cadastro não é o da secretaria da sessão;
- **\* Usuario sem acesso ao grupo deste orgao \*** — quando a coordenadoria do
  servidor não é a coordenadoria do órgão.

Passando por isso, a descrição do órgão aparece no cabeçalho e a coordenadoria do
órgão passa a ser a do pedido — o que o servidor tiver digitado no campo da
coordenadoria é substituído pela do cadastro do órgão.

[?] A recusa **\* Orgao nao cadastrado \*** tem duas portas. Uma procura o código
informado no cadastro de órgãos; a outra decide pela descrição do órgão que veio do
vínculo da sessão, comparando-a com um texto fixo de não cadastrado — e esta tela
nunca escreve essa descrição: a que ela mostra vem do próprio cadastro. Ou o texto
chega de outro lugar pela área de trabalho da sessão, ou essa segunda porta não
abre. Não se conclui do acervo. Pergunta ao site.

### RN-05 — O fornecedor tem de estar cadastrado e não estar excluído

O código do fornecedor (4 dígitos) é procurado no cadastro de fornecedores. Não
existindo — ou estando marcado como excluído, que a tela não aceita — ela recusa com
**\* Fornecedor nao cadastrado \***, com o cursor no campo, e não grava nada.
Achado, a razão social do fornecedor aparece no cabeçalho.

[?] Quando o fornecedor informado está marcado como excluído, a tela volta a
procurá-lo pelo mesmo código, em laço; a única saída do laço é a releitura deixar de
devolver o registro. Das duas leituras, uma posiciona pelo código e a outra relê, e
nada no acervo diz se a releitura avança para o fornecedor seguinte. Se não avançar,
a tela fica presa nesse caso. Pergunta ao site.

### RN-06 — O tipo de contrato tem de estar cadastrado

O tipo de contrato é procurado no cadastro de tipos de contrato do par (secretaria,
tipo de contrato). Não existindo, a tela recusa com **\* Tipo contrato nao
cadastrado \***, com o cursor no campo, e não grava nada.

[?] O fornecedor é conferido contra a marca de exclusão do cadastro e o tipo de
contrato não é: um tipo de contrato marcado como excluído é aceito por esta tela. Ou
a conferência do fornecedor é que é o caso particular, ou faltou aqui a mesma
conferência. Pergunta ao site.

### RN-07 — O início do período não pode cair em sábado, domingo nem feriado

O dia, o mês e o ano do início do período formam a data de início da entrega. Ela é
recusada, com o cursor no campo do dia do início e sem gravar nada:

- **\* Inicio da entrega nao deve ser um sabado \*** — quando a data cai em um
  sábado;
- **\* Inicio da entrega nao deve ser um domingo \*** — quando a data cai em um
  domingo;
- **\* Inicio da entrega nao deve ser um feriado \*** — quando a data está entre os
  feriados cadastrados para o tipo de órgão.

[?] A tela converte a data informada, mas não confere se ela existe no calendário —
a tela irmã do pedido comum recusa a data inválida com mensagem própria, e esta não.
Do acervo só se conclui que o nome do dia da data convertida é o que decide as três
recusas acima; o que a tela mostra quando o dia, o mês e o ano não formam uma data
não se conclui daqui. Pergunta ao site.

### RN-08 — O período de entrega é sempre de cinco dias úteis

O pedido acumulado tem **cinco** dias de entrega: o primeiro é o próprio início, e
cada seguinte é o próximo dia que não seja sábado, domingo nem feriado do tipo de
órgão. O limite do período é o **quinto** desses dias, e é ele que aparece nos
campos do limite — não há campo para o servidor informar a quantidade de dias.

[?] A conferência de feriado dos dias seguintes só é feita para datas posteriores a
**01/09/2009**, uma data fixa comparada no meio do cálculo; para datas até ela, o dia
é tomado como útil mesmo que esteja no cadastro de feriados. Não se conclui do acervo
se a intenção era comparar com o período informado. Pergunta ao site.

### RN-09 — A semana da entrega tem de ser de A a E

O campo da semana da entrega aceita de **A** a **E**. Qualquer outro valor —
inclusive em branco — é recusado com **\* Informe semana com A / B / C / D / E \***,
com o cursor no campo, e nada é gravado.

### RN-10 — A subclasse e o gênero têm de estar cadastrados

O par (subclasse, gênero) é procurado, para a data de início do período, no cadastro
de gêneros. Não existindo — inclusive quando o gênero está marcado como excluído, que
esse cadastro não devolve — a tela recusa com **\* Genero nao cadastrado \***, com o
cursor no campo da subclasse, e não grava nada. Achado, a descrição resumida do
gênero acompanha o pedido.

### RN-11 — A permissão do contrato tem de existir e cobrir o período

Antes de abrir o pedido, a tela procura a permissão cadastrada para o conjunto
(secretaria, tipo de contrato, fornecedor, coordenadoria, subclasse e gênero) cujo
período cubra o do pedido. Ou ela não existe, ou o período do pedido começa antes do
período permitido, ou o limite do pedido passa do limite permitido: em qualquer
desses casos a recusa é **\* Permissao nao cadastrada ou fora do intervalo \***, com
o cursor no campo do dia do início, e nada é gravado. Achada a permissão, o operador
dela é o operador do pedido.

### RN-12 — O pedido acumulado já existente no mesmo período não ganha número novo

Ainda na inclusão, a tela procura pedidos acumulados do **mesmo órgão, mesma
coordenadoria, mesmo fornecedor e mesmo início de período** e, em cada um deles, um
gênero do **mesmo tipo de contrato**. Achando, compara a semana: valem como iguais
os dois pedidos com a semana **E** e os dois com uma semana determinada — qualquer
uma —, e nesse caso o pedido existente é o dono do período. A tela então pergunta a
confirmação e, confirmada, **não** cria número novo: abre o pedido que já existe, em
alteração, na tela dos gêneros, e passa a semana do pedido existente para o lugar da
informada.

Se o pedido encontrado não estiver registrado como acumulado, ou estiver como
acumulado calculado, ou como auxiliar do acumulado calculado, ou estiver fechado, a
confirmação da inclusão é recusada com **<- Pedido nao cadastrado como acumulado
\***, **<- Pedido acumulado calculado \***, **\* Pedido auxiliar do acumulado
calculado \***, ou **<- Pedido fechado \***, respectivamente, com o cursor no campo
do dia do início — menos na terceira, em que o cursor fica no número do pedido.

[?] A comparação da semana trata como iguais dois pedidos com semanas determinadas
diferentes: informada a semana B e existindo um pedido da semana A do mesmo início,
a tela adota a semana A e segue para o pedido existente. Não se conclui do acervo se
a intenção era comparar as letras. Pergunta ao site.

### RN-13 — O pedido se identifica pelo número e pelo ano, e tem de estar registrado como acumulado

Nas operações de alterar, excluir, consultar e na requisição de impressão, o servidor
informa o número do pedido e o ano da entrega — juntos, os dez dígitos que
identificam o pedido acumulado. A tela recusa, sem gravar nada:

- **\* Informe o numero do pedido \*** — quando o número não foi informado, com o
  cursor no campo;
- **\* Pedido nao cadastrado \*** — quando o pedido não existe para a coordenadoria
  do órgão, com o cursor no número do pedido;
- **\* Pedido nao cadastrado como acumulado \*** — quando o pedido existe mas não
  está registrado como acumulado;
- **\* Pedido acumulado calculado \*** — quando o pedido está registrado como
  acumulado calculado;
- **\* Pedido auxiliar do acumulado calculado \*** — quando o pedido está registrado
  como auxiliar do acumulado calculado.

Passando por isso, a tela repõe no cabeçalho o órgão com a descrição, a
coordenadoria, o fornecedor com a razão social, o operador com o nome, o período, a
semana e o tipo de contrato que estão no pedido procurado.

[?] Os dez dígitos do pedido acumulado são montados como número do pedido mais **ano
da entrega** quando a tela procura o pedido, e como número do pedido mais **ano do
início do período** quando ela o entrega à tela seguinte; e o contador de onde o
número sai é procurado pelo ano do início do período, embora o campo dele no acervo
se chame ano da entrega. Se os dois anos divergirem, não se conclui do acervo qual
deles identifica o pedido. Pergunta ao site.

### RN-14 — A alteração exige o gênero no pedido, e o pedido e o gênero não podem estar fechados

Na alteração, o gênero é procurado no pedido acumulado. Não estando lá, a recusa é
**\* Genero nao cadastrado neste pedido \***, com o cursor no campo da subclasse, e
nada é gravado. Estado o gênero:

- **\* Pedido fechado \*** — quando o pedido está fechado, com o cursor no número
  do pedido;
- **\* Genero fechado no pedido \*** — quando aquele gênero do pedido está fechado,
  com o cursor no campo do gênero.

### RN-15 — A exclusão exige gêneros e recusa pedido com quantidades recebidas

Na exclusão a tela percorre os gêneros do pedido acumulado. Sem nenhum gênero
cadastrado a recusa é **\* Pedido sem generos cadastrados \***, com o cursor no
campo da subclasse. Havendo gênero com quantidade recebida — o acumulado já recebeu
alguma coisa —, a recusa é **\* Ja existem quantidades recebidas \***, com o cursor
no número do pedido, e o pedido não é apagado.

### RN-16 — A tela pede confirmação antes de gravar

Antes de incluir, alterar ou excluir, a tela reabre a si mesma com a pergunta no
campo de resposta: **\* Confirma inclusao do pedido <S/N> ? \***, **\* Confirma
alteracao do pedido <S/N> ? \*** ou **\* Confirma exclusao do pedido <S/N> ? \***,
conforme a operação, com o cursor no campo da resposta. Só com a resposta afirmativa
a operação segue; **entre a pergunta e a resposta a tela confere que nada mudou** —
a operação, o órgão, o fornecedor, a semana, as três partes do início, o pedido
acumulado, a subclasse e o gênero. Se algum deles mudou, a confirmação é descartada e
a tela volta a conferir tudo antes de perguntar de novo. A consulta e a requisição de
impressão não pedem confirmação.

[?] Quando a resposta é negativa, a tela descarta a confirmação e volta a conferir
tudo; no caminho da inclusão ela chega outra vez à pergunta, porque a passagem que
pede a confirmação é a mesma que confere os dados. Não se conclui do acervo se o
servidor consegue desistir da inclusão respondendo "não". Pergunta ao site.

### RN-17 — O que a inclusão grava

Confirmada a inclusão **sem** pedido já existente no período, a tela dá o número ao
pedido:

- o número sai de um contador por tipo de órgão, coordenadoria regional escolar e
  ano: ela soma 1 ao último número do ano e, quando ainda não há pedido no ano,
  começa em **1** e cria o contador;
- o contador deixa um registro de auditoria — de inclusão quando o número é o **1**,
  de alteração nos demais casos;
- a tela **não** grava o pedido nem os gêneros: quem os grava é a tela seguinte
  (`E222T`), que ela abre em alteração com o pedido acumulado recém-numerado.

Confirmada a inclusão **com** pedido já existente no período (RN-12), nada é criado:
o contador não é tocado, e a tela seguinte abre com o pedido existente.

### RN-18 — O que a exclusão grava

Confirmada a exclusão, a tela desfaz o vínculo dos gêneros que apontam para o pedido
acumulado — reescrevendo cada um sem o vínculo e deixando um registro de auditoria de
alteração com o conteúdo anterior —, depois apaga os gêneros que **são** do pedido
acumulado e, por fim, apaga o próprio pedido, deixando um registro de auditoria de
exclusão para cada registro apagado. O contador do número do pedido **não** é tocado.

[?] O laço que desfaz o vínculo limpa, em cada registro que lê, exatamente o campo
pelo qual está varrendo, e volta a varrer pelo mesmo valor; não se conclui do acervo
se a varredura alcança todos os gêneros vinculados ou se perde a posição depois do
primeiro. Pergunta ao site.

### RN-19 — A consulta não grava nada e abre a tela de consulta

Na consulta a tela exige que o pedido acumulado tenha ao menos um gênero
(**\* Pedido sem generos cadastrados \***, com o cursor no campo da subclasse,
quando não tem) e, achado o pedido com gêneros, **não pede confirmação**, não cria,
não altera e não apaga nada, e abre a tela `E221T` em consulta, levando o pedido e o
cabeçalho que a tela já havia composto.

### RN-20 — O que a tela entrega à tela seguinte

Terminada a passagem, a tela deixa na área de trabalho da sessão, para a tela
seguinte, o órgão filho com a descrição, a coordenadoria regional escolar, o pedido
acumulado, o fornecedor com a razão social, o operador com o nome, o período, a
semana, o tipo de contrato, a subclasse e o gênero com a descrição resumida, e a
operação — e abre:

- a **`E221T`**, com a operação de **consultar**, quando o servidor consultou;
- a **`E222T`**, com a operação de **alterar**, quando o servidor alterou, quando ele
  incluiu sobre um pedido que já existia no período (RN-12) ou quando a inclusão
  confirmada acabou de receber o número (RN-17) — nos dois últimos casos a tela
  seguinte é quem grava o pedido e os gêneros do acumulado.

A exclusão não segue para outra tela: ela termina aqui. A `E221T` e a `E222T` decidem
pela operação entregue se abrem em consulta ou em alteração: entregue a consulta, a
`E221T` abre em consulta; entregue a alteração, a `E222T` abre em alteração e deixa
incluir, alterar e excluir gêneros.

### RN-21 — A requisição de impressão do pedido

Quando o servidor preenche o código de impressão, a operação que ele havia marcado é
**descartada** e a tela passa a procurar o pedido como na consulta (RN-13): o número
do pedido passa a ser obrigatório, e as recusas de estado do pedido valem. Achado, ela
monta a requisição de impressão do acumulado com o pedido, a secretaria (o tipo de
órgão), a coordenadoria, a matrícula do servidor, a estação, uma cópia e o endereço
de correio eletrônico do cadastro do servidor, e a entrega ao serviço de requisições
do sistema. Nenhum cadastro é gravado, e a tela não segue para outra.

### RN-22 — Nada é gravado sem a conferência de tela, de acesso e da operação

Na abertura, a tela confere que a estação é a mesma em que a sessão foi aberta — não
sendo, o acesso é encerrado —, que a tela está registrada (senão **\* Tela nao
disponivel \***) e que o código de acesso do servidor alcança a tela (senão **\*
Acesso negado para esta matricula \***). Em toda passagem de mensagem ela repõe, do
vínculo da sessão, a matrícula, o tipo de órgão, a coordenadoria, o órgão filho, o
acesso e o privilégio, entrega ao despacho de telas o código da próxima tela
informada — que, existindo e estando registrada, é aberta — e confere a **permissão
da operação** que está executando (senão **\* Acesso negado para esta operacao \***).
Nenhuma dessas conferências grava.

---

## Cenários BDD

```gherkin
Funcionalidade: Abertura do pedido acumulado de alimentação escolar de um órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenadoria regional escolar,
      o órgão filho, o código de acesso e a matrícula
    E tenho acesso à tela E220T

  Cenário: Incluir um pedido acumulado
    Dado que o órgão filho é do meu alcance, está cadastrado, ativo, marcado como
      acumulado, com os dados completos, é da minha secretaria e da minha
      coordenadoria
    E que o fornecedor está cadastrado e não excluído e o tipo de contrato existe
      para a minha secretaria
    E que o início do período é um dia útil que não é feriado e a semana é A
    E que o par de subclasse e gênero está cadastrado
    E que há permissão cadastrada para esse contrato cobrindo o período
    E que não existe pedido acumulado do mesmo fornecedor e início com gênero do
      mesmo tipo de contrato
    Quando confirmo a inclusão
    Então o pedido recebe um número novo, com o ano
    E sou levado à tela E222T, que abre em alteração para receber os gêneros

  Cenário: Incluir um pedido acumulado que já existe no período
    Dado que existe pedido acumulado do mesmo órgão, coordenadoria, fornecedor e
      início, com gênero do mesmo tipo de contrato e a mesma semana
    Quando confirmo a inclusão
    Então nenhum número novo é criado
    E sou levado à tela E222T com o pedido que já existe, em alteração
    E a semana do pedido existente passa a ser a do pedido

  Cenário: Alterar um pedido acumulado
    Dado que o pedido está cadastrado para o meu órgão e a minha coordenadoria,
      registrado como acumulado, não está fechado
    E que o gênero informado está no pedido e não está fechado
    Quando informo a operação de alterar e confirmo
    Então sou levado à tela E222T, que abre em alteração

  Cenário: Excluir um pedido acumulado
    Dado que o pedido está cadastrado, registrado como acumulado, tem gêneros e
      nenhum deles tem quantidade recebida
    Quando informo a operação de excluir e confirmo a exclusão
    Então os gêneros vinculados ao pedido são reescritos sem o vínculo
    E os gêneros do pedido são apagados
    E o pedido é apagado
    E fica um registro de auditoria para cada registro reescrito ou apagado
    E o contador do número do pedido não é tocado

  Cenário: Consultar um pedido acumulado
    Dado que existe um pedido acumulado do meu órgão e da minha coordenadoria, com
      gêneros
    Quando informo a operação de consultar
    Então vejo no cabeçalho o órgão, a coordenadoria, o fornecedor, o operador, o
      período, a semana e o tipo de contrato do pedido
    E sou levado à tela E221T, que abre em consulta
    E nada é gravado

  Cenário: A operação não é nenhuma das quatro
    Dado que estou na tela E220T
    Quando confirmo com uma operação que não é incluir, alterar, excluir nem
      consultar
    Então vejo "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: Campo numérico em branco antes das conferências
    Dado que estou na tela E220T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências do pedido

  Cenário: A tela abre em inclusão com o órgão e a coordenadoria do vínculo
    Dado que o meu vínculo na sessão tem um órgão filho
    Quando a tela E220T é aberta
    Então a operação já vem como incluir
    E o órgão filho e a coordenadoria do vínculo já vêm informados
    E vejo a descrição do órgão no cabeçalho
    E o número do pedido, o ano da entrega e o código de impressão vêm vazios

  Cenário: A tela abre sem órgão no vínculo
    Dado que o meu vínculo na sessão não tem órgão filho
    Quando a tela E220T é aberta
    Então o cursor já fica no campo do órgão filho, para eu informá-lo

  Cenário: Órgão filho não informado
    Dado que estou na tela E220T
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

  Cenário: Órgão do vínculo não cadastrado
    Dado que o órgão filho que o meu vínculo traz não existe no cadastro de órgãos
    Quando a tela E220T é aberta
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho não cadastrado
    Dado que estou na tela E220T
    Quando confirmo um órgão filho que não existe no cadastro de órgãos
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho inativo
    Dado que o cadastro do órgão filho está marcado como inativo
    Quando confirmo
    Então vejo "* Orgao cadastrado como inativo *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão que não é do acumulado
    Dado que o cadastro do órgão filho não está marcado como acumulado
    Quando confirmo
    Então vejo "* Orgao nao cadastrado para pedido acumulado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho com dados incompletos
    Dado que falta um dos dados do cadastro do órgão filho — bairro, órgão pai,
      nome, endereço, quantidade de matrículas ou de pessoas
    Quando confirmo
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho de outra secretaria
    Dado que o tipo de órgão do cadastro do órgão filho não é o da minha secretaria
    Quando confirmo
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho de outra coordenadoria
    Dado que a coordenadoria do cadastro do órgão filho não é a minha
    Quando confirmo
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Fornecedor não cadastrado
    Dado que estou na tela E220T para incluir, com um órgão filho válido
    Quando confirmo um código de fornecedor que não existe ou está excluído
    Então vejo "* Fornecedor nao cadastrado *"
    E o cursor fica no campo do fornecedor
    E nada é gravado

  Cenário: Tipo de contrato não cadastrado
    Dado que estou na tela E220T para incluir, com órgão e fornecedor válidos
    Quando confirmo um tipo de contrato que não existe para a minha secretaria
    Então vejo "* Tipo contrato nao cadastrado *"
    E o cursor fica no campo do tipo de contrato
    E nada é gravado

  Cenário: Início do período em um sábado
    Dado que estou na tela E220T para incluir
    Quando o início do período cai em um sábado
    Então vejo "* Inicio da entrega nao deve ser um sabado *"
    E o cursor fica no campo do dia do início
    E nada é gravado

  Cenário: Início do período em um domingo
    Dado que estou na tela E220T para incluir
    Quando o início do período cai em um domingo
    Então vejo "* Inicio da entrega nao deve ser um domingo *"
    E o cursor fica no campo do dia do início
    E nada é gravado

  Cenário: Início do período em um feriado do órgão
    Dado que o início do período está entre os feriados cadastrados para o tipo de
      órgão
    Quando confirmo
    Então vejo "* Inicio da entrega nao deve ser um feriado *"
    E o cursor fica no campo do dia do início
    E nada é gravado

  Cenário: O limite do período é o quinto dia útil
    Dado que o início do período cai em uma sexta-feira e o dia seguinte é feriado
    Quando a tela monta o período de entrega
    Então o primeiro dia é o próprio início
    E os quatro dias seguintes são os próximos dias que não são sábado, domingo nem
      feriado do tipo de órgão
    E o limite do período é o quinto desses dias

  Cenário: Semana da entrega inválida
    Dado que estou na tela E220T para incluir
    Quando confirmo com uma semana que não é A, B, C, D nem E
    Então vejo "* Informe semana com A / B / C / D / E *"
    E o cursor fica no campo da semana
    E nada é gravado

  Cenário: Gênero não cadastrado
    Dado que estou na tela E220T para incluir, com o período já aceito
    Quando confirmo um par de subclasse e gênero que não existe no cadastro, ou
      cujo gênero está excluído
    Então vejo "* Genero nao cadastrado *"
    E o cursor fica no campo da subclasse
    E nada é gravado

  Cenário: Permissão não cadastrada ou fora do intervalo
    Dado que estou na tela E220T para incluir, com o período já aceito
    Quando não existe permissão para o contrato, ou o período do pedido não cabe
      no intervalo permitido
    Então vejo "* Permissao nao cadastrada ou fora do intervalo *"
    E o cursor fica no campo do dia do início
    E nada é gravado

  Cenário: Número do pedido não informado
    Dado que estou na tela E220T para alterar, excluir, consultar ou imprimir
    Quando confirmo sem informar o número do pedido
    Então vejo "* Informe o numero do pedido *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido não cadastrado
    Dado que estou na tela E220T para alterar, excluir, consultar ou imprimir
    Quando confirmo um número e um ano que não existem para a minha coordenadoria
    Então vejo "* Pedido nao cadastrado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido não registrado como acumulado
    Dado que o pedido existe mas não está registrado como acumulado
    Quando confirmo a alteração, a exclusão, a consulta ou a impressão
    Então vejo "* Pedido nao cadastrado como acumulado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Pedido registrado como acumulado calculado
    Dado que o pedido está registrado como acumulado calculado
    Quando confirmo a alteração, a exclusão, a consulta ou a impressão
    Então vejo "* Pedido acumulado calculado *"
    E nada é gravado

  Cenário: Pedido registrado como auxiliar do acumulado calculado
    Dado que o pedido está registrado como auxiliar do acumulado calculado
    Quando confirmo a alteração, a exclusão, a consulta ou a impressão
    Então vejo "* Pedido auxiliar do acumulado calculado *"
    E nada é gravado

  Cenário: Gênero não cadastrado no pedido
    Dado que estou alterando um pedido acumulado
    Quando confirmo um par de subclasse e gênero que não está no pedido
    Então vejo "* Genero nao cadastrado neste pedido *"
    E o cursor fica no campo da subclasse
    E nada é gravado

  Cenário: Pedido fechado
    Dado que o pedido acumulado está fechado
    Quando confirmo a alteração
    Então vejo "* Pedido fechado *"
    E o cursor fica no número do pedido
    E nada é gravado

  Cenário: Gênero fechado no pedido
    Dado que o gênero informado está fechado no pedido
    Quando confirmo a alteração
    Então vejo "* Genero fechado no pedido *"
    E o cursor fica no campo do gênero
    E nada é gravado

  Cenário: Pedido sem gêneros cadastrados
    Dado que o pedido acumulado não tem nenhum gênero cadastrado
    Quando confirmo a exclusão ou a consulta
    Então vejo "* Pedido sem generos cadastrados *"
    E o cursor fica no campo da subclasse
    E nada é gravado

  Cenário: Pedido com quantidades recebidas
    Dado que ao menos um gênero do pedido tem quantidade recebida
    Quando confirmo a exclusão
    Então vejo "* Ja existem quantidades recebidas *"
    E o cursor fica no número do pedido
    E o pedido não é apagado

  Cenário: A confirmação é pedida antes de gravar
    Dado que informei uma inclusão, uma alteração ou uma exclusão e ela passou por
      todas as conferências
    Quando a tela pede a confirmação
    Então vejo "* Confirma inclusao do pedido <S/N> ? *",
      "* Confirma alteracao do pedido <S/N> ? *" ou
      "* Confirma exclusao do pedido <S/N> ? *" conforme a operação
    E o cursor fica no campo da resposta
    E a operação só segue com a resposta afirmativa

  Cenário: A confirmação é descartada quando os dados mudam
    Dado que a tela pediu a confirmação de uma operação
    Quando respondo que sim, mas mudo a operação, o órgão, o fornecedor, a semana,
      o início do período, o pedido acumulado, a subclasse ou o gênero
    Então a confirmação é descartada
    E a tela confere tudo de novo antes de perguntar outra vez

  Cenário: A consulta não pede confirmação
    Dado que pedi a consulta de um pedido acumulado com gêneros
    Quando a tela o encontra
    Então ela não pede confirmação
    E abre a tela E221T em consulta
    E nada é gravado

  Cenário: A inclusão dá o número ao pedido
    Dado que confirmei a inclusão e não existe pedido acumulado no período
    Quando a tela termina a passagem
    Então o contador do ano avança e o pedido recebe o número seguinte
    E fica um registro de auditoria do contador
    E a tela E222T é aberta com o pedido acumulado, em alteração
    E o pedido e os gêneros ainda não existem: quem os grava é a tela E222T

  Cenário: O número do pedido começa em 1 quando não há pedido no ano
    Dado que ainda não há pedido acumulado no ano, para o meu tipo de órgão e a
      minha coordenadoria
    Quando confirmo a inclusão
    Então o pedido recebe o número 1
    E o contador do ano é criado

  Cenário: A exclusão desvincula, apaga os gêneros e apaga o pedido
    Dado que confirmei a exclusão de um pedido acumulado
    Quando a tela termina a passagem
    Então cada gênero vinculado ao pedido é reescrito sem o vínculo, com um
      registro de auditoria de alteração
    E cada gênero do pedido é apagado, com um registro de auditoria de exclusão
    E o pedido é apagado, com um registro de auditoria de exclusão
    E o contador do número do pedido não é tocado

  Cenário: A consulta e a recusa não gravam nada
    Dado que consultei um pedido acumulado ou que a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então o pedido e os gêneros continuam como estavam
    E nenhum contador foi tocado
    E nenhum registro de auditoria foi incluído

  Cenário: O que a tela entrega à tela seguinte
    Dado que terminei uma inclusão, uma alteração ou uma consulta
    Quando a tela abre a E221T ou a E222T
    Então ela deixa o órgão com a descrição, a coordenadoria, o pedido acumulado, o
      fornecedor com a razão social, o operador com o nome, o período, a semana, o
      tipo de contrato e a subclasse com o gênero
    E deixa a operação: consultar, se consultei; alterar, se alterei ou se incluí
    E a tela seguinte decide por essa operação se abre em consulta ou em alteração

  Cenário: A requisição de impressão do pedido
    Dado que preenchi o código de impressão e informei um pedido acumulado válido
    Quando confirmo
    Então a operação que eu havia marcado é descartada
    E a tela procura o pedido como na consulta
    E monta a requisição de impressão do acumulado com o pedido, a secretaria, a
      coordenadoria, a minha matrícula, a estação, uma cópia e o meu correio
      eletrônico
    E nenhum cadastro é gravado, e a tela não segue para outra

  Cenário: Nada é gravado sem a conferência de tela, de acesso e da operação
    Dado que estou na tela E220T
    Quando a conferência da estação, do registro da tela, do código de acesso ou da
      permissão da operação não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *"
      ou "* Acesso negado para esta operacao *"
    E nada é gravado
    E, se a estação não for a da minha sessão, o acesso é encerrado
```
