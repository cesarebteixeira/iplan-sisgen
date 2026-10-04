# US — E028T — Excluir um pedido de alimentação escolar

## Estória

Como **servidor de CRE**, quero **excluir um pedido de alimentação escolar já
fechado, informando o órgão, a coordenadoria regional escolar, o número do pedido e o
ano da entrega**, para que **um pedido lançado errado ou que não vai ser entregue saia
do sistema com tudo o que ele levou**.

A exclusão não é um ajuste de tela: ela tira o pedido inteiro, com todos os gêneros
que ele levou, e deixa registrado quem apagou e quando. Como o pedido já está fechado,
ele não pode mais ser corrigido — apagá-lo é a única saída para um pedido que não deve
ser cumprido. Se ele ficasse, continuaria valendo para a entrega do período e para o
que a secretaria compra e distribui às escolas.

## Contexto

Jornada S000M → E000M → E010M → E028T.

Ator: servidor de CRE — informa o órgão, a coordenadoria regional escolar, o número
do pedido e o ano da entrega e exclui um pedido de alimentação escolar já fechado.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas do meio do caminho são menus: não encadeiam a transação e não deixam,
de próprio, nada que a tela de destino use — o que esta tela lê da sessão vem da
entrada. A tela desta jornada **não** muda de comportamento conforme a tela que a
chamou: ela não compara a tela de origem com código nenhum nem tem operação
alternativa que dependa disso. E não encadeia para outra tela: a única tela que ela
abre é ela mesma, para pedir a confirmação da exclusão.

Da sessão a tela usa a matrícula, o código de acesso, a estação, o tipo de órgão (a
secretaria a que o órgão tem de pertencer), a coordenadoria regional escolar e o
órgão filho do vínculo, além da descrição do órgão da sessão e da data do sistema,
que ela mostra no cabeçalho.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela exclui um pedido, e só isso

A tela não inclui nem altera: a única operação que ela executa é a exclusão de um
pedido. Ao ser aberta, ela mesma põe a operação de exclusão no campo da operação e a
exige de volta — qualquer outra operação é recusada com
**\* Opcao nao disponivel. Use EXC \***, o cursor volta ao campo da operação e nada é
apagado. É coerente com o resto: o que se apaga aqui é um pedido já fechado (RN-08),
isto é, um pedido que cumpriu o seu ciclo.

Não há modo de consulta nesta tela: abrir e percorrer os campos não grava nada, mas
também não registra consulta nenhuma — a tela serve para excluir.

[?] A tela repõe a operação de exclusão a cada abertura e manda usar a tecla EXC, mas a
máscara da tela não está no acervo: não se conclui se a tecla de outra operação pode
sobrescrever esse campo — e, nesse caso, o servidor veria a recusa. Pergunta ao site.

### RN-02 — A tela lê cinco cadastros e escreve em três

Para excluir, a tela consulta **cinco cadastros** — o registro das telas, o cadastro
dos órgãos, o cadastro dos pedidos, o cadastro dos gêneros do pedido e o cadastro dos
fornecedores —, além dos dois que as conferências de acesso leem (o cadastro do
servidor e o das autorizações do código de acesso, RN-11). Escreve em **três**: apaga
cada gênero do pedido, apaga o próprio pedido e inclui um registro de auditoria para
cada registro apagado. Nenhum outro cadastro é incluído, alterado ou excluído, e a
simples abertura da tela não escreve nada.

Os cadastros são dimensionados para: pedidos **10 milhões**; gêneros do pedido **200
milhões**; órgãos **12 mil**; fornecedores **10 mil**; telas **2 mil**; auditoria **60
milhões**. Capacidade declarada é o máximo esperado do dimensionamento, e não o volume
já cadastrado.

### RN-03 — Ao abrir, a tela propõe o órgão e a coordenadoria da sessão

Ao ser aberta, a tela preenche o órgão filho e a coordenadoria regional escolar com os
do vínculo da sessão e mostra no cabeçalho a descrição do órgão da sessão e a data do
sistema. Quando o vínculo não tem órgão filho, o campo do órgão fica em branco, para o
servidor informar. O cursor fica no número do pedido; só quando o vínculo não tem
órgão nem coordenadoria ele fica no campo do órgão, que é o que falta informar. Abrir
a tela só lê: não apaga nem grava nada.

[?] O órgão filho que a tela propõe vem de uma área da sessão, e nenhum programa do
acervo lhe atribui valor — a única atribuição é o zeramento, na reinicialização da
sessão. A entrada carrega o órgão filho do vínculo para outra área da sessão, e a
passagem de uma para a outra não está nos fontes fornecidos. Se ela não acontecer, o
campo abre em branco e a restrição de órgão (RN-04) não tem por onde valer. Pergunta
ao site.

### RN-04 — O servidor só exclui o pedido do seu órgão e do seu grupo

Quando o vínculo da sessão carrega um órgão filho, o órgão informado tem de ser esse;
outro é recusado com **\* Usuario sem acesso a outro orgao \*** e o cursor volta ao
órgão. Passando por essa conferência, a coordenadoria usada dali em diante é a **do
órgão cadastrado**, e não a que o servidor digitou: se o órgão estiver em outra
coordenadoria e o vínculo carregar uma, a recusa é
**\* Usuario sem acesso ao grupo deste orgao \***. Quando o vínculo não carrega nem
órgão nem coordenadoria, é preciso informar um dos dois: com o órgão **e** a
coordenadoria em branco, a recusa é **\* Informe o orgao \***.

[?] Quando o vínculo tem coordenadoria mas **não** tem órgão filho, a coordenadoria
digitada não é comparada com a da sessão: as conferências que impõem a coordenadoria
do órgão e a comparam com a da sessão só são percorridas se o órgão for informado, e o
caminho que confere o pedido aceita o órgão em branco. Assim, com o órgão em branco, um
servidor do grupo 1 pode informar o grupo 2 e excluir o pedido do grupo 2. Ou a sessão
sempre traz o órgão filho — e o caminho não acontece no site —, ou a recusa de grupo
não vale nesse caso. Pergunta ao site; não escolho um dos dois lados.

### RN-05 — O órgão informado tem de existir, estar completo e ser da secretaria

O órgão tem de estar cadastrado e não estar excluído: senão
**\* Orgao nao cadastrado \***. O cadastro tem de estar completo — bairro, órgão pai,
nome, endereço, número de matrículas e número de pessoas —, senão
**\* Orgao cadastrado com dados incompletos \***. E o tipo de órgão tem de ser o da
sessão, senão **\* Orgao nao pertence a esta secretaria \***. Nas três recusas o
cursor volta ao campo do órgão e nada é apagado. Quando o vínculo tem coordenadoria e
o órgão é deixado em branco, nenhuma dessas três conferências é feita: a tela segue
direto para a conferência do pedido.

[?] Há uma recusa que compara o nome do órgão com o texto "NAO CADASTRADO", mas esta
tela nunca escreve esse texto no campo: ele só recebe o nome do órgão cadastrado ou
fica vazio. Ou a recusa vale para um caso que já não acontece nesta tela, ou ela
depende de um caminho que não está no fonte. Pergunta ao site.

### RN-06 — O pedido é procurado pela coordenadoria, pelo número e pelo ano da entrega

O número do pedido (6 dígitos) e o ano da entrega (4 dígitos) formam juntos o número de
**10 dígitos** que identifica o pedido. A tela exige ao menos um dos dois: com os dois
zerados, a recusa é **\* Informe o numero do pedido \***, com o cursor no número. A
procura é feita pela secretaria da sessão, pela coordenadoria e por esse número de 10
dígitos; não achando, a recusa é **\* Pedido nao cadastrado \***. O órgão informado
**não** faz parte da identificação do pedido: ele serve para chegar à coordenadoria e
para as conferências de acesso — o pedido pertence à coordenadoria, e não ao órgão.

[?] O ano da entrega sozinho já faz a tela procurar o pedido (e responder "não
cadastrado"); a recusa de campo em branco só aparece com o número **e** o ano zerados.
Se o site espera a mensagem sempre que faltar o número, é pergunta ao site.

### RN-07 — Os campos numéricos passam por edição numérica antes das conferências

Antes de qualquer conferência sobre o pedido, os **11 campos numéricos** — órgão
filho, coordenadoria, número do pedido, ano da entrega, código do fornecedor, dia, mês
e ano do início do período e dia, mês e ano do limite — passam por edição numérica, e o
campo em branco é tratado como zero. A operação, o código da próxima tela, o cartão e a
resposta da confirmação **não** passam por essa edição.

[?] O que o servidor vê quando digita algo que não é número não se conclui desta tela:
a rotina que faz a edição não está no acervo. E a tela só sabe devolver o cursor ao
órgão, ao número do pedido e ao ano da entrega; um erro de digitação na coordenadoria,
no fornecedor ou em qualquer uma das seis datas não tem posição de cursor definida.
Pergunta ao site.

### RN-08 — Só um pedido fechado, não acumulado, com gêneros e totalmente estornado pode ser excluído

O pedido tem de estar **fechado** (senão **\* Pedido nao esta fechado \***), não pode
ser um pedido **acumulado** (senão **\* Pedido acumulado \***), tem de ter pelo menos
um gênero (senão **\* Pedido sem generos cadastrados \***), nenhum dos seus gêneros
pode ser de pedido acumulado (senão
**\* Pedido com genero de pedido acumulado \***) e a quantidade destinada de cada
gênero tem de ser igual à quantidade pedida (senão
**\* Pedido nao esta totalmente estornado \***). Os gêneros já excluídos não entram
nessas conferências. Em todas as recusas o cursor fica no número do pedido e nada é
apagado.

### RN-09 — A exclusão é confirmada antes de acontecer

Passando por todas as conferências, a tela ainda não apaga: ela mostra os dados do
pedido — o código e a razão social do fornecedor, o cartão, o período de entrega e a
situação **FECHADO** — e pergunta **\* Confirma exclusao do pedido <S/N> ? \***, com o
cursor na resposta. Só a resposta afirmativa leva à exclusão, e ela só vale para o
pedido que estava na pergunta: se a operação, o órgão ou o pedido tiverem mudado, a
confirmação é descartada. Qualquer resposta que não seja afirmativa descarta a
confirmação pendente e a tela refaz todas as conferências, voltando à mesma pergunta.

[?] A resposta diferente de "S" não devolve o servidor ao começo nem sai da tela: ela
só descarta a pendência, e a tela confere tudo de novo e pergunta outra vez. Se a
intenção era permitir desistir com a resposta negativa, o caminho não faz isso — quem
responde "N" só sai encerrando a tela. Pergunta ao site.

[?] Quando o fornecedor do pedido não está cadastrado, a tela não avisa: a razão social
aparece em branco na confirmação e a exclusão segue assim mesmo. Se existe outro
cadastro de fornecedor que devesse ser consultado, o fonte não o mostra. Pergunta ao
site.

### RN-10 — Confirmada, a exclusão apaga os gêneros, apaga o pedido e registra a auditoria

Confirmada a exclusão, a tela apaga **todos os gêneros** do pedido, um a um, e depois o
**próprio pedido**. De cada registro apagado ela inclui um registro de auditoria com a
operação de exclusão, qual cadastro foi atingido, o número do pedido, a coordenadoria,
a secretaria, a matrícula do servidor, a estação, a data e a hora da sessão e o
conteúdo do registro. No fim, a tela informa **\* Pedido excluido com sucesso \*** e o
campo da situação do pedido, que mostrava FECHADO, passa a mostrar **EXCLUIDO**.

[?] Os dois campos de conteúdo do registro de auditoria (o anterior e o posterior)
recebem a mesma imagem do registro apagado; em telas da mesma família a imagem vai só
no campo anterior, e o posterior fica vazio. O que a auditoria deve guardar da exclusão
é pergunta ao site.

[?] O laço que apaga **não** salta os gêneros já marcados como excluídos, embora a
conferência salte: um gênero já excluído é apagado de novo e ganha uma segunda linha de
auditoria. Se isso é intencional, é pergunta ao site.

[?] A inclusão do registro de auditoria passa por uma conferência de destino que a
própria tela não comanda: o trecho que decidiria gravar neste ambiente ou encaminhar
para outro destino depende de marcas de destino que esta tela não preenche — e ela
apaga a marca de distribuição imediatamente antes de executá-lo, de modo que a inclusão
segue para a gravação local. Se a transação puder rodar com outro destino, o que
acontece com a exclusão nesse caso não se conclui do fonte. Pergunta ao site.

[?] Na passagem que apaga, a tela relê o pedido mas não confere se ele ainda existe: se
ele tiver sido apagado entre a pergunta e a resposta, a auditoria e a exclusão seguem
com o que ficou da leitura anterior. Pergunta ao site.

### RN-11 — Nada é excluído sem a conferência de sessão, de tela, de acesso e de operação

Na abertura, a tela confere que o servidor está na **estação em que a sessão foi
aberta** (em outra, o acesso é encerrado e a sessão volta à entrada), que a tela está
registrada (senão **\* Tela nao disponivel \***), que ela pertence ao módulo da sessão
e que o código de acesso do servidor alcança a tela (senão
**\* Acesso negado para esta matricula \***). Na confirmação, confere a rota e a
operação: a exclusão exige que o código de acesso tenha a **permissão de exclusão**
para esta tela, senão **\* Acesso negado para esta operacao \***. Também é recusada a
requisição da segunda página da tela (**\* Acesso a pagina 2 negado \***). Sem passar
por tudo, nada é apagado e nada é gravado.

[?] A rota da transação é decidida por um campo da própria tela — o código da próxima
tela — que chega preenchido de fora dela: estando preenchido, a transação é
encaminhada para a tela indicada antes de qualquer exclusão. Não se conclui desta tela
quem o preenche, nem se ele pode desviar a transação. Pergunta ao site.

### RN-12 — A recusa e a abertura não apagam nada

Cada recusa encerra a passagem **antes** das exclusões e antes da auditoria, de modo
que uma confirmação recusada não apaga gênero nenhum nem o pedido e não grava
auditoria. A simples abertura da tela também não escreve nem apaga nada.

---

## Cenários BDD

```gherkin
Funcionalidade: Excluir um pedido de alimentação escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a coordenadoria regional escolar e o
      órgão filho do meu vínculo
    E tenho acesso à tela E028T

  Cenário: Excluir um pedido fechado
    Dado que existe um pedido fechado, não acumulado, com gêneros, todos com a
      quantidade destinada igual à quantidade pedida
    E que o pedido é da coordenadoria do meu vínculo
    Quando informo o órgão, a coordenadoria, o número do pedido e o ano da entrega
    E confirmo a exclusão
    Então todos os gêneros do pedido são apagados
    E o pedido é apagado
    E vejo "* Pedido excluido com sucesso *"
    E o campo da situação passa a mostrar EXCLUIDO

  Cenário: A tela só exclui
    Dado que estou na tela E028T
    Quando a transação chega com uma operação que não é a de exclusão
    Então vejo "* Opcao nao disponivel. Use EXC *"
    E o cursor fica no campo da operação
    E nada é apagado

  Cenário: A abertura propõe o órgão e a coordenadoria da sessão
    Dado que o meu vínculo tem órgão filho e coordenadoria
    Quando abro a tela E028T
    Então o campo do órgão vem preenchido com o órgão do meu vínculo
    E o campo da coordenadoria vem preenchido com a coordenadoria do meu vínculo
    E o cursor fica no número do pedido
    E vejo a descrição do órgão da minha sessão e a data do sistema

  Cenário: A abertura sem órgão nem coordenadoria no vínculo
    Dado que o meu vínculo não tem órgão filho nem coordenadoria
    Quando abro a tela E028T
    Então o campo do órgão fica em branco, para eu informar
    E o cursor fica no campo do órgão

  Cenário: A abertura da tela não apaga nem grava nada
    Dado que o meu vínculo tem órgão filho e coordenadoria
    Quando abro a tela E028T
    Então nenhum gênero é apagado, nenhum pedido é apagado e nenhuma auditoria é
      gravada

  Cenário: O servidor não exclui pedido de outro órgão
    Dado que o meu vínculo carrega um órgão filho
    Quando informo outro órgão e confirmo
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor fica no campo do órgão
    E nada é apagado

  Cenário: O servidor não exclui pedido de outro grupo
    Dado que o meu vínculo carrega uma coordenadoria
    Quando informo um órgão cadastrado em outra coordenadoria e confirmo
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor fica no campo do órgão
    E nada é apagado

  Cenário: Sem órgão e sem coordenadoria no vínculo, um dos dois é obrigatório
    Dado que o meu vínculo não tem órgão filho nem coordenadoria
    Quando confirmo sem informar o órgão e sem informar a coordenadoria
    Então vejo "* Informe o orgao *"
    E o cursor fica no campo do órgão
    E nada é apagado

  Cenário: Órgão não cadastrado
    Dado que estou na tela E028T
    Quando informo um órgão que não está cadastrado e confirmo
    Então vejo "* Orgao nao cadastrado *"
    E o cursor fica no campo do órgão
    E nada é apagado

  Cenário: Órgão com cadastro incompleto
    Dado que o órgão informado não tem bairro, órgão pai, nome, endereço, número de
      matrículas ou número de pessoas preenchido
    Quando confirmo
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E o cursor fica no campo do órgão
    E nada é apagado

  Cenário: Órgão de outra secretaria
    Dado que o órgão informado é de um tipo de órgão diferente do da minha sessão
    Quando confirmo
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor fica no campo do órgão
    E nada é apagado

  Cenário: O número do pedido é obrigatório
    Dado que estou na tela E028T
    Quando confirmo com o número do pedido e o ano da entrega zerados
    Então vejo "* Informe o numero do pedido *"
    E o cursor fica no número do pedido
    E nada é apagado

  Cenário: O número do pedido é a junção do número com o ano da entrega
    Dado que estou na tela E028T
    Quando informo apenas o ano da entrega e confirmo
    Então a tela procura o pedido pelo número de 10 dígitos formado pelo número e pelo
      ano
    E não encontrando, vejo "* Pedido nao cadastrado *"

  Cenário: Pedido não cadastrado
    Dado que estou na tela E028T
    Quando informo um pedido que não existe para a coordenadoria e confirmo
    Então vejo "* Pedido nao cadastrado *"
    E o cursor fica no número do pedido
    E nada é apagado

  Cenário: Os campos numéricos são editados antes das conferências
    Dado que estou na tela E028T
    Quando deixo um campo numérico em branco e confirmo
    Então o campo em branco é tratado como zero antes das conferências
    E o que não for número passa pela mesma edição, antes de qualquer conferência do
      pedido

  Cenário: Pedido acumulado
    Dado que o pedido é um pedido acumulado
    Quando confirmo a exclusão
    Então vejo "* Pedido acumulado *"
    E o cursor fica no número do pedido
    E nada é apagado

  Cenário: Pedido não fechado
    Dado que o pedido não está fechado
    Quando confirmo a exclusão
    Então vejo "* Pedido nao esta fechado *"
    E o cursor fica no número do pedido
    E nada é apagado

  Cenário: Pedido sem gêneros
    Dado que o pedido não tem nenhum gênero
    Quando confirmo a exclusão
    Então vejo "* Pedido sem generos cadastrados *"
    E o cursor fica no número do pedido
    E nada é apagado

  Cenário: Gênero de pedido acumulado
    Dado que um dos gêneros do pedido é de pedido acumulado
    Quando confirmo a exclusão
    Então vejo "* Pedido com genero de pedido acumulado *"
    E o cursor fica no número do pedido
    E nada é apagado

  Cenário: Pedido não totalmente estornado
    Dado que um dos gêneros do pedido tem a quantidade destinada diferente da
      quantidade pedida
    Quando confirmo a exclusão
    Então vejo "* Pedido nao esta totalmente estornado *"
    E o cursor fica no número do pedido
    E nada é apagado

  Cenário: A exclusão é pedida com confirmação
    Dado que o pedido passou por todas as conferências
    Quando confirmo a exclusão
    Então vejo os dados do fornecedor, o período de entrega, o cartão e a situação
      FECHADO
    E vejo "* Confirma exclusao do pedido <S/N> ? *"
    E o cursor fica na resposta
    E nada foi apagado ainda

  Cenário: A resposta negativa não exclui
    Dado que a tela me pediu a confirmação da exclusão
    Quando respondo algo diferente de "S"
    Então a exclusão não acontece
    E a tela confere o pedido de novo e volta a pedir a confirmação

  Cenário: A exclusão apaga os gêneros, apaga o pedido e deixa auditoria
    Dado que confirmei a exclusão do pedido
    Quando a exclusão é executada
    Então cada gênero do pedido é apagado, um a um
    E o pedido é apagado
    E cada registro apagado deixa um registro de auditoria com a operação de
      exclusão, o cadastro atingido, o número do pedido, a minha matrícula, a
      estação, a coordenadoria, a secretaria e a data e a hora da sessão
    E nenhum outro cadastro é incluído ou alterado

  Cenário: Nada é apagado sem a conferência de sessão, de tela, de acesso e de operação
    Dado que estou na tela E028T
    Quando a conferência da estação, do registro da tela, do módulo, do código de
      acesso ou da operação não passa
    Então vejo "* Tela nao disponivel *", "* Acesso negado para esta matricula *",
      "* Acesso negado para esta operacao *" ou "* Acesso a pagina 2 negado *"
    E nada é apagado e nada é gravado
    E, se a estação não for a da minha sessão, o acesso é encerrado

  Cenário: A recusa não apaga nada
    Dado que estou na tela E028T e a minha confirmação foi recusada
    Quando a tela termina a passagem
    Então nenhum gênero do pedido foi apagado
    E o pedido continua como estava
    E nenhum registro de auditoria foi incluído
```
