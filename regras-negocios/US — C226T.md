# US — C226T — Substituir o órgão provisório pelo órgão definitivo SDI da coordenadoria regional

## Estória

Como **servidor de CRE**, quero **registrar que o órgão provisório da minha coordenadoria
foi substituído pelo órgão definitivo SDI**, para que os vínculos e os registros que
estavam presos ao provisório passem a apontar para o definitivo e o histórico da
coordenadoria mostre de qual provisório ele veio.

O órgão provisório é a situação transitória de uma coordenadoria: enquanto o órgão
definitivo não assume, os vínculos de atendimento, as referências e os vínculos dos
servidores ficam presos a ele. Quando o definitivo assume, tudo isso tem de mudar de órgão
de uma vez — e é essa passagem que a tela registra e manda processar. Sem ela, a
coordenadoria continuaria apontando para um órgão que não é mais o seu, e o histórico não
diria de onde o órgão definitivo veio.

## Contexto

Jornada S000M → C000M → C200M → C226T.

Ator: servidor de CRE — registra a substituição do órgão provisório pelo órgão definitivo
da sua coordenadoria.

A entrada — o LOGON e o menu principal S000M — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O C000M e o C200M são menus e não gravam nada: só encaminham, e não deixam dado de negócio
nenhum para esta tela. A C226T é alcançada só por esse caminho de menu, e por isso não
recebe de quem a chamou nem o registro nem a operação: ela fixa a operação sozinha (RN-02),
e o seu comportamento não muda conforme a tela de origem. O contexto de que ela se serve —
a matrícula, o código de acesso, o privilégio, o tipo de órgão, a coordenadoria e a estação
da sessão — é o que a entrada deixou na sessão. Para ver o histórico já registrado existe a
C226C; esta tela é de manutenção.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela registra a substituição do órgão provisório pelo órgão definitivo da coordenadoria

A C226T é a manutenção do histórico de órgãos da coordenadoria regional escolar. Ela se
identifica pelos rótulos **CORD.REG.ESCOLAR** — a coordenadoria — e **ORGAO FILHO SDI** — o
órgão definitivo — e pede três dados: a coordenadoria (2 dígitos), o órgão provisório (8
dígitos) e o órgão definitivo (8 dígitos), além da resposta da confirmação. A tela mostra o
nome dos dois órgãos, a descrição do tipo de órgão da sessão e a data do sistema. Ela não
abre outra tela: depois da atualização ela mesma é reapresentada.

### RN-02 — A tela só opera em alteração

A tela abre com a operação fixada em **alteração** e a repõe a cada apresentação. Se for
informada uma operação diferente, o sistema recusa com
**\* Operacao nao disponivel. Use ALT \*** e devolve o cursor ao campo da operação. Não há
modo de consulta nesta tela.

[?] A recusa só existe se a máscara apresentar o campo da operação ao servidor. Como a
abertura repõe a alteração sozinha, a recusa só pode ser alcançada numa mensagem seguinte;
o texto da máscara não está no material lido. Pergunta ao site.

### RN-03 — A coordenadoria é a do vínculo do servidor

O campo da coordenadoria abre preenchido com a coordenadoria do vínculo do servidor e não
aceita outra: informada uma coordenadoria diferente, o sistema recusa com
**\* Usuario sem acesso a outro grupo \*** e devolve o cursor ao campo da coordenadoria.
Em branco, a recusa é **\* Informe o grupo \***. Um servidor sem coordenadoria no vínculo é
o único caso em que o campo aceita um código digitado; nesse caso é a coordenadoria
informada que passa a valer.

[?] A área que a entrada deixa na sessão e a cópia que a tela lê são duas áreas diferentes
da mesma sessão. Se elas não carregarem o mesmo valor, a conferência recusa a coordenadoria
do próprio servidor, e a atualização fica inalcançável para quem tem coordenadoria. O que
separa as duas cópias é do ambiente de execução e não está no acervo. Pergunta ao site.

### RN-04 — A atualização só acontece depois da pergunta de confirmação

Passadas as conferências, o sistema pergunta
**\* Confirma atualizacao do Orgao <S/N> ? \*** e só a resposta **S** prossegue. A resposta
**N** não cancela: o sistema confere tudo de novo e volta a fazer a mesma pergunta. Se
algum dos três dados mudar entre a pergunta e a resposta, a pergunta é refeita. Confirmada
a resposta, a tela avisa **\* Cadastro sendo atualizado \***.

[?] Como o servidor desiste da operação não está no fonte desta tela: a resposta diferente
de S devolve a pergunta, e o abandono depende dos recursos de saída do ambiente de
execução, que não têm fonte no acervo. Pergunta ao site.

### RN-05 — O órgão provisório tem de existir, estar desativado e ser o da coordenadoria

O órgão provisório informado é procurado no cadastro de órgãos. Não existindo — ou estando
excluído —, a recusa é **\* Orgao provisorio nao cadastrado \***. Existindo, ele ainda
precisa passar por cinco conferências, cada uma com a sua recusa: não pode ser um órgão de
pedido acumulado (**\* Orgao cadastrado para pedido acumulado \***); os dados cadastrais
têm de estar completos — bairro, órgão pai, nome, endereço, quantidade de matrículas e
quantidade de pessoas (**\* Orgao cadastrado com dados incompletos \***); tem de ser do
tipo de órgão da secretaria da sessão (**\* Orgao nao pertence a esta secretaria \***); tem
de ser da coordenadoria informada (**\* Orgao provisorio cadastrado em outro grupo \***); e
tem de estar **desativado** — um provisório ainda ativo é recusado com
**\* Orgao provisorio nao desativado \***.

[?] A tela exige o órgão provisório desativado, mas não é ela que o desativa: nenhum
caminho desta jornada grava no cadastro de órgãos. A desativação é feita antes, na
manutenção de órgãos. Se o servidor chegar aqui com o provisório ainda ativo, o que ele faz
é pergunta ao site.

### RN-06 — O órgão definitivo tem de existir, estar ativo e ainda não ter registros próprios

O órgão definitivo (o órgão filho SDI) é procurado no mesmo cadastro de órgãos. Não
existindo — ou estando excluído —, a recusa é **\* Orgao definitivo nao cadastrado \***.
Existindo, valem as mesmas conferências do provisório — pedido acumulado, dados
incompletos, tipo de órgão da secretaria e coordenadoria — com as recusas correspondentes,
mas na direção oposta quanto à situação: o definitivo tem de estar **ativo**, e um
definitivo desativado é recusado com **\* Orgao definitivo desativado \***. Por fim, o
definitivo não pode já ter vínculo com segmento de atendimento registrado: havendo, a
recusa é **\* Ja existem registros para o Orgao definitivo \***, porque é para ele que os
vínculos do provisório vão ser transferidos.

[?] A conferência dos vínculos do órgão definitivo procura o vínculo por um único segmento
— o primeiro. Se o órgão já tiver vínculos em outros segmentos, a conferência não os vê.
Se isso é intenção, pergunta ao site.

### RN-07 — Confirmada a substituição, a tela registra o histórico da coordenadoria

Confirmada a resposta, a tela grava um registro novo no cadastro do histórico de órgãos
(C227T), com o tipo de órgão, a coordenadoria, o **órgão definitivo**, o **órgão
provisório** de onde ele veio, a matrícula do servidor que registrou e a data e a hora da
atualização. É esse registro que a C226C mostra e que a relação imprime.

[?] O histórico aceita mais de um registro para o mesmo órgão definitivo — a tela não
confere se já existe um. O que impede uma segunda substituição para o mesmo órgão
definitivo é a conferência dos vínculos de segmento, que passam a existir depois da
primeira transferência. Se a intenção era recusar pelo próprio histórico, o caminho não o
faz. Pergunta ao site.

### RN-08 — A operação fica registrada na auditoria

Além do histórico, a tela grava um registro na trilha de auditoria (A010T) com a tela de
origem (C226T), o cadastro alterado (o histórico de órgãos), a operação de inclusão, a
matrícula do servidor, a estação, a sessão (ano, dia, mês e hora do sistema), o número do
processo — o código do órgão definitivo —, o tipo de órgão e a coordenadoria, sem conteúdo
anterior e com o registro novo como conteúdo posterior.

### RN-09 — A tela pede a relação da coordenadoria e dispara a transferência dos registros

A tela registra um pedido na fila de requisições de impressão (S040T) com o **número
seguinte ao do último pedido da fila**, a relação da coordenadoria, o tipo de órgão, a
coordenadoria, a matrícula de quem pediu, a estação, o dia, o mês e o ano do pedido. Em
seguida dispara o processamento da relação. É esse processamento que **transfere para o
órgão definitivo os registros que estavam apontando para o órgão provisório** — cadastro a
cadastro, entre eles o vínculo do órgão com o segmento de atendimento e o vínculo dos
servidores com a secretaria — e que, ao terminar, apaga da fila os pedidos que atendeu.
Enquanto ele não roda, a substituição está apenas registrada: os registros continuam no
órgão provisório.

[?] O que liga o pedido ao processamento é o nome do trabalho entregue à fila de execução.
Não há, no material lido, catálogo que ligue esse nome ao programa que roda: a ligação é
conclusão tirada de os dois terem a mesma relação. Pergunta ao site.

[?] O endereço de correio do servidor é lido do cadastro de funcionários e vai no parâmetro
do processamento, mas não é gravado no pedido da fila. Se a relação deveria usar o correio
do pedido, o caminho não o preenche. Pergunta ao site.

### RN-10 — Com um pedido pendente para a coordenadoria, a tela recusa nova atualização

Antes de gravar, o sistema procura um pedido ainda não atendido da relação desta tela para
o tipo de órgão e a coordenadoria informados. Havendo, recusa com
**\* Relatorio em processamento. Aguarde. \*** e devolve o cursor ao campo da confirmação. A
conferência é pela **coordenadoria**, não pelo par de órgãos: enquanto houver um pedido
pendente, nenhuma nova substituição é aceita naquela coordenadoria.

### RN-11 — Sem confirmação, a tela não grava nada

Todas as gravações ficam depois da confirmação e das conferências. Uma recusa, ou uma
resposta diferente de **S**, termina a passagem sem gravar: nenhum registro de histórico,
nenhum registro de auditoria e nenhum pedido é criado.

---

## Cenários BDD

```gherkin
Funcionalidade: Substituir o órgão provisório pelo órgão definitivo SDI da coordenadoria regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a minha coordenadoria regional escolar
    E tenho acesso à tela C226T

  Cenário: Substituição registrada e mandada processar
    Dado que o órgão provisório existe, está desativado e é da minha coordenadoria
    E que o órgão definitivo existe, está ativo e ainda não tem vínculos de segmento
    Quando informo os dois órgãos e respondo S à pergunta de confirmação
    Então o sistema registra no histórico da coordenadoria o órgão definitivo e de qual provisório ele veio
    E registra a operação na auditoria
    E põe na fila o pedido da relação
    E dispara o processamento que transfere os registros do provisório para o definitivo
    E vejo a mensagem "* Cadastro sendo atualizado *"

  Cenário: O histórico registra a data e a hora da atualização
    Dado que confirmei a substituição
    Então o registro do histórico traz o tipo de órgão, a coordenadoria e a matrícula de quem registrou
    E traz a data e a hora da atualização

  Cenário: O processamento transfere os registros e limpa a fila
    Dado que registrei a substituição e o processamento da relação roda
    Então os registros que apontavam para o órgão provisório passam a apontar para o órgão definitivo
    E o pedido atendido sai da fila de requisições de impressão

  Cenário: Operação diferente da alteração
    Dado que estou na tela C226T
    Quando informo uma operação diferente da alteração
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo da operação

  Cenário: Coordenadoria em branco
    Dado que estou na tela C226T
    Quando deixo a coordenadoria em branco
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo da coordenadoria

  Cenário: Coordenadoria de outra coordenadoria é recusada
    Dado que estou na tela C226T com a minha coordenadoria preenchida
    Quando informo outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo da coordenadoria

  Cenário: A pergunta de confirmação
    Dado que os dois órgãos passaram nas conferências
    Quando envio a tela
    Então vejo a pergunta "* Confirma atualizacao do Orgao <S/N> ? *"
    E nada é gravado antes de eu responder

  Cenário: Resposta diferente de S não cancela a substituição
    Dado que vejo a pergunta de confirmação
    Quando respondo N
    Então o sistema confere os dois órgãos de novo
    E vejo a mesma pergunta outra vez
    E nada foi gravado

  Cenário: Órgão provisório não cadastrado
    Dado que o órgão provisório informado não existe no cadastro de órgãos
    Quando envio a tela
    Então vejo a mensagem "* Orgao provisorio nao cadastrado *"
    E o cursor volta ao campo do órgão provisório
    E nada é gravado

  Cenário: Órgão de pedido acumulado é recusado
    Dado que o órgão informado é de pedido acumulado
    Quando envio a tela
    Então vejo a mensagem "* Orgao cadastrado para pedido acumulado *"
    E o cursor volta ao campo do órgão
    E nada é gravado

  Cenário: Órgão com dados cadastrais incompletos é recusado
    Dado que falta bairro, órgão pai, nome, endereço, matrículas ou pessoas no órgão informado
    Quando envio a tela
    Então vejo a mensagem "* Orgao cadastrado com dados incompletos *"
    E o cursor volta ao campo do órgão
    E nada é gravado

  Cenário: Órgão de outra secretaria é recusado
    Dado que o órgão informado é de outro tipo de órgão, e não o da minha sessão
    Quando envio a tela
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E o cursor volta ao campo do órgão
    E nada é gravado

  Cenário: Órgão provisório de outra coordenadoria é recusado
    Dado que o órgão provisório informado pertence a outra coordenadoria
    Quando envio a tela
    Então vejo a mensagem "* Orgao provisorio cadastrado em outro grupo *"
    E o cursor volta ao campo do órgão provisório
    E nada é gravado

  Cenário: Órgão provisório ainda ativo é recusado
    Dado que o órgão provisório informado continua ativo
    Quando envio a tela
    Então vejo a mensagem "* Orgao provisorio nao desativado *"
    E o cursor volta ao campo do órgão provisório
    E nada é gravado

  Cenário: Órgão definitivo não cadastrado
    Dado que o órgão definitivo informado não existe no cadastro de órgãos
    Quando envio a tela
    Então vejo a mensagem "* Orgao definitivo nao cadastrado *"
    E o cursor volta ao campo do órgão definitivo
    E nada é gravado

  Cenário: Órgão definitivo de outra coordenadoria é recusado
    Dado que o órgão definitivo informado pertence a outra coordenadoria
    Quando envio a tela
    Então vejo a mensagem "* Orgao definitivo cadastrado em outro grupo *"
    E o cursor volta ao campo do órgão definitivo
    E nada é gravado

  Cenário: Órgão definitivo desativado é recusado
    Dado que o órgão definitivo informado está desativado
    Quando envio a tela
    Então vejo a mensagem "* Orgao definitivo desativado *"
    E o cursor volta ao campo do órgão definitivo
    E nada é gravado

  Cenário: Órgão definitivo já com vínculos de segmento é recusado
    Dado que o órgão definitivo informado já tem vínculo com segmento de atendimento
    Quando envio a tela
    Então vejo a mensagem "* Ja existem registros para o Orgao definitivo *"
    E o cursor volta ao campo do órgão definitivo
    E nada é gravado

  Cenário: Pedido da relação ainda pendente
    Dado que já existe um pedido da relação desta coordenadoria sem atender
    Quando confirmo a substituição
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da confirmação
    E nada é gravado

  Cenário: Sem confirmação a tela não grava nada
    Dado que estou na tela C226T e as conferências passaram
    Quando a transação termina sem eu responder S à pergunta de confirmação
    Então nenhum registro de histórico é criado
    E nenhum registro de auditoria é criado
    E nenhum pedido é posto na fila
```
