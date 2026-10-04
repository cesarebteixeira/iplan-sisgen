# US — C023T — Manter bairros

## Estória

Como **servidor da CRE**, quero **manter o cadastro de bairros**, para que os órgãos da
Secretaria possam ser classificados pelo bairro onde ficam.

O bairro é cadastro de apoio: quem o usa é o cadastro de órgãos. Por isso a exclusão de
um bairro é recusada enquanto houver órgão cadastrado nele, e o código do bairro é
atribuído pelo sistema, não escolhido por quem opera — o que se informa é a descrição.
Se o cadastro de bairros não estiver em ordem, o órgão fica sem classificação de bairro,
e é essa classificação que organiza o atendimento por região.

## Contexto

Jornada S000M → C000M → C015M → C023T.

Ator: servidor de CRE — mantém o cadastro de bairros que o cadastro de órgãos usa.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A tela é aberta por um menu, e não encadeada por outra tela que lhe passe o registro e a
operação: quem chega escolhe na própria `C023T` o que fazer e sobre qual bairro. Da tela
anterior a `C023T` guarda apenas a identificação de origem — ela é enviada à conferência
de perfil e de rota e vai registrada na auditoria. As regras abaixo são só as desta tela;
o que a tela anterior faz com o próprio menu não é regra desta estória.

## Regras de negócio

### RN-01 — A tela mantém o cadastro de bairros

A tela se identifica como CODIGO DO BAIRRO e é a manutenção do cadastro de bairros. Cada
linha visível traz **três dados**: o código do bairro (3 dígitos), a descrição (25
caracteres) e a situação (1 caractere). A tela mostra **15 linhas** por vez, e é esse
cadastro — e só ele — que ela lê e grava. O cadastro de bairros tem **2 campos**, a
descrição, de preenchimento obrigatório, e o código; a descrição e o código formam a
segunda chave de acesso.

### RN-02 — A tela só executa com a opção de alteração ou de consulta

A tela só grava quando a opção de manutenção informada é a de **alteração (ALT)** ou a de
**consulta (CON)**. Qualquer outra opção é recusada com * Opcao nao disponivel. Use ALT ou
CON * — a mensagem não lista as opções: ela descreve a opção recusada —, e o cursor volta
para o campo da opção.

[?] O acervo não permite concluir com que valor a tela abre quando o operador não informa
opção de manutenção: nesta tela não encontrei o trecho que assume a consulta por omissão,
como existe em telas irmãs. Se ela abre em branco ou assume CON, o site confirma.

[?] A correspondência entre o texto que a tela exibe (ALT, CON) e as operações internas de
alteração e de consulta vem da própria mensagem e não é confirmada em nenhum ponto do
fonte desta jornada. É pergunta ao site.

### RN-03 — A situação de cada linha diz o que fazer com ela

Em cada linha, a **situação** decide a operação: **I** inclui o bairro, **A** altera e
**E** exclui. Linha sem descrição, ou com situação diferente de I, A e E, é ignorada: não
gera operação nenhuma.

[?] A situação **A** só produz efeito no modo de alteração; no modo de consulta o fluxo
termina antes de qualquer gravação. Se a tela permite digitar A em consulta, o que o
operador espera ver é pergunta ao site.

### RN-04 — A consulta por descrição busca o bairro e devolve o seu código

Digitada uma descrição como consulta, o sistema procura o bairro por essa descrição e
preenche a linha com o código e a descrição encontrados; não achando, deixa o código em
branco. Depois de uma consulta por descrição, a linha não é gravada nem excluída: a
consulta serve para identificar o bairro, não para operá-lo.

### RN-05 — O código do bairro é atribuído pelo sistema

Ao registrar um bairro novo, o sistema busca o código mais alto já cadastrado e grava o
**código seguinte**; se não houver nenhum bairro, começa em **1**. O código que aparece na
linha não é escolhido por quem opera.

[?] Nenhum ponto desta jornada define o que o sistema usa como referência de "último
código": o valor que posiciona essa busca é uma constante de outro módulo do acervo. Se a
busca é mesmo pelo código mais alto já gravado, o site confirma.

### RN-06 — Inclusão de bairro que já existe é recusada

Para incluir, o sistema procura o bairro pela descrição informada e também pelo código. Se
já existir bairro com aquela descrição, ou se o código da linha já estiver cadastrado, a
inclusão é recusada com * Bairro ja cadastrado *, e nada é gravado.

### RN-07 — Alteração é recusada nos dois desfechos possíveis

Para alterar, o bairro precisa existir: não encontrando o bairro, o sistema recusa com
* Bairro nao cadastrado *. Encontrando, o caminho de gravação recusa com
* <- bairro ja cadastrado *, que é a recusa de descrição já usada. Lendo o código do
bairro, a alteração não encontra o bairro e é recusada; lendo a descrição, ela encontra e
também é recusada — os dois desfechos levam à recusa, e a alteração fica **inalcançável
por este caminho**.

[?] A alteração é inalcançável: quando o bairro existe, a conferência da descrição recusa
com * <- bairro ja cadastrado *; quando não existe, a conferência de existência recusa com
* Bairro nao cadastrado *. As duas conferências leem a mesma referência do bairro na
memória, que a tela nunca sincroniza com o registro encontrado. Ou o caminho de gravação
usa outra referência, ou a alteração não funciona. Pergunta ao site.

### RN-08 — A exclusão é recusada quando há órgão cadastrado no bairro

O sistema varre o cadastro de órgãos procurando algum cujo bairro seja o bairro excluído.
Achando, recusa a exclusão com * Nao exclua. Orgaos cad. neste bairro * e o bairro
continua cadastrado.

[?] A conferência varre o cadastro de órgãos inteiro, comparando bairro a bairro, porque o
bairro não faz parte da chave desse cadastro — o cadastro de órgãos declara **27 campos**,
e o bairro é um deles, sem compor chave. Se essa varredura completa é aceitável, ou se
existe outro caminho, é pergunta ao site.

### RN-09 — A exclusão exige bairro existente e nenhum órgão no bairro

Para excluir, o bairro precisa existir: não encontrando, o sistema recusa com * Bairro
nao cadastrado *. E não pode haver órgão cadastrado no bairro. Passando nas duas
conferências, o registro é travado e excluído.

### RN-10 — A consulta não grava nada

Na consulta, a tela lista e procura por descrição e para: nenhuma linha é incluída,
alterada ou excluída, e nenhum rastro de operação é gerado.

### RN-11 — Quando não há bairro cadastrado, a tela avisa

Abrindo sobre um cadastro de bairros vazio, a tela avisa
* Nao existem bairros cadastrados * e posiciona o cursor na primeira linha.

### RN-12 — O código do bairro é tratado como número

O código do bairro é editado como número: o campo em branco vale zero, os zeros à esquerda
são descartados e a formatação com sinal é removida. O que não for número é recusado, sem
chegar ao cadastro.

[?] A tela converte o campo do código em branco para zero e, no mesmo movimento, recusa o
que não for numérico — o efeito prático do zero e o texto da recusa não se concluem do
fonte desta jornada. Confirmação no site.

### RN-13 — A operação depende do perfil, e a rota é conferida contra a tela de origem

Cada linha, antes de gravar, passa pela conferência de acesso: o sistema procura a
autorização do usuário para a tela e para a operação pretendida (inclusão, alteração ou
exclusão). Não estando liberada, a operação é recusada e a tela é abandonada sem gravar. A
conferência recebe o contexto da sessão — a tela de origem, a matrícula, o código de
acesso, o privilégio, o tipo de órgão e a CRE. A tela de origem chega à `C023T` pela tela
anterior (`C015M`), e a rota é conferida contra ela: não sendo a rota esperada, a operação
é abandonada.

### RN-14 — Toda gravação fica registrada na auditoria

Inclusão, alteração e exclusão gravam, além do bairro, um registro de auditoria com a tela
de origem (`C021T` — a tela dona do cadastro de bairros), a operação, o conteúdo anterior
e o posterior, a matrícula do servidor, a estação, o número do processo, o dia, a hora e o
minuto da sessão e o tipo de órgão. O cadastro de auditoria tem **15 campos** e admite
60 milhões de registros, que é **capacidade** declarada — quanto existe de fato, o acervo
não informa.

### RN-15 — Falha de banco interrompe a operação

Erro de banco durante a leitura ou a gravação interrompe a operação: a tela avisa e não
completa a gravação.

## Cenários BDD

```gherkin
Funcionalidade: Manter bairros

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C023T

  Cenário: Consulta lista os bairros em 15 linhas
    Dado que estou na C023T em modo de consulta
    Quando a tela abre
    Então vejo os bairros cadastrados, até 15 por vez, com código, descrição e situação

  Cenário: A consulta não grava nada
    Dado que estou na C023T em modo de consulta
    Quando a tela percorre o cadastro de bairros
    Então nenhuma linha é incluída, alterada ou excluída
    E nenhum rastro de operação é gerado

  Cenário: Não há bairros cadastrados
    Dado que o cadastro de bairros está vazio
    Quando abro a C023T
    Então vejo a mensagem "* Nao existem bairros cadastrados *"
    E o cursor fica na primeira linha

  Cenário: Consulta por descrição mostra o código do bairro
    Dado que existe um bairro com a descrição que vou informar
    Quando faço a consulta por essa descrição
    Então a linha mostra o código do bairro encontrado
    E nada é gravado

  Cenário: Consulta por descrição de bairro inexistente
    Dado que não existe bairro com a descrição informada
    Quando faço a consulta por essa descrição
    Então o código do bairro fica em branco
    E nada é gravado

  Cenário: Opção de manutenção indisponível
    Dado que informei uma opção de manutenção diferente de ALT e de CON
    Quando a tela confere a opção
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo da opção

  Cenário: Inclusão de um bairro novo
    Dado que estou na C023T em modo de alteração
    Quando informo a situação I em uma linha com a descrição de um bairro que não existe
    Então o sistema atribui o código seguinte ao último cadastrado
    E grava o bairro
    E registra a operação na auditoria

  Cenário: Primeiro bairro do cadastro
    Dado que o cadastro de bairros está vazio
    Quando incluo o primeiro bairro
    Então o sistema atribui a ele o código 1

  Cenário: Inclusão de bairro com descrição já cadastrada é recusada
    Dado que já existe um bairro com a descrição informada
    Quando tento incluir o bairro
    Então vejo a mensagem "* Bairro ja cadastrado *"
    E nada é gravado

  Cenário: Inclusão com código já cadastrado é recusada
    Dado que o código informado na linha pertence a um bairro já cadastrado
    Quando tento incluir o bairro
    Então vejo a mensagem "* Bairro ja cadastrado *"
    E nada é gravado

  Cenário: Operação sobre bairro não cadastrado é recusada
    Dado que o bairro informado não existe no cadastro
    Quando tento alterar ou excluir
    Então vejo a mensagem "* Bairro nao cadastrado *"
    E nada é gravado

  Cenário: A alteração é recusada nos dois desfechos
    Dado que o bairro existe ou não existe no cadastro
    Quando tento alterar
    Então vejo a mensagem "* <- bairro ja cadastrado *" quando o bairro é encontrado
    E vejo a mensagem "* Bairro nao cadastrado *" quando o bairro não é encontrado
    E nada é gravado

  Cenário: Exclusão de bairro sem órgão cadastrado
    Dado que nenhum órgão usa o bairro
    Quando informo a situação E
    Então o sistema trava o registro e exclui o bairro
    E registra a operação na auditoria

  Cenário: Exclusão recusada porque há órgão no bairro
    Dado que existe pelo menos um órgão cadastrado naquele bairro
    Quando tento excluir o bairro
    Então vejo a mensagem "* Nao exclua. Orgaos cad. neste bairro *"
    E o bairro continua cadastrado

  Cenário: Linha sem descrição ou com situação desconhecida é ignorada
    Dado que preenchi uma linha sem descrição ou com situação diferente de I, A e E
    Quando a tela processa as linhas
    Então aquela linha não gera operação nenhuma

  Cenário: Código do bairro em branco ou não numérico
    Dado que o campo do código está em branco ou contém algo que não é número
    Quando a tela edita o código
    Então o campo em branco é tratado como zero
    E o que não for número é recusado, sem chegar ao cadastro

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não tem a operação pretendida liberada para a tela
    Quando tento incluir, alterar ou excluir
    Então a operação é recusada
    E a tela é abandonada sem gravar

  Cenário: Rota não esperada para a tela de origem
    Dado que cheguei à C023T por uma tela de origem diferente da esperada
    Quando tento gravar
    Então a operação é abandonada
    E nada é gravado

  Cenário: Falha de banco interrompe a operação
    Dado que o banco falha durante a leitura ou a gravação
    Quando tento operar a linha
    Então a tela avisa da falha
    E a gravação não é completada
```
