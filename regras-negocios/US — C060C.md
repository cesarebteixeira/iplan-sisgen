# US — C060C — Consultar as permissões de contrato da coordenadoria regional

## Estória

Como **servidor de CRE**, quero **consultar as permissões de contrato registradas
para uma coordenadoria regional, com a vigência, o tipo de contrato, o tipo de
licitação e o fornecedor de cada uma**, para que **eu saiba o que está registrado
para aquela regional, de que contrato e de que licitação cada permissão é, com qual
fornecedor e até quando ela vale — sem risco de alterar nada**.

A permissão é o registro que liga uma coordenadoria regional a um contrato e a um
grupo de licitação, com o fornecedor e a vigência daquela permissão; como o cadastro
guarda uma permissão por vigência, é a data limite que distingue uma versão da
outra. Quem precisa conferir o que a regional tem registrado — e não pode alterar
nada — responde por esta consulta; sem ela, a única forma de ver as permissões seria
abrir a tela de manutenção, que é de quem cadastra. Esta tela é só de leitura.

## Contexto

Jornada S000M → C000M → C050M → C060M → C060C.

Ator: servidor de CRE — informa a coordenadoria regional, a data limite, o tipo de
contrato e o grupo de licitação e vê, linha a linha, as permissões registradas.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O C000M, o C050M e o C060M são passos de menu que apenas encaminham, e nenhum deles
grava. O que a C060C usa da sessão — matrícula, código de acesso, privilégio, tipo de
órgão e a coordenadoria regional do servidor — é o que a entrada deixou; nada disso é
recalculado aqui. O C060M é o passo imediatamente anterior: ele escolhe a tela desta
jornada, mas **não** deixa opção de manutenção nem próxima tela para ela, de modo que
a C060C abre em consulta por conta própria e não há registro a passar adiante — ela é
o fim da jornada.

---

## Regras de negócio

### RN-01 — A tela é de consulta: qualquer outra opção é recusada

A tela abre em modo de consulta e repõe esse modo quando encontra o campo da opção
em branco. Se o operador enviar outra opção de manutenção, o sistema recusa com
**\* Operacao nao disponivel. Use CON \*** e devolve o cursor ao campo da opção —
antes de ler qualquer permissão. O caminho que monta a lista também só lê quando a
opção é a consulta.

[?] A recusa manda usar "CON", mas o sistema reconhece a consulta por um código
interno que o acervo escreve como "INQ"; nenhum valor "CON" existe no corpus lido.
Ou o formulário traduz o que o servidor digita para esse código, ou quem seguir a
mensagem é recusado. Pergunta ao site.

[?] A recusa só existe se a máscara oferecer ao operador um campo de opção: a ficha
da tela lista os seis rótulos informados e nenhum campo de opção. Se a máscara não
tem esse campo, a recusa é trecho sem uso. Pergunta ao site.

### RN-02 — Antes de mostrar a lista, o sistema confere o acesso

A abertura confere o acesso com o contexto que a sessão já trazia — matrícula,
código de acesso, privilégio, tipo de órgão e coordenadoria regional — e exige que a
tela esteja cadastrada no cadastro de telas: não estando, a recusa é
**\* Tela nao disponivel \***. A matrícula precisa ter a tela autorizada no seu
código de acesso: não tendo, a recusa é
**\* Acesso negado para esta matricula \***. A mensagem do operador passa ainda pela
lógica de rota, que recusa com **\* Operacao nao disponivel \*** uma opção que o
sistema não reconheça. Esse contexto não é recalculado aqui: é o que a entrada
deixou.

[?] A conferência da operação procura os flags de inclusão, de alteração e de
exclusão, mas **não** o de consulta: quem tem a tela autorizada consulta sem
precisar do flag de consulta. Se a intenção era exigir esse flag por tela, o caminho
não o exige. Pergunta ao site.

[?] A tela tem a sua própria recusa por opção inválida e a lógica de rota também
recusa opções antes dela; as duas mensagens são diferentes e não está no acervo qual
delas o operador vê em cada caso. Pergunta ao site.

### RN-03 — A tela consulta o cadastro das permissões de contrato

O cadastro consultado é o das permissões de contrato, na C061T. Ele tem **52 campos**
e capacidade para **1.000.000** de registros (capacidade é o máximo esperado,
parâmetro de dimensionamento, não o que está cadastrado). Cada permissão é um
registro próprio: a consulta distingue uma da outra pela coordenadoria regional,
pela vigência — as três partes da data limite —, pelo tipo de contrato, pelo grupo de
licitação, pela classe, pela subclasse e pelo gênero, e a chave admite repetições.
As permissões marcadas como excluídas ficam fora da consulta. Quem mantém esse
cadastro é a C060T, a tela de manutenção do mesmo menu, e dezenas de outras telas do
acervo também gravam nele; esta tela, não.

### RN-04 — A consulta é pela coordenadoria, pela vigência, pelo contrato e pelo grupo de licitação

O operador informa **a coordenadoria regional**, **o dia, o mês e o ano limite**,
**o tipo de contrato** e **o grupo de licitação**; a leitura leva também o tipo de
órgão da sessão — a tela só enxerga as permissões do órgão de quem está logado — e
leva classe, subclasse e gênero zerados, porque não são informados. Não achando, a
tela recusa (RN-07); achando, o que foi informado passa a ser a consulta.

[?] A leitura usa o recurso de posicionamento do dicionário de dados, cujo efeito
exato não está no acervo nem no manual: se ele exige a chave exata, o operador só
acha quem sabe a combinação inteira; se ele posiciona na primeira permissão igual ou
posterior, o que foi informado é apenas o ponto de partida da lista. Os dois
comportamentos são compatíveis com o que o fonte mostra — a conferência seguinte
compara o tipo de órgão e a coordenadoria regional, e **nunca** a data, o contrato ou
o grupo. O site precisa dizer qual é o esperado.

### RN-05 — Ao informar outra coordenadoria, a tela adota a última vigência registrada nela

Ao informar uma coordenadoria regional **diferente da última consultada**, a tela não
parte do que foi digitado: monta a consulta com os valores máximos de ano, mês e dia
e vai buscar a última permissão registrada para aquela coordenadoria. Quando a
encontra, a data limite dessa permissão passa a ser a data da consulta e o tipo de
contrato informado é apagado; o grupo de licitação informado fica no campo, mas não
entra na consulta. Não encontrando nenhuma permissão para a coordenadoria, a consulta
segue com o que o operador informou.

[?] Esse ramo vale para todo primeiro uso de uma coordenadoria — a comparação é com a
última coordenadoria consultada, não com a da sessão —, de modo que a data limite
digitada na primeira consulta de uma coordenadoria é descartada. Se isso é o
pretendido ou resíduo do gerador, o acervo não diz. Pergunta ao site.

[?] O achado da "última permissão" depende do posicionamento da leitura: se o recurso
não devolver registro para os valores máximos, o ramo que adota a data registrada
nunca roda e a data informada permanece. Pergunta ao site.

### RN-06 — A grade mostra até 14 permissões, uma por linha

A grade da tela tem **14 linhas**, e cada linha traz **oito informações**: a data de
início, a data limite, o tipo de contrato, o tipo de licitação, a descrição do tipo
de licitação, o grupo de licitação, o código do fornecedor e a razão social. As duas
datas saem no formato **dia/mês/ano**, com o dia e o mês em dois dígitos e o ano em
quatro. A descrição do tipo de licitação vem do cadastro C143T e a razão social, do
cadastro C030T: a linha mostra as duas **cortadas** em 13 e em 20 posições, embora os
cadastros guardem 30 e 40. As permissões aparecem na ordem da chave do cadastro:
dentro da coordenadoria regional, por ano, mês e dia limite e, na mesma data, por
tipo de contrato, grupo de licitação, classe, subclasse e gênero. Não havendo mais
permissão para mostrar, as linhas restantes ficam em branco.

[?] Os rótulos das colunas da grade não estão no acervo lido: o programa só traz os
seis rótulos dos campos informados. Pergunta ao site.

### RN-07 — Não havendo permissão para o que foi informado, a tela avisa

Não havendo permissão para o que foi informado, a tela avisa
**\* Nao existem permissoes para estes dados \*** e não preenche nenhuma linha. O
aviso é decidido na montagem da **primeira linha** da página e não é repetido nas
demais. Na conferência que adota uma data já informada, a recusa é a mesma, com o
cursor de volta ao campo do ano limite.

### RN-08 — A lista continua de onde parou

A tela guarda a chave da última permissão listada e a chave com que a consulta
começou. Ao montar a página seguinte, a primeira linha relê a partir da última
permissão listada e **pula** a que já apareceu, de modo que a lista continua de onde
parou; quando a página enche as 14 linhas, os campos informados passam a mostrar a
chave da 14ª permissão, e reenviar a consulta nesse estado traz as próximas 14.

[?] O trecho que adota uma chave informada nova só roda quando a lista já avançou
além do ponto de partida; se a consulta anterior não achou nada — ou acabou na
primeira linha —, uma data nova informada para a mesma coordenadoria é descartada
sem aviso, e a tela repete o resultado anterior. Se isso é o pretendido, é pergunta
ao site.

[?] A chave da última consulta fica guardada na área livre da sessão; se ela
sobrevive a sair da tela e voltar depois, o acervo não mostra. Pergunta ao site.

### RN-09 — A digitação dos seis campos é editada, e o cursor volta ao campo recusado

Os seis campos informados — a coordenadoria regional, o dia, o mês e o ano limite, o
tipo de contrato e o grupo de licitação — passam por edição numérica antes de
qualquer leitura: campo em branco é tratado como zero, o que não for número é
recusado e a consulta não segue, e o cursor volta ao campo recusado.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual — não
está nos fontes desta jornada: a rotina que faz a edição numérica não faz parte do
acervo lido. Pergunta ao site.

### RN-10 — Cada consulta começa com os campos de resultado limpos

Antes de conferir a digitação e de ler qualquer permissão, a tela apaga os **dez
campos de resultado** que a consulta anterior havia mostrado: a descrição do tipo de
órgão, a data do sistema, as duas datas, o tipo de contrato, o tipo de licitação, a
descrição da licitação, o grupo de licitação, o código do fornecedor e a razão
social. Uma consulta recusada, portanto, não deixa na tela o resultado da consulta
anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe
um caminho de entrada em que os campos não são limpos, é pergunta ao site.

### RN-11 — A tela mostra a data do sistema e a descrição do tipo de órgão da sessão

Fora da grade, a tela exibe a **data do sistema** e a **descrição do tipo de órgão**
da sessão; ela também lê o cadastro dos tipos de órgão, na C120T, pela chave do tipo
da sessão.

[?] Nem a data do sistema nem a descrição do tipo de órgão são preenchidas por nenhum
caminho que o acervo mostre: a leitura do cadastro dos tipos de órgão guarda a
descrição numa área de trabalho que não é a que a tela exibe, e os dois campos só
aparecem como origem de cópia de outra área. Se o ambiente transporta os valores de
uma para a outra — e de onde vem a data do sistema —, é pergunta ao site; se não
transportar, os dois campos saem em branco.

### RN-12 — A consulta não grava nada e não deixa rastro de auditoria

A tela e as rotinas comuns que ela chama só leem. Nenhuma permissão é incluída,
alterada ou excluída, e nenhum registro de auditoria é gerado. As operações de
gravação, de exclusão e de travamento de registro existem declaradas para os cinco
cadastros que a tela enxerga, mas **não são executadas em nenhum caminho**: declarar
não é executar.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar as permissões de contrato da coordenadoria regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C060C

  Cenário: Consulta das permissões da coordenadoria regional
    Dado que a coordenadoria regional informada tem permissões registradas
    Quando envio a consulta
    Então vejo as permissões em linhas, cada uma com a data de início, a data limite, o contrato, a licitação e o fornecedor

  Cenário: A grade mostra no máximo 14 permissões
    Dado que a coordenadoria regional informada tem mais de 14 permissões registradas
    Quando envio a consulta
    Então a grade mostra no máximo 14 linhas
    E as linhas restantes ficam em branco

  Cenário: As permissões aparecem na ordem da vigência
    Dado que a coordenadoria regional informada tem mais de uma permissão registrada
    Quando envio a consulta
    Então cada linha traz uma permissão diferente, em ordem crescente de data limite

  Cenário: As datas aparecem no formato dia/mês/ano
    Dado que uma permissão tem data de início e data limite registradas
    Quando envio a consulta
    Então vejo as duas datas no formato dia/mês/ano, com o ano em quatro dígitos

  Cenário: Cada linha traz a licitação e o fornecedor
    Dado que uma permissão tem tipo de licitação e fornecedor registrados
    Quando envio a consulta
    Então vejo a descrição do tipo de licitação e a razão social do fornecedor na linha da permissão

  Cenário: A data do sistema e o tipo de órgão da sessão
    Dado que entrei no sistema
    Quando abro a tela C060C
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: Consulta pela coordenadoria, pela vigência, pelo contrato e pelo grupo
    Dado que existe permissão registrada para a coordenadoria regional, a data limite, o tipo de contrato e o grupo de licitação que informei
    Quando envio a consulta
    Então a tela mostra as permissões daquela coordenadoria a partir daquele ponto

  Cenário: Coordenadoria regional diferente da última consultada
    Dado que informo uma coordenadoria regional diferente da última consultada
    Quando envio a consulta
    Então a data limite passa a ser a da última permissão registrada para aquela coordenadoria
    E o tipo de contrato informado não é considerado

  Cenário: Nenhuma permissão para o que foi informado
    Dado que não existe permissão para a coordenadoria regional, a data limite, o tipo de contrato e o grupo de licitação que informei
    Quando envio a consulta
    Então vejo a mensagem "* Nao existem permissoes para estes dados *"
    E nenhuma linha da grade é preenchida

  Cenário: A consulta continua na página seguinte
    Dado que a consulta mostrou as 14 linhas da página
    Quando reenvio a consulta sem mudar nada
    Então vejo as permissões seguintes, a partir da que já apareceu por último

  Cenário: Opção de manutenção diferente de consulta
    Dado que estou na tela C060C
    Quando informo uma opção diferente da consulta
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nenhuma permissão é lida nesse caminho

  Cenário: Digitação não numérica na coordenadoria ou na data limite
    Dado que digito na coordenadoria regional, na data limite, no tipo de contrato ou no grupo de licitação algo que não é número
    Quando envio a consulta
    Então o sistema recusa a digitação antes de listar qualquer permissão
    E o cursor volta ao campo recusado

  Cenário: O resultado da consulta anterior não fica na tela
    Dado que já abri a tela e ela mostrou permissões
    Quando volto a consultar
    Então as datas, o contrato, a licitação e o fornecedor da consulta anterior não ficam na tela

  Cenário: A consulta não grava nada
    Dado que abro a tela C060C
    Quando a lista é mostrada
    Então nenhuma permissão é incluída, alterada ou excluída
    E nenhum registro de auditoria é gerado

  Cenário: Tela não cadastrada
    Dado que a tela C060C não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo consultar

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela C060C autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo consultar
```
