# US — C655T — Rescindir a permissão de fornecimento e registrá-la em outro tipo de contrato e fornecedor

## Estória

Como **servidor da Coordenação Regional Escolar**, quero **rescindir a permissão de
fornecimento da minha regional e registrá-la em outro tipo de contrato e para outro
fornecedor**, para que **a minha regional deixe de comprar pelo contrato que não vale
mais e passe a comprar pelo contrato novo, mantendo o mesmo período de vigência e o
mesmo grupamento que já estavam autorizados**.

A permissão de fornecimento é o que diz de qual fornecedor, em qual tipo de contrato e
dentro de qual vigência a regional pode comprar — é ela que sustenta as quantidades e os
valores que a regional executa. Quando o contrato é substituído, a permissão antiga
precisa ser encerrada e reapresentada no contrato e no fornecedor novos; sem isso a
regional continua comprando por um contrato encerrado, ou para de comprar de vez, porque
fica sem permissão válida para o período que ainda está aberto. A rescisão, porém, não
acontece na hora: quem opera monta o pedido, confirma, e ele entra numa fila de
requisições que um processamento da secretaria executa depois. Por isso a tela avisa que
o cadastro está sendo atualizado, e quem opera precisa voltar à tela para conferir se o
pedido saiu da fila.

## Contexto

Jornada S000M → C000M → C050M → C060M → C655T.

Ator: servidor de CRE — informa a permissão de fornecimento da sua coordenadoria
regional escolar que vai ser rescindida, informa também o tipo de contrato e o
fornecedor para onde a permissão passa, e confirma o pedido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O C000M, o C050M e o C060M são menus: só
encaminham, e não deixam registro nem modo de operação para esta tela.

Esta tela **não abre em consulta**: não existe no fonte comparação com a tela que a
chamou, e o comportamento dela não muda conforme quem a abriu — a opção de operação que
ela exige é sempre a de alteração. O C060M passa a chamada adiante sem passar por menu
nenhum, e o que ele entrega à C655T é a chamada de volta para ela mesma: a C655T é
aberta pelo C060M e, a cada resposta, reabre a própria tela, mantendo no formulário o
que já foi digitado. Como não há registro de passagem, é o operador que informa todos os
dados da permissão; a tela não recebe e não devolve registro nenhum para outra tela.

As regras abaixo são só as da **tela desta jornada**. As regras da entrada estão no
arquivo dela, citado acima.

---

## Regras de negócio

### RN-01 — A permissão é identificada por sete dados, dos dois lados

A tela trabalha com duas fotos da mesma permissão e o operador informa as duas. Do lado
atual — a permissão que existe e vai ser rescindida — ele informa a coordenação regional
escolar, o tipo de contrato, o fornecedor e o grupamento, mais o início e o limite do
período de vigência. Do lado novo — para onde a permissão passa — ele informa o tipo de
contrato, o fornecedor e o grupamento, e o período aparece igual ao do lado atual; a
coordenação regional escolar é a mesma.

O grupamento é dado uma vez e vale para os dois lados. O tipo de contrato e o fornecedor
são os únicos dados que apontam para outro lugar.

### RN-02 — O tipo de órgão é o da sessão, e não se digita

A tela não oferece o tipo de órgão como escolha: ela trabalha dentro do tipo de órgão
que a sessão do servidor deixou, e é ele que amarra todas as consultas que a tela faz —
a permissão, o tipo de contrato, o fornecedor e o período. A data do sistema, exibida no
alto, também vem da sessão, e não é digitada.

### RN-03 — O acesso é conferido a cada operação, e a permissão é do órgão de quem opera

A cada operação o sistema confere se a estação de trabalho é a mesma da sessão e se o
servidor tem o privilégio de alteração para este cadastro. Sem esse privilégio, a
operação não é concluída.

### RN-04 — A tela só trabalha em alteração

A C655T não tem modo de consulta. A opção de operação que ela aceita é a de alteração, e
é a própria tela que a repõe a cada exibição; qualquer outra opção é recusada com o
aviso de que a opção não está disponível e de que se deve usar a tecla de alternativa.

### RN-05 — A coordenação regional escolar é obrigatória

Sem coordenação regional escolar informada — zero ou em branco — a tela recusa com o
aviso de que se deve informar o grupo, devolve o cursor ao campo da coordenação e não
segue para nenhuma outra verificação.

### RN-06 — O tipo de contrato novo tem de ser diferente do atual

A rescisão só se sustenta se o contrato de destino for outro. Se o operador informar o
mesmo tipo de contrato nos dois lados, a tela recusa com o aviso de que se deve informar
outro tipo de contrato, devolve o cursor ao campo do lado novo e para.

### RN-07 — O fornecedor novo tem de ser diferente do atual

Pela mesma razão, o fornecedor de destino tem de ser diferente do fornecedor atual. Se
for o mesmo, a tela recusa com o aviso de que se deve informar outro fornecedor e
devolve o cursor ao campo.

### RN-08 — O grupamento da permissão tem de ser informado

O grupamento também é obrigatório: se estiver em zero, a tela recusa com o aviso de que
se deve informar o grupamento e devolve o cursor ao campo do fornecedor atual.

### RN-09 — A permissão a rescindir tem de existir, e é localizada pelo limite do período

A tela procura a permissão atual pela coordenação regional escolar, pelo tipo de
contrato, pelo fornecedor, pelo grupamento, pelo limite do período e pelo tipo de órgão
da sessão — e só entre as permissões que não estão excluídas e que têm grupamento
preenchido. Se não encontrar, ou se o que encontrar divergir em qualquer um desses
dados, recusa com o aviso de que não há permissão para rescisão cadastrada e devolve o
cursor ao campo do limite do período. Quando encontra, aproveita o início do período da
permissão para as verificações seguintes.

### RN-10 — O tipo de contrato novo tem de estar cadastrado

O tipo de contrato para onde a permissão passa tem de existir no cadastro de tipos de
contrato do tipo de órgão da sessão. Não existindo, a tela recusa com o aviso de que o
tipo de contrato não está cadastrado e devolve o cursor ao campo. O tipo de contrato
atual não passa por essa conferência: ele só é usado para trazer a descrição que aparece
na tela.

### RN-11 — O fornecedor novo tem de estar cadastrado, e não pode estar excluído

O fornecedor de destino tem de existir no cadastro de fornecedores; se não existir, a
tela recusa com o aviso de que o fornecedor não está cadastrado e devolve o cursor ao
campo. Existindo, ele ainda é conferido quanto à situação do cadastro: fornecedor
excluído ou pendente derruba a operação. O fornecedor atual não passa por essa
conferência de situação — ele só é usado para trazer a razão social que aparece na tela,
e a razão social do fornecedor novo, essa sim, só é trazida depois que ele passa.

### RN-12 — O tipo de contrato novo não pode já ter período registrado

Se o tipo de contrato de destino já tiver um período registrado na coordenação regional
escolar informada, com o mesmo início e o mesmo limite, a tela recusa com o aviso de que
o período já está cadastrado para aquele tipo de contrato e devolve o cursor ao campo.
Esse é o caso em que o destino é justamente o contrato que já responde pelo mesmo
período.

### RN-13 — O tipo de contrato novo não pode ter permissão que alcance o início da atual

A tela procura as permissões já existentes do tipo de contrato de destino, na mesma
coordenação regional escolar, no mesmo tipo de órgão e no mesmo grupamento, e compara os
inícios de período delas com o início do período da permissão atual. Se alguma dessas
permissões começar no mesmo momento ou depois, a tela recusa mostrando a data do limite
da permissão mais antiga que alcança esse início, com o aviso de que já existe permissão
para aquele tipo de contrato. Em outras palavras: a permissão nova não pode começar
dentro de um período que o contrato de destino já cobre.

### RN-14 — Nada é gravado antes da confirmação

Passadas todas as conferências, a tela mostra o pedido já montado — coordenação regional
escolar, os dois tipos de contrato com as descrições, os dois fornecedores com as razões
sociais, o grupamento e os dois períodos — e pergunta se a rescisão da permissão deve ser
confirmada. Enquanto a resposta não for a de confirmação, **nada é gravado**: a tela
apenas volta a perguntar. Confirmar é uma resposta de um único caractere, e qualquer
outra coisa mantém o pedido parado.

### RN-15 — Confirmado, o pedido é registrado na fila de requisições

Com a confirmação, o sistema monta o pedido e o registra na fila de requisições que o
processamento desta rescisão consome, com o tipo de requisição, o número de requisição,
a data, o tipo de órgão, a coordenação regional escolar, o tipo de contrato e o
fornecedor de origem, o grupamento, o limite do período, a estação de trabalho e a
matrícula funcional de quem pediu, e o registra como requisição de inclusão. O número da
requisição é o do último pedido do mesmo tipo mais um. A tela então avisa que o cadastro
está sendo atualizado e reabre a si mesma, já com os dados do pedido.

[?] O processamento que consome a fila não está entre os fontes que esta estória devia
ler; pelo que a própria tela declara, ele roda depois e não na hora. O que ele faz com a
permissão não foi conferido aqui e não é afirmado acima.

### RN-16 — A tela não altera a permissão de fornecimento

Esta tela **não** grava, altera nem exclui a permissão de fornecimento. Dos cadastros que
ela lê — permissão de fornecimento, tipo de contrato, fornecedor, título da tela e
servidor — ela só registra na fila de requisições. Quem altera a permissão é o
processamento que consome a fila, depois.

### RN-17 — Um pedido de cada vez: requisição pendente do mesmo processamento recusa

Se já existir requisição pendente para este mesmo processamento, sem resposta, a tela não
aceita outro pedido: ela avisa que o relatório está em processamento e que se deve
aguardar, devolve o cursor ao campo da resposta e para. O aviso aponta para o momento em
que o operador confirma — é o pedido anterior, ainda não atendido, que trava.

### RN-18 — Toda resposta limpa o que estava exibido

A cada resposta, o que a tela havia trazido dos cadastros — descrições do tipo de
contrato, razões sociais dos fornecedores e mensagem — é apagado antes das conferências.
O que o operador vê depois de uma recusa é apenas a mensagem da recusa, e não o que a
tela tinha mostrado na tentativa anterior.

---

## Cenários BDD

```gherkin
Funcionalidade: Rescisão da permissão de fornecimento e registro em outro tipo de contrato e fornecedor

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C655T
    E a tela trabalha dentro do tipo de órgão da minha sessão

  Cenário: A tela identifica a permissão pelos dados dos dois lados
    Dado que informei a coordenação regional escolar, o tipo de contrato, o fornecedor e o grupamento da permissão atual, com o início e o limite do período
    E informei o tipo de contrato e o fornecedor para onde a permissão passa
    Quando confirmo os dados
    Então a tela passa a tratar a permissão atual e a de destino com o mesmo grupamento

  Cenário: O tipo de órgão e a data não são digitados
    Dado que abri a tela
    Então vejo o tipo de órgão e a data do sistema vindos da sessão
    E não há campo para escolher outro tipo de órgão

  Cenário: O acesso é conferido a cada operação
    Dado que estou na estação da minha sessão
    E tenho o privilégio de alteração deste cadastro
    Quando confirmo o pedido
    Então o sistema confere o acesso antes de deixar seguir

  Cenário: A tela só aceita a operação de alteração
    Dado que a operação informada não é a de alteração
    Quando envio o formulário
    Então a tela recusa com o aviso de que a opção não está disponível e que se deve usar a tecla de alternativa
    E o cursor volta ao campo da operação

  Cenário: Sem coordenação regional escolar não passa
    Dado que deixei a coordenação regional escolar em branco
    Quando envio o formulário
    Então a tela recusa com o aviso de que se deve informar o grupo
    E o cursor volta ao campo da coordenação regional escolar
    E nenhuma outra conferência é feita

  Cenário: O tipo de contrato novo tem de ser diferente do atual
    Dado que informei o mesmo tipo de contrato nos dois lados
    Quando envio o formulário
    Então a tela recusa com o aviso de que se deve informar outro tipo de contrato
    E o cursor volta ao campo do lado novo

  Cenário: O fornecedor novo tem de ser diferente do atual
    Dado que informei o mesmo fornecedor nos dois lados
    Quando envio o formulário
    Então a tela recusa com o aviso de que se deve informar outro fornecedor
    E o cursor volta ao campo do fornecedor novo

  Cenário: Sem grupamento não passa
    Dado que deixei o grupamento em zero
    Quando envio o formulário
    Então a tela recusa com o aviso de que se deve informar o grupamento
    E o cursor volta ao campo do fornecedor atual

  Cenário: A permissão a rescindir tem de existir
    Dado que os dados informados não correspondem a nenhuma permissão de fornecimento da minha coordenação regional escolar
    Quando envio o formulário
    Então a tela recusa com o aviso de que a permissão para rescisão não está cadastrada
    E o cursor volta ao campo do limite do período

  Cenário: O tipo de contrato novo tem de estar cadastrado
    Dado que o tipo de contrato de destino não existe no cadastro de tipos de contrato
    Quando envio o formulário
    Então a tela recusa com o aviso de que o tipo de contrato não está cadastrado
    E o cursor volta ao campo do tipo de contrato novo

  Cenário: O fornecedor novo tem de estar cadastrado
    Dado que o fornecedor de destino não existe no cadastro de fornecedores
    Quando envio o formulário
    Então a tela recusa com o aviso de que o fornecedor não está cadastrado
    E o cursor volta ao campo do fornecedor novo

  Cenário: Fornecedor novo excluído ou pendente derruba o pedido
    Dado que o fornecedor de destino existe, mas está excluído ou pendente
    Quando envio o formulário
    Então a tela recusa a operação
    E o cursor volta ao campo do fornecedor novo

  Cenário: O tipo de contrato novo não pode já ter o mesmo período registrado
    Dado que o tipo de contrato de destino já tem período registrado com o mesmo início e o mesmo limite
    Quando envio o formulário
    Então a tela recusa com o aviso de que o período já está cadastrado para aquele tipo de contrato
    E o cursor volta ao campo do tipo de contrato novo

  Cenário: O tipo de contrato novo não pode ter permissão que alcance o início da atual
    Dado que o tipo de contrato de destino já tem permissão que começa no mesmo momento ou depois do início da permissão atual
    Quando envio o formulário
    Então a tela mostra a data do limite da permissão mais antiga que alcança esse início
    E recusa com o aviso de que já existe permissão para aquele tipo de contrato
    E o cursor volta ao campo do tipo de contrato novo

  Cenário: O grupamento pode ser o mesmo do atual, o destino é que muda
    Dado que o grupamento é o mesmo da permissão atual
    E o fornecedor de destino é diferente do atual e está cadastrado e ativo
    E o tipo de contrato de destino é diferente do atual e está cadastrado
    Quando envio o formulário
    Então a tela segue para a confirmação do pedido

  Cenário: Nada é gravado antes da confirmação
    Dado que passou pelas conferências e a tela pediu a confirmação da rescisão da permissão
    Quando respondo algo diferente da confirmação
    Então nenhum pedido é registrado
    E a tela volta a perguntar se a rescisão deve ser confirmada

  Cenário: Confirmado, o pedido entra na fila de requisições
    Dado que a tela pediu a confirmação da rescisão da permissão
    Quando confirmo
    Então o pedido é registrado na fila de requisições do processamento desta rescisão, com o tipo e o número da requisição, a data, o tipo de órgão, a coordenação regional escolar, o tipo de contrato e o fornecedor de origem, o grupamento, o limite do período, a estação e a matrícula funcional
    E o pedido é registrado como requisição de inclusão
    E a tela avisa que o cadastro está sendo atualizado
    E a própria tela é reaberta com os dados do pedido

  Cenário: A permissão de fornecimento não é alterada por esta tela
    Dado que o pedido foi registrado
    Então a permissão de fornecimento continua como estava
    E a alteração depende do processamento que consome a fila

  Cenário: Com requisição pendente do mesmo processamento, a tela recusa
    Dado que já existe requisição pendente, sem resposta, do mesmo processamento
    Quando confirmo o pedido
    Então a tela recusa com o aviso de que o relatório está em processamento e que se deve aguardar
    E o cursor volta ao campo da resposta

  Cenário: A recusa limpa o que estava exibido
    Dado que a tela havia mostrado as descrições e as razões sociais trazidas dos cadastros
    Quando envio um formulário e ele é recusado
    Então o que estava exibido é apagado
    E só a mensagem da recusa permanece
```
