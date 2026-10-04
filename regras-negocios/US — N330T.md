# US — N330T — Pedido de emissão do movimento do lote

## Estória

Como **servidor da CRE**, quero **pedir a emissão do movimento de um lote na
impressora que eu escolher**, para que **a relação do lote saia para conferência
sem eu depender de quem opera o processamento em lote**.

O movimento não é montado na tela: quem o produz é o processamento em lote, e o que
a tela faz é reunir o pedido e entregá-lo. Sem o pedido, o processamento não tem
trabalho a executar, e o lote fica sem a sua relação. A tela não mantém cadastro de
negócio nenhum: o único registro que ela atualiza é a impressora preferida do
próprio servidor.

## Contexto

Jornada S000M → N000M → N050M → N300M → N330T.

Ator: servidor de CRE — informa a coordenadoria regional escolar, o código da
secretaria, o lote e a impressora, e pede a emissão do movimento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As telas que antecedem esta são **menus**: tanto a `N050M` quanto a `N300M` têm
opções declaradas, e é por uma opção da `N300M` que a `N330T` abre. A tela desta
jornada **não** recebe operação encadeada de quem a chamou: ela abre no seu próprio
modo e o decide por si, e não muda de comportamento conforme a tela de origem. O que
ela usa — matrícula, código de acesso, privilégio, tipo de órgão e coordenadoria
regional escolar — é o que a entrada deixou na sessão, e a `N330T` apenas o repassa
às conferências e ao pedido. Esta é a última tela da jornada: dela não se passa para
outra.

A conferência de autorização da tela é regra da entrada, e está no anexo de
evidências. As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela pede a emissão do movimento de um lote

A tela não monta o movimento: ela reúne o pedido — a coordenadoria regional escolar,
o código da secretaria, o lote, a impressora escolhida, uma cópia, a matrícula de
quem pediu, o endereço de correio desse servidor, o tipo de órgão da sessão e a pasta
de saída — e o entrega ao processamento em lote, que é quem produz a relação. O
relatório pedido é sempre o do movimento do lote: a tela não deixa escolher outro, e
a emissão é sempre de uma cópia.

[?] O trabalho entregue é o da atualização do movimento do lote. O trecho que o
dispara foi lido, mas a rotina que o entrega é do ambiente e não tem corpo no
acervo: o que esse trabalho executa com o lote — e o que o "movimento" do seu nome
designa — não se decide pelo fonte. Pergunta ao site.

[?] O pedido carrega um campo de estação (o terminal de origem) que a tela nunca
preenche: ele sai em branco. Se quem processa o movimento precisa saber de que
terminal veio o pedido, pergunta ao site.

### RN-02 — A tela não mantém cadastro de negócio: lê seis e escreve em dois

A tela enxerga seis registros — o registro das telas e relatórios, o registro do
servidor, o cadastro das coordenadorias regionais escolares, o cadastro dos tipos de
órgão, a impressora do servidor e a fila de requisições — e escreve em apenas
**dois**: a impressora do próprio servidor, que ela atualiza ou cria com a escolhida,
e a fila de requisições, onde apaga o pedido pendente do lote. Nenhum cadastro de
negócio é incluído, alterado ou excluído, e a tela não deixa rastro de auditoria.

### RN-03 — A coordenadoria regional escolar é obrigatória, tem de existir e é a da sessão

A tela exige a coordenadoria (o grupo). Se ela vier em branco, a recusa é
* Informe o grupo *; se não estiver cadastrada para o tipo de órgão da sessão,
* Grupo nao cadastrado *. Quando a sessão já carrega uma coordenadoria, o servidor
só pode pedir para essa: informar outra é recusado com
* Usuario sem acesso a outro grupo *. Ao abrir, a tela já sugere a coordenadoria da
sessão. Nas três recusas o cursor volta ao campo da coordenadoria.

[?] A conferência compara a coordenadoria informada com a cópia da área de trabalho
da sessão, e nenhum dos seis programas desta jornada escreve nessa cópia: no acervo,
o que existe são zeragens na montagem da sessão e cópias de dados de outras telas.
Se ela chegar zerada, a guarda não recusa nada e qualquer coordenadoria cadastrada
passa; e, como o campo já vem preenchido com a coordenadoria da sessão, apagá-lo cai
na recusa de "outro grupo", e não na de "informe o grupo". Pergunta ao site.

### RN-04 — O lote é obrigatório e vem em três partes

O lote é informado em três partes — o código da secretaria, com 2 dígitos; o código
do lote, com 6; e mais quatro dígitos que a tela não rotula — e o sistema as junta num
único número de 12 dígitos. Basta uma das três estar preenchida para o lote ser
aceito; com as três zeradas a recusa é * Informe numero do lote * e o cursor volta ao
campo da secretaria.

[?] O que os quatro últimos dígitos do lote identificam não está no acervo: esse
campo não tem rótulo de negócio nem na tela nem no fonte. E o código de secretaria
informado no lote **não** é conferido contra a secretaria da sessão — só a
coordenadoria é. Pergunta ao site.

### RN-05 — O servidor precisa ter endereço de correio cadastrado

Antes de emitir, a tela procura o registro do servidor pela matrícula da sessão e
exige que ele tenha endereço de correio. Sem ele, a recusa é
* Usuario sem e-mail cadastrado * e nada é emitido; o endereço encontrado segue no
pedido.

[?] A recusa é sobre o endereço de correio, mas o cursor volta ao campo da
coordenadoria — o endereço não está na tela. Pergunta ao site.

### RN-06 — A impressora é obrigatória e a tela mantém a preferida do servidor

A impressora é exigida — * Informe a impressora *, com o cursor no campo dela. Ao
abrir, a tela já traz a impressora guardada para a matrícula do servidor, e ao
confirmar o pedido mantém essa preferência atualizada: se a informada for diferente
da guardada, a guardada passa a ser a informada; se o servidor ainda não tiver
nenhuma guardada, o registro é criado com a informada. A preferência é por servidor, e
esse cadastro é dimensionado para **10 mil** registros — capacidade (máximo esperado,
parâmetro de dimensionamento), não volume cadastrado.

[?] A criação do registro, quando ele não existe, passa por uma escolha que o próprio
programa não comanda: conforme o destino calculado coincida ou não com a origem, a
gravação local é trocada por um encaminhamento a outro ambiente. Nenhum fonte do
acervo determina esse destino para esta transação. Pergunta ao site.

[?] O cadastro da impressora admite mais de um registro para a mesma matrícula e a
leitura toma o último; o que a tela faz com os registros anteriores não está no
programa. Pergunta ao site.

### RN-07 — A emissão apaga o pedido pendente do lote e dispara o movimento

Confirmado o pedido, a tela procura na fila de requisições o pedido de movimento
**pendente** daquele lote e apaga o que encontrar, para não ficar um pedido pendente
do mesmo lote; em seguida entrega ao processamento em lote o trabalho do movimento,
com os dados do pedido: o relatório, a impressora, uma cópia, a matrícula, o tipo de
órgão, a coordenadoria, o lote, o endereço de correio e a pasta de saída. A pasta de
saída acompanha o tipo de órgão da sessão: no tipo de órgão da coordenadoria regional
escolar ela é o prefixo da CRE seguido do código da coordenadoria informada; em dois
tipos de órgão previstos, é uma pasta fixa do próprio tipo; nos demais, são os três
primeiros caracteres da descrição do tipo de órgão, seguidos de "01". Se o tipo de
órgão da sessão não estiver cadastrado, a pasta vai em branco e a emissão segue assim
mesmo.

### RN-08 — Os quatro códigos passam pela edição numérica

Os quatro códigos da tela — a coordenadoria, as duas partes do lote e o quarto código
— são tratados como número: o que estiver em branco vira zero, os zeros à esquerda são
descartados e o que não for número é recusado, com o cursor de volta ao campo. A
impressora não passa por essa edição.

### RN-09 — O relatório do movimento tem de estar autorizado e registrado

Na abertura, além da conferência da tela, a tela confere o **relatório do movimento**:
ele tem de constar do código de acesso do servidor — não constando, a recusa é
* Acesso negado para esta matricula * e a sessão volta ao menu. Constar do código de
acesso não basta: o relatório também tem de estar registrado entre as telas e
relatórios do sistema.

[?] Quando o relatório não está registrado, a conferência termina **sem mensagem
nenhuma**: o servidor vê a transação abandonada e não sabe por quê. Pergunta ao site.

[?] A tela declara-se de não-manutenção: como ela nunca pede uma operação de
manutenção, a conferência da permissão de operação não chega a exigir nada, e a
recusa * Acesso negado para esta operacao * não é alcançada por ela. Pergunta ao
site.

### RN-10 — A tela abre com a coordenadoria e a impressora preenchidas e mostra a data e o órgão

Ao abrir, a tela preenche a coordenadoria com a da sessão — quando a sessão carrega
uma, o cursor é deixado no campo do lote, e não no da coordenadoria — e a impressora
com a guardada para a matrícula. Mostra também, em campos só de leitura, a data do
sistema e a descrição do tipo de órgão da sessão; esses dois campos de exibição são
limpos quando o pedido é confirmado.

### RN-11 — A tela não encadeia em outra

Esta é a última tela da jornada: o programa não aponta para tela seguinte nenhuma. O
único desvio possível é o da rota — se a transação chegar com uma tela de destino já
preenchida, a tela não valida nem emite nada e leva o servidor para a tela indicada.

[?] Não se sabe quem preenche essa tela de destino nas transações que chegam a esta
tela; o menu que a abre não a informa. Pergunta ao site.

[?] A ficha estrutural diz que a tela alcança uma tela em nenhuma saída, e o programa
não aponta para tela seguinte: ou a tela contada é a do menu a que a conferência
devolve a sessão, ou a contagem vem de outro mecanismo. Divergência a confirmar com
quem mantém o grafo. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedido de emissão do movimento do lote

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão e a coordenadoria regional escolar
    E tenho acesso à tela N330T

  Cenário: A tela pede a emissão do movimento de um lote
    Dado que estou na tela N330T
    Quando informo a coordenadoria, a secretaria, o lote e a impressora e confirmo
    Então o pedido do movimento do lote é entregue ao processamento em lote
    E o pedido leva quem pediu, a coordenadoria, a secretaria, o lote, a impressora
      e o endereço de correio do solicitante
    E a emissão é de uma cópia do relatório do movimento do lote

  Cenário: A tela não mantém cadastro de negócio
    Dado que confirmei um pedido na tela N330T
    Quando o pedido é processado
    Então nenhum cadastro de negócio é incluído, alterado ou excluído
    E o único cadastro escrito é a impressora preferida do servidor
    E um pedido pendente do mesmo lote é apagado da fila de requisições
    E nenhum registro de auditoria é criado

  Cenário: A coordenadoria regional escolar é obrigatória
    Dado que estou na tela N330T
    Quando confirmo sem informar a coordenadoria
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é emitido

  Cenário: Coordenadoria não cadastrada é recusada
    Dado que estou na tela N330T
    Quando informo uma coordenadoria que não existe para o meu tipo de órgão
    Então vejo "* Grupo nao cadastrado *"
    E o cursor fica no campo da coordenadoria
    E nada é emitido

  Cenário: O servidor só pede para a coordenadoria da sua sessão
    Dado que a minha sessão carrega uma coordenadoria
    Quando informo outra coordenadoria
    Então vejo "* Usuario sem acesso a outro grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é emitido

  Cenário: O lote é obrigatório
    Dado que estou na tela N330T
    Quando confirmo com as três partes do lote zeradas
    Então vejo "* Informe numero do lote *"
    E o cursor fica no campo do código da secretaria
    E nada é emitido

  Cenário: O lote é aceito com uma das três partes informada
    Dado que estou na tela N330T
    Quando informo apenas uma das três partes do lote e confirmo
    Então o lote é aceito
    E o pedido segue com o número de 12 dígitos montado a partir das três partes

  Cenário: O endereço de correio do servidor é exigido
    Dado que estou na tela N330T
    E que o meu registro de servidor não tem endereço de correio
    Quando confirmo o pedido
    Então vejo "* Usuario sem e-mail cadastrado *"
    E nada é emitido

  Cenário: A impressora preferida do servidor é preenchida e mantida
    Dado que estou na tela N330T
    Então o campo da impressora já vem com a impressora guardada para a minha matrícula
    Quando informo outra impressora e confirmo o pedido
    Então a impressora guardada para a minha matrícula passa a ser a informada

  Cenário: A impressora é obrigatória
    Dado que estou na tela N330T
    Quando confirmo o pedido sem informar a impressora
    Então vejo "* Informe a impressora *"
    E o cursor fica no campo da impressora
    E nada é emitido

  Cenário: A emissão apaga o pedido pendente do lote e dispara o movimento
    Dado que estou na tela N330T
    E que existe um pedido de movimento pendente para o lote
    Quando confirmo a emissão
    Então o pedido pendente daquele lote é apagado da fila de requisições
    E o movimento é entregue ao processamento em lote
    E o pedido leva a pasta de saída do meu tipo de órgão

  Cenário: Código que não é número é recusado
    Dado que estou na tela N330T
    Quando informo, na coordenadoria ou em uma das partes do lote, algo que não é número
    Então a confirmação é recusada antes de qualquer consulta
    E o cursor volta ao campo recusado
    E nada é emitido

  Cenário: O relatório do movimento tem de estar autorizado
    Dado que estou na tela N330T
    E que o meu código de acesso não alcança o relatório do movimento
    Quando confirmo o pedido
    Então vejo "* Acesso negado para esta matricula *"
    E a sessão volta ao menu
    E nada é emitido

  Cenário: A tela abre com a coordenadoria, a impressora, a data e o órgão
    Dado que a minha sessão carrega uma coordenadoria e uma impressora guardada
    Quando abro a tela N330T
    Então o campo da coordenadoria já vem com a coordenadoria da sessão
    E o campo da impressora já vem com a impressora guardada para a minha matrícula
    E a tela mostra a data do sistema e a descrição do tipo de órgão da sessão
    Quando confirmo o pedido
    Então os dois campos de exibição são limpos

  Cenário: A tela não encadeia em outra
    Dado que confirmei um pedido na tela N330T
    Quando o processamento recebe o pedido
    Então a tela não me leva para nenhuma outra tela
    E, se a transação chegar com uma tela de destino preenchida, sou levado para ela
      sem que nada seja validado nem emitido
```
