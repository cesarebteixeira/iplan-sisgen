# US — C223C — Consulta dos períodos de vínculo do órgão filho

## Estória

Como **servidor de CRE que acompanha os órgãos escolares**, quero **consultar os períodos de
vínculo de um órgão filho com as coordenações regionais — vendo, período a período, a coordenação,
o nome do órgão, se a unidade é creche, se o pedido é acumulado, se o vínculo está vigente, o órgão
final e até quando aquele período valeu — e, dessa consulta, abrir a relação de unidades da
coordenação**, para que **a secretaria consiga dizer a que coordenação cada órgão esteve ligado em
cada período, sem abrir o cadastro e sem depender de quem fez a transferência**.

O vínculo de um órgão com a sua coordenação regional vale por um período: quando o órgão muda de
coordenação, o período antigo termina e um novo começa. Quem confere consumo, estimativa ou
relatório de um mês já fechado precisa saber qual coordenação atendia o órgão naquele período — e
essa resposta não está no cadastro do órgão, que guarda só o vínculo de hoje. Sem esta consulta, o
histórico de um órgão transferido só aparece órgão por órgão, e um número atribuído à coordenação
errada passa despercebido.

## Contexto

Jornada S000M → C000M → C200M → C223C.
Ator: servidor de CRE — consulta o histórico de coordenações de um órgão filho e, daí, abre a
relação de unidades da coordenação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

As duas telas do caminho antes desta são **menus** — o `C000M`, de 9 opções, e o `C200M`, de 12 —,
de modo que nenhuma delas encadeia um registro nesta tela: ela abre pelo menu, sem registro
passado, e a operação com que abre é decidida por ela mesma (RN-04). Da sessão, a tela usa o **tipo
de órgão (a secretaria)**, a **matrícula**, o **código de acesso**, o **privilégio**, a
**coordenação regional da sessão**, o **nome da secretaria** e a **data do sistema** — regras da
entrada, registradas no anexo de evidências.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela consulta os períodos de vínculo do órgão filho

Esta é uma tela de **consulta**. Informado o **órgão filho**, ela mostra os **períodos de vínculo**
daquele órgão, **quatro por tela**, um por linha. Cada linha traz a **coordenação regional
escolar** do período, o **nome do órgão**, se a unidade é **creche**, se o pedido é **acumulado**,
se o **período está vigente**, o **órgão final** e a **data-limite do período**, com a indicação
"Dt.Lim". A data-limite **só aparece nos períodos que têm fim**; o período em curso, que não tem
limite, é mostrado sem ela. Junto vêm o **nome da secretaria** e a **data do sistema**.

[?] A **coordenação regional escolar** é um campo da tela e passa pela conferência de número, mas
não filtra a consulta: o que a linha mostra vem do registro lido, e o campo é reescrito com a
coordenação desse registro. Se ele deveria posicionar a lista em uma coordenação, pergunta ao site.

### RN-02 — A lista só tem os períodos do tipo de órgão do servidor

O **tipo de órgão** vem do vínculo do servidor com a secretaria e é o filtro de tudo o que a tela
lê: só aparecem períodos gravados naquele tipo de órgão, e órgão de outro tipo não é encontrado —
a recusa é a da RN-06. A **coordenação da sessão** não limita a lista: um órgão pode ter períodos
em coordenações que não são a do servidor e todos eles aparecem.

### RN-03 — A tela lembra o último órgão consultado; sem órgão lembrado, abre sem lista

A tela guarda o órgão consultado na área da sessão e o repõe no campo ao reabrir: a lista é montada
a partir do órgão lembrado, mesmo que o campo venha em branco. Na primeira visita da sessão, sem
órgão lembrado, a tela abre **sem lista e sem aviso** — a leitura só começa quando há um órgão.

### RN-04 — A tela só opera em consulta, e a operação é reposta pela própria tela

A operação apresentada é sempre a **consulta**: ao montar a tela, o sistema repõe a consulta no
campo da operação. Se a mensagem chegar com outra operação, a recusa é
**\* Operacao nao disponivel. Use CON \***, com o cursor de volta no campo da operação, e nada é
consultado.

[?] A recusa manda usar CON, mas a comparação é feita com o código interno da consulta; o texto da
máscara não veio no lote, de modo que a correspondência entre o que o operador digita e o que a
tela confere não pôde ser verificada. A mesma dúvida está registrada na tela C213C. Pergunta ao
site.

### RN-05 — Os três códigos informados são conferidos antes de qualquer consulta

O **órgão filho**, a **coordenação regional escolar** e o **órgão final** são tratados como número
**antes** de qualquer leitura: o que estiver em branco vira zero, os zeros à esquerda são
descartados e o que não for número é recusado no próprio campo, e nada é consultado por causa
disso.

[?] A recusa do órgão filho e a do órgão final devolvem o cursor ao campo; para a **coordenação
regional escolar** não há posição de cursor declarada, de modo que o cursor não volta a esse campo.
Pergunta ao site.

### RN-06 — O órgão informado tem de ter período registrado

Informado um órgão **diferente** do que está lembrado na sessão, a tela confere se ele tem período
registrado. Não tendo, a recusa é **\* Orgao sem historico cadastrado \***, com o cursor no campo
do órgão filho, e a lista não é montada. O órgão que já está lembrado não é conferido de novo.

[?] Existe no programa uma segunda mensagem para o mesmo fato — **\* Orgao nao cadastrado \*** —,
exibida na montagem da lista quando o órgão lembrado não tem período. Como o órgão digitado no
campo já é recusado antes, pela primeira mensagem, esse segundo aviso só é alcançado quando o
órgão vem da área da sessão, e não do campo. Ou os dois textos querem dizer coisas diferentes, ou
o caminho do segundo ficou inalcançável pelo campo. Pergunta ao site.

### RN-07 — A consulta não grava nada

A tela lê o cadastro de telas, para o título e a autorização, e o cadastro de períodos do órgão:
**não inclui, não altera e não exclui nada** e não deixa trilha de auditoria. As rotinas de gravar,
de excluir e de travar registro existem no programa, mas nenhum caminho as executa.

### RN-08 — O indicador de consulta abre a relação de unidades da coordenação

Marcado o **indicador de consulta**, a tela não segue com a operação: ela **entrega à relação de
unidades da coordenação** (`C020C`) a **coordenação do primeiro período do órgão** e **nenhum
órgão**, para que a lista se abra em **consulta** sobre as unidades daquele grupo. É a única saída
da tela, e é por ela que a jornada continua. Com o indicador em branco ou marcado com "N", a tela
apenas segue mostrando o histórico; o indicador é reposto em "N" a cada apresentação da tela.

[?] O campo desse indicador é exibido e lido — qualquer valor diferente de branco e de "N" dispara
a passagem —, mas o corpus não traz o rótulo que o servidor vê nem o valor que ele digita. Pergunta
ao site.

[?] A coordenação entregue é a do **primeiro** período do órgão na ordem do cadastro (a de menor
código de coordenação), que não é necessariamente a coordenação vigente: um órgão já transferido
pode ter o período antigo com código menor. E a lista de destino adota a coordenação da sessão
quando o servidor tem uma, de modo que o grupo entregue só é usado por quem não tem coordenação na
sessão. Se a intenção era entregar a coordenação vigente, pergunta ao site.

### RN-09 — A tela não segue quando a tela anterior está por terminar

Quando o controle da tela anterior está preenchido, ou quando a passagem anterior deixou a marca de
erro, a tela não segue com a consulta: devolve o controle e nada é mostrado nem gravado.

[?] A guarda é anterior a qualquer conferência de órgão, não tem mensagem própria e o corpus não
diz o que preenche o controle da tela anterior. A mesma guarda, na mesma forma, está na tela C020C.
Pergunta ao site.

### RN-10 — Nada é lido sem sessão válida, título e autorização de operação

Antes de mostrar ou ler qualquer coisa, a tela passa por três conferências: a **sessão** precisa
ser válida e da mesma estação; o **título** e o código da tela vêm do cadastro de telas; e a
**operação pretendida** precisa estar liberada no cadastro de autorizações do código de acesso do
servidor, que recebe o contexto da sessão — matrícula, código de acesso, privilégio, tipo de órgão
e coordenação. Não passando, nada é lido nem mostrado.

[?] Na conferência de permissão, a operação de consulta cai no ramo que confere a permissão de
**alteração**, e não a de consulta — o cadastro guarda as quatro permissões separadas (consulta,
inclusão, alteração e exclusão). A mesma dúvida está registrada nas telas C020C e C213C. Pergunta
ao site.

### RN-11 — Falha do banco interrompe a consulta e avisa

Toda leitura desta tela testa o erro do banco. Erro de leitura, fora o caso de "não encontrado",
vira a ação de erro de acesso, com a mensagem de erro do sistema, e a consulta para ali, sem
completar a lista.

## Cenários BDD

```gherkin
Funcionalidade: Consulta dos períodos de vínculo do órgão filho com as coordenações regionais

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C223C

  Cenário: Consulta dos períodos do órgão
    Dado que informo o órgão filho
    Quando confirmo a consulta
    Então vejo a coordenação, o nome do órgão, a indicação de creche, a indicação de pedido acumulado, a situação do período, o órgão final e a data-limite de cada período
    E vejo o nome da secretaria e a data do sistema
    E nada foi gravado

  Cenário: A lista traz quatro períodos por tela
    Dado que o órgão tem mais de quatro períodos registrados
    Quando confirmo a consulta
    Então vejo quatro períodos, na ordem do cadastro
    E nada foi gravado

  Cenário: Período em curso aparece sem data-limite
    Dado que o órgão tem um período sem fim
    Quando confirmo a consulta
    Então esse período é mostrado sem a data-limite

  Cenário: Coordenação informada não filtra a lista
    Dado que informo o órgão e uma coordenação qualquer
    Quando confirmo a consulta
    Então vejo os períodos do órgão em todas as coordenações que ele tem

  Cenário: A lista só enxerga o tipo de órgão da minha secretaria
    Dado que o órgão informado só tem períodos em outro tipo de órgão
    Quando confirmo a consulta
    Então vejo a mensagem "* Orgao sem historico cadastrado *"
    E a lista não é montada

  Cenário: Órgão lembrado de uma consulta anterior
    Dado que já consultei um órgão nesta sessão
    Quando reabro a tela sem informar o órgão
    Então o órgão lembrado volta ao campo
    E a lista é montada a partir dele

  Cenário: Primeira visita sem órgão lembrado
    Dado que ainda não consultei nenhum órgão nesta sessão
    Quando abro a tela C223C
    Então a tela abre sem lista e sem aviso

  Cenário: A consulta não grava nada
    Dado que faço uma consulta
    Quando a lista é apresentada
    Então nenhum período é incluído, alterado ou excluído
    E nenhum registro é travado
    E nenhuma linha nova aparece na trilha de auditoria

  Cenário: Operação diferente de consulta
    Dado que a mensagem chega com uma operação que não é a consulta
    Quando a tela processa
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta para o campo da operação
    E nada é consultado

  Cenário: Código não numérico
    Quando informo texto no órgão filho
    Então o campo é recusado antes de qualquer consulta
    E o cursor volta para o campo do órgão filho
    E nada é consultado por causa dele

  Cenário: Órgão sem período registrado
    Dado que informo um órgão que não tem período registrado
    Quando confirmo a consulta
    Então vejo a mensagem "* Orgao sem historico cadastrado *"
    E o cursor volta para o campo do órgão filho
    E a lista não é montada

  Cenário: Indicador de consulta marcado abre a relação de unidades
    Dado que informo o órgão e marco o indicador de consulta
    Quando confirmo
    Então a relação de unidades da coordenação se abre em consulta
    E nenhum órgão é levado para ela

  Cenário: Indicador de consulta em branco não abre nada
    Dado que informo o órgão e deixo o indicador de consulta em branco
    Quando confirmo
    Então a tela apenas segue mostrando o histórico
    E nenhuma outra tela se abre

  Cenário: Controle da tela anterior preenchido
    Dado que o controle da tela anterior está preenchido
    Quando confirmo
    Então a tela não segue com a consulta
    E nada é mostrado nem gravado

  Cenário: Sem autorização para a operação
    Dado que o meu código de acesso não tem a operação liberada para esta tela
    Quando confirmo a consulta
    Então a operação é recusada com a mensagem do sistema
    E nada é lido

  Cenário: Falha do banco durante a consulta
    Dado que a leitura do cadastro falha no banco
    Quando confirmo a consulta
    Então a operação é interrompida com a mensagem de erro do sistema
    E a lista não é completada
```
