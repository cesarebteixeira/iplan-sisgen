# US — C275T — Percentual do atendimento por tipo de refeição

## Estória

Como **servidor da CRE**, quero **definir, para cada tipo de refeição do tipo de órgão da
minha secretaria, o percentual que a atualização do cadastro de atendimento deve aplicar**,
para que **os quantitativos de atendimento sejam apurados na proporção certa em cada
refeição, sem ninguém refazer a conta refeição por refeição**.

O percentual é o que converte o atendimento apurado no quantitativo que cabe a cada tipo de
refeição: a atualização do cadastro de atendimento lê o percentual registrado para o tipo de
refeição e o aplica sobre o total apurado — sem percentual registrado, ela toma a refeição
por inteiro. E é também por esta tela que a secretaria pede que a atualização do cadastro
rode, para não depender de alguém lembrar de disparar o processamento depois.

## Contexto

Jornada S000M → C000M → C028M → C275T.

Ator: servidor de CRE — define o percentual de cada tipo de refeição do tipo de órgão da sua
secretaria e decide se manda atualizar o cadastro.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O tipo de órgão, a coordenação regional escolar, a matrícula de quem opera, o código de
acesso e o terminal chegam pela sessão, carregados na entrada a partir do vínculo da
matrícula com a secretaria: a tela não pergunta nada disso. Os tipos de refeição que ela
lista são os que o cadastro de refeições já tem para esse tipo de órgão — a tela não cria
refeição. A opção de manutenção é informada na própria tela: quem a chama não decide por ela
se ela abre em consulta ou em alteração.

A tela **grava**: mantém o percentual de cada tipo de refeição, registra a auditoria de cada
mudança e cria o pedido de atualização do cadastro quando o servidor responde S. Ela **não**
encadeia em outra tela: depois do pedido, ela volta para si mesma.

As regras abaixo são só as da tela desta jornada; as da entrada não se repetem aqui.

---

## Regras de negócio

### RN-01 — A tela mantém um percentual por tipo de refeição do tipo de órgão da sessão

A tela mantém, para cada tipo de refeição, um percentual inteiro de zero a cem, junto com a
matrícula de quem o registrou e a data do registro. O tipo de órgão da sessão e o tipo de
refeição identificam o registro; o tipo de órgão é sempre o da sessão, e a tela não pergunta
de qual secretaria se trata nem deixa manter o percentual de outra.

[?] O cadastro do percentual não está no dicionário da base entregue com o acervo: as chaves
e a capacidade dele não vêm de lá, só do programa. Pelo dicionário não dá para afirmar se um
tipo de refeição poderia ficar com mais de um percentual, nem qual é o limite de registros
desse cadastro. Pergunta ao site.

### RN-02 — A tela abre em consulta e lista os tipos de refeição do tipo de órgão, doze por vez

Ao ser aberta sem opção guardada da passagem anterior, a tela assume a **consulta** e lista
os tipos de refeição do tipo de órgão da sessão, um por linha, com o código, a descrição e o
percentual de cada um — sem percentual quando não há nenhum registrado. A lista da tela
comporta **doze** linhas; o que passar disso não aparece. A tela mostra ainda a descrição do
tipo de órgão, a data do sistema e, no fim da lista, a pergunta **Atualiza Cadastro <S/N>?**
com o campo da resposta ao lado. Quando o tipo de órgão não tem nenhuma refeição, a tela
avisa **\* Nao existem registros cadastrados \*** e termina. Os códigos de refeição e o
percentual passam pela edição numérica: o que não for número é recusado no próprio campo,
antes das conferências de negócio.

[?] A máscara da tela não está no corpus: o programa preenche doze linhas, mas quantas delas
o servidor vê de uma vez, e em que linha cai a pergunta do fim, não se lê do fonte. Pergunta
ao site.

### RN-03 — A refeição de referência posiciona a lista e é reescrita quando a página se completa

A tela tem uma linha própria com o código e a descrição de uma **refeição de referência**. A
refeição informada ali é conferida no cadastro de refeições do tipo de órgão e posiciona a
listagem: sendo uma das que o tipo de órgão tem, a lista recomeça por ela; não sendo, a lista
recomeça pela primeira. Quando a página se completa com as doze linhas, a própria tela
reescreve ali o código e a descrição da última refeição listada.

### RN-04 — A tela só aceita alteração e consulta

A opção informada só pode ser **alteração** ou **consulta**. Qualquer outra é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da opção e nada é
lido nem gravado.

[?] A mensagem nomeia as opções como **ALT** e **CON**, mas a tela confere o que foi digitado
contra os códigos internos de alteração e de consulta do sistema. Nenhum fonte do acervo
mostra quem traduz o que o servidor digita no código conferido; se não houver essa tradução,
a guarda recusa toda opção — inclusive as duas que a própria mensagem pede — e nenhum
percentual é mantido por esta tela. Pergunta ao site.

### RN-05 — O percentual vai de zero a cem

O percentual informado pode ir de **zero a cem**. Acima de cem a recusa é
**\* Percentual maximo invalido \***, com o cursor de volta ao campo do percentual, e nada é
gravado na passagem em que a recusa acontece. O campo deixado em branco conta como zero; o
zero é aceito e tem significado — a refeição fica **sem percentual registrado**, e é ele que
apaga o que estava lá (RN-07).

[?] O texto que o servidor lê nessa coluna não é demonstrável: o nome interno do campo fala
em quantidade de pessoas, a mensagem de recusa o chama de percentual e a atualização do
cadastro o divide por cem para obter a fração. O rótulo da coluna não está no corpus.
Pergunta ao site.

### RN-06 — A consulta não grava nada

Com a consulta escolhida, o processamento termina antes de qualquer decisão de gravação:
nenhum percentual é incluído, trocado ou apagado, nenhum registro de auditoria é escrito e
nenhum pedido de atualização é criado — mesmo que o servidor preencha a resposta do fim da
lista. A consulta ainda pode mostrar a recusa de relatório em processamento (RN-09), mas não
cria pedido nenhum.

### RN-07 — Na alteração, cada tipo de refeição é incluído, trocado, apagado ou deixado como está

Quando a opção é alteração e a resposta do fim da lista **não é S** (o **N** da pergunta; em
branco também não é S e segue o mesmo caminho), a tela percorre a página linha a linha e
cuida do percentual de **cada** refeição informada; o que ela faz depende do que já estava
registrado:

- não havia percentual e o informado não é zero: o percentual é **incluído**;
- havia um percentual diferente do informado e o informado não é zero: o percentual é
  **trocado**;
- havia um percentual registrado e o informado é zero: o registro é **apagado**;
- o informado é igual ao que já estava registrado: **nada é feito**;
- não havia percentual e o informado é zero: **nada é feito**.

Na inclusão, a matrícula de quem operou e a data do dia ficam no registro. A recusa de uma
linha barra a gravação dessa linha e das seguintes, na mesma passagem; o que já foi gravado
antes dela não é desfeito.

[?] Na troca, o registro mantém a matrícula e a data de quem o registrou pela primeira vez:
o sistema reescreve apenas o percentual. O dado é apresentado como data de atualização, mas
numa troca ela não avança — pela tela, a data do registro é sempre a da inclusão. Ou a
intenção é guardar quem cadastrou, ou a data da última mudança está se perdendo. Pergunta ao
site.

[?] A gravação não reconfere contra o cadastro de refeições o código da refeição que ela
grava: procura o percentual por esse código e grava. Só a refeição de referência é conferida
no cadastro. Se o terminal só devolve as linhas listadas, a conferência é desnecessária; se
deixa digitar um código, o percentual pode ser gravado para uma refeição que o tipo de órgão
não tem. A máscara não está no corpus. Pergunta ao site.

### RN-08 — A resposta S pede a atualização do cadastro e não grava os percentuais informados

Quando a resposta é **S**, o sistema cria um **pedido de atualização do cadastro** — o
relatório **C27001** — com o número seguinte ao último pedido já registrado, o tipo de órgão
da sessão, a coordenação regional escolar **1**, a matrícula de quem opera, o terminal, o dia
e o mês — e, na instalação que processa em lote, manda o pedido ao processamento com o código
do relatório, uma cópia, o terminal, a matrícula, o correio eletrônico de quem opera e os
parâmetros da secretaria. A tela avisa **\*\* Cadastro sendo atualizado \*\*** e volta para
si mesma. A resposta só é considerada no fim da lista: nas demais linhas o pedido não é
criado.

**Os percentuais informados nessa passagem não são gravados**: quem os grava é a resposta
diferente de S (RN-07), e a atualização usa o que já estava registrado para cada refeição.

[?] Se o servidor digitar percentuais novos e responder S, a atualização roda com os
percentuais que já estavam registrados e os novos se perdem. O acervo não mostra o servidor
fazendo as duas coisas em duas passagens, nem permite dizer se a intenção era essa. Pergunta
ao site.

[?] O pedido é registrado sempre para a **coordenação regional escolar 1**, e não para a
coordenação de quem opera. O acervo não diz por quê. Pergunta ao site.

[?] O envio ao processamento depende da instalação: numa instalação que não seja a que
processa em lote, pelo texto o pedido fica criado e o servidor vê o aviso de que o cadastro
está sendo atualizado, sem que a atualização rode. O que a instalação vale não está no
corpus. Pergunta ao site.

### RN-09 — Não se pede a atualização com um relatório em processamento

Antes de aceitar a resposta **S**, o sistema confere se já existe um pedido do mesmo relatório
de atualização para o tipo de órgão da sessão e a coordenação 1. Havendo, a recusa é
**\* Relatorio em processamento. Aguarde. \***, com o cursor no campo da resposta, e nada é
pedido nem gravado. A conferência vale só para a resposta **S**: com a resposta diferente de
S os percentuais são registrados mesmo com o relatório em andamento.

### RN-10 — Nada acontece sem a segurança do perfil, da rota e da operação

Antes de conferir os dados, a tela leva a sessão à segurança do perfil e, na passagem de
conferência, à da rota e à da operação (a **alteração**, que é a operação desta tela). Se
qualquer uma não devolver OK, o processamento é abandonado: nada é conferido, nada é gravado
e nenhum pedido é feito. A liberação da alteração é conferida uma vez, na passagem de
conferência, e não se repete na de gravação.

### RN-11 — Toda mudança do percentual deixa rastro na auditoria

Cada inclusão, troca ou exclusão grava um registro de auditoria com o objeto auditado (o
próprio cadastro do percentual por tipo de refeição), a operação, os valores anterior e
posterior e o contexto da sessão: matrícula, coordenação regional escolar, terminal, sessão e
data e hora. O número do processo no rastro é o **código da refeição**. O pedido de
atualização **não** gera registro de auditoria: o próprio pedido é o documento da solicitação.

[?] Na inclusão, o valor anterior que vai para a auditoria é o registro recém-criado e o
posterior fica em branco — o mesmo formato da exclusão, e o inverso do que fazem outras telas
do mesmo sistema. Ou o campo guarda o valor gravado, ou a auditoria da inclusão conta a
história trocada. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Percentual do atendimento por tipo de refeição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C275T

  Cenário: A tela abre em consulta, com as refeições do tipo de órgão
    Dado que o meu tipo de órgão tem refeições no cadastro
    Quando abro a tela
    Então ela abre em consulta
    E vejo cada tipo de refeição com o código, a descrição e o percentual
    E vejo a descrição do meu tipo de órgão e a data do sistema
    E vejo a pergunta "Atualiza Cadastro <S/N>?" no fim da lista

  Cenário: Tipo de órgão sem refeições cadastradas
    Dado que o meu tipo de órgão não tem nenhuma refeição cadastrada
    Quando abro a tela
    Então vejo a mensagem "* Nao existem registros cadastrados *"
    E a tela termina

  Cenário: A refeição de referência posiciona a lista
    Dado que informo na linha de referência uma refeição que o meu tipo de órgão tem
    Quando confirmo
    Então a lista recomeça por essa refeição

  Cenário: A refeição de referência fora do cadastro
    Dado que informo na linha de referência uma refeição que o meu tipo de órgão não tem
    Quando confirmo
    Então a lista recomeça pela primeira refeição do tipo de órgão

  Cenário: A página completa reescreve a refeição de referência
    Dado que o tipo de órgão tem refeições suficientes para completar a página
    Quando abro a tela
    Então a linha de referência mostra o código e a descrição da última refeição listada

  Cenário: Opção de manutenção fora de alteração e consulta
    Quando informo uma opção diferente de alteração e de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é lido nem gravado

  Cenário: Percentual acima de cem
    Quando informo um percentual maior que cem
    Então vejo a mensagem "* Percentual maximo invalido *"
    E o cursor volta ao campo do percentual
    E nada é gravado

  Cenário: A consulta não grava nada
    Dado que a tela está em consulta
    Quando percorro a lista e confirmo
    Então nenhum percentual é incluído, trocado ou apagado
    E nenhum pedido de atualização é criado
    E nenhum registro de auditoria é escrito

  Cenário: Alteração inclui o percentual de uma refeição que não tinha
    Dado que uma das refeições listadas não tem percentual registrado
    Quando informo um percentual de um a cem, respondo N e confirmo
    Então o percentual dessa refeição fica registrado
    E a data do dia e a minha matrícula ficam no registro
    E a operação deixa rastro na auditoria

  Cenário: Alteração troca o percentual de uma refeição
    Dado que uma das refeições listadas já tem um percentual registrado
    Quando informo outro percentual, respondo N e confirmo
    Então o percentual dessa refeição passa a ser o informado
    E a operação deixa rastro na auditoria

  Cenário: Alteração com percentual zero apaga o registro
    Dado que uma das refeições listadas já tem um percentual registrado
    Quando informo zero, respondo N e confirmo
    Então o percentual dessa refeição deixa de existir
    E a operação deixa rastro na auditoria

  Cenário: Alteração com o mesmo percentual não muda nada
    Dado que uma das refeições listadas já tem um percentual registrado
    Quando informo o mesmo percentual, respondo N e confirmo
    Então nada é gravado

  Cenário: Resposta S pede a atualização do cadastro
    Dado que não há atualização em processamento para o meu tipo de órgão
    Quando respondo S no fim da lista e confirmo
    Então o sistema cria um pedido de atualização do cadastro
    E o pedido recebe o número seguinte ao último já registrado
    E vejo a mensagem "** Cadastro sendo atualizado **"
    E a tela volta para si mesma
    E, na instalação que processa em lote, o pedido é enviado ao processamento

  Cenário: Resposta S não grava os percentuais informados
    Dado que uma das refeições listadas já tem um percentual registrado
    Quando informo um percentual diferente, respondo S e confirmo
    Então o pedido de atualização é criado
    E o percentual informado não é gravado
    E a atualização usa o percentual que já estava registrado

  Cenário: Relatório de atualização já em processamento
    Dado que já existe um pedido de atualização em processamento para o meu tipo de órgão
    Quando respondo S no fim da lista e confirmo
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da resposta
    E nada é pedido nem gravado

  Cenário: Operação sem autorização
    Dado que a minha sessão não passa na segurança do perfil, da rota ou da alteração
    Quando tento manter os percentuais
    Então a tela volta sem conferir os dados
    E nada é gravado nem pedido

  Cenário: Toda mudança do percentual deixa rastro na auditoria
    Dado que incluí, troquei ou apaguei o percentual de uma refeição
    Quando a gravação termina
    Então existe um registro de auditoria com o objeto, a operação e os valores anterior e posterior
    E com a matrícula, a coordenação regional escolar, o terminal, a sessão e a data e a hora
    E o número do processo no rastro é o código da refeição
```
