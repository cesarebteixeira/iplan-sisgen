# US — C020T — Manter o cadastro do órgão filho (SDI) da coordenadoria regional escolar

## Estória

Como **servidor da CRE que responde pelo cadastro das unidades da sua coordenadoria**, quero
**consultar, corrigir e desativar o cadastro do órgão filho (SDI) — identificação, endereço,
contato, classificação e quantidades —**, para que **cada unidade da rede fique com o endereço,
o contato, o segmento de atendimento, a marca de creche, o tipo de apoio e as quantidades de
matriculados e de comensais certos**.

O órgão filho é a unidade da rede dentro da coordenadoria regional escolar: é o cadastro dela
que guarda o endereço e os contatos, a que segmento de atendimento ela pertence, se é creche,
que tipo de apoio recebe e quantas pessoas atende. É por unidade que o mapa de atendimento é
aberto e conferido, e é o nome da unidade que fica gravado como origem dos servidores ligados
a ela. Cadastro incompleto, ou unidade desativada por engano, aparece depois no mapa e nos
vínculos da unidade — e não há outra tela desta jornada que corrija isso.

## Contexto

Jornada S000M → C000M → C200M → C020T.

Ator: servidor de CRE — consulta e mantém o cadastro das unidades (órgãos filhos SDI) da sua
secretaria e do seu grupo.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os dois menus do caminho não gravam nada: só encaminham.

O que esta tela usa do que veio antes é o **tipo de órgão (a secretaria)** e a **coordenação
regional escolar (o grupo)** da sessão, além da matrícula e do código de acesso; essa é regra
da entrada e está no anexo de evidências, em **Regras que se revelaram da entrada**. O
**órgão filho do servidor**, que a entrada também carrega, **não** limita esta tela: aqui o
alcance é a secretaria e o grupo.

Esta tela é alcançada de mais de uma origem, e não é a mesma coisa chegar pelo menu ou chegar
encadeada de outra tela: **o modo como ela abre é decidido por quem a chamou** (RN-02), e uma
tela que abre em consulta onde deveria abrir em alteração não falha — só não deixa gravar. Ela
também encadeia em outra tela e reabre a si mesma (RN-03).

## Regras de negócio

### RN-01 — A tela mantém o cadastro do órgão filho, e é a única da jornada que o grava

O cadastro do órgão filho (SDI) reúne quatro blocos. A **identificação**: a coordenação
regional escolar (o grupo), o órgão filho, o código do órgão, o órgão pai e a unidade
orçamentária. O **endereço e os contatos**: endereço, complemento, número do imóvel, extensão,
código do bairro, CEP, nome da pessoa de contato, dois telefones e ramal. A **classificação**:
segmento de atendimento, tipo de apoio, se é creche e se é órgão para pedido acumulado. As
**quantidades e a situação**: matriculados (capacidade), comensais (refeições servidas) e a
marca de ativo.

Das telas desta jornada é a **única que grava esse cadastro**; a entrada e os menus só deixam
contexto. Ela altera, exclui e consulta — incluir não é operação dela (RN-05).

### RN-02 — Como a tela abre depende de quem a chamou

A tela abre sempre em **consulta** e, quando chega pelo menu de órgãos, chega **em branco**: o
menu não passa registro nenhum. Mas há dois caminhos em que ela é chamada encadeada, sem passar
por menu, e em cada um o comportamento é outro:

- vinda da **inclusão de órgão** (`C019T`), logo depois de a unidade ter sido criada, ela abre
  em **alteração**, já com o registro criado carregado — é por esse caminho que a inclusão se
  completa, porque incluir não é operação desta tela (RN-05);
- vinda da **lista de órgãos do grupo** (`C020C`), ela abre em **consulta** sobre o órgão
  escolhido naquela lista.

Quem decide é a tela de origem que ficou guardada na área de trabalho da sessão: só essas duas
origens têm tratamento; qualquer outra cai no caso do menu. Isso não aparece em campo nenhum
da tela nova — é a regra mais fácil de se perder.

### RN-03 — O que a tela entrega à lista de órgãos do grupo, e como ela volta

Marcado o indicador de consulta de grupo, a tela não segue com a operação: ela entrega à **lista
de órgãos do grupo** (`C020C`) a **coordenação regional escolar informada** e **nenhum órgão
filho**, para que a lista abra as unidades daquele grupo. Do outro lado, escolhida uma unidade
na lista, o retorno é para esta tela, em **consulta**, sobre o órgão escolhido. Terminada uma
consulta bem-sucedida, a tela reabre a si mesma com o registro carregado.

[?] O campo desse indicador é exibido e lido — qualquer valor diferente de branco e de "N"
dispara a ida para a lista —, mas nunca é gravado no cadastro e o corpus não traz o rótulo que
o servidor vê nem o valor que ele digita. Pergunta ao site.

### RN-04 — Os campos numéricos são conferidos antes de qualquer regra

A coordenação regional escolar, o órgão filho, o código do órgão, o órgão pai, o número do
imóvel, o código do bairro, o CEP, os dois telefones, o ramal, o segmento de atendimento, o
tipo de apoio, a unidade orçamentária, os matriculados e os comensais passam por uma edição
numérica **antes** de qualquer consulta ou conferência de negócio: o que não for número é
recusado no próprio campo, e nada é consultado por causa dele.

### RN-05 — Só alterar, excluir e consultar; incluir não se faz por aqui

A operação é informada no campo de manutenção. **Incluir** é recusado com
**\* Opcao nao disponivel. Use ALT, EXC ou CON \***, com o cursor de volta no campo. As
operações de navegação da lista de valores (recuperar, voltar, primeiro, último, próximo) são
recusadas com a mensagem de que aquela operação não está disponível neste formato. Sobram
**alterar**, **excluir** e **consultar**, e cada uma delas ainda depende da permissão que o
servidor tem para aquela operação naquela tela: sem a permissão, a tela não opera e nada é
gravado.

A inclusão da unidade não se faz por aqui: quem cria o registro é a tela de inclusão de órgão,
que já chama a gravação do cadastro; esta tela entra depois, em alteração, para completar os
dados (RN-02). Existe no programa um caminho interno que troca a operação para inclusão quando
o registro que está sendo alterado ainda não tem tipo de órgão (RN-07) — é a única inclusão que
esta tela executa.

[?] A tela recusa a inclusão, mas não recusa a **purga** (a operação que apaga o registro de
vez): o código interno da purga não está na lista de operações recusadas, a conferência de
permissão por operação não o contempla, ele não passa por nenhuma conferência de secretaria nem
de grupo e o ramo que grava, para ele, **apaga** o registro. Ou falta recusá-lo, ou falta
conferir o escopo nesse caminho. Pergunta ao site.

### RN-06 — A consulta não grava nada

Em consulta a tela apenas mostra: lê o cadastro do órgão, o nome do bairro, a descrição do
segmento de atendimento e a do tipo de apoio, exibe tudo e reabre a si mesma com o registro
carregado. Nenhum cadastro é gravado, nenhum registro é travado e nenhuma linha vai para a
trilha de auditoria. A própria rotina que grava recusa a operação de consulta.

[?] A recusa da gravação em consulta usa uma mensagem da tabela do sistema cujo texto no corpus
está em inglês ("not available with this format"); como a tabela é recarregada por idioma em
tempo de execução, não afirmo o texto que o servidor lê. A mesma guarda existe nas outras telas
deste formato. Pergunta ao site.

### RN-07 — O órgão é da secretaria da sessão; sem tipo de órgão, o sistema manda atualizá-lo

O órgão procurado tem de ser da **secretaria da sessão**. Sendo de outra, a recusa é
**\* Orgao cadastrado em outra secretaria \***. Há um caso à parte: quando o registro está
cadastrado **sem tipo de órgão** (sem secretaria), a **alteração** o aceita e o recria com a
secretaria da sessão, enquanto a **consulta** e a **exclusão** recusam com
**\* Os dados deste orgao devem ser atualizados \***.

[?] Um cadastro sem secretaria é apagado e recriado com a secretaria da sessão na alteração, e
recusado na consulta e na exclusão. Ou ele é um cadastro em construção (e a recusa da consulta
é proposital), ou é um cadastro inválido que a alteração não deveria recriar. Pergunta ao site.

### RN-08 — O grupo: o do servidor manda, e o grupo do órgão não se troca nesta tela

Quando o servidor tem coordenação regional escolar na sessão, o órgão alcançado tem de ser do
**grupo dele** — senão **\* Usuario sem acesso ao grupo deste orgao \*** — e o grupo informado
na tela tem de ser o dele — senão **\* Usuario sem acesso a outro grupo \***. Quando o servidor
não tem grupo, o grupo informado passa a ser obrigatório (**\* Informe o grupo \***) e tem de
estar cadastrado para a secretaria da sessão (**\* Grupo nao cadastrado \***).

Em qualquer dos casos, o grupo informado tem de ser o que o órgão **já tem gravado** (ou o
órgão ainda não ter grupo): trocar o grupo do órgão por esta tela é recusado com
**\* Nao altere o grupo do orgao nesta tela \***. Na **exclusão** valem as mesmas conferências
de escopo, menos a obrigatoriedade do grupo: quem não tem grupo não precisa informá-lo para
excluir.

### RN-09 — O órgão filho é obrigatório e tem de estar cadastrado

Na alteração e na exclusão, o órgão filho tem de ser informado —
**\*Informe o codigo do orgao \*** — e tem de existir no cadastro, nas três operações, com a
recusa **\* Orgao nao cadastrado \***.

### RN-10 — Nome, endereço, bairro e contato são obrigatórios, e o bairro tem de estar cadastrado

Na alteração, nesta ordem: o **nome do órgão** (**\* Informe o nome do orgao \***), o
**endereço** (**\* Informe o endereco do orgao \***), o **código do bairro**
(**\* Informe o codigo do bairro do orgao \***), o bairro tem de estar cadastrado
(**\* Bairro nao cadastrado \***) e o **nome da pessoa de contato**
(**\* Informe o nome da pessoa para contato \***) — que pode ser de outra pessoa, não
necessariamente do servidor que digita.

### RN-11 — Segmento de atendimento e tipo de apoio, se informados, têm de existir na secretaria

O segmento de atendimento e o tipo de apoio são opcionais no cadastro. Informado o segmento, ele
tem de estar cadastrado para o **tipo de órgão da sessão** (**\* Segmento nao cadastrado \***);
informado o tipo de apoio, idem (**\* Tipo apoio nao cadastrado \***). Em branco, os dois não
são conferidos. A descrição do segmento e a do tipo de apoio são mostradas ao lado do código.

### RN-12 — Creche, ativo e pedido acumulado só valem S ou N

Os três indicadores do cadastro — se a unidade é **creche**, se está **ativo** e se é **órgão
para pedido acumulado** — só aceitam **S** ou **N**. Qualquer outro valor é recusado, cada um
com a sua mensagem: **\* Informe se creche ou nao com S ou N \***, **\* Informe se ativo ou nao
com S ou N \*** e **\* Inf. se Orgao para pedido acumulado com S ou N \***.

### RN-13 — A unidade orçamentária do órgão tem de ser a do grupo

A unidade orçamentária é obrigatória (**\* Informe a unidade orcamentaria \***) e tem de ser
exatamente a que o **grupo** tem cadastrada: sendo outra, a recusa é
**<- Unidade orcamentaria do Grupo \***, e nada é gravado.

### RN-14 — Matriculados e comensais são obrigatórios, e os comensais não passam os matriculados

As duas quantidades são obrigatórias: **\* Informe numero de matriculados / capacidade \*** e
**\* Inf. numero de comensais / refeicoes servidas \***. Além disso, os comensais não podem ser
maiores que os matriculados: **\* Numero de comensais > numero de matriculados \***.

[?] Essa comparação só roda quando o registro ainda não tem tipo de órgão (RN-07): para a
unidade normal, com secretaria, os comensais podem passar os matriculados sem recusa. Ou a
conferência deveria valer para todos, ou ela existe só para o cadastro em construção. Pergunta
ao site.

### RN-15 — Trocar o nome do órgão mantém o índice de nomes e a origem dos servidores

O nome da unidade não é texto solto: ele é o que identifica a unidade no **índice de nomes**
(que não admite nomes repetidos) e é o que está gravado como **origem** de cada servidor daquela
unidade. Alterado o nome, a tela tira o nome antigo do índice, inclui o novo e reescreve a
origem de todos os servidores que estavam ligados ao nome antigo — cada uma dessas mudanças com
o seu registro próprio na trilha de auditoria.

[?] O corpus não define, em negócio, o que é a "origem" do servidor nem por que o nome da
unidade funciona como índice de nomes do sistema; a leitura feita aqui é a do efeito — nome
repetido é barrado pela chave sem duplicatas do índice. Pergunta ao site.

### RN-16 — Desativar o órgão fecha o mapa de atendimento dele

Quando a alteração deixa a unidade **inativa**, a tela percorre os mapas de atendimento daquela
unidade e do seu grupo e **fecha** todos os que estiverem abertos — o mapa diário e o perfil do
mês de referência. É o que impede que uma unidade desativada continue recebendo lançamento.

### RN-17 — Excluir não apaga o órgão: marca-o como inativo e excluído

Excluir não remove o registro: a tela marca a unidade como **inativa**, grava a marca de
exclusão no próprio registro, **fecha os mapas** como em RN-16 e deixa a exclusão na trilha de
auditoria. O registro continua na base, fora do alcance das consultas.

### RN-18 — Toda gravação deixa rastro na auditoria

Cada alteração e cada exclusão do cadastro — e também cada mudança que elas provocam no índice
de nomes e na origem dos servidores — monta uma linha na trilha de auditoria (`A010T`) com a
origem da mudança, a operação, a matrícula, a estação, a data e a hora, os valores de antes e os
de depois, antes de a mudança ser gravada.

### RN-19 — Antes de gravar, a tela confere a chave do registro e o tipo de órgão da sessão

Antes de concluir a gravação, o sistema relê o registro pela chave do cadastro (tipo de órgão +
órgão filho + código do órgão) e confere que ele existe para alterar e excluir, e que ele **não**
existe para incluir; e confere que o **tipo de órgão da sessão** está cadastrado e não está
marcado como excluído. Quando a leitura não fecha, a operação é recusada e nada é gravado.

[?] A releitura do registro, no momento de gravar, usa o **código do órgão digitado na tela**
como parte da chave, mas nenhuma mensagem desta tela exige esse código na alteração nem na
exclusão — a única mensagem que o requer é a da inclusão, que é recusada antes (RN-05). Se ele
vier em branco, a releitura não acha o registro. Pergunta ao site.

### RN-20 — Falha do banco interrompe a operação e avisa

Toda leitura e toda gravação testam o erro do banco. Erro de leitura e erro de exclusão viram a
ação de erro de acesso, e erro de gravação vira a ação de erro de gravação; nas duas a operação
para ali, sem completar o resto, com a mensagem de erro do sistema.

### RN-21 — A tela enxerga doze cadastros e grava em seis

A tela enxerga doze cadastros: além do cadastro do órgão filho, o do tipo de órgão, o do bairro,
o do segmento de atendimento, o do tipo de apoio, o do grupo, o do título das telas, o cadastro
do servidor, o índice de nomes, a auditoria e os dois mapas de atendimento. Grava em seis deles: o
**cadastro do órgão filho**, o **índice de nomes**, o **cadastro do servidor** (só a origem),
os **dois mapas** (só o fechamento) e a **auditoria**. O tipo de órgão, o bairro, o segmento, o
tipo de apoio, o grupo e o título são apenas lidos.

## Cenários BDD

```gherkin
Funcionalidade: Manter o cadastro do órgão filho (SDI) da coordenadoria regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C020T

  Cenário: RN-02 — abrir pelo menu de órgãos
    Dado que chego a esta tela pela opção do menu de órgãos
    Então ela abre em consulta
    E o formulário vem em branco

  Cenário: RN-02 — abrir encadeada da inclusão de órgão
    Dado que a unidade acaba de ser incluída pela tela de inclusão de órgão
    Quando sou levado a esta tela
    Então ela abre em alteração
    E o registro recém-criado já está carregado

  Cenário: RN-02 — abrir encadeada da lista de órgãos do grupo
    Dado que escolhi uma unidade na lista de órgãos do grupo
    Quando sou levado a esta tela
    Então ela abre em consulta sobre a unidade escolhida

  Cenário: RN-04 — campo numérico com texto
    Quando informo texto em um campo numérico
    Então o campo é recusado antes de qualquer consulta ao cadastro
    E permaneço na tela

  Cenário: RN-05 — operação de inclusão informada
    Quando informo a operação de inclusão
    Então vejo "* Opcao nao disponivel. Use ALT, EXC ou CON *"
    E o cursor volta para o campo da operação

  Cenário: RN-05 — operação de navegação informada
    Quando informo uma operação de navegação da lista de valores
    Então vejo a mensagem de que a operação não está disponível neste formato
    E nada é gravado

  Cenário: RN-05 — sem permissão para a operação
    Dado que não tenho permissão para esta operação nesta tela
    Quando confirmo
    Então a tela não opera
    E nada é gravado

  Cenário: RN-01 e RN-06 — consultar uma unidade
    Dado que estou na tela em consulta
    E informo um órgão filho do meu escopo
    Quando confirmo a consulta
    Então vejo a identificação, o endereço, os contatos, a classificação e as quantidades da unidade
    E o nome do bairro, a descrição do segmento e a do tipo de apoio aparecem ao lado dos códigos
    E nada é gravado

  Cenário: RN-06 — consultar não deixa rastro
    Dado que consulto uma unidade
    Quando a consulta termina
    Então nenhum registro é travado
    E nenhuma linha nova aparece na trilha de auditoria

  Cenário: RN-03 — marcar o indicador e abrir a lista do grupo
    Dado que informo a coordenação regional escolar do grupo
    E marco o indicador de consulta de grupo
    Quando confirmo
    Então a lista de órgãos do grupo se abre com as unidades daquele grupo

  Cenário: RN-03 — escolher a unidade na lista e voltar
    Dado que estou na lista de órgãos do grupo
    Quando escolho uma unidade da lista
    Então volto a esta tela em consulta
    E o registro escolhido aparece carregado

  Cenário: RN-09 — órgão filho em branco na alteração
    Dado que estou em alteração
    Quando confirmo sem informar o órgão filho
    Então vejo "*Informe o codigo do orgao *"
    E nada é gravado

  Cenário: RN-09 — órgão filho não cadastrado
    Dado que estou em alteração, em exclusão ou em consulta
    Quando informo um órgão filho que não existe no cadastro
    Então vejo "* Orgao nao cadastrado *"
    E nada é gravado

  Cenário: RN-07 — órgão de outra secretaria
    Quando informo um órgão filho cadastrado em outra secretaria
    Então vejo "* Orgao cadastrado em outra secretaria *"
    E nada é gravado

  Cenário: RN-07 — órgão cadastrado sem secretaria
    Dado que o órgão existe no cadastro sem tipo de órgão
    Quando o consulto ou o excluo
    Então vejo "* Os dados deste orgao devem ser atualizados *"
    E nada é gravado

  Cenário: RN-07 — alterar uma unidade cadastrada sem secretaria
    Dado que o órgão existe no cadastro sem tipo de órgão
    E completo os dados obrigatórios
    Quando confirmo a alteração
    Então o registro é recriado com a secretaria da sessão
    E a operação fica registrada na trilha de auditoria

  Cenário: RN-08 — órgão de outro grupo
    Dado que tenho coordenação regional escolar na sessão
    Quando informo um órgão filho de outra coordenação
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E nada é gravado

  Cenário: RN-08 — grupo informado diferente do meu
    Dado que tenho coordenação regional escolar na sessão
    Quando informo uma coordenação que não é a minha
    Então vejo "* Usuario sem acesso a outro grupo *"
    E nada é gravado

  Cenário: RN-08 — grupo não informado por quem não tem grupo
    Dado que o meu usuário não tem coordenação regional escolar
    Quando confirmo a alteração sem informar o grupo
    Então vejo "* Informe o grupo *"
    E nada é gravado

  Cenário: RN-08 — tentar trocar o grupo do órgão
    Dado que o órgão já tem um grupo gravado
    Quando informo um grupo diferente do gravado
    Então vejo "* Nao altere o grupo do orgao nesta tela *"
    E nada é gravado

  Cenário: RN-08 — grupo não cadastrado
    Quando informo um grupo que não está cadastrado para a minha secretaria
    Então vejo "* Grupo nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — nome do órgão em branco
    Quando confirmo a alteração sem o nome do órgão
    Então vejo "* Informe o nome do orgao *"
    E nada é gravado

  Cenário: RN-10 — endereço em branco
    Quando confirmo a alteração sem o endereço do órgão
    Então vejo "* Informe o endereco do orgao *"
    E nada é gravado

  Cenário: RN-10 — código do bairro em branco
    Quando confirmo a alteração sem o código do bairro
    Então vejo "* Informe o codigo do bairro do orgao *"
    E nada é gravado

  Cenário: RN-10 — bairro não cadastrado
    Quando informo um código de bairro que não existe no cadastro
    Então vejo "* Bairro nao cadastrado *"
    E nada é gravado

  Cenário: RN-10 — contato em branco
    Quando confirmo a alteração sem o nome da pessoa de contato
    Então vejo "* Informe o nome da pessoa para contato *"
    E nada é gravado

  Cenário: RN-11 — segmento de atendimento não cadastrado
    Quando informo um segmento de atendimento que não existe para a minha secretaria
    Então vejo "* Segmento nao cadastrado *"
    E nada é gravado

  Cenário: RN-11 — tipo de apoio não cadastrado
    Quando informo um tipo de apoio que não existe para a minha secretaria
    Então vejo "* Tipo apoio nao cadastrado *"
    E nada é gravado

  Cenário: RN-12 — marca de creche fora de S ou N
    Quando informo na marca de creche um valor diferente de S e de N
    Então vejo "* Informe se creche ou nao com S ou N *"
    E nada é gravado

  Cenário: RN-12 — marca de ativo fora de S ou N
    Quando informo na marca de ativo um valor diferente de S e de N
    Então vejo "* Informe se ativo ou nao com S ou N *"
    E nada é gravado

  Cenário: RN-12 — marca de pedido acumulado fora de S ou N
    Quando informo na marca de órgão para pedido acumulado um valor diferente de S e de N
    Então vejo "* Inf. se Orgao para pedido acumulado com S ou N *"
    E nada é gravado

  Cenário: RN-13 — unidade orçamentária em branco
    Quando confirmo a alteração sem a unidade orçamentária
    Então vejo "* Informe a unidade orcamentaria *"
    E nada é gravado

  Cenário: RN-13 — unidade orçamentária diferente da do grupo
    Quando informo uma unidade orçamentária que não é a do grupo
    Então vejo "<- Unidade orcamentaria do Grupo *"
    E nada é gravado

  Cenário: RN-14 — matriculados em branco
    Quando confirmo a alteração sem o número de matriculados
    Então vejo "* Informe numero de matriculados / capacidade *"
    E nada é gravado

  Cenário: RN-14 — comensais em branco
    Quando confirmo a alteração sem o número de comensais
    Então vejo "* Inf. numero de comensais / refeicoes servidas *"
    E nada é gravado

  Cenário: RN-14 — comensais acima dos matriculados
    Quando informo mais comensais do que matriculados
    Então vejo "* Numero de comensais > numero de matriculados *"
    E nada é gravado

  Cenário: RN-01, RN-10 a RN-14 — alterar a unidade
    Dado que consultei a unidade e ela é do meu grupo
    E preencho nome, endereço, bairro cadastrado, contato, creche, ativo, pedido acumulado, unidade orçamentária do grupo, matriculados e comensais
    Quando confirmo a alteração
    Então os dados da unidade são gravados
    E a operação fica registrada na trilha de auditoria

  Cenário: RN-15 — alterar o nome da unidade
    Dado que a unidade tem o nome antigo no índice de nomes
    E há servidores com esse nome como origem
    Quando altero o nome e confirmo
    Então o nome antigo sai do índice e o novo entra
    E a origem desses servidores passa a ser o nome novo
    E cada uma dessas mudanças fica na trilha de auditoria

  Cenário: RN-16 — desativar a unidade
    Dado que a unidade tem mapa diário aberto e perfil do mês de referência aberto
    Quando deixo a marca de ativo como N e confirmo
    Então o mapa diário e o perfil do mês da unidade ficam fechados
    E a operação fica registrada na trilha de auditoria

  Cenário: RN-17 — excluir a unidade
    Dado que consultei a unidade e ela é do meu grupo
    Quando informo a exclusão e confirmo
    Então a unidade fica marcada como inativa e como excluída
    E o registro continua na base, fora do alcance das consultas
    E os mapas dela ficam fechados
    E a operação fica registrada na trilha de auditoria

  Cenário: RN-19 — registro não encontrado na conferência prévia
    Dado que o registro deixou de existir entre a consulta e a confirmação
    Quando confirmo a alteração ou a exclusão
    Então a operação é recusada com a mensagem do sistema
    E nada é gravado

  Cenário: RN-19 — tipo de órgão excluído
    Dado que o tipo de órgão da sessão está marcado como excluído
    Quando confirmo a operação
    Então a operação é recusada com a mensagem do sistema
    E nada é gravado

  Cenário: RN-20 — falha do banco durante a gravação
    Dado que a gravação do cadastro falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E a unidade não é considerada gravada

  Cenário: RN-21 — o que a tela grava
    Dado que faço uma alteração e uma exclusão de unidade
    Quando o sistema processa cada operação
    Então só o cadastro do órgão filho, o índice de nomes, o cadastro do servidor, os dois mapas e a auditoria recebem gravação
    E o tipo de órgão, o bairro, o segmento, o tipo de apoio, o grupo e o título das telas são apenas lidos
```
