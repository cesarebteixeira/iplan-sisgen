# US — C272C — Consultar órgãos filhos com registro de refeição

## Estória

Como **servidor de CRE**, quero **consultar os órgãos filhos da minha coordenação
regional que têm registro de refeição e escolher um deles**, para que **eu siga
para a manutenção do percentual de atendimento daquele órgão sabendo, antes de
abrir a tela de manutenção, quais órgãos existem e qual é a coordenação regional
escolar e a matrícula funcional ligadas a cada um**.

O registro de refeição do órgão filho é o que liga um órgão da rede a um segmento
de atendimento e a um tipo de refeição; é sobre ele que o percentual de atendimento
do órgão é mantido. Sem esta consulta, quem vai manter o percentual teria de saber
de cor o código do órgão filho — e o código é o que a tela seguinte pede. Esta tela
é só de leitura: ela não inclui, não altera e não exclui registro nenhum.

## Contexto

Jornada S000M → C000M → C028M → C272C.

Ator: servidor de CRE — informa o código de um órgão filho da sua coordenação
regional, confere na lista o que está registrado para aquele órgão e segue para a
tela de manutenção do percentual de atendimento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O C000M e o C028M são menus: eles não
gravam nada e apenas encaminham.

Esta tela **encadeia** com a C272T, a tela de manutenção do percentual de
atendimento por órgão filho, segmento e tipo de refeição. O operador não volta ao
menu para chegar lá: é esta tela que a abre.

O que ela usa da sessão — o tipo de órgão (a secretaria), a matrícula, o código de
acesso, a coordenação regional escolar e o órgão filho do usuário — é o que a
entrada e as telas anteriores deixaram.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela é de consulta: ela não grava nada

A tela abre em modo de consulta e assim permanece em todo caminho de quem a usa,
venha ela do menu ou de outra tela. Nenhuma inclusão, alteração ou exclusão é
executada, e nenhum registro de auditoria é gerado. As operações de gravação, de
exclusão e de travamento existem declaradas para os cadastros que a tela enxerga,
mas **não são executadas em nenhum caminho** — declarar não é executar.

### RN-02 — A lista é das inscrições de órgão filho, segmento e tipo de refeição

O que a tela lista é o registro que liga um **órgão filho**, um **segmento de
atendimento** e um **tipo de refeição**. Como cada combinação é uma inscrição
própria, o mesmo órgão filho pode aparecer em mais de linha, uma por segmento e
refeição. A tela mostra **13 linhas** por página; a inscrição listada é sempre da
secretaria da sessão — a tela não pergunta de qual secretaria se trata.

[?] A inscrição tem uma situação registrada, e a tela parece decidir por ela se o
que foi digitado é uma linha da lista; nenhum caminho que o acervo mostre preenche
essa situação. Ou o formulário a preenche, ou a decisão é sempre a mesma. Pergunta
ao site.

### RN-03 — Cada linha traz o órgão filho, o nome do órgão, a coordenação regional escolar e a situação

Cada uma das 13 linhas traz **quatro informações**: o **código do órgão filho**, o
**nome do órgão**, a **coordenação regional escolar** e a **situação**. Órgão filho
e coordenação vêm do próprio registro de refeição; o nome do órgão vem do cadastro
do órgão, e a tela o mostra **cortado em 13 posições**, embora o cadastro guarde 40.
Não havendo inscrição para mostrar, as linhas restantes ficam em branco.

### RN-04 — O nome do órgão é o do cadastro do órgão filho da sessão

O nome que a linha mostra é o **nome do órgão** registrado no cadastro do órgão
para a secretaria da sessão. A tela não pergunta o nome: ele é lido do cadastro a
partir do órgão filho que está sendo listado.

### RN-05 — A tela não navega sozinha: sem escolha, ela apenas volta a se mostrar

A tela não abre outra tela por conta própria. Se o operador confirmar sem ter
escolhido um órgão — o campo do órgão filho em branco —, a tela volta a se mostrar
em consulta e nada mais acontece: nenhuma tela é aberta e nada é lido além do que a
própria lista já exige.

### RN-06 — Confirmando com um órgão filho, a tela abre a manutenção do percentual em consulta

Confirmando com o **código de um órgão filho** informado, a tela abre a **C272T**,
a manutenção do percentual de atendimento por órgão filho, segmento e tipo de
refeição, **passando o órgão filho escolhido**. A tela seguinte abre em
**consulta**, não em alteração: quem chega por aqui vê o que está registrado, e
alterar depende de outra origem.

[?] O órgão filho informado é aceito sem que a tela confira, no caminho da
confirmação, se ele existe de fato no cadastro: a conferência que existe está no
caminho que monta a lista, e não no que abre a tela seguinte. Se o pretendido era
recusar um código inexistente antes de abrir a manutenção, o caminho não o faz.
Pergunta ao site.

### RN-07 — O teclado dos três campos é editado antes de qualquer leitura

Os três campos informados — o **órgão filho**, a **coordenação regional escolar** e
a **matrícula funcional** — passam por edição numérica antes de qualquer leitura:
campo em branco é tratado como zero, o que não for número é recusado no campo e a
consulta não segue, e o cursor volta ao campo recusado.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não
está nos fontes desta jornada: a rotina que faz a edição numérica não faz parte do
acervo lido, e o nome do campo que ela recebe é só um identificador de trabalho.
Pergunta ao site.

### RN-08 — Sem órgão filho informado, a tela assume que se trata do órgão do próprio usuário

Não havendo órgão filho informado, o campo passa a mostrar o **órgão filho do
usuário** que a sessão já trazia — o código da própria lotação de quem está logado
— e a lista é montada a partir dele. É esse o caminho de quem abre a tela apenas
para se localizar antes de escolher.

### RN-09 — O que a tela apaga antes de mostrar depende do tipo de terminal

Antes de mostrar a lista, a tela apaga a **coordenação regional escolar** e o
**órgão filho** informados para os terminais cujo tipo de estação é o de tela cheia
antiga; no terminal de 3270 os campos **permanecem** como foram digitados. O mesmo
tipo de terminal decide, no outro sentido, o que é apagado na tela seguinte.

### RN-10 — A situação da linha não é preenchida e o aviso de "máximos comensais" é inalcançável

Duas coisas que o fonte promete e não entrega, e que quem for reimplementar precisa
decidir: a **situação** que a linha exibe nunca é preenchida por caminho nenhum, de
modo que a tela mostra a situação em branco; e o aviso
**\* Maximos comensais nao cadastrados \***, que deveria aparecer quando não há
inscrição para o órgão, está guardado por uma condição que o caminho de quem usa a
tela nunca satisfaz — por ele, o aviso não aparece.

[?] A tela seguinte decide por uma situação diferente, com o código "X", e a tela
desta jornada não escreve situação nenhuma: se a intenção era marcar as linhas com
um código de situação, ou o formulário marca, ou a decisão da tela seguinte nunca
distingue. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar os órgãos filhos com registro de refeição da coordenação regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C272C

  Cenário: A lista dos órgãos filhos com registro de refeição
    Dado que a coordenadoria regional tem órgãos filhos com registro de refeição
    Quando abro a tela C272C sem informar órgão filho
    Então vejo a lista dos órgãos filhos da minha secretaria

  Cenário: A lista mostra no máximo 13 linhas
    Dado que existem mais inscrições de órgão filho, segmento e refeição do que cabem na página
    Quando abro a tela C272C
    Então a lista mostra no máximo 13 linhas
    E as linhas restantes ficam em branco

  Cenário: Cada linha traz o órgão filho, o nome do órgão e a coordenação
    Dado que existe inscrição de um órgão filho
    Quando abro a tela C272C
    Então a linha daquele órgão traz o código do órgão filho, o nome do órgão, a coordenação regional escolar e a situação

  Cenário: O mesmo órgão filho em mais de linha
    Dado que o órgão filho tem inscrição em mais de um segmento ou tipo de refeição
    Quando abro a tela C272C
    Então aquele órgão filho aparece em uma linha para cada segmento e tipo de refeição

  Cenário: O nome do órgão vem do cadastro do órgão
    Dado que o órgão filho listado está cadastrado com um nome
    Quando abro a tela C272C
    Então a linha mostra o nome registrado no cadastro daquele órgão

  Cenário: Sem escolher órgão filho, a tela só volta a se mostrar
    Dado que estou na tela C272C
    Quando confirmo sem informar órgão filho
    Então a tela continua em consulta
    E nenhuma outra tela é aberta

  Cenário: Escolher um órgão filho abre a manutenção do percentual
    Dado que o órgão filho informado tem registro de refeição
    Quando confirmo com o código daquele órgão filho
    Então a tela C272T abre em consulta, com aquele órgão filho escolhido

  Cenário: Sem informar órgão filho, vale o órgão do próprio usuário
    Dado que a minha sessão tem um órgão filho
    Quando abro a tela C272C e deixo o órgão filho em branco
    Então o órgão filho do meu usuário passa a ser o que a tela mostra

  Cenário: Digitação não numérica no órgão filho, na coordenação ou na matrícula
    Dado que digito no órgão filho, na coordenação regional escolar ou na matrícula funcional algo que não é número
    Quando confirmo
    Então o sistema recusa a digitação antes de listar qualquer registro
    E o cursor volta ao campo recusado

  Cenário: Os campos informados são apagados no terminal de tela cheia antiga
    Dado que estou em um terminal de tela cheia antiga
    Quando abro a tela C272C
    Então a coordenação regional escolar e o órgão filho informados aparecem em branco

  Cenário: No terminal de 3270 os campos permanecem
    Dado que estou em um terminal de 3270
    Quando abro a tela C272C
    Então a coordenação regional escolar e o órgão filho permanecem como foram digitados

  Cenário: A situação da linha aparece em branco
    Dado que existe inscrição de um órgão filho
    Quando abro a tela C272C
    Então a situação da linha aparece em branco

  Cenário: Sem inscrição para o órgão, nenhum aviso é mostrado
    Dado que o órgão filho não tem registro de refeição
    Quando confirmo com o código daquele órgão
    Então a lista não é preenchida para ele
    E o aviso "* Maximos comensais nao cadastrados *" não é mostrado por esse caminho

  Cenário: A consulta não grava nada
    Dado que abro a tela C272C
    Quando a lista é mostrada e escolho um órgão filho
    Então nenhum registro é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado
```
