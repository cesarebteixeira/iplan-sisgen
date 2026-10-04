# US — M023T — Pedir a atualização dos matriculados de um período

## Estória

Como **servidor de CRE**, quero **pedir a atualização dos matriculados de um período, informando o mês
e o ano em que ele começa e a impressora em que o resultado sai**, para que **os matriculados daquele
período passem a ser os que o sistema usa, e não os de antes**.

A atualização dos matriculados não acontece sozinha: é um processamento que alguém precisa pedir, e é o
pedido que diz de que período se trata, para onde o resultado vai e quem o pediu. Como o pedido vale
para um período exato, o sistema só o registra depois de mostrar o que entendeu e ouvir a confirmação
de quem pediu. Enquanto houver um pedido do mesmo relatório em processamento, um segundo pedido é
recusado, para o mesmo período não ser processado duas vezes.

## Contexto

Jornada S000M → M000M → M023T.

Ator: servidor de CRE — pede, nesta tela, a atualização dos matriculados de um período, informando o mês
e o ano de início do período e a impressora; confirma o pedido e o vê registrado.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu
a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio.

As regras abaixo são só as da tela desta jornada. As telas anteriores do caminho só encaminham: não
gravam nada e não decidem nada sobre esta. O que a M023T usa — o tipo de órgão, a descrição do órgão, a
matrícula, o privilégio e a CRE da sessão, além da data do sistema — é o que a entrada deixou, e a tela
apenas o repassa às rotinas de rota e de segurança. A tela **não** confere de que tela foi chamada, e
esta jornada não passa por tela encadeada: quem a abre é a opção do menu, e é a própria tela que repõe a
sua operação. A jornada termina aqui: a tela não leva a outra, e o seu único efeito é o pedido.

---

## Regras de negócio

### RN-01 — A tela é o pedido: período, impressora e as informações da sessão

A tela pede uma coisa só: a **atualização dos matriculados de um período**. Para isso, quem usa informa
o **mês** e o **ano em que o período começa** — dois e quatro dígitos — e a **impressora** em que o
resultado sai. A tela mostra ainda, sem que se digite nada, o **tipo de órgão** e a sua **descrição** e
a **data do sistema**, todas vindas da sessão, e a **operação**. A tela não lê nem altera nenhum outro
parâmetro do período: os demais limites que a atualização porventura use não são informados aqui e não
são carregados por ela.

### RN-02 — A operação é a alteração, e vem da própria tela

A operação reposta quando a tela abre é a de **alteração**, e é essa que a tela apresenta e confere; o
que a máscara mostra nesse campo não está no material lido. A recusa por operação não disponível
(**\* Opcao nao disponivel. Use ALT \***) tem o texto escrito no programa, mas **não tem caminho**: a
tela escreve a alteração e, na mesma passagem, confere se o valor é a alteração.

[?] A recusa por operação não disponível é inalcançável por este caminho — o campo é reposto com a
alteração e a guarda seguinte só deixa passar justamente com ela. Ou a guarda vale para uma passagem
que não está no material lido, ou o ramo ficou sem caminho. Pergunta ao site. (As duas linhas estão no
anexo de evidências.)

### RN-03 — O mês de início do período é obrigatório

O **mês** é um código de dois dígitos e passa pela conferência de número; o que chega em branco é
tratado como zero. Mês zerado ou em branco é recusado com **\* Informe mes / ano \***, com o cursor de
volta no mês, e o pedido não é registrado. O **ano** de quatro dígitos passa pela mesma conferência de
número, mas **não** por essa exigência: um ano zerado cai na conferência de validade.

### RN-04 — O período tem de ser uma data válida de um ano entre 1994 e 2099

O mês e o ano informados têm de formar uma data, e o período começa sempre no **dia 1** desse mês. O ano
tem de estar entre **1994** e **2099**; fora disso o pedido não é registrado. Quando o período não
fecha, a recusa é **\* Mes / ano invalido \***, com o cursor de volta no mês.

[?] A validade da data em si depende de uma rotina de conversão que o gerador chama mas não traz: o
corpo dela não está no material lido, e a tela decide entre data boa e data ruim por um valor de retorno
cuja semântica não está nos fontes lidos. O que se afirma acima é o que a tela confere: o ano entre 1994
e 2099, o dia 1 e o mês de dois dígitos. Pergunta ao site.

### RN-05 — A impressora é obrigatória

A impressora não pode ficar em branco: sem ela, a recusa é **\* Informe a impressora \***, com o cursor
de volta no campo, e nada é registrado.

### RN-06 — Um pedido do mesmo relatório em processamento recusa o novo

Antes de registrar, o sistema procura no **cadastro de requisições** um pedido do **mesmo relatório**
que ainda esteja **em processamento**. Achando, recusa com
**\* Relatorio em processamento. Aguarde. \***, com o cursor de volta no campo em que se responde à
confirmação, apaga a resposta e o período guardado, e não registra nada.

[?] A procura leva, além do código do relatório e da marca de "ainda não processado", um **número de
requisição zerado** — e o pedido que a tela registra recebe o número seguinte ao último já registrado,
que é **1** quando não há nenhum. Se a leitura usa o número como parte da chave, a recusa só alcança um
pedido de número zero e nunca aparece; se a leitura posiciona pelo começo da chave, qualquer pedido em
processamento daquele relatório barra o novo. As marcas que dizem como a leitura posiciona são
fornecidas pelo ambiente e não têm valor nos fontes lidos. Disso depende a recusa existir. Pergunta ao
site.

### RN-07 — O pedido é confirmado antes de ser registrado

Conferidos o período e a impressora, o sistema **não** registra: ele guarda o mês e o ano que conferiu,
mostra **\* Confirma atualizacao dos matriculados <S/N> ? \*** e espera a resposta de quem pediu. Sem a
resposta **S**, nada é registrado nessa passagem.

### RN-08 — A resposta vale para o período que foi mostrado

Se, ao responder, o mês ou o ano já não forem os que a tela mostrou quando pediu a confirmação, o
sistema **descarta a resposta**, apaga a mensagem, valida o período de novo e apresenta a mesma pergunta
outra vez. A **impressora não entra** nessa reconferência.

[?] A conferência da impressora vale só para a passagem de validação e não se repete na da resposta: se
a impressora for apagada ou trocada entre a pergunta e a resposta, o pedido é registrado assim mesmo,
com o que estiver no campo na hora do registro, e a recusa da RN-05 não aparece. Se é esse o desenho,
confirma com o site.

### RN-09 — Resposta diferente de S não registra, e a tela volta a perguntar

Qualquer resposta diferente de **S** — inclusive **N** — não registra nada: o sistema limpa a mensagem,
descarta a resposta e apresenta o mesmo pedido de confirmação outra vez. A tela só deixa de perguntar
quando o mês é apagado (e então pede o mês) ou quando o período é trocado (e então valida o novo
período e pergunta de novo).

[?] Responder **N** não cancela o pedido: a tela insiste e repete a pergunta, e não há no fonte nenhum
caminho de cancelamento. Se isso é o desenho, ou se o ramo ficou sem saída, pergunta ao site.

### RN-10 — O pedido confirmado é registrado como uma requisição do relatório

Respondida a confirmação com **S**, o sistema registra o pedido no **cadastro de requisições** como uma
**inclusão**, com o número **seguinte** ao último já registrado. O pedido leva:

- o **relatório** da atualização dos matriculados;
- a **matrícula** de quem pediu, tirada da sessão, e o **e-mail** desse mesmo servidor, tirado do
  cadastro do funcionário;
- o **ano** e o **mês** de início do período;
- o **tipo de órgão** da sessão;
- o **mês** e a **data do sistema**;
- a indicação de que ainda é uma requisição **não processada**.

Os demais dados do pedido — entre eles o campo próprio da impressora e o da CRE — **não** são
preenchidos por esta tela: ficam como o registro é criado. O que a tela informa de impressora, período,
tipo de órgão e CRE de quem pediu viaja reunido num **bloco de parâmetros** que a requisição leva
consigo.

[?] O cadastro marca o campo próprio da impressora como **obrigatório** e a requisição desta tela o
grava **em branco**, com a impressora informada viajando no bloco de parâmetros. Se o obrigatório do
dicionário barra essa gravação, não está no corpus lido — e uma tela da mesma família grava a impressora
nos dois lugares. Pergunta ao site.

[?] A CRE do pedido é a **fixa 1**, e não a CRE da sessão: a tela leva o tipo de órgão da sessão, mas
zera a CRE do pedido. Se a atualização dos matriculados é sempre da CRE 1, pergunta ao site.

### RN-11 — A execução é entregue ao ambiente e a tela avisa

Registrado o pedido, o sistema entrega ao ambiente uma **solicitação de execução** — o relatório da
atualização dos matriculados, com o bloco de parâmetros do pedido e a matrícula de quem o fez — e a tela
avisa **\* Cadastro sendo atualizado \***. O estado de confirmação é descartado: um novo pedido exige
uma nova confirmação.

[?] O retorno da entrega é guardado e não conferido: se a entrega falhar, quem pediu vê a mesma
mensagem de cadastro sendo atualizado. O que aparece nesse caso, e se o pedido fica esperando o
processamento seguinte, pergunta ao site.

### RN-12 — A tela limpa o modo de distribuição automática, e a recusa de destino não aparece

Antes de preparar o registro, a tela limpa o **modo de distribuição automática** da transação. Por isso
a recusa de **destino inválido**, que a ficha da tela lista, não é apresentada por este caminho.

[?] A conferência da distribuição continua no caminho do registro: com o modo automático preenchido por
outra origem, o pedido não é registrado e uma mensagem do catálogo aparece no lugar. O que preenche as
chaves de origem e de destino, e o que o operador vê nesse caso, não está no corpus lido — e disso
depende o pedido ser registrado ou não. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedido da atualização dos matriculados de um período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E a minha sessão carrega o tipo de órgão, a descrição do órgão, a matrícula, o privilégio e a CRE
    E tenho acesso à tela M023T

  Cenário: RN-01 — a tela abre pedindo o período e a impressora
    Quando abro a tela M023T
    Então vejo os campos do mês e do ano de início do período e o campo da impressora
    E vejo o tipo de órgão e a sua descrição e a data do sistema
    E nada foi registrado ainda

  Cenário: RN-02 — a tela repõe a operação de alteração
    Quando abro a tela M023T
    Então a operação da tela é a alteração

  Cenário: RN-03 — sem o mês de início do período nada é registrado
    Dado que estou na tela M023T
    Quando deixo o mês em branco e confirmo
    Então vejo "* Informe mes / ano *"
    E o cursor fica no mês
    E nenhuma requisição é criada

  Cenário: RN-04 — período fora do ano permitido ou mês inexistente
    Dado que estou na tela M023T
    Quando informo um ano fora de 1994 a 2099, ou um mês que não existe
    Então vejo "* Mes / ano invalido *"
    E o cursor fica no mês
    E nenhuma requisição é criada

  Cenário: RN-05 — sem a impressora nada é registrado
    Dado que informei um período válido
    Quando deixo a impressora em branco e confirmo
    Então vejo "* Informe a impressora *"
    E o cursor fica no campo da impressora
    E nenhuma requisição é criada

  Cenário: RN-06 — já existe um pedido do mesmo relatório em processamento
    Dado que já existe um pedido do mesmo relatório em processamento
    Quando confirmo um novo pedido na tela M023T
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor fica no campo em que respondi à confirmação
    E a resposta e o período guardado são apagados
    E nenhuma requisição é criada

  Cenário: RN-07 — a tela pede a confirmação e não registra ainda
    Dado que informei o período e a impressora na tela M023T
    Quando a conferência do período e da impressora termina
    Então vejo "* Confirma atualizacao dos matriculados <S/N> ? *"
    E nenhuma requisição foi criada
    E nenhuma execução foi entregue

  Cenário: RN-08 — a resposta vale para o período mostrado
    Dado que a tela pediu a confirmação de um período
    Quando troco o mês ou o ano e respondo
    Então a minha resposta é descartada
    E o sistema valida o novo período e pede a confirmação outra vez

  Cenário: RN-09 — responder N não registra, e a tela volta a perguntar
    Dado que a tela pediu a confirmação de um período
    Quando respondo N
    Então nenhuma requisição é criada
    E vejo o mesmo pedido de confirmação outra vez

  Cenário: RN-10 — o pedido é registrado como requisição do relatório
    Dado que informei um período válido e a impressora
    Quando respondo S à confirmação
    Então a requisição é registrada como inclusão, com o número seguinte ao último já registrado
    E ela leva a matrícula e o e-mail de quem pediu, o mês e o ano do período, o tipo de órgão e a data do sistema
    E ela fica marcada como ainda não processada

  Cenário: RN-10 — o que a tela deixa em branco no pedido
    Dado que confirmei um pedido na tela M023T
    Quando a requisição é registrada
    Então o campo próprio da impressora e o da CRE do pedido ficam em branco
    E o que informei de impressora, período, tipo de órgão e CRE de quem pediu viaja no bloco de parâmetros da requisição

  Cenário: RN-11 — a execução é entregue e a tela avisa
    Dado que confirmei um pedido na tela M023T
    Quando a requisição é registrada
    Então o ambiente recebe a solicitação de execução do relatório da atualização dos matriculados
    E vejo "* Cadastro sendo atualizado *"
    E um novo pedido exige uma nova confirmação

  Cenário: RN-12 — a recusa de destino inválido não é apresentada
    Dado que confirmei um pedido na tela M023T
    Quando o registro é preparado
    Então a tela limpa o modo de distribuição automática
    E a recusa de destino inválido não aparece por este caminho
```
