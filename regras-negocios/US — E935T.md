# US — E935T — Manter as justificativas de cartão

## Estória

Como **servidor da coordenação regional de ensino (CRE)**, quero **manter a lista dos
motivos que podem justificar o cancelamento e o bloqueio do cartão de um aluno**,
para que **o motivo fique registrado no cartão e a secretaria e a auditoria possam
conferir depois por que aquele cartão foi cancelado ou bloqueado**.

A justificativa é o motivo oficial do cartão: quem cancela ou bloqueia informa o
código do motivo e o sistema vai buscá-lo nesta lista, levando a descrição encontrada
para o registro do cartão. Não achando o motivo, aquela operação não fecha, com o
aviso de que a justificativa não está cadastrada. É por isso que a lista é pequena e
mantida por uma tela só: motivo que não estiver aqui não pode ser usado no atendimento
do cartão, e a descrição escrita aqui é o que a escola e a auditoria vão ler depois.

## Contexto

Jornada S000M → E000M → E900M → E935T.

Ator: servidor da CRE — mantém a lista de motivos (justificativas) que o cancelamento
e o bloqueio de cartão podem usar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada são menus — a `E000M`, com 11 opções, e a
`E900M`, com 9 — e não telas encadeadas: nenhuma delas deixa registro nem operação
pronta para esta tela. A tela abre em consulta, e é o modo informado na passagem que
decide entre consultar e alterar (RN-04).

O cadastro de justificativas é mantido só por esta tela: as telas de cartão apenas o
consultam. A tela termina nela mesma — não abre outra tela por opção nenhuma (RN-11).

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — A justificativa é o motivo que o cancelamento e o bloqueio do cartão exigem

A justificativa é o motivo que precisa estar cadastrado para que um cartão seja
cancelado ou bloqueado. Quem opera o cartão informa o código do motivo; o sistema
procura esse código nesta lista e leva a descrição encontrada para o registro do
cartão. Não achando o motivo, aquela operação é recusada, com o aviso de que a
justificativa não está cadastrada. Ou seja: motivo que não estiver aqui não pode ser
usado lá.

### RN-02 — O que a tela mantém: código e descrição, em 14 linhas

Cada justificativa tem **2 dados**: o **código**, de 2 dígitos, informado por quem
opera, e a **descrição**, de até 40 caracteres, de preenchimento obrigatório no
dicionário de dados. A tela mostra **14 justificativas por vez**, cada linha com o
código, a descrição e a situação. O cadastro está dimensionado para **100 registros** —
isto é **capacidade** (o máximo esperado no dimensionamento), não a quantidade
cadastrada.

O código passa pela conferência numérica — em branco vale zero, e o que não for número
não chega ao cadastro — e o **código zero não é uma justificativa utilizável**: a tela
o trata como "não informado", tanto na conferência quanto na gravação.

[?] A chave do cadastro admite códigos repetidos no dicionário de dados, mas esta tela
recusa incluir um código já existente e nunca grava o código zero. Se existe um
registro de código zero, ou repetido, ele só pode ter vindo de carga, de conversão ou
de versão anterior do sistema. Pergunta ao site.

### RN-03 — Ao abrir, a tela lista as justificativas e avisa quando não há nenhuma

Ao entrar, a tela percorre o cadastro e preenche as 14 linhas com as justificativas
existentes. Não encontrando nenhuma, avisa **\* Nao existem justificativas
cadastradas \*** e deixa o cursor no campo do código da primeira linha. O cabeçalho
mostra a descrição do órgão da sessão e a data do sistema, e há uma linha de
mensagens.

[?] O que a lista mostra ao abrir depende de como a leitura posiciona o cadastro: a
posição inicial guardada na sessão é zero, e a tela não grava o código zero. Se a
leitura parte do começo do cadastro, a lista abre na primeira justificativa; se ela
procura exatamente o código guardado, a lista só abriria quando existisse uma
justificativa de código zero. Pergunta ao site.

[?] A tela mostra 14 justificativas e o programa não tem opção de passar para as
seguintes. Com mais de 14 cadastradas, como o operador alcança as demais — por tecla
de rolagem tratada fora do programa, ou não alcança — é pergunta ao site.

### RN-04 — O modo só admite alteração e consulta, e em branco a tela assume consulta

A tela tem um campo de modo. Aberta sem modo informado, ela assume **consulta**. Os
modos aceitos são **alteração** e **consulta**; informado qualquer outro, o sistema
recusa com **\* Opcao nao disponivel. Use ALT ou CON \***, devolve o cursor ao campo do
modo e não grava nada. O modo usado fica guardado na sessão: enquanto o campo vier em
branco, a tela continua no último modo.

[?] A mensagem manda usar ALT e CON, mas a conferência aceita os códigos internos de
alteração e de consulta. Onde a máscara da tela traduz o rótulo que o operador digita
no código que o programa confere não está no acervo — se não houver tradução, quem
digitar ALT ou CON é recusado sempre. É pergunta ao site.

### RN-05 — A situação da linha decide a operação, e a tela não exclui

Cada linha traz a **situação**: **I** manda incluir e **A** manda alterar. Linha com o
código zerado, ou com situação diferente de I e A, passa em silêncio: não gera
operação, não gera recusa e não grava nada. A tela **não exclui** justificativa — não
há situação nem caminho que leve à exclusão.

### RN-06 — Inclusão recusa código já cadastrado e exige a descrição

Na situação **I**, o sistema procura o código informado no cadastro. Se já existe uma
justificativa com aquele código, a inclusão é recusada com **\* Justificativa ja
cadastrada \*** e o cursor vai para a coluna da situação. Se a descrição estiver em
branco, a recusa é **\* Informe a descricao \*** e o cursor vai para a coluna da
descrição. Passando nas duas conferências, a justificativa é criada no cadastro com o
código e a descrição informados, e a operação fica registrada na auditoria.

[?] A recusa da linha não é reconferida pela passagem que grava: a passagem de
conferência marca a recusa num indicador próprio e a de gravação decide apenas pelo
modo e pela situação da linha. O lote não traz a rotina de comunicação nem o controle
de cópias da página, então não dá para afirmar se, numa página com mais de uma linha,
a recusa de uma impede a gravação. Pergunta ao site.

### RN-07 — Alteração exige justificativa cadastrada e exige a descrição

Na situação **A**, a justificativa precisa existir: não existindo, o sistema recusa com
**\* Justificativa nao cadastrada \*** e o cursor vai para a coluna da situação. A
descrição também precisa ser informada: em branco, a recusa é **\* Informe a
descricao \***. Passando nas duas, o registro é travado e regravado com a nova
descrição, e a operação fica registrada na auditoria. O código não muda: ele é a chave
que identifica a justificativa.

[?] A alteração percorre o cadastro pela chave informada e regrava enquanto encontrar
registros com aquele código. A chave admite códigos repetidos no dicionário, embora
esta tela recuse incluir um código já existente; se houver repetição vinda de outro
caminho, quantos registros a alteração reescreve é pergunta ao site.

### RN-08 — Inclusão e alteração ficam registradas na auditoria

Além da justificativa, a inclusão e a alteração gravam um registro na trilha de
auditoria das telas, com o cadastro auditado, a tela de origem, a operação (inclusão ou
alteração), o conteúdo anterior, o conteúdo posterior, a matrícula do funcionário, o
terminal, o dia, o mês, o ano e a hora da sessão, o número do processo, o tipo de órgão
e a CRE. O conteúdo auditado é o par código e descrição da justificativa. Na inclusão o
conteúdo anterior vai em branco; na alteração vão a descrição anterior e a nova.

[?] O código de manutenção do registro de auditoria sai com o mesmo valor nos dois
casos — inclusão e alteração —, embora o campo de operação distinga as duas. Qual dos
dois o consumidor da auditoria lê é pergunta ao site.

[?] A trilha da inclusão fica sob uma condição de estado que a própria rotina de
gravação limpa antes de gravar: pelo que o lote mostra, ela é sempre gravada. Se existe
um caso em que esse estado chega preenchido e a inclusão fica sem a trilha, o acervo
não diz qual. Pergunta ao site.

### RN-09 — A consulta não grava nada

Em consulta, a tela lista e para: nenhuma justificativa é incluída ou alterada e
nenhuma trilha de auditoria é gerada. É o modo em que a tela abre quando nenhum modo
lhe é informado.

### RN-10 — A operação só acontece se a autorização do servidor liberar

Antes de mostrar a lista, a tela confere a matrícula, a estação e o cadastro da própria
tela, e confere se aquele código de acesso alcança a tela. Na confirmação, confere de
novo o cadastro da tela e, no cadastro de telas por código de acesso — que guarda, por
operação, se a inclusão, a alteração, a exclusão e a consulta estão liberadas —, confere
a operação pedida, levando em conta a matrícula, o código de acesso, o privilégio, o
tipo de órgão e a CRE da sessão. Não estando liberada, a operação não é validada nem
gravada, e o servidor vê a recusa de acesso à operação.

### RN-11 — Chegando com a tela de retorno preenchida, a manutenção é abandonada

O registro da tela tem um campo de **tela de retorno**, que é o dado que a rota usa para
levar o servidor a outra tela sem passar por menu. Chegando preenchido, a manutenção é
abandonada: nada é validado, nada é gravado e o servidor é levado à tela indicada.

[?] Nada nesta jornada preenche o campo de tela de retorno, e o lote não diz quem o
preenche nem para onde ele levaria. Pergunta ao site.

### RN-12 — A recusa de destino inválido não é alcançável por esta tela

A recusa de **destino inválido** — a distribuição automática entre destinos —, que a
ficha estrutural lista entre as mensagens desta tela, não é produzida por ela: o modo
de distribuição externa, de que a recusa depende, é limpo imediatamente antes de
montar o registro que a gravação usa. Pelo caminho desta tela, a recusa não sai.

[?] A ficha do grafo lista essa recusa para esta tela, e o programa limpa o campo antes
de usá-lo: divergência entre a ficha e o comportamento, a confirmar com quem mantém o
grafo. E o lote não deixa ver se a comparação de chaves que dispara o aviso genérico de
distribuição pode ocorrer aqui. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter as justificativas de cartão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E935T

  Cenário: A tela lista as justificativas cadastradas
    Dado que existem justificativas cadastradas
    Quando abro a E935T
    Então vejo as justificativas, com código, descrição e situação, até 14 por vez
    E nada é gravado

  Cenário: Nenhuma justificativa cadastrada
    Dado que não existe nenhuma justificativa cadastrada
    Quando abro a E935T
    Então vejo a mensagem "* Nao existem justificativas cadastradas *"
    E o cursor fica no campo do código da primeira linha

  Cenário: Modo não informado abre em consulta
    Dado que não informei o modo
    Quando abro a E935T
    Então a tela assume consulta
    E nada é gravado

  Cenário: Modo indisponível
    Quando informo um modo diferente de alteração e de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo do modo
    E nada é gravado

  Cenário: Inclusão de uma justificativa nova
    Dado que estou na E935T em alteração
    Quando informo um código ainda não cadastrado, a descrição e a situação I
    Então a justificativa é criada no cadastro
    E a operação fica registrada na auditoria

  Cenário: Inclusão de justificativa que já existe é recusada
    Dado que já existe uma justificativa com o código informado
    Quando confirmo a situação I
    Então vejo a mensagem "* Justificativa ja cadastrada *"
    E o cursor fica na coluna da situação
    E nada é gravado

  Cenário: Justificativa sem descrição é recusada
    Dado que deixei a descrição em branco
    Quando confirmo a inclusão ou a alteração
    Então vejo a mensagem "* Informe a descricao *"
    E o cursor fica na coluna da descrição
    E nada é gravado

  Cenário: Alteração da descrição de uma justificativa
    Dado que a justificativa existe
    Quando informo a nova descrição e a situação A
    Então a descrição é regravada
    E a auditoria guarda a descrição anterior e a nova

  Cenário: Alteração de justificativa não cadastrada é recusada
    Dado que a justificativa informada não existe
    Quando confirmo a situação A
    Então vejo a mensagem "* Justificativa nao cadastrada *"
    E o cursor fica na coluna da situação
    E nada é gravado

  Cenário: Linha sem código ou com situação desconhecida é ignorada
    Dado que deixei o código em branco, ou informei uma situação diferente de I e A
    Quando a tela processa as linhas
    Então aquela linha não gera operação nenhuma
    E não vejo mensagem

  Cenário: A tela não exclui justificativa
    Dado que a justificativa está cadastrada
    Quando tento excluí-la pela E935T
    Então nada é excluído
    E a justificativa continua cadastrada

  Cenário: Consulta não grava nada
    Dado que estou na E935T em consulta
    Quando a tela processa as linhas
    Então nenhuma justificativa é incluída ou alterada
    E nenhuma trilha de auditoria é gerada

  Cenário: Operação não liberada pela autorização do servidor
    Dado que a minha autorização de código de acesso não libera a operação pedida
    Quando confirmo a linha
    Então a linha não é validada e nada é gravado
    E vejo a recusa de acesso à operação

  Cenário: Chegando com a tela de retorno preenchida
    Dado que a transação chega com o campo de tela de retorno preenchido
    Quando confirmo
    Então a manutenção é abandonada e nada é gravado
    E sou levado à tela indicada
```
