# US — C835T — Manter os preços dos gêneros do período da estimativa

## Estória

Como **servidor de CRE que responde pela estimativa da merenda**, quero **manter a tabela de
preços dos gêneros de cada período da estimativa**, para que **o cálculo daquele período
tenha o preço certo de cada gênero sem que ninguém redigite a tabela a cada período novo**.

A estimativa de custo é calculada por período — de uma data de início a uma data limite —, e
o preço de cada gênero daquele período tem de estar na tabela do período antes de o cálculo
rodar: o cálculo **recusa o pedido** quando não encontra tabela de preços para a data limite
informada. É esta tela que mantém essa tabela, uma linha por gênero, com o preço. Para não
redigitar tudo a cada período novo, a tela também **copia** os preços de uma data já
cadastrada para o período em branco e **apaga** a tabela de um período inteiro quando ele foi
cadastrado errado. Sem ela, o período fica sem preço, o cálculo não fecha e a estimativa da
merenda daquele período não sai.

## Contexto

Jornada S000M → C000M → C800M → C840M → C835T.
Ator: servidor de CRE — escolhe o período, vê os preços dos gêneros daquele período e
inclui, altera ou exclui o preço de cada gênero; pode mandar copiar os preços de uma data já
cadastrada e pode apagar a tabela do período inteira.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os três menus do caminho (`C000M`, `C800M` e `C840M`) só
encaminham: não gravam nada e não decidem nada sobre esta tela — o menu que a abre só nomeia
a tela, e a opção de manutenção é digitada nela e reposta pelo que ela mesma guardou na
sessão (RN-02). Esta tela é **terminal**: não encadeia para nenhuma outra e não passa
registro nem operação adiante (RN-17).

Da sessão, esta tela usa o **tipo de órgão**, que faz parte da identidade da tabela e abre
toda leitura que ela faz; a **matrícula**, o **código de acesso** e o **privilégio** do
vínculo, que entram na conferência de permissão e na trilha de auditoria; a **coordenação
regional escolar** do vínculo, que vai na trilha; e a **descrição do tipo de órgão** e a
**data do sistema**, que ela exibe no cabeçalho. O que a entrada deixa e esta tela aproveita
está no anexo de evidências, em **Regras que se revelaram da entrada**.

Os cadastros de que a tela se serve — os dois cadastros de gêneros e a tabela de preços por
data, de onde a cópia tira os preços — são de outras telas e aqui só são lidos.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O que a tela mantém

A tela mantém a **tabela de preços dos gêneros de um período da estimativa**, no **tipo de
órgão** da sessão. O cabeçalho traz o **modo de uso**, a **data de início** e a **data
limite** do período, cada uma em dia, mês e ano, a **data de cópia** (dia, mês e ano) e a
**marca de exclusão da tabela inteira**. Abaixo vem a grade de **treze linhas**; cada linha
tem **sete informações**: a **subclasse** (2 dígitos), o **código do gênero** (5 dígitos), a
**descrição resumida do gênero**, um **indicador**, a **unidade de compra**, o **preço**
(6 dígitos, com 2 decimais) e a **ação** a executar naquela linha. A tela mostra também a
descrição do tipo de órgão da sessão e a data do sistema.

Um registro da tabela é identificado pelo **tipo de órgão**, pela **data limite** e pela
**subclasse e o gênero**; a data de início é guardada junto, mas **não distingue** um
registro do outro. A tabela comporta **100.000 registros** — capacidade é o máximo esperado
declarado no dicionário de dados, parâmetro de dimensionamento, não o volume cadastrado.

A tela é de **manutenção**, não de consulta: além de ler, ela grava. Das **seis bases** que
enxerga, só **duas** recebem escrita: a **tabela de preços do período** (RN-18) e a **trilha
de auditoria** (RN-14).

[?] O formulário da tela não veio no lote de fontes. O programa só declara o nome de **nove**
campos: as seis datas do período, a subclasse, o gênero e o preço. O texto que o operador lê
no campo do modo de uso e no da marca de exclusão não está em nenhum fonte lido, e os nomes
que o programa usa para os três campos da data de cópia são abreviaturas internas, não texto
de tela. Pergunta ao site.

### RN-02 — A tela abre em consulta, o modo não vem de quem a chamou, e só ALT e CON passam

O **modo de uso** admite **consulta** e **alteração**. Quem abre a tela é a opção do menu
`C840M`, e o menu só nomeia a tela: não manda modo nenhum. Na primeira vez da sessão, sem
modo guardado, a tela abre em **consulta**, sem período e sem linha nenhuma; depois disso,
ela repõe o modo que ela mesma guardou. Informando um modo diferente de consulta e de
alteração, o sistema recusa com **\* Opcao nao disponivel. Use ALT ou CON \***, devolve o
cursor ao campo do modo e, por esse caminho, não lê e não grava nada.

Todas as operações desta tela — incluir, alterar ou excluir o preço de um gênero, copiar os
preços de uma data e apagar a tabela do período inteiro — são feitas no modo de **alteração**.

[?] A recusa manda usar **ALT** ou **CON** e a conferência compara o campo com os códigos
internos de consulta e de alteração; nenhum fonte do lote mostra quem traduz o que o
operador digita. A mesma dúvida está registrada nas telas irmãs. Pergunta ao site.

### RN-03 — No modo consulta nada é gravado

Com o modo de uso em **consulta**, o tratamento das linhas é abandonado antes de qualquer
teste de ação, e a passagem que grava também é abandonada antes da cópia, da exclusão da
tabela e das linhas: a consulta percorre a tabela do período e não toca em nada.

### RN-04 — Os campos informados passam pela conferência de número antes de tudo

Antes de qualquer conferência de negócio, **doze** campos passam pela conferência de
numérico: o dia, o mês e o ano da data de início; o dia, o mês e o ano da data limite; o
dia, o mês e o ano da data de cópia; a subclasse; o gênero; e o preço. O preço é conferido
com **duas casas decimais**. Campo em branco vira **zero**; o que não for número é recusado,
o cursor volta ao próprio campo e nada mais é conferido nem gravado por causa dele.

[?] O texto que o operador vê quando um valor não numérico é recusado não está no programa:
a conferência é chamada de uma rotina de biblioteca cujo corpo não veio no lote. Pergunta ao
site.

[?] A conferência está sob a condição de a mensagem não ser automática, e o que distingue
uma mensagem de operador de uma mensagem automática não está explicado no acervo nem no
manual. Se existe um caminho de entrada em que ela não roda, não deu para determinar.
Pergunta ao site.

### RN-05 — O período tem de ser um intervalo de datas válido

Na **consulta**, quando o período informado difere do período já consultado, o sistema
confere: o **ano** da data de início e o da data limite têm de estar entre **1994** e
**2099**, e o **dia** tem de existir naquele mês e ano. Recusando, a mensagem é
**\* Data inicial do periodo invalida \*** ou **\* Data final do periodo invalida \***, com o
cursor na data correspondente, e nada é gravado. Passando, o sistema ainda exige que a
**data de início não seja maior que a data limite**; sendo, a recusa é
**\* Data inicial maior que data final \***, com o cursor no dia da data de início.

[?] O programa limita o ano de 1994 a 2099 e o acervo não diz de onde vêm esses limites.
Pergunta ao site.

[?] A conferência das datas só é executada na consulta: na alteração o período não é
reconferido, porque esse caminho só aceita o período que já foi consultado (RN-07). Se a
alteração deveria reconferir as datas que recebe, pergunta ao site.

### RN-06 — Sem preços no período, a consulta avisa

Sem nenhum preço cadastrado para o período informado, a página não mostra linha e avisa
**\* Tabela sem generos cadastrados \***; o aviso sai uma vez, na primeira linha da página.

[?] A mesma marca de "não encontrei" serve a dois casos — o período sem tabela nenhuma e o
fim da lista de registros daquele período — e por isso não se sabe se o aviso distingue "não
há tabela para este período" de "acabaram as linhas desta tabela". Pergunta ao site.

### RN-07 — Para alterar é preciso ter consultado o período

No modo **alteração**, o período informado tem de ser exatamente o período que a última
consulta deixou na sessão — as seis datas, uma a uma. Se não for, o sistema recusa com
**\* Consulte a tabela antes da atualizacao \***, devolve o cursor ao campo do modo e nada é
lido nem gravado.

É a regra de **consultar antes de atualizar** — e é também por ela que um período que ainda
não existe começa: a consulta mostra o período sem linhas e o deixa guardado como o
consultado, de modo que a alteração seguinte pode incluir os primeiros preços. Quando o
período consultado já tem tabela, a **data de início que passa a valer é a do registro
gravado**, e não a que foi digitada; a data limite continua a que foi digitada.

### RN-08 — A cópia traz os preços de uma data para o período

Informada a **data de cópia**, o sistema copia para a tabela do período em manutenção o
**preço de cada gênero** da tabela de preços daquela data, um registro por gênero, com a
data de início e a data limite do período. A cópia só acontece para um período que **ainda
não tem preço nenhum**: se o período já tem registro, a recusa é
**\* Ja existem registros cadastrados nesta tabela \***, com o cursor na data de cópia; e se
não existe tabela de preços naquela data, a recusa é
**\* Tabela para copia nao cadastrada \***, também com o cursor na data de cópia.

[?] Na cópia o cadastro de gêneros não é conferido: vêm os gêneros que a tabela da data
tiver, ainda que já não estejam vigentes, ao contrário da inclusão à mão, que exige gênero
vigente (RN-11). Se a cópia deveria trazer só gêneros vigentes, pergunta ao site.

[?] A recusa "Tabela para copia nao cadastrada" avisa, mas não interrompe: é o único ponto
desse bloco em que o sistema segue adiante depois de recusar. O pedido acaba sem copiar nada
de qualquer forma — a leitura seguinte não acha a tabela de origem —, mas o caminho não é o
mesmo dos outros. Se a intenção era parar ali, a guarda está incompleta. Pergunta ao site.

### RN-09 — A marca de exclusão apaga a tabela do período inteira

Com a **marca de exclusão da tabela** preenchida, o sistema apaga todos os registros do
período informado, um a um, deixando o rastro de cada um. Se o período não tem preço nenhum,
a recusa é **\* Nao existem registros cadastrados nesta tabela \***, com o cursor na marca, e
nada é apagado.

[?] A cópia e a exclusão da tabela inteira não se combinam: uma guarda exige que o período
esteja **vazio** para copiar e a guarda seguinte exige que ele **tenha registros** para
apagar, de modo que um pedido com as duas marcas preenchidas é sempre recusado — com uma das
duas mensagens, conforme o estado da tabela — e nem a cópia nem a exclusão acontecem. Se a
intenção era permitir trocar a tabela do período de uma vez (apagar e copiar no mesmo
pedido), o caminho não existe hoje. Não escolhi um dos dois lados; pergunta ao site.

[?] A tela reconhece um único valor na marca de exclusão e não dá rótulo ao campo: o acervo
não diz o que significam os outros valores nem como o operador preenche a marca. Pergunta ao
site.

### RN-10 — A linha só é tratada quando traz a subclasse e uma ação conhecida

Uma linha só é processada quando a **ação** é `I` (inclusão), `A` (alteração) ou `E`
(exclusão); ação em branco ou ação que a tela não reconhece simplesmente passa: nada é
recusado, nada é gravado para essa linha e nenhuma mensagem é mostrada. A conferência de
permissão da operação só acontece depois que a ação foi reconhecida.

[?] A conferência da linha começa abandonando qualquer linha **sem subclasse**, mas a
passagem que grava abandona a linha apenas quando a **subclasse e o gênero** estão ambos em
branco. Uma linha com a subclasse em branco e o gênero preenchido não passa, portanto, por
conferência nenhuma — nem a do gênero, nem a do preço, nem a da repetição, nem a da
permissão — e ainda assim chega à gravação, que age sobre o registro que a última leitura
deixou posicionado e não sobre a subclasse e o gênero informados. Ou a conferência deveria
cobrir esse caso, ou a gravação deveria ignorá-lo. Pergunta ao site.

### RN-11 — A inclusão exige gênero cadastrado, ainda fora da tabela, e o preço

Ao incluir, o sistema procura o gênero informado no **cadastro de gêneros** e exige que ele
esteja **vigente** na data limite do período. Não achando, ou achando um gênero que não está
vigente, a recusa é **\* Genero nao cadastrado \***, com o cursor na subclasse, e nada é
gravado. Em seguida confere se o gênero já está na tabela daquele período; estando, a recusa
é **\* Genero ja cadastrado nesta tabela \***, com o cursor na ação, e o preço que já estava
gravado não é tocado. Por fim, o **preço** é obrigatório: zerado, a recusa é
**\* Informe o preco do genero \***, com o cursor no preço, e nada é gravado.

Passando por tudo, nasce o registro do gênero naquele período, com a data de início e a data
limite do período e o preço informado, e o rastro fica na auditoria (RN-14).

[?] A mesma mensagem serve a duas situações distintas — gênero inexistente e gênero que não
está vigente — e o operador não fica sabendo qual foi. Pergunta ao site.

[?] Há **dois cadastros de gêneros** e a tela escolhe o cadastro pela subclasse: a subclasse
**99** é procurada num deles e as demais no outro, e só as linhas vindas do cadastro da
subclasse 99 aparecem marcadas com `*`. O acervo não diz o que distingue os dois cadastros
nem o que a marca `*` significa. Pergunta ao site.

[?] Nas linhas de subclasse **99** a **classe** que fica gravada é lida do cadastro que
**não** foi consultado nesse caminho, e o registro do período sai com a classe que estiver
ali — a do último gênero lido, ou zero. Não deu para concluir de onde a classe deveria vir
nesse caso. Pergunta ao site.

[?] A conferência do gênero vigente inclui a data limite do período na busca, mas as marcas
de leitura que dizem se a busca é por data exata ou por data a partir de não estão
explicadas no corpus nem no manual. A regra "vigente na data limite" é a leitura dos dados
informados, não uma semântica de dialeto confirmada. Pergunta ao site.

### RN-12 — A alteração exige o gênero na tabela do período e o preço, e grava o novo preço

A alteração exige o gênero informado na tabela daquele período — senão
**\* Genero nao cadastrado nesta tabela \***, com o cursor na ação, e nada é gravado — e o
**preço** preenchido — senão **\* Informe o preco do genero \***, com o cursor no preço.
Confirmada, o sistema trava o registro, substitui o preço pelo informado e grava; a data de
início, a data limite, a subclasse e o gênero continuam os mesmos.

[?] A gravação não reconfere a linha: ela age sobre o registro que a leitura da conferência
deixou posicionado. Se essa leitura for reexecutada ou avançar antes da gravação, o preço
informado pode cair em outro gênero. O acervo não permite concluir qual dos dois acontece.
Pergunta ao site.

### RN-13 — A exclusão apaga a linha da tabela do período

A exclusão exige o gênero informado na tabela daquele período; senão
**\* Genero nao cadastrado nesta tabela \***, com o cursor na ação, e nada é apagado.
Existindo, o registro é **apagado**: ele deixa a tabela e com ele o preço daquele gênero
naquele período. Não é marca de exclusão: aqui o registro desaparece.

### RN-14 — Toda operação confirmada deixa rastro na auditoria

Cada operação confirmada grava um registro na **trilha de auditoria** com o objeto (o
registro da tabela de preços), a operação (inclusão, alteração ou exclusão), o **valor
anterior** e o **posterior** do preço e o contexto da sessão — a matrícula, o tipo de órgão,
a coordenação regional escolar, o terminal, a data e a hora, o número do processo e o código
da base auditada. Na inclusão e na cópia o valor anterior vai em branco; na alteração vão o
preço como estava e como ficou; na exclusão vai o preço como estava e o posterior em branco.
A cópia da tabela e a exclusão da tabela inteira também deixam os seus rastros, um por
registro copiado ou apagado.

[?] O rastro da **inclusão de uma linha** e o da **cópia** ficam sob a condição de o estado
da mensagem não ser a marca de retorno automático do ambiente; o rastro da alteração, o da
exclusão e o da exclusão da tabela inteira não têm essa condição. Não deu para concluir se a
gravação do registro acontece na mesma passagem em que essa marca aparece — se acontecer,
essas duas operações gravam sem rastro. Pergunta ao site.

[?] O número do processo que a trilha guarda vem da sessão e esta tela não o monta; quem o
preenche não está nesta jornada. Pergunta ao site.

### RN-15 — A operação só acontece se o perfil autorizar

Antes de qualquer leitura da tabela, a tela passa pela **segurança de acesso à tela**: o
sistema procura a matrícula, confere que a estação é a da sessão e procura a autorização do
**código de acesso** do servidor para aquela tela; não estando autorizada, a sessão é
recusada e nada é lido. Depois, cada linha com ação reconhecida passa pela **segurança da
operação**: o sistema procura de novo a autorização do código de acesso e verifica se o
**flag da operação** (inclusão, alteração ou exclusão) está liberado; não estando, a operação
é recusada com mensagem e a tela é abandonada sem gravar. A cópia e a exclusão da tabela
inteira passam pela segurança da operação de **alteração**.

### RN-16 — A tela seguinte preenchida abandona a manutenção

Se a mensagem chega com o código da **próxima tela** preenchido, a manutenção é abandonada
antes de qualquer teste de linha: nada é conferido, nada é gravado e a sessão é encaminhada
para a tela indicada.

[?] O que preenche o código da próxima tela nesta tela não está no acervo: a tela não o
atribui em nenhum ponto. Pergunta ao site.

[?] A tela tem uma guarda própria para esse caso, mas o encaminhamento já acontece antes,
numa rotina de rota que encerra a manutenção; a guarda própria fica sem uso. Se a intenção
era avisar o operador antes de sair, esse aviso não chega a acontecer. Pergunta ao site.

### RN-17 — A tela é o fim da jornada

A tela não encadeia para nenhuma outra: não passa registro nem operação adiante, e o que ela
deixa para as próximas consultas é a tabela que gravou e o que guardou na sessão — o modo
usado e o período consultado (RN-02 e RN-07).

### RN-18 — A tela grava a tabela do período e a auditoria, e só lê os outros quatro cadastros

Para cada uma das **seis bases** que a tela enxerga, o gerador declara uma rotina de
gravação, uma de exclusão e uma de trava — **declarar não é usar**: o que a tela executa é a
gravação, a alteração e a exclusão da **tabela de preços do período** e a gravação da
**trilha de auditoria**. Os dois cadastros de gêneros, a tabela de preços por data e o
cadastro das telas são aqui apenas lidos: nenhuma rotina de gravação ou de exclusão deles
chega a rodar.

### RN-19 — Falha de banco interrompe a transação

Toda leitura da tela confere o erro do banco: o erro que **não** é o de registro não
encontrado interrompe a transação com a ação de erro do sistema, e o resto do processamento
não acontece. A gravação e a exclusão também conferem o erro do banco e interrompem do mesmo
modo. Não achar registro **não é erro**: é o caminho normal das conferências.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os preços dos gêneros do período da estimativa

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C835T

  Cenário: RN-01 — a consulta mostra a tabela do período
    Dado que estou na tela C835T no modo consulta
    E o período informado tem preços cadastrados
    Quando a página é apresentada
    Então vejo, em cada linha, a subclasse, o código do gênero, a descrição resumida, o indicador, a unidade de compra, o preço e a ação
    E vejo no máximo 13 linhas por vez
    E vejo a descrição do tipo de órgão da sessão e a data do sistema

  Cenário: RN-02 — abrir a tela sem nada guardado da vez anterior
    Dado que abro a tela C835T pela primeira vez na sessão
    Então ela está no modo consulta
    E não há período informado nem linha preenchida
    E nada é gravado

  Cenário: RN-02 — o menu que abre a tela não manda o modo
    Dado que abro a tela C835T pela opção do menu C840M
    Então o menu não interfere no modo da tela
    E a tela repõe o modo que ela mesma guardou da última transação

  Cenário: RN-02 — modo de uso não disponível
    Dado que estou na tela C835T
    Quando informo um modo de uso diferente de consulta e de alteração
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo do modo
    E nada é lido e nada é gravado

  Cenário: RN-03 — no modo consulta nada é gravado
    Dado que estou na tela C835T no modo consulta
    E preencho as linhas com ações e preços
    Quando confirmo a transação
    Então nenhum gênero é incluído, alterado ou excluído
    E nada é copiado e nada é apagado do período

  Cenário: RN-04 — valor não numérico em um campo informado
    Dado que estou na tela C835T
    Quando informo um valor não numérico em um dos campos de data, na subclasse, no gênero ou no preço
    Então o campo é recusado antes de qualquer conferência de negócio
    E o cursor volta ao campo recusado
    E nada mais é conferido nem gravado por causa dele

  Cenário: RN-05 — data de início que não existe
    Dado que estou na tela C835T no modo consulta
    Quando informo uma data de início inexistente ou com o ano fora da faixa aceita
    Então vejo "* Data inicial do periodo invalida *"
    E o cursor volta à data de início
    E nada é gravado

  Cenário: RN-05 — data limite que não existe
    Dado que estou na tela C835T no modo consulta
    Quando informo uma data limite inexistente ou com o ano fora da faixa aceita
    Então vejo "* Data final do periodo invalida *"
    E o cursor volta à data limite
    E nada é gravado

  Cenário: RN-05 — data de início maior que a data limite
    Dado que estou na tela C835T no modo consulta
    Quando informo uma data de início maior que a data limite
    Então vejo "* Data inicial maior que data final *"
    E o cursor volta ao dia da data de início
    E nada é gravado

  Cenário: RN-05 — a alteração não reconfere as datas
    Dado que estou na tela C835T no modo alteração
    E informo o período que consultei
    Quando confirmo a transação
    Então as datas do período não passam pela conferência de data válida

  Cenário: RN-06 — período sem preços cadastrados
    Dado que estou na tela C835T no modo consulta
    E não há preço nenhum para o período informado
    Quando a página é apresentada
    Então vejo "* Tabela sem generos cadastrados *"
    E a página não mostra linha alguma
    E nada é gravado

  Cenário: RN-07 — alterar sem ter consultado o período
    Dado que estou na tela C835T no modo alteração
    E informo um período diferente do que a última consulta deixou
    Quando confirmo a transação
    Então vejo "* Consulte a tabela antes da atualizacao *"
    E o cursor fica no campo do modo
    E nada é lido e nada é gravado

  Cenário: RN-07 — a consulta deixa o período guardado
    Dado que consultei um período que ainda não tem preço nenhum
    Quando passo para o modo alteração com o mesmo período
    Então a alteração é aceita
    E posso incluir os primeiros preços daquele período

  Cenário: RN-07 — o início do período vem do registro gravado
    Dado que estou na tela C835T no modo consulta
    E o período informado já tem preços cadastrados com outra data de início
    Quando confirmo a consulta
    Então a data de início que a tela mostra é a do registro gravado
    E a data limite é a que informei

  Cenário: RN-08 — copiar os preços de uma data para o período
    Dado que estou na tela C835T no modo alteração
    E consultei um período que ainda não tem preço nenhum
    E existe tabela de preços na data de cópia que informei
    Quando confirmo a cópia
    Então nasce um registro naquele período para cada gênero da tabela daquela data
    E cada registro fica com o preço que estava na tabela daquela data
    E cada cópia fica registrada na auditoria

  Cenário: RN-08 — copiar para um período que já tem preços
    Dado que estou na tela C835T no modo alteração
    E o período informado já tem preços cadastrados
    Quando confirmo a cópia
    Então vejo "* Ja existem registros cadastrados nesta tabela *"
    E o cursor fica na data de cópia
    E nada é copiado

  Cenário: RN-08 — copiar de uma data sem tabela de preços
    Dado que estou na tela C835T no modo alteração
    E não existe tabela de preços na data de cópia que informei
    Quando confirmo a cópia
    Então vejo "* Tabela para copia nao cadastrada *"
    E o cursor fica na data de cópia
    E nada é copiado

  Cenário: RN-09 — apagar a tabela do período inteiro
    Dado que estou na tela C835T no modo alteração
    E o período informado tem preços cadastrados
    Quando marco a exclusão da tabela e confirmo
    Então todos os registros daquele período são apagados
    E cada registro apagado fica registrado na auditoria

  Cenário: RN-09 — apagar um período sem preços
    Dado que estou na tela C835T no modo alteração
    E o período informado não tem preço nenhum
    Quando marco a exclusão da tabela e confirmo
    Então vejo "* Nao existem registros cadastrados nesta tabela *"
    E o cursor fica na marca de exclusão
    E nada é apagado

  Cenário: RN-09 — copiar e apagar no mesmo pedido
    Dado que estou na tela C835T no modo alteração
    E consultei o período
    Quando informo a data de cópia e marco a exclusão da tabela no mesmo pedido
    Então o pedido é recusado
    E a mensagem é a de tabela já cadastrada ou a de tabela sem registros, conforme o estado do período
    E nada é copiado e nada é apagado

  Cenário: RN-10 — linha com ação em branco ou desconhecida
    Dado que estou na tela C835T no modo alteração
    Quando preencho a linha com uma ação diferente de I, A e E
    Então aquela linha não é conferida
    E nada é gravado para ela
    E nenhuma mensagem é mostrada

  Cenário: RN-10 — linha sem a subclasse
    Dado que estou na tela C835T no modo alteração
    Quando deixo a subclasse em branco
    Então a linha não passa por nenhuma conferência
    E nenhuma mensagem é mostrada

  Cenário: RN-11 — incluir um gênero não cadastrado ou não vigente
    Dado que estou na tela C835T no modo alteração
    Quando tento incluir um gênero que não existe no cadastro ou que não está vigente na data limite do período
    Então vejo "* Genero nao cadastrado *"
    E o cursor fica na subclasse
    E nada é gravado

  Cenário: RN-11 — incluir um gênero que já está no período
    Dado que estou na tela C835T no modo alteração
    E o gênero já está na tabela daquele período
    Quando confirmo a inclusão desse gênero
    Então vejo "* Genero ja cadastrado nesta tabela *"
    E o cursor fica na ação
    E o preço que já estava gravado não é alterado

  Cenário: RN-11 — incluir sem o preço
    Dado que estou na tela C835T no modo alteração
    E o gênero está cadastrado, vigente e ainda não está na tabela daquele período
    Quando confirmo a inclusão sem informar o preço
    Então vejo "* Informe o preco do genero *"
    E o cursor fica no preço
    E nada é gravado

  Cenário: RN-11 — incluir um gênero no período
    Dado que estou na tela C835T no modo alteração
    E o gênero está cadastrado, vigente e ainda não está na tabela daquele período
    Quando informo o preço e confirmo a ação I
    Então o registro é gravado na tabela daquele período
    E com a data de início e a data limite do período
    E a inclusão fica registrada na auditoria

  Cenário: RN-12 — alterar um gênero fora do período
    Dado que estou na tela C835T no modo alteração
    Quando confirmo a ação A para um gênero que não está na tabela daquele período
    Então vejo "* Genero nao cadastrado nesta tabela *"
    E o cursor fica na ação
    E nada é gravado

  Cenário: RN-12 — alterar sem o preço
    Dado que estou na tela C835T no modo alteração
    E o gênero está na tabela daquele período
    Quando confirmo a ação A sem informar o preço
    Então vejo "* Informe o preco do genero *"
    E o cursor fica no preço
    E nada é gravado

  Cenário: RN-12 — alterar o preço de um gênero do período
    Dado que estou na tela C835T no modo alteração
    E o gênero está na tabela daquele período
    Quando informo o novo preço e confirmo a ação A
    Então o novo preço fica gravado no registro daquele gênero naquele período
    E a data de início, a data limite, a subclasse e o gênero continuam os mesmos
    E o preço como estava e como ficou fica registrado na auditoria

  Cenário: RN-13 — excluir um gênero do período
    Dado que estou na tela C835T no modo alteração
    E o gênero está na tabela daquele período
    Quando confirmo a ação E
    Então o registro é apagado da tabela daquele período
    E o gênero deixa de aparecer na consulta daquele período
    E o preço que havia fica registrado na auditoria

  Cenário: RN-13 — excluir um gênero fora do período
    Dado que estou na tela C835T no modo alteração
    E o gênero não está na tabela daquele período
    Quando confirmo a ação E
    Então vejo "* Genero nao cadastrado nesta tabela *"
    E o cursor fica na ação
    E nada é apagado

  Cenário: RN-14 — toda operação confirmada deixa rastro na auditoria
    Dado que confirmei uma inclusão, uma alteração ou uma exclusão na C835T
    Quando a gravação termina
    Então existe um registro de auditoria da tabela de preços
    E com a operação e com o preço anterior e o posterior
    E com a matrícula, o tipo de órgão, a coordenação regional escolar, o terminal, a data e a hora e o número do processo

  Cenário: RN-15 — a tela não autorizada para o meu código de acesso
    Dado que o meu código de acesso não tem a tela C835T autorizada
    Quando a tela começa a ser tratada
    Então a sessão é recusada
    E nada é lido e nada é gravado

  Cenário: RN-15 — operação não autorizada pelo perfil
    Dado que o meu código de acesso não tem o flag da operação pretendida
    Quando confirmo a ação de incluir, alterar ou excluir
    Então o sistema recusa a operação com mensagem
    E nada é gravado

  Cenário: RN-15 — a cópia e a exclusão da tabela passam pela alteração
    Dado que o meu código de acesso tem a alteração liberada
    E não tem a inclusão nem a exclusão liberadas
    Quando confirmo a cópia ou a exclusão da tabela do período
    Então a operação é aceita quanto à permissão
    E o que decide é a autorização de alteração

  Cenário: RN-16 — a próxima tela preenchida abandona a manutenção
    Dado que a mensagem chega à C835T com o código da próxima tela preenchido
    Quando a manutenção começaria
    Então a linha não é conferida e nada é gravado
    E a sessão é encaminhada para a tela indicada

  Cenário: RN-17 — a tela não encadeia para outra
    Dado que concluí uma consulta ou uma alteração
    Então nenhum registro e nenhuma operação são passados a outra tela
    E o que fica para as próximas consultas é a tabela gravada e o que a tela guardou na sessão

  Cenário: RN-18 — a tela só grava a tabela do período e a auditoria
    Dado que consultei um período
    Quando confirmo a consulta
    Então os dois cadastros de gêneros, a tabela de preços por data e o cadastro das telas são apenas lidos
    E nenhuma rotina de gravação ou de exclusão deles é executada

  Cenário: RN-19 — falha de banco durante a gravação
    Dado que a gravação da tabela do período falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E o preço não é considerado gravado

  Cenário: RN-19 — registro não encontrado não é erro
    Dado que estou na tela C835T no modo alteração
    Quando confirmo a ação E para um gênero que não está na tabela do período
    Então o sistema mostra a recusa da conferência
    E a transação segue pelo caminho normal, sem ser interrompida por erro de banco
```
