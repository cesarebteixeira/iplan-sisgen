# US — N031C — Consultar as notas fiscais do órgão filho

## Estória

Como **servidor de CRE**, quero **consultar as notas fiscais lançadas para o órgão
filho a que tenho acesso, partindo do ano, do mês e do número da nota**, para que
**eu confira o que o órgão recebeu, de qual fornecedor, por qual valor e em qual
processo**.

A nota fiscal é o documento que amarra o fornecedor, o valor e o processo de
compra; o órgão filho é a unidade que a recebe e responde por ela. É por esta
consulta que a CRE enxerga, uma a uma, as notas lançadas para o seu órgão, com a
data, o fornecedor, o valor e o processo de cada uma. Sem ela, quem acompanha a
despesa do órgão teria só o número do processo, sem saber quais notas o compõem,
de quem são e por quanto foram.

A consulta é de leitura: ela não inclui, não altera e não exclui nota alguma.

## Contexto

Jornada S000M → E000M → E600M → N031C.

Ator: servidor de CRE — consulta as notas fiscais lançadas para o órgão filho que
o seu acesso alcança.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e
menus.md`: é dado de navegação, não regra de negócio.

Esta é a última tela da jornada: ela não abre nenhuma outra. O órgão filho e a
coordenadoria regional não são escolhidos nela — vêm do acesso que a entrada
carregou para a sessão do servidor. A tela também não confere qual tela a chamou:
o modo de operação com que ela abre é decisão dela, e não de quem a chamou. O nome
do órgão é lido do cadastro de órgãos, a razão social de cada nota, do cadastro de
fornecedores, e as notas, do cadastro de notas fiscais.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A consulta é sempre do órgão filho do servidor

A tela não deixa escolher de qual órgão é a consulta. Ela abre com o órgão filho
que está na sessão do servidor — o mesmo que a entrada carregou do cadastro de
acesso da matrícula — e mostra o código e o nome desse órgão e a coordenadoria
regional de ensino do acesso. A lista é a das notas desse órgão, do tipo de órgão
da sessão. Quem decide o que o servidor pode consultar é o acesso dele, não o que
ele digita na tela.

### RN-02 — A tela só consulta: nada é incluído, alterado ou excluído

Esta tela é de leitura. Para os quatro cadastros que ela enxerga — as telas do
sistema, as notas fiscais, os órgãos e os fornecedores —, o programa declara as
operações de gravar, excluir e travar registro, mas nenhuma delas é executada em
caminho algum: todas as operações de dados que a tela executa são leituras.
Também não há registro de auditoria, porque não há gravação para auditar. O
desfecho de cada consulta é apenas a lista apresentada.

### RN-03 — A tela abre em consulta e recusa qualquer outro modo

A tela aceita um único modo de operação, o de consulta, e ela própria o assume ao
abrir — não lê a tela de origem para decidir o modo. Se a confirmação chegar com
outro modo, o sistema recusa com **\* Operacao nao disponivel. Use CON \***,
devolve o cursor ao campo do modo de operação e não apresenta lista alguma.

[?] O único modo que a tela aceita é igual ao código interno de consulta, que o
sistema carrega da tabela de mensagens do idioma e que, no texto do programa,
nasce como **INQ**; o aviso, porém, manda usar **CON**. Não há, no acervo, a
tabela de mensagens que diria qual é o texto carregado em tempo de execução, e sem
ela não se sabe o que o servidor precisa digitar para ser aceito. Pergunta ao site.

### RN-04 — A tela mostra doze notas por vez

A tela apresenta **12 notas por vez**, na ordem do cadastro de notas: ano, mês e
número. Cada linha traz a data da nota, o código do fornecedor, a razão social, o
número da nota, o valor total, o número do processo e o tipo de contrato. O
cabeçalho traz o código e o nome do órgão, a coordenadoria regional, o ano, o mês
e o número informados, a descrição do tipo de órgão e a data do sistema.

[?] Se há mais notas do que as 12 da página, o fonte não mostra como chegar às
seguintes: não há comando de página seguinte nem contador de passada na área de
trabalho da tela. Não se sabe se a consulta pagina ou se mostra apenas as 12
primeiras notas do ponto de partida. Pergunta ao site.

### RN-05 — A lista parte do ano, do mês e do número

O ano, o mês e o número são o ponto de partida da lista. Ao abrir, a tela parte do
ano, do mês e do número que a sua área de trabalho já tem; quando ela chega sem
nenhum órgão na área de trabalho — isto é, sem nada que a tela anterior tenha
deixado —, toma o ano corrente do sistema, zera o mês e o número e começa na
primeira nota daquele ano. Quando o servidor informa outro ano, outro mês ou outro
número e confirma, essa combinação passa a ser o ponto de partida da lista; se a
combinação não existe para o órgão, o ano, o mês e o número são zerados e a lista
recomeça pelas primeiras notas do órgão.

[?] A tela anterior (E600M) publica na área comum apenas os seus próprios campos —
o modo, o órgão, o nome, a coordenadoria, a impressora e a descrição do relatório
—, e essa área termina antes do ano, do mês e do número que a consulta usa. O que
a lista mostra no ano, no mês e no número quando o servidor abre a tela vindo da
E600M sem ter informado nada fica sem resposta no acervo. Pergunta ao site.

### RN-06 — Órgão sem notas é avisado

Quando a busca não encontra nenhuma nota para o órgão no ponto de partida, o
sistema avisa **\* Orgao sem notas cadastradas \***, zera o ano, o mês e o número
da área de trabalho e não apresenta linha alguma.

### RN-07 — Órgão diferente do que está na sessão é recusado

Quando o servidor tem um órgão filho na sessão e informa outro — ou deixa o campo
em branco —, o sistema recusa com **\* Usuario sem acesso a outro orgao \***,
devolve o cursor ao campo do órgão e não lista nada. Vale dizer o mesmo de outra
forma: ninguém consulta nota de órgão que não é o seu.

### RN-08 — Órgão em branco é recusado

Quando a sessão do servidor não tem órgão filho e ele confirma sem informar um, o
sistema recusa com **\* Informe o orgao \*** e devolve o cursor ao campo do órgão.

### RN-09 — Órgão não cadastrado é recusado

Informado um órgão que não existe no cadastro de órgãos, o sistema recusa com
**\* Orgao nao cadastrado \*** e devolve o cursor ao campo do órgão.

[?] A recusa do órgão não cadastrado depende de um indicador de "achou" que a
leitura que **não** encontrou o órgão não deixa marcado: quem não encontra não
grava o indicador, e a guarda seguinte testa o que a leitura anterior tinha
deixado. Se o indicador estiver marcado como "achou" — o que acontece depois de
uma leitura que achou —, um órgão inexistente passa pela guarda e a tela segue com
o nome do órgão anterior. Ou a guarda vale para outro caso, ou o caminho do órgão
não cadastrado fica inalcançável. Pergunta ao site.

### RN-10 — Órgão de outra coordenadoria regional é recusado

O cadastro de órgãos guarda a coordenadoria regional de cada órgão. Se a do órgão
informado for diferente da coordenadoria do servidor, o sistema recusa com
**\* Usuario sem acesso ao grupo deste Orgao \*** e devolve o cursor ao campo do
órgão. Servidor sem coordenadoria na sessão não passa por essa conferência.

### RN-11 — Servidor sem órgão filho não vê lista

Se a sessão do servidor não tem órgão filho e nenhuma outra tela deixou um órgão,
a tela abre com o cursor no campo do órgão e **não apresenta lista nem mensagem**:
nada é lido e nada é dito sobre o motivo.

[?] A tela deixa o cursor e não avisa nada; o servidor vê uma tela vazia sem
explicação. A tela anterior aceita um órgão digitado nesse caso, mas a consulta
trabalha com o órgão da sessão e com o que ficou na área comum — não com o que foi
digitado. Era para haver um aviso, ou para a consulta aproveitar o órgão digitado
na tela anterior? Pergunta ao site.

### RN-12 — A conferência dos campos informados

Ao confirmar, o sistema confere **cinco** campos, um a um: o órgão, a coordenadoria
regional, o mês, o ano e o número da nota. Cada um tem de ser numérico e caber no
tamanho do seu campo; campo em branco vale zero e os zeros à esquerda são
descartados. O campo reprovado é marcado e o cursor volta para ele. Antes da
conferência, o sistema limpa os **nove** campos que ele mesmo preenche a partir
dos cadastros — o nome do órgão, a descrição do tipo de órgão, a data do sistema,
o código do fornecedor, a razão social, o número da nota, o valor total, o número
do processo e o tipo de contrato —, de modo que a lista anterior não fica na tela.

### RN-13 — A data, o valor e o processo aparecem em forma de leitura

A data da nota é montada como dia, mês e ano separados por barras. O valor total
aparece com vírgula decimal. O número do processo, guardado como uma sequência de
14 dígitos, é apresentado em grupos separados por barras; quando os dois primeiros
dígitos são zeros, o primeiro grupo não é apresentado.

### RN-14 — A razão social vem do cadastro de fornecedores

O código do fornecedor vem da nota; a razão social é buscada no cadastro de
fornecedores por esse código. A razão social que aparece na linha é a do cadastro
cortada em **20 posições** — o cadastro guarda 40.

[?] Quando o fornecedor da nota não está no cadastro, o sistema não limpa a razão
social da linha: a coluna pode repetir a razão social da linha anterior. E o corte
em 20 posições não é do cadastro, é da tela. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consultar as notas fiscais do órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o órgão filho e a coordenadoria regional do meu acesso
    E tenho acesso à tela N031C

  Cenário: A consulta é do órgão filho do meu acesso
    Dado que o meu acesso tem um órgão filho
    Quando a tela N031C abre
    Então vejo o código e o nome do meu órgão filho e a minha coordenadoria regional
    E a lista é a das notas desse órgão

  Cenário: A consulta não grava nada
    Dado que estou na tela N031C
    Quando abro a lista e confirmo a consulta
    Então nenhuma nota, órgão ou fornecedor é incluído, alterado ou excluído
    E nenhum registro de auditoria é criado

  Cenário: Modo de operação diferente do de consulta é recusado
    Dado que estou na tela N031C
    Quando confirmo com um modo de operação diferente do de consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo do modo de operação
    E nenhuma lista é apresentada

  Cenário: A tela mostra doze notas do órgão
    Dado que o meu órgão filho tem notas fiscais lançadas
    Quando a lista é apresentada
    Então vejo até 12 notas, na ordem de ano, mês e número
    E cada linha traz a data da nota, o código do fornecedor, a razão social, o
      número da nota, o valor total, o número do processo e o tipo de contrato

  Cenário: A lista parte do ano, do mês e do número informados
    Dado que estou na tela N031C
    Quando informo o ano, o mês e o número da nota e confirmo
    Então a lista começa na nota dessa combinação
    E, se a combinação não existe para o órgão, a lista recomeça pelas primeiras notas

  Cenário: Órgão sem notas é avisado
    Dado que o meu órgão filho não tem nota no ponto de partida
    Quando a lista é pedida
    Então vejo a mensagem "* Orgao sem notas cadastradas *"
    E nenhuma linha é apresentada

  Cenário: Órgão diferente do meu é recusado
    Dado que a minha sessão tem o meu órgão filho
    Quando informo outro órgão, ou deixo o campo em branco, e confirmo
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E o cursor volta ao campo do órgão
    E nenhuma lista é apresentada

  Cenário: Órgão em branco é recusado quando não tenho órgão na sessão
    Dado que a minha sessão não tem órgão filho
    Quando confirmo sem informar o órgão
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor volta ao campo do órgão

  Cenário: Órgão não cadastrado é recusado
    Dado que estou na tela N031C
    Quando informo um órgão que não existe no cadastro de órgãos
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão

  Cenário: Órgão de outra coordenadoria regional é recusado
    Dado que estou na tela N031C
    E que o órgão informado pertence a outra coordenadoria regional
    Quando confirmo
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste Orgao *"
    E o cursor volta ao campo do órgão

  Cenário: Servidor sem órgão filho não vê lista
    Dado que a minha sessão não tem órgão filho
    E que nenhuma tela anterior deixou um órgão
    Quando a tela N031C abre
    Então o cursor fica no campo do órgão
    E nenhuma lista e nenhuma mensagem são apresentadas

  Cenário: Campos em branco e conteúdo recusado na confirmação
    Dado que estou na tela N031C
    Quando deixo campos em branco e confirmo
    Então o sistema os trata como zero
    E o campo que não passar na conferência é marcado, com o cursor de volta nele
    E os campos preenchidos a partir dos cadastros são limpos

  Cenário: A data, o valor e o processo aparecem em forma de leitura
    Dado que a lista é apresentada
    Quando olho uma linha
    Então a data da nota aparece com o dia, o mês e o ano separados por barras
    E o valor total aparece com vírgula decimal
    E o número do processo aparece em grupos separados por barras

  Cenário: A razão social vem do cadastro de fornecedores
    Dado que a lista é apresentada
    Quando olho o fornecedor de uma nota
    Então vejo a razão social que está no cadastro de fornecedores
    E ela aparece cortada em 20 posições
```
