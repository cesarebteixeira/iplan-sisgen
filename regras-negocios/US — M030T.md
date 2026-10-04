# US — M030T — Manter a movimentação de estoque do mês de referência de um órgão

## Estória

Como **servidor de CRE**, quero **incluir, excluir e consultar as movimentações de estoque
do mês de referência de um órgão filho da minha coordenadoria**, para que **o mapa daquela
unidade fique com o que de fato entrou e saiu no mês, e o órgão seguinte possa ser lançado
sobre um mês já fechado**.

Cada linha da movimentação registra o que aconteceu com o estoque da unidade no mês: a
ocorrência (remanejamento, recebimento, determinação ou extra), o órgão de destino, o
fornecedor e a nota fiscal, o gênero, a quantidade e o valor. É essa movimentação que fecha
o mapa do mês. Sem ela, o mapa da unidade fica sem lastro — e o mês seguinte não tem sobre o
que começar.

## Contexto

Jornada S000M → M000M → M030T (3 passos).

Ator: servidor de CRE — a mantenedora da movimentação de estoque do mês de referência das
unidades da sua coordenadoria.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O contexto que ela usa — a matrícula, o
privilégio, o tipo de órgão, a coordenadoria e o órgão permitido do vínculo — é o que a
entrada deixou na sessão, e as regras disso são da entrada. A jornada termina nesta tela:
ela não encadeia em outra.

---

## Regras de negócio

### RN-01 — A operação vem de quem abriu a tela, e a tela não deixa passar outra

A tela mantém a movimentação do mês em três modos, e o modo é decidido **fora** dela: é a
operação que a tela de origem passou junto com o registro. Chegando uma operação diferente
de inclusão, exclusão e consulta, o sistema recusa com
**\* Operacao nao disponivel. Use INC, EXC ou CON \***, devolve o cursor ao campo da
operação e encerra a passagem sem ler nem gravar nada.

As telas não mostram o mesmo rótulo para as três operações: a mensagem pede **INC**, **EXC**
e **CON**, e o que a tela recebe são os códigos de operação do sistema. O que aparece no
campo é a forma curta de cada uma.

[?] O rótulo que o servidor lê no campo da operação não está no material desta jornada — a
máscara da tela não foi lida. Se ela mostra INC/EXC/CON ou a forma curta, pergunta ao site.

### RN-02 — A operação e o órgão da tela de origem continuam valendo

O modo da tela não é escolhido aqui: quem o decide é a tela que a abriu, e o que ela passou
continua valendo — inclusive a coordenadoria e o órgão filho do vínculo. Em termos de
negócio, a mesma tela aberta a partir de outra rotina pode abrir em consulta onde o servidor
esperava alterar.

A tela também é uma estação de passagem: se a origem deixou o código da próxima tela, esta
tela não mantém nada e entrega a vez à tela indicada.

[?] Nenhum programa desta jornada escreve esse código de próxima tela, e a navegação desta
jornada termina aqui. Se existe uma rotina do sistema que abre esta tela com a próxima já
definida — e em que caso — não está no material lido. Pergunta ao site.

### RN-03 — A tela se identifica por dez campos

A tela trabalha com dez campos de identificação: o **órgão filho** e a **coordenadoria
regional escolar** (que dizem de que unidade é a movimentação), o **mês** e o **ano de
referência** (o mês de que se está falando), e as datas de **início** e de **limite** do
período — cada uma com dia, mês e ano.

O sistema confere cada um deles como número; o que não passa nessa conferência é recusado e
o cursor volta ao campo.

### RN-04 — O órgão tem de estar na alçada do vínculo do servidor

O vínculo do servidor limita o que ele alcança, em três conferências independentes. O órgão
informado tem de ser o **órgão permitido do vínculo**, quando o vínculo traz um; outro é
recusado com **\* Usuario sem acesso a outro orgao \***. O órgão tem de ser da **secretaria
do vínculo**, senão **\* Orgao nao pertence a esta secretaria \***. E, quando o vínculo traz
uma coordenadoria, o órgão tem de ser daquela coordenadoria — o que se compara é a
coordenadoria do **cadastro do órgão**, não a digitada —, senão
**\* Usuario sem acesso ao grupo deste orgao \***. Nas três recusas o cursor volta ao campo
do órgão.

### RN-05 — O órgão tem de estar cadastrado e com os dados completos

O órgão filho é obrigatório: em branco, a recusa é **\* Informe o orgao \***, com o cursor no
campo. Informado, o sistema lê o cadastro de órgãos (C020T) e recusa de três formas: se o
órgão não existir **ou estiver marcado como excluído**,
**\* Orgao nao cadastrado \***; se existir e lhe faltar o bairro, o órgão pai, o nome, o
endereço, o número de matriculados ou o número de pessoas,
**\* Orgao cadastrado com dados incompletos \***. Qualquer uma delas devolve o cursor ao
campo do órgão e encerra a passagem.

Passando por tudo, é o cadastro que manda: o nome do órgão e a coordenadoria passam a ser os
do cadastro, e o que o servidor tiver digitado na coordenadoria é reescrito.

### RN-06 — A consulta e a exclusão exigem matrícula de quem já entrou

A tela não atende quem chega sem matrícula na sessão: sem ela, o sistema não faz nada do que
esta tela faz.

[?] Não encontrei no material desta jornada onde a matrícula entra e qual a mensagem que o
servidor vê nesse caso. Parece conferência da entrada do sistema. Pergunta ao site.

### RN-07 — O mês e o ano de referência não são herdados do menu

Quem informa o mês e o ano de referência é esta tela, não o menu. Em branco — ou zerados — a
recusa é **\* Informe o Mes/Ano \***, com o cursor no mês. Informados, o par tem de formar
uma data de calendário válida do sistema, senão **\* Mes/Ano invalidos \***, também com o
cursor no mês. Na inclusão, o par ainda tem de constar da **tabela de períodos do mapa**
(C171T) — senão **\* Mes/Ano nao cadastr.na tab.de periodos do mapa \***, com o cursor no
mês.

### RN-08 — A inclusão só entra em mês aberto, e a exclusão só sai em mês fechado

A tela trata a situação do mês como uma marca de duas posições, e as duas operações exigem
marcas opostas:

- a **inclusão** exige o mês **aberto** — fechado, recusa com
  **\* Movimentacao fechada. Reabra antes da inclusao \***, com o cursor no mês;
- a **exclusão** exige o mês **fechado** — aberto, recusa com
  **\* Movimentacao fechada para este Mes/Ano \***, com o cursor no mês.

A marca do mês não é digitada nesta tela e não é um campo comum a todas as linhas do mês: ela
é parte da chave do próprio mês (um mês fechado e um mês aberto convivem no cadastro, cada um
com as suas linhas).

A mesma conferência vale para cada linha da movimentação: a tela trabalha as linhas em
passagens sucessivas, todas sujeitas à conferência do mês.

[?] Aqui a conferência e o que grava não fecham. A montagem do mês, nesta tela, **só grava a
marca de fechado** — a leitura que a inclusão faz desse mesmo mês pede a marca de aberto, e
é a rotina que abre a marca que a tela consulta para decidir se pode incluir. Com os valores
deste programa, a inclusão nunca passa dessa conferência: o valor que ela aceita não é o
valor que o próprio programa escreve. Some-se a isso que a recusa da exclusão
(**Movimentacao fechada para este Mes/Ano**) exige a marca **diferente** de fechado com a
linha já cadastrada — e a única gravação da marca é a de fechado. Ou a marca de aberto é
gravada por outra tela do sistema — a `M060T` grava essa marca, e é outra tela do mesmo menu
— ou as duas conferências nunca foram satisfeitas. **A inclusão é inalcançável por este
caminho.** Pergunta ao site.

### RN-09 — O período de lançamento vem da tabela de períodos do mapa

As datas de início e de limite do período não são digitadas para valer: a tela as preenche
com o período do mês de referência que está na tabela de períodos do mapa (C171T) — início e
limite no mesmo ano da referência. O que o servidor digitar nesses campos não entra na
movimentação; serve só para a edição numérica.

O cadastro de movimentação guarda o mês e o ano de referência, não as datas do período — por
isso essas datas são apresentadas, mas não são gravadas na linha.

### RN-10 — Passando o mês, quem foi excluído do cadastro deixa de existir para a operação

As leituras que sustentam a consulta e a exclusão ignoram os registros marcados como
excluídos. Na prática, um mês inteiro que foi excluído passa a **não existir** para estas
operações: a consulta não o encontra, a exclusão não o encontra para excluir de novo, e os
órgãos marcados como excluídos no cadastro de órgãos não aparecem nas descrições.

### RN-11 — Incluir exige a linha inteira: ocorrência, destino, fornecedor, nota, gênero, quantidade e valor

Na inclusão, nesta ordem: a **ocorrência** é obrigatória e vai de 1 a 4 — acima disso,
**\* Ocorrencia invalida \***, com o cursor na ocorrência da linha. Nas ocorrências **1 e 2**
(remanejamento e recebimento) o **órgão de destino** é obrigatório — **\* Informe o Orgao de
destino \*** —; nas ocorrências **3 e 4** ele não é exigido, mas, se informado, passa pelas
conferências do órgão. O destino tem de existir e não estar excluído —
**\* Orgao nao cadastrado \*** — e ser da secretaria do vínculo —
**\* Orgao nao pertence a esta secretaria \***. Depois, o **fornecedor** é obrigatório —
**\* Informe o fornecedor \*** — e tem de existir no cadastro de fornecedores (C030T) —
**\* Fornecedor nao cadastrado \***; a **nota fiscal** é obrigatória —
**\* Informe o numero da nota fiscal \***; a **subclasse** e o **gênero** são obrigatórios —
**\* Informe o codigo do genero \*** — e o par tem de estar cadastrado no cadastro de gêneros
(C051T) — **\* Genero nao cadastrado \*** —, procurado pelo par **vigente no mês de
referência**, no dia 1; a **quantidade** — **\* Informe a quantidade \*** — e o **valor** —
**\* Informe o valor \*** — não podem ficar zerados. Cada recusa devolve o cursor ao campo da
própria linha.

### RN-12 — A exclusão exige consulta prévia do mesmo mês e do mesmo órgão

Para excluir, a operação tem de ser a de exclusão e o **órgão e o mês/ano informados** têm de
ser os da última operação feita nesta sessão — a consulta que a antecedeu —, senão
**\* Consulte antes de excluir \***, com o cursor no campo da operação. É a tela que obriga a
passar primeiro pelo modo de consulta.

### RN-13 — A exclusão exclui a linha, não o mês

Passando as conferências, a exclusão **não apaga a movimentação do mês**: ela marca como
excluída a linha que o servidor marcou para exclusão. Marcar uma linha **vazia** é recusado
com **\* Exclua linha preenchida \***; marcar uma linha que **não existe** naquele mês é
recusado com **\* Movimentacao nao cadastrada para este Mes/Ano \***, com o cursor na
marcação da linha. A linha excluída fica marcada e passa a não ser encontrada pelas leituras
do mês (RN-10).

A exclusão sem nenhuma linha marcada termina em silêncio: as conferências do mês são feitas,
e como a única exclusão que existe é a da linha marcada, nada é gravado e nenhum aviso
aparece.

### RN-14 — Nada é lido nem gravado sem as conferências de tela, de acesso e de permissão

A abertura da tela e cada passagem passam antes pelas conferências do sistema: a de **tela**
(a estação da sessão e o cadastro de telas e acessos), a de **rota** (a tela existe e não
está excluída) e a de **permissão por operação** (o acesso libera a inclusão, a exclusão e a
consulta nesta tela). Se qualquer uma não liberar, a passagem termina sem ler e sem gravar
cadastro.

### RN-15 — A exclusão registra quem excluiu e quando

A linha excluída não é apagada: ela recebe a data e a hora da operação, a estação, a
matrícula de quem excluiu e a operação — e a situação do mês daquela linha é zerada. É esse
registro que permite dizer depois quem tirou a linha do mapa, e quando.

### RN-16 — A consulta mostra o mês e as suas linhas, e não grava nada

Na consulta, a tela apresenta a situação do mês — **ABERTO** ou **FECHADO** — e as linhas da
movimentação, cada uma com o nome do órgão de destino, o nome da ocorrência (remanejamento,
recebimento, determinação ou extra), a razão social do fornecedor, a quantidade, o valor e o
gênero. Os campos que o servidor não informou aparecem preenchidos pela tela com o que foi
lido do cadastro.

A consulta **não grava nada** — nem linha, nem auditoria. É a única das três operações que só
lê.

### RN-17 — O mês sem movimentação é recusado na consulta

Consultando um mês que **não tem** movimentação cadastrada para aquele órgão e aquela
coordenadoria, a tela recusa com
**\* Nao existem movimentacoes cad.neste Mes/Ano \***, com o cursor no mês. E, encontrando a
movimentação do mês mas não a linha procurada, informa
**\* Orgao sem movimentacao de estoque no Mes/Ano \***.

### RN-18 — Toda inclusão e toda exclusão confirmadas ficam na auditoria

Toda inclusão e toda exclusão que chegou ao fim deixam um registro no **cadastro de
auditoria** (A010T): o que foi a operação, em que tela, com que matrícula, em que estação e
em que momento, com o registro de antes e o registro depois da movimentação. É essa trilha
que responde, depois, quem mexeu no mapa.

### RN-19 — O momento da gravação é o do relógio do sistema

A tela apresenta a **data do sistema**, e a data e a hora que a linha recebe ao ser gravada
ou excluída são as do relógio do sistema no momento da operação — não são informadas pelo
servidor nem vêm de campo nenhum da tela.

---

## Cenários BDD

```gherkin
Funcionalidade: Manutenção da movimentação de estoque do mês de referência de um órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M030T

  Cenário: Consulta da movimentação do mês
    Dado que estou com a operação de consulta e informei o órgão e o mês de referência
    Quando confirmo
    Então vejo a situação do mês, ABERTO ou FECHADO
    E vejo as linhas da movimentação com o órgão de destino, a ocorrência, o fornecedor, a
      quantidade, o valor e o gênero
    E nada é gravado

  Cenário: Inclusão de uma linha de movimentação
    Dado que estou com a operação de inclusão
    E o mês de referência está aberto
    Quando informo a ocorrência, o órgão de destino, o fornecedor, a nota fiscal, o gênero,
      a quantidade e o valor
    Então a linha é gravada na movimentação daquele mês
    E fica registrada na auditoria quem incluiu e quando

  Cenário: Operação não disponível
    Dado que a tela que me encaminhou passou uma operação que não é inclusão, exclusão nem
      consulta
    Quando confirmo
    Então vejo a mensagem "* Operacao nao disponivel. Use INC, EXC ou CON *"
    E o cursor volta para o campo da operação
    E nada é lido nem gravado

  Cenário: Operação herdada da tela de origem
    Dado que a tela de origem passou a operação de consulta junto com o órgão
    Quando chego à tela
    Então ela abre no modo de consulta, e não no modo de inclusão
    E não me deixa lançar linha nenhuma nessa passagem

  Cenário: Campo do órgão não é número
    Quando informo um órgão que não é número
    Então a tela recusa o campo antes de consultar o cadastro
    E o cursor volta para o campo

  Cenário: Órgão fora da minha secretaria
    Dado que informo um órgão de outra secretaria
    Quando confirmo
    Então vejo "* Orgao nao pertence a esta secretaria *"
    E o cursor volta para o campo do órgão

  Cenário: Órgão fora da minha coordenadoria
    Dado que o meu vínculo tem uma coordenadoria
    E informo um órgão de outra coordenadoria
    Quando confirmo
    Então vejo "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor volta para o campo do órgão

  Cenário: Órgão não é o permitido pelo meu vínculo
    Dado que o meu vínculo traz um órgão permitido
    E informo outro órgão
    Quando confirmo
    Então vejo "* Usuario sem acesso a outro orgao *"
    E o cursor volta para o campo do órgão

  Cenário: Órgão não informado
    Quando deixo o órgão em branco
    Então vejo "* Informe o orgao *"
    E o cursor volta para o campo do órgão

  Cenário: Órgão não cadastrado
    Quando informo um órgão que não existe no cadastro
    Então vejo "* Orgao nao cadastrado *"
    E o cursor volta para o campo do órgão

  Cenário: Órgão excluído não conta como cadastrado
    Dado que o órgão informado está marcado como excluído no cadastro
    Quando confirmo
    Então vejo "* Orgao nao cadastrado *"
    E nada mais é lido nem gravado

  Cenário: Órgão com cadastro incompleto
    Dado que falta ao órgão o bairro, o órgão pai, o nome, o endereço, o número de
      matriculados ou o número de pessoas
    Quando confirmo
    Então vejo "* Orgao cadastrado com dados incompletos *"
    E o cursor volta para o campo do órgão

  Cenário: Mês e ano de referência não informados
    Quando deixo o mês e o ano de referência em branco
    Então vejo "* Informe o Mes/Ano *"
    E o cursor volta para o campo do mês

  Cenário: Mês e ano de referência inválidos
    Quando informo um mês e um ano que não formam uma data válida
    Então vejo "* Mes/Ano invalidos *"
    E o cursor volta para o campo do mês

  Cenário: Mês de referência fora da tabela de períodos
    Dado que estou com a operação de inclusão
    E informo um mês e um ano que não estão na tabela de períodos do mapa
    Quando confirmo
    Então vejo "* Mes/Ano nao cadastr.na tab.de periodos do mapa *"
    E o cursor volta para o campo do mês
    E nada é gravado

  Cenário: Inclusão em mês fechado
    Dado que estou com a operação de inclusão
    E a movimentação daquele mês está fechada
    Quando confirmo
    Então vejo "* Movimentacao fechada. Reabra antes da inclusao *"
    E o cursor volta para o campo do mês
    E nada é gravado

  Cenário: O mês se fecha sozinho quando o mês seguinte é lançado
    Dado que estou com a operação de inclusão
    E existe movimentação do mês anterior
    Quando a passagem chega ao fim sem recusa
    Então a movimentação do mês anterior passa a fechada
    E aquele mês deixa de aceitar inclusão e exclusão nesta tela

  Cenário: Exclusão sem consulta prévia
    Dado que estou com a operação de exclusão
    E o órgão ou o mês informados não são os que eu consultei antes
    Quando confirmo
    Então vejo "* Consulte antes de excluir *"
    E o cursor volta para o campo da operação

  Cenário: Exclusão de um mês sem movimentação
    Dado que estou com a operação de exclusão
    E consultei um órgão e um mês que não têm movimentação cadastrada
    Quando confirmo a exclusão
    Então vejo "* Nao existem movimentacoes cad.neste Mes/Ano *"
    E o cursor volta para o campo do mês

  Cenário: Linha vazia marcada para exclusão
    Dado que estou com a operação de exclusão
    Quando marco para exclusão uma linha que está vazia
    Então vejo "* Exclua linha preenchida *"
    E o cursor volta para a marcação da linha

  Cenário: Linha marcada para exclusão não existe naquele mês
    Dado que estou com a operação de exclusão
    Quando marco para exclusão uma linha que não está cadastrada naquele mês
    Então vejo "* Movimentacao nao cadastrada para este Mes/Ano *"
    E o cursor volta para a marcação da linha

  Cenário: Inclusão sem a ocorrência da linha
    Dado que estou com a operação de inclusão
    Quando informo uma ocorrência acima de 4
    Então vejo "* Ocorrencia invalida *"
    E o cursor volta para a ocorrência da linha
    E a linha não é gravada

  Cenário: Órgão de destino não informado
    Dado que estou com a operação de inclusão
    E a ocorrência da linha é de remanejamento ou de recebimento
    Quando deixo o órgão de destino em branco
    Então vejo "* Informe o Orgao de destino *"
    E o cursor volta para o campo da linha
    E a linha não é gravada

  Cenário: Fornecedor não cadastrado
    Dado que estou com a operação de inclusão
    Quando informo um fornecedor que não existe no cadastro
    Então vejo "* Fornecedor nao cadastrado *"
    E a linha não é gravada

  Cenário: Gênero não cadastrado no mês de referência
    Dado que estou com a operação de inclusão
    Quando informo um par de subclasse e gênero que não existe para aquele mês
    Então vejo "* Genero nao cadastrado *"
    E a linha não é gravada

  Cenário: Quantidade da linha zerada
    Dado que estou com a operação de inclusão
    Quando deixo a quantidade zerada
    Então vejo "* Informe a quantidade *"
    E a linha não é gravada

  Cenário: Valor da linha zerado
    Dado que estou com a operação de inclusão
    Quando deixo o valor zerado
    Então vejo "* Informe o valor *"
    E a linha não é gravada
```
