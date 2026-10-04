# US — C116T — Manter as refeições de cada segmento de atendimento

## Estória

Como **servidor de CRE**, quero **declarar quais refeições cada segmento de
atendimento do tipo de órgão da minha secretaria oferece**, para que **a oferta de
alimentação fique registrada segmento a segmento, e não só para o tipo de órgão
inteiro**.

A refeição e o segmento de atendimento são mantidos em outros cadastros, e o que não
existe em lugar nenhum é a **ligação** entre os dois: é essa ligação que esta tela
registra e desfaz. Sem ela, a refeição existe no cadastro do tipo de órgão, mas não
se sabe a que segmento ela atende — e a oferta fica declarada para todos. A tela
serve às duas coisas, declarar a ligação e conferi-la, e é na conferência que nada é
gravado.

## Contexto

Jornada S000M → C000M → C028M → C116T.
Ator: servidor de CRE — declara quais refeições cada segmento de atendimento do tipo
de órgão do seu vínculo oferece.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Esta tela é alcançada por **menu**, e não encadeada de outra: quem a chama não lhe
passa registro nem operação, e por isso ela abre sempre no modo padrão — a consulta.
Ela também **não encadeia** em outra tela: é a última da jornada. O tipo de órgão com
que ela trabalha, e a descrição que abre o cabeçalho, vêm do vínculo do servidor,
carregado na entrada.

As regras abaixo são só as da **tela desta jornada**; as da entrada não se repetem
aqui.

---

## Regras de negócio

### RN-01 — A tela mantém a ligação entre o segmento de atendimento e a refeição

A tela declara quais **refeições** cada **segmento de atendimento** do tipo de órgão
oferece. A ligação não guarda atributo nenhum: ou existe, ou não existe. O cadastro
dos segmentos é mantido na tela C161T e o das refeições, na tela C101T; desta tela
não sai inclusão, alteração nem exclusão de segmento nem de refeição — ela apenas os
lê.

### RN-02 — Tudo o que a tela lê e grava é do tipo de órgão do vínculo do servidor

Os segmentos lidos, as refeições listadas e a ligação gravada pertencem sempre ao
**tipo de órgão do vínculo** do servidor — o mesmo cuja descrição abre o cabeçalho.
Não há campo para escolher outro tipo de órgão: o que for de outro tipo é tratado
como inexistente.

### RN-03 — O segmento e a refeição são códigos de 2 dígitos e passam pela edição numérica

Os dois códigos que a tela recebe — o do **segmento** e o da **refeição** — são
numéricos de **2 dígitos**. O que não for número é recusado pela edição numérica, com
o cursor de volta ao campo, e o que não passa por ela não chega a nenhuma consulta.

### RN-04 — As descrições exibidas vêm do cadastro, não do terminal

A descrição do tipo de órgão, a data do sistema, a descrição do segmento, a descrição
de cada refeição e a indicação legível do vínculo são recarregadas do cadastro e da
sessão a cada exibição: o que o terminal devolver nesses campos é descartado.

### RN-05 — O cabeçalho tem 7 itens e a grade, 13 linhas de 4 itens

O cabeçalho tem **7 itens**: a opção de manutenção, a próxima tela, o código e a
descrição do segmento, o indicador de passagem, a descrição do tipo de órgão e a data
do sistema. Cada uma das **13 linhas** da grade tem **4 itens**: o código da refeição,
a marcação (um caractere), a descrição da refeição e a indicação legível do vínculo.
Contei item a item no leiaute de exibição da tela.

### RN-06 — A tela abre em consulta e retoma a opção da última vez

Aberta sem opção de manutenção escolhida, a tela assume a **consulta**; a opção usada
fica guardada no espaço da própria tela e volta a valer na abertura seguinte. Sem
segmento em foco, ela se posiciona no **primeiro segmento** cadastrado para o tipo de
órgão e mostra o código e a descrição dele. Se o tipo de órgão não tem segmento
nenhum, a grade fica vazia e a tela **não dá aviso próprio**.

### RN-07 — A tela só altera ou consulta

A opção de manutenção aceita apenas **alteração** e **consulta**; incluir e excluir
não se escolhem por aqui. Qualquer outra opção é recusada com
**\* Operacao nao disponivel \***, com o cursor de volta ao campo da opção.

[?] A recusa não diz quais opções valem, e os dois mnemônicos aceitos saem da tabela
da língua instalada do sistema, que não está no acervo: não dá para demonstrar o que
o servidor deve digitar no campo. Pergunta ao site.

### RN-08 — Alterar exige ter consultado antes

Para alterar, o segmento informado tem de ser **o mesmo que a tela já está
mostrando**. Informar outro é recusa: **\* Consulte antes de atualizar \***, com o
cursor de volta ao campo do segmento. Na prática, para mexer em outro segmento é
preciso consultá-lo primeiro.

### RN-09 — Consultar exige um segmento informado e cadastrado

Na consulta o segmento é obrigatório: em branco, a recusa é
**\* Informe o segmento \***. Informado e diferente do que a tela já mostrava, ele é
procurado no cadastro do tipo de órgão: não existindo, a recusa é
**\* Segmento nao cadastrado \***, com o cursor no campo; existindo, a tela passa a
mostrar aquele segmento, com a sua descrição, e reinicia a lista desde a primeira
refeição. Sendo o mesmo que já estava em tela, o cadastro não é relido.

### RN-10 — A lista é a das refeições do tipo de órgão, marcando o que o segmento já tem

A tela percorre as refeições cadastradas para o tipo de órgão, uma por linha, e para
cada uma verifica se ela está ligada ao segmento em foco. Quando está, a linha
aparece com a marcação preenchida e a indicação legível **"Sim"**; quando não está, a
linha aparece sem o vínculo. Não há filtro por segmento: a lista é sempre a do tipo
de órgão inteiro.

### RN-11 — Sem refeição no cadastro do tipo de órgão, a tela avisa e encerra a lista

Quando a leitura das refeições do tipo de órgão não encontra nenhuma, a tela avisa
**\* Segmento sem refeicoes cadastradas \*** e encerra a listagem, na primeira linha.

[?] O aviso fala em **segmento** sem refeições, mas quem o dispara é a falta de
refeições no cadastro do **tipo de órgão**; a falta de vínculo do segmento com uma
refeição não o dispara — a marca que a detectaria é apagada antes do teste. Ou o
aviso anuncia o caso errado, ou o silêncio no caso do vínculo é intencional. Pergunta
ao site.

### RN-12 — O indicador de passagem leva ao segmento seguinte e, nessa passagem, nada é mantido

Com o indicador de passagem preenchido, a tela passa ao **segmento seguinte** ao
informado e, quando não existe seguinte, volta ao **primeiro** segmento do tipo de
órgão, relendo-o do cadastro. Nessa passagem a ligação não é mantida: não se inclui
nem se exclui nada, em nenhuma linha. O programa só lê esse indicador; nunca o
escreve.

[?] O indicador de passagem é comparado em três pontos da tela e nunca é escrito por
ela. Se ninguém o preencher — o terminal ou a lógica global —, a passagem para o
segmento seguinte é inalcançável. Pergunta ao site.

### RN-13 — É a alteração que inclui e exclui a ligação, conforme a marcação da linha

Com a opção de **alteração**, a marcação da linha decide a operação: **"S"** inclui a
ligação entre o segmento em foco e a refeição daquela linha, se ela ainda não
existir; **"N"** exclui a ligação, se ela existir. A tela não duplica o que já existe
nem apaga o que não existe: nesses dois casos não faz nada. Marcação em branco,
marcação diferente de "S" e de "N", e linha sem refeição também não fazem nada — em
silêncio, sem mensagem e sem gravação.

[?] A alteração confere apenas se a ligação já existe; ela **não** confere se o
código de refeição informado está cadastrado para o tipo de órgão — esse cadastro só
é lido na exibição. Ou o terminal só deixa informar refeições que a tela listou, ou é
possível gravar uma ligação para uma refeição que não existe. Pergunta ao site.

### RN-14 — A consulta não grava nada

Na consulta a tela apenas exibe: a passagem que grava, linha a linha, é desviada de
propósito quando a opção não é a alteração. Nenhuma ligação é incluída ou excluída e
nenhum rastro de auditoria é produzido.

### RN-15 — Toda gravação deixa rastro na auditoria

Cada ligação incluída ou excluída monta um registro na trilha de auditoria **A010T**,
com a tela de origem da operação, o cadastro auditado (a ligação entre segmento e
refeição), a operação (**inclusão** ou **exclusão**), o segmento informado como
número de processo e o contexto da sessão — matrícula, estação, CRE, tipo de órgão,
data e hora. Na inclusão o valor anterior vai em branco e o novo é a ligação gravada;
na exclusão o valor anterior é a ligação lida e o novo vai em branco. A auditoria da
exclusão é montada **antes** da exclusão; a da inclusão, **depois** da gravação.

[?] O rastro da inclusão está atrás da condição de o estado da transação não ser
"DATA" — estado que nenhum programa do acervo atribui e que, no ambiente, nasce do
retorno de mensagem externa com conteúdo. Se ele estiver posto quando a inclusão
grava, a inclusão fica sem rastro, enquanto a exclusão sempre tem o seu. Pergunta ao
site.

### RN-16 — Com uma próxima tela no registro, a tela não faz as suas conferências

Quando o registro de entrada traz uma **próxima tela** preenchida, a tela repassa o
controle a ela e não faz nenhuma das suas conferências de cabeçalho — nem a da opção
de manutenção, nem a do "consulte antes de atualizar", nem a do segmento informado. O
programa nunca preenche esse campo: só o exibe e o repassa.

[?] Quem preenche a próxima tela não está no corpus, e o caminho que grava as linhas
não reconfere o que a passagem pulou. Se a combinação for possível — próxima tela
preenchida e marcação em linha —, a linha pode ser gravada sem nenhuma das recusas.
Pergunta ao site.

### RN-17 — Nada é exibido nem gravado sem a autorização da tela e a permissão da operação

Antes de exibir, a tela confere a sessão e o acesso à tela para a matrícula e o
código de acesso do servidor; sem essa conferência ela não exibe nada e encerra.
Antes de manter, confere a rota e a **permissão da operação**: alterar exige a
permissão de alteração liberada, e a consulta não exige permissão de operação. As
recusas são as da rotina de segurança do sistema — entre elas
**\* Acesso negado para esta operacao \*** e **\* Tela nao disponivel \***. Qualquer
resultado diferente do esperado limpa o estado da tela e a encerra: nada é validado,
nada é gravado e nada é auditado.

### RN-18 — A falha do banco interrompe a operação

Todo acesso a dados testa o retorno do banco: o erro de leitura e o de gravação viram
ações de erro despachadas pela rotina de comunicação, e a transação para ali. Não
encontrar registro **não** é erro: é desfecho de conferência, tratado caso a caso.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter as refeições de cada segmento de atendimento

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C116T

  Cenário: RN-01, RN-14 — a ligação entre o segmento e a refeição, e nada mais
    Dado que o tipo de órgão do meu vínculo tem segmentos e refeições cadastrados
    Quando abro a tela C116T
    Então vejo as refeições do tipo de órgão ligadas ao segmento em foco
    E não encontro nenhuma operação que crie ou apague segmento ou refeição
    E nada é gravado

  Cenário: RN-02 — o escopo é o tipo de órgão do meu vínculo
    Dado que entrei com a secretaria em que atuo
    Quando consulto um segmento na tela C116T
    Então só vejo segmentos, refeições e ligações do tipo de órgão daquela secretaria
    E o cabeçalho mostra a descrição desse tipo de órgão
    E não há campo para escolher outro tipo de órgão

  Cenário: RN-03 — código não numérico é recusado
    Dado que estou na tela C116T
    Quando informo um código de segmento ou de refeição que não é número
    Então a tela recusa o código antes de qualquer consulta
    E o cursor volta ao campo

  Cenário: RN-04 — as descrições em tela vêm do cadastro
    Dado que estou na tela C116T com um segmento em foco
    Então a descrição do tipo de órgão, a do segmento e as das refeições são as do cadastro
    E a data exibida é a do sistema
    E o que o terminal devolver nesses campos é descartado

  Cenário: RN-05 — o cabeçalho tem 7 itens e a grade, 13 linhas
    Dado que abro a tela C116T
    Então o cabeçalho traz a opção de manutenção, a próxima tela, o código e a descrição do segmento, o indicador de passagem, a descrição do tipo de órgão e a data do sistema
    E vejo uma grade de 13 linhas
    E cada linha tem o código da refeição, a marcação, a descrição da refeição e a indicação do vínculo

  Cenário: RN-06 — ao abrir, a tela está em consulta no primeiro segmento
    Dado que abro a tela C116T sem escolher a opção de manutenção
    Então a tela está em consulta
    E mostra o primeiro segmento cadastrado para o tipo de órgão, com a sua descrição

  Cenário: RN-06 — a tela retoma a opção da última vez
    Dado que usei a tela C116T com a opção de alteração
    Quando volto a abri-la
    Então ela volta na opção de alteração

  Cenário: RN-06 — tipo de órgão sem segmento cadastrado
    Dado que o tipo de órgão do meu vínculo não tem nenhum segmento cadastrado
    Quando abro a tela C116T
    Então a grade fica vazia
    E nenhum aviso próprio é mostrado

  Cenário: RN-07 — opção de manutenção não disponível
    Dado que estou na tela C116T
    Quando informo uma opção diferente de alteração e de consulta
    Então vejo "* Operacao nao disponivel *"
    E o cursor volta ao campo da opção

  Cenário: RN-08 — alterar um segmento que não foi consultado
    Dado que estou na tela C116T com a opção de alteração
    E informo um segmento diferente do que a tela está mostrando
    Quando confirmo
    Então vejo "* Consulte antes de atualizar *"
    E nada é gravado

  Cenário: RN-09 — consultar sem informar o segmento
    Dado que estou na tela C116T com a opção de consulta
    Quando confirmo com o segmento em branco
    Então vejo "* Informe o segmento *"

  Cenário: RN-09 — consultar um segmento não cadastrado
    Dado que estou na tela C116T com a opção de consulta
    Quando informo um segmento que não está cadastrado para o tipo de órgão
    Então vejo "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento

  Cenário: RN-09 — consultar um segmento cadastrado carrega o segmento
    Dado que estou na tela C116T com a opção de consulta
    Quando informo um segmento cadastrado para o tipo de órgão, diferente do que está em tela
    Então a tela passa a mostrar aquele segmento, com a sua descrição
    E a lista volta a começar na primeira refeição

  Cenário: RN-10 — a lista marca o que o segmento já tem
    Dado que consultei um segmento
    Então vejo as refeições cadastradas para o tipo de órgão, uma por linha
    E as que o segmento já tem aparecem com a marcação preenchida e a indicação "Sim"
    E as demais aparecem sem o vínculo
    E não há filtro por segmento na lista

  Cenário: RN-11 — tipo de órgão sem refeição cadastrada
    Dado que o tipo de órgão do meu vínculo não tem nenhuma refeição cadastrada
    Quando abro a tela C116T
    Então vejo "* Segmento sem refeicoes cadastradas *"
    E a listagem termina na primeira linha

  Cenário: RN-12 — passagem ao segmento seguinte
    Dado que estou na tela C116T com um segmento em foco
    Quando aciono a passagem ao próximo segmento
    Então a tela passa ao segmento seguinte cadastrado
    E, se não houver seguinte, volta ao primeiro
    E nada é gravado nessa passagem

  Cenário: RN-13 — incluir a ligação de uma refeição
    Dado que consultei o segmento e a refeição ainda não está ligada a ele
    Quando marco "S" na linha dessa refeição e confirmo com a opção de alteração
    Então a ligação entre o segmento e a refeição é gravada

  Cenário: RN-13 — excluir a ligação de uma refeição
    Dado que consultei o segmento e a refeição já está ligada a ele
    Quando marco "N" na linha dessa refeição e confirmo com a opção de alteração
    Então a ligação entre o segmento e a refeição é apagada

  Cenário: RN-13 — marcação fora de S e N, ou linha sem refeição, não faz nada
    Dado que consultei o segmento
    Quando deixo a marcação em branco, ou com outra letra, ou deixo a linha sem refeição, e confirmo com a opção de alteração
    Então nenhuma ligação é incluída e nenhuma é apagada
    E nenhuma mensagem é mostrada

  Cenário: RN-13 — não duplica nem apaga o que não existe
    Dado que consultei o segmento
    Quando marco "S" numa refeição que já está ligada, ou "N" numa que não está
    Então nada é gravado

  Cenário: RN-14 — a consulta não grava
    Dado que consultei o segmento com a opção de consulta
    Quando confirmo a tela, mesmo com marcações nas linhas
    Então nenhuma ligação é incluída ou apagada
    E nenhum rastro de auditoria é criado

  Cenário: RN-15 — toda gravação deixa rastro na auditoria
    Dado que incluí a ligação de uma refeição com o segmento consultado
    Então fica registrada a inclusão, com o valor novo da ligação
    E com a minha matrícula, a estação, a CRE, o tipo de órgão, a data e a hora
    E, ao excluir uma ligação, fica registrada a exclusão com o valor anterior

  Cenário: RN-16 — com uma próxima tela no registro, a tela não confere
    Dado que o registro que chega à tela C116T traz uma próxima tela preenchida
    Quando confirmo a tela
    Então ela não faz as conferências de opção, de "consulte antes de atualizar" nem de segmento
    E repassa o controle à tela indicada

  Cenário: RN-17 — sem autorização para a tela
    Dado que o meu código de acesso não tem a tela C116T liberada
    Quando abro a tela C116T
    Então a grade não é exibida
    E recebo a mensagem da rotina de segurança

  Cenário: RN-17 — sem permissão de alteração
    Dado que o meu código de acesso não tem a alteração liberada para a tela C116T
    Quando confirmo uma alteração na tela C116T
    Então vejo "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-18 — falha do banco interrompe a operação
    Dado que estou alterando na tela C116T
    Quando o acesso ao banco falha
    Então a operação é interrompida e a rotina de comunicação assume
    E a linha não é gravada
```
