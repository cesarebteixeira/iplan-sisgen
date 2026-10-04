# US — C205T — Manutenção dos projetos da secretaria

## Estória

Como **servidor de CRE com acesso a uma secretaria**, quero **manter o cadastro
dos projetos da secretaria**, para que **o órgão que executa um projeto possa ser
vinculado a um projeto que já existe, e o que a secretaria faz fique
classificado por projeto**.

O projeto é o código de dois dígitos com uma descrição, pelo qual a secretaria
identifica cada um dos seus projetos. Sem esse cadastro não há a que vincular: o
vínculo entre o órgão e o projeto procura um projeto que só existe aqui, e um
projeto que já está em uso por algum órgão não pode ser apagado, senão o vínculo
fica apontando para o nada. A mesma página serve de consulta da lista de
projetos: abri-la não grava nada.

## Contexto

Jornada S000M → C000M → C200M → C205T.

Ator: servidor de CRE — mantém, na secretaria a que tem acesso, o cadastro dos
projetos dessa secretaria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

As regras abaixo são só as da tela desta jornada. O `C000M` e o `C200M` são menus
e não deixam dado de negócio para esta tela: a secretaria, a matrícula, a CRE, o
código de acesso, o privilégio e a estação que ela usa são o que a entrada deixou
na sessão, e a página apenas os repassa às rotinas comuns de segurança e de rota.
O modo da página — alteração ou consulta — é o da própria página, que abre em
consulta quando nada foi informado. Esta tela é o fim da jornada: não abre outra
tela de negócio. O que ela entrega adiante é o rastro de cada operação confirmada
na auditoria, e a própria transação à rotina de rota quando a página chega com
uma próxima tela informada.

## Regras de negócio

### RN-01 — O que a tela mantém

A tela mantém o **projeto**: o **código** (2 dígitos) e a **descrição** (40
caracteres), dentro da **secretaria** a que o servidor tem acesso. O par
secretaria + código identifica o projeto e não admite repetição — o mesmo código
pode existir em outra secretaria, mas não duas vezes na mesma. A descrição é o
único campo obrigatório do cadastro. A capacidade é de **1.000** projetos —
capacidade, isto é, o máximo esperado declarado para dimensionamento, não o
volume cadastrado. Como o código tem dois dígitos e o código zero é reservado à
linha vazia (RN-07), dentro de uma secretaria cabem no máximo **99** projetos; a
capacidade de 1.000 só se alcança somando secretarias.

### RN-02 — A página tem 15 linhas, com código, descrição e ação

Cada página apresenta **15 linhas**, e cada linha tem o **código**, a **descrição**
e a **ação**. O **modo da página** e a **próxima tela** são campos de cabeçalho —
valem para a página inteira —, e não colunas de linha. O cabeçalho mostra ainda a
descrição da secretaria do acesso e a data do sistema.

### RN-03 — A tela abre em consulta e mostra os projetos da secretaria do acesso

Ao ser aberta sem modo informado, a página assume sozinha a **consulta** e o
código zero, e percorre o cadastro pela chave secretaria + código, mostrando até
15 projetos por página, em ordem de código. O que ela mostra são os projetos da
**secretaria do acesso** — aquela em que o servidor entrou no `LOGON` —, e não os
de todas; a descrição dessa secretaria aparece no cabeçalho da página.

[?] A secretaria escolhida na entrada é gravada em um campo da sessão e a página
lê a descrição de um campo de trabalho; a passagem de um para o outro não aparece
no material desta jornada. Se ela não acontecer, a página não tem secretaria por
onde filtrar. Pergunta ao site.

### RN-04 — A consulta não grava nada

Com o modo da página igual a consulta, o processamento de cada linha é abandonado
antes de qualquer conferência de ação e antes de qualquer gravação: é a garantia
de que a consulta é somente leitura.

### RN-05 — Sem projetos cadastrados, a tela avisa

Quando não há nenhum projeto para a secretaria, a página não mostra linha alguma
e avisa **\* Nao existem projetos cadastrados \***, com o cursor no código da
primeira linha. O aviso é dado uma única vez, no processamento da primeira linha
da página.

### RN-06 — O modo da página só admite ALT ou CON

O modo da página admite dois valores: **alteração (ALT)** e **consulta (CON)**.
Qualquer outro — inclusive a inclusão e a exclusão de uma página inteira — é
recusado com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no campo
do modo, e nada é processado. A conferência é feita no processamento da primeira
linha da página, que representa o modo de toda a página.

[?] A mensagem nomeia as opções como ALT e CON, mas a página confere o modo
contra os **códigos de operação do sistema**, que o ambiente carrega do catálogo
de mensagens no idioma da sessão; no programa ficam apenas os valores padrão
desse catálogo, e o catálogo do site não está neste material. Se o catálogo em
uso não traduzir a alteração e a consulta como ALT e CON, o que o operador digita
e o que a página confere não são o mesmo vocabulário, e a recusa alcança toda
opção. Pergunta ao site.

### RN-07 — Linha sem código ou com ação fora de I, A e E é ignorada

Uma linha só é processada se o **código** estiver preenchido **e** a **ação** for
inclusão (**I**), alteração (**A**) ou exclusão (**E**). Código zerado, ação em
branco ou ação que não seja uma dessas três passa batido: não gera recusa nem
gravação.

### RN-08 — A inclusão recusa projeto já cadastrado

A ação **I** inclui o projeto. Antes, o sistema lê o cadastro pela secretaria e
pelo código: se o projeto já existe, recusa com
**\* Projeto ja cadastrado \*** e devolve o cursor à coluna da ação.

### RN-09 — A alteração e a exclusão exigem o projeto cadastrado

Nas ações **A** e **E**, o sistema exige que o projeto exista no cadastro da
secretaria. Se não existe, recusa com **\* Projeto nao cadastrado \*** e devolve
o cursor à coluna da ação.

### RN-10 — A inclusão e a alteração exigem a descrição

Nas ações **I** e **A**, descrição em branco é recusada com
**\* Informe a descricao \***, com o cursor na coluna da descrição. É o único
campo obrigatório do cadastro.

### RN-11 — A exclusão é recusada enquanto o projeto estiver vinculado a um órgão

Antes de excluir, o sistema percorre o cadastro dos vínculos entre projeto e
órgão da secretaria procurando algum vínculo com aquele projeto. Havendo, recusa
com **<- Projeto cadastrado para este orgao \***, mostra o órgão do vínculo e
devolve o cursor à coluna da ação; o projeto continua cadastrado. O vínculo é
mantido por outra tela (`C207T`), não por esta: aqui ele é apenas consultado. A
chave daquele cadastro é secretaria + órgão + projeto, e a varredura vai até o
fim; a capacidade da tabela é de **1.000** registros.

[?] A recusa fala em "este órgão", mas a página não tem órgão informado — só o
projeto. A varredura alcança os vínculos de **todos** os órgãos da secretaria e
mostra o órgão do vínculo que barrou a exclusão. "Este órgão" era para ser um
órgão específico conferido, ou é o órgão do vínculo? Pergunta ao site.

### RN-12 — A inclusão grava o projeto com a secretaria do acesso

Passadas as guardas, a inclusão grava o projeto no cadastro, com o código e a
descrição informados e a **secretaria do acesso**. A operação é registrada na
auditoria (RN-15).

[?] A inclusão grava por um caminho próprio, que cria o registro; a alteração e a
exclusão pedem antes a leitura corrente do registro e só então gravam ou apagam.
O material desta jornada não diz se o caminho da inclusão também confere o
registro corrente antes de criar. Pergunta ao site.

### RN-13 — A alteração grava a descrição nova e guarda a anterior

A alteração traz o projeto para atualização, substitui a descrição pela informada
e grava; o código e a secretaria do projeto não mudam. A auditoria guarda o
conteúdo anterior e o novo.

### RN-14 — A exclusão confirmada apaga o projeto

Passadas as guardas, a exclusão traz o projeto para atualização e o apaga do
cadastro. A auditoria guarda o conteúdo apagado.

### RN-15 — Toda operação confirmada deixa rastro na auditoria

Cada operação confirmada gera um registro no cadastro de auditoria (`A010T`) com
o cadastro auditado (o cadastro de projetos da secretaria), a operação (inclusão,
alteração ou exclusão), o conteúdo anterior e o posterior, e o contexto da
sessão: matrícula, secretaria, CRE, tela, estação, data, hora e número do
processo. O conteúdo guardado é o do projeto — código, descrição e secretaria.

[?] Na inclusão, o rastro é gravado sob uma condição de retorno **diferente** de
um status que o material chama de DATA; a própria gravação do projeto limpa esse
status antes de gravar, mas, se ele voltar preenchido por outro caminho, a
inclusão não deixa rastro. A alteração e a exclusão não têm essa condição.
Pergunta ao site.

### RN-16 — Nada é gravado sem as conferências de tela, de matrícula e de operação

Antes de listar a página, e antes de validar e de gravar cada linha, a tela
repassa o contexto da sessão — matrícula, código de acesso, privilégio,
secretaria e estação — às rotinas comuns de segurança e de rota, e é a operação
pretendida (inclusão, alteração ou exclusão) que é conferida contra o perfil. As
recusas são as das rotinas comuns: **\* Tela nao disponivel \*** quando a tela
não está no cadastro de telas; **\* Tela nao cadastrada \*** quando ela está
marcada como excluída;
**\* Acesso negado para esta matricula \*** quando a matrícula não tem a tela no
seu código de acesso; **\* Acesso negado para esta operacao \*** quando a operação
não está liberada para ela; e a sessão é encerrada, em vez de a página seguir, se
a estação registrada no cadastro do funcionário não for a estação da sessão. Sem
a resposta favorável, a linha não é validada, nada é gravado e nada é auditado.

[?] A conferência da operação é feita na passagem de validação e não se repete na
passagem de gravação: se o perfil mudar entre as duas, a gravação não o
reconfere. Pergunta ao site.

### RN-17 — Uma recusa interrompe a validação do resto da página

Quando uma linha é recusada, a validação para ali: as linhas seguintes da mesma
página não são validadas, e a mensagem da recusa é a que o operador vê.

[?] O que impede a gravação depois de uma recusa é o sinalizador de erro da
rotina comum de mensagens — a passagem de gravação testa esse sinalizador, e não
a recusa. O material desta jornada não mostra se a mensagem de recusa o aciona.
Se não acionar, a gravação da página seguiria mesmo com uma linha recusada.
Pergunta ao site.

### RN-18 — A recusa de destino inválido não é apresentada

Antes de cada gravação, a página limpa o modo de distribuição automática entre
destinos. O ramo que produz a recusa de **destino inválido** só roda se esse modo
estiver preenchido; por esta página, essa recusa **não** é apresentada.

[?] A ficha estrutural da tela lista a recusa de destino inválido entre as
mensagens desta tela, mas o fonte não alcança o ramo. Divergência entre a ficha e
o comportamento, a confirmar com quem mantém o grafo.

### RN-19 — Próxima tela informada abandona a manutenção

Se a transação chega com a **próxima tela** preenchida, a validação da manutenção
é interrompida antes de qualquer teste de ação e nada é gravado: a rotina de rota
encaminha a transação para a tela informada.

[?] Quem preenche esse campo nesta jornada não se lê no material: o menu `C200M`
leva o seu próprio campo de próxima tela ao contexto da rota antes de abrir esta
página, e a passagem desse contexto para o campo da página aberta não está no
material. Se ela acontecer, uma página aberta com próxima tela informada abandona
a manutenção. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manutenção dos projetos da secretaria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C205T

  Cenário: RN-01 — o limite de projetos de uma secretaria
    Dado que a minha secretaria já tem 99 projetos cadastrados
    Quando tento incluir mais um
    Então não há código disponível, porque o código zero é reservado à linha vazia

  Cenário: RN-02 — a página tem 15 linhas
    Dado que a minha secretaria tem projetos cadastrados
    Quando a página é apresentada
    Então vejo 15 linhas, cada uma com o código, a descrição e a ação
    E vejo o modo da página e a próxima tela no cabeçalho
    E o cabeçalho mostra a descrição da minha secretaria e a data do sistema

  Cenário: RN-03 — a tela abre em consulta com os projetos da minha secretaria
    Dado que estou na tela C205T
    Quando a página é aberta sem modo informado
    Então a página está em consulta
    E vejo até 15 projetos da minha secretaria, em ordem de código, cada um com código, descrição e ação

  Cenário: RN-04 — a consulta não grava nada
    Dado que estou na tela C205T no modo CON
    Quando percorro e confirmo a página
    Então nenhum projeto é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: RN-05 — secretaria sem projetos cadastrados
    Dado que a minha secretaria não tem nenhum projeto cadastrado
    Quando abro a tela C205T
    Então não vejo linha alguma
    E vejo a mensagem "* Nao existem projetos cadastrados *"
    E o cursor fica no código da primeira linha

  Cenário: RN-06 — modo da página diferente de ALT e de CON
    Quando informo um modo de página diferente de ALT e de CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-07 — linha sem código ou com ação fora de I, A e E
    Dado que estou na tela C205T no modo ALT
    Quando deixo o código zerado, ou a ação em branco, ou escrevo uma ação que não é I, A nem E
    Então aquela linha não gera recusa nem gravação

  Cenário: RN-08 — inclusão de um projeto que já existe
    Dado que o código informado já está cadastrado na minha secretaria
    Quando marco a ação I
    Então vejo a mensagem "* Projeto ja cadastrado *"
    E o cursor fica na coluna da ação
    E o projeto existente não é alterado

  Cenário: RN-09 — alteração ou exclusão de um projeto que não existe
    Dado que o projeto não está cadastrado na minha secretaria
    Quando marco a ação A ou a ação E
    Então vejo a mensagem "* Projeto nao cadastrado *"
    E o cursor fica na coluna da ação
    E nada é gravado

  Cenário: RN-10 — inclusão ou alteração sem a descrição
    Dado que estou na tela C205T no modo ALT
    Quando marco a ação I ou a ação A sem preencher a descrição
    Então vejo a mensagem "* Informe a descricao *"
    E o cursor fica na coluna da descrição
    E nada é gravado

  Cenário: RN-11 — exclusão de um projeto vinculado a um órgão
    Dado que o projeto está cadastrado
    E que ele está vinculado a um órgão
    Quando marco a ação E
    Então vejo a mensagem "<- Projeto cadastrado para este orgao *"
    E o cursor fica na coluna da ação
    E o projeto continua cadastrado

  Cenário: RN-12 — inclusão de um projeto novo
    Dado que o código informado ainda não está cadastrado na minha secretaria
    E a descrição está preenchida
    Quando marco a ação I
    Então o projeto fica cadastrado com o código, a descrição e a minha secretaria

  Cenário: RN-13 — alteração de um projeto cadastrado
    Dado que o projeto está cadastrado
    Quando informo outra descrição e marco a ação A
    Então a descrição do projeto é gravada
    E o código e a secretaria do projeto não mudam
    E o conteúdo anterior fica na auditoria

  Cenário: RN-14 — exclusão de um projeto sem vínculo com órgão
    Dado que o projeto está cadastrado
    E que ele não está vinculado a nenhum órgão
    Quando marco a ação E
    Então o projeto é apagado do cadastro
    E o conteúdo apagado fica na auditoria

  Cenário: RN-15 — cada operação confirmada deixa rastro na auditoria
    Dado que incluí, alterei ou excluí um projeto
    Quando a operação é concluída
    Então a auditoria registra o cadastro de projetos como objeto auditado, a operação e o conteúdo anterior e o novo
    E registra a minha matrícula, a minha secretaria, a CRE, a tela, a minha estação, a data, a hora e o número do processo

  Cenário: RN-16 — a tela não está disponível
    Dado que a tela C205T não está no cadastro de telas, ou está marcada como excluída
    Quando abro a tela
    Então vejo a mensagem "* Tela nao disponivel *" ou "* Tela nao cadastrada *"
    E não consigo operar

  Cenário: RN-16 — matrícula ou operação sem autorização
    Dado que a minha matrícula não tem a tela no código de acesso, ou o perfil não libera a operação pedida
    Quando confirmo a página
    Então vejo a mensagem "* Acesso negado para esta matricula *" ou "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-17 — uma recusa interrompe a validação do resto da página
    Dado que a página tem mais de uma linha preenchida
    E a primeira linha é recusada
    Quando confirmo a página
    Então as linhas seguintes não são validadas

  Cenário: RN-18 — a recusa de destino inválido não é apresentada
    Dado que estou na tela C205T e confirmei uma inclusão
    Quando a gravação é preparada
    Então o modo de distribuição automática entre destinos é limpo
    E a recusa de destino inválido não é apresentada

  Cenário: RN-19 — a página chega com a próxima tela informada
    Dado que a transação chega à C205T com a próxima tela preenchida
    Quando a validação da manutenção começaria
    Então o processamento da linha é abandonado
    E a transação é encaminhada para a tela informada
```
