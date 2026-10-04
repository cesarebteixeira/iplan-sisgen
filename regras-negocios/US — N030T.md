# US — N030T — Pedido de emissão e reimpressão do movimento do lote

## Estória

Como **servidor da CRE**, quero **pedir a emissão do movimento de um lote, ou a
reimpressão de um movimento que já foi pedido**, para que **a relação do lote saia
na minha impressora sem eu depender de quem opera o processamento em lote**.

O movimento não é montado na tela: quem o produz é o processamento em lote, e o que
a tela faz é reunir o pedido e entregá-lo. Sem o pedido, o processamento não tem
trabalho a executar; e a reimpressão só existe para um lote cujo movimento já tenha
sido pedido antes — é do pedido anterior que ela reaproveita os parâmetros. A tela
não mantém cadastro de negócio nenhum: o único registro que ela atualiza é a
impressora preferida do próprio servidor.

## Contexto

Jornada S000M → N000M → N050M → N030T.

Ator: servidor de CRE — informa a coordenadoria regional escolar, o código da
secretaria e o código do lote, escolhe a impressora e pede a emissão do movimento
(ou liga a reimpressão).

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As três telas que antecedem esta são menus: tanto a `N000M` quanto a `N050M` têm
opções declaradas, e é por uma opção da `N050M` que a `N030T` abre. A tela desta
jornada **não** recebe operação encadeada de quem a chamou — ela abre no seu próprio
modo e o decide por si, e não muda de comportamento conforme a tela de origem. O que
ela usa — matrícula, código de acesso, privilégio, tipo de órgão e coordenadoria
regional escolar — é o que a entrada deixou na sessão, e a `N030T` apenas o repassa
às conferências e ao pedido. As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela pede a emissão do movimento de um lote

A tela não monta o movimento: ela reúne o pedido — a coordenadoria regional
escolar, a secretaria, o lote, a impressora escolhida, quem pediu e o endereço de
correio do solicitante — e o entrega ao processamento em lote, que é quem produz a
relação. O pedido é sempre do mesmo relatório, o movimento; a tela não deixa
escolher outro, e a emissão é sempre de uma cópia.

[?] O trabalho pedido é o `J/M104/ATU/0010/MOVIMENTO`: o trecho que o dispara foi
lido, mas o programa que ele executa não está no acervo — não se sabe se é ele que
monta o movimento, se é ele que grava o pedido na fila, nem o que o "MOVIMENTO" do
nome designa. Pergunta ao site.

### RN-02 — A tela não mantém cadastro: lê seis e escreve em dois

A tela enxerga seis cadastros — o registro das telas, o registro do servidor, o das
coordenadorias regionais escolares, o dos tipos de órgão, o da impressora do
servidor e a fila de requisições de impressão — e escreve em apenas **dois**: a
impressora do próprio servidor e a fila de requisições. Nenhum outro cadastro é
incluído, alterado ou excluído, e a tela não deixa rastro de auditoria.

### RN-03 — A coordenadoria regional escolar é obrigatória, tem de existir e é a da sessão

A tela exige a coordenadoria (o grupo). Se ela vier em branco, a recusa é
* Informe o grupo *; se não estiver cadastrada para o tipo de órgão da sessão,
* Grupo nao cadastrado *. Quando a sessão já carrega uma coordenadoria, o servidor
só pode pedir para essa: informar outra é recusado com
* Usuario sem acesso a outro grupo *. Ao abrir, a tela já sugere a coordenadoria da
sessão. Nas três recusas o cursor volta ao campo da coordenadoria.

### RN-04 — O código do lote é obrigatório e vem em três partes

O lote é informado em três partes — o código da secretaria, com 2 dígitos; o código
do lote, com 6; e mais quatro dígitos que o sistema não rotula — e o sistema as
junta num único número de 12 dígitos. Basta uma das três estar preenchida para o
lote ser aceito; com as três zeradas a recusa é * Informe numero do lote * e o
cursor volta ao campo da secretaria.

[?] O que os quatro últimos dígitos do lote identificam não está no acervo: esse
campo não tem rótulo na tela nem no fonte, e nada mais o explica. E o código de
secretaria informado no lote **não** é conferido contra a secretaria da sessão —
só a coordenadoria é. Pergunta ao site.

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
nenhuma guardada, o registro é criado com a informada. A preferência é por
servidor, e esse cadastro é dimensionado para **10 mil** registros — capacidade
(máximo esperado, parâmetro de dimensionamento), não volume cadastrado.

[?] A criação do registro, quando ele não existe, passa por uma escolha que o
próprio programa não comanda: conforme o destino calculado coincida ou não com a
origem, a gravação local é trocada por um encaminhamento a outro ambiente. Nenhum
fonte do acervo determina esse destino para esta transação. Pergunta ao site.

### RN-07 — A emissão nova apaga o pedido pendente do lote e dispara o movimento

Quando o indicador de reimpressão está desligado, a tela procura na fila de
requisições o pedido de movimento **pendente** daquele lote e apaga o que
encontrar, para não ficar um pedido pendente do mesmo lote; em seguida entrega ao
processamento em lote o trabalho do movimento, com os dados do pedido: o relatório,
a impressora, uma cópia, a matrícula, o tipo de órgão, a coordenadoria, o lote, o
endereço de correio e a pasta de saída do órgão. A pasta de saída acompanha o tipo
de órgão da sessão: para a CRE, a coordenadoria informada; para os órgãos "SMS" e
"SMA", o seu próprio código; nos demais, a descrição do tipo de órgão.

### RN-08 — A reimpressão exige um movimento já pedido para o lote

Com o indicador de reimpressão ligado, a tela não apaga nada: ela procura na fila o
pedido de movimento daquele lote e, não encontrando, recusa com
* Lote sem relatorio para reimpressao *, com o cursor no campo da secretaria —
nada é reimpresso.

### RN-09 — A reimpressão reaproveita os parâmetros do pedido anterior

Encontrando o pedido do lote, a tela manda reimprimir usando os parâmetros
guardados naquele pedido, junto com a impressora informada agora. A reimpressão,
portanto, reproduz o que foi pedido antes, e não o que estiver na tela no momento —
só a impressora é a de agora.

[?] A conferência que exige o pedido trata como "encontrado" um registro em que o
lote guardado não confere com o informado, e a tela prossegue para a reimpressão
mesmo assim. Se isso é intencional, ou se é defeito da conferência, não se decide
pelo fonte. Pergunta ao site.

### RN-10 — A tela abre sempre com a reimpressão desligada

Toda abertura da tela repõe o indicador de reimpressão em "não". É o servidor que o
liga, na mesma passagem, para pedir a reimpressão; desligado, o pedido é de emissão
nova.

[?] O que o servidor vê e como ele liga esse indicador não se sabe: a máscara da
tela não veio no lote e o rótulo do indicador não está no fonte. Se a máscara não
expuser o campo, o caminho da reimpressão nunca é alcançado e toda confirmação
seria de emissão nova. Pergunta ao site.

### RN-11 — Nada é emitido sem a conferência de sessão, de tela, de relatório, de rota e de operação

Ao abrir, a tela confere: o servidor tem de estar no terminal em que a sessão foi
aberta — em outro, o acesso é encerrado; a tela tem de estar registrada, senão
* Tela nao disponivel *; o código de acesso do servidor tem de alcançar a tela,
senão * Acesso negado para esta matricula *; e o relatório do movimento tem de estar
autorizado para esse código, com a mesma recusa. Na confirmação, a rota e a operação
são conferidas: um modo de manutenção que a tela não realiza é recusado com
* Operacao nao disponivel *, e uma tela fora do registro com * Tela nao cadastrada *.
Sem passar por tudo, nada é emitido, nada é apagado da fila e a impressora não é
atualizada.

[?] A tela declara-se de não-manutenção: como ela nunca pede uma operação de
manutenção, a conferência da permissão de operação não chega a exigir nada, e a
recusa * Acesso negado para esta operacao * não é alcançada por ela. Pergunta ao
site.

[?] Quando o relatório não está registrado, a conferência termina **sem mensagem
nenhuma**: o servidor vê a transação abandonada e não sabe por quê. Pergunta ao
site.

### RN-12 — Prefixo de rota preenchido desvia a tela

Se a transação chega com o prefixo de rota preenchido, a tela não valida nem emite
nada: a rota leva o servidor para a tela indicada nesse prefixo. A `N050M`, que é o
menu de onde esta tela é aberta, não preenche esse prefixo.

[?] Não se sabe quem preenche o prefixo de rota nas transações que chegam a esta
tela. Pergunta ao site.

### RN-13 — A tela não apresenta a recusa de destino inválido

A recusa de **destino inválido** existe no trecho que a tela executa para guardar a
impressora do servidor, e a ficha estrutural da tela a lista entre as suas
mensagens. Esse trecho só produz a recusa com o modo de distribuição automática
preenchido, e a própria tela limpa esse campo imediatamente antes de executá-lo.
Pela `N030T`, portanto, essa mensagem não é apresentada.

[?] Divergência entre a ficha e o comportamento, sem explicação no acervo: ou a
guarda vale para outro caso, ou o caminho ficou inalcançável. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedido de emissão e reimpressão do movimento do lote

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão e a coordenadoria regional escolar
    E tenho acesso à tela N030T

  Cenário: A tela pede a emissão do movimento de um lote
    Dado que estou na tela N030T
    Quando informo a coordenadoria, a secretaria, o lote e a impressora e confirmo
    Então o pedido do movimento do lote é entregue ao processamento em lote
    E o pedido leva quem pediu, a coordenadoria, a secretaria, o lote, a impressora
      e o endereço de correio do solicitante

  Cenário: A tela não mantém cadastro
    Dado que confirmei um pedido de emissão na tela N030T
    Quando o pedido é processado
    Então nenhum cadastro de negócio é incluído, alterado ou excluído
    E o único cadastro escrito é a impressora preferida do servidor
    E nenhum registro de auditoria é criado

  Cenário: A coordenadoria regional escolar é obrigatória
    Dado que estou na tela N030T
    Quando confirmo sem informar a coordenadoria
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é emitido

  Cenário: Coordenadoria não cadastrada é recusada
    Dado que estou na tela N030T
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
    Dado que estou na tela N030T
    Quando confirmo com as três partes do lote zeradas
    Então vejo "* Informe numero do lote *"
    E o cursor fica no campo do código da secretaria
    E nada é emitido

  Cenário: O lote é aceito com uma das três partes informada
    Dado que estou na tela N030T
    Quando informo apenas uma das três partes do lote e confirmo
    Então o lote é aceito
    E o pedido segue com o número de 12 dígitos montado a partir das três partes

  Cenário: O endereço de correio do servidor é exigido
    Dado que estou na tela N030T
    E que o meu registro de servidor não tem endereço de correio
    Quando confirmo o pedido
    Então vejo "* Usuario sem e-mail cadastrado *"
    E nada é emitido

  Cenário: A impressora preferida do servidor é preenchida e mantida
    Dado que estou na tela N030T
    Então o campo da impressora já vem com a impressora guardada para a minha matrícula
    Quando informo outra impressora e confirmo o pedido
    Então a impressora guardada para a minha matrícula passa a ser a informada

  Cenário: A impressora é obrigatória
    Dado que estou na tela N030T
    Quando confirmo o pedido sem informar a impressora
    Então vejo "* Informe a impressora *"
    E o cursor fica no campo da impressora
    E nada é emitido

  Cenário: A emissão nova apaga o pedido pendente do lote e dispara o movimento
    Dado que estou na tela N030T com a reimpressão desligada
    E que existe um pedido de movimento pendente para o lote
    Quando confirmo a emissão
    Então o pedido pendente daquele lote é apagado da fila
    E o movimento é entregue ao processamento em lote
    E nada é reimpresso

  Cenário: A reimpressão exige movimento já pedido para o lote
    Dado que estou na tela N030T com a reimpressão ligada
    E que não existe pedido de movimento para o lote
    Quando confirmo
    Então vejo "* Lote sem relatorio para reimpressao *"
    E o cursor fica no campo do código da secretaria
    E nada é reimpresso

  Cenário: A reimpressão reaproveita os parâmetros do pedido anterior
    Dado que estou na tela N030T com a reimpressão ligada
    E que existe pedido de movimento para o lote
    Quando confirmo
    Então a reimpressão é entregue ao processamento em lote com os parâmetros
      guardados naquele pedido
    E com a impressora informada agora

  Cenário: A tela abre com a reimpressão desligada
    Dado que abro a tela N030T
    Então o indicador de reimpressão está desligado
    Quando confirmo sem ligá-lo
    Então o pedido é de emissão nova, e não de reimpressão

  Cenário: Nada é emitido sem a conferência de sessão, tela, relatório, rota e operação
    Dado que estou na tela N030T
    Quando a conferência do terminal, do registro da tela, do código de acesso,
      do relatório, da rota ou da operação não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *",
      "* Operacao nao disponivel *" ou "* Tela nao cadastrada *"
    E nada é emitido, nada é apagado da fila e a impressora não é atualizada
    E, se o terminal não for o da sessão, o acesso é encerrado

  Cenário: Prefixo de rota preenchido desvia a tela
    Dado que a transação chega à tela N030T com o prefixo de rota preenchido
    Quando a tela começaria a validar
    Então sou levado para a tela indicada no prefixo
    E nada é emitido

  Cenário: A recusa de destino inválido não é apresentada
    Dado que estou na tela N030T e confirmei o pedido
    Quando a impressora do servidor é guardada
    Então a tela limpa o modo de distribuição automática
    E a recusa de destino inválido não é apresentada
```
