# US — C126T — Manter os grupos da secretaria e a sua unidade orçamentária

## Estória

Como **servidor da CRE**, quero **manter a lista dos grupos da secretaria — a lista das
coordenações regionais escolares, com a descrição e a unidade orçamentária de cada uma —,
incluindo os grupos que faltam, corrigindo os que existem e tirando os que não têm órgão
nenhum**, para que **cada órgão da rede fique ligado ao grupo certo e todos os órgãos de um
mesmo grupo apontem para a mesma unidade orçamentária**.

O grupo é o que amarra uma coordenação regional escolar à unidade orçamentária por que correm
os seus gastos: é do grupo que sai a unidade que os órgãos daquela região usam. Enquanto
faltar o grupo, os órgãos daquela região não têm de onde tirar a sua unidade orçamentária; e
um grupo que já tem órgãos não pode sair, senão os órgãos ficam apontando para um grupo que
não existe mais. É esta tela que completa a lista, que corrige a descrição e a unidade de
cada grupo e que leva a unidade nova aos órgãos do grupo.

## Contexto

Jornada S000M → C000M → C020M → C126T.

Ator: servidor de CRE — mantém a lista dos grupos da secretaria: consulta os que existem,
inclui os que faltam, corrige a descrição e a unidade orçamentária dos que já existem e tira
os que não têm órgão nenhum.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As duas telas do meio do caminho, a `C000M` e a `C020M`, são menus: não leem cadastro de
negócio nenhum e não deixam dado de negócio para a `C126T` — só dizem qual tela abrir. O que
a `C126T` usa da sessão — a matrícula de quem opera, o código de acesso, o privilégio, a CRE
e o tipo de órgão — foi deixado pela entrada; é o **tipo de órgão** (a secretaria) que
delimita a lista que ela mostra, e a CRE de quem opera só vai junto para a auditoria.

A `C126T` é uma tela de transação, com **15 linhas por vez**, e termina nela mesma: não
encadeia para outra tela e não passa registro nem operação adiante. O mesmo cadastro é
atendido também pela tela `C125T`, que trata um grupo por vez.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O grupo tem código, descrição e unidade orçamentária

A tela mantém o cadastro dos **grupos** — as coordenações regionais escolares da secretaria.
Cada grupo tem **três dados**: o **código** (2 dígitos), que a identifica; a **descrição** (40
caracteres); e a **unidade orçamentária** (8 dígitos). É a **coordenação regional escolar** o
nome de negócio do código do grupo. O código é único **dentro do tipo de órgão**: dois tipos de
órgão podem ter, cada um, o seu grupo de mesmo código, e um não é o outro. O cadastro comporta
**1.000** grupos — capacidade declarada (máximo esperado, parâmetro de dimensionamento), não o
volume já cadastrado.

A tela mostra **15 grupos por vez**, e cada linha tem ainda a **ação**, que diz o que fazer
com ela. O único dado que o cadastro marca como obrigatório é um campo de controle interno do
registro, que a tela não mostra: a exigência da descrição e da unidade é da própria tela
(RN-11 e RN-12).

### RN-02 — Só os dois códigos passam pela conferência numérica

Antes de qualquer consulta, o sistema confere os dois códigos: o **código do grupo** e a
**unidade orçamentária**. Em branco vale zero, os separadores de milhar caem e o que não for
número é recusado, com o cursor de volta no campo. A **descrição** e a **ação** da linha
**não** passam por conferência nenhuma: chegam ao cadastro como o servidor as digitou.

[?] O texto exato da recusa por código não numérico não está no lote: a conferência é feita
por rotina padrão de edição numérica, e a mensagem que o terminal mostra sai da rotina de
comunicação, fora dos fontes fornecidos. Pergunta ao site.

### RN-03 — A página tem 15 linhas, com código, descrição, unidade e ação

A página mostra **15 linhas**, e cada linha tem **quatro dados**: o código do grupo, a
descrição, a unidade orçamentária e a ação. Ao abrir, o sistema lê o cadastro e vai
preenchendo as linhas, uma a uma, em ordem de código, com o código, a descrição e a unidade
que leu. Numa linha em branco o servidor digita o código, a descrição e a unidade de um grupo
novo; numa linha já preenchida, digita a descrição e a unidade novas, quando for alterar.

### RN-04 — Ao abrir, a lista é a dos grupos do tipo de órgão de quem opera

Na abertura, a tela percorre o cadastro dos grupos e preenche as 15 linhas mostrando só os
grupos do **tipo de órgão** da sessão — os grupos de outra secretaria não aparecem. A **CRE
de quem opera não delimita a lista**: aparecem os grupos de todas as coordenações daquela
secretaria. Quando não há nenhum grupo, o sistema avisa **\* Nao existem grupos cadastrados
\***, com o cursor na coluna do código, na primeira linha, e nada é gravado.

[?] A leitura que preenche a página é posicionada pelos sinalizadores do conjunto, que são do
dialeto e não estão explicados no corpus nem no manual: se a primeira linha da página seguinte
repete o último grupo lido, e se a leitura continua de uma mensagem para a outra, não foi
possível determinar. Pergunta ao site.

### RN-05 — A tela abre na consulta, e a opção da página só admite alteração ou consulta

Chegando à tela sem opção informada, ela assume a **consulta**, e é esse valor que aparece no
campo da opção. A opção informada só pode ser **alteração** ou **consulta**; qualquer outra é
recusada com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no campo da opção, e
a página não é processada: nada é validado e nada é gravado.

[?] A mensagem nomeia as opções pelas abreviaturas **ALT** e **CON**, e a conferência da tela
compara o que foi informado com as siglas internas de alteração e de consulta — que não são
essas duas palavras. Nenhum fonte do lote mostra quem traduz o que o operador digita na sigla
conferida. Se não houver tradução, a conferência recusa toda opção, inclusive as duas que a
própria mensagem pede, e nenhum grupo é mantido por esta tela. Pergunta ao site.

[?] A recusa da opção não é reconferida no caminho que grava: esse caminho descarta apenas a
consulta, e o que separa uma recusa da gravação é a marca que a rotina de mensagem do ambiente
deixa — rotina que não está no lote. Se ela não marcar, uma linha com a opção recusada ainda
assim é gravada. Pergunta ao site.

### RN-06 — A tela reabre na opção e no grupo da última passagem

A opção usada e o último grupo lido ficam guardados na área de trabalho da sessão, que só é
inicializada na primeira vez. Reabrindo a tela, ela volta na mesma opção — alteração, se foi a
última — e apontada para o grupo que a última leitura deixou, e não do começo do cadastro.
Chegando ao fim do cadastro, o ponteiro volta ao começo.

### RN-07 — A ação de cada linha decide a operação, e a linha sem código ou com ação desconhecida é ignorada

Só três ações operam uma linha: **I** inclui, **A** altera e **E** exclui. A linha cujo código
é zero, ou cuja ação está em branco ou fora dessas três, passa em silêncio: não gera recusa,
não é validada e não grava nada. A operação decidida pela ação é a que vai para a conferência
de permissão de quem opera (RN-08).

### RN-08 — Cada linha é autorizada pela operação que ela pede

A ação da linha é traduzida para a operação correspondente — inclusão, alteração ou exclusão
—, e é essa operação que a autorização do servidor confere no cadastro de telas por código de
acesso, que guarda, por operação, se ela está liberada. Sem a marca da operação, a linha não é
validada nem gravada, e a tela volta.

[?] A autorização é conferida duas vezes: uma com a opção da página e outra com a operação da
ação da linha. Como a opção só pode ser alteração ou consulta, incluir exige a permissão de
alteração **e** a de inclusão — e excluir, a de alteração e a de exclusão. Se quem tem só a
permissão de inclusão deveria poder incluir por esta tela, a conferência da opção o impede.
Pergunta ao site.

[?] A permissão de consulta não é conferida: com a opção de consulta, a conferência de
operação não encontra o que checar e passa direto. Quem tem a tela autorizada consulta sem a
permissão de consulta. Pergunta ao site.

### RN-09 — Nenhuma operação sem a tela, a rota e a sessão conferidas

Na abertura, a tela confere se ela própria consta da relação de telas do sistema — não
constando, o aviso é **\* Tela nao disponivel \*** — e se o código de acesso de quem opera tem
a tela — não tendo, a recusa é **\* Acesso negado para esta matricula \***. A conferência da
sessão ainda exige que a estação seja a mesma do cadastro do funcionário; não sendo, a sessão
é encerrada.

A cada resposta a tela confere de novo a relação de telas — tendo a tela sido retirada de lá,
o aviso é **\* Tela nao cadastrada \*** — e a rota do módulo, que exige a marca de manutenção
da tela: sem ela, o aviso é **\* Operacao nao disponivel \***. Em qualquer dessas recusas nada
é validado e nada é gravado.

### RN-10 — Inclusão recusa grupo já cadastrado

Para incluir, a tela procura o código informado entre os grupos do tipo de órgão da sessão.
Já existindo um grupo com aquele código, a inclusão é recusada com **\* Grupo ja cadastrado
\***, com o cursor no campo da ação da linha, e nada é gravado.

### RN-11 — Inclusão e alteração exigem a descrição

Na inclusão de um código que ainda não existe e na alteração de um grupo já cadastrado, a
**descrição** é obrigatória: sem ela, a recusa é **\* Informe a descricao \***, com o cursor
no campo da descrição, e nada é gravado. A exclusão não exige a descrição.

### RN-12 — Inclusão e alteração exigem a unidade orçamentária

Além da descrição, a inclusão e a alteração exigem a **unidade orçamentária**: sem ela, a
recusa é **\* Informe a unidade orcamentaria \***, com o cursor no campo da unidade
orçamentária, e nada é gravado. A exclusão não exige a unidade orçamentária.

[?] A tela aceita qualquer unidade orçamentária, contanto que diferente de zero, e não confere
se ela existe no cadastro das unidades orçamentárias: esta tela só lê a relação de telas, o
cadastro dos grupos, o cadastro dos órgãos e a auditoria. Se o vínculo pode ficar apontando
para uma unidade inexistente, pergunta ao site.

### RN-13 — Alteração e exclusão exigem grupo cadastrado

Para alterar ou excluir, o código informado tem de estar cadastrado entre os grupos do tipo de
órgão da sessão; não estando, a recusa é **\* Grupo nao cadastrado \***, com o cursor no campo
da ação da linha, e nada é gravado.

### RN-14 — Inclusão cria o grupo no cadastro

Passadas as conferências, a ação **I** cria o grupo no cadastro, com o código, a descrição e a
unidade orçamentária informados e o tipo de órgão da sessão, e em seguida deixa o rastro na
auditoria (RN-18).

### RN-15 — Alteração troca a descrição e a unidade, e leva a unidade nova aos órgãos do grupo

A ação **A** lê o grupo, guarda o conteúdo anterior e o novo, trava o registro, substitui a
**descrição** e a **unidade orçamentária** e regrava. O código não muda: ele é a chave do
grupo. Em seguida a tela percorre os **órgãos** do grupo — os órgãos do mesmo tipo de órgão e
com o mesmo código de grupo — e regrava em cada um a unidade orçamentária do grupo, de modo
que o grupo e os seus órgãos não fiquem com unidades diferentes.

[?] A leitura que percorre os órgãos é posicionada com a terceira parte da chave zerada (o
código do órgão filho), e o que os sinalizadores dessa leitura fazem não está no corpus nem no
manual. Se a leitura exigir a chave inteira, nenhum órgão é alcançado com aquele campo zerado
e a unidade não chega aos órgãos do grupo; se ela repetir o registro, o laço de regravação não
termina. Pergunta ao site.

### RN-16 — A exclusão é recusada quando há órgãos no grupo

Antes de excluir, a tela percorre os órgãos do grupo e, achando pelo menos um, recusa com
**\* Nao exclua. Orgaos neste grupo \***, com o cursor no campo da ação da linha, e o grupo
continua cadastrado. Passando na conferência, a tela trava o registro, deixa o rastro na
auditoria (RN-18) e apaga o grupo do cadastro.

[?] É a mesma leitura com a terceira parte da chave zerada que sustenta esta recusa: se ela
não alcançar os órgãos do grupo, a recusa fica **inalcançável** e a tela apaga um grupo que
tem órgãos ligados a ele. Pergunta ao site.

[?] O mesmo cadastro tem duas semânticas de exclusão: a tela `C125T`, que trata um grupo por
vez, registra a exclusão **marcando** o grupo e mantendo o registro, e a `C126T` apaga o
registro. Qual das duas vale — e se as duas devem conviver — pergunta ao site.

### RN-17 — A consulta não grava nada

Na consulta a tela só mostra: ela lista os grupos e, na resposta, desvia antes das peneiras da
linha e antes de qualquer operação de escrita. Nenhum grupo é incluído, alterado ou apagado,
nenhum órgão do grupo é tocado e nenhuma trilha de auditoria é gerada.

### RN-18 — Toda gravação deixa rastro na auditoria

Cada inclusão, alteração e exclusão confirmadas gravam, no cadastro de auditoria, um registro
com a operação (inclusão, alteração ou exclusão), o cadastro auditado, a tela **C126T**, a
matrícula de quem operou, a estação, a CRE e o tipo de órgão da sessão, o número do processo,
a data e a hora do sistema, e o conteúdo anterior e o posterior do grupo. Na inclusão o valor
anterior vai vazio; na exclusão, o posterior.

Além do cadastro dos grupos e da auditoria, a tela só grava no cadastro dos órgãos, e só na
alteração: é por ali que a unidade orçamentária nova chega a cada órgão do grupo (RN-15).

### RN-19 — A recusa de destino inválido não é alcançável por esta tela

A recusa de **destino inválido** — a distribuição automática entre destinos —, que a ficha
estrutural da tela lista entre as suas mensagens, não é alcançável por ela: o modo de
distribuição automática é limpo imediatamente antes dos pontos em que a recusa poderia
disparar, tanto na gravação do grupo quanto na da auditoria.

[?] A ficha do grafo lista essa recusa para esta tela, e o programa limpa o campo antes de
usá-lo: divergência entre a ficha e o comportamento, a confirmar com quem mantém o grafo.

### RN-20 — Chegando com a tela de retorno preenchida, a manutenção é abandonada

Se a transação chegar com a indicação de **tela de retorno** preenchida — o dado que a rota usa
para devolver o servidor a outra tela —, a manutenção é abandonada: nada é validado, nada é
gravado e o servidor é levado à tela indicada.

[?] Nada nesta jornada preenche essa indicação — o caminho até a tela é a opção de um menu,
que só nomeia a tela —, e o lote não diz quem a preenche nem para onde ela levaria. Pergunta
ao site.

### RN-21 — A resposta não repõe a data do sistema nem a descrição do tipo de órgão

A abertura mostra, no cabeçalho, a **data do sistema** e a **descrição do tipo de órgão** da
sessão. A cada resposta esses dois dados são apagados e não são repostos: a resposta sai com
os dois campos em branco.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe um
caminho de entrada em que os campos não são limpos, não foi possível determinar. Pergunta ao
site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os grupos da secretaria e a sua unidade orçamentária

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C126T

  Cenário: A tela mostra o código, a descrição e a unidade orçamentária de cada grupo
    Dado que estou na tela C126T e existem grupos cadastrados no meu tipo de órgão
    Quando a lista é apresentada
    Então vejo, em cada linha, o código do grupo, a descrição e a unidade orçamentária
    E o código do grupo é único dentro do meu tipo de órgão
    E o cadastro comporta até 1.000 grupos

  Cenário: Código do grupo ou unidade orçamentária não numéricos
    Dado que estou na tela C126T
    Quando informo no código do grupo, ou na unidade orçamentária, algo que não é número
    Então o sistema recusa o campo antes de consultar o cadastro
    E o cursor volta ao campo
    E a descrição e a ação que digitei não são conferidas

  Cenário: A página tem 15 linhas
    Dado que estou na tela C126T
    Quando a página é apresentada
    Então vejo 15 linhas, cada uma com código, descrição, unidade orçamentária e ação
    E as linhas já cadastradas vêm preenchidas pelo sistema, em ordem de código

  Cenário: A lista é a dos grupos do meu tipo de órgão
    Dado que estou na tela C126T
    E o cadastro tem grupos do meu tipo de órgão e grupos de outro tipo de órgão
    Quando a lista é apresentada
    Então vejo os grupos do meu tipo de órgão, até 15 por vez
    E não vejo os grupos de outro tipo de órgão
    E nada é gravado

  Cenário: Não há nenhum grupo cadastrado no meu tipo de órgão
    Dado que não existe nenhum grupo cadastrado no meu tipo de órgão
    Quando abro a tela C126T
    Então vejo a mensagem "* Nao existem grupos cadastrados *"
    E o cursor fica na coluna do código, na primeira linha

  Cenário: A tela abre na opção de consulta
    Dado que ainda não usei a tela nesta sessão
    Quando abro a tela C126T
    Então a tela abre na opção de consulta
    E nada é gravado

  Cenário: Opção da página diferente de alteração e de consulta
    Dado que estou na tela C126T
    Quando informo uma opção que não é a de alteração nem a de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: A tela reabre na opção e no grupo da última passagem
    Dado que passei pela tela C126T em alteração, sobre um grupo
    Quando volto a abrir a tela
    Então ela reabre em alteração
    E apontada para o grupo que a última leitura deixou

  Cenário: Linha com ação desconhecida é ignorada
    Dado que estou na tela C126T na opção de alteração
    E preenchi uma linha com uma ação diferente de I, A e E
    Quando confirmo a mensagem
    Então aquela linha não é validada
    E nada é gravado para ela

  Cenário: Linha com o código em branco é ignorada
    Dado que estou na tela C126T na opção de alteração
    E deixei o código de uma linha em branco, mesmo com a ação preenchida
    Quando confirmo a mensagem
    Então aquela linha não gera operação nenhuma
    E nada é gravado para ela

  Cenário: Sem autorização para a operação que a linha pede
    Dado que o meu código de acesso tem a tela C126T sem aquela operação liberada
    E informo a opção de alteração com uma linha preenchida
    Quando confirmo a mensagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E aquela linha não é validada
    E nada é gravado

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela C126T
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Tela fora da relação de telas do sistema
    Dado que a tela C126T não consta da relação de telas do sistema
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Tela retirada da relação de telas do sistema
    Dado que a tela C126T foi retirada da relação de telas do sistema
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é gravado

  Cenário: Estação diferente da do meu cadastro
    Dado que estou operando de uma estação diferente da que está no meu cadastro
    Quando a tela confere a sessão
    Então a minha sessão é encerrada
    E não consigo operar

  Cenário: Inclusão de grupo que já está cadastrado
    Dado que estou na tela C126T na opção de alteração
    E o grupo informado já está cadastrado no meu tipo de órgão
    E assinalo nessa linha a ação I
    Quando confirmo a mensagem
    Então vejo a mensagem "* Grupo ja cadastrado *"
    E o cursor volta ao campo da ação
    E nada é gravado

  Cenário: Inclusão ou alteração sem a descrição
    Dado que estou na tela C126T na opção de alteração
    E deixo a descrição em branco numa linha com a ação I ou A
    Quando confirmo a mensagem
    Então vejo a mensagem "* Informe a descricao *"
    E o cursor volta ao campo da descrição
    E nada é gravado

  Cenário: Inclusão ou alteração sem a unidade orçamentária
    Dado que estou na tela C126T na opção de alteração
    E deixo a unidade orçamentária em branco numa linha com a ação I ou A
    Quando confirmo a mensagem
    Então vejo a mensagem "* Informe a unidade orcamentaria *"
    E o cursor volta ao campo da unidade orçamentária
    E nada é gravado

  Cenário: Alteração ou exclusão de grupo não cadastrado
    Dado que estou na tela C126T na opção de alteração
    E o código informado não está cadastrado no meu tipo de órgão
    E assinalo nessa linha a ação A ou a ação E
    Quando confirmo a mensagem
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo da ação
    E nada é gravado

  Cenário: Inclusão cria o grupo no cadastro
    Dado que estou na tela C126T na opção de alteração
    E informo, numa linha, um código que ainda não está cadastrado no meu tipo de órgão, com a descrição e a unidade orçamentária
    E assinalo nessa linha a ação I
    Quando confirmo a mensagem
    Então o grupo passa a constar do cadastro
    E a auditoria registra a inclusão, sem valor anterior

  Cenário: Alteração troca a descrição e a unidade e as leva aos órgãos do grupo
    Dado que estou na tela C126T na opção de alteração
    E o grupo informado está cadastrado e tem órgãos ligados a ele
    E informo a nova descrição e a nova unidade orçamentária
    E assinalo nessa linha a ação A
    Quando confirmo a mensagem
    Então o cadastro dos grupos passa a mostrar a nova descrição e a nova unidade
    E a unidade orçamentária de cada órgão do grupo passa a ser a nova
    E a auditoria registra a alteração, com o conteúdo anterior e o posterior do grupo

  Cenário: Exclusão recusada porque há órgãos no grupo
    Dado que estou na tela C126T na opção de alteração
    E o grupo informado está cadastrado e tem pelo menos um órgão ligado a ele
    E assinalo nessa linha a ação E
    Quando confirmo a mensagem
    Então vejo a mensagem "* Nao exclua. Orgaos neste grupo *"
    E o cursor volta ao campo da ação
    E o grupo continua cadastrado

  Cenário: Exclusão de um grupo que não tem órgãos
    Dado que estou na tela C126T na opção de alteração
    E o grupo informado está cadastrado e nenhum órgão está ligado a ele
    E assinalo nessa linha a ação E
    Quando confirmo a mensagem
    Então o grupo sai do cadastro
    E a auditoria registra a exclusão, com o conteúdo anterior do grupo

  Cenário: A consulta não grava nada
    Dado que estou na tela C126T na opção de consulta
    Quando percorro e confirmo as linhas da página
    Então o cadastro dos grupos é apenas lido
    E nenhum grupo é incluído, alterado ou apagado
    E nenhum órgão do grupo é tocado
    E nenhuma trilha de auditoria é gerada

  Cenário: Toda gravação deixa rastro na auditoria
    Dado que confirmei uma inclusão, uma alteração ou uma exclusão na C126T
    Quando a gravação termina
    Então existe um registro de auditoria do cadastro dos grupos
    E com a operação, o conteúdo anterior e o posterior do grupo
    E com a tela, a matrícula, a estação, a CRE e o tipo de órgão da sessão
    E com o número do processo, a data e a hora do sistema

  Cenário: A tela não apresenta a recusa de destino inválido
    Dado que estou na tela C126T na opção de alteração e confirmei uma operação
    Quando a gravação é preparada
    Então o sistema limpa o modo de distribuição automática
    E a recusa de destino inválido não é apresentada

  Cenário: A tela de retorno preenchida abandona a manutenção
    Dado que a transação chega à C126T com a indicação de tela de retorno preenchida
    Quando a manutenção começaria
    Então o processamento é abandonado e nada é gravado
    E o servidor é levado à tela indicada

  Cenário: A resposta volta com a data do sistema e a descrição do tipo de órgão em branco
    Dado que a tela abriu mostrando a data do sistema e a descrição do tipo de órgão
    Quando respondo a mensagem
    Então a resposta vem com esses dois campos em branco
```
