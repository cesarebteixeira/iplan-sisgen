# US — C144T — Manutenção das fontes de recursos da secretaria

## Estória

Como **servidor da secretaria que opera a tela de fontes**, quero **consultar as
fontes de recursos da minha secretaria** — vendo o código, a descrição e o
indicador de prestação de contas do FNDE de cada uma —, para que eu saiba com que
classificação o dinheiro da secretaria está identificado antes de usar esse código
em qualquer despesa.

A fonte de recursos é a classificação que amarra o dinheiro da secretaria: outros
cadastros do sistema apontam para o código da fonte, e um código errado contamina
tudo o que o usa. Por isso a consulta precisa ser fiel e **somente leitura** —
passar pela tela para conferir o cadastro não pode alterá-lo. Pelo caminho desta
jornada o sistema abre a tela em consulta e não deixa incluir nem alterar; a
inclusão e a alteração existem desenhadas no programa, mas o caminho não as
alcança, e o próprio sistema declara a operação indisponível em vez de gravá-la.

## Contexto

Jornada S000M → C000M → C020M → C144T.

Ator: servidor da secretaria — consulta as fontes de recursos do seu órgão e, se a
operação estivesse disponível, as incluiria e alteraria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A tela de destino é alcançada por um menu: quem chega escolhe a opção na tela
anterior e cai aqui. Não é tela encadeada — ninguém lhe passa registro nem
operação —, e é dentro dos próprios campos da `C144T` que se informa o que fazer e
sobre qual fonte. Da tela anterior ela guarda apenas a identificação de origem, que
alimenta as conferências de perfil, de rota e de permissão e vai registrada na
auditoria.

A sessão carrega a secretaria (o órgão), a matrícula, a CRE, o acesso e o
privilégio de quem entrou; é o órgão da sessão que decide quais fontes a tela
enxerga, e esses dados também identificam quem registra na auditoria.

As duas telas do meio do caminho são menus: não deixam nada de próprio para a tela
de destino além do contexto de sessão que a entrada já havia deixado. O que a tela
anterior faz com o próprio menu — inclusive o bloqueio de uma das suas opções — não
é regra desta estória; o lastro disso vai no anexo.

A tela não encadeia para nenhuma outra: não passa registro nem operação adiante, e
a jornada termina nela.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela consulta e mantém as fontes de recursos da secretaria

A tela opera o cadastro de **fontes de recursos**. Cada fonte tem um **código de 7
dígitos** — a chave, junto com o órgão —, uma **descrição de 30 caracteres**, de
preenchimento obrigatório, e um **indicador de prestação de contas do FNDE**, de um
caractere. O mesmo código pode existir em outro órgão; cada secretaria só enxerga e
trata as fontes do seu órgão, e o órgão que vale é o da sessão.

A tela mostra **15 linhas**, e cada linha tem **quatro dados**: o código, a
descrição, o indicador do FNDE e a ação. O cadastro comporta **1.000** fontes —
capacidade declarada é o máximo esperado, parâmetro de dimensionamento, e não o
volume já cadastrado.

### RN-02 — A tela abre em consulta e não deixa incluir nem alterar

O modo de manutenção da tela tem três códigos internos possíveis, mas a tela só
aceita dois: **alteração** e **consulta** — os mesmos que a mensagem de recusa
nomeia como **ALT** e **CON**. Qualquer outro valor é recusado com * Opcao nao
disponivel. Use ALT ou CON *, com o cursor de volta no campo do modo, e nada é
gravado para aquela linha.

Aqui está o ponto que decide a jornada: **quando o campo do modo chega em branco, a
tela o preenche com a consulta**. E é em branco que ele chega, porque na primeira
entrada do programa o formulário é apresentado vazio e não há outro ponto que
preencha esse campo antes da conferência. O único modo que o servidor alcança por
este caminho é, portanto, a consulta: incluir e alterar não ficam disponíveis pela
jornada, e o sistema responde com a recusa de opção indisponível em vez de gravar
errado.

[?] A mensagem manda usar ALT ou CON, mas o teste da tela é feito contra os
**códigos internos** de alteração e de consulta: se o campo recebesse exatamente o
que a mensagem manda digitar, a operação seria recusada. O lote mostra o teste e não
a tradução que a camada de apresentação faria. Pergunta ao site.

[?] O programa tem desenhados os ramos que incluem e alteram, e até um aviso de
fonte já cadastrada, mas todos eles ficam depois da conferência do modo e só rodam
com alteração ou consulta; como o campo do modo nunca chega com o código de
alteração, esses ramos não são alcançáveis por esta jornada. Se a inclusão e a
alteração deveriam estar disponíveis e foram perdidas na montagem da tela, ou se a
tela é de consulta e os ramos são sobra de gerador, o corpus não permite concluir.
Pergunta ao site.

### RN-03 — A consulta é somente leitura

Com o modo em consulta, a passagem que valida cada linha sai antes de qualquer
teste de ação, e a passagem que grava sai antes de qualquer operação. Percorrer a
tela, conferir as fontes e confirmar a página **não inclui, não altera e não apaga
nada** — é a garantia de que a consulta não mexe no cadastro.

### RN-04 — A abertura: o cabeçalho da sessão e o aviso quando não há fonte

Ao abrir, a tela mostra no cabeçalho a **descrição do órgão da sessão** e a **data
do sistema**, que vêm da sessão. Em seguida ela tenta ler a fonte que a sessão
tratou por último: se não encontra — porque a sessão ainda não tratou nenhuma, o
que acontece na primeira abertura, ou porque aquela fonte não existe mais no
órgão —, o sistema avisa * Nao existem fontes cadastradas * e deixa o cursor na
coluna do código. O aviso não impede a tela de abrir: ele é a informação de que não
há o que apresentar na primeira linha.

### RN-05 — A tela reabre na fonte da última passagem

O modo usado e o último código lido ficam guardados na área de trabalho da sessão.
Reabrindo a tela, ela volta apontada para a fonte que a última passagem deixou, e
não do começo do cadastro.

### RN-06 — Toda operação exige a descrição

Nas operações de inclusão e de alteração, a descrição da fonte é obrigatória:
chegando em branco, a recusa é * Informe a descricao *, com o cursor de volta na
coluna da descrição, e nada é gravado. É a mesma exigência que o cadastro faz — a
descrição é o único campo da fonte marcado como obrigatório.

### RN-07 — O indicador do FNDE só aceita S ou N

Nas operações de inclusão e de alteração, o indicador de prestação de contas do
FNDE só é aceito com **S** ou **N**. Qualquer outro valor, inclusive em branco, é
recusado com * Informe prest.contas FNDE com S ou N *, com o cursor nessa coluna, e
nada é gravado.

[?] O indicador é de um único caractere e a tela só aceita S ou N; o corpus não diz
o que significa o indicador em branco nem o que ele produz num cadastro já
existente. Pergunta ao site.

### RN-08 — Inclusão recusa fonte já cadastrada

Na operação de inclusão, antes de qualquer conferência de conteúdo, o sistema
procura a fonte pelo código **dentro do órgão da sessão**. Se ela já existe, recusa
com * Fonte ja cadastrada * e devolve o cursor à coluna do código; a fonte
existente não é alterada e nada é gravado.

### RN-09 — Alteração recusa fonte não cadastrada

Na operação de alteração, a fonte tem de existir no órgão da sessão. Não achando
pelo código, a recusa é * Fonte nao cadastrada *, com o cursor de volta na coluna
do código, e nada é gravado.

### RN-10 — Nada é conferido nem gravado sem a segurança de perfil, de rota e de permissão

Antes de validar as linhas e antes de gravar, a tela chama as rotinas globais de
**perfil de acesso**, de **rota do módulo** e de **permissão por operação**. Se
qualquer uma delas devolver resultado diferente de "OK", a tela limpa o status e
sai: a linha não é validada, nada é gravado e nada é auditado. Na passagem de
validação a permissão é conferida de novo, já com a operação que a linha pede
(inclusão ou alteração).

[?] As rotinas de segurança e de rota só aparecem **chamadas** nos programas; a
fonte e a regra efetiva de permissão por perfil e por operação não estão no corpus.
Pergunta ao site.

### RN-11 — Cada gravação deixa também o rastro na auditoria

Quando uma inclusão ou uma alteração passa por todas as conferências, a tela grava
a fonte no órgão da sessão e deixa também um registro de auditoria da operação,
identificando o órgão, a matrícula, a CRE, o terminal, a data e a hora da sessão e o
número do processo, com o valor anterior e o valor posterior do registro. Como o
modo alcançável desta jornada é a consulta, esse rastro não chega a ser produzido
por este caminho; o lastro do que ele conteria está no anexo.

[?] A auditoria é montada com o contexto da sessão e gravada depois da leitura da
fonte; o corpus não mostra o que acontece com a auditoria quando a gravação da
fonte falha por duplicidade. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Fontes de recursos da secretaria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a secretaria, a matrícula, a CRE, o acesso e o privilégio
    E tenho acesso à tela C144T

  Cenário: A tela lista as fontes de recursos da minha secretaria
    Dado que estou na tela C144T
    Quando a página é apresentada
    Então vejo 15 linhas, cada uma com o código, a descrição, o indicador do FNDE e a ação
    E vejo a descrição do meu órgão e a data do sistema no cabeçalho
    E o cadastro comporta até 1.000 fontes
    E só enxergo as fontes do meu órgão

  Cenário: A tela abre em consulta e não deixa incluir nem alterar
    Dado que estou abrindo a tela C144T e o campo do modo chega em branco
    Quando a página é apresentada
    Então a tela assume a consulta
    E incluir e alterar não ficam disponíveis por este caminho

  Cenário: O modo da tela só admite ALT ou CON
    Dado que estou na tela C144T
    Quando informo um modo diferente de alteração e de consulta
    Então vejo "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo do modo
    E nada é gravado

  Cenário: A consulta não grava nada
    Dado que estou na tela C144T em consulta
    Quando percorro e confirmo as linhas da página
    Então nenhuma fonte é incluída, alterada ou apagada
    E a tela volta sem gravar

  Cenário: A abertura avisa quando não há fonte para apresentar
    Dado que estou abrindo a tela C144T pela primeira vez na sessão
    Quando a tela procura a última fonte que a sessão tratou
    Então vejo "* Nao existem fontes cadastradas *"
    E o cursor fica na coluna do código
    E a tela abre mesmo assim

  Cenário: A tela reabre na fonte da última passagem
    Dado que passei pela tela C144T sobre uma fonte
    Quando volto a abrir a tela
    Então ela reabre apontada para a fonte que a última passagem deixou

  Cenário: A operação exige a descrição
    Dado que estou na tela C144T em uma operação de inclusão ou de alteração
    Quando confirmo a linha com a descrição em branco
    Então vejo "* Informe a descricao *"
    E o cursor fica na coluna da descrição
    E nada é gravado

  Cenário: O indicador do FNDE só aceita S ou N
    Dado que estou na tela C144T em uma operação de inclusão ou de alteração
    Quando informo um indicador de prestação de contas diferente de S e de N
    Então vejo "* Informe prest.contas FNDE com S ou N *"
    E o cursor fica nessa coluna
    E nada é gravado

  Cenário: A inclusão recusa fonte já cadastrada
    Dado que estou na tela C144T em uma operação de inclusão
    E que a fonte do código informado já existe no meu órgão
    Quando confirmo a linha
    Então vejo "* Fonte ja cadastrada *"
    E o cursor fica na coluna do código
    E a fonte existente não é alterada

  Cenário: A alteração recusa fonte não cadastrada
    Dado que estou na tela C144T em uma operação de alteração
    Quando confirmo a linha de uma fonte que não existe no meu órgão
    Então vejo "* Fonte nao cadastrada *"
    E o cursor fica na coluna do código
    E nada é gravado

  Cenário: Nada é validado nem gravado sem a segurança de perfil, de rota e de permissão
    Dado que estou na tela C144T
    Quando a conferência de perfil, de rota ou de permissão por operação não retorna OK
    Então a linha não é validada
    E nada é gravado e nada é auditado
```
