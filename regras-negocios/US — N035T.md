# US — N035T — Manutenção dos modelos de nota fiscal

## Estória

Como **servidor da CRE**, quero **manter o cadastro dos modelos de nota fiscal**,
para que as telas que registram nota usem o modelo certo e não recusem a nota por
falta de modelo cadastrado.

O modelo é o código curto que qualifica a nota fiscal: as telas do módulo o leem
pelo código e mostram a descrição. Sem o modelo no cadastro, a nota não entra — a
tela que a registra recusa o modelo que não encontra. É esta tela que mantém esse
cadastro: inclui, altera e exclui modelos, e é a única do sistema que o faz.

## Contexto

Jornada S000M → N000M → N050M → N035T.

Ator: servidor da CRE — mantém o cadastro dos modelos de nota fiscal que as demais
telas do módulo leem.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio.

As duas telas do meio do caminho são menus: não deixam nada de próprio para esta
tela, apenas dizem qual tela abrir. O que a N035T usa da sessão — a matrícula, o
código de acesso, o privilégio, o tipo de órgão, a CRE e o terminal — foi deixado
pela entrada. A tela não compara a tela de origem com código nenhum: o
comportamento dela não muda conforme quem a chamou. E ela não encadeia para outra
tela — a jornada termina nela, e nada é passado adiante.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O cadastro que a tela mantém é o dos modelos de nota fiscal

O cadastro é o dos **modelos de nota fiscal** e tem dois dados: o **código do
modelo**, de 2 posições, que o identifica, e a **descrição**, de 40 caracteres, de
preenchimento obrigatório. O código é a chave do cadastro e não se repete. A
capacidade do cadastro é de **100 modelos** — **capacidade** (máximo esperado,
parâmetro de dimensionamento), não volume cadastrado.

### RN-02 — Só esta tela mantém o cadastro; as demais telas apenas o leem

**Doze** outros programas do sistema leem este cadastro, sempre pelo código do
modelo, para obter a descrição — entre eles a N014T, que registra a nota fiscal e
recusa com **\* Modelo de nota fiscal nao cadastrado \*** quando o modelo
informado não está no cadastro. Só a N035T inclui, altera e exclui modelos.
Excluir um modelo, portanto, tira-o de circulação para todas as telas que o leem.

### RN-03 — Cada linha traz a sua ação

A confirmação é linha a linha: cada linha da página tem uma **ação**, que diz o
que fazer com aquele modelo. A ação de **inclusão** cadastra o modelo, a de
**alteração** muda a descrição e a de **exclusão** apaga o modelo. A ação vale
para a linha em que foi informada, e a tela processa uma linha por vez.

### RN-04 — A página tem 15 linhas e um modo de manutenção próprio

A tela apresenta **15 linhas** por página — o mesmo limite que ela fixa nas duas
passagens em que trabalha, a de conferência e a de gravação. Cada linha tem o
código do modelo (2 posições), a descrição (40) e a ação (1). O cabeçalho tem o
**modo de manutenção da página** (3 posições) e o **prefixo de rota** (5), e
mostra a descrição do tipo de órgão da sessão e a data do sistema.

### RN-05 — O modo da página só admite alteração e consulta

A página é usada em dois modos: **alteração** e **consulta** — os mesmos que a
mensagem de recusa nomeia como **ALT** e **CON**. Quando a transação chega sem
modo informado, a própria tela o preenche com o de consulta. Com qualquer outro
valor — inclusive o modo em branco — a manutenção não é validada: a recusa é
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta no campo do
modo, e nada é gravado. Um valor que o sistema não reconheça de todo é recusado
antes disso, pela conferência de rota, com **\* Operacao nao disponivel \***.

[?] A mensagem manda usar ALT ou CON, mas essas duas palavras não são reconhecidas
em ponto nenhum do sistema: os valores que ele aceita e confere são os códigos
internos de alteração e de consulta, e é com o código de consulta que a própria
tela preenche o campo quando ele vem em branco. Ou o formulário da tela traduz o
que o servidor digita, ou a mensagem indica valores que a tela recusa. Pergunta ao
site.

### RN-06 — No modo consulta nada é validado nem gravado

Com o modo da página igual a consulta, o processamento de cada linha é abandonado
antes de qualquer teste de ação — tanto na passagem de conferência quanto na de
gravação. É a garantia de que a consulta é somente leitura.

### RN-07 — Sem modelo na primeira linha, a tela avisa que não há modelos cadastrados

Ao abrir, a tela busca os modelos e mostra os que encontra, até 15, cada um com o
código e a descrição. A busca começa pelo número que ficou guardado da consulta
anterior — zero quando ainda não houve nenhuma. Quando a busca da primeira linha
não devolve registro, não há linha nenhuma para mostrar: a tela avisa
**\* Nao existem modelos cadastrados \*** e põe o cursor no campo do código do
modelo.

[?] O aviso fala de modelos cadastrados, mas o que o dispara é a busca da primeira
linha não devolver registro, e essa busca parte de um número guardado (zero na
primeira vez). Se a busca for pela igualdade do número, o aviso aparece mesmo
havendo modelos, desde que nenhum tenha aquele número; se for pela ordem, ele quer
dizer que a lista começou depois do último modelo. A semântica da busca neste
dialeto não está no acervo. Pergunta ao site.

### RN-08 — A inclusão recusa código já cadastrado

A ação de inclusão é traduzida para a operação de inclusão e cadastra o modelo.
Antes, a tela lê o cadastro pelo código do modelo: se ele já existe, a inclusão é
recusada com **\* Modelo ja cadastrado \***, com o cursor na coluna da ação, e o
modelo existente não é tocado.

### RN-09 — A alteração e a exclusão exigem modelo cadastrado

Para as ações de alteração e de exclusão, a tela exige que o modelo exista no
cadastro. Se a leitura pelo código não encontra o registro, a operação é recusada
com **\* Modelo nao cadastrado \***, com o cursor na coluna da ação.

### RN-10 — A inclusão e a alteração exigem a descrição

Nas ações de inclusão e de alteração, descrição em branco é recusada com
**\* Informe a descricao do modelo \***, com o cursor na coluna da descrição. É a
única exigência de preenchimento do cadastro — o código é obrigatório apenas
porque a linha sem código não é processada (RN-14).

### RN-11 — A inclusão grava o modelo e registra o valor posterior

Passadas as guardas e a conferência da operação, a inclusão cria o registro do
modelo e o grava, com o código e a descrição informados na linha. A auditoria
recebe o valor posterior — o modelo novo — e a operação de inclusão.

### RN-12 — A alteração grava a nova descrição e registra a anterior

A ação de alteração lê o modelo, guarda o registro anterior, reserva o registro,
substitui a descrição pela que foi informada na linha e grava. A auditoria recebe
o valor anterior e o posterior — o código e a descrição antes e depois.

### RN-13 — A exclusão apaga o modelo e não verifica se ele está em uso

Confirmada a exclusão, a tela reserva o registro, apaga o modelo e deixa o rastro
na auditoria. Ela **não** verifica se o modelo está em uso: além do próprio
cadastro dos modelos, a tela só lê o cadastro de telas da sessão e só escreve a
auditoria. Excluir um modelo que as telas de nota usam não é impedido.

### RN-14 — Linha sem código ou com ação desconhecida é ignorada

Uma linha só é processada se o código do modelo estiver preenchido **e** a ação
for uma das três. Código em branco, ação em branco ou ação fora das três passa
batido: não gera recusa nem gravação.

### RN-15 — Cada operação só é conferida com a sessão e a autorização validadas

Ao abrir e a cada confirmação, antes de conferir as linhas, a tela chama as
conferências comuns do sistema. Elas exigem que o terminal da sessão seja o do
cadastro do servidor — senão o acesso é encerrado —, que a tela esteja no perfil
do servidor e que o código de acesso dele tenha a tela e, para cada linha
confirmada, a operação pretendida: inclusão, alteração ou exclusão. Sem isso a
linha não é conferida, nada é gravado e nada é auditado: o servidor vê
**\* Tela nao disponivel \***, **\* Tela nao cadastrada \***,
**\* Acesso negado para esta matricula \*** ou
**\* Acesso negado para esta operacao \***.

### RN-16 — Prefixo de rota preenchido desvia a tela

Se a transação chega com o prefixo de rota preenchido, a conferência de rota é
interrompida e o servidor é levado para a tela indicada nesse prefixo: nenhuma
linha é conferida nessa passagem e nada é gravado nesta tela.

[?] O mecanismo está no acervo — a conferência de rota devolve o prefixo como a
próxima tela —, mas não quem preenche esse prefixo nas transações que chegam à
N035T. Pergunta ao site.

### RN-17 — Toda operação confirmada deixa rastro na auditoria

Cada operação confirmada grava um registro no cadastro de auditoria (A010T): o
objeto auditado (o cadastro dos modelos), a operação, o valor anterior, o valor
posterior e o contexto da sessão — matrícula, código de acesso, secretaria, CRE,
tipo de órgão, terminal, data e hora e número do processo.

[?] O código de manutenção do rastro recebe o mesmo valor nas três operações —
quem distingue a operação é o campo próprio da operação. O significado desse
código não está no acervo. Pergunta ao site.

### RN-18 — A recusa de destino inválido não é apresentada por esta tela

A distribuição automática entre destinos tem uma recusa própria — **destino
inválido** —, que a ficha da tela lista entre as mensagens dela. O ramo só roda
com o modo de distribuição automática preenchido, e a tela limpa esse campo
imediatamente antes dos pontos em que ele poderia disparar. Pela N035T, portanto,
essa mensagem não é apresentada.

---

## Cenários BDD

```gherkin
Funcionalidade: Manutenção dos modelos de nota fiscal

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, o código de acesso, o privilégio, a CRE e o terminal
    E tenho acesso à tela N035T

  Cenário: RN-01, RN-02 e RN-04 — a consulta lista os modelos em 15 linhas
    Dado que estou na tela N035T
    Quando a página é apresentada
    Então vejo até 15 linhas, cada uma com o código, a descrição e a ação do modelo
    E vejo o modo de manutenção da página
    E vejo a descrição do tipo de órgão da sessão e a data do sistema
    E o código do modelo é a chave do cadastro e não se repete
    E é este mesmo cadastro que as outras telas leem pelo código

  Cenário: RN-03 — cada linha traz a sua ação
    Dado que estou na tela N035T no modo de alteração
    Quando informo a ação de inclusão, de alteração ou de exclusão em uma linha
    Então a linha é tratada pela operação correspondente

  Cenário: RN-05 — opção de manutenção não disponível
    Dado que estou na tela N035T
    Quando o modo de manutenção da página não é o de alteração nem o de consulta
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-05 — o modo em branco é preenchido com consulta
    Dado que a transação chega à N035T sem modo de manutenção informado
    Quando a tela abre
    Então o modo de manutenção da página está preenchido com o de consulta

  Cenário: RN-06 — a consulta não grava nada
    Dado que estou na tela N035T no modo de consulta
    Quando percorro e confirmo as linhas da página
    Então nenhum modelo é incluído, alterado ou excluído
    E nenhum rastro de auditoria é criado

  Cenário: RN-07 — não há modelos cadastrados
    Dado que estou na tela N035T
    Quando a busca da primeira linha não devolve registro
    Então não vejo linha alguma
    E vejo "* Nao existem modelos cadastrados *"
    E o cursor fica no campo do código do modelo

  Cenário: RN-08 — inclusão de modelo já cadastrado é recusada
    Dado que estou na tela N035T no modo de alteração
    Quando tento incluir um modelo cujo código já está cadastrado
    Então vejo "* Modelo ja cadastrado *"
    E o cursor fica na coluna da ação
    E o modelo existente não é alterado

  Cenário: RN-09 — alteração e exclusão de modelo não cadastrado são recusadas
    Dado que estou na tela N035T no modo de alteração
    Quando informo a ação de alteração ou a de exclusão para um código que não existe
    Então vejo "* Modelo nao cadastrado *"
    E o cursor fica na coluna da ação

  Cenário: RN-10 — inclusão e alteração sem descrição são recusadas
    Dado que estou na tela N035T no modo de alteração
    Quando tento incluir ou alterar um modelo deixando a descrição em branco
    Então vejo "* Informe a descricao do modelo *"
    E o cursor fica na coluna da descrição

  Cenário: RN-11 — a inclusão grava o modelo novo
    Dado que estou na tela N035T no modo de alteração
    E que o código informado não está cadastrado
    Quando informo a descrição e confirmo a ação de inclusão
    Então o modelo é cadastrado com esse código e essa descrição
    E a auditoria registra a inclusão com o valor posterior

  Cenário: RN-12 — a alteração grava a nova descrição
    Dado que estou na tela N035T no modo de alteração
    E que o modelo está cadastrado
    Quando informo a nova descrição e confirmo a ação de alteração
    Então a descrição do modelo é gravada
    E a auditoria registra o valor anterior e o posterior

  Cenário: RN-13 — a exclusão apaga o modelo
    Dado que estou na tela N035T no modo de alteração
    E que o modelo está cadastrado
    Quando confirmo a ação de exclusão
    Então o modelo é apagado do cadastro
    E a auditoria registra a exclusão com o valor anterior
    E a tela não verifica se o modelo está em uso nas notas

  Cenário: RN-14 — linha sem código ou com ação desconhecida é ignorada
    Dado que estou na tela N035T no modo de alteração
    Quando deixo o código do modelo em branco, ou informo uma ação que não é nenhuma das três
    Então a linha não é conferida, não gera recusa e nada é gravado para ela

  Cenário: RN-15 — operação sem autorização
    Dado que estou na tela N035T e confirmo uma linha
    Quando a conferência da sessão, da tela ou da operação daquela linha não passa
    Então vejo "* Tela nao disponivel *", "* Tela nao cadastrada *",
      "* Acesso negado para esta matricula *" ou "* Acesso negado para esta operacao *"
    E nada é gravado e nenhum rastro de auditoria é criado

  Cenário: RN-15 — sessão em terminal diferente do cadastro
    Dado que estou na tela N035T e confirmo uma linha
    Quando o terminal da minha sessão não é o do meu cadastro
    Então o acesso é encerrado e nada é gravado

  Cenário: RN-16 — prefixo de rota preenchido desvia a tela
    Dado que a transação chega à N035T com um prefixo de rota preenchido
    Quando a conferência de rota é chamada
    Então sou levado para a tela indicada no prefixo
    E nenhuma linha é conferida e nada é gravado

  Cenário: RN-17 — toda operação confirmada deixa rastro na auditoria
    Dado que confirmei uma inclusão, uma alteração ou uma exclusão na N035T
    Quando a gravação termina
    Então existe um registro de auditoria do cadastro dos modelos
    E ele traz a operação, o valor anterior e o valor posterior
    E traz a matrícula, o código de acesso, a secretaria, a CRE e o terminal
    E traz a data e a hora e o número do processo

  Cenário: RN-18 — a recusa de destino inválido não é apresentada
    Dado que confirmei uma operação na N035T
    Quando a gravação é preparada
    Então a tela limpa o modo de distribuição automática
    E a recusa de destino inválido não é apresentada
```
