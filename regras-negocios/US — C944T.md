# US — C944T — Exclusão dos cadastros do cardápio de um período

## Estória

Como **servidor de CRE**, quero **excluir os cadastros do cardápio de um período já
encerrado**, para que **os registros daquele período saiam do sistema, em vez de se
acumularem indefinidamente no cadastro**.

O cardápio guarda um registro por período de validade: o mesmo código de cardápio
reaparece a cada versão, e é a data limite que diz qual delas está valendo. Terminado o
período, os registros dele não servem mais — é esta a tela que os retira, junto com tudo
o que depende deles. Só que ela não apaga na hora: ela **pede** a exclusão ao
processamento que roda fora da transação, e é esse processamento que apaga.

## Contexto

Jornada S000M → C000M → C800M → C900M → C944T.

Ator: servidor de CRE — informa o período que quer encerrar e confirma a exclusão dos
cadastros dele.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — a opção 9
do `C000M`, a opção 9 do `C800M` e a opção 8 do `C900M` — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio. As três telas do caminho são menus e não gravam nada: só encaminham. Esta tela
não encadeia em outra: ela reabre a si mesma — para a pergunta de confirmação e para o
aviso final — e entrega o trabalho ao processamento.

As regras abaixo são só as da tela desta jornada. Cada dúvida fica ao fim da regra a que
pertence; o lastro de tudo o que aqui se afirma está no anexo de evidências.

## Regras de negócio

### RN-01 — A tela não tem consulta: a opção de manutenção é sempre alteração

Esta tela só serve para excluir: não há modo de consulta. A cada apresentação ela repõe
a opção de manutenção em **alteração**. Quando a resposta do terminal chega, antes de ler
qualquer cadastro, a tela exige alteração: qualquer outra opção é recusada com
**\* Opcao nao disponivel. Use ALT \***, com o cursor no campo da opção, e a transação
termina ali — nada é lido e nada é excluído. O modo não vem de quem chamou a tela: quem a
abre pelo menu não escolhe consulta nem inclusão.

[?] A recusa manda usar **ALT**, mas a opção que a tela exige é a de alteração; o acervo
não traz a tradução do que o terminal envia. Ou a mensagem está desalinhada da
conferência, ou o que o servidor digita é convertido antes de chegar à tela. Pergunta ao
site.

### RN-02 — O período é informado por seis campos numéricos

O que a tela pede é o período, em duas datas: o **dia, o mês e o ano do início** e o
**dia, o mês e o ano do limite** — seis campos, todos numéricos. O ano tem quatro
dígitos; o dia e o mês, dois. O que estiver em branco vale zero; o que não for número é
recusado no próprio campo, antes de qualquer consulta aos cadastros, e o cursor volta
para o campo errado.

[?] A tela confere que os seis campos são números, e só: não confere se a data existe no
calendário nem se o ano está dentro da faixa admitida, como fazem as telas irmãs, que têm
mensagem própria para a data inválida. Aqui uma data que não existe segue para a procura
e simplesmente não acha o período (RN-03). Ou a omissão é intencional, ou a conferência
ficou de fora. Pergunta ao site.

### RN-03 — O período tem de estar cadastrado, e a tela o procura pela data limite

Com o tipo de órgão do servidor, a tela percorre as coordenações regionais escolares
cadastradas para ele e, em cada uma, procura o período cadastrado cuja data limite seja a
informada. Não achando em nenhuma, a exclusão não é aceita: **\* Salva nao cadastrada \***,
com o cursor na data limite, e a transação para ali — nada é pedido e nada é excluído.

[?] A recusa fala em "salva nao cadastrada", e "salva" não é o nome que o acervo dá a
esse período: o cadastro e os rótulos que a própria tela mostra para as datas dele usam
outros nomes. Ou "salva" é o nome de negócio do cadastro do período, ou é de uma versão
dele, ou a mensagem perdeu o sentido. Pergunta ao site.

[?] Nenhum programa deste acervo grava o cadastro dos períodos: cinco telas e três
programas de processamento o leem, e todos apenas o leem. Se nada o grava, esta
conferência nunca passa e a exclusão nunca chega a ser pedida — e a tela irmã, que copia
no sentido contrário, exige justamente o oposto: recusa quando o período **está**
registrado. Ou o cadastro é alimentado por processo de fora do acervo, ou um dos dois
caminhos é inalcançável. Pergunta ao site.

[?] A procura usa sinalizadores de leitura do gerador que não correspondem um a um às
partes da chave, e a semântica deles não está no acervo: não se conclui se a procura exige
a data limite inteira ou só parte dela, nem se a passagem de uma coordenação para a
seguinte avança de fato. Se fixar menos do que a data inteira, a procura aceita o período
de outra data. Pergunta ao site.

### RN-04 — A data de início em branco é completada pelo período cadastrado

O servidor pode informar só a data limite: achado o período, se o ano do início veio em
branco, a tela o preenche com o dia, o mês e o ano do início daquele mesmo período
cadastrado.

[?] O cadastro dos períodos guarda, além do início e do limite, outros dois períodos e
três pares de datas de referência, e esta tela só olha o início e o limite. Como a
exclusão é em cascata e não volta atrás, o acervo não diz se algum deles também deveria
ser considerado. Pergunta ao site.

### RN-05 — A exclusão só segue com a confirmação S

Achado o período, a tela ainda não exclui nada: ela guarda os seis campos informados,
pede **\* Confirma exclusao dos cadastros <S/N> ? \*** e se reapresenta. Só a resposta
**S** leva adiante. Qualquer outra resposta desfaz a confirmação, e a tela volta a pedir
o período. Trocar a data limite entre a pergunta e a resposta também desfaz a
confirmação: o que a tela guardou na pergunta é o que volta para ela e o que vale.

[?] A conferência entre a pergunta e a resposta não inclui os três campos do início:
trocar só essa data não desfaz a confirmação, e o valor guardado — o da pergunta — é o
que volta para a tela e o que vale. Pergunta ao site.

[?] Mesmo a resposta diferente de S passa pela conferência da fila (RN-06): responder N
com um pedido de exclusão em andamento mostra a recusa de "relatorio em processamento" em
vez de simplesmente desfazer a confirmação. Pergunta ao site.

### RN-06 — Só um pedido de exclusão por vez, em todo o sistema

Enquanto houver um pedido de exclusão desta operação em andamento — **de qualquer
órgão**, não só do órgão do servidor —, a tela recusa outro com **\* Relatorio em
processamento. Aguarde. \***, com o cursor no campo da resposta, e desfaz a confirmação:
o servidor precisa informar o período de novo. O pedido sai da fila quando o
processamento que exclui termina de apagar.

[?] A conferência da fila não é feita quando a tela pergunta, e sim quando recebe a
resposta: a pergunta é apresentada mesmo havendo um pedido em andamento, e a recusa só
vem depois de o servidor responder. Pergunta ao site.

### RN-07 — A confirmação deixa rastro na auditoria

Confirmada a exclusão, fica um registro na trilha de auditoria com o tipo de órgão, o
período informado como valor anterior, o valor posterior em branco, a coordenação
regional escolar da sessão, a matrícula, a estação, a data e a hora, e o número do
processo — montado com o tipo de órgão e as três partes da data limite. O cadastro que
originou a operação é a própria tela, e a operação fica registrada como **inclusão**.

[?] A exclusão confirmada é registrada na auditoria como inclusão, e não como exclusão, e
o cadastro que a originou é a própria tela, não os cadastros que o processamento vai
apagar. Ou a auditoria registra o pedido (que de fato é incluído na fila), ou o rótulo da
operação está trocado. Pergunta ao site.

### RN-08 — A exclusão é pedida ao processamento que roda fora da transação

Confirmando, a tela lê o servidor pela matrícula — para levar o correio eletrônico dele
no pedido —, cria um **pedido de processamento** com o número seguinte ao do último
pedido da fila, o tipo de órgão, o período informado, a matrícula, a estação e a data,
monta a área de parâmetros que o processamento vai receber (o código do relatório, o tipo
de órgão e as seis datas do período, a matrícula, a estação e o correio eletrônico) e o
entrega ao processamento fora da transação. A tela então se reapresenta com
**\* Cadastro sendo atualizado \***: nada foi excluído na transação e o servidor não vê o
resultado.

[?] A entrega ao processamento só acontece quando o ambiente é o produto LINC; fora dele
o pedido fica na fila sem ser executado, e o acervo não diz o que faria com ele. Pergunta
ao site.

### RN-09 — A tela não apaga nada

Dos seis cadastros que a tela enxerga, as rotinas que gravariam, apagariam ou travaram
estão todas declaradas, e **nenhuma rotina de exclusão é executada**: as duas únicas
gravações que a transação faz são a auditoria (RN-07) e o pedido de processamento
(RN-08). Quem apaga é o processamento da RN-10.

### RN-10 — O processamento apaga os cardápios do período e o que depende deles

O processamento enfileirado recebe o tipo de órgão e as seis datas do período e trabalha
em três varreduras. Na primeira, apaga os cardápios daquele tipo de órgão e daquela data
limite e, para cada cardápio, a composição dele e as referências. Na segunda, percorre as
coordenações regionais escolares do tipo de órgão e, em cada uma, apaga o cardápio de cada
dia da semana, as quantidades mês a mês e as médias por segmento daquela data limite. Na
terceira, apaga os pedidos desta exclusão e libera a fila. É exclusão em cascata, sem
volta.

[?] A varredura é pelo tipo de órgão e pela data limite, sem separar a coordenação: apaga
em todas as coordenações do tipo de órgão, embora a conferência da tela (RN-03) se
satisfaça com o período achado em qualquer uma delas. Se um tipo de órgão tiver mais de
uma coordenação, a exclusão alcança mais do que a coordenação do servidor. Pergunta ao
site.

### RN-11 — Falha de banco interrompe a transação

Todo acesso ao banco é conferido: o erro de leitura e o de gravação são despachados pela
rotina de comunicação, e a transação para ali, sem completar o resto — a auditoria e o
pedido não chegam a ser gravados.

### RN-12 — A tela exibe a descrição do órgão e a data do sistema

Além dos campos do período, a tela mostra a **descrição do órgão** e a **data do
sistema**, as duas vindas da sessão — não são digitadas —, e a linha de mensagem. As três
são apagadas da tela a cada entrada e repostas na passagem seguinte.

### RN-13 — Nada é conferido nem gravado sem a segurança de tela, de rota e de permissão

Nada acontece sem que a tela esteja cadastrada e habilitada, sem que a rota exista e sem
que o servidor tenha permissão para a operação. Na abertura, a tela lê o cadastro de
títulos que a habilita e chama a segurança de tela; antes de conferir o período e de
registrar, chama a rota e a permissão por operação, levando a matrícula, o privilégio, o
tipo de órgão, a coordenação regional escolar e o código de acesso da sessão. Qualquer
resultado diferente de OK limpa a situação e encerra a transação ali: nada é conferido,
nada é gravado e nada é auditado. Como esta tela só abre em alteração, a permissão que ela
exige é a de **alteração**.

[?] A operação que a tela realiza é uma exclusão, mas a permissão exigida é a de
alteração, e não a de exclusão: como o modo da tela é forçado em alteração (RN-01), a
permissão de exclusão nunca é consultada. Ou a exigência está certa e a exclusão é tratada
como alteração, ou a permissão conferida é a errada. Pergunta ao site.

### RN-14 — O modo não vem de quem chamou a tela; o código da tela seguinte, sim

O modo desta tela não depende de quem a chamou — é ela mesma que repõe a alteração
(RN-01). O que ela carrega de quem a chamou é o **código da tela seguinte**: a tela o
repassa à rotina de rota antes de conferir o período e, quando ele vem preenchido, a
transação é encaminhada para aquela tela em vez de seguir aqui. Sem isso, quem ler esta
estória isolada não vê que a tela de origem pode desviar a transação.

[?] O acervo não mostra quem preenche o código da tela seguinte que o registro carrega:
nenhum programa o escreve, e a máscara da tela não está no acervo. Nesta jornada, em que a
tela é aberta por menu, não se conclui se ele chega preenchido. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Exclusão dos cadastros do cardápio de um período

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o tipo de órgão, a coordenação regional escolar e o código de acesso
    E tenho acesso à tela C944T

  Cenário: RN-01 — a tela não tem consulta
    Dado que estou na tela C944T
    Quando a opção de manutenção chega diferente de alteração
    Então vejo "* Opcao nao disponivel. Use ALT *"
    E o cursor fica no campo da opção
    E nada é lido e nada é excluído

  Cenário: RN-02 — letra em um campo de data
    Quando preencho com uma letra o dia, o mês ou o ano do início ou do limite do período
    Então o campo é recusado antes de qualquer consulta
    E o cursor volta para o campo errado
    E nada é excluído

  Cenário: RN-03, RN-04 e RN-12 — informar um período cadastrado
    Dado que existe um período cadastrado com a data limite que vou informar
    Quando informo a data limite do período, deixando o ano do início em branco
    Então a tela mostra a descrição do meu órgão e a data do sistema
    E completa o início do período com o do período cadastrado

  Cenário: RN-12 — abrir a tela não grava nada
    Dado que abro a tela C944T
    Então vejo a descrição do meu órgão e a data do sistema
    E nenhum cadastro do período é lido ou gravado

  Cenário: RN-03 — período não cadastrado
    Quando informo uma data limite que não corresponde a nenhum período cadastrado para o meu tipo de órgão
    Então vejo "* Salva nao cadastrada *"
    E o cursor fica na data limite
    E a transação para ali
    E nada é pedido e nada é excluído

  Cenário: RN-05 — a pergunta de confirmação
    Dado que o período informado está cadastrado
    Quando confirmo o período
    Então vejo "* Confirma exclusao dos cadastros <S/N> ? *"
    E nada foi excluído nem pedido ainda

  Cenário: RN-05 — resposta diferente de S
    Dado que estou vendo a pergunta de confirmação
    Quando respondo N, ou deixo a resposta em branco
    Então a confirmação é desfeita
    E a tela volta a pedir o período
    E nada é pedido e nada é excluído

  Cenário: RN-05 — troca da data limite entre a pergunta e a resposta
    Dado que estou vendo a pergunta de confirmação
    Quando troco a data limite e respondo S
    Então a confirmação é desfeita
    E a tela volta a pedir o período
    E nada é pedido e nada é excluído

  Cenário: RN-06 — já existe um pedido de exclusão em andamento
    Dado que existe um pedido desta exclusão em andamento, de qualquer órgão
    Quando respondo à pergunta de confirmação
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E a confirmação é desfeita: preciso informar o período de novo
    E nada é excluído

  Cenário: RN-07, RN-08 e RN-09 — confirmar a exclusão de um período
    Dado que existe um período cadastrado e nenhum pedido em andamento
    Quando respondo S à pergunta de confirmação
    Então o sistema grava o registro na trilha de auditoria
    E cria o pedido de processamento com o período, a minha matrícula, a estação e a data
    E entrega o pedido ao processamento que roda fora da transação
    E vejo "* Cadastro sendo atualizado *"
    E nenhum cadastro do cardápio é apagado nesta transação

  Cenário: RN-10 — o processamento apaga os cadastros do período
    Dado que o pedido de exclusão foi criado para um tipo de órgão e uma data limite
    Quando o processamento assume o pedido
    Então os cardápios daquele tipo de órgão e daquela data limite são apagados
    E são apagadas a composição, as referências, o cardápio de cada dia da semana, as quantidades mês a mês e as médias por segmento desses cardápios
    E o pedido é apagado ao fim, liberando a fila

  Cenário: RN-11 — falha de banco durante a confirmação
    Dado que a gravação falha no banco
    Quando respondo S à pergunta de confirmação
    Então a transação é interrompida com a mensagem de erro do sistema
    E o pedido de exclusão não é considerado criado

  Cenário: RN-13 — sem habilitação, rota ou permissão nada acontece
    Dado que estou na tela C944T
    Quando a tela não está habilitada, ou a rota não existe, ou o meu código de acesso não tem a permissão de alteração para ela
    Então a transação termina sem conferir o período
    E nada é gravado e nenhum registro de auditoria é criado

  Cenário: RN-14 — a tela de origem desvia a transação
    Dado que a tela traz preenchido o código da tela seguinte
    Quando a tela chama a rotina de rota
    Então a transação é encaminhada para aquela tela
    E o período não chega a ser conferido
```
