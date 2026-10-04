# US — S062T — Autorizações de um nível de acesso nas telas e relatórios

## Estória

Como **servidor de CRE responsável pela segurança do sistema**, quero **definir e
manter, para cada nível de acesso, o que ele pode fazer em cada tela e em cada
relatório**, para que **cada servidor só alcance, com o nível que o seu vínculo
carrega, aquilo que a secretaria liberou**.

O nível de acesso acompanha o vínculo de cada servidor com a secretaria e é o que
abre as telas do sistema. Quem escreve, nível a nível, quais telas e relatórios
aquele nível alcança e o que ele pode fazer em cada um — consultar, incluir,
alterar e excluir — é esta tela. Uma tela nova entra no sistema sem liberação para
ninguém, e é esta tela que a libera; sem ela, a liberação fica como está, e um
nível continua fazendo o que não deveria ou deixa de fazer o que precisa.

## Contexto

Jornada S000M → S001M → S004M → S062T.

Ator: servidor de CRE — escolhe um nível de acesso, um módulo e o tipo, e mantém,
tela a tela, as autorizações daquele nível.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas anteriores da jornada são menus: elas só encaminham e não deixam dado
de negócio para esta tela. O contexto que a `S062T` usa — a matrícula, o nível de
acesso do vínculo, o privilégio, o órgão e a CRE — é o que a entrada deixou na
sessão, e a tela apenas o repassa às rotinas de rota e de segurança.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela mantém, para cada nível de acesso, o que ele pode fazer em cada tela e relatório

O que a tela guarda é, para um nível de acesso, o que ele pode fazer numa tela ou
num relatório: consultar, incluir, alterar e excluir. Existe um registro por
combinação de nível de acesso, tipo — tela ou relatório — e código; não havendo
registro, aquele nível não tem nenhuma autorização naquele código. A tela se apoia
em três cadastros que apenas lê: o de níveis de acesso, o de telas e relatórios
(donde vêm o nome do código e a marca de que a tela aceita atualização) e o de
vínculos da matrícula com a secretaria.

### RN-02 — A tela grava: inclui, altera e exclui autorizações, e registra cada operação

Esta não é uma tela de consulta. Ela inclui, altera e exclui autorizações, e cada
uma dessas operações deixa um registro na auditoria com o cadastro afetado, a
operação, o operador, a CRE, o órgão, o terminal, a data e a hora, e os valores da
autorização antes e depois. Nenhum outro cadastro é alterado por ela: os cadastros
de níveis de acesso, de telas e relatórios e de vínculos são apenas lidos.

[?] Quando uma leitura ou uma gravação não se completa — o registro está travado,
por exemplo —, o texto que o operador vê depende de um tratamento que não está
neste lote. Pergunta ao site.

[?] O registro de auditoria da inclusão é gravado sob uma condição que depende do
resultado da própria gravação, enquanto os da alteração e da exclusão são gravados
sempre; não foi possível confirmar, pelo lote, que essa condição se cumpre em toda
inclusão. Pergunta ao site.

[?] Nos três casos — inclusão, alteração e exclusão — o registro de auditoria é
marcado com o mesmo código de manutenção, e é outro campo que distingue a operação.
O que esse código de manutenção separa não está no lote nem no manual. Pergunta ao
site.

### RN-03 — A tela só opera em consulta ou em alteração

A tela reconhece duas operações: consulta e alteração. Qualquer outra operação
informada é recusada com **\* Opcao nao disponivel. Use ALT ou CON \***, e a
mensagem é interrompida antes de qualquer gravação. Sem nenhuma operação registrada
na área da sessão, a tela abre em consulta.

[?] A máscara da tela não está no lote: não é possível confirmar que o campo de
operação é oferecido ao operador, nem como ele escolhe entre consulta e alteração.
Se o campo não existir na máscara, esta recusa é trecho sem uso. Pergunta ao site.

### RN-04 — A consulta não grava nada

Informando a operação de consulta, a tela só lê e monta a lista: nenhuma
autorização é incluída, alterada ou excluída, e nenhum registro de auditoria é
gravado.

### RN-05 — Para alterar, é preciso ter consultado a mesma combinação antes

A alteração só é aceita se o nível de acesso, o módulo e o tipo informados forem os
mesmos da consulta anterior. Se forem outros, a recusa é
**\* Consulte antes de alterar \***: o sistema não deixa alterar uma combinação que
o operador não consultou.

### RN-06 — O operador identifica o nível, o módulo, o tipo e o código

O operador informa o nível de acesso, o módulo, o tipo — tela ou relatório — e, em
cada linha, o código e a ação pretendida. O módulo de um código é o seu primeiro
caractere: é assim que a tela separa as telas e relatórios de um módulo dos
demais. Linha sem código, ou com ação diferente de incluir, alterar e excluir, é
ignorada — nada é gravado por ela.

[?] Há na tela um campo de próxima tela que encerra a mensagem sem nada fazer. Se
ele é o encadeamento de telas do sistema ou um campo que o operador preenche, não
está no lote. Pergunta ao site.

### RN-07 — O nível de acesso informado tem de estar cadastrado

Na alteração, o nível de acesso informado é procurado no cadastro de níveis. Não
estando lá — ou estando retirado do cadastro — a recusa é
**\* Nivel de acesso nao cadastrado \***.

### RN-08 — O módulo tem de ser um dos sete do sistema

O módulo informado tem de ser um destes sete: **C**, cadastro; **E**, pedidos;
**F**, financeiro; **M**, consumo; **N**, nota fiscal; **P**, pagamento; e **S**,
segurança. Outro valor é recusado com
**\* Informe modulo com C/E/F/M/N/P/S \***.

### RN-09 — O tipo tem de ser tela ou relatório

O tipo informado tem de ser **T**, para tela, ou **R**, para relatório. Outro valor
é recusado com **\* Informe T para Tela ou R para Relatorio \***.

### RN-10 — O operador só alcança níveis abaixo do seu; o próprio nível exige privilégio

A tela compara o nível informado com o maior nível de acesso que o operador tem nos
seus vínculos com as secretarias. Nível acima do dele é sempre recusado; o nível
igual ao maior dele só passa se ele estiver marcado como privilegiado no cadastro
de funcionários; níveis abaixo do maior dele passam sem essa marca. Em qualquer
recusa, a mensagem é **\* Seu nivel de acesso nao permite esta operacao \***.

[?] O maior nível do operador é lido dos vínculos da matrícula com o tipo de órgão
zerado. Se essa leitura alcança todos os vínculos da matrícula — como a entrada faz
para contar as secretarias — o operador fica com o maior nível entre eles; se ela
procura exatamente o tipo de órgão zero, fica com zero e a tela recusa qualquer
nível diferente de zero. Não está no lote o que a leitura faz quando o tipo de
órgão procurado é o zero. Pergunta ao site.

### RN-11 — A operação precisa estar liberada para o próprio operador nesta tela

Para incluir, alterar ou excluir uma autorização, o nível de acesso do operador
precisa ter a operação correspondente liberada nesta própria tela: a inclusão exige
a autorização de inclusão, a alteração a de alteração e a exclusão a de exclusão.
Faltando, a recusa é **\* Acesso negado para esta operacao \***.

### RN-12 — A tela mostra as telas e relatórios do módulo com as autorizações do nível

Montada a consulta, a tela lista as telas e relatórios do módulo e do tipo
informados, com o nome de cada código, e ao lado de cada um as quatro autorizações
que aquele nível tem naquele código. A lista traz **13 linhas** por vez.

[?] A lista parte de um código montado a partir do módulo e varre o cadastro de
telas e relatórios. O que acontece quando o cadastro tem mais códigos do que as 13
linhas — se os demais aparecem numa consulta seguinte e a partir de qual código —
depende da leitura com a chave parcial e do que a tela guarda entre as mensagens, e
isso o lote não documenta. Pergunta ao site.

### RN-13 — Sem tela ou relatório para mostrar, a tela avisa

Se a varredura não encontrar nenhuma tela ou relatório do módulo e do tipo
informados, a tela avisa **\* Nivel de acesso sem registros cadastrados \*** e não
segue.

[?] O aviso fala do nível de acesso, mas quem decide mostrá-lo é a varredura do
cadastro de telas e relatórios, não a do nível. Se o aviso significa "este nível
não tem autorizações" ou "não há tela nem relatório neste módulo", não foi possível
determinar. Pergunta ao site.

### RN-14 — Inclusão: o código não pode existir no nível e exige a autorização de consulta

Para incluir, o código informado não pode ter autorização naquele nível: se já
tiver, a recusa é **\* Codigo ja cadastrado neste nivel de acesso \***. E a inclusão
não é aceita sem a autorização de consulta: sem ela, a recusa é
**\* Informe autorizacoes para o codigo \***.

[?] A inclusão confere a autorização do nível, mas não confere se o código informado
existe no cadastro de telas e relatórios: esse cadastro só é lido para saber se a
tela aceita atualização, e a leitura não barra quando o código não está lá. Se o
operador informar um código que não está no cadastro, a decisão sobre a tela aceitar
atualização passa a depender do que a tela leu antes. Se isso é intencional — deixar
a autorização de um código que ainda vai ser cadastrado — ou descuido, não foi
possível determinar. Pergunta ao site.

### RN-15 — Alteração e exclusão: o código tem de existir no nível

Para alterar ou excluir, o código informado precisa ter autorização naquele nível.
Não tendo, a recusa é **\* Codigo nao cadastrado neste nivel de acesso \***.

### RN-16 — Numa tela marcada como sem opção de atualização só se libera a consulta

Quando o cadastro marca a tela como sem opção de atualização, liberar inclusão,
alteração ou exclusão naquela tela é recusado com
**\* Tela sem opcao de atualizacao \***; se nenhuma dessas três for informada, a
liberação da consulta continua valendo. Num relatório, a tela nem chega a
considerar as três: relatório só tem consulta.

### RN-17 — Liberar uma atualização libera também a consulta

Ao liberar inclusão, alteração ou exclusão, a tela libera junto a consulta. Uma
autorização com alguma liberação de atualização nunca fica sem a consulta.

### RN-18 — Alterar uma linha sem nenhuma autorização apaga a autorização

Se a alteração deixar a linha sem nenhuma das quatro autorizações, a autorização
daquele nível naquele código é apagada, em vez de ficar guardada em branco.

[?] Apagar a linha quando a alteração a deixa sem nenhuma autorização pode ser
proposital — a linha sem consulta não serve para nada — ou um efeito colateral: a
inclusão tem a exigência de informar as autorizações, a alteração não tem. Pergunta
ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Autorizações de um nível de acesso nas telas e relatórios

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S062T

  Cenário: A consulta mostra as telas do módulo e o que o nível pode fazer
    Dado que o nível de acesso 5 está cadastrado
    Quando informo o nível 5, o módulo C e o tipo tela com a operação de consulta
    Então vejo a lista das telas e relatórios do módulo cadastro
    E ao lado de cada código vejo as autorizações de consulta, inclusão, alteração e exclusão que o nível 5 tem
    E nada é gravado

  Cenário: Inclusão de uma autorização para um nível
    Dado que consultei o nível 5 no módulo C e no tipo tela
    E que o código C023T não tem autorização para o nível 5
    Quando informo a operação de alteração com a ação de inclusão para o código C023T
    E libero a consulta e a inclusão
    Então o nível 5 passa a ter autorização no código C023T
    E a consulta fica liberada junto com a inclusão
    E fica registrado na auditoria o que foi incluído

  Cenário: Alteração das autorizações de um código que já existe
    Dado que consultei o nível 5 no módulo C e no tipo tela
    E que o nível 5 já tem autorização no código C023T
    Quando informo a operação de alteração com a ação de alteração para o código C023T
    E libero a alteração
    Então as autorizações do nível 5 naquele código ficam como informei

  Cenário: Exclusão das autorizações de um nível num código
    Dado que consultei o nível 5 no módulo C e no tipo tela
    E que o nível 5 tem autorização no código C023T
    Quando informo a operação de alteração com a ação de exclusão para o código C023T
    Então o nível 5 deixa de ter autorização naquele código

  Cenário: Alterar a linha sem nenhuma autorização apaga a autorização
    Dado que consultei o nível 5 no módulo C e no tipo tela
    E que o nível 5 tem autorização no código C023T
    Quando informo a ação de alteração para o código C023T sem nenhuma autorização
    Então o nível 5 deixa de ter autorização naquele código

  Cenário: Operação não reconhecida
    Quando informo uma operação que a tela não reconhece
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E nenhuma autorização é gravada

  Cenário: A alteração exige a consulta anterior
    Dado que consultei o nível 5 no módulo C e no tipo tela
    Quando informo a operação de alteração para o módulo F, que não consultei
    Então vejo a mensagem "* Consulte antes de alterar *"
    E nenhuma autorização é gravada

  Cenário: Nível de acesso não cadastrado
    Quando informo a operação de alteração com um nível de acesso que não está no cadastro
    Então vejo a mensagem "* Nivel de acesso nao cadastrado *"
    E nenhuma autorização é gravada

  Cenário: Módulo diferente dos sete do sistema
    Quando informo a operação de alteração com um módulo que a tela não reconhece
    Então vejo a mensagem "* Informe modulo com C/E/F/M/N/P/S *"

  Cenário: Tipo diferente de tela ou relatório
    Quando informo a operação de alteração com um tipo que não é tela nem relatório
    Então vejo a mensagem "* Informe T para Tela ou R para Relatorio *"

  Cenário: Nível acima do meu
    Quando informo a operação de alteração com um nível maior que o meu
    Então vejo a mensagem "* Seu nivel de acesso nao permite esta operacao *"
    E nenhuma autorização é gravada

  Cenário: Operação não liberada para mim nesta tela
    Dado que o meu nível de acesso tem a tela S062T sem a autorização de inclusão
    Quando peço a inclusão de uma autorização
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nenhuma autorização é gravada

  Cenário: Inclusão para um código que o nível já tem
    Dado que consultei o nível 5 no módulo C e no tipo tela
    E que o nível 5 já tem autorização no código C023T
    Quando informo a ação de inclusão para o código C023T
    Então vejo a mensagem "* Codigo ja cadastrado neste nivel de acesso *"
    E a autorização existente não é alterada

  Cenário: Inclusão sem nenhuma autorização informada
    Dado que consultei o nível 5 no módulo C e no tipo tela
    E que o nível 5 não tem autorização no código C025T
    Quando informo a ação de inclusão para o código C025T sem nenhuma autorização
    Então vejo a mensagem "* Informe autorizacoes para o codigo *"
    E nenhuma autorização é gravada

  Cenário: Alteração ou exclusão de um código que o nível não tem
    Dado que consultei o nível 5 no módulo C e no tipo tela
    E que o nível 5 não tem autorização no código C025T
    Quando informo a ação de exclusão para o código C025T
    Então vejo a mensagem "* Codigo nao cadastrado neste nivel de acesso *"
    E nada é apagado

  Cenário: Tela sem opção de atualização
    Dado que consultei o nível 5 num módulo e o tipo tela
    E que o cadastro marca aquela tela como sem opção de atualização
    Quando peço a inclusão de uma autorização de alteração nessa tela
    Então vejo a mensagem "* Tela sem opcao de atualizacao *"
    E nenhuma autorização é gravada

  Cenário: Relatório só tem consulta
    Dado que consultei o nível 5 e o tipo relatório
    Quando informo a ação de inclusão para um código de relatório, liberando a consulta
    Então a autorização daquele nível naquele relatório fica só com a consulta
    E as autorizações de inclusão, alteração e exclusão não são consideradas

  Cenário: Linha sem código é ignorada
    Dado que consultei o nível 5 no módulo C e no tipo tela
    Quando informo a ação de inclusão sem dizer o código
    Então nada é gravado para essa linha

  Cenário: Sem tela nem relatório para mostrar
    Dado que consultei um módulo que não tem tela nem relatório cadastrados
    Então vejo a mensagem "* Nivel de acesso sem registros cadastrados *"
```
