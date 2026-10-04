# US — M010C — Consultar a situação do mapa mensal dos órgãos filhos da coordenadoria

## Estória

Como **servidor de CRE**, quero **consultar, para um mês e um ano de referência, a
situação do mapa de cada órgão filho da minha coordenadoria regional**, para que
**eu veja de uma vez quais unidades já têm o mapa daquele mês aberto, quais já o
fecharam e quais ainda não o registraram**.

O mapa do mês de referência é o registro da unidade para aquele mês, e o estado
dele — **aberto**, **fechado** ou **ainda não digitado** — é o que diz à
coordenação o que já está registrado no mês e o que falta registrar. Sem esta
lista, sobraria abrir unidade por unidade para descobrir isso, e a conferência do
mês não teria por onde começar. A tela é de leitura: ela mostra a lista e a
situação, e não inclui, não altera e não exclui mapa nenhum.

## Contexto

Jornada S000M → M000M → M020M → M010C.

Ator: servidor de CRE — acompanha, para um mês e um ano de referência, a situação
do mapa dos órgãos filhos da sua coordenadoria regional.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O M000M e o M020M são menus e não
gravam nada: apenas encaminham, e nada do que eles mostram é aproveitado aqui. O
contexto que a M010C usa — o tipo de órgão e a coordenadoria do servidor — é o que a
entrada deixou na sessão. A tela termina em si: não abre nenhuma outra, e o modo
dela não depende de quem a abriu (RN-01). As conferências de tela, de estação, de
rota e de permissão que a M010C executa antes de aceitar a operação são as mesmas de
todas as telas e já estão no documento da entrada: ficam no anexo de evidências, em
**Regras que se revelaram da entrada**.

---

## Regras de negócio

### RN-01 — A tela é de consulta: qualquer outra operação é recusada

A tela abre em modo de consulta e repõe esse modo ao montar a lista, de modo que a
opção da tela volta a ser sempre a consulta. Se o servidor enviar outra operação, o
sistema recusa com **\* Operacao nao disponivel. Use CON \*** e devolve o cursor ao
campo da opção. A recusa vem depois da conferência numérica dos campos digitados e
**antes de qualquer leitura da lista**: nenhum órgão e nenhum mapa é lido nesse
caminho.

A tela é a mesma para quem a abre: ela não guarda nem compara a tela de origem e não
recebe dela nenhum modo de operação — o modo é sempre a consulta. E ela não
encaminha nada adiante: é aqui que a jornada termina.

[?] A recusa só existe se a máscara oferecer ao servidor o campo da opção. Como a
montagem da tela repõe a consulta sozinha, essa recusa só pode ser alcançada numa
mensagem seguinte do servidor; se a máscara não tem esse campo, a recusa é trecho
sem uso. O texto da máscara não está no material lido. Pergunta ao site.

[?] A mensagem manda usar **CON**, e o valor que a tela aceita como consulta é o
código de consulta do sistema. O que a máscara mostra nesse campo não está no
material lido.

[?] O que acontece depois de qualquer uma das recusas desta tela. A expansão do
programa descartou a instrução que encerra a passagem de recusa — o descarte é da
premissa de perfil do expansor, não do acervo — e o programa que li segue adiante
em vez de sair. Se o perfil de compilação real mantém essa instrução, a recusa
encerra como as outras telas do sistema. Pergunta ao site.

### RN-02 — A consulta é sempre do grupo do próprio servidor

O campo da coordenadoria regional abre preenchido com o grupo do servidor e não
aceita outro: informado um grupo diferente do da sessão, o sistema recusa com
**\* Usuario sem acesso a outro grupo \***, devolve o cursor ao campo do grupo e
não lê nada. Quem determina o alcance da consulta é o vínculo do servidor, não o
que ele digita.

[?] A sessão sem grupo é o único caso em que o campo aceita um grupo digitado
(RN-03). O acervo não diz se isso é intenção — um servidor de âmbito geral — ou
resíduo do gerador. Pergunta ao site.

### RN-03 — Quem não tem grupo na sessão informa o grupo, e ele tem de ser da secretaria

Chegando a sessão sem grupo, é o servidor que informa a coordenadoria regional, e
o sistema confere que aquele grupo pertence à secretaria do seu tipo de órgão. Não
pertencendo, recusa com **\* Grupo nao pertence a esta secretaria \***, devolve o
cursor ao campo do grupo e não lê nada. Sem grupo informado, a recusa é
**\* Informe o Grupo para a consulta \***, também com o cursor no campo do grupo.

[?] A conferência de que o grupo pertence à secretaria só roda nesse caminho. Para
quem tem grupo na sessão, a conferência da RN-02 obriga o grupo da própria sessão
a passar, e a conferência de secretaria nunca é alcançada; o cadastro de grupos é
lido em nenhum outro ponto desta tela. Se a intenção era conferir também o grupo
da sessão, o caminho não o faz. Pergunta ao site.

[?] O cadastro de grupos é lido para conferir a secretaria e a descrição do grupo
vem junto no mesmo registro, mas a tela não mostra essa descrição em lugar nenhum.
Se o nome do grupo deveria aparecer para o servidor, o caminho não o leva à tela.

### RN-04 — O mês e o ano de referência são informados os dois, ou valem os correntes

O mês e o ano de referência andam juntos: informado um só — o outro em branco —, o
sistema recusa com **\* Informe Mes/Ano para a consulta \*** e devolve o cursor ao
campo do mês, sem ler nada. Informados os dois, o par passa a valer e a lista
recomeça do primeiro órgão do grupo. Quando ainda não há par em vigor — a primeira
abertura da tela —, a tela usa o **mês e o ano correntes**, não janeiro.

[?] A recusa vale para os dois campos em conjunto, mas a mensagem e o cursor falam
só do mês: falta só o ano, e o cursor volta ao mês. Se é esse o desenho, ou se cada
campo deveria ter a sua recusa, pergunta ao site.

### RN-05 — Trocar de grupo descarta o mês e o ano informados

Na mensagem em que um grupo novo é aceito — o que só acontece para quem não tem
grupo na sessão (RN-03) —, o mês e o ano que vieram com ela **não são
aproveitados**: a tela volta a mostrar o par em vigor e a lista recomeça do
primeiro órgão do grupo. Não há mensagem: o que foi digitado simplesmente não vale
naquela passagem.

[?] Não há, no fonte, nenhum aviso de que o mês e o ano informados foram
descartados; o servidor só percebe porque a tela volta com o par anterior. Se é
intenção, ou se o grupo e o par deveriam valer na mesma passagem, pergunta ao site.

### RN-06 — A lista traz os órgãos filhos do grupo, 13 por vez

A lista é uma grade de **13 linhas**. Cada linha traz o **código e o nome do órgão
filho**, o indicador de **creche** (aparece como **Sim** ou **Nao**) e a **situação
do mapa** daquele órgão no mês e no ano de referência. As linhas vêm do cadastro de
órgãos, restritas ao tipo de órgão da sessão e ao grupo da consulta, na ordem do
cadastro; o cadastro de órgãos tem **27 campos** e capacidade para **12.000**
órgãos — capacidade é o máximo esperado, parâmetro de dimensionamento, não o que
está cadastrado. A grade para na 13ª linha: não havendo mais órgão para mostrar, a
listagem termina.

[?] Se a leitura percorre os órgãos. O critério de leitura é remontado a cada linha
com o código do órgão que acabou de ser lido, e a segunda leitura em diante usa uma
forma diferente de posicionamento; a rotina de leitura é importada da biblioteca de
execução e não tem fonte no acervo, e os sinalizadores de posicionamento que ela
recebe não estão explicados no corpus nem no manual. Se a leitura avança, a grade
mostra órgãos consecutivos; se ela relê a mesma chave, o mesmo órgão se repete nas
13 linhas. Os dois comportamentos são compatíveis com o que o fonte mostra, e o
site precisa dizer qual é o esperado.

[?] O que aparece nas linhas que sobram quando o grupo tem menos de 13 órgãos: a
montagem da lista não limpa os campos da linha ao terminá-la — a limpeza só existe
na passagem em que o servidor envia a tela —, e o que a máscara traz para essas
linhas não está no material lido. Se elas deveriam sair em branco, o caminho de
montagem não as limpa. Pergunta ao site.

[?] O código do órgão filho de cada linha é conferido como número quando volta da
tela, mas — ao contrário do grupo, do mês, do ano e do órgão de partida — não tem
desvio de cursor para ele. Se existe recusa que deva devolver o cursor à linha, o
caminho não a tem.

[?] O rótulo que o servidor lê em cima de cada coluna da grade não está no acervo:
a ficha da tela registra só os rótulos dos campos que ela valida.

[?] A tela declara na área de trabalho um campo para o **nome do órgão** que nenhum
caminho preenche nem lê — o nome que ela guarda vai para outro campo da mesma área
—, e um campo de controle que ela reinicia em branco e nunca lê. Se algum dos dois
deveria alimentar alguma coluna, algum destaque ou o cabeçalho, o caminho não o faz.

### RN-07 — A situação do mapa: um mapa até julho de 2008, outro de agosto de 2008 em diante

A situação de cada órgão é **Aberto** ou **Fechado**, conforme o registro do mapa
daquele órgão no mês e no ano de referência. O mapa consultado depende da época: de
**agosto de 2008** em diante há um só mapa, e o estado vem do próprio registro;
para mês e ano **anteriores**, a situação vem do **mapa mensal antigo** e, quando o
órgão é **creche**, do **mapa de creche**. O mapa mensal antigo guarda **46
campos**, o mapa de creche **31** e o mapa único **14**; as capacidades declaradas
são, respectivamente, **1.000.000**, **500.000** e **1.000.000** registros —
capacidade é dimensionamento, não volume.

[?] A data que separa os dois mapas é uma constante da própria tela, fixa em agosto
de 2008, e não algo que venha do cadastro. O nome do campo sugere "data do mapa
anterior"; o que exatamente ela separa — qual geração de mapa — não está no corpus
nem no manual. Pergunta ao site.

[?] O indicador de creche da linha e o caminho do mapa leem o **mesmo atributo** em
sentidos opostos: o indicador mostra "Nao" para tudo que não é **S**, e o caminho
do mapa manda para o mapa de creche tudo que não é **N**. Um órgão com o atributo
em branco — que é o valor inicial do cadastro — aparece como "Nao" na linha e é
consultado no mapa de creche. Os dois desfechos não podem ser ambos pretendidos; o
site precisa dizer qual vale.

### RN-08 — Sem mapa no mês, a linha diz que não foi digitado

Não havendo registro do mapa daquele órgão no mês e no ano de referência, a linha
não mostra "Aberto" nem "Fechado": mostra **\* Nao digitado \***. A conferência é
feita primeiro pelo estado aberto e, não achando, pelo estado fechado; só então a
linha conclui que o mapa não foi digitado.

### RN-09 — O órgão informado é o ponto de partida da lista, e o campo volta com o último mostrado

O campo do órgão de partida, rotulado **CDORGDIS** na tela, aceita o código de um
órgão filho e faz a lista começar por ele — desde que o mês e o ano não tenham sido
trocados na mesma passagem; trocados, a lista recomeça do primeiro órgão do grupo
(RN-04). Um órgão que não é do grupo faz a lista recomeçar do primeiro órgão, sem
mensagem nenhuma. Terminada a listagem, o campo volta preenchido com o **último
órgão mostrado**, e volta zerado quando o grupo tem menos órgãos do que a grade.

[?] Um código de órgão digitado que não existe no grupo não gera aviso: a lista
recomeça no primeiro órgão do grupo e o servidor não fica sabendo que o código foi
descartado. Se o desenho previa aviso, o caminho não o tem.

[?] O que a tela mostra quando o servidor reenvia a tela sem mudar nada. Nessa
passagem a tela não decide reler por conta própria: ela encontra o ponto de partida
igual ao que está em vigor e encerra a passagem. Se a lista volta com a mesma
página ou continua na seguinte depende da leitura importada, que é a mesma raiz da
dúvida da RN-06.

### RN-10 — O grupo sem nenhum órgão cadastrado avisa

Não havendo nenhum órgão filho cadastrado no grupo, a tela avisa
**\* Grupo sem perfis cadastrados para o Mes/Ano \*** e não preenche nenhuma linha.

[?] A mensagem fala do mês e do ano, mas a leitura que a produz não os usa: o
cadastro de órgãos é procurado só pelo tipo de órgão e pelo grupo, e o aviso sai
igual para qualquer mês. A palavra "perfis" também não é o nome que o resto desta
tela dá aos órgãos do grupo. Se o aviso deveria distinguir "grupo sem órgãos" de
"sem mapa no mês", o caminho não distingue.

### RN-11 — O cabeçalho traz a descrição do tipo de órgão e a data do sistema

Fora da grade, a tela mostra a **descrição do tipo de órgão** da sessão e a **data
do sistema**.

[?] Nem a descrição do tipo de órgão nem a data do sistema são preenchidas por
nenhum programa do acervo lido: as duas aparecem **480 vezes cada**, sempre como
origem de cópia, e a única outra linha é a inicialização em branco. Se não vierem
do ambiente de execução, os dois campos saem em branco. De onde vêm é pergunta ao
site.

### RN-12 — A consulta não grava nada e não deixa rastro de auditoria

A tela e as rotinas comuns que ela chama **só leem**. Nenhum registro é incluído,
alterado ou excluído, e nenhum registro de auditoria é gerado. A tela faz **18
chamadas de leitura** de cadastro — nove pontos de leitura, cada um com as duas
formas de posicionamento — e **nenhuma de gravação**. As operações de inclusão, de
exclusão e de travamento de registro existem declaradas para os **6 cadastros** que
a tela enxerga, mas **não são executadas em nenhum caminho**: declarar não é
executar.

### RN-13 — Cada consulta começa com os campos de resultado limpos

Antes de conferir a digitação e de ler os cadastros, a tela apaga os **seis** campos
de resultado — a descrição do tipo de órgão, a data do sistema, o nome e o código do
órgão de partida, o indicador de creche e a situação. Uma consulta recusada,
portanto, não deixa na tela o resultado da consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica — o tipo
cujo valor é 4 e cujo significado não está no corpus nem no manual. Se existe um
caminho de entrada em que os campos não são limpos, não foi possível determinar.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar a situação do mapa mensal dos órgãos filhos da coordenadoria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M010C

  Cenário: A lista dos órgãos filhos com a situação do mapa
    Dado que o meu grupo tem órgãos filhos cadastrados
    E que há mapa de agosto de 2008 em diante registrado para esses órgãos
    Quando abro a tela M010C e informo o mês e o ano de referência
    Então vejo uma linha por órgão, com o código e o nome do órgão,
      o indicador de creche e a situação do mapa daquele mês

  Cenário: A grade mostra no máximo 13 órgãos
    Dado que o meu grupo tem mais de 13 órgãos filhos cadastrados
    Quando abro a tela M010C e informo o mês e o ano de referência
    Então a grade mostra 13 linhas
    E a listagem para nessa linha

  Cenário: O indicador de creche
    Dado que um órgão filho do meu grupo está cadastrado como creche
    Quando a lista é montada
    Então a linha desse órgão mostra "Sim" no indicador de creche
    E a linha de um órgão que não é creche mostra "Nao"

  Cenário: A situação vem do mapa único a partir de agosto de 2008
    Dado que informo um mês e um ano de referência de agosto de 2008 em diante
    Quando a lista é montada
    Então a situação de cada órgão vem do mapa único daquele mês
    E aparece "Aberto" quando o mapa está aberto e "Fechado" quando está fechado

  Cenário: A situação vem do mapa antigo antes de agosto de 2008
    Dado que informo um mês e um ano de referência anteriores a agosto de 2008
    Quando a lista é montada
    Então a situação de cada órgão vem do mapa mensal antigo
    E, para os órgãos cadastrados como creche, vem do mapa de creche

  Cenário: Órgão sem mapa no mês de referência
    Dado que um órgão filho do meu grupo não tem mapa registrado para o mês informado
    Quando a lista é montada
    Então a linha desse órgão mostra "* Nao digitado *" na situação

  Cenário: O órgão informado é o ponto de partida da lista
    Dado que o meu grupo tem órgãos filhos cadastrados
    Quando informo o código de um desses órgãos no campo do órgão de partida,
      sem trocar o mês e o ano
    Então a lista começa por esse órgão

  Cenário: O órgão de partida de outro grupo
    Dado que informo o código de um órgão que não pertence ao meu grupo
    Quando envio a tela
    Então a lista recomeça do primeiro órgão do meu grupo
    E nenhum aviso é mostrado

  Cenário: O campo do órgão de partida volta com o último órgão mostrado
    Dado que a lista mostrou 13 órgãos
    Quando a tela é apresentada
    Então o campo do órgão de partida volta com o último órgão mostrado

  Cenário: Faltando o mês ou o ano de referência
    Dado que estou na tela M010C
    Quando envio a tela com o mês em branco, ou com o ano em branco
    Então vejo a mensagem "* Informe Mes/Ano para a consulta *"
    E o cursor volta ao campo do mês
    E nenhum órgão é lido

  Cenário: O mês e o ano correntes na primeira abertura
    Dado que abro a tela M010C pela primeira vez
    Quando ela é montada sem eu informar o mês e o ano
    Então o mês e o ano mostrados são os correntes

  Cenário: Grupo diferente do meu
    Dado que a minha sessão tem uma coordenadoria
    Quando informo o código de outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo do grupo
    E nenhum órgão é lido

  Cenário: Grupo informado por quem não tem grupo na sessão
    Dado que a minha sessão não tem coordenadoria
    E que o grupo que informo pertence à minha secretaria
    Quando envio a tela
    Então a lista traz os órgãos filhos desse grupo

  Cenário: Grupo de outra secretaria
    Dado que a minha sessão não tem coordenadoria
    Quando informo o código de um grupo que não pertence à minha secretaria
    Então vejo a mensagem "* Grupo nao pertence a esta secretaria *"
    E o cursor volta ao campo do grupo
    E nenhum órgão é lido

  Cenário: Sem grupo informado por quem não tem grupo na sessão
    Dado que a minha sessão não tem coordenadoria
    Quando envio a tela sem informar o grupo
    Então vejo a mensagem "* Informe o Grupo para a consulta *"
    E o cursor volta ao campo do grupo

  Cenário: Trocar de grupo descarta o mês e o ano informados
    Dado que a minha sessão não tem coordenadoria
    Quando informo um grupo e, junto, um mês e um ano de referência
    Então a lista traz os órgãos desse grupo
    E o mês e o ano mostrados são os que já estavam em vigor

  Cenário: Grupo sem órgãos cadastrados
    Dado que o grupo da consulta não tem nenhum órgão filho cadastrado
    Quando a lista é montada
    Então vejo a mensagem "* Grupo sem perfis cadastrados para o Mes/Ano *"
    E nenhuma linha da grade é preenchida

  Cenário: Operação diferente da consulta
    Dado que estou na tela M010C
    Quando informo uma operação diferente da consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nenhum órgão nem mapa é lido nesse caminho

  Cenário: O tipo de órgão e a data do sistema no cabeçalho
    Dado que entrei no sistema
    Quando abro a tela M010C
    Então vejo a descrição do tipo de órgão da minha sessão
    E vejo a data do sistema

  Cenário: A consulta não grava nada
    Dado que a lista dos órgãos foi mostrada
    Quando a tela é apresentada
    Então nenhum órgão e nenhum mapa é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: O resultado da consulta anterior não fica na tela
    Dado que já abri a tela e ela mostrou uma lista
    Quando volto a enviar a tela
    Então o código e o nome do órgão de partida, o indicador de creche,
      a situação e os campos do cabeçalho da consulta anterior não ficam na tela
```
