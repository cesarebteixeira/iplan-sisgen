# US — C114T — Manter as refeições de cada grupo de atendimento

## Estória

Como **servidor de CRE**, quero **declarar quais refeições cada grupo de atendimento
recebe — e em qual dessas ligações o grupo tem sobremesa —**, para que **a oferta de
alimentação chegue ao nível em que o atendimento acontece, o grupo de atendimento, e não
fique declarada só para o segmento inteiro**.

A refeição nasce no cadastro do tipo de órgão, e o que cada segmento oferece é declarado à
parte. Esta tela desce mais um degrau: liga a refeição aos grupos de atendimento de um
segmento e marca, em cada ligação, se aquele grupo recebe sobremesa. É essa marca que diz
à distribuição o que servir a cada grupo; sem ela, a sobremesa sai para quem não tem
direito, ou deixa de sair para quem tem.

## Contexto

Jornada S000M → C000M → C028M → C029M → C114T.

Ator: servidor de CRE — declara, para o tipo de órgão da sua secretaria, quais refeições
cada grupo de atendimento recebe e onde há sobremesa.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A `C114T` é uma tela de transação, não um menu: ela mostra as ligações já declaradas, **14
por vez**, e mantém uma linha por vez. Do contexto da sessão ela usa o tipo de órgão do
vínculo do servidor e o que a entrada deixou; **não há campo para escolher o tipo de
órgão**. Ela encadeia: por um campo fora da grade entrega a sessão à tela `C118T`, que
trata as justificativas de cada refeição.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A ligação que esta tela mantém

O cadastro que esta tela mantém é a lista das refeições oferecidas a cada **grupo de
atendimento**, dentro do segmento daquele grupo. Cada registro tem **6 campos** — contei
entre o cabeçalho e o fechamento do cadastro no dicionário da base — e se identifica por
quatro códigos: o **tipo de órgão**, a **refeição**, o **segmento de atendimento** e o
**grupo de atendimento**. Essa combinação **não se repete**: a chave do cadastro não admite
duplicidade. Além dos códigos, cada ligação guarda a **indicação de sobremesa**, que o
dicionário marca como obrigatória, e um **indicador de atendimento em creche**.

O cadastro é dimensionado para **120.000 registros** — capacidade, o máximo esperado, e não
o volume cadastrado. Esta tela é a única que o escreve; a tela `C118T` só o lê.

[?] O indicador de atendimento em creche existe na ligação e esta tela **nunca** o informa:
nem na inclusão, nem na alteração. O que fica gravado nesse campo, e o que ele significa
nesta ligação, não está no acervo. Pergunta ao site.

### RN-02 — A grade tem 14 linhas, e cada linha traz os códigos, as descrições e a situação

A grade comporta **14 linhas**, e cada linha tem **5 campos** — a refeição (2 dígitos), a
indicação de sobremesa (uma letra), o segmento de atendimento (2 dígitos), o grupo de
atendimento (2 dígitos) e a situação (uma letra) —, o que dá **8 posições por linha**. Fora
da grade, o cabeçalho tem **9 itens**: a tela, a origem, o número da transação, a data de
entrada, o mês de referência, a opção de manutenção, a tela de destino, a grade e a
refeição informada fora da grade. Contei item a item o leiaute de entrada do programa: 9 no
cabeçalho e 5 em cada uma das 14 linhas.

Na exibição, cada linha mostra, além dos códigos, as descrições que vêm dos cadastros: a
descrição abreviada da refeição, a indicação legível da sobremesa — **"Sim"** ou
**"Nao"** —, a descrição do segmento e a descrição do grupo de atendimento. Fora da grade,
a tela mostra a descrição do tipo de órgão da sessão e a data do sistema.

[?] A tela nomeia só dois dos seus campos: a refeição da linha (**COD.REFEICAO**) e o
segmento (**COD.SEGMENTO**). O grupo de atendimento e o campo da refeição que fica fora da
grade entram na conferência numérica sem nome de negócio — o rótulo deles é o próprio nome
técnico do campo —, e o que o usuário lê nessas colunas, na indicação de sobremesa e na
situação não está na fonte. Pergunta ao site.

### RN-03 — O tipo de órgão do vínculo do servidor é o escopo de tudo

Tudo o que a tela lê e grava é do **tipo de órgão do vínculo** do servidor — o mesmo que a
entrada deixou na sessão: as ligações, as refeições, os grupos de atendimento, os segmentos
e a declaração de refeição por segmento. Não há campo para escolher outro tipo de órgão; a
identificação dele e a data do sistema abrem o cabeçalho.

### RN-04 — Abrindo, a tela mostra as ligações já declaradas, em consulta e sem gravar

Aberta sem opção guardada na sessão, a tela assume a **consulta** e percorre as ligações do
tipo de órgão na ordem da chave do cadastro — refeição, segmento e grupo de atendimento —,
mostrando 14 por vez. Quando o tipo de órgão não tem **nenhuma** ligação declarada, ela
avisa **\* Registros nao cadastrados \*** e encerra a listagem. Esgotada a lista, a tela
volta ao começo na exibição seguinte. A consulta não grava nada.

[?] A leitura das ligações parte da posição deixada pela última linha mostrada, e o que os
sinalizadores de posicionamento da leitura fazem não está explicado no acervo: ou a lista
continua no registro seguinte, ou repete o registro guardado — se repetir, uma ligação
aparece em duas linhas; se pular, uma ligação some da lista. Pergunta ao site.

### RN-05 — A tela só altera ou consulta

A opção de manutenção aceita apenas **alterar** e **consultar**: incluir e excluir se fazem
pelas linhas, com a alteração. Qualquer outra opção é recusada com
**\* Opcao nao disponivel. Use ALT ou COm \***, com o cursor de volta no campo da opção.
Passando a conferência, a opção fica guardada na sessão da tela: é nela que a tela reabre
na exibição seguinte.

[?] A mensagem manda usar **ALT** e **COm**, e a conferência compara o que foi informado
com os códigos internos de alteração e de consulta. Nenhum fonte do lote mostra quem
traduz o que o servidor digita no código conferido — a mesma forma aparece nas outras
telas de manutenção deste sistema. Se não houver tradução, a conferência recusa toda
opção, inclusive as duas que a própria mensagem pede, e nenhuma ligação é mantida por esta
tela. Pergunta ao site.

[?] A recusa da opção não é reconferida no caminho que grava: ele descarta apenas a
consulta, e o que separa uma recusa da gravação é a marca de falha que a rotina de mensagem
do ambiente deixa — rotina que não está no lote. Se ela não marcar, uma linha com a opção
recusada ainda assim é gravada. Pergunta ao site.

### RN-06 — A situação da linha decide o que fazer com ela

Em cada linha, a **situação** decide a operação: **I** inclui, **A** altera e **E** exclui.
Linha cuja situação não é I, A nem E não gera operação nenhuma — a tela passa adiante sem
avisar. Antes de manter, a tela confere se o perfil de quem opera autoriza a operação
daquela linha. Linha sem **refeição** informada é descartada antes das conferências.

[?] A conferência descarta a linha de refeição em branco, e a gravação descarta a linha de
**grupo de atendimento** em branco: as duas guardas olham campos diferentes. Uma linha com
a refeição em branco e o grupo preenchido, portanto, não passa por conferência nenhuma e
chega ao caminho que grava. Na tela irmã — a dos grupos de atendimento de cada refeição —
as duas guardas olham o mesmo campo. Ou a guarda está no campo errado, ou a gravação
deveria rejeitar essa linha. Pergunta ao site.

### RN-07 — Incluir exige a refeição e o grupo de atendimento cadastrados

Para incluir, a tela confere dois cadastros. A **refeição** informada tem de estar
cadastrada para o tipo de órgão; não estando, a recusa é **\* Refeicao nao cadastrada \***,
com o cursor de volta no campo da refeição. O **grupo de atendimento** informado tem de
estar no catálogo de grupos do tipo de órgão; não estando, a recusa é
**\* Grupo de atendimento nao cadastrado \***, com o cursor no campo do grupo. Nas duas
recusas nada é gravado.

### RN-08 — Na inclusão, é o grupo de atendimento que decide o segmento

Achado o grupo de atendimento, o **segmento da ligação é o do grupo**: o segmento que
estiver na coluna é substituído pelo segmento daquele grupo no catálogo, e é esse que a
tela grava. Em seguida a tela confere se a **refeição está declarada para esse segmento** —
a declaração que a tela das refeições de cada segmento mantém. Não estando, a recusa é
**\* Segmento nao cad. para esta refeicao \***, com o cursor no campo do grupo de
atendimento, e nada é gravado.

[?] Na inclusão o segmento digitado é descartado, mas na alteração e na exclusão é ele que
identifica a ligação a manter. E a recusa "segmento não cadastrado para esta refeição"
devolve o cursor ao campo do **grupo de atendimento**, e não ao do segmento. Se a coluna do
segmento é só informativa na inclusão, e por que a recusa aponta para outro campo, a fonte
não diz. Pergunta ao site.

### RN-09 — A sobremesa é S ou N, e o S só passa onde a refeição a prevê

A indicação de sobremesa tem de ser **S** ou **N**. Em branco ou com outra letra, a recusa
é **\* Informe se sobremesa com S ou N \***, com o cursor no campo da sobremesa. Marcado
**S**, a tela confere se aquela refeição prevê sobremesa no cadastro das refeições; não
prevendo, a recusa é **\* Refeicao nao cadastrada para sobremesa \***, e nada é gravado.
Marcado **N**, não há o que conferir. As duas conferências valem para incluir e para
alterar; a exclusão não olha a sobremesa.

### RN-10 — Incluir não repete a ligação que já existe

Antes de incluir, a tela procura a ligação com a refeição, o segmento e o grupo de
atendimento informados. Já existindo, a inclusão é recusada com
**\* Refeicao/Grupo atend. ja cadastrados \***, com o cursor no campo da situação, e nada é
gravado. A chave do cadastro não admite a combinação repetida.

### RN-11 — Alterar e excluir exigem a ligação existente

Para alterar ou excluir, a ligação com a refeição, o segmento e o grupo de atendimento
informados tem de existir; não existindo, a recusa é
**\* Refeicao/Grupo atend. nao cadastrados \***, com o cursor no campo da situação, e nada
é gravado. Nesse caminho — ao contrário da inclusão — a tela **não** reconfere o cadastro
da refeição, o catálogo de grupos nem o cadastro de segmentos: a alteração chega a ler o
cadastro das refeições, mas só aproveita dele a indicação de sobremesa.

### RN-12 — A alteração muda só a sobremesa; a exclusão apaga a ligação

A alteração **não** troca a refeição, o segmento nem o grupo de atendimento — eles
identificam a ligação e são a chave do cadastro: ela regrava apenas a **indicação de
sobremesa**. A exclusão apaga a ligação inteira. Nenhuma das duas toca o cadastro das
refeições, o catálogo de grupos de atendimento nem o cadastro de segmentos: esses são
apenas lidos.

### RN-13 — A refeição informada fora da grade entrega a sessão à tela C118T, em consulta

Preenchendo o campo de **refeição que fica fora da grade**, a tela não processa as linhas:
ela confere que existe pelo menos uma ligação daquela refeição no tipo de órgão — não
havendo, a recusa é **\* Refeicao nao cadastrada para este calculo \***, com o cursor
naquele campo —, adota aquela refeição com a descrição que vem do cadastro das refeições e
**entrega a sessão à tela `C118T`, em consulta**. Essa entrega tem precedência sobre a
manutenção das linhas: acontece tanto com a opção de consulta quanto com a de alteração.

A `C118T` abre assim mostrando aquela refeição, e é ela que trata as justificativas de cada
refeição. Quem ler esta estória isolada precisa saber que a passagem se faz **sem menu**:
esta tela passa o registro — a refeição — e o modo de consulta à seguinte, e é por isso que
a `C118T` já abre na refeição informada aqui.

### RN-14 — Cada operação grava o rastro na auditoria

Cada inclusão, alteração e exclusão grava também um registro no cadastro de auditoria
(`A010T`), com a operação (inclusão, alteração ou exclusão), o cadastro tocado, a tela
`C114T`, a matrícula de quem operou, a estação, o tipo de órgão, a data e a hora, o número
do processo — que recebe o **código da refeição** — e o conteúdo anterior e o posterior da
ligação. Na inclusão o anterior vai em branco e o posterior é a ligação gravada; na
alteração o anterior é a ligação lida e o posterior é a mesma ligação com a nova sobremesa;
na exclusão o anterior é a ligação apagada e o posterior vai em branco.

[?] A auditoria grava a **CRE zerada**: o programa zera esse campo antes de montar o
registro nas três operações. Se isso é intencional, e como se confere a auditoria sem a
CRE de quem operou, não está no acervo. Pergunta ao site.

### RN-15 — Nada é exibido nem gravado sem a segurança de sessão, de rota e de permissão

Na abertura, a tela confere se ela própria existe no cadastro de telas — não existindo, o
aviso é **\* Tela nao disponivel \*** — e se o código de acesso de quem opera tem a tela —
não tendo, a recusa é **\* Acesso negado para esta matricula \***. Na passagem que mantém,
ela confere a rota — tendo a tela sido retirada do cadastro de telas, o aviso é
**\* Tela nao cadastrada \*** — e, para a operação que a linha pede, a autorização daquela
operação no mesmo código de acesso — não tendo, a recusa é
**\* Acesso negado para esta operacao \***. A conferência recebe o contexto da sessão: a
matrícula, o código de acesso, o privilégio, a CRE e o tipo de órgão. Nas recusas nada é
gravado.

[?] A permissão da operação é conferida na passagem de validação e **não** se repete na
passagem que grava: se ela mudasse entre as duas, a gravação não a reconferiria. Pergunta
ao site.

[?] De onde vêm os dados da sessão que a conferência recebe não está em nenhum programa
desta jornada: nem o `LOGON` nem o `S000M` os preenchem — os dois não citam esses campos —,
e quem os preenche não veio no acervo. Pergunta ao site.

### RN-16 — A consulta não grava nada

Na consulta a tela só mostra: ela lista as ligações, não confere as linhas e desvia do
caminho que grava. Nenhuma ligação é incluída, alterada ou apagada, e nenhuma trilha de
auditoria é gerada.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter as refeições de cada grupo de atendimento

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C114T

  Cenário: RN-01, RN-02, RN-03 e RN-04 — abrir a tela mostra as ligações do meu tipo de órgão
    Dado que o tipo de órgão do meu vínculo tem ligações declaradas
    Quando abro a tela C114T
    Então ela abre em consulta
    E vejo até 14 linhas, cada uma com a refeição, a indicação de sobremesa, o segmento, o grupo de atendimento e a situação
    E cada linha traz a descrição abreviada da refeição, a indicação "Sim" ou "Nao" da sobremesa e as descrições do segmento e do grupo de atendimento
    E o cabeçalho identifica o tipo de órgão do meu vínculo e a data do sistema
    E não há campo para escolher outro tipo de órgão
    E nada é gravado

  Cenário: RN-04 — tipo de órgão sem nenhuma ligação declarada
    Dado que o tipo de órgão do meu vínculo não tem nenhuma ligação declarada
    Quando abro a tela C114T
    Então vejo a mensagem "* Registros nao cadastrados *"
    E nenhuma linha é preenchida

  Cenário: RN-05 — opção de manutenção não disponível
    Dado que estou na tela C114T
    Quando informo uma opção diferente de alterar e de consultar
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou COm *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: RN-05 — a tela reabre na opção da última vez
    Dado que usei a tela C114T com a opção de alteração
    Quando a tela é exibida de novo na mesma sessão
    Então ela reabre na opção de alteração

  Cenário: RN-06 — linha com situação desconhecida é ignorada
    Dado que estou na tela C114T com a opção de alteração
    E preenchi uma linha com uma situação diferente de I, A e E
    Quando confirmo a mensagem
    Então aquela linha não gera operação nenhuma
    E nenhuma mensagem é mostrada
    E nada é gravado

  Cenário: RN-07 — incluir com uma refeição que não está cadastrada
    Dado que estou na tela C114T com a opção de alteração
    E informo, numa linha, uma refeição que não está cadastrada no meu tipo de órgão
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Refeicao nao cadastrada *"
    E o cursor volta ao campo da refeição
    E nada é gravado

  Cenário: RN-07 — incluir com um grupo de atendimento que não está no catálogo
    Dado que estou na tela C114T com a opção de alteração
    E informo, numa linha, uma refeição cadastrada e um grupo de atendimento que não está no catálogo
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Grupo de atendimento nao cadastrado *"
    E o cursor volta ao campo do grupo de atendimento
    E nada é gravado

  Cenário: RN-08 — incluir uma refeição que o segmento do grupo não tem declarada
    Dado que estou na tela C114T com a opção de alteração
    E informo, numa linha, uma refeição cadastrada e um grupo de atendimento do catálogo
    E aquela refeição não está declarada para o segmento daquele grupo
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Segmento nao cad. para esta refeicao *"
    E o cursor volta ao campo do grupo de atendimento
    E nada é gravado

  Cenário: RN-08 e RN-12 — incluir uma ligação nova
    Dado que estou na tela C114T com a opção de alteração
    E informo, numa linha, uma refeição cadastrada e um grupo de atendimento do catálogo
    E a refeição está declarada para o segmento daquele grupo
    E não existe ligação daquela refeição com aquele grupo
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então a ligação passa a constar do cadastro, com o segmento do grupo de atendimento
    E o segmento gravado é o do grupo, e não o que eu digitei na coluna
    E a auditoria registra a inclusão

  Cenário: RN-09 — sobremesa em branco ou fora de S e N
    Dado que estou na tela C114T com a opção de alteração
    E informo, numa linha, uma refeição cadastrada
    E deixo a indicação de sobremesa em branco, ou com outra letra
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Informe se sobremesa com S ou N *"
    E o cursor volta ao campo da sobremesa
    E nada é gravado

  Cenário: RN-09 — sobremesa S numa refeição que não a prevê
    Dado que estou na tela C114T com a opção de alteração
    E a refeição informada não prevê sobremesa no cadastro das refeições
    E marco a sobremesa S na linha
    Quando confirmo a mensagem
    Então vejo a mensagem "* Refeicao nao cadastrada para sobremesa *"
    E nada é gravado

  Cenário: RN-10 — incluir uma ligação que já existe
    Dado que estou na tela C114T com a opção de alteração
    E já existe ligação da refeição com o segmento e o grupo de atendimento informados
    E assinalo nessa linha a situação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Refeicao/Grupo atend. ja cadastrados *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: RN-11 — alterar ou excluir uma ligação que não existe
    Dado que estou na tela C114T com a opção de alteração
    E informo, numa linha, uma refeição, um segmento e um grupo de atendimento sem ligação declarada
    E assinalo nessa linha a situação A, ou a situação E
    Quando confirmo a mensagem
    Então vejo a mensagem "* Refeicao/Grupo atend. nao cadastrados *"
    E o cursor volta ao campo da situação
    E nada é gravado

  Cenário: RN-12 — alterar a sobremesa de uma ligação
    Dado que existe a ligação da refeição com o segmento e o grupo de atendimento informados
    E estou na tela C114T com a opção de alteração
    E mudo a indicação de sobremesa na linha
    E assinalo nessa linha a situação A
    Quando confirmo a mensagem
    Então a ligação fica com a nova indicação de sobremesa
    E a refeição, o segmento e o grupo de atendimento continuam os mesmos
    E a auditoria registra a alteração com o valor anterior e o novo

  Cenário: RN-12 — excluir uma ligação
    Dado que existe a ligação da refeição com o segmento e o grupo de atendimento informados
    E estou na tela C114T com a opção de alteração
    E assinalo nessa linha a situação E
    Quando confirmo a mensagem
    Então a ligação sai do cadastro
    E a auditoria registra a exclusão com o valor anterior

  Cenário: RN-13 — a refeição informada fora da grade entrega a tela C118T, em consulta
    Dado que existe pelo menos uma ligação da refeição informada no meu tipo de órgão
    Quando informo essa refeição no campo que fica fora da grade
    Então a tela entrega a sessão à C118T, sem passar por menu
    E a C118T abre mostrando aquela refeição, em consulta
    E nenhuma linha é conferida nem gravada nessa passagem

  Cenário: RN-13 — refeição informada fora da grade sem nenhuma ligação declarada
    Dado que a refeição informada no campo que fica fora da grade não tem nenhuma ligação no meu tipo de órgão
    Quando confirmo a mensagem
    Então vejo a mensagem "* Refeicao nao cadastrada para este calculo *"
    E o cursor volta àquele campo
    E nada é gravado

  Cenário: RN-14 — toda gravação deixa rastro na auditoria
    Dado que incluí, alterei ou excluí uma ligação
    Então a auditoria registra a operação, o cadastro tocado, a tela C114T
    E registra a minha matrícula, a estação, o tipo de órgão, a data e a hora
    E registra o número do processo com o código da refeição
    E registra o conteúdo anterior e o posterior da ligação

  Cenário: RN-15 — sem permissão para a operação
    Dado que o meu código de acesso tem a tela C114T sem aquela operação liberada
    E informo a opção de alteração com uma linha preenchida
    Quando confirmo a mensagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-15 — sem acesso à tela
    Dado que o meu código de acesso não tem a tela C114T
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: RN-15 — tela fora do cadastro de telas
    Dado que a tela C114T não consta do cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: RN-15 — tela retirada do cadastro de telas
    Dado que a tela C114T foi retirada do cadastro de telas
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é gravado

  Cenário: RN-16 — a consulta não grava nada
    Dado que abri a tela e estou na opção de consulta
    Quando confirmo a mensagem
    Então o cadastro é apenas lido
    E nenhuma ligação é incluída, alterada ou apagada
    E nenhuma trilha de auditoria é gerada
```
