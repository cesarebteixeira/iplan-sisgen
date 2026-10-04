# US — E920T — Manter o contrato de referência e o período de entrega dos cartões

## Estória

Como **servidor da coordenação regional de ensino (CRE)**, quero **registrar o
contrato de referência dos cartões do órgão — com o fornecedor, o período de entrega
e a validade do cartão — e depois consultá-lo, alterá-lo ou excluí-lo**, para que **a
entrega dos cartões de alimentação escolar tenha fornecedor, prazo e validade
declarados, e cada cartão entregue possa ser atribuído ao contrato a que pertence**.

O contrato de referência é o que dá existência ao cartão: é ele que diz de que
fornecedor o cartão é, em que janela de datas ele deve ser entregue e até quando ele
vale. As telas de entrega registram, cartão a cartão, o que foi entregue e o que
ficou pendente contra esse contrato, e é a situação dele — aberto ou fechado para
entrega — que diz se ainda se pode receber cartão por ele. Um contrato cadastrado com
o fornecedor ou o prazo trocados contamina a entrega e a cobrança de todos os cartões
que dependem dele.

## Contexto

Jornada S000M → E000M → E900M → E920T.
Ator: servidor de CRE — define, para o órgão do seu vínculo, o contrato de referência
dos cartões e depois o consulta, altera ou exclui.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O órgão que assina o contrato não é escolhido nesta tela: ele vem do vínculo do
servidor, definido na entrada, e os menus do caminho não o alteram. A operação com que
a tela abre, porém, vem de quem a chamou: pelo menu desta jornada ela abre pronta para
incluir; pela lista de contratos (`E920C`) abre em consulta, já mostrando o contrato
escolhido na lista. Esta tela não passa o contrato para outra: depois de cada envio ela
reabre a si mesma, e o contrato lido fica na sessão. O contrato que ela mantém é o
mesmo que a lista de contratos apresenta e que as telas de entrega usam depois — esta
tela não cadastra aluno nem cartão, ela define o contrato em que os dois entram.

As regras abaixo são só as desta tela.

---

## Regras de negócio

### RN-01 — A tela mantém o contrato de referência dos cartões do órgão

A tela cria, consulta, altera e exclui o **contrato de referência dos cartões** do
órgão do vínculo de quem está usando o sistema. O contrato é do órgão: o órgão não é
escolhido nem alterado aqui. O contrato guarda o fornecedor responsável, o período de
entrega — data inicial e data limite —, o mês e o ano até quando o cartão vale e a
situação do cadastro. Nada de fornecedor, de cartão ou de aluno é criado ou alterado
nesta tela: o que ela grava é o contrato, e é nele que as telas de entrega anotam
depois o que foi entregue.

### RN-02 — A tela abre em inclusão pelo menu e em consulta pela lista de contratos

A operação com que a tela abre é decidida pela tela que a chamou. Vinda do menu desta
jornada, ela abre pronta para **incluir**. Vinda da lista de contratos (`E920C`), abre
em **consulta**, já com o contrato da linha escolhida na lista — o ano, o número, o
fornecedor, o período e a validade do cartão vêm preenchidos. Depois de cada envio a
tela reabre a si mesma e a operação que estiver informada é que decide o que acontece
dali em diante: é assim que uma consulta pode ser seguida de uma alteração ou de uma
exclusão do mesmo contrato.

### RN-03 — O contrato é identificado pelo órgão, pelo ano e por um número que o sistema atribui

O contrato é identificado pelo órgão, por um **ano** e por um **número**. O número não
é digitado: na inclusão a tela toma o próximo da sequência daquele ano para aquele
órgão — o seguinte ao último usado, ou 1 quando é o primeiro contrato do ano — e já o
grava na numeração antes de perguntar qualquer coisa. O ano do contrato é o ano em que
o período de entrega começa. Como o número tem dois dígitos, a sequência do ano
comporta 99 contratos por órgão.

[?] O campo do ano aceita digitação, mas a inclusão grava ali o ano do início do
período e descarta o que foi digitado; na alteração, mudar o ano do início do período
não muda o ano do contrato, e a tela passa a mostrar os dois diferentes. Se os dois
deveriam poder divergir, o campo do ano não tem efeito na inclusão. Pergunta ao site.

[?] A tela não trata o fim da sequência do ano: ao chegar ao 99º contrato do ano, o
número seguinte não cabe nos dois dígitos e o programa não avisa o que fazer. Não se
conclui do fonte o que acontece nesse contrato. Pergunta ao site.

### RN-04 — O mesmo fornecedor não pode ter dois contratos com o mesmo fim de período no órgão

Na inclusão e na alteração, se já existe contrato daquele fornecedor com a mesma data
limite no órgão, a tela recusa, mostra o contrato que já existe — ano e número — e não
segue. O mesmo fornecedor pode ter mais de um contrato no órgão, desde que os períodos
não terminem no mesmo dia.

### RN-05 — O período de entrega: as duas datas são obrigatórias, válidas, e o fim não pode ser anterior ao início

As duas datas do período são obrigatórias. Cada uma tem de ser data de calendário
válida, com o ano entre 1994 e 2099, e a data limite não pode ser anterior à data
inicial. Cada recusa tem a sua mensagem: sem a data inicial, **\* Informe data inicial
do contrato \***; data inicial que não existe no calendário ou com ano fora da faixa,
**\* Periodo inicial invalido \***; sem a data limite, **\* Informe data limite do
contrato \***; data limite inválida, **\* Periodo final invalido \***; e fim anterior
ao início, **\* Data final menor que data inicial \***.

A tela não exige que o período comece no futuro nem o compara com a data de hoje: um
período já vencido é aceito.

### RN-06 — A validade do cartão: o mês e o ano são obrigatórios

A tela pede o mês e o ano até quando o cartão vale e exige os dois: sem o mês,
**\* Informe mes de validade do cartao \***; sem o ano, **\* Informe ano de validade
do cartao \***.

[?] A tela confere apenas que o mês e o ano foram preenchidos como números: não há
faixa de mês nem a faixa de ano que o período tem, de modo que um mês 13 passa e um ano
fora de 1994 a 2099 também. Se a intenção era validar a validade do cartão, é defeito;
não se conclui do fonte. Pergunta ao site.

### RN-07 — O fornecedor precisa existir e não pode estar apagado

O código do fornecedor é obrigatório — sem ele, **\* Informe o fornecedor \*** — e tem
de constar do cadastro de fornecedores; quando não consta, a tela recusa com
**\* Fornecedor nao cadastrado \***. O cadastro é conferido também quando o operador
sai do campo, por uma checagem do próprio campo, que devolve o cursor a ele e recusa o
fornecedor que não existe ou que está apagado. A tela mostra a razão social do
fornecedor informado.

### RN-08 — A inclusão abre o cadastro; a alteração decide entre aberto e fechado

Ao incluir, o contrato é gravado **aberto para entrega de cartões**, qualquer que seja
o valor que esteja no campo da situação. Na alteração, a situação tem de ser **A**,
para abrir, ou **F**, para fechar: outro valor é recusado com **\* Informe A para Abrir
ou F para Fechar Contrato \***. A tela mostra por extenso **Cadastro Aberto para
Entrega de Cartoes** ou **Cadastro Fechado para Entrega de Cartoes**. A alteração não
muda o órgão, o ano nem o número do contrato: ela mexe só nos dados do contrato —
fornecedor, período, validade do cartão e situação.

### RN-09 — A tela pergunta antes de gravar, e o número do contrato já foi reservado

Recebidos os dados, a tela não grava: ela confere e pergunta **Confirma inclusao do
contrato <S/N> ?** — ou **Confirma alteracao do contrato <S/N> ?**, ou **Confirma
exclusao do contrato <S/N> ?** — com o cursor no campo da resposta. Só a resposta **S**
grava. Resposta diferente de S, ou resposta acompanhada de mudança em qualquer dado do
contrato, cancela a operação e nada é gravado. Depois de gravar, a tela não exibe aviso
de sucesso: ela volta mostrando o contrato.

[?] Na inclusão, o número do contrato é tomado da numeração e gravado ali antes de a
tela perguntar. Uma inclusão cancelada consome o número e deixa lacuna na sequência do
ano. Se a intenção era reservar o número só depois do S, a lacuna é defeito. Pergunta
ao site.

### RN-10 — A consulta mostra o contrato e não grava nada

Informando o ano e o número, a tela mostra o contrato do órgão: o fornecedor com a
razão social, o período de entrega, a validade do cartão e a situação do cadastro. Sem
o número, a tela recusa com **\* Informe o numero do contrato \***; não existindo o
contrato, com **\* Contrato nao cadastrado \***. A consulta não grava, não altera e não
exclui: nenhum cadastro de negócio é tocado por ela.

### RN-11 — Alterar e excluir exigem que o contrato já tenha sido lido

A alteração e a exclusão só seguem quando o ano e o número informados são os do
contrato lido por último nesta sessão — lido na consulta desta tela ou trazido da lista
de contratos. Com outro ano ou outro número, a tela recusa com **\* Consulte antes de
atualizar \***: é preciso consultar o contrato antes de mexer nele.

### RN-12 — Não se exclui contrato que já tem cartões

Antes de pedir a confirmação da exclusão, a tela procura os cartões daquele contrato.
Existindo qualquer um, a exclusão é recusada com **\* Ja existem cartoes para este
Contrato \*** e nada é excluído: primeiro se resolvem os cartões, depois o contrato.

[?] A procura dos cartões do contrato é feita com parte da identificação do cartão
zerada — o órgão filho, a matrícula do aluno e o número do cartão. O que a leitura faz
com essa identificação incompleta é do banco, e não está no corpus. Se a leitura exigir
a identificação inteira, nenhum cartão é achado com essas partes zeradas, a recusa fica
inalcançável e a tela apaga um contrato que tem cartões. Pergunta ao site.

### RN-13 — Cada inclusão, alteração e exclusão fica registrada

Toda gravação no contrato deixa um registro de auditoria com o conteúdo anterior, o
conteúdo novo (em branco, no caso da exclusão), a operação, a identificação do
contrato, quem fez, quando e de que terminal. É esse registro que permite reconstruir
quem trocou o fornecedor, o período, a validade do cartão ou a situação de um contrato.

### RN-14 — Código de operação fora dos quatro é recusado

A tela só reconhece quatro operações: incluir, alterar, excluir e consultar. Qualquer
outro código no campo da operação é recusado com **\* Oper. nao disponivel. Use
INC,ALT,EXC ou CON \***, e o cursor volta a esse campo.

## Cenários BDD

```gherkin
Funcionalidade: Manter o contrato de referência e o período de entrega dos cartões

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E920T
    E o órgão do meu vínculo é o órgão do contrato

  Cenário: Abrir a tela pelo menu da jornada
    Dado que escolhi, no menu, a opção que abre a E920T
    Quando a tela aparece
    Então ela abre pronta para incluir um contrato

  Cenário: Abrir a tela pela lista de contratos
    Dado que escolhi um contrato na lista de contratos
    Quando a tela aparece
    Então ela abre em consulta
    E mostra o contrato que escolhi na lista, com o fornecedor e o período

  Cenário: Incluir um contrato e abri-lo para entrega
    Dado que informei um fornecedor que consta do cadastro
    E informei o período de entrega, com a data limite posterior à inicial
    E informei o mês e o ano de validade do cartão
    Quando confirmo a inclusão com S
    Então o contrato fica gravado para o órgão, aberto para entrega de cartões
    E a tela volta mostrando o contrato

  Cenário: A inclusão numera o contrato na sequência do ano
    Dado que já existe contrato naquele ano para o órgão
    Quando incluo o próximo contrato do ano e confirmo com S
    Então o novo contrato recebe o número seguinte ao último usado naquele ano

  Cenário: O primeiro contrato do ano recebe o número 1
    Dado que ainda não existe contrato naquele ano para o órgão
    Quando incluo o primeiro contrato do ano e confirmo com S
    Então o contrato recebe o número 1

  Cenário: A inclusão pergunta antes de gravar
    Dado que informei fornecedor, período e validade do cartão
    Quando envio os dados
    Então a tela me pede a confirmação da inclusão do contrato
    E nada foi gravado ainda

  Cenário: Resposta diferente de S cancela a inclusão
    Dado que a tela me pediu a confirmação da inclusão
    Quando respondo N, ou deixo a resposta em branco
    Então a confirmação é descartada e a tela volta com os dados informados
    E nada foi gravado
    E o número tomado para este contrato não volta para a sequência do ano

  Cenário: Mudar um dado junto com a confirmação cancela a inclusão
    Dado que a tela me pediu a confirmação da inclusão
    Quando altero a data limite e respondo S
    Então a confirmação é cancelada
    E nada foi gravado

  Cenário: Incluir sem o fornecedor
    Dado que deixei o código do fornecedor em branco
    Quando envio os dados
    Então vejo a mensagem "* Informe o fornecedor *"
    E o cursor volta ao campo do fornecedor
    E nada é gravado

  Cenário: Incluir com fornecedor que não consta do cadastro
    Dado que informei um código de fornecedor que não existe
    Quando envio os dados
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E nada é gravado

  Cenário: Incluir sem a data inicial
    Dado que deixei a data inicial em branco
    Quando envio os dados
    Então vejo a mensagem "* Informe data inicial do contrato *"
    E nada é gravado

  Cenário: Incluir com data inicial que não existe no calendário
    Dado que informei uma data inicial inexistente, ou com ano fora de 1994 a 2099
    Quando envio os dados
    Então vejo a mensagem "* Periodo inicial invalido *"
    E nada é gravado

  Cenário: Incluir sem a data limite
    Dado que deixei a data limite em branco
    Quando envio os dados
    Então vejo a mensagem "* Informe data limite do contrato *"
    E nada é gravado

  Cenário: Incluir com data limite que não existe no calendário
    Dado que informei uma data limite inexistente, ou com ano fora de 1994 a 2099
    Quando envio os dados
    Então vejo a mensagem "* Periodo final invalido *"
    E nada é gravado

  Cenário: Incluir com a data limite anterior à inicial
    Dado que informei a data limite antes da data inicial
    Quando envio os dados
    Então vejo a mensagem "* Data final menor que data inicial *"
    E nada é gravado

  Cenário: Incluir sem o mês de validade do cartão
    Dado que deixei o mês de validade do cartão em branco
    Quando envio os dados
    Então vejo a mensagem "* Informe mes de validade do cartao *"
    E nada é gravado

  Cenário: Incluir sem o ano de validade do cartão
    Dado que deixei o ano de validade do cartão em branco
    Quando envio os dados
    Então vejo a mensagem "* Informe ano de validade do cartao *"
    E nada é gravado

  Cenário: Incluir um contrato que já existe para o fornecedor
    Dado que já existe contrato daquele fornecedor com a mesma data limite
    Quando envio os dados do novo contrato
    Então vejo a mensagem "* <- Contrato ja cadastrado *", com o contrato existente
    E nada é gravado

  Cenário: Consultar um contrato do órgão
    Dado que informei o ano e o número de um contrato cadastrado
    Quando envio a consulta
    Então vejo o fornecedor com a razão social, o período, a validade do cartão e a
      situação do cadastro
    E nada foi gravado, alterado ou excluído

  Cenário: Consultar sem informar o número do contrato
    Dado que deixei o número do contrato em branco
    Quando envio a consulta
    Então vejo a mensagem "* Informe o numero do contrato *"
    E nada é mostrado

  Cenário: Consultar um contrato que não existe
    Dado que informei ano e número de um contrato não cadastrado
    Quando envio a consulta
    Então vejo a mensagem "* Contrato nao cadastrado *"
    E nada é mostrado

  Cenário: Alterar um contrato consultado
    Dado que consultei um contrato do órgão
    E alterei o fornecedor, o período e a validade do cartão
    Quando confirmo a alteração com S
    Então o contrato fica gravado com os novos dados
    E o órgão, o ano e o número do contrato não mudam
    E a alteração fica registrada com o conteúdo anterior e o novo

  Cenário: Fechar o contrato para entrega de cartões
    Dado que consultei um contrato aberto
    Quando informo a situação F e confirmo a alteração com S
    Então o contrato fica fechado, mostrado como "Cadastro Fechado para Entrega de
      Cartoes"

  Cenário: Excluir um contrato sem cartões
    Dado que consultei um contrato que não tem cartões
    Quando confirmo a exclusão com S
    Então o contrato é excluído
    E a exclusão fica registrada com o contrato que foi excluído

  Cenário: Alterar um contrato sem consultá-lo antes
    Dado que informei ano e número diferentes do contrato lido por último
    Quando envio a alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E nada é gravado

  Cenário: Alterar com situação diferente de A e F
    Dado que consultei um contrato
    Quando informo uma situação que não é A nem F e envio
    Então vejo a mensagem "* Informe A para Abrir ou F para Fechar Contrato *"
    E nada é gravado

  Cenário: Alterar para um período que já existe para o fornecedor
    Dado que consultei um contrato
    E já existe outro contrato daquele fornecedor com a data limite que informei
    Quando confirmo a alteração com S
    Então vejo a mensagem "* <- Contrato ja cadastrado *", com o contrato existente
    E nada é gravado

  Cenário: Excluir um contrato que já tem cartões
    Dado que consultei um contrato que tem cartões
    Quando envio a exclusão
    Então vejo a mensagem "* Ja existem cartoes para este Contrato *"
    E o contrato não é excluído

  Cenário: A operação fica registrada para auditoria
    Dado que incluí, alterei ou excluí um contrato
    Quando a operação é gravada
    Então fica registrado o conteúdo anterior, o conteúdo novo, a operação, o
      contrato, quem fez, quando e de que terminal

  Cenário: Operação que a tela não reconhece
    Quando informo um código de operação que não é incluir, alterar, excluir nem
      consultar
    Então vejo a mensagem "* Oper. nao disponivel. Use INC,ALT,EXC ou CON *"
    E o cursor volta ao campo da operação
```
