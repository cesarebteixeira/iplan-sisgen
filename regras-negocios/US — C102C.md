# US — C102C — Consultar grupos de atendimento do órgão

## Estória

Como **servidor da CRE**, quero **consultar os grupos de atendimento cadastrados para o
órgão da minha secretaria e, a partir dessa relação, abrir o mapa de atendimento**, para
que **eu confira com que grupos os atendimentos do órgão se classificam e chegue ao mapa
já no órgão filho certo, sem digitar o código dele**.

O grupo de atendimento é a peça mais fina da classificação do atendimento: é apontando
para um grupo que o cadastro de atendimentos do órgão diz qual é o seu grupo integral,
qual é o parcial e qual é o de 24 horas. Quem vai montar o mapa de atendimento do órgão
filho precisa ver antes quais grupos existem ali — e é esta a tela que mostra essa
relação. Sem ela, o mapa se abre às cegas, sem que o servidor saiba com que grupos pode
contar.

## Contexto

Jornada S000M → C000M → C028M → C102C.
Ator: servidor de CRE — consulta os grupos de atendimento do órgão da sua secretaria e,
marcando o indicador, abre o mapa de atendimento em inclusão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

Esta tela não recebe cadastro nenhum da tela anterior: o passo que a abre é uma opção de
menu, e o menu só encaminha. O que ela usa vem da sessão, do vínculo da matrícula com a
secretaria escolhida no `LOGON`: o **tipo de órgão**, que filtra a relação; o **órgão
filho**, que ela entrega à tela do mapa; e o **código de acesso**, que a autoriza. Isso é
regra da entrada e está no anexo de evidências, em **Regras que se revelaram da entrada**.

A tela é de consulta e não é menu: quando o servidor marca o indicador do mapa (RN-09),
ela encadeia direto na tela do mapa de atendimento, sem passar por menu nenhum.

## Regras de negócio

### RN-01 — A tela consulta os grupos de atendimento do órgão da minha secretaria

Esta é uma tela de **consulta**. Ela mostra a relação dos **grupos de atendimento**
cadastrados para o **tipo de órgão** que o meu vínculo com a secretaria deixou na sessão —
nunca para um órgão digitado, que não se digita aqui. O cabeçalho mostra a descrição desse
órgão e a data do sistema, e cada grupo aparece com o segmento a que pertence e com as
suas duas descrições. Nada nesta tela é gravado.

### RN-02 — A relação tem 15 linhas, e cada linha informa cinco dados

São **15 linhas** por vez. Cada linha informa o **código do segmento** (2 dígitos), a
**descrição resumida do segmento** (15 caracteres), o **código do grupo de atendimento**
(2), a **descrição do grupo** (20) e a **descrição resumida do grupo** (5). A descrição
resumida do segmento vem do cadastro de segmentos de atendimento e não se digita; as
demais vêm do cadastro de grupos. Os grupos aparecem na ordem do cadastro: primeiro o
segmento e, dentro dele, o código do grupo.

Fora da grade, o cabeçalho traz cinco dados que o terminal informa (a tela, a origem, o
número da transação, a data de entrada e o mês de referência), três campos que o servidor
pode preencher (a opção de manutenção, o código da tela de destino e o indicador do mapa),
a descrição do órgão, a data do sistema e a linha de mensagem.

[?] A relação continua a partir do último grupo exibido, mas o corpus não traz o contrato da
leitura encadeada; não dá para concluir, só por esta tela, se ao passar de uma página para a
seguinte o primeiro grupo se repete ou se é pulado. Pergunta ao site.

### RN-03 — A relação começa pela referência de grupo que a sessão traz

A primeira leitura da relação parte da referência de **segmento e grupo de atendimento**
que estiver na sessão. Com a sessão sem referência nenhuma — isto é, chegando sem operação
de manutenção em curso —, a tela zera a referência de segmento e a relação começa no
primeiro grupo do órgão. Chegando com uma referência, ela é preservada e a relação começa
por ela, que é o que permite reabrir a relação na altura em que ela ficou.

[?] O corpus não mostra qual tela deixa essa referência na sessão, e nenhuma das telas
deste caminho deixa. Também não dá para concluir se este caminho de retomada é alcançável
por aqui. Pergunta ao site.

### RN-04 — Órgão sem grupos de atendimento a tela avisa

Quando a primeira leitura da relação não encontra nenhum grupo de atendimento para o órgão,
a tela avisa **\* Nao existe grupos de atendimento cadastrados \*** e não preenche nenhuma
linha. O aviso é dado uma vez, ao abrir a relação.

### RN-05 — Segmento fora do cadastro deixa a linha sem a descrição resumida

Cada grupo da relação aponta para um segmento de atendimento. Quando esse segmento não está
no cadastro de segmentos do órgão, a linha continua sendo mostrada, com o código do grupo e
as duas descrições do grupo, mas **sem** a descrição resumida do segmento. A falta do
segmento não esconde o grupo.

### RN-06 — A tela é de consulta: só a consulta é aceita, e ela é adotada sempre

A opção de manutenção do cabeçalho aceita **apenas a consulta**. A própria tela preenche o
campo com a consulta quando abre, e ao confirmar qualquer outra opção ela recusa com
**\* Operacao nao disponivel \***, devolve o cursor ao campo da opção e não faz mais nada.
O modo da tela **não** depende de quem a chamou: venha do menu ou de outra tela, ela adota
a consulta sempre, e não há nesta tela nenhuma comparação com a tela de origem.

[?] O campo da opção é preenchido com o código interno de consulta, e a conferência compara
o que foi digitado com esse mesmo código interno. O corpus lido não traz a máscara desta
tela, então não dá para concluir que texto o servidor vê no campo — se o código interno ou
um mnemônico. Pergunta ao site.

### RN-07 — A tela só opera com a tela e o código de acesso autorizados

Antes de mostrar a relação, a tela confere, nesta ordem, se o cadastro de telas tem esta
tela e se o meu **código de acesso** tem registro para ela. Faltando a tela, o aviso é
**\* Tela nao disponivel \***; faltando o registro do meu código de acesso, o aviso é
**\* Acesso negado para esta matricula \***. Nos dois casos eu volto ao menu principal e
nada é consultado.

A opção informada e a tela passam, em seguida, pela conferência de permissão de operação.
Como só a consulta é aceita, a conferência da operação não chega a exigir permissão de
inclusão, de alteração ou de exclusão.

### RN-08 — O código da tela de destino leva a transação para aquela tela

Se o servidor preenche o campo do **código da tela de destino**, a transação segue para a
tela informada e mais nada desta tela é processado: a relação não é remontada e o indicador
do mapa não é considerado. Em branco, a tela segue o seu curso normal.

[?] Esse campo não tem rótulo nem valor no material lido, porque não há máscara desta tela;
o que se sabe é o efeito de o servidor preenchê-lo. Pergunta ao site.

### RN-09 — O indicador do mapa entrega a tela seguinte em inclusão

Preenchido o **indicador do mapa**, a tela passa para a tela do mapa de atendimento a ser
aberta o **registro do órgão filho da minha sessão** e a **operação de inclusão**; os
demais dados do registro vão em branco. A tela do mapa abre, por isso, **em inclusão** para
esse órgão filho. Sem o indicador, nada é entregue: a tela apenas volta a mostrar a
relação.

[?] O indicador tem um caractere, não passa por conferência de valor e não tem rótulo no
material lido; o valor que o servidor digita para disparar a passagem não está no corpus.
Pergunta ao site.

[?] A entrega leva o órgão filho e a operação, mas deixa em branco a coordenadoria regional
escolar, que a tela do mapa também usa. Não dá para concluir, só por esta tela, se a tela
seguinte busca a coordenadoria na sessão ou se o servidor a informa lá. Pergunta ao site.

### RN-10 — Consultar não grava nada

A tela só lê. Ela enxerga cinco cadastros: o de telas, o de acessos, o de funcionários, o
de grupos de atendimento e o de segmentos de atendimento. Para três deles — o de telas, o
de grupos e o de segmentos — o sistema traz prontas as operações de gravar e de apagar,
mas **nenhuma delas é executada**: não sai desta tela nenhuma gravação, nenhum travamento
de registro e nenhuma linha de auditoria.

### RN-11 — Falha no banco interrompe a consulta

Toda leitura desta tela testa o erro do banco: o erro vira a ação de erro de acesso, com a
mensagem de erro do sistema, e a operação para ali, sem completar a relação.

## Cenários BDD

```gherkin
Funcionalidade: Consultar os grupos de atendimento do órgão da secretaria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C102C

  Cenário: RN-01, RN-02 e RN-10 — consultar a relação dos grupos de atendimento do órgão
    Dado que estou na tela C102C
    Quando confirmo a consulta
    Então vejo, no cabeçalho, a descrição do órgão da minha secretaria e a data do sistema
    E vejo, em cada linha, o segmento, a descrição resumida do segmento, o grupo, a descrição do grupo e a descrição resumida do grupo
    E nada é gravado

  Cenário: RN-02 — o órgão tem mais grupos do que a página mostra
    Dado que o órgão da minha secretaria tem mais de 15 grupos de atendimento
    Quando confirmo a consulta
    Então vejo 15 grupos na relação
    E a relação segue na ordem do cadastro: primeiro o segmento, e dentro dele o grupo

  Cenário: RN-03 — a relação começa pela referência de grupo da sessão
    Dado que a sessão traz a referência de um grupo de atendimento
    Quando confirmo a consulta
    Então a relação começa por esse grupo

  Cenário: RN-04 — órgão sem grupos de atendimento
    Dado que o órgão da minha secretaria não tem nenhum grupo de atendimento
    Quando confirmo a consulta
    Então vejo "* Nao existe grupos de atendimento cadastrados *"
    E nenhuma linha é preenchida

  Cenário: RN-05 — grupo cujo segmento não está no cadastro de segmentos
    Dado que um grupo de atendimento aponta para um segmento que o órgão não tem cadastrado
    Quando confirmo a consulta
    Então aquela linha mostra o grupo e as suas descrições
    E a descrição resumida do segmento fica em branco

  Cenário: RN-06 — a tela abre em consulta venha de onde vier
    Dado que outra tela me encaminhou para a tela C102C
    Quando a tela abre
    Então o campo da opção vem preenchido com a consulta
    E confirmando sem digitar nada, nenhuma operação é executada e nada é gravado

  Cenário: RN-06 — opção diferente da consulta
    Dado que estou na tela C102C
    Quando informo uma opção de manutenção diferente da consulta e confirmo
    Então vejo "* Operacao nao disponivel *"
    E o cursor volta para o campo da opção
    E nada é gravado

  Cenário: RN-07 — sem o registro de acesso
    Dado que o meu código de acesso não tem registro para esta tela
    Quando a tela abre
    Então vejo "* Acesso negado para esta matricula *"
    E volto ao menu principal
    E nada é consultado

  Cenário: RN-07 — tela fora do cadastro de telas
    Dado que o cadastro de telas não tem esta tela
    Quando a tela abre
    Então vejo "* Tela nao disponivel *"
    E volto ao menu principal

  Cenário: RN-08 — código da tela de destino informado
    Dado que estou na tela C102C
    Quando informo o código de outra tela e confirmo
    Então a transação segue para a tela informada
    E nada mais desta tela é processado

  Cenário: RN-09 — indicador do mapa preenchido
    Dado que a relação mostra os grupos de atendimento do órgão
    Quando preencho o indicador do mapa e confirmo
    Então a tela do mapa de atendimento M040T abre em inclusão para o órgão filho da minha sessão
    E nada é gravado por esta tela

  Cenário: RN-09 — indicador do mapa em branco
    Dado que a relação mostra os grupos de atendimento do órgão
    Quando confirmo sem preencher o indicador do mapa
    Então a tela continua mostrando a relação
    E nenhuma tela se abre

  Cenário: RN-11 — falha do banco durante a consulta
    Dado que a leitura do cadastro falha no banco
    Quando confirmo a consulta
    Então a operação é interrompida com a mensagem de erro do sistema
    E a relação não é completada
```
