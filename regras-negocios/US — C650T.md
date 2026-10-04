# US — C650T — Cadastro das permissões do operador logístico a partir do contrato de cooperativa

## Estória

Como **servidor de CRE**, quero **cadastrar as permissões do contrato do operador
logístico a partir das permissões que o contrato de cooperativa já tem**, para que
**o operador logístico passe a operar os mesmos grupamentos — as mesmas coordenações
regionais, os mesmos fornecedores, os mesmos grupos de licitação e os mesmos períodos
vigentes — sem que ninguém os digite de novo**.

O contrato de cooperativa e o contrato do operador logístico são dois tipos de contrato
distintos: a cooperativa é quem tem as permissões lançadas e o operador logístico é quem
as executa. O caminho entre os dois é indireto: o que a cooperativa cobre vira, primeiro,
uma permissão auxiliar — que ainda não vale na operação —, e é dessa permissão auxiliar e
do período já registrado para a cooperativa que sai a permissão de verdade do operador
logístico. Esta tela é essa passagem: ela confere os dois contratos, mostra o que a
cooperativa cobre, confere que o operador logístico ainda não tem permissão e só então
pede a confirmação. Sem ela, o operador logístico fica sem permissão e não opera; com
ela, a secretaria transfere o que já estava autorizado sem redigitar item a item.

## Contexto

Jornada S000M → C000M → C050M → C060M → C650T.
Ator: servidor de CRE — informa o contrato de cooperativa e o contrato do operador
logístico, confere o que a cooperativa cobre e confirma o cadastro das permissões.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Entre a entrada e esta tela há três menus — o C000M, o C050M e o C060M —, e menu não grava
nem decide operação: apenas encaminha. Os três não gravam nada, e o contexto que esta tela
usa é o que a entrada deixou na sessão — o tipo de órgão, o código de acesso e a matrícula
—, que a tela não recalcula. Esta tela também **não lê a tela de origem**: não há no
material comparação com código de tela chamadora, e o comportamento dela não muda conforme
quem a abriu; o modo de operação não vem de quem a chamou, e sim do próprio campo do modo,
que a tela preenche com a alteração ao se apresentar.

A jornada termina aqui. A tela é folha: não encaminha para outra tela nem espera tela
seguinte — ela reabre a si mesma para pedir a confirmação e para avisar o fim do cadastro.
O que ela entrega ao sistema não é uma passagem, e sim o que grava: o período e as
permissões do contrato do operador logístico, a baixa das permissões auxiliares e os
registros da auditoria.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela só trabalha no modo de alteração

A tela se apresenta já no modo de alteração e recusa qualquer outro modo com
**\* Opcao nao disponivel. Use ALT \***, devolvendo o cursor ao campo do modo. Nada é lido
e nada é gravado.

[?] A recusa manda usar a tecla de alteração do terminal, mas a conferência exige que o
campo já traga o código interno da alteração — o mesmo código que a própria tela escreveu
ali ao se apresentar. O que a tecla do terminal envia não está no material lido: ou o
terminal traduz a tecla para esse código antes de enviar, ou a mensagem recusa justamente
o modo que ela manda usar. Pergunta ao site.

### RN-02 — O contrato de cooperativa tem de ser informado

Sem o tipo de contrato da cooperativa, a tela recusa com
**\* Informe o contrato da cooperativa \*** e devolve o cursor ao campo. Nada é gravado.

### RN-03 — O contrato de cooperativa tem de estar cadastrado para o órgão da sessão

O contrato informado tem de existir entre os tipos de contrato cadastrados para o tipo de
órgão da sessão; senão a recusa é **\* Tipo contrato nao cadastrado \***, com o cursor no
campo do contrato.

### RN-04 — O contrato informado tem de ser de cooperativa

O tipo de contrato informado tem de estar marcado, no cadastro, como tipo de permissão de
cooperativa; senão a recusa é **\* Tipo contrato nao e de cooperativa \***. O cadastro de
tipos de contrato admite três tipos de permissão — normal, cooperativa e operador
logístico —, e esta tela trabalha com dois deles.

### RN-05 — A cooperativa tem de estar sem permissão auxiliar pendente

Se houver permissão auxiliar lançada para o contrato de cooperativa, a tela recusa com
**<- Transferir todos os grupamentos para producao \***, mostrando junto a coordenação
regional da permissão auxiliar que encontrou. Isto é: a cooperativa tem de estar com os
grupamentos já transferidos para produção antes de o operador logístico ser cadastrado.

[?] O que é, em negócio, a permissão auxiliar — que as mensagens chamam de grupamento — e
por que ela precisa sair antes: o material mostra a chave, as telas que a mantêm e as
mensagens que a nomeiam, mas não define o conceito. Pergunta ao site.

### RN-06 — A cooperativa tem de ter permissão cadastrada

Sem nenhuma permissão cadastrada para o contrato de cooperativa, a tela recusa com
**<- Nao existem permiss cad. para este contrato \***, com o cursor de volta no contrato da
cooperativa. Permissão marcada como excluída não conta.

### RN-07 — A tela mostra o que a cooperativa cobre e o período registrado

Para o contrato de cooperativa, a tela monta e mostra a lista das coordenações regionais
que têm permissão — a área de trabalho desta etapa comporta 20 — e, para cada uma, o
período registrado, com as datas de início e de limite em dia, mês e ano. A periodicidade
vem do cadastro do contrato de cooperativa e aparece como **Quinzena Normal** ou, quando a
tabela do contrato é a especial, como **Quinzena Especial**. A tela devolve também a
descrição do tipo de contrato.

[?] Quando mais de uma coordenação regional tem período registrado, a tela fica com as
datas de uma só — as da última que encontrar —, porque há uma única área para as datas do
período e a leitura as sobrescreve a cada coordenação. Não concluo o que o servidor vê
nesse caso, nem se ele pode digitar as datas: a tela as devolve por cima do que foi
digitado. Pergunta ao site.

### RN-08 — O contrato do operador logístico tem de ser informado

Sem o tipo de contrato do operador logístico, a recusa é
**\* Informe o contrato do oper.logistico \***, com o cursor nesse campo.

### RN-09 — O contrato do operador logístico tem de estar cadastrado para o órgão da sessão

O contrato informado tem de existir entre os tipos de contrato cadastrados para o tipo de
órgão da sessão; senão a recusa é **\* Tipo contrato oper.logistico nao cadastrado \***,
com o cursor no campo.

### RN-10 — O contrato informado tem de ser de operador logístico

O tipo de contrato informado tem de estar marcado, no cadastro, como tipo de permissão de
operador logístico; senão a recusa é **\* Tipo contrato nao e de oper.logistico \***, com o
cursor no campo. Como cada tipo de contrato tem um único tipo de permissão, o mesmo
contrato não pode ser, ao mesmo tempo, da cooperativa e do operador logístico: os dois
contratos que esta tela pede são necessariamente diferentes.

### RN-11 — O operador logístico não pode já ter permissão cadastrada

Se já houver permissão cadastrada para o contrato do operador logístico, a tela recusa com
**<- Ja existe permiss cad para o oper.logistico \***, com o cursor de volta no campo do
contrato. É o que faz desta tela um cadastro de abertura: uma vez cadastrado, o contrato
não passa por aqui outra vez.

### RN-12 — A tela pede confirmação, e só a resposta S segue

Conferidos os dois contratos, a tela pede **\* Confirma cadastro da permissao <S/N> ? \***
com o cursor no campo da resposta e encerra a transação sem gravar. Na transação seguinte,
só **S** segue para o cadastro: qualquer outra resposta não grava nada e a tela limpa a
resposta e volta a conferir os dois contratos antes de perguntar de novo. Do mesmo modo, se
um dos dois contratos for trocado depois da pergunta, a tela confere tudo de novo, com os
contratos novos. Terminado o cadastro, a tela reabre a si mesma e avisa
**\* Cadastro sendo atualizado \***.

### RN-13 — O que a confirmação faz

Confirmado o cadastro, com os dois contratos conferidos, a tela:

1. percorre as permissões do contrato de cooperativa e, para cada uma, lança no cadastro de
   permissões auxiliares a permissão auxiliar correspondente do contrato do operador
   logístico;
2. reúne as combinações distintas de coordenação regional, data limite, fornecedor e grupo
   de licitação — a área de trabalho desta etapa comporta 500 combinações, e o que passar
   disso não é considerado;
3. apaga o período que já esteja registrado para o contrato do operador logístico em cada
   uma dessas combinações;
4. exige que exista o período registrado para o contrato de cooperativa naquela combinação
   e, existindo, cria o período do operador logístico com os mesmos dados do período da
   cooperativa — o mesmo texto de período, as mesmas datas, a mesma classe e o mesmo
   operador;
5. procura a permissão auxiliar do operador logístico naquela combinação, transforma-a na
   permissão de verdade do operador logístico, apaga a permissão auxiliar e deixa o
   registro da auditoria.

As etapas 4 e 5 só acontecem nas combinações em que o período da cooperativa existe; nas
demais, nada é criado e a permissão auxiliar daquela combinação permanece no cadastro. Cada
período e cada permissão criados deixam na trilha de auditoria a data, a hora, a matrícula,
o terminal, a operação e a imagem do registro gravado.

### RN-14 — Só quem tem a tela liberada e permissão de alteração chega a operar

A operação é feita dentro do tipo de órgão e do código de acesso da sessão. O sistema
confere, no cadastro de acesso, se o perfil da matrícula tem esta tela e, para a alteração,
se o perfil permite alterar. Faltando a tela no perfil, a transação é recusada com
**\* Acesso negado para esta matricula \***; faltando a permissão de alteração, com
**\* Acesso negado para esta operacao \***; e, se a tela não estiver disponível para o
perfil ou para o órgão da sessão, com **\* Tela nao disponivel \***. Em qualquer um dos
casos, nada é lido e nada é gravado.

### RN-15 — Chamada por outra tela na mesma transação, esta não opera

Se a transação chega a esta tela trazendo preenchida a identificação da tela de origem, o
roteamento devolve o controle à tela que a chamou e esta tela encerra sem fazer nenhuma das
conferências de cadastro desta jornada e sem gravar nada.

## Cenários BDD

```gherkin
Funcionalidade: Cadastro das permissões do operador logístico a partir do contrato de cooperativa

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C650T

  Cenário: o caminho feliz do cadastro — RN-02, RN-03, RN-04, RN-06, RN-07, RN-08, RN-09, RN-10, RN-11, RN-12 e RN-13
    Dado que existe o contrato de cooperativa, marcado como cooperativa, com permissões cadastradas e sem permissão auxiliar pendente
    E existe o contrato do operador logístico, marcado como operador logístico, e ainda sem permissão cadastrada
    Quando informo os dois contratos
    Então vejo a descrição dos dois contratos, as coordenações regionais cobertas, as datas do período e a periodicidade do contrato
    E vejo "* Confirma cadastro da permissao <S/N> ? *" com o cursor no campo da resposta
    Quando respondo S
    Então a tela lança a permissão auxiliar do operador logístico para cada permissão da cooperativa
    E apaga o período que já estava registrado para o operador logístico, cria o período dele a partir do da cooperativa e transforma cada permissão auxiliar em permissão
    E vejo "* Cadastro sendo atualizado *"

  Cenário: RN-01 — modo diferente de alteração
    Quando chego à tela em um modo que não é o de alteração
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo do modo
    E nada é lido e nada é gravado

  Cenário: RN-02 — contrato de cooperativa não informado
    Quando confirmo sem informar o contrato de cooperativa
    Então vejo "* Informe o contrato da cooperativa *"
    E o cursor volta ao campo do contrato de cooperativa
    E nada é gravado

  Cenário: RN-03 — contrato de cooperativa não cadastrado
    Dado que o contrato de cooperativa que informei não existe para o órgão da minha sessão
    Quando confirmo
    Então vejo "* Tipo contrato nao cadastrado *"
    E o cursor volta ao campo do contrato de cooperativa
    E nada é gravado

  Cenário: RN-04 — o contrato informado não é de cooperativa
    Dado que o contrato de cooperativa que informei existe, mas não está marcado como cooperativa
    Quando confirmo
    Então vejo "* Tipo contrato nao e de cooperativa *"
    E o cursor volta ao campo do contrato de cooperativa
    E nada é gravado

  Cenário: RN-05 — a cooperativa ainda tem permissão auxiliar pendente
    Dado que o contrato de cooperativa tem permissões cadastradas
    E existe permissão auxiliar lançada para esse contrato
    Quando confirmo
    Então vejo "<- Transferir todos os grupamentos para producao *" com a coordenação regional da permissão auxiliar encontrada
    E nada é gravado

  Cenário: RN-06 — a cooperativa não tem permissão cadastrada
    Dado que o contrato de cooperativa que informei existe, mas não tem nenhuma permissão cadastrada
    Quando confirmo
    Então vejo "<- Nao existem permiss cad. para este contrato *"
    E o cursor volta ao campo do contrato de cooperativa
    E nada é gravado

  Cenário: RN-07 — o que a tela mostra do contrato de cooperativa
    Dado que o contrato de cooperativa tem permissões em coordenações regionais diferentes
    E existe período registrado para elas
    Quando informo o contrato de cooperativa
    Então vejo as coordenações regionais cobertas
    E vejo as datas do período registrado
    E vejo a periodicidade do contrato, normal ou especial

  Cenário: RN-08 — contrato do operador logístico não informado
    Dado que a cooperativa passou pelas conferências
    Quando confirmo sem informar o contrato do operador logístico
    Então vejo "* Informe o contrato do oper.logistico *"
    E o cursor volta ao campo do contrato do operador logístico
    E nada é gravado

  Cenário: RN-09 — contrato do operador logístico não cadastrado
    Dado que o contrato do operador logístico que informei não existe para o órgão da minha sessão
    Quando confirmo
    Então vejo "* Tipo contrato oper.logistico nao cadastrado *"
    E o cursor volta ao campo do contrato do operador logístico
    E nada é gravado

  Cenário: RN-10 — o contrato informado não é de operador logístico
    Dado que o contrato do operador logístico que informei existe, mas não está marcado como operador logístico
    Quando confirmo
    Então vejo "* Tipo contrato nao e de oper.logistico *"
    E o cursor volta ao campo do contrato do operador logístico
    E nada é gravado

  Cenário: RN-11 — o operador logístico já tem permissão cadastrada
    Dado que o contrato do operador logístico que informei já tem permissão cadastrada
    Quando confirmo
    Então vejo "<- Ja existe permiss cad para o oper.logistico *"
    E o cursor volta ao campo do contrato do operador logístico
    E nada é gravado

  Cenário: RN-12 — respondo outra coisa que não S
    Dado que a tela me pediu a confirmação do cadastro
    Quando respondo N
    Então nada é lançado, nada é apagado e nada é criado
    E a tela refaz as conferências dos dois contratos e me pede a confirmação de novo

  Cenário: RN-12 — troco um dos contratos depois da pergunta
    Dado que a tela me pediu a confirmação do cadastro
    Quando troco o contrato do operador logístico
    Então a tela confere tudo de novo, com os contratos novos
    E nada é gravado antes de eu responder S à nova pergunta

  Cenário: RN-13 — o que a confirmação lança, apaga e cria
    Dado que respondi S com os dois contratos conferidos
    Quando a tela percorre as permissões da cooperativa
    Então lança no cadastro de permissões auxiliares a permissão auxiliar do operador logístico para cada permissão da cooperativa
    E apaga o período registrado do operador logístico de cada combinação de coordenação regional, data limite, fornecedor e grupo de licitação
    E cria o período do operador logístico com os mesmos dados do período da cooperativa
    E transforma cada permissão auxiliar em permissão do operador logístico, apaga a permissão auxiliar e registra a auditoria
    E me avisa "* Cadastro sendo atualizado *"

  Cenário: RN-13 — combinação sem período registrado na cooperativa
    Dado que respondi S com os dois contratos conferidos
    E a cooperativa tem permissão em uma combinação sem período registrado
    Quando a tela percorre aquela combinação
    Então não cria o período nem a permissão do operador logístico
    E a permissão auxiliar daquela combinação permanece no cadastro

  Cenário: RN-14 — sem perfil de acesso à tela
    Dado que a minha matrícula não tem perfil de acesso a esta tela
    Quando confirmo
    Então vejo "* Acesso negado para esta matricula *"
    E nada é lido e nada é gravado

  Cenário: RN-14 — sem permissão para alterar
    Dado que o meu perfil de acesso tem esta tela, mas não permite alterar
    Quando confirmo
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-14 — tela indisponível para o meu perfil ou para o meu órgão
    Dado que esta tela não está disponível para o meu perfil ou para o órgão da minha sessão
    Quando confirmo
    Então vejo "* Tela nao disponivel *"
    E nada é lido e nada é gravado

  Cenário: RN-15 — a tela chamada por outra dentro da mesma transação
    Dado que outra tela chama esta dentro da mesma transação
    Quando a transação chega a esta tela
    Então nenhuma das conferências de cadastro desta tela é feita
    E o controle volta para a tela que a chamou
    E nada é gravado
```
