# US — E508T — Consulta dos preparos do órgão filho

## Estória

Como **servidor da CRE**, quero **consultar os preparos já lançados para o órgão filho**, para que eu saiba que períodos já foram preparados, com que datas e em que situação eles estão antes de mexer em qualquer cálculo.

O preparo é o que organiza a distribuição do órgão: cada período tem o início e o limite do cálculo e um período de entrega. A tela que mantém o cálculo trabalha **um período por vez** — quem vai incluir, alterar ou excluir precisa de um lugar onde veja o conjunto inteiro sem risco de mexer nele. É o que esta tela faz: mostra os preparos do órgão e **não grava nada**.

## Contexto

Jornada S000M → E000M → E500M → E508T.
Ator: servidor de CRE — consulta os preparos do órgão filho do seu vínculo e escolhe um deles para abrir no cálculo.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de negócio.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela mostra, de uma vez, os preparos lançados para o órgão

A tela lista os preparos do órgão filho, **um por linha**, em até **11 linhas**. Cada linha traz o **início do cálculo**, o **limite do cálculo**, o **início da entrega** e o **limite da entrega**, em dia/mês/ano, e a **situação** do preparo, que aparece como **Calculada** quando a requisição já foi calculada. No cabeçalho a tela mostra o nome do órgão, a descrição do tipo de órgão do vínculo e a data do sistema.

Cada preparo é identificado pela **data de início do cálculo** — é ela que distingue dois preparos do mesmo órgão em períodos diferentes —, e é essa data que a linha carrega.

[?] Cada linha traz, entre as datas, duas marcas fixas — a mesma letra "A" — e o sistema só as preenche com esse valor; o que elas significam na máscara é pergunta ao site. E o dia, o mês e o ano de início do cálculo mostrados no cabeçalho só são preenchidos quando o órgão tem preparos suficientes para ocupar a última das 11 linhas; com menos que isso o campo fica zerado. Se a intenção era o cabeçalho identificar o preparo consultado, o caminho só faz isso em parte.

### RN-02 — A tela é de consulta; as operações de manutenção são recusadas

Esta tela só consulta, e é com a consulta que ela abre. Informada uma operação de manutenção — inclusão, alteração ou exclusão —, a recusa é **\* Operacao nao disponivel. Use CON \***, com o cursor no campo da operação e sem gravar nada.

A operação informada passa antes pela conferência de perfil: sem o flag daquela operação liberado no cadastro de acesso do servidor para esta tela, a recusa é **\* Acesso negado para esta operacao \***. A consulta em si não tem flag — não há como o perfil negar a consulta desta tela.

### RN-03 — O órgão é o do vínculo; informar outro é recusado

Quando o vínculo do servidor carrega um órgão filho, é esse órgão que a tela consulta, e ele já vem preenchido. Informar outro órgão é recusado com **\* Usuario sem acesso a outro orgao \***, nomeando o órgão do vínculo, com o cursor no órgão e sem gravar nada.

### RN-04 — Sem órgão no vínculo, o órgão tem de ser informado

Quando o vínculo não carrega órgão filho, a tela não propõe órgão nenhum, deixa o cursor no campo e **não lista preparo algum**. Confirmando sem informar o órgão, a recusa é **\* Informe o orgao \***, com o cursor no campo.

### RN-05 — O órgão tem de estar cadastrado

Informado o órgão — pelo vínculo ou pelo servidor —, ele é procurado no cadastro de órgãos. Não estando cadastrado, a recusa é **\* Orgao nao cadastrado \***, com o cursor no órgão e sem gravar nada.

### RN-06 — A coordenadoria considerada é a do vínculo

A coordenadoria regional escolar que governa a consulta é a do vínculo da sessão. Informar outra é recusado com **<- Usuario sem acesso ao grupo deste orgao \***, com o cursor no órgão e sem gravar nada.

[?] Há um caminho em que a coordenadoria informada é trocada pela cadastrada no próprio órgão antes da conferência, e ele só ocorre quando o órgão não tem preparo para o dia corrente. Qual das duas governa o acesso de fato — a do vínculo ou a do órgão — é pergunta ao site.

### RN-07 — A linha escolhida tem de estar preenchida

Para escolher um preparo, o servidor marca a linha com **X**. Marcada uma linha cuja data de início do cálculo está em branco, a recusa é **\* A linha deve estar preenchida \***, com o cursor na marca da linha, e nada é gravado.

[?] A linha marcada só chega adiante quando o dia, o mês e o ano do cabeçalho coincidem com o preparo que a tela leu. Trocando o órgão informado, se o preparo do órgão novo não for o do dia corrente, a linha marcada é descartada **sem aviso**. Se o cabeçalho deveria filtrar o preparo consultado, a guarda e o ramo não fecham: pergunta ao site.

### RN-08 — A linha escolhida abre o cálculo em consulta, levando o preparo

Marcada uma linha com data, a tela não faz mais nenhuma conferência aqui: ela **passa o preparo adiante** e a tela de cálculo abre com o que veio. Vão o **órgão filho**, o **nome do órgão**, a **coordenadoria**, a **operação de consulta** e a **data de início do cálculo daquela linha**, separada em dia, mês e ano.

A tela de cálculo recebe a origem identificada, adota a operação e as datas como estão e mostra **\* Consulta preparo \***, com o cursor no órgão. É essa identificação que faz a tela de cálculo abrir em **consulta** quando vem daqui: aberta pelo menu, ela abriria em inclusão. Sem essa passagem, quem quer ver o preparo teria de redigitá-lo na tela de cálculo.

### RN-09 — Órgão sem preparos é avisado

Quando o órgão não tem preparo nenhum lançado, a tela avisa **\* Orgao sem preparos cadastrados \*** e não mostra linha alguma.

### RN-10 — A consulta não grava nada

Nenhuma passagem desta tela inclui, altera ou exclui preparo do órgão, e nenhuma deixa registro de auditoria. A tela só lê: o cadastro de órgãos, as requisições de cálculo do órgão e o cadastro de telas do sistema.

### RN-11 — A tela só abre com a sessão na estação registrada e com acesso liberado

Antes de mostrar qualquer coisa, a tela confere três coisas: se a **estação** da sessão é a estação gravada no cadastro do funcionário; se a tela existe no **cadastro de telas** do sistema; e se existe **autorização de acesso** do servidor para esta tela.

- Estação diferente: o acesso é **encerrado**, sem abrir a tela.
- Tela fora do cadastro: **\* Tela nao disponivel \***.
- Sem autorização: **\* Acesso negado para esta matricula \***.
- Pedido de segunda página: **\* Acesso a pagina 2 negado \***.

Nas recusas de cadastro — tela fora do cadastro, sem autorização e pedido de segunda página — o sistema devolve o servidor ao menu principal, e nada é gravado.

### RN-12 — A tela pode ser trocada pela tela indicada no campo de destino

Se a confirmação vier com o código de outra tela no campo de **tela de destino**, é essa tela que abre e esta não faz mais nada. As saídas comuns — encerrar a sessão, voltar à tela anterior e ir ao menu — valem aqui como nas demais telas.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta dos preparos do órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E508T

  Cenário: A tela lista os preparos do órgão do vínculo
    Dado que o meu vínculo carrega o órgão filho e a coordenadoria regional escolar
    Quando abro a E508T
    Então o órgão já vem preenchido, com o nome do órgão e a data do sistema no cabeçalho
    E vejo os preparos lançados, um por linha, em até 11 linhas
    E cada linha mostra o início e o limite do cálculo e o início e o limite da entrega
    E a situação aparece como "Calculada" quando a requisição já foi calculada
    E nada é gravado

  Cenário: Órgão sem preparos
    Dado que o órgão não tem nenhum preparo lançado
    Quando abro a E508T
    Então vejo o aviso "* Orgao sem preparos cadastrados *"
    E nenhuma linha é preenchida

  Cenário: Sem órgão no vínculo, a tela não propõe nem lista nada
    Dado que o meu vínculo não carrega órgão filho
    Quando abro a E508T
    Então o campo do órgão fica em branco, com o cursor nele
    E nenhum preparo é listado

  Cenário: Confirmação sem informar o órgão é recusada
    Dado que o meu vínculo não carrega órgão filho
    Quando confirmo sem informar o órgão
    Então vejo "* Informe o orgao *"
    E o cursor volta para o órgão

  Cenário: Órgão de outro vínculo é recusado
    Dado que o meu vínculo carrega um órgão filho
    Quando informo outro órgão
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor volta para o órgão

  Cenário: Órgão não cadastrado é recusado
    Quando informo um órgão que não existe no cadastro de órgãos
    Então vejo "* Orgao nao cadastrado *"
    E o cursor volta para o órgão

  Cenário: Coordenadoria de outro grupo é recusada
    Quando informo uma coordenadoria diferente da do meu vínculo
    Então vejo "<- Usuario sem acesso ao grupo deste orgao *"
    E nada é gravado

  Cenário: Operação de manutenção é recusada
    Dado que estou na E508T
    Quando confirmo com a operação de inclusão, de alteração ou de exclusão
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor volta para o campo da operação
    E nada é gravado

  Cenário: Operação sem autorização no perfil é recusada
    Dado que o meu perfil não tem aquela operação liberada para esta tela
    Quando confirmo com ela
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Linha marcada sem data é recusada
    Dado que estou na E508T
    Quando marco uma linha que está em branco
    Então vejo "* A linha deve estar preenchida *"
    E o cursor fica na marca da linha
    E nada é gravado

  Cenário: Linha marcada abre a consulta do cálculo
    Dado que a linha tem a data de início do cálculo
    Quando marco essa linha e confirmo
    Então a tela de cálculo abre em consulta
    E vejo o aviso "* Consulta preparo *", com o cursor no órgão
    E ela recebeu o órgão, o nome do órgão, a coordenadoria e a data de início do cálculo da linha
    E nada foi gravado por esta tela

  Cenário: A tela não grava nada
    Dado que estou na E508T
    Quando a tela termina qualquer uma das suas passagens
    Então nenhum preparo é incluído, alterado ou excluído
    E nenhum registro de auditoria é gravado

  Cenário: Sessão em estação diferente encerra o acesso
    Dado que a estação da minha sessão não é a gravada no meu cadastro
    Quando abro a E508T
    Então o acesso é encerrado
    E a tela não abre

  Cenário: Tela indisponível ou sem autorização
    Dado que a tela não existe no cadastro de telas do sistema, ou que não tenho acesso a ela
    Quando tento abri-la
    Então vejo "* Tela nao disponivel *" ou "* Acesso negado para esta matricula *"
    E o sistema me devolve ao menu principal
    E nada é gravado

  Cenário: Segunda página é negada
    Dado que estou na E508T
    Quando a requisição pede a segunda página da tela
    Então vejo "* Acesso a pagina 2 negado *"
    E nada é gravado

  Cenário: Outra tela indicada no campo de destino
    Dado que estou na E508T
    Quando informo o código de outra tela no campo de tela de destino e confirmo
    Então essa outra tela é aberta
    E a E508T não faz mais nada
```
