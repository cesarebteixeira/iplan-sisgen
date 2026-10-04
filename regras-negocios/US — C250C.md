# US — C250C — Consultar as justificativas do tipo de órgão

## Estória

Como **servidor de CRE que lança o mapa de atendimento de uma unidade**, quero
**consultar a relação das justificativas que o tipo de órgão da minha secretaria
tem cadastradas, com o código e a descrição de cada uma**, para que **eu informe
no mapa a justificativa certa sem ter de adivinhar o código**.

Cada dia do mapa de uma unidade leva uma justificativa, e o mapa só aceita um
código que exista no cadastro da secretaria. Sem a relação à mão, quem lança o
mapa erra o código e o dia fica sem a justificativa que lhe cabe — e é essa
relação que a tela entrega. Ela é só de leitura: quem inclui, altera e exclui
justificativa é a tela de manutenção do cadastro.

## Contexto

Jornada S000M → M000M → M040T → C250C.

Ator: servidor de CRE — consulta as justificativas do tipo de órgão da sua sessão
de dentro da tela do mapa da unidade.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio.

A tela desta jornada **não** é aberta por menu: a `M040T` — a tela do mapa, que a
`M000M` abre pela opção 10 — **encadeia** nela, passando-lhe o **órgão filho da
unidade em uso**, e a `C250C` a ela devolve o controle com a marca de inclusão
(RN-08). O modo da `C250C`, porém, **não** depende de quem a chamou: ela adota a
consulta sempre (RN-05). O que ela usa da sessão é o **tipo de órgão (a
secretaria)**, a **matrícula**, o **código de acesso** e o **privilégio** — regra
da entrada, registrada no anexo de evidências, em **Regras que se revelaram da
entrada**.

## Regras de negócio

### RN-01 — A tela consulta as justificativas do tipo de órgão da sessão

Esta é uma tela de **consulta**. Ela mostra a relação das **justificativas**
cadastradas para o **tipo de órgão** que o meu vínculo com a secretaria deixou na
sessão — nunca para um órgão digitado, que não se digita aqui. O cabeçalho mostra
a **descrição da secretaria** e a **data do sistema**, e cada linha traz o
**código da justificativa** e a **descrição**.

A relação é presa ao tipo de órgão: a justificativa de outro tipo de órgão **não**
entra, e a leitura para na primeira que não for do tipo da sessão — as linhas que
sobrarem ficam em branco. Nada nesta tela é gravado.

### RN-02 — A relação tem 15 linhas, e cada linha informa dois dados

São **15 linhas** por vez. Cada linha informa o **código da justificativa** (2
dígitos) e a **descrição** (40 caracteres). As justificativas saem na ordem do
cadastro dentro do tipo de órgão — pelo código.

Fora da grade, a tela mostra o **campo da opção de manutenção**, o **código da
tela de destino**, o **indicador do mapa**, a **descrição da secretaria**, a
**data do sistema** e a **linha de mensagem**.

### RN-03 — A relação começa pela referência de justificativa que a sessão traz

A primeira leitura da relação parte do **código de justificativa** que estiver na
área de trabalho da sessão; chegando com referência, ela é preservada e a relação
começa por ela, e a cada linha lida a referência é atualizada, de modo que a
leitura seguinte continue a partir dali. No caminho desta jornada a tela do mapa
**zera** essa referência antes de chamá-la, de modo que a relação chega à tela sem
ponto de partida.

[?] O corpus não traz o contrato da leitura encadeada: não dá para concluir, só
por esta tela, se a referência posiciona a leitura no código exato ou na primeira
justificativa igual ou seguinte — e, se for no código exato, chegar sem referência
não listaria justificativa nenhuma. Também não dá para concluir se passar de uma
página para a seguinte repete ou pula uma justificativa, nem qual outra tela deixa
essa referência na sessão. Pergunta ao site.

### RN-04 — Tipo de órgão sem justificativa cadastrada: a tela avisa

Quando a primeira leitura da relação não encontra nenhuma justificativa para o
tipo de órgão, a tela avisa **\* Nao existe justificativa cadastrada  \*** e não
preenche nenhuma linha. O aviso é dado uma vez, ao abrir a relação.

### RN-05 — A tela é de consulta: só a consulta é aceita, e ela é adotada sempre

A opção de manutenção do cabeçalho aceita **apenas a consulta**. A própria tela
preenche o campo com a consulta quando abre, e ao confirmar qualquer outra opção
ela recusa com **\* Operacao nao disponivel \***, devolve o cursor ao campo da
opção e não faz mais nada. A mesma recusa existe na conferência de rota, que roda
antes.

O modo da tela **não** depende de quem a chamou: venha do menu ou da tela do mapa,
ela adota a consulta sempre, e não há nesta tela nenhuma comparação com a tela de
origem.

[?] O campo da opção é preenchido com o código interno de consulta, e a
conferência compara o que foi digitado com esse mesmo código interno. O corpus
lido não traz a máscara desta tela, então não dá para concluir que texto o
servidor vê no campo — se o código interno ou um mnemônico. Pergunta ao site.

### RN-06 — A tela só opera com a tela e o código de acesso autorizados

Antes de mostrar a relação, a tela confere a sessão e depois, nesta ordem, se o
cadastro de telas tem esta tela e se o meu **código de acesso** tem registro para
ela. Faltando a tela, o aviso é **\* Tela nao disponivel \***; faltando o registro
do meu código de acesso, o aviso é **\* Acesso negado para esta matricula \***.
Nos dois casos eu volto ao menu principal e nada é consultado.

A opção informada e a tela passam, em seguida, pela conferência de permissão de
operação. Como só a consulta é aceita, a conferência da operação não chega a
exigir permissão de inclusão, de alteração ou de exclusão.

[?] O cadastro de telas por código de acesso guarda as quatro permissões por
operação, entre elas a de **consulta**, e a conferência por operação desta tela
nunca lê a permissão de consulta: quem tem a tela autorizada consulta sem esse
flag. Ou a consulta é livre por desenho, ou a permissão de consulta deveria ser
exigida aqui. Pergunta ao site.

### RN-07 — O código da tela de destino leva a transação para aquela tela

Se o servidor preenche o campo do **código da tela de destino**, a transação segue
para a tela informada e mais nada desta tela é processado: a relação não é
remontada e o indicador do mapa não é considerado. Em branco, a tela segue o seu
curso normal.

[?] Esse campo não tem rótulo nem valor no material lido, porque não há máscara
desta tela; o que se sabe é o efeito de o servidor preenchê-lo. Pergunta ao site.

### RN-08 — O indicador do mapa devolve o controle à tela do mapa, em inclusão

Preenchido o **indicador do mapa**, a tela passa para a tela do mapa (a `M040T`) o
**registro do órgão filho** que recebeu de quem a chamou e a **operação de
inclusão**; os demais dados do registro vão em branco. A tela do mapa abre, por
isso, **em inclusão** para esse órgão filho. Sem o indicador, nada é entregue: a
tela apenas termina em si mesma.

A verificação do indicador é feita na **última** linha da página, e a recusa da
opção de manutenção (RN-05) na **primeira**: com a opção de manutenção errada e o
indicador do mapa preenchido ao mesmo tempo, a tela recusa e, ainda assim,
encaminha ao mapa — a menos que a recusa interrompa o resto da página, o que o
corpus não mostra.

[?] O indicador tem um caractere, não passa por conferência de valor e não tem
rótulo no material lido; o valor que o servidor digita para disparar a passagem
não está no corpus. Pergunta ao site.

[?] A entrega leva o órgão filho e a operação, mas deixa em branco a coordenadoria
regional escolar, que a tela do mapa também usa. Não dá para concluir, só por esta
tela, se a tela seguinte busca a coordenadoria na sessão ou se o servidor a
informa lá. Pergunta ao site.

### RN-09 — Consultar não grava nada

A tela só lê. Ela enxerga o cadastro de telas e o cadastro das justificativas; a
rotina comum de segurança lê ainda o cadastro de funcionários e o de acessos. Para
os dois cadastros que ela enxerga, o sistema traz prontas as operações de gravar e
de apagar, mas **nenhuma delas é executada**: não sai desta tela nenhuma
gravação, nenhum travamento de registro e nenhuma linha de auditoria.

### RN-10 — Falha no banco interrompe a consulta

Toda leitura desta tela testa o erro do banco: o erro vira a ação de erro de
acesso, com a mensagem de erro do sistema, e a operação para ali, sem completar a
relação.

## Cenários BDD

```gherkin
Funcionalidade: Consultar as justificativas do tipo de órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C250C

  Cenário: RN-01 e RN-09 — consultar a relação das justificativas do tipo de órgão
    Dado que o tipo de órgão da minha sessão tem justificativas cadastradas
    Quando confirmo a consulta
    Então vejo, em cada linha, o código e a descrição de uma justificativa
    E vejo a descrição da secretaria e a data do sistema no cabeçalho
    E nada é gravado

  Cenário: RN-01 — a relação é presa ao tipo de órgão da sessão
    Dado que outro tipo de órgão tem justificativas cadastradas
    Quando confirmo a consulta
    Então nenhuma justificativa de outro tipo de órgão aparece na relação

  Cenário: RN-02 — a relação mostra 15 justificativas
    Dado que o tipo de órgão da minha sessão tem mais de 15 justificativas cadastradas
    Quando confirmo a consulta
    Então a relação mostra 15 justificativas
    E as linhas que sobram ficam em branco

  Cenário: RN-02 — as justificativas saem na ordem do cadastro
    Dado que o tipo de órgão da minha sessão tem justificativas cadastradas
    Quando confirmo a consulta
    Então as justificativas aparecem na ordem do código

  Cenário: RN-03 — a relação começa pela referência de justificativa da sessão
    Dado que a área de trabalho da sessão traz o código de uma justificativa
    Quando confirmo a consulta
    Então aquela justificativa é o ponto de partida da leitura

  Cenário: RN-03 — a relação chega sem referência
    Dado que a tela do mapa me encaminhou sem deixar referência de justificativa
    Quando confirmo a consulta
    Então a leitura começa sem ponto de partida informado

  Cenário: RN-04 — tipo de órgão sem justificativa cadastrada
    Dado que o tipo de órgão da minha sessão não tem nenhuma justificativa cadastrada
    Quando confirmo a consulta
    Então vejo "* Nao existe justificativa cadastrada  *"
    E nenhuma linha é preenchida

  Cenário: RN-05 — a tela abre em consulta venha de onde vier
    Dado que a tela do mapa me encaminhou para a tela C250C
    Quando a tela abre
    Então o campo da opção vem preenchido com a consulta
    E não há nenhuma comparação com a tela que me encaminhou

  Cenário: RN-05 — opção diferente da consulta
    Dado que estou na tela C250C
    Quando informo uma opção de manutenção diferente da consulta e confirmo
    Então vejo "* Operacao nao disponivel *"
    E o cursor volta para o campo da opção
    E nada é gravado

  Cenário: RN-06 — tela fora do cadastro de telas
    Dado que o cadastro de telas não tem esta tela
    Quando a tela abre
    Então vejo "* Tela nao disponivel *"
    E volto ao menu principal
    E nada é consultado

  Cenário: RN-06 — sem o registro de acesso
    Dado que o meu código de acesso não tem registro para esta tela
    Quando a tela abre
    Então vejo "* Acesso negado para esta matricula *"
    E volto ao menu principal
    E nada é consultado

  Cenário: RN-06 — a consulta não exige permissão por operação
    Dado que tenho a tela autorizada no meu código de acesso
    E não tenho a permissão de consulta
    Quando confirmo a consulta
    Então a relação é mostrada

  Cenário: RN-07 — código da tela de destino informado
    Dado que estou na tela C250C
    Quando informo o código de outra tela e confirmo
    Então a transação segue para a tela informada
    E nada mais desta tela é processado

  Cenário: RN-08 — indicador do mapa preenchido
    Dado que a tela do mapa me encaminhou com o órgão filho de uma unidade
    E a relação mostra as justificativas do tipo de órgão
    Quando preencho o indicador do mapa e confirmo
    Então a tela do mapa M040T abre em inclusão para aquele órgão filho
    E nada é gravado por esta tela

  Cenário: RN-08 — indicador do mapa em branco
    Dado que a relação mostra as justificativas do tipo de órgão
    Quando confirmo sem preencher o indicador do mapa
    Então a tela termina em si mesma
    E nenhuma tela se abre

  Cenário: RN-09 — consultar não deixa rastro
    Dado que faço uma consulta
    Quando a consulta termina
    Então nenhum registro é travado
    E nenhuma linha nova aparece na trilha de auditoria

  Cenário: RN-10 — falha do banco durante a consulta
    Dado que a leitura do cadastro falha no banco
    Quando confirmo a consulta
    Então a operação é interrompida com a mensagem de erro do sistema
    E a relação não é completada
```
