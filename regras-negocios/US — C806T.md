# US — C806T — Manter os feriados do órgão

## Estória

Como **servidor de CRE**, quero **manter os feriados do meu órgão — o dia, o mês, o
ano e a descrição de cada um**, para que **o cálculo do período da alimentação
escolar conte os dias do meu órgão como eles são, e não como uma sequência de dias
comuns**.

O feriado é o dia em que o órgão não funciona, e quem depende disto é o cálculo do
período: ao montar o calendário de um período, ele percorre os feriados do órgão e
marca os que caem dentro daquele período, como já trata os fins de semana. Sem o
feriado cadastrado, o cálculo enxerga um dia comum — e o resultado do período sai
contando um dia em que não houve atendimento. O cadastro é do órgão de quem o
mantém: cada órgão tem o seu próprio calendário de feriados, e nenhum serve para
outro.

## Contexto

Jornada S000M → C000M → C800M → C806T.
Ator: servidor de CRE — mantém os feriados do próprio órgão, um a um, identificados
pela data.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O contexto que a tela usa — o órgão da
sessão, a matrícula funcional, o código de acesso, o privilégio e a CRE — é o que a
entrada deixou na sessão.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela mantém o calendário de feriados de um órgão

A tela mantém o cadastro de feriados do órgão de quem a está usando. Cada feriado é
identificado pelo **órgão** e pela **data** — dia (2 dígitos), mês (2) e ano (4) — e
guarda a **descrição**, de até 40 caracteres, que é o nome do feriado e o único dado
de preenchimento obrigatório. O órgão não é informado nesta tela: é o órgão da sessão
do servidor, de modo que o feriado que ele cadastra entra no calendário do seu órgão
e de mais nenhum. A capacidade declarada do cadastro é de **100.000 registros** —
parâmetro de dimensionamento, não volume cadastrado.

O cadastro guarda também um terceiro dado, além da data e da descrição, e esta tela
não o mostra nem permite alterá-lo; nesta jornada nenhuma outra tela o mantém.

[?] A tela abre exigindo que o **código de acesso** e a **origem** estejam
preenchidos, e, se qualquer um dos dois estiver em branco, abandona a transação sem
processar linha nenhuma e sem mensagem. O lote não mostra quem preenche a origem nem
para que serve essa saída — e, como o único caminho até a tela no acervo é uma opção
de menu, que é justamente o caminho em que a origem pode chegar em branco, não se
conclui se a tela é alcançável nesse caminho. Pergunta ao site.

### RN-02 — A tela só aceita as opções de alteração e de consulta

A tela tem uma **opção de manutenção**. Se a opção informada for diferente de
**alteração (ALT)** e de **consulta (CON)**, o sistema recusa com
**\* Opcao nao disponivel. Use ALT ou CON \***, devolve o cursor ao campo da opção e
não confere nem grava linha nenhuma. Esse é o desfecho de qualquer terceira opção —
inclusive das que a máscara venha a oferecer.

[?] A correspondência entre os rótulos que a mensagem manda usar (ALT e CON) e os
códigos internos de alteração e de consulta que a guarda compara não está verificada:
ou o ambiente traduz o que o servidor digita, ou a mensagem está desalinhada da
guarda. É a mesma dúvida já registrada nas telas irmãs deste módulo. Pergunta ao site.

[?] Não se sabe, pelo lote, com que valor o campo da opção chega preenchido quando a
tela é aberta: a máscara da tela não está no lote, e o programa, ao abrir, só repõe
uma referência interna de posição. Se a opção chegar em branco, a tela é recusada por
esta mesma guarda. Pergunta ao site.

### RN-03 — A tela lista os feriados do órgão, em páginas de 14 linhas

A tela mostra os feriados do órgão em **até 14 linhas** por vez, cada linha com o
dia, o mês, o ano e a descrição. A lista parte de uma **data de referência**: na
primeira abertura são o ano e o mês do dia do sistema, e a data em que a lista parou
fica guardada na sessão para as aberturas seguintes. A referência também é um campo
da tela, no pé do formulário: é o período do calendário de feriados que o servidor
está vendo, e o que a tela passar a mostrar em seguida parte dela.

Quando a leitura não encontra feriado a partir daquela referência, a tela avisa
**\* Nao existem feriados cadastrados \*** e devolve o cursor ao campo do dia da
primeira linha.

[?] O aviso aparece quando não há feriado **a partir da referência**; existindo
feriados anteriores a ela, o fonte não permite concluir se o aviso ainda sai — quem
decide isso é a leitura, que é do ambiente e não do programa. Pergunta ao site.

[?] Se a data de referência é digitável pelo servidor, e com que rótulo, depende da
máscara da tela, que não está neste lote. Pergunta ao site.

### RN-04 — A marca de cada linha diz o que fazer com ela

Cada linha tem uma **marca de ação**: **I** inclui, **A** altera e **E** exclui.
Linha sem dia informado, ou com marca diferente de I, A e E, é ignorada — não gera
operação nenhuma. A marca é traduzida na operação correspondente e é ela que decide
o que a tela vai fazer com aquela linha; na hora de gravar, a marca e o dia são
conferidos de novo.

O servidor também vê uma linha já cadastrada preenchida com a data e a descrição do
feriado; uma data informada que não tem feriado aparece em branco, com o campo de
descrição livre para o texto novo.

[?] A marca só produz efeito no modo de alteração: na consulta o fluxo termina antes
de qualquer gravação. Se a máscara deixa digitar a marca em consulta, o que o
servidor espera ver é pergunta ao site.

### RN-05 — Inclusão: a data não pode ter feriado, tem de ser válida, e a descrição é obrigatória

Para incluir, o sistema procura a data informada no calendário do órgão. Já existindo
feriado naquela data, a inclusão é recusada com **\* Feriado ja cadastrado \***, com o
cursor de volta ao campo da marca. Não existindo, a data é conferida: o dia, o mês e
o ano têm de formar uma data do calendário e o ano tem de estar entre **1994** e
**2099**; não formando, ou estando o ano fora do intervalo, a recusa é
**\* Data invalida \***, com o cursor de volta ao campo do dia. Por fim, a descrição é
obrigatória: em branco, a recusa é **\* Informe a descricao \***, com o cursor de
volta ao campo da descrição. Passando nas três conferências, o feriado é gravado para
o órgão da sessão.

[?] O ano é conferido contra limites fixos (1994 e 2099) e o programa também calcula o
ano do dia do sistema, sem o comparar com nada. Se a intenção era recusar data
anterior a hoje, ou se o intervalo fixo é a regra, é pergunta ao site.

[?] A repetição de data só é recusada por esta conferência: no dicionário a chave do
calendário admite duplicados. Se duas datas iguais podem conviver no mesmo órgão por
outro caminho — outra tela, carga ou rotina de processamento —, é pergunta ao site.

### RN-06 — Alteração: o feriado tem de existir e só a descrição muda

Para alterar, o feriado precisa existir na data informada — senão o sistema recusa
com **\* Feriado nao cadastrado \*** e o cursor volta ao campo da marca. Existindo, a
descrição é obrigatória (a mesma recusa **\* Informe a descricao \*** se estiver em
branco) e o registro é travado e regravado com a nova descrição. O órgão e a data são
a identificação do feriado: a alteração não os muda. Para mudar a data, o servidor
exclui o feriado e inclui outro.

### RN-07 — Exclusão: o feriado tem de existir e a descrição não é exigida

Para excluir, o feriado precisa existir na data informada — senão a recusa é
**\* Feriado nao cadastrado \***. Existindo, o registro é travado e excluído; nesse
caminho a descrição não é conferida, e o servidor pode excluir deixando-a em branco.

### RN-08 — A consulta não grava nada

Na consulta a tela lista e para: nenhuma linha é conferida, gravada, alterada ou
excluída, e nenhum registro de auditoria é gerado.

### RN-09 — Toda gravação deixa rastro na auditoria

Inclusão, alteração e exclusão gravam, além do feriado, um registro de auditoria com
a tela de origem, o cadastro que originou a operação, a operação (inclusão, alteração
ou exclusão), a matrícula do servidor, a estação, a sessão (ano, mês, dia e hora), o
tipo de órgão, a CRE, o órgão e os valores anterior e posterior — a inclusão sem valor
anterior e a exclusão sem valor posterior.

[?] O número do processo do registro de auditoria recebe o **dia do feriado**, e não
um número de processo da operação. Se é o campo próprio da auditoria sendo
aproveitado, ou um engano, é pergunta ao site.

### RN-10 — O cálculo do período consome os feriados e marca o que já consumiu

O cálculo do período da alimentação escolar percorre os feriados do órgão dentro do
período pedido e, para cada um, monta a data e a compara com o limite do período: o
que cai dentro do período é consumido pelo cálculo e **marcado como já consumido**. A
marca é interna do processamento — esta tela não a mostra nem deixa mexer nela — e a
rotina que refaz o cálculo a limpa antes de começar, de modo que o mesmo feriado pode
ser consumido de novo.

[?] O que exatamente o processamento marca, e o que a marca impede enquanto está
posta, não se lê no lote desta jornada: as telas que disparam esse processamento não
fazem parte dela. Quem lê a estória isolada fica sem saber se a marca é só controle
de execução ou se ela bloqueia alguma coisa. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os feriados do órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E o meu vínculo tem o órgão, a CRE e o código de acesso que a tela usa
    E tenho acesso à tela C806T

  Cenário: Consulta lista os feriados do órgão, em páginas de 14 linhas
    Dado que estou na C806T em modo de consulta
    Quando a tela abre
    Então vejo os feriados do meu órgão, com dia, mês, ano e descrição
    E vejo no máximo 14 feriados por vez
    E nada é gravado

  Cenário: Órgão sem feriados a partir do período de referência
    Dado que não há feriado cadastrado para o meu órgão a partir da data de referência
    Quando abro a C806T
    Então vejo a mensagem "* Nao existem feriados cadastrados *"
    E o cursor fica no campo do dia da primeira linha

  Cenário: A data de referência é informada e a lista segue a partir dela
    Dado que estou na C806T com um período de referência informado
    Quando o sistema recarrega a lista
    Então os feriados que vejo partem daquela data
    E o período informado fica guardado para as telas seguintes

  Cenário: Opção de manutenção indisponível
    Quando informo uma opção de manutenção diferente de ALT e de CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta para o campo da opção
    E nenhuma linha é conferida ou gravada

  Cenário: Linha sem data ou com marca desconhecida é ignorada
    Dado que preenchi uma linha sem o dia, ou com uma marca diferente de I, A e E
    Quando a tela processa as linhas
    Então aquela linha não gera operação nenhuma

  Cenário: Inclusão de um feriado novo
    Dado que estou na C806T com a opção em ALT
    E não há feriado na data que vou informar
    Quando informo o dia, o mês, o ano e a descrição, com a marca I na linha
    Então o feriado é gravado para o órgão da minha sessão
    E a operação fica registrada na auditoria

  Cenário: Inclusão em data que já tem feriado
    Dado que já existe feriado na data informada, no meu órgão
    Quando tento incluir com a marca I
    Então vejo a mensagem "* Feriado ja cadastrado *"
    E o cursor volta para o campo da marca
    E nada é gravado

  Cenário: Data que não existe no calendário
    Dado que informo um dia, um mês e um ano que não formam data do calendário
    Quando tento incluir com a marca I
    Então vejo a mensagem "* Data invalida *"
    E o cursor volta para o campo do dia
    E nada é gravado

  Cenário: Ano do feriado fora do intervalo aceito
    Dado que informo uma data com o ano anterior a 1994 ou posterior a 2099
    Quando tento incluir com a marca I
    Então vejo a mensagem "* Data invalida *"
    E o cursor volta para o campo do dia
    E nada é gravado

  Cenário: Inclusão sem descrição
    Dado que informo a data de um feriado novo e deixo a descrição em branco
    Quando tento incluir com a marca I
    Então vejo a mensagem "* Informe a descricao *"
    E o cursor volta para o campo da descrição
    E nada é gravado

  Cenário: Alteração da descrição de um feriado
    Dado que existe feriado na data informada
    Quando informo a nova descrição com a marca A
    Então o sistema regrava o feriado com a nova descrição
    E o órgão e a data do feriado continuam os mesmos
    E a operação fica registrada na auditoria

  Cenário: Alteração sem descrição
    Dado que existe feriado na data informada
    Quando tento alterar com a marca A deixando a descrição em branco
    Então vejo a mensagem "* Informe a descricao *"
    E nada é gravado

  Cenário: Alteração de feriado não cadastrado
    Dado que não existe feriado na data informada
    Quando tento alterar com a marca A
    Então vejo a mensagem "* Feriado nao cadastrado *"
    E o cursor volta para o campo da marca
    E nada é gravado

  Cenário: Exclusão de um feriado
    Dado que existe feriado na data informada
    Quando informo a marca E, mesmo com a descrição em branco
    Então o sistema trava e exclui o feriado
    E a operação fica registrada na auditoria

  Cenário: Exclusão de feriado não cadastrado
    Dado que não existe feriado na data informada
    Quando tento excluir com a marca E
    Então vejo a mensagem "* Feriado nao cadastrado *"
    E o cursor volta para o campo da marca
    E o feriado continua cadastrado

  Cenário: Consulta não grava nada
    Dado que estou na C806T com a opção em CON
    Quando informo data, descrição e marca em uma linha
    Então nenhuma linha é conferida, gravada, alterada ou excluída
    E nenhum registro de auditoria é gerado

  Cenário: Operação não autorizada pelo perfil
    Dado que o meu código de acesso não tem o flag da operação pretendida
    Quando tento incluir, alterar ou excluir
    Então o sistema recusa a operação, sem mensagem na tela
    E nada é gravado

  Cenário: O cálculo do período marca o feriado que consumiu
    Dado que registrei um feriado do meu órgão dentro de um período
    Quando o cálculo do período da alimentação escolar é processado
    Então aquele feriado é consumido pelo cálculo
    E fica marcado como já consumido, sem que eu veja isso nesta tela
```
