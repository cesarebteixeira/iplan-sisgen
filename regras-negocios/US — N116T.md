# US — N116T — Pedido de inclusão automática das notas de um processo

## Estória

Como **servidor da CRE**, quero **pedir a inclusão automática das notas fiscais de
um processo**, para que **as notas daquele processo entrem no sistema sem digitação,
a partir do que o processamento em lote monta**.

A tela não inclui nota nenhuma: ela reúne o pedido — o processo, a coordenadoria, o
tipo de contrato, o fornecedor, a fonte, o tipo de processo e a impressora —, registra
a requisição e a entrega ao processamento em lote. Sem esse pedido o lote não tem o
que processar; e, enquanto houver requisição recente deste relatório para a mesma
coordenadoria do mesmo órgão, o sistema não deixa pedir de novo. Nada é gravado antes
de o servidor responder à pergunta de confirmação.

## Contexto

Jornada S000M → N000M → N050M → N116T.
Ator: servidor de CRE — informa o processo e os parâmetros do pedido, confirma e pede
a inclusão automática das notas.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada, `N000M` e `N050M`, são menus: nenhuma delas passa
operação nem registro para a `N116T`. Quem decide o modo da tela é ela mesma — ela
abre sempre em inclusão —, e a tela não muda de comportamento conforme quem a chamou.
Depois de cada passo a `N116T` reabre a si mesma; ela não encadeia em outra tela.

O que a tela usa da sessão — a matrícula, o órgão, a coordenadoria regional escolar e a
estação — é o que a entrada deixou do vínculo da matrícula com a secretaria, e a tela
apenas o repassa às conferências e à requisição. As regras abaixo são só as da tela
desta jornada.

---

## Regras de negócio

### RN-01 — A tela não inclui a nota: ela pede a inclusão automática

A tela não monta nem inclui nota fiscal nenhuma. Ela reúne o pedido, registra uma
requisição no cadastro de requisições e entrega essa requisição ao processamento em
lote, junto com o bloco de parâmetros do relatório, que é quem faz a inclusão
automática das notas do processo. Nenhum cadastro do processo, da nota, do fornecedor
ou da fonte é gravado por ela: a única gravação é a da própria requisição. Entregue o
pedido, a tela avisa **\* Cadastro sendo atualizado \*** e volta a si mesma, pronta
para outro pedido.

[?] A tela enfileira o relatório desta jornada, mas não confere se o meu acesso tem
esse relatório liberado — a conferência de autorização de relatório, que outra tela do
módulo chama, não é chamada por esta. Se ela deveria valer aqui, ou se é feita no
processamento em lote, pergunta ao site.

[?] O que a inclusão automática cobre, em negócio, não sai desta jornada: o programa
que o processamento em lote executa não é uma das telas da jornada. Nos cadastros a
abreviação é de nota fiscal; a tela diz só "notas". Pergunta ao site.

### RN-02 — A tela abre em inclusão e só opera em inclusão

Ao abrir, a própria tela fixa a operação em inclusão — nesta tela não há consulta,
alteração nem exclusão, e a operação não vem de quem a chamou. Um envio marcado com
outra operação é recusado com **\* Opcao nao disponivel. Use INC \***, e a tela fica
parada.

[?] A tela fixa a inclusão na abertura e, no mesmo envio, recusa qualquer outra
operação — mas o acervo não traz o desenho da tela (a máscara dos campos). Se o campo
de operação for protegido, essa recusa nunca aparece. Pergunta ao site.

### RN-03 — A tela abre com a secretaria, a coordenadoria e os dígitos de controle preenchidos

Ao abrir, a tela consulta o cadastro do órgão da sessão e já traz preenchidos o
**código da secretaria** — o código de secretaria municipal do órgão —, a
**coordenadoria regional escolar** da sessão e, quando o cadastro do órgão manda
numerar o processo pela coordenadoria regional, os **dois dígitos de controle** do
número do processo, com a coordenadoria da sessão. O código do lote, o número central
do processo, o tipo de contrato, o fornecedor, a fonte, o tipo de processo e a
impressora vêm em branco. Abrir a tela não grava nada: ela só lê o cadastro do órgão e
o cadastro da própria tela.

[?] O indicador do cadastro do órgão que decide se os dois dígitos de controle entram no
número do processo é comparado com dois valores apenas, e nenhuma tela da jornada o
descreve em negócio. O que ele significa é pergunta ao site.

### RN-04 — O processo é identificado por quatro códigos, e dois deles são obrigatórios

O servidor identifica o processo pelo **código da secretaria** (dois dígitos), pelo
**código do lote** (seis dígitos) e pelo **número central do processo** (quatro
dígitos); a esses a tela acrescenta os **dois dígitos de controle**, e as quatro partes
formam o número de processo de catorze dígitos, que é o que a tela lê e entrega ao
pedido. O lote e o número central são obrigatórios: chegando em branco, a recusa é
**\* Numero do processo invalido \***.

Quando o cadastro do órgão não manda numerar o processo pela coordenadoria regional, os
dois dígitos de controle têm de vir em branco: preenchidos, a mesma recusa
**\* Numero do processo invalido \***.

[?] O número de catorze dígitos muda de desenho conforme os dois dígitos de controle
venham preenchidos ou não: com eles, o código da secretaria ocupa as duas primeiras
posições do número; sem eles, as duas primeiras ficam zeradas e o código passa para a
terceira e a quarta. Se os dois desenhos convivem no mesmo cadastro, o mesmo processo
pode ser alcançado por dois números diferentes. Pergunta ao site.

[?] Os dois dígitos de controle e o número central do processo não têm rótulo de negócio
no acervo: o rótulo que a tela carrega para eles é o nome interno do campo, enquanto os
outros seis códigos têm rótulo em português. O que os dois identificam é pergunta ao
site.

### RN-05 — O código da secretaria tem de ser um dos seis do órgão da sessão

O código da secretaria não é livre: a tela o confere contra o cadastro do órgão da
sessão — um código principal e mais cinco alternativos, seis ao todo. Não estando entre
os seis, a recusa é **\* Inicio do processo invalido \*** e a tela não segue.

### RN-06 — A coordenadoria regional escolar tem de estar cadastrada e ser a minha

A coordenadoria regional escolar informada é conferida contra o cadastro de
coordenadorias: não existindo, a recusa é **\* Grupo nao cadastrado \***. Quando a
minha sessão tem coordenadoria fixa, o pedido tem de ser dessa coordenadoria; sendo
outra, a recusa é **\* Usuario sem acesso a este grupo \***. Quando a minha sessão não
tem coordenadoria fixa, a tela exige que uma seja informada —
**\* Informe o grupo \***.

### RN-07 — O processo tem de ser da coordenadoria do servidor

Quando o processo já tem nota lançada, a tela toma a coordenadoria do próprio processo
e a confere contra a da sessão; sendo outra, a recusa é
**\* Usuario sem acesso ao grupo deste processo \***. É essa conferência que impede o
servidor de uma coordenadoria de pedir a inclusão das notas do processo de outra.

### RN-08 — Os códigos da tela são numéricos

Os nove códigos que o servidor informa — a secretaria, os dígitos de controle, o lote,
o número central do processo, a coordenadoria regional escolar, o tipo de contrato, o
fornecedor, a fonte de recursos e o tipo de processo — são números, cada um com o seu
tamanho. O que não for número, ou não couber no tamanho, é recusado antes de qualquer
consulta a cadastro, e a tela marca o campo para correção.

### RN-09 — O tipo de contrato tem de estar cadastrado

O tipo de contrato informado é conferido no cadastro de tipos de contrato do órgão. Não
existindo — ou estando marcado para exclusão — a recusa é
**\* Tipo de contrato nao cadastrado \***.

### RN-10 — O fornecedor tem de estar cadastrado

O fornecedor informado é conferido no cadastro de fornecedores. Não existindo — ou
estando marcado para exclusão — a recusa é **\* Fornecedor nao cadastrado \***.
Existindo, a tela mostra a razão social dele no pedido.

### RN-11 — A fonte de recursos tem de ter código a partir de 1000 e estar cadastrada

Código de fonte menor que 1000 é recusado de saída, com **\* Fonte invalida \***.
Código válido que não exista no cadastro de fontes do órgão — ou que esteja marcado
para exclusão — é recusado com **\* Fonte nao cadastrada \***. Existindo, a tela mostra
a descrição da fonte no pedido.

### RN-12 — O tipo de processo, quando informado, tem de estar cadastrado

Informado o tipo de processo, a tela o confere no cadastro de tipos de processo do
órgão; não existindo, a recusa é **\* Tipo processo nao cadastrado \***. Não informado,
não há conferência: a tela segue com o tipo que vier do processo.

### RN-13 — Processo com nota lançada fornece os próprios dados ao pedido

Quando o processo já tem nota lançada, a tela não usa o que o servidor digitou para o
tipo de contrato, o fornecedor, a fonte e o tipo de processo: ela toma esses dados do
próprio processo — o tipo de contrato, o fornecedor e a fonte da nota, e o tipo de
processo do registro do processo —, mostra-os na tela, e é com eles que o pedido sai. A
coordenadoria segue a mesma regra: passa a ser a do processo. As conferências de
cadastro recaem sobre esses valores, não sobre os digitados.

[?] Com o processo tendo nota lançada, a coordenadoria que o servidor digita é
substituída pela do processo, pouco antes da conferência que compara a coordenadoria do
campo com a da sessão. O campo é digitável, mas o que vale é o do processo: se ele
serve para alguma conferência, ou se é simplesmente ignorado, o fonte não diz. Pergunta
ao site.

### RN-14 — Processo pré-liquidado, liquidado ou pago não entra no pedido

Se o andamento do processo já chegou a pré-liquidado, liquidado ou pago, a inclusão
automática das notas é recusada, com a mensagem do estágio:
**\* Processo pre-liquidado \***, **\* Processo liquidado \*** ou
**\* Processo pago \***. Processo que ainda não chegou a nenhum desses estágios segue
normalmente.

[?] O processo que está no cadastro de empenhos com uma situação diferente das três
também barra o pedido, mas aí a tela para **sem mensagem nenhuma**: o servidor vê a
transação terminar sem saber por quê. Se as três situações são as únicas possíveis, o
desfecho mudo não acontece. Pergunta ao site.

### RN-15 — A conferência do andamento e a da integração só rodam com nota lançada

As duas conferências anteriores — a do andamento do processo e a da integração com o
SIAFIC —, e também a leitura do tipo de processo do processo, só acontecem quando o
processo já tem nota lançada no cadastro de notas. Sem nota lançada, a tela não as
faz: segue direto para as conferências da coordenadoria, do tipo de contrato, do
fornecedor, da fonte e do tipo de processo, e o pedido pode sair sem que o andamento e
a integração tenham sido olhados.

[?] Se a ausência de nota lançada é mesmo para liberar o pedido, ou se as duas
conferências deveriam valer sempre, o fonte não diz — a tela irmã lê o mesmo cadastro do
mesmo jeito. Pergunta ao site.

### RN-16 — A impressora é obrigatória

Sem a impressora informada, a tela recusa com **\* Informe a impressora \*** e não
chega a fazer a pergunta de confirmação.

### RN-17 — A tela pergunta, e só grava depois do S

Passadas todas as conferências, a tela ainda não grava nada: ela mostra
**\* Confirma inclusao automatica das notas <S/N> ? \*** e espera a resposta. Só com
**S** a requisição é registrada e entregue ao processamento em lote. Qualquer outra
resposta não grava: o pedido volta à conferência e a pergunta é feita de novo. Se
algum dado do pedido mudar entre a pergunta e a resposta, a confirmação é descartada e
a tela pergunta outra vez.

[?] A resposta N não cancela o pedido nem encerra a tela: o pedido volta à conferência
e a pergunta é repetida. O fonte não mostra outro desfecho para o N — o que ele deveria
fazer não está no acervo. Pergunta ao site.

### RN-18 — Requisição recente do mesmo relatório e da mesma coordenadoria impede outra

Na hora de gravar, a tela confere se já existe requisição deste relatório para a mesma
coordenadoria do mesmo órgão. Sendo recente, a tela avisa
**\* Relatorio em processamento. Aguarde. \*** e não registra a nova. Sendo antiga, a
tela descarta a requisição vencida e registra a nova.

[?] A comparação é entre a hora da requisição e a hora do sistema, na forma hora.minuto
tratada como número: cinco centésimos correspondem a cinco minutos dentro da mesma
hora, mas a virada de hora faz uma requisição recente parecer vencida. O intervalo
pretendido não está no fonte. Pergunta ao site.

### RN-19 — A tela grava uma requisição, e só isso

Passando por tudo, a tela grava **um** registro no cadastro de requisições: o relatório
desta tela, a impressora, o órgão, a coordenadoria, a matrícula de quem pediu, a
estação, o dia, o mês, o ano e a hora do sistema — e ele recebe um número próprio, o
seguinte ao último pedido da fila. Nenhum outro cadastro é gravado: dos **treze** que a
tela enxerga, os outros doze são só lidos, e as rotinas de gravar e de apagar que o
gerador declara para cada um deles não são executadas.

O número do processo **não** vai nesse registro: ele viaja só no bloco que a tela
entrega ao processamento em lote. E o pedido leva o meu e-mail, tirado do cadastro
funcional; não achando o cadastro, ele sai com o e-mail em branco, sem recusa.

[?] O pedido gravado não leva o número do processo. Se quem lê a fila precisa saber de
que processo é o pedido, pergunta ao site.

[?] O fonte não mostra se a criação do registro zera os campos que a tela não informa ou
se herda o que estava na área do último pedido lido — e o mesmo vale para o número do
pedido quando a fila está vazia. Pergunta ao site.

[?] Não achando o cadastro funcional do servidor, a requisição sai com o e-mail em
branco, sem recusa. Se o e-mail é exigido para a inclusão, pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Pedido de inclusão automática das notas de um processo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N116T

  Cenário: Pedido confirmado e entregue ao processamento em lote
    Dado que informei um processo válido, a coordenadoria, o tipo de contrato, o fornecedor, a fonte, o tipo de processo e a impressora
    Quando respondo S à pergunta de confirmação
    Então a requisição é registrada e entregue ao processamento em lote
    E vejo "* Cadastro sendo atualizado *"
    E a tela N116T reabre

  Cenário: A tela não grava nota nenhuma
    Dado que confirmei um pedido
    Então nenhuma nota, nenhum processo e nenhum cadastro de fornecedor ou de fonte é gravado pela tela
    Mas a inclusão das notas é feita pelo processamento em lote

  Cenário: Abrir a tela não grava nada
    Dado que abro a tela N116T pelo menu
    Então o código da secretaria, a coordenadoria regional escolar e os dígitos de controle vêm preenchidos com os da minha sessão
    E o lote, o número do processo, o tipo de contrato, o fornecedor, a fonte, o tipo de processo e a impressora vêm em branco
    E nada é gravado

  Cenário: Envio com operação diferente da inclusão
    Dado que envio a tela com uma operação que não é a inclusão
    Então vejo "* Opcao nao disponivel. Use INC *"
    E a tela não segue

  Cenário: Lote ou número do processo em branco
    Dado que deixo o código do lote ou o número central do processo em branco
    Quando envio a tela
    Então vejo "* Numero do processo invalido *"
    E nada é gravado

  Cenário: Dígitos de controle preenchidos onde o órgão não numera pela coordenadoria
    Dado que o cadastro do meu órgão não manda numerar o processo pela coordenadoria regional
    Quando informo os dois dígitos de controle
    Então vejo "* Numero do processo invalido *"

  Cenário: Código de secretaria fora dos seis do órgão
    Quando informo um código de secretaria que não é nenhum dos seis do meu órgão
    Então vejo "* Inicio do processo invalido *"
    E nada é gravado

  Cenário: Coordenadoria regional escolar não cadastrada
    Quando informo uma coordenadoria regional escolar que não está no cadastro
    Então vejo "* Grupo nao cadastrado *"

  Cenário: Coordenadoria regional escolar diferente da minha
    Dado que a minha sessão tem coordenadoria fixa
    Quando informo outra coordenadoria regional escolar
    Então vejo "* Usuario sem acesso a este grupo *"

  Cenário: Sem coordenadoria na sessão e sem coordenadoria informada
    Dado que a minha sessão não tem coordenadoria fixa
    Quando deixo a coordenadoria regional escolar em branco
    Então vejo "* Informe o grupo *"

  Cenário: Processo de outra coordenadoria
    Dado que o processo já tem nota lançada em outra coordenadoria
    Quando envio a tela
    Então vejo "* Usuario sem acesso ao grupo deste processo *"

  Cenário: Código não numérico
    Quando digito letras em um dos códigos da tela
    Então a tela recusa o campo antes de consultar qualquer cadastro
    E marca o campo para correção

  Cenário: Tipo de contrato não cadastrado
    Quando informo um tipo de contrato que não está no cadastro
    Então vejo "* Tipo de contrato nao cadastrado *"

  Cenário: Fornecedor não cadastrado
    Quando informo um fornecedor que não está no cadastro
    Então vejo "* Fornecedor nao cadastrado *"

  Cenário: Fonte com código abaixo de 1000
    Quando informo um código de fonte menor que 1000
    Então vejo "* Fonte invalida *"

  Cenário: Fonte não cadastrada
    Quando informo uma fonte que não está no cadastro
    Então vejo "* Fonte nao cadastrada *"

  Cenário: Tipo de processo não cadastrado
    Quando informo um tipo de processo que não está no cadastro
    Então vejo "* Tipo processo nao cadastrado *"

  Cenário: Processo com nota lançada traz os próprios dados
    Dado que o processo já tem nota lançada
    Quando informo o processo junto com outros dados de contrato, fornecedor, fonte e tipo de processo
    Então a tela mostra a coordenadoria, o tipo de contrato, o fornecedor, a fonte e o tipo de processo do próprio processo
    E é com esses dados que o pedido sai

  Cenário: Processo pré-liquidado
    Dado que o processo está pré-liquidado
    Quando envio a tela
    Então vejo "* Processo pre-liquidado *"
    E nada é gravado

  Cenário: Processo liquidado
    Dado que o processo está liquidado
    Quando envio a tela
    Então vejo "* Processo liquidado *"
    E nada é gravado

  Cenário: Processo pago
    Dado que o processo está pago
    Quando envio a tela
    Então vejo "* Processo pago *"
    E nada é gravado

  Cenário: Processo em integração com o SIAFIC
    Dado que o processo está em integração com o SIAFIC
    Quando envio a tela
    Então vejo "* Processo na integracao com SIAFIC *"
    E nada é gravado

  Cenário: Processo sem nota lançada não passa pelo andamento nem pela integração
    Dado que o processo não tem nota lançada
    Quando envio a tela com os demais dados válidos
    Então a tela não confere o andamento do processo nem a integração com o SIAFIC
    E o pedido segue para a pergunta de confirmação

  Cenário: Impressora não informada
    Dado que deixo a impressora em branco
    Quando envio a tela
    Então vejo "* Informe a impressora *"
    E não chego à pergunta de confirmação

  Cenário: Resposta diferente de S não grava
    Dado que a tela mostrou a pergunta de confirmação
    Quando respondo N
    Então nada é registrado
    E a pergunta é feita de novo

  Cenário: Dados alterados entre a pergunta e a resposta
    Dado que a tela mostrou a pergunta de confirmação
    Quando altero o código do lote antes de responder
    Então a confirmação é descartada
    E a tela pergunta de novo

  Cenário: Requisição recente do mesmo relatório
    Dado que já existe requisição recente deste relatório para a minha coordenadoria
    Quando confirmo um novo pedido
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E nada é registrado

  Cenário: Requisição antiga do mesmo relatório é descartada
    Dado que existe requisição antiga deste relatório para a minha coordenadoria
    Quando confirmo o pedido
    Então a requisição antiga é descartada
    E a minha requisição é registrada

  Cenário: A requisição leva a minha identificação e recebe um número próprio
    Dado que confirmei o pedido
    Então a requisição fica com a matrícula, o órgão, a coordenadoria, a estação, a data, a hora e o meu e-mail
    E recebe o número seguinte ao último registrado
    E nenhum outro cadastro é gravado
```
