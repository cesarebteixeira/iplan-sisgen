# US — E945T — Substituir o cartão de referência bloqueado do aluno

## Estória

Como **servidor da coordenação regional escolar (CRE)**, quero **emitir um cartão de
referência novo para o aluno cujo cartão está bloqueado**, para que **o aluno volte a
ter cartão para receber sem que o bloqueio seja desfeito e sem que se perca o vínculo
entre o cartão bloqueado e o cartão novo**.

O bloqueio tira o cartão de circulação: o cartão bloqueado deixa de contar como
entregue ou como não entregue e passa a contar como cancelado na contagem do contrato
de referência. Enquanto ele estiver assim, o aluno não tem cartão para receber — e
desfazer o bloqueio não é a saída, porque apaga o motivo que o justificou. A
substituição é a operação que resolve isso: ela emite o cartão novo, marca o cartão
bloqueado como já substituído, para que ninguém o troque duas vezes, e soma o cartão
novo à contagem do contrato.

## Contexto

Jornada S000M → E000M → E900M → E945T.

Ator: servidor da CRE — emite o cartão de referência que substitui um cartão bloqueado
do aluno, dentro do contrato e do órgão filho informados.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A E945T não é menu e não é aberta por menu: a E900M passa o controle para ela direto, e
por isso a tela abre sem os dados do contrato — o contrato, o ano, a matrícula e o
cartão bloqueado não vêm preenchidos da tela anterior. Ela é a tela da substituição:
trabalha só na opção de alteração, emite o cartão novo, marca o cartão bloqueado,
acerta a contagem do contrato e registra as duas operações na auditoria; não exclui
nada e não encaminha para outra tela — ao terminar, ela reexibe a si mesma.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela emite o cartão novo no lugar do bloqueado: ela grava, e não exclui

A E945T faz a substituição do cartão de referência bloqueado. Ela faz duas coisas no
mesmo ato: marca o cartão bloqueado como **já substituído**, apontando-o para o número
do cartão novo, e **inclui** o cartão novo para a mesma matrícula, no mesmo contrato e
no mesmo órgão filho, com a situação de **não entregue** e sem justificativa. Depois
acerta a contagem do contrato. O cartão bloqueado continua bloqueado: o programa não
lhe mexe na situação nem na justificativa.

É uma tela que **grava**: altera um cartão, inclui outro, cria ou altera a contagem do
contrato e deixa duas operações na auditoria. Ela **não exclui** nada — as rotinas de
exclusão existem declaradas para os oito cadastros que a tela enxerga, e nenhuma delas
é executada. Também **não altera** contrato, órgão, fornecedor nem justificativa, e
**não inclui** cartão para matrícula, contrato ou órgão diferentes dos informados.

### RN-02 — A tela só trabalha em alteração, e toda transmissão passa pela conferência de acesso

A E945T não tem modo de consulta: ela só executa na opção de **alteração**. Em qualquer
outra opção de manutenção, a recusa é **\* Operacao nao disponivel. Use ALT \***, com o
cursor de volta ao campo da opção, e nada é gravado. A consulta do contrato do mesmo
menu abre em modo de leitura; a E945T não tem esse modo — o único valor que ela põe no
campo da opção é o da alteração.

Antes de ler e antes de gravar, a transmissão passa pela conferência de segurança do
sistema, que leva em conta a matrícula do funcionário, o código de acesso, o
privilégio, o tipo de órgão e a coordenação regional escolar da sessão. Não vindo a
autorização, a tela para e nada é gravado.

[?] A opção de manutenção é reescrita pelo próprio programa com o código da alteração a
cada exibição da tela; o reexame da execução também exige esse mesmo código. Se o
campo não for digitável, a recusa por opção indisponível nunca acontece. O que define
se o campo é digitável está na máscara da tela, que não está no acervo. Pergunta ao
site.

### RN-03 — O órgão filho é obrigatório, e a coordenação vem do cadastro do órgão

O órgão filho é informado pelo operador. Em branco, a recusa é **\* Informe o orgao \***;
não cadastrado, a recusa é **\* Orgao nao cadastrado \***, com o cursor no campo do
órgão.

A coordenação regional escolar não é conferida do jeito que o operador a digitou: o
sistema lê a coordenação que está no cadastro do órgão filho informado, e é ela que
vale dali em diante. Se o vínculo do usuário tem uma coordenação regional escolar, o
órgão informado só passa se a coordenação dele for a mesma; sendo outra, a recusa é
**\* Usuario sem acesso ao grupo deste Orgao \***. E se o vínculo do usuário tem um
órgão filho, informar outro órgão é recusado com
**\* Usuario sem acesso a outro orgao \***.

[?] A recusa por órgão não cadastrado sai de uma conferência que examina um indicador
que a própria leitura do cadastro do órgão não preenche: ou a recusa nunca dispara — e
um órgão inexistente passa por cadastrado —, ou ela depende de um valor do ambiente que
não está no acervo. Não escolho um dos dois lados. Pergunta ao site.

[?] A recusa por "outro órgão" compara o órgão informado com o órgão do vínculo do
usuário guardado na área da tela; essa área é zerada na primeira passagem e só recebe o
órgão **depois** de passar por essa mesma recusa, e em todo o acervo o órgão do vínculo
que a tela consulta aparece atribuído apenas a zeros. Ou a recusa nunca dispara — e
qualquer órgão cadastrado passa —, ou quem preenche esse lugar está fora do que se
conseguiu ler. Não escolho um dos dois lados. Pergunta ao site.

[?] A tela tem o rótulo COORD.REG.ESCOLA num campo que o programa sobrescreve com a
coordenação lida no cadastro do órgão. Ou o campo é só de exibição, ou o que o operador
digita ali é descartado sem aviso. Pergunta ao site.

### RN-04 — O contrato é obrigatório, tem de existir e tem de estar aberto

O contrato de referência é identificado pelo ano e pelo número informados. Sem o
número, a recusa é **\* Informe o Contrato \***, com o cursor de volta ao campo do
contrato. Informado, o sistema procura o contrato pelo tipo de órgão da secretaria da
sessão, pelo ano e pelo número; não achando, recusa com
**\* Contrato nao cadastrado \***. Só o número é conferido em branco: o ano em branco
não gera aviso próprio e faz a procura por ano zero, que cai na recusa de contrato não
cadastrado.

E a substituição não é permitida em contrato fechado: estando o contrato marcado como
fechado, a recusa é **\* Contrato fechado \***, também com o cursor no campo do
contrato. Só contrato aberto aceita a emissão do cartão novo.

### RN-05 — A matrícula do aluno e o cartão bloqueado são obrigatórios

A matrícula do aluno é obrigatória: em branco, a recusa é
**\* Informe a Matricula do Aluno \***, com o cursor no campo da matrícula. E o número
do cartão que se quer substituir também é obrigatório: em branco, a recusa é
**\* Informe o Cartao Bloqueado \***, com o cursor no campo do cartão.

### RN-06 — O cartão informado tem de existir para a matrícula, o contrato e o órgão

Informados o contrato, o órgão, a matrícula e o número do cartão, o sistema procura o
cartão; não achando, a recusa é **\* Matricula nao cadastrada \***, com o cursor de
volta ao campo da matrícula — a mensagem fala só da matrícula, mas a procura é pelo
conjunto todo: tipo de órgão, ano e número do contrato, órgão filho, matrícula e número
do cartão. Não existe cartão procurado pela matrícula sozinha: o número do cartão é
parte do que identifica o registro.

### RN-07 — Só o cartão bloqueado, com justificativa registrada e ainda não substituído, pode ser trocado

O cartão informado tem de estar **bloqueado**: estando em qualquer outra situação, a
recusa é **\* Cartao nao bloqueado \***, com o cursor no campo do cartão. E o bloqueio
tem de ter deixado uma **justificativa registrada** no cartão: sem ela, a recusa é
**\* Cartao atual nao bloqueado \***, com o cursor no mesmo campo. A tela mostra, para
conferência, a descrição da justificativa que o bloqueio gravou.

O cartão bloqueado também não pode ter sido substituído antes: se ele já aponta para um
cartão substituto, a recusa é **<- Cartao bloqueado ja substituido \***, com o cursor
no campo do cartão. Substituir é operação de uma vez só por cartão: gravado o vínculo
com o cartão novo, nenhuma segunda substituição daquele mesmo cartão passa por esta
tela.

### RN-08 — A matrícula não pode ter outro cartão fora de cancelado e bloqueado

Antes de emitir, o sistema percorre os cartões da matrícula naquele contrato e naquele
órgão. Encontrando um cartão que não esteja cancelado nem bloqueado, a substituição é
recusada com **<- Ja existe cartao ativo para esta matricula \*** e o cursor volta ao
campo da matrícula.

A matrícula não pode ficar com dois cartões valendo ao mesmo tempo: só se emite o
cartão novo quando todos os outros cartões daquela matrícula, naquele contrato e
naquele órgão, estão cancelados ou bloqueados.

[?] A varredura depende de parâmetros da rotina de leitura cujo significado não está no
acervo: não concluo se ela percorre os cartões da matrícula naquele contrato, do
primeiro ao último, ou se procura exatamente o cartão de número zero, que a própria
tela trata como número não informado. No segundo caso ela nunca encontraria um cartão
ativo, e a substituição passaria mesmo com outro cartão valendo. Não escolho um dos
dois lados. Pergunta ao site.

### RN-09 — O número do cartão novo é obrigatório, diferente do atual e não pode já existir

O número do cartão novo é informado pelo operador. Em branco, a recusa é
**\* Informe Novo Cartao \***, com o cursor no campo do cartão novo. Informado, ele tem
de ser diferente do número do cartão bloqueado: sendo o mesmo, a recusa é
**\* Cartao nao pode ser o mesmo \***, com o cursor no mesmo campo.

E o número novo não pode pertencer a nenhum cartão já cadastrado: achando um cartão com
aquele número, a recusa é **<- Cartao ja cadastrado \***, com o cursor no campo do
cartão novo. A conferência é pelo número do cartão dentro do tipo de órgão, sem olhar o
contrato nem a matrícula: a unicidade que o sistema garante é essa, e não a do número
dentro do contrato.

### RN-10 — A tela mostra o que encontrou e pede confirmação antes de gravar

Ao receber os dados, a tela **não grava**. Ela confere tudo e mostra o que encontrou — o
número e o ano do contrato, a vigência do contrato, o fornecedor com a razão social, a
matrícula, o cartão bloqueado, a justificativa registrada nele e o número do cartão novo
— e pergunta **Confirma inclusao do cartao <S/N> ?**, com o cursor no campo da
confirmação.

A gravação só acontece numa segunda transmissão, com a resposta **S**. Qualquer outra
resposta deixa a tela como estava e não grava nada. E se algum dos dados que identificam
o cartão for alterado junto com a resposta — órgão, contrato, ano, matrícula, número do
cartão bloqueado ou número do cartão novo — a confirmação é cancelada e o operador
recomeça do zero.

Toda recusa desta tela devolve a transmissão à primeira passagem: recusado o dado, a
substituição fica barrada naquela transmissão e nada é gravado.

[?] A execução da confirmação só acontece se os sete campos que identificam a operação
estiverem preenchidos — entre eles a coordenação regional escolar, que vem do cadastro
do órgão. Faltando algum, a tela volta sem gravar e sem avisar nada: o operador responde
S e não vê nem a inclusão nem uma explicação. Se a coordenação puder chegar zerada, é
defeito; não se conclui do programa. Pergunta ao site.

### RN-11 — Executada a substituição, o bloqueado fica marcado e o cartão novo nasce não entregue

Confirmada a substituição, o cartão bloqueado continua bloqueado e ganha o número do
cartão novo como **substituto** — é esse vínculo que impede uma segunda substituição do
mesmo cartão. O cartão novo é incluído para a mesma matrícula, no mesmo contrato, no
mesmo órgão filho e na mesma coordenação regional escolar, com a situação de **não
entregue**, sem justificativa e sem substituto. A tela então avisa
**\* Cartao incluido \*** e continua na E945T, reexibindo os mesmos dados.

### RN-12 — A contagem do contrato ganha um não entregue e um cartão no total

A substituição acerta a contagem do contrato naquela coordenação e naquele órgão: soma
um aos **não entregues** e soma um ao **total** de cartões do contrato. Nada é
diminuído: o cartão bloqueado já tinha sido jogado para os cancelados no ato do
bloqueio, e continua contado lá. A contagem de entregues não é tocada.

Não existindo o registro de contagem do contrato naquela coordenação e naquele órgão, a
tela o cria com um não entregue e um cartão no total, e as demais contagens em zero.

[?] O registro criado quando não existe contagem começa em **um**, sem considerar os
cartões que o contrato já tem: se a contagem do contrato puder faltar num contrato com
cartões, ela passa a mostrar menos do que existe, e a consulta do contrato publica esse
número. A tela não avisa nem corrige. Pergunta ao site.

### RN-13 — As duas operações ficam registradas na auditoria

Cada substituição grava **dois** registros na trilha de auditoria das telas: um da
alteração do cartão bloqueado, com o conteúdo anterior e o posterior do cartão — que
diferem só pelo vínculo com o cartão novo —, e um da inclusão do cartão novo, com o
conteúdo posterior do cartão criado. Nos dois vão o cadastro auditado, a tela de origem,
a operação, a matrícula do funcionário, o terminal, o dia, o mês, o ano e a hora da
sessão, o número do processo — que aqui é a matrícula do aluno —, o tipo de órgão e a
coordenação regional escolar.

[?] O cartão novo é gravado com o código da tela que **bloqueia** cartões no campo que
identifica a tela de origem, e esse valor entra no conteúdo posterior do registro de
auditoria da inclusão: a auditoria da inclusão aponta a tela de bloqueio, não a da
substituição. Se isso é intencional — o cartão nasce pertencendo ao bloqueio — ou se é
vestígio de outra rotina, não se conclui do programa. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Substituir o cartão de referência bloqueado do aluno

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E945T

  Cenário: Emissão de um cartão novo no lugar de um cartão bloqueado
    Dado que existe um cartão de referência bloqueado, com justificativa registrada, para a matrícula informada
    E o contrato de referência está aberto
    E não existe outro cartão da matrícula fora de cancelado ou bloqueado
    Quando informo o órgão filho, o contrato, a matrícula, o cartão bloqueado e o número do cartão novo
    Então a tela mostra o número e o ano do contrato, a vigência e o fornecedor com a razão social
    E mostra a justificativa registrada no cartão bloqueado e o número do cartão novo
    E me pede a confirmação da inclusão do cartão
    E nada é gravado ainda

  Cenário: Confirmar a emissão do cartão novo
    Dado que a tela me pediu a confirmação da inclusão do cartão
    Quando respondo S
    Então o cartão bloqueado continua bloqueado e fica marcado como substituído pelo número do cartão novo
    E o cartão novo é incluído como não entregue, sem justificativa
    E a quantidade de não entregues do contrato aumenta um
    E a quantidade total de cartões do contrato aumenta um
    E vejo a mensagem "* Cartao incluido *"
    E continuo na E945T, com os mesmos dados na tela

  Cenário: Resposta diferente de S não inclui cartão nenhum
    Dado que a tela me pediu a confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a tela volta ao estado anterior
    E nada é gravado

  Cenário: Alterar um dado junto com a confirmação cancela a inclusão
    Dado que a tela me pediu a confirmação
    Quando altero o número do cartão novo e respondo S
    Então a confirmação é cancelada
    E nada é gravado

  Cenário: Opção de manutenção diferente de alteração
    Quando informo uma opção de manutenção diferente de alteração
    Então vejo a mensagem "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: Operação não autorizada para o perfil
    Dado que o meu perfil não tem a autorização para a operação
    Quando confirmo os dados
    Então o sistema recusa a operação
    E nada é gravado

  Cenário: Órgão filho não informado
    Quando deixo o órgão filho em branco
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho não cadastrado
    Quando informo um órgão filho que não existe
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Órgão filho de outra coordenação
    Dado que estou vinculado a uma coordenação regional escolar
    Quando informo um órgão filho de outra coordenação
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste Orgao *"
    E nada é gravado

  Cenário: Órgão filho diferente do vinculado ao usuário
    Dado que o meu vínculo tem um órgão filho
    Quando informo outro órgão filho
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E nada é gravado

  Cenário: Contrato não informado
    Dado que deixei o número do contrato em branco
    Quando confirmo os dados
    Então vejo a mensagem "* Informe o Contrato *"
    E o cursor fica no campo do contrato
    E nada é gravado

  Cenário: Contrato não cadastrado
    Dado que informei ano e número de contrato que não existem para a minha secretaria
    Quando confirmo os dados
    Então vejo a mensagem "* Contrato nao cadastrado *"
    E o cursor fica no campo do contrato
    E nada é gravado

  Cenário: Contrato fechado
    Dado que o contrato informado está fechado
    Quando confirmo os dados
    Então vejo a mensagem "* Contrato fechado *"
    E o cursor fica no campo do contrato
    E nada é gravado

  Cenário: Matrícula do aluno não informada
    Quando deixo a matrícula do aluno em branco
    Então vejo a mensagem "* Informe a Matricula do Aluno *"
    E o cursor fica no campo da matrícula
    E nada é gravado

  Cenário: Número do cartão bloqueado não informado
    Quando deixo o número do cartão que quero substituir em branco
    Então vejo a mensagem "* Informe o Cartao Bloqueado *"
    E o cursor fica no campo do cartão
    E nada é gravado

  Cenário: Cartão não encontrado para a matrícula, o contrato e o órgão
    Dado que não existe cartão com o número informado para a matrícula, o contrato e o órgão
    Quando confirmo os dados
    Então vejo a mensagem "* Matricula nao cadastrada *"
    E o cursor fica no campo da matrícula
    E nada é gravado

  Cenário: O cartão informado não está bloqueado
    Dado que o cartão informado está entregue, cancelado ou não entregue
    Quando confirmo os dados
    Então vejo a mensagem "* Cartao nao bloqueado *"
    E o cursor fica no campo do cartão
    E nada é gravado

  Cenário: O cartão bloqueado não tem justificativa registrada
    Dado que o cartão está bloqueado, mas sem justificativa registrada
    Quando confirmo os dados
    Então vejo a mensagem "* Cartao atual nao bloqueado *"
    E o cursor fica no campo do cartão
    E nada é gravado

  Cenário: O cartão bloqueado já foi substituído
    Dado que o cartão bloqueado já aponta para um cartão substituto
    Quando confirmo os dados
    Então vejo a mensagem "<- Cartao bloqueado ja substituido *"
    E o cursor fica no campo do cartão
    E nada é gravado

  Cenário: A matrícula tem outro cartão fora de cancelado e bloqueado
    Dado que a matrícula tem, nesse contrato e nesse órgão, um cartão que não está cancelado nem bloqueado
    Quando tento substituir o cartão bloqueado da mesma matrícula
    Então vejo a mensagem "<- Ja existe cartao ativo para esta matricula *"
    E o cursor fica no campo da matrícula
    E nada é gravado

  Cenário: Número do cartão novo não informado
    Quando deixo o número do cartão novo em branco
    Então vejo a mensagem "* Informe Novo Cartao *"
    E o cursor fica no campo do cartão novo
    E nada é gravado

  Cenário: Número do cartão novo igual ao do cartão bloqueado
    Dado que informei o mesmo número do cartão bloqueado como cartão novo
    Quando confirmo os dados
    Então vejo a mensagem "* Cartao nao pode ser o mesmo *"
    E o cursor fica no campo do cartão novo
    E nada é gravado

  Cenário: Número do cartão novo já cadastrado
    Dado que já existe um cartão cadastrado com o número que informei como cartão novo
    Quando confirmo os dados
    Então vejo a mensagem "<- Cartao ja cadastrado *"
    E o cursor fica no campo do cartão novo
    E nada é gravado

  Cenário: A contagem do contrato acompanha a substituição
    Dado que o contrato tem contagem de entregues, de não entregues, de cancelados e de total
    Quando confirmo a emissão do cartão novo
    Então a quantidade de não entregues aumenta um
    E a quantidade total de cartões aumenta um
    E a quantidade de cancelados não muda
    E a quantidade de entregues não muda

  Cenário: Sem registro de contagem, a contagem é criada com o cartão novo
    Dado que não existe registro de contagem para o contrato, a coordenação e o órgão
    Quando confirmo a emissão do cartão novo
    Então o cartão novo é incluído
    E a contagem do contrato passa a ter um não entregue e um cartão no total
    E vejo a mensagem de sucesso

  Cenário: A tela não grava na primeira transmissão
    Quando informo os dados e a tela me pede a confirmação
    Então o cartão bloqueado não é alterado
    E nenhum cartão novo é incluído
    E a contagem do contrato não muda

  Cenário: Toda substituição fica registrada na auditoria
    Quando confirmo a emissão do cartão novo
    Então ficam dois registros na auditoria: o da alteração do cartão bloqueado e o da inclusão do cartão novo
    E cada um tem a tela de origem, a operação, o cartão antes e depois, a matrícula do funcionário, a data e a hora da sessão e a matrícula do aluno como número do processo

  Cenário: A tela não exclui nada e não encaminha para outra tela
    Dado que estou na E945T
    Quando a substituição termina
    Então nenhum cartão é excluído
    E nenhum contrato, órgão, fornecedor ou justificativa é alterado
    E continuo na E945T
```
