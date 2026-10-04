# US — P525T — Conferência do arquivo do ano e do grupo escolar

## Estória

Como **servidor de CRE**, quero **confirmar o grupo escolar e o ano de arquivo em que
vou trabalhar — e saber se aquele grupo tem registros escolares naquele ano**, para
que **eu só siga para a conferência dos registros quando o arquivo do ano existir e
estiver regular, sem abrir uma relação que não tem o que mostrar**.

O registro escolar de cada grupo vive dentro do arquivo de um ano, e esse arquivo é
antes publicado e devolvido pelo SIAFIC: um ano pode estar aberto sem o retorno, e um
grupo pode não ter registro escolar nenhum naquele ano. Esta é a tela que confere as
duas coisas antes de deixar seguir — ela mostra o arquivo do ano e, em seguida,
confirma que o grupo tem registro naquele arquivo. Sem essa conferência, a
conferência dos registros abriria vazia, ou sobre um arquivo que ainda não voltou do
SIAFIC, e o servidor não saberia distinguir "não há o que conferir" de "ainda não
pode conferir".

## Contexto

Jornada S000M → P000M → P500M → P525T.
Ator: servidor de CRE — nesta tela, confirma o grupo escolar e o ano de arquivo em
que vai trabalhar e confere se aquele grupo tem registros escolares no arquivo
daquele ano.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada, `P000M` e `P500M`, são menus: só encaminham e
não deixam dado de negócio para esta tela. O contexto que a `P525T` usa — a matrícula,
o código de acesso, a estação, a CRE e o ano de exercício — é o que a entrada deixou
na sessão, e é a própria sessão que faz o limite de alcance que a tela aplica
(`RN-05`). Esta tela não é alcançada por opção de menu de nenhum módulo: ela só é
chamada por outra tela, encadeada, e essa chamada é o que a faz existir na jornada.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — Ao abrir, a tela mostra o arquivo do ano em que se está trabalhando

Abrir a tela não grava nada: ela mostra o arquivo do ano em curso — o ano que a
sessão carrega — e, com ele, até doze arquivos anuais daquele ano, um por linha, com
o número do arquivo, o dia e a hora em que ele foi gerado, se já tem o retorno do
SIAFIC e o grupo escolar. Não havendo arquivo nenhum para aquele ano, a tela avisa
**\* Nao existem arquivos neste ano \*** e encerra a operação sem mostrar linha
nenhuma.

[?] A tela monta as linhas do arquivo anual em uma tabela que ela depois reordena,
posição a posição, antes de mostrar: a linha que o operador vê na primeira posição
pode ser a segunda da tabela. Se o efeito é só de ordenação, ou se a primeira linha é
mostrada trocada, não se lê nos fontes desta jornada. Pergunta ao site.

[?] Os nomes das colunas que o operador vê não estão no lote: o que se lê no fonte
são os rótulos de conferência e a estrutura das linhas. Se a máscara tem outros
rótulos, ou se mostra o grupo em cada linha ou só uma vez, não se lê no corpus.
Pergunta ao site.

### RN-02 — Na abertura, a operação é consulta

A tela só executa a consulta: ela não inclui, não altera e não exclui nada do
cadastro. Se a operação informada for diferente da consulta, ela recusa com
**\* Opcao nao disponivel. Use CON \***, deixa o cursor no campo da operação e não
grava nada.

[?] A tela é procurada pelo código de operação da consulta e recusa a operação que
não for essa — mas, ao ser chamada por outra tela, nenhum trecho desta jornada deixa
a operação preenchida como consulta: a área de trabalho da tela não é inicializada
com esse valor, ao contrário do que fazem outras telas do acervo. Ou a rotina comum
preenche a operação antes de a tela ser chamada, ou a recusa acontece no uso normal.
Pergunta ao site.

### RN-03 — O ano do arquivo tem de ser o ano da sessão

O sistema só aceita o ano de arquivo que for o ano em curso da sessão. Informado
outro ano, ou nenhum ano, a tela procura esse ano no cadastro de arquivos anuais e
recusa quando ele não está cadastrado, com **\* Nao existem registros cadastrados \***
e o cursor no campo do ano — ou seja, não se confere outro exercício por esta tela.

### RN-04 — O arquivo do ano tem de estar cadastrado

Antes de seguir, a tela procura no cadastro de arquivos anuais o arquivo que identifica
o ano em que se está trabalhando. Não achando, a recusa é
**\* Nao existem arquivos neste ano \***, o cursor fica no campo do ano e nada é
gravado.

### RN-05 — O grupo escolar é obrigatório e limitado ao alcance do servidor

A consulta exige que o grupo escolar esteja informado: sem ele, a recusa é
**\* Informe o grupo para consulta \*** e o cursor fica no campo do grupo.

O grupo informado ainda tem de caber no alcance que a sessão define: quando a
matrícula do servidor tem um grupo, só esse grupo é aceito, e informar outro dá
**\* Usuario sem acesso a este grupo \***, com o cursor no campo do grupo; quando a
matrícula não tem grupo, o servidor alcança os grupos da sua secretaria.

### RN-06 — Arquivo publicado sem retorno do SIAFIC não deixa consultar

Quando o arquivo do ano já está publicado e o arquivo ainda não tem o retorno do
SIAFIC, a tela recusa com **\* Arquivo sem retorno do SIAFIC \***, deixa o cursor na
coluna do retorno e não grava nada. Publicar e ainda não ter voltado do SIAFIC é
impedimento para a conferência.

### RN-07 — A tela confere se o grupo tem registro escolar naquele arquivo

Antes de encaminhar, a tela procura o registro escolar do grupo dentro do arquivo
daquele ano. Não havendo registro escolar do grupo naquele arquivo, ela recusa com
**\* Grupo sem reg cadastrados neste arquivo \***, deixa o cursor na coluna do retorno
e não grava nada — é o que impede a abertura de uma relação vazia. Havendo, a
consulta segue.

### RN-08 — A consulta não grava nem apaga nada

Esta tela não inclui, não altera e não exclui em nenhum cadastro: o que ela faz é ler
o cadastro de arquivos anuais, ler o cadastro de registros escolares do ano e mostrar.
O que aparece na tela — o número do arquivo, o dia e a hora da geração, se há retorno
do SIAFIC, o grupo escolar e a situação — vem do cadastro, não de cálculo da tela.

### RN-09 — O grupo e o ano conferidos seguem para a tela dos registros

Passando por todas as conferências, a tela entrega à tela seguinte o grupo escolar e
o ano de arquivo que acabou de conferir, e a abre no mesmo modo desta operação — o
modo de consulta. É essa entrega que decide o que a tela seguinte mostra: se a
conferência desta tela não passar, a tela seguinte não é aberta.

### RN-10 — A tela não se abre sobre ela mesma

Quando a tela já está aberta e é chamada de novo por outra tela, a operação é
encerrada em silêncio: nada é mostrado, nada é gravado e nenhuma mensagem aparece.

### RN-11 — A relação do arquivo do ano cabe em uma tabela de doze linhas

A relação do arquivo do ano é montada em uma tabela de até doze linhas: quando a
leitura não encontra o arquivo, a montagem para na linha que falhou e as linhas
seguintes não são mostradas. Quando a leitura falha na primeira linha, o aviso é
**\* Nao existem arquivos neste ano \***.

[?] Os fontes desta jornada têm dois avisos para a mesma leitura que não achou o
arquivo — **\* Nao existem arquivos neste ano \*** e
**\* Nao existem registros cadastrados \*** —, e só o primeiro é emitido na linha que
inicia a montagem. Se o segundo chega a aparecer para o operador, em que situação, e
o que ele quer dizer, não se lê no corpus. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Conferência do arquivo do ano e do grupo escolar antes de seguir para os registros

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela P525T

  Cenário: Abertura mostra o arquivo do ano em que estou trabalhando
    Dado que o ano da sessão tem arquivo anual cadastrado
    Quando abro a tela P525T
    Então vejo o arquivo do ano, até doze linhas, com o número do arquivo, o dia e a hora da geração, o retorno do SIAFIC e o grupo escolar
    E nada é gravado

  Cenário: O ano não tem arquivo nenhum
    Dado que o ano da sessão não tem arquivo anual cadastrado
    Quando abro a tela P525T
    Então vejo a mensagem "* Nao existem arquivos neste ano *"
    E nenhuma linha é mostrada
    E nada é gravado

  Cenário: Operação diferente da consulta é recusada
    Dado que o ano da sessão tem arquivo anual cadastrado
    Quando informo uma operação que não é a de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor fica no campo da operação
    E nada é gravado

  Cenário: A consulta é do grupo e do ano informados
    Dado que o meu grupo tem registro escolar no arquivo do ano
    Quando confirmo a consulta
    Então vejo o arquivo do ano conferido
    E nada é gravado

  Cenário: Sem grupo informado, a consulta é recusada
    Dado que não informo o grupo escolar
    Quando confirmo a consulta
    Então vejo a mensagem "* Informe o grupo para consulta *"
    E o cursor fica no campo do grupo
    E nada é gravado

  Cenário: Grupo fora do meu alcance é recusado
    Dado que a minha matrícula tem um grupo
    Quando informo outro grupo e confirmo a consulta
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo do grupo
    E nada é gravado

  Cenário: Ano diferente do ano da sessão é recusado
    Dado que o ano da sessão tem arquivo anual cadastrado
    Quando informo um ano de arquivo diferente e que não está cadastrado
    Então vejo a mensagem "* Nao existem registros cadastrados *"
    E o cursor fica no campo do ano
    E nada é gravado

  Cenário: Arquivo do ano não cadastrado é recusado
    Dado que o arquivo que identifica o ano em que trabalho não está cadastrado
    Quando confirmo a consulta
    Então vejo a mensagem "* Nao existem arquivos neste ano *"
    E o cursor fica no campo do ano
    E nada é gravado

  Cenário: Arquivo publicado sem retorno do SIAFIC é recusado
    Dado que o arquivo do ano está publicado
    E esse arquivo ainda não tem retorno do SIAFIC
    Quando confirmo a consulta
    Então vejo a mensagem "* Arquivo sem retorno do SIAFIC *"
    E o cursor fica na coluna do retorno
    E nada é gravado

  Cenário: Grupo sem registro escolar no arquivo do ano é recusado
    Dado que o meu grupo não tem registro escolar no arquivo do ano
    Quando confirmo a consulta
    Então vejo a mensagem "* Grupo sem reg cadastrados neste arquivo *"
    E o cursor fica na coluna do retorno
    E nada é gravado

  Cenário: A conferência passa e a tela dos registros é aberta
    Dado que o meu grupo tem registro escolar no arquivo do ano
    E o arquivo do ano não está publicado sem retorno do SIAFIC
    Quando confirmo a consulta
    Então a tela entrega o grupo e o ano conferidos à tela dos registros
    E a tela dos registros abre em consulta

  Cenário: A relação do arquivo do ano para na linha que falhou
    Dado que o ano da sessão tem arquivo anual cadastrado
    Quando abro a tela P525T
    Então a relação mostra até doze linhas de arquivo
    E a montagem para na primeira linha que não encontrar arquivo

  Cenário: A tela não se abre sobre ela mesma
    Dado que a tela P525T já está aberta
    Quando outra tela a chama de novo
    Então a operação é encerrada sem mensagem
    E nada é gravado
```
