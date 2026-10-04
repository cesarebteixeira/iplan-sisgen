# US — C776T — Pedir a exclusão do cardápio de um período

## Estória

Como **servidor de CRE**, quero **pedir a exclusão do cardápio de um período**, para
que **as validades que já venceram saiam do cadastro e a montagem do período seguinte
não encontre o que já passou**.

O cardápio é cadastrado por validade: cada versão vale de uma data de início até uma
data limite, e é a data limite que distingue uma versão da outra. Terminado o período,
o que ficou no cadastro precisa sair, e quem responde por isso na ponta é a
coordenação regional de ensino. A tela não apaga na hora: ela confere o período e
registra o pedido que manda o cadastro ser apagado em processamento. Enquanto houver
planejamento ou pedido alcançando o período, a exclusão é recusada — o período só sai
quando já não depende dele.

## Contexto

Jornada S000M → C000M → C070M → C776T.
Ator: servidor de CRE — pede a exclusão das validades do cardápio de um período do
tipo de órgão da sua sessão e é recusado enquanto o período ainda tiver planejamento
ou pedidos.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O C000M e o C070M são menus: não gravam
nada e só encaminham.

O contexto de que a tela se serve — a matrícula, o código de acesso, o privilégio, o
tipo de órgão, a estação e a data do sistema — é o que a entrada deixou na sessão; a
tela não o recalcula. O tipo de órgão não é digitado nesta tela, e a coordenação
regional do servidor **não** limita a conferência dos pedidos: ela percorre todas as
coordenações regionais do tipo de órgão da sessão.

O modo de operação não é escolhido pelo servidor e não muda conforme quem chamou a
tela: ao se apresentar, a tela marca a operação como **alteração**, e é essa operação
que segue para as conferências. As conferências de acesso que ela chama são as da
entrada e estão no anexo, em **Regras que se revelaram da entrada**.

A jornada termina nesta tela: ela não encadeia nenhuma outra passando registro e
operação adiante.

---

## Regras de negócio

### RN-01 — A tela pede a exclusão do cardápio de um período; quem apaga é o processamento

A tela não apaga nada por si: ela confere o período, pede a confirmação e registra o
**pedido** do processamento que apaga, em lote, as validades do cardápio do período
(o cadastro C072T) e os registros que compõem cada validade. O que a tela grava é o
pedido e o registro de **auditoria** da operação — as rotinas de exclusão existem
declaradas para todos os cadastros que ela enxerga e nenhuma delas é executada por
caminho nenhum. Terminado o registro, o servidor vê **\* Cadastro sendo excluido \***.

[?] O acervo liga o pedido ao processamento pelo código do relatório, mas **não** tem
catálogo que ligue o trabalho disparado ao programa que ele roda: o que exatamente
apaga o cadastro é conclusão tirada da leitura do programa em lote, não de um
registro do despacho. Pergunta ao site.

### RN-02 — O período é informado pelo dia, o mês e o ano de início e de limite

A tela recebe **seis dados de data**: o dia, o mês e o ano de início e o dia, o mês e
o ano limite. Os seis passam por edição numérica antes de qualquer leitura — campo em
branco é tratado como zero e o que não for número é recusado —, e a conferência não
segue enquanto a digitação não passar. O órgão do cardápio não é informado: tudo o que
a tela faz depois é pelo **tipo de órgão da sessão**.

[?] O que o servidor vê quando a digitação é recusada não está nos fontes desta
jornada — a rotina que faz a edição numérica não faz parte do acervo lido —, e a
devolução do cursor ao campo recusado só está escrita, no fonte da tela, para os três
campos da **data limite**: para o dia, o mês e o ano de início não há posição de
cursor definida. Se a recusa no início é silenciosa ou se a rotina comum devolve o
cursor, o acervo não mostra. Pergunta ao site.

### RN-03 — O período conferido é o da validade do cardápio, não o início digitado

Encontrada a validade do cardápio pela **data limite**, o sistema repõe em tela a data
de início **da própria validade**, e é ela que passa a valer: é ela que entra nas
conferências seguintes e é ela que vai no pedido. O dia, o mês e o ano de início
digitados não são conferidos contra nada nem aproveitados.

[?] Se o início informado deveria limitar a exclusão, ou se a intenção era apenas
mostrar o período, o acervo não responde: o que o fonte mostra é a reposição, sem
nenhuma conferência do que foi digitado. Pergunta ao site.

### RN-04 — Sem validade de cardápio para a data limite, nada é pedido

A tela procura, no cadastro dos cardápios do tipo de órgão da sessão, a validade cuja
data limite é a informada. Não achando — ou achando uma cuja data limite seja outra —,
recusa com **\* Nao existem registros cadastrados \***, devolve o cursor ao campo do
dia limite e não registra pedido nenhum.

### RN-05 — Com planejamento cadastrado no período, a exclusão é recusada

Existindo planejamento do período para o tipo de órgão, a tela recusa com
**\* Nao exclua. Planejamentos cadastrados \***, devolve o cursor ao dia limite e não
pede a exclusão. A conferência é do período como um todo: o planejamento (o cadastro
C771T) é procurado pelo tipo de órgão e pelas três datas de limite.

[?] A leitura do planejamento é feita com a coordenação regional zerada, e a
conferência que vem depois compara só o tipo de órgão e as três datas de limite — a
coordenação regional nunca é comparada. Se isso alcança o planejamento de qualquer
coordenação regional ou só o de uma depende do posicionamento da leitura, que o
acervo não explica. Pergunta ao site.

### RN-06 — Com pedidos que alcançam o período, a exclusão é recusada

A tela percorre as coordenações regionais do tipo de órgão e, em cada uma, os pedidos
(o cadastro E010T) registrados. Se algum pedido alcançar o período — começando dentro
dele, terminando dentro dele ou envolvendo-o por inteiro —, a exclusão é recusada com
**\* Nao exclua. Ja existem pedidos cadastrados \***, com o cursor de volta ao dia
limite. Pedido que já foi excluído não conta.

[?] A varredura dos pedidos começa na data de início da validade do cardápio e para
quando encontra um pedido que começa depois da data limite; um pedido que comece
**antes** do período e termine dentro dele pode ficar fora da conferência. Se isso é
possível no dia a dia, e se a leitura posiciona ou exige a data exata, o acervo não
responde. Pergunta ao site.

### RN-07 — A exclusão só é pedida depois da confirmação do servidor

Passando nas conferências, a tela mostra o período e pergunta
**\* Confirma exclusao dos cadastros <S/N> ? \***. Só a resposta **S** leva ao pedido;
qualquer outra resposta não grava nada e devolve a tela às conferências, que são
refeitas e a confirmação é pedida de novo.

[?] Como a resposta diferente de S volta a pedir a confirmação, quem responde N não
cancela: refaz as conferências e vê a mesma pergunta — não há, no fluxo, um caminho de
desistir que não seja abandonar a tela. Se isso é o pretendido, e o que a máscara
mostra nesse caso, o acervo não diz. Pergunta ao site.

### RN-08 — Com um pedido do mesmo processamento em andamento, a tela recusa outro

Havendo um pedido do mesmo relatório já registrado e ainda não processado, a tela não
registra um segundo: avisa **\* Relatorio em processamento. Aguarde. \*** e volta com
o cursor ao campo da resposta. O processamento apaga o próprio pedido ao terminar, e é
isso que libera a tela para o pedido seguinte.

### RN-09 — A tela só trabalha em alteração

Ao se apresentar, a tela marca a operação como **alteração**, e é essa operação que
segue para as conferências. Se a mensagem do servidor chegar com outra operação, a
recusa é **\* Opcao nao disponivel. Use ALT \***, com o cursor no campo da resposta e
nada lido nem registrado. Não há modo de consulta nesta tela: ela não lista nada.

[?] A recusa manda usar ALT, mas o que a tela aceita é o código interno da alteração,
e nenhum valor "ALT" existe no acervo lido; o texto exato da máscara não está no lote.
A mesma dúvida está registrada nas telas irmãs. Pergunta ao site.

### RN-10 — O pedido é numerado pelo sistema, identificado pela sessão, e a operação fica na auditoria

O pedido recebe o **número seguinte** ao do último pedido registrado — o servidor não
o informa. Com ele vão a matrícula do funcionário, a estação, o dia e o mês do
sistema, o tipo de órgão da sessão, o período e o **e-mail do funcionário**, e o
pedido é encaminhado para processamento. A operação também fica na **auditoria**
(A010T), com a tela de origem, a operação, o período pedido, a matrícula, a estação, o
dia, o mês, o ano e a hora da sessão e o tipo de órgão.

[?] O número seguinte é tirado da última requisição registrada com o auxílio de um
posicionamento de leitura cujo efeito exato não está no acervo nem no manual. Se a
numeração é sempre a do último pedido mais um, o site precisa confirmar. Pergunta ao
site.

### RN-11 — Nenhuma recusa deixa pedido nem rastro de auditoria

Cada uma das **cinco recusas** da tela — operação diferente de alteração, relatório já
em processamento, validade de cardápio não encontrada, planejamento cadastrado e
pedidos alcançando o período — devolve a tela ao começo e termina sem gravar: nesses
caminhos não há pedido nem registro de auditoria.

### RN-12 — A tela mostra a data do sistema e a descrição do tipo de órgão da sessão

Fora do período e das mensagens, a tela exibe a **data do sistema** e a **descrição do
tipo de órgão** da sessão.

[?] Nem uma nem outra são preenchidas por um caminho que o acervo mostre: a tela copia
as duas de áreas de trabalho da sessão, e a entrada as guarda em outras. Se o ambiente
transporta os valores de uma área para a outra — e de onde vem a data do sistema —, o
acervo não diz; se não transportar, os dois campos saem em branco. A mesma dúvida está
registrada nas telas irmãs. Pergunta ao site.

### RN-13 — Chegando com a próxima tela preenchida, a tela encaminha e não faz mais nada

O campo da próxima tela é o que faz uma tela passar o servidor para outra sem passar
por menu nenhum. Chegando preenchido, o roteamento do sistema leva o servidor à tela
indicada e a conferência desta tela termina ali: ela não lê, não avisa e não grava.

[?] O campo da próxima tela faz parte do registro da tela, mas não tem rótulo na ficha
desta tela; se ele é visível e digitável pelo servidor, ou se só quem chama a tela o
preenche, o acervo não mostra. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedir a exclusão do cardápio de um período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C776T

  Cenário: Exclusão pedida para um período sem uso
    Dado que existe uma validade de cardápio do meu tipo de órgão terminando na data limite que vou informar
    E não há planejamento nem pedido alcançando o período
    Quando informo o dia, o mês e o ano de início e de limite e confirmo com S
    Então o sistema registra o pedido da exclusão com o número seguinte ao do último pedido
    E registra a operação na auditoria
    E vejo a mensagem "* Cadastro sendo excluido *"

  Cenário: O período conferido passa a ser o da validade do cardápio
    Dado que informei uma data de início diferente da data de início da validade do cardápio
    Quando o sistema encontra a validade pela data limite
    Então a data de início em tela passa a ser a da validade
    E é essa data que vale para as conferências e para o pedido

  Cenário: Digitação não numérica ou em branco nas datas
    Dado que digitei algo que não é número em um dos campos de data
    Quando envio a tela
    Então a tela recusa a digitação
    E não pede a exclusão

  Cenário: Não há validade de cardápio para a data limite
    Dado que não existe validade de cardápio do meu tipo de órgão terminando na data limite informada
    Quando envio a exclusão
    Então vejo a mensagem "* Nao existem registros cadastrados *"
    E o cursor volta ao campo do dia limite
    E nada é pedido

  Cenário: Exclusão recusada porque há planejamento no período
    Dado que existe planejamento do período para o meu tipo de órgão
    Quando envio a exclusão
    Então vejo a mensagem "* Nao exclua. Planejamentos cadastrados *"
    E o cursor volta ao campo do dia limite
    E nada é pedido

  Cenário: Exclusão recusada porque há pedidos alcançando o período
    Dado que existe pedido de alguma coordenação regional do meu tipo de órgão alcançando o período
    Quando envio a exclusão
    Então vejo a mensagem "* Nao exclua. Ja existem pedidos cadastrados *"
    E o cursor volta ao campo do dia limite
    E nada é pedido

  Cenário: Pedido já excluído não impede a exclusão
    Dado que o único pedido que alcançaria o período já foi excluído
    Quando envio a exclusão
    Então o sistema pede a confirmação
    E o pedido da exclusão pode ser registrado

  Cenário: A confirmação é pedida antes de registrar
    Dado que o período passou em todas as conferências
    Quando envio a exclusão
    Então vejo a mensagem "* Confirma exclusao dos cadastros <S/N> ? *"
    E nada foi gravado ainda

  Cenário: Resposta diferente de S não grava nada
    Dado que vi a pergunta de confirmação
    Quando respondo N
    Então nada é pedido
    E a tela volta às conferências e pede a confirmação de novo

  Cenário: Já existe um pedido do mesmo processamento em andamento
    Dado que existe um pedido do mesmo relatório ainda não processado
    Quando confirmo a exclusão
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da resposta
    E nada é pedido

  Cenário: Operação diferente de alteração é recusada
    Quando informo uma operação diferente de alteração
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo da resposta
    E nada é lido nem pedido

  Cenário: Nenhuma recusa deixa rastro
    Dado que a exclusão foi recusada por qualquer um dos motivos
    Então nenhum pedido é registrado
    E nenhum registro de auditoria é gerado

  Cenário: A data do sistema e a descrição do tipo de órgão
    Quando abro a tela C776T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: Chegando com a próxima tela preenchida
    Dado que cheguei à tela C776T com o campo da próxima tela preenchido
    Quando envio a tela
    Então o sistema me leva à tela indicada
    E esta tela não lê, não avisa e não grava
```
