# US — F310T — Manter as permissões de fornecimento por coordenação regional

## Estória

Como **servidor da CRE que responde pelas permissões de fornecimento da sua
coordenação regional**, quero **consultar e alterar as permissões de fornecimento
de cada contrato — o tipo de contrato, o prazo da permissão e os fornecedores
autorizados**, para que **só forneça quem estiver autorizado, dentro do prazo, na
coordenação certa e no contrato certo**.

A permissão de fornecimento é o que autoriza um fornecedor a atender um contrato
de uma coordenação regional, e ela tem prazo: um dia, um mês e um ano limite. É
dessa autorização que saem os números que o resto da cadeia de compras usa — o
processo, o contrato e a NAD de cada fornecedor. Sem ela, o fornecedor não tem
por onde ser aceito; com ela errada, o erro aparece no processo inteiro, e não
nesta tela.

Esta tela **não cria** a permissão. Ela só a consulta e a altera, dentro do que
já foi cadastrado — e o que ela exibe são as cópias por fornecedor dessa
permissão, três por vez na tela.

## Contexto

Jornada S000M → F000M → F300M → F310T.

Ator: servidor de CRE — consulta e altera as permissões de fornecimento da sua
coordenação regional e os fornecedores de cada uma.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — a
opção 3 do `S000M` abre o `F000M`, a opção 11 dele abre o `F300M` e a opção 1
dele abre esta tela — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. Os dois menus do caminho não gravam
nada: só encaminham.

O `F300M` não trata o pedido desta tela: ao receber a opção 1 ele **devolve o
chamado para a tela seguinte**, e é o `F310T` que abre. O que o `F300M` deixa na
sessão — e que esta tela usa — é a **operação** que estava em curso; por isso a
tela chega **em consulta**, e é o servidor que precisa pedir a alteração.

O vínculo da matrícula com a secretaria, que a entrada deixa na sessão, é o que
define a **coordenação regional** e o **tipo de órgão** do servidor; essas são
regras da entrada e estão no anexo de evidências, em **Regras que se revelaram da
entrada**.

## Regras de negócio

### RN-01 — Esta tela só consulta e altera, e abre em consulta

A tela aceita duas operações: **consultar** e **alterar**. Qualquer outra é
recusada com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta
no campo da operação.

O que a tela já encontra preenchido como operação vem do que ficou guardado na
sessão pela tela anterior. Quando o servidor chega pela opção 1 do `F300M` (o
caminho desta jornada), a operação que chega é **consultar** — a tela abre em
consulta. Esta tela **não inclui nem exclui** a permissão: o que ela grava é a
permissão do fornecedor, dentro de uma permissão que já existe.

### RN-02 — A coordenação regional que o servidor pode usar é a dele

O servidor só trabalha com a **coordenação regional do seu próprio vínculo**. A
coordenação é obrigatória: em branco, a recusa é **\* Informe o grupo \***. Se
for informada uma coordenação diferente da do vínculo do servidor, a recusa é
**\* Usuario sem acesso a este grupo \***. Nos dois casos o cursor volta para o
campo da coordenação.

Uma vez aceita a coordenação, ela passa a ser a coordenação de referência da
tela: as consultas seguintes usam a que o servidor informou.

### RN-03 — A coordenação regional tem de estar cadastrada e não pode estar excluída

A coordenação informada é procurada no cadastro das coordenações regionais da
secretaria. Não existindo — ou estando marcada como excluída —, a recusa é
**\* Grupo nao cadastrado \***, com o cursor de volta no campo da coordenação.

### RN-04 — A permissão tem de existir para a coordenação, o contrato e o prazo informados

A permissão é identificada por **quatro dados**: o **tipo de contrato**, o **dia
limite**, o **mês limite** e o **ano limite** do prazo, dentro da **coordenação
regional** e do **tipo de órgão** do servidor. Procurada essa combinação no
cadastro de permissões da secretaria, não existindo — ou estando marcada como
excluída —, a recusa é **\* Permissao nao cadastrada \***, com o cursor de volta
no campo do tipo de contrato.

É a essa permissão que se prendem o processo, o contrato, a NAD e a autuação que
a tela mostra.

### RN-05 — O servidor não muda o que identifica a permissão

Em alteração, os cinco dados que identificam a permissão — a **coordenação**, o
**tipo de contrato** e o **dia, o mês e o ano limite** — têm de ser exatamente os
mesmos que foram informados na consulta que o servidor acabou de fazer. Se
qualquer um deles estiver diferente, a recusa é **\* Consulte antes de atualizar
\***, com o cursor de volta no campo da coordenação. Nos outros modos de operação
a conferência não é feita.

### RN-06 — Só se altera a permissão de um fornecedor que já esteja nela

Informado o **código do fornecedor** (o rótulo da tela é COD.FORNECEDOR), o
sistema procura a permissão do fornecedor para aquela coordenação, tipo de
contrato, prazo, número e ano do contrato. Não existindo, a recusa é
**\* Fornecedor nao cadastrado neste contrato \***, com o cursor de volta no
campo do processo.

[?] Na consulta, o sistema procura a razão social do fornecedor por um cadastro
de fornecedores, usando a coordenação e o prazo informados na tela, e essa
procura é um caminho diferente da procura da permissão do fornecedor. Os dois
caminhos usam a mesma mensagem. Se a mensagem é sobre a permissão do fornecedor
ou sobre o cadastro do fornecedor, o fonte não decide — pergunta ao site.

### RN-07 — Com fornecedor informado, o processo RIO e o processo interno são obrigatórios

Quando o servidor informa um fornecedor, ele tem de informar também o
**processo RIO** e o **processo interno** (o rótulo da tela deste é COD LOTE).
Faltando um dos dois, a recusa é **\* Informe PROCESSO RIO ou processo \***, com o
cursor de volta no campo do processo RIO.

### RN-08 — O processo interno tem de terminar com a coordenação regional

O **processo interno** é conferido contra a coordenação regional que o servidor
informou e que a tela aceitou: se os **dois últimos dígitos** do processo não
forem o código dessa coordenação, a recusa é **\* Numero do processo invalido \***,
com o cursor de volta no campo do processo interno.

Esses dois últimos dígitos são o pedaço da coordenação dentro do processo: o
processo é montado com a secretaria, a coordenação, o lote e o processo RIO, e o
mesmo código de coordenação aparece no fim.

### RN-09 — Com fornecedor informado, a data de autuação tem de ser válida

A **data de autuação** (dia, mês e ano) é conferida como data do sistema, entre
1994 e 2099. Não sendo uma data válida nessa faixa, a recusa é
**\* Data de autuacao invalida \***, com o cursor de volta no campo do dia da
autuação.

### RN-10 — Com fornecedor informado, o contrato e a NAD têm de vir em pares

Informado o **número do contrato**, o **ano do contrato** tem de vir junto; e
informado o **número da NAD**, o **ano da NAD** tem de vir junto. Faltando o par
do contrato, a recusa é **\* Numero do contrato invalido \***; faltando o par da
NAD, a recusa é **\* NAD invalida \***.

As conferências de processo, autuação, contrato e NAD só acontecem **quando há um
fornecedor informado**. Sem fornecedor, a tela não confere esses campos e a
alteração não grava nada.

### RN-11 — A alteração grava a permissão do fornecedor e a autuação que a autorizou

Passando todas as conferências, a alteração grava duas coisas:

- no **cadastro do fornecedor dentro da permissão**, atualiza o **número do
  processo**, o **processo RIO**, o **número do contrato** com o seu ano, o
  **número da NAD** com o seu ano, a **data de autuação** e o indicador de pessoa
  física ou jurídica;
- e, quando há **processo interno** informado, grava também a **trilha de
  auditoria** da sessão: o órgão, a coordenação, a operação praticada, a
  matrícula, a estação, a data e a hora da sessão, e o **registro anterior e o
  registro novo** da permissão, para que a alteração fique rastreável.

Sem processo interno informado, a alteração **não deixa rastro na trilha** — a
auditoria depende de haver processo.

### RN-12 — A alteração apaga a permissão do fornecedor que não é o informado

Quando a permissão do fornecedor é encontrada com um fornecedor **diferente** do
que o servidor informou, o sistema **exclui a permissão do fornecedor antigo** e
continua procurando, num laço, a permissão do fornecedor informado. O laço tem
**50 posições** de fornecedores por permissão.

[?] Nessa exclusão o registro é apagado antes de o laço terminar, e o que sobra
do laço só é desfeito se a gravação seguinte falhar. Se a intenção é substituir o
fornecedor da permissão (apagar o antigo e gravar o novo) ou apenas limpar as
permissões antigas do contrato, o fonte não diz — pergunta ao site.

### RN-13 — A tela não encaminha para outra tela

A última tela da jornada termina em si mesma: ela exibe a permissão consultada
ou alterada e não abre nenhuma outra tela nem passa registro ou operação para
outra tela.

## Cenários BDD

```gherkin
Funcionalidade: Permissões de fornecimento por coordenação regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F310T

  Cenário: A tela abre em consulta e consulta a permissão
    Dado que cheguei pela opção 1 do F300M e a operação que veio é consultar
    Quando informo a minha coordenação regional, o tipo de contrato e o prazo
    Então vejo a permissão com os fornecedores dela
    E nada é gravado

  Cenário: Operação diferente de consultar e alterar
    Quando informo uma operação que não é consultar nem alterar
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo da operação

  Cenário: Coordenação em branco
    Quando deixo a coordenação regional em branco
    Então vejo "* Informe o grupo *"
    E o cursor volta para o campo da coordenação

  Cenário: Coordenação de outra regional
    Quando informo uma coordenação regional diferente da do meu vínculo
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor volta para o campo da coordenação

  Cenário: Coordenação não cadastrada
    Quando informo uma coordenação regional que não existe
    Então vejo "* Grupo nao cadastrado *"
    E o cursor volta para o campo da coordenação

  Cenário: Permissão não cadastrada para a coordenação, o contrato e o prazo
    Quando informo coordenação, tipo de contrato e prazo que não têm permissão
    Então vejo "* Permissao nao cadastrada *"
    E o cursor volta para o campo do tipo de contrato

  Cenário: Alteração sem ter consultado a mesma permissão
    Dado que entrei em alteração
    Quando informo uma coordenação, um tipo de contrato ou um prazo diferente do que consultei
    Então vejo "* Consulte antes de atualizar *"
    E nada é gravado

  Cenário: Fornecedor fora da permissão
    Dado que estou em alteração sobre uma permissão já consultada
    Quando informo um fornecedor que não está nessa permissão
    Então vejo "* Fornecedor nao cadastrado neste contrato *"
    E nada é gravado

  Cenário: Fornecedor informado sem o processo RIO ou sem o processo interno
    Dado que informei o fornecedor
    Quando deixo o processo RIO ou o processo interno em branco
    Então vejo "* Informe PROCESSO RIO ou processo *"
    E o cursor volta para o campo do processo RIO

  Cenário: Processo interno que não termina com a coordenação regional
    Dado que informei o fornecedor e a coordenação regional
    Quando informo um processo interno cujos dois últimos dígitos não são a coordenação
    Então vejo "* Numero do processo invalido *"
    E nada é gravado

  Cenário: Data de autuação inválida
    Dado que informei o fornecedor
    Quando informo uma data de autuação que não é data válida
    Então vejo "* Data de autuacao invalida *"
    E nada é gravado

  Cenário: Contrato sem o ano
    Dado que informei o fornecedor
    Quando informo o número do contrato sem o ano do contrato
    Então vejo "* Numero do contrato invalido *"
    E nada é gravado

  Cenário: NAD sem o ano
    Dado que informei o fornecedor
    Quando informo o número da NAD sem o ano da NAD
    Então vejo "* NAD invalida *"
    E nada é gravado

  Cenário: Alteração gravada com sucesso
    Dado que consultei a permissão e estou em alteração sobre ela
    Quando informo o fornecedor, o processo RIO, o processo interno, o contrato, a NAD e a autuação válidos
    Então a permissão do fornecedor é atualizada
    E a alteração fica registrada na trilha de auditoria, com o registro anterior e o novo

  Cenário: Alteração sem processo interno não deixa rastro na auditoria
    Dado que consultei a permissão e estou em alteração sobre ela
    Quando informo o fornecedor com contrato e NAD, mas sem o processo interno
    Então a permissão do fornecedor é atualizada
    E a trilha de auditoria não recebe registro dessa alteração

  Cenário: Fornecedor diferente na permissão
    Dado que consultei uma permissão cujo fornecedor cadastrado é outro
    Quando informo um fornecedor diferente do cadastrado
    Então a permissão do fornecedor antigo é excluída
    E o sistema segue procurando a permissão do fornecedor que informei

  Cenário: A tela não encaminha para outra tela
    Dado que consultei ou alterei uma permissão
    Quando confirmo a operação
    Então a tela se reexibe com o resultado
    E não abre nenhuma outra tela
```
