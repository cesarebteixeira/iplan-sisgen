# US — C855T — Geração do planejamento de um período a partir da estimativa fechada do grupo

## Estória

Como **servidor da Coordenação Regional Escolar (CRE)**, quero **informar o grupo, o período
cuja estimativa já está fechada e o período que vai receber o planejamento, e confirmar a
geração**, para que **o planejamento do período novo saia da estimativa já conferida, sem
redigitar cardápio, segmento e refeição um a um**.

A estimativa diz o que o grupo serve em cada dia da semana, por cardápio, segmento e refeição, e
é ela que precisa estar fechada antes de virar o planejamento de outro período. Passar esse
conteúdo de um período para o outro à mão é onde o trabalho se perde e o erro entra: o que esta
tela faz é conferir se o período de destino está livre, se o de origem existe e está fechado e se
as refeições dele constam do cadastro oficial, confirmar com quem opera e entregar a geração ao
processamento. Sem ela, o planejamento do período ou se redigita cadastro por cadastro, ou se
copia por fora do sistema, sem conferência e sem registro de quem pediu.

## Contexto

Jornada S000M → C000M → C800M → C840M → C855T (5 passos).

Ator: servidor de CRE — informa o grupo e os dois períodos e confirma a geração do planejamento
de um deles a partir da estimativa fechada do outro.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

Os três passos anteriores — o `C000M`, o `C800M` e o `C840M` — são menus: só encaminham e não
gravam nada, e nenhum deles deixa modo de operação ou dado para esta tela. O contexto de que a
`C855T` se serve — a matrícula, o código de acesso, o privilégio, o tipo de órgão, a coordenação
regional escolar, a estação e a data do sistema — é o que a entrada deixou na sessão; a tela não
recalcula nada disso: usa para conferir o acesso, montar o cabeçalho, identificar quem pede a
geração e compor a auditoria. Essas conferências de sessão e de perfil são as mesmas de todas as
telas e não estão repetidas aqui: estão no anexo, na seção das regras que se revelaram da entrada.

A tela monta os próprios campos a partir do formulário e é ela mesma que marca a operação como
atualização: não há no material comparação com o código da tela que a chamou, de modo que o
comportamento dela **não muda** conforme quem a abriu. Ela também não aponta para outra tela:
reabre a si mesma para pedir a confirmação e, depois de confirmada, para mostrar o aviso.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela só trabalha na atualização, e é ela que a repõe ao abrir

Ao ser apresentada, a tela confere o acesso pela sessão, limpa as respostas que ela mesma escreve
— a descrição do tipo de órgão, a data do sistema e a sua mensagem — e já vem com a operação
marcada como **atualização**. É esse o único valor que ela aceita: chegando a mensagem com outra
operação, o sistema recusa com **\* Opcao nao disponivel. Use ALT \***, devolve o cursor ao campo
da operação, volta a tela ao começo e **não lê cadastro nenhum nem registra nada**.

O operador não escolhe a operação, e a origem não a escolhe por ele: a tela repõe a atualização
sozinha, a cada abertura, venha ela do menu ou de qualquer outra tela. O código da tela de onde se
veio é apenas repassado ao encaminhamento da sessão, não a esta decisão.

[?] A recusa manda usar a tecla ALT, mas o texto da máscara não vem no material: o que o operador
vê e digita nesse campo não pôde ser conferido. Se a máscara não oferece campo de operação, esta
recusa só é alcançável numa mensagem seguinte.

### RN-02 — O grupo é obrigatório, e é um só para os dois períodos

O grupo da estimativa tem de vir preenchido; em branco ou zerado, o sistema recusa com
**\* Informe o grupo \***, devolve o cursor a esse campo e **não lê cadastro nenhum nem registra
nada**.

É esse mesmo grupo que vale para o planejamento: antes de procurar qualquer cadastro, a tela copia
o grupo informado para o do período de destino. O grupo, portanto, não se pergunta duas vezes — e o
que o operador tiver digitado no campo do grupo do destino é descartado.

### RN-03 — O período de destino tem de ter cardápio cadastrado na sua data-limite

O período que vai receber o planejamento é identificado pela **data-limite** informada para ele: a
tela procura o cardápio do órgão da sessão que termina naquela data e, não achando, recusa com
**\* Cardapios nao cadastrados para esta data \***, com o cursor no dia dessa data-limite, e não
segue: nada é registrado. O período de destino precisa existir no cadastro de cardápios antes de
receber o planejamento — é o cardápio que diz que aquele período existe.

[?] A procura é posicionada com o código do cardápio zerado, e a chave do cadastro termina
justamente nesse código; o acervo não define se a leitura, assim posicionada, alcança o primeiro
cardápio do período ou se exige um cardápio de código zero. No segundo caso, **toda** operação
desta tela seria recusada aqui e a geração ficaria inalcançável. Pergunta ao site.

### RN-04 — O período de destino não pode já ter planejamento para o grupo

Antes de seguir, a tela procura o planejamento do órgão, daquela data-limite e daquele grupo;
achando **qualquer** registro, recusa com **\* Planejamentos ja cadastrados \***, com o cursor no
dia da data-limite do destino, e nada é registrado.

É por isso que a geração de um período e grupo se pede **uma vez**: pedida, o período deixa de ser
aceito por esta tela enquanto o planejamento estiver lá.

### RN-05 — O período de origem tem de ter estimativa para o grupo

O período de origem é identificado pela **data-limite** informada no outro par de datas. Não
havendo estimativa do órgão da sessão e do grupo que termine naquela data, a tela recusa com
**\* Nao existe planejamento para a data informada \***, com o cursor no dia dessa data-limite, e
nada é registrado.

### RN-06 — A estimativa de origem tem de estar fechada

A tela percorre os registros da estimativa daquele período e daquele grupo e exige que **todos**
estejam marcados como **fechados**. Achando um que não esteja, recusa com
**\* Cadastro nao fechado para este periodo \***, com o cursor no dia da data-limite da origem, e
nada é registrado. O fechamento da estimativa é o que libera a geração: estimativa aberta não vira
planejamento.

[?] A marca de fechamento é um código de um caractere cujo significado pleno não está no acervo —
sabe-se que a letra **F** é o fechado; o que os demais valores dizem, não. Tudo o que não for o
fechado é recusado.

### RN-07 — Cada refeição da estimativa tem de constar do cadastro oficial de refeições

Para cada registro da estimativa do período, a tela procura a refeição dele no **cadastro oficial
de refeições** do órgão. Enquanto a acha, passa ao registro seguinte da estimativa; faltando uma,
recusa com **\<- Refeicao nao cad no cadastro oficial \***, mostra o código da refeição e devolve
o cursor ao dia da data-limite da origem, e nada é registrado. A geração só passa quando **todas**
as refeições da estimativa do período estão no cadastro oficial.

[?] O que faz a tela percorrer os registros da estimativa é o recurso de posicionamento do
dicionário de dados, cujo efeito exato não está no acervo nem no manual: não se pode afirmar pelo
material que a leitura avança um registro por chamada dentro da mesma mensagem. Se a travessia não
terminar como o programa espera, a pergunta de confirmação e o registro do pedido não são
alcançados por esse caminho. Pergunta ao site.

### RN-08 — Só a resposta afirmativa leva ao registro

Passadas as conferências, a tela pergunta **\* Confirma atualizacao dos planejamentos <S/N> ? \***,
devolve o cursor ao campo da resposta e guarda o que conferiu: o grupo da estimativa e as duas
datas-limite. Na mensagem seguinte, só a resposta **S** segue; qualquer outra resposta limpa a
pergunta, devolve a tela ao começo da conferência — que ela refaz e volta a perguntar — e nada é
registrado.

Se algum dos valores guardados tiver mudado, a resposta também é descartada e a conferência
recomeça, sem registrar nada.

[?] As datas de **início** dos dois períodos não entram nessa guarda e não são usadas em
conferência nenhuma: um início redigitado depois da pergunta não invalida a resposta e ainda é
substituído pelo início do cadastro antes de a tela compor o pedido. Se a máscara permite editar
essas datas depois da pergunta, ou a guarda deveria incluí-las, ou os campos deveriam ser só de
exibição. Pergunta ao site.

### RN-09 — Um pedido do mesmo relatório já em processamento bloqueia o pedido novo

Antes de registrar, a tela procura na **fila de pedidos de relatório** um pedido do mesmo relatório
de geração ainda não processado. Achando um, avisa **\* Relatorio em processamento. Aguarde. \***,
devolve a tela ao começo e não registra nada: a geração de um período espera a anterior terminar.

[?] A procura é posicionada só pelo código do relatório, com o estado e o número do pedido em
branco, e a chave da fila é (relatório, estado, número). Se essa leitura alcança qualquer pedido
daquele relatório, a recusa funciona como descrita; se exige a chave inteira, a recusa seria
praticamente inalcançável. O acervo não define o alcance da leitura. Pergunta ao site.

### RN-10 — Confirmado, o pedido é registrado e o processamento é disparado

Com a resposta **S** e nenhum pedido em processamento, a tela lê o e-mail da matrícula que está
pedindo, toma o número seguinte da fila de pedidos e registra o pedido com o relatório de geração,
esse número, o dia, o mês e o ano da sessão, a matrícula, a estação e o órgão. Em seguida entrega o
processamento com o bloco de parâmetro — o órgão, o grupo e os dois períodos, com as duas datas de
início e as duas datas-limite — e mostra **\* Cadastro sendo atualizado \***, voltando a se
apresentar.

O disparo **não leva impressora**: esta tela não tem campo de impressora, e o pedido é registrado
com esse dado em branco.

[?] O número do pedido é o da última requisição da fila mais um, contado sobre o que estiver na
área da leitura; com a fila vazia o primeiro número é 1, e se a área guardar valor de leitura
anterior o número pode repetir. E o pedido é registrado **sem impressora**, embora o cadastro de
pedidos declare esse campo obrigatório: se o processamento depende da impressora no pedido é
pergunta ao site.

### RN-11 — O início dos dois períodos vem do cadastro, não do que foi digitado

Nenhuma conferência usa as datas de **início** informadas: o período de destino é procurado só pela
data-limite, e o de origem também. O início que vale é o do cadastro — o do cardápio achado, para o
período de destino, e o da estimativa achada, para o de origem — e é esse que a tela repõe antes da
pergunta e que segue no pedido e na auditoria.

### RN-12 — A tela não gera o planejamento: quem o gera é o processamento

Esta transação não inclui, altera nem exclui planejamento, cardápio, estimativa ou refeição: ela
**lê** esses cadastros para conferir e grava **dois** registros — o pedido e a auditoria. Quem cria
o planejamento do período a partir da estimativa é o processamento disparado, que roda fora do
atendimento.

[?] O material não declara a ligação entre o trabalho disparado e o programa do processamento: ela
é por convenção de nome e de código de relatório. E esse programa está **fora desta jornada** — o
que se pode afirmar é o que está no trecho lido, não o efeito completo dele. Pergunta ao site.

### RN-13 — Toda geração deixa trilha de auditoria

O caminho confirmado monta um registro de auditoria com a identificação da tela, o tipo de órgão, a
coordenação regional escolar da sessão, a matrícula, a estação, a data e a hora da sessão, o número
do processo e o conteúdo dos dois períodos — o mesmo conteúdo que vai no pedido — e o grava antes
de registrar o pedido.

[?] A auditoria registra a operação como **inclusão**, embora a tela seja de atualização; o número
do processo é o **dia do início** do período de destino, e não o período; e o conteúdo dos dois
períodos vai no **conteúdo anterior**, com o posterior em branco. Qual desses campos diz o que a
quem lê a auditoria é pergunta ao site.

### RN-14 — Os catorze campos de código e de data passam por edição numérica

Os dois códigos de grupo e as doze componentes de data passam por edição numérica antes de qualquer
conferência: campo em branco vira zero e o que não for número é recusado no próprio campo, e a
transação não segue. A tela não confere calendário nem compara o início com a data-limite: uma data
impossível segue adiante e simplesmente não encontra cadastro.

[?] O que exatamente a rotina de edição recusa — e se ela valida mês e dia — não está no acervo: a
rotina é importada, não vem no lote. Dos catorze campos, sete têm posição de cursor definida para
quando a digitação é recusada; os outros sete, não.

### RN-15 — Depois do pedido o operador continua na mesma tela

Terminada a conferência ou registrado o pedido, a tela volta a se apresentar: ela não aponta para
outra tela. Sai-se dela pelo campo de próxima tela, que é entregue ao encaminhamento da sessão,
fora desta transação.

---

## Cenários BDD

```gherkin
Funcionalidade: Geração do planejamento de um período a partir da estimativa fechada do grupo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C855T

  Cenário: RN-01 — abertura da tela
    Quando a tela C855T é apresentada
    Então a operação já vem marcada como atualização
    E a descrição do tipo de órgão, a data do sistema e a mensagem da tela vêm em branco
    E nenhum cadastro é consultado

  Cenário: RN-01 — operação diferente de atualização é recusada
    Dado que a mensagem chega com a operação diferente de atualização
    Quando envio a transação
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo da operação
    E nenhum cadastro é lido
    E nada é registrado

  Cenário: RN-02 — grupo não informado
    Dado que estou na tela C855T em atualização
    Quando deixo o grupo em branco e envio a transação
    Então vejo "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nenhum cadastro é lido
    E nada é registrado

  Cenário: RN-02 — é o mesmo grupo nos dois períodos
    Dado que informei o grupo da estimativa
    E digitei um grupo diferente no campo do período de destino
    Quando envio a transação
    Então o grupo do período de destino passa a ser o da estimativa
    E é esse grupo que a tela procura no planejamento

  Cenário: RN-03 — sem cardápio no período de destino
    Dado que informei a data-limite do período de destino
    E não há cardápio do meu órgão terminando nessa data
    Quando envio a transação
    Então vejo "* Cardapios nao cadastrados para esta data *"
    E o cursor volta ao dia-limite do destino
    E nada é registrado

  Cenário: RN-04 — o período de destino já tem planejamento
    Dado que existe planejamento do meu órgão, do grupo informado e do período de destino
    Quando envio a transação
    Então vejo "* Planejamentos ja cadastrados *"
    E o cursor volta ao dia-limite do destino
    E nada é registrado

  Cenário: RN-05 — sem estimativa no período de origem
    Dado que informei os dois períodos e o grupo
    E não há estimativa do meu órgão e do grupo terminando na data-limite de origem
    Quando envio a transação
    Então vejo "* Nao existe planejamento para a data informada *"
    E o cursor volta ao dia-limite da origem
    E nada é registrado

  Cenário: RN-06 — estimativa de origem não fechada
    Dado que existe estimativa do meu órgão e do grupo no período de origem
    E um dos registros dessa estimativa não está marcado como fechado
    Quando envio a transação
    Então vejo "* Cadastro nao fechado para este periodo *"
    E o cursor volta ao dia-limite da origem
    E nada é registrado

  Cenário: RN-07 — refeição da estimativa fora do cadastro oficial
    Dado que existe estimativa do meu órgão e do grupo no período de origem
    E uma das refeições dela não consta do cadastro oficial de refeições do meu órgão
    Quando envio a transação
    Então vejo "<- Refeicao nao cad no cadastro oficial *" com o código da refeição
    E o cursor volta ao dia-limite da origem
    E nada é registrado

  Cenário: RN-08 — as conferências passam e a tela pergunta
    Dado que há cardápio no período de destino e o destino não tem planejamento
    E a estimativa do período de origem existe, está fechada e todas as refeições dela constam do cadastro oficial
    Quando envio a transação
    Então vejo a pergunta "* Confirma atualizacao dos planejamentos <S/N> ? *"
    E o cursor fica no campo da resposta
    E ainda nada é registrado

  Cenário: RN-08 — resposta diferente de S volta ao começo
    Dado que estou na pergunta de confirmação
    Quando respondo N
    Então a pergunta é limpa
    E a tela volta ao começo da conferência
    E nada é registrado

  Cenário: RN-08 — valor guardado mudou e a resposta é descartada
    Dado que estou na pergunta de confirmação
    Quando troco o grupo ou uma das duas datas-limite e respondo S
    Então a resposta é descartada
    E a tela volta ao começo da conferência
    E nada é registrado

  Cenário: RN-09 — relatório já em processamento
    Dado que passei por todas as conferências
    E já existe um pedido do relatório de geração esperando processamento
    Quando respondo S à pergunta de confirmação
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E nada é registrado

  Cenário: RN-10 — pedido registrado e processamento disparado
    Dado que passei por todas as conferências e respondi S
    Então o sistema registra o pedido com o número seguinte da fila, o relatório de geração, o dia, o mês e o ano da sessão, a minha matrícula, a estação e o meu órgão
    E entrega o processamento com o órgão, o grupo e os dois períodos
    E vejo "* Cadastro sendo atualizado *"

  Cenário: RN-10 — o disparo não leva impressora
    Dado que passei por todas as conferências e respondi S
    Então o pedido é registrado sem impressora
    E o processamento é disparado sem impressora

  Cenário: RN-11 — o início dos dois períodos vem do cadastro
    Dado que informei um início diferente do início do cardápio e do da estimativa achados
    Quando a tela confere os dados
    Então o início que vejo na pergunta é o do cardápio, para o período de destino, e o da estimativa, para o de origem
    E o início que digitei não entra em nenhuma conferência
    E é esse início do cadastro que segue no pedido e na auditoria

  Cenário: RN-12 — a tela não gera o planejamento
    Dado que passei por todas as conferências e respondi S
    Então nenhum planejamento, cardápio, estimativa ou refeição é incluído, alterado ou excluído nesta transação
    E os únicos registros gravados são o pedido e a auditoria
    E o planejamento do período é gerado pelo processamento disparado

  Cenário: RN-13 — o pedido deixa trilha de auditoria
    Dado que respondi S à pergunta de confirmação
    Então a auditoria registra a tela de origem, o tipo de órgão, a coordenação regional escolar, a minha matrícula, a estação, a data e a hora da sessão, o número do processo e os dois períodos
    E ela é gravada antes do pedido

  Cenário: RN-14 — digitação que não é número
    Dado que digito letras em um dos campos de grupo ou de data
    Quando envio a transação
    Então a transação não segue
    E o cursor volta ao campo recusado, quando há posição definida para ele
    E nada é registrado

  Cenário: RN-15 — depois do pedido continuo na C855T
    Dado que acabei de registrar um pedido, ou que a tela recusou o pedido
    Então continuo na C855T
    E nenhuma outra tela é aberta por esta transação
```
