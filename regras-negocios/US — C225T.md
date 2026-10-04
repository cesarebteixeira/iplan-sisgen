# US — C225T — Transferir os órgãos de uma coordenação regional escolar para outra

## Estória

Como **servidor da CRE que responde pela coordenação regional escolar**, quero
**transferir os órgãos do meu grupo para outra coordenação regional, a partir de uma
data de início, trocando também a coordenação e a unidade orçamentária do órgão**, para
que **a rede seja reorganizada sem refazer órgão por órgão, e cada órgão fique apontando
para a coordenação e a unidade orçamentária certas a partir do período informado**.

O vínculo de um órgão com a sua coordenação regional **vale por um período**: quando o
órgão muda de coordenação, o período antigo precisa terminar e um novo precisa começar.
É esse par de períodos que o resto do sistema lê para saber a qual coordenação pertence
o que o órgão consome em cada ano. Sem essa passagem registrada, o órgão continua
apontando para a coordenação antiga — e o consumo, a estimativa e os relatórios do
período saem atribuídos à coordenação errada.

A tela serve para isso mesmo quando a coordenação **não** muda de nome: é por ela que o
órgão do grupo ganha a **unidade orçamentária que o FINCON exige**, dado sem o qual o
órgão não entra nos processos da unidade.

## Contexto

Jornada S000M → C000M → C200M → C225T.

Ator: servidor de CRE — relaciona os órgãos da coordenação em tela e executa a passagem
deles para outra coordenação regional, a partir de uma data.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas do meio do caminho são menus: não deixam nada de próprio para a tela de
destino, apenas dizem qual tela abrir. O que a C225T usa da sessão — o tipo de órgão, a
coordenação regional, o acesso, a matrícula e a estação, mais a descrição da secretaria
e a data do sistema que ela mostra no cabeçalho — foi deixado pela entrada.

A tela não encadeia para nenhuma outra: não passa registro nem operação adiante, e a
jornada termina nela. Ela **reabre a si mesma** na mesma transação, uma vez por linha da
lista, até dez linhas.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O que a tela faz e onde ela grava

A tela transfere os órgãos de uma **coordenação regional escolar** (o grupo) para outra,
a partir de uma **data de início**. Ela tem três dados de cabeçalho — a coordenação de
origem, a coordenação de destino e a unidade orçamentária de destino que o **FINCON**
exige —, a **data de início** em dia, mês e ano, e uma **ação por linha**, que relaciona
ou desrelaciona o órgão.

A tela grava em quatro lugares, sempre com o rastro na trilha de auditoria: o
**histórico de períodos do órgão por coordenação**, o **cadastro do órgão** — a
coordenação e a unidade orçamentária —, a **relação de órgãos a atualizar** e a
auditoria. Nada é apagado do cadastro de órgãos: o que a tela apaga e remonta é a
relação (RN-13).

### RN-02 — A identificação dos campos passa pela conferência numérica

Antes de qualquer consulta, o sistema confere, **um a um**, os campos de código da tela:
a coordenação de origem, a coordenação de destino, o número do órgão, o número da
unidade orçamentária de destino e o dia, o mês e o ano de início — e, em cada uma das
dez linhas, o código do órgão e o código do órgão inicial. Campo em branco vale zero, os
separadores de milhar caem e o campo não numérico é recusado, com o cursor de volta **no
campo que falhou**.

[?] O texto exato da recusa por campo não numérico não está no lote: a conferência é
feita por rotina padrão de edição numérica, e a mensagem que o terminal mostra sai da
rotina de comunicação, fora dos fontes fornecidos. Pergunta ao site.

### RN-03 — A tela só admite alteração ou consulta

O **modo** da tela aceita **alteração** ou **consulta** — os mesmos que a mensagem de
recusa nomeia **ALT** e **CON**. Qualquer outro valor é recusado com
**\* Operacao nao disponivel. Use ALT ou CON \***, com o cursor de volta no campo do
modo, e nada é gravado.

Abrindo a tela sem informar o modo, ela assume **consulta**.

[?] A mensagem manda usar ALT ou CON, mas o teste é feito contra os códigos internos de
alteração e de consulta: se o campo recebe exatamente o que a mensagem manda digitar, a
alteração seria recusada. O lote mostra o teste, não a tradução que a camada de
apresentação faria. Pergunta ao site.

### RN-04 — A alteração confere os dados da última consulta

Na **alteração**, o sistema compara os sete dados que identificam a passagem — a
coordenação de origem, a coordenação de destino, o número do órgão, o número da unidade
orçamentária de destino e o dia, o mês e o ano de início — com os que a **última
consulta** deixou guardados. Diferindo algum deles, a alteração é recusada com
**\* Consulte antes de atualizar \***, com o cursor de volta no campo da coordenação de
origem. É a consulta que prepara os dados; a alteração apenas confirma.

[?] O fonte não deixa claro se essa recusa chega a impedir a gravação: ela não marca o
estado de erro que interrompe a passagem seguinte, e a passagem que grava roda depois,
sem repetir as conferências. Pergunta ao site.

### RN-05 — A coordenação de origem é obrigatória

A **coordenação regional de origem** — o grupo de que os órgãos estão saindo — tem de
estar informada. Em branco, a recusa é **\* Informe o grupo \***, com o cursor de volta
no campo da origem, e nada é gravado.

### RN-06 — A coordenação de destino é obrigatória e tem de ser diferente da de origem

A **coordenação regional de destino** também tem de estar informada, com a mesma recusa
**\* Informe o grupo \***, com o cursor de volta no campo do destino.

Origem e destino **não podem ser a mesma coordenação**: iguais, a recusa é
**\* Informe grupo diferente para atualizacao \***, com o cursor no campo do destino, e
nada é gravado.

### RN-07 — A coordenação de destino tem de estar cadastrada

Informada a coordenação de destino, o sistema procura o grupo no cadastro das
coordenações regionais do **tipo de órgão da sessão**. Não achando, a recusa é
**\* Grupo nao cadastrado \***, com o cursor de volta no campo do destino, e nada é
gravado.

[?] O cadastro da coordenação regional guarda uma unidade orçamentária própria, que esta
tela **não** usa: a unidade gravada é a que o servidor digita. Se a unidade deveria vir
da coordenação de destino, é pergunta ao site.

### RN-08 — A coordenação de origem precisa ter pelo menos um órgão ativo

Antes de gravar, o sistema percorre o cadastro de órgãos do grupo de origem. Se **nenhum**
órgão ativo for encontrado, a recusa é
**\* Nao existem Orgaos ativos para este grupo \***, com o cursor no campo da origem, e
nada é gravado.

### RN-09 — A unidade orçamentária de destino no FINCON é obrigatória

A **unidade orçamentária de destino, no FINCON**, tem de vir informada. Em branco, a
recusa é **\* Informe unidade orcamentaria no FINCON \***, com o cursor de volta no
campo, e nada é gravado.

### RN-10 — A data de início tem de ser uma data real, entre 1994 e 2099

A **data de início** é conferida antes de qualquer gravação. Não sendo uma data de
calendário — dia ou mês em branco, mês fora de 1 a 12, dia fora do mês, ano fora da
faixa de **1994 a 2099** —, a recusa é **\* Data de inicio invalida \***, com o cursor
de volta no dia do início, e nada é gravado.

[?] O dia e o mês são conferidos como data, mas não têm mensagem própria de campo: em
branco, eles viram zero e a recusa que aparece é a de data inválida. O texto de uma
recusa específica de dia ou de mês, se existir, não está no lote. Pergunta ao site.

### RN-11 — A lista mostra os órgãos ativos do grupo, dez por linha

Ao entrar, a tela mostra os órgãos **ativos** do grupo de origem, até **dez linhas**;
cada linha traz o **código do órgão**, o **nome**, a **ação** e a indicação de
relacionado, que aparece como **Sim**. Os órgãos **inativos são pulados**, e as linhas
já relacionadas aparecem com a ação marcada.

Não havendo **nenhum** órgão na lista, a tela avisa
**\* Nao existem orgaos cadastrados \***, com o cursor no campo da origem, e a lista sai
em branco. A lista é remontada a cada passagem, continuando do último órgão mostrado.

[?] Essa mensagem também é apresentada quando a leitura não devolve nada, e não só
quando o grupo não tem órgão: o fonte não distingue as duas situações. Pergunta ao site.

### RN-12 — Só a linha já consultada é operada, e a linha relacionada exige código e nome

A alteração percorre a lista **linha a linha** e só opera a linha que já tenha sido
**consultada** — isto é, cujo órgão já esteja marcado como existente no cadastro de
órgãos do grupo. A linha que aponta para um órgão que não está mais lá é **ignorada em
silêncio**: não é relacionada nem desrelacionada, e nada é gravado para ela.

Numa linha **relacionada**, dois dados são exigidos: o **código do órgão**, que não pode
estar zerado — senão a recusa é **\* Atualize linha preenchida \*** —, e o **nome do
órgão**, que não pode estar em branco — senão a recusa é **\* Informe nome do orgao \***.
Nas duas, o cursor vai para a **ação da linha**, e nada é gravado para ela.

### RN-13 — A ação da linha relaciona ou desrelaciona o órgão

Cada uma das dez linhas tem uma **ação**. Numa passagem de alteração, marcar a ação põe
o órgão na **relação** da transferência — e essa inclusão fica registrada na auditoria;
deixar a ação em branco retira o órgão da relação — e a retirada também fica registrada.
A relação é o que a passagem seguinte executa.

[?] O texto que a máscara dá à ação não está no lote: o extrator do grafo a registra
como **S** e como **Sim**, mas o fonte só mostra que a linha é relacionada ou não.
Pergunta ao site.

### RN-14 — Confirmada a atualização, a tela percorre a relação e transfere cada órgão

Com a confirmação marcada, o sistema percorre a **relação de órgãos a atualizar** e, para
cada órgão:

- procura o órgão no cadastro **dentro do grupo de origem**. Não achando, o órgão apenas
  sai da relação, sem transferência;
- **encerra o período na coordenação de origem**: o período daquele órgão naquela
  coordenação passa a ter como limite o **ano informado**, e o dia e o mês informados
  entram como dia e mês **limite**;
- **abre o período na coordenação de destino**: o período começa no **ano do sistema**,
  vai até o ano **9999**, com mês e dia limite **99** — isto é, fica **em vigor, sem data
  limite** —, com a **marca de creche**, a **marca de pedido acumulado** e o **número da
  unidade orçamentária de destino** vindos do cadastro do órgão;
- **grava o cadastro do órgão**, que passa a apontar para a **coordenação de destino** e
  para a **unidade orçamentária de destino**;
- remove o órgão da relação e segue para o próximo.

[?] A abertura do período novo e a mudança do cadastro do órgão estão sob uma condição
de estado da gravação anterior que **nenhum ponto dos fontes desta jornada produz**. Se
ela não passar, o período antigo é encerrado, o órgão sai da relação e a tela ainda
avisa **Cadastro Atualizado** — sem abrir o período novo e sem mudar a coordenação do
órgão. Pergunta ao site.

[?] O **dia e o mês de início** informados entram como limite do período antigo, e o ano
informado é o limite daquele período; o período do destino começa no ano do **sistema**,
não no ano informado. A leitura do fonte não permite dizer se o ano gravado deveria ser
o ano informado. Pergunta ao site.

### RN-15 — A consulta não grava nada

No modo **consulta**, a passagem que grava é abandonada antes de qualquer rotina de
escrita, e a passagem de conferência sai antes das peneiras da linha: nenhum período é
encerrado ou aberto, nenhum órgão muda de coordenação, nenhuma relação é incluída ou
retirada, o cadastro do órgão não é tocado e nada vai para a auditoria. A consulta serve
para conferir os dados e prepará-los para a alteração (RN-04).

### RN-16 — Ao concluir, a tela avisa * Cadastro Atualizado *

Terminada a passagem pela relação, a tela apresenta **Cadastro Atualizado** no lugar da
mensagem da tela.

[?] A mensagem é apresentada ao fim do laço que percorre a relação, mesmo quando nenhuma
linha foi operada. Pergunta ao site.

### RN-17 — Toda gravação deixa rastro na auditoria

Cada gravação deixa um registro na trilha de auditoria com a **tela de origem**, a
**operação**, o **valor anterior** e o **posterior** e o contexto da sessão —
coordenação regional, tipo de órgão, estação, matrícula, data e hora da sessão e número
do processo. Na inclusão o valor anterior vai vazio; na exclusão, o posterior. A
auditoria cobre a inclusão, a alteração e a retirada do órgão na relação, os dois
períodos gravados e a mudança do cadastro do órgão.

### RN-18 — Nada é lido nem gravado sem a autorização da sessão

A tela passa pelas conferências da jornada antes de mostrar ou gravar qualquer coisa: a
sessão precisa ser válida e reconhecida, a tela precisa estar na relação de telas do
sistema e liberada para o acesso do servidor, e a **operação** pretendida precisa estar
liberada no cadastro de autorizações do código de acesso. A conferência recebe a
coordenação regional, o tipo de órgão, o acesso, a matrícula, a estação e o modo
informado. Não passando, a tela volta sem validar nem gravar nada.

[?] A rotina de autorização é comum à jornada e não está entre os fontes desta tela: o
que exatamente ela exige é regra da entrada, e está registrada no anexo, em **Regras que
se revelaram da entrada**. Pergunta ao site.

### RN-19 — Chegando com a tela de retorno preenchida, a transferência é abandonada

Se a transação chegar com a indicação de **tela de retorno** preenchida — o dado que a
rota usa para devolver o servidor a outra tela —, a manutenção é abandonada: nada é
validado, nada é gravado e o servidor é levado à tela indicada.

[?] Nada nesta jornada preenche essa indicação, e o lote não diz quem a preenche nem
para onde ela levaria. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Transferir os órgãos de uma coordenação regional escolar para outra

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenação regional e o acesso
    E tenho acesso à tela C225T

  Cenário: Os campos de código passam pela conferência numérica
    Dado que estou na tela C225T
    Quando informo, em qualquer campo de código, algo que não é número
    Então o sistema recusa e o cursor volta ao campo que falhou
    E nada é gravado

  Cenário: O modo só admite alteração ou consulta
    Dado que estou na tela C225T
    Quando informo um modo diferente de alteração e de consulta
    Então vejo "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: A alteração confere os dados da última consulta
    Dado que estou na tela C225T e consultei o grupo
    Quando submeto a alteração com um dado diferente do que foi consultado
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo da coordenação de origem

  Cenário: A coordenação de origem é obrigatória
    Dado que estou na tela C225T
    Quando tento transferir sem informar a coordenação regional de origem
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo da coordenação de origem
    E nada é gravado

  Cenário: A coordenação de destino é obrigatória
    Dado que estou na tela C225T
    Quando tento transferir sem informar a coordenação regional de destino
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo da coordenação de destino
    E nada é gravado

  Cenário: A coordenação de destino tem de ser diferente da de origem
    Dado que estou na tela C225T
    Quando informo como destino a mesma coordenação regional da origem
    Então vejo "* Informe grupo diferente para atualizacao *"
    E o cursor fica no campo da coordenação de destino
    E nada é transferido

  Cenário: A coordenação de destino tem de estar cadastrada
    Dado que estou na tela C225T
    E que a coordenação regional de destino informada não existe
    Quando tento transferir
    Então vejo "* Grupo nao cadastrado *"
    E o cursor fica no campo da coordenação de destino
    E nada é transferido

  Cenário: A coordenação de origem sem órgão ativo não deixa transferir
    Dado que estou na tela C225T
    E que a coordenação regional de origem não tem nenhum órgão ativo
    Quando tento transferir
    Então vejo "* Nao existem Orgaos ativos para este grupo *"
    E o cursor fica no campo da coordenação de origem
    E nada é transferido

  Cenário: A unidade orçamentária de destino no FINCON é obrigatória
    Dado que estou na tela C225T
    Quando tento transferir sem informar a unidade orçamentária de destino
    Então vejo "* Informe unidade orcamentaria no FINCON *"
    E o cursor fica no campo da unidade
    E nada é transferido

  Cenário: A data de início tem de ser válida
    Dado que estou na tela C225T
    Quando informo uma data que não existe no calendário, ou um ano fora de 1994 a 2099
    Então vejo "* Data de inicio invalida *"
    E o cursor fica no dia do início
    E nada é gravado

  Cenário: A lista mostra os órgãos ativos do grupo, dez por linha
    Dado que estou na tela C225T em consulta
    E que a coordenação regional de origem tem órgãos cadastrados e ativos
    Quando a tela é apresentada
    Então vejo até dez linhas, cada uma com o código, o nome e a ação
    E os órgãos ativos vêm preenchidos pelo sistema
    E os órgãos inativos não aparecem
    E os órgãos já relacionados aparecem com a ação marcada e com a indicação "Sim"

  Cenário: Não havendo órgão na lista, a tela avisa
    Dado que estou na tela C225T
    E que a coordenação regional de origem não tem nenhum órgão ativo
    Quando a lista é montada
    Então vejo "* Nao existem orgaos cadastrados *"
    E o cursor fica no campo da coordenação de origem
    E a lista sai em branco

  Cenário: Linha de órgão que não está mais no grupo é ignorada
    Dado que estou na tela C225T em alteração
    E que a linha aponta para um órgão que não está mais no cadastro do grupo
    Quando confirmo a linha
    Então o órgão não é transferido, nem relacionado, nem desrelacionado
    E nada é gravado para essa linha

  Cenário: Linha relacionada sem o código do órgão
    Dado que estou na tela C225T em alteração
    Quando relaciono uma linha com o código do órgão zerado
    Então vejo "* Atualize linha preenchida *"
    E o cursor fica na ação da linha
    E nada é gravado

  Cenário: Linha relacionada sem o nome do órgão
    Dado que estou na tela C225T em alteração
    Quando relaciono uma linha com o nome do órgão em branco
    Então vejo "* Informe nome do orgao *"
    E o cursor fica na ação da linha
    E nada é gravado

  Cenário: Relacionar um órgão para a transferência
    Dado que estou na tela C225T em alteração
    E que a linha aponta para um órgão ativo do grupo de origem
    Quando marco a ação da linha
    Então o órgão passa a fazer parte da relação da transferência
    E a inclusão fica registrada na auditoria

  Cenário: Desfazer a relação de um órgão
    Dado que estou na tela C225T em alteração
    E que o órgão já está relacionado para a transferência
    Quando deixo a ação da linha em branco
    Então o órgão sai da relação
    E a retirada fica registrada na auditoria

  Cenário: A transferência dos órgãos relacionados
    Dado que estou na tela C225T em alteração
    E que relates os órgãos que devem passar
    Quando confirmo a transferência
    Então o período de cada órgão na coordenação de origem é encerrado com o limite no ano informado
    E o período de cada órgão na coordenação de destino é aberto, em vigor e sem data limite
    E com a marca de creche, a marca de pedido acumulado e a unidade orçamentária de destino
    E o cadastro de cada órgão passa a apontar a coordenação e a unidade orçamentária de destino
    E cada órgão sai da relação
    E cada gravação fica registrada na auditoria
    E vejo "Cadastro Atualizado"

  Cenário: A consulta não grava nada
    Dado que estou na tela C225T em consulta
    Quando percorro e confirmo as linhas da lista
    Então nenhum período é encerrado ou aberto
    E nenhum órgão muda de coordenação
    E nenhuma relação é incluída ou retirada
    E o cadastro do órgão não é tocado
    E nada vai para a auditoria

  Cenário: A tela de retorno preenchida abandona a transferência
    Dado que a transação chega à C225T com a indicação de tela de retorno preenchida
    Quando a manutenção começaria
    Então o processamento é abandonado e nada é gravado
    E o servidor é levado à tela indicada

  Cenário: Sem autorização a transferência não passa
    Dado que estou na tela C225T em alteração
    E que a minha autorização não cobre a operação pedida
    Quando confirmo a transferência
    Então a linha não é validada e nada é gravado
    E a tela volta
```
