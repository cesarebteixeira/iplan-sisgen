# US — F220T — Consultar a nota fiscal e a sua composição de agricultores

## Estória

Como **servidor de CRE**, quero **consultar uma nota fiscal de pedido acumulado e ver
a que agricultores ela foi atribuída, com o valor de cada um**, para que **a secretaria
possa conferir como a nota foi repartida entre os agricultores e em que ponto do
processo o pedido está**.

A nota fiscal é lançada contra um fornecedor e repartida entre os agricultores que a
compõem; é esta tela que mostra essa repartição, agricultor por agricultor, com o
valor atribuído a cada CPF. Sem ela, ninguém conseguiria dizer de quem é a parcela da
nota, nem acompanhar a situação do pedido que a originou. A tela é só de consulta: não
inclui, não corrige e não exclui nada.

## Contexto

Jornada S000M → F000M → F200M → F220T.

Ator: servidor de CRE — informa a identificação de uma nota fiscal (número, ano,
fornecedor, sub-classe e gênero), consulta os dados da nota e a relação dos
agricultores que a compõem.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os dois menus da jornada só encaminham: não deixam dado de negócio nenhum para a
`F220T`. O contexto de que a tela se serve — matrícula, código de acesso, privilégio,
tipo de órgão, CRE e estação da sessão — é o que a entrada deixou na sessão, e a tela
apenas o repassa às conferências de acesso; essas conferências são da entrada e estão
no anexo de evidências, não aqui. Desse contexto, dois valores entram na regra de
negócio desta tela: o **tipo de órgão** da sessão faz parte da identificação da nota, e
a **CRE** da sessão limita quais notas o servidor pode ver (RN-13). A tela não encadeia
para nenhuma outra: ela é o fim da jornada, e não entrega registro nem operação a tela
seguinte. As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A consulta é a única operação da tela

A tela só atende a consulta. Escolhida qualquer outra operação, o sistema recusa com
**\* Operacao nao disponivel. Use CON \***, devolve o cursor ao campo da operação e
abandona a mensagem: nada é mostrado e nada é gravado. Ao ser aberta, a tela repõe
como consulta a operação guardada na sessão.

[?] A operação da mensagem é conferida três vezes no caminho, e só a última é a que
aparece nesta regra: antes dela, a rotina de rota da entrada recusa a operação que não
seja inclusão, alteração, exclusão ou consulta com **\* Operacao nao disponivel \***, e
a conferência de acesso da entrada pode recusá-la com a mensagem de acesso negado. Qual
das três o operador vê depende de valores do runtime que o acervo lido não define. Se a
intenção era sempre mostrar a mensagem da tela, a ordem das conferências não é essa.
Pergunta ao site.

### RN-02 — Cada mensagem começa com os campos de resultado limpos

Antes de conferir o que o operador digitou, a tela apaga doze campos de resultado: a
descrição do órgão da sessão, a data do sistema, a situação da nota, a descrição do
modelo, o indicador de nota acumulada, a razão social do fornecedor, o nome do órgão,
a descrição da fonte, a descrição resumida do gênero, o valor unitário do item, o
rótulo do processo (ou do lote) e o nome do agricultor. Uma mensagem recusada,
portanto, não deixa na tela o resultado da mensagem anterior.

### RN-03 — Os campos digitados passam pela edição numérica

Os dezessete campos numéricos da tela passam pela edição numérica: o que estiver em
branco vira zero e o que não for número é recusado, com o cursor devolvido ao campo
recusado quando a tela conhece a posição dele. Os dois campos de valor — o total da
nota e o valor de cada agricultor — são conferidos como número com duas casas
decimais.

[?] O que o operador vê quando a digitação é recusada não está nos fontes desta
jornada: a rotina que faz essa edição não faz parte do acervo lido. Pergunta ao site.

[?] Só oito dos dezessete campos têm posição de cursor registrada na tela; nos outros
nove, a recusa da edição numérica não devolve o cursor. Se todos deveriam devolvê-lo,
a lista está incompleta. Pergunta ao site.

### RN-04 — A tela repõe a última nota consultada

Enquanto a tela continuar em uso, ela guarda a identificação e os dados da última nota
consultada. Ao ser aberta de novo, os campos aparecem preenchidos com aquela nota e a
relação dos agricultores é mostrada outra vez, sem que o operador precise redigitá-la.
Na primeira mensagem, quando ainda não há nota guardada, os campos ficam como o
operador os deixou e o campo da operação é reposto como consulta.

[?] A área em que a tela guarda a última nota é comum ao programa, e o acervo não diz
se ela é da sessão do servidor ou compartilhada entre terminais. Se for compartilhada,
a nota de um operador pode reaparecer na tela de outro. Pergunta ao site.

### RN-05 — Repetir a mesma nota não refaz a leitura

Enviada de novo exatamente a mesma identificação de nota — número, ano, fornecedor,
sub-classe e gênero —, a tela não consulta os cadastros outra vez: ela reaproveita o
que guardou e responde com os mesmos dados, sem aviso nenhum. Os dados da nota que
vieram do que ficou guardado continuam como estavam.

### RN-06 — O número e o ano da nota são obrigatórios

A nota é identificada pelo número, pelo ano de emissão, pelo fornecedor, pela
sub-classe e pelo gênero. O número é obrigatório: em branco — ou zerado — o sistema
recusa com **\* Informe o numero da nota fiscal \***, devolve o cursor ao campo e não
lê cadastro nenhum. O ano também é obrigatório: em branco, a recusa é
**\* Informe o ano de entrega da nota fiscal \***, no mesmo campo do ano.

A obrigatoriedade só é conferida quando a identificação informada difere, em algum dos
cinco dados, da que a tela guardou da mensagem anterior (RN-05). Por isso uma mensagem
inteiramente em branco logo depois de outra igual — inclusive a primeira mensagem da
tela, quando ainda não há nada guardado — não produz recusa nem leitura: a tela fica
como está, sem avisar nada.

[?] O aviso do ano chama o campo de "ano de entrega", mas o campo em que ele aparece é
o do ano de emissão da nota, e a tela tem outro campo, separado, para o ano da
entrega. Se a mensagem deveria citar o ano de emissão, o texto não é esse. Pergunta ao
site.

### RN-07 — O dia e o mês de emissão não localizam a nota

O dia e o mês de emissão existem na tela e passam pela edição numérica, mas não entram
na localização da nota: a tela procura a nota pelo número, pelo ano, pelo fornecedor,
pela sub-classe e pelo gênero, dentro do tipo de órgão da sessão. O dia e o mês que a
tela mostra são os que vêm da nota encontrada, não os que o operador digitou.

[?] A procura no cadastro das notas ligadas a processo fixa o dia e o mês em zero, o
que sugere que esse cadastro guarda só o ano; se houver nota com dia e mês
preenchidos nesse cadastro, ela não seria encontrada por esse caminho, e a tela não
avisa. O acervo não permite decidir. Pergunta ao site.

### RN-08 — O fornecedor tem de estar cadastrado e em uso

O fornecedor informado tem de estar no cadastro de fornecedores e não pode estar
marcado como excluído. Não estando — ou estando excluído — a recusa é
**\* Fornecedor nao cadastrado \***, com o cursor de volta ao campo do fornecedor.
Achado o fornecedor, a tela mostra a razão social dele.

### RN-09 — A sub-classe é obrigatória e o gênero tem de estar cadastrado

A sub-classe é obrigatória: em branco, a recusa é **\* Informe o genero \***, com o
cursor no campo da sub-classe. Informada, a combinação da sub-classe com o gênero tem
de estar no cadastro de gêneros, para o ano informado; não estando, a recusa é
**\* Genero nao cadastrado \***, no mesmo campo. Achado o gênero, a tela mostra a
descrição resumida dele.

[?] O aviso de campo em branco fala em gênero, mas o campo que a tela exige é o da
sub-classe, e o gênero é outro campo. Se o aviso deveria citar a sub-classe, o texto
não é esse. Pergunta ao site.

[?] A procura do gênero leva o ano da nota e deixa o mês e o dia de início da vigência
em branco, e a chave do cadastro de gêneros tem as três partes. O acervo lido não diz o
que a leitura casa da chave — se basta o ano ou se o mês e o dia também contam —, de
modo que não dá para afirmar se um gênero com vigência iniciada em outro mês seria
encontrado. Pergunta ao site.

### RN-10 — A nota é procurada em dois cadastros

A nota fiscal é procurada primeiro no cadastro das notas ligadas a processo e, não a
achando lá, no cadastro das notas ligadas a lote. Não achada em nenhum dos dois, a
recusa é **\* Nota fiscal nao cadastrada \***, com o cursor de volta ao campo do
número da nota. O cadastro em que a nota foi achada decide como o número do processo
aparece na tela: com o rótulo **Processo** ou com o rótulo **Lote**.

[?] O acervo não diz o que distingue os dois cadastros de nota além disso, nem se toda
nota deveria existir nos dois. Pergunta ao site.

### RN-11 — O gênero tem de constar da nota

A nota encontrada tem de ter o gênero informado: se a nota não tiver item naquela
combinação de sub-classe e gênero, a recusa é **\* Genero nao cadastrado nesta nota \***,
com o cursor de volta ao campo da sub-classe.

### RN-12 — A nota tem de ser de pedido acumulado

A nota só é mostrada se o pedido dela for um pedido acumulado. Não sendo, a recusa é
**\* Nota nao e de pedido acumulado \***, com o cursor de volta ao campo do número da
nota.

[?] A tela não distingue o pedido que não é acumulado do pedido que não está
cadastrado: nos dois casos o aviso é o mesmo, e no segundo a tela segue com os dados
que estiverem no registro do pedido. Se o pedido ausente deveria ter aviso próprio,
ele não existe neste fonte. Pergunta ao site.

### RN-13 — O servidor só consulta nota da sua CRE

A consulta é limitada à CRE do servidor. Se a sessão tem uma CRE e a nota é de outra,
a recusa é **\* Usuario sem acesso a outro grupo \***, com o cursor de volta ao campo
do número da nota, e a nota não é mostrada. Quando a sessão não tem CRE, a tela não
faz essa conferência.

### RN-14 — A tela completa a nota com os cadastros

Achada a nota, a tela mostra, além da identificação informada, a razão social do
fornecedor, o nome do órgão, a descrição da fonte, a descrição resumida do gênero, a
descrição do modelo, a CRE da nota, o número do pedido, o ano da entrega, o tipo de
contrato, o número do processo (ou do lote), o valor total da nota e o valor unitário
do item. O que o operador houver digitado nesses campos é substituído pelo que vem do
cadastro.

[?] A tela lê o nome do operador do pedido, mas nenhum campo de exibição recebe esse
nome: ele fica só na área de trabalho. Se ele deveria aparecer, o layout não o mostra.
Pergunta ao site.

### RN-15 — A tela mostra a situação da nota

A nota achada no cadastro das notas ligadas a lote aparece sempre como **Fechada**. A
nota achada no cadastro das notas ligadas a processo mostra **Fechada** enquanto não
estiver marcada nesse cadastro para seguir o processamento do pedido; marcada, a tela
procura o processamento e mostra **Pre Liq** para o processo pré-liquidado,
**Liquida** para o liquidado e **Paga** para qualquer outro.

[?] Qualquer estágio do processamento que não seja o pré-liquidado nem o liquidado
aparece como **Paga**. O acervo não traz a lista dos estágios possíveis, e não permite
decidir se "Paga" é mesmo o nome certo para todo o resto. Pergunta ao site.

### RN-16 — A tela mostra a composição da nota, de 9 em 9

A composição da nota é mostrada em até nove linhas por mensagem; em cada linha, o CPF
do agricultor, o nome dele e o valor que lhe foi atribuído na nota. Quando há mais
agricultores do que cabem numa mensagem, a tela guarda o CPF do último agricultor
mostrado e a mensagem seguinte retoma a relação a partir dele.

[?] O acervo não deixa decidir se a retomada relê a última linha mostrada ou começa na
seguinte; se a listagem puder repetir ou pular um agricultor, é pergunta ao site.

### RN-17 — Nota sem composição de agricultores

Quando a nota existe mas não tem nenhum agricultor atribuído a ela, a tela avisa
**\* Nota fiscal sem composicao de agricultores \*** e não mostra linha nenhuma.

### RN-18 — A consulta não grava nada

A consulta não grava, não corrige e não exclui nada, e não deixa registro de
auditoria: é uma tela de leitura. Nenhum cadastro de negócio é alterado por ela, em
nenhum caminho — ainda que o programa traga declaradas as operações de gravar e de
apagar dos quinze cadastros que enxerga, porque declarar não é executar: nenhuma delas
é chamada por caminho nenhum.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar a nota fiscal e a sua composição de agricultores

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F220T

  Cenário: Consulta de uma nota fiscal com composição de agricultores
    Dado que a nota informada está cadastrada e é de um pedido acumulado
    E o fornecedor informado está cadastrado
    E o gênero informado está cadastrado e consta da nota
    Quando envio a consulta
    Então vejo os dados da nota, a razão social do fornecedor e o nome do órgão
    E vejo, em cada linha, o CPF do agricultor, o nome dele e o valor que lhe foi atribuído

  Cenário: Nota com mais agricultores do que cabem numa mensagem
    Dado que a nota informada tem mais de nove agricultores
    Quando envio a consulta
    Então vejo nove agricultores
    E a tela guarda o CPF do último agricultor mostrado
    E a mensagem seguinte continua a relação a partir dele

  Cenário: Nota de lote mostra a situação fechada
    Dado que a nota informada está no cadastro das notas ligadas a lote
    Quando envio a consulta
    Então a situação mostrada é "Fechada"

  Cenário: Nota de processo com processamento
    Dado que a nota informada está no cadastro das notas ligadas a processo
    E ela está marcada para seguir o processamento do pedido
    Quando envio a consulta
    Então vejo a situação "Pre Liq", "Liquida" ou "Paga", conforme o estágio do processamento

  Cenário: Nota de processo sem marca de processamento
    Dado que a nota informada está no cadastro das notas ligadas a processo
    E ela não está marcada para seguir o processamento do pedido
    Quando envio a consulta
    Então a situação mostrada é "Fechada"

  Cenário: Nota sem composição de agricultores
    Dado que a nota informada existe e não tem agricultores atribuídos
    Quando envio a consulta
    Então vejo a mensagem "* Nota fiscal sem composicao de agricultores *"

  Cenário: A consulta não grava nada
    Dado que a nota informada está cadastrada e é de um pedido acumulado
    Quando envio a consulta
    Então nenhum cadastro é incluído, corrigido ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Operação diferente de consulta
    Dado que estou na tela F220T
    Quando informo uma operação que não é a consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nada é mostrado nem gravado

  Cenário: Número da nota em branco
    Dado que a tela já mostrou uma nota fiscal
    E deixo o número da nota fiscal em branco na mensagem seguinte
    Quando envio a consulta
    Então vejo a mensagem "* Informe o numero da nota fiscal *"
    E o cursor volta ao campo do número
    E nada é lido

  Cenário: Ano da nota em branco
    Dado que a tela já mostrou uma nota fiscal
    E informo um número de nota diferente e deixo o ano em branco
    Quando envio a consulta
    Então vejo a mensagem "* Informe o ano de entrega da nota fiscal *"
    E o cursor volta ao campo do ano
    E nada é lido

  Cenário: Mensagem em branco que repete a identificação guardada
    Dado que a tela acabou de abrir e nenhuma nota foi mostrada ainda
    Quando envio a consulta sem informar nada
    Então nenhuma mensagem de recusa aparece
    E nenhum cadastro é lido

  Cenário: Fornecedor não cadastrado
    Dado que informo um fornecedor que não está no cadastro de fornecedores
    Quando envio a consulta
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo do fornecedor
    E nada é mostrado

  Cenário: Fornecedor marcado como excluído
    Dado que informo um fornecedor que está marcado como excluído
    Quando envio a consulta
    Então vejo a mensagem "* Fornecedor nao cadastrado *"

  Cenário: Sub-classe em branco
    Dado que informo número, ano e fornecedor e deixo a sub-classe em branco
    Quando envio a consulta
    Então vejo a mensagem "* Informe o genero *"
    E o cursor volta ao campo da sub-classe

  Cenário: Gênero não cadastrado
    Dado que informo uma sub-classe e um gênero que não estão no cadastro de gêneros
    Quando envio a consulta
    Então vejo a mensagem "* Genero nao cadastrado *"
    E o cursor volta ao campo da sub-classe

  Cenário: Nota fiscal não cadastrada
    Dado que a nota informada não está em nenhum dos cadastros de nota
    Quando envio a consulta
    Então vejo a mensagem "* Nota fiscal nao cadastrada *"
    E o cursor volta ao campo do número da nota

  Cenário: Gênero que não consta da nota
    Dado que a nota informada não tem item na sub-classe e no gênero informados
    Quando envio a consulta
    Então vejo a mensagem "* Genero nao cadastrado nesta nota *"
    E o cursor volta ao campo da sub-classe

  Cenário: Nota que não é de pedido acumulado
    Dado que a nota informada é de um pedido que não é acumulado
    Quando envio a consulta
    Então vejo a mensagem "* Nota nao e de pedido acumulado *"
    E o cursor volta ao campo do número da nota

  Cenário: Nota de outra CRE
    Dado que a minha sessão tem uma CRE
    E a nota informada é de outra CRE
    Quando envio a consulta
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo do número da nota
    E a nota não é mostrada

  Cenário: Dia e mês digitados não mudam a nota encontrada
    Dado que informo a identificação de uma nota cadastrada
    Quando troco só o dia e o mês de emissão e envio a consulta
    Então a tela mostra a mesma nota
    E o dia e o mês mostrados são os da nota, não os que digitei

  Cenário: Reenviar a mesma nota não refaz a leitura
    Dado que consultei uma nota cadastrada
    Quando envio de novo a mesma identificação
    Então a tela responde com os mesmos dados
    E nenhum cadastro é consultado de novo

  Cenário: A tela repõe a última nota consultada
    Dado que consultei uma nota cadastrada
    Quando abro a tela F220T de novo
    Então os campos aparecem preenchidos com aquela nota
    E a composição de agricultores é mostrada outra vez

  Cenário: Campo digitado que não é número
    Dado que digito um valor que não é número em um dos campos numéricos
    Quando envio a consulta
    Então a tela recusa a digitação
    E a mensagem não é processada

  Cenário: A mensagem começa com os campos de resultado limpos
    Dado que a mensagem anterior mostrou a razão social de um fornecedor
    Quando envio uma mensagem que é recusada
    Então a razão social da mensagem anterior não fica na tela
```
