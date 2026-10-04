# US — C845T — Consultar a estimativa da alimentação escolar do grupo no período, excluir o cálculo do período e pedir a impressão da relação

## Estória

Como **servidor de CRE**, quero **conferir a estimativa da alimentação escolar que está
calculada para o meu grupo em cada período, apagar o cálculo de um período inteiro e pedir a
impressão da relação**, para que **um período calculado com o cardápio, os preços ou as
quantidades erradas possa ser desfeito e refeito, e para que a coordenação possa conferir em
papel o que ficou calculado antes de isso virar cardápio oficial e planejamento**.

A estimativa da alimentação escolar é apurada período a período — cada período vale de uma
data de início até uma data limite —, e é o cálculo do período que alimenta o cardápio
oficial e o planejamento da alimentação. Depois de calculado, o período não se corrige por
esta tela: ou ele está certo, ou o cálculo inteiro se apaga para ser refeito. Sem isso, um
período fechado com dados errados ficaria preso, e a conferência do que foi calculado não
teria por onde começar.

## Contexto

Jornada S000M → C000M → C800M → C840M → C845T.

Ator: servidor de CRE — confere a estimativa calculada do seu grupo no período, apaga o
cálculo do período inteiro e pede a impressão da relação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os três menus do caminho — `C000M`, `C800M` e `C840M` —
só encaminham e não gravam nada; o último é quem oferece a tela.

O contexto de que a C845T se serve — a matrícula, o tipo de órgão, o privilégio, a estação e
a data e a hora da sessão — é o que a entrada deixou na sessão; a tela não recalcula nada
disso. É o **tipo de órgão da sessão** que entra na chave do cadastro de grupos e de todos os
registros do cálculo, e é ele que limita o que a tela alcança.

A C845T **encadeia** para a C846T, a consulta do gênero: marcada uma linha da grade, ela
entrega à tela seguinte o gênero e o período e faz a tela seguinte abrir em consulta
(RN-12). A volta da C846T deixa de novo o gênero escolhido na sessão, e a C845T reabre com o
período consultado.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela abre em consulta, e só consulta e alteração passam

A cada apresentação, a tela repõe a **opção** como consulta, a **marca de exclusão** como N
e a **impressora** em branco: o que estiver nesses campos é descartado. Passam só a consulta
e a alteração; qualquer outra opção é recusada com **\* Operacao nao disponivel. Use ALT ou
CON \***, com o cursor de volta ao campo da opção e sem ler cadastro nenhum. Nesta tela a
alteração **não altera nada**: ela não grava nem muda o cálculo — é apenas a chave que
libera a exclusão (RN-09).

[?] A recusa manda usar ALT e CON, mas o que a tela aceita é o código interno da consulta e
o da alteração, que não são esses textos; nada no material lido diz que o terminal traduz o
mnemônico antes de enviar. Ou o formulário traduz, ou quem seguir a mensagem é recusado.
Pergunta ao site.

### RN-02 — A estimativa é a de um grupo num período, e a grade mostra os gêneros que a compõem

Quem opera informa o **grupo** (a coordenação regional escolar) e o **período**: as três
partes do início (dia, mês e ano) e as três do limite (dia, mês e ano). O período é
identificado pelo **limite**. A consulta mostra, no cabeçalho, a situação do período (aberto
ou fechado), a descrição do tipo de órgão da sessão e a data do sistema e, na **grade de 14
linhas**, cada gênero do cálculo com **8 valores**: o código da subclasse, o código do
gênero, a descrição do gênero, a marca do indicador da linha, a quantidade de saldo inicial,
o valor inicial, o preço e a marca da linha. Fora da grade a tela tem **18 campos**, entre
eles a opção, a coordenação, as seis partes das duas datas, a impressora e a marca de
exclusão, além de **dois campos auxiliares sem rótulo**.

[?] A grade comporta 14 gêneros e o caminho lido monta uma passada só: havendo mais gêneros
num período, não há paginação nesta tela. Se o período puder ter mais de 14, pergunta ao
site como o restante é alcançado.

### RN-03 — O início do período mostrado vem do cálculo, não do que foi digitado

O dia, o mês e o ano de início são conferidos como número, mas a tela os **repõe** com os do
cálculo do grupo para aquele período: o que for digitado no início é substituído. Quem
identifica o período é o limite.

[?] O início tem campo na tela e passa pela edição numérica, mas nenhuma leitura o usa —
todas as leituras identificam o período pelo limite, e o início exibido vem do cálculo do
grupo. Se o campo serve para conferência de quem opera, o fonte não diz. Pergunta ao site.

### RN-04 — A consulta exige o grupo cadastrado

O grupo informado tem de existir no cadastro de grupos **dentro do tipo de órgão da
sessão**. Não existindo, a recusa é **\* Grupo nao cadastrado \***, com o cursor de volta ao
campo da coordenação, e nada mais é lido.

[?] A tela não compara a coordenação informada com a coordenação do vínculo de quem opera: o
que limita o alcance é a lógica de rota e de segurança da tela, que não está no acervo
lido. Se um servidor de uma coordenação pode consultar e apagar a estimativa de outra, o
fonte desta tela não responde. Pergunta ao site.

### RN-05 — A consulta exige o cálculo do período no calendário do grupo

A tela procura o cálculo do grupo para aquele período. Não achando, recusa com **\* Grupo
sem estimativa para esta data \***, com o cursor de volta ao dia do limite, e não preenche
nada. **Quando o dia do limite não é informado**, a tela adota o período já registrado para o
grupo e passa a mostrá-lo no lugar do limite em branco. Achado o período, a grade exige ainda
o cálculo dos gêneros: não havendo nenhum gênero calculado naquele período, a recusa é
**\* Grupo sem calculo de estimativa cadastrado \*** e linha nenhuma é preenchida.

[?] A procura do período adotado é feita pelo ano **9999** no cadastro do calendário do
grupo. O que o ano 9999 significa nesse cadastro — período em vigor, último período, período
padrão — não está no material lido. Pergunta ao site.

### RN-06 — A descrição de cada gênero vem do cadastro de gêneros

A descrição mostrada em cada linha é lida do cadastro de gêneros, e só é usada quando o
gênero está **ativo**; o código da subclasse e o do gênero são os que identificam a linha.
Quando a subclasse é **99**, a descrição vem de outro cadastro — o dos gêneros por
composição — e a linha recebe uma **marca** ao lado da descrição.

[?] O que significa a subclasse 99, e o que a marca da linha indica a quem opera, não está no
material lido. Pergunta ao site.

[?] A descrição da linha **não é limpa** quando o gênero não é achado no cadastro ou não
está ativo: nesses casos a linha fica com a descrição que estava na linha anterior. Se o
esperado é a linha sair sem descrição, o caminho não limpa. Pergunta ao site.

[?] A versão do gênero é procurada pela **data limite** do período, e a conferência seguinte
não compara as datas — só o par subclasse e gênero. Se a descrição mostrada deveria ser a da
versão vigente no período, o fonte não permite concluir: o posicionamento do banco é
importado e não está no acervo lido. Pergunta ao site.

### RN-07 — Período fechado aparece marcado, e não se apaga

Quando o cálculo do grupo para o período está **fechado**, a tela o mostra com a marca
**FECHADO** no lugar do tracejado; aberto, mostra o tracejado. E a exclusão de um período
fechado é recusada com **\* Cadastro fechado para este periodo \***, com o cursor na marca de
exclusão — nada é apagado.

[?] A situação do período é lida de **um único registro** do cálculo do grupo (a leitura
posiciona-se pelo grupo e pelo período e não confere o gênero). Se os gêneros de um mesmo
período puderem ter situações diferentes, a tela mostra e recusa por uma delas. Pergunta ao
site.

### RN-08 — A impressão da relação é pedida preenchendo a impressora

Informada a **impressora**, a tela registra o pedido da relação da estimativa do grupo
naquele período — com o número seguinte da fila de pedidos, a impressora, a estação, a
matrícula e a data — e entrega o processamento à fila. O pedido pode ser feito em consulta ou
em alteração. Se já houver um pedido da mesma relação para o mesmo grupo na fila, o pedido
novo é recusado com **\* Relatorio em processamento. Aguarde. \***, com o cursor na
coordenação, e nada é registrado.

[?] O processamento só é entregue à fila quando o produto em execução é o LINC; fora dele o
pedido fica registrado e o caminho lido não mostra o disparo. Pergunta ao site.

### RN-09 — Excluir exige a opção ALT e a marca de exclusão

A exclusão do cálculo é pedida pela **marca de exclusão** (S) junto com a opção
**alteração**. Marcada a exclusão com a opção em consulta, a recusa é **\* Use ALT para
exclusão do cadastro \***, com o cursor na opção, e nada é apagado. Marca diferente de S não
exclui: a tela segue como consulta comum.

### RN-10 — Excluir e imprimir exigem ter consultado o mesmo grupo e período antes

As duas operações que agem sobre o período só passam quando a coordenação e o limite
informados são **os mesmos da última consulta da sessão**. Não sendo, a exclusão é recusada
com **\* Consulte a estimativa antes de excluir \*** e a impressão com **\* Consulte a
estimativa antes de imprimir \***, nos dois casos com o cursor na coordenação e sem apagar
nem registrar nada.

### RN-11 — A exclusão apaga o cálculo do período inteiro e deixa rastro na auditoria

Passando as guardas, a tela apaga, do período, **todos os registros que dependem dele** — os
valores por gênero, as quantidades por refeição e segmento, as quantidades por cardápio e os
ajustes com motivo — e, por fim, o registro do período no calendário do grupo. Antes disso
monta um lançamento na **auditoria** com a tela de origem, a operação de exclusão, o grupo, a
matrícula, a estação, a data e a hora e o registro do período apagado. A exclusão **não pede
confirmação** e não olha outro cadastro antes de apagar. Pedidas juntas a exclusão e a
impressão, as guardas das duas são conferidas, a exclusão prevalece e a impressão não chega
a ser pedida.

[?] A exclusão por esta tela é imediata e não pede confirmação. A tela C885T — outra tela do
módulo, que trata dos cadastros de estimativa do mesmo período — pede confirmação e não apaga
nada por si: registra o pedido e entrega o processamento, e é o processamento que apaga. Se a
exclusão do cálculo do período deveria ser confirmada, ou entregue a um processamento, o
material lido não diz. Pergunta ao site.

### RN-12 — A linha marcada leva à consulta do gênero na C846T

Marcada uma linha com **X**, a tela entrega à **C846T** — a consulta do gênero — o grupo, o
gênero (subclasse e código), o período com as duas datas, a quantidade, o valor, o preço e a
situação, e **repõe a operação como consulta** na sessão: a tela seguinte abre em consulta
por causa disso. A linha marcada precisa ter cálculo no período; não tendo, a transação
termina sem mensagem e nada é entregue. Linha sem marca, ou com marca diferente de X, não
leva a lugar nenhum.

### RN-13 — A consulta não grava nada

Na consulta a tela só lê: monta o cabeçalho e a grade a partir do cálculo do grupo e do
cadastro de gêneros, e nenhum registro é incluído, alterado ou apagado — nem lançamento de
auditoria. As rotinas de gravação e de exclusão existem **declaradas** para os **doze**
cadastros que a tela enxerga — **24 parágrafos** —, mas a tela executa **sete**: duas
gravações (o lançamento de auditoria da exclusão e o pedido da relação) e cinco exclusões (as
quatro famílias de registros do período e o registro do período). Declarar não é executar.

### RN-14 — A digitação passa pela edição numérica e o cursor volta ao campo recusado

**Onze** campos da tela passam pela edição numérica antes de qualquer leitura: a
coordenação, as três partes do início, as três do limite, o código da subclasse, o código do
gênero e os **dois campos auxiliares** sem rótulo. Campo em branco vale zero; o que não for
número é recusado, a passagem não segue e o cursor volta ao campo recusado.

[?] A edição numérica é feita por uma rotina importada, declarada no runtime só como entrada:
o que quem opera vê quando a digitação é recusada — se há mensagem, e qual — não está nos
fontes desta jornada. Pergunta ao site.

### RN-15 — Falha de banco interrompe a passagem e avisa

Todo acesso a dados testa o erro do banco; o erro de leitura e o de exclusão viram o mesmo
aviso de erro, e o de gravação um aviso próprio, despachados pela rotina de comunicação — a
passagem para ali, sem completar o resto.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar a estimativa da alimentação escolar do grupo no período e decidir sobre o cálculo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C845T

  Cenário: RN-02, RN-03 e RN-13 — consultar a estimativa do grupo no período
    Dado que o grupo tem cálculo para o período informado
    Quando informo a coordenação, o início e o limite do período com a opção CON
    Então vejo a situação do período, a descrição do tipo de órgão e a data do sistema
    E o início mostrado é o do cálculo do grupo, e não o que digitei
    E em cada uma das 14 linhas da grade vejo o código da subclasse, o código do gênero, a descrição, a marca do indicador, a quantidade de saldo inicial, o valor inicial, o preço e a marca da linha
    E nada é gravado

  Cenário: RN-01 — a tela se reapresenta em consulta
    Dado que acabei de enviar uma operação
    Quando a tela se apresenta de novo
    Então a opção volta a ser consulta
    E a marca de exclusão volta a N
    E a impressora volta em branco

  Cenário: RN-01 — operação diferente de consulta e de alteração
    Dado que estou na tela C845T
    Quando informo uma opção que não é consulta nem alteração
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nenhum cadastro é lido

  Cenário: RN-02 — período aberto
    Dado que o cálculo do grupo para o período não está fechado
    Quando consulto o período
    Então a situação do período aparece como tracejada

  Cenário: RN-06 — a descrição de cada gênero
    Dado que o gênero de uma linha está cadastrado e ativo
    Quando consulto o período
    Então aquela linha mostra a descrição do cadastro de gêneros

  Cenário: RN-06 — linha de gênero do cadastro genérico
    Dado que uma das linhas é de um gênero da subclasse 99
    Quando consulto o período
    Então a descrição daquela linha vem do cadastro genérico
    E a linha recebe a marca do indicador

  Cenário: RN-04 — grupo não cadastrado
    Quando informo uma coordenação que não existe no meu tipo de órgão
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo da coordenação
    E nada mais é lido

  Cenário: RN-05 — período sem cálculo
    Dado que o grupo não tem cálculo para o período informado
    Quando consulto o período
    Então vejo a mensagem "* Grupo sem estimativa para esta data *"
    E o cursor volta ao dia do limite
    E nada é preenchido

  Cenário: RN-05 — dia do limite em branco
    Dado que deixo o dia do limite em branco
    Quando consulto
    Então a tela adota o período já registrado para o grupo
    E passa a mostrá-lo no campo do limite
    E mostra o cálculo desse período, se ele existir

  Cenário: RN-05 — período sem cálculo de gênero
    Dado que o período existe no calendário do grupo
    E nenhum gênero está calculado naquele período
    Quando consulto o período
    Então vejo a mensagem "* Grupo sem calculo de estimativa cadastrado *"
    E nenhuma linha da grade é preenchida

  Cenário: RN-07 — período fechado aparece marcado
    Dado que o cálculo do grupo para o período está fechado
    Quando consulto o período
    Então a situação do período aparece como FECHADO

  Cenário: RN-07 — excluir um período fechado
    Dado que consultei um período fechado
    E marco a exclusão com a opção ALT
    Quando envio
    Então vejo a mensagem "* Cadastro fechado para este periodo *"
    E o cursor fica na marca de exclusão
    E nada é apagado

  Cenário: RN-09 — exclusão marcada com a opção em consulta
    Dado que consultei o período
    E marquei a exclusão
    Quando envio com a opção CON
    Então vejo a mensagem "* Use ALT para exclusão do cadastro *"
    E o cursor volta ao campo da opção
    E nada é apagado

  Cenário: RN-09 — marca de exclusão diferente de S
    Dado que consultei o período
    Quando preencho a marca de exclusão com outra coisa que não S e envio com a opção ALT
    Então nada é apagado
    E a consulta segue normalmente

  Cenário: RN-10 — excluir sem ter consultado o mesmo período
    Dado que estou na tela C845T com a opção ALT
    E marco a exclusão de uma coordenação e de um limite que não consultei
    Quando envio
    Então vejo a mensagem "* Consulte a estimativa antes de excluir *"
    E o cursor volta à coordenação
    E nada é apagado

  Cenário: RN-10 — imprimir sem ter consultado o mesmo período
    Dado que preencho a impressora com uma coordenação e um limite que não consultei
    Quando envio
    Então vejo a mensagem "* Consulte a estimativa antes de imprimir *"
    E o cursor volta à coordenação
    E nenhum pedido é registrado

  Cenário: RN-08 — pedir a impressão da relação
    Dado que consultei o período
    E não há pedido da mesma relação para o mesmo grupo na fila
    Quando informo a impressora e envio
    Então o pedido da relação da estimativa do grupo naquele período é registrado com o número seguinte da fila
    E o processamento é entregue à fila
    E nada do cálculo do período é alterado

  Cenário: RN-08 — pedido da mesma relação já na fila
    Dado que consultei o período
    E já existe um pedido da mesma relação para o mesmo grupo na fila
    Quando informo a impressora e envio
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta à coordenação
    E nenhum pedido novo é registrado

  Cenário: RN-11 — excluir o cálculo do período
    Dado que consultei um período aberto
    Quando marco a exclusão com a opção ALT e envio
    Então os valores por gênero, as quantidades por refeição e segmento, as quantidades por cardápio e os ajustes do período são apagados
    E o registro do período no calendário do grupo é apagado
    E fica na auditoria um lançamento com a operação de exclusão, a matrícula, a estação, a data e a hora e o registro apagado
    E nenhuma confirmação é pedida antes de apagar

  Cenário: RN-11 — exclusão e impressão pedidas juntas
    Dado que consultei o período
    Quando marco a exclusão com a opção ALT, preencho a impressora e envio
    Então o cálculo do período é apagado
    E nenhum pedido de impressão é registrado

  Cenário: RN-12 — a linha marcada abre a consulta do gênero
    Dado que consultei o período
    Quando marco uma linha com X e envio
    Então sou levado à tela C846T
    E ela abre em consulta
    E recebe o grupo, o gênero, o período, a quantidade, o valor, o preço e a situação daquela linha

  Cenário: RN-12 — linha marcada sem cálculo no período
    Dado que consultei o período
    Quando marco uma linha que não tem cálculo no período e envio
    Então a transação termina sem mensagem
    E não sou levado a nenhuma tela

  Cenário: RN-12 — nenhuma linha marcada
    Dado que consultei o período
    Quando não marco nenhuma linha e envio
    Então a transação termina
    E não sou levado a nenhuma tela
    E nada é alterado

  Cenário: RN-14 — digitação não numérica
    Dado que digito na coordenação, em uma das datas, no código da subclasse, no código do gênero ou em um campo auxiliar algo que não é número
    Quando envio
    Então a passagem não segue antes de ler qualquer cadastro
    E o cursor volta ao campo recusado

  Cenário: RN-15 — falha de banco
    Dado que o banco falha durante uma leitura ou durante a exclusão
    Quando envio
    Então a transação é interrompida com o aviso de erro do sistema
    E a operação não é considerada concluída
```
