# US — F030T — Pedido de impressão da relação de pagamentos por fonte

## Estória

Como **servidor de CRE**, quero **informar o mês, o ano e a fonte dos pagamentos, ver os
fornecedores que receberam por aquela fonte no período e pedir a impressão da relação**,
para que **a secretaria tenha em papel o que foi pago a cada fornecedor naquele mês, para
conferir com o que saiu do banco e prestar contas**.

A tela existe para virar do avesso o pagamento do mês: ela reúne, por fonte, os
fornecedores pagos e o quanto cada um recebeu, e é nela que se diz quais desses
fornecedores devem sair na relação impressa. Sem ela, a conferência do que foi pago no
mês ficaria sem o documento que a secretaria usa para bater com o banco, e a relação
teria de ser pedida fora do sistema.

A tela não mantém cadastro nenhum: ela lê o que já está lançado pelos outros módulos e a
única coisa que acrescenta é o pedido de impressão.

## Contexto

Jornada S000M → F000M → F030T.
Ator: servidor de CRE — informa o mês, o ano e a fonte, marca os fornecedores que devem
sair na relação, informa a impressora e confirma.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores desta jornada são menus, e menu só encaminha: a F030T não
recebe registro nem operação de quem a chamou. O contexto de que ela se serve — a
matrícula, o código de acesso, o privilégio, o tipo de órgão, a CRE e a estação da
sessão — é o que a entrada deixou, e a tela apenas o repassa às conferências. O modo de
operação também não vem de fora: é a própria tela que fixa a consulta. E a tela não abre
outra tela — ela termina a jornada —, e o que entrega adiante é o pedido que o
processamento da relação consome. As regras abaixo são só as desta tela.

---

## Regras de negócio

### RN-01 — A tela é de consulta e é assim que ela abre

A tela é de consulta, e é esse o valor com que o campo da operação chega à mão do
operador: a cada abertura a tela repõe a consulta nesse campo, e não aceita outra
operação. Operação diferente da consulta é recusada com
**\* Operacao nao disponivel. Use CON \***, com o cursor de volta ao campo da operação,
e a mensagem é abandonada antes de qualquer leitura de cadastro de negócio.

A conferência de encaminhamento, que roda antes desta guarda, também recusa por conta
própria a operação que não reconhece, com **\* Operacao nao disponivel \*** — mensagem
mais curta, sem a sugestão da consulta.

[?] O texto que o operador vê no campo da operação não está nos fontes desta jornada: a
tela compara o campo com o **código interno** da consulta, e a mensagem pede **CON**.
Se o que se digita e o que a tela compara não forem o mesmo vocabulário, quem digitar o
CON que a mensagem sugere é recusado antes, pela conferência de encaminhamento, com a
outra mensagem. O texto exato da máscara não está no lote — está no LINCFORM. Pergunta
ao site.

### RN-02 — A tela e o acesso são conferidos antes de qualquer leitura de negócio

Toda mensagem passa, antes de qualquer leitura de cadastro de negócio, por duas
conferências: a da tela e a do acesso.

A tela precisa estar no cadastro de telas — não estando, a recusa é
**\* Tela nao disponivel \***. A matrícula precisa ter esta tela no seu código de
acesso — não tendo, a recusa é **\* Acesso negado para esta matricula \***. Na
confirmação, a conferência de encaminhamento refaz a leitura do cadastro de telas e
recusa com **\* Tela nao cadastrada \*** a tela que dele foi retirada.

Se a mensagem chegar com um código de próxima tela preenchido, ela é encaminhada para
essa tela e esta abandona: a F030T não segue.

[?] A conferência do código de acesso só lê as liberações de **inclusão**, de
**alteração** e de **exclusão**, e só quando a operação é uma dessas. Como esta tela
opera em consulta e, mesmo assim, inclui um pedido, a liberação de inclusão não é
exigida de ninguém: quem tem a tela no código de acesso pede a relação, sem flag
nenhum. Se a intenção era exigir a autorização de inclusão, o caminho não a pede.
Pergunta ao site.

### RN-03 — O mês, o ano e a fonte são números

O mês de pagamento, o ano de pagamento e o código da fonte são números. Campo em branco
vira zero, o que não for número é recusado e o cursor volta ao primeiro campo recusado;
a tela não segue enquanto houver campo recusado.

[?] O que o operador vê nessa recusa — se há mensagem e qual é o texto — não está nos
fontes desta jornada: as rotinas que fazem a edição numérica e devolvem o cursor não
fazem parte do acervo lido. Pergunta ao site.

### RN-04 — Cada confirmação começa com os campos de resultado limpos

Antes de conferir qualquer coisa, a tela apaga o que mostrou na confirmação anterior: a
descrição do tipo de órgão, a data do sistema, a descrição da fonte, a razão social do
fornecedor e os valores acumulados. Nas recusas que abandonam a mensagem, o total
mostrado também é apagado. Uma confirmação recusada não deixa na tela o resultado da
anterior.

### RN-05 — O mês, o ano e a fonte são obrigatórios

O mês e o ano de pagamento são obrigatórios, e os dois têm de ser diferentes de zero:
faltando qualquer um, a recusa é **\* Informe mes/ano de Pagamento \*** e o cursor volta
ao campo do mês. Sem o código da fonte, a recusa é **\* Informe a fonte \*** e o cursor
volta ao campo da fonte. Nas duas, a conferência daquela mensagem é abandonada na hora.

[?] A recusa abandona a conferência sem marcar o estado que decide a gravação, e o
programa segue, logo depois, para a passagem que grava o pedido da linha marcada. Pelo
fonte desta jornada, a recusa não impede a gravação; se quem a impede é a rotina que
mostra a mensagem, isso não está no corpus — e as recusas de RN-06, RN-10, RN-11 e RN-12
têm a mesma forma. Pergunta ao site.

### RN-06 — A fonte tem de estar cadastrada para o tipo de órgão da sessão

O código da fonte informado é procurado no cadastro de fontes pela chave formada pelo
**tipo de órgão da sessão** e pelo próprio código. Não estando lá — ou estando marcado
como excluído —, a recusa é **\* Fonte nao cadastrada \***, com o cursor de volta ao
campo da fonte. Achando, a tela passa a mostrar a descrição da fonte.

### RN-07 — A consulta exige pagamento lançado com empenho no mês, no ano e na fonte

Se o mês, o ano e a fonte informados forem iguais aos da consulta anterior, a tela não
refaz a busca. Sendo diferentes, ela percorre os pagamentos do tipo de órgão da sessão
naquele mês, naquele ano e naquela fonte e exige encontrar pelo menos um **com número de
empenho**; não encontrando, recusa com **\* Nao existem registros cadastrados \*** e
devolve o cursor ao campo do mês.

Pagamento sem número de empenho não conta para essa conferência e também não entra na
lista.

### RN-08 — A tela lista os fornecedores pagos, com o valor acumulado e o total

Passada a conferência, a tela monta a lista dos fornecedores daquela fonte no mês e no
ano: para cada **CNPJ distinto**, a razão social do cadastro de fornecedores e o valor
acumulado dos pagamentos dele no período; e, uma vez, o total dos pagamentos daquele
mês, daquele ano e daquela fonte.

A lista guarda até **24 fornecedores**. O fornecedor que não couber nas 24 posições não
aparece na lista, mas o que foi pago a ele continua somando no total.

### RN-09 — A lista tem duas páginas de doze

A página mostra **12 fornecedores**. A tela abre na primeira página; confirmando de novo
a mesma fonte, o mesmo mês e o mesmo ano, ela passa a mostrar os fornecedores das
posições 13 a 24 — e confirmando outra vez, volta à primeira. Não havendo 13º
fornecedor, ela fica na primeira página mesmo que se confirme de novo.

### RN-10 — Só a linha marcada gera pedido, e ela tem de ter fornecedor

A tela percorre as linhas da página. Linha sem a marca **X** é ignorada: não gera pedido
nem mensagem. Linha marcada sem CNPJ é recusada com
**\* Relatorio apenas para linha preenchida \***, com o cursor de volta ao campo da
marcação daquela linha.

A marcação não fica na tela: lida a linha, a marca é apagada.

### RN-11 — A linha marcada exige a impressora

Havendo pelo menos uma linha marcada, o código da impressora é obrigatório: sem ele, a
recusa é **\* Informe a impressora \***, com o cursor no campo da impressora.

### RN-12 — Pedido da mesma relação já na fila é recusado

Antes de gravar, a tela procura na fila de requisições um pedido daquela relação para o
tipo de órgão da sessão. Havendo, recusa com
**\* Relatorio em processamento. Aguarde. \*** e devolve o cursor ao campo da impressora.

[?] A procura alcança o pedido **em qualquer situação** — a chave consultada não filtra
por situação. E, como em RN-05, a recusa abandona a conferência sem marcar a falha, de
modo que a gravação que roda em seguida não é barrada por ela. Com mais de uma linha
marcada, a conferência da linha seguinte procura a fila pela mesma chave e pode
encontrar o pedido que a linha anterior acabou de gravar — se um registro gravado na
mesma mensagem já é visível para a leitura seguinte é semântica do banco, e não está no
corpus. Pergunta ao site.

### RN-13 — O pedido recebe o número seguinte e os dados da consulta

O pedido recebe o **número seguinte** ao do último pedido da fila e leva o tipo de órgão
da sessão, o mês, o ano, a fonte, o CNPJ do fornecedor marcado, o código da impressora,
a matrícula de quem pediu, a estação, a data do pedido e a operação marcada como
**inclusão**; a situação do pedido fica em branco.

[?] A contagem parte do último pedido da fila. Se a fila estiver vazia, o número sai do
que estiver na área do registro de requisição, e o parâmetro que posiciona essa leitura
não está definido em nenhum arquivo do lote: não foi possível determinar com que número
o primeiro pedido sai. Pergunta ao site.

[?] A montagem do pedido zera o campo da CRE antes de copiá-lo para o registro, e essa
cópia só acontece quando ele **não** é zero — de modo que a CRE gravada não é a da
sessão, e sim a que já estivesse na área do registro. Se a intenção era separar os
pedidos por CRE, este caminho não separa. Pergunta ao site.

[?] O CNPJ do fornecedor é gravado no campo que, no cadastro de pagamentos, guarda o
número do processo. Se é isso mesmo que a relação usa para separar um fornecedor do
outro, ou se o campo foi reaproveitado, o acervo lido não diz. Pergunta ao site.

### RN-14 — Gravado o pedido, o processamento da relação é disparado e a fila é consumida

Gravado o pedido, a tela monta o pedido de execução da relação de pagamentos e o entrega
ao processamento. Ao rodar, a relação percorre a fila daquela relação para o tipo de
órgão e apaga os pedidos que consumiu — é assim que o pedido sai da fila.

[?] A relação apaga **todos** os pedidos daquela relação para o tipo de órgão, e não só
o pedido que ela mesma está atendendo: pedindo vários fornecedores na mesma mensagem, o
primeiro processamento que rodar tira da fila os pedidos dos demais. Se os pedidos já
disparados não dependem de continuar na fila, o efeito é nenhum. Não foi possível
determinar. Pergunta ao site.

[?] O disparo é condicionado a o estado da transação não ser um valor que a tela nunca
atribui; como a gravação deixa o estado em branco, o disparo acontece em todos os
desfechos observados. O que esse valor significa é pergunta ao site.

### RN-15 — A tela não mantém cadastro nenhum e não deixa auditoria

Nenhum cadastro de negócio é incluído, alterado ou excluído por esta tela: ela lê o
cadastro de telas, o de funcionários, o de fontes, o de fornecedores e o de pagamentos,
e escreve apenas o pedido, e só incluindo. Nenhum registro de auditoria é gerado.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedido de impressão da relação de pagamentos por fonte

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F030T

  Cenário: Consulta dos pagamentos de uma fonte no mês
    Dado que existem pagamentos da fonte informada, no mês e no ano informados, para o meu tipo de órgão
    Quando informo o mês, o ano e o código da fonte
    Então vejo a lista dos fornecedores daquela fonte, com a razão social e o valor acumulado de cada um
    E vejo o total dos pagamentos daquele mês, daquele ano e daquela fonte

  Cenário: A consulta não grava nada
    Dado que existem pagamentos da fonte informada no mês e no ano informados
    Quando informo o mês, o ano e a fonte e confirmo a tela sem marcar nenhuma linha
    Então nenhum pedido é registrado
    E nenhum cadastro de negócio é alterado

  Cenário: Pedido de impressão da relação dos fornecedores marcados
    Dado que a lista dos fornecedores da fonte está na tela
    Quando marco com X as linhas dos fornecedores que devem sair na relação
    E informo o código da impressora
    E confirmo a tela
    Então cada fornecedor marcado vira um pedido de impressão da relação
    E o pedido leva o meu órgão, a minha matrícula, a minha estação e o mês, o ano e a fonte informados
    E o processamento da relação é disparado

  Cenário: Linha sem marcação não gera pedido
    Dado que a lista dos fornecedores da fonte está na tela
    Quando confirmo a tela sem marcar nenhuma linha
    Então nenhum pedido é registrado
    E nenhum processamento é disparado

  Cenário: Linha marcada sem fornecedor
    Dado que marco com X uma linha que não tem CNPJ
    Quando confirmo a tela
    Então vejo a mensagem "* Relatorio apenas para linha preenchida *"
    E o cursor volta ao campo da marcação daquela linha

  Cenário: A marcação não fica na tela
    Dado que marquei com X uma linha da lista
    Quando confirmo a tela
    Então a marca não continua na tela

  Cenário: Linha marcada sem a impressora
    Dado que marco com X um fornecedor da lista
    E deixo o código da impressora em branco
    Quando confirmo a tela
    Então vejo a mensagem "* Informe a impressora *"
    E o cursor volta ao campo da impressora

  Cenário: Operação diferente da consulta
    Dado que informo uma operação diferente da consulta
    Quando confirmo a tela
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nada é lido nos cadastros de negócio

  Cenário: Mês ou ano de pagamento em branco
    Dado que deixo o mês ou o ano de pagamento em branco
    Quando confirmo a tela
    Então vejo a mensagem "* Informe mes/ano de Pagamento *"
    E o cursor volta ao campo do mês

  Cenário: Fonte em branco
    Dado que deixo o código da fonte em branco
    Quando confirmo a tela
    Então vejo a mensagem "* Informe a fonte *"
    E o cursor volta ao campo da fonte

  Cenário: Fonte não cadastrada para o meu tipo de órgão
    Dado que informo um código de fonte que não existe para o meu tipo de órgão
    Quando confirmo a tela
    Então vejo a mensagem "* Fonte nao cadastrada *"
    E o cursor volta ao campo da fonte

  Cenário: Fonte retirada do cadastro
    Dado que informo o código de uma fonte marcada como excluída
    Quando confirmo a tela
    Então vejo a mensagem "* Fonte nao cadastrada *"

  Cenário: Sem pagamento para o mês, o ano e a fonte
    Dado que não existe pagamento lançado para o meu tipo de órgão no mês, no ano e na fonte informados
    Quando confirmo a tela
    Então vejo a mensagem "* Nao existem registros cadastrados *"
    E o cursor volta ao campo do mês

  Cenário: Pagamento sem empenho não entra na relação
    Dado que os pagamentos do mês e da fonte só têm registros sem número de empenho
    Quando confirmo a tela
    Então vejo a mensagem "* Nao existem registros cadastrados *"
    E nenhum fornecedor aparece na lista

  Cenário: Relação já na fila
    Dado que já existe um pedido da relação de pagamentos para o meu tipo de órgão
    Quando confirmo a tela com uma linha marcada
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da impressora

  Cenário: A página mostra doze fornecedores
    Dado que a fonte tem mais de 12 fornecedores no mês e no ano informados
    Quando confirmo a tela
    Então a página mostra 12 fornecedores

  Cenário: A segunda página da lista
    Dado que a fonte tem mais de 12 fornecedores no mês e no ano informados
    E a primeira página da lista está na tela
    Quando confirmo a tela de novo com a mesma fonte, o mesmo mês e o mesmo ano
    Então vejo os fornecedores seguintes
    E confirmando outra vez, volto à primeira página

  Cenário: O total soma os fornecedores que não cabem na lista
    Dado que a fonte tem mais de 24 fornecedores no mês e no ano informados
    Quando confirmo a tela
    Então o total mostrado soma também o que foi pago aos fornecedores que não aparecem na lista

  Cenário: Digitação que não é número
    Dado que digito, no mês, no ano ou no código da fonte, algo que não é número
    Quando confirmo a tela
    Então o cursor volta ao primeiro campo recusado
    E a tela não segue

  Cenário: Cada confirmação limpa os campos de resultado
    Dado que a tela já mostrou a descrição da fonte, a razão social e os valores da consulta anterior
    Quando confirmo a tela
    Então esses campos não continuam na tela

  Cenário: Tela não cadastrada
    Dado que a tela F030T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo pedir relação nenhuma

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela F030T no seu código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo pedir relação nenhuma

  Cenário: Tela retirada do cadastro
    Dado que a tela F030T foi retirada do cadastro de telas
    Quando confirmo a tela
    Então vejo a mensagem "* Tela nao cadastrada *"

  Cenário: Próxima tela informada
    Dado que a mensagem chega com um código de próxima tela preenchido
    Quando confirmo a tela
    Então a mensagem é encaminhada para a tela informada
    E a F030T abandona

  Cenário: O pedido sai da fila quando a relação roda
    Dado que registrei o pedido de impressão da relação
    Quando a relação é processada
    Então ela apaga os pedidos daquela relação para o meu tipo de órgão

  Cenário: A tela não mantém cadastro e não deixa auditoria
    Dado que registro um pedido de impressão
    Então nenhum cadastro de negócio é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado
```
