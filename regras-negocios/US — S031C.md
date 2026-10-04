# US — S031C — Consulta das telas e relatórios de um módulo do sistema

## Estória

Como **servidor de CRE**, quero **consultar, por módulo e por tipo, quais telas e
relatórios o sistema tem cadastrados**, para que **eu encontre o código e o nome
corretos sem depender de quem decorou, e confira o que cada módulo oferece**.

Todo programa do sistema — cada tela e cada relatório — tem, no cadastro, um código,
um tipo (tela ou relatório) e um nome. É esse mesmo cadastro que a segurança consulta
para decidir se uma matrícula pode abrir uma tela, e que a navegação usa para saber o
que cada programa faz. Esta tela é a leitura desse cadastro: o servidor informa o
módulo e o tipo e vê a lista dos códigos e dos nomes, onze por vez. Sem ela, descobrir
o código certo dependeria de percorrer os menus, e um cadastro com nome errado ou pela
metade só apareceria quando alguém tentasse abrir a tela.

## Contexto

Jornada S000M → S001M → S005M → S031C.

Ator: servidor de CRE — consulta o cadastro de telas e relatórios do sistema, por
módulo e por tipo.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

Os três passos anteriores da jornada são menus: eles só encaminham, não gravam nada e
não deixam dado de negócio novo para esta tela. O contexto que a S031C usa — a
matrícula, o código de acesso, o privilégio, o tipo de órgão e a CRE — é o que a
entrada deixou na sessão; a tela apenas o repassa às conferências de rota e de acesso.

O modo de operação **não** é decidido por quem chamou a tela: a S031C abre sempre em
consulta, qualquer que seja a origem. Não há, nesta tela, comparação com a tela de
origem. E a jornada termina aqui: a S031C não encadeia em outra tela, a não ser pelo
campo de próxima tela (RN-13).

---

## Regras de negócio

### RN-01 — A tela é de consulta e não grava nada

A S031C só lê o cadastro de telas e relatórios. Não inclui, não altera e não exclui
nada, e não deixa registro de auditoria. São **duas leituras de negócio** — a do
próprio registro da tela, que as conferências de acesso e de rota usam, e a que
percorre o cadastro para montar a listagem — e **nenhuma gravação**: as operações de
incluir, alterar e excluir existem escritas no programa para esse cadastro, mas
**nenhum caminho as executa** — declarar não é executar. Quem mantém o cadastro é a
tela de manutenção dele, a S030T, em outra jornada.

A única gravação que esta jornada alcança não é da consulta: é o encerramento da
sessão de quem opera, quando o campo da opção traz a saída do sistema — e nesse
caminho a consulta não acontece (RN-14).

[?] O que o servidor vê quando uma leitura do cadastro falha. A tela marca o erro e
entrega o tratamento à rotina de comunicação do ambiente, que não está no acervo lido:
não se sabe se há aviso, nem qual. Pergunta ao site.

### RN-02 — Ao abrir, a tela põe a consulta na opção e não lista nada

A abertura monta o cabeçalho com a data do sistema e a descrição do tipo de órgão da
sessão, repõe a consulta no campo da operação e **não** lê o cadastro para listar: a
lista sai vazia e sem o aviso de que não há registros. A listagem sai do módulo e do
tipo **correntes**, guardados na área de trabalho da sessão; o que o servidor informa
numa mensagem não é lido para listar na mesma passagem — fica guardado, e é a montagem
seguinte da tela que percorre o cadastro e preenche as linhas. Numa tela recém-aberta
não há módulo nem tipo correntes, e a lista sai vazia.

[?] O acervo não mostra o momento em que o ambiente volta a montar a tela depois de
uma mensagem — é dessa montagem que a lista sai. O que se pode afirmar é que a
passagem que confere a mensagem do servidor não lê o cadastro para listar. Pergunta ao
site.

[?] Nem a descrição do tipo de órgão nem a data do sistema são preenchidas por este
programa: as duas são copiadas de campos da sessão, e o acervo lido só mostra a
entrada montando campos de nome semelhante **em outra área de trabalho** e o ambiente
de execução apagando os dois. Se não vierem do ambiente, os dois campos saem em
branco. Pergunta ao site.

### RN-03 — A única operação aceita é a consulta

Confirmada a tela com qualquer operação que não seja a consulta, depois das
conferências de rota e de acesso e antes de qualquer leitura do cadastro para listar,
a recusa é **\* Operacao nao disponivel. Use CON \*** e o cursor volta ao campo da
operação. A consulta é a única operação que esta tela executa.

Como a abertura repõe a consulta nesse campo, a recusa só é alcançada numa mensagem
seguinte do servidor, se a máscara deixar digitar ali.

[?] O aviso manda usar a consulta pelo nome **CON**, mas a tela confere o campo contra
o código interno de consulta do sistema, e esse texto não é CON. Se o ambiente traduz
o que o servidor digita antes de a tela conferir, o acervo lido não mostra; sem essa
tradução, quem seguir o aviso é recusado de novo. Pergunta ao site.

### RN-04 — O módulo da listagem é a letra inicial do código, entre sete

A lista é de um módulo por vez, e o módulo é a **letra com que o código do programa
começa**: cada tela e cada relatório tem um código de seis posições cuja primeira
letra é o módulo. No acervo, os módulos são **cadastro (C), pedidos (E), financeiro
(F), consumo (M), nota fiscal (N), pagamento (P) e segurança (S)** — os mesmos sete
módulos do menu principal do sistema. Com qualquer outra letra, a recusa é
**\* Informe modulo com C/E/F/M/N/P/S \*** e o cursor volta ao campo do módulo.

[?] O decodificador comum de módulos conhece também as letras de ADMINISTRACAO, de
COBRANCA e de RELATORIO, que esta consulta recusa, e o despacho do sistema tem
transações cadastradas com outras duas letras — a da própria tela de entrada do
sistema e uma segunda. Se essas telas deveriam aparecer nesta consulta, ou se a lista
de sete letras é a definitiva, pergunta ao site.

### RN-05 — O tipo da listagem é tela ou relatório

Além do módulo, a lista é de um tipo por vez: **tela (T)** ou **relatório (R)** — os
dois tipos de registro do cadastro de telas e relatórios. Com qualquer outro valor no
campo do tipo, a recusa é **\* Informe T para tela ou R para relatorio \*** e o cursor
volta ao campo do tipo. A conferência do tipo vem depois da conferência do módulo.

### RN-06 — A lista traz o código e o nome, onze por página

Para o módulo e o tipo pedidos, a lista traz **dois dados por linha**: o código e o
nome do registro. O tipo não aparece na linha, e nem as telas de menu nem a tela
anterior, que o cadastro também guarda, são mostradas. A página tem **onze linhas**: o
cadastro é percorrido em sequência, uma linha por vez, e a página para na décima
primeira.

O cadastro de telas e relatórios tem **sete campos** e capacidade para **2.000**
registros; a chave é o par (tipo, código), sem dois registros com o mesmo par.
Capacidade é o máximo esperado, parâmetro de dimensionamento — não o que está
cadastrado.

### RN-07 — As entradas retiradas do cadastro não aparecem

Uma entrada marcada como excluída **não aparece** na lista: quando a leitura encontra
uma, ela é saltada e a leitura segue para a próxima, dentro do mesmo percurso. A lista
não avisa que saltou.

[?] O dicionário de dados não documenta os valores possíveis do marcador de manutenção
do cadastro; que a letra usada seja a de excluído vem do mapeamento da própria rotina
gerada e da conferência de rota, não do dicionário. Se a letra que a tela trata é
mesmo a de excluído, pergunta ao site.

### RN-08 — A lista para no fim do módulo e no fim do tipo

A leitura não passa para o módulo seguinte nem troca o tipo: ao encontrar um registro
de outro módulo, ou um registro do outro tipo, a listagem **termina ali**, sem aviso,
e a página sai com menos de onze linhas. O mesmo acontece quando o cadastro acaba.

### RN-09 — Sem nada para mostrar, a tela avisa

Se a **primeira** linha da página não tiver o que mostrar — módulo sem registros do
tipo pedido, ou código de início já no fim do módulo —, o aviso é
**\* Nao existem registros cadastrados \*** e nenhuma linha é preenchida. O aviso é
decidido **uma única vez, na primeira linha**: se a lista terminar no meio da página,
as linhas seguintes saem em branco e sem aviso.

### RN-10 — A última linha da página vira o ponto de partida da seguinte

Ao completar as onze linhas, a tela devolve nos campos de início o **código e o nome
da última linha mostrada** — é por esse código que a leitura seguinte começa, e assim
o servidor avança de página em página. Quando a lista termina antes de a página
completar, esses dois campos voltam **vazios**: não há continuação.

[?] Se a leitura seguinte **repete** a última linha mostrada ou começa depois dela, o
acervo não diz: a leitura usa um recurso de posicionamento do dicionário de dados cujo
efeito não está no corpus nem no manual, e a rotina de leitura é importada da
biblioteca de execução, sem fonte no acervo. Com o código da última linha como ponto
de partida, os dois comportamentos são compatíveis com o que o programa mostra.
Pergunta ao site.

### RN-11 — Trocar de módulo ou de tipo recomeça a leitura

Quando o módulo ou o tipo informados são diferentes dos correntes, a tela apaga o
código de início guardado, para a leitura começar no princípio do módulo; sendo os
mesmos, o código de início é mantido e a listagem continua de onde estava.

[?] A limpeza pode não sobreviver à mesma mensagem: ao fechar a página, o código de
início guardado é reposto com o que estiver no campo da tela, que ainda traz o código
da listagem anterior. Se esse campo não for limpo do lado de fora, trocar de módulo
mantém o ponto antigo de leitura, e a lista nova pode sair vazia. Pergunta ao site.

### RN-12 — Antes de listar, o sistema confere a tela, o acesso e a rota

A abertura exige que a tela esteja no cadastro de telas — não estando, a recusa é
**\* Tela nao disponivel \*** — e que o código de acesso de quem opera a tenha
autorizada no cadastro de telas por código de acesso — não tendo, a recusa é
**\* Acesso negado para esta matricula \***. Em toda mensagem, a conferência de rota
exige a tela no cadastro de telas, e tendo ela sido retirada a recusa é
**\* Tela nao cadastrada \***, e a conferência de permissão passa **sem exigir flag
nenhum** quando a operação é a consulta. O contexto da sessão não é recalculado aqui:
é o que a entrada deixou.

[?] A conferência de permissão procura os flags de inclusão, de alteração e de
exclusão, mas **não** o de consulta: com a operação de consulta nenhum flag é
conferido. Se a intenção era exigir o flag de consulta por tela, o caminho não o
exige. Pergunta ao site.

### RN-13 — O campo de próxima tela desvia a transação

A tela leva o seu campo de **próxima tela** para a conferência de rota. Estando
preenchido, a transação é encaminhada para a tela indicada e a S031C encerra sem
listar.

[?] Nenhum programa desta jornada preenche esse campo; quem o preenche, se alguém o
preenche, não está no acervo lido, e o leiaute da máscara também não. Pergunta ao
site.

### RN-14 — A opção de saída do sistema encerra a sessão de quem opera

Se o campo da opção trouxer a **saída do sistema**, o que acontece não é a consulta: a
rotina comum de rota encerra a sessão de quem está operando — com o dia, o mês, o ano
e a hora do momento — e devolve o terminal à entrada. A tela não chega a conferir a
opção nem a listar. É a única gravação que esta jornada alcança, e ela é o fim da
sessão, não da consulta.

[?] A opção de saída é oferecida pelo mesmo campo que a tela repõe como consulta; se a
máscara não deixar digitar ali, o caminho não é alcançável. O texto da máscara não
está no acervo lido. Pergunta ao site.

### RN-15 — A consulta anterior não fica na tela

Antes de conferir a mensagem, a tela apaga o código e o nome mostrados, o nome da
continuação e os dois campos de cabeçalho. Uma consulta recusada, portanto, não deixa
na tela o resultado da consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe
um caminho de entrada em que os campos não são limpos, não foi possível determinar.
Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta das telas e relatórios de um módulo do sistema

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S031C

  Cenário: Consulta das telas de um módulo
    Dado que o cadastro de telas e relatórios tem telas do módulo cadastro
    Quando abro a tela S031C e informo o módulo cadastro e o tipo tela
    Então vejo o código e o nome das telas desse módulo
    E a lista mostra no máximo onze linhas

  Cenário: Consulta dos relatórios de um módulo
    Dado que o cadastro de telas e relatórios tem relatórios do módulo consumo
    Quando informo o módulo consumo e o tipo relatório
    Então vejo o código e o nome dos relatórios desse módulo

  Cenário: A tela abre em consulta e com a lista vazia
    Dado que abro a tela S031C pela primeira vez
    Então não vejo nenhuma linha da lista
    E não vejo o aviso de que não existem registros
    E o campo da opção já traz a consulta
    E vejo a descrição do tipo de órgão da minha sessão e a data do sistema

  Cenário: A tela só consulta
    Dado que o cadastro de telas e relatórios tem telas do módulo cadastro
    Quando informo o módulo cadastro e o tipo tela
    Então a lista é mostrada
    E nenhum registro é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Módulo sem telas nem relatórios do tipo pedido
    Dado que o módulo informado não tem registros do tipo pedido
    Quando envio a tela
    Então vejo a mensagem "* Nao existem registros cadastrados *"
    E nenhuma linha é preenchida

  Cenário: A lista para no fim do módulo
    Dado que o módulo cadastro tem menos de onze telas cadastradas
    Quando informo o módulo cadastro e o tipo tela
    Então a lista termina na última tela do módulo
    E as linhas que sobram ficam em branco, sem aviso
    E nenhuma tela de outro módulo aparece

  Cenário: As entradas retiradas do cadastro não aparecem
    Dado que uma tela do módulo está marcada como excluída no cadastro
    Quando informo esse módulo e o tipo tela
    Então essa tela não aparece na lista
    E a lista segue para a tela seguinte

  Cenário: A última linha da página vira o ponto de partida da seguinte
    Dado que o módulo tem mais de onze telas cadastradas
    Quando informo esse módulo e o tipo tela
    Então os campos de início trazem o código e o nome da décima primeira tela
    E a página seguinte começa por esse código

  Cenário: A lista terminou antes da página
    Dado que o módulo tem menos de onze telas cadastradas
    Quando informo esse módulo e o tipo tela
    Então os campos de início voltam vazios
    E não há página seguinte

  Cenário: Trocar de módulo ou de tipo recomeça a leitura
    Dado que consultei as telas do módulo cadastro
    Quando informo outro módulo e envio a tela
    Então a leitura recomeça no princípio do módulo informado

  Cenário: Opção diferente da consulta
    Dado que estou na tela S031C
    Quando informo uma opção que não é a consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nenhum registro é lido para listar

  Cenário: Módulo fora dos sete
    Dado que estou na tela S031C
    Quando informo um módulo que não é cadastro, pedidos, financeiro, consumo,
      nota fiscal, pagamento nem segurança
    Então vejo a mensagem "* Informe modulo com C/E/F/M/N/P/S *"
    E o cursor volta ao campo do módulo

  Cenário: Tipo que não é tela nem relatório
    Dado que estou na tela S031C
    Quando informo um tipo que não é tela nem relatório
    Então vejo a mensagem "* Informe T para tela ou R para relatorio *"
    E o cursor volta ao campo do tipo

  Cenário: Tela não disponível
    Dado que a tela S031C não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo consultar

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela S031C
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo consultar

  Cenário: Tela retirada do cadastro
    Dado que a tela S031C foi retirada do cadastro de telas
    Quando envio uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"

  Cenário: Próxima tela preenchida
    Dado que a tela chega com uma próxima tela indicada
    Quando envio a tela
    Então a transação é encaminhada para a tela indicada
    E nada é lido para listar

  Cenário: Opção de saída do sistema
    Dado que informo a saída do sistema no campo da opção
    Quando envio a tela
    Então a minha sessão é encerrada, com o dia e a hora do momento
    E o terminal volta à entrada
    E nenhuma linha é listada

  Cenário: O resultado da consulta anterior não fica na tela
    Dado que já consultei um módulo e a lista foi mostrada
    Quando envio uma mensagem que é recusada
    Então o código e o nome mostrados e o nome da continuação não ficam na tela
```
