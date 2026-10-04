# US — S014T — Manter as descrições de origem dos funcionários

## Estória

Como **servidor de CRE que opera a manutenção das descrições de origem**, quero
**renomear a descrição de origem de um órgão — informando de qual nome ela sai e
para qual nome ela vai — e consultar as descrições já cadastradas**, para que o
catálogo de origens continue batendo com os órgãos do sistema sem que ninguém
perca o vínculo.

O nome da origem é a chave do catálogo e vai gravado em cada funcionário lotado
naquele órgão. Renomear não é um luxo de digitação: é a única forma de corrigir um
nome errado ou desatualizado sem recadastrar os funcionários. Se o catálogo e os
órgãos divergirem, os relatórios por origem deixam de encontrar quem deveriam
encontrar — e a tela deixa de traduzir a origem que o funcionário tem no cadastro.

## Contexto

Jornada S000M → S001M → S004M → S014T.
Ator: servidor de CRE — entra pela Secretaria, abre a tela de manutenção pela
opção de menu e, nela, renomeia ou consulta as descrições de origem.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`, e as regras dela não se
repetem aqui. O caminho até a tela — qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`, e é dado de navegação, não regra de
negócio.

Esta tela é a folha da jornada: não abre outra tela e não devolve registro nem
operação para nenhuma seguinte. Ela recebe, porém, duas entradas diferentes: a
opção de menu, que a abre na **alteração**, e a tela de consulta de órgãos, que a
abre na **consulta** — a única a que ela responde.

## Regras de negócio

### RN-01 — A tela só aceita alteração e consulta

A tela trabalha com uma **opção** que quem opera informa. Só duas opções passam:
a de **consultar** e a de **alterar**. Qualquer outra coisa — inclusive a opção de
incluir e a de excluir — é recusada com **\* Opcao nao disponivel. Use ALT ou
CON \***, e o cursor volta ao campo da opção. A recusa não é só da primeira
linha: toda linha do pedido passa pela mesma conferência.

[?] A mensagem nomeia as opções pelas abreviaturas portuguesas **ALT** e **CON**,
e a conferência compara o que foi digitado com as siglas internas de alteração e
de consulta do sistema, que vêm do catálogo de mensagens do ambiente — cujo texto
não está no lote de fontes disponível. Nenhum fonte desta jornada mostra quem
traduz o que a pessoa digita na sigla conferida. Se não houver tradução, a
conferência recusa toda opção, inclusive as duas que a própria mensagem pede, e
nenhuma alteração é possível. Pergunta ao site.

### RN-02 — A consulta só mostra; não grava nada

Com a opção de consulta, a tela apenas lê o catálogo e o apresenta. Nenhuma
descrição é incluída, alterada ou apagada e nenhum funcionário é reescrito: o
caminho que mexe no catálogo é descartado antes de qualquer gravação. A consulta
confere apenas se a descrição informada existe no catálogo, para recusá-la quando
não existe.

### RN-03 — O catálogo vazio é avisado, não é erro

Quando o catálogo não tem nenhuma descrição de origem, a tela avisa **\* Nao
existem registros cadastrados \*** e o cursor fica no campo da descrição de
origem. O aviso não impede a operação.

### RN-04 — A alteração exige o nome de saída e o nome de destino

Na alteração, os dois campos são obrigatórios e são a mesma coisa em dois estados:
o **de**, que é o nome que a origem tem hoje, e o **para**, que é o nome que ela
passa a ter. Faltando qualquer um dos dois, a alteração é recusada. Se o nome de
saída não estiver no catálogo, a tela avisa **\* Descricao nao cadastrada - de \***
com o cursor nesse campo; se o nome de destino não estiver cadastrado como
descrição de origem, avisa **\* Descricao nao cadastrada - para \*** com o cursor
nesse campo. Nos dois casos nada é gravado.

### RN-05 — O nome de destino não pode ser o nome de um órgão já cadastrado

O catálogo de descrições de origem não pode receber um nome que já seja o nome de
um órgão do cadastro de órgãos. Se o nome de destino for igual ao nome de um
órgão, a alteração é recusada com **<- Orgao cadastrado com este nome \*** e o
cursor volta ao campo do nome de saída.

[?] A recusa da alteração barra o nome que já é de um órgão cadastrado, mas a
inclusão de descrição não faz essa conferência (ver RN-08): um nome de órgão que
ainda não esteja no catálogo poderia entrar por lá e, depois, nunca mais sair por
esta tela — a guarda da exclusão barra exatamente o que a inclusão teria deixado
entrar. Ou a inclusão deveria conferir o cadastro de órgãos, ou a exclusão não
deveria barrar esse caso. Pergunta ao site; não se escolhe um dos dois lados.

### RN-06 — A transferência não pode deixar dois funcionários com a mesma matrícula na mesma origem

Se algum funcionário já tem o nome de destino como sua descrição de origem, a
alteração é recusada com **<- Matricula neste orgao de origem \***, e o cursor
volta ao campo do nome de saída. É essa conferência que impede que a renomeação
junte, debaixo do mesmo nome, um funcionário que já estava lá com outro que está
chegando.

[?] A conferência percorre os funcionários com aquele nome de origem comparando a
matrícula, e o desenho do laço não deixa claro se ele continua para o funcionário
seguinte ou volta ao mesmo registro. Se voltar, a conferência enxerga um
funcionário só: uma matrícula repetida em qualquer outro ponto do conjunto não
seria vista, e a renomeação juntaria os dois assim mesmo. Depende da semântica de
posicionamento do banco, que não está no corpus nem no manual. Pergunta ao site.

### RN-07 — Renomear a origem reescreve os funcionários e troca o nome no catálogo

Passadas as conferências, a alteração faz três coisas na mesma operação: reescreve
**cada funcionário** que estava sob o nome de saída com o nome de destino,
acrescenta o nome de destino ao catálogo de origens e retira do catálogo o nome de
saída. Se a lista de funcionários daquela origem estiver vazia, a alteração ainda
troca o nome no catálogo. Toda alteração também deixa o seu registro na auditoria,
com o que o funcionário tinha antes e o que passou a ter, a data e a hora do
sistema, quem operou e a indicação de que o que mudou foi a descrição de origem.

[?] A tela percorre os funcionários daquela origem e reescreve um a um; se essa
leitura, depois de reescrever o registro — que muda de chave —, continua para os
demais funcionários da origem ou volta ao registro já alterado e encerra o laço,
depende da semântica de posicionamento do banco, que não está no corpus. Se
voltar, a transferência atinge um funcionário só, os outros continuam com o nome
antigo — e a tela apaga esse nome do catálogo logo depois. Pergunta ao site.

[?] O conteúdo anterior e o novo passam por uma área de trabalho de tamanho fixo,
menor que o campo que os recebe na auditoria, e o acervo não diz quanto do
registro essa passagem aproveita. Se ela cortar, a auditoria de uma transferência
pode não guardar tudo o que mudou no funcionário — e quem auditar não terá como
saber o que faltou. Pergunta ao site.

### RN-08 — Nesta jornada a tela não inclui nem exclui descrição; a inclusão e a exclusão ficam inalcançáveis

A tela carrega um campo de estado por linha, que decide entre incluir e excluir a
descrição de origem, com inclusão e exclusão escritas e com as suas mensagens
próprias (**\* Orgao ja cadastrado \***, **\* Informe o orgao de origem \***,
**\* Orgao de origem nao cadastrado \***). Só que os dois estados que acionam
esses caminhos ficam atrás do tratamento de um **registro copiado**, que só exige
a opção de alteração ou de consulta e descarta todo o resto: com a opção de
alteração, a tela segue para o caminho da troca de nome e não chega à inclusão nem
à exclusão; com a de consulta, sai antes. Por esta jornada, portanto, a inclusão e
a exclusão de descrição não acontecem.

[?] O campo de estado que decide entre incluir e excluir a descrição não é
preenchido por nenhum caminho desta jornada: o único ramo que o examina exige que
esteja em curso o tratamento de um registro copiado e que a opção seja a de
alteração — e, nesse caso, o fluxo já seguiu para a troca de nome antes de chegar
lá. Ou esses caminhos vêm de outra origem, que não está nos fontes lidos, ou
ficaram inalcançáveis. O acervo não mostra quem os aciona. Pergunta ao site; não
se escolhe um dos dois lados.

### RN-09 — Quem não tem a alteração liberada no seu código de acesso não altera

Antes de tocar no catálogo, a alteração passa pela conferência de acesso: a tela
leva o código de acesso de quem está operando e a opção pretendida, e o sistema
confere, no cadastro de autorizações, se aquele código tem a alteração liberada
para esta tela. Sem essa liberação, a alteração não segue.

[?] O que quem opera vê quando a conferência de acesso recusa: a rotina que
decide é do ambiente e não está no corpo do programa desta tela; o que se vê no
fonte é que ela avisa por uma rotina de mensagem comum. O texto e a forma do aviso
não estão nos fontes lidos. Pergunta ao site.

### RN-10 — A alteração passa pelo roteamento da tela e a tela é auditada

Além da conferência de acesso, a alteração passa pelo roteamento da tela, que
pode recusá-la; e a própria execução da tela é registrada na auditoria, com quem
operou, a tela, a data e a hora e o tipo de operação.

[?] O que o roteamento recusa e com que aviso: a rotina de roteamento é uma
rotina global, sem corpo nos fontes desta jornada. Pergunta ao site.

### RN-11 — O que a tela mostra além das descrições

O cabeçalho da tela traz a descrição do tipo de órgão da sessão e a data do
sistema; a lista traz, por origem, a descrição de origem e a marca de estado da
linha. A identificação da tela — código e nome — e a data do sistema não são
digitadas: vêm da sessão. A tela não tem página 2: uma requisição marcada como
página 2 recebe **\* Acesso a pagina 2 negado \***.

## Cenários BDD

```gherkin
Funcionalidade: Manter as descrições de origem dos funcionários

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S014T

  Cenário: Consultar as descrições de origem não grava nada
    Dado que a opção informada é a de consulta
    E informo uma descrição de origem que está no catálogo
    Quando confirmo a mensagem
    Então o catálogo é apenas lido
    E nenhuma descrição é incluída, renomeada ou apagada
    E nenhum funcionário é reescrito

  Cenário: Catálogo sem nenhuma descrição
    Dado que a opção informada é a de consulta
    E o catálogo não tem nenhuma descrição de origem
    Quando confirmo a mensagem
    Então vejo a mensagem "* Nao existem registros cadastrados *"
    E o cursor fica no campo da descrição de origem
    E nada é gravado

  Cenário: Consulta de descrição que não está cadastrada
    Dado que a opção informada é a de consulta
    E informo uma descrição de origem que não está no catálogo
    Quando confirmo a mensagem
    Então vejo a mensagem "* Descricao nao cadastrada - de *"
    E o cursor volta ao campo da descrição de origem
    E nada é gravado

  Cenário: Opção diferente de alteração e de consulta
    Dado que a opção informada não é a de alteração nem a de consulta
    Quando confirmo a mensagem
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: Renomear a descrição de origem de um órgão
    Dado que a opção informada é a de alteração
    E informo o nome que a origem tem hoje no catálogo
    E informo o nome novo
    E nenhum funcionário daquele nome novo tem a matrícula dos que estão no nome antigo
    Quando confirmo a mensagem
    Então cada funcionário que estava sob o nome antigo passa a ter o nome novo
    E o nome novo passa a constar do catálogo
    E o nome antigo sai do catálogo
    E a auditoria registra a alteração com o valor anterior e o novo, a data e a hora

  Cenário: Alteração sem o nome de saída ou sem o nome de destino
    Dado que a opção informada é a de alteração
    E deixo em branco o nome que a origem tem hoje ou o nome novo
    Quando confirmo a mensagem
    Então a alteração não é feita
    E nada é gravado

  Cenário: Alteração de nome que não está no catálogo
    Dado que a opção informada é a de alteração
    E informo, como nome de saída, uma descrição que não está no catálogo
    Quando confirmo a mensagem
    Então vejo a mensagem "* Descricao nao cadastrada - de *"
    E o cursor volta ao campo do nome de saída
    E nada é gravado

  Cenário: Alteração para um nome que não está cadastrado como origem
    Dado que a opção informada é a de alteração
    E informo um nome de destino que não está no catálogo
    Quando confirmo a mensagem
    Então vejo a mensagem "* Descricao nao cadastrada - para *"
    E o cursor fica no campo do nome de destino
    E nada é gravado

  Cenário: Nome de destino igual ao nome de um órgão já cadastrado
    Dado que a opção informada é a de alteração
    E informo, como nome de destino, o nome de um órgão que já está no cadastro de órgãos
    Quando confirmo a mensagem
    Então vejo a mensagem "<- Orgao cadastrado com este nome *"
    E o cursor volta ao campo do nome de saída
    E o catálogo não é tocado

  Cenário: Matrícula que já está na origem de destino
    Dado que a opção informada é a de alteração
    E um funcionário que tem a matrícula dos que estão sob o nome antigo já está cadastrado sob o nome novo
    Quando confirmo a mensagem
    Então vejo a mensagem "<- Matricula neste orgao de origem *"
    E o cursor volta ao campo do nome de saída
    E nenhum funcionário é reescrito

  Cenário: Operador sem a alteração liberada
    Dado que a opção informada é a de alteração
    E o meu código de acesso não tem a alteração liberada para esta tela
    Quando confirmo a mensagem
    Então a alteração não segue
    E o catálogo não é tocado
```
