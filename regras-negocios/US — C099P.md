# US — C099P — Informar os parâmetros do relatório e pedir a sua emissão

## Estória

Como **servidor de CRE**, quero **informar os parâmetros do relatório que escolhi e pedir
a sua emissão**, para que **o relatório saia pela impressora da minha sessão, delimitado
pelos dados que eu informei, sem eu ter de levantar o que quero fora do sistema**.

Esta tela é a porta por onde saem os pedidos de dezenas de relatórios do sistema: cada
relatório tem o seu conjunto de parâmetros, e é aqui que eles são informados, conferidos
e registrados antes de a emissão correr. Sem essa etapa, o relatório sairia com os
parâmetros de outro pedido, ou não sairia — e quem opera não teria como delimitar o
período, a faixa de classes ou a faixa de fornecedores do que quer ver impresso.

## Contexto

Jornada S000M → C000M → C010M → C099P.

Ator: servidor de CRE — informa os parâmetros do relatório escolhido no menu e pede a
sua emissão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O `C000M` é o menu geral e não grava nada;
o `C010M` é a tela de impressão que antecede esta jornada: ele exige a impressora,
deixa-a na sessão junto com o código de saída do pedido e manda a sessão para a `C099P`
levando o relatório já escolhido. O que a `C099P` usa da sessão — matrícula, tipo de
órgão, terminal, impressora e o relatório — é o que a entrada e o `C010M` deixaram.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela atende muitos relatórios e só processa o relatório escolhido no menu

A `C099P` não é a tela de um relatório: é a tela de parâmetros por onde passam os pedidos
de dezenas de relatórios do sistema. O relatório escolhido no menu chega pela sessão, e
a tela só trabalha esse: são os campos, as conferências e o pedido daquele relatório.
Chegando o código de um relatório que esta tela não atende, ela abre e não faz nada —
não habilita campo, não confere, não registra e não avisa quem opera.

[?] O dado da jornada não fixa qual relatório foi pedido: o menu anterior (`C010M`)
oferece mais de uma porta para a `C099P`, cada porta levando um relatório diferente, e o
passo da jornada deixou a opção em branco. As regras abaixo descrevem os dois pedidos que
esse caminho pode trazer. Pergunta ao site qual deles é o desta jornada.

### RN-02 — Os campos da tela são os do relatório escolhido

Para cada relatório, a tela habilita o conjunto de campos que ele usa e deixa os demais
fora. O pedido cujos parâmetros são o período inicial e a faixa de classes usa o dia, o
mês e o ano iniciais, a classe inicial e a final, e a subclasse e o gênero inicial e
final; o pedido cujos parâmetros são a faixa de fornecedores usa apenas o código do
fornecedor inicial e o do final. Fora desses campos, a tela mostra sempre a data do
sistema e a descrição do tipo de órgão de quem opera.

[?] O texto e a posição exata dos campos na tela vêm da máscara, que não faz parte do
acervo lido; o que o programa diz é quais campos cada relatório usa. Pergunta ao site.

### RN-03 — A tela trabalha com o contexto que a sessão já traz

A matrícula de quem opera, o tipo de órgão, o terminal e a impressora vêm da sessão — a
impressora foi exigida e guardada pela tela anterior — e são esses dados que o pedido
leva; quem opera não os digita aqui. A tela usa ainda o código de saída que a tela
anterior deixou, para identificar o tipo de pedido entregue à emissão.

### RN-04 — No pedido por classe e período, o período é conferido e a classe inicial é obrigatória

O período inicial tem de ser uma data válida — dia, mês e ano formando data, com o ano
entre 1994 e 2099 —, senão a recusa é **\* Data invalida \***, com o cursor de volta ao
dia inicial. Passando a data, a classe inicial é obrigatória
(**\* Informe a Classe inicial \***) e a classe final não pode ser menor que a inicial
(**\* Classe final menor que inicial \***). A subclasse e o gênero inicial e final são
informados, mas não passam por conferência.

### RN-05 — No pedido por faixa de fornecedores, a faixa é obrigatória e não pode estar invertida

Com os dois códigos de fornecedor em branco, a recusa é **\* Informe o fornecedor \***;
com o inicial maior que o final, a recusa é
**\* Codigo inicial maior que o final \***.

### RN-06 — Um pedido de cada vez por órgão e relatório

Antes de conferir os parâmetros, e só no pedido por faixa de fornecedores, o sistema
procura um pedido já registrado para o mesmo tipo de órgão e o mesmo relatório. Achando,
recusa com **\* Relatorio ja esta em processamento. Aguarde. \*** e não confere mais
nada. A procura é por qualquer pedido, sem olhar a situação dele nem a data.

[?] Como o sistema não olha a situação do pedido, um pedido antigo que continue na base
bloqueia os pedidos seguintes daquele órgão, e esta tela não oferece como tirá-lo dali.
Quem remove esses pedidos está fora desta jornada. Pergunta ao site.

[?] A procura é feita com o grupo em branco, e o pedido que esta tela grava também sai
com o grupo em branco: se a intenção era bloquear por grupo, o grupo não está sendo usado
na procura. Pergunta ao site.

### RN-07 — Passando nas conferências, o pedido é numerado, registrado e entregue à emissão

O sistema toma o próximo número de pedido (o seguinte ao último já registrado), registra
o pedido com o relatório, a data e a hora em que foi pedido, a matrícula, o terminal, a
impressora, o órgão e a coordenação de quem opera, e marca o pedido como requisitado; os
parâmetros informados seguem com o pedido para a emissão. Em seguida o sistema monta a
execução do relatório e a entrega ao serviço que dispara a emissão pela impressora da
sessão.

[?] O número do pedido é o último registrado mais um, lido sem travamento: dois pedidos
simultâneos podem receber o mesmo número, e o acervo não diz o que acontece nesse caso.
Pergunta ao site.

[?] No pedido por faixa de fornecedores, o registro guarda, no lugar dos parâmetros
informados, uma área de parâmetros que esse caminho não preenche — os parâmetros
informados vão para outro campo do mesmo pedido. Se isso é intencional ou resto do
pedido anterior, o acervo não diz. Pergunta ao site.

[?] A tela não mostra mensagem de confirmação depois de registrar o pedido; o que quem
opera vê ao voltar não está no programa. Pergunta ao site.

[?] A tela entrega a execução do relatório e não acompanha o resultado: o que o serviço
de relatórios faz com o pedido — se imprime, se guarda, se devolve erro — não está no
acervo lido. Pergunta ao site.

### RN-08 — A tela só grava o pedido; os cadastros são apenas lidos

Nenhum cadastro do sistema é alterado ou apagado por esta tela: o único registro que ela
cria é o do pedido de relatório (`S040T`), o mesmo cadastro usado pelas outras telas de
pedido de relatório do sistema. Esse pedido não deixa rastro na auditoria: o cadastro da
auditoria não é sequer declarado por esta tela.

[?] Se a ausência de rastro é intencional: quem pediu, quando e com que parâmetros não
fica registrado para auditoria. Pergunta ao site.

### RN-09 — Falha de banco interrompe o pedido

Toda leitura e a gravação testam o erro do banco; havendo erro, a transação é
interrompida com a mensagem de erro do sistema e o pedido não é considerado registrado.

### RN-10 — O acesso à tela e o acesso ao relatório são conferidos antes de tudo

Antes de conferir qualquer parâmetro, a tela passa pela autorização da tela, pela
autorização do relatório, pela rota e pela data e hora do sistema; sem qualquer uma delas,
o processamento para ali, nada é conferido e nada é registrado. Na abertura da tela, a
autorização da tela e a do relatório são conferidas de novo, e os campos do relatório não
chegam a ser habilitados quando elas recusam. Não tendo a tela no cadastro, o aviso é
**\* Tela nao disponivel \***; não tendo o meu código de acesso autorizado para a tela ou
para o relatório, o aviso é **\* Acesso negado para esta matricula \***. Nas operações de
inclusão, alteração e exclusão há ainda a permissão da própria operação: faltando ela, o
aviso é **\* Acesso negado para esta operacao \*** — e as demais operações passam sem que
essa permissão seja lida.

[?] As duas faltas de autorização — a da tela e a do relatório — saem como o mesmo aviso,
o de acesso negado para a matrícula: quem opera não tem como distinguir pela mensagem qual
das duas faltou. Se é intencional, pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Informar os parâmetros do relatório e pedir a sua emissão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C099P

  Cenário: RN-01 e RN-02 — abrir a tela pelo relatório escolhido no menu
    Dado que o menu anterior me mandou para esta tela com o relatório já escolhido
    Quando a tela abre
    Então vejo os campos daquele relatório
    E vejo a data do sistema e a descrição do tipo de órgão da minha sessão
    E nada é registrado

  Cenário: RN-01 — abrir a tela com um relatório que ela não atende
    Dado que a sessão traz o código de um relatório que esta tela não atende
    Quando a tela abre
    Então nenhum campo é habilitado
    E nada é conferido e nada é registrado
    E não vejo mensagem nenhuma

  Cenário: RN-03 — o pedido leva o contexto da sessão
    Dado que a tela anterior exigiu a impressora e a deixou na minha sessão
    Quando o pedido é registrado
    Então ele leva a minha matrícula, o tipo de órgão, o terminal e a impressora da sessão

  Cenário: RN-04 — período inicial inválido
    Dado que o relatório pedido é o que usa o período inicial e a faixa de classes
    Quando informo um dia, um mês e um ano que não formam uma data válida
    Então vejo "* Data invalida *"
    E nada é registrado

  Cenário: RN-04 — classe inicial em branco
    Dado que o relatório pedido usa a faixa de classes
    Quando confirmo sem informar a classe inicial
    Então vejo "* Informe a Classe inicial *"
    E nada é registrado

  Cenário: RN-04 — classe final menor que a inicial
    Dado que o relatório pedido usa a faixa de classes
    Quando informo uma classe final menor que a inicial
    Então vejo "* Classe final menor que inicial *"

  Cenário: RN-05 — faixa de fornecedores em branco
    Dado que o relatório pedido é o que usa a faixa de fornecedores
    Quando confirmo sem informar o fornecedor inicial nem o final
    Então vejo "* Informe o fornecedor *"
    E nada é registrado

  Cenário: RN-05 — fornecedor inicial maior que o final
    Dado que o relatório pedido usa a faixa de fornecedores
    Quando informo um fornecedor inicial maior que o final
    Então vejo "* Codigo inicial maior que o final *"

  Cenário: RN-06 — já existe pedido para o órgão e o relatório
    Dado que já existe um pedido registrado para o meu tipo de órgão e este relatório
    Quando confirmo o pedido por faixa de fornecedores
    Então vejo "* Relatorio ja esta em processamento. Aguarde. *"
    E nada é registrado

  Cenário: RN-07 — pedir o relatório por classe e período
    Dado que o relatório pedido usa o período inicial e a faixa de classes
    E informo um período inicial válido, a classe inicial e a classe final
    Quando confirmo
    Então o pedido é registrado com um número, a data e a hora do pedido, a minha matrícula, o terminal e a impressora da sessão
    E os parâmetros informados vão junto no pedido
    E a execução da emissão é entregue ao serviço de relatórios

  Cenário: RN-07 — pedir o relatório por faixa de fornecedores
    Dado que o relatório pedido usa a faixa de fornecedores
    E não há pedido em andamento para o meu órgão e este relatório
    E informo um fornecedor inicial e um fornecedor final válidos
    Quando confirmo
    Então o pedido é registrado com um número e os dados da minha sessão
    E a execução da emissão é entregue ao serviço de relatórios

  Cenário: RN-08 — recusa não registra nada
    Dado que confirmo um pedido com um parâmetro em falta ou inválido
    Quando a tela recusa
    Então nenhum pedido é registrado
    E nenhum cadastro do sistema é alterado

  Cenário: RN-08 — o pedido não fica na auditoria
    Quando o pedido é registrado
    Então o único registro criado é o do pedido de relatório
    E a auditoria não registra quem pediu nem com que parâmetros

  Cenário: RN-09 — falha de banco durante o registro do pedido
    Dado que a gravação do pedido falha no banco
    Quando confirmo o pedido
    Então a transação é interrompida com a mensagem de erro do sistema
    E o pedido não é considerado registrado

  Cenário: RN-10 — sem autorização para a tela ou para o relatório
    Dado que o meu código de acesso não autoriza esta tela ou este relatório
    Quando confirmo
    Então a tela não confere nenhum parâmetro
    E nenhum pedido é registrado
```
