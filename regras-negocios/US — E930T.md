# US — E930T — Registrar a entrega dos cartões de um contrato

## Estória

Como **servidor da coordenação regional escolar (CRE)**, quero **registrar quais
cartões de um contrato foram entregues aos alunos de cada órgão filho (SDI)**,
para que **a coordenação saiba o que ainda falta entregar e possa cobrar a
pendência de cada órgão antes de o contrato fechar**.

A entrega do cartão é o que separa o cartão emitido do cartão na mão do aluno. É
este registro que alimenta as quantidades de cartões entregues e não entregues do
contrato, e é delas que a coordenação se serve para cobrar o órgão e para fechar a
prestação do serviço. Sem esse registro, o contrato fecha sem que ninguém saiba
quais alunos ficaram sem o cartão, e a cobrança da pendência sai contra o órgão
errado. O registro é também o que a auditoria lê depois para saber quem mudou a
entrega de cada cartão.

## Contexto

Jornada S000M → E000M → E900M → E930T.

Ator: servidor da CRE — registra a entrega dos cartões do contrato, órgão filho por
órgão filho.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada são menus, e não telas encadeadas: a tela desta
jornada é aberta por escolha de menu e não recebe registro nem operação de quem a
chamou. Ela abre em branco, e por isso é a própria tela que decide se a transmissão
é consulta ou alteração — não há tela de origem determinando o modo.

O cadastro de cartões é mantido por esta tela e pelas telas irmãs do mesmo menu (o
cancelamento, o bloqueio, a troca do cartão bloqueado e o estorno), que são quem cria
e desfaz as situações *Cancelado* e *Bloqueado* que esta tela apenas mostra. A
contagem de cartões entregues e não entregues que esta tela ajusta é a que a consulta
de entrega (`E960T`) publica depois. A tela termina nela mesma: não abre outra tela
nem encaminha o usuário para lugar nenhum.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela registra a entrega dos cartões de um contrato

A tela registra, para os cartões de um contrato de referência — ano e número — de um
órgão filho (SDI) e da coordenação regional escolar a que ele pertence, quais foram
entregues aos alunos e quais não foram. O que ela grava é a **situação de entrega de
cada cartão**: **entregue** ou **não entregue**. Um cartão pode ainda estar
**cancelado** ou **bloqueado** — situações que as telas irmãs do cartão mantêm, e que
esta tela mostra mas não cria.

A gravação é no cadastro de cartões, e a única alteração que esta tela faz nele é a
situação de entrega. Nada mais do cadastro de cartões, do contrato, do órgão ou do
fornecedor é gravado, alterado ou excluído por esta tela.

### RN-02 — O que a tela mostra e o que ela mantém

A tela mostra o órgão filho (SDI) com o seu nome, a coordenação, o contrato — ano e
número —, o fornecedor do contrato com a sua razão social, a vigência do contrato e a
situação dele. Abaixo, uma lista de **até 11 cartões por vez**. Cada linha traz a
**matrícula do aluno**, o **número do cartão**, o **texto da situação** (*Cancelado*,
*Bloqueado*) e a **entrega** (*Sim*, quando entregue). O campo que o operador muda é o
**código da situação** da linha.

A vigência é montada das datas de início e de limite do contrato, no formato
dia/mês/ano, com as duas datas separadas por " a " — o campo tem 23 posições,
exatamente as duas datas de dez caracteres e o separador no meio. Quando o contrato
está fechado, a situação mostrada é a palavra **Contrato Fechado**; nas demais
situações o campo aparece todo tracejado, sem palavra nenhuma.

O cadastro de cartões está dimensionado para **2 milhões de registros** e o de
contratos de referência para **mil**. Isso é **capacidade** (o máximo esperado no
dimensionamento), não a quantidade cadastrada.

### RN-03 — A lista parte da posição informada e avança cartão a cartão

Ao entrar, a tela percorre os cartões do contrato no órgão informado e preenche as
11 linhas, uma leitura por linha, começando pela posição indicada no **campo
auxiliar (NRPEDAUX)**. A cada cartão lido a posição avança, de modo que a linha
seguinte traz o cartão seguinte.

Quando existem mais cartões do que as 11 linhas, o campo auxiliar fica com a posição
do último cartão mostrado, e repetir a transmissão continua a lista a partir dali.
Quando a lista termina antes da última linha, o campo é limpo e a lista recomeça do
início. Não achando nenhum cartão para o órgão já na primeira linha, a tela avisa
**\* Orgao sem cartoes cadastrados \*** e não preenche a grade.

[?] A posição guardada com que a lista começa é zero. Se a leitura do cadastro for
pela chave exata, essa posição nunca corresponde a um cartão e a lista nunca abre; se
for a partir da chave, a lista abre no primeiro cartão do contrato. Qual das duas a
rotina de leitura faz não está no acervo nem no manual. Pergunta ao site.

### RN-04 — A opção de manutenção é alteração ou consulta, e a opção em branco herda a anterior

A tela exige a opção de manutenção: as aceitas são **alteração** e **consulta**.
Informada qualquer outra — inclusive em branco, na primeira vez —, o sistema recusa
com **\* Operacao nao disponivel. Use ALT ou CON \***, devolve o cursor ao campo da
opção e não processa mais nada naquela transmissão. Quando a opção é deixada em
branco, a tela reaproveita a opção da transmissão anterior.

[?] A mensagem manda usar ALT e CON, mas a conferência do sistema aceita os códigos
internos de alteração e de consulta. Onde a máscara da tela traduz o rótulo que o
operador digita no código que o programa confere não está no acervo. Se não houver
tradução, quem digitar ALT ou CON é recusado sempre. É pergunta ao site.

### RN-05 — O órgão e a coordenação informados têm de estar no alcance do usuário

O órgão filho é obrigatório: em branco, a recusa é **\* Informe o orgao \***, com o
cursor de volta ao campo. Informado, o sistema procura o órgão no cadastro de
órgãos: não achando, recusa com **\* Orgao nao cadastrado \***. Quando o vínculo do
usuário tem um órgão filho, só esse passa: informar outro é recusado com
**\* Usuario sem acesso a outro orgao \***. A coordenação regional escolar segue a
mesma lógica: havendo uma coordenação no vínculo, informar outra é recusado com
**\* Usuario sem acesso ao grupo deste Orgao \***; não havendo, qualquer coordenação
cadastrada passa. Passando pelas duas, o órgão e a coordenação informados viram os
da sessão.

[?] As duas recusas de alcance dependem de valores da sessão — o órgão filho e a
coordenação do vínculo do usuário — que, em todo o acervo lido, só aparecem zerados
na área que esta tela consulta; a entrada do sistema grava o órgão e a coordenação
do vínculo noutra área. Ou as duas recusas nunca disparam — e qualquer órgão e
qualquer coordenação cadastrados passam —, ou a área é preenchida por rotina fora do
programa. Não escolhi um dos dois lados. Pergunta ao site.

### RN-06 — A consulta exige o contrato cadastrado e com cartões no órgão

A consulta do contrato exige o número: em branco, a recusa é
**\* Informe o contrato \***, com o cursor de volta ao campo do contrato. Informado,
o sistema procura o contrato pelo tipo de órgão da sessão, pelo ano e pelo número; não
achando, recusa com **\* Contrato nao cadastrado \***. Achando, verifica se o
contrato tem cartões para o órgão: não tendo, recusa com
**\* Contrato sem cartoes cadastrados \***. Passando, a tela guarda o contrato,
mostra a razão social do fornecedor e a vigência, e passa a listar os cartões dele.

O fornecedor mostrado é o do contrato, lido no cadastro de fornecedores pelo código
que o contrato carrega — não um informado na tela.

### RN-07 — A alteração exige o contrato já consultado e o contrato aberto

Para alterar, o contrato informado tem de ser o mesmo que a tela guardou da
consulta anterior; sendo outro, a alteração é recusada com
**\* Consulte antes de atualizar \***, com o cursor de volta ao campo da opção. E o
contrato não pode estar fechado: estando, a alteração é recusada com
**\* Contrato fechado para entregas \***. Em consulta, informar o mesmo contrato da
consulta anterior não relê os cadastros: a tela usa o que já tem.

[?] A alteração depende de o contrato ter sido consultado antes, e o registro dessa
consulta vive na área de trabalho que a tela mantém de uma transmissão para a outra
— a mesma área que as outras telas da família usam com outro arranjo de campos. Se
essa memória não sobrevive de uma transmissão para a outra (ou se é sobrescrita por
outra tela), a alteração nunca é alcançada: toda alteração cairia em "consulte antes
de atualizar". Não escolhi um dos dois lados. Pergunta ao site.

[?] A tela carrega também um campo com o código da próxima tela, que deve vir vazio
— a tela não tem saída para outra tela. Vindo preenchido, a conferência da
transmissão é encerrada antes das conferências de negócio, e esse campo não é
consultado de novo no caminho que grava. Se ele pode vir preenchido, a alteração
passaria sem as conferências; se não pode, é campo morto. Pergunta ao site.

### RN-08 — A situação de entrega: só entregue e não entregue, e o cartão cancelado não muda

A tela aceita mudar a situação de entrega de um cartão para **entregue** ou **não
entregue**. Linha sem matrícula de aluno, ou com situação diferente dessas duas, não
gera operação nenhuma e a tela não avisa nada. O cartão **cancelado** não tem a
entrega alterada: a tela recusa com **\* Cartao cancelado \*** e devolve o cursor à
coluna da situação. O cartão apenas **bloqueado** não sofre essa recusa — a entrega
dele é registrada normalmente como a de qualquer outro.

A situação do cartão só é regravada quando a situação pedida é diferente da que está
no cadastro: confirmar a mesma situação não grava e não ajusta a contagem.

[?] A guarda recusa alterar a entrega de um cartão cancelado, mas o caminho que
grava tem por única condição que a situação do cartão seja diferente da pedida —
exatamente o caso recusado — e nada no programa consulta a recusa antes de gravar.
Ou a recusa (dada pela rotina comum de mensagem, fora do programa) interrompe a
transmissão e o cartão cancelado fica protegido, ou a gravação acontece e a situação
do cartão cancelado é sobrescrita. Não escolhi um dos dois lados. Pergunta ao site.

### RN-09 — A contagem de entregues e não entregues do contrato acompanha a mudança

Junto com o cartão, a tela mantém a contagem do contrato para a coordenação e o
órgão: quando um cartão passa a **entregue**, soma um aos entregues e tira um dos
não entregues; quando passa a **não entregue**, soma um aos não entregues e tira um
dos entregues. É essa contagem que a consulta de entrega publica depois. A mudança
da contagem não deixa trilha de auditoria — o que a trilha registra é a mudança do
cartão.

[?] A contagem só é ajustada quando existe o registro de contagem do contrato para
aquela coordenação e aquele órgão. Não existindo, a situação do cartão já foi
gravada e a contagem fica como estava, sem mensagem de negócio. Se essa falta é
possível no site, e o que o operador vê nesse caso, é pergunta ao site.

[?] A tela não confere o resultado da gravação do cartão antes de ajustar a
contagem: se a gravação do cartão falhar e a da contagem não, os dois ficam fora de
passo até alguém corrigir. Se essa falha é possível no site, é pergunta ao site.

### RN-10 — Toda mudança fica registrada na auditoria

A mudança da situação de entrega grava um registro na trilha de auditoria das telas,
com o cadastro auditado, a tela de origem da operação, a operação de alteração, o
conteúdo anterior e o posterior do cartão, a matrícula do funcionário, o terminal, o
dia, o mês, o ano e a hora da sessão, o tipo de órgão e a coordenação. O conteúdo
anterior é o cartão como estava; o posterior, com a nova situação de entrega. O
número do processo levado à auditoria é a **matrícula do aluno** do cartão alterado.

### RN-11 — Consulta não grava nada

Em consulta a tela lê e mostra: nenhuma situação de cartão é gravada, a contagem do
contrato não é ajustada e nenhuma trilha de auditoria é gerada.

### RN-12 — A operação só acontece se o perfil do usuário autorizar

Antes de gravar, a tela passa pelas conferências de segurança: lê o cadastro de telas
para a tela e a situação do usuário e confere a autorização da operação, levando em
conta a matrícula, o código de acesso, o privilégio, o tipo de órgão e a coordenação
da sessão. Não estando a operação autorizada, a transmissão é interrompida e nada é
gravado.

---

## Cenários BDD

```gherkin
Funcionalidade: Registrar a entrega dos cartões de um contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E930T

  Cenário: A tela abre listando os cartões do contrato
    Dado que o contrato tem cartões cadastrados para o órgão filho
    Quando abro a E930T com a coordenação, o órgão filho e o contrato
    Então vejo até 11 cartões, cada um com a matrícula do aluno, o número do cartão, a situação e a entrega
    E vejo a razão social do fornecedor do contrato e a vigência
    E nada é gravado

  Cenário: Órgão sem cartões cadastrados
    Dado que o contrato não tem cartões para o órgão filho
    Quando abro a E930T
    Então vejo a mensagem "* Orgao sem cartoes cadastrados *"
    E a lista não é preenchida

  Cenário: A lista continua a partir da posição informada
    Dado que existem mais cartões do que as 11 linhas
    Quando a lista é mostrada
    Então o campo auxiliar fica com a posição do último cartão mostrado
    E repetindo a transmissão a lista continua a partir dali

  Cenário: Opção de manutenção não informada na primeira vez
    Dado que não informei a opção de manutenção
    Quando confirmo a tela
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: Opção de manutenção indisponível
    Quando informo uma opção diferente de alteração e de consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: Órgão não informado
    Quando confirmo a tela sem o órgão filho
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor fica no campo do órgão filho
    E nada é gravado

  Cenário: Órgão não cadastrado
    Quando informo um órgão filho que não existe
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E nada é gravado

  Cenário: Órgão fora do vínculo do usuário
    Dado que o meu vínculo tem um órgão filho
    Quando informo outro órgão filho
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão filho
    E nada é gravado

  Cenário: Coordenação fora do grupo do órgão
    Dado que o meu vínculo tem uma coordenação regional escolar
    Quando informo outra coordenação
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste Orgao *"
    E nada é gravado

  Cenário: Contrato não informado
    Quando confirmo a consulta sem o número do contrato
    Então vejo a mensagem "* Informe o contrato *"
    E o cursor fica no campo do contrato
    E nada é gravado

  Cenário: Contrato não cadastrado
    Quando informo um contrato que não existe
    Então vejo a mensagem "* Contrato nao cadastrado *"
    E nada é gravado

  Cenário: Contrato sem cartões cadastrados
    Dado que o contrato existe e não tem cartões para o órgão
    Quando consulto o contrato
    Então vejo a mensagem "* Contrato sem cartoes cadastrados *"
    E nada é gravado

  Cenário: Alteração sem consultar o contrato antes
    Dado que o contrato informado não é o que a tela guardou da consulta anterior
    Quando confirmo a alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: Alteração em contrato fechado
    Dado que o contrato está fechado para entregas
    Quando confirmo a alteração
    Então vejo a mensagem "* Contrato fechado para entregas *"
    E nada é gravado

  Cenário: Registrar que um cartão foi entregue
    Dado que estou na E930T em alteração e o contrato já foi consultado
    Quando informo a situação entregue para o cartão de um aluno
    Então a situação do cartão é gravada como entregue
    E a contagem de entregues do contrato sobe um e a de não entregues desce um
    E a mudança fica registrada na auditoria

  Cenário: Registrar que um cartão não foi entregue
    Dado que estou na E930T em alteração e o contrato já foi consultado
    Quando informo a situação não entregue para o cartão de um aluno
    Então a situação do cartão é gravada como não entregue
    E a contagem de não entregues do contrato sobe um e a de entregues desce um
    E a mudança fica registrada na auditoria

  Cenário: A situação do cartão só é regravada quando muda
    Dado que a situação informada é igual à que está no cadastro do cartão
    Quando confirmo a linha
    Então nada é gravado naquela linha
    E a contagem do contrato fica como estava

  Cenário: Cartão cancelado não tem a entrega alterada
    Dado que o cartão está cancelado
    Quando informo a situação entregue para ele
    Então vejo a mensagem "* Cartao cancelado *"
    E o cursor fica na coluna da situação

  Cenário: Cartão bloqueado tem a entrega registrada
    Dado que o cartão está bloqueado
    Quando informo a situação entregue para ele
    Então a situação do cartão é gravada como entregue

  Cenário: Linha sem matrícula ou com situação desconhecida é ignorada
    Dado que deixei a matrícula do aluno em branco, ou informei uma situação diferente de entregue e de não entregue
    Quando a tela processa as linhas
    Então aquela linha não gera operação nenhuma
    E não vejo mensagem

  Cenário: Consulta não grava nada
    Dado que estou na E930T em consulta
    Quando a tela processa as linhas
    Então nenhuma situação de cartão é gravada
    E a contagem do contrato não é ajustada
    E nenhuma trilha de auditoria é gerada

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não tem a autorização para a operação
    Quando tento alterar a entrega
    Então o sistema interrompe a transmissão
    E nada é gravado

  Cenário: A tela não encaminha para outra tela
    Dado que estou na E930T
    Quando a operação termina
    Então continuo na E930T
    E nenhuma outra tela é aberta
```
