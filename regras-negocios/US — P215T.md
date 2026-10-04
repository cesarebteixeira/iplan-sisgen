# US — P215T — Consultar processo pelo número

## Estória

Como **servidor de CRE**, quero **informar o número de um processo e ver o que o
sistema tem registrado dele — em que empenho e ano ele corre, o fornecedor, o tipo do
processo, as datas e as ordens do pré-empenho, da liquidação e do pagamento, os
valores e a diferença entre eles —**, para que **eu responda a uma escola, a um
fornecedor ou a um órgão de controle sem abrir os cadastros um a um nem pedir a
informação a outro setor**.

O processo é o lançamento que corre contra um empenho autorizado, e o número dele é o
que a regional tem em mãos quando alguém pergunta "e o processo tal?". Esta é a tela
em que esse número vira resposta; e ela é também uma das portas da ficha, porque a
lista de processos a chama já com um processo escolhido. Sem ela, quem tem o número só
descobre o que existe nele pedindo a outra pessoa que abra o cadastro.

A tela é só de leitura: não inclui, não altera e não exclui processo, empenho nem
fornecedor — quem os mantém são outras telas. E ela recusa em vez de responder pela
metade: quando não há processo com o número, quando a nota fiscal dele já está fechada
e quando a operação pedida não é a de consulta.

## Contexto

Jornada S000M → P000M → P215T.

Ator: servidor de CRE — informa o número do processo e vê o que o sistema tem
registrado dele: em que empenho e ano ele corre, o fornecedor, o tipo e a descrição do
tipo do processo, as datas e as ordens do pré-empenho, da liquidação e do pagamento, os
valores e a diferença.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O menu do módulo só encaminha: não procura processo, não informa operação e não deixa
dado de negócio para esta tela. O que esta tela toma das telas anteriores é o que a
entrada deixou na sessão — o **tipo de órgão**, a **CRE do vínculo** e a **data do
sistema** — e o que ela relê do **cadastro de tipos de órgão** da sessão. Por isso não
há regra de negócio do menu nesta jornada.

A tela tem uma segunda porta, e essa é regra de negócio, não navegação: a **lista de
processos (`N105T`)** passa para ela o processo que o servidor escolheu, tela a tela,
sem passar por menu nenhum — e é por isso que ela pode abrir já com a ficha montada
(RN-02). Esta tela, por sua vez, **não encadeia em outra**: ela não indica tela de
destino e deixa na área de trabalho da sessão o que a sua própria abertura seguinte
consome (RN-03).

## Regras de negócio

### RN-01 — A tela é de consulta: qualquer outra operação é recusada

A tela é de consulta, e só. Toda vez que ela se monta, ela mesma repõe a consulta na
opção de manutenção; se o operador informar uma opção diferente da consulta, o sistema
recusa com **\* Opcao invalida. Use CON \***, devolve o cursor ao campo da opção e não
lê nem grava nada.

[?] A mensagem manda usar a consulta pela sigla **CON**, e o valor que a tela compara
nesse campo não está no acervo lido: ele vem da tabela de mensagens do sistema. Se quem
digita "CON" é aceito, é pergunta ao site.

### RN-02 — A ficha do processo só é carregada quando a tela foi chamada pela lista de processos

Ao abrir, a tela olha a marca que o programa que a chamou deixou na área de trabalho da
sessão. Quando a marca é a da **lista de processos (`N105T`)** — que a chama com um
processo escolhido, o tipo do número auxiliar e o número auxiliar —, a tela decompõe o
número recebido nas suas partes, monta o número SEI ou o número RIO conforme o tipo
recebido, lê os cadastros e **mostra a ficha daquele processo** (RN-09). Quando a marca
não é essa — como quando a tela é aberta pela opção do menu, que não deixa marca
nenhuma —, a tela **não carrega ficha nenhuma**: abre com as partes do número que ela
mesma propõe (RN-04) e com o resto em branco, à espera de que o operador informe o
número.

A marca da origem é **consumida** ao fim do carregamento, para não valer numa abertura
seguinte. E é essa mesma marca que a própria tela deixa na área de trabalho quando o
operador confirma um número (RN-03): assim, a abertura que vem depois da confirmação
carrega a ficha do processo que acabou de ser resolvido.

[?] O que decide que a tela é reaberta depois de uma confirmação — o motor que, ao fim
da transação, reexecuta a tela — não está no acervo lido. O fonte mostra a tela
deixando a área de trabalho marcada com a lista de processos e com o processo
resolvido, que é exatamente a condição do carregamento; sem esse motor não se prova que
ela reabre sozinha, e se ela não reabrir o operador fica com o número quebrado em
partes na tela e sem a ficha. Pergunta ao site.

### RN-03 — O que a tela deixa para a abertura seguinte

A tela não pede passagem para nenhuma outra: ela não indica tela de destino. Ao
confirmar um número que passou por todas as conferências, ela deixa na área de trabalho
da sessão: a **operação de consulta**, a **marca da lista de processos**, o **número do
processo resolvido**, a **parte de seis dígitos do número**, o **tipo do número
auxiliar** (SEI ou RIO) e o **número auxiliar** correspondente — o SEI com a sua
segunda parte, ou o RIO com a sua quarta parte. Não entrega o empenho, o ano, os
valores nem os dados do fornecedor: quem os mostra é o carregamento da abertura
seguinte (RN-02).

Como a mesma marca também diz "o número informado é este", quando a tela reabre com o
processo que ela mesma resolveu, ela **não relê** o cadastro de notas fiscais para o
número igual ao que recebeu.

### RN-04 — Ao abrir, a tela propõe as partes do número e o que a sessão conhece do tipo de órgão

Ao ser aberta, a tela preenche, no número do processo, o **código da secretaria** que o
cadastro de tipos de órgão guarda para o **tipo de órgão da sessão** e a **CRE do
vínculo do servidor**; no número RIO, os **dois prefixos** desse mesmo tipo de órgão e
o **ano do sistema**; e, no número SEI, o **ano do sistema**. Fora dos números, mostra a
**data do sistema** e o **nome do tipo de órgão** da sessão. Quando o vínculo não tem
CRE, a parte da CRE fica em branco e é o operador quem a informa.

A CRE do vínculo é **proposta**, não imposta: a tela não confere se a CRE do processo é
a do servidor e o operador pode trocá-la no campo. O tipo de órgão da sessão serve para
achar a secretaria, os prefixos do número RIO e o tipo do processo (RN-10).

[?] Pelas regras da entrada, o vínculo limita o que as telas seguintes deixam
consultar; esta tela não usa a CRE para limitar nada. Se um servidor de uma CRE pode
consultar, pelo número, o processo de outra, é pergunta ao site.

### RN-05 — O número do processo é mostrado e recebido em quatro partes

O número do processo tem **quatorze dígitos** e a tela o trata em **quatro partes**: a
do **código da secretaria** (2 dígitos), a da **CRE** (2), a do **lote** (6) e a
**última** (4). O que o operador informa é a junção dessas quatro partes, na ordem em
que aparecem. O número **SEI** é tratado em quatro partes de 6, 6, 4 e 2 caracteres, e
o número **RIO** em quatro partes de 3, 3, 4 e 6.

[?] Para decompor um número que chega pronto, a tela tem **dois** caminhos: quando as
duas primeiras posições do número vêm preenchidas, ela mostra as quatro partes; quando
vêm zeradas, ela desloca as partes — mostra a segunda metade da primeira dupla como
primeira parte visível e deixa a parte da CRE em branco. Se o acervo guarda processos
nos dois formatos, ou se um deles é resto de carga antiga, é pergunta ao site.

### RN-06 — A existência do processo é conferida no cadastro de notas fiscais

O processo informado é procurado no **cadastro de notas fiscais**; é lá que a tela
atesta que ele existe. Não achando, recusa com **\* Processo nao cadastrado \***, com o
cursor de volta ao campo do número do processo, e nada mais é lido. Essa procura é
feita pelo número do processo quando ele foi informado, e é ela que decide: se o número
do processo não for achado, a tela não cai para o número SEI nem para o número RIO.

[?] A tela atesta a existência no cadastro de notas fiscais, mas lê os dados do
processo no **cadastro de processos** sem recusar quando não o acha ali: se um processo
tiver nota fiscal e não tiver registro no cadastro de processos, a tela não avisa —
mostra o bloco de valores com o que conseguiu, e sem recusa. Se esse caso é possível, e
o que o operador deveria ver, é pergunta ao site.

### RN-07 — O número SEI e o número RIO têm as suas próprias recusas

Informado o número SEI e não achado o processo, a recusa é **\* SEI nao cadastrado \***,
com o cursor de volta ao campo do SEI. Informado o número RIO e não achado, a recusa é
**\* PROCESSO RIO nao cadastrado \***, com o cursor de volta ao campo do RIO. Achado o
número auxiliar, é dele que sai o número do processo.

O número SEI e o número RIO entram na conferência **depois** do número do processo:
quando os dois caminhos resolvem, prevalece o número auxiliar, o SEI antes do RIO. Com
os números auxiliares em branco, nada é conferido por eles.

[?] A tela procura o número RIO na **mesma chave com que procura o número SEI** — o
campo em que o cadastro de notas fiscais guarda o número SEI/RIO —, embora o cadastro
tenha uma chave própria pelo número RIO. As telas irmãs fazem a mesma troca ao passar o
número adiante. Se os processos com numeração RIO ficam guardados no campo próprio, a
tela os recusa como não cadastrados. Pergunta ao site.

### RN-08 — O processo com a nota fiscal fechada é recusado como não pré-liquidado

Quando a **situação da nota fiscal** do processo é a de **fechada**, a tela recusa com
**\* Processo nao esta pre-liquidado \***, com o cursor de volta ao campo do número do
processo, e não mostra a ficha.

[?] A tela recusa a situação **fechada** e deixa passar **qualquer outra** — inclusive
uma situação em branco ou que o acervo não nomeia; as telas irmãs do mesmo assunto
fazem o inverso: nelas o processo só segue quando a situação **não** é a de fechada, e
a de fechada é que as leva a dizer "FECHADO". Se o cadastro tem outras situações além
de "fechada" e de "aberta/pré-liquidada", esta tela as trata como pré-liquidado.
Pergunta ao site; não se escolhe um dos dois lados.

### RN-09 — A tela mostra o que os cadastros guardam do processo

Achado o processo, a tela mostra: o **número do empenho** e o **ano de referência**; o
**dia, o mês e o ano do processo**; o **código da fonte**; o **código do fornecedor** e a
**razão social** dele; o **tipo do processo** com o seu rótulo e a **descrição** desse
tipo; o **trabalho**, a **despesa** e o **órgão financeiro**; a **data de
pré-liquidação** com a **ordem de pré-empenho** e o **valor do processo**; o **valor do
processo**, o **valor a ele vinculado** e a **diferença** entre os dois.

[?] O bloco da data de pré-liquidação não tem rótulo nos fontes desta jornada: os
outros dois blocos trazem os seus rótulos escritos no próprio programa ("Liquidacao" e
"Pagamento"), e esse não. Se o site usa outro nome para ele, é pergunta ao site.

### RN-10 — O tipo do processo e a sua descrição são procurados no tipo de órgão da sessão

O **tipo do processo** é procurado pelo **tipo de órgão da sessão** junto com o número
do processo; a **descrição** do tipo, pelo tipo de órgão junto com o próprio tipo.
Processo de outro tipo de órgão aparece sem tipo e sem descrição, e o bloco do tipo não
é montado.

### RN-11 — Os blocos da liquidação e do pagamento só aparecem quando o processo tem essas datas

A tela só monta o bloco sob o rótulo **"Liquidacao"** quando o processo tem **data de
liquidação**, e o bloco sob o rótulo **"Pagamento"** quando tem **data de pagamento**.
Sem a data, o bloco não é montado — e o rótulo dele também não aparece. Cada bloco traz
a sua data, a ordem de pagamento e um valor.

[?] O cadastro do processo guarda **dois** valores ligados à liquidação e ao pagamento e
a tela usa o **mesmo** nos dois blocos; o outro valor não aparece em campo nenhum desta
tela. Se o bloco da liquidação deveria trazer o outro valor, é pergunta ao site.

### RN-12 — Os campos digitados que não são o número não mudam a consulta

O **número do empenho**, o **ano de referência**, o **dia, o mês e o ano do processo**,
o **código da fonte**, o **tipo do processo**, o **código do fornecedor**, o
**trabalho**, a **despesa**, o **órgão financeiro** e os **valores** podem ser
digitados, mas não participam da consulta: antes de montar a tela, o sistema os
substitui pelo que os cadastros guardam para o processo achado. Quem decide o resultado
é o número do processo (e, na falta dele, o número auxiliar).

### RN-13 — O indicador de empenho muda conforme a tela por que o processo passou

Cada **registro do processo** guarda, no seu próprio cadastro, o **código da tela por
onde o processo passou**. Ao ler o processo, a tela procura entre os seus registros de
empenho o primeiro que tenha **número de empenho preenchido** e, quando o código desse
registro é o da **tela P212T**, deixa na área de trabalho da sessão o **indicador de
empenho** marcado como "S"; nos outros casos o indicador fica **como estava** — em
branco, quando a tela veio da lista de processos.

Quem escreve esse código é a tela que mantém o registro do processo; nesta jornada ele
é **lido**, não escrito.

[?] O indicador que a tela deixa marcado não é lido por nenhuma tela do acervo lido —
nem por esta, nem pelas irmãs, que apenas o repõem em branco. O que ele decide, e para
quem, não está no acervo: ou o consumidor ficou fora do lote, ou o campo é resto de uma
versão anterior. Pergunta ao site.

### RN-14 — Os campos digitados passam pela edição numérica antes da consulta

Os **vinte e quatro** campos digitáveis passam pela edição numérica antes da consulta.
Em **treze** deles a tela trata o campo em branco como zero antes de editar; o que não
for número é recusado, o cursor volta ao primeiro campo recusado e a consulta não é
feita.

[?] Só **nove** desses campos — as partes dos números do processo, do SEI e do RIO —
têm posição de cursor declarada; nos outros, a recusa devolve o cursor à posição padrão
da máscara, que é a do número do processo. Se é isso que o site espera, é pergunta ao
site.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não
está nos fontes desta jornada: a rotina que faz a edição não faz parte do acervo lido.

### RN-15 — Cada consulta começa com os campos de resultado limpos

Antes de conferir qualquer coisa, a tela apaga o que a consulta anterior havia
mostrado: o tipo de órgão, a data do sistema, o título e a descrição do tipo do
processo, a razão social do fornecedor e, de cada um dos três blocos, o título, a data,
a ordem e o valor. Uma consulta recusada, portanto, não deixa na tela o resultado da
consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe um
caminho de entrada em que os campos não são limpos, é pergunta ao site.

### RN-16 — A consulta não grava nada

A tela e as conferências que ela chama só **leem** cadastros — o de telas, o de tipos de
órgão, o de processos, o de fornecedores, o que diz o tipo de cada processo, o que
descreve cada tipo de processo e o de notas fiscais. Nenhum registro é incluído,
alterado ou excluído, nenhum registro é reservado para alteração e nada é gerado para
auditoria.

## Cenários BDD

```gherkin
Funcionalidade: Consultar processo pelo número

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela P215T

  Cenário: Consulta de um processo que existe
    Dado que existe um processo com o número que vou informar
    Quando informo o número do processo e confirmo a consulta
    Então vejo o número do empenho e o ano de referência do processo
    E vejo o dia, o mês e o ano do processo, o código da fonte e o tipo do processo
    E vejo a razão social do fornecedor, o trabalho, a despesa e o órgão financeiro
    E vejo a data de pré-liquidação com a ordem de pré-empenho e o valor do processo
    E vejo o valor do processo, o valor a ele vinculado e a diferença entre os dois

  Cenário: Abertura pelo menu
    Dado que abro a tela P215T pela opção do menu do módulo
    Então o número do processo vem com o código da secretaria do meu tipo de órgão
    E vem com a CRE do meu vínculo
    E o número SEI e o número RIO vêm com o ano do sistema
    E o número RIO vem com os prefixos do meu tipo de órgão
    E vejo a data do sistema e o nome do tipo de órgão
    E nenhuma ficha de processo é carregada

  Cenário: Abertura pela lista de processos
    Dado que escolhi um processo na lista de processos
    Quando a tela P215T abre
    Então a ficha do processo escolhido já está montada
    E o número aparece nas suas quatro partes
    E não preciso digitar o número

  Cenário: Abertura com o vínculo sem CRE
    Dado que o meu vínculo não tem CRE
    Quando abro a tela P215T
    Então a parte da CRE fica em branco e eu a informo

  Cenário: Consulta pelo número SEI
    Dado que o processo tem numeração SEI
    Quando informo o número SEI e confirmo a consulta
    Então vejo a ficha do processo
    E o número do processo vem do número SEI

  Cenário: Consulta pelo número RIO
    Dado que o processo tem numeração RIO
    Quando informo o número RIO e confirmo a consulta
    Então vejo a ficha do processo
    E o número do processo vem do número RIO

  Cenário: Processo que não existe
    Dado que não existe processo com o número que vou informar
    Quando confirmo a consulta
    Então vejo a mensagem "* Processo nao cadastrado *"
    E o cursor volta ao campo do número do processo
    E a ficha não é mostrada

  Cenário: Número SEI que não existe
    Dado que informo um número SEI que não está em nenhuma nota fiscal
    Quando confirmo a consulta
    Então vejo a mensagem "* SEI nao cadastrado *"
    E o cursor volta ao campo do número SEI
    E a ficha não é mostrada

  Cenário: Número RIO que não existe
    Dado que informo um número RIO que não é achado pelo cadastro
    Quando confirmo a consulta
    Então vejo a mensagem "* PROCESSO RIO nao cadastrado *"
    E o cursor volta ao campo do número RIO
    E a ficha não é mostrada

  Cenário: Nota fiscal fechada
    Dado que a situação da nota fiscal do processo é a de fechada
    Quando confirmo a consulta
    Então vejo a mensagem "* Processo nao esta pre-liquidado *"
    E o cursor volta ao campo do número do processo
    E a ficha não é mostrada

  Cenário: Número do processo informado que não existe não cai para o SEI
    Dado que informo um número de processo que não está em nenhuma nota fiscal
    E informo também um número SEI que existe
    Quando confirmo a consulta
    Então vejo a mensagem "* Processo nao cadastrado *"
    E o número SEI não é procurado

  Cenário: Confirmação sem informar número nenhum
    Dado que abri a tela pela opção do menu e não informei número de processo
    Quando confirmo a consulta
    Então o número que a tela montou com o que ela propôs não existe no cadastro
    E vejo a mensagem "* Processo nao cadastrado *"

  Cenário: Operação diferente de consulta
    Dado que estou na tela P215T
    Quando informo uma opção de manutenção diferente da consulta
    Então vejo a mensagem "* Opcao invalida. Use CON *"
    E o cursor volta ao campo da opção
    E nada é consultado nem gravado

  Cenário: Processo sem liquidação e sem pagamento
    Dado que o processo existe e não tem data de liquidação nem de pagamento
    Quando confirmo a consulta
    Então vejo a ficha do processo e o bloco do pré-empenho
    E não vejo o bloco da liquidação
    E não vejo o bloco do pagamento

  Cenário: O que digito fora dos números não muda o resultado
    Dado que existe um processo com o número que vou informar
    Quando digito outro empenho, outro ano, outra fonte e outros valores
    E confirmo a consulta
    Então vejo o empenho, o ano, a fonte e os valores do processo achado
    E não os que digitei

  Cenário: Processo de outro tipo de órgão
    Dado que o processo é de um tipo de órgão diferente do da minha sessão
    Quando confirmo a consulta
    Então vejo os dados do processo que não dependem do tipo de órgão
    E o bloco do tipo do processo não aparece

  Cenário: Campo digitado que não é número
    Dado que digito, num dos campos do processo, algo que não é número
    Quando confirmo a consulta
    Então o cursor volta ao primeiro campo recusado
    E a consulta não é feita

  Cenário: Nova consulta começa com os resultados limpos
    Dado que já mostrei a ficha de uma consulta anterior
    Quando peço uma nova consulta
    Então a ficha da consulta anterior não fica na tela
    E só aparecem os resultados da consulta que passou pelas conferências

  Cenário: O que a tela deixa para a abertura seguinte
    Dado que informei um número de processo que existe
    Quando confirmo a consulta
    Então a operação de consulta fica na área de trabalho da sessão
    E com ela ficam a marca da lista de processos e o número do processo resolvido
    E a ficha do processo é carregada na abertura seguinte

  Cenário: O processo cujo registro veio da tela P212T
    Dado que o registro de empenho do processo é o da tela P212T
    Quando confirmo a consulta
    Então a tela deixa o indicador de empenho marcado como "S" na área de trabalho
    E nenhuma tela do sistema mostra esse indicador

  Cenário: A consulta não grava nada
    Dado que existe o processo informado
    Quando consulto o processo
    Então nenhum cadastro é incluído, alterado ou excluído
    E nenhum registro é reservado para alteração
    E nada é gerado para auditoria
```
