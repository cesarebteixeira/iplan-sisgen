# US — C101T — Manter as refeições do tipo de órgão

## Estória

Como **servidor da CRE**, quero **manter as refeições do tipo de órgão da minha
secretaria**, para que **os segmentos de atendimento tenham refeições existentes para
oferecer e as demais telas encontrem o que ler**.

A refeição é a peça mais fina da oferta de alimentação: é sobre as refeições cadastradas no
tipo de órgão que os segmentos de atendimento declaram o que cada um serve, e é delas que
as outras telas do sistema leem a oferta. Cada refeição diz se traz sobremesa, se é a
básica e se exige justificativa. Sem refeição cadastrada no tipo de órgão, nenhum segmento
tem o que oferecer — e a refeição não sai do cadastro enquanto algum segmento a estiver
usando.

## Contexto

Jornada S000M → C000M → C028M → C101T.

Ator: servidor de CRE — cadastra, corrige, retira e confere as refeições do tipo de órgão da
sua secretaria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O tipo de órgão com que a tela trabalha, a identificação do servidor e a sua secretaria
chegam pela sessão, carregados na entrada a partir do vínculo da matrícula. As regras
abaixo são só as da tela desta jornada; as da entrada não se repetem aqui.

A tela é a porta da manutenção das refeições: quem abre o cadastro pelo caminho antigo
chega ao menu e é recusado com "* Acesso deve ser feito pela tela C101T *", sendo
encaminhado para cá. Ela **grava** — inclui, altera e exclui refeições e registra a
auditoria de cada operação — e **não** cria nem apaga segmentos nem os vínculos das
refeições com eles.

---

## Regras de negócio

### RN-01 — A tela trabalha sobre o tipo de órgão da secretaria do usuário, nunca sobre um órgão digitado

A tela não tem campo de órgão: o tipo de órgão que a entrada deixou na sessão é a chave de
tudo o que ela lê e grava, e o cabeçalho apenas mostra a descrição desse tipo de órgão e a
data do sistema. Toda refeição listada, conferida e gravada pertence a esse tipo de órgão, e
o usuário não tem como operar outro.

### RN-02 — A grade tem 15 linhas, e cada linha informa sete dados da refeição

São 15 linhas por vez. Cada linha informa o código da refeição (2 dígitos), a descrição (20
caracteres), a descrição resumida (8), a ação (1) e três indicações de uma letra — tem
sobremesa, é a básica, exige justificativa —, e mostra cada uma dessas indicações também
por extenso, como Sim ou Não. Fora da grade, o cabeçalho traz a opção de manutenção, o
prefixo de tela, a descrição do tipo de órgão e a data do sistema.

### RN-03 — O código da refeição tem de ser numérico

O código digitado na linha passa pela edição numérica antes de qualquer conferência de
negócio: o que não for número é recusado no próprio campo e não chega a ser conferido.

### RN-04 — A tela só trabalha em ALT (alterar) ou CON (consultar); sem opção informada, ela abre em consulta

A opção de manutenção aceita apenas alteração e consulta. Qualquer outra é recusada com
"* Opcao nao disponivel. Use ALT ou CON *". Quando a tela não tem opção guardada da
passagem anterior, ela adota a consulta e recomeça a lista do começo.

[?] A guarda interna compara a opção com os códigos de alteração e de consulta, enquanto a
mensagem manda usar "ALT" e "CON". Ou o terminal traduz o mnemônico antes de enviar, ou a
mensagem está desalinhada da guarda — e, se for o caso, a manutenção inteira fica
inalcançável pelo terminal. Pergunta ao site; não concluo qual dos dois.

### RN-05 — Consultar lista as refeições do tipo de órgão, uma por linha, até 15

Na consulta a tela percorre as refeições cadastradas para o tipo de órgão e mostra uma por
linha, até 15, na ordem do código. Quando o tipo de órgão não tem nenhuma refeição, a tela
avisa "* Nao existem refeicoes cadastradas *".

[?] A lista é retomada a partir do código da última refeição exibida; não dá para concluir,
pela fonte, se a retomada de uma página para a seguinte repete essa refeição ou passa
direto para a próxima. Pergunta ao site.

### RN-06 — A ação é por linha: I inclui, A altera, E exclui; o resto não faz nada

A ação é da linha, não da tela: I inclui, A altera e E exclui, e a tela traduz a letra para
a operação correspondente antes de pedir autorização. Linha sem código de refeição é
ignorada, e ação fora de I, A e E também — silenciosamente, sem mensagem.

### RN-07 — Cada linha executável passa antes pela conferência de acesso do usuário

Antes de tocar no cadastro, a operação pretendida pela linha — incluir, alterar ou excluir —
é conferida contra o perfil de acesso do usuário àquela tela: sem a permissão, a operação
para ali e nada é executado. A própria opção de manutenção passa pela mesma conferência.

### RN-08 — Incluir exige que a refeição não exista no tipo de órgão

Ao incluir, a tela procura primeiro a refeição pelo código no tipo de órgão: existindo,
recusa com "* Refeicao ja cadastrada *" e nada é gravado.

### RN-09 — Incluir e alterar exigem a descrição e a descrição resumida

Para incluir ou alterar, a descrição da refeição e a sua versão resumida têm de vir
preenchidas: em branco, a tela recusa com "* Informe a descricao *" e, na falta da outra,
com "* Informe a descricao resumida *". A exclusão não pede descrição nenhuma.

### RN-10 — Sobremesa, básica e justificativa só aceitam S ou N

As três indicações da linha só aceitam S ou N, tanto na inclusão quanto na alteração.
Qualquer outro valor é recusado no próprio campo, com "* Inf.se refeic.tem sobremesa ou nao
com S ou N *" para a sobremesa, "* Inf. se refeicao basica com S ou N *" para a básica e
"* Inf. se obriga justificativa com S ou N *" para a justificativa.

### RN-11 — Alterar exige que a refeição exista, e troca só os seus dados

Ao alterar, a refeição tem de existir no tipo de órgão: se não existir,
"* Refeicao nao cadastrada *". Existindo, a alteração substitui a descrição, a descrição
resumida, a sobremesa, a básica e a justificativa — o código da refeição e o tipo de órgão
permanecem os que estavam gravados.

### RN-12 — Excluir exige que a refeição exista e que nenhum segmento a use

Ao excluir, a refeição tem de existir; se não existir, "* Refeicao nao cadastrada *".
Existindo, a tela percorre os vínculos das refeições com os segmentos do tipo de órgão e
recusa a exclusão quando algum segmento usa essa refeição —
"* Nao exclua.Refeicao cad. em segmentos *". Sem nenhum uso, a exclusão é executada.

### RN-13 — Consultar não grava nada

Na consulta a tela só lê e exibe: as duas passagens que poderiam gravar são desviadas de
propósito quando a opção não é alteração, e nenhuma gravação é feita.

### RN-14 — A tela grava em dois cadastros e lê outros dois

A tela inclui, altera e exclui somente no cadastro de refeições, e grava também a trilha de
auditoria. Os outros dois cadastros que ela enxerga — o de títulos de tela e o de vínculo
entre refeição e segmento — são apenas lidos. Para cada cadastro que enxerga, o sistema traz
prontas as operações de gravar, apagar e travar; mas trazer pronto não é usar: das operações
que a tela executa, ela grava em dois cadastros.

### RN-15 — Toda gravação deixa rastro na auditoria

Cada inclusão, alteração e exclusão monta um registro na trilha de auditoria com o tipo de
órgão, a matrícula, a estação, a data e a hora, o cadastro de origem, a operação (inclusão,
alteração ou exclusão) e os valores antes e depois — e só então grava a refeição. Na
inclusão os valores anteriores vão em branco; na exclusão, os posteriores.

[?] Na inclusão, a montagem desse rastro está condicionada a um estado do banco de dados que
nenhuma instrução desta tela produz; se esse estado ocorrer justamente na inclusão
bem-sucedida, a inclusão não deixa rastro, ainda que a alteração e a exclusão deixem. O que
esse estado significa não está no acervo. Pergunta ao site.

### RN-16 — A conferência vem toda antes da gravação

A tela percorre as linhas duas vezes: numa primeira passagem só confere e produz as recusas;
é a última passagem que grava. A conferência e a gravação são separadas de propósito.

### RN-17 — Falha no banco interrompe a operação

Todo acesso ao banco testa o erro: o erro de leitura e o de gravação são levados à rotina de
comunicação do sistema, e a transação para ali, sem completar o resto.

### RN-18 — A conferência inteira fica atrás do prefixo de tela

Toda a conferência das linhas — refeição já cadastrada, descrições obrigatórias, indicações
com S ou N, refeição cadastrada para alterar e para excluir, e uso por segmento — está
pendurada em um único campo do cabeçalho, o prefixo de tela: chegando vazio, a tela confere;
chegando preenchido, ela pula a conferência inteira, em silêncio.

[?] A passagem que grava não testa o prefixo, e nada nesta jornada limpa o campo. Não dá
para concluir, pela fonte, se esse caminho é alcançável pelo terminal; se for, incluir,
alterar e excluir passam sem nenhuma das conferências — inclusive a que impede apagar uma
refeição que algum segmento usa. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter as refeições do tipo de órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C101T

  Cenário: RN-01, RN-02, RN-05 e RN-13 — consultar as refeições do tipo de órgão
    Dado que estou na tela C101T com a opção CON
    Quando confirmo a consulta
    Então vejo, no cabeçalho, a descrição do tipo de órgão da minha secretaria e a data do sistema
    E vejo, em cada uma das 15 linhas, o código, a descrição, a descrição resumida, a ação e as três indicações por extenso
    E nada é gravado

  Cenário: RN-04 — sem opção informada a tela abre em consulta
    Dado que abro a tela C101T sem informar a opção de manutenção
    Quando confirmo sem digitar nenhuma linha
    Então a tela se comporta como consulta
    E nada é gravado

  Cenário: RN-04 — opção de manutenção não disponível
    Dado que estou na tela C101T
    Quando informo uma opção de manutenção diferente de ALT e CON
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E nada é gravado

  Cenário: RN-05 — tipo de órgão sem refeições
    Dado que o tipo de órgão da minha secretaria não tem nenhuma refeição
    Quando confirmo a consulta
    Então vejo "* Nao existem refeicoes cadastradas *"

  Cenário: RN-03 — código da refeição não numérico
    Quando preencho o código da refeição em uma linha com letra
    Então a tela recusa o campo antes de qualquer conferência
    E nada é gravado

  Cenário: RN-06 — linha sem código ou com ação desconhecida
    Dado que preencho uma linha sem o código da refeição, ou com uma ação diferente de I, A e E
    Quando confirmo
    Então aquela linha é ignorada
    E nenhuma mensagem é mostrada

  Cenário: RN-07 — acesso negado para a operação da linha
    Dado que o meu perfil de acesso não permite incluir, alterar ou excluir nesta tela
    Quando confirmo a linha com a ação correspondente
    Então a operação não é executada
    E nada é gravado

  Cenário: RN-08, RN-09, RN-10 e RN-14 — incluir uma refeição nova
    Dado que estou na tela C101T com a opção ALT
    E o código da refeição ainda não existe no tipo de órgão
    Quando preencho a linha com a ação I, a descrição, a descrição resumida e as três indicações com S ou N, e confirmo
    Então a refeição fica gravada no tipo de órgão
    E a operação fica registrada na auditoria

  Cenário: RN-08 — incluir uma refeição que já existe
    Dado que a refeição já está cadastrada no tipo de órgão
    Quando preencho a linha com a ação I e confirmo
    Então vejo "* Refeicao ja cadastrada *"
    E nada é gravado

  Cenário: RN-09 — incluir ou alterar sem a descrição
    Quando preencho a linha com a ação I e deixo a descrição em branco
    Então vejo "* Informe a descricao *"
    E nada é gravado

  Cenário: RN-09 — incluir ou alterar sem a descrição resumida
    Quando preencho a descrição e deixo a descrição resumida em branco
    Então vejo "* Informe a descricao resumida *"
    E nada é gravado

  Cenário: RN-10 — indicação de sobremesa que não é S nem N
    Quando preencho a indicação de sobremesa com outra letra
    Então vejo "* Inf.se refeic.tem sobremesa ou nao com S ou N *"
    E nada é gravado

  Cenário: RN-10 — indicação de refeição básica que não é S nem N
    Quando preencho a indicação de refeição básica com outra letra
    Então vejo "* Inf. se refeicao basica com S ou N *"
    E nada é gravado

  Cenário: RN-10 — indicação de justificativa que não é S nem N
    Quando preencho a indicação de justificativa com outra letra
    Então vejo "* Inf. se obriga justificativa com S ou N *"
    E nada é gravado

  Cenário: RN-11 — alterar os dados de uma refeição existente
    Dado que a refeição existe no tipo de órgão
    Quando preencho a linha com a ação A, os novos dados e confirmo
    Então a descrição, a descrição resumida e as três indicações passam a ser as novas
    E o código da refeição e o tipo de órgão não mudam
    E a operação fica registrada na auditoria

  Cenário: RN-11 — alterar uma refeição que não existe
    Quando preencho a linha com a ação A em um código que o tipo de órgão não tem
    Então vejo "* Refeicao nao cadastrada *"
    E nada é gravado

  Cenário: RN-12 — excluir uma refeição que nenhum segmento usa
    Dado que a refeição existe e nenhum segmento do tipo de órgão a usa
    Quando preencho a linha com a ação E e confirmo
    Então a refeição é apagada do tipo de órgão
    E a operação fica registrada na auditoria

  Cenário: RN-12 — excluir uma refeição que um segmento usa
    Dado que um segmento do tipo de órgão usa essa refeição
    Quando preencho a linha com a ação E e confirmo
    Então vejo "* Nao exclua.Refeicao cad. em segmentos *"
    E nada é apagado

  Cenário: RN-12 — excluir uma refeição que não existe
    Quando preencho a linha com a ação E em um código que o tipo de órgão não tem
    Então vejo "* Refeicao nao cadastrada *"
    E nada é apagado

  Cenário: RN-17 — falha no banco durante a gravação
    Dado que a gravação da refeição falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com a mensagem de erro do sistema
    E a refeição não é considerada gravada
```
