# US — N032T — Troca da fonte de recursos das notas fiscais de um processo

## Estória

Como **servidor da CRE que lança e corrige a despesa da minha secretaria**, quero **trocar a
fonte de recursos das notas fiscais de um processo já registrado — e a dos itens dessas
notas**, para que **a despesa daquele processo passe a contar a fonte certa sem que as notas
tenham de ser lançadas de novo**.

A fonte de recursos é a classificação que amarra o dinheiro da secretaria: cada nota fiscal e
cada item dela nasce apontando para uma fonte, e uma fonte errada contamina o processo
inteiro. Esta é a tela que corrige a fonte enquanto o processo ainda não tem pagamento lançado
ao fornecedor; havendo pagamento, a correção é feita pela tela do pagamento, que é quem
alcança as notas. A consulta existe e é só leitura: percorrer o processo não muda nada.

## Contexto

Jornada S000M → N000M → N050M → N032T.
Ator: servidor de CRE — localiza um processo da sua secretaria pelo número, informa o empenho
e o ano de referência, confere o fornecedor, o total das notas e a fonte que está lá, e troca
a fonte das notas fiscais e dos itens.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As duas telas anteriores da jornada são menus: elas não encadeiam a N032T, não decidem o modo
dela e não deixam dado de negócio para ela. O que a N032T usa — a matrícula funcional, o
código de acesso, o privilégio, o tipo de órgão e a coordenadoria regional escolar — é o que
a entrada deixou na sessão. A N032T é o último passo da jornada: por este caminho ela não
encadeia outra tela e não entrega registro nem operação a ninguém.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela troca a fonte de recursos das notas fiscais e dos itens do processo

A tela tem uma única operação de escrita: reescrever a **fonte de recursos**. Ela percorre as
notas fiscais do processo no tipo de órgão da sessão e, em cada nota, os itens daquela nota, e
grava nos dois a nova fonte. Nada mais é tocado: fornecedor, valores, datas e situação
continuam como estavam, e nenhuma nota e nenhum item é incluído ou excluído. O que a tela cria
é só o registro de auditoria (RN-19), e o processo sobre o qual ela escreve é o que a consulta
deixou em uso (RN-07).

### RN-02 — O número do processo é informado em quatro partes, e a segunda pode ficar em branco

O número do processo — catorze dígitos — é informado em quatro partes, nesta ordem: duas de
**2 dígitos**, uma de **6** e uma de **4**. A segunda parte pode ficar em branco: em branco —
ou zerada —, os dois dígitos da primeira passam a valer como a segunda dupla do número, e as
duas primeiras posições do número ficam zeradas. Nas duas formas o número que a tela usa é o
mesmo.

[?] O que cada uma das quatro partes representa em negócio não está no programa: a tela as
valida como número e as junta em posições fixas. A primeira é o código de secretaria que o
cadastro do tipo de órgão da sessão define (RN-03); as outras três, o acervo lido não nomeia.
Pergunta ao site.

### RN-03 — A tela abre em consulta, e a primeira parte do número vem preenchida

Ao abrir, a tela assume sozinha a **consulta**. A primeira parte do número do processo vem
preenchida com o **código de secretaria** que o cadastro do tipo de órgão da sessão define — o
mesmo código com que a tela que cria o processo inicia o número. Se a sessão já tem um
processo em uso, a tela o retoma (RN-04) e não recoloca o código.

[?] O cadastro do tipo de órgão guarda, além desse código, outros cinco códigos numerados de
secretaria municipal; por que é esse, e não outro, que preenche a primeira parte, o acervo
lido não diz. Pergunta ao site.

[?] O que o operador lê ao lado de cada parte do número não está no programa: as partes que
passam pela edição numérica são identificadas por códigos internos, e não por um nome de
negócio. O que a máscara escreve ali o acervo lido não tem. Pergunta ao site.

### RN-04 — A tela retoma o processo, o empenho e o ano que a consulta deixou em uso

O **processo**, o **empenho** e o **ano de referência** que a última consulta aceitou voltam à
tela na abertura seguinte, e é esse conjunto que a alteração exige (RN-07). O que a tela
guarda sobrevive de uma operação para a outra; uma consulta recusada esquece o conjunto
(RN-11, RN-13, RN-14 e RN-15), e uma nova consulta o substitui.

[?] De quem é essa memória — do terminal, do servidor ou só da tela — o acervo lido não
documenta. Pergunta ao site.

### RN-05 — Com um processo em uso, a abertura mostra o fornecedor, o total das notas e a fonte atual

Quando a tela é aberta e já há um processo em uso, ela mostra o **fornecedor** (o código e a
razão social), o **total das notas** — a soma dos valores de todas as notas fiscais daquele
processo — e a **fonte de recursos atual**. Mostra também a descrição do tipo de órgão e a
data do sistema, que vêm da sessão. O fornecedor e a fonte saem da **primeira** nota
encontrada para o processo; o total soma todas. As notas cuja última manutenção foi uma
exclusão ficam de fora da conta. O cadastro das notas fiscais comporta até **29.000.000** de
registros — **capacidade** (o máximo esperado, dado de dimensionamento), não volume
cadastrado.

[?] Se as notas do mesmo processo tiverem fontes diferentes, a tela mostra a da primeira e é
contra ela que a alteração confere a nova fonte (RN-10) — e depois a troca sobrescreve todas.
Se isso é o projeto ou um resto do gerador, o acervo lido não diz. Pergunta ao site.

### RN-06 — A tela só aceita alteração e consulta

A tela faz duas coisas: **alteração** e **consulta**. Qualquer outra opção é recusada com
**\* Operacao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da opção, e nenhum
cadastro de negócio é lido ou gravado.

[?] A mensagem nomeia as opções como ALT e CON, mas a tela confere a opção contra os códigos
internos de alteração e de consulta do sistema — e é o código interno que ela própria escreve
nesse campo ao abrir. Nenhum programa do acervo lido mostra quem traduz o que o operador
digita no código conferido; se não houver essa tradução, toda opção é recusada, inclusive as
duas que a mensagem pede. E, para uma opção que não seja nenhuma das cinco operações do
sistema, quem recusa primeiro é a conferência de rota, com a mensagem **\* Operacao nao
disponivel \***, sem o "Use ALT ou CON"; qual das duas o servidor vê depende de a rotina que
apresenta a mensagem marcar o erro, e essa rotina não está no acervo lido. Pergunta ao site.

### RN-07 — A alteração exige a consulta anterior do mesmo processo, empenho e ano

A alteração só começa quando o **processo**, o **empenho** e o **ano de referência**
informados são exatamente os que a consulta anterior deixou em uso (RN-04). Diferindo
qualquer um deles, a tela recusa com **\* Consulte antes de atualizar \***, devolve o cursor ao
campo da opção e não grava nada.

[?] As recusas desta regra e das três seguintes (RN-08, RN-09 e RN-10) só apresentam a
mensagem: nada nos programas desta jornada marca a operação como falha na área da tela, e a
etapa que grava é chamada logo depois, atrás de uma conferência do erro do sistema. Essa
conferência depende da rotina que apresenta as mensagens, e nenhum arquivo do acervo lido a
define. Se ela não marcar o erro, a alteração recusada grava assim mesmo — inclusive a fonte
que acabou de ser recusada, e no processo que a consulta deixou em uso, que pode não ser o que
estava na tela. Ou a recusa barra, ou é só aviso: o acervo lido não decide, e não se escolhe
um dos lados. Pergunta ao site.

### RN-08 — A nova fonte é obrigatória

A alteração exige uma **nova fonte**: em branco — ou zerada —, a tela recusa com
**\* Informe a fonte correta \***, devolve o cursor ao campo da nova fonte e não grava nada.

### RN-09 — A nova fonte tem de estar cadastrada para o órgão da sessão

A nova fonte tem de existir no **cadastro de fontes de recursos** do **tipo de órgão da
sessão**. Se não existir, a tela recusa com **\* Fonte nao cadastrada \***, devolve o cursor
ao campo da nova fonte e não grava nada.

[?] A leitura que confere a fonte não descarta os registros marcados como excluídos, embora o
cadastro das fontes tenha essa marca e outros cadastros desta jornada tenham leituras que a
respeitam. Se uma fonte excluída ainda puder ser alcançada, esta tela a aceita. Pergunta ao
site.

### RN-10 — A nova fonte tem de ser diferente da fonte que a tela mostra

A alteração exige que a nova fonte seja **diferente** da que está no campo da fonte atual do
processo. Igual, a tela recusa com **\* Altere a fonte \***, devolve o cursor ao campo da nova
fonte e não grava nada.

### RN-11 — Processo sem empenho lançado manda para a N016T

A consulta exige que o processo tenha **empenho lançado**. Não havendo nenhum lançamento para
o número informado, a recusa é **\* Atualize a fonte na tela N016T \***, o cursor volta à
**segunda parte do número do processo** e a tela **esquece o processo que estava em uso** — a
alteração seguinte volta a exigir consulta.

[?] A mensagem manda o servidor à N016T, mas quem grava o lançamento do processo no empenho
não é essa tela: a N016T grava as notas fiscais e os itens do processo e nunca executa a
gravação do lançamento. O que a mensagem espera que o servidor faça lá, o acervo lido não diz.
Pergunta ao site.

### RN-12 — O empenho e o ano de referência são obrigatórios na consulta

Consultar sem o **número do empenho** é recusado com **\* Informe o empenho \***, com o cursor
de volta ao campo do empenho; sem o **ano de referência**, com **\* Informe o exercicio \***,
com o cursor de volta ao campo do ano. Nas duas recusas o processamento para ali.

### RN-13 — O empenho informado tem de estar lançado no processo

A consulta exige que exista, para o processo e para o empenho e o ano informados, o
**lançamento do processo naquele empenho** — o que a mensagem chama de pagamento. Sem ele, a
recusa é **\* Pagamento nao cadastrado neste empenho \***, o cursor volta ao campo do empenho
e a tela esquece o processo que estava em uso.

[?] A leitura que procura esse lançamento não descarta os registros marcados como excluídos,
embora o mesmo cadastro tenha outra leitura que os descarta. Se um lançamento excluído ainda
puder ser encontrado, a consulta passa por ele. Pergunta ao site.

### RN-14 — Processo que já tem pagamento ao fornecedor manda para a F042T

Se já existir **pagamento ao fornecedor** lançado para aquele processo, empenho e ano, esta
tela não faz a troca: recusa com **\* Atualize a fonte na tela F042T \***, devolve o cursor à
**segunda parte do número do processo** e esquece o processo que estava em uso. É a tela do
pagamento que corrige a fonte nesse caso.

[?] Essa conferência só é feita na consulta: a alteração não a repete. Se o pagamento ao
fornecedor for lançado depois da consulta e antes da alteração, a troca passa assim mesmo.
Pergunta ao site.

[?] A leitura que procura esse pagamento também não descarta os registros marcados como
excluídos. Pergunta ao site.

### RN-15 — A consulta só aceita o empenho de maior valor do processo

Entre os lançamentos do processo, a tela procura o de **maior valor** e compara o empenho e o
ano informados com os dele. Informando qualquer outro empenho do processo, a recusa é uma
mensagem que **mostra o número do empenho de maior valor** seguido de **\<- Empenho de maior
valor \***, o cursor volta ao campo do empenho e o processo em uso é esquecido.

[?] A procura do empenho de maior valor ignora os lançamentos sem número de empenho; se o
processo não tiver nenhum lançamento com empenho, a tela não tem contra o que comparar e a
consulta é recusada apontando um empenho de maior valor em branco. Pergunta ao site.

### RN-16 — A alteração reescreve a fonte de cada nota e de cada item

Passadas as conferências, a alteração percorre as notas fiscais do processo e, em cada nota,
os itens dela, e grava a nova fonte nos dois. Ficam de fora as notas cuja última manutenção
foi uma exclusão e os itens nessa mesma situação. Se o processo não tiver nota nenhuma, a
alteração termina sem gravar.

[?] O laço dos itens de cada nota só termina quando não há mais registros, sem comparar o que
leu com a nota corrente — ao contrário do laço das notas, que confere o processo e o órgão a
cada volta. Se essa leitura passar da nota, a tela altera itens de outra nota. Pergunta ao
site.

### RN-17 — A alteração desiste em silêncio quando o empenho de maior valor mudou

Antes de gravar, a alteração refaz a procura do **empenho de maior valor** do processo que a
consulta deixou em uso e só segue se ele continuar sendo o mesmo. Se os lançamentos do
processo mudaram entre a consulta e a alteração, a tela **volta sem gravar e sem avisar**.

[?] A tela não diz nada quando desiste por esse motivo: nada é gravado e o servidor não recebe
mensagem. Se a intenção era avisar, o aviso não existe por este caminho. Pergunta ao site.

### RN-18 — A consulta não grava nada

Na consulta a tela lê o processo, os lançamentos, o fornecedor e as notas fiscais, e não
executa gravação nenhuma: nenhuma nota, nenhum item e nenhum lançamento é alterado e nenhum
registro de auditoria é criado. O que a consulta deixa é só o processo, o empenho e o ano em
uso (RN-04).

### RN-19 — Cada nota e cada item alterados deixam rastro na auditoria

Para **cada item** e para **cada nota fiscal** alterados, a tela grava um registro na
auditoria: o cadastro de origem, a operação de alteração, o número do processo, o conteúdo
**anterior** e o **novo** — que diferem exatamente na fonte — e o contexto da sessão
(matrícula, tipo de órgão, coordenadoria, terminal, data e hora, e o ano e o mês de
referência). O cadastro de auditoria comporta até **60.000.000** de registros —
**capacidade**, não volume cadastrado. O rastro é gravado **antes** da gravação do cadastro, e
um aborto dele impede a gravação.

[?] O passo de auditoria pode não rodar: o trecho que o executa sai sem gravar quando o erro
do sistema está marcado e, também, quando as chaves de distribuição automática do ambiente não
coincidem — e esta tela não preenche essas chaves. Com que valores elas chegam, o acervo lido
não diz. Pergunta ao site.

### RN-20 — Antes de cada operação o sistema confere a sessão, a tela, o acesso e a operação

Ao abrir e ao confirmar, a tela passa pelas conferências do sistema. O servidor tem de estar
no **terminal** em que a sessão foi aberta — em outro, o acesso é encerrado; a **tela** tem de
estar registrada, senão **\* Tela nao disponivel \*** na abertura e **\* Tela nao cadastrada
\*** na confirmação; o **código de acesso** da matrícula tem de ter a tela autorizada, senão
**\* Acesso negado para esta matricula \***; e a **operação** pedida tem de constar do perfil
do código de acesso — a alteração exige o direito de alteração, senão **\* Acesso negado para
esta operacao \***. A consulta não exige direito nenhum. Sem passar por tudo, nada é lido e
nada é gravado.

[?] O perfil da tela guarda quatro permissões — inclusão, alteração, exclusão e consulta —,
mas a conferência da consulta só olha as três primeiras. Quem tem a tela autorizada consulta
sem a permissão de consulta. Pergunta ao site.

### RN-21 — Os campos numéricos da página passam por edição numérica

Os **dez campos numéricos** da página passam pela edição numérica do sistema: campo em branco
vira zero e o que não for número é recusado, com o cursor de volta ao primeiro campo recusado.
São eles: as quatro partes do número do processo, o número do empenho, o ano de referência, o
código do fornecedor, o valor total das notas, o código da fonte atual e o código da nova
fonte.

[?] **Quatro** desses dez campos não têm posição de cursor declarada na tela: quando a edição
recusa um deles, não se sabe para onde o cursor volta. E o que o operador vê na recusa também
não está nos programas desta jornada — a rotina que faz a edição não faz parte do acervo lido.
Pergunta ao site.

### RN-22 — Cada operação começa com os campos de resultado limpos

Antes de conferir qualquer coisa, cada operação enviada começa apagando o que a operação
anterior tinha mostrado fora do processo: a **descrição do tipo de órgão**, a **data do
sistema** e a **razão social do fornecedor**.

### RN-23 — A recusa de destino inválido não é apresentada por esta tela

A recusa de **destino inválido** existe no trecho que a tela executa para gravar a auditoria, e
a ficha estrutural da tela a lista entre as suas mensagens. Esse caminho só roda com o modo de
distribuição automática preenchido, e a própria tela limpa esse campo imediatamente antes de
executar o trecho. Pela N032T, portanto, essa mensagem não é apresentada.

[?] Divergência entre a ficha e o comportamento, a confirmar com quem mantém o grafo.

---

## Cenários BDD

```gherkin
Funcionalidade: Troca da fonte de recursos das notas fiscais de um processo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N032T

  Cenário: A abertura da tela
    Quando abro a tela N032T
    Então ela abre em consulta
    E a primeira parte do número do processo vem preenchida com o código de secretaria
      do tipo de órgão da minha sessão
    E nada é gravado

  Cenário: A tela retoma o processo, o empenho e o ano consultados antes
    Dado que consultei um processo nesta sessão
    Quando abro a tela N032T de novo
    Então ela retoma o processo, o empenho e o ano que estavam em uso

  Cenário: A abertura com um processo em uso mostra o fornecedor, o total das notas e a fonte atual
    Dado que consultei um processo nesta sessão
    E que o processo tem notas fiscais
    Quando abro a tela N032T de novo
    Então vejo o código e a razão social do fornecedor da primeira nota
    E vejo o valor somado de todas as notas do processo
    E vejo a fonte de recursos atual
    E vejo a descrição do tipo de órgão e a data do sistema

  Cenário: O número do processo com a segunda parte em branco
    Dado que preencho a primeira parte do número do processo com dois dígitos
    E deixo a segunda parte em branco
    Quando a tela monta o número do processo
    Então esses dois dígitos passam a valer como a segunda dupla do número
    E as duas primeiras posições do número ficam zeradas

  Cenário: A consulta de um processo lançado no empenho informado
    Dado que o processo tem lançamento no empenho e no ano que informei
    E que esse empenho é o de maior valor do processo
    E que não existe pagamento ao fornecedor para esse empenho e esse ano
    Quando peço a consulta
    Então a tela aceita a consulta
    E passa a guardar o processo, o empenho e o ano para a alteração seguinte
    E nada é gravado

  Cenário: A consulta não grava nada
    Dado que consultei um processo
    Quando a consulta termina
    Então nenhuma nota fiscal e nenhum item são alterados
    E nenhum lançamento é alterado
    E nenhum registro de auditoria é criado

  Cenário: A troca da fonte das notas fiscais e dos itens
    Dado que consultei o processo
    Quando informo uma nova fonte cadastrada para o meu tipo de órgão e diferente da atual
    E peço a alteração
    Então as notas fiscais do processo ficam com a nova fonte
    E cada item dessas notas fica com a nova fonte
    E os valores, as datas, a situação e o fornecedor continuam como estavam

  Cenário: Cada nota e cada item alterados deixam rastro na auditoria
    Dado que consultei o processo e troquei a fonte
    Quando a gravação termina
    Então existe um registro de auditoria para cada nota fiscal alterada
    E existe um registro de auditoria para cada item alterado
    E o conteúdo anterior e o novo de cada registro diferem só na fonte
    E cada registro guarda a matrícula, o tipo de órgão, a coordenadoria, o terminal,
      a data e a hora da sessão

  Cenário: A nota fiscal e o item excluídos ficam de fora
    Dado que o processo tem uma nota fiscal cuja última manutenção foi uma exclusão
    Quando troco a fonte do processo
    Então aquela nota fiscal e os itens dela não são alterados

  Cenário: A tela só aceita alteração e consulta
    Dado que estou na tela N032T
    Quando informo uma opção diferente de ALT e de CON
    Então vejo "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é lido nem gravado

  Cenário: A alteração de um processo que não foi consultado
    Dado que o processo, o empenho ou o ano informados não são os que a consulta
      deixou em uso
    Quando peço a alteração
    Então vejo "* Consulte antes de atualizar *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: A alteração sem a nova fonte
    Dado que consultei o processo
    E deixo a nova fonte em branco
    Quando peço a alteração
    Então vejo "* Informe a fonte correta *"
    E o cursor volta ao campo da nova fonte
    E nada é gravado

  Cenário: A nova fonte que não existe para o tipo de órgão
    Dado que consultei o processo
    Quando informo, como nova fonte, uma que não está cadastrada para o meu tipo de órgão
    Então vejo "* Fonte nao cadastrada *"
    E o cursor volta ao campo da nova fonte
    E nada é gravado

  Cenário: A nova fonte igual à fonte que a tela mostra
    Dado que consultei o processo
    Quando informo, como nova fonte, a fonte que a tela está mostrando
    Então vejo "* Altere a fonte *"
    E o cursor volta ao campo da nova fonte
    E nada é gravado

  Cenário: A consulta de um processo sem empenho lançado
    Dado que não existe nenhum lançamento para o número do processo que informei
    Quando peço a consulta
    Então vejo "* Atualize a fonte na tela N016T *"
    E o cursor volta à segunda parte do número do processo
    E a tela esquece o processo que estava em uso

  Cenário: A consulta sem o número do empenho
    Dado que o processo tem lançamento
    E deixo o número do empenho em branco
    Quando peço a consulta
    Então vejo "* Informe o empenho *"
    E o cursor volta ao campo do empenho

  Cenário: A consulta sem o ano de referência
    Dado que informei o número do empenho
    E deixo o ano de referência em branco
    Quando peço a consulta
    Então vejo "* Informe o exercicio *"
    E o cursor volta ao campo do ano

  Cenário: O empenho sem lançamento no processo
    Dado que não existe lançamento do processo para o empenho e o ano informados
    Quando peço a consulta
    Então vejo "* Pagamento nao cadastrado neste empenho *"
    E o cursor volta ao campo do empenho
    E a tela esquece o processo que estava em uso

  Cenário: O processo que já tem pagamento ao fornecedor
    Dado que existe pagamento ao fornecedor para o processo, o empenho e o ano informados
    Quando peço a consulta
    Então vejo "* Atualize a fonte na tela F042T *"
    E o cursor volta à segunda parte do número do processo
    E a tela esquece o processo que estava em uso

  Cenário: O empenho que não é o de maior valor do processo
    Dado que o processo tem mais de um empenho lançado
    Quando informo um empenho que não é o de maior valor
    Então vejo o número do empenho de maior valor seguido de "<- Empenho de maior valor *"
    E o cursor volta ao campo do empenho
    E a tela esquece o processo que estava em uso

  Cenário: A alteração desiste em silêncio quando o empenho de maior valor mudou
    Dado que consultei o processo
    E que o empenho de maior valor do processo deixou de ser o que a consulta guardou
    Quando peço a alteração
    Então nada é gravado
    E não recebo mensagem nenhuma

  Cenário: A tela não cadastrada
    Dado que a tela N032T não está registrada
    Quando tento abrir a tela
    Então vejo "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que o código de acesso da minha matrícula não tem a tela N032T autorizada
    Quando tento abrir a tela
    Então vejo "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: A operação não autorizada pelo perfil
    Dado que o meu perfil não dá o direito de alteração
    Quando peço a alteração
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: A digitação que não é número
    Dado que digito, num dos campos numéricos da página, algo que não é número
    Quando peço a operação
    Então o cursor volta ao primeiro campo recusado
    E a operação não é feita

  Cenário: Cada operação começa com os campos de resultado limpos
    Dado que a tela já mostrou a descrição do tipo de órgão, a data do sistema
      e a razão social do fornecedor
    Quando envio uma nova operação
    Então a descrição do tipo de órgão, a data do sistema e a razão social do fornecedor
      não ficam na tela

  Cenário: A recusa de destino inválido não é apresentada
    Dado que estou na tela N032T em alteração e confirmei a troca da fonte
    Quando a tela grava o registro de auditoria
    Então ela limpa o modo de distribuição automática
    E a recusa de destino inválido não é apresentada
```
