# US — C070C — Consultar o cardápio pela data limite

## Estória

Como **servidor de CRE**, quero **informar o código de um cardápio do meu órgão e
o dia, o mês e o ano do limite dele e ver o que está cadastrado nessa posição**,
para que **eu confira a descrição do cardápio e o seu período de vigência — quando
ele começa e até quando vale — sem risco de alterar o cadastro**.

O cardápio reúne os gêneros da alimentação escolar e cada versão dele vale por um
período, com uma data de início e uma data limite. Quando é preciso dizer a que
cardápio uma data pertence, é esta tela que responde, pela combinação exata do
órgão, do código e da data limite. Como ela é só de leitura, quem consulta não
corre o risco de mexer no cadastro por engano; quem inclui, altera e exclui
cardápio são as telas de manutenção.

## Contexto

Jornada S000M → C000M → C070M → C070C.

Ator: servidor de CRE — consulta o cardápio do seu órgão pelo código e pela data
limite.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

As regras abaixo são só as da tela desta jornada. O C000M e o C070M são telas de
encaminhamento: não gravam nada e entregam à C070C o que a sessão já trazia — a
matrícula, o órgão e o código de acesso. O modo de operação com que a C070C abre
chega junto com a tela, entregue por quem a chamou; por isso ele é regra daqui, e
não regra da entrada.

---

## Regras de negócio

### RN-01 — A tela só consulta e não grava nada

A C070C lê o cadastro dos cardápios e o cadastro do órgão da sessão; não inclui,
não altera e não exclui cardápio nenhum. Por mais que o cadastro dos cardápios
disponha de inclusão, alteração e exclusão, esta tela não chega a nenhuma delas —
e, como não grava, também não deixa registro de auditoria. Quem mantém o cadastro
dos cardápios são as telas de manutenção.

### RN-02 — A operação chega com a tela e só a consulta é aceita

O modo de operação com que a tela abre é o que a tela anterior entregou, não uma
escolha feita aqui. A única operação que a C070C executa é a consulta. Quando o
campo de operação chega em branco, a própria tela repõe a consulta; quando chega
outra operação e o servidor confirma, o sistema recusa com
**\* Operacao nao disponivel. Use CON \*** e devolve o cursor ao campo da
operação, sem ler e sem gravar nada.

[?] A mensagem manda usar "CON", mas a tela só reconhece o código interno de
consulta do sistema; nenhum valor "CON" existe no acervo lido. Ou o formulário
traduz o que o servidor digita, ou quem seguir a mensagem é recusado. Pergunta ao
site.

### RN-03 — Ao abrir, a tela não procura cardápio nenhum

A abertura traz os campos de limite zerados e não lê cardápio nenhum: a lista só
se monta depois de uma consulta confirmada. A posição de onde a leitura parte é a
que a sessão já trazia da passagem anterior; não havendo posição guardada, a tela
fica na consulta vazia.

[?] A tela carrega a posição deixada pela passagem anterior na área de trabalho
compartilhada da sessão, e é isso que decide se a abertura já mostra alguma
validade. O acervo não mostra se, no uso real, essa passagem sempre deixa uma
posição. Pergunta ao site.

### RN-04 — O cardápio consultado é o do órgão do servidor

A consulta é sempre dentro do órgão da sessão: o tipo de órgão não é digitado
nesta tela. Um cardápio de outro órgão não é encontrado, ainda que o código e a
data limite existam no cadastro.

### RN-05 — O cardápio é identificado pelo código e pela data limite completa

A identidade do que se consulta é a combinação do órgão com o código do cardápio
e com a data limite completa — dia, mês e ano. Não basta o código: a mesma versão
de cardápio pode ter mais de uma validade, e é a data que diz qual delas está em
questão. O conjunto pelo qual a tela lê está ordenado pelo órgão, pelo código do
cardápio e pela data limite, e admite mais de um registro para a mesma combinação.

[?] A leitura avança de registro em registro pelo mesmo conjunto, mas o recurso de
leitura vem de biblioteca sem fonte no lote; o que ordena a passagem de um
registro para o seguinte não está no acervo lido. Se a lista atravessa para
outros códigos do mesmo órgão, o acervo também não mostra. Pergunta ao site.

### RN-06 — Os quatro campos informados são números; em branco valem zero

O código do cardápio e o dia, o mês e o ano do limite são editados como número
antes de qualquer leitura, e campo em branco vale zero. Quando a edição recusa um
campo, o cursor volta para ele, na ordem em que a tela os confere: primeiro o
código do cardápio, depois o dia, o mês e o ano do limite.

### RN-07 — Não existindo o cardápio informado, a tela recusa com **\* Cardapio nao cadastrado \***

Procurado o cardápio do órgão pela combinação informada e não o achando, o
sistema recusa com **\* Cardapio nao cadastrado \*** e deixa o cursor no código do
cardápio; nada é alterado. Como campo em branco vale zero, confirmar a consulta
com os quatro campos em branco procura o cardápio de código zero e recebe a mesma
recusa.

### RN-08 — A lista mostra até 14 validades, com início, limite e descrição

A página da C070C tem 14 linhas, e cada linha traz a data de início, a data limite
e a descrição do cardápio, com as duas datas montadas no formato dia/mês/ano a
partir das partes de cada data do cadastro. Fora da lista, a tela leva a data do
sistema e a descrição do órgão da sessão. A leitura começa na posição informada e
segue adiante, uma linha por vez, até a página completar ou até o cadastro acabar.

### RN-09 — Esgotado o cadastro antes do fim da página, os limites voltam a zero

Se a lista se esgota antes de a página completar, os campos de limite voltam a
zero, sem aviso ao servidor.

[?] A volta a zero acontece no fim da montagem da página e não olha o que o
servidor informou: se ele consultou uma validade que existe e o cadastro acabou
antes de a página completar, os limites que ele digitou se perdem na tela. Se isso
é intencional, o acervo não diz. Pergunta ao site.

### RN-10 — Preenchido o campo de próxima tela, a tela encaminha e não faz mais nada

O campo de próxima tela é o que faz uma tela passar o servidor para outra sem
passar por menu nenhum. Chegando preenchido, o roteamento do sistema leva o
servidor à tela indicada e a confirmação da C070C termina ali: ela não consulta,
não avisa e não grava.

[?] O campo de próxima tela faz parte do registro da tela, mas não tem rótulo na
ficha da C070C; se ele é visível e digitável pelo servidor, ou se só a tela que a
chamou o preenche, o acervo não mostra. Pergunta ao site.

### RN-11 — Antes de mostrar a lista o sistema confere o acesso, e na confirmação confere de novo

Ao abrir, a tela confere o vínculo do servidor e o cadastro da própria tela antes
de ler qualquer cardápio; na confirmação, confere a rota e, depois, a permissão de
operação do código de acesso. Tela não cadastrada sai
**\* Tela nao cadastrada \***; tela fora do quadro de telas liberadas para o
código de acesso sai **\* Tela nao disponivel \***; par de código de acesso e tela
não autorizado sai **\* Acesso negado para esta matricula \***; operação não
permitida ao código de acesso sai **\* Acesso negado para esta operacao \***.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar o cardápio pela data limite

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C070C

  Cenário: Consultar um cardápio pela data limite
    Dado que informo o código de um cardápio do meu órgão
    E informo o dia, o mês e o ano do limite desse cardápio
    Quando confirmo a consulta
    Então vejo a descrição do cardápio
    E vejo a data de início e a data limite da validade consultada

  Cenário: Abrir a tela sem consultar
    Quando abro a tela C070C
    Então os campos de limite aparecem zerados
    E a lista aparece vazia

  Cenário: Consultar com os campos em branco
    Dado que deixo o código do cardápio e os limites em branco
    Quando confirmo a consulta
    Então o sistema recusa com "* Cardapio nao cadastrado *"
    E o cursor volta ao código do cardápio

  Cenário: Consultar uma data limite sem cardápio
    Dado que informo o código de um cardápio do meu órgão
    E informo uma data limite que esse cardápio não tem
    Quando confirmo a consulta
    Então o sistema recusa com "* Cardapio nao cadastrado *"
    E o cursor volta ao código do cardápio
    E nada é gravado

  Cenário: Consultar o cardápio de outro órgão
    Dado que informo o código e a data limite de um cardápio de outro órgão
    Quando confirmo a consulta
    Então o sistema recusa com "* Cardapio nao cadastrado *"

  Cenário: Recusa de operação diferente da consulta
    Dado que a tela chega com uma operação de manutenção
    Quando confirmo
    Então o sistema recusa com "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: Recusa de campo não numérico
    Dado que informo letras no mês limite
    Quando confirmo a consulta
    Então o sistema recusa o mês limite
    E o cursor volta ao campo do mês limite

  Cenário: A lista de validades
    Dado que informo o código de um cardápio que tem mais de uma validade
    Quando confirmo a consulta
    Então a lista mostra até 14 linhas, a começar pela validade informada
    E cada linha traz a data de início, a data limite e a descrição do cardápio

  Cenário: Lista que acaba antes do fim da página
    Dado que consulto uma validade perto do fim do cadastro do cardápio
    Quando confirmo a consulta
    Então os campos de limite voltam a zero
    E nenhum aviso é mostrado

  Cenário: Encaminhamento pela próxima tela
    Dado que a tela chega com o campo de próxima tela preenchido
    Quando confirmo
    Então o sistema me leva à tela indicada
    E a C070C não consulta e não grava nada

  Cenário: Recusa de acesso, quando a tela não está liberada
    Dado que a tela C070C não está liberada para o meu código de acesso
    Quando abro a tela
    Então o sistema recusa com "* Tela nao disponivel *"

  Cenário: Recusa de operação não permitida ao meu código de acesso
    Dado que o meu código de acesso não permite a operação informada
    Quando confirmo
    Então o sistema recusa com "* Acesso negado para esta operacao *"

  Cenário: A consulta não grava nada
    Dado que consulto um cardápio do meu órgão por uma validade existente
    Quando confirmo a consulta
    Então nenhum cardápio é incluído, alterado ou excluído
    E nenhum registro de auditoria é deixado
```
