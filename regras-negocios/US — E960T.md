# US — E960T — Consultar a entrega de cartões por órgão filho (SDI) da coordenação regional escolar

## Estória

Como **servidor da CRE**, quero **consultar quantos cartões foram entregues, não
entregues e cancelados em cada órgão filho (SDI) da minha coordenação, em um
contrato de referência**, para que eu saiba o que ainda falta entregar e possa
cobrar a pendência de cada órgão.

A consulta junta em uma tela só o que está espalhado em outros cadastros: as
quantidades de cartões por órgão filho, os dados do contrato (vigência, fornecedor
e situação) e os totais do contrato na coordenação. É por ela que a CRE confere,
antes de cobrar o órgão, se a entrega registrada bate com o que foi contratado. Sem
essa conferência, a cobrança sai contra o órgão errado — ou o contrato fecha sem
que ninguém veja o que ficou pendente.

## Contexto

Jornada S000M → E000M → E900M → E960T.

Ator: servidor de CRE — consulta, por coordenação regional escolar e contrato de
referência, a entrega de cartões de cada órgão filho (SDI).

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A E960T é o último passo da jornada. Ela é aberta pela E900M sem passar registro
nem operação de quem a chamou, e não encaminha para nenhuma outra tela: quem
consulta sai dela pelo menu. É tela de consulta — não grava, não altera e não
exclui nada —, e tudo o que ela mostra foi cadastrado em outras telas: o contrato
no cadastro de contratos de referência, o nome do órgão no cadastro de órgãos, o
fornecedor no cadastro de fornecedores e as quantidades de cartões na apuração que
o próprio sistema mantém.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela consulta a entrega de cartões por órgão filho (SDI) da coordenação

A tela consulta, para uma coordenação regional escolar (CRE) e um contrato de
referência — ano e número —, a situação dos cartões de cada órgão filho (SDI)
daquela coordenação. Ela mostra uma grade de **doze linhas**, e cada linha tem
**seis colunas**: o órgão filho (SDI), o nome do órgão, os cartões **entregues**,
os **não entregues**, os **cancelados** e o **total** daquele órgão. No cabeçalho
ficam a coordenação, o ano e o número do contrato, a vigência, a razão social do
fornecedor, a situação do contrato e o campo rotulado **NRPEDAUX**; abaixo da
grade, a linha dos **totais do contrato na coordenação**. Consulta-se um contrato
por vez.

[?] A grade tem doze linhas e o programa não tem, em ponto nenhum, passagem para a
página seguinte: o único dado que ele guarda de uma consulta para a outra é o campo
rotulado NRPEDAUX. Se um contrato tiver mais de doze órgãos filhos com cartões, como
o operador alcança os demais é pergunta ao site.

[?] O trecho que posiciona a lista depende de parâmetros da rotina de leitura cujo
significado não está no acervo, e o primeiro posicionamento vem do que ficou na área
de trabalho da sessão — área que a tela anterior não preenche com contrato nenhum.
Não concluo se a grade parte do primeiro órgão filho do contrato ou da posição
guardada na sessão e, portanto, se o campo NRPEDAUX serve para o operador escolher
por onde a lista começa ou é só o resto da leitura anterior. Pergunta ao site.

### RN-02 — A tela só consulta: não grava, não altera, não exclui e não abre outra tela

A E960T não muda nada. O programa traz, para os cinco cadastros que enxerga, a
rotina de gravar, a de excluir e a de travar registro — mas nenhuma delas é
executada: a tela só lê. Para o negócio, isso quer dizer que nenhuma quantidade de
cartão, contrato, órgão ou fornecedor sai desta tela, e que a consulta não deixa
trilha de auditoria. A tela também não encaminha para outra: ela não chama tela
nenhuma e não compara a tela de origem com código algum — o modo de consulta não é
decisão de quem a chamou.

[?] A tela carrega um campo com o código da próxima tela, que ela exibe e repassa:
preenchido, esse campo desvia a transmissão antes da consulta, e o desvio é
silencioso. A tela não o preenche, e quem o preencheria — se a máscara da tela ou o
cadastro de telas do site — não está no acervo. Pergunta ao site.

### RN-03 — A consulta é a única operação: qualquer outra é recusada

Ao terminar de montar a consulta, a tela deixa a opção de manutenção preenchida com
**consulta**: é a própria tela que fixa o modo. Informada outra opção, a transmissão
é recusada antes das leituras da consulta e o cursor volta ao campo da opção. A
recusa que o operador vê depende de qual conferência examina o campo primeiro: a
conferência que toda transmissão atravessa recusa com **\* Operacao nao disponivel
\***; quando ela deixa passar e é a própria tela que examina o campo — opção em
branco, por exemplo —, a recusa é **\* Operacao nao disponivel. Use CON \***.

[?] A mensagem manda usar CON, mas o código que o sistema compara é o de consulta.
Onde a máscara da tela traduz o rótulo que o operador digita no código que o
programa confere não está no acervo. Se não houver tradução, quem digitar CON é
recusado sempre — a conferência que roda antes da tela já recusa. É pergunta ao
site.

### RN-04 — A consulta só acontece com o acesso à tela e a operação autorizados

Antes de ler o contrato, a tela confere o acesso do servidor: a matrícula, o código
de acesso, o privilégio, o tipo de órgão e a coordenação da sessão vão para a
conferência de segurança, que procura o cadastro do funcionário, o cadastro da tela
e a autorização daquele código de acesso para aquela tela. Não vindo a autorização,
a consulta é interrompida: nada é lido e a grade fica como estava. Cada transmissão
passa ainda pela conferência de rota e pela autorização da operação, que confere no
perfil de acesso se a operação pedida está liberada.

### RN-05 — O servidor vinculado a uma coordenação só consulta a própria coordenação

A coordenação que a tela usa vem do vínculo do servidor com a secretaria escolhida
na entrada. Se esse vínculo tem coordenação regional escolar, é ela que a tela abre
preenchida, e informar outra é recusado com **\* Usuario sem acesso a ao grupo \***,
com o cursor de volta ao campo da coordenação. Servidor sem coordenação no vínculo
pode consultar qualquer uma. A comparação é feita sobre o contrato e a coordenação
informados, antes de qualquer leitura, e a coordenação também entra na chave com que
os cartões são procurados.

### RN-06 — O contrato é obrigatório e tem de estar cadastrado

A consulta exige o número do contrato: em branco (zero), é recusada com **\*
Informe o contrato \***. Informado, o sistema procura o contrato pelo tipo de órgão
da secretaria da sessão, pelo ano informado e pelo número informado; não achando,
recusa com **\* Contrato nao cadastrado \***, com o cursor no campo do contrato. É
esse par ano e número que identifica o contrato de referência.

### RN-07 — Contrato e grupo sem cartões: a consulta não mostra nada

Ainda que o contrato exista, é preciso que existam cartões para o grupo e o contrato
informados — a coordenação, o contrato e o órgão filho: não existindo, a consulta é
recusada com **\* Grupo/Contrato sem cartoes cadastrados \***, com o cursor no campo
da coordenação. Quando a tela é recarregada e a leitura do grupo volta vazia, o
aviso é **\* Grupo sem cartoes cadastrados \***. Nos dois casos a grade não é
preenchida.

### RN-08 — O nome do órgão e a razão social do fornecedor vêm dos cadastros

A tela não aceita esses nomes do usuário. Para cada linha da grade, o nome do órgão
filho é lido no cadastro de órgãos pelo código do órgão filho daquela linha; e a
razão social é lida no cadastro de fornecedores pelo código de fornecedor que está
no contrato. É o fornecedor do contrato — e não um informado na tela — que aparece.

### RN-09 — A vigência do contrato aparece como período

A vigência mostrada é montada das datas de início e de limite do contrato, no
formato dia/mês/ano, com as duas datas separadas por " a ". O campo de vigência tem
23 posições — exatamente as duas datas de dez caracteres e o separador no meio.

### RN-10 — O contrato fechado é destacado na tela

Quando o contrato está marcado como fechado, a situação mostrada é a palavra
**Contrato Fechado**. Nas demais situações o campo aparece todo tracejado, sem
palavra nenhuma: a tela destaca o contrato fechado e não nomeia as outras situações.

### RN-11 — Os campos informados são numéricos, e o código do fornecedor não comanda a consulta

Os **seis** campos que o operador informa — a coordenação, o número do contrato, o
ano do contrato, o código do fornecedor, o órgão filho (SDI) e o campo NRPEDAUX —
passam pela edição numérica da tela: o que não for número não chega ao cadastro e o
cursor volta ao campo. O código do fornecedor, porém, não é usado para buscar nada:
o fornecedor exibido é sempre o do contrato.

[?] O campo do código do fornecedor é digitável e é conferido como numérico, mas o
programa sempre o substitui pelo fornecedor do contrato. Ou ele serve para o
operador conferir, ou o programa ignora o que foi digitado. Pergunta ao site.

### RN-12 — Repetir a mesma consulta não relê os cadastros

Informados a mesma coordenação, o mesmo ano e o mesmo contrato da última consulta
bem-sucedida, a tela não lê os cadastros de novo: mantém o que já estava na grade e
apenas guarda o valor informado no campo NRPEDAUX. Na prática, uma segunda
confirmação com os mesmos dados não atualiza a tela, mesmo que os cartões tenham
mudado nesse intervalo.

### RN-13 — A linha de totais soma os grupos do contrato

O programa tem uma passagem que percorre os cartões do contrato e soma, para os
quatro números, as quantidades de todos os grupos — é dela que deveriam sair os
totais do contrato na coordenação, exibidos abaixo da grade.

[?] Essa soma, pelo encadeamento do próprio programa, não é alcançada: o trecho que
soma exige que o contador de linhas esteja na última, e a passagem que o chama
acabou de reiniciar o contador na primeira. Ou a guarda deve ser outra, ou o
reinício é o defeito — e, se for o defeito, os totais exibidos não são a soma dos
grupos. Não escolho um dos dois lados. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar a entrega de cartões por órgão filho (SDI) da coordenação regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E960T

  Cenário: Consulta da entrega de cartões de um contrato
    Dado que existe um contrato de referência cadastrado, com cartões para a minha coordenação
    Quando informo a coordenação e o contrato
    Então vejo até doze linhas, cada uma com o órgão filho (SDI), o nome do órgão e as quantidades de cartões entregues, não entregues, cancelados e o total
    E vejo a vigência do contrato, a razão social do fornecedor e a situação do contrato
    E nada é gravado

  Cenário: Contrato não informado
    Dado que deixei o número do contrato em branco
    Quando confirmo a consulta
    Então vejo a mensagem "* Informe o contrato *"
    E o cursor fica no campo do contrato
    E a consulta não é feita

  Cenário: Contrato não cadastrado
    Dado que informei um ano e um número de contrato que não existem para a minha secretaria
    Quando confirmo a consulta
    Então vejo a mensagem "* Contrato nao cadastrado *"
    E o cursor fica no campo do contrato
    E a grade não é preenchida

  Cenário: Contrato existente sem cartões para o grupo
    Dado que o contrato existe mas não há cartões para o grupo e o contrato informados
    Quando confirmo a consulta
    Então vejo a mensagem "* Grupo/Contrato sem cartoes cadastrados *"
    E o cursor fica no campo da coordenação
    E a grade não é preenchida

  Cenário: Grupo sem cartões ao recarregar a tela
    Dado que a última consulta ficou sem cartões
    Quando a tela é recarregada
    Então vejo a mensagem "* Grupo sem cartoes cadastrados *"
    E a grade não é preenchida

  Cenário: Opção de manutenção preenchida com outra operação
    Dado que estou na E960T
    Quando informo uma opção de manutenção diferente de consulta
    Então vejo a mensagem "* Operacao nao disponivel *"
    E o cursor volta ao campo da opção
    E nada é lido e nada é gravado

  Cenário: Opção de manutenção em branco
    Dado que estou na E960T
    Quando apago a opção de manutenção e confirmo
    Então vejo a mensagem "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E a consulta não é feita

  Cenário: Coordenação diferente da do servidor
    Dado que estou vinculado a uma coordenação regional escolar
    Quando informo outra coordenação
    Então vejo a mensagem "* Usuario sem acesso a ao grupo *"
    E o cursor fica no campo da coordenação
    E a grade não é preenchida

  Cenário: Consulta não autorizada para o acesso
    Dado que o meu código de acesso não tem autorização para a tela E960T
    Quando confirmo a consulta
    Então o sistema recusa a consulta
    E a grade fica como estava

  Cenário: Consulta não autorizada para a operação
    Dado que o meu perfil não libera a operação de consulta
    Quando confirmo a consulta
    Então o sistema recusa a consulta
    E nada é lido

  Cenário: Campo de código preenchido com o que não é número
    Dado que informei letras em um dos campos de código
    Quando confirmo a consulta
    Então o cursor volta ao campo
    E a consulta não é feita

  Cenário: Nome do órgão e fornecedor vêm dos cadastros
    Dado que consultei um contrato com cartões para a minha coordenação
    Quando vejo a grade
    Então o nome de cada órgão filho é o do cadastro de órgãos
    E a razão social é a do fornecedor que está no contrato

  Cenário: Vigência do contrato como período
    Dado que o contrato consultado tem data de início e data de limite
    Quando vejo o cabeçalho
    Então a vigência aparece como as duas datas no formato dia/mês/ano separadas por " a "

  Cenário: Contrato fechado
    Dado que o contrato consultado está fechado
    Quando confirmo a consulta
    Então a situação do contrato aparece como "Contrato Fechado"
    E as outras situações aparecem sem palavra nenhuma

  Cenário: Código do fornecedor informado não comanda a consulta
    Dado que informei um código de fornecedor
    Quando confirmo a consulta
    Então o fornecedor exibido é o do contrato
    E o código informado não é usado para buscar nada

  Cenário: Repetir a mesma consulta não relê os cadastros
    Dado que acabei de consultar um contrato
    Quando confirmo de novo, com a mesma coordenação, o mesmo ano e o mesmo contrato
    Então a tela continua mostrando o que mostrou da primeira vez
    E os cadastros não são lidos de novo

  Cenário: Consulta não grava nada
    Dado que estou na E960T
    Quando a consulta termina
    Então nenhum cartão, contrato, órgão ou fornecedor é incluído, alterado ou excluído
    E nenhuma trilha de auditoria é gerada

  Cenário: A tela não encaminha para outra tela
    Dado que estou na E960T
    Quando a consulta termina
    Então continuo na E960T
    E nenhuma outra tela é aberta
```
