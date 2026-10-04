# US — C698T — Cópia do cadastro de permissões entre tipos de contrato

## Estória

Como **servidor da Coordenação Regional de Ensino**, quero **copiar o cadastro de permissões de um
tipo de contrato para outro tipo de contrato**, para que o tipo de contrato novo já nasça com as
permissões do tipo antigo, sem ser lançado de novo item a item.

O cadastro de permissões é o que diz o que a secretaria pode comprar em cada tipo de contrato, e ele
é lançado item a item — por fornecedor, por classe, por subclasse e por gênero do objeto. Quando a
secretaria abre um tipo de contrato novo, o cadastro que ele precisa é o mesmo do tipo que já
existe, e refazê-lo à mão é trabalho grande e sujeito a erro. Esta tela recolhe o que a reprodução
exige — de que tipo de contrato e de que grupos o cadastro sai, para qual tipo de contrato ele vai e
em que período —, confere as duas pontas e agenda a reprodução. Sem ela, cada tipo de contrato novo
começaria do zero, ou seria copiado por fora do sistema.

## Contexto

Jornada S000M → C000M → C050M → C060M → C698T.
Ator: servidor de CRE — informa a origem e o destino da cópia, os grupos alcançados e o período,
confirma e agenda o processamento.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — a opção 12 do menu
`C060M` — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

A tela é aberta por uma opção de menu, e a opção não leva registro nem operação: por isso não há
nela dois comportamentos, um de consulta e outro de alteração — ela abre sempre no modo de
alteração, e é isso que a deixa agendar o pedido. Nenhuma outra tela do sistema leva a esta: ela é
a única porta da cópia. E o que ela entrega não é uma tela seguinte — é o pedido de processamento;
para mostrar a pergunta e os avisos, ela reabre a si mesma. O tipo de órgão e a coordenação regional
vêm do vínculo escolhido na entrada, e são eles que situam a secretaria sobre a qual a cópia
trabalha.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela agenda a cópia; quem copia é o processamento

A tela não copia nada enquanto é usada. Passando por todas as conferências, ela monta o pedido de
reprodução do cadastro de permissões, guarda esse pedido na fila de requisições e avisa
**\* Cadastro sendo atualizado \***. O cadastro de permissões não é tocado por ela: dos oito
cadastros que a tela enxerga, ela grava em um só, o de requisições. Até o pedido ser processado, o
tipo de contrato de destino continua sem as permissões.

[?] O que a reprodução faz com o cadastro — o que ela copia, o que deixa de fora e se mexe no tipo
de contrato de origem — não se apura nos fontes desta jornada: quem executa é o processamento que
recebe o pedido, e ele não foi lido aqui. Pergunta ao site.

### RN-02 — A cópia é identificada por dois tipos de contrato, um grupamento, uma data limite, até doze grupos e um período

Da origem vêm o tipo de contrato, o grupamento — a classificação de licitação, que aceita **9999**
para todos — e a data limite da permissão. Vêm também os grupos cujo cadastro será copiado: a tela
aceita até doze, e são coordenações regionais da secretaria. Do destino vêm o tipo de contrato que
recebe a cópia e o período de validade da permissão nova: a data inicial e a data final. O início do
período de origem aparece na tela, mas não é digitado — quem o preenche é o sistema, a partir da
permissão que servir de modelo.

Os códigos e as datas são tratados como número: o que não for número é recusado antes de qualquer
consulta, e o cursor volta ao campo. Vinte e sete campos do formulário passam por essa edição — os
dois tipos de contrato, o grupamento, os oito componentes de data dos períodos e os doze grupos.

A tela não confere os grupos informados com a coordenação regional da sessão: o que limita o alcance
é o perfil de alteração.

[?] O que o servidor vê quando essa edição recusa um campo não se apura aqui: o texto da recusa sai
de uma rotina de biblioteca que não está entre os fontes desta jornada — a tela só devolve o cursor
ao campo.

### RN-03 — A tela só funciona no modo de alteração

A tela abre no modo de alteração e só opera nele. Estando o modo em tela em qualquer outro, a
operação é recusada com **\* Operacao nao disponivel. Use ALT \***, e nada é conferido nem agendado.

[?] O material não diz o que o servidor precisa digitar para pôr a tela em alteração: os códigos de
operação vêm da tabela de textos do idioma, que não está no lote; a única pista é a própria recusa,
que manda usar ALT.

### RN-04 — O acesso à tela e a alteração dependem do perfil

Abrir a tela exige que o código de acesso do servidor esteja autorizado para ela; alterar exige que
o perfil tenha a alteração liberada. Sem a autorização da tela, ela não abre; sem a da alteração, o
pedido não é agendado.

[?] A conferência de operação examina inclusão, alteração e exclusão, e um modo em branco passa por
ela sem exame; como esta tela sempre abre em alteração e recusa os outros modos, isso não muda o que
o servidor alcança aqui — mas o material não diz se é desenho ou sobra.

### RN-05 — A permissão de origem precisa existir no grupamento informado

Antes de seguir, o sistema procura, entre as permissões do tipo de contrato de origem na secretaria,
uma cujo grupamento seja o informado — ou qualquer uma, quando o grupamento é **9999**. Não havendo
nenhuma, a cópia é recusada com **\* Permissao nao cadastrada neste grupamento \***. A permissão
encontrada é o modelo da cópia, e é dela que sai o início do período mostrado na tela. Permissões já
marcadas como excluídas não contam.

[?] A data limite informada não entra nessa procura: o sistema aceita a primeira permissão do tipo de
contrato, seja qual for a data limite dela, e é dessa primeira que sai o início do período mostrado
— não necessariamente a do grupamento informado. Se a intenção era copiar a permissão daquela data
limite, o material não diz.

[?] As consultas ao cadastro de permissões são feitas com parte da chave em branco, e o material não
diz se a leitura exige a chave exata; se exigir, só as permissões com fornecedor, classe, subclasse
e gênero zerados seriam encontradas, e a conferência responderia por menos do que existe.

### RN-06 — O tipo de contrato de destino precisa estar cadastrado

O tipo de contrato que recebe a cópia é procurado no cadastro de tipos de contrato da secretaria. Não
existindo, a cópia é recusada com **\* Tipo contrato nao cadastrado - PARA \***.

### RN-07 — Os campos que identificam a cópia são exigidos um a um, nesta ordem

A tela recusa, apontando o campo, quando falta:

| o que falta | o que se vê |
| --- | --- |
| o tipo de contrato de origem | **\* Informe o tipo contrato - DE \*** |
| o grupamento (ou 9999) | **\* Informe o grupamento ou 9999 para todos \*** |
| a data limite da permissão de origem | **\* Informe data limite da permissao - DE \*** |
| ao menos um dos grupos | **\* Informe grupos para copia \*** |
| o tipo de contrato de destino | **\* Informe o tipo contrato - PARA \*** |
| a data inicial do período de destino | **\* Informe data inicial da permissao - PARA \*** |

A data final do período de destino não tem recusa própria de campo em branco: uma data final vazia é
recusada como data inválida.

### RN-08 — As datas do período de destino precisam ser válidas, e a final não pode vir antes da inicial

As duas datas do período de destino são conferidas como data: uma data que não existe no calendário,
ou com ano fora da faixa de **1994 a 2099**, é recusada — **\* Data inicial invalida - PARA \*** para
a inicial, **\* Data final invalida - PARA \*** para a final. E a data final anterior à inicial é
recusada com **\* Data final menor que data inicial - PARA \***.

### RN-09 — Já havendo período cadastrado para o tipo de contrato de destino, as datas informadas têm de ser as mesmas

Se o tipo de contrato de destino já tiver período cadastrado em algum grupo da secretaria, o sistema
compara as datas informadas com as datas desse período e recusa quando diferem, mostrando antes a
data cadastrada: **<data> <- Data inicial dif data cadastrada \*** ou
**<data> <- Data final dif data cadastrada \***.

A conferência percorre os grupos cadastrados na secretaria, na ordem do cadastro, e para no primeiro
grupo em que o tipo de contrato de destino tiver período: ela não se limita aos grupos informados na
tela.

### RN-10 — O destino não pode já ter permissão nos grupos informados

A cópia só é agendada se o tipo de contrato de destino ainda não tiver permissão cadastrada em
nenhum dos grupos informados, dentro do grupamento informado — ou de qualquer grupamento, quando o
grupamento é **9999**. Havendo, a recusa é **\* Permissao ja cadastrada para este TC \***, apontando
o tipo de contrato de destino. Permissões marcadas como excluídas não contam.

### RN-11 — A cópia só é agendada depois da confirmação, e a confirmação vale para os dados que identificam a cópia

Passando por todas as conferências, a tela pergunta **Copia cadastro da permissao <S/N>?** e espera a
resposta. Só a resposta **S** segue. Resposta diferente de S não encerra o pedido: a tela limpa a
resposta e pergunta de novo.

A resposta só vale para os **vinte e quatro** dados que identificam a cópia — os dois tipos de
contrato, o grupamento, as três partes da data limite de origem, as três partes de cada uma das duas
datas de destino e os doze grupos. Se algum deles mudar depois da pergunta, a resposta perde a
validade e a tela pergunta outra vez, com tudo conferido de novo. O início do período de origem não
está entre esses dados: mudá-lo não invalida a resposta. Para sair sem copiar, o servidor abandona a
tela.

### RN-12 — Um pedido de cópia na fila impede outro

Se já existe requisição do relatório de cópia na fila, o novo pedido é recusado com
**\* Relatorio em processamento. Aguarde. \***, com o cursor na resposta, e nada é agendado. A
conferência é pelo relatório, não pelo servidor: o pedido pendente de qualquer colega também barra o
novo.

### RN-13 — A tela não encadeia para outra tela; o que ela entrega é o pedido

A única saída da tela é ela mesma, reaberta para mostrar a pergunta e os avisos — ela não passa
registro nem operação para uma tela seguinte, e nenhuma outra tela do sistema é aberta por ela. O
que ela entrega ao sistema é o pedido de processamento, com o tipo de contrato de origem e o de
destino, o grupamento, a data limite da origem, as datas inicial e final do destino, os doze grupos,
a matrícula de quem pediu, o terminal, o e-mail do cadastro do funcionário e a data do pedido; o
pedido recebe o número seguinte ao último emitido.

---

## Cenários BDD

```gherkin
Funcionalidade: Cópia do cadastro de permissões entre tipos de contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C698T
    E o meu perfil permite alteração

  Cenário: RN-01 — cópia agendada
    Dado que informei o tipo de contrato de origem, o grupamento, a data limite, um grupo, o tipo de contrato de destino e o período de destino válido
    Quando confirmo com S
    Então o sistema guarda o pedido na fila de requisições
    E vejo "* Cadastro sendo atualizado *"
    E o cadastro de permissões do tipo de contrato de destino continua como estava

  Cenário: RN-01 — nada é gravado antes da confirmação
    Dado que preenchi a tela com dados válidos e ainda não confirmei
    Quando a tela me apresenta a pergunta
    Então nada foi gravado na fila de requisições
    E o cadastro de permissões não muda

  Cenário: RN-02 — campo não numérico
    Quando preencho com letra um dos tipos de contrato, o grupamento, uma das datas ou um dos grupos
    Então a tela recusa o campo antes de qualquer leitura
    E o cursor volta ao campo recusado
    E nada é agendado

  Cenário: RN-03 — operação diferente de alteração
    Dado que o modo de manutenção em tela não é o de alteração
    Quando confirmo
    Então vejo "* Operacao nao disponivel. Use ALT *"
    E nada é conferido e nada é agendado

  Cenário: RN-04 — sem acesso à tela
    Dado que o meu código de acesso não está autorizado para a tela C698T
    Quando tento abri-la
    Então a tela não abre

  Cenário: RN-04 — perfil sem alteração
    Dado que o meu perfil não tem a alteração liberada
    Quando confirmo a cópia
    Então o pedido não é agendado

  Cenário: RN-05 — permissão de origem não cadastrada no grupamento
    Dado que não existe permissão do tipo de contrato de origem no grupamento que informei
    Quando confirmo
    Então vejo "* Permissao nao cadastrada neste grupamento *"
    E o cursor volta ao tipo de contrato de origem
    E nada é agendado

  Cenário: RN-05 — grupamento 9999 aceita qualquer grupamento
    Dado que informei 9999 no grupamento
    E existe ao menos uma permissão do tipo de contrato de origem na secretaria
    Quando confirmo
    Então a cópia é aceita para a conferência seguinte

  Cenário: RN-06 — tipo de contrato de destino não cadastrado
    Dado que não existe o tipo de contrato que informei para receber a cópia
    Quando confirmo
    Então vejo "* Tipo contrato nao cadastrado - PARA *"
    E o cursor volta ao tipo de contrato de destino
    E nada é agendado

  Cenário: RN-07 — falta o tipo de contrato de origem
    Dado que não informei o tipo de contrato de origem
    Quando confirmo
    Então vejo "* Informe o tipo contrato - DE *"
    E o cursor volta a esse campo
    E nada é agendado

  Cenário: RN-07 — falta o grupamento
    Dado que informei o tipo de contrato de origem e deixei o grupamento em branco
    Quando confirmo
    Então vejo "* Informe o grupamento ou 9999 para todos *"
    E o cursor volta ao grupamento

  Cenário: RN-07 — falta a data limite da origem
    Dado que deixei em branco a data limite da permissão de origem
    Quando confirmo
    Então vejo "* Informe data limite da permissao - DE *"
    E o cursor volta à data limite

  Cenário: RN-07 — faltam os grupos
    Dado que não informei nenhum dos grupos
    Quando confirmo
    Então vejo "* Informe grupos para copia *"
    E o cursor volta ao primeiro grupo
    E nada é agendado

  Cenário: RN-07 — falta o tipo de contrato de destino
    Dado que deixei em branco o tipo de contrato que recebe a cópia
    Quando confirmo
    Então vejo "* Informe o tipo contrato - PARA *"
    E o cursor volta a esse campo

  Cenário: RN-07 — falta a data inicial do período de destino
    Dado que deixei em branco a data inicial do período de destino
    Quando confirmo
    Então vejo "* Informe data inicial da permissao - PARA *"
    E o cursor volta à data inicial

  Cenário: RN-08 — data inicial do destino inválida
    Dado que informei uma data inicial que não existe no calendário, ou com ano fora de 1994 a 2099
    Quando confirmo
    Então vejo "* Data inicial invalida - PARA *"
    E o cursor volta à data inicial
    E nada é agendado

  Cenário: RN-08 — data final do destino inválida
    Dado que informei uma data final que não existe no calendário, ou com ano fora de 1994 a 2099
    Quando confirmo
    Então vejo "* Data final invalida - PARA *"
    E o cursor volta à data final
    E nada é agendado

  Cenário: RN-08 — data final anterior à inicial
    Dado que informei a data final do período de destino anterior à data inicial
    Quando confirmo
    Então vejo "* Data final menor que data inicial - PARA *"
    E o cursor volta à data final
    E nada é agendado

  Cenário: RN-09 — data inicial diferente da cadastrada
    Dado que o tipo de contrato de destino já tem período cadastrado
    E informei uma data inicial diferente da cadastrada
    Quando confirmo
    Então vejo a data cadastrada e "<- Data inicial dif data cadastrada *"
    E o cursor volta à data inicial
    E nada é agendado

  Cenário: RN-09 — data final diferente da cadastrada
    Dado que o tipo de contrato de destino já tem período cadastrado
    E informei uma data final diferente da cadastrada
    Quando confirmo
    Então vejo a data cadastrada e "<- Data final dif data cadastrada *"
    E o cursor volta à data final
    E nada é agendado

  Cenário: RN-09 — a conferência das datas vale para grupo que eu não informei
    Dado que o tipo de contrato de destino tem período cadastrado em um grupo que não está entre os doze que informei
    E as minhas datas diferem das daquele período
    Quando confirmo
    Então a cópia é recusada com a mensagem de diferença de data
    E nada é agendado

  Cenário: RN-10 — permissão já cadastrada para o tipo de contrato de destino
    Dado que o tipo de contrato de destino já tem permissão cadastrada em um dos grupos que informei
    Quando confirmo
    Então vejo "* Permissao ja cadastrada para este TC *"
    E o cursor volta ao tipo de contrato de destino
    E nada é agendado

  Cenário: RN-11 — resposta diferente de S volta à pergunta
    Dado que a tela me apresentou a pergunta "Copia cadastro da permissao <S/N>?"
    Quando respondo N
    Então a tela limpa a resposta e pergunta de novo
    E nada é agendado

  Cenário: RN-11 — mudar um dado da cópia depois de responder S invalida a resposta
    Dado que respondi S à pergunta
    Quando mudo um dos vinte e quatro dados que identificam a cópia e confirmo
    Então a resposta perde a validade
    E a tela pergunta de novo, com tudo conferido outra vez
    E nada é agendado enquanto eu não responder S de novo

  Cenário: RN-12 — pedido de cópia pendente na fila
    Dado que já existe uma requisição do relatório de cópia na fila, pedida por mim ou por um colega
    Quando confirmo a cópia
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor volta à resposta
    E nada é agendado

  Cenário: RN-13 — a tela reabre a si mesma e não encadeia para outra tela
    Dado que a cópia foi agendada
    Quando o sistema me devolve o controle
    Então a tela C698T é reaberta com o aviso
    E nenhuma outra tela é aberta no meu lugar
```
