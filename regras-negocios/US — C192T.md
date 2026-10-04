# US — C192T — Manter o calendário de feriados do órgão

## Estória

Como **servidor de CRE**, quero **manter o calendário de feriados do tipo de órgão da
minha sessão — o dia, o mês, o ano e a descrição de cada data**, para que **as telas
que marcam entrega e merenda não tratem como dia comum o dia em que o órgão não
funciona**.

Este calendário é o que as outras telas do sistema consultam para saber em que dias o
órgão para. Ao calcular as **datas previstas de entrega** de um pedido, o sistema pula
os dias registrados aqui, como já pula sábados e domingos; e, num dia registrado aqui,
as telas de pedido recusam marcar o início ou o fim da entrega e as telas de merenda
recusam informar comensais. Sem o feriado cadastrado, o dia passa por dia comum — a
entrega é marcada e a merenda é lançada num dia em que o órgão não funciona.

O calendário é do **tipo de órgão**, não do servidor: quem tem o vínculo de um tipo de
órgão mantém o calendário daquele tipo, e as telas que consultam os feriados usam o
tipo de órgão da própria sessão. A descrição de cada data também não é enfeite: há
palavras que o processamento da merenda lê ao pé da letra, e é por elas que o dia
recebe um tratamento diferente do de feriado (RN-14).

## Contexto

Jornada S000M → C000M → C020M → C192T.
Ator: servidor de CRE — mantém, para o tipo de órgão do seu vínculo, o calendário de
feriados que as outras telas consultam.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As duas telas do meio do caminho são menus: elas não deixam registro nem operação para
a tela de destino, apenas dizem qual tela abrir. A C192T é a última tela da jornada e
não entrega nada a nenhuma outra — não passa registro nem operação adiante. Como o menu
também não deixa modo, é a própria tela que decide o modo em que abre. O que ela usa é
o que a entrada deixou na sessão: a matrícula funcional, o código de acesso, o
privilégio, o tipo de órgão e a coordenação regional escolar. O tipo de órgão é o dono
do calendário e não se digita nesta tela.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O calendário é do tipo de órgão, e cada feriado é uma data com descrição

A tela mantém o **cadastro de feriados (C193T)**. Cada feriado é identificado pelo
**tipo de órgão** e pela **data** — dia (2 dígitos), mês (2) e ano (4) — e guarda a
**descrição**, de até 40 caracteres, que é o único dado de preenchimento obrigatório. O
tipo de órgão não é digitado: é o do vínculo da sessão, de modo que cada tipo de órgão
tem o seu próprio calendário. No dicionário o cadastro tem **5 campos**, e a capacidade
declarada é de **10.000 registros** — parâmetro de dimensionamento, não volume
cadastrado.

A tela exibe ainda, no alto, a identificação do tipo de órgão da sessão e a data do
sistema.

[?] O mesmo assunto existe num segundo cadastro de feriados, com a mesma chave de data
e um indicador a mais, mantido por outra tela (a C806T). Nesta jornada nenhum programa
lê os dois. Se os dois cadastros devem continuar existindo, ou qual deles é o oficial,
é decisão de negócio. Pergunta ao site.

[?] A chave do cadastro admite datas repetidas para o mesmo tipo de órgão; é a própria
tela que recusa a repetição (RN-07). Se outra entrada no cadastro pode criar duas
datas iguais para o mesmo tipo de órgão, é pergunta ao site.

### RN-02 — As seis datas digitadas passam pela conferência numérica

Antes de qualquer consulta, os **seis campos de data** da tela — dia, mês e ano do
feriado e dia, mês e ano da data de referência (RN-04) — passam pela conferência
numérica: campo em branco vira zero, os zeros à esquerda são descartados e o que não
for número é recusado, com o cursor devolvido ao campo. O que não passa por essa
conferência não chega ao cadastro.

### RN-03 — A tela abre em consulta e só aceita alteração e consulta

Ao abrir, a tela assume **consulta (CON)**: é ela mesma que preenche a opção de
manutenção com o código de consulta. Se a opção informada for diferente de **alteração
(ALT)** e de **consulta (CON)**, o sistema recusa com **\* Opcao nao disponivel. Use
ALT ou CON \***, devolve o cursor ao campo da opção e não confere nem grava linha
nenhuma.

[?] A mensagem nomeia ALT e CON, e a guarda compara com outros dois códigos; a tradução
entre o que o servidor digita e o código conferido depende da máscara da tela, que não
está no material lido. Pergunta ao site.

### RN-04 — A lista traz até 14 feriados, a partir de uma data de referência

A tela lista os feriados do tipo de órgão em **14 linhas**, e cada linha traz o dia, o
mês, o ano e a descrição. A leitura parte de uma **data de referência**: na primeira
abertura são o **ano e o mês do sistema**; não achando feriado nessa posição, a
referência é zerada. A posição alcançada volta para o campo de referência da tela.

[?] A leitura do cadastro é feita por uma rotina do ambiente, com indicadores de
posicionamento que o fonte não explica e que o corpus não documenta; o que está no
fonte é a referência com que a leitura é pedida. Se a rotina obedece à referência ou
devolve sempre o primeiro feriado do órgão, não se conclui daqui — e isso muda o que o
servidor vê na primeira abertura. Pergunta ao site.

### RN-05 — Tipo de órgão sem feriado na referência é avisado

Quando a primeira linha não encontra feriado a partir da referência, o sistema avisa
**\* Nao existem feriados cadastrados \***, posiciona o cursor no campo do dia da
primeira linha e encerra a consulta.

[?] O aviso sai quando não há feriado **a partir da referência**; havendo feriados
apenas anteriores a ela, o fonte não permite concluir se o aviso ainda aparece — quem
decide isso é a leitura, que é do ambiente. Pergunta ao site.

### RN-06 — Cada linha traz a sua marca: I inclui, A altera, E exclui; linha vazia ou marca desconhecida é ignorada

A marca é da linha, não da tela. O sistema traduz a marca na operação correspondente —
**I** vira inclusão, **A** vira alteração, **E** vira exclusão — antes de pedir a
autorização daquela operação. Linha sem dia informado, ou com marca diferente de I, A
e E, não gera operação nenhuma, e nenhuma mensagem é mostrada por isso.

### RN-07 — Inclusão: o feriado não pode existir, a data tem de valer e a descrição é obrigatória

Para incluir, o sistema procura a data informada no calendário do tipo de órgão. Já
existindo feriado naquela data, a inclusão é recusada com **\* Feriado ja cadastrado
\***, com o cursor de volta ao campo da marca. Não existindo, a data é conferida: o
dia, o mês e o ano têm de formar uma data do calendário e o ano tem de estar entre
**1994** e **2099**; não formando, ou estando o ano fora do intervalo, a recusa é
**\* Data invalida \***, com o cursor no campo do dia. Por fim, a descrição é
obrigatória: em branco, a recusa é **\* Informe a descricao \***, com o cursor no campo
da descrição. Passando pelas três conferências, o feriado é gravado para o tipo de
órgão da sessão.

### RN-08 — Alteração: o feriado tem de existir e só a descrição muda

Para alterar, o feriado precisa existir na data informada — senão o sistema recusa com
**\* Feriado nao cadastrado \***, com o cursor de volta ao campo da marca. Existindo, a
descrição é obrigatória (a mesma recusa de RN-07, se estiver em branco), o registro é
travado e regravado com a nova descrição. A data e o tipo de órgão são a identificação
do feriado: a alteração não os muda. Para mudar a data, o servidor exclui o feriado e
inclui outro.

### RN-09 — Exclusão: o feriado tem de existir e a descrição não é exigida

Para excluir, o feriado precisa existir na data informada — senão a recusa é **\*
Feriado nao cadastrado \***. Existindo, o registro é travado e excluído; nesse caminho
a descrição não é conferida.

### RN-10 — A consulta não grava nada

Na consulta a tela apenas lista: nenhuma linha é conferida, gravada, alterada ou
excluída, e nenhum registro de auditoria é gerado. A passagem que grava é desviada de
propósito quando a opção é consulta.

### RN-11 — Cada operação só grava depois de autorizada

A abertura passa pela segurança da tela e cada linha passa de novo pela segurança antes
de gravar: o sistema confere a autorização do código de acesso da sessão para aquela
tela e para **aquela** operação — inclusão, alteração e exclusão têm permissões
separadas. Sem o registro da tela, a recusa é **\* Acesso negado para esta matricula
\*** e a tela não é processada; sem a permissão da operação pedida na linha, a recusa é
**\* Acesso negado para esta operacao \*** e a linha não é gravada.

### RN-12 — Toda gravação deixa rastro na auditoria

Inclusão, alteração e exclusão gravam, além do feriado, um registro na **trilha de
auditoria (A010T)**: a tela de origem, o cadastro auditado (o cadastro de feriados), a
operação (inclusão, alteração ou exclusão), o tipo de órgão, a coordenação regional
escolar, a matrícula funcional, a estação, a sessão (ano, mês, dia e hora) e os valores
**antes e depois**. Na inclusão o "antes" fica vazio e o "depois" é o feriado novo; na
alteração os dois são o feriado, com a descrição trocada no segundo; na exclusão o
"antes" é o feriado apagado e o "depois" fica vazio.

[?] O número do processo do registro de auditoria recebe o **dia do feriado**; se é o
campo próprio da auditoria ou um aproveitamento, é pergunta ao site.

### RN-13 — Falha de banco interrompe a operação e avisa

Todo acesso a dados testa o erro do banco: a falha de leitura e a de exclusão viram o
aviso de erro de leitura, e a de gravação vira o aviso de erro de gravação —
despachados pela rotina de comunicação do sistema — e a transação para ali, sem
completar o resto.

### RN-14 — A descrição de RECESSO tem tratamento próprio no mapa diário

No processamento do **mapa diário** da merenda, a descrição gravada é comparada ao pé
da letra: o dia cuja descrição é **RECESSO** ou **RECESSO ESCOLAR** não recebe a
justificativa de feriado; os demais dias registrados no calendário recebem. A
descrição, portanto, é o que o processamento obedece — não é texto livre de enfeite.

[?] A comparação é literal: "Recesso" com outra caixa, com acento ou com espaço a mais
não é reconhecido, e não se lê no lote se a tela converte o que foi digitado. Qual é a
grafia oficial é pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter o calendário de feriados do órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E o meu vínculo tem o tipo de órgão cujo calendário eu mantenho
    E tenho acesso à tela C192T

  Cenário: RN-01 — o calendário do meu tipo de órgão
    Dado que abro a C192T
    Quando a tela carrega
    Então vejo os feriados do tipo de órgão da minha sessão, com dia, mês, ano e descrição
    E vejo no alto a identificação do tipo de órgão e a data do sistema

  Cenário: RN-02 — data que não é número
    Quando informo um dia, um mês ou um ano que não é número
    Então o sistema recusa o campo antes de consultar o cadastro
    E o cursor volta para o campo recusado

  Cenário: RN-03 — opção de manutenção indisponível
    Dado que abro a C192T
    Então a opção de manutenção já vem preenchida com consulta
    Quando informo uma opção diferente de ALT e de CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo da opção
    E nenhuma linha é conferida ou gravada

  Cenário: RN-04 — a lista traz até 14 feriados
    Dado que o tipo de órgão tem feriados cadastrados
    Quando a tela abre
    Então a lista traz até 14 feriados
    E a data de referência de onde a lista partiu aparece na tela

  Cenário: RN-05 — tipo de órgão sem feriado a partir da referência
    Dado que não há feriado para o meu tipo de órgão a partir da data de referência
    Quando abro a C192T
    Então vejo a mensagem "* Nao existem feriados cadastrados *"
    E o cursor fica no campo do dia da primeira linha

  Cenário: RN-06 — linha sem dia ou com marca desconhecida é ignorada
    Dado que preenchi uma linha sem dia, ou com marca diferente de I, A e E
    Quando confirmo a tela
    Então aquela linha não gera operação nenhuma
    E nenhuma mensagem é mostrada por isso

  Cenário: RN-07 — inclusão de um feriado novo
    Dado que estou com a opção em ALT
    E não há feriado na data que vou informar
    Quando informo o dia, o mês, o ano e a descrição, com a marca I
    Então o feriado é gravado para o tipo de órgão da minha sessão
    E a inclusão fica registrada na auditoria

  Cenário: RN-07 — inclusão em data que já tem feriado
    Dado que já existe feriado na data informada, no meu tipo de órgão
    Quando tento incluir com a marca I
    Então vejo a mensagem "* Feriado ja cadastrado *"
    E o cursor volta para o campo da marca
    E nada é gravado

  Cenário: RN-07 — data que não existe no calendário
    Dado que informo um dia e um mês que não formam data do calendário
    Quando tento incluir com a marca I
    Então vejo a mensagem "* Data invalida *"
    E o cursor volta para o campo do dia
    E nada é gravado

  Cenário: RN-07 — ano do feriado fora do intervalo aceito
    Dado que informo uma data com o ano anterior a 1994 ou posterior a 2099
    Quando tento incluir com a marca I
    Então vejo a mensagem "* Data invalida *"
    E nada é gravado

  Cenário: RN-07 — inclusão sem descrição
    Dado que informo a data de um feriado novo e deixo a descrição em branco
    Quando tento incluir com a marca I
    Então vejo a mensagem "* Informe a descricao *"
    E o cursor volta para o campo da descrição
    E nada é gravado

  Cenário: RN-08 — alteração da descrição de um feriado
    Dado que existe feriado na data informada
    Quando informo a nova descrição com a marca A
    Então o sistema regrava o feriado com a nova descrição
    E a data e o tipo de órgão do feriado continuam os mesmos
    E a alteração fica registrada na auditoria

  Cenário: RN-08 — alteração de feriado não cadastrado
    Dado que não existe feriado na data informada
    Quando tento alterar com a marca A
    Então vejo a mensagem "* Feriado nao cadastrado *"
    E o cursor volta para o campo da marca
    E nada é gravado

  Cenário: RN-08 — alteração sem descrição
    Dado que existe feriado na data informada
    Quando deixo a descrição em branco com a marca A
    Então vejo a mensagem "* Informe a descricao *"
    E nada é gravado

  Cenário: RN-09 — exclusão de um feriado
    Dado que existe feriado na data informada
    Quando informo a marca E
    Então o sistema exclui o feriado, sem exigir a descrição
    E a exclusão fica registrada na auditoria

  Cenário: RN-09 — exclusão de feriado não cadastrado
    Dado que não existe feriado na data informada
    Quando tento excluir com a marca E
    Então vejo a mensagem "* Feriado nao cadastrado *"
    E o feriado continua cadastrado

  Cenário: RN-10 — a consulta não grava nada
    Dado que estou com a opção em CON
    Quando confirmo a tela
    Então a lista é exibida
    E nenhuma linha é conferida, gravada, alterada ou excluída
    E nenhum registro de auditoria é gerado

  Cenário: RN-11 — tela não autorizada ao meu código de acesso
    Dado que o meu código de acesso não tem a tela C192T autorizada
    Quando abro a C192T
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E a tela não é processada

  Cenário: RN-11 — operação não autorizada pelo meu perfil
    Dado que o meu código de acesso não tem a permissão da operação pedida na linha
    Quando confirmo a operação
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: RN-12 — toda gravação deixa rastro na auditoria
    Dado que incluo, altero ou excluo um feriado
    Quando a operação é gravada
    Então a trilha de auditoria registra a operação, o tipo de órgão, a CRE, a minha matrícula,
      a estação e a data e a hora da sessão
    E registra os valores anterior e posterior conforme a operação

  Cenário: RN-13 — falha de banco na gravação
    Dado que a gravação do feriado falha no banco
    Quando confirmo a operação
    Então a transação é interrompida com o aviso de erro do sistema
    E o feriado não é considerado gravado

  Cenário: RN-14 — o dia descrito como recesso tem tratamento próprio no mapa
    Dado que registrei um dia com a descrição "RECESSO ESCOLAR"
    Quando o mapa diário da merenda é processado naquele dia
    Então o dia não recebe a justificativa de feriado
    E os demais dias registrados no calendário recebem
```
