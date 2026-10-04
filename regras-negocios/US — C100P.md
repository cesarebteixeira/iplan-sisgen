# US — C100P — Pedir a emissão do relatório comparativo de permissões de contrato entre o período inicial e o período limite

## Estória

Como **servidor de CRE**, quero **pedir a emissão do relatório comparativo de permissões
de contrato informando o grupo escolar, o período inicial e o período limite**, para que
**eu leve à impressora, de uma vez, a posição das permissões daquele grupo nos dois
períodos — com quantidade e valor de cada grupamento — sem ter de levantar os dois lados
por fora do sistema**.

O pedido é a porta pela qual esse relatório sai: quem o faz aponta de qual permissão de
contrato e para qual permissão a comparação deve correr, cada lado com a sua data limite
e o seu tipo de contrato. Sem essa etapa, a emissão correria sem período e sem grupo, ou
com os parâmetros do pedido anterior — e o relatório sairia vazio, com o intervalo
trocado ou apontando para a permissão errada.

## Contexto

Jornada S000M → C000M → C050M → C068M → C680M → C100P.

Ator: servidor de CRE — informa o grupo escolar, o período inicial e o período limite e
pede a emissão do relatório comparativo de permissões de contrato.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O `C000M`, o `C050M` e o `C068M` são menus e
não gravam nada.

O penúltimo passo da jornada, o `C680M`, **não é menu**: é uma tela de preparação que
encadeia direto nesta, sem passar por opção nenhuma. Ele exige a impressora, confere se
quem opera tem e-mail cadastrado, guarda na sessão a impressora e o código de saída do
pedido e manda a sessão para a `C100P` levando o código do relatório. A `C100P` não abre
por menu: ela só é alcançada por esse encadeamento, e o que o `C680M` deixou na sessão é
condição de funcionamento dela. O que a `C100P` usa da sessão — a matrícula, o tipo de
órgão, a estação, a impressora e o código do relatório — vem da entrada e do `C680M`.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela prepara a impressão e só processa o relatório a que está amarrada

A tela é a tela de parâmetros de um relatório, e não de vários: ela recebe da sessão o
código do relatório escolhido no caminho e só segue adiante quando esse código é o do
relatório dela. Com qualquer outro código, a tela aparece igual, nada é conferido, nada é
registrado e quem opera não recebe aviso nenhum.

Além disso, quem prepara a impressão é a tela anterior: ela exige a impressora, guarda na
sessão a impressora e o código de saída do pedido, e só entrega a sessão a esta tela
quando quem opera tem e-mail cadastrado. Por isso esta tela não abre por menu — só se
chega a ela com a impressão já preparada.

[?] O acervo desta jornada não traz nenhuma opção de menu que abra esta tela: o único
caminho encontrado é o encadeamento da tela anterior. Se o relatório deve continuar sem
entrada própria, o acervo lido não diz. Pergunta ao site.

### RN-02 — O pedido tem dois blocos: a permissão inicial e a permissão limite

Cada bloco identifica uma permissão de contrato pelos mesmos dados: a coordenação
regional escolar (o grupo), a data limite — dia, mês e ano — e o tipo de contrato. Os
dois blocos usam o mesmo grupo: não há grupo próprio do bloco limite. O bloco limite tem
ainda o grupamento de licitação, um só para os dois blocos.

A tela mostra também a data do sistema e a descrição do tipo de órgão de quem opera, e
traz a impressora preparada pela tela anterior.

[?] O texto e a posição exata dos campos vêm da máscara da tela, que não faz parte do
acervo lido; o programa diz quais campos cada bloco usa. Pergunta ao site.

### RN-03 — Toda data informada é conferida, campo a campo

As seis datas do pedido — dia, mês e ano iniciais e dia, mês e ano limite —, o grupo, os
dois tipos de contrato e o grupamento passam pela mesma conferência de campo numérico, na
ordem em que aparecem na tela, antes de qualquer conferência de negócio. Campo em branco
conta como zero. A recusa devolve o cursor ao campo errado.

[?] O texto da recusa vem de rotina comum do ambiente, sem corpo nos fontes lidos; o que
o fonte desta tela mostra é só o cursor de volta ao campo. Pergunta ao site.

### RN-04 — O acesso à tela e ao relatório é conferido antes de qualquer parâmetro

Na abertura e na confirmação, a tela passa pela autorização de tela, pela autorização do
relatório, pela rota e pela data e hora do sistema. Sem qualquer uma delas, o
processamento para ali: nada é conferido e nada é registrado.

[?] O texto da recusa por falta de autorização, de rota ou de data e hora não está no
acervo: as rotinas são comuns, sem corpo nos fontes lidos, e a tela só testa o retorno.
Pergunta ao site.

### RN-05 — O tipo de contrato do período inicial não pode ser o mesmo do período limite

Se o tipo de contrato informado para o período inicial for igual ao do período limite, o
pedido é recusado com **\* Mesmo tipo contrato - DE e PARA \*** e não se confere mais
nada. Um tipo de contrato em branco nos dois lados é recusado por esta mesma regra: a
comparação é entre iguais, e dois brancos são iguais.

### RN-06 — A permissão do período inicial tem de estar cadastrada, exatamente como informada

O sistema procura no cadastro das permissões de contrato a permissão do tipo de órgão de
quem opera, com o grupo, a data limite inicial (dia, mês e ano) e o tipo de contrato
inicial informados; a classe, a subclasse e o gênero da permissão entram zerados, porque
a tela não os informa. Permissão marcada como excluída não é encontrada. Não achando, a
recusa é **\* Permissao DE nao cadastrada \***, com o cursor no dia inicial.

Havendo pedido já registrado para o mesmo tipo de órgão, o mesmo grupo e o mesmo
relatório, esta leitura encontra o pedido — e a recusa é a mesma,
**\* Permissao DE nao cadastrada \***. Não há mensagem própria para o pedido em
andamento neste caminho.

[?] O pedido gravado por esta tela sai com a situação dele em branco e a busca não olha
essa situação: um pedido antigo que continue na base bloqueia os pedidos seguintes
daquele grupo, e esta tela não mostra como tirá-lo dali. Quem remove esses pedidos está
fora desta jornada. Pergunta ao site.

### RN-07 — O grupo escolar tem de ser o de quem opera, ou quem opera não tem grupo

Se o cadastro de quem opera tem uma coordenação regional escolar, o grupo informado tem
de ser essa mesma; informar outro é recusa, com **\* Usuario sem acesso a outro grupo \***
e o cursor no grupo. Se quem opera não tem coordenação no cadastro, qualquer grupo passa
nessa conferência.

### RN-08 — O grupo escolar é obrigatório

Sem o grupo o pedido não anda: a recusa é **\* Informe o grupo \***, com o cursor de volta
ao campo.

### RN-09 — A permissão do período limite tem de estar cadastrada, exatamente como informada

A procura é no mesmo cadastro, agora pelo tipo de órgão de quem opera, pelo mesmo grupo,
pela data limite do período limite (dia, mês e ano) e pelo tipo de contrato do período
limite; classe, subclasse e gênero também entram zerados. Não achando, a recusa é
**\* Permissao PARA nao cadastrada \***, com o cursor no dia limite.

### RN-10 — O grupamento de licitação é obrigatório e vale 9999 para todos

Sem o grupamento o pedido não anda: a recusa é
**\* Informe grupamento ou 9999 para todos \***, com o cursor no grupamento. Informado o
grupamento, ele entra também na conferência dos dois lados.

[?] Se o grupamento em branco é para significar "todos", a regra o recusa antes de chegar
lá; quem quer todos tem de digitar 9999. Se era para o branco valer todos, o acervo lido
não diz. Pergunta ao site.

### RN-11 — O grupamento tem de estar cadastrado nas duas permissões, cada uma com o seu tipo de contrato

Cada permissão — a inicial, com o tipo de contrato do período inicial, e a limite, com o
tipo de contrato do período limite — é procurada de novo no cadastro das permissões, agora
também pelo grupamento informado. A que não tiver o grupamento cadastrado para o seu tipo
de contrato é recusada, uma de cada vez, nesta ordem:
**\* Permissao DE - grupamento nao cadastrado \*** e
**\* Permissao PARA - grupamento nao cadastrado \***, com o cursor no grupamento nas duas.

### RN-12 — Passando nas conferências, o pedido é numerado, registrado e entregue à emissão

O sistema toma o próximo número de pedido — o seguinte ao último já registrado — e
registra o pedido com o relatório, o tipo de órgão, o grupo, a data do pedido, a
matrícula, a estação, a impressora da sessão, o órgão e a coordenação de quem opera, e
deixa a situação do pedido em branco. Os parâmetros informados — o grupo, os dois períodos
e os dois tipos de contrato, com o grupamento — seguem com o pedido. Em seguida o sistema
monta a execução do relatório e a entrega ao serviço que dispara a emissão pela impressora
da sessão.

[?] O número do pedido é o último registrado mais um, lido sem travamento: dois pedidos
simultâneos podem receber o mesmo número, e o acervo não diz o que acontece nesse caso.
Pergunta ao site.

[?] O registro guarda, no campo do número de processo, o código do grupo escolar — o mesmo
valor que o campo do grupo já leva. Se isso é intencional ou resto do pedido anterior, o
acervo não diz; outras telas de parâmetro de relatório do sistema fazem o mesmo. Pergunta
ao site.

[?] Há um caminho em que o pedido fica registrado e a execução não é entregue — reservado
a um ambiente diferente do de origem, que o próprio acervo fixa no valor normal. Se esse
caminho ainda tem uso, o acervo não diz. Pergunta ao site.

[?] A tela não mostra mensagem de confirmação depois de registrar o pedido; o que quem
opera vê ao voltar não está no programa. Pergunta ao site.

[?] A tela entrega a execução do relatório e não acompanha o resultado: o que o serviço de
relatórios faz com o pedido — se imprime, se guarda, se devolve erro — não está no acervo
lido. Pergunta ao site.

### RN-13 — A tela só escreve o pedido; os cadastros e a auditoria ficam de fora

Nenhuma permissão de contrato é alterada ou apagada por esta tela: o cadastro das
permissões é só lido. O único registro que ela cria é o do pedido de relatório (`S040T`),
o mesmo cadastro usado pelas outras telas de parâmetro de relatório do sistema. Esse
pedido não deixa rastro na auditoria: o cadastro da auditoria não é sequer declarado por
esta tela.

[?] Se a ausência de rastro é intencional: quem pediu, quando e com que parâmetros não
fica registrado para auditoria. Pergunta ao site.

### RN-14 — Falha de banco interrompe o pedido

Toda leitura e a gravação testam o erro do banco; havendo erro, a transação é
interrompida com a mensagem de erro do sistema e o pedido não é considerado registrado.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedir a emissão do relatório comparativo de permissões de contrato entre o período inicial e o período limite

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C100P

  Cenário: RN-01 e RN-02 — abrir a tela com a impressão preparada pela tela anterior
    Dado que a tela anterior exigiu a impressora e confirmou que tenho e-mail cadastrado
    E que ela me entregou a sessão com o relatório desta tela
    Quando a tela abre
    Então vejo os campos do grupo escolar, do período inicial, do tipo de contrato, do período limite e do grupamento de licitação
    E vejo a data do sistema, a descrição do tipo de órgão da minha sessão e a impressora preparada
    E nada é registrado

  Cenário: RN-01 — abrir a tela com o código de outro relatório
    Dado que a sessão traz o código de um relatório que esta tela não atende
    Quando confirmo o pedido
    Então nada é conferido e nada é registrado
    E não vejo mensagem nenhuma

  Cenário: RN-03 — campo de parâmetro que não é número
    Quando informo, em um dos campos de parâmetro, algo que não é número
    Então a tela recusa o campo
    E o cursor volta ao campo errado
    E nada é registrado

  Cenário: RN-04 — sem autorização para a tela ou para o relatório
    Dado que o meu acesso não autoriza esta tela ou este relatório
    Quando confirmo o pedido
    Então a tela não confere nenhum parâmetro
    E nada é registrado

  Cenário: RN-05 — mesmo tipo de contrato nos dois períodos
    Dado que informo o mesmo tipo de contrato para o período inicial e para o período limite
    Quando confirmo
    Então vejo "* Mesmo tipo contrato - DE e PARA *"
    E nada é registrado

  Cenário: RN-06 — permissão do período inicial não cadastrada
    Quando informo um grupo, um período inicial e um tipo de contrato que não formam uma permissão cadastrada
    Então vejo "* Permissao DE nao cadastrada *"
    E o cursor volta ao dia inicial
    E nada é registrado

  Cenário: RN-06 — já existe pedido registrado para o grupo e o relatório
    Dado que já existe pedido registrado para o meu tipo de órgão, o grupo informado e este relatório
    Quando confirmo o pedido
    Então vejo "* Permissao DE nao cadastrada *"
    E nada é registrado

  Cenário: RN-07 — grupo fora do grupo de quem opera
    Dado que o meu cadastro tem coordenação regional escolar
    Quando informo outro grupo
    Então vejo "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao grupo

  Cenário: RN-07 — sem coordenação no meu cadastro, o grupo é livre
    Dado que o meu cadastro não tem coordenação regional escolar
    Quando informo qualquer grupo
    Então essa conferência não me recusa

  Cenário: RN-08 — grupo em branco
    Quando confirmo sem informar o grupo
    Então vejo "* Informe o grupo *"
    E nada é registrado

  Cenário: RN-09 — permissão do período limite não cadastrada
    Quando informo, para o período limite, uma combinação de grupo, data limite e tipo de contrato que não está cadastrada
    Então vejo "* Permissao PARA nao cadastrada *"
    E o cursor volta ao dia limite
    E nada é registrado

  Cenário: RN-10 — grupamento em branco
    Quando confirmo sem informar o grupamento
    Então vejo "* Informe grupamento ou 9999 para todos *"
    E o cursor volta ao grupamento
    E nada é registrado

  Cenário: RN-10 e RN-12 — pedir o relatório de todos os grupamentos
    Dado que as duas permissões estão cadastradas, exatamente como informadas
    E informo 9999 no grupamento
    Quando confirmo
    Então o pedido é registrado
    E a execução da emissão é entregue ao serviço de relatórios

  Cenário: RN-11 — grupamento não cadastrado na permissão do período inicial
    Dado que a permissão do período inicial não tem o grupamento informado cadastrado para o tipo de contrato inicial
    Quando confirmo
    Então vejo "* Permissao DE - grupamento nao cadastrado *"
    E nada é registrado

  Cenário: RN-11 — grupamento não cadastrado na permissão do período limite
    Dado que a permissão do período limite não tem o grupamento informado cadastrado para o tipo de contrato limite
    Quando confirmo
    Então vejo "* Permissao PARA - grupamento nao cadastrado *"
    E nada é registrado

  Cenário: RN-12 e RN-13 — pedir a emissão com as duas permissões cadastradas
    Dado que a permissão do período inicial e a do período limite existem, exatamente como informadas
    E o grupamento está cadastrado nas duas, cada uma com o seu tipo de contrato
    E não há pedido em andamento para o grupo e o relatório
    Quando confirmo
    Então o pedido é registrado com o relatório, o tipo de órgão, o grupo, a data do pedido, a minha matrícula, a estação, a impressora da sessão, o órgão e a coordenação de quem opera
    E a situação do pedido fica em branco
    E os parâmetros informados seguem com o pedido
    E a execução da emissão é entregue ao serviço de relatórios
    E nenhuma permissão de contrato é alterada

  Cenário: RN-13 — recusa não registra nada
    Dado que confirmo um pedido com um parâmetro em falta ou com uma permissão não cadastrada
    Quando a tela recusa
    Então nenhum pedido é registrado
    E nenhuma permissão de contrato é alterada

  Cenário: RN-13 — o pedido não fica na auditoria
    Quando o pedido é registrado
    Então o único registro criado é o do pedido de relatório
    E a auditoria não registra quem pediu nem com que parâmetros

  Cenário: RN-14 — falha de banco durante o registro do pedido
    Dado que a gravação do pedido falha no banco
    Quando confirmo o pedido
    Então a transação é interrompida com a mensagem de erro do sistema
    E o pedido não é considerado registrado
```
