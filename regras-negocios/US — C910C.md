# US — C910C — Consultar a validade dos cardápios

## Estória

Como **servidor de CRE**, quero **consultar os cardápios da minha secretaria pela
data limite de validade, vendo numa mesma lista o período de cada um, o seu código
e a sua descrição**, para que **eu saiba qual versão do cardápio está valendo no
período que eu informe, sem ter de abrir o cadastro de cada um**.

O cardápio reúne a alimentação servida num período, e o cadastro guarda **um
registro por período de validade**: o mesmo código de cardápio reaparece a cada
versão nova, e é a data limite que separa uma versão da outra. Quem estima a
alimentação de um período e quem monta o cardápio precisam saber qual versão está
vigente; sem esta consulta, o servidor só descobre a validade de um cardápio
abrindo o cadastro dele, um a um.

## Contexto

Jornada S000M → C000M → C800M → C900M → C910C.

Ator: servidor de CRE — consulta os cardápios da sua secretaria pela data limite de
validade, com o período, o código e a descrição de cada um.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. Os três menus do caminho não
gravam nada: apenas encaminham. O contexto que a tela usa — matrícula, código de
acesso, privilégio, tipo de órgão, coordenação regional escolar e a data do sistema
— é o que a entrada deixou na sessão; a tela não recalcula esse contexto. Ela é o
**fim da jornada**: não tem opção de menu e não passa registro nem operação adiante.

---

## Regras de negócio

### RN-01 — A tela é de consulta, e qualquer outra operação é recusada

A tela abre sempre em modo de consulta e repõe esse modo a cada apresentação, de
modo que a operação em tela volta a ser a consulta. Se uma mensagem seguinte chegar
com outra operação, o sistema recusa com **\* Operacao nao disponivel \***, devolve
o cursor ao campo da operação e **não lê nenhum cardápio**: nesse caminho a grade
não chega a ser montada. A recusa vem depois das conferências de acesso e da edição
dos campos, e antes de qualquer leitura.

O comportamento **não muda conforme a tela que abriu esta**: não há, no programa,
nenhuma comparação com a tela de origem, e o modo de consulta é reposto em toda
abertura, venha ela do menu ou de qualquer outro caminho.

[?] A recusa só existe se a máscara oferecer ao operador um campo de operação. Como
a abertura repõe a consulta sozinha, a recusa só pode ser alcançada numa mensagem
seguinte do operador; se a máscara não tem esse campo, a recusa é trecho sem uso.
Pergunta ao site.

### RN-02 — O cadastro consultado é o dos cardápios, um registro por período de validade

O cadastro consultado tem **17 campos**: o tipo de órgão, o dia, o mês e o ano de
início e de limite do período, o código do cardápio (5 dígitos), a descrição do
cardápio (60 caracteres), **quatro marcas de uma posição — uma para cada semana A,
B, C e D —**, duas marcas de uma posição que dizem se o período tem fruta e se tem
sobremesa, e mais dois campos que a tela desta jornada não mostra. A capacidade
declarada é de **100.000 registros** (capacidade é o máximo esperado, parâmetro de
dimensionamento, não o que está cadastrado).

A chave que a tela usa reúne, nesta ordem, **o tipo de órgão, o ano, o mês e o dia
limite e o código do cardápio**, e **admite repetição**. O que distingue uma versão
de um cardápio da outra é a data limite: o mesmo código aparece uma vez por
período.

[?] Dois campos do cadastro — uma marca de uma posição e um segundo código de cinco
dígitos, gravado ao lado do código do cardápio — não têm rótulo em nenhuma tela
lida nem significado no corpus ou no manual. Pergunta ao site.

### RN-03 — A grade mostra até 14 linhas, cada uma com o período, o código e a descrição

A grade tem **14 linhas**. Cada linha traz **quatro informações**: a **data de
início** da validade, a **data limite**, o **código do cardápio** e a **descrição do
cardápio**. As duas datas saem no formato **dia/mês/ano**, com o dia e o mês em dois
dígitos e o ano em quatro; o código sai com cinco dígitos. A descrição guardada tem
60 caracteres e a da linha tem 50: descrição maior aparece **cortada**.

As linhas são preenchidas uma a uma, por leituras sucessivas do mesmo caminho de
acesso — a primeira posicionada pelo que o operador informou, e cada seguinte
avançando para o registro seguinte desse caminho. Por isso a grade sai na **ordem do
caminho**: tipo de órgão, ano, mês e dia limite e, dentro da mesma data limite, o
código do cardápio. Não havendo mais o que mostrar, a varredura para e as linhas
restantes ficam em branco.

[?] A varredura da grade só entra quando uma marca de continuidade está no estado
"não"; essa marca é carregada da área da sessão, reinicializada pela própria tela e
ligada em "sim" quando a varredura termina. Se a primeira abertura pode sair sem
nenhuma linha por causa disso — e o que o operador vê nesse caso —, o acervo não
responde. Pergunta ao site.

### RN-04 — A consulta é pelo dia, o mês e o ano limite e o código do cardápio, dentro do tipo de órgão da sessão

O operador informa **o dia, o mês e o ano limite** e **o código do cardápio**; a
tela acrescenta **o tipo de órgão da sessão** e procura o período com essa
combinação. Achando, o que foi informado passa a ser o ponto de partida da lista e
volta para os campos em tela. Reenviar exatamente o que já está na tela **não
provoca nova procura**: os valores são aceitos como estão.

[?] A leitura usa o recurso de posicionamento do dicionário de dados, cujo efeito
exato não está no acervo nem no manual: se ela exige a **combinação exata** de um
período registrado, o operador só consulta quem sabe a data e o código; se ela
apenas **posiciona** no primeiro período igual ou posterior, a data e o código
informados são só o ponto de partida da lista. Os dois comportamentos são
compatíveis com o que o fonte mostra. Pergunta ao site.

### RN-05 — Não havendo período para o que foi informado, a tela avisa e apaga o informado

Não achando o período para a combinação informada, o sistema avisa
**\* Cardapio nao cadastrado \***, **não preenche nenhuma linha** da grade e **apaga
os quatro valores informados**, de modo que a próxima apresentação da tela recomeça
a lista de uma posição zerada. O aviso é decidido quando a **primeira linha** da
página é montada e não é repetido nas demais.

[?] O que o operador vê exatamente quando a procura não acha. A procura que não acha
apaga o que foi informado e a próxima apresentação recomeça de uma posição zerada:
se a leitura exigir a combinação exata, a posição zerada não acha nada e o operador
vê o aviso; se a leitura apenas posicionar, a posição zerada é o começo do cadastro
e o operador vê o começo da lista, sem aviso. O acervo mostra os dois trechos e não
permite escolher. Pergunta ao site.

[?] Como o aviso é decidido uma única vez, na primeira linha, uma grade que esvazie
mais adiante fica em branco sem explicação. Se isso é o pretendido ou resíduo do
gerador, é pergunta ao site.

### RN-06 — A digitação dos quatro campos é editada, e o cursor volta ao campo recusado

Os quatro campos informados — o dia, o mês e o ano limite e o código do cardápio —
passam por edição numérica antes de qualquer leitura: campo em branco é tratado como
zero, o que não for número é recusado e a consulta não segue, e o cursor volta ao
campo recusado.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não
está nos fontes desta jornada: a rotina que faz a edição numérica é importada de uma
biblioteca que não faz parte do acervo lido.

### RN-07 — A tela mostra a data do sistema e a descrição do tipo de órgão da sessão

Fora da grade, a tela exibe a **data do sistema** e a **descrição do tipo de órgão**
da sessão.

[?] Nem a data do sistema nem a descrição do tipo de órgão são preenchidas por
nenhum caminho que o acervo mostre: as duas aparecem sempre como origem de cópia, e
a entrada guarda a descrição do tipo de órgão em outra área da sessão. Se o ambiente
transporta o valor de uma área para a outra — e de onde vem a data do sistema —, o
acervo não diz; se não transportar, os dois campos saem em branco. Pergunta ao site.

### RN-08 — Cada consulta começa com os campos de resultado limpos

Antes de conferir a digitação e de ler qualquer cardápio, a tela apaga os **seis
campos de resultado**: o código, a descrição e as duas datas que a consulta anterior
havia mostrado, e também a descrição do tipo de órgão e a data do sistema. Uma
consulta recusada, portanto, não deixa na tela o resultado da consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se
existe um caminho de entrada em que os campos não são limpos, é pergunta ao site.

### RN-09 — A consulta não grava nada e não deixa rastro de auditoria

A tela **só lê**. Nenhum registro é incluído, alterado ou excluído, e nenhum
registro de auditoria é gerado. As operações de gravação, de exclusão e de
travamento de registro existem declaradas para os cadastros que a tela enxerga, mas
**não são executadas em nenhum caminho**: declarar não é executar.

### RN-10 — O cadastro consultado não é mantido por nenhuma tela

As **seis** telas do acervo lido que consultam esse cadastro **não o gravam**:
nenhuma inclui, altera, exclui ou trava registro nele. Os únicos pontos do acervo
lido que o gravam são **dois programas de trabalho em lote** de relatórios do mesmo
módulo — um inclui registros, o outro exclui.

[?] Se o cadastro continua sendo alimentado no dia a dia, e por quem, não se conclui
das telas: o acervo lido não mostra nenhuma manutenção dele pela operação, e os
únicos que o gravam não são telas. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar a validade dos cardápios

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C910C

  Cenário: Consulta dos cardápios pela data limite
    Dado que informo o dia, o mês e o ano limite e o código do cardápio
    Quando envio a consulta
    Então vejo os cardápios em linhas, cada uma com a data de início, a data limite, o código e a descrição

  Cenário: A grade mostra no máximo 14 cardápios
    Dado que há mais de 14 cardápios a mostrar a partir do que informei
    Quando envio a consulta
    Então a grade mostra no máximo 14 linhas
    E as linhas restantes ficam em branco

  Cenário: Os cardápios saem na ordem do período
    Dado que há mais de um cardápio a mostrar
    Quando envio a consulta
    Então cada linha traz um cardápio diferente, em ordem crescente de ano, mês e dia limite e, na mesma data, de código

  Cenário: As datas aparecem no formato dia/mês/ano
    Dado que um cardápio tem data de início e data limite registradas
    Quando a lista é mostrada
    Então vejo as duas datas com o dia e o mês em dois dígitos e o ano em quatro

  Cenário: Descrição maior que a linha aparece cortada
    Dado que o cardápio tem uma descrição com mais de 50 caracteres
    Quando a lista é mostrada
    Então vejo a descrição cortada no que cabe na linha

  Cenário: Reenviar o que já está na tela
    Dado que a tela já mostra o resultado de uma consulta
    Quando envio de novo exatamente os mesmos valores
    Então a consulta não é refeita e a lista continua a mesma

  Cenário: Cardápio não cadastrado
    Dado que informo uma combinação de data limite e código de cardápio sem período registrado
    Quando envio a consulta
    Então vejo a mensagem "* Cardapio nao cadastrado *"
    E nenhuma linha da grade é preenchida
    E o que eu havia informado é apagado

  Cenário: Sem nenhum cardápio para o meu órgão
    Dado que não há nenhum cardápio registrado para o tipo de órgão da minha sessão
    Quando abro a tela C910C
    Então vejo a mensagem "* Cardapio nao cadastrado *"
    E nenhuma linha da grade é preenchida

  Cenário: Operação diferente da consulta
    Dado que estou na tela C910C
    Quando chega uma operação diferente da consulta
    Então vejo a mensagem "* Operacao nao disponivel *"
    E o cursor volta ao campo da operação
    E nenhum cardápio é lido nesse caminho

  Cenário: Digitação não numérica na data limite ou no código do cardápio
    Dado que digito na data limite ou no código do cardápio algo que não é número
    Quando envio a consulta
    Então o sistema recusa a digitação antes de ler qualquer cardápio
    E o cursor volta ao campo recusado

  Cenário: A data do sistema e o tipo de órgão da sessão
    Dado que entrei no sistema
    Quando abro a tela C910C
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: O resultado da consulta anterior não fica na tela
    Dado que já abri a tela e ela mostrou cardápios
    Quando volto a consultar
    Então o código, a descrição e as datas da consulta anterior não ficam na tela

  Cenário: A consulta não grava nada
    Dado que abro a tela C910C
    Quando a lista é mostrada
    Então nenhum cardápio é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Nenhuma tela mantém o cadastro consultado
    Dado que percorro as telas do acervo que consultam este cadastro
    Quando procuro quem inclui, altera ou exclui um período
    Então nenhuma tela o grava
    E a gravação só existe em programas de trabalho em lote
```
