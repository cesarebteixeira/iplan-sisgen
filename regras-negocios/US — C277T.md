# US — C277T — Percentual da atualização do cadastro de atendimento

## Estória

Como **servidor da CRE**, quero **registrar o percentual que a atualização do cadastro de
atendimento deve aplicar ao tipo de órgão da minha secretaria e decidir se ela roda agora**,
para que **os quantitativos de atendimento de cada órgão da minha secretaria sejam
recalculados de uma vez, sem ninguém refazer a conta registro por registro**.

O percentual é o que converte o atendimento apurado no quantitativo que cabe a cada órgão: a
atualização do cadastro lê o percentual registrado para o tipo de órgão e o aplica sobre o
total apurado. Sem percentual registrado, a atualização não tem por onde recalcular. E o
pedido de atualização precisa ser único por tipo de órgão e coordenação: dois pedidos ao
mesmo tempo trabalhariam o mesmo cadastro.

## Contexto

Jornada S000M → C000M → C028M → C277T.

Ator: servidor de CRE — registra o percentual da atualização do cadastro de atendimento do
tipo de órgão da sua secretaria e decide se ela roda agora.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A tela trabalha com um registro só: mostra o percentual que o tipo de órgão já tem e recebe,
junto com ele, a resposta a **Atualiza Cadastro <S/N>?**. O tipo de órgão, a coordenação
regional escolar, a matrícula de quem opera, o código de acesso e o terminal chegam pela
sessão, carregados na entrada a partir do vínculo da matrícula com a secretaria: a tela não
pergunta nada disso. A opção de manutenção fica na própria tela, e é ela que decide se o
servidor consulta ou altera. A tela **não** encadeia em outra: depois do pedido, ela volta
para si mesma.

As regras abaixo são só as da tela desta jornada; as da entrada não se repetem aqui.

## Regras de negócio

### RN-01 — A tela mantém um percentual por tipo de órgão

O cadastro por trás da tela guarda **quatro dados**: o percentual, a matrícula de quem o
registrou, a data em que isso aconteceu e o tipo de órgão. O tipo de órgão é o que identifica
o registro: a tela não pergunta de qual tipo de órgão se trata e não há como manter o
percentual de outro.

[?] O cadastro do percentual não está no dicionário de dados entregue com o acervo: nem ele,
nem a chave pela qual a tela o lê aparecem lá. Pelo fonte só se sabe que a leitura é feita
pelo tipo de órgão; se um mesmo tipo de órgão poderia ter mais de um percentual, e qual é a
capacidade do cadastro, o dicionário não diz. Pergunta ao site.

### RN-02 — A tela abre em consulta, com o percentual vigente

Aberta sem opção de manutenção informada, a tela assume a **consulta** e mostra o percentual
que o tipo de órgão já tem — zerado, quando não tem nenhum —, a descrição do tipo de órgão, a
data do sistema e a pergunta **Atualiza Cadastro <S/N>?**, cuja resposta fica no campo ao
lado. O percentual aparece no campo editado como número, sem os zeros à esquerda.

[?] A opção de manutenção chega à tela pelo contexto de trabalho que a tela anterior deixa,
e o menu desta jornada não informa nenhuma: por este caminho a tela abre em consulta. Se
alguma origem a abre já em alteração, o fonte desta jornada não mostra: a tela não compara a
tela de origem com código nenhum para decidir isso. Pergunta ao site.

### RN-03 — A tela só executa com alteração ou consulta

A opção de manutenção só pode ser **alteração** ou **consulta**. Qualquer outra é recusada
com * Opcao nao disponivel. Use ALT ou CON *, o cursor volta ao campo da opção, e nada é
lido nem gravado.

[?] A mensagem nomeia as opções como **ALT** e **CON**, mas a tela confere o que foi
informado contra os códigos internos de alteração e de consulta. Nenhum fonte do acervo
mostra quem traduz o que o servidor digita no código conferido; sem essa tradução, a guarda
recusaria toda opção — inclusive as duas que a própria mensagem pede. Pergunta ao site.

### RN-04 — O percentual vai de zero a cem

O percentual informado pode ir de **zero a cem**. Acima de cem a recusa é
* Percentual maximo invalido * e o cursor volta para o campo do percentual. O campo deixado
em branco conta como zero. O zero é aceito: é ele que apaga o percentual registrado (RN-07).

### RN-05 — A consulta não grava nada

Com a consulta escolhida, as duas passagens do processamento terminam antes de qualquer
decisão de gravação: nenhum percentual é incluído, trocado ou apagado, nenhum pedido de
atualização é criado e nenhum registro de auditoria é escrito.

### RN-06 — A resposta S pede a atualização e não regrava o percentual

Quando a resposta a **Atualiza Cadastro <S/N>?** é **S**, o sistema cria um **pedido de
atualização do cadastro** — com o número seguinte ao último pedido já registrado, o tipo de
órgão da sessão, a coordenação regional escolar 1, a matrícula de quem opera, o terminal e a
data — e, na instalação que processa em lote, dispara o processamento. A tela avisa
**\*\* Cadastro sendo atualizado \*\*** e volta para si mesma.

**O percentual informado não é gravado nesse caminho**: quem grava o percentual é a resposta
N (RN-07), e a atualização usa o que já estava registrado para o tipo de órgão.

[?] Se o servidor digitar um percentual novo e responder **S**, a atualização roda com o
percentual que já estava registrado e o novo se perde. O acervo não mostra o servidor fazendo
as duas coisas em duas passagens, nem permite dizer se a intenção era essa. Pergunta ao site.

[?] A criação do pedido é precedida de uma conferência da passagem corrente contra o total de
passagens da tela; esta tela não fixa esse total (as telas que mostram lista fixam) e o
acervo não diz o valor que ela recebe do ambiente. Se os dois números não coincidirem,
responder **S** termina em silêncio, sem pedido e sem aviso. Pergunta ao site.

[?] O processamento em lote só é disparado quando a instalação roda sob o produto LINC; o que
acontece nas demais não está no acervo — pelo texto, o pedido fica criado e a atualização não
roda, e mesmo assim o servidor vê o aviso de que o cadastro está sendo atualizado. Pergunta
ao site.

### RN-07 — A resposta N registra, troca ou apaga o percentual da secretaria

Quando a resposta a **Atualiza Cadastro <S/N>?** não é **S**, o sistema cuida do percentual
do tipo de órgão, e o que ele faz depende do que já existia:

- não havia percentual e o informado não é zero: o percentual é **incluído**;
- havia um percentual diferente do informado e o informado não é zero: o percentual é
  **trocado** pelo informado;
- havia percentual registrado e o informado é zero: o registro é **apagado**;
- o informado é igual ao que já estava registrado: **nada é feito**;
- não havia percentual e o informado é zero: **nada é feito**.

Na inclusão ficam gravados, além do percentual, a matrícula de quem operou e a data do dia;
a troca grava só o percentual — a data e a matrícula continuam as do registro original.

[?] A troca do percentual não refaz a data do registro, embora ela seja a data da última
atualização; a exclusão leva o registro inteiro para a auditoria. Se a troca deveria passar a
data para a do dia, o site confirma. Pergunta ao site.

### RN-08 — Não se pede a atualização com um pedido em processamento

Antes de aceitar a resposta **S**, o sistema confere se já existe um pedido do mesmo relatório
de atualização para o tipo de órgão na coordenação 1. Havendo, a recusa é
* Relatorio em processamento. Aguarde. *, com o cursor no campo da resposta, e nada é pedido
nem gravado. A conferência vale só para a resposta **S**: com a resposta **N** o percentual é
mantido mesmo com um pedido em andamento.

[?] A conferência e o pedido usam sempre a coordenação regional escolar de código 1, e não a
coordenação da sessão, que a tela usa no resto do que faz. Se o pedido de uma coordenação
deveria ser conferido contra os pedidos daquela coordenação, o site confirma. Pergunta ao
site.

### RN-09 — Nada é conferido nem gravado sem a segurança da tela, do perfil e da rota

A abertura passa pela conferência de segurança da sessão: a tela tem de estar liberada para a
matrícula, a matrícula tem de ter acesso a ela, e a estação tem de ser a do cadastro do
servidor. Barrada aí, a tela avisa — * Tela nao disponivel * ou
* Acesso negado para esta matricula * — e a sessão sai sem processar nada. A passagem de
conferência leva o contexto da sessão à conferência da rota e à segurança da operação, que
para esta tela é a **alteração**; qualquer desfecho diferente de OK abandona o processamento
antes de qualquer leitura ou gravação. A liberação da alteração é conferida uma vez, na
passagem de conferência, e não se repete na passagem que grava.

### RN-10 — Toda mudança do percentual deixa rastro na auditoria

Cada inclusão, troca ou exclusão do percentual grava um registro de auditoria com o objeto
auditado (o próprio cadastro do percentual), a operação, os valores anterior e posterior e o
contexto da sessão: matrícula, coordenação regional escolar, terminal e data e hora. O pedido
de atualização **não** gera registro de auditoria: o próprio pedido é o documento da
solicitação.

[?] Na inclusão, o valor anterior que vai para a auditoria é o registro recém-criado e o
posterior fica em branco — o mesmo formato da exclusão, e o inverso do que faz a tela de
percentual por gênero do mesmo sistema. Ou o campo guarda o valor gravado, ou a auditoria da
inclusão conta a história trocada. Pergunta ao site.

### RN-11 — A recusa de destino inválido não é apresentada por esta tela

Entre as mensagens que a ficha da tela lista está a recusa de **destino inválido**, da
distribuição automática entre destinos. O caminho que a produz só roda quando o modo de
distribuição automática está preenchido, e a tela o limpa imediatamente antes de cada ponto
em que ele poderia disparar. Por esta tela, portanto, essa recusa não aparece.

[?] A ficha da tela lista a recusa e o programa não a alcança: divergência entre a ficha e o
comportamento, a confirmar com quem mantém o grafo. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Percentual da atualização do cadastro de atendimento

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C277T

  Cenário: Abertura da tela em consulta, com o percentual do tipo de órgão
    Dado que o tipo de órgão da minha secretaria já tem um percentual registrado
    Quando abro a tela sem informar opção de manutenção
    Então ela abre em consulta
    E vejo o percentual registrado, a descrição do tipo de órgão e a data do sistema
    E vejo a pergunta "Atualiza Cadastro <S/N>?"

  Cenário: Tipo de órgão sem percentual registrado
    Dado que o tipo de órgão da minha secretaria não tem percentual registrado
    Quando abro a tela
    Então o campo do percentual aparece zerado
    E nada é gravado

  Cenário: Opção de manutenção fora de alteração e consulta
    Quando informo uma opção de manutenção diferente de alteração e de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo da opção
    E nada é lido nem gravado

  Cenário: Percentual acima de cem
    Quando informo um percentual maior que cem
    Então vejo a mensagem "* Percentual maximo invalido *"
    E o cursor volta para o campo do percentual
    E nada é gravado

  Cenário: A consulta não grava nada
    Dado que a tela está em consulta
    Quando percorro a tela e confirmo
    Então nenhum percentual é incluído, trocado ou apagado
    E nenhum pedido de atualização é criado
    E nenhum registro de auditoria é escrito

  Cenário: Resposta N registra um percentual que ainda não existia
    Dado que o tipo de órgão da minha secretaria não tem percentual registrado
    Quando informo um percentual de um a cem e respondo N
    Então o percentual fica registrado para o tipo de órgão
    E a data do dia e a minha matrícula ficam no registro
    E a operação deixa rastro na auditoria

  Cenário: Resposta N troca o percentual registrado
    Dado que o tipo de órgão já tem um percentual registrado
    Quando informo outro percentual e respondo N
    Então o percentual do tipo de órgão passa a ser o informado
    E a operação deixa rastro na auditoria

  Cenário: Resposta N com percentual zero apaga o registro
    Dado que o tipo de órgão já tem um percentual registrado
    Quando informo zero e respondo N
    Então o percentual daquele tipo de órgão deixa de existir
    E a operação deixa rastro na auditoria

  Cenário: Resposta N com o mesmo percentual não muda nada
    Dado que o tipo de órgão já tem um percentual registrado
    Quando informo o mesmo percentual e respondo N
    Então nada é gravado
    E nenhum rastro de operação é gerado

  Cenário: Resposta N sem percentual e com zero não muda nada
    Dado que o tipo de órgão não tem percentual registrado
    Quando informo zero e respondo N
    Então nada é gravado
    E nenhum rastro de operação é gerado

  Cenário: Resposta S pede a atualização do cadastro
    Dado que não há atualização em processamento para o meu tipo de órgão
    Quando respondo S
    Então o sistema cria um pedido de atualização do cadastro para o meu tipo de órgão
    E o pedido recebe o número seguinte ao último já registrado
    E vejo a mensagem "** Cadastro sendo atualizado **"
    E, na instalação que processa em lote, a atualização é disparada

  Cenário: Resposta S não regrava o percentual informado
    Dado que o tipo de órgão já tem um percentual registrado
    Quando informo um percentual diferente e respondo S
    Então o pedido de atualização é criado
    E o percentual informado não é gravado
    E a atualização usa o percentual que já estava registrado

  Cenário: Pedido de atualização já em processamento
    Dado que já existe um pedido de atualização em processamento para o meu tipo de órgão
    Quando respondo S
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta para o campo da resposta
    E nada é pedido nem gravado

  Cenário: Tela não liberada ou matrícula sem acesso
    Dado que a tela não está liberada para a minha matrícula, ou ela não tem acesso a ela
    Quando abro a tela
    Então vejo a mensagem "* Tela nao disponivel *" ou "* Acesso negado para esta matricula *"
    E a sessão sai da tela sem processar nada

  Cenário: Operação de alteração não liberada no perfil
    Dado que o meu perfil não tem a alteração liberada para esta tela
    Quando tento manter o percentual
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é lido nem gravado

  Cenário: Rota não esperada para a tela
    Dado que cheguei à C277T por uma rota que a conferência não espera
    Quando confirmo a tela
    Então a operação é abandonada
    E nada é gravado nem pedido

  Cenário: Toda mudança do percentual deixa rastro na auditoria
    Dado que incluí, troquei ou apaguei o percentual do tipo de órgão
    Quando a gravação termina
    Então existe um registro de auditoria com o objeto, a operação e os valores anterior e posterior
    E com a matrícula, a coordenação regional escolar, o terminal e a data e a hora

  Cenário: A recusa de destino inválido não é apresentada
    Dado que estou na tela e o modo de distribuição automática está preenchido
    Quando a tela prepara uma gravação
    Então ela limpa o modo de distribuição automática
    E a recusa de destino inválido não é apresentada
```
