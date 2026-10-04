# US — N017T — Manter notas fiscais do processo

## Estória

Como **servidor da Coordenadoria Regional de Ensino que responde pela prestação de
contas**, quero **lançar no processo de despesa as notas fiscais que ele deve
reunir e retirar dele as que não devem**, para que **o processo fique com as notas
certas, o que ele consumiu do contrato seja exatamente o que as notas lançadas
valem, e a despesa possa seguir para a conferência e o pagamento**.

O processo é a pasta que amarra as notas fiscais de um fornecedor, de um contrato e
de uma fonte de recursos. Esta tela é onde a pasta recebe o conteúdo: é ela que diz
quais notas pertencem ao processo e quais não, e é ela que mantém o contrato em dia,
devolvendo ou consumindo quantidade e valor a cada entrada e saída de nota. Sem
isso, a nota fiscal ficaria solta, sem processo a que pertencer; e o contrato
continuaria comprometido com uma nota que o processo não reconhece — ou deixaria de
estar comprometido com uma que ele reconhece.

## Contexto

Jornada S000M → N000M → N050M → N016T → N017T.
Ator: servidor de CRE — escolhe a nota fiscal e diz se ela entra ou sai do processo
de prestação de contas, e confere os totais que o processo passa a ter.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US —
00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu a abre
— está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

Os passos anteriores não são todos menus. O `N000M` e o `N050M` são menus e não
gravam nada; o `N016T`, não: ele é a tela do processo e **encadeia nesta**, passando
o processo e a operação sem passar por menu nenhum. É por isso que a operação com
que esta tela abre — incluir, alterar ou consultar — **não é decidida aqui**: vem
decidida pela tela anterior (RN-02), e o processo vem junto. Esta tela também **muda
conforme quem a chamou**: ela só se deixa abrir por quatro telas e manda as demais
de volta ao menu de processos (RN-01).

Esta tela não é o fim da jornada: terminada a operação, ela entrega o processo
adiante (RN-20).

## Regras de negócio

### RN-01 — A tela só abre por quatro telas; qualquer outra origem cai no menu de processos

A tela só se deixa abrir quando vem de uma das quatro telas que tratam o processo: a
tela do processo (`N016T`), a tela de consulta do processo (`N016C`), a `N018T` e a
`N105T`. Vindo de qualquer outra origem, ela não abre: devolve o servidor ao menu de
processos (`N050M`) marcada como se tivesse saído da família da tela do processo. O
menu, ao receber essa marca, **bloqueia a opção que abre a `N016T`** e avisa
**\* Acesso deve ser feito pela tela N016T \***.

É essa marcação que fecha o cerco: sem ela, quem chegasse à tela por um caminho que
não é o do processo poderia tentar entrar de novo pelo menu; com ela, o caminho de
volta está bloqueado e o servidor é obrigado a passar pela tela do processo, que é
quem monta o processo e decide a operação.

### RN-02 — As operações são incluir, alterar e consultar, e a operação vem de quem chamou a tela

Esta tela não tem exclusão de processo nem de nota: as operações que ela conhece são
**incluir**, **alterar** e **consultar**. Qualquer outra operação é recusada com
**\* Opcao nao disponivel. Use INC, ALT ou CON \***, com o cursor de volta no campo
da operação, e nada é gravado.

A operação não é escolhida livremente aqui: ela chega decidida pela tela que chamou
esta, e esta tela a assume. A inclusão é a operação da tela do processo quando o
servidor está montando o processo; a consulta é a que chega da tela de consulta do
processo; e a alteração é a operação com que se tira uma nota do processo ou se
acrescenta outra a um processo que já existe.

Cada linha de nota traz, além do número da nota, um **código de ação** que diz o que
o servidor quer daquela nota: que ela **entre** no processo ou que ela **saia**
dele. É esse código, e não a operação da tela, que escolhe o caminho de cada linha —
e é ele também que decide qual autorização do servidor é conferida: a de inclusão,
para a nota que entra, e a de exclusão, para a nota que sai.

### RN-03 — Sem número de processo montado, a tela volta para a tela do processo

O processo desta tela é identificado pelo número de catorze dígitos, montado a partir
de quatro partes que o servidor vê na tela: o **código da secretaria**, dois dígitos
de controle, o **código do lote** e o número central. A tela refaz essa montagem a
partir do número que recebeu de quem a chamou.

Quando a montagem não resulta em número nenhum — isto é, quando não há processo com
que trabalhar —, a tela **não abre em branco nem inventa um processo**: ela devolve o
servidor à tela do processo (`N016T`) para que ele escolha ou monte o processo. A
mesma volta acontece quando o servidor pede, na própria tela, um **processo novo**:
a tela limpa o que tinha do processo anterior e devolve o controle à tela do
processo, que é quem cria processo.

[?] O campo que pede o processo novo não tem rótulo de negócio no fonte: é um campo
de um caractere, sem nome de tela associado, e o acervo não diz o que o servidor lê
nele. O que a tela faz com ele está no fonte — limpa os dados do processo anterior e
volta à tela do processo —, mas se o rótulo diz "novo processo" ou outra coisa,
pergunta ao site.

### RN-04 — Processo sem notas cadastradas não abre

Ao abrir, a tela procura a nota do processo — a que quem a chamou apontou; não
apontando nota nenhuma, a primeira nota do processo. **Não encontrando nenhuma**, a
tela avisa **\* Processo sem notas cadastradas \*** e para ali. Não é uma recusa de
operação: é a constatação de que não há o que manter, e a tela não segue para a
conferência nem para a gravação.

### RN-05 — Só se mexe em processo cuja nota esteja na situação que libera a manutenção

Antes de aceitar incluir ou alterar, a tela lê a situação da nota do processo. Se ela
não for a situação que libera a manutenção, a recusa é **\* Processo nao pode ser
modificado \***, com o cursor de volta no campo da operação, e nada é gravado. A
consulta não passa por essa conferência: ela continua liberada em qualquer situação.

[?] A tela decide duas vezes com a mesma leitura — e a segunda decisão não fecha com
esta conferência. Primeiro ela recusa a manutenção quando a situação não é a que
libera; mais adiante, lendo de novo a mesma situação, ela decide se a passagem
continua sendo consulta ou vira alteração. Como esta conferência já barra exatamente
o caso da segunda, não ficou claro pelo fonte em que situação real a passagem vira
alteração — e quando a primeira consulta não encontra nota nenhuma, a comparação
seguinte usa o que ficou da leitura anterior. Pergunta ao site.

### RN-06 — Processo em integração com o SIAFIC não recebe nem devolve nota

Existem processos que já estão em integração com o SIAFIC. A tela descobre isso
procurando, para a coordenadoria da nota, um registro de integração que aponte para
este processo. Achando, a inclusão é recusada com **\* Processo na integracao com
SIAFIC \*** — e a retirada de nota, com a mesma mensagem. Em ambos os casos o cursor
volta ao número da nota e nada é gravado.

### RN-07 — O processo tem de ser de uma coordenadoria a que o servidor tenha acesso

A tela confere se a coordenadoria regional escolar do processo é a mesma com que ela
está trabalhando. Sendo outra, a recusa é **\<- Processo pertence a outro grupo \***
e a operação para. É essa conferência que impede que uma nota seja lançada num
processo que não é da coordenadoria do servidor.

### RN-08 — A nota tem de ser do mesmo tipo de contrato e do mesmo fornecedor do processo

A nota que o servidor aponta tem de bater com o processo em duas coisas: o **tipo de
contrato** e o **fornecedor**. Tipo de contrato diferente recusa com **\<- Proc. de
outro tp contrato \***; fornecedor diferente recusa com **\<- Processo de outro
fornecedor \***. Nas duas, a tela devolve o cursor ao número da nota e não grava.

### RN-09 — O processo comporta no máximo 999 notas

O processo tem um teto de **999** notas. A tela confere se já existe nota com esse
número de ordem; existindo, a recusa é **\* Maximo qt notas no processo = 999 \***,
com o cursor no número da nota, e a nota não entra.

[?] O teto não fecha com a numeração que a própria tela dá à nota nova. A tela
procura a nota de número de ordem 999 e, conforme o que encontra, atribui à nota que
está entrando **ou o número 1 ou o número seguinte ao 999** — sem consultar as notas
que o processo já tem. Como o processo é numerado em sequência pela tela do processo,
não ficou claro pelo fonte como a nota nova recebe o seu número de ordem, nem se a
recusa dos 999 chega a acontecer. Pergunta ao site.

### RN-10 — A mesma nota não entra duas vezes no processo

A tela confere, de duas maneiras, se a nota apontada já está lançada neste processo:
pelo **número da nota dentro do processo** — recusa **\* Nota ja cadastrada neste
processo \*** — e pela combinação de **fornecedor, número da nota e ano** — recusa
**\* <- Nota ja cadastrada neste processo \***. Nas duas, o cursor volta ao número da
nota e nada é gravado.

[?] As duas conferências não usam o mesmo ano. Uma procura a nota pelo ano que o
servidor informa na linha; a outra, pelo ano corrente menos dois. O fonte não diz
qual dos dois é o ano da nota, nem por que a segunda conferência usa outro. Pergunta
ao site.

### RN-11 — Para entrar no processo, a nota tem de existir e ser compatível com ele

Antes de lançar a nota, a tela procura a nota fiscal no cadastro. **Não existindo**,
a recusa é **\* Nota nao cadastrada \***. Existindo, ela ainda tem de ser compatível
com o processo, em três conferências independentes:

- a **coordenadoria regional escolar** da nota tem de ser a do processo — recusa
  **\* Nota nao pertence a este grupo \***;
- o **tipo de contrato** da nota tem de ser o do processo — recusa **\* Nota nao
  pertence a este tipo contrato \***;
- a **fonte de recursos** da nota, quando informada, tem de ser a do processo —
  recusa **\* Nota nao pertence a esta fonte \***.

A conferência da fonte é dispensada quando a nota não tem fonte: nota sem fonte entra
em qualquer processo. Passando por tudo, a tela mostra na linha a data da nota e os
seus dois valores.

### RN-12 — A unidade orçamentária da nota e a soma dos seus itens têm de fechar com o processo

Duas conferências de conteúdo fecham a entrada da nota:

- a **unidade orçamentária** da nota — o seu órgão, como o cadastro de órgãos o
  classifica — tem de ser a mesma do processo; sendo outra, a recusa é **\* Unidade
  orcamentaria difere do processo \***;
- a **soma dos itens da nota** tem de dar exatamente o **valor total da nota**;
  somando diferente, a recusa é **\* Valor dos itens difere do total da nota \***.

Nas duas, o cursor volta ao número da nota e nada é gravado. A unidade orçamentária
mostrada na tela passa a ser a da nota.

### RN-13 — Para sair do processo, a nota tem de estar lançada nele

A retirada de uma nota — a alteração com o código de ação de saída — exige que a nota
esteja de fato lançada neste processo. Não estando, a recusa é **\* Nota nao
cadastrada neste processo \***, com o cursor no número da nota, e nada é apagado.

### RN-14 — A inclusão pergunta antes de gravar, e só grava com a resposta S

Preparada a nota para entrar, a tela **não grava**: ela mostra
**\* Confirma inclusao <S/N> ? \*** e se reapresenta, com o cursor no campo da
resposta, devolvendo ao servidor o processo e a operação. Só quando a resposta é
**S** a gravação acontece.

Respondendo qualquer outra coisa, a tela desfaz a marcação da inclusão e volta ao
estado anterior: nada foi lançado, nada foi consumido do contrato e nenhum vínculo do
processo mudou. A retirada de nota não pede essa confirmação — ela grava direto.

### RN-15 — A inclusão confirmada tira a nota do cadastro avulso e a lança no processo

Confirmada a inclusão, a tela transfere a nota: ela **cria o lançamento da nota
dentro do processo** e **apaga a nota fiscal do cadastro avulso** — a nota deixa de
existir solta, porque passou a existir dentro do processo. O caminho é o mesmo para
cada item da nota, e para cada item a tela:

- **cria o item no processo**, copiando do item da nota o gênero, a quantidade, o
  valor unitário e o valor total;
- **apaga o item da nota avulsa**;
- **consome do contrato** a quantidade e o valor do item: a quantidade ainda não
  faturada sobe, o valor comprometido sobe, a quantidade empenhada cai e o valor em
  empenho cai, na medida exata do item.

Terminados os itens, a tela lança a nota no processo com os seus valores totais e
apaga a nota avulsa. Se o processo ainda não tinha **tipo de processo**, ela registra
o tipo informado; já tendo, não mexe no tipo.

### RN-16 — A retirada confirmada devolve a nota ao cadastro avulso e desfaz o consumo do contrato

A retirada é o caminho de volta da inclusão, e é completa. Para cada item que a nota
tinha dentro do processo, a tela:

- **recria o item na nota avulsa**;
- **apaga o item do processo**;
- **devolve ao contrato** o que o item havia consumido: a quantidade ainda não
  faturada cai, o valor comprometido cai, a quantidade empenhada sobe e o valor em
  empenho sobe, na medida exata do item.

Terminados os itens, a tela **recria a nota fiscal no cadastro avulso** e **apaga o
lançamento da nota no processo** — a nota volta a existir solta, e não fica rastro
dela dentro do processo.

### RN-17 — Terminada a operação, a tela refaz o que o processo reúne e limpa os vínculos que sobraram

Terminada uma inclusão ou uma retirada, a tela percorre novamente todas as notas do
processo e refaz a conta do que ele reúne: a **quantidade de notas**, o **valor total
das notas** e o **valor total do imposto retido**. É essa conta que ela devolve.

Ela também limpa o que ficou sem sentido:

- se o processo **não tem mais nota nenhuma**, ela apaga o registro do processo no
  protocolo (o número SEI ou RIO que apontava para ele) e apaga a ligação do processo
  com o seu tipo;
- tendo ainda notas, o processo é devolvido **fechado**, com a quantidade e os totais
  recém-calculados, e o fornecedor e a fonte são relidos para a tela mostrar a razão
  social e a descrição da fonte.

Na alteração, a tela ainda procura, entre as notas do processo, a primeira que tenha
um processo SEI ou RIO registrado e grava esse mesmo número na primeira nota que não
o tenha — é essa passagem que mantém o número SEI ou RIO visível no processo.

### RN-18 — A consulta não grava nada

Na consulta, a tela não valida nota nenhuma, não pede confirmação e **não grava, não
apaga e não consome contrato**: ela apenas lê o processo, mostra o que ele reúne e os
totais das suas notas e sai. É a operação em que o servidor confere sem risco de
alterar a prestação de contas.

### RN-19 — Toda operação que grava fica registrada

Toda vez que a tela grava ou apaga — cada lançamento de nota no processo, cada nota
avulsa criada ou apagada, cada item lançado ou retirado, cada ajuste no contrato,
cada ligação de tipo de processo criada ou desfeita, cada registro de protocolo
apagado — ela deixa um registro no cadastro de auditoria (`A010T`) com o órgão, o
processo, o cadastro tocado, a operação, a matrícula, a estação, a data, a hora e o
valor antes e o valor depois. É esse rastro que permite reconstruir quem lançou e
quem retirou cada nota.

### RN-20 — O que a tela entrega à tela seguinte

Esta tela não termina sozinha. Do seu desfecho saem quatro caminhos, e o que ela
entrega vai junto:

- **de volta à tela de consulta do processo (`N016C`)**, quando o servidor marca o
  indicador de consulta na própria tela: ela refaz a conta das notas do processo e
  entrega o processo com os totais apurados, identificando-se como origem;
- **de volta à tela do processo (`N016T`)**, quando o servidor pede um processo novo:
  a tela limpa o processo anterior e passa o pedido adiante, que é quem cria
  processo;
- **de volta a si mesma**, para colher a resposta da pergunta de confirmação da
  inclusão (RN-14): nesse caminho ela não grava nada e apenas se reapresenta com a
  pergunta;
- **de volta ao menu de processos (`N050M`)**, quando a origem não é uma das quatro
  telas aceitas (RN-01).

[?] O indicador que leva o processo de volta à tela de consulta não tem rótulo de
negócio no fonte: ele é um campo de um caractere, sem nome de tela associado, e o
acervo não diz o que o servidor lê nele. Nas telas irmãs o mesmo campo é usado para
pedir a consulta; aqui ele devolve o processo com os totais. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Notas fiscais do processo de prestação de contas — lançar e retirar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N017T

  Cenário: RN-01 — a tela abre pelo caminho do processo
    Dado que abri a tela vindo da tela do processo N016T
    Então a tela abre sobre o processo que a tela anterior deixou
    E não me desvia para o menu de processos

  Cenário: RN-01 — origem não reconhecida cai no menu e a opção fica bloqueada
    Dado que cheguei à tela por um caminho que não é o do processo
    Então volto ao menu de processos N050M marcado como vindo da família da tela do processo
    E o menu bloqueia a opção que abre a N016T
    E vejo * Acesso deve ser feito pela tela N016T *

  Cenário: RN-02 — recusa uma operação que não é incluir, alterar nem consultar
    Dado que enviei a tela com uma operação diferente das três
    Então vejo * Opcao nao disponivel. Use INC, ALT ou CON *
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: RN-02 — a operação vem decidida pela tela anterior
    Dado que a tela do processo me passou o processo e uma operação
    Então a tela abre com aquela operação
    E não me pede para escolher a operação

  Cenário: RN-03 — sem número de processo a tela volta para a tela do processo
    Dado que o processo recebido não forma número nenhum
    Então volto à tela do processo N016T para escolher ou montar o processo
    E nada é gravado

  Cenário: RN-03 — pedido de processo novo volta para a tela do processo
    Dado que estou na tela sobre um processo
    Quando peço um processo novo
    Então o processo anterior é limpo
    E volto à tela do processo N016T, que é quem cria processo

  Cenário: RN-04 — processo sem notas cadastradas
    Dado que o processo não tem nenhuma nota lançada
    Quando a tela abre
    Então vejo * Processo sem notas cadastradas *
    E a tela para ali

  Cenário: RN-05 — recusa mexer em processo que não está na situação que libera
    Dado que a situação da nota do processo não é a que libera a manutenção
    Quando escolho incluir ou alterar e envio
    Então vejo * Processo nao pode ser modificado *
    E o cursor volta ao campo da operação
    E nada é gravado

  Cenário: RN-05 — a consulta continua liberada
    Dado que a situação da nota do processo não é a que libera a manutenção
    Quando escolho consultar e envio
    Então a tela mostra o processo
    E não vejo a recusa de manutenção

  Cenário: RN-06 — recusa incluir nota em processo em integração com o SIAFIC
    Dado que o processo está em integração com o SIAFIC
    Quando aponto uma nota para entrar e envio
    Então vejo * Processo na integracao com SIAFIC *
    E o cursor volta ao número da nota
    E nada é gravado

  Cenário: RN-06 — recusa retirar nota de processo em integração com o SIAFIC
    Dado que o processo está em integração com o SIAFIC
    Quando aponto uma nota do processo para sair e envio
    Então vejo * Processo na integracao com SIAFIC *
    E nada é apagado

  Cenário: RN-07 — recusa processo de outra coordenadoria
    Dado que o processo é de uma coordenadoria regional escolar diferente da minha
    Quando envio a tela
    Então vejo * <- Processo pertence a outro grupo *
    E nada é gravado

  Cenário: RN-08 — recusa nota de outro tipo de contrato
    Dado que a nota apontada é de um tipo de contrato diferente do processo
    Quando envio a tela
    Então vejo * <- Proc. de outro tp contrato *
    E o cursor volta ao número da nota
    E nada é gravado

  Cenário: RN-08 — recusa nota de outro fornecedor
    Dado que a nota apontada é de um fornecedor diferente do processo
    Quando envio a tela
    Então vejo * <- Processo de outro fornecedor *
    E nada é gravado

  Cenário: RN-09 — recusa quando o processo já tem nota no número de ordem 999
    Dado que o processo já tem uma nota com o número de ordem 999
    Quando aponto uma nota para entrar e envio
    Então vejo * Maximo qt notas no processo = 999 *
    E o cursor volta ao número da nota
    E nada é gravado

  Cenário: RN-10 — recusa nota que já está lançada neste processo
    Dado que a nota apontada já está lançada neste processo
    Quando envio a tela
    Então vejo * Nota ja cadastrada neste processo *
    E o cursor volta ao número da nota
    E nada é gravado

  Cenário: RN-10 — recusa nota que já está no processo pelo fornecedor e pelo ano
    Dado que a combinação de fornecedor, número da nota e ano já está lançada neste processo
    Quando envio a tela
    Então vejo * <- Nota ja cadastrada neste processo *
    E nada é gravado

  Cenário: RN-11 — recusa nota que não está cadastrada
    Dado que aponto uma nota que não existe no cadastro de notas fiscais
    Quando envio a tela
    Então vejo * Nota nao cadastrada *
    E o cursor volta ao número da nota
    E nada é gravado

  Cenário: RN-11 — recusa nota de outra coordenadoria
    Dado que a coordenadoria regional escolar da nota é diferente da do processo
    Quando aponto essa nota para entrar e envio
    Então vejo * Nota nao pertence a este grupo *
    E nada é gravado

  Cenário: RN-11 — recusa nota de outro tipo de contrato
    Dado que o tipo de contrato da nota é diferente do processo
    Quando aponto essa nota para entrar e envio
    Então vejo * Nota nao pertence a este tipo contrato *
    E nada é gravado

  Cenário: RN-11 — recusa nota de outra fonte
    Dado que a fonte de recursos da nota é diferente da do processo
    Quando aponto essa nota para entrar e envio
    Então vejo * Nota nao pertence a esta fonte *
    E nada é gravado

  Cenário: RN-11 — nota sem fonte entra em qualquer processo
    Dado que a nota apontada não tem fonte de recursos
    Quando envio a tela
    Então a tela não recusa a nota por causa da fonte
    E mostra na linha a data e os dois valores da nota

  Cenário: RN-12 — recusa nota de outra unidade orçamentária
    Dado que a unidade orçamentária da nota difere da do processo
    Quando aponto essa nota para entrar e envio
    Então vejo * Unidade orcamentaria difere do processo *
    E o cursor volta ao número da nota
    E nada é gravado

  Cenário: RN-12 — recusa nota cujos itens não somam o total da nota
    Dado que a soma dos itens da nota é diferente do valor total dela
    Quando aponto essa nota para entrar e envio
    Então vejo * Valor dos itens difere do total da nota *
    E nada é gravado

  Cenário: RN-13 — recusa retirar nota que não está lançada no processo
    Dado que aponto para sair uma nota que não está lançada neste processo
    Quando envio a tela
    Então vejo * Nota nao cadastrada neste processo *
    E o cursor volta ao número da nota
    E nada é apagado

  Cenário: RN-14 — a inclusão pergunta antes de gravar
    Dado que a nota apontada passou por todas as conferências
    Quando envio a tela
    Então vejo * Confirma inclusao <S/N> ? *
    E a tela se reapresenta com a pergunta
    E nada foi lançado ainda

  Cenário: RN-14 — respondendo N, nada é gravado
    Dado que vejo a pergunta de confirmação da inclusão
    Quando respondo qualquer coisa que não seja S
    Então a marcação da inclusão é desfeita
    E nada foi lançado no processo
    E nada foi consumido do contrato

  Cenário: RN-15 — a inclusão confirmada lança a nota no processo
    Dado que a nota apontada passou por todas as conferências
    Quando respondo S à confirmação da inclusão
    Então o lançamento da nota é criado dentro do processo
    E a nota fiscal deixa de existir no cadastro avulso
    E cada item da nota vira item do processo
    E o contrato fica com a quantidade e o valor do item consumidos

  Cenário: RN-15 — a inclusão registra o tipo do processo quando ele não tem
    Dado que o processo ainda não tem tipo de processo
    Quando confirmo a inclusão de uma nota
    Então o tipo de processo informado fica ligado ao processo

  Cenário: RN-16 — a retirada devolve a nota e desfaz o consumo do contrato
    Dado que a nota está lançada neste processo
    Quando envio a tela com o código de ação de saída
    Então o lançamento da nota é apagado do processo
    E a nota fiscal volta a existir no cadastro avulso
    E cada item volta a ser item da nota
    E o contrato recebe de volta a quantidade e o valor que o item havia consumido

  Cenário: RN-17 — terminada a operação, a tela refaz os totais do processo
    Dado que confirmei uma inclusão ou uma retirada
    Então a tela mostra a quantidade de notas e os dois totais do processo
    E o processo é devolvido fechado
    E a razão social do fornecedor e a descrição da fonte aparecem na tela

  Cenário: RN-17 — processo que fica sem nota perde os vínculos
    Dado que retirei a última nota do processo
    Quando a operação termina
    Então o registro do processo no protocolo é apagado
    E a ligação do processo com o seu tipo é apagada
    E o processo fica sem notas e sem totais

  Cenário: RN-18 — a consulta não grava nada
    Dado que o processo existe e é da minha coordenadoria
    Quando escolho consultar e envio
    Então a tela mostra o processo, a quantidade de notas e os seus totais
    E nenhuma nota é validada
    E nada é gravado, apagado ou consumido do contrato

  Cenário: RN-19 — toda operação que grava fica registrada
    Dado que confirmei uma inclusão ou uma retirada
    Então fica registrado o cadastro tocado, a operação, o meu órgão, o processo e a minha matrícula
    E ficam registrados a estação, a data, a hora e o valor antes e o valor depois

  Cenário: RN-20 — marcado o indicador, o processo volta à tela de consulta com os totais
    Dado que estou na tela sobre um processo com notas
    Quando marco o indicador de consulta
    Então a tela refaz a conta das notas do processo
    E entrega o processo e os totais à tela de consulta do processo N016C
    E se identifica como origem

  Cenário: RN-20 — pedido de processo novo vai à tela do processo
    Dado que estou na tela sobre um processo
    Quando peço um processo novo
    Então o processo anterior é limpo
    E o controle volta à tela do processo N016T

  Cenário: RN-20 — a tela se reapresenta para colher a confirmação
    Dado que preparei uma nota para entrar no processo
    Quando envio a tela
    Então a própria tela se reapresenta com a pergunta de confirmação
    E nada foi gravado antes da minha resposta
```
