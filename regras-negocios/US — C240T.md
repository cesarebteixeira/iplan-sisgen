# US — C240T — Manter os grupamentos de classificação de licitação e suas vigências

## Estória

Como **servidor de CRE**, quero **manter os grupamentos de classificação de licitação,
com a descrição e a data a partir da qual cada versão passa a valer**, para que **quem
classifica um item encontre sempre o grupamento descrito e saiba desde quando aquela
descrição vale**.

O grupamento é a classificação de licitação que agrupa os itens, e o mesmo grupamento
tem mais de uma versão ao longo do tempo: cada versão é uma descrição que passa a valer
numa data. Sem poder incluir a versão nova, a classificação fica congelada na descrição
antiga; e uma versão que comece a valer antes da última já cadastrada voltaria atrás no
tempo e mudaria uma descrição que já estava em vigor — por isso a data nova tem de ser
posterior. A descrição também não pode ficar em branco, porque é por ela que quem
classifica reconhece o grupamento.

## Contexto

Jornada S000M → C000M → C055M → C240T.

Ator: servidor de CRE — cadastra e mantém os grupamentos de classificação de licitação e a
data de vigência de cada versão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O C000M e o C055M são menus: encaminham
por opção e não gravam nada, e a C240T não recebe deles registro nem operação — ela abre
por menu, já em inclusão. O contexto que a C240T usa — matrícula, código de acesso,
privilégio, tipo de órgão e CRE — é o que a entrada deixou na sessão. A tela também não
entrega nada à seguinte: a única saída que ela escreve é ela mesma, para se reapresentar.

---

## Regras de negócio

### RN-01 — O que a tela mantém: o grupamento e a vigência de cada versão

A tela é a manutenção do cadastro dos grupamentos de classificação de licitação. Cada
vigência é um registro com o **código do grupamento** (4 dígitos), a **data a partir da
qual ela vale** — dia (2 dígitos), mês (2 dígitos) e ano (4 dígitos) — e a **descrição**
(30 caracteres). A descrição é de preenchimento obrigatório no dicionário de dados. O
cadastro tem capacidade declarada para **500** registros de vigência; capacidade é o
máximo esperado, um parâmetro de dimensionamento, não o que está cadastrado.

Fora do cadastro, a tela mostra a **data do sistema**, a **descrição do tipo de órgão** da
sessão, a linha de mensagem e até **12 datas de vigência** do grupamento consultado.

[?] O cadastro do grupamento não tem campo de secretaria, de CRE nem de órgão: se a base é
compartilhada entre as secretarias, o mesmo grupamento e a mesma descrição valem para
todas, e o único recorte é a autorização da tela. Se deveria haver recorte por secretaria,
é pergunta ao site.

### RN-02 — A tela abre na inclusão; as demais operações dependem da operação informada

Ao abrir, a tela já vem com a **operação de inclusão** preenchida e os campos de dados em
branco. Além da inclusão, a tela trata a **alteração**, a **exclusão** e a **consulta** —
é o campo da operação que decide o que a tela faz. Os pedidos de primeiro registro, último
registro, próximo, anterior e recuperação não são operações de manutenção: eles só
reapresentam o que já está cadastrado, sem processar nem gravar.

[?] Se a máscara deixa o operador trocar a operação. A abertura repõe a inclusão, o cursor
das recusas aponta para o campo da operação e a conferência de navegação supõe que ele
possa ser digitado; mas o texto da máscara não está no acervo lido e a ficha do programa
só registra os três rótulos dos campos de dados. Se o campo vier protegido, a inclusão é a
única operação alcançável por esta tela. Pergunta ao site.

### RN-03 — Na inclusão, grupamento, data e descrição são obrigatórios, e a data tem de ser válida

Na inclusão, o sistema exige, nesta ordem, o **código do grupamento**, a **data de
vigência** e a **descrição**. Sem o código, recusa com **\* Informe o Grupamento \*** e
devolve o cursor ao campo. A data passa por conversão de calendário: se o dia não existir
no mês, ou se o ano estiver fora da faixa de **1994 a 2099**, a recusa é **\* Data de
inicio invalida \***, com o cursor de volta ao campo do dia. Sem a descrição, a recusa é
**\* Informe descricao do grupamento \***, com o cursor no campo da descrição. O código,
o dia, o mês e o ano passam antes por edição numérica: campo em branco vira zero.

[?] Os avisos desta regra saem como mensagem de tela, e não pela marcação de erro que
interrompe a transação, usada nas demais recusas. Se a mensagem de tela, sozinha, não
interromper, uma inclusão com o código do grupamento em branco e o ano preenchido pode
seguir até a gravação; se interromper, esse caminho não existe. Pergunta ao site.

### RN-04 — A vigência nova não pode repetir a data já cadastrada nem ser igual ou anterior à última vigência

Ainda na inclusão, o sistema procura o par **código do grupamento e data**: se já existir,
recusa com **\* Grupamento ja cadastrado \***. Não existindo, procura a **última vigência
já cadastrada daquele grupamento** e compara as duas datas: se a data informada não for
**posterior** à última, recusa com **\* <- Grupamento ja ativo nesta data \***, mostrando a
data da vigência que já está valendo. Só passando pelas duas conferências a inclusão
segue — e a conferência da descrição vem depois destas.

[?] A leitura que busca a última vigência se posiciona pela maior data possível, mas o
efeito desse posicionamento não está no acervo nem no manual. Se ele devolve a vigência
mais recente do grupamento, vale o que está escrito acima; se devolve a primeira, a
comparação é com a mais antiga e a regra é outra. Pergunta ao site.

### RN-05 — O cadastro guarda uma vigência por grupamento e por ano

A chave do cadastro é o **ano da vigência junto com o código do grupamento**, sem
repetição: não cabe mais de uma vigência do mesmo grupamento no mesmo ano, mesmo em datas
diferentes. Ao incluir, o sistema consulta essa chave antes de gravar e, achando registro,
recusa a inclusão — com uma mensagem do ambiente de execução, e **não** com as mensagens da
tela: nem **\* Grupamento ja cadastrado \*** nem **\* <- Grupamento ja ativo nesta data \***
mencionam o ano.

[?] O texto da mensagem de registro repetido vem do ambiente de execução e não está no
lote. Se a intenção era permitir mais de uma vigência do mesmo grupamento no mesmo ano, a
chave do cadastro não permite; se a intenção é mesmo essa, as mensagens da tela deveriam
dizer o ano. Pergunta ao site.

### RN-06 — A alteração troca a descrição de uma vigência existente

Para alterar, o sistema exige que exista vigência daquele grupamento **naquela data**: não
existindo, recusa com **\* Grupamento nao cadastrado nesta data \***. Exige também a
**descrição**: em branco, recusa com **\* Informe descricao do grupamento \***, com o
cursor no campo. Passando pelas duas, a vigência é regravada com a descrição nova e a
operação fica registrada na auditoria, com o conteúdo anterior e o novo.

[?] A conferência de existência procura o par grupamento e data, mas o ramo que grava
procura o registro pelo **grupamento e ano**. Quando o grupamento tem uma vigência naquele
ano em outra data, a recusa e a gravação não falam do mesmo registro: ou o aviso
interrompe a transação e a alteração nunca chega a gravar nesse caso, ou não interrompe e a
vigência do ano é a atingida. As duas linhas estão no fonte; não foi possível decidir.
Pergunta ao site.

### RN-07 — A exclusão marca a vigência como excluída, sem apagá-la

Para excluir, o sistema exige que exista vigência daquele grupamento **naquela data** —
não existindo, recusa com **\* Grupamento nao cadastrado nesta data \***. A exclusão não
apaga o registro: ela o **marca como excluído**, de modo que a vigência deixa de valer mas
continua no cadastro, com o conteúdo anterior guardado na auditoria.

[?] O mesmo programa tem um caminho que apaga o registro de vez: ele recusa essa operação
com o aviso de que a exclusão definitiva não é permitida e, no entanto, o ramo que grava
chama a exclusão definitiva — que **não** gera registro de auditoria. Se o aviso interrompe
a transação, o caminho é inalcançável; se não interrompe, a vigência é apagada sem rastro.
Pergunta ao site.

### RN-08 — A vigência excluída continua ocupando a chave do ano

Uma vigência marcada como excluída continua no cadastro e continua ocupando a **chave do
ano** do grupamento. Por isso, sobre uma vigência excluída o sistema recusa a **exclusão**
de novo e recusa a **inclusão** de outra vigência no mesmo ano, com o aviso de que a chave
está excluída; a **alteração** é aceita e devolve o registro ao cadastro com a descrição
nova; na **consulta** a conferência da chave excluída é dispensada.

[?] Como a alteração regrava a situação do registro junto com a descrição, uma vigência
excluída que seja alterada volta a valer. Se o efeito pretendido era só corrigir a
descrição de um registro excluído, ou se alterar é a forma de "reviver" a vigência, é
pergunta ao site.

### RN-09 — A consulta mostra a vigência ou lista as datas do grupamento, e não grava nada

Na consulta, informando o **código do grupamento e a data**, a tela mostra a descrição
daquela vigência. Informando **só o código**, a tela mostra a descrição do grupamento e
lista as **datas das vigências** já cadastradas para ele, até **12 datas**; a primeira
vigência encontrada preenche os campos de dia, mês e ano. Não achando vigência naquela
data, avisa **\* Grupamento nao cadastrado nesta data \***; não achando o grupamento, avisa
**\* Grupamento nao cadastrado \***. A consulta não inclui, não altera e não exclui nada, e
não gera registro de auditoria.

[?] A ordem em que as datas saem na lista — e qual delas ocupa os campos de dia, mês e ano
— depende do mesmo posicionamento de leitura da RN-04, cujo efeito não está no acervo. Se a
lista sai da vigência mais antiga para a mais nova, muda o que o operador vê. Pergunta ao
site.

### RN-10 — Inclusão, alteração e exclusão deixam registro na auditoria

Toda inclusão, alteração e exclusão de vigência grava, além do cadastro, um registro de
auditoria com a **tela de origem**, a **operação**, o **conteúdo anterior** e o **conteúdo
posterior** do registro, a **matrícula** do funcionário, a estação, o número do processo, a
sessão (dia, mês, ano e hora), a CRE e o tipo de órgão. Na inclusão o conteúdo anterior vai
em branco e o posterior é a vigência incluída; na alteração os dois conteúdos são
preenchidos; na exclusão o conteúdo posterior vai em branco. A consulta não gera auditoria.

### RN-11 — Antes de deixar operar, o sistema confere a tela, a matrícula e a operação

A abertura da tela passa por três conferências com o contexto da sessão. A **tela** precisa
estar cadastrada no cadastro de telas: não estando, o acesso é recusado com **\* Tela nao
disponivel \***. A **matrícula** precisa ter a tela autorizada no seu código de acesso: não
tendo, a recusa é **\* Acesso negado para esta matricula \***. A **operação** pretendida
precisa estar liberada no mesmo código de acesso: inclusão, alteração e exclusão têm, cada
uma, a sua permissão, e sem a da operação a recusa é **\* Acesso negado para esta operacao
\***.

[?] A consulta não é conferida contra nenhuma permissão: quem tem a tela autorizada
consulta sem precisar da permissão de consulta, embora o cadastro de autorização tenha esse
indicador. Se a intenção era exigir essa permissão por tela, o caminho não a exige.
Pergunta ao site.

### RN-12 — O cabeçalho mostra a data do sistema e o tipo de órgão da sessão

Fora do cadastro, a tela exibe a **data do sistema** e a **descrição do tipo de órgão** da
sessão.

[?] Nem a data do sistema nem o tipo de órgão são preenchidos por nenhum programa do acervo
lido: os dois só aparecem como origem de cópia e são inicializados em branco pelo ambiente
comum. De onde vêm os valores é pergunta ao site; se não vierem do ambiente, os dois campos
saem em branco.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os grupamentos de classificação de licitação e suas vigências

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C240T

  Cenário: A tela abre pronta para incluir
    Quando abro a tela C240T
    Então os campos de dados vêm em branco
    E a operação que a tela mostra é a inclusão

  Cenário: Inclusão de uma vigência nova
    Dado que o grupamento 1234 não tem vigência cadastrada em 01/03/2020
    Quando informo o grupamento, a data 01/03/2020 e a descrição
    Então a vigência é gravada no cadastro do grupamento
    E a operação fica registrada na auditoria

  Cenário: Inclusão sem o grupamento
    Quando envio a tela com o campo do grupamento em branco
    Então vejo a mensagem "* Informe o Grupamento *"
    E o cursor volta ao campo do grupamento
    E nada é gravado

  Cenário: Data de vigência inválida
    Quando informo um dia que não existe no mês, ou um ano fora da faixa de 1994 a 2099
    Então vejo a mensagem "* Data de inicio invalida *"
    E o cursor volta ao campo do dia da vigência
    E nada é gravado

  Cenário: Inclusão sem a descrição
    Dado que informo o grupamento e a data
    Quando deixo a descrição em branco
    Então vejo a mensagem "* Informe descricao do grupamento *"
    E o cursor volta ao campo da descrição
    E nada é gravado

  Cenário: A vigência informada já está cadastrada
    Dado que o grupamento já tem uma vigência naquela data
    Quando tento incluir a mesma data
    Então vejo a mensagem "* Grupamento ja cadastrado *"
    E nada é gravado

  Cenário: A vigência informada não é posterior à última do grupamento
    Dado que a última vigência do grupamento começa em 10/05/2020
    Quando informo uma data igual ou anterior a 10/05/2020
    Então vejo a mensagem "* <- Grupamento ja ativo nesta data *"
    E vejo a data da vigência que já está valendo
    E nada é gravado

  Cenário: Segunda vigência do mesmo grupamento no mesmo ano
    Dado que o grupamento já tem uma vigência em 2020
    Quando informo outra data de 2020, posterior à última vigência
    Então o sistema recusa a inclusão pela chave do cadastro
    E nada é gravado

  Cenário: Alteração da descrição de uma vigência existente
    Dado que o grupamento tem a vigência de 10/05/2020
    Quando informo a operação de alteração, a mesma data e uma descrição nova
    Então o cadastro fica com a descrição nova
    E a auditoria guarda o conteúdo anterior e o novo

  Cenário: Alteração de vigência que não existe naquela data
    Dado que o grupamento não tem vigência na data informada
    Quando tento alterar
    Então vejo a mensagem "* Grupamento nao cadastrado nesta data *"
    E nada é gravado

  Cenário: Exclusão de uma vigência existente
    Dado que o grupamento tem a vigência de 10/05/2020
    Quando informo a operação de exclusão e a data
    Então a vigência fica marcada como excluída e deixa de valer
    E a auditoria guarda o conteúdo anterior

  Cenário: Operação sobre vigência já excluída
    Dado que a vigência do grupamento naquele ano está marcada como excluída
    Quando tento excluí-la de novo, ou incluir outra vigência no mesmo ano
    Então vejo o aviso de que a chave está excluída
    E nada é gravado

  Cenário: Alteração de uma vigência excluída
    Dado que a vigência do grupamento naquele ano está marcada como excluída
    Quando informo a operação de alteração com uma descrição nova
    Então o cadastro fica com a descrição nova e a vigência volta a valer

  Cenário: Consulta pelo grupamento e pela data mostra a vigência
    Dado que o grupamento tem a vigência de 10/05/2020, com a sua descrição
    Quando informo a operação de consulta, o grupamento e a data
    Então vejo a descrição daquela vigência
    E nada é gravado

  Cenário: Consulta só pelo grupamento lista as vigências
    Dado que o grupamento tem vigências cadastradas
    Quando informo a operação de consulta e só o código do grupamento
    Então vejo a descrição do grupamento e até 12 datas de vigência
    E nada é gravado

  Cenário: Consulta de grupamento não cadastrado
    Quando consulto um grupamento que não existe
    Então vejo a mensagem "* Grupamento nao cadastrado *"
    E nada é gravado

  Cenário: A consulta não deixa rastro
    Dado que abro a tela em consulta
    Quando a consulta é mostrada
    Então nenhuma vigência é incluída, alterada ou excluída
    E nenhum registro de auditoria é gerado

  Cenário: Operação não permitida no código de acesso
    Dado que o meu código de acesso não tem a permissão da operação pretendida
    Quando tento incluir, alterar ou excluir
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Tela não cadastrada
    Dado que a tela C240T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela C240T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: O cabeçalho da tela
    Dado que entrei no sistema
    Quando abro a tela C240T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão
```
