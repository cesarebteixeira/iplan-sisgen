# US — C207T — Projetos vinculados ao órgão

## Estória

Como **servidor de CRE**, quero **vincular e desvincular projetos aos órgãos da minha
secretaria**, para que **cada órgão fique classificado pelos projetos que executa e a
secretaria consiga ver, por projeto, quais órgãos o atendem**.

O cadastro de órgãos diz quais órgãos existem; o cadastro de projetos diz quais projetos a
secretaria executa. **É nesta tela que os dois são amarrados.** Sem esse vínculo o órgão não
aparece em nenhuma relação por projeto — e o projeto não pode ser apagado, porque a tela que
o mantém recusa a exclusão enquanto houver órgão vinculado a ele. Esta tela **não cria nem
altera** órgão nem projeto: ela exige que os dois já estejam cadastrados e só liga e desliga.

## Contexto

Jornada S000M → C000M → C200M → C207T.

Ator: servidor de CRE — mantém, na secretaria a que tem acesso, os projetos vinculados a
cada órgão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As duas telas anteriores da jornada são menus: a `C000M` encaminha para a `C200M` e a `C200M`
encaminha para a `C207T`. Nenhuma delas passa registro nem operação: a `C207T` abre sem dado
de negócio vindo de quem a chamou, e o modo de trabalho é o que ela mesma assume ou o que o
operador informa. A `C207T` é a última da jornada — não encadeia para outra tela.

As regras abaixo são só as da tela desta jornada: a secretaria, a matrícula, o privilégio, a
CRE e o órgão do usuário são o que a entrada deixou na sessão, e a `C207T` apenas os repassa
às conferências de acesso e de rota.

## Regras de negócio

### RN-01 — A tela mantém o vínculo entre o órgão e o projeto

O que a tela cria e apaga é o **vínculo**: o par **órgão + projeto** dentro de uma
**secretaria**, guardando também a **coordenadoria** do órgão. O conjunto **secretaria +
órgão + projeto** identifica o vínculo e não admite repetição — um projeto só se liga uma vez
ao mesmo órgão. O cadastro de vínculos tem **4 campos** e capacidade para **1.000** registros;
o cadastro de órgãos tem **27 campos** e capacidade para **12.000**; o de projetos tem **3
campos** e capacidade para **1.000**. Capacidade é o máximo esperado, parâmetro de
dimensionamento — não é volume cadastrado.

### RN-02 — A tela só liga e desliga: não altera órgão nem projeto

Esta tela **não inclui, não altera e não apaga** órgão nem projeto. O órgão e o projeto são
apenas **lidos** — o órgão para conferir a que secretaria e a que grupo pertence e para
mostrar o nome, o projeto para conferir que existe e para mostrar a descrição. O que a tela
grava é o vínculo e o rastro da operação na auditoria. Quem cadastra o projeto é outra tela;
quem cadastra o órgão, outra ainda.

### RN-03 — A página tem o órgão no cabeçalho e 13 projetos nas linhas

O cabeçalho da página traz o **órgão** (o campo que a tela chama de ORGAO FILHO SDI), o
**nome do órgão**, a **coordenadoria** (COORD.REG.ESCOLA), se o órgão **é creche** (Sim/Não),
a **descrição do tipo de órgão**, a **data do sistema**, a **opção de manutenção** da página e
o código de uma eventual **tela de continuação**. Abaixo vêm **13 linhas**, cada uma com o
**código do projeto** (2 dígitos), a **descrição do projeto** (40 caracteres) e a **ação** (1
caractere).

[?] O cadastro do órgão guarda o nome com 40 caracteres e a página mostra 24: se a intenção
era exibir o nome inteiro, a coluna perde 16 caracteres. Pergunta ao site.

[?] A página mostra 13 vínculos por vez; se o órgão tiver mais, quem mostra o resto é o
mecanismo de releitura do sistema, que não está no lote lido. Se a intenção era paginar, o
site confirma como.

### RN-04 — A opção da página só admite alteração e consulta

A opção de manutenção da página admite dois valores: **alteração** e **consulta**. Qualquer
outro valor é recusado com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no
campo da opção, e nada é processado. A recusa por opção inválida é dada no processamento da
primeira linha da página — é ela que representa a opção de toda a página; as linhas seguintes
só distinguem consulta de alteração.

[?] A correspondência entre o texto que a tela exibe (ALT, CON) e as operações internas de
alteração e de consulta vem da própria mensagem e não é confirmada em nenhum ponto do fonte
desta jornada. É pergunta ao site.

### RN-05 — A tela abre em consulta e lembra a última opção

Ao ser montada, se não houver opção na área de trabalho da sessão, a tela assume sozinha a
**consulta**; se houver, ela repete a última opção usada. É por isso que a tela pode ser
aberta sem que o operador escolha a opção de manutenção.

### RN-06 — A consulta carrega o órgão e lista os projetos vinculados

Informado o órgão, o sistema carrega os dados dele — nome, coordenadoria e se é creche — e
percorre os vínculos, mostrando em cada linha o código do projeto e a sua descrição. O órgão
já vem preenchido quando o acesso do operador está limitado a um órgão.

### RN-07 — Órgão sem nenhum projeto vinculado avisa

Quando o órgão consultado não tem nenhum projeto vinculado, a página não mostra linha alguma
e avisa **\* Orgao sem projetos cadastrados \***. O aviso é dado uma única vez, no
processamento da primeira linha da página.

### RN-08 — A consulta não grava nada

Com a opção em **consulta**, a tela para: não valida linha nenhuma e não grava vínculo nem
rastro de auditoria. É a garantia de que a consulta é somente leitura — mesmo que o operador
marque ações nas linhas, nada é incluído nem excluído.

### RN-09 — Linha sem projeto, ou com ação desconhecida, é ignorada

Uma linha só é processada se o **código do projeto** estiver preenchido **e** a **ação** for
inclusão (**I**) ou exclusão (**E**). Código zerado, ação em branco ou ação que não seja uma
dessas duas passa batido: não gera recusa nem gravação. Não existe ação de alteração, porque o
vínculo não tem dado a alterar além dos próprios códigos.

### RN-10 — A inclusão recusa vínculo repetido e projeto não cadastrado

A ação **I** inclui o vínculo. Antes, o sistema procura o vínculo pela secretaria, pelo órgão
e pelo projeto: se ele já existe, recusa com **\* Orgao ja cadastrado neste projeto \***. Se
não existe, procura o **projeto** na secretaria do usuário: não estando cadastrado, recusa com
**\* Projeto nao cadastrado \***. Passando nas duas conferências, o vínculo é gravado.

### RN-11 — A exclusão exige o vínculo

A ação **E** apaga o vínculo. O sistema procura o vínculo pela secretaria, pelo órgão e pelo
projeto: não existindo, recusa com **\* Orgao nao cadastrado neste projeto \***. Existindo, o
registro é relido, o conteúdo anterior vai para a auditoria, o registro é travado e o vínculo é
apagado.

### RN-12 — O órgão tem de existir, não estar excluído e estar completo

Antes de trabalhar com um órgão que não seja o já carregado na sessão, o sistema procura-o no
cadastro de órgãos. Não existindo, recusa com **\* Orgao nao cadastrado \***; e os registros
marcados como **excluídos** são pulados — o sistema avança para o próximo registro do mesmo
código. Existindo, exige que **seis** dados estejam preenchidos — o **bairro**, o **órgão a
que está subordinado**, o **nome**, o **endereço**, a **quantidade de matrículas** e a
**quantidade de pessoas** — e recusa com **\* Orgao cadastrado com dados incompletos \*** se
faltar qualquer um deles.

[?] Essa exigência é dispensada quando o órgão informado é o mesmo que já está carregado na
sessão — e é assim que o órgão do próprio usuário entra. O mesmo órgão, então, passa ou não
pela conferência conforme o acesso do operador. Pergunta ao site.

### RN-13 — O órgão tem de ser da secretaria e do grupo do usuário

Ainda sobre o órgão informado: ele tem de pertencer à **secretaria do usuário** — senão a
recusa é **\* Orgao nao pertence a esta secretaria \***. E, quando o acesso do usuário está
limitado a uma **coordenadoria**, o órgão tem de ser daquela coordenadoria — senão a recusa é
**\* Usuario sem acesso ao grupo deste orgao \***.

### RN-14 — O órgão é obrigatório, e o acesso restrito só alcança o próprio órgão

Na consulta, o órgão tem de ser informado: em branco, a recusa é **\* Informe o orgao \***. E,
quando o acesso do usuário está limitado a um órgão, a consulta só alcança aquele: informado
outro, a recusa é **\* Usuario sem acesso a outro orgao \***.

[?] A restrição por órgão depende de o órgão do acesso chegar preenchido à tela: a entrada
guarda esse dado em uma área da sessão e a tela o lê de outra, e a passagem de uma para a
outra não aparece nos fontes desta jornada. Se a passagem não acontecer, a restrição nunca se
aplica e o órgão chega em branco. Pergunta ao site.

### RN-15 — Consultar antes de atualizar

Para alterar, o órgão informado tem de ser **o mesmo que já está carregado na sessão** — isto
é, o que foi consultado. Se não for, a recusa é **\* Consulte antes de atualizar \***, com o
cursor no campo do órgão, e nada é gravado. O caminho normal é: consultar o órgão, ver os
vínculos e, na mesma sessão, enviar a página em modo de alteração.

### RN-16 — Toda inclusão e toda exclusão deixam rastro na auditoria

Cada vínculo incluído ou apagado grava, além do próprio vínculo, um registro no cadastro de
auditoria com a tela de onde partiu a operação, a operação (**inclusão** ao ligar, **exclusão**
ao desligar), o conteúdo anterior e o posterior do vínculo, a matrícula do servidor, a estação,
o número do processo, a sessão (dia, mês, ano e hora) e o tipo de órgão. O cadastro de
auditoria tem **15 campos** e capacidade para 60 milhões de registros — capacidade declarada,
não volume.

[?] No ramo da inclusão a auditoria está sob uma condição do status do processamento; no ramo
da exclusão não há essa condição. O que é esse status e por que só a inclusão o testa é
pergunta ao site.

### RN-17 — Nada é gravado sem as conferências de tela, de acesso e de operação

Antes de gravar, a tela passa por três conferências: a da **tela** (a estação da sessão tem de
ser a mesma da estação registrada para o servidor e a tela tem de estar registrada para o
módulo), a do **acesso** e a da **operação**. A conferência da operação é feita linha a linha:
o perfil do usuário tem de liberar **incluir** e **excluir**, e a opção de alteração da página
tem a sua própria conferência. Faltando qualquer uma, a operação é recusada com mensagem e a
manutenção é abandonada sem gravar. As conferências recebem o contexto da sessão: a matrícula,
o código de acesso, o privilégio, o tipo de órgão e a CRE.

[?] A consulta não confere nenhuma liberação de consulta: quem tem a tela autorizada consulta,
mesmo que exista no cadastro uma marca de consulta liberada que a conferência não lê. Se a
intenção era exigir essa marca, o caminho não a exige.

[?] A conferência da exclusão é precedida de um teste de um sinal em tempo real cujo valor a
tela não define; com o sinal ligado, a exclusão não confere a liberação de exclusão. O que
preenche esse sinal não está no lote lido. Pergunta ao site.

### RN-18 — A recusa de uma linha impede a gravação da página inteira

A validação percorre **todas** as linhas da página antes de qualquer gravação. Se qualquer
linha for recusada, a transação é abandonada e **nenhum** vínculo da página é gravado — nem o
das linhas válidas. A gravação só começa depois de a página inteira passar.

[?] Quem liga o sinal de recusa que interrompe a gravação é a rotina comum que apresenta a
mensagem, e ela não tem fonte no lote lido. A leitura do fonte mostra a interrupção; o que
exatamente a dispara é pergunta ao site.

### RN-19 — Tela de continuação informada abandona a manutenção

Se o cabeçalho da página trouxer o código de uma **tela de continuação**, a manutenção é
abandonada antes de qualquer teste de linha e a transação é encaminhada para aquela tela. É o
mecanismo pelo qual a `C207T` pode ser usada como passo intermediário de outro programa.

[?] Nesta jornada a `C207T` é aberta pelo menu e nenhum programa do acervo lido preenche esse
código para ela; se há outro caminho que a use como passo intermediário, o site confirma.

## Cenários BDD

```gherkin
Funcionalidade: Projetos vinculados ao órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C207T

  Cenário: Consulta mostra os projetos vinculados ao órgão
    Dado que o órgão está cadastrado, não está excluído e pertence à minha secretaria
    Quando informo o órgão em modo de consulta
    Então vejo o nome do órgão, a sua coordenadoria e se ele é creche
    E vejo os projetos vinculados a ele, até 13 na página, com código e descrição
    E nada é gravado

  Cenário: A tela abre em consulta
    Dado que não escolhi a opção de manutenção
    Quando abro a tela
    Então ela abre em consulta e lista os vínculos do órgão do meu acesso

  Cenário: Órgão sem nenhum projeto vinculado
    Dado que nenhum projeto está vinculado ao órgão
    Quando abro a tela para esse órgão
    Então vejo a mensagem "* Orgao sem projetos cadastrados *"

  Cenário: Inclusão de um vínculo
    Dado que consultei o órgão e que o projeto existe na minha secretaria sem vínculo com ele
    Quando informo a ação I na linha do projeto, em modo de alteração
    Então o vínculo entre o órgão e o projeto é gravado
    E a operação fica registrada na auditoria

  Cenário: Inclusão recusada porque o vínculo já existe
    Dado que o projeto já está vinculado ao órgão
    Quando tento incluir o vínculo
    Então vejo a mensagem "* Orgao ja cadastrado neste projeto *"
    E nada é gravado

  Cenário: Inclusão recusada porque o projeto não está cadastrado
    Dado que o código do projeto não está cadastrado na minha secretaria
    Quando tento incluir o vínculo
    Então vejo a mensagem "* Projeto nao cadastrado *"
    E nada é gravado

  Cenário: Exclusão de um vínculo
    Dado que consultei o órgão e que o projeto está vinculado a ele
    Quando informo a ação E na linha do projeto, em modo de alteração
    Então o vínculo é apagado
    E a operação fica registrada na auditoria

  Cenário: Exclusão recusada porque o vínculo não existe
    Dado que o projeto não está vinculado ao órgão
    Quando tento excluir o vínculo
    Então vejo a mensagem "* Orgao nao cadastrado neste projeto *"
    E nada é gravado

  Cenário: Linha sem projeto ou com ação desconhecida é ignorada
    Dado que preenchi uma linha sem o código do projeto, ou com ação diferente de I e de E
    Quando a tela processa as linhas
    Então aquela linha não gera operação nenhuma

  Cenário: Órgão não cadastrado
    Dado que o órgão informado não existe no cadastro, ou está marcado como excluído
    Quando tento consultá-lo
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E nada é gravado

  Cenário: Órgão com cadastro incompleto
    Dado que falta no órgão o bairro, o órgão a que está subordinado, o nome, o endereço, as matrículas ou as pessoas
    Quando tento consultá-lo
    Então vejo a mensagem "* Orgao cadastrado com dados incompletos *"
    E nada é gravado

  Cenário: Órgão de outra secretaria
    Dado que o órgão pertence a outra secretaria
    Quando tento consultá-lo
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E nada é gravado

  Cenário: Órgão de outra coordenadoria
    Dado que o órgão pertence a uma coordenadoria diferente da minha
    Quando tento consultá-lo
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste orgao *"
    E nada é gravado

  Cenário: Órgão não informado
    Dado que o meu acesso não está limitado a um órgão
    Quando envio a tela em modo de consulta sem informar o órgão
    Então vejo a mensagem "* Informe o orgao *"
    E nada é gravado

  Cenário: Acesso restrito a um órgão só alcança o próprio órgão
    Dado que o meu acesso está limitado a um órgão
    Quando informo outro órgão em modo de consulta
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E nada é gravado

  Cenário: Atualizar sem consultar antes
    Dado que o órgão informado não é o que já está carregado na sessão
    Quando envio a página em modo de alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor fica no campo do órgão
    E nada é gravado

  Cenário: Opção de manutenção indisponível
    Dado que informei uma opção de manutenção diferente de ALT e de CON
    Quando a tela confere a opção
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo da opção

  Cenário: A recusa de uma linha impede a gravação da página
    Dado que uma das linhas da página traz um projeto não cadastrado
    Quando envio a página com outra linha válida em modo de alteração
    Então vejo a mensagem da linha recusada
    E nenhum vínculo da página é gravado

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu perfil não libera incluir ou excluir nesta tela
    Quando tento incluir ou excluir um vínculo
    Então o sistema recusa a operação com mensagem
    E nada é gravado

  Cenário: Consulta não grava nem com ação marcada
    Dado que estou na tela em modo de consulta
    Quando envio uma linha marcada com a ação I ou com a ação E
    Então vejo a lista de vínculos do órgão
    E nada é incluído nem excluído

  Cenário: Tela de continuação informada abandona a manutenção
    Dado que o cabeçalho da página traz o código de uma tela de continuação
    Quando envio a página
    Então a manutenção é abandonada
    E nada é gravado
```
