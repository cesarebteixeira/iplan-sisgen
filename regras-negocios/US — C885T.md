# US — C885T — Excluir os registros de estimativa de um período

## Estória

Como **servidor de CRE**, quero **excluir os registros de estimativa de um período já
encerrado do meu órgão**, para que **a estimativa daquele período saia do cadastro, em
vez de continuar ocupando espaço e servindo de base a um planejamento que não existe
mais**.

A estimativa é o cardápio previsto para um período: ela é cadastrada antes de o período
começar, com a composição e as refeições amarradas às datas dele, e o planejamento do
período se refere às mesmas datas. Encerrado o período, esses registros não servem mais —
e é esta a operação que os retira. Só que ela não apaga na hora: ela **pede** a exclusão
ao processamento que roda fora da transação, e é esse processamento que apaga.

## Contexto

Jornada S000M → C000M → C800M → C811M → C885T.

Ator: servidor de CRE — informa o período da estimativa do seu órgão, confirma a exclusão
e recebe o aviso de que o cadastro está sendo excluído.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

As três telas do meio do caminho são **menus** — o `C000M`, o `C800M` e a `C811M` —, e
nenhuma delas passa registro nem operação para esta: elas apenas chamam a tela pelo nome.
A `C885T` abre sozinha, **sempre no modo de alteração**, e o que ela usa da sessão — a
matrícula, o acesso, o privilégio, a CRE e a secretaria — foi deixado pela entrada. A
tela recebe o código da tela que a chamou e o entrega à lógica de rota da entrada, mas
não o compara com nada: o comportamento dela **não muda conforme quem a chamou**.

A tela também não encadeia em outra: terminado o pedido ela **reabre a si mesma** — uma
vez para mostrar a pergunta de confirmação e outra para avisar que o cadastro está sendo
excluído. O que ela entrega não vai para uma tela seguinte, e sim para o processamento do
sistema: o serviço pedido, a secretaria e o período.

As regras abaixo são só as da tela desta jornada. As da entrada estão no documento dela;
as que se revelaram pertencer à entrada estão registradas no **anexo de evidências**, na
seção própria.

---

## Regras de negócio

### RN-01 — A tela pede a exclusão dos registros de estimativa de um período

O que a tela recolhe é o **período** — uma data de início e uma data de limite —, e o que
ela pede é que os registros de estimativa daquele período, do órgão do servidor, saiam do
cadastro. Quem apaga não é a tela: ela registra o **pedido de exclusão**, entrega-o ao
processamento que roda fora da transação e avisa o servidor; o resultado não volta para
ela. O cadastro da estimativa comporta até **100.000** registros — capacidade declarada,
o máximo esperado, parâmetro de dimensionamento, e não o volume cadastrado.

[?] O que o processamento faz com os registros — quantos apaga, em que ordem, o que faz
com o que depende deles e como libera a fila — não tem fonte nesta jornada: o programa
que atende o pedido não está entre os fontes que ela manda ler. O que dá para afirmar é o
contrato que a tela deixa: o código do serviço pedido, a secretaria e as duas datas do
período. Pergunta ao site.

### RN-02 — A tela é da estimativa do órgão da sessão, e o órgão não é digitável

Ao abrir, a tela mostra a **descrição da secretaria** (o tipo de órgão do vínculo do
servidor) e a **data do sistema**; não há campo de secretaria nem de órgão — todas as
procuras da tela são do órgão do servidor. Além do período, a tela tem o campo da
resposta da confirmação e a linha de mensagem.

### RN-03 — A tela só opera em modo de alteração

A cada apresentação a tela repõe a opção de manutenção em **alteração**. Acionada em
qualquer outra opção de manutenção, a operação é recusada com
**\* Opcao nao disponivel. Use ALT \***, o cursor volta ao campo da resposta e nada é
lido nem gravado. Essa conferência acontece depois da conferência numérica das datas e
antes de qualquer consulta ao cadastro.

[?] A recusa manda usar ALT e a conferência aceita apenas o código interno de alteração;
o acervo não traz a correspondência entre a tecla e o código. Ou o terminal traduz a
tecla antes de enviar, ou a mensagem está desalinhada da conferência. Pergunta ao site.

### RN-04 — O período é informado em seis campos numéricos

O período são **duas datas**, cada uma em dia, mês e ano: o **início** e o **limite**.
São **seis** campos, todos numéricos — o ano com quatro dígitos, o dia e o mês com dois.
Campo em branco vira zero, e o que não for número é recusado antes de qualquer consulta
ao cadastro. Depois da recusa, o cursor volta ao campo do **limite** que falhou; para os
campos do início a tela não reposiciona o cursor. Ao abrir, o cursor está no dia do
limite.

[?] Só os três campos do limite têm posição de cursor mapeada. Ou o terminal valida os
três campos do início antes de enviar, ou a recusa fica sem apontar o campo. Pergunta ao
site.

### RN-05 — A procura da estimativa é pela data de limite, e sem ela a tela recusa

A procura é feita pela **secretaria do servidor** e pela **data de limite** informada; a
data de início não entra na procura, e quem manda no limite é sempre o que foi digitado.
Não havendo estimativa daquele órgão com aquele limite, a exclusão não é aceita:
**\* Nao existem reg.de estimativa cadastrados \***, com o cursor no dia do limite, e a
transação para ali — nada é pedido e nada é apagado.

[?] A procura leva o código do cardápio zerado e, do registro que encontra, a tela só
reconfere a secretaria e as três partes da data de limite: o código do cardápio não é
reconferido. E um mesmo órgão e um mesmo limite podem ter mais de um registro de
estimativa, um por cardápio. O que os modificadores da leitura fazem não está no corpus
nem no manual: se a leitura exigir a chave exata, só serve o registro de código de
cardápio zero; se ela apenas se posicionar no conjunto e seguir adiante, serve o de menor
código. Não escolho entre os dois desfechos. Pergunta ao site.

### RN-06 — A data de início vem do cadastro, não do que foi digitado

Achado o registro, a tela repõe o **dia, o mês e o ano do início** com os do registro da
estimativa: o que tiver sido digitado ali é descartado. É essa data reposta que segue
para a pergunta de confirmação, para a trilha de auditoria e para o pedido. O limite
continua sendo o que foi digitado.

### RN-07 — A estimativa fechada não se exclui

Estimativa já **fechada** não se exclui por esta tela:
**\* Cadastro fechado para este periodo \***, com o cursor no dia do limite, e a
transação para ali. O fechamento é um estado gravado no próprio registro da estimativa,
que esta tela apenas lê: ela não fecha nem reabre período nenhum, e enquanto o período
estiver fechado não o exclui.

### RN-08 — Não se exclui enquanto houver planejamento do período

Antes de perguntar qualquer coisa, a tela verifica se existe **planejamento** para o
período — o planejamento dos cardápios por dia da semana e o das quantidades por mês.
Havendo qualquer registro de um ou de outro, a exclusão não é aceita:
**\* Nao exclua. Planejamentos cadastrados \***, com o cursor no dia do limite, e nada é
pedido: esta tela não remove planejamento, e enquanto houver qualquer um dos dois a
estimativa do período fica.

### RN-09 — A exclusão só segue com a confirmação S

Passadas as conferências, a tela ainda não exclui nada: ela repõe o período na tela,
guarda o período conferido, pergunta **\* Confirma exclusao dos cadastros <S/N> ? \***,
põe o cursor no campo da resposta e devolve a mesma tela com a pergunta. Só a resposta
**S**, com a data de limite igual à que foi guardada, leva adiante. Qualquer outra
resposta — ou a troca da data de limite entre a pergunta e a resposta — desfaz a
confirmação, e a tela volta à primeira passagem, refazendo as conferências e perguntando
de novo. A data de início não entra nessa conferência: ela é sempre reposta com a do
cadastro (RN-06), aconteça o que acontecer com o que foi digitado.

[?] Responder N — ou deixar a resposta em branco — não encerra a operação: a tela limpa a
resposta e volta às conferências, que pedem a mesma confirmação outra vez. Não há, no
caminho lido, um desfecho que encerre a operação com a resposta negativa. Pergunta ao
site.

### RN-10 — Só um pedido de exclusão por vez, em todo o sistema

Na passagem da resposta, antes de registrar, o sistema procura um pedido **desta mesma
operação** já na fila. Existindo, a recusa é
**\* Relatorio em processamento. Aguarde. \***, com o cursor no campo da resposta, e a
confirmação é desfeita: o servidor precisa informar o período de novo. Nada é registrado
nessa passagem.

[?] A procura olha só o código do serviço, sem examinar a secretaria nem a situação do
pedido: um pedido de outro órgão, ou um já atendido e ainda não retirado, também bloqueia.
E a própria tela registra o pedido **sem marcar a situação**; quem o marca como atendido,
ou o remove da fila, não está nos fontes desta jornada. Se ninguém o retirar, a exclusão
só pode ser pedida uma vez. Pergunta ao site.

### RN-11 — A confirmação deixa registro na trilha de auditoria

Confirmada a exclusão, o sistema grava um registro na **trilha de auditoria** com a tela
de origem, a operação registrada como **inclusão**, a secretaria, o período, a matrícula,
a CRE, a estação, a data e a hora — o período guardado como valor anterior e o valor
posterior em branco.

[?] O número do processo da auditoria recebe apenas o **dia da data de início** do
período, um número de 1 a 31, e não o órgão com o período. O fonte não explica a escolha,
e é esse número que distingue um registro do outro na trilha — junto com a secretaria, o
cadastro de origem, a operação e a matrícula. Pergunta ao site.

### RN-12 — A exclusão é pedida ao processamento que roda fora da transação

Confirmando, a tela lê o cadastro do funcionário pela matrícula (para o correio
eletrônico), toma o número **seguinte** ao do último pedido da fila e cria o **pedido de
exclusão** com o código do serviço, a secretaria, a matrícula, a estação e a data, e o
entrega ao serviço de processamento fora de linha, com os parâmetros do período — a
secretaria e as duas datas — e **uma cópia**. A tela então se reapresenta com
**\* Cadastro sendo excluido \***. Nada é apagado na transação: o servidor recebe o aviso
e vai embora sem ver o resultado.

[?] A entrega do serviço depende de indicadores do ambiente — o produto em execução e o
retorno da gravação — cujo valor e origem não estão nos fontes desta jornada: quando ela
não acontece, o pedido fica registrado mas o serviço não é entregue. Pergunta ao site.

[?] O número do pedido é o seguinte ao último já usado na fila; a tela não escolhe o
número sozinha, ela o lê da fila e incrementa. Se duas sessões pedirem ao mesmo tempo, o
fonte desta jornada não permite dizer o que acontece. Pergunta ao site.

### RN-13 — A tela não apaga nada

Dos **sete** cadastros que a tela enxerga, as rotinas de exclusão estão **todas
declaradas e nenhuma é executada**, e não há rotina de travamento executada. As duas
únicas gravações que a transação faz são o registro da trilha de auditoria (RN-11) e o
pedido de exclusão (RN-12). Nenhum registro de estimativa é apagado por esta tela: quem
apaga é o processamento que recebe o pedido.

### RN-14 — Falha de banco interrompe a transação

Toda leitura e toda gravação conferem o retorno do banco: o erro de leitura e o de
gravação são despachados pela rotina de comunicação do sistema, e a transação para ali.
Depois de cada gravação a tela ainda confere o sinal de aborto e sai antes de montar o
resto — quando a gravação da trilha de auditoria é interrompida, o pedido de exclusão não
chega a ser criado.

---

## Cenários BDD

```gherkin
Funcionalidade: Excluir os registros de estimativa de um período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C885T

  Cenário: RN-01, RN-05, RN-06, RN-09, RN-11, RN-12 e RN-13 — excluir a estimativa de um período
    Dado que existe estimativa cadastrada e aberta para a minha secretaria, sem planejamento do período
    E não existe pedido de exclusão desta operação na fila
    Quando informo o dia, o mês e o ano do limite, deixando o início em branco, e envio os dados
    Então vejo "* Confirma exclusao dos cadastros <S/N> ? *"
    E a data de início passa a ser a do cadastro da estimativa
    Quando respondo S
    Então vejo "* Cadastro sendo excluido *"
    E o registro da operação fica gravado na trilha de auditoria
    E o pedido de exclusão fica registrado com a minha secretaria, a minha matrícula, a estação e a data
    E o serviço é entregue ao processamento com a secretaria e as duas datas do período
    E nenhum registro de estimativa é apagado nesta transação

  Cenário: RN-02 — a tela abre na minha secretaria e com a data do sistema
    Dado que entrei com um usuário de uma secretaria
    Quando a tela C885T abre
    Então vejo a descrição da minha secretaria e a data do sistema
    E não há campo de secretaria nem de órgão

  Cenário: RN-03 — opção de manutenção diferente de ALT
    Dado que estou na tela C885T
    Quando aciono a tela em uma opção de manutenção diferente de ALT
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor volta ao campo da resposta
    E nenhuma estimativa é consultada e nada é gravado

  Cenário: RN-04 — campo de data sem número
    Quando preencho o dia, o mês ou o ano do início ou do limite com algo que não é número
    Então o campo é recusado antes de qualquer consulta ao cadastro
    E o cursor volta ao dia do limite quando a recusa é num dos campos do limite
    E nada é pedido

  Cenário: RN-05 — período sem estimativa cadastrada
    Quando informo uma data de limite que não corresponde a nenhuma estimativa da minha secretaria
    Então vejo "* Nao existem reg.de estimativa cadastrados *"
    E o cursor volta ao dia do limite
    E nada é pedido e nada é apagado

  Cenário: RN-06 — a data de início vem do cadastro da estimativa
    Dado que existe estimativa para a minha secretaria com a data de limite que vou informar
    Quando informo o período com uma data de início diferente da do cadastro
    Então a tela repõe o início com o do cadastro da estimativa
    E é essa data reposta que segue para a confirmação e para o pedido

  Cenário: RN-07 — estimativa fechada
    Dado que a estimativa do período informado já foi fechada
    Quando confirmo a data de limite
    Então vejo "* Cadastro fechado para este periodo *"
    E o cursor volta ao dia do limite
    E nada é pedido e nada é apagado

  Cenário: RN-08 — há planejamento dos cardápios por dia da semana
    Dado que existe estimativa aberta para a minha secretaria com a data de limite que vou informar
    E existe planejamento dos cardápios por dia da semana para aquele período
    Quando confirmo a data de limite
    Então vejo "* Nao exclua. Planejamentos cadastrados *"
    E o cursor volta ao dia do limite
    E nada é pedido e nada é apagado

  Cenário: RN-08 — há quantidades por mês no período
    Dado que existe estimativa aberta para a minha secretaria com a data de limite que vou informar
    E não existe planejamento por dia da semana, mas existem quantidades por mês para aquele período
    Quando confirmo a data de limite
    Então vejo "* Nao exclua. Planejamentos cadastrados *"
    E o cursor volta ao dia do limite
    E nada é pedido e nada é apagado

  Cenário: RN-09 — resposta diferente de S
    Dado que estou vendo a pergunta de confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a confirmação é desfeita
    E a tela refaz as conferências e pede a mesma confirmação outra vez
    E nada é pedido e nada é apagado

  Cenário: RN-09 — data de limite trocada entre a pergunta e a resposta
    Dado que estou vendo a pergunta de confirmação
    Quando troco a data de limite guardada e respondo S
    Então a tela não aproveita a resposta
    E refaz as conferências e pergunta de novo
    E nada é gravado

  Cenário: RN-10 — já existe um pedido de exclusão em andamento
    Dado que existe um pedido desta operação na fila, de qualquer órgão
    Quando respondo S à pergunta de confirmação
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E a confirmação é desfeita: preciso informar o período de novo
    E nada é gravado

  Cenário: RN-13 — o que a transação grava e o que ela não apaga
    Dado que confirmei a exclusão com a resposta S
    Quando a operação termina
    Então o que passa a existir é a trilha de auditoria e o pedido de exclusão
    E os sete cadastros que a tela enxerga continuam como estavam
    E nenhuma exclusão é executada pela tela

  Cenário: RN-14 — falha de banco durante a confirmação
    Dado que a gravação falha no banco
    Quando respondo S à pergunta de confirmação
    Então a transação é interrompida com a mensagem de erro do sistema
    E o pedido de exclusão não é considerado criado
```
