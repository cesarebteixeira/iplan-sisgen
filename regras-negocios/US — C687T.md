# US — C687T — Cancelamento da prorrogação da permissão de contrato da coordenação regional escolar

## Estória

Como **servidor da CRE que responde pela permissão de contrato**, quero **cancelar a prorrogação
registrada na permissão de contrato da minha coordenação regional escolar**, para que **a
quantidade e o valor que a prorrogação acrescentou deixem de contar no contrato e os saldos
voltem a refletir o que de fato será fornecido**.

A permissão de contrato é o que autoriza um fornecedor, dentro de um contrato de uma coordenação
regional escolar, de um grupamento de licitação e de um período, a fornecer cada item — uma
classe, uma subclasse e um gênero. A prorrogação é registrada à parte, e o que ela acrescenta fica
somado à permissão, item por item. Enquanto ninguém cancela, o contrato segue autorizando uma
quantidade e um valor que não vão ser entregues, e o total de prorrogação do contrato fica acima
do real. Cancelar é desfazer esse acréscimo: a permissão volta ao que era, o item deixa de contar
com a prorrogação e a operação fica registrada na auditoria.

## Contexto

Jornada S000M → C000M → C050M → C664M → C687T.
Ator: servidor de CRE — consulta a permissão de contrato da sua coordenação regional escolar com as
prorrogações registradas nela e cancela a prorrogação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

A jornada termina nesta tela: ela não abre outra, e as únicas saídas dela são as rotinas do
ambiente que ela chama. O menu que a abre não lhe entrega contrato nenhum — é esta tela que pede a
identificação ao servidor —, e ela abre em consulta. O tipo de órgão e a coordenação regional da
sessão, a matrícula, o código de acesso, o privilégio, a estação, a data do sistema e a descrição
do tipo de órgão chegam pela sessão, deixados pela entrada; esta tela não os recalcula.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela cancela a prorrogação e não apaga registro nenhum

A tela grava três coisas: regrava a permissão de contrato do item, devolvendo-lhe a quantidade e o
valor prorrogados; zera a quantidade e o valor no registro da prorrogação; e cria o rastro na
auditoria. **Nada é apagado** — a prorrogação continua cadastrada, apenas sem quantidade e sem
valor.

A tela enxerga **sete** cadastros e traz declaradas, para cada um, uma rotina de gravar e uma de
apagar — quatorze ao todo. Dessas, executa **três**: a regravação da permissão, a regravação da
prorrogação e a criação do rastro. **Nenhuma** das sete rotinas de apagar é executada por caminho
nenhum. As capacidades são de dimensionamento, não de volume cadastrado: as permissões de contrato
comportam 1.000.000 de registros, as prorrogações 30.000, a auditoria 60.000.000, os gêneros
150.000, os fornecedores 10.000, o cadastro de telas 2.000 e os tipos de órgão 200.

### RN-02 — A tela só atende à consulta e ao cancelamento, e abre em consulta

A tela tem um modo de manutenção que só admite dois valores: **consulta** e **exclusão** — os
mesmos que a recusa nomeia como **EXC** e **CON**. Qualquer outro valor é recusado com
**\* Opcao nao disponivel. Use EXC ou CON \***, com o cursor no campo do modo, e nada é lido nem
gravado. Abrindo sem modo informado, a tela assume sozinha a consulta.

[?] A guarda compara o modo informado com o código interno da exclusão e o da consulta, e a
mensagem manda usar "EXC" e "CON". Se as duas palavras não forem as mesmas depois de o terminal
traduzir o mnemônico, a tela recusa justamente os dois modos que ela aceita e fica inutilizável.
Pergunta ao site.

### RN-03 — A permissão e a prorrogação são localizadas pela coordenação regional, pelo tipo de contrato, pelo grupamento de licitação e pelo limite do período

Para chegar à permissão, o servidor informa a **coordenação regional escolar**, o **tipo de
contrato**, o **grupamento de licitação** e o **dia, o mês e o ano do limite do período**; o **tipo
de órgão vem da sessão** e é a primeira parte da identificação. São **seis** os campos de
identificação em que a tela devolve o cursor quando a digitação é recusada — a coordenação
regional, o tipo de contrato, o grupamento de licitação e as três partes do limite do período. As
prorrogações do contrato são procuradas pela mesma identificação. O código do fornecedor e o
início do período, que também se digitam, **não** fazem parte dessa busca.

### RN-04 — O que a tela mostra vem do cadastro e da sessão, não do que se digita

Os demais campos da tela existem para exibição: o código do fornecedor, o início do período, o
valor adjudicado, o valor aditivo e o valor de prorrogação. Ainda que o servidor os digite, a tela
os substitui pelo que está gravado na permissão antes de exibir. O fornecedor mostrado é o da
permissão: a razão social é buscada no cadastro de fornecedores pelo código que a permissão traz.
A descrição do tipo de órgão e a data do sistema vêm da sessão.

[?] O código do fornecedor, o início do período e os três valores são conferidos como número, mas a
tela sempre os substitui pelo que está na permissão, e o valor de prorrogação digitado é novamente
substituído, no fim, pelo total que a própria tela calcula: ou esses campos servem para
conferência, ou a tela ignora o que o servidor digita. Pergunta ao site.

### RN-05 — A tela só atende à coordenação regional da sessão

Quando a sessão do servidor tem uma coordenação regional, a coordenação informada tem de ser a
mesma; informando outra, a recusa é **\* Usuario sem acesso a este grupo \*** — a mensagem chama a
coordenação regional de **grupo** —, o cursor volta ao campo da coordenação regional e nada é lido
nem gravado. Quando a sessão não tem coordenação regional, a tela não impõe essa restrição.

[?] A conferência compara a coordenação informada com a coordenação de um **segundo** contexto de
sessão, e nenhum programa desta jornada escreve nesse segundo contexto. Se ele chega zerado, a
guarda não distingue nada e a restrição não vale. Pergunta ao site.

### RN-06 — Sem permissão cadastrada, a consulta é recusada

Não estando a permissão registrada para o tipo de órgão da sessão, a coordenação regional, o tipo
de contrato, o grupamento de licitação e o limite do período informados, a recusa é
**\* Permissao nao cadastrada \***, o cursor volta à coordenação regional e nada mais é lido nem
exibido. Consultar duas vezes os mesmos dados não relê o cadastro: a segunda passagem reapresenta o
que já está na tela.

### RN-07 — Sem prorrogação com quantidade, a consulta é recusada

Achada a permissão, ela tem de ter prorrogação registrada para a mesma identificação. Não tendo, a
recusa é **\* Prorrogacao nao cadastrada \***, com o cursor no ano do limite do período. Tendo, mas
com a quantidade prorrogada zerada — prorrogação já cancelada —, a recusa é
**\* Nao existem quantidades prorrogadas \***, com o mesmo cursor. É a segunda recusa que impede
reler um contrato já cancelado.

[?] A falta de prorrogação é dita **duas vezes com o mesmo texto**, em pontos diferentes: a
apresentação da grade escreve o aviso quando não encontra prorrogação para o que a área de trabalho
guardou, e a conferência da consulta o escreve quando não encontra prorrogação para o que o
servidor informou. Não consegui determinar qual dos dois o servidor vê em cada caso. Pergunta ao
site.

### RN-08 — A grade tem doze linhas, uma por prorrogação com quantidade

A grade tem **doze** linhas, uma por prorrogação registrada que ainda tenha quantidade, e para na
primeira linha sem prorrogação. Cada linha traz a subclasse, o gênero, a descrição resumida do
gênero, a quantidade prorrogada e o valor prorrogado. A grade só é montada nos modos de consulta e
de exclusão.

[?] A descrição do gênero é buscada no cadastro de gêneros tomando o **limite do período**
informado como se fosse a data de início do registro do gênero — e esse cadastro é versionado pela
data de início. O efeito é a linha ficar sem descrição sempre que não houver registro de gênero
começando exatamente nessa data. O material não explica por que o limite serve de referência.
Pergunta ao site.

### RN-09 — O cancelamento exige a consulta anterior dos mesmos dados

O cancelamento só é aceito para a permissão que a tela acabou de apresentar: se a coordenação
regional, o tipo de contrato, o grupamento de licitação ou as três partes do limite do período
informados não forem os da última consulta registrada naquela sessão, a recusa é
**\* Consulte antes de excluir \***, com o cursor no campo do modo, e nada é lido nem gravado.

### RN-10 — O cancelamento exige a quantidade a cancelar e recusa quando o saldo fica abaixo do já pedido

O cancelamento é pedido com a quantidade a cancelar na linha da grade. Sem quantidade informada, a
tela não confere saldo nenhum e segue. Com quantidade, a tela procura a permissão do item daquela
linha e exige que, tirando a quantidade a cancelar, o que sobra ainda cubra a quantidade já pedida
daquele item; não cobrindo, a recusa é **\* Quantidade prorrogada ja pedida \***, com o cursor no
ano do limite do período, e nada é gravado.

[?] A quantidade que a conferência usa é a que o servidor digitou, e a que a gravação devolve é a
que está gravada na prorrogação: digitando um valor diferente do que a grade mostra, a conferência
aprova ou recusa por um número, e a gravação aplica outro. Pergunta ao site.

### RN-11 — A confirmação no pé da tela é o que executa o cancelamento

No pé da tela existe um campo de confirmação. Enquanto ele não está marcado, a passagem apenas
confere: nada é regravado e nada é auditado. Marcado, e desde que a conferência não tenha recusado
nada, a tela cancela. A tela escreve esse campo como não confirmado quando se apresenta e o repõe
como não confirmado quando recusa alguma coisa. Nenhum caminho do sistema o marca.

[?] Quem marca a confirmação é a estação de trabalho — o campo faz parte do registro da transação e
nenhum dos 506 programas do acervo marca o próprio campo de confirmação. O acervo não tem a máscara
da tela, e por isso não se sabe se o campo é digitável pelo servidor. Se ele não puder ser marcado,
o cancelamento nunca é gravado e a tela fica só de consulta. Pergunta ao site.

### RN-12 — O cancelamento percorre todas as prorrogações do contrato, devolve à permissão e zera a prorrogação

Confirmado o cancelamento, a tela percorre **todas** as prorrogações daquele contrato que ainda
tenham quantidade — não apenas a linha que o servidor indicou — e, para cada uma, procura a
permissão daquele item e devolve a ela a quantidade e o valor prorrogados, zerando em seguida a
quantidade e o valor no registro da prorrogação. O registro da prorrogação permanece cadastrado;
nada é apagado.

[?] A conferência usa a linha e a quantidade que o servidor digitou, e a gravação não olha para
nenhuma das duas: ela percorre todas as prorrogações do contrato e devolve o que está gravado em
cada uma. Quem pede o cancelamento de uma linha cancela o contrato inteiro, e o número digitado não
é o número devolvido. Ou a gravação deveria respeitar a linha digitada, ou a tela não deveria
pedi-la. Pergunta ao site.

### RN-13 — O valor de prorrogação do contrato é recalculado e regravado em todos os itens

Terminado o cancelamento, a tela percorre **todos** os itens da permissão do mesmo contrato e
regrava em cada um o valor de prorrogação do contrato: a soma dos valores prorrogados dos itens, já
sem o que foi devolvido. Ao final a tela escreve **Cadastro Atualizado**.

[?] A tela recalcula e regrava o valor de prorrogação de todos os itens, e avisa
"Cadastro Atualizado", mesmo quando não havia prorrogação nenhuma a cancelar: a passagem repetida
de um cancelamento já feito deixa rastro na auditoria sem mudar o cadastro. Se era para avisar que
nada havia a cancelar, o material não diz. Pergunta ao site.

### RN-14 — Toda gravação deixa rastro na auditoria

Cada cancelamento cria registros de auditoria: um para a permissão do item, um para a prorrogação
daquele item e um para cada item do contrato na regravação do total — sempre com a operação de
alteração, a imagem do registro antes e a depois, o objeto auditado, e a matrícula, o órgão, a
coordenação regional, a estação, a data e a hora da sessão e o número do processo. O rastro é
criado, nunca alterado.

[?] O número do processo que o rastro guarda é o tipo de contrato, e nada no material diz se é
assim mesmo ou se o campo deveria receber o número do processo do contrato. Pergunta ao site.

### RN-15 — Nada é lido, conferido nem gravado sem a autorização de perfil, de rota e de operação

Antes de apresentar, a tela passa pela rotina de segurança: confere a matrícula no cadastro de
funcionários e exige que a estação da sessão seja a do cadastro; confere a tela no cadastro de
telas (senão **\* Tela nao disponivel \***); e confere o código de acesso contra o perfil (senão
**\* Acesso negado para esta matricula \***). Antes de conferir, passa pela rota do sistema, que
recusa com **\* Tela nao cadastrada \*** quando a tela está apagada do cadastro de telas e devolve
o controle à tela anterior quando a transação traz uma; e passa pela autorização por operação, que,
no cancelamento, exige o **flag de exclusão** no perfil do servidor — sem ele,
**\* Acesso negado para esta operacao \***. Antes de cada gravação, passa pela rotina de data e
hora. Não voltando "OK" de qualquer uma delas, a transação é abandonada: nada é lido, nada é
gravado e nenhum rastro é criado.

[?] Nenhuma tela deste caminho entrega a esta tela um código de tela anterior, e a máscara dela não
está no acervo: não se sabe em que caso esse código chega preenchido nem para que tela a transação
voltaria — e, chegando preenchido, esta tela não processa nada. Pergunta ao site.

### RN-16 — Todo campo digitável é conferido como número, e seis deles devolvem o cursor

Os **dezessete** campos numéricos da tela passam pela conferência numérica, cada um com o tamanho
que o dicionário declara: a coordenação regional com 2 dígitos, o tipo de contrato com 3, o código
do fornecedor e o grupamento de licitação com 4, os dias e os meses com 2 e os anos com 4, os
valores com 11 inteiros e 2 decimais, a quantidade prorrogada com 7 inteiros e 3 decimais e o valor
prorrogado com 8 inteiros e 2 decimais. O campo em branco vira zero. O que não for número é
recusado, e a tela devolve o cursor a **seis** deles — a coordenação regional, o tipo de contrato,
o grupamento de licitação e as três partes do limite do período; os outros onze são recusados sem
posicionar o cursor.

[?] O texto da recusa por campo não numérico não está no fonte da tela: ele vem da rotina de
edição, que só aparece declarada no material. O que o operador lê nesse caso não pôde ser
conferido. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Cancelamento da prorrogação da permissão de contrato da coordenação regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C687T

  Cenário: RN-03, RN-04 e RN-08 — consultar a permissão e as suas prorrogações
    Dado que estou na tela C687T no modo de consulta
    E informo a coordenação regional, o tipo de contrato, o grupamento de licitação e o dia, o mês e o ano do limite do período
    Quando confirmo a consulta
    Então vejo o fornecedor da permissão com a sua razão social, o início do período, o valor adjudicado, o valor aditivo e o valor de prorrogação
    E vejo, em cada linha, a subclasse, o gênero com a descrição, a quantidade prorrogada e o valor prorrogado
    E nada é gravado

  Cenário: RN-01, RN-11 e RN-12 — cancelar a prorrogação de um contrato
    Dado que consultei uma permissão que tem prorrogação com quantidade
    E informo o modo de exclusão com a quantidade a cancelar
    Quando marco a confirmação no pé da tela e confirmo
    Então a quantidade e o valor prorrogados são devolvidos à permissão de contrato do item
    E a quantidade e o valor ficam zerados no registro da prorrogação
    E o registro da prorrogação continua cadastrado
    E vejo "Cadastro Atualizado"

  Cenário: RN-12 — o cancelamento alcança todas as prorrogações do contrato
    Dado que o contrato tem prorrogação com quantidade em mais de uma linha
    E consultei uma permissão do contrato
    Quando confirmo a exclusão de uma única linha
    Então todas as prorrogações daquele contrato ficam sem quantidade e sem valor
    E a permissão de cada item recebe de volta o que a sua prorrogação tinha

  Cenário: RN-01 — nada é apagado
    Dado que cancelei uma prorrogação na C687T
    Quando a gravação termina
    Então nenhum registro de permissão, de prorrogação, de fornecedor ou de auditoria é apagado

  Cenário: RN-02 — modo de manutenção diferente de excluir e de consultar
    Dado que estou na tela C687T
    Quando informo um modo diferente de EXC e de CON
    Então vejo "* Opcao nao disponivel. Use EXC ou CON *"
    E o cursor fica no campo do modo
    E nada é lido nem gravado

  Cenário: RN-02 — a tela abre em consulta
    Dado que abro a tela C687T pela opção 5 do menu C664M
    Então ela abre no modo de consulta
    E nenhum cadastro é lido

  Cenário: RN-05 — coordenação regional fora da minha sessão
    Dado que o meu usuário está preso a uma coordenação regional
    Quando informo outra coordenação regional
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo da coordenação regional
    E nada é lido nem gravado

  Cenário: RN-06 — permissão não cadastrada
    Dado que estou na tela C687T
    Quando informo uma coordenação regional, um tipo de contrato, um grupamento de licitação e um limite de período que não têm permissão
    Então vejo "* Permissao nao cadastrada *"
    E o cursor fica no campo da coordenação regional
    E nada é exibido

  Cenário: RN-06 — a consulta repetida não relê o cadastro
    Dado que consultei uma permissão e os seus dados ficaram na tela
    Quando confirmo a consulta com os mesmos dados
    Então a tela reapresenta o que já estava na tela
    E nada é gravado

  Cenário: RN-07 — permissão sem prorrogação cadastrada
    Dado que a permissão existe e não tem prorrogação registrada
    Quando confirmo a consulta
    Então vejo "* Prorrogacao nao cadastrada *"
    E o cursor fica no ano do limite do período
    E nada é exibido

  Cenário: RN-07 — prorrogação sem quantidade
    Dado que a permissão tem prorrogação e todas as linhas estão sem quantidade
    Quando confirmo a consulta
    Então vejo "* Nao existem quantidades prorrogadas *"
    E nenhuma linha é exibida

  Cenário: RN-08 — a grade para na primeira linha sem prorrogação
    Dado que a permissão tem prorrogação com quantidade em duas linhas
    Quando confirmo a consulta
    Então vejo duas linhas preenchidas
    E as outras dez linhas ficam vazias

  Cenário: RN-09 — cancelamento sem a consulta anterior
    Dado que estou na tela C687T e nunca consultei este contrato
    Quando informo o modo de exclusão com uma coordenação regional, um tipo de contrato, um grupamento de licitação ou um limite de período diferentes dos da última consulta
    Então vejo "* Consulte antes de excluir *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-10 — cancelamento que deixaria o saldo abaixo do já pedido
    Dado que consultei uma permissão cujo item tem quantidade já pedida
    Quando informo uma quantidade a cancelar que faz o saldo do item ficar abaixo da quantidade já pedida
    Então vejo "* Quantidade prorrogada ja pedida *"
    E o cursor fica no ano do limite do período
    E nada é gravado

  Cenário: RN-10 — cancelamento sem quantidade informada
    Dado que consultei uma permissão que tem prorrogação
    Quando informo o modo de exclusão sem a quantidade a cancelar
    Então a tela não confere o saldo do item
    E segue para a passagem de gravação

  Cenário: RN-11 — cancelamento sem a confirmação no pé da tela
    Dado que consultei uma permissão e pedi a exclusão
    Quando não marco a confirmação no pé da tela
    Então a prorrogação continua com a quantidade e o valor anteriores
    E a permissão continua com os saldos anteriores
    E nenhum registro de auditoria é criado

  Cenário: RN-13 — o valor de prorrogação do contrato é regravado em todos os itens
    Dado que cancelei uma prorrogação na C687T
    Quando a gravação termina
    Então o valor de prorrogação do contrato passa a ser a soma dos valores prorrogados dos itens, já sem o que foi devolvido
    E esse valor é regravado em todos os itens do contrato

  Cenário: RN-14 — todo cancelamento deixa rastro na auditoria
    Dado que cancelei uma prorrogação na C687T
    Quando a gravação termina
    Então existe um registro de auditoria da permissão do item e outro da prorrogação, com a operação de alteração
    E cada um com a imagem do registro antes e a depois
    E com a matrícula, o órgão, a coordenação regional, a estação, a data e a hora

  Cenário: RN-15 — sem o acesso à tela
    Dado que a minha matrícula não tem o perfil de acesso a esta tela
    Quando confirmo
    Então vejo "* Acesso negado para esta matricula *"
    E nada é lido nem gravado

  Cenário: RN-15 — sem o flag de exclusão no perfil
    Dado que o meu perfil não permite excluir nesta tela
    Quando informo o modo de exclusão e confirmo
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-16 — campo não numérico
    Dado que estou na tela C687T
    Quando informo letras no campo do ano do limite do período
    Então a tela recusa a digitação e devolve o cursor ao campo
    E nada é lido nem gravado
```
