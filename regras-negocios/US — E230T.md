# US — E230T — Pedir as quantidades de gênero de um órgão filho no pedido do ano

## Estória

Como **servidor de CRE**, quero **pedir, alterar, excluir e consultar a quantidade
de cada gênero que um órgão filho vai receber no pedido do ano**, para que **a
unidade receba o que precisa, dentro do que a permissão de fornecimento do contrato
ainda permite, e a secretaria consiga conferir depois o que foi pedido e o que já
foi recebido**.

O pedido do ano reúne, por órgão filho, fornecedor e período de entrega, os gêneros
que a unidade vai receber. É esta tela que transforma a necessidade em quantidade
pedida: ela confere o gênero, o período, a semana da entrega e a permissão do
contrato, e guarda o que foi pedido ao lado do que já foi recebido. Sem ela o gênero
não entra no pedido do órgão, e o que depende dele — a entrega, a nota fiscal e a
conferência do recebido — não acontece; e sem o saldo da permissão, a quantidade não
pode ser aumentada.

## Contexto

Jornada S000M → E000M → E200M → E230M → E230T.
Ator: servidor de CRE — informa e mantém, para um órgão filho, a quantidade pedida de
cada gênero do pedido do ano.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da **tela desta jornada**. Nenhuma delas repete as regras
da entrada: o que a tela revela sobre o que veio do `LOGON` está registrado no anexo
de evidências.

---

## Regras de negócio

### RN-01 — A tela só aceita incluir, alterar, excluir e consultar

O campo da operação aceita quatro coisas: **incluir**, **alterar**, **excluir** e
**consultar**. Sem nenhuma delas — campo em branco, valor estranho ou qualquer outra
coisa — a tela recusa com **\* Opcao nao disponivel. Use INC, ALT, EXC ou CON \***,
devolve o cursor ao campo da operação e não grava nada.

[?] A tela compara a operação com quatro códigos internos de três letras — os mesmos
que ela própria escreve no campo ao abri-lo para um pedido novo — e não com as siglas
que a mensagem manda usar. Não se conclui do acervo se o terminal entrega a sigla já
traduzida ou se a mensagem está desalinhada da comparação. Pergunta ao site.

### RN-02 — Os campos numéricos passam por edição numérica antes das conferências

Antes de qualquer conferência de negócio, **dezesseis campos** passam por edição
numérica: o órgão filho, a coordenadoria regional escolar, o número do pedido, o ano
da entrega, o código do fornecedor, o tipo de contrato, o operador, o dia, o mês e o
ano do início do período, o dia, o mês e o ano do limite, o código da subclasse, o
código do gênero e a quantidade a ser pedida. O campo em branco é tratado como zero,
e o que não for número é recusado antes das conferências de negócio. A operação, a
semana da entrega, o código de impressão e a resposta da confirmação **não** passam
por essa edição.

A cada mensagem, a tela apaga do cabeçalho a descrição da secretaria, a data do
sistema, a descrição do órgão, a razão social do fornecedor, o nome do operador, a
descrição resumida do gênero e a mensagem da passagem anterior.

A tela devolve o cursor a **onze** dos dezesseis campos conferidos: a coordenadoria
regional escolar, o operador e as três partes do limite ficam sem posição de erro.

### RN-03 — A tela abre em inclusão, com o órgão e a coordenadoria do vínculo

Toda abertura começa um pedido novo: a operação é a **inclusão**, e o número do
pedido, o ano da entrega e o código de impressão vêm vazios. Vindo do vínculo da
sessão um órgão filho, a tela já o informa e traz a coordenadoria do vínculo; não
vindo órgão do vínculo, o cursor fica no campo do órgão, para o servidor informá-lo.

A tela **não** muda de comportamento conforme a tela que a chamou: ela é alcançada
pelo menu `E230M` e por si mesma, na reabertura da confirmação, e nas duas entradas o
que decide o que acontece é a operação informada e o estado do pedido procurado —
nunca a origem.

### RN-04 — O órgão filho tem de ser informado, ser do acumulado e estar no alcance do servidor

O órgão filho (o SDI, de 8 dígitos) é a chave da tela. A tela recusa, com o cursor de
volta no campo do órgão e sem gravar nada:

- **\* Informe o orgao \*** — quando o órgão não foi informado;
- **\* Usuario sem acesso a outro orgao \*** — quando o vínculo da sessão tem um
  órgão filho e o servidor informa outro;
- **\* Orgao nao cadastrado \*** — quando o órgão trazido do vínculo não existe no
  cadastro de órgãos;
- **\* Orgao nao cadastrado \*** — quando o código informado não existe no cadastro
  de órgãos, ou quando o cadastro dele está marcado como excluído;
- **\* Orgao cadastrado como inativo \*** — quando o cadastro está marcado como
  inativo;
- **\* Orgao nao cadastrado para pedido acumulado \*** — quando o cadastro do órgão
  **não** está marcado como acumulado, que é o único caso que esta tela atende;
- **\* Orgao cadastrado com dados incompletos \*** — quando faltam, no cadastro, o
  bairro, o órgão pai, o nome, o endereço, a quantidade de matrículas ou a de
  pessoas;
- **\* Orgao nao pertence a esta secretaria \*** — quando o tipo de órgão do cadastro
  não é o da secretaria da sessão;
- **\* Usuario sem acesso ao grupo deste orgao \*** — quando a coordenadoria do
  servidor não é a coordenadoria do órgão.

Passando por isso, a descrição do órgão aparece no cabeçalho e a coordenadoria do
órgão passa a ser a do pedido — o que o servidor tiver digitado no campo da
coordenadoria é substituído pela do cadastro do órgão.

[?] A recusa **\* Orgao nao cadastrado \*** tem duas portas. Uma procura o código
informado no cadastro de órgãos; a outra decide pela descrição do órgão que veio do
vínculo da sessão, comparando-a com um texto fixo de não cadastrado — e esta tela
nunca escreve essa descrição: a que ela mostra vem do próprio cadastro. Ou o texto
chega de outro lugar pela área de trabalho da sessão, ou essa segunda porta não abre.
Não se conclui do acervo. Pergunta ao site.

### RN-05 — O fornecedor e o tipo de contrato têm de estar cadastrados

Na inclusão, o código do fornecedor (4 dígitos) é procurado no cadastro de
fornecedores. Não existindo — ou estando marcado como excluído, que essa procura não
devolve — a tela recusa com **\* Fornecedor nao cadastrado \***, com o cursor no
campo, e não grava nada. Achado, a razão social do fornecedor aparece no cabeçalho.

Ainda na inclusão, o tipo de contrato é procurado no cadastro de tipos de contrato do
par (secretaria, tipo de contrato). Não existindo, a tela recusa com **\* Tipo
contrato nao cadastrado \***, com o cursor no campo, e não grava nada. Achado, a
permissão de fornecimento daquele contrato é procurada (RN-11).

### RN-06 — O início do período não pode cair em sábado, domingo nem feriado

O dia, o mês e o ano do início do período formam a data de início da entrega. Ela é
recusada, com o cursor no campo do dia do início e sem gravar nada:

- **\* Inicio da entrega nao deve ser um sabado \*** — quando a data cai em um
  sábado;
- **\* Inicio da entrega nao deve ser um domingo \*** — quando a data cai em um
  domingo;
- **\* Inicio da entrega nao deve ser um feriado \*** — quando a data está entre os
  feriados cadastrados para o tipo de órgão.

### RN-07 — O período de entrega é sempre de cinco dias úteis, e o limite é calculado pela tela

O pedido do órgão tem **cinco** dias de entrega: o primeiro é o próprio início, e
cada seguinte é o próximo dia que não seja sábado, domingo nem feriado do tipo de
órgão. O limite do período é o **quinto** desses dias, e é ele que a tela mostra no
campo do limite — não há campo para o servidor informar a quantidade de dias.

[?] As três partes do limite são conferidas como numéricas como qualquer outro campo
digitável, mas a tela sempre as substitui pelo quinto dia útil calculado: o que o
servidor tiver digitado ali é descartado. Ou o campo é apenas de leitura na prática,
ou a conferência dele não serve para nada. Pergunta ao site.

### RN-08 — A semana da entrega tem de ser de A a E

O campo da semana da entrega aceita de **A** a **E**. Qualquer outro valor — inclusive
em branco — é recusado com **\* Informe semana com A / B / C / D / E \***, com o
cursor no campo, e nada é gravado.

[?] O acervo só diz que a semana vai de A a E: não há, no corpus, o que cada letra
significa no calendário de entregas da secretaria, nem se a semana informada tem de
coincidir com a do pedido do período. Não se conclui. Pergunta ao site.

### RN-09 — O gênero tem de estar cadastrado, e a quantidade tem de respeitar a fração do gênero

O par (código da subclasse, código do gênero) é procurado, para a data de início do
período, no cadastro de gêneros. Não existindo — inclusive quando o gênero está
marcado como excluído, que esse cadastro não devolve — a tela recusa com **\* Genero
nao cadastrado \***, com o cursor no campo da subclasse, e não grava nada. Achado, a
descrição resumida do gênero aparece no cabeçalho.

O gênero traz a fração em que ele é fornecido. A quantidade pedida tem de ser um
múltiplo exato dessa fração; sobrando resto na divisão, a recusa é **\* Quant.
fracionada invalida para este genero \***, com o cursor no campo da quantidade, e
nada é gravado.

### RN-10 — A quantidade a ser pedida tem de ser informada e ser menor que 100.000

A quantidade a ser pedida é obrigatória: em branco ou zerada, a recusa é **\*
Informe quantidade a ser pedida \***. Informada, ela tem de ser **menor que
100.000**; a partir daí a recusa é **\* Quantidade deve ser < 100000 \***. Nas duas,
o cursor volta ao campo da quantidade e nada é gravado.

### RN-11 — A permissão do contrato tem de existir, cobrir o período e trazer o operador

A tela procura a permissão cadastrada para o conjunto (secretaria, tipo de contrato,
fornecedor, coordenadoria, subclasse e gênero) cujo período cubra o do pedido. Ou ela
não existe, ou o período do pedido começa antes do período permitido, ou o limite do
pedido passa do limite permitido: em qualquer desses casos a recusa é **\* Permissao
nao cadastrada ou fora do intervalo \***, com o cursor no campo do dia do início, e
nada é gravado. Achada a permissão, o operador dela é o operador do pedido — o que o
servidor tiver digitado no campo do operador é substituído.

[?] O código do operador está entre os campos que a tela confere como numéricos, mas
ela sempre o substitui pelo operador da permissão, ao incluir, e pelo operador do
pedido procurado, ao alterar, excluir ou consultar. Ou o campo é apenas informativo,
ou a conferência dele não serve para nada. Pergunta ao site.

### RN-12 — O saldo da permissão tem de bastar para a quantidade pedida

Achada a permissão, a tela soma os saldos iniciais que ela registra — são **três**
saldos — e soma à quantidade já pedida a nova quantidade. A soma não pode passar do
saldo: passando, a recusa é **\* Quantidade insuficiente na permissao \***, com o
cursor no campo da quantidade, e nada é gravado.

Na alteração, a conferência troca a quantidade antiga pela nova antes de comparar: o
saldo é conferido sobre o que o pedido passa a ser, não sobre o que era.

### RN-13 — O gênero não pode já existir no pedido do período

Na inclusão, a tela percorre os pedidos do **mesmo órgão, mesma coordenadoria, mesmo
fornecedor e mesmo início de período** que já tenham gêneros, e procura neles um
gênero do mesmo tipo de contrato que o informado. Achando, a recusa é **\* <- Genero
ja cadastrado \***, com o cursor no campo da subclasse, e nada é gravado.

### RN-14 — O pedido informado tem de ser um pedido do ano já calculado

Nas operações de alterar, excluir, consultar e na requisição de impressão, o servidor
informa o número do pedido e o ano da entrega — juntos, os dez dígitos que
identificam o pedido. A tela recusa, sem gravar nada:

- **\* Informe o numero do pedido \*** — quando o número não foi informado, com o
  cursor no campo;
- **\* Pedido nao cadastrado \*** — quando o pedido não existe para a coordenadoria
  do órgão, com o cursor no número do pedido;
- **\* Pedido nao cadastrado como acumulado \*** — quando o pedido existe mas não
  está registrado como pedido do ano;
- **\* Pedido acumulado digitado \*** — quando o pedido está registrado como o
  acumulado do ano;
- **\* Pedido auxiliar do acumulado calculado \*** — quando o pedido é o auxiliar
  calculado de outro pedido.

Passando por isso, a tela repõe no cabeçalho o órgão com a descrição, a
coordenadoria, o fornecedor com a razão social, o operador com o nome, o período, a
semana e o tipo de contrato que estão no pedido procurado.

### RN-15 — A inclusão entra no pedido do período; sem ele, abre um pedido novo

Confirmada a inclusão, se já existir no período (mesmo órgão, coordenadoria,
fornecedor e início) um pedido do ano com gêneros, o gênero informado entra nesse
pedido, com um número auxiliar novo.

Se não existir, a tela abre o pedido: o número sai de um contador por secretaria,
coordenadoria e ano, que ela soma em 1 — quando ainda não há pedido no ano, o número
começa em **1** e o contador é criado. O número auxiliar é o seguinte, e o contador
fica gravado com ele. Cada gênero incluído passa a ter, além do pedido do órgão, um
pedido auxiliar que o acompanha.

[?] Os dez dígitos do pedido são montados como número do pedido mais o **ano da
entrega**, e o contador de onde o número sai é procurado pelo **ano do início do
período** — embora o campo dele no acervo se chame ano da entrega. Se os dois anos
divergirem, não se conclui do acervo qual deles identifica o pedido. Pergunta ao
site.

### RN-16 — A consulta exige pedido com gêneros e não grava nada

Na consulta a tela exige que o pedido procurado tenha ao menos um gênero; sem
nenhum, a recusa é **\* Pedido sem generos cadastrados \***, com o cursor no campo da
subclasse. Achado o pedido com gêneros, ela **não pede confirmação** e não cria,
altera nem apaga nada: abre a tela `E231T` em consulta, levando o pedido.

### RN-17 — A alteração exige o gênero no pedido, e o pedido e o gênero não podem estar fechados

Na alteração, o gênero informado é procurado no pedido procurado. Não estando lá, a
recusa é **\* Genero nao cadastrado neste pedido \***, com o cursor no campo da
subclasse, e nada é gravado. Estando o gênero no pedido:

- **\* Pedido fechado \*** — quando o pedido está fechado, com o cursor no número do
  pedido;
- **\* Genero fechado no pedido \*** — quando aquele gênero do pedido está fechado,
  com o cursor no campo do gênero.

### RN-18 — A alteração exige quantidade nova, e ela não pode ser menor que a recebida

Na alteração a quantidade tem de ser **diferente** da que o gênero já tem no pedido;
igual, a recusa é **\* Informe a nova quantidade a ser pedida \***, com o cursor no
campo. A quantidade nova passa pelas mesmas conferências da inclusão — obrigatória
(**\* Informe quantidade a ser pedida \***), menor que 100.000 (**\* Quantidade deve
ser < 100000 \***) e múltipla da fração do gênero (**\* Quant. fracionada invalida
para este genero \***) — e mais uma: ela **não pode ser menor que a quantidade já
recebida**; sendo, a recusa é **\* Quantidade pedida < quantidade recebida \***.
Aumentando a quantidade, o saldo da permissão é conferido como na inclusão (RN-12).

### RN-19 — A exclusão recusa pedido com quantidade recebida e gênero fechado

Na exclusão a tela percorre os gêneros do pedido procurado. Sem nenhum gênero
cadastrado a recusa é **\* Pedido sem generos cadastrados \***, com o cursor no campo
da subclasse. Havendo gênero **fechado**, a recusa é **\* Genero fechado no pedido
\***; havendo gênero com **quantidade recebida**, a recusa é **\* Ja existe
quantidade recebida \***, com o cursor no número do pedido. Em qualquer dessas
recusas nada é apagado.

### RN-20 — A tela pede confirmação antes de gravar

Antes de incluir, alterar ou excluir, a tela reabre a si mesma com a pergunta no
campo de resposta: **\* Confirma inclusao do pedido <S/N> ? \***, **\* Confirma
alteracao do pedido <S/N> ? \*** ou **\* Confirma exclusao do pedido <S/N> ? \***,
conforme a operação, com o cursor no campo da resposta. Só com a resposta afirmativa
a operação segue; entre a pergunta e a resposta a tela confere que nada mudou — a
operação, o órgão, o fornecedor, a semana, as três partes do início, o pedido, a
subclasse, o gênero e a quantidade. Se algum deles mudou, a confirmação é descartada
e a tela volta a conferir tudo antes de perguntar de novo. A consulta **não** pede
confirmação.

[?] Quando a resposta não é afirmativa, a tela descarta a confirmação e volta a
conferir tudo; no caminho da inclusão ela chega outra vez à pergunta, porque a
passagem que pergunta é a mesma que confere os dados. Não se conclui do acervo se o
servidor consegue desistir respondendo "não". Pergunta ao site.

### RN-21 — O que a gravação faz

Confirmada a inclusão, a tela numera o pedido (RN-15) e grava o pedido do ano do
gênero com a quantidade pedida, o pedido auxiliar que o acompanha, o gênero com os
cinco dias de entrega do período e, junto, a baixa do saldo da permissão. Confirmada
a alteração, ela regrava o gênero com a quantidade nova, ajusta o saldo da permissão
— devolvendo a quantidade antiga e baixando a nova — e fecha o gênero quando a
quantidade nova alcança o que já foi recebido; zerado o que resta do pedido do
gênero, o pedido auxiliar é apagado. Confirmada a exclusão, ela apaga os gêneros do
pedido e os pedidos que os acompanham — inclusive o auxiliar — e devolve o saldo das
permissões.

Cada uma dessas gravações deixa um registro de auditoria com a operação, o órgão, a
coordenadoria, o operador, a data e a hora, e o conteúdo anterior e o posterior do
registro. O contador do número do pedido **não** é desfeito em nenhuma delas.

### RN-22 — A requisição de impressão do pedido

Quando o servidor preenche o **código de impressão**, a operação que ele havia
marcado é descartada e a tela passa a procurar o pedido como na consulta (RN-14): o
número do pedido passa a ser obrigatório e as recusas de estado do pedido valem.
Achado, ela monta a requisição de impressão do pedido com o pedido, a secretaria, a
coordenadoria, a matrícula do servidor, a estação, uma cópia e o endereço de correio
eletrônico do cadastro do servidor, e a entrega ao serviço de requisições do sistema.
Nenhum cadastro é gravado e a tela não segue para outra.

### RN-23 — O que a tela entrega à tela seguinte

Terminada a passagem, a tela deixa na área de trabalho da sessão, para a tela
seguinte, o órgão filho, a coordenadoria regional escolar, o pedido, o fornecedor, o
operador, o período, a semana, o tipo de contrato, a subclasse e o gênero, e a
operação — e abre:

- a **`E231T`**, com a operação de **consultar**, quando o servidor consultou;
- a **`E232T`**, com a operação de **consultar**, quando o servidor incluiu ou
  alterou e a gravação terminou.

A exclusão não segue para outra tela: ela termina aqui. Como a operação entregue é a
consulta nas duas saídas, a tela seguinte abre em consulta, sem deixar gravar — é a
tela que a chamou que decide isso, não um campo da tela nova.

[?] O que a tela seguinte recebe, campo a campo, não se conclui desta tela: as telas
`E231T` e `E232T` leem as áreas de trabalho e os registros de passagem delas, e a
partir do vigésimo primeiro campo o conteúdo que esta tela deixa não corresponde ao
que elas declaram esperar. O que se conclui — e está acima — é a operação, o pedido e
o resto do cabeçalho que esta tela compõe. Pergunta ao site.

### RN-24 — Nada é gravado sem a conferência de tela, de acesso e da operação

Na abertura, a tela confere que a estação é a mesma em que a sessão foi aberta — não
sendo, o acesso é encerrado —, que a tela está registrada (senão **\* Tela nao
disponivel \***) e que o código de acesso do servidor alcança a tela (senão **\*
Acesso negado para esta matricula \***). Em toda passagem de mensagem ela repõe, do
vínculo da sessão, a matrícula, o tipo de órgão, a coordenadoria, o órgão filho, o
acesso e o privilégio, e confere a **permissão da operação** que está executando
(senão **\* Acesso negado para esta operacao \***). Nenhuma dessas conferências grava.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedir as quantidades de gênero de um órgão filho no pedido do ano

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E230T

  Cenário: RN-03 — a tela abre em inclusão, com o órgão e a coordenadoria do vínculo
    Dado que o vínculo da minha sessão tem órgão filho e coordenadoria
    Quando abro a tela E230T
    Então a operação já está como incluir
    E o órgão filho e a coordenadoria da minha sessão já estão informados
    E o número do pedido, o ano da entrega e o código de impressão estão vazios

  Cenário: RN-01 — operação não disponível
    Dado que estou na tela E230T
    Quando informo uma operação diferente de incluir, alterar, excluir e consultar
    Então vejo "* Opcao nao disponivel. Use INC, ALT, EXC ou CON *"
    E nada é gravado

  Cenário: RN-04 — órgão filho não informado
    Quando deixo o órgão filho em branco e confirmo
    Então vejo "* Informe o orgao *"
    E nada é gravado

  Cenário: RN-04 — órgão de outro alcance
    Dado que o vínculo da minha sessão tem um órgão filho
    Quando informo outro órgão filho
    Então vejo "* Usuario sem acesso a outro orgao *"
    E nada é gravado

  Cenário: RN-04 — órgão que a tela não atende
    Quando informo um órgão filho que não existe no cadastro
    Então vejo "* Orgao nao cadastrado *"
    E nada é gravado

  Cenário: RN-04 — órgão inativo, incompleto, de outra secretaria ou fora do meu grupo
    Dado que o cadastro do órgão filho está inativo, ou está sem bairro, órgão pai, nome, endereço, matrículas ou pessoas, ou é de outra secretaria, ou é de outra coordenadoria
    Quando informo esse órgão e confirmo
    Então vejo "* Orgao cadastrado como inativo *", ou "* Orgao cadastrado com dados incompletos *", ou "* Orgao nao pertence a esta secretaria *", ou "* Usuario sem acesso ao grupo deste orgao *", conforme o caso
    E nada é gravado

  Cenário: RN-04 — órgão que não é do acumulado
    Dado que o cadastro do órgão filho não está marcado como acumulado
    Quando informo esse órgão e confirmo
    Então vejo "* Orgao nao cadastrado para pedido acumulado *"
    E nada é gravado

  Cenário: RN-05 — fornecedor ou tipo de contrato sem cadastro
    Quando incluo um pedido com um fornecedor que não está cadastrado
    Então vejo "* Fornecedor nao cadastrado *"
    E nada é gravado
    Quando incluo um pedido com fornecedor cadastrado e um tipo de contrato que não está cadastrado para a secretaria
    Então vejo "* Tipo contrato nao cadastrado *"
    E nada é gravado

  Cenário: RN-06 — início da entrega em sábado, domingo ou feriado
    Quando informo um início de período que cai em sábado
    Então vejo "* Inicio da entrega nao deve ser um sabado *"
    E nada é gravado
    Quando informo um início de período que cai em domingo
    Então vejo "* Inicio da entrega nao deve ser um domingo *"
    E nada é gravado
    Quando informo um início de período que está entre os feriados do tipo de órgão
    Então vejo "* Inicio da entrega nao deve ser um feriado *"
    E nada é gravado

  Cenário: RN-07 — o limite do período é o quinto dia útil
    Dado que informei um início de período em dia útil
    Quando confirmo a inclusão
    Então o limite do período mostrado é o quinto dia útil contado do início
    E os dias de sábado, domingo e feriado não entram na contagem

  Cenário: RN-08 — semana da entrega fora de A a E
    Quando informo a semana da entrega com um valor diferente de A, B, C, D e E
    Então vejo "* Informe semana com A / B / C / D / E *"
    E nada é gravado

  Cenário: RN-09 — gênero não cadastrado ou quantidade fora da fração
    Quando informo um par de subclasse e gênero que não está cadastrado
    Então vejo "* Genero nao cadastrado *"
    E nada é gravado
    Quando informo uma quantidade que não é múltipla da fração do gênero
    Então vejo "* Quant. fracionada invalida para este genero *"
    E nada é gravado

  Cenário: RN-10 — quantidade a ser pedida em branco ou acima do teto
    Quando deixo a quantidade a ser pedida em branco e confirmo
    Então vejo "* Informe quantidade a ser pedida *"
    E nada é gravado
    Quando informo uma quantidade igual ou maior que 100.000
    Então vejo "* Quantidade deve ser < 100000 *"
    E nada é gravado

  Cenário: RN-11 — permissão do contrato inexistente ou fora do intervalo
    Dado que não há permissão cadastrada para o conjunto de secretaria, tipo de contrato, fornecedor, coordenadoria, subclasse e gênero cobrindo o período
    Quando confirmo a inclusão
    Então vejo "* Permissao nao cadastrada ou fora do intervalo *"
    E nada é gravado

  Cenário: RN-12 — saldo da permissão insuficiente
    Dado que a permissão existe e cobre o período, mas o saldo dela não cobre a quantidade pedida
    Quando confirmo a inclusão
    Então vejo "* Quantidade insuficiente na permissao *"
    E nada é gravado

  Cenário: RN-13 — gênero já cadastrado no pedido do período
    Dado que já existe no período um pedido do mesmo órgão, coordenadoria e fornecedor com esse gênero do mesmo tipo de contrato
    Quando confirmo a inclusão
    Então vejo "* <- Genero ja cadastrado *"
    E nada é gravado

  Cenário: RN-14 — pedido não informado, não cadastrado ou de espécie errada
    Quando deixo o número do pedido em branco e confirmo uma alteração
    Então vejo "* Informe o numero do pedido *"
    E nada é gravado
    Quando informo um pedido que não existe para a coordenadoria do órgão
    Então vejo "* Pedido nao cadastrado *"
    E nada é gravado
    Quando informo o pedido acumulado do ano
    Então vejo "* Pedido acumulado digitado *"
    E nada é gravado
    Quando informo o pedido auxiliar calculado de outro pedido
    Então vejo "* Pedido auxiliar do acumulado calculado *"
    E nada é gravado

  Cenário: RN-15 — incluir um gênero num pedido novo do período
    Dado que não existe pedido do ano para esse órgão, coordenadoria, fornecedor e período
    E o gênero está cadastrado e a permissão cobre o período com saldo
    Quando incluo a quantidade pedida e confirmo
    Então o pedido do ano recebe o próximo número do contador da secretaria, coordenadoria e ano
    E o gênero é gravado com os cinco dias de entrega do período e a quantidade pedida
    E o pedido auxiliar que o acompanha é gravado
    E o saldo da permissão é baixado
    E a operação fica registrada na auditoria

  Cenário: RN-15 — incluir um gênero num pedido que já existe no período
    Dado que já existe no período um pedido do ano do mesmo órgão, coordenadoria e fornecedor, com gêneros
    Quando incluo outro gênero e confirmo
    Então o gênero entra nesse pedido, com um número auxiliar novo
    E nenhum número de pedido novo é consumido do contador

  Cenário: RN-16 — consultar um pedido com gêneros
    Dado que o pedido procurado tem gêneros cadastrados
    Quando consulto o pedido
    Então a tela não pede confirmação
    E nada é criado, alterado ou apagado
    E abro a tela E231T em consulta com esse pedido

  Cenário: RN-16 — consultar um pedido sem gêneros
    Dado que o pedido procurado não tem nenhum gênero
    Quando consulto o pedido
    Então vejo "* Pedido sem generos cadastrados *"
    E nada é gravado

  Cenário: RN-17 — alterar um gênero que não está no pedido, ou com o pedido ou o gênero fechados
    Dado que o gênero informado não está no pedido procurado
    Quando confirmo a alteração
    Então vejo "* Genero nao cadastrado neste pedido *"
    E nada é gravado
    Dado que o pedido procurado está fechado
    Quando confirmo a alteração
    Então vejo "* Pedido fechado *"
    E nada é gravado
    Dado que aquele gênero do pedido está fechado
    Quando confirmo a alteração
    Então vejo "* Genero fechado no pedido *"
    E nada é gravado

  Cenário: RN-18 — alterar a quantidade
    Dado que o gênero está no pedido com uma quantidade pedida
    Quando informo a mesma quantidade e confirmo
    Então vejo "* Informe a nova quantidade a ser pedida *"
    E nada é gravado
    Quando informo uma quantidade menor que a já recebida
    Então vejo "* Quantidade pedida < quantidade recebida *"
    E nada é gravado
    Quando informo uma quantidade nova válida e confirmo
    Então o gênero fica com a quantidade nova
    E o saldo da permissão é ajustado: a quantidade antiga volta e a nova é baixada
    E a operação fica registrada na auditoria

  Cenário: RN-21 — a alteração fecha o gênero quando a quantidade alcança o recebido
    Dado que a quantidade nova é igual à quantidade já recebida daquele gênero
    Quando confirmo a alteração
    Então o gênero fica fechado no pedido

  Cenário: RN-19 — excluir um pedido com gêneros
    Dado que o pedido procurado tem gêneros, nenhum deles fechado e nenhum com quantidade recebida
    Quando confirmo a exclusão
    Então os gêneros do pedido e os pedidos que os acompanham são apagados
    E o saldo das permissões é devolvido
    E cada apagamento fica registrado na auditoria
    E a tela não segue para outra

  Cenário: RN-19 — excluir um pedido sem gêneros, com gênero fechado ou com quantidade recebida
    Dado que o pedido procurado não tem nenhum gênero
    Quando confirmo a exclusão
    Então vejo "* Pedido sem generos cadastrados *"
    E nada é apagado
    Dado que um gênero do pedido está fechado
    Quando confirmo a exclusão
    Então vejo "* Genero fechado no pedido *"
    E nada é apagado
    Dado que um gênero do pedido já tem quantidade recebida
    Quando confirmo a exclusão
    Então vejo "* Ja existe quantidade recebida *"
    E nada é apagado

  Cenário: RN-20 — a confirmação antes de gravar
    Dado que preenchi tudo para incluir um gênero no pedido
    Quando confirmo
    Então a tela reabre com "* Confirma inclusao do pedido <S/N> ? *"
    E nada foi gravado ainda
    Quando respondo que sim
    Então a inclusão é gravada
    Quando respondo que não
    Então os dados são mantidos e a tela volta a pedir a confirmação

  Cenário: RN-22 — reemitir a impressão do pedido
    Dado que informo o código de impressão junto do número do pedido e do ano da entrega
    Quando confirmo
    Então a requisição de impressão do pedido é montada com o pedido, a secretaria, a coordenadoria, a minha matrícula, a estação, uma cópia e o meu correio eletrônico
    E ela é entregue ao serviço de requisições do sistema
    E nenhum cadastro é gravado
    E a tela não segue para outra

  Cenário: RN-24 — acesso negado para a tela ou para a operação
    Dado que o meu código de acesso não alcança a tela E230T
    Quando abro a tela
    Então vejo "* Acesso negado para esta matricula *"
    E nada é gravado
    Dado que o meu código de acesso não alcança a operação que estou executando
    Quando confirmo
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado
```
