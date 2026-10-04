# US — C068T — Registrar o aditivo de quantidade de um item da permissão

## Estória

Como **servidor de CRE que responde pela execução da permissão**, quero **calcular e
registrar o aditivo de quantidade de um item da permissão**, para que **a permissão passe
a autorizar a quantidade acrescida, dentro do teto de 25% do quantitativo inicial, sem que
o contrato fique autorizando mais do que pode**.

A permissão é o registro que autoriza um fornecedor, dentro de um contrato de uma
coordenação regional escolar, de um grupo de licitação e de um período, a entregar um item
— uma classe, uma subclasse e um gênero — por uma quantidade e um valor. Quando a demanda
cresce, essa quantidade precisa ser acrescida por aditivo: a tela apura quanto ainda cabe
(o teto de 25% sobre a quantidade inicial, descontado o que já foi aditivado), calcula o
valor do acréscimo e, confirmada a operação, registra o acréscimo na permissão, deixando o
rastro de quem o fez e de como o registro estava antes. Sem ela, o acréscimo de quantidade
seria combinado por fora do sistema, e o contrato poderia passar do limite sem que ninguém
percebesse.

## Contexto

Jornada S000M → C000M → C050M → C068M → C068T.
Ator: servidor de CRE — calcula e registra o aditivo de quantidade de um item da permissão
da sua coordenação regional escolar, dentro da secretaria em que entrou.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O que esta tela usa do que veio antes é o **tipo de órgão da secretaria** escolhida no
LOGON — ele entra na identificação de tudo o que a tela lê e a tela não deixa digitá-lo —,
além da **matrícula**, do **acesso**, da **coordenação regional** e da **data do sistema**
da sessão. Essas são regras da entrada e estão no anexo de evidências, em **Regras que se
revelaram da entrada**.

A tela anterior da jornada é um menu, e a tela desta jornada não recebe dela nem o registro
nem a operação: quem abre a C068T é uma opção de menu, sem encadeamento de tela para tela.
A jornada termina aqui: a única tela a que a C068T leva é ela mesma, reapresentada com o
resultado do cálculo.

---

## Regras de negócio

### RN-01 — A tela calcula e, confirmada, registra o aditivo de quantidade de um item da permissão

A tela trata do acréscimo de **quantidade** de um item da permissão — o aditivo de
quantidade. Em um primeiro momento ela **calcula**: localiza a permissão, apura o valor do
acréscimo e apresenta o teto que ainda cabe. Confirmada a operação (RN-10), ela **grava**.

A gravação acrescenta à permissão a quantidade e o valor do aditivo. **Nada é apagado**: a
operação de exclusão está declarada para os cadastros que a tela enxerga e não é executada
por caminho nenhum. A tela enxerga **9 cadastros**: **7** deles ela lê — o de telas, o do
tipo de órgão, o da permissão, o de fornecedores, o de gêneros, o do tipo de licitação e o
da liberação da tela por tipo de licitação — e **3** ela grava: o da permissão, que também
lê, o da trilha de auditoria e o do acompanhamento do aditivo.

O cadastro das permissões tem **52 campos** e comporta até **1.000.000** de registros; o da
trilha de auditoria comporta **60.000.000**; o do acompanhamento do aditivo, **200.000**.
Esses números são **capacidade** — o máximo esperado, parâmetro de dimensionamento —, **não**
volume cadastrado.

### RN-02 — A permissão do item é identificada pela coordenação regional, pelo contrato, pelo período, pelo grupo de licitação e pelo item

A tela localiza a permissão pela **coordenação regional escolar**, pelo **tipo de
contrato**, pela **data limite do período** — dia, mês e ano —, pelo **grupo de licitação**
e pelo **item** — classe, subclasse e gênero —, sempre dentro do **tipo de órgão da
secretaria da sessão**, que não se digita. A data de início do período e as datas-base não
identificam a permissão: elas vêm do cadastro e são apenas mostradas.

O **fornecedor** é tratado de forma diferente nos dois modos. Na **alteração**, o servidor
informa o código do fornecedor e a tela mostra a razão social lida do cadastro de
fornecedores. Na **consulta**, a tela preenche o código com o da própria permissão e busca
a razão social. Em nenhum dos dois a gravação troca o fornecedor da permissão: o que se
grava é o acréscimo de quantidade e de valor (RN-11).

### RN-03 — O item tem de estar informado

Sem a classe, a subclasse e o gênero informados, a tela não procura a permissão e não
calcula nada: recusa com **\* Informe o genero para o calculo do aditivo \***, com o cursor
de volta no campo da classe. A recusa vale tanto na alteração quanto na consulta.

### RN-04 — A permissão informada tem de estar cadastrada

Procurada a permissão pela combinação informada e não existindo, a recusa é
**\* Permissao nao cadastrada \***, com o cursor de volta no campo da coordenação regional
escolar, e nada é mostrado nem calculado. A tela também não enxerga permissão marcada como
excluída no cadastro.

### RN-05 — O modo da tela é alteração ou consulta, e a consulta não grava

A tela tem um modo de operação que só admite dois valores: **alteração** e **consulta** —
os que a recusa nomeia como **ALT** e **CON**. Qualquer outro valor é recusado com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor no campo do modo, e a
transação não segue. Quando a tela abre sem modo informado, ela assume sozinha o modo
consulta.

No modo consulta **nada é gravado**: a consulta termina por si mesma, antes da passagem que
gravaria. No modo alteração, a tela confere tudo o que as regras seguintes exigem e
recalcula o aditivo.

### RN-06 — O aditivo exige a quantidade ou o percentual, e o percentual não passa de 25%

Informado o item e encontrada a permissão, a alteração exige que o acréscimo venha de algum
lugar: sem a quantidade e sem o percentual, a recusa é
**\* Informe a quantidade ou % do aditivo \***, com o cursor no campo da quantidade.
Informado apenas o percentual, ele não pode passar de **25**: acima disso a recusa é
**\* Maximo = 25 % \***, com o cursor no campo do percentual. O percentual informado é
convertido em quantidade sobre a quantidade inicial do item.

### RN-07 — O aditivo não pode passar de 25% da quantidade inicial, somado o que já foi aditivado

O teto do aditivo de quantidade é **25% da quantidade inicial do item**. A tela soma a
quantidade que já foi aditivada nessa permissão à quantidade agora informada e recusa se o
resultado passar do teto, com **\* Qt Aditivo ultrapassa 25% da Qt Inicial \*** e o cursor
no campo da quantidade. O que já foi aditivado entra na conta: um item que já consumiu parte
dos 25% só admite o que falta.

O teto de **valor** correspondente é calculado e mostrado, mas não é conferido: nenhuma
recusa desta tela compara o valor do aditivo com ele.

### RN-08 — O valor do aditivo é a quantidade aditivada pelo preço do item, já ajustado pelo percentual registrado na permissão

O valor do aditivo é calculado pela tela: a quantidade aditivada vezes o preço unitário do
item. O preço usado não é o preço cru: é o preço do item ajustado pelo número com sinal e
duas casas decimais registrado na permissão — o preço multiplicado por um mais esse número
dividido por cem. O sinal desse número aparece ao lado dele na tela: negativo, positivo ou
nenhum, quando é zero.

A tela mostra também o preço unitário já ajustado, o valor do aditivo, o percentual que o
aditivo representa do valor inicial do item, a quantidade máxima do aditivo (o teto de 25%)
e o valor máximo correspondente. O percentual máximo mostrado é sempre **25**.

[?] O que é, em negócio, o número com sinal e duas casas decimais guardado na permissão e
mostrado ao lado do preço não está nomeado em nenhuma mensagem do acervo: a leitura
"desconto" vem do nome que o campo tem no programa, não de uma fonte de negócio. Pergunta
ao site.

### RN-09 — A consulta mostra o item e o teto, e só ela confere a liberação da tela para o tipo de licitação

No modo consulta a tela mostra a permissão do item — o fornecedor e a razão social, o tipo
de licitação com a sua descrição, o período, as datas-base, os valores homologado,
adjudicado e do aditivo, as quantidades e os valores já aditivados — e o **teto do
aditivo**, com a quantidade do aditivo zerada.

É também na consulta que a tela confere se está **liberada para o tipo de licitação da
permissão**. Não estando, a recusa é **\* Tela nao disponivel para esta licitacao \***, com
o cursor de volta no campo da coordenação regional escolar.

[?] A liberação da tela para o tipo de licitação da permissão só é conferida na consulta: a
alteração não a confere. Se isso é intencional — a tela é liberada uma vez, quando o
servidor consulta — ou se é lacuna, a fonte não diz. Pergunta ao site.

### RN-10 — A confirmação no pé da tela separa o cálculo da gravação

No pé da tela existe um campo de **confirmação**. Enquanto ele não está marcado, a tela
apenas **calcula** o aditivo, apresenta o teto e se reapresenta com os valores calculados —
e **não grava**. Marcado, a tela confere tudo o que a alteração exige e **aplica** o
aditivo: percorre a permissão e grava (RN-11).

A tela escreve esse campo como **não confirmado** quando se apresenta; com a confirmação
marcada, ela ainda transforma a operação em alteração, seja qual for o modo informado.

[?] Quem marca a confirmação é a estação de trabalho: o campo faz parte do registro da
transação, a tela só o escreve como não confirmado, e a varredura dos 506 programas
expandidos do acervo não encontra nenhum que marque o próprio campo de confirmação. O
acervo não tem a máscara da tela, e por isso não se sabe se o campo é digitável pelo
servidor. Se ele não puder ser marcado, o aditivo nunca é gravado e a tela fica só de
cálculo. Pergunta ao site.

[?] As recusas desta tela não marcam a falha da transação em nenhuma linha: quem decide
interromper depois de uma mensagem é a rotina de comunicação do sistema, que não está no
acervo. Se ela não interromper, a passagem de gravação poderia rodar depois de uma recusa.
Pergunta ao site.

### RN-11 — Confirmado, a tela regrava a permissão item a item

Confirmada a operação, a tela percorre os itens da permissão — mesma coordenação regional,
mesmo contrato, mesmo período, mesmo grupo de licitação — e, em cada um:

- no item informado, soma a quantidade e o valor do aditivo ao que já estava aditivado e
  grava também o valor do aditivo;
- nos demais itens, regrava o valor do aditivo, somado o valor do aditivo novo.

Nenhum outro dado da permissão é tocado: fornecedor, tipo de licitação, datas e preços não
são reescritos, e **nada é apagado**.

[?] O valor do aditivo é somado ao valor do aditivo de **cada** item percorrido da
permissão, e não só ao do item informado. Se o valor do aditivo é um total da permissão
replicado nos itens — e por isso precisa mesmo ser regravado em todos — ou se a intenção era
gravar só no item aditivado, a fonte não diz. Pergunta ao site.

### RN-12 — Toda alteração confirmada deixa rastro na auditoria e no acompanhamento do aditivo

Em cada item percorrido, a gravação deixa dois registros além da própria permissão: um
registro na **trilha de auditoria** — o dado auditado, a operação de alteração, a imagem do
registro antes e a de depois, e o contexto da sessão (tipo de órgão, órgão auditado,
matrícula, terminal, data e hora) — e um registro no **cadastro de acompanhamento do
aditivo**, com a mesma operação e as mesmas imagens, mais a data e a hora da sessão, o tipo
de contrato e o tipo de licitação. O acompanhamento distingue, no próprio registro, o item
que recebeu o acréscimo dos demais itens da permissão.

[?] O número do processo que vai para a trilha de auditoria não nasce nesta tela: ela apenas
o repassa, e a fonte não diz quem o preenche. O número de ofício que o acompanhamento do
aditivo guarda também não é preenchido por esta tela — ela o deixa em branco na área de
trabalho do registro, e o gravador só o copia quando vem preenchido. De onde qualquer um dos
dois viria, a fonte não diz. Pergunta ao site.

### RN-13 — Nada é lido nem gravado sem a conferência de acesso do sistema

Antes de ler qualquer cadastro, a tela pede ao sistema de segurança que confira o acesso.
Sem perfil de acesso a esta tela, a transação para com
**\* Acesso negado para esta matricula \***; quando o cadastro da tela não corresponde, a
recusa é **\* Tela nao disponivel \***; quando a requisição chega marcada como segunda
página, **\* Acesso a pagina 2 negado \***; e quando a estação não é a da sessão, a
transação é encerrada. Na passagem em que o servidor confirma o que informou, a tela confere
também a **permissão por operação**: sem ela, a recusa é
**\* Acesso negado para esta operacao \***. A mesma passagem submete a transação ao
roteamento do sistema.

A conferência de operação examina a opção que o servidor digitou — e a transformação dessa
opção em alteração acontece **depois** dela. A conferência só distingue inclusão, alteração
e exclusão: a consulta passa sem teste de perfil, ainda que o cadastro de acesso tenha uma
marca própria para ela.

[?] Se o caminho da confirmação for alcançável pelo terminal e a opção digitada for a
consulta, a gravação acontece como alteração sem que o perfil de alteração tenha sido
conferido — a conferência rodou sobre a consulta, que ela não testa. Pergunta ao site se
isso é aceitável.

### RN-14 — Todos os campos da tela passam pela edição numérica antes das conferências

Nenhum campo desta tela é texto livre. São **36** os campos com rótulo na tela que passam
pela edição numérica antes de qualquer conferência de cadastro: os códigos de identificação
(coordenação regional, tipo de contrato, fornecedor, grupo de licitação, tipo de licitação,
classe, subclasse e gênero), as doze partes das quatro datas (início do período, limite,
base inicial e base limite), os valores e as quantidades da permissão e do aditivo, os
percentuais e o percentual com sinal registrado na permissão. O que não for número é
recusado no próprio campo, com o cursor devolvido a ele, e não chega a ser conferido.

[?] A rotina que faz essa conferência não está no acervo e o texto da mensagem que o
servidor vê quando digita letra num campo não pôde ser conferido. Só **11** dos 36 campos
estão no mapa que devolve o cursor ao campo; os outros 25 não têm posição de cursor mapeada,
e a fonte não diz se é intencional. Pergunta ao site.

### RN-15 — A leitura que falha interrompe a transação

Toda leitura desta tela testa o retorno do banco. O "registro não encontrado" é tratado como
ausência e vira a recusa correspondente; qualquer outro erro é levado à rotina de
comunicação do sistema, e a transação para ali, sem completar o resto. Uma leitura que
falhou não segue para o passo seguinte.

[?] O que essa rotina de comunicação faz com a transação não pôde ser conferido — ela não
está no acervo, e é dela que depende se a leitura que falhou realmente barra o que vem
depois. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Registrar o aditivo de quantidade de um item da permissão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a matrícula, o acesso e a coordenação regional
    E tenho acesso à tela C068T

  Cenário: RN-02 — consultar a permissão do item
    Dado que existe permissão para a coordenação regional escolar, o tipo de contrato, a data limite, o grupo de licitação e o item que informei
    Quando confirmo a consulta
    Então vejo o fornecedor e a sua razão social, o tipo de licitação com a sua descrição, o período, as datas-base, os valores e as quantidades do item
    E vejo o teto do aditivo, com a quantidade do aditivo zerada

  Cenário: RN-02 — alterar o item informando o fornecedor
    Dado que estou na tela C068T no modo alteração
    Quando informo a coordenação regional escolar, o tipo de contrato, a data limite, o grupo de licitação, o item e o código do fornecedor
    Então vejo a razão social lida do cadastro de fornecedores
    E a permissão é a daquela combinação

  Cenário: RN-03 — o item não informado
    Dado que estou na tela C068T
    Quando deixo a classe, a subclasse ou o gênero sem informar
    Então vejo "* Informe o genero para o calculo do aditivo *"
    E o cursor fica no campo da classe
    E nada é calculado

  Cenário: RN-04 — permissão não cadastrada
    Dado que estou na tela C068T
    Quando a combinação informada não tem permissão cadastrada
    Então vejo "* Permissao nao cadastrada *"
    E o cursor fica no campo da coordenação regional escolar
    E nada é mostrado

  Cenário: RN-05 — modo diferente de ALT e de CON
    Dado que estou na tela C068T
    Quando informo um modo diferente de alteração e de consulta
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: RN-05 — a tela abre sem modo informado
    Dado que abro a tela C068T sem informar o modo
    Então a tela está no modo consulta
    E nada é gravado

  Cenário: RN-05 — a consulta não grava nada
    Dado que estou na tela C068T no modo consulta e a permissão está cadastrada
    Quando informo o item e confirmo a consulta
    Então a tela apenas apresenta os dados do item e o teto do aditivo
    E a permissão continua com a quantidade e o valor anteriores

  Cenário: RN-06 — nem quantidade nem percentual
    Dado que estou na tela C068T no modo alteração e a permissão existe
    Quando não informo a quantidade nem o percentual do aditivo
    Então vejo "* Informe a quantidade ou % do aditivo *"
    E o cursor fica no campo da quantidade
    E nada é gravado

  Cenário: RN-06 — percentual acima de 25
    Dado que estou na tela C068T no modo alteração e a permissão existe
    Quando informo só o percentual, acima de 25
    Então vejo "* Maximo = 25 % *"
    E o cursor fica no campo do percentual
    E nada é gravado

  Cenário: RN-07 — o aditivo passa de 25% da quantidade inicial
    Dado que a permissão já tem quantidade aditivada
    Quando a quantidade informada, somada à já aditivada, passa de 25% da quantidade inicial
    Então vejo "* Qt Aditivo ultrapassa 25% da Qt Inicial *"
    E o cursor fica no campo da quantidade
    E nada é gravado

  Cenário: RN-08 — o valor do aditivo é calculado
    Dado que a permissão tem preço unitário e o percentual com sinal registrado
    Quando informo a quantidade do aditivo
    Então vejo o preço já ajustado por esse percentual, o valor do aditivo e o percentual que ele representa do valor inicial
    E vejo a quantidade máxima do aditivo, o valor máximo e o percentual máximo de 25

  Cenário: RN-09 — a tela não está liberada para o tipo de licitação da permissão
    Dado que a permissão existe, mas esta tela não está liberada para o tipo de licitação dela
    Quando confirmo a consulta
    Então vejo "* Tela nao disponivel para esta licitacao *"
    E o cursor fica no campo da coordenação regional escolar
    E nada é mostrado

  Cenário: RN-10 — sem a confirmação a tela calcula e não grava
    Dado que estou na tela C068T no modo alteração e a permissão existe
    Quando informo a quantidade do aditivo sem marcar a confirmação
    Então a tela reapresenta os valores calculados e o teto
    E a permissão continua com a quantidade e o valor anteriores

  Cenário: RN-10, RN-11 e RN-12 — com a confirmação o aditivo é gravado
    Dado que a tela já calculou o aditivo do item
    Quando marco a confirmação e confirmo a alteração
    Então a quantidade e o valor do aditivo são somados no item informado
    E o valor do aditivo é regravado em cada item da permissão
    E a alteração fica registrada na trilha de auditoria e no acompanhamento do aditivo
    E nenhum registro é apagado

  Cenário: RN-11 — o aditivo não troca o resto da permissão
    Dado que confirmei o aditivo de um item
    Quando a gravação termina
    Então o fornecedor, o tipo de licitação, as datas e os preços da permissão continuam os mesmos
    E só a quantidade e o valor adicionais e o valor do aditivo mudaram

  Cenário: RN-12 — o item aditivado fica distinguido dos demais
    Dado que confirmei o aditivo de um item
    Quando a gravação termina
    Então o acompanhamento do aditivo registra cada item percorrido da permissão
    E o registro do item que recebeu o acréscimo se distingue do registro dos demais

  Cenário: RN-13 — sem perfil de acesso à tela
    Dado que a minha matrícula não tem perfil de acesso a esta tela
    Quando confirmo a consulta
    Então vejo "* Acesso negado para esta matricula *"
    E nada é lido

  Cenário: RN-13 — o cadastro da tela não corresponde
    Dado que o cadastro da tela não corresponde a esta transação
    Quando confirmo a consulta
    Então vejo "* Tela nao disponivel *"

  Cenário: RN-13 — sem permissão para a operação
    Dado que informo a alteração
    E o meu perfil de acesso não permite alterar
    Quando confirmo
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-14 — campo não numérico
    Quando preencho um dos campos da tela com letra
    Então a tela recusa o campo antes de qualquer conferência de cadastro
    E o cursor volta ao campo, quando ele tem posição mapeada
    E nada é lido

  Cenário: RN-15 — falha no banco durante a leitura
    Dado que a leitura de um dos cadastros falha
    Quando confirmo
    Então a transação é interrompida com o tratamento de erro do sistema
    E a operação não é completada
```
