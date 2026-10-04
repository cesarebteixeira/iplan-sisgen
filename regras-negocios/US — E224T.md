# US — E224T — Emitir o resumo da carga de um lote

## Estória

Como **servidor de CRE**, quero **pedir a emissão do resumo da carga de um lote,
informando a coordenadoria regional escolar, o código da secretaria, o código do
lote e a impressora**, para que **o processamento daquele lote seja executado e o
seu resumo saia na minha impressora**.

O resumo da carga não é montado na tela: quem o produz é o processamento em lote, e o
que esta tela faz é reunir o pedido e entregá-lo ao trabalho que o executa. Sem o
pedido não há trabalho, e o pedido só chega ao lugar certo se a coordenadoria, a
secretaria e o lote estiverem certos, porque é por eles que a carga é localizada e é
deles que sai a pasta em que o trabalho vai procurá-la. É também esta tela que mantém
atualizada a impressora preferida de quem pede, de modo que a próxima emissão já saia
endereçada. Se a tela não existisse, o lote ficaria sem o seu resumo impresso, e quem
opera teria de entregar o trabalho por fora do sistema.

## Contexto

Jornada S000M → E000M → E200M → E220M → E224T.

Ator: servidor de CRE — informa a coordenadoria regional escolar, o código da
secretaria, o código do lote e a impressora e confirma; a tela entrega o pedido ao
processamento em lote e termina nela mesma.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Das telas anteriores a tela usa o que a entrada deixou na sessão: a matrícula, o
código de acesso, o privilégio, o tipo de órgão, a coordenadoria regional escolar e a
data e a descrição do órgão. A tela que a abre não deixa registro nem operação — esta
tela abre em branco, com o contexto da sessão, e não muda de comportamento por causa
de quem a chamou (RN-04). Ela não abre outra tela: termina nela mesma.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela pede a emissão do resumo da carga de um lote, e não monta o relatório

A tela não monta o relatório: ela reúne o pedido e o entrega ao processamento em lote,
que faz o trabalho e emite o resumo da carga daquele lote na impressora indicada. O
relatório é sempre o mesmo, com **uma cópia**, e o pedido leva a impressora escolhida,
o tipo de órgão e a coordenadoria da sessão, a coordenadoria e a secretaria
informadas, o número do lote, a pasta de saída do órgão e o endereço de correio do
servidor. Nada disso é gravado por aqui: a tela só entrega o trabalho, e não confirma
ao operador que ele foi entregue.

[?] O trecho que monta e entrega o trabalho foi lido, mas o programa que ele executa
não está no acervo com o nome do trabalho e não há catálogo de trabalhos no lote que
faça essa ligação. O programa de lote cujo código de relatório é o mesmo que esta tela
usa se intitula "Resumo da Carga" e imprime a linha do lote e o resumo dos pedidos
lidos, cadastrados e rejeitados; ele é o candidato, mas se é ele que roda, ou outro,
não se conclui do fonte. Pergunta ao site.

### RN-02 — A tela não mantém cadastro: lê seis cadastros e escreve em dois

Para montar o pedido a tela consulta **seis cadastros** — o das telas, o do servidor,
o das coordenadorias regionais escolares, o dos tipos de órgão, o da impressora do
servidor e a fila de requisições de impressão — e escreve em **dois**: a impressora do
próprio servidor, alterada ou criada, e a fila de requisições, de onde apaga um pedido.
Nenhum outro cadastro é incluído, alterado ou excluído, e a tela não deixa registro de
auditoria.

### RN-03 — Ao abrir, a tela propõe a coordenadoria da sessão e a impressora guardada

Ao ser aberta, a tela preenche o campo da coordenadoria regional escolar com a
**coordenadoria do vínculo da sessão** e o campo da impressora com a **impressora
guardada para a matrícula** do servidor. Quando o vínculo não tem coordenadoria, o
campo fica em branco, para ele informar, e o cursor fica nele; quando a coordenadoria
veio da sessão, o cursor fica no campo do código da secretaria. O cabeçalho mostra a
descrição do órgão da sessão e a data do sistema. Abrir a tela não grava nem emite
nada: a abertura só lê.

### RN-04 — A entrada da tela não traz registro nem operação, e o comportamento não muda por causa de quem a chamou

A tela que a abre encaminha só a tela: não deixa registro nem operação. Esta tela abre
em branco, com o contexto da sessão — nenhum lote, nenhuma coordenadoria informada e
nenhuma impressora vêm de quem a chamou. Também não há, no programa, comparação da
tela de origem com código de tela nenhum: o comportamento desta tela é o mesmo
qualquer que seja a origem, e o código de operação (consulta, inclusão, alteração)
chega com a própria tela, e não de quem a chamou. É esse código que decide se a
emissão passa (RN-11).

### RN-05 — A coordenadoria regional escolar é obrigatória, tem de existir e é a da sessão

A coordenadoria regional escolar é exigida, tem de estar cadastrada para o **tipo de
órgão da sessão** e, quando o vínculo da sessão já carrega uma coordenadoria, tem de
ser essa mesma. As recusas são **\* Usuario sem acesso a outro grupo \***, quando o
vínculo tem coordenadoria e a informada é outra; **\* Informe o grupo \***, quando o
vínculo não tem coordenadoria e o campo está em branco; e **\* Grupo nao cadastrado \***,
quando ela não existe para o tipo de órgão da sessão. Nas três o cursor volta ao campo
da coordenadoria e nada é emitido. Quando o vínculo não tem coordenadoria, qualquer
coordenadoria cadastrada passa.

[?] Um servidor cujo vínculo não tem coordenadoria pede o resumo da carga de qualquer
coordenadoria. Se isso é intencional, ou se deveria haver outro recorte, é pergunta ao
site.

[?] Com vínculo preenchido e o campo em branco, a mensagem que aparece é a de acesso a
outro grupo, e não a de campo em branco: a conferência de acesso vem antes da de
preenchimento. Se é a mensagem que o site espera nesse caso, é pergunta ao site.

### RN-06 — O lote é informado em três partes e é obrigatório

O lote é informado em três partes — o **código da secretaria**, com 2 dígitos; o
**código do lote**, com 6; e mais **quatro dígitos que a tela não rotula** — e o
sistema as junta num único número de 12 dígitos, que é o que identifica o lote no
pedido. Basta uma das três estar preenchida; com as três zeradas a recusa é
**\* Informe numero do lote \*** e o cursor volta ao campo do código da secretaria. Os
campos numéricos passam por edição numérica antes das conferências e o campo em branco
é tratado como zero; entre os campos que o operador preenche, a impressora é o único
de texto.

[?] O que os quatro últimos dígitos identificam não está no acervo: o campo não tem
rótulo de negócio no programa e o fonte não diz o que ele é. O código de secretaria
informado também **não** é conferido contra a secretaria da sessão — só a
coordenadoria é. Pergunta ao site.

[?] O que o operador vê quando digita algo que não é número não se conclui desta tela:
a rotina que faz a edição numérica não está no acervo. Pergunta ao site.

### RN-07 — O servidor precisa ter e-mail cadastrado

Antes de emitir, a tela procura o registro do servidor pela matrícula da sessão e
exige que ele tenha **e-mail**: sem e-mail, a recusa é
**\* Usuario sem e-mail cadastrado \*** e nada é emitido. O endereço encontrado segue
no pedido.

[?] A recusa é sobre o e-mail, mas o cursor volta ao campo da coordenadoria — o e-mail
não está nesta tela. Se é intencional apontar para outro campo, é pergunta ao site.

### RN-08 — A impressora é obrigatória e a tela mantém a preferida do servidor

A impressora é exigida — **\* Informe a impressora \***, com o cursor nela. Na
abertura o campo já vem com a impressora guardada para a matrícula do servidor; ao
confirmar o pedido essa preferência é mantida atualizada: se a informada for diferente
da guardada, a guardada passa a ser a informada; se o servidor ainda não tiver nenhuma
guardada, o registro é criado com a informada. Esse cadastro é dimensionado para
**10 mil** registros — capacidade (máximo esperado no dimensionamento), não volume
cadastrado.

[?] A criação do registro, quando ele não existe, passa por uma conferência de destino
que a própria tela não comanda: os dois desfechos dessa conferência leem a mesma
comparação em sentidos opostos, e a tela apaga a marca de distribuição automática
imediatamente antes de executar o trecho. A recusa de destino inválido existe no
caminho, mas é **inalcançável** por esta tela, e qual dos desfechos vale no site não se
conclui do fonte. Pergunta ao site.

### RN-09 — Antes de entregar o trabalho, a tela apaga o pedido pendente do mesmo lote

Antes de entregar o trabalho, a tela procura na fila de requisições de impressão o
pedido daquele relatório para aquele lote, **com a situação em branco e ainda sem
número de requisição**, e apaga o que encontrar, repetindo a procura enquanto houver;
só depois entrega o trabalho. Assim não fica um pedido pendente do mesmo lote. A
procura é pelo relatório e pelo lote, e **não** por quem pediu: o pedido pendente
daquele lote é apagado por qualquer servidor que confirme a emissão daquele lote. Não
havendo pedido pendente, nada é apagado. Esta tela **não** cria o pedido na fila.

[?] O que a situação em branco significa não está no acervo: outra tela do sistema
rotula três situações da fila — requisitado, processando e terminado — e deixa a
quarta sem rótulo. Quem cria o registro na fila também não é esta tela. Se o pedido
novo já nasce com situação preenchida, esta tela nunca encontra nada para apagar. Não
escolhi um dos dois lados. Pergunta ao site.

### RN-10 — A pasta de saída do pedido acompanha o tipo de órgão da sessão

O pedido leva a pasta em que a carga deve ser deixada, montada a partir do **tipo de
órgão da sessão** e da **coordenadoria regional escolar**: para o tipo de órgão da
CRE a pasta é a da coordenadoria da sessão, para os dois outros tipos previstos são
pastas fixas do próprio tipo, e para os demais é a pasta do órgão da sessão. Se o
órgão da sessão não estiver cadastrado, a pasta vai em branco e a emissão segue assim
mesmo.

### RN-11 — Nada é emitido sem a conferência de sessão, de tela, do relatório, da rota e da operação

Na abertura a tela confere o servidor, a tela e o relatório: o servidor tem de estar no
**terminal em que a sessão foi aberta** — em outro, o acesso é encerrado e a sessão
volta à entrada; a tela tem de estar registrada, senão **\* Tela nao disponivel \***;
o código de acesso do servidor tem de alcançar a tela, senão
**\* Acesso negado para esta matricula \***; e o relatório do resumo da carga tem de
estar registrado e autorizado para esse código de acesso. Na confirmação a rota e a
operação são conferidas: a tela tem de estar registrada, senão
**\* Tela nao cadastrada \***; uma operação de inclusão, alteração ou exclusão é
recusada com **\* Operacao nao disponivel \*** — a tela não mantém nada —; e as
operações de retorno e de menu levam às telas anterior e de menu registradas para esta
tela. Sem passar por tudo, nada é emitido, nada é apagado da fila e a impressora não é
atualizada.

[?] Quando o relatório não está registrado, a conferência termina **sem mensagem
nenhuma**: o servidor vê a transação abandonada e não sabe por quê. Pergunta ao site.

[?] Quem preenche o código de operação desta tela não está no programa: ele chega
pronto na transação e é ele que decide se a emissão passa. Se a tela mandar inclusão,
alteração ou exclusão, a emissão nunca acontece, e a máscara da tela não veio no lote.
Pergunta ao site.

[?] A conferência de segurança recebe a **coordenadoria da sessão**, e não a
coordenadoria informada na tela: o grupo digitado é conferido depois, pela própria
tela (RN-05). Se a intenção era a conferência de segurança recusar o grupo digitado, o
caminho não o faz. Pergunta ao site.

### RN-12 — Toda confirmação é uma emissão nova: a tela não tem caminho de reimpressão

Repetir a confirmação é pedir o relatório de novo, e não reimprimir o que já saiu. A
tela conhece os dados de um pedido de reimpressão — o relatório, a impressora, uma
cópia, a estação e o texto da reimpressão — e repõe essa área a cada transação, mas
nunca pede um trabalho de reimpressão: o único trabalho que ela entrega é o da
emissão.

### RN-13 — A recusa e a abertura não gravam nada

A tela só escreve quando a confirmação passa por todas as conferências: cada recusa
encerra a passagem **antes** das gravações e antes do trabalho, de modo que uma
confirmação recusada não apaga pedido da fila nem altera a impressora do servidor. A
simples abertura da tela também não grava nem emite nada.

[?] A tela apaga o pedido pendente do lote **antes** de conferir se está no ambiente
previsto; fora desse ambiente, o pedido do lote é apagado sem que o trabalho seja
entregue. Se esse ambiente ocorre no site, é pergunta ao site.

[?] Quem marca a falha que interrompe a passagem não está no programa: as recusas
exibem a mensagem e desviam para o fim, mas a rotina comum de mensagem, que é quem
marca o estado de falha consultado adiante, não está no acervo. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Emitir o resumo da carga de um lote

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão e a coordenadoria regional escolar
    E tenho acesso à tela E224T

  Cenário: A tela pede a emissão do resumo da carga de um lote
    Dado que estou na tela E224T
    Quando informo a coordenadoria, o código da secretaria, o código do lote e a impressora e confirmo
    Então o resumo da carga daquele lote é pedido ao processamento em lote
    E o pedido leva uma cópia, a impressora, o meu endereço de correio e a pasta de
      saída do meu órgão
    E nada do pedido é gravado por esta tela

  Cenário: A abertura da tela propõe a coordenadoria e a impressora
    Dado que o meu vínculo tem coordenadoria
    E que existe impressora guardada para a minha matrícula
    Quando abro a tela E224T
    Então o campo da coordenadoria vem preenchido com a coordenadoria do meu vínculo
    E o campo da impressora vem preenchido com a impressora guardada para a minha matrícula
    E o cursor fica no campo do código da secretaria
    E vejo a descrição do órgão da minha sessão e a data do sistema

  Cenário: A abertura da tela não grava nem emite
    Dado que o meu vínculo não tem coordenadoria
    Quando abro a tela E224T e ainda não confirmo nada
    Então o campo da coordenadoria fica em branco e o cursor fica nele
    E nenhum trabalho é entregue ao processamento em lote
    E nenhum pedido é apagado da fila
    E a impressora guardada para a minha matrícula não é alterada

  Cenário: A tela abre sem registro e sem operação vindos de quem a chamou
    Dado que a tela anterior me encaminhou a esta
    Quando a tela E224T abre
    Então nenhum lote e nenhuma coordenadoria informada vêm preenchidos por ela
    E a tela abre com o contexto da minha sessão
    E o comportamento dela é o mesmo, qualquer que tenha sido a origem

  Cenário: A tela não mantém cadastro
    Dado que confirmei um pedido de emissão na tela E224T
    Quando o pedido é processado
    Então nenhum cadastro de negócio é incluído ou alterado
    E o único cadastro escrito é a impressora preferida do servidor
    E o pedido pendente do lote é apagado da fila de requisições
    E nenhum registro de auditoria é criado

  Cenário: A coordenadoria é obrigatória
    Dado que o meu vínculo não tem coordenadoria
    Quando confirmo sem informar a coordenadoria
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é emitido

  Cenário: Coordenadoria em branco com vínculo preenchido
    Dado que a minha sessão carrega uma coordenadoria
    Quando confirmo sem informar a coordenadoria
    Então vejo "* Usuario sem acesso a outro grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é emitido

  Cenário: Coordenadoria não cadastrada
    Dado que estou na tela E224T
    Quando informo uma coordenadoria que não existe para o meu tipo de órgão
    Então vejo "* Grupo nao cadastrado *"
    E o cursor fica no campo da coordenadoria
    E nada é emitido

  Cenário: O servidor só pede para a coordenadoria da sua sessão
    Dado que a minha sessão carrega uma coordenadoria
    Quando informo outra coordenadoria e confirmo
    Então vejo "* Usuario sem acesso a outro grupo *"
    E o cursor fica no campo da coordenadoria
    E nada é emitido

  Cenário: O lote é obrigatório
    Dado que estou na tela E224T
    Quando confirmo com as três partes do lote zeradas
    Então vejo "* Informe numero do lote *"
    E o cursor fica no campo do código da secretaria
    E nada é emitido

  Cenário: O lote é aceito com uma das três partes informada
    Dado que estou na tela E224T
    Quando informo apenas uma das três partes do lote e confirmo
    Então o lote é aceito
    E o pedido segue com o número de 12 dígitos montado a partir das três partes

  Cenário: O e-mail do servidor é exigido
    Dado que o meu registro de servidor não tem e-mail cadastrado
    Quando confirmo o pedido
    Então vejo "* Usuario sem e-mail cadastrado *"
    E o cursor fica no campo da coordenadoria
    E nada é emitido

  Cenário: A impressora é obrigatória
    Dado que estou na tela E224T
    Quando confirmo o pedido sem informar a impressora
    Então vejo "* Informe a impressora *"
    E o cursor fica no campo da impressora
    E nada é emitido

  Cenário: A impressora informada passa a ser a preferida do servidor
    Dado que existe impressora guardada para a minha matrícula
    Quando informo outra impressora e confirmo o pedido
    Então a impressora guardada para a minha matrícula passa a ser a informada
    E, se eu ainda não tiver nenhuma guardada, o registro é criado com a informada

  Cenário: A emissão apaga o pedido pendente do mesmo lote
    Dado que existe um pedido pendente daquele relatório para aquele lote, com a
      situação em branco e sem número de requisição
    Quando confirmo a emissão
    Então o pedido pendente daquele lote é apagado da fila
    E o resumo da carga do lote é pedido de novo

  Cenário: O pedido pendente é apagado mesmo tendo sido pedido por outro servidor
    Dado que o pedido pendente daquele lote foi feito por outro servidor
    Quando confirmo a emissão daquele lote
    Então o pedido pendente é apagado da mesma forma

  Cenário: Sem pedido pendente nada é apagado
    Dado que não existe pedido pendente para aquele relatório e aquele lote
    Quando confirmo a emissão
    Então nenhum registro da fila é apagado
    E o resumo da carga do lote é pedido

  Cenário: A pasta de saída acompanha o tipo de órgão da sessão
    Dado que a minha sessão carrega um tipo de órgão
    Quando confirmo a emissão
    Então o pedido leva a pasta de saída que corresponde ao meu tipo de órgão
    E, para o tipo de órgão da CRE, a pasta é a da coordenadoria da sessão

  Cenário: Nada é emitido sem a conferência de sessão, de tela, do relatório, da rota e da operação
    Dado que estou na tela E224T
    Quando a conferência do terminal, do registro da tela, do código de acesso, do
      relatório, da rota ou da operação não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *",
      "* Operacao nao disponivel *" ou "* Tela nao cadastrada *"
    E nada é emitido, nada é apagado da fila e a impressora não é atualizada
    E, se o terminal não for o da sessão, o acesso é encerrado

  Cenário: Operação de manutenção é recusada
    Dado que estou na tela E224T, que é de consulta e de emissão
    Quando a transação chega com uma operação de inclusão, alteração ou exclusão
    Então vejo "* Operacao nao disponivel *"
    E nada é emitido

  Cenário: Repetir a confirmação é pedir o relatório de novo
    Dado que já pedi o resumo da carga de um lote
    Quando confirmo a mesma tela outra vez
    Então o relatório daquele lote é pedido de novo
    E nenhuma reimpressão do que já saiu é solicitada

  Cenário: A confirmação recusada não grava nada
    Dado que estou na tela E224T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então nenhum pedido foi apagado da fila
    E a impressora guardada para a minha matrícula não foi alterada
    E nenhum trabalho foi entregue ao processamento em lote
```
