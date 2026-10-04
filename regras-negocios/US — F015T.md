# US — F015T — Detalhar as unidades de medida do código de gênero FAE

## Estória

Como **servidor de CRE**, quero **detalhar um código de gênero FAE já cadastrado —
corrigindo o grupo do código e mantendo o vínculo dele com as unidades de medida que
podem ser usadas —**, para que **a classificação do item no FNDE fique completa, sem
que ninguém precise redigitar o código que já existe**.

O código de gênero FAE sozinho não fecha a classificação do item: é o vínculo com a
unidade de medida que diz como o item é medido, e é este detalhamento que o mantém.
Sem ele, o código existe mas não serve para classificar item nenhum, e quem trabalha
com o item não tem por onde saber com que unidade medi-lo. Esta tela só trabalha
sobre código que já foi criado: ela não cria código, e o código que ela não encontrar
é recusado.

## Contexto

Jornada S000M → F000M → F015T.

Ator: servidor de CRE — detalha um código de gênero FAE já cadastrado: corrige o
grupo do código e mantém o vínculo dele com as unidades de medida.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O menu `F000M` não deixa dado de
negócio para esta tela: apenas a escolha da opção que a abre. A outra origem da tela
é a tela dos códigos de gênero FAE (`F010T`), que entrega o código e o modo de
consulta — é dela que vem o comportamento descrito em RN-10. O contexto que a tela
usa — matrícula, código de acesso, privilégio, tipo de órgão e CRE — é o que a
entrada deixou na sessão, e a tela apenas o repassa às rotinas de segurança.

---

## Regras de negócio

### RN-01 — Esta é a tela que detalha as unidades de medida de um código de gênero FAE

Esta tela trabalha sobre um código de gênero FAE **já cadastrado**: mostra o código,
a descrição dele e o grupo, e lista as unidades de medida vinculadas a ele, com a
descrição de cada uma. O código não é criado nem apagado aqui — quem faz isso é a
tela dos códigos, e esta tela recusa o código que não encontrar.

Da lista, cada linha traz a **unidade de medida** e a **situação da linha** — o que
se quer fazer com ela: incluir o vínculo ou apagá-lo. A tela mostra **até onze linhas
por vez**.

Não havendo nenhuma unidade de medida vinculada ao código, a tela avisa
**\* Nao existem unid.medidas cadastradas \*** e deixa a lista vazia.

Os cadastros que a tela consulta — o das telas, o dos códigos de gênero FAE, o do
vínculo com a unidade de medida e o das unidades de medida — são só lidos; o cadastro
das unidades de medida não é mantido aqui.

### RN-02 — A tela abre em consulta, e só alteração e consulta são aceitas

A tela tem um campo de opção. Quando quem a abre não deixa opção nenhuma, ela abre em
**consulta**.

Informada uma opção diferente de alteração e de consulta — ou em branco —, o sistema
recusa com **\* Opcao nao disponivel. Use ALT ou CON \***, devolve o cursor ao campo
da opção e não lê nem grava nada.

Na **consulta**, a tela não grava: ela mostra o código e a lista e sai antes das
operações que gravam. Só a opção de **alteração** chega às operações que gravam.

[?] Depois de uma recusa, o que impede a gravação é o estado que a rotina comum de
mensagem deixa. Essa rotina não faz parte do acervo lido. Se ela não marcar esse
estado, uma operação recusada ainda seria gravada. Pergunta ao site.

### RN-03 — O código tem de estar cadastrado, e a alteração exige que ele tenha sido consultado

O **código do gênero FAE** é obrigatório: em branco, a recusa é
**\* Informe o codigo FNDE \***, com o cursor de volta ao campo do código. Informado,
ele tem de estar **cadastrado**: não estando, a recusa é
**\* Codigo FNDE nao cadastrado \***, também com o cursor no campo do código.

Para **alterar**, o código informado tem de ser o mesmo que foi **consultado** na
sessão: sendo outro, a recusa é **\* Consulte antes de atualizar \***, com o cursor de
volta ao campo do código. É a consulta que carrega a ficha do código; a alteração só
segue sobre a ficha já carregada.

### RN-04 — O grupo do código FNDE é obrigatório na alteração

Para alterar, o **grupo do código FNDE** tem de estar preenchido: em branco, a recusa
é **\* Informe o grupo do codigo FNDE \***, com o cursor de volta ao campo do grupo, e
nada é gravado.

### RN-05 — A lista traz as unidades de medida vinculadas, e cada linha aceita incluir ou excluir

A lista mostra as unidades de medida vinculadas ao código, **até onze linhas por
vez**. Cada linha tem a **unidade de medida** e a **situação**: **incluir**, para
vincular a unidade ao código, ou **excluir**, para desfazer o vínculo.

Linha sem unidade de medida é ignorada. Linha com unidade e situação diferente de
incluir e de excluir também é ignorada, sem recusa nenhuma. As recusas da lista
apontam a linha em que aconteceram.

[?] A passagem que grava só processa a primeira posição da lista. Se o operador marcar
mais de uma linha na mesma mensagem, o acervo lido não permite concluir o que acontece
com as demais — se a mensagem é reapresentada linha a linha, ou se as outras linhas são
descartadas. Pergunta ao site.

### RN-06 — Incluir exige a unidade de medida cadastrada e ainda não vinculada

Para incluir, a unidade de medida informada tem de existir no cadastro das unidades de
medida: não existindo, a recusa é **\* Unidade de medida nao cadastrada \***, com o
cursor de volta ao campo da unidade.

A unidade também **não pode estar vinculada** ao código: estando, a recusa é
**\* Unidade de medida ja cadastrada \***, com o cursor de volta ao campo da situação
da linha. Passando as duas conferências, o vínculo é criado e a inclusão deixa registro
no rastro de auditoria.

### RN-07 — Excluir exige a unidade de medida vinculada ao código

Para excluir, a unidade de medida informada tem de estar vinculada ao código: não
estando, a recusa é **\* Unidade de medida nao cadastrada \***, com o cursor de volta
ao campo da situação da linha. Passando, o vínculo é apagado e a exclusão deixa
registro no rastro de auditoria. A tela **não apaga o cadastro da unidade de medida**
— ela apaga só o vínculo com o código.

### RN-08 — O que a alteração grava

Passando as conferências, a alteração grava no código de gênero FAE o **grupo
informado** e a **matrícula** de quem alterou, e grava a **linha da lista**: na
inclusão, o vínculo novo entre o código e a unidade de medida; na exclusão, o vínculo
é apagado. A descrição do código não é alterada por esta tela.

[?] A alteração troca a matrícula e o grupo do código, mas não repõe a data de
atualização: os campos de ano, mês e dia voltam iguais aos que foram lidos. Se a data
deveria acompanhar a alteração, é pergunta ao site.

### RN-09 — A consulta não grava nada

Na consulta a tela só mostra: nenhum vínculo é criado ou apagado, o código de gênero
FAE não é alterado e nenhum registro de auditoria é gerado.

### RN-10 — A tela abre no modo que a origem deixou, e devolve o controle à tela dos códigos

A tela tem duas origens. Quem a abre pelo **menu** não deixa modo nem código: ela abre
em **consulta**, sem código. Quem a abre pela **tela dos códigos de gênero FAE** deixa
o **modo de consulta** e o **código** já escolhido: a tela abre em consulta,
**posicionada nesse código**, com a descrição e o grupo dele carregados e a lista das
unidades vinculadas. Depois da primeira mensagem, a tela reapresenta o modo e a ficha
que ficaram da passagem anterior.

Preenchida a **marca de consulta**, a tela não altera nada: ela devolve o controle à
**tela dos códigos de gênero FAE**, em modo de consulta e sem código de partida. Para
isso o código informado tem de estar cadastrado.

[?] A entrega é feita por uma área de trabalho comum às duas telas. No fonte, a área de
trabalho das duas tem tamanhos diferentes: esta guarda, antes dela, um bloco de campos
que a outra não tem. O acervo não diz se os valores são encontrados pelo nome dos campos
ou pela posição; se for pela posição, os valores não chegam alinhados e a tela seguinte
abre no código errado. Pergunta ao site.

[?] A marca de consulta é um campo de uma posição que o acervo lido não rotula — a
máscara da tela não está no lote. O que o fonte fixa é o efeito: preenchida, ela devolve
o controle à tela dos códigos. Se o campo deveria ter outro nome ou outra posição na
tela, é pergunta ao site.

### RN-11 — Antes de operar, a tela confere o acesso e a operação autorizada

A abertura da tela confere o acesso no cadastro de telas, com o código de acesso e a
matrícula da sessão: sem o registro da tela, o acesso é recusado com
**\* Tela nao disponivel \***; sem a autorização da matrícula para a tela, a recusa é
**\* Acesso negado para esta matricula \***.

Cada mensagem passa, ainda, por duas conferências com o contexto da sessão — matrícula,
código de acesso, privilégio, tipo de órgão e CRE: a rota da tela e a **operação
autorizada**. A **alteração** exige a autorização de alteração no código de acesso:
sem ela, a recusa é **\* Acesso negado para esta operacao \***. A **exclusão** de uma
linha da lista exige a autorização de exclusão, com a mesma recusa. A consulta, e a
**inclusão** de uma unidade de medida na lista, são conferidas como consulta.

[?] A inclusão de uma unidade de medida não exige a autorização de inclusão: ela é
conferida como consulta, e quem tem a tela autorizada vincula. Se a intenção era exigir
essa autorização, o caminho não a exige. Pergunta ao site.

### RN-12 — Toda gravação deixa rastro de auditoria

Cada alteração do código, inclusão e exclusão de vínculo grava um registro no cadastro
de auditoria com o **conteúdo anterior** e o **conteúdo posterior**, a **matrícula** do
servidor, a **data e a hora** da sessão, a **estação**, o **órgão**, a **CRE** e o
**cadastro de origem** — o do código, quando o que mudou foi o grupo, ou o do vínculo,
quando o que mudou foi a unidade de medida. Na inclusão do vínculo o conteúdo anterior
vai em branco; na exclusão, o conteúdo posterior vai em branco.

[?] A auditoria da inclusão do vínculo só é gravada sob uma condição de estado que o
acervo não explica; se existe um caminho em que a inclusão passa sem deixar rastro, é
pergunta ao site.

### RN-13 — O código passa por edição numérica, e cada mensagem começa com o resultado anterior limpo

O **código do gênero FAE** (sete dígitos) passa por edição numérica antes de qualquer
leitura; em branco, ele vira zero. O que não for número é recusado, o cursor volta ao
campo do código e a operação não é feita.

Antes de conferir qualquer coisa, a tela apaga o órgão, a data do sistema, a descrição
do código e a descrição das unidades de medida que a operação anterior havia mostrado.
Uma operação recusada, portanto, não deixa na tela o resultado anterior.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não
está nos fontes desta jornada: a rotina que faz a edição não faz parte do acervo lido.
Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Detalhar as unidades de medida de um código de gênero FAE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F015T

  Cenário: Consulta de um código cadastrado
    Dado que o código do gênero FAE informado está cadastrado
    E o código tem unidades de medida vinculadas
    Quando informo a opção de consulta
    Então vejo o código, a descrição e o grupo dele
    E vejo as unidades de medida vinculadas, com a descrição de cada uma

  Cenário: A lista não passa de onze linhas por vez
    Dado que o código informado tem mais de onze unidades de medida vinculadas
    Quando peço a consulta
    Então vejo no máximo onze linhas por vez

  Cenário: Código sem unidades de medida vinculadas
    Dado que o código informado está cadastrado
    E não tem nenhuma unidade de medida vinculada
    Quando peço a consulta
    Então vejo a mensagem "* Nao existem unid.medidas cadastradas *"
    E a lista fica vazia

  Cenário: A consulta não grava nada
    Dado que o código informado está cadastrado
    Quando informo a opção de consulta
    Então nenhum vínculo é criado ou apagado
    E o código não é alterado
    E nenhum registro de auditoria é gerado

  Cenário: Alteração do grupo de um código já consultado
    Dado que consultei o código do gênero FAE nesta sessão
    E o código está carregado na tela
    Quando informo a opção de alteração
    E informo o grupo do código FNDE
    Então o grupo informado é gravado no código
    E a ficha do código fica com a minha matrícula
    E a alteração deixa registro no rastro de auditoria

  Cenário: Inclusão de uma unidade de medida na lista
    Dado que consultei o código do gênero FAE nesta sessão
    E a unidade de medida informada está cadastrada
    E a unidade não está vinculada a esse código
    Quando informo a opção de alteração
    E marco a linha com a unidade de medida e a situação de incluir
    Então o vínculo entre o código e a unidade de medida é criado
    E a inclusão deixa registro no rastro de auditoria

  Cenário: Exclusão de uma unidade de medida da lista
    Dado que consultei o código do gênero FAE nesta sessão
    E a unidade de medida informada está vinculada a esse código
    Quando informo a opção de alteração
    E marco a linha com a unidade de medida e a situação de excluir
    Então o vínculo entre o código e a unidade de medida é apagado
    E a exclusão deixa registro no rastro de auditoria
    E o cadastro da unidade de medida continua existindo

  Cenário: Opção diferente de alteração e de consulta
    Dado que estou na tela F015T
    Quando informo uma opção diferente de alteração e de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é lido nem gravado

  Cenário: Código do gênero FAE não informado
    Dado que estou na tela F015T
    Quando deixo o código do gênero FAE em branco
    E peço a operação
    Então vejo a mensagem "* Informe o codigo FNDE *"
    E o cursor volta ao campo do código

  Cenário: Código do gênero FAE não cadastrado
    Dado que o código informado não está cadastrado
    Quando peço a operação
    Então vejo a mensagem "* Codigo FNDE nao cadastrado *"
    E o cursor volta ao campo do código
    E nada é gravado

  Cenário: Alteração de um código que não foi consultado
    Dado que o código informado está cadastrado
    E o código informado não é o que consultei nesta sessão
    Quando informo a opção de alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo do código
    E nada é gravado

  Cenário: Grupo do código FNDE não informado na alteração
    Dado que consultei o código do gênero FAE nesta sessão
    E deixo o grupo do código FNDE em branco
    Quando informo a opção de alteração
    Então vejo a mensagem "* Informe o grupo do codigo FNDE *"
    E o cursor volta ao campo do grupo
    E nada é gravado

  Cenário: Inclusão de uma unidade de medida já vinculada
    Dado que a unidade de medida informada já está vinculada ao código
    Quando marco a linha com a situação de incluir
    Então vejo a mensagem "* Unidade de medida ja cadastrada *"
    E o cursor volta ao campo da situação da linha
    E o vínculo não é criado de novo

  Cenário: Inclusão de uma unidade de medida que não está cadastrada
    Dado que a unidade de medida informada não está no cadastro das unidades de medida
    Quando marco a linha com a situação de incluir
    Então vejo a mensagem "* Unidade de medida nao cadastrada *"
    E o cursor volta ao campo da unidade
    E o vínculo não é criado

  Cenário: Exclusão de uma unidade de medida que não está vinculada
    Dado que a unidade de medida informada não está vinculada ao código
    Quando marco a linha com a situação de excluir
    Então vejo a mensagem "* Unidade de medida nao cadastrada *"
    E o cursor volta ao campo da situação da linha
    E nada é apagado

  Cenário: Linha sem unidade de medida é ignorada
    Dado que consultei o código do gênero FAE nesta sessão
    Quando deixo uma linha sem unidade de medida
    E peço a operação
    Então essa linha não é conferida
    E nenhuma recusa é mostrada por causa dela

  Cenário: A marca de consulta devolve o controle à tela dos códigos
    Dado que o código informado está cadastrado
    Quando preencho a marca de consulta
    Então a tela dos códigos de gênero FAE abre em consulta
    E ela não abre posicionada em nenhum código
    E esta tela não grava nada

  Cenário: Código digitado que não é número
    Dado que digito um código do gênero FAE que não é número
    Quando peço a operação
    Então o cursor volta ao campo do código
    E a operação não é feita

  Cenário: O resultado da operação anterior não fica na tela
    Dado que já mostrei um código e a lista das unidades de medida dele
    Quando peço uma nova operação
    Então o órgão, a data do sistema e as descrições que apareciam não ficam na tela
    E só aparecem os resultados da operação que passou nas conferências

  Cenário: Tela não cadastrada
    Dado que a tela F015T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela F015T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Sem autorização para alterar
    Dado que a minha matrícula tem a tela F015T autorizada, mas não a operação de alteração
    Quando informo a opção de alteração
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Sem autorização para excluir uma unidade de medida
    Dado que a minha matrícula tem a tela F015T autorizada, mas não a operação de exclusão
    Quando marco a linha com a situação de excluir
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E o vínculo não é apagado

  Cenário: Toda gravação deixa rastro de auditoria
    Dado que altero o grupo de um código ou incluo e excluo um vínculo
    Quando a operação é gravada
    Então o rastro guarda o conteúdo anterior e o posterior
    E guarda a minha matrícula, a data e a hora, a estação, o órgão, a CRE e o cadastro de origem
```
