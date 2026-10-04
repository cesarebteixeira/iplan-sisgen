# US — C848T — Somar os cálculos do grupo e encomendar a impressão do resultado

## Estória

Como **servidor de CRE**, quero **somar os cálculos de estimativa do meu grupo para até
seis datas de cálculo e encomendar a impressão do resultado**, para que **eu tenha num
único arquivo a soma do que já foi calculado em vários períodos, sem somar período a
período à mão e sem perder o registro de quem pediu**.

A estimativa é calculada período a período: cada cálculo vale de uma data de início a uma
data limite, e é a data limite que distingue um período do outro. Esta tela recebe o grupo,
até seis datas de cálculo e a impressora, confere quais dessas datas têm cálculo
cadastrado, mostra a data de início de cada período e, depois da confirmação de quem opera,
registra o pedido, deixa o lançamento na auditoria e entrega o processamento que gera o
arquivo. Sem ela, a soma de vários períodos sairia por fora do sistema, sem conferência
contra o cadastro e sem registro de quem pediu.

## Contexto

Jornada S000M → C000M → C800M → C840M → C848T.

Ator: servidor de CRE — informa o grupo, até seis datas de cálculo e a impressora, confere
as datas de início trazidas do cadastro e confirma a geração.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os três menus do caminho — `C000M`, `C800M` e `C840M` —
só encaminham e não gravam nada; o último é quem oferece a tela.

O contexto de que a C848T se serve — a matrícula, o tipo de órgão, o privilégio, a
coordenação regional escolar da sessão, a estação e a data e a hora — é o que a entrada
deixou na sessão; a tela não recalcula nada disso: usa para conferir o acesso, montar o
cabeçalho e identificar quem pede. O **tipo de órgão da sessão** é um dos componentes da
procura do cálculo.

A tela **não encadeia para outra tela**: depois das conferências ela se reabre para pedir a
confirmação (RN-09), e é essa reabertura — a única saída que o grafo de navegação registra
— que separa a conferência do registro.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela abre em consulta e não aceita outra operação

Ao ser apresentada, a tela repõe a operação como **consulta**, e é esse o único valor que
aceita: o operador não escolhe a operação. Se a mensagem chegar com outra operação, o
sistema recusa com **\* Operacao nao disponivel. Use CON \***, devolve o cursor ao campo da
operação e, nesse caminho, não lê nem registra nada.

O modo não vem de quem chamou: o menu que abre a tela passa a própria opção adiante, mas a
tela a descarta ao se apresentar. Não há, no caminho lido, comparação da tela de origem com
código de tela nenhum.

[?] A recusa manda usar **CON**, mas o que a tela aceita é o código interno da consulta, que
não é esse texto. O texto da máscara não está no material lido: se o terminal não traduzir
o que o operador digita, a recusa pode ser intransponível. Pergunta ao site.

### RN-02 — O grupo é obrigatório

O operador informa o **grupo** — a coordenação regional escolar — e ele tem de vir
preenchido; em branco, o sistema recusa com **\* Informe o grupo \***, devolve o cursor ao
campo do grupo e não lê cálculo nenhum. Na tela o campo se chama *COORD.REG.ESCOLA*; a
mensagem o chama de grupo.

### RN-03 — É preciso informar ao menos uma data de cálculo

A tela pede até seis datas de cálculo. Se todas as seis vierem em branco, o sistema recusa
com **\* Informe data de calculo \***, devolve o cursor à primeira data de cálculo e não lê
cálculo nenhum.

### RN-04 — A tela trabalha com seis períodos, e cada período tem data de início e data de cálculo

A máscara tem **46 itens**, dos quais **5 são o cabeçalho da transação** (o identificador da
tela, a origem, o número da transação, a data e o mês de referência) e os outros **41** são
campos: a operação, um código de tela que a máscara carrega, o grupo, as **36 datas**, a
impressora e a resposta da confirmação. As 36 datas são **seis períodos**, e cada período
tem duas datas, cada uma em dia, mês e ano: a data de **início** do período e a data de
**cálculo** (a data limite). A tela não exige os seis: período em branco é simplesmente
saltado, e os preenchidos são tratados na ordem em que aparecem.

[?] Os rótulos das 36 datas não vêm no material lido: a única palavra de negócio que a ficha
da tela registra é *COORD.REG.ESCOLA*, para o grupo. Se as seis datas são seis períodos do
ano, bimestres ou datas escolhidas livremente, o acervo lido não diz. Pergunta ao site.

### RN-05 — A data de início mostrada vem do cálculo cadastrado, não do que foi digitado

Cada data de início que a tela mostra é a do cálculo encontrado no cadastro: antes de
conferir, a tela apaga as seis datas de início e, para cada período que tenha cálculo, copia
a data de início do cálculo para a tela. O que o operador tiver digitado nesses campos é
descartado — embora a digitação deles seja editada como as demais.

[?] Os campos da data de início são digitáveis e passam pela edição numérica, mas o valor
digitado não entra em conferência alguma nem no pedido: é sempre substituído pelo do
cadastro. Ou os campos deveriam ser só de exibição, ou a tela está ignorando o que o
operador digita. Pergunta ao site.

### RN-06 — Cada data de cálculo tem de ter cálculo para o grupo e para o órgão da sessão

Para cada data de cálculo informada, a tela procura o cálculo no cadastro dos cálculos de
estimativa pelo **tipo de órgão da sessão**, pelo **grupo** informado e pela **data
limite**, com duas dimensões do cálculo — a subclasse e o gênero — fixadas em zero. Não
achando, ou achando registro de outro grupo ou de outra data, o sistema recusa com
**\* Calculo nao cadastrado para esta data \***, devolve o cursor ao dia da data de cálculo
que falhou e não registra nada.

[?] A procura fixa a subclasse e o gênero em zero e a conferência do que foi achado não olha
essas duas dimensões: um cálculo cadastrado apenas por subclasse e gênero não é encontrado,
e a tela diz que não há cálculo para a data. Se só o cálculo "geral" deve contar, é pergunta
ao site.

### RN-07 — A impressora é obrigatória, e a exigência vale só até a pergunta

A tela pede a **impressora** e ela tem de vir preenchida; em branco, o sistema recusa com
**\* Informe a impressora \***, devolve o cursor ao campo da impressora e não registra nada.
O que for digitado não é conferido contra cadastro nenhum: qualquer texto serve. É esta
impressora que segue no pedido — e é ela que distingue esta tela da irmã do mesmo menu, que
faz a mesma soma sem perguntar impressora.

[?] A impressora é exigida na passagem que confere o grupo e as datas, mas a guarda da
confirmação não inclui esse campo e a passagem que atende a resposta **S** não volta a
conferi-lo: apagada depois da pergunta, a resposta continua valendo e o pedido é gravado com
a impressora em branco — embora o cadastro da fila exija impressora. Se o processamento
depende dela, o material lido não diz. Pergunta ao site.

### RN-08 — O usuário tem de ter e-mail cadastrado

Antes de conferir o grupo e as datas, a tela lê o cadastro do usuário pela matrícula da
sessão e exige e-mail preenchido; em branco, recusa com
**\* Usuario sem e-mail cadastrado \*** e não segue. É esse e-mail que segue no bloco de
parâmetro que a tela entrega ao processamento.

[?] O e-mail vai no bloco de parâmetro; o pedido registrado na fila fica com o e-mail em
branco. Se o processamento lê o destinatário do parâmetro ou do registro da fila, o acervo
lido não diz. Pergunta ao site.

### RN-09 — A soma só é pedida com a resposta afirmativa, e a tela se reabre para perguntar

Passadas as conferências, a tela pergunta **\* Confirma soma dos calculos <S/N> ? \ ***,
devolve o cursor ao campo da resposta e guarda o que conferiu: o grupo e as seis datas de
cálculo. Para perguntar, ela **reabre a si mesma** — não passa para tela nenhuma. Na
apresentação seguinte, só a resposta **S** segue para o registro; qualquer outra resposta
limpa a pergunta e devolve a tela ao começo da conferência, sem registrar nada. Se o grupo
ou alguma das seis datas tiver mudado depois da pergunta, a resposta é descartada e a
conferência recomeça — e a tela pergunta de novo.

[?] A guarda da resposta compara o grupo e as seis datas de cálculo, mas não as datas de
início: redigitadas depois da pergunta, elas não invalidam a resposta — e, ainda assim, são
substituídas pelas do cadastro antes de a tela compor o pedido. Ou o operador não deveria
poder editar essas datas depois da pergunta, ou a guarda deveria incluí-las. Pergunta ao
site.

### RN-10 — Um pedido de atualização já em processamento recusa o pedido novo

Confirmada a soma, e antes de registrar, a tela procura na fila de pedidos de relatório um
pedido do mesmo relatório; achando um, avisa
**\* Atualizacao em processamento. Aguarde. \ ***, devolve o cursor ao campo da resposta e
não registra nada. O mesmo relatório não é pedido duas vezes enquanto o anterior não
terminar.

[?] A procura é posicionada com o número do pedido zerado e o status em branco, e o pedido
que a própria tela registra leva um número calculado (o último da fila mais um) e o status
em branco. Se a leitura alcança qualquer pedido pendente daquele relatório, a recusa vale;
se ela exigir a chave inteira do pedido, a recusa é praticamente inalcançável. O acervo lido
não define qual dos dois; não escolho um lado. Pergunta ao site.

[?] A mensagem fala de "atualização", e não do relatório — embora a tela irmã do mesmo menu,
que faz a mesma soma, avise "relatório em processamento". Se a diferença de texto é
intencional, o material lido não diz. Pergunta ao site.

### RN-11 — Confirmado, o pedido é registrado, a auditoria é gravada e o processamento é disparado

Com a resposta **S**, a tela compõe o bloco de parâmetro — a matrícula, o tipo de órgão, o
grupo e as seis datas de cálculo —, toma o número seguinte da fila de pedidos e registra o
pedido com o código do relatório de soma, esse número, a impressora, o tipo de órgão, a
estação, o ano, o mês e o dia da sessão e a matrícula de quem pede. Grava também um
lançamento na **auditoria**, com a operação de inclusão, a tela, o grupo, a matrícula, a
estação e a data e a hora. Em seguida entrega o processamento do relatório e mostra
**\* Arquivo sendo gerado \ ***, voltando a se apresentar. Quem soma e gera o arquivo é o
processamento disparado, não a tela.

[?] O processamento só é entregue à fila quando o produto em execução é o LINC; fora dele o
pedido fica registrado e o caminho lido não mostra o disparo. E o que o processamento faz
com o parâmetro — que é o que de fato soma os períodos — não está nos fontes desta jornada.
Pergunta ao site.

[?] O lançamento da auditoria é montado como inclusão, com o grupo e as seis datas no lugar
do registro anterior e o registro posterior em branco; não há cadastro da tela que ele
registre (o código do relatório não é um cadastro). O que esse antes e depois significa,
para quem audita, não está no material lido. Pergunta ao site.

### RN-12 — A consulta não grava nada

A tela não altera cadastro nenhum: ela **lê** o cadastro de telas, o do usuário, o dos
cálculos de estimativa e a fila de pedidos de relatório, e **grava dois registros** — a
auditoria e o pedido. Nenhum registro é alterado ou excluído. As operações de gravação e de
exclusão estão **declaradas** para os cinco cadastros que a tela enxerga — dez conjuntos de
instruções, cinco de gravação e cinco de exclusão —, mas a tela executa **duas**: a gravação
da auditoria e a do pedido; nenhuma exclusão. Declarar não é executar. Sem a resposta
afirmativa, nada disso acontece: a conferência e a pergunta só leem.

### RN-13 — O grupo informado não é conferido contra o grupo do usuário

A tela não compara o grupo informado com a coordenação regional escolar da sessão — e as
rotinas que ela chama também não: elas conferem se a tela está cadastrada e se o servidor
tem acesso àquela tela, operação por operação, e nunca olham o grupo. Nada, no caminho
lido, restringe o grupo ao vínculo de quem opera: quem tem acesso à tela pede a soma de
qualquer grupo que tenha cálculo cadastrado para a data.

[?] O vínculo que a entrada carrega — matrícula, coordenação regional escolar, tipo de órgão
e órgão filho — não é lido nesta jornada, e as rotinas que a tela chama também não o leem.
Se um limite de grupo deveria valer, ele não está no material lido. Pergunta ao site.

### RN-14 — A digitação dos 37 campos é editada, e o cursor volta ao campo recusado

O grupo e as 36 datas passam por edição numérica antes de qualquer leitura: campo em branco
vira zero, e o que não for número é recusado e a conferência não segue. A tela não confere
calendário: uma data impossível segue adiante e simplesmente não encontra cálculo. O cursor
volta ao campo recusado no grupo e nas 18 datas de **cálculo**; para as 18 datas de
**início**, a tela não define para onde devolvê-lo.

[?] O que a rotina de edição recusa, além do não numérico, não está no acervo lido: ela é
importada. E metade das datas não tem posição de cursor definida para quando a digitação é
recusada. Pergunta ao site.

### RN-15 — A tela não confere a situação do cálculo

Qualquer cálculo cadastrado para a data e para o grupo serve, seja qual for a sua marca de
situação: a tela lê essa marca junto com o cálculo, mas nunca a examina. Período ainda não
fechado é somado como qualquer outro — o que distingue esta tela das irmãs do mesmo menu que
mostram ou exigem o fechamento do período.

[?] O cadastro do cálculo tem uma marca de situação obrigatória que esta tela não confere. O
que essa marca significa em negócio e se só períodos fechados deveriam ser somados, o
acervo lido não diz — mas, numa tela irmã do menu, é ela que produz o aviso **FECHADO**.
Pergunta ao site.

### RN-16 — Ao abrir, a tela mostra o cabeçalho; a cada envio ele é apagado

Na abertura, a tela preenche a descrição do tipo de órgão e a data do sistema, que formam o
cabeçalho. A cada envio — antes de qualquer conferência e de qualquer leitura —, os três
campos de resultado da apresentação anterior (a descrição do tipo de órgão, a data do
sistema e a mensagem da tela) são apagados, e nenhum caminho da passagem de conferência os
repõe: uma recusa reapresenta a tela sem o cabeçalho da abertura.

### RN-17 — Falha de banco interrompe a operação

Todo acesso a dados testa o erro do banco: o erro de leitura vira uma ação de erro e o de
gravação, outra, ambas despachadas pela rotina de comunicação — a transação para ali, sem
completar o resto.

---

## Cenários BDD

```gherkin
Funcionalidade: Somar os cálculos do grupo e encomendar a impressão do resultado

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C848T

  Cenário: RN-01 — abertura da tela
    Dado que abro a tela C848T
    Então a operação vem marcada como consulta
    E eu não escolho a operação

  Cenário: RN-01 — operação diferente de consulta é recusada
    Dado que estou na tela C848T
    Quando envio com uma operação diferente da consulta
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da operação
    E nenhum cadastro é lido nesse caminho

  Cenário: RN-02 — grupo não informado
    Dado que deixo o grupo em branco
    Quando envio
    Então vejo "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nenhum cálculo é lido

  Cenário: RN-03 — nenhuma data de cálculo informada
    Dado que deixo as seis datas de cálculo em branco
    Quando envio
    Então vejo "* Informe data de calculo *"
    E o cursor volta à primeira data de cálculo
    E nenhum cálculo é lido

  Cenário: RN-04 — a tela trata seis períodos
    Dado que informo o grupo e preencho uma, algumas ou as seis datas de cálculo
    Quando envio
    Então só os períodos preenchidos são conferidos
    E cada um deles é tratado na ordem em que aparece na tela

  Cenário: RN-05 — a data de início digitada é substituída pela do cálculo
    Dado que digito uma data de início diferente da do cálculo cadastrado
    Quando envio
    Então a tela mostra a data de início do cálculo cadastrado

  Cenário: RN-06 — data de cálculo sem cálculo cadastrado
    Dado que informo uma data de cálculo sem cálculo para o grupo
    Quando envio
    Então vejo "* Calculo nao cadastrado para esta data *"
    E o cursor volta ao dia da data de cálculo que falhou
    E nada é registrado

  Cenário: RN-07 — impressora não informada
    Dado que informo o grupo e as datas de cálculo, todas com cálculo cadastrado
    E deixo a impressora em branco
    Quando envio
    Então vejo "* Informe a impressora *"
    E o cursor volta ao campo da impressora
    E nada é registrado

  Cenário: RN-07 — impressora apagada depois da pergunta
    Dado que a tela já perguntou "* Confirma soma dos calculos <S/N> ? *"
    Quando apago a impressora e respondo S
    Então o pedido é registrado com a impressora em branco

  Cenário: RN-08 — usuário sem e-mail cadastrado
    Dado que o meu cadastro de usuário está sem e-mail
    Quando envio a consulta
    Então vejo "* Usuario sem e-mail cadastrado *"
    E a conferência não segue

  Cenário: RN-09 — conferência e pergunta de confirmação
    Dado que informo o grupo, até seis datas de cálculo com cálculo cadastrado e a impressora
    Quando envio
    Então cada data de início vem do cálculo cadastrado
    E a tela se reabre e pergunta "* Confirma soma dos calculos <S/N> ? *"
    E nenhum registro foi gravado ainda

  Cenário: RN-09 — resposta diferente de S volta ao começo
    Dado que a tela perguntou "* Confirma soma dos calculos <S/N> ? *"
    Quando respondo N, ou deixo a resposta em branco
    Então a pergunta é limpa
    E a conferência recomeça
    E nada é registrado

  Cenário: RN-09 — grupo ou datas mudados depois da pergunta
    Dado que a tela já perguntou e eu respondo S
    E mudo o grupo ou uma das seis datas de cálculo
    Quando envio
    Então a resposta é descartada
    E a conferência recomeça
    E a tela pergunta de novo

  Cenário: RN-10 — atualização do mesmo relatório já em processamento
    Dado que há um pedido do mesmo relatório ainda em processamento
    Quando confirmo a soma com S
    Então vejo "* Atualizacao em processamento. Aguarde. *"
    E o cursor volta ao campo da resposta
    E nada é registrado

  Cenário: RN-11 — pedido registrado, auditoria gravada e processamento disparado
    Dado que informei o grupo, as datas de cálculo e a impressora
    E respondi S à confirmação
    Quando envio
    Então o pedido é registrado na fila com o código do relatório de soma e o número seguinte da fila
    E o pedido leva a impressora, o grupo, o órgão, a matrícula, a estação e a data da sessão
    E fica na auditoria um lançamento com a operação de inclusão, a tela, o grupo, a matrícula, a estação, a data e a hora
    E o processamento que gera o arquivo é disparado
    E vejo "* Arquivo sendo gerado *"

  Cenário: RN-12 — a consulta não confirmada não grava nada
    Dado que informo o grupo, as datas de cálculo e a impressora
    E ainda não respondi a confirmação
    Quando a tela confere e mostra as datas de início
    Então nenhum pedido é registrado
    E nenhum lançamento de auditoria é gravado
    E nenhum registro é alterado ou excluído

  Cenário: RN-13 — o grupo informado não é conferido contra o da sessão
    Dado que informo um grupo diferente da coordenação regional escolar da minha sessão
    Quando envio
    Então a tela não recusa por isso
    E a autorização que ela consulta confere o meu acesso à tela, e não o grupo

  Cenário: RN-14 — digitação não numérica
    Dado que digito letras no grupo ou em uma das datas
    Quando envio
    Então a conferência é recusada antes de ler qualquer cadastro
    E o cursor volta ao campo recusado

  Cenário: RN-14 — data de início recusada não tem posição de cursor
    Dado que digito algo que não é número em uma data de início
    Quando envio
    Então a conferência é recusada
    E a tela não define para onde devolver o cursor

  Cenário: RN-15 — período ainda não fechado também é somado
    Dado que o cálculo existe para uma das datas de cálculo
    E o período não está marcado como fechado
    Quando informo essa data e confirmo a soma com S
    Então a tela aceita e o pedido é registrado

  Cenário: RN-16 — o cabeçalho da abertura é apagado a cada envio
    Dado que a abertura mostrou a descrição do tipo de órgão e a data do sistema
    Quando envio uma conferência que é recusada
    Então os dois campos não ficam em tela
    E a recusa é reapresentada sem o cabeçalho

  Cenário: RN-17 — falha de banco durante a operação
    Dado que a leitura de um cadastro ou a gravação do pedido falha
    Quando envio
    Então a transação é interrompida com a mensagem de erro do sistema
    E a operação não é considerada concluída
```
