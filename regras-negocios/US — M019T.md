# US — M019T — Consulta do mês da coordenação regional escolar

## Estória

Como **servidor de CRE**, quero **consultar os registros cadastrados do mês de referência de uma
coordenação regional escolar, unidade por unidade, e abrir o perfil de atendimento da unidade que
eu marcar**, para que **eu veja quais unidades da minha coordenadoria têm números lançados naquele
mês e chegue ao perfil de cada uma sem acertar o código do órgão de memória**.

O perfil de atendimento do mês é mantido unidade a unidade, e ninguém sabe de cor o código de cada
escola da coordenadoria: esta tela é o índice do mês. Ela relaciona as unidades que têm registros
cadastrados naquele mês — com o segmento, o atendimento e as quantidades de parciais e de
integrais de cada uma — e leva o servidor ao perfil da unidade escolhida em consulta. Sem essa
relação, chegar ao perfil de uma unidade vira tentativa por código. Nada aqui é gravado: quem
mantém o perfil do mês é a tela seguinte.

## Contexto

Jornada S000M → M000M → M019T.

Ator: servidor de CRE — consulta os registros do mês de uma coordenação regional escolar e escolhe
uma unidade para abrir o perfil de atendimento dela em consulta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

As regras abaixo são só as da tela desta jornada. Os dois menus do caminho não gravam nada: só
encaminham. Esta tela também não grava — ela consulta e **encadeia** para a tela do perfil de
atendimento, a M010T, que é onde o mês se mantém; o que ela deixa para a tela seguinte está na
RN-08. As conferências de tela, de estação, de rota e de permissão que a M019T executa antes de
aceitar a operação são as mesmas de todas as telas e já estão no documento da entrada: ficam no
anexo de evidências, em **Regras que se revelaram da entrada**.

---

## Regras de negócio

### RN-01 — A tela consulta os registros do mês da coordenadoria e não grava nada

A M019T é uma tela de **consulta**. Ela relaciona, para uma **coordenação regional escolar** — o
grupo — e um **mês e ano de referência**, os **registros cadastrados** daquele mês: cada linha da
relação é uma **unidade** daquele grupo, com o **segmento** (código e descrição), o **atendimento**
(código e descrição) e as quantidades de **parciais** e de **integrais**. O cabeçalho mostra a
**operação**, o **grupo**, o **mês** e o **ano**, a **data de atualização** daquele conjunto de
registros, a descrição do **tipo de órgão** da sessão e a **data do sistema**.

Nada nesta tela é gravado: nem cadastro, nem travamento de registro, nem linha de auditoria. Nove
são as mensagens que a tela sabe mostrar, e todas são recusas ou avisos — não há aviso de sucesso.

[?] O que são, em negócio, esses registros. A própria tela os nomeia de duas maneiras —
**\* Nao existem reg.cadastr para este Mes/Ano \*** e **\* Matriculas nao cadastradas para esta
data \*** —, e o cadastro que ela lê **não está no dicionário de dados lido**: o dicionário da base
não traz esse cadastro, nem os seus campos, nem a sua chave, nem a sua capacidade. Sem ele, o que a
relação mostra não se confere pelo dicionário. Pergunta ao site.

### RN-02 — A tela abre com o grupo, o mês, o ano e a operação que ficaram guardados

Ao abrir, a tela repõe no **grupo**, no **mês** e no **ano de referência** e no campo da
**operação** o que ficou guardado da última utilização, e mostra no cabeçalho a **data de
atualização** do conjunto de registros daquele mês. Não havendo grupo guardado, a tela não
relaciona nada. A operação em branco é reposta como **consulta**.

[?] Com que grupo a tela abre. O grupo não é recalculado a partir do vínculo do servidor: ele é
lido do contexto da sessão, que é o mesmo espaço em que as telas deixam dados para as seguintes. A
tela abre, então, com o grupo que a última tela deixou ali — que é o do vínculo enquanto nenhuma
tela o substituir. A tela do mês, a M022C, abre esta já com o grupo que o servidor informou nela.
Se a tela deveria abrir sempre com o grupo do vínculo, pergunta ao site.

[?] Com que operação a tela reabre. A operação vem do que a última utilização deixou, e só é
reposta como consulta quando chega em branco — de modo que a tela pode reabrir com a operação que
outra tela usou antes. Se era para abrir sempre em consulta, pergunta ao site.

### RN-03 — Só a consulta é aceita

A tela só trabalha em **consulta**. Confirmando com qualquer outra operação no campo da operação, a
recusa é **\* Operacao nao disponivel. Use CON \***, com o cursor de volta nesse campo, e nada é
conferido nem gravado.

[?] O que a máscara mostra no campo da operação: a tela confere o código interno da consulta e a
mensagem manda usar **CON**. O que o servidor vê nesse campo não está no material lido. Pergunta ao
site.

### RN-04 — O grupo é o filtro da relação, e só vale o grupo do acesso

O grupo é o filtro: só aparecem as unidades daquele grupo.

O grupo informado tem de ser o **mesmo** que a tela já tinha. Informando outro, a recusa é
**\* Usuario sem acesso a este grupo \***, com o cursor de volta no campo do grupo, e nada é
consultado. Ele tem ainda de estar **cadastrado** para o tipo de órgão da sessão: não estando, a
recusa é **\* Grupo nao cadastrado \***, também com o cursor no campo do grupo e sem consultar
nada. E deixá-lo em branco — quando ele difere do que já estava na tela — é recusado com
**\* Informe o grupo \***, com o cursor no mesmo campo.

Quando o grupo, o mês e o ano informados são os mesmos que a tela já tinha, a relação não é
refeita: a tela reaproveita o que já mostrou.

[?] A conferência de acesso compara o grupo informado com o **grupo guardado na tela**, e esse
guardado pode ter vindo de outra tela — a M022C abre esta já com o grupo que o servidor informou
nela. Por esse caminho, o que a tela confere é o grupo informado aqui contra o grupo informado lá,
e não contra o vínculo do servidor. Se a conferência deveria ser sempre contra o vínculo, pergunta
ao site.

### RN-05 — O mês e o ano de referência são obrigatórios

Informar o **mês** e o **ano de referência** é obrigatório: chegando os dois em branco, a recusa é
**\* Informe Mes/Ano \***, com o cursor de volta no mês, e nada é consultado.

[?] A recusa só acontece quando o mês **e** o ano estão em branco: informando apenas um dos dois, a
conferência passa e a tela procura os registros por uma referência incompleta. Se o par deveria ser
exigido, falta a conferência. Pergunta ao site.

[?] A tela não confere se o mês informado existe no calendário (de 1 a 12): fora dessa faixa, o
valor passa pela conferência de número e vai à procura dos registros. Se o mês deveria ser validado
aqui, falta a conferência. Pergunta ao site.

### RN-06 — Sem registros no mês, a tela avisa

Não havendo registros cadastrados para aquele grupo naquele mês, a tela avisa e não relaciona nada.
A mensagem depende de quando a falta é encontrada: ao **abrir** a tela com a relação vazia,
**\* Matriculas nao cadastradas para esta data \***; ao **confirmar** um grupo ou um mês diferente
do que estava na tela, **\* Nao existem reg.cadastr para este Mes/Ano \***, com o cursor de volta
no mês.

### RN-07 — A relação vem em páginas de treze linhas, com os números de cada unidade

A relação é montada em **treze** linhas por vez, e cada linha é uma unidade com o seu segmento e o
seu atendimento. Chegando ao fim da página, a tela pede ao ambiente a linha seguinte, uma a uma,
até preencher a página; a relação **para na primeira linha em que não encontra registro**.

Cada linha mostra o **código e o nome da unidade**, o **segmento** com a sua **descrição**, o
**atendimento** com a sua **descrição**, as quantidades de **parciais** e de **integrais** e o
**indicador de seleção** da linha. O nome da unidade, a descrição do segmento e a do atendimento
vêm dos cadastros correspondentes. No rodapé, a tela mostra o código e o nome de uma unidade — a
última da página —, que é por onde a página seguinte começa.

### RN-08 — A linha marcada abre o perfil da unidade na tela do perfil do mês

Marcando o **indicador de seleção** de uma linha e confirmando, a M019T não segue com operação
própria: ela deixa no contexto a **unidade** daquela linha (código e nome), o **grupo**, o **mês e
o ano de referência**, o **início e o limite do período** daquele mês e a **situação do mapa** do
mês, com a operação em **consulta**, e passa para a **tela do perfil de atendimento** (M010T) —
que abre, por isso, em **consulta** daquele mês daquela unidade. É por essa passagem que a jornada
termina, e é ela que dispensa o servidor de digitar o código do órgão.

[?] O que marca a linha. O indicador de seleção é lido e exibido, mas o material lido só mostra o
literal que dispara a passagem ("S", a mesma letra de "sim"): a tela não tem conferência de valor
para esse campo, não tem mensagem própria para ele e não traz o rótulo que o servidor vê. Pergunta
ao site.

[?] A unidade que esta tela entrega é a mesma que a tela seguinte confere contra o vínculo. A tela
do perfil recusa a unidade que não é a do vínculo do servidor, mas, por este caminho, ela compara a
unidade que a M019T deixou com ela mesma — de modo que essa recusa não fecha, e a relação abre o
perfil de **qualquer** unidade da coordenadoria, e não só a do vínculo. Se a passagem deveria
alcançar apenas a unidade do vínculo, falta a conferência nesta tela. Pergunta ao site.

### RN-09 — Linha marcada sem unidade é recusada

Marcando a linha cujo campo da unidade está vazio, a recusa é
**\* Acesse perfil de linha preenchida \***, com o cursor no **indicador de seleção** daquela
linha, e nada é aberto.

### RN-10 — Unidade marcada sem perfil no mês é recusada

A unidade da linha marcada tem de ter **perfil de atendimento naquele mês**: não tendo, a recusa é
**\* Perfil nao cadastrado para este Orgao \***, com o cursor no **indicador de seleção**, e nada é
aberto.

[?] A unidade da linha não é conferida no cadastro das unidades: a leitura daquele cadastro tem
desfecho para "não achado", e ele segue adiante sem recusa própria. O que a tela faz é procurar o
perfil pelo **grupo que está no cadastro da unidade**, e não pelo grupo informado na tela: uma
unidade que não existe no cadastro, ou que exista noutro grupo, cai na recusa da falta de perfil.
Se a unidade inexistente deveria recusar por si, falta a recusa; pergunta ao site.

### RN-11 — Confirmar sem marcar nenhuma linha não abre nada

Confirmando a tela **sem** marcar nenhuma linha, a M019T não abre a tela seguinte e não grava nada:
ela aproveita a confirmação para guardar a unidade em que a página parou — que é por onde a relação
continua — e segue mostrando a relação. É o caminho de quem está só percorrendo a lista.

### RN-12 — Os campos desta tela passam pela conferência de número

Os códigos e as quantidades desta tela — o **grupo**, o **mês**, o **ano**, a **unidade** da linha,
o **segmento**, o **atendimento**, as **parciais**, as **integrais** e a **unidade** do rodapé; nove
campos — passam por uma conferência de **número** antes de a tela procurar os registros: o que não
for número é recusado no próprio campo. Nos sete campos de código, o que chega em branco é tratado
como zero.

[?] O que a tela faz depois da recusa e para onde o cursor volta. A conferência de número é uma
rotina externa, e o corpo dela não está no material lido: não se sabe a mensagem que o servidor vê
nem como a tela segue depois dela. A rotina desta tela posiciona o cursor em quatro dos nove campos
— o grupo, o mês, o ano e a unidade do rodapé —, e nos outros cinco o cursor fica com o que a
conferência deixou. Pergunta ao site.

### RN-13 — A tela não processa a confirmação quando chega prefixada por outra

Chegando com o **prefixo de tela** preenchido — a marca de que ela foi aberta por outra tela como
tela prefixada —, a M019T não processa a confirmação: nada é conferido, nada é aberto e nada é
gravado. A confirmação também para depois de a tela já ter encadeado para a tela seguinte, em vez de
processar as linhas restantes.

[?] O que preenche o prefixo de tela não está no corpus lido: não se sabe qual tela o manda nem o
que o servidor vê quando isso acontece. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar os registros do mês de uma coordenação regional escolar e abrir o perfil de atendimento da unidade escolhida

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M019T

  Cenário: RN-01 — consultar os registros do mês da coordenadoria
    Dado que informo a coordenação regional escolar e o mês e o ano de referência
    Quando confirmo a consulta
    Então vejo a relação das unidades daquele grupo naquele mês
    E vejo, de cada unidade, o nome, o segmento com a sua descrição, o atendimento com a sua descrição, as parciais e as integrais
    E vejo a data de atualização do conjunto, a descrição do tipo de órgão e a data do sistema

  Cenário: RN-01 — a consulta não grava nada
    Dado que faço uma consulta
    Quando a consulta termina
    Então nenhum registro é travado
    E nenhum cadastro é gravado
    E nenhuma linha nova aparece na trilha de auditoria

  Cenário: RN-02 — a tela abre com o que ficou guardado
    Dado que a última utilização deixou um grupo, um mês e um ano
    Quando abro a tela M019T
    Então o grupo, o mês e o ano já estão preenchidos com o que ficou guardado
    E o cabeçalho mostra a data de atualização daquele conjunto

  Cenário: RN-02 — sem grupo guardado a tela não relaciona nada
    Dado que não há grupo guardado nenhum
    Quando abro a tela M019T
    Então nenhuma unidade é relacionada

  Cenário: RN-03 — operação diferente de consulta é recusada
    Dado que estou na tela M019T
    Quando a tela chega com uma operação que não é a consulta
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor fica no campo da operação
    E nada é conferido e nada é gravado

  Cenário: RN-04 — grupo diferente do do acesso
    Dado que a tela já tem um grupo
    Quando informo outro grupo
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo do grupo
    E nada é consultado

  Cenário: RN-04 — grupo não cadastrado
    Dado que informo um grupo que não existe para o tipo de órgão da sessão
    Quando confirmo a consulta
    Então vejo "* Grupo nao cadastrado *"
    E o cursor fica no campo do grupo
    E nenhuma unidade é relacionada

  Cenário: RN-04 — grupo em branco
    Dado que o grupo informado difere do que já estava na tela
    Quando deixo o grupo em branco
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo do grupo
    E nada é consultado

  Cenário: RN-04 — o mesmo grupo, o mesmo mês e o mesmo ano não refazem a relação
    Dado que a relação do grupo já está na tela
    Quando confirmo outra vez com o mesmo grupo, o mesmo mês e o mesmo ano
    Então a relação não é refeita
    E vejo o que a tela já mostrava

  Cenário: RN-05 — sem o mês e o ano de referência
    Dado que estou na tela M019T
    Quando deixo o mês e o ano em branco e confirmo
    Então vejo "* Informe Mes/Ano *"
    E o cursor fica no mês
    E nada é consultado

  Cenário: RN-06 — a tela abre sem registros para o mês
    Dado que o grupo da tela não tem registros cadastrados no mês
    Quando abro a tela M019T
    Então vejo "* Matriculas nao cadastradas para esta data *"
    E nenhuma unidade é relacionada

  Cenário: RN-06 — confirmo um mês sem registros
    Dado que informo um mês que não é o que estava na tela
    E aquele mês não tem registros cadastrados para o grupo
    Quando confirmo a consulta
    Então vejo "* Nao existem reg.cadastr para este Mes/Ano *"
    E o cursor fica no mês
    E nenhuma unidade é relacionada

  Cenário: RN-07 — a relação em páginas de treze linhas
    Dado que o grupo tem mais unidades com registros no mês do que cabem na página
    Quando confirmo a consulta
    Então vejo as treze primeiras unidades, com segmento, atendimento, parciais e integrais
    E o rodapé mostra a última unidade da página
    E a relação continua pela página seguinte, a partir daquela unidade

  Cenário: RN-07 — a relação para na primeira unidade sem registro
    Dado que a lista de unidades acaba antes do fim da página
    Quando confirmo a consulta
    Então a relação para naquela altura
    E nenhuma linha sem registro é mostrada

  Cenário: RN-08 — a linha marcada abre o perfil da unidade em consulta
    Dado que a relação mostra as unidades do meu grupo naquele mês
    E marco o indicador de seleção da linha de uma unidade
    Quando confirmo
    Então a tela do perfil de atendimento abre, em consulta, naquele mês daquela unidade
    E nada é gravado por esta tela

  Cenário: RN-08 — o que a tela entrega à tela seguinte
    Dado que marco a linha de uma unidade
    Quando confirmo
    Então a tela seguinte abre com aquela unidade, aquele grupo e aquele mês e ano
    E ela abre com o início e o limite do período daquele mês e a situação do mapa do mês
    E ela abre em consulta

  Cenário: RN-09 — linha marcada sem unidade
    Dado que marco o indicador de seleção de uma linha sem unidade
    Quando confirmo
    Então vejo "* Acesse perfil de linha preenchida *"
    E o cursor fica no indicador de seleção da linha
    E nada é aberto

  Cenário: RN-10 — unidade marcada sem perfil no mês
    Dado que marco a linha de uma unidade que não tem perfil naquele mês
    Quando confirmo
    Então vejo "* Perfil nao cadastrado para este Orgao *"
    E o cursor fica no indicador de seleção da linha
    E nada é aberto

  Cenário: RN-11 — confirmar sem marcar nenhuma linha
    Dado que a relação mostra as unidades do meu grupo
    Quando confirmo sem marcar nenhuma linha
    Então nenhuma tela se abre
    E nada é gravado
    E a tela segue mostrando a relação

  Cenário: RN-12 — campo com texto em vez de número
    Quando informo texto em um dos códigos ou das quantidades desta tela
    Então o campo é recusado no próprio campo, pela conferência de número
    E a tela não procura os registros com esse texto

  Cenário: RN-13 — o prefixo de tela preenchido
    Dado que a tela chega prefixada por outra tela
    Quando confirmo
    Então nada é conferido, nada é aberto e nada é gravado
```
