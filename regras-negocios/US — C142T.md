# US — C142T — Manter tipos de licitação

## Estória

Como **servidor de CRE**, quero **manter a lista dos tipos de licitação do sistema — incluir um tipo novo e corrigir a descrição de um que já existe — e, de uma linha da lista, ir ver quais telas usam aquele tipo**, para que **toda licitação seja classificada por um tipo que existe e tem descrição, e cada tipo tenha declaradas as telas que pode usar**.

O tipo de licitação é a classificação com que o sistema reconhece a licitação: outros treze cadastros do sistema carregam um tipo de licitação para classificar o que registram. Um tipo sem descrição, ou cadastrado duas vezes, deixa quem registra a licitação sem saber qual escolher. E um tipo que nasce sem as telas dele declaradas fica sem nenhuma tela liberada — por isso esta tela não termina nela mesma quando inclui: ela entrega o servidor à tela onde o uso daquele tipo é declarado. O cadastro é do sistema inteiro, não de uma secretaria: o que se cadastra aqui vale para todas.

## Contexto

Jornada S000M → C000M → C015M → C142T.
Ator: servidor de CRE — mantém a lista dos tipos de licitação e, de uma linha dela, vai conferir as telas de uso do tipo.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de negócio. Os dois menus do caminho não gravam nada e não têm cadastro próprio: só encaminham a sessão que a entrada montou.

A `C142T` é uma tela de transação, não um menu: ela é uma **lista de tipos de licitação** de treze linhas e termina encadeando, sem passar por menu, com a tela das **telas de uso de cada tipo** (`C148T`). Da sessão ela usa o **órgão**, a **data do sistema** e, para autorizar e para auditar, a **matrícula**, o **código de acesso**, a **CRE**, o **tipo de órgão**, o **terminal** e o **número do processo** — essa carga é regra da entrada e está no anexo, em **Regras que se revelaram da entrada**.

As regras abaixo são só as da tela desta jornada; as da entrada não se repetem aqui.

---

## Regras de negócio

### RN-01 — O cadastro dos tipos de licitação e o que esta tela faz nele

O cadastro dos tipos de licitação guarda **dois** dados por tipo: o **código**, de dois dígitos, que identifica o tipo e não se repete, e a **descrição**, de trinta posições, de preenchimento obrigatório. O cadastro é dimensionado para **mil** registros; como o código tem dois dígitos, cabem **noventa e nove** tipos utilizáveis — o código zero é o que a tela entende por linha vazia, e nenhuma operação o trata.

O cadastro **não é por secretaria**: ele não guarda secretaria, coordenadoria nem órgão, e por isso o tipo cadastrado aqui vale para todas as secretarias. Outros **treze** cadastros do dicionário carregam um tipo de licitação para classificar o que guardam.

Esta tela é a **única** que escreve nesse cadastro: dos **506** programas do lote, **22** carregam a cópia do cadastro e só esta tela executa a gravação — os outros **21** apenas trazem os trechos de gravação que o gerador declara para todo cadastro que o programa enxerga, e declaração não é execução. A tela **inclui** e **altera**; **não exclui** — não há operação de exclusão nela, e o trecho de exclusão declarado para esse cadastro nunca é executado.

### RN-02 — A lista: treze linhas, na ordem do cadastro, com a descrição do cadastro

A tela é uma **lista de treze linhas**, uma por tipo de licitação. Cada linha carrega quatro dados: o **código** do tipo, a **descrição**, a **ação** da linha e a **marca** da linha — as duas últimas são do servidor, não do cadastro. A **descrição exibida é a do cadastro**, recarregada a cada exibição; o que o terminal devolver nesse campo é descartado.

A leitura começa pelo **tipo que a sessão traz como referência**; na primeira abertura de uma sessão não há referência, e a lista começa pelo primeiro tipo do cadastro. Quando o cadastro acaba antes da última linha, as linhas restantes não são preenchidas.

[?] A continuação da lista de uma exibição para a seguinte: a referência da sessão é reescrita a cada linha lida, e a exibição seguinte parte dela, mas o contrato de leitura do banco não está no material lido, e não afirmo se a segunda exibição continua da linha seguinte à última mostrada ou repete a mesma página. Pergunta ao site.

### RN-03 — Sem nenhum tipo para mostrar, a tela avisa

Quando não há nenhum tipo de licitação a mostrar, a lista fica sem a primeira linha e a tela avisa **\* Nao existem tipos de licitacao cadastrados \***, com o cursor na coluna do tipo da primeira linha.

### RN-04 — O cabeçalho mostra o órgão da sessão e a data do sistema

O órgão e a data que a tela exibe são os da sessão — o órgão a que o servidor está vinculado e a data do sistema naquele momento. O que o terminal devolver nesses dois campos é descartado antes de qualquer uso.

### RN-05 — O código do tipo é tratado como número

O código do tipo passa pela conferência numérica antes de qualquer uso: campo em branco vira zero, os zeros à esquerda são descartados e o que não for número é recusado, com o cursor de volta na coluna do tipo daquela linha. O que não passa por essa conferência não chega às leituras nem à gravação.

### RN-06 — A tela trabalha em alterar e consultar, e sem opção escolhida abre em consulta

A opção de manutenção acompanha a sessão; quando a tela chega sem nenhuma opção, ela adota a **consulta**. A tela aceita **alterar** e **consultar**; qualquer outra opção é recusada com **\* Opcao nao disponivel. Use ALT ou CON \***, com o cursor de volta no campo da opção, e nada é gravado.

[?] A recusa manda usar ALT e CON, e a conferência compara a opção com os códigos de alteração e de consulta, que o programa carrega da tabela de mensagens do sistema — a mesma de onde sai o texto da mensagem. O material lido não traz o valor desses códigos, então não afirmo se a comparação aceita exatamente o que a mensagem manda. Pergunta ao site.

### RN-07 — A consulta não grava nada

Com a opção de consulta, a tela não valida nenhuma linha e não chega à gravação: nada é incluído, nada é alterado e nenhum registro de auditoria é criado. A consulta serve para ler a lista e, pela marca da linha, para ir às telas de uso do tipo (RN-12).

### RN-08 — Incluir exige um tipo que ainda não exista e a descrição preenchida

A inclusão de uma linha tem duas conferências, nesta ordem: se o código informado **já existe** no cadastro, a recusa é **\* Tipo de licitacao ja cadastrado \***, com o cursor na coluna da ação da linha; se não existe, mas a **descrição** está em branco, a recusa é **\* Informe a descricao \***, com o cursor na coluna da descrição. Passando as duas, o tipo é criado no cadastro com o código e a descrição informados, e a inclusão vai para a auditoria (RN-11).

[?] A rotina de gravação prevê uma recusa por destino inválido, e essa recusa aparece na ficha da tela; a tela, porém, desliga essa conferência antes de qualquer inclusão. Por esta tela, essa recusa não acontece. Pergunta ao site se a ficha está defasada.

### RN-09 — Alterar exige um tipo cadastrado e a descrição preenchida

A alteração de uma linha tem as mesmas duas conferências, com a primeira no sentido invertido: se o código informado **não existe** no cadastro, a recusa é **\* Tipo de licitacao nao cadastrado \***, com o cursor na coluna da ação; se existe, mas a **descrição** está em branco, a recusa é **\* Informe a descricao \***. Passando as duas, a descrição do tipo é substituída pela informada, e a alteração vai para a auditoria (RN-11); o código, que é a chave, não muda.

### RN-10 — Linha sem tipo, ou com ação diferente de incluir e alterar, não faz nada

Linha com o código em branco — que a conferência numérica transforma em zero — é ignorada. Linha com código preenchido e ação em branco, ou com ação diferente de incluir e de alterar, também não faz nada: não gera recusa e não grava. Só as duas ações, com o código preenchido, são tratadas.

### RN-11 — Toda inclusão e toda alteração deixam rastro na auditoria

Cada tipo incluído ou alterado gera um registro na auditoria, com **o cadastro tocado** (o cadastro dos tipos de licitação), **a tela de origem** da operação, **a operação** (inclusão ou alteração), **o valor anterior** e **o valor novo**, e o contexto da sessão — matrícula, CRE, tipo de órgão, órgão, terminal, data, hora e número do processo. Na inclusão, o valor anterior vai em branco e o valor novo é o tipo gravado; na alteração, o valor anterior é o tipo como estava e o valor novo é o tipo com a descrição corrigida.

[?] A auditoria da inclusão está presa a uma marca de status que o programa não escreve: ele limpa o status imediatamente antes de gravar, e o material lido não mostra quem escreveria o valor que a condição testa. Se quem escreve é o banco, a inclusão pode não ser auditada. Pergunta ao site.

### RN-12 — Marcar a linha leva às telas de uso do tipo

A marca da linha é o pedido de ver **quais telas usam aquele tipo**. Com a marca preenchida e o tipo informado e cadastrado, a tela abre a tela das telas de uso (`C148T`) **em consulta**, já com o tipo em foco — código e descrição lidos do cadastro. Marcando uma linha **sem** o tipo informado, a recusa é **\* Consulte telas de uso para linha preenchida \***, com o cursor na coluna da marca; marcando com um tipo que **não está** no cadastro, a recusa é **\* Tipo de licitacao nao cadastrado \***, com o cursor na mesma coluna.

A marca é conferida **antes** da ação da linha: a linha marcada não é incluída nem alterada, e a ida às telas de uso recusa a página inteira (RN-13).

[?] A recusa manda consultar as telas de uso de uma linha **preenchida**, mas é exatamente a linha **sem** tipo que ela barra. Ou a mensagem está trocada, ou o que a tela chama de linha preenchida é outra coisa. Pergunta ao site; não escolho um dos dois.

### RN-13 — Uma linha recusada recusa a página inteira

A recusa de uma linha interrompe a validação das linhas seguintes e a página não chega à gravação: nenhuma linha é incluída nem alterada enquanto houver uma linha recusada — não existe gravação parcial da página. A linha marcada para consultar as telas de uso (RN-12) também recusa a página: ela não é gravada, e as demais linhas da mesma confirmação também não.

[?] A marca que fecha a gravação da página, nas recusas, vem da rotina comum de mensagem, que não está no material lido; a passagem para as telas de uso escreve a dela por conta própria. Não afirmo por qual das duas a página fecha. Pergunta ao site.

### RN-14 — Depois de incluir, a tela entrega o tipo às telas de uso, em alteração

Terminada a página, se houve inclusão, a tela **não fica nela**: ela abre a tela das telas de uso (`C148T`) já no modo de **alteração**, com o tipo recém-incluído em foco — o código, a descrição lida do cadastro e a indicação de que a passagem veio desta tela. É assim que um tipo novo sai daqui com as telas dele declaradas.

### RN-15 — Nada é exibido nem gravado sem a autorização da tela e da operação

Antes de exibir, a tela confere a autorização da tela para o código de acesso do servidor e o estado da sessão; sem isso não exibe, e a recusa é a da rotina de segurança do sistema. Antes de manter, confere a rota e a permissão da operação: **incluir exige a inclusão liberada** e **alterar exige a alteração liberada** para a tela. Se qualquer conferência não retorna OK, a tela limpa o status e sai: nada é validado, nada é gravado e nada é auditado.

### RN-16 — Prefixo de tela preenchido abandona a validação

Se a transação chega com o prefixo de tela preenchido, a validação da manutenção é interrompida antes de qualquer teste de linha: nada é validado e nada é gravado.

[?] O programa só lê esse prefixo; quem o preenche não aparece em nenhuma das telas da jornada. Ou o terminal o preenche, ou o abandono é inalcançável. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os tipos de licitação e ver quais telas cada um usa

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C142T

  Cenário: RN-01 — o tipo cadastrado vale para todas as secretarias
    Dado que cadastrei um tipo de licitação
    Quando outro servidor, de outra secretaria, abre a lista
    Então ele vê o mesmo tipo, com a mesma descrição

  Cenário: RN-02 — a lista mostra treze linhas, com a descrição do cadastro
    Quando abro a tela C142T
    Então vejo até treze linhas, uma por tipo de licitação
    E cada linha traz o código, a descrição do cadastro, a ação e a marca
    E nada é gravado

  Cenário: RN-03 — nenhum tipo cadastrado
    Dado que não há nenhum tipo de licitação a mostrar
    Quando abro a tela C142T
    Então vejo "* Nao existem tipos de licitacao cadastrados *"
    E o cursor fica na coluna do tipo da primeira linha

  Cenário: RN-04 — o cabeçalho é o da sessão
    Quando abro a tela C142T
    Então o órgão exibido é o da minha sessão
    E a data exibida é a do sistema
    E o que o terminal mandou nesses campos é descartado

  Cenário: RN-05 — código do tipo com texto
    Quando informo texto no código do tipo de uma linha
    Então o código é recusado antes de qualquer uso
    E o cursor volta à coluna do tipo daquela linha
    E nada é gravado

  Cenário: RN-06 — a tela abre em consulta quando a sessão não traz opção
    Quando abro a tela C142T sem opção escolhida
    Então a tela está em consulta
    E nada é gravado

  Cenário: RN-06 — opção que a tela não aceita
    Quando informo uma opção diferente de alterar e de consultar
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: RN-07 — a consulta não grava nada
    Dado que estou na tela C142T em consulta
    Quando confirmo a tela
    Então nenhuma linha é validada
    E nenhum tipo é incluído ou alterado
    E nenhum registro de auditoria é criado

  Cenário: RN-08 — incluir um tipo novo
    Dado que estou na tela C142T no modo de alteração
    E informo o código de um tipo que não existe e a descrição
    Quando confirmo a inclusão
    Então o tipo passa a constar do cadastro, com a descrição informada
    E a inclusão fica registrada na auditoria

  Cenário: RN-08 — incluir um tipo que já existe
    Dado que estou na tela C142T no modo de alteração
    Quando informo o código de um tipo que já está no cadastro
    Então vejo "* Tipo de licitacao ja cadastrado *"
    E o cursor fica na coluna da ação da linha
    E nada é gravado

  Cenário: RN-08 — incluir sem a descrição
    Dado que estou na tela C142T no modo de alteração
    E informo o código de um tipo que não existe
    Quando deixo a descrição em branco e confirmo
    Então vejo "* Informe a descricao *"
    E o cursor fica na coluna da descrição
    E nada é gravado

  Cenário: RN-09 — alterar a descrição de um tipo cadastrado
    Dado que estou na tela C142T no modo de alteração
    E informo o código de um tipo que existe, com outra descrição
    Quando confirmo a alteração
    Então a descrição do tipo passa a ser a informada
    E o código do tipo não muda
    E a alteração fica registrada na auditoria

  Cenário: RN-09 — alterar um tipo que não existe
    Dado que estou na tela C142T no modo de alteração
    Quando informo o código de um tipo que não está no cadastro
    Então vejo "* Tipo de licitacao nao cadastrado *"
    E o cursor fica na coluna da ação da linha
    E nada é gravado

  Cenário: RN-09 — alterar sem a descrição
    Dado que estou na tela C142T no modo de alteração
    E informo o código de um tipo que existe
    Quando deixo a descrição em branco e confirmo
    Então vejo "* Informe a descricao *"
    E nada é gravado

  Cenário: RN-10 — linha sem tipo, ou com ação desconhecida
    Dado que estou na tela C142T no modo de alteração
    Quando deixo o código da linha em branco, ou escrevo uma ação diferente de incluir e de alterar
    Então a linha não é validada, não recebo recusa e nada é gravado para ela

  Cenário: RN-11 — toda gravação deixa rastro na auditoria
    Dado que incluí um tipo de licitação e alterei a descrição de outro
    Então ficam registradas a inclusão e a alteração
    E a inclusão fica com o valor anterior em branco e o valor novo gravado
    E a alteração fica com o valor anterior e o valor novo
    E as duas ficam com a minha matrícula, a CRE, o órgão, o terminal, a data, a hora e o número do processo

  Cenário: RN-12 — marcar uma linha com o tipo informado
    Dado que estou na tela C142T
    E marco uma linha cujo tipo está no cadastro
    Quando confirmo
    Então a tela das telas de uso C148T se abre em consulta
    E o tipo marcado já está em foco

  Cenário: RN-12 — marcar uma linha sem o tipo
    Dado que estou na tela C142T
    Quando marco uma linha e deixo o tipo em branco
    Então vejo "* Consulte telas de uso para linha preenchida *"
    E o cursor fica na coluna da marca
    E nada é gravado

  Cenário: RN-12 — marcar uma linha com um tipo não cadastrado
    Dado que estou na tela C142T
    Quando marco uma linha e informo um tipo que não está no cadastro
    Então vejo "* Tipo de licitacao nao cadastrado *"
    E nada é gravado

  Cenário: RN-13 — uma linha recusada recusa a página inteira
    Dado que estou na tela C142T no modo de alteração
    E uma das linhas da página é recusada
    Quando confirmo a tela
    Então nenhuma das outras linhas é gravada
    E a página não grava nada

  Cenário: RN-13 — a linha marcada também recusa a página
    Dado que estou na tela C142T no modo de alteração
    E uma linha está marcada para consultar as telas de uso
    E outra linha tem uma inclusão válida
    Quando confirmo a tela
    Então a inclusão não é gravada
    E nenhum registro de auditoria é criado

  Cenário: RN-14 — depois de incluir, a tela entrega o tipo às telas de uso
    Dado que estou na tela C142T no modo de alteração
    Quando incluo um tipo novo e confirmo a página
    Então a tela das telas de uso C148T se abre no modo de alteração
    E o tipo recém-incluído já está em foco
    E a passagem diz que veio da tela C142T

  Cenário: RN-15 — sem autorização para a tela
    Dado que o meu código de acesso não tem a tela C142T liberada
    Quando abro a tela C142T
    Então a lista não é exibida
    E recebo a mensagem da rotina de segurança

  Cenário: RN-15 — sem permissão para a operação
    Dado que o meu código de acesso não tem a inclusão liberada para a tela C142T
    Quando confirmo uma inclusão na tela C142T
    Então a operação é recusada pela rotina de segurança
    E nada é gravado
    E nenhum registro de auditoria é criado

  Cenário: RN-16 — prefixo de tela preenchido abandona a validação
    Dado que a transação chega à tela C142T com o prefixo de tela preenchido
    Quando a validação da manutenção começaria
    Então nenhuma linha é validada
    E nada é gravado
```
