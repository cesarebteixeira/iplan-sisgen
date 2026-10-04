# US — C025T — Manutenção das unidades orçamentárias

## Estória

Como **servidor da CRE**, quero **manter o cadastro das unidades orçamentárias da
secretaria** — consultando, incluindo, alterando e excluindo unidades —, para que
grupos de atendimento e contratos da secretaria fiquem sempre presos a uma unidade
orçamentária existente.

A unidade orçamentária é a classificação a que o gasto da secretaria se amarra: é
por ela que grupos e contratos se referenciam. Por isso a exclusão é recusada
enquanto houver grupo ou contrato na unidade, e a consulta é somente leitura —
percorrer a tela para conferir o cadastro não pode mexer nele.

## Contexto

Jornada S000M → C000M → C015M → C025T.

Ator: servidor de CRE — mantém o cadastro das unidades orçamentárias.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas do meio do caminho são menus: não deixam nada de próprio para a tela
de destino, apenas dizem qual tela abrir. O que a C025T usa da sessão — a matrícula,
o acesso, a CRE, o tipo de órgão e o privilégio, mais a descrição da secretaria e a
data do sistema que ela mostra no cabeçalho — foi deixado pela entrada.

A tela não encadeia para nenhuma outra: não passa registro nem operação adiante, e a
jornada termina nela.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O cadastro que a tela mantém é o das unidades orçamentárias

A unidade orçamentária é feita de um **código de 8 dígitos** — a chave do cadastro —
e de uma **descrição de 40 caracteres**, de preenchimento obrigatório. O cadastro
comporta **1.500.000** unidades; capacidade declarada é o máximo esperado, parâmetro
de dimensionamento, e não o volume já cadastrado.

[?] No dicionário, a chave do cadastro admite códigos repetidos, mas a tela recusa a
inclusão de unidade já cadastrada: a chave aceita duplicata neste dialeto? Pergunta
ao site.

### RN-02 — Só o código passa pela conferência numérica

Antes de qualquer consulta, o sistema confere o **código**: em branco vale zero, os
separadores de milhar caem e o que não for número é recusado, com o cursor de volta
no campo do código. A descrição e a ação da linha **não** passam por conferência
nenhuma: chegam ao cadastro como o servidor as digitou.

[?] O texto exato da recusa por código não numérico não está no lote: a conferência
é feita por rotina padrão de edição numérica, e a mensagem que o terminal mostra sai
da rotina de comunicação, fora dos fontes fornecidos.

### RN-03 — A página tem 15 linhas, com código, descrição e ação

A página mostra **15 linhas**, e cada linha tem **três dados**: o código, a descrição
e a ação. Ao abrir, o sistema lê o cadastro e vai preenchendo as linhas, uma a uma,
em ordem de código, com o código e a descrição que leu. Numa linha em branco da página
o servidor digita o código e a descrição de uma unidade nova; numa linha já
preenchida, digita a descrição nova, quando for alterar.

### RN-04 — O modo da página só admite ALT ou CON

A página tem um campo próprio de modo, e ele aceita **alteração** ou **consulta** —
os mesmos que a mensagem de recusa nomeia como **ALT** e **CON**. Qualquer outro
valor é recusado com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de
volta no campo do modo, e nada é gravado.

[?] A mensagem manda usar ALT ou CON, mas o teste da tela é feito contra os códigos
internos de alteração e de consulta: se o campo recebe exatamente o que a mensagem
manda digitar, a alteração seria recusada. O lote mostra o teste, não a tradução que
a camada de apresentação faria. Pergunta ao site.

### RN-05 — A abertura: consulta, do começo do cadastro, e o aviso quando não há unidade

Ao abrir pela primeira vez na sessão, a tela assume **consulta** e começa pelo começo
do cadastro, do código zero. Se não houver nenhuma unidade orçamentária cadastrada, o
sistema não deixa seguir e avisa **\* Nao existem un.orcamentarias cadastradas \***,
com o cursor no campo do código. No cabeçalho a tela mostra a descrição da secretaria
e a data do sistema, que vêm da sessão.

### RN-06 — A tela reabre no modo e na unidade da última passagem

O modo usado e o último código lido ficam guardados na área de trabalho da sessão.
Reabrindo a tela, ela volta no mesmo modo — alteração, se foi o último — e apontada
para a unidade que a última leitura deixou, e não do começo do cadastro.

### RN-07 — Linha sem código ou com ação desconhecida é ignorada

Só três ações operam uma linha: **I** inclui, **A** altera e **E** exclui. Linha com
o código zerado, ou com ação em branco ou fora dessas três, passa em silêncio: não
gera recusa e não grava nada.

### RN-08 — Cada linha é autorizada pela operação que ela pede

A ação da linha é traduzida para a operação correspondente — inclusão, alteração ou
exclusão — e é essa operação que a autorização do servidor confere, no cadastro de
telas por código de acesso, que guarda, por operação, se ela está liberada. Sem a
marca da operação, a linha não é validada nem gravada, e a tela volta. Antes de
gravar, a tela ainda confere a tela na relação de telas do sistema, a rota do módulo
e a estação da sessão; sem qualquer uma dessas conferências, nada é validado nem
gravado.

### RN-09 — Inclusão recusa unidade já cadastrada

Na ação **I**, o sistema lê a unidade pelo código digitado: achando, recusa a
inclusão com **\* Unidade orcamentaria ja cadastrada \*** e devolve o cursor à coluna
da ação da linha.

[?] A recusa da linha não é reconferida pela passagem que grava — a passagem de
conferência marca a recusa em um indicador próprio e a de gravação decide apenas pelo
modo da página e pela ação da linha. O lote não traz a rotina de comunicação nem o
controle de cópias da página, então não dá para afirmar se, numa página com mais de
uma linha, a recusa de uma impede a gravação das outras. Pergunta ao site.

### RN-10 — Inclusão e alteração exigem a descrição

Nas ações **I** e **A**, descrição em branco é recusada com **\* Informe a descricao
\***, com o cursor de volta no campo da descrição. É a mesma exigência que o cadastro
faz: a descrição é o único dado obrigatório da unidade orçamentária.

### RN-11 — Alteração e exclusão exigem unidade cadastrada

Nas ações **A** e **E**, a unidade tem de existir no cadastro. Não achando pelo
código, a recusa é **\* Unidade orcamentaria nao cadastrada \***, com o cursor na
coluna da ação.

### RN-12 — Inclusão cria a unidade no cadastro

Passadas as conferências, a ação **I** cria a unidade no cadastro, com o código e a
descrição informados, e deixa o rastro na auditoria.

### RN-13 — Alteração troca a descrição da unidade

A ação **A** lê a unidade, guarda o registro anterior e o novo, trava o registro,
substitui a descrição pela informada e grava. O código não muda: ele é a chave da
unidade.

### RN-14 — Exclusão é recusada enquanto houver grupo na unidade

Na ação **E**, antes de apagar, o sistema percorre o cadastro de grupos procurando
algum registro com o mesmo código de unidade. Achando, recusa com **\* Nao exclua.
Grupo nesta unid.orcamentaria \***, com o cursor na coluna da ação, e a unidade
continua cadastrada.

[?] A guarda do grupo percorre o cadastro um registro por vez comparando o código da
unidade, porque a chave desse cadastro é o tipo de órgão com a CRE e não contém o
código da unidade. O lote não documenta o posicionamento dessa leitura: não dá para
afirmar se a varredura alcança o cadastro inteiro ou só a parte da chave do servidor
— e, se for só a parte, um grupo de outra secretaria não bloquearia a exclusão.
Pergunta ao site.

[?] A mensagem chama o cadastro de "grupo", mas os campos dele são a CRE e uma
descrição: "grupo" é o conjunto das CREs da unidade orçamentária? Pergunta ao site.

### RN-15 — Exclusão é recusada enquanto houver contrato na unidade

A mesma varredura é feita no cadastro de contratos: havendo contrato com o mesmo
código de unidade, a recusa é **\* Nao exclua. Contrato nesta unid.orcamentaria \***,
com o cursor na coluna da ação, e a unidade continua cadastrada.

[?] Vale para os contratos a mesma dúvida da RN-14: a chave desse cadastro é o tipo
de órgão com o tipo de contrato, e o lote não documenta o posicionamento da leitura —
não dá para afirmar se a varredura cobre o cadastro inteiro. Pergunta ao site.

### RN-16 — Exclusão confirmada apaga a unidade

Passadas as guardas, a ação **E** trava o registro e o apaga do cadastro, deixando o
rastro na auditoria.

### RN-17 — A consulta não grava nada

No modo consulta, a passagem que grava é abandonada antes de qualquer operação, e a
passagem de conferência sai antes das peneiras da linha: nenhuma unidade é incluída,
alterada ou excluída. É a garantia de que a consulta é somente leitura.

### RN-18 — Toda gravação deixa rastro na auditoria

Cada inclusão, alteração e exclusão confirmadas gravam um registro de auditoria com o
objeto auditado (a unidade orçamentária), a operação, o **valor anterior** e o
**posterior** e o contexto da sessão — matrícula, secretaria, CRE, estação, data e
hora da sessão e número do processo. Na inclusão o valor anterior vai vazio; na
exclusão, o posterior. O valor auditado é o par código e descrição da unidade.

### RN-19 — A recusa de destino inválido não é alcançável por esta tela

A recusa de **destino inválido** — a distribuição automática entre destinos —, que a
ficha estrutural lista entre as mensagens desta tela, não é alcançável por ela: o
modo de distribuição automática é limpo imediatamente antes dos dois únicos pontos em
que a recusa poderia disparar.

[?] A ficha do grafo lista essa recusa para esta tela, e o programa limpa o campo
antes de usá-lo: divergência entre a ficha e o comportamento, a confirmar com quem
mantém o grafo.

### RN-20 — Chegando com a tela de retorno preenchida, a manutenção é abandonada

Se a transação chegar com a indicação de **tela de retorno** preenchida — o dado que
a rota usa para devolver o servidor a outra tela —, a manutenção é abandonada: nada é
validado, nada é gravado e o servidor é levado à tela indicada.

[?] Nada nesta jornada preenche essa indicação, e o lote não diz quem a preenche nem
para onde ela levaria. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manutenção das unidades orçamentárias

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, o acesso, a CRE e o tipo de órgão
    E tenho acesso à tela C025T

  Cenário: O cadastro mantém a unidade orçamentária pelo código e pela descrição
    Dado que estou na tela C025T
    Quando consulto uma unidade orçamentária
    Então vejo o seu código de 8 dígitos e a sua descrição de 40 caracteres
    E o cadastro comporta até 1.500.000 unidades

  Cenário: Só o código passa pela conferência numérica
    Dado que estou na tela C025T
    Quando informo no código algo que não é número
    Então o sistema recusa e o cursor volta ao campo do código
    E a descrição e a ação que digitei não são conferidas

  Cenário: A página tem 15 linhas preenchidas com o cadastro
    Dado que estou na tela C025T
    Quando a página é apresentada
    Então vejo 15 linhas, cada uma com código, descrição e ação
    E as linhas já cadastradas vêm preenchidas pelo sistema, em ordem de código

  Cenário: O modo da página só admite ALT ou CON
    Dado que estou na tela C025T
    Quando informo um modo diferente de alteração e de consulta
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: A abertura assume consulta e avisa quando não há unidade cadastrada
    Dado que estou abrindo a tela C025T pela primeira vez na sessão
    Quando o cadastro não tem nenhuma unidade orçamentária
    Então a tela abre em consulta, começando pelo começo do cadastro
    E vejo "* Nao existem un.orcamentarias cadastradas *", com o cursor no código
    E nada é gravado

  Cenário: A tela reabre no modo e na unidade da última passagem
    Dado que passei pela tela C025T em alteração, sobre uma unidade
    Quando volto a abrir a tela
    Então ela reabre em alteração
    E apontada para a unidade que a última leitura deixou

  Cenário: Linha sem código ou com ação desconhecida é ignorada
    Dado que estou na tela C025T no modo ALT
    Quando deixo o código em branco, ou informo uma ação diferente de I, A e E
    Então a linha não é validada
    E nada é gravado para ela

  Cenário: Cada linha é autorizada pela operação que ela pede
    Dado que estou na tela C025T no modo ALT
    E que a minha autorização não libera a operação pedida na linha
    Quando confirmo a linha
    Então a linha não é validada e nada é gravado
    E a tela volta

  Cenário: Inclusão recusa unidade já cadastrada
    Dado que estou na tela C025T no modo ALT
    E que a unidade do código informado já está cadastrada
    Quando confirmo a ação I
    Então vejo "* Unidade orcamentaria ja cadastrada *"
    E o cursor fica na coluna da ação
    E nada é gravado

  Cenário: Inclusão e alteração exigem a descrição
    Dado que estou na tela C025T no modo ALT
    Quando confirmo a ação I ou a ação A com a descrição em branco
    Então vejo "* Informe a descricao *"
    E o cursor fica no campo da descrição
    E nada é gravado

  Cenário: Alteração e exclusão exigem unidade cadastrada
    Dado que estou na tela C025T no modo ALT
    Quando confirmo a ação A ou a ação E para uma unidade que não existe
    Então vejo "* Unidade orcamentaria nao cadastrada *"
    E o cursor fica na coluna da ação
    E nada é gravado

  Cenário: Inclusão cria a unidade no cadastro
    Dado que estou na tela C025T no modo ALT
    E que a unidade ainda não existe
    Quando informo o código, a descrição e a ação I
    Então a unidade é criada no cadastro
    E a inclusão fica registrada na auditoria com o valor posterior

  Cenário: Alteração troca a descrição da unidade
    Dado que estou na tela C025T no modo ALT
    E que a unidade está cadastrada
    Quando informo a nova descrição e a ação A
    Então a descrição da unidade é gravada
    E a alteração fica registrada na auditoria com o valor anterior e o posterior

  Cenário: A exclusão é bloqueada por grupo na unidade orçamentária
    Dado que estou na tela C025T no modo ALT
    E que a unidade está cadastrada e tem grupo vinculado a ela
    Quando confirmo a ação E
    Então vejo "* Nao exclua. Grupo nesta unid.orcamentaria *"
    E o cursor fica na coluna da ação
    E a unidade continua cadastrada

  Cenário: A exclusão é bloqueada por contrato na unidade orçamentária
    Dado que estou na tela C025T no modo ALT
    E que a unidade está cadastrada e tem contrato vinculado a ela
    Quando confirmo a ação E
    Então vejo "* Nao exclua. Contrato nesta unid.orcamentaria *"
    E o cursor fica na coluna da ação
    E a unidade continua cadastrada

  Cenário: A exclusão confirmada apaga a unidade
    Dado que estou na tela C025T no modo ALT
    E que a unidade está cadastrada, sem grupo e sem contrato
    Quando confirmo a ação E
    Então a unidade é excluída do cadastro
    E a exclusão fica registrada na auditoria com o valor anterior

  Cenário: A consulta não grava nada
    Dado que estou na tela C025T no modo CON
    Quando percorro e confirmo as linhas da página
    Então nenhuma unidade é incluída, alterada ou excluída

  Cenário: Toda gravação deixa rastro na auditoria
    Dado que confirmei uma inclusão, uma alteração ou uma exclusão na C025T
    Quando a gravação termina
    Então existe um registro de auditoria da unidade orçamentária
    E com a operação, o valor anterior e o valor posterior
    E com a matrícula, a secretaria, a CRE, a estação, a data e a hora da sessão
    E com o número do processo

  Cenário: A tela não apresenta a recusa de destino inválido
    Dado que estou na tela C025T no modo ALT e confirmei uma inclusão
    Quando a gravação é preparada
    Então o sistema limpa o modo de distribuição automática
    E a recusa de destino inválido não é apresentada

  Cenário: A tela de retorno preenchida abandona a manutenção
    Dado que a transação chega à C025T com a indicação de tela de retorno preenchida
    Quando a manutenção começaria
    Então o processamento é abandonado e nada é gravado
    E o servidor é levado à tela indicada
```
