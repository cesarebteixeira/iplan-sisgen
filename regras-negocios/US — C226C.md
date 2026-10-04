# US — C226C — Consultar os órgãos definitivo e provisório do grupo e pedir a relação

## Estória

Como **servidor de CRE**, quero **consultar, para a coordenadoria regional escolar do meu
vínculo, os órgãos definitivo e provisório registrados e a data da atualização de cada
um, e pedir a relação em papel**, para que **eu saiba em que órgão a coordenadoria está,
de qual provisório ele veio e desde quando, e possa entregar a conferência a quem precisa
dela**.

A coordenadoria tem os seus órgãos registrados aos pares: cada registro diz qual é o
**órgão definitivo** do grupo, de qual **órgão provisório** ele veio e quando isso foi
atualizado. Quem mantém esse registro é a tela de manutenção do histórico — não esta.
Esta tela existe para ler o registro e para tirar dele a relação que a secretaria
confere; sem ela, saber em que órgão a coordenadoria está daria uma consulta por
registro, e o documento da conferência não teria por onde ser pedido.

## Contexto

Jornada S000M → C000M → C200M → C226C.

Ator: servidor de CRE — consulta os órgãos definitivo e provisório da sua coordenadoria
e a data da atualização de cada um, e pede a relação em papel.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O `C000M` e o `C200M` são menus de opções e não gravam nada: entregam a transação à tela
desta jornada sem passar registro nem operação, e é a própria `C226C` que fixa o modo
com que abre. O contexto de que a tela se serve — a matrícula, o código de acesso, o
privilégio, o tipo de órgão, a coordenadoria e a estação da sessão — é o que a entrada
deixou na sessão. A `C226C` é o fim da jornada: não abre outra tela.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela é de consulta: qualquer outra operação é recusada

A tela abre com a operação fixada em **consulta** e repõe esse valor a cada
apresentação, de modo que a operação mostrada volta a ser a consulta. Informada outra
operação, o sistema recusa com **\* Operacao nao disponivel. Use CON \***, devolve o
cursor ao campo da operação e não lê o grupo nem o histórico.

[?] A recusa só existe se a tela oferecer ao operador o campo da operação: a abertura
repõe a consulta sozinha, e o texto da tela não está no material lido. Pergunta ao site.

[?] A mensagem manda usar **CON** e o programa confere o código interno de consulta do
sistema; se a tela mostra um texto e o programa confere o outro, o que o operador digita
para consultar não está no material lido. Pergunta ao site.

[?] Depois de qualquer uma das recusas desta tela, a transação deveria encerrar; o
material lido não fecha esse ponto, porque a instrução de encerramento foi descartada na
preparação do fonte — o descarte é premissa do perfil de compilação assumido, não do
acervo. Pergunta ao site.

### RN-02 — A consulta é sempre do grupo do próprio servidor

A consulta é sempre da coordenadoria do vínculo do servidor: o campo do grupo abre
preenchido com essa coordenadoria e não aceita outra. Informado um grupo diferente do da
sessão, o sistema recusa com **\* Usuario sem acesso a este grupo \***, devolve o cursor
ao campo do grupo e não lê nada. Quem determina o alcance da consulta é o vínculo do
servidor, não o que ele digita.

[?] A conferência compara o grupo que volta da tela com uma **segunda cópia** da área da
sessão, e não com a cópia que preencheu o campo; essa segunda cópia só é refeita quando a
tela que entra é de outro módulo. Se ela não for refeita nesta abertura, a conferência
compara o grupo com um resíduo e pode recusar o próprio grupo do servidor — e a consulta
fica inalcançável para quem tem grupo na sessão. O material lido não decide esse caso.
Pergunta ao site.

### RN-03 — Quem não tem grupo na sessão informa o grupo, e ele tem de estar cadastrado

Chegando a sessão sem grupo, é o servidor que informa a coordenadoria, e o sistema
confere que aquele grupo existe no cadastro de grupos da secretaria do seu tipo de
órgão. Não existindo, a recusa é **\* Grupo nao cadastrado \***, com o cursor no campo do
grupo, e nada é lido. Aceito o grupo, é ele que passa a valer para a consulta; como a
lista é montada na abertura da tela, o grupo informado só governa a lista na apresentação
seguinte. A capacidade do cadastro de grupos é de **1.000** grupos — capacidade é o máximo
esperado, parâmetro de dimensionamento, não volume cadastrado.

[?] A conferência do cadastro de grupos só roda quando o grupo informado difere do da
sessão; com o grupo da sessão preenchido, o cadastro não é lido de novo. Se um grupo da
sessão apagado do cadastro deveria ser avisado, o caminho não avisa. Pergunta ao site.

[?] Se o grupo informado deveria valer já na mesma mensagem: o caminho que o aceita
guarda o grupo e termina sem remontar a lista, que só é montada na apresentação seguinte.
Pergunta ao site.

[?] A sessão sem grupo é o único caso em que o campo aceita um grupo digitado; o material
lido não diz se isso é intenção — um servidor de âmbito geral — ou resíduo do gerador.
Pergunta ao site.

### RN-04 — O grupo digitado passa por edição numérica

O campo do grupo aceita digitação e passa por edição numérica: o que não for número é
recusado, com o cursor de volta ao campo do grupo, e a recusa interrompe o tratamento
antes de o histórico ser lido. Campo em branco é tratado como zero.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não está
nos fontes desta jornada: a rotina que faz a edição numérica é importada do ambiente de
execução, sem fonte no acervo. O que esta tela faz, na recusa, é devolver o cursor ao
campo do grupo. Pergunta ao site.

### RN-05 — Antes de mostrar e antes de pedir, o sistema confere a tela, a rota e a permissão

Toda transação — a abertura que monta a lista e a mensagem que pede a impressão — passa
por conferências com o contexto da sessão. A tela precisa estar cadastrada no cadastro de
telas: não estando, a recusa é **\* Tela nao disponivel \***. A matrícula precisa ter a
tela autorizada no seu código de acesso: não tendo, a recusa é
**\* Acesso negado para esta matricula \***. A transação passa também pela lógica de
rota, que decide o encaminhamento a partir do que a tela manda. Se qualquer conferência
não fecha, a tela abandona a transação: nada é lido e nada é pedido.

[?] A conferência por operação procura os flags de inclusão, de alteração e de exclusão
do código de acesso, mas **não** o de consulta: quem tem a tela autorizada consulta sem
precisar do flag de consulta. Se a intenção era exigir esse flag por tela, o caminho não
o exige. Pergunta ao site.

### RN-06 — Cada consulta começa com os campos de resultado limpos

Antes de conferir a digitação e de ler o histórico, a tela apaga o órgão definitivo, o
órgão provisório, os dois nomes e a data da atualização que a consulta anterior havia
mostrado. Uma consulta recusada não deixa na tela o resultado da consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe um
caminho de entrada em que os campos não são limpos, é pergunta ao site.

### RN-07 — A tela mostra o órgão definitivo, o provisório e a data, quatro registros por vez

Para o grupo da consulta, a tela mostra os registros do cadastro do histórico de órgãos.
Cada registro traz **cinco dados**: o código e o nome do **órgão definitivo**, o código e
o nome do **órgão provisório** e a **data da atualização**, no formato dia/mês/ano com
quatro dígitos no ano. Os dois nomes saem do cadastro de órgãos. A tela apresenta
**quatro registros por vez**, e é esse o tamanho da página. A capacidade do cadastro do
histórico é de **1.000** registros e a do cadastro de órgãos, de **12.000**; capacidade é
o máximo esperado, parâmetro de dimensionamento, não volume cadastrado. Quem mantém o
histórico de órgãos é a tela `C226T`, não esta.

[?] Se cada registro da página é um órgão diferente do grupo: a leitura que traz o
registro seguinte parte do código do órgão que acabou de voltar, e o efeito dos
sinalizadores de posicionamento da leitura não está no corpus nem no manual. Pela leitura
que avança, a página mostra órgãos distintos; pela que relê a chave, o mesmo órgão se
repete nas quatro linhas. Pergunta ao site.

[?] O que a página seguinte mostra quando o grupo tem mais registros do que os quatro que
cabem: o caminho que reinicia a contagem só roda quando a leitura chegou ao fim do
histórico. Pergunta ao site.

[?] O nome do órgão provisório sai em **28** caracteres nesta tela e o do definitivo em
**40**, embora os dois venham do mesmo campo de 40 do cadastro de órgãos. Se a tela corta
o nome do provisório, é pergunta ao site.

### RN-08 — O grupo sem histórico é avisado

Não havendo nenhum registro de histórico para o grupo da consulta, a tela não preenche
linha nenhuma e avisa **\* Nao existe historico de orgaos \***. O aviso é decidido na
montagem do **primeiro** registro: a partir do segundo, a leitura que não acha registro
simplesmente para de preencher a página, sem aviso.

### RN-09 — O cabeçalho traz a data do sistema e a descrição do tipo de órgão

Fora dos registros, a tela exibe a **data do sistema** e a **descrição do tipo de órgão**
da sessão.

[?] Nem a data do sistema nem a descrição do tipo de órgão são preenchidas por nenhum
programa do acervo lido: os dois campos só aparecem como origem de cópia e são
inicializados em branco pelo ambiente comum. De onde vêm os valores é pergunta ao site;
se não vierem do ambiente, os dois campos saem em branco.

### RN-10 — Preenchido o código de impressão, a tela registra o pedido da relação

A tela é de consulta, mas o campo do **código de impressão** é o que faz dela um pedido.
Preenchido — e passadas as conferências —, a tela registra **um pedido** na fila de
requisições de impressão e o entrega ao processamento em lote, que monta a relação do
grupo. Em branco, nada é pedido: é a consulta pura, e nada é gravado.

[?] O código de impressão é o único dado da tela que não passa por edição nem por
conferência: qualquer valor de até dez caracteres é aceito e vai para o pedido. Se ele
deveria apontar para uma impressora cadastrada, esta tela não o confere. Pergunta ao
site.

### RN-11 — O grupo sem histórico não emite a relação

Com o código de impressão preenchido, a tela exige que o grupo tenha histórico: não
havendo nenhum registro para o grupo, recusa com **\* Grupo sem historico de orgaos \***,
com o cursor no campo do grupo, e nada é pedido. É a única conferência própria do pedido.

### RN-12 — O pedido leva o próximo número da fila e os dados da consulta

O pedido recebe o **número seguinte ao do último pedido** da fila de requisições e leva: o
código do relatório, o **código de impressão**, **uma cópia**, a estação, a matrícula de
quem pediu, o **endereço de correio** do servidor (lido do cadastro de funcionários no
momento do pedido), o **tipo de órgão** da sessão, o **grupo** e a **data do pedido**. A
situação do pedido fica em branco e o número do processo, zerado. A fila tem capacidade
para **90.000** pedidos — capacidade, não volume.

[?] De onde sai o número quando a fila está vazia: a tela procura o último pedido da fila
e soma um; não achando, o número sai do que estiver na área do registro de requisição, e
o fonte não diz o que é. Pergunta ao site.

[?] O que o pedido leva nos campos que a tela não informa: a área do registro fica com o
conteúdo do último pedido lido para achar o número, e a tela só repõe os campos que ela
mesma preenche; se os demais saem zerados ou herdados do pedido anterior, o fonte não diz
— a criação do registro é feita por recurso importado, sem fonte no acervo. Pergunta ao
site.

### RN-13 — Registrado o pedido, o processamento da relação é disparado

Gravado o pedido, a tela dispara o processamento em lote que monta a relação do grupo. Ao
rodar, a relação imprime, por grupo, o órgão definitivo, o órgão provisório e a data da
atualização de cada registro — os mesmos dados da tela — e **apaga da fila os pedidos que
consumiu**: é assim que o pedido sai da fila.

[?] O disparo é condicionado a o estado da transação não ser um valor que a tela nunca
atribui; como a gravação deixa o estado em branco, o disparo acontece em todos os
desfechos observados. O que esse valor significa é pergunta ao site.

[?] A relação apaga os pedidos daquela relação para o tipo de órgão e o grupo, e não
apenas o pedido que ela mesma está atendendo: pedindo duas vezes para o mesmo grupo, o
primeiro processamento que rodar tira da fila o pedido da segunda. Se os pedidos já
disparados não dependem de continuar na fila, o efeito é nenhum. Pergunta ao site.

[?] O que o trabalho de lote faz além de imprimir e apagar os pedidos: a tela só monta a
chamada do trabalho, e o material lido não traz catálogo que ligue o nome do trabalho ao
programa que ele roda. Pergunta ao site.

### RN-14 — A consulta não altera cadastro nenhum e não deixa auditoria

A tela e as rotinas comuns que ela chama, nesta consulta, só leem: o cadastro de telas, o
cadastro de funcionários, o cadastro de órgãos, o cadastro de grupos, o cadastro do
histórico de órgãos e a fila de requisições. A única escrita é o pedido de impressão, e
só incluindo: nenhum registro é alterado ou excluído, e **nenhum registro de auditoria é
gerado**. As operações de gravação e de exclusão dos cadastros que a tela enxerga existem
declaradas no programa, mas **não são executadas em nenhum caminho**: declarar não é
executar.

[?] Se o pedido de impressão deveria deixar rastro de auditoria: a tela não enxerga o
cadastro de auditoria e não grava nada nele; se a inclusão de um pedido deveria ser
auditada como as inclusões das telas de manutenção, o caminho não a audita. Pergunta ao
site.

### RN-15 — Prefixo de tela preenchido desvia a transação

Chegando a transação com o campo de prefixo de tela preenchido, a conferência de rota a
encaminha para a tela indicada no prefixo, em vez de tratar a consulta: nada é lido e
nada é pedido.

[?] O que preenche o campo de prefixo de tela não está no corpus: não se sabe quem manda
prefixo para a tela desta jornada. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar os órgãos definitivo e provisório do grupo e pedir a relação

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C226C

  Cenário: A consulta é do grupo do meu vínculo
    Dado que a minha sessão carrega a minha coordenadoria regional escolar
    Quando abro a tela C226C
    Então o campo do grupo aparece preenchido com a minha coordenadoria
    E a lista é a dos órgãos do meu grupo

  Cenário: Consulta dos órgãos do grupo
    Dado que o meu grupo tem histórico de órgãos registrado
    Quando abro a tela C226C
    Então vejo os registros em linhas, cada uma com o órgão definitivo e o órgão provisório
    E cada linha traz o código e o nome dos dois órgãos
    E cada linha traz a data da atualização, no formato dia/mês/ano com quatro dígitos no ano

  Cenário: A página traz quatro registros
    Dado que o meu grupo tem histórico de órgãos registrado
    Quando abro a tela C226C
    Então vejo no máximo quatro registros
    E cada registro traz os cinco dados do histórico

  Cenário: O grupo sem histórico é avisado
    Dado que o meu grupo não tem nenhum registro de histórico
    Quando abro a tela C226C
    Então vejo a mensagem "* Nao existe historico de orgaos *"
    E nenhuma linha é preenchida

  Cenário: A data do sistema e o tipo de órgão no cabeçalho
    Dado que entrei no sistema
    Quando abro a tela C226C
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: Cada consulta começa sem o resultado da anterior
    Dado que a consulta anterior mostrou registros
    Quando volto a abrir a tela C226C
    Então os órgãos, os nomes e a data da consulta anterior não ficam na tela

  Cenário: Operação diferente da consulta
    Dado que estou na tela C226C
    Quando informo uma operação diferente da consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nada do histórico é lido nesse caminho

  Cenário: Grupo de outra coordenadoria é recusado
    Dado que estou na tela C226C com a minha coordenadoria preenchida
    Quando informo outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo do grupo
    E nada é lido

  Cenário: Sessão sem grupo informa o grupo, e ele tem de existir
    Dado que a minha sessão não carrega coordenadoria
    Quando informo uma coordenadoria que não está cadastrada para a minha secretaria
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo do grupo
    E nada é lido

  Cenário: O grupo informado numa sessão sem grupo passa a valer
    Dado que a minha sessão não carrega coordenadoria
    E que a coordenadoria que informei está cadastrada
    Quando envio a tela e volto a ela
    Então a lista é a do grupo que informei

  Cenário: Digitação não numérica no grupo
    Dado que estou na tela C226C
    Quando digito no campo do grupo algo que não é número
    Então o sistema recusa a digitação antes de ler o histórico
    E o cursor volta ao campo do grupo

  Cenário: Tela não cadastrada
    Dado que a tela C226C não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo consultar

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela C226C autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo consultar

  Cenário: A consulta sem código de impressão não grava nada
    Dado que estou na tela C226C com o código de impressão em branco
    Quando a lista é mostrada e eu confirmo a tela
    Então nenhum pedido é registrado na fila de requisições
    E nenhum cadastro é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Pedido de impressão da relação
    Dado que estou na tela C226C
    E que o meu grupo tem histórico de órgãos registrado
    Quando informo o código de impressão e confirmo a tela
    Então um pedido é registrado na fila de requisições
    E o pedido leva o próximo número da fila, o código do relatório e o código de impressão
    E leva uma cópia, a estação, a minha matrícula e o meu endereço de correio
    E leva o tipo de órgão, o grupo e a data do pedido

  Cenário: O grupo sem histórico não emite a relação
    Dado que estou na tela C226C
    E que o meu grupo não tem nenhum registro de histórico
    Quando informo o código de impressão e confirmo a tela
    Então vejo a mensagem "* Grupo sem historico de orgaos *"
    E o cursor volta ao campo do grupo
    E nenhum pedido é registrado

  Cenário: Registrado o pedido, o processamento da relação é disparado
    Dado que registrei um pedido de impressão da relação do meu grupo
    Quando o processamento da relação roda
    Então a relação imprime, por grupo, o órgão definitivo e o órgão provisório de cada registro
    E imprime a data da atualização de cada registro
    E o pedido consumido sai da fila de requisições

  Cenário: Nenhuma operação de cadastro é executada
    Dado que estou na tela C226C e a consulta foi mostrada
    Quando a transação termina
    Então nenhum registro dos cadastros que a tela enxerga foi incluído, alterado ou excluído
    E nenhum registro de auditoria foi gerado

  Cenário: Prefixo de tela preenchido desvia a transação
    Dado que a transação chega à C226C com o prefixo de tela preenchido
    Quando a conferência de rota roda
    Então a transação é encaminhada para a tela indicada no prefixo
    E nada é lido e nada é pedido
```
