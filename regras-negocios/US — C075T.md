# US — C075T — Manter os períodos semanais da coordenação regional

## Estória

Como **servidor de CRE**, quero **registrar, para a minha coordenação regional, o
início e a letra de cada semana do período**, para que **a sequência de semanas do
ano fique completa sem eu cadastrar uma semana por vez**.

O período é registrado semana a semana: cada semana precisa da data em que começa e
de uma letra que a distinga das outras — a letra da semana. Quem responde por essa
sequência na ponta é a coordenação regional de ensino. A tela mostra as semanas já
registradas e, na alteração, completa as que faltam até o fim do ano informado. Sem
essa sequência, as telas que usam o período depois não têm de onde tirar a letra da
semana de cada data.

## Contexto

Jornada S000M → C000M → C070M → C075T.

Ator: servidor de CRE — registra e confere, para a sua coordenação regional, o
início e a letra de cada semana do período.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é **dado de navegação**, não regra de negócio.

Os dois passos anteriores são menus e não gravam nada. O que a C075T usa da sessão
— a matrícula, o código de acesso, o privilégio, o tipo de órgão e a coordenação
regional — é o que o vínculo do servidor deixou registrado na entrada. A jornada
termina nesta tela: a C075T não encadeia outra passando o período e a operação
adiante.

---

## Regras de negócio

### RN-01 — O que a tela mantém: uma semana por período, com data de início e letra

Cada período é uma semana da coordenação regional, e dele se guardam o **tipo de
órgão**, a **coordenação regional**, a **data de início** — dia, mês e ano — e a
**letra da semana**. Não existem dois períodos com o mesmo tipo de órgão, a mesma
coordenação regional e a mesma data de início; a letra não faz parte da identidade,
de modo que a mesma semana não pode ser registrada duas vezes com letras
diferentes. O cadastro é dimensionado para **10.000** períodos (capacidade é o
máximo esperado, parâmetro de dimensionamento, não o que está registrado).

### RN-02 — A lista mostra até 12 semanas, em ordem de data de início

Ao apresentar a tela, o sistema lê os períodos da coordenação regional em ordem
crescente de data de início e mostra **até 12** por vez, cada linha com a **data de
início** e a **letra** daquela semana. Terminados os períodos registrados, a lista
para e as linhas seguintes ficam em branco.

### RN-03 — A consulta é pela coordenação regional e pela data de início

O servidor informa a coordenação regional e o dia, o mês e o ano de início, e envia
a consulta. A tela procura o período dessa coordenação a partir daquela data; não
achando nenhum, avisa **\* Nao existem registros a partir da data inf \***, devolve
o cursor ao campo do dia de início e não monta a lista. Achando, a lista começa
naquele período.

### RN-04 — A coordenação informada tem de constar do cadastro da secretaria

Quando a consulta é de uma coordenação regional diferente da que está em tela, a
tela confere se ela consta do cadastro de coordenações regionais da secretaria,
pela combinação do tipo de órgão com a coordenação regional. Não constando, recusa
com **\* Grupo nao pertence a esta secretaria \*** e devolve o cursor ao campo da
coordenação regional. Na alteração essa conferência não se repete.

### RN-05 — O servidor só alcança a coordenação regional a que tem acesso

Quando o vínculo da sessão traz uma coordenação regional, a informada tem de ser a
mesma; sendo outra, a tela recusa com **\* Usuario sem acesso a este grupo \*** e
devolve o cursor ao campo. Quando o vínculo não traz coordenação regional, essa
conferência não é feita, e o servidor alcança as demais coordenações da sua
secretaria.

### RN-06 — A tela abre em consulta e só aceita consulta e alteração

A tela abre no modo de consulta, e é ela que repõe esse modo a cada abertura. Se a
operação informada for diferente de consulta e de alteração — inclusão, exclusão ou
qualquer outra —, o sistema recusa com **\* Operacao nao disponivel \***, devolve o
cursor ao campo da operação e não lê nem mostra nada.

### RN-07 — A alteração exige que a coordenação regional já esteja em tela

A alteração só segue quando a coordenação regional informada é a que já está em
tela, isto é, a que foi consultada. Sendo outra, a tela recusa com
**\* Consulte antes de atualizar \*** e devolve o cursor ao campo da coordenação
regional.

[?] Quando o vínculo da sessão já traz a coordenação regional do servidor, a
conferência de acesso anterior obriga as duas a serem iguais, de modo que essa
recusa fica inalcançável por esse caminho — e esse servidor altera sem ter
consultado antes. Se a intenção era exigir sempre a consulta prévia, o caminho não
a exige. Pergunta ao site.

### RN-08 — A atualização tem de começar numa segunda-feira

A data informada para começar a atualização precisa cair numa **segunda-feira**.
Não caindo, a tela recusa com **\* Atualizacao deve comecar na segunda-feira \*** e
devolve o cursor ao campo do dia da atualização.

### RN-09 — A letra da semana vai de A a D

A letra informada para a primeira semana atualizada tem de ser **A, B, C ou D**.
Sendo outra, a tela recusa com
**\* Letra de atualizacao deve ser A, B, C ou D \*** e devolve o cursor ao campo da
letra.

### RN-10 — A alteração completa as semanas até o fim do ano, alternando a letra

Confirmada a alteração, o sistema percorre as semanas de **sete em sete dias**, a
partir da data informada, enquanto elas estiverem no **ano daquela data**: para
cada semana, se o período ainda não existir, ele é incluído; se já existir, ele é
regravado com a letra daquela semana. A letra começa na informada e alterna na
ordem **A, B, C, D**, voltando a A. Numa só confirmação, portanto, o servidor
registra o resto do ano — não uma semana só. Sem o dia da atualização informado, a
alteração não faz nada e não avisa nada.

### RN-11 — O que a alteração grava e o que a consulta não grava

Cada semana incluída ou regravada é gravada no cadastro de períodos e deixa um
registro na auditoria das operações (A010T), com a operação — inclusão ou alteração
—, a imagem anterior e a imagem posterior do período, a matrícula, a estação, a
data e a hora da sessão. A consulta não grava nada e não deixa rastro. A tela não
exclui período nenhum: as rotinas de exclusão existem declaradas para os cadastros
que ela enxerga, mas não são executadas — declarar não é executar; o que a tela
executa é a gravação do período e a da auditoria. A tela também não inclui período
por inclusão avulsa: a inclusão só acontece dentro da sequência da alteração.

[?] Na inclusão, o registro de auditoria está sob uma condição do estado devolvido
pela gravação — o mesmo estado que o ambiente de mensagens marca como "DATA" —, e
na alteração ele é incondicional. Se esse estado estiver posto justamente quando a
semana é incluída, a semana fica gravada sem rastro. Pergunta ao site.

### RN-12 — A digitação dos campos numéricos é conferida, e o cursor volta ao campo recusado

A coordenação regional, o dia, o mês e o ano de início e o dia, o mês e o ano da
atualização — **sete campos** — passam por conferência de digitação antes de
qualquer leitura: campo em branco é tratado como zero, o que não for número é
recusado, e o cursor volta ao campo recusado.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual — não
está nos fontes desta jornada: a rotina que faz essa conferência não faz parte do
acervo lido. Pergunta ao site.

### RN-13 — A tela mostra a data do sistema e a descrição do tipo de órgão

Ao abrir, a tela exibe a **data do sistema** e a **descrição do tipo de órgão** do
vínculo da sessão.

[?] Nem uma nem outra são preenchidas por um caminho que o acervo lido mostre: a
tela copia a data e a descrição da área de trabalho da sessão, e quem as preenche é
o ambiente, fora do lote. Se o ambiente não as preencher, os dois campos saem em
branco. Pergunta ao site.

### RN-14 — Cada apresentação apaga o resultado anterior

Antes de conferir a digitação e de ler qualquer período, a tela apaga a data do
sistema, a descrição do tipo de órgão e as datas e as letras que a apresentação
anterior havia mostrado. Uma consulta recusada, portanto, não deixa em tela o
resultado da anterior.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os períodos semanais da coordenação regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C075T

  Cenário: A lista das semanas da minha coordenação regional
    Dado que a minha coordenação regional tem semanas registradas
    Quando abro a tela C075T
    Então vejo as semanas em linhas, cada uma com a data de início e a letra da semana
    E as semanas aparecem em ordem crescente de data de início

  Cenário: A lista mostra até 12 semanas por vez
    Dado que a coordenação regional tem mais de 12 semanas registradas
    Quando abro a tela C075T
    Então a lista mostra no máximo 12 linhas
    E as linhas seguintes ficam em branco

  Cenário: Consulta a partir de uma data de início
    Dado que existe uma semana a partir da data de início que informei
    Quando envio a consulta
    Então a lista começa naquela semana

  Cenário: Consulta recusada por não haver semana a partir da data
    Dado que não existe semana a partir da data de início que informei
    Quando envio a consulta
    Então vejo a mensagem "* Nao existem registros a partir da data inf *"
    E o cursor volta ao campo do dia de início
    E a lista não é montada

  Cenário: Coordenação regional que não é da minha secretaria
    Dado que informei uma coordenação regional que não consta do cadastro da minha secretaria
    Quando envio a consulta
    Então vejo a mensagem "* Grupo nao pertence a esta secretaria *"
    E o cursor volta ao campo da coordenação regional

  Cenário: Coordenação regional fora do meu acesso
    Dado que o meu vínculo traz uma coordenação regional
    E informei outra coordenação regional
    Quando envio a consulta ou a alteração
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenação regional
    E nada é gravado

  Cenário: A tela abre em consulta
    Quando abro a tela C075T
    Então a operação em tela é a consulta

  Cenário: Operação diferente de consulta e de alteração
    Quando informo uma operação diferente de consulta e de alteração
    Então vejo a mensagem "* Operacao nao disponivel *"
    E o cursor volta ao campo da operação
    E nada é lido nem mostrado

  Cenário: Alteração sem a coordenação regional em tela
    Dado que a coordenação regional informada não é a que está em tela
    Quando envio a alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo da coordenação regional
    E nada é gravado

  Cenário: A atualização tem de começar numa segunda-feira
    Dado que informei uma data de atualização que não cai numa segunda-feira
    Quando envio a alteração
    Então vejo a mensagem "* Atualizacao deve comecar na segunda-feira *"
    E o cursor volta ao campo do dia da atualização
    E nada é gravado

  Cenário: A letra da semana tem de ser A, B, C ou D
    Dado que informei uma letra diferente de A, B, C e D
    Quando envio a alteração
    Então vejo a mensagem "* Letra de atualizacao deve ser A, B, C ou D *"
    E o cursor volta ao campo da letra
    E nada é gravado

  Cenário: A alteração completa as semanas do ano
    Dado que a coordenação regional está em tela
    E informei uma segunda-feira e a letra A
    Quando confirmo a alteração
    Então o sistema registra uma semana a cada sete dias, até o fim do ano daquela data

  Cenário: As semanas seguintes recebem a letra seguinte
    Dado que informei a letra A para a primeira semana
    Quando confirmo a alteração
    Então as semanas seguintes recebem as letras B, C e D, e a letra volta a A

  Cenário: Semanas já registradas são regravadas, e as que faltam são incluídas
    Dado que parte das semanas do ano já está registrada com outra letra
    Quando confirmo a alteração
    Então as semanas já registradas passam a ter a letra da sequência
    E as semanas que faltavam passam a existir

  Cenário: Alteração sem o dia da atualização não faz nada
    Dado que não informei o dia da atualização
    Quando confirmo a alteração
    Então nenhuma semana é incluída ou regravada
    E não vejo mensagem nenhuma

  Cenário: A alteração deixa rastro na auditoria
    Dado que confirmo uma alteração que grava semanas
    Então cada semana incluída ou regravada deixa um registro na auditoria
    E esse registro guarda a operação, a imagem anterior e a imagem posterior do período

  Cenário: A consulta não grava nada
    Dado que estou no modo de consulta
    Quando envio a consulta
    Então nenhuma semana é incluída, regravada ou excluída
    E nenhum registro de auditoria é gerado

  Cenário: A tela não exclui semana nenhuma
    Dado que uma semana existe
    Quando informo uma operação de exclusão
    Então vejo a mensagem "* Operacao nao disponivel *"
    E a semana continua registrada

  Cenário: Digitação não numérica é recusada
    Dado que digitei uma letra num campo numérico
    Quando envio a tela
    Então a tela recusa a digitação
    E o cursor volta ao campo recusado

  Cenário: A apresentação anterior é apagada antes da conferência
    Dado que a apresentação anterior mostrou semanas
    Quando envio uma consulta recusada
    Então a lista anterior não fica em tela

  Cenário: A data do sistema e a descrição do tipo de órgão
    Quando abro a tela C075T
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão do meu vínculo
```
