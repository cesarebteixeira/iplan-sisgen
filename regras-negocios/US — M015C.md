# US — M015C — Consultar o quadro mensal de matriculados e pessoas do órgão filho

## Estória

Como **servidor de CRE**, quero **consultar, órgão por órgão, o quadro mensal de
matriculados e de pessoas das unidades da minha coordenadoria regional**, para que
**eu acompanhe como cada unidade evolui mês a mês e veja em que mês o número
mudou**, e não apenas o total do ano.

Cada unidade tem, para cada mês de referência, quantos matriculados e quantas
pessoas atende; é esse quadro que a coordenação regional acompanha ao longo do ano.
Sem a consulta por órgão e por mês, sobraria o número do cadastro da unidade, e não
daria para saber em que mês a diferença apareceu. A tela é de leitura: ela não
inclui, não altera e não exclui nada.

## Contexto

Jornada S000M → M000M → M020M → M015C.

Ator: servidor de CRE — consulta o quadro mensal de matriculados e de pessoas de um
órgão filho da sua coordenadoria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O M000M e o M020M são menus e não
gravam nada: apenas encaminham, e nada do que eles mostram é aproveitado aqui. O
contexto que a M015C usa — o tipo de órgão e a coordenadoria da sessão — é o que a
entrada deixou. A tela é a mesma para quem a abre: ela não guarda nem compara a tela
de origem, e o modo dela não depende de quem a chamou (RN-01). Ela termina em si: não
abre nenhuma outra tela e não passa registro nem operação adiante. As conferências
que toda tela do sistema repete antes de aceitar a operação — a tela estar
cadastrada, a matrícula tê-la autorizada, a estação bater com a do cadastro, a
segunda página ser negada, a rota e a permissão por operação — valem aqui, mas não
são regra desta tela: ficam no anexo de evidências, em **Regras que se revelaram da
entrada**.

---

## Regras de negócio

### RN-01 — A tela é de consulta: qualquer outra opção é recusada

A tela abre em modo de consulta e repõe esse modo ao montar o quadro, de modo que o
campo da opção volta a ser sempre a consulta. Enviada a tela com o campo da opção
**em branco**, o sistema recusa com **\* Operacao nao disponivel. Use CON \*** e
devolve o cursor ao campo da opção. Enviada com uma opção de manutenção — inclusão,
alteração ou exclusão —, quem recusa é a conferência comum de rota, que toda tela do
sistema executa, com **\* Operacao nao disponivel \***, antes de esta tela olhar o
cadastro de órgãos. Em nenhum dos dois caminhos o cadastro de órgãos nem o quadro
mensal são lidos.

[?] Por que duas mensagens para a mesma recusa. A mensagem da própria tela, que manda
usar **CON**, só é alcançada quando o campo da opção chega em branco: com uma opção de
manutenção, a conferência comum já barrou a passagem antes, com o texto genérico. Se a
intenção era que a tela respondesse "Use CON" a toda opção diferente da consulta, o
caminho não a alcança. Pergunta ao site.

[?] A recusa da própria tela só existe se a máscara oferecer ao servidor o campo da
opção. Como a montagem da tela repõe a consulta sozinha, essa recusa só pode ser
alcançada numa mensagem seguinte do servidor; se a máscara não tem esse campo, o
trecho fica sem uso. O texto da máscara não está no material lido. Pergunta ao site.

### RN-02 — Sem o código do órgão filho a consulta não começa

A tela exige o código do órgão filho. Não informado, o sistema recusa com
**\* Informe o orgao \*** e devolve o cursor ao campo do órgão. A exigência é
conferida antes de qualquer leitura do cadastro de órgãos.

O código do órgão passa antes por edição numérica: o que não for número é recusado no
próprio campo, e o que não passa por essa edição não chega à leitura.

### RN-03 — O órgão filho tem de estar cadastrado

O código informado tem de existir no cadastro de órgãos. Não existindo, a tela recusa
com **\* Orgao nao cadastrado \***, devolve o cursor ao campo do órgão e não mostra
nada. O cadastro de órgãos tem **27 campos** e capacidade para **12.000** órgãos —
capacidade é o máximo esperado, parâmetro de dimensionamento, não o que está
cadastrado.

[?] A tela procura o órgão pelo código do órgão filho sozinho, e a chave dessa leitura
admite mais de um registro com o mesmo código. Se o mesmo código aparecer em mais de
uma coordenadoria, o nome e o grupo comparados são os do registro que a leitura
devolver — e não há nada que diga qual é. Pergunta ao site.

### RN-04 — Só se consulta o órgão do próprio grupo do servidor

O órgão filho só é mostrado se a coordenadoria dele for a mesma do servidor. Sendo de
outra, a tela recusa com **\* Usuario sem acesso ao grupo deste Orgao \***, devolve o
cursor ao campo do órgão e não mostra nada. Servidor sem coordenadoria na sessão
**não** passa por essa conferência: para ele, qualquer órgão cadastrado é consultado.

[?] Por que servidor sem coordenadoria na sessão escapa da conferência de grupo. O
acervo não diz se é intenção — servidor de âmbito geral — ou resíduo do gerador.
Pergunta ao site.

[?] De onde vem a coordenadoria da sessão que esta tela compara. Nenhum programa desta
jornada a preenche: a entrada guarda o vínculo da matrícula em outros campos da sessão,
e quem alimenta a área de trabalho que esta tela lê são telas de manutenção de órgão,
que não estão nesta jornada. Se o alcance da consulta sai do vínculo, o caminho não
está aqui. Pergunta ao site.

### RN-05 — A tela identifica o órgão consultado e mostra se ele é creche

Aprovado o órgão, a tela passa a mostrar o **nome do órgão** (até 40 caracteres) e a
**coordenadoria** que está no cadastro dele, e um indicador de creche que aparece como
**Sim** ou **Nao**.

[?] O indicador de creche nunca aparece como "Sim". A marca que o decide é inicializada
em branco e **nenhum caminho deste programa a liga**; o cadastro de órgãos tem, sim, o
atributo de creche, com S ou N, e esta tela não o lê. A marca é guardada junto com o
estado da tela, de uma mensagem para a outra, e pode chegar preenchida de fora do
programa. Se o atributo deveria vir do cadastro, o caminho não o lê. Pergunta ao site.

### RN-06 — O cabeçalho traz a descrição do tipo de órgão e a data do sistema

Fora do quadro, a tela mostra a **descrição do tipo de órgão** da sessão e a **data do
sistema**.

[?] Nem a descrição do tipo de órgão nem a data do sistema são preenchidas por nenhum
programa do acervo lido: as duas aparecem **480 vezes cada**, sempre como origem de
cópia, e a única outra linha é a inicialização em branco. Se não vierem do ambiente de
execução, os dois campos saem em branco. De onde vêm é pergunta ao site.

### RN-07 — O quadro tem 14 linhas, uma por mês de referência

A lista é um quadro de **14 linhas**. Cada linha tem **3 campos**: o **mês e o ano de
referência**, no formato mês/ano (por exemplo **03/2002**), a **quantidade de
matriculados** e a **quantidade de pessoas** daquele mês. Os números vêm do quadro
mensal do órgão, que guarda matriculados e pessoas por mês, por órgão e por
coordenadoria, e tem **7 campos** e capacidade para **200.000** registros —
capacidade é dimensionamento, não volume. A leitura do quadro é restrita ao **tipo de
órgão da sessão**, ao órgão, à coordenadoria e ao mês e ano de referência. O quadro
para nas 14 linhas; não havendo mais mês para mostrar, as linhas restantes ficam em
branco.

[?] Se a leitura percorre os meses. O critério com que a leitura do quadro procura o
mês é montado **só para a primeira linha** e não é avançado depois; quem poderia
percorrer é a própria leitura, por um recurso de posicionamento do dicionário de dados
cujo efeito não está no acervo nem no manual — a rotina de leitura é importada da
biblioteca de execução e não tem fonte no acervo. Se ela avança, o quadro mostra meses
consecutivos; se ela relê o mesmo mês, a mesma linha aparece nas 14. Os dois
comportamentos são compatíveis com o que o fonte mostra, e o site precisa dizer qual é
o esperado.

[?] As duas quantidades da linha são as mesmas grandezas do cadastro de órgãos? O
cadastro de órgãos também tem uma quantidade de matriculados, descrita como "numero de
matriculados / capacidade", e uma quantidade de pessoas, descrita como "comensais /
refeições servidas", e esta tela não as lê: os números do quadro vêm do registro
mensal. Se os dois pares são a mesma grandeza em momentos diferentes, ou grandezas
diferentes, o acervo não diz. Pergunta ao site.

[?] O rótulo que o servidor lê em cima de cada coluna do quadro e nos campos do mês e
do ano não está no acervo: a ficha da tela registra só os rótulos "ORGAO FILHO SDI" e
"COORD.REG.ESCOLA".

### RN-08 — O mês e o ano de referência: repostos ao trocar de órgão, usados ao repetir

O mês e o ano de referência ficam na tela como campos auxiliares e passam por edição
numérica, com o cursor de volta ao campo quando o que foi digitado não é número. Ao
consultar um órgão **diferente** do anterior, a tela os repõe para **janeiro do ano
corrente** — o ano vem da data do sistema —, ignorando o que o servidor havia
digitado. Ao **repetir** a consulta do mesmo órgão, é o mês e o ano informados que a
leitura leva — e ela só acontece quando o último ano lido for diferente do primeiro
ano mostrado; sendo iguais, a tela encerra sem reler. Não achando registro no mês e no
ano informados, as referências voltam a zero.

[?] Quando, na prática, os dois anos diferem — e portanto quando a repetição relê o
quadro. O acervo não mostra um caso em que isso aconteça, e a hipótese de virada de ano
não está sustentada por nenhuma linha. Pergunta ao site.

[?] Se a leitura do quadro começa no mês informado ou no primeiro mês cadastrado do
órgão: é a mesma raiz da dúvida da RN-07, e o site precisa dizer qual é o esperado.

### RN-09 — Não havendo quadro para o órgão, a tela avisa

Não havendo registro de quadro para o órgão, a tela avisa
**\* Orgao sem registros cadastrados \***, devolve o cursor ao campo do órgão e não
preenche nenhuma linha. O aviso é decidido em dois pontos — na conferência do órgão
informado e na montagem do quadro — e, no quadro, **só na primeira linha**: as outras
13 não o refazem.

[?] O que o servidor vê quando o órgão tem quadro, mas nenhum no mês em que a leitura
começa. O aviso é decidido uma única vez, na primeira linha, e não é recalculado
depois; um quadro que esvazie mais adiante fica em branco sem explicação. Pergunta ao
site.

### RN-10 — A coordenadoria digitada não comanda a consulta

O campo da coordenadoria aceita digitação e passa por edição numérica — o que não for
número é recusado antes de qualquer leitura —, mas **não escolhe nada**: a tela procura
o órgão pelo código do órgão filho e reescreve o campo com a coordenadoria que está no
cadastro do órgão. Quem recorta a consulta é o grupo do órgão, não o que foi digitado.

[?] Quando a coordenadoria digitada é recusada pela edição, esta tela não devolve o
cursor a nenhum campo, ao contrário dos outros três campos que ela valida. Se há
mensagem, ela não está nos fontes desta jornada: a rotina de edição é importada e não
tem fonte no acervo.

[?] Se o campo da coordenadoria deveria servir de filtro — consultar um órgão pela sua
coordenadoria — ou se é apenas um campo de saída que a máscara deixa digitar, é
pergunta ao site.

### RN-11 — A consulta não grava nada e não deixa rastro de auditoria

A tela e as rotinas comuns que ela chama, no caminho da consulta, **só leem**. Nenhum
registro é incluído, alterado ou excluído, e nenhum registro de auditoria é gerado. A
tela faz **16 chamadas de leitura** de cadastro — oito pontos de leitura, cada um com
as duas formas de posicionamento — e **nenhuma de gravação**. As operações de gravação,
de exclusão e de travamento de registro existem declaradas para os três cadastros que
a tela enxerga, mas **não são executadas em nenhum caminho**: declarar não é executar.

### RN-12 — Cada consulta começa com os campos de resultado limpos

Antes de conferir a digitação e de ler o órgão, a tela apaga os **sete** campos de
resultado — a descrição do tipo de órgão, a data do sistema, o nome do órgão, o
indicador de creche, o mês e o ano de referência e as duas quantidades. Uma consulta
recusada, portanto, não deixa na tela o resultado da consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica — o tipo cujo
valor é 4 e cujo significado não está no corpus nem no manual. Se existe um caminho de
entrada em que os campos não são limpos, não foi possível determinar.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar o quadro mensal de matriculados e pessoas do órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M015C

  Cenário: Consulta do quadro do órgão
    Dado que o órgão filho está cadastrado no meu grupo
    E que o órgão tem quadro mensal registrado
    Quando abro a tela M015C e informo o código do órgão filho
    Então vejo as linhas do quadro, cada uma com o mês e o ano de referência,
      a quantidade de matriculados e a quantidade de pessoas

  Cenário: O quadro mostra no máximo 14 meses
    Dado que o órgão tem quadro em mais de 14 meses de referência
    Quando abro a tela M015C e informo o código do órgão filho
    Então o quadro mostra 14 linhas
    E as linhas que sobram ficam em branco

  Cenário: A tela identifica o órgão consultado
    Dado que o órgão filho está cadastrado no meu grupo
    Quando abro a tela M015C e informo o código do órgão filho
    Então vejo o nome do órgão
    E vejo a coordenadoria que está no cadastro dele

  Cenário: O indicador de creche
    Dado que o órgão filho está cadastrado como creche
    Quando abro a tela M015C e informo o código do órgão filho
    Então o indicador de creche mostra "Nao"

  Cenário: O tipo de órgão e a data do sistema no cabeçalho
    Dado que entrei no sistema
    Quando abro a tela M015C
    Então vejo a descrição do tipo de órgão da minha sessão
    E vejo a data do sistema

  Cenário: Opção em branco
    Dado que estou na tela M015C
    Quando envio a tela sem informar a opção
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nenhum órgão é lido nesse caminho

  Cenário: Opção de manutenção
    Dado que estou na tela M015C
    Quando envio a tela com uma opção de inclusão, de alteração ou de exclusão
    Então vejo a mensagem "* Operacao nao disponivel *"
    E nenhum órgão é lido nesse caminho

  Cenário: Sem o código do órgão filho
    Dado que estou na tela M015C
    Quando envio a tela sem informar o código do órgão filho
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor volta ao campo do órgão
    E nenhum órgão é lido nesse caminho

  Cenário: Código do órgão filho que não é número
    Dado que digito no campo do órgão filho algo que não é número
    Quando envio a tela
    Então o sistema recusa a digitação antes de ler qualquer órgão
    E o cursor volta ao campo do órgão

  Cenário: Órgão filho não cadastrado
    Dado que informo um código de órgão filho que não está no cadastro de órgãos
    Quando envio a tela
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo do órgão
    E nenhuma linha do quadro é mostrada

  Cenário: Órgão filho de outro grupo
    Dado que o órgão filho está cadastrado em outra coordenadoria
    Quando informo o código dele
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste Orgao *"
    E o cursor volta ao campo do órgão
    E nenhuma linha do quadro é mostrada

  Cenário: Servidor sem coordenadoria na sessão
    Dado que a minha sessão não tem coordenadoria
    Quando informo o código de um órgão filho cadastrado em qualquer coordenadoria
    Então o quadro do órgão é mostrado

  Cenário: Órgão sem quadro registrado
    Dado que o órgão filho está cadastrado no meu grupo
    E que não há quadro mensal registrado para ele
    Quando informo o código dele
    Então vejo a mensagem "* Orgao sem registros cadastrados *"
    E o cursor volta ao campo do órgão
    E nenhuma linha do quadro é preenchida

  Cenário: A coordenadoria digitada não comanda a consulta
    Dado que informo um código de órgão filho do meu grupo
    E informo uma coordenadoria diferente da dele
    Quando envio a tela
    Então a coordenadoria mostrada é a do cadastro do órgão
    E o quadro mostrado é o do órgão informado

  Cenário: Coordenadoria digitada que não é número
    Dado que digito no campo da coordenadoria algo que não é número
    Quando envio a tela
    Então o sistema recusa a digitação antes de ler qualquer órgão
    E o cursor não volta a nenhum campo

  Cenário: Mês ou ano de referência que não é número
    Dado que digito no mês, ou no ano de referência, algo que não é número
    Quando envio a tela
    Então o sistema recusa a digitação antes de ler qualquer órgão
    E o cursor volta ao campo do mês e do ano

  Cenário: Ao trocar de órgão, o mês e o ano voltam para janeiro do ano corrente
    Dado que consultei o quadro de um órgão
    Quando informo o código de outro órgão, com outro mês e outro ano
    Então o mês e o ano de referência mostrados são janeiro do ano corrente

  Cenário: Ao repetir a consulta do mesmo órgão, o mês e o ano informados valem
    Dado que consultei o quadro de um órgão
    Quando envio de novo o mesmo órgão, com outro mês e outro ano
    Então o quadro é lido a partir do mês e do ano que informei

  Cenário: A consulta não grava nada
    Dado que o quadro do órgão é mostrado
    Quando a lista é apresentada
    Então nenhum órgão e nenhum registro de quadro é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: O resultado da consulta anterior não fica na tela
    Dado que já abri a tela e ela mostrou um quadro
    Quando volto a enviar a tela
    Então o nome do órgão, a coordenadoria, o indicador de creche, o mês e o ano
      e as quantidades da consulta anterior não ficam na tela
```
