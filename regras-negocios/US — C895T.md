# US — C895T — Reabertura dos cálculos de estimativa por grupo da coordenação regional

## Estória

Como **servidor da CRE**, quero **reabrir os cálculos de estimativa já fechados do meu
grupo, informando até seis datas de fechamento**, para que os períodos encerrados
voltem a ser aceitos pelas telas de manutenção sem depender de abertura feita por fora
do sistema.

A estimativa é apurada período a período, e é a **data de fechamento** que distingue um
período do outro. Fechado o período, o cálculo daquela data deixa de ser tratado pelas
telas que o mantêm; para voltar a mexer nele é preciso reabri-lo. Esta tela recebe o
grupo e até seis datas de fechamento, confere se cada data tem cálculo cadastrado,
mostra a data de início de cada período e, confirmada a operação, registra o pedido e
entrega ao processamento que faz a reabertura. **Quem reabre é esse processamento, não a
tela**: o que a tela deixa é o pedido registrado e a trilha de quem pediu.

## Contexto

Jornada S000M → C000M → C800M → C840M → C895T (5 passos).

Ator: servidor de CRE — informa o grupo e as datas de fechamento dos períodos que quer
ver reabertos.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A tela é alcançada **por dentro da C840M**, pela opção 12, e trabalha sobre a mesma
matéria que a C840M mantém: o cálculo de estimativa do grupo. As telas anteriores da
jornada dão o contexto da sessão — o tipo de órgão, a CRE, a matrícula, o privilégio e a
data do sistema — que a tela usa para procurar o cálculo, conferir o acesso e identificar
quem pede.

A tela **não** encadeia para outra: não passa registro nem operação adiante, e a jornada
termina nela. Ela se reapresenta a si mesma para conduzir a pergunta de confirmação e
recolher a resposta.

As regras abaixo são só as desta jornada.

---

## Regras de negócio

### RN-01 — A tela reabre o cálculo de estimativa fechado de um grupo

O que a tela reabre é o **cálculo de estimativa** de um **grupo** da estrutura da
secretaria, em uma **data de fechamento**. Um cálculo é reconhecido por cinco dados: o
**tipo de órgão**, a **CRE**, a **data de fechamento** (dia, mês e ano) e os códigos de
**subclasse** e de **gênero**. A tela lê esses cálculos; não é ela que os cria.

A tela trabalha com **seis períodos** de uma vez. Cada período é um cálculo e tem duas
datas, em dia, mês e ano: a **data de início** e a **data de fechamento**. A tela mostra
a data de início de cada período e recebe dele a data de fechamento.

### RN-02 — A tela só opera em alteração

A tela só opera quando a operação pedida é **alteração**. Se o pedido chega como
qualquer outra operação — inclusão, exclusão ou consulta —, a tela recusa com
**\* Opcao nao disponivel. Use ALT \***, devolve o cursor ao campo da operação e **nada
é gravado**.

[?] A tela é aberta pela opção 12 da `C840M`, e a `C840M` não deixa operação nenhuma
declarada na passagem: a tela herda o modo de quem a chamou. Se tudo o que chega pela
jornada é alteração, a recusa acima não chegaria a aparecer por esse caminho — e os
fontes desta jornada não mostram outra origem que chame a tela com outra operação.
Pergunta ao site.

### RN-03 — Os campos da tela são numéricos

Antes de consultar os cadastros, o sistema edita o que foi digitado. O **grupo** e as
três partes de cada data — **dia**, **mês** e **ano** — são tratados como número: o que
estiver em branco vira zero, os zeros à esquerda caem, o separador de milhar é
descartado e **o que não for número é recusado**, com o cursor de volta no próprio campo.
A tela não confere calendário: uma data impossível, mas numérica, passa e simplesmente
não encontra cálculo.

### RN-04 — São obrigatórios o grupo e pelo menos uma data de fechamento

Sem o **grupo**, o sistema não segue: mostra **\* Informe o grupo \*** e devolve o
cursor ao campo do grupo. Com o grupo informado, é preciso ao menos **uma data de
fechamento** entre os seis períodos; sem nenhuma, o sistema mostra
**\* Informe data para reabertura do cadastro \*** e devolve o cursor à data do primeiro
período. Nos dois casos nada é gravado, e período deixado em branco é saltado: não é
conferido e não impede a reabertura dos outros.

### RN-05 — Cada data informada tem de ter cálculo cadastrado para o grupo

Para cada período cuja data de fechamento foi informada, o sistema procura o cálculo
daquele **grupo**, daquele **tipo de órgão** e daquela **data**, com a subclasse e o
gênero fixados em zero. Não achando — ou achando registro de outro grupo ou de outra
data —, recusa com **\* Calculo nao cadastrado para esta data \***, devolve o cursor à
data daquele período e nada é gravado.

[?] A procura fixa a subclasse e o gênero em zero, e a conferência do que foi achado não
olha essas duas dimensões: um cálculo cadastrado apenas por subclasse e gênero não é
encontrado, e a tela diz que não há cálculo para a data. Se só o cálculo sem subclasse e
sem gênero deve contar, é pergunta ao site.

### RN-06 — O cálculo cadastrado para a data é recusado, e a recusa diz o contrário do que foi conferido

[?] A guarda que recusa o cálculo já cadastrado exige, para deixar passar, exatamente a
condição com que ela recusa: o cálculo cadastrado para a data é recusado com
**\* Cadastro nao fechado para esta data \*** — e as telas irmãs, que leem o mesmo
indicador de fechamento, usam a condição invertida para dizer **\* Cadastro fechado para
este periodo \***. Ou a condição desta tela está invertida, ou a mensagem está: pelas duas
leituras, a reabertura fica **inalcançável** por este caminho, porque toda data com
cálculo cadastrado cai nesta recusa. Pergunta ao site.

### RN-07 — Pedido do mesmo grupo já na fila bloqueia a reabertura

O sistema procura, na fila de pedidos de relatório, uma requisição do relatório de
reabertura do mesmo grupo ainda pendente. Havendo, ele não aceita o pedido novo: mostra
**\* Atualizacao em processamento. Aguarde. \*** e encerra a operação, sem gravar nada.

### RN-08 — Verificados grupo e datas, o sistema mostra os inícios e pergunta a confirmação

Passadas as conferências, o sistema mostra a **data de início** de cada período — que vem
do cálculo cadastrado, não do que foi digitado — e pergunta
**\* Confirma reabertura dos cadastros <S/N> ? \***, com o cursor no campo de resposta.
Só a resposta afirmativa, digitando **S**, leva ao pedido.

### RN-09 — A resposta negativa não desiste: a tela refaz a conferência e pergunta de novo

Qualquer resposta diferente de **S** não grava nada: a tela limpa a pergunta, limpa a
resposta e **refaz a conferência dos dados digitados**, voltando a perguntar em seguida.
Se o grupo ou alguma data de fechamento tiver mudado depois da pergunta, a resposta é
descartada e a conferência recomeça sobre o dado novo. As datas de início não entram
nessa comparação. Não há caminho de cancelamento nesta tela: para sair sem pedir, o
servidor abandona a tela.

[?] O caminho da resposta negativa devolve a tela ao começo e a primeira passagem termina
repondo a pergunta; os fontes lidos não mostram outra saída. Se a intenção era cancelar,
o comportamento está errado; se era reconferir, está certo. Pergunta ao site.

### RN-10 — Confirmada, a reabertura muda só as datas de fechamento

Confirmada a operação, o que muda no cálculo do grupo são as **datas de fechamento** dos
seis períodos, com os valores informados. A **data de início** de cada período não é
alterada: ela é lida do cálculo e apenas reapresentada.

### RN-11 — A tela não reabre o cálculo: ela registra o pedido e entrega ao processamento

A tela não altera o cálculo de estimativa. Confirmada a operação, ela deixa duas marcas.
Na **trilha de auditoria** grava a ocorrência da reabertura: o grupo, a estação, a data e
a hora da sessão, a matrícula do servidor, a operação de alteração e as **datas de
fechamento anteriores**. Na **fila de pedidos** cria uma **requisição numerada** do
relatório de reabertura — o número seguinte da fila —, guardando o **código do
relatório**, o **grupo** e as **seis datas de fechamento** como parâmetros, mais o ano, o
mês, o dia, a estação e o tipo de órgão da sessão, e entrega essa requisição ao
processamento que roda fora da tela. O servidor vê **\* Cadastros sendo atualizado \***.

O efeito da reabertura, portanto, não se vê nesta tela, e o resultado do processamento
não é mostrado por ela.

### RN-12 — Os dados são autorizados antes de a reabertura ser pedida

A operação de alteração é conferida contra o **cadastro de telas do sistema** — que
guarda, por tela e por operação, se a alteração está liberada — e contra as **telas de
acesso do servidor**. A estação da sessão também é conferida. Sem qualquer uma dessas
marcas, a tela não valida nem registra o pedido, e o servidor vê a recusa de acesso
correspondente.

### RN-13 — O grupo informado não é conferido contra o grupo da sessão

O sistema confere, para cada data, se o cálculo cadastrado é do **grupo informado** — e
não se esse grupo é o da sessão. Nada nesta tela impede informar o grupo de outra
coordenação nem limita a consulta ao grupo da sessão.

---

## Cenários BDD

```gherkin
Funcionalidade: Reabertura dos cálculos de estimativa por grupo da coordenação regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C895T
    E abri a tela pela opção 12 da C840M

  Cenário: A tela abre mostrando os períodos já cadastrados
    Dado que estou na tela C895T
    Quando informo um grupo que tem cálculos cadastrados
    Então vejo a data de início de cada um dos seis períodos
    E posso informar a data de fechamento de cada um deles
    E nada é gravado

  Cenário: A tela só opera em alteração
    Dado que estou na tela C895T
    Quando a operação pedida não é alteração
    Então vejo "* Opcao nao disponivel. Use ALT *", com o cursor no campo da operação
    E nada é gravado

  Cenário: O grupo não foi informado
    Dado que estou na tela C895T
    Quando deixo o grupo em branco e confirmo
    Então vejo "* Informe o grupo *", com o cursor no campo do grupo
    E nada é gravado

  Cenário: Nenhuma data de fechamento foi informada
    Dado que estou na tela C895T com o grupo preenchido
    Quando deixo as seis datas de fechamento em branco e confirmo
    Então vejo "* Informe data para reabertura do cadastro *"
    E o cursor fica na data do primeiro período
    E nada é gravado

  Cenário: Período em branco é saltado
    Dado que estou na tela C895T com o grupo preenchido
    Quando informo a data de fechamento de um único período e deixo os outros em branco
    Então só aquele período é conferido no cadastro dos cálculos
    E os demais não impedem a reabertura

  Cenário: A data informada não tem cálculo cadastrado
    Dado que estou na tela C895T com o grupo preenchido
    Quando informo a data de fechamento de um período que não tem cálculo cadastrado
    Então vejo "* Calculo nao cadastrado para esta data *"
    E o cursor fica na data daquele período
    E nada é gravado

  Cenário: O cálculo cadastrado para a data é recusado
    Dado que estou na tela C895T com o grupo preenchido
    Quando informo a data de fechamento de um período que tem cálculo cadastrado
    Então vejo "* Cadastro nao fechado para esta data *"
    E nada é gravado
    E a reabertura não chega a ser pedida por este caminho

  Cenário: Já existe pedido do mesmo grupo na fila
    Dado que estou na tela C895T com o grupo preenchido
    Quando já existe requisição de reabertura pendente para aquele grupo
    Então vejo "* Atualizacao em processamento. Aguarde. *"
    E o pedido novo não é registrado

  Cenário: A pergunta de confirmação é apresentada
    Dado que estou na tela C895T com o grupo e as datas de fechamento preenchidos
    Quando confirmo os dados
    Então vejo "* Confirma reabertura dos cadastros <S/N> ? *", com o cursor na resposta
    E a data de início de cada período é a do cálculo cadastrado

  Cenário: Confirmo a reabertura
    Dado que estou na tela C895T com a pergunta de confirmação apresentada
    Quando respondo S
    Então a reabertura é solicitada
    E vejo "* Cadastros sendo atualizado *"

  Cenário: A resposta não é afirmativa
    Dado que estou na tela C895T com a pergunta de confirmação apresentada
    Quando respondo algo diferente de S
    Então a pergunta é limpa
    E os dados digitados são conferidos de novo
    E a pergunta volta a ser apresentada
    E nada é gravado

  Cenário: O grupo muda depois da pergunta
    Dado que a tela já me apresentou a pergunta de confirmação
    Quando troco o grupo e respondo S
    Então a resposta é descartada
    E a conferência recomeça

  Cenário: A reabertura muda só a data de fechamento
    Dado que confirmei a reabertura de um grupo
    Quando a reabertura é solicitada
    Então as datas de fechamento dos seis períodos são as que informei
    E as datas de início continuam as do cálculo cadastrado

  Cenário: A tela registra o pedido e não altera o cálculo
    Dado que confirmei a reabertura de um grupo
    Quando a tela conclui a operação
    Então existe um registro de auditoria com a operação, as datas de fechamento
      anteriores, a matrícula, a secretaria, a CRE, a estação, a data e a hora da sessão
    E existe uma requisição numerada do relatório de reabertura, com o grupo e as seis
      datas de fechamento como parâmetros
    E o cálculo do grupo não é alterado pela tela

  Cenário: Sem o acesso à alteração, nada é registrado
    Dado que estou na tela C895T com o grupo e as datas de fechamento preenchidos
    Quando o meu acesso não libera a alteração nesta tela
    Então vejo a recusa de acesso
    E o pedido de reabertura não é registrado

  Cenário: Digitação não numérica é recusada
    Dado que estou na tela C895T
    Quando digito letras em uma data de fechamento
    Então a edição recusa o campo, com o cursor de volta nele
    E nenhuma data é conferida

  Cenário: Data impossível, mas numérica, não é recusada pela edição
    Dado que estou na tela C895T
    Quando informo uma data impossível, mas numérica
    Então a edição aceita a data
    E a conferência procura o cálculo dessa data

  Cenário: A conferência, sozinha, não grava nada
    Dado que estou na tela C895T com o grupo e as datas de fechamento preenchidos
    Quando envio os dados e não respondo à pergunta de confirmação
    Então nenhum pedido é registrado
    E nenhuma trilha de auditoria é gravada
```
