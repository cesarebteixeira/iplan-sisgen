# US — E760C — Consultar cardápios do mês por órgão filho

## Estória

Como **servidor de CRE**, quero **consultar, para um órgão filho da minha
coordenadoria regional escolar, os cardápios de um mês, com o segmento, a
refeição, a descrição de cada cardápio e a quantidade já solicitada ao lado do
máximo previsto**, para que **eu saiba o que já foi pedido e o que ainda cabe
pedir em cada segmento e em cada refeição, sem abrir tela por tela**.

A alimentação escolar é programada por período: para cada órgão, segmento e
refeição existe um cardápio previsto, com a quantidade de cada cardápio que pode
ser servida no mês, e o que a escola pede vira solicitação. Sem uma visão que
junte as duas pontas — o previsto e o solicitado —, ninguém consegue dizer se o
mês já estourou ou se ainda sobra quantidade, e quem monta a distribuição
trabalha às cegas. Esta tela é só de leitura: não inclui, não altera e não
exclui cardápio nem solicitação; o previsto e o solicitado são mantidos nas
telas de manutenção.

## Contexto

Jornada S000M → E000M → E050M → E760C.

Ator: servidor de CRE — consulta, na sua coordenadoria regional escolar, o
cardápio previsto e o já solicitado de um órgão filho num mês.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e
menus.md`: é **dado de navegação**, não regra de negócio.

O `E000M` e o `E050M` são menus de opção: não gravam nada e apenas encaminham a
opção escolhida. O `E760C`, porém, não é aberto por menu: o `E050M` o chama
diretamente e, junto com a chamada, passa adiante a área de trabalho da sessão —
e é dessa área que o `E760C` tira a operação com que abre. O `E760C`, por sua
vez, também encadeia: ao fim do tratamento ele entrega à `E760T`, a tela de
manutenção do mesmo cardápio, o órgão filho, a coordenadoria, o segmento, a
refeição e o mês e o ano já conferidos, além da operação.

O contexto que a tela usa — tipo de órgão, coordenadoria e órgão filho do
servidor — é o que a entrada deixou na sessão. As regras abaixo são só as da
tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela só atende em consulta, e a operação vem de quem a chamou

A tela é de leitura e **não escolhe a operação sozinha**: ela recebe a operação
da tela que a chamou, pela área de trabalho da sessão, e só adota a consulta
quando não recebe operação nenhuma. Se a operação que chegar não for a consulta,
a tela recusa com **\* Operacao nao disponivel. Use CON \***, devolve o cursor ao
campo da operação e não lê cadastro nenhum.

[?] Quem pode entregar a esta tela uma operação diferente da consulta. Os menus
desta jornada zeram a operação na área de trabalho, e é por isso que, por esse
caminho, ela sempre abre em consulta; mas a tela não compara a tela de origem
com nenhum código de tela — ela confia na operação que a área de trabalho traz.
Se a tela de manutenção devolver o comando com a alteração ainda ligada, a
consulta é recusada; se o ambiente limpa a operação antes de cada chamada, esse
ramo nunca é alcançado. A recusa por operação, além disso, tem dois textos
diferentes — o da própria tela e o da rotina de rota que roda antes dela —, e o
acervo não diz qual deles o operador vê. Pergunta ao site.

### RN-02 — O órgão filho da sessão limita o que se pode consultar

Quando o vínculo do servidor aponta um órgão filho, a tela só deixa consultar
esse órgão: informando outro, a recusa é **\* Usuario sem acesso a outro orgao \***,
o cursor volta ao campo do órgão filho e nenhum cardápio é lido. Nesse caso o
campo já abre preenchido com o órgão do vínculo — e é repreenchido a cada
apresentação —, com o nome do órgão ao lado. Quem não tem órgão filho no vínculo
abre o campo em branco e pode consultar qualquer órgão da sua secretaria.

[?] De onde vem o órgão filho da sessão. A entrada o guarda na área da sessão e a
tela o lê da área de trabalho do módulo; nenhum caminho do acervo copia uma na
outra — as duas áreas são registros distintos, e as únicas escritas nos campos da
área de trabalho são limpezas. Se o ambiente não transportar o valor de uma para
a outra, o campo chega sempre zerado, todo servidor cai no ramo de quem não tem
órgão filho e a restrição deixa de valer. A mesma dúvida vale para o tipo de
órgão (RN-05) e para a coordenadoria (RN-06). Pergunta ao site.

### RN-03 — O órgão filho é obrigatório, e a mesma combinação não é reconferida

Mudando algum dos dados da consulta e vindo o órgão filho em branco, a recusa é
**\* Informe o orgao \***, com o cursor de volta ao campo do órgão filho, e nada
é lido. A conferência inteira — desta regra até a dos registros do mês — só é
refeita quando algum dos cinco dados informados (órgão filho, coordenadoria,
segmento, refeição e mês/ano) muda em relação à última combinação aceita;
repetida a mesma combinação, a tela passa direto, sem reconferir cadastro algum.

### RN-04 — O órgão filho tem de estar cadastrado

O órgão filho informado tem de existir no cadastro de órgãos. Não existindo, a
recusa é **\* Orgao nao cadastrado \***, com o cursor no campo do órgão filho, e
nenhum cardápio é lido.

### RN-05 — O órgão tem de ser de um tipo de órgão da secretaria do servidor

A tela compara o tipo de órgão do órgão filho informado com o tipo de órgão da
sessão. Não batendo — o que acontece quando se informa, por engano ou por
digitação, o órgão de outra rede —, a recusa é
**\* Orgao nao pertence a esta secretaria \***, com o cursor no campo do órgão
filho. Vale aqui a mesma dúvida da RN-02 sobre a origem do tipo de órgão da
sessão.

### RN-06 — O órgão tem de pertencer à coordenadoria do servidor

Quando o vínculo aponta uma coordenadoria regional escolar, o órgão filho
consultado tem de pertencer a ela: pertencendo a outra, a recusa é
**<- Usuario sem acesso ao grupo deste orgao \*** (o texto começa com a seta),
com o cursor no campo do órgão filho. Quem não tem coordenadoria no vínculo
consulta órgãos de qualquer coordenadoria da sua secretaria. Vale aqui a mesma
dúvida da RN-02 sobre a origem da coordenadoria da sessão.

### RN-07 — O segmento tem de estar cadastrado

O segmento informado tem de existir no cadastro de segmentos, para o tipo de
órgão da sessão: não existindo, a recusa é **\* Segmento nao cadastrado \***, com
o cursor no campo do segmento, e nenhum cardápio é listado. Existindo, a tela
mostra a descrição do segmento.

### RN-08 — A refeição tem de estar cadastrada

A refeição informada tem de existir no cadastro de refeições, para o tipo de
órgão da sessão: não existindo, a recusa é **\* Refeicao nao cadastrada \***, com
o cursor no campo da refeição. Existindo, a tela mostra a descrição da refeição.

### RN-09 — O mês e o ano do cardápio são obrigatórios

Faltando o mês ou o ano, a recusa é **\* Informe mes/ano \***, com o cursor no
campo do mês, e nenhum cardápio é listado.

### RN-10 — A consulta precisa de um período de cardápio para o mês pedido

Para o órgão, a coordenadoria, o segmento e a refeição informados, a tela procura
o período de cardápio do mês pedido — o período cujo início não é posterior ao
mês pedido e cuja data limite cai nesse mês. Não achando nenhum período com
quantidade prevista para o mês, a recusa é
**\* Nao existem registros para este mes/ano \***, com o cursor no campo do mês,
e a lista não é preenchida. Achando, o período encontrado fica guardado e é ele
que a lista usa.

[?] A leitura do período usa o recurso de posicionamento do dicionário de dados,
cujo efeito exato não está no acervo nem no manual. A tela confere o órgão, a
coordenadoria, o segmento e a refeição do registro lido, mas **não** reconfere a
data limite: se a leitura posiciona na primeira chave igual ou posterior à
pedida, o período aceito pode ser o de um mês seguinte ao informado, e a recusa
por falta de registros some para meses que só têm período adiante. O site precisa
dizer qual é o esperado. Pergunta ao site.

### RN-11 — A digitação é numérica, e o cursor volta ao campo recusado

O órgão filho, a coordenadoria, o segmento, a refeição, o código de cardápio e o
mês e o ano do cartão passam por edição numérica antes de qualquer leitura:
campo em branco vale zero e o que não for número é recusado, e a consulta não
segue. Quando a recusa cai no órgão filho, no segmento, na refeição, no mês ou no
ano do cartão, o cursor volta ao campo recusado.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual —
não está nos fontes desta jornada: a rotina que faz a edição numérica é importada
de uma biblioteca sem fonte no acervo, e a tela não emite mensagem nenhuma nesse
caminho.

[?] Dois campos editados, a coordenadoria e o código de cardápio, não têm posição
de cursor definida entre os campos de recusa: se a recusa cair em um deles, o
acervo não diz onde o cursor fica. Pergunta ao site.

### RN-12 — A lista junta o previsto e o solicitado, em até 14 linhas

A lista tem **14 linhas** e cada linha traz o **código do cardápio**, a
**descrição do cardápio**, a **quantidade solicitada** e a **quantidade máxima do
mês**. Ela junta as duas origens: primeiro os cardápios **previstos** no período
encontrado, com a quantidade máxima que o cadastro de períodos guarda para aquele
mês — cardápio com quantidade zero no mês não entra; depois, os cardápios que
aparecem nas **solicitações** do órgão naquele mês, que entram com a quantidade
solicitada contada, ou seja, o número de solicitações registradas para aquele
cardápio no mês. Um cardápio que esteja nas duas origens recebe as duas
quantidades; um que só foi solicitado aparece com o máximo zerado. Não havendo o
cardápio no cadastro de cardápios, a linha sai sem a descrição e sem aviso.
Acabando as duas origens, a listagem para e as linhas restantes ficam em branco.

[?] O mês informado não é conferido contra a faixa de 1 a 12. A escolha da
quantidade máxima do mês é uma cadeia de comparações que termina em "senão, é a
de dezembro", de modo que um mês fora da faixa — 13, por exemplo — leria a
quantidade de dezembro. Se a máscara já limita o campo, o ramo é inalcançável; se
não limita, é defeito. Pergunta ao site.

### RN-13 — A tela entrega a consulta à E760T

Ao fim do tratamento, a tela passa o serviço para a `E760T` — a tela de
manutenção do mesmo cardápio —, e não volta para menu nenhum. Ela entrega o
órgão filho, a coordenadoria, o segmento, a refeição e o mês e o ano já
conferidos, com as descrições de órgão, segmento e refeição, e a operação da
sessão, que é a consulta. É por isso que a `E760T` abre **em consulta**, e não em
alteração; para alterar, o operador muda a operação lá. A passagem só acontece
quando a última linha da lista já foi tratada e o campo de continuação que a
máscara mantém está preenchido.

[?] O que preenche esse campo de continuação. A tela nunca o escreve: ele só
chega da máscara, e nenhum caminho do programa o alimenta. Se a máscara não o
preencher, a passagem para a `E760T` não acontece por este caminho e o grafo de
navegação registra um destino que a tela sozinha não cumpre. Pergunta ao site.

### RN-14 — A consulta não grava nada e não deixa rastro de auditoria

A tela e as rotinas comuns que ela chama só leem: cadastro de órgãos, de
segmentos, de refeições, de períodos de cardápio, de cardápios, de cardápios
solicitados por órgão e o cadastro de telas. Nenhum registro é incluído, alterado
ou excluído, e nenhum registro de auditoria é gerado. As operações de gravação,
de exclusão e de travamento existem **declaradas** para os sete cadastros que a
tela enxerga, mas não são executadas em nenhum caminho: declarar não é executar.

### RN-15 — A abertura confere o acesso ao sistema e à tela

Cada abertura da tela passa por conferências de acesso com o contexto da sessão —
matrícula, código de acesso, privilégio, tipo de órgão e coordenadoria. A tela
precisa estar cadastrada: não estando, a recusa da abertura é
**\* Tela nao disponivel \***. A matrícula precisa ter a tela autorizada no seu
código de acesso: não tendo, a recusa é
**\* Acesso negado para esta matricula \***. Quando o operador envia a consulta, o
caminho passa ainda pela rotina de rota, que confere a operação e decide o
encaminhamento; é ela que responde **\* Tela nao cadastrada \*** quando a tela não
está no cadastro de telas.

[?] A mesma falta — tela não cadastrada — tem duas mensagens diferentes, porque
duas rotinas comuns conferem isso em momentos distintos: a da abertura e a da
rota, que roda quando o operador envia a consulta. Qual das duas o operador vê
depende do momento em que a falta é percebida. Pergunta ao site.

[?] A conferência de operação procura os sinalizadores de inclusão, de alteração
e de exclusão, mas **não** o de consulta: quem tem a tela autorizada consulta sem
precisar do sinalizador de consulta. Se a intenção era exigir esse sinalizador
por tela, o caminho não o exige. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar os cardápios de um mês para um órgão filho da coordenadoria regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E760C

  Cenário: Consulta dos cardápios do mês
    Dado que informei o órgão filho, a coordenadoria, o segmento, a refeição e o mês e o ano
    Quando envio a consulta
    Então vejo as linhas dos cardápios, com o código, a descrição, a quantidade solicitada e a quantidade máxima do mês
    E vejo o nome do órgão e as descrições do segmento e da refeição

  Cenário: A lista mostra no máximo 14 cardápios
    Dado que o órgão tem mais de 14 cardápios no mês
    Quando envio a consulta
    Então a lista mostra no máximo 14 linhas
    E as linhas restantes ficam em branco

  Cenário: A lista junta o previsto e o solicitado
    Dado que o período do mês prevê um cardápio que não foi solicitado
    E que há um cardápio solicitado que o período não prevê
    Quando envio a consulta
    Então os dois aparecem na lista
    E o previsto mostra a quantidade máxima do mês
    E o solicitado mostra a quantidade solicitada contada no mês

  Cenário: O órgão filho da sessão já vem preenchido
    Dado que o meu vínculo aponta um órgão filho
    Quando abro a tela E760C
    Então o campo do órgão filho já vem preenchido com esse órgão
    E vejo o nome do órgão

  Cenário: Operação diferente da consulta
    Dado que a tela recebe uma operação diferente da consulta
    Quando envio a consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nenhum cadastro é lido nesse caminho

  Cenário: Órgão filho fora do meu acesso
    Dado que o meu vínculo aponta um órgão filho
    Quando informo outro órgão filho
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E o cursor volta ao campo do órgão filho
    E nenhum cardápio é listado

  Cenário: Órgão filho em branco
    Dado que mudei algum dos dados da consulta
    E deixei o órgão filho em branco
    Quando envio a consulta
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor volta ao campo do órgão filho

  Cenário: Órgão filho que não existe
    Dado que informo um órgão filho que não está no cadastro de órgãos
    Quando envio a consulta
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão filho

  Cenário: Órgão de outro tipo de órgão
    Dado que informo um órgão filho de um tipo de órgão diferente do da minha sessão
    Quando envio a consulta
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E o cursor volta ao campo do órgão filho

  Cenário: Órgão de outra coordenadoria
    Dado que o meu vínculo aponta uma coordenadoria
    E informo um órgão filho de outra coordenadoria
    Quando envio a consulta
    Então vejo a mensagem "<- Usuario sem acesso ao grupo deste orgao *"
    E o cursor volta ao campo do órgão filho

  Cenário: Segmento que não existe
    Dado que informo um segmento que não está no cadastro de segmentos
    Quando envio a consulta
    Então vejo a mensagem "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento
    E nenhum cardápio é listado

  Cenário: Refeição que não existe
    Dado que informo uma refeição que não está no cadastro de refeições
    Quando envio a consulta
    Então vejo a mensagem "* Refeicao nao cadastrada *"
    E o cursor volta ao campo da refeição

  Cenário: Mês ou ano em branco
    Dado que deixei o mês ou o ano em branco
    Quando envio a consulta
    Então vejo a mensagem "* Informe mes/ano *"
    E o cursor volta ao campo do mês

  Cenário: Sem período de cardápio para o mês
    Dado que não há período de cardápio com quantidade prevista para o mês informado
    Quando envio a consulta
    Então vejo a mensagem "* Nao existem registros para este mes/ano *"
    E o cursor volta ao campo do mês
    E nenhuma linha da lista é preenchida

  Cenário: Digitação não numérica
    Dado que digito algo que não é número no órgão filho, no segmento, na refeição ou no mês ou no ano
    Quando envio a consulta
    Então o sistema recusa a digitação antes de ler qualquer cadastro
    E o cursor volta ao campo recusado

  Cenário: A consulta passa para a E760T
    Dado que a consulta foi aceita
    Quando o tratamento da última linha termina
    Então a E760T abre com o órgão filho, a coordenadoria, o segmento, a refeição e o mês e o ano que eu conferi
    E a E760T abre em consulta

  Cenário: A consulta não grava nada
    Dado que abro a tela E760C
    Quando a lista é mostrada
    Então nenhum órgão, segmento, refeição, período, cardápio ou solicitação é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Tela não cadastrada
    Dado que a tela E760C não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo consultar

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela E760C autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo consultar
```
