# US — C060T — Manter os gêneros das permissões de contrato da coordenadoria regional

## Estória

Como **servidor de CRE**, quero **manter os gêneros de cada permissão de contrato da
minha coordenadoria regional, com a quantidade, o desconto ou acréscimo, os valores e
a identificação de órgãos de cada um**, para que **a regional fique com o conteúdo
autorizado daquela permissão — o que ela pode licitar, comprar e pedir dentro da
vigência e da quinzena de preços — e a secretaria consiga conferir o que cada regional
tem liberado**.

A permissão de contrato liga uma coordenadoria regional a um tipo de contrato, a um
grupo de licitação e a um fornecedor, dentro de uma vigência; o que ela autoriza,
porém, é a lista de gêneros. É esta tela que dá esse conteúdo: sem ela a permissão
existe e não libera nada, e é aqui que cada gênero recebe a quantidade inicial, o
desconto ou acréscimo e o valor com que a regional vai operar. A tela não cria a
permissão — ela acrescenta, altera e exclui gêneros de uma permissão que já exista e
que tenha sido consultada antes — e não deixa a permissão fechar com a soma dos
gêneros diferente do valor adjudicado.

## Contexto

Jornada S000M → C000M → C050M → C060M → C060T.

Ator: servidor de CRE — informa a permissão (coordenadoria regional, vigência, tipo de
contrato e grupo de licitação), consulta e depois mantém, linha a linha, os gêneros
daquela permissão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O C000M, o C050M e o C060M são menus e não gravam nada: eles apenas encaminham. O
contexto que a C060T usa — matrícula, código de acesso, privilégio, tipo de órgão e
coordenadoria regional — é o que a entrada deixou na sessão, e a tela não o recalcula.
Os dois passos imediatamente anteriores são menus: **não** deixam para a tela nem
registro nem modo de operação, de modo que é o próprio campo de opção da C060T que
decide entre consultar e alterar, e ele chega em branco. Esta tela também **não lê a
tela de origem**: não há no fonte comparação com código de tela chamadora, e o
comportamento dela não muda conforme quem a abriu.

A jornada termina aqui. A tela é folha — não encaminha para outra tela nem espera tela
seguinte — e o que ela entrega ao sistema não é uma passagem, e sim o que grava: os
registros da permissão, os registros de identificação de órgãos, a auditoria e o log
de operações. Isso está nas regras abaixo e no anexo.

---

## Regras de negócio

### RN-01 — A tela mantém os gêneros das permissões de contrato

A permissão de contrato é o registro que liga uma coordenadoria regional a um tipo de
contrato, a um grupo de licitação e a um fornecedor, dentro de uma vigência. Esta tela
é a que dá conteúdo a essa permissão: para cada **gênero** autorizado ela guarda a
subclasse, o percentual de desconto ou acréscimo, a quantidade inicial, o valor
inicial, o valor fixo e a indicação de identificação de órgãos.

O cadastro que a tela mantém é o das permissões de contrato, na `C061T` — o mesmo que a
tela de consulta do menu lê. Ele tem **52 campos** e capacidade para **1.000.000** de
registros: capacidade é o máximo esperado, parâmetro de dimensionamento, e não o que
está cadastrado. Cada gênero é um registro próprio; a identidade de um registro é a
coordenadoria regional, a vigência, o tipo de contrato, o grupo de licitação, a classe,
a subclasse e o gênero, e a chave admite repetições. Os registros marcados como
excluídos ficam fora das leituras.

Esta tela **grava**: o programa tem **16 pontos de gravação** e **1 de exclusão** nesse
cadastro, e ainda grava o registro de identificação de órgãos, a auditoria e o log de
operações. **53 programas** do acervo gravam nesse mesmo cadastro — a C060T é um deles.

### RN-02 — A tela só admite ALT e CON; a opção em branco vira consulta

A tela abre em consulta quando encontra a opção de manutenção em branco. Se o operador
enviar uma opção diferente de **ALT** e de **CON**, o sistema recusa com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no campo da opção, antes de
ler qualquer permissão. Só a opção de alteração grava.

[?] A recusa manda usar "ALT" e "CON", mas o sistema reconhece a alteração e a consulta
por códigos internos que o acervo escreve como "CHG" e "INQ"; nenhum valor literal
"ALT" ou "CON" existe no corpus lido. Ou o formulário traduz o que o servidor digita
para esses códigos, ou quem seguir a mensagem é recusado. Pergunta ao site.

[?] A tela tem uma isenção para um modo de exclusão da permissão — no aviso de permissão
não cadastrada —, mas a guarda da opção recusa tudo o que não seja ALT ou CON: pela
tela, esse modo nunca chega à isenção. Se a máscara oferece ao operador uma opção de
exclusão, ela é recusada antes; se não oferece, a isenção é trecho sem uso. Pergunta ao
site.

### RN-03 — A consulta não grava nada

Com a opção de consulta, o tratamento da linha é abandonado antes de qualquer validação
de ação e antes da gravação: nenhum gênero é incluído, alterado ou excluído, e nenhum
registro de auditoria ou de log é criado. Nessa opção a tela só lê — a permissão, as
tabelas de preço e os cadastros de apoio.

### RN-04 — A tela exige que a permissão exista: ela não cria a permissão

Ao consultar uma combinação que não tem nenhum gênero registrado, a tela recusa com
**\* Permissao nao cadastrada \***, com o cursor na coordenadoria regional, e não lista
linha alguma. A alteração e a exclusão também exigem o registro: o sistema procura o
gênero na permissão e recusa quando ele não está lá. A primeira permissão de uma
combinação, portanto, nasce em outra tela do acervo — esta só acrescenta gêneros a uma
permissão que já exista.

[?] As leituras da permissão usam o recurso de posicionamento do dicionário de dados,
cujo efeito exato não está no acervo nem no manual: se ele exige a chave exata, a
consulta só acha quem sabe a combinação inteira; se posiciona no primeiro registro igual
ou posterior, o que foi informado é apenas o ponto de partida da lista. O site precisa
dizer qual é o esperado.

[?] A alteração só é aceita para a permissão que a última consulta deixou guardada na
área da sessão, e a consulta exige que a permissão exista. Se a área da sessão
sobrevive a sair da tela e voltar — ou se outra tela pode deixar nela uma chave que esta
não consultou —, o acervo não mostra. Pergunta ao site.

### RN-05 — A alteração exige a mesma permissão que foi consultada

Em ALT, o sistema recusa quando a coordenadoria regional, as três partes da data
limite, o tipo de contrato ou o grupo de licitação em tela são diferentes dos que a
última consulta deixou guardados: **\* Consulte antes de atualizar \***, com o cursor no
campo da opção. É o que amarra a alteração à permissão que o operador acabou de ver.

### RN-06 — O acesso é conferido a cada operação, e a permissão é da coordenadoria de quem opera

A abertura confere o perfil: a tela tem de estar cadastrada no cadastro de telas. Antes
de validar e antes de gravar, a tela chama a lógica de rota e a conferência de permissão
por operação, com o contexto da sessão — matrícula, código de acesso, privilégio, tipo
de órgão e coordenadoria regional. Se qualquer uma não devolver resultado bom, a linha
não é validada, nada é gravado e nada é auditado. Além disso, a coordenadoria regional
informada tem de ser a do usuário: sendo outra, a recusa é
**\* Usuario sem acesso a este grupo \***, com o cursor na coordenadoria.

[?] As rotinas de segurança e de rota aparecem declaradas nos programas, mas a regra
efetiva de permissão está nas rotinas comuns do acervo, e a conferência da coordenadoria
compara o que foi informado com uma das cópias da coordenadoria do usuário na área de
trabalho, só a conferindo quando outra cópia está preenchida. Qual das cópias o ambiente
preenche — e com que valor — não está no acervo lido. Pergunta ao site.

[?] O conjunto de permissões por tela e por operação que as rotinas comuns leem não é o
desta jornada, e a conferência da operação não tem marca para a consulta: quem tem a
tela autorizada consulta sem precisar de uma marca de consulta. Pergunta ao site.

### RN-07 — Pedir outra tela interrompe a manutenção

Se a requisição chega com a tela pedida para depois preenchida, a validação da
manutenção é interrompida na primeira guarda e nada é gravado: o pedido de tela é
tratado como navegação. Em qualquer outro caso — sem tela pedida — a manutenção segue
normalmente.

[?] O que preenche esse campo não está no corpus lido: nenhum caminho do programa, nem
dos passos anteriores da jornada, o preenche a partir de um cadastro. De onde ele vem, e
o que significa um pedido de tela junto de uma alteração, o acervo não diz. Pergunta ao
site.

### RN-08 — A tela pode estar indisponível para o tipo de licitação

Na consulta, o sistema confere se a tela está liberada para o tipo de licitação da
permissão; não estando, recusa com **\* Tela nao disponivel para esta licitacao \***,
com o cursor no tipo de contrato. Essa conferência é feita só no caminho da consulta: em
ALT ela não se repete.

A consulta lê também os cadastros de apoio para mostrar, fora da grade, a descrição do
tipo de licitação, a razão social do fornecedor e o nome do operador da permissão.

[?] Os três valores são guardados na área de trabalho da tela, e os campos em tela
recebem os valores dessa área no começo da montagem da página — que roda antes dessas
leituras. Se o operador os vê na mesma consulta ou só numa montagem posterior, o acervo
não mostra. Pergunta ao site.

### RN-09 — A permissão tem de estar liberada para ser atualizada

Ao carregar a permissão, o sistema confere o indicador de liberação de cada registro;
encontrando um registro marcado, recusa com **\* Permissao nao pode ser atualizada \***,
com o cursor na coordenadoria regional, e não segue.

[?] Nenhum programa do acervo escreve esse indicador — as duas únicas atribuições que
existem o deixam em branco. Se quem o marca é um processo de fora do acervo, a recusa só
vale para as permissões que esse processo já liberou; se ninguém o marca, a recusa é
trecho sem uso. Pergunta ao site.

### RN-10 — Os valores da permissão e a quinzena da tabela de referência

O operador informa o valor homologado e o valor adjudicado da permissão. O valor
homologado não pode ser zero (**\* Informe o valor homologado \***), o valor adjudicado
não pode ser zero (**\* Informe o valor adjudicado \***) nem maior que o homologado
(**\* Valor adjudicado maior que valor homologado \***). O valor adjudicado tem de
cobrir o total já comprado da permissão; ficando abaixo dele, a recusa é
**\* Vl.Adjudicado menor que total comprado \***, com o cursor no valor adjudicado.

As datas da tabela de referência — o início e o limite — não podem ser posteriores à
data de início da vigência: sendo, a recusa é
**\* Tabela de referencia maior que data de inicio \***, com o cursor na data de início
da tabela.

Fora da grade, a tela mostra uma descrição da quinzena: **Quinzena Normal**,
**Quinzena Especial** — quando o tipo de contrato é de tabela especial — ou
**Valor Fixo**, quando o gênero em tela tem valor fixo.

[?] O total comprado da permissão, que a conferência do valor adjudicado usa, é a soma
de dois campos de cada registro — um valor comprado e um valor comprado temporário —, e
a diferença entre os dois não está no acervo; a única mensagem que os nomeia fala de
notas fiscais. Pergunta ao site.

### RN-11 — As datas da tabela não mudam quando já houve compra

Quando a permissão já tem total comprado, alterar as datas da tabela de referência é
recusado com **\* Nao altere Tb.Refer. Ja existem notas fiscais \***, com o cursor na
data de início da tabela.

### RN-12 — A grade tem oito linhas, e a lista continua de onde parou

A grade mostra **oito** gêneros por vez. Cada linha traz a subclasse, o gênero, a
descrição do gênero, o percentual, o sinal, a quantidade inicial, o valor inicial, o
valor fixo, o indicador de valor fixo, a identificação de órgãos e a ação. A leitura
começa onde a página anterior parou — a chave do último gênero listado fica guardada —,
de modo que reenviar a consulta traz os gêneros seguintes. A descrição do gênero é
mostrada em 10 posições, embora o cadastro de gêneros guarde 15.

[?] A tela carrega até **90** gêneros por permissão, e a conferência de encerramento da
gravação é a **linha vazia** da lista: numa permissão com 90 gêneros ou mais as 90
posições ficam preenchidas, não há linha vazia e a gravação não tem como terminar — a
tela fica presa. Os gêneros além do 90º, ainda, entram nas somas da permissão sem
aparecer na grade nem poder ser mantidos por esta tela. Se o limite é aceitável, e o que
o operador deve fazer com o que sobra, o acervo não diz. Pergunta ao site.

[?] Os rótulos das colunas da grade não estão no acervo lido: a ficha da tela registra
só os rótulos do cabeçalho, e os nomes usados nesta estória vêm do que os cadastros
guardam. Pergunta ao site.

[?] A descrição do gênero é mostrada em 10 posições enquanto o cadastro de gêneros
guarda 15; o que é cortado — e por que —, o acervo não diz. Pergunta ao site.

### RN-13 — Inclusão: o gênero tem de existir, ser do grupamento e não estar na permissão

A linha só é tratada quando traz uma ação: inclusão (**I**), alteração (**A**) ou
exclusão (**E**). Em branco a linha é ignorada, e a subclasse em branco encerra o
tratamento da página.

A inclusão de um gênero passa, nesta ordem, por: o gênero tem de estar cadastrado e
ativo no cadastro de gêneros, senão **\* Genero nao cadastrado \***, com o cursor na
subclasse; o gênero não pode já estar na permissão — nem na vigência que a consulta
deixou guardada —, senão **\* Genero ja cadastrado nesta permissao \***; o gênero tem de
pertencer ao mesmo grupo de licitação da permissão, senão
**\* Genero nao cadastrado neste grupamento \***; tem de haver preço para o gênero na
tabela de referência (RN-14); a quantidade inicial tem de ser informada, senão
**\* Informe a quantidade \***, com o cursor na quantidade. Passando por tudo, o sistema
acrescenta a linha à grade e grava um registro novo da permissão, marcado como ativo, e
deixa a auditoria e o log.

### RN-14 — O preço vem da tabela de referência, e o valor fixo sai do desconto ou acréscimo

A tabela de preços é escolhida pelas datas informadas: a tabela de referência do dia,
quando o início e o limite da tabela são o mesmo dia; a tabela de referência normal,
caso contrário; e a tabela especial, quando o tipo de contrato é de tabela especial. Não
existindo a tabela para a data de início e o limite informados, a recusa é
**\* Tabela de referencia nao cadastrada \***; quando a tabela especial existe para a
data de início mas o limite dela não é o informado, a recusa é
**\* Tabela especial nao cadastrada \***. Não achando preço para o gênero, a recusa é
**\* Genero sem preco na tabela de referencia \*** ou
**\* Genero sem preco na tabela especial \***, conforme a tabela.

O percentual informado tem de ter sinal: um percentual diferente de zero sem sinal é
recusado com **\* Permissao sem desconto ou acrescimo \***. O sinal é herdado da
permissão — o sistema percorre os gêneros já registrados e adota o sinal do primeiro com
percentual diferente de zero; não havendo nenhum, um percentual informado é tomado como
desconto.

O valor fixo do gênero é o preço da tabela ajustado pelo percentual — o preço
multiplicado por um mais o percentual dividido por cem —, de modo que um percentual
negativo reduz e um positivo acrescenta; o valor inicial é a quantidade inicial
multiplicada por esse valor fixo. A linha só guarda o valor fixo quando o operador marca
o indicador de valor fixo; o valor inicial é sempre calculado.

[?] Na tabela de referência normal, a procura do preço percorre até **cinco** registros
a partir do início da tabela e aceita o primeiro com preço preenchido cujo limite esteja
a até **75 dias** do início da tabela; o que define essa janela não está no acervo nem
no manual. Pergunta ao site.

### RN-15 — Alteração: a quantidade, o que já está comprometido e os valores

A alteração exige que o gênero já esteja na permissão, senão
**\* Genero nao cadastrado nesta permissao \***, com o cursor na subclasse; exige a
quantidade inicial, senão **\* Informe a quantidade \***; e exige que a quantidade
informada, somada ao que a permissão já tem de aditivo e de prorrogação, alcance a
quantidade já comprometida: ficando abaixo, a recusa é
**\* Quantidade menor que a comprometida \***.

Passando, o sistema regrava **só os campos que mudaram** — a quantidade inicial, o valor
inicial, o valor fixo, o percentual, os valores homologado e adjudicado, as datas da
tabela de referência e a identificação de órgãos —, travando o registro antes de cada
gravação, e deixa a auditoria e o log.

[?] A conferência de que o gênero está cadastrado e ativo só vale para a inclusão: nos
caminhos da alteração e da exclusão o sistema faz a mesma conferência e descarta o
resultado logo depois, de modo que um gênero inativo pode ser alterado e excluído, mas
não incluído. Se é pretendido, pergunta ao site.

### RN-16 — Identificação de órgãos

O campo de identificação de órgãos só admite **I** ou branco; qualquer outro valor é
recusado com **\* Informe I para identificacao dos Orgaos \***, com o cursor no próprio
campo. Marcando **I**, o sistema cria o registro de identificação daquele gênero, com a
quantidade da linha; retirando a marca, apaga esse registro. Tanto retirar a marca quanto
excluir a linha são recusados enquanto existir a lista de órgãos identificados:
**\* Exclua a lista de Orgaos identificados \***, com o cursor no campo.

[?] A recusa lê a lista de órgãos identificados do cadastro `C676T`, que tem o código do
órgão, mas o caminho que apaga o registro de identificação mexe em outro cadastro, o
`C674T`, que tem a quantidade e o fornecedor e não tem órgão. Se são duas listas
diferentes, ou a mesma vista de dois jeitos, o acervo não diz: a tela grava uma e só lê
a outra. Pergunta ao site.

### RN-17 — Exclusão: o gênero, o que está comprometido e a lista de órgãos

A exclusão de uma linha exige que o gênero esteja na permissão, senão
**\* Genero nao cadastrado nesta permissao \***; que não haja quantidade comprometida,
senão **\* Ja existe quantidade comprometida \***; e que a lista de órgãos identificados
esteja vazia, senão **\* Exclua a lista de Orgaos identificados \***. Passando, o sistema
apaga o registro da permissão, apaga o registro de identificação daquele gênero e deixa
a auditoria e o log. É a única exclusão da tela, e ela é definitiva: o registro sai do
cadastro.

### RN-18 — O fechamento: a soma dos gêneros tem de bater com o valor adjudicado

Ao confirmar a alteração, na última linha da página, o sistema soma os valores iniciais
de todos os gêneros da permissão e exige que a soma seja igual ao valor adjudicado:
diferindo, recusa com **\* Soma qt.inicial dos generos difere do vl.adj \***. A
conferência é dispensada quando todas as linhas estão sendo excluídas e a soma já é
zero; o valor adjudicado continua tendo de cobrir o total comprado (RN-10).

### RN-19 — Toda gravação deixa rastro na auditoria e no log

Cada operação confirmada grava um registro de auditoria com a tela de origem, o cadastro
e o objeto auditado, a operação — inclusão, alteração ou exclusão —, o valor anterior, o
valor posterior e o contexto da sessão (matrícula, coordenadoria regional, terminal,
data e hora e número do processo). A inclusão, a alteração e a exclusão deixam ainda um
registro no log de operações, com a operação e o antes e o depois. O programa grava
**7** registros de auditoria e **4** de log.

[?] A atualização em massa das três somas da permissão — aditivo, prorrogação e
apostilamento — regrava todos os registros da permissão e deixa o log, mas não deixa
registro de auditoria: o valor anterior chega a ser capturado e não é gravado. Se a
secretaria espera auditoria para essa atualização, o caminho não a produz. Pergunta ao
site.

### RN-20 — Uma linha recusada interrompe a gravação das linhas seguintes

A validação e a gravação acontecem linha a linha, na ordem da página. Recusada uma
linha, o sistema marca a página e passa a pular a gravação das linhas seguintes; as
linhas anteriores já foram gravadas. A página, portanto, pode ficar gravada pela metade
quando uma linha posterior é recusada.

[?] Se a gravação parcial é aceitável para a secretaria — o operador vê a mensagem da
linha recusada e não vê quais linhas já foram gravadas —, o acervo não diz, e não há
desfazimento. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os gêneros das permissões de contrato da coordenadoria regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, o acesso e a coordenadoria regional
    E tenho acesso à tela C060T

  Cenário: A consulta da permissão e dos seus gêneros
    Dado que estou na tela C060T
    E informo a coordenadoria regional, a vigência, o tipo de contrato e o grupo de licitação de uma permissão existente
    Quando envio a consulta
    Então a tela mostra os gêneros daquela permissão, oito por vez
    E cada linha traz a subclasse, o gênero, a descrição do gênero, o percentual, a quantidade inicial, os valores e a identificação de órgãos

  Cenário: A opção de manutenção em branco vira consulta
    Dado que estou na tela C060T
    Quando deixo a opção de manutenção em branco e envio
    Então a tela trata o envio como consulta
    E nada é gravado

  Cenário: Opção de manutenção diferente de ALT e de CON
    Dado que estou na tela C060T
    Quando informo uma opção diferente de ALT e de CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo da opção
    E nenhuma permissão é lida nesse caminho

  Cenário: A consulta não grava nada
    Dado que estou na tela C060T na opção CON
    Quando percorro e valido as linhas da página
    Então nenhum gênero é incluído, alterado ou excluído
    E nenhum registro de auditoria ou de log é criado

  Cenário: Permissão sem nenhum gênero registrado
    Dado que estou na tela C060T na opção CON
    Quando informo uma combinação que não tem nenhum gênero registrado
    Então vejo "* Permissao nao cadastrada *"
    E o cursor fica na coordenadoria regional
    E nenhuma linha da grade é preenchida

  Cenário: A permissão não pode ser atualizada
    Dado que a permissão que consultei está marcada como liberada
    Quando envio a alteração
    Então vejo "* Permissao nao pode ser atualizada *"
    E o cursor fica na coordenadoria regional
    E nada é gravado

  Cenário: A alteração exige a permissão consultada
    Dado que estou na tela C060T e já consultei uma permissão
    Quando informo a opção ALT e troco a coordenadoria regional, a data limite, o tipo de contrato ou o grupo de licitação
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo da opção
    E nada é gravado

  Cenário: Permissão de outra coordenadoria regional
    Dado que estou na tela C060T
    Quando informo a coordenadoria regional de outra regional
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica na coordenadoria regional
    E nada é gravado

  Cenário: A tela não está liberada para o tipo de licitação
    Dado que estou na tela C060T na opção CON
    E que a tela não está liberada para o tipo de licitação da permissão
    Quando envio a consulta
    Então vejo "* Tela nao disponivel para esta licitacao *"
    E o cursor fica no tipo de contrato

  Cenário: Nada é gravado sem a segurança de perfil, de rota e de operação
    Dado que estou na tela C060T no modo ALT
    Quando a checagem de perfil, de rota ou de permissão por operação não retorna resultado bom
    Então a linha não é validada
    E nada é gravado e nada é auditado

  Cenário: Um pedido de tela interrompe a manutenção
    Dado que a requisição chega à C060T com uma tela pedida para depois
    Quando a validação da manutenção começaria
    Então o tratamento da linha é abandonado
    E nada é gravado

  Cenário: Os valores da permissão são conferidos
    Dado que estou na tela C060T no modo ALT
    E que a permissão está consultada
    Quando deixo o valor homologado em branco
    Então vejo "* Informe o valor homologado *"
    E o cursor fica no valor homologado
    Quando deixo o valor adjudicado em branco
    Então vejo "* Informe o valor adjudicado *"
    Quando informo o valor adjudicado maior que o homologado
    Então vejo "* Valor adjudicado maior que valor homologado *"
    E nada é gravado

  Cenário: O valor adjudicado tem de cobrir o total comprado
    Dado que a permissão já tem total comprado
    Quando informo um valor adjudicado menor que esse total
    Então vejo "* Vl.Adjudicado menor que total comprado *"
    E o cursor fica no valor adjudicado
    E nada é gravado

  Cenário: A data da tabela de referência posterior à data de início
    Dado que estou na tela C060T no modo ALT
    Quando informo uma data de tabela de referência posterior à data de início da vigência
    Então vejo "* Tabela de referencia maior que data de inicio *"
    E o cursor fica na data de início da tabela
    E nada é gravado

  Cenário: A quinzena da tabela aparece fora da grade
    Dado que consulto uma permissão cujo tipo de contrato é de tabela especial
    Quando a página é apresentada
    Então vejo "Quinzena Especial" na descrição da quinzena
    E numa permissão cujo gênero em tela tem valor fixo vejo "Valor Fixo"

  Cenário: As datas da tabela não mudam quando já houve compra
    Dado que a permissão já tem total comprado
    Quando tento alterar as datas da tabela de referência
    Então vejo "* Nao altere Tb.Refer. Ja existem notas fiscais *"
    E o cursor fica na data de início da tabela
    E as datas não são alteradas

  Cenário: A grade tem oito linhas e a lista continua de onde parou
    Dado que a permissão tem mais de oito gêneros registrados
    Quando consulto a permissão
    Então a grade mostra oito gêneros
    Quando reenvio a consulta sem mudar nada
    Então a grade mostra os gêneros seguintes, a partir do último que apareceu

  Cenário: Inclusão de um gênero na permissão
    Dado que estou na tela C060T no modo ALT
    E que a permissão está consultada
    E que o gênero está cadastrado e ativo no cadastro de gêneros
    E que o gênero pertence ao grupo de licitação da permissão
    E que o gênero ainda não está na permissão
    Quando informo a ação I, a quantidade inicial e o percentual e confirmo
    Então o gênero é gravado na permissão
    E a inclusão fica registrada na auditoria e no log

  Cenário: Inclusão de gênero não cadastrado
    Dado que estou na tela C060T no modo ALT
    Quando informo a ação I para um gênero que não está cadastrado ou não está ativo
    Então vejo "* Genero nao cadastrado *"
    E o cursor fica na subclasse
    E nada é gravado

  Cenário: Inclusão de gênero que já está na permissão
    Dado que estou na tela C060T no modo ALT
    Quando informo a ação I para um gênero que já está na permissão
    Então vejo "* Genero ja cadastrado nesta permissao *"
    E nada é gravado

  Cenário: Inclusão de gênero de outro grupamento
    Dado que estou na tela C060T no modo ALT
    Quando informo a ação I para um gênero de outro grupo de licitação
    Então vejo "* Genero nao cadastrado neste grupamento *"
    E nada é gravado

  Cenário: A tabela de referência e o preço do gênero
    Dado que estou na tela C060T no modo ALT
    E que a tabela de referência da janela informada não está cadastrada
    Quando confirmo a linha
    Então vejo "* Tabela de referencia nao cadastrada *"
    E o cursor fica na data de início da tabela
    E nada é gravado
    Quando a tabela existe mas o limite dela não é o que informei
    Então vejo "* Tabela especial nao cadastrada *"
    Quando a tabela existe mas o gênero não tem preço nela
    Então vejo "* Genero sem preco na tabela de referencia *"
    E numa permissão de tabela especial vejo "* Genero sem preco na tabela especial *"

  Cenário: Percentual sem sinal
    Dado que estou na tela C060T no modo ALT
    Quando informo um percentual diferente de zero sem sinal
    Então vejo "* Permissao sem desconto ou acrescimo *"
    E nada é gravado

  Cenário: O valor inicial sai da quantidade pelo valor fixo
    Dado que estou na tela C060T no modo ALT
    E que o preço do gênero na tabela de referência é conhecido
    Quando informo uma quantidade inicial e um percentual de desconto e confirmo
    Então o valor fixo do gênero é o preço reduzido pelo percentual
    E o valor inicial é a quantidade inicial multiplicada por esse valor fixo

  Cenário: Alteração de um gênero da permissão
    Dado que estou na tela C060T no modo ALT
    E que o gênero está na permissão
    Quando informo a ação A com a nova quantidade e os novos valores e confirmo
    Então só os campos que mudaram são gravados
    E a alteração fica registrada na auditoria e no log

  Cenário: Alteração exige a quantidade e o comprometido
    Dado que estou na tela C060T no modo ALT
    E que o gênero está na permissão
    Quando informo a ação A sem a quantidade
    Então vejo "* Informe a quantidade *"
    E o cursor fica na quantidade
    Quando informo uma quantidade que não alcança o que já está comprometido
    Então vejo "* Quantidade menor que a comprometida *"
    E nada é gravado

  Cenário: Identificação de órgãos
    Dado que estou na tela C060T no modo ALT
    Quando informo um valor diferente de I e de branco no campo de identificação de órgãos
    Então vejo "* Informe I para identificacao dos Orgaos *"
    E o cursor fica no campo
    Quando informo I e confirmo
    Então o sistema cria o registro de identificação daquele gênero
    Quando retiro o I com a lista de órgãos identificados preenchida
    Então vejo "* Exclua a lista de Orgaos identificados *"
    E nada é apagado

  Cenário: Exclusão de um gênero da permissão
    Dado que estou na tela C060T no modo ALT
    E que o gênero está na permissão, sem quantidade comprometida e sem lista de órgãos identificados
    Quando informo a ação E e confirmo
    Então o registro da permissão é apagado
    E o registro de identificação daquele gênero também é apagado
    E a exclusão fica registrada na auditoria e no log

  Cenário: Exclusão recusada
    Dado que estou na tela C060T no modo ALT
    Quando informo a ação E para um gênero que não está na permissão
    Então vejo "* Genero nao cadastrado nesta permissao *"
    Quando o gênero está na permissão mas tem quantidade comprometida
    Então vejo "* Ja existe quantidade comprometida *"
    Quando o gênero tem a lista de órgãos identificados preenchida
    Então vejo "* Exclua a lista de Orgaos identificados *"
    E nada é apagado

  Cenário: O fechamento da permissão
    Dado que estou na tela C060T no modo ALT
    E que os gêneros da permissão somam um valor inicial diferente do valor adjudicado
    Quando confirmo a última linha da página
    Então vejo "* Soma qt.inicial dos generos difere do vl.adj *"
    E nada é gravado nesse fechamento

  Cenário: Linha com ação em branco é ignorada
    Dado que estou na tela C060T no modo ALT
    Quando deixo a subclasse ou a ação da linha em branco
    Então a linha não é validada e nada é gravado para ela

  Cenário: Uma linha recusada interrompe a gravação das seguintes
    Dado que estou na tela C060T no modo ALT com linhas preenchidas
    Quando a terceira linha da página é recusada
    Então as linhas anteriores a ela já foram gravadas
    E nenhuma linha seguinte é gravada nesse envio
```
