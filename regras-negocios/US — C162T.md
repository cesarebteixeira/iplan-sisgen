# US — C162T — Manter os tipos de processo do órgão

## Estória

Como **servidor de CRE**, quero **manter os tipos de processo do tipo de órgão da minha
sessão**, para que os processos fiquem classificados por tipo e as telas que registram e
consultam processos possam mostrar a descrição do tipo escolhido.

O tipo de processo é a classificação que diz de que natureza é um processo. Ele não existe
solto no sistema: cada tipo pertence a um tipo de órgão, e é o tipo de órgão da sessão que
delimita o conjunto que o servidor enxerga e onde o tipo novo vai ficar. Sem o tipo
cadastrado, o processo fica sem classificação. O cadastro é de apoio e esta tela não o
esvazia: um tipo incluído por engano não sai por aqui.

## Contexto

Jornada S000M → C000M → C020M → C162T.

Ator: servidor de CRE — mantém, para o tipo de órgão da sua sessão, o cadastro dos tipos de
processo e a descrição de cada um.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A C162T é a última tela da jornada e não entrega registro nem operação a nenhuma outra. Ela é
aberta por escolha em menu, e não encadeada por outra tela: não recebe de quem a chamou nem o
registro nem o modo de operação — ela mesma decide o modo, e decide começar em consulta. O que
ela usa é o que a entrada deixou na sessão: a matrícula, o acesso, o privilégio, o tipo de
órgão e a CRE.

As regras abaixo são só as desta tela.

## Regras de negócio

### RN-01 — A tela mantém os tipos de processo do tipo de órgão da sessão

A tela opera o cadastro dos **tipos de processo**. Cada tipo tem um **código de 2 dígitos** e
uma **descrição de 40 caracteres**, e pertence a um **tipo de órgão**. O tipo de órgão não é
informado na tela: é o da sessão do servidor, e é ele que decide qual conjunto de tipos a tela
enxerga e onde o tipo novo vai ser gravado. Dentro de um tipo de órgão o mesmo código de tipo
existe uma vez só — o cadastro não aceita dois tipos com o mesmo código. A capacidade
declarada do cadastro é de **1.000** registros: é **capacidade** (o máximo esperado, parâmetro
de dimensionamento), não o volume cadastrado.

A tela apresenta **15 linhas** por vez e cada linha tem **3 campos**: o código do tipo, a
descrição e a marca que diz o que fazer com aquela linha. Além das linhas, a tela mostra a
identificação do tipo de órgão da sessão e a data do sistema. A lista é montada percorrendo o
cadastro do tipo de órgão da sessão a partir do primeiro código, na ordem do código, e a
varredura para quando a leitura encontra um registro de outro tipo de órgão — a tela não
mostra tipos de outro órgão.

[?] A identificação do tipo de órgão e a data do sistema que a tela exibe vêm da área da
sessão: os programas desta jornada só as copiam. Quem as preenche não está no material lido.
Pergunta ao site.

[?] A tela monta 15 linhas. Como o servidor alcança os tipos de processo além desses 15 — se a
página rola, se há mais de uma página, ou se a tela só trabalha com os 15 primeiros — não se
conclui do fonte desta tela. Pergunta ao site.

### RN-02 — A opção de manutenção aceita alteração e consulta, e a tela abre em consulta

A opção de manutenção da tela aceita **dois valores**: **alteração** e **consulta** — os
mesmos que a mensagem de recusa nomeia **ALT** e **CON**. Qualquer outro valor, inclusive a
opção de inclusão, que esta tela não oferece, é recusado com
**\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta no campo da opção, e
nada é conferido nem gravado nessa passagem.

Quando a tela abre sem opção informada, ela mesma assume a **consulta** e passa a exibi-la. A
inclusão e a alteração de fato não são escolhidas no campo da opção: elas vêm da marca de cada
linha.

[?] A mensagem manda usar **ALT** e **CON**, mas o que a tela confere são os códigos de
alteração e de consulta do sistema. Ou a máscara da tela traduz o que o servidor digita antes
de enviar, ou a mensagem está desalinhada da conferência. A máscara não está no material lido.
Pergunta ao site.

### RN-03 — A marca da linha inclui ou altera, e a tela não exclui

Cada linha tem uma **marca** de uma posição que diz o que fazer com aquela linha: **I** inclui
o tipo de processo, **A** altera um tipo já cadastrado. A tela **não exclui**: não existe marca
de exclusão, e um tipo incluído por engano não sai por aqui — só pode ter a descrição
alterada.

### RN-04 — Linha sem código ou com marca fora de I e A não é processada

Uma linha só entra na conferência quando tem o **código do tipo** preenchido **e** a marca
**I** ou **A**. Código zerado, marca em branco ou marca diferente dessas duas passam em claro:
a linha não é conferida, não grava nada e não gera aviso ao usuário.

[?] Quando uma linha é recusada, a conferência para e a mensagem aparece, mas a passagem que
grava não reconfere o indicador de erro que a recusa preencheu. Não se conclui do fonte desta
tela se a linha recusada ainda chega a ser gravada, nem se as demais linhas da mesma página são
gravadas depois de uma recusa. Pergunta ao site.

### RN-05 — Na inclusão o tipo de processo não pode existir

Para incluir, o código informado na linha é procurado no cadastro do tipo de órgão da sessão.
Se já houver um tipo com esse código, a inclusão é recusada com
**\* Tipo de processo ja cadastrado \***, com o cursor na coluna da marca, e nada é gravado.

### RN-06 — Na alteração o tipo de processo tem de existir

Para alterar, o código informado na linha também é procurado no cadastro do tipo de órgão da
sessão. Não havendo tipo com esse código, a alteração é recusada com
**\* Tipo de processo nao cadastrado \***, com o cursor na coluna da marca, e nada é gravado.

### RN-07 — A descrição é obrigatória nas duas operações

Tanto na inclusão quanto na alteração, a descrição em branco é recusada com
**\* Informe a descricao \***, com o cursor na coluna da descrição, e nada é gravado. No
cadastro, a descrição é o único campo marcado como obrigatório.

### RN-08 — A inclusão cria o tipo de processo no tipo de órgão da sessão

Com a marca **I**, o sistema cria o registro do tipo de processo com o **código informado na
linha**, a **descrição informada** e o **tipo de órgão da sessão**. O tipo de órgão não é
digitado na tela: é o que a entrada deixou na sessão, e é ele que decide a que órgão o tipo
novo passa a pertencer.

### RN-09 — A alteração grava a nova descrição do tipo

Com a marca **A**, o sistema lê o registro do tipo, guarda o valor anterior, trava o registro,
substitui a **descrição** pela que está na linha e grava. O **código do tipo** é a identidade
do registro: a alteração muda a descrição, não o código.

### RN-10 — Na consulta nada é gravado

Com a opção de manutenção em consulta, o processamento da linha é abandonado antes de qualquer
conferência de marca e antes de qualquer gravação — tanto na passagem de conferência quanto na
de gravação. A consulta é somente leitura: percorrer a página não inclui, não altera e não
deixa rastro na auditoria. Como a tela abre em consulta, abrir a tela também não grava.

### RN-11 — Tipo de órgão sem tipos de processo cadastrados é avisado

Quando a página é montada e o tipo de órgão da sessão não tem nenhum tipo de processo
cadastrado, a tela não mostra linha alguma e avisa
**\* Nao existem tipos de processo cadastrados \***, com o cursor na coluna do código do tipo
da primeira linha.

### RN-12 — Toda gravação deixa rastro na auditoria

Cada inclusão e cada alteração grava também um registro na trilha de auditoria: o cadastro
auditado, a operação, o valor anterior e o posterior e o contexto da sessão — a matrícula, a
CRE, o tipo de órgão, a tela, o terminal, o número do processo e a data e a hora. Na alteração,
o valor anterior é o registro como estava e o posterior é o registro já com a descrição nova;
na inclusão, o valor anterior vai em branco.

[?] Na inclusão, o rastro só é escrito quando o estado devolvido pela distribuição automática
do registro não indica dados recebidos de outro destino; na alteração o rastro é
incondicional. Esse estado vem do ambiente e não está nos fontes desta jornada: se a guarda
barrar, a inclusão grava o tipo de processo e não deixa rastro. Pergunta ao site.

### RN-13 — Nada é gravado sem as conferências de tela, de rota e de permissão

Antes de conferir a linha e antes de gravar, a tela entrega o contexto da sessão — a matrícula,
o acesso, o privilégio, o tipo de órgão, a CRE e a indicação de tela seguinte — às conferências
globais de rota e de permissão, e ainda confere a existência do próprio cadastro de telas. Se
qualquer uma delas não aprovar, a tela sai sem conferir a linha, sem gravar e sem deixar rastro
de auditoria.

[?] O que cada conferência exige — o cadastro que ela lê e o que ela considera aprovado — não
está nos fontes desta jornada: as rotinas são globais e aparecem aqui só como chamada. Pergunta
ao site.

### RN-14 — O código do tipo é conferido como número

O código do tipo informado na linha é conferido como número antes de qualquer operação: em
branco é tratado como zero, e o valor conferido volta formatado ao campo. Quando a conferência
numérica acusa erro, o cursor volta para o campo do código.

[?] A rotina que confere o número não está entre os fontes desta jornada; o que ela aceita e o
que ela recusa não se conclui daqui. Pergunta ao site.

### RN-15 — A indicação de tela seguinte preenchida abandona a manutenção

Se a transação chega com a **indicação de tela seguinte** preenchida, a conferência da
manutenção é abandonada antes de qualquer teste de linha e antes de qualquer gravação; a
indicação é entregue à conferência de rota.

[?] Nenhum programa desta jornada preenche essa indicação, e o que a conferência de rota faz
com ela não está no material lido. Pergunta ao site.

### RN-16 — A recusa de destino inválido não é apresentada por esta tela

O ramo que produz a recusa de **destino inválido** só roda quando a distribuição automática do
registro está marcada; a tela limpa essa marca imediatamente antes dos pontos em que a
distribuição aconteceria. Por esta tela, portanto, a mensagem de destino inválido que a ficha
da tela lista **não** é apresentada.

[?] A ficha da tela, no grafo, lista essa recusa; o fonte não alcança o ramo. Divergência
entre a ficha e o comportamento, a confirmar com quem mantém o grafo. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Manutenção dos tipos de processo do órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão
    E tenho acesso à tela C162T

  Cenário: A tela lista os tipos de processo do tipo de órgão da sessão
    Dado que estou na tela C162T
    Quando a página é apresentada
    Então vejo até 15 linhas, cada uma com o código do tipo, a descrição e a marca
    E vejo a opção de manutenção, a identificação do tipo de órgão e a data do sistema
    E só aparecem tipos de processo do meu tipo de órgão
    E o cadastro comporta até 1.000 tipos de processo

  Cenário: A tela abre em consulta
    Dado que estou na tela C162T sem informar a opção de manutenção
    Quando a página é apresentada
    Então a tela assume a consulta e a exibe no campo da opção
    E nada é gravado

  Cenário: Opção de manutenção diferente de ALT e de CON é recusada
    Dado que estou na tela C162T
    Quando informo uma opção de manutenção diferente de ALT e de CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo da opção
    E nada é gravado

  Cenário: A marca I inclui e a marca A altera, e não existe exclusão
    Dado que estou na tela C162T no modo ALT
    Quando procuro na página a marca que removeria um tipo de processo
    Então só existem as marcas I e A
    E o tipo já cadastrado continua no cadastro

  Cenário: Linha sem código ou com marca fora de I e A é ignorada
    Dado que estou na tela C162T no modo ALT
    Quando deixo o código zerado, ou a marca em branco, ou informo uma marca que não é I nem A
    Então a linha não é conferida, não grava nada e não gera aviso

  Cenário: Inclusão recusa tipo de processo já cadastrado
    Dado que estou na tela C162T no modo ALT
    E que o tipo de processo já está cadastrado no meu tipo de órgão
    Quando informo a marca I para esse código de tipo
    Então vejo "* Tipo de processo ja cadastrado *"
    E o cursor fica na coluna da marca
    E o tipo existente não é alterado

  Cenário: Alteração recusa tipo de processo não cadastrado
    Dado que estou na tela C162T no modo ALT
    Quando informo a marca A para um código de tipo que não existe
    Então vejo "* Tipo de processo nao cadastrado *"
    E o cursor fica na coluna da marca
    E nada é gravado

  Cenário: Inclusão e alteração exigem a descrição
    Dado que estou na tela C162T no modo ALT
    Quando tento incluir ou alterar um tipo de processo sem descrição
    Então vejo "* Informe a descricao *"
    E o cursor fica na coluna da descrição
    E nada é gravado

  Cenário: Inclusão de um tipo de processo novo
    Dado que estou na tela C162T no modo ALT
    Quando informo o código de um tipo que ainda não existe, a descrição e a marca I
    Então o tipo de processo é incluído no tipo de órgão da minha sessão
    E a inclusão fica registrada na auditoria

  Cenário: Alteração grava a nova descrição do tipo
    Dado que estou na tela C162T no modo ALT
    E que o tipo de processo está cadastrado
    Quando informo a nova descrição e a marca A
    Então a descrição do tipo é gravada e o código continua o mesmo
    E a descrição anterior fica registrada na auditoria

  Cenário: Na consulta nada é gravado
    Dado que estou na tela C162T no modo CON
    Quando percorro as linhas e confirmo a página
    Então nenhuma linha é conferida e nenhuma é gravada
    E nenhum registro de auditoria é criado

  Cenário: Tipo de órgão sem tipos de processo cadastrados é avisado
    Dado que estou na tela C162T e o meu tipo de órgão não tem tipo de processo cadastrado
    Quando a página é apresentada
    Então vejo "* Nao existem tipos de processo cadastrados *"
    E o cursor fica na coluna do código do tipo da primeira linha

  Cenário: Toda gravação deixa rastro na auditoria
    Dado que confirmei uma inclusão ou uma alteração na C162T
    Quando a gravação termina
    Então existe um registro de auditoria do tipo de processo
    E com a operação, o cadastro auditado, o valor anterior e o valor posterior
    E com a matrícula, a CRE, o tipo de órgão, o terminal e a data e a hora

  Cenário: Nada é gravado sem a conferência de tela, de rota e de permissão
    Dado que estou na tela C162T
    Quando a conferência de tela, de rota ou de permissão não retorna OK
    Então a tela volta sem conferir as linhas e sem gravar nada
    E nenhum registro de auditoria é criado

  Cenário: O código do tipo é conferido como número
    Dado que estou na tela C162T
    Quando informo no código do tipo um valor que não é número
    Então a conferência numérica acusa erro e o cursor volta para o campo do código
    E o código não é tratado como um tipo de processo

  Cenário: A indicação de tela seguinte preenchida abandona a manutenção
    Dado que a transação chega à C162T com a indicação de tela seguinte preenchida
    Quando a conferência da manutenção começaria
    Então nenhuma linha é conferida e nada é gravado
    E a indicação é entregue à conferência de rota

  Cenário: A tela não apresenta a recusa de destino inválido
    Dado que estou na tela C162T no modo ALT e confirmei uma inclusão
    Quando a gravação é preparada
    Então a tela limpa a marca de distribuição automática do registro
    E a recusa de destino inválido não é apresentada
```
