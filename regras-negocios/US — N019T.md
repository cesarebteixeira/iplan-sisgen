# US — N019T — Posição da nota fiscal na sequência do processo

## Estória

Como **servidor da CRE**, quero **dar posição a uma nota fiscal dentro da sequência do
processo**, para que **as notas daquele processo fiquem numa ordem única e conhecida, e as
telas que leem a nota encontrem a sequência em ordem**.

A nota fiscal de um processo carrega, além dos seus próprios dados, a posição que ocupa na
ordem das notas daquele processo. É essa ordem que outras telas leem quando trabalham com
uma nota do processo; sem uma tela que a mantenha, as notas ficariam sem posição ou
repetindo a posição umas das outras, e não haveria por onde corrigir. Por isso esta tela não
cria nem apaga nota: ela só diz onde cada nota fica.

## Contexto

Jornada S000M → N000M → N050M → N019T.

Ator: servidor de CRE — diz onde a nota fiscal fica na ordem das notas do processo e mantém
a numeração dessa ordem.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Os dois menus do caminho — `N000M` e `N050M` — só encaminham: **não deixam processo nem
nota na sessão, e não informam o modo da página**. O processo e a nota com que a tela
trabalha são informados nela mesma, e ela repõe o que guardou da última consulta; não
havendo nada guardado, ela completa os primeiros grupos do processo com o que o cadastro do
órgão do servidor traz. Como os menus não passam modo, a tela chega sempre sem modo
informado e abre em consulta — é o próprio padrão da tela que decide isso, não a tela
anterior. O que a tela usa da sessão — matrícula, acesso, privilégio, secretaria e CRE — é o
que a entrada deixou, e a tela apenas o repassa às conferências de segurança e o grava na
auditoria.

A tela mostra o número do processo em quatro grupos, o número da nota fiscal, a posição da
nota, uma marca de atualização da sequência, o número da nota que vai anteceder a nota
trabalhada, o modo da página e o aviso da operação.

---

## Regras de negócio

### RN-01 — A tela mantém a posição da nota fiscal na sequência do processo

Cada nota fiscal de um processo guarda a posição que ocupa na ordem das notas daquele
processo, de **1 a 999**. Esta tela é a que coloca a nota na posição desejada e reescreve a
sequência das demais notas do processo. Ao gravar, ela escreve **apenas** a posição: nenhum
outro dado da nota é alterado, e ela não cria nem apaga nota — só reordena as que já
existem. O cadastro onde ela grava é o mesmo que dezenas de outras telas leem, e sua
capacidade declarada é de **29 milhões** de notas — capacidade de dimensionamento, não o
volume existente.

[?] O que a ordem das notas decide na prática — se é a ordem de liquidação, a de conferência
ou outra — não está no acervo: a tela só a numera e a reordena. Pergunta ao site.

[?] A posição tem três dígitos. Com 999 notas já posicionadas no processo não há para onde
deslocar a última, e o acervo não mostra o que o sistema faz nesse limite. Pergunta ao site.

### RN-02 — O processo é um número de catorze dígitos, informado em quatro grupos

O processo é identificado por um número de **catorze** dígitos, e a tela o recebe em quatro
grupos: dois de dois dígitos, um de seis e um de quatro. Ao gravar, os quatro grupos são
juntados no número de catorze dígitos que o cadastro usa. Os dois primeiros grupos vêm do
cadastro do órgão do servidor: o primeiro é o código da secretaria daquele órgão; o segundo
é o código da CRE do servidor, preenchido quando o cadastro do órgão assim o registra. Os
outros dois grupos o servidor informa. A nota fiscal, dentro do processo, é identificada
pelo seu número de **nove** dígitos.

### RN-03 — Ao abrir, a tela repõe a última consulta e completa o processo com o órgão

A tela guarda consigo o processo, o número da nota fiscal e a posição da última consulta
bem-sucedida, e os repõe nos campos ao abrir, para que o servidor continue de onde parou.
Não havendo consulta anterior, ela preenche os dois primeiros grupos do processo com o que o
cadastro do órgão do servidor traz, como na regra anterior — e o que fica no segundo grupo é
o código da CRE da sessão. Quando uma consulta é recusada, a tela esquece o que guardara.

### RN-04 — A tela abre em consulta, e o modo da página só admite consulta e alteração

A tela se apresenta no modo de **consulta**: chegando sem modo informado — que é como os
menus do caminho a abrem —, é o modo de consulta que fica no campo. Os dois modos que ela
aceita são o de **alteração** e o de **consulta**. Com qualquer outro valor, ela recusa com
* Operacao nao disponivel. Use ALT ou CON *, devolvendo o cursor ao campo do modo, e não
valida nem grava nada.

[?] A recusa manda usar **ALT** e **CON**, mas essas duas palavras não são valor nenhum
aceito pelo sistema: o que a tela compara são os códigos internos de alteração e de
consulta, e é com o código de consulta que ela mesma preenche o campo quando ele vem em
branco. Ou o formulário da tela traduz o que o servidor digita, ou a recusa indica valores
que o sistema não reconhece. Pergunta ao site.

### RN-05 — Os campos de número passam pela edição numérica antes de qualquer consulta

Os **sete** campos de número da tela — os quatro grupos do processo, o número da nota
fiscal, a posição e o número da nota que vai anteceder — passam por uma edição numérica
antes de qualquer procura no cadastro: o que estiver em branco vira zero, os zeros à
esquerda caem e o que não for número é recusado, com o cursor de volta ao campo. O que não
passa por essa edição não chega a ser procurado no cadastro.

### RN-06 — A consulta exige o processo cadastrado e do mesmo grupo do servidor

Consultando, a tela procura o processo pelo número informado. O processo é dado por
cadastrado quando existe **pelo menos uma nota fiscal** dele: a tela lê a primeira nota do
processo e, não achando, recusa com * Processo nao cadastrado *, com o cursor no grupo do
processo, e esquece o que guardara da consulta anterior. Achando, ela compara o grupo do
processo com o grupo do servidor: se a sessão tem uma CRE e ela é diferente da CRE do
processo, a recusa é * Usuario sem acesso ao grupo deste processo *, também com o cursor no
grupo do processo. Quando a sessão não tem CRE, essa comparação não é feita.

### RN-07 — A consulta numera as notas do processo que ainda não têm posição — e grava

Ainda na consulta, antes de mostrar a nota, a tela percorre as notas daquele processo e
**grava** a posição nas que estão sem posição: a primeira recebe 1, a seguinte 2, e assim
por diante, até a primeira nota que já tem posição — o laço para ali. Isso é gravação de
verdade, feita na consulta e **sem deixar rastro na auditoria**, ao contrário da alteração.
Se a nota consultada não existir, a numeração já terá sido gravada antes da recusa.

[?] A numeração da consulta grava a nota sem deixar rastro na auditoria, enquanto a
alteração sempre deixa. Se essa assimetria é intencional, pergunta ao site.

### RN-08 — A consulta exige a nota fiscal no processo

Depois de numerar, a tela procura a nota informada **no processo informado**. Não achando, a
recusa é * Nota nao cadastrada neste processo *, com o cursor no campo do número da nota
fiscal, e a tela esquece o que guardara da consulta anterior. Achando, ela guarda o
processo, a nota e a posição lidos — e é essa guarda que habilita a alteração.

### RN-09 — A alteração exige uma consulta antes

Para alterar, o servidor precisa ter consultado, na mesma sessão, **o mesmo processo e a
mesma nota** que estão nos campos. A tela compara o processo e a nota informados com os que
guardou da consulta; não sendo os mesmos, a recusa é * Consulte antes de atualizar *, com o
cursor no modo da página, e nada é gravado. É a consulta que escolhe a nota a reordenar.

### RN-10 — A alteração exige exatamente uma das duas formas de reordenar

A alteração aceita duas formas de dizer onde a nota vai ficar: **marcar a atualização da
sequência**, ou **informar o número de uma nota que vai anteceder** a nota trabalhada. As
duas ao mesmo tempo são recusadas com * Informe apenas uma atualizacao da sequencia *
(cursor no campo da marca); nenhuma das duas é recusada com * Informe uma atualizacao da
sequencia * (mesmo cursor). Pela tela, não se confirma uma alteração sem dizer onde a nota
fica.

### RN-11 — A nota que antecede precisa existir no processo e não pode ser a própria nota

Quando o servidor informa o número da nota que vai anteceder, essa nota precisa existir
naquele processo: não existindo, a recusa é * Nota nao cadastrada no processo *, com o
cursor no campo da nota anterior. E ela não pode ser a própria nota que está sendo
reordenada — nesse caso a recusa é * Atualizacao da sequencia invalida *, também com o
cursor no campo da nota anterior. Uma nota não antecede a si mesma.

### RN-12 — Marcar a atualização da sequência põe a nota em primeiro lugar

Marcando a atualização da sequência — e deixando em branco a nota que antecederia —, a nota
trabalhada passa a ocupar a **posição 1** do processo e as demais notas do processo andam
para as posições seguintes. Ao fim, a tela mostra o aviso * ** Sequencia Atualizada ** * e
apresenta a nota com a sua nova posição.

[?] Depois de marcar a atualização, a tela reescreve a sequência duas vezes sobre os mesmos
registros, por dois caminhos diferentes: num deles a nota é numerada a partir de 1; no
outro, a posição é recalculada a partir da posição da nota seguinte. O acervo não permite
dizer qual das duas numerações o servidor vê ao fim. Pergunta ao site.

### RN-13 — Informar a nota anterior coloca a nota logo depois dela

Informando o número da nota que vai anteceder, a nota trabalhada passa a ocupar a posição
**imediatamente seguinte** à daquela nota, e as notas que estavam dessa posição em diante
andam uma posição para trás. A nota trabalhada não é deslocada duas vezes: ela fica fora do
deslocamento. Ao fim, o mesmo aviso de sequência atualizada e a nova posição à mostra.

[?] Por este caminho, o acervo **não grava a posição nova na própria nota trabalhada**: as
gravações deslocam as demais notas, e a comparação que encerra o deslocamento é feita sobre
a posição da nota trabalhada — de modo que ela nunca chega a ser gravada com posição nova.
Além disso, o deslocamento compara a posição de cada nota com um valor que ele mesmo
atualiza durante a leitura, e não com a posição da nota indicada. O resultado que o servidor
vê não se pode determinar pelo fonte: ou a nota fica com a posição antiga e repete a posição
de outra, ou o deslocamento se aplica a notas erradas. Pergunta ao site.

### RN-14 — Toda alteração confirmada deixa rastro na auditoria

Cada nota deslocada pela alteração deixa um registro na auditoria, com: o cadastro auditado
(a nota fiscal), a operação de alteração, a imagem da nota antes e depois (com a posição
nova) e o contexto da sessão — matrícula, acesso, secretaria, CRE, órgão, terminal, data e
hora, número do processo e número da transação. As gravações da consulta que numera, como
dito, não deixam rastro.

### RN-15 — A tela confirma a alteração e volta a ela mesma

Terminada a alteração, a tela mostra o aviso * ** Sequencia Atualizada ** * e se apresenta de
novo, já com o número da nota consultada e a posição nova nos campos. O servidor não é
levado a outra tela.

### RN-16 — As recusas interrompem a tela antes de qualquer gravação

Cada recusa acima é apresentada com a mensagem e o cursor no campo culpado, e o
processamento da tela termina ali: nada é gravado na passagem de alteração.

[?] A interrupção depois da recusa não se prova só com o fonte da tela: o acervo desta
jornada não contém a rotina global que marcaria esse erro, e é ela que a tela consulta antes
de seguir para a gravação. Se essa rotina não marcar o erro, uma tela recusada ainda poderia
seguir para a passagem de gravação. Pergunta ao site.

### RN-17 — Nada é processado sem a conferência de sessão, de tela e de operação

Antes de validar e antes de gravar, a tela confere a sessão e a autorização. A conferência
exige que o servidor esteja no terminal da sessão — se não estiver, o acesso é encerrado —,
que a tela esteja registrada no cadastro de telas e que o código de acesso tenha, para esta
tela, a operação pretendida: a **alteração**, no modo de alteração. Sem isso a tela não
valida, não grava e devolve o servidor ao menu, com * Tela nao disponivel *,
* Acesso negado para esta matricula * ou * Acesso negado para esta operacao *.

[?] A **consulta** não é conferida contra a permissão de consulta do código de acesso: quem
tem a tela registrada consulta, mesmo que a consulta não esteja liberada para o seu código
de acesso. Pergunta ao site se é assim mesmo.

### RN-18 — Prefixo de tela preenchido desvia a tela

Se a transação chega com o campo do prefixo de tela preenchido, a conferência de rota
interrompe o processamento e leva o servidor para a tela indicada nesse prefixo — nenhum
campo é validado e nada é gravado nesta tela.

[?] O mecanismo está no acervo — a rota devolve o prefixo como a próxima tela —, mas não
quem preenche esse prefixo nas transações que chegam a esta tela. Pergunta ao site.

### RN-19 — A recusa de destino inválido não é alcançada por esta tela

A rotina de distribuição automática entre destinos tem uma recusa própria — **destino
inválido** —, que a ficha da tela lista entre as mensagens. O ramo só roda com o modo de
distribuição automática preenchido, e a tela limpa esse campo imediatamente antes dos
pontos em que ele poderia disparar. Por esta tela, portanto, essa mensagem não é
apresentada.

[?] A ficha da tela atribui a mensagem a esta tela, mas o fonte não alcança o ramo:
divergência entre a ficha e o comportamento, a confirmar com quem mantém o grafo.

---

## Cenários BDD

```gherkin
Funcionalidade: Posição da nota fiscal na sequência do processo

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o acesso, o privilégio, a secretaria, a CRE e o órgão
    E tenho acesso à tela N019T

  Cenário: A tela mantém a posição da nota na sequência do processo
    Dado que estou na tela N019T
    Quando consulto uma nota fiscal de um processo
    Então vejo a posição que essa nota ocupa na ordem das notas do processo
    E a posição vai de 1 a 999

  Cenário: Ao gravar, só a posição da nota é escrita
    Dado que confirmei uma reordenação na N019T
    Quando a gravação termina
    Então apenas a posição da nota foi alterada
    E nenhum outro dado da nota mudou
    E nenhuma nota foi incluída nem excluída

  Cenário: O processo é informado em quatro grupos
    Dado que estou na tela N019T
    Quando o processo é apresentado
    Então vejo o número do processo em quatro grupos, que formam um número de catorze dígitos
    E os dois primeiros grupos vêm preenchidos pelo cadastro do órgão do meu vínculo

  Cenário: Ao abrir, a tela repõe a última consulta
    Dado que já consultei um processo e uma nota nesta sessão
    Quando volto à tela N019T
    Então os campos já vêm com aquele processo, aquela nota e aquela posição

  Cenário: Ao abrir sem consulta anterior, o processo é completado pelo órgão
    Dado que ainda não consultei nada nesta sessão
    Quando abro a tela N019T
    Então os dois primeiros grupos do processo já vêm preenchidos com o que o cadastro
      do meu órgão traz
    E os dois últimos grupos vêm em branco, para eu informar

  Cenário: A tela abre em consulta
    Dado que abro a tela N019T sem informar o modo
    Quando a tela é apresentada
    Então o modo que vejo é o de consulta

  Cenário: Modo da página não admitido
    Dado que estou na tela N019T
    Quando informo um modo que não é o de alteração nem o de consulta
    Então vejo "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: Campo de número que não é número
    Dado que estou na tela N019T
    Quando informo letras em um dos campos de número
    Então a tela recusa o campo antes de consultar o cadastro
    E o cursor volta ao campo

  Cenário: Processo não cadastrado
    Dado que estou na tela N019T no modo de consulta
    Quando o processo informado não tem nenhuma nota fiscal
    Então vejo "* Processo nao cadastrado *"
    E o cursor fica no grupo do processo
    E nada é gravado
    E a tela esquece o processo que guardara da consulta anterior

  Cenário: Servidor de outro grupo
    Dado que estou na tela N019T no modo de consulta
    E que a minha sessão tem uma CRE
    Quando o processo informado pertence a outro grupo
    Então vejo "* Usuario sem acesso ao grupo deste processo *"
    E o cursor fica no grupo do processo
    E nada é gravado

  Cenário: A consulta numera as notas que estavam sem posição
    Dado que estou na tela N019T no modo de consulta
    E que o processo tem notas sem posição
    Quando consulto o processo
    Então as notas sem posição recebem 1, 2, 3 e assim por diante, a partir da primeira
    E a numeração para na primeira nota que já tinha posição
    E as posições ficam gravadas, sem registro na auditoria

  Cenário: Nota não cadastrada no processo
    Dado que estou na tela N019T no modo de consulta
    Quando informo uma nota que não existe naquele processo
    Então vejo "* Nota nao cadastrada neste processo *"
    E o cursor fica no campo do número da nota fiscal
    E nada é gravado
    E a tela esquece o processo que guardara da consulta anterior

  Cenário: Alteração sem consulta antes
    Dado que estou na tela N019T no modo de alteração
    Quando o processo e a nota informados não são os que consultei
    Então vejo "* Consulte antes de atualizar *"
    E o cursor fica no campo do modo
    E a nota trabalhada não é gravada

  Cenário: Alteração sem dizer onde a nota fica
    Dado que estou na tela N019T no modo de alteração
    E que consultei o processo e a nota
    Quando não marco a atualização da sequência nem informo a nota anterior
    Então vejo "* Informe uma atualizacao da sequencia *"
    E o cursor fica no campo da marca
    E nada é gravado

  Cenário: As duas formas de reordenar informadas ao mesmo tempo
    Dado que estou na tela N019T no modo de alteração
    E que consultei o processo e a nota
    Quando marco a atualização da sequência e também informo uma nota anterior
    Então vejo "* Informe apenas uma atualizacao da sequencia *"
    E o cursor fica no campo da marca
    E nada é gravado

  Cenário: A nota anterior não existe no processo
    Dado que estou na tela N019T no modo de alteração
    E que consultei o processo e a nota
    Quando informo, como nota anterior, uma nota que não existe naquele processo
    Então vejo "* Nota nao cadastrada no processo *"
    E o cursor fica no campo da nota anterior
    E nada é gravado

  Cenário: A nota anterior é a própria nota trabalhada
    Dado que estou na tela N019T no modo de alteração
    E que consultei o processo e a nota
    Quando informo, como nota anterior, a própria nota que estou reordenando
    Então vejo "* Atualizacao da sequencia invalida *"
    E o cursor fica no campo da nota anterior
    E nada é gravado

  Cenário: A nota vai para a primeira posição
    Dado que estou na tela N019T no modo de alteração
    E que consultei o processo e a nota
    Quando marco a atualização da sequência e confirmo
    Então a nota passa a ocupar a posição 1 do processo
    E as demais notas do processo andam para as posições seguintes
    E vejo o aviso "* ** Sequencia Atualizada ** *"

  Cenário: A nota vai logo depois da nota indicada
    Dado que estou na tela N019T no modo de alteração
    E que consultei o processo e a nota
    Quando informo a nota anterior e confirmo
    Então a nota passa a ocupar a posição imediatamente seguinte à daquela nota
    E as notas que estavam dessa posição em diante andam uma posição para trás
    E vejo o aviso "* ** Sequencia Atualizada ** *"
    E quando a posição da nota fica repetida ou o deslocamento pega a nota errada,
      isso é a dúvida registrada na regra do deslocamento, não o resultado esperado

  Cenário: A alteração deixa rastro na auditoria
    Dado que confirmei uma reordenação na N019T
    Quando a gravação termina
    Então existe um registro de auditoria da nota fiscal para cada nota deslocada
    E com a operação de alteração, a imagem da nota antes e depois
    E com a matrícula, o acesso, a secretaria, a CRE, o órgão, o terminal, a data e hora
      e o número do processo

  Cenário: A tela confirma e volta a ela mesma
    Dado que confirmei uma reordenação na N019T
    Quando a gravação termina
    Então continuo na tela N019T
    E vejo o número da nota e a posição nova nos campos

  Cenário: Nada é processado sem a conferência de sessão, de tela e de operação
    Dado que estou na tela N019T
    Quando a conferência de sessão, do registro da tela ou da permissão da operação não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *"
      ou "* Acesso negado para esta operacao *"
    E volto ao menu sem que nada seja validado nem gravado

  Cenário: Prefixo de tela preenchido desvia a tela
    Dado que a transação chega à N019T com um prefixo de tela preenchido
    Quando a conferência de rota rodaria
    Então sou levado para a tela indicada no prefixo
    E nada é validado nem gravado nesta tela

  Cenário: A tela não apresenta a recusa de destino inválido
    Dado que estou na tela N019T e confirmei uma alteração
    Quando a gravação é preparada
    Então o modo de distribuição automática já foi limpo
    E a recusa de destino inválido não é apresentada
```
