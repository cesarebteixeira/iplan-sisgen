# US — C690T — Manter o contrato do FINCON dos fornecedores com permissão na coordenação regional escolar

## Estória

Como **servidor da CRE**, quero **registrar, corrigir e desfazer o contrato do
FINCON de cada fornecedor com permissão na minha coordenação regional escolar**,
para que **o gasto desses fornecedores seja lançado contra um contrato que o
sistema reconhece**.

A permissão diz que um fornecedor pode atender àquela coordenação regional
escolar, naquele tipo de contrato e naquele período; o contrato no FINCON é o que
autoriza o gasto. Enquanto ele não estiver registrado, o processo trava: as telas
que conferem o contrato do fornecedor recusam o lançamento e mandam regularizar
aqui. É esta tela que fecha a ligação entre a permissão e o contrato, corrige essa
ligação quando o contrato muda e a desfaz quando o contrato não vale mais.

## Contexto

Jornada S000M → C000M → C050M → C690M → C690T.

Ator: servidor de CRE — registra, corrige e desfaz, para a sua coordenação
regional escolar, o contrato do FINCON dos fornecedores que têm permissão nela.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e
menus.md`: é **dado de navegação**, não regra de negócio. O `C000M`, o `C050M` e
o `C690M` são menus: não leem cadastro de negócio nenhum e não gravam nada.

A `C690T` é uma tela de transação. Ela trata **uma coordenação regional escolar
por vez**, com um tipo de contrato e dois períodos, e mostra **12 linhas**, uma
por fornecedor com permissão. A jornada termina nela: a tela não encaminha para
nenhuma outra.

O que ela usa do que veio antes é o **tipo de órgão** e a **coordenação regional
escolar** que a sessão carrega e a **identificação de quem opera** — matrícula,
estação, data e hora — para o rastro da auditoria. Essas são regras da entrada e
estão no anexo de evidências, em **Regras que se revelaram da entrada**.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — O que a tela trata e o que ela mostra

A tela trata **uma coordenação regional escolar por vez**. Fora da grade, ela
identifica o registro pela **coordenação** (2 dígitos), pelo **tipo de contrato**
(3 dígitos) e por dois períodos — o **período de início** e o **período limite**,
cada um com dia, mês e ano.

A área de linhas é uma grade de **12 linhas**, e cada linha tem **7 colunas**: o
**código do fornecedor** (4 dígitos), o **nome do fornecedor** (preenchido pelo
sistema), o **número** (6 dígitos) e o **ano** (4 dígitos) do contrato já
registrado, o **número** (6 dígitos) e o **ano** (4 dígitos) do contrato no
FINCON que o servidor informa, e a **ação** da linha (1 caractere).

Das duas datas, só o **período limite** escolhe registros: é por ele que a tela
procura a permissão e o contrato. O **período de início** é informado e
conferido, e vai para a linha e para o registro que nasce da permissão, mas não
escolhe nada.

[?] O texto da máscara não veio no lote: o que está escrito ao lado de cada campo
é pergunta ao site. Nesta estória os campos são nomeados pelos rótulos de negócio
que o próprio programa carrega ao conferir cada um.

[?] A linha carrega **dois** pares para a mesma coisa — o número e o ano do
contrato registrado e o número e o ano do contrato no FINCON — e a tela usa cada
par num momento diferente. Se a máscara deixa o servidor digitar os dois, ou se
um dos pares é só de exibição, é pergunta ao site.

### RN-02 — A coordenação regional escolar tem de ser a de quem opera

Se a sessão carrega uma coordenação regional escolar, a informada tem de ser
exatamente essa. Sendo outra, a recusa é **\* Usuario sem acesso a este grupo \***,
com o cursor de volta ao campo da coordenação, e nada é conferido nem gravado. Se
a sessão **não** carrega coordenação, essa conferência não roda e a tela aceita
qualquer uma.

É a coordenação da sessão que a tela carrega no campo da coordenação ao abrir.

### RN-03 — A tela abre em consulta, e só aceita consulta ou alteração

Ao abrir, a tela assume a **consulta**, e é esse valor que aparece na opção de
manutenção. A opção informada só pode ser **consulta** ou **alteração**; qualquer
outra é recusada com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor
no campo da opção, e a confirmação para ali: nada é conferido e nada é gravado.

[?] A mensagem nomeia as opções pelas abreviaturas **ALT** e **CON**, e o que a
conferência compara é o que o sistema carrega como alteração e como consulta.
Nenhum fonte lido mostra quem traduz o que o servidor digita na sigla comparada —
a mesma forma aparece nas outras telas de manutenção do sistema. Se não houver
tradução, a tela recusa toda opção, inclusive as duas que a própria mensagem
pede. Pergunta ao site.

### RN-04 — A coordenação informada tem de estar cadastrada

Na consulta de uma coordenação que a sessão ainda não consultou, o sistema
procura a coordenação no cadastro das coordenações regionais escolares, pelo
tipo de órgão de quem opera. Não achando, a recusa é **\* Grupo nao cadastrado \***,
com o cursor no campo da coordenação, e nada é mostrado nem gravado.

### RN-05 — O tipo de contrato informado tem de estar cadastrado

O tipo de contrato é procurado no cadastro dos tipos de contrato, pelo tipo de
órgão de quem opera. Não achando, a recusa é **\* Contrato nao cadastrado \***,
com o cursor no campo do tipo de contrato, e nada é mostrado nem gravado.

### RN-06 — O período limite é obrigatório

O período limite tem de vir preenchido na consulta; sem o ano limite, a recusa é
**\* Data limite invalida \***, com o cursor no campo do ano limite, e nada é
mostrado nem gravado. Essa conferência é da consulta: a alteração não a repete,
porque só alcança coordenação, tipo de contrato e período que já foram
consultados antes (RN-10).

### RN-07 — A coordenação tem de ter permissão lançada para o tipo de contrato e o período

O sistema procura a permissão daquela coordenação para o tipo de contrato e o
período limite informados. Não achando, a recusa é
**\* Permissao nao cadastrada \***, com o cursor no campo da coordenação, e nada
é mostrado nem gravado. Permissão marcada como excluída não conta: fica fora
dessa procura. A capacidade do cadastro das permissões é de **1.000.000** de
registros.

[?] A tela entra na procura com quatro classificações da permissão zeradas e,
depois de achar o primeiro registro, não reconfere essas quatro contra o que
pediu. Se a procura com classificação zerada puder devolver a permissão de outra
classificação, a conferência aceita uma permissão que não é a pedida. O que faz a
leitura casar com a classificação zerada é do dialeto e não está explicado no
material lido. Pergunta ao site.

### RN-08 — Os campos são numéricos

Os campos de código, data e contrato são numéricos: valor que não é número é
recusado, com o cursor de volta no campo e a confirmação sem efeito.

[?] O texto que o servidor vê nessa recusa sai de uma rotina comum do sistema,
que não está no material lido — o que os fontes desta tela mostram é a
conferência e o retorno do cursor ao campo. Pergunta ao site.

### RN-09 — Consultar cria os contratos que faltam para as permissões

Ao consultar uma coordenação que a sessão ainda não consultou — ou cuja
coordenação, tipo de contrato ou período limite mudou desde a última consulta —,
o sistema percorre as permissões daquela coordenação, tipo de contrato e período
e, para cada fornecedor com permissão que ainda **não** tenha registro de
contrato, **cria** o registro, copiando para ele a coordenação, o fornecedor, o
tipo de contrato, o período de início e o período limite da permissão, e deixando
zerados o número e o ano do contrato no FINCON, os valores do contrato e a data
de atualização.

É gravação de verdade: o registro nasce nessa consulta. E essa criação **não**
deixa rastro na auditoria — quem deixa rastro são as gravações da alteração
(RN-21).

[?] O que faz a leitura avançar de uma permissão para a seguinte é do dialeto e
não está explicado no material lido. Se a leitura repetisse o mesmo registro, a
consulta não voltaria. Pergunta ao site.

[?] Quem preenche os valores do contrato — o valor contratado, os aditivos, o
valor liquidado e o pré-liquidado — é pergunta ao site: esta tela cria e mantém
esses valores zerados, e nenhum programa lido move valor para eles.

### RN-10 — Alterar exige ter consultado antes a mesma coordenação, o mesmo tipo de contrato e o mesmo período

Ao alterar, a coordenação, o tipo de contrato e o período limite informados têm
de ser os mesmos da última consulta da sessão. Sendo outros, a recusa é
**\* Consulte antes de atualizar \***, com o cursor no campo da opção, e nada é
conferido nem gravado. É por isso que as conferências de coordenação, de tipo de
contrato, de período e de permissão (RN-04 a RN-07) não se repetem na alteração:
ela confia na consulta que a antecedeu.

### RN-11 — O nome do fornecedor vem do cadastro de fornecedores

A tela não aceita o nome do fornecedor digitado. Lido o contrato de cada linha,
ela procura o fornecedor pelo código no cadastro dos fornecedores e copia a razão
social para a linha. A coluna da linha mostra **34** caracteres e o cadastro
guarda **40**: o que passa dos 34 não aparece na tela. A capacidade do cadastro
dos fornecedores é de **10.000** fornecedores.

### RN-12 — A ação é por linha: informar, alterar, excluir e consultar

A ação é da linha, não da tela. A tela conhece cinco códigos: **I** informa o
contrato no FINCON, **A** altera, **E** exclui e **C** e **X** consultam a linha.
Linha sem o código do fornecedor não passa por ação nenhuma: com ação de
informar, alterar ou excluir ela é ignorada em silêncio. Ação fora desses cinco
códigos também é ignorada, sem mensagem.

### RN-13 — Informar exige que o fornecedor tenha permissão na coordenação, no tipo de contrato e no período

Ao informar, o sistema procura a permissão daquele fornecedor para a coordenação,
o tipo de contrato e o período limite da tela. Não achando, a recusa é
**\* Fornecedor nao cadastrado para esta permissao \***, com o cursor no código do
fornecedor da linha, e nenhuma linha da tela é gravada (RN-17).

### RN-14 — Informar e alterar exigem o número e o ano do contrato no FINCON, e o ano não pode passar do ano corrente

Nas duas ações, o número e o ano do contrato no FINCON são obrigatórios: faltando
qualquer um dos dois, a recusa é **\* Informe contrato/ano FINCON \***, com o
cursor no campo do número. Informado um ano maior que o ano corrente, a recusa é
**\* Ano do contrato maior que ano atual \***, com o cursor no campo do ano. Em
qualquer dos casos, nenhuma linha da tela é gravada (RN-17).

### RN-15 — Excluir exige que o contrato esteja registrado na coordenação

Ao excluir, o sistema procura o contrato naquela coordenação pelo número e pelo
ano registrados na linha. Não achando, a recusa é **\* Registro nao cadastrado \***,
com o cursor no campo do número do contrato, e nada é apagado.

[?] A conferência da exclusão procura o contrato só pela coordenação, pelo número
e pelo ano — sem o tipo de contrato, sem o período limite e sem o fornecedor —,
enquanto a exclusão propriamente dita procura pelo tipo de contrato, pelo período
limite e pelo fornecedor da linha. Se o contrato existir na coordenação com outro
período ou outro fornecedor, a tela aceita a linha e não apaga nada, sem avisar.
Ou a conferência deveria usar a mesma chave da exclusão, ou a exclusão deveria
usar a da conferência. Pergunta ao site; não concluo qual dos dois.

### RN-16 — Consultar a linha exige a linha preenchida e um contrato já registrado

A ação de consultar a linha — o código **C** ou o **X** — exige o código do
fornecedor na linha: em branco, a recusa é **\* Consulte linha preenchida \***,
com o cursor no campo da ação. Com o fornecedor informado, o sistema procura o
registro daquela coordenação, tipo de contrato e período e, se o registro ainda
não tiver contrato no FINCON, a recusa é
**\* Fornecedor sem contrato FINCON cadastrado \***. Achando um contrato
registrado, a tela carrega os dados do registro, passa a transação para
**consulta** e nenhuma gravação daquela confirmação é feita — mesmo que outras
linhas tragam ação de informar, alterar ou excluir.

[?] Os dois códigos de consultar a linha existem, fazem a mesma coisa e só
diferem num ajuste interno que a tela faz depois. Por que dois códigos para a
mesma ação é pergunta ao site.

[?] A procura do registro na ação de consultar a linha não usa o fornecedor
informado: ela começa pelo primeiro registro daquela coordenação, tipo de
contrato e período. O que a tela pretende carregar quando o servidor consulta uma
linha específica é pergunta ao site.

### RN-17 — Só a alteração grava, e uma linha recusada interrompe a confirmação

Informar, alterar e excluir só chegam ao banco com a opção **alteração**. Com a
opção consulta, a confirmação termina sem gravar nada. E uma linha recusada
interrompe a confirmação: as linhas seguintes da grade não são conferidas nem
gravadas.

[?] As linhas são gravadas na ordem da grade, antes de a linha seguinte ser
conferida. O programa não desfaz o que já gravou; se a confirmação inteira é
desfeita quando uma linha é recusada, isso é do controle de transação, que não
está no material lido. Pergunta ao site.

### RN-18 — Informar grava o contrato no registro do fornecedor

Informando o contrato, o sistema percorre os registros daquele fornecedor na
coordenação, no tipo de contrato e no período:

- achando um registro **sem** contrato no FINCON, grava nele o número e o ano
  informados na linha, e a auditoria sai com a operação de alteração;
- achando um registro que **já tem** contrato no FINCON, a linha é ignorada, sem
  mensagem e sem auditoria;
- **não** achando registro nenhum do fornecedor, a tela cria um a partir da
  permissão: o registro nasce com o número e o ano informados, com a data de
  atualização do dia, com o período de início vindo da permissão e com os valores
  do contrato zerados; a auditoria sai com a operação de inclusão.

### RN-19 — Alterar troca o contrato do registro identificado na linha

A alteração não age só pelo fornecedor: ela percorre os registros daquele
fornecedor na coordenação, no tipo de contrato e no período e só age no registro
que tiver exatamente o número e o ano do contrato registrados na linha. Nesse,
grava o número e o ano do contrato no FINCON informados, e a auditoria sai com a
operação de alteração. Se nenhum registro casar com o que a linha identifica, a
linha termina sem alteração e **sem mensagem** — o servidor não é avisado de que
nada aconteceu. A data de atualização do registro não é renovada nessa troca.

[?] A alteração exige que a linha identifique um registro pelo número e pelo ano
do contrato registrado e, quando nada casa, termina em silêncio. Ou o silêncio é
proposital, ou a tela deveria avisar que não alterou nada — e a máscara poderia
tornar obrigatória a identificação do registro. Pergunta ao site.

### RN-20 — Excluir apaga o registro do contrato

Casando o registro pelo número e pelo ano do contrato registrados na linha — e
pelo fornecedor, pelo tipo de contrato e pelo período —, o sistema **apaga** o
registro. A exclusão é definitiva, não é marca de excluído, e a auditoria sai com
a operação de exclusão, sem valores depois da operação.

### RN-21 — Toda gravação da alteração deixa rastro na auditoria

Cada inclusão, alteração e exclusão de registro de contrato feita pela alteração
monta um registro na trilha de auditoria (o cadastro `A010T`), com o tipo de
órgão, o cadastro de origem (o contrato), a operação, a matrícula de quem opera,
a estação, a sessão, a data e a hora, e os valores antes e depois.

A criação de registros que a consulta faz (RN-09) **não** monta esse rastro. A
trilha de auditoria comporta **60.000.000** de registros.

### RN-22 — A tela declara muito mais gravação do que executa

O programa declara, para cada um dos **8** cadastros que enxerga, as rotinas de
gravação e de exclusão — **16** operações ao todo. Dessas, a tela executa **3**:
gravar o registro do contrato, apagar o registro do contrato e gravar a
auditoria. As outras **13** não são alcançadas em caminho nenhum.

Dos 8 cadastros, **6** são só de leitura: o cadastro das telas, o tipo de órgão,
o fornecedor, a permissão, a coordenação regional escolar e o tipo de contrato.
Declarar não é executar: a lista de cadastros que o programa enxerga não diz o
que a tela grava.

### RN-23 — Indicada a próxima tela, a tela encaminha sem conferir nada

A tela recebe, junto com a transação, o código da **próxima tela**. Vindo
preenchido, a tela não roda nenhuma das conferências desta seção — acesso à
coordenação, opção disponível, consulta prévia e conferências de linha — e
encaminha a transação para a tela indicada.

[?] O material lido mostra que a tela deixa de conferir quando a próxima tela vem
informada, e que o encaminhamento é feito por uma rotina comum de roteamento das
telas. O que essa rotina confere antes de encaminhar é pergunta ao site.

### RN-24 — Falha de banco interrompe a transação e avisa

Toda leitura e toda gravação testam o erro do banco. O erro de leitura e o de
gravação entram na comunicação da sessão como erro do sistema — a confirmação
para ali, sem completar o resto e sem considerar nada gravado.

## Cenários BDD

```gherkin
Funcionalidade: Manter o contrato do FINCON dos fornecedores com permissão na coordenação regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C690T

  Cenário: RN-03 — opção de manutenção não disponível
    Dado que estou na tela C690T
    Quando informo uma opção de manutenção diferente de ALT e CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E nada é conferido nem gravado

  Cenário: RN-02 — coordenação fora da minha
    Dado que a minha sessão carrega uma coordenação regional escolar
    Quando informo outra coordenação
    Então vejo "* Usuario sem acesso a este grupo *"
    E nada é conferido nem gravado

  Cenário: RN-04 — coordenação não cadastrada
    Quando consulto uma coordenação regional escolar que não está cadastrada
    Então vejo "* Grupo nao cadastrado *"
    E nada é mostrado nem gravado

  Cenário: RN-05 — tipo de contrato não cadastrado
    Quando consulto uma coordenação com um tipo de contrato que não está cadastrado
    Então vejo "* Contrato nao cadastrado *"
    E nada é mostrado nem gravado

  Cenário: RN-06 — período limite em branco
    Quando consulto uma coordenação sem informar o ano limite
    Então vejo "* Data limite invalida *"
    E nada é mostrado nem gravado

  Cenário: RN-07 — coordenação sem permissão para o tipo de contrato e o período
    Quando consulto uma coordenação que não tem permissão lançada para aquele tipo de contrato e período
    Então vejo "* Permissao nao cadastrada *"
    E nada é mostrado nem gravado

  Cenário: RN-08 — campo numérico preenchido com o que não é número
    Dado que consultei a coordenação
    Quando informo letras num campo de código ou de data
    Então a confirmação é recusada e o cursor volta para o campo
    E nada é mostrado nem gravado

  Cenário: RN-01, RN-09 e RN-11 — consultar a coordenação pela primeira vez
    Dado que a coordenação está cadastrada, o tipo de contrato está cadastrado e há permissão para o período
    E os fornecedores com permissão ainda não têm contrato registrado
    Quando confirmo a consulta
    Então vejo as 12 linhas, cada uma com o código e o nome do fornecedor
    E os registros de contrato que faltavam são criados a partir das permissões, com o contrato do FINCON em branco
    E essa criação não deixa registro na auditoria

  Cenário: RN-09 — consultar de novo a mesma coordenação
    Dado que os fornecedores da coordenação já têm os seus registros de contrato
    Quando confirmo de novo a consulta da mesma coordenação, tipo de contrato e período
    Então nenhum registro novo é criado
    E nada é gravado

  Cenário: RN-10 — alterar sem consultar antes
    Dado que estou na tela C690T com a opção ALT
    E informo uma coordenação, um tipo de contrato e um período diferentes dos que consultei
    Quando confirmo
    Então vejo "* Consulte antes de atualizar *"
    E nada é conferido nem gravado

  Cenário: RN-17 — a consulta não grava o que as linhas pedem
    Dado que consultei a coordenação
    E preencho uma linha com a ação I e o contrato do FINCON
    Quando confirmo com a opção CON
    Então a lista é mostrada
    E nada é gravado

  Cenário: RN-12 — linha em branco ou ação desconhecida
    Dado que estou na tela C690T com a opção ALT
    Quando preencho uma linha sem o código do fornecedor e com a ação I, A ou E
    Ou preencho uma linha com uma ação diferente de I, A, E, C e X
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada

  Cenário: RN-13 — informar para um fornecedor sem permissão
    Dado que consultei a coordenação
    E preencho uma linha com a ação I, o código de um fornecedor sem permissão e o contrato do FINCON
    Quando confirmo com a opção ALT
    Então vejo "* Fornecedor nao cadastrado para esta permissao *"
    E nenhuma linha é gravada

  Cenário: RN-14 — informar sem o número ou sem o ano do contrato
    Dado que consultei a coordenação e o fornecedor tem permissão
    Quando preencho a linha com a ação I e deixo o número ou o ano do contrato em branco
    Então vejo "* Informe contrato/ano FINCON *"
    E nenhuma linha é gravada

  Cenário: RN-14 — ano do contrato maior que o ano corrente
    Dado que consultei a coordenação e o fornecedor tem permissão
    Quando preencho a linha com a ação I ou A e um ano do contrato maior que o ano corrente
    Então vejo "* Ano do contrato maior que ano atual *"
    E nenhuma linha é gravada

  Cenário: RN-18 — informar o contrato de um registro que ainda não tem contrato
    Dado que consultei a coordenação e o fornecedor tem permissão e o seu registro está sem contrato
    Quando preencho a linha com a ação I, o número e o ano do contrato, e confirmo com a opção ALT
    Então o número e o ano do contrato ficam gravados no registro do fornecedor
    E a operação fica registrada na auditoria como alteração

  Cenário: RN-18 — informar o contrato de um fornecedor sem registro nenhum
    Dado que consultei a coordenação e o fornecedor tem permissão, mas não tem registro de contrato
    Quando preencho a linha com a ação I, o número e o ano do contrato, e confirmo com a opção ALT
    Então o registro é criado a partir da permissão, com o contrato informado e os valores zerados
    E a operação fica registrada na auditoria como inclusão

  Cenário: RN-18 — informar uma linha cujo registro já tem contrato
    Dado que consultei a coordenação e o registro do fornecedor já tem contrato
    Quando preencho a linha com a ação I, outro número e outro ano de contrato, e confirmo com a opção ALT
    Então nada é gravado
    E nenhuma mensagem é mostrada

  Cenário: RN-19 — alterar o contrato de um registro
    Dado que consultei a coordenação e o fornecedor tem contrato registrado
    E informo na linha o número e o ano desse contrato
    Quando preencho a linha com a ação A e um novo número e ano de contrato, e confirmo com a opção ALT
    Então o número e o ano do contrato do registro passam a ser os informados
    E a operação fica registrada na auditoria como alteração

  Cenário: RN-19 — alterar uma linha cujo contrato registrado não é o informado
    Dado que consultei a coordenação e o fornecedor tem contrato registrado
    Quando preencho a linha com a ação A e um número e um ano que não são os do registro, e confirmo com a opção ALT
    Então nada é alterado
    E nenhuma mensagem é mostrada

  Cenário: RN-15 — excluir um contrato que não está registrado na coordenação
    Dado que consultei a coordenação
    Quando preencho a linha com a ação E e um número e um ano de contrato que não estão registrados naquela coordenação
    Então vejo "* Registro nao cadastrado *"
    E nada é apagado

  Cenário: RN-20 — excluir o registro do contrato
    Dado que consultei a coordenação e o fornecedor tem contrato registrado
    E informo na linha o número e o ano desse contrato
    Quando preencho a linha com a ação E e confirmo com a opção ALT
    Então o registro do contrato é apagado
    E a operação fica registrada na auditoria como exclusão

  Cenário: RN-16 — consultar uma linha em branco
    Dado que estou na tela C690T com a opção ALT, numa coordenação já consultada
    Quando preencho uma linha sem o código do fornecedor e com a ação C ou X
    Então vejo "* Consulte linha preenchida *"
    E nenhuma linha é gravada

  Cenário: RN-16 — consultar a linha de um fornecedor sem contrato
    Dado que consultei a coordenação e o fornecedor tem permissão e não tem contrato registrado
    Quando preencho a linha com o código desse fornecedor e a ação C ou X, e confirmo
    Então vejo "* Fornecedor sem contrato FINCON cadastrado *"
    E nenhuma linha é gravada

  Cenário: RN-16 e RN-17 — consultar a linha impede a gravação da confirmação
    Dado que consultei a coordenação e o fornecedor tem contrato registrado
    E preencho uma linha com a ação C ou X
    E preencho outra linha com a ação I e o contrato do FINCON
    Quando confirmo com a opção ALT
    Então o contrato da outra linha não é gravado

  Cenário: RN-17 — uma linha recusada interrompe a confirmação
    Dado que consultei a coordenação
    E preencho uma linha com a ação I e um contrato válido
    E preencho uma linha seguinte com a ação I e um fornecedor sem permissão
    Quando confirmo com a opção ALT
    Então vejo "* Fornecedor nao cadastrado para esta permissao *"
    E as linhas seguintes à recusada não são conferidas nem gravadas

  Cenário: RN-23 — próxima tela informada
    Dado que estou na tela C690T
    Quando informo o código de uma próxima tela e confirmo
    Então a transação é encaminhada para a tela indicada
    E nenhuma conferência desta tela é feita

  Cenário: RN-24 — falha de banco durante a gravação
    Dado que a gravação do registro do contrato falha no banco
    Quando confirmo a alteração
    Então a transação é interrompida com a mensagem de erro do sistema
    E nada é considerado gravado
```
