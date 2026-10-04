# US — F158T — Registrar o desconto da nota fiscal de recursos próprios

## Estória

Como **servidor de CRE**, quero **consultar a nota fiscal de um fornecedor e registrar o
desconto concedido sobre ela**, para que **o desconto fique igual ao que foi negociado, o valor
de cada gênero que compõe a nota passe a refletir esse desconto e o acumulado do convênio
daquele fornecedor deixe de somar um valor que não foi pago**.

A nota chega ao sistema com o valor total, o valor dos gêneros e a parcela paga com recursos
próprios da unidade. Quando o fornecedor concede um desconto, ele não pode ficar só no total da
nota: é pelo valor de cada gênero que a prestação de contas do convênio é montada, e é esse
acumulado, por fornecedor e por competência, que a secretaria usa para conferir o que foi gasto.
Sem esta tela, a nota continua com o desconto antigo, os gêneros continuam valendo o valor cheio
e o acumulado do convênio segue somando um valor que não foi pago.

Esta tela **grava**: registra o desconto na nota, o desconto de cada gênero da nota e o
acumulado do convênio do fornecedor, e deixa o rastro das alterações na auditoria. Só não grava
no modo de consulta, e não exclui nada em nenhum modo.

## Contexto

Jornada S000M → F000M → F100M → F158T.

Ator: servidor de CRE — consulta a nota fiscal de um fornecedor pela identificação dela e
registra o desconto dado sobre ela.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**,
não regra de negócio.

A `F000M` e a `F100M` são menus: não leem cadastro de negócio nenhum e não deixam dado de
negócio para a `F158T`. O contexto que a tela usa — a matrícula, o código de acesso, o
privilégio, o tipo de órgão e o grupo (a coordenadoria regional escolar, a CRE) — é o que a
entrada deixou na sessão, e a `F158T` apenas o repassa às conferências de acesso. **Quem abre a
tela não escolhe o modo dela**: se ela abre em consulta ou em alteração vem da última operação
feita nela nesta sessão.

A `F158T` **não encadeia em outra tela**: terminada a operação, ela se reapresenta, com a nota
na tela.

O cadastro da nota fiscal que esta tela consulta e altera é o mesmo que as telas irmãs incluem e
mantêm: não há nota "desta tela". Por isso a nota que a `F158T` aceita já passou pelas
conferências daquelas telas, descritas nas jornadas de cada uma.

## Regras de negócio

### RN-01 — A F158T é a manutenção do desconto da nota fiscal: consulta a nota e altera o desconto dela

A tela trata da nota fiscal de um fornecedor e do desconto concedido sobre ela. A nota guarda o
fornecedor, o órgão, o grupo, a unidade (pelo código INEP), o modelo, o convênio e a
competência, as duas datas da nota e **quatro valores**: o total da nota, o total dos gêneros, a
parcela de recursos próprios e o desconto. São **20 campos**, e o cadastro tem capacidade para
**100.000** notas.

Cada nota tem **gêneros** — os itens —, e cada gênero guarda o código FNDE, a unidade de medida,
a quantidade, o valor unitário, o valor total do gênero e o desconto do gênero: **13 campos**,
capacidade de **100.000**. E o convênio de cada fornecedor tem um acumulado próprio, com o valor
dos gêneros, o valor das notas, o desconto e a parcela de recursos próprios somados por órgão,
grupo, unidade e competência: **9 campos**, capacidade de **100.000**.

As capacidades acima são **capacidade** — o máximo esperado, parâmetro de dimensionamento —, não
volume cadastrado.

### RN-02 — A tela mostra a nota e os valores dela; o único dado que o operador muda é o desconto

Na consulta a tela mostra a identificação da nota — número, grupo, dia, mês e ano de emissão,
dia, mês e ano da nota, competência, convênio, unidade e fornecedor —, a razão social do
fornecedor, a descrição do modelo, o nome do órgão e os quatro valores. A **data do sistema** e
a **descrição do tipo de órgão** da sessão também aparecem; as duas são informação de saída — o
usuário as vê, o terminal não as devolve — e são apagadas no começo de cada operação.

A descrição do modelo, a razão social do fornecedor e o nome do órgão vêm de outros cadastros. A
tela **não confere** se esses cadastros têm o registro: quando não têm, ela não avisa nada.

Na alteração, o único dado que o operador muda é o **desconto**. A identificação da nota não é
reescrita por esta tela: é ela que localiza o registro.

[?] Quando a descrição do modelo, a razão social do fornecedor ou o nome do órgão não existem no
cadastro, a tela não avisa e segue mostrando a nota. O que aparece no lugar — o campo em branco
ou o conteúdo que já estava na tela — não se lê no corpus. Pergunta ao site.

### RN-03 — A tela abre na consulta, e a operação só acontece no modo de alteração

Sem operação guardada, a tela assume a **consulta**; a operação usada na última vez fica
guardada na sessão e volta preenchida. A tela só admite duas operações — **alteração** e
**consulta** —, e qualquer outra é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da operação e nada é lido
nem gravado.

**Só a operação de alteração executa.** Na consulta a tela mostra a nota e termina: nada é
gravado, ainda que o desconto mostrado seja mudado na tela.

[?] A mensagem nomeia as operações como **ALT** e **CON**, mas a conferência compara o que foi
digitado com o código de operação da língua do sistema. O corpus só traz a tabela em que esse
código é a palavra de alteração e a de consulta em inglês, e não os rótulos ALT e CON. Se a
língua do site traduz um no outro, a mensagem e a conferência concordam; se não traduz, a tela
recusa **toda** operação, inclusive a que a própria mensagem pede, e a alteração desta tela fica
**inalcançável**. Pergunta ao site.

### RN-04 — A consulta identifica a nota pelo órgão da sessão, pelo fornecedor, pelo ano de entrega e pelo número da nota

A consulta exige três dados informados: o **número da nota fiscal** — senão
**\* Informe o numero da nota fiscal \*** —, o **ano de entrega** — senão
**\* Informe o ano de entrega \*** — e o **CNPJ/CPF do fornecedor** — senão
**\* Informe o CNPJ / CPF do fornecedor \***. O órgão não é digitado: vem da sessão. Nas três
recusas o cursor volta ao campo que falta e nada é lido nem gravado.

Com os três informados, a tela procura a nota por essa identificação. Não encontrando, avisa
**\* Nota fiscal nao cadastrada \*** e nada é gravado.

[?] O rótulo do ano, na tela, fala de **emissão da nota fiscal** ("ANO EMISSAO N.F."), e a
mensagem de recusa pede o **ano de entrega**. As telas irmãs que mantêm a mesma nota tratam as
duas datas como distintas — há uma de emissão e uma de entrega, com conferências próprias entre
elas. Se o rótulo está trocado, ou se as duas datas são a mesma coisa, pergunta ao site.

### RN-05 — A nota tem de ser do grupo da sessão

A nota pertence a um **grupo** — a coordenadoria regional escolar (CRE). Se a nota encontrada for
de outro grupo, a tela recusa com **\* Nota ja cadastrada em outro grupo \*** e nada é gravado.
Quando a sessão não tem grupo definido, a conferência é dispensada e a nota é aceita.

[?] A recusa é dispensada justamente quando a sessão não tem grupo. Se quem entra sem grupo
deveria ver a nota de qualquer grupo — ou se a sessão nunca chega aqui sem grupo —, o corpus lido
não diz. Pergunta ao site.

### RN-06 — A consulta só aceita nota de recursos próprios e com os valores fechados

A tela só trata nota **de recursos próprios**: se a parcela de recursos próprios da nota for
zero, recusa com **\* Nota fiscal nao e de recursos proprios \***.

E só mostra a nota quando os valores dela fecham: o **total da nota** tem de ser igual à soma do
total dos gêneros com a parcela de recursos próprios, menos o desconto. Não fechando, recusa com
**\* Falta lancar valores \***.

[?] A recusa * Falta lancar valores * protege a igualdade que esta tela mantém quando grava. Se a
nota está fora dela — e é justamente a nota errada que a secretaria precisaria corrigir —, não
há caminho nesta tela para corrigi-la: como a alteração exige a consulta antes, ela também não
pode ser alterada aqui. Se a intenção era permitir a correção por esta tela, pergunta ao site.

### RN-07 — A alteração só é aceita para a nota que já foi consultada

A alteração exige que a **mesma nota** — mesmo número, mesmo ano de entrega e mesmo fornecedor —
tenha sido consultada antes: a identificação da última nota consultada fica guardada na sessão, e
é com ela que a tela compara o que foi digitado. Não batendo, recusa com
**\* Consulte antes de atualizar \*** e nada é gravado.

Consultar outra nota troca a identificação guardada: a partir daí só a última consultada pode
ser alterada.

### RN-08 — O desconto não pode passar do valor da nota

A alteração recusa o desconto maior que a soma do total dos gêneros com a parcela de recursos
próprios, com **\* Desconto > que valor da nota \***; o cursor volta ao campo do desconto e nada
é gravado.

### RN-09 — Desconto igual ao que já está gravado não faz nada

Se o desconto informado for igual ao que a nota já tem gravado, a tela não grava, não audita
e **não avisa nada**: a operação termina e a tela volta.

### RN-10 — A alteração grava o desconto na nota e deixa o rastro na auditoria

Passadas as conferências, a alteração trava o registro da nota e o regrava com o **novo
desconto** e com o **total recalculado** — total dos gêneros mais recursos próprios, menos o novo
desconto. Antes disso grava na auditoria um registro com a operação de alteração, o cadastro de
origem, a sessão, o grupo, a matrícula, a estação de trabalho, a data e a hora, o tipo de órgão,
o número da nota como processo e as imagens anterior e nova da nota — que diferem só no desconto
e no total.

### RN-11 — O desconto é distribuído pelos gêneros da nota, proporcionalmente ao valor de cada um

Depois de gravar a nota, a tela reparte o desconto entre os **gêneros da nota**. Cada gênero
recebe a parte proporcional ao valor total dele: a tela soma o valor de todos os gêneros da nota,
divide o novo desconto por essa soma e multiplica o resultado pelo valor de cada gênero. O gênero
de **maior valor** não entra nessa conta: ele recebe o que sobrar, de modo que a soma dos
descontos dos gêneros feche exatamente com o desconto da nota. Cada gênero é travado e regravado
com o desconto dele.

[?] A repartição parte da soma dos valores dos gêneros da nota. Se a nota não tiver gênero nenhum
— ou todos com valor zerado —, a conta é uma divisão por zero, e a tela trata o resultado da
divisão com o recurso de erro de tamanho, que zera a fração; o que o sistema faz nesse caso, e se
uma nota assim chega a esta tela, não se lê no corpus. Pergunta ao site.

### RN-12 — Zerar o desconto limpa o desconto dos gêneros e devolve o total dos itens à nota

Quando o desconto informado é **zero**, a tela grava a nota com desconto zero e com o total igual
à soma do total dos gêneros com a parcela de recursos próprios, e **zera o desconto de todos os
gêneros da nota**, um a um, sem exceção. A auditoria registra a alteração da nota com a imagem
anterior preenchida e a nova sem desconto.

### RN-13 — A tela refaz o acumulado do convênio do fornecedor

Terminada a alteração da nota, a tela refaz o acumulado do convênio daquele fornecedor: soma, de
todas as notas do mesmo órgão, grupo, unidade, competência e fornecedor, o valor dos gêneros, o
valor total das notas, o desconto e a parcela de recursos próprios, e regrava o acumulado com
essas somas — a soma inclui a nota que acabou de ser alterada. A auditoria registra essa segunda
alteração, com a imagem anterior do acumulado e a nova.

[?] A tela só reescreve o acumulado que **já existe**: quando o fornecedor ainda não tem
acumulado para aquela unidade e competência, a nota é alterada, mas o acumulado não é criado e a
tela não avisa. Se o acumulado deveria existir sempre — e quem o cria não é nenhuma das telas que
gravam esse cadastro —, pergunta ao site.

### RN-14 — A consulta não grava nada, e a tela não exclui

Na consulta, a tela mostra a nota e para: nenhuma nota, nenhum gênero e nenhum acumulado de
convênio é gravado, e nenhum registro de auditoria é gerado — ainda que o desconto mostrado seja
mudado na tela.

A tela **não exclui** nada, em nenhuma operação: a exclusão da nota, dos gêneros e do acumulado
do convênio está escrita no programa e **não é executada** por caminho nenhum.

### RN-15 — Nenhuma operação acontece sem a conferência de acesso e de permissão

A abertura e cada operação passam pelas conferências comuns do sistema: a tela tem de estar
cadastrada no cadastro de telas — senão **\* Tela nao disponivel \***; o código de acesso da
matrícula tem de ter a tela autorizada — senão **\* Acesso negado para esta matricula \***; e a
operação digitada tem de constar do perfil da tela — senão
**\* Acesso negado para esta operacao \***.

Como só a alteração executa, é a permissão de **alteração** que a tela confere quando a operação
digitada é a de alteração.

[?] O perfil da tela guarda quatro permissões — inclusão, alteração, exclusão e consulta —, mas
a conferência da consulta não lê a de consulta. Quem tem a tela autorizada consulta sem essa
permissão. Se a intenção era exigi-la, o caminho não a exige. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Registrar o desconto da nota fiscal de recursos próprios

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F158T

  Cenário: A consulta mostra a nota fiscal
    Dado que informo o número, o ano de entrega e o CNPJ do fornecedor de uma nota cadastrada
    E informo a operação de consulta
    Quando peço a consulta
    Então vejo o grupo, as duas datas, a competência, o convênio, a unidade, o fornecedor, o órgão e os quatro valores da nota
    E vejo a data do sistema e a descrição do tipo de órgão da minha sessão, que não são digitáveis
    E nada é gravado

  Cenário: Consulta sem o número da nota
    Dado que deixo o número da nota fiscal em branco
    Quando peço a consulta
    Então vejo a mensagem "* Informe o numero da nota fiscal *"
    E o cursor volta ao campo do número da nota
    E nada é lido nem gravado

  Cenário: Consulta sem o ano de entrega
    Dado que informo o número da nota fiscal
    E deixo o ano de entrega em branco
    Quando peço a consulta
    Então vejo a mensagem "* Informe o ano de entrega *"
    E o cursor volta ao campo do ano
    E nada é lido nem gravado

  Cenário: Consulta sem o CNPJ do fornecedor
    Dado que informo o número da nota fiscal e o ano de entrega
    E deixo o CNPJ do fornecedor em branco
    Quando peço a consulta
    Então vejo a mensagem "* Informe o CNPJ / CPF do fornecedor *"
    E o cursor volta ao campo do CNPJ
    E nada é lido nem gravado

  Cenário: Nota fiscal não cadastrada
    Dado que informo um número de nota fiscal que não existe para aquele fornecedor e aquele ano
    Quando peço a consulta
    Então vejo a mensagem "* Nota fiscal nao cadastrada *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: Nota de outro grupo
    Dado que a nota informada pertence a outro grupo
    Quando peço a consulta
    Então vejo a mensagem "* Nota ja cadastrada em outro grupo *"
    E nada é gravado

  Cenário: Nota sem recursos próprios
    Dado que a nota informada não tem parcela de recursos próprios
    Quando peço a consulta
    Então vejo a mensagem "* Nota fiscal nao e de recursos proprios *"
    E nada é gravado

  Cenário: Nota com valores que não fecham
    Dado que o total da nota informada não é igual ao total dos gêneros mais os recursos próprios menos o desconto
    Quando peço a consulta
    Então vejo a mensagem "* Falta lancar valores *"
    E nada é gravado

  Cenário: Registrar o desconto de uma nota já consultada
    Dado que consultei a nota
    E informo um desconto menor que o valor da nota
    Quando peço a alteração
    Então a nota fica com o novo desconto e com o total recalculado
    E cada gênero da nota fica com a parte do desconto proporcional ao valor dele
    E o gênero de maior valor fica com a diferença, de modo que a soma dos descontos dos gêneros feche com o desconto da nota
    E o acumulado do convênio do fornecedor é refeito com a soma das notas do mesmo órgão, grupo, unidade e competência
    E a auditoria registra a alteração da nota e a do acumulado do convênio

  Cenário: Alterar uma nota que não foi consultada
    Dado que informo a identificação de uma nota que não foi a última consultada nesta sessão
    Quando peço a alteração
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: Desconto maior que o valor da nota
    Dado que consultei a nota
    E informo um desconto maior que o total dos gêneros somado aos recursos próprios
    Quando peço a alteração
    Então vejo a mensagem "* Desconto > que valor da nota *"
    E o cursor volta ao campo do desconto
    E nada é gravado

  Cenário: Desconto igual ao que já está gravado
    Dado que consultei a nota
    E informo o mesmo desconto que a nota já tem
    Quando peço a alteração
    Então a tela não mostra mensagem nenhuma
    E nada é gravado nem auditado

  Cenário: Zerar o desconto da nota
    Dado que consultei a nota
    E informo desconto zero
    Quando peço a alteração
    Então a nota fica com desconto zero e com o total igual ao total dos gêneros mais os recursos próprios
    E todos os gêneros da nota ficam com desconto zero
    E o acumulado do convênio do fornecedor é refeito
    E a auditoria registra a alteração da nota

  Cenário: Operação diferente de alteração e de consulta
    Quando informo uma operação diferente de ALT e de CON
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da operação
    E nada é lido nem gravado

  Cenário: A consulta não grava nada
    Dado que consultei uma nota
    E mudo o desconto mostrado na tela
    Quando peço a consulta
    Então a nota continua com o desconto que estava gravado
    E nenhum gênero e nenhum acumulado de convênio é alterado
    E nenhum registro de auditoria é gerado

  Cenário: A tela se reapresenta depois da operação
    Dado que consultei ou alterei uma nota
    Quando a operação termina
    Então a nota continua na tela, com os valores atualizados
    E não sou levado a nenhuma outra tela

  Cenário: Tela não cadastrada
    Dado que a tela F158T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Sem autorização para a tela
    Dado que o código de acesso da minha matrícula não tem a tela F158T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Sem permissão de alteração
    Dado que o perfil da tela não libera a alteração
    Quando peço a alteração com um desconto diferente do gravado
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado nem auditado
```
